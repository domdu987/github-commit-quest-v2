#!/bin/bash
# post7.sh : after the EP.7 60 fps render — HQ/share/strip + checks, the cold-open hook (ครูพิม "ตบหลัง! ตบแรงๆ!" 36.0 + 1.9 s, FADEIN 0.2 because
# the episode opens bright), the cover from the choking frame, the repo copy
W=/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work
R=/home/user/github-commit-quest-v2
set -e
n=EP7-khon-rai-prayot
bash $W/finish.sh 7 $n
cd $W/fence7
echo "black/freeze:"; ffmpeg -nostdin -v info -i $n-HQ.mp4 -vf "blackdetect=d=0.3:pix_th=0.06,freezedetect=n=0.002:d=2.5" -an -f null - 2>&1 | grep -oE "black_(start|end):[0-9.]+|freeze_(start|duration):[0-9.]+" | tr '\n' ' '; echo
echo "first-frame luma: $(ffmpeg -nostdin -v error -i raw.mp4 -frames:v 1 -vf "scale=64:114,format=gray" -f rawvideo - | python3 -c 'import sys; b=sys.stdin.buffer.read(); print(round(sum(b)/len(b)))')"
# the cold open
bash $W/hook/mkhook.sh $W/fence7/$n-HQ.mp4 $W/hook/$n-HQ-hook.mp4 36.0 1.9 $W/hook/hl7.png $W/hook/hook7_sfx.wav 0.2
bash $W/hook/mkshare.sh $W/hook/$n-HQ-hook.mp4 $W/hook/$n-hook-share.mp4
ffmpeg -nostdin -nostats -i $W/hook/$n-HQ-hook.mp4 -filter_complex ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
# the cover: ปั้น at the table, hands at her throat, the symptom cards above
ffmpeg -nostdin -loglevel error -y -ss 34.5 -i raw.mp4 -frames:v 1 $W/hook/cov7_frame.png
cd $W/hook && python3 cover.py $W/hook/cov7_frame.png $W/hook/cover-ep7.jpg "EP.7" "เด็กสำลักข้าว พูดไม่ได้…" "แค่ตบหลัง… พอมั้ย?" 1180 0.8
cp -f $W/hook/cover-ep7.jpg $R/video/fence/hook/cover-ep7.jpg
bash $W/deliver.sh 7 $n
echo POST7 DONE
