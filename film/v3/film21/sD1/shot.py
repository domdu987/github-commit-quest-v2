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
G_LOOK = G_LAUGH - 9             # looks up across the river
G_WHIP = G1 - 6                  # last 6 frames: whip right
CEN = (-13.0, -26.6)             # the table


def cam_fn(world):
    def f(g):
        t = (g - G0) / float(G1 - G0)
        u = 0.25 * ez(t) + 0.75 * t
        az = math.radians(lerp(-112.0, -48.0, u))                    # arc round the table (from the south-west to the south-east)
        r = lerp(2.6, 1.9, u) + 0.12 * math.sin(t * 5)
        r -= 0.5 * ez((g - (G_LAUGH - 6)) / 22.0)                  # director note: push in during the laugh so the head is >= 130 px
        z = lerp(1.85, 2.0, u) + K.ground(CEN[0], CEN[1]) * 0.0
        loc = np3(CEN[0] + r * math.cos(az), CEN[1] + r * math.sin(az), z)
        look = np3(CEN[0] + 0.25 * math.cos(az + 1.57), CEN[1] - 0.2 + 0.25 * math.sin(az + 1.57), lerp(2.12, 2.1, u))
        if g > G_WHIP - 1:                                           # whip right: the view yaws clockwise, accelerating
            w = (g - (G_WHIP - 1)) / 6.0
            ang = -math.radians(95.0 * w * w)
            d = np3(look[0] - loc[0], look[1] - loc[1], 0.0)
            ca, sa = math.cos(ang), math.sin(ang)
            look = np3(loc[0] + d[0] * ca - d[1] * sa, loc[1] + d[0] * sa + d[1] * ca, look[2] - 0.2 * w)
        return dict(loc=loc, look=look, lens=22.0, vivid=K.VIVID.get("camp_table", (1.05, 1.1)))
    return f


def np3(x, y, z):
    return (float(x), float(y), float(z))


def act_fn(A):
    cx, cy, cz = A["marks"]["camp_table"]["cress"][:3]

    def f(g):
        if g < G_LOOK:                                               # counting coins into the chest: the pinched coin drops and is fetched again
            p = dict(cast21.STORY21["cressingham_counting"][1]); ph = math.sin((g - G0) * 0.34)
            p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.78, 0.55, 0.5 + 0.5 * ph), lerp(1.0, 1.28, 0.5 + 0.5 * ph)))
            p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.09); p["head_roll"] = 1.5 * math.sin(g * 0.05)
            p["t"] = g / 30.0; p["blink"] = blink(g, [556, 590])
            return {"cre": ((cx, cy, cz), p)}
        if g < G_LAUGH:                                              # he looks up across the river
            p = dict(cast21.STORY21["cressingham_counting"][1]); u = ez((g - G_LOOK) / 6.0)
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
