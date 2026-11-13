#!/usr/bin/env python3
"""shot.py -- film 5 take s11: shot 11 (the gaffer's lamp, quote 2), mine set tunnel LAMP, g 971..1092 + 8-frame handles.

    11a g  963..1010  low angle (tunnel_low family) on the gaffer under the roof timbers: he lifts his flame lamp high on
                      "ยกตะเกียงขึ้นชี้" (lift g 978..992), the flame grows bright (flame 1.0 -> 1.7); miners behind; slow push
                      (ref a t0083: low medium, the figure points, a second figure smaller behind)
    11b g 1011..1050  cut, closer and lower: the raised lamp beside his smug face, he points at it; his mouth moves on the quoted
                      line "ไฟยังสว่างอยู่เลย นกเอ็งแค่ง่วงนอน" from g 1026 (34.09 s) (ref a t0085)
    11c g 1051..1100  cut, wider eye-level two-plane: the gaffer foreground right still talking, the three miners behind shrug
                      (g 1056..1068) and nod along; g 1093..1100 = out-handle rendered in 3D (ref a t0087)
Mouth: only the gaffer's, only inside the quote (lip-sync from the narration level, a new drawing every 2 frames).
NO depth of field anywhere.  python3 shot.py probe|stills|final <sids> <g spec|all> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk                                                     # noqa: E402
from tk import Vector, TP, ez, lerp, lerpv, blink, pulse, keys, cam_keys, g_of, cast5, lipsync  # noqa: E402

G0, G1, H = 971, 1093, 8
G_11B, G_11C = 1011, 1051
LIFT = (978, 992)                              # g_of(32.97) = 992: the lamp is up on "ตะเกียงขึ้นชี้"
Q_ON, Q_OFF = g_of(34.09), g_of(36.40)         # 1026 .. 1095: the quoted line
SHRUG = (1056, 1068)

GAFFER = TP(9.7, -0.65, 0)
MINERS = {"miner1": TP(13.2, -2.0, 0), "miner2": TP(11.0, 1.15, 0), "miner3": TP(11.8, 0.05, 0)}


def cam_11a(g):
    a = (TP(6.15, 0.55, 0.78), TP(10.4, -0.55, 2.62))
    b = (TP(6.55, 0.45, 0.80), TP(10.4, -0.60, 2.70))
    return cam_keys(g, [(G0 - H, a, "sine"), (G_11B, b, "hold")])


def cam_11b(g):
    a = (TP(7.55, 0.40, 1.50), TP(9.9, -0.40, 2.90))
    b = (TP(7.75, 0.36, 1.52), TP(9.9, -0.42, 2.92))
    return cam_keys(g, [(G_11B, a, "sine"), (G_11C, b, "hold")])


def cam_11c(g):
    a = (TP(18.3, -1.15, 2.0), TP(9.7, -0.35, 2.35))
    b = (TP(17.8, -1.15, 2.0), TP(9.7, -0.35, 2.38))
    return cam_keys(g, [(G_11C, a, "sine"), (G1 + H, b, "hold")])


def gaffer(g):
    """lamp in the screen-right hand (prop_r), lifted from his side to high beside his head; the other hand points at it."""
    base = cast5.STORY5["gaffer_lift_lamp"][1]
    u = ez((g - LIFT[0]) / float(LIFT[1] - LIFT[0]), "back_out")
    up = clamp01(u)
    p = dict(base)
    p["arm_r"] = dict(hand=(lerp(0.74, 1.00, u), lerp(0.95, -0.45, u)), bend=lerp(0.4, -0.9, up), stretch=lerp(1.0, 1.3, up))
    v = ez((g - (LIFT[1] - 4)) / 8.0)
    p["arm_l"] = dict(hand=(lerp(-0.55, 0.56, v), lerp(0.90, 0.66, v)), shape="point" if v > 0.4 else "fist",
                      bend=lerp(0.4, -1.0, v), stretch=lerp(1.0, 1.3, v))
    p["flame"] = lerp(1.0, 1.7, up) + 0.06 * math.sin(g * 1.3)
    p["pitch"] = lerp(-0.30, -0.55, up)
    p["gaze"] = (lerp(0.2, 0.8, up), lerp(0.0, -0.8, up))
    p["head_roll"] = 6 + 2 * math.sin(g * 0.13)
    p["lean"] = -4 - 2 * up + 1.0 * math.sin(g * 0.09)
    m = lipsync(g, Q_ON, Q_OFF)
    if m:
        p["mouth"] = m
        p["gaze"] = (lerp(0.8, -0.3, ez((g - Q_ON) / 10.0)), lerp(-0.8, 0.1, ez((g - Q_ON) / 10.0)))   # turns from the lamp to the boy
    p["blink"] = blink(g, [1000, 1043, 1079])
    p["t"] = g / 30.0
    return p


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def miner(n):
    off = {"miner1": 0, "miner2": 4, "miner3": 9}[n]

    def f(g):
        g2 = g - off // 3
        k = keys(g2, [(SHRUG[0] - 2, 0.0, "back_out"), (SHRUG[0] + 5, 1.0, "lin"), (SHRUG[1] + 4, 1.0, "sine"), (SHRUG[1] + 16, 0.3, "lin")])
        p = dict(yaw={"miner1": 0.35, "miner2": -0.30, "miner3": -0.1}[n], pitch=-0.15, expr="smirk" if n == "miner3" else "unimpressed",
                 legs="stand", head_roll=lerp(0, 12 if off % 2 == 0 else -12, k) + 2 * math.sin(g * 0.1 + off),
                 arm_r=dict(hand=(lerp(0.32, 0.78, k), lerp(0.95, 0.05, k)), bend=-0.6, shape="open" if k > 0.3 else "fist", stretch=1.15),
                 arm_l=dict(hand=(lerp(-0.32, -0.78, k), lerp(0.95, 0.05, k)), bend=0.6, shape="open" if k > 0.3 else "fist", stretch=1.15),
                 squash=(1.0, 1.0 + 0.02 * k), head_dy=-0.04 * k)
        p["blink"] = blink(g, [985 + off, 1040 + off, 1080 + off])
        p["t"] = g / 30.0
        return p
    return f


def lamps(T, g, f, cam):
    a = T.actors["gaffer"]; an = T.anch[("gaffer", f)]
    tip = tk.actors.local_to_world(a, an["prop_tip_r"], f)
    loc, _ = cam(g)
    tc = loc - tip; tc.z = 0; tc.normalize()
    up = clamp01(ez((g - LIFT[0]) / float(LIFT[1] - LIFT[0])))
    return {"lamp_a": (tip + tc * 0.08, lerp(1.0, 1.6, up)),              # his flame lamp, burning bright
            "lamp_b": (TP(12.4, 0.4, 2.9), 0.40)}                           # miners' lamps behind (warm, off-screen)


def _spec(name, g0, g1, cam, **kw):
    d = dict(name=name, g=(g0, g1), cam=cam)
    d.update(kw)
    return d


def _cast(gppd, mppd):
    d = {"gaffer": dict(cast="gaffer", ppd=gppd, place=lambda g: GAFFER, pose=gaffer)}
    if not mppd:
        return d
    for n, p in MINERS.items():
        d[n] = dict(cast=n, ppd=mppd, place=(lambda g, p=p: p), pose=miner(n))
    return d


SHOTS = {
    0: _spec("11a", G0 - H, G_11B - 1, cam_11a, cage="hidden", actors=_cast(384, 192), lamps=lambda T, g, f: lamps(T, g, f, cam_11a)),
    1: _spec("11b", G_11B, G_11C - 1, cam_11b, cage="hidden", actors=_cast(576, 0), lamps=lambda T, g, f: lamps(T, g, f, cam_11b)),
    2: _spec("11c", G_11C, G1 + H - 1, cam_11c, cage="hidden", lens=30, actors=_cast(384, 256), lamps=lambda T, g, f: lamps(T, g, f, cam_11c)),
}

if __name__ == "__main__":
    tk.main(SHOTS, "s11", sys.argv)
