#!/bin/bash
# มือพราย ฉบับเต็ม (YouTube 16:9): join the three rendered parts with the film mix → HQ, then a 2-pass share under 95 MB, and checks.
#   bash tools/assemble.sh <dir with r1.mp4 r2.mp4 r3.mp4 and mix/film_mix.wav>     writes LONG-phrai-16x9-HQ.mp4, -share.mp4 there
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; D="$1"; cd "$D"
# frames per part and the film length from the schedules (each part ends on a multiple of 0.25 s, so totals × 60 are whole)
read -r F1 F2 F3 T < <(python3 - "$W" <<'PY2'
import json, sys
t = [json.load(open(f"{sys.argv[1]}/ep{e}/schedule.json"))["total"] for e in (1, 2, 3)]
print(*[round(x * 60) for x in t], round(sum(t), 3))
PY2
)
want=($F1 $F2 $F3); echo "parts ${want[*]} frames · film $T s"
for i in 1 2 3; do
  n=$(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames -of csv=p=0 "r$i.mp4")
  [ "$n" = "${want[$((i-1))]}" ] || { echo "r$i.mp4 has $n frames, expected ${want[$((i-1))]}" >&2; exit 1; }; echo "r$i $n frames ok"
done
printf "file '%s'\n" "$D/r1.mp4" "$D/r2.mp4" "$D/r3.mp4" > parts.txt
ffmpeg -v error -y -f concat -safe 0 -i parts.txt -map 0:v:0 -c copy film_v.mp4
ffmpeg -v error -y -i film_v.mp4 -i mix/film_mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -t $T -movflags +faststart LONG-phrai-16x9-HQ.mp4
ffprobe -v error -show_entries format=duration -show_entries stream=codec_name,width,height,r_frame_rate,sample_rate -of compact LONG-phrai-16x9-HQ.mp4
ffmpeg -nostats -i LONG-phrai-16x9-HQ.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
echo "== black >= 0.3 s"; ffmpeg -hide_banner -nostats -i film_v.mp4 -vf "blackdetect=d=0.3:pix_th=0.08" -an -f null - 2>&1 | grep -o "black_start:[0-9.]* black_end:[0-9.]* black_duration:[0-9.]*" || echo none
echo "== frozen >= 3 s"; ffmpeg -hide_banner -nostats -i film_v.mp4 -vf "freezedetect=n=0.002:d=3" -an -f null - 2>&1 | grep -o "freeze_start: [0-9.]*\|freeze_duration: [0-9.]*" | paste - - || echo none
KB=$(python3 -c "print(int((92e6*8/$T - 160e3)/1000))"); echo "share video bitrate ${KB}k"
ffmpeg -v error -y -i LONG-phrai-16x9-HQ.mp4 -c:v libx264 -preset slow -b:v ${KB}k -pass 1 -passlogfile pp -an -f null /dev/null
ffmpeg -v error -y -i LONG-phrai-16x9-HQ.mp4 -map 0:v -map 0:a -c:v libx264 -preset slow -b:v ${KB}k -pass 2 -passlogfile pp -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart LONG-phrai-16x9-share.mp4
rm -f pp-0.log pp-0.log.mbtree
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,width,height,r_frame_rate -show_entries format=duration -of compact LONG-phrai-16x9-share.mp4
ffmpeg -nostats -i LONG-phrai-16x9-share.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
stat -c '%s %n' LONG-phrai-16x9-HQ.mp4 LONG-phrai-16x9-share.mp4; sha256sum LONG-phrai-16x9-HQ.mp4 LONG-phrai-16x9-share.mp4
ffmpeg -v error -y -i LONG-phrai-16x9-share.mp4 -vf "fps=1/2,scale=240:135,tile=12x16" -frames:v 1 share.sheet.jpg
echo ASSEMBLE_DONE
