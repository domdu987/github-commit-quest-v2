#!/bin/bash
# 50 % scale, 32 sample PASS/MISS sweep -> sweep/<preset>.png + sweep/log.txt   usage: sweep.sh preset...
cd "$(dirname "$0")"; mkdir -p sweep
for p in "$@"; do python3 set25.py render $p sweep/$p.png --draft 0.5 --samples 32 > sweep/$p.out 2>&1; python3 ../../film25/tools/light_metrics.py sweep/$p.png | tee -a sweep/log.txt; done
