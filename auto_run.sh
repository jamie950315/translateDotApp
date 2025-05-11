#!/usr/bin/env bash
set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set +e
echo "[auto_run] Checking Python dependencies..."

if [ -f "${script_dir}/venv/bin/activate" ]; then
    source "${script_dir}/venv/bin/activate"
fi


python3 - << 'PY'
import sys
try:
    import openai  # replace/add more packages if needed
    sys.exit(0)
except ImportError:
    sys.exit(1)
PY
status=$?
set -e

if [ "$status" -ne 0 ]; then
    echo "[auto_run] Missing dependencies detected. Setting up virtual environment..."
    python3 -m venv "${script_dir}/venv"
    source "${script_dir}/venv/bin/activate"
    echo "[auto_run] Installing Python libraries..."
    pip install --upgrade pip
    pip install openai
else
    echo "[auto_run] Dependencies are satisfied."
fi


bash "${script_dir}/setup_translate.sh"

python3 "${script_dir}/OAITranslateAsync.py"

bash "${script_dir}/apply_translate.sh"