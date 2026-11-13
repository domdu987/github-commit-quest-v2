#!/usr/bin/env python3
"""deliver.py -- take s12: frames, meta, cues, contact, compare, take.mkv, work/qa.txt.  python3 deliver.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import shot as S
from deliver_lib import deliver
cues = [(1085, 1212, "deep tunnel room tone, quieter than before; a faint airy hiss (the gas)", "ambience", {}),
        (1093, 1093, "dissolve / cut: next day, the cage on its nail", "cut", {}),
        (1132, 1132, "cut: closer, inbye side", "cut", {}),
        (S.G_NOTE, S.G_NOTE + 14, "the canary sings ONE thin note (one floating note), then silence", "bird_song", dict(notes=1, peak_frame=S.G_NOTE)),
        (S.G_NOTE + 14, S.G_NOTE + 26, "soft feather ruffle as it droops; eyes close", "foley", {}),
        (1168, 1168, "cut: low, level with the cage floor", "cut", {}),
        (S.G_FALL[0], S.G_FALL[1], "the bird tips off the perch and drops to the cage floor: tiny soft thump, faint wire ring", "foley", dict(peak_frame=S.G_FALL[1])),
        (S.G_FALL[1], 1212, "silence over the still bird (low sad drone)", "accent", {})]
deliver(HERE, "s12", 12, S.SUBS, S.G0, S.G1, S.H, S.H, cues, [("12a", 1110, 41), ("12b", 1150, 41), ("12c", 1195, 41)],
        {"type": "dissolve_or_cut", "frames": 12, "note": "in-handle g 1085..1092 rendered in 3D (next day: a dissolve fits)"},
        {"set": "v3/set3d5/mine.py tunnel LAMP; the set's 3D cage on its nail, canary sprite (cast5 canary) at the perch = cage centre, inside the bars; gas 1.6 with keyed drift",
         "cast": "v3/cast5 canary (perch_quiet -> sing_one (1 note) -> droop -> fallen, eyes closed, never X eyes)", "light": "LAMP + keyed warm rim lamp behind the cage"})
