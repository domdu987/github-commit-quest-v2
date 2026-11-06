#!/usr/bin/env bash
# render the นาทีก่อนจม chapter projects one at a time (raw video only) into /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out
set -uo pipefail
export TMPDIR=/dev/shm/tmp; mkdir -p $TMPDIR
for n in 1 2 3; do
  [ -s /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/c$n.mp4 ] && continue
  rm -rf /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/work-* /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/.c$n.part*
  P=skr$n; [ -d /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/hf/$P ] || P=skc$n; cd /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/hf/$P && npx --yes hyperframes@0.8.185 render -f 60 -w 3 -o /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/c$n.part.mp4 > /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/c$n.log 2>&1 && mv /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/c$n.part.mp4 /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/c$n.mp4
  echo "chapter $n exit $?" >> /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/status
done
echo ALLDONE >> /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/sk/out/status
