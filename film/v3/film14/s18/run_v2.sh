#!/bin/bash
# s18 v2: shot 19 only, camera inside the fence; resumable; 2 procs x 2 threads, 12 samples
cd "$(dirname "$0")"; export THREADS=2 SAMPLES=12 S19V=2; mkdir -p work frames_v2
loop(){ log=$1; a=$2; b=$3; for i in 1 2 3 4 5 6; do python3 shot.py final 19 $a:$b frames_v2 >> $log 2>&1 && break; echo retry >> $log; done; }
( loop work/v2A.txt 1226 1268 ) &
( loop work/v2B.txt 1269 1312 ) &
wait
