#!/bin/bash
# v2 (brighten / clarify) proofs: two lanes of niced single-thread Blender processes
cd "$(dirname "$0")"
run() { nice -n 10 python3 tests.py "$@" > "out/log3_$(echo "$@" | tr ' ' '_' | tr -d ',-').txt" 2>&1; echo "$(date +%H:%M:%S) done $*" >> out/queue3.log; }
laneA() { run still X1S --tag v2; run hookcheck; run still X1 --size 640x360 --tag w169; run still X2 --size 640x360 --tag w169; run still X1S --size 640x360 --tag w169; run still GEAR --size 640x360 --tag w169; }
laneB() { while pgrep -f "tests.py still STAIR|tests.py still UND" > /dev/null; do sleep 5; done; run still CAB --tag v2; run still GEAR --tag v2; run still CAB --size 640x360 --tag w169; run still STAIR --size 640x360 --tag w169; run still UND --size 640x360 --tag w169; }
: > out/queue3.log
laneA & laneB & wait
echo ALLDONE >> out/queue3.log
