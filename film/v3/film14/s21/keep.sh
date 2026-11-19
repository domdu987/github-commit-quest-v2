#!/bin/bash
# resumable renderer for take s21 (g1362-1458 = 97 frames), relaunches until all frames exist
cd "$(dirname "$0")"; mkdir -p frames logs
while [ $(ls frames/g_*.png 2>/dev/null | wc -l) -lt 97 ]; do
  pgrep -f "shot.py 1362" > /dev/null || (THREADS=4 python3 shot.py 1362 1458 final frames >> logs/render.log 2>&1)
  sleep 5
done
