#!/bin/bash
# s25 v2 = shot 25 only (director split; shots 26-27 -> take s26, team 3). One process, 4 threads; resumable.
cd "$(dirname "$0")"
python3 shot.py render 25 1672:1770 raw 1.0 24 4 >> logs/s25.log 2>&1
