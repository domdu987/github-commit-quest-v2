#!/bin/bash
# usage: runall.sh k   (k = 0|1 : interleaved half of every range)
cd "$(dirname "$0")"
k=$1
for job in "25 1323:1391" "26 1392:1469" "27 1470:1517" "28 1502:1593" "29 1578:1651" "30 1652:1745" "31 1746:1811"; do
  set -- $job
  python3 shot.py final $1 $2 $k 2 2>&1 | grep -v "CUEW\|Saved\|^$"
done
