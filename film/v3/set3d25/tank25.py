#!/usr/bin/env python3
"""tank25.py : the Mark I of film 25 with HOOKS (build stages, drive, crossing, states, stencil, sparks).  bpy 5.x.  Imported lazily by front.build_tank.

    import tank25 as TK
    t = TK.build_tank('mk1', pos, yaw, pitch, roll, mud=1.0)      # TankH (dict + attribute access); t.root is the root empty
    TK.set_build(t, dict(chassis=1, plates=.4, rivets=0, tracks=0, sponsons=0, guns=0), frame=12)
    TK.set_drive(t, dist, frame=12)                              # links scroll round the loop, tail wheels roll
    TK.setup_crossing(t, origin_xy, yaw, s_a, s_b); TK.set_crossing(t, u, frame=12)    # u 0..1: approach, nose lift, grip, pull, level
    TK.set_state(t, 'stuck'|'smoking'|'tilted'|'normal', level, frame=12);  TK.set_stencil(t, on, frame);  TK.set_sparks(t, t_sec, frame)
Local frame: origin = front end of the straight bottom run, x forward, y left, z up (see API.md)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import front as F
from front import S, MB, rnd, mkobj, poly_face, obox, beam, rod, ell, hexl, NB, J, T

TANK_OUT = F.TANK_OUT; TRACK_Y = F.TRACK_Y; HULL_HW = F.HULL_HW
STAGES = ('chassis', 'plates', 'rivets', 'tracks', 'sponsons', 'guns')
LINK_STEP = 0.60
COM = (-4.0, 2.2)                                   # centre of mass in the local (x, z) plane (for the resting pose)
TAIL_HINGE = (-10.3, 2.6); TAIL_AX = (-7.4, -0.65); TAIL_R = 1.95
N_RIV = 10

class TankH(dict):
    __getattr__ = dict.__getitem__
    def __setattr__(s, k, v): s[k] = v

def ease(x): x = min(1.0, max(0.0, x)); return x * x * (3 - 2 * x)

# ----------------------------------------------------------------------------- materials (mud factor per tank: factory tanks are clean)
def tank_mats(mud=1.0, tag=''):
    key = 'tm_%s_%d' % (tag, int(mud * 100))
    if key in S: return S[key]
    M = S['M']; nm = lambda n: n + '_%d' % int(mud * 100)
    def camo(b):
        c = b.coord(); vv = b.n('ShaderNodeTexVoronoi', voronoi_dimensions='3D', feature='F1'); vv.inputs['Scale'].default_value = 0.40; vv.inputs['Randomness'].default_value = 1.0
        wp = b.n('ShaderNodeVectorMath', operation='ADD'); b.l(c, wp.inputs[0]); wv = b.n('ShaderNodeVectorMath', operation='SCALE'); wv.inputs['Scale'].default_value = 1.6
        nz3 = b.n('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 0.8; nz3.inputs['Detail'].default_value = 2.0; b.l(c, nz3.inputs['Vector']); b.l(nz3.outputs['Color'], wv.inputs[0]); b.l(wv.outputs[0], wp.inputs[1]); b.l(wp.outputs[0], vv.inputs['Vector'])
        ve = b.n('ShaderNodeTexVoronoi', voronoi_dimensions='3D', feature='DISTANCE_TO_EDGE'); ve.inputs['Scale'].default_value = 0.40; ve.inputs['Randomness'].default_value = 1.0; b.l(wp.outputs[0], ve.inputs['Vector'])
        g = b.n('ShaderNodeRGBToBW'); b.l(vv.outputs['Color'], g.inputs[0])
        ramp = b.n('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
        pal = ['#cf9a2e', '#5c8a34', '#7c4a26', '#bcae6c']; cr.elements[0].position = 0.0; cr.elements[0].color = (*hexl(pal[0]), 1); cr.elements[1].position = 0.25; cr.elements[1].color = (*hexl(pal[1]), 1)
        for pos, cc in ((0.5, pal[2]), (0.75, pal[3])): e = cr.elements.new(pos); e.color = (*hexl(cc), 1)
        b.l(g.outputs[0], ramp.inputs['Fac'])
        edge = b.rng(ve.outputs['Distance'], 0.0, 0.035, 1.0, 0.0); col = b.mix(edge, ramp.outputs['Color'], (0.07, 0.06, 0.05))
        z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); mudm = b.rng(z.outputs['Z'], 0.1, 1.5, 1.0, 0.0); dn = b.noise(5.0, 3.0, 0.6, c, None)
        mm = b.math('MULTIPLY', b.math('MULTIPLY', mudm, b.rng(dn, 0.35, 0.7, 0.4, 1.0)), mud)
        return b.mix(mm, col, (0.22, 0.15, 0.09))
    def hullm(b):
        col = camo(b); uv = b.n('ShaderNodeUVMap').outputs[0]; br = b.n('ShaderNodeTexBrick'); br.offset = 0.5; br.offset_frequency = 2; br.squash = 1.0
        br.inputs['Brick Width'].default_value = F.PLATE_W; br.inputs['Row Height'].default_value = F.PLATE_H; br.inputs['Mortar Size'].default_value = 0.035; br.inputs['Mortar Smooth'].default_value = 0.35; br.inputs['Scale'].default_value = 1.0
        br.inputs['Bias'].default_value = 0.0; br.inputs['Color1'].default_value = (1, 1, 1, 1); br.inputs['Color2'].default_value = (0.9, 0.9, 0.9, 1); br.inputs['Mortar'].default_value = (0.0, 0.0, 0.0, 1); b.l(uv, br.inputs['Vector'])
        seam = b.math('SUBTRACT', 1.0, br.outputs['Fac']); col = b.mul(col, b.mix(b.math('MULTIPLY', seam, 0.8), (1, 1, 1), (0.35, 0.33, 0.3)))
        nn = b.noise(18.0, 3.0, 0.6, None, None); h = b.math('ADD', b.math('MULTIPLY', br.outputs['Fac'], 0.7), b.math('MULTIPLY', nn, 0.08))
        b.princ(col, 0.55, 0.12, b.bump(h, 1.0, 0.06))
    def trackm(b):
        c = b.coord(); oi = b.n('ShaderNodeObjectInfo'); mp = b.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 1.5,) * 3; b.l(c, mp.inputs['Vector'])
        t = b.n('ShaderNodeTexImage'); t.image = F._img('steel_c'); t.projection = 'BOX'; b.l(mp.outputs[0], t.inputs['Vector']); nn = b.noise(4.0, 3.0, 0.6, c, None)
        col = b.mul(t.outputs['Color'], (*hexl('#5b4a3a'), 1)); col = b.mix(b.math('MULTIPLY', b.rng(nn, 0.35, 0.65), b.math('MULTIPLY', b.rng(oi.outputs['Random'], 0.0, 1.0, 0.45, 1.0), mud)), col, (0.34, 0.2, 0.1))
        col = b.mix(b.math('MULTIPLY', b.rng(oi.outputs['Random'], 0.0, 1.0, 0.0, 0.4), mud), col, (0.25, 0.17, 0.1))
        if mud < 0.5: col = b.mul(col, (1.5, 1.35, 1.2, 1))
        b.princ(col, 0.62, 0.55, b.bump(nn, 0.5, 0.05))
    d = dict(hull=F.fmat(nm('thull'), hullm), track=F.fmat(nm('ttrack'), trackm))
    d['frame'] = F.flat('t_frame', '#8a3c2c', 0.6, 0.3); d['frame2'] = F.flat('t_frame2', '#4a5058', 0.45, 0.7); d['engine'] = F.flat('t_engine', '#3d5a6a', 0.5, 0.55)
    d['brass'] = F.flat('t_brass', '#b08a3a', 0.35, 0.8)
    def paint(b): b.princ(hexl('#cfc6aa'), 0.85, 0.0, None)
    d['paint'] = F.fmat('t_paint', paint); d['paint_d'] = F.flat('t_paint_d', '#3a3a3a', 0.85)
    def spark(b):
        e = b.n('ShaderNodeEmission'); e.inputs['Color'].default_value = (1.0, 0.82, 0.45, 1); e.inputs['Strength'].default_value = 6.0; b.l(e.outputs[0], b.out.inputs['Surface'])
    d['spark'] = F.fmat('t_spark', spark)
    S[key] = d; return d

# ----------------------------------------------------------------------------- water-tank silhouette decal (plain shape, never letters)
def tank_silhouette(mb, c, X, Y, Z, s, mat_p, mat_d, lift=0.0):
    """flat water-tank silhouette (cylinder on legs with a tap) in the plane spanned by X (horizontal) and Z (up) at centre c, outward normal Y, total height ~2*s.  Shapes are layered 0.012 apart."""
    c = Vector(c); X, Y, Z = Vector(X), Vector(Y), Vector(Z); layer = [0]
    def P(u, v, k): return c + X * (u * s) + Z * (v * s) + Y * (lift + 0.012 * k)
    def poly(pts2, m, k): mb.pid += 1; mb.oface([P(u, v, k) for (u, v) in pts2], m, [(0, 0)] * len(pts2), Y)
    def rect(u0, v0, u1, v1, m, k): poly([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], m, k)
    def ellipse(cu, cv, rx, ry, m, k, n=24): poly([(cu + rx * math.cos(2 * math.pi * i / n), cv + ry * math.sin(2 * math.pi * i / n)) for i in range(n)], m, k)
    o = 0.06                                                              # dark outline = same shape slightly bigger, below
    for (lu0, lu1) in ((-0.42, -0.30), (0.30, 0.42)): rect(lu0 - o, -1.05 - o, lu1 + o, -0.6, mat_d, 1); rect(lu0, -1.05, lu1, -0.6, mat_p, 2)
    ellipse(0, -0.58, 0.58 + o, 0.17 + o, mat_d, 1); rect(-0.58 - o, -0.58, 0.58 + o, 0.62, mat_d, 1); ellipse(0, 0.62, 0.58 + o, 0.17 + o, mat_d, 1)
    ellipse(0, -0.58, 0.58, 0.17, mat_p, 3); rect(-0.58, -0.58, 0.58, 0.62, mat_p, 3); ellipse(0, 0.62, 0.58, 0.17, mat_p, 3)
    for v in (0.22, -0.2): rect(-0.58, v - 0.03, 0.58, v + 0.03, mat_d, 4)                       # bands
    ellipse(0, 0.62, 0.45, 0.11, mat_d, 4); ellipse(0, 0.62, 0.40, 0.09, mat_p, 5)
    rect(0.55 - o, -0.33 - o, 0.88 + o, -0.25 + o, mat_d, 1); rect(0.55, -0.33, 0.88, -0.25, mat_p, 4)                    # tap: pipe, spout, handle
    rect(0.80 - o, -0.52 - o, 0.88 + o, -0.25 + o, mat_d, 1); rect(0.80, -0.52, 0.88, -0.25, mat_p, 4)
    rect(0.62, -0.25, 0.64, -0.14, mat_d, 4); rect(0.56, -0.16, 0.70, -0.12, mat_d, 4)

# ----------------------------------------------------------------------------- rivet sink: chunks along x so rows can punch in one after the other
class RivetSink:
    def __init__(s, n=N_RIV, x0=-11.0, x1=4.0): s.n = n; s.x0 = x0; s.x1 = x1; s.mbs = [MB() for _ in range(n)]
    def pick(s, x): return s.mbs[min(s.n - 1, max(0, int((x - s.x0) / (s.x1 - s.x0) * s.n)))]
    def frustum(s, p0, p1, r0, r1, mat, **kw): s.pick(Vector(p0).x).frustum(p0, p1, r0, r1, mat, **kw)

# ----------------------------------------------------------------------------- the build
def track_path():
    return F.round_poly([(x, z) for x, z in TANK_OUT], [1.6, 1.3, 1.3, 1.5], 8)

def path_tables(res=0.05):
    pts = [Vector(p) for p in track_path()]; P = pts + [pts[0]]; L = [(P[i + 1] - P[i]).length for i in range(len(P) - 1)]; cum = np.concatenate([[0], np.cumsum(L)])
    return P, cum, float(cum[-1])

def path_at(s, tab):
    P, cum, tot = tab; s = s % tot; i = int(np.searchsorted(cum, s, side='right') - 1); i = min(i, len(P) - 2); l = cum[i + 1] - cum[i]
    t = (s - cum[i]) / max(l, 1e-9); p = P[i] + (P[i + 1] - P[i]) * t; tan = (P[i + 1] - P[i]).normalized(); return p, tan

def build_tank(name='tank', pos=(0, 0, 0), yaw=0.0, pitch=0.0, roll=0.0, camo=True, roof_mesh=False, tail=True, tail_angle=0.0, mud=1.0, stencil=True):
    TM = tank_mats(mud, 'a'); M = dict(S['M']); M.update(TM); M['hull'] = TM['hull']; M['track'] = TM['track']
    root = F.empty(name, loc=pos); root.rotation_mode = 'XYZ'; root.rotation_euler = (math.radians(roll), -math.radians(pitch), math.radians(yaw))
    H = TankH(name=name, root=root, mats=TM, groups={}, parts={}, base=dict(pos=tuple(pos), yaw=yaw, pitch=pitch, roll=roll), links={'L': [], 'R': []}, state={}, sparks=[], stencils=[], smoke=None, drive=0.0)
    S.setdefault('tanks', {})[name] = root
    def group(stage, subs=None):
        g = F.empty('%s_g_%s' % (name, stage), parent=root); H.groups[stage] = g; H.parts[stage] = []
        for (sn, dirv) in (subs or [('', (0, 0, 0))]):
            e = F.empty('%s_g_%s%s' % (name, stage, sn), parent=g); H.parts[stage].append((e, Vector(dirv))); H['_sub_' + stage + sn] = e
        return g
    group('chassis'); group('plates', [('', (0, 0, 16.0))]); group('rivets'); group('tracks', [('', (0, 0, 14.0))])
    group('sponsons', [('L', (0, 5.5, 0)), ('R', (0, -5.5, 0))]); group('guns', [('L', (0, 6.0, 0)), ('R', (0, -6.0, 0))])
    E = lambda st, sn='': H['_sub_' + st + sn]
    # ---- tracks: one object per link (shared mesh), parented to the track group; positions set by set_drive
    tab = path_tables(); H.tab = tab; Ltot = tab[2]; nl = int(round(Ltot / LINK_STEP)); H.L_total = Ltot; H.n_links = nl; y0, y1 = TRACK_Y
    tmpl = []
    for par in (0, 1):
        mb = MB(); wid = (y1 - y0) / 2
        mb.pid += 1; obox(mb, (0, 0, 0.07), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.275, wid, 0.07, M['track']); obox(mb, (0, 0, -0.05), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.11, wid - 0.04, 0.07, M['track'])
        if par == 0:
            for yy in (-wid + 0.2, wid - 0.2): mb.frustum((0.12, yy, -0.1), (0.12, yy, -0.25), 0.06, 0.04, M['rivet'], seg=5, cap0=False)
        me = mb.obj('%s_linkmesh%d' % (name, par), S['coll'], smooth=False).data; tmpl.append(me)
        o_ = bpy.data.objects.get('%s_linkmesh%d' % (name, par)); bpy.data.objects.remove(o_, do_unlink=True)
    for sd, sg in (('L', 1), ('R', -1)):
        te = F.empty('%s_track%s' % (name, sd), parent=E('tracks'))
        for i in range(nl):
            ob = bpy.data.objects.new('%s_link%s%d' % (name, sd, i), tmpl[i % 2]); S['coll'].objects.link(ob); ob.parent = te; H.links[sd].append(ob)
    H.link_y = (y0 + y1) / 2
    # ---- hull plates
    ins = F.inset_poly(TANK_OUT, 0.62); mb = MB(); sink = RivetSink(); H0 = TRACK_Y[0] - 0.05; hh = HULL_HW
    for sg in (1, -1):
        poly = [(x, sg * hh, z) for x, z in ins]; nrm = (0, sg, 0); poly_face(mb, poly, M['hull'], nrm)
        small = F.inset_poly(ins, 0.3)
        F.rivet_rows(sink, lambda u, v: (u, sg * (hh + 0.0), v), nrm, lambda u, v: F.point_in_poly(small, u, v), -10, 4, -0.5, 5.0)
        F.edge_rivets(sink, [(x, sg * hh, z) for x, z in small], nrm)
    n_ = len(ins)
    for i in range(n_):
        a, b = ins[i], ins[(i + 1) % n_]; e = Vector((b[0] - a[0], b[1] - a[1])); nn = Vector((e.y, -e.x)).normalized()
        q = [(a[0], -hh, a[1]), (b[0], -hh, b[1]), (b[0], hh, b[1]), (a[0], hh, a[1])]; poly_face(mb, q, M['hull'], (nn.x, 0, nn.y))
        nrm3 = (nn.x, 0, nn.y); Lp = e.length; ed = e.normalized()
        def to3(u, v, a=a, ed=ed): return (a[0] + ed.x * u, v, a[1] + ed.y * u)
        for k in range(1, int(Lp / 2.6) + 1):
            u = k * 2.6 - 0.6
            if u > Lp - 0.3: break
            for sg_ in (-1, 1):
                for j in range(-int(hh / 0.44), int(hh / 0.44) + 1): p = Vector(to3(u + sg_ * 0.17, j * 0.44 + 0.22)); sink.frustum(p, p + Vector(nrm3) * 0.075, 0.095, 0.058, M['rivet'], seg=6)
        for sg_ in (-1, 1):
            for k in range(1, int(Lp / 0.44)): p = Vector(to3(k * 0.44, sg_ * 0.17)); sink.frustum(p, p + Vector(nrm3) * 0.075, 0.095, 0.058, M['rivet'], seg=6)
    mkobj(mb, name + '_hull', parent=E('plates'))
    H.rivet_objs = []
    for k, rm in enumerate(sink.mbs):
        if rm.f: H.rivet_objs.append(mkobj(rm, '%s_rivets%d' % (name, k), parent=E('rivets')))
    # ---- cab, roof furniture (plates group)
    mb = MB(); mbr = MB(); ms = MB(); zt = 3.9; cx0, cx1, cy = 0.2, 3.0, 1.15; zc = zt + 0.75
    mb.box((cx0, -cy, zt - 0.1), (cx1, cy, zc), M['hull']); mb.pid += 1
    for (x0_, y0_, x1_, y1_) in ((cx1 - 0.02, -0.9, cx1 + 0.03, -0.35), (cx1 - 0.02, 0.35, cx1 + 0.03, 0.9)): ms.box((x0_, y0_, zc - 0.62), (x1_, y1_, zc - 0.4), M['slit'])
    for sg in (1, -1): ms.box((1.4, sg * cy - 0.02, zc - 0.62), (2.2, sg * cy + sg * 0.03, zc - 0.4), M['slit'])
    mb.box((cx0 - 0.15, -cy - 0.12, zc), (cx1 + 0.15, cy + 0.12, zc + 0.14), M['hull'])
    for xr in (cx0, cx1):
        for k in range(-5, 6): mbr.frustum(Vector((xr + (-0.1 if xr == cx0 else 0.1), k * 0.22, zc + 0.14)), Vector((xr + (-0.1 if xr == cx0 else 0.1), k * 0.22, zc + 0.205)), 0.07, 0.045, M['rivet'], seg=6)
    for sg in (1, -1):
        for k in range(1, 12): mbr.frustum(Vector((cx0 + k * 0.24, sg * cy, zc - 0.28)), Vector((cx0 + k * 0.24, sg * (cy + 0.075), zc - 0.28)), 0.07, 0.045, M['rivet'], seg=6)
    mb.box((-1.6, -0.55, zt), (-0.4, 0.55, zt + 0.35), M['hull'])
    rod(ms, (-2.0, -0.85, zt + 0.52), (-6.3, -0.85, zt + 0.52), 0.2, M['steel'], 10); rod(ms, (-4.7, -0.85, zt + 0.52), (-6.9, -0.85, zt + 0.52), 0.46, M['steel'], 12)
    for xk in (-2.6, -5.5): rod(ms, (xk, -0.85, zt), (xk, -0.85, zt + 0.5), 0.07, M['rivet'], 5)
    if roof_mesh:
        for k in range(0, 14): x = -6.0 + k * 0.7; rod(ms, (x, -1.7, zt + 0.7), (x, 1.7, zt + 0.7), 0.025, M['wire'], 4)
        for k in range(0, 8): y = -1.75 + k * 0.5; rod(ms, (-6.0, y, zt + 0.7), (3.4, y, zt + 0.7), 0.025, M['wire'], 4)
        for (x, y) in ((-6, -1.7), (-6, 1.7), (3.2, -1.7), (3.2, 1.7)): rod(ms, (x, y, zt), (x, y, zt + 0.72), 0.05, M['steel'], 5)
    mkobj(mb, name + '_cab', parent=E('plates')); mkobj(mbr, name + '_cabriv', parent=E('plates')); mkobj(ms, name + '_roof', parent=E('plates'), smooth=True)
    # ---- sponsons + guns
    for sd, sg in (('L', 1), ('R', -1)):
        mb = MB(); mbr = MB(); mg = MB(); xc = -1.4; zlo, zhi = 0.95, 3.3; yi, yo = hh - 0.05, 4.25; wi, wo = 2.65, 1.45
        P = lambda x, y, z: (xc + x, sg * y, z); v = {}
        for nm_, (x, y, z) in dict(a=(-wi, yi, zlo), b=(wi, yi, zlo), c=(wo, yo, zlo), d=(-wo, yo, zlo), e=(-wi, yi, zhi), f=(wi, yi, zhi), g=(wo, yo, zhi - 0.25), h=(-wo, yo, zhi - 0.25)).items(): v[nm_] = P(x, y, z)
        faces = [('d', 'c', 'g', 'h'), ('a', 'd', 'h', 'e'), ('b', 'f', 'g', 'c'), ('e', 'h', 'g', 'f'), ('a', 'b', 'c', 'd')]; cen = Vector((xc, sg * (yi + yo) / 2, (zlo + zhi) / 2))
        for fcs in faces:
            pts = [v[k] for k in fcs]; c_ = sum((Vector(p) for p in pts), Vector()) / 4; nn = (Vector(pts[1]) - Vector(pts[0])).cross(Vector(pts[3]) - Vector(pts[0])).normalized()
            if nn.dot(c_ - cen) < 0: nn = -nn
            poly_face(mb, pts, M['hull'], tuple(nn)); F.edge_rivets(mbr, pts, tuple(nn), 0.42)
            if fcs == ('d', 'c', 'g', 'h'): front_n = nn
        gc = Vector(P(0.0, yo, 2.05)); fn = Vector(front_n); X_ = Vector((1, 0, 0)); Z_ = Vector((0, 0, 1)); Y_ = fn
        obox(mg, gc + fn * 0.1, X_, Y_, Z_, 0.78, 0.1, 0.78, M['steel_l']); mg.pid += 1
        for k in range(8):
            a_ = k * math.pi / 4; q = gc + fn * 0.22 + X_ * math.cos(a_) * 0.64 + Z_ * math.sin(a_) * 0.64; mg.frustum(q, q + fn * 0.08, 0.075, 0.05, M['rivet'], seg=6)
        mg.sphere(gc + fn * 0.28, 0.47, M['gun'], 12, 8)
        d = Vector((0.30, sg * 1.0, -0.03)).normalized(); b0 = gc + fn * 0.6; b1 = b0 + d * 2.3
        rod(mg, b0, b1, 0.24, M['gun'], 10, 0.18); rod(mg, b1 - d * 0.5, b1 + d * 0.12, 0.27, M['gun'], 10, 0.27); rod(mg, b0 + d * 0.1, b0 + d * 0.55, 0.32, M['gun'], 10, 0.26)
        mkobj(mb, '%s_sponson%s' % (name, sd), parent=E('sponsons', sd)); mkobj(mbr, '%s_spriv%s' % (name, sd), parent=E('sponsons', sd)); mkobj(mg, '%s_gun%s' % (name, sd), parent=E('guns', sd), smooth=True)
        H['muzzle' + sd] = (b1 + d * 0.12, d)
    # ---- chassis: bare frame (girders along the hull outline, cross members, floor, engine) + steering tail
    mb = MB(); mf = M['frame']; fi = F.inset_poly(TANK_OUT, 0.55); n_ = len(fi)
    for sg in (1, -1):
        for i in range(n_):
            a, b = fi[i], fi[(i + 1) % n_]; beam(mb, (a[0], sg * 1.75, a[1]), (b[0], sg * 1.75, b[1]), 0.32, 0.42, mf)
            beam(mb, (a[0], sg * 1.75, a[1]), (a[0], sg * 1.75, a[1]), 0.1, 0.1, mf) if False else None
        for x in (-9.0, -6.5, -4.0, -1.5, 0.8, 2.8):                                                  # uprights + diagonal braces
            zb = 0.0 if x < 0.2 else x - 0.2; zt_ = 4.25 - (x + 6.8) * 0.04 if x > -6.8 else (x + 11) * 1.0
            zt_ = min(zt_, 4.15); beam(mb, (x, sg * 1.75, zb + 0.2), (x, sg * 1.75, max(zb + 1.0, zt_ - 0.2)), 0.26, 0.26, mf)
    for x in (-9.5, -7.5, -5.5, -3.5, -1.5, 0.3):
        beam(mb, (x, -1.75, 0.35), (x, 1.75, 0.35), 0.3, 0.3, mf)
    for x in (-6.0, -3.0, 0.5): beam(mb, (x, -1.75, 3.8), (x, 1.75, 3.8), 0.3, 0.3, mf)
    mb.box((-9.8, -1.6, 0.18), (0.1, 1.6, 0.4), M['frame2'])
    for k in range(5): mb.box((-7.2 + k * 1.3, -0.75, 0.4), (-6.2 + k * 1.3, 0.75, 1.9), M['engine'])
    mb.box((-8.1, -1.0, 0.4), (-2.9, 1.0, 0.9), M['engine']); mb.box((-3.0, -1.1, 0.4), (-0.6, 1.1, 2.1), M['frame2']); mb.box((-10.2, -1.2, 0.5), (-9.0, 1.2, 3.0), M['frame2'])
    for k in range(5): rod(mb, (-7.0 + k * 1.3, 0, 1.9), (-7.0 + k * 1.3, 0, 2.5), 0.28, M['brass'], 8)
    mkobj(mb, name + '_chassis', parent=H.groups['chassis'])
    if tail:
        hinge = F.empty(name + '_tail', parent=H.groups['chassis'], loc=(TAIL_HINGE[0], 0, TAIL_HINGE[1])); hinge.rotation_euler = (0, -math.radians(tail_angle), 0); root['tail'] = hinge.name; H.tail = hinge
        mb = MB(); R = TAIL_R; ax = (TAIL_AX[0], 0.0, TAIL_AX[1])
        for sg in (1, -1):
            beam(mb, (0.3, sg * 1.05, 0.0), (ax[0], sg * 1.45, ax[2]), 0.5, 0.45, M['frame2']); beam(mb, (0.3, sg * 1.05, -0.9), (ax[0] + 0.3, sg * 1.45, ax[2] - 0.2), 0.4, 0.34, M['frame2']); beam(mb, (0.3, sg * 1.05, 0.0), (0.3, sg * 1.05, -0.9), 0.5, 0.5, M['frame2'])
        beam(mb, (ax[0] + 0.1, -1.5, ax[2]), (ax[0] + 0.1, 1.5, ax[2]), 0.45, 0.45, M['frame2']); beam(mb, (-3.8, -1.2, 0.2), (-3.8, 1.2, 0.2), 0.4, 0.4, M['frame2'])
        rod(mb, (ax[0], -2.9, ax[2]), (ax[0], 2.9, ax[2]), 0.14, M['steel'], 8); mkobj(mb, name + '_tailframe', parent=hinge)
        H.wheels = []
        for sg in (1, -1):
            we = F.empty('%s_wheel%s' % (name, 'L' if sg > 0 else 'R'), parent=hinge, loc=(ax[0], sg * 2.25, ax[2])); mw = MB()
            mw.frustum((0, -0.28, 0), (0, 0.28, 0), R, R, M['tirem'], seg=40, cap0=False, cap1=False)
            for ys in (-0.28, 0.28): mw.frustum((0, ys, 0), (0, ys + 0.06, 0), R, R - 0.28, M['steel'], seg=40)
            mw.frustum((0, -0.12, 0), (0, 0.12, 0), R - 0.35, R - 0.35, M['wheel'], seg=40, cap0=False, cap1=False); rod(mw, (0, -0.35, 0), (0, 0.35, 0), 0.42, M['steel'], 12)
            for k in range(14): a_ = k * 2 * math.pi / 14; rod(mw, (math.cos(a_) * 0.4, 0, math.sin(a_) * 0.4), (math.cos(a_) * (R - 0.3), 0, math.sin(a_) * (R - 0.3)), 0.075, M['wheel'], 6)
            mkobj(mw, '%s_tailwheel%d' % (name, sg), parent=we); H.wheels.append(we)
        S['tank_tail'] = hinge; S['tail_axle'] = (ax, R)
    # ---- stencil decals (hull sides, plain water-tank silhouette) + sparks rig
    if stencil:
        for sg in (1, -1):
            sm = MB(); tank_silhouette(sm, (-6.7, sg * (hh + 0.02), 2.35), (1, 0, 0), (0, sg, 0), (0, 0, 1), 1.0, TM['paint'], TM['paint_d'])
            if sg < 0: pass
            H.stencils.append(mkobj(sm, '%s_stencil%d' % (name, sg), parent=E('plates')))
    H.spark_pos = [(-7.8, 1.5), (-6.0, 3.2), (-4.4, 3.0), (-8.2, 2.7), (-5.4, 1.2), (-3.2, 3.9), (-9.0, 1.4), (-2.2, 4.1)]
    for sg in (1, -1):
        for i, (x, z) in enumerate(H.spark_pos):
            mbk = MB(); c = Vector((x, sg * (hh + 0.14), z)); X = Vector((1, 0, 0)); Zv = Vector((0, 0, 1)); Y = Vector((0, sg, 0)); r_ = rnd(900 + i + 17 * sg)
            for k in range(8):                                                           # star: 8 spikes alternately long / short
                a = k * math.pi / 4 + r_.uniform(-0.1, 0.1); ln = 0.55 if k % 2 == 0 else 0.3; w = 0.07
                d1 = X * math.cos(a) + Zv * math.sin(a); n1 = X * (-math.sin(a)) + Zv * math.cos(a)
                mbk.pid += 1; mbk.oface([c + n1 * w, c + d1 * ln, c - n1 * w], M['spark'], [(0, 0)] * 3, Y)
            for k in range(5):                                                           # tiny streaks flying off
                a = r_.uniform(0, 6.28); d1 = X * math.cos(a) + Zv * math.sin(a); p = c + d1 * r_.uniform(0.6, 1.1) + Y * 0.1
                mbk.pid += 1; mbk.oface([p, p + d1 * 0.18 + X * 0.02, p + d1 * 0.18 - X * 0.02], M['spark'], [(0, 0)] * 3, Y)
            ob = mkobj(mbk, '%s_spark%d_%d' % (name, sg, i), parent=root, shadow=False); ob.hide_render = True; ob.location = (0, 0, 0); H.sparks.append((ob, i, c.copy()))
    set_drive(H, 0.0)
    set_build(H, {s: 1.0 for s in STAGES})
    return H

# ----------------------------------------------------------------------------- hooks
def _key(ob, path, frame, idx=-1, interp='LINEAR'):
    if frame is None: return
    ob.keyframe_insert(path, index=idx, frame=frame)

def _vis(ob, vis, frame):
    ob.hide_render = not vis; ob.hide_viewport = not vis
    if frame is not None: ob.keyframe_insert('hide_render', frame=frame)

def _kids(e):
    out = []
    for c in e.children:
        out.append(c)
        out += _kids(c)
    return out

def set_build(H, levels, frame=None):
    """show / hide and slide the build stages: levels = {'chassis':1,'plates':.5,'rivets':.3,'tracks':0,'sponsons':0,'guns':0}; 0 = hidden / away, 1 = locked in place.
    plates drop from above (crane), tracks drop round the hull, sponsons slide in sideways, guns slide in along the barrel, rivets punch in chunk by chunk along the hull (level * n)."""
    for st, lv in levels.items():
        if st not in H.groups: continue
        lv = float(lv); e = ease(lv)
        for (sub, dirv) in H.parts[st]:
            sub.location = dirv * (1.0 - e)
            if st == 'plates': sub.rotation_euler = (0, 0.12 * (1.0 - e), 0)
            _key(sub, 'location', frame)
            if st == 'plates': _key(sub, 'rotation_euler', frame)
        if st == 'rivets':
            objs = H.rivet_objs; n = len(objs)
            for i, ob in enumerate(objs): _vis(ob, lv * n > i + 1e-6 or lv >= 0.999, frame)
        else:
            for (sub, dirv) in H.parts[st]:
                for ob in _kids(sub):
                    if ob.type == 'MESH': _vis(ob, lv > 0.001, frame)
    if 'plates' in levels:                                                               # stencil follows the plates and its own switch
        pass

def set_stencil(H, on, frame=None):
    for ob in H.stencils: _vis(ob, bool(on), frame)

def set_drive(H, dist, frame=None, wheels=True):
    """track links scroll round the loop with the distance travelled (hull frame: the bottom run moves backwards), the twin tail wheels roll."""
    tab = H.tab; Ltot = H.L_total; nl = H.n_links; H.drive = dist
    for sd, sg in (('L', 1), ('R', -1)):
        for i, ob in enumerate(H.links[sd]):
            s = (i * Ltot / nl - dist) % Ltot; p, tn = path_at(s, tab)
            ob.location = (p.x, sg * H.link_y, p.y); ob.rotation_euler = (0, -math.atan2(tn.y, tn.x), 0)
            if frame is not None: ob.keyframe_insert('location', frame=frame); ob.keyframe_insert('rotation_euler', frame=frame)
    if wheels and 'wheels' in H:
        for we in H.wheels:
            we.rotation_euler = (0, dist / TAIL_R, 0)
            if frame is not None: we.keyframe_insert('rotation_euler', frame=frame)

# ----------------------------------------------------------------------------- resting pose on a 2D profile (crossing, crater)
def rot2(x, z, th): return x * math.cos(th) - z * math.sin(th), x * math.sin(th) + z * math.cos(th)

def outline_pts(step=0.35):
    P = [Vector(p) for p in track_path()]; out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]; n = max(1, int((a - b).length / step))
        for k in range(n): q = a + (b - a) * (k / n); out.append((q.x, q.y))
    return np.array(out)

_OUT = None
def tail_geom(phi_deg):
    """tail wheel centres in the hull-local (x,z) plane for hinge angle phi (deg; the hinge rotates -phi about y)"""
    psi = -math.radians(phi_deg); hx, hz = TAIL_HINGE; ax, az = TAIL_AX
    return hx + ax * math.cos(psi) + az * math.sin(psi), hz - ax * math.sin(psi) + az * math.cos(psi)

def solve_pose(g, s, pitch_range=(-38, 38), tail=True, prefer=None):
    """resting pose of the rhomboid at position s along a path with ground profile g(s): the pitch that minimizes the height of the centre of mass while the track outline
    (and tail wheels) stay on or above the ground.  returns (z0, pitch_deg, tail_phi_deg).  `prefer(pitch_deg)` is an optional extra cost."""
    global _OUT
    if _OUT is None: _OUT = outline_pts()
    best = None
    for pd in np.arange(pitch_range[0], pitch_range[1] + 0.01, 1.0):
        th = math.radians(pd); xs = _OUT[:, 0] * math.cos(th) - _OUT[:, 1] * math.sin(th); zs = _OUT[:, 0] * math.sin(th) + _OUT[:, 1] * math.cos(th)
        gz = g(s + xs); z0 = float(np.max(gz - zs)); cx, cz = rot2(COM[0], COM[1], th); cost = z0 + cz + (prefer(pd) if prefer else 0.0)
        if best is None or cost < best[0]: best = (cost, z0, pd)
    _, z0, pd = best; th = math.radians(pd); phi = 0.0
    if tail:
        def gap(ph):
            cx, cz = tail_geom(ph); x, z = rot2(cx, cz, th); return z0 + z - TAIL_R - float(g(s + x))
        lo, hi = -40.0, 40.0
        for _ in range(26):
            mid = (lo + hi) / 2
            if gap(mid) > 0: lo = mid
            else: hi = mid
        phi = (lo + hi) / 2
    return z0, pd, phi

def profile_fn(x0, y0, h, s_lo, s_hi, step=0.05):
    """vectorised ground profile g(s) along the heading from (x0, y0): sampled once from the world heightfield, then interpolated"""
    ss = np.arange(s_lo, s_hi + step, step); Z = F.ground_h(x0 + h[0] * ss, y0 + h[1] * ss); return lambda s: np.interp(s, ss, Z)

def pose_on_ground(H, x, y, yaw_deg, **kw):
    """rest the tank (bottom-run front end at world x,y, heading yaw) on the world heightfield along its heading; returns the pose and applies it"""
    h = (math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg)))
    g = profile_fn(x, y, h, -30, 12)
    z0, pd, phi = solve_pose(g, 0.0, **kw); apply_pose(H, (x, y, z0), yaw_deg, pd, 0.0, phi); return z0, pd, phi

def apply_pose(H, pos, yaw, pitch, roll=0.0, tail_phi=None, frame=None):
    r = H.root; r.location = pos; r.rotation_euler = (math.radians(roll), -math.radians(pitch), math.radians(yaw))
    if tail_phi is not None and 'tail' in H: H.tail.rotation_euler = (0, -math.radians(tail_phi), 0)
    if frame is not None:
        r.keyframe_insert('location', frame=frame); r.keyframe_insert('rotation_euler', frame=frame)
        if tail_phi is not None and 'tail' in H: H.tail.keyframe_insert('rotation_euler', frame=frame)

def setup_crossing(H, origin_xy, yaw_deg, s_a, s_b, n=160, speed=None, g=None, prefer=None, smooth=6):
    """crossing path: the tank origin runs from s_a to s_b along the heading from origin_xy.  `speed(u)` maps u 0..1 to progress 0..1 (default: slow in the middle, where it lifts and grips).
    Builds a pose table (smoothed pitch, contact-exact heights) used by set_crossing."""
    h = (math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))); x0, y0 = origin_xy
    g = g or profile_fn(x0, y0, h, s_a - 30, s_b + 12)
    speed = speed or (lambda u: u - 0.12 * math.sin(2 * math.pi * u) / (2 * math.pi) * 2.0)
    prefer = prefer or (lambda pd: 0.7 * max(0.0, 2.0 - pd) + 0.012 * max(0.0, 10.0 - pd))          # no nose-dips: the nose stays up while it reaches over the gap
    us = np.linspace(0, 1, n); ss = np.array([s_a + (s_b - s_a) * min(1, max(0, speed(u))) for u in us]); pit = []; phis = []
    for s in ss: z0, pd, ph = solve_pose(g, s, prefer=prefer); pit.append(pd)
    pit = np.array(pit); k = np.exp(-0.5 * (np.arange(-3 * smooth, 3 * smooth + 1) / smooth) ** 2); k /= k.sum(); pad = np.pad(pit, (3 * smooth, 3 * smooth), mode='edge'); pit_s = np.convolve(pad, k, 'valid')
    if _OUT is None: outline_pts()
    rows = []
    for s, pd in zip(ss, pit_s):
        th = math.radians(pd); xs = _OUT[:, 0] * math.cos(th) - _OUT[:, 1] * math.sin(th); zs = _OUT[:, 0] * math.sin(th) + _OUT[:, 1] * math.cos(th)
        z0 = float(np.max(g(s + xs) - zs))
        def gap(ph):
            cx, cz = tail_geom(ph); x, z = rot2(cx, cz, th); return z0 + z - TAIL_R - float(g(s + x))
        lo, hi = -40.0, 40.0
        for _ in range(26):
            mid = (lo + hi) / 2
            if gap(mid) > 0: lo = mid
            else: hi = mid
        rows.append((s, z0, pd, (lo + hi) / 2))
    H.cross = dict(origin=origin_xy, yaw=yaw_deg, h=h, us=us, rows=np.array(rows), s_a=s_a, s_b=s_b, g=g)
    return H.cross

def crossing_pose(H, u):
    c = H.cross; rows = c['rows']; k = np.interp(u, c['us'], np.arange(len(rows))); i = int(min(len(rows) - 2, math.floor(k))); f = k - i; r = rows[i] * (1 - f) + rows[i + 1] * f
    s, z0, pd, ph = r; x = c['origin'][0] + c['h'][0] * s; y = c['origin'][1] + c['h'][1] * s; return dict(s=s, pos=(x, y, z0), pitch=pd, phi=ph)

def set_crossing(H, u, frame=None):
    """pose the tank for crossing progress u 0..1: approach, nose lifts over the trench, front horn grips the far lip, pulls across, levels on the far side. Also scrolls the tracks."""
    p = crossing_pose(H, u); apply_pose(H, p['pos'], H.cross['yaw'], p['pitch'], 0.0, p['phi'], frame); set_drive(H, p['s'] - H.cross['s_a'], frame)
    return p

# ----------------------------------------------------------------------------- states
def set_state(H, state, level=1.0, frame=None):
    """'stuck': sunk to the sponsons (root down by 1.15 D, pitch -3, roll 2.5 at level 1, ground mesh hides the lower hull); 'smoking': engine smoke column level; 'normal': reset the sink."""
    b = H.base
    if state == 'stuck':
        e = ease(level); r = H.root; r.location = (b['pos'][0], b['pos'][1], b['pos'][2] - 1.15 * e); r.rotation_euler = (math.radians(b['roll'] + 2.5 * e), -math.radians(b['pitch'] - 3.0 * e), math.radians(b['yaw']))
        if frame is not None: r.keyframe_insert('location', frame=frame); r.keyframe_insert('rotation_euler', frame=frame)
    elif state == 'smoking':
        import kit as K
        if H.smoke is None:
            K.use(S['coll']); sm = K.smoke_column((0, 0, 0), H=16.0, r0=0.9, wind=(-5.0, 3.0), parent=H.root, name=H.name + '_smoke', a=0.4, b=1.6, dens=2.0, nscale=0.45); sm.location = (-5.4, -0.85, 5.3); H.smoke = sm
        K.set_level(H.smoke, level, frame)
    elif state == 'normal':
        apply_pose(H, b['pos'], b['yaw'], b['pitch'], b['roll'], None, frame)
    H.state[state] = level

def set_sparks(H, t, frame=None):
    """bullet pings on the hull plates (bloodless): t seconds since the burst; t < 0 = none.  Each of the 16 spots flashes for 0.16 s, staggered 0.045 s."""
    for (ob, i, c) in H.sparks:
        tt = t - i * 0.045; on = 0.0 <= tt < 0.16; sc = (0.5 + 2.0 * tt / 0.16) if on else 0.01
        _vis(ob, on, frame); ob.scale = (sc, sc, sc); ob.location = tuple(c * (1.0 - sc)) if on else (0, 0, 0)
        if frame is not None: ob.keyframe_insert('scale', frame=frame); ob.keyframe_insert('location', frame=frame)

def tank_point(H, p):
    return H.root.matrix_world @ Vector(p)
