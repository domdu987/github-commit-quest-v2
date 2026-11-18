#!/bin/bash
# relaunch loop: re-runs the (resumable) renderer until frames g 995..1173 all exist
cd "$(dirname "$0")"
while [ $(ls frames/g_*.png 2>/dev/null | awk -F'[_.]' '$2>=995 && $2<=1173' | wc -l) -lt 179 ]; do
  pgrep -f "shot.py final" > /dev/null || ./run_all.sh
  sleep 30
done
