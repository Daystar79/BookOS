"""Continuity_Ledger.md parse and write helpers."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .paths import CONTINUITY_LEDGER, ROOT

PLACEHOLDER_RE = re.compile(
    r"\[Day & Time\]|\[Somatic|\[Crucial|\[Ch / Mov\]|TODO|TBD|placeholder",
    re.I,
)

# Ch / Mov cells like "1 M1", "Ch1 M2", "1 / M1"
MOV_RE = re.compile(
    r"(?:ch(?:apter)?\s*)?(\d+)\s*[/ ]\s*m(?:ov(?:ement)?)?\s*(\d+)",
    re.I,
)
MOV_RE_ALT = re.compile(r"^(\d+)\s+M(\d+)\b", re.I)


@dataclass
class LedgerRow:
    act: str
    ch_mov: str
    draft_file: str
    day_time: str
    somatic: str
    beats: str
    line_index: int  # 0-based line of table row in full file

    @property
    def chapter(self) -> int | None:
        m = MOV_RE.search(self.ch_mov) or MOV_RE_ALT.search(self.ch_mov.strip())
        return int(m.group(1)) if m else None

    @property
    def movement(self) -> int | None:
        m = MOV_RE.search(self.ch_mov) or MOV_RE_ALT.search(self.ch_mov.strip())
        return int(m.group(2)) if m else None

    @property
    def movement_id(self) -> str:
        if self.chapter is not None and self.movement is not None:
            return f"chapter_{self.chapter}_m{self.movement}"
        return re.sub(r"\s+", "_", self.ch_mov.strip().lower())

    def is_placeholder(self) -> bool:
        blob = " ".join(
            [self.ch_mov, self.draft_file, self.day_time, self.somatic, self.beats]
        )
        if PLACEHOLDER_RE.search(blob):
            return True
        if not self.ch_mov.strip() or self.ch_mov.strip() in ("—", "-", "…"):
            return True
        return False

    def draft_path(self) -> Path | None:
        raw = self.draft_file.strip()
        if not raw or raw in ("—", "-", "…"):
            return None
        # strip markdown links [[x]] or [text](path)
        m = re.search(r"\(([^)]+)\)", raw)
        if m:
            raw = m.group(1)
        raw = raw.strip("`[]() ")
        raw = raw.replace("[[", "").replace("]]", "")
        # common: Drafts/... or bare filename
        candidates = [
            ROOT / raw,
            ROOT / "Drafts" / raw,
            ROOT / "Drafts" / "samples" / raw,
            ROOT / "Drafts" / f"{raw}.md" if not raw.endswith(".md") else ROOT / "Drafts" / raw,
        ]
        if not raw.endswith(".md"):
            candidates.append(ROOT / "Drafts" / f"{raw}.md")
            candidates.append(ROOT / "Drafts" / "samples" / f"{raw}.md")
        for c in candidates:
            if c.is_file():
                return c
        # return first relative interpretation even if missing (caller checks exists)
        if raw.startswith("Drafts/") or raw.startswith("Framework/"):
            return ROOT / raw
        return ROOT / "Drafts" / (raw if raw.endswith(".md") else f"{raw}.md")


def _split_table_row(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    # skip separator rows
    if re.match(r"^\|[\s:|\-]+\|$", s) or re.match(r"^\|[\s\-:|]+\|$", s.replace(" ", "")):
        # more reliable:
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and all(re.match(r"^:?-+:?$", c.replace(" ", "")) for c in cells if c):
            return None
    cells = [c.strip() for c in s.strip().strip("|").split("|")]
    return cells


def parse_ledger(text: str | None = None) -> list[LedgerRow]:
    if text is None:
        if not CONTINUITY_LEDGER.is_file():
            return []
        text = CONTINUITY_LEDGER.read_text(encoding="utf-8")

    lines = text.splitlines()
    rows: list[LedgerRow] = []
    current_act = "Unknown"
    in_table = False
    header_seen = False

    for i, line in enumerate(lines):
        h = re.match(r"^##\s+(Act\s+\w+|.+)$", line.strip())
        if h and not line.strip().startswith("###"):
            title = h.group(1).strip()
            if title.lower().startswith("act") or title in (
                "Act One",
                "Act Two",
                "Act Three",
            ):
                current_act = title
                in_table = False
                header_seen = False
            continue

        cells = _split_table_row(line)
        if cells is None:
            # blank or note under section
            if line.strip().startswith("*(no approved"):
                in_table = False
            continue

        # header row only (first cell is the Ch/Mov label — not data like "1 M1")
        first = (cells[0] if cells else "").strip().lower()
        if first in ("ch / mov", "ch/mov", "chapter / movement", "movement") or (
            "mov" in first and first.startswith("ch") and not re.search(r"\d", first)
        ):
            in_table = True
            header_seen = True
            continue

        # separator already filtered by _split_table_row returning None for --- rows
        # but some separators slip through
        if cells and all(re.match(r"^:?-+:?$", c.replace(" ", "") or "-") for c in cells):
            continue

        if not header_seen and not in_table:
            continue

        # data row — need at least 5 columns ideally
        while len(cells) < 5:
            cells.append("")
        ch_mov, draft, day, somatic, beats = cells[0], cells[1], cells[2], cells[3], cells[4]
        if not ch_mov and not draft:
            continue
        rows.append(
            LedgerRow(
                act=current_act,
                ch_mov=ch_mov,
                draft_file=draft,
                day_time=day,
                somatic=somatic,
                beats=beats,
                line_index=i,
            )
        )
        in_table = True

    return rows


def append_ledger_row(
    *,
    act: str,
    ch_mov: str,
    draft_file: str,
    day_time: str,
    somatic: str,
    beats: str,
    path: Path | None = None,
) -> None:
    path = path or CONTINUITY_LEDGER
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Find ## Act section
    act_header = f"## {act}"
    act_idx = None
    for i, line in enumerate(lines):
        if line.strip() == act_header or line.strip().lower() == act_header.lower():
            act_idx = i
            break
    if act_idx is None:
        # append new act section at end
        lines.extend(
            [
                "",
                act_header,
                "",
                "| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |",
                "| :---: | :--- | :--- | :--- | :--- |",
                f"| {ch_mov} | {draft_file} | {day_time} | {somatic} | {beats} |",
                "",
            ]
        )
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return

    # Find table under act: header + separator, then rows; remove empty note
    header_idx = None
    sep_idx = None
    for j in range(act_idx + 1, len(lines)):
        if lines[j].startswith("## "):
            break
        if "Ch / Mov" in lines[j] and lines[j].strip().startswith("|"):
            header_idx = j
            if j + 1 < len(lines) and re.search(r"\|[\s:-]+\|", lines[j + 1]):
                sep_idx = j + 1
            break

    new_row = f"| {ch_mov} | {draft_file} | {day_time} | {somatic} | {beats} |"

    if header_idx is None:
        # insert table after act header
        insert_at = act_idx + 1
        block = [
            "",
            "| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |",
            "| :---: | :--- | :--- | :--- | :--- |",
            new_row,
            "",
        ]
        lines[insert_at:insert_at] = block
    else:
        # remove *(no approved movements)* under this act
        end = header_idx
        for j in range(header_idx, len(lines)):
            if j > header_idx and lines[j].startswith("## "):
                break
            end = j
            if lines[j].strip().startswith("*(no approved"):
                lines[j] = ""
        insert_at = (sep_idx + 1) if sep_idx is not None else (header_idx + 1)
        # find last data row after separator
        last_data = insert_at
        for j in range(insert_at, len(lines)):
            if lines[j].startswith("## "):
                break
            if lines[j].strip().startswith("|") and "Ch / Mov" not in lines[j]:
                cells = _split_table_row(lines[j])
                if cells is not None:
                    last_data = j + 1
            elif lines[j].strip() == "" or lines[j].strip().startswith("*("):
                if lines[j].strip().startswith("*("):
                    lines[j] = ""
                break
        lines.insert(last_data, new_row)

    # compact double blanks lightly
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
