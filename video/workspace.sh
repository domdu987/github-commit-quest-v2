#!/usr/bin/env bash
# Rebuild the working layout the production scripts expect from the copies kept in this repo.
# make.py / mix.py resolve ../hf/lib, ../hf/rig, ../hf/<proj>, ../synth.py and ../music relative to each episode folder.
# hf/lib gets the newest shared libraries (from the latest episode); each episode's own lib/ folder keeps the
# exact versions it was rendered with, should an old episode need a byte-identical rebuild.
# Usage: bash video/workspace.sh <work dir>      (then e.g.: cd <work dir>/zom1 && python3 make.py)
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
W="${1:?usage: workspace.sh <work dir>}"
LATEST="$R/zom-ep1"          # newest libraries (rig.js with smooth blends, zom.js, sig.js, voice.py with "take", voice_qa.py)
TEMPLATE="$R/koi-ep3"        # newest rendered composition: HyperFrames project files and fonts
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$LATEST"/lib/*.js "$LATEST"/lib/voice.py "$LATEST"/lib/voice_qa.py "$W/hf/lib/"
cp "$TEMPLATE"/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
cp -r "$TEMPLATE"/composition/assets/fonts "$W/hf/rig/assets/"
cp "$LATEST"/production/synth.py "$W/"
cp "$R"/music/suno1.mp3 "$W/music/"
for n in 1 2 3; do
  mkdir -p "$W/camp$n"
  cp -r "$R/camp-ep$n/production/." "$W/camp$n/"
  cp "$R/camp-ep$n/mix.wav" "$W/camp$n/"
done
for n in 1 2 3; do
  mkdir -p "$W/koi$n"
  cp -r "$R/koi-ep$n/production/." "$W/koi$n/"
  cp -r "$R/koi-ep$n/lib" "$W/koi$n/lib"   # make.py builds from the episode's own libraries (as rendered) + the shared sig.js
  [ -f "$R/koi-ep$n/mix.wav" ] && cp "$R/koi-ep$n/mix.wav" "$W/koi$n/"
done
mkdir -p "$W/zom1"
cp -r "$R/zom-ep1/production/." "$W/zom1/"
[ -f "$R/zom-ep1/mix.wav" ] && cp "$R/zom-ep1/mix.wav" "$W/zom1/"
echo "workspace ready: $W (camp1-3 → hf/camp, hf/camp2, hf/camp3; koi1-3 → hf/koi1-3; zom1 → hf/zom1)"
