#!/bin/bash
# posti1.sh : ติดเกาะร้าง EP.1 after the user's OK — 60 fps render of a frozen copy (refused while hold/ISLE1 exists), HQ + share mux,
# checks (frames, duration, loudness, black/freeze, first-frame luma), a 10-frame strip; the cover is built separately (hook/cover_isle.py)
W=/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work
S=$W/isle1; n=ISLE1-phi-am
if [ -e $W/hold/ISLE1 ]; then echo "ISLE1 held (waiting for the user's OK on the preview)"; exit 1; fi
rm -rf $W/hf/ri1; cp -a $W/hf/isle1 $W/hf/ri1 && rm -rf $W/hf/ri1/.hyperframes $W/hf/ri1/work-* $W/hf/ri1/snap_*
cd $W/hf/ri1 && rm -f $S/raw.mp4
nice -n 5 npx --yes hyperframes@0.8.185 render -f 60 -o $S/raw.mp4 > $S/render.log 2>&1 || { echo "Error: render failed"; exit 1; }
cd $S
ffmpeg -nostdin -loglevel error -y -i raw.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart $n-HQ.mp4
bash $W/hook/mkshare.sh $n-HQ.mp4 $n-share.mp4
echo "frames $(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 $n-HQ.mp4)  dur $(ffprobe -v error -show_entries format=duration -of csv=p=0 $n-HQ.mp4)"
ls -l $n-HQ.mp4 $n-share.mp4 | awk '{print $5, $9}'
ffmpeg -nostdin -nostats -i $n-HQ.mp4 -filter_complex ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
echo "black/freeze:"; ffmpeg -nostdin -v info -i $n-HQ.mp4 -vf "blackdetect=d=0.3:pix_th=0.06,freezedetect=n=0.002:d=2.5" -an -f null - 2>&1 | grep -oE "black_(start|end):[0-9.]+|freeze_(start|duration):[0-9.]+" | tr '\n' ' '; echo
echo "first-frame luma: $(ffmpeg -nostdin -v error -i raw.mp4 -frames:v 1 -vf "scale=64:114,format=gray" -f rawvideo - | python3 -c 'import sys; b=sys.stdin.buffer.read(); print(round(sum(b)/len(b)))')"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $n-HQ.mp4); mkdir -p strip; L=""
for k in 0 1 2 3 4 5 6 7 8 9; do t=$(python3 -c "print(round($dur*($k+0.5)/10,2))"); ffmpeg -nostdin -loglevel error -y -ss $t -i $n-HQ.mp4 -frames:v 1 -vf scale=216:-1 strip/s$k.png; L="$L -i strip/s$k.png"; done
ffmpeg -nostdin -loglevel error -y $L -filter_complex "hstack=10" strip/final.jpg && echo strip ok
echo POSTI1 DONE
