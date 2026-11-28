#!/bin/bash
# regrade.sh <take> <label> <g0> <g1> <first> <last> "<move>"  : autograde existing frames in place, then re-finish + push
export SETPROJ=/tmp/claude-0/-home-user-github-commit-quest-v2/f179a70c-581e-5684-9961-eff4e8515831/scratchpad/snap/film
cd $(dirname $0)/$1 && python3 shot.py autograde $5:$6 2>&1 | grep AUTOGRADE
rm -f QA.md; python3 ../s06/finish.py . "$2" $3 $4 $5 $6 --move "$7" --push 2>&1 | grep -E "row" | cut -c1-230
