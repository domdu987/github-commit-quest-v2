"""c12.py -- helpers for film-12 take scripts: street.py set + per-frame cast12 cards (variants toggled by hide_render), camera moves, lip-sync from the narration."""
import os, sys, math, json, hashlib, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = '/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj'
for p in (PROJ + '/v3/set3d12', PROJ + '/v3/cast12', PROJ + '/v3/cast10'):
    if p not in sys.path: sys.path.insert(0, p)
import street as S, bpy
from mathutils import Vector
import cast12

def g_of(t): return int(round((t + 0.10) * 30))
def g_bound(t): return int(round(t * 30))

# ---- narration envelope -> mouth level per film frame
_ENV = None
def env(g):
    global _ENV
    if _ENV is None:
        w = wave.open(PROJ + '/film12/audio/narration.wav'); sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
        n = int(sr / 30); k = len(a) // n
        _ENV = np.sqrt((a[:k * n].reshape(k, n) ** 2).mean(1))
        _ENV = _ENV / (np.percentile(_ENV, 90) + 1e-9)
    i = g - 3                                    # narration starts at +0.10 s = 3 frames
    return float(_ENV[i]) if 0 <= i < len(_ENV) else 0.0

def mouth(g, lo=0.12):
    e = env(g)
    if e < lo: return 'flat'
    return cast12.talk_mouth(g, min(1.0, e), 1.0, 2)

# ---- camera
def lerp3(a, b, e): return tuple(x + (y - x) * e for x, y in zip(a, b))
def cam_setup(preset, u):
    c = S.CAMS[preset]
    return dict(loc=lerp3(c['loc'], c['loc_b'], u), look_at=lerp3(c['look_at'], c['look_b'], u), lens=c['lens'])
def ease(p): q = min(1.0, max(0.0, p)); return 0.35 * q * q * (3 - 2 * q) + 0.65 * p        # never dead at the ends; linear outside (handles)

def key_cam(g, setup):
    cam = S.make_camera(setup)
    cam.keyframe_insert('location', frame=g); cam.keyframe_insert('rotation_euler', frame=g)
    cam.data.keyframe_insert('lens', frame=g)
    return cam

# ---- per-frame cards
class Actor(object):
    """add(g, cast, pose, pos, ...) per frame, then bake(cam_pos_of_g): one card object per distinct drawing, shown by keyed hide_render."""
    def __init__(self, name): self.name = name; self.rec = {}
    def add(self, g, cast, pose, pos, mirror=False, rim=None, tint=None, roll=0.0, tilt=0.0, hide=False, over=None):
        self.rec[g] = (cast, dict(pose, **(over or {})), tuple(pos), mirror, rim, tint, roll, tilt, hide)
    def bake(self, campos, fa=None, fb=None):
        vars_ = {}
        for g, (cast, pose, pos, mirror, rim, tint, roll, tilt, hide) in self.rec.items():
            key = hashlib.sha1(repr((cast, sorted(pose.items(), key=lambda kv: kv[0]), mirror, rim, tint)).encode()).hexdigest()[:12]
            if key not in vars_:
                vars_[key] = S.cast_card('%s_%s' % (self.name, key), cast, pose, pos, None, rim=rim, tint=tint, mirror=mirror)
        for ob in vars_.values(): ob.hide_render = True
        gs = range(fa if fa is not None else min(self.rec), (fb if fb is not None else max(self.rec)) + 1)
        for g in gs:
            if g not in self.rec:
                for ob in vars_.values(): ob.hide_render = True; ob.keyframe_insert('hide_render', frame=g)
                continue
            cast, pose, pos, mirror, rim, tint, roll, tilt, hide = self.rec[g]
            key = hashlib.sha1(repr((cast, sorted(pose.items(), key=lambda kv: kv[0]), mirror, rim, tint)).encode()).hexdigest()[:12]
            cp = campos(g); d = Vector(cp) - Vector(pos); yaw = math.atan2(d.x, -d.y)
            for k, ob in vars_.items():
                ob.hide_render = hide or (k != key); ob.keyframe_insert('hide_render', frame=g)
                if k == key and not hide:
                    ob.location = pos; ob.rotation_euler = (math.radians(-tilt), math.radians(roll), yaw)
                    ob.keyframe_insert('location', frame=g); ob.keyframe_insert('rotation_euler', frame=g)
        for ob in vars_.values():
            for _, fc in S._fcs(ob):
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT' if fc.data_path == 'hide_render' else 'LINEAR'
        self.vars = vars_
        return vars_

def head_y(cam, pos, h): return S.project_px(cam, (pos[0], pos[1], pos[2] + h))

def walk(name, g, speed_cycle=36.0): return cast12.cycle_frame(name, (g / speed_cycle) % 1.0, facing=1)

def render_range(first, last, outdir, draft=False, shard=None):
    sc = bpy.context.scene; os.makedirs(outdir, exist_ok=True); import time
    for g in range(first, last + 1):
        if shard and (g % shard[1]) != shard[0]: continue
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p): continue
        sc.frame_set(g); t = time.time(); S.render(p + '.tmp.png'); os.replace(p + '.tmp.png', p)
        print('g %d  %.1f s' % (g, time.time() - t), flush=True)
