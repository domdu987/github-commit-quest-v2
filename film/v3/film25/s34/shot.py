#!/usr/bin/env python3
"""s34: row 34 (g 982-1015) PROCESS "ปืนใหญ่ 6 ปอนด์": C: worker_c25 pushes the 6-pounder barrel into the sponson; it slides in and CLUNKS home at ~g 1005 (squash on the clunk,
tiny recoil settle).  FACTORY (fac_sponsons preset), sponsons locked.  FOLLOW the barrel in, then PUNCH 15 % on the clunk."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
bpy = R.bpy
from mathutils import Vector

PRESET = "fac_sponsons"
HAZE = 0.0006
ROWS = (34, 982, 1016)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
TANK_Z = 1.0
CLUNK = 1005
RIG = [None]
WC_X = -9.6


def pre():
    import factory as FA
    p = FA.PRESETS[PRESET]
    p["tank"] = dict(pos=(-6, 22), yaw=0.0, z=TANK_Z)
    p["stages"] = FA._st(plates=1, rivets=1, tracks=1, sponsons=1.0, guns=0.0)


def lvl(g):
    return C.smooth((g - 988) / float(CLUNK - 988)) ** 0.8                  # slides in, arrives (level 1) exactly on the clunk


def build(rig):
    import factory as FA
    RIG[0] = rig
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.16, 0.05))
    rig.wc = rig.actor("wc", "worker_c25")
    rig.H = F.S["tank"]; rig.FA = FA
    rig.backdrop((-8.0, 30.0, 0.0), -90.0, w=44.0, h=18.0, col=(0.05, 0.16, 0.42), name="blue_plate")


def hook(g):
    rig = RIG[0]
    rig.FA.TK.set_build(rig.H, {"guns": lvl(g)})
    if g >= CLUNK:                                                                # clunk: the barrel sits home with a tiny recoil
        k = g - CLUNK
        for (sub, d) in rig.H.parts["guns"]:
            sub.location = Vector((0, 0.0, 0.0)) + d.normalized() * [0.0, 0.18, 0.06, -0.04, 0.0][k] if k < 5 else Vector((0, 0, 0))


def barrel_tip(g):
    """world point of the muzzle end of the right gun (toward the camera, min y) at level lvl(g)"""
    rig = RIG[0]
    rig.FA.TK.set_build(rig.H, {"guns": lvl(g)}); bpy.context.view_layer.update()
    sub = [s for (s, d) in rig.H.parts["guns"] if d.y < 0][0]
    pts = []
    for ob in sub.children_recursive:
        if ob.type == "MESH":
            pts += [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    ymin = min(p.y for p in pts)
    near = [p for p in pts if p.y < ymin + 0.3]
    return Vector((sum(p.x for p in near) / len(near), ymin, sum(p.z for p in near) / len(near)))


def cam_at(g, tip):
    u = (g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0])
    k = C.out_cubic((g - CLUNK) / 7.0) if g >= CLUNK else 0.0                  # PUNCH 15 % on the clunk
    d = 3.9 * (1 - 0.15 * k) / (1 + 0.04 * u)
    s = d / 3.9
    c = Vector((WC_X + 0.62 * s, 15.1 - d, 2.2))
    look = Vector((c.x + 0.72, 22.0, 2.0))
    return c, look, 34.0


def state(g):
    tip = barrel_tip(g)
    loc, look, lens = cam_at(g, tip)
    p = R.story("worker_c25_push_barrel")
    w = C.smooth((g - CLUNK) / 5.0)
    p["lean"] = round(26 - 14 * w, 2); p["t"] = round((g * 0.1) % 1.0, 3)
    p["expr"] = "determined" if w < 0.4 else "grinning"; p["mouth"] = "clench" if w < 0.4 else "smile"
    p["light25"] = -1; p["rim25"] = 0.6; p["blink"] = R.blink(g, [992, 1010])
    sq = None
    if CLUNK <= g < CLUNK + 6:
        sq = {0: [1.06, 0.94], 1: [1.08, 0.92], 2: [0.98, 1.03], 3: [0.97, 1.05], 4: [1.0, 1.02], 5: [1.0, 1.0]}[g - CLUNK]
        p["squash"] = sq
    if g >= CLUNK + 1:
        p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [0.9, 0.85]
        p["arm_l"] = dict(p["arm_l"]); p["arm_l"]["hand"] = [0.8, 1.0]
    pos = (WC_X, 15.1, 0.0)
    A = {"wc": dict(pos=pos, pose=p, flip=False)}
    return dict(cam=(loc, look, lens), dof=(2.4, R.dist(loc, (pos[0], pos[1], 2.4))), actors=A, hook=hook)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
