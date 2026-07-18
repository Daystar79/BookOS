#!/usr/bin/env python3
import unittest
import sys
import os
import tempfile

# Add Framework directory to path to import linter
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../Framework'))
import linter

class TestLinter(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.test_dir.cleanup()

    def create_file(self, filename, content):
        path = os.path.join(self.test_dir.name, filename)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_clean_prose(self):
        content = """---
title: Sample Draft
---
He walked down the street. It was a cold evening, and he adjusted his collar.
"""
        path = self.create_file("clean.md", content)
        findings = linter.audit_file(path)
        self.assertEqual(len(findings), 0)

    def test_system_leak_realm(self):
        content = "He felt a strange presence from Realm II."
        path = self.create_file("leak.md", content)
        findings = linter.audit_file(path)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['type'], "System Leak")
        self.assertEqual(findings[0]['category'], "Framework Jargon")

    def test_system_leak_bias(self):
        content = "She was acting out of Saviour Complex."
        path = self.create_file("leak_bias.md", content)
        findings = linter.audit_file(path)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['type'], "System Leak")
        self.assertEqual(findings[0]['category'], "Engine Bias Names")

    def test_watchlist_only_wound_trigger_mirror(self):
        content = """---
title: Contextual Test
---
A shallow wound on his arm.
He pulled the trigger of the gun.
The mirror on the wall was dusty.
"""
        path = self.create_file("watchlist.md", content)
        findings = linter.audit_file(path)
        
        # They should be Banned/Filler Phrase (watchlist warning), not System Leak (critical)
        self.assertEqual(len(findings), 3)
        for f in findings:
            self.assertEqual(f['type'], "Banned/Filler Phrase")
            self.assertEqual(f['category'], "Contextual Watchlist (Warning Only)")

    def test_critical_wound_trigger_mirror(self):
        content = """---
title: Critical Test
---
His active wound was throbbing.
It was an emotional trigger.
She looked into the Mirror bias.
"""
        path = self.create_file("critical_watchlist.md", content)
        findings = linter.audit_file(path)
        self.assertEqual(len(findings), 3)
        # All three should be critical system leaks
        for f in findings:
            self.assertEqual(f['type'], "System Leak")

    def test_yaml_frontmatter_boundaries(self):
        content = """---
title: Open YAML
No closing fence
"""
        path = self.create_file("malformed.md", content)
        findings = linter.audit_file(path)
        self.assertTrue(any(f['category'] == "YAML Frontmatter" for f in findings))

    def test_horizontal_rules_continuous_action(self):
        content = """---
title: HR test
---
First action beat.
---
Second action beat.
---
Third action beat.
---
Fourth action beat.
"""
        path = self.create_file("excess_hr.md", content)
        findings = linter.audit_file(path)
        self.assertTrue(any(f['category'] == "Continuous Action Break" for f in findings))

if __name__ == '__main__':
    unittest.main()
