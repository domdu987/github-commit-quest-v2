#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film10
( cd s01 && python3 shot.py final 2 69:139 > work/f2.log 2>&1; cd ../s03 && python3 shot.py final 4 213:298 > work/f4.log 2>&1 ) &
( cd s03 && python3 shot.py final 3 128:212 > work/f3.log 2>&1 ) &
wait
