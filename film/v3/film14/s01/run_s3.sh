#!/bin/bash
# s01 v5: re-render shot 3 (g123-186), resumable, 2 procs
cd "$(dirname "$0")"; export LADDER_DX=2.6
loop(){ log=$1; for i in 1 2 3 4 5 6; do python3 shot.py final 3 $2:$3 frames 12 >> $log 2>&1 && break; echo retry >> $log; done; }
( loop logA.txt 123 154 ) &
( loop logB.txt 155 186 ) &
wait
