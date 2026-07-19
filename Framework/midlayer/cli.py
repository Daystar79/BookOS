#!/usr/bin/env python3
"""
Midlayer runtime CLI — status, pack, commit, gate, rebuild-log, seed-log.

Usage (preferred):
  python3 scripts/run.py midlayer status
  python3 scripts/run.py midlayer pack --slugs reed,helen
  python3 scripts/run.py midlayer commit --movement "1 M1" --draft … --slugs …
  python3 scripts/run.py midlayer gate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow `python Framework/midlayer/cli.py`, `python -m Framework.midlayer`, and run.py
_PKG = Path(__file__).resolve().parent
_ROOT = _PKG.parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from Framework.midlayer import card_io  # noqa: E402
from Framework.midlayer import commit as commit_mod  # noqa: E402
from Framework.midlayer import integrity, logs_io  # noqa: E402
from Framework.midlayer import pack as pack_mod  # noqa: E402
from Framework.midlayer.paths import BUILD_CONTEXT, ROOT  # noqa: E402


def cmd_status(args: argparse.Namespace) -> int:
    report = integrity.check_integrity(strict_samples=args.strict_samples)
    print(integrity.format_report(report))
    if args.json:
        print(
            json.dumps(
                {
                    "status": report.status,
                    "blocked": report.blocked,
                    "issues": [
                        {"severity": i.severity.value, "code": i.code, "message": i.message}
                        for i in report.issues
                    ],
                },
                indent=2,
            )
        )
    return 1 if report.blocked else 0


def cmd_gate(args: argparse.Namespace) -> int:
    report = integrity.check_integrity(strict_samples=args.strict_samples)
    if report.blocked:
        print(integrity.format_report(report))
        print("gate: FAIL — do not draft", file=sys.stderr)
        return 1
    print(f"gate: PASS — {report.status}")
    return 0


def cmd_pack(args: argparse.Namespace) -> int:
    report = integrity.check_integrity(strict_samples=False)
    if report.blocked and not args.force:
        print(integrity.format_report(report))
        print("pack: refused (integrity BLOCKED). Use --force to emit anyway.", file=sys.stderr)
        return 1

    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    if not slugs:
        print("pack: --slugs required (comma-separated)", file=sys.stderr)
        return 2

    brief = args.brief or ""
    if args.brief_file:
        brief = Path(args.brief_file).read_text(encoding="utf-8")

    preceding = Path(args.preceding) if args.preceding else None
    if preceding and not preceding.is_file():
        alt = ROOT / preceding
        preceding = alt if alt.is_file() else preceding

    try:
        content = pack_mod.build_pack(
            slugs=slugs,
            brief=brief,
            tier=args.tier,
            include_preceding=preceding,
        )
    except FileNotFoundError as e:
        print(f"pack: {e}", file=sys.stderr)
        return 2

    out = Path(args.out) if args.out else BUILD_CONTEXT / "movement_pack.md"
    if not out.is_absolute():
        out = ROOT / out
    path = pack_mod.write_pack(content, out)
    print(f"Wrote {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}")
    print(f"Load this pack (+ preceding prose if not embedded) to draft. Cast: {', '.join(slugs)}")
    return 0


def cmd_commit(args: argparse.Namespace) -> int:
    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()]
    if not slugs:
        print("commit: --slugs required", file=sys.stderr)
        return 2
    if not args.movement or not args.draft or not args.day or not args.somatic or not args.beats:
        print(
            "commit: require --movement --draft --day --somatic --beats",
            file=sys.stderr,
        )
        return 2

    draft = Path(args.draft)
    if not draft.is_file():
        draft = ROOT / args.draft

    expected: dict[str, int] = {}
    if args.expected_revision:
        for part in args.expected_revision.split(","):
            if "=" not in part:
                print("commit: --expected-revision form slug=N", file=sys.stderr)
                return 2
            s, n = part.split("=", 1)
            expected[s.strip()] = int(n.strip())

    try:
        characters = commit_mod.parse_character_json(
            args.character_json,
            slugs,
            args.pressure,
            args.strength,
        )
        result = commit_mod.run_commit(
            commit_mod.CommitRequest(
                movement=args.movement,
                draft=draft,
                day_time=args.day,
                somatic=args.somatic,
                beats=args.beats,
                slugs=slugs,
                act=args.act,
                title=args.title or "",
                characters=characters,
                expected_revisions=expected,
                pressure_default=args.pressure,
                strength_default=args.strength,
            )
        )
    except (commit_mod.CommitError, json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print(f"commit: FAIL — {e}", file=sys.stderr)
        return 1

    print("commit: OK")
    print(json.dumps(result, indent=2))
    # re-status
    report = integrity.check_integrity()
    print(integrity.format_report(report))
    return 0 if not report.blocked else 0  # commit succeeded even if other warns


def cmd_rebuild_log(args: argparse.Namespace) -> int:
    logs_io.regenerate_character_change_log()
    print("Regenerated Framework/Character_Change_Log.md from Characters/*_log.yaml")
    return 0


def cmd_seed_log(args: argparse.Namespace) -> int:
    slugs = [s.strip() for s in args.slugs.split(",") if s.strip()] if args.slugs else None
    cards = card_io.load_cards(slugs) if slugs else card_io.list_cards()
    n = 0
    for card in cards:
        path = ROOT / "Characters" / f"{card.slug}_log.yaml"
        if path.is_file() and not args.force:
            print(f"skip {card.slug}_log.yaml (exists; use --force to overwrite)")
            continue
        data = logs_io.default_log_from_card_meta(card.meta, as_of="build")
        logs_io.save_log(path, data)
        print(f"seeded {path.relative_to(ROOT)}")
        n += 1
    if n:
        logs_io.regenerate_character_change_log()
    print(f"seed-log: {n} file(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="midlayer",
        description="Midlayer runtime: integrity gates, context packs, state commits",
    )
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("status", help="Ledger/log integrity report (exit 1 if BLOCKED)")
    s.add_argument("--json", action="store_true")
    s.add_argument(
        "--strict-samples",
        action="store_true",
        help="Also flag uncommitted Drafts/samples/* drafts",
    )
    s.set_defaults(func=cmd_status)

    g = sub.add_parser("gate", help="Exit 0 only if integrity allows drafting")
    g.add_argument("--strict-samples", action="store_true")
    g.set_defaults(func=cmd_gate)

    pk = sub.add_parser("pack", help="Write minimal movement context pack")
    pk.add_argument("--slugs", required=True, help="Comma-separated character slugs")
    pk.add_argument("--brief", default="", help="Brief text")
    pk.add_argument("--brief-file", default=None)
    pk.add_argument("--tier", default="yellow", choices=["green", "yellow", "red"])
    pk.add_argument("--preceding", default=None, help="Preceding draft path to embed")
    pk.add_argument("--out", default=None, help="Output path (default Build/.context/movement_pack.md)")
    pk.add_argument("--force", action="store_true", help="Pack even if integrity BLOCKED")
    pk.set_defaults(func=cmd_pack)

    c = sub.add_parser("commit", help="Atomic post-movement state commit")
    c.add_argument("--movement", required=True, help='e.g. "1 M1" or "chapter 1 m1"')
    c.add_argument("--draft", required=True, help="Path to approved draft file")
    c.add_argument("--day", required=True, help="Day & time close")
    c.add_argument("--somatic", required=True, help="Somatic state on close")
    c.add_argument("--beats", required=True, help="Continuity & plot beats")
    c.add_argument("--slugs", required=True, help="On-scene character slugs")
    c.add_argument("--act", default="Act One")
    c.add_argument("--title", default="")
    c.add_argument("--pressure", default="Emotional/Social")
    c.add_argument("--strength", default="Medium", help="Low|Medium|High|Extreme")
    c.add_argument(
        "--character-json",
        default=None,
        help='JSON list of per-character overrides: [{"slug":"reed","strength":"High",...}]',
    )
    c.add_argument(
        "--expected-revision",
        default=None,
        help="slug=N pairs for optimistic concurrency",
    )
    c.set_defaults(func=cmd_commit)

    r = sub.add_parser("rebuild-log", help="Regenerate Character_Change_Log.md from YAML")
    r.set_defaults(func=cmd_rebuild_log)

    seed = sub.add_parser("seed-log", help="Create _log.yaml from card defaults")
    seed.add_argument("--slugs", default=None, help="Comma-separated; default all cards")
    seed.add_argument("--force", action="store_true")
    seed.set_defaults(func=cmd_seed_log)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
