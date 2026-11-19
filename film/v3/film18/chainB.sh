#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film18
while [ $(ls s17/frames | wc -l) -lt 91 ]; do sleep 20; done
sleep 8
for s in s20 s23; do (cd $s && python3 shot.py final > final.log 2>&1); done
