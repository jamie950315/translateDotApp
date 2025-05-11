#!/usr/bin/env bash
set -e

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "${script_dir}/setup_translate.sh"

python3 "${script_dir}/OAITranslateAsync.py"

bash "${script_dir}/apply_translate.sh"