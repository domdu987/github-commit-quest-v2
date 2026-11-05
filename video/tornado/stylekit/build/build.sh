#!/bin/bash
# Build the นาคเล่นน้ำ project (style frames / episodes): build.sh <part dir, e.g. sf> <hf dir> <project> [landscape]
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; T="$B/.."; E="$1"; H="$(cd "$2" && pwd)"; P="$3"; S=/tmp/claude-0/-home-user-github-commit-quest-v2/4f94749f-8122-57a4-aa41-e38e84dcb96c/scratchpad
cp $S/tkw/video/takhian/src/takhian.js $S/tkw/video/takhian/src/stormfx.js $S/rw/rup/lib/rupnak.js $S/rw/rup/lib/rupnak2.js $S/rw/rup/lib/rupstill.js $S/rw/rup/lib/rupx.js "$T/src/ngw.js" "$H/lib/"
W="$(mktemp -d)"; cat "$B/head.part" "$B/sigcard.part" "$B/helpers.part" "$B/sinkkit.part" "$T/src/handkit.part" "$T/$E/common.part" "$T/$E/body.part" "$B/foot.part" > "$W/ep.tmpl.html"
[ -n "${BADGE:-}" ] && sed -i "s/ทอร์นาโด · EP.1/${BADGE}/" "$W/ep.tmpl.html"   # the corner badge (full story: BADGE="เสียงรถไฟ")
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="$T/$E/schedule.json" TK_TMPL="$W/ep.tmpl.html" python3 "$B/make.py"
rm -rf "$W"
if [ "${4:-}" = "landscape" ]; then
  cp /home/user/github-commit-quest-v2/video/longform/landscape.js "$H/$P/assets/"
  python3 - "$H/$P/index.html" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('content="width=1080, height=1920"','content="width=1920, height=1080"'),('width: 1080px; height: 1920px;','width: 1920px; height: 1080px;'),('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"'),('<script src="assets/engine.js"></script>','<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')]:
    s=s.replace(a,b)
# 16:9 paint fix: with every shot laid out (only visibility:hidden) Chrome runs out of raster memory on the widened, scaled stages
# and paints black tiles, so a hidden clip leaves the layout. Done in CSS off the runtime's own inline visibility (a script hooked
# on the timeline's render ran in snapshots but not inside the HyperFrames render: every clip after the first stayed black).
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip > .capwrap { top: 955px !important; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
fi
