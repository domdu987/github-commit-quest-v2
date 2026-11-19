"""c17.py -- helpers for film 17 take s07 (copy of the film8/common.py idea, switched to cast17 + set3d17/bertillon.py)."""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); V3 = os.path.abspath(os.path.join(HERE, "..", ".."))
for p in (os.path.join(V3, "cast17"), os.path.join(V3, "stage"), os.path.join(V3, "set3d17")):
    if p not in sys.path: sys.path.insert(0, p)
import cast17                                   # before sprites
import bpy
from mathutils import Vector
import bertillon as K
import actors, camrig, render, sprites

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def lerp(a, b, t): return a + (b - a) * t
def sstep(x): x = clamp(x); return x * x * (3 - 2 * x)
def lerpv(a, b, t): return tuple(lerp(x, y, t) for x, y in zip(a, b))

class Path:
    """camera path: waypoints [(g, loc, look)], cardinal spline through them (continuous velocity: no dead stops)."""
    def __init__(self, wps, tension=0.0):
        self.w = wps
    def at(self, g):
        w = self.w
        if g <= w[0][0]: g = w[0][0]
        if g >= w[-1][0]: g = w[-1][0]
        i = 0
        while i < len(w) - 2 and g > w[i + 1][0]: i += 1
        g0, g1 = w[i][0], w[i + 1][0]; u = (g - g0) / float(g1 - g0)
        def tan(k, which):
            a, b = max(k - 1, 0), min(k + 1, len(w) - 1)
            dt = float(w[b][0] - w[a][0]) or 1.0
            return [(w[b][which][c] - w[a][which][c]) / dt for c in range(3)]
        out = []
        for which in (1, 2):
            m0, m1 = tan(i, which), tan(i + 1, which); h = g1 - g0; r = []
            for c in range(3):
                p0, p1 = w[i][which][c], w[i + 1][which][c]
                r.append((2*u**3 - 3*u**2 + 1) * p0 + (u**3 - 2*u**2 + u) * h * m0[c] + (-2*u**3 + 3*u**2) * p1 + (u**3 - u**2) * h * m1[c])
            out.append(tuple(r))
        return out

class Rig:
    def __init__(self, preset, light=None):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset=preset, light=light)
        self.scene = bpy.context.scene
        old = self.scene.camera
        if old is not None: bpy.data.objects.remove(old, do_unlink=True)
        self.cam = camrig.make_camera(self.scene, name="cam_s07", lens=22.0); self.cam.data.clip_start = 0.02; self.cam.data.clip_end = 400
        self.cast = {}
        self.sdir = os.path.join(HERE, "work", "sprites"); os.makedirs(self.sdir, exist_ok=True)
        self.frames = []
    def key_cam(self, g, loc, look): camrig.key_camera(g, Vector(loc), Vector(look), cam=self.cam, lens=22.0, interp="LINEAR", easing="AUTO")
    def add(self, key, story, xyz, face=None, seated=None, H=None, rim=True, mirror=False, expr=None):
        cast, pose = cast17.STORY17[story]; pose = dict(pose)
        sc = (H or K.CAST_H[cast]) / K.CAST_HD[cast]
        a = actors.Actor("c_" + key, cast); a.build(sprites.DEFAULT_CANVAS[cast], self.sdir, contact=True); a.head_flip = True
        x, y, z = xyz
        if seated:
            fx, fy = sprites.feet_of(cast, dict(pose, seat17=None)); zz = K.HEAD_Z[seated] - sc * fy
        else: zz = z
        self.cast[key] = dict(a=a, cast=cast, pose0=pose, sc=sc, pos=(x, y, zz), mirror=mirror, rim=rim)
        return a
    def pose(self, key, g, pose, pos=None):
        c = self.cast[key]; p = dict(pose); p["seat17"] = None
        if c["mirror"]: p["mirror"] = True
        if c["rim"] and c["cast"] in K.RIM_FOR: p["rim"] = K.RIM_FOR[c["cast"]]; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
        c["a"].place(g, pos or c["pos"], scale=c["sc"]); c["a"].pose(g, p, camera=self.cam)
    def sprites(self, ppd, frames):
        for c in self.cast.values(): c["a"].render_sprites(ppd, frames=list(frames))
    def render(self, frames, out, scale, samples, threads):
        sc = self.scene; K.setup_render(sc, "final", samples); sc.render.threads = threads
        sc.cycles.denoising_prefilter = "FAST"
        res = []
        for g in frames:
            st = render.render_frames([g], out, scale=scale, threads=threads, scene=sc, camera=self.cam, verbose=False)[0]
            K.STATE["scale"] = scale; K.grade(st["path"], scale=scale)
            final = os.path.join(out, "g_%04d.png" % g); os.replace(st["path"], final)
            print("g", g, "%.1f s" % st["wall"], flush=True); res.append(st["wall"])
        return res
