#!/bin/bash
# v2: UND after the far-side dressing, the v1 figure measurements, and the 24-frame draft cost of the changed sets
cd "$(dirname "$0")"
run() { nice -n 10 python3 tests.py "$@" > "out/log4_$(echo "$@" | tr ' ' '_' | tr -d ',-/' | cut -c1-80).txt" 2>&1; echo "$(date +%H:%M:%S) done $*" >> out/queue4.log; }
laneA() { run still UND --tag v2; run measure STAIR --camdefs _v1_src --tag v1; run measure UND --camdefs _v1_src --tag v1; run cost UND; run cost X1S; }
laneB() { run still UND --size 640x360 --tag w169; run measure STAIR --tag v2; run measure UND --tag v2; run cost STAIR; run cost CAB; }
: > out/queue4.log
laneA & laneB & wait
echo ALLDONE >> out/queue4.log
