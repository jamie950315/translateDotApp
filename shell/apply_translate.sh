#!/usr/bin/env bash

APP_NAME=$1
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/Output"
APP_DIR="${OUTPUT_DIR}/${APP_NAME}"
LPROJ_DIR="${APP_DIR}/zh-Hant.lproj"

APP_RESOURCES="${APP_DIR}/${APP_NAME}.app/Contents/Resources"

if [ ! -d "${LPROJ_DIR}" ]; then
  echo "[apply] Error: ${LPROJ_DIR} not found."
  exit 1
fi

if [ ! -d "${APP_RESOURCES}" ]; then
  echo "[apply] Error: ${APP_RESOURCES} not found."
  exit 1
fi

cp -R "${LPROJ_DIR}" "${APP_RESOURCES}/"

codesign --force --deep --sign - "${APP_DIR}/${APP_NAME}.app"

echo "[apply] ✅ Applied translation!"
echo "[apply] • Copied zh-Hant.lproj → ${APP_RESOURCES}"