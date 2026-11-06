#!/bin/bash
# style-frame composition: sf.sh <shots.part> <key1,key2,...>  (each shot 2 s, no voice)
set -euo pipefail
cd "$(dirname "$0")"
python3 - "$2" <<'PY'
import json, sys
ks = sys.argv[1].split(","); shots = [{"key": k, "start": 2.0 * i, "dur": 2.0, "vo": []} for i, k in enumerate(ks)]
json.dump({"total": 2.0 * len(ks), "shots": shots}, open("schedule.json", "w"), ensure_ascii=False)
PY
cat prelude.part "$1" > body.part
cat helpers.part body.part > shots.part && cat head.part sigcard.part shots.part foot.part > ep.tmpl.html && python3 make.py
