#!/bin/bash
# make.sh -- rebuild everything for the opening (shots/s01.py): frame SVGs, raw frames, mixed frames, captions JSON, MP4,
# contact sheet, comparison image, metrics.          usage:  ./make.sh            (final quality, about 2 minutes)
#                                                            DRAFT=1 ./make.sh    (dsf 1, about 1 minute)
set -e
V2="$(cd "$(dirname "$0")" && pwd)"
PROJ="$(dirname "$V2")"
SHOTS="${SHOTS:-$V2/shots/s01.py}"
OUT="$V2/out"
cd "$V2"
mkdir -p "$OUT"

echo "== 1/7 build: frame SVGs, manifest, caps.json, qa.json"
python3 build.py "$SHOTS" --out "$OUT"

echo "== 2/7 render: one persistent Chromium page"
rm -rf "$OUT/raw"
if [ -n "$DRAFT" ]; then
  node render.js "$OUT/manifest.json" --dsf 1 --jpg
else
  node render.js "$OUT/manifest.json" --dsf 2 --jpg --quality 98     # 2x supersampling, scaled down in step 3
fi

echo "== 3/7 post: scale, mix the dissolves (smoothstep) -> out/frames/f_0001.png ..."
python3 post.py "$OUT/manifest.json"

echo "== 4/7 assemble: captions burned last, H.264"
# caps_burn.json = caps.json plus the libass size calibration (\fs70), see build.py; the tool itself is untouched
python3 "$PROJ/assemble.py" "$OUT/frames" "$OUT/proto_v2.mp4" "$OUT/caps_burn.json" 30 2>&1 | tail -1

echo "== 5/7 contact sheet and comparison image"
python3 tools/sheet.py contact "$OUT/proto_v2.mp4" "$OUT/contact_v2.jpg" 12 6 360
python3 tools/compare.py 120

echo "== 6/7 staging and camera checks"
python3 tools/qa_check.py "$OUT/qa.json" | tee "$OUT/qa_check.txt"
python3 tools/pop_check.py "$OUT/frames" | tail -1 | tee -a "$OUT/qa_check.txt"

echo "== 7/7 metrics"
[ -f "$OUT/edge_softness.json" ] || python3 tools/edge_setting_test.py > /dev/null
python3 tools/metrics_report.py 40 70 120 147 > /dev/null
python3 tools/write_metrics.py
echo "done: $OUT/proto_v2.mp4"
