#!/usr/bin/env python3
"""ghost_props.py : props of the film-23 set. The hero is the inflatable rubber M4 Sherman: pillow-puffed hull / tracks / wheels, seams, a valve,
a sausage barrel that sags (`sag`), and `inflate` 0..1 (0 = a flat rubber sheet on the grass).  Also: 2.5-ton rubber truck, towed gun, camouflage
nets on poles, crates with stencils, sound truck with a big horn, radio tent, jeep, lanterns, pump + hose, bicycle, stone wall, trees, cows, cards.
Local frames: tank / vehicles face +x, y left, z up, ground z = 0.  All builders take (mb or Bk, M, ...) and write into mesh banks."""
import os, sys, math, random
import bpy
from mathutils import Vector, Matrix
import ghost as GH
import tower as T
import mine as MN
import bakery as BK
from tower import MB, no_bounce, mat_emit
from mine import obox, rod, lumpy, _obj, _glossy, vnoise
V = lambda *a: Vector(a[0] if len(a) == 1 else a)
STATE = T.STATE
def _rnd(s): return random.Random(s)
INK = 0.0

# ----------------------------------------------------------------------------- materials
def setup_materials(P, tx, pre):
    sc = STATE['scene']; cfgs = GH.GX.SCENES[sc]; x0, x1, y0, y1 = cfgs['rect']; night = P.get('night', False); G = mat_g_factory(P, tx, pre)
    C, TX = G['C'], G['TX']; mg = GH.mat_g
    M = {}
    M['ground'] = mg(pre + 'ground', art=GH.art_detail(tx['fields_' + sc], tx['grass_detail'], (x1 - x0) / 7.0, 0.55), gain=1.5 * P['ground_k'], shade_mul=0.95, form=False, glow=tx.get('fields_' + sc + '_glint'), glow_k=0.9)
    M['sky'] = mat_emit(pre + 'sky', image=tx[P.get('sky', 'sky_' + sc)], strength=P['sky_k'])
    fm = P.get('fol_mix')                                                     # foliage: own shade mix (cool shade side) + smooth normals (rounded volume)
    M['hedge'] = TX('hedge', 0.95, smix=fm, sn=True); M['leaf'] = TX('leaf', 1.0, smix=fm, sn=True); M['poplar'] = TX('poplar', 1.05, smix=fm, sn=True); M['apple'] = TX('apple', 1.0, smix=fm, sn=True)
    M['trunk'] = C('#6a4a2c', 1.0); M['trunk_l'] = C('#8a6a44', 1.0)
    M['roof'] = TX('roof_red', 1.1); M['roof_d'] = TX('roof_red_d', 1.1); M['slate'] = TX('roof_slate', 1.15)
    M['stone'] = TX('stone_farm', 1.05); M['stone_w'] = TX('stone_wall', 1.05); M['stone_c'] = TX('stone_church', 1.1); M['barn'] = TX('barn_wood', 1.05); M['wood'] = TX('wood', 1.05)
    M['plaster'] = C('#e8d4a8', 1.05); M['white'] = C('#f4efe4', 1.1); M['shutter'] = C('#3a86c8', 1.1); M['shutter_g'] = C('#3e9a5a', 1.1); M['door'] = C('#8a3c22', 1.0)
    M['glass'] = C('#2c4a78', 1.0, form=False)
    M['dark'] = C('#26222c', 1.0); M['metal'] = GH.mat_g(pre + 'metal', art='#5e6470', gain=1.0, spec=((0.9, 0.9, 1.0), 0.3, 0.4) if not night else None); M['brass'] = mg(pre + 'brass', art='#d0a040', gain=1.1, spec=((1.0, 0.85, 0.5), 0.6, 0.3))
    M['red'] = C('#d03020', 1.1); M['white_p'] = C('#f6f2e8', 1.1); M['yellow'] = C('#f0c030', 1.1); M['blue'] = C('#2a5ab0', 1.1)
    M['hay'] = C('#ecc040', 1.1); M['hay_d'] = C('#c89a2c', 1.0); M['soil'] = C('#8a5a34', 1.0)
    M['canvas'] = TX('canvas_khaki', 1.05); M['canvas_o'] = TX('canvas_olive', 1.0); M['camonet'] = mg(pre + 'camonet', art=tx['camonet'], gain=1.0 if not night else 0.3, alpha=True, form=False)
    M['olive'] = mg(pre + 'olive', art='#6a7a34', gain=1.1, spec=((0.9, 0.95, 0.8), 0.12 if not night else 0.0, 0.5) if not night else None); M['olive_d'] = C('#4a5a26', 1.0); M['khaki'] = C('#c0aa62', 1.05)
    M['tire'] = C('#2a2a30', 1.0, spec=None); M['crate'] = TX('wood', 1.05)
    M['crate_30'] = TX('crate_30', 1.1); M['crate_79'] = TX('crate_79', 1.1); M['crate_a'] = TX('crate_a', 1.1); M['crate_b'] = TX('crate_b', 1.1); M['crate_c'] = TX('crate_c', 1.1); M['crate_p'] = TX('crate_plain', 1.1); M['sign'] = TX('sign', 1.1)
    M['cow'] = TX('cow', 1.05); M['cow_b'] = TX('cow_b', 1.05); M['pink'] = C('#f0a0a0', 1.0)
    # rubber (smooth normal for the toon terminator, GGX sheen, warm rim on sun-facing edges)
    rim = ((1.0, 0.8, 0.45), 0.9, 2.4) if not night else ((0.45, 0.62, 1.0), 1.25, 3.2)
    spec = ((1.0, 0.98, 0.9), 0.22 if not night else 0.10, 0.42)
    smr = 0.55 if not night else 0.7; STATE['smr'] = smr
    M['rubber'] = mg(pre + 'rubber', art=tx['rubber'], gain=1.5 if not night else 0.62, smooth_n=True, spec=spec, rim=rim, shade_mul=smr)
    M['rubber_d'] = mg(pre + 'rubber_d', art=tx['rubber_d'], gain=1.4, shade_mul=smr, smooth_n=True, spec=((1.0, 0.95, 0.85), 0.35, 0.34), rim=rim)
    M['rubber_l'] = mg(pre + 'rubber_l', art=tx['rubber_l'], gain=1.5, shade_mul=smr, smooth_n=True, spec=spec, rim=rim)
    STATE['star_args'] = (tx, spec, rim)
    M['seam_ink'] = C('#1c2412', 1.0)
    M['rubber_white'] = mg(pre + 'rubber_white', art='#f2efe0', gain=1.1, smooth_n=True, spec=spec)
    M['rubber_black'] = mg(pre + 'rubber_black', art='#242622', gain=1.0, smooth_n=True, spec=((1, 1, 1), 0.3, 0.4))
    # light things
    M['lantern'] = mat_emit(pre + 'lantern', '#ffb040', strength=3.6); M['lantern_g'] = mat_emit(pre + 'lantern_g', '#ffd890', strength=5.0)
    M['halo'] = BK._mat_add(pre + 'halo', tx['glow'], (1.0, 0.62, 0.26), 0.75); M['halo_w'] = BK._mat_add(pre + 'halo_w', tx['glow'], (1.0, 0.72, 0.4), 0.8)
    M['halo_s'] = BK._mat_add(pre + 'halo_s', tx['glow'], (1.0, 0.8, 0.5), 1.0); M['pool'] = BK._mat_add(pre + 'pool', tx['pool'], (1.0, 0.42, 0.10), 0.7)
    M['sun_halo'] = BK._mat_add(pre + 'sun_halo', tx['glow'], (1.0, 0.8, 0.45), 0.5)
    M['mist'] = BK._mat_add(pre + 'mist', tx['mist'], (0.8, 0.88, 1.0), 0.55); M['puff'] = mg(pre + 'puff', art=tx['puff'], gain=1.1, alpha=True, form=False, shade_mix=0.0, shade_mul=tuple(c / s_ for c, s_ in zip((0.78, 0.8, 0.88), P['shade'])))   # white-grey smoke, cool grey side
    M['blob'] = _mat_blob(pre + 'blob', tx['glow'])
    M['water'] = mg(pre + 'water', art=tx['water'], gain=1.0, form=False, glow=tx['water'], glow_k=0.14)
    M['glow_win'] = mat_emit(pre + 'glow_win', '#ffcf80', strength=2.6); M['screen'] = mat_emit(pre + 'screen', '#8affc0', strength=2.0)
    STATE['M'] = M; return M

def mat_g_factory(P, tx, pre):
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None, spec=None): return GH.mat_g('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, spec), art=hexcol, gain=gain, shade_mul=sm, form=form, shade_mix=smix, spec=spec)
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, sn=False): return GH.mat_g('%st_%s_%g_%s_%d_%d_%s_%d' % (pre, name, gain, _k(sm), form, alpha, smix, sn), art=tx[name], gain=gain, shade_mul=sm, form=form, alpha=alpha, shade_mix=smix, smooth_n=sn)
    return dict(C=C, TX=TX)

def _mat_blob(name, glow):
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(glow); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.01, 0.015, 0.07, 1)
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = 0.8; L(tx.outputs['Alpha'], mu.inputs[0])
    L(mu.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

# ----------------------------------------------------------------------------- primitives
def _sgp(x, e): return math.copysign(abs(x) ** e, x)
def _fv(mb, pts, mat, uvs): mb.face(pts, mat, uvs)

def pillow(mb, c, puff, mat, n=7, deflate=0.0, cave=0.0, seed=0, faces=('top', 'front', 'back', 'left', 'right'), mats=None, uvk=0.25, a=0.5, noise=0.0, f2=None):
    """Pillow-puffed hexahedron. c = 8 corners [bottom 0..3, top 4..7], 0=(-x,-y) 1=(+x,-y) 2=(+x,+y) 3=(-x,+y). Every face is a bulging grid; each face is its own patch (own vertices), so
    smooth shading rounds the pillow and the edges stay creased (the inflation seams). deflate wrinkles the surface and sinks the top (cave)."""
    c = [V(v) for v in c]; FC = dict(top=(4, 5, 6, 7), front=(1, 2, 6, 5), back=(3, 0, 4, 7), left=(2, 3, 7, 6), right=(0, 1, 5, 4), bottom=(0, 3, 2, 1)); mats = mats or {}
    for fn in faces:
        A, B, Cc, D = [c[i] for i in FC[fn]]; mt = mats.get(fn, mat); mb.pid += 1; g = []
        lu = ((B - A).length + (Cc - D).length) / 2; lv = ((D - A).length + (Cc - B).length) / 2
        for j in range(n + 1):
            row = []
            for i in range(n + 1):
                s, t = i / n, j / n; P0 = A * ((1 - s) * (1 - t)) + B * (s * (1 - t)) + Cc * (s * t) + D * ((1 - s) * t)
                ds = (B - A) * (1 - t) + (Cc - D) * t; dt = (D - A) * (1 - s) + (Cc - B) * s; nrm = ds.cross(dt)
                nrm = nrm.normalized() if nrm.length > 1e-9 else V((0, 0, 1))
                bu = (max(0.0, 1 - (2 * s - 1) ** 2) * max(0.0, 1 - (2 * t - 1) ** 2)) ** a
                off = puff * bu * (1 - 1.7 * deflate) if deflate < 0.6 else puff * bu * (-0.35)
                off += noise * deflate * (vnoise(P0.x * 0.9 + seed, P0.y * 0.9 + P0.z * 0.7, seed + 3) - 0.5) * 2 * (0.3 + bu)
                P = P0 + nrm * off
                if fn == 'top' and cave: P = P - V((0, 0, cave * bu))
                row.append(P)
            g.append(row)
        for j in range(n):
            for i in range(n):
                mb.face([g[j][i], g[j][i + 1], g[j + 1][i + 1], g[j + 1][i]], mt, [(i / n * lu * uvk, j / n * lv * uvk), ((i + 1) / n * lu * uvk, j / n * lv * uvk), ((i + 1) / n * lu * uvk, (j + 1) / n * lv * uvk), (i / n * lu * uvk, (j + 1) / n * lv * uvk)])

def box8(x0, x1, y0, y1, z0, z1, top=None, bot=None):
    """Corners of a box; top / bot = (xf0, xf1, yf0, yf1) override x / y extents at the top or bottom ring (to slope faces)."""
    t = top or (x0, x1, y0, y1); b = bot or (x0, x1, y0, y1)
    return [(b[0], b[2], z0), (b[1], b[2], z0), (b[1], b[3], z0), (b[0], b[3], z0), (t[0], t[2], z1), (t[1], t[2], z1), (t[1], t[3], z1), (t[0], t[3], z1)]

def puffball(mb, c, r, mat, e=(0.8, 0.9), seg=16, rings=8, lat=(-math.pi / 2, math.pi / 2), uvs=(1, 1), deflate=0.0, seed=0, noise=0.0, mats=None):
    """Superquadric (rounded blob) with semi-axes r=(rx, ry, rz); lat range limits it (dome: lat=(0, pi/2))."""
    c = V(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        th = lat[0] + (lat[1] - lat[0]) * k / rings; row = []
        for i in range(seg):
            ph = 2 * math.pi * i / seg; ct = _sgp(math.cos(th), e[0]); st = _sgp(math.sin(th), e[0])
            p = V((r[0] * ct * _sgp(math.cos(ph), e[1]), r[1] * ct * _sgp(math.sin(ph), e[1]), r[2] * st))
            if noise and deflate: p = p * (1 + noise * deflate * (vnoise(p.x * 1.3 + seed, p.y * 1.3 + p.z, seed + 1) - 0.5) * 2)
            row.append(c + p)
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            j = (i + 1) % seg
            mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]], mat, [(uvs[0] * i / seg, uvs[1] * k / rings), (uvs[0] * (i + 1) / seg, uvs[1] * k / rings), (uvs[0] * (i + 1) / seg, uvs[1] * (k + 1) / rings), (uvs[0] * i / seg, uvs[1] * (k + 1) / rings)])
    return R

def tube(mb, pts, radii, mat, seg=8, cap0=True, cap1=True, uvk=0.5):
    """Smooth tube along pts with per-station radii; rings built from a parallel-transport frame."""
    pts = [V(p) for p in pts]; n = len(pts); mb.pid += 1; rings = []; prev = None
    for i in range(n):
        t = (pts[min(i + 1, n - 1)] - pts[max(i - 1, 0)]).normalized()
        u = prev if prev is not None else t.cross(V((0, 0, 1)))
        if u.length < 1e-4: u = V((0, 1, 0))
        u = (u - t * u.dot(t)).normalized(); v = t.cross(u); prev = u
        rings.append([pts[i] + (u * math.cos(2 * math.pi * k / seg) + v * math.sin(2 * math.pi * k / seg)) * radii[i] for k in range(seg)])
    acc = 0.0; ds = [0.0]
    for i in range(1, n): acc += (pts[i] - pts[i - 1]).length; ds.append(acc)
    for i in range(n - 1):
        for k in range(seg):
            j = (k + 1) % seg; mb.face([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]], mat, [(k / seg, ds[i] * uvk), ((k + 1) / seg, ds[i] * uvk), ((k + 1) / seg, ds[i + 1] * uvk), (k / seg, ds[i + 1] * uvk)])
    if cap0: mb.face(rings[0][::-1], mat)
    if cap1: mb.face(rings[-1], mat)

def sausage(mb, p0, p1, r, mat, k=1.0, n=1, seg=8, sag=0.0, bulge=0.22):
    """Inflated tube p0 -> p1 made of n swollen sections pinched at the joints; sag bends it down (a limp half-inflated tube)."""
    p0, p1 = V(p0), V(p1); pts = []; rad = []; m = 6 * n
    for i in range(m + 1):
        t = i / m; p = p0.lerp(p1, t) - V((0, 0, sag * (t ** 1.6)))
        pts.append(p); sec = (t * n) % 1.0 if i < m else 1.0
        rad.append(r * k * (0.72 + 0.28 * math.sin(math.pi * sec) ** 0.7 + bulge * 0.0))
    tube(mb, pts, rad, mat, seg=seg)

def seam(mb, p0, p1, M, r=0.07):
    rod(mb, p0, p1, r, M['seam_ink'], seg=5)

def inst(ob, name, loc, yaw=0.0, hull=0.0, scale=1.0):
    """Linked duplicate of a mesh object (shared mesh data) with its own ink hull modifier."""
    o2 = bpy.data.objects.new(name, ob.data); STATE['SET'].objects.link(o2); o2.location = loc; o2.rotation_euler = (0, 0, math.radians(yaw)); o2.scale = (scale,) * 3
    if hull > 0:
        mats = ob.data.materials; ink = [i for i, m in enumerate(mats) if m.name.startswith('ink')]
        if not ink: mats.append(T.mat_ink()); ink = [len(mats) - 1]
        mod = o2.modifiers.new('ink_hull', 'SOLIDIFY'); mod.thickness = hull; mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False; mod.material_offset = ink[0]; mod.use_even_offset = True
    no_bounce(o2); STATE.setdefault('objects', {})[name] = o2; return o2

def make_obj(mb, name, loc=(0, 0, 0), yaw=0.0, hull=0.0, smooth_=True, shadow=True):
    ob = _obj(mb, name, STATE['SET'], hull=hull, shadow=shadow); ob.location = loc; ob.rotation_euler = (0, 0, math.radians(yaw))
    if smooth_:
        for p in ob.data.polygons: p.use_smooth = True
    return ob

# ----------------------------------------------------------------------------- the rubber M4 Sherman
def tank_mesh(M, inflate=1.0, sag=0.0, seed=1, lod=1.0, valve=True, wheels=True, valve_x=0.9, valve_side=1, elev=0.0, mb=None, star_f=None):
    """Local frame: +x = barrel, y left, z up, tracks on the ground. Returns an MB (materials from M). inflate 0 = flat sheet; sag 0..1 = limp barrel."""
    f = max(0.0, min(1.0, inflate)); de = 1.0 - f; mb = mb if mb is not None else MB(); n = max(4, int(7 * lod)); n2 = max(5, int(9 * lod))
    # set r1: FIXED TOPOLOGY - every part is always built (parts that only exist when inflated shrink to specks), so meshes built at different
    # inflate / sag / elev have the same vertex order and become shape keys (make_tank).  elev = barrel elevation (deg, 'barrels up').
    kw_ = GH.smooth(0.15, 0.5, f) * 0.97 + 0.03; ks_ = GH.smooth(0.35, 0.6, f) * 0.95 + 0.05
    zf = 0.12 + 0.88 * f ** 0.75; wf = 1.0 + 0.10 * de; pf = f; cave = 0.55 * de
    def Z(z): return z * zf
    def W(y): return y * wf
    def X(x): return x * wf
    rb, rd, rl = M['rubber'], M['rubber_d'], M['rubber_l']
    tx_, spec_, rim_ = STATE['star_args']; sf = f if star_f is None else star_f; fk = '%.2f' % sf; pre_ = STATE['pre']
    star_h = GH.mat_g('%sstar_h_%s' % (pre_, fk), art=GH.art_star(tx_['rubber'], tx_['star'], (X(1.7), Z(2.3)) if star_f is None else (1.7, 2.3), 0.95 * (0.5 + 0.5 * sf)), gain=1.5, shade_mul=STATE['smr'], smooth_n=True, spec=spec_, rim=rim_)
    star_t = GH.mat_g('%sstar_t_%s' % (pre_, fk), art=GH.art_star(tx_['rubber'], tx_['star'], (X(-0.4), Z(2.78) + 0.55 * (1.3 * zf + 0.05)) if star_f is None else (-0.4, 2.78 + 0.55 * 1.35), 1.35 * (0.55 + 0.45 * sf)), gain=1.5, shade_mul=STATE['smr'], smooth_n=True, spec=spec_, rim=rim_)
    pu = 0.30 * pf + 0.02; wr = 0.5
    # tracks (two), then road wheels on their outer sides
    for sy in (-1, 1):
        y0, y1 = (1.5, 2.25) if sy > 0 else (-2.25, -1.5)
        c = box8(0, 0, 0, 0, 0, 0)
        pillow(mb, [(X(-4.6), W(y0), 0), (X(4.5), W(y0), 0), (X(4.5), W(y1), 0), (X(-4.6), W(y1), 0), (X(-4.1), W(y0), Z(1.95)), (X(4.0), W(y0), Z(1.95)), (X(4.0), W(y1), Z(1.95)), (X(-4.1), W(y1), Z(1.95))],
               pu, rd, n=n2, deflate=de, cave=0.3 * cave, seed=seed + (3 if sy > 0 else 5), uvk=0.35, noise=wr * pu, faces=('top', 'front', 'back', 'left', 'right'))
        if wheels:
            yw = W(y1 if sy > 0 else y0) + sy * 0.05
            for k in range(6):
                x = X(-3.35 + 1.34 * k); rr = 0.62 * (0.55 + 0.45 * f) * kw_
                puffball(mb, (x, yw, Z(1.02)), (rr, (0.2 * f + 0.06) * kw_, rr * zf ** 0.5), rl, e=(0.75, 0.9), seg=max(8, int(14 * lod)), rings=max(4, int(6 * lod)))
            for xs_ in (-4.0, 3.8): puffball(mb, (X(xs_), yw, Z(1.2)), ((0.62 * f + 0.1) * kw_, (0.2 * f + 0.06) * kw_, (0.62 * f * zf ** 0.5 + 0.1) * kw_), rl, e=(0.75, 0.9), seg=max(8, int(12 * lod)), rings=5)
    # hull body (sloped glacis in front, rear slightly raised)
    pillow(mb, box8(0, 0, 0, 0, 0, 0, ) if False else [(X(-4.4), W(-1.55), Z(0.7)), (X(4.3), W(-1.55), Z(0.7)), (X(4.3), W(1.55), Z(0.7)), (X(-4.4), W(1.55), Z(0.7)),
                      (X(-4.2), W(-1.55), Z(2.8)), (X(3.0), W(-1.55), Z(2.8)), (X(3.0), W(1.55), Z(2.8)), (X(-4.2), W(1.55), Z(2.8))],
           0.42 * pf + 0.03, rb, n=n2, deflate=de, cave=cave, seed=seed + 7, uvk=0.3, noise=0.6 * pu, mats=dict(left=star_h, right=star_h))
    # engine deck bulge (rear)
    pillow(mb, [(X(-4.0), W(-1.2), Z(2.8)), (X(-1.6), W(-1.2), Z(2.8)), (X(-1.6), W(1.2), Z(2.8)), (X(-4.0), W(1.2), Z(2.8)), (X(-3.9), W(-1.1), Z(3.2)), (X(-1.8), W(-1.1), Z(3.2)), (X(-1.8), W(1.1), Z(3.2)), (X(-3.9), W(1.1), Z(3.2))],
           0.22 * pf + 0.01, rb, n=max(4, n - 2), deflate=de, seed=seed + 8, noise=0.3 * pu, faces=('top', 'front', 'back', 'left', 'right'))
    # turret: dome with a star on each side, sits on the hull top
    tz = Z(2.78)
    puffball(mb, (X(-0.4), 0, tz), (2.05 * wf, 1.75 * wf, 1.3 * zf + 0.05), star_t, e=(0.62, 0.8), seg=max(14, int(22 * lod)), rings=max(5, int(9 * lod)), lat=(-0.12, math.pi / 2), deflate=de, seed=seed + 11, noise=0.35)
    puffball(mb, (X(1.55), 0, tz + Z(0.28)), (0.72 * (0.5 + 0.5 * f), 0.95 * wf, 0.78 * zf + 0.05), rb, e=(0.8, 0.8), seg=max(12, int(16 * lod)), rings=6)
    # hatches, cupola, MG
    for (hx, hy, hz, hr) in ((-0.3, -0.85, 1.28, 0.46), (-1.15, 0.75, 1.3, 0.5)):
        puffball(mb, (X(hx), W(hy), tz + Z(hz)), (hr * (0.4 + 0.6 * f), hr * (0.4 + 0.6 * f), 0.26 * zf + 0.04), rl, e=(0.7, 0.85), seg=max(10, int(14 * lod)), rings=4, lat=(0, math.pi / 2))
    if True:
        sausage(mb, (X(-1.15), W(0.75), tz + Z(1.5)), (X(-0.35), W(0.75), tz + Z(1.5) + 0.22 * kw_), 0.1 * kw_, M['rubber_black'], seg=6)
        puffball(mb, (X(3.55), W(-0.75), Z(2.1)), (0.34 * kw_, 0.34 * kw_, (0.3 * zf + 0.05) * kw_), rl, e=(0.8, 0.8), seg=10, rings=4)
    # barrel: sausage sections, droops with sag (and with deflation); muzzle brake ring
    sg = max(sag, min(1.0, de * 1.4)); L_ = 4.9; r = 0.30 * (0.55 + 0.45 * f); p0 = V((X(2.2), 0, tz + Z(0.32))); drop = min(sg * 3.3, max(0.3, p0.z - 1.0))
    ea = math.radians(elev) * (1.0 - min(1.0, sg)); bd_ = V((math.cos(ea), 0, math.sin(ea)))
    sausage(mb, p0, p0 + bd_ * L_, r, rb, n=6, seg=max(6, int(9 * lod)), sag=drop)
    vs = 1 if valve_side >= 0 else -1
    mz = p0 + bd_ * L_ - V((0, 0, drop)); mb.info = dict(tip=tuple(mz), valve=(X(valve_x), vs * (W(1.62) + 0.6), Z(1.55)), top=tz + Z(1.3)); puffball(mb, mz, (0.34 * (0.5 + 0.5 * f) + 0.06, r * 1.35, r * 1.35), rl, e=(0.8, 0.8), seg=10, rings=5)
    # inflation valve (small brass nozzle + white cap) at the rear left, with seam rods along the hull edges
    if valve:
        vb = V((X(valve_x), vs * W(1.62), Z(1.55))); rod(mb, vb, vb + V((0, vs * 0.42, 0)), 0.17, M['brass'], seg=8); rod(mb, vb + V((0, vs * 0.42, 0)), vb + V((0, vs * 0.58, 0)), 0.24, M['white_p'], seg=8)
        puffball(mb, vb + V((0, vs * 0.12, 0)), (0.3, 0.3, 0.3), rl, e=(1, 1), seg=8, rings=4)
    if True:
        sr_ = 0.07 * ks_
        for sy in (-1, 1):
            seam(mb, V((X(-4.4), W(1.55 * sy), Z(2.8))), V((X(3.0), W(1.55 * sy), Z(2.8))), M, sr_); seam(mb, V((X(-4.4), W(1.55 * sy), Z(0.72))), V((X(4.3), W(1.55 * sy), Z(0.72))), M, sr_)
            seam(mb, V((X(3.0), W(1.55 * sy), Z(2.8))), V((X(4.3), W(1.55 * sy), Z(0.72))), M, sr_)
        seam(mb, V((X(3.0), W(-1.55), Z(2.8))), V((X(3.0), W(1.55), Z(2.8))), M, sr_)
    if not hasattr(mb, 'info'): mb.info = {}
    return mb

def tank_obj(name, loc, yaw, M, inflate=1.0, sag=0.0, seed=1, lod=1.0, hull=0.0, shared=None, **kw):
    """Create a tank object. Pass shared=<an earlier tank object> to reuse its mesh (instances). kw: valve_x, valve_side."""
    if shared is not None: return inst(shared, name, loc, yaw, hull)
    mb = tank_mesh(M, inflate, sag, seed, lod, **kw); ob = make_obj(mb, name, loc, yaw, hull=hull); ob['info'] = str(mb.info); STATE['tank_info'] = mb.info; return ob

# ----------------------------------------------------------------------------- vehicles
def truck_mesh(M, inflate=1.0, rubber=True, horn=False, seed=3, lod=1.0):
    """Inflatable 2.5-ton truck (or, rubber=False, a real hard-edged sound truck with a loudspeaker horn). Faces +x."""
    f = max(0.0, min(1.0, inflate)); de = 1.0 - f; mb = MB(); n = max(4, int(6 * lod)); zf = 0.14 + 0.86 * f ** 0.75
    def Z(z): return z * zf
    pu = (0.26 * f + 0.02) if rubber else 0.0; body = M['olive'] if not rubber else M['rubber']; bd = M['rubber_d'] if rubber else M['olive_d']; wm = M['rubber_l'] if rubber else M['metal']
    cv = M['canvas'] if not rubber else M['rubber_l']
    def pl(c, p, mat, **kw):
        if rubber: pillow(mb, c, p, mat, n=n, deflate=de, seed=seed, noise=0.4 * p, **kw)
        else: pillow(mb, c, 0.0, mat, n=2, **kw)
    pl(box8(-5.2, 5.4, -1.75, 1.75, Z(1.0), Z(2.1)), pu, bd, uvk=0.3)
    pl(box8(2.9, 5.4, -1.45, 1.45, Z(2.1), Z(3.5), top=(3.2, 5.1, -1.4, 1.4)), pu, body, uvk=0.3)                                                    # hood
    pl([(0.7, -1.7, Z(2.1)), (3.3, -1.7, Z(2.1)), (3.3, 1.7, Z(2.1)), (0.7, 1.7, Z(2.1)), (0.8, -1.6, Z(4.7)), (2.8, -1.6, Z(4.7)), (2.8, 1.6, Z(4.7)), (0.8, 1.6, Z(4.7))], pu * 1.1, body, uvk=0.3, mats=dict(left=body, right=body))
    pl(box8(-5.2, 0.5, -1.85, 1.85, Z(2.1), Z(3.4)), pu, body, uvk=0.3)                                                                               # bed
    if f > 0.3:
        puffball(mb, (-2.35, 0, Z(3.4)), (3.0, 1.8, 1.75 * zf + 0.05), cv, e=(0.8, 0.85), seg=18, rings=6, lat=(0, math.pi / 2), uvs=(2, 1))               # tarp
        for xx in (-4.6, -3.0, -1.4, 0.2): puffball(mb, (xx, 0, Z(3.4)), (0.1, 1.84, 1.78 * zf + 0.06), bd if rubber else M['olive_d'], e=(0.8, 0.85), seg=6, rings=6, lat=(0, math.pi / 2))
    for xw in (3.9, -0.9, -3.7):
        for sy in (-1, 1):
            if f > 0.2: puffball(mb, (xw, sy * 1.9, Z(1.0)), (1.05 * (0.5 + 0.5 * f), 0.5 * f + 0.1, 1.05 * (0.5 + 0.5 * f) * zf ** 0.5), M['rubber_black'] if rubber else M['tire'], e=(0.75, 0.9), seg=14, rings=6)
    if f > 0.4:                                                                                                                                         # windscreen, side windows, lamps
        mb.oface([V(2.83, -1.45, Z(3.2)), V(2.83, 1.45, Z(3.2)), V(2.83, 1.45, Z(4.35)), V(2.83, -1.45, Z(4.35))], M['glass'], [(0, 0)] * 4, (1, 0, 0)) if False else None
        for sy in (-1, 1):
            mb.oface([V(1.1, sy * 1.7 + sy * 0.12, Z(3.2)), V(2.5, sy * 1.7 + sy * 0.12, Z(3.2)), V(2.5, sy * 1.7 + sy * 0.12, Z(4.3)), V(1.1, sy * 1.7 + sy * 0.12, Z(4.3))], M['glass'], [(0, 0)] * 4, (0, sy, 0))
            puffball(mb, (5.3, sy * 1.0, Z(2.9)), (0.2, 0.28, 0.28), M['white_p'], e=(1, 1), seg=8, rings=4)
        mb.oface([V(2.99, -1.3, Z(3.3)), V(2.99, 1.3, Z(3.3)), V(2.99, 1.3, Z(4.4)), V(2.99, -1.3, Z(4.4))], M['glass'], [(0, 0)] * 4, (1, 0, 0)) if False else None
    if horn:                                                                                                                                              # deep flared metal bell on a boom, facing back-right
        base = V(-3.2, 0, Z(5.0)); rod(mb, V(-3.2, 0, Z(3.4)), base, 0.25, M['metal'], seg=8); rod(mb, base, base + V(-0.7, 0, 0.5), 0.22, M['metal'], seg=8)
        hc = base + V(-1.0, 0, 0.7); ax = V(-0.85, 0, 0.30).normalized(); L_ = 4.2; prev = None
        for i in range(10):
            t = i / 10.0; t2 = (i + 1) / 10.0; r0 = 0.45 + 2.3 * t ** 2.2; r1 = 0.45 + 2.3 * t2 ** 2.2
            mb.frustum(hc + ax * (L_ * t), hc + ax * (L_ * t2), r0, r1, M['metal'], seg=28, cap0=False, cap1=False)
        mb.frustum(hc + ax * L_, hc + ax * (L_ + 0.18), 2.75, 2.75, M['brass'], seg=28, cap0=False, cap1=False)
        mb.frustum(hc + ax * (L_ - 0.1), hc + ax * 0.5, 2.5, 0.55, M['dark'], seg=28, cap0=False, cap1=False)
        rod(mb, hc - ax * 0.2, hc + ax * 0.5, 0.7, M['metal'], seg=12)
    return mb

def gun_mesh(M, inflate=1.0, seed=2):
    """Towed gun (inflatable howitzer): shield, barrel, two wheels, two trails. Faces +x (barrel), trails go -x."""
    f = inflate; mb = MB(); pu = 0.2 * f + 0.02
    for sy in (-1, 1):
        puffball(mb, (0, sy * 2.0, 1.1), (1.1, 0.35, 1.1), M['rubber_black'], e=(0.75, 0.9), seg=14, rings=6)
        sausage(mb, V(-0.4, sy * 0.5, 1.0), V(-5.2, sy * 2.4, 0.3), 0.26, M['rubber_d'], n=4, seg=7)
    pillow(mb, [(0.3, -1.5, 1.1), (0.55, -1.5, 1.1), (0.55, 1.5, 1.1), (0.3, 1.5, 1.1), (0.3, -1.4, 3.1), (0.55, -1.4, 3.1), (0.55, 1.4, 3.1), (0.3, 1.4, 3.1)], pu, M['rubber'], n=6, faces=('top', 'front', 'back', 'left', 'right'))
    sausage(mb, V(0.2, 0, 1.9), V(5.2, 0, 2.3), 0.3, M['rubber'], n=5, seg=8, sag=0.3 * (1 - f)); puffball(mb, V(0.4, 0, 1.9), (0.7, 0.55, 0.6), M['rubber_l'], e=(0.8, 0.8), seg=10, rings=5)
    puffball(mb, V(5.25, 0, 2.3 - 0.3 * (1 - f)), (0.35, 0.42, 0.42), M['rubber_l'], e=(0.8, 0.8), seg=10, rings=5)
    return mb

# ----------------------------------------------------------------------------- camouflage net on poles
def camo_net(Bk, M, centre, yaw, L=13.0, Wd=7.5, h0=5.2, h1=4.6, seed=1, ground=lambda x, y: 0.0, skirt=True):
    """A net canopy on four poles: a gently sagging, tilted sheet of camo netting (alpha cut, casts a patterned shadow) with a draped skirt on one side."""
    F = BK.Frame(centre, yaw); nb = Bk('nets', hull=0.0, shadow=True); pb = Bk('poles', hull=0.0); rr = _rnd(seed); nx_, ny_ = 8, 5
    def ptz(u, v): return F.p((u - 0.5) * L, (v - 0.5) * Wd, 0)
    def hz(u, v):
        base = h0 + (h1 - h0) * v; return base - 0.55 * math.sin(math.pi * u) * math.sin(math.pi * v) + 0.15 * (vnoise(u * 4 + seed, v * 4, seed) - 0.5)
    G = [[None] * (ny_ + 1) for _ in range(nx_ + 1)]
    for i in range(nx_ + 1):
        for j in range(ny_ + 1):
            u, v = i / nx_, j / ny_; q = ptz(u, v); G[i][j] = V((q.x, q.y, ground(q.x, q.y) + hz(u, v)))
    nb.pid += 1
    for i in range(nx_):
        for j in range(ny_):
            q = [G[i][j], G[i + 1][j], G[i + 1][j + 1], G[i][j + 1]]; nb.face(q, M['camonet'], [(i / 1.2, j / 1.2), ((i + 1) / 1.2, j / 1.2), ((i + 1) / 1.2, (j + 1) / 1.2), (i / 1.2, (j + 1) / 1.2)])
            nb.face(q[::-1], M['camonet'], [(i / 1.2, j / 1.2), ((i + 1) / 1.2, j / 1.2), ((i + 1) / 1.2, (j + 1) / 1.2), (i / 1.2, (j + 1) / 1.2)][::-1])
    if skirt:
        for i in range(nx_):
            a, b = G[i][0], G[i + 1][0]; a2 = V((a.x, a.y, ground(a.x, a.y) + 1.6 + 0.3 * math.sin(i * 1.7))); b2 = V((b.x, b.y, ground(b.x, b.y) + 1.6 + 0.3 * math.sin((i + 1) * 1.7)))
            nb.pid += 1; nb.face([a, b, b2, a2], M['camonet'], [(i, 0), (i + 1, 0), (i + 1, 1), (i, 1)]); nb.face([a, b, b2, a2][::-1], M['camonet'], [(i, 0), (i + 1, 0), (i + 1, 1), (i, 1)][::-1])
    for (u, v) in ((0.04, 0.04), (0.96, 0.04), (0.04, 0.96), (0.96, 0.96), (0.5, 0.04), (0.5, 0.96)):
        q = ptz(u, v); z0 = ground(q.x, q.y); rod(pb, V((q.x, q.y, z0)), V((q.x, q.y, z0 + hz(u, v))), 0.16, M['trunk'], seg=5)

# ----------------------------------------------------------------------------- crates, sign, pump, lamps, wall, bicycle
def crate(Bk, M, pos, yaw, size=(3.0, 1.9, 1.9), front='crate_a', open_=False, name='crates', rubber_in=False, seed=1):
    """Wooden crate with a stencil on the +y... front (local -y side faces the camera when yaw=0). size = (x, y, z). Open crates have a lid hinged back and a rolled rubber bundle inside."""
    F = BK.Frame(pos, yaw); sx, sy, sz = size; b = Bk(name, hull=0.0)
    hx, hy = sx / 2, sy / 2; wood = M['wood']; ft = M[front]
    def face(pts, mat, uv, nrm): b.oface([F.p(*q) for q in pts], mat, uv, F.X * nrm[0] + F.Y * nrm[1] + F.Z * nrm[2])
    wall_t = 0.12
    # outer faces
    face([(-hx, -hy, 0), (hx, -hy, 0), (hx, -hy, sz), (-hx, -hy, sz)], ft, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    face([(hx, hy, 0), (-hx, hy, 0), (-hx, hy, sz), (hx, hy, sz)], wood, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 0))
    face([(hx, -hy, 0), (hx, hy, 0), (hx, hy, sz), (hx, -hy, sz)], M['crate_p'], [(0, 0), (1, 0), (1, 1), (0, 1)], (1, 0, 0))
    face([(-hx, hy, 0), (-hx, -hy, 0), (-hx, -hy, sz), (-hx, hy, sz)], M['crate_p'], [(0, 0), (1, 0), (1, 1), (0, 1)], (-1, 0, 0))
    if not open_:
        face([(-hx, -hy, sz), (hx, -hy, sz), (hx, hy, sz), (-hx, hy, sz)], wood, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    else:                                                                                                                       # open: inner floor + inner walls, bundle of rubber inside, lid propped up at the back
        face([(-hx, -hy, sz * 0.78), (hx, -hy, sz * 0.78), (hx, hy, sz * 0.78), (-hx, hy, sz * 0.78)], M['rubber'], [(0, 0), (3, 0), (3, 2), (0, 2)], (0, 0, 1))
        for (a, c_, n_) in (((-hx, -hy), (hx, -hy), (0, 1)), ((hx, hy), (-hx, hy), (0, -1))):
            face([(a[0], a[1], sz * 0.78), (c_[0], c_[1], sz * 0.78), (c_[0], c_[1], sz), (a[0], a[1], sz)], wood, [(0, 0), (1, 0), (1, 1), (0, 1)], (n_[0], n_[1], 0))
        for (px, nx_) in ((hx, -1), (-hx, 1)): face([(px, -hy, sz * 0.78), (px, hy, sz * 0.78), (px, hy, sz), (px, -hy, sz)], wood, [(0, 0), (1, 0), (1, 1), (0, 1)], (nx_, 0, 0))
        for (x0, y0, z0, x1, y1, z1) in ((-hx, hy - 0.1, sz - 0.05, hx, hy, sz), (-hx, -hy, sz - 0.05, hx, -hy + 0.1, sz)): obox(b, F.p((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), F.X, F.Y, F.Z, (x1 - x0) / 2, (y1 - y0) / 2, (z1 - z0) / 2, M['crate'])
        lid = [F.p(-hx, hy, sz), F.p(hx, hy, sz), F.p(hx, hy + 0.35, sz + sy * 0.97), F.p(-hx, hy + 0.35, sz + sy * 0.97)]
        b.oface(lid, wood, [(0, 0), (1, 0), (1, 1), (0, 1)], F.Y * 0.4 + F.Z * 0.2); b.oface(lid[::-1], ft, [(0, 0), (1, 0), (1, 1), (0, 1)][::-1], -F.Y * 0.4 - F.Z * 0.2)
        rb_ = Bk(name + '_rub', hull=0.0, smooth_=True)
        for k in range(3): puffball(rb_, F.p(-hx * 0.5 + k * hx * 0.5, 0.05 * (k - 1), sz * 0.78 + 0.3), (0.85, 0.7, 0.42), M['rubber'], e=(0.8, 0.85), seg=10, rings=5)
    return F

def sign_post(Bk, M, pos, yaw, w=6.0, h=2.4, ph=5.0):
    """Canvas sign '23rd HQ SPECIAL TROOPS' stretched between two posts."""
    F = BK.Frame(pos, yaw); b = Bk('sign', hull=0.0); pb = Bk('poles', hull=0.0); z0 = ph - h - 0.1
    for sx in (-1, 1): rod(pb, F.p(sx * (w / 2 + 0.2), 0, 0), F.p(sx * (w / 2 + 0.2), 0, ph + 0.3), 0.18, M['trunk'], seg=6)
    b.oface([F.p(-w / 2, 0, z0), F.p(w / 2, 0, z0), F.p(w / 2, 0, z0 + h), F.p(-w / 2, 0, z0 + h)], M['sign'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Y * -1)
    b.oface([F.p(w / 2, 0.03, z0), F.p(-w / 2, 0.03, z0), F.p(-w / 2, 0.03, z0 + h), F.p(w / 2, 0.03, z0 + h)], M['canvas'], [(0, 0), (1, 0), (1, 1), (0, 1)], F.Y)
    for k in range(4):
        rod(pb, F.p(-w / 2 + k * w / 3, -0.02, z0 + h), F.p(-w / 2 + k * w / 3 + 0.1, -0.02, z0 + h + 0.3), 0.03, M['trunk_l'], seg=4)
    return F

def blob(Bk, c, rx, ry, M, z=0.05):
    b = Bk('blobs', hull=0.0, shadow=False); c = V(c)
    b.face([V(c.x - rx, c.y - ry, c.z + z), V(c.x + rx, c.y - ry, c.z + z), V(c.x + rx, c.y + ry, c.z + z), V(c.x - rx, c.y + ry, c.z + z)], M['blob'], [(0, 0), (1, 0), (1, 1), (0, 1)])

def lantern(Bk, M, p, s=1.0, light=0.0, halo_r=3.0, rgb=(1.0, 0.62, 0.3), name='ln', pole=0.0):
    """Oil lantern at p (its centre): glowing glass body with a cap, a halo, optional point light. pole>0: also a post down to z = p.z - pole."""
    p = V(p); b = Bk('lanterns', hull=0.0, shadow=False); hb = Bk('halos', hull=0.0, shadow=False); w = Bk('lanternmetal', hull=0.0)
    rod(w, p + V(0, 0, -0.35 * s), p + V(0, 0, 0.35 * s), 0.3 * s, M['lantern_g'], seg=8, r1=0.26 * s)
    rod(w, p + V(0, 0, 0.35 * s), p + V(0, 0, 0.52 * s), 0.34 * s, M['dark'], seg=8, r1=0.1 * s); rod(w, p + V(0, 0, -0.45 * s), p + V(0, 0, -0.35 * s), 0.3 * s, M['dark'], seg=8)
    rod(w, p + V(0, 0, 0.52 * s), p + V(0, 0, 0.75 * s), 0.04 * s, M['dark'], seg=4)
    if pole > 0:
        rod(w, p + V(0, 0, -pole), p + V(0, 0, 1.0), 0.12, M['trunk'], seg=6); rod(w, p + V(0, 0, 0.95), p + V(0.7, 0, 0.95), 0.08, M['trunk'], seg=5)
    BK._halo(hb, p, halo_r * s, M, 'halo')
    if light > 0:
        d = bpy.data.lights.new(name, 'POINT'); d.color = rgb; d.energy = light; d.shadow_soft_size = 0.35 * s
        ob = bpy.data.objects.new(name, d); STATE['LIGHTS'].objects.link(ob); ob.location = p; ob.visible_camera = False; STATE['lamps'].append(ob)
    return p

def pool(Bk, M, c, r, mat='pool'):
    """Warm light pool decal on the ground (camera-only additive)."""
    b = Bk('pools', hull=0.0, shadow=False); c = V(c)
    b.face([V(c.x - r, c.y - r, c.z + 0.06), V(c.x + r, c.y - r, c.z + 0.06), V(c.x + r, c.y + r, c.z + 0.06), V(c.x - r, c.y + r, c.z + 0.06)], M[mat], [(0, 0), (1, 0), (1, 1), (0, 1)])

def pump(Bk, M, pos, yaw, valve_pos, gz=lambda x, y: 0.0, seed=1):
    """Hand-pump / compressor: olive frame, red tank, gauge, handle lever, and a black hose to valve_pos."""
    F = BK.Frame(pos, yaw); b = Bk('pump', hull=0.0); p0 = V(pos)
    obox(b, F.p(0, 0, 0.5), F.X, F.Y, F.Z, 1.3, 0.8, 0.12, M['olive_d'])
    for sx in (-1, 1):
        for sy in (-1, 1): rod(b, F.p(sx * 1.1, sy * 0.65, 0), F.p(sx * 1.1, sy * 0.65, 0.5), 0.09, M['metal'], seg=5)
    rod(b, F.p(-0.7, 0, 0.62), F.p(0.7, 0, 0.62), 0.5, M['red'], seg=14); b.sphere(F.p(0.7, 0, 0.62), 0.5, M['red'], seg=12, rings=6); b.sphere(F.p(-0.7, 0, 0.62), 0.5, M['red'], seg=12, rings=6)
    rod(b, F.p(1.0, 0.2, 0.6), F.p(1.0, 0.2, 1.8), 0.14, M['metal'], seg=6); rod(b, F.p(1.0, -0.3, 1.7), F.p(1.0, 1.0, 1.7), 0.08, M['metal'], seg=5)
    rod(b, F.p(1.0, 0.2, 1.75), F.p(1.0, 0.2, 2.45), 0.07, M['metal'], seg=5); rod(b, F.p(1.0, -0.6, 2.4), F.p(1.0, 1.0, 2.55), 0.1, M['brass'], seg=6)         # lever
    b.sphere(F.p(-0.1, -0.52, 0.95), 0.26, M['white_p'], seg=10, rings=6)                                                                                  # gauge
    hp = F.p(-1.25, 0, 0.5); end = V(valve_pos); pts = []; n = 14
    for i in range(n + 1):
        t = i / n; q = hp.lerp(end, t); zz = gz(q.x, q.y) + 0.14 + 0.5 * math.sin(math.pi * t) * (1 - t) ** 0.5 + (hp.z - gz(hp.x, hp.y)) * (1 - t) * 0.6
        pts.append(V((q.x + 0.35 * math.sin(t * 6.0), q.y + 0.3 * math.sin(t * 4.0 + 1), zz)))
    tube(b, pts, [0.1] * len(pts), M['rubber_black'], seg=6, uvk=0.2)

def bicycle(Bk, M, pos, yaw, lean=14.0, s=1.0, name='bike'):
    """French roadster at real scale (a 3 D soldier: wheel radius 0.58 D, wheelbase 1.75 D): black tyres, grey rims and spokes, blue frame, swept
    handlebar, brown saddle, wicker basket on the front rack with a baguette.  Local +x = forward; it rests on both tyres, leaning `lean` deg about x."""
    F = BK.Frame(pos, yaw); b = Bk(name, hull=0.0); la = math.radians(lean); R = 0.58
    def P(x, y, z):
        z2 = z * math.cos(la) - y * math.sin(la); y2 = y * math.cos(la) + z * math.sin(la); return F.p(x * s, y2 * s, z2 * s)
    fr, mt, dk = M['blue'], M['metal'], M['dark']
    for cx in (-0.87, 0.87):
        ring = [P(cx + R * math.cos(2 * math.pi * k / 32), 0, R + R * math.sin(2 * math.pi * k / 32)) for k in range(33)]
        for a, c_ in zip(ring, ring[1:]): rod(b, a, c_, 0.045 * s, M['tire'], seg=6)
        rim = [P(cx + R * 0.9 * math.cos(2 * math.pi * k / 32), 0, R + R * 0.9 * math.sin(2 * math.pi * k / 32)) for k in range(33)]
        for a, c_ in zip(rim, rim[1:]): rod(b, a, c_, 0.018 * s, mt, seg=4)
        for k in range(0, 32, 2): rod(b, P(cx, 0, R), rim[k], 0.006 * s, mt, seg=3)
        rod(b, P(cx, -0.06, R), P(cx, 0.06, R), 0.045 * s, mt, seg=8)
    bb_ = (0.0, 0, 0.36); st = (-0.22, 0, 1.12); ht = (0.62, 0, 1.12); hb_ = (0.68, 0, 0.92)
    for a, c_ in ((( -0.87, 0, R), bb_), (bb_, st), (st, ht), (bb_, hb_), ((-0.87, 0, R), st), (hb_, ht)): rod(b, P(*a), P(*c_), 0.034 * s, fr, seg=6)
    rod(b, P(*hb_), P(0.87, 0, R), 0.028 * s, mt, seg=5); rod(b, P(*ht), P(0.6, 0, 1.3), 0.028 * s, mt, seg=5)
    hbar = [(0.48, -0.32, 1.33), (0.62, -0.26, 1.33), (0.62, 0.26, 1.33), (0.48, 0.32, 1.33)]
    for a, c_ in zip(hbar, hbar[1:]): rod(b, P(*a), P(*c_), 0.024 * s, mt, seg=5)
    for g in (hbar[0], hbar[-1]): rod(b, P(*g), P(g[0] - 0.1, g[1], g[2]), 0.035 * s, dk, seg=5)
    rod(b, P(-0.22, 0, 1.12), P(-0.25, 0, 1.26), 0.026 * s, mt, seg=5); obox(b, P(-0.27, 0, 1.3), F.X, F.Y, F.Z, 0.15 * s, 0.08 * s, 0.035 * s, M['trunk'])
    rod(b, P(0, -0.12, 0.36), P(0, 0.12, 0.36), 0.1 * s, mt, seg=10)
    for sy in (-1, 1): rod(b, P(0, sy * 0.12, 0.36), P(0.1 * sy, sy * 0.2, 0.36 - 0.16 * sy), 0.016 * s, dk, seg=3)
    # front rack + wicker basket + baguette
    rod(b, P(0.75, 0, 1.0), P(0.98, 0, 1.0), 0.016 * s, mt, seg=3)
    bc = P(0.92, 0, 1.13); obox(b, bc, F.X, F.Y, F.Z, 0.19 * s, 0.22 * s, 0.13 * s, M['hay_d'])
    for k in range(4): rod(b, P(0.73, -0.225, 1.03 + k * 0.065), P(1.11, -0.225, 1.03 + k * 0.065), 0.01 * s, M['trunk'], seg=3)
    rod(b, P(0.82, -0.08, 1.12), P(1.18, 0.12, 1.52), 0.045 * s, M['bread'], seg=7)
    rod(b, P(0.86, 0.06, 1.12), P(1.0, 0.1, 1.36), 0.04 * s, M['bread'], seg=7)
    return F

def stone_wall(Bk, M, p0, p1, h=1.4, w=1.1, seed=1, gz=lambda x, y: 0.0, step=0.9, name='wall'):
    """Low dry-stone field wall p0 -> p1: two courses of irregular stones (random size, small yaw/tilt, staggered joints) and flat cap stones."""
    p0, p1 = V(p0), V(p1); L = (p1 - p0).length; d = (p1 - p0).normalized(); nrm = V((-d.y, d.x, 0)); rr = _rnd(seed); b = Bk(name, hull=0.0)
    ch = h * 0.42
    for course in range(2):
        x = -rr.uniform(0, step * 0.5) if course else 0.0
        while x < L:
            ln = step * rr.uniform(0.55, 1.05); c = p0 + d * min(L - 0.1, x + ln / 2); z0 = gz(c.x, c.y) + course * ch; a = rr.uniform(-0.12, 0.12)
            dd = (d * math.cos(a) + nrm * math.sin(a)).normalized(); nn = V((-dd.y, dd.x, 0)); up = V((0, 0, 1)) + dd * rr.uniform(-0.06, 0.06)
            obox(b, V((c.x, c.y, z0 + ch * 0.5)) + nn * rr.uniform(-0.05, 0.05), dd, nn, up.normalized(), ln * 0.47, w * 0.5 * rr.uniform(0.85, 1.0), ch * 0.5 * rr.uniform(0.85, 1.05), M['stone_w'], uvk=0.4)
            x += ln
    x = 0.0
    while x < L:
        ln = step * rr.uniform(0.4, 0.75); c = p0 + d * min(L - 0.05, x + ln / 2); z0 = gz(c.x, c.y) + 2 * ch
        obox(b, V((c.x, c.y, z0 + h * 0.07)), d, nrm, V((0, 0, 1)), ln * 0.5, w * 0.55, h * 0.07 + rr.uniform(0, 0.03), M['stone_w'], uvk=0.4); x += ln

def card(name, tex, pos, face_to, height=3.0, lean=0.0, flip=False):
    """Camera-facing (yaw) puppet card with feet at pos. Card art is 2.6 x 3.2 D at height 3.0: scale = height/3.0."""
    k = height / 3.0; w, h = 2.6 * k, 3.2 * k
    me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, 0, h), (-w / 2, 0, h)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((1, 0), (0, 0), (0, 1), (1, 1)) if flip else ((0, 0), (1, 0), (1, 1), (0, 1))): uv.data[i].uv = c
    mn = 'GHcard_' + os.path.basename(tex)
    mat = bpy.data.materials.get(mn) or T.mat_card(mn, tex)
    me.materials.append(mat); ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob); ob.location = pos; no_bounce(ob)
    d = V(face_to) - V(pos); yaw = math.atan2(d.x, -d.y); ob.rotation_euler = (math.radians(-lean), 0, yaw); STATE.setdefault('cards', []).append(ob); return ob

# ----------------------------------------------------------------------------- r3: lane strip with real ruts, small props (jerrycan, toolbox)
def lane_strip(Bk, M, lane, gz, s0, s1, width=8.0, ruts=(-1.95, 1.95), rut_w=0.95, depth=0.10, step=0.35, puddle=None):
    """The lane as geometry between arc lengths s0..s1 of the polyline: packed-dirt crown, two tread-marked ruts (sunk `depth`, with raised
    berms), a grassy hump between them, edges that fall back to the terrain.  u runs along the lane (UVs in D).  puddle=(s_a, s_b, rut index)
    fills a stretch of one rut with a sky-reflecting puddle."""
    pts = [V((p[0], p[1], 0)) for p in lane]; acc = [0.0]
    for a, b in zip(pts, pts[1:]): acc.append(acc[-1] + (b - a).length)
    def at(s):
        for i in range(len(pts) - 1):
            if acc[i + 1] >= s:
                t = (s - acc[i]) / max(1e-9, acc[i + 1] - acc[i]); d = (pts[i + 1] - pts[i]).normalized(); return pts[i].lerp(pts[i + 1], t), d
        return pts[-1], (pts[-1] - pts[-2]).normalized()
    hw = width / 2
    prof = [(-hw - 0.9, -0.03, 'g'), (-hw, 0.05, 'd')]                      # (lateral offset, height, material key of the band that STARTS here)
    for rc in ruts:
        a = rc - rut_w / 2; b = rc + rut_w / 2
        prof += [(a - 0.28, 0.09, 'd'), (a, 0.05, 'r'), (a + 0.14, -depth + 0.04, 'r'), (rc, -depth, 'r'), (b - 0.14, -depth + 0.04, 'r'), (b, 0.05, 'd'), (b + 0.28, 0.09, 'd')]
    prof += [(hw, 0.05, 'g'), (hw + 0.9, -0.03, 'g')]
    prof.sort(key=lambda q: q[0])
    mats = dict(d=M['lane_dirt'], r=M['rut'], g=M['ground'])
    b = Bk('lane', hull=0.0, smooth_=True); n = max(2, int((s1 - s0) / step)); rows = []
    for k in range(n + 1):
        s = s0 + (s1 - s0) * k / n; c, d = at(s); lat = V((-d.y, d.x, 0)); row = []
        for (o, h, mk) in prof:
            q = c + lat * o; wob = 0.03 * math.sin(s * 1.7 + o * 3.1) if mk == 'r' else 0.0; row.append(V((q.x, q.y, gz(q.x, q.y) + h + wob)))
        rows.append((s, row))
    x0, x1, y0, y1 = GH.GX.SCENES[STATE['scene']]['rect']
    for (sa, ra), (sb, rb_) in zip(rows, rows[1:]):
        b.pid += 1
        for j in range(len(prof) - 1):
            mk = prof[j][2]; o0, o1 = prof[j][0], prof[j + 1][0]
            if mk == 'g':                                                   # verge: ground UVs so the painted fields line up
                uv = [((p.x - x0) / (x1 - x0), (p.y - y0) / (y1 - y0)) for p in (ra[j], rb_[j], rb_[j + 1], ra[j + 1])]
            elif mk == 'r':
                rc = min(ruts, key=lambda r_: abs(r_ - (o0 + o1) / 2)); v0 = (o0 - rc) / rut_w + 0.5; v1 = (o1 - rc) / rut_w + 0.5
                uv = [(sa / 2.0, v0), (sb / 2.0, v0), (sb / 2.0, v1), (sa / 2.0, v1)]
            else: uv = [(sa / 4.0, o0 / 4.0), (sb / 4.0, o0 / 4.0), (sb / 4.0, o1 / 4.0), (sa / 4.0, o1 / 4.0)]
            b.face([ra[j], rb_[j], rb_[j + 1], ra[j + 1]], mats[mk], uv)
    if puddle:
        sa_, sb_, ri = puddle; rc = ruts[ri]; pb = Bk('puddle', hull=0.0, shadow=False); m_ = 16
        for k in range(m_):
            t0, t1 = k / m_, (k + 1) / m_; wa = math.sin(math.pi * t0) ** 0.6 * rut_w * 0.42; wb = math.sin(math.pi * t1) ** 0.6 * rut_w * 0.42
            ca, da = at(sa_ + (sb_ - sa_) * t0); cb, db = at(sa_ + (sb_ - sa_) * t1); la, lb = V((-da.y, da.x, 0)), V((-db.y, db.x, 0))
            za = gz(ca.x, ca.y) - depth + 0.045; zb = gz(cb.x, cb.y) - depth + 0.045
            P = [ca + la * (rc - wa), cb + lb * (rc - wb), cb + lb * (rc + wb), ca + la * (rc + wa)]
            pb.face([V((P[0].x, P[0].y, za)), V((P[1].x, P[1].y, zb)), V((P[2].x, P[2].y, zb)), V((P[3].x, P[3].y, za))], M['puddle'], [(t0, 0), (t1, 0), (t1, 1), (t0, 1)])
    return at

def jerrycan(Bk, M, pos, yaw, s=1.0):
    """Olive 5-gallon jerrycan (0.7 x 0.35 x 0.95 D at s=1) with the X pressings and a 3-bar handle."""
    F = BK.Frame(pos, yaw); b = Bk('jerry', hull=0.0); hx, hy, hz = 0.33 * s, 0.17 * s, 0.46 * s
    obox(b, F.p(0, 0, hz), F.X, F.Y, F.Z, hx, hy, hz, M['olive'])
    for sy in (-1, 1):
        for (a, c) in (((-0.8, -0.8), (0.8, 0.8)), ((-0.8, 0.8), (0.8, -0.8))):
            rod(b, F.p(a[0] * hx, sy * (hy + 0.012), hz + a[1] * hz), F.p(c[0] * hx, sy * (hy + 0.012), hz + c[1] * hz), 0.03 * s, M['olive_d'], seg=4)
    for xx in (-0.18, 0.0, 0.18): rod(b, F.p(xx * s, 0, 2 * hz), F.p(xx * s, 0, 2 * hz + 0.16 * s), 0.03 * s, M['olive_d'], seg=4)
    rod(b, F.p(-0.22 * s, 0, 2 * hz + 0.16 * s), F.p(0.22 * s, 0, 2 * hz + 0.16 * s), 0.035 * s, M['olive_d'], seg=4)
    rod(b, F.p(0.24 * s, 0, 2 * hz), F.p(0.3 * s, 0, 2 * hz + 0.12 * s), 0.07 * s, M['metal'], seg=6)

def toolbox(Bk, M, pos, yaw, s=1.0):
    """Open wooden tool tray: four sides, a centre handle bar, a mallet and a spanner lying in it, a rubber patch roll beside it."""
    F = BK.Frame(pos, yaw); b = Bk('toolbox', hull=0.0); hx, hy, hz = 0.55 * s, 0.28 * s, 0.17 * s; t = 0.03 * s
    obox(b, F.p(0, 0, 0.02 * s), F.X, F.Y, F.Z, hx, hy, 0.02 * s, M['wood'])
    for sy in (-1, 1): obox(b, F.p(0, sy * (hy - t), hz), F.X, F.Y, F.Z, hx, t, hz, M['wood'])
    for sx in (-1, 1): obox(b, F.p(sx * (hx - t), 0, hz + 0.08 * s), F.X, F.Y, F.Z, t, hy, hz + 0.08 * s, M['wood'])
    rod(b, F.p(-hx, 0, 2 * hz + 0.12 * s), F.p(hx, 0, 2 * hz + 0.12 * s), 0.035 * s, M['trunk_l'], seg=6)
    rod(b, F.p(-0.35 * s, -0.12 * s, 0.12 * s), F.p(0.25 * s, -0.1 * s, 0.14 * s), 0.03 * s, M['trunk_l'], seg=5); obox(b, F.p(0.3 * s, -0.1 * s, 0.14 * s), F.X, F.Y, F.Z, 0.07 * s, 0.12 * s, 0.06 * s, M['metal'])
    rod(b, F.p(-0.3 * s, 0.12 * s, 0.1 * s), F.p(0.3 * s, 0.1 * s, 0.1 * s), 0.025 * s, M['metal'], seg=5)
    c = F.p(0.0, -hy - 0.45 * s, 0.16 * s); rod(b, c - F.Y * (0.0) - F.X * 0.22 * s, c + F.X * 0.22 * s, 0.16 * s, M['rubber_d'], seg=12)

# ============================================================================= set r1: animatable tanks (shape keys), the production prop kit
class MBRec(MB):
    """MB that records which vertex index every _vert call returned (the call order of a builder)."""
    def __init__(s): MB.__init__(s); s.calls = []
    def _vert(s, p):
        i = MB._vert(s, p); s.calls.append(i); return i

class MBFollow(MB):
    """Replays a builder against a recorded MBRec: the k-th _vert call maps to the recorded index, its position is stored -> same topology."""
    def __init__(s, rec):
        MB.__init__(s); s.rec = rec; s.k = 0; s.pos = [None] * len(rec.v)
    def _vert(s, p):
        i = s.rec.calls[s.k]; s.k += 1
        if s.pos[i] is None: s.pos[i] = (p[0], p[1], p[2])
        return i
    def face(s, pts, mat, uvs=None):
        for p in pts: s._vert(p)
    def oface(s, pts, mat, uvs, normal):
        # same flip decision as the recording is NOT guaranteed, so follow the recorded call order: positions only, no flip
        for p in pts: s._vert(Vector(p))

INFLATE_KEYS = (0.0, 0.25, 0.5, 0.75)
_TANK_CACHE = {}

def tank_shape_mesh(M, lod=1.0, seed=1, valve_x=0.9, valve_side=1, elev_key=35.0):
    """One tank mesh (basis = fully inflated, sag 0, barrel level) with shape keys i0 / i25 / i50 / i75 (the shape at that inflate),
    sag (barrel limp at full inflate) and elev (barrel raised `elev_key` deg).  Cached per (lod, seed, valve)."""
    key = (round(lod, 2), seed, valve_x, valve_side, STATE['pre'])
    if key in _TANK_CACHE and _TANK_CACHE[key].name in bpy.data.meshes: return _TANK_CACHE[key]
    kw = dict(seed=seed, lod=lod, valve_x=valve_x, valve_side=valve_side, star_f=1.0)
    rec = MBRec(); tank_mesh(M, 1.0, 0.0, mb=rec, **kw); info = rec.info
    tmp = _obj(rec, 'tankmesh_tmp', STATE['SET'], hull=0.0); me = tmp.data; bpy.data.objects.remove(tmp, do_unlink=True)
    me.name = 'tankmesh_%s_%d_%g' % (STATE['pre'], seed, lod)
    for p in me.polygons: p.use_smooth = True
    ob = bpy.data.objects.new('tank_keys_tmp', me); STATE['SET'].objects.link(ob)
    ob.shape_key_add(name='Basis', from_mix=False)
    def add(name, **a):
        fo = MBFollow(rec); tank_mesh(M, mb=fo, **dict(kw, **a)); assert fo.k == len(rec.calls), (name, fo.k, len(rec.calls))
        sk = ob.shape_key_add(name=name, from_mix=False)
        for i, p in enumerate(fo.pos):
            if p is not None: sk.data[i].co = p
    for v in INFLATE_KEYS: add('i%d' % int(v * 100), inflate=v, sag=0.0)
    add('sag', inflate=1.0, sag=1.0); add('elev', inflate=1.0, sag=0.0, elev=elev_key)
    bpy.data.objects.remove(ob, do_unlink=True); me['info'] = str(info); me['elev_key'] = elev_key
    _TANK_CACHE[key] = me; return me

def tank_weights(inflate):
    """Shape key weights for an inflate value (piecewise linear between the i-keys and the basis at 1)."""
    lv = list(INFLATE_KEYS) + [1.0]; v = max(0.0, min(1.0, inflate)); w = {('i%d' % int(k * 100)): 0.0 for k in INFLATE_KEYS}
    for a, b in zip(lv, lv[1:]):
        if a <= v <= b:
            t = (v - a) / (b - a)
            if a < 1.0: w['i%d' % int(a * 100)] = 1.0 - t
            if b < 1.0: w['i%d' % int(b * 100)] = t
            break
    return w

def make_tank(name, loc, yaw, M, inflate=1.0, sag=0.0, elev=0.0, lod=1.0, seed=1, hull=0.0, scale=1.0, own=True, **kw):
    """A rubber tank object with live inflate / sag / elev (shape keys).  own=True gives it its own mesh copy (needed when its shape is
    keyed per tank; GH.set_inflate makes the copy on demand)."""
    me = tank_shape_mesh(M, lod, seed, **kw)
    if own: me = me.copy(); me.name = name + '_mesh'
    ob = bpy.data.objects.new(name, me); STATE['SET'].objects.link(ob); ob.location = loc; ob.rotation_euler = (0, 0, math.radians(yaw)); ob.scale = (scale,) * 3
    if hull > 0:
        mats = me.materials; ink = [i for i, m in enumerate(mats) if m.name.startswith('ink')]
        if not ink: mats.append(T.mat_ink()); ink = [len(mats) - 1]
        mod = ob.modifiers.new('ink_hull', 'SOLIDIFY'); mod.thickness = hull / max(scale, 1e-3); mod.offset = 1.0; mod.use_flip_normals = True; mod.use_rim = False; mod.material_offset = ink[0]; mod.use_even_offset = True
    no_bounce(ob); ob['tank'] = True; ob['inflate'] = 1.0; ob['sag'] = 0.0; ob['elev'] = 0.0; ob['info'] = me.get('info', '')
    STATE.setdefault('objects', {})[name] = ob; STATE.setdefault('tank_objs', {})[name] = ob
    set_tank_shape(ob, inflate, sag, elev)
    return ob

def set_tank_shape(ob, inflate=None, sag=None, elev=None, frame=None):
    """Drive the shape keys of one tank object; with frame: key them (LINEAR)."""
    kb = ob.data.shape_keys.key_blocks
    if inflate is not None:
        ob['inflate'] = float(inflate)
        for k, w in tank_weights(inflate).items(): kb[k].value = w
    if sag is not None: ob['sag'] = float(sag); kb['sag'].value = max(0.0, min(1.0, sag)) * max(0.0, min(1.0, ob['inflate']))
    if elev is not None: ob['elev'] = float(elev); kb['elev'].value = max(0.0, min(1.5, elev / ob.data.get('elev_key', 35.0)))
    if frame is not None:
        for k in kb[1:]:
            k.keyframe_insert('value', frame=frame)
        _lin(ob.data.shape_keys)

def _lin(idb):
    ad = idb.animation_data
    if ad and ad.action:
        for fc in _fcs(ad.action):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def _fcs(action):
    """F-curves of an action (Blender 4.4+ layered actions or legacy)."""
    try:
        out = []
        for l in action.layers:
            for st in l.strips:
                for cb in st.channelbags: out += list(cb.fcurves)
        if out: return out
    except Exception: pass
    return list(getattr(action, 'fcurves', []))
