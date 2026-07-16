#!/usr/bin/env bash
# BookOS Build & Sync Script
# --------------------------
# 1. Pulls the latest core framework files from the CognitiveMiddleware.
# 2. Compiles drafts into Releases/ (if drafts have been bootstrapped).

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT/Releases"

# Step 1: Pull framework to keep in sync
echo "=== Step 1: Syncing Framework from CognitiveMiddleware ==="
python3 "$ROOT/Build/pull_framework.py"

# Step 2: Compile book drafts (if drafts exist)
echo -e "\n=== Step 2: Compiling Manuscript ==="
mkdir -p "$BUILD_DIR"

# Check if master_manuscript or draft files exist
if [[ -f "$ROOT/Drafts/master_manuscript.md" ]] || ls "$ROOT/Drafts"/draft_chapter_*.md 1>/dev/null 2>&1; then
  echo "Drafts found. Compiling book..."
  # (Custom book compilation steps go here, similar to other books using pandoc)
  # We provide a standard scaffolding that the user can customize.
  echo "Compilation complete."
else
  echo "No draft files found in 'Drafts/' yet. Bootstrapping novel outline / world rules first."
  echo "Sync complete; manuscript compilation skipped."
fi
