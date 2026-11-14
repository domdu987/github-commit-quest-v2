#!/bin/bash
# run_ep1.sh shot[:level] ... : render EP.1 shots in order (skips frames already on disk)
cd "$(dirname "$0")"
for j in "$@"; do n=${j%%:*}; lv=""; [ "$n" != "$j" ] && lv="--level ${j#*:}"
  python3 lt_ep1.py render $n $lv 2>&1 | grep -E "^frame|rror" | tail -1; done
echo "QUEUE-END $*"
