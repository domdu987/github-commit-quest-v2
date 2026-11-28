#!/usr/bin/env python3
"""s62: row 62 (g 1813-1842) "ที่แปลว่าถังน้ำ": DOCK: a REAL riveted WATER TANK on legs (with a tap) side by side with the Mark I; worker_a25 walks across and looks from one to
the other (head turns).  DOCK preset dock_watertank.  Lateral slide from the water tank to the Mark I."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
from mathutils import Vector

PRESET = "dock_watertank"
HAZE = 0.0006
ROWS = (62, 1813, 1843)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
WY = 29.0


def pre():
    pass


def build(rig):
    rig.set_look(True)
    rig.wa = rig.actor("wa", "worker_a25")


def wx(g):
    u = C.calm((g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0]))
    return -6.6 + 4.6 * u


def cam_at(g):
    u = C.calm((g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0]))
    x = -6.9 + 5.0 * u
    return Vector((x + 0.4, WY + 7.0, 2.4)), Vector((x + 1.0, 20.0, 0.2)), 28.0


def state(g):
    loc, look, lens = cam_at(g)
    p = R.story("worker_a25_nod") if False else R.story("worker_a25_stand")
    ph = (g - 1813) / 29.0
    look_r = C.smooth((g - 1827) / 6.0)                             # first the water tank (left), then the Mark I (right)
    p = R.cast25.cycle("worker_a25", (g * 1.0) / 28.0, "walk") if False else p
    p["yaw"] = round(-0.7 + 1.5 * look_r, 3); p["gaze"] = [round(-0.8 + 1.6 * look_r, 2), 0.0]
    p["expr"] = "surprised" if look_r < 0.5 else "happy"
    p["pitch"] = round(0.15 * math.sin(g * 0.4), 3); p["blink"] = R.blink(g, [1822, 1838])
    p["head_roll"] = round(-4 + 8 * look_r, 2); p["light25"] = -1; p["rim25"] = 0.6
    p["arm_r"] = "akimbo"
    A = {"wa": dict(pos=(wx(g), WY, 0.0), pose=p, flip=False)}
    return dict(cam=(loc, look, lens), dof=(3.2, R.dist(loc, (wx(g), WY, 2.0))), actors=A)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
