#!/usr/bin/env python3
"""film 14, take s21: shot 21 only (45.59-48.44 s, g1368-1452; take g1362-1458 with 6 handle frames each side). NIGHT, no elephant.
"one wire threads every hive, so a push in one place swings the whole row and the hives knock": camera low along the front row (units 3, 2, 1 side by side), a slow drift
toward unit 1, the swing wave arrives from screen-right and passes hive to hive; each hive slides into its OWN post and BANGS it (g1390 u3, g1410 u2, g1430 u1):
8-12 px jolt of the hive on the contact frame, 2-frame shake of posts + roofs, a spray crown of chips / droplets (150-200 px wide, fades over 8 frames).
Bees: none before g1442, then small puffs (leading into shot 22's burst). World / sky / lamps as team 4's shot 22 (plain NIGHT, lamps dimmed 0.12).
  python3 shot.py <g0> <g1> [preview|final] [outdir]   (resumable: skips finished frames)"""
import sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp
import bpy, numpy as np
from mathutils import Vector

PS = 14.0 + 10.25                    # push point arc (x 10.25, front row) = the push of shot 19/20
WAVE = 7.5                           # m/s: 5 m hive spacing = 20 frames between knocks
BANG = {3: 1390, 2: 1410, 1: 1430}   # unit -> frame of the contact
T_U3 = 1382                          # g at which the wave front reaches unit 3 (tau 0)
SLIDE = 0.26                         # m the hive slides along the wire into its post (hive end gap to the post)
LENS_END = 24

def tsec(g): return (PS and (abs(PS - (14 + 3.5)) / WAVE + 0.12)) + (g - T_U3) / 30.0          # wire sim seconds: unit 3's tau = 0 at T_U3
def cam_of(g):
    """leg 1 (g1362-1434): pull back along the row and drift toward unit 1 so units 3, 2, 1 knock in turn on screen; leg 2: ease into the start of shot 22 (unit 1, 24 mm)"""
    P0 = ((-17.2, 1.3, 1.05), (-2.6, 5.0, 1.25), 44.0); P1 = ((-10.4, 2.4, 1.25), (-7.8, 4.95, 1.5), 28.0); P2 = ((-9.0, 2.1, 1.3), (-6.4, 4.9, 1.45), 24.0)
    if g <= 1434:
        u = mv(clamp((g - 1362) / 72.0)); A, B = P0, P1
    else:
        u = clamp((g - 1434) / 18.0) * 0.8 + 0.2 * (clamp((g - 1434) / 18.0)) ** 2; A, B = P1, P2
    loc = tuple(lerp(a, b, u) for a, b in zip(A[0], B[0])); look = tuple(lerp(a, b, u) for a, b in zip(A[1], B[1]))
    return loc, look, lerp(A[2], B[2], u)

def hive_off(i, g):
    """metres the hive of unit i is displaced along the wire (toward -x, its downstream post) by the wave: eases in, hits at BANG, rebounds"""
    gb = BANG.get(i)
    if gb is None: return 0.0, 0
    a = g - gb
    if a < -9: return 0.0, 0
    if a <= 0: return SLIDE * (1 - (-a / 9.0) ** 2) , 0          # accelerates into the post
    if a == 0: return SLIDE, 0
    reb = SLIDE * (-0.18) * math.exp(-a / 3.0) * math.cos(a * 1.4)   # rebound + settle
    return SLIDE * 0.0 + reb, (1 if a <= 2 else 0)

def sprayfx(g, cam_loc, focal):
    verts = []; faces = []; mats = []; cam = Vector(cam_loc)
    for i, gb in BANG.items():
        a = (g - gb) / 30.0
        if a < 0.0 or a > 0.27: continue
        h = F.STATE['hive'][i]; mw = h.matrix_world
        c0 = mw @ Vector((-0.70, 0.0, -0.42))                       # the contact point: hive end against its post
        d = (c0 - cam).length; fwd = (c0 - cam).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd).normalized()
        k = (150.0 / focal * d) / 0.8                                # half-width 87 px -> 175 px crown at full res
        rr = random.Random(i * 91 + 3); f = 1.0 - a / 0.27
        for n in range(15):
            kind = 0 if n < 8 else (1 if n < 13 else 2)             # 8 chips, 5 droplets, 2 wisps
            ang = math.radians(rr.uniform(-52, 52)); sp = (rr.uniform(2.4, 3.6) if kind < 2 else rr.uniform(0.9, 1.4)) * k
            v0 = right * (math.sin(ang) * sp) + up * (math.cos(ang) * sp * (1.0 if kind < 2 else 1.2)) + fwd * rr.uniform(-0.3, 0.3)
            p = c0 + v0 * a + Vector((0, 0, -4.5 * a * a * k)); vel = v0 + Vector((0, 0, -9.0 * a * k))
            wx, wy = vel.dot(right), vel.dot(up); n_ = math.hypot(wx, wy) or 1.0; dd = (right * wx + up * wy) / n_; pp = (-right * wy + up * wx) / n_
            L, W = ((0.17, 0.07) if kind == 0 else (0.11, 0.07) if kind == 1 else (0.28, 0.05)); L *= 2.4 * max(0.7, k); W *= 2.4 * max(0.7, k)
            sz = f if kind < 2 else min(1.0, f * 1.4); Lh, Wh = L * sz / 2, W * sz / 2
            b = len(verts); verts += [tuple(p - dd * Lh - pp * Wh), tuple(p + dd * Lh - pp * Wh), tuple(p + dd * Lh + pp * Wh), tuple(p - dd * Lh + pp * Wh)]
            faces.append((b, b + 1, b + 2, b + 3)); mats.append(kind)
    return verts, faces, mats

_KM = {}
def spray_update(g, cam_loc, focal):
    ob = bpy.data.objects.get('knockfx')
    if ob is not None: me = ob.data; bpy.data.objects.remove(ob); bpy.data.meshes.remove(me)
    verts, faces, mats = sprayfx(g, cam_loc, focal)
    if not faces: return 0
    if not _KM:
        for k, (col, st) in enumerate((((0.85, 0.62, 0.38, 1), 2.2), ((0.95, 0.80, 0.55, 1), 2.0), ((0.85, 0.72, 0.52, 1), 0.9))):
            m = bpy.data.materials.new('kfx%d' % k); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
            e.inputs['Color'].default_value = col; e.inputs['Strength'].default_value = st
            if k == 2:
                tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.45
                nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs['Surface'])
            else: nt.links.new(e.outputs[0], o.inputs['Surface'])
            _KM[k] = m
    me = bpy.data.meshes.new('knockfx'); me.from_pydata(verts, [], faces); me.update()
    for k in range(3): me.materials.append(_KM[k])
    for p, mi in zip(me.polygons, mats): p.material_index = mi
    ob = bpy.data.objects.new('knockfx', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False
    return len(faces)

class Driver:
    def __init__(self, quality, threads):
        c0, l0, ln0 = cam_of(1368)
        C.register_preset('s21', c0, l0, ln0)
        F.WAVE_C = WAVE; C.SLEEP_N[0] = 0
        C.build('s21', quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=240)
        self.cam = C.Cam(); print('maize rows hidden', C.hide_maize_rows(8.0))
        pts = [cam_of(g)[0] for g in range(1362, 1459, 6)]
        C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
        C.cut_path(pts, 2.4, names=('grass', 'flowers', 'edge', 'pebbles'), keep=None)
        C.cut_path(pts, 2.2, names=('props',), zmax=5.0, keep=lambda w: w.y > 4.0)
        print('lamps dimmed', C.dim_lamps(pts[0], 16.0, 0.12), C.dim_lamps((-10.4, 0.5, 1.0), 9.0, 0.03))
        self.base = {i: (F.STATE['hive'][i].location.copy(), F.STATE['bar'][i].location.copy()) for i in F.STATE['hive']}
        self.shake = [o for o in bpy.data.objects if o.name.startswith(('posts_', 'roof'))]

    def frame(self, g, path):
        loc, look, lens = cam_of(g)
        shk = any(0 <= g - gb < 2 for gb in BANG.values())
        if shk: sh = 0.012 * (1 if g % 2 == 0 else -1); loc = (loc[0] + sh, loc[1], loc[2] + sh * 0.6); look = (look[0] + sh, look[1], look[2])
        self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        F.set_fence_stage(3); F.set_wire_push(tsec(g) / F.SEQ_T, PS); bpy.context.view_layer.update()
        focal = lens / 36.0 * 1280.0; jolt = {}
        for i, h in F.STATE['hive'].items():
            k = lerp(1.9, 1.0, sm((g - 1432) / 20.0)); h.scale = (k, k, k)        # hives x1.9 for readability, back to natural size at the cut into shot 22
            off, hit = hive_off(i, g)
            if off:
                tg = Vector((1, 0, 0)) if True else None; d = Vector((off, 0, 0))              # front-row wire runs along x
                h.location = h.location + d; F.STATE['bar'][i].location = F.STATE['bar'][i].location + d
            if g == BANG.get(i, -99):                                            # the jolt lands on the contact frame: 10 px
                dist = (Vector(h.location) - Vector(loc)).length; w = 10.0 / focal * dist
                h.location = h.location + Vector((w * 0.5, 0, w * 0.3)); jolt[i] = round(w, 3)
        if shk:
            r_ = random.Random(g); d = Vector((r_.uniform(-1, 1), 0, r_.uniform(-0.5, 0.5))) * (10.0 / focal * 10.0)
            for o in self.shake: o.location = d
        else:
            for o in self.shake: o.location = (0, 0, 0)
        bpy.context.view_layer.update()
        bs = (g - 1442) / 30.0                                                    # bees only from g1442: small puffs at the hives, leading into shot 22
        if bs < 0: F.set_bees(-1.0, 0.0, None, None)
        else: F.set_bees((3.3 + bs) / F.SEQ_T, 0.03 + 0.05 * clamp(bs / 0.4), None, None)
        bpy.context.view_layer.update()
        info = dict(fx=spray_update(g, loc, focal), jolt=jolt)
        for i in (1, 2, 3): info['u%d' % i] = C.screen(F.STATE['hive'][i].location)
        w, cpu = F.render(path); return w, cpu, info

if __name__ == '__main__':
    a = sys.argv[1:]; g0, g1 = int(a[0]), int(a[1]); q = a[2] if len(a) > 2 else 'preview'; outdir = a[3] if len(a) > 3 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(q, thr)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
