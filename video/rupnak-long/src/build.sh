#!/bin/bash
# Build the full-story 16:9 project: build.sh <hf dir> <project>
set -euo pipefail
D="$(cd "$(dirname "$0")" && pwd)"; U="$D/../br/video/rupnak/upgrade"; H="$(cd "$1" && pwd)"; P="$2"
python3 "$D/assemble.py" "$U" "$D/ep.tmpl.html"
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="${SCHED:-$D/schedule.json}" TK_TMPL="$D/ep.tmpl.html" python3 "$U/build/make.py"
cp "$D/../br/video/longform/landscape.js" "$H/$P/assets/"
cp "$D/chipfix.js" "$H/$P/assets/"
python3 - "$H/$P/index.html" <<'PY'
import sys
p=sys.argv[1]; s=open(p).read()
for a,b in [('content="width=1080, height=1920"','content="width=1920, height=1080"'),('width: 1080px; height: 1920px;','width: 1920px; height: 1080px;'),('data-width="1080" data-height="1920"','data-width="1920" data-height="1080"'),('<script src="assets/engine.js"></script>','<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>\n    <script src="assets/chipfix.js"></script>')]:
    assert a in s, a; s=s.replace(a,b)
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip > .capwrap { top: 955px !important; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
echo "built $H/$P"
