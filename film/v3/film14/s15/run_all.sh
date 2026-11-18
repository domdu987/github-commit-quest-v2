#!/bin/bash
# two processes x 2 threads
cd "$(dirname "$0")"; export THREADS=2
( python3 shot.py final 15 995:1061 frames; python3 shot.py final 16 1062:1126 frames; python3 shot.py final 17 1127:1167 frames ) > work/logA.txt 2>&1 &
( python3 shot.py final 18 1168:1225 frames; python3 shot.py final 19 1226:1312 frames ) > work/logB.txt 2>&1 &
wait
