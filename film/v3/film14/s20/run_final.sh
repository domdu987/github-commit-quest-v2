#!/bin/bash
# usage: run_final.sh "<shot g0 g1>" ...   (final: 720x1280, 24 samples, 2 threads)
cd "$(dirname "$0")"
for job in "$@"; do set -- $job; THREADS=2 RESUME=1 python3 shot.py $1 $2 $3 final frames >> work_log_$1.txt 2>&1; done
