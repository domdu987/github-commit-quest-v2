#!/bin/bash
# join_one.sh <g>: T6a2's light setup (shade_mul 0.8, fill_w 220, gain 0.65, beam off) before g1548; eased (smoothstep) to T6b's override (1.4 / 600 / 1.15) over g1548-1575; beam hidden in this range
cd "$(dirname "$0")"
g=$1
J=$(python3 - "$g" <<'PY'
import sys, json
g = int(sys.argv[1]); u = max(0.0, min(1.0, (g - 1548) / 27.0)); m = u * u * (3 - 2 * u)
print(json.dumps({"shade_mul": round(0.8 + 0.6 * m, 4), "fill_w": round(220 + 380 * m, 2), "gain": round(0.65 + 0.5 * m, 4), "beam_k": 0}))
PY
)
T6EXTRA="$J" BEAMOFF=1 python3 render_t6b.py frames_join $g $g 1 16 >> join.log 2>&1
echo "$g $J" >> join_values.log
