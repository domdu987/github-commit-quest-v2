#!/bin/bash
# ship.sh <take> <label> <g0> <g1_excl> "<move>" "<notes>"  : wait for frames, finish, QA.md, status line, commit, push
T=$1; B=/home/user/github-commit-quest-v2/film/v3/film25
cd $B/s21; cp .gitignore $B/$T/.gitignore
timeout 560 bash -c "until [ \$(ls $B/$T/frames 2>/dev/null | wc -l) -ge $(( $4 - $3 )) ]; do sleep 15; done" || { echo "not ready: $(ls $B/$T/frames | wc -l)"; exit 1; }
python3 finish.py ../$T $2 $3 $4 $3 >/dev/null 2>&1
python3 qa_write.py ../$T "$T row $2" "$5" "$6" >/dev/null
M=$(head -n 1 $B/$T/metrics.txt)
S=$(python3 -c "
import json,glob
w=[json.load(open(p))['wall_total'] for p in glob.glob('$B/$T/work/meta/*.json')]
print(round(sum(w)/len(w)))")
cd /home/user/github-commit-quest-v2
echo "| $T (row $2) | g $3-$(( $4 - 1 )) | $S s | $(echo $M | sed 's/|/\\|/g') |" >> film/v3/film25/T3_STATUS.md
git add film/v3/film25; git commit -q -m "film25 T3: take $T (row $2)

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_017iwyCvGSyqdmJ5b3qRADSe"
for i in 1 2 3 4; do git push -q origin render25/t3 2>/dev/null && break || sleep 3; done
echo "$M"
