#!/usr/bin/env python3
"""s22 -- row 22 "ถ้ามันข้าม สนามเพลาะได้จริง" (g 626-675), TRIAL trial_close_general, Look A.  M: over the general's shoulder, behind the tank's nose: the stick jabs toward the test trench on
"สนามเพลาะ" and then he looks back at us; lip-sync.  Camera: over-the-shoulder PUSH 8 % with a slight lateral slide; the tank hull (grey-olive plain, stencil off) is the near backdrop
behind him, his cast shadow falls on it.   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D
C, F, cast25, bpy = D.C, D.F, D.C.cast25, D.bpy
from mathutils import Vector
import tank25 as TK
G0, G1 = 626, 676
G22 = (-7.6, -31.6)


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, "trial_close_general", work, fstop=2.2, sun_e=12.0, sky_k=1.2, sun_left=30.0, sun_el=26.0)
        TK.set_stencil(F.S["tank"], 0)
        self.gen = self.actor("gen", "general25", contact=dict(width=1.6, depth=0.8, opacity=0.7))
        self.P = Vector((G22[0], G22[1], F.gh(*G22)))

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        az, d, cz, lz = 304.0, 3.9 / (1.0 + 0.08 * w), 2.6, 2.1
        A = math.radians(az)
        loc = Vector((self.P.x + math.cos(A) * d, self.P.y + math.sin(A) * d, self.P.z + cz))
        fwd = Vector((-math.cos(A), -math.sin(A), 0.0)); right = fwd.cross(Vector((0, 0, 1))).normalized()
        la = math.radians(az + 180.0 - 11.0)
        look = Vector((loc.x + 10 * math.cos(la), loc.y + 10 * math.sin(la), self.P.z + lz))
        side = -0.25 * w
        return (loc + right * side, look + right * side), 24.0

    def pose_of(self, g):
        p = D.story("general25_point_stick")
        p["mouth"] = D.talk(g)
        w = C.smooth((g - 656) / 7.0)
        p["yaw"] = round(0.95 - 0.55 * w, 3); p["head_roll"] = round(4 - 10 * w, 2); p["gaze"] = [round(0.9 - 0.8 * w, 2), 0.05]
        jab = math.exp(-((g - 646) / 3.5) ** 2)
        p["arm_r"]["stretch"] = round(1.3 + 0.15 * jab, 3)
        p["arm_r"]["hand"] = [0.95, round(0.12 - 0.12 * jab, 3)]
        p["prop_r"]["angle"] = round(-10 - 8 * jab + 3 * math.sin((g - G0) * 0.45), 2)
        p["expr"] = "smug" if g < 657 else "smirk"
        p["lean"] = round(1.5 * math.sin((g - G0) * 0.25), 2)
        p["blink"] = D.blink(g, [655, 640])
        p["light25"] = -1; p["rim25"] = 0.6
        return p

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, dict(gen=dict(feet=self.P, pose=self.pose_of(g))), focus=self.P + Vector((0, 0, 2.5)))
        self.pose_frames(gs)


if __name__ == "__main__":
    D.cli(Take, G0, G1)
