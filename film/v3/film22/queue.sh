#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film22
while pgrep -f "^python3 shot.py final" >/dev/null; do sleep 10; done
(cd s05 && python3 shot.py final 444 510 > r1.log 2>&1 &) 
(cd s05 && python3 shot.py final 511 576 > r2.log 2>&1 &)
sleep 20
while pgrep -f "^python3 shot.py final" >/dev/null; do sleep 10; done
(cd s04 && python3 shot.py final 318 386 > r1.log 2>&1 &)
(cd s04 && python3 shot.py final 387 455 > r2.log 2>&1 &)
