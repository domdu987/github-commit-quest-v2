#!/usr/bin/env python3
"""s25 -- row 25 "ทหารทั้งค่าย" (g 760-784), TRIAL trial_camp, Look A.  W: the camp: rows of tents, six soldiers (four Tommies, two of them repeated far back with other poses / mirrored /
other size) laughing and pointing at the Mark I.  Lateral slide 25 %/s.  A wide: no DOF, no backdrop.   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F, cast25 = D.C, D.F, D.C.cast25
from mathutils import Vector
G0, G1 = 760, 785
# (name, member, pose, x, y, scale, flip, phase)
CAST = [("a", "tommy_a25", "laugh_point", -21.5, -19.0, 1.05, False, 0.0), ("b", "tommy_b25", "cheer", -24.5, -16.5, 1.0, True, 0.3), ("c", "tommy_c25", "laugh_point", -27.0, -19.5, 0.95, False, 0.6),
        ("d", "tommy_d25", "cheer", -30.0, -15.5, 1.0, True, 0.15), ("e", "tommy_a25", "stand", -33.0, -13.0, 0.9, True, 0.0), ("f", "tommy_c25", "cheer", -19.0, -14.0, 0.9, True, 0.45)]


class Take(D.Rig):
    SHADE = False
    SCALE, SAMPLES = 0.7, 14                              # wides: characters are small, 14 adaptive samples + OIDN at 70 % are plenty

    def __init__(self, work):
        D.Rig.__init__(self, "trial_camp", work, fstop=None, sun_e=10.0, sky_k=1.2, sun_left=28.0, sun_el=34.0)
        for n, m, *_ in CAST:
            self.actor(n, m, contact=dict(width=1.4, depth=0.7, opacity=0.6))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        loc = Vector((-17.0 - 6.0 * w, -29.0, 2.2)); look = Vector((-24.5 - 6.0 * w, -14.0, 3.0))
        return (loc, look), 24.0

    def pose(self, n, m, pn, g, ph):
        k = g - G0
        p = D.story(m + "_" + pn)
        if "t" in p or pn in ("laugh_point", "cheer"):
            p["t"] = ((k / 9.0) + ph) % 1.0
        if pn in ("laugh_point", "cheer"):
            s = math.sin(k * 0.9 + ph * 9)
            p["squash"] = [round(1.0 - 0.03 * s, 3), round(1.0 + 0.03 * s, 3)]
            p["head_roll"] = round(5 * math.sin(k * 0.6 + ph * 6), 2)
        p["blink"] = D.blink(g, [int(768 + ph * 10)])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            per = {}
            for n, m, pn, x, y, sc, fl, ph in CAST:
                per[n] = dict(feet=Vector((x, y, F.gh(x, y))), pose=self.pose(n, m, pn, g, ph), scale=sc, flip=fl)
            self.key_frame(g, cam, lens, per)
        self.pose_frames(gs)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
