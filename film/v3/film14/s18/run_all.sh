#!/bin/bash
# resumable (existing frames are skipped); 2 processes x 2 threads; relaunch this script if the container restarts
cd "$(dirname "$0")"; export THREADS=2 SAMPLES=12; mkdir -p work frames
loop(){ log=$1; shift; while [ $# -gt 0 ]; do for i in 1 2 3 4 5 6; do python3 shot.py final $1 $2 frames >> $log 2>&1 && break; echo retry >> $log; done; shift 2; done; }
( loop work/logA.txt 18 1162:1226 19 1290:1312 ) &
( loop work/logB.txt 19 1227:1289 ) &
wait
