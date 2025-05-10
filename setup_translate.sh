#!/usr/bin/env bash
read -p "Enter app name (without .app): " APPNAME

SOURCE_DIR="/Applications"
TRANSLATE_DIR="$HOME/Downloads/translating"
ALTER_SOURCE_DIR="$HOME/Applications"

if [ ! -d "${SOURCE_DIR}/${APPNAME}.app" ]; then
    if [ -d "${ALTER_SOURCE_DIR}/${APPNAME}.app" ]; then
        SOURCE_DIR="${ALTER_SOURCE_DIR}"
    else
        echo "Error: ${SOURCE_DIR}/${APPNAME}.app not found."
        echo "Error: ${ALTER_SOURCE_DIR}/${APPNAME}.app not found."
        exit 1
    fi
fi

mkdir -p "${TRANSLATE_DIR}"
cp -R "${SOURCE_DIR}/${APPNAME}.app" "${TRANSLATE_DIR}/"

LPROJ_DIR="${TRANSLATE_DIR}/zh-Hant.lproj"
mkdir -p "${LPROJ_DIR}"
touch "${LPROJ_DIR}/Localizable.strings"

STRING_DIR="${TRANSLATE_DIR}/rawStrings"
mkdir -p "${STRING_DIR}"
strings "${TRANSLATE_DIR}/${APPNAME}.app/Contents/MacOS/${APPNAME}" > ${STRING_DIR}/all_strings.txt
grep -E '^[A-Za-z0-9[:punct:] ]{2,}$' ${STRING_DIR}/all_strings.txt \
  | grep ' ' > ${STRING_DIR}/ui_strings.txt

echo "✅ Setup complete!"
echo "  • Copied to: ${TRANSLATE_DIR}/${APPNAME}.app"
echo "  • Created:   ${LPROJ_DIR}/Localizable.strings"