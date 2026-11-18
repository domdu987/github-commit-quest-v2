#!/bin/bash
# take s15 = shots 15-17 only (g 995..1173 incl. handles); shots 18-19 are rendered by team 6 as take s18 (shot.py final 18 1168:1225 / final 19 1226:1312)
cd "$(dirname "$0")"; export THREADS=${THREADS:-4}
( python3 shot.py final 15 995:1061 frames; python3 shot.py final 16 1062:1126 frames; python3 shot.py final 17 1127:1173 frames ) > work/logA.txt 2>&1
