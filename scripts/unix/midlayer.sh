#!/usr/bin/env bash
# Midlayer runtime (Unix) — integrity, packs, commits
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
exec python3 -m Framework.midlayer "$@"
