#!/usr/bin/env python3
"""s06: row 6 (g 125-154) GAG "กำลังทำ ถังน้ำ": worker_c25 solemnly pours a WATERING CAN into the tank hatch (pour starts g 139 on "ถังน้ำ"),
worker_b25 nods seriously.  M, FACTORY preset fac_close_hull (hull side plate behind = near backdrop, cast shadows land on it).  PULL 10 %."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import rig25 as R
C = R.C; F = R.F; cast25 = R.cast25
from mathutils import Vector

PRESET = "fac_close_hull"
HAZE = 0.0006
ROW = (6, 125, 154)
HANDLE = 6
G_TAKE = (ROW[1] - HANDLE, ROW[2] - 1 + HANDLE)
HULL_Y = 22.0 - 3.15
HATCH_X = -11.0
GATE_POUR = 139


def story(n):
    return json.loads(json.dumps(cast25.STORY25[n][1]))


def blink(g, at):
    for b in at:
        if g - b in (0, 2): return 1
        if g - b == 1: return 2
    return 0


def pre():
    import factory as FA
    FA.PRESETS[PRESET]["tank"] = dict(pos=(-6, 22), yaw=0.0, z=0.02)      # tank on the floor: hatch at chest height


def build(rig):
    # frozen build: full tank on low trestles (set preset places it at z 0.9), hide nothing else
    import factory as FA
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.105, 0.055))
    rig.wc = rig.actor("wc", "worker_c25")
    rig.wb = rig.actor("wb", "worker_b25")
    rig.mk = Vector((HATCH_X, 17.6, 0.0))
    rig.backdrop((HATCH_X - 6.0, 26.0, 0.0), -90.0, w=40.0, h=16.0, col=(0.20, 0.23, 0.17), name="wall_plate")   # calm grey-olive plate behind the hull: hides the girders above it


def cam_of(g):
    u = C.calm((g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0]))
    d = 5.3 * (1.0 + 0.06 * u)                                       # PULL 10 %
    loc = Vector((HATCH_X - 0.2, 17.0 - d, 2.3))
    look = Vector((HATCH_X - 0.2, HULL_Y, 2.6))
    return loc, look, 30.0


def state(g):
    loc, look, lens = cam_of(g)
    pw = C.smooth((g - GATE_POUR) / 8.0)
    pc = story("worker_c25_pour_can"); pc["pour25"] = round(0.15 + 0.7 * pw, 3); pc["t"] = round((g * 0.09) % 1.0, 4)
    pc["light25"] = -1; pc["rim25"] = 0.6
    pc["gaze"] = [0.9, 0.55]; pc["arm_r"]["hand"] = [0.66, round(0.42 - 0.62 * pw, 3)]; pc["yaw"] = round(0.5 + 0.12 * pw, 3)
    pc["blink"] = blink(g, [131, 150]); pc["head_roll"] = round(-3 + 2.5 * math.sin((g - 125) * 0.31), 2); pc["lean"] = round(1.5 * math.sin((g - 125) * 0.2), 2)
    sq = None
    pb = story("worker_b25_nod_serious")
    pb["pitch"] = round(0.15 + 0.3 * (0.5 - 0.5 * math.cos((g - 125) * 2 * math.pi / 11.0)), 3)    # solemn nod
    pb["head_dy"] = round(0.02 + 0.05 * (0.5 - 0.5 * math.cos((g - 125) * 2 * math.pi / 11.0)), 3)
    pb["light25"] = -1; pb["rim25"] = 0.6; pb["blink"] = blink(g, [141, 128])
    pb["yaw"] = 0.4
    pb["head_roll"] = round(5 + 3 * math.sin((g - 125) * 0.57), 2)
    pbm = dict(pb)
    A = {"wc": dict(pos=(HATCH_X - 1.1, 16.5, 0.0), pose=pc, flip=False),
         "wb": dict(pos=(HATCH_X + 0.6, 16.3, 0.0), pose=pbm, flip=True)}
    fd = (loc - Vector((HATCH_X - 1.1, 16.5, 1.8))).length
    return dict(cam=(loc, look, lens), dof=(2.4, fd), actors=A)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(__import__("sys").modules[__name__], cmd, gs)
