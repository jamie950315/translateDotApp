#!/usr/bin/env bash

APP_NAME=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="/Applications"
ALTER_SOURCE_DIR="$HOME/Applications"
OUTPUT_DIR="${SCRIPT_DIR}/Output"

if [ ! -d "${SOURCE_DIR}/${APP_NAME}.app" ]; then
    if [ -d "${ALTER_SOURCE_DIR}/${APP_NAME}.app" ]; then
        SOURCE_DIR="${ALTER_SOURCE_DIR}"
    else
        echo "[setup] Error: ${SOURCE_DIR}/${APP_NAME}.app not found."
        echo "[setup] Error: ${ALTER_SOURCE_DIR}/${APP_NAME}.app not found."
        exit 1
    fi
fi

APP_DIR="${OUTPUT_DIR}/${APP_NAME}"
mkdir -p "${APP_DIR}"

cp -R "${SOURCE_DIR}/${APP_NAME}.app" "${APP_DIR}/"

LPROJ_DIR="${APP_DIR}/zh-Hant.lproj"
mkdir -p "${LPROJ_DIR}"
touch "${LPROJ_DIR}/Localizable.strings"

STRING_DIR="${APP_DIR}/rawStrings"
mkdir -p "${STRING_DIR}"
strings "${APP_DIR}/${APP_NAME}.app/Contents/MacOS/${APP_NAME}" > ${STRING_DIR}/all_strings.txt
grep -E '^[A-Za-z0-9[:punct:] ]{2,}$' ${STRING_DIR}/all_strings.txt \
  | grep ' ' > ${STRING_DIR}/ui_strings.txt

echo "[setup] ✅ Setup complete!"
echo "[setup] • Copied to: ${APP_DIR}/${APP_NAME}.app"
echo "[setup] • Created:   ${STRING_DIR}/ui_strings.txt"
echo "[setup] • Created:   ${LPROJ_DIR}/Localizable.strings"