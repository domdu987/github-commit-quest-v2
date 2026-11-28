#!/bin/bash
# checker's re-run of every proof after the fixes: two lanes of niced single-thread Blender processes
cd "$(dirname "$0")"
run() { nice -n 10 python3 tests.py "$@" > "out/log2_$(echo "$@" | tr ' ' '_' | tr -d ',-').txt" 2>&1; echo "$(date +%H:%M:%S) done $*" >> out/queue2.log; }
laneA() { run still X1S; run still CAB; run cost UND; run cost CAB; run cost X1; run final UND --steady 3; run final X1 --steady 3; run final GEAR --steady 3; run still CAB --cam S78 --tier final; run hookcheck; }
laneB() { run still GEAR; run still X1; run still UND; run still STAIR; run cost X1S; run cost GEAR; run cost STAIR; run final X1S --steady 3; run final CAB --steady 3; run final STAIR --steady 3; run final X2 --steady 3; nice -n 10 python3 smoke_register.py > out/log2_smoke.txt 2>&1; echo "$(date +%H:%M:%S) done smoke" >> out/queue2.log; }
: > out/queue2.log
laneA & laneB & wait
echo ALLDONE >> out/queue2.log
