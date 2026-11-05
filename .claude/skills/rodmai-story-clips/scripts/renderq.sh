#!/usr/bin/env bash
# Render episodes one at a time: disk check (≥ 2 GB), HyperFrames 60 fps with 3 workers, then the skill's mux (HQ + share), raw.mp4 deleted.
# usage (from <mw>/<story>/):  ST=jk bash renderq.sh 1 2        # hf/<ST>1 ↔ ep1, hf/<ST>2 ↔ ep2 … also 1A, 1L, 2L (variants / landscape twins)
# Run it as a Bash background task (run_in_background, timeout 7200000) and keep ≤ 2 episodes per task; a nohup/setsid render gets cancelled.
set -uo pipefail
MW="$(cd "$(pwd)/.." && pwd)"; ST="${ST:-$(basename "$(pwd)")}"
R="$(cd "$(dirname "$0")" && pwd)/../../rodmai-club-video/scripts/render.sh"
[ -f "$R" ] || R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel 2>/dev/null)/.claude/skills/rodmai-club-video/scripts/render.sh"
for n in "$@"; do
  avail=$(df --output=avail -BG /tmp | tail -1 | tr -dc 0-9); [ "$avail" -ge 2 ] || { echo "disk low ($avail G), stop before ep$n"; exit 1; }
  E="$MW/$ST/ep$n"; H="$MW/hf/${ST}$n"
  N="EP$n-${STORY_NAME:-$ST}"        # output stem, e.g. STORY_NAME=jom-kohok → EP1-jom-kohok-HQ.mp4 (EP1L-… for the landscape twin)
  rm -f "$E/raw.mp4"
  (cd "$H" && npx --yes hyperframes@0.8.185 render -f 60 -w 3 -o "$E/raw.mp4" > "$E/render.log" 2>&1) || { echo "render failed ep$n"; exit 1; }
  bash "$R" "$H" "$E" "$N" --mux && rm -f "$E/raw.mp4" && echo "done ep$n"
done
echo "queue end"
