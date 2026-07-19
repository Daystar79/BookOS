"""Ledger / log integrity checks — CLEAN vs BLOCKED."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from . import card_io, ledger_io, logs_io
from .paths import DRAFTS, ROOT, rel


class Severity(str, Enum):
    BLOCK = "BLOCK"
    WARN = "WARN"
    INFO = "INFO"


@dataclass
class Issue:
    severity: Severity
    code: str
    message: str


@dataclass
class IntegrityReport:
    issues: list[Issue] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return any(i.severity == Severity.BLOCK for i in self.issues)

    @property
    def status(self) -> str:
        if self.blocked:
            return "BLOCKED"
        if any(i.severity == Severity.WARN for i in self.issues):
            return "CLEAN (warnings)"
        return "CLEAN"

    def add(self, severity: Severity, code: str, message: str) -> None:
        self.issues.append(Issue(severity, code, message))


def _draft_candidates() -> list[Path]:
    if not DRAFTS.is_dir():
        return []
    out: list[Path] = []
    for path in DRAFTS.rglob("draft_chapter_*.md"):
        out.append(path)
    return out


def check_integrity(*, strict_samples: bool = False) -> IntegrityReport:
    """
    Run integrity pass.

    BLOCK:
      - placeholder ledger rows
      - ledger rows whose draft file is missing
      - character logs missing snapshot fields when file exists empty
    WARN:
      - draft_chapter_* outside samples/ with no ledger row
      - log history without matching ledger movement (demo drift)
      - consolidated log staleness is not checked (regenerated on commit)
    """
    report = IntegrityReport()
    rows = ledger_io.parse_ledger()
    logs = logs_io.load_all_logs()
    cards = {c.slug.lower(): c for c in card_io.list_cards()}

    committed_ids: set[str] = set()
    committed_drafts: set[Path] = set()

    for row in rows:
        if row.is_placeholder():
            report.add(
                Severity.BLOCK,
                "placeholder_row",
                f"Placeholder continuity row under {row.act}: {row.ch_mov!r}",
            )
            continue
        draft = row.draft_path()
        if draft is None:
            report.add(
                Severity.BLOCK,
                "missing_draft_ref",
                f"Ledger {row.ch_mov!r} has empty draft path",
            )
            continue
        if not draft.is_file():
            report.add(
                Severity.BLOCK,
                "orphan_ledger",
                f"Ledger {row.ch_mov!r} points to missing draft: {rel(draft)}",
            )
        else:
            committed_drafts.add(draft.resolve())
            committed_ids.add(row.movement_id)
            # also store ch_mov forms
            committed_ids.add(row.ch_mov.strip().lower())

    # Orphan drafts (not under samples unless strict)
    for draft in _draft_candidates():
        under_samples = "samples" in draft.parts
        if under_samples and not strict_samples:
            continue
        if draft.resolve() in committed_drafts:
            continue
        # ignore README
        if draft.name.lower() == "readme.md":
            continue
        sev = Severity.WARN if under_samples else Severity.WARN
        report.add(
            sev,
            "uncommitted_draft",
            f"Draft has no continuity row: {rel(draft)} (run midlayer commit after approval)",
        )

    # Logs without snapshots
    for slug, data in logs.items():
        snap = data.get("snapshot")
        if not snap or not isinstance(snap, dict):
            report.add(
                Severity.BLOCK,
                "empty_snapshot",
                f"Log {slug}_log.yaml missing snapshot — seed from card",
            )
            continue
        if not str(snap.get("active_focus") or "").strip() and not str(
            snap.get("default_somatic") or ""
        ).strip():
            report.add(
                Severity.BLOCK,
                "empty_snapshot",
                f"Log {slug}_log.yaml has empty snapshot focus/somatic — seed from card",
            )

        # Card missing for log
        if slug.lower() not in cards:
            report.add(
                Severity.WARN,
                "log_without_card",
                f"Log exists for {slug} but no Characters/{slug}.md card",
            )

        history = data.get("history") or []
        if history and not rows:
            report.add(
                Severity.WARN,
                "history_without_ledger",
                f"{slug}: history entries exist but Continuity_Ledger has no committed rows "
                f"(demo drift or incomplete commit)",
            )
        elif history and rows:
            # soft check: any history movement string overlapping ledger
            ledger_blob = " ".join(r.ch_mov.lower() for r in rows) + " " + " ".join(
                committed_ids
            )
            unmatched = 0
            for entry in history:
                if not isinstance(entry, dict):
                    continue
                mov = str(entry.get("movement") or "").lower()
                if not mov:
                    continue
                # match chapter_1_m1 or "1 M1"
                token_hit = False
                for rid in committed_ids:
                    if rid in mov.replace(" ", "_") or mov in rid:
                        token_hit = True
                        break
                if not token_hit:
                    # try digits
                    m = ledger_io.MOV_RE_ALT.search(mov) or ledger_io.MOV_RE.search(mov)
                    if m and f"chapter_{m.group(1)}_m{m.group(2)}" in committed_ids:
                        token_hit = True
                if not token_hit:
                    unmatched += 1
            if unmatched and not any(
                "history_without_ledger" in i.code for i in report.issues if i.message.startswith(slug)
            ):
                report.add(
                    Severity.WARN,
                    "history_ledger_mismatch",
                    f"{slug}: {unmatched} history entr(y/ies) do not match ledger movement ids",
                )

    # Cards without logs
    for slug, card in cards.items():
        if slug not in {s.lower() for s in logs}:
            report.add(
                Severity.WARN,
                "card_without_log",
                f"Card {card.slug}.md has no {card.slug}_log.yaml (seed before drafting)",
            )

    if not report.issues:
        report.add(Severity.INFO, "ok", "No integrity issues. Honest empty is valid.")

    return report


def format_report(report: IntegrityReport) -> str:
    lines = [
        f"Ledger integrity: {report.status}",
        f"Issues: {len([i for i in report.issues if i.severity != Severity.INFO])}",
        "",
    ]
    for issue in report.issues:
        if issue.severity == Severity.INFO and report.status.startswith("CLEAN") and len(report.issues) == 1:
            lines.append(f"  · {issue.message}")
            continue
        if issue.severity == Severity.INFO:
            continue
        lines.append(f"  [{issue.severity.value}] {issue.code}: {issue.message}")
    if report.blocked:
        lines.append("")
        lines.append("Drafting is blocked until BLOCK issues are resolved.")
        lines.append("Fix ledger/logs, or run: python3 scripts/run.py midlayer commit …")
    return "\n".join(lines)
