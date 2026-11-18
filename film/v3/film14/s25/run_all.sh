#!/bin/bash
# two worker processes (2 threads each); one location per process, so each shot is its own python run
cd "$(dirname "$0")"
( for s in 25 26 28; do python3 shot.py render $s 0:9999 raw 1.0 24 2 > logs/s$s.log 2>&1; done ) &
( for s in 27 29 30; do python3 shot.py render $s 0:9999 raw 1.0 24 2 > logs/s$s.log 2>&1; done ) &
wait
