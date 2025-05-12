#!/usr/bin/env bash

read -p "Enter app name (without .app): " APP_NAME

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
echo "[auto_run] Checking Python dependencies..."

if [ -f "${SCRIPT_DIR}/venv/bin/activate" ]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
fi


python3 - << 'PY'
import sys
try:
    import openai
    sys.exit(0)
except ImportError:
    sys.exit(1)
PY
status=$?
set -e

if [ "$status" -ne 0 ]; then
    echo "[auto_run] Missing dependencies detected. Setting up virtual environment..."
    python3 -m venv "${SCRIPT_DIR}/venv"
    source "${SCRIPT_DIR}/venv/bin/activate"
    echo "[auto_run] Installing Python libraries..."
    pip install --upgrade pip
    pip install openai
else
    echo "[auto_run] Dependencies are satisfied."
fi

bash "${SCRIPT_DIR}/shell/setup_translate.sh" "$APP_NAME"

python3 "${SCRIPT_DIR}/python/OAITranslateAsync.py" "$APP_NAME"

bash "${SCRIPT_DIR}/shell/apply_translate.sh" "$APP_NAME"

echo "[auto_run] Complete. ${APP_NAME} have been translated."