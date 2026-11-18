#!/bin/sh
# usage: runloop.sh log shot a:b ... ; retries a shot until all frames exist (process crashes are rare but real)
log=$1; shift
while [ $# -gt 0 ]; do
  shot=$1; rng=$2; shift 2
  for i in 1 2 3 4 5 6; do python3 shot.py final $shot $rng frames 12 >> $log 2>&1 && break; echo "retry $shot" >> $log; done
done
