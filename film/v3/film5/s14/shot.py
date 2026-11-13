#!/usr/bin/env python3
"""shot.py -- film 5 take s14: shot 14 (45.49-50.08 s, g 1365..1501, handles g 1357..1364 / 1502..1509), mine tunnel LAMP.

The foreman's lamp flame flares tall and blue (firedamp), the gas lights, and a fireball races down the roadway behind the running
group.  No casualties: everybody (the gaffer last) is ahead of the front in every frame.
    14a g 1365..1404  lamp_insert ECU: the hanging flame safety lamp, flame normal, then tall (set_flame 1 -> 2, g 1378..1396) and
                      pale blue (the set's insert-flame emission keyed warm -> blue at runtime; "แล้วเปลวไฟในตะเกียง")
    14b g 1405..1440  low angle under the lamp: the gaffer looks up at the blue flame, hands up, shocked; on "ก็จุดแก๊ส" (g 1422)
                      the flame bursts (k 3.2) with an orange flash, and he turns and runs off outbye
    14c g 1441..1475  blast_wide from the pit bottom: alfie (cage held, bird inside), miners 1-3 and the gaffer run at the camera;
                      the fireball comes round the bend behind them (set_blast 0.12 -> 0.42, "ทั้งอุโมงค์ระเบิด" g 1464)
    14d g 1476..1501  low and close, the camera backing off before them: the runners big in front, the fire front y 17 -> 10
                      behind ("ไล่หลังพวกเขามา").  Handle to g 1509.
Internal sub ids 1..4 (= 14a..14d).  No depth of field anywhere.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s12"))
from base import *                                       # noqa: F401,F403
import base as B
B.CAST["gaffer"] = ("gaffer", (-2.25, -5.25, 2.25, 0.125))    # roomier canvas: both hands up

G0, G1, H = 1365, 1502, 8
G_B, G_C, G_D = 1405, 1441, 1476
G_IGN = g_of(47.31)                                       # 1422 "ก็จุดแก๊ส"
G_BOOM = g_of(48.70)                                      # 1464 "ระเบิด"
SWING = lambda g: 14 * math.sin(g * 0.45)
GAFFER = TP(9.35, 0.45, 0)


def cam_a(g):
    return cam_keys(g, [(G0 - H, TP(8.22, 0.76, 3.38), TP(8.75, 1.25, 3.33), "sine"), (G_B, TP(8.36, 0.88, 3.36), TP(8.75, 1.25, 3.36), "hold")])


def cam_b(g):
    return cam_keys(g, [(G_B, TP(13.4, -0.55, 1.35), TP(9.0, 0.75, 3.1), "sine"), (G_C, TP(13.1, -0.50, 1.35), TP(9.0, 0.75, 3.05), "hold")])


def cam_c(g):
    return cam_keys(g, [(G_C, TP(0.6, 0.9, 3.3), TP(18, 0.2, 1.7), "sine"), (G_D, TP(1.0, 0.9, 3.2), TP(18, 0.2, 1.7), "hold")])


def cam_d(g):
    return cam_keys(g, [(G_D, TP(1.4, 1.35, 1.6), TP(10.0, -0.7, 2.4), "lin"), (G1 + H, TP(-0.6, 1.35, 1.6), TP(8.0, -0.7, 2.4), "hold")])


def flame_k(g):
    k = keys(g, [(1378, 1.0, "sine"), (1396, 2.0, "hold")])
    if g >= G_IGN:
        k = 2.0 + 1.2 * pulse(g, G_IGN, G_IGN + 3, G_IGN + 16, 1.0)
    return k + 0.06 * math.sin(g * 1.7)


def flame_blue(g):
    return keys(g, [(1380, 0.0, "sine"), (1396, 1.0, "hold")])


def blast_u(g):
    return keys(g, [(G_C - 1, 0.0, "lin"), (G_C, 0.35, "lin"), (G_D, 0.55, "lin"), (G1 + H, 0.66, "hold")])


def ctl(T, f, g):
    T.flame(f, flame_k(g), flame_blue(g))
    M.set_blast(blast_u(g) if g >= G_C else 0.0, frame=f)


# ----------------------------------------------------------------------------- poses
def cage_bird(g):
    return dict(state="fallen", eyes=0.0, swing=SWING(g), t=g / 30.0, breath=0.15)


def gaffer_b(g):
    if g < G_IGN + 4:
        p = dict(cast5.STORY5["gaffer_shocked"][1])
        for k in ("prop_l", "prop_r", "flame", "flame_blue"):
            p.pop(k, None)
        u = ez((g - G_B) / 8.0)
        p.update(yaw=0.25, pitch=-0.55, gaze=(0.6, -0.9), expr="worried" if g < 1414 else "shocked", t=g / 30.0,
                 arm_r=dict(hand=(lerp(0.6, 0.85, u), lerp(0.4, -0.35, u)), bend=-0.8, shape="open", stretch=1.2),
                 arm_l=dict(hand=(lerp(-0.6, -0.85, u), lerp(0.45, -0.3, u)), bend=-0.8, shape="open", stretch=1.2))
        p["fx"] = ["sweat"] if g >= 1414 else []
        p["mouth"] = "o" if g >= 1414 else "frown"
        p["blink"] = blink(g, [1410])
        return GAFFER, p
    p = dict(cast5.STORY5["gaffer_run"][1]); p.pop("prop_r", None); p.pop("flame", None)
    p.update(yaw=-0.85, legs=run_legs(g, 10, 1.1), arm_r=dict(hand=(0.6, -0.2), bend=-0.9, shape="open"), t=g / 30.0, mouth="o")
    u = (g - (G_IGN + 4)) / 14.0
    return TP(9.35 - 1.6 * max(0.0, u) ** 1.3, 0.45 - 0.9 * clamp(u), 0), p


def stage_b(T, g):
    pos, p = gaffer_b(g)
    return {"gaffer": dict(pos=pos, pose=p)}


RUN = {  # name: (s across, start station lag behind alfie, run phase)
    "alfie": (-0.9, 0.0, 0.0), "miner1": (0.15, 0.8, 0.3), "miner2": (-1.7, 1.6, 0.6), "miner3": (1.1, 2.2, 0.15), "gaffer": (-0.6, 3.3, 0.45)}


def runner(n, g):
    if n == "alfie":
        p = dict(yaw=0.2, pitch=-0.05, expr="worried", mouth="frown", fx=["sweat"], lean=10, head_roll=-5, prop_r="cage", bird=cage_bird(g),
                 arm_r=dict(hand=(0.55, 0.25), bend=-0.8, stretch=1.3), arm_l=dict(hand=(-0.55, 0.55), bend=0.6))
    elif n == "gaffer":
        p = dict(cast5.STORY5["gaffer_run"][1]); p.pop("prop_r", None); p.pop("flame", None)
        p.update(yaw=0.2, arm_r=dict(hand=(0.6, -0.25), bend=-0.9, shape="open"), mouth="o")
    else:
        p = dict(cast5.STORY5["miners_run" + ("" if n == "miner1" else "_" + n)][1])
        p.update(yaw={"miner1": -0.2, "miner2": 0.25, "miner3": -0.3}[n])
    s, lag, ph = RUN[n]
    p["legs"] = run_legs(g, 10, 1.15, ph)
    p["t"] = g / 30.0
    p["lean"] = 6
    p["blink"] = blink(g, [1450 + int(10 * ph), 1490 + int(10 * ph)])
    return p


def stage_run(y_of):
    def st(T, g):
        ya = y_of(g)
        out = {}
        for n, (s, lag, ph) in RUN.items():
            bob = 0.05 * abs(math.sin(math.pi * (g / 10.0 + ph)))
            out[n] = dict(pos=TP(ya + lag, s, 0) + Vector((0, 0, bob)), pose=runner(n, g))
        return out
    return st


def lamps(T, g, f):
    S = T.subs[T.cur]
    on = {}
    if S.name == "14b":
        fl = Vector(M.STATE["insert_flame_pos"])
        on["lamp_ign"] = (fl + Vector((0, 0, 0.2)), 9.0 * pulse(g, G_IGN, G_IGN + 2, G_IGN + 14, 1.0), (1.0, 0.55, 0.22))
    if "alfie" in S.actors and ("alfie", f) in T.anch:
        a = T.actors["alfie"]
        hx, hy = T.anch[("alfie", f)]["hip"]
        p = actors.local_to_world(a, (hx + 0.30, hy + 0.12), f)
        loc = S.cam(g)[0]; tc = loc - p; tc.z = 0; tc.normalize()
        on["lamp_alfie"] = (p + tc * 0.12, 0.75)
    return on


RUNNERS = ["alfie", "miner1", "miner2", "miner3", "gaffer"]
SUBS = {1: Sub("14a", (G0 - H, G_B - 1), cam_a, lambda T, g: {}, ctl=ctl, lamps=None, actors=[], gas=2.4),
        2: Sub("14b", (G_B, G_C - 1), cam_b, stage_b, ctl=ctl, lamps=lamps, actors=["gaffer"], gas=2.4, ppd={"gaffer": 384}),
        3: Sub("14c", (G_C, G_D - 1), cam_c, stage_run(lambda g: 8.6 - 0.10 * (g - G_C)), ctl=ctl, lamps=lamps, actors=RUNNERS, gas=0.0,
               ppd={n: 192 for n in RUNNERS}),
        4: Sub("14d", (G_D, G1 + H - 1), cam_d, stage_run(lambda g: 5.0 - 0.085 * (g - G_D)), ctl=ctl, lamps=lamps, actors=RUNNERS, gas=0.0,
               ppd={"alfie": 384, "miner1": 320, "miner2": 288, "miner3": 288, "gaffer": 256})}
for _s in SUBS.values():
    _s.lamp_names = ("lamp_alfie", "lamp_ign")
    _s.extra = {"cage3d": lambda g: False}

if __name__ == "__main__":
    B.main("s14", SUBS, HERE, sys.argv)
