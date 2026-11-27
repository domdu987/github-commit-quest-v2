#!/bin/bash
# tuning render: full res, 24 samples -> d/<preset>_t.png + metrics line.  usage: tn.sh preset...
cd "$(dirname "$0")"; D=/tmp/claude-0/-home-user-github-commit-quest-v2/c258056c-ae4b-5b97-9034-9d0f6592f6c0/scratchpad/set25b/d; mkdir -p $D
for p in "$@"; do python3 set25.py render $p $D/${p}_t.png --samples 24 > $D/${p}_t.out 2>&1; python3 ../../film25/tools/light_metrics.py $D/${p}_t.png | tee -a $D/tune_log.txt; done
