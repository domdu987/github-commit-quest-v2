#!/usr/bin/env python3
"""shot.py -- film 7 take s18: shot 18 (58.80-62.62 s, g 1764..1878) + 6-frame handles (g 1758..1884).

    "ภาพไปไหน  หอคอยนอเทรอดามยังอยู่ครบ  แต่โมนาลิซ่าหายไปแล้ว" -- the callback to the director's boast:
      id 1  g 1758..1801  paris notre_dame_view, STREET_DUSK: the quai at dusk, Notre-Dame's two towers standing at the end, the gas
                          lamps lit; a lady strolls along the quai, a gentleman crosses; slow push in ("หอคอยนอเทรอ" 59.49)
      id 2  g 1802..1835  CUT: low angle from the quai, tilting up the west front to the two towers, still there ("ดามยังอยู่ครบ" 60.17)
      id 3  g 1836..1884  HARD CUT on "แต่โมนาลิซ่า" (61.11): louvre wall_eye, the director (top hat, monocle) before the empty wall
                          (four hooks), staring at it, then whips round to us, pale, sweating, hands up, shocked ("หายไปแล้ว" 61.89);
                          low angle, a quick punch-in on the turn
Mouths: nobody speaks (client rule): static expression mouths.  NO depth of field (common.Take).
    python3 shot.py probe|stills|final <ids> a:b[:step] ...   (engine.py)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine as E                                       # noqa: E402
from engine import C, L, cast7, lerp, clamp, blink, ez, Cast, Setup, walker, story   # noqa: E402

G0, G1, H = 1764, 1879, 6
R = {1: (1758, 1801), 2: (1802, 1835), 3: (1836, 1884)}


def keys_paris(g):
    return dict(papers=24, flames=1.0)          # the theft is known now (shot 18 on): her face on the kiosks (far behind this camera)


# ----------------------------------------------------------------------------- id 1: the quai at dusk
def cam1(g):
    u = ez((g - R[1][0]) / float(R[1][1] - R[1][0]))
    return (lerp(1.6, 1.9, u), lerp(38.5, 42.5, u), lerp(3.7, 3.55, u)), (lerp(3.0, 3.4, u), 108.0, lerp(12.0, 13.5, u)), 22.0


lady_pos, lady_pose = walker("lady", (-2.4, 55.5, 0), (0.055, 0.0, 0), R[1][0], 1, base=dict(expr="happy", yaw=0.7), period=30, speed=0.7)
gent_pos, gent_pose = walker("gentleman", (6.2, 57.5, 0), (-0.07, 0.0, 0), R[1][0], -1, base=dict(expr="neutral", yaw=0.7), period=27, speed=0.8)


# ----------------------------------------------------------------------------- id 2: tilt up the towers
def cam2(g):
    u = ez((g - R[2][0]) / float(R[2][1] - R[2][0]))
    return (lerp(1.2, 1.4, u), lerp(46.0, 47.0, u), 1.0), (lerp(4.6, 4.8, u), 108.0, lerp(12.0, 28.0, u)), 48.0


# ----------------------------------------------------------------------------- id 3: the director at the empty wall
DIR = (1.25, 19.55, 0.0)
G_TURN = C.g_of(61.45)             # he whips round between "แต่โมนาลิซ่า" and "หายไปแล้ว"


def dir_pose(g):
    if g < G_TURN:
        p = story("director_proud", mirror=True)
        p["yaw"] = 0.75
        p["gaze"] = (0.9, -0.4)
        p["pitch"] = -0.35
        p["expr"] = "stunned"
        p["arm_r"] = dict(hand=(0.3, 0.9), bend=0.5)
        p["arm_l"] = dict(hand=(-0.3, 0.9), bend=0.5)
        p["head_roll"] = 3.0 * math.sin(g * 0.4)
    else:
        u = ez((g - G_TURN) / 4.0)
        p = story("director_shocked")
        p["yaw"] = lerp(0.6, -0.1, u)
        p["lean"] = lerp(0.0, -6.0, u) + 0.8 * math.sin(g * 1.7)
        p["head_roll"] = 4.0 + 1.5 * math.sin(g * 2.3)          # trembling
        p["pale"] = lerp(0.3, 1.0, u)
    p["blink"] = blink(g, [G_TURN - 1])
    p["t"] = g / 30.0
    return p


def cam3(g):
    u = ez((g - G_TURN) / 5.0) if g >= G_TURN else 0.0
    d = (g - R[3][0]) / float(R[3][1] - R[3][0])
    loc = (lerp(0.15, 0.55, u), lerp(15.4, 16.6, u) + 0.2 * d, 1.75)
    look = (lerp(0.55, 0.95, u), 22.0, lerp(3.75, 3.35, u))
    return loc, look, lerp(22.0, 24.0, u)


SETUPS = {
    1: Setup("paris", "notre_dame_view", R[1], cam1, [
        Cast("lady", "lady", lady_pos, lady_pose, ppd=256),
        Cast("gent", "gentleman", gent_pos, gent_pose, ppd=256)], keys=keys_paris, lens=22.0),
    2: Setup("paris", "notre_dame_view", R[2], cam2, [], keys=keys_paris, lens=48.0),
    3: Setup("louvre", "wall_eye", R[3], cam3, [Cast("dir", "director", lambda g: DIR, dir_pose, ppd=320)],
             keys=lambda g: dict(mona=False, flames=1.0), lens=22.0),
}

if __name__ == "__main__":
    E.main(SETUPS, HERE, "s18")
