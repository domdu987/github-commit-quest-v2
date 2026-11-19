#!/bin/bash
# s13 = shots 13-14 (g 858-1006 incl. 6 handle frames each side); resumable (shot.py skips finished frames); relaunch if the container restarts
cd "$(dirname "$0")"; mkdir -p work/frames; export SAMPLES=12 THREADS=2
( for pass in 1 2 3 4; do python3 shot.py 13 858:929 work/frames final >> work/log_13.txt 2>&1; done ) &
( for pass in 1 2 3 4; do python3 shot.py 14 930:1006 work/frames final >> work/log_14.txt 2>&1; done ) &
wait
