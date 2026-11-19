"""c17.py -- helpers for film 17 take s04 (copy-adapted from film8/common.py: cast17 + set3d17/bertillon.py)."""
import os, sys, math, json, time
FILM = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(FILM, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast17                                            # before sprites
import bpy
from mathutils import Vector
import bertillon as K
import actors, camrig, render, sprites
puppet = sys.modules.get("puppet")


def g_of(t):
    return int(round((t + 0.10) * 30))


def lerp(a, b, u):
    return a + (b - a) * u


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def sm(u):
    u = clamp(u); return u * u * u * (u * (6 * u - 15) + 10)


def sine(u):
    u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def mix3(a, b, u):
    return tuple(lerp(a[i], b[i], u) for i in range(3))


def key_hide(obs, f, hidden):
    for o in obs:
        o.hide_render = bool(hidden)
        o.keyframe_insert("hide_render", frame=f)
        fc = None
        for c in camrig.fcurves_of(o):
            if c.data_path == "hide_render":
                for kp in c.keyframe_points:
                    kp.interpolation = "CONSTANT"
