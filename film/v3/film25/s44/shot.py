#!/usr/bin/env python3
"""s44 -- row 44 "เห็นไหม ไอ้ถังน้ำ" (g 1331-1367), FRONT OP op_close_general, Look A.  general25_glasses_laugh: lip-sync (his second quote g 1331-1396), the free hand pointing, glasses
in the other, laughing tears; squash accent on the stress; PUNCH 20 % on "ไอ้ถังน้ำ" (g 1347).  Plate wall 2 D behind him.
   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D, gshot as GS
C, cast25 = D.C, D.C.cast25
G0, G1 = 1331, 1368


class Take(GS.GeneralClose):
    PRESET = "op_close_general"
    G0, G1 = G0, G1
    WALL_AZ = 12.0

    def cam_of(self, g):
        k = C.out_cubic((g - 1347) / 7.0) if g >= 1347 else 0.0          # PUNCH 20 % over g 1347-1354
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        d = 5.0 / (1.0 + 0.04 * w) / (1.0 + 0.20 * k)
        return D.orbit(self.P, self.f0 + 12.0 - 6.0 * w, d, 1.6, 2.15, side=-0.1 * w, lx=0.0), 40.0

    def pose_of(self, g):
        k = g - G0
        p = D.story("general25_glasses_laugh")
        p["mouth"] = D.talk(g)
        p["t"] = (k / 8.0) % 1.0
        h = list(p["arm_r"]["hand"]); h[0] = round(h[0] + 0.06 * math.sin(k * 0.8), 3); h[1] = round(h[1] - 0.05 * abs(math.sin(k * 0.8)), 3); p["arm_r"] = dict(p["arm_r"], hand=h)   # the pointing hand jabs
        p["head_roll"] = round(-8 + 4 * math.sin(k * 0.5), 2)
        p["lean"] = round(-6 + 3 * math.sin(k * 0.6), 2)
        sq = D.squash_accent(g, 1347)
        if sq: p["squash"] = sq
        p["blink"] = D.blink(g, [1340, 1360])
        p["light25"] = -1; p["rim25"] = 0.6
        return p


if __name__ == "__main__":
    D.cli(Take, G0, G1)
