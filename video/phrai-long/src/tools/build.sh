#!/bin/bash
# Build one long-version part: tools/build.sh <1|2|3> [out dir] → the vertical project from the episode's own make.py, then 16:9 (land.py)
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; E="$1"; OUT="${2:-$W/build/ep$E}"
cd "$W/ep$E"
PARTS="helpers.part"; [ -f common.part ] && PARTS="$PARTS common.part"; PARTS="$PARTS body.part"; [ -f land.part ] && PARTS="$PARTS land.part"
cat $PARTS > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html
rm -rf "$OUT" && PROJ="$OUT" python3 make.py
python3 "$W/tools/land.py" "$OUT" มือพราย
