#!/usr/bin/env python3
"""s58: row 58 (g 1724-1745) EXPLAINER "มันมีไว้ข้าม": C: engineer25 holds the CHALK BOARD (chalk drawing: a rhomboid straddling a trench, no letters) and TAPS it
with a finger on the beats.  FACTORY preset fac_close_engineer; plain cobalt plate behind (cast shadow).  PUSH 10 % onto the board."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s06"))
import rig25 as R
C, F, cast25 = R.C, R.F, R.cast25
from mathutils import Vector

PRESET = "fac_close_engineer"
HAZE = 0.0006
ROWS = (58, 1724, 1746)
HANDLE = 6
G_TAKE = (ROWS[1] - HANDLE, ROWS[2] - 1 + HANDLE)
MK = (0.0, 46.5, 0.0)


def pre():
    import factory as FA
    FA.PRESETS[PRESET] = dict(FA.PRESETS[PRESET]); FA.PRESETS[PRESET]["cast"] = []         # no set puppet card (ours replaces it)
    FA.PRESETS[PRESET]["backdrop"] = None


def build(rig):
    rig.set_look(True); rig.open_shell(floor_col=(0.30, 0.12, 0.07))
    rig.eng = rig.actor("eng", "engineer25")
    rig.backdrop((0.0, 48.2, 0.0), -90.0, w=16.0, h=12.0, col=(0.04, 0.16, 0.48), name="blue_plate")


def cam_at(g):
    u = C.calm((g - G_TAKE[0]) / float(G_TAKE[1] - G_TAKE[0]))
    d = 3.9 / (1 + 0.10 * u)                                           # PUSH 10 %
    return Vector((0.3 - 0.25 * u, MK[1] - d, 2.4)), Vector((0.1, MK[1], 2.3 - 0.1 * u)), 34.0


def state(g):
    loc, look, lens = cam_at(g)
    p = R.story("engineer25_chalkboard_tap")
    taps = [1728, 1732, 1736, 1740]
    k = min([abs(g - t) for t in taps])
    tap = math.exp(-(k / 1.4) ** 2)
    h = list(p["arm_r"]["hand"]); p["arm_r"] = dict(p["arm_r"]); p["arm_r"]["hand"] = [round(h[0] - 0.12 * tap, 3), round(h[1] + 0.06 * (1 - tap) - 0.02, 3)]
    p["yaw"] = round(0.2 + 0.25 * math.sin((g - 1724) * 0.19), 3); p["pitch"] = round(0.05 + 0.1 * tap, 3)
    p["gaze"] = [0.0, round(0.7 - 0.7 * (1 if (g // 9) % 2 else 0), 2)]                      # glances at the board, then at us
    p["expr"] = "determined" if g < 1738 else "smirk"
    p["blink"] = R.blink(g, [1730, 1742]); p["light25"] = -1; p["rim25"] = 0.6
    p["head_roll"] = round(-2 + 2.5 * math.sin((g - 1724) * 0.31), 2)
    A = {"eng": dict(pos=MK, pose=p, flip=False)}
    return dict(cam=(loc, look, lens), dof=(2.4, R.dist(loc, (MK[0], MK[1], 2.2))), actors=A)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    R.run(sys.modules[__name__], cmd, gs)
