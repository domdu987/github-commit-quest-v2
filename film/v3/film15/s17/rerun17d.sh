#!/bin/bash
cd "$(dirname "$0")"
( python3 shot.py final s17 975:1052 work/f17 12 > work/log17d1.txt 2>&1 ) &
( while pgrep -f "shot.py final s24" >/dev/null || [ $(ls work/f24 | wc -l) -lt 72 ]; do sleep 5; done; python3 shot.py final s17 1053:1130 work/f17 12 > work/log17d2.txt 2>&1 ) &
wait
