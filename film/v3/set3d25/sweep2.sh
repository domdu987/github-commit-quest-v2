#!/bin/bash
# gentle-grade sweep: 50 % scale, 32 samples -> sweep2/<preset>.png + sweep2/log.txt
cd "$(dirname "$0")"; mkdir -p sweep2
for p in "$@"; do python3 set25.py render $p sweep2/$p.png --draft 0.5 --samples 32 > sweep2/$p.out 2>&1; python3 ../../film25/tools/light_metrics.py sweep2/$p.png | tee -a sweep2/log.txt; done
