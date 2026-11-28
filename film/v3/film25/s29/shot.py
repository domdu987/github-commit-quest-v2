#!/usr/bin/env python3
"""s29: rows 29+30 (g 882-917) PROCESS "แผ่นเหล็ก" then "หมุดย้ำ": worker_c25 guides the steel hull shell hanging on CHAINS (damped swing, lands with a small bounce
and LOCKS g 882-895); worker_a25's hammer strikes and a chunk of RIVETS pops in on each strike (g 902-918).  FACTORY fac_plates.  FOLLOW the plate in, PUSH 8 % on the rivets."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
bpy = R.bpy
from mathutils import Vector

PRESET = "fac_plates"
HAZE = 0.0006
ROWS = (29, 882, 918)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
TANK_Z = 1.0
STRIKES = [902, 905, 909, 912, 915]
PTS = [(-5.5, 1.8, 4.25), (-5.5, -1.8, 4.25), (0.8, 1.8, 4.0), (0.8, -1.8, 4.0)]


def pre():
    import factory as FA
    p = FA.PRESETS[PRESET]
    p["tank"] = dict(pos=(-6, 22), yaw=0.0, z=TANK_Z); p["slings"] = None
    p["stages"] = FA._st(plates=1.0, rivets=0.0)
    p["trestles_off"] = False


def shell_offset(g):
    """(dx, dz, tilt): the hull shell swings in on its chains, lands with a small bounce.  g 882 high and to the side, lands ~g 890, locks 895."""
    t = (g - 880) / 14.0
    if t <= 0: return 4.0, 3.2, 0.10
    if t >= 1.0: return 0.0, 0.0, 0.0
    e = 1 - (1 - t) ** 2.2
    dz = 3.2 * (1 - e)
    dx = 4.0 * (1 - e) * math.cos(t * 5.0) * 0.9
    bounce = 0.22 * math.exp(-((g - 891.5) / 1.6) ** 2) if g >= 890 else 0.0       # lands: a small bounce
    return dx, dz + bounce, 0.10 * (1 - e) * math.cos(t * 6.0)


def build(rig):
    import factory as FA
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.12, 0.07))
    rig.wc = rig.actor("wc", "worker_c25"); rig.wa = rig.actor("wa", "worker_a25")
    rig.H = F.S["tank"]; rig.FA = FA
    rig.plate = rig.H.parts["plates"][0][0]
    rig.backdrop((-8.0, 30.0, 0.0), -90.0, w=44.0, h=18.0, col=(0.05, 0.16, 0.42), name="blue_plate")


def sling_hook(rig, g):
    FA = rig.FA; H = rig.H; sub = rig.plate
    dx, dz, tilt = shell_offset(g)
    sub.location = Vector((dx, 0.0, dz)); sub.rotation_euler = (0, tilt, 0)
    rig.FA.TK.set_build(H, {"rivets": min(1.0, 0.0 if g < STRIKES[0] else sum(1 for s in STRIKES if g >= s) / float(len(STRIKES)))})
    old = bpy.data.objects.get("sl_dyn")
    if old:
        me = old.data; bpy.data.objects.remove(old); bpy.data.meshes.remove(me)
    mb = FA.MB(); M = F.S["M"]; hb = Vector((-5.0, 22.0, 11.6))
    for lp in PTS:
        wp = H.root.matrix_world @ (sub.matrix_basis @ Vector(lp))
        FA.L.chain(mb, hb + Vector((0, 0, -0.4)), wp, 0.3, 0.05, M["steel"])
        FA.obox(mb, wp + Vector((0, 0, 0.12)), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.22, 0.22, 0.12, M["p_yellow"])
    FA.mkobj(mb, "sl_dyn")


def cam_at(g):
    u = (g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0])
    A = (Vector((-9.65, 12.3, 2.3)), Vector((-9.65, 22.0, 3.8)), 28.0)
    B = (Vector((-9.65, 12.3, 2.2)), Vector((-9.65, 22.0, 3.3)), 28.0)
    Cc = (Vector((-9.6, 12.6, 2.2)), Vector((-9.6, 22.0, 3.2)), 29.0)
    return R.spline([A, B, Cc], C.calm(u))


def state(g):
    loc, look, lens = cam_at(g)
    # worker_c guides the plate: pushes (steps), then steps back with a thumb-up once it locks
    pc = R.story("worker_c25_push_barrel")
    w = C.smooth((g - 893) / 6.0)
    pc["lean"] = round(26 - 22 * w, 2); pc["t"] = round((g * 0.1) % 1.0, 3)
    pc["expr"] = "determined" if w < 0.5 else "grinning"
    pc["light25"] = -1; pc["rim25"] = 0.6; pc["blink"] = R.blink(g, [888, 905])
    dx, dz, tilt = shell_offset(g)
    # worker_a hammers: strike pose on the 5 strikes (3 frames), otherwise the raised rivet pose
    st = any(s <= g < s + 2 for s in STRIKES)
    pa = R.story("worker_a25_rivet_strike" if st else "worker_a25_rivet")
    pa["light25"] = -1; pa["rim25"] = 0.6; pa["blink"] = R.blink(g, [900, 913])
    if g < 899:
        pa = R.story("worker_a25_stand"); pa["light25"] = -1; pa["rim25"] = 0.6; pa["yaw"] = 0.5; pa["gaze"] = [0.7, -0.8]; pa["expr"] = "surprised"
    sq = None
    A = {"wc": dict(pos=(-10.9 + 0.5 * w, 16.2, 0.0), pose=pc, flip=False),
         "wa": dict(pos=(-8.9, 16.4, 0.0), pose=pa, flip=False)}
    fd = R.dist(loc, (-9.0, 16.3, 2.0))
    return dict(cam=(loc, look, lens), dof=(2.8, fd), actors=A, hook=lambda f: sling_hook(RIG[0], f))


RIG = [None]
_build = build


def build(rig):
    RIG[0] = rig; _build(rig)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
