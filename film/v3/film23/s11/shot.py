#!/usr/bin/env python3
"""shot.py -- film 23 take s11: shot S11 (LANE day), "bikes": side tracking with two cyclists along the hedgerow (low hedge in the foreground), baguette in the
basket; they pedal and chat (held mouth drawings).  Dissolve 13 in (in-handle 9).

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples] | ground all
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402

SPEED = 4.0            # D/s (plan: they ride 4 D/s)
LENS = 34.0
LEAD = 1.7             # cyclist a is this far (D) right of the camera look-at at the middle of the planned move


class T(C.Take):
    SID = "S11"
    D_IN = 13
    HERE_DIR = HERE

    def tweak(self):
        # tighter (lens 24 -> 34), the camera stays behind the low hedge: the cyclists read medium (head ~80 px) instead of tiny at the left edge
        sh = C.SH.SHOTS["S11"]
        sh["cam"] = dict(sh["cam"], lens=LENS)
        sh["move"] = dict(end=dict(sh["move"]["end"], lens=LENS))

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        self.pa = m["cyclist_a"][0][:3]
        self.pb = m["cyclist_b"][0][:3]
        W = cast23.CANVAS23_WIDE
        self.a = self.add("cya", "fr_beret", W["fr_beret"])
        self.b = self.add("cyb", "fr_cap", W["fr_cap"])
        self.shadow_all()

    def ypos(self, g):
        """cyclists ride at SPEED, centred on the camera look-at at the middle of the planned move"""
        i_mid = (self.clk["g1"] - self.clk["g0"]) / 2.0
        return -74.8 + LEAD + SPEED * ((g - self.clk["g0"]) - i_mid) / 30.0

    def gz(self, x, y):
        z = GH.ground_z(x, y)
        return 0.0 if z is None else z

    def pose_a(self, g):
        i = g - self.clk["g0"]
        p = cast23.ride_frame("fr_beret", i / 14.0, facing=1, expr="happy", mouth="talk_a", basket=True, look=0.3)    # held chatty mouth (not a quote)
        p["blink"] = cast23.blink_at(i, 88, 9)
        p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(i * 0.17)
        return p

    def pose_b(self, g):
        i = g - self.clk["g0"]
        p = cast23.ride_frame("fr_cap", i / 14.0 + 0.35, facing=1, expr="happy", mouth="smile", look=0.3)
        p["blink"] = cast23.blink_at(i, 94, 41)
        p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(i * 0.15 + 1.0)
        return p

    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        for g in gs:
            f = self.f_of(g); dy = self.ypos(g)
            xa, ya = self.pa[0], dy + self.origin.y
            xb, yb = self.pb[0], dy - 3.4 + self.origin.y
            C.place(self.a, f, (xa, ya, self.gz(xa, ya)))
            C.place(self.b, f, (xb, yb, self.gz(xb, yb)))
        for g in gs:
            f = self.f_of(g)
            self.scene.frame_set(f)
            self.a.pose(f, self.pose_a(g), camera=self.cam, upper_k=1.0)
            self.b.pose(f, self.pose_b(g), camera=self.cam, upper_k=1.0)
        self.sprites_for([(self.a, 256), (self.b, 256)], fs)

    def report(self, g):
        f = self.f_of(g)
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in self.cam.location], heads=C.head_report(self, f))


if __name__ == "__main__":
    C.run(T)
