#!/bin/bash
# Redraws every diagram (SVG) and exports each one as a 2x PNG with headless Chrome.
# Usage: cd wiring && ./render.sh
set -e
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for py in gen.py lionpins.py jetpins.py how.py heatsinks.py; do python3 "$py"; done
for svg in *.svg; do
  read W H < <(sed -nE 's/.*<svg[^>]* width="([0-9]+)" height="([0-9]+)".*/\1 \2/p' "$svg" | head -1) || true  # some SVGs have no final newline
  "$CHROME" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --window-size="$W,$H" --screenshot="$PWD/${svg%.svg}.png" "file://$PWD/$svg" 2>/dev/null
  echo "$svg -> ${svg%.svg}.png"
done
