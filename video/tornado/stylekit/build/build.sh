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
# and paints black tiles. After every render of the published timeline, only the clip on screen stays in the layout.
s=s.replace('</body>','<script>(() => { const tl = window.__timelines && window.__timelines.main; if (!tl) return;\n  const clips = [...document.querySelectorAll(".clip")].map((c) => [c, +c.dataset.start, +c.dataset.duration]);\n  const sync = () => { const t = tl.time(); for (const [c, a, d] of clips) { const v = t >= a - 1e-4 && t < a + d ? "" : "none"; if (c.style.display !== v) c.style.display = v; } };\n  const r0 = tl.render.bind(tl); tl.render = function (x, y, z) { const o = r0(x, y, z); sync(); return o; }; sync(); })();</script>\n  </body>',1)
s=s.replace('</style>','\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .badge { bottom: 40px; }\n    </style>',1)
open(p,'w').write(s)
PY
fi
