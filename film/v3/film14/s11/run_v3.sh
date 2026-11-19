#!/bin/bash
# v3: re-render shot 12 only (g821-869), two detached workers with resume loops
cd "$(dirname "$0")"; export SAMPLES=18
( for p in 1 2 3; do python3 shot.py 12 821:845 work/frames final >> work/log_12a.txt 2>&1; done ) &
( for p in 1 2 3; do python3 shot.py 12 846:869 work/frames final >> work/log_12b.txt 2>&1; done ) &
wait
