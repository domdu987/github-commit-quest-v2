#!/bin/bash
# Build the HyperFrames project for one episode of รูพญานาค from the repo (same contract as video/takhian/build/build.sh).
# usage: [TK_RANGE="a b"] build.sh <ep 1|2|3> <workspace hf dir (has lib/ and rig/, from setup_workspace.sh)> [project name, default rk<ep>]
# Copies lib/*.js into <hf>/lib (lib/rig2-fingers.js → rig2.js: the stock rig plus an opt-in "fingers" flag; every other cast draws
# exactly as before), assembles head + sigcard + helpers + ep<N>/body + foot<N>, writes <hf>/<project>/index.html with ep<N>/schedule.json.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; T="$B/.."; E="$1"; H="$(cd "$2" && pwd)"; P="${3:-rk$E}"
cp "$T/lib/rupnak.js" "$T/lib/rupnak2.js" "$T/lib/rupui.js" "$T/lib/rupcast.js" "$T/lib/rupstill.js" "$T/lib/rupx.js" "$H/lib/"
cp "$T/lib/rig2-fingers.js" "$H/lib/rig2.js"
W="$(mktemp -d)"; cat "$B/head.part" "$B/sigcard.part" "$B/helpers.part" "$T/ep$E/body.part" "$B/foot$E.part" > "$W/ep.tmpl.html"
TK_LIB="$H/lib" TK_PROJ="$H/$P" TK_SCHED="$T/ep$E/schedule.json" TK_TMPL="$W/ep.tmpl.html" python3 "$B/make.py"
rm -rf "$W"
