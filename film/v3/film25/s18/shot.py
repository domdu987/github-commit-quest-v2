#!/usr/bin/env python3
"""s18 -- row 18 "ท่านนายพล มาดูทดสอบ" (g 485-521), TRIAL trial_wide, Look A.  W: the green trial park; the general marches in (walk cycle, stick under his arm) with two staff officers
(tommy_a25 / tommy_d25 as stand-in staff) a step behind; the Mark I stands by the test trench.  FOLLOW: the camera pans with them, leading (about 22 % of the width per second).
A wide: no DOF, no backdrop.   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F, cast25 = D.C, D.F, D.C.cast25
from mathutils import Vector
G0, G1 = 485, 522
V = 0.085


class Take(D.Rig):
    SHADE = False
    SCALE, SAMPLES = 0.7, 14                              # wides: characters are small, 14 adaptive samples + OIDN at 70 % are plenty

    def __init__(self, work):
        D.Rig.__init__(self, "trial_wide", work, fstop=None, sun_e=10.0, sky_k=1.2, sun_left=28.0, sun_el=34.0)
        self.gen = self.actor("gen", "general25", contact=dict(width=1.8, depth=0.8, opacity=0.7))
        self.s1 = self.actor("s1", "tommy_a25", contact=dict(width=1.4, depth=0.7, opacity=0.6))
        self.s2 = self.actor("s2", "tommy_d25", contact=dict(width=1.4, depth=0.7, opacity=0.6))

    def pos(self, g, dx, dy):
        x = -27.0 + V * (g - G0) + dx; y = -15.0 + dy
        return Vector((x, y, F.gh(x, y)))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        P = Vector((-27.0 + V * (g - G0) + 0.04 * (g - G0) + 0.7, -15.0, 0.0)); P.z = F.gh(P.x, P.y)
        return D.orbit(P, -78.0 + 8.0 * w, 13.5 - 2.0 * w, 2.0 - 0.2 * w, 2.4, side=0.0, lx=0.0), 26.0

    def walk(self, name, g, off, mouth="flat", extra=None):
        p = json.loads(json.dumps(cast25.cycle(name, (g - G0) / 28.0 + off, "walk"), default=list))
        p["mouth"] = mouth; p["light25"] = -1; p["rim25"] = 0.6
        if extra: p.update(extra)
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            per = dict(gen=dict(feet=self.pos(g, 0.0, 0.0), pose=self.walk("general25", g, 0.0, "flat", dict(expr="smug", pitch=-0.25))),
                       s1=dict(feet=self.pos(g, -2.6, 1.3), pose=self.walk("tommy_a25", g, 0.5)),
                       s2=dict(feet=self.pos(g, -3.9, -1.1), pose=self.walk("tommy_d25", g, 0.15)))
            self.key_frame(g, cam, lens, per)
        self.pose_frames(gs)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
