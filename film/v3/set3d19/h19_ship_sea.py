"""h19_ship_sea.py : the sea of film 19 (smooth layered swells, lacy hull foam, V-wake, glitter path, haze) in METRES.
Frame: the ship sits at the origin heading +y (see h19_ship_hull).  The sea is ONE camera-fitted grid (vertex per ~pixel) whose heights are computed by a
geometry-nodes group from the world xy and the sea time (hook set_sea), foam is a mix of baked per-vertex fields (hull lines, wake, bow ring, rocks, shore)
and shader lace.  Grown from styleboard part_ship6.build_sea6 (approved v6 look) + film 10 swell group."""
import os, sys, math
import numpy as np
import bpy
from mathutils import Vector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h19_kit as K
from h19_kit import hexc
import h19_ship_hull as HU
from h19_ship_hull import ss, vnoise2, fbm2, w_wl, YS, YB

SC = K.SC
PH = math.radians(180.0 - 33.0)                      # v6 hero: ship yaw in the old world
V6C = (7.5, 67.0)
def v6_pos(p):
    """old v6 world (metres) -> ship frame"""
    dx, dy = p[0] - V6C[0], p[1] - V6C[1]
    return (dx * math.cos(PH) + dy * math.sin(PH), -dx * math.sin(PH) + dy * math.cos(PH), p[2] if len(p) > 2 else 0.0)
def v6_dir(v):
    return (v[0] * math.cos(PH) + v[1] * math.sin(PH), -v[0] * math.sin(PH) + v[1] * math.cos(PH), v[2] if len(v) > 2 else 0.0)

# ----------------------------------------------------------------------------- swells (same RNG order as the approved v6 sea, rotated into the ship frame)
def wave_tables():
    rng = np.random.RandomState(3); sw = []; ch = []
    for (L, A, deg) in [(52, 0.85, 80), (31, 0.55, 112), (19, 0.34, 70)]:
        a = math.radians(deg + rng.uniform(-8, 8)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28)
        kx, ky = k * math.cos(a), k * math.sin(a)
        kxl = kx * math.cos(PH) + ky * math.sin(PH); kyl = -kx * math.sin(PH) + ky * math.cos(PH); phl = ph + kx * V6C[0] + ky * V6C[1]
        sw.append(dict(kx=kxl, ky=kyl, ph=phl, A=A, L=L, w=math.sqrt(9.81 * k)))
    for (L, A) in [(7.4, .10), (4.8, .06), (3.1, .04), (2.0, .026), (1.3, .016)]:
        a = math.radians(80 + rng.uniform(-50, 50)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28)
        kx, ky = k * math.cos(a), k * math.sin(a)
        kxl = kx * math.cos(PH) + ky * math.sin(PH); kyl = -kx * math.sin(PH) + ky * math.cos(PH); phl = ph + kx * V6C[0] + ky * V6C[1]
        ch.append(dict(kx=kxl, ky=kyl, ph=phl, A=A, L=L, w=math.sqrt(9.81 * k)))
    return sw, ch
SW, CH = wave_tables()

def swell_h(px, py, t=0.0, amp=1.0):
    h = np.zeros_like(np.asarray(px, dtype=np.float64))
    for w in SW:
        q = 0.5 + 0.5 * np.sin(w['kx'] * px + w['ky'] * py + w['ph'] - w['w'] * t); h = h + amp * w['A'] * (2 * q ** 1.5 - 1.0)
    return h
def swell_grad(px, py, t=0.0, amp=1.0, e=0.5):
    hx = (swell_h(px + e, py, t, amp) - swell_h(px - e, py, t, amp)) / (2 * e); hy = (swell_h(px, py + e, t, amp) - swell_h(px, py - e, t, amp)) / (2 * e)
    return hx, hy

# ----------------------------------------------------------------------------- node helpers
def _nm(nt, op, a=None, b=None, c=None, clamp=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    for i, v in enumerate((a, b, c)):
        if v is None: continue
        if hasattr(v, 'node'): nt.links.new(v, n.inputs[i])
        else: n.inputs[i].default_value = v
    return n.outputs[0]

def swell_group(SP, camloc):
    """GN group: z += swells + faded chop of world xy and the sea time (Value node 'sea_t', keyed by set_sea) + baked 'hump' attribute.  Smooth shaded."""
    ng = bpy.data.node_groups.new('H19_swell', 'GeometryNodeTree')
    ng.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry'); ng.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
    N = ng.nodes.new; L = ng.links.new; gi = N('NodeGroupInput'); go = N('NodeGroupOutput')
    pos = N('GeometryNodeInputPosition'); sp = N('ShaderNodeSeparateXYZ'); L(pos.outputs[0], sp.inputs[0])
    tv = N('ShaderNodeValue'); tv.name = 'sea_t'; tv.label = 'sea_t'; tv.outputs[0].default_value = 0.0
    amp = SP.get('amp', 1.0); chk = SP.get('chop', 1.0)
    # distance to the camera (for the chop fade): the grid is fitted to the camera so chop that the pixel grid cannot resolve fades out
    cb = N('ShaderNodeCombineXYZ'); cb.inputs[0].default_value = camloc[0]; cb.inputs[1].default_value = camloc[1]; cb.inputs[2].default_value = camloc[2]
    dd = N('ShaderNodeVectorMath'); dd.operation = 'DISTANCE'; L(pos.outputs[0], dd.inputs[0]); L(cb.outputs[0], dd.inputs[1])
    dist = dd.outputs['Value']
    tot = None
    def addto(tot, v):
        return v if tot is None else _nm(ng, 'ADD', tot, v)
    for w in SW:
        a = _nm(ng, 'MULTIPLY', sp.outputs['X'], w['kx']); b = _nm(ng, 'MULTIPLY_ADD', sp.outputs['Y'], w['ky'], a)
        c = _nm(ng, 'MULTIPLY_ADD', tv.outputs[0], -w['w'], b); c = _nm(ng, 'ADD', c, w['ph']); s = _nm(ng, 'SINE', c)
        q = _nm(ng, 'MULTIPLY_ADD', s, 0.5, 0.5); qp = _nm(ng, 'POWER', q, 1.5); h = _nm(ng, 'MULTIPLY_ADD', qp, 2.0 * w['A'] * amp, -w['A'] * amp)
        tot = addto(tot, h)
    fpxk = (2 * 0.4602 * 1.15 / 720.0) * 1.1 / 1.12
    for w in CH:
        a = _nm(ng, 'MULTIPLY', sp.outputs['X'], w['kx']); b = _nm(ng, 'MULTIPLY_ADD', sp.outputs['Y'], w['ky'], a)
        c = _nm(ng, 'MULTIPLY_ADD', tv.outputs[0], -w['w'], b); c = _nm(ng, 'ADD', c, w['ph']); s = _nm(ng, 'SINE', c)
        fpx = _nm(ng, 'MAXIMUM', _nm(ng, 'MULTIPLY', dist, fpxk), 1e-4)
        f1 = _nm(ng, 'DIVIDE', w['L'], fpx); f2 = _nm(ng, 'MULTIPLY', _nm(ng, 'SUBTRACT', f1, 4.0), 1.0 / 7.0, clamp=True)
        f3 = _nm(ng, 'MULTIPLY_ADD', dist, -1.0 / 260.0, 1.0, clamp=True); fd = _nm(ng, 'MULTIPLY', f2, f3)
        h = _nm(ng, 'MULTIPLY', _nm(ng, 'MULTIPLY', s, w['A'] * chk), fd)
        tot = addto(tot, h)
    far = _nm(ng, 'POWER', _nm(ng, 'MULTIPLY_ADD', dist, -1.0 / 3500.0, 1.0, clamp=True), 0.5); tot = _nm(ng, 'MULTIPLY', tot, far)
    hp = N('GeometryNodeInputNamedAttribute'); hp.data_type = 'FLOAT'; hp.inputs['Name'].default_value = 'hump'
    tot = _nm(ng, 'ADD', tot, hp.outputs['Attribute'])
    cz = N('ShaderNodeCombineXYZ'); L(tot, cz.inputs['Z'])
    setp = N('GeometryNodeSetPosition'); L(gi.outputs[0], setp.inputs['Geometry']); L(cz.outputs[0], setp.inputs['Offset'])
    sm = N('GeometryNodeSetShadeSmooth'); L(setp.outputs[0], sm.inputs['Geometry']); L(sm.outputs[0], go.inputs[0])
    return ng, tv

# ----------------------------------------------------------------------------- foam fields (ship frame, metres)
def pulse(d, w):
    e = np.clip(1 - np.abs(d) / w, 0, 1); return e * e * (3 - 2 * e)

def foam_fields(px, py, SP):
    """smooth foam ENVELOPES (the lace is made in the shader): fenv (0..1: where lacy foam may grow), fcore (solid foam), hump (baked small bow hump), shal (shore shallows)"""
    ly = py; lx = px; ax = np.abs(lx)
    tt = np.clip((ly - YS) / (YB - YS), 0, 1); bw = w_wl(tt)
    dh = np.where(ly >= YB, np.hypot(lx, ly - YB), ax - bw)
    dback = np.maximum(YS - ly, 0.0)
    sk = SP.get('foam_k', 1.0)
    env = np.zeros_like(px); core = np.zeros_like(px); hump = np.zeros_like(px)
    if SP.get('ship_foam', True):
        anch = SP.get('anchored')
        hump = 0.38 * np.exp(-((np.maximum(dh, 0) - 1.6) / 2.4) ** 2) * ss(YB - 16.0, YB - 2.0, ly) * ss(YB + 5.0, YB, ly) * (dh > -1.0) * (0.0 if anch else 1.0)
        sideok = ss(YS - 3.5, YS + 1.0, ly) * ss(YB + 8.0, YB + 2.0, ly)
        along = lambda sd: 0.50 + 0.50 * fbm2(ly / 11.0 + sd, ax / 6.0 + 0.3 * sd, 4 + sd, 3)
        if not anch:
            hl = np.zeros_like(px)
            for (off, wd, amp_, sd) in ((1.5, 0.55, 1.0, 4), (4.0, 0.8, 0.95, 14), (7.2, 1.1, 0.85, 24), (11.0, 1.4, 0.7, 34), (15.5, 1.7, 0.5, 44)):
                wob = 0.35 * np.sin(ly * 0.21 + off) + 0.5 * (fbm2(ly / 6.5 + sd, 1.0, 9 + sd, 2) - 0.5)
                hl = np.maximum(hl, pulse(dh - off - wob, wd) * amp_ * np.clip(along(sd) * 1.35 - 0.1, 0, 1))
            hl *= sideok * np.clip(1 - dback / 9.0, 0, 1) ** 0.5 * ss(-0.6, 0.5, dh)
            lap = pulse(dh - 0.35, 0.55) * sideok * np.clip(along(7) * 1.4, 0, 1) * (ly > YS)
            env = np.maximum(env, hl); core = np.maximum(core, lap * 0.8)
            bws = float(w_wl(0.0))
            wk = np.zeros_like(px)
            for (slope, wd0, wd1, amp_) in ((0.30, 1.7, 0.2, 1.0), (0.13, 1.5, 0.12, 0.9), (0.52, 2.0, 0.24, 0.85)):
                xarm = bws * 0.9 + slope * dback; wd = wd0 + wd1 * dback
                m_ = np.clip(0.8 + 0.7 * (fbm2(dback / 14.0 + slope * 9, ax / 9.0, 20 + int(slope * 10), 3) - 0.5) + 0.3, 0, 1)
                wk = np.maximum(wk, pulse(ax - xarm, wd) * amp_ * m_ * np.exp(-dback / 150.0))
            cr = np.exp(-(lx / (bws * 0.95 + 0.07 * dback)) ** 2) * np.exp(-dback / 42.0)
            wk = np.maximum(wk, cr * 0.95)
            wk *= (ly < YS + 3.0) * ss(YS + 3.0, YS - 1.0, ly)
            env = np.maximum(env, wk); core = np.maximum(core, np.exp(-dback / 12.0) * np.exp(-(lx / (bws * 0.6 + 0.04 * dback)) ** 2) * (ly < YS + 1.5) * 0.7)
            ringenv = ss(0.0, 1.4, dh) * (1 - ss(3.2, 6.0, dh)) * ss(YB - 15.0, YB - 2.0, ly) * ss(YB + 7.0, YB + 1.0, ly)
            env = np.maximum(env, ringenv * 0.95)
            skirt = (1 - ss(2.6, 4.2, dh)) * ss(-0.3, 0.2, dh) * ss(YB - 15.0, YB - 3.0, ly) * ss(YB + 7.0, YB + 1.0, ly)
            core = np.maximum(core, skirt * 0.55)
        else:
            lap = pulse(dh - 0.5, 0.6) * (ly > YS) * (ly < YB + 1.0) * np.clip(along(3) * 1.3, 0, 1)
            env = np.maximum(env, lap * 0.55); core = np.maximum(core, lap * 0.35)
        env = env * sk; core = core * sk
    for (cx, cy, r, h) in SP.get('rocks', []):
        d = np.hypot(px - cx, py - cy) - r
        e = pulse(d - 1.2, 3.6) * (0.75 + 0.35 * fbm2(px / 4.0 + cx, py / 4.0, 71, 3))
        env = np.maximum(env, np.clip(e, 0, 1) * 1.0); core = np.maximum(core, np.clip(1 - np.maximum(d, 0) / 1.4, 0, 1) * (d > -0.8) * 0.85)
    for (a, b, wd, amp_) in SP.get('streaks', []):                       # broken foam lines (a swell crest's foam, the water round a floating spar): segment a-b (ship frame, m)
        dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy; ln = math.sqrt(L2)
        t = np.clip(((px - a[0]) * dx + (py - a[1]) * dy) / L2, 0, 1); d = np.hypot(px - (a[0] + t * dx), py - (a[1] + t * dy))
        brk = np.clip(0.35 + 1.5 * (fbm2(t * ln / 4.5 + a[0] * 0.1, 3.0 + a[1] * 0.1, 61, 3) - 0.4), 0, 1)
        e = pulse(d, wd) * amp_ * brk * ss(0.0, 0.08, t) * ss(1.0, 0.92, t)
        env = np.maximum(env, e); core = np.maximum(core, np.clip(e - 0.25, 0, 1) * 0.6)
    shal = np.zeros_like(px); sf = SP.get('shore')
    if sf is not None:
        sd = sf(px, py)
        shal = np.exp(-np.maximum(sd, 0) / SP.get('shal_w', 60.0))
        env = np.maximum(env, pulse(sd - 2.5, 4.0) * 0.85 * ss(-3.0, 1.0, sd))
        core = np.maximum(core, pulse(sd - 0.4, 0.9) * 0.8)
        for kk in range(3):
            line = pulse(sd - (10.0 + 11.0 * kk + 3.0 * np.sin(py * 0.05 + kk)), 1.6) * np.exp(-kk * 0.45) * np.clip(0.4 + 1.2 * fbm2(py / 14.0 + kk * 7, 1.0, 95 + kk, 3), 0, 1)
            env = np.maximum(env, line * 0.8)
    return dict(fenv=np.nan_to_num(np.clip(env, 0, 1)), fcore=np.nan_to_num(np.clip(core, 0, 1)), hump=hump, shal=shal)

# ----------------------------------------------------------------------------- the grid
def fit_grid(cam_loc, cam_look, NU, NV):
    loc = np.array(cam_loc, dtype=np.float64); look = np.array(cam_look, dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.15, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy) if u[2] * hy > 1e-6 else 1.3
    vmax = min(vmax, 1.6); vmin = -1.35
    uu = np.linspace(-1.12, 1.12, NU); vv = vmin + (vmax - vmin) * (np.linspace(0, 1, NV) ** 1.0)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    rz = np.where(ray[..., 2] < -1e-5, ray[..., 2], -1e-5)
    t = -loc[2] / rz; t = np.minimum(t, 7000.0)
    px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    return px, py, t

def polar_grid(c, a0, a1, r0, r1, NU, NV):
    """a fan of rays from the point c (ship frame, m): angles a0..a1 (rad), radii r0..r1 spaced geometrically.  Used where the
    camera travels far (the coast BIGZOOM from high above the bay down to the beach): a camera-fitted grid only covers one view."""
    aa = np.linspace(a0, a1, NU); rr = r0 * (r1 / r0) ** np.linspace(0.0, 1.0, NV)
    A_, R_ = np.meshgrid(aa, rr)
    return c[0] + R_ * np.cos(A_), c[1] + R_ * np.sin(A_), R_

def build_sea(SP, parent):
    c = SP['cam']; cam_loc = np.array(c['loc'], dtype=np.float64)
    NU, NV = SP.get('sea_nu', 560), SP.get('sea_nv', 820)
    if SP.get('polar'):
        pg = SP['polar']; px, py, t = polar_grid(pg['c'], pg['a0'], pg['a1'], pg['r0'], pg['r1'], NU, NV)
    else:
        px, py, t = fit_grid(c['loc'], c['look'], NU, NV)
    F = foam_fields(px, py, SP)
    verts = np.stack([px, py, np.zeros_like(px)], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    a_ = idx[:-1, :-1]; b_ = idx[:-1, 1:]; c_ = idx[1:, 1:]; d_ = idx[1:, :-1]
    alt = ((np.arange(NU - 1)[None, :] + np.arange(NV - 1)[:, None]) % 2).astype(bool)
    t1 = np.where(alt[..., None], np.stack([a_, b_, c_], -1), np.stack([a_, b_, d_], -1)); t2 = np.where(alt[..., None], np.stack([a_, c_, d_], -1), np.stack([b_, c_, d_], -1))
    tris = np.concatenate([t1.reshape(-1, 3), t2.reshape(-1, 3)])
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nt_ = len(tris); me.loops.add(nt_ * 3); me.polygons.add(nt_)
    me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nt_) * 3).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nt_, 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nt_, dtype=bool))
    for nm in ('fenv', 'fcore', 'hump', 'shal'):
        at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', F[nm].reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob); ob.parent = parent
    ng, tv = swell_group(SP, cam_loc)
    md = ob.modifiers.new('swell', 'NODES'); md.node_group = ng
    m, tsock = sea_material(SP)
    ob.data.materials.append(m)
    # glossy-only virtual sun (light-linked to the sea): the sharp glitter lobe lands under it
    coll = bpy.data.collections.new('seacoll'); bpy.context.scene.collection.children.link(coll); coll.objects.link(ob)
    gk = SP['glint']
    kd = Vector(gk['dir']).normalized(); d = bpy.data.lights.new('glint', 'SUN'); d.color = (1.0, 0.86, 0.62); d.energy = gk['k']; d.angle = math.radians(gk['ang'])
    o = bpy.data.objects.new('glint', d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    o.visible_diffuse = False; o.light_linking.receiver_collection = coll
    return dict(ob=ob, tsocks=[tv.outputs[0], tsock], glint=o, ng=ng)

# ----------------------------------------------------------------------------- the sea material
def sea_material(SP):
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.name = 'bsdf'
    bs.inputs['Roughness'].default_value = SP.get('rough', 0.1); bs.inputs['IOR'].default_value = 1.33
    cd = N('ShaderNodeCameraData'); dm = _nm(nt, 'DIVIDE', cd.outputs['View Distance'], SC)          # view distance in metres
    def mixc(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        if hasattr(fac, 'node'): L(fac, mx.inputs[0])
        else: mx.inputs[0].default_value = fac
        return mx.outputs[2]
    def mrange(val, a, b, lo=0.0, hi=1.0, clamp=True):
        mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = a; mr.inputs['From Max'].default_value = b; mr.inputs['To Min'].default_value = lo; mr.inputs['To Max'].default_value = hi
        mr.clamp = clamp; L(val, mr.inputs['Value']); return mr.outputs['Result']
    L(mrange(dm, 20.0, 120.0, SP.get('spec_near', 0.12), SP.get('spec_far', 0.5)), bs.inputs['Specular IOR Level'])
    # colour layers: deep teal near -> teal mid -> deep navy far -> haze at the horizon
    col = mixc(hexc(SP['sea_near']), hexc(SP.get('sea_mid', SP['sea_near'])), mrange(dm, 12.0, 90.0))
    col = mixc(col, hexc(SP['sea_far']), mrange(dm, 70.0, 260.0))
    shl = N('ShaderNodeAttribute'); shl.attribute_type = 'GEOMETRY'; shl.attribute_name = 'shal'
    if SP.get('shore'):
        col = mixc(col, hexc(SP.get('sea_shal', '#38b3a6')), _nm(nt, 'MULTIPLY', _nm(nt, 'POWER', shl.outputs['Fac'], 1.6, clamp=True), SP.get('shal_k', 0.9), clamp=True))
    tcw = N('ShaderNodeTexCoord'); spz = N('ShaderNodeSeparateXYZ'); L(tcw.outputs['Object'], spz.inputs[0])
    # ---- foam: envelope (baked fenv + crest whitecap env) -> lace (web + noise) with the pattern drifting aft with the sea time; fcore = solid
    tv = N('ShaderNodeValue'); tv.name = 'sea_t'; tv.label = 'sea_t'; tv.outputs[0].default_value = 0.0
    fa = N('ShaderNodeAttribute'); fa.attribute_type = 'GEOMETRY'; fa.attribute_name = 'fenv'
    fc = N('ShaderNodeAttribute'); fc.attribute_type = 'GEOMETRY'; fc.attribute_name = 'fcore'
    wmin, wmax = SP.get('wc_min', 0.74), SP.get('wc_max', 1.05)
    mpw = N('ShaderNodeMapping'); mpw.inputs['Scale'].default_value = (0.55, 0.40, 1.0); L(tcw.outputs['Object'], mpw.inputs['Vector'])
    nzw = N('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 1.0; nzw.inputs['Detail'].default_value = 2.0; L(mpw.outputs[0], nzw.inputs['Vector'])
    wcz = mrange(spz.outputs['Z'], wmin, wmax)
    wcn = mrange(nzw.outputs['Fac'], 0.38, 0.66, 0.0, 1.0)
    wc = _nm(nt, 'MULTIPLY', wcz, wcn, clamp=True)                                   # whitecap envelope (crest height x spotty noise)
    env = _nm(nt, 'MAXIMUM', fa.outputs['Fac'], _nm(nt, 'MULTIPLY', wc, SP.get('wc_k', 0.85)))
    sx = N('ShaderNodeSeparateXYZ'); L(tcw.outputs['Object'], sx.inputs[0])
    dy = _nm(nt, 'MULTIPLY_ADD', tv.outputs[0], -SP.get('drift', 3.2), sx.outputs['Y'])
    cv = N('ShaderNodeCombineXYZ'); L(sx.outputs['X'], cv.inputs['X']); L(dy, cv.inputs['Y'])
    n1 = N('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 0.8; n1.inputs['Detail'].default_value = 4.0; n1.inputs['Roughness'].default_value = 0.6; L(cv.outputs[0], n1.inputs['Vector'])
    mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (4.0, 4.0, 4.0); mp2.inputs['Location'].default_value = (13.0, 7.0, 3.0); L(cv.outputs[0], mp2.inputs['Vector'])
    n2 = N('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 1.0; n2.inputs['Detail'].default_value = 2.0; L(mp2.outputs[0], n2.inputs['Vector'])
    # organic lace: thin curvy contour lines of domain-warped noise (no regular cells)
    wv = N('ShaderNodeTexNoise'); wv.inputs['Scale'].default_value = 0.9; wv.inputs['Detail'].default_value = 1.0; L(cv.outputs[0], wv.inputs['Vector'])
    wvec = N('ShaderNodeVectorMath'); wvec.operation = 'MULTIPLY_ADD'; wvec.inputs[1].default_value = (0.9, 0.9, 0.9); wvec.inputs[2].default_value = (0.0, 0.0, 0.0); L(cv.outputs[0], wvec.inputs[2]); L(wv.outputs['Color'], wvec.inputs[0])
    c1n = N('ShaderNodeTexNoise'); c1n.inputs['Scale'].default_value = SP.get('lace_scale', 1.5); c1n.inputs['Detail'].default_value = 2.0; c1n.inputs['Roughness'].default_value = 0.5; L(wvec.outputs[0], c1n.inputs['Vector'])
    web = _nm(nt, 'SUBTRACT', 1.0, mrange(_nm(nt, 'ABSOLUTE', _nm(nt, 'SUBTRACT', c1n.outputs['Fac'], 0.5)), 0.012, 0.06))
    c2n = N('ShaderNodeTexNoise'); c2n.inputs['Scale'].default_value = SP.get('lace_scale', 1.5) * 3.1; c2n.inputs['Detail'].default_value = 1.0; L(wvec.outputs[0], c2n.inputs['Vector'])
    web2 = _nm(nt, 'SUBTRACT', 1.0, mrange(_nm(nt, 'ABSOLUTE', _nm(nt, 'SUBTRACT', c2n.outputs['Fac'], 0.5)), 0.015, 0.075))
    wfade = mrange(dm, 70.0, 220.0, 1.0, 0.0)                                                     # lace only where a pixel can resolve it
    webc = _nm(nt, 'MULTIPLY', _nm(nt, 'MAXIMUM', web, _nm(nt, 'MULTIPLY', web2, 0.7)), wfade)
    pat = _nm(nt, 'ADD', _nm(nt, 'MULTIPLY', webc, 0.62), _nm(nt, 'ADD', _nm(nt, 'MULTIPLY', n1.outputs['Fac'], 0.5), _nm(nt, 'MULTIPLY', _nm(nt, 'SUBTRACT', n2.outputs['Fac'], 0.5), 0.3)))
    thr = _nm(nt, 'MULTIPLY_ADD', env, -SP.get('lace_gain', 1.0), SP.get('lace_off', 1.0))
    lace = mrange(_nm(nt, 'SUBTRACT', pat, thr), 0.0, 0.14)
    lace = _nm(nt, 'MULTIPLY', lace, mrange(env, 0.04, 0.2), clamp=True)
    fm = _nm(nt, 'MAXIMUM', lace, _nm(nt, 'MULTIPLY', fc.outputs['Fac'], mrange(n1.outputs['Fac'], 0.30, 0.55, 0.55, 1.0)), clamp=True)
    # horizon haze (also hides the far clip of the sea)
    hz = mrange(dm, SP.get('haze0', 380.0), SP.get('haze1', 900.0), 0.0, SP.get('haze_k', 0.85))
    col = mixc(col, hexc(SP.get('haze', '#b0cbe8')), hz)
    # the body colour is painted with emission (so the blue-violet ambient does not tint the water); a faint diffuse term keeps the facets lit; foam is lit white
    blk = hexc('#000000')
    base = mixc(mixc(col, blk, 0.80), hexc('#eef4f0'), fm)
    L(base, bs.inputs['Base Color'])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    fk = _nm(nt, 'MULTIPLY', mrange(dm, 20.0, 120.0, 0.12, 1.0), SP.get('fresnel_k', 0.38))
    em = _nm(nt, 'MULTIPLY', lw.outputs['Fresnel'], fk)
    ecol = mixc(col, hexc('#f4f8f2'), fm)
    e1 = N('ShaderNodeEmission'); L(ecol, e1.inputs['Color']); e1.inputs['Strength'].default_value = SP.get('body_k', 0.85)
    L(_nm(nt, 'MAXIMUM', _nm(nt, 'MULTIPLY', _nm(nt, 'SUBTRACT', 1.0, fm), SP.get('body_k', 0.85)), _nm(nt, 'MULTIPLY', fm, SP.get('foam_glow', 0.45))), e1.inputs['Strength'])
    e2 = N('ShaderNodeEmission'); e2.inputs['Color'].default_value = hexc(SP.get('lift', '#9fc2d8')); L(_nm(nt, 'MULTIPLY', em, _nm(nt, 'SUBTRACT', 1.0, fm)), e2.inputs['Strength'])
    ad1 = N('ShaderNodeAddShader'); L(bs.outputs[0], ad1.inputs[0]); L(e1.outputs[0], ad1.inputs[1])
    ad2 = N('ShaderNodeAddShader'); L(ad1.outputs[0], ad2.inputs[0]); L(e2.outputs[0], ad2.inputs[1])
    mpb = N('ShaderNodeMapping'); mpb.inputs['Scale'].default_value = (1.0, 1.0, 1.0); L(tcw.outputs['Object'], mpb.inputs['Vector'])
    nzb = N('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 0.9; nzb.inputs['Detail'].default_value = 0.0; L(mpb.outputs[0], nzb.inputs['Vector'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = SP.get('bump', 0.04); bp.inputs['Distance'].default_value = 0.2; L(nzb.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(ad2.outputs[0], out.inputs['Surface'])
    return m, tv.outputs[0]
