#!/bin/bash
# lane D wrapper: fitcheck on the three chapter projects (served on 8991-8993) with the chapter schedules
for E in 1 2 3; do O=/tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/fit/c$E; mkdir -p $O; rm -f $O/t*.png
TS=$(python3 -c "import json;s=json.load(open('/tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/long/ch$E.json'));print(' '.join(f\"{sh['start']+sh['dur']*f:.2f}\" for sh in s['shots'] for f in (0.3,0.75)))")
node /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/qa/snapFit.cjs 899$E $O $TS > $O/info.txt 2>&1
echo "chapter $E $(ls $O/t*.png | wc -l) frames, $(grep -c PAGEERROR $O/info.txt) pageerrors"
done; echo FITDONE
