#!/usr/bin/env bash
# Unix launcher — one-time optimized-file migration (if *_optimized sources exist).
# AI agents on Linux/macOS/BSD: run this (or: python3 scripts/run.py migrate).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Error: Python 3 not found on PATH." >&2
  exit 127
fi

exec "$PY" "$ROOT/migrate_optimized.py" "$@"
