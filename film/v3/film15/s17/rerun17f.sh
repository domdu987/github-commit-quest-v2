#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final s17 924:1027 work/f17 12 > work/log17f1.txt 2>&1 ) &
( python3 shot.py final s17 1028:1130 work/f17 12 > work/log17f2.txt 2>&1 ) &
wait
