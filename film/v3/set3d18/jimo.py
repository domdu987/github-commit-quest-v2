#!/usr/bin/env python3
"""jimo.py : the PRODUCTION set of film 18 ("ไอ้เสมียนวัว", Tian Dan's fire oxen at Jimo, Qi vs Yan, 279 BC): a real 3D Blender set (bpy 5.3, Cycles CPU).
See API.md.  World: 1 unit = 1 D = one head, Z up; the Jimo wall runs along x at y = 0 (outer face y -5 at the base, inner face y +4); +y = toward / inside Jimo.

    import jimo as J
    A = J.build('jimo_in', 's01')              # location, preset (a shot name s01..s26 or a location default), light=None (NIGHT | DUSK | DAWN)
    cam = J.make_camera(A['cam'])              # or J.set_shot_camera('s01', frame_in_shot)
    J.set_holes(6.5, frame=1301); J.flicker(frame)

Locations: jimo_in (DUSK NIGHT), jimo_out (DUSK NIGHT DAWN), yan_camp (DUSK NIGHT), vista (DUSK DAWN).
CLI: python3 jimo.py stills [spec ...] | final [spec ...] | digest [spec] | contact"""
import os, sys, math, json, time, random, subprocess, shutil
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, ) + tuple(os.path.join(PROJ, 'v3', d) for d in ('set3d9', 'set3d8', 'set3d7', 'set3d6', 'set3d5', 'set3d4', 'set3d2')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import desert as D                                         # noqa: E402
import wall as W9                                          # noqa: E402
import jimo_tex as JX                                      # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
STATE = T.STATE
Frame = BK.Frame
OUT = os.path.join(HERE, 'board')
WORK = os.path.join(HERE, 'set_work')
def _rnd(s): return random.Random(s)
V = Vector
FIRE = (1.0, 0.50, 0.18); LAMP = (1.0, 0.62, 0.30)

# ----------------------------------------------------------------------------- dimensions (D)
WH = 16.0                                                   # wall height (walk level)
def yo(z): return -5.0 + 2.0 * z / WH                       # outer face y at height z (battered)
def yi(z): return 4.0 - 1.0 * z / WH                        # inner face y
WATER_Z = -2.2; MOAT = (-30.0, -9.5)
GATE_W = 3.6; GATE_H = 9.6
HOLE_W, HOLE_H = 3.4, 4.3                                   # a breach: wide enough for one ox card (3.2 D tall with horns)
HOLE_X = [-41.0 + 5.5 * k for k in range(6)] + [13.5 + 5.5 * k for k in range(6)]     # 12 breaches along the wall base, x -41 .. -13.5 and 13.5 .. 41
HEIGHT = dict(tiandan=3.0, general=3.4, soldier=3.2, townsfolk=3.0, child=2.0, envoy=3.0, ox=2.6, qi_soldier=3.2, party_crowd=3.2, sentry=3.2)
LOCS = dict(jimo_in=('NIGHT', 'DUSK'), jimo_out=('NIGHT', 'DUSK', 'DAWN'), yan_camp=('NIGHT', 'DUSK'), vista=('DUSK', 'DAWN'))
LEGACY = dict(wall='jimo_out', camp='yan_camp', holes='jimo_in')

# ----------------------------------------------------------------------------- light presets (shade hue 240-260 against warm fire / lantern light)
_B = dict(toon=1.0, key_desat=0.55, ink='#141a3e', night=True, form=(0.0, -0.05, 0.22), bloom_size=0.12, sun_angle=0.6, sky='NIGHT', sky_k=0.88, star_k=1.0,
          shade=(0.085, 0.105, 0.34), shade_tint=(0.085, 0.115, 0.38), shade_mix=0.72, lift=(0.010, 0.012, 0.040), grade_offset=(0.002, 0.003, 0.010), grade_saturation=1.14,
          lamps=1.0, air=('#6a5cb8', 0.28, 40.0, 420.0), beams=0.0, ground_k=1.0)
def _kdaz(az, el): return W9._kdaz(az, el)
LIGHTS = dict(
    NIGHT=dict(_B, key=(0.24, 0.42, 1.18), key_dir=G._kd((0.45, 0.89), 38), moon_az=58.0, moon_el=20.0, wall_tint=(0.07, 0.12, 0.46), wall_mix=0.92),
    DUSK=dict(_B, night=False, key_desat=0.15, key=(1.7, 0.95, 0.5), key_dir=_kdaz(250, 9), sun_az=250.0, sun_el=9.0, sun_angle=0.9, sky='DUSK', sky_k=0.88, star_k=0.0, ink='#2a1a2e',
              shade=(0.06, 0.10, 0.27), shade_tint=(0.06, 0.115, 0.32), shade_mix=0.78, lift=(0.010, 0.008, 0.026), grade_offset=(-0.004, -0.006, -0.002), grade_saturation=1.12,
              bloom_size=0.08, air=('#f0a070', 0.30, 30.0, 300.0), lamps=0.8, wall_tint=(0.07, 0.12, 0.38), wall_mix=0.9),
    DAWN=dict(_B, night=False, key_desat=0.15, key=(1.60, 1.00, 0.62), key_dir=_kdaz(80, 8), sun_az=80.0, sun_el=8.0, sun_angle=1.0, sky='DAWN', sky_k=0.8, star_k=0.0, ink='#2a1a2e',
              shade=(0.07, 0.12, 0.28), shade_tint=(0.07, 0.13, 0.33), shade_mix=0.78, lift=(0.010, 0.008, 0.024), grade_offset=(-0.004, -0.006, -0.010), grade_saturation=1.18,
              bloom_size=0.08, air=('#f4bca0', 0.30, 30.0, 300.0), lamps=0.6, wall_tint=(0.07, 0.12, 0.38), wall_mix=0.9),
)
SUN_AZ = {('jimo_in', 'DUSK'): 200.0, ('jimo_out', 'DUSK'): 255.0, ('yan_camp', 'DUSK'): 322.0, ('vista', 'DUSK'): 215.0, ('jimo_out', 'DAWN'): 75.0, ('vista', 'DAWN'): 330.0}
MOON_AZ_LOC = {'jimo_in': 80.0, 'jimo_out': 58.0, 'yan_camp': 74.0, 'vista': 58.0}
SKY_SUN = dict(NIGHT=(58.0, 20.0), DUSK=(35.0, 6.0), DAWN=(330.0, 8.0))      # sun / moon azimuth and elevation baked in the sky textures

# ----------------------------------------------------------------------------- the warm / cool split material (earth wall: OCHRE where fire-lit, blue moon-shade elsewhere)
WARM_COL = (1.0, 0.84, 0.62)
def mat_lit_warm(name, image, gain=1.0, shade_mul=1.0, form=None, kw=0.72):
    """mat_lit for big earth faces with a per-vertex `warm` weight (0 = moon / sky only, 1 = fire-lit; baked from the lamp positions by bake_warm()).
    Where warm -> 1: the blue ambient emission fades out, the key term keeps the art's full ochre (no desaturation) and a warm emission (art x fire colour) is added,
    so fire light on the wall reads ochre #b8874e.. #c07a3c instead of rose (blue ambient + orange light = magenta). Elsewhere it is the plain blue moon-shade material."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    P = STATE['P']; m = bpy.data.materials.new(name); nt = T._tree(m); L = nt.links.new; N = nt.nodes.new
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    kd = V(P['key_dir']).normalized(); geo = N('ShaderNodeNewGeometry')
    att = N('ShaderNodeAttribute'); att.attribute_type = 'GEOMETRY'; att.attribute_name = 'warm'
    wk = N('ShaderNodeMath'); wk.operation = 'MULTIPLY'; wk.use_clamp = True; wk.inputs[1].default_value = 1.0; L(att.outputs['Fac'], wk.inputs[0]); warm = wk.outputs[0]
    tex = N('ShaderNodeTexImage'); tex.image = T._img(image); art = tex.outputs['Color']
    bw = N('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
    # key colour term: art desaturated toward its luma by key_desat, un-desaturated where warm
    fd = N('ShaderNodeMath'); fd.operation = 'MULTIPLY_ADD'; fd.inputs[1].default_value = -0.9 * float(P.get('key_desat', 0.0)); fd.inputs[2].default_value = float(P.get('key_desat', 0.0)); L(warm, fd.inputs[0])
    kdm = N('ShaderNodeMix'); kdm.data_type = 'RGBA'; kdm.blend_type = 'MIX'; L(fd.outputs[0], kdm.inputs[0]); L(art, kdm.inputs[6]); L(bw.outputs[0], kdm.inputs[7])
    md = N('ShaderNodeVectorMath'); md.operation = 'SCALE'; md.inputs['Scale'].default_value = gain; L(kdm.outputs[2], md.inputs[0]); L(md.outputs['Vector'], dif.inputs['Color'])
    # blue ambient: art x SHADE (mixed toward the luma x tint), faded where warm
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0; ms.inputs[7].default_value = (*P['shade'], 1.0); L(art, ms.inputs[6])
    mm = float(P.get('wall_mix', P.get('shade_mix', 0.0)))
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 1.0 - mm; L(ms.outputs[2], sa.inputs[0])
    tb = N('ShaderNodeVectorMath'); tb.operation = 'SCALE'; tb.inputs[0].default_value = tuple(x * mm for x in P.get('wall_tint', P.get('shade_tint', (0, 0, 0)))); L(bw.outputs[0], tb.inputs['Scale'])
    sab = N('ShaderNodeVectorMath'); sab.operation = 'ADD'; L(sa.outputs['Vector'], sab.inputs[0]); L(tb.outputs['Vector'], sab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P.get('lift', (0, 0, 0))); L(sab.outputs['Vector'], lf.inputs[0]); amb = lf.outputs['Vector']
    if form and any(abs(x) > 1e-6 for x in form):
        fdd = N('ShaderNodeVectorMath'); fdd.operation = 'DOT_PRODUCT'; fdd.inputs[1].default_value = tuple(form); L(geo.outputs['True Normal'], fdd.inputs[0])
        fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fdd.outputs['Value'], fa.inputs[0])
        fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(amb, fs.inputs[0]); L(fa.outputs[0], fs.inputs['Scale']); amb = fs.outputs['Vector']
    fade = N('ShaderNodeMath'); fade.operation = 'MULTIPLY_ADD'; fade.inputs[1].default_value = -0.92; fade.inputs[2].default_value = 1.0; L(warm, fade.inputs[0])
    ab = N('ShaderNodeVectorMath'); ab.operation = 'SCALE'; L(amb, ab.inputs[0]); L(fade.outputs[0], ab.inputs['Scale'])
    # warm emission: art x fire colour x warm
    we = N('ShaderNodeVectorMath'); we.operation = 'MULTIPLY'; we.inputs[1].default_value = tuple(c * kw for c in WARM_COL); L(art, we.inputs[0])
    wf = N('ShaderNodeVectorMath'); wf.operation = 'SCALE'; L(we.outputs['Vector'], wf.inputs[0]); L(warm, wf.inputs['Scale'])
    tot = N('ShaderNodeVectorMath'); tot.operation = 'ADD'; L(ab.outputs['Vector'], tot.inputs[0]); L(wf.outputs['Vector'], tot.inputs[1])
    emi = N('ShaderNodeEmission'); emi.inputs['Strength'].default_value = 1.0; L(tot.outputs['Vector'], emi.inputs['Color'])
    add = N('ShaderNodeAddShader'); L(dif.outputs['BSDF'], add.inputs[0]); L(emi.outputs['Emission'], add.inputs[1]); L(add.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def warm_at(p):
    """Warm (fire-lit) weight 0..1 at world point p from the registered fire sources STATE['warm'] = [(pos, radius, strength)]."""
    w = 0.0
    for (c, r, k) in STATE.get('warm', ()):
        d = (p - c); d = math.sqrt(d.x * d.x + d.y * d.y + (d.z * 0.8) ** 2); w += k * math.exp(-(d / r) ** 2)
    return min(1.0, w)

def bake_warm(ob):
    """Write the per-vertex `warm` attribute (the wall objects must be subdivided about every 2 D for a smooth pool)."""
    me = ob.data; a = me.attributes.get('warm') or me.attributes.new('warm', 'FLOAT', 'POINT')
    mw = ob.matrix_world; a.data.foreach_set('value', [warm_at(mw @ v.co) for v in me.vertices])

# ----------------------------------------------------------------------------- mesh banks
class Banks:
    def __init__(s): s.b = {}; s.hull = {}; s.shadow = {}
    def __call__(s, name, hull=0.0, shadow=True):
        if name not in s.b: s.b[name] = MB(); s.hull[name] = hull; s.shadow[name] = shadow
        return s.b[name]
    def flush(s, SET):
        for n, mb in s.b.items():
            if mb.f: _obj(mb, n, SET, hull=s.hull[n], shadow=s.shadow[n])

def lamp(name, loc, energy, rgb=LAMP, r=0.25, shadow=False):
    return BK._light(name, tuple(loc), rgb, energy, radius=r, shadow=shadow)

def halo(mb, c, r, mat, vertical=True):
    """Camera-only glow disc (crossed cards) around a light."""
    BK._halo(mb, c, r, {'halo': mat})

def flat(mb, o, du, dv, mat, uv=None):
    mb.quad(o, du, dv, mat, uv or (0, 0, 1, 1))

def ellipsoid(mb, c, rx, ry, rz, mat, seg=14, rings=8, uvs=(1, 1), phi=(0.0, 2 * math.pi), th=(0.0, math.pi), rough=0.0, seed=0, fn=None):
    """Ellipsoid (semi-axes rx ry rz, along x/y/z) with UV u around z, v pole to pole; theta/phi ranges for partial shells; fn(p) -> point warp."""
    c = V(c); R = []; mb.pid += 1
    for k in range(rings + 1):
        t = th[0] + (th[1] - th[0]) * k / rings; row = []
        for i in range(seg + 1):
            ph = phi[0] + (phi[1] - phi[0]) * i / seg
            n = 1 + (rough * (vnoise(2 * math.sin(t) * math.cos(ph) + 3, 2 * math.sin(t) * math.sin(ph) + 2.2 * math.cos(t), int(seed)) - 0.5) * 2 if rough else 0.0)
            p = V((rx * n * math.sin(t) * math.cos(ph), ry * n * math.sin(t) * math.sin(ph), -rz * n * math.cos(t)))
            row.append(fn(c + p) if fn else c + p)
        R.append(row)
    for k in range(rings):
        for i in range(seg):
            mb.face([R[k][i], R[k][i + 1], R[k + 1][i + 1], R[k + 1][i]], mat, [(uvs[0] * i / seg, uvs[1] * k / rings), (uvs[0] * (i + 1) / seg, uvs[1] * k / rings),
                                                                              (uvs[0] * (i + 1) / seg, uvs[1] * (k + 1) / rings), (uvs[0] * i / seg, uvs[1] * (k + 1) / rings)])

def cyl(mb, c, r, h, mat, seg=10, r1=None, cap=True):
    mb.frustum(V(c), V(c) + V((0, 0, h)), r, r if r1 is None else r1, mat, seg=seg, cap0=cap, cap1=cap)

def prism(mb, x0, x1, z0, z1, mo, mi, mt, mb_=None, ends=True, uvk=1.0 / 8):
    """Wedge wall segment between x0..x1 and heights z0..z1: outer face yo(z), inner face yi(z), top, bottom, end caps. Normals outward."""
    po = [V((x0, yo(z0), z0)), V((x1, yo(z0), z0)), V((x1, yo(z1), z1)), V((x0, yo(z1), z1))]
    pi_ = [V((x0, yi(z0), z0)), V((x1, yi(z0), z0)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))]
    L = math.hypot(z1 - z0, yo(z1) - yo(z0)); a = (x1 - x0)
    mb.oface(po, mo, [(x0 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0 + L / 4.0), (x0 * uvk, z0 / 4.0 + L / 4.0)], (0, -1, 0.12))
    mb.oface(pi_, mi, [(x0 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0), (x1 * uvk, z0 / 4.0 + L / 4.0), (x0 * uvk, z0 / 4.0 + L / 4.0)], (0, 1, 0.06))
    mb.oface([V((x0, yo(z1), z1)), V((x1, yo(z1), z1)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))], mt, [(x0 / 8, 0), (x1 / 8, 0), (x1 / 8, 0.7), (x0 / 8, 0.7)], (0, 0, 1))
    if z0 > 0: mb.oface([V((x0, yo(z0), z0)), V((x1, yo(z0), z0)), V((x1, yi(z0), z0)), V((x0, yi(z0), z0))], mi, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, -1))
    if ends:
        for xe, nx in ((x0, -1), (x1, 1)):
            mb.oface([V((xe, yo(z0), z0)), V((xe, yi(z0), z0)), V((xe, yi(z1), z1)), V((xe, yo(z1), z1))], mi, [(0, z0 / 4.0), (0.9, z0 / 4.0), (0.9, z1 / 4.0), (0, z1 / 4.0)], (nx, 0, 0))

# ----------------------------------------------------------------------------- hip roof with upturned eaves
def hip_roof(mb, o, yaw, A, Bh, r, z0, rise, M, lift=1.1, nx=28, ny=18, thick=0.4, tile=4.0, mat=None, under=None, edge=None, horns=False, wadang=True):
    """Chinese hip roof: plan half sizes A x Bh around o (yaw deg), ridge half length r along local x, eave level z0, ridge z0 + rise,
    concave slopes and corners curled up by `lift`. Tile surface, underside board and a fascia edge."""
    F = Frame(o, yaw); mat = mat or M['tiles']; under = under or M['wood_d']; edge = edge or M['red']
    def hz(x, y):
        u = max(abs(y) / Bh, max(abs(x) - r, 0.0) / max(A - r, 1e-3)); u = min(u, 1.0)
        c = (abs(x) / A) * (abs(y) / Bh); return z0 + rise * (1 - u) ** 1.7 + lift * max(0.0, (u - 0.72) / 0.28) ** 2 * c ** 1.3, u
    xs = [A * (-1 + 2 * i / nx) for i in range(nx + 1)]; ys = [Bh * (-1 + 2 * j / ny) for j in range(ny + 1)]
    Pt = [[None] * (ny + 1) for _ in range(nx + 1)]; Uu = [[0] * (ny + 1) for _ in range(nx + 1)]
    for i, x in enumerate(xs):
        for j, y in enumerate(ys): z, u = hz(x, y); Pt[i][j] = F.p(x, y, z); Uu[i][j] = u
    Ls = math.hypot(rise, Bh)
    for i in range(nx):
        for j in range(ny):
            q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]; pts = [Pt[a][b] for a, b in q]
            uv = [(xs[a] / tile, Uu[a][b] * Ls / tile) for a, b in q]
            mb.oface(pts, mat, uv, (0, 0, 1))
            mb.oface([p - V((0, 0, thick * 0.9)) for p in pts], under, [(xs[a] / 4, ys[b] / 4) for a, b in q], (0, 0, -1))
    for (a, b), (a2, b2) in [(((i, 0), (i + 1, 0))) for i in range(nx)] + [(((i, ny), (i + 1, ny))) for i in range(nx)] + [(((0, j), (0, j + 1))) for j in range(ny)] + [(((nx, j), (nx, j + 1))) for j in range(ny)]:
        p0, p1 = Pt[a][b], Pt[a2][b2]; n = (p0 + p1) / 2 - F.p(0, 0, p0.z)
        mb.oface([p0, p1, p1 - V((0, 0, thick * 0.9)), p0 - V((0, 0, thick * 0.9))], edge, [(0, 0), (1, 0), (1, 1), (0, 1)], (n.x, n.y, 0))
    if r > 0.3:                                                                                           # plain ridge (no curled horns: Warring States)
        rz = z0 + rise
        rod(mb, F.p(-r, 0, rz + 0.1), F.p(r, 0, rz + 0.1), 0.38, M['tiles_d_c'], seg=8)
        if horns:
            for sx in (-1, 1): rod(mb, F.p(sx * r, 0, rz + 0.1), F.p(sx * (r + 0.4), 0, rz + 0.8), 0.28, M['tiles_d_c'], seg=6, r1=0.12)
    if wadang:                                                                                            # half-round eaves tiles (wadang) along the long eaves
        for jj in (0, ny):
            for ii in range(1, nx, 2):
                p0 = Pt[ii][jj]; out = F.Y * (-1 if jj == 0 else 1)
                mb.frustum(p0 - V((0, 0, 0.1)) + out * 0.02, p0 - V((0, 0, 0.1)) + out * 0.16, 0.26, 0.26, M['stone'], seg=7)
    for sx in (-1, 1): hz_ = 0                                                                            # (corner finials)
    return F

def rafters(mb, o, yaw, A, Bh, z, M, step=1.3):
    F = Frame(o, yaw)
    for s_ in (-1, 1):
        for k in range(int(2 * A / step) + 1):
            x = -A + k * step
            if abs(x) <= A: obox(mb, F.p(x, s_ * (Bh - 0.5), z), F.X, F.Y, F.Z, 0.18, 0.36, 0.2, M['white'] if k % 2 else M['red'])

# ----------------------------------------------------------------------------- materials
def materials(P, tx, pre):
    FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, glow=None, glow_k=0.0):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s_%g' % (pre, name, gain, _k(sm), form, alpha, smix, glow_k), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                               alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    def WM(name, gain=1.0): return _untoon(mat_lit_warm('%swm_%s_%g' % (pre, name, gain), image=tx[name], gain=gain, shade_mul=1.0, form=FORM))
    def E(name, hexcol='#ffffff', k=1.0, image=None, alpha=False): return mat_emit(pre + 'e_' + name, hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    def ADD(name, image, rgb, k): return BK._mat_add(pre + 'a_' + name, tx[image], rgb, k)
    M = dict(rammed=WM('rammed', 1.25), rammed_d=WM('rammed_d', 1.15), earth=TX('earth', 0.9, form=False), vwater=C('#4a78b0', 1.0, 1.0, form=False), win_dim=E('win_dim', '#ff9a38', 0.55), fields=TX('fields', 0.9, form=False), fields_b=TX('fields_b', 0.9, form=False), road=TX('road', 0.95, form=False), bank=TX('bank', 0.85, form=False),
             grass=TX('grass', 0.85, form=False), grass2=TX('grass2', 0.8, form=False), tiles=TX('tiles', 1.5), tiles_d=TX('tiles_d', 1.4), tiles_d_c=C('#3a4058', 1.3),
             canvas=TX('canvas', 1.35), canvas_red=TX('canvas_red', 1.0), hide=TX('hide', 1.3), planks=TX('planks', 1.1), planks_d=TX('planks_d', 1.1),
             water=TX('water', 1.0, form=False, glow='water', glow_k=0.30), silk=TX('silk', 1.6, glow='silk', glow_k=0.22),
             wood=C('#8a5a36', 1.1), wood_d=C('#5a3a24', 1.0), wood_l=C('#b88a56', 1.1), red=C('#b82c20', 1.15), red_d=C('#7a1c1c', 1.1), gold=_glossy(C('#e0b040', 1.3, (1.5, 1.2, 0.8)), (1.0, 0.82, 0.45), 0.35, 0.3),
             iron=_glossy(C('#3a3c48', 1.2), (0.7, 0.75, 0.9), 0.4, 0.3), steel=_glossy(C('#b8c0d0', 1.5), (0.8, 0.88, 1.0), 0.55, 0.2), bronze=_glossy(C('#b8843a', 1.3), (1.0, 0.76, 0.42), 0.4, 0.3),
             stone=C('#9a98a8', 1.1), stone_d=C('#6a6878', 1.0), black=C('#201c28', 1.0), cream=C('#eadcc0', 1.15), white=C('#f0e8d8', 1.2), straw=C('#d8b860', 1.15), straw_d=C('#b08a40', 1.0),
             clay=C('#8a5a40', 1.1), clay_d=C('#5a3a2a', 1.0), jade=C('#3a8a74', 1.2), teal=C('#2a6a7a', 1.1), indigo=C('#2a3470', 1.1), ox=C('#7a5640', 1.25), ox_d=C('#3a2a22', 1.0), ox_n=C('#b89478', 1.1), hay=C('#d0b060', 1.2),
             tunnel=C('#3a3046', 0.9, 0.5, form=False), plaster=C('#d8c8a8', 1.1), plaster_d=C('#b0a088', 1.05), leaf=C('#4a7a4a', 1.0), hill=C('#2a2c6a', 0.9, form=False),
             lantern=E('lantern', '#ff8a30', 4.2), lantern_g=E('lantern_g', '#ffd070', 5.5), win=E('win', '#ff9a38', 1.25), win_c=E('win_c', '#ffb860', 1.5), gate_glow=E('gate_glow', '#ff8a34', 1.3),
             flame=E('flame', '#e8561c', 1.0), flame_t=E('flame_t', '#b8301a', 0.9), flame_e=E('flame_e', '#e8561c', 0.9), flame_m=E('flame_m', '#ffb238', 0.85), flame_c=E('flame_c', '#fffeec', 1.45), ember=E('ember', '#ff6a20', 2.2),
             skin=C('#d8a47a', 1.15), lacq=C('#4a1a20', 1.0), tiles_g=C('#4a5068', 1.3), rain=mat_emit(pre + 'e_rain', image=tx['rain'], strength=1.0, alpha=True), moon=mat_emit(pre + 'e_moon', image=tx['moon'], strength=3.2, alpha=True),
             moon_h=BK._mat_add(pre + 'a_moonh', tx['glow'], (0.35, 0.54, 0.96), 1.0), sky=D._mat_sky(pre + 'sky', P, tx['sky_' + STATE['light']], P['sky_k']),
             halo=ADD('halo', 'glow', (1.0, 0.6, 0.28), 1.0), halo_s=ADD('halo_s', 'glow', (1.0, 0.7, 0.35), 0.8), halo_big=ADD('halo_big', 'glow', (1.0, 0.55, 0.24), 0.55),
             pool=ADD('pool', 'pool', (1.0, 0.5, 0.14), 0.9), pool_w=ADD('pool_w', 'pool', (1.0, 0.5, 0.16), 0.6), streak=ADD('streak', 'streak', (1.0, 0.62, 0.3), 1.5), streak_m=ADD('streak_m', 'streak', (1.0, 0.88, 0.6), 1.5),
             mist=BK._mat_add(pre + 'a_mist', tx['glow'], (0.5, 0.42, 0.85), 0.08), dust=ADD('dust', 'glow', (0.62, 0.48, 0.38), 0.5))
    return M

# ----------------------------------------------------------------------------- wall
# ----------------------------------------------------------------------------- real flames (layered tongues)
def flame(fb, base, h, s=1.0, lean=(0.0, 0.0), seed=0, n=4, spread=0.35, mats=None):
    """Layered flame: n outer tongues graded tip #b8301a -> edge #e8561c, mid tongues #ffb238, a small core #fffeec (the only part that clips).
    Each tongue is a bent chain of tapering cone segments leaning with `lean` (xy offset at the tip, in D) with a little S wobble. `fb` is a mesh bank
    without shadows. base = V (root centre), h = full height."""
    M = STATE['M']; base = V(base); rr = _rnd(int(abs(base.x * 13 + base.y * 7 + base.z * 3) * 10 + seed) & 0xffff)
    lx, ly = lean; seg = 7
    def tongue(c0, ht, rad, mats_by_t, wob, lx_, ly_, a0):
        pts = []
        for k in range(seg + 1):
            t = k / seg; sw = math.sin(t * 3.1 + a0) * wob * t
            pts.append(c0 + V((lx_ * t ** 1.5 + sw * math.cos(a0), ly_ * t ** 1.5 + sw * math.sin(a0), ht * t)))
        for k in range(seg):
            t0, t1 = k / seg, (k + 1) / seg
            r0 = rad * (1 - t0) ** 0.72 * min(1.0, 0.55 + t0 * 3.0) if t0 > 0 else rad * 0.55; r1 = rad * (1 - t1) ** 0.72 if t1 < 1 else 0.0
            fb.frustum(pts[k], pts[k + 1], r0, r1, mats_by_t(t0), seg=5, cap0=(k == 0), cap1=False)
    ot = lambda t: M['flame_t'] if t > 0.62 else (M['flame_e'] if t > 0.2 else M['flame_m'])
    cam = V(STATE['cam']['loc']); ac = math.atan2(cam.y - base.y, cam.x - base.x)                         # layering is seen from the camera: red outer tongues behind, amber in the middle, the cream core in front
    for k in range(n):                                                                       # outer tongues: tall, red-orange, tipped dark red, behind and around
        a = ac + math.pi + (k - (n - 1) / 2) * (2.6 / max(1, n - 1)) + rr.uniform(-0.2, 0.2); d = spread * s * 0.85
        c0 = base + V((d * math.cos(a), d * math.sin(a), 0)); ht = h * rr.uniform(0.78, 1.0)
        tongue(c0, ht, (0.52 if n <= 4 else 0.38) * s, ot, (0.18 if n <= 4 else 0.34) * s, lx * ht / h + rr.uniform(-0.15, 0.15) * s, ly * ht / h + rr.uniform(-0.15, 0.15) * s, a)
    for k in range(max(2, n - 1)):                                                           # mid tongues: amber, in front of the outer ones
        a = ac + math.pi + (k - (max(2, n - 1) - 1) / 2) * 1.5; d = spread * s * 0.22; c0 = base + V((d * math.cos(a), d * math.sin(a), 0.03 * s)); ht = h * rr.uniform(0.60, 0.80)
        tongue(c0, ht, 0.40 * s, lambda t: M['flame_m'] if t < 0.62 else M['flame_e'], 0.12 * s, lx * ht / h * 0.9, ly * ht / h * 0.9, a)
    cf = base + V((0.16 * s * math.cos(ac), 0.16 * s * math.sin(ac), 0.04 * s))                      # hot core, nearest the camera
    tongue(cf, h * 0.46, 0.27 * s, lambda t: M['flame_c'] if t < 0.7 else M['flame_m'], 0.05 * s, lx * 0.3, ly * 0.3, 0.0)
    for k in range(int(3 + 2 * s)):                                                          # embers
        fb.sphere(base + V((rr.uniform(-0.8, 0.8) * s + lx * 0.7, rr.uniform(-0.8, 0.8) * s + ly * 0.7, rr.uniform(0.9, 1.9) * h)), 0.05 * s, M['ember'], seg=4, rings=3)

def px(p, cam=None):
    """World point -> (x, y) pixel on the 720x1280 frame of the current camera (None if behind)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = cam or sc.camera; bpy.context.view_layer.update(); v = world_to_camera_view(sc, cam, Vector(p))
    return (round(v.x * 720), round((1 - v.y) * 1280), round(v.z, 1))

def person(Bk, M, pos, yaw=0.0, pose='stand', s=1.0, robe=None, cup=False, cd=40.0, helmet=True, seed=1):
    """Stand-in soldier / guard (low-poly, 4.6 D tall when standing): robe cone, belt, head with cap or helmet, arms, optional spear / cup.
    poses: stand, spear, cheer (cup raised), sit (on the ground / a log, cup to the mouth), sleep (lying on the side, back to camera)."""
    F = Frame((pos[0], pos[1], pos[2] if len(pos) > 2 else 0.0), yaw); b = Bk('people', hull=T.hull(cd)); robe = robe or M['black']; sk = M['skin']
    P = lambda x, y, z: F.p(x * s, y * s, z * s)
    if pose == 'sleep':
        b.frustum(P(-1.4, 0, 0.55), P(1.5, 0, 0.6), 0.55 * s, 0.5 * s, robe, seg=8)
        b.sphere(P(1.95, 0, 0.62), 0.42 * s, sk, seg=8, rings=5); b.frustum(P(1.95, 0, 0.8), P(2.1, 0, 0.86), 0.46 * s, 0.4 * s, M['black'], seg=8)
        b.frustum(P(-1.4, -0.1, 0.5), P(-2.6, -0.3, 0.35), 0.28 * s, 0.22 * s, M['red_d'], seg=6)
        b.frustum(P(0.6, 0.5, 0.45), P(1.4, 0.55, 0.9), 0.14 * s, 0.12 * s, robe, seg=5)
        return
    zs = 0.0
    if pose == 'sit':
        zs = -1.2
        b.frustum(P(-0.3, 0, 0.2), P(0.9, 0, 0.5), 0.4 * s, 0.34 * s, robe, seg=7); b.frustum(P(0.9, -0.28, 0.45), P(1.5, -0.4, 0.2), 0.2 * s, 0.17 * s, M['red_d'], seg=6)
        b.frustum(P(0.9, 0.28, 0.45), P(1.5, 0.4, 0.2), 0.2 * s, 0.17 * s, M['red_d'], seg=6)
    else:
        b.frustum(P(0, -0.22, 0.05), P(0, -0.22, 1.9), 0.26 * s, 0.2 * s, M['black'], seg=6); b.frustum(P(0, 0.22, 0.05), P(0, 0.22, 1.9), 0.26 * s, 0.2 * s, M['black'], seg=6)
    b.frustum(P(0, 0, 1.6 + zs), P(0, 0, 3.4 + zs), 0.78 * s, 0.5 * s, robe, seg=9)
    b.frustum(P(0, 0, 2.3 + zs), P(0, 0, 2.5 + zs), 0.8 * s, 0.8 * s, M['red'], seg=9, cap0=False, cap1=False)
    b.frustum(P(0, 0, 3.4 + zs), P(0, 0, 3.7 + zs), 0.2 * s, 0.2 * s, sk, seg=6)
    hz = 4.1 + zs; b.sphere(P(0, 0, hz), 0.46 * s, sk, seg=9, rings=6); b.sphere(P(0.2, -0.05, hz + 0.04), 0.1 * s, M['black'], seg=4, rings=3)
    if helmet:
        b.frustum(P(0, 0, hz + 0.16), P(0, 0, hz + 0.62), 0.5 * s, 0.22 * s, M['iron'], seg=9); b.frustum(P(0, 0, hz + 0.62), P(0, 0, hz + 1.0), 0.04 * s, 0.1 * s, M['red'], seg=5)
    else: b.frustum(P(0, 0, hz + 0.2), P(0, 0, hz + 0.55), 0.46 * s, 0.4 * s, M['black'], seg=9)
    if pose in ('cheer', 'sit') and cup:
        sh = P(0.0, -0.75, 3.1 + zs); hand = P(0.35, -1.0, 4.45 + zs) if pose == 'cheer' else P(0.5, -0.3, hz - 0.35)
        J_rod(b, sh, hand, 0.14 * s, robe); b.frustum(hand, hand + V((0, 0, 0.32 * s)), 0.13 * s, 0.22 * s, M['bronze'], seg=6)
        sh2 = P(0.0, 0.75, 3.1 + zs); J_rod(b, sh2, P(0.4, 0.45, 2.0 + zs), 0.14 * s, robe)
    elif pose == 'spear':
        J_rod(b, P(0, -0.75, 3.1), P(0.3, -0.85, 2.3), 0.14 * s, robe); J_rod(b, P(0, 0.75, 3.1), P(0.3, 0.85, 2.3), 0.14 * s, robe)
        J_rod(b, P(0.4, -0.9, 0.0), P(0.4, -0.9, 7.0), 0.07 * s, M['wood']); b.frustum(P(0.4, -0.9, 7.0), P(0.4, -0.9, 7.9), 0.12 * s, 0.0, M['steel'], seg=4)
    else:
        for sy in (-1, 1): J_rod(b, P(0, sy * 0.75, 3.1 + zs), P(0.3, sy * 0.85, 2.0 + zs), 0.14 * s, robe)

def J_rod(mb, a, b, r, mat, seg=5): rod(mb, a, b, r, mat, seg=seg)

# ----------------------------------------------------------------------------- live fires: every flame is its own object (scale / lean flicker per frame) with its light
def _hash(a, b=0): return ((a * 73856093) ^ (b * 19349663) ^ 0x5bd1e995) & 0xffffff
def _fl(frame, seed=0):
    """Deterministic flicker 0.78 .. 1.25 from the frame number (smooth, per fire phase)."""
    r = random.Random(_hash(int(seed), 7)); p1, p2, p3 = r.uniform(0, 6.28), r.uniform(0, 6.28), r.uniform(0, 6.28)
    f = float(frame); return 1.0 + 0.13 * math.sin(f * 0.83 + p1) + 0.08 * math.sin(f * 1.91 + p2) + 0.07 * math.sin(f * 3.37 + p3)

def live_flame(base, h, s=1.0, lean=(0.0, 0.0), seed=0, n=4, spread=0.35, light=0.0, name='fl', rgb=FIRE, lamp_r=0.3, lamp_dz=0.5, shadow=False, warm=(4.0, 0.9)):
    """Layered flame as its own object (origin at the flame root, so scale flickers around the base) + optional point light + a warm source for the wall material."""
    base = V(base); mb = MB(); flame(mb, base, h, s, lean=lean, seed=seed, n=n, spread=spread)
    ob = _obj(mb, 'flame_%s_%d' % (name, len(STATE['fires'])), STATE['SET'], shadow=False); ob.data.transform(Matrix.Translation(-base)); ob.location = base; ob.visible_shadow = False
    L_ = lamp('%s_%d' % (name, len(STATE['fires'])), base + V((0, 0, lamp_dz)), light, rgb, r=lamp_r, shadow=shadow) if light > 0 else None
    STATE['fires'].append(dict(ob=ob, light=L_, E0=light, seed=seed + len(STATE['fires']) * 3, base=base, h=h))
    if warm: STATE['warm'].append((base + V((0, 0, h * 0.4)), warm[0], warm[1]))
    return ob

def flicker(frame=None, k=1.0):
    """Flicker every fire for `frame` (default: the scene frame): flame objects scale / sway, lights vary; k scales the light (0 = all out). With frame= the values are keyed
    (LINEAR) - call it for every frame of a shot, or rely on the frame handler (installed by build) when rendering an animation."""
    f = bpy.context.scene.frame_current if frame is None else frame
    for fi in STATE.get('fires', ()):
        a = _fl(f, fi['seed']); ob = fi['ob']; b_ = _fl(f + 5, fi['seed'] + 1)
        kk = fi.get('k', 1.0); ob.scale = ((0.94 + 0.10 * (a - 1) * 3) * kk, (0.94 + 0.10 * (b_ - 1) * 3) * kk, max(0.001, (0.92 + 0.6 * (a - 1)) * (1.0 if k > 0 else 0.001)) * kk)
        ob.rotation_euler = (0.05 * (b_ - 1) * 3, 0.05 * (a - 1) * 3, 0.0)
        if fi['light'] is not None: fi['light'].data.energy = fi['E0'] * a * k
        if frame is not None:
            for path in ('scale', 'rotation_euler'): ob.keyframe_insert(path, frame=frame)
            if fi['light'] is not None: T._key(fi['light'].data, 'energy', frame, 'LINEAR')
    for fc in STATE.get('flame_cards', ()):
        a = _fl(f, fc['seed']); root = fc['root']; on = root.get('lit', 1.0)
        root['fu'] = float(int(((f + fc['seed']) // 2) % 4) * 0.25); root['fk'] = a * on
        for ch in root.children:
            if ch.type == 'LIGHT': ch.data.energy = fc['E0'] * a * on * k
        if frame is not None:
            for ch in root.children:
                if ch.type == 'LIGHT': T._key(ch.data, 'energy', frame, 'LINEAR')
            root.keyframe_insert('["fu"]', frame=frame); root.keyframe_insert('["fk"]', frame=frame)

def _flicker_handler(scene, *a): flicker()

def install_handlers():
    for h in (bpy.app.handlers.frame_change_pre, bpy.app.handlers.render_pre):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_flicker_handler', '_sky_follow'): h.remove(f)
        h.append(_flicker_handler); h.append(_sky_follow)

def _sky_follow(scene, *a):
    cam = scene.camera; so = STATE.get('sky_obj'); mo = STATE.get('moon_objs', ())
    if cam is None or so is None: return
    so.location = cam.matrix_world.translation
    for o, off in mo: o.location = cam.matrix_world.translation + off

def brazier(Bk, M, p, s=1.0, light=0.0, name='br', halo_r=3.2, shadow=False, tall=2.2, lean=(0.0, 0.0), flame_k=1.0, warm=(4.0, 0.9)):
    """Bronze / iron brazier on a tripod with a layered live flame; point light (1.0, 0.50, 0.18)."""
    p = V(p)
    if R2.skipped(p): return p + V((0, 0, (tall + 0.66) * s))
    w = Bk('wood', hull=0.0); h = Bk('halos', shadow=False)
    for k in range(3):
        a = 2 * math.pi * k / 3 + 0.5; rod(w, p + V((0.7 * s * math.cos(a), 0.7 * s * math.sin(a), 0)), p + V((0.14 * s * math.cos(a), 0.14 * s * math.sin(a), tall * s)), 0.1 * s, M['iron'], seg=5)
    rod(w, p + V((0, 0, tall * s)), p + V((0, 0, (tall + 0.55) * s)), 0.30 * s, M['bronze'], seg=9, r1=0.62 * s)
    rod(w, p + V((0, 0, (tall + 0.5) * s)), p + V((0, 0, (tall + 0.62) * s)), 0.66 * s, M['iron'], seg=9, r1=0.66 * s)
    c = p + V((0, 0, (tall + 0.66) * s))
    live_flame(c, 1.9 * s * flame_k, 0.62 * s, lean=lean, seed=int(p.x + p.y), n=3, spread=0.3, light=light, name=name, lamp_dz=0.5, shadow=shadow, warm=warm)
    halo(h, c + V((0, 0, 0.8 * s)), halo_r * s, M['halo'])
    STATE['torches'].append(tuple(c)); return c

def oil_lamp(Bk, M, p, s=1.0, light=0.0, name='ol', halo_r=1.6, h=3.4):
    """Bronze standing oil lamp (Warring States): three feet, a stem with discs, a shallow dish with one small flame. p = floor point."""
    p = V(p)
    if R2.skipped(p): return p + V((0, 0, h * s))
    w = Bk('wood', hull=0.0); hl = Bk('halos', shadow=False)
    for k in range(3):
        a = 2 * math.pi * k / 3; rod(w, p + V((0.5 * s * math.cos(a), 0.5 * s * math.sin(a), 0.0)), p + V((0.08 * s * math.cos(a), 0.08 * s * math.sin(a), 0.4 * s)), 0.08 * s, M['bronze'], seg=4)
    rod(w, p + V((0, 0, 0.4 * s)), p + V((0, 0, (h - 0.3) * s)), 0.09 * s, M['bronze'], seg=6)
    for z in (0.9, 1.9): rod(w, p + V((0, 0, z * s)), p + V((0, 0, (z + 0.1) * s)), 0.3 * s, M['bronze'], seg=8, r1=0.3 * s)
    rod(w, p + V((0, 0, (h - 0.3) * s)), p + V((0, 0, h * s)), 0.2 * s, M['bronze'], seg=8, r1=0.5 * s)
    c = p + V((0, 0, h * s)); live_flame(c, 0.95 * s, 0.26 * s, seed=int(p.x * 3 + p.y), n=2, spread=0.1, light=light, name=name, lamp_dz=0.3, rgb=LAMP, warm=(3.0, 0.5))
    halo(hl, c + V((0, 0, 0.35 * s)), halo_r * s, M['halo_s'])
    return c

def lantern(Bk, M, p, s=1.0, light=0.0, name='ln', halo_r=1.8, hang=0.9, floor=None):
    """Kept for the call sites: now a bronze standing oil lamp whose FLAME is at p (stem down to `floor`, else 3 D)."""
    p = V(p); fl = floor if floor is not None else p.z - 3.4 * s
    return oil_lamp(Bk, M, V((p.x, p.y, fl)), s=s, light=light, name=name, halo_r=halo_r, h=(p.z - fl) / s)

def torch_post(Bk, M, p, s=1.0, light=900.0, name='t', halo_r=3.2, shadow=False, warm=(4.0, 0.9)):
    return brazier(Bk, M, p, s=s * 0.8, light=light, name=name, halo_r=halo_r, shadow=shadow, warm=warm)

def banner(Bk, M, base, h, cloth_w, cloth_h, col, trim, wave=0.0, yaw=0.0, sw=True):
    """Pole with a hanging banner (plain shape, no text): a long swallow-tailed cloth with a trim stripe."""
    w = Bk('wood'); cl = Bk('cloth'); base = V(base); F = Frame(base, yaw)
    rod(w, base, base + V((0, 0, h)), 0.16, M['wood_d'], seg=6); w.sphere(base + V((0, 0, h + 0.25)), 0.3, M['gold'], seg=8, rings=5)
    rod(w, base + V((0, 0, h - 0.3)), F.p(cloth_w + 0.4, 0, h - 0.3), 0.08, M['wood_d'], seg=5)
    n = 8
    for i in range(n):
        x0, x1 = cloth_w * i / n, cloth_w * (i + 1) / n; z0_, z1_ = 0.0, 0.0
        sw0 = math.sin(i * 0.9 + wave) * 0.35 * (i / n); sw1 = math.sin((i + 1) * 0.9 + wave) * 0.35 * ((i + 1) / n)
        top = h - 0.4; bot0 = top - cloth_h; bot1 = bot0
        if sw: bot0 = top - cloth_h * (1 - 0.35 * (i / n)); bot1 = top - cloth_h * (1 - 0.35 * ((i + 1) / n))
        pts = [F.p(x0, sw0, top), F.p(x1, sw1, top), F.p(x1, sw1, bot1), F.p(x0, sw0, bot0)]
        cl.oface(pts, col, [(0, 0)] * 4, F.Y * -1); cl.oface(pts[::-1], col, [(0, 0)] * 4, F.Y)
        tp = [F.p(x0, sw0, top), F.p(x1, sw1, top), F.p(x1, sw1, top - 0.45), F.p(x0, sw0, top - 0.45)]
        cl.oface(tp, trim, [(0, 0)] * 4, F.Y * -1); cl.oface(tp[::-1], trim, [(0, 0)] * 4, F.Y)


# ----------------------------------------------------------------------------- flame cards for the 2D puppets (ox tails, torches in hands)
def flame_card(parent=None, scale=1.0, loc=(0.0, 0.0, 0.0), name='flame', light=True, lit=1.0, energy=700.0):
    """A camera-facing flame card (painted layered flame, 4 flicker variants) + a warm point light, under one Empty `root`. Parent it to an ox card / a hand:
    root.parent = parent (pass `parent`), root.location = loc (local to the parent; the card's BOTTOM centre is the flame root). scale 1 = 2.2 D tall.
    flicker(frame) drives the card variant / brightness and the light each frame; set_flame_card(root, lit, frame) switches it on / off (keyed).
    Returns the root Empty."""
    tx = STATE['tx']; M = STATE['M']
    if 'flame_card' not in M:
        m = bpy.data.materials.new(STATE['pre'] + 'flame_card'); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
        out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); t = N('ShaderNodeTexImage'); t.image = T._img(tx['flame_atlas']); t.interpolation = 'Linear'; t.extension = 'CLIP'
        uv = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.vector_type = 'POINT'
        at = N('ShaderNodeAttribute'); at.attribute_type = 'OBJECT'; at.attribute_name = '["fu"]'; cm = N('ShaderNodeCombineXYZ'); L(at.outputs['Fac'], cm.inputs['X'])
        ad = N('ShaderNodeVectorMath'); ad.operation = 'SCALE'; ad.inputs['Scale'].default_value = 1.0; L(cm.outputs['Vector'], ad.inputs[0])
        L(uv.outputs['UV'], mp.inputs['Vector']); L(ad.outputs['Vector'], mp.inputs['Location']); L(mp.outputs['Vector'], t.inputs['Vector'])
        ak = N('ShaderNodeAttribute'); ak.attribute_type = 'OBJECT'; ak.attribute_name = '["fk"]'
        sm = N('ShaderNodeMath'); sm.operation = 'MULTIPLY'; sm.inputs[1].default_value = 1.35; L(ak.outputs['Fac'], sm.inputs[0]); L(sm.outputs[0], em.inputs['Strength'])
        L(t.outputs['Color'], em.inputs['Color']); L(t.outputs['Alpha'], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
        m.cycles.emission_sampling = 'NONE'; M['flame_card'] = m
    n = len(STATE['flame_cards']); root = bpy.data.objects.new('%s_%d' % (name, n), None); STATE['SET'].objects.link(root); root.empty_display_size = 0.3
    if parent is not None: root.parent = parent
    root.location = loc; root.scale = (scale,) * 3; root['lit'] = float(lit); root['fu'] = 0.0; root['fk'] = 1.0
    w, h = 1.3, 2.2; me = bpy.data.meshes.new('flame_card_mesh'); me.from_pydata([(-w / 2, 0, 0), (w / 2, 0, 0), (w / 2, h, 0), (-w / 2, h, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name='UVMap')
    for i, c in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = (c[0] * 0.25, c[1])
    me.materials.append(M['flame_card']); card = bpy.data.objects.new('%s_card_%d' % (name, n), me); STATE['SET'].objects.link(card); card.parent = root
    card.visible_shadow = False; no_bounce(card); tc = card.constraints.new('TRACK_TO'); tc.track_axis = 'TRACK_Z'; tc.up_axis = 'UP_Y'; tc.target = bpy.data.objects.get('cam')
    d = bpy.data.lights.new('%s_lamp_%d' % (name, n), 'POINT'); d.color = FIRE; d.energy = energy * scale * lit; d.shadow_soft_size = 0.4; d.use_shadow = False
    lo = bpy.data.objects.new(d.name, d); STATE['LIGHTS'].objects.link(lo); lo.parent = root; lo.location = (0, 0.6, 1.0); lo.visible_camera = False
    if not light: lo.hide_render = True
    STATE['flame_cards'].append(dict(root=root, card=card, seed=n * 5 + 1, E0=energy * scale))
    return root

def set_flame_card(root, lit, frame=None):
    """Switch a flame card (and its light) on (1) / off (0); keyed CONSTANT at `frame`."""
    root['lit'] = float(lit)
    for ch in root.children: _vis(ch, lit > 0.0, frame)
    if frame is not None: root.keyframe_insert('["lit"]', frame=frame)

# ----------------------------------------------------------------------------- keyed visibility / transform helpers
def _vis(ob, on, frame=None):
    ob.hide_render = not on; ob.hide_viewport = not on
    if frame is not None:
        for p in ('hide_render', 'hide_viewport'): ob.keyframe_insert(p, frame=frame)
        for fc in T._fcurves(ob):
            if fc.data_path in ('hide_render', 'hide_viewport'):
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'

def _xf(ob, loc=None, rot=None, scl=None, frame=None, interp='LINEAR'):
    if loc is not None: ob.location = loc
    if rot is not None: ob.rotation_euler = rot
    if scl is not None: ob.scale = scl if hasattr(scl, '__len__') else (scl,) * 3
    if frame is not None:
        for p, v in (('location', loc), ('rotation_euler', rot), ('scale', scl)):
            if v is not None: ob.keyframe_insert(p, frame=frame)
        for fc in T._fcurves(ob):
            if fc.data_path in ('location', 'rotation_euler', 'scale'):
                for kp in fc.keyframe_points: kp.interpolation = interp

def localize(ob, c):
    """Move an object's origin to world point c (the mesh stays where it is)."""
    c = V(c); ob.data.transform(Matrix.Translation(-c)); ob.location = c; return ob

def animate(setter, f0, f1, v0, v1, step=1, ease='smooth', **kw):
    """Key a state setter over frames f0..f1: setter(v, frame=f) with v eased from v0 to v1, e.g. animate(J.set_holes, 1205, 1309, 0, 12)."""
    n = max(1, int(f1 - f0)); fs = list(range(int(f0), int(f1) + 1, step))
    if fs[-1] != int(f1): fs.append(int(f1))
    for f in fs:
        t = (f - f0) / n; t = t * t * (3 - 2 * t) if ease == 'smooth' else t
        setter(v0 + (v1 - v0) * t, frame=f, **kw)

# ----------------------------------------------------------------------------- build
import jimo_shots as S                                      # noqa: E402  (shot table, cameras, marks, herd helper)
import jimo_wall as WL                                      # noqa: E402
import jimo_in as IN                                        # noqa: E402
import jimo_camp as CAMP                                    # noqa: E402
import jimo_vista as VS                                     # noqa: E402
import jimo_ox as OX                                        # noqa: E402
import jimo_r2 as R2                                        # noqa: E402  (round 2: cards, per-shot tweaks)

def build(location=None, preset=None, light=None, clear=True):
    """Build one location ('jimo_in' | 'jimo_out' | 'yan_camp' | 'vista') for a preset (a shot name 's01'..'s26', or the location name for its default wide
    camera) and a light (NIGHT | DUSK | DAWN; default = the preset's). Returns the anchors dict (API.md); A['cam'] is the preset camera: J.make_camera(A['cam'])."""
    if preset in S.SHOTS: location = location or S.SHOTS[preset]['loc']; light = light or S.SHOTS[preset]['light']
    location = LEGACY.get(location, location) or (S.SHOTS[preset]['loc'] if preset in S.SHOTS else 'jimo_out')
    if preset is None: preset = location
    light = light or (S.SHOTS[preset]['light'] if preset in S.SHOTS else LOCS[location][0])
    assert location in LOCS and light in LOCS[location], 'location %s has lights %s (got %s)' % (location, LOCS.get(location), light)
    scene = bpy.context.scene; P = dict(LIGHTS[light])
    if light != 'NIGHT':
        az = SUN_AZ.get((location, light), P['sun_az'])
        if preset in S.SHOTS and S.SHOTS[preset].get('sun') is not None: az = S.SHOTS[preset]['sun']          # per-shot sun azimuth (round 2: sun behind or beside the camera)
        P['sun_az'] = az
        if location == 'vista': P['sun_el'] = 15.0; P['air'] = (P['air'][0], 0.45, 120.0, 700.0)
        P['key_dir'] = _kdaz(az, P['sun_el'])
    else: P['moon_az'] = MOON_AZ_LOC[location]
    STATE.clear(); STATE.update(P=P, preset=preset, loc=location, area=location, light=light, location=location)
    for hk in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_pre):
        for f in list(hk):
            if getattr(f, '__name__', '') in ('_flicker_handler', '_sky_follow'): hk.remove(f)
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('JM_', 'ink')): bpy.data.materials.remove(m)
    tx = JX.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_jimo') or bpy.data.worlds.new('W_jimo'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(scene, 'final'); scene.render.threads = 2; scene.frame_start = 1; scene.frame_current = 1
    pre = 'JM_%s_%s_' % (location, light); M = materials(P, tx, pre); STATE['M'] = M; STATE['pre'] = pre
    kd = V(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    STATE.update(fires=[], flame_cards=[], marks={}, torches=[], warm=[], banks_obj={}, moon_objs=[], states={})
    cams = S.cams_for(location, light); STATE['cams'] = cams
    cs = S.preset_cam(preset, location, light); STATE['cam'] = cs
    Bk = Banks(); STATE['B'] = Bk
    sky_dome(SET, P, M, location, light)
    if location == 'jimo_out': WL.bind(sys.modules[__name__]); WL.build_out(Bk, M, light)
    elif location == 'jimo_in': WL.bind(sys.modules[__name__]); IN.bind(sys.modules[__name__]); IN.build_in(Bk, M, light)
    elif location == 'yan_camp': WL.bind(sys.modules[__name__]); CAMP.bind(sys.modules[__name__]); CAMP.build_camp(Bk, M, light)
    elif location == 'vista': VS.bind(sys.modules[__name__]); VS.build_vista(Bk, M, light)
    Bk.flush(SET)
    nf = bpy.data.collections.get('NOFIRE') or bpy.data.collections.new('NOFIRE')
    for ob in list(nf.objects): nf.objects.unlink(ob)
    for n in STATE.get('warm_names', ()):
        if n in STATE['objects']: bake_warm(STATE['objects'][n]); nf.objects.link(STATE['objects'][n])
    for co in nf.collection_objects: co.light_linking.link_state = 'EXCLUDE'
    for lo in LIG.objects:                                   # the static fires' light on the wall is painted (warm weights), the real lamps must not wash it pink
        if lo.type == 'LIGHT' and lo.data.type == 'POINT': lo.light_linking.receiver_collection = nf
    scene.cycles.use_light_tree = True
    MN._denoise(scene); setup_grade(scene)
    W9._air_comp(scene, P); hue_guard(scene)
    for ob in SET.objects: no_bounce(ob)
    for f in STATE.get('post_flush', ()): f()
    _post_build(); install_handlers(); flicker(1)
    A = anchors(preset, location, light); STATE['A'] = A
    if preset in S.SHOTS: R2.post_build(preset, location, light)
    return A

def sky_dome(SET, P, M, location, light):
    R = 330.0; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [V((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    so = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = so
    taz = SKY_SUN[light][0]; waz = P['moon_az'] if light == 'NIGHT' else P['sun_az']; so.rotation_euler = (0, 0, math.radians(waz - taz))
    STATE['moon_objs'] = []
    if light == 'NIGHT':                                         # the moon: a pale disc + soft halo on the dome (follows the camera)
        mel = P['moon_el']; d = V((math.cos(math.radians(mel)) * math.cos(math.radians(waz)), math.cos(math.radians(mel)) * math.sin(math.radians(waz)), math.sin(math.radians(mel))))
        u = d.cross(V((0, 0, 1))).normalized(); v = u.cross(d).normalized(); rr = 12.5 * R / 250; mc = V((0, 0, 0)) + d * (R * 0.92)
        mb = MB(); mb.face([mc - u * rr - v * rr, mc + u * rr - v * rr, mc + u * rr + v * rr, mc - u * rr + v * rr][::-1], M['moon'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
        rh = rr * 3.2; mb.face([mc * 0.999 - u * rh - v * rh, mc * 0.999 + u * rh - v * rh, mc * 0.999 + u * rh + v * rh, mc * 0.999 - u * rh + v * rh][::-1], M['moon_h'], [(0, 0), (1, 0), (1, 1), (0, 1)][::-1])
        mo = _obj(mb, 'moon', SET, shadow=False); STATE['moon_dir'] = d; STATE['moon_objs'] = [(mo, V((0, 0, 0)))]

def hue_guard(scene, shift=0.07):
    """Compositor 'rose / lavender guard' just before the output: hues 295-350 deg (blue ambient + orange fire light = magenta rose) are pushed toward warm red-orange, 255-295 (lavender)
    toward blue. The fire-lit earth and the dusk ground stay warm, the night shade stays blue; no pixel is left magenta."""
    ng = scene.compositing_node_group; go = [n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'][0]
    lk = go.inputs[0].links[0]; src = lk.from_socket; ng.links.remove(lk)
    hc = ng.nodes.new('CompositorNodeHueCorrect'); hc.name = 'hue_guard'; cv = hc.mapping.curves[0]
    pts = [(0.0, 0.5), (0.05, 0.5), (0.62, 0.5), (0.70, 0.5), (0.74, 0.44), (0.80, 0.42), (0.815, 0.43), (0.822, 0.57), (0.86, 0.62), (0.93, 0.62), (0.98, 0.56), (1.0, 0.5)]
    while len(cv.points) > 2: cv.points.remove(cv.points[1])
    cv.points[0].location = pts[0]; cv.points[-1].location = pts[-1]
    for (x, y) in pts[1:-1]: cv.points.new(x, y)
    for p in cv.points: p.handle_type = 'VECTOR'
    hc.mapping.update(); ng.links.new(src, hc.inputs['Image']); ng.links.new(hc.outputs['Image'], go.inputs[0])

def hills(Bk, M, centre=(0.0, 0.0), r0=165.0, r1=195.0, n=26, seed=7, rad=(34, 62), z=0.3):
    hb = Bk('hills', shadow=False); r = _rnd(seed)
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-0.1, 0.1); Rr = r.uniform(r0, r1); rd = r.uniform(*rad)
        lumpy(hb, V((centre[0] + Rr * math.cos(a), centre[1] + Rr * math.sin(a), -rd * z)), rd, M['hill'], 50 + i, seg=14, rings=6, rough=0.16, squash=0.42)

def make_camera(setup, name='cam'):
    ob = T.make_camera(setup, name); ob.data.clip_end = 900.0; ob.data.clip_start = 0.1; ob.data.dof.use_dof = False
    for fc in STATE.get('flame_cards', ()):
        for c in fc['card'].constraints:
            if c.type == 'TRACK_TO': c.target = ob
    _sky_follow(bpy.context.scene); return ob

def anchors(preset, location, light):
    P = STATE['P']; sh = S.SHOTS.get(preset)
    A = dict(location=location, preset=preset, light=light, cams=S.cams_for(location, light), cam=S.preset_cam(preset, location, light), key_dir=tuple(V(P['key_dir']).normalized()),
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), marks=dict(STATE.get('marks', {})), heights=dict(HEIGHT),
             lights=[o.name for o in STATE['LIGHTS'].objects], shot=dict(sh) if sh else None)
    return A

# ----------------------------------------------------------------------------- set states (every setter takes frame=None; with a frame it KEYS the values: call per frame or use animate())
def _post_build():
    ob = STATE['objects']
    for i, hx in enumerate(HOLE_X):
        if 'plug%d' % i in ob: localize(ob['plug%d' % i], (hx, (yo(0) + yi(0)) / 2, 0.0))
        for n, c in (('breach%d', (hx, yo(0), 0.0)), ('rubble%d', (hx, yo(0) - 1.0, 0.0)), ('dig%d', (hx, yi(0) + 2.0, 0.0)), ('hglow%d', (hx, (yo(0) + yi(0)) / 2, 0.0))):
            if n % i in ob: localize(ob[n % i], c)
    set_holes(0.0); set_gate(0.0)

def set_holes(n, frame=None):
    """Ragged breaches in the wall base (both faces): n = 0 .. 12 (float; 6.5 = six open and the seventh half dug). Hole i opens when n > i: its plug sinks (z scale), the rubble / rim /
    dug-earth heap + pick + basket grow in. HOLE_X lists the 12 centres (x -41 .. -13.5, 13.5 .. 41), width HOLE_W 3.4, height HOLE_H 4.3."""
    n = max(0.0, min(12.0, float(n))); ob = STATE['objects']; STATE['states']['holes'] = n
    for i in range(12):
        p = min(1.0, max(0.0, n - (11 - i)))                                                                   # opening order: x 41 -> -41 (hole 11 first, then 10 ... 0; s16 slides along x 50 -> 25)
        pl = ob.get('plug%d' % i)
        if pl is not None: _vis(pl, p < 0.999, frame); _xf(pl, scl=(1.0, 1.0, max(0.03, 1.0 - p)), frame=frame)
        for nm, th in (('breach%d', 0.15), ('rubble%d', 0.15), ('dig%d', 0.0), ('hglow%d', 0.15)):
            o = ob.get(nm % i)
            if o is not None:
                on = p > th; sc = 0.35 + 0.65 * min(1.0, max(0.0, (p - th) / (1 - th + 1e-6) if th < 1 else 1.0)); _vis(o, on, frame); _xf(o, scl=(sc, sc, sc), frame=frame)

def set_gate(k, frame=None):
    """Gate leaves: k 0 = shut .. 1 = open 75 degrees outward; 0.15 is 'a crack' (shot 12)."""
    STATE['states']['gate'] = k
    for (ob, sgn, hx, yy) in STATE.get('gate_leaves', ()): _xf(ob, rot=(0.0, 0.0, sgn * math.radians(75.0 * k)), frame=frame)

def set_party(k, frame=None): CAMP.set_party(k, frame)
def set_rout(k, frame=None): CAMP.set_rout(k, frame)
def set_pennants(k, side='yan', frame=None): VS.set_pennants(k, side, frame)
def set_qi_return(k, frame=None): VS.set_qi_return(k, frame)

def apply_state(spec, frame=None):
    """State string (comma separated): h<n> holes, g<k> gate, pt<k> party, ro<k> rout, pn<k> pennants (yan), qr<k> qi return, fl<k> flames (0 out .. 1)."""
    for tok in [t for t in (spec or '').split(',') if t]:
        if tok.startswith('pt'): set_party(float(tok[2:]), frame)
        elif tok.startswith('pn'): set_pennants(float(tok[2:]), 'yan', frame)
        elif tok.startswith('qr'): set_qi_return(float(tok[2:]), frame)
        elif tok.startswith('ro'): set_rout(float(tok[2:]), frame)
        elif tok.startswith('fl'): flicker(frame, k=float(tok[2:]))
        elif tok.startswith('h'): set_holes(float(tok[1:]), frame)
        elif tok.startswith('g'): set_gate(float(tok[1:]), frame)

def debug_ox(show=True):
    """The 3D placeholder ox (style board). NOT used in production (the oxen are 2D puppet cards); hidden by default; show=True builds / shows it at STATE['marks']['debug_ox']."""
    ob = STATE.get('debug_ox_objs')
    if ob is None:
        if not show: return
        n0 = set(STATE['SET'].objects); Bk2 = Banks(); OX.ox(sys.modules[__name__], Bk2, STATE['M'], STATE['marks'].get('debug_ox', (0.0, 10.0)), 90.0, s=0.6, tail_lit=False, name='dbg_ox'); Bk2.flush(STATE['SET'])
        ob = STATE['debug_ox_objs'] = [o for o in STATE['SET'].objects if o not in n0]
    for o in ob: _vis(o, show)

# ----------------------------------------------------------------------------- foreground props (1-2 D from the lens, parented to the camera)
def _cam_frame(setup):
    loc = V(setup['loc']); f = (V(setup['look_at']) - loc).normalized(); r = f.cross(V((0, 0, 1))).normalized(); u = r.cross(f).normalized(); return loc, f, r, u

def attach_fg(cam, setup, spec):
    """Build the shot's foreground prop 1.5-2 D in front of the lens (lower corner `side`) and parent it to the camera, so it stays 1-2 D from the lens through the move."""
    if not spec: return []
    kind, side = spec; sg = 1 if side == 'right' else -1; loc, f, r, u = _cam_frame(setup); M = STATE['M']; n0 = set(STATE['SET'].objects); Bk2 = Banks()
    o = loc + f * 1.9 + r * (0.74 * sg) + u * (-0.40); FGK = dict(reeds=0.15, jar=0.12, lantern=0.2, torch=0.13, counter=0.22, pick_baskets=0.22).get(kind, 0.3)
    ground = V((o.x, o.y, 0.0)) if o.z > 2.4 else V((o.x, o.y, max(0.0, o.z - 2.6)))
    if kind == 'lantern': oil_lamp(Bk2, M, V((o.x, o.y, o.z - 2.4)), s=0.9, light=0.0, name='fglamp', halo_r=1.2, h=3.0)
    elif kind == 'wheel':
        Fm = Frame((o.x, o.y, o.z - 1.9), math.degrees(math.atan2(f.y, f.x)) + 70.0); R = 1.9; w = Bk2('fgwood', hull=T.hull(3.0)); n = 20
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; beam(w, Fm.p(R * math.cos(a0), 0, R * math.sin(a0) + R), Fm.p(R * math.cos(a1), 0, R * math.sin(a1) + R), 0.34, 0.46, M['wood_d'], up=(Fm.Y.x, Fm.Y.y, Fm.Y.z))
        for i in range(6): a = math.pi * i / 6; rod(w, Fm.p(R * math.cos(a), 0, R * math.sin(a) + R), Fm.p(-R * math.cos(a), 0, -R * math.sin(a) + R), 0.14, M['wood'], seg=6)
        rod(w, Fm.p(0, -0.5, R), Fm.p(0, 0.5, R), 0.4, M['wood_d'], seg=10)
    elif kind == 'spear_rack':
        Fm = Frame((o.x, o.y, o.z - 2.6), math.degrees(math.atan2(f.y, f.x)) + 90.0); rk = Bk2('fgrack', hull=T.hull(3.0))
        for sx in (-1.2, 1.2): obox(rk, Fm.p(sx, 0, 2.0), Fm.X, Fm.Y, Fm.Z, 0.12, 0.12, 2.0, M['wood_d'])
        for z in (1.0, 2.6): obox(rk, Fm.p(0, 0, z), Fm.X, Fm.Y, Fm.Z, 1.3, 0.1, 0.09, M['wood'])
        for k in range(6): x = -1.0 + 0.4 * k; rod(rk, Fm.p(x, 0.3, 0.0), Fm.p(x * 0.9, 0.5, 5.2), 0.05, M['wood'], seg=4); rk.frustum(Fm.p(x * 0.9, 0.5, 5.2), Fm.p(x * 0.9, 0.5, 5.8), 0.1, 0.0, M['steel'], seg=4)
    elif kind == 'jar':
        Fm = V((o.x, o.y, o.z - 1.3)); jb = Bk2('fgjar', hull=T.hull(3.0)); ellipsoid(jb, Fm + V((0, 0, 0.9)), 0.8, 0.8, 0.95, M['clay'], seg=12, rings=8, rough=0.05, seed=3); cyl(jb, Fm + V((0, 0, 1.75)), 0.45, 0.4, M['clay_d'], seg=10, r1=0.55); cyl(jb, Fm + V((0, 0, 2.15)), 0.58, 0.18, M['red'], seg=10); cyl(jb, Fm + V((0, 0, 1.5)), 0.6, 0.2, M['straw'], seg=10, cap=False)
    elif kind == 'pick_baskets':
        Fm = Frame((o.x, o.y, o.z - 2.0), math.degrees(math.atan2(f.y, f.x)) + 30.0); pb = Bk2('fgdig', hull=T.hull(3.0))
        rod(pb, Fm.p(0, 0, 0.0), Fm.p(-0.5, 0.2, 3.6), 0.1, M['wood'], seg=5); obox(pb, Fm.p(-0.5, 0.2, 3.6), Fm.X, Fm.Y, Fm.Z, 0.08, 0.6, 0.12, M['iron'])
        pb.frustum(Fm.p(0.9, 0.2, 0), Fm.p(0.9, 0.2, 1.0), 0.5, 0.8, M['straw_d'], seg=10); lumpy(pb, Fm.p(0.9, 0.2, 1.0), 0.72, M['bank'], 5, seg=8, rings=4, rough=0.2, squash=0.4)
    elif kind == 'reeds':
        reed_ = Bk2('fgreeds', hull=T.hull(3.0)); b0 = V((o.x, o.y, o.z - 2.0))
        for k in range(4): q = b0 + r * (0.5 * k) + f * (0.1 * (k % 2)); rod(reed_, q + V((0, 0, 0.1)), q + V((-0.25, 0.1, 3.4)), 0.38, M['hay'], seg=8); cyl(reed_, q + V((-0.07, 0.03, 1.1)), 0.4, 0.14, M['red_d'], seg=8, cap=False); cyl(reed_, q + V((-0.16, 0.06, 2.2)), 0.4, 0.14, M['red_d'], seg=8, cap=False)
    elif kind == 'counter':
        cb = Bk2('fgcounter', hull=T.hull(3.0)); b0 = V((o.x, o.y, o.z - 1.6)); obox(cb, tuple(b0 + V((0, 0, 0.0))), (r.x, r.y, 0), (f.x, f.y, 0), (0, 0, 1), 1.3, 0.8, 0.1, M['planks'], uvk=0.4)
        cyl(cb, b0 + V((0, 0, 0.1)), 0.5, 0.2, M['straw_d'], seg=8, r1=0.4); ellipsoid(cb, b0 + V((0.8 * r.x, 0.8 * r.y, 0.65)), 0.42, 0.42, 0.5, M['clay'], seg=9, rings=6)
        rod(cb, b0 + V((-0.8 * r.x, -0.8 * r.y, 0.1)), b0 + V((-0.8 * r.x, -0.8 * r.y, 2.2)), 0.05, M['wood'], seg=4); rod(cb, b0 + V((-0.8 * r.x, -0.8 * r.y, 2.2)), b0 + V((-0.1 * r.x, -0.1 * r.y, 2.2)), 0.04, M['wood'], seg=4)
        for sgn in (-1, 1): rod(cb, b0 + V((-0.1 * r.x, -0.1 * r.y, 2.2)), b0 + V((-0.1 * r.x + sgn * 0.3 * r.x, -0.1 * r.y + sgn * 0.3 * r.y, 1.7)), 0.015, M['black'], seg=3); cyl(cb, b0 + V((-0.1 * r.x + sgn * 0.3 * r.x, -0.1 * r.y + sgn * 0.3 * r.y, 1.7)), 0.16, 0.05, M['bronze'], seg=8)
    elif kind == 'torch':
        b0 = V((o.x, o.y, o.z - 2.6)); tb = Bk2('fgtorch', hull=T.hull(3.0)); rod(tb, b0, b0 + V((0, 0, 3.2)), 0.1, M['wood_d'], seg=5); cyl(tb, b0 + V((0, 0, 3.0)), 0.3, 0.3, M['iron'], seg=8, r1=0.4)
        live_flame(b0 + V((0, 0, 3.4)), 1.3, 0.38, seed=77, n=3, light=0.0, name='fgtorch', warm=None)
    Bk2.flush(STATE['SET'])
    objs = [ob for ob in STATE['SET'].objects if ob not in n0]
    for ob in objs:                                                                            # scale the prop about its anchor so it takes about a fifth of the frame width
        if ob.type == 'MESH' and tuple(ob.location) == (0.0, 0.0, 0.0) and tuple(ob.scale) == (1.0, 1.0, 1.0): ob.data.transform(Matrix.Translation(o) @ Matrix.Scale(FGK, 4) @ Matrix.Translation(-o))
        else:
            ob.location = o + (V(ob.location) - o) * FGK; ob.scale = tuple(x * FGK for x in ob.scale)
            for fi in STATE['fires']:
                if fi['ob'] is ob: fi['k'] = FGK
        no_bounce(ob); ob.parent = cam; ob.matrix_parent_inverse = cam.matrix_world.inverted()
    STATE.setdefault('fg_objs', []).extend(objs); return objs

# ----------------------------------------------------------------------------- placeholder cards at the marks (stills / contact sheet only; the render teams add the real puppets)
def placeholders(name, t=0.5, herd_max=80):
    """Flat placeholder silhouettes at the shot's stand marks (people with their HEIGHT, ox cards 2.6 D, herd ox cards), turned to the camera at pose t. Named ph_*; remove with clear_placeholders()."""
    clear_placeholders(); sh = S.SHOTS[name]; marks = S.marks_for(name); M = STATE['M']; pose = S.pose_at(sh, 0.0); cam = V(pose['loc']); Bk2 = Banks(); k = 0
    cols = dict(tiandan=(M['wood_l'], M['black']), general=(M['lacq'], M['red']), soldier=(M['black'], M['red_d']), townsfolk=(M['hide'], M['black']), child=(M['jade'], M['black']), envoy=(M['cream'], M['black']), qi_soldier=(M['indigo'], M['black']), sentry=(M['black'], M['red_d']))
    def person(m, role):
        h = HEIGHT.get(role, 3.0); p = V(m[:3]); yaw = m[3] if len(m) > 3 else 0.0; F = Frame(p, yaw); b = Bk2('ph_%s_%d' % (role, k)); robe, cap = cols.get(role, (M['black'], M['black'])); w = 0.42 * h
        b.face([F.p(-w, 0, 0), F.p(w, 0, 0), F.p(w * 0.7, 0, h * 0.72), F.p(-w * 0.7, 0, h * 0.72)], robe, [(0, 0)] * 4); b.face([F.p(-w, 0, 0)] [:0] or [F.p(w, 0, 0), F.p(-w, 0, 0), F.p(-w * 0.7, 0, h * 0.72), F.p(w * 0.7, 0, h * 0.72)], robe, [(0, 0)] * 4)
        hc = F.p(0, 0, h - 0.5); n = 10
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; q = [hc, hc + F.X * (0.5 * math.cos(a0)) + F.Z * (0.5 * math.sin(a0)), hc + F.X * (0.5 * math.cos(a1)) + F.Z * (0.5 * math.sin(a1))]
            b.face(q, M['skin'], [(0, 0)] * 3); b.face(q[::-1], M['skin'], [(0, 0)] * 3)
        b.face([F.p(-0.5, 0, h - 0.4), F.p(0.5, 0, h - 0.4), F.p(0.4, 0, h + 0.05), F.p(-0.4, 0, h + 0.05)], cap, [(0, 0)] * 4); b.face([F.p(0.5, 0, h - 0.4), F.p(-0.5, 0, h - 0.4), F.p(-0.4, 0, h + 0.05), F.p(0.4, 0, h + 0.05)], cap, [(0, 0)] * 4)
    def ox(m):
        p = V(m[:3]); yaw = m[3] if len(m) > 3 else 0.0; sc = m[4] if len(m) > 4 else 1.0; F = Frame(p, yaw); b = Bk2('ph_ox_%d' % k); P = lambda x, z: F.p(x * sc, 0, z * sc)
        polys = [([(-2.0, 1.0), (1.7, 1.0), (1.9, 2.5), (-1.9, 2.6)], M['red']), ([(-1.8, 0), (-1.3, 0), (-1.2, 1.1), (-1.8, 1.1)], M['ox_d']), ([(1.2, 0), (1.7, 0), (1.7, 1.1), (1.2, 1.1)], M['ox_d']), ([(1.7, 1.5), (2.8, 1.4), (2.9, 2.3), (1.9, 2.6)], M['ox']),
                 ([(2.2, 2.3), (2.7, 3.2), (2.9, 3.1), (2.5, 2.2)], M['steel']), ([(-1.9, 2.3), (-2.9, 3.4), (-2.6, 3.5), (-1.7, 2.6)], M['gold'])]
        for pts_, mat in polys:
            q = [P(x, z) for x, z in pts_]; b.face(q, mat, [(0, 0)] * len(q)); b.face(q[::-1], mat, [(0, 0)] * len(q))
    for role, lst in marks.items():
        for m in lst[:herd_max if role.startswith('herd') else 12]:
            if role == 'ox' or role.startswith('herd'): ox(m)
            elif role in HEIGHT or role in cols: person(m, role)
            k += 1
    Bk2.flush(STATE['SET'])
    for ob in STATE['SET'].objects:
        if ob.name.startswith('ph_'): no_bounce(ob); ob['placeholder'] = 1

def clear_placeholders():
    for ob in [o for o in bpy.data.objects if o.name.startswith('ph_')]: bpy.data.objects.remove(ob, do_unlink=True)

# ----------------------------------------------------------------------------- shot cameras
def _look_rot(loc, look, prev=None):
    q = (V(look) - V(loc)).normalized().to_track_quat('-Z', 'Y'); return q.to_euler('XYZ', prev) if prev is not None else q.to_euler()

def shot_camera(name, t=0.0, fg=True):
    """Pose the scene camera for shot `name` at t = 0..1 of the move (not keyed). Builds the shot's foreground prop the first time (parented to the camera)."""
    sh = S.SHOTS[name]; pose = S.pose_at(sh, t); first = 'cam' not in bpy.data.objects
    cam = make_camera(S.pose_at(sh, 0.0) if first else pose)
    if first or not STATE.get('fg_shot') == name:
        for ob in STATE.get('fg_objs', []): bpy.data.objects.remove(ob, do_unlink=True)
        STATE['fg_objs'] = []; cam.location = S.pose_at(sh, 0.0)['loc']; cam.rotation_euler = _look_rot(S.pose_at(sh, 0.0)['loc'], S.pose_at(sh, 0.0)['look_at']); bpy.context.view_layer.update()
        if fg: attach_fg(cam, S.pose_at(sh, 0.0), sh['fg'])
        STATE['fg_shot'] = name
    cam.location = pose['loc']; cam.rotation_euler = _look_rot(pose['loc'], pose['look_at']); cam.data.lens = pose['lens']; _sky_follow(bpy.context.scene); bpy.context.view_layer.update(); return cam

def key_camera(name, f0=None):
    """Key the whole shot's camera move (one LINEAR key per frame from f0, default the shot's first frame of the film)."""
    sh = S.SHOTS[name]; f0 = sh['f0'] if f0 is None else f0; cam = shot_camera(name, 0.0); prev = None
    for i in range(sh['frames'] + 1):
        pose = S.pose_at(sh, i / max(1, sh['frames'])); prev = cam.rotation_euler = _look_rot(pose['loc'], pose['look_at'], prev); cam.location = pose['loc']; cam.data.lens = pose['lens']
        cam.keyframe_insert('location', frame=f0 + i); cam.keyframe_insert('rotation_euler', frame=f0 + i); cam.data.keyframe_insert('lens', frame=f0 + i)
    for fc in T._fcurves(cam):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    return cam

def head_rows(name, ts=(0.0, 0.5, 1.0)):
    """[(role, t, mark, head_top_y, chin_y, feet_y)] in px of the 720x1280 frame for every stand mark of shot `name` (caption rule: chin (head bottom) < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sh = S.SHOTS[name]; marks = S.marks_for(name); sc = bpy.context.scene; out = []
    for t in ts:
        cam = shot_camera(name, t, fg=False)
        for role, lst in marks.items():
            if role not in HEIGHT: continue
            for m in lst[:12]:
                h = HEIGHT[role]; p = V(m[:3]); top, chin, feet = V((p.x, p.y, p.z + h)), V((p.x, p.y, p.z + h - 1.0)), p
                a, b, c = (world_to_camera_view(sc, cam, v) for v in (top, chin, feet))
                if a.z <= 0: continue
                out.append((role, t, tuple(round(x, 1) for x in m[:3]), round((1 - a.y) * 1280), round((1 - b.y) * 1280), round((1 - c.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def digest():
    import hashlib
    h = hashlib.sha1()
    for ob in sorted(bpy.data.objects, key=lambda o: o.name):
        h.update(ob.name.encode()); h.update(('%.3f' * 3 % tuple(ob.matrix_world.translation)).encode())
        if ob.type == 'MESH': h.update(str(len(ob.data.vertices)).encode()); h.update(('%.3f' % sum(v.co.x + 2 * v.co.y + 3 * v.co.z for v in ob.data.vertices)).encode())
        if ob.type == 'LIGHT': h.update(('%.2f' % ob.data.energy).encode())
    return h.hexdigest()[:16]

def wall_polys(loc):
    """Projected cells of the visible wall face (outer for jimo_out / yan_camp, inner for jimo_in) in 720x1280 px: [[(x, y) x4]] (occlusion is NOT tested; the hue / edge numbers use it as the wall region)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; fy = yi if loc == 'jimo_in' else yo; out = []
    for x in np.arange(-95.0, 95.0, 5.0):
        for z in np.arange(0.5, 15.5, 2.0):
            if any(abs(x + 2.5 - hc) < hw / 2 + 1 and z < hh + 1 for hc, hw, hh in STATE['holes'] if hh > 9): continue
            q = [world_to_camera_view(sc, cam, V((x + dx, fy(z + dz), z + dz))) for dx, dz in ((0, 0), (5, 0), (5, 2), (0, 2))]
            if any(p.z <= 0.1 for p in q): continue
            P_ = [(p.x * 720, (1 - p.y) * 1280) for p in q]
            if max(p[0] for p in P_) < 0 or min(p[0] for p in P_) > 720 or max(p[1] for p in P_) < 0 or min(p[1] for p in P_) > 1280: continue
            out.append([(round(a, 1), round(b, 1)) for a, b in P_])
    return out

def write_meta(spec):
    name, t, light, state = parse_spec(spec); A = build(None, name, light); sh = S.SHOTS[name]; apply_state(state if state is not None else sh['state']); shot_camera(name, t); bpy.context.view_layer.update()
    meta = dict(shot=name, loc=sh['loc'], light=A['light'], t=t, state=sh['state'], heads=head_rows(name), wall=wall_polys(sh['loc']) if sh['loc'] != 'vista' else [])
    json.dump(meta, open(os.path.join(WORK, 'final', name + '.json'), 'w')); print('meta', name, len(meta['wall']), 'wall cells', len(meta['heads']), 'head rows', flush=True)

def parse_spec(spec):
    """'s16' | 's16@0.5' | 's16:NIGHT' | 's16@0.5:NIGHT:h6' | 'jimo_in' (location default, 'wide' camera)."""
    parts = spec.split(':'); head = parts[0]; t = 0.5
    if '@' in head: head, ts = head.split('@'); t = float(ts)
    return head, t, (parts[1] if len(parts) > 1 and parts[1] else None), (parts[2] if len(parts) > 2 else None)

def render_spec(spec, quality='final', outdir=None, tag=None):
    name, t, light, state = parse_spec(spec); outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True)
    A = build(None if name in S.SHOTS else name, name, light); sc = bpy.context.scene; MN.setup_render(sc, quality); sc.render.threads = 2
    st = state if state is not None else (S.SHOTS[name]['state'] if name in S.SHOTS else ''); apply_state(st)
    if name in S.SHOTS:
        shot_camera(name, t)
        if os.environ.get('ACTORS', '1') == '1': R2.placeholders(name, t)
    else: make_camera(A['cam'])
    bpy.context.view_layer.update(); flicker(1 if name not in S.SHOTS else S.SHOTS[name]['f0'] + int(t * S.SHOTS[name]['frames']))
    tag = tag or ('%s' % name + ('' if light is None else '_' + light))
    w, c = T.render(os.path.join(outdir, tag + '.png'))
    hr = head_rows(name, (t,)) if name in S.SHOTS else []
    print('%s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, w, c, _load(), [(r[0], r[4]) for r in hr][:6]), flush=True)
    return dict(tag=tag, wall=round(w, 1), cpu=round(c, 1), heads=hr)

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('stills', 'final'):
        specs = arg or list(S.SHOTS)
        for sp in specs: render_spec(sp, 'final' if cmd == 'final' else 'preview')
    elif cmd == 'digest':
        name, t, light, state = parse_spec(arg[0] if arg else 's01'); A = build(None if name in S.SHOTS else name, name, light); bpy.context.view_layer.update(); print('digest', digest())
    elif cmd == 'meta':
        for sp in (arg or list(S.SHOTS)): write_meta(sp)
    elif cmd == 'contact':
        import jimo_sheet; jimo_sheet.run(arg)
    else: print(__doc__)
