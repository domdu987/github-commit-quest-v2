#!/usr/bin/env python3
"""s19 -- row 19 "แล้วหัวเราะลั่น" (g 522-551), TRIAL trial_close_general, Look A.  general25 waist-up belly laugh: laugh / laugh_b every 3-4 frames with a lerp_pose in-between
on each swap, head rolling, medals jiggling by the bounce, winds down into a smug look.  PUNCH 20 % over g 522-529, then a slow drift.  Tight crop (head about 0.45 W),
grey-olive plate 2 D behind him (cast shadow), sky above, mild DOF.   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D, gshot as GS
C, cast25 = D.C, D.C.cast25
G0, G1 = 522, 552
SEQ = [3, 4, 3, 3, 4, 3, 4, 3, 3]


def laugh_frame(g):
    k, i, use_b = g - G0, 0, False
    while k >= SEQ[i % len(SEQ)]:
        k -= SEQ[i % len(SEQ)]; i += 1; use_b = not use_b
    return use_b, i, k


class Take(GS.GeneralClose):
    G0, G1 = G0, G1
    WALL_AZ = 10.0

    def cam_of(self, g):
        k = C.out_cubic((g - G0) / 7.0)
        d = 5.0 / (1.0 + 0.20 * k)
        w = C.calm((g - 529) / float(G1 - 1 - 529))
        d = d / (1.0 + 0.04 * w)
        return D.orbit(self.P, self.f0 + 10.0, d, 1.55, 2.12 + 0.04 * w, side=0.35 * w, lx=0.0), 40.0

    def pose_of(self, g):
        use_b, i, k = laugh_frame(g)
        pa = D.story("general25_laugh_b" if use_b else "general25_laugh"); pb = D.story("general25_laugh" if use_b else "general25_laugh_b")
        p = pa
        if k == 0 and g > G0:                                              # in-between on every swap: halfway from the previous pose
            p = D.lerp_poses(pb, pa, 0.5)
        p.pop("mouth", None)
        u = (g - G0) / 29.0
        p["yaw"] = round(0.25 - 0.2 * u + 0.05 * math.sin(i * 1.7), 3)
        p["head_roll"] = p.get("head_roll", 0) + (4 if i % 3 == 0 else -2)
        p["lean"] = p.get("lean", 0) - 3.0 * math.sin(math.pi * u)
        p["t"] = (g - G0) / 9.0 % 1.0
        sq = D.squash_accent(g, G0 + sum(SEQ[:i])) if False else None
        if g >= 545:
            p["pitch"] = -0.45
        p["light25"] = -1; p["rim25"] = 0.6
        return p


if __name__ == "__main__":
    D.cli(Take, G0, G1)
