#!/bin/bash
cd "$(dirname "$0")"
cat jobs.txt | xargs -P 2 -L 1 bash -c 'python3 shot.py $0 $1 work/frames final > work/log_$0_${1/:/_}.txt 2>&1'
echo ALLDONE > work/done.txt
