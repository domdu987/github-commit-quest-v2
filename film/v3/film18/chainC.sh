#!/bin/bash
cd /home/user/github-commit-quest-v2/film/v3/film18
run(){ s=$1; a=$2; m=$3; b=$4; (cd $s && rm -rf frames && (python3 shot.py final $a $m > fa.log 2>&1 &) ; (python3 shot.py final $((m+1)) $b > fb.log 2>&1) ); while pgrep -f "$s/shot.py|shot.py final" >/dev/null; do sleep 5; done; }
for spec in "s18 1382 1407 1432" "s17 1303 1347 1393" "s20 1509 1555 1601" "s19 1421 1470 1520" "s16 1195 1254 1314"; do set -- $spec; run $1 $2 $3 $4; echo done $1 >> chainC.log; done
