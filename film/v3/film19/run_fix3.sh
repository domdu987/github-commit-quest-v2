#!/bin/bash
cd "$(dirname "$0")"
for t in "s25 2019 2094" "s26 2077 2159"; do
  set -- $t
  (cd $1 && for k in 0 1; do python3 shot.py final $(( $2 + k )):$3:2 1.0 > work_final_$k.log 2>&1 & done; wait; python3 deliver.py > deliver.log 2>&1)
done
echo finished > run_fix3.done
