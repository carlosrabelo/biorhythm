#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

rm -rf "$ROOT_DIR/dist/" "$ROOT_DIR/build/" "$ROOT_DIR"/*.egg-info
find "$ROOT_DIR" -type d -name __pycache__ -exec rm -rf {} +
find "$ROOT_DIR" -type f -name "*.pyc" -delete
echo "Cleaned build artifacts and caches."
