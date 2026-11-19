"""c17.py -- helper for film-17 take s13 (copied/trimmed from film8/common.py: cast17 + set3d17/bertillon.py, no depth of field)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                              # noqa  (before sprites)
import bpy                                                 # noqa
from mathutils import Vector                               # noqa
import bertillon as K                                      # noqa
import actors, camrig, render, sprites                     # noqa

def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def lerp(a, b, t): return a + (b - a) * t
def ez(u):
    u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def ez_out(u):
    u = clamp(u); return 1 - (1 - u) ** 3
def blink(g, starts, n=4):
    for s in starts:
        if 0 <= g - s < n: return 1.0 if 1 <= g - s <= 2 else 0.5
    return 0.0

def make_actor(name, cast, sprite_dir):
    a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True); a.head_flip = True
    return a
