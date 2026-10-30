#!/usr/bin/env bash
# Build the working layout from the copies kept in this repo. Put it in the session scratchpad: nothing here is committed.
# The production scripts resolve ../hf/lib, ../hf/rig, ../hf/<proj>, ../synth.py and ../music relative to each episode folder,
# so everything lives under one work dir.
#
# usage: bash .claude/skills/rodmai-club-video/scripts/setup_workspace.sh <work dir> [episode ...]
#   <work dir>/hf/lib     the newest libraries: everything ตึกโยก EP.1 (the last delivered episode) was rendered with
#                         (video/quake-ep1/lib), overlaid by the newest story kits (video/tide/lib) and the shared travel map
#                         (video/lib-shared) — a superset of every set, cast and UI the channel has built
#   <work dir>/hf/rig     HyperFrames project template: package.json, hyperframes.json, meta.json, assets/fonts (Kanit, Mali, Sriracha)
#   <work dir>/synth.py   the SFX synthesiser · <work dir>/music/suno1.mp3 the music bed
#   each episode argument is one of:
#     <name>              a NEW episode folder seeded from the newest template (ทะเลลด EP.1: head/helpers/sigcard/foot parts,
#                         make.py with PROJ = hf/<name>, timing.py, mix.py) plus its body.part as body.example.part to learn from
#     <name>=<repo dir>   RESUME a saved episode, voices included, e.g. tide1=video/tide/ep1 (work in progress saved by
#                         wip_save.sh) or quake1=video/quake-ep1/production (a delivered one); PROJ is pointed at hf/<name>.
#                         Then `python3 ../hf/lib/voice.py lines.json vo` rebuilds the wavs from the saved mp3s (no credits) and
#                         `python3 timing.py` the schedule.
set -euo pipefail
R="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
V="$R/video"
W="${1:?usage: setup_workspace.sh <work dir> [episode | name=repo dir ...]}"; shift
mkdir -p "$W/hf/lib" "$W/hf/rig/assets" "$W/music"
cp "$V"/quake-ep1/lib/*.js "$V"/quake-ep1/lib/voice.py "$V"/quake-ep1/lib/voice_qa.py "$W/hf/lib/"
cp "$V"/tide/lib/*.js "$W/hf/lib/"
cp "$V"/lib-shared/*.js "$W/hf/lib/"
cp "$V"/quake-ep1/composition/{package.json,hyperframes.json,meta.json} "$W/hf/rig/"
rm -rf "$W/hf/rig/assets/fonts" && cp -r "$V"/quake-ep1/composition/assets/fonts "$W/hf/rig/assets/"
cp "$V"/quake-ep1/production/synth.py "$W/"
cp "$V"/music/suno1.mp3 "$W/music/"
setproj() {  # point make.py's PROJ at hf/<name>
  sed -i -E "s#^PROJ = os.path.join\(HERE, \"..\", \"hf\", \"[^\"]+\"\)#PROJ = os.path.join(HERE, \"..\", \"hf\", \"$2\")#" "$1/make.py"
  grep -q "\"hf\", \"$2\")" "$1/make.py" || { echo "could not set PROJ in $1/make.py" >&2; exit 1; }
}
for arg in "$@"; do
  n="${arg%%=*}"
  if [ -e "$W/$n" ]; then echo "skip $n: $W/$n already exists"; continue; fi
  if [ "$arg" != "$n" ]; then
    src="$R/${arg#*=}"
    [ -f "$src/make.py" ] || { echo "no make.py in $src" >&2; exit 1; }
    mkdir -p "$W/$n" && cp -r "$src/." "$W/$n/"
    setproj "$W/$n" "$n"
    echo "resumed $n from ${arg#*=} ($(ls "$W/$n/vo" 2>/dev/null | grep -c '\.mp3$' || true) saved voice takes)"
  else
    mkdir -p "$W/$n"
    cp "$V"/tide/ep1/{head.part,helpers.part,sigcard.part,foot.part,make.py,timing.py,mix.py} "$W/$n/"
    cp "$V"/tide/ep1/body.part "$W/$n/body.example.part"
    setproj "$W/$n" "$n"
    echo "new episode $n: change the badge in foot.part, SHOTS in timing.py and CUES in mix.py for the new story"
  fi
done
echo "workspace ready: $W  (libs: $(ls "$W/hf/lib" | wc -l) files)"
echo "build: cd <ep> && cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py"
