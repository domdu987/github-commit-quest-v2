#!/usr/bin/env bash
# นาทีก่อนจม ฉบับเต็ม: join the chapter renders, mux the mix, HQ + share (2-pass to ~93 MB)
set -euo pipefail
cd /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out
printf "file '%s'\n" c1.mp4 c2.mp4 c3.mp4 > list.txt
ffmpeg -v error -y -f concat -safe 0 -i list.txt -c copy raw.mp4
for f in c1 c2 c3 raw; do echo "$f frames $(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $f.mp4)"; done
ffmpeg -v error -y -i raw.mp4 -i /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/long/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest LONG-sink-16x9-HQ.mp4
T=$(ffprobe -v error -show_entries format=duration -of csv=p=0 raw.mp4)
VB=$(python3 -c "print(int(93e6*8/$T/1000 - 165))")k
ffmpeg -v error -y -i raw.mp4 -c:v libx264 -preset slow -b:v $VB -pass 1 -passlogfile /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/p2 -pix_fmt yuv420p -an -f mp4 /dev/null
ffmpeg -v error -y -i raw.mp4 -i /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/long/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v $VB -pass 2 -passlogfile /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/p2 -pix_fmt yuv420p -af volume=-0.5dB -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest LONG-sink-16x9-share.mp4
rm -f raw.mp4 p2-0.log p2-0.log.mbtree
ls -la *.mp4; echo FINISHED
