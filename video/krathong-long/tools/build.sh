#!/usr/bin/env bash
# krathong long (16:9): build one section's HyperFrames project from its workspace (vertical shot code + long.part 16:9 cameras).
# usage: build.sh <workspace dir, e.g. kp/L1>   (make.py there names the project dir)
set -euo pipefail
W="$(cd "$1" && pwd)"; H="$(cd "$(dirname "$0")" && pwd)"
cd "$W"
LP=""; [ -f long.part ] && LP=long.part; [ -f longcam.part ] && LP="$LP longcam.part"
cat helpers.part kit.part common.part $LP body.part > shots.part
cat head.part sigcard.part shots.part foot.part > ep.tmpl.html
OUT=$(python3 make.py); echo "$OUT"
P=$(echo "$OUT" | sed -n 's/^built \(.*\) total.*/\1/p')
cp "$H/landscape.js" "$P/assets/"
# cine.js draws its grade filter region, the flash and the grade-glow rect for the 1080-wide frame: widen them to the 16:9 stage
# (x -660 … 1740), or everything outside the old frame is cut away by the filter region
python3 - "$P/assets/cine.js" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
R=[('filterUnits="userSpaceOnUse" x="0" y="0" width="${W}" height="${H}"','filterUnits="userSpaceOnUse" x="-660" y="0" width="2400" height="${H}"'),
   ('<rect id="${id}-cineflash" width="${W}" height="${H}"','<rect id="${id}-cineflash" x="-660" width="2400" height="${H}"'),
   ('const html = `<rect id="${gid}" width="${W}" height="${H}"','const html = `<rect id="${gid}" x="-660" width="2400" height="${H}"')]
for a,b in R:
    assert s.count(a)==1, a; s=s.replace(a,b)
open(p,'w').write(s)
PY
python3 - "$P/index.html" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('content="width=1080, height=1920"','content="width=1920, height=1080"'),('width: 1080px; height: 1920px;','width: 1920px; height: 1080px;'),('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"'),('<script src="assets/engine.js"></script>','<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')]:
    assert a in s, a; s=s.replace(a,b)
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
