#!/bin/bash
# two lanes of niced single-thread Blender processes
cd "$(dirname "$0")"
lane() { for job in "$@"; do set -- $job; nice -n 10 python3 tests.py ${job//:/ } > out/log_${job//:/_}.txt 2>&1; done; }
lane "still:UND" "still:STAIR" "cost:X1" "cost:X2" "cost:GEAR" "cost:UND" "final:X1" "final:X2" "final:GEAR" "final:UND" &
lane "cost:X1S" "cost:CAB" "cost:STAIR" "final:X1S" "final:CAB" "final:STAIR" "still:X1" "still:X1S" "still:X2" "still:CAB" "still:GEAR" &
wait
echo ALLDONE > out/queue_done.txt
