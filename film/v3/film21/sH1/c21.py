"""c21.py -- helper for film 21 take s09 (REVEAL): stirling set + cast21 sprite cards (stage actors) in ONE scene.
Units: set = metres (K.D = 1.7 m character); stage actors = head diameters, so a card is scaled by (set height / drawn height in head D)."""
import os, sys, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np
import cast21                                    # before sprites / actors
import bpy
from mathutils import Vector
import actors, camrig, sprites
import stirling as K

# drawn height (head top to soles, head diameters) -> true height (m)
DRAWN = {"cressingham": (3.23, 1.78), "surrey": (3.20, 1.66), "knight_a": (3.26, 1.78), "knight_b": (3.38, 1.78), "knight_a_open": (3.26, 1.78),
         "footman_a": (3.04, 1.68), "footman_b": (3.24, 1.68), "scot_a": (3.18, 1.70), "scot_b": (3.36, 1.70), "scot_c": (3.07, 1.70),
         "scot_horn": (3.16, 1.70), "helmet_float": (3.0, 1.66), "wallace": (3.59, 1.92), "moray": (3.32, 1.80)}
SPR = os.path.join(HERE, "sprites")

def cast_scale(cast):
    base = cast.split("_v")[0]
    d, h = DRAWN[base]; return h / d

def make_actor(name, cast, px=None):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], SPR, contact=True)
    a.head_flip = False
    return a

def lerp(a, b, u): return a + (b - a) * u
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * u * (u * (6 * u - 15) + 10)
def sstep(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)

def set_cam(cam, loc, look, lens, roll=0.0):
    cam.location = Vector(loc)
    cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    cam.data.lens = lens
    bpy.context.view_layer.update()

def seconds(g): return g / 30.0
