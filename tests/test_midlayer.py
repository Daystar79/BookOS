#!/usr/bin/env python3
"""Tests for Midlayer runtime (integrity, ledger, commit, pack)."""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Framework.midlayer import commit as commit_mod  # noqa: E402
from Framework.midlayer import integrity, ledger_io, logs_io, pack as pack_mod  # noqa: E402


class TestLedgerParse(unittest.TestCase):
    def test_empty_ledger(self):
        text = """# Ledger
## Act One

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |

*(no approved movements)*
"""
        rows = ledger_io.parse_ledger(text)
        self.assertEqual(rows, [])

    def test_parse_row(self):
        text = """## Act One

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |
| 1 M1 | Drafts/x.md | Day 1 evening | Reed: jaw lock | Tea offered |
"""
        rows = ledger_io.parse_ledger(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].chapter, 1)
        self.assertEqual(rows[0].movement, 1)
        self.assertEqual(rows[0].movement_id, "chapter_1_m1")
        self.assertFalse(rows[0].is_placeholder())

    def test_placeholder(self):
        text = """## Act One
| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |
| 1 M1 | Drafts/x.md | [Day & Time] | x | y |
"""
        rows = ledger_io.parse_ledger(text)
        self.assertTrue(rows[0].is_placeholder())


class TestTransform(unittest.TestCase):
    def test_medium_bias_delta(self):
        data = {
            "revision": 1,
            "snapshot": {
                "active_focus": "VIII",
                "latent_weights": {},
                "bias_strength": 70,
                "default_somatic": "jaw",
                "flexibility": 30,
                "as_of": "build",
            },
            "history": [],
            "temporary_effects": [],
        }
        out = logs_io.apply_pressure(
            data,
            movement_id="1 M1",
            pressure="Emotional",
            strength="Medium",
            notes="test",
        )
        self.assertEqual(out["snapshot"]["bias_strength"], 75)
        self.assertEqual(len(out["history"]), 1)

    def test_low_no_history(self):
        data = {
            "snapshot": {"bias_strength": 50, "active_focus": "I", "default_somatic": "x", "flexibility": 40, "latent_weights": {}, "as_of": "build"},
            "history": [],
            "temporary_effects": [],
        }
        out = logs_io.apply_pressure(
            data, movement_id="1 M1", pressure="Social", strength="Low"
        )
        self.assertEqual(out["snapshot"]["bias_strength"], 50)
        self.assertEqual(out["history"], [])

    def test_temp_decay(self):
        data = {
            "temporary_effects": [
                {"id": "a", "field": "x", "delta": 1, "remaining_movements": 1},
                {"id": "b", "field": "y", "delta": 1, "remaining_movements": 3},
            ]
        }
        notes = logs_io.decay_temporary_effects(data)
        self.assertTrue(any("expired" in n for n in notes))
        self.assertEqual(len(data["temporary_effects"]), 1)
        self.assertEqual(data["temporary_effects"][0]["remaining_movements"], 2)


class TestCommitPackIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # minimal book tree
        (self.root / "Characters").mkdir()
        (self.root / "Framework").mkdir()
        (self.root / "Drafts").mkdir()
        (self.root / "Framework" / "Psychology").mkdir()
        (self.root / "Build" / ".context").mkdir(parents=True)

        card = """---
name: "Test"
call_name: "Test"
age: 30
canon_adult: true
physical: "tall"
voice_archetype: "A"
cultural_bias: "none"
active_focus: "Realm VIII — Integration"
latent_anchors: ["Realm I — Origin"]
cognitive_bias: "Debt Ledger — safety rewritten as debt"
default_somatic_alignment: "jaw lock"
transformation_weights:
  active_focus: 65
  latent_anchors:
    Realm_I: 10
  bias_strength: 70
  somatic_flexibility: 30
voice:
  baseline: "short"
  hard_bans: ["therapy"]
---
"""
        (self.root / "Characters" / "test.md").write_text(card, encoding="utf-8")
        log = logs_io.default_log_from_card_meta(
            {
                "active_focus": "Realm VIII — Integration",
                "default_somatic_alignment": "jaw lock",
                "transformation_weights": {
                    "bias_strength": 70,
                    "somatic_flexibility": 30,
                    "latent_anchors": {"Realm_I": 10},
                },
            }
        )
        # patch paths
        self._orig = {}
        import Framework.midlayer.card_io as card_io_mod
        import Framework.midlayer.paths as paths

        self.paths = paths
        self.card_io_mod = card_io_mod
        for attr, val in [
            ("ROOT", self.root),
            ("FRAMEWORK", self.root / "Framework"),
            ("CHARACTERS", self.root / "Characters"),
            ("DRAFTS", self.root / "Drafts"),
            ("BUILD_CONTEXT", self.root / "Build" / ".context"),
            ("CONTINUITY_LEDGER", self.root / "Framework" / "Continuity_Ledger.md"),
            ("CHARACTER_CHANGE_LOG", self.root / "Framework" / "Character_Change_Log.md"),
            ("REALM_DATA", self.root / "Framework" / "Psychology" / "realm_data.yaml"),
            ("KERNEL", ROOT / "Framework" / "midlayer" / "kernel.md"),
            ("LOG_TEMPLATE", self.root / "Characters" / "_log_template.yaml"),
        ]:
            self._orig[attr] = getattr(paths, attr)
            setattr(paths, attr, val)

        # re-bind module-level path copies
        ledger_io.CONTINUITY_LEDGER = paths.CONTINUITY_LEDGER
        ledger_io.ROOT = paths.ROOT
        logs_io.CHARACTER_CHANGE_LOG = paths.CHARACTER_CHANGE_LOG
        logs_io.CHARACTERS = paths.CHARACTERS
        card_io_mod.CHARACTERS = paths.CHARACTERS
        pack_mod.BUILD_CONTEXT = paths.BUILD_CONTEXT
        pack_mod.KERNEL = paths.KERNEL
        pack_mod.REALM_DATA = paths.REALM_DATA
        commit_mod.ROOT = paths.ROOT
        integrity.DRAFTS = paths.DRAFTS
        integrity.ROOT = paths.ROOT

        paths.CONTINUITY_LEDGER.write_text(
            """# Chapter & Movement Continuity Ledger

## Act One

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |

*(no approved movements)*

## Act Two

| Ch / Mov | Draft File | Day & Time | Somatic State on Close | Crucial Continuity & Plot Beats |
| :---: | :--- | :--- | :--- | :--- |

*(no approved movements)*
""",
            encoding="utf-8",
        )
        (self.root / "Framework" / "Psychology" / "realm_data.yaml").write_text(
            "realms:\n  VIII:\n    name: Integration\n    zone: hands\n    micro: [a]\n    moderate: [b]\n    macro: [c]\n    release: [d]\n  I:\n    name: Origin\n    zone: x\n    micro: []\n    moderate: []\n    macro: []\n    release: []\n",
            encoding="utf-8",
        )
        logs_io.save_log(self.root / "Characters" / "test_log.yaml", log)
        draft = self.root / "Drafts" / "draft_chapter_1_m1.md"
        draft.write_text("He set the cup down.\n", encoding="utf-8")
        self.draft = draft

    def tearDown(self):
        import Framework.midlayer.paths as paths

        for attr, val in self._orig.items():
            setattr(paths, attr, val)
        ledger_io.CONTINUITY_LEDGER = paths.CONTINUITY_LEDGER
        ledger_io.ROOT = paths.ROOT
        logs_io.CHARACTER_CHANGE_LOG = paths.CHARACTER_CHANGE_LOG
        logs_io.CHARACTERS = paths.CHARACTERS
        self.card_io_mod.CHARACTERS = paths.CHARACTERS
        pack_mod.BUILD_CONTEXT = paths.BUILD_CONTEXT
        pack_mod.KERNEL = paths.KERNEL
        pack_mod.REALM_DATA = paths.REALM_DATA
        commit_mod.ROOT = paths.ROOT
        integrity.DRAFTS = paths.DRAFTS
        integrity.ROOT = paths.ROOT
        self.tmp.cleanup()

    def test_clean_then_commit(self):
        report = integrity.check_integrity()
        self.assertFalse(report.blocked, integrity.format_report(report))

        result = commit_mod.run_commit(
            commit_mod.CommitRequest(
                movement="1 M1",
                draft=self.draft,
                day_time="Day 1 · evening",
                somatic="Test: jaw lock",
                beats="Cup set down",
                slugs=["test"],
                act="Act One",
                title="Cup",
                pressure_default="Emotional",
                strength_default="Medium",
            )
        )
        self.assertIn("test", result["logs"])
        rows = ledger_io.parse_ledger()
        self.assertEqual(len(rows), 1)
        self.assertTrue(self.draft.is_file())
        log = logs_io.load_log(self.root / "Characters" / "test_log.yaml")
        self.assertEqual(log["snapshot"]["bias_strength"], 75)
        self.assertTrue(self.root.joinpath("Framework/Character_Change_Log.md").is_file())

        # duplicate commit fails
        with self.assertRaises(commit_mod.CommitError):
            commit_mod.run_commit(
                commit_mod.CommitRequest(
                    movement="1 M1",
                    draft=self.draft,
                    day_time="x",
                    somatic="y",
                    beats="z",
                    slugs=["test"],
                )
            )

    def test_pack_contains_kernel_and_cast(self):
        text = pack_mod.build_pack(slugs=["test"], brief="Job: test scene", tier="yellow")
        self.assertIn("Hard bans", text)
        self.assertIn("Debt Ledger", text)
        self.assertIn("test", text.lower())


class TestLinterBrackets(unittest.TestCase):
    def test_bracket_somatic(self):
        sys.path.insert(0, str(ROOT / "Framework"))
        import linter

        path = Path(tempfile.mkdtemp()) / "x.md"
        path.write_text("[throat tight] He nodded.\n", encoding="utf-8")
        findings = linter.audit_file(str(path))
        self.assertTrue(any(f["type"] == "System Leak" for f in findings))
        shutil.rmtree(path.parent)


if __name__ == "__main__":
    unittest.main()
