#!/bin/bash
# ทะเลลด ฉบับเต็ม (YouTube 16:9): join the three rendered parts and the film mix into one HQ file.
# Run after the three renders (PLAN.md §3) have written /dev/shm/tidelong/ep1.mp4, ep2.mp4, ep3.mp4.
#   bash assemble.sh [out.mp4]      default out: /dev/shm/tidelong/LONG-tide-16x9-HQ.mp4
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"; R=/dev/shm/tidelong; OUT="${1:-$R/LONG-tide-16x9-HQ.mp4}"
want=(6780 6150 6795)   # frames at 60 fps: 113.000 s · 102.500 s · 113.250 s
for i in 1 2 3; do
  n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "$R/ep$i.mp4")
  [ "$n" = "${want[$((i-1))]}" ] || { echo "ep$i.mp4 has $n frames, expected ${want[$((i-1))]}" >&2; exit 1; }
done
# video: hard cuts, stream copy (the three renders share one encoder setup)
printf "file '%s'\n" "$R/ep1.mp4" "$R/ep2.mp4" "$R/ep3.mp4" > "$R/parts.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$R/parts.txt" -map 0:v:0 -c copy "$R/film_v.mp4"
# audio: mix/film_mix.wav = the three part mixes joined sample-exact (0 ms crossfade: the fades are inside the parts)
ffmpeg -v error -y -i "$R/film_v.mp4" -i "$T/mix/film_mix.wav" -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 \
  -t 328.75 -movflags +faststart "$OUT"
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate -of compact "$OUT"
ffmpeg -nostats -i "$OUT" -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
sha256sum "$OUT"
