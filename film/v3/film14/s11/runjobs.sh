#!/bin/bash
# resumable v2 render: two detached workers, each loops until its frame ranges are complete (shot.py skips finished frames)
cd "$(dirname "$0")"; mkdir -p work/frames
worker() { # args: list of "shot a:b"
  for r in "$@"; do set -- $r; python3 shot.py $1 $2 work/frames final >> work/log_$1.txt 2>&1; done; }
export SAMPLES=18
( for pass in 1 2 3; do worker "11 753:820" "12 821:863"; done; echo A > work/doneA ) &
( for pass in 1 2 3; do worker "13 864:929" "14 930:1006"; done; echo B > work/doneB ) &
wait
