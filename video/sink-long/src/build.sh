#!/usr/bin/env bash
# นาทีก่อนจม ฉบับเต็ม: build a 16:9 HyperFrames project.  usage: [SCHED=long/ch1.json] build.sh <project name>
set -euo pipefail
K="$(cd "$(dirname "$0")/.." && pwd)"; P="$1"; SCHED="${SCHED:-$K/long/schedule.json}"
python3 "$K/long/assemble.py" "$K/video" "$K/build/ep.tmpl.html" "$K/long/land.json" >/dev/null
TK_HERE="$K/build" TK_LIB="$K/hf/lib" TK_PROJ="$K/hf/$P" TK_SCHED="$SCHED" TK_RIG="$K/hf/rig" python3 "$K/build/make.py" >/dev/null
cp "$K/video/longform/landscape.js" "$K/hf/$P/assets/"
python3 - "$K/hf/$P/index.html" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('content="width=1080, height=1920"','content="width=1920, height=1080"'),('width: 1080px; height: 1920px;','width: 1920px; height: 1080px;'),('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"'),('<script src="assets/engine.js"></script>','<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')]:
    assert a in s, a; s=s.replace(a,b)
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
echo "built $K/hf/$P ($(python3 -c "import json;print(json.load(open('$SCHED'))['total'])") s)"
