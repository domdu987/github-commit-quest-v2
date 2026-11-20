#!/bin/bash
# usage: supervisor2.sh G0 G1 : re-runs the renderer for [G0,G1] until every frame exists (resumes, skips files >50kB)
cd /home/user/github-commit-quest-v2; G0=$1; G1=$2
while true; do
  n=0; for g in $(seq $G0 $G1); do f=film/v3/film17v2/T5b2/frames/g_$g.png; [ -f $f ] && [ $(stat -c %s $f) -gt 50000 ] && n=$((n+1)); done
  [ "$n" -ge $((G1-G0+1)) ] && echo DONE $G0-$G1 && break
  python3 -I film/v3/film17v2/T5b2/render_T5b2.py full $G0 $G1 >> /tmp/claude-0/t5b2_render_$G0.log 2>&1
  sleep 5
done
