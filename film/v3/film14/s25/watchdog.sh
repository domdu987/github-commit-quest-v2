#!/bin/bash
cd "$(dirname "$0")"
while true; do
  if ! pgrep -f "shot.py render" >/dev/null && ! pgrep -f run_all.sh >/dev/null; then
    n=$(ls raw/*.png 2>/dev/null | wc -l); [ "$n" -ge 257 ] && break
    setsid nohup ./run_all.sh >> logs/run_all.log 2>&1 < /dev/null &
  fi
  sleep 30
done
