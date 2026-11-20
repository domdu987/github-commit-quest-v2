#!/usr/bin/env python3
"""c21.py -- film 21 take helper (adapted from film8/common.py): cast21 cards in the Stirling set (set3d21/stirling.py).
One location per process.  Per frame: key camera + actors, pose, rasterise sprites (gamma pre-compensated for K.grade), render with K.render."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast21"), os.path.join(V3, "stage"), os.path.join(V3, "set3d21"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast21                                            # noqa: E402  (before sprites)
import numpy as np                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
from PIL import Image                                    # noqa: E402
import stirling as K                                     # noqa: E402
import actors, camrig, sprites                           # noqa: E402

GAMMA = 1.28
SC = 0.54            # metres per puppet D (head-to-soles ~3.2 D -> ~1.75 m)


def g_of(t): return int(round((t + 0.10) * 30))
def lerp(a, b, u): return a + (b - a) * u
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def sine(u): u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def blink(g, starts, n=4):
    return any(s <= g < s + n for s in starts)
def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out


class Take(object):
    """cast cards in a K.build_world scene; the camera is moved by K.cam_path (set per frame before posing AND before rendering)."""
    def __init__(self, presets, work, fg=True, hide=(), extra=None):
        t0 = time.time()
        self.work = work; self.presets = presets
        self.A = K.build_world(presets, fg=fg)
        for o in bpy.data.objects:
            if any(o.name.startswith(h) for h in hide): o.hide_render = True
        if extra: extra(self.A)
        self.scene = bpy.context.scene; self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        self.actors = {}; self.anch = {}
        print("take: built %s in %.1f s" % (presets, time.time() - t0), flush=True)

    def actor(self, name, cast, ppd=192):
        a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], os.path.join(self.work, "sprites"), contact=True)
        a.head_flip = False; a.ppd = ppd; self.actors[name] = a; return a

    def place(self, name, f, xyz, scale=SC, flip=False):
        self.actors[name].place(f, tuple(map(float, xyz)), scale=scale, flip=flip)

    def pose(self, name, f, pose):
        self.scene.frame_set(f)
        return self.actors[name].pose(f, K.with_rim(pose), camera=self.cam)

    def sprites_for(self, frames_by_actor, vivid=None):
        for name, frames in frames_by_actor.items():
            a = self.actors[name]
            if not frames: continue
            for f in frames:
                try: os.remove(a.sprite_path(f))
                except OSError: pass
            res = a.render_sprites(a.ppd, frames=frames)
            for f, r in zip(frames, res): self.anch[(name, f)] = r["anchors"]
            for f in frames:                                   # pre-compensate the grade's gamma so the cards keep their drawn colours
                p = a.sprite_path(f); im = np.asarray(Image.open(p).convert("RGBA")).astype(np.float32) / 255
                vg = vivid(f) if vivid else 1.4
                im[..., :3] = im[..., :3] ** (1.0 / (GAMMA * vg))
                Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(p)
            a._sig.clear()
            if a.image is not None: a.image.reload()

    def render(self, f, path, samples=32, mode="final", used=()):
        sc = self.scene; sc.frame_set(f)
        for n, a in self.actors.items(): a.set_hidden(n not in used)
        for n in used: self.actors[n].sync(self.cam, sc)
        K.setup_render(sc, mode, samples); sc.cycles.denoising_prefilter = "FAST"; sc.render.threads = int(os.environ.get("THREADS", "4"))
        sc.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True); K.grade(path)
        return time.time() - t

    def heads(self, f):
        out = {}
        self.scene.frame_set(f)
        for n, a in self.actors.items():
            if a.card.hide_render or f not in a.poses: continue
            hx, hy = self.anch.get((n, f), {}).get("head", (0.0, 0.0)); c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            out[n] = (round(c[0]), round(c[1]))
        return out
