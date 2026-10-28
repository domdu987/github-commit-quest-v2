#!/usr/bin/env bash
# Build the working layout of the v2 ("pro look") pipeline from the copies kept in this repo.
# The production scripts resolve ../hf/lib, ../hf/rig, ../hf/<proj>, ../synth.py and ../music relative to each episode folder,
# so everything lives under one work dir (put it in the session scratchpad; nothing here needs committing).
#
# usage: bash .claude/skills/rodmai-club-video/scripts/setup_workspace.sh <work dir> [new episode folder ...]
#   <work dir>/hf/lib     every library of the newest stored episode (video/pop-ep3-v2/lib), overlaid by the newest v2 kit (video/pop/v2/lib),
#                         plus the shared tools in video/lib-shared (maps.js + mapsdata.js: the travel map every journey needs)
#   <work dir>/hf/rig     HyperFrames project template: package.json, hyperframes.json, meta.json, assets/fonts (Kanit + Mali + Sriracha)
#   <work dir>/synth.py   the SFX synthesiser · <work dir>/music/suno1.mp3 the music bed
#   <work dir>/<name>     for every extra argument: a new episode folder seeded from เห็ดปอบ EP.3 v2 (head/helpers/sigcard/foot parts,
#                         make.py with PROJ = hf/<name>, timing.py, mix.py) plus its body.part as body.example.part to learn from
set -euo pipefail
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)/video"
W="${1:?usage: setup_workspace.sh <work dir> [episode ...]}"; shift
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$R"/pop-ep3-v2/lib/*.js "$R"/pop-ep3-v2/lib/voice.py "$R"/pop-ep3-v2/lib/voice_qa.py "$W/hf/lib/"
cp "$R"/pop/v2/lib/*.js "$W/hf/lib/"
cp "$R"/lib-shared/*.js "$W/hf/lib/"
cp "$R"/pop-ep3-v2/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
rm -rf "$W/hf/rig/assets/fonts" && cp -r "$R"/pop-ep3-v2/composition/assets/fonts "$W/hf/rig/assets/"
cp "$R"/pop-ep3-v2/production/synth.py "$W/"
cp "$R"/music/suno1.mp3 "$W/music/"
for n in "$@"; do
  if [ -e "$W/$n" ]; then echo "skip $n: already exists"; continue; fi
  mkdir -p "$W/$n"
  cp "$R"/pop/v2/ep3/{head.part,helpers.part,sigcard.part,foot.part,make.py,timing.py,mix.py} "$W/$n/"
  cp "$R"/pop/v2/ep3/body.part "$W/$n/body.example.part"
  sed -i "s#\"hf\", \"pop3v2\"#\"hf\", \"$n\"#" "$W/$n/make.py"
  # the travel map is always loaded (S12: every journey gets a map)
  sed -i 's#<script src="assets/pop2end.js"></script>#<script src="assets/pop2end.js"></script>\n    <script src="assets/mapsdata.js"></script>\n    <script src="assets/maps.js"></script>#' "$W/$n/head.part"
  sed -i 's#"pop2end.js", #"pop2end.js", "mapsdata.js", "maps.js", #' "$W/$n/make.py"
  grep -q "\"hf\", \"$n\"" "$W/$n/make.py" || { echo "could not set PROJ in $W/$n/make.py" >&2; exit 1; }
done
echo "workspace ready: $W  (libs: $(ls "$W/hf/lib" | wc -l) files)"
echo "next: write <ep>/lines.json → voices → timing.py → body.part, then: cd <ep> && cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py"
