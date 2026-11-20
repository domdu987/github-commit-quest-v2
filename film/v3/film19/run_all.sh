#!/bin/bash
# team9 final renders, one take at a time, two processes each (interleaved frames)
cd "$(dirname "$0")"
for t in "s23 1847 1941" "s24 1924 2036" "s25 2019 2094" "s26 2077 2159"; do
  set -- $t
  (cd $1 && for k in 0 1; do python3 shot.py final $(( $2 + k )):$3:2 1.0 > work_final_$k.log 2>&1 & done; wait)
done
