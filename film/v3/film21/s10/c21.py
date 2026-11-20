#!/usr/bin/env python3
"""c21.py -- helper for film-21 take s10 (copy of the film8/common.py idea, switched to cast21 + set3d21/stirling.py).
Stage actors (emission cards) in the Stirling set; per-frame camera (unkeyed, set in code), hooks and sprites; render through K.render (grade included).
Frames: Blender frame f = g + 1."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                    # noqa: E402  (before sprites)
import bpy                                       # noqa: E402
from mathutils import Vector                     # noqa: E402
import actors, camrig, sprites                   # noqa: E402
import stirling as K                             # noqa: E402
import numpy as np                               # noqa: E402

M_PER_D = 0.55          # metres per head diameter for the cast cards (knight head-top to soles 3.26 D = 1.78 m)


def g_of(t):  return int(round((t + 0.10) * 30))
def ez(u, k="sine"):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u) if k == "sine" else u
def lerp(a, b, u): return a + (b - a) * u
def vlerp(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))


def register_bare_knights():
    """knight_a_bare / knight_a_open_bare (+ _mtd riders): the same knights with a bare head (for the helmet that pops off)."""
    import puppet
    import cast_ext as CE
    for base in ("knight_a",):
        nb = base + "_bare"
        c = dict(puppet.CAST[base]); c["hat_style"] = "bare7"; c["hair"] = dict(color="#5a3a26", front=0.0, grow=0.0)
        c.pop("hat_colors", None)
        puppet.CAST[nb] = c
        puppet.CAST[nb + "_mtd"] = dict(puppet.CAST["knight_a"], _special21=True)
        cast21.MOUNTED[nb + "_mtd"] = nb
        cast21.DEFAULT_CAP[nb] = "red"
        CE.CANVAS[nb] = CE.CANVAS[base]
        CE.CANVAS[nb + "_mtd"] = cast21.CANVAS_SPECIAL21["knight_a_mtd"]
        sprites.DEFAULT_CANVAS[nb] = CE.CANVAS[nb]
        sprites.DEFAULT_CANVAS[nb + "_mtd"] = cast21.CANVAS_SPECIAL21["knight_a_mtd"]


def patch_air_helmet():
    """helmet_float without the foam ring when pose['air21'] (a helmet flying through the air)."""
    orig = cast21._helmet_float
    def hf(pose, uid):
        r = orig(pose, uid)
        if pose.get("air21"):
            import re
            svg = r["svg"]
            i = svg.rfind("</g></g>")
            r = dict(r); r["svg"] = svg[:i + 8]
        return r
    cast21._helmet_float = hf


class Take(object):
    def __init__(self, preset, quality="draft", samples=None, name="cam21"):
        t0 = time.time()
        self.A = K.build_for_cli(preset, placeholders=False)
        self.pr = K.PRESETS[preset]
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        self.cam.data.clip_start = 0.05
        self.quality, self.samples = quality, samples
        self.actors = {}
        self.anch = {}
        self.lens = self.pr.get("lens", 22.0)
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    def actor(self, name, cast, ppd_canvas=None, contact=True):
        a = actors.Actor(name, cast)
        a.build(ppd_canvas or sprites.DEFAULT_CANVAS[cast], os.path.join(HERE, "sprites_" + self.quality), contact=contact)
        a.head_flip = False
        self.actors[name] = a
        return a

    def set_cam(self, loc, look, lens=None):
        self.cam.location = Vector(loc)
        self.cam.rotation_euler = camrig.look_rotation(loc, look)
        self.cam.data.lens = lens or self.lens
        bpy.context.view_layer.update()

    def sprites_for(self, ppd, frames=None):
        for a in self.actors.values():
            fr = [f for f in (frames or a.poses.keys()) if f in a.poses]
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]
                if r.get("clipped"):
                    print("take: WARNING sprite %s clipped f%d" % (a.name, f), flush=True)

    def render(self, f, out_png):
        sc = self.scene
        sc.frame_set(f)
        actors.sync_all(sc, self.cam)
        t0 = time.time()
        K.render(out_png, self.quality, self.samples)
        return time.time() - t0


def head_px(take, name, f, radius=0.5):
    a = take.actors[name]
    take.scene.frame_set(f)
    res = a.feet.get(f)
    hx, hy = take.anch[(name, f)]["head"]
    c = actors.local_to_screen(a, take.cam, (hx, hy), f, res)
    return (round(c[0], 1), round(c[1], 1))
