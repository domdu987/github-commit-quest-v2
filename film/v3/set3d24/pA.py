#!/usr/bin/env python3
"""joseon.py : set of film 24 ("ไอ้เรือเต่า": Admiral Yi Sun-sin's turtle ship, Joseon Korea 1592) as a real 3D Blender set, PATH-TRACED
(bpy 5.x, Cycles CPU, GI, Principled materials, thin volumetric haze, DOF allowed), after the client's R9 look (qtest/r9_scene.py).
Characters are 2D puppet cards (emission to camera, unlit, they cast shadows); everything else is lit by one soft warm sun + a gradient sky.

    import joseon as J
    A = J.build('yard', 'roof_low')      # yard: roof_low | bow | yard_wide | roof_top | macro_spikes | macro_dragon
    A = J.build('sea', 'fleet_wide')     # sea : fleet_wide flag_deck flag_deck_b flag_deck_crew hansan_high flag_bow chase board reveal_top aftermath shore macro_oar
    cam = J.make_camera(A['cam']); J.set_spikes(2, frame=10); J.set_ports(1); J.set_fleet_chase(s); J.set_korean_turn(k) ...
World: 1 unit = 1 D (head), Z up. See API.md.   CLI: python3 joseon.py final|stills [spec ...]   (render 75 % + post upscale)"""
import os, sys, math, json, time, random, subprocess
import numpy as np
import bpy
from mathutils import Vector, Matrix, Quaternion

HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'),
          os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7'), os.path.join(PROJ, 'v3', 'set3d10')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402  (MB mesh builder, placeholder_actor cards, keys)
import joseon_tex as JX                                    # noqa: E402
MB = T.MB; hexl = T.hex_lin
WORK = os.path.join(HERE, 'joseon_work')
S = {}                                                      # scene state (reset by build)
FPS = 30
CHASE_V = 3.0                                               # Japanese fleet speed, D / s (hook set_fleet_chase(s) moves them +x by CHASE_V * s)
def rnd(seed): return random.Random(seed)
def V(*a): return Vector(a)

# ============================================================================= node helpers
class NB:
    def __init__(s, m):
        s.m = m; m.use_nodes = True; s.nt = m.node_tree
        for n in list(s.nt.nodes):
            if n.type != 'OUTPUT_MATERIAL': s.nt.nodes.remove(n)
        s.out = [n for n in s.nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]
    def n(s, kind, **kw):
        nd = s.nt.nodes.new(kind)
        for k, v in kw.items(): setattr(nd, k, v)
        return nd
    def l(s, a, b): s.nt.links.new(a, b)
    def put(s, sock, v):
        if isinstance(v, bpy.types.NodeSocket): s.l(v, sock)
        else: sock.default_value = (*v, 1.0) if isinstance(v, (tuple, list)) and len(v) == 3 and sock.type == 'RGBA' else v
    def math(s, op, a, b=0.0, clamp=False):
        n = s.n('ShaderNodeMath', operation=op, use_clamp=clamp); s.put(n.inputs[0], a); s.put(n.inputs[1], b); return n.outputs[0]
    def rng(s, v, a, b, c=0.0, d=1.0, clamp=True, smooth=False):
        n = s.n('ShaderNodeMapRange', interpolation_type='SMOOTHSTEP' if smooth else 'LINEAR', clamp=clamp); s.put(n.inputs['Value'], v)
        for k, x in (('From Min', a), ('From Max', b), ('To Min', c), ('To Max', d)): n.inputs[k].default_value = x
        return n.outputs['Result']
    def mix(s, fac, a, b):
        n = s.n('ShaderNodeMix', data_type='RGBA'); s.put(n.inputs[0], fac); s.put(n.inputs[6], a); s.put(n.inputs[7], b); return n.outputs[2]
    def mul(s, a, b):
        n = s.n('ShaderNodeMix', data_type='RGBA', blend_type='MULTIPLY'); n.inputs[0].default_value = 1.0; s.put(n.inputs[6], a); s.put(n.inputs[7], b); return n.outputs[2]
    def coord(s, k='Object'): return s.n('ShaderNodeTexCoord').outputs[k]
    def noise(s, scale, detail=3.0, rough=0.55, vec=None, mapscale=None):
        n = s.n('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = scale; n.inputs['Detail'].default_value = detail; n.inputs['Roughness'].default_value = rough
        v = vec if vec is not None else s.coord()
        if mapscale: mp = s.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = mapscale; s.l(v, mp.inputs['Vector']); v = mp.outputs[0]
        s.l(v, n.inputs['Vector']); return n.outputs['Fac']
    def bump(s, h, strength, dist=0.1):
        b = s.n('ShaderNodeBump'); b.inputs['Strength'].default_value = strength; b.inputs['Distance'].default_value = dist; s.l(h, b.inputs['Height']); return b.outputs['Normal']
    def princ(s, col, rough=0.6, metal=0.0, normal=None, **kw):
        p = s.n('ShaderNodeBsdfPrincipled'); s.put(p.inputs['Base Color'], col if isinstance(col, bpy.types.NodeSocket) else (*col, 1.0)); s.put(p.inputs['Roughness'], rough)
        p.inputs['Metallic'].default_value = metal
        if normal is not None: s.l(normal, p.inputs['Normal'])
        for k, v in kw.items(): s.put(p.inputs[k], v)
        s.l(p.outputs[0], s.out.inputs['Surface']); return p
    def img(s, key, scale=1.0, proj='BOX', vec=None, cs='sRGB', ext='REPEAT'):
        t = s.n('ShaderNodeTexImage'); t.image = bpy.data.images.load(S['tx'][key], check_existing=True); t.image.colorspace_settings.name = cs
        t.projection = proj; t.extension = ext
        if proj == 'BOX': t.projection_blend = 0.25
        v = vec if vec is not None else s.coord()
        mp = s.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale, scale); s.l(v, mp.inputs['Vector']); s.l(mp.outputs[0], t.inputs['Vector']); return t

def mat(name, build=None):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); b = NB(m)
    if build: build(b)
    return m

def flat(name, hexcol, rough=0.7, metal=0.0, **kw):
    """Plain principled colour (hex sRGB)."""
    def f(b): b.princ(hexl(hexcol), rough, metal, **kw)
    return mat('J_' + name, f)

def tint(h, k): c = hexl(h); return tuple(min(1.0, x * k) for x in c)

def wood(name, base='#976c4d', dark='#6a4630', scale=1.25, axis='Z', rough=0.72, waterline=False, bumpk=0.35):
    """Plank wood by object-space nodes: seams between boards (wave bands along `axis`), stretched grain noise, bump, optional dark wet waterline."""
    def f(b):
        c = b.coord(); w = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction=axis, wave_profile='SAW'); w.inputs['Scale'].default_value = scale
        w.inputs['Distortion'].default_value = 0.5; w.inputs['Detail'].default_value = 1.0; b.l(c, w.inputs['Vector'])
        ms = (0.4, 9.0, 9.0) if axis == 'Z' else (9.0, 0.4, 9.0) if axis == 'Y' else (9.0, 9.0, 0.4)
        gr = b.noise(2.5, 3.0, 0.6, c, ms); seam = b.rng(w.outputs['Fac'], 0.0, 0.07, 0.0, 1.0)
        col = b.mix(b.rng(gr, 0.3, 0.7), hexl(base), hexl(dark)); col = b.mix(seam, tint(dark, 0.45) + (1.0,), col)
        if waterline:
            z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); wl = b.rng(z.outputs['Z'], 0.05, 0.45); col = b.mix(wl, hexl('#4a2a20'), col)
        nrm = b.bump(b.math('ADD', gr, b.math('MULTIPLY', seam, 0.8)), bumpk, 0.08)
        b.princ(col, rough, 0.0, nrm)
    return mat('J_w_%s' % name, f)

def imgmat(name, key, scale=0.25, proj='BOX', rough=0.8, metal=0.0, bumpk=0.25, tintc=None, uv=False):
    def f(b):
        t = b.img(key, scale, 'FLAT' if uv else proj, vec=None if not uv else b.n('ShaderNodeUVMap').outputs[0])
        if uv:                                              # UV mapped: undo the mapping node scale so UV 0..1 is the tile
            pass
        col = t.outputs['Color']
        if tintc: col = b.mul(col, (*hexl(tintc), 1))
        h = b.n('ShaderNodeRGBToBW'); b.l(t.outputs['Color'], h.inputs[0])
        b.princ(col, rough, metal, b.bump(h.outputs[0], bumpk, 0.05) if bumpk else None)
    return mat('J_i_%s' % name, f)

def emit(name, hexcol, k=8.0):
    def f(b):
        e = b.n('ShaderNodeEmission'); e.inputs['Color'].default_value = (*hexl(hexcol), 1); e.inputs['Strength'].default_value = k; b.l(e.outputs[0], b.out.inputs['Surface'])
    return mat('J_e_' + name, f)

def flagmat(key):
    def f(b):
        t = b.img(key, 1.0, 'FLAT', vec=b.n('ShaderNodeUVMap').outputs[0], ext='CLIP'); mp = [n for n in b.nt.nodes if n.type == 'MAPPING'][0]
        d = b.n('ShaderNodeBsdfDiffuse'); b.l(t.outputs['Color'], d.inputs['Color']); tr = b.n('ShaderNodeBsdfTranslucent'); b.l(t.outputs['Color'], tr.inputs['Color'])
        mx = b.n('ShaderNodeMixShader'); mx.inputs[0].default_value = 0.35; b.l(d.outputs[0], mx.inputs[1]); b.l(tr.outputs[0], mx.inputs[2])
        tp = b.n('ShaderNodeBsdfTransparent'); m2 = b.n('ShaderNodeMixShader'); b.l(t.outputs['Alpha'], m2.inputs[0]); b.l(tp.outputs[0], m2.inputs[1]); b.l(mx.outputs[0], m2.inputs[2])
        b.l(m2.outputs[0], b.out.inputs['Surface'])
    return mat('J_f_' + key, f)

def smoke_mat(name, hexcol, k=1.0):
    """Cartoon smoke billow: matte, slightly translucent-looking soft white-grey with a warm lit side (principled, rough 1)."""
    def f(b): b.princ(hexl(hexcol), 1.0, 0.0, None, **{'Subsurface Weight': 0.15})
    return mat('J_s_' + name, f)

def tx_sync(): S['tx'] = JX.ensure(verbose=False)

# ============================================================================= mesh helpers
def mk(mb, name, parent=None, coll=None, smooth=False, shadow=True, loc=None):
    o = mb.obj(name, coll or S['coll'], smooth=smooth)
    if parent is not None: o.parent = parent
    if loc is not None: o.location = loc
    if not shadow: o.visible_shadow = False
    return o

def empty(name, parent=None, loc=(0, 0, 0), rot=None):
    o = bpy.data.objects.new(name, None); S['coll'].objects.link(o); o.location = loc
    if rot is not None: o.rotation_euler = rot
    if parent is not None: o.parent = parent
    return o

def obox(mb, c, X, Y, Z, hx, hy, hz, m):
    c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); mb.pid += 1
    for (n, a, b, ha, hb, hn) in ((X, Y, Z, hy, hz, hx), (-X, Y, Z, hy, hz, hx), (Y, X, Z, hx, hz, hy), (-Y, X, Z, hx, hz, hy), (Z, X, Y, hx, hy, hz), (-Z, X, Y, hx, hy, hz)):
        o = c + n * hn; pts = [o - a * ha - b * hb, o + a * ha - b * hb, o + a * ha + b * hb, o - a * ha + b * hb]
        mb.oface(pts, m, [(0, 0), (1, 0), (1, 1), (0, 1)], n)

def bx(mb, lo, hi, m): mb.box(lo, hi, m)
def cbox(mb, c, hx, hy, hz, m): mb.box((c[0] - hx, c[1] - hy, c[2] - hz), (c[0] + hx, c[1] + hy, c[2] + hz), m)
def beam(mb, p0, p1, w, h, m, up=(0, 0, 1)):
    p0, p1 = Vector(p0), Vector(p1); X = p1 - p0; Ln = X.length; X.normalize(); Y = Vector(up).cross(X)
    if Y.length < 1e-4: Y = Vector((0, 1, 0)).cross(X)
    Y.normalize(); Z = X.cross(Y); obox(mb, (p0 + p1) / 2, X, Y, Z, Ln / 2, w / 2, h / 2, m)
def rod(mb, p0, p1, r, m, seg=8, r1=None): mb.frustum(p0, p1, r, r if r1 is None else r1, m, seg=seg)
def cone(mb, base, tip, r, m, seg=6): mb.frustum(base, tip, r, 0.0, m, seg=seg, cap1=False)

def ell(mb, c, rx, ry, rz, m, seg=12, rings=8, axes=None):
    """Ellipsoid (optionally rotated: axes = (X, Y, Z) unit vectors)."""
    c = Vector(c); X, Y, Z = axes or (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; R.append([c + X * (rx * math.sin(th) * math.cos(2 * math.pi * i / seg)) + Y * (ry * math.sin(th) * math.sin(2 * math.pi * i / seg)) - Z * (rz * math.cos(th)) for i in range(seg)])
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], m)

def lump(mb, c, r, m, seed, seg=10, rings=6, rough=0.2, squash=1.0):
    rs = rnd(seed); c = Vector(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = math.pi * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; d = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), -math.cos(th) * squash))
            row.append(c + d * r * (1 + rs.uniform(-rough, rough)) if 0 < k < rings else c + d * r)
        if k in (0, rings): row = [row[0]] * seg
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], m)

def torus(mb, c, R, r, m, segs=18, sides=6, tilt=0.0):
    c = Vector(c); pts = []
    for i in range(segs):
        a = 2 * math.pi * i / segs; ctr = Vector((R * math.cos(a), R * math.sin(a), 0)); rad = Vector((math.cos(a), math.sin(a), 0)); ring = []
        for j in range(sides):
            b = 2 * math.pi * j / sides; ring.append(c + ctr + rad * (r * math.cos(b)) + Vector((0, 0, r * math.sin(b))))
        pts.append(ring)
    mb.pid += 1
    for i in range(segs):
        for j in range(sides):
            i2, j2 = (i + 1) % segs, (j + 1) % sides; mb.face([pts[i][j], pts[i2][j], pts[i2][j2], pts[i][j2]], m)

def quad_grid(mb, f, nu, nv, m, uvs=None, orient=None):
    """f(i, j) -> Vector on an (nu+1) x (nv+1) lattice; faces with uv (i/nu, j/nv) unless uvs(i, j) given; orient(centre) -> wanted normal."""
    P = [[f(i, j) for j in range(nv + 1)] for i in range(nu + 1)]; mb.pid += 1
    for i in range(nu):
        for j in range(nv):
            idx = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            if orient is not None:
                q = [P[a][b] for a, b in idx]; nrm = (q[2] - q[0]).cross(q[3] - q[1]); c = (q[0] + q[1] + q[2] + q[3]) / 4
                if nrm.dot(orient(c)) < 0: idx = idx[::-1]
            mb.face([P[a][b] for a, b in idx], m, [uvs(a, b) if uvs else (a / nu, b / nv) for a, b in idx])
    return P

def key_attr(ob, path, frame, interp='LINEAR', idx=-1):
    ob.keyframe_insert(path, index=idx, frame=frame)
    for fc in T._fcurves(ob):
        if fc.data_path == path and (idx < 0 or fc.array_index == idx):
            for kp in fc.keyframe_points:
                if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def show(ob, vis, frame=None):
    ob.hide_render = not vis
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame)

def smooth_round(ob, levels=2):
    md = ob.modifiers.new('ss', 'SUBSURF'); md.levels = levels; md.render_levels = levels
    for pg in ob.data.polygons: pg.use_smooth = True
