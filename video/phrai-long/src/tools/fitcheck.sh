#!/bin/bash
# 16:9 band check for every shot of a built part: the whole vertical frame with the band outlined in red (tools/snapFit.cjs),
# at 30% and 75% of each shot, tiled into labelled contact sheets.   tools/fitcheck.sh <1|2|3> <build dir> <out dir> <port>
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; E="$1"; B="$2"; O="$3"; P="$4"
mkdir -p "$O"; rm -f "$O"/t*.png
(cd "$B" && setsid nohup python3 -m http.server "$P" >/dev/null 2>&1 &) ; sleep 1
TS=$(python3 - "$W/ep$E/schedule.json" <<'PY'
import json, sys
s = json.load(open(sys.argv[1]))
print(" ".join(f"{sh['start'] + sh['dur'] * f:.2f}" for sh in s["shots"] for f in (0.3, 0.75)))
PY
)
node "$W/tools/snapFit.cjs" "$P" "$O" $TS > "$O/info.txt" 2>&1 || true
pkill -f "http.server $P" || true
python3 - "$W/ep$E/schedule.json" "$O" "$E" <<'PY'
import json, sys, glob, os
from PIL import Image, ImageDraw, ImageFont
s = json.load(open(sys.argv[1])); O = sys.argv[2]; E = sys.argv[3]
info = {}
for ln in open(os.path.join(O, "info.txt")):
    p = ln.split()
    if len(p) >= 2 and p[0].replace(".", "").isdigit(): info[float(p[0])] = " ".join(p[1:])
fs = sorted(glob.glob(os.path.join(O, "t*.png")), key=lambda f: float(os.path.basename(f)[1:-4]))
W_, H_ = 640, 360; cols = 4
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
for k in range(0, len(fs), 16):
    chunk = fs[k:k + 16]; rows = (len(chunk) + cols - 1) // cols
    cs = Image.new("RGB", (W_ * cols, H_ * rows), (0, 0, 0))
    for i, f in enumerate(chunk):
        t = float(os.path.basename(f)[1:-4]); key = next((sh["key"] for sh in s["shots"] if sh["start"] <= t < sh["start"] + sh["dur"]), "?")
        im = Image.open(f).convert("RGB").resize((W_, H_)); d = ImageDraw.Draw(im)
        lab = f"ep{E} {t:.2f} {key} {info.get(round(t, 2), '')}"; d.rectangle((0, 0, 10 * len(lab) + 8, 24), fill=(0, 0, 0)); d.text((4, 2), lab, fill=(255, 255, 0), font=font)
        cs.paste(im, ((i % cols) * W_, (i // cols) * H_))
    cs.save(os.path.join(O, f"fit_{k // 16:02d}.jpg"), quality=80)
print(len(fs), "frames")
PY
