#!/usr/bin/env bash
# Render one episode at 60 fps and mux the two deliverables:
#   <name>-HQ.mp4    video stream copied from the render (no second encode) + AAC 256k — this is the file the user posts
#   <name>-share.mp4 re-encoded CRF 21, small enough for the repo (< 100 MB) — never post this one
# Run it with the Bash tool's run_in_background and timeout 7200000: the default 30-minute background limit kills a render or
# the share encode half-way (EP.2 of เห็ดปอบ lost its share file that way). One episode at a time: two renders at once slow both.
# The picture does not need the mix: start the render first (no mix.wav yet → it renders raw.mp4 and stops), build the mix
# meanwhile, then mux with --mux. ~200 frames a minute on 4 cores (a 2:00 episode ≈ 35–40 min). Progress: tail -c 300 render.log
# usage: render.sh <hf project dir> <episode dir> <name stem, e.g. EP1-thale-thoi-ya-khoi-du> [--mux]
set -euo pipefail
H="$(cd "$1" && pwd)"; E="$(cd "$2" && pwd)"; N="$3"
if [ "${4:-}" != "--mux" ]; then
  cd "$H"; rm -f "$E/raw.mp4"
  npx --yes hyperframes@0.8.185 render -f 60 -o "$E/raw.mp4" > "$E/render.log" 2>&1
fi
[ -f "$E/mix.wav" ] || { echo "raw.mp4 done; no $E/mix.wav yet: run mix.py, then render.sh $1 $2 $3 --mux"; exit 0; }
cd "$E"
ffmpeg -v error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$N-HQ.mp4"
ffmpeg -v error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$N-share.mp4"
echo "done $N"
