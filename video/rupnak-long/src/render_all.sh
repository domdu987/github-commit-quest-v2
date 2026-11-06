#!/usr/bin/env bash
# render chapter projects one at a time into /dev/shm (raw video only)
set -uo pipefail
export TMPDIR=/dev/shm/tmp; mkdir -p $TMPDIR /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out
for n in 1 2 3; do
  [ -s /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/c$n.mp4 ] && continue
  cd /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/hf/rkc$n && npx --yes hyperframes@0.8.185 render -f 60 -w 3 -o /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/c$n.part.mp4 > /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/c$n.log 2>&1 && mv /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/c$n.part.mp4 /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/c$n.mp4
  echo "chapter $n exit $?" >> /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/status
done
echo ALLDONE >> /tmp/claude-0/-home-user-github-commit-quest-v2/0d2beef4-35e5-59ae-b226-665b332623b9/scratchpad/lf/out/status
