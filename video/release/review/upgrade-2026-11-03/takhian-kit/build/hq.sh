#!/bin/bash
# HQ for ต้นตะเคียนกลางนา (coordinator 2 พ.ย.: one file for the owner and the repo, < 100 MB):
# x264 slow, 2-pass, ~95 MB total, High / yuv420p / 60 fps / +faststart, AAC 256k from the episode mix.
# Pass 2 must see exactly the frames pass 1 saw: the audio is padded and cut to the video duration (no -shortest, which drops the last frame).
# usage: hq.sh <raw joined video, no audio> <mix.wav> <out HQ.mp4> [target MB, default 95]
set -euo pipefail
RAW="$1"; MIX="$2"; OUT="$3"; MB="${4:-95}"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$RAW")
VK=$(python3 -c "print(int(${MB}*8192/${DUR} - 256))")
echo "duration ${DUR}s → video ${VK} kbps"
P="$(mktemp -d)/x264"
ffmpeg -v error -y -i "$RAW" -c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -r 60 -b:v ${VK}k -pass 1 -passlogfile "$P" -an -f mp4 /dev/null
ffmpeg -v error -y -i "$RAW" -i "$MIX" -map 0:v -map 1:a -c:v libx264 -preset slow -profile:v high -pix_fmt yuv420p -r 60 -b:v ${VK}k -pass 2 -passlogfile "$P" \
  -af apad -c:a aac -b:a 256k -ar 48000 -movflags +faststart -t "$DUR" "$OUT"
rm -f "$P"*
ls -la "$OUT"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=profile,pix_fmt,width,height,r_frame_rate,nb_read_frames -of compact "$OUT"
ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
ffmpeg -nostats -i "$MIX" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | sed 's/^/mix /'
