#!/bin/bash
# renders every preset to finals/<preset>.png (720x1280, 64 samples) + metrics; usage: run_finals.sh [preset ...]
cd "$(dirname "$0")"; mkdir -p finals
PRE=${@:-$(python3 set25.py list 2>/dev/null | tail -1)}
for p in $PRE; do python3 set25.py render $p finals/$p.png > finals/$p.out 2>&1; python3 ../../film25/tools/light_metrics.py finals/$p.png | tee -a finals/metrics_run.txt; grep "^render" finals/$p.out | cut -c1-40 >> finals/metrics_run.txt; done
