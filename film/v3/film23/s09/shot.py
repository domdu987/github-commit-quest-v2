#!/usr/bin/env python3
"""shot.py -- film 23 take s09: shot S09 (CAMP night), "count": crane from the tank rows down to the sound truck, push toward the horn.
Sound man flips switches, the record spins, guards act.  QA_ART_SET: the sound man's head must be <= y 760 in the last frame.

    python3 shot.py probe a:b[:s] | stills a:b[:s] out [scale] [samples] | final a:b[:s] [scale] [samples]     (a:b = film frames g, 'all')
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c23 as C                                                          # noqa: E402
from c23 import GH, cast23, lerp, sm, seg                                # noqa: E402
S = cast23.STORY23

LOOK_END_Z = 1.9
SOUND_SHIFT = (0.0, 0.0)          # world nudge of the sound man mark (QA: head centre y <= 760 on the last frame)


class T(C.Take):
    SID = "S09"
    D_IN = 15                      # dissolve 15 in
    HERE_DIR = HERE

    def tweak(self):
        # QA_ART_SET S09: end the push higher in the frame so the sound man's head sits at y <= 760 (look-at lowered = subject up)
        sh = C.SH.SHOTS["S09"]
        k = sh["move"]["path"]
        C0 = k[0][1]; C1 = k[1][1]; C2 = k[2][1]
        k[2] = (k[2][0], dict(C2, loc=(3.0, -24.0, 4.0), look_at=(-6.6, -9.8, LOOK_END_Z)))
        k[1] = (k[1][0], dict(C1, look_at=(C1["look_at"][0], C1["look_at"][1], 2.6)))

    def __init__(self, quality="preview"):
        C.Take.__init__(self, quality, work=os.path.join(HERE, "work"))
        m = self.marks
        sx, sy, sz, syaw, _ = m["soundman"][0]
        self.sound_pos = (sx + SOUND_SHIFT[0], sy + SOUND_SHIFT[1], sz)
        self.g1, self.g1r = self.clk["g1"], self.clk["g1_render"]
        self.snd = self.add("snd", "gi_sound")
        self.gd = [self.add("gd0", "gi_designer"), self.add("gd1", "gi_pump")]
        self.gpos = [(m["guard"][0][0], m["guard"][0][1], m["guard"][0][2]), (m["guard"][1][0], m["guard"][1][1], m["guard"][1][2])]
        self.shadow_all()

    # ---------------------------------------------------------------- poses
    def pose_snd(self, g):
        i = g - self.clk["g0"]
        p = dict(S["gi_sound_switches"][1])
        # flips switches on the desk: right arm taps left/right alternately, left hand rests; lean follows
        ph = (i % 36) / 36.0
        k = 0.5 + 0.5 * math.sin(2 * math.pi * ph)
        p["arm_r"] = dict(hand=(lerp(0.80, 1.05, k), lerp(0.55, 0.28, k)), bend=-0.2, stretch=1.25, shape="point")
        p["lean"] = 6 + 2.5 * math.sin(2 * math.pi * ph)
        p["head_roll"] = 2.0 * math.sin(i * 0.11)
        p["blink"] = cast23.blink_at(i, 84, 11)
        p["t"] = i / 30.0
        p.update(C.tint_for(self.light))
        return p

    def pose_guard(self, k, g):
        i = g - self.clk["g0"]
        name, pose = ("gi_stand_designer", "gi_stand_designer") if k == 0 else ("gi_carry_pump", "gi_carry_pump")
        p = dict(S[pose][1])
        p["blink"] = cast23.blink_at(i, 100 + 13 * k, 7 + 31 * k)
        p["head_roll"] = 1.0 * math.sin(i * 0.09 + k)
        p["lean"] = p.get("lean", 0) + 0.8 * math.sin(i * 0.15 + 2 * k)
        p["t"] = i / 30.0
        p.update(C.tint_for(self.light))
        return p

    # ---------------------------------------------------------------- staging
    def staging(self, gs):
        fs = [self.f_of(g) for g in gs]
        for g in gs:
            f = self.f_of(g)
            i = g - self.clk["g0"]
            GH.flicker(f)
            GH.set_record(198.0 * i / 30.0, frame=f)                  # 33 rpm: 6.6 deg per frame
            C.place(self.snd, f, self.sound_pos)
            for k, a in enumerate(self.gd):
                C.place(a, f, self.gpos[k])
        for g in gs:
            f = self.f_of(g)
            self.scene.frame_set(f)
            self.snd.pose(f, self.pose_snd(g), camera=self.cam)
            for k, a in enumerate(self.gd):
                a.pose(f, self.pose_guard(k, g), camera=self.cam)
        self.sprites_for([(self.snd, 256), (self.gd[0], 256), (self.gd[1], 256)], fs)

    def report(self, g):
        f = self.f_of(g)
        c = self.cam
        self.scene.frame_set(f)
        return dict(g=g, f=f, cam=[round(v, 3) for v in c.location], heads=C.head_report(self, f))


if __name__ == "__main__":
    C.run(T)
