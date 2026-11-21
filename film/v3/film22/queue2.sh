#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film22/s05
while [ $(pgrep -fc "^python3 shot.py final") -gt 1 ]; do sleep 10; done
(nohup python3 shot.py final 444 509 > r1.log 2>&1 &)
(nohup python3 shot.py final 510 576 > r2.log 2>&1 &)
