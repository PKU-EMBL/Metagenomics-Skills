#!/usr/bin/env bash
# Backward-compatible wrapper for the cross-platform Python installer.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: Python 3 is required; run scripts/install-skills.py with Python 3.10+" >&2
  exit 127
fi

exec python3 "$ROOT/scripts/install-skills.py" "$@"
