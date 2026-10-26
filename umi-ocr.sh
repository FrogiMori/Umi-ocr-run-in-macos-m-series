#!/bin/bash
# Umi-OCR macOS Native Launcher
set -e

cd "$(dirname "$0")"
PROJECT_DIR="$(pwd)"

if [ -f "$PROJECT_DIR/.venv/bin/python3" ]; then
    PYTHON_EXE="$PROJECT_DIR/.venv/bin/python3"
elif command -v python3 &>/dev/null; then
    PYTHON_EXE="$(command -v python3)"
else
    echo "Error: Python 3 not found." >&2
    exit 1
fi

export PYTHONPATH="$PROJECT_DIR/UmiOCR-data:$PYTHONPATH"
exec "$PYTHON_EXE" "$PROJECT_DIR/UmiOCR-data/main.py" "$@"
