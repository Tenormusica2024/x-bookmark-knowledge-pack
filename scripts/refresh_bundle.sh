#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: ./scripts/refresh_bundle.sh <input.json> <output-dir> [--publish-dir <dir>] [--no-html]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"
python "$SCRIPT_DIR/refresh_bundle.py" "$@"
