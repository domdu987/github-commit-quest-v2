#!/usr/bin/env bash
# Render one episode at 60 fps and mux the two deliverables:
#   <name>-HQ.mp4    video stream copied from the render (no second encode) + AAC 256k — this is the file the user posts
#   <name>-share.mp4 re-encoded CRF 21, small enough for the repo (< 100 MB) — never post this one
# Run it with the Bash tool's run_in_background and timeout 7200000: the default 30-minute background limit kills a render or
# the share encode half-way (EP.2 of เห็ดปอบ lost its share file that way). One episode per call; two calls may run at once.
# usage: render.sh <hf project dir> <episode dir with mix.wav> <name stem, e.g. EP1-ya-hak-sai-khong>
set -euo pipefail
H="$(cd "$1" && pwd)"; E="$(cd "$2" && pwd)"; N="$3"
[ -f "$E/mix.wav" ] || { echo "no $E/mix.wav (run mix.py first)" >&2; exit 1; }
cd "$H"; rm -f "$E/raw.mp4"
npx --yes hyperframes@0.8.185 render -f 60 -o "$E/raw.mp4" > "$E/render.log" 2>&1
cd "$E"
ffmpeg -v error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest "$N-HQ.mp4"
ffmpeg -v error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$N-share.mp4"
echo "done $N"
