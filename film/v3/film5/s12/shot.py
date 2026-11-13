#!/usr/bin/env python3
"""shot.py -- film 5 take s12: shot 12 (36.42-40.14 s, g 1093..1203, handles g 1085..1092 / 1204..1211), mine tunnel LAMP.

Next day: the brass cage hangs on its nail (the set's 3D cage, cage_insert side); the canary sprite stands on the perch at the cage
centre, INSIDE the bars (front wires cross it, back wires behind it).  Three ECU framings (a framing change every 1.2-1.3 s):
    12a g 1093..1131  front three-quarter from outbye, the bird quiet and a little ruffled on its perch; slow push      (ref a t0041)
    12b g 1132..1167  tighter, from the inbye side: it sings ONE note (beak opens g 1144 "โน้ตเดียว"), then droops, the eyes
                      close softly (never X eyes)
    12c g 1168..1203  low, level with the cage floor: it tips off the perch and drops gently to the floor (g 1172..1181, on
                      "แล้วล้มลงที่"), a small settle, then lies still, eyes closed, faint breathing; slow push.  Handle to 1211.
Internal sub ids 1, 2, 3 (= 12a, 12b, 12c).  No depth of field anywhere.
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from base import *                                       # noqa: F401,F403
import base as B

G0, G1, H = 1093, 1204, 8                                 # shot 12 = [1093, 1204); handles 8 each side (dissolve 12 / 2 + 2)
G_B, G_C = 1132, 1168
G_NOTE = g_of(38.04) + 1                                  # 1145 "โน้ตเดียว": the one note
G_FALL = (1172, 1181)                                     # the drop (on "แล้วล้มลงที่" 1167 .. "พื้นกรง" 1189)
Y, S0 = 16.25, -1.86                                      # the cage: station y, across s


def C(dy, ds, z):
    return TP(Y + dy, S0 + ds, z)


def cam_a(g):
    return cam_keys(g, [(G0 - H, C(-0.62, 0.52, 2.98), C(0.0, 0.0, 2.93), "sine"), (G_B, C(-0.47, 0.40, 2.95), C(0.0, 0.0, 2.92), "hold")])


def shifted(lk, sr, up):
    """move the look point by sr D to screen-right and up D (the bird sits left of centre, room for the note)"""
    def f(g):
        loc, look = lk(g)
        v = look - loc; r = v.cross(Vector((0, 0, 1))).normalized()
        return loc, look + r * sr + Vector((0, 0, up))
    return f


def _cam_b(g):
    return cam_keys(g, [(G_B, C(0.48, 0.66, 2.95), C(0.02, 0.0, 2.91), "sine"), (G_C, C(0.40, 0.55, 2.92), C(0.02, 0.0, 2.88), "hold")])


cam_b = shifted(_cam_b, 0.06, 0.05)


def cam_c(g):
    return cam_keys(g, [(G_C, C(-0.50, 0.86, 2.98), C(0.0, 0.0, 2.74), "sine"), (G1 + H, C(-0.40, 0.66, 2.93), C(0.0, 0.0, 2.72), "hold")])


def bird(T, g):
    """the canary: quiet -> one note -> droop, eyes closing -> the drop -> lies still on the cage floor (eyes closed)"""
    p = dict(state="perch_quiet", beak=0.0, eyes=0.9, droop=0.25, ruffle=0.35, lie=0.0, notes=0, breath=0.25, t=g / 30.0)
    p["eyes"] = 0.9 if blink(g, [1110, 1128]) == 0 else (0.45 if blink(g, [1110, 1128]) == 1 else 0.05)
    if G_NOTE - 3 <= g <= G_NOTE + 14:                                         # the one note
        u = clamp((g - (G_NOTE - 3)) / 3.0)
        p.update(state="sing_one", beak=0.65 * u * (1.0 if g < G_NOTE + 9 else clamp((G_NOTE + 14 - g) / 5.0)), eyes=0.85, droop=0.3)
    if G_NOTE - 1 <= g <= G_NOTE + 22:
        p["notes"] = 1
    if g > G_NOTE + 14:                                                        # droop, the eyes close softly
        u = ez((g - (G_NOTE + 14)) / 12.0)
        p.update(state="droop", droop=lerp(0.3, 1.0, u), ruffle=lerp(0.35, 0.9, u), eyes=lerp(0.85, 0.0, ez((g - (G_NOTE + 14)) / 9.0)))
    if g >= G_FALL[0]:                                                          # the drop: lie 0 -> 1
        u = clamp((g - G_FALL[0]) / float(G_FALL[1] - G_FALL[0]))
        p.update(state="fallen", eyes=0.0, droop=lerp(1.0, 0.7, u), ruffle=lerp(0.9, 0.6, u), lie=ez(u, "quad_in"), breath=0.0)
    if g > G_FALL[1] + 6:
        p["breath"] = 0.18                                                     # gentle: still breathing (it revives at the end)
    pos = Vector(T.perch)
    if g >= G_FALL[0]:
        u = clamp((g - G_FALL[0]) / float(G_FALL[1] - G_FALL[0]))
        drop = ease(u, "quad_in") if u < 1 else 1.0                               # falls under gravity
        bounce = 0.025 * pulse(g, G_FALL[1], G_FALL[1] + 2, G_FALL[1] + 5, 1.0)
        pos = lerpv(T.perch, T.floor + Vector((0, 0, 0.012)), drop) + Vector((0, 0, bounce))
    return pos, p


def stage(T, g):
    pos, p = bird(T, g)
    return {"bird": dict(pos=pos, pose=p)}


def lamps(T, g, f):
    if os.environ.get("NOLAMP"):
        return {}
    loc = T.subs[T.cur].cam(g)[0]
    d = loc - T.perch; d.z = 0; d.normalize()
    return {"lamp_rim": (T.perch - d * 0.6 + Vector((0, 0, 0.55)), 0.10)}   # warm back light on the wires (a key lamp blew out the tray)


def gas(g):
    return 1.6


SUBS = {1: Sub("12a", (G0 - H, G_B - 1), cam_a, stage, lamps=lamps, actors=["bird"], gas=gas, ppd={"bird": 2048}),
        2: Sub("12b", (G_B, G_C - 1), cam_b, stage, lamps=lamps, actors=["bird"], gas=gas, ppd={"bird": 2048}),
        3: Sub("12c", (G_C, G1 + H - 1), cam_c, stage, lamps=lamps, actors=["bird"], gas=gas, ppd={"bird": 2048})}
for _s in SUBS.values():
    _s.lamp_names = ("lamp_rim",)

if __name__ == "__main__":
    B.main("s12", SUBS, HERE, sys.argv)
