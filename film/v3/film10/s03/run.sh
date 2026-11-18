#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "shot.py final [12] " >/dev/null; do sleep 20; done
python3 shot.py final 3 128:212 > work/f3.log 2>&1 &
python3 shot.py final 4 213:298 > work/f4.log 2>&1 &
wait
