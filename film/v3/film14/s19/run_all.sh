#!/bin/bash
# final render: 3 jobs, 2 at a time (2 threads each); resumable (existing frames are skipped); detached: nohup ./run_all.sh &
cd "$(dirname "$0")"; mkdir -p raw logs
cat jobs.txt | xargs -P 2 -L 1 bash -c 'MZ=14 THREADS=2 python3 shot.py $0 $1 $2 final raw > logs/s19_$0_$1.log 2>&1'
echo ALLDONE > raw/done.txt
