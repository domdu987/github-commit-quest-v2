#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f "film10/s15|shot.py final 1[56] " >/dev/null || pgrep -f "python3 shot.py final 15" >/dev/null || pgrep -f "python3 shot.py final 16" >/dev/null; do sleep 5; done
python3 shot.py final 17 1084:1193 > log17.txt 2>&1 &
python3 shot.py final 19 1296:1433 > log19.txt 2>&1 &
wait
python3 shot.py final 18 1194:1295 > log18.txt 2>&1
