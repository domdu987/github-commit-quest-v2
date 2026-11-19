#!/usr/bin/env python3
"""film 14 take s19: shots 19-20 (THE PUSH), g 1226-1367 + 6 handle frames each side (g 1220-1373). Night.
  usage: python3 shot.py <shot 19|20> <g0> <g1> [preview|final] [outdir]       (one shot = one process = one set build)
Director brief: head-UP pose, the wire crosses her CHEST (the span of wire is lowered locally to her chest), a CLEAR V bow, hives tilt; shot 20 a different low
angle along the wire, hold the V ~12 frames then release it into the wave down the row; same night grade, NO bees, wire 3 cm matte grey-silver."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp, cast14
import bpy, numpy as np
from mathutils import Vector

PX = float(os.environ.get('PX', 6.0)); PS0 = 14.0 + PX        # push point (front row x 6.0, mid-span between units 3 and 4: posts at 4.5 / 7.5)
CUT20, G_FIRST, G_LAST = 1307, 1220, 1373
G_CONTACT, G_PUSH0, G_HOLD1 = 1226, 1236, 1318               # she reaches the wire at G_CONTACT; the bow grows G_PUSH0..1306 and is held to 1318; released at 1319
B_MAX = float(os.environ.get('BMAX', 0.9)); LH = 1.9        # bow depth (m) and V half-width (m)
DZ = float(os.environ.get('DZ', -0.2)); C_W = 7.0            # wire lowered to her chest at the push point; wave speed along the row (m/s)
CUR = {'g': 1220}

def bow_amp(g): return B_MAX * sm((g - G_PUSH0) / (1306.0 - G_PUSH0)) if g < 1307 else B_MAX
def t_rel(g): return (g - (G_HOLD1 + 1)) / 30.0              # seconds since the release (< 0 : held)

def wire_disp(s, t, s0=None):
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s)
    g = CUR['g']; d = F._ring_dist(s, PS0); env = 1 - 0.7 * np.exp(-(F._post_dist(s) / 0.45) ** 2)
    B = bow_amp(g); V = np.clip(1 - d / LH, 0, None) ** 1.15; tt = t_rel(g)
    if tt < 0: return B * env * V
    ring = math.cos(2 * math.pi * 1.1 * tt) * math.exp(-tt / 1.3)
    tw = tt - np.maximum(d - 1.0, 0) / C_W; wave = np.where(tw > 0, np.cos(2 * math.pi * 1.1 * tw) * np.exp(-np.maximum(tw, 0) / 1.6) * np.minimum(tw / 0.12, 1.0), 0.0)
    return B * env * V * ring + 0.55 * np.exp(-d / 25.0) * env * np.where(d > 1.2, 1.0, 0.0) * wave

def hive_swing(s, t, s0=None):
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s), np.zeros_like(s)
    g = CUR['g']; d = F._ring_dist(s, PS0); tt = t_rel(g)
    if tt < 0: return 0.55 * (bow_amp(g) / B_MAX) ** 1.5 * np.exp(-d / 14.0), 0.05 * (bow_amp(g) / B_MAX) * np.exp(-d / 14.0)
    tw = tt - np.maximum(d - 1.0, 0) / C_W - 0.05; fall = np.exp(-np.maximum(tw, 0) / 1.8)
    ang = np.where(tw <= 0, 0.34 * np.exp(-d / 14.0), 0.85 * np.exp(-d / 30.0) * np.cos(2 * math.pi * 0.95 * tw) * fall + 0.34 * np.exp(-d / 14.0) * np.exp(-np.maximum(tw, 0) / 0.5))
    return ang, 0.18 * np.exp(-d / 30.0) * np.where(tw <= 0, 0.0, np.sin(2 * math.pi * 1.7 * tw) * fall)

# ----------------------------------------------------------------------------- cameras (field side: the wire is between the camera and her chest)
def cam19(g):
    u = clamp((g - G_FIRST) / 86.0); e = mv(u)
    return (lerp(7.8, 7.1, e), lerp(9.4, 8.8, e), lerp(1.5, 1.55, e)), (lerp(5.9, 5.9, e), 5.3, lerp(1.45, 1.6, e)), lerp(22.0, 24.0, e)
def cam20(g):
    u = clamp((g - CUT20) / 66.0); e = mv(u)
    loc = (lerp(10.3, 7.0, e), lerp(7.0, 6.3, e), lerp(1.35, 1.45, e))
    look = (lerp(5.8, 1.8, e), lerp(5.2, 5.0, e), lerp(2.0, 2.0, e))
    return loc, look, lerp(24.0, 22.0, e)
CAM = {19: cam19, 20: cam20}

# ----------------------------------------------------------------------------- elephant
def mat_pose(g, ph):
    """FRONT view (head-on, head UP, the wire crosses her chest under the chin); the trunk hangs; a small step bob"""
    w = sm((g - G_PUSH0) / (1306.0 - G_PUSH0)); k = g - G_FIRST
    p = dict(view='front', expr='grumpy', trunk='hang', ear_flare=0.12 + 0.08 * w, t=0.2 + g * 0.012, head_dip=0.0)
    p['squash'] = [1.0, 1.0 + 0.012 * math.sin(ph * 6.283 * 2) * (1.0 if g < 1307 else 0.3)]
    p['blink'] = C.cast14.blink_at(g, 90, 3) if hasattr(C.cast14, 'blink_at') else 0
    if g > G_HOLD1: p['ear_flare'] = min(0.5, 0.2 + 0.3 * sm((g - G_HOLD1) / 8.0)); p['head_dip'] = -3.0 * sm((g - G_HOLD1) / 8.0)
    return 'matriarch', p

class Driver:
    def __init__(self, shot, quality, threads):
        self.shot = shot
        C.register_preset('s19', CAM[shot](G_FIRST if shot == 19 else CUT20)[0], CAM[shot](G_FIRST if shot == 19 else CUT20)[1], CAM[shot](G_FIRST if shot == 19 else CUT20)[2])
        F.hive_swing = hive_swing; F.wire_disp = wire_disp
        C.build('s19', quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=90)
        self.cam = C.Cam(); sc = bpy.context.scene
        W = F.STATE['wire']; S = W['S']; d = F._ring_dist(S, PS0); w = np.clip(1 - d / 1.5, 0, 1); w = w * w * (3 - 2 * w); W['base'][:, 2] -= DZ * w     # the span lowered to her chest
        for o in bpy.data.objects:
            if o.name == 'bees': o.hide_render = True
        try: C.darken_mat('tinunder', 0.35)
        except Exception as e: print('tinunder', e)
        pts = [CAM[shot](g)[0] for g in range(G_FIRST if shot == 19 else CUT20, (1306 if shot == 19 else G_LAST) + 1, 6)]
        print('maize rows hidden', C.hide_maize_rows(float(os.environ.get('MZ', 7.5))))
        C.cut_path(pts, 1.6, keep=lambda w: w.y > 3.0 and w.y < 6.6 and w.x > -14.0 and w.x < 11.5 and False)
        if shot == 20: print('roof cut', C.cut_roofs(7.0, 10.3, 3.0, 8.0), 'post cut', C.cut_roofs(9.2, 9.8, 3.0, 6.0, zmin=-1.0, prefix='posts_'))
        self.mat = C.Card('mat', 'matriarch', cast14.CANVAS14_FRONT['matriarch'], 128, contact=(1.0 * C.MPD * 7, 0.30 * C.MPD * 7)); self.mat.grade = True; self.ph = 0.0; self.first = True
    def frame(self, g, path):
        CUR['g'] = g; loc, look, lens = CAM[self.shot](g); self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        F.set_fence_stage(3); F.set_wire_push(0.2, PS0)                    # t >= 0 enables the patched wire_disp; the patch ignores t
        for o in bpy.data.objects:
            if o.name == 'bees': o.hide_render = True
        # elephant: chest anchor on the wire apex
        self.ph = 0.021 * min(g - 1219, 26) + 0.01 * max(0, g - 1245)
        cast_, pose = mat_pose(g, self.ph); r = self.mat.sprite(pose, '%04d' % g)
        apex_y = 5.0 - F.WIRE_OFF + float(F.wire_disp(np.array([PS0]), 0.2)[0]); gap = lerp(0.7, 0.0, sm((g - G_FIRST) / float(G_CONTACT - G_FIRST))) if g < G_CONTACT else 0.0
        cx, cy = PX, apex_y - gap - float(os.environ.get('OFF', 0.9))
        yaw = float(os.environ.get('YAWK', 1.0)) * C.yaw_to(loc, (cx, cy, 1.4))
        self.mat.put_anchor('chest_push', (cx, cy), yaw)
        ch = self.mat.world('chest_push'); info = dict(head=C.screen(self.mat.world('head')), chest=C.screen(ch), chest_z=round(ch.z, 2), apex_y=round(apex_y, 2))
        bpy.context.view_layer.update()
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; shot = int(a[0]); g0 = int(a[1]); g1 = int(a[2]); q = a[3] if len(a) > 3 else 'preview'; outdir = a[4] if len(a) > 4 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2')); d = Driver(shot, q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
