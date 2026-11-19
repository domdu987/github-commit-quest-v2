#!/bin/bash
cd "$(dirname "$0")"; k=$1
for job in "28 1502:1593" "30 1652:1745" "31 1746:1811"; do
  set -- $job; python3 shot.py final $1 $2 $k 2 2>&1 | grep -v "CUEW\|Saved\|^$"; done
