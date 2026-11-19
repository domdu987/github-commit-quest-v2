#!/usr/bin/env python3
"""film 14, take s20 v3: ONLY shots 20-21 (g 1301-1452). usage: python3 shot_v3.py <20|21> <g0> <g1> [preview|final] [outdir]
Shot 20 continues team 6's shot 19 (camera INSIDE the fence, push point x 6.0, max bow t 0.11 at g 1307), holds on her chest + the V for 12 frames, then slides along the wire past hives that start to swing.
Shot 21: wide 3/4 cut-away of the whole row, the swing wave runs hive to hive with a knock + puff each."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp
import bpy, numpy as np
from mathutils import Vector

PS = 20.0                           # push point arc (x 6.0 on the front row) = team 6's shot 19 v2
PXC = 6.0
HOLD_END = 1319                     # hold on the V until here, then the clock runs in real time
SW_K = [1.0]; SWT = [None]; ALT = [False]
def shot_of(g): return 20 if g < 1368 else 21
def clock(g):
    if g < 1368: return 0.55 if g < HOLD_END else 0.55 + (g - HOLD_END) / 30.0      # wire sim seconds (t 0.11 = max bow)
    return 0.2 + (g - 1368) * 0.03 * 0.9
def swing_clock(g):
    if g < 1368: return 0.30 if g < HOLD_END else 0.30 + (g - HOLD_END) / 30.0
    return None
def bee_clock(g):
    if g < 1368: return swing_clock(g)
    return -1.0 if g < 1438 else (12.5 / F.WAVE_C + 0.15) + (g - 1438) * 0.1

def mvx(u): return 0.65 * u if u < 0 else (1 + 0.65 * (u - 1) if u > 1 else mv(u))
def burst(g): return 0.0 if g < HOLD_END else (0.2 if g >= 1368 else 0.035)

def _hive_swing(s, t, s0=None):
    s = np.asarray(s, dtype=float)
    if t is None or t < 0: return np.zeros_like(s), np.zeros_like(s)
    s0 = F.PUSH_S0 if s0 is None else s0; d = F._ring_dist(s, s0); tt = SWT[0] if SWT[0] is not None else t * F.SEQ_T; tau = tt - d / F.WAVE_C - 0.12
    sg = np.ones_like(s)
    if ALT[0]:
        for k, ss in enumerate(s): sg[k] = (-1.0) ** min(F.UNITS, key=lambda u: abs(u['s'] - ss))['i']
    return sg * 0.85 * SW_K[0] * F._h(tau), 0.20 * np.where(tau <= 0, 0.0, np.sin(2 * math.pi * 1.7 * tau) * np.exp(-np.maximum(tau, 0) / 1.2))

def cam_of(g):
    if g < 1368:
        # open on team 6's last framing (inside the fence, wide lens, looking out at her chest), swing to a low oblique CLOSE on chest + V (V reads as a kink), hold, slide left along the bent wire
        p = sm((g - 1307) / 8.0); e = mvx((g - HOLD_END) / 48.0) if g >= HOLD_END else 0.0
        x0 = lerp(6.0, 3.0, p); y0 = lerp(11.5, 9.3, p); z0 = lerp(1.55, 1.1, p)
        loc = (lerp(x0, -6.0, e), lerp(y0, 7.6, e), lerp(z0, 1.5, e))
        look = (lerp(lerp(6.0, 6.5, p), loc[0] - 2.4, e), lerp(5.0, 5.2, e), lerp(lerp(2.6, 2.1, p), 1.9, e))
        if g < 1307: loc = (loc[0] + 0.02 * (1307 - g), loc[1] + 0.04 * (1307 - g), loc[2])      # handle frames drift slightly (never frozen)
        return loc, look, lerp(lerp(20, 24, p), 28, e)
    # shot 21 v6: the look point follows the hive being knocked (u3 g1388, u2 1405, u1 1422, u0 1438) so every hit lands mid-frame, camera 41 deg to the row, low, pitched up
    kn = [(1368, 6.4), (1388, 3.5), (1405, -1.5), (1422, -6.5), (1438, -11.5), (1452, -12.6)]
    for (g0, x0), (g1, x1) in zip(kn, kn[1:]):
        if g <= g1:
            u = clamp((g - g0) / float(g1 - g0)); u = u * u * (3 - 2 * u) * 0.8 + u * 0.2; fx = lerp(x0, x1, u); break
    else: fx = kn[-1][1]
    return (fx - 4.2, 1.4, 0.6), (fx, 5.0, 1.9), 50

def hive_scale(cam_loc, h): return 1.5

BANG = {3: 1388, 2: 1405, 1: 1422, 0: 1438}      # unit -> frame the swing peaks and the hive BANGS into its own post/frame (wave front u3 g1381, u2 1398, u1 1415, u0 1431)

def knock_mesh(g, cam_loc):
    """spray CROWN at each bang: 12 wood chips + 14 droplets thrown in a ~110 deg upward cone (speed + gravity, thin shards stretched along their motion) + 2 thin wisps; fades over 8 frames"""
    import random
    verts = []; faces = []; mats = []
    cam = Vector(cam_loc)
    for i, gb in BANG.items():
        a = (g - gb) / 30.0
        if a < 0.03 or a > 0.27: continue
        h = F.STATE['hive'][i]; mw = h.matrix_world; sg = 1.0 if i % 2 == 0 else -1.0
        c0 = mw @ Vector((0.67 * sg, 0.0, -0.45))
        fwd = (c0 - cam).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
        rr = random.Random(i * 77 + 5); f = 1.0 - a / 0.27
        for k in range(28):
            kind = 0 if k < 12 else (1 if k < 26 else 2)
            ang = math.radians(rr.uniform(-55, 55)); sp = rr.uniform(2.4, 3.6) if kind < 2 else rr.uniform(0.8, 1.4)
            v0 = right * (math.sin(ang) * sp) + up * (math.cos(ang) * sp * (1.0 if kind < 2 else 1.3)) + fwd * rr.uniform(-0.3, 0.3)
            vel = v0 + Vector((0, 0, -9.0 * a)); p = c0 + v0 * a + Vector((0, 0, -4.5 * a * a))
            wx, wy = vel.dot(right), vel.dot(up); n_ = math.hypot(wx, wy) or 1.0; d = (right * wx + up * wy) / n_; pp = (-right * wy + up * wx) / n_
            L, W = ((0.13, 0.05) if kind == 0 else (0.08, 0.05) if kind == 1 else (0.55, 0.035))
            sz = f if kind < 2 else min(1.0, f * 1.4)
            Lh, Wh = L * sz / 2, W * sz / 2
            b = len(verts); verts += [tuple(p - d * Lh - pp * Wh), tuple(p + d * Lh - pp * Wh), tuple(p + d * Lh + pp * Wh), tuple(p - d * Lh + pp * Wh)]
            faces.append((b, b + 1, b + 2, b + 3)); mats.append(kind)
    return verts, faces, mats

_KMATS = {}
def knock_update(g, cam_loc):
    ob = bpy.data.objects.get('knockfx')
    if ob is not None:
        me = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me)
    verts, faces, mats = knock_mesh(g, cam_loc)
    if not faces: return 0
    if not _KMATS:
        for k, (col, st) in enumerate((((0.85, 0.62, 0.38, 1), 2.2), ((1.0, 0.95, 0.85, 1), 2.6), ((0.85, 0.72, 0.52, 1), 0.9))):
            m = bpy.data.materials.new('kfx%d' % k); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
            e.inputs['Color'].default_value = col; e.inputs['Strength'].default_value = st
            if k == 2:
                tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.45
                nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs['Surface'])
            else: nt.links.new(e.outputs[0], o.inputs['Surface'])
            _KMATS[k] = m
    me = bpy.data.meshes.new('knockfx'); me.from_pydata(verts, [], faces); me.update()
    for k in range(3): me.materials.append(_KMATS[k])
    for p, mi in zip(me.polygons, mats): p.material_index = mi
    ob = bpy.data.objects.new('knockfx', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    return len(faces)

class Driver:
    def __init__(self, shot, quality, threads):
        self.shot = shot
        c0, l0, ln0 = cam_of(1310 if shot == 20 else 1370)
        C.register_preset('v3s%d' % shot, c0, l0, ln0)
        F.hive_swing = _hive_swing; ALT[0] = (shot == 21)
        if shot == 21: C.SLEEP_N[0] = 0
        C.build('v3s%d' % shot, quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=240)
        self.cam = C.Cam(); C.darken_mat('tinunder', 0.62 if shot == 20 else 0.40); C.darken_mat('woodpale', 0.8)
        if shot == 21:
            C.darken_mat('winlit', 0.3); C.darken_mat('lamp', 0.3)
            for o in bpy.data.objects:
                if o.name.startswith('props_winlit'): o.hide_render = True
            print('hut lamps dimmed', C.dim_lamps((20.0, 12.0, 1.5), 16.0, 0.08))
            nm = bpy.data.materials.new('roofunder21'); nm.use_nodes = True; pb = [n for n in nm.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
            pb.inputs['Base Color'].default_value = (0.30, 0.17, 0.10, 1); pb.inputs['Roughness'].default_value = 0.7
            pb.inputs['Emission Color'].default_value = (0.55, 0.30, 0.14, 1); pb.inputs['Emission Strength'].default_value = 0.22
            nt2 = bpy.data.materials.new('roofout21'); nt2.use_nodes = True; pb2 = [n for n in nt2.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'][0]
            pb2.inputs['Base Color'].default_value = (0.30, 0.31, 0.34, 1); pb2.inputs['Roughness'].default_value = 0.6; pb2.inputs['Emission Color'].default_value = (0.5, 0.35, 0.25, 1); pb2.inputs['Emission Strength'].default_value = 0.12
            for ob in bpy.data.objects:
                if ob.type == 'MESH' and ob.name.startswith('roof'):
                    for sl in ob.material_slots:
                        if sl.material is not None and sl.material.name.startswith('tinunder'): sl.material = nm
                        elif sl.material is not None and sl.material.name.startswith('tin') and not sl.material.name.startswith('tinunder'): sl.material = nt2
            nt = bpy.context.scene.world.node_tree
            for n in nt.nodes:
                if n.type == 'BACKGROUND': n.inputs['Strength'].default_value *= 0.4
                if n.type == 'MATH' and n.operation == 'MULTIPLY' and abs(n.inputs[1].default_value - 16.0) < 1e-6: n.inputs[1].default_value = 40.0
        pts = [cam_of(g)[0] for g in range(1301 if shot == 20 else 1368, 1368 if shot == 20 else 1453, 6)]
        if shot == 20:
            print('maize hidden', C.hide_maize_rows(15.0)); C.cut_boxes([(2.5, 10.0, 5.6, 16.0, 4.5)])
            print('trees cut', C.cut_roofs(2, 30, 6.0, 90, zmin=-1.0, prefix='trees_'), C.cut_roofs(2, 30, 6.0, 90, zmin=-1.0, prefix='scrub_acacia'))
            print('roof cut u3/u4', C.cut_roofs(2.0, 10.0, 3.0, 8.0))
            print('mountains hidden', sum(1 for o in bpy.data.objects if 'mount' in o.name.lower() and not setattr(o, 'hide_render', True)))
            C.cut_boxes([(4.2, 5.7, 1.9, 3.3, 9.0)]); print('lamps dimmed', C.dim_lamps((4.0, 8.0, 2.0), 12.0, 0.3))
            C.cut_path(pts, 1.4, names=('grass', 'flowers', 'edge', 'pebbles'), keep=None)
            self.mat = C.matriarch_card(128); self.mat.grade = True
        else:
            self.mat = None
            C.hide_maize_rows(8.0); print('mountains hidden', sum(1 for o in bpy.data.objects if 'mount' in o.name.lower() and not setattr(o, 'hide_render', True)))
            C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
            C.cut_path(pts, 2.6, names=('grass', 'flowers', 'edge', 'pebbles'), keep=None)
            C.cut_path(pts, 2.6, names=('props',), zmax=5.0, keep=lambda w: w.y > 4.0)
            print('lamps dimmed', C.dim_lamps((-8.0, 3.0, 2.0), 26.0, 0.12))

    def frame(self, g, path):
        shot = self.shot
        loc, look, lens = cam_of(g)
        if shot == 21 and any(0 <= g - gb < 2 for gb in BANG.values()):         # 2-frame camera shake (about 4 px)
            sh = 0.02 * (1 if g % 2 == 0 else -1); loc = (loc[0] + sh, loc[1], loc[2] + sh * 0.7); look = (look[0] + sh, look[1], look[2])
        self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        t = clock(g); SWT[0] = swing_clock(g)
        F.set_fence_stage(3); F.set_wire_push(t / F.SEQ_T, PS)
        if shot == 21:
            for i, h in F.STATE['hive'].items(): k = hive_scale(loc, h); h.scale = (k, k, k)
        if shot == 21:
            import random
            for i, gb in BANG.items():
                if 0 <= g - gb < 2:                                       # 2-frame jolt of the hive, its bar, the posts and roofs
                    rr = random.Random(g * 13 + i); h = F.STATE['hive'][i]; bq = F.STATE['bar'][i]; s = 0.065 if g == gb else 0.04
                    d = Vector((rr.uniform(-s, s), rr.uniform(-s, s), rr.uniform(-s, s) * 0.6)); h.location += d; bq.location += d
                    for o in bpy.data.objects:
                        if o.name.startswith(('posts_', 'roof')): o.location = d * 0.5 * (1 if o.name.startswith('posts_') else 1)
            if not any(0 <= g - gb < 2 for gb in BANG.values()):
                for o in bpy.data.objects:
                    if o.name.startswith(('posts_', 'roof')): o.location = (0, 0, 0)
        bpy.context.view_layer.update()
        info = {}
        if self.mat is not None:
            te = t / F.SEQ_T
            bow = float(F.wire_disp(np.array([PS]), te, PS)[0])
            c, pp = C.story('matriarch_push'); p = dict(pp); p['push'] = 1.0; p['lean'] = 4.0; p['head_dip'] = 9; p['ear_flare'] = 0.15; p['t'] = 0.2 + g * 0.01
            r = self.mat.sprite(p, '%04d' % g)
            cy = 5.0 + bow - 0.5; dxx, dyy = loc[0] - PXC, loc[1] - cy
            yaw = math.pi - math.atan2(dxx, dyy)
            self.mat.put_anchor('chest_push', (PXC, cy), yaw)
            hd = C.screen(self.mat.world('head')); tp = C.screen(self.mat.world('trunk_tip')); info = dict(head=hd, trunk=tp, chest=C.screen(self.mat.world('chest_push')))
            if hd[0] < -40 or hd[0] > 760: self.mat.hide()          # no stray trunk / ear sliding along the wire once her head has left the frame
        bpy.context.view_layer.update()
        bc = bee_clock(g); F.set_bees(bc / F.SEQ_T if bc >= 0 else -1.0, burst(g), None, None)
        bpy.context.view_layer.update()
        if shot == 21: info['fx'] = knock_update(g, loc)
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; shot = int(a[0]); g0 = int(a[1]); g1 = int(a[2]); q = a[3] if len(a) > 3 else 'preview'; outdir = a[4] if len(a) > 4 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(shot, q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
