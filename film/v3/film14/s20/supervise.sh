#!/bin/bash
# relaunch loop: if a worker chain is dead and its frames are unfinished, restart it (finished frames are skipped, RESUME=1)
cd "$(dirname "$0")"
need() { for g in $(seq $1 $2); do [ -f frames/g_$g.png ] || return 0; done; return 1; }
while true; do
  A=0; B=0
  need 1301 1502 && A=1; need 1503 1683 && B=1
  if [ $A = 1 ] && ! pgrep -f "run_final.sh 20 1301" >/dev/null && ! pgrep -f "shot.py 2[012] " >/dev/null; then setsid nohup ./run_final.sh "20 1301 1367" "21 1368 1452" "22 1453 1502" >/dev/null 2>&1 & fi
  if [ $B = 1 ] && ! pgrep -f "run_final.sh 23 1503" >/dev/null && ! pgrep -f "shot.py 2[34] " >/dev/null; then setsid nohup ./run_final.sh "23 1503 1598" "24 1599 1683" >/dev/null 2>&1 & fi
  [ $A = 0 ] && [ $B = 0 ] && break
  sleep 60
done
