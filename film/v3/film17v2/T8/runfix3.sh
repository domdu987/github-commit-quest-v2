#!/bin/bash
# usage: runfix3.sh g0 g1 tag : resumable render of g0-g1 into frames_fix3 (render.py skips frames already written)
cd /home/user/github-commit-quest-v2
D=film/v3/film17v2/T8/frames_fix3
until python3 - <<P
import os,sys
sys.exit(0 if all(os.path.exists('$D/g_%04d.png'%g) and os.path.getsize('$D/g_%04d.png'%g)>50000 for g in range($1,$2+1)) else 1)
P
do python3 film/v3/film17v2/T8/render.py range $1 $2 $D >> /tmp/t8_f3_$3.log 2>&1 || sleep 5; done
echo ALLDONE >> /tmp/t8_f3_$3.log
