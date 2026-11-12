#!/usr/bin/env python3
"""deliver.py -- s11: raw/s11 -> frames/ (g 910..1007), take.mkv, meta.json, cues.json, contact.jpg; then QA numbers.
python3 deliver.py [qa]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib3
from lib3 import g_of

G0, G1, HIN = 918, 1008, 8
meta = {"shots": [11], "g0": G0, "g1": G1, "handle_in": HIN, "handle_out": 0,
        "transition_in": {"type": "dissolve", "frames": 12, "note": "in-handle g 910..917 rendered in 3D (shot 11 camera before its start)"},
        "transition_out": {"type": "cut", "frames": 0},
        "shot_ranges": {"11": [G0, G1 - 1]}, "set": "v3/set3d3/harbor.py", "light": "WINTER",
        "state": "paint 1 (brown), seep 0.7, snowfall (6500 flakes), kerb snow heaps settle (height x0.55 -> x1.15)"}
cues = [(G0 - HIN, G1, "winter wind over the rooftops, soft hush of falling snow (bed for the whole shot)", "ambience"),
        (G0 - 6, G0 + 6, "dissolve in from shot 10", "dissolve"),
        (G0, G1, "two workers trudging up the snowy street (muffled crunching footsteps, very far, optional)", "footsteps_far"),
        (g_of(31.662), g_of(31.662), "push speeds up slightly on 'thang ko yang' (no sound needed)", "camera"),
        (950, 1000, "kids playing far down the street (faint laughter, optional)", "voices_far"),
        (G1, G1, "hard cut to shot 12", "cut")]
lib3.deliver("s11", [("raw", 11, G0 - HIN, G1 - 1)], meta, cues)
if len(sys.argv) > 1:
    lib3.qa({11: (G0, G1 - 1)}, extra_rows=[("ref b t0010 t0030 (exteriors)", [os.path.join(lib3.PROJ, "ref", "b", "t%04d.jpg" % t) for t in (10, 30)])])
