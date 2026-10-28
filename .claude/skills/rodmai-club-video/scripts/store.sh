#!/usr/bin/env bash
# Keep a finished episode in the repo so any later chat can rebuild or re-render it byte for byte:
#   video/<repo ep dir>/<name>-share.mp4, mix.wav,
#   production/ (lines.json, timing.py, schedule.json, make.py, mix.py, every *.part, ep.tmpl.html, synth.py, vo/ incl. the mp3 cache),
#   composition/ (index.html + assets + HyperFrames json), lib/ (the exact libraries rendered + voice.py + voice_qa.py)
# The HQ file is NOT committed (it can pass 100 MB); it goes to the user with SendUserFile.
# usage: store.sh <episode dir> <hf project dir> <repo ep dir name, e.g. pop-ep1-v2> <name stem>
set -euo pipefail
W="$(cd "$1" && pwd)"; H="$(cd "$2" && pwd)"; N="$4"
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)/video"
E="$R/$3"
[ -f "$W/$N-share.mp4" ] || { echo "no $W/$N-share.mp4" >&2; exit 1; }
mkdir -p "$E/production"
rm -f "$E"/*-share.mp4
cp "$W/$N-share.mp4" "$W/mix.wav" "$E/"
for f in "$W"/*.part "$W"/ep.tmpl.html "$W"/lines.json "$W"/make.py "$W"/mix.py "$W"/schedule.json "$W"/timing.py "$W"/sfx_cues.json "$W"/sb_labels.json; do
  [ -f "$f" ] && cp "$f" "$E/production/"
done
[ -f "$W/../synth.py" ] && cp "$W/../synth.py" "$E/production/"
rm -rf "$E/production/vo" && mkdir -p "$E/production/vo"
cp "$W"/vo/*.wav "$W"/vo/*.mp3 "$W"/vo/*.json "$E/production/vo/" 2>/dev/null || true
rm -rf "$E/composition" && mkdir -p "$E/composition"
cp -r "$H/index.html" "$H/assets" "$H/package.json" "$H/hyperframes.json" "$H/meta.json" "$E/composition/"
rm -rf "$E/lib" && mkdir -p "$E/lib"
cp "$H"/assets/*.js "$E/lib/"
cp "$H/../lib/voice.py" "$H/../lib/voice_qa.py" "$E/lib/" 2>/dev/null || true
du -sh "$E"
