#!/bin/bash
cd "$(dirname "$0")"; k=$1
for job in "26 1392:1469" "27 1470:1517" "28 1502:1593" "25 1323:1391"; do
  set -- $job; python3 shot.py final $1 $2 $k 2 2>&1 | grep -v "CUEW\|Saved\|^$"; done
