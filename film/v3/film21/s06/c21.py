#!/usr/bin/env python3
"""c21.py -- film 21 take helper (own copy, after film8/common.py): set3d21/stirling.py + cast21 puppets as stage actors.
Blender frame bf(g) = g + 1.  Per frame: key camera + actors, pose, rasterise sprites, sync cards, K.render (graded)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                            # noqa: E402 (BEFORE sprites)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
import stirling as K                                     # noqa: E402
import actors, camrig, sprites                           # noqa: E402

F = 22.0
# metres per puppet D = character height / puppet height (head top to soles, hat included)
PUPPET_H = dict(footman_a=3.36, footman_b=3.56, knight_a=3.48, knight_b=3.76, scot_a=3.18, scot_b=3.60, scot_c=3.07, scot_horn=3.16,
                wallace=3.76, moray=3.44, surrey=3.32, cressingham=3.54)
REAL_H = dict(footman_a=1.68, footman_b=1.68, knight_a=1.78, knight_b=1.78, scot_a=1.70, scot_b=1.70, scot_c=1.70, scot_horn=1.70,
              wallace=1.92, moray=1.80, surrey=1.66, cressingham=1.78)


def bf(g):
    return int(g) + 1


def ez(u):
    u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)


def lerp(a, b, t):
    return a + (b - a) * t


class Rig(object):
    """camera path: base loc/look, push fraction of `dref` metres per second, lateral slide px/s, plus snaps (g0, n frames, dist factor)."""

    def __init__(self, loc, look, dref, g0, push=0.0, slide_px=0.0, snaps=(), lens=F, tilt_per_s=0.0):
        self.loc, self.look, self.dref, self.g0 = Vector(loc), Vector(look), dref, g0
        self.push, self.slide, self.snaps, self.lens, self.tilt = push, slide_px, list(snaps), lens, tilt_per_s
        d = (self.look - self.loc); self.dir = d.normalized(); self.right = self.dir.cross(Vector((0, 0, 1))).normalized()

    def at(self, g):
        t = (g - self.g0) / 30.0
        adv = self.push * self.dref * t                      # metres toward the look point
        for (s0, n, fac) in self.snaps:                      # fac < 1 : push in (distance x fac), fac > 1: pull out
            u = ez((g - s0) / float(n))
            adv += (1.0 - 1.0 / fac) * self.dref * u
        slide = self.slide / 782.2 * self.dref * t
        loc = self.loc + self.dir * adv + self.right * slide
        look = self.look + self.right * slide + self.dir * (adv * 0.0)
        return loc, look


class Take(object):
    def __init__(self, preset, work, quality="draft", fg=True, troops=False, extra=None):
        self.preset, self.quality = preset, quality
        self.work = work
        os.makedirs(work, exist_ok=True)
        self.A = K.build(preset=preset)
        self.pr = K.PRESETS[preset]
        if fg and self.pr.get('fg'):
            self.pr['fg'](self.A, self.pr)
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.actors = {}
        self.anch = {}

    def hide(self, *prefixes):
        for o in bpy.data.objects:
            if any(o.name.startswith(p) for p in prefixes):
                o.hide_render = True

    def make_actor(self, name, cast):
        a = actors.Actor(name, cast)
        a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(self.work, "sprites"), contact=True, shadow="proxy")
        a.head_flip = False
        self.actors[name] = a
        return a

    def key_cam(self, g, loc, look, lens=F):
        camrig.key_camera(bf(g), Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    def ppd_for(self, cast, dist, safety=1.15):
        s = REAL_H.get(cast.split("_")[0] if cast not in REAL_H else cast, 1.7) / PUPPET_H.get(cast.split("_")[0] if cast not in PUPPET_H else cast, 3.4)
        v = s * 782.2 * (self.cam.data.lens / F if False else 1.0) / max(dist, 1.0) * safety
        return int(max(48, min(192, math.ceil(v / 16.0) * 16)))

    def place(self, a, g, xyz, cast_key, flip=False):
        s = REAL_H[cast_key] / PUPPET_H[cast_key]
        a.place(bf(g), xyz, scale=s, flip=flip)

    def pose(self, a, g, pose):
        a.pose(bf(g), pose, camera=self.cam)

    def sprites_for(self, items):
        """items: [(actor, ppd, [g..])]"""
        for a, ppd, gs in items:
            fr = [bf(g) for g in gs]
            for f, r in zip(fr, a.render_sprites(ppd, frames=fr)):
                self.anch[(a.name, f)] = r["anchors"]

    def heads(self, g):
        out = {}
        f = bf(g); self.scene.frame_set(f)
        for a in self.actors.values():
            if a.card.hide_render or (a.name, f) not in self.anch:
                continue
            res = a.feet.get(f)
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            out[a.name] = (round(c[0]), round(c[1]))
        return out

    def render(self, g, path, samples=None, hook=None):
        f = bf(g)
        self.scene.frame_set(f)
        if hook:
            hook(g)
        actors.sync_all(self.scene, self.cam)
        mode = "draft" if self.quality == "draft" else "final"
        return K.render(path, mode, samples)
