#!/usr/bin/env bash
# Unix launcher — prose linter for drafts.
# AI agents on Linux/macOS/BSD: run this (or: python3 scripts/run.py lint …).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <file_or_directory> [extra linter args...]" >&2
  echo "Example: $0 Drafts/" >&2
  exit 2
fi

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Error: Python 3 not found on PATH." >&2
  exit 127
fi

exec "$PY" "$ROOT/Framework/linter.py" "$@"
