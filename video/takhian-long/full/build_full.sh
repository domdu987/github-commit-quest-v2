#!/bin/bash
# Build ต้นตะเคียนกลางนา ฉบับเต็ม: build_full.sh <workspace hf dir> <project> [landscape]
# body = common + { EP.1 } + { bridge } + { EP.2 with colliding shot keys renamed e2_<key> and colliding set ids prefixed q }
# Skipped shots (EP.1 next, EP.2 hook/cmd) are guarded inside their episode block: ADD returns early when SH[k].skip.
set -euo pipefail
F="$(cd "$(dirname "$0")" && pwd)"; T="$F/.."; B="$T/build"; H="$(cd "$1" && pwd)"; P="$2"
python3 "$F/combine.py" >/dev/null
cp "$T/src/takhian.js" "$T/src/stormfx.js" "$H/lib/"
W="$(mktemp -d)"
python3 - "$T" "$W/body.part" <<'PY'
import json, re, sys
T, out = sys.argv[1], sys.argv[2]
S = json.load(open(T + "/full/schedule.json")); col = S["collide"]
e1 = open(T + "/ep1/body.part").read(); e2 = open(T + "/ep2/body.part").read(); br = open(T + "/full/bridge.part").read()
for k in col:
    n = e2.count(f'"{k}"'); assert n > 0, k; e2 = e2.replace(f'"{k}"', f'"e2_{k}"')
for a, b in [('CLR("cr"', 'CLR("qcr"'), ('"cr-amb"', '"qcr-amb"'), ('"#cr-amb"', '"#qcr-amb"'), ('BUND("no"', 'BUND("qno"'), ('BUND("rp"', 'BUND("qrp"'), ('id: "sp"', 'id: "qsp"'), ('CLR("tr"', 'CLR("qtr"')]:
    assert a in e2, a; e2 = e2.replace(a, b)
G = "        const ADD = (k, spec) => (SH[k] && !SH[k].skip ? ADD_G(k, spec) : null);\n"
open(out, "w").write("      const ADD_G = ADD;\n      { // ===== EP.1 =====\n" + G + e1 + "\n      }\n      { // ===== bridge =====\n" + br + "\n      }\n      { // ===== EP.2 =====\n" + G + e2 + "\n      }\n")
PY
sed 's/ต้นตะเคียนกลางนา · EP.2/ต้นตะเคียนกลางนา/' "$B/foot2.part" > "$W/foot.part"
cat "$B/head.part" "$B/sigcard.part" "$B/helpers.part" "$B/sinkkit.part" "$T/src/handkit.part" "$T/ep1/common.part" "$W/body.part" "$W/foot.part" > "$W/ep.tmpl.html"
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="$F/schedule.json" TK_TMPL="$W/ep.tmpl.html" python3 "$B/make.py"
rm -rf "$W"
if [ "${3:-}" = "landscape" ]; then
  cp "$F/landscape.js" "$H/$P/assets/"
  python3 - "$H/$P/index.html" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
for a, b in [('content="width=1080, height=1920"', 'content="width=1920, height=1080"'), ('width: 1080px; height: 1920px;', 'width: 1920px; height: 1080px;'), ('data-width="1080" data-height="1920"', 'data-width="1920" data-height="1080"'), ('<script src="assets/engine.js"></script>', '<script src="assets/engine.js"></script>\n    <script>window.LANDSCAPE = {};</script>\n    <script src="assets/landscape.js"></script>')]:
    assert a in s, a; s = s.replace(a, b)
# as video/tornado/stylekit/build/build.sh: hidden clips leave the layout (Chrome raster memory on the widened stages)
s = s.replace('</style>', '\n      .clip > .capwrap .capbox { font-size: 50px; }\n      .clip > .capwrap { top: 955px !important; }\n      .clip.lfit { background: radial-gradient(ellipse 60% 80% at 50% 50%, #1a2226, #05080a); }\n      .clip[style*="visibility: hidden"] { display: none !important; }\n      .badge { bottom: 40px; }\n    </style>', 1)
open(p, 'w').write(s)
PY
fi
