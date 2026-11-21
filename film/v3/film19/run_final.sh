#!/bin/bash
cd "$(dirname "$0")/s24"
for k in 0 1; do python3 shot.py final $(( 1924 + k )):2159:2 1.0 > work_final_$k.log 2>&1 & done; wait
python3 deliver.py > deliver.log 2>&1
echo finished > ../run_final.done
