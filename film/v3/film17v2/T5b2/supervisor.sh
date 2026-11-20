#!/bin/bash
# restart supervisor: re-runs the renderer until all frames g1297-1383 exist (resumes, skips files >50kB)
cd /home/user/github-commit-quest-v2
while true; do
  n=$(find film/v3/film17v2/T5b2/frames -name 'g_*.png' -size +50k | wc -l)
  [ "$n" -ge 87 ] && echo DONE && break
  python3 -I film/v3/film17v2/T5b2/render_T5b2.py full 1297 1383 >> /tmp/claude-0/t5b2_render.log 2>&1
  sleep 5
done
