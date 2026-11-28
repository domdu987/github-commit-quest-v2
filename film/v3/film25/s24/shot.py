#!/usr/bin/env python3
"""s24 -- row 24 "โห่เชียร์ไปทั้งเมืองเลย!" (g 712-759), TRIAL, Look A.  Back to reality: general25 wags his finger (finger_wag, lip-sync, his quote ends g 760), staff officers (two
Tommies, tommy_a25 mirrored / tommy_d25) snigger behind him, hands over mouths.  PUSH 12 % + slight ARC.  Plate wall behind the staff.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D, gshot as GS
from mathutils import Vector
C, F, cast25 = D.C, D.F, D.C.cast25
G0, G1 = 712, 760


class Take(GS.GeneralClose):
    G0, G1 = G0, G1
    WALL_AZ = 14.0
    ND = 3.2
    WALL_W = 16.0

    def __init__(self, work):
        GS.GeneralClose.__init__(self, work)
        self.s1 = self.actor("s1", "tommy_a25", contact=dict(width=1.4, depth=0.7, opacity=0.6))
        self.s2 = self.actor("s2", "tommy_d25", contact=dict(width=1.4, depth=0.7, opacity=0.6))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        d = 4.7 / (1.0 + 0.12 * w)
        return D.orbit(self.P, self.f0 + 6.0 + 8.0 * w, d, 1.6, 2.15, side=0.15 * w, lx=-0.05), 40.0

    def pose_of(self, g):
        p = D.story("general25_finger_wag")
        p["mouth"] = D.talk(g)
        k = g - G0
        wag = math.sin(k * 2 * math.pi / 7.0)                              # the finger wags
        h = list(p["arm_r"]["hand"]); h[0] = round(h[0] + 0.05 * wag, 3); h[1] = round(h[1] - 0.04 * abs(wag), 3); p["arm_r"] = dict(p["arm_r"], hand=h)
        p["head_roll"] = round(-6 + 4 * math.sin(k * 0.45), 2); p["yaw"] = round(0.25 + 0.08 * math.sin(k * 0.3), 3)
        sq = D.squash_accent(g, 728)
        if sq: p["squash"] = sq
        p["blink"] = D.blink(g, [722, 741])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def staff_pose(self, name, g, off):
        k = g - G0
        p = D.story("tommy_a25_laugh_point" if name == "tommy_a25" else "tommy_d25_laugh_point")
        p["t"] = (k / 8.0 + off) % 1.0
        sq = (0.97 + 0.03 * math.sin(k * 1.3 + off * 7), 1.0 - 0.03 * math.sin(k * 1.3 + off * 7))
        p["squash"] = [round(sq[0], 3), round(sq[1], 3)]
        p["head_roll"] = round(6 * math.sin(k * 0.8 + off * 5), 2)
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        rt = Vector((math.sin(math.radians(self.f0 + 6.0)), -math.cos(math.radians(self.f0 + 6.0)), 0.0))     # camera-right at the mid azimuth
        back = Vector((-math.cos(math.radians(self.f0 + 6.0)), -math.sin(math.radians(self.f0 + 6.0)), 0.0))
        for g in gs:
            cam, lens = self.cam_of(g)
            a = self.P + back * 1.2 + rt * 1.45; a.z = F.gh(a.x, a.y)
            b = self.P + back * 1.7 - rt * 1.5; b.z = F.gh(b.x, b.y)
            self.key_frame(g, cam, lens, dict(gen=dict(feet=self.P, pose=self.pose_of(g)), s1=dict(feet=a, pose=self.staff_pose("tommy_a25", g, 0.0), flip=True),
                                              s2=dict(feet=b, pose=self.staff_pose("tommy_d25", g, 0.5))), focus=self.P + Vector((0, 0, 2.7)))
        self.pose_frames(gs)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
