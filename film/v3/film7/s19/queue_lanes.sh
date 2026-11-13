#!/bin/bash
# lane runner for takes s18 / s19 after s16 (two lanes, 2 threads each)
cd "$(dirname "$0")/.."
lane=$1
if [ "$lane" = A ]; then
  while pgrep -f "shot.py final 1,2,3 1530" >/dev/null; do sleep 20; done
  (cd s18 && python3 shot.py final 1,2 1758:1835 > work/finA.log 2>&1)
  (cd s19 && python3 shot.py final 1,2 1873:1964 > work/finA.log 2>&1)
else
  while pgrep -f "shot.py final 4,5 1664" >/dev/null; do sleep 20; done
  (cd s18 && python3 shot.py final 3 1836:1884 > work/finB.log 2>&1)
  (cd s19 && python3 shot.py final 3,4 1965:2049 > work/finB.log 2>&1)
fi
