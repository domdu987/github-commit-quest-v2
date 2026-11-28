#!/usr/bin/env python3
"""s33: row 33 (g 960-981) PROCESS "ป้อมสองข้าง": worker_b25 with a spanner as the SPONSON slides in sideways and bolts on (locked by g 978, small squash bounce).
FACTORY fac_sponsons.  PUSH 10 % on the sponson."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
bpy = R.bpy
from mathutils import Vector

PRESET = "fac_sponsons"
HAZE = 0.0006
ROWS = (33, 960, 982)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
TANK_Z = 1.0
RIG = [None]


def pre():
    import factory as FA
    p = FA.PRESETS[PRESET]
    p["tank"] = dict(pos=(-6, 22), yaw=0.0, z=TANK_Z)
    p["stages"] = FA._st(plates=1, rivets=1, tracks=1, sponsons=0.0, guns=0.0)


def lvl(g):
    """sponson slide-in level: 0 until g 962, 1 (locked) by g 978; slight overshoot then settle = bolt-on bounce"""
    return C.smooth((g - 962) / 16.0)


def build(rig):
    import factory as FA
    RIG[0] = rig
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.12, 0.07))
    rig.wb = rig.actor("wb", "worker_b25")
    rig.H = F.S["tank"]; rig.FA = FA
    rig.backdrop((-8.0, 30.0, 0.0), -90.0, w=44.0, h=18.0, col=(0.05, 0.16, 0.42), name="blue_plate")


def hook(g):
    rig = RIG[0]; TK = rig.FA.TK
    TK.set_build(rig.H, {"sponsons": lvl(g)})
    sq = 0.0
    for (sub, d) in rig.H.parts["sponsons"]:
        if g >= 978:                                                              # tiny settle when it bolts on
            k = g - 978
            sub.location = d * 0.0 + Vector((0, 0, [0.0, -0.10, 0.05, -0.02, 0.0][k] if k < 5 else 0.0))


def cam_at(g):
    u = C.calm((g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0]))
    return Vector((-8.1 - 0.2 * u, 8.8, 2.3)), Vector((-8.0 - 0.2 * u, 22.0, 2.4)), 26.0 * (1 + 0.10 * u)


def state(g):
    loc, look, lens = cam_at(g)
    p = R.story("worker_c25_spanner")
    pb = R.story("worker_b25_stand")
    pb["arm_r"] = p["arm_r"]; pb["prop_r"] = p["prop_r"]; pb["arm_l"] = p["arm_l"]; pb["legs"] = {"preset": "step", "stride": 0.25, "crouch": 0.06}
    pb["yaw"] = 0.55; pb["expr"] = "determined"; pb["mouth"] = "clench"; pb["lean"] = 8
    turn = 0.5 + 0.5 * math.sin((g - 960) * 0.9)                        # tightens the bolts: wrench rocks
    pb["prop_r"] = dict(pb["prop_r"]); pb["prop_r"]["angle"] = round(-30 + 22 * (turn if 966 < g < 980 else 0), 2)
    pb["t"] = 0.2; pb["light25"] = -1; pb["rim25"] = 0.6; pb["blink"] = R.blink(g, [964, 981])
    w = C.smooth((g - 978) / 4.0)
    if g >= 979:
        pb["expr"] = "grinning"; pb["lean"] = 2; pb["pitch"] = -0.1
    A = {"wb": dict(pos=(-8.8, 11.9, 0.0), pose=pb, flip=False)}
    return dict(cam=(loc, look, lens), dof=(2.8, R.dist(loc, (-8.8, 11.9, 2.0))), actors=A, hook=hook)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
