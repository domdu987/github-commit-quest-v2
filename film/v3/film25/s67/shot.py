#!/usr/bin/env python3
"""s67 -- row 67 "เดินไปตามถนน กลางเมืองแฟลร์" (g 1961-2008), STREET street_wide, Look A.  Street level: the Mark I rolls up the brick street of Flers toward us (tracks scroll, tail
wheels turn), brick houses on both sides; the camera FOLLOWS it, backing away a little slower than the tank with a slow lateral drift.  A wide: no DOF, no backdrop.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F = D.C, D.F
from mathutils import Vector
import tank25 as TK
G0, G1 = 1961, 2009
V = -0.11                                                 # the tank rolls toward the camera (-y): D per frame
TY0 = 52.0                                                # tank front y at G0


class Take(D.Rig):
    SHADE = False
    SCALE, SAMPLES = 0.7, 14                              # wides: characters are small, 14 adaptive samples + OIDN at 70 % are plenty

    def __init__(self, work):
        D.Rig.__init__(self, "street_wide", work, fstop=None, sun_e=10.0, sky_k=1.3, sun_left=24.0, sun_el=40.0)
        self.H = F.S["tank"]

    def ty(self, g):
        return TY0 + V * (g - G0)

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        cy = 14.0 + 0.085 * (g - G0)                         # the camera backs away slower than the tank closes (it follows, leading the street)
        loc = Vector((3.2 - 3.0 * w, cy - 2.0, 1.35 + 0.3 * w))
        look = Vector((-0.4 + 1.0 * w, self.ty(g) - 10.0, 2.6))
        return (loc, look), 24.0

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, {})
        self.pose_frames(gs)

    def on_frame(self, f):
        D.Rig.on_frame(self, f)
        TK.pose_on_ground(self.H, 0.0, self.ty(f), 270.0)
        TK.set_drive(self.H, abs(V) * (f - G0) + 2.0)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
