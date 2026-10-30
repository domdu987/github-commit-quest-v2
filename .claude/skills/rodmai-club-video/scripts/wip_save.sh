#!/usr/bin/env bash
# Save an episode that is still in progress into the repo, so the next chat can resume it with
# `setup_workspace.sh <work> <name>=video/<story>/epN` without spending voice credits again.
# Keeps: every *.part, lines.json, timing.py, make.py, mix.py, schedule.json, sb_labels.json, CAPTIONS-like notes (*.md),
# and the voice takes vo/*.mp3 + vo/durations.json (+ vo/qa.json). Skips renders, snapshots and wavs (they are rebuilt).
# Libraries the episode needs that are new or changed must be saved too: copy them into video/<story>/lib/ and add that
# folder to setup_workspace.sh (it overlays video/tide/lib today).
#
# usage: wip_save.sh <episode dir in the work dir> <repo dir, e.g. video/tide/ep1>
set -euo pipefail
E="$(cd "${1:?usage: wip_save.sh <episode dir> <repo dir>}" && pwd)"
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
D="$R/${2:?usage: wip_save.sh <episode dir> <repo dir>}"
mkdir -p "$D/vo"
for f in "$E"/*.part "$E"/lines.json "$E"/timing.py "$E"/make.py "$E"/mix.py "$E"/schedule.json "$E"/sb_labels.json "$E"/*.md; do
  [ -f "$f" ] && cp "$f" "$D/"
done
rm -f "$D/ep.tmpl.html" "$D/shots.part"   # both are rebuilt from the parts
cp "$E"/vo/*.mp3 "$D/vo/" 2>/dev/null || true
for f in durations.json qa.json; do [ -f "$E/vo/$f" ] && cp "$E/vo/$f" "$D/vo/"; done
echo "saved $(ls "$D" | wc -l) files and $(ls "$D/vo" | grep -c '\.mp3$' || true) voice takes to ${2}"
echo "next: git add ${2} && git commit && git push (and update video/STATUS.md)"
