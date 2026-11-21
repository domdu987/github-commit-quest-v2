#!/usr/bin/env python3
"""harbour_tex.py : artwork of the film-10 set (British naval dockyard 1917 + the open North Atlantic).
Everything is painted with numpy + PIL (supersampled, deterministic: fixed seeds) and cached in v3/set3d10/tex_harbour/ by a hash
of the painter's parameters + TEX_V (bump TEX_V after editing painter code). The painted skies reuse wall_tex.sky (film 9, same
sky-dome UV: u = azimuth / 360 from +x CCW, v = (elevation + 15) / 105); the noise helpers come from wall_tex too (imported).

Dazzle paint: every ship's paint lives in ship space (x along the ship, stern -L/2 .. bow +L/2; z up, waterline 0). A paint image
spans x -L/2..L/2 (u 0..1) and z ZP0..ZP1 (v 0..1) and is projected from the side onto hull, superstructure and funnels.
  dz_<id>_base   grey ship (stage 0): mid grey, red boot-topping below the waterline, black waterline, portholes, hawse pipe.
  dz_hero_l1     stage 1 layer (RGBA): bold black + white zigzag bands along the hull.
  dz_hero_l2     stage 2 layer (RGBA): black / white staircases at stern, bow and on the superstructure.
  dz_hero_l3     stage 3 layer (RGBA): angled bands in black, white and two greys over everything, a false white bow wave at the
                 stern and a black wedge that cuts the real bow, leaving gaps so the zigzags and staircases still show.
  dz_v<k>        full-dazzle variants for the other ships (set_harbour_dazzle, the convoy has none: it is grey).

    import harbour_tex as HX
    tx = HX.ensure()           # {name: png path}
"""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8')):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np                                              # noqa: E402
from PIL import Image, ImageDraw                                 # noqa: E402
import wall_tex as WX                                            # noqa: E402  (film-9 painters: sky, noise, save)
from wall_tex import hexf, hex8, pnoise, pfbm, save              # noqa: E402

TEX = os.path.join(HERE, 'tex_harbour')
DESERT_TEX = os.path.join(PROJ, 'v3', 'set3d8', 'tex_desert')
TEX_V = 'h10.9'
ZP0, ZP1 = -2.0, 24.0                                           # paint image z span (ship space)
PANO_R = 420.0; PANO_Z0, PANO_Z1 = -4.0, 70.0                   # harbour backdrop ring (harbour.py builds it with these)
JOBS = {}
def reg(name, params, fn): JOBS[name] = (params, fn)

BLACK, WHITE, DGREY, LGREY, MGREY = '#17191d', '#f0f0ea', '#4e545c', '#bfc4c8', '#9c968c'
# 1917 dazzle palette (client round 3): navy, cerulean / sky blue, pale grey-white, slate; sea-green, pale blue, off-white; black only an accent
NAVY, CERUL, SKY, PALE, SLATE, SEAG, PBLUE, OFFW = '#1f2f5a', '#3f86c4', '#8fc0e2', '#eef0ea', '#5c6a7a', '#4f9784', '#a8cde0', '#f2eee2'
WL = 1.15                                                        # top of the white boot-top line (ship z): dazzle paint starts above it
PALETTES = [[NAVY, PALE, CERUL, PALE], [SEAG, OFFW, PBLUE, NAVY], [SLATE, SKY, PALE, NAVY], [NAVY, SKY, OFFW, CERUL], [SEAG, PBLUE, OFFW, SLATE], [CERUL, PALE, NAVY, SKY]]

# ============================================================================= dazzle paint
class Canvas:
    """Supersampled RGBA canvas in ship coordinates (x -L/2..L/2, z ZP0..ZP1)."""
    def __init__(s, L, ppd, ss=2, bg=None):
        s.L = L; s.ppd = ppd; s.ss = ss; s.W = int(L * ppd); s.H = int((ZP1 - ZP0) * ppd)
        s.im = Image.new('RGBA', (s.W * ss, s.H * ss), hex8(bg) + (255,) if bg else (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im)
    def P(s, x, z): return ((x + s.L / 2) * s.ppd * s.ss, (ZP1 - z) * s.ppd * s.ss)
    def poly(s, pts, col, a=255): s.d.polygon([s.P(x, z) for x, z in pts], fill=hex8(col) + (a,))
    def rect(s, x0, z0, x1, z1, col, a=255): s.poly([(x0, z0), (x1, z0), (x1, z1), (x0, z1)], col, a)
    def circle(s, x, z, r, col): (cx, cy) = s.P(x, z); R = r * s.ppd * s.ss; s.d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=hex8(col) + (255,))
    def band(s, pts, z_lo, z_hi, col):
        """Zigzag band: polyline pts (x, z) thickened vertically from z+z_lo to z+z_hi (parallel, hard corners)."""
        s.poly([(x, z + z_hi) for x, z in pts] + [(x, z + z_lo) for x, z in pts[::-1]], col)
    def slant(s, x0, x1, z0, z1, slope, width, cols, phase=0.0, skip=()):
        """Parallel slanted stripes (z = slope * x + c) of `width` (measured along z) clipped to the box, colours cycling; indices
        in skip are left transparent."""
        tmp = Image.new('RGBA', s.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
        span = abs(slope) * (x1 - x0) + (z1 - z0); n = int(span / width) + 3; c0 = z0 - (slope * x1 if slope > 0 else slope * x0) - width + phase
        for k in range(n):
            if k % len(cols) in skip: continue
            c = c0 + k * width; col = cols[k % len(cols)]
            pts = [(x0 - 1, slope * (x0 - 1) + c), (x1 + 1, slope * (x1 + 1) + c), (x1 + 1, slope * (x1 + 1) + c + width), (x0 - 1, slope * (x0 - 1) + c + width)]
            d.polygon([s.P(x, z) for x, z in pts], fill=hex8(col) + (255,))
        bx0, by0 = s.P(x0, z1); bx1, by1 = s.P(x1, z0); box = Image.new('L', s.im.size, 0); ImageDraw.Draw(box).rectangle([bx0, by0, bx1, by1], fill=255)
        a = Image.fromarray(np.minimum(np.asarray(tmp)[..., 3], np.asarray(box)).astype('uint8')); tmp.putalpha(a)
        s.im = Image.alpha_composite(s.im, tmp); s.d = ImageDraw.Draw(s.im)
    def clip_below(s, z):
        a = np.asarray(s.im).copy(); y = int((ZP1 - z) * s.ppd * s.ss); a[y:, :, 3] = 0; s.im = Image.fromarray(a); s.d = ImageDraw.Draw(s.im)
    def fixtures(s, L):
        """Portholes and the hawse pipe, drawn on every layer so they stay visible through the paint."""
        for x in np.arange(-L / 2 + 6, L / 2 - 8, 2.6): s.circle(x, 4.6, 0.36, '#c8a050'); s.circle(x, 4.6, 0.25, '#1c2230')   # brass-rimmed portholes
        s.circle(L / 2 - 3.6, 7.2, 0.55, '#141418')
    def save(s, out, rgb_only=False):
        im = s.im.resize((s.W, s.H), Image.LANCZOS)
        a = np.asarray(im).astype('float32') / 255; rgb = a[..., :3]
        n = pnoise(np.random.RandomState(5), s.H, s.W, 48, 12)[..., None]          # a hand-painted, slightly uneven finish
        rgb = rgb * (0.95 + 0.08 * n)
        save(rgb, out, None if rgb_only else a[..., 3])

def dz_base(p, out):
    L = p['L']; c = Canvas(L, p['ppd'], bg=p['grey'])
    n = pfbm(np.random.RandomState(p['seed']), c.H * c.ss, c.W * c.ss, 24, 8, 3)
    c.rect(-L / 2 - 1, ZP0, L / 2 + 1, 0.9, '#8a2a24'); c.rect(-L / 2 - 1, 0.9, L / 2 + 1, WL, '#f4f2ea')   # antifouling red + white boot-top line
    c.fixtures(L)
    a = np.asarray(c.im).astype('float32'); a[..., :3] *= (0.94 + 0.1 * n[..., None]); c.im = Image.fromarray(np.clip(a, 0, 255).astype('uint8'))
    # rust streaks under the hawse pipe and the scuppers (grey ship only: the paint covers them)
    rr = np.random.RandomState(p['seed'] + 7)
    for x in list(np.arange(-L / 2 + 5, L / 2 - 6, 7.5)) + [L / 2 - 3.6]:
        c.poly([(x - 0.16, 6.9), (x + 0.16, 6.9), (x + 0.06, 3.6), (x - 0.06, 3.6)], '#8a5236', 150)
    for x in np.arange(-L / 2 + 6, L / 2 - 8, 2.6):                               # rust weeping from the portholes
        if rr.rand() < 0.55: ln = rr.uniform(0.8, 2.6); c.poly([(x - 0.09, 4.4), (x + 0.09, 4.4), (x + 0.03, 4.4 - ln), (x - 0.03, 4.4 - ln)], '#8e5634', 120)
    for k in range(40):                                                           # weather blotches along the waterline
        x = rr.uniform(-L / 2, L / 2); c.poly([(x, 1.2), (x + rr.uniform(0.6, 2.0), 1.2), (x + 0.4, 1.2 + rr.uniform(0.3, 1.0))], '#6e6a62', 70)
    c.save(out, rgb_only=True)

def _zig(x0, x1, step, za, zb):
    pts = []; x = x0; k = 0
    while x <= x1 + 1e-6: pts.append((x, za if k % 2 == 0 else zb)); x += step; k += 1
    return pts

def dz_hero(p, out):
    """The painter's ship (L 64): layer = 1 zigzag, 2 staircase, 3 full dazzle."""
    L = p['L']; c = Canvas(L, p['ppd']); layer = p['layer']; h = L / 2
    if layer == 1:
        z = _zig(-h - 1, h + 1, 8.0, 0.8, 6.0)
        c.band(z, -1.0, 1.0, NAVY)                                           # the big navy zigzag
        c.band(z, 1.0, 2.2, PALE)                                            # pale zigzag riding on it
        c.band(z, -2.3, -1.0, CERUL)
        c.band(_zig(-h - 5, h + 1, 8.0, 7.0, 10.5), -0.9, 0.9, NAVY)         # a second zigzag up the bulwark / forecastle
        c.clip_below(WL)
    elif layer == 2:
        for i in range(6):                                                    # stern: black staircase rising toward the bow
            c.rect(-h - 1 + 3.0 * i, WL, -h + 2.0 + 3.0 * i, 2.0 + 1.35 * i, NAVY)
            c.rect(-h - 1 + 3.0 * i, 2.0 + 1.35 * i, -h + 2.0 + 3.0 * i, 3.1 + 1.35 * i, SKY)
        for i in range(6):                                                    # bow: white staircase stepping down toward the stem
            c.rect(h - 3.0 * (i + 1), 9.6 - 1.4 * i, h + 1 - 3.0 * i, 10.5, PALE)
            c.rect(h - 3.0 * (i + 1), 8.4 - 1.4 * i, h + 1 - 3.0 * i, 9.6 - 1.4 * i, NAVY)
        for i in range(5):                                                    # superstructure + funnels: stepped grey / black blocks
            c.rect(-9 + 4.0 * i, 7.2 + 1.6 * i, -5 + 4.0 * i, 9.0 + 1.6 * i, NAVY if i % 2 == 0 else CERUL)
            c.rect(-9 + 4.0 * i, 9.0 + 1.6 * i, -5 + 4.0 * i, 10.6 + 1.6 * i, PALE)
        c.rect(-8.2, 13.5, -3.8, 15.0, NAVY); c.rect(-0.2, 15.0, 4.2, 16.6, CERUL)
        c.clip_below(WL)
    else:
        W, B, G, LG = PALE, NAVY, SLATE, SKY
        c.slant(-h - 1, -12, WL, 24, 0.75, 2.4, [B, W, G, W], skip=(3,))            # stern quarter: steep bands
        c.slant(-12, 6, WL, 24, -1.4, 3.0, [W, B, CERUL, B], phase=1.0, skip=(2,))   # midships: hard opposite slope
        c.slant(6, h + 1, WL, 24, 0.42, 2.2, [B, W, B, G], phase=0.6, skip=(3,))     # bow: shallow bands
        c.poly([(-h - 1, WL), (-h + 13, WL), (-h + 9, 1.9), (-h + 5, 3.4), (-h + 1.5, 5.6), (-h - 1, 6.6)], W)   # false bow wave at the stern
        c.poly([(-h - 1, 6.6), (-h + 1.5, 5.6), (-h + 2.2, 8.5), (-h - 1, 9.5)], B)
        c.poly([(h - 9, 10.5), (h + 1, 10.5), (h + 1, 1.0)], BLACK)                     # black accent wedge that cuts the real bow line
        c.poly([(h - 6, WL), (h + 1, WL), (h + 1, 1.4), (h - 12, 6.5), (h - 14, 6.5)], W)
        c.poly([(-6.5, 18.6), (-5.0, 18.6), (-3.0, 24), (-4.5, 24)], W)                 # funnel flashes
        c.poly([(1.0, 18.6), (2.6, 18.6), (0.6, 24), (-1.0, 24)], B)
        c.clip_below(WL)
    c.fixtures(L)
    c.save(out)

def dz_variant(p, out):
    """Full dazzle for the other ships: 3-4 zones of slanted bands with random slopes / widths / palettes, a zigzag, a false bow."""
    L = p['L']; h = L / 2; rs = np.random.RandomState(p['seed']); c = Canvas(L, p['ppd'], bg=p['bg'])
    pals = [PALETTES[p['pal']], PALETTES[p['pal']][::-1], PALETTES[p['pal']][1:] + PALETTES[p['pal']][:1]]
    cuts = sorted(rs.uniform(-h + 8, h - 8, rs.randint(2, 4))); edges = [-h - 1] + list(cuts) + [h + 1]
    for i in range(len(edges) - 1):
        sl = rs.choice([-1.6, -1.0, -0.6, -0.35, 0.35, 0.6, 1.0, 1.6]) * (1 if i % 2 else -1); pal = pals[i % len(pals)]
        c.slant(edges[i], edges[i + 1], WL, 24, sl, rs.uniform(1.8, 3.4), pal, phase=rs.uniform(0, 2))
    if rs.rand() < 0.8: c.band(_zig(-h - 1, h + 1, rs.uniform(6, 10), 1.8, 5.5), -0.8, 0.8, PALETTES[p['pal']][0])
    c.poly([(-h - 1, WL), (-h + 10, WL), (-h + 4, 3.0), (-h - 1, 5.0)], PALETTES[p['pal']][1])
    c.poly([(h - 5, 10.5), (h + 1, 10.5), (h + 1, 4.0)], BLACK)                                  # black accent at the bow
    c.clip_below(WL); c.fixtures(L)
    c.save(out)

# ============================================================================= dockyard surfaces
def brick_bay(p, out):
    """Warehouse facade bay 6 x 5 D (u along the wall, v one storey): red brick in English bond, sooty, a tall arched window with
    white glazing bars over a stone sill and a soldier-course arch; kind 'side' = plain brick with a pilaster."""
    ppd = p['ppd']; Wd, Hd = 6.0, 5.0; W, H = int(Wd * ppd), int(Hd * ppd); rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:H, 0:W].astype('float32') / ppd
    course = np.floor(yy / 0.25); bl = np.where(course % 2 == 0, 0.75, 0.375); off = np.where(course % 4 == 1, 0.19, 0.0)
    bx = np.floor((xx + off) / bl); bid = (course * 97 + bx * 13).astype(int) % 211; rnd = rs.rand(211, 3)
    base = hexf(p['brick']); col = base * (0.78 + 0.34 * rnd[bid, :1]) + (rnd[bid, 1:2] - 0.5) * np.array([0.08, 0.02, -0.02])
    u = (xx + off) % bl; v = yy % 0.25; mort = (np.minimum(np.minimum(u, bl - u), np.minimum(v, 0.25 - v)) < 0.028)
    col = np.where(mort[..., None], hexf('#b8ab98')[None, None] * 0.9, col)
    n = pfbm(rs, H, W, 6, 5, 4); col = col * (0.82 + 0.25 * n[..., None])
    soot = np.clip((yy / Hd) ** 3 * 0.0 + pfbm(rs, H, W, 3, 2, 3) - 0.55, 0, 1) * 0.6; col = col * (1 - soot[..., None] * 0.5)
    im = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    def R(x0, z0, x1, z1, c): d.rectangle([x0 * ppd, (Hd - z1) * ppd, x1 * ppd, (Hd - z0) * ppd], fill=hex8(c))
    if p['kind'] == 'bay':
        cx = 3.0; w = 2.1; z0, z1 = 0.9, 3.7
        d.ellipse([(cx - w / 2 - 0.25) * ppd, (Hd - z1 - 1.3) * ppd, (cx + w / 2 + 0.25) * ppd, (Hd - z1 + 1.3) * ppd], fill=hex8('#8a3a26'))   # arch ring
        R(cx - w / 2 - 0.25, z0, cx + w / 2 + 0.25, z1, '#8a3a26')
        d.ellipse([(cx - w / 2) * ppd, (Hd - z1 - 1.05) * ppd, (cx + w / 2) * ppd, (Hd - z1 + 1.05) * ppd], fill=hex8(p['glass'])); R(cx - w / 2, z0, cx + w / 2, z1, p['glass'])
        for k in range(1, 3): R(cx - w / 2 + k * w / 3 - 0.04, z0, cx - w / 2 + k * w / 3 + 0.04, z1 + 0.9, '#e8e2d4')
        for zz in np.arange(z0 + 0.7, z1 + 0.9, 0.7): R(cx - w / 2, zz - 0.04, cx + w / 2, zz + 0.04, '#e8e2d4')
        R(cx - w / 2 - 0.35, z0 - 0.22, cx + w / 2 + 0.35, z0, '#d6ccb4')                                       # stone sill
        R(0, 4.75, Wd, 5.0, '#d0c4a8')                                                                          # string course
    else:
        R(0, 0, 0.6, Hd, '#7a2e20'); R(Wd - 0.6, 0, Wd, Hd, '#7a2e20')
    im.save(out)

def glow_bay(p, out):
    """Window glow mask of brick_bay (warm lit panes at DUSK): white where the glass is."""
    ppd = p['ppd']; Wd, Hd = 6.0, 5.0; W, H = int(Wd * ppd), int(Hd * ppd); im = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    rs = np.random.RandomState(4); cx = 3.0; w = 2.1; z0, z1 = 0.9, 3.7
    d.ellipse([(cx - w / 2) * ppd, (Hd - z1 - 1.05) * ppd, (cx + w / 2) * ppd, (Hd - z1 + 1.05) * ppd], fill=(255, 200, 130)); d.rectangle([(cx - w / 2) * ppd, (Hd - z1) * ppd, (cx + w / 2) * ppd, (Hd - z0) * ppd], fill=(255, 200, 130))
    for k in range(1, 3): d.rectangle([(cx - w / 2 + k * w / 3 - 0.04) * ppd, 0, (cx - w / 2 + k * w / 3 + 0.04) * ppd, H], fill=(0, 0, 0))
    for zz in np.arange(z0 + 0.7, z1 + 0.9, 0.7): d.rectangle([0, (Hd - zz - 0.04) * ppd, W, (Hd - zz + 0.04) * ppd], fill=(0, 0, 0))
    im.save(out)

def tile_tex(p, out):
    """Generic 4 x 4 D tiles: setts (granite quay paving), slate (roof), planks (scaffold / deck / crates), steel (deck plates)."""
    ppd = p['ppd']; S = int(4 * ppd); rs = np.random.RandomState(p['seed']); kind = p['kind']
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd; base = hexf(p['col'])
    if kind == 'setts':
        row = np.floor(yy / 0.5); off = (row % 2) * 0.35; bx = np.floor((xx + off) / 0.7); bid = (row * 31 + bx * 7).astype(int) % 173; r = rs.rand(173, 2)
        u = (xx + off) % 0.7; v = yy % 0.5; gap = np.minimum(np.minimum(u, 0.7 - u), np.minimum(v, 0.5 - v))
        col = base * (0.8 + 0.3 * r[bid, :1]) * (0.9 + 0.15 * pnoise(rs, S, S, 60, 60)[..., None])
        col = np.where((gap < 0.035)[..., None], base * 0.45, col * (1 - 0.25 * np.clip(1 - gap / 0.09, 0, 1)[..., None]))
    elif kind == 'slate':
        row = np.floor(yy / 0.4); off = (row % 2) * 0.3; bx = np.floor((xx + off) / 0.6); bid = (row * 31 + bx * 7).astype(int) % 173; r = rs.rand(173, 2)
        u = (xx + off) % 0.6; v = yy % 0.4
        col = base * (0.78 + 0.3 * r[bid, :1]) * (1 - 0.35 * (v / 0.4) ** 3)[..., None]
        col = np.where(((u < 0.03) | (v > 0.37))[..., None], base * 0.4, col)
    elif kind == 'planks':
        w = p.get('w', 0.5); row = np.floor(yy / w); r = rs.rand(512, 2); seg = np.floor((xx + r[row.astype(int) % 512, 1] * 4) / 3.0)
        bid = (row * 17 + seg * 5).astype(int) % 512; grain = np.sin(xx * 9 + pnoise(rs, S, S, 4, 40) * 14)
        col = base * (0.8 + 0.28 * r[bid, :1]) * (0.94 + 0.05 * grain[..., None])
        v = yy % w; u = (xx + r[row.astype(int) % 512, 1] * 4) % 3.0
        col = np.where(((v < 0.03) | (u < 0.025))[..., None], base * 0.4, col)
    else:                                                                       # steel deck plates with rivet rows
        col = base * (0.88 + 0.16 * pfbm(rs, S, S, 4, 4, 4)[..., None]); u = xx % 2.0; v = yy % 1.0
        col = np.where(((u < 0.03) | (v < 0.03))[..., None], base * 0.55, col)
    col = col * (0.9 + 0.14 * pfbm(rs, S, S, 3, 3, 4)[..., None])
    save(np.clip(col, 0, 1), out)

def foam(p, out):
    """Foam / wake alpha (white, blotchy, hard-edged cartoon lace): u along the wake, v across (centre v 0.5). kind 'wake' (long, a
    lace band thinning to the sides and tail), 'bow' (bow-wave crest), 'bubbles' (torpedo track: a dotted bubble line)."""
    W, H = p['w'], p['h']; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    u = xx / W; v = yy / H; n = pfbm(rs, H, W, p.get('cx', 16), p.get('cy', 4), 4); n2 = pnoise(rs, H, W, p.get('cx', 16) * 4, 16)
    kind = p['kind']
    if kind == 'wake':
        prof = np.clip(1 - np.abs(v - 0.5) * 2 / (0.35 + 0.65 * u), 0, 1) * np.clip(1 - u * 0.9, 0, 1)
        a = np.clip((prof * 1.3 + n * 0.9 - 0.75) * 9, 0, 1) + np.clip((n2 - 0.8) * 8, 0, 1) * prof
    elif kind == 'bow':
        prof = np.exp(-((v - 0.5) / 0.22) ** 2) * np.clip(1 - u * 0.75, 0, 1)
        a = np.clip((prof * 1.4 + n * 0.6 - 0.7) * 10, 0, 1)
    else:
        prof = np.exp(-((v - 0.5) / 0.22) ** 2); blot = np.clip((pfbm(rs, H, W, 40, 3, 3) - 0.42) * 6, 0, 1)
        a = np.clip((prof + n2 * 0.9 - 1.0) * 8, 0, 1) + np.clip((prof - 0.3) * 4, 0, 1) * (0.25 + 0.75 * blot)
    a = np.clip(a, 0, 1); rgb = np.ones((H, W, 3), 'float32') * (0.92 + 0.08 * n[..., None])
    save(rgb, out, a)

def flag(p, out):
    """Flags without text: White Ensign (red St George's cross, union canton) and the red pennant."""
    W, H = 240, 120; im = Image.new('RGB', (W, H), hex8('#f2f0ea')); d = ImageDraw.Draw(im)
    if p['kind'] == 'ensign':
        d.rectangle([0, 52, W, 68], fill=hex8('#c8202a')); d.rectangle([112, 0, 128, H], fill=hex8('#c8202a'))
        d.rectangle([0, 0, 112, 52], fill=hex8('#1c2a6a')); d.line([(0, 0), (112, 52)], fill=hex8('#f2f0ea'), width=9); d.line([(0, 52), (112, 0)], fill=hex8('#f2f0ea'), width=9)
        d.line([(0, 0), (112, 52)], fill=hex8('#c8202a'), width=3); d.line([(0, 52), (112, 0)], fill=hex8('#c8202a'), width=3)
        d.rectangle([0, 21, 112, 31], fill=hex8('#f2f0ea')); d.rectangle([50, 0, 62, 52], fill=hex8('#f2f0ea'))
        d.rectangle([0, 23, 112, 29], fill=hex8('#c8202a')); d.rectangle([53, 0, 59, 52], fill=hex8('#c8202a'))
    else:
        d.rectangle([0, 0, W, H], fill=hex8(p['col']))
    im.save(out)

# ============================================================================= backdrop ring (harbour)
PANH = dict(
    DAY=dict(far='#9aa2c0', hill='#6a7a52', hill2='#7e8a5a', brick='#a65a42', roof='#4a4a5a', stack='#5a4a48', smoke='#d8d2cc', fog='#f0dcc0', win=None, sea='#6a8ab0'),
    DUSK=dict(far='#7a74a8', hill='#3e4058', hill2='#4a4a66', brick='#7a4a4a', roof='#2a2a3c', stack='#2e2a36', smoke='#a08890', fog='#ffb890', win='#ffb048', sea='#d89a7a'),
)
def pano_harb(p, out):
    """Painted ring R 420 around the dockyard (u = azimuth / 360 from +x CCW): green headlands, a terraced brick town with chimneys
    and smoke, church spires, a gasholder, distant cranes and sheds over the land side (az 150..390), open sea with a far headland
    and tiny ship silhouettes toward the harbour mouth (az 40..140). DUSK adds warm windows."""
    c = PANH[p['mode']]; ppd = p['ppd']; Wd = 2 * math.pi * PANO_R; Hd = PANO_Z1 - PANO_Z0; W, H = int(Wd * ppd), int(Hd * ppd)
    rs = np.random.RandomState(41); im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def Y(z): return (PANO_Z1 - z) * ppd
    def X(az): return (az % 360) / 360.0 * W
    def land(az0, az1, base, amp, col, seed, n=80):
        r = np.random.RandomState(seed); xs = np.linspace(X(az0), X(az0) + (az1 - az0) / 360 * W, n)
        zs = [base + amp * (0.55 + 0.3 * math.sin(i * 0.21 + seed) + 0.15 * math.sin(i * 0.77)) + r.uniform(0, amp * 0.1) for i in range(n)]
        zs[0] = zs[-1] = -2
        pts = [(x % W, Y(z)) for x, z in zip(xs, zs)]
        for sh in (0, -W, W): d.polygon([(x + sh, y) for x, y in pts] + [(xs[-1] + sh, Y(-4)), (xs[0] + sh, Y(-4))], fill=hex8(col) + (255,))
    def blend(a, b, t): A, B = hexf(a), hexf(b); return '#%02x%02x%02x' % tuple(int(255 * (A[i] * (1 - t) + B[i] * t)) for i in range(3))
    land(150, 395, 18, 26, blend(c['far'], c['fog'], 0.3), 3, 120)
    land(165, 385, 6, 16, c['hill2'], 5, 160)
    land(20, 70, 2, 9, blend(c['far'], c['fog'], 0.15), 9, 40)                 # far headland across the mouth
    hx = X(44.0); hcol = blend(c['hill'], c['fog'], 0.25)                           # a green hill with a church and cottages on it
    d.polygon([(hx - 40 * ppd, Y(-2)), (hx - 12 * ppd, Y(13)), (hx + 10 * ppd, Y(14)), (hx + 38 * ppd, Y(-2))], fill=hex8(hcol) + (255,))
    cc = blend(c['brick'], c['fog'], 0.3); rc = blend(c['roof'], c['fog'], 0.2)
    d.rectangle([hx - 4 * ppd, Y(20), hx + 6 * ppd, Y(13)], fill=hex8(cc) + (255,)); d.polygon([(hx - 5 * ppd, Y(20)), (hx + 1 * ppd, Y(24)), (hx + 7 * ppd, Y(20))], fill=hex8(rc) + (255,))
    d.rectangle([hx - 8 * ppd, Y(26), hx - 4 * ppd, Y(13)], fill=hex8(cc) + (255,)); d.polygon([(hx - 8.6 * ppd, Y(26)), (hx - 6 * ppd, Y(36)), (hx - 3.4 * ppd, Y(26))], fill=hex8(rc) + (255,))
    for k in range(9):
        qx = hx + (-30 + k * 7) * ppd; qz = 13 - abs(k - 4) * 2.6
        d.rectangle([qx, Y(qz + 2.6), qx + 4 * ppd, Y(qz - 2)], fill=hex8(blend('#e8dcc8', c['fog'], 0.3)) + (255,)); d.polygon([(qx - 0.6 * ppd, Y(qz + 2.6)), (qx + 2 * ppd, Y(qz + 4.4)), (qx + 4.6 * ppd, Y(qz + 2.6))], fill=hex8(rc) + (255,))
        if c['win']: d.rectangle([qx + 1.5 * ppd, Y(qz + 1.4), qx + 2.5 * ppd, Y(qz + 0.4)], fill=hex8(c['win']) + (255,))
    land(118, 160, 3, 12, c['hill'], 11, 40)
    # the town: terraces, chimneys, spires, gasholder, sheds, cranes
    x = X(170)
    while x < X(380):
        w = rs.uniform(10, 26) * ppd; h = rs.uniform(4, 11); z0 = rs.uniform(-1, 6)
        d.rectangle([x % W, Y(z0 + h), (x + w) % W if (x + w) % W > x % W else W, Y(-3)], fill=hex8(blend(c['brick'], c['fog'], rs.uniform(0, 0.4))) + (255,))
        d.polygon([(x % W - 2, Y(z0 + h)), ((x + w / 2) % W, Y(z0 + h + rs.uniform(2, 4))), ((x + w) % W + 2, Y(z0 + h))], fill=hex8(c['roof']) + (255,)) if (x + w) % W > x % W else None
        if c['win']:
            for k in range(int(w / ppd / 3)):
                if rs.rand() < 0.45: wx = x + (k + 0.4) * 3 * ppd; d.rectangle([wx % W, Y(z0 + h * 0.6), (wx + ppd) % W, Y(z0 + h * 0.6 - 1.2)], fill=hex8(c['win']) + (255,))
        if rs.rand() < 0.55:                                                   # chimney stacks with a smoke plume
            sx = x + rs.uniform(0.2, 0.8) * w; sh = rs.uniform(10, 26)
            d.rectangle([sx % W, Y(z0 + h + sh), (sx + 1.8 * ppd) % W, Y(z0 + h)], fill=hex8(c['stack']) + (255,))
            for j in range(6):
                r_ = (1.6 + j * 1.1) * ppd; cx = sx + 0.9 * ppd + j * 2.6 * ppd; cy = Y(z0 + h + sh + 1.2 + j * 1.4)
                d.ellipse([cx % W - r_, cy - r_ * 0.7, cx % W + r_, cy + r_ * 0.7], fill=hex8(blend(c['smoke'], c['fog'], j / 7)) + (230 - j * 25,))
        x += w + rs.uniform(0, 4) * ppd
    for az in (205.0, 262.0, 318.0):                                            # spires
        sx = X(az); d.rectangle([sx, Y(22), sx + 5 * ppd, Y(-2)], fill=hex8(blend(c['roof'], c['fog'], 0.15)) + (255,))
        d.polygon([(sx - 0.5 * ppd, Y(22)), (sx + 2.5 * ppd, Y(42)), (sx + 5.5 * ppd, Y(22))], fill=hex8(c['roof']) + (255,))
    gx = X(236); d.rectangle([gx, Y(14), gx + 22 * ppd, Y(-2)], fill=hex8(blend(c['stack'], c['fog'], 0.35)) + (255,))  # gasholder frame
    for k in range(7): d.rectangle([gx + k * 3.5 * ppd, Y(17), gx + k * 3.5 * ppd + 0.6 * ppd, Y(-2)], fill=hex8(c['stack']) + (255,))
    for az in (178.0, 290.0, 350.0, 372.0):                                     # distant hammerhead cranes
        cx = X(az); d.rectangle([cx, Y(30), cx + 1.4 * ppd, Y(-2)], fill=hex8(c['stack']) + (255,))
        d.rectangle([cx - 14 * ppd, Y(31), cx + 9 * ppd, Y(28.5)], fill=hex8(c['stack']) + (255,))
    for k in range(9):                                                          # tiny ship silhouettes out at sea
        sx = X(rs.uniform(48, 132)); w = rs.uniform(10, 18) * ppd
        d.polygon([(sx, Y(-0.5)), (sx + w, Y(-0.5)), (sx + w * 1.06, Y(1.6)), (sx - w * 0.04, Y(1.6))], fill=hex8(blend(c['far'], c['fog'], 0.2)) + (255,))
        d.rectangle([sx + w * 0.4, Y(4.5), sx + w * 0.5, Y(1.6)], fill=hex8(blend(c['far'], c['fog'], 0.2)) + (255,))
    a = np.asarray(im).astype('float32') / 255
    zrow = PANO_Z1 - (np.arange(H) + 0.5) / ppd; fog = np.clip(1 - (zrow + 4) / 18.0, 0, 1)[:, None, None] * 0.45
    rgb = a[..., :3] * (1 - fog) + hexf(c['fog'])[None, None] * fog
    save(rgb, out, a[..., 3])

def bars(p, out):
    """Periscope reticle: nothing painted (the crosshair is 3D geometry); kept for API symmetry."""
    Image.new('RGBA', (8, 8), (0, 0, 0, 0)).save(out)

# ============================================================================= registry
HERO_L = 64.0
SHIP_LS = dict(hero=64.0, v1=60.0, v2=58.0, v3=66.0, v4=52.0, v5=56.0, v6=62.0)
def plates(p, out):
    """Hull plating overlay (multiply, RGB): one 4 D wide x 26 D tall tile in ship space (x repeats every 4 D, v = (z - ZP0) / 26):
    vertical butt seams, horizontal strake lines at z 1.15 / 3.1 / 5.1 / 7.1 / 9.1, rivet dots along both, a soft plate-edge shadow."""
    ppd = p['ppd']; W, H = int(4 * ppd), int((ZP1 - ZP0) * ppd); im = np.ones((H, W), 'float32')
    def Y(z): return int((ZP1 - z) * ppd)
    for z in (3.1, 5.1, 7.1, 9.1, 11.3, 13.4, 15.5):
        y = Y(z); im[max(0, y - 1):y + 1, :] *= 0.72; im[y + 1:y + 3, :] *= 0.9                     # strake line + its soft shadow
        for x in np.arange(0.12, 4.0, 0.3): xi = int(x * ppd); im[y - 4:y - 2, xi:xi + 2] *= 0.62     # rivet row above the seam
    for x in (0.0, 2.0):
        xi = int(x * ppd); im[:, xi:xi + 1] *= 0.78; im[:, xi + 1:xi + 3] *= 0.92
        for z in np.arange(1.3, 16.0, 0.3): yi = Y(z); im[yi:yi + 2, xi + 4:xi + 6] *= 0.68
    im[Y(1.15):, :] = 1.0                                                                             # none on the antifouling
    save(np.repeat(im[..., None], 3, 2), out)

def shallow(p, out):
    """Shallow-water glow (alpha): full at v 0 (the wall / hull) fading to 0 at v 1, with a soft wavy edge."""
    W, H = 256, 64; rs = np.random.RandomState(3); yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    v = yy / H + (pnoise(rs, H, W, 8, 2) - 0.5) * 0.25; a = np.clip(1 - v, 0, 1) ** 2
    save(np.ones((H, W, 3), 'float32'), out, a)

def net(p, out):
    """Fishing / cargo net (RGBA): diamond mesh of tarred cord with a few floats."""
    S = 256; yy, xx = np.mgrid[0:S, 0:S].astype('float32'); c = 22.0
    d1 = np.abs(((xx + yy) % c) - c / 2); d2 = np.abs(((xx - yy) % c) - c / 2)
    a = np.clip((np.maximum(d1, d2) - (c / 2 - 2.2)) * 0.8, 0, 1)
    rgb = np.ones((S, S, 3), 'float32') * hexf('#4a3a28')
    save(rgb, out, a)

def quaywall(p, out):
    """Granite quay wall 4 x 4 D (v 0 = z -4, v 1 = z 0, water at z -2.4): ashlar courses, a dark wet band and green weed at the
    waterline, lighter dry stone above with run-down stains."""
    ppd = p['ppd']; S = int(4 * ppd); rs = np.random.RandomState(9); yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    z = -yy                                                                         # top row = z 0
    row = np.floor(yy / 0.8); off = (row % 2) * 0.9; bx = np.floor((xx + off) / 1.8); bid = (row * 31 + bx * 7).astype(int) % 97; r = rs.rand(97)
    col = hexf('#a8a090')[None, None] * (0.82 + 0.25 * r[bid][..., None]) * (0.9 + 0.15 * pfbm(rs, S, S, 6, 6, 4)[..., None])
    u = (xx + off) % 1.8; v = yy % 0.8; j = (np.minimum(np.minimum(u, 1.8 - u), np.minimum(v, 0.8 - v)) < 0.04)
    col = np.where(j[..., None], col * 0.55, col)
    wet = np.clip((-1.3 - z) / 0.5, 0, 1); streak = np.clip((pnoise(rs, S, S, 30, 2) - 0.4) * 3, 0, 1) * np.clip((-0.4 - z) / 1.5, 0, 1)
    col = col * (1 - 0.45 * np.maximum(wet, 0.6 * streak)[..., None])
    weed = np.clip(1 - np.abs(z + 2.25) / (0.35 + 0.2 * pnoise(rs, S, S, 24, 4)), 0, 1)
    col = col * (1 - weed[..., None]) + weed[..., None] * hexf('#3e6a2e') * (0.8 + 0.4 * pnoise(rs, S, S, 40, 8)[..., None])
    save(np.clip(col, 0, 1), out)

def sky_rich(p, out):
    """The film-9 sky painter (wall_tex.sky) + a richer cloud deck: a low bank of big cartoon cumulus along the horizon, scattered small
    puffs high up, a few long thin streaks, and a soft warm haze band toward the horizon for depth."""
    WX.sky(dict(p, mode=p['base']), out)
    img = np.asarray(Image.open(out).convert('RGB')).astype('float32') / 255; H, W = img.shape[:2]; rs = np.random.RandomState(p['seed'])
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0
    def disc_cloud(cx, by, wd, hd, nd, c_body, c_top, c_bot):
        ppd = W / 360.0; X = np.arange(int(cx - wd * ppd), int(cx + wd * ppd)); Y = np.arange(max(0, int(by - hd * ppd * 2.8)), min(H, int(by + 1)))
        if len(Y) < 2: return
        XX, YY = np.meshgrid(X.astype('float32'), Y.astype('float32')); cov = np.zeros(XX.shape, 'float32'); top = np.zeros_like(cov)
        for k in range(nd):
            u = (k + 0.5) / nd - 0.5; x0 = cx + u * wd * ppd * 1.6; rd = hd * ppd * rs.uniform(0.7, 1.3) * (1 - 1.6 * u * u); y0 = by - rd * rs.uniform(0.2, 0.5)
            d = np.sqrt((XX - x0) ** 2 + (YY - y0) ** 2); cov = np.maximum(cov, np.clip(rd - d + 0.5, 0, 1))
            top = np.maximum(top, np.clip(rd * 0.8 - np.sqrt((XX - x0 + rd * 0.1) ** 2 + (YY - y0 + rd * 0.3) ** 2) + 0.5, 0, 1))
        cov *= np.clip(by - YY + 0.5, 0, 1); bot = np.clip(YY - (by - hd * ppd * 0.45) + 0.5, 0, 1)
        col = hexf(c_body)[None, None] * (1 - top[..., None]) + hexf(c_top)[None, None] * top[..., None]; col = col * (1 - bot[..., None]) + hexf(c_bot)[None, None] * bot[..., None]
        xs = X % W; sl = img[Y][:, xs]; img[np.ix_(Y, xs)] = sl * (1 - cov[..., None]) + col * cov[..., None]
    cb, ct, cbo = p['cloud']
    for k in range(70):                                                            # low bank of big cumulus near the horizon
        e = rs.uniform(1.5, 7.0); disc_cloud(rs.uniform(0, W), (90 - e) / 105 * H, rs.uniform(8, 20), rs.uniform(1.6, 3.2), rs.randint(5, 10), cb, ct, cbo)
    for k in range(60):                                                            # medium puffs, higher
        e = rs.uniform(14, 50); disc_cloud(rs.uniform(0, W), (90 - e) / 105 * H, rs.uniform(3.5, 8.0), rs.uniform(1.0, 1.9), rs.randint(3, 6), cb, ct, cbo)
    for k in range(22):                                                            # long thin streaks
        e = rs.uniform(18, 40); disc_cloud(rs.uniform(0, W), (90 - e) / 105 * H, rs.uniform(25, 45), rs.uniform(0.55, 0.85), rs.randint(10, 16), ct, ct, cb)
    hz = np.exp(-np.clip(el, 0, 90) / 7.0)[:, None, None] * np.clip(el + 3, 0, 3)[:, None, None] / 3.0 * 0.45   # soft horizon haze
    img = img * (1 - hz) + hexf(p['haze'])[None, None] * hz
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype('uint8'), 'RGB').save(out)

def all_jobs():
    JOBS.clear()
    reg('dz_hero_base', dict(L=HERO_L, ppd=40, grey='#9a958c', seed=3), dz_base)
    for k in (1, 2, 3): reg('dz_hero_l%d' % k, dict(L=HERO_L, ppd=40, layer=k), dz_hero)
    for i, (nm, L) in enumerate(SHIP_LS.items()):
        if nm == 'hero': continue
        reg('dz_%s_base' % nm, dict(L=L, ppd=24, grey=['#9c968c', '#a19a8e', '#958f87', '#a39d93', '#98928a', '#9e988e'][i % 6], seed=3 + i), dz_base)   # warm battleship greys
        reg('dz_%s' % nm, dict(L=L, ppd=24, seed=100 + 7 * i, pal=(i - 1) % 6, bg=[PALE, OFFW, PALE, OFFW, PBLUE, PALE][i % 6]), dz_variant)
    reg('brick_bay', dict(kind='bay', ppd=64, seed=11, brick='#a04a34', glass='#2e3448'), brick_bay)
    reg('brick_bay_b', dict(kind='bay', ppd=64, seed=13, brick='#8e4632', glass='#2e3448'), brick_bay)
    reg('brick_side', dict(kind='side', ppd=64, seed=17, brick='#9a4632', glass='#2e3448'), brick_bay)
    reg('glow_bay', dict(ppd=32), glow_bay)
    reg('setts', dict(kind='setts', ppd=64, seed=21, col='#9a948c'), tile_tex)
    reg('kerb', dict(kind='setts', ppd=48, seed=22, col='#b6aea0'), tile_tex)
    reg('slate', dict(kind='slate', ppd=48, seed=23, col='#4e5462'), tile_tex)
    reg('planks', dict(kind='planks', ppd=64, seed=25, col='#a87a4c', w=0.5), tile_tex)
    reg('deck', dict(kind='planks', ppd=48, seed=27, col='#c88e58', w=0.3), tile_tex)
    reg('crate', dict(kind='planks', ppd=48, seed=29, col='#b88a52', w=0.6), tile_tex)
    reg('steel', dict(kind='steel', ppd=32, seed=31, col='#6e747c'), tile_tex)
    reg('foam_wake', dict(kind='wake', w=1024, h=256, seed=41, cx=24, cy=6), foam)
    reg('foam_bow', dict(kind='bow', w=512, h=128, seed=43, cx=16, cy=4), foam)
    reg('foam_bubbles', dict(kind='bubbles', w=1024, h=128, seed=45, cx=48, cy=4), foam)
    reg('flag_ensign', dict(kind='ensign'), flag)
    reg('plates', dict(ppd=20), plates); reg('shallow', dict(), shallow); reg('net', dict(), net); reg('quaywall', dict(ppd=48), quaywall)
    reg('flag_red', dict(kind='plain', col='#c8282a'), flag)
    for m in ('DAY', 'DUSK'): reg('pano_HARB_' + m, dict(mode=m, ppd=3), pano_harb)
    # skies (wall_tex.sky painter, film-9 look): sun (azimuth, elevation) matches harbour.LIGHTS key_dir
    reg('sky_DAY', dict(base='DAY', sun=(235.0, 32.0), w=WX.SKY_W, seed=11, cloud=('#ecc2b4', '#ffd890', '#b29cc2'), haze='#f4dcbc'), sky_rich)
    reg('sky_DUSK', dict(base='DAWNG', sun=(300.0, 9.0), w=WX.SKY_W, seed=12, cloud=('#f6c8b4', '#ffe0a0', '#c8a0b8'), haze='#ffd0b0'), sky_rich)   # crisp cartoon clouds at dusk
    reg('sky_SEA_DAY', dict(base='DAY', sun=(250.0, 18.0), w=WX.SKY_W, seed=13, cloud=('#f0cabc', '#ffdc98', '#aea0c8'), haze='#f2dcc4'), sky_rich)

def ensure(verbose=True):
    """Paint every changed texture; return {name: png path} (+ shared desert glow images pool / shaft / glint / wisp)."""
    os.makedirs(TEX, exist_ok=True); all_jobs()
    mpath = os.path.join(TEX, 'manifest.json')
    try: man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    except ValueError: man = {}
    man0 = dict(man); out = {}
    for name, (params, fn) in JOBS.items():
        ver = WX.TEX_V + TEX_V if fn in (WX.sky, sky_rich) else TEX_V
        h = hashlib.sha1((ver + fn.__name__ + json.dumps(params, sort_keys=True)).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            fn(params, png); man[name] = h
            if verbose: print('painted', name, flush=True)
    if man != man0:
        tmp = '%s.%d.tmp' % (mpath, os.getpid()); json.dump(man, open(tmp, 'w'), indent=0, sort_keys=True); os.replace(tmp, mpath)
    for nm in ('pool', 'shaft', 'glint', 'wisp'): out[nm] = os.path.join(DESERT_TEX, nm + '.png')
    return out

if __name__ == '__main__':
    p = ensure(); print(len(p), 'textures')
