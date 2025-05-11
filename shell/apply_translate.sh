#!/usr/bin/env bash
TRANSLATE_DIR="$HOME/Downloads/translating"
APP_APP=$(find "$TRANSLATE_DIR" -maxdepth 1 -type d -name "*.app" | head -n 1)
if [ -z "$APP_APP" ]; then
  echo "Error: no .app found in $TRANSLATE_DIR"
  exit 1
fi

LPROJ_SRC="$TRANSLATE_DIR/zh-Hant.lproj"
TARGET_RESOURCES="$APP_APP/Contents/Resources"

if [ ! -d "${LPROJ_SRC}" ]; then
  echo "Error: ${LPROJ_SRC} not found."
  exit 1
fi

if [ ! -d "${TARGET_RESOURCES}" ]; then
  echo "Error: ${TARGET_RESOURCES} not found."
  exit 1
fi

cp -R "${LPROJ_SRC}" "${TARGET_RESOURCES}/"

codesign --force --deep --sign - "$APP_APP"

echo "✅ Applied translation!"
echo "  • Copied zh-Hant.lproj → ${TARGET_RESOURCES}"