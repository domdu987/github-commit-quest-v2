#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "s24/shot.py\|shot.py final 19" >/dev/null; do sleep 15; done
for t in "s23 1847 1941" "s25 2019 2094" "s26 2077 2159"; do
  set -- $t
  (cd $1 && for k in 0 1; do python3 shot.py final $(( $2 + k )):$3:2 1.0 > work_final_$k.log 2>&1 & done; wait)
done
