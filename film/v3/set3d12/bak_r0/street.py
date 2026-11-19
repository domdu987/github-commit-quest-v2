#!/usr/bin/env python3
"""street.py : set of film 12 (Jonas Hanway and the first umbrella, London early 1750s) as a real 3D Blender set (bpy 5.x, Cycles CPU):
a Georgian London street in the rain at golden dusk. House look: flat unlit-style painted artwork on REAL lit geometry, one hard warm key
(a low sun behind the camera, through the cross lane), blue-violet shade, warm practicals (sash windows, shop bows, lamps), wide 22 mm camera,
no depth of field. Wet setts and puddles mirror the windows (glossy bounce 1), rain streaks are real crisp geometry.

    import street as S
    A = S.build('street_wide')            # presets: street_wide | coach_low | street_high      (all one location, STREET light)
    cam = S.make_camera(A['cams'][A['cam_name']])
    S.stage_placeholders(A, A['cam_name']); S.render('/abs/out.png')
CLI:  python3 street.py stills [preset ...]      360x640 6 samples      python3 street.py final [preset ...]      720x1280, 14 samples
      python3 street.py styleboard                renders the three board stills into styleboard/ (see STYLEBOARD.md)
World: 1 unit = 1 head (adults 3 units), Z up, road crown z 0, street along +y (x -5.2..5.2 roadway, kerbs, pavements to +-8.6, house fronts
x = +-8.6, rooflines z 19.9+). Right row (x > 0) faces the key (warm), left row is in blue shade. Coach rank on the right kerb (y 20..56).
Imports (never copies) the film 2 / 5 / 6 / 8 / 9 / 10 helpers the way harbour.py does."""
import os, sys, math, json, time, random
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d10'), os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'),
          os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import mine as MN                                          # noqa: E402
import wall as W9                                          # noqa: E402  (film-9 set: air / mist compositor)
import street_tex as ST                                    # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, _obj, _untoon, _append_shader, _light   # noqa: E402,F401
WORK = os.path.join(HERE, 'street_work')
T.ACT = os.path.join(WORK, 'actors')                       # placeholder actor art stays inside this folder
STATE = T.STATE
def _rnd(seed): return random.Random(seed)
digest = None

# ----------------------------------------------------------------------------- light
def _kdaz(az, el):
    """key_dir (travel) of a sun at azimuth az (deg from +x CCW) and elevation el."""
    e = math.radians(el); a = math.radians(az)
    return (-math.cos(a) * math.cos(e), -math.sin(a) * math.cos(e), -math.sin(e))

P_STREET = dict(toon=1.0, key_desat=0.08, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.6, wet=1.0, lamps=1.0,
                key=(2.0, 1.16, 0.5), key_dir=_kdaz(205, 60), sun_elev=60, shade=(0.17, 0.165, 0.46), shade_tint=(0.16, 0.15, 0.46), shade_mix=0.78,
                grade_offset=(0.0, -0.004, -0.008), lift=(0.008, 0.008, 0.026), sky='sky_rain', sky_k=1.0, grade_saturation=1.14,
                bounce=(1.0, 0.7, 0.45, 0.07), air=('#d8b8a8', 0.5, 60.0, 260.0), beams=0.0, rain=1.0)

PRESETS = dict(
    street_wide=dict(cam='street_wide', hero=(-0.9, 2.5, 0.0), extra=None),
    coach_low=dict(cam='coach_low', hero=None, extra='coachman'),
    street_high=dict(cam='street_high', hero=None, extra='umbrellas'),
)
CAMS = dict(
    street_wide=dict(loc=(1.2, -14.0, 3.4), look_at=(0.3, 40.0, 3.2), lens=22),
    coach_low=dict(loc=(-3.6, 4.2, 1.35), look_at=(3.6, 19.0, 3.3), lens=22),
    street_high=dict(loc=(-3.0, -20.0, 30.0), look_at=(0.5, 34.0, 1.0), lens=22),
)

X0 = 9.8                    # house front
XK = 5.9                    # roadway edge (kerb face)
XP = 6.3                    # pavement edge
ZP = 0.28                   # pavement level
Y0, Y1 = -56.0, 112.0       # row extent
LOT = 8.0
H_FAC = 19.35               # cornice base (top of the painted facade)

# ----------------------------------------------------------------------------- materials
def _wetgloss(m, k, rough, hmap=None, hscale=1.0, bump=0.25, fres=True, tint=(1.0, 0.95, 0.9)):
    """Glossy lobe with Fresnel-weighted strength (wet stone / water): the reflection of the lit windows, lamps and sky."""
    def make(nt):
        N = nt.nodes.new; L = nt.links.new
        gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
        if fres:
            fr = N('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.38
            mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = (*(c * k * 0.3 for c in tint), 1); mx.inputs[7].default_value = (*(c * k for c in tint), 1)
            L(fr.outputs['Fac'], mx.inputs[0]); L(mx.outputs[2], gl.inputs['Color'])
        else: gl.inputs['Color'].default_value = (*(c * k for c in tint), 1)
        if hmap:
            tx = N('ShaderNodeTexImage'); tx.image = T._img(hmap); tx.image.colorspace_settings.name = 'Non-Color'
            bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.05
            L(tx.outputs['Color'], bp.inputs['Height']); L(bp.outputs['Normal'], gl.inputs['Normal'])
        return gl.outputs['BSDF']
    return _append_shader(m, make)

def _mat_water(name, base='#141a3c', rough=0.02, k=1.0, deep=0.0, body=0.5):
    """Puddle / gutter water: a see-through dark blue-violet film (the setts show through, `body` = how opaque) plus a strong, almost
    mirror glossy lobe weighted by Fresnel (the windows, lamps and sky lie in it)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*T.hex_lin(base), 1); em.inputs['Strength'].default_value = 1.0
    tr = N('ShaderNodeBsdfTransparent'); mb_ = N('ShaderNodeMixShader'); mb_.inputs['Fac'].default_value = body; L(tr.outputs['BSDF'], mb_.inputs[1]); L(em.outputs['Emission'], mb_.inputs[2])
    gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
    fr = N('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.33
    mp = N('ShaderNodeMath'); mp.operation = 'MULTIPLY_ADD'; mp.inputs[1].default_value = 0.9 * k; mp.inputs[2].default_value = 0.12 + deep; mp.use_clamp = True; L(fr.outputs['Fac'], mp.inputs[0])
    gc = N('ShaderNodeMix'); gc.data_type = 'RGBA'; gc.inputs[6].default_value = (0, 0, 0, 1); gc.inputs[7].default_value = (1, 1, 1, 1); L(mp.outputs[0], gc.inputs[0]); L(gc.outputs[2], gl.inputs['Color'])
    ad = N('ShaderNodeAddShader'); L(mb_.outputs['Shader'], ad.inputs[0]); L(gl.outputs['BSDF'], ad.inputs[1]); L(ad.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_streak(name, rgb=(0.78, 0.86, 1.0), k=1.6, opacity=0.5):
    """Rain / drip streak: camera-only, a pale cool emission mixed over what is behind (crisp, not additive-blurred)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = opacity
    lp = N('ShaderNodeLightPath'); mx2 = N('ShaderNodeMixShader'); tr2 = N('ShaderNodeBsdfTransparent')
    L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2]); L(mx2.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_halo(name, image, rgb, k):
    """Camera-only additive lamp halo card."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(image)
    bw = N('ShaderNodeRGBToBW'); L(tx.outputs['Color'], bw.inputs[0]); st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = k; L(bw.outputs[0], st.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(st.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _materials(P, C, TX, tx, pre):
    M = {}
    M['cobbles'] = _wetgloss(TX('cobbles', form=False), 0.2, 0.26, hmap=tx['cobbles_h'], bump=0.5)
    M['pave'] = _wetgloss(TX('pave', form=False), 0.32, 0.12)
    M['kerb'] = _wetgloss(TX('kerb'), 0.22, 0.14)
    M['gutter'] = _mat_water(pre + 'gutterw', '#1d2a58', 0.05, 0.9, body=0.3)
    M['gutter_flow'] = TX('gutter', form=False, glow='gutter', glow_k=0.18)
    for k in ('fac_a', 'fac_b', 'fac_c', 'fac_d', 'fac_e', 'fac_f', 'fac_s1', 'fac_s2', 'fac_s3', 'fac_s4'):
        M[k] = TX(k, glow=k + '_glow', glow_k=1.25 * P['lamps'])
    M['brick_a'] = TX('brickwall_a'); M['brick_b'] = TX('brickwall_b')
    M['slate'] = TX('slate'); M['wood'] = TX('wood'); M['wood_d'] = TX('wood_d')
    M['barrel'] = TX('barrel'); M['awn_a'] = TX('awn_a', sm=(1.2, 1.0, 1.0)); M['awn_b'] = TX('awn_b')
    M['cream'] = C('#eadfc0'); M['stone'] = C('#cfc6b0'); M['stone_d'] = C('#9a94a0')
    M['iron'] = _wetgloss(C('#26262e', 1.0, 1.2), 0.5, 0.25, fres=False)
    M['iron_b'] = C('#1c1c24', 1.0, 1.2)
    M['brass'] = _wetgloss(C('#c4902c', 1.0, (2.0, 1.4, 0.6), smix=0.2), 0.6, 0.25, fres=False, tint=(1.0, 0.8, 0.5))
    M['green'] = C('#2f5c46'); M['oxblood'] = C('#6e2433'); M['navy'] = C('#2b3f66'); M['cream_w'] = C('#f2ead4')
    M['lead'] = C('#5a5e6c', 1.0, 1.1); M['pot'] = C('#b8683c')
    M['coach'] = C('#1c3a30', 1.0, 1.2); M['coach_d'] = C('#14231f', 1.0, 1.2); M['coach_gold'] = C('#c8a040', 1.0, (1.6, 1.3, 0.7), smix=0.2)
    M['coach_side'] = TX('coach_side', form=False, glow='coach_side_glow', glow_k=1.5 * P['lamps'])
    M['wheel'] = C('#3a2a1c', 1.0, 1.1); M['wheel_r'] = C('#7a2c26', 1.0, (1.3, 0.9, 0.8), smix=0.3); M['cloth'] = C('#6e2230', 1.0, (1.4, 0.8, 0.8), smix=0.3)
    M['leather'] = C('#3a2a22', 1.0, 1.1)
    M['horse'] = C('#7c4528', 1.0, (1.3, 1.0, 0.9), smix=0.3); M['horse_d'] = C('#3a2216'); M['horse_w'] = C('#f0e6d4'); M['hoof'] = C('#1c1a1e')
    M['canvas'] = C('#d4c298'); M['sack'] = C('#b8a070'); M['umb_dark'] = C('#141622', 0.8, 1.0)
    M['umb_brown'] = C('#5a3a2a'); M['umb_green'] = C('#2c4a3a'); M['umb_blue'] = C('#2a3a68'); M['umb_red'] = C('#7a2a30')
    M['pink'] = TX('lace', form=False, alpha=True, sm=(1.2, 1.0, 1.1), smix=0.3)
    M['cabbage'] = C('#5c9a4a', 1.0, (1.2, 1.1, 1.0), smix=0.3); M['carrot'] = C('#e07a2a', 1.0, (1.3, 0.9, 0.8), smix=0.3); M['apple'] = C('#b8302a', 1.0, (1.3, 0.8, 0.8), smix=0.3)
    M['turnip'] = C('#e8dcc8'); M['onion'] = C('#c89a50'); M['turnip_top'] = C('#8a4a8a')
    M['glass_lamp'] = mat_emit(pre + 'e_lamp', '#ffd890', strength=4.2); M['lantern'] = mat_emit(pre + 'e_lantern', '#ffc070', strength=3.4)
    M['shopwin'] = {k: mat_emit(pre + 'e_sw_' + k, image=tx['shopwin_' + k], strength=1.25) for k in ('boots', 'teapots', 'pretzels', 'greens')}
    M['sign'] = {k: TX('sign_' + k, form=False, alpha=True) for k in ('boot', 'teapot', 'pretzel')}
    M['puddle'] = _mat_water(pre + 'pud', '#222c64', 0.012, 0.8, deep=-0.04, body=0.66); M['puddle_s'] = _mat_water(pre + 'pud_s', '#2a3670', 0.06, 0.5, deep=-0.08, body=0.42)
    M['ripple'] = {k: mat_emit(pre + 'e_rip_' + k, image=tx['ripples_' + k], strength=0.6, alpha=True) for k in ('a', 'b')}
    M['rain'] = _mat_streak(pre + 'rain', (0.82, 0.9, 1.0), 1.5, 0.42); M['drip'] = _mat_streak(pre + 'drip', (0.86, 0.92, 1.0), 1.5, 0.55)
    M['halo'] = _mat_halo(pre + 'halo', tx['halo'], (1.0, 0.62, 0.26), 1.3); M['halo_w'] = _mat_halo(pre + 'halo_w', tx['halo'], (1.0, 0.7, 0.4), 0.7)
    M['sky'] = mat_emit(pre + 'sky', image=tx['sky_rain'], strength=P['sky_k'])
    M['flame'] = mat_emit(pre + 'e_flame', '#ffe8a8', strength=7.0)
    return M

# ----------------------------------------------------------------------------- tiny geometry helpers
def qface(mb, p0, pu, pv, mat, uv, normal):
    p0, pu, pv = Vector(p0), Vector(pu), Vector(pv); u0, v0, u1, v1 = uv
    mb.oface([p0, p0 + pu, p0 + pu + pv, p0 + pv], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], normal)

def bx(mb, lo, hi, mat, **kw):
    mb.box(lo, hi, mat, **kw)

def cyl(mb, p0, p1, r, mat, seg=8, r1=None, caps=True):
    mb.frustum(p0, p1, r, r if r1 is None else r1, mat, seg=seg, cap0=caps, cap1=caps)

def streak_poly(mb, mat, p, d, side, L, w):
    """Pointed ribbon centred at p along unit d, half width w/2 along unit side."""
    p = Vector(p); a = p - d * (L / 2); b = p + d * (L / 2); s = side * (w / 2)
    mb.face([a, p - s * 0.9 + d * (-L * 0.15), p - s + d * (L * 0.15), b, p + s + d * (L * 0.15), p + s * 0.9 + d * (-L * 0.15)][::-1] if False else [a, p + s + d * (-L * 0.1), b, p - s + d * (-L * 0.1)], mat)

# ----------------------------------------------------------------------------- the ground
def _ground(SET, M):
    mb = MB(); T4 = 4.0
    # roadway: setts, UV = world / 4
    def ground_quad(x0, x1, y0, y1, z, mat, tile=T4):
        qface(mb, (x0, y0, z), (x1 - x0, 0, 0), (0, y1 - y0, 0), mat, (x0 / tile, y0 / tile, x1 / tile, y1 / tile), (0, 0, 1))
    ground_quad(-XK, XK, Y0 - 40, Y1 + 120, 0.0, M['cobbles'])
    # the cross lane (left) and the wide ground behind the rows
    ground_quad(-60, -XK, 44, 52, 0.0, M['cobbles']); ground_quad(XK, 60, 44, 52, 0.0, M['cobbles']) if False else None
    mb2 = MB(); mb2.mats = mb.mats
    _obj(mb, 'road', SET)
    pv = MB()
    for s in (-1, 1):
        x0, x1 = (XP, X0 + 0.6) if s > 0 else (-X0 - 0.6, -XP)
        qface(pv, (x0, Y0 - 40, ZP), (x1 - x0, 0, 0), (0, Y1 + 160 - Y0, 0), M['pave'], (x0 / 4, (Y0 - 40) / 4, x1 / 4, (Y1 + 120) / 4), (0, 0, 1))
        # kerb: top and face
        kx = s * XK
        qface(pv, (min(XK, XP) * s, Y0 - 40, ZP), (s * 0.4 * (1 if s > 0 else 1) * (1 if True else 0), 0, 0), (0, Y1 + 160 - Y0, 0), M['kerb'], (0, 0, 0.1, (Y1 + 120 - Y0) / 4), (0, 0, 1)) if False else None
        lo = (XK, Y0 - 40, 0.0) if s > 0 else (-XP, Y0 - 40, 0.0); hi = (XP, Y1 + 120, ZP) if s > 0 else (-XK, Y1 + 120, ZP)
        pv.box(lo, hi, M['kerb'], tile=(4, 4))
    # the pavement is cut by the lane: lay the lane across it as a sunk strip (cobbles over the slab)
    _obj(pv, 'pavement', SET)
    # lane floor (covers pavement slab strip at y 44..52 on the left)
    ln = MB(); qface(ln, (-X0 - 0.6, 44, ZP + 0.01), (X0 + 0.6 - XP, 0, 0), (0, 8, 0), M['cobbles'], ((-X0 - 0.6) / 4, 11, -XP / 4, 13), (0, 0, 1)); _obj(ln, 'lane_floor', SET)
    # a dark ground far out behind the rows (never seen from the street, filled for the high shot)
    gb = MB(); qface(gb, (-90, Y0 - 40, -0.05), (180, 0, 0), (0, Y1 - Y0 + 160, 0), M['cobbles'], (-20, 0, 20, 40), (0, 0, 1)); _obj(gb, 'ground_far', SET)
    # gutters: a shallow channel with running water next to each kerb
    gt = MB()
    for s in (-1, 1):
        xa, xb = (XK - 0.75, XK - 0.05) if s > 0 else (-XK + 0.05, -XK + 0.75)
        qface(gt, (xa, Y0 - 40, 0.03), (xb - xa, 0, 0), (0, Y1 + 120 - Y0 + 40, 0), M['gutter_flow'], (0, 0, 1, (Y1 + 120 - Y0 + 40) / 4), (0, 0, 1))
    go = _obj(gt, 'gutters', SET)
    gm = MB()
    for s in (-1, 1):
        xa, xb = (XK - 0.75, XK - 0.05) if s > 0 else (-XK + 0.05, -XK + 0.75)
        qface(gm, (xa, Y0 - 40, 0.035), (xb - xa, 0, 0), (0, Y1 + 120 - Y0 + 40, 0), M['gutter'], (0, 0, 1, 1), (0, 0, 1))
    _obj(gm, 'gutter_water', SET)
    return

def _blob(cx, cy, r, rs, n=40, sq=1.0):
    pts = []; ph = rs.uniform(0, 6.28); a1, a2, a3 = rs.uniform(0.08, 0.16), rs.uniform(0.05, 0.1), rs.uniform(0.02, 0.05)
    for i in range(n):
        t = 2 * math.pi * i / n; rr = r * (1 + a1 * math.sin(2 * t + ph) + a2 * math.sin(3 * t + ph * 1.7) + a3 * math.sin(5 * t + ph * 0.6))
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t) * sq))
    return pts

def _puddles(SET, M, preset):
    """Layered puddles: a wide shallow wet sheet with a smaller, deeper (more mirror-like) pool inside, and soft ripple-ring decals
    where drips fall. Positions: dense in front of the camera, along both gutters and in the coach rank."""
    rs = _rnd(5); big = MB(); inner = MB(); rip = MB(); spots = []
    near = {'street_wide': (-14, 30), 'coach_low': (0, 28), 'street_high': (-10, 70)}[preset]
    for i in range(46):
        y = rs.uniform(*near) if i < 38 else rs.uniform(-30, 90)
        side = rs.choice([-1, 1]); x = rs.choice([rs.uniform(-4.2, 4.2), side * rs.uniform(3.0, 5.0), rs.uniform(-2, 2)])
        r = rs.uniform(0.8, 2.4) * (1.35 if rs.random() < 0.25 else 1.0); spots.append((x, y, r))
    spots += [(-1.2, 7.2, 2.2), (2.2, 3.8, 1.7), (0.2, 14.0, 2.6), (3.6, 8.5, 1.6), (-2.8, 20.0, 2.0), (4.0, 24.0, 1.9)]
    for (x, y, r) in spots:
        if abs(x) > XK - 0.3: continue
        pts = _blob(x, y, r, rs, 40, sq=rs.uniform(0.7, 1.25))
        c = Vector((x, y, 0.012)); ring = [Vector((px, py, 0.012)) for px, py in pts]
        for i in range(len(ring)): big.face([c, ring[i], ring[(i + 1) % len(ring)]][::-1] if False else [ring[(i + 1) % len(ring)], ring[i], c], M['puddle_s'])
        pts2 = _blob(x + rs.uniform(-0.1, 0.1) * r, y + rs.uniform(-0.1, 0.1) * r, r * 0.62, rs, 36, sq=rs.uniform(0.7, 1.2)); c2 = Vector((x, y, 0.02))
        ring2 = [Vector((px, py, 0.02)) for px, py in pts2]
        for i in range(len(ring2)): inner.face([ring2[(i + 1) % len(ring2)], ring2[i], c2], M['puddle'])
        # ripple rings: 1-2 decals per puddle (square quads aligned to the ground, ellipses by perspective)
        for k in range(rs.choice([1, 2])):
            rx, ry = x + rs.uniform(-0.45, 0.45) * r, y + rs.uniform(-0.4, 0.4) * r; sz = rs.uniform(0.35, 0.7) * min(r, 1.6) * 1.2
            qface(rip, (rx - sz, ry - sz, 0.03), (2 * sz, 0, 0), (0, 2 * sz, 0), M['ripple']['a' if rs.random() < 0.5 else 'b'], (rs.uniform(0, 0.5), rs.uniform(0, 0.5), 0, 0) if False else (0, 0, 1, 1), (0, 0, 1))
    _obj(big, 'puddles_shallow', SET, shadow=False); _obj(inner, 'puddles_deep', SET, shadow=False); ro = _obj(rip, 'ripples', SET, shadow=False)
    return spots

# ----------------------------------------------------------------------------- houses
LEFT_SEQ = ['fac_b', 'fac_s2', 'fac_c', 'fac_a', 'fac_f', 'fac_s1', 'fac_e', 'fac_d', 'fac_s3', 'fac_b', 'fac_c', None, 'fac_f', 'fac_s4', 'fac_a', 'fac_e', 'fac_d', 'fac_c', 'fac_b', 'fac_f', 'fac_a', 'fac_s2']
RIGHT_SEQ = ['fac_d', 'fac_a', 'fac_s1', 'fac_e', 'fac_c', 'fac_b', 'fac_s3', 'fac_f', 'fac_a', 'fac_s4', 'fac_d', 'fac_c', 'fac_e', 'fac_s2', 'fac_b', 'fac_f', 'fac_a', 'fac_c', 'fac_d', 'fac_e', 'fac_s1', 'fac_b']
SHOPKIND = dict(fac_s1='boots', fac_s2='teapots', fac_s3='pretzels', fac_s4='greens')
SIGNKIND = dict(fac_s1='boot', fac_s2='teapot', fac_s3='pretzel', fac_s4=None)
SHOP_DOOR = dict(fac_s1=0, fac_s2=1, fac_s3=0, fac_s4=1)
DOORCOL = dict(fac_a='green', fac_b='oxblood', fac_c='navy', fac_d='green', fac_e='oxblood', fac_f='green')
DOORBAY = dict(fac_a=1, fac_b=0, fac_c=2, fac_d=0, fac_e=1, fac_f=2)

class Row:
    """Collects the geometry of one terrace side into a few merged meshes (one per kind) so the scene stays light."""
    def __init__(s, name): s.name = name; s.fac = MB(); s.trim = MB(); s.roof = MB(); s.brk = MB(); s.iron = MB(); s.misc = MB(); s.glass = MB(); s.awn = MB(); s.sign = MB()

def _house(R, M, side, y0, fac, rs, lot_i):
    """One terrace house. side +1: right row (front at x = +X0, faces -x). y0 = the lot's low-y edge."""
    s = side; xf = s * X0; dirn = -s                              # outward normal of the front (toward the street)
    nrm = (dirn, 0, 0)
    # frame helpers: u along the front runs along -y for the right row (seen from the street, left to right), +y for the left row
    def Y(u): return y0 + (LOT - u if s > 0 else u)               # world y of texture coordinate u (units from the left edge as seen from the street)
    def box_f(u0, u1, z0, z1, depth, mat, d0=0.0, **kw):          # box protruding from the front by depth (from d0)
        ya, yb = sorted((Y(u0), Y(u1))); xa, xb = sorted((xf + dirn * d0, xf + dirn * (d0 + depth)))
        R.trim.box((xa, ya, z0), (xb, yb, z1), mat, **kw)
    # painted facade quad: u = x/8, v = z/20
    mat = M[fac]
    z1 = H_FAC; v1 = z1 / ST.FACADE_H
    p0 = (xf, Y(0), 0.0); pu = (0, Y(LOT) - Y(0), 0); pv = (0, 0, z1)
    qface(R.fac, p0, pu, pv, mat, (0, 0, 1, v1), nrm)
    # string courses and plinth, cornice, parapet
    box_f(0, 8, 5.45, 5.85, 0.16, M['cream']); box_f(0, 8, 10.75, 10.95, 0.1, M['cream']); box_f(0, 8, 15.05, 15.25, 0.1, M['cream'])
    box_f(0, 8, 0.0, 0.95, 0.12, M['stone'])
    box_f(0, 8, 19.35, 19.62, 0.95, M['cream']); box_f(0, 8, 19.62, 19.9, 0.7, M['cream_w'])
    ph = rs.choice([0.7, 1.0, 1.4, 1.8]) if rs.random() < 0.35 else 1.0
    box_f(0, 8, 19.9, 19.9 + ph, 0.0, M['brick_a' if rs.random() < 0.6 else 'brick_b'], d0=0.1) if False else None
    # parapet as a thin brick wall with stone coping
    ya, yb = sorted((Y(0), Y(8))); xa, xb = sorted((xf - dirn * 0.02, xf - dirn * 0.55))
    pw = M['brick_a' if lot_i % 2 else 'brick_b']
    R.brk.box((min(xa, xb), ya, 19.9), (max(xa, xb), yb, 19.9 + ph), pw, tile=(4, 4))
    xa2, xb2 = sorted((xf + dirn * 0.15, xf - dirn * 0.75)); R.trim.box((xa2, ya, 19.9 + ph), (xb2, yb, 19.9 + ph + 0.22), M['stone'])
    # window sills and lintels (painted too; the relief catches the key)
    xs = (1.4, 4.0, 6.6)
    for fi, (zc, h) in enumerate(((8.1, 3.3), (12.7, 3.1), (16.9, 2.4))):
        for cx in xs:
            box_f(cx - 0.95, cx + 0.95, zc - h / 2 - 0.2, zc - h / 2, 0.32, M['cream'])
            box_f(cx - 1.0, cx + 1.0, zc + h / 2 + 0.04, zc + h / 2 + 0.44, 0.14, M['cream'])
    shop = fac in SHOPKIND
    if not shop:
        db = DOORBAY[fac]; dx = xs[db]
        for cx in xs:
            if cx == dx: continue
            box_f(cx - 0.95, cx + 0.95, 1.65, 1.85, 0.3, M['cream']); box_f(cx - 1.0, cx + 1.0, 4.4, 4.8, 0.14, M['cream'])
        # door surround: pilasters, entablature, triangular pediment, three steps, a lamp bracket
        box_f(dx - 1.0, dx - 0.72, 0.95, 4.9, 0.34, M['cream']); box_f(dx + 0.72, dx + 1.0, 0.95, 4.9, 0.34, M['cream'])
        box_f(dx - 1.15, dx + 1.15, 4.9, 5.2, 0.5, M['cream_w'])
        y_a, y_b = Y(dx - 1.15), Y(dx + 1.15); yc = (y_a + y_b) / 2
        pts = [(xf + dirn * 0.5, y_a, 5.2), (xf + dirn * 0.5, y_b, 5.2), (xf + dirn * 0.5, yc, 5.2 + 0.7)]
        for k in range(3):
            d0 = 0.35 + 0.3 * k; box_f(dx - 1.05 - 0.1 * (2 - k), dx + 1.05 + 0.1 * (2 - k), ZP * 0 + 0.0, 0.3 + 0.0 * k, 0.0, M['stone']) if False else None
        for k in range(3):
            d0 = 0.12 + 0.34 * k; zt = ZP + 0.0
            box_f(dx - 1.05, dx + 1.05, 0.0, 0.28 - 0.0 * k + 0.0, 0.0, M['stone']) if False else None
        # the pavement is z 0.28; steps rise to the door sill (z 0.95)
        for k in range(3):
            d0 = 0.15 + 0.4 * (2 - k); box_f(dx - 1.0, dx + 1.0, 0.0, ZP + 0.22 * (k + 1), 0.45, M['stone'], d0=d0 - 0.0)
        # triangular pediment: 3 faces (front = painted via cream) as a prism
        d_f = 0.5; xp = xf + dirn * d_f
        R.trim.face([(xf + dirn * 0.1, y_a, 5.2), (xf + dirn * 0.1, y_b, 5.2), (xf + dirn * 0.1, yc, 5.9)], M['cream_w'])
        R.trim.oface([(xp, y_a, 5.2), (xp, y_b, 5.2), (xp, yc, 5.9)], M['cream_w'], [(0, 0), (1, 0), (0.5, 0.5)], nrm)
        R.trim.oface([(xf + dirn * 0.1, y_a, 5.2), (xp, y_a, 5.2), (xp, yc, 5.9), (xf + dirn * 0.1, yc, 5.9)], M['cream'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 1))
        R.trim.oface([(xf + dirn * 0.1, y_b, 5.2), (xp, y_b, 5.2), (xp, yc, 5.9), (xf + dirn * 0.1, yc, 5.9)], M['cream'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 1))
        # lamp over the door: brass bracket + a small glass lantern
        lam = Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.0)); R.glass.sphere(lam, 0.17, M['glass_lamp'], seg=8, rings=5)
        R.iron.frustum(Vector((xf + dirn * 0.05, Y(dx + 1.35), 5.4)), Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.4)), 0.035, 0.035, M['iron'], seg=4)
        R.iron.frustum(Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.4)), Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.2)), 0.03, 0.03, M['iron'], seg=4)
        # area railings in front of the ground-floor windows
        for cx in xs:
            if cx == dx: continue
            _railing(R.iron, M, xf + dirn * 0.95 + 0.0, Y(cx - 1.25), Y(cx + 1.25), ZP, 1.7, s)
    else:
        kind = SHOPKIND[fac]; db = SHOP_DOOR[fac]
        u0, u1 = (2.6, 7.7) if db == 0 else (0.3, 5.6)
        _bow(R, M, s, y0, u0, u1, xf, dirn, Y, kind, fac)
        # fascia projection
        box_f(0, 8, 4.55, 5.45, 0.3, M[{'fac_s1': 'green', 'fac_s2': 'oxblood', 'fac_s3': 'navy', 'fac_s4': 'wood'}[fac]])
        box_f(0, 8, 5.45, 5.5, 0.34, M['brass']) if False else None
        # shop door steps and a lamp
        dx0 = 0.6 if db == 0 else 5.9
        for k in range(2):
            box_f(dx0 - 0.1, dx0 + 1.8, 0.0, ZP + 0.2 * (k + 1), 0.4, M['stone'], d0=0.1 + 0.4 * (1 - k))
        # hanging sign on an iron bracket at the pavement end of the fascia
        sk = SIGNKIND[fac]
        if sk:
            _sign(R, M, s, Y(7.5 if db == 0 else 0.5), xf, dirn, sk, rs)
        if fac == 'fac_s3' or fac == 'fac_s4':
            _awning(R, M, s, Y, xf, dirn, 'awn_a' if fac == 'fac_s3' else 'awn_b', u0, u1)
    # rainwater pipe at the left edge (as seen from the street) and a hopper head
    yp = Y(0.15); R.iron.frustum(Vector((xf + dirn * 0.18, yp, 0.3)), Vector((xf + dirn * 0.18, yp, 19.1)), 0.11, 0.11, M['lead'], seg=6)
    R.iron.box if False else None
    for zc in (4.0, 9.0, 14.0): R.iron.frustum(Vector((xf + dirn * 0.18, yp, zc)), Vector((xf + dirn * 0.18, yp, zc + 0.14)), 0.16, 0.16, M['iron_b'], seg=6)
    R.trim.box((min(xf + dirn * 0.0, xf + dirn * 0.5), yp - 0.3, 18.5), (max(xf + dirn * 0.0, xf + dirn * 0.5), yp + 0.3, 19.3), M['lead'])
    # chimneys + roof
    _roof(R, M, s, y0, xf, dirn, ph, rs, lot_i)

def _railing(mb, M, x, ya, yb, z0, h, s):
    """Iron area railing along y from ya to yb at x: spear-top rods every 0.45, two rails."""
    lo, hi = min(ya, yb), max(ya, yb); n = max(2, int((hi - lo) / 0.45))
    for i in range(n + 1):
        y = lo + (hi - lo) * i / n
        mb.frustum(Vector((x, y, z0)), Vector((x, y, z0 + h)), 0.035, 0.035, M['iron'], seg=4, cap0=False, cap1=False)
        mb.frustum(Vector((x, y, z0 + h)), Vector((x, y, z0 + h + 0.2)), 0.07, 0.0, M['iron'], seg=4, cap0=True, cap1=False)
    for zr in (z0 + 0.25, z0 + h - 0.2): mb.frustum(Vector((x, lo, zr)), Vector((x, hi, zr)), 0.035, 0.035, M['iron'], seg=4)
    for y in (lo, hi): mb.frustum(Vector((x, y, z0)), Vector((x, y, z0 + h + 0.1)), 0.075, 0.075, M['iron'], seg=5)

def _bow(R, M, s, y0, u0, u1, xf, dirn, Y, kind, fac):
    """Bow shop window: a 6-facet curve in front of the shopfront, glass painted with the goods (lit from inside), stallriser,
    mullions, a transom board and a cornice shelf. u0..u1: the window span along the front (as seen from the street)."""
    n = 6; depth = 1.05; zb, zt = 1.35, 4.15; M_w = M['shopwin'][kind]
    pts = []
    for i in range(n + 1):
        t = i / n; u = u0 + (u1 - u0) * t; d = depth * (1 - (2 * t - 1) ** 2) ** 0.7 if 0 < i < n else 0.0
        d = depth * math.sin(math.pi * t) ** 0.6 if 0 < i < n else 0.0
        pts.append((Y(u), xf + dirn * (0.1 + d)))
    for i in range(n):
        (ya, xa), (yb, xb) = pts[i], pts[i + 1]
        mat = M_w
        R.glass.oface([(xa, ya, zb), (xb, yb, zb), (xb, yb, zt), (xa, ya, zt)], mat, [(i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1)], (dirn, 0, 0))
        # stallriser (painted board) and transom board, flat sides
        R.trim.oface([(xa, ya, 0.0), (xb, yb, 0.0), (xb, yb, zb), (xa, ya, zb)], M['wood_d'], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
        R.trim.oface([(xa, ya, zt), (xb, yb, zt), (xb, yb, 4.55), (xa, ya, 4.55)], M['wood_d'], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
    for i in range(n + 1):
        ya, xa = pts[i]; R.trim.box((xa - 0.07, ya - 0.07, 0.0), (xa + 0.07, ya + 0.07, 4.55), M['cream_w'])
    # window shelf / sill (counter) and top cornice shelf
    for i in range(n):
        (ya, xa), (yb, xb) = pts[i], pts[i + 1]
        R.trim.oface([(xa, ya, zb - 0.0), (xb, yb, zb), (xb + dirn * 0.12, yb, zb), (xa + dirn * 0.12, ya, zb)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
        R.trim.oface([(xa, ya, 4.55), (xb, yb, 4.55), (xb + dirn * 0.2, yb, 4.55), (xa + dirn * 0.2, ya, 4.55)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
        R.trim.oface([(xa, ya, zt), (xb, yb, zt), (xb, yb, zt - 0.0), (xa, ya, zt)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1)) if False else None
    # a window lamp glow: warm light spilling out onto the pavement (real light, small)
    ym = (pts[n // 2][0]); xm = pts[n // 2][1] + dirn * 1.2
    STATE.setdefault('shop_lights', []).append((Vector((xm, ym, 2.6)), kind))

def _sign(R, M, s, y_wall, xf, dirn, kind, rs):
    """Iron bracket from the wall with a scroll ring, two short chains, a board hanging on them: a picture, no letters."""
    arm = 2.7; z = 6.3; y = y_wall; mat = M['sign'][kind]
    R.iron.frustum(Vector((xf + dirn * 0.1, y, z)), Vector((xf + dirn * (0.1 + arm), y, z)), 0.055, 0.055, M['iron'], seg=5)
    R.iron.frustum(Vector((xf + dirn * 0.1, y, z - 1.1)), Vector((xf + dirn * (0.1 + arm * 0.85), y, z - 0.05)), 0.04, 0.04, M['iron'], seg=4)
    # scroll: a ring under the arm
    for i in range(10):
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10; r0 = 0.45
        c = Vector((xf + dirn * (0.1 + arm * 0.45), y, z - 0.55))
        R.iron.frustum(c + Vector((dirn * r0 * math.cos(a0), 0, r0 * math.sin(a0))), c + Vector((dirn * r0 * math.cos(a1), 0, r0 * math.sin(a1))), 0.03, 0.03, M['iron'], seg=4, cap0=False, cap1=False)
    # board: its broad faces look along the street (normal +-y), hangs 0.6 below the arm; width 2.0 (into the street), height 2.4
    xb0 = xf + dirn * (0.55); xb1 = xf + dirn * (0.55 + 2.0); xa, xb = min(xb0, xb1), max(xb0, xb1); zt = z - 0.55; zb = zt - 2.4
    ym0, ym1 = y - 0.07, y + 0.07
    R.sign.box((xa, ym0, zb), (xb, ym1, zt), M['wood_d'], mats=dict(front=mat, back=mat))
    # the board is built with box(): front face (-y) uses UV 0..1 along +x. Mirror for the left row so the picture is not reversed on the viewer's side
    for xe in (xa + 0.25, xb - 0.25): R.iron.frustum(Vector((xe, y, zt)), Vector((xe, y, z)), 0.025, 0.025, M['iron'], seg=3)

def _awning(R, M, s, Y, xf, dirn, mat, u0, u1):
    """Striped canvas awning over the bow window: slopes from the fascia down toward the street, side triangles."""
    ya, yb = Y(u0 - 0.2), Y(u1 + 0.2); zt0, zt1 = 4.65, 3.95; d = 2.4
    xa = xf + dirn * 0.3; xb = xf + dirn * (0.3 + d)
    R.awn.oface([(xa, ya, zt0), (xa, yb, zt0), (xb, yb, zt1), (xb, ya, zt1)], M[mat], [(0, 0), (1, 0), (1, 1), (0, 1)], (dirn * 0.5, 0, 1))
    R.awn.oface([(xb, ya, zt1), (xb, yb, zt1), (xb, yb, zt1 - 0.45), (xb, ya, zt1 - 0.45)], M[mat], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
    for yy in (ya, yb):
        R.awn.face([Vector((xa, yy, zt0)), Vector((xb, yy, zt1)), Vector((xb, yy, zt1 - 0.0))], M[mat])
    for yy in (ya, yb): R.iron.frustum(Vector((xa, yy, zt0 - 0.1)), Vector((xb, yy, zt1 - 0.1)), 0.04, 0.04, M['iron'], seg=4)

def _roof(R, M, s, y0, xf, dirn, ph, rs, lot_i):
    """Slate roof behind the parapet (two pitches, ridge parallel to the street) and two chimney stacks with pots."""
    depth = 11.5; ridge_h = 4.6; zt = 19.9 + ph
    xa = xf - dirn * 0.5; xr = xf - dirn * (0.5 + depth / 2); xb = xf - dirn * (0.5 + depth)
    ya, yb = y0, y0 + LOT
    R.roof.oface([(xa, ya, zt - 0.3), (xa, yb, zt - 0.3), (xr, yb, zt + ridge_h), (xr, ya, zt + ridge_h)], M['slate'], [(0, 0), (LOT / 4, 0), (LOT / 4, 1.3), (0, 1.3)], (-dirn * 0.6, 0, 1))
    R.roof.oface([(xr, ya, zt + ridge_h), (xr, yb, zt + ridge_h), (xb, yb, zt - 0.3), (xb, ya, zt - 0.3)], M['slate'], [(0, 0), (LOT / 4, 0), (LOT / 4, 1.3), (0, 1.3)], (dirn * 0.6, 0, 1))
    # gable ends: simple dark brick triangles on the party walls (seen from the high camera)
    for yy, nn in ((ya, (0, -1, 0)), (yb, (0, 1, 0))):
        R.brk.oface([(xa, yy, zt - 0.3), (xb, yy, zt - 0.3), (xr, yy, zt + ridge_h)], M['brick_b'], [(0, 0), (3, 0), (1.5, 1.3)], nn)
    # chimneys on the ridge line near the party walls
    for (yy, k) in ((ya + 0.7, 0), (yb - 0.7, 1)):
        if rs.random() < 0.15: continue
        hh = rs.uniform(3.0, 4.2); c0 = Vector((xr + dirn * rs.uniform(-0.8, 0.8), yy, zt + ridge_h - 0.4)); w = 0.85
        R.brk.box((c0.x - w / 2, c0.y - w / 2, c0.z), (c0.x + w / 2, c0.y + w / 2, c0.z + hh), M['brick_b' if k else 'brick_a'], tile=(4, 4))
        R.trim.box((c0.x - w / 2 - 0.1, c0.y - w / 2 - 0.1, c0.z + hh), (c0.x + w / 2 + 0.1, c0.y + w / 2 + 0.1, c0.z + hh + 0.18), M['stone'])
        for dxp in (-0.2, 0.2):
            R.misc.frustum(Vector((c0.x + dxp * 0.0, c0.y + dxp, c0.z + hh + 0.18)), Vector((c0.x, c0.y + dxp, c0.z + hh + 0.18 + 0.95)), 0.2, 0.15, M['pot'], seg=8)

def _row_finish(SET, R, side):
    out = []
    for nm, mb in (('fac', R.fac), ('trim', R.trim), ('roof', R.roof), ('brk', R.brk), ('iron', R.iron), ('misc', R.misc), ('glass', R.glass), ('awn', R.awn), ('sign', R.sign)):
        if mb.f:
            o = _obj(mb, 'row%+d_%s' % (side, nm), SET); out.append(o)
    return out

def _lane_walls(SET, M, rs):
    """Side walls of the two houses flanking the cross lane on the left, and the backdrop houses beyond (sunlit through the lane)."""
    mb = MB(); y_a, y_b = 44.0, 52.0
    for (yy, nn) in ((y_a, (0, 1, 0)), (y_b, (0, -1, 0))):
        qface(mb, (-X0, yy, 0), (-12.0, 0, 0), (0, 0, H_FAC + 1.2), M['brick_a'], (0, 0, 3, 5), nn)
    # lane end wall + a backdrop house front
    qface(mb, (-24.0, y_a, 0), (0, 8, 0), (0, 0, 22), M['brick_b'], (0, 0, 2, 5), (1, 0, 0))
    _obj(mb, 'lane_walls', SET)
    # lane: a hanging lantern across and a barrel
    return

def _end_block(SET, M):
    """A terrace closing the far end of the street (y = Y0 + 22 lots): seven fronts across, cornice, parapet, slate roof and chimneys."""
    ye = Y0 + 22 * LOT + 0.4; fb = MB(); tb = MB(); rb = MB(); kb = MB(); rs = _rnd(31)
    for k, fac in enumerate(('fac_c', 'fac_a', 'fac_e', 'fac_s3', 'fac_b', 'fac_f', 'fac_d', 'fac_a', 'fac_c')):
        x0 = -36.0 + k * LOT
        qface(fb, (x0, ye, 0), (LOT, 0, 0), (0, 0, H_FAC), M[fac], (0, 0, 1, H_FAC / ST.FACADE_H), (0, -1, 0))
        tb.box((x0, ye - 0.95, 19.35), (x0 + LOT, ye, 19.62), M['cream']); tb.box((x0, ye - 0.7, 19.62), (x0 + LOT, ye, 19.9), M['cream_w'])
        tb.box((x0, ye - 0.16, 5.45), (x0 + LOT, ye, 5.85), M['cream'])
        kb.box((x0, ye, 19.9), (x0 + LOT, ye + 0.55, 20.9), M['brick_a' if k % 2 else 'brick_b'], tile=(4, 4))
        qface(rb, (x0, ye + 0.5, 19.6), (LOT, 0, 0), (0, 11.5 / 2, 4.6 + 0.3), M['slate'], (0, 0, LOT / 4, 1.3), (0, -0.6, 1))
        for xx in (x0 + 0.7, x0 + LOT - 0.7):
            kb.box((xx - 0.45, ye + 4.0, 22.0), (xx + 0.45, ye + 4.9, 25.2), M['brick_b']); tb.frustum(Vector((xx, ye + 4.45, 25.2)), Vector((xx, ye + 4.45, 26.1)), 0.2, 0.15, M['pot'], seg=8)
    for nm, mb in (('end_fac', fb), ('end_trim', tb), ('end_roof', rb), ('end_brick', kb)): _obj(mb, nm, SET)

# ----------------------------------------------------------------------------- street furniture
def _lamp_post(R, M, x, y, h=7.8, side=1):
    """Cast-iron oil lamp: fluted post on a plinth, a glass lantern with a cap and a finial, a scrolled bracket arm, a ladder bar."""
    I = M['iron']; mb = R['iron']; gl = R['glass']
    mb.frustum(Vector((x, y, ZP)), Vector((x, y, ZP + 0.7)), 0.38, 0.32, I, seg=8); mb.frustum(Vector((x, y, ZP + 0.7)), Vector((x, y, h - 1.2)), 0.2, 0.13, I, seg=8)
    mb.frustum(Vector((x, y, ZP + 0.7)), Vector((x, y, ZP + 0.95)), 0.3, 0.3, I, seg=8); mb.frustum(Vector((x, y, h - 1.2)), Vector((x, y, h - 1.0)), 0.25, 0.25, I, seg=8)
    mb.box((x - 0.55, y - 0.04, h - 2.6), (x + 0.55, y + 0.04, h - 2.52), I) if False else None
    mb.frustum(Vector((x - 0.45, y, h - 2.4)), Vector((x + 0.45, y, h - 2.4)), 0.04, 0.04, I, seg=4)          # ladder bar
    # lantern
    gl.frustum(Vector((x, y, h - 1.0)), Vector((x, y, h + 0.35)), 0.42, 0.5, M['glass_lamp'], seg=8, cap0=False, cap1=False)
    for k in range(8):
        a = 2 * math.pi * k / 8; mb.frustum(Vector((x + 0.43 * math.cos(a), y + 0.43 * math.sin(a), h - 1.0)), Vector((x + 0.5 * math.cos(a), y + 0.5 * math.sin(a), h + 0.35)), 0.025, 0.025, I, seg=3)
    mb.frustum(Vector((x, y, h + 0.35)), Vector((x, y, h + 0.8)), 0.62, 0.12, I, seg=8); mb.frustum(Vector((x, y, h + 0.8)), Vector((x, y, h + 1.1)), 0.06, 0.02, I, seg=4)
    mb.frustum(Vector((x, y, h - 1.0)), Vector((x, y, h - 1.12)), 0.5, 0.3, I, seg=8)
    return Vector((x, y, h - 0.35))

def _barrel(mb, M, c, r=0.7, h=1.7, lying=False, yaw=0.0):
    c = Vector(c); seg = 12
    if not lying:
        mb.frustum(c, c + Vector((0, 0, h * 0.5)), r * 0.82, r, M['barrel'], seg=seg, cap0=True, cap1=False, uv_wrap=(1.0, 1.0))
        mb.frustum(c + Vector((0, 0, h * 0.5)), c + Vector((0, 0, h)), r, r * 0.82, M['barrel'], seg=seg, cap0=False, cap1=True, uv_wrap=(1.0, 1.0))
    else:
        a = Vector((math.cos(yaw), math.sin(yaw), 0)); mb.frustum(c - a * h / 2, c, r * 0.82, r, M['barrel'], seg=seg, uv_wrap=(1.0, 1.0)); mb.frustum(c, c + a * h / 2, r, r * 0.82, M['barrel'], seg=seg, uv_wrap=(1.0, 1.0))

def _crate(mb, M, c, sx=1.2, sy=1.2, sz=1.0, yaw=0.0, mat='wood'):
    obox(mb, Vector(c) + Vector((0, 0, sz / 2)), Vector((math.cos(yaw), math.sin(yaw), 0)), Vector((-math.sin(yaw), math.cos(yaw), 0)), Vector((0, 0, 1)), sx / 2, sy / 2, sz / 2, M[mat], uvk=0.5)

def _barrow(mb, M, c, yaw, rs):
    """Market barrow: a wooden tray on two shafts and one big wheel, heaped with cabbages, turnips, carrots, apples, onions."""
    c = Vector(c); f = Vector((math.cos(yaw), math.sin(yaw), 0)); sd = Vector((-math.sin(yaw), math.cos(yaw), 0)); up = Vector((0, 0, 1))
    obox(mb, c + up * 1.15, f, sd, up, 1.5, 0.95, 0.16, M['wood'], uvk=0.5)                              # floor
    for sgn in (-1, 1):
        obox(mb, c + up * 1.55 + sd * sgn * 0.95, f, sd, up, 1.5, 0.07, 0.36, M['wood_d'], uvk=0.5)         # sides
        beam(mb, c + up * 1.0 + sd * sgn * 0.6 - f * 3.1, c + up * 1.1 + sd * sgn * 0.6 + f * 1.5, 0.12, 0.12, M['wood_d'])  # shafts
    obox(mb, c + up * 1.55 - f * 1.5, f, sd, up, 0.07, 0.95, 0.36, M['wood_d'], uvk=0.5); obox(mb, c + up * 1.7 + f * 1.5, f, sd, up, 0.07, 0.95, 0.5, M['wood_d'], uvk=0.5)
    for sgn in (-1, 1):                                                                                  # legs and the wheel
        rod(mb, c + sd * sgn * 0.7 - f * 1.2 + up * 1.0, c + sd * sgn * 0.7 - f * 1.2, 0.07, M['wood_d'])
    wc = c + f * 1.55 + up * 0.62
    for sgn in (-0.3, 0.3):
        mb.frustum(wc + sd * sgn - sd * 0.04, wc + sd * sgn + sd * 0.04, 0.62, 0.62, M['wheel'], seg=14)
    rod(mb, wc - sd * 0.5, wc + sd * 0.5, 0.06, M['iron_b'])
    # produce: heaps (lumpy spheres)
    kinds = [('cabbage', 0.34), ('turnip', 0.24), ('carrot', 0.14), ('apple', 0.2), ('onion', 0.2)]
    for i in range(46):
        u = rs.uniform(-1.3, 1.3); v = rs.uniform(-0.8, 0.8); kind, r = kinds[(i // 6) % len(kinds)] if rs.random() < 0.7 else kinds[rs.randrange(len(kinds))]
        pos = c + f * u + sd * v + up * (1.3 + r * 0.8 + 0.28 * (1 - (abs(u) / 1.5) ** 2) * (1 - (abs(v) / 0.95) ** 2) * 1.6)
        if kind == 'carrot':
            d = (f * rs.uniform(-1, 1) + sd * rs.uniform(-1, 1)).normalized(); rod(mb, pos - d * 0.4 + up * 0.1, pos + d * 0.4, 0.07, M['carrot'], seg=5, r1=0.025)
        else:
            lumpy(mb, pos, r, M[kind], rs.randint(1, 999), seg=8, rings=5, rough=0.12)
            if kind == 'turnip': mb.sphere(pos + up * r * 0.7, r * 0.5, M['turnip_top'], seg=6, rings=4)

def _umbrella(mb, M, top, r=2.1, h=0.9, mat='umb_dark', tilt=(0.0, 0.0), n=10, scallop=0.0, pole_to=None, canopy_mat=None):
    """Umbrella: n gores bulging to a dome, whalebone-style ribs, a pole to `pole_to` (the hand) with a crook. top = canopy apex.
    tilt = (dx, dy) shift of the rim relative to the apex (a lean into the rain)."""
    top = Vector(top); cm = canopy_mat or M[mat]; rings = 5; R = []
    for k in range(rings + 1):
        t = k / rings; ang = t * (math.pi / 2) * 0.85; rr = r * math.sin(ang) / math.sin(math.pi / 2 * 0.85); z = -h * (1 - math.cos(ang)) / (1 - math.cos(math.pi / 2 * 0.85)) if k else 0.0
        row = []
        for i in range(n):
            a = 2 * math.pi * i / n; sc = 1.0 - (scallop * 0.5 if (k == rings) else 0.0)
            row.append(top + Vector((rr * math.cos(a) + tilt[0] * t, rr * math.sin(a) + tilt[1] * t, z)))
        R.append(row)
    for k in range(rings):
        for i in range(n):
            j = (i + 1) % n; mb.face([R[k][j], R[k][i], R[k + 1][i], R[k + 1][j]][::-1] if k else [R[0][0], R[1][j], R[1][i]], cm,
                                     [(1, 1), (0, 1), (0, 0), (1, 0)] if False else [(i / n, k / rings), ((i + 1) / n, k / rings), ((i + 1) / n, (k + 1) / rings), (i / n, (k + 1) / rings)][:4 if k else 3])
    for i in range(n):
        rod(mb, R[0][0], R[rings][i], 0.025, M['iron_b'], seg=3)
    if pole_to is not None:
        pt = Vector(pole_to); rod(mb, top + Vector((0, 0, 0.1)), pt, 0.05, M['wood_d'], seg=5)
        mb.sphere(top + Vector((0, 0, 0.12)), 0.09, M['brass'], seg=6, rings=4)
        mb.frustum(pt, pt + Vector((0.0, 0.0, -0.22)), 0.07, 0.09, M['wood_d'], seg=6)

# ----------------------------------------------------------------------------- the hackney coach and horse
def _wheel(mb, M, c, ax, R_, w=0.32):
    c = Vector(c); ax = Vector(ax).normalized(); up = Vector((0, 0, 1)); fw = ax.cross(up).normalized()
    N = 22; rim_r = 0.13
    for i in range(N):
        a0, a1 = 2 * math.pi * i / N, 2 * math.pi * (i + 1) / N
        p0 = c + fw * R_ * math.cos(a0) + up * R_ * math.sin(a0); p1 = c + fw * R_ * math.cos(a1) + up * R_ * math.sin(a1)
        mb.frustum(p0 - ax * w / 2, p0 + ax * w / 2, 0.0, 0.0, M['iron_b'], seg=3, cap0=False, cap1=False) if False else None
        obox(mb, (p0 + p1) / 2, (p1 - p0).normalized(), ax, ((p1 - p0).normalized().cross(ax)).normalized(), (p1 - p0).length / 2 + 0.01, w / 2, rim_r * 0.9, M['iron_b'] if i % 2 else M['wheel_r'], uvk=0.5)
    for k in range(12):
        a = 2 * math.pi * k / 12; d = fw * math.cos(a) + up * math.sin(a); rod(mb, c + d * 0.3, c + d * (R_ - 0.08), 0.075, M['wheel_r'], seg=4)
    mb.frustum(c - ax * 0.26, c + ax * 0.26, 0.3, 0.3, M['wheel'], seg=10); mb.frustum(c - ax * 0.32, c + ax * 0.32, 0.12, 0.12, M['brass'], seg=6)

def _coach(SET, M, name, loc, yaw, rs, horse=True, seat_empty=True, umbrella=None):
    """Hackney coach (black-green box on perch and C-springs, big rear wheels, hammercloth coachman's box, two lanterns) with a horse
    in the shafts. Built facing +y at the origin, then rotated by `yaw` (deg) and moved to `loc`."""
    mb = MB(); I = M['iron_b']
    BY0, BY1 = -2.7, 2.7; hw = 1.65
    # undercarriage
    for sgn in (-1, 1):
        beam(mb, Vector((sgn * 0.85, -3.2, 1.55)), Vector((sgn * 0.85, 3.4, 1.55)), 0.3, 0.2, M['wheel'])            # perch / side bars
        for yy in (-1.5, 2.1): mb.frustum(Vector((sgn * 1.1, yy, 1.6)), Vector((sgn * 1.2, yy + 0.0, 2.55)), 0.09, 0.09, M['iron'], seg=5)
    rod(mb, Vector((-2.1, -1.3, 2.3)), Vector((2.1, -1.3, 2.3)), 0.12, I, seg=6); rod(mb, Vector((-2.0, 2.3, 1.5)), Vector((2.0, 2.3, 1.5)), 0.1, I, seg=6)
    for sgn in (-1, 1):
        _wheel(mb, M, Vector((sgn * 2.0, -1.3, 2.3)), (1, 0, 0), 2.3); _wheel(mb, M, Vector((sgn * 1.9, 2.3, 1.5)), (1, 0, 0), 1.5)
    # body: waisted box. lower z 2.55..3.4 (wider), cabin 3.4..5.6 (tapers in), side quads carry the painted door / window / crest
    z0, z1, z2 = 2.55, 3.35, 5.55
    def side_quad(sgn, y0_, y1_, za, zb, xa, xb, uv, mat, flip=False):
        n_ = (sgn, 0, 0)
        mb.oface([(xa, y0_, za), (xa, y1_, za), (xb, y1_, zb), (xb, y0_, zb)], mat, [(uv[0], uv[1]), (uv[2], uv[1]), (uv[2], uv[3]), (uv[0], uv[3])], n_)
    for sgn in (-1, 1):
        ua, ub = (0.0, 1.0) if sgn > 0 else (1.0, 0.0)
        side_quad(sgn, BY0, BY1, z0, z1, sgn * (hw - 0.1), sgn * hw, (ua, 0.0, ub, 0.24), M['coach'])
        mb.oface([(sgn * hw, BY0, z1), (sgn * hw, BY1, z1), (sgn * (hw - 0.22), BY1, z2), (sgn * (hw - 0.22), BY0, z2)], M['coach_side'],
                 [(ua, 0.2), (ub, 0.2), (ub, 1.0), (ua, 1.0)], (sgn, 0, 0))
        mb.oface([(sgn * (hw - 0.1), BY0, z0), (sgn * (hw - 0.1), BY1, z0), (sgn * hw, BY1, z1), (sgn * hw, BY0, z1)], M['coach'], [(0, 0), (1, 0), (1, 1), (0, 1)], (sgn, 0, -0.2)) if False else None
    # front and back
    for yy, nn in ((BY1, (0, 1, 0)), (BY0, (0, -1, 0))):
        mb.oface([(-hw, yy, z0), (hw, yy, z0), (hw, yy, z1), (-hw, yy, z1)], M['coach'], [(0, 0), (1, 0), (1, 0.3), (0, 0.3)], nn)
        mb.oface([(-hw, yy, z1), (hw, yy, z1), (hw - 0.22, yy, z2), (-hw + 0.22, yy, z2)], M['coach_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], nn)
    # roof: an arched half-cylinder along y, with a gold rail
    seg = 9; rr = hw - 0.22
    for i in range(seg):
        a0, a1 = math.pi * i / seg, math.pi * (i + 1) / seg
        p0, p1 = (rr * math.cos(a0), 0.75 * math.sin(a0)), (rr * math.cos(a1), 0.75 * math.sin(a1))
        mb.oface([(-p0[0] * -1 * -1 if False else p0[0], BY0 - 0.25, z2 + p0[1]), (p0[0], BY1 + 0.25, z2 + p0[1]), (p1[0], BY1 + 0.25, z2 + p1[1]), (p1[0], BY0 - 0.25, z2 + p1[1])], M['coach_d'], [(0, 0), (1, 0), (1, 1), (0, 1)], ((p0[0] + p1[0]) / 2, 0, (p0[1] + p1[1]) / 2 + 0.3))
    for yy, nn in ((BY1 + 0.25, (0, 1, 0)), (BY0 - 0.25, (0, -1, 0))):
        mb.oface([(rr * math.cos(math.pi * i / seg), yy, z2 + 0.75 * math.sin(math.pi * i / seg)) for i in range(seg + 1)] + [(-rr, yy, z2)], M['coach_d'], [(0, 0)] * (seg + 2), nn)
    rod(mb, Vector((-rr, BY0 - 0.25, z2 + 0.02)), Vector((-rr, BY1 + 0.25, z2 + 0.02)), 0.06, M['coach_gold'], seg=4); rod(mb, Vector((rr, BY0 - 0.25, z2 + 0.02)), Vector((rr, BY1 + 0.25, z2 + 0.02)), 0.06, M['coach_gold'], seg=4)
    # coachman's box: hammercloth in oxblood with a gold fringe, seat plank, footboard
    obox(mb, Vector((0, 3.35, 3.55)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 1.3, 0.8, 0.5, M['cloth'], uvk=0.5)
    obox(mb, Vector((0, 3.35, 4.1)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 1.35, 0.85, 0.08, M['leather'], uvk=0.5)
    for sgn in (-1, 1): rod(mb, Vector((sgn * 1.3, 2.55, 3.18)), Vector((sgn * 1.3, 4.15, 3.18)), 0.04, M['coach_gold'], seg=3)
    rod(mb, Vector((-1.3, 4.15, 3.18)), Vector((1.3, 4.15, 3.18)), 0.04, M['coach_gold'], seg=3)
    obox(mb, Vector((0, 4.3, 2.55)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 1.1, 0.5, 0.06, M['wheel'], uvk=0.5)       # footboard
    # rear footman board + straps, lanterns on the front corners
    obox(mb, Vector((0, -3.3, 2.0)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 0.9, 0.35, 0.07, M['wheel'], uvk=0.5)
    lan = []
    for sgn in (-1, 1):
        c = Vector((sgn * (hw + 0.1), 2.25, 4.9)); mb.frustum(c - Vector((0, 0, 0.35)), c + Vector((0, 0, 0.35)), 0.26, 0.3, M['lantern'], seg=6, cap0=False, cap1=False)
        mb.frustum(c + Vector((0, 0, 0.35)), c + Vector((0, 0, 0.62)), 0.34, 0.06, I, seg=6); mb.frustum(c - Vector((0, 0, 0.35)), c - Vector((0, 0, 0.45)), 0.3, 0.2, I, seg=6)
        beam(mb, c + Vector((-sgn * 0.12, 0, -0.45)), c + Vector((-sgn * 0.12, 0, -0.9)), 0.1, 0.1, I); lan.append(c)
    # shafts and the horse
    for sgn in (-1, 1): beam(mb, Vector((sgn * 0.75, 2.3, 1.85)), Vector((sgn * 0.55, 8.0, 3.05)), 0.18, 0.14, M['wheel'])
    if umbrella: pass
    o = _obj(mb, name, SET)
    o.location = loc; o.rotation_euler = (0, 0, math.radians(yaw)); STATE.setdefault('coaches', []).append((name, Vector(loc), yaw, lan))
    if horse:                                              # the horse is its own object: a little squat and thick, as a hackney horse is
        hb = MB(); _horse(hb, M, Vector((0, 0, 0)), rs); ho = _obj(hb, name + '_horse', SET)
        a = math.radians(yaw); ho.location = Vector(loc) + Vector((-8.1 * math.sin(a), 8.1 * math.cos(a), 0.0)); ho.rotation_euler = (0, 0, a); ho.scale = (0.84, 0.84, 0.76)
    return o

def _horse(mb, M, c, rs):
    """A simple, chunky cart horse (chestnut, white blaze, dark mane and tail, black harness with brass studs). Faces +y, standing at c."""
    c = Vector(c); hm, hd, hw_, hh = M['horse'], M['horse_d'], M['horse_w'], M['hoof']
    lumpy(mb, c + Vector((0, 0.0, 3.55)), 1.0, hm, 3, seg=14, rings=8, rough=0.03, squash=1.0) if False else None
    def ell(ctr, rx, ry, rz, mat, seg=14, rings=8):
        R = []
        for k in range(rings + 1):
            th = math.pi * k / rings; row = []
            for i in range(seg):
                ph = 2 * math.pi * i / seg; row.append(Vector(ctr) + Vector((rx * math.sin(th) * math.cos(ph), ry * math.sin(th) * math.sin(ph), -rz * math.cos(th))))
            R.append(row)
        mb.pid += 1
        for k in range(rings):
            for i in range(seg):
                j = (i + 1) % seg; mb.face([R[k][i], R[k][j], R[k + 1][j], R[k + 1][i]][::-1], mat, [(0, 0)] * 4)
    ell(c + Vector((0, 0.0, 3.75)), 1.0, 2.1, 1.05, hm)                       # barrel
    ell(c + Vector((0, 1.75, 4.0)), 1.0, 1.05, 1.15, hm)                      # chest
    ell(c + Vector((0, -1.55, 3.9)), 1.02, 1.15, 1.15, hm)                    # rump
    cyl(mb, c + Vector((0, 2.1, 4.4)), c + Vector((0, 3.1, 5.6)), 0.66, hm, seg=10, r1=0.42, caps=False)            # neck
    cyl(mb, c + Vector((0, 3.0, 5.7)), c + Vector((0, 4.05, 5.0)), 0.44, hm, seg=10, r1=0.3, caps=True)              # head
    cyl(mb, c + Vector((0, 3.95, 5.1)), c + Vector((0, 4.45, 4.8)), 0.3, hm, seg=8, r1=0.24, caps=True)              # muzzle
    obox(mb, c + Vector((0, 3.93, 5.34)), Vector((1, 0, 0)), Vector((0, 0.82, -0.57)), Vector((0, 0.57, 0.82)), 0.07, 0.5, 0.05, hw_, uvk=0.5)  # blaze
    for sgn in (-1, 1):
        cyl(mb, c + Vector((sgn * 0.2, 3.0, 5.85)), c + Vector((sgn * 0.26, 2.95, 6.4)), 0.1, hm, seg=5, r1=0.01, caps=False)               # ears
        mb.sphere(c + Vector((sgn * 0.33, 3.45, 5.55)), 0.1, M['iron_b'], seg=6, rings=4)                                                  # eye
        obox(mb, c + Vector((sgn * 0.45, 3.4, 5.5)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 0.03, 0.3, 0.3, M['leather'], uvk=0.5)  # blinker
    for k in range(7):                                                              # mane
        t = k / 6; p = c + Vector((0, 2.2 + 0.85 * t, 5.55 + 0.1 - 0.5 * (1 - t) * 0.0 + 0.55 * t - 0.2)); obox(mb, p, Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 0.09, 0.2, 0.3, hd, uvk=0.5)
    # legs: upper and lower segments, hooves
    for (lx, ly) in ((-0.62, 2.25), (0.62, 2.25), (-0.62, -1.9), (0.62, -1.9)):
        top = c + Vector((lx, ly, 3.0)); knee = c + Vector((lx, ly + (0.1 if ly > 0 else -0.25), 1.55)); foot = c + Vector((lx, ly + (0.05 if ly > 0 else -0.2), 0.32))
        cyl(mb, top, knee, 0.42, hm, seg=8, r1=0.26, caps=False); cyl(mb, knee, foot, 0.25, hm, seg=7, r1=0.2, caps=False)
        cyl(mb, foot, foot - Vector((0, 0, 0.32)), 0.2, hh, seg=7, r1=0.24, caps=True); mb.frustum(foot + Vector((0, 0, 0.18)), foot + Vector((0, 0, 0.42)), 0.2, 0.2, hw_, seg=7)
    # tail: a swept chain
    pts = [c + Vector((0, -2.5, 4.3)), c + Vector((0, -2.9, 3.7)), c + Vector((0, -3.0, 2.8)), c + Vector((0, -2.9, 1.9))]
    for a, b, rr in zip(pts, pts[1:], (0.22, 0.2, 0.15)): cyl(mb, a, b, rr, hd, seg=6, r1=rr * 0.85, caps=False)
    # harness: collar, back strap, girth, traces to the shafts, brass studs
    cyl(mb, c + Vector((0, 2.0, 4.6)), c + Vector((0, 2.2, 3.5)), 0.78, M['leather'], seg=10, r1=0.8, caps=False)
    obox(mb, c + Vector((0, 0.3, 4.82)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)), 0.95, 0.18, 0.05, M['leather'], uvk=0.5)
    for sgn in (-1, 1):
        beam(mb, c + Vector((sgn * 0.8, 1.6, 3.9)), c + Vector((sgn * 0.7, -2.5, 3.0)), 0.07, 0.04, M['leather'])
    for k in range(9): mb.sphere(c + Vector((0, 2.35 - 0.03 * k, 4.3 - 0.1 * k)), 0.07, M['brass'], seg=4, rings=3)

# ----------------------------------------------------------------------------- rain
def _camera_basis(cam):
    m = cam.matrix_world.to_quaternion(); fwd = m @ Vector((0, 0, -1)); right = m @ Vector((1, 0, 0)); up = m @ Vector((0, 1, 0))
    return cam.matrix_world.translation.copy(), fwd, right, up

def _rain(SET, M, cam, n=1700, seed=9, depth=(2.5, 75.0)):
    """Crisp rain streaks: thin pointed ribbons facing the camera, constant on-screen width (~2 px) at every depth, slightly slanted by
    the wind. Camera-only (no shadow, no bounce). Also eave drips falling from the cornice lines are added by _drips."""
    rs = _rnd(seed); mb = MB(); c, fwd, right, up = _camera_basis(cam); fx = 782.2 / 1.0
    th = math.tan(math.radians(24.7)); tv = math.tan(math.radians(39.3))
    wind = Vector((0.16, 0.0, 0.0))
    for i in range(n):
        d = depth[0] * (depth[1] / depth[0]) ** (rs.random() ** 1.3)
        u, v = rs.uniform(-1.12, 1.12), rs.uniform(-1.12, 1.12)
        p = c + fwd * d + right * (u * th * d) + up * (v * tv * d)
        dirv = (Vector((0, 0, -1)) + wind + Vector((0.0, 0.05 * rs.uniform(-1, 1), 0))).normalized()
        to_cam = (c - p).normalized(); side = dirv.cross(to_cam)
        if side.length < 1e-3: continue
        side.normalize()
        Lpx = rs.uniform(26, 56) if d > 6 else rs.uniform(40, 80); wpx = rs.uniform(1.4, 2.2) if d > 10 else rs.uniform(2.0, 3.0)
        L = Lpx * d / fx; w = wpx * d / fx
        a = p - dirv * L / 2; b = p + dirv * L / 2; s_ = side * (w / 2)
        mb.face([a, p + s_ - dirv * (L * 0.15), b, p - s_ - dirv * (L * 0.15)], M['rain'])
    o = _obj(mb, 'rain', SET, shadow=False)
    o.visible_diffuse = False; o.visible_glossy = False; o.visible_transmission = False

def _drips(SET, M, cam, rs, y_range, rows=((1, 'R'), (-1, 'L')), n_per=5):
    """Drips falling from the cornice (a thread of water with a bright head) and small jets out of the rain-water hoppers."""
    mb = MB(); c, fwd, right, up = _camera_basis(cam); ys = [y for y in np.arange(y_range[0], y_range[1], LOT)]
    for s, _ in rows:
        for y0 in ys:
            for k in range(n_per):
                y = y0 + rs.uniform(0.3, LOT - 0.3); x = s * (X0 - 0.95 - 0.05); z0 = 19.4; L = rs.uniform(0.5, 1.5); zc = z0 - rs.uniform(0.2, 7.0) - L / 2
                p = Vector((x, y, zc)); to_cam = (c - p).normalized(); side = Vector((0, 0, -1)).cross(to_cam)
                if side.length < 1e-3: continue
                side.normalize(); dist = (c - p).length; w = max(0.035, 2.6 * dist / 782.2)
                a = p + Vector((0, 0, L / 2)); b = p - Vector((0, 0, L / 2)); s_ = side * (w / 2)
                mb.face([a + s_ * 0.3, a - s_ * 0.3, b - s_ * 1.0, b + s_ * 1.0][::-1], M['drip'])
    _obj(mb, 'drips', SET, shadow=False).visible_glossy = False

def _halos(SET, M, cam, pts, size=3.4, mat='halo'):
    mb = MB(); c, fwd, right, up = _camera_basis(cam)
    for p, sz in pts:
        p = Vector(p); to_cam = (c - p).normalized(); sd = Vector((0, 0, 1)).cross(to_cam).normalized(); up2 = to_cam.cross(sd).normalized(); h = sz / 2
        mb.face([p - sd * h - up2 * h, p + sd * h - up2 * h, p + sd * h + up2 * h, p - sd * h + up2 * h], M[mat], [(0, 0), (1, 0), (1, 1), (0, 1)])
    o = _obj(mb, 'halos', SET, shadow=False); o.visible_glossy = True

# ----------------------------------------------------------------------------- sky
def _sky(SET, M, R=900.0):
    mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o; o.visible_glossy = True

# ----------------------------------------------------------------------------- build
def build(preset='street_wide', clear=True):
    assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; scene = bpy.context.scene; P = dict(P_STREET)
    STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = 'street'; STATE['area'] = 'street'; STATE['light'] = 'STREET'
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_pov_follow', '_sun_screen', '_cards_face'): h.remove(f)
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('ST_', 'ink')): bpy.data.materials.remove(m)
    tx = ST.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_street') or bpy.data.worlds.new('W_street'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'ST_street_'; FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, glow=None, glow_k=0.0):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s_%g' % (pre, name, gain, _k(sm), form, alpha, smix, glow_k), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                               alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    STATE.update(C=C, TX=TX, pre=pre)
    M = _materials(P, C, TX, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
    d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
    o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    STATE['shop_lights'] = []; STATE['coaches'] = []
    _street(SET, LIG, P, M, preset)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    _grade(scene, P)
    W9._air_comp(scene, P)
    for ob in SET.objects:
        no_bounce(ob); ob.visible_glossy = ob.name not in ('rain', 'drips')
    cs = CAMS[PR['cam']]
    A = dict(cam_name=PR['cam'], cams=CAMS, preset=preset, key_dir=tuple(kd), units='1 unit = 1 head; z up; street along +y', hero=PR['hero'])
    STATE['A'] = A
    return A

def _grade(scene, P, bloom=0.22):
    """tower.setup_grade with a lighter bloom (the lit windows glow, the brick around them does not turn pink)."""
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=bloom, bloom_size=P.get('bloom_size', 0.05), offset=tuple(P['grade_offset']), saturation=float(P['grade_saturation'])))
    scene.render.use_compositing = True

def setup_render(scene, quality='final'):
    MN.setup_render(scene, quality); c = scene.cycles; c.transparent_max_bounces = 24; c.glossy_bounces = 1; c.max_bounces = 2
    scene.render.threads = 4
    if os.environ.get('SAMPLES'): c.samples = int(os.environ['SAMPLES'])
    elif quality == 'final': c.samples = 14
    elif quality == 'hq': c.samples = 16

def make_camera(setup, name='cam', scene=None):
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 3000.0; ob.data.dof.use_dof = False
    return ob

def _street(SET, LIG, P, M, preset):
    rs = _rnd(11)
    _sky(SET, M)
    _ground(SET, M)
    spots = _puddles(SET, M, preset)
    rows = {}
    for side, seq in ((-1, LEFT_SEQ), (1, RIGHT_SEQ)):
        R = Row('L' if side < 0 else 'R'); rows[side] = R
        for i, fac in enumerate(seq):
            y0 = Y0 + i * LOT
            if fac is None:
                continue
            _house(R, M, side, y0, fac, _rnd(100 + i * 7 + (side + 1) * 31), i)
        # end of the row: a tall brick end house closing the far end
    # lamps, barrels, crates, barrow on the pavements
    LP = dict(iron=MB(), glass=MB()); halos = []
    lamp_ys = [-34, -18, -2, 14, 30, 46, 62, 78, 94]
    for i, y in enumerate(lamp_ys):
        for s in (-1, 1):
            if (i + (s > 0)) % 2: continue
            top = _lamp_post(LP, M, s * (XP + 0.35), y + (3 if s > 0 else 0), 7.8, s)
            halos.append(top)
            if y > -20 and y < 100: STATE.setdefault('lamp_pts', []).append(top)
    for key in ('iron', 'glass'): _obj(LP[key], 'lamps_' + key, SET)
    # pavement dressing
    dm = MB(); bm = MB()
    _barrow(bm, M, Vector((-8.3, 10.5, ZP)), math.radians(80), _rnd(3)); _obj(bm, 'barrow', SET)
    for (x, y, k) in ((-8.6, 22.5, 0), (-8.8, 2.5, 1), (8.6, 9.0, 0), (-8.4, 36.0, 1), (8.8, 62.0, 0), (-8.8, 60.0, 1)):
        _barrel(dm, M, Vector((x, y, ZP)), r=0.72, h=1.8, lying=False)
        _barrel(dm, M, Vector((x + 0.3 * (1 if x < 0 else -1), y + 1.5, ZP)), r=0.7, h=1.7, lying=bool(k), yaw=1.3)
    for (x, y) in ((-8.5, 5.5), (8.7, 14.5), (-8.7, 40.5), (8.5, 48.0)):
        _crate(dm, M, Vector((x, y, ZP)), 1.3, 1.3, 1.0, 0.2); _crate(dm, M, Vector((x - (0.1 if x > 0 else -0.1), y + 0.2, ZP + 1.0)), 1.1, 1.1, 0.9, 0.5)
    _obj(dm, 'barrels_crates', SET)
    # the coach rank on the right kerb, facing the camera (-y)
    for i, y in enumerate((22.0, 40.5, 58.0)):
        _coach(SET, M, 'coach_%d' % i, (3.55, y, 0.0), 180.0, _rnd(40 + i), horse=True)
    # a rank bollard / water trough
    for sgn in (-1, 1):
        pass
    # finish the rows
    for side, R in rows.items(): _row_finish(SET, R, side)
    _lane_walls(SET, M, rs); _end_block(SET, M)
    STATE['rows'] = rows

# ----------------------------------------------------------------------------- per-shot things (camera dependent)
def _shot_extras(A, cam, preset):
    SET = STATE['SET']; LIG = STATE['LIGHTS']; M = STATE['M']; PR = PRESETS[preset]; rs = _rnd(77)
    rows = [(1, 'R'), (-1, 'L')]
    # real warm lamps: a few point lights near the camera's reach (lamps, shop bows) to put warm pools on the wet stones
    c = cam.matrix_world.translation
    lp = sorted(STATE.get('lamp_pts', []), key=lambda p: (p - c).length)[:6]
    for i, p in enumerate(lp):
        _light('lamp_%d' % i, p, (1.0, 0.64, 0.3), 1600.0, radius=0.35)
    sl = sorted(STATE.get('shop_lights', []), key=lambda t: (t[0] - c).length)[:6]
    for i, (p, kind) in enumerate(sl): _light('shop_%d' % i, p, (1.0, 0.66, 0.34), 1100.0, radius=0.5)
    for i, (name, loc, yaw, lan) in enumerate(STATE['coaches']):
        if (loc - c).length < 70:
            for j, lc in enumerate(lan):
                a = math.radians(yaw); w = loc + Vector((lc.x * math.cos(a) - lc.y * math.sin(a), lc.x * math.sin(a) + lc.y * math.cos(a), lc.z))
                _light('clamp_%d_%d' % (i, j), w, (1.0, 0.62, 0.28), 380.0, radius=0.2)
    # halos on the lamps near the camera and the lanterns of the coaches
    hp = [(p, 3.6) for p in STATE.get('lamp_pts', []) if (p - c).length < 130]
    for (name, loc, yaw, lan) in STATE['coaches']:
        for lc in lan:
            a = math.radians(yaw); w = loc + Vector((lc.x * math.cos(a) - lc.y * math.sin(a), lc.x * math.sin(a) + lc.y * math.cos(a), lc.z)); hp.append((w, 1.5))
    _halos(SET, M, cam, hp)
    _drips(SET, M, cam, rs, (max(Y0, c.y - 8), min(Y1, c.y + 90)))
    _rain(SET, M, cam, n=1000 if preset != 'street_high' else 900)
    ob_list = [o for o in SET.objects]
    for ob in ob_list:
        no_bounce(ob); ob.visible_glossy = ob.name not in ('rain', 'drips')
    ob = SET.objects.get('rain')

PH_ROLES = dict(hero=('priest', 3.1), man=('extra_a', 2.9), coachman=('extra_c', 3.0), woman=('extra_b', 2.9))

def _placeholder(role, mark, face_to, name, tilt=0.0):
    ob = T.placeholder_actor(PH_ROLES[role][0], mark, face_to=face_to, tilt=tilt, name=name)
    ob.visible_glossy = True
    return ob

def stage_placeholders(A, cam_name):
    """Placeholder actor cards (stand-ins, 1 unit = 1 head): Hanway under the dark umbrella (and a passer-by), the coachman on the box, or umbrellas."""
    scene = bpy.context.scene; cam = scene.camera; cl = cam.matrix_world.translation; M = STATE['M']; SET = STATE['SET']; out = []
    el = math.degrees(math.atan2(cam.matrix_world.translation.z - 1.5, 30.0)); tilt = 0.0
    if cam_name == 'street_wide':
        hx, hy = -0.7, -1.5
        out.append(_placeholder('hero', (hx, hy, 0.0), cl, 'actor_hero_0'))
        um = MB(); _umbrella(um, M, Vector((hx + 0.1, hy - 0.2, 4.05)), r=2.2, h=0.8, mat='umb_dark', tilt=(0.0, 0.0), pole_to=Vector((hx + 0.62, hy - 0.06, 1.9))); _obj(um, 'umbrella_hero', SET)
        out.append(_placeholder('man', (-4.0, 16.0, ZP), cl, 'actor_man_1'))
        um2 = MB(); _umbrella(um2, M, Vector((-4.0, 15.8, ZP + 4.0)), r=2.0, h=0.8, mat='umb_brown', pole_to=Vector((-3.6, 15.95, ZP + 1.9))); _obj(um2, 'umbrella_2', SET)
        out.append(_placeholder('coachman', (3.9, 40.0 - 6.0, 4.6), cl, 'actor_coachman_2'))
    elif cam_name == 'coach_low':
        out.append(_placeholder('coachman', (3.55, 22.0 - 3.35, 4.3), cl, 'actor_coachman_0'))
        out.append(_placeholder('hero', (-2.9, 13.5, 0.0), cl, 'actor_hero_1'))
        um = MB(); _umbrella(um, M, Vector((-2.8, 13.3, 4.05)), r=2.2, h=0.8, mat='umb_dark', pole_to=Vector((-2.2, 13.45, 1.9))); _obj(um, 'umbrella_hero', SET)
    else:
        um = MB(); rs = _rnd(8)
        spots = [(-3.0, 8.0, 'umb_dark'), (1.0, 14.0, 'umb_brown'), (-2.4, 20.0, 'umb_green'), (3.2, 26.0, 'umb_blue'), (-1.2, 30.0, 'umb_dark'), (0.5, 38.0, 'umb_red'),
                 (-3.5, 45.0, 'umb_brown'), (2.0, 52.0, 'umb_dark'), (-0.6, 3.0, 'umb_blue'), (6.8, 12.0, 'umb_green'), (-6.6, 18.0, 'umb_dark'), (6.7, 33.0, 'umb_brown'), (-6.8, 28.0, 'umb_red'),
                 (1.8, 62.0, 'umb_green'), (-2.0, 70.0, 'umb_dark'), (6.6, 50.0, 'umb_dark'), (-6.6, 40.0, 'umb_blue')]
        for (x, y, m) in spots:
            z = ZP if abs(x) > XK else 0.0
            _umbrella(um, M, Vector((x, y, z + 3.9)), r=rs.uniform(1.7, 2.2), h=0.8, mat=m, n=10, pole_to=Vector((x + 0.0, y, z + 1.0)))
        _umbrella(um, M, Vector((3.55, 25.0, 6.8)), r=2.3, h=0.9, mat='pink', n=14, canopy_mat=M['pink'], pole_to=Vector((3.55, 25.0, 4.4)))
        _obj(um, 'umbrellas', SET)
        out.append(_placeholder('coachman', (3.55, 25.0, 4.3), cl, 'actor_coachman_0', tilt=0.0))
    for ob in SET.objects: no_bounce(ob); ob.visible_glossy = ob.name not in ('rain', 'drips')
    for o in out: o.visible_glossy = True
    return out

def render(path, scene=None):
    return T.render(path, scene)

def render_preset(preset, out, quality='final', seed_extras=True):
    A = build(preset); sc = bpy.context.scene; setup_render(sc, quality)
    cam = make_camera(CAMS[A['cam_name']]); bpy.context.view_layer.update()
    stage_placeholders(A, A['cam_name'])
    _shot_extras(A, cam, preset)
    bpy.context.view_layer.update()
    w, c = render(out, sc)
    return w, c

# ----------------------------------------------------------------------------- CLI
BOARD = dict(street_wide='sb1_street_wide.png', coach_low='sb2_coach_low.png', street_high='sb3_street_high.png')

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('stills', 'final', 'styleboard'):
        q = 'preview' if cmd == 'stills' else 'final'; names = arg or list(PRESETS)
        outdir = os.path.join(HERE, 'styleboard') if cmd == 'styleboard' else os.path.join(WORK, 'stills' if cmd == 'stills' else 'final'); os.makedirs(outdir, exist_ok=True)
        for pr in names:
            fn = BOARD[pr] if cmd == 'styleboard' else '%s_%s.png' % (pr, q)
            w, c = render_preset(pr, os.path.join(outdir, fn), q)
            print('%s %s: %.1f s wall, %.1f s cpu' % (q, fn, w, c), flush=True)
    else: print(__doc__)
