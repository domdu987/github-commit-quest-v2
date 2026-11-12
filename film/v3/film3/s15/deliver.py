#!/usr/bin/env python3
"""deliver.py -- s15: raw/s15 -> frames/ (g 1323..1468), take.mkv, meta.json, cues.json, contact.jpg; then QA numbers.
python3 deliver.py [qa]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3

G0, G1, H_ = 1330, 1462, 7
meta = {"shots": [15], "g0": G0, "g1": G1, "handle_in": H_, "handle_out": H_,
        "transition_in": {"type": "dissolve", "frames": 10, "note": "in-handle g 1323..1329 rendered in 3D"},
        "transition_out": {"type": "dissolve", "frames": 10, "note": "out-handle g 1462..1468 rendered in 3D"},
        "shot_ranges": {"15": [G0, G1 - 1]}, "set": "v3/set3d3/harbor.py", "light": "WARM",
        "camera": "custom elevated three-quarter view of the whole tank from the yard end of Commercial Street (plan: high_down / insert)",
        "events": {"xray_in": [1328, 1342], "water_rises": [1340, 1384], "water_fades": [1398, 1410], "pour_starts": 1404, "molasses_rises": [1408, 1468]}}
cues = [(G0 - H_, G1 + H_, "warm morning ambience, muted (diagram moment)", "ambience"),
        (G0 - 5, G0 + 5, "dissolve in from shot 14", "dissolve"),
        (1328, 1342, "the tank turns x-ray: soft shimmer / glassy whoosh", "diagram"),
        (1340, 1384, "clean water rushing in, the level rising (pitch rising)", "pour_water"),
        (1384, 1398, "water settles, small slosh (test: no leaks)", "water"),
        (1398, 1410, "the blue ghost drains away (reverse shimmer)", "diagram"),
        (1404, G1 + H_, "thick molasses pouring from the pipe at the rim (heavy glugging pour, low)", "pour"),
        (G1 - 5, G1 + 5, "dissolve out to shot 16", "dissolve")]
lib3.deliver("s15", [("raw", 15, G0 - H_, G1 + H_ - 1)], meta, cues)
if len(sys.argv) > 1:
    lib3.qa({15: (G0, G1 - 1)}, extra_rows=[("ref b t0010 t0030 (exteriors)", [os.path.join(lib3.PROJ, "ref", "b", "t%04d.jpg" % t) for t in (10, 30)])])
