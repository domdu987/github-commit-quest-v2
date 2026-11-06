#!/usr/bin/env bash
# One episode at a time, 3 Chrome workers (auto-calibration picks 1 on these heavy frames), then the skill's mux step.
MW=/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/mw
R=/home/user/github-commit-quest-v2/.claude/skills/rodmai-club-video/scripts/render.sh
for n in "$@"; do
  avail=$(df --output=avail -BG /tmp | tail -1 | tr -dc 0-9); [ "$avail" -ge 2 ] || { echo "disk low ($avail G), stop before ep$n"; exit 1; }
  E=$MW/lt/ep$n; rm -f $E/raw.mp4
  (cd $MW/hf/lt$n && npx --yes hyperframes@0.8.185 render -f 60 -w 3 -o $E/raw.mp4 > $E/render.log 2>&1) || { echo "render failed ep$n"; exit 1; }
  bash $R $MW/hf/lt$n $E EP$n-welder-lightning --mux && rm -f $E/raw.mp4 && echo "done ep$n"
done
echo "exit 0"
