#!/bin/bash
# resumable render of shots 11-12 only (take s11 = g753-869; shots 13-14 belong to take s13): two detached workers, resume loops (shot.py skips finished frames)
cd "$(dirname "$0")"; mkdir -p work/frames; export SAMPLES=18
( for pass in 1 2 3; do python3 shot.py 11 753:820 work/frames final >> work/log_11.txt 2>&1; done; echo A > work/doneA ) &
( for pass in 1 2 3; do python3 shot.py 12 821:869 work/frames final >> work/log_12.txt 2>&1; done; echo B > work/doneB ) &
wait
