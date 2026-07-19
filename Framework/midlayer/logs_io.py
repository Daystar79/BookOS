"""Character runtime log IO + consolidated Character_Change_Log regeneration."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import yaml_util
from .paths import (
    CHARACTER_CHANGE_LOG,
    CHARACTERS,
    LOG_TEMPLATE,
    SKIP_LOG_NAMES,
    rel,
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def list_log_paths() -> list[Path]:
    if not CHARACTERS.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(CHARACTERS.glob("*_log.yaml")):
        if path.name in SKIP_LOG_NAMES:
            continue
        out.append(path)
    return out


def slug_from_log_path(path: Path) -> str:
    name = path.name
    if name.endswith("_log.yaml"):
        return name[: -len("_log.yaml")]
    return path.stem


def load_log(path: Path) -> dict[str, Any]:
    data = yaml_util.load_file(path)
    if not isinstance(data, dict):
        return {}
    return data


def default_log_from_card_meta(card_meta: dict[str, Any], *, as_of: str = "build") -> dict[str, Any]:
    """Seed a runtime log dict from card build defaults."""
    tw = card_meta.get("transformation_weights") or {}
    latents = tw.get("latent_anchors") or {}
    latent_weights: dict[str, Any] = {}
    if isinstance(latents, dict):
        for k, v in latents.items():
            key = str(k).replace("Realm_", "").replace("realm_", "")
            latent_weights[key] = v
    return {
        "schema_version": 1,
        "revision": 1,
        "updated_at": _utc_now(),
        "last_commit_id": None,
        "snapshot": {
            "active_focus": card_meta.get("active_focus") or "",
            "latent_weights": latent_weights,
            "bias_strength": tw.get("bias_strength", 60),
            "default_somatic": card_meta.get("default_somatic_alignment") or "",
            "flexibility": tw.get("somatic_flexibility", 40),
            "as_of": as_of,
        },
        "skills": {"active": [], "latent": []},
        "memories": {"detailed": [], "footnote": []},
        "temporary_effects": [],
        "history": [],
    }


def ensure_log_shape(data: dict[str, Any]) -> dict[str, Any]:
    data.setdefault("schema_version", 1)
    data.setdefault("revision", 1)
    data.setdefault("updated_at", _utc_now())
    data.setdefault("last_commit_id", None)
    data.setdefault("snapshot", {})
    data.setdefault("skills", {"active": [], "latent": []})
    data.setdefault("memories", {"detailed": [], "footnote": []})
    data.setdefault("temporary_effects", [])
    data.setdefault("history", [])
    snap = data["snapshot"]
    if isinstance(snap, dict):
        snap.setdefault("active_focus", "")
        snap.setdefault("latent_weights", {})
        snap.setdefault("bias_strength", 60)
        snap.setdefault("default_somatic", "")
        snap.setdefault("flexibility", 40)
        snap.setdefault("as_of", "build")
    return data


def save_log(path: Path, data: dict[str, Any]) -> None:
    ensure_log_shape(data)
    # Write document-start --- for consistency with templates
    body = yaml_util.dump(data)
    path.write_text("---\n" + body, encoding="utf-8")


def load_all_logs() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in list_log_paths():
        result[slug_from_log_path(path)] = ensure_log_shape(load_log(path))
    return result


def decay_temporary_effects(data: dict[str, Any]) -> list[str]:
    """Decrement remaining_movements; drop expired. Returns notes."""
    notes: list[str] = []
    effects = data.get("temporary_effects") or []
    if not isinstance(effects, list):
        return notes
    kept: list[Any] = []
    for eff in effects:
        if not isinstance(eff, dict):
            continue
        rem = eff.get("remaining_movements")
        if rem is None:
            kept.append(eff)
            continue
        try:
            rem_i = int(rem) - 1
        except (TypeError, ValueError):
            kept.append(eff)
            continue
        if rem_i <= 0:
            notes.append(f"expired effect {eff.get('id', '?')}")
            continue
        eff = dict(eff)
        eff["remaining_movements"] = rem_i
        kept.append(eff)
    data["temporary_effects"] = kept
    return notes


STRENGTH_DELTA = {
    "low": 0,
    "medium": 5,
    "high": 10,
    "extreme": 15,
}


def apply_pressure(
    data: dict[str, Any],
    *,
    movement_id: str,
    pressure: str,
    strength: str,
    notes: str = "",
    delta_override: str | None = None,
    permanence: str | None = None,
    somatic_override: str | None = None,
    bias_delta: int | None = None,
) -> dict[str, Any]:
    """
    Deterministic transformation write-back.
    Low: no history, no bias change (scene-only close lives in ledger).
    Medium+: bias_strength shift + history row + snapshot as_of.
    """
    data = ensure_log_shape(data)
    strength_key = strength.strip().lower()
    auto_delta = STRENGTH_DELTA.get(strength_key, 5)
    if bias_delta is not None:
        auto_delta = bias_delta

    snap = data["snapshot"]
    old_bias = int(snap.get("bias_strength") or 60)
    new_bias = old_bias

    if strength_key != "low" and auto_delta:
        new_bias = max(0, min(100, old_bias + auto_delta))
        snap["bias_strength"] = new_bias

    if somatic_override:
        snap["default_somatic"] = somatic_override

    snap["as_of"] = movement_id

    if strength_key == "low" and not delta_override:
        # Scene-local only; still update as_of for presence tracking optional — keep history clean
        return data

    if permanence is None:
        permanence = {
            "low": "temporary",
            "medium": "medium",
            "high": "permanent",
            "extreme": "permanent",
        }.get(strength_key, "medium")

    if delta_override:
        delta_text = delta_override
    elif new_bias != old_bias:
        delta_text = f"bias_strength {old_bias}→{new_bias}"
    else:
        delta_text = "no weight shift"

    if strength_key != "low" or delta_override:
        history = data.get("history") or []
        if not isinstance(history, list):
            history = []
        history.append(
            {
                "movement": movement_id,
                "pressure": f"{pressure} · {strength.capitalize()}",
                "delta": delta_text,
                "permanence": permanence,
                "notes": notes or "",
            }
        )
        data["history"] = history

    return data


def regenerate_character_change_log(logs: dict[str, dict[str, Any]] | None = None) -> None:
    """Rewrite Framework/Character_Change_Log.md from YAML logs (YAML wins)."""
    if logs is None:
        logs = load_all_logs()
    now = _utc_now()

    lines: list[str] = [
        "---",
        "generated_from: Characters/*_log.yaml",
        f"generated_at: {now}",
        "schema_version: 1",
        "---",
        "",
        "# Character Change Log",
        "*Matrix evolution ledger — consolidated quick reference for the author.*",
        "",
        "**Individual logs** (`Characters/[slug]_log.yaml`) are the canonical mutable runtime state. "
        "**YAML always wins.** This file is regenerated by `midlayer commit` / `midlayer rebuild-log`.",
        "",
        "Do not write movement history onto character cards.",
        "",
        "---",
        "",
        "## Current Matrix Snapshot",
        "",
        "| Character | Active Focus | Latent weights | Bias strength | Default somatic | Flexibility | As of |",
        "| :--- | :--- | :--- | :---: | :--- | :---: | :---: |",
    ]

    if not logs:
        lines.append("")
        lines.append("*(empty — seed from cards when cast exists)*")
    else:
        for slug, data in sorted(logs.items()):
            snap = data.get("snapshot") or {}
            latents = snap.get("latent_weights") or {}
            if isinstance(latents, dict):
                lat_s = ", ".join(f"{k}:{v}" for k, v in latents.items())
            else:
                lat_s = str(latents)
            focus = str(snap.get("active_focus") or "").replace("|", "/")
            somatic = str(snap.get("default_somatic") or "").replace("|", "/")
            lines.append(
                f"| {slug} | {focus} | {lat_s} | {snap.get('bias_strength', '')} | "
                f"{somatic} | {snap.get('flexibility', '')} | {snap.get('as_of', '')} |"
            )

    lines.extend(
        [
            "",
            "---",
            "",
            "## Movement History",
            "",
        ]
    )

    # Group history by movement label
    by_movement: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for slug, data in sorted(logs.items()):
        for entry in data.get("history") or []:
            if not isinstance(entry, dict):
                continue
            mov = str(entry.get("movement") or "unknown")
            by_movement.setdefault(mov, []).append((slug, entry))

    if not by_movement:
        lines.append("*(no approved movements)*")
    else:
        for mov, rows in by_movement.items():
            lines.append(f"### {mov}")
            lines.append("| Character | Pressure | Delta | Permanence | Notes |")
            lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for slug, entry in rows:
                lines.append(
                    f"| {slug} | {entry.get('pressure', '')} | "
                    f"{str(entry.get('delta', '')).replace('|', '/')} | "
                    f"{entry.get('permanence', '')} | "
                    f"{str(entry.get('notes', '')).replace('|', '/')} |"
                )
            lines.append("")

    lines.append("")
    lines.append(f"*Regenerated from {len(logs)} log file(s). Paths relative: `{rel(CHARACTERS)}/*_log.yaml`.*")
    lines.append("")

    CHARACTER_CHANGE_LOG.write_text("\n".join(lines), encoding="utf-8")
