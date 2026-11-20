#!/usr/bin/env python3
"""c17.py -- film-17 take helper (copy of the film8/common.py idea for set3d17/bertillon.py + cast17).  Import FIRST in shot.py.
Take = one K.build(preset, light) scene + one keyed camera + animated cast cards (stage Actor) + per-frame render with the set's grade.
Frame numbering: Blender frame f == film frame g (g >= 1)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(V3, "set3d17"), os.path.join(V3, "cast17"), os.path.join(V3, "stage")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast17                                   # noqa: E402  (before sprites)
import bpy                                      # noqa: E402
from mathutils import Vector                    # noqa: E402
import bertillon as K                           # noqa: E402
import actors, camrig, sprites                  # noqa: E402

def lerp(a, b, u): return a + (b - a) * u
def clamp(u, a=0.0, b=1.0): return max(a, min(b, u))
def ease(u): u = clamp(u); return 0.5 - 0.5 * math.cos(math.pi * u)
def mix(u, k=0.35): return k * ease(u) + (1 - k) * clamp(u)         # never a dead end
def blink(g, starts):
    for s in starts:
        d = g - s
        if 0 <= d < 5: return (0.5, 1.0, 1.0, 1.0, 0.5)[d]
    return 0.0
def vl(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))


class Take(object):
    def __init__(self, preset, light=None, mode="draft", samples=None, threads=2):
        t0 = time.time()
        self.preset, self.mode = preset, mode
        self.samples = samples or (6 if mode == "draft" else 12)
        self.A = K.build(preset=preset, light=light)
        K.clear_keys()
        for o in bpy.data.objects:                      # director fix: the additive light shafts wash over the cast cards
            if any(m and m.name.startswith('beam_fx') for m in (getattr(o.data, 'materials', None) or [])): o.hide_render = True
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.data.clip_start = 0.02; self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.threads = threads
        self.spec = {}; self.acts = {}
        self.sprite_dir = os.path.join(HERE, "raw", "sprites_" + mode)
        os.makedirs(self.sprite_dir, exist_ok=True)
        print("take: built %s in %.1f s" % (preset, time.time() - t0), flush=True)

    # ---- camera
    def key_cam(self, f, loc, look, lens=22.0):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")

    # ---- cast
    def add(self, key, mark, story, seated=None, mirror=False, dx=0.0, dy=0.0, dz=0.0, rim="auto", H=None):
        cast, pose = cast17.STORY17[story]
        x, y, z, fz, who = self.A["marks"][mark]
        sc = (H or K.CAST_H[cast]) / K.CAST_HD[cast]
        a = actors.Actor("c_" + key, cast); a.build(sprites.DEFAULT_CANVAS[cast], self.sprite_dir, contact=True); a.head_flip = True
        if seated:
            fx, fy = sprites.feet_of(cast, dict(pose, seat17=None)); zz = K.HEAD_Z[seated] - sc * fy
        else:
            zz = z
        self.spec[key] = dict(cast=cast, story=story, pos=(x + dx, y + dy, zz + dz), scale=sc, mirror=mirror,
                              rim=K.RIM_FOR.get(cast) if rim == "auto" else rim)
        self.acts[key] = a
        return a

    def pose_cast(self, key, f, pose, dz=0.0, dx=0.0):
        sp = self.spec[key]; a = self.acts[key]
        p = dict(pose); p["seat17"] = None
        if sp["mirror"]: p["mirror"] = True
        if sp["rim"]: p["rim"] = sp["rim"]; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
        x, y, z = sp["pos"]
        a.place(f, (x + dx, y, z + dz), scale=sp["scale"])
        return p

    def finish_poses(self, f, key, p):
        self.acts[key].pose(f, p, camera=self.cam)

    def make_sprites(self, gs, ppd=None):
        ppd = ppd or (160 if self.mode == "draft" else 256)
        for k, a in self.acts.items():
            t0 = time.time()
            res = a.render_sprites(ppd, frames=list(gs))
            for r in res:
                if r.get("clipped"): print("WARNING sprite clipped", k, flush=True)
            print("sprites %s %d frames %.1f s" % (k, len(gs), time.time() - t0), flush=True)

    # ---- heads on screen (720x1280 px), for QA
    def heads(self, f):
        self.scene.frame_set(f); out = {}
        for k, a in self.acts.items():
            an = a.poses.get(f)
            try:
                w = actors.local_to_world(a, (0.0, 0.0), f, camera=self.cam)
                px, py, dz = K.project(self.cam, tuple(w))
                w2 = actors.local_to_world(a, (0.5, 0.0), f, camera=self.cam)
                qx, qy, _ = K.project(self.cam, tuple(w2))
                R = math.hypot(qx - px, qy - py); out[k] = dict(cx=round(px), cy=round(py), R=round(R), chin=round(py + R))
            except Exception as e:
                out[k] = dict(err=str(e))
        return out

    def render(self, g, path):
        sc = self.scene
        sc.frame_set(g)
        actors.sync_all(sc, self.cam)
        K.setup_render(sc, self.mode, self.samples)
        sc.render.threads = self.threads
        sc.render.filepath = path
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        K.grade(path)
        return time.time() - t0


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out
