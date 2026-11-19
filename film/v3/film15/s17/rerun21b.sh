#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final s21 1119:1196 work/f21 12 > work/log21c1.txt 2>&1 ) &
( python3 shot.py final s21 1197:1274 work/f21 12 > work/log21c2.txt 2>&1 ) &
wait
