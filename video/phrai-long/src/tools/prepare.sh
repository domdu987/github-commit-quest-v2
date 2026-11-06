#!/bin/bash
# มือพราย long version: fresh working copies from the repo, the theme, every long-version patch, then the schedules.
set -euo pipefail
W="$(cd "$(dirname "$0")/.." && pwd)"; R="$(git -C /home/user/github-commit-quest-v2 rev-parse --show-toplevel)"
bash "$W/tools/fresh.sh"
mkdir -p "$W/music"; cp "$R/video/music/suno1.mp3" "$W/music/suno1.mp3"
python3 "$W/tools/patch_long.py"
python3 "$W/tools/patch_libs.py"
python3 "$W/tools/patch_band.py"
python3 "$W/tools/patch_review.py"
for e in 1 2 3; do (cd "$W/ep$e" && python3 timing.py > timing.log); done
python3 - "$W" <<'PY'
import json, sys
W = sys.argv[1]
for e in (1, 2, 3):
    s = json.load(open(f"{W}/ep{e}/schedule.json"))
    print(f"ep{e}: {s['total']:.3f} s · {len(s['shots'])} shots · first {s['shots'][0]['key']} · last {s['shots'][-1]['key']}")
PY
