#!/usr/bin/env python3
"""shot.py -- film 4 takes s09 / s10 / s11 (shots 9-12, the three yearly quakes), pagoda set v2.  This file holds the whole
engine of the three takes; s10/shot.py and s11/shot.py only load it (same cameras, quake clock and set state everywhere).

  take s09 = shot 9  (g 593..709)  quake 1, DAY
      9a  g 593..628  two_buildings wide: master smug before his still tower, kenta at the pagoda; quake starts g 603, the
                      pagoda begins to sway, lanterns swing, camera shakes; slow push (ref a t0039)
      9b  g 629..661  hard cut, insert: a tea cup on a sill of the tower, the tea perfectly still (no ripple) while the pagoda
                      sways soft in the background ("หอของช่างใหญ่นิ่งสนิท" g 644)  (ref a t0043: the wine cup)
      9c  g 662..709  hard cut, low up-shot of the pagoda: storeys swaying opposite ways, one hand-span (amp 0.5);
                      punch-in g 688..695 to the upper storeys, lands on "หนึ่งคืบ" g 696  (ref a t0041: insert)
  take s10 = shot 10 (g 710..781)  nickname, DAY: merchant / woman2 / farmer point at the still-rocking pagoda and laugh
                      ("หัวเราะลั่น" g 726); snap punch-in g 752..759 onto merchant + woman2 before "เจดีย์เมา" g 766 (ref a t0047)
  take s11 = shots 11 + 12 (g 782..1054)
      11a g 782..835  DAY, low wide on both buildings: quake 2 ("ปีที่สอง" g 786), pagoda sways two spans (amp 0.85); snap toward
                      the pagoda g 816..824, lands on "สองคืบ" g 825  (ref a t0049)
      11b g 836..876  hard cut, crack insert: the hairline crack appears at the joint g 856 ("ร้าว") (ref a t0051)
      11c g 877..919  hard cut, medium: the master on a scaffold plank plasters it (patch at g 897, "ฉาบปูนปิด" g 889) (t0053)
      12a g 920..971  10-frame dissolve (g 915..924) to SUNSET: wide, quake 3 ("ปีที่สาม" g 922), three spans (amp 1.2);
                      snap g 952..959, lands on "สามคืบ" g 960  (ref a t0061 / t0063, sunset hill)
      12b g 972..1015 hard cut, crack insert: the crack is finger-wide through the old patch ("รอยร้าวกว้าง" g 973); the
                      master's finger pokes into it g 990..1006 ("จนยัดนิ้วได้" g 996)
      12c g 1016..1054 hard cut, medium low: he plasters over it again, second patch g 1036 ("อีกชั้น" g 1041) (ref a t0065)
Handles: 7 frames rendered in 3D before / after every take (10-frame dissolves), and 7 each side of the 11 -> 12 dissolve.
Blender frame of (sub-shot index i, film frame g) = 2000 * i + g + 1.  Mouths never move (no quoted line in shots 9-12).

    python3 shot.py probe <sub,...> a:b[:step]
    python3 shot.py stills <sub,...> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <sub,...> a:b[:step] [scale] [samples]      (raw/<sub>/g_%04d.png + .json, in the take folder)
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast4"), os.path.join(V3, "stage"), os.path.join(V3, "set3d4"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast4                                            # noqa: E402  (first)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import pagoda as G                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402


def g_of(t):
    return int(round((t + 0.10) * 30))


# ----------------------------------------------------------------------------- timing (narration_bankky / captions_bankky)
H = 7                                                       # handle frames (10-frame dissolves)
G9, G10, G11, G12, G13 = 593, 710, 782, 920, 1055           # round(t*30) of 19.78, 23.65, 26.07, 30.67, 35.18
DISS = 10
SUBS = [  # name, shot, preset, first g (incl. handle), last g (incl. handle), take
    ("9a", 9, "DAY", G9 - H, 628, "s09"), ("9b", 9, "DAY", 629, 661, "s09"), ("9c", 9, "DAY", 662, G10 - 1 + H, "s09"),
    ("10", 10, "DAY", G10 - H, G11 - 1 + H, "s10"),
    ("11a", 11, "DAY", G11 - H, 835, "s11"), ("11b", 11, "DAY", 836, 876, "s11"), ("11c", 11, "DAY", 877, G12 - 1 + H, "s11"),
    ("12a", 12, "SUNSET", G12 - H, 971, "s11"), ("12b", 12, "SUNSET", 972, 1015, "s11"), ("12c", 12, "SUNSET", 1016, G13 - 1 + H, "s11")]
SUB = {s[0]: dict(i=k + 1, shot=s[1], preset=s[2], r=(s[3], s[4]), take=s[5]) for k, s in enumerate(SUBS)}

E = dict(year1=g_of(19.76), quake1=g_of(20.0), tower_still=g_of(21.38), but=g_of(21.97), span1=g_of(23.09),
         town=g_of(23.64), laugh=g_of(24.11), call=g_of(24.76), drunk=g_of(25.45),
         year2=g_of(26.11), sway2=g_of(26.58), span2=g_of(27.4), crack=g_of(28.44), hair=g_of(29.16), plaster1=g_of(29.54),
         year3=g_of(30.65), sway3=g_of(31.13), span3=g_of(31.9), wide=g_of(32.32), finger=g_of(33.1), plaster2=g_of(33.83),
         layer=g_of(34.59))
# 596 603 644 662 696 | 712 726 746 766 | 786 800 825 856 878 889 | 922 937 960 973 996 1018 1041


def bf(sub, g):
    return 2000 * SUB[sub]["i"] + int(g) + 1


# ----------------------------------------------------------------------------- the quake clock (continuous in g)
def quake(g):
    """strength 0..1 of the ground shaking at film frame g."""
    q1 = 0.45 * ease((g - 600) / 14.0, "sine") * (1 - ease((g - 700) / 24.0, "sine"))
    q2 = 0.75 * ease((g - 784) / 14.0, "sine") * (1 - ease((g - 872) / 22.0, "sine"))
    q3 = 1.00 * ease((g - 920) / 14.0, "sine") * (1 - ease((g - 986) / 22.0, "sine"))
    return max(q1, q2, q3)


def sway_amp(g):
    """sway amplitude (D at the top storey): one span 0.5, two spans 0.85, three spans 1.2; rocks on after each quake."""
    a1 = 0.5 * ease((g - 603) / 22.0, "sine") * (1 - 0.75 * ease((g - 702) / 70.0, "sine"))
    a1 *= 1 - ease((g - 778) / 8.0, "sine")
    a2 = 0.85 * ease((g - 788) / 22.0, "sine") * (1 - ease((g - 868) / 40.0, "sine"))
    a3 = 1.2 * ease((g - 924) / 22.0, "sine") * (1 - ease((g - 984) / 36.0, "sine"))
    return max(a1, a2, a3)


SWAY_HZ = 1.1


def sway_phase(g):
    return 2 * math.pi * SWAY_HZ * g / 30.0


def crack_level(g):
    if g < E["crack"]:
        return 0
    return 1 if g < G12 else 2


def plaster_level(g):
    if g < 897:
        return 0
    return 1 if g < 1036 else 2


def shake_vec(g, amp):
    """deterministic hand-held quake shake: (d loc, d look) in D for strength amp."""
    s = lambda f, ph: math.sin(2 * math.pi * f * g / 30.0 + ph)
    dl = Vector((s(5.3, 0.3) + 0.5 * s(8.9, 1.7), 0.3 * s(4.1, 2.2), s(6.7, 0.9) + 0.4 * s(11.3, 2.9)))
    dk = Vector((s(4.7, 1.1) + 0.4 * s(9.7, 0.4), 0.0, s(5.9, 2.4) + 0.5 * s(7.9, 0.6)))
    return dl * amp, dk * amp


# ----------------------------------------------------------------------------- cameras
def _pk(a, b):
    return tuple(a) + tuple(b)


def V(*a):
    return Vector(a)


def _kc(g, ks):
    k = keys(g, ks)
    return Vector(k[:3]), Vector(k[3:6])


TB = (V(6.9, -31.0, 3.4), V(7.4, 0.0, 9.6))                 # the set's two_buildings
CUP = V(11.95, -3.12, 3.18)                                 # tea cup on the tower sill (base centre)
SCAF_Z = 9.12                                               # scaffold plank top
MASTER_SCAF = (12.25, -4.02, SCAF_Z)                        # master standing on the plank, west of the joint
JX, JY, JZ = G.JOINT
CAM = {}


def cam_9a(g):
    a, b = G9 - H, 628
    l, k = _kc(g, [(a, _pk(V(6.95, -31.6, 3.25), V(7.35, 0.0, 9.5)), "sine"), (b + 1, _pk(V(6.85, -30.0, 3.45), V(7.3, 0.0, 9.9)), "hold")])
    dl, dk = shake_vec(g, 0.012 * quake(g)); return l + dl, k + dk * 2, 22        # small: the tower must read still


def cam_9b(g):
    a, b = 629, 661
    l, k = _kc(g, [(a, _pk(CUP + V(-1.05, -1.0, 0.78), CUP + V(0.55, 0.42, 0.02)), "sine"),
                   (b + 1, _pk(CUP + V(-0.86, -0.82, 0.66), CUP + V(0.55, 0.42, 0.04)), "hold")])
    return l, k, 35


def cam_9c(g):
    a, b = 662, G10 - 1 + H
    ks = [(a, _pk(V(-0.75, -14.6, 1.25), V(0.0, 0.0, 11.0)), "sine"), (688, _pk(V(-0.7, -14.2, 1.3), V(0.0, 0.0, 11.4)), "quint"),
          (696, _pk(V(-0.45, -11.4, 2.2), V(0.0, 0.0, 14.2)), "sine"), (b + 1, _pk(V(-0.42, -11.1, 2.25), V(0.0, 0.0, 14.4)), "hold")]
    l, k = _kc(g, ks)
    dl, dk = shake_vec(g, 0.04 * quake(g)); return l + dl, k + dk * 3, 22


TOWN10 = {"merchant": (1.0, -15.6, 0.0), "woman2": (2.4, -16.2, 0.0), "farmer": (-0.25, -14.6, 0.0)}


def cam_10(g):
    a, b = G10 - H, G11 - 1 + H
    ks = [(a, _pk(V(0.4, -22.3, 2.05), V(0.45, -12.0, 3.9)), "sine"), (752, _pk(V(0.42, -21.9, 2.05), V(0.5, -12.0, 3.95)), "quint"),
          (759, _pk(V(1.0, -20.2, 2.1), V(1.25, -12.0, 3.75)), "sine"), (b + 1, _pk(V(1.0, -19.95, 2.1), V(1.25, -12.0, 3.8)), "hold")]
    return _kc(g, ks) + (22,)


def cam_11a(g):
    a, b = G11 - H, 835
    ks = [(a, _pk(V(3.2, -27.0, 1.7), V(5.6, 0.0, 10.4)), "sine"), (816, _pk(V(3.0, -26.3, 1.75), V(5.4, 0.0, 10.6)), "quint"),
          (824, _pk(V(1.0, -20.0, 2.2), V(0.6, 0.0, 12.6)), "sine"), (b + 1, _pk(V(0.95, -19.6, 2.25), V(0.6, 0.0, 12.8)), "hold")]
    l, k = _kc(g, ks)
    dl, dk = shake_vec(g, 0.05 * quake(g)); return l + dl, k + dk * 4, 22


def cam_11b(g):
    a, b = 836, 876
    ks = [(a, _pk(V(JX + 0.25, -5.75, JZ + 0.18), V(JX, JY, JZ)), "sine"), (b + 1, _pk(V(JX + 0.2, -5.0, JZ + 0.12), V(JX, JY, JZ)), "hold")]
    l, k = _kc(g, ks)
    dl, dk = shake_vec(g, 0.012 * quake(g) + 0.02 * pulse(g, 855, 857, 864, 1.0)); return l + dl, k + dk * 2, 22


def cam_11c(g):
    a, b = 877, G12 - 1 + H
    ks = [(a, _pk(V(10.9, -10.4, 10.0), V(12.75, -3.0, 11.15)), "sine"), (b + 1, _pk(V(11.2, -9.6, 10.15), V(12.8, -3.0, 11.15)), "hold")]
    return _kc(g, ks) + (22,)


def cam_12a(g):
    a, b = G12 - H, 971
    ks = [(a, _pk(V(-1.0, -30.0, 1.4), V(7.0, 0.0, 10.4)), "sine"), (952, _pk(V(-0.9, -29.4, 1.45), V(6.9, 0.0, 10.6)), "quint"),
          (959, _pk(V(0.2, -19.2, 2.1), V(0.2, 0.0, 12.4)), "sine"), (b + 1, _pk(V(0.2, -18.8, 2.15), V(0.2, 0.0, 12.6)), "hold")]
    l, k = _kc(g, ks)
    dl, dk = shake_vec(g, 0.06 * quake(g)); return l + dl, k + dk * 4, 22


def cam_12b(g):
    a, b = 972, 1015
    ks = [(a, _pk(V(JX - 0.95, -8.0, JZ + 0.3), V(JX - 0.75, JY, JZ + 0.1)), "sine"),
          (b + 1, _pk(V(JX - 0.85, -7.3, JZ + 0.28), V(JX - 0.7, JY, JZ + 0.1)), "hold")]
    l, k = _kc(g, ks)
    dl, dk = shake_vec(g, 0.012 * quake(g)); return l + dl, k + dk * 2, 22


def cam_12c(g):
    a, b = 1016, G13 - 1 + H
    ks = [(a, _pk(V(14.1, -9.2, 9.35), V(12.6, -3.0, 11.45)), "sine"), (b + 1, _pk(V(13.85, -8.6, 9.45), V(12.6, -3.0, 11.45)), "hold")]
    return _kc(g, ks) + (22,)


CAMS = {"9a": cam_9a, "9b": cam_9b, "9c": cam_9c, "10": cam_10, "11a": cam_11a, "11b": cam_11b, "11c": cam_11c,
        "12a": cam_12a, "12b": cam_12b, "12c": cam_12c}


# ----------------------------------------------------------------------------- poses
def master_smug(g):
    p = dict(cast4.STORY4["master_arms_crossed"][1])
    p["head_roll"] = -4 + 2 * math.sin(g * 0.09)
    p["blink"] = blink(g, [606, 640])
    p["lean"] = 1.5 * math.sin(g * 0.07)
    return p


def kenta_9a(g):
    p = dict(cast4.STORY4["kenta_determined"][1])
    u = ease((g - 606) / 8.0, "sine")
    p["yaw"] = lerp(0.3, -0.45, u); p["pitch"] = lerp(0.0, -0.5, u); p["gaze"] = (lerp(0.0, -0.6, u), lerp(0.0, -0.7, u))
    p["expr"] = "determined"
    p["blink"] = blink(g, [598, 620])
    return p


def town10(name, g):
    sfx = {"merchant": "", "woman2": "_woman2", "farmer": "_farmer"}[name]
    p = dict(cast4.STORY4["town_laugh_point" + sfx][1])
    off = {"merchant": 0, "woman2": 3, "farmer": 6}[name]
    start = E["laugh"] - 10 + off
    u = ease((g - start) / 7.0, "back_out") if g >= start else 0.0
    if name == "woman2":
        p["mirror"] = False                              # all three point screen-left, at the pagoda
        p["yaw"] = 0.35; p["head_roll"] = -10; p["lean"] = -5
    bounce = math.sin(2 * math.pi * (g - start) / 9.0) * u        # belly laugh bounce (body only, the grin is fixed)
    p["squash"] = (1.0 - 0.02 * bounce, 1.0 + 0.025 * bounce)
    p["head_roll"] = p.get("head_roll", 0) + 4 * bounce
    p["lean"] = p.get("lean", 0) - 3 * u
    hand0 = (-0.30, 0.90)
    pt = p["arm_l"]["hand"]
    jab = pulse(g, E["drunk"] - 4 + off, E["drunk"] + off, E["drunk"] + 8 + off, 1.0)
    al = dict(p["arm_l"]); al["hand"] = (lerp(hand0[0], pt[0] - 0.06 * jab, u), lerp(hand0[1], pt[1] - 0.05 * jab, u))
    al["shape"] = "point" if u > 0.35 else "fist"; p["arm_l"] = al
    if u < 0.3:                                          # before the laugh: a plain amused look, mouth closed
        p["expr"] = "smirk"; p.pop("fx", None)
    p["t"] = (g % 30) / 30.0
    p["blink"] = 0 if u >= 0.3 else blink(g, [705 + off])
    return p


def master_plaster(g, g0, g_patch):
    base = cast4.STORY4["master_plaster"][1]
    p = dict(base)
    st = 0.5 - 0.5 * math.cos(2 * math.pi * (g - g0) / 12.0)          # trowel strokes, one every 12 frames
    p["head_roll"] = -3 + 2 * st
    p["lean"] = 4 + 2 * st
    p["blink"] = blink(g, [g0 + 9, g0 + 33])
    p["expr"] = "determined" if g < g_patch + 4 else "smug"
    return p, st


def master_poke(g):
    p = dict(cast4.STORY4["master_plaster"][1])
    p.pop("prop_r", None)
    p["expr"] = "worried"; p["fx"] = ["sweat"]
    p["yaw"] = 0.65; p["gaze"] = (0.9, 0.1); p["head_roll"] = -4
    p["arm_r"] = dict(hand=(0.80, 0.30), bend=-0.5, shape="point", stretch=1.3)
    p["blink"] = blink(g, [980, 1010])
    return p


# ----------------------------------------------------------------------------- shot-only set pieces
def _ensure_coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def build_cup():
    """Tea cup on a wooden sill on the tower's south face near its west corner (shot 9b)."""
    coll = _ensure_coll("S09_CUP"); C = G.STATE["C"]
    mb = G.MB()
    wood = C("#6a4228"); wood_d = C("#3e2618")
    sx0, sx1 = 11.62, 12.36
    mb.box((sx0, -3.42, CUP.z - 0.14), (sx1, -2.6, CUP.z), wood)                 # sill board
    mb.box((sx0, -3.44, CUP.z - 0.30), (sx1, -2.6, CUP.z - 0.14), wood_d)        # its bracket band
    sill = mb.obj("s09_sill", coll, hull=0.012)
    cup = G.MB()
    clay = C("#efe6d0"); band = C("#2e4a8a"); inner = C("#e2d8c0"); tea = C("#8a6a1c"); hi = C("#fffaf0")
    c = CUP
    cup.frustum((c.x, c.y, c.z), (c.x, c.y, c.z + 0.04), 0.085, 0.085, clay, seg=24)            # foot ring
    cup.frustum((c.x, c.y, c.z + 0.04), (c.x, c.y, c.z + 0.20), 0.105, 0.16, clay, seg=28, cap1=False)
    cup.frustum((c.x, c.y, c.z + 0.20), (c.x, c.y, c.z + 0.235), 0.16, 0.168, band, seg=28, cap0=False, cap1=False)     # blue rim band
    cup.frustum((c.x, c.y, c.z + 0.235), (c.x, c.y, c.z + 0.245), 0.168, 0.166, inner, seg=28, cap0=False, cap1=False)
    co = cup.obj("s09_cup", coll, hull=0.008)
    tm = G.MB()
    zt = c.z + 0.205
    tm.frustum((c.x, c.y, zt - 0.03), (c.x, c.y, zt), 0.150, 0.152, tea, seg=28)               # tea, dead flat
    hx, hy = c.x - 0.04, c.y - 0.03                                                              # still reflection highlight
    tm.frustum((hx, hy, zt), (hx, hy, zt + 0.003), 0.04, 0.04, hi, seg=16)
    to = tm.obj("s09_tea", coll)
    for o in (sill, co, to):
        T.no_bounce(o)
    return [sill, co, to]


def build_scaffold():
    """Plank scaffold in front of the tower's joint (shots 11c / 12b / 12c): poles, lashed ledgers, a plank, a plaster bucket."""
    coll = _ensure_coll("S11_SCAF"); C = G.STATE["C"]
    mb = G.MB()
    pole = C("#8a6a44"); plank = C("#b08a5a"); rope = C("#d8c69a"); bucket = C("#5a4030"); plaster = C("#f2eee4")
    z = SCAF_Z
    mb.box((10.5, -4.55, z - 0.12), (15.9, -3.58, z), plank)
    for x in (10.75, 15.65):
        for y in (-4.45,):
            mb.frustum((x, y, 0.0), (x, y, z + 3.6), 0.09, 0.075, pole, seg=8)
            mb.frustum((x, y, z - 0.35), (x, y, z - 0.15), 0.13, 0.13, rope, seg=8)
        mb.frustum((x, -4.45, z - 0.2), (x, -2.62, z - 0.2), 0.07, 0.07, pole, seg=6)          # ledger to the wall
    mb.frustum((10.6, -4.45, z + 1.15), (15.8, -4.45, z + 1.15), 0.06, 0.06, pole, seg=6)      # guard rail (low, behind the legs)
    mb.frustum((10.6, -4.45, z - 0.2), (15.8, -4.45, z - 0.2), 0.07, 0.07, pole, seg=6)
    mb.frustum((14.6, -3.95, z), (14.6, -3.95, z + 0.42), 0.2, 0.24, bucket, seg=14)
    mb.frustum((14.6, -3.95, z + 0.42), (14.6, -3.95, z + 0.44), 0.235, 0.235, plaster, seg=14)
    ob = mb.obj("s11_scaffold", coll, hull=0.015)
    T.no_bounce(ob)
    return [ob]


# ----------------------------------------------------------------------------- the take
def wanted(sub):
    """actors visible in a sub-shot."""
    return {"9a": ["master"], "10": ["merchant", "woman2", "farmer"], "11c": ["master"], "12b": ["master"],
            "12c": ["master"]}.get(sub, [])


PLACE = {"9a": {"kenta": (-1.6, -11.5, 0.0), "master": (9.6, -10.8, 0.0)},
         "10": TOWN10, "11c": {"master": MASTER_SCAF}, "12b": {"master": MASTER_SCAF}, "12c": {"master": MASTER_SCAF}}
PPD = {"9a": 128, "10": 384, "11c": 384, "12b": 512, "12c": 384}
DOF = {"9a": (None, None), "9b": ("cup", 2.2), "9c": (None, None), "10": ("merchant", 2.5), "11a": (None, None),
       "11b": ((JX, JY, JZ), 2.5), "11c": ("master", 3.0), "12a": (None, None), "12b": ((JX, JY, JZ), 3.0), "12c": ("master", 3.0)}


class Take(object):
    def __init__(self, preset="DAY", quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.preset = preset
        self.scene = scene = bpy.context.scene
        self.A = G.build(preset)
        G.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 30000
        self.cup = build_cup()
        self.scaf = build_scaffold()
        self.cam = camrig.make_camera(scene, name="cam_s09")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 400
        sd = os.path.join(HERE, "work", "sprites")
        self.act = {}
        for n in ("kenta", "master", "merchant", "woman2", "farmer"):
            a = actors.Actor(n, n); a.build(sprites.DEFAULT_CANVAS[n], sd, contact=True); self.act[n] = a
            a.head_flip = False                  # DAY / SUNSET key from the south-west / west: screen-left in every view here
            T.no_bounce(a.card)
        self.anch = {}
        self.pin = {}
        if verbose:
            print("take: %s built in %.1f s" % (preset, time.time() - t0), flush=True)

    def visible(self, sub):
        w = wanted(sub)
        for n, a in self.act.items():
            a.set_hidden(n not in w)
        for o in self.cup:
            o.hide_render = sub not in ("9b",)
        for o in self.scaf:
            o.hide_render = sub not in ("11b", "11c", "12b", "12c")

    def set_state(self, g, f):
        G.set_sway(sway_amp(g), sway_phase(g), frame=f)
        G.set_quake(quake(g), frame=f)
        G.set_crack(crack_level(g), frame=f)
        G.set_plaster(plaster_level(g), frame=f)

    def pose(self, sub, gs):
        self.visible(sub)
        for g in gs:
            f = bf(sub, g)
            loc, look, lens = CAMS[sub](g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")
            for n, xyz in PLACE.get(sub, {}).items():
                self.act[n].place(f, xyz)
            self.set_state(g, f)
        for g in gs:
            f = bf(sub, g)
            self.scene.frame_set(f)
            if sub == "9a":
                self.act["kenta"].pose(f, kenta_9a(g), camera=self.cam)
                self.act["master"].pose(f, master_smug(g), camera=self.cam)
            elif sub == "10":
                for n in ("merchant", "woman2", "farmer"):
                    self.act[n].pose(f, town10(n, g), camera=self.cam)
            elif sub in ("11c", "12c"):
                g0, gp = (877, 897) if sub == "11c" else (1016, 1036)
                p, st = master_plaster(g, g0, gp)
                tip = (JX - 0.05 + 0.10 * math.sin((g - g0) * 0.26), JY - 0.03, JZ - 0.28 + 0.42 * st)
                _, info = self.act["master"].pose(f, p, hands={"r": {"tip": tip, "prop": "plaster_trowel",
                                                                     "angle": p["prop_r"]["angle"], "stretch": 1.3}}, camera=self.cam)
                self.pin[f] = info.get("r", {}).get("error")
            elif sub == "12b":
                p = master_poke(g)
                u = ease((g - 984) / 10.0, "sine") * (1 - ease((g - 1004) / 8.0, "sine"))
                poke = pulse(g, 994, 997, 1003, 1.0)
                rest = (JX - 1.0, JY - 0.4, JZ - 0.9)
                tgt = (JX + 0.02, JY + 0.12 * poke, JZ + 0.02)
                hand = tuple(lerp(rest[k], tgt[k], u) for k in range(3))
                _, info = self.act["master"].pose(f, p, hands={"r": {"hand": hand, "stretch": 1.35}}, camera=self.cam)
                self.pin[f] = info.get("r", {}).get("error")
        fr = [bf(sub, g) for g in gs]
        for n in wanted(sub):
            a = self.act[n]
            for f, r in zip(fr, a.render_sprites(PPD[sub], frames=fr)):
                self.anch[(n, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite of %s clipped on frame %d" % (n, f), flush=True)

    def report(self, sub, g):
        f = bf(sub, g)
        self.scene.frame_set(f)
        loc, look, lens = CAMS[sub](g)
        v = look - loc
        out = dict(sub=sub, shot=SUB[sub]["shot"], g=g, cam=[round(c, 3) for c in loc], lens=lens,
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   yaw=round(math.degrees(math.atan2(v.x, v.y)), 1), quake=round(quake(g), 3), sway=round(sway_amp(g), 3),
                   crack=crack_level(g), plaster=plaster_level(g), heads={})
        sc = 22.0 / lens
        for n in wanted(sub):
            a = self.act[n]
            if (n, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(n, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.5, hy), f, res)
            out["heads"][n] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        if f in self.pin and self.pin[f] is not None:
            out["pin_err"] = round(self.pin[f], 3)
        pts = {"joint": G.JOINT, "cup": tuple(CUP), "pagoda_top": (0, 0, G.SORIN_TOP), "tower_top": (14.0, 0.0, 20.8)}
        out["pts"] = {k: [round(x, 1) for x in render.world_to_screen(self.cam, p, f)[:2]] for k, p in pts.items()}
        return out

    def dof(self, sub):
        foc, fs = DOF[sub]
        if foc == "cup":
            foc = (CUP.x, CUP.y, CUP.z + 0.2)
        elif isinstance(foc, str):
            foc = self.act[foc].card
        self.scene.camera = self.cam
        G.setup_dof(self.scene, foc, fs, cam=self.cam)

    def render(self, sub, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(sub)
        self.dof(sub)
        self.scene.cycles.samples = samples
        return render.render_frames([bf(sub, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(argv, take_dir=HERE):
    cmd = argv[1]
    subs = argv[2].split(",")
    presets = sorted({SUB[s]["preset"] for s in subs})
    assert len(presets) == 1, "one preset per process"
    if cmd in ("probe", "stills"):
        Tk = Take(presets[0])
        for sub in subs:
            r0, r1 = SUB[sub]["r"]
            gs = [g for g in parse(argv[3]) if r0 <= g <= r1] or [r0, (r0 + r1) // 2, r1]
            Tk.pose(sub, gs)
            for g in gs:
                print(json.dumps(Tk.report(sub, g)), flush=True)
                if cmd == "stills":
                    out = argv[4]
                    scale = float(argv[5]) if len(argv) > 5 else 0.5
                    samples = int(argv[6]) if len(argv) > 6 else 6
                    st = Tk.render(sub, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "%s_g_%04d.png" % (sub, g)))
                    print("%s g %d  %.1f s wall %.1f cpu" % (sub, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        Tk = None
        for sub in subs:
            r0, r1 = SUB[sub]["r"]
            gs = [g for g in parse(argv[3]) if r0 <= g <= r1]
            out = os.path.join(take_dir, "raw", sub)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: %s, %d to render, %d done" % (sub, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take(presets[0], quality="final")
            Tk.pose(sub, todo)
            for g in todo:
                st = Tk.render(sub, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(sub, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("%s g %d  %.1f s wall  %.1f s cpu" % (sub, g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    main(sys.argv)
