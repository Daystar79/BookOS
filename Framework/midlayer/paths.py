"""Repository path helpers."""

from __future__ import annotations

from pathlib import Path

# Framework/midlayer/paths.py → repo root is parents[2]
ROOT = Path(__file__).resolve().parents[2]
FRAMEWORK = ROOT / "Framework"
CHARACTERS = ROOT / "Characters"
DRAFTS = ROOT / "Drafts"
BUILD_CONTEXT = ROOT / "Build" / ".context"

CONTINUITY_LEDGER = FRAMEWORK / "Continuity_Ledger.md"
CHARACTER_CHANGE_LOG = FRAMEWORK / "Character_Change_Log.md"
RULES_INDEX = FRAMEWORK / "Rules_Index.md"
MAIN_MD = FRAMEWORK / "Main.md"
REALM_DATA = FRAMEWORK / "Psychology" / "realm_data.yaml"
KERNEL = Path(__file__).resolve().parent / "kernel.md"
LOG_TEMPLATE = CHARACTERS / "_log_template.yaml"

SKIP_CARD_NAMES = {
    "_template.md",
    "README.md",
    "Relations.md",
}
SKIP_LOG_NAMES = {
    "_log_template.yaml",
    "README.md",
}


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)
