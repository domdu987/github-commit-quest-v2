#!/usr/bin/env python3
"""s43 -- row 43 "นายพลหัวเราะ" (g 1301-1330), FRONT OP op_close_general, Look A.  general25 waist-up in the observation post: the field glasses sweep the battlefield (lift, scan), then
a laughing double-take: the glasses drop, the cap pops up (hat_up25), he bursts out laughing (laugh / laugh_b bounce, lerp in-betweens).  No lip-sync (his quote starts g 1331).
PUSH 12 %.  Plate wall 2 D behind him (sky above).   python3 shot.py probe|draft|final <gspec>   post: python3 ../s21/post_d.py . <gspec>"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "s21"))
import d25 as D, gshot as GS
C, cast25 = D.C, D.C.cast25
G0, G1 = 1301, 1331


class Take(GS.GeneralClose):
    PRESET = "op_close_general"
    HIDE = ("op_wood",)
    G0, G1 = G0, G1
    WALL_AZ = -14.0

    def cam_of(self, g):
        u = (g - G0) / float(G1 - 1 - G0); w = C.calm(u)
        d = 4.7 / (1.0 + 0.12 * w)
        return D.orbit(self.P, self.f0 - 14.0 + 7.0 * w, d, 1.6, 2.12, side=0.15 * w, lx=0.0), 40.0

    def pose_of(self, g):
        k = g - G0
        gl = D.story("general25_field_glasses"); lg = D.story("general25_laugh")
        if k < 13:                                              # scanning left to right with the glasses
            p = gl
            p["yaw"] = round(0.35 + 0.25 * math.sin(k * 0.45), 3); p["pitch"] = round(-0.1 + 0.05 * math.sin(k * 0.3), 3)
            p["lean"] = round(1.5 * math.sin(k * 0.45), 2)
        elif k < 17:                                            # double-take: glasses snap down, cap pops up
            u = (k - 13) / 4.0
            p = D.lerp_poses(gl, lg, C.smooth(u))
            p["hat_up25"] = round(0.9 * math.sin(math.pi * min(1.0, u * 1.1)), 3)
            p["expr"] = "shocked" if u < 0.6 else "laughing"
        else:
            use_b = ((k - 17) // 3) % 2 == 1
            p = D.story("general25_laugh_b" if use_b else "general25_laugh")
            if (k - 17) % 3 == 0 and k > 17:
                p = D.lerp_poses(D.story("general25_laugh" if use_b else "general25_laugh_b"), p, 0.5)
            p["yaw"] = round(0.3 + 0.06 * math.sin(k), 3)
        p["t"] = (k / 9.0) % 1.0
        p["mouth"] = p.get("mouth", "flat") if k >= 13 else "flat"
        p["blink"] = D.blink(g, [1308])
        p["light25"] = -1; p["rim25"] = 0.6
        return p


if __name__ == "__main__":
    D.cli(Take, G0, G1)
