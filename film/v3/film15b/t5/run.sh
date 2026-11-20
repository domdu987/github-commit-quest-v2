#!/bin/bash
# usage: run.sh draft|final OUTDIR [stride]   (draft: every 2nd frame, 2 procs; final: all frames, 2 procs x 2 threads)
Q=$1; O=$2; S=${3:-2}
cd "$(dirname "$0")"
for k in $(seq 0 $((S-1))); do nohup python3 shot.py --q $Q --out $O --stride $S --offset $k --threads 2 > $O.log.$k 2>&1 & done
