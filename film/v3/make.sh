#!/bin/sh
# v3: the whole pipeline for the first 5 s.  Usage: sh make.sh [samples=12]
# Resumable: finished frames (PNG + meta json) are skipped; a change of the Thai timing file re-renders everything.
set -e
V3="$(cd "$(dirname "$0")" && pwd)"
S="${1:-12}"
cd "$V3/shots"
python3 timing.py
python3 render_all.py A "$V3/out/raw" --samples "$S" --threads 2 > "$V3/tmp/shots/logs/final_A.log" 2>&1 &
python3 render_all.py B "$V3/out/raw" --samples "$S" --threads 2 > "$V3/tmp/shots/logs/final_B.log" 2>&1 &
wait
python3 render_layers.py A "$V3/out/raw"                  # plate + actor matte for the fast frames outside the whip
python3 render_layers.py B "$V3/out/raw"
python3 post.py "$V3/out/raw" "$V3/out/frames"            # camera streak: plate streaked, actors sharp; whip streaked whole
python3 finish.py "$V3/out/frames" "$V3/out"              # Thai captions last, then the narration
python3 sheets.py "$V3/out/proto_v3.mp4" "$V3/out"        # contact_v3.jpg, compare_v3.png, aspects_v3.png
python3 cues.py "$V3/out/sfx_cues.json"                   # cue sheet for sound
