#!/bin/bash
# take s26 = shots 26-27 (g 1758..1919 incl. 6 handle frames each side); no dissolve baked (done at conform). Resumable; 2 workers x 2 threads.
cd "$(dirname "$0")"; mkdir -p logs raw
( python3 shot.py render 26 1758:1839 raw 1.0 24 2 > logs/s26.log 2>&1 ) &
( python3 shot.py render 27 1840:1919 raw 1.0 24 2 > logs/s27.log 2>&1 ) &
wait
