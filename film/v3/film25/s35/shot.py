#!/usr/bin/env python3
"""s35: row 35 (g 1016-1042) M "แล้วตอกลังไม้": two workers hammer the giant crate planks round the tank (worker_a25 then worker_c25, alternating strikes on the plank wall).
FACTORY fac_crate (crate closed, stencil not yet painted -- masked).  FOLLOW the hammer, slide right."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import ck, rig25 as R, facb
C = R.C; F = R.F; bpy = R.bpy; from mathutils import Vector
PRESET = "fac_crate"; HAZE = 0.0006; ROWS = (35, 1016, 1043)
ACTORS = dict(wa="worker_a25", wc="worker_c25")
PLATE = ((0.0, 30.0, 0.0), -90.0, 60.0, 24.0, (0.05, 0.16, 0.42))
FLOOR = (0.30, 0.12, 0.07)
WALL_Y = 22.0 - 5.5 + 0.2
MASK = [None]


def pre_extra():
    import factory as FA
    p = FA.PRESETS[PRESET]; p["cards"] = []; p["tank_on"] = False; p["crate"] = dict(x=0, y=22, open=0.0)


def build_extra(rig):
    facb.paint_crate()
    fw = [o for o in bpy.data.objects if o.name == "crate_frontwall"]
    MASK[0] = facb.StencilMask(fw, axis=2); MASK[0].set(99.0, +1)             # the stencil is not painted yet (s36)
    # the plank wall behind the plate? the crate itself is the backdrop; hide the plate behind it (the crate hides it)


def strikes(g):
    return [1019, 1024, 1029, 1034, 1039]


def cam(g):
    u = C.calm((g - 1010) / 38.0)
    return Vector((-6.5 + 0.4 * u, 11.5, 2.4)), Vector((-6.4 + 0.4 * u, WALL_Y, 2.75)), 28.0


def acts(g):
    ss = strikes(g)
    out = {}
    for nm, member, x, sset, flip in (("wa", "worker_a25", -7.2, [1019, 1029, 1039], False), ("wc", "worker_c25", -5.7, [1024, 1034], False)):
        k = min(abs(g - s) for s in sset)
        hit = k <= 1
        base = "worker_a25_hammer_crate"
        p = R.story("worker_a25_hammer_crate")
        if member == "worker_c25":
            sp = R.story("worker_c25_spanner")
            p = dict(sp); p["prop_r"] = {"type": "hammer25", "angle": -50, "scale": 1.3}; p["arm_r"] = dict(R.story("worker_a25_hammer_crate")["arm_r"])
        p["light25"] = -1; p["rim25"] = 0.6
        arm = dict(p["arm_r"]); h = arm["hand"]
        arm["hand"] = [round(h[0] + (0.25 if hit else -0.05), 3), round(h[1] - (0.0 if hit else 0.18), 3)]
        p["arm_r"] = arm
        pr = dict(p["prop_r"]); pr["angle"] = 8 if hit else -62; p["prop_r"] = pr
        p["t"] = 0.2; p["blink"] = R.blink(g, [1022, 1036] if nm == "wa" else [1027]); p["yaw"] = 0.55
        if hit:
            p["squash"] = [1.03, 0.97]
        out[nm] = dict(pos=(x, 15.2, 0.0), pose=p, flip=flip)
    return out


def focus(g): return (-7.0, 15.2, 2.2)


ck.main(sys.modules[__name__])
