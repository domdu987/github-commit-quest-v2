#!/usr/bin/env bash
# Rebuild the working layout the production scripts expect from the copies kept in this repo.
# make.py / mix.py resolve ../hf/lib, ../hf/rig, ../hf/campN, ../synth.py and ../music relative to each episode folder.
# Usage: bash video/workspace.sh <work dir>      (then: cd <work dir>/camp3 && python3 make.py)
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
W="${1:?usage: workspace.sh <work dir>}"
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$R"/camp-ep3/lib/*.js "$R"/camp-ep3/lib/voice.py "$W/hf/lib/"
cp "$R"/camp-ep3/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
cp -r "$R"/camp-ep3/composition/assets/fonts "$W/hf/rig/assets/"
cp "$R"/camp-ep3/production/synth.py "$W/"
cp "$R"/music/suno1.mp3 "$W/music/"
for n in 1 2 3; do
  mkdir -p "$W/camp$n"
  cp -r "$R/camp-ep$n/production/." "$W/camp$n/"
  cp "$R/camp-ep$n/mix.wav" "$W/camp$n/"
done
echo "workspace ready: $W (episodes in camp1 camp2 camp3; builds go to hf/camp hf/camp2 hf/camp3)"
