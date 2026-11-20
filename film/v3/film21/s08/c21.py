#!/usr/bin/env python3
"""c21.py -- helpers for the film-21 take s08 (adapted from film8/common.py): cast21 + set3d21/stirling.py + v3/stage actors."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path: sys.path.insert(0, p)
import cast21                                            # noqa  (before sprites)
import bpy, numpy as np                                  # noqa
from mathutils import Vector                             # noqa
import stirling as K                                     # noqa
import actors, camrig, render, sprites                   # noqa

# head-top-to-soles height in head diameters (cast21 table) and the set's true heights (m) -> card scale
CAST_H = dict(scot_a=3.18, scot_b=3.36, scot_c=3.07, scot_horn=3.16, wallace=3.59, moray=3.32, knight_a=3.26, knight_a_open=3.26, knight_b=3.38,
              footman_a=3.04, footman_b=3.24, cressingham=3.23, surrey=3.20)
TRUE_H = dict(scot_a=1.70, scot_b=1.70, scot_c=1.70, scot_horn=1.70, wallace=1.92, moray=1.80, knight_a=1.78, knight_a_open=1.78, knight_b=1.78,
              footman_a=1.68, footman_b=1.68)

def g_of(t): return int(round((t + 0.10) * 30))
def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sm(u): u = clamp(u); return u * u * (3 - 2 * u)
def blink(g, period=70, off=0): return cast21.blink_at(g, period, off)

def hide_prefix(*prefixes):
    for o in bpy.data.objects:
        if any(o.name.startswith(p) for p in prefixes): o.hide_render = True

class Take(object):
    def __init__(self, preset, mode="draft", samples=None, lens=None, hide=()):
        t0 = time.time()
        self.preset = preset
        self.A = K.build_for_cli(preset, placeholders=False)
        self.scene = bpy.context.scene; self.cam = self.scene.camera
        self.cam.data.clip_start = 0.02; self.cam.data.dof.use_dof = False
        if lens: self.cam.data.lens = lens
        hide_prefix(*hide)
        K.setup_render(self.scene, mode, samples); self.mode = mode
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.actors = {}; self.casts = {}; self.sp = os.path.join(HERE, "work", "sprites_" + preset)
        os.makedirs(self.sp, exist_ok=True)
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def actor(self, name, cast, scale=None):
        a = actors.Actor(name, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], self.sp, contact=True)
        a.head_flip = False
        a.k_scale = scale or (TRUE_H.get(cast.replace("_mtd", ""), 1.7) / CAST_H.get(cast, 3.2))
        self.actors[name] = a; self.casts[name] = cast
        return a

    def key_cam(self, f, loc, look, lens=None, roll=0.0):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, roll=roll, interp="LINEAR", easing="AUTO")

    def place(self, name, f, xyz, flip=False, scale=1.0):
        a = self.actors[name]
        a.place(f, tuple(float(v) for v in xyz), scale=a.k_scale * scale, flip=flip)

    def pose(self, name, f, pose):
        self.scene.frame_set(f)
        self.actors[name].pose(f, pose, camera=self.cam)

    def sprites_for(self, frames, ppd=160):
        for a in self.actors.values():
            fr = [f for f in frames if f in a.poses]
            if fr: a.render_sprites(ppd, frames=fr)

    def render(self, frames, out_dir, scale=1.0, hook=None, threads=4):
        os.makedirs(out_dir, exist_ok=True)
        res = []
        for f in frames:
            def on(ff, hook=hook): 
                if hook: hook(ff)
            st = render.render_frames([f], out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, on_frame=on, verbose=False)[0]
            K.grade(st["path"], scale=scale); res.append(st)
        return res
