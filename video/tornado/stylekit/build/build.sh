#!/bin/bash
# Build the style frames: build.sh <hf dir with lib/> <project> [landscape|vertical] [parts dir: tw (big tornado, default) | sf (v1, rejected)]
# lib/ must hold the shared engine libs (rig, sets, engine …); this copies in takhian.js + stormfx.js (takhian kit),
# the rupnak libs (rupnak kit) and ngw.js, assembles the parts and runs make.py. "landscape" re-lays it out 1920×1080.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; T="$B/.."; R="$(cd "$T/../../.." && pwd)"; H="$(cd "$1" && pwd)"; P="$2"
U="$R/video/release/review/upgrade-2026-11-03"
cp "$U/takhian-kit/src/takhian.js" "$U/takhian-kit/src/stormfx.js" "$U/rupnak-kit/lib/rupnak.js" "$U/rupnak-kit/lib/rupnak2.js" "$U/rupnak-kit/lib/rupstill.js" "$U/rupnak-kit/lib/rupx.js" "$T/src/ngw.js" "$H/lib/"
W="$(mktemp -d)"; cat "$B/head.part" "$B/sigcard.part" "$B/helpers.part" "$B/sinkkit.part" "$T/src/handkit.part" "$T/${4:-tw}/common.part" "$T/${4:-tw}/body.part" "$B/foot.part" > "$W/ep.tmpl.html"
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="$T/${4:-tw}/schedule.json" TK_TMPL="$W/ep.tmpl.html" python3 "$B/make.py"
rm -rf "$W"
if [ "${3:-}" = "landscape" ]; then
  cp "$R/video/longform/landscape.js" "$H/$P/assets/"
  python3 - "$H/$P/index.html" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('content="width=1080, height=1920"','content="width=1920, height=1080"'),('width: 1080px; height: 1920px;','width: 1920px; height: 1080px;'),('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"'),('<script src="assets/engine.js"></script>','<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')]:
    s=s.replace(a,b)
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
fi
