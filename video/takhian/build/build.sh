#!/bin/bash
# Build the HyperFrames project for one episode of ต้นตะเคียนกลางนา from the repo.
# usage: build.sh <ep 1|2> <workspace hf dir (has lib/ and rig/, from setup_workspace.sh)> [project name, default tk<ep>]
# Copies src/takhian.js + src/stormfx.js into <hf>/lib, assembles the template
#   head + sigcard + helpers + sinkkit + src/handkit + ep<N>/common + ep<N>/body + foot<N>
# and writes <hf>/<project>/index.html with ep<N>/schedule.json. Render: render.sh <hf>/<project> <episode dir> <name>.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; T="$B/.."; E="$1"; H="$(cd "$2" && pwd)"; P="${3:-tk$E}"
cp "$T/src/takhian.js" "$T/src/stormfx.js" "$H/lib/"
W="$(mktemp -d)"; cat "$B/head.part" "$B/sigcard.part" "$B/helpers.part" "$B/sinkkit.part" "$T/src/handkit.part" "$T/ep$E/common.part" "$T/ep$E/body.part" "$B/foot$E.part" > "$W/ep.tmpl.html"
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="$T/ep$E/schedule.json" TK_TMPL="$W/ep.tmpl.html" python3 "$B/make.py"
rm -rf "$W"
