#!/usr/bin/env python3
"""s26 -- row 26 "เลยเรียกมันว่า" (g 785-816), TRIAL camp_close_tank, Look A.  tommy_c25 taps the tank hull with a LADLE like a bucket, grinning (ladle_tap: laughing, tears): the ladle
swings back and strikes the plate every 8 frames with a squash on each strike.  The (plain) hull side is the near backdrop 0.6 D behind him, his shadow on it.  PUSH 10 %.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector
import tank25 as TK
G0, G1 = 785, 817
ND = 0.7


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, "camp_close_tank", work, fstop=2.0, sun_e=15.0, sky_k=1.3, sun_col=(1.0, 0.95, 0.88), ev=1.0)
        self.H = F.S["tank"]; TK.set_stencil(self.H, 0); D.flatten_hull(self.H, (0.34, 0.38, 0.17)); bpy.context.view_layer.update()
        mw = self.H.root.matrix_world
        m = F.S["mark"]; ml = mw.inverted() @ Vector(m["pos"]); sg = -1.0 if ml.y < 0 else 1.0
        n = mw.to_3x3() @ Vector((0, sg, 0)); self.nrm = math.degrees(math.atan2(n.y, n.x))
        self.feet = mw @ Vector((-8.2, sg * (2.02 + ND), 0.0)); self.feet.z = F.gh(self.feet.x, self.feet.y)
        self.tc = self.actor("tc", "tommy_c25", contact=dict(width=1.5, depth=0.7, opacity=0.6))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        d = 4.5 / (1.0 + 0.10 * w)
        return D.orbit(self.feet, self.nrm + 12.0 - 5.0 * w, d, 1.6, 1.85, side=0.2 * w, lx=0.35), 40.0

    def pose_of(self, g):
        k = g - G0
        p = D.story("tommy_c25_ladle_tap")
        ph = (k % 8) / 8.0                                           # tap cycle: wind up (0-0.5), strike at 0.5-0.6, rebound
        sw = math.sin(ph * 2 * math.pi)
        h = list(p["arm_r"]["hand"]); h[0] = round(h[0] + 0.10 * sw, 3); h[1] = round(h[1] - 0.14 * max(0, math.sin((ph + 0.15) * 2 * math.pi)), 3); p["arm_r"] = dict(p["arm_r"], hand=h)
        p["prop_r"] = dict(p["prop_r"], angle=round(-10 + 22 * sw, 2))
        if ph < 0.25 and k >= 4:
            p["squash"] = [1.04, 0.96]
        p["t"] = (k / 10.0) % 1.0                                    # the laughing tears loop
        p["head_roll"] = round(6 + 4 * math.sin(k * 0.7), 2)
        p["blink"] = D.blink(g, [795, 809])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, dict(tc=dict(feet=self.feet, pose=self.pose_of(g))), focus=self.feet + Vector((0, 0, 2.2)))
        self.pose_frames(gs)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
