#!/usr/bin/env bash
# Rebuild the working layout the production scripts expect from the copies kept in this repo.
# make.py / mix.py resolve ../hf/lib, ../hf/rig, ../hf/<proj>, ../synth.py and ../music relative to each episode folder.
# hf/lib gets the newest shared libraries (from the latest episode); each episode's own lib/ folder keeps the
# exact versions it was rendered with, should an old episode need a byte-identical rebuild.
# Usage: bash video/workspace.sh <work dir>      (then e.g.: cd <work dir>/zom1 && python3 make.py)
set -euo pipefail
R="$(cd "$(dirname "$0")" && pwd)"
W="${1:?usage: workspace.sh <work dir>}"
LATEST="$R/mok-ep1"          # newest libraries (rendered last: engine.js with the "drop" ease, opener.js, mok.js, hands.js, phrai.js, sig.js, voice.py, voice_qa.py)
TEMPLATE="$R/koi-ep3"        # newest rendered composition: HyperFrames project files and fonts
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$LATEST"/lib/*.js "$LATEST"/lib/voice.py "$LATEST"/lib/voice_qa.py "$W/hf/lib/"
cp "$R"/brand/opener/opener.js "$W/hf/lib/"   # EP.1 opener of every new story: title in the sky, dive down to the first scene
cp "$TEMPLATE"/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
cp -r "$TEMPLATE"/composition/assets/fonts "$W/hf/rig/assets/"
cp "$LATEST"/production/synth.py "$W/"   # includes the car sounds: engine screech blinker ratchet motor stalk
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
for n in 1 2 3; do
  [ -d "$R/zom-ep$n/production" ] || continue
  mkdir -p "$W/zom$n"
  cp -r "$R/zom-ep$n/production/." "$W/zom$n/"
  [ -f "$R/zom-ep$n/mix.wav" ] && cp "$R/zom-ep$n/mix.wav" "$W/zom$n/"
done
for ep in mok-ep1:mok1 mok-ep2:mok2 mok-ep3:mok3 phrai-ep1:phrai1; do
  src="$R/${ep%%:*}"; dst="$W/${ep##*:}"
  [ -d "$src/production" ] || continue
  mkdir -p "$dst"; cp -r "$src/production/." "$dst/"
  [ -f "$src/mix.wav" ] && cp "$src/mix.wav" "$dst/"
done
echo "workspace ready: $W (camp1-3 → hf/camp, hf/camp2, hf/camp3; koi1-3 → hf/koi1-3; zom1-3 → hf/zom1-3; mok1-3 → hf/mok1-3; phrai1 = paused draft)"
