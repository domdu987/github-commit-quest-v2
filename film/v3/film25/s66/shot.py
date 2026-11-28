#!/usr/bin/env python3
"""s66 -- row 66 "มีแท็งก์คันหนึ่ง" (g 1932-1960), STREET street_high, Look A.  The pilot's view: high above the brick high street of Flers, one tank rolling up it (tracks scroll).
Slow descending tilt + PUSH 8 %.  A wide: no DOF, no backdrop, no characters.   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F = D.C, D.F
from mathutils import Vector
import tank25 as TK
G0, G1 = 1932, 1961
V = 0.14


class Take(D.Rig):
    SHADE = False
    SCALE, SAMPLES = 0.7, 14                              # wides: characters are small, 14 adaptive samples + OIDN at 70 % are plenty

    def __init__(self, work):
        D.Rig.__init__(self, "street_high", work, fstop=None, sun_e=9.0, sky_k=1.2, sun_left=26.0, sun_el=48.0)
        self.H = F.S["tank"]

    def ty(self, g):
        return 22.0 + V * (g - G0)

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        loc = Vector((5.0 - 0.8 * w, -8.0 + 5.0 * w, 34.0 - 7.0 * w))                       # descends and pushes in
        look = Vector((0.0, 26.0 + 2.0 * w, 1.0 + 1.5 * w))
        return (loc, look), 28.0 + 2.2 * w

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, {})
        self.pose_frames(gs)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        TK.pose_on_ground(self.H, 0.0, self.ty(f), 90.0)
        TK.set_drive(self.H, V * (f - G0) + 2.0)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
