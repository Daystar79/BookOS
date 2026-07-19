"""Atomic post-movement state commit."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import card_io, ledger_io, logs_io
from .paths import ROOT, rel


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass
class CharacterCommit:
    slug: str
    pressure: str = "Emotional"
    strength: str = "Medium"
    notes: str = ""
    delta: str | None = None
    permanence: str | None = None
    somatic: str | None = None
    bias_delta: int | None = None
    skip_matrix: bool = False  # ledger presence only


@dataclass
class CommitRequest:
    movement: str  # e.g. "1 M1"
    draft: Path
    day_time: str
    somatic: str
    beats: str
    slugs: list[str]
    act: str = "Act One"
    title: str = ""
    characters: list[CharacterCommit] = field(default_factory=list)
    expected_revisions: dict[str, int] = field(default_factory=dict)
    pressure_default: str = "Emotional/Social"
    strength_default: str = "Medium"


class CommitError(Exception):
    pass


def _movement_id(movement: str, title: str = "") -> str:
    m = ledger_io.MOV_RE.search(movement) or ledger_io.MOV_RE_ALT.search(movement.strip())
    if m:
        base = f"chapter_{int(m.group(1))}_m{int(m.group(2))}"
    else:
        base = re.sub(r"[^a-z0-9]+", "_", movement.lower()).strip("_")
    if title:
        return f"{base} — {title}"
    return base


def _ch_mov_cell(movement: str) -> str:
    m = ledger_io.MOV_RE.search(movement) or ledger_io.MOV_RE_ALT.search(movement.strip())
    if m:
        return f"{int(m.group(1))} M{int(m.group(2))}"
    return movement.strip()


def parse_character_json(raw: str | None, slugs: list[str], pressure: str, strength: str) -> list[CharacterCommit]:
    if not raw:
        return [
            CharacterCommit(slug=s, pressure=pressure, strength=strength) for s in slugs
        ]
    data = json.loads(raw)
    if not isinstance(data, list):
        raise CommitError("--character-json must be a JSON list")
    out: list[CharacterCommit] = []
    for item in data:
        if not isinstance(item, dict) or "slug" not in item:
            raise CommitError("each character entry needs a slug")
        out.append(
            CharacterCommit(
                slug=str(item["slug"]),
                pressure=str(item.get("pressure") or pressure),
                strength=str(item.get("strength") or strength),
                notes=str(item.get("notes") or ""),
                delta=item.get("delta"),
                permanence=item.get("permanence"),
                somatic=item.get("somatic"),
                bias_delta=item.get("bias_delta"),
                skip_matrix=bool(item.get("skip_matrix", False)),
            )
        )
    return out


def run_commit(req: CommitRequest) -> dict[str, Any]:
    draft = req.draft
    if not draft.is_file():
        # try relative to root
        alt = ROOT / draft
        if alt.is_file():
            draft = alt
        else:
            raise CommitError(f"Draft not found: {req.draft}")

    draft_rel = rel(draft)

    # Existing ledger: refuse duplicate draft path
    for row in ledger_io.parse_ledger():
        p = row.draft_path()
        if p and p.resolve() == draft.resolve():
            raise CommitError(f"Draft already committed in ledger: {draft_rel}")

    ch_mov = _ch_mov_cell(req.movement)
    if req.title:
        # title stays out of ch/mov cell; used in history labels
        pass
    mov_label = f"{ch_mov}" + (f" — {req.title}" if req.title else "")
    commit_id = _movement_id(req.movement, "")

    # Ensure character commits cover slugs
    by_slug = {c.slug.lower(): c for c in req.characters}
    for s in req.slugs:
        if s.lower() not in by_slug:
            by_slug[s.lower()] = CharacterCommit(
                slug=s,
                pressure=req.pressure_default,
                strength=req.strength_default,
            )

    cards = {c.slug.lower(): c for c in card_io.list_cards()}
    results: dict[str, Any] = {"draft": draft_rel, "movement": mov_label, "logs": {}}

    for slug_l, cc in by_slug.items():
        slug = cc.slug
        log_path = ROOT / "Characters" / f"{slug}_log.yaml"
        if log_path.is_file():
            data = logs_io.ensure_log_shape(logs_io.load_log(log_path))
        else:
            card = cards.get(slug_l)
            if not card:
                raise CommitError(f"No card or log for slug {slug}")
            data = logs_io.default_log_from_card_meta(card.meta, as_of="build")

        # revision check (optimistic concurrency)
        expected = None
        for k, v in req.expected_revisions.items():
            if k.lower() == slug_l:
                expected = int(v)
                break
        if expected is not None and int(data.get("revision") or 1) != expected:
            raise CommitError(
                f"Revision mismatch for {slug}: log has {data.get('revision')}, "
                f"expected {expected}"
            )

        decay_notes = logs_io.decay_temporary_effects(data)

        if not cc.skip_matrix:
            data = logs_io.apply_pressure(
                data,
                movement_id=mov_label,
                pressure=cc.pressure,
                strength=cc.strength,
                notes=cc.notes or ("; ".join(decay_notes) if decay_notes else ""),
                delta_override=cc.delta,
                permanence=cc.permanence,
                somatic_override=cc.somatic,
                bias_delta=cc.bias_delta,
            )
        else:
            # still advance as_of for presence
            snap = data.setdefault("snapshot", {})
            snap["as_of"] = mov_label

        data["revision"] = int(data.get("revision") or 1) + 1
        data["updated_at"] = _utc_now()
        data["last_commit_id"] = commit_id
        logs_io.save_log(log_path, data)
        results["logs"][slug] = {
            "path": rel(log_path),
            "revision": data["revision"],
            "bias_strength": (data.get("snapshot") or {}).get("bias_strength"),
            "as_of": (data.get("snapshot") or {}).get("as_of"),
        }

    # Ledger row
    ledger_io.append_ledger_row(
        act=req.act,
        ch_mov=ch_mov,
        draft_file=draft_rel,
        day_time=req.day_time,
        somatic=req.somatic,
        beats=req.beats,
    )

    logs_io.regenerate_character_change_log()
    results["ledger"] = rel(ROOT / "Framework" / "Continuity_Ledger.md")
    results["change_log"] = rel(ROOT / "Framework" / "Character_Change_Log.md")
    return results
