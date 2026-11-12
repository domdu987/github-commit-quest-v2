#!/usr/bin/env python3
"""shot.py -- film 3 take s12: shot 12 (the foreman kicks the bucket away), harbor set WINTER, base_eye (custom, nearer).

    shot 12  g 1008..1130 (plan 33.60-37.70 s)  hard cut in from shot 11; 12-frame dissolve out to shot 13 (out-handle
             g 1131..1138 rendered in 3D).
    g 1008  two-shot at eye level by the tank foot: the foreman (near, smug, cigar) beside tommy's bucket under the dripping
            seam, tommy behind him at the left, worried.  Slow push.
    g 1027  wind-up, g 1035 KICK ("foreman_kick", boot on the bucket on "หัวหน้าเตะ" / "ถังรอง"): the bucket flies off to the
            right and clatters down (g 1047, bounce 1052), its molasses splashes at the foot of the wall; small camera jolt.
    g 1050..1058  snap punch-in on the foreman.  g 1062..1122 the quote ("เห็นไหม ถังเหงื่อแตกของแกยังยืนอยู่เลย"):
            mouth moves (lip-sync cycle, 2 frames per drawing), thumb jabbed over his shoulder at the tank, smug.  Mouth closed
            everywhere else (cigar back in).
    g 1092..1104  reframe left onto tommy, worried (sweat), the foreman's shoulder at the right edge; slow push to the end.
    The drip keeps falling (glossy elongated drop): into the bucket before the kick, onto the ground after.
    Darks: the shade of the barrels / trestle falls over the near yard (lower left).

    python3 shot.py probe 12 a:b:step | stills 12 a:b:step <dir> [scale] [samples] | final 12 [a:b] [scale] [samples]
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib3 import *            # noqa: F401,F403

G0, G1 = gb(33.60), gb(37.70)                      # 1008, 1131
H_OUT = 12 // 2 + 2                                 # 8
G_KICK = g_of(34.4)                                 # 1035
G_Q0, G_Q1 = g_of(35.3), g_of(37.3)                 # 1062, 1122: mouth moves only inside
PUNCH = (1050, 1058)
TO_TOMMY = (1092, 1104)

B = Vector(H.BUCKET_MARK)
CAM0 = Vector(H.CAMS["base_eye"]["loc"])
_d = (B - CAM0); _d.z = 0; _d.normalize()
YAW = math.degrees(math.atan2(_d.x, _d.y))          # 17.8: looking at the bucket seam
R = Vector((_d.y, -_d.x, 0.0))                     # camera right on the ground
D = _d
FOREMAN = B - R * 1.12 - D * 0.32                   # his kicking boot lands on the bucket's near-left side at g 1035
TOMMY = B - R * 2.45 + D * 0.12
F_HEAD = FOREMAN + Vector((0, 0, 2.76))
T_HEAD = TOMMY + Vector((0, 0, 1.97))

# bucket flight (world) after the kick: up and away to the right along the wall, lands on its side, one bounce
FLY = [(G_KICK, B, (0, 0, 0)),
       (G_KICK + 6, B + R * 1.55 + D * 0.05 + Vector((0, 0, 1.25)), (40, 0, 160)),
       (G_KICK + 12, B + R * 2.85 - D * 0.25 + Vector((0, 0, 0.0)), (90, 0, 300)),
       (G_KICK + 15, B + R * 3.15 - D * 0.32 + Vector((0, 0, 0.22)), (90, 0, 330)),
       (G_KICK + 18, B + R * 3.40 - D * 0.38 + Vector((0, 0, 0.0)), (90, 0, 352)),
       (G_KICK + 26, B + R * 3.55 - D * 0.40 + Vector((0, 0, 0.0)), (90, 0, 360))]


def frame(look, dist, yaw, pitch, dx=0.0, dz=0.0):
    """camera that looks at `look` (offset dx along camera right, dz up so the subject sits off-centre)"""
    yr = math.radians(yaw)
    r = Vector((math.cos(yr), -math.sin(yr), 0.0))
    lk = Vector(look) + r * dx + Vector((0, 0, dz))
    return sph(lk, dist, yaw, pitch), lk


MID = F_HEAD.lerp(T_HEAD, 0.42)
CA = frame(MID, 6.4, YAW + 1.0, -6.0, 0.25, -0.55)
CB = frame(MID, 5.45, YAW - 1.5, -7.0, 0.15, -0.50)
CP = frame(F_HEAD, 3.15, YAW - 3.0, -4.0, -0.15, -0.30)
CP2 = frame(F_HEAD, 2.95, YAW - 3.5, -4.0, -0.15, -0.28)
CT = frame(T_HEAD, 3.6, YAW + 6.0, -5.0, 0.55, -0.25)
CT2 = frame(T_HEAD, 3.15, YAW + 6.5, -5.0, 0.50, -0.22)


def shake(g, amp):
    d = g - G_KICK
    if 0 <= d <= 8:
        a = amp * math.exp(-0.5 * d)
        return 0.6 * a * math.sin(d * 2.9), a * math.cos(d * 2.3)
    return 0.0, 0.0


class Take(BaseTake):
    PRESET = "WINTER"
    SHOTS = {12: (G0, G1 + H_OUT - 1)}
    SEEP = 0.7
    BUCKET = dict(fill=0.3, visible=True)

    def setup(self):
        self.actor("foreman"); self.actor("tommy")
        self.drip = Drip(period=22, phase=3)
        si = 0
        for g, p, rot in FLY:
            H.set_bucket(pos=tuple(p), rot=(rot[0], rot[1], math.degrees(H.TH_B + math.pi / 2) + rot[2]), frame=bf(si, g))
        H.set_bucket(fill=0.3, frame=bf(si, G_KICK)); H.set_bucket(fill=0.0, frame=bf(si, G_KICK + 2))
        # splash of molasses where the bucket stood
        m = H.STATE["M"]["molasses"]; mb = H.MB(); pts = []
        for j in range(16):
            a = 2 * math.pi * j / 16; k = 1 + 0.25 * math.sin(5 * a + 1) + 0.1 * math.sin(3 * a)
            pts.append((0.55 * k * math.cos(a), 0.42 * k * math.sin(a), 0.0))
        mb.oface(pts, m, [(0, 0)] * 16, (0, 0, 1))
        self.splash = mb.obj("w3_splash", self.fx); T.no_bounce(self.splash)
        self.splash.location = (B.x + R.x * 0.5, B.y + R.y * 0.5, 0.016)

    def cam(self, shot, g):
        a, b = self.SHOTS[12]
        k = lambda c: tuple(c[0]) + tuple(c[1])
        ks = [(a, k(CA), "cubic_out"), (PUNCH[0], k(CB), "quint"), (PUNCH[1], k(CP), "quad_out"),
              (TO_TOMMY[0], k(CP2), "smooth"), (TO_TOMMY[1], k(CT), "sine"), (b, k(CT2), "lin")]
        v = mkeys(g, ks, 0.22)
        loc, look = Vector(v[:3]), Vector(v[3:])
        sx, sz = shake(g, 0.06)
        f, r, u = cam_basis(loc, look)
        return loc, look + r * sx + u * sz

    def cast_in(self, shot):
        return ["foreman", "tommy"]

    def place(self, shot, n, g):
        return FOREMAN if n == "foreman" else TOMMY

    def pose(self, shot, n, g):
        if n == "foreman":
            return self.foreman_pose(g)
        return self.tommy_pose(g)

    def foreman_pose(self, g):
        bl = blink(g, [1016, 1047, 1084, 1110, 1129])
        if g < G_KICK - 8:
            c, p = cast3.STORY3["foreman_smug"]; p = dict(p)
            p["head_roll"] = 5 + 2 * math.sin(g * 0.15); p["lean"] = 1.5 * math.sin(g * 0.11)
            p["blink"] = bl
            return p
        if g < G_KICK - 2:                                    # wind-up: lean back, angry, weight on the back foot
            c, p = cast3.STORY3["foreman_kick"]; p = dict(p)
            p["legs"] = "stand"; p["lean"] = -4 - 2 * (g - (G_KICK - 8)); p["head_roll"] = 4
            return p
        if g < G_KICK + 7:
            c, p = cast3.STORY3["foreman_kick"]; p = dict(p)
            if g < G_KICK:                                    # boot swinging forward
                legs = dict(p["legs"]); fr = legs["foot_r"]; u = (g - (G_KICK - 2) + 1) / 3.0
                legs["foot_r"] = (0.35 + (fr[0] - 0.35) * u, fr[1] + 0.62 * (1 - u) * 0.6); p["legs"] = legs
            p["squash"] = (1.0 + 0.03 * pulse(g, G_KICK - 1, G_KICK, G_KICK + 4, 1.0), 1.0 - 0.03 * pulse(g, G_KICK - 1, G_KICK, G_KICK + 4, 1.0))
            return p
        if g < G_KICK + 12:                                   # in-betweens: the boot comes down, the body settles (no pop)
            ca, pa = cast3.STORY3["foreman_kick"]; cb, pb = cast3.STORY3["foreman_smug_kick_after"]
            u = ease((g - (G_KICK + 6)) / 6.0, "sine")
            p = sprites.puppet.lerp_pose("foreman", pa, pb, u)
            p["blink"] = bl
            return p
        if g < G_Q0:
            c, p = cast3.STORY3["foreman_smug_kick_after"]; p = dict(p)
            p["head_roll"] = 6 + 2 * math.sin(g * 0.13); p["blink"] = bl; p["gaze"] = (0.6, 0.1)
            return p
        # the quote and after: thumb over his (screen-right) shoulder at the tank, smug; mouth only inside the quote
        p = dict(yaw=0.35, pitch=-0.3, expr="smug", head_roll=6 + 3 * math.sin(g * 0.45), lean=-2 + 1.5 * math.sin(g * 0.3),
                 arm_l=dict(hand=(-0.34, 0.98), bend=0.6), arm_r=dict(hand=(0.82, -0.30), shape="point", bend=0.7, stretch=1.25), legs="wide", blink=bl)
        m = mouth_at(g, G_Q0, G_Q1)
        if m is not None:
            p["mouth"] = m
            p["squash"] = (1.0 + 0.012 * math.sin(g * 1.1), 1.0 - 0.012 * math.sin(g * 1.1))
        else:
            p["cigar"] = True
        return p

    def tommy_pose(self, g):
        c, p = cast3.STORY3["tommy_worried"]; p = dict(p)
        fl = pulse(g, G_KICK - 1, G_KICK + 1, G_KICK + 9, 1.0)
        p["squash"] = (1.0 + 0.05 * fl, 1.0 - 0.06 * fl)
        p["head_roll"] = 6 - 10 * fl + 1.5 * math.sin(g * 0.5)
        if G_KICK <= g < G_KICK + 28:
            p["gaze"] = (1.0, 0.1)
            p["expr"] = "shocked" if g < G_KICK + 10 else "worried"
        else:
            p["gaze"] = (0.6, -0.2)
        p["blink"] = blink(g, [1020, 1070, 1101, 1125])
        return p

    def ppd(self, shot, n):
        return 384 if n == "foreman" else 320

    def per_frame(self, shot, g):
        self.drip.update(g, floor_z=None if g < G_KICK else 0.03)
        u = clamp((g - G_KICK - 1) / 6.0)
        self.splash.scale = (max(0.01, u), max(0.01, u), 1.0)
        self.splash.hide_render = u <= 0.0

    def report(self, shot, g):
        out = BaseTake.report(self, shot, g)
        f = bf(0, g)
        if ("foreman", f) in self.anch:
            a = self.actors["foreman"]
            fx, fy = self.anch[("foreman", f)]["foot_r"]
            out["foot_r_px"] = [round(v, 1) for v in actors.local_to_screen(a, self.camera, (fx, fy), f, a.feet.get(f))[:2]]
        out["bucket_px"] = [round(v, 1) for v in render.world_to_screen(self.camera, tuple(B + Vector((0, 0, 0.55)) - R * 0.3), f)[:2]]
        return out


if __name__ == "__main__":
    main(Take, sys.argv)
