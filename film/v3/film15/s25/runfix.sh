#!/bin/bash
cd "$(dirname "$0")"; k=$1
for job in "28 1510:1517" "29 1586:1593" "27 1510:1517" "28 1502:1509" "28 1586:1593" "29 1578:1585"; do
  set -- $job; python3 shot.py final $1 $2 $k 2 2>&1 | grep -v "CUEW\|Saved\|^$"; done
