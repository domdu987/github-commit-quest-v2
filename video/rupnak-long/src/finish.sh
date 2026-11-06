#!/usr/bin/env bash
# join the chapter renders, mux the full mix, make HQ + share (<=95 MB), and run the file checks
set -euo pipefail
R=/tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out; cd $R
printf "file '%s'\n" c1.mp4 c2.mp4 c3.mp4 > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy raw.mp4
for f in c1 c2 c3 raw; do echo "$f frames $(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $f.mp4)"; done
ffmpeg -v error -y -i raw.mp4 -i /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/long/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest LONG-rupnak-16x9-HQ.mp4
# share: two-pass to ~93 MB incl. 160k audio
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 raw.mp4)
VB=$(python3 -c "print(int(93e6*8/$T/1000 - 165))")k
ffmpeg -v error -y -i raw.mp4 -c:v libx264 -preset slow -b:v $VB -pass 1 -passlogfile $R/p2 -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i raw.mp4 -i /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/long/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v $VB -pass 2 -passlogfile $R/p2 -pix_fmt yuv420p -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest LONG-rupnak-16x9-share.mp4
rm -f raw.mp4 p2-0.log p2-0.log.mbtree
ls -la *.mp4; echo FINISHED
