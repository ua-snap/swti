#!/usr/bin/env bash
# Builds the stand-alone macOS app (and a .dmg) into dist/.
#
#   desktop/build_macos.sh            # build the .app and .dmg
#   PYTHON=python3.12 desktop/build_macos.sh
#
# The app is built for the architecture of the Python used (arm64 on Apple
# silicon, x86_64 on Intel).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv-desktop"
PYTHON="${PYTHON:-python3.13}"
APP_NAME="Alaska Statewide Temperature Index"

cd "$ROOT"

if [[ ! -x "$VENV/bin/python" ]]; then
    echo "==> Creating build environment in $VENV"
    "$PYTHON" -m venv "$VENV"
fi
echo "==> Installing dependencies"
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r desktop/requirements.txt

if [[ ! -f desktop/swti.icns ]]; then
    "$VENV/bin/python" desktop/make_icon.py
fi

echo "==> Building app"
"$VENV/bin/pyinstaller" --noconfirm --clean \
    --distpath "$ROOT/dist" --workpath "$ROOT/build" \
    desktop/swti.spec

# PyInstaller leaves the intermediate onedir build next to the .app.
rm -rf "$ROOT/dist/swti"

echo "==> Creating disk image"
DMG="$ROOT/dist/$APP_NAME.dmg"
STAGING="$ROOT/build/dmg"
rm -rf "$STAGING" "$DMG"
mkdir -p "$STAGING"
cp -R "$ROOT/dist/$APP_NAME.app" "$STAGING/"
ln -s /Applications "$STAGING/Applications"
hdiutil create -quiet -volname "$APP_NAME" -srcfolder "$STAGING" -ov -format UDZO "$DMG"

echo
echo "Built:"
echo "  $ROOT/dist/$APP_NAME.app"
echo "  $DMG"
