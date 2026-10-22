#!/usr/bin/env bash
# Rebuild the working layout the production scripts expect from the copies kept in this repo.
# make.py / mix.py resolve ../hf/lib, ../hf/rig, ../hf/<proj>, ../synth.py and ../music relative to each episode folder.
# hf/lib gets the newest shared libraries (from the latest episode); each episode's own lib/ folder keeps the
# exact versions it was rendered with, should an old episode need a byte-identical rebuild.
# Usage: bash video/workspace.sh <work dir>      (then e.g.: cd <work dir>/koi1 && python3 make.py)
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
W="${1:?usage: workspace.sh <work dir>}"
LATEST="$R/koi-ep1"
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$LATEST"/lib/*.js "$LATEST"/lib/voice.py "$W/hf/lib/"
cp "$LATEST"/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
cp -r "$LATEST"/composition/assets/fonts "$W/hf/rig/assets/"
cp "$LATEST"/production/synth.py "$W/"
cp "$R"/music/suno1.mp3 "$W/music/"
for n in 1 2 3; do
  mkdir -p "$W/camp$n"
  cp -r "$R/camp-ep$n/production/." "$W/camp$n/"
  cp "$R/camp-ep$n/mix.wav" "$W/camp$n/"
done
mkdir -p "$W/koi1"
cp -r "$R/koi-ep1/production/." "$W/koi1/"
[ -f "$R/koi-ep1/mix.wav" ] && cp "$R/koi-ep1/mix.wav" "$W/koi1/"
echo "workspace ready: $W (camp1-3 → hf/camp, hf/camp2, hf/camp3; koi1 → hf/koi1)"
