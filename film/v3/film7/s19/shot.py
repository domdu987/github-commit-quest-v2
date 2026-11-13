#!/usr/bin/env python3
"""shot.py -- film 7 take s19: shots 19-20 (62.62-68.13 s, g 1879..2043) + 6-frame handles (g 1873..2049), louvre gallery.

    shot 19 "ลูฟวร์ปิดหนึ่งสัปดาห์ ตำรวจค้นทั้งตึก" -- the police search the Salon Carré in chaos:
      id 1  g 1873..1918  gallery_wide: policemen run across the salon in all directions, one searches under the divan with a
                          lantern, the guard waves them on; the empty wall far at the back; slow push
      id 2  g 1919..1964  CUT on "ตำรวจค้นทั้งตึก" (63.85): at the empty wall: an inspector crouches with his lantern at the four
                          hooks, a policeman runs through the foreground, the guard shrugs
    shot 20 "จับปิกัสโซไปสอบสวนด้วยซ้ำ แต่ไม่มีใครสงสัยไอ้มักกะโรนีเลย" -- the gallery corner as a make-shift office:
      id 3  g 1965..2004  CUT (65.50): the inspector questions a generic young painter (striped shirt; no name, no likeness) at a
                          little table with a lantern and papers; the painter, hands up, nervous
      id 4  g 2005..2049  CUT on "แต่ไม่มีใคร" (66.38): punch-in on the painter, indignant ("me?!"); behind him, small and unnoticed,
                          vincenzo strolls across the gallery, hands in pockets, and throws us a tiny smug look ("มักกะโรนีเลย" 67.41)
Plan deviation: shot 20 says "louvre / closet (as an office)": the closet is a 5 x 3.6 D box with no depth behind the actors, so
"vincenzo walks by in the background" is impossible there; staged in the gallery's service-door corner, dressed as an office instead.
Mouths: nobody speaks (client rule): static expression mouths only.  NO depth of field (common.Take).
    python3 shot.py probe|stills|final <ids> a:b[:step] ...   (engine.py)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine as E                                       # noqa: E402
from engine import C, L, cast7, lerp, clamp, blink, ez, Cast, Setup, walker, story   # noqa: E402
from mathutils import Vector                             # noqa: E402

G0, G1, H = 1879, 2044, 6
R = {1: (1873, 1918), 2: (1919, 1964), 3: (1965, 2004), 4: (2005, 2049)}


def keys(g):
    return dict(mona=False, flames=1.0)


def runner(cast, p0, vel, g0, facing, base=None, period=16.0):
    """a run cycle along a straight line (police in a hurry)."""
    p0, vel = Vector(p0), Vector(vel)

    def pos(g):
        return tuple(p0 + vel * (g - g0))

    def pose(g):
        p = cast7.cycle(cast, (g - g0) / period, "run", facing=facing, base=dict(base or {}), speed=1.0)
        p["t"] = g / 30.0
        return p
    return pos, pose


# ----------------------------------------------------------------------------- id 1: wide chaos
p1_pos, p1_pose = runner("police", (-5.0, 9.8, 0), (0.22, 0.0, 0), R[1][0], 1, base=dict(expr="determined", yaw=0.7))
p2_pos, p2_pose = runner("police", (6.8, 9.6, 0), (-0.24, 0.02, 0), R[1][0], -1, base=dict(expr="angry", yaw=0.7), period=15)
p3_pos, p3_pose = runner("police", (-2.0, 17.5, 0), (0.17, 0.0, 0), R[1][0] + 8, 1, base=dict(expr="determined", yaw=0.7), period=17)


def search_pose(g, mirror=False):
    p = story("police_search", mirror=mirror)
    p["arm_r"] = dict(p["arm_r"], hand=(0.78 + 0.08 * math.sin(g * 0.35), 0.55 + 0.05 * math.sin(g * 0.5)))
    p["gaze"] = (0.8, 0.6 + 0.1 * math.sin(g * 0.3))
    p["blink"] = blink(g, [1890, 1935, 1957])
    p["t"] = g / 30.0
    return p


def guard_wave(g):
    p = story("guard_shrug" if g > 1905 else "guard_at_ease", mirror=True)
    if g <= 1905:
        p["arm_l"] = dict(hand=(-0.85, -0.35 + 0.15 * math.sin(g * 0.6)), shape="open", bend=-0.5, stretch=1.3)
        p["expr"] = "worried"
        p["yaw"] = 0.35
    p["blink"] = blink(g, [1880, 1912])
    p["t"] = g / 30.0
    return p


def cam1(g):
    u = ez((g - R[1][0]) / float(R[1][1] - R[1][0]))
    return (lerp(5.6, 4.9, u), lerp(0.9, 2.2, u), 3.4), (lerp(-2.6, -2.2, u), 21.0, 4.0), 22.0


# ----------------------------------------------------------------------------- id 2: at the empty wall
INSP = (-1.35, 20.95, 0.0)
GUARD2 = (2.05, 21.05, 0.0)
p4_pos, p4_pose = runner("police", (-4.0, 18.8, 0), (0.24, 0.0, 0), R[2][0] + 12, 1, base=dict(expr="determined", yaw=0.7), period=15)


def cam2(g):
    u = ez((g - R[2][0]) / float(R[2][1] - R[2][0]))
    return (lerp(1.0, 0.75, u), lerp(14.9, 15.6, u), 2.75), (lerp(-0.1, -0.2, u), 22.0, 3.05), 22.0


def guard2_pose(g):
    p = story("guard_shrug", mirror=True)
    p["head_roll"] = 10.0 + 3.0 * math.sin(g * 0.3)
    p["blink"] = blink(g, [1930, 1950])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- shot 20: the corner office
YP = (3.6, 6.3, 0.0)            # the young painter
COP = (5.95, 6.45, 0.0)          # the inspector
TABLE = (4.8, 6.75)
COP_MIRROR = False
G_INDIG = C.g_of(65.94) + 2       # "ด้วยซ้ำ": he flares up (seen in id 3's last beat and all of id 4)


def yp_pose(g):
    if g < G_INDIG:
        p = story("young_painter_questioned")
        p["head_roll"] = 8.0 + 2.0 * math.sin(g * 0.9)
    else:
        u = ez((g - G_INDIG) / 5.0)
        p = story("young_painter_indignant")
        p.pop("fx", None)                 # the anger_fill fx is purple-magenta on this cast (colour rule): plain furious face instead
        p["expr"] = "furious"
        p["head_roll"] = lerp(8.0, -8.0, u)
        p["lean"] = lerp(-4.0, -6.0, u) + 1.0 * math.sin(g * 1.1)
    p["blink"] = blink(g, [1975, G_INDIG - 1, 2030])
    p["t"] = g / 30.0
    return p


def cop_pose(g):
    p = story("police_question", mirror=COP_MIRROR)
    p["arm_l"] = dict(p["arm_l"], hand=(-0.92 + 0.06 * math.sin(g * 0.7), 0.3 + 0.04 * math.sin(g * 0.45)))
    p["blink"] = blink(g, [1985, 2020])
    p["t"] = g / 30.0
    return p


VIN0, VIN_V, G_VIN = Vector((-0.6, 14.4, 0.0)), Vector((0.075, 0.0, 0.0)), 1990
G_GLANCE = C.g_of(67.41)


def vin_pos(g):
    return tuple(VIN0 + VIN_V * (g - G_VIN))


def vin_pose(g):
    k = ez((g - G_GLANCE) / 6.0) if g >= G_GLANCE else 0.0
    base = dict(expr="smug", yaw=lerp(0.7, 0.35, k), gaze=(lerp(0.3, -0.1, k), 0.0), pitch=-0.15)
    p = cast7.cycle("vincenzo", (g - G_VIN) / 30.0, "walk", facing=1, base=base, arms="none" if False else "both", speed=0.7)
    p["arm_r"] = dict(hand=(0.28, 1.45), bend=0.5, shape="fist", layer="back")    # hands in pockets
    p["arm_l"] = dict(hand=(-0.28, 1.45), bend=0.5, shape="fist", layer="front")
    p["blink"] = blink(g, [G_GLANCE - 1])
    p["t"] = g / 30.0
    return p


def cam3(g):
    u = ez((g - R[3][0]) / float(R[3][1] - R[3][0]))
    return (lerp(6.6, 6.35, u), lerp(1.2, 1.7, u), 2.8), (lerp(2.4, 2.6, u), 14.0, 2.45), 22.0


def cam4(g):
    u = ez((g - R[4][0]) / float(R[4][1] - R[4][0]))
    return (lerp(5.2, 5.05, u), lerp(3.3, 3.75, u), 2.62), (lerp(1.9, 1.7, u), 14.0, 2.55), 24.0


def dress_office(take):
    """runtime: a little table with a lantern, papers and an ink pot between the inspector and the painter (louvre helpers)."""
    S = L.STATE; M = S['M']; SET = S['SET']
    mb, fl, cards = L.MB(), L.MB(), L.MB()
    x, y = TABLE
    mb.box((x - 0.75, y - 0.45, 1.45), (x + 0.75, y + 0.45, 1.58), M['wood_d'])
    for sx in (-0.65, 0.65):
        for sy in (-0.37, 0.37):
            L.rod(mb, (x + sx, y + sy, 0.0), (x + sx, y + sy, 1.45), 0.05, M['wood_d'], seg=6)
    for k in range(3):
        mb.box((x - 0.45 + 0.2 * k, y - 0.3 + 0.05 * k, 1.58 + 0.008 * k), (x - 0.0 + 0.2 * k, y + 0.2 + 0.05 * k, 1.586 + 0.008 * k), M['plaque'])
    L.rod(mb, (x + 0.15, y + 0.25, 1.58), (x + 0.15, y + 0.25, 1.7), 0.06, M['black'], seg=8)
    f = L._lantern(mb, fl, cards, (x + 0.5, y + 0.1, 1.58), M, hang=False, s=0.7)
    L._flame_light('s19_lantern', tuple(f), L.LANTERN, 50.0, radius=0.12, shadow=False)
    L._obj(mb, 's19_dressing', SET, hull=0.012); L._obj(fl, 's19_glow', SET, shadow=False); L._obj(cards, 's19_halos', SET, shadow=False)
    for ob in SET.objects:
        if ob.name.startswith('s19_'):
            L.no_bounce(ob)


SETUPS = {
    1: Setup("louvre", "gallery_wide", R[1], cam1, [
        Cast("cop1", "police", p1_pos, p1_pose, ppd=192),
        Cast("cop2", "police", p2_pos, p2_pose, ppd=192),
        Cast("cop3", "police", p3_pos, p3_pose, ppd=160),
        Cast("search", "police", lambda g: (-2.4, 10.4, 0.0), lambda g: search_pose(g, mirror=False), ppd=192),
        Cast("guard", "guard", lambda g: (3.2, 9.4, 0.0), guard_wave, ppd=192)],
        keys=keys, lens=22.0),
    2: Setup("louvre", "wall_eye", R[2], cam2, [
        Cast("insp", "police", lambda g: INSP, lambda g: search_pose(g), ppd=288),
        Cast("guard", "guard", lambda g: GUARD2, guard2_pose, ppd=256),
        Cast("cop", "police", p4_pos, p4_pose, ppd=320, vis=lambda g: g >= R[2][0] + 12)],
        keys=keys, lens=22.0),
    3: Setup("louvre", "gallery_wide", R[3], cam3, [
        Cast("yp", "young_painter", lambda g: YP, yp_pose, ppd=320),
        Cast("cop", "police", lambda g: COP, cop_pose, ppd=320),
        Cast("vin", "vincenzo", vin_pos, vin_pose, ppd=192, vis=lambda g: g >= G_VIN)],
        keys=keys, dress=dress_office, lens=22.0),
    4: Setup("louvre", "gallery_wide", R[4], cam4, [
        Cast("yp", "young_painter", lambda g: YP, yp_pose, ppd=352),
        Cast("vin", "vincenzo", vin_pos, vin_pose, ppd=224)],
        keys=keys, dress=dress_office, lens=24.0),
}

if __name__ == "__main__":
    E.main(SETUPS, HERE, "s19")
