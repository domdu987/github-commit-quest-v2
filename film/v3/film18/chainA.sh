#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film18
while pgrep -f "s16/shot.py|python3 shot.py final" >/dev/null && [ $(ls s16/frames | wc -l) -lt 120 ]; do sleep 20; done
sleep 5
for s in s18 s19; do (cd $s && python3 shot.py final > final.log 2>&1); done
