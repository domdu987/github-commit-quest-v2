#!/bin/bash
cd "$(dirname "$0")"; mkdir -p logs
( python3 shot.py render 28 0:9999 raw 1.0 24 2 > logs/s28.log 2>&1; python3 shot.py render 30 0:9999 raw 1.0 24 2 > logs/s30.log 2>&1 ) &
( python3 shot.py render 29 0:9999 raw 1.0 24 2 > logs/s29.log 2>&1 ) &
wait; echo ALLDONE > raw/done.txt
