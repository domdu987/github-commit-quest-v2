#!/usr/bin/env python3
"""deliver.py -- take s13: frames, meta, cues, contact, compare, take.mkv, work/qa.txt.  python3 deliver.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s12")); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import shot as S
from deliver_lib import deliver
cues = [(1196, 1373, "tunnel room tone; footsteps on coal and ballast build to a run", "ambience", {}),
        (1204, 1204, "hard cut: alfie at the nail", "cut", {}),
        (1205, 1212, "alfie snatches the cage off the nail: wire jangle, nail scrape", "prop", dict(peak_frame=S.G_GRAB)),
        (1226, 1373, "running boots on coal, the cage rattling at each stride", "foley", {}),
        (1246, 1246, "cut: low, they run at the camera; miner1 dragged by the hand (grunt-free)", "cut", {}),
        (1288, 1288, "cut: miner3 mocking", "cut", {}),
        (S.G_Q[0], S.G_Q[1], "miner3 mocks: 'ไอ้เด็กเลี้ยงนก ตื่นตูมอีกแล้ว' (mouth moving, narration line)", "dialogue", {}),
        (1330, 1330, "cut: high wide, they pass the gaffer who stays under his hanging lamp", "cut", {})]
deliver(HERE, "s13", 13, S.SUBS, S.G0, S.G1, S.H, S.H, cues, [("13a", 1215, 79), ("13c", 1315, 77), ("13d", 1350, 81)],
        {"type": "cut", "frames": 0, "note": "in-handle g 1196..1203 rendered in 3D"},
        {"set": "v3/set3d5/mine.py tunnel LAMP; nail + 3D cage lowered 0.55 D at runtime (shot.setup); 3D cage hidden from g 1208 (held = cast 2D cage); gas 1.6",
         "cast": "v3/cast5 alfie (prop_r cage, bird fallen, eyes closed), miner1-3, gaffer (arms crossed, no lamp in hand: his lamp hangs on its chain)",
         "mouths": "miner3 only, g %d..%d" % S.G_Q, "light": "LAMP + alfie's keyed belt lamp"})
