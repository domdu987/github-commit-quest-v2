#!/bin/bash
# s25b = shot 25 only, g1672-1770 (99 frames); resumable (shot.py skips finished frames with the same scale/samples); relaunch if the container restarts
cd "$(dirname "$0")"; mkdir -p work/frames2
( for pass in 1 2 3 4; do python3 shot.py render 25 1672:1721 work/frames2 1.0 16 2 >> work/logA.txt 2>&1; done ) &
( for pass in 1 2 3 4; do python3 shot.py render 25 1722:1770 work/frames2 1.0 16 2 >> work/logB.txt 2>&1; done ) &
wait
