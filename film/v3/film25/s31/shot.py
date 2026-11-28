#!/usr/bin/env python3
"""s31: rows 31+32 (g 918-959) PROCESS "ตีนตะขาบ วนรอบทั้งคัน": side-on, the track loop on CHAINS drops round the hull (g 918-933, small bounce), then the links run all the
way round the rhomboid (set_drive, g 933-960).  FACTORY fac_tracks.  FOLLOW the drop, then a lateral slide along the loop."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R, facb
C, F, cast25 = R.C, R.F, R.cast25
bpy = R.bpy
from mathutils import Vector

PRESET = "fac_tracks"
HAZE = 0.0006
ROWS = (31, 918, 960)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
TANK_Z = 1.0
PTS = [(-6.0, 2.6, 4.4), (-6.0, -2.6, 4.4), (0.0, 2.6, 4.2), (0.0, -2.6, 4.2)]
RIG = [None]


def pre():
    import factory as FA
    p = FA.PRESETS[PRESET]
    p["tank"] = dict(pos=(-6, 22), yaw=0.0, z=TANK_Z); p["slings"] = None
    p["stages"] = FA._st(plates=1, rivets=1, tracks=1.0)


def drop(g):
    """(dz, dx, tilt) of the track loop: hangs high until 918, drops with a swing, lands (small bounce) at ~931, locked 933"""
    t = (g - 916) / 16.0
    if t <= 0: return 3.6, 0.0, 0.0
    if t >= 1.0: return 0.0, 0.0, 0.0
    e = 1 - (1 - t) ** 2.4
    bounce = 0.2 * math.exp(-((g - 931.5) / 1.5) ** 2) if g >= 929 else 0.0
    return 3.6 * (1 - e) + bounce, 0.5 * (1 - e) * math.cos(t * 5.5), 0.05 * (1 - e) * math.cos(t * 6.5)


def build(rig):
    import factory as FA
    RIG[0] = rig
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.12, 0.07))
    rig.wc = rig.actor("wc", "worker_c25"); rig.wb = rig.actor("wb", "worker_b25")
    rig.H = F.S["tank"]; rig.FA = FA
    rig.trk = rig.H.parts["tracks"][0][0]
    rig.backdrop((-8.0, 30.0, 0.0), -90.0, w=44.0, h=18.0, col=(0.05, 0.16, 0.42), name="blue_plate")


def hook(g):
    rig = RIG[0]; TK = rig.FA.TK
    dz, dx, tilt = drop(g)
    rig.trk.location = Vector((dx, 0.0, dz)); rig.trk.rotation_euler = (0, tilt, 0)
    TK.set_drive(rig.H, 0.0 if g < 933 else 0.55 * (g - 933))
    if dz > 0.01 or g < 934:
        facb.slings(rig, rig.trk, PTS, hb=(-5.0, 22.0, 12.0))
    else:
        facb.clear_slings()


def cam_at(g):
    u = (g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0])
    A = (Vector((-8.9, 12.4, 2.3)), Vector((-8.8, 22.0, 3.3)), 28.0)
    B = (Vector((-9.1, 12.4, 2.2)), Vector((-9.0, 22.0, 3.0)), 28.0)
    Cc = (Vector((-9.0, 12.6, 2.2)), Vector((-8.9, 22.0, 3.0)), 28.0)
    return R.spline([A, B, Cc], C.calm(u))


def state(g):
    loc, look, lens = cam_at(g)
    w = C.smooth((g - 931) / 5.0)
    pc = R.story("worker_c25_push_barrel"); pc["lean"] = round(26 - 20 * w, 2); pc["t"] = round((g * 0.1) % 1.0, 3)
    pc["expr"] = "determined" if w < 0.5 else "grinning"; pc["light25"] = -1; pc["rim25"] = 0.6; pc["blink"] = R.blink(g, [925, 945])
    pb = R.story("worker_b25_nod"); pb["light25"] = -1; pb["rim25"] = 0.6
    pb["pitch"] = round(0.1 + 0.3 * (0.5 - 0.5 * math.cos((g - 918) * 0.5)), 3); pb["head_roll"] = round(4 + 3 * math.sin((g - 918) * 0.4), 2); pb["blink"] = R.blink(g, [936])
    pb["arm_r"] = "akimbo"
    xw = -9.8
    A = {"wc": dict(pos=(xw, 16.4, 0.0), pose=pc, flip=False),
         "wb": dict(pos=(-8.3, 15.8, 0.0), pose=pb, flip=True)}
    return dict(cam=(loc, look, lens), dof=(2.8, R.dist(loc, (xw, 16.4, 2.0))), actors=A, hook=hook)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
