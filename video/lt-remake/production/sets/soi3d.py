"""A narrow soi in Thonburi with ร้านเหล็กดัดเจ๊หงส์ (Jae Hong's wrought-iron shop), as a real 3D set (bpy 5.3, Cycles CPU).
World: 1 unit = 1 m, Z up, ground z = 0. The soi runs along +y (camera end y ~ -4, far end y ~ 58 under the 7-storey block).
Soi concrete x -2.25..2.25, drain gutters to |x| 2.6, painted curb to 2.75, aprons to the shophouse fronts at x = XL (-5.0, left row,
facing +x, hero shop y 4..12) and x = XR (4.4, right row, facing -x).
Light model from office3d.mat_lit: ambient as emission (blue-violet shade) + one hard sun, toon key. Sky = camera-only world texture.
Preset 'evening' (just after sunset, every practical light ON): toon materials from toonlit.py that take the key from real lights
(shop fluorescent tubes = area lights, street lamps = spots, bulbs = points) plus a dim moon; lit windows, LED / neon signs and the
7-storey block's windows are emission terms. set_lights(False) switches all of them off on the same camera (moonlight only).
CLI: python3 soi3d.py stills [preset] [final|preview] [off] [cam ...]   -> out_soi/<cam>[_preset][_off].png (+ timing.json)
     python3 soi3d.py land [preset]                                  -> out_soi/wide_soi_16x9.png (1920x1080)"""
import os, sys, math, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, HERE)
import bpy
from mathutils import Vector, Matrix, Euler
import office3d as S
import tex_soi
import toonlit as TL
MB = S.MB
OUT = os.path.join(HERE, 'out_soi')

XL, XR = -5.0, 4.4                  # facade planes of the left / right rows
FH = 11.2                           # facade height (parapet top)
PRESETS = {
    'afternoon_storm': dict(shade=(0.250, 0.272, 0.45), key=(2.62, 1.72, 0.60), lift=(0.009, 0.013, 0.026), key_dir=(-0.17, 0.90, -0.40), sun_angle=0.2,
                            form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.05, grade_offset=(0.002, 0.004, 0.011), grade_saturation=1.22,
                            sky='sky_storm', tubes=3.2, lamps=0.0, phones=0.0, gain=0.60),
    'day': dict(shade=(0.30, 0.31, 0.56), key=(2.35, 2.05, 1.55), lift=(0.012, 0.012, 0.028), key_dir=(-0.30, 0.55, -0.78), sun_angle=0.25,
                form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.05, grade_offset=(0.003, 0.003, 0.010), grade_saturation=1.08,
                sky='sky_day', tubes=1.6, lamps=0.0, phones=0.0, gain=0.50),
    'night_blackout': dict(shade=(0.050, 0.055, 0.15), key=(0.42, 0.50, 0.85), lift=(0.004, 0.004, 0.012), key_dir=(0.45, 0.35, -0.82), sun_angle=0.8,
                           form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.06, grade_offset=(0.002, 0.002, 0.008), grade_saturation=1.05,
                           sky='sky_night', tubes=0.0, lamps=0.0, phones=4.0, gain=0.52),
    # just after sunset: blue-violet dusk ambient, a dim moon high behind the camera, every practical light on (set_lights toggles them)
    'evening': dict(shade=(0.092, 0.099, 0.240), key=(0.15, 0.19, 0.34), lift=(0.006, 0.007, 0.018), key_dir=(0.30, 0.42, -0.86), sun_angle=0.6,
                    form=(0.0, 0.0, 0.22), falloff_y=0.0, bloom_size=0.06, grade_offset=(0.002, 0.003, 0.010), grade_saturation=1.18,
                    sky='sky_evening', tubes=3.0, lamps=7.0, phones=0.0, gain=0.55, practicals=True, lambert=0.35, amb_off=0.66,
                    shop=dict(color='#e4f2ff', K=1.6), lamp=dict(color='#ffb45c', K=2.6), led=dict(color='#dcefff', K=2.2),
                    bulb=dict(color='#ffc27a', K=1.25), window_glow=(1.15, 0.0, 0.95, 1.05, 0.0, 0.8)),
}
A = {}; P = {}; M = {}; TX = {}; PR = []          # PR: practical lights collected while building (evening)

# ----------------------------------------------------------------------------- materials
_MEAN = {}
def art_mean(img=None, color='#808080'):
    """Mean linear colour of a texture (opaque pixels) or of a flat colour."""
    if img is None: return S.hex_lin(color)
    if img not in _MEAN:
        from PIL import Image
        import numpy as np
        a = np.asarray(Image.open(TX[img]).convert('RGBA').resize((64, 64)), dtype=float) / 255; m = a[..., 3] > 0.5
        c = a[..., :3][m] if m.any() else a[..., :3].reshape(-1, 3); c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
        _MEAN[img] = tuple(float(x) for x in c.mean(0))
    return _MEAN[img]

def shade_fix(mean, strength=0.8):
    """Per-channel shade multiplier that turns art x SHADE into the preset's shade hue (blue-violet) at the art's own luminance.
    strength 1 = every surface shades to exactly the same hue; 0 = plain multiply (warm art -> violet / magenta)."""
    sh = P['shade']; lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    L = max(lum(mean), 1e-4); want = [x / lum(sh) * L for x in sh]; got = [max(m * x, 1e-5) for m, x in zip(mean, sh)]
    return tuple(min(2.2, max(0.45, (w / g) ** strength)) for w, g in zip(want, got))

def lit(name, img=None, color='#808080', gain=0.9, shade=None, alpha=False, fix=0.8, glow=None, glow_strength=0.0):
    sm = shade if shade is not None else shade_fix(art_mean(img, color), fix)
    if P.get('practicals'):                                              # evening: toon key from every light (lamps, tubes, bulbs, moon)
        return TL.mat_toon('SOI_' + name, P, color=color, image=img and TX[img], gain=gain * P['gain'], shade_mul=sm, alpha=alpha, form=P['form'],
                           glow=glow and TX[glow], glow_strength=glow_strength, lambert=P.get('lambert', 0.0), amb_off=P.get('amb_off'))
    return S.mat_lit('SOI_' + name, color=color, image=img and TX[img], gain=gain * P['gain'], shade_mul=sm, alpha=alpha, form=P['form'])

def emit(name, color='#ffffff', strength=1.0, img=None, off=0.03, off_color=None):
    if P.get('practicals'): return TL.mat_glow('SOI_G_' + name, color, strength, image=img and TX[img], off=off, off_color=off_color)
    return S.mat_emit('SOI_E_' + name, color, image=img and TX[img], strength=strength)

def flat(hexcol, gain=0.85, shade=None):
    nm = 'f_%s_%g' % (hexcol.lstrip('#'), gain)
    if nm not in M: M[nm] = lit(nm, color=hexcol, gain=gain)
    return M[nm]

def materials():
    W = None                       # every material: automatic shade compensation from its mean colour (shade_fix)
    m = dict(
        road_a=lit('road_a', 'road_a', gain=0.95), road_b=lit('road_b', 'road_b', gain=0.95),
        tile_red=lit('tile_red', 'tile_red', gain=0.85), tile_grey=lit('tile_grey', 'tile_grey', gain=0.9), tile_white=lit('tile_white', 'tile_white', gain=0.85),
        hero_floor=lit('hero_floor', 'hero_floor', gain=0.95), gutter=lit('gutter', 'gutter', gain=0.9), curb=lit('curb', 'curb', gain=0.8),
        manhole=lit('manhole', 'manhole', gain=0.9), fac_hero=lit('fac_hero', 'fac_hero', gain=0.88, ),
        shut_grey=lit('shut_grey', 'shut_grey', gain=0.85), shut_green=lit('shut_green', 'shut_green', gain=0.85), shut_blue=lit('shut_blue', 'shut_blue', gain=0.85),
        shut_rust=lit('shut_rust', 'shut_rust', gain=0.85),
        grille_sun=lit('grille_sun', 'grille_sun', gain=0.85, alpha=True), grille_dia=lit('grille_dia', 'grille_dia', gain=0.8, alpha=True), grille_tul=lit('grille_tul', 'grille_tul', gain=0.8, alpha=True),
        ac=lit('ac', 'ac', gain=0.85), sign_hero=lit('sign_hero', 'sign_hero', gain=0.80), sign_board=lit('sign_board', 'sign_board', gain=0.8),
        signs=lit('signs', 'signs', gain=0.85), soi_sign=lit('soi_sign', 'soi_sign', gain=0.85), posters=lit('posters', 'posters', gain=0.85),
        interiors=lit('interiors', 'interiors', gain=0.7), hero_wall=lit('hero_wall', 'hero_wall', gain=0.9),
        gate_black=lit('gate_black', 'gate_black', gain=0.85, alpha=True), gate_white=lit('gate_white', 'gate_white', gain=0.8, alpha=True),
        gate_green=lit('gate_green', 'gate_green', gain=0.85, alpha=True), gate_red=lit('gate_red', 'gate_red', gain=0.85, alpha=True), gate_raw=lit('gate_raw', 'gate_raw', gain=0.9, alpha=True),
        slip=lit('slip', 'slip', gain=0.78), bench_top=lit('bench_top', 'bench_top', gain=0.9), pole=lit('pole', 'pole', gain=0.9), transformer=lit('transformer', 'transformer', gain=0.85),
        tower=lit('tower', 'tower', gain=0.9), billboard=lit('billboard', 'billboard', gain=0.85), banana=lit('banana', 'banana', gain=0.85, alpha=True),
        leaves=lit('leaves', 'leaves', gain=0.85, alpha=True), laundry=lit('laundry', 'laundry', gain=0.8, alpha=True),
        tin=lit('tin', 'tin', gain=0.85), tin_blue=lit('tin_blue', 'tin_blue', gain=0.85), planks=lit('planks', 'planks', gain=0.85, ), bike=lit('bike', 'bike', gain=0.8),
        crate=lit('crate', 'crate', gain=0.8), spirit=lit('spirit', 'spirit', gain=0.85), concrete=lit('concrete', 'concrete', gain=0.9),
        concrete_dark=lit('concrete_dark', 'concrete_dark', gain=0.85),
        tube=emit('tube', '#eef6ff', P['tubes'], off_color='#7a7e88') if P['tubes'] > 0 else flat('#d8dcd8'), phone=emit('phone', strength=P['phones'], img='phone') if P['phones'] > 0 else flat('#1a1a22'),
        lamp=emit('lamp', '#ffd890', P['lamps'], off_color='#8a8678') if P['lamps'] > 0 else flat('#d8d4c0'), red_bulb=emit('red_bulb', '#ff3a20', 2.5 if P['tubes'] > 0 else 0.3),
        glass=lit('glass', color='#2a3444', gain=0.6),
    )
    for i in range(8): m[f'fac{i}'] = lit(f'fac{i}', f'fac{i}', gain=0.88, ); m[f'pier{i}'] = lit(f'pier{i}', f'pier{i}', gain=0.88, )
    for i in range(6): m[f'win{i}'] = lit(f'win{i}', f'win{i}', gain=0.7)
    if P.get('practicals'):                                              # evening: lit rooms, lightbox signs, the block's windows, a flood-lit billboard
        for i, g in enumerate(P['window_glow']):
            if g > 0: m[f'win{i}'] = lit(f'win{i}_lit', f'win{i}', gain=0.7, glow=f'win{i}_glow', glow_strength=g)
        m['signs'] = lit('signs_lit', 'signs', gain=0.85, glow='signs', glow_strength=0.62)
        m['tower'] = lit('tower_lit', 'tower', gain=0.9, glow='tower_glow', glow_strength=1.1)
        m['billboard'] = lit('billboard_lit', 'billboard', gain=0.85, glow='billboard', glow_strength=0.55)
        m['interiors'] = lit('interiors_lit', 'interiors', gain=0.7, glow='interiors', glow_strength=0.12)
        for nm, col in (('led_cyan', '#40e8ff'), ('led_green', '#50ff90'), ('led_warm', '#fff0c0'), ('led_red', '#ff4a30'), ('led_blue', '#4a8aff'), ('led_yellow', '#ffd040')):
            m[nm] = emit(nm, col, 3.2, off=0.0, off_color='#3a3a40')
        m['bulb'] = emit('bulb', '#fff0c8', 8.0, off=0.02, off_color='#8a8478')
    M.update(m)

# ----------------------------------------------------------------------------- geometry helpers
def newell(pts):
    n = Vector((0, 0, 0))
    for i in range(len(pts)):
        a, b = pts[i], pts[(i + 1) % len(pts)]; n += Vector(((a.y - b.y) * (a.z + b.z), (a.z - b.z) * (a.x + b.x), (a.x - b.x) * (a.y + b.y)))
    return n

def F(mb, pts, mat, uvs=None, n=None):
    """Polygon; if n is given, flipped so its normal points along n."""
    pts = [Vector(p) for p in pts]; uvs = list(uvs) if uvs else [(0, 0), (1, 0), (1, 1), (0, 1)][:len(pts)] if len(pts) == 4 else None
    if n is not None and newell(pts).dot(Vector(n)) < 0: pts = pts[::-1]; uvs = uvs[::-1] if uvs else None
    mb.pid += 1; mb.face(pts, mat, uvs)

def rect(mb, c, u, v, mat, uv=(0, 0, 1, 1), n=None):
    """Quad centred at c with half-edge vectors u, v (normal u x v unless n given)."""
    c, u, v = Vector(c), Vector(u), Vector(v); u0, v0, u1, v1 = uv
    F(mb, [c - u - v, c + u - v, c + u + v, c - u + v], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], n)

def tube(mb, pts, r, mat, seg=5):
    """Swept tube through points (parallel-transport frames)."""
    pts = [Vector(p) for p in pts]
    if len(pts) < 2: return
    mb.pid += 1; t = (pts[1] - pts[0]).normalized(); u = t.cross(Vector((0, 0, 1)))
    if u.length < 1e-3: u = t.cross(Vector((1, 0, 0)))
    u.normalize(); rings = []
    for i, p in enumerate(pts):
        tn = (pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)]).normalized()
        u = (u - tn * u.dot(tn)); u = u.normalized() if u.length > 1e-6 else tn.orthogonal().normalized(); v = tn.cross(u)
        rings.append([p + r * (math.cos(2 * math.pi * k / seg) * u + math.sin(2 * math.pi * k / seg) * v) for k in range(seg)])
    for i in range(len(rings) - 1):
        for k in range(seg):
            j = (k + 1) % seg; mb.face([rings[i][k], rings[i][j], rings[i + 1][j], rings[i + 1][k]], mat)

def catenary(p0, p1, sag, n=24):
    p0, p1 = Vector(p0), Vector(p1)
    return [p0.lerp(p1, i / n) + Vector((0, 0, -sag * 4 * (i / n) * (1 - i / n))) for i in range(n + 1)]

def sq_prism(mb, x, y, z0, z1, r0, r1, mat, rot=0.0):
    """Tapered square post with per-face UVs (u 0..1 per face, v = 0..1 over the height)."""
    mb.pid += 1; c = [(math.cos(rot + math.pi / 4 + k * math.pi / 2), math.sin(rot + math.pi / 4 + k * math.pi / 2)) for k in range(4)]
    for k in range(4):
        a, b = c[k], c[(k + 1) % 4]; s = math.sqrt(2)
        mb.face([Vector((x + a[0] * r0 * s, y + a[1] * r0 * s, z0)), Vector((x + b[0] * r0 * s, y + b[1] * r0 * s, z0)),
                 Vector((x + b[0] * r1 * s, y + b[1] * r1 * s, z1)), Vector((x + a[0] * r1 * s, y + a[1] * r1 * s, z1))], mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.face([Vector((x + a[0] * r1 * math.sqrt(2), y + a[1] * r1 * math.sqrt(2), z1)) for a in c], mat)

class Fr:
    """Frame of one row of facades: a = along the wall (texture u grows with a), d = out of the wall toward the soi, z up."""
    def __init__(s, side):
        s.L = side == 'L'; s.nd = Vector((1 if s.L else -1, 0, 0)); s.na = Vector((0, 1 if s.L else -1, 0))
    def P(s, a, d, z): return Vector((XL + d, a, z)) if s.L else Vector((XR - d, -a, z))
    def a_of(s, y): return y if s.L else -y
    def quad(s, mb, a0, a1, z0, z1, d, mat, uv=(0, 0, 1, 1)):
        u0, v0, u1, v1 = uv
        F(mb, [s.P(a0, d, z0), s.P(a1, d, z0), s.P(a1, d, z1), s.P(a0, d, z1)], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], s.nd)
    def hquad(s, mb, a0, a1, d0, d1, z, mat, up=True, uv=(0, 0, 1, 1)):
        u0, v0, u1, v1 = uv
        F(mb, [s.P(a0, d0, z), s.P(a1, d0, z), s.P(a1, d1, z), s.P(a0, d1, z)], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], (0, 0, 1 if up else -1))
    def side(s, mb, a, d0, d1, z0, z1, mat, toward=1, uv=(0, 0, 1, 1)):
        u0, v0, u1, v1 = uv
        F(mb, [s.P(a, d0, z0), s.P(a, d1, z0), s.P(a, d1, z1), s.P(a, d0, z1)], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], s.na * toward)
    def box(s, mb, a0, a1, d0, d1, z0, z1, mat, tile=None, front=None):
        p, q = s.P(a0, d0, z0), s.P(a1, d1, z1); lo = (min(p.x, q.x), min(p.y, q.y), min(p.z, q.z)); hi = (max(p.x, q.x), max(p.y, q.y), max(p.z, q.z))
        mb.box(lo, hi, mat, mats={('right' if s.L else 'left'): front} if front else None, tile=tile)
    def cyl(s, mb, a, d, z0, z1, r, mat, seg=10): mb.frustum(tuple(s.P(a, d, z0)), tuple(s.P(a, d, z1)), r, r, mat, seg=seg)

def atlas_row(i, n=8): return (0.0, 1.0 - (i + 1) / n, 1.0, 1.0 - i / n)

# ----------------------------------------------------------------------------- small props (world coordinates)
def pot_plant(mb, p, r=0.18, h=0.3, big=1.0, col='#a85a3a', mb_alpha=None):
    x, y, z = p; mb.frustum((x, y, z), (x, y, z + h), r * 0.75, r, flat(col), seg=10); mb.frustum((x, y, z + h - 0.02), (x, y, z + h + 0.01), r * 0.95, r * 0.95, flat('#3a2a1e'), seg=10)
    s = 0.45 * big; mba = mb_alpha or mb
    for k in range(3):
        a = k * math.pi / 3 + 0.3; u = Vector((math.cos(a) * s, math.sin(a) * s, 0))
        rect(mba, (x, y, z + h + s * 0.85), u, (0, 0, s * 0.9), M['leaves'])

def stool(mb, p, col, h=0.45):
    x, y, z = p; mb.frustum((x, y, z), (x, y, z + h), 0.17, 0.14, flat(col, 0.8, (0.9, 1.05, 1.25)), seg=10, cap1=True)
    mb.frustum((x, y, z + h - 0.03), (x, y, z + h), 0.16, 0.16, flat(col, 0.8, (0.9, 1.05, 1.25)), seg=10)

def ac_unit(mb, fr, a, d, z, w=0.8, h=0.55, dep=0.32):
    fr.box(mb, a - w / 2, a + w / 2, d, d + dep, z, z + h, flat('#dedcd4'), front=M['ac'])
    for aa in (a - w / 2 + 0.05, a + w / 2 - 0.05): fr.box(mb, aa - 0.02, aa + 0.02, 0, d + dep + 0.05, z - 0.06, z - 0.02, flat('#3a3634'))
    tube(mb, [fr.P(a + w / 2 - 0.1, d + 0.1, z + 0.1), fr.P(a + w / 2 + 0.1, 0.05, z + 0.2), fr.P(a + w / 2 + 0.15, 0.05, z + 1.4)], 0.02, flat('#e8e4d8'))

def laundry_line(mb, mba, fr, a0, a1, d, z, r, n=None):
    tube(mb, [fr.P(a0, d, z), fr.P((a0 + a1) / 2, d, z - 0.05), fr.P(a1, d, z)], 0.006, flat('#e8e4d8'), seg=4)
    n = n or int((a1 - a0) / 0.42);
    for i in range(n):
        a = a0 + (i + 0.5) * (a1 - a0) / n + r.uniform(-0.05, 0.05); c = r.randrange(8); cu, cv = (c % 4) / 4, 1 - (c // 4 + 1) / 2
        w, h = 0.36, 0.72 * r.uniform(0.8, 1.1)
        F(mba, [fr.P(a - w / 2, d + r.uniform(-0.03, 0.03), z - h), fr.P(a + w / 2, d, z - h), fr.P(a + w / 2, d, z), fr.P(a - w / 2, d, z)], M['laundry'],
          [(cu, cv), (cu + 0.25, cv), (cu + 0.25, cv + 0.5), (cu, cv + 0.5)], fr.nd)

# ----------------------------------------------------------------------------- one shophouse bay
def window(mb, mba, fr, a0, a1, z0, z1, wt, gr=None, shade_box=True):
    fr.quad(mb, a0, a1, z0, z1, 0.012, M[wt])
    t = 0.07; fm = flat('#c8ccd0')
    fr.box(mb, a0 - t, a1 + t, 0, 0.06, z1, z1 + t, fm); fr.box(mb, a0 - t, a1 + t, 0, 0.06, z0 - t, z0, fm)
    fr.box(mb, a0 - t, a0, 0, 0.06, z0, z1, fm); fr.box(mb, a1, a1 + t, 0, 0.06, z0, z1, fm)
    fr.box(mb, a0 - 0.12, a1 + 0.12, 0, 0.16, z0 - 0.14, z0 - t, flat('#b8b2a4'))
    if gr: fr.quad(mba, a0 - 0.04, a1 + 0.04, z0 - 0.04, z1 + 0.04, 0.13, M[gr], uv=(0, 0, (a1 - a0 + 0.08) / 1.0, (z1 - z0 + 0.08) / 1.0))
    if gr:
        for aa in (a0 - 0.04, a1 + 0.04): fr.box(mb, aa - 0.015, aa + 0.015, 0, 0.14, z0 - 0.04, z1 + 0.04, flat('#2a2a2e'))
    if shade_box: fr.box(mb, a0 - 0.25, a1 + 0.25, 0, 0.55, z1 + 0.18, z1 + 0.28, M['concrete'], tile=(2, 2))

def bay(G, fr, a0, a1, cfg, r):
    """One 3-storey shophouse bay between a0 and a1 (pier at a0). G = dict of mesh builders."""
    mb, mba = G['row'], G['alpha']; wall, pier = M[f"fac{cfg['wall']}"], M[f"pier{cfg['wall']}"]
    top = cfg.get('top', FH); W = a1 - a0; b0, b1 = a0 + 0.36 + 0.08, a1 - 0.08; zo = 3.35          # ground-floor opening
    # wall pieces around the opening (texture spans the whole bay)
    U = lambda a: (a - a0) / W; V = lambda z: z / FH
    fr.quad(mb, a0 + 0.36, a1, zo, top, 0, wall, (U(a0 + 0.36), V(zo), 1, V(top)))
    fr.quad(mb, a0 + 0.36, b0, 0, zo, 0, wall, (U(a0 + 0.36), 0, U(b0), V(zo))); fr.quad(mb, b1, a1, 0, zo, 0, wall, (U(b1), 0, 1, V(zo)))
    fr.box(mb, a0, a0 + 0.36, 0, 0.12, 0, top, pier, front=pier)
    fr.quad(mb, a0, a0 + 0.36, 0, top, 0.121, pier, (0, 0, 1, V(top)))
    for z in (3.75, 7.05)[:2 if top > 8 else 1]: fr.box(mb, a0, a1, 0, 0.08, z, z + 0.22, flat('#c8c2b4'))
    fr.box(mb, a0, a1, -0.1, 0.1, top, top + 0.1, flat('#9a968c'))                      # coping
    # interior behind the opening
    D = 3.6; st = cfg['shut']
    fr.quad(mb, b0, b1, 0.15, zo, -D, M['interiors'], atlas_row(cfg['interior'], 4))
    fr.hquad(mb, b0, b1, -D, 0, 0.15, M['concrete_dark'], True, (0, 0, 2, 2)); fr.hquad(mb, b0, b1, -D, 0, zo, flat('#4a4644'), False)
    fr.side(mb, b0, -D, 0, 0, zo, flat('#8a8478'), 1); fr.side(mb, b1, -D, 0, 0, zo, flat('#8a8478'), -1)
    fr.box(mb, b0, b1, -0.05, 0.0, 0.0, 0.15, flat('#7a766c'))                       # threshold step
    if st in ('up', 'half') and P['tubes'] > 0:
        fr.box(mb, (b0 + b1) / 2 - 0.6, (b0 + b1) / 2 + 0.6, -D * 0.5 - 0.03, -D * 0.5 + 0.03, zo - 0.08, zo - 0.04, M['tube'])
        if P.get('practicals'): PR.append(('shop', tuple(fr.P((b0 + b1) / 2, -D * 0.5, zo - 0.1)), tuple(fr.na)))
    # roller shutter
    sh = M[cfg['shtex']]; fr.box(mb, b0 - 0.05, b1 + 0.05, 0, 0.32, zo - 0.25, zo + 0.15, flat('#8a8e90'))
    zb = {'down': 0.0, 'half': 1.55 + r.uniform(-0.3, 0.3), 'up': zo - 0.3, 'grille': zo - 0.3}[st]
    if zb < zo - 0.3:
        fr.quad(mb, b0, b1, zb, zo - 0.25, 0.08, sh, (0, zb / 2, (b1 - b0) / 2, (zo - 0.25) / 2)); fr.box(mb, b0, b1, 0.06, 0.11, zb - 0.04, zb + 0.04, flat('#5a5e60'))
        for aa in (b0, b1): fr.box(mb, aa - 0.05, aa, 0, 0.12, 0, zo - 0.2, flat('#6a6e70'))
    if st == 'grille': fr.quad(mba, b0, b1, 0, zo - 0.3, 0.1, M['grille_dia'], (0, 0, (b1 - b0) / 0.8, (zo - 0.3) / 1.2))
    # goods spilling out of open shops
    if st in ('up', 'half'):
        for k in range(r.randint(2, 5)):
            a = r.uniform(b0 + 0.3, b1 - 0.3); d = r.uniform(0.3, 1.2); s = r.uniform(0.3, 0.55)
            what = r.random()
            if what < 0.35: fr.box(mb, a - s / 2, a + s / 2, d, d + s * 0.7, 0, s * 0.6, M['crate'])
            elif what < 0.6: stool(mb, tuple(fr.P(a, d, 0)), r.choice(['#d8302a', '#2a5ad0', '#f0c030']))
            elif what < 0.8: fr.box(mb, a - 0.3, a + 0.3, d, d + 0.45, 0, 0.75, flat(r.choice(['#e8e8e8', '#3a6ab0', '#c83a2a'])))
            else: pot_plant(mb, tuple(fr.P(a, d, 0)), 0.2, 0.35, 1.0, mb_alpha=mba)
    # floor 2
    f2 = cfg['f2']; signz = None
    if f2 in ('cage', 'open'):
        fr.box(mb, a0, a1, 0, 1.1, 3.62, 3.8, M['concrete'], tile=(2, 2)); signz = (3.84, 4.66, 1.13)
        window(mb, mba, fr, a0 + 0.8, a1 - 0.5, 4.2, 6.5, f"win{r.randrange(6)}", None, False)
        if f2 == 'open':
            fr.box(mb, a0, a1, 0.98, 1.1, 3.8, 4.8, M[f"fac{cfg['wall']}"], tile=(4, 11.2)); fr.box(mb, a0, a1, 0.94, 1.14, 4.8, 4.86, flat('#8a8478'))
            for k in range(r.randint(2, 4) if cfg.get('plants', True) else 0): pot_plant(mb, tuple(fr.P(r.uniform(a0 + 0.4, a1 - 0.4), 1.04, 4.86)), 0.14, 0.22, 0.8, mb_alpha=mba)
            if cfg.get('laundry', True): laundry_line(mb, mba, fr, a0 + 0.4, a1 - 0.3, 0.6, 6.3, r)
            if P.get('practicals') and int(abs(a0) * 10) % 3 != 1:          # a bare bulb on the open balcony
                bp = fr.P((a0 + a1) / 2 + 0.6, 0.35, 6.85); fr.box(mb, (a0 + a1) / 2 + 0.58, (a0 + a1) / 2 + 0.62, 0.33, 0.37, 6.85, 7.05, flat('#2a2a2e')); mb.sphere(tuple(bp), 0.045, M['bulb'], 10, 6)
                PR.append(('balcony', tuple(bp - Vector((0, 0, 0.06))), None))
        else:
            fr.quad(mba, a0 + 0.05, a1, 3.8, 6.9, 1.08, M[cfg['grille']], (0, 0, W, 3.1))
            fr.side(mba, a0 + 0.05, 0, 1.08, 3.8, 6.9, M[cfg['grille']], -1, (0, 0, 1.08, 3.1)); fr.side(mba, a1 - 0.01, 0, 1.08, 3.8, 6.9, M[cfg['grille']], 1, (0, 0, 1.08, 3.1))
            fr.box(mb, a0, a1, 0, 1.15, 6.9, 7.0, M['tin'], tile=(2, 2))
            for aa in (a0 + 0.05, a1 - 0.03): fr.box(mb, aa - 0.02, aa + 0.02, 1.04, 1.1, 3.8, 6.9, flat('#2a2a2e'))
            if cfg.get('laundry', True): laundry_line(mb, mba, fr, a0 + 0.3, a1 - 0.3, 0.55, 6.6, r)
            for k in range(r.randint(1, 3)): pot_plant(mb, tuple(fr.P(r.uniform(a0 + 0.4, a1 - 0.4), 0.85, 3.8)), 0.16, 0.25, 1.0, mb_alpha=mba)
    else:
        can = cfg['canopy']
        if can == 'slab': fr.box(mb, a0, a1, 0, 0.85, 3.62, 3.78, M['concrete'], tile=(2, 2))
        else:
            tm = M['tin' if can == 'tin' else 'tin_blue']
            F(mb, [fr.P(a0, 0, 3.92), fr.P(a1, 0, 3.92), fr.P(a1, 1.9, 3.3), fr.P(a0, 1.9, 3.3)], tm, [(0, 0), (W / 2, 0), (W / 2, 1), (0, 1)], (0, 0, 1))
            F(mb, [fr.P(a0, 0, 3.91), fr.P(a1, 0, 3.91), fr.P(a1, 1.9, 3.29), fr.P(a0, 1.9, 3.29)], tm, [(0, 0), (W / 2, 0), (W / 2, 1), (0, 1)], (0, 0, -1))
            for aa in (a0 + 0.2, a1 - 0.2): tube(mb, [fr.P(aa, 0, 3.0), fr.P(aa, 1.7, 3.33)], 0.02, flat('#3a3634'), 4)
        signz = (4.0, 4.82, 0.1)
        for k in range(2): window(mb, mba, fr, a0 + 0.55 + k * (W - 0.4) / 2, a0 + 0.55 + k * (W - 0.4) / 2 + (W - 1.2) / 2, 5.1, 6.55, f"win{r.randrange(6)}", cfg['grille'])
        if r.random() < 0.6: ac_unit(mb, fr, r.uniform(a0 + 0.8, a1 - 0.8), 0.05, 4.95 if r.random() < 0.5 else 6.75)
    if cfg['sign'] is not None and signz:
        z0, z1, d = signz; fr.box(mb, a0 + 0.42, a1 - 0.12, d - 0.06, d, z0 - 0.02, z1 + 0.02, flat('#3a3634')); fr.quad(mb, a0 + 0.45, a1 - 0.15, z0, z1, d + 0.005, M['signs'], atlas_row(cfg['sign']))
        if P.get('practicals'):                                          # LED strip round the lightbox (colour from the sign row, no random draw)
            lm = M[['led_cyan', 'led_warm', 'led_green', 'led_red', 'led_blue', 'led_yellow', 'led_cyan', 'led_red'][cfg['sign']]]; e = 0.025
            for (p0, p1, q0, q1) in ((a0 + 0.42, a1 - 0.12, z0 - 0.04, z0 - 0.04 + e), (a0 + 0.42, a1 - 0.12, z1 + 0.04 - e, z1 + 0.04), (a0 + 0.42, a0 + 0.42 + e, z0 - 0.04, z1 + 0.04), (a1 - 0.12 - e, a1 - 0.12, z0 - 0.04, z1 + 0.04)):
                fr.box(mb, p0, p1, d, d + 0.02, q0, q1, lm)
            PR.append(('sign', tuple(fr.P((a0 + a1) / 2, d + 0.5, (z0 + z1) / 2)), cfg['sign']))
    if top < 8:                                                          # two-storey bay: low roof with a tin shack and plants on top
        fr.box(mb, a0 + 0.3, a1 - 0.3, -3.5, -0.6, top - 0.6, top + 1.9, M['planks'], tile=(1.5, 3)); fr.box(mb, a0 + 0.1, a1 - 0.1, -3.7, -0.3, top + 1.9, top + 2.0, M['tin'], tile=(2, 2))
        for k in range(3): pot_plant(mb, tuple(fr.P(a0 + 0.6 + k * 1.2, -0.25, top + 0.1)), 0.2, 0.35, 1.2, mb_alpha=mba)
        row_mass(mb, fr, a0, a1, top=top); return
    # floor 3
    window(mb, mba, fr, a0 + 0.6, a1 - 0.35, 8.25, 9.75, f"win{r.randrange(6)}", cfg['grille'] if r.random() < 0.8 else None)
    if cfg['f3'] == 'win_ac': ac_unit(mb, fr, r.uniform(a0 + 0.9, a1 - 0.9), 0.05, 7.45)
    if r.random() < 0.5: laundry_line(mb, mba, fr, a0 + 0.6, a1 - 0.4, 0.45, 8.15, r, 4)
    # downpipe, meter
    tube(mb, [fr.P(a0 + 0.18, 0.2, FH), fr.P(a0 + 0.18, 0.2, 0.1), fr.P(a0 + 0.18, 0.4, 0.05)], 0.05, flat('#d8d2c4'), 8)
    fr.box(mb, a0 + 0.06, a0 + 0.32, 0.12, 0.26, 2.3, 2.75, flat('#e4e0d4'), front=M['posters'])
    # roof top things
    row_mass(mb, fr, a0, a1)
    rf = cfg['roof']; ac_ = (a0 + a1) / 2
    if rf == 'tank': fr.cyl(mb, ac_, -2.0, FH - 0.85, FH + 0.6, 0.5, flat('#3a72b0', 0.85)); fr.box(mb, ac_ - 0.6, ac_ + 0.6, -2.6, -1.4, FH - 0.85, FH - 0.7, flat('#5a5650'))
    elif rf == 'shack':
        fr.box(mb, a0 + 0.4, a1 - 0.6, -4.5, -1.2, FH - 0.85, FH + 1.6, M['planks'], tile=(1.5, 3)); fr.box(mb, a0 + 0.2, a1 - 0.4, -4.7, -0.9, FH + 1.6, FH + 1.7, M['tin'], tile=(2, 2))
    elif rf == 'antenna':
        tube(mb, [fr.P(ac_, -1.5, FH - 0.85), fr.P(ac_, -1.5, FH + 2.5)], 0.02, flat('#8a8a8a'), 4)
        for k in range(5): tube(mb, [fr.P(ac_ - 0.5 + k * 0.05, -1.5 - 0.4, FH + 1.6 + k * 0.15), fr.P(ac_ - 0.5 + k * 0.05, -1.5 + 0.4, FH + 1.6 + k * 0.15)], 0.008, flat('#8a8a8a'), 4)

def row_mass(mb, fr, a0, a1, depth=12.0, top=FH):
    fr.hquad(mb, a0, a1, -depth, 0, top - 0.85, flat('#8a857a'), True)
    fr.box(mb, a0, a1, -depth, -depth + 0.2, top - 0.85, top, flat('#8a857a'))

# ----------------------------------------------------------------------------- the hero shop
HERO = (4.0, 12.0)
def hero_shop(G, r):
    fr = Fr('L'); mb, mba, pm = G['hero'], G['alpha'], G['props']; a0, a1 = HERO; W = a1 - a0; wall = M['fac_hero']
    mi = mb
    if P.get('practicals'): mi = pm = G['hero_in']                     # evening: the workshop interior is its own object (light linking)
    U = lambda a: (a - a0) / W; V = lambda z: z / FH; zo = 3.45; D = 6.0
    ops = [(a0 + 0.36, 7.82), (8.18, a1 - 0.36)]
    fr.quad(mb, a0, a1, zo, FH, 0, wall, (0, V(zo), 1, 1))
    for (p0, p1) in ((a0, a0 + 0.36), (7.82, 8.18), (a1 - 0.36, a1)):
        fr.box(mb, p0, p1, 0, 0.14, 0, zo + 0.1, M['pier4'], front=M['pier4'])
    for z in (3.75, 7.05): fr.box(mb, a0, a1, 0, 0.08, z, z + 0.22, flat('#c8c2b4'))
    fr.box(mb, a0, a1, -0.1, 0.1, FH, FH + 0.1, flat('#9a968c'))
    # interior: 8 x 6 m workshop
    fr.quad(mi, a0 + 0.36, a1 - 0.36, 0.12, 3.6, -D, M['hero_wall'], (0, 0.03, 1, 0.93))
    fr.hquad(mi, a0 + 0.36, a1 - 0.36, -D, 0, 0.12, M['hero_floor'], True, (0, 0, 2, 1.5)); fr.hquad(mi, a0 + 0.36, a1 - 0.36, -D, 0, 3.6, flat('#3e3a38'), False)
    fr.side(mi, a0 + 0.36, -D, 0, 0, 3.6, M['concrete_dark'], 1, (0, 0, 3, 1.8)); fr.side(mi, a1 - 0.36, -D, 0, 0, 3.6, M['concrete_dark'], -1, (0, 0, 3, 1.8))
    fr.quad(mi, a0, a1, zo, 3.6, -0.02, flat('#3a3634'))
    for (p0, p1) in ops:
        fr.box(mb, p0 - 0.04, p1 + 0.04, 0, 0.34, zo - 0.3, zo + 0.12, flat('#7a7e80'))                # rolled-up shutter box
        fr.box(mb, p0, p1, 0.02, 0.08, zo - 0.36, zo - 0.3, flat('#4a4e50'))
        if P['tubes'] > 0:
            for dd in (-1.5, -4.0): fr.box(mb, (p0 + p1) / 2 - 0.6, (p0 + p1) / 2 + 0.6, dd - 0.03, dd + 0.03, 3.5, 3.55, M['tube'])
            if P.get('practicals') and p0 < 8.0: PR.append(('hero_tube', tuple(fr.P(8.0, -1.5, 3.46)), tuple(fr.na)))   # one long light for the whole workshop
    fr.box(mb, a0 + 0.36, a1 - 0.36, -0.06, 0.0, 0.0, 0.12, flat('#6a665e'))
    st = flat('#5a5c60', 0.8); rust = flat('#8a4a28', 0.8); stl = flat('#9aa0a4', 0.85)
    # steel stock rack on the left wall: cantilever arms with long bars along d
    for z in (0.6, 1.2, 1.8, 2.4):
        for d in (-0.6, -2.4, -4.2): fr.box(pm, a0 + 0.36, a0 + 0.9, d - 0.04, d + 0.04, z - 0.05, z, st)
        for k in range(r.randint(6, 12)):
            aa = a0 + 0.42 + r.uniform(0, 0.45); s = r.choice([0.02, 0.025, 0.04, 0.05])
            fr.box(pm, aa, aa + s, -5.8, -0.2 + r.uniform(-0.3, 0.2), z, z + s, r.choice([st, rust, stl, st]))
    for d in (-0.6, -2.4, -4.2): fr.box(pm, a0 + 0.36, a0 + 0.46, d - 0.05, d + 0.05, 0.12, 2.7, st)
    # bars leaning at the back wall, sheets, drill press, chop saw, anvil, cylinders, hanging gates
    for k in range(26):
        aa = r.uniform(a0 + 1.2, a0 + 3.3); s = r.choice([0.02, 0.03, 0.04])
        p0 = fr.P(aa, -5.6 + r.uniform(-0.1, 0.1), 0.12); p1 = fr.P(aa + r.uniform(-0.15, 0.15), -5.95, 3.2 + r.uniform(-0.3, 0.2)); tube(pm, [p0, p1], s, r.choice([st, rust, stl]), 4)
    for k in range(5): F(pm, [fr.P(a1 - 2.0 + k * 0.05, -5.4 + k * 0.08, 0.12), fr.P(a1 - 0.6 + k * 0.05, -5.4 + k * 0.08, 0.12), fr.P(a1 - 0.6, -5.95, 2.3), fr.P(a1 - 2.0, -5.95, 2.3)], r.choice([st, stl, rust]), None, fr.nd)
    dp = (a1 - 1.4, -3.0); fr.box(pm, dp[0] - 0.25, dp[0] + 0.25, dp[1] - 0.3, dp[1] + 0.25, 0.12, 0.2, st); fr.cyl(pm, dp[0], dp[1] - 0.15, 0.2, 1.7, 0.05, st)
    fr.box(pm, dp[0] - 0.12, dp[0] + 0.12, dp[1] - 0.15, dp[1] + 0.3, 1.2, 1.75, flat('#3a6a4a')); fr.box(pm, dp[0] - 0.2, dp[0] + 0.2, dp[1] - 0.1, dp[1] + 0.3, 0.75, 0.8, st)
    cs = (a0 + 2.0, -2.2); fr.box(pm, cs[0] - 0.4, cs[0] + 0.4, cs[1] - 0.3, cs[1] + 0.3, 0.12, 0.7, flat('#5a7a6a'))
    fr.box(pm, cs[0] - 0.25, cs[0] + 0.25, cs[1] - 0.25, cs[1] + 0.25, 0.7, 0.78, st); fr.cyl(pm, cs[0], cs[1], 0.78, 1.05, 0.18, flat('#c8302a'), 16)
    fr.box(pm, cs[0] - 0.05, cs[0] + 0.05, cs[1] - 0.05, cs[1] + 0.35, 0.95, 1.05, flat('#c8302a'))
    av = (a0 + 4.6, -1.6); fr.cyl(pm, av[0], av[1], 0.12, 0.62, 0.18, flat('#5a3a20'), 10); fr.box(pm, av[0] - 0.3, av[0] + 0.3, av[1] - 0.1, av[1] + 0.1, 0.62, 0.8, flat('#2e2e30'))
    for k, aa in enumerate((a1 - 0.9, a1 - 0.62)):
        fr.cyl(pm, aa, -1.0, 0.12, 1.45, 0.11, flat(['#1e1e22', '#7a2228'][k], 0.8), 12); pm.sphere(tuple(fr.P(aa, -1.0, 1.45)), 0.11, flat(['#1e1e22', '#7a2228'][k], 0.8), 10, 5)
        fr.cyl(pm, aa, -1.0, 1.5, 1.62, 0.04, flat('#c8a040'), 8)
    for k, (gt, aa) in enumerate((('gate_white', a0 + 3.6), ('gate_red', a0 + 5.2))):         # finished gates hanging on the back wall
        fr.quad(mba, aa - 0.7, aa + 0.7, 1.7, 3.1, -5.9 + 0.1 * k, M[gt])
    fr.box(pm, a0 + 5.6, a0 + 6.6, -5.98, -5.7, 2.95, 3.0, flat('#8a5a30')); fr.box(pm, a0 + 5.8, a0 + 6.4, -5.9, -5.75, 3.0, 3.25, flat('#e8c040'))   # Buddha shelf
    fr.box(pm, a0 + 5.95, a0 + 6.05, -5.88, -5.8, 3.0, 3.1, M['red_bulb'])
    fr.box(pm, a0 + 4.2, a0 + 6.0, -1.2, -0.4, 0.12, 0.88, st, tile=(1, 1)); fr.box(pm, a0 + 4.15, a0 + 6.05, -1.25, -0.35, 0.88, 0.92, M['bench_top'])   # inner workbench
    for k in range(6):
        aa = a0 + 4.3 + k * 0.28; fr.box(pm, aa, aa + r.uniform(0.1, 0.25), -1.1, -0.5, 0.92, 0.92 + r.uniform(0.03, 0.15), r.choice([st, rust, flat('#c8302a'), flat('#e8b020')]))
    # big red/yellow sign + services board, lamp arms
    fr.box(mb, a0 + 0.1, a1 - 0.1, 0.05, 0.16, 3.95, 5.62, flat('#5a2a1a')); fr.quad(mb, a0 + 0.2, a1 - 0.2, 4.0, 5.57, 0.165, M['sign_hero'])
    for aa in (a0 + 1.6, a0 + 4.0, a1 - 1.6):
        tube(mb, [fr.P(aa, 0.05, 5.85), fr.P(aa, 0.7, 5.95)], 0.02, flat('#2a2a2e'), 4); fr.box(mb, aa - 0.12, aa + 0.12, 0.6, 0.8, 5.82, 5.95, flat('#2a2a2e'))
        if P.get('practicals'):
            fr.box(mb, aa - 0.1, aa + 0.1, 0.62, 0.78, 5.8, 5.82, M['lamp']); PR.append(('sign_spot', tuple(fr.P(aa, 0.7, 5.78)), tuple(fr.P(aa, 0.16, 4.5))))
    # tin awning over the apron (attaches under the sign)
    F(mb, [fr.P(a0, 0.0, 3.92), fr.P(a1, 0.0, 3.92), fr.P(a1, 1.55, 3.55), fr.P(a0, 1.55, 3.55)], M['tin'], [(0, 0), (4, 0), (4, 0.8), (0, 0.8)], (0, 0, 1))
    F(mb, [fr.P(a0, 0.0, 3.91), fr.P(a1, 0.0, 3.91), fr.P(a1, 1.55, 3.54), fr.P(a0, 1.55, 3.54)], M['tin'], [(0, 0), (4, 0), (4, 0.8), (0, 0.8)], (0, 0, -1))
    fr.box(mb, a0, a1, 1.5, 1.58, 3.42, 3.56, flat('#2a2a2e'))
    for aa in (a0 + 0.2, 8.0, a1 - 0.2): tube(mb, [fr.P(aa, 0.1, 3.2), fr.P(aa, 1.5, 3.52)], 0.025, flat('#2a2a2e'), 4)
    # floor 2: windows with the shop's own ornate grilles; floor 3: balcony cage in black/gold gate panels, laundry, plants
    for k in range(4): window(mb, mba, fr, a0 + 0.55 + k * 1.95, a0 + 0.55 + k * 1.95 + 1.4, 5.95, 6.75, f'win{k}', 'grille_sun', False)
    for k in range(2): fr.box(mb, a0 + 0.3 + k * 4, a0 + 3.7 + k * 4, 0, 0.5, 6.85, 6.95, M['concrete'], tile=(2, 2))
    ac_unit(mb, fr, a0 + 3.95, 0.05, 6.25, 0.7, 0.5); ac_unit(mb, fr, a1 - 0.45, 0.05, 9.3, 0.7, 0.5)
    fr.box(mb, a0, a1, 0, 1.0, 7.15, 7.3, M['concrete'], tile=(2, 2))
    window(mb, mba, fr, a0 + 0.8, a0 + 3.4, 7.6, 9.6, 'win4', None, False); window(mb, mba, fr, a0 + 4.6, a1 - 0.8, 7.6, 9.6, 'win5', None, False)
    for k in range(5): fr.quad(mba, a0 + 0.05 + k * 1.59, a0 + 0.05 + (k + 1) * 1.59, 7.3, 8.75, 0.98, M['gate_black'], (0, 0.08, 1, 0.92))
    fr.box(mb, a0, a1, 0, 1.05, 9.9, 10.0, M['tin'], tile=(2, 2)); fr.box(mb, a0, a1, 0.93, 1.0, 8.72, 8.8, flat('#1e1c1e'))
    for aa in (a0 + 0.04, 8.0, a1 - 0.04): fr.box(mb, aa - 0.025, aa + 0.025, 0.95, 1.0, 7.3, 9.9, flat('#1e1c1e'))
    laundry_line(mb, mba, fr, a0 + 0.4, a1 - 0.4, 0.55, 9.5, r, 12)
    if P.get('practicals'):
        bp = fr.P(a0 + 2.2, 0.55, 9.7); mb.sphere(tuple(bp), 0.05, M['bulb'], 10, 6); tube(mb, [bp + Vector((0, 0, 0.04)), bp + Vector((0, 0, 0.2))], 0.004, flat('#1a1a1a'), 4)
        PR.append(('balcony', tuple(bp - Vector((0, 0, 0.07))), None))
    for k in range(6): pot_plant(mb, tuple(fr.P(a0 + 0.5 + k * 1.4, 0.8, 7.3)), 0.15, 0.25, 0.9, mb_alpha=mba)
    tube(mb, [fr.P(a0 + 0.18, 0.2, FH), fr.P(a0 + 0.18, 0.2, 0.1)], 0.05, flat('#d8d2c4'), 8)
    row_mass(mb, fr, a0, a1)

def hero_front(G, r):
    """Pavement in front of the shop: welding bench with the half-made gate, gates on display, welding machine, cylinders, cables, grinder,
    Jae Hong's cashier table with a fan and her sun-faded chair, stools, services board. Returns anchors."""
    fr = Fr('L'); pm, mba = G['props'], G['alpha']; st = flat('#4a4c50', 0.8); dark = flat('#1e1e20', 0.8)
    # welding bench: 2.6 x 0.95 m, top at 0.9
    ba0, ba1, bd0, bd1 = 6.3, 8.9, 1.0, 1.95; zt = 0.9
    for (aa, dd) in ((ba0 + 0.05, bd0 + 0.05), (ba1 - 0.05, bd0 + 0.05), (ba0 + 0.05, bd1 - 0.05), (ba1 - 0.05, bd1 - 0.05)): fr.box(pm, aa - 0.035, aa + 0.035, dd - 0.035, dd + 0.035, 0, zt - 0.03, st)
    fr.box(pm, ba0 + 0.05, ba1 - 0.05, bd0 + 0.02, bd1 - 0.02, 0.25, 0.29, st)
    fr.box(pm, ba0, ba1, bd0, bd1, zt - 0.03, zt, flat('#3a3836'), front=M['bench_top'])
    fr.hquad(pm, ba0, ba1, bd0, bd1, zt + 0.001, M['bench_top'], True)
    fr.box(pm, ba0 + 0.1, ba1 - 0.1, bd0 + 0.1, bd1 - 0.1, 0.29, 0.31, flat('#6a5a4a'))
    for k in range(22):                                                  # bar stock and angle offcuts on the shelf, along the bench
        dd = bd0 + 0.12 + r.uniform(0, bd1 - bd0 - 0.3); s_ = r.choice([0.02, 0.025, 0.03, 0.04]); l0 = ba0 + r.uniform(0.05, 0.6); l1 = ba1 - r.uniform(0.05, 0.9)
        fr.box(pm, l0, l1, dd, dd + s_, 0.31 + (k % 3) * 0.02, 0.31 + (k % 3) * 0.02 + s_, r.choice([st, flat('#8a4a28'), flat('#6a6c70'), st]))
    # half-made gate clamped on the bench: raw steel frame (real bars) + scroll texture
    g0, g1, gd0, gd1 = ba0 + 0.25, ba0 + 1.75, bd0 + 0.08, bd1 - 0.05; zg = zt + 0.02
    fr.hquad(mba, g0, g1, gd0, gd1, zg + 0.012, M['gate_raw'], True, (0, 0.13, 1, 0.97))
    raw = flat('#9aa2ac', 0.9)
    for (x0, x1, y0, y1) in ((g0, g1, gd0, gd0 + 0.03), (g0, g1, gd1 - 0.03, gd1), (g0, g0 + 0.03, gd0, gd1), (g1 - 0.03, g1, gd0, gd1), (g0, g1, (gd0 + gd1) / 2 - 0.015, (gd0 + gd1) / 2 + 0.015)):
        fr.box(pm, x0, x1, y0, y1, zt, zg + 0.012, raw)
    for k in range(6): aa = g0 + (k + 1) * (g1 - g0) / 7; fr.box(pm, aa - 0.01, aa + 0.01, (gd0 + gd1) / 2, gd1, zt, zg + 0.01, raw)
    for aa in (g0 + 0.1, g1 - 0.1):                                    # C-clamps
        fr.box(pm, aa - 0.02, aa + 0.02, gd0 - 0.12, gd0 + 0.04, zg + 0.012, zg + 0.04, flat('#c8302a')); fr.box(pm, aa - 0.02, aa + 0.02, gd0 - 0.12, gd0 - 0.09, zt - 0.12, zg + 0.04, flat('#c8302a'))
        fr.cyl(pm, aa, gd0 + 0.02, zt - 0.12, zt - 0.03, 0.008, st, 6)
    bench_point = fr.P(g1 - 0.03, (gd0 + gd1) / 2, zg + 0.02)
    # payment slip, held down by a wrench; grinder; welding helmet; electrode box; hammer; phone
    sa, sd = ba1 - 0.5, bd0 + 0.5
    sl = MB(); rect(sl, (0, 0, 0), (0.105, 0, 0), (0, 0.145, 0), M['slip']); so = sl.obj('soi_slip', G['coll']); so.location = fr.P(sa, sd, zt + 0.003); so.rotation_euler = (0, 0, math.radians(84 if fr.L else -96))
    wr = MB(); wr.box((-0.13, -0.012, 0), (0.13, 0.012, 0.01), flat('#b8bcc0')); wr.frustum((0.15, 0, 0), (0.15, 0, 0.012), 0.035, 0.035, flat('#b8bcc0'), seg=8)
    wo = wr.obj('soi_wrench', G['coll']); wo.location = fr.P(sa + 0.12, sd - 0.06, zt + 0.004); wo.rotation_euler = (0, 0, 2.3)
    gp = fr.P(ba0 + 0.1, bd0 + 0.25, zt); gx = MB()
    gx.frustum((0, 0, 0.045), (0.24, 0, 0.045), 0.04, 0.045, flat('#2a5ab0'), seg=10); gx.frustum((0.24, 0, 0.045), (0.3, 0, 0.045), 0.05, 0.05, dark, seg=10)
    gx.frustum((0.3, 0, 0.0), (0.3, 0, 0.09), 0.065, 0.065, flat('#8a8e90'), seg=16); gx.frustum((0.3, 0, -0.005), (0.3, 0, 0.0), 0.06, 0.06, flat('#4a3a2a'), seg=16)
    gx.frustum((0.22, 0, 0.08), (0.22, 0.12, 0.1), 0.015, 0.015, dark, seg=6); gx.frustum((-0.12, 0, 0.045), (0, 0, 0.045), 0.012, 0.03, dark, seg=6)
    go = gx.obj('soi_grinder', G['coll']); go.location = gp + Vector((0, 0, 0.005)); go.rotation_euler = (math.radians(90), 0, 2.2)
    fr.box(pm, ba1 - 0.32, ba1 - 0.05, bd0 + 0.05, bd0 + 0.33, zt, zt + 0.06, flat('#2a2a2e')); fr.box(pm, ba1 - 0.24, ba1 - 0.13, bd0 + 0.13, bd0 + 0.23, zt + 0.06, zt + 0.065, flat('#1a4a2a', 0.6))   # welding mask, face down
    fr.box(pm, ba0 + 1.82, ba0 + 2.07, bd0 + 0.05, bd0 + 0.17, zt, zt + 0.07, flat('#e8b020')); fr.box(pm, ba0 + 1.85, ba0 + 2.15, bd0 + 0.25, bd0 + 0.28, zt, zt + 0.025, flat('#8a5a30'))
    fr.box(pm, ba0 + 2.13, ba0 + 2.23, bd0 + 0.23, bd0 + 0.31, zt, zt + 0.04, flat('#4a4c50'))
    fr.box(pm, ba0 + 1.9, ba0 + 1.98, bd0 + 0.45, bd0 + 0.6, zt, zt + 0.012, M['phone'])
    for k in range(14): aa = ba0 + 0.1 + r.uniform(0, 2.3); fr.box(pm, aa, aa + r.uniform(0.02, 0.12), bd1 - 0.12, bd1 - 0.05, zt, zt + 0.006, r.choice([flat('#3a3a3a'), flat('#9aa0a4')]))
    for k in range(10):                                                 # welding rods, bolts, nuts, soapstone, tape, glass of iced coffee
        aa = r.uniform(ba1 - 0.85, ba1 - 0.1); dd = r.uniform(bd0 + 0.6, bd1 - 0.08); t = r.uniform(0, 3.14)
        tube(pm, [fr.P(aa, dd, zt + 0.004), fr.P(aa + 0.32 * math.cos(t), dd + 0.32 * math.sin(t) * 0.3, zt + 0.004)], 0.0025, flat(r.choice(['#4a4c50', '#8a8a8a', '#c8b070'])), 4)
    for k in range(14):
        aa = r.uniform(ba0 + 1.6, ba1 - 0.1); dd = r.uniform(bd0 + 0.05, bd1 - 0.05)
        if r.random() < 0.5: fr.cyl(pm, aa, dd, zt, zt + 0.012, r.uniform(0.008, 0.014), flat(r.choice(['#9aa0a4', '#c8a040', '#5a5c60'])), 6)
        else: fr.box(pm, aa - 0.01, aa + 0.01, dd - 0.03, dd + 0.03, zt, zt + 0.01, flat('#7a7c80'))
    fr.box(pm, ba1 - 0.85, ba1 - 0.75, bd0 + 0.08, bd0 + 0.11, zt, zt + 0.012, flat('#f4f0e4'))
    fr.cyl(pm, ba1 - 0.62, bd1 - 0.15, zt, zt + 0.035, 0.045, flat('#f0c020'), 14); fr.cyl(pm, ba1 - 0.62, bd1 - 0.15, zt + 0.035, zt + 0.037, 0.02, flat('#2a2a2e'), 8)
    fr.cyl(pm, ba1 - 0.18, bd1 - 0.42, zt, zt + 0.14, 0.04, flat('#c8e0e8', 0.7), 12); fr.cyl(pm, ba1 - 0.18, bd1 - 0.42, zt + 0.02, zt + 0.1, 0.037, flat('#6a3a1e'), 12)
    tube(pm, [fr.P(ba1 - 0.17, bd1 - 0.42, zt + 0.08), fr.P(ba1 - 0.15, bd1 - 0.44, zt + 0.2)], 0.004, flat('#e83a2a'), 4)
    # welding machine + cables (stinger on the bench, ground clamp on the gate)
    wm = (ba1 + 0.45, 1.45); fr.box(pm, wm[0] - 0.22, wm[0] + 0.22, wm[1] - 0.3, wm[1] + 0.3, 0.08, 0.5, flat('#c8302a'))
    fr.box(pm, wm[0] - 0.24, wm[0] + 0.24, wm[1] + 0.3, wm[1] + 0.31, 0.12, 0.46, flat('#2a2a2e')); fr.box(pm, wm[0] - 0.24, wm[0] + 0.24, wm[1] - 0.32, wm[1] + 0.32, 0.5, 0.53, flat('#2a2a2e'))
    for k in (-1, 1): fr.cyl(pm, wm[0] + k * 0.2, wm[1], 0.0, 0.0001, 0.001, dark)
    for (aa, dd) in ((wm[0] - 0.18, wm[1] - 0.25), (wm[0] + 0.18, wm[1] - 0.25), (wm[0] - 0.18, wm[1] + 0.25), (wm[0] + 0.18, wm[1] + 0.25)):
        pm.frustum(tuple(fr.P(aa, dd, 0.04) + Vector((-0.03, 0, 0))), tuple(fr.P(aa, dd, 0.04) + Vector((0.03, 0, 0))), 0.04, 0.04, dark, seg=8)
    fr.box(pm, wm[0] - 0.1, wm[0] + 0.1, wm[1] + 0.31, wm[1] + 0.33, 0.35, 0.44, flat('#e8e4d8'))
    pts = [fr.P(wm[0] - 0.1, wm[1] + 0.32, 0.3), fr.P(wm[0] - 0.3, wm[1] + 0.7, 0.03), fr.P(ba1 - 0.4, 2.3, 0.03), fr.P(ba1 - 1.3, 2.25, 0.03), fr.P(ba1 - 1.5, 2.05, 0.03),
           fr.P(ba1 - 1.1, 2.0, 0.03), fr.P(ba1 - 0.9, bd1 + 0.02, 0.5), fr.P(ba1 - 0.85, bd1 - 0.15, zt + 0.03), fr.P(ba1 - 0.95, bd1 - 0.3, zt + 0.04)]
    tube(pm, smooth(pts, 4), 0.014, dark, 6)
    pts = [fr.P(wm[0] + 0.1, wm[1] + 0.32, 0.3), fr.P(wm[0], wm[1] + 0.8, 0.03), fr.P(ba1 - 0.3, bd0 - 0.15, 0.03), fr.P(g1 + 0.1, bd0 - 0.05, 0.6), fr.P(g1 - 0.05, gd0 + 0.1, zg + 0.03)]
    tube(pm, smooth(pts, 4), 0.012, dark, 6)
    for k in range(3):                                                  # coil of spare cable on the apron
        c = fr.P(ba0 - 0.35, 1.7, 0.02 + k * 0.025); tube(pm, [c + Vector((math.cos(t) * 0.28, math.sin(t) * 0.28, 0)) for t in [i * math.pi / 10 for i in range(21)]], 0.013, dark, 5)
    # gas cylinders chained to the pier at 8.0 (oxygen black, acetylene maroon) + hoses + torch
    for k, (col, aa) in enumerate((('#1e1e22', 11.0), ('#7a2228', 11.32))):
        fr.cyl(pm, aa, 0.35, 0.0, 1.3, 0.115, flat(col, 0.8), 12); pm.sphere(tuple(fr.P(aa, 0.35, 1.3)), 0.115, flat(col, 0.8), 10, 5)
        fr.cyl(pm, aa, 0.35, 1.38, 1.5, 0.035, flat('#c8a040'), 8); fr.box(pm, aa - 0.03, aa + 0.03, 0.35, 0.42, 1.4, 1.47, flat('#c8a040'))
        tube(pm, smooth([fr.P(aa, 0.42, 1.45), fr.P(aa + 0.1, 0.7, 0.8), fr.P(aa + 0.3, 0.8, 0.03), fr.P(ba1 - 0.3, bd0 - 0.05, 0.03), fr.P(ba1 - 0.2, bd0 + 0.1, zt + 0.02)], 3), 0.008, flat(['#2a8a3a', '#c83a2a'][k]), 5)
    tube(pm, [fr.P(10.85, 0.2, 1.0), fr.P(11.17, 0.5, 0.95), fr.P(11.5, 0.2, 1.0)], 0.006, flat('#9aa0a4'), 4)
    # finished gates on display: leaning against the neighbour's shutter and the shop's end pier
    gates = [('gate_black', 12.15, 1.7, 0.42), ('gate_green', 12.5, 1.6, 0.3), ('gate_white', 13.1, 1.55, 0.18), ('gate_red', 13.9, 1.4, 0.08), ('gate_black', 10.1, 1.5, 0.55)]
    for (gt, aa, s, dd) in gates:
        lean = 0.22; F(mba, [fr.P(aa, dd + lean, 0.02), fr.P(aa + s, dd + lean, 0.02), fr.P(aa + s, dd, s * 1.0), fr.P(aa, dd, s * 1.0)], M[gt], [(0, 0.04), (1, 0.04), (1, 0.98), (0, 0.98)], fr.nd)
        for (x0) in (aa, aa + s - 0.03): tube(pm, [fr.P(x0 + 0.015, dd + lean, 0.02), fr.P(x0 + 0.015, dd, s * 0.98)], 0.015, flat({'gate_black': '#1e1c1e', 'gate_green': '#2a6a4a', 'gate_white': '#ecebe4', 'gate_red': '#9a3a2a'}[gt]), 4)
    # services board on an A-frame
    sb = (11.1, 1.25); F(pm, [fr.P(sb[0] - 0.6, sb[1] + 0.25, 0), fr.P(sb[0] + 0.6, sb[1] + 0.25, 0), fr.P(sb[0] + 0.6, sb[1], 0.7), fr.P(sb[0] - 0.6, sb[1], 0.7)], M['sign_board'], None, fr.nd + Vector((0, 0, 0.3)))
    F(pm, [fr.P(sb[0] - 0.6, sb[1] - 0.25, 0), fr.P(sb[0] + 0.6, sb[1] - 0.25, 0), fr.P(sb[0] + 0.6, sb[1] - 0.01, 0.7), fr.P(sb[0] - 0.6, sb[1] - 0.01, 0.7)], flat('#2a2a2e'), None, -fr.nd)
    # Jae Hong's cashier table (by the near pier), electric fan, calculator, receipt book, jar; her sun-faded chair
    ta0, ta1, td0, td1, zt2 = 4.45, 5.55, 0.25, 0.95, 0.76
    fr.box(pm, ta0, ta1, td0, td1, zt2 - 0.03, zt2, flat('#c8b088'))
    for (aa, dd) in ((ta0 + 0.04, td0 + 0.04), (ta1 - 0.04, td0 + 0.04), (ta0 + 0.04, td1 - 0.04), (ta1 - 0.04, td1 - 0.04)): fr.box(pm, aa - 0.02, aa + 0.02, dd - 0.02, dd + 0.02, 0, zt2 - 0.03, flat('#6a6a6e'))
    fr.box(pm, ta0 + 0.02, ta1 - 0.02, td0 + 0.02, td0 + 0.04, 0.3, zt2 - 0.03, flat('#a89070'))
    fp = fr.P(ta0 + 0.2, td0 + 0.2, zt2); fr.cyl(pm, ta0 + 0.2, td0 + 0.2, zt2, zt2 + 0.04, 0.11, flat('#3a8ad0'), 12); fr.cyl(pm, ta0 + 0.2, td0 + 0.2, zt2, zt2 + 0.32, 0.018, flat('#e8e8e4'), 8)
    fc = fr.P(ta0 + 0.2, td0 + 0.26, zt2 + 0.4); dv = (fr.nd * 0.6 + fr.na * 0.8).normalized()
    pm.frustum(tuple(fc - dv * 0.08), tuple(fc + dv * 0.05), 0.07, 0.07, flat('#3a8ad0'), seg=12); pm.frustum(tuple(fc + dv * 0.05), tuple(fc + dv * 0.1), 0.2, 0.2, flat('#e8eef4'), seg=20, cap0=False, cap1=False)
    for k in range(3):
        a = k * 2.094; u = Vector((0, 0, 1)); w = dv.cross(u).normalized(); bl = fc + dv * 0.075 + (math.cos(a) * u + math.sin(a) * w) * 0.1
        rect(pm, bl, (math.cos(a) * u + math.sin(a) * w) * 0.08, (-math.sin(a) * u + math.cos(a) * w) * 0.035, flat('#7ac0f0', 0.75))
    for k in range(9):                                                   # fan guard wires
        a = k * math.pi / 9; u = Vector((0, 0, 1)); w = dv.cross(u).normalized(); e = (math.cos(a) * u + math.sin(a) * w) * 0.2
        tube(pm, [fc + dv * 0.1 - e, fc + dv * 0.16, fc + dv * 0.1 + e], 0.003, flat('#e8eef4'), 3)
    fr.box(pm, ta0 + 0.5, ta0 + 0.66, td0 + 0.15, td0 + 0.27, zt2, zt2 + 0.02, flat('#2a2a2e')); fr.box(pm, ta0 + 0.75, ta0 + 0.98, td0 + 0.12, td0 + 0.4, zt2, zt2 + 0.025, flat('#f4f0e4'))
    fr.cyl(pm, ta1 - 0.15, td1 - 0.15, zt2, zt2 + 0.2, 0.07, flat('#c8e0e8', 0.7), 12); fr.box(pm, ta0 + 0.3, ta0 + 0.45, td1 - 0.2, td1 - 0.1, zt2, zt2 + 0.01, M['phone'])
    fr.box(pm, ta1 - 0.45, ta1 - 0.3, td1 - 0.3, td1 - 0.1, zt2, zt2 + 0.12, flat('#e8b020'))
    ch = (5.2, 1.35); chair = flat('#e89a8a', 0.8, (0.9, 1.05, 1.25))
    for (aa, dd) in ((ch[0] - 0.2, ch[1] - 0.2), (ch[0] + 0.2, ch[1] - 0.2), (ch[0] - 0.2, ch[1] + 0.2), (ch[0] + 0.2, ch[1] + 0.2)):
        pm.frustum(tuple(fr.P(aa, dd, 0)), tuple(fr.P(aa * 0.85 + ch[0] * 0.15, dd * 0.85 + ch[1] * 0.15, 0.44)), 0.03, 0.025, chair, seg=6)
    fr.box(pm, ch[0] - 0.24, ch[0] + 0.24, ch[1] - 0.22, ch[1] + 0.24, 0.42, 0.46, chair)
    F(pm, [fr.P(ch[0] - 0.23, ch[1] + 0.22, 0.45), fr.P(ch[0] + 0.23, ch[1] + 0.22, 0.45), fr.P(ch[0] + 0.22, ch[1] + 0.32, 0.9), fr.P(ch[0] - 0.22, ch[1] + 0.32, 0.9)], chair, None, -fr.nd)
    F(pm, [fr.P(ch[0] - 0.23, ch[1] + 0.235, 0.45), fr.P(ch[0] + 0.23, ch[1] + 0.235, 0.45), fr.P(ch[0] + 0.22, ch[1] + 0.335, 0.9), fr.P(ch[0] - 0.22, ch[1] + 0.335, 0.9)], chair, None, fr.nd)
    for k, (aa, dd) in enumerate(((9.5, 0.35), (9.9, 0.4))): stool(pm, tuple(fr.P(aa, dd, 0.0 + 0.0 * k)), ['#2a5ad0', '#d8302a'][k])
    stool(pm, tuple(fr.P(9.5, 0.35, 0.45)), '#d8302a')
    pot_plant(pm, tuple(fr.P(4.2, 0.3, 0)), 0.22, 0.4, 1.3, '#3a6ab0', mb_alpha=mba)
    return dict(bench_point=tuple(round(v, 3) for v in bench_point), bench_mark=tuple(round(v, 3) for v in fr.P(7.6, 0.5, 0)), hong_mark=tuple(round(v, 3) for v in fr.P(5.35, 1.75, 0)),
                door_mark=tuple(round(v, 3) for v in fr.P(6.0, -0.5, 0.12)), slip=tuple(round(v, 3) for v in fr.P(sa, sd, zt)), bench_top=dict(a=(ba0, ba1), x=(XL + bd0, XL + bd1), z=zt))

def smooth(pts, n=4):
    """Catmull-Rom through the points."""
    pts = [Vector(p) for p in pts]; out = []
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1]); return out

# ----------------------------------------------------------------------------- vacant lot: spirit house, banana clump, scrap pile, low wall
def vacant_lot(G, r):
    fr = Fr('L'); mb, pm, mba = G['row'], G['props'], G['alpha']; a0, a1 = 1.6, 4.0
    fr.hquad(mb, a0, a1, -8, 0, 0.0, flat('#7a7058'), True)
    fr.box(mb, a0, a0 + 0.2, -8, 0, 0, FH, M['concrete'], tile=(2, 2)); fr.quad(mb, a0 + 0.2, a1, 0, FH, -8, M['concrete_dark'], (0, 0, 1.2, 5.6))
    fr.side(mb, a1, -8, 0, 0, FH, M['fac_hero'], -1, (0.0, 0, 0.25, 1))
    fr.box(mb, a0 + 0.2, a1 - 0.9, -0.15, 0.0, 0, 1.25, M['concrete'], tile=(1.5, 1.5)); fr.box(mb, a0 + 0.2, a1 - 0.9, -0.17, 0.02, 1.25, 1.32, flat('#9a948a'))
    for aa in (a1 - 0.9, a1 - 0.05): fr.box(mb, aa - 0.1, aa + 0.1, -0.2, 0.05, 0, 1.45, M['concrete'])
    for k in range(10):                                                   # weeds
        p = fr.P(r.uniform(a0 + 0.3, a1 - 0.2), r.uniform(-6, -0.4), 0); s = r.uniform(0.25, 0.5)
        rect(mba, p + Vector((0, 0, s * 0.8)), (s, s * 0.3, 0), (0, 0, s * 0.8), M['leaves'])
    for k in range(5):                                                    # scrap pile: old tyres, bars
        fr.cyl(pm, r.uniform(a0 + 0.5, a1 - 0.5), r.uniform(-5, -3), 0.0 + k * 0.12, 0.12 + k * 0.12, 0.3, flat('#1e1e20'), 14)
    for k in range(12): tube(pm, [fr.P(r.uniform(a0 + 0.3, a1 - 0.3), -4.5 + r.uniform(-1, 1), 0.05), fr.P(r.uniform(a0 + 0.3, a1 - 0.3), -3 + r.uniform(-1, 1), r.uniform(0.1, 0.6))], 0.02, flat(r.choice(['#8a4a28', '#5a5c60'])), 4)
    # spirit house on its post, in front of the wall
    sp = fr.P(2.55, 0.45, 0); x, y = sp.x, sp.y; red = M['spirit']; gold = flat('#e8b030', 0.9, (0.9, 1.05, 1.25)); wht = flat('#f0ece4')
    mb2 = pm; mb2.box((x - 0.1, y - 0.1, 0), (x + 0.1, y + 0.1, 1.35), wht); mb2.box((x - 0.18, y - 0.18, 0), (x + 0.18, y + 0.18, 0.12), wht)
    mb2.box((x - 0.42, y - 0.42, 1.35), (x + 0.42, y + 0.42, 1.42), gold); mb2.box((x - 0.26, y - 0.22, 1.42), (x + 0.26, y + 0.22, 1.85), red, tile=(0.5, 0.5))
    for (dx, dy) in ((-0.26, -0.22), (0.26, -0.22), (-0.26, 0.22), (0.26, 0.22)): mb2.frustum((x + dx, y + dy, 1.42), (x + dx, y + dy, 1.9), 0.025, 0.025, gold, seg=6)
    for t, (h0, w) in enumerate(((1.88, 0.36), (2.08, 0.27), (2.24, 0.18))):
        for sgn in (-1, 1): F(mb2, [Vector((x - w * 1.25, y, h0 + 0.24)), Vector((x + w * 1.25, y, h0 + 0.24)), Vector((x + w * 1.2, y + sgn * w, h0)), Vector((x - w * 1.2, y + sgn * w, h0))], red, None, (0, sgn, 0.5))
        for sgn in (-1, 1):
            F(mb2, [Vector((x + sgn * w * 1.2, y - w, h0)), Vector((x + sgn * w * 1.2, y + w, h0)), Vector((x + sgn * w * 1.25, y, h0 + 0.24))], gold, None, (sgn, 0, 0))
            tube(mb2, [Vector((x + sgn * w * 1.25, y, h0 + 0.24)), Vector((x + sgn * w * 1.4, y, h0 + 0.36))], 0.012, gold, 4)
    mb2.frustum((x, y, 2.48), (x, y, 2.85), 0.05, 0.0, gold, seg=8)
    if P.get('practicals'):                                              # the little red/orange bulbs of the spirit house
        for k in range(5): mb2.sphere((x - 0.24 + k * 0.12, y - 0.43, 1.83), 0.018, M['led_red'] if k % 2 else M['led_yellow'], 6, 4)
        PR.append(('spirit', (x, y - 0.6, 1.75), None))
    for k in range(4): mb2.sphere((x - 0.3 + k * 0.2, y - 0.36, 1.47), 0.035, flat('#f08a20'), 8, 4)   # marigold garlands
    for k in range(5): mb2.frustum((x - 0.35 + k * 0.08, y + 0.33, 1.42), (x - 0.35 + k * 0.08, y + 0.33, 1.6), 0.022, 0.018, flat('#d8281e', 0.8, (0.9, 1.05, 1.25)), seg=6)   # red soda bottles
    mb2.frustum((x + 0.3, y + 0.3, 1.42), (x + 0.3, y + 0.3, 1.5), 0.05, 0.06, flat('#8a6a3a'), seg=8)
    for k in range(4): tube(mb2, [Vector((x + 0.3 + k * 0.01, y + 0.3, 1.5)), Vector((x + 0.29 + k * 0.015, y + 0.31, 1.68))], 0.003, flat('#c8302a'), 3)
    mb2.box((x - 0.06, y - 0.4, 1.42), (x + 0.06, y - 0.32, 1.55), flat('#2a2a2e')); mb2.box((x + 0.12, y - 0.4, 1.42), (x + 0.2, y - 0.34, 1.52), flat('#f0ece4'))
    # banana clump behind the lot wall
    bc = fr.P(2.8, -1.6, 0); stems = [(0, 0, 3.4), (0.35, 0.3, 2.9), (-0.3, 0.25, 2.4), (0.25, -0.35, 3.7), (-0.4, -0.2, 1.6)]
    trunk = flat('#6a8a3a', 0.85, (0.9, 1.15, 1.1)); brown = flat('#8a6a3a')
    for (dx, dy, h) in stems:
        b = bc + Vector((dx, dy, 0)); pm.frustum(tuple(b), tuple(b + Vector((0.05, 0.03, h))), 0.14 * h / 3.4 + 0.04, 0.08, trunk, seg=10)
        F(pm, [b + Vector((0.13, -0.05, 0.2)), b + Vector((0.15, 0.05, 0.2)), b + Vector((0.1, 0.06, h * 0.6)), b + Vector((0.09, -0.04, h * 0.6))], brown, None, (1, 0, 0))
        for k in range(4 if h > 2 else 2):
            az = r.uniform(0, 6.28) if k else math.atan2(-0.62, 0.9); L = r.uniform(1.6, 2.3); el = r.uniform(0.3, 0.9); droop = r.uniform(0.5, 1.2)
            top = b + Vector((0.05, 0.03, h)); d = Vector((math.cos(az), math.sin(az), 0)); side = Vector((-d.y, d.x, 0)); n = 8; wdt = 0.32
            ring = []
            for i in range(n + 1):
                t = i / n; c = top + d * L * t + Vector((0, 0, L * (el * t - droop * t * t)))
                ring.append((c - side * wdt * (0.2 + math.sin(math.pi * min(t * 1.1, 1)) * 0.8) - Vector((0, 0, 0.06 * t)), c + side * wdt * (0.2 + math.sin(math.pi * min(t * 1.1, 1)) * 0.8) - Vector((0, 0, 0.06 * t))))
            lf = (k + int(h * 10)) % 2
            for i in range(n):
                v0, v1 = 0.03 + 0.94 * i / n, 0.03 + 0.94 * (i + 1) / n; u0, u1 = lf * 0.5 + 0.01, lf * 0.5 + 0.49
                F(mba, [ring[i][0], ring[i][1], ring[i + 1][1], ring[i + 1][0]], M['banana'], [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])
    # the bunch, hanging from the tallest stem toward the soi
    top = bc + Vector((0.3, -0.32, 3.7)); stalk = [top, top + Vector((0.35, -0.1, 0.1)), top + Vector((0.6, -0.15, -0.3)), top + Vector((0.65, -0.15, -0.9)), top + Vector((0.65, -0.15, -1.5))]
    tube(pm, smooth(stalk, 4), 0.035, flat('#5a7a2a'), 6); grn = flat('#6aa83a', 0.85, (0.9, 1.15, 1.1)); ax = top + Vector((0.65, -0.15, 0))
    for hnd in range(6):
        z = -0.4 - hnd * 0.15
        for f in range(9):
            a = f * 2 * math.pi / 9 + hnd * 0.3; c = ax + Vector((0, 0, z)); d = Vector((math.cos(a), math.sin(a), 0))
            tube(pm, [c + d * 0.05, c + d * 0.13 + Vector((0, 0, 0.03)), c + d * 0.17 + Vector((0, 0, 0.12))], 0.022, grn, 5)
    pm.frustum(tuple(ax + Vector((0, 0, -1.45))), tuple(ax + Vector((0, 0, -1.85))), 0.09, 0.0, flat('#7a2a4a', 0.8, (0.9, 1.05, 1.25)), seg=10)
    return dict(banana=tuple(round(v, 3) for v in ax + Vector((0, 0, -0.8))), spirit_house=tuple(round(v, 3) for v in sp))

# ----------------------------------------------------------------------------- the right side near the camera: old wooden house with a noodle stall, cross soi
def wooden_house(G, r):
    fr = Fr('R'); mb, pm, mba = G['row'], G['props'], G['alpha']; a0, a1 = -7.0, 1.0; sb = 1.6   # set back
    fr.hquad(mb, a0, a1, -sb, 0, 0.0, M['tile_grey'], True, (0, 0, 8 / 1.5, sb / 1.5))
    fr.quad(mb, a0, a1, 0, 2.9, -sb, M['planks'], (0, 0, 8 / 2, 1.45)); fr.quad(mb, a0, a1, 2.9, 4.6, -sb + 0.25, M['planks'], (0, 0, 8 / 2, 0.85))
    fr.hquad(mb, a0, a1, -sb, -sb + 0.25, 2.9, M['planks'], False)
    for k in range(3): window(mb, mba, fr, a0 + 0.8 + k * 2.6, a0 + 2.0 + k * 2.6, 3.2, 4.2, f'win{k + 2}', None, False)
    for k in range(3):
        for s_ in (-1, 1): aa = a0 + 1.4 + k * 2.6 + s_ * 0.95; fr.box(mb, aa - 0.32, aa + 0.32, -sb + 0.25, -sb + 0.3, 3.15, 4.25, flat('#3a6a5a'))
    fr.box(mb, a0 - 0.3, a1 + 0.3, -sb - 0.4, -sb + 1.0, 4.6, 4.7, M['tin'], tile=(2, 2))
    F(mb, [fr.P(a0 - 0.3, -sb + 0.9, 4.7), fr.P(a1 + 0.3, -sb + 0.9, 4.7), fr.P(a1 + 0.3, -sb - 3.5, 7.0), fr.P(a0 - 0.3, -sb - 3.5, 7.0)], M['tin'], [(0, 0), (4, 0), (4, 2.5), (0, 2.5)], (0, 0, 1))
    F(mb, [fr.P(a0 - 0.3, -sb - 3.5, 7.0), fr.P(a1 + 0.3, -sb - 3.5, 7.0), fr.P(a1 + 0.3, -sb - 8, 4.7), fr.P(a0 - 0.3, -sb - 8, 4.7)], M['tin'], [(0, 0), (4, 0), (4, 2.5), (0, 2.5)], (0, 0, 1))
    for aa in (a0, a1): F(mb, [fr.P(aa, -sb + 0.25, 4.6), fr.P(aa, -sb - 8, 4.6), fr.P(aa, -sb - 3.5, 6.95)], M['planks'], [(0, 0), (4, 0), (2, 1)], fr.na * (1 if aa == a1 else -1))
    for aa in (a0, a1): fr.box(mb, aa - 0.1, aa, -sb - 8, -sb + 0.25, 0, 4.6, M['planks'], tile=(2, 4))
    fr.box(mb, a0 - 0.05, a1 + 0.05, -sb - 0.05, -sb + 0.3, 2.85, 2.95, flat('#5a3a20'))
    # tin awning over the front yard, posts, noodle cart, tables, stools, sign
    F(mb, [fr.P(a0 + 0.3, -sb, 2.85), fr.P(a1 - 0.3, -sb, 2.85), fr.P(a1 - 0.3, 1.7, 2.45), fr.P(a0 + 0.3, -sb + 0.0, 2.85)], M['tin_blue'], None, (0, 0, 1))
    F(mb, [fr.P(a0 + 0.3, -sb, 2.85), fr.P(a1 - 0.3, -sb, 2.85), fr.P(a1 - 0.3, 1.7, 2.45), fr.P(a0 + 0.3, 1.7, 2.45)], M['tin_blue'], [(0, 0), (4, 0), (4, 1.6), (0, 1.6)], (0, 0, 1))
    F(mb, [fr.P(a0 + 0.3, -sb, 2.84), fr.P(a1 - 0.3, -sb, 2.84), fr.P(a1 - 0.3, 1.7, 2.44), fr.P(a0 + 0.3, 1.7, 2.44)], M['tin_blue'], [(0, 0), (4, 0), (4, 1.6), (0, 1.6)], (0, 0, -1))
    for aa in (a0 + 0.4, (a0 + a1) / 2, a1 - 0.4): fr.cyl(mb, aa, 1.6, 0, 2.47, 0.04, flat('#8a8e90'), 6)
    fr.box(mb, a0 + 1.2, a1 - 1.6, 1.62, 1.68, 2.0, 2.44, flat('#3a3634')); fr.quad(mb, a0 + 1.25, a1 - 1.65, 2.02, 2.42, 1.685, M['signs'], atlas_row(0))
    nc = (a1 - 1.6, 0.6); fr.box(pm, nc[0] - 0.75, nc[0] + 0.75, nc[1] - 0.4, nc[1] + 0.4, 0, 0.9, flat('#b8bcc0')); fr.box(pm, nc[0] - 0.72, nc[0] + 0.72, nc[1] - 0.38, nc[1] + 0.38, 0.9, 1.4, M['glass'])
    fr.box(pm, nc[0] - 0.75, nc[0] + 0.75, nc[1] - 0.4, nc[1] + 0.4, 1.4, 1.44, flat('#c8302a'))
    if P.get('practicals'):                                              # bare bulb over the noodle cart, a tube under the awning
        bp = fr.P(nc[0], 0.9, 2.2); pm.sphere(tuple(bp), 0.05, M['bulb'], 10, 6); tube(pm, [bp + Vector((0, 0, 0.04)), fr.P(nc[0], 0.9, 2.55)], 0.004, flat('#1a1a1a'), 4)
        PR.append(('stall', tuple(bp - Vector((0, 0, 0.07))), None))
        fr.box(pm, a0 + 1.2, a0 + 2.4, 0.8, 0.86, 2.62, 2.66, M['tube']); PR.append(('stall_tube', tuple(fr.P(a0 + 1.8, 0.83, 2.6)), tuple(fr.na)))
    for k in range(2): fr.cyl(pm, nc[0] - 0.4 + k * 0.6, nc[1], 1.44, 1.75, 0.2, flat('#c8ccd0'), 14)
    for k in range(3):
        tb = (a0 + 1.0 + k * 1.6, -0.6); fr.box(pm, tb[0] - 0.5, tb[0] + 0.5, tb[1] - 0.35, tb[1] + 0.35, 0.72, 0.75, flat('#e8e4d8'))
        for (dx, dd) in ((-0.45, -0.3), (0.45, -0.3), (-0.45, 0.3), (0.45, 0.3)): fr.box(pm, tb[0] + dx - 0.02, tb[0] + dx + 0.02, tb[1] + dd - 0.02, tb[1] + dd + 0.02, 0, 0.72, flat('#8a8e90'))
        fr.box(pm, tb[0] - 0.3, tb[0] - 0.05, tb[1] - 0.1, tb[1] + 0.1, 0.75, 0.82, flat('#c8302a')); fr.cyl(pm, tb[0] + 0.25, tb[1], 0.75, 0.9, 0.04, flat('#e8d8a0'), 6)
        for s_ in (-1, 1): stool(pm, tuple(fr.P(tb[0] + s_ * 0.35, tb[1] + 0.7 * s_, 0)), r.choice(['#d8302a', '#2a5ad0', '#f0c030', '#2a9a5a']))
    for k in range(4): pot_plant(pm, tuple(fr.P(a0 + 0.3 + k * 0.25, 1.4, 0)), 0.15, 0.3, 1.0, r.choice(['#a85a3a', '#3a6ab0', '#e8e4d8']), mb_alpha=mba)
    fr.box(pm, a0 + 0.1, a0 + 0.7, 1.0, 1.6, 0, 0.6, M['crate']); fr.box(pm, a0 + 0.12, a0 + 0.68, 1.02, 1.58, 0.6, 1.2, M['crate'])
    # cross soi (y -6..-1 on the right): concrete lane into the block, low houses, a tree
    mb.quad((XR - 0.1, -6.0, 0.0), (26, 0, 0), (0, 5.0, 0), M['road_a'], uv=(0, 0, 26 / 4.5 * 0.0 + 1.0, 5 / 18.0))
    for k, x0 in enumerate((XR + 6, XR + 13)):
        for (y0, y1) in ((-13, -6.2), (-0.8, 6.0)):
            mb.box((x0, y0, 0), (x0 + 6, y1, 4.2 + k * 1.5), M[f'fac{(k * 3 + int(y0)) % 8}'], tile=(4, 11.2))
    for (tx, ty) in ((XR + 9, -3.5), (XR + 19, -3.0)):
        pm.frustum((tx, ty, 0), (tx, ty, 3.0), 0.18, 0.12, flat('#5a3a24'), seg=8)
        for k in range(5): pm.sphere((tx + r.uniform(-1, 1), ty + r.uniform(-1, 1), 3.6 + r.uniform(0, 1.2)), r.uniform(1.0, 1.5), flat('#4a8a3a', 0.85, (0.9, 1.15, 1.1)), 12, 8)

# ----------------------------------------------------------------------------- ground
def ground(G, r):
    mb = G['ground']
    y = -18.0; k = 0
    while y < 58:
        mb.quad((-2.25, y, 0), (4.5, 0, 0), (0, 18, 0), M['road_a' if k % 2 == 0 else 'road_b'], uv=(0, 0, 1, 1)); y += 18; k += 1
    for sx in (-1, 1):
        xg0, xg1 = sorted((sx * 2.25, sx * 2.6)); xc0, xc1 = sorted((sx * 2.6, sx * 2.75))
        mb.quad((xg0, -18, 0.0), (xg1 - xg0, 0, 0), (0, 76, 0), M['gutter'], uv=(0, 0, 1, 76 / 2.0)) if False else None
        yy = -18.0
        while yy < 58:
            if r.random() < 0.07:                                         # a missing cover: dark drain below
                mb.box((xg0, yy, -0.35), (xg1, yy + 0.5, -0.3), flat('#1a1c18')); mb.box((xg0 - 0.02, yy, -0.35), (xg0, yy + 0.5, 0), M['concrete_dark']); mb.box((xg1, yy, -0.35), (xg1 + 0.02, yy + 0.5, 0), M['concrete_dark'])
            else: mb.quad((xg0, yy, 0.0), (xg1 - xg0, 0, 0), (0, 0.5, 0), M['gutter'], uv=(0, 0, 0.25, 1))
            yy += 0.5
        mb.box((xc0, -18, 0), (xc1, 58, 0.05), M['curb'], tile=(2.0, 2.0)) if False else None
        for yy in range(-18, 58, 2): mb.quad((xc0, yy, 0.05), (xc1 - xc0, 0, 0), (0, 2, 0), M['curb'], uv=(0, 0, 1, 1)); mb.quad((xc0 if sx > 0 else xc1, yy, 0), (0, 2, 0), (0, 0, 0.05), M['curb'], uv=(0, 0, 1, 0.3)) if sx < 0 else mb.quad((xc0, yy + 2, 0), (0, -2, 0), (0, 0, 0.05), M['curb'], uv=(0, 0, 1, 0.3))
    # aprons per bay
    for (side, x0, x1) in (('L', XL, -2.75), ('R', 2.75, XR)):
        y = -18.0
        while y < 58:
            y1 = y + 4.0; tex = 'hero_floor' if side == 'L' and HERO[0] <= y < HERO[1] else r.choice(['tile_red', 'tile_grey', 'tile_white', 'tile_grey'])
            ts = 4.0 if tex == 'hero_floor' else 1.5
            mb.quad((x0, y, 0.0), (x1 - x0, 0, 0), (0, 4.0, 0), M[tex], uv=(x0 / ts, y / ts, x1 / ts, y1 / ts)); y = y1
    mb.quad((-30, 56, -0.01), (60, 0, 0), (0, 30, 0), M['road_a'], uv=(0, 0, 60 / 4.5, 30 / 18))
    mb.quad((-60, -60, -0.02), (120, 0, 0), (0, 160, 0), flat('#6a6458'))
    mh = MB(); mh.frustum((0.7, 15.0, 0.0), (0.7, 15.0, 0.012), 0.38, 0.38, M['manhole'], seg=20); mh.obj('soi_manhole', G['coll'])
    me = bpy.data.objects['soi_manhole'].data                             # planar UVs for the cap
    uvl = me.uv_layers[0]
    for poly in me.polygons:
        for li in poly.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co; uvl.data[li].uv = (0.5 + (v.x - 0.7) / 0.8, 0.5 + (v.y - 15.0) / 0.8)

# ----------------------------------------------------------------------------- poles, transformer, cables
POLES = [('L', -3.0, 12.25, 11.0), ('L', -3.0, 29.0, 10.5), ('L', -3.0, 51.0, 10.5), ('R', 3.05, -12.0, 10.5), ('R', 3.0, 17.5, 10.5), ('R', 3.0, 40.0, 10.5)]
def poles(G, r):
    mb, cb = G['poles'], G['cables']; blk = flat('#141416', 0.7); grey = flat('#8a8e90'); por = flat('#e8e4dc')
    for (side, x, y, h) in POLES:
        sq_prism(mb, x, y, 0, h, 0.17, 0.11, M['pole'])
        for z, w in ((h - 1.2, 1.9), (h - 0.55, 1.6)):
            mb.box((x - w / 2, y - 0.05, z - 0.05), (x + w / 2, y + 0.05, z + 0.05), grey)
            for k in (-1, 0, 1): mb.frustum((x + k * w * 0.42, y, z + 0.05), (x + k * w * 0.42, y, z + 0.22), 0.04, 0.03, por, seg=8)
        mb.box((x - 0.18, y - 0.18, 6.2), (x + 0.18, y + 0.18, 6.32), grey)          # cable rack
        for k in range(r.randint(2, 4)):                                   # grey boxes and splice tubes on the pole
            zz = r.uniform(2.6, 5.5); s = r.uniform(0.18, 0.32); sd = r.choice((-1, 1))
            mb.box((x - s / 2, y + sd * 0.12, zz), (x + s / 2, y + sd * (0.12 + s * 0.6), zz + s * 1.3), flat(r.choice(['#b8bcc0', '#d8d8d0', '#7a8a8a'])))
        for k in range(2): mb.frustum((x + 0.15, y - 0.3 + k * 0.6, 5.6 + k * 0.4), (x + 0.15, y - 0.3 + k * 0.6, 6.2 + k * 0.4), 0.06, 0.06, blk, seg=8)
        for k in range(6):                                                   # cables spiralling down the pole
            zz0 = r.uniform(3.0, 6.0); pts = [Vector((x + 0.15 * math.cos(t * 0.8 + k), y + 0.15 * math.sin(t * 0.8 + k), zz0 + t * 0.12)) for t in range(int((6.3 - zz0) / 0.12))]
            if len(pts) > 2: tube(cb, pts, 0.012, blk, 4)
    # spans: HV wires and the spaghetti of comm cables along each side, plus crossings
    byside = {s: sorted([p for p in POLES if p[0] == s], key=lambda p: p[2]) for s in 'LR'}
    for s, pl in byside.items():
        pl = [(s, pl[0][1], -24.0, 0)] + pl + [(s, pl[-1][1], 64.0, 0)]
        for (_, x0, y0, _), (_, x1, y1, _) in zip(pl[:-1], pl[1:]):
            for k in (-1, 0, 1): tube(cb, catenary((x0 + k * 0.8, y0, 10.0), (x1 + k * 0.8, y1, 10.0), 0.35, 20), 0.008, blk, 4)
            n = 26 if (s == 'L' and (abs(y0 - 12.25) < 0.1 or abs(y1 - 12.25) < 0.1)) else 16
            for k in range(n):
                dx0, dz0 = r.uniform(-0.25, 0.3), r.uniform(-0.4, 0.45); dx1, dz1 = r.uniform(-0.25, 0.3), r.uniform(-0.4, 0.45)
                tube(cb, catenary((x0 + dx0, y0, 6.6 + dz0), (x1 + dx1, y1, 6.6 + dz1), r.uniform(0.25, 0.7), 22), r.choice([0.008, 0.01, 0.013, 0.018]), blk, 4)
    for (ya, yb) in ((12.25, 17.5), (29.0, 17.5), (29.0, 40.0), (51.0, 40.0)):
        for k in range(r.randint(3, 7)): tube(cb, catenary((-3.05, ya, 6.0 + r.uniform(-0.4, 0.6)), (3.0, yb, 6.0 + r.uniform(-0.4, 0.6)), r.uniform(0.3, 0.9), 22), r.choice([0.008, 0.012]), blk, 4)
    # drop cables from the spans to each facade (meters)
    for side in 'LR':
        xs = XL if side == 'L' else XR; xp = -3.0 if side == 'L' else 3.0
        for y in range(-12, 56, 4):
            for k in range(r.randint(1, 3)):
                p0 = (xp + r.uniform(-0.2, 0.2), y + r.uniform(-1.5, 1.5), 6.5 + r.uniform(-0.2, 0.3)); p1 = (xs + (0.15 if side == 'L' else -0.15), y + r.uniform(0.5, 3.5), r.uniform(6.2, 8.5))
                tube(cb, catenary(p0, p1, r.uniform(0.1, 0.4), 10), 0.008, blk, 4)
    # the hero pole tangle: loops, coils, hanging slack, bundles
    x, y = -3.0, 12.25
    for k in range(9):
        c = Vector((x + r.uniform(-0.2, 0.35), y + r.uniform(-0.6, 0.6), r.uniform(4.6, 6.0))); rr = r.uniform(0.18, 0.45); tilt = r.uniform(-0.6, 0.6)
        tube(cb, [c + Vector((math.cos(t) * rr * math.sin(tilt), math.cos(t) * rr * math.cos(tilt), math.sin(t) * rr)) for t in [i * math.pi / 12 for i in range(25)]], r.choice([0.01, 0.014]), blk, 4)
    for k in range(10):
        a = Vector((x + r.uniform(-0.1, 0.2), y + r.uniform(-1.6, 1.6), 6.2 + r.uniform(-0.3, 0.3))); b = a + Vector((r.uniform(-0.3, 0.6), r.uniform(-0.5, 0.5), 0)); m = (a + b) / 2 + Vector((0, 0, -r.uniform(0.8, 2.2)))
        tube(cb, smooth([a, m, b], 6), 0.01, blk, 4)
    for k in range(4): mb.box((x + 0.12, y - 0.9 + k * 0.5, 6.0 - k * 0.15), (x + 0.32, y - 0.7 + k * 0.5, 6.25 - k * 0.15), flat('#2a2a2e'))
    # transformer on the hero pole (road side)
    tx, ty, tz = x + 0.52, y, 7.45; tk = flat('#7e8a86', 0.85)
    mb.box((x + 0.1, y - 0.45, tz - 0.62), (x + 0.95, y + 0.45, tz - 0.55), grey)
    mb.frustum((tx, ty, tz - 0.55), (tx, ty, tz + 0.4), 0.36, 0.36, M['transformer'], seg=20)
    me_uv_cyl = None
    for k in range(16):
        a = k * 2 * math.pi / 16; d = Vector((math.cos(a), math.sin(a), 0)); c = Vector((tx, ty, tz - 0.1))
        if abs(math.cos(a)) > 0.9 and math.cos(a) > 0: continue
        mb.box(tuple(c + d * 0.36 + Vector((-0.012, -0.012, -0.4))), tuple(c + d * 0.36 + Vector((0.012, 0.012, 0.4))), tk) if False else rect(mb, c + d * 0.44, d * 0.08, Vector((0, 0, 0.38)), tk, n=d.cross(Vector((0, 0, 1))))
    mb.frustum((tx, ty, tz + 0.4), (tx, ty, tz + 0.5), 0.38, 0.3, tk, seg=20)
    for k in (-1, 0, 1):
        for j in range(4): mb.frustum((tx + k * 0.17, ty, tz + 0.5 + j * 0.06), (tx + k * 0.17, ty, tz + 0.53 + j * 0.06), 0.05, 0.04, flat('#8a4a2a'), seg=8)
        tube(cb, [Vector((tx + k * 0.17, ty, tz + 0.75)), Vector((x + k * 0.6, y + 0.15, 9.2)), Vector((x + k * 0.75, y, 10.0))], 0.008, blk, 4)
        mb.box((x + k * 0.6 - 0.03, y + 0.1, 9.0), (x + k * 0.6 + 0.03, y + 0.18, 9.3), por)
    for k in range(4): tube(cb, smooth([Vector((tx + 0.37, ty - 0.15 + k * 0.1, tz + 0.1)), Vector((tx + 0.5, ty - 0.2 + k * 0.12, tz - 0.4)), Vector((x + 0.2, y - 0.4 + k * 0.25, 6.4))], 5), 0.016, blk, 5)
    # street lamp arm (toward the road) and the soi number sign facing the camera end
    tube(mb, [Vector((x + 0.1, y, 8.4)), Vector((x + 1.0, y, 8.75)), Vector((x + 1.8, y, 8.8))], 0.035, grey, 6)
    mb.box((x + 1.6, y - 0.13, 8.66), (x + 2.15, y + 0.13, 8.82), grey); mb.box((x + 1.65, y - 0.1, 8.62), (x + 2.1, y + 0.1, 8.66), M['lamp'])
    if P.get('practicals'):
        PR.append(('lamp', (x + 1.88, y, 8.58), 'lamp'))
        for (px, py, sx, kind) in ((3.0, 17.5, -1, 'led'), (-3.0, 29.0, 1, 'lamp'), (3.0, 40.0, -1, 'lamp'), (-3.0, 51.0, 1, 'led')):     # the soi's other street lamps
            tube(mb, [Vector((px + sx * 0.1, py, 8.0)), Vector((px + sx * 1.0, py, 8.35)), Vector((px + sx * 1.6, py, 8.4))], 0.03, grey, 6)
            mb.box((px + sx * 1.45 - 0.25, py - 0.12, 8.28), (px + sx * 1.45 + 0.25, py + 0.12, 8.42), grey)
            mb.box((px + sx * 1.45 - 0.21, py - 0.09, 8.25), (px + sx * 1.45 + 0.21, py + 0.09, 8.28), M['lamp'] if kind == 'lamp' else M['led_warm'])
            PR.append(('lamp', (px + sx * 1.45, py, 8.2), kind))
    sg = MB(); sg.quad((x - 0.26, y - 0.2, 2.75), (0.52, 0, 0), (0, 0, 0.26), M['soi_sign']); sg.box((x - 0.27, y - 0.19, 2.74), (x + 0.27, y - 0.17, 3.02), flat('#d8d8d0'))
    for so in sg.v: pass
    sgo = sg.obj('soi_sign', G['coll'])
    return dict(transformer=(round(tx, 3), round(ty, 3), round(tz, 3)), pole=(x, y, 0.0), lamp=(round(x + 1.9, 3), y, 8.62))

# ----------------------------------------------------------------------------- motorbike
def motorbike(G, loc, yaw, lean=0.06):
    b = MB(); red = M['bike']; blk = flat('#1a1a1c', 0.8); chrome = flat('#c8ccd0', 0.9); grey = flat('#6a6e72')
    def wheel(xw):
        b.frustum((xw, -0.04, 0.28), (xw, 0.04, 0.28), 0.28, 0.28, blk, seg=20); b.frustum((xw, -0.045, 0.28), (xw, 0.045, 0.28), 0.17, 0.17, chrome, seg=16)
        b.frustum((xw, -0.06, 0.28), (xw, 0.06, 0.28), 0.04, 0.04, grey, seg=8)
    wheel(0.62); wheel(-0.6)
    tube(b, [(0.62, 0.06, 0.28), (0.52, 0.06, 0.75), (0.45, 0.06, 0.95)], 0.025, chrome, 6); tube(b, [(0.62, -0.06, 0.28), (0.52, -0.06, 0.75), (0.45, -0.06, 0.95)], 0.025, chrome, 6)
    b.box((0.45, -0.1, 0.48), (0.78, 0.1, 0.56), red)                                # front fender (simplified)
    b.box((0.34, -0.2, 0.55), (0.48, 0.2, 1.0), red); b.box((0.3, -0.14, 0.2), (0.4, 0.14, 0.55), red)   # leg shield
    b.box((0.38, -0.16, 0.95), (0.56, 0.16, 1.1), red); b.box((0.52, -0.1, 0.96), (0.6, 0.1, 1.06), flat('#f4f0d8')) ; b.box((0.6, -0.08, 0.98), (0.61, 0.08, 1.04), M['lamp'])   # headlight cowl
    tube(b, [(0.44, -0.38, 1.12), (0.46, 0, 1.1), (0.44, 0.38, 1.12)], 0.016, chrome, 6)
    for s in (-1, 1): b.box((0.4, s * 0.36 - 0.03, 1.1), (0.48, s * 0.36 + 0.03, 1.14), blk); tube(b, [(0.44, s * 0.3, 1.12), (0.42, s * 0.32, 1.4)], 0.008, chrome, 4); b.box((0.39, s * 0.32 - 0.07, 1.4), (0.43, s * 0.32 + 0.07, 1.48), blk)
    b.box((-0.15, -0.16, 0.25), (0.32, 0.16, 0.33), blk)                              # floor step
    b.box((-0.75, -0.17, 0.42), (0.05, 0.17, 0.72), red); b.box((-0.7, -0.15, 0.72), (0.05, 0.15, 0.8), blk)  # body + seat
    b.box((-0.85, -0.12, 0.62), (-0.7, 0.12, 0.74), flat('#c8281e')); b.box((-0.86, -0.08, 0.64), (-0.85, 0.08, 0.7), emit('tail', '#ff3020', 1.0) if P['tubes'] > 0 else flat('#c82a20'))
    b.box((-0.88, -0.13, 0.42), (-0.86, 0.13, 0.6), flat('#f4f0e8'))                  # licence plate
    tube(b, [(-0.2, 0.17, 0.32), (-0.55, 0.2, 0.36), (-0.9, 0.2, 0.42)], 0.045, chrome, 10)  # muffler
    b.box((-0.6, -0.12, 0.3), (-0.1, 0.12, 0.45), grey)                               # engine
    tube(b, [(-0.7, -0.17, 0.8), (-0.82, -0.17, 0.82), (-0.82, 0.17, 0.82), (-0.7, 0.17, 0.8)], 0.012, chrome, 5)   # grab rail
    b.sphere((-0.3, 0.0, 0.93), 0.15, flat('#f0c020', 0.8), 14, 7); b.box((-0.2, -0.1, 0.9), (-0.14, 0.1, 0.98), flat('#2a3a4a'))   # helmet on the seat
    tube(b, [(-0.12, 0.17, 0.33), (-0.08, 0.32, 0.0)], 0.012, grey, 4)                # kickstand
    ob = b.obj('soi_bike', G['coll']); ob.location = loc; ob.rotation_euler = (lean, 0, yaw); S.no_bounce(ob)
    return ob

# ----------------------------------------------------------------------------- far end: 7-storey block with a billboard truss, distant skyline
def far_end(G, r):
    mb, cb = G['far'], G['cables']; x0, x1, y0, y1, h = -9.0, 11.0, 58.0, 72.0, 24.5
    mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, 0, h), M['tower']); mb.box((x0, y0 + 0.01, 0), (x1, y1, h), M['concrete'], tile=(4, 4), skip='front')
    mb.box((x0 - 0.1, y0 - 0.1, h), (x1 + 0.1, y1 + 0.1, h + 1.0), flat('#9a968c'))
    for f in range(1, 7): mb.box((x0, y0 - 0.9, 3.5 * f - 0.05), (x1, y0, 3.5 * f + 0.1), M['concrete']) if f % 2 == 0 else None
    mb.box((x0 + 2, y0 + 3, h), (x0 + 6, y0 + 7, h + 3.2), M['concrete']); mb.frustum((x1 - 3, y0 + 9, h), (x1 - 3, y0 + 9, h + 2.5), 1.2, 1.2, flat('#3a72b0'), seg=14)
    # billboard truss (lattice) + panel facing the soi + catwalk
    bx0, bx1, by, bz0, bz1 = -6.0, 8.0, y0 + 4.0, h + 3.2, h + 9.0; stl = flat('#3a3c40', 0.8)
    for xx in (bx0 + 0.5, (bx0 + bx1) / 2, bx1 - 0.5):
        for yy in (by, by + 3.0): tube(mb, [(xx, yy, h + 1.0), (xx, yy, bz0 + 0.2)], 0.08, stl, 6)
        for k in range(4): z0_ = h + 1.0 + k * 0.55; tube(mb, [(xx, by, z0_), (xx, by + 3, z0_ + 0.55)], 0.03, stl, 4); tube(mb, [(xx, by + 3, z0_), (xx, by, z0_ + 0.55)], 0.03, stl, 4)
    for zz in (bz0, h + 2.0): tube(mb, [(bx0, by, zz), (bx1, by, zz)], 0.06, stl, 4); tube(mb, [(bx0, by + 3, zz), (bx1, by + 3, zz)], 0.06, stl, 4)
    for k in range(15): xx = bx0 + k * (bx1 - bx0) / 14; tube(mb, [(xx, by + 0.3, bz0), (xx, by + 0.3, bz1)], 0.04, stl, 4)
    for k in range(14):
        xa = bx0 + k * (bx1 - bx0) / 14; xb = xa + (bx1 - bx0) / 14; tube(mb, [(xa, by + 0.35, bz0), (xb, by + 0.35, bz1)], 0.025, stl, 4)
    for zz in (bz0, (bz0 + bz1) / 2, bz1): tube(mb, [(bx0, by + 0.3, zz), (bx1, by + 0.3, zz)], 0.05, stl, 4)
    mb.quad((bx0, by - 0.02, bz0 + 0.1), (bx1 - bx0, 0, 0), (0, 0, bz1 - bz0 - 0.1), M['billboard'])
    mb.box((bx0, by - 1.2, bz0 - 0.08), (bx1, by - 0.05, bz0), stl)
    for k in range(29): xx = bx0 + k * (bx1 - bx0) / 28; tube(mb, [(xx, by - 1.15, bz0), (xx, by - 1.15, bz0 + 1.0)], 0.015, stl, 4)
    tube(mb, [(bx0, by - 1.15, bz0 + 1.0), (bx1, by - 1.15, bz0 + 1.0)], 0.025, stl, 4)
    for k in range(5): xx = bx0 + 1 + k * 3; tube(mb, [(xx, by - 1.0, bz0 - 0.05), (xx + 0.3, by - 1.6, bz0 + 0.4)], 0.03, stl, 4)    # flood-lamp arms
    if P.get('practicals'):
        for k in range(5): xx = bx0 + 1 + k * 3; mb.box((xx + 0.15, by - 1.75, bz0 + 0.35), (xx + 0.45, by - 1.6, bz0 + 0.5), M['led_warm'])
    tube(mb, [(x1 - 1.0, y0 + 0.4, h + 1.0), (x1 - 1.0, y0 + 0.4, bz0)], 0.03, stl, 4)
    for k in range(int((bz0 - h - 1) / 0.35)): zz = h + 1 + k * 0.35; tube(mb, [(x1 - 1.25, y0 + 0.4, zz), (x1 - 0.75, y0 + 0.4, zz)], 0.015, stl, 4)  # ladder
    # distant skyline: blocks, a wat roof, water towers
    for k in range(18):
        sx = r.choice([-1, 1]); xx = sx * r.uniform(9, 40); yy = r.uniform(62, 110); w = r.uniform(5, 14); hh = r.uniform(10, 34)
        mb.box((xx - w / 2, yy, 0), (xx + w / 2, yy + w, hh), M[r.choice(['concrete', 'concrete_dark', 'fac6', 'fac1'])], tile=(6, 6))
        if r.random() < 0.4: mb.frustum((xx, yy + w / 2, hh), (xx, yy + w / 2, hh + 2), 1.0, 1.0, flat('#5a6a8a'), seg=10)
    wx, wy = -24.0, 80.0; red = flat('#b8402a', 0.85, (0.9, 1.05, 1.25)); gold = flat('#e8b030', 0.9, (0.9, 1.05, 1.25))
    for t, (z0_, w, l) in enumerate(((10, 7, 14), (13, 5, 11), (15.5, 3.4, 8))):
        F(mb, [Vector((wx - w, wy - l / 2, z0_)), Vector((wx - w, wy + l / 2, z0_)), Vector((wx, wy + l / 2, z0_ + 4)), Vector((wx, wy - l / 2, z0_ + 4))], red, None, (-1, 0, 0.5))
        F(mb, [Vector((wx + w, wy - l / 2, z0_)), Vector((wx + w, wy + l / 2, z0_)), Vector((wx, wy + l / 2, z0_ + 4)), Vector((wx, wy - l / 2, z0_ + 4))], red, None, (1, 0, 0.5))
        F(mb, [Vector((wx - w, wy - l / 2, z0_)), Vector((wx + w, wy - l / 2, z0_)), Vector((wx, wy - l / 2, z0_ + 4))], gold, None, (0, -1, 0))
        tube(mb, [(wx, wy - l / 2, z0_ + 4), (wx + 0.3, wy - l / 2 - 0.4, z0_ + 5.2)], 0.15, gold, 6)
    mb.box((wx - 6, wy - 7, 0), (wx + 6, wy + 7, 10), flat('#f0e8d8'))
    return dict(tower_top=(1.0, round(by - 0.7, 3), h + 1.0), billboard=dict(x=(bx0, bx1), y=by, z=(bz0, bz1)), tower=dict(x=(x0, x1), y=(y0, y1), h=h))

# ----------------------------------------------------------------------------- sky
def world_sky(scene, key):
    w = bpy.data.worlds.new('soi_sky'); scene.world = w; w.use_nodes = True; nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld'); bg = nt.nodes.new('ShaderNodeBackground'); tc = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Rotation'].default_value = (0, 0, math.pi); env = nt.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(TX[key], check_existing=True)
    lp = nt.nodes.new('ShaderNodeLightPath'); L = nt.links.new
    L(tc.outputs['Generated'], mp.inputs['Vector']); L(mp.outputs['Vector'], env.inputs['Vector']); L(env.outputs['Color'], bg.inputs['Color'])
    L(lp.outputs['Is Camera Ray'], bg.inputs['Strength']); L(bg.outputs[0], out.inputs[0]); w.light_settings.distance = 0.001
    w.cycles.sampling_method = 'NONE'                                    # camera-only backdrop: never sampled as a light (it would steal samples from the sun)

# ----------------------------------------------------------------------------- build
UNITS_L = [(-14, -10), (-10, -6), (-6, -2), (-2, 1.6)] + [(y, y + 4) for y in range(12, 56, 4)]
UNITS_R = [(-14, -10), (-10, -6), (7, 11), (11, 15), (15, 19), (19, 23), (25, 29), (29, 33), (33, 37), (37, 41), (43, 47), (47, 51), (51, 55)]
GAPS_R = [(23, 25), (41, 43)]
def unit_cfg(r, side, y0):
    c = dict(wall=r.randrange(8), shut=r.choice(['down', 'down', 'half', 'up', 'up', 'grille']), shtex=r.choice(['shut_grey', 'shut_green', 'shut_blue', 'shut_rust', 'shut_grey']),
             canopy=r.choice(['slab', 'tin', 'tin_blue', 'slab']), f2=r.choice(['win', 'cage', 'open', 'win', 'cage']), f3=r.choice(['win', 'win_ac']),
             roof=r.choice(['tank', 'shack', 'antenna', None]), interior=r.randrange(4), grille=r.choice(['grille_sun', 'grille_dia', 'grille_tul']), laundry=True)
    c['sign'] = r.randrange(8) if c['shut'] in ('up', 'half') or r.random() < 0.3 else None
    if side == 'L' and y0 == 12: c.update(shut='down', shtex='shut_grey', sign=None, f2='open', wall=6)                          # gates lean on this one
    if side == 'R' and y0 == 11: c.update(f2='open', laundry=False, plants=False, sign=6, shut='up', interior=0)                                # camera balcony of high_soi
    if side == 'R' and y0 == 7: c.update(shut='half', sign=3, interior=3, f2='cage')
    if side == 'L' and y0 == 16: c.update(shut='up', sign=2, interior=0)
    if side == 'R' and y0 in (15, 29): c.update(top=7.6, f2='open')
    return c

def build(preset='afternoon_storm', clear=True):
    scene = bpy.context.scene
    if clear: bpy.ops.wm.read_factory_settings(use_empty=True); scene = bpy.context.scene
    P.clear(); P.update(PRESETS[preset]); S.STATE.clear(); S.STATE['P'] = P; M.clear(); A.clear(); PR.clear(); TL.reset()
    TX.clear(); TX.update(tex_soi.build_all())
    coll = S._coll('SET', scene); S._wipe(coll); lc = S._coll('LIGHTS', scene); S._wipe(lc)
    materials(); r = random.Random(20261113)
    G = dict(coll=coll, ground=MB(), row=MB(), hero=MB(), props=MB(), alpha=MB(), poles=MB(), cables=MB(), far=MB(), hero_in=MB())
    ground(G, r)
    for side, units in (('L', UNITS_L), ('R', UNITS_R)):
        fr = Fr(side)
        for (y0, y1) in units:
            a0, a1 = (y0, y1) if side == 'L' else (-y1, -y0)
            bay(G, fr, a0, a1, unit_cfg(r, side, y0), r)
        if side == 'R':
            for (g0, g1) in GAPS_R:                                       # narrow walkways between buildings: light shafts across the soi
                fr.side(G['row'], -g0, -12, 0, 0, FH, M['concrete_dark'], -1, (0, 0, 6, 5.6)); fr.side(G['row'], -g1, -12, 0, 0, FH, M['concrete_dark'], 1, (0, 0, 6, 5.6))
                fr.hquad(G['row'], -g1, -g0, -12, 0, 0.0, M['concrete'], True, (0, 0, 1, 6))
                for k in range(4): tube(G['props'], [fr.P(-g1 + 0.1 + k * 0.05, -12 + k, 0.4 + k * 1.5), fr.P(-g1 + 0.1 + k * 0.05, -0.2, 0.4 + k * 1.5)], 0.03, flat('#d8d2c4'), 6)
                pot_plant(G['props'], tuple(fr.P(-(g0 + g1) / 2, -0.5, 0)), 0.2, 0.35, 1.2, mb_alpha=G['alpha'])
    hero_shop(G, r); A.update(hero_front(G, r)); A.update(vacant_lot(G, r)); wooden_house(G, r)
    A.update(poles(G, r)); A.update(far_end(G, r))
    bk = motorbike(G, (-3.35, 15.3, 0.0), math.radians(97), 0.07); A['bike'] = (-3.35, 15.3, 0.0)
    if P['phones'] > 0:                                                   # night: a few phone screens glowing in the dark
        ph = MB()
        for (x, y, z) in ((-2.4, 7.9, 1.35), (2.9, 1.2, 1.2), (-0.6, 20.0, 1.4), (3.2, 25.0, 4.9), (-4.6, 31.0, 5.2)): rect(ph, (x, y, z), (0.04, 0, 0), (0, 0, 0.08), M['phone'], n=(0, -1, 0))
        ph.obj('soi_phones', coll)
    for nm in ('ground', 'row', 'hero', 'props', 'alpha', 'poles', 'cables', 'far', 'hero_in'):
        if G[nm].f: G[nm].obj('soi_' + nm, coll)
    for ob in coll.objects: S.no_bounce(ob)
    bpy.data.objects['soi_alpha'].visible_shadow = True
    sd = bpy.data.lights.new('key_sun', 'SUN'); kmax = max(P['key']); sd.energy = math.pi * kmax; sd.color = tuple(c / kmax for c in P['key']); sd.angle = math.radians(P['sun_angle'])
    sd.use_shadow = True; so = bpy.data.objects.new('key_sun', sd); lc.objects.link(so)
    so.rotation_euler = Vector(P['key_dir']).normalized().to_track_quat('-Z', 'Y').to_euler()
    if P.get('practicals'):
        A['practicals'] = practicals(lc)
        # light linking: the workshop interior is lit only by its own tube; every other light (and the moon) skips it, so the light tree
        # never spends interior samples on lamps that cannot reach it (that was the grain)
        out_c = bpy.data.collections.new('RX_outside')
        for ob in coll.objects:
            if ob.name != 'soi_hero_in': out_c.objects.link(ob)
        rx = dict(outside=out_c)
        for key, names in (('workshop', ('soi_hero_in', 'soi_ground', 'soi_props', 'soi_alpha')), ('hero', ('soi_hero',)), ('props', ('soi_props', 'soi_row')),
                           ('noground', [o.name for o in out_c.objects if o.name != 'soi_ground'])):
            c_ = rx[key] = bpy.data.collections.new('RX_' + key)
            for nm in names:
                if nm in bpy.data.objects: c_.objects.link(bpy.data.objects[nm])
        for ob in list(lc.objects): ob.light_linking.receiver_collection = rx[ob.get('rx', 'outside')]
    world_sky(scene, P['sky']); S.setup_render(scene, 'fast'); scene.cycles.samples = 12; scene.render.use_persistent_data = False; S.setup_grade(scene, bloom=True)
    if P.get('practicals'): scene.cycles.use_light_tree = True; A['lights_on'] = True
    A['key_dir'] = tuple(round(v, 4) for v in Vector(P['key_dir']).normalized()); A['preset'] = preset; A['cams'] = CAMS; A['cams_16x9'] = CAMS_16x9; A['units'] = 1.0
    A['soi'] = dict(road_x=(-2.25, 2.25), gutter_x=(2.25, 2.6), curb_x=(2.6, 2.75), facade_left_x=XL, facade_right_x=XR, hero_shop_y=HERO, far_end_y=58.0)
    return A

def pool_tex():
    """Soft elliptical light-pool mask (alpha) for the camera-only decals of the far shops' tube light."""
    path = os.path.join(tex_soi.TEX, 'pool_v1.png')
    if not os.path.exists(path):
        import numpy as np
        from PIL import Image
        y, x = np.mgrid[-1:1:256j, -1:1:256j]; r2 = x * x + y * y; a = np.clip(1 - r2, 0, 1) ** 1.8
        im = np.zeros((256, 256, 4), np.uint8); im[..., :3] = 255; im[..., 3] = (a * 255).astype(np.uint8); Image.fromarray(im, 'RGBA').save(path)
    return path

NEAR_Y = (-3.0, 21.0)          # shops in this stretch (around the hero shop) get real area lights; further ones a pool decal (noise budget)
def practicals(lc):
    """Real lights for the evening, from the positions collected while building (PR). Returns a list for the anchors.
    Noise budget at 12 samples: about 18 real lights; lightbox signs and most balcony bulbs are emission only, the shops far down the
    soi spill a camera-only pool decal instead of a light."""
    out = []; n = {}; dec = MB(); pm = TL.mat_additive('SOI_A_pool', P['shop']['color'], 0.3, image=pool_tex()); hero_balc = True
    for kind, pos, extra in PR:
        n[kind] = n.get(kind, 0) + 1; nm = f'{kind}_{n[kind]}'
        if kind in ('shop', 'stall_tube'):                                # every shop spills a pool decal on the apron (no shadow, no sampling noise)
            x = (-4.1 if pos[0] < 0 else 3.5) if kind == 'shop' else 3.2; rect(dec, (x, pos[1], 0.055), (1.5, 0, 0), (0, 1.7, 0), pm, n=(0, 0, 1))
            if not (NEAR_Y[0] <= pos[1] <= NEAR_Y[1]): out.append((nm + '_decal', (x, pos[1], 0.055))); continue
        if kind in ('shop', 'hero_tube', 'stall_tube'):                   # fluorescent tubes: small area lights facing down (cold pools out over the apron)
            c = P['shop']; K = c['K'] * (1.15 if kind == 'hero_tube' else 0.85 if kind == 'stall_tube' else 1.0)
            ob = TL.area(lc, nm, pos, (0, 0, -1), c['color'], K * (1.6 if kind == 'hero_tube' else 1.0), pos[2], size=6.6 if kind == 'hero_tube' else 1.2, size_y=0.06)
            ob['rx'] = 'workshop' if kind == 'hero_tube' else 'noground'
            ob.rotation_euler = (0, 0, math.pi / 2) if abs(extra[1]) > 0.5 else (0, 0, 0)
        elif kind == 'lamp':                                              # street lamps: spots straight down, sodium or LED
            c = P['lamp'] if extra == 'lamp' else P['led']; TL.spot(lc, nm, pos, (0, 0, -1), c['color'], c['K'], pos[2], 78 if n[kind] == 1 else 64, 0.3, 0.06)
        elif kind == 'sign_spot':                                         # gooseneck lamps washing the hero sign
            d = Vector(extra) - Vector(pos); ob = TL.spot(lc, nm, pos, tuple(d), '#ffe0a0', 1.15, d.length, 108, 0.55, 0.03); ob['rx'] = 'hero'
        elif kind == 'sign': continue                                     # lightbox: emission only
        elif kind == 'balcony':
            if pos[0] > XL + 0.4 or not (HERO[0] <= pos[1] <= HERO[1]): continue   # only the hero shop's balcony bulb is a real light
            TL.point(lc, nm, pos, P['bulb']['color'], 0.9, 1.6, radius=0.03)
        elif kind == 'stall': TL.point(lc, nm, pos, P['bulb']['color'], P['bulb']['K'], 2.1, radius=0.03)
        elif kind == 'spirit': ob = TL.point(lc, nm, pos, '#ff8a50', 0.5, 1.0, radius=0.05); ob['rx'] = 'props'
        out.append((nm, tuple(round(v, 3) for v in pos)))
    if dec.f: do = dec.obj('soi_pool_decals', bpy.data.collections['SET']); do.visible_shadow = False; S.no_bounce(do)
    return out

def set_lights(on=True):
    """Every practical light of the soi (shop tubes, street lamps, sign lamps, balcony / stall / spirit-house bulbs) and every emissive
    window, sign, LED strip and tube on (True) or off (False). Off = dark blue moonlight only (the ambient drops to amb_off).
    Only meaningful for the 'evening' preset (other presets have nothing registered). Returns the number of switched items."""
    n = TL.set_lights(on); A['lights_on'] = bool(on); return n

CAMS = dict(
    wide_soi=dict(loc=(1.35, -4.6, 2.2), look_at=(-1.6, 22.0, 6.6), lens=21),
    med_bench=dict(loc=(-0.5, 9.4, 1.6), look_at=(-4.3, 7.4, 2.3), lens=24),
    low_hong=dict(loc=(1.3, 7.7, 0.6), look_at=(-4.6, 5.3, 4.3), lens=18),
    high_soi=dict(loc=(3.2, 13.0, 5.3), look_at=(-3.9, 7.9, 0.8), lens=20),
    insert_bench=dict(loc=(-2.55, 8.75, 1.85), look_at=(-3.5, 8.1, 0.9), lens=30),
)

CAMS_16x9 = dict(wide_soi=dict(CAMS['wide_soi'], lens=18))      # landscape 1920x1080 (sensor fit AUTO: the 36 mm sensor spans the width)

def render_cam(name, path, res=(720, 1280), cam=None):
    scene = bpy.context.scene; scene.render.resolution_x, scene.render.resolution_y = res; scene.render.resolution_percentage = 100
    S.make_camera(cam or CAMS[name], name='cam'); return S.render(path)

if __name__ == '__main__':
    args = sys.argv[1:]; cmd = args[0] if args else 'stills'
    preset = args[1] if len(args) > 1 and args[1] in PRESETS else 'afternoon_storm'
    rest = [a for a in args[1:] if a not in PRESETS]; off = 'off' in rest
    q = 'preview' if 'preview' in rest else 'final'; cams = [a for a in rest if a in CAMS] or list(CAMS)
    os.makedirs(OUT, exist_ok=True); t0 = time.time(); build(preset); tb = time.time() - t0; scene = bpy.context.scene
    tag = '' if preset == 'afternoon_storm' else '_' + preset
    if off: set_lights(False); tag += '_off'
    times = {}
    if cmd == 'stills':
        if q == 'preview': scene.cycles.samples = 6
        for c in cams:
            res = (720, 1280) if q == 'final' else (360, 640)
            w, cpu = render_cam(c, os.path.join(OUT, f'{c}{tag}.png'), res); times[c] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(c, times[c], flush=True)
    elif cmd == 'land':
        w, cpu = render_cam('wide_soi', os.path.join(OUT, f'wide_soi_16x9{tag}.png'), (1920, 1080), CAMS_16x9['wide_soi']); times['wide_soi_16x9'] = dict(wall=round(w, 2), cpu=round(cpu, 2), load=os.getloadavg()[0]); print(times, flush=True)
    jp = os.path.join(OUT, 'timing.json'); old = json.load(open(jp)) if os.path.exists(jp) else {}
    old.update({f'{k}{tag}': dict(v, samples=scene.cycles.samples, quality=q, build_s=round(tb, 1)) for k, v in times.items()}); json.dump(old, open(jp, 'w'), indent=1)
    an = {k: v for k, v in A.items()}; json.dump(an, open(os.path.join(OUT, f'anchors{tag}.json'), 'w'), indent=1, default=str)
