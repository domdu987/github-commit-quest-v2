#!/bin/bash
cd "$(dirname "$0")"
while [ $(ls work/f17 | wc -l) -lt 207 ]; do sleep 5; done
python3 shot.py final s21 1119:1274 work/f21 12 > work/log21b.txt 2>&1
