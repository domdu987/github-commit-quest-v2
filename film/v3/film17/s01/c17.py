"""c17.py -- helpers for film 17 take scripts (copy of film8/common.py reduced to what s01 needs; cast17 + set3d17/bertillon.py)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.dirname(os.path.dirname(HERE)); PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                            # noqa  (before sprites)
import bpy                                               # noqa
from mathutils import Vector                             # noqa
import bertillon as K                                    # noqa
import actors, camrig, render, sprites                   # noqa
from anim import ease, blink, lerp, clamp                # noqa

def ez(u, kind="sine"): return ease(clamp(u), kind)
def bf(g): return int(g) + 1

def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else: out.append(int(part))
    return out

def vis(actor, f, on):
    """key an actor's render visibility (card, shadow proxy, contact decal) constant at Blender frame f."""
    for o in actor.objects():
        o.hide_render = not on; o.keyframe_insert("hide_render", frame=f)
        fc = None
        for c in camrig.fcurves_of(o):
            if c.data_path == "hide_render": fc = c
        if fc:
            for kp in fc.keyframe_points: kp.interpolation = "CONSTANT"

class Take(object):
    def __init__(self, preset, quality="draft"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = K.build(preset=preset); self.scene = scene = bpy.context.scene
        K.setup_render(scene, "final" if quality == "final" else "draft")
        scene.cycles.denoising_prefilter = "FAST"; scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 9000
        old = scene.camera
        self.cam = camrig.make_camera(scene, name="cam_s01", lens=22.0)
        self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        self.cam.data.dof.use_dof = False
        scene.camera = self.cam
        K.clear_keys()
        self.actors = {}; self.anch = {}
    def key_cam(self, f, loc, look, lens=22.0):
        camrig.key_camera(f, Vector(loc), Vector(look), cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")
    def make_actor(self, name, cast, sprite_dir):
        a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], sprite_dir, contact=True); a.head_flip = True
        self.actors[name] = a; return a
    def sprites_for(self, a, ppd, frames):
        for f, r in zip(frames, a.render_sprites(ppd, frames=frames)):
            self.anch[(a.name, f)] = r["anchors"]
            if r.get("clipped"): print("WARNING clipped", a.name, f, flush=True)
    def render(self, frames, out_dir, scale, samples, threads=2):
        self.scene.camera = self.cam; self.cam.data.dof.use_dof = False
        self.scene.cycles.samples = samples
        return render.render_frames(list(frames), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)
