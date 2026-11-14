#!/bin/bash
# run_X.sh EP shot[:level]... : final 16:9 render of the EP.2-4 engine (skips frames on disk)
cd "$(dirname "$0")"; export LT_EP=$1 LT_ORI=L LT_SAMPLES=10; shift
for s in "$@"; do n=${s%%:*}; lv=""; [ "$n" != "$s" ] && lv="--level ${s#*:}"
  python3 lt_epx.py render $n $lv 2>&1 | grep -E "^frame|rror" | grep -v CUEW | tail -1; done
echo "X-END $LT_EP"
