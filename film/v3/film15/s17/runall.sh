#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final s17 924:1130 work/f17 12 > work/log17.txt 2>&1 ) &
( python3 shot.py final s21 1119:1274 work/f21 12 > work/log21.txt 2>&1; python3 shot.py final s24 1263:1334 work/f24 12 > work/log24.txt 2>&1 ) &
wait
