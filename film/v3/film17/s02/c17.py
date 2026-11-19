"""c17.py: film-17 take helper (own copy, adapted from film8/common.py: cast17 + set3d17/bertillon.py)."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.normpath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17"), os.path.join(V3, "..", "v2", "shots")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                    # before sprites
import bpy
from mathutils import Vector
import bertillon as K
import actors, camrig, render, sprites
from anim import blink, lerp, clamp

def sm(u):
    u = clamp(u); return u * u * (3 - 2 * u)
def mix(u):                                       # mostly linear: no dead ends
    return 0.3 * sm(u) + 0.7 * clamp(u)
def vlerp(a, b, u): return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))
def snap(g, g0, dur):                             # 0..1 eased snap progress
    return sm((g - g0) / float(dur))

class Take(object):
    def __init__(self, preset, light=None, quality="draft"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.preset = preset
        self.A = K.build(preset=preset, light=light); self.scene = bpy.context.scene
        K.clear_keys(); self.cam = camrig.make_camera(self.scene, name="cam_s02", lens=22.0)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400; self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        self.actors = {}; self.anch = {}; self.quality = quality
    def mk(self, name, cast, sprite_dir):
        a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True); a.head_flip = True
        self.actors[name] = a; return a
    def key_cam(self, f, loc, look):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
    def place(self, a, f, xyz, scale):
        a.place(f, tuple(xyz), scale=scale)
    def finish_sprites(self, frames, ppd):
        for a in self.actors.values():
            for f, r in zip(frames, a.render_sprites(ppd, frames=frames)): self.anch[(a.name, f)] = r["anchors"]
    def render(self, frames, out_dir, scale, samples):
        K.setup_render(self.scene, "final", samples); self.scene.render.resolution_x = int(720 * scale); self.scene.render.resolution_y = int(1280 * scale)
        K.STATE['scale'] = scale; self.scene.render.threads = 2
        self.scene.camera = self.cam; self.cam.data.dof.use_dof = False
        st = render.render_frames(list(frames), out_dir, scale=scale, threads=2, scene=self.scene, camera=self.cam, verbose=False)
        for s in st: K.grade(s["path"], scale=scale)
        return st
    def heads(self, f):
        out = {}; self.scene.frame_set(f)
        for a in self.actors.values():
            if (a.name, f) not in self.anch or a.card.hide_render: continue
            hx, hy = self.anch[(a.name, f)]["head"]; res = a.feet.get(f)
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res); l = actors.local_to_screen(a, self.cam, (hx - .5, hy), f, res); r = actors.local_to_screen(a, self.cam, (hx + .5, hy), f, res)
            out[a.name] = dict(x=round(c[0]), y=round(c[1]), w=round(math.hypot(r[0] - l[0], r[1] - l[1])))
        return out
def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out
