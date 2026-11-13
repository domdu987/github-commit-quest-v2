#!/usr/bin/env python3
"""deliver.py -- take s14: frames, meta, cues, contact, compare, take.mkv, work/qa.txt.  python3 deliver.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s12")); sys.path.insert(0, HERE)
sys.argv = [sys.argv[0]]
import shot as S
from deliver_lib import deliver
cues = [(1357, 1405, "close lamp: the flame hisses louder and climbs, turning blue (firedamp)", "lamp", {}),
        (1365, 1365, "cut: the lamp", "cut", {}),
        (1405, 1405, "cut: low under the lamp, the gaffer looks up", "cut", {}),
        (S.G_IGN, S.G_IGN + 14, "the gas ignites: deep WHUMP, orange flash", "impact", dict(peak_frame=S.G_IGN + 2)),
        (1426, 1441, "the gaffer runs: boots", "foley", {}),
        (1441, 1441, "cut: from the pit bottom down the roadway", "cut", {}),
        (1441, 1510, "fireball roar rushing closer, timbers crack, debris rattle, running boots", "fx", {}),
        (S.G_BOOM, S.G_BOOM + 6, "explosion accent on 'ระเบิด'", "impact", dict(peak_frame=S.G_BOOM)),
        (1476, 1476, "cut: low and close, the runners ahead of the fire", "cut", {})]
deliver(HERE, "s14", 14, S.SUBS, S.G0, S.G1, S.H, S.H, cues, [("14a", 1398, 93), ("14b", 1424, 95), ("14d", 1500, 97)],
        {"type": "cut", "frames": 0, "note": "in-handle g 1357..1364 rendered in 3D"},
        {"set": "v3/set3d5/mine.py tunnel LAMP; set_flame 1 -> 2 (burst 3.2 at ignition) + insert-flame emission keyed warm -> pale blue at runtime; set_blast 0.35 -> 0.66 (14c-14d); gas 2.4 (14a-b)",
         "cast": "v3/cast5 gaffer (shocked, run), alfie (held cage, bird inside, eyes closed), miner1-3 (run)",
         "no_casualties": "every runner (gaffer last) stays outbye of the fire front in every frame", "light": "LAMP + ignition flash lamp_ign + alfie's belt lamp + blast lights"})
