#!/usr/bin/env python3
"""shot.py -- film 5 take s08: shot 8 (the nickname "ไอ้เด็กเลี้ยงนก"), mine set tunnel LAMP, g 691..756 + 8-frame handles.

    8a  g 683..728  eye level looking inbye: the three miners in the foreground point (screen-left) and laugh at alfie, who stands
                    small in the depth on the walkway with the cage in his hand (2D held cage, the canary inside the bars); slow push
                    and drift (ref a t0047: the group laughing at the table)
    8b  g 729..764  cut on "ไอ้เด็ก" (24.25 s): the reverse, looking outbye: alfie in the foreground, hurt, hugging the cage to his
                    chest, the bird singing 3 small notes; behind him the miners still point and laugh; slow push (g 757..764 = handle)
Mouths: laughing faces are static drawings (wide grin); no mouth moves in this take (no quoted line).
NO depth of field anywhere.  python3 shot.py probe|stills|final <sids> <g spec|all> ...
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tk                                                     # noqa: E402
from tk import Vector, TP, ez, lerp, lerpv, blink, pulse, cam_keys, g_of, cast5  # noqa: E402

G0, G1, H = 691, 757, 8
G_8B = 729                                   # g_of(24.25) = 730: cut one frame before the word

ALFIE = TP(11.8, -1.05, 0)
MINERS = {"miner2": TP(7.3, 1.25, 0), "miner1": TP(8.4, 0.30, 0), "miner3": TP(10.1, 0.95, 0)}


def cam_8a(g):
    a = (TP(3.75, -0.15, 2.12), TP(10.6, -0.10, 1.98))
    b = (TP(4.25, -0.25, 2.08), TP(10.6, -0.25, 1.98))
    return cam_keys(g, [(G0 - H, a, "sine"), (G_8B + 1, b, "hold")])


def cam_8b(g):
    a = (TP(14.25, -0.95, 1.86), TP(8.6, -0.30, 1.90))
    b = (TP(13.90, -0.98, 1.84), TP(8.6, -0.35, 1.90))
    return cam_keys(g, [(G_8B, a, "cubic_out"), (G1 + H, b, "hold")])


def miner_laugh(n):
    sfx = {"miner1": "", "miner2": "_miner2", "miner3": "_miner3"}[n]
    off = {"miner1": 0, "miner2": 7, "miner3": 13}[n]
    base = cast5.STORY5["miners_laugh" + sfx][1]

    def f(g):
        p = dict(base)
        ph = (g + off) * 0.55
        b = 0.5 + 0.5 * math.sin(ph)                       # laugh bounce
        p["head_roll"] = base["head_roll"] + 5 * math.sin(ph * 0.5 + off) - 3 * b
        p["lean"] = base["lean"] - 3 * b + 2 * math.sin(g * 0.07 + off)
        p["squash"] = (1.0 + 0.025 * b, 1.0 - 0.025 * b)
        p["head_dy"] = 0.02 * b
        hx, hy = base["arm_l"]["hand"]
        p["arm_l"] = dict(base["arm_l"], hand=(hx + 0.04 * math.sin(ph), hy + 0.05 * math.sin(ph * 1.3)))
        p["t"] = g / 30.0
        return p
    return f


def alfie_8a(g):
    p = dict(cast5.STORY5["alfie_hold_cage"][1])
    p.update(expr="sad", pitch=0.35, yaw=0.25, head_roll=4, gaze=(0.6, 0.4), arm_l="down", legs="narrow")
    p["arm_r"] = dict(hand=(0.55, 0.30), bend=-0.6, stretch=1.25)
    p["bird"] = dict(state="perch_sing", notes=3, beak=0.6 + 0.2 * math.sin(g * 0.9), t=g / 30.0, swing=2 * math.sin(g * 0.15))
    p["blink"] = blink(g, [700, 722])
    p["t"] = g / 30.0
    return p


def alfie_8b(g):
    """foreground: hurt, the cage held up against his chest (both read: the boy and the bird inside the bars)."""
    p = dict(cast5.STORY5["alfie_hold_cage"][1])
    u = ez((g - G_8B) / 14.0)
    p.update(expr="sad", yaw=lerp(0.30, 0.20, u), pitch=lerp(0.15, 0.40, u), head_roll=lerp(2, 7, u), gaze=(0.7, 0.5),
             arm_l=dict(hand=(0.30, 0.62), bend=0.6), legs="narrow", lean=2)
    p["arm_r"] = dict(hand=(0.22, lerp(0.50, 0.56, u)), bend=-0.7, stretch=1.2)
    p["bird"] = dict(state="perch_sing", notes=3, beak=0.55 + 0.2 * math.sin(g * 0.9), eyes=0.9, t=g / 30.0, swing=1.5 * math.sin(g * 0.2))
    p["blink"] = blink(g, [745])
    p["fx"] = []
    p["t"] = g / 30.0
    return p


def lamps(T, g, f, cam):
    out = {}
    a = T.actors["alfie"]; an = T.anch[("alfie", f)]
    hx, hy = an["hip"]
    p = tk.actors.local_to_world(a, (hx + 0.30, hy + 0.12), f)
    loc, _ = cam(g)
    tc = loc - p; tc.z = 0; tc.normalize()
    out["lamp_a"] = (p + tc * 0.12, 0.75)                                  # alfie's belt lamp
    out["lamp_b"] = (TP(8.4, -1.6, 3.0), 0.55)                             # warm key on the laughing group (miners' lamps off-screen)
    out["lamp_c"] = (TP(10.9, 0.5, 2.9), 0.35)
    return out


def _spec(name, g0, g1, cam, **kw):
    d = dict(name=name, g=(g0, g1), cam=cam)
    d.update(kw)
    return d


def _miners(ppd):
    return {n: dict(cast=n, ppd=ppd, place=(lambda g, p=p: p), pose=miner_laugh(n)) for n, p in MINERS.items()}


SHOTS = {
    0: _spec("8a", G0 - H, G_8B - 1, cam_8a, cage="hidden",
             actors=dict(_miners(320), alfie=dict(cast="alfie", ppd=256, place=lambda g: ALFIE, pose=alfie_8a)),
             lamps=lambda T, g, f: lamps(T, g, f, cam_8a)),
    1: _spec("8b", G_8B, G1 + H - 1, cam_8b, cage="hidden",
             actors=dict(_miners(224), alfie=dict(cast="alfie", ppd=512, place=lambda g: ALFIE, pose=alfie_8b)),
             lamps=lambda T, g, f: lamps(T, g, f, cam_8b)),
}

if __name__ == "__main__":
    tk.main(SHOTS, "s08", sys.argv)
