#!/usr/bin/env python3
"""shot.py -- film 3 take s13: shots 13 and 14 (the unusually warm morning), harbor set WARM.

    shot 13  g 1131..1229 (plan 37.70-41.00 s)  12-frame dissolve in from shot 12 (in-handle g 1123..1130 in 3D).
             street_wide -> street_low: a crane down Commercial Street in two eased segments (speed change on "อากาศอุ่น"
             g 1188).  Bright warm sun, the snow heaps sink and melt into wet glossy patches, two dock workers in shirt
             sleeves (no coats) walk down the street toward the camera, two kids play by the kerb; the brown tank gleams at
             the end of the street.
    shot 14  g 1230..1329 (plan 41.00-44.35 s)  10-frame dissolve 13 -> 14 mixed in this take (g 1225..1234; raw shot 13 to
             g 1236, shot 14 from g 1223).  Low angle at the tank foot (tank_low family, custom): tommy beside his bucket
             (back under the drip) looks up the towering riveted wall, worried; slow push and tilt up (two segments, speed change
             on "ถังใบนี้ไม่" g 1273).  Ladder, seep strips, rivet rows and the falling drip give the wall life; a barrel in
             shade at the lower right edge.  Out: 10-frame dissolve to shot 15 (out-handle g 1330..1336 in 3D).

    python3 shot.py probe 13|14 a:b:step | stills <shot> a:b:step <dir> [scale] [samples] | final <shot> [a:b] [scale] [samples]
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3 import *            # noqa: F401,F403

G13, G14, G15 = gb(37.70), gb(41.00), gb(44.35)     # 1131, 1230, 1330
H_IN = 12 // 2 + 2                                   # 8
D14 = 10; H14 = D14 // 2 + 2                          # internal dissolve, 7
H_OUT = 10 // 2 + 2                                   # 7
G_WARM = g_of(39.511)                                 # 1188 "อากาศอุ่น"
G_MECH = g_of(42.345)                                 # 1273 "ถังใบนี้ไม่"

# ---------------------------------------------------------------- shot 13
C13 = [(Vector((2.0, -62.0, 21.0)), Vector((9.0, 12.0, 6.0))),
       (Vector((1.8, -53.0, 8.0)), Vector((8.6, 14.0, 7.2))),
       (Vector((1.6, -41.0, 1.5)), Vector((8.4, 18.0, 8.0)))]
WALK13 = {"worker1": ((0.3, -25.5, 0.0), (0.5, -29.4, 0.0), 0.0), "worker2": ((1.9, -24.0, 0.0), (1.8, -27.8, 0.0), 2.1)}
KIDS13 = {"kid1": (3.7, -16.0, 0.0), "kid2": (2.6, -14.6, 0.0)}
PUDDLES13 = [(-1.5, -44.0, 0.0, 1.6, 0.9), (2.4, -40.5, 0.0, 1.2, 0.7), (0.4, -33.0, 0.0, 1.9, 0.9), (-3.0, -29.0, 0.0, 1.1, 0.6),
             (3.4, -23.0, 0.0, 1.4, 0.8), (-0.8, -18.0, 0.0, 1.7, 0.8), (1.0, -47.0, 0.0, 1.0, 0.5), (-3.6, -38.0, 0.0, 0.9, 0.5)]

MOUNDS13 = [(-4.45, -35.5, 0.0, 0.85), (4.5, -32.0, 0.0, 0.7), (-4.5, -28.5, 0.0, 0.6), (4.45, -37.8, 0.0, 0.9), (-6.6, -33.0, 0.15, 0.55)]

# ---------------------------------------------------------------- shot 14
TOMMY = Vector(H.HERO_MARK) + H.TAN(H.TH_B) * (-0.15) + H.OUT(H.TH_B) * 0.25
OUTV = H.OUT(H.TH_B)
TANV = H.TAN(H.TH_B)
T_HEAD = TOMMY + Vector((0, 0, 1.97))


def c14(dist, side, z, look_up, look_side):
    loc = TOMMY + OUTV * dist + TANV * side + Vector((0, 0, z - TOMMY.z))
    look = T_HEAD + TANV * look_side + Vector((0, 0, look_up)) - OUTV * 1.2
    return loc, look


C14 = [c14(5.0, -1.55, 0.75, 1.05, 0.55), c14(4.4, -1.35, 0.72, 0.95, 0.50), c14(3.85, -1.20, 0.70, 0.85, 0.45)]


class Take(BaseTake):
    PRESET = "WARM"
    SHOTS = {13: (G13 - H_IN, G14 + H14 - 1), 14: (G14 - H14, G15 + H_OUT - 1)}
    SEEP = 0.8
    BUCKET = dict(fill=0.45, visible=True)

    def setup(self):
        for n in ("worker1", "worker2", "kid1", "kid2", "tommy"):
            self.actor(n)
        self.puddles = Puddles(PUDDLES13, coll=self.fx)
        # melting snow mounds by the kerbs near the end of the crane (they sink and shrink through the shot)
        self.mounds = []
        for i, (x, y, z, r) in enumerate(MOUNDS13):
            mb = H.MB(); mb.sphere((0.0, 0.0, 0.0), 1.0, H.STATE["M"]["snow"], seg=16, rings=8)
            o = mb.obj("w3_mound_%d" % i, self.fx, hull=0.01); o.location = (x, y, z); o["r"] = r; T.no_bounce(o)
            self.mounds.append(o)
        self.drip = Drip(period=20, phase=5)
        sm = shade_mat("barrel_fg14", color="#5a3422", shade_mul=0.30)
        bm = H.MB(); c, lk = C14[0]
        f_, r_, u_ = cam_basis(c, lk); f_.z = 0; f_.normalize(); r_.z = 0
        p = c + f_ * 1.9 + r_ * 1.0
        bm.frustum((p.x, p.y, 0.0), (p.x, p.y, 0.6), 0.40, 0.46, sm, seg=18)
        bm.frustum((p.x, p.y, 0.6), (p.x, p.y, 1.2), 0.46, 0.40, sm, seg=18)
        self.barrel = bm.obj("w3_barrel14", self.fx, hull=0.012); self.barrel.visible_shadow = False

    def cam(self, shot, g):
        a, b = self.SHOTS[shot]
        k = lambda c: tuple(c[0]) + tuple(c[1])
        if shot == 13:
            ks = [(a, k(C13[0]), "sine"), (G_WARM, k(C13[1]), "cubic_out"), (b, k(C13[2]), "lin")]
            v = mkeys(g, ks, 0.25)
        else:
            ks = [(a, k(C14[0]), "sine"), (G_MECH, k(C14[1]), "sine"), (b, k(C14[2]), "lin")]
            v = mkeys(g, ks, 0.35)
        return Vector(v[:3]), Vector(v[3:])

    def cast_in(self, shot):
        return ["worker1", "worker2", "kid1", "kid2"] if shot == 13 else ["tommy"]

    def place(self, shot, n, g):
        if shot == 14:
            return TOMMY
        a, b = self.SHOTS[13]
        if n in WALK13:
            p0, p1, _ = WALK13[n]
            return Vector(p0).lerp(Vector(p1), (g - a) / float(b - a))
        return KIDS13[n]

    def pose(self, shot, n, g):
        if n in WALK13:
            legs, bob = walk_legs(g, WALK13[n][2], period=16, stride=0.8)
            happy = n == "worker1"
            return dict(yaw=-0.25 if happy else 0.3, pitch=-0.25, expr="happy" if happy else "smirk", head_roll=(5 if happy else -4) + 3 * bob,
                        legs=legs, arm_r=dict(hand=(0.42, 0.62 + 0.1 * bob), bend=-0.6), arm_l=dict(hand=(-0.40, 0.66), bend=0.6),
                        squash=(1.0, 1.0 - 0.02 * bob), blink=blink(g, [1150, 1201]))
        if n == "kid1":
            c, p = cast3.STORY3["kids_play"]; p = dict(p)
            ph = (g // 12) % 2
            p["arm_r"] = dict(hand=(0.40, -0.42 if ph else 0.15), bend=-0.8, shape="open", stretch=1.2)
            return p
        if n == "kid2":
            c, p = cast3.STORY3["kids_play_girl"]; p = dict(p); p["head_roll"] = 8 * math.sin(g * 0.22)
            return p
        # tommy: looks up the wall, worried; a swallow, slow breathing
        c, p = cast3.STORY3["tommy_worried"]; p = dict(p)
        p["pitch"] = -0.9; p["gaze"] = (0.45, -1.0); p["head_roll"] = -8 + 1.5 * math.sin(g * 0.18)
        p["yaw"] = 0.35
        br = math.sin(g * 0.21)
        p["squash"] = (1.0 + 0.01 * br, 1.0 - 0.012 * br)
        p["blink"] = blink(g, [1244, 1290, 1322])
        p["arm_r"] = dict(hand=(0.10, 0.80 - 0.03 * br), bend=0.8); p["arm_l"] = dict(hand=(-0.02, 0.84), bend=0.8)
        return p

    def ppd(self, shot, n):
        return 384 if shot == 14 else 128

    def visible(self, shot):
        for o in self.puddles.obs:
            o.hide_render = shot != 13
        self.barrel.hide_render = shot != 14
        for o in self.mounds:
            o.hide_render = shot != 13
        H.STATE["bucket"]["root"].hide_render = False

    def per_frame(self, shot, g):
        if shot == 13:
            a, b = self.SHOTS[13]
            u = clamp((g - a) / float(b - a))
            set_snow_depth(0.95 - 0.6 * ease(u, "sine"))
            self.puddles.update(0.45 + 0.55 * ease(u, "sine"))
            for o in self.mounds:
                k = 1.0 - 0.3 * u; r = o["r"]
                o.scale = (r * 1.6 * k, r * 1.1 * k, r * (0.62 - 0.27 * u))
            self.drip.ob.hide_render = True
        else:
            set_snow_depth(0.35)
            self.drip.ob.hide_render = False
            self.drip.update(g)


if __name__ == "__main__":
    main(Take, sys.argv)
