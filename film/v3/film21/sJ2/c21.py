#!/usr/bin/env python3
"""c21.py -- helpers for the film-21 take scripts (cast21 cards inside the Stirling set), adapted from film8/common.py.
Import first: sets sys.path, imports cast21 BEFORE sprites, bpy, the set module K (stirling) and the stage modules."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
FILM = os.path.dirname(HERE)                       # v3/film21
V3 = os.path.dirname(FILM)
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                      # noqa: E402  (before sprites)
import bpy                                         # noqa: E402
from mathutils import Vector                       # noqa: E402
import stirling as K                               # noqa: E402
import actors, camrig, render, sprites             # noqa: E402
import numpy as np                                 # noqa: E402

NARRATION_OFFSET = 0.10


def g_of(t):
    """narration time -> film frame of an event"""
    return int(round((t + NARRATION_OFFSET) * 30))


def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sine(u): u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def ez(u): return sine(u)
def smooth(u): u = clamp(u); return u * u * u * (u * (6 * u - 15) + 10)


def blink(g, per=97, off=0):
    return 1 if ((g + off) % per) in (0, 1, 2) else 0


def bf(g):
    return int(g) + 1


def make_actor(name, cast, sprite_dir, contact=True):
    a = actors.Actor(name, cast)
    a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=contact, shadow="proxy")
    a.head_flip = False
    return a


class Take(object):
    """one K preset in a fresh scene; one camera (the K camera) keyed per frame; actors as cast21 cards."""

    def __init__(self, preset, quality="draft", placeholders=False):
        t0 = time.time()
        self.preset, self.quality = preset, quality
        if isinstance(preset, (list, tuple)):
            self.A = K.build_world(list(preset), placeholders=False, over=dict(foam_k=0.5))
            self.pr = K.PRESETS[preset[0]]
        else:
            self.A = K.build_for_cli(preset, placeholders=placeholders)
            self.pr = K.PRESETS[preset]
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.data.clip_start = 0.05
        self.cam.data.dof.use_dof = False
        self.cam.animation_data_clear() if self.cam.animation_data else None
        self.actors = {}
        self.anch = {}
        print("take: built %s in %.1fs" % (preset, time.time() - t0), flush=True)

    def key_cam(self, f, loc, look, lens=None):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def add(self, name, cast):
        a = make_actor(name, cast, os.path.join(self.workdir, "sprites"))
        self.actors[name] = a
        return a

    def sprites_for(self, ppd=256):
        for a in self.actors.values():
            frames = sorted(a.poses)
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
                self.anch[(a.name, f)] = r["anchors"]

    def head_px(self, a, f):
        """screen px (x, y) of the head centre of actor a at Blender frame f"""
        self.scene.frame_set(f)
        res = a.feet.get(f)
        hx, hy = self.anch[(a.name, f)]["head"]
        c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
        return round(c[0], 1), round(c[1], 1)

    def render(self, gs, out_dir, on_g, samples=24, draft=False, threads=4):
        """render film frames gs; on_g(g) runs after frame_set (hooks)."""
        K.setup_render(self.scene, "draft" if draft else "final", samples)
        self.scene.cycles.denoising_prefilter = "FAST"
        r = self.scene.render
        r.threads_mode = "FIXED"; r.threads = threads
        stats = []
        for g in gs:
            png = os.path.join(out_dir, "g_%04d.png" % g)
            st = render.render_frames([bf(g)], out_dir, scale=1.0, threads=threads, scene=self.scene, camera=self.cam,
                                      on_frame=lambda f, g=g: on_g(g), verbose=False)[0]
            os.replace(st["path"], png)
            K.grade(png, scale=K.STATE.get("scale", 1.0))
            stats.append(st)
            print("g %d  %.1fs" % (g, st["wall"]), flush=True)
        return stats


def hide_prefix(prefix, hide=True):
    n = 0
    for o in bpy.data.objects:
        if o.name.startswith(prefix):
            o.hide_render = hide; n += 1
    return n
