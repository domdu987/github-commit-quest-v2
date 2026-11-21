#!/usr/bin/env python3
"""shot.py -- film 23 take s13: shot S13 (LANE day), "cover + QUOTE พวกเราอเมริกัน แข็งแรงมาก": medium two-shot in depth, quick push on the soldier's dry smile.
The tank is held overhead by the 4-man lift (the ONLY airborne tank; lift=1 all shot, flagged airborne).  The smiling GI lip-syncs the quote (talk cycle
over the quote window); every other mouth is a held drawing.  The cyclists brake and stop by the mid frame and stay framed (x 0.15-0.85, heads above
y 860); one 'falls' off his bike by sitting down dazed, unhurt.  Cut in (no in-handle).

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples] | ground all
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402
import bpy                                                               # noqa: E402
from mathutils import Vector                                             # noqa: E402
S = cast23.STORY23

QUOTE = (60, 134)         # shot-local frames of the quote window (est. timing: the last ~2.4 s of the 4.5 s)
FALL_I = 112              # the second cyclist sits down (on "แข็งแรงมาก")
V0, BRAKE_I = 2.6, 16     # cyclists roll up (D/s) and have stopped by BRAKE_I (before the mid frame)
CAM_SHIFT = (0.0, 0.0)    # tracking: shift of the start/end camera (world x, y) -- set after the probe


def lifter_casts(marks, cam0):
    order = sorted(range(4), key=lambda i: (Vector(marks[i][:2]) - Vector(cam0[:2])).length)
    names = {order[0]: "gi_smile", order[1]: "gi_driver", order[2]: "gi_pump", order[3]: "gi_designer"}
    return [names[i] for i in range(4)]


class T(C.Take):
    SID = "S13"
    D_IN = 0
    HERE_DIR = HERE

    def tweak(self):
        sh = C.SH.SHOTS["S13"]
        sh["cam"] = CAM0
        sh["move"] = dict(MOVE)
        cm = sh["marks"]
        cm["cyclist_a"] = [C.SH.M_(*MARK_A, ph="cyclist_a", pose="stand")] if hasattr(C.SH, "M_") else cm["cyclist_a"]

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        o = self.origin
        self.pa = (MARK_A[0] + o.x, MARK_A[1] + o.y, 0.0)
        self.pb = (MARK_B[0] + o.x, MARK_B[1] + o.y, 0.0)
        W = cast23.CANVAS23_WIDE
        self.a = self.add("cya", "fr_beret", W["fr_beret"])
        self.b = self.add("cyb", "fr_cap", W["fr_cap"])
        self.lm = m["lifters"]
        self.lc = lifter_casts([(x[0], x[1]) for x in self.lm], (CAM0["loc"][0] + o.x, CAM0["loc"][1] + o.y))
        self.L = [self.add("lf%d" % k, self.lc[k]) for k in range(4)]
        self.tank = bpy.data.objects["tank_lift"]
        self.smile = self.lc.index("gi_smile")
        self.shadow_all()

    # ------------------------------------------------------------ choreography
    def roll_d(self, i):
        T0 = BRAKE_I / 30.0
        s = i / 30.0
        return V0 * (T0 - s) ** 2 / (2 * T0) if s < T0 else 0.0

    def pose_a(self, g):
        i = g - self.clk["g0"]
        braking = i >= 4
        stare = i >= 20
        p = cast23.ride_frame("fr_beret", i / 14.0, facing=1, expr="stunned", mouth=("open", 0.14, 0.1) if stare else None, state="brake" if braking else "ride",
                              basket=True, look=0.8)
        if not stare:
            p.pop("mouth", None)
        p["blink"] = cast23.blink_at(i, 70, 19)
        p["fx"] = ["sweat"] if i > 40 else []
        p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(i * 0.2)
        p["t"] = i / 30.0
        return p

    def pose_b(self, g):
        i = g - self.clk["g0"]
        if i >= FALL_I:                                                       # sat on the grass, dazed, unhurt; the bike lies beside him
            p = cast23.fall_pose("fr_cap", (i - FALL_I) / 30.0, facing=1)
            p["blink"] = cast23.blink_at(i, 60, 3)
            return p
        wob = max(0.0, 1.0 - abs(i - (FALL_I - 4)) / 6.0)                    # a wobble leaning back just before he sits down
        braking = i >= 4
        p = cast23.ride_frame("fr_cap", i / 14.0 + 0.4, facing=1, expr="stunned", mouth=("open", 0.14, 0.1) if i >= 20 else None, state="brake" if braking else "ride", look=0.8)
        if i < 20:
            p.pop("mouth", None)
        p["lean"] = p.get("lean", 0) - 8.0 * wob
        p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(i * 0.17) - 6.0 * wob
        p["blink"] = cast23.blink_at(i, 76, 51)
        p["t"] = i / 30.0
        return p

    def pose_lift(self, k, g):
        i = g - self.clk["g0"]
        c = self.lc[k]
        p = cast23.lift_pose(c, i / 30.0 + 0.37 * k, lift_h=3.45, expr="determined", strain=1.0)
        if c == "gi_smile":
            q = S["gi_smile_lift_quote"][1]
            p = cast23.lift_pose(c, i / 30.0, lift_h=3.45, expr="grinning", strain=1.0)
            p["bigsweat23"] = 1
            if QUOTE[0] <= i <= QUOTE[1]:
                p["mouth"] = cast23.talk_mouth(g, 1.0)                        # synthetic loudness: 4-6 Hz pattern with pauses (cast6 talk_mouth)
            else:
                p["mouth"] = "grin"
        p["blink"] = cast23.blink_at(i, 100 + 9 * k, 17 * k)
        return p

    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        for g in gs:
            f = self.f_of(g); i = g - self.clk["g0"]
            GH.set_lift(1.0, frame=f)
            d = self.roll_d(i)
            C.place(self.a, f, (self.pa[0], self.pa[1] - d, C.gz(self.pa[0], self.pa[1] - d)))
            fallen = i >= FALL_I
            C.place(self.b, f, (self.pb[0], self.pb[1] - d, C.gz(self.pb[0], self.pb[1] - d)))
            for k, a in enumerate(self.L):
                C.place(a, f, self.lm[k][:3])
        for g in gs:
            f = self.f_of(g); i = g - self.clk["g0"]
            self.scene.frame_set(f)
            self.a.pose(f, self.pose_a(g), camera=self.cam, upper_k=1.0)
            pb = self.pose_b(g)
            self.b.pose(f, pb, camera=self.cam, upper_k=1.0)
            for k, a in enumerate(self.L):
                a.pose(f, self.pose_lift(k, g), camera=self.cam, upper_k=1.0)
        self.sprites_for([(self.a, 256), (self.b, 256)] + [(a, 256) for a in self.L], fs)

    def report(self, g):
        f = self.f_of(g)
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in self.cam.location], lens=round(self.cam.data.lens, 1), heads=C.head_report(self, f))


# camera: the planned S13 move (zoom_rate 0.08, slide 20) re-aimed so both cyclists stay framed
CAM0 = dict(loc=(-0.7, -45.0, 3.6), look_at=(-5.2, -31.5, -1.2), lens=24.0)
MOVE = dict(zoom_rate=0.10, slide=-6, sdist=12.0)
MARK_A = (-4.3, -36.2)
MARK_B = (-2.7, -37.6)

if __name__ == "__main__":
    C.run(T)
