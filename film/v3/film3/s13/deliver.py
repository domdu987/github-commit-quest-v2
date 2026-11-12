#!/usr/bin/env python3
"""deliver.py -- s13: raw/s13 + raw/s14 -> frames/ (g 1123..1336, dissolve 13 -> 14 mixed g 1225..1234), take.mkv, meta.json,
cues.json, contact.jpg; then QA numbers.  python3 deliver.py [qa]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3

G13, G14, G15, HIN, HOUT, D = 1131, 1230, 1330, 8, 7, 10
M0 = G14 - D // 2                         # 1225
meta = {"shots": [13, 14], "g0": G13, "g1": G15, "handle_in": HIN, "handle_out": HOUT,
        "transition_in": {"type": "dissolve", "frames": 12, "note": "in-handle g 1123..1130 rendered in 3D"},
        "transition_out": {"type": "dissolve", "frames": 10, "note": "out-handle g 1330..1336 rendered in 3D"},
        "internal": [{"at": G14, "type": "dissolve", "frames": D, "mixed": [M0, M0 + D - 1], "from_shot": 13, "to_shot": 14,
                      "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 13 to g 1236, shot 14 from g 1223 (raw/)"}],
        "shot_ranges": {"13": [G13, G14 - 1], "14": [G14, G15 - 1]}, "set": "v3/set3d3/harbor.py", "light": "WARM",
        "state": "paint 1, seep 0.8, bucket back under the drip (fill 0.45); snow heaps sink x0.95 -> x0.35, five kerb mounds melt, wet patches grow"}
drips = [g for g in range(G14 - 7, G15 + HOUT) if (g - 5) % 20 == 19]
cues = [(G13 - HIN, G14, "warm morning: birdsong, gulls, harbour water lapping, distant ship horn (soft)", "ambience"),
        (G13 - 6, G13 + 6, "dissolve in from shot 12", "dissolve"),
        (G13, G14, "meltwater trickling and dripping from eaves and kerb heaps", "water"),
        (1160, G14, "two dock workers in shirt sleeves walking toward the camera (footsteps on wet cobbles)", "footsteps"),
        (1150, G14, "kids playing by the kerb (laughter)", "voices"),
        (M0, M0 + D, "dissolve to shot 14 (tank foot)", "dissolve"),
        (G14 - 7, G15 + HOUT, "close to the tank: low steel hum, birds further away", "ambience"),
        (1245, 1300, "low groan of the tank (steel creak, long)", "groan"),
        (1300, G15 + HOUT, "second, lower groan building", "groan")]
for g in drips:
    cues.append((g, g, "drip: molasses drop plinks into the tin bucket", "drip", {"impact_frame": g}))
cues.append((G15 - 5, G15 + 5, "dissolve out to shot 15", "dissolve"))
lib3.deliver("s13", [("raw", 13, G13 - HIN, M0 - 1), ("mix", 13, 14, M0, D), ("raw", 14, M0 + D, G15 + HOUT - 1)], meta, cues)
if len(sys.argv) > 1:
    lib3.qa({13: (G13, G14 - 1), 14: (G14, G15 - 1)}, main={14: "tommy"})
