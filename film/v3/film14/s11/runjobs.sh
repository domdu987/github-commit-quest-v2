#!/bin/bash
cd "$(dirname "$0")"; mkdir -p work/frames
( python3 shot.py 11 753:820 work/frames final > work/log_11.txt 2>&1; python3 shot.py 12 821:863 work/frames final > work/log_12.txt 2>&1; echo A > work/doneA ) &
( python3 shot.py 13 864:929 work/frames final > work/log_13.txt 2>&1; python3 shot.py 14 930:1006 work/frames final > work/log_14.txt 2>&1; echo B > work/doneB ) &
wait
