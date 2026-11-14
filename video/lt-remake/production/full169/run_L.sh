#!/bin/bash
# run_L.sh: render the 16:9 twin of EP.1 (look-test shots then EP.1 shots), skipping frames on disk
cd "$(dirname "$0")"; export LT_ORI=L LT_SAMPLES=10
for s in R1 R2 R3:1 R3:0 R3b R4 R5 S1 S2 S3 S4 S5; do n=${s%%:*}; lv=""; [ "$n" != "$s" ] && lv="--level ${s#*:}"
  python3 lt_look2.py render $n $lv 2>&1 | grep -E "^frame|rror" | grep -v CUEW | tail -1; done
for s in "$@"; do n=${s%%:*}; lv=""; [ "$n" != "$s" ] && lv="--level ${s#*:}"
  python3 lt_ep1.py render $n $lv 2>&1 | grep -E "^frame|rror" | grep -v CUEW | tail -1; done
echo "L-END"
