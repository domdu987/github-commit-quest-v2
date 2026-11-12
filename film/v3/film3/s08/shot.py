#!/usr/bin/env python3
"""shot.py -- film 3 take s08: shot 8, harbor set WINTER (engine: take3.py, same folder).

    shot 8  g 620..746  hard cut in.  base_eye two-shot in depth: the foreman near, laughing (foreman_laugh, belly heaving,
                        mouth held open: no lip movement), tommy far by the bucket at the tank foot, worker1 / worker2 laughing
                        behind.  Snap reframe onto the foreman g 657..667 (on 22.0 s = g 663).  Quoted line 22.1-24.6 s
                        (g 666..741): his mouth moves (lip-sync every 2 frames); on "pai ao si nam tan ma tha sa" (g 709) he
                        points at the tank.  Out-handle g 747..752 (9-frame dissolve into shot 9).

    python3 shot.py probe|stills|final 8 <a:b[:step]|all> [out_dir] [scale] [samples]
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import take3 as X                                      # noqa: E402
from take3 import W, g_of, kcam, sph, keys, ease, blink, pulse, lerp, clamp, H, Vector, lipsync   # noqa: E402
import puppet                                          # noqa: E402
import cast3                                           # noqa: E402

G8, G9 = 620, 747
H_OUT = 9 // 2 + 2                                     # 6
RNG = {8: (G8, G9 + H_OUT - 1)}
SNAP = (657, 667)
Q0, Q1 = g_of(22.1), g_of(24.6)                        # 666, 741: the quoted line
GAPS = [(g_of(23.03), g_of(23.07)), (g_of(23.52), g_of(23.55))]
POINT = g_of(23.54)                                    # 709
TOMMY = W(-1.0, 1.45)
HEAD_T = Vector((TOMMY.x, TOMMY.y, 1.95))
HEADING = -6.0
_f = Vector((math.sin(math.radians(HEADING)), math.cos(math.radians(HEADING)), 0.0))
_r = Vector((_f.y, -_f.x, 0.0))
CAM0 = HEAD_T - _f * 11.6
FOREMAN = CAM0 + _f * 4.1 - _r * 0.55
FOREMAN.z = 0.0
W1 = W(1.1, 0.9)
W2 = W(2.4, 2.6)
FHEAD = Vector((FOREMAN.x, FOREMAN.y, 2.75))


def cam8(g):
    # two-shot: look between the foreman's head and tommy;  after the snap: on the foreman, tommy over his shoulder
    mid = FHEAD.lerp(HEAD_T, 0.30)
    ks = [(G8, (6.0, HEADING - 2.0, -2.0, mid.x, mid.y, 2.55), "sine"),
          (641, (5.75, HEADING - 3.0, -1.5, mid.x, mid.y, 2.52), "sine"),
          (SNAP[0], (5.6, HEADING - 3.5, -1.2, mid.x, mid.y, 2.50), "quint"),
          (SNAP[1], (2.75, HEADING - 15.0, 1.0, FHEAD.x + _r.x * 0.42, FHEAD.y + _r.y * 0.42, 2.55), "sine"),
          (700, (2.6, HEADING - 17.0, 1.5, FHEAD.x + _r.x * 0.46, FHEAD.y + _r.y * 0.46, 2.58), "cubic"),
          (RNG[8][1], (2.45, HEADING - 21.0, 2.0, FHEAD.x + _r.x * 0.55, FHEAD.y + _r.y * 0.55, 2.62), "hold")]
    return kcam(g, ks, 0.2)


def foreman(g):
    lau = dict(cast3.STORY3["foreman_laugh"][1])
    heave = math.sin(g * 0.85)
    if g < Q0:
        p = dict(lau)
        p["head_roll"] = 14 + 3 * heave
        p["lean"] = -6 - 2.5 * abs(heave)
        p["squash"] = (1.03 + 0.015 * heave, 0.97 - 0.015 * heave)
        p["t"] = (g - G8) / 30.0
        return p, None
    talk = dict(yaw=0.35, pitch=-0.35, expr="smug", head_roll=6 + 2 * math.sin(g * 0.3), lean=-3,
                arm_r=dict(hand=(0.30, 1.12), bend=0.9), arm_l=dict(hand=(-0.26, 1.16), bend=0.9), legs="wide")
    pnt = dict(talk, arm_r=dict(hand=(1.02, 0.05), shape="point", bend=-0.6, stretch=1.25), head_roll=-3, yaw=0.45)
    u = ease((g - POINT + 3) / 7.0, "back_out")
    if g < POINT - 3:
        p = puppet.lerp_pose("foreman", lau, talk, ease((g - Q0 + 3) / 5.0, "sine")) if g < Q0 + 2 else dict(talk)
    else:
        p = puppet.lerp_pose("foreman", talk, pnt, clamp(u)) if u < 1 else dict(pnt)
        if u > 1.0:
            p["arm_r"] = dict(p["arm_r"]); h = p["arm_r"]["hand"]; p["arm_r"]["hand"] = (h[0] + 0.03 * (u - 1), h[1])
    p = dict(p)
    p["expr"] = "smug"
    p["mouth"] = lipsync(g, Q0, Q1, GAPS) or "smile"
    p["blink"] = blink(g, [Q0 - 1, 690, 730])
    p["squash"] = (1.0 + 0.01 * math.sin(g * 0.6), 1.0 - 0.01 * math.sin(g * 0.6))
    return p, None


def tommy(g):
    p = dict(cast3.STORY3["tommy_worried"][1])
    p["yaw"] = -0.45
    p["gaze"] = (-0.8, -0.2)
    p["blink"] = blink(g, [648, 712])
    p["head_roll"] = 6 + 2 * math.sin(g * 0.11)
    return p, None


def worker1(g):
    p = dict(cast3.STORY3["workers_laugh"][1])
    p["mirror"] = True
    b = math.sin(g * 0.9 + 1)
    p["head_roll"] = -10 + 3 * b
    p["squash"] = (1.0 + 0.012 * b, 1.0 - 0.012 * b)
    p["t"] = (g - G8) / 30.0
    return p, None


def worker2(g):
    p = dict(cast3.STORY3["workers_laugh_beard"][1])
    b = math.sin(g * 0.8 + 2)
    p["head_roll"] = 12 + 3 * b
    p["lean"] = -5 - 2 * abs(b)
    p["squash"] = (1.0 + 0.012 * b, 1.0 - 0.012 * b)
    return p, None


def state8(g):
    return dict(paint=0.0, seep=0.8, bucket=(H.BUCKET_MARK, 0.55, True, None))


DROPS = [dict(key="d0", strip=0, period=24, form=15, phase=3, floor=0.62, size=1.8)]


def build_fg(tk):
    """two barrels in shade at the near-right edge"""
    M = tk.M
    a = CAM0 + _f * 5.8 + _r * 1.9; b = CAM0 + _f * 6.7 + _r * 2.5
    return {"fg8": X.barrel("s8_barrel_a", (a.x, a.y, 0.0), tk.coll, M) + X.barrel("s8_barrel_b", (b.x, b.y, 0.0), tk.coll, M)}


SHOTS = {
    8: dict(rng=RNG[8], cam=cam8, state=state8, fg=("fg8",), drops=DROPS,
            actors={"foreman": dict(cast="foreman", place=lambda g: FOREMAN, pose=foreman, ppd=512),
                    "tommy": dict(cast="tommy", place=lambda g: TOMMY, pose=tommy, ppd=192),
                    "worker1": dict(cast="worker1", place=lambda g: W1, pose=worker1, ppd=192),
                    "worker2": dict(cast="worker2", place=lambda g: W2, pose=worker2, ppd=192)},
            marks={"bucket": W(0, 0.47, 0.7)}),
}

if __name__ == "__main__":
    X.main(SHOTS, build_fg, "s08")
