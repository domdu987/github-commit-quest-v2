#!/bin/bash
# v6b = v6[0,2346) + new[2346,2664) + v6[2664,4334) + new[4334,7200) at 60 fps (frame-exact, on shot cuts);
# near-lossless intermediates, then one final encode with the new mix over the whole thing
set -e
P=/tmp/claude-0/-home-user-github-commit-quest-v2/2379a335-2a12-59c5-bdf9-6c760b7486b5/scratchpad/mw/p2
V6=/home/user/github-commit-quest-v2/video/release/hq/plane-ep2-v6-HQ.mp4
NEW=$P/out6b/full.mp4
S=$P/out6b/seg; mkdir -p $S
seg() { ffmpeg -v error -y -i "$1" -vf "trim=start_frame=$2:end_frame=$3,setpts=PTS-STARTPTS" -an -c:v libx264 -preset veryfast -crf 6 -pix_fmt yuv420p -r 60 "$S/$4.mp4"; echo "$4 $(ffprobe -v error -count_frames -show_entries stream=nb_read_frames -of csv=p=0 $S/$4.mp4)"; }
seg "$V6" 0 2346 a; seg "$NEW" 2346 2664 b; seg "$V6" 2664 4334 c; seg "$NEW" 4334 7200 d
printf "file '%s'\n" $S/a.mp4 $S/b.mp4 $S/c.mp4 $S/d.mp4 > $S/list.txt
OUT=$P/out6b/plane-ep2-v6b-HQ.mp4
ffmpeg -v error -y -f concat -safe 0 -i $S/list.txt -i $P/ep6/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -b:v 5800k -maxrate 8000k -bufsize 12000k -r 60 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size:stream=codec_name,nb_frames -of compact "$OUT"
