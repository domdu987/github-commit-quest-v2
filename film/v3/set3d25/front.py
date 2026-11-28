#!/usr/bin/env python3
"""front.py : set of film 25 (Britain's first tank, the Mark I, Flers-Courcelette, 15 Sep 1916, Somme).  bpy 5.x, Cycles CPU, PATH TRACED, LIGHT_SPEC v2 look
(bright golden-hour sun, strong sky fill, textured materials, crisp native 720x1280).  Characters are 2D puppet cards (emission to camera rays only, cast shadows).

    import front as F
    A = F.build('cross_hero')            # builds the scene for a preset, returns anchors
    F.render_still(path)                 # 720x1280 native + post (unsharp)
CLI:  python3 front.py render cross_hero out.png [--draft 0.4] [--samples 64]
World: 1 unit = 1 D (head, ~0.53 m), z up.  See API.md."""
import os, sys, math, json, time, random, hashlib, subprocess, copy
import numpy as np
import bpy
from PIL import Image
from mathutils import Vector, Matrix, Euler
if __name__ == '__main__': sys.modules['front'] = sys.modules['__main__']          # lib25 / tank25 do `import front`

HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d24'), os.path.join(PROJ, 'v3', 'kit')):
    if p not in sys.path: sys.path.insert(0, p)
import joseon as J                                          # noqa: E402  (NB node helper, MB mesh helpers, tower card material) -- not edited
T = J.T; MB = T.MB; hexl = T.hex_lin; NB = J.NB
TEX = os.path.join(HERE, 'tex'); ACT = os.path.join(HERE, 'actors')
S = {}
OVR = {}
def rnd(seed): return random.Random(seed)
def V(*a): return Vector(a)
def sstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)

# ============================================================================= materials
def _img(key, cs='sRGB'):
    p = os.path.join(TEX, key + '.jpg'); im = bpy.data.images.load(p, check_existing=True); im.colorspace_settings.name = cs; return im

def fmat(name, build):
    return J.mat('F_' + name, build)

def pbr(name, key, size=2.0, tint=None, sat=1.0, val=1.0, rough=None, bump=0.4, bump_dist=0.05, metal=0.0, coord='Object', blend=0.25, mul=None, extra=None):
    """Textured PBR (ambientCG CC0 colour + height -> bump + roughness) with box projection in object (or world) space; `size` = tile size in D."""
    def f(b):
        mp = b.n('ShaderNodeMapping'); s = 1.0 / size; mp.inputs['Scale'].default_value = (s, s, s); b.l(b.coord(coord), mp.inputs['Vector'])
        def tx(suffix, cs):
            t = b.n('ShaderNodeTexImage'); t.image = _img(key + suffix, cs); t.projection = 'BOX'; t.projection_blend = blend; t.extension = 'REPEAT'; b.l(mp.outputs[0], t.inputs['Vector']); return t
        col = tx('_c', 'sRGB').outputs['Color']
        if tint: col = b.mul(col, (*hexl(tint), 1))
        if sat != 1.0 or val != 1.0:
            h = b.n('ShaderNodeHueSaturation'); h.inputs['Saturation'].default_value = sat; h.inputs['Value'].default_value = val; b.l(col, h.inputs['Color']); col = h.outputs['Color']
        if extra: col = extra(b, col)
        ht = tx('_h', 'Non-Color').outputs['Color']; nrm = b.bump(ht, bump, bump_dist)
        r = rough if rough is not None else tx('_r', 'Non-Color').outputs['Color']
        b.princ(col, r, metal, nrm)
    return fmat(name, f)

def flat(name, hexcol, rough=0.7, metal=0.0, **kw):
    def f(b): b.princ(hexl(hexcol), rough, metal, **kw)
    return fmat(name, f)

def wood_seam(name, tint='#c9a070', size=2.6, seam_scale=1.0, axis='X', bump=0.9, sat=1.0, val=1.0, mud=0.0, vertical=False):
    """Wood049 grain + vertical plank seams (wave bands along the object axis) -> dark gaps and a bump: plank revetments / duckboards / crates."""
    def f(b):
        c = b.coord(); mp = b.n('ShaderNodeMapping'); s = 1.0 / size; mp.inputs['Scale'].default_value = (s, s, s); b.l(c, mp.inputs['Vector'])
        if vertical: mp.inputs['Rotation'].default_value = (0.0, math.pi / 2, 0.0)
        def tx(suffix, cs):
            t = b.n('ShaderNodeTexImage'); t.image = _img('wood' + suffix, cs); t.projection = 'BOX'; t.projection_blend = 0.2; b.l(mp.outputs[0], t.inputs['Vector']); return t
        col = b.mul(tx('_c', 'sRGB').outputs['Color'], (*hexl(tint), 1))
        w = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction=axis, wave_profile='SAW'); w.inputs['Scale'].default_value = seam_scale / 0.62; w.inputs['Distortion'].default_value = 0.25
        b.l(c, w.inputs['Vector'])
        seam = b.rng(w.outputs['Fac'], 0.0, 0.05, 1.0, 0.0)                                    # 1 inside a seam, 0 on the board
        seam = b.math('SUBTRACT', 1.0, b.rng(w.outputs['Fac'], 0.0, 0.06, 0.0, 1.0))
        tone = b.noise(2.0, 2.0, 0.5, c, (0.7, 0.7, 0.7))                                       # board-to-board tone
        col = b.mul(col, b.mix(b.rng(tone, 0.3, 0.7), (0.78, 0.74, 0.7), (1.12, 1.08, 1.02)))
        col = b.mix(seam, col, (0.05, 0.035, 0.03))
        if mud:
            z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); m = b.rng(z.outputs['Z'], -mud, -mud + 1.6, 0.9, 0.0); col = b.mix(b.math('MULTIPLY', m, 0.7), col, (0.17, 0.11, 0.07))
        h = tx('_h', 'Non-Color').outputs['Color']; hh = b.math('SUBTRACT', b.math('MULTIPLY', h, 0.6), b.math('MULTIPLY', seam, 0.9))
        b.princ(col, 0.72, 0.0, b.bump(hh, bump, 0.08))
    return fmat(name, f)

def brick_mat(name, size=2.4, tint=None, sat=1.1, val=1.0, soot=0.0):
    def extra(b, col):
        if soot:
            n = b.noise(3.0, 3.0, 0.6, None, None); return b.mul(col, b.mix(b.rng(n, 0.35, 0.65), (1, 1, 1), (0.45, 0.42, 0.40)))
        return col
    return pbr(name, 'brick', size, tint, sat, val, None, 1.0, 0.06, extra=extra)

def tile_mat(name, c1='#d04a22', c2='#a8341c'):
    """Red clay roof tiles (procedural brick texture on the roof's UV plane: u along the eave, v up the slope)."""
    def f(b):
        uv = b.n('ShaderNodeUVMap').outputs[0]; br = b.n('ShaderNodeTexBrick'); br.offset = 0.5; br.offset_frequency = 2; br.squash = 1.0
        br.inputs['Color1'].default_value = (*hexl(c1), 1); br.inputs['Color2'].default_value = (*hexl(c2), 1); br.inputs['Mortar'].default_value = (0.12, 0.05, 0.04, 1)
        br.inputs['Scale'].default_value = 1.0; br.inputs['Mortar Size'].default_value = 0.035; br.inputs['Mortar Smooth'].default_value = 0.1; br.inputs['Bias'].default_value = 0.0
        br.inputs['Brick Width'].default_value = 0.62; br.inputs['Row Height'].default_value = 0.55; b.l(uv, br.inputs['Vector'])
        n = b.noise(6.0, 3.0, 0.55, None, None); col = b.mul(br.outputs['Color'], b.mix(b.rng(n, 0.3, 0.7), (0.82, 0.78, 0.74), (1.15, 1.1, 1.05)))
        hh = b.math('ADD', b.math('MULTIPLY', br.outputs['Fac'], 0.5), b.math('MULTIPLY', n, 0.25))
        b.princ(col, 0.6, 0.0, b.bump(hh, 1.2, 0.06))
    return fmat(name, f)

def make_materials():
    M = {}
    M['ground'] = ground_mat()
    M['brick'] = brick_mat('brick', 2.2, '#f8d4c0', 1.45, 1.02); M['brick_s'] = brick_mat('brick_s', 2.2, '#cdb8a8', 0.9, 0.9, soot=1.0)
    M['tile'] = tile_mat('tile'); M['tile_d'] = tile_mat('tile_d', '#b04a2a', '#8a3320')
    M['plaster'] = flat('plaster', '#e0d2b4', 0.9)
    M['rev'] = wood_seam('rev', '#e6bf88', 2.4, 1.0, 'X', 1.4, mud=3.6, vertical=True); M['rev_d'] = wood_seam('rev_d', '#c49a68', 2.4, 1.0, 'X', 1.4, mud=3.6, vertical=True)
    M['post'] = wood_seam('post', '#b98b58', 2.0, 0.0, 'X', 0.7); M['duck'] = wood_seam('duck', '#d2aa76', 1.6, 0.0, 'X', 0.8)
    M['crate'] = wood_seam('crate', '#bfa684', 1.6, 1.2, 'X', 0.9)
    M['beam'] = pbr('beam', 'wood', 1.8, '#b08850', 1.0, 0.85, 0.75, 0.6)
    def wattle(b):
        c = b.coord(); w1 = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction='Z', wave_profile='SIN'); w1.inputs['Scale'].default_value = 5.5; w1.inputs['Distortion'].default_value = 2.0; b.l(c, w1.inputs['Vector'])
        w2 = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X', wave_profile='SIN'); w2.inputs['Scale'].default_value = 7.0; w2.inputs['Distortion'].default_value = 1.5; b.l(c, w2.inputs['Vector'])
        h = b.math('MAXIMUM', w1.outputs['Fac'], w2.outputs['Fac']); col = b.mix(b.rng(h, 0.2, 0.9), (0.28, 0.19, 0.11), (0.78, 0.58, 0.34))
        b.princ(col, 0.85, 0.0, b.bump(h, 1.4, 0.07))
    M['wattle'] = fmat('wattle', wattle)
    def sandbag(b):
        c = b.coord(); mp = b.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 0.55,) * 3; b.l(c, mp.inputs['Vector'])
        t = b.n('ShaderNodeTexImage'); t.image = _img('burlap_c'); t.projection = 'BOX'; t.projection_blend = 0.3; b.l(mp.outputs[0], t.inputs['Vector'])
        hh = b.n('ShaderNodeTexImage'); hh.image = _img('burlap_h', 'Non-Color'); hh.projection = 'BOX'; hh.projection_blend = 0.3; b.l(mp.outputs[0], hh.inputs['Vector'])
        g = b.n('ShaderNodeRGBToBW'); b.l(t.outputs['Color'], g.inputs[0]); lum = b.rng(g.outputs[0], 0.2, 0.7, 0.55, 1.15)
        tone = b.noise(1.3, 2.0, 0.5, c, None); col = b.mix(b.rng(tone, 0.35, 0.65), (0.50, 0.34, 0.17), (0.38, 0.27, 0.14))
        col = b.mul(col, (lum, lum, lum, 1)) if False else col
        wv = b.noise(14.0, 2.0, 0.6, c, None); lumc = b.math('MULTIPLY', lum, 1.0)
        b.princ(b.mul(col, b.mix(b.rng(wv, 0.3, 0.7), (0.82, 0.8, 0.78), (1.15, 1.12, 1.08))), 0.96, 0.0, b.bump(b.math('ADD', hh.outputs['Color'], b.math('MULTIPLY', wv, 0.35)), 1.3, 0.04))
    M['sandbag'] = fmat('sandbag', sandbag)
    M['wire'] = flat('wire', '#55504c', 0.45, 0.8); M['stump'] = flat('stump', '#7a6a58', 0.9)
    M['rubble'] = pbr('rubble', 'brick', 1.0, '#e8cdb8', 0.9, 0.9, None, 1.2, 0.05)
    M['leaf'] = flat('leaf', '#4f8a3a', 0.8); M['leaf2'] = flat('leaf2', '#6aa040', 0.8); M['poplar'] = flat('poplar', '#5e9438', 0.85)
    M['trunk'] = flat('trunk', '#6a5a48', 0.9)
    M['water'] = water_mat()
    M['black'] = flat('black', '#16140f', 0.9); M['barrel'] = flat('barrel', '#7a5a38', 0.55, 0.5); M['chalk_rock'] = pbr('chalk_rock', 'chalk', 0.8, '#fbefd8', 1.0, 1.25, None, 1.0, 0.04)
    # ---- tank
    def camo(b):
        c = b.coord(); vv = b.n('ShaderNodeTexVoronoi', voronoi_dimensions='3D', feature='F1'); vv.inputs['Scale'].default_value = 0.40; vv.inputs['Randomness'].default_value = 1.0
        nz = b.noise(0.9, 3.0, 0.55, c, None); wp = b.n('ShaderNodeVectorMath', operation='ADD'); b.l(c, wp.inputs[0]); wv = b.n('ShaderNodeVectorMath', operation='SCALE'); wv.inputs['Scale'].default_value = 1.6
        nz3 = b.n('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 0.8; nz3.inputs['Detail'].default_value = 2.0; b.l(c, nz3.inputs['Vector']); b.l(nz3.outputs['Color'], wv.inputs[0]); b.l(wv.outputs[0], wp.inputs[1]); b.l(wp.outputs[0], vv.inputs['Vector'])
        ve = b.n('ShaderNodeTexVoronoi', voronoi_dimensions='3D', feature='DISTANCE_TO_EDGE'); ve.inputs['Scale'].default_value = 0.40; ve.inputs['Randomness'].default_value = 1.0; b.l(wp.outputs[0], ve.inputs['Vector'])
        g = b.n('ShaderNodeRGBToBW'); b.l(vv.outputs['Color'], g.inputs[0])
        ramp = b.n('ShaderNodeValToRGB'); cr = ramp.color_ramp; cr.interpolation = 'CONSTANT'
        pal = ['#c9993f', '#6f8a43', '#7e5230', '#bdb07c', '#c9993f']; cr.elements[0].position = 0.0; cr.elements[0].color = (*hexl(pal[0]), 1); cr.elements[1].position = 0.25; cr.elements[1].color = (*hexl(pal[1]), 1)
        for pos, cc in ((0.5, pal[2]), (0.75, pal[3])): e = cr.elements.new(pos); e.color = (*hexl(cc), 1)
        b.l(g.outputs[0], ramp.inputs['Fac'])
        edge = b.rng(ve.outputs['Distance'], 0.0, 0.035, 1.0, 0.0); col = b.mix(edge, ramp.outputs['Color'], (0.07, 0.06, 0.05))
        z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); mud = b.rng(z.outputs['Z'], 0.1, 1.5, 1.0, 0.0); dn = b.noise(5.0, 3.0, 0.6, c, None)
        col = b.mix(b.math('MULTIPLY', mud, b.rng(dn, 0.35, 0.7, 0.4, 1.0)), col, (0.22, 0.15, 0.09)); return col, edge, dn
    def hullm(b):
        col, edge, dn = camo(b); uv = b.n('ShaderNodeUVMap').outputs[0]; br = b.n('ShaderNodeTexBrick'); br.offset = 0.5; br.offset_frequency = 2; br.squash = 1.0
        br.inputs['Brick Width'].default_value = PLATE_W; br.inputs['Row Height'].default_value = PLATE_H; br.inputs['Mortar Size'].default_value = 0.035; br.inputs['Mortar Smooth'].default_value = 0.35; br.inputs['Scale'].default_value = 1.0
        br.inputs['Bias'].default_value = 0.0; br.inputs['Color1'].default_value = (1, 1, 1, 1); br.inputs['Color2'].default_value = (0.9, 0.9, 0.9, 1); br.inputs['Mortar'].default_value = (0.0, 0.0, 0.0, 1); b.l(uv, br.inputs['Vector'])
        seam = b.math('SUBTRACT', 1.0, br.outputs['Fac']); col = b.mul(col, b.mix(b.math('MULTIPLY', seam, 0.8), (1, 1, 1), (0.35, 0.33, 0.3)))
        nn = b.noise(18.0, 3.0, 0.6, None, None); h = b.math('ADD', b.math('MULTIPLY', br.outputs['Fac'], 0.7), b.math('MULTIPLY', nn, 0.08))
        b.princ(col, 0.55, 0.12, b.bump(h, 1.0, 0.06))
    M['hull'] = fmat('hull', hullm)
    def trackm(b):
        c = b.coord(); mp = b.n('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 1.5,) * 3; b.l(c, mp.inputs['Vector'])
        t = b.n('ShaderNodeTexImage'); t.image = _img('steel_c'); t.projection = 'BOX'; b.l(mp.outputs[0], t.inputs['Vector']); nn = b.noise(4.0, 3.0, 0.6, c, None)
        col = b.mul(t.outputs['Color'], (*hexl('#5b4a3a'), 1)); col = b.mix(b.rng(nn, 0.35, 0.65), col, (0.34, 0.2, 0.1))
        z = b.n('ShaderNodeSeparateXYZ'); b.l(c, z.inputs[0]); mud = b.rng(z.outputs['Z'], 0.2, 1.6, 1.0, 0.0); col = b.mix(b.math('MULTIPLY', mud, 0.85), col, (0.25, 0.17, 0.1))
        b.princ(col, 0.62, 0.55, b.bump(nn, 0.5, 0.05))
    M['track'] = fmat('track', trackm)
    M['rivet'] = flat('rivet', '#5b5249', 0.38, 0.75); M['steel'] = flat('steel', '#4a4e52', 0.4, 0.8); M['steel_l'] = flat('steel_l', '#6a6a60', 0.45, 0.6)
    M['gun'] = flat('gun', '#34352f', 0.35, 0.8); M['slit'] = flat('slit', '#0a0a0a', 0.9); M['wheel'] = pbr('wheel', 'wood', 1.2, '#7b5c3a', 1.0, 0.8, 0.75, 0.5)
    M['tirem'] = flat('tirem', '#3a3a3c', 0.5, 0.7)
    S['M'] = M; return M

PLATE_W, PLATE_H = 2.6, 2.0

def water_mat():
    def f(b):
        c = b.coord(); nn = b.noise(1.5, 3.0, 0.5, c, None)
        p = b.princ(b.mix(b.rng(nn, 0.3, 0.7), (0.07, 0.065, 0.05), (0.11, 0.10, 0.08)), 0.03, 0.0, b.bump(nn, 0.04, 0.02)); p.inputs['IOR'].default_value = 1.33
    return fmat('water', f)

def ground_mat():
    def f(b):
        c = b.coord(); w = b.n('ShaderNodeAttribute'); w.attribute_name = 'wet'; w.attribute_type = 'GEOMETRY'; wet = w.outputs['Fac']
        far = b.n('ShaderNodeAttribute'); far.attribute_name = 'far'; far.attribute_type = 'GEOMETRY'; fa = far.outputs['Fac']
        def tex(key, size, tint=None, sat=1.0, val=1.0, vec=None):
            mp = b.n('ShaderNodeMapping'); s = 1.0 / size; mp.inputs['Scale'].default_value = (s, s, s); b.l(vec if vec else c, mp.inputs['Vector'])
            def tx(suffix, cs):
                t = b.n('ShaderNodeTexImage'); t.image = _img(key + suffix, cs); t.projection = 'BOX'; t.projection_blend = 0.3; b.l(mp.outputs[0], t.inputs['Vector']); return t
            col = tx('_c', 'sRGB').outputs['Color']
            if tint: col = b.mul(col, (*hexl(tint), 1))
            if sat != 1.0 or val != 1.0:
                h = b.n('ShaderNodeHueSaturation'); h.inputs['Saturation'].default_value = sat; h.inputs['Value'].default_value = val; b.l(col, h.inputs['Color']); col = h.outputs['Color']
            return col, tx('_h', 'Non-Color').outputs['Color']
        cc, ch = tex('chalk', 3.6, '#f2e2c8', 0.92, 1.2); cc2, ch2 = tex('chalk', 11.0, '#f0e4d0', 0.9, 1.15); sd, sh = tex('sand', 5.0, '#e4cba0', 0.92, 1.05)
        mn = b.noise(0.10, 3.0, 0.5, c, None)
        dry = b.mix(b.rng(mn, 0.35, 0.65), cc, sd); dry = b.mix(0.35, dry, cc2); mv = b.noise(0.55, 3.0, 0.6, c, None); dry = b.mul(dry, b.mix(b.rng(mv, 0.3, 0.7), (0.62, 0.55, 0.48), (1.22, 1.18, 1.1)))
        mc, mh = tex('mud', 3.0, '#a07650', 1.1, 1.2)
        wetm = b.rng(wet, 0.25, 0.75, 0.0, 1.0)
        col = b.mix(wetm, dry, mc)
        gr = b.n('ShaderNodeAttribute'); gr.attribute_name = 'green'; gr.attribute_type = 'GEOMETRY'; gcol, gh_ = tex('grass', 2.4, '#d8e08a', 1.25, S.get('grass_val', 0.85)); gv = b.noise(0.6, 3.0, 0.6, c, None)
        gcol = b.mul(gcol, b.mix(b.rng(gv, 0.3, 0.7), (0.85, 0.9, 0.6), (1.35, 1.25, 0.8)))
        col = b.mix(b.rng(gr.outputs['Fac'], 0.25, 0.7), col, gcol)
        # distant fields: green-gold stripes fading in with the 'far' attribute
        st = b.n('ShaderNodeTexWave', wave_type='BANDS', bands_direction='X', wave_profile='SAW'); st.inputs['Scale'].default_value = 0.035; st.inputs['Distortion'].default_value = 3.0; b.l(c, st.inputs['Vector'])
        fn = b.noise(0.02, 2.0, 0.5, c, None); fld = b.mix(b.rng(fn, 0.35, 0.65), b.mix(b.rng(st.outputs['Fac'], 0.4, 0.6), (0.50, 0.66, 0.18), (0.80, 0.68, 0.26)), (0.34, 0.58, 0.16))
        col = b.mix(fa, col, fld)
        hgt = b.math('ADD', b.math('MULTIPLY', ch, 0.6), b.math('MULTIPLY', ch2, 0.4)); hgt = b.mix(wetm, hgt, mh)
        rough = b.rng(wetm, 0.0, 1.0, 0.92, 0.38); hgt = b.mix(b.rng(gr.outputs['Fac'], 0.25, 0.7), hgt, gh_) if False else hgt
        b.princ(col, rough, 0.0, b.bump(hgt, 0.7, 0.1))
    return fmat('ground', f)

# ============================================================================= terrain: heightfield with the German trench, craters, mounds
def axis(lo_f, hi_f, step, lo, hi, growth=1.07):
    xs = list(np.arange(lo_f, hi_f + 1e-6, step)); a = hi_f; st = step
    while a < hi: st *= growth; a += st; xs.append(a)
    a = lo_f; st = step
    while a > lo: st *= growth; a -= st; xs.insert(0, a)
    return np.array(xs)

def poly_dist(X, Y, P):
    """distance to the polyline P, side (+1 left of the direction of travel = west for a south->north line) and the along-length parameter"""
    d = np.full(X.shape, 1e9); side = np.zeros(X.shape); along = np.zeros(X.shape); acc = 0.0
    for (ax, ay), (bx, by) in zip(P[:-1], P[1:]):
        dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy; t = np.clip(((X - ax) * dx + (Y - ay) * dy) / L2, 0, 1); px, py = ax + t * dx, ay + t * dy
        dd = np.hypot(X - px, Y - py); cr = dx * (Y - ay) - dy * (X - ax); m = dd < d
        d = np.where(m, dd, d); side = np.where(m, np.sign(cr), side); along = np.where(m, acc + t * math.sqrt(L2), along)
        acc += math.sqrt(L2)
    return d, side, along

_NZ = None
def _noise_init():
    global _NZ
    r = rnd(5); _NZ = [(r.uniform(0.05, 0.5), r.uniform(0, 6.28), r.uniform(0, 6.28), r.uniform(0, 6.28), 1.0 / (1 + i * 0.5)) for i in range(14)]
def terrain_noise(X, Y):
    if _NZ is None: _noise_init()
    h = np.zeros_like(X)
    for k, a, b, ph, w in _NZ: h += w * np.sin(X * k * math.cos(a) + Y * k * math.sin(a) + ph) * np.sin(X * k * 0.7 * math.cos(b) - Y * k * 0.7 * math.sin(b) + ph * 1.7)
    return h

def ground_h0_raw(X, Y):
    """ground height before corridors / the tank: churned noise, craters, parapet / parados mounds, trenches (S['trenches']) with a batter wall that climbs to the local lip height"""
    far = sstep(18, 60, np.hypot(X * 0.4, Y - 5))
    h = terrain_noise(X, Y) * (0.14 + 0.1 * (1 - far)) + 0.05 * np.sin(X * 1.9 + Y * 1.3) * np.sin(Y * 2.1 - X * 0.7)
    tr_d = []
    for tr in S['trenches']:
        d, side, al = poly_dist(X, Y, tr['poly']); de = np.maximum(d, tr['hw'])
        h += np.where(side > 0, tr['mw'], tr['me']) * np.exp(-((de - 4.9) / 2.0) ** 2) * (1 - 0.25 * np.sin(al * 0.37) ** 2) * sstep(0.5, tr.get('taper', 7.0), al); tr_d.append(d)
    for (cx, cy, r, dep, wat) in S['craters']:
        rr = np.hypot(X - cx, Y - cy) / r; bowl = -dep * np.clip(1 - rr * rr, 0, 1) ** 0.8; rim = 0.22 * dep * np.exp(-((rr - 1.12) / 0.28) ** 2)
        h += bowl + rim
    for tr, d in zip(S['trenches'], tr_d):
        D, HF, HW = tr['depth'], tr['hf'], tr['hw']; t = np.clip((d - HF) / (HW - HF), 0, 1); wall = -D + (h + D) * t + terrain_noise(X * 2.3, Y * 2.3) * 0.05 * (1 - t)
        h = np.where(d < HW, wall, h)
    return h

def corridor_sv(c, X, Y):
    hx, hy = c['h']; dx, dy = X - c['o'][0], Y - c['o'][1]; return dx * hx + dy * hy, -dx * hy + dy * hx

def ground_h0(X, Y):
    """raw ground, then every corridor (a tank's lane: the ground across the lane equals the centre-line profile, so the tracks sit on it level, no noise under them)"""
    h = ground_h0_raw(X, Y)
    for c in S.get('corridors', []):
        s, v = corridor_sv(c, X, Y); w = (1 - sstep(c['flat'], c['blend'], np.abs(v))) * sstep(c['s0'] - 3, c['s0'], s) * (1 - sstep(c['s1'], c['s1'] + 3, s))
        if not np.any(w > 0): continue
        sc = np.clip(s, c['s0'] - 3, c['s1'] + 3); cx, cy = c['o'][0] + c['h'][0] * sc, c['o'][1] + c['h'][1] * sc; hc = ground_h0_raw(cx, cy) + c.get('dz', 0.0)
        h = h * (1 - w) + hc * w
    return h

def ground_h(X, Y):
    if S.get('flat'): return np.zeros_like(np.asarray(X, float)) + S.get('flat_z', 0.0)
    h = ground_h0(X, Y)
    tk = S.get('tank_crush')
    if tk is not None:
        c = tk(X, Y, h); h = np.where(c < 1e8, c, h)
    return h

def gh(x, y): return float(ground_h(np.array([x], float), np.array([y], float))[0])

def build_ground():
    xs = axis(-30, 32, 0.42, -230, 230, 1.09); ys = axis(-36, 26, 0.42, -150, 520, 1.09)
    X, Y = np.meshgrid(xs, ys); Z = ground_h(X, Y); ny, nx = X.shape
    wet = np.zeros_like(Z); grn = np.zeros_like(Z)
    for tr in S['trenches']:
        d, side, al = poly_dist(X, Y, tr['poly']); wet += np.where(d < tr['hf'] + 0.6, 1.0, 0.0); grn += np.exp(-((d - tr['hw'] - 0.9) / 1.3) ** 2) * 0.85 * (d > tr['hw'] - 0.3)
    for (cx, cy, r, dep, wat) in S['craters']:
        rr = np.hypot(X - cx, Y - cy) / r; wet += (1 - sstep(0.15, 0.95, rr)) * (0.5 + 0.5 * wat); grn += np.exp(-((rr - 1.25) / 0.35) ** 2) * 0.9
    nz = terrain_noise(X * 1.7 + 11, Y * 1.7 - 3); wet += np.clip((nz - 1.0) * 0.8, 0, 0.7) * (1 - sstep(25, 60, np.hypot(X, Y - 5)))
    for (cx, cy, rx, ry, ang) in S.get('mud_zones', []):
        c, s = math.cos(ang), math.sin(ang); u = ((X - cx) * c + (Y - cy) * s) / rx; v = (-(X - cx) * s + (Y - cy) * c) / ry; wet += np.exp(-(u * u + v * v) * 2.0) * 0.9
    tkc = S.get('tank_wet')
    if tkc is not None: wet += tkc(X, Y)
    wet = np.clip(wet, 0, 1); far = sstep(S.get('far0', 55), S.get('far1', 140), np.hypot(X * 0.9, Y - 8))
    gn = terrain_noise(X * 0.35 + 3, Y * 0.35 - 7); grn += np.clip((gn - 0.15) * S.get('green_k', 0.9), 0, 0.9) * (1 - sstep(0, 1, wet)); grn = np.clip(grn * (1 - wet), 0, 1)
    if S.get('all_green'): grn = np.clip(np.ones_like(Z) * (1 - wet) * (1 - sstep(0, 1, np.zeros_like(Z))), 0, 1)
    tkg = S.get('tank_green')
    verts = np.stack([X, Y, Z], -1).reshape(-1, 3); idx = np.arange(nx * ny).reshape(ny, nx); f = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
    me = bpy.data.meshes.new('ground'); me.from_pydata(verts.tolist(), [], f.tolist()); me.update()
    for nm, arr in (('wet', wet), ('far', far), ('green', grn)):
        at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr.reshape(-1).astype(np.float32))
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); me.materials.append(S['M']['ground'])
    ob = bpy.data.objects.new('ground', me); S['coll'].objects.link(ob); S['ground_ob'] = ob; return ob

# ============================================================================= mesh helpers
def mkobj(mb, name, parent=None, loc=None, rot=None, smooth=False, shadow=True, coll=None):
    o = mb.obj(name, coll or S['coll'], smooth=smooth)
    if parent is not None: o.parent = parent
    if loc is not None: o.location = loc
    if rot is not None: o.rotation_euler = rot
    if not shadow: o.visible_shadow = False
    return o

def empty(name, parent=None, loc=(0, 0, 0), rot=None):
    o = bpy.data.objects.new(name, None); S['coll'].objects.link(o); o.location = loc
    if rot is not None: o.rotation_euler = rot
    if parent is not None: o.parent = parent
    return o

def poly_face(mb, pts, mat, n_hint=None, uvmode=None, uvscale=1.0):
    """planar polygon with outward normal n_hint (flips winding) and a box-style UV (drops the dominant axis) so the plate seams of the hull material are world-aligned"""
    pts = [Vector(p) for p in pts]; nrm = Vector((0, 0, 0))
    for i in range(len(pts)): nrm += pts[i].cross(pts[(i + 1) % len(pts)])
    if n_hint is not None and nrm.dot(Vector(n_hint)) < 0: pts = pts[::-1]; nrm = -nrm
    a = [abs(nrm.x), abs(nrm.y), abs(nrm.z)]; ax = a.index(max(a))
    uv = [((p.y, p.z) if ax == 0 else (p.x, p.z) if ax == 1 else (p.x, p.y)) for p in pts]; uv = [(u * uvscale, v * uvscale) for u, v in uv]
    mb.pid += 1; mb.face(pts, mat, uv)

def obox(mb, c, X, Y, Z, hx, hy, hz, m): J.obox(mb, c, X, Y, Z, hx, hy, hz, m)
def beam(mb, p0, p1, w, h, m, up=(0, 0, 1)): J.beam(mb, p0, p1, w, h, m, up)
def rod(mb, p0, p1, r, m, seg=8, r1=None): mb.frustum(p0, p1, r, r if r1 is None else r1, m, seg=seg)
def ell(mb, c, rx, ry, rz, m, seg=12, rings=8, axes=None): J.ell(mb, c, rx, ry, rz, m, seg, rings, axes)
def rot_axes(yaw=0.0, pitch=0.0, roll=0.0):
    M = Euler((roll, pitch, yaw), 'XYZ').to_matrix(); return M.col[0].copy(), M.col[1].copy(), M.col[2].copy()

# ============================================================================= the German trench
def trench_segments(tr=None):
    P = (tr or S['trenches'][0])['poly']; return list(zip(P[:-1], P[1:]))

def build_trench(tr=None, tag=''):
    """Zig-zag trench: per straight bay a revetment panel on each wall (vertical planks or wattle) that climbs to the local lip, posts and wales, duckboards on rails."""
    tr = tr or S['trenches'][0]; M = S['M']; D = tr['depth']; HF, HW = tr['hf'], tr['hw']
    for i, ((ax, ay), (bx, by)) in enumerate(trench_segments(tr)):
        dx, dy = bx - ax, by - ay; L = math.hypot(dx, dy); yaw = math.atan2(dy, dx); ex, ey = dx / L, dy / L; nx_, ny_ = -ey, ex
        ext = 2.4; wmat = M['rev'] if i % 3 != 1 else M['wattle']; wmat2 = M['rev_d'] if i % 3 != 2 else M['wattle']
        for sd, sg in (('L', 1), ('R', -1)):
            mb = MB(); m = wmat if sg > 0 else wmat2; yb, yt = HF - 0.08, HW - 0.13; zb = -D + 0.02
            def top(t): return gh(ax + ex * t + nx_ * sg * (HW + 0.2), ay + ey * t + ny_ * sg * (HW + 0.2)) - 0.14
            n = max(2, int((L + 2 * ext) / 1.1)); ts = [-ext + k * (L + 2 * ext) / n for k in range(n + 1)]; tops = [top(t) for t in ts]; tm = max(tops)
            for k in range(n):
                q = [(ts[k], sg * yb, zb), (ts[k + 1], sg * yb, zb), (ts[k + 1], sg * yt, tops[k + 1]), (ts[k], sg * yt, tops[k])]
                poly_face(mb, q, m, (0, -sg, 0.0))
            for k in range(int(L // 3.4) + 1):                       # posts every 3.4 D, proud of the planks, up to the lip
                tt = 1.0 + k * 3.4
                if tt > L - 0.3: break
                tp = top(tt); pp = []
                for tx_ in (tt - 0.16, tt + 0.16):
                    for z_ in (zb, tp + 0.0): pp.append((tx_, sg * (yb + (yt - yb) * (z_ - zb) / (tp - zb)) - sg * 0.17, z_))
                poly_face(mb, [pp[0], pp[2], pp[3], pp[1]], M['beam'], (0, -sg, 0))
                for sx_ in (-0.16, 0.16):
                    poly_face(mb, [(tt + sx_, sg * (yb + (yt - yb) * 0.0) - sg * 0.17, zb), (tt + sx_, sg * yb, zb), (tt + sx_, sg * yt, tp), (tt + sx_, sg * (yt) - sg * 0.17, tp)], M['beam'], (sx_, 0, 0))
            for zz in (-1.0, -2.6, -3.9):                            # wales across the planks
                inw = sg * (yb + (yt - yb) * (zz - zb) / (tm - zb)) - sg * 0.2
                poly_face(mb, [(ts[0], inw, zz - 0.12), (ts[-1], inw, zz - 0.12), (ts[-1], inw, zz + 0.12), (ts[0], inw, zz + 0.12)], M['beam'], (0, -sg, 0))
            mkobj(mb, 'rev%s_%d%s' % (tag, i, sd), loc=(ax, ay, 0), rot=(0, 0, yaw))
        mb = MB(); zf = -D + 0.18                                    # duckboards: two rails + slats along the bay
        for rr in (-1.25, 1.25): mb.box((0.0, rr - 0.10, zf - 0.02), (L, rr + 0.10, zf + 0.10), M['beam'])
        for k in range(int(L / 0.52)):
            u = 0.15 + k * 0.52; mb.box((u, -1.6, zf + 0.10), (u + 0.40, 1.6, zf + 0.17), M['duck'])
        mkobj(mb, 'duck%s_%d' % (tag, i), loc=(ax, ay, 0), rot=(0, 0, yaw))

def sandbag_row(mb, p0, p1, z_of, layers=3, size=(0.95, 0.5, 0.32), seed=1, skip=None, lean=0.0):
    r = rnd(seed); p0, p1 = Vector(p0), Vector(p1); dvec = p1 - p0; L = dvec.length; e = dvec / L; nrm = Vector((-e.y, e.x, 0)); n = int(L / (size[0] * 0.92)); yaw = math.atan2(e.y, e.x)
    for layer in range(layers):
        for k in range(n):
            t = (k + 0.5 + (0.5 if layer % 2 else 0.0)) * size[0] * 0.92
            if t > L: continue
            c = p0 + e * t + nrm * r.uniform(-0.06, 0.06) + nrm * lean * layer * 0.12
            if skip and skip(c.x, c.y): continue
            z = z_of(c.x, c.y) + size[2] * 0.5 + layer * size[2] * 0.86
            X, Y, Z = rot_axes(yaw + r.uniform(-0.08, 0.08), r.uniform(-0.05, 0.05), r.uniform(-0.05, 0.05))
            ell(mb, (c.x, c.y, z), size[0] * 0.5 * r.uniform(0.93, 1.05), size[1] * 0.5 * r.uniform(0.92, 1.08), size[2] * 0.5 * r.uniform(0.95, 1.1), S['M']['sandbag'], 10, 6, (X, Y, Z))

def build_sandbags():
    M = S['M']; mb = MB(); crushed = S.get('in_tank', lambda x, y: False)
    for ti, tr in enumerate(S['trenches']):
        if not tr.get('sandbags', True): continue
        HW = tr['hw']; P = tr['poly']; lw, le = tr.get('sb_layers', (3, 2))
        for (a, b) in zip(P[:-1], P[1:]):
            a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0)); e = (b - a).normalized(); nrm = Vector((-e.y, e.x, 0)); off = nrm * (HW + 0.55)
            if lw: sandbag_row(mb, a + off - e * 0.6, b + off + e * 0.6, lambda x, y: gh(x, y), lw, seed=int(a.y * 7) + 3 + ti, skip=lambda x, y: crushed(x, y))
        for (a, b) in zip(P[:-1], P[1:]):
            a, b = Vector((a[0], a[1], 0)), Vector((b[0], b[1], 0)); e = (b - a).normalized(); nrm = Vector((e.y, -e.x, 0)); off = nrm * (HW + 0.7)
            if le: sandbag_row(mb, a + off, b + off, lambda x, y: gh(x, y), le, seed=int(a.y * 5) + 9 + ti, skip=lambda x, y: crushed(x, y) or y < S.get('parados_y0', -9.0))
    r = rnd(77)
    for (cx, cy, rad, n) in S.get('spill', []):
        for i in range(n):
            a = r.uniform(0, 6.28); rr = r.uniform(0.6, rad); x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
            if crushed(x, y): continue
            z = gh(x, y); X, Y, Z = rot_axes(r.uniform(0, 6.28), r.uniform(-0.5, 0.5), r.uniform(-0.6, 0.6))
            ell(mb, (x, y, max(z, -S['trenches'][0]['depth'] + 0.3) + 0.22), 0.47, 0.26, 0.19, M['sandbag'], 10, 6, (X, Y, Z))
    mkobj(mb, 'sandbags', smooth=True)

# ============================================================================= barbed wire
def wire_tube(mb, pts, r=0.032, seg=4):
    for a, b in zip(pts[:-1], pts[1:]):
        if (Vector(a) - Vector(b)).length > 1e-4: mb.frustum(a, b, r, r, S['M']['wire'], seg=seg, cap0=False, cap1=False)

def barb(mb, p, r_, rr):
    d = Vector((r_.uniform(-1, 1), r_.uniform(-1, 1), r_.uniform(-1, 1))).normalized() * 0.13; p = Vector(p)
    mb.frustum(p - d, p + d, 0.018, 0.018, S['M']['wire'], seg=3, cap0=False, cap1=False)
    e = d.cross(Vector((0, 0, 1))).normalized() * 0.1 if d.cross(Vector((0, 0, 1))).length > 1e-3 else Vector((0.1, 0, 0))
    mb.frustum(p - e, p + e, 0.018, 0.018, S['M']['wire'], seg=3, cap0=False, cap1=False)

def strand(mb, p0, p1, sag, seed, twist=0.035, barbs=0.42, flat=False):
    r = rnd(seed); p0, p1 = Vector(p0), Vector(p1); L = (p1 - p0).length; n = max(4, int(L / 0.22)); pts = []; bp = []
    e = (p1 - p0).normalized(); side = e.cross(Vector((0, 0, 1))).normalized() if abs(e.z) < 0.99 else Vector((1, 0, 0)); up = side.cross(e)
    for i in range(n + 1):
        t = i / n; p = p0 + (p1 - p0) * t; p.z -= 4 * sag * t * (1 - t); ph = t * L * 5.5
        if flat: p.z = max(p.z, gh(p.x, p.y) + 0.05)
        p = p + side * math.cos(ph) * twist + up * math.sin(ph) * twist; pts.append(p)
    wire_tube(mb, pts)
    for i in range(1, n, max(1, int(barbs / (L / n)))): barb(mb, pts[i], r, 0)

def coil(mb, c, axis_dir, length, R, turns, seed, squash=1.0):
    """concertina / tangle of helical wire, optionally squashed flat (R in the z direction x squash)"""
    r = rnd(seed); c = Vector(c); e = Vector(axis_dir).normalized(); side = e.cross(Vector((0, 0, 1))).normalized(); up = side.cross(e); n = int(turns * 12); pts = []
    for i in range(n + 1):
        t = i / n; a = t * turns * 2 * math.pi; rr = R * (1 + 0.12 * math.sin(t * 17 + seed))
        p = c + e * (t - 0.5) * length + side * math.cos(a) * rr + up * math.sin(a) * rr * squash; p.z = max(p.z, gh(p.x, p.y) + 0.04); pts.append(p)
    wire_tube(mb, pts, 0.03)
    for i in range(2, n, 7): barb(mb, pts[i], r, 0)

def build_wire():
    """Entanglement belt on pickets west of the trench (British approach), crushed flat in the lane the tank came through."""
    M = S['M']; mb = MB(); mp = MB(); r = rnd(31); crushed = S.get('in_tank_wide', lambda x, y: False)
    belts = S['wire_belts']
    for (x0, y0, x1, y1, rows) in belts:
        n = max(2, int(math.hypot(x1 - x0, y1 - y0) / 2.6))
        for row in range(rows):
            off = row * 2.4
            pts = []
            for i in range(n + 1):
                t = i / n; x = x0 + (x1 - x0) * t - off * 0.55 + (0.6 if i % 2 else -0.6) * 0.5 * (row % 2) + r.uniform(-0.15, 0.15); y = y0 + (y1 - y0) * t + off * 0.15 + r.uniform(-0.2, 0.2); pts.append((x, y))
            for i, (x, y) in enumerate(pts):
                z0 = gh(x, y)
                if crushed(x, y):                                    # pickets snapped and lying flat in random directions
                    a = r.uniform(0, 6.28); h = r.uniform(1.0, 1.9); X = Vector((math.cos(a), math.sin(a), r.uniform(0.05, 0.25))).normalized()
                    rod(mp, (x, y, z0 + 0.08), Vector((x, y, z0 + 0.08)) + X * h, 0.075, M['post'], 5)
                else:
                    h = 2.05 * r.uniform(0.92, 1.05); lean = Vector((r.uniform(-0.06, 0.06), r.uniform(-0.06, 0.06), 0)); rod(mp, (x, y, z0 - 0.1), Vector((x, y, z0 + h)) + lean, 0.085, M['post'], 5, 0.065)
            for i in range(n):
                (xa, ya), (xb, yb) = pts[i], pts[i + 1]; za, zb = gh(xa, ya), gh(xb, yb)
                ca, cb = crushed(xa, ya), crushed(xb, yb)
                if ca and cb:
                    strand(mb, (xa, ya, za + 0.06), (xb, yb, zb + 0.06), 0.0, r.randint(0, 99999), 0.07, 0.5, flat=True); continue
                if ca or cb: continue
                for hh_ in (0.5, 1.05, 1.6):
                    strand(mb, (xa, ya, za + hh_), (xb, yb, zb + hh_), 0.07, r.randint(0, 99999), 0.03, 0.5)
                strand(mb, (xa, ya, za + 0.5), (xb, yb, zb + 1.6), 0.05, r.randint(0, 99999), 0.03, 0.6)
                strand(mb, (xa, ya, za + 1.6), (xb, yb, zb + 0.5), 0.05, r.randint(0, 99999), 0.03, 0.6)
    for (cx, cy, ln, R, tn) in S.get('wire_coils', []):
        coil(mb, (cx, cy, gh(cx, cy) + 0.25), (math.cos(0.7), math.sin(0.7), 0), ln, R, tn, int(cx * 13 + cy), 0.12 if crushed(cx, cy) else 0.35)
    mkobj(mp, 'pickets'); mkobj(mb, 'wire')

# ============================================================================= village of Flers (ruins), stumps, poplars
def brick_wall(mb, x0, y0, x1, y1, z0, hfun, t=0.7, windows=(), m=None, m2=None):
    """straight wall along (x0,y0)->(x1,y1): columns of height hfun(s) (s 0..1 along), window holes (s0, s1, z0, z1) cut out"""
    m = m or S['M']['brick']; e = Vector((x1 - x0, y1 - y0, 0)); L = e.length; e.normalize(); nrm = Vector((-e.y, e.x, 0)); n = max(4, int(L / 0.9)); a0 = Vector((x0, y0, 0))
    for i in range(n):
        s0, s1 = i / n, (i + 1) / n; sm = (s0 + s1) / 2; h = hfun(sm)
        if h <= 0.01: continue
        pa = a0 + e * (L * s0); pb = a0 + e * (L * s1); cut = [w for w in windows if w[0] <= sm <= w[1]]
        segs = [(z0, z0 + h)]
        for w in cut:
            ns = []
            for (za, zb) in segs:
                if w[3] <= za or w[2] >= zb: ns.append((za, zb)); continue
                if w[2] > za: ns.append((za, w[2]))
                if w[3] < zb: ns.append((w[3], zb))
            segs = ns
        for (za, zb) in segs:
            c = (pa + pb) / 2; X, Y, Z = e, nrm, Vector((0, 0, 1)); zg = gh(c.x, c.y) - 0.45 if za <= z0 + 0.01 else None
            if zg is not None: za = zg; zb = max(zb, zg + 0.2)
            obox(mb, (c.x, c.y, (za + zb) / 2), X, Y, Z, (pb - pa).length / 2 + 0.005, t / 2, (zb - za) / 2, m)

def gable_roof(mb, c, W, Dp, z0, rise, yaw, holes, mt, seed):
    """red tile gable roof (ridge along the local x): two slopes, each a grid of slab panels; `holes` = list of (slope, u0, u1, v0, v1) in 0..1 left out"""
    r = rnd(seed); ex, ey = math.cos(yaw), math.sin(yaw); nx_, ny_ = -ey, ex; slope = math.atan2(rise, Dp / 2); nu, nv = 10, 5
    for sgn in (1, -1):
        for iu in range(nu):
            for iv in range(nv):
                u0, u1, v0, v1 = iu / nu, (iu + 1) / nu, iv / nv, (iv + 1) / nv
                if any(h[0] == sgn and h[1] <= (u0 + u1) / 2 <= h[2] and h[3] <= (v0 + v1) / 2 <= h[4] for h in holes): continue
                def P(u, v):
                    x = (u - 0.5) * W; y = sgn * (Dp / 2) * (1 - v) + sgn * 0.45 * 0 ; z = z0 + rise * v
                    return (c[0] + ex * x + nx_ * y, c[1] + ey * x + ny_ * y, z)
                pts = [P(u0, v0), P(u1, v0), P(u1, v1), P(u0, v1)]; nrm = (nx_ * sgn * math.sin(slope), ny_ * sgn * math.sin(slope), math.cos(slope)); mb.pid += 1
                q = [Vector(p) for p in pts]
                if (q[1] - q[0]).cross(q[3] - q[0]).dot(Vector(nrm)) < 0: pts = pts[::-1]; uvs = [(0, 1), (1, 1), (1, 0), (0, 0)][::-1]
                else: uvs = [(0, 0), (1, 0), (1, 1), (0, 1)]
                uvs = [(u * (W / 6.5) * 6.5 * 0.5 + 0.0, v * 5.0 * 0.5) for (u, v) in [((u0 + (u1 - u0) * a), (v0 + (v1 - v0) * b)) for a, b in ([(0, 0), (1, 0), (1, 1), (0, 1)] if uvs[0] == (0, 0) else [(0, 1), (1, 1), (1, 0), (0, 0)][::-1])]]
                mb.face(pts, mt, uvs)
    # rafters / purlins visible through the holes
    for k in range(9):
        u = (k + 0.5) / 9
        for sgn in (1, -1):
            xa = (u - 0.5) * W; p0 = (c[0] + ex * xa, c[1] + ey * xa, z0 + rise); p1 = (c[0] + ex * xa + nx_ * sgn * Dp / 2, c[1] + ey * xa + ny_ * sgn * Dp / 2, z0)
            if (any(h[0] == sgn and h[1] <= u <= h[2] for h in holes)): beam(mb, p0, p1, 0.14, 0.2, S['M']['beam'])
    beam(mb, (c[0] - ex * W / 2, c[1] - ey * W / 2, z0 + rise), (c[0] + ex * W / 2, c[1] + ey * W / 2, z0 + rise), 0.2, 0.24, S['M']['beam'])

def build_village():
    M = S['M']; r = rnd(17); mb = MB(); mr = MB(); mt = MB(); ms = MB()
    # farmhouse (red tile roof, holed): footprint 22 x 13 D at (cx, cy) yaw
    for (name, cx, cy, W, Dp, yaw, hole_seed) in S['houses']:
        ex, ey = math.cos(yaw), math.sin(yaw); nx_, ny_ = -ey, ex; wh = 8.0
        corners = [(-W / 2, -Dp / 2), (W / 2, -Dp / 2), (W / 2, Dp / 2), (-W / 2, Dp / 2)]
        def wp(u, v): return (cx + ex * u + nx_ * v, cy + ey * u + ny_ * v)
        rr = rnd(hole_seed)
        for i in range(4):
            (u0, v0), (u1, v1) = corners[i], corners[(i + 1) % 4]; a, b = wp(u0, v0), wp(u1, v1); horiz = (i % 2 == 0); Lw = math.hypot(b[0] - a[0], b[1] - a[1])
            if horiz:
                prof = lambda s, rr=rr: wh * (1.0 if (s < 0.35 or s > 0.7) else 0.35 + 0.5 * math.sin(s * 9)) if i == 0 else wh * (0.55 + 0.45 * abs(math.sin(s * 5.0)))
                wins = [(0.12, 0.2, 2.3, 5.3), (0.42, 0.52, 2.3, 5.3), (0.76, 0.84, 2.3, 5.3)]
            else:
                prof = lambda s, rr=rr: wh * (1.0 if s < 0.15 else 0.55 + 0.45 * abs(math.cos(s * 4.0 + 1)))
                wins = [(0.4, 0.55, 2.3, 5.3)]
            brick_wall(mb, a[0], a[1], b[0], b[1], 0.0, prof, 0.8, wins)
        holes = [(1, 0.25, 0.6, 0.2, 0.75), (-1, 0.62, 0.82, 0.3, 0.9), (1, 0.8, 0.95, 0.5, 1.0)]
        gable_roof(mt, (cx, cy), W + 1.4, Dp + 1.4, wh - 0.5, 4.4, yaw, holes, M['tile'], hole_seed)
        for k in range(9):                                            # rubble heap round the base
            a_ = rr.uniform(0, 6.28); rd = rr.uniform(0.5, 1.0) * (W / 2 + 2.5)
            lx, ly = wp(math.cos(a_) * rd * (1.0), math.sin(a_) * rd * 0.6)
    for (cx, cy, w, h, yaw) in S['towers']:                           # church tower stub: ragged top, arched louvre opening
        ex, ey = math.cos(yaw), math.sin(yaw)
        for (dx_, dy_, ln, ang) in ((0, w / 2, w, 0), (w / 2, 0, w, 1), (0, -w / 2, w, 0), (-w / 2, 0, w, 1)):
            p = (cx + ex * dx_ - ey * dy_, cy + ey * dx_ + ex * dy_); e = (ex, ey) if ang == 0 else (-ey, ex)
            a = (p[0] - e[0] * ln / 2, p[1] - e[1] * ln / 2); b = (p[0] + e[0] * ln / 2, p[1] + e[1] * ln / 2)
            brick_wall(mb, a[0], a[1], b[0], b[1], 0.0, lambda s, ang=ang, dx_=dx_: h * (0.72 + 0.28 * abs(math.sin(s * 3.1 + dx_ * 0.3 + ang))) if (s > 0.22) else h * 0.55, 0.9,
                       windows=[(0.38, 0.62, h * 0.55, h * 0.7)] if ang == 0 else [(0.38, 0.62, h * 0.62, h * 0.78)])
        for k in range(10): ell(mr, (cx + r.uniform(-w, w), cy + r.uniform(-w, w) - 0.0, 0.3), r.uniform(0.5, 1.3), r.uniform(0.5, 1.2), r.uniform(0.3, 0.7), M['rubble'], 7, 5)
    for (x0, y0, x1, y1, h0) in S['walls']:
        brick_wall(mb, x0, y0, x1, y1, 0.0, lambda s, h0=h0, x0=x0: h0 * (0.35 + 0.65 * abs(math.sin(s * 6.0 + x0))) * (1.0 if 0.1 < s < 0.9 else 0.5), 0.75, windows=[(0.3, 0.38, 1.8, 3.8)])
    for (x, y, rad) in S['rubble']:
        for k in range(int(rad * 3)):
            a_ = r.uniform(0, 6.28); d_ = r.uniform(0, rad); X, Y, Z = rot_axes(r.uniform(0, 6.28), r.uniform(-0.5, 0.5), r.uniform(-0.5, 0.5)); sz = r.uniform(0.35, 0.9)
            ell(mr, (x + math.cos(a_) * d_, y + math.sin(a_) * d_, gh(x, y) + sz * 0.2), sz, sz * r.uniform(0.6, 1.0), sz * 0.45, M['rubble'], 6, 4, (X, Y, Z))
    for (x, y, h, rr_) in S['stumps']:                                # shattered tree stumps: tapering trunk with splintered top
        z = gh(x, y); rod(ms, (x, y, z - 0.2), (x, y, z + h), rr_, M['stump'], 9, rr_ * 0.8)
        for k in range(7):
            a_ = k / 7 * 6.28 + r.uniform(-0.2, 0.2); hh_ = r.uniform(0.5, 1.8); p0 = (x + math.cos(a_) * rr_ * 0.6, y + math.sin(a_) * rr_ * 0.6, z + h - 0.1)
            ms.frustum(p0, (p0[0] + math.cos(a_) * 0.15, p0[1] + math.sin(a_) * 0.15, p0[2] + hh_), rr_ * 0.3, 0.0, M['stump'], seg=4, cap1=False)
        # fallen limb
        a_ = r.uniform(0, 6.28); rod(ms, (x, y, z + 0.4), (x + math.cos(a_) * 3.2, y + math.sin(a_) * 3.2, z + 0.25), rr_ * 0.3, M['stump'], 6, rr_ * 0.15)
    mkobj(mb, 'village_walls'); mkobj(mt, 'village_roofs'); mkobj(mr, 'village_rubble', smooth=True); mkobj(ms, 'stumps')

def build_water():
    M = S['M']; mb = MB()
    for (cx, cy, r, dep, wat) in S['craters']:
        if wat < 0.5: continue
        z = gh(cx, cy) + 0.30 * dep + 0.06; rr = r * 0.66; n = 28
        pts = [(cx + math.cos(2 * math.pi * i / n) * rr * (1 + 0.08 * math.sin(i * 2.3)), cy + math.sin(2 * math.pi * i / n) * rr * (1 + 0.08 * math.cos(i * 1.7)), z) for i in range(n)]
        mb.pid += 1; mb.face(pts, M['water'])
    for (x, y, rx, ry, ang) in S.get('puddles', []):
        z = gh(x, y) + 0.05; n = 20; ca, sa = math.cos(ang), math.sin(ang)
        pts = [(x + math.cos(2 * math.pi * i / n) * rx * ca - math.sin(2 * math.pi * i / n) * ry * sa, y + math.cos(2 * math.pi * i / n) * rx * sa + math.sin(2 * math.pi * i / n) * ry * ca, z) for i in range(n)]
        mb.pid += 1; mb.face(pts, M['water'])
    for (x0, y0, x1, y1) in S.get('floor_pools', []):                   # puddles on the trench floor between duckboards
        pass
    mkobj(mb, 'water')

def build_debris():
    M = S['M']; r = rnd(41); mb = MB(); mm = MB(); mst = MB()
    for (x, y, sz, yaw, tilt) in S['crates']:
        z = gh(x, y); X, Y, Z = rot_axes(yaw, 0.0, tilt)
        obox(mb, (x, y, z + sz * 0.5 - 0.03), X, Y, Z, sz * 0.62, sz * 0.5, sz * 0.5, M['crate'])
        for dz in (-1, 1): obox(mb, Vector((x, y, z + sz * 0.5 - 0.03)) + Z * dz * sz * 0.5, X, Y, Z, sz * 0.62 + 0.02, sz * 0.5 + 0.02, 0.035, M['post'])
    for (x, y, rr_, h, lying, yaw) in S['barrels']:
        z = gh(x, y)
        if lying:
            d = Vector((math.cos(yaw), math.sin(yaw), 0)); c0 = Vector((x, y, z + rr_ * 0.95)); mst.frustum(c0 - d * h / 2, c0 + d * h / 2, rr_, rr_, M['barrel'], seg=14)
            for t in (-0.38, 0.0, 0.38): q = c0 + d * h * t; mst.frustum(q - d * 0.05, q + d * 0.05, rr_ * 1.04, rr_ * 1.04, M['rivet'], seg=14)
        else:
            c0 = Vector((x, y, z - 0.02)); mst.frustum(c0, c0 + Vector((0, 0, h)), rr_, rr_, M['barrel'], seg=14)
            for t in (0.08, 0.5, 0.92): q = c0 + Vector((0, 0, h * t)); mst.frustum(q - Vector((0, 0, 0.05)), q + Vector((0, 0, 0.05)), rr_ * 1.04, rr_ * 1.04, M['rivet'], seg=14)
    for (x, y, n, rad) in S['rocks']:                                    # chalk lumps and brick bats
        for k in range(n):
            a_ = r.uniform(0, 6.28); d_ = r.uniform(0, rad); sz = r.uniform(0.12, 0.38); X, Y, Z = rot_axes(r.uniform(0, 6.28), r.uniform(-0.6, 0.6), r.uniform(-0.6, 0.6)); px, py = x + math.cos(a_) * d_, y + math.sin(a_) * d_
            J.lump(mm, (px, py, gh(px, py) + sz * 0.25), sz, M['rubble'] if k % 2 else M['chalk_rock'], r.randint(0, 9999), 7, 5, 0.3, 0.6)
    for (x, y, ang) in S['planks']:                                      # broken duckboards / planks lying about
        z = gh(x, y); L = r.uniform(2.2, 4.0); X, Y, Z = rot_axes(ang, r.uniform(-0.1, 0.1), r.uniform(-0.1, 0.1))
        obox(mb, (x, y, z + 0.1), X, Y, Z, L / 2, 0.36, 0.06, M['crate'])
    for (x, y, ang) in S.get('stakes', []):                              # iron screw pickets leaning, thin
        z = gh(x, y); lean = Vector((math.cos(ang), math.sin(ang), 0)) * 0.35; rod(mst, (x, y, z - 0.05), Vector((x, y, z + 2.0)) + lean, 0.05, M['wire'], 5)
    mkobj(mb, 'crates'); mkobj(mm, 'rocks', smooth=True); mkobj(mst, 'barrels', smooth=True)

def build_far():
    M = S['M']; mb = MB(); r = rnd(23)
    for k in range(S['n_poplar']):
        x = -230 + k * (460 / S['n_poplar']) + r.uniform(-4, 4); y = 210 + r.uniform(-6, 6) + 14 * math.sin(k * 0.5); h = r.uniform(18, 28); z = 0.0
        z = gh(x, y); ell(mb, (x, y, z + h * 0.5), 2.4, 2.4, h * 0.5, M['poplar'] if k % 3 else M['leaf'], 8, 6)
    for k in range(60):                                               # hedgerow trees / orchard blobs mid-distance
        x = r.uniform(-120, 120); y = r.uniform(70, 150); hh = r.uniform(5, 10)
        if abs(x) < 25 and y < 100: continue
        z = gh(x, y); ell(mb, (x, y, z + hh * 0.6), hh * 0.5, hh * 0.5, hh * 0.45, M['leaf'] if k % 2 else M['leaf2'], 8, 6); rod(mb, (x, y, z - 0.3), (x, y, z + hh * 0.35), 0.35, M['trunk'], 5)
    mkobj(mb, 'far_trees', smooth=True)

# ============================================================================= the MARK I
TANK_OUT = [(-11.0, 0.0), (0.0, 0.0), (3.9, 3.9), (-6.8, 4.3)]        # rhomboid outline (x, z), local frame: origin at the front end of the straight bottom run, x forward
TRACK_Y = (2.05, 3.15); HULL_HW = 2.0
def inset_poly(poly, d):
    n = len(poly); lines = []
    for i in range(n):
        a, b = Vector(poly[i]), Vector(poly[(i + 1) % n]); e = (b - a).normalized(); nn = Vector((-e.y, e.x)); lines.append((a + nn * d, e))      # CCW polygon: left normal is inward
    out = []
    for i in range(n):
        (p, e1), (q, e2) = lines[i - 1], lines[i]; M_ = Matrix(((e1.x, -e2.x), (e1.y, -e2.y))); t = M_.inverted() @ (q - p); out.append(tuple(p + e1 * t[0]))
    return out

def round_poly(poly, rad, n=7):
    """path along the polygon with rounded corners, returns list of points (x, z) and tangent"""
    pts = []; m = len(poly)
    for i in range(m):
        p0, p1, p2 = Vector(poly[i - 1]), Vector(poly[i]), Vector(poly[(i + 1) % m]); a = (p0 - p1).normalized(); b = (p2 - p1).normalized(); ang = math.acos(max(-1, min(1, a.dot(b))))
        d = min(rad[i] / math.tan(ang / 2), (p0 - p1).length * 0.45, (p2 - p1).length * 0.45); r_ = d * math.tan(ang / 2); s = p1 + a * d; e = p1 + b * d; bis = (a + b).normalized(); cen = p1 + bis * (r_ / math.sin(ang / 2))
        a0 = math.atan2(s.y - cen.y, s.x - cen.x); a1 = math.atan2(e.y - cen.y, e.x - cen.x)
        da = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        for k in range(n + 1): aa = a0 + da * k / n; pts.append((cen.x + r_ * math.cos(aa), cen.y + r_ * math.sin(aa)))
    return pts

def resample(pts, step):
    out = [Vector(pts[0])]; acc = 0.0; tot = []; P = [Vector(p) for p in pts] + [Vector(pts[0])]
    L = [(P[i + 1] - P[i]).length for i in range(len(P) - 1)]; total = sum(L); n = int(total / step); res = []
    for k in range(n):
        s = k * total / n; i = 0
        while i < len(L) - 1 and s > L[i]: s -= L[i]; i += 1
        t = s / max(L[i], 1e-9); p = P[i] + (P[i + 1] - P[i]) * t; tan = (P[i + 1] - P[i]).normalized(); res.append((p, tan))
    return res

def rivet_rows(mb, to3, nrm3, inside, u0, u1, v0, v1, sp=0.44, pw=PLATE_W, ph=PLATE_H, off=0.17, r=0.095, mat=None, edge_rows=()):
    """rivets along every seam of the hull's brick-plate layout in UV (u,v): horizontal seams v = j ph, vertical seams u = i pw (+ pw/2 on odd rows); to3(u,v)->point, inside(u,v)->bool"""
    mat = mat or S['M']['rivet']; n = Vector(nrm3)
    def rv(u, v):
        if not inside(u, v): return
        p = Vector(to3(u, v)); mb.frustum(p - n * 0.01, p + n * 0.075, r, r * 0.62, mat, seg=6, cap0=False)
    for j in range(int(math.floor(v0 / ph)) - 1, int(math.ceil(v1 / ph)) + 2):
        vs = j * ph
        for sgn in (-1, 1):
            k = int(math.floor(u0 / sp)) - 1
            while k * sp < u1 + sp: rv(k * sp, vs + sgn * off); k += 1
        for i in range(int(math.floor(u0 / pw)) - 2, int(math.ceil(u1 / pw)) + 3):
            us = i * pw + (pw / 2 if j % 2 else 0.0)
            for sgn in (-1, 1):
                k = 0
                while k * sp < ph: rv(us + sgn * off, vs + k * sp + sp * 0.5); k += 1

def edge_rivets(mb, pts3, nrm3, sp=0.40, r=0.09, mat=None):
    mat = mat or S['M']['rivet']; n = Vector(nrm3)
    for a, b in zip(pts3, pts3[1:] + pts3[:1]):
        a, b = Vector(a), Vector(b); L = (b - a).length; k = int(L / sp)
        for i in range(1, k): p = a + (b - a) * (i / k); mb.frustum(p - n * 0.01, p + n * 0.07, r, r * 0.62, mat, seg=6, cap0=False)

def point_in_poly(poly, x, z):
    c = False; n = len(poly)
    for i in range(n):
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % n]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1: c = not c
    return c

def build_tank(*a, **k):
    """Mark I with hooks: see tank25.py (returns TankH: dict + attributes, .root is the root empty)"""
    import tank25; return tank25.build_tank(*a, **k)

def tank_world(root, p):
    return root.matrix_world @ Vector(p)

def solve_tail(root, ground=None):
    """lower the steering tail until the wheel rims touch the ground (hinge angle by bisection)"""
    hinge = S['tank_tail']; (ax, R) = S['tail_axle']; ground = ground or gh
    def gap(phi):
        hinge.rotation_euler = (0, -math.radians(phi), 0); bpy.context.view_layer.update(); worst = 1e9
        for yc in (2.25, -2.25):
            c = hinge.matrix_world @ Vector((ax[0], yc, ax[2])); worst = min(worst, c.z - R - gh(c.x, c.y))
        return worst
    lo, hi = -40.0, 40.0
    for _ in range(30):
        mid = (lo + hi) / 2
        if gap(mid) > 0.0: lo = mid
        else: hi = mid
    # positive phi raises the tail (nose-down convention), so the root of gap(phi)=0 is the touching angle
    hinge.rotation_euler = (0, -math.radians((lo + hi) / 2), 0); bpy.context.view_layer.update(); return (lo + hi) / 2

# ============================================================================= people (2D puppet cards)
BRODIE = ('<g stroke="#3a2832" stroke-width="0.034" stroke-linejoin="round">'
          '<ellipse cx="%(cx).3f" cy="-0.19" rx="0.60" ry="0.10" fill="#59633a"/>'
          '<path d="M %(l).3f -0.19 C %(l).3f -0.60 %(r).3f -0.60 %(r).3f -0.19 Z" fill="#707a43"/>'
          '<path d="M %(l2).3f -0.33 C %(l2).3f -0.52 %(m).3f -0.58 %(m2).3f -0.52" fill="none" stroke="#a4ad66" stroke-width="0.05" stroke-linecap="round"/></g>'
          '<path d="M -0.40 -0.12 Q -0.44 0.30 -0.20 0.46" fill="none" stroke="#3a2832" stroke-width="0.03"/>')

def world_at_pixel(px, py, cam=None):
    """ground point under pixel (px, py) of the 720x1280 frame (ray march against the heightfield)"""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = cam or sc.camera; bpy.context.view_layer.update()
    f = cam.data.lens; sw = cam.data.sensor_width; sx = (px / 720 - 0.5) * (sw * 720 / 1280); sy = (0.5 - py / 1280) * sw
    d = (cam.matrix_world.to_3x3() @ Vector((sx, sy, -f))).normalized(); o = cam.matrix_world.translation; t = 0.5
    while t < 200:
        p = o + d * t
        if p.z < gh(p.x, p.y): break
        t += 0.2
    lo, hi = t - 0.2, t
    for _ in range(25):
        mid = (lo + hi) / 2; p = o + d * mid
        if p.z > gh(p.x, p.y): lo = mid
        else: hi = mid
    p = o + d * lo; return (p.x, p.y)

def tommy_card(name, mark, face_to, height=3.2, yaw_pose=0.25, expr='determined', arm=('down', 'down'), tilt=0.0, ppd=256, pose_extra=None):
    """STAND-IN Tommy: the `clerk` puppet (lanky, slim) recoloured in khaki with a drawn Brodie steel helmet overlay (no real film-25 costume yet).  Card staged like tower.placeholder_actor."""
    sys.path.insert(0, os.path.join(PROJ, 'v3', 'cast')); sys.path.insert(0, os.path.join(PROJ, 'v2', 'puppet'))
    import cast_ext                                                    # noqa: F401
    import puppet
    if 'tommy25' not in puppet.CAST:
        c = copy.deepcopy(puppet.CAST['clerk']); c['hat'] = None; c['garters'] = False
        c['colors'].update(base='#a8985a', dark='#7d6f3e', collar='#a8985a', tie='#a8985a', tie_dark='#7d6f3e', pants='#8e8048', belt='#4a3420', buckle='#c8b060', button='#c8b060', stripe='#a8985a', pocket='#968848', clip='#a8985a')
        c['hair'] = dict(color='#5a3a28', front=0.085, grow=0.22, shine='#8a6040', style='cap'); puppet.CAST['tommy25'] = c
    pose = dict(yaw=yaw_pose, expr=expr, arm_l=arm[0], arm_r=arm[1], legs='stand'); pose.update(pose_extra or {})
    f = puppet.figure('tommy25', pose, name); svg_body = f['svg'] + BRODIE % dict(cx=yaw_pose * 0.08, l=-0.50 + yaw_pose * 0.03, r=0.50 + yaw_pose * 0.03, l2=-0.30, m=-0.1, m2=0.1)
    bx0, by0, bx1, by1 = f['bbox']; by0 -= 0.2; pad = 0.08; bx0 -= pad; by0 -= pad; bx1 += pad; by1 = max(by1, f['feet_y']) + pad; w, h = bx1 - bx0, by1 - by0; Wp, Hp = int(round(w * ppd)), int(round(h * ppd))
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wp}" height="{Hp}" viewBox="{bx0:.4f} {by0:.4f} {w:.4f} {h:.4f}" style="display:block">{svg_body}</svg>'
    os.makedirs(ACT, exist_ok=True); tag = name + '_' + hashlib.sha1(svg.encode()).hexdigest()[:10]; sp = os.path.join(ACT, tag + '.svg'); pp = os.path.join(ACT, tag + '.png')
    if not os.path.exists(pp):
        open(sp, 'w').write(svg); jp = os.path.join(ACT, tag + '_job.json'); json.dump([dict(src=sp, out=pp, w=Wp, h=Hp, transparent=True)], open(jp, 'w'))
        r = subprocess.run(['node', os.path.join(PROJ, 'v3', 'set3d', 'raster.js'), jp], capture_output=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))
        if r.returncode != 0: raise RuntimeError('card raster failed: ' + r.stderr.decode()[-500:])
    fx = f['anchors']['feet'][0]; fy = f['feet_y']; k = height / max(1e-6, fy - f['bbox'][1])
    me = bpy.data.meshes.new(name); xs = ((bx0 - fx) * k, (bx1 - fx) * k); zs = ((fy - by1) * k, (fy - by0) * k)
    me.from_pydata([(xs[0], 0, zs[0]), (xs[1], 0, zs[0]), (xs[1], 0, zs[1]), (xs[0], 0, zs[1])], [], [(0, 1, 2, 3)]); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for i, c_ in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))): uvl.data[i].uv = c_
    m = T.mat_card(name + '_mat', pp); m.node_tree.nodes['Emission'].inputs['Strength'].default_value = 1.0; me.materials.append(m)
    ob = bpy.data.objects.new(name, me); S['coll'].objects.link(ob); ob.location = mark; T.no_bounce(ob)
    d = Vector(face_to) - Vector(mark); ob.rotation_euler = (math.radians(-tilt), 0, math.atan2(d.x, -d.y))
    # contact decal: dark soft ellipse under the feet, lies on the ground (sampled height), casts nothing
    dm = bpy.data.meshes.new(name + '_decal'); n = 24; vs = [(0, 0, 0)] + [(math.cos(a) * 1.0, math.sin(a) * 0.55, 0) for a in (2 * math.pi * i / n for i in range(n))]
    dm.from_pydata(vs, [], [(0, 1 + i, 1 + (i + 1) % n) for i in range(n)]); dm.update(); uvl = dm.uv_layers.new(name='UVMap')
    for i, p in enumerate(dm.polygons):
        for li, vi in zip(p.loop_indices, p.vertices): uvl.data[li].uv = (0.5 + vs[vi][0] * 0.5, 0.5 + vs[vi][1] / 0.55 * 0.5)
    dm.materials.append(S['decal_mat']); do = bpy.data.objects.new(name + '_decal', dm); S['coll'].objects.link(do); do.location = (mark[0], mark[1], gh(mark[0], mark[1]) + 0.03)
    do.rotation_euler = (0, 0, math.atan2(d.x, -d.y)); do.visible_shadow = False; do.visible_glossy = False
    return ob

def decal_material():
    def f(b):
        uv = b.n('ShaderNodeUVMap').outputs[0]; gr = b.n('ShaderNodeTexGradient', gradient_type='SPHERICAL'); b.l(uv, gr.inputs['Vector'])
        mp = b.n('ShaderNodeMapping'); mp.inputs['Location'].default_value = (0.5, 0.5, 0.0); b.l(uv, mp.inputs['Vector']); b.l(mp.outputs[0], gr.inputs['Vector'])
        a = b.rng(gr.outputs['Fac'], 0.0, 0.5, 0.55, 0.0); a = b.math('POWER', a, 2.0)
        tr = b.n('ShaderNodeBsdfTransparent'); di = b.n('ShaderNodeBsdfDiffuse'); di.inputs['Color'].default_value = (0.02, 0.03, 0.05, 1); mx = b.n('ShaderNodeMixShader')
        b.l(a, mx.inputs[0]); b.l(tr.outputs[0], mx.inputs[1]); b.l(di.outputs[0], mx.inputs[2]); b.l(mx.outputs[0], b.out.inputs['Surface'])
    return fmat('decal', f)

# ============================================================================= world, sun, haze, render
SKY_Z = [(0.0, '#f4ecd6'), (0.06, '#cfe4f2'), (0.30, '#74aeee'), (0.7, '#2c74de')]

def setup_world(sc, sky_k=1.0, cloud_k=1.0):
    w = bpy.data.worlds.new('front_sky'); sc.world = w; w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_WORLD': nt.nodes.remove(n)
    def N(kind, **kw):
        nd = nt.nodes.new(kind)
        for k_, v_ in kw.items(): setattr(nd, k_, v_)
        return nd
    L = nt.links.new; o = [n for n in nt.nodes if n.type == 'OUTPUT_WORLD'][0]
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0]); ramp = N('ShaderNodeValToRGB'); cr = ramp.color_ramp
    cr.elements[0].position = SKY_Z[0][0]; cr.elements[0].color = (*hexl(SKY_Z[0][1]), 1); cr.elements[1].position = SKY_Z[-1][0]; cr.elements[1].color = (*hexl(SKY_Z[-1][1]), 1)
    for pos, col in SKY_Z[1:-1]: e = cr.elements.new(pos); e.color = (*hexl(col), 1)
    L(sep.outputs['Z'], ramp.inputs[0])
    # cumulus: fbm noise on the direction projected onto a high plane (xy / (z + 0.22)), thresholded, white lit top -> blue-grey base
    dv = N('ShaderNodeVectorMath', operation='DIVIDE'); L(tc.outputs['Generated'], dv.inputs[0])
    zp = N('ShaderNodeMath', operation='ADD'); L(sep.outputs['Z'], zp.inputs[0]); zp.inputs[1].default_value = 0.22; L(zp.outputs[0], dv.inputs[1]) if False else None
    comb = N('ShaderNodeCombineXYZ'); sx = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sx.inputs[0])
    d1 = N('ShaderNodeMath', operation='DIVIDE'); L(sx.outputs['X'], d1.inputs[0]); L(zp.outputs[0], d1.inputs[1]); d2 = N('ShaderNodeMath', operation='DIVIDE'); L(sx.outputs['Y'], d2.inputs[0]); L(zp.outputs[0], d2.inputs[1])
    L(d1.outputs[0], comb.inputs['X']); L(d2.outputs[0], comb.inputs['Y']); comb.inputs['Z'].default_value = 0.0
    seed = float(S.get('cloud_seed', 0.0)); mp = N('ShaderNodeMapping'); k_ = 0.8 + 0.45 * ((seed * 7.31) % 1.0); mp.inputs['Location'].default_value = (seed * 3.7, seed * 2.3, 0.0); mp.inputs['Scale'].default_value = (k_, k_ * (0.85 + 0.3 * ((seed * 3.1) % 1.0)), 1.0)
    L(comb.outputs[0], mp.inputs['Vector'])                                                  # per-preset cloud seed: offset + scale + aspect, so no two shots show the same clouds
    n1a = N('ShaderNodeTexNoise'); n1a.inputs['Scale'].default_value = 1.15; n1a.inputs['Detail'].default_value = 5.0; n1a.inputs['Roughness'].default_value = 0.62; L(mp.outputs[0], n1a.inputs['Vector'])
    n3 = N('ShaderNodeTexNoise'); n3.inputs['Scale'].default_value = 0.42; n3.inputs['Detail'].default_value = 2.0; L(mp.outputs[0], n3.inputs['Vector'])         # big structures: clouds of very different sizes and spacing
    m1 = N('ShaderNodeMath', operation='MULTIPLY'); m1.inputs[1].default_value = 0.70; L(n1a.outputs['Fac'], m1.inputs[0]); m2 = N('ShaderNodeMath', operation='MULTIPLY'); m2.inputs[1].default_value = 0.50; L(n3.outputs['Fac'], m2.inputs[0])
    n1 = N('ShaderNodeMath', operation='ADD'); L(m1.outputs[0], n1.inputs[0]); L(m2.outputs[0], n1.inputs[1]);     n2 = N('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 5.0; n2.inputs['Detail'].default_value = 3.0; L(mp.outputs[0], n2.inputs['Vector'])
    cm = N('ShaderNodeMapRange'); cm.inputs['From Min'].default_value = 0.55; cm.inputs['From Max'].default_value = 0.68; L(n1.outputs[0], cm.inputs['Value'])
    cm.interpolation_type = 'SMOOTHSTEP'; S['cloud_map'] = cm
    hz = N('ShaderNodeMapRange'); hz.inputs['From Min'].default_value = 0.03; hz.inputs['From Max'].default_value = 0.16; L(sep.outputs['Z'], hz.inputs['Value'])          # no clouds on the horizon line
    cmask = N('ShaderNodeMath', operation='MULTIPLY'); L(cm.outputs['Result'], cmask.inputs[0]); L(hz.outputs['Result'], cmask.inputs[1])
    shade = N('ShaderNodeMapRange'); shade.inputs['From Min'].default_value = 0.54; shade.inputs['From Max'].default_value = 0.86; shade.inputs['To Min'].default_value = 1.0; shade.inputs['To Max'].default_value = 0.0; L(n1.outputs[0], shade.inputs['Value'])
    ccol = N('ShaderNodeMix', data_type='RGBA'); L(shade.outputs['Result'], ccol.inputs[0]); ccol.inputs[6].default_value = (0.42, 0.52, 0.74, 1); ccol.inputs[7].default_value = (2.0 * cloud_k, 1.98 * cloud_k, 1.9 * cloud_k, 1)
    fin = N('ShaderNodeMix', data_type='RGBA'); L(cmask.outputs[0], fin.inputs[0]); L(ramp.outputs[0], fin.inputs[6]); L(ccol.outputs[2], fin.inputs[7])
    bg = N('ShaderNodeBackground'); bg.inputs['Strength'].default_value = sky_k; L(fin.outputs[2], bg.inputs['Color']); L(bg.outputs[0], o.inputs['Surface'])

def make_haze(density, size=(1500, 1500, 300), center=(0, 0, 90)):
    m = J.mat('F_haze', lambda b: None); b = NB(m); v = b.n('ShaderNodeVolumePrincipled'); v.inputs['Density'].default_value = density; v.inputs['Anisotropy'].default_value = 0.4
    v.inputs['Color'].default_value = (*hexl('#e9f0f8'), 1); b.l(v.outputs[0], b.out.inputs['Volume']); S['haze_node'] = v
    vs = [(center[0] + sx * size[0], center[1] + sy * size[1], center[2] + sz * size[2]) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    fs = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    me = bpy.data.meshes.new('haze'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(m); ob = bpy.data.objects.new('haze', me); S['coll'].objects.link(ob); ob.visible_shadow = False; return ob

def set_sun(az_deg, elev, energy=None):
    sun = S['sun']; e = math.radians(elev); a = math.radians(az_deg); to_sun = Vector((math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)))
    sun.rotation_euler = (-to_sun).to_track_quat('-Z', 'Y').to_euler(); S['to_sun'] = to_sun
    if energy: sun.data.energy = energy

def sun_for_camera(setup, elev=28.0, left=1.0, front=0.45):
    """key from the camera's left and a little from its front side (shadows fall right and away)"""
    f = Vector(setup['look_at']) - Vector(setup['loc']); f.z = 0; f.normalize(); lf = Vector((-f.y, f.x, 0)); h = (lf * left - f * front).normalized()
    return math.degrees(math.atan2(h.y, h.x)), elev

def setup_render(sc, quality='final', samples=None, scale=None):
    r = sc.render; r.engine = 'CYCLES'; r.resolution_x, r.resolution_y = 720, 1280; r.resolution_percentage = 100 if quality == 'final' else int((scale or 0.4) * 100)
    r.image_settings.file_format = 'PNG'; r.image_settings.color_depth = '16'; r.use_motion_blur = False; r.fps = 30
    cy = sc.cycles; cy.device = 'CPU'; cy.samples = int(samples or S.get('samples', 64)) if quality == 'final' else int(samples or 16); cy.use_adaptive_sampling = True; cy.adaptive_threshold = S.get('adapt', 0.012); cy.adaptive_min_samples = 16
    cy.use_denoising = True; cy.denoiser = 'OPENIMAGEDENOISE'; cy.denoising_prefilter = 'ACCURATE'; cy.denoising_input_passes = 'RGB_ALBEDO_NORMAL'; cy.denoising_use_gpu = False
    cy.max_bounces = 6; cy.diffuse_bounces = 5; cy.glossy_bounces = 3; cy.transmission_bounces = 2; cy.volume_bounces = 0; cy.transparent_max_bounces = 8; cy.caustics_reflective = False; cy.caustics_refractive = False
    cy.blur_glossy = 0.5; cy.volume_step_rate = 2.0; cy.use_light_tree = True; cy.sample_clamp_indirect = 8.0; cy.sample_clamp_direct = 0.0
    r.threads_mode = 'FIXED'; r.threads = int(os.environ.get('SET25_THREADS', 4)); r.use_persistent_data = True
    sc.view_settings.view_transform = S.get('view', 'Standard')
    try: sc.view_settings.look = S.get('look', 'None')
    except TypeError: pass
    sc.view_settings.exposure = float(S.get('exposure', 0.0)); sc.view_settings.gamma = 1.0

def make_camera(setup, name='cam'):
    sc = bpy.context.scene; ob = bpy.data.objects.get(name)
    if ob is None: cd = bpy.data.cameras.new(name); ob = bpy.data.objects.new(name, cd); sc.collection.objects.link(ob)
    cd = ob.data; cd.lens = setup.get('lens', 24); cd.sensor_width = 36; cd.sensor_fit = 'AUTO'; cd.clip_start = 0.05; cd.clip_end = 9000; cd.dof.use_dof = False
    ob.location = setup['loc']; fwd = (Vector(setup['look_at']) - Vector(setup['loc'])).normalized(); ob.rotation_euler = fwd.to_track_quat('-Z', 'Y').to_euler()
    if 'up' in setup:
        right = fwd.cross(Vector(setup['up'])).normalized(); up = right.cross(fwd); ob.rotation_euler = Matrix((right, up, -fwd)).transposed().to_euler()
    if setup.get('roll'): ob.rotation_euler.rotate_axis('Z', math.radians(setup['roll']))
    sc.camera = ob; return ob

# ============================================================================= presets (FRONT location; other locations: factory.py trial.py street.py dock.py sky.py, entry point set25.py)
CAMS = dict(
    plan=dict(loc=(0.0, 4.0, 70.0), look_at=(0.0, 4.0, 0.0), lens=40, up=(0, 1, 0)),
    side=dict(loc=(-26.0, -28.0, 8.0), look_at=(-2.0, 3.0, 2.5), lens=30),
    back=dict(loc=(12.0, 24.0, 6.0), look_at=(-1.0, 2.0, 2.5), lens=30),
)

def _cam_idler(S_):
    n = S_['tank'].root.matrix_world @ Vector((3.0, -2.6, 3.4)); return dict(loc=(n.x + 1.0, n.y - 6.5, n.z - 2.4), look_at=(n.x, n.y, n.z + 0.4), lens=35)

def _cam_lip(S_):
    """camera at the lowest outline point of the right track where it meets the far mound (the grip), looking at it from the side and a little below"""
    import tank25 as TK
    H = S_['tank']; bpy.context.view_layer.update(); best = None
    for (x, z) in TK.outline_pts(0.3):
        p = H.root.matrix_world @ Vector((x, -2.6, z)); cl = p.z - gh(p.x, p.y)
        if p.x > 1.0 and (best is None or cl < best[0]): best = (cl, p)
    p = best[1]; return dict(loc=(p.x + 1.5, p.y - 8.5, p.z + 0.6), look_at=(p.x, p.y, p.z + 0.9), lens=30)
_TP = [(0.0, -3.0), (0.0, 14.0), (7.0, 21.0), (31.0, 21.0)]
_CR = dict(x0=0.0, y=4.5, s_a=-5.0, s_b=27.0, mud=1.0)
_CT = dict(poly=_TP, mw=0.8, me=1.9, sb_layers=(2, 2))
def _cross(name, u, cam, **kw):
    d = dict(loc='front', cam=cam, cross=dict(_CR, u=u), trench0=_CT); d.update(kw); return d
PRESETS = dict(
    cross_nose=_cross('cross_nose', 0.34, dict(loc=(0.5, -18.5, 1.0), look_at=(2.0, 4.5, 3.8), lens=21), dress_n=2.4, world=dict(rocks=[(5.0, -9.6, 3, 1.6), (8.8, -7.0, 4, 3.0), (3.0, -9.5, 5, 2.2), (-6.0, 8.0, 8, 4.0), (6.5, 5.0, 6, 3.0), (-3.5, -9.0, 5, 2.5), (3.0, -12.0, 16, 4.0), (7.0, -9.0, 12, 3.0), (-1.0, -11.0, 12, 3.5), (1.0, -7.0, 10, 3.0)]), tune=dict(green_k=0.3), cards=[('a', (-8, -6), 3.2)], clamp=True, note='shot 24: side-on low, the nose lifting over the trench gap'),
    cross_hero=_cross('cross_hero', 0.40, dict(loc=(4.0, -18.5, 1.0), look_at=(2.5, 4.5, 3.8), lens=21), dress_n=2.4, world=dict(rocks=[(5.0, -9.6, 3, 1.6), (8.8, -7.0, 4, 3.0), (3.0, -9.5, 5, 2.2), (-6.0, 8.0, 8, 4.0), (6.5, 5.0, 6, 3.0), (-3.5, -9.0, 5, 2.5), (3.0, -12.0, 16, 4.0), (7.0, -9.0, 12, 3.0), (-1.0, -11.0, 12, 3.5), (1.0, -7.0, 10, 3.0)]), tune=dict(green_k=0.3), cards=[('a', (-9, -5), 3.2), ('b', (10, -4), 3.2)], clamp=True, note='shot 25: SIDE-ON, nose lifted, front track gripping the far lip, rear on the near parapet'),
    cross_pull=_cross('cross_pull', 0.60, dict(loc=(7.5, -11.0, 1.3), look_at=(4.5, 4.5, 1.8), lens=24), fill=500.0, dress_n=2.6, cards=[('a', (-6, -6), 3.2)], clamp=True, note='shot 26: pulling across, rear tracks leaving the near lip'),
    cross_wire=_cross('cross_wire', 0.12, dict(loc=(-5.0, -8.0, 0.8), look_at=(-9.5, 2.0, 1.2), lens=22), dress_n=0.3, near=False, sun=(205.0, 30.0), fill=1200.0, tune=dict(cloud_k=0.8, green_k=0.2), lane_ok=True, world=dict(crates=[]), note='shot 27: low insert, barbed wire squashed flat under the track'),
    cross_hull=_cross('cross_hull', 0.50, dict(loc=(11.0, -7.0, 3.2), look_at=(5.0, 4.5, 3.0), lens=24), sparks=0.30, sun=(205.0, 30.0), fill=2200.0, dress_n=0.4, near=False, tune=dict(cloud_k=0.8), note='shot 28: hull side, bullet pings (sparks)'),
    cross_flee=_cross('cross_flee', 0.62, dict(loc=(-27.0, -3.0, 8.0), look_at=(6.0, 5.0, 2.6), lens=20), dress_n=2.0, tune=dict(cloud_k=0.9), cards=[('b', (14, 3), 3.2), ('a', (19, 8), 3.2), ('b', (24, 0), 3.2), ('a', (17, 12), 3.2)], clamp=True, note='shot 29: wide behind the tank, Germans (stand-ins) running'),
    cross_bucket=_cross('cross_bucket', 0.50, dict(loc=(-3.0, -14.0, 1.2), look_at=(0.5, 6.0, 1.4), lens=24), extras=[('bucket', -5.2, -5.5)], near=False, dress_n=1.2, tune=dict(cloud_k=0.95), note='shot 30: plain water bucket by the trench vs the tank over it'),
    front_aerial=dict(loc='front', tune=dict(haze=0.0, cloud_k=0.8, green_k=0.2), dress_n=1.5, cam=dict(loc=(-62.0, -22.0, 34.0), look_at=(-6.0, 6.0, 2.0), lens=24), cards=[('a', (-28, -6), 3.6), ('b', (-33, 8), 3.6), ('a', (-1, 4), 3.6), ('b', (6, 18), 3.6)], note='shot 5: high wide over the two zig-zag lines'),
    front_parapet=dict(loc='front', tune=dict(cloud_k=0.95), cam=dict(loc=(-33.0, -0.5, 2.6), look_at=(-4.0, 5.0, 1.4), lens=28), extras=[('mg', -5.2, 5.0, math.pi, True)], cards=[('a', (-30.5, -3.0), 3.0)], note='shot 6: behind the British parapet, German MG nest across the wire'),
    front_column=dict(loc='front', tune=dict(cloud_k=1.15), dress_n=2.5, cam=dict(loc=(8.0, -58.0, 4.5), look_at=(-20.0, -74.0, 1.8), lens=24), tanks=[dict(front=(-20.0, -34.0), yaw=90.0), dict(front=(-20.0, -56.0), yaw=90.0), dict(front=(-20.0, -78.0), yaw=90.0), dict(front=(-20.0, -100.0), yaw=90.0, smoke=1.0)], note='shot 20: column crawling to the start line'),
    front_halt=dict(loc='front', tune=dict(cloud_k=0.85, green_k=2.2), dress_n=4.0, cam=dict(loc=(8.0, -36.0, 2.8), look_at=(-22.0, -36.0, 2.0), lens=22), tanks=[dict(front=(-22.0, -33.0), yaw=90.0, nocorr=True), dict(front=(-8.0, -22.0), yaw=95.0, smoke=1.0)], clamp=True, note='shot 21: one smoking, one nose-down in a crater'),
    front_stuck=dict(loc='front', dress_n=3.0, tune=dict(cloud_k=0.85, green_k=0.3), world=dict(rocks=[(5.0, -9.6, 3, 1.6), (3.0, -49.0, 22, 4.0), (6.0, -47.0, 16, 3.0), (0.0, -46.0, 14, 3.0), (8.0, -44.0, 12, 3.0)], spill=[(4.0, -48.0, 4.0, 14)]), cam=dict(loc=(6.0, -52.0, 1.4), look_at=(-4.0, -41.0, -0.6), lens=24), tanks=[dict(front=(-4.0, -42.0), yaw=90.0, state='stuck')], extras=[('mud', -4.0, -42.0, math.pi / 2)], cards=[('a', (2.0, -45.0), 3.2), ('b', (-9.0, -47.0), 3.2)], clamp=True, note='shot 22: sunk to the sponsons in mud'),
    front_op=dict(loc='front', tune=dict(cloud_k=0.85), fill=3000.0, cam=dict(loc=(-45.0, -17.0, 6.5), look_at=(-26.0, -8.0, 2.4), lens=28), extras=[('op', -28.0, -8.0, 0.0)], tanks=[dict(front=(-6.0, -16.0), yaw=90.0, smoke=1.0)], cards=[('a', (-30.5, -9.0), 2.6)], note='shot 23: observation post'),
    front_close_britishtrench=dict(loc='front', mark=dict(pos=(-34.0, -8.0), face_deg=262.9, dist=4.2, lens=28, zc=1.9, look_dz=-0.4), clamp=True, cast=[dict(story='tommy_a25_peek')], extras=[('bags', -34.0, -4.5), ('pop', -34.0, -3.0)], dress_n=0.3, near=False, note='shots 8-9, 10-11: waist-up Tommy inside the British trench (mark)'),
    front_close_germantrench=dict(loc='front', mark=dict(pos=(0.0, 6.0), face_deg=90.0, dist=4.2, lens=28, zc=1.9, look_dz=-0.4), clamp=True, cast=[dict(story='german_a25_peek', mirror=True)], extras=[('bags', 0.0, 2.0), ('pop', 0.0, 1.0)], dress_n=0.3, near=False, note='shots 8-9, 55: German trench mirror close (mark)'),
    op_close_general=dict(loc='front', mark=dict(pos=(-30.2, -8.0), face_deg=0.0, dist=4.2, lens=28, zc=1.9), cast=[dict(story='general25_point_stick')], extras=[('op', -28.0, -8.0, 0.0)], dress_n=0.3, near=False, note='shots 43-44: general in the observation post (mark)'),
    cross_close_idler=_cross('cross_close_idler', 0.40, _cam_idler, clamp=True, dress_n=1.2, note='shots 47-49: track links round the front idler as the nose lifts against the sky'),
    cross_close_lip=_cross('cross_close_lip', 0.40, _cam_lip, clamp=True, dress_n=1.6, extras=[('clods', 5.0, 4.5)], note='shot 50: the front track gripping the far lip, earth crumbling'),
)

def default_world():
    """the Front: layout constants shared by every preset of the location (trench lines, craters, village, wire belts)"""
    S['trenches'] = [dict(name='german', poly=[(11.0, -38.0), (11.0, -26.0), (2.0, -14.0), (0.0, -6.0), (0.0, 14.0), (7.0, 21.0), (31.0, 21.0)], depth=4.7, hf=2.2, hw=3.3, mw=1.55, me=0.5, sb_layers=(3, 2)),
                     dict(name='british', poly=[(-31.0, -60.0), (-31.0, -30.0), (-35.0, -16.0), (-33.0, 0.0), (-30.0, 14.0), (-34.0, 26.0), (-33.0, 60.0)], depth=4.3, hf=2.0, hw=3.1, mw=0.5, me=1.2, sb_layers=(1, 3))]
    S['trench'] = S['trenches'][0]['poly']
    S['craters'] = [(-15.0, -9.0, 4.4, 1.5, 1.0), (13.0, -4.0, 3.6, 1.1, 0.9), (8.6, -13.0, 2.6, 0.7, 0.7), (9.0, -26.0, 5.0, 1.8, 1.0), (-20.0, 17.0, 5.0, 1.6, 0.4), (22.0, 8.0, 3.0, 0.9, 0.3), (-9.0, -31.0, 3.5, 1.2, 0.5), (18.0, 30.0, 6.0, 1.8, 0.8),
                    (-22.0, -34.0, 7.5, 2.6, 0.9), (-14.0, 33.0, 4.0, 1.2, 0.6), (-12.0, -48.0, 5.0, 1.8, 1.0), (4.0, -46.0, 4.0, 1.3, 0.6)]
    S['mud_zones'] = [(-9.0, -6.0, 6.0, 3.0, 0.4), (12.0, -4.0, 7.0, 4.0, -0.3), (3.0, -18.0, 6.0, 3.0, 0.2), (-18.0, -40.0, 14.0, 6.0, 0.3), (-4.0, -42.0, 10.0, 5.0, -0.2)]
    S['wire_belts'] = [(-9.0, -14.0, -11.5, 22.0, 3), (-12.5, -14.0, -15.0, 22.0, 2), (9.0, -1.0, 10.0, 16.0, 2), (-22.0, -20.0, -23.0, 12.0, 2)]
    S['wire_coils'] = [(2.6, 0.2, 3.2, 0.62, 6), (4.8, -1.6, 3.0, 0.6, 6), (5.2, 2.4, 3.4, 0.6, 6), (1.8, 3.4, 3.0, 0.55, 6), (-4.2, 9.0, 4.5, 0.55, 8), (-8.0, 2.0, 3.5, 0.5, 6), (-2.0, 12.0, 3.0, 0.45, 6), (6.0, 2.0, 4.0, 0.55, 7), (7.5, -1.5, 3.2, 0.5, 6), (5.5, 4.5, 3.0, 0.5, 6), (-6.5, 5.5, 4.0, 0.5, 7)]
    S['houses'] = [('farm', -4.0, 40.0, 22.0, 12.0, 0.10, 5), ('barn', 26.0, 46.0, 16.0, 9.0, -0.15, 8), ('farm2', 56.0, 4.0, 20.0, 11.0, 1.5, 11), ('barn2', 62.0, -22.0, 14.0, 9.0, 1.7, 14)]
    S['towers'] = [(-24.0, 48.0, 7.2, 26.0, 0.15), (74.0, 18.0, 7.0, 24.0, 0.3)]
    S['walls'] = [(-20.0, 34.0, -9.0, 35.0, 6.5), (10.0, 36.0, 20.0, 38.0, 5.5), (-46.0, 40.0, -34.0, 44.0, 6.0), (36.0, 52.0, 56.0, 55.0, 6.0), (44.0, -14.0, 44.5, -2.0, 6.0), (48.0, 20.0, 49.0, 32.0, 5.0)]
    S['rubble'] = [(-14.0, 38.0, 5.0), (8.0, 36.0, 4.0), (-30.0, 46.0, 4.5), (22.0, 40.0, 4.0), (-3.0, 30.0, 3.0), (46.0, -6.0, 4.0), (50.0, 26.0, 4.0)]
    S['stumps'] = [(-12.0, 30.0, 6.0, 0.7), (8.0, 36.0, 5.0, 0.6), (26.0, 24.0, 7.0, 0.8), (-28.0, 28.0, 4.5, 0.6), (40.0, 42.0, 6.0, 0.7), (-6.0, 27.0, 3.5, 0.5), (36.0, -10.0, 6.0, 0.7), (38.0, 8.0, 4.0, 0.6)]
    S['n_poplar'] = 38
    S['crates'] = [(9.4, -9.2, 1.7, 0.3, 0.0), (11.2, -9.9, 1.5, -0.2, 0.0), (10.0, -9.4, 1.3, 0.8, 0.0), (5.6, 6.5, 1.6, 0.5, 0.15), (-2.5, 15.0, 1.5, 0.2, 0.0), (-7.5, -4.5, 1.6, -0.3, 0.1)]
    S['barrels'] = [(12.4, -7.5, 0.62, 1.6, False, 0.0), (13.5, -8.6, 0.62, 1.6, True, 0.6), (-8.5, 9.5, 0.62, 1.6, True, 2.0)]
    S['rocks'] = [(5.0, -9.6, 3, 1.6), (8.8, -7.0, 4, 3.0), (3.0, -9.5, 5, 2.2), (-6.0, 8.0, 8, 4.0), (6.5, 5.0, 6, 3.0), (-3.5, -9.0, 5, 2.5)]
    S['planks'] = [(8.8, -2.6, 0.4), (-4.0, -2.0, 2.3), (-5.5, 11.0, 0.9), (7.0, 9.0, 1.9)]
    S['stakes'] = [(7.8, -4.4, 0.8), (8.6, -3.4, 2.5), (2.4, -8.2, 4.0), (-6.5, 6.8, 5.0)]
    S['puddles'] = [(6.0, -3.2, 1.6, 0.9, 0.4), (2.5, -9.8, 1.2, 0.7, -0.3), (-5.2, 6.5, 1.6, 1.0, 0.2)]
    S['spill'] = []; S['corridors'] = []; S['far0'] = 70; S['far1'] = 150

def corridor_pred(wide=0.0):
    cs = S.get('corridors', [])
    def f(x, y):
        for c in cs:
            s, v = corridor_sv(c, np.array([x]), np.array([y]))
            if c['s0'] - 2 - wide < s[0] < c['s1'] + 2 and abs(v[0]) < c['flat'] + 0.5 + wide: return True
        return False
    return f

def add_corridor(o, yaw_deg, s0, s1, flat=4.8, blend=6.8, dz=0.0):
    S['corridors'].append(dict(o=o, h=(math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))), s0=s0, s1=s1, flat=flat, blend=blend, dz=dz))

# --------------------------------------------------------------------------- extras: MG nest, OP, bucket, dressing
def mg_nest(x, y, yaw, flash=False):
    """German machine-gun nest on the lip: horseshoe of sandbags (3 courses, open to the front), a Maxim on a tripod with a shield and a belt box; yaw = firing direction (rad)"""
    import lib25 as L
    M = S['M']; mb = MB(); mg = MB(); e = Vector((math.cos(yaw), math.sin(yaw), 0)); nrm = Vector((-e.y, e.x, 0)); c = Vector((x, y, gh(x, y)))
    for (a, b) in ((-1.9, 1.9),):
        p0 = c + e * 1.7 - nrm * 1.9; p1 = c + e * 1.7 - nrm * 0.6; sandbag_row(mb, p0, p1, gh, 3, seed=5)
        p0 = c + e * 1.7 + nrm * 0.6; p1 = c + e * 1.7 + nrm * 1.9; sandbag_row(mb, p0, p1, gh, 3, seed=6)
        p0 = c + e * 1.7 - nrm * 1.9; p1 = c - e * 1.4 - nrm * 1.9; sandbag_row(mb, p0, p1, gh, 3, seed=7)
        p0 = c + e * 1.7 + nrm * 1.9; p1 = c - e * 1.4 + nrm * 1.9; sandbag_row(mb, p0, p1, gh, 3, seed=8)
    z0 = c.z + 0.55; X, Y, Z = rot_axes(yaw)
    for sg in (-1, 1): rod(mg, c + e * 0.6 + nrm * sg * 0.55 + Vector((0, 0, 0.05)), c + e * 0.9 + Vector((0, 0, z0 + 0.45)), 0.04, M['steel'], 5)
    rod(mg, c + e * 0.15 + Vector((0, 0, z0 + 0.5)), c + e * 1.0 + Vector((0, 0, z0 + 0.52)), 0.17, M['steel'], 10); rod(mg, c + e * 1.0 + Vector((0, 0, z0 + 0.52)), c + e * 1.9 + Vector((0, 0, z0 + 0.52)), 0.09, M['gun'], 8)
    rod(mg, c + e * 1.8 + Vector((0, 0, z0 + 0.52)), c + e * 2.1 + Vector((0, 0, z0 + 0.52)), 0.13, M['gun'], 8); obox(mg, c + e * 0.1 + Vector((0, 0, z0 + 0.52)), X, Y, Z, 0.35, 0.22, 0.24, M['steel'])
    obox(mg, c + e * 1.35 + Vector((0, 0, z0 + 0.8)), X, Y, Z, 0.04, 0.5, 0.35, M['steel_l'])
    obox(mg, c - e * 0.2 + nrm * 0.45 + Vector((0, 0, z0 + 0.3)), X, Y, Z, 0.28, 0.15, 0.2, M['rivet'])
    mkobj(mb, 'mg_bags', smooth=True); mkobj(mg, 'mg_gun', smooth=True)
    if flash:
        mf = MB(); m = S['M']['glow']; mu = c + e * 2.15 + Vector((0, 0, z0 + 0.52)); X, Y, Z = rot_axes(yaw)
        for k in range(4):
            a = k * math.pi / 4; d1 = Y * math.cos(a) + Z * math.sin(a); mf.pid += 1; mf.oface([mu + d1 * 0.1 - X * 0.02, mu + d1 * 0.75 + X * 0.1, mu - d1 * 0.1 - X * 0.02], m, [(0, 0)] * 3, X)
            mf.pid += 1; mf.oface([mu - d1 * 0.1, mu - d1 * 0.75 + X * 0.1, mu + d1 * 0.1], m, [(0, 0)] * 3, X)
        mkobj(mf, 'mg_flash', shadow=False); L.smoke_puffs('mg_puff', (mu.x + e.x * 0.5, mu.y + e.y * 0.5, mu.z + 0.2), 4, 0.28, 0.5, 3, '#f4f0e8')
    return c

def op_post(x, y, yaw):
    """British observation post: three-sided sandbag chamber with a slit facing yaw, a plank roof, a periscope and a ledge for field glasses"""
    import lib25 as L
    M = S['M']; mb = MB(); mw = MB(); e = Vector((math.cos(yaw), math.sin(yaw), 0)); nrm = Vector((-e.y, e.x, 0)); c = Vector((x, y, gh(x, y))); X, Y, Z = rot_axes(yaw)
    def row(p0, p1, layers, skipz=()): sandbag_row(mb, p0, p1, gh, layers, seed=int(abs(p0.x * 3 + p0.y)) + 2)
    W = 3.4; Dp = 2.6
    row(c + e * Dp - nrm * W, c + e * Dp - nrm * 0.9, 5); row(c + e * Dp + nrm * 0.9, c + e * Dp + nrm * W, 5); row(c + e * Dp - nrm * 0.9, c + e * Dp + nrm * 0.9, 2)       # front wall with a viewing slit above 2 courses
    row(c + e * Dp - nrm * W, c - e * 2.2 - nrm * W, 5); row(c + e * Dp + nrm * W, c - e * 2.2 + nrm * W, 5)
    obox(mw, c - e * 0.2 + Vector((0, 0, 3.1)), X, Y, Z, 3.0, W + 0.5, 0.06, M['tin'])                                     # corrugated-iron roof sheet
    for k in range(3): beam(mw, c + e * (-2.4 + k * 2.4) - nrm * (W + 0.3) + Vector((0, 0, 2.9)), c + e * (-2.4 + k * 2.4) + nrm * (W + 0.3) + Vector((0, 0, 2.9)), 0.25, 0.2, M['beam'])
    obox(mw, c + e * (Dp - 0.5) + Vector((0, 0, 1.75)), X, Y, Z, 0.5, 2.8, 0.06, M['crate'])                   # ledge
    obox(mw, c + e * (Dp - 0.2) - nrm * 0.0 + Vector((0, 0, 1.95)), X, Y, Z, 0.35, 0.22, 0.1, M['galv'])                                          # field glasses
    obox(mw, c + e * (Dp - 0.2) + nrm * 0.3 + Vector((0, 0, 1.95)), X, Y, Z, 0.35, 0.22, 0.1, M['galv'])
    pp = c - nrm * 2.0 + e * 1.0; rod(mw, pp + Vector((0, 0, 0)), pp + Vector((0, 0, 4.6)), 0.16, M['steel'], 8); obox(mw, pp + Vector((0, 0, 4.6)) + e * 0.12, X, Y, Z, 0.3, 0.22, 0.32, M['steel_l'])
    obox(mw, pp + Vector((0, 0, 4.6)) - e * 0.1 + Vector((0, 0, 0)), X, Y, Z, 0.05, 0.18, 0.28, M['galv'])
    mkobj(mb, 'op_bags', smooth=True); mkobj(mw, 'op_wood')
    return c

def bucket_at(x, y):
    import lib25 as L
    mb = MB(); L.bucket3d(mb, (x, y, gh(x, y)), 0.5, 0.75, True); return mkobj(mb, 'bucket_%d' % int(x * 7), smooth=True)

def clods(x, y, n=18, seed=9):
    """loose lumps of earth crumbling off a lip (insert shot): small mud lumps on and below the crest"""
    mb = MB(); rr = rnd(seed); m = S['M']['mud_lump']
    for i in range(n):
        px, py = x + rr.uniform(-1.2, 1.2), y + rr.uniform(-1.6, 0.8); J.lump(mb, (px, py, gh(px, py) + rr.uniform(0.05, 0.3)), rr.uniform(0.08, 0.26), m, rr.randint(0, 9999), 7, 5, 0.3, 0.7)
    return mkobj(mb, 'clods', smooth=True)

def mud_heaps(x, y, yaw, n=26, seed=3):
    """lumps of churned mud banked against both sides of a sunk tank (the ground mesh covers its lower hull)"""
    mb = MB(); rr = rnd(seed); e = (math.cos(yaw), math.sin(yaw)); nn = (-e[1], e[0]); m = S['M']['mud_lump']
    for i in range(n):
        u = rr.uniform(-13, 2.5); v = rr.choice((-1, 1)) * rr.uniform(3.4, 5.4); px, py = x + e[0] * u + nn[0] * v, y + e[1] * u + nn[1] * v
        J.lump(mb, (px, py, gh(px, py) + 0.2), rr.uniform(0.5, 1.1), m, rr.randint(0, 99999), 8, 5, 0.3, 0.6)
    return mkobj(mb, 'mud_heaps', smooth=True)

def far_ring():
    """poplar avenues, orchards and hedgerows on the horizon all round (green field beyond, blue sky above)"""
    import lib25 as L
    M = S['M']; mt = MB(); ml = MB(); r = rnd(23)
    for k in range(70):
        a = k / 70 * 2 * math.pi + r.uniform(-0.03, 0.03); d = r.uniform(190, 240); x, y = 5 + math.cos(a) * d, 10 + math.sin(a) * d
        L.poplar(mt, ml, x, y, gh(x, y), r.uniform(18, 28), k)
    for k in range(110):
        a = r.uniform(0, 6.283); d = r.uniform(85, 170); x, y = 5 + math.cos(a) * d, 10 + math.sin(a) * d
        if abs(x) < 40 and abs(y - 5) < 40: continue
        L.oak(mt, ml, x, y, gh(x, y), r.uniform(7, 13), k, M['fol_a'] if k % 2 else M['fol_b'])
    mkobj(mt, 'far_trunks'); mkobj(ml, 'far_leaves', smooth=True)

P_NEAR = [True]
def cam_project(cam, p):
    """screen position (u right, v down, 0..1 of the 720x1280 frame) and depth of a world point for a camera dict (loc, look_at, lens; sensor 36 on the long side)"""
    loc = Vector(cam['loc']); fwd = (Vector(cam['look_at']) - loc).normalized(); right = fwd.cross(Vector((0, 0, 1))).normalized(); up = right.cross(fwd); d = Vector(p) - loc
    zc = d.dot(fwd)
    if zc < 0.1: return None
    f = cam['lens']; return (0.5 + d.dot(right) / zc * f / 20.25, 0.5 - d.dot(up) / zc * f / 36.0, zc)

def tank_screen_boxes(cam, pad=0.05):
    bpy.context.view_layer.update(); out = []
    for H in S.get('tanks_h', []):
        pts = []
        for lp in ((-11, 0, 0), (0, 0, 0), (4, 0, 4), (-7, 0, 4.4), (-1, 4.2, 3.3), (-1, -4.2, 3.3), (-17.7, 2.3, 0), (-17.7, -2.3, 0), (-17.7, 0, 4), (2, 0, 6)):
            r = cam_project(cam, H.root.matrix_world @ Vector(lp))
            if r: pts.append(r)
        if pts: out.append((min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad, max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad * 1.6))
    return out

def dress_front(cam, focus, n=1.0, seed=11, lane_ok=False):
    """texture + colour in the near foreground (producer fix 1 + 3): grass tufts and weeds along every trench lip and crater rim, scattered tufts, poppies, red brick bats,
    broken duckboards, spilled sandbags, wire stakes; everything within ~34 D of the camera"""
    import lib25 as L
    cx, cy = cam[0], cam[1]; near = lambda x, y: math.hypot(x - cx, y - cy) < 34
    crushed = corridor_pred(); wetc = [(c[0], c[1], c[2] * 0.75) for c in S['craters']]
    def ok(x, y):
        if not near(x, y): return False
        for tr_ in S['trenches']:                                                         # never on a trench floor (duckboards stay clean)
            if poly_dist(np.array([x]), np.array([y]), tr_['poly'])[0][0] < tr_['hw'] + 0.15: return False
        for (a, b, r) in wetc:
            if math.hypot(x - a, y - b) < r: return False
        if S.get('tank_boxes') and S.get('cam_dict'):
            r = cam_project(S['cam_dict'], (x, y, gh(x, y) + 0.4))
            if r:
                for (u0, v0, u1, v1) in S['tank_boxes']:
                    if u0 < r[0] < u1 and v0 < r[1] < v1: return False
        return lane_ok or not crushed(x, y)
    g = []; w = []; f = []; bk = []; nok = lambda x, y: not ok(x, y)
    for tr in S['trenches']:
        pts = L.scatter_poly_edge(tr['poly'], 0, int(900 * n), seed, 0.1)
        for sg in (1, -1):
            for (x, y) in L.scatter_poly_edge(tr['poly'], sg * (tr['hw'] + 0.35), int(260 * n), seed + sg, 0.9):
                if ok(x, y): g.append((x, y))
            for (x, y) in L.scatter_poly_edge(tr['poly'], sg * (tr['hw'] + 1.4), int(120 * n), seed + 5 + sg, 1.0):
                if ok(x, y): w.append((x, y))
            for (x, y) in L.scatter_poly_edge(tr['poly'], sg * (tr['hw'] + 0.9), int(90 * n), seed + 8 + sg, 1.5):
                if ok(x, y): bk.append((x, y)); 
    for (cx_, cy_, r, dep, wat) in S['craters']:
        for (x, y) in L.scatter_disc(cx_, cy_, r * 1.45, int(90 * n), seed + int(cx_)):
            d = math.hypot(x - cx_, y - cy_)
            if d > r * 0.95 and ok(x, y): g.append((x, y))
        for (x, y) in L.scatter_disc(cx_, cy_, r * 1.5, int(14 * n), seed + 3 + int(cy_)):
            if math.hypot(x - cx_, y - cy_) > r * 0.9 and ok(x, y): w.append((x, y))
    fx, fy = focus; mid = ((cx + fx) / 2, (cy + fy) / 2); rad = min(34.0, math.hypot(fx - cx, fy - cy) * 0.7 + 8)
    for (x, y) in L.scatter_disc(mid[0], mid[1], rad, int(260 * n), seed + 30, nok): g.append((x, y))
    for (x, y) in L.scatter_disc(mid[0], mid[1], rad, int(60 * n), seed + 31, nok): w.append((x, y))
    for (x, y) in L.scatter_disc(mid[0], mid[1], rad, int(20 * n), seed + 32, nok): f.append((x, y))
    for (x, y) in L.scatter_disc(mid[0], mid[1], rad, int(110 * n), seed + 33, nok): bk.append((x, y))
    lx, ly = fx - cx, fy - cy; ln = max(1e-6, math.hypot(lx, ly)); nx_, ny_ = cx + lx / ln * 7.0, cy + ly / ln * 7.0                 # dense carpet in the nearest 14 D (bottom third of the frame)
    if P_NEAR[0]: L.dress(gh, L.scatter_disc(nx_, ny_, 7.5, int(380 * n), seed + 50, nok), None, L.scatter_disc(nx_, ny_, 7.5, int(22 * n), seed + 52, nok), None if S.get('no_bricks') else L.scatter_disc(nx_, ny_, 7.5, int((22 if S.get('clamp') else 90) * n), seed + 53, nok), seed + 9, 'near', 6, (0.16, 0.42))
    if S.get('no_bricks'): bk = []
    L.dress(gh, g, w, f, bk, seed, 'dress', 7, (0.3, 0.8))
    mb = MB(); rr = rnd(seed + 40)                                                  # broken duckboard panels, planks, iron stakes in the foreground
    for (x, y) in L.scatter_disc(mid[0], mid[1], rad * 0.8, int(10 * n), seed + 41, nok):
        ang = rr.uniform(0, 3.14); z = gh(x, y); X, Y, Z = rot_axes(ang, rr.uniform(-0.1, 0.1), rr.uniform(-0.1, 0.1))
        for k in range(5): obox(mb, Vector((x, y, z + 0.12)) + Y * (k * 0.34 - 0.7) + X * rr.uniform(-0.05, 0.05), X, Y, Z, rr.uniform(1.2, 1.8) / 2, 0.15, 0.04, S['M']['duck'])
        for dy in (-0.55, 0.55): obox(mb, Vector((x, y, z + 0.08)) + Y * dy, X, Y, Z, 1.0, 0.07, 0.07, S['M']['beam'])
    mkobj(mb, 'duck_scrap')

def front_pose_tank(spec, idx):
    import tank25 as TK
    name = spec.get('name', 'tank%d' % idx); mud = spec.get('mud', 1.0)
    H = TK.build_tank(name, mud=mud, tail_angle=0.0)
    return H

def build(preset, samples=None, quality=None):
    """Build the Front for a preset into a fresh scene: ground, trenches, wire, sandbags, village, far ring, extras, dressing, tanks, cards, sun, sky, haze, render settings."""
    import tank25 as TK, lib25 as L
    assert preset in PRESETS, preset; P = PRESETS[preset]; t0 = time.time()
    begin('front', preset, P); default_world(); S.update(P.get('world', {}))
    if 'trench0' in P: S['trenches'][0].update(P['trench0']); S['trench'] = S['trenches'][0]['poly']
    cam = P.get('cam') if isinstance(P.get('cam'), dict) else dict(loc=(0.0, -20.0, 3.0), look_at=(0.0, 0.0, 3.0), lens=24); S['cam_loc'] = cam['loc']; S['cam_dict'] = cam
    cr = P.get('cross')
    if cr: add_corridor((cr['x0'], cr['y']), 0.0, -40, 50, 4.8, 6.8)
    for tk in P.get('tanks', []):
        if not tk.get('nocorr'): add_corridor((tk['front'][0], tk['front'][1]), tk['yaw'], -15, 7, 4.7, 6.4)
    S['in_tank'] = corridor_pred(); S['in_tank_wide'] = corridor_pred(1.2)
    build_ground(); [build_trench(tr, str(i)) for i, tr in enumerate(S['trenches']) if tr.get('build', True)]; build_sandbags(); build_wire(); build_village(); far_ring(); build_water(); build_debris()
    for ex in P.get('extras', []):
        k = ex[0]
        if k == 'mg': mg_nest(ex[1], ex[2], ex[3], flash=ex[4] if len(ex) > 4 else False)
        elif k == 'op': op_post(ex[1], ex[2], ex[3])
        elif k == 'bucket': bucket_at(ex[1], ex[2])
        elif k == 'mud': mud_heaps(ex[1], ex[2], ex[3])
        elif k == 'tufts': L.dress(gh, ex[1], None, None, None, 5)
        elif k == 'clods': clods(ex[1], ex[2])
        elif k == 'bags': import lib25 as L_; mbb = MB(); L_.bag_pile(mbb, (ex[1], ex[2]), 26, 5, gh, 1.8); mkobj(mbb, 'warm_bags', smooth=True)
        elif k == 'pop': import lib25 as L_; L_.poppies('close_poppies', L_.scatter_disc(ex[1], ex[2], 2.2, 40, 7), gh, 7, ('poppy',)) ; L_.dress(gh, L_.scatter_disc(ex[1], ex[2], 2.5, 60, 8), None, None, None, 4, 'cl')
    S['tank_h'] = {}; S['tanks_h'] = []
    for i, tk in enumerate(P.get('tanks', [])):
        H = front_pose_tank(tk, i); S['tanks_h'].append(H); st = tk.get('state', 'normal'); x, y = tk['front']
        if 'build' in tk: TK.set_build(H, tk['build'])
        TK.pose_on_ground(H, x, y, tk['yaw'])
        if tk.get('nocorr') : pass
        if st == 'stuck': H.base.update(pos=tuple(H.root.location), yaw=tk['yaw'], pitch=0.0, roll=0.0); TK.set_state(H, 'stuck', 1.0)
        if tk.get('smoke'): TK.set_state(H, 'smoking', tk['smoke'])
        if tk.get('stencil') is False: TK.set_stencil(H, False)
    if cr:
        H = TK.build_tank('mk1', mud=cr.get('mud', 1.0)); S['tank'] = H; S['tanks_h'].append(H)
        TK.setup_crossing(H, (cr['x0'], cr['y']), 0.0, cr['s_a'], cr['s_b'])
        TK.set_crossing(H, S.get('cu', cr['u'])); print('crossing table', [(round(u, 2), round(TK.crossing_pose(H, u)['s'], 1), round(TK.crossing_pose(H, u)['pos'][2], 2), round(TK.crossing_pose(H, u)['pitch'], 1)) for u in np.linspace(0, 1, 11)]); H.base = dict(pos=tuple(H.root.location), yaw=0.0, pitch=0.0, roll=0.0)
        if P.get('sparks') is not None: TK.set_sparks(H, P['sparks'])
        if cr.get('stencil') is False: TK.set_stencil(H, False)
        if cr.get('smoke'): TK.set_state(H, 'smoking', 1.0)
    F_ = P.get('cam')
    if callable(F_): cam = F_(S)
    elif 'mark' in P:
        mk = dict(P['mark']); pos = mk.pop('pos'); mk.setdefault('ground', gh(pos[0], pos[1])); cam = close_cam(pos, **mk)
    S['cam_loc'] = cam['loc']; S['cam_dict'] = cam
    S['clamp'] = bool(P.get('clamp')); S['tank_boxes'] = tank_screen_boxes(cam) if S['clamp'] else []
    P_NEAR[0] = P.get('near', True); dress_front(cam['loc'], P.get('focus', cam['look_at'][:2]), P.get('dress_n', 1.0), lane_ok=P.get('lane_ok', False))
    S['cards'] = []
    for (k, xy, ht) in P.get('cards', []):
        if 'pix' in P and xy[0] > 100 and xy[1] > 100: xy = world_at_pixel(xy[0], xy[1])
        L.cards([(k, xy, ht)], gh, cam['loc'])
    finish(cam, P, samples, quality)
    S['build_s'] = time.time() - t0
    return anchors()

def close_cam(pos, face_deg, dist=4.2, lens=28, zc=1.9, ground=0.0, head=3.2, look_dz=0.0):
    """waist-up close camera for a puppet card ~3.2 D tall standing at pos=(x, y) on `ground`, facing face_deg (the card faces the camera): the camera is `dist` D away on that side at the chest height zc, level.
    With 40 mm the head sits at ~0.30-0.45 of the frame height.  The mark (card position + facing) is stored for the cast shots (anchors()['mark']); close presets render with NO puppet."""
    a = math.radians(face_deg); cam = dict(loc=(pos[0] + math.cos(a) * dist, pos[1] + math.sin(a) * dist, ground + zc), look_at=(pos[0], pos[1], ground + zc + look_dz), lens=lens)
    S['mark'] = dict(pos=(pos[0], pos[1], ground), face_deg=face_deg, height=head, dist=dist, lens=lens); return cam

def anchors():
    return dict(mark=S.get('mark'), preset=S['preset'], cam=dict(S['cam']), sun_elev=S['sun_elev'], key_dir=tuple(-S['to_sun']), build_s=S.get('build_s'))

# ============================================================================= scene prologue / epilogue shared by every location
def begin(loc, preset, P=None):
    bpy.ops.wm.read_factory_settings(use_empty=True); sc = bpy.context.scene; S.clear(); S.update(coll=sc.collection, trench_objs=[], preset=preset, loc=loc); S.update(OVR); S.update((P or {}).get('tune', {})); S.setdefault('cloud_seed', (sum(ord(c) * (i + 3) for i, c in enumerate(preset)) % 997) * 0.37); J.S.clear(); J.S['coll'] = sc.collection
    setup_world(sc, S.get('sky_k', 1.0), S.get('cloud_k', 1.0)); S['M'] = None; make_materials()
    import lib25; lib25.more_materials(); S['decal_mat'] = decal_material()
    M = S['M']; M['mud_lump'] = flat('mud_lump', '#4a3622', 0.55)
    import kit as K; K.use(sc.collection)
    return sc

def finish(cam, P, samples=None, quality=None, sun=None, haze=None):
    """light recipe (identical for every location): warm key sun 5.0 at 28 deg from the camera's left/front, bright pastel sky, thin far haze, Standard view -0.25 EV, 64 samples + OIDN"""
    sc = bpy.context.scene; S['cam'] = cam
    sun_d = bpy.data.lights.new('key_sun', 'SUN'); sun_d.color = S.get('sun_col', (1.0, 0.78, 0.50)); sun_d.energy = S.get('sun_e', 5.0); sun_d.angle = math.radians(1.6)
    so = bpy.data.objects.new('key_sun', sun_d); sc.collection.objects.link(so); S['sun'] = so
    sun = sun or P.get('sun'); az, el = (sun if sun else sun_for_camera(cam, S.get('sun_elev', 28.0), S.get('sun_left', 1.0), S.get('sun_front', 0.45)))
    set_sun(az, el); S['sun_elev'] = el
    if P.get('cast') and S.get('mark'):                                                    # real cast25 puppet at the mark (framing reference; stays in the finals)
        import lib25 as L_; mk = S['mark']; side = L_.light_side(cam, az)
        for c in P['cast']: L_.cast_card(c['story'], mk['pos'][:2], mk['pos'][2], mk['face_deg'], side, c.get('mirror', False))
    make_haze((S.get('haze', 0.0003 if S.get('mark') else 0.0009)) if haze is None else haze); make_camera(cam)
    rim = bpy.data.lights.new('rim_fill', 'SUN'); rim.color = (0.74, 0.87, 1.0); rim.energy = S.get('rim_e', 1.4); rim.angle = math.radians(25.0)                       # cool back fill / rim: from behind the subject toward the camera, no shadow
    try: rim.use_shadow = False
    except Exception: pass
    ro = bpy.data.objects.new('rim_fill', rim); sc.collection.objects.link(ro); f_ = Vector(cam['look_at']) - Vector(cam['loc']); f_.z = 0; f_.normalize(); to_rim = Vector((f_.x * math.cos(math.radians(22)), f_.y * math.cos(math.radians(22)), math.sin(math.radians(22))))
    ro.rotation_euler = (-to_rim).to_track_quat('-Z', 'Y').to_euler()
    if P.get('fill'):                                                                  # hidden soft bounce card beside the camera for close-ups (practical fill, invisible to the camera)
        fd = bpy.data.lights.new('bounce', 'AREA'); fd.shape = 'DISK'; fd.size = 14.0; fd.energy = P['fill']; fd.color = (1.0, 0.93, 0.82); fo = bpy.data.objects.new('bounce', fd); sc.collection.objects.link(fo)
        loc = Vector(cam['loc']); tgt = Vector(cam['look_at']); fo.location = loc + (tgt - loc).normalized() * 3.0 + Vector((0, 0, 3.0)); fo.rotation_euler = (tgt - fo.location).to_track_quat('-Z', 'Y').to_euler()
    S['exposure'] = S.get('exposure', -0.25); S['samples'] = samples or P.get('samples', 64); setup_render(sc, 'final')

# ============================================================================= render + post
def _rgb2lab(x):
    lin = np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4); M = np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]], np.float32)
    xyz = (lin @ M) / np.array([0.95047, 1.0, 1.08883], np.float32); f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)

def _lab2rgb(lab):
    fy = (lab[..., 0] + 16) / 116; fx = fy + lab[..., 1] / 500; fz = fy - lab[..., 2] / 200; f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * np.array([0.95047, 1.0, 1.08883], np.float32)
    Mi = np.linalg.inv(np.array([[0.4124, 0.2126, 0.0193], [0.3576, 0.7152, 0.1192], [0.1805, 0.0722, 0.9505]], np.float32)).astype(np.float32); lin = np.clip(xyz @ Mi, 0, 1)
    return np.clip(np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * np.power(lin, 1 / 2.4) - 0.055), 0, 1)

def _rgb2hsv(a):
    mx = a.max(2); mn = a.min(2); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-6), 0); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    h = np.where(d < 1e-6, 0, np.where(mx == r, ((g - b) / np.maximum(d, 1e-6)) % 6, np.where(mx == g, (b - r) / np.maximum(d, 1e-6) + 2, (r - g) / np.maximum(d, 1e-6) + 4)))
    return h, s, mx

def _hsv2rgb(h, s, v):
    c = v * s; x = c * (1 - np.abs(h % 2 - 1)); m = v - c; hi = np.floor(h).astype(int) % 6; z = np.zeros_like(c)
    r = np.choose(hi, [c, x, z, z, x, c]); g = np.choose(hi, [x, c, c, x, z, z]); b = np.choose(hi, [z, z, x, c, c, x]); return np.stack([r + m, g + m, b + m], -1)

def grade(im, mask=None, p1_t=0.035, p99_t=0.925, mean_t=0.51, knee=0.85, vib=1.4, wb=(1.5, 1.5), wb_k=0.6, wb_max=6.0, depth_k=0.12):
    """gentle final grade (director, 28 Nov): (1) levels p1 -> 0.035, p99 -> 0.925 with a soft knee above 0.85, (2) luma gamma to mean 0.51 (clamped 0.8-1.3), (3) white-balance shift of the mean Lab a*, b* toward `wb`
    at 60 % strength, at most 6 Lab units, (4) vibrance ~1.4 weighted to mid-saturation pixels (S -> S (1 + (vib-1) 4 S (1-S)); hue, value untouched: no hue shifts, no clipping).  Statistics ignore the puppet cards;
    `mask` (0..1, the cards' alpha) composites the puppets back UNGRADED so faces and costume colours stay exactly as drawn."""
    src = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0; a = src.copy(); W709 = np.array([0.2126, 0.7152, 0.0722], np.float32)
    keep = np.ones(a.shape[:2], bool) if mask is None else (mask < 0.05)
    def lum(x): return x @ W709
    L = lum(a)[keep]; lo, hi = np.percentile(L, 1), np.percentile(L, 99)
    a = (a - lo) / max(hi - lo, 1e-3) * (p99_t - p1_t) + p1_t; k = knee; a = np.where(a > k, k + (1 - k) * np.tanh((a - k) / (1 - k)), a); a = np.clip(a, 0, 1)
    lo_, hi_ = 0.8, 1.3
    for _ in range(22):
        mid = (lo_ + hi_) / 2
        if float(np.mean(lum(np.power(np.clip(a, 1e-4, 1), mid))[keep])) > mean_t: lo_ = mid
        else: hi_ = mid
    a = np.power(np.clip(a, 1e-4, 1), (lo_ + hi_) / 2)
    lab = _rgb2lab(a); sm = lab[::4, ::4][keep[::4, ::4]]; da = float(np.clip((wb[0] - sm[:, 1].mean()) * wb_k, -wb_max, wb_max)); db = float(np.clip((wb[1] - sm[:, 2].mean()) * wb_k, -wb_max, wb_max))
    lab = lab.copy(); lab[..., 1] += da; lab[..., 2] += db; a = _lab2rgb(lab)
    h, s, v = _rgb2hsv(a)
    def vibr(vb): return np.clip(s * (1 + (vb - 1) * (0.35 + 3.0 * s * (1 - s)) * (1 - s)), 0, 1)                    # mid-saturation pixels boosted most, neutrals a little, full colours not at all
    def msat(s2):
        sm_ = np.asarray(Image.fromarray((np.clip(_hsv2rgb(h[::2, ::2], s2[::2, ::2], v[::2, ::2]), 0, 1) * 255).astype(np.uint8)).resize((180, 320))).astype(np.float32) / 255; mx_, mn_ = sm_.max(2), sm_.min(2); return float(np.where(mx_ > 0, (mx_ - mn_) / np.maximum(mx_, 1e-6), 0).mean())
    vb = vib
    if msat(vibr(vb)) < 0.42:                                                               # gate: mean sat 0.40-0.50 (aim 0.40-0.48): raise the vibrance just enough (max 3.2)
        lo_, hi_ = vib, 3.2
        for _ in range(9):
            mid = (lo_ + hi_) / 2
            if msat(vibr(mid)) < 0.42: lo_ = mid
            else: hi_ = mid
        vb = hi_
    s = vibr(vb); m_ = msat(s)
    if m_ > 0.47: s = s * float(np.clip(0.46 / m_, 0.6, 1.0))                               # already vivid enough: do not exceed R11
    a = np.clip(_hsv2rgb(h, s, v), 0, 1)
    ys = np.linspace(0, 1, a.shape[0], dtype=np.float32)[:, None, None]                    # depth: foreground (lower frame) a touch darker, distance (upper frame) a touch lighter and bluer (mild aerial perspective)
    fg = 1 - depth_k * np.clip((ys - 0.62) / 0.38, 0, 1) ** 1.5; bg = depth_k * 0.55 * np.clip((0.55 - ys) / 0.55, 0, 1) ** 1.2
    a = np.clip(a * fg * (1 - bg) + np.array([0.80, 0.88, 0.97], np.float32) * bg, 0, 1)
    if mask is not None: m = np.clip(mask, 0, 1)[..., None]; a = a * (1 - m) + src * m
    return Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8))

def post(src, dst, W=720, H=1280, sharp=0.55, radius=1.1):
    """mild unsharp + clarity at native size, then the gentle grade(); the puppet cards (alpha mask from the `_mask.png` the render writes) are composited back ungraded"""
    from PIL import Image, ImageFilter
    im = Image.open(src).convert('RGB')
    if im.size != (W, H): im = im.resize((W, H), Image.LANCZOS)
    mp = src[:-8] + '_mask.png' if src.endswith('_raw.png') else None; mask = None
    if mp and os.path.exists(mp):
        mi = Image.open(mp).convert('RGBA').split()[3]
        if mi.size != (W, H): mi = mi.resize((W, H), Image.LANCZOS)
        mask = np.asarray(mi).astype(np.float32) / 255.0
        if mask.max() < 0.02: mask = None
    raw_im = im
    im = im.filter(ImageFilter.UnsharpMask(radius=radius, percent=int(sharp * 100), threshold=2)); im = im.filter(ImageFilter.UnsharpMask(radius=5, percent=int(S.get('clarity', 40)), threshold=1))
    if mask is not None:                                                            # puppet pixels: exactly as rendered (no sharpen, no grade)
        a0 = np.asarray(im).astype(np.float32); a1 = np.asarray(raw_im).astype(np.float32); m3 = mask[..., None]; im = Image.fromarray(np.clip(a0 * (1 - m3) + a1 * m3, 0, 255).astype(np.uint8))
    if S.get('grade', 1): im = grade(im, mask)
    im.save(dst)

def render_card_mask(path):
    """alpha of the puppet cards only (everything else is a holdout), so post() can keep them out of the grade"""
    sc = bpy.context.scene; cards = set(S.get('cards', []))
    if not cards: return None
    cy = sc.cycles; r = sc.render; saved = dict(ft=r.film_transparent, sm=cy.samples, ad=cy.use_adaptive_sampling, dn=cy.use_denoising, cm=r.image_settings.color_mode, bounces=cy.max_bounces)
    hold = [(o, o.is_holdout) for o in sc.objects if o.type == 'MESH' and o not in cards]
    for o, _ in hold: o.is_holdout = True
    r.film_transparent = True; cy.samples = 6; cy.use_adaptive_sampling = False; cy.use_denoising = False; r.image_settings.color_mode = 'RGBA'; cy.max_bounces = 0
    r.filepath = path; bpy.ops.render.render(write_still=True)
    for o, h in hold: o.is_holdout = h
    r.film_transparent = saved['ft']; cy.samples = saved['sm']; cy.use_adaptive_sampling = saved['ad']; cy.use_denoising = saved['dn']; r.image_settings.color_mode = saved['cm']; cy.max_bounces = saved['bounces']
    return path

def render_still(path, quality='final', samples=None, scale=None):
    sc = bpy.context.scene; setup_render(sc, quality, samples, scale); raw = path[:-4] + '_raw.png'; mp_ = raw[:-8] + '_mask.png'
    if os.path.exists(mp_): os.remove(mp_)
    w, c = T.render(raw); render_card_mask(mp_); post(raw, path); return w, c

def render_settings():
    sc = bpy.context.scene; cy = sc.cycles; r = sc.render
    return dict(resolution=[r.resolution_x * r.resolution_percentage // 100, r.resolution_y * r.resolution_percentage // 100], samples=cy.samples, adaptive_threshold=cy.adaptive_threshold, adaptive_min=cy.adaptive_min_samples,
                denoiser=cy.denoiser, prefilter=cy.denoising_prefilter, passes=cy.denoising_input_passes, bounces=dict(total=cy.max_bounces, diffuse=cy.diffuse_bounces, glossy=cy.glossy_bounces, transmission=cy.transmission_bounces),
                view=sc.view_settings.view_transform, exposure=sc.view_settings.exposure, threads=r.threads, sun=dict(energy=S['sun'].data.energy, elevation=S['sun_elev'], color=tuple(S['sun'].data.color)), haze=S.get('haze', 0.0006),
                post='unsharp r1.1 55%% + clarity r5 %d%%' % int(S.get('clarity', 40)))

def card_report():
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for o in S.get('cards', []):
        top = o.matrix_world @ Vector((0, 0, 3.2)); bot = o.matrix_world @ Vector((0, 0, 0)); a = world_to_camera_view(sc, cam, top); b = world_to_camera_view(sc, cam, bot)
        out.append((o.name, round((1 - a.y) * 1280), round((1 - b.y) * 1280), round(b.x * 720)))
    return out

def proj_report():
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = {}; pts = {}
    for i, H in enumerate(S.get('tanks_h', [])):
        r = H.root; pts['tank%d_nose' % i] = r.matrix_world @ Vector((4, 0, 3.9)); pts['tank%d_front' % i] = r.matrix_world @ Vector((0, 0, 0)); pts['tank%d_rear' % i] = r.matrix_world @ Vector((-11, 0, 3))
    for k, p in pts.items(): v = world_to_camera_view(sc, cam, p); out[k] = (round(v.x * 720), round((1 - v.y) * 1280))
    return out

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('cmd'); ap.add_argument('preset'); ap.add_argument('out'); ap.add_argument('--draft', type=float, default=0.0); ap.add_argument('--samples', type=int, default=0)
    ap.add_argument('--set', nargs='*', default=[]); a = ap.parse_args()
    for kv in a.set: k, v = kv.split('='); OVR[k] = float(v) if v.replace('.', '', 1).replace('-', '', 1).isdigit() else v
    A = build(a.preset, a.samples or None)
    print('build %.1f s' % S['build_s'], flush=True)
    if a.draft: w, c = render_still(a.out, 'draft', a.samples or 16, a.draft)
    else: w, c = render_still(a.out, 'final', a.samples or None)
    print('render %.1f s wall, %.1f s cpu' % (w, c), card_report(), proj_report(), flush=True)
    json.dump(dict(preset=a.preset, wall_s=round(w, 1), cpu_s=round(c, 1), build_s=round(S['build_s'], 1), settings=render_settings(), cards=card_report(), anchors=proj_report()), open(a.out[:-4] + '_log.json', 'w'), indent=1, default=str)
