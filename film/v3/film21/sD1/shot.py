#!/usr/bin/env python3
"""shot.py -- film 21 segment D1 (g 542-642, CUT in, whip right out): Cressingham under the money canopy (camp_table, lantern, "KING'S TREASURY"
chest) counts coins into the chest; the camera ARCS around the table; he looks up across the river and bursts out LAUGHING at narration 20.29
(g 612): fixed laugh drawing, belly bounce, NO lip-sync.  The last 6 frames are a fast pan right (whip; joins by cut to team 4's whip-in).
    python3 shot.py stills a:b[:step] out [scale] [samples]   |   python3 shot.py final a:b[:step] [scale] [samples]
"""
import os, sys, math
import c21 as C
K, cast21 = C.K, C.cast21
from mathutils import Vector
ez, lerp, blink = C.ez, C.lerp, C.blink
HERE = C.HERE
G0, G1 = 542, 642
G_LAUGH = C.g_of(20.29)          # 612
G_LOOK = G_LAUGH - 10            # looks up across the river
G_WHIP = G1 - 6                  # last 6 frames: whip right
CEN = (-13.0, -26.6)             # the table


def cam_fn(world):
    tx, ty, tz = world["camp"]["table"]
    SIGN = (tx - 0.92, ty - 0.05 - 0.322, tz + 1.2)                  # centre of the KING'S TREASURY board (faces -y)
    HEAD = (-12.97, -26.0, tz + 1.55)                                  # Cressingham's face, roughly
    G_SIGN = G0 + 32                                                   # sign read until here, then the camera glides in front of him

    def f(g):
        t = (g - G0) / float(G1 - G0)
        # 1) the board: camera due south of the chest at table-top height, pushes in and slides, board kept centred (both lines readable)
        s1 = min(1.0, (g - G0) / float(G_SIGN - G0)); u1 = 0.35 * ez(s1) + 0.65 * s1
        d = lerp(1.95, 1.4, u1)
        c1 = (SIGN[0] + lerp(-0.30, 0.12, u1), SIGN[1] - d, tz + lerp(1.28, 1.34, u1))
        l1 = (SIGN[0], SIGN[1], SIGN[2])
        # 2) glide over the table front to him: head >= 15 % of the frame, coins and the counting hand in view
        s2 = max(0.0, min(1.0, (g - G_SIGN) / 24.0)); u2 = ez(s2)
        c2 = (lerp(c1[0], -13.30, u2), lerp(c1[1], -27.95, u2), lerp(c1[2], tz + 1.5, u2))
        l2 = (lerp(l1[0], -12.75, u2), lerp(l1[1], -26.3, u2), lerp(l1[2], tz + 1.62, u2))
        # 3) slow lateral drift and a push during the laugh
        dr = (g - G_SIGN - 24) / float(G1 - G_SIGN - 24) if g > G_SIGN + 24 else 0.0
        c2 = (c2[0] + 0.45 * dr, c2[1] + 0.5 * ez(max(0.0, (g - (G_LAUGH - 8)) / 24.0)), c2[2])
        loc, look = (c1, l1) if g <= G_SIGN else (c2, l2)
        if g > G_SIGN:
            pass
        if g > G_WHIP - 1:                                           # whip right: the view yaws clockwise, accelerating
            w = (g - (G_WHIP - 1)) / 6.0
            ang = -math.radians(95.0 * w * w)
            dd = np3(look[0] - loc[0], look[1] - loc[1], 0.0)
            ca, sa = math.cos(ang), math.sin(ang)
            look = np3(loc[0] + dd[0] * ca - dd[1] * sa, loc[1] + dd[0] * sa + dd[1] * ca, look[2] - 0.1 * w)
        return dict(loc=np3(*loc), look=np3(*look), lens=22.0, vivid=K.VIVID.get("camp_table", (1.05, 1.1)))
    return f


def np3(x, y, z):
    return (float(x), float(y), float(z))


def act_fn(A):
    cx, cy, cz = A["marks"]["camp_table"]["cress"][:3]

    def f(g):
        if g < G_LOOK:                                               # counting coins into the chest: the pinched coin drops and is fetched again
            p = dict(cast21.STORY21["cressingham_counting"][1]); ph = math.sin((g - G0) * 0.34)
            p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.78, 0.55, 0.5 + 0.5 * ph), lerp(1.45, 1.75, 0.5 + 0.5 * ph)))
            p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.09); p["head_roll"] = 1.5 * math.sin(g * 0.05)
            p["t"] = g / 30.0; p["blink"] = blink(g, [556, 590])
            return {"cre": ((cx, cy, cz), p)}
        if g < G_LAUGH:                                              # he looks up across the river
            p = dict(cast21.STORY21["cressingham_counting"][1]); u = ez((g - G_LOOK) / 7.0)
            p["pitch"] = lerp(p.get("pitch", 0), -0.8, u); p["gaze"] = (lerp(0.3, 0.8, u), lerp(0.9, -0.6, u)); p["lean"] = lerp(7, -2, u)
            p["arm_r"] = dict(p["arm_r"], hand=(0.78, 1.0)); p["t"] = g / 30.0
            p["blink"] = blink(g, [G_LAUGH - 3])
            return {"cre": ((cx, cy, cz), p)}
        p, dy = cast21.laugh(dict(cast21.STORY21["cressingham_laughing"][1]), g, phase=0.4)
        p["t"] = (g * 3.0 / 30.0) % 1.0
        return {"cre": ((cx, cy, cz + dy * K.D), p)}
    return f


def post(g, path):
    if g >= G_WHIP:
        C.motion_blur_h(path, 6 + 14 * (g - G_WHIP))


if __name__ == "__main__":
    holder = {}
    T = C.Take.__new__(C.Take)
    # build the world first (the camera / actor closures need A)
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    A = K.build_world(["camp_table"])
    for _o in bpy.data.objects:
        for _sl in _o.material_slots:
            if _sl.material is K._MATS.get('silver'): _sl.material = K._MATS['gold']        # coins read GOLD, not chalk
    T.A = A
    class Wrap(C.Take):
        def __init__(self):
            pass
    T = Wrap()
    T.A = A; T.cam = bpy.context.scene.camera; T.cam.data.dof.use_dof = False; T.cam.data.clip_start = 0.1
    K.setup_render(bpy.context.scene, "final")
    T.cam_fn, T.act_fn, T.g0, T.work, T.post_fn = cam_fn(A), act_fn(A), G0, os.path.join(HERE, "work"), post
    T.cast = {"cre": "cressingham"}; T.acts = {}; T.vivid = {}
    a = C.actors.Actor("cre", "cressingham"); a.build(C.sprites.DEFAULT_CANVAS["cressingham"], os.path.join(T.work, "sprites"), contact=True); a.head_flip = False
    T.acts["cre"] = a
    T.main(sys.argv, (G0, G1))
