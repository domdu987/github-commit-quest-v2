#!/bin/bash
cd /home/user/github-commit-quest-v2
D=film/v3/film17v2/T8/frames_fix
for r in "1862 1892" "2009 2052"; do
  set -- $r
  n=$(( $2 - $1 + 1 ))
  until [ $(ls $D 2>/dev/null | grep -c "g_") -ge 0 ] && python3 - <<P
import os,sys
ok=all(os.path.exists('$D/g_%04d.png'%g) and os.path.getsize('$D/g_%04d.png'%g)>50000 for g in range($1,$2+1))
sys.exit(0 if ok else 1)
P
  do python3 film/v3/film17v2/T8/render.py range $1 $2 $D >> /tmp/t8_fix.log 2>&1 || sleep 5; done
done
echo ALLDONE >> /tmp/t8_fix.log
