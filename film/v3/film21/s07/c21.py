"""c21.py -- s07 helpers: film 21 = set3d21/stirling.py (K) + cast21 + v3/stage.  (film8/common.py adapted.)"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                           # noqa: E402  BEFORE sprites / actors
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import stirling as K                                    # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402

# true card height (head top to soles, head-D units) -> world height (m, K.HEIGHT)
CARD_H = dict(cressingham=3.23, surrey=3.20, knight_b=3.38, knight_b_great=3.38, footman_a=3.04, footman_b=3.24)
WORLD_H = dict(cressingham=1.78, surrey=1.66, knight_b=1.78, knight_b_great=1.78, footman_a=1.68, footman_b=1.68)


def unit_scale(cast):
    return WORLD_H[cast] / CARD_H[cast]


def g_of(t):                      # narration time -> film frame of an event
    return int(round((t + 0.10) * 30))


def ez(u):
    u = max(0.0, min(1.0, u)); return 0.5 - 0.5 * math.cos(math.pi * u)


def lerp(a, b, u):
    return a + (b - a) * u


def blink(g, starts):
    return any(0 <= g - s < 3 for s in starts)


def make_actor(name, cast, sprite_dir):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True)
    a.head_flip = False
    return a
