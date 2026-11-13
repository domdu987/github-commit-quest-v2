#!/usr/bin/env python3
"""shot.py -- film 7 take s16: shots 16-17 (51.19-58.80 s, g 1536..1763) + 6-frame handles (g 1530..1769), louvre / wall_eye area.

    shot 16 "ทั้งวันไม่มีใครสังเกต ยามเห็นผนังว่าง ก็นึกว่าช่างภาพยืมไปถ่ายรูป" -- the empty wall (four hooks, the unfaded patch), all day:
      id 1  g 1530..1576  wide on the empty wall: passers-by stride past in time-lapse, nobody looks; the guard at ease by the wall;
                          the skylight sun swings and warms (midday -> afternoon) -- light keyed per frame
      id 2  g 1577..1617  CUT on "ยามเห็นผนัง" (52.48): medium on the guard, he turns his head to the empty spot ("ว่าง" 53.23)
      id 3  g 1618..1663  CUT on "ก็นึกว่า" (53.48): punch-in, he turns to us and shrugs (the photographers took it); sunset gold,
                          the gas torcheres come up
    shot 17 "วันรุ่งขึ้น จิตรกรคนหนึ่งมาวาดรูปตรงนั้น แล้วถามว่า" -- next morning:
      id 4  g 1664..1712  CUT (55.46): morning light; the copyist painter (beret, palette) walks in to his easel before the empty wall
      id 5  g 1713..1769  CUT on "วาดรูป" (57.17): closer: he dabs at the easel, looks up, and points at the empty hooks, shocked
                          ("แล้วถามว่า" 58.13); out-handle g 1764..1769
Mouths: nobody speaks (client rule: mouths only on shot 6 / shot 9): static expression mouths only.  NO depth of field (common.Take).
    python3 shot.py probe|stills|final <ids> a:b[:step] ...   (engine.py)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine as E                                       # noqa: E402
from engine import C, L, cast7, lerp, clamp, blink, ez, Cast, Setup, walker, story, key_sun, key_grade   # noqa: E402

G0, G1, H = 1536, 1764, 6                                 # take [g0, g1) + handles
G16 = (1536, 1663)
G17 = (1664, 1763)
SPLIT = [G0 - H, 1577, 1618, 1664, 1713, G1 + H - 1]
R = {1: (1530, 1576), 2: (1577, 1617), 3: (1618, 1663), 4: (1664, 1712), 5: (1713, 1769)}

# ----------------------------------------------------------------------------- light: shot 16 = a day passing (midday -> sunset)
DAY = dict(rgb=(1.55, 1.30, 0.92), elev=57.0, travel=(0.22, 0.97), fill=1.0, fill_rgb=(1.0, 0.86, 0.66), flames=1.0, slope=(1.0, 0.985, 0.97))
EVE = dict(rgb=(1.60, 0.70, 0.30), elev=24.0, travel=(0.80, 0.60), fill=0.35, fill_rgb=(1.0, 0.60, 0.34), flames=1.9, slope=(0.98, 0.76, 0.56))


def day_u(g):
    return clamp((g - R[1][0]) / float(R[3][1] - R[1][0]))


def light16(take, f, g):
    u = ez(day_u(g), "sine")
    mix = lambda a, b: tuple(lerp(x, y, u) for x, y in zip(a, b))
    key_sun(take, f, mix(DAY["rgb"], EVE["rgb"]), lerp(DAY["elev"], EVE["elev"], u),
            travel=mix(DAY["travel"], EVE["travel"]), fill=lerp(DAY["fill"], EVE["fill"], u), fill_rgb=mix(DAY["fill_rgb"], EVE["fill_rgb"]))
    key_grade(take, f, mix(DAY["slope"], EVE["slope"]))


def keys16(g):
    return dict(mona=False, flames=lerp(DAY["flames"], EVE["flames"], ez(day_u(g), "sine")))


def keys17(g):
    return dict(mona=False, flames=1.0)


# ----------------------------------------------------------------------------- set-up 1: wide on the empty wall, time-lapse passers
GUARD = (1.85, 21.05, 0.0)


def guard_pose1(g):
    p = story("guard_at_ease", mirror=True, yaw=0.28)
    p["blink"] = blink(g, [1541, 1566])
    p["head_roll"] = 2.0 * math.sin(g * 0.15)
    p["t"] = g / 30.0
    return p


lady_pos, lady_pose = walker("lady", (-3.7, 17.6, 0), (0.17, 0.0, 0), R[1][0], 1, base=dict(expr="happy", yaw=0.7), period=16, speed=1.0)
gent_pos, gent_pose = walker("gentleman", (4.3, 16.4, 0), (-0.19, 0.0, 0), R[1][0], -1, base=dict(expr="neutral", yaw=0.7), period=15, speed=1.0)
lady2_pos, lady2_pose = walker("lady", (3.4, 19.0, 0), (-0.13, 0.0, 0), R[1][0], -1, base=dict(expr="neutral", yaw=0.7), period=17, speed=0.9, phase0=0.4)


def cam1(g):
    u = ez((g - R[1][0]) / float(R[1][1] - R[1][0]))
    return (lerp(0.95, 0.75, u), lerp(12.6, 13.3, u), 2.85), (lerp(0.25, 0.15, u), 22.0, 3.35), 21.0


# ----------------------------------------------------------------------------- set-up 2: the guard notices the empty spot
G_LOOK = C.g_of(53.0)          # turns his head toward the spot just before "ว่าง" (53.23)


def guard_pose2(g):
    u = ez((g - G_LOOK + 4) / 8.0)
    p = story("guard_at_ease", mirror=True)
    p["yaw"] = lerp(0.15, 0.62, u)
    p["gaze"] = (lerp(0.0, 0.9, u), lerp(0.0, -0.45, u))
    p["pitch"] = lerp(-0.15, -0.35, u)
    p["expr"] = "neutral" if g < G_LOOK + 6 else "unimpressed"
    p["head_roll"] = lerp(0.0, 7.0, u)
    p["blink"] = blink(g, [G_LOOK + 6])
    p["t"] = g / 30.0
    return p


def cam2(g):
    u = ez((g - R[2][0]) / float(R[2][1] - R[2][0]))
    return (lerp(0.55, 0.75, u), lerp(16.4, 16.9, u), 2.75), (lerp(0.75, 0.85, u), 22.0, 3.15), 24.0


# ----------------------------------------------------------------------------- set-up 3: punch-in, the shrug
G_SHRUG = C.g_of(54.08)        # "ช่างภาพยืมไป"


def guard_pose3(g):
    u = ez((g - (G_SHRUG - 10)) / 8.0)
    if g < G_SHRUG - 2:
        p = story("guard_at_ease", mirror=True)
        p["yaw"] = lerp(0.55, 0.12, u)
        p["gaze"] = (lerp(0.8, 0.0, u), lerp(-0.4, 0.0, u))
        p["expr"] = "unimpressed"
    else:
        p = story("guard_shrug", mirror=True)
        k = ez((g - (G_SHRUG - 2)) / 5.0)
        p["head_roll"] = lerp(0.0, 10.0, k)
        p["squash"] = (1.0, lerp(1.0, 0.98, k))
        p["yaw"] = 0.12
    p["blink"] = blink(g, [G_SHRUG - 2, 1656])
    p["t"] = g / 30.0
    return p


def cam3(g):
    u = ez((g - R[3][0]) / float(R[3][1] - R[3][0]))
    return (lerp(1.15, 1.25, u), lerp(17.6, 17.95, u), 2.68), (lerp(1.55, 1.6, u), 22.0, 2.72), 26.0


# ----------------------------------------------------------------------------- shot 17: next morning, the painter
EASEL = (-1.25, 19.5, 0.0)
PAINTER_STOP = (-2.65, 19.0, 0.0)
G_ARRIVE = 1696


def painter_pos4(g):
    x0 = -6.4
    if g >= G_ARRIVE:
        return PAINTER_STOP
    d = G_ARRIVE - g
    v = 0.115
    return (PAINTER_STOP[0] - v * (d if d > 4 else d * d / 8.0 + 2.0), PAINTER_STOP[1], 0.0) if d > 0 else PAINTER_STOP


def painter_pose4(g):
    if g < G_ARRIVE - 2:
        base = dict(expr="happy", yaw=0.6, prop_l="palette")
        p = cast7.cycle("painter", (g - R[4][0]) / 22.0, "walk", facing=1, base=base, arms="r", speed=lerp(0.9, 0.4, ez((g - (G_ARRIVE - 10)) / 8.0)))
        p["arm_l"] = dict(hand=(-0.25, 0.7), bend=0.6)
    else:
        u = ez((g - G_ARRIVE) / 10.0)
        p = story("painter_paint")
        p["yaw"] = lerp(0.6, 0.45, u)
        p["gaze"] = (0.9, lerp(0.0, -0.2, u))
    p["prop_l"] = "palette"
    p["blink"] = blink(g, [1680, 1706])
    p["t"] = g / 30.0
    return p


def cam4(g):
    u = ez((g - R[4][0]) / float(R[4][1] - R[4][0]))
    return (lerp(-2.4, -2.05, u), lerp(13.2, 13.9, u), 2.85), (lerp(-2.0, -1.6, u), 22.0, 3.3), 22.0


G_UP = C.g_of(57.62)            # "ตรงนั้น": looks up at the wall
G_POINT = C.g_of(58.13) - 2     # "แล้วถามว่า": the point


def painter_pose5(g):
    if g < G_UP:
        p = story("painter_paint")
        p["arm_r"] = dict(p["arm_r"], hand=(0.8 + 0.05 * math.sin(g * 0.9), 0.1 + 0.04 * math.sin(g * 1.3)))
        p["gaze"] = (0.9, 0.0)
    elif g < G_POINT:
        u = ez((g - G_UP) / 6.0)
        p = story("painter_paint")
        p["pitch"] = lerp(0.0, -0.4, u)
        p["gaze"] = (0.9, lerp(0.0, -0.7, u))
        p["expr"] = "neutral" if g < G_UP + 5 else "worried"
    else:
        u = ez((g - G_POINT) / 5.0)
        p = story("painter_point")
        p["arm_r"] = dict(p["arm_r"], stretch=lerp(1.0, 1.3, u))
        p["lean"] = lerp(0.0, 5.0, u)
    p["blink"] = blink(g, [G_UP + 4])
    p["t"] = g / 30.0
    return p


def cam5(g):
    u = ez((g - R[5][0]) / float(R[5][1] - R[5][0]))
    return (lerp(-2.85, -2.6, u), lerp(15.5, 16.1, u), 2.7), (lerp(-1.6, -1.45, u), 22.0, 3.3), 22.0


# ----------------------------------------------------------------------------- runtime dressing
_EASEL_CARD = {}


def dress_easel(take):
    png = C.svg_png(cast7.easel_svg("s16easel", canvas=True, painted=0.12)[0], (-0.9, -1.95, 0.9, 0.06), 260, os.path.join(HERE, "work", "svg"))
    card = C.PropCard("s16_easel", [png], (-0.9, -1.95, 0.9, 0.06), scale=1.25)
    loc, look, _ = take.cam_at(take.S.g[0])
    card.put(EASEL, face=tuple(loc))
    _EASEL_CARD["c"] = card


SH = ("sun_shafts",)            # the camera-only shaft sheets follow the built sun only: hidden while the sun moves (shot 16)

SETUPS = {
    1: Setup("louvre", "wall_eye", R[1], cam1, [
        Cast("guard", "guard", lambda g: GUARD, guard_pose1, ppd=256),
        Cast("lady", "lady", lady_pos, lady_pose, ppd=256),
        Cast("gent", "gentleman", gent_pos, gent_pose, ppd=256),
        Cast("lady2", "lady", lady2_pos, lady2_pose, ppd=224)],
        keys=keys16, frame_fx=light16, hide=SH, lens=21.0),
    2: Setup("louvre", "wall_eye", R[2], cam2, [Cast("guard", "guard", lambda g: GUARD, guard_pose2, ppd=320)],
             keys=keys16, frame_fx=light16, hide=SH, lens=24.0),
    3: Setup("louvre", "wall_eye", R[3], cam3, [Cast("guard", "guard", lambda g: GUARD, guard_pose3, ppd=384)],
             keys=keys16, frame_fx=light16, hide=SH, lens=26.0),
    4: Setup("louvre", "wall_eye", R[4], cam4, [Cast("painter", "painter", painter_pos4, painter_pose4, ppd=304)],
             keys=keys17, dress=dress_easel, lens=22.0),
    5: Setup("louvre", "wall_eye", R[5], cam5, [Cast("painter", "painter", lambda g: PAINTER_STOP, painter_pose5, ppd=336)],
             keys=keys17, dress=dress_easel, lens=24.0),
}

if __name__ == "__main__":
    E.main(SETUPS, HERE, "s16")
