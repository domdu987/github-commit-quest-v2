#!/usr/bin/env python3
"""c22.py -- per-take helper for film 22 (copied into each take folder; adapted from film8/common.py to cast22 + set3d22).
Builds ONE location of set3d22 (beck.build), then renders a range of film frames with PER-FRAME cast cards:
  T = Take(shot, location, light, here, state=..., hide=[object names], keys=PATH)   # PATH = master camera keys (absolute film frames)
  T.render(gs, actors_fn, out_dir, quality='final'|'preview', samples=None)
actors_fn(g, T) builds the cast cards of film frame g with beck.cast_card (T.ob list is wiped every frame).
Camera: cardinal spline through PATH keys (g, loc, look, lens[, roll]); identical lists in two takes give an exact travel join.
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))                    # film/
SET = os.path.join(PROJ, 'v3', 'set3d22')
sys.path.insert(0, SET)
os.environ.setdefault('NODE_PATH', '/opt/node22/lib/node_modules')
import numpy as np
import bpy
from mathutils import Vector
import beck                                           # noqa: E402
import beck_hq as HQ                                  # noqa: E402
import tower as TW                                    # noqa: E402
V = Vector


def g_of(t): return int(round((t + 0.10) * 30))      # event at narration time t -> film frame
def nt(g): return g / 30.0 - 0.10                      # film frame -> narration time


class Path(object):
    """cardinal (Catmull-Rom, tension 0.5) spline through keys [(g, loc, look, lens[, roll])]; linear extrapolation beyond the ends."""
    def __init__(self, keys):
        self.f = [k[0] for k in keys]
        self.v = [np.array([*k[1], *k[2], k[3], (k[4] if len(k) > 4 else 0.0)], float) for k in keys]
        n = len(keys); self.t = []
        for i in range(n):
            if i == 0: tg = (self.v[1] - self.v[0]) / (self.f[1] - self.f[0])
            elif i == n - 1: tg = (self.v[-1] - self.v[-2]) / (self.f[-1] - self.f[-2])
            else: tg = (self.v[i + 1] - self.v[i - 1]) / (self.f[i + 1] - self.f[i - 1])
            self.t.append(tg)
    def __call__(self, g):
        f, v, t = self.f, self.v, self.t; n = len(f)
        if g <= f[0]: o = v[0] + t[0] * (g - f[0])
        elif g >= f[-1]: o = v[-1] + t[-1] * (g - f[-1])
        else:
            i = max(j for j in range(n - 1) if f[j] <= g); h = f[i + 1] - f[i]; u = (g - f[i]) / h
            h00, h10, h01, h11 = 2*u**3 - 3*u**2 + 1, u**3 - 2*u**2 + u, -2*u**3 + 3*u**2, u**3 - u**2
            o = h00 * v[i] + h10 * h * t[i] + h01 * v[i + 1] + h11 * h * t[i + 1]
        return V(o[0:3]), V(o[3:6]), float(o[6]), float(o[7])


class Take(object):
    def __init__(self, shot, keys, quality='final', state=None, pre=None, hide=(), animate=None, light=None, samples=None, here=HERE):
        self.shot, self.here = shot, here
        TW.ACT = os.path.join(here, 'actors'); os.makedirs(TW.ACT, exist_ok=True)       # cast card cache lives in the take folder
        sh = beck.ALL_SHOTS[shot]; self.sh = sh; self.path = Path(keys)
        sh.pop('actors', None); sh['animate'] = {}; sh['animate_objs'] = []
        if state is not None: sh['state'] = state
        if pre is not None: sh['pre'] = pre
        g0 = keys[0][0]; self.quality = quality
        k0 = (tuple(keys[0][1]), tuple(keys[0][2]), keys[0][3]); sh['cam'] = [(0,) + k0, (10,) + k0]
        beck.build(sh['location'], light or sh.get('light'), shot, quality, g0)
        self.sc = bpy.context.scene
        for nme in hide:
            o = bpy.data.objects.get(nme)
            if o is None: print('WARNING hide: no object', nme, flush=True)
            else: o.hide_render = True; o.hide_viewport = True
        self.static = set(o.name for o in bpy.data.objects)
        self.sc.render.threads = 2; self.sc.cycles.samples = 13 if quality == 'final' else self.sc.cycles.samples
        self.ob = []; self.animate = animate or (lambda g, T: None)
        if samples: self.sc.cycles.samples = samples
        print('take: built', shot, sh['location'], 'objects', len(self.static), flush=True)

    def clear(self):
        for o in [o for o in bpy.data.objects if o.name not in self.static]:
            bpy.data.objects.remove(o, do_unlink=True)
        for me in [m for m in bpy.data.meshes if m.users == 0]: bpy.data.meshes.remove(me)

    def card(self, *a, **kw):
        o = beck.cast_card(*a, **kw); self.ob.append(o); return o

    def set_cam(self, g):
        loc, look, lens, roll = self.path(g); roll += 0.7 * math.sin(g / 9.0)   # hand-held sway
        cam = self.sc.camera
        cam.animation_data_clear(); cam.rotation_mode = 'XYZ'; beck.apply_cam(cam, loc, look, lens, roll); beck.STATE['cam'] = V(loc)
        return loc, look, lens, roll

    def pose(self, g, actors_fn):
        self.clear(); self.ob = []
        self.set_cam(g)
        actors_fn(g, self)
        self.animate(g, self)
        self.sc.frame_set(1)
        bpy.context.view_layer.update()

    def render(self, gs, actors_fn, out_dir, samples=None, scale=None):
        os.makedirs(out_dir, exist_ok=True)
        if samples: self.sc.cycles.samples = samples
        if scale: self.sc.render.resolution_percentage = scale
        for g in gs:
            png = os.path.join(out_dir, 'g_%04d.png' % g)
            if os.path.exists(png): continue
            t0 = time.time(); self.pose(g, actors_fn)
            wall, cpu = TW.render(png + '.tmp.png', self.sc); os.replace(png + '.tmp.png', png)
            print('g %d  %.1f s wall %.1f s cpu (%.1f total)' % (g, wall, cpu, time.time() - t0), flush=True)


def parse(spec):
    out = []
    for part in spec.split(','):
        if ':' in part:
            a = [int(v) for v in part.split(':')]; out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        elif part: out.append(int(part))
    return out
