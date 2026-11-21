#!/usr/bin/env python3
"""c21.py -- helpers of take s05 (film 21): the Stirling set (set3d21/stirling.py = K) + cast21 puppet cards (v3/stage actors).
One location per process.  Every actor card is an emission card; the set's own sun casts the shadow proxies.
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                            # noqa: E402  (BEFORE sprites)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import stirling as K                                     # noqa: E402
import actors, camrig, sprites                           # noqa: E402
import numpy as np                                       # noqa: E402

CS = 0.50          # card scale: 1 head diameter = 0.5 m (a 3.4 D figure = 1.7 m = K.D)
SCALE = {"wallace": 0.52}


def g_of(t):
    return int(round((t + 0.10) * 30))


def ez(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def lerp(a, b, u):
    return a + (b - a) * u


def make_actor(name, cast, sprite_dir, contact=True):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact)
    a.head_flip = False
    return a


def aim_rot(loc, look):
    return (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()


def key_cam(cam, f, loc, look):
    camrig.key_camera(f, Vector(loc), Vector(look), cam=cam, interp="LINEAR", easing="AUTO")


def right_vec(cam_loc, look):
    d = Vector(look) - Vector(cam_loc); d.z = 0; d.normalize()
    return Vector((d.y, -d.x, 0.0))


def head_px(cam, p, W=720, Hh=1280):
    return K.project(cam, p, W, Hh)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out
