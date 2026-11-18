#!/usr/bin/env python3
"""c13.py -- helpers for the film-13 ending take (copied from film8/common.py, switched to cast13 + set3d13/chicago.py).
GOTCHAS: key every animated hook on EVERY rendered frame; one location (street) per process; NO DOF; cards need per-frame pose + sprites."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast13"), os.path.join(V3, "stage"), os.path.join(V3, "set3d13"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast13                                          # noqa: E402  (before sprites)
import puppet                                          # noqa: E402
import bpy                                             # noqa: E402
from mathutils import Vector                           # noqa: E402
import chicago as B                                    # noqa: E402
import actors, camrig, render, sprites                 # noqa: E402
from anim import ease, lerp, clamp                     # noqa: E402,F401

N_FILM = 1995


def g_of(t):
    return int(round((t + 0.10) * 30))


def g_bound(t):
    return int(round(t * 30))


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def ez(u, kind="sine"):
    return ease(clamp(u), kind)


def make_actor(name, cast, sprite_dir, canvas=None, contact=True, shadow="proxy"):
    a = actors.Actor(name, cast)
    a.build(canvas or sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow=shadow)
    a.head_flip = False
    B.no_bounce(a.card)
    return a


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def head_report(scene, cam, acts, anch, f, radius=0.5):
    out = {}
    scene.frame_set(f)
    for a in acts.values():
        if a.card.hide_render or (a.name, f) not in anch:
            continue
        res = a.feet.get(f)
        hx, hy = anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, cam, (hx, hy), f, res)
        l = actors.local_to_screen(a, cam, (hx - radius, hy), f, res)
        r = actors.local_to_screen(a, cam, (hx + radius, hy), f, res)
        out[a.name] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
    return out
