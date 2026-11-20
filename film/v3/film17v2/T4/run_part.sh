#!/bin/bash
# usage: run_part.sh g0 g1 ; resumes (render_t4 skips frames > 50 kB)
cd /home/user/github-commit-quest-v2/film/v3/film17v2/T4
until python3 render_t4.py $1 $2 frames >> log_$1.txt 2>&1; do sleep 5; done
echo FINISHED >> log_$1.txt
