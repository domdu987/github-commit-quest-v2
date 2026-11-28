#!/usr/bin/env python3
"""s20 -- row 20 "ถังน้ำเหล็ก จะไปรบเนี่ยนะ!" (g 552-601), TRIAL, Look A.  general25 point_stick at the tank, lip-sync (his quote, g 552-760); eased PUSH 10 % + a slight arc.
Beats: head to the tank + a stick jab on "ถังน้ำเหล็ก", turns to us scoffing on "จะไปรบเนี่ยนะ!", a squash accent on "นะ!", stick wag.  Plate wall 2 D behind him.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D, gshot as GS
C, cast25 = D.C, D.C.cast25
G0, G1 = 552, 602


class Take(GS.GeneralClose):
    G0, G1 = G0, G1
    WALL_AZ = -28.0
    WALL_W = 9.0

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        d = 4.5 / (1.0 + 0.10 * w)
        return D.orbit(self.P, self.f0 - 38.0 + 6.0 * w, d, 1.7 + 0.08 * w, 2.10, side=-0.2 * w, lx=0.30), 40.0

    def pose_of(self, g):
        p = D.story("general25_point_stick")
        p["mouth"] = D.talk(g)
        if g < 574:
            p["yaw"] = 0.55; p["head_roll"] = 9; p["gaze"] = [0.7, -0.1]
            jab = math.exp(-((g - 558) / 3.0) ** 2)
            p["arm_r"]["stretch"] = round(1.3 + 0.12 * jab, 3)
            p["prop_r"]["angle"] = round(8 - 10 * jab, 2)
            p["lean"] = 2.0 * math.sin((g - G0) * 0.3)
        else:
            w = C.smooth((g - 574) / 6.0)
            p["yaw"] = round(0.55 - 0.40 * w, 3); p["head_roll"] = round(9 - 15 * w, 2); p["gaze"] = [round(0.7 - 0.7 * w, 2), 0.0]
            p["expr"] = "smirk" if g >= 576 else "smug"
            p["prop_r"]["angle"] = round(6 + 12 * math.sin((g - 576) * 2 * math.pi / 10.0), 2)
            p["lean"] = -5.0 * w
            sq = D.squash_accent(g, 594)
            if sq: p["squash"] = sq
        p["blink"] = D.blink(g, [565, 574, 590])
        p["light25"] = -1; p["rim25"] = 0.6
        return p


if __name__ == "__main__":
    D.cli(Take, G0, G1)
