#!/bin/bash
# relaunch loop: reruns run_all.sh until 162 frames (g 1758..1919) exist
cd "$(dirname "$0")"
while true; do
  n=$(ls raw/*.png 2>/dev/null | wc -l); [ "$n" -ge 162 ] && break
  pgrep -f "shot.py render" >/dev/null || ./run_all.sh >> logs/run_all.log 2>&1
  sleep 20
done
