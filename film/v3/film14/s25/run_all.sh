#!/bin/bash
# s25 = shots 25-27 only (director split; shots 28-30 moved to take s28). Two workers, 2 threads each; resumable.
cd "$(dirname "$0")"
( python3 shot.py render 25 1672:1722 raw 1.0 24 2 > logs/s25a.log 2>&1; python3 shot.py render 26 0:9999 raw 1.0 24 2 > logs/s26.log 2>&1 ) &
( python3 shot.py render 27 0:9999 raw 1.0 24 2 > logs/s27.log 2>&1; python3 shot.py render 25 1723:1767 raw 1.0 24 2 > logs/s25b.log 2>&1 ) &
wait
