#!/bin/bash
# prev7.sh : whole-episode approval preview of ติดเกาะร้าง EP.1 — a 24 fps draft render of a frozen copy, muxed with mix.wav
# (the user's rule "ก่อนเรนเดอร์ทุกครั้งส่งให้ผมก่อน": this is the preview; the 60 fps render stays held by hold/ISLE1)
W=/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work
rm -rf "$W/hf/pi1"; cp -a $W/hf/isle1 $W/hf/pi1 && rm -rf $W/hf/pi1/.hyperframes
cd $W/hf/pi1 && nice -n 5 npx --yes hyperframes@0.8.185 render -f 24 -q draft -o $W/isle1/prev24.mp4 > $W/isle1/prev24.log 2>&1 || { echo "Error: render failed"; exit 1; }
ffmpeg -nostdin -v error -y -i $W/isle1/prev24.mp4 -i $W/isle1/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $W/preview_epi1.mp4 && echo "wrote preview_epi1.mp4"
echo PREV7 DONE
