#!/usr/bin/env python3
"""shot.py -- film 4 take s14: shots 14 and 15 (NIGHT).  Renders g 1173..1438 (7-frame handles: in before g 1180, out after 1431).

    shot 14  g 1180..1261  A (g 1173-1221) high wide over the street roofs toward the gate, pagoda + tower and the moon (ref a
             t0067-t0071: night, moon, lanterns); the ground starts to shake on "พื้นดินก็สั่นแรง" (40.02 s = g 1204): lanterns
             swing, the pagoda starts to sway, camera shake grows.  B (cut g 1222) low in the street looking up at the swinging
             lanterns and hopping roof tiles, hard shake.
    shot 15  g 1262..1431  a (g 1262-1302) side tracking shot: kenta sprints down the lantern street shouting (ref a t0075);
             b (g 1303-1344) he stops in the street and shouts toward the doorways, hand cupped ("ตะโกนให้ทุกคนเข้าไปหลบในเจดีย์"),
             the merchant smug in his doorway behind him (soft); c1 (g 1345-1386) LOW ANGLE on the merchant in his doorway under
             the eave and a lantern (ref a t0083-t0087: the guard mocking from the wall), the woman laughing behind kenta in shot b;
             he cups his hands and mock-shouts back: mouth on the quote "เจดีย์เมาจะพาพวกข้าตายหรือไง" (46.01..47.73 s ->
             g 1383..1435); c2 (g 1387-1438) snap closer, lower.  Handle out g 1432..1438 (c2 continues).
    Kenta's mouth is a fixed shout drawing (never animated); only the merchant's mouth moves (the quoted line).

    python3 shot.py probe 14,15 1173:1438:10 | stills 14,15 a:b <out> [scale] [samples] | final 14,15 1173:1438
"""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from base4 import *                                   # noqa: F401,F403
import base4 as B

G_IN, G14, G15, G16, G_OUT = 1173, 1180, 1262, 1432, 1438
G_QUAKE = g_of(40.02)              # 1204 "พื้นดินก็": the shaking starts
G_B14 = 1222                       # cut to the low street view
G_b, G_c1, G_c2 = 1303, 1345, 1387
G_SHOUT = g_of(43.31)              # 1302 "ตะโกนให้"
Q0, Q1 = g_of(46.01), g_of(47.73)  # 1383..1435 the townsman's quote
G_CUP = 1374                       # the merchant brings his hands to his mouth

KENTA_RUN_X = -1.3
KENTA_B = (-0.25, -47.3, 0.0)
MERCHANT = (3.2, -51.2, 0.0)       # at his doorway, just out from under the east house's pent roof (lantern at y -49.35)
FARMER = (3.90, -47.55, 0.0)       # next doorway north, laughing
WOMAN2 = (-0.3, -53.5, 0.0)        # in the street behind kenta, laughing (shot 15 b background)


def kenta_y(g):
    return -58.6 + (g - G15) * 0.22


def quake(g):
    if g < G_QUAKE - 4:
        return 0.0
    if g < G_B14:
        return ease((g - (G_QUAKE - 4)) / float(G_B14 - G_QUAKE + 4), "cubic_in") * 1.0
    if g < G15:
        return 1.0
    return 0.85


class Take14(B.Take):
    PRESET = "NIGHT"
    NAME = "s14"
    HERE = os.path.dirname(os.path.abspath(__file__))
    SHOTS = {14: (G_IN, G15 - 1), 15: (G15, G_OUT)}
    CAST = ["kenta", "merchant", "woman2"]

    def camera_at(self, shot, g):
        q = quake(g)
        if shot == 14 and g < G_B14:
            ks = [(G_IN, V(1.0, -60.0, 12.5), V(1.6, -12.0, 9.2), "sine"), (G_B14, V(1.0, -58.4, 12.1), V(1.7, -12.0, 8.5), "hold")]
            loc, look = path(g, ks); amp = 0.04 + 0.55 * q
        elif shot == 14:
            ks = [(G_B14, V(0.8, -53.2, 0.9), V(-2.6, -44.5, 3.3), "sine"), (G15, V(0.6, -52.5, 0.95), V(-2.5, -44.5, 3.85), "hold")]
            loc, look = path(g, ks); amp = 0.85
        elif g < G_b:
            y = kenta_y(g) + 0.55
            loc, look = V(2.2, y, 1.55), V(KENTA_RUN_X, y + 0.25, 1.78)
            loc = loc + V(0, 0.12 * ease((g - G15) / 40.0, "sine"), 0)          # the camera slowly loses ground on him
            amp = 0.45
        elif g < G_c1:
            ks = [(G_b, V(-1.75, -43.9, 1.75), V(-0.2, -47.9, 1.95), "sine"), (G_c1, V(-1.6, -44.35, 1.75), V(-0.15, -47.9, 1.92), "hold")]
            loc, look = path(g, ks); amp = 0.35
        elif g < G_c2:
            ks = [(G_c1, V(1.35, -54.0, 0.55), V(3.1, -51.2, 2.95), "sine"), (G_c2, V(1.45, -53.65, 0.58), V(3.1, -51.2, 2.85), "hold")]
            loc, look = path(g, ks); amp = 0.3
        else:
            ks = [(G_c2 - 1, V(1.45, -53.65, 0.58), V(3.1, -51.2, 2.85), "quint"), (G_c2 + 6, V(2.1, -53.15, 0.95), V(3.15, -51.2, 2.62), "sine"),
                  (G_OUT + 1, V(2.2, -52.85, 0.95), V(3.15, -51.2, 2.6), "hold")]
            loc, look = path(g, ks); amp = 0.3
        return apply_shake(loc, look, g, amp, seed=shot)

    def dof(self, shot, g):
        if shot == 14:
            return (None, None) if g < G_B14 else ((-3.8, -46.0, 2.4), 2.5)
        if g < G_c1:
            return "kenta", 3.0
        return (MERCHANT[0], MERCHANT[1], 2.6), 3.5

    def set_state(self, shot, g, f):
        q = quake(g)
        G.set_quake(q, frame=f)
        G.set_sway(1.0 * q, phase=2 * math.pi * 1.1 * g / 30.0, frame=f)

    def actors_at(self, shot, g):
        if shot == 14:
            return {}
        if g < G_b:
            return {"kenta": dict(pos=(KENTA_RUN_X, kenta_y(g), 0.0), pose=kenta_run(g), ppd=256)}
        if g < G_c1:
            return {"kenta": dict(pos=KENTA_B, pose=kenta_shout(g), ppd=256),
                    "merchant": dict(pos=MERCHANT, pose=merchant_pose(g), ppd=128),
                    "woman2": dict(pos=WOMAN2, pose=laugh_pose("woman2", g), ppd=128)}
        return {"merchant": dict(pos=MERCHANT, pose=merchant_pose(g), ppd=320)}


# ----------------------------------------------------------------------------- poses
def kenta_run(g):
    p = dict(cast4.STORY4["kenta_run_shout"][1])
    ph = 2 * math.pi * (g - G15) / 10.0                    # 3 strides a second
    legs = dict(p["legs"])
    legs["stride"] = 1.3 * math.sin(ph)
    legs["lift_l"] = 0.9 * max(0.0, math.cos(ph)); legs["lift_r"] = 0.9 * max(0.0, -math.cos(ph))
    legs.pop("knee_l", None)
    p["legs"] = legs
    p["squash"] = (1.0, 1.0 + 0.025 * math.cos(2 * ph))
    arm_l = dict(p["arm_l"]); arm_l["hand"] = (-0.5 + 0.22 * math.sin(ph), 0.82 - 0.08 * math.cos(ph)); p["arm_l"] = arm_l
    p["head_roll"] = -8 + 2 * math.sin(2 * ph)
    p["t"] = ((g - G15) % 20) / 20.0
    p["blink"] = blink(g, [1284])
    return p


def kenta_shout(g):
    p = dict(cast4.STORY4["kenta_run_shout"][1])
    p["mirror"] = True                                       # faces the doorways (screen-left)
    u = ease((g - G_b) / 6.0, "quad_out")
    p["legs"] = dict(preset="wide", spread=0.15)
    p["lean"] = lerp(14, 6, u) + 3 * math.sin((g - G_b) * 0.45)
    p["yaw"] = 0.75
    p["head_roll"] = -6 + 3 * math.sin((g - G_b) * 0.45)
    arm_l = dict(hand=(-0.45, 0.62 + 0.12 * math.sin((g - G_b) * 0.45)), bend=0.5, shape="open")   # beckoning hand
    p["arm_l"] = arm_l
    p["t"] = ((g - G_b) % 20) / 20.0
    p["blink"] = blink(g, [1322])
    return p


def merchant_pose(g):
    p = dict(cast4.STORY4["town_mock_shout"][1])
    p["mirror"] = True                                       # faces kenta (screen-left)
    p["legs"] = "stand"
    m = mouth_at(g, Q0, Q1)
    p["mouth"] = m if m is not None else "flat"
    u = ease((g - G_CUP) / 7.0, "back_out") if g >= G_CUP else 0.0
    cross_r, cross_l = (-0.18, 0.98), (0.18, 0.96)          # arms folded over the belly
    shr, shl = p["arm_r"]["hand"], p["arm_l"]["hand"]
    p["arm_r"] = dict(p["arm_r"], hand=lerp(cross_r, shr, u), bend=lerp(0.7, -0.8, u))
    p["arm_l"] = dict(p["arm_l"], hand=lerp(cross_l, shl, u), bend=lerp(-0.7, -0.5, u))
    if u < 0.5:
        p["arm_r"]["shape"] = "fist"; p["arm_l"]["shape"] = "fist"
    talk = m is not None
    p["lean"] = -4 + (-4 * u) + (2.5 * math.sin((g - Q0) * 0.4) if talk else 0)
    p["head_roll"] = 6 + (4 * math.sin((g - Q0) * 0.27) if talk else 1.5 * math.sin(g * 0.1))
    p["pitch"] = -0.4 if g >= G_CUP else -0.25
    p["blink"] = blink(g, [1330, 1360])
    return p


def laugh_pose(name, g):
    key = {"farmer": "town_laugh_point_farmer", "woman2": "town_laugh_point_woman2"}[name]
    p = dict(cast4.STORY4[key][1])
    p["mirror"] = False                                     # points screen-left, toward kenta
    off = 7 if name == "woman2" else 0
    bob = math.sin((g + off) * 0.75)
    p["squash"] = (1.0, 1.0 + 0.02 * bob)
    p["head_roll"] = -10 + 5 * bob
    p["lean"] = -5 + 3 * bob
    p["t"] = ((g + off) % 24) / 24.0
    return p


if __name__ == "__main__":
    B.main(Take14)
