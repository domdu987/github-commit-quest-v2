#!/bin/sh
# Check what the pipeline needs on this machine. Prints one line per requirement; nothing is installed.
# usage: sh check_env.sh [<project_dir>]   (with the project folder made by bootstrap.py it also checks the fonts there)
ok() { printf "ok       %s\n" "$1"; }
no() { printf "MISSING  %s  -> %s\n" "$1" "$2"; }
PROJ=${1:-$PROJ}
command -v ffmpeg >/dev/null 2>&1 && ok ffmpeg || no ffmpeg "install ffmpeg"
ffmpeg -hide_banner -filters 2>/dev/null | grep -q " ass " && ok "ffmpeg with libass (burns captions)" || no "ffmpeg libass filter" "an ffmpeg build with --enable-libass"
v=$(python3 -c "import bpy; print(bpy.app.version_string)" 2>/dev/null) && ok "Blender as a Python module (bpy $v; tested 5.3.0)" || no "bpy" "pip install bpy  (about 300 MB; Cycles on CPU works headless)"
python3 -c "import numpy, PIL, cv2" >/dev/null 2>&1 && ok "numpy, Pillow, cv2" || no "numpy/Pillow/cv2" "pip install numpy pillow opencv-python-headless"
python3 -c "import fontTools" >/dev/null 2>&1 && ok "fontTools (v3/paper/paper.py measures Thai text)" || no "fontTools" "pip install fonttools"
[ -n "$NODE_PATH" ] || NODE_PATH=$(npm root -g 2>/dev/null); export NODE_PATH
node -e "require('playwright')" >/dev/null 2>&1 && ok "Playwright with Chromium (rasterises SVG); export NODE_PATH=$NODE_PATH before rendering" || no "playwright" "npm i -g playwright && npx playwright install chromium (skip the install where a browser is preinstalled); the rasterisers read NODE_PATH, default /opt/node22/lib/node_modules"
[ -f /usr/share/fonts/opentype/tlwg/Loma-Bold.otf ] && ok "Loma Bold (typed Thai on paper props)" || no "Loma-Bold.otf" "apt-get install fonts-tlwg-loma-otf (package name inferred); paper.py stops on the props that use it"
[ -f /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf ] && ok "DejaVu Sans Bold" || no "DejaVuSans-Bold.ttf" "apt-get install fonts-dejavu-core"
if [ -n "$PROJ" ]; then
  for f in fonts/th/Kanit_800ExtraBold.ttf fonts/th/Kanit_900Black.ttf fonts/Kanit_900Black.ttf fonts/WorkSans-Black.ttf; do
    [ -f "$PROJ/$f" ] && ok "$f" || no "$PROJ/$f" "re-run scripts/bootstrap.py; the skill ships it under pipeline/$f"
  done
else
  echo "info     pass the project folder (sh check_env.sh <project_dir>) to check the fonts under it"
fi
python3 -c "import rapidocr_onnxruntime" >/dev/null 2>&1 && ok "rapidocr (caption OCR of the reference)" || no "rapidocr" "pip install rapidocr-onnxruntime (optional: only for reading burned-in captions)"
code=$(curl -s -o /dev/null -m 15 -w "%{http_code}" -X POST https://fal.run/fal-ai/elevenlabs/sound-effects/v2 -H "Content-Type: application/json" -d '{"text":5}')
[ "$code" = "422" ] && ok "fal.ai reachable and authorised (a 422 validation answer costs nothing)" || no "fal.ai (got HTTP $code)" "ask the user for a fal.ai key for host fal.run (header Authorization, prefix Key) and allow v3.fal.media and v3b.fal.media; see references/environment.md (only needed for voice, effects and stems)"
nproc 2>/dev/null | xargs printf "info     CPU cores: %s (a final 720x1280 frame costs about 18 CPU seconds)\n"
