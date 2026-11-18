#!/usr/bin/env python3
"""chicago_tex.py : artwork of the film-13 set (Chicago 1861, raising the Tremont House). numpy + PIL, deterministic, cached in
v3/set3d13/tex_chicago/ by a hash of (TEX_V, painter, params). Bump TEX_V after editing painter code.  tx = CX.ensure() -> {name: png}.
Skies reuse harbour_tex.sky_rich (film 10) with this set's sun."""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d10'), os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8')):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np                                              # noqa: E402
from PIL import Image, ImageDraw, ImageFilter                    # noqa: E402
import wall_tex as WX                                            # noqa: E402
import harbour_tex as HX                                         # noqa: E402
from wall_tex import hexf, hex8, pnoise, pfbm, save              # noqa: E402

TEX = os.path.join(HERE, 'tex_chicago')
DESERT_TEX = os.path.join(PROJ, 'v3', 'set3d8', 'tex_desert')
TEX_V = 'c13.8'
PANO_R = 420.0; PANO_Z0, PANO_Z1 = -4.0, 90.0
SUN_DAY = (325.0, 33.0)          # sky-texture azimuth (from +x CCW) / elevation of the key sun (street: sun at +x, -y side)
JOBS = {}
def reg(name, params, fn): JOBS[name] = (params, fn)

# ----------------------------------------------------------------------------- helpers
def _rs(p): return np.random.RandomState(p.get('seed', 1))

def _grid(H, W, ppd):
    yy, xx = np.mgrid[0:H, 0:W].astype('float32'); return yy / ppd, xx / ppd

def _brick_arr(rs, H, W, ppd, base, cw=0.62, ch=0.3, var=0.3, mort='#b9ab94', soot=0.0):
    yy, xx = _grid(H, W, ppd)
    course = np.floor(yy / ch); off = np.where(course % 2 == 0, 0.0, cw / 2); bx = np.floor((xx + off) / cw)
    bid = ((course * 97 + bx * 13).astype(int)) % 509; rnd = rs.rand(509, 3)
    b = hexf(base); col = b * (1 - var / 2 + var * rnd[bid, :1]) + (rnd[bid, 1:2] - 0.5) * np.array([0.07, 0.015, -0.03])
    u = (xx + off) % cw; v = yy % ch; d = np.minimum(np.minimum(u, cw - u), np.minimum(v, ch - v))
    m = np.clip(1 - (d - 0.012) / 0.03, 0, 1)[..., None]                     # soft mortar line
    col = col * (1 - m) + hexf(mort)[None, None] * 0.92 * m
    n = pfbm(rs, H, W, 6, 6, 4); col = col * (0.84 + 0.22 * n[..., None])
    if soot: col = col * (1 - soot * np.clip(pfbm(rs, H, W, 3, 4, 3) - 0.5, 0, 1)[..., None] * 1.2)
    return col

def _vgrad(H, W, top, bot):
    t = np.linspace(0, 1, H, dtype='float32')[:, None, None]; return hexf(top)[None, None] * (1 - t) + hexf(bot)[None, None] * t

# ----------------------------------------------------------------------------- brick / stone / timber / plank
def brick_tile(p, out):
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p)
    save(np.clip(_brick_arr(rs, S, S, ppd, p['col'], soot=p.get('soot', 0.2)), 0, 1), out)

def stone_tile(p, out):
    """cream ashlar (kind 'ash') or deeply jointed rusticated stone ('rust')."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); base = hexf(p['col'])
    bh = 1.0 if p['kind'] == 'rust' else 0.8; bw = 2.0 if p['kind'] == 'rust' else 1.6
    row = np.floor(yy / bh); off = (row % 2) * bw / 2; bx = np.floor((xx + off) / bw); bid = ((row * 31 + bx * 7).astype(int)) % 257; r = rs.rand(257, 2)
    col = base * (0.92 + 0.14 * r[bid, :1]) * (0.94 + 0.1 * pfbm(rs, S, S, 8, 8, 4)[..., None])
    u = (xx + off) % bw; v = yy % bh; d = np.minimum(np.minimum(u, bw - u), np.minimum(v, bh - v))
    jw = 0.06 if p['kind'] == 'rust' else 0.025
    m = np.clip(1 - (d - jw * 0.4) / jw, 0, 1)[..., None]; col = col * (1 - 0.55 * m) + 0.0
    if p['kind'] == 'rust': col = col * (0.86 + 0.14 * np.clip(d / 0.25, 0, 1)[..., None])   # chamfer shading toward the joints
    save(np.clip(col, 0, 1), out)

def planks(p, out):
    """weathered boards: sidewalk / floor / crates.  w = board width, col base colour, 'nails' dots, dir along x."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); w = p['w']; base = hexf(p['col'])
    row = np.floor(yy / w); r = rs.rand(256, 3); ri = row.astype(int) % 256; seg = np.floor((xx + r[ri, 1] * 6) / p.get('len', 4.0))
    bid = ((row * 17 + seg * 5).astype(int)) % 256
    grain = np.sin((yy * 22 + pnoise(rs, S, S, 4, 30) * 9)) * 0.5 + 0.5
    col = base * (0.78 + 0.3 * r[bid, :1]) * (0.92 + 0.1 * grain[..., None]) * (0.9 + 0.2 * pfbm(rs, S, S, 5, 12, 4)[..., None])
    v = yy % w; u = (xx + r[ri, 1] * 6) % p.get('len', 4.0)
    gap = (v < 0.035) | (v > w - 0.02) | (u < 0.03)
    col = np.where(gap[..., None], base * 0.35, col)
    if p.get('nails'):
        nx = (xx % 1.0 < 0.06) & ((v > w * 0.4) & (v < w * 0.6)); col = np.where(nx[..., None], base * 0.4, col)
    if p.get('wet'): col = col * (1 - 0.35 * np.clip(pfbm(rs, S, S, 3, 3, 3) - 0.45, 0, 1)[..., None] * 2)
    save(np.clip(col, 0, 1), out)

def timber(p, out):
    """hewn beams: long grain along x, bolts dots (for beams / cribbing)."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); base = hexf(p['col'])
    g = pnoise(rs, S, S, 3, 40); grain = np.sin(yy * 30 + g * 14) * 0.5 + 0.5
    col = base * (0.78 + 0.34 * grain[..., None]) * (0.88 + 0.22 * pfbm(rs, S, S, 4, 14, 4)[..., None])
    for _ in range(5):                                                       # knots
        kx, ky = rs.uniform(0, S), rs.uniform(0, S); d = np.sqrt(((xx * ppd - kx) / 2.5) ** 2 + (yy * ppd - ky) ** 2)
        col = col * (1 - 0.35 * np.exp(-(d / 9) ** 2)[..., None])
    col = col * (1 - 0.25 * np.clip(pfbm(rs, S, S, 3, 3, 3) - 0.55, 0, 1)[..., None] * 3)
    save(np.clip(col, 0, 1), out)

def clap(p, out):
    """clapboard siding (horizontal overlapping boards), painted."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); base = hexf(p['col']); bh = 0.38
    v = (yy % bh) / bh; col = base * (0.84 + 0.2 * v[..., None] ** 0.5)
    col = np.where((v < 0.08)[..., None], base * 0.5, col) * (0.92 + 0.12 * pfbm(rs, S, S, 4, 16, 3)[..., None])
    save(np.clip(col, 0, 1), out)

# ----------------------------------------------------------------------------- mud / earth / gravel
def mud(p, out):
    """glossy-street mud: ochre-brown, wetter darker patches, straw flecks, hoof and wheel dents (painted shading), tileable."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); base = hexf(p['col'])
    n1 = pfbm(rs, S, S, 4, 4, 5); n2 = pfbm(rs, S, S, 14, 14, 3); n3 = pfbm(rs, S, S, 30, 30, 2)
    wet = np.clip((n1 - 0.45) * 3.2, 0, 1)
    col = base[None, None] * (0.82 + 0.34 * n2[..., None]) * (1 - 0.30 * wet[..., None])
    col = col * (1 + 0.12 * (n3[..., None] - 0.5)) + wet[..., None] * np.array([-0.03, -0.035, 0.0], 'float32')
    dry = np.clip((n1 - 0.62) * 4, 0, 1)[..., None]; col = col * (1 - dry) + dry * (hexf(p.get('dry', '#a07a4c')) * (0.9 + 0.2 * n2[..., None]))   # drier ochre crust
    im = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for _ in range(int(p.get('straw', 160))):                               # straw / chaff flecks
        x, y = rs.uniform(0, S), rs.uniform(0, S); a = rs.uniform(0, 3.14); l = rs.uniform(4, 11) * ppd / 40
        d.line([(x, y), (x + l * math.cos(a), y + l * math.sin(a))], fill=(214, 178, 96) if rs.rand() < 0.7 else (120, 84, 50), width=1)
    for _ in range(int(p.get('hoof', 30))):                                  # hoof prints: darker crescent with pale rim
        x, y = rs.uniform(0, S), rs.uniform(0, S); r = rs.uniform(7, 11) * ppd / 40
        d.ellipse([x - r, y - r * 0.8, x + r, y + r * 0.8], fill=tuple(int(c * 0.62) for c in (base * 255)))
        d.ellipse([x - r * 0.6, y - r * 0.5 - 2, x + r * 0.6, y + r * 0.5 - 2], fill=tuple(int(c * 0.9) for c in (base * 255)))
    im = im.filter(ImageFilter.GaussianBlur(0.7)); im.save(out)

def earth(p, out):
    """fill earth / gravel / clay heap: lighter ochre-orange clay with pebbles."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); base = hexf(p['col'])
    n = pfbm(rs, S, S, 6, 6, 5); n2 = pfbm(rs, S, S, 24, 24, 3)
    col = base[None, None] * (0.78 + 0.4 * n[..., None]) * (0.92 + 0.16 * n2[..., None])
    im = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for _ in range(int(S * S / 260)):
        x, y = rs.uniform(0, S), rs.uniform(0, S); r = rs.uniform(1.0, 2.6) * ppd / 40; c = int(rs.uniform(70, 130))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(c, int(c * 0.86), int(c * 0.68)))
    im.save(out)

# ----------------------------------------------------------------------------- windows (a single sash window image: W x H D)
def _lamp_glow(rs, W, H, warm):
    return warm

def window(p, out):
    """Tall double-hung sash window, W x H D (u across, v up): cream frame, 2 x 3 panes per sash, sill line. state: dark | lit | curt | lit2.
    Panes: reflected sky (violet-blue top to teal-grey bottom) with a diagonal glint; lit: warm amber interior with a dark furniture
    silhouette; curt: lace curtain half drawn."""
    ppd = p['ppd']; Wd, Hd = p['w'], p['h']; W, H = int(Wd * ppd), int(Hd * ppd); rs = _rs(p); st = p['state']
    if st in ('lit', 'lit2'):
        g = _vgrad(H, W, '#ffd890', '#f0902e') if st == 'lit' else _vgrad(H, W, '#ffe6b0', '#e8742a')
        g = g * (0.85 + 0.3 * pfbm(rs, H, W, 3, 4, 3)[..., None])
    else:
        g = _vgrad(H, W, '#5a64a8', '#324a62'); yy, xx = _grid(H, W, ppd)
        gl = np.clip(1 - np.abs((xx / Wd + yy / Hd * 0.5) % 1.0 - 0.3) / 0.07, 0, 1) * 0.35 + np.clip(1 - np.abs((xx / Wd + yy / Hd * 0.5) % 1.0 - 0.52) / 0.03, 0, 1) * 0.25
        g = g * (0.9 + 0.2 * pfbm(rs, H, W, 3, 4, 3)[..., None]) + gl[..., None] * np.array([0.5, 0.5, 0.65], 'float32')
    im = Image.fromarray((np.clip(g, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im); fw = 0.13 * ppd
    def R(x0, y0, x1, y1, c): d.rectangle([x0 * ppd, (Hd - y1) * ppd, x1 * ppd, (Hd - y0) * ppd], fill=c)
    if st in ('lit', 'lit2'):                                                 # furniture silhouette + a lamp bloom
        R(Wd * 0.12, 0, Wd * 0.45, Hd * 0.32, '#4a2814'); R(Wd * 0.55, 0.0, Wd * 0.62, Hd * 0.5, '#5a3418'); d.ellipse([Wd * 0.5 * ppd, Hd * 0.45 * ppd, Wd * 0.85 * ppd, Hd * 0.62 * ppd], fill='#fff4d0')
    if st == 'curt' or st == 'lit2':
        c = '#efe6d2' if st == 'curt' else '#f4d9a8'
        R(0, 0, Wd * 0.34, Hd, c); R(Wd * 0.66, 0, Wd, Hd, c)
        for k in range(1, 6): R(Wd * 0.34 * k / 6 - 0.02, 0, Wd * 0.34 * k / 6 + 0.02, Hd, '#c8b894'); R(Wd - Wd * 0.34 * k / 6 - 0.02, 0, Wd - Wd * 0.34 * k / 6 + 0.02, Hd, '#c8b894')
    fc = '#ece4cc'; sh = '#a89c80'
    R(0, 0, Wd, 0.1, fc); R(0, Hd - 0.1, Wd, Hd, fc); R(0, 0, 0.1, Hd, fc); R(Wd - 0.1, 0, Wd, Hd, fc)       # outer frame
    R(Wd / 2 - 0.06, 0, Wd / 2 + 0.06, Hd, fc); R(0, Hd * 0.5 - 0.09, Wd, Hd * 0.5 + 0.09, fc)                  # centre stile, meeting rail
    for k in (1, 2):                                                          # glazing bars: 3 panes high per sash
        for h0 in (0.0, 0.5):
            R(0, Hd * (h0 + 0.5 * k / 3) - 0.03, Wd, Hd * (h0 + 0.5 * k / 3) + 0.03, fc)
    R(0.1, Hd * 0.5 + 0.09, Wd - 0.1, Hd * 0.5 + 0.13, sh)
    im.save(out)

def window_top(p, out):
    """window head: segmental arch / pediment cap, cream with a dark underside (separate decal strip above the window)."""
    ppd = p['ppd']; W, H = int(p['w'] * ppd), int(p['h'] * ppd); im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, H], fill=hex8('#ece0c0') + (255,)); d.rectangle([0, H * 0.78, W, H], fill=hex8('#b8a888') + (255,)); im.save(out)

# ----------------------------------------------------------------------------- shop / neighbour facade (whole facade painted)
def facade(p, out):
    """Painted neighbour facade W x H D: brick or clapboard with rows of windows, a shopfront (tall panes, door) on the ground floor.
    p: w, h, floors, bays, kind ('brick'|'clap'), col, trim, ground_h, glow (probability a window is lit), seed."""
    ppd = p['ppd']; Wd, Hd = p['w'], p['h']; W, H = int(Wd * ppd), int(Hd * ppd); rs = _rs(p)
    if p['kind'] == 'brick': col = _brick_arr(rs, H, W, ppd, p['col'], soot=0.35)
    else:
        yy, xx = _grid(H, W, ppd); v = (yy % 0.38) / 0.38; b = hexf(p['col']); col = b * (0.84 + 0.2 * v[..., None] ** 0.5); col = np.where((v < 0.08)[..., None], b * 0.5, col) * (0.92 + 0.12 * pfbm(rs, H, W, 4, 16, 3)[..., None])
    im = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    def R(x0, y0, x1, y1, c): d.rectangle([x0 * ppd, (Hd - y1) * ppd, x1 * ppd, (Hd - y0) * ppd], fill=c)
    trim = p['trim']; gh = p['ground_h']; fl = p['floors']; bays = p['bays']; fh = (Hd - gh - 0.9) / max(1, fl)
    bw = Wd / bays
    for f in range(fl):                                                        # upper floors
        z0 = gh + f * fh
        R(0, z0 - 0.12, Wd, z0 + 0.12, trim)                                    # string course
        for b in range(bays):
            cx = (b + 0.5) * bw; ww = bw * 0.42; wh = fh * 0.62; zb = z0 + fh * 0.18
            lit = rs.rand() < p.get('glow', 0.25)
            g1, g2 = ('#ffd890', '#f09a3a') if lit else ('#58629e', '#304660')
            for i in range(int(wh * ppd)):
                t = i / max(1, wh * ppd); c = tuple(int(a + (b2 - a) * t) for a, b2 in zip(hex8(g1), hex8(g2))); y = (Hd - (zb + wh)) * ppd + i
                d.line([((cx - ww / 2) * ppd, y), ((cx + ww / 2) * ppd, y)], fill=c)
            R(cx - ww / 2 - 0.16, zb + wh, cx + ww / 2 + 0.16, zb + wh + 0.3, trim); R(cx - ww / 2 - 0.2, zb - 0.22, cx + ww / 2 + 0.2, zb, trim)
            R(cx - 0.05, zb, cx + 0.05, zb + wh, trim); R(cx - ww / 2, zb + wh * 0.5 - 0.06, cx + ww / 2, zb + wh * 0.5 + 0.06, trim)
            for k in (1, 2): R(cx - ww / 2, zb + wh * k / 3 * 0.5 - 0.025 + wh * 0.5, cx + ww / 2, zb + wh * k / 3 * 0.5 + 0.025 + wh * 0.5, trim)
    # ground floor: shopfront
    R(0, 0, Wd, 0.5, '#4a3a2c'); R(0, gh, Wd, gh + 0.5, trim)                                   # plinth, fascia
    nd = max(1, bays // 2)
    for b in range(bays):
        cx = (b + 0.5) * bw
        if b == nd:                                                              # door
            R(cx - 0.9, 0.5, cx + 0.9, gh - 0.5, '#3a5a4a' if rs.rand() < 0.5 else '#6a2a24'); R(cx - 0.65, gh * 0.45, cx + 0.65, gh - 0.7, '#caa860'); continue
        w2 = bw * 0.78
        g1, g2 = ('#ffe0a0', '#f0a040') if rs.rand() < p.get('glow', 0.25) + 0.25 else ('#50648a', '#2c4058')
        for i in range(int((gh - 1.3) * ppd)):
            t = i / max(1, (gh - 1.3) * ppd); c = tuple(int(a + (b2 - a) * t) for a, b2 in zip(hex8(g1), hex8(g2))); y = (Hd - (gh - 0.7)) * ppd + i
            d.line([((cx - w2 / 2) * ppd, y), ((cx + w2 / 2) * ppd, y)], fill=c)
        for k in range(1, 4): R(cx - w2 / 2 + w2 * k / 4 - 0.04, 0.8, cx - w2 / 2 + w2 * k / 4 + 0.04, gh - 0.7, trim)
        R(cx - w2 / 2 - 0.1, 0.5, cx + w2 / 2 + 0.1, 0.9, trim)
        for sx in range(3):                                                      # goods on the sill (blobs)
            c = ['#c05a3a', '#e8c060', '#4a8a7a'][sx]; R(cx - w2 / 2 + 0.3 + sx * w2 * 0.28, 0.9, cx - w2 / 2 + 0.7 + sx * w2 * 0.28, 1.5 + 0.4 * (sx % 2), c)
    R(0, Hd - 0.9, Wd, Hd - 0.55, trim)                                          # frieze under the cornice
    im.filter(ImageFilter.GaussianBlur(0.5)).save(out)

# ----------------------------------------------------------------------------- awnings / canvas
def awning(p, out):
    ppd = p['ppd']; W, H = int(p['w'] * ppd), int(p['h'] * ppd); rs = _rs(p); a, b = hexf(p['a']), hexf(p['b'])
    xx = np.arange(W)[None, :] / ppd; s = (np.floor(xx / p['sw']) % 2)[..., None]
    col = np.where(s == 0, a, b) * np.ones((H, 1, 1), 'float32'); col = col * (0.92 + 0.14 * pfbm(rs, H, W, 6, 3, 3)[..., None])
    yy = np.arange(H)[:, None, None] / H; col = col * (0.94 + 0.1 * np.sin(xx[..., None] * 6) * 0.3)
    col[int(H * 0.92):] *= 0.7                                                     # scalloped hem shade
    save(np.clip(col, 0, 1), out)

# ----------------------------------------------------------------------------- interior: wallpaper / parquet / rug / velvet / paintings
def wallpaper(p, out):
    """damask: sage-teal ground, cream lattice of diamonds and leaf blobs, soft vertical stripe; tile 4 x 4 D."""
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); base = hexf(p['col']); ink = hexf(p['ink'])
    col = base[None, None] * (0.94 + 0.12 * pfbm(rs, S, S, 8, 8, 3)[..., None]) * np.ones((S, S, 1), 'float32')
    u = (xx % 1.0); v = (yy % 1.6)
    dia = np.clip(1 - (np.abs(u - 0.5) * 1.7 + np.abs(v - 0.8) * 1.0 - 0.38) / 0.06, 0, 1)
    ring = np.clip(1 - np.abs(np.sqrt((u - 0.5) ** 2 + ((v - 0.8) * 0.62) ** 2) - 0.28) / 0.03, 0, 1)
    blob = np.clip(1 - (np.sqrt((u - 0.5) ** 2 + ((v - 0.8) * 0.8) ** 2) - 0.1) / 0.03, 0, 1)
    pat = np.clip(dia * 0.7 + ring * 0.6 + blob, 0, 1)
    pat = np.maximum(pat, np.clip(1 - (np.sqrt((u % 1.0) ** 2 + (((v + 0.8) % 1.6 - 0.8) * 0.8) ** 2) - 0.08) / 0.03, 0, 1) * 0.9)
    col = col * (1 - pat[..., None] * 0.8) + ink * pat[..., None] * 0.8
    stripe = (np.abs((xx % 1.0) - 0.0) < 0.02); col = np.where(stripe[..., None], col * 0.85, col)
    save(np.clip(col, 0, 1), out)

def parquet(p, out):
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); yy, xx = _grid(S, S, ppd); base = hexf(p['col'])
    cell = 0.9; cx = np.floor(xx / cell); cy = np.floor(yy / cell); sw = ((cx + cy) % 2 == 0); u = xx % cell; v = yy % cell
    t = np.where(sw, v, u); n = 6; strip = np.floor(t / (cell / n)); bid = ((cx * 7 + cy * 3 + strip * 13).astype(int)) % 97; r = rs.rand(97)
    col = base * (0.78 + 0.34 * r[bid][..., None]) * (0.93 + 0.1 * np.sin(np.where(sw, u, v) * 40 + pnoise(rs, S, S, 4, 20) * 6)[..., None] * 0.5 + 0.05)
    g = (t % (cell / n) < 0.02); col = np.where(g[..., None], col * 0.45, col)
    save(np.clip(col, 0, 1), out)

def rug(p, out):
    """oriental rug 7 x 5 D, fine: red field with a lattice of small diamonds and flowers, a teal medallion, 5 border bands with a running key, fringe."""
    ppd = p['ppd']; W, H = int(p['w'] * ppd), int(p['h'] * ppd); rs = _rs(p); yy, xx = _grid(H, W, ppd); Wd, Hd = p['w'], p['h']
    col = np.ones((H, W, 3), 'float32') * hexf('#9c2c2a'); dB = np.minimum(np.minimum(xx, Wd - xx), np.minimum(yy, Hd - yy))
    u = (xx % 0.5) - 0.25; v = (yy % 0.5) - 0.25                                     # lattice of small diamonds
    dia = (np.abs(u) + np.abs(v)) < 0.17; dia2 = (np.abs(u) + np.abs(v)) < 0.09
    col = np.where(dia[..., None], hexf('#d8b86a'), col); col = np.where(dia2[..., None], hexf('#1f5a5c'), col)
    fl = (((xx + 0.25) % 0.5 - 0.25) ** 2 + ((yy + 0.25) % 0.5 - 0.25) ** 2) < 0.012; col = np.where(fl[..., None], hexf('#efe2c0'), col)
    cx, cy = Wd / 2, Hd / 2; dd = np.abs(xx - cx) / 1.7 + np.abs(yy - cy) / 1.2
    for lim, c in ((1.0, '#1f5a5c'), (0.86, '#efe2c0'), (0.72, '#7a1e26'), (0.56, '#d8a848'), (0.4, '#1f5a5c'), (0.24, '#efe2c0'), (0.1, '#9c2c2a')): col = np.where((dd < lim)[..., None], hexf(c), col)
    for lo, hi, c in ((0.0, 0.34, '#efe2c0'), (0.34, 0.46, '#1f5a5c'), (0.46, 0.62, '#c8a050'), (0.62, 0.72, '#7a1e26'), (0.72, 0.84, '#1f5a5c')):
        m = (dB >= lo) & (dB < hi); col = np.where(m[..., None], hexf(c), col)
    run = (dB > 0.04) & (dB < 0.3) & ((((xx + yy) % 0.36) < 0.18)); col = np.where(run[..., None], col * 0.62 + hexf('#7a1e26') * 0.4, col)
    col = col * (0.88 + 0.2 * pfbm(rs, H, W, 60, 40, 3)[..., None]) * (0.95 + 0.07 * np.sin(yy * 220)[..., None]); save(np.clip(col, 0, 1), out)

def velvet(p, out):
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); base = hexf(p['col'])
    n = pfbm(rs, S, S, 12, 12, 4); col = base[None, None] * (0.8 + 0.4 * n[..., None]) * (0.96 + 0.08 * rs.rand(S, S, 1))
    save(np.clip(col, 0, 1), out)

def painting(p, out):
    """Small framed pictures, no text: lake (sea and sails), landscape (hills, trees), still life (jug and fruit), oval portrait silhouette."""
    ppd = p['ppd']; W, H = int(p['w'] * ppd), int(p['h'] * ppd); rs = _rs(p); k = p['kind']; im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
    def Y(f): return int(f * H)
    if k in ('lake', 'land'):
        for i in range(H):
            t = i / H; c = tuple(int(a + (b - a) * min(1, t / 0.55)) for a, b in zip(hex8('#f4c890'), hex8('#7aa0c8'))); d.line([(0, i), (W, i)], fill=c)
        d.rectangle([0, Y(0.62), W, H], fill=hex8('#2e6a8a') if k == 'lake' else hex8('#4a7a3a'))
        if k == 'lake':
            for i in range(Y(0.62), H): t = (i - Y(0.62)) / (H - Y(0.62)); d.line([(0, i), (W, i)], fill=tuple(int(a + (b - a) * t) for a, b in zip(hex8('#6aa8b8'), hex8('#1f4a66'))))
            for sx, sc in ((0.3, 1.0), (0.62, 0.7)):
                x = sx * W; d.polygon([(x, Y(0.62) - 60 * sc), (x, Y(0.62) - 4), (x + 34 * sc, Y(0.62) - 6)], fill=(244, 238, 224)); d.polygon([(x - 2, Y(0.62) - 4), (x - 2, Y(0.62) - 40 * sc), (x - 26 * sc, Y(0.62) - 6)], fill=(230, 220, 200)); d.rectangle([x - 20 * sc, Y(0.62) - 6, x + 30 * sc, Y(0.62)], fill=(90, 50, 36))
        else:
            d.polygon([(0, Y(0.62)), (W * 0.3, Y(0.4)), (W * 0.65, Y(0.58)), (W, Y(0.44)), (W, Y(0.7)), (0, Y(0.7))], fill=hex8('#5a8a6a'))
            for tx in (0.2, 0.72, 0.85):
                x = tx * W; d.rectangle([x - 3, Y(0.62), x + 3, Y(0.8)], fill=(80, 54, 36)); d.ellipse([x - 22, Y(0.44), x + 22, Y(0.72)], fill=(52, 100, 64))
        d.ellipse([W * 0.7, Y(0.18), W * 0.7 + 34, Y(0.18) + 34], fill=(255, 236, 170))
    elif k == 'still':
        d.rectangle([0, 0, W, H], fill=hex8('#4a2e3a')); d.rectangle([0, Y(0.72), W, H], fill=hex8('#8a5a36'))
        d.ellipse([W * 0.3, Y(0.3), W * 0.52, Y(0.78)], fill=hex8('#3e7a7a')); d.rectangle([W * 0.36, Y(0.2), W * 0.46, Y(0.4)], fill=hex8('#3e7a7a'))
        for i, c in enumerate(('#d8582e', '#e8b838', '#a83a3a')): d.ellipse([W * (0.56 + 0.1 * i), Y(0.62 - 0.02 * i), W * (0.56 + 0.1 * i) + 40, Y(0.62 - 0.02 * i) + 40], fill=hex8(c))
    else:
        d.rectangle([0, 0, W, H], fill=hex8('#3a3a52')); d.ellipse([W * 0.28, Y(0.12), W * 0.72, Y(0.55)], fill=hex8('#e4b896')); d.polygon([(W * 0.1, H), (W * 0.2, Y(0.62)), (W * 0.8, Y(0.62)), (W * 0.9, H)], fill=hex8('#22242e'))
        d.ellipse([W * 0.26, Y(0.06), W * 0.74, Y(0.3)], fill=hex8('#5a3a2a'))
    arr = np.asarray(im).astype('float32') / 255; arr = arr * (0.9 + 0.2 * pfbm(rs, H, W, 20, 20, 3)[..., None]); save(np.clip(arr, 0, 1), out)

def frame_gold(p, out):
    ppd = 40; S = 160; rs = _rs(p); base = hexf('#d4a640'); n = pfbm(rs, S, S, 8, 8, 3)
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / S; col = base * (0.75 + 0.25 * np.sin(xx * 40 * 3.14) ** 2 + 0.2 * n)[..., None]; save(np.clip(col, 0, 1), out)

def lace(p, out):
    pass


def thread_tex(p, out):
    """screw thread: horizontal dark grooves on mid-grey iron (v along the screw); tile 1 x 1 (u around, v repeats via uv_wrap)."""
    S = 128; rs = _rs(p); yy = np.linspace(0, 1, S, dtype='float32')[:, None]; xx = np.linspace(0, 1, S, dtype='float32')[None, :]
    g = np.sin((yy * 8 + xx * 0.9) * 2 * math.pi) * 0.5 + 0.5; base = hexf('#5c606c')
    col = base[None, None] * (0.55 + 0.7 * g[..., None]) * (0.9 + 0.2 * pfbm(rs, S, S, 4, 4, 3)[..., None]); save(np.clip(col, 0, 1), out)

def scum(p, out):
    """floating scum / soft foam on puddles: alpha blotches of pale tan-grey, tileable 12 x 12 D."""
    ppd = p['ppd']; S = int(12 * ppd); rs = _rs(p); n = pfbm(rs, S, S, 9, 9, 5); n2 = pfbm(rs, S, S, 30, 30, 3)
    a = np.clip((n - 0.52) * 7, 0, 1) * np.clip(0.55 + n2, 0, 1) ; a = np.clip(a, 0, 0.92)
    col = hexf('#cdbf9f')[None, None] * (0.85 + 0.25 * n2[..., None]) * np.ones((S, S, 3), 'float32'); save(np.clip(col, 0, 1), out, alpha=a)

def sky_plain(p, out):
    WX.sky(dict(p, mode=p['base']), out)

# ----------------------------------------------------------------------------- distant skyline ring
def pano_chi(p, out):
    """Backdrop ring: flat-toned roofs, chimneys, gables, a flat green-grey prairie, a lake strip with sails and a smoke wisp, in warm
    haze (u 0..1 = azimuth from +x CCW; the ring spans z PANO_Z0..PANO_Z1 at PANO_R)."""
    ppd = p['ppd']; W = int(360 * ppd * 1.0); H = int(W * (PANO_Z1 - PANO_Z0) / (2 * math.pi * PANO_R)); rs = np.random.RandomState(5)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); gy = int(H * (PANO_Z1 - 0) / (PANO_Z1 - PANO_Z0))
    def Z(z): return gy - int(z / (PANO_Z1 - PANO_Z0) * H)
    px = W / 360.0
    d.rectangle([0, Z(0.6), W, H], fill=hex8('#a6a07a') + (255,))
    lake = (int(20 * px), int(95 * px))                                          # the lake lies at azimuth 20..95 deg
    d.rectangle([lake[0], Z(1.6), lake[1], Z(0.5)], fill=hex8('#7a9ec8') + (255,))
    for _ in range(10):
        x = rs.uniform(*lake); h = rs.uniform(2.5, 5.5); d.polygon([(x, Z(1.6) - 2), (x, Z(1.6 + h)), (x + 9, Z(1.7))], fill=(240, 232, 218, 255)); d.line([(x - 3, Z(1.55)), (x + 8, Z(1.55))], fill=(70, 60, 60, 255), width=3)
    col_far = hex8('#b9a2b4'); col_near = hex8('#9c7e9a')
    for layer, (col, zmax, n) in enumerate(((col_far, 9.0, 240), (col_near, 7.0, 190))):
        x = 0.0
        while x < W:
            w = rs.uniform(1.2, 4.2) * px; h = rs.uniform(1.8, zmax); x0 = x
            if lake[0] < x0 < lake[1]: x += w; continue
            d.rectangle([x0, Z(h), x0 + w, Z(0.4)], fill=col + (255,))
            if rs.rand() < 0.5: d.polygon([(x0 - 1, Z(h)), (x0 + w / 2, Z(h + w / px * 0.7)), (x0 + w + 1, Z(h))], fill=tuple(int(c * 0.9) for c in col) + (255,))
            if rs.rand() < 0.35: cx = x0 + rs.uniform(0.2, 0.8) * w; d.rectangle([cx, Z(h + 2.2), cx + 2, Z(h)], fill=tuple(int(c * 0.8) for c in col) + (255,))
            x += w * rs.uniform(0.9, 1.15)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    a = np.asarray(im).astype('float32') / 255; yy = np.linspace(0, 1, H)[:, None, None]
    haze = hexf('#f0cfc0')[None, None] * (0.28 + 0.34 * np.clip((yy - 0.5) * 2, 0, 1)); a[..., :3] = a[..., :3] * (1 - haze * 0.5) + haze * 0.5
    save(a[..., :3], out, alpha=a[..., 3])

def far_ground(p, out):
    ppd = p['ppd']; S = int(p['size'] * ppd); rs = _rs(p); n = pfbm(rs, S, S, 8, 8, 5); col = hexf('#8c8a5a')[None, None] * (0.8 + 0.4 * n[..., None]); save(np.clip(col, 0, 1), out)

# ----------------------------------------------------------------------------- jobs
def all_jobs():
    JOBS.clear()
    for nm, c in (('brick_a', '#b45238'), ('brick_b', '#a14a38'), ('brick_c', '#b86a40'), ('brick_d', '#8a4638'), ('brick_e', '#c05a3c')):
        reg(nm, dict(size=6, ppd=36, col=c, seed=hash_s(nm), soot=0.25), brick_tile)
    reg('ash', dict(kind='ash', size=8, ppd=32, col='#eadcb8', seed=3), stone_tile); reg('rustic', dict(kind='rust', size=8, ppd=32, col='#d8c8a2', seed=5), stone_tile)
    reg('stone_grey', dict(kind='ash', size=8, ppd=32, col='#aaa296', seed=7), stone_tile)
    reg('plank_walk', dict(size=8, ppd=40, w=0.55, col='#a98258', seed=9, nails=1, len=5.0), planks)
    reg('plank_dark', dict(size=8, ppd=40, w=0.4, col='#6c5036', seed=10, len=3.0), planks)
    reg('plank_floor', dict(size=8, ppd=40, w=0.5, col='#8a5e38', seed=11, len=6.0), planks)
    reg('crate', dict(size=4, ppd=48, w=0.5, col='#b88a52', seed=12, len=2.0), planks)
    reg('timber', dict(size=8, ppd=36, col='#a88455', seed=14), timber); reg('timber_d', dict(size=8, ppd=36, col='#6a4c30', seed=15), timber)
    reg('timber_w', dict(size=8, ppd=36, col='#c19a62', seed=16), timber)
    for nm, c in (('clap_ochre', '#d8a548'), ('clap_teal', '#3f8a80'), ('clap_cream', '#e4d6b2'), ('clap_green', '#5e8a52')): reg(nm, dict(size=8, ppd=32, col=c, seed=hash_s(nm)), clap)
    reg('mud', dict(size=10, ppd=36, col='#6c5d4a', seed=21, straw=200, hoof=40, dry='#8a7656'), mud)
    reg('mud_wet', dict(size=10, ppd=36, col='#3e362e', seed=22, straw=30, hoof=20, dry='#54483a'), mud)
    reg('clay', dict(size=8, ppd=36, col='#8e7050', seed=23), earth); reg('gravel', dict(size=8, ppd=36, col='#9a8c78', seed=24), earth)
    for st, (w, h) in (('dark', (2.2, 3.7)), ('lit', (2.2, 3.7)), ('curt', (2.2, 3.7)), ('lit2', (2.2, 3.7))):
        reg('win_' + st, dict(w=w, h=h, ppd=64, state=st, seed=4), window)
    reg('win_dark_short', dict(w=2.2, h=3.0, ppd=64, state='dark', seed=6), window); reg('win_lit_short', dict(w=2.2, h=3.0, ppd=64, state='lit', seed=7), window)
    reg('win_dark_big', dict(w=2.6, h=4.9, ppd=64, state='dark', seed=8), window); reg('win_lit_big', dict(w=2.6, h=4.9, ppd=64, state='lit2', seed=9), window)
    reg('win_dark_base', dict(w=1.6, h=1.5, ppd=64, state='dark', seed=10), window)
    reg('fac_a', dict(w=26.0, h=17.0, floors=3, bays=5, kind='brick', col='#b8623e', trim='#e6d6b0', ground_h=4.4, glow=0.3, ppd=36, seed=31), facade)
    reg('fac_b', dict(w=20.0, h=14.0, floors=2, bays=4, kind='clap', col='#e0b04c', trim='#f0e6c8', ground_h=4.4, glow=0.35, ppd=36, seed=32), facade)
    reg('fac_c', dict(w=24.0, h=21.0, floors=4, bays=5, kind='brick', col='#9a4a3a', trim='#d8cbb0', ground_h=4.6, glow=0.3, ppd=34, seed=33), facade)
    reg('fac_d', dict(w=18.0, h=15.0, floors=3, bays=4, kind='clap', col='#3f8a80', trim='#efe4c4', ground_h=4.4, glow=0.3, ppd=36, seed=34), facade)
    reg('fac_e', dict(w=22.0, h=18.0, floors=3, bays=4, kind='brick', col='#c07a46', trim='#e8dcb8', ground_h=4.6, glow=0.3, ppd=36, seed=35), facade)
    reg('fac_f', dict(w=16.0, h=12.5, floors=2, bays=3, kind='clap', col='#5e8a52', trim='#eee2c0', ground_h=4.4, glow=0.3, ppd=36, seed=36), facade)
    reg('awn_rc', dict(w=8, h=2, ppd=40, a='#c0432e', b='#efe2c4', sw=0.55, seed=1), awning); reg('awn_tc', dict(w=8, h=2, ppd=40, a='#2f8a82', b='#efe2c4', sw=0.55, seed=2), awning)
    reg('awn_oc', dict(w=8, h=2, ppd=40, a='#d89a30', b='#efe2c4', sw=0.55, seed=3), awning)
    reg('wallpaper', dict(size=4, ppd=64, col='#5f8f7e', ink='#e6d8a8', seed=41), wallpaper)
    reg('parquet', dict(size=8, ppd=40, col='#a06a3c', seed=42), parquet)
    reg('rug', dict(w=7.0, h=5.0, ppd=96, seed=43), rug)
    reg('velvet_red', dict(size=2, ppd=64, col='#8a2038', seed=44), velvet); reg('velvet_teal', dict(size=2, ppd=64, col='#1f6a6a', seed=45), velvet)
    for k, (w, h) in (('lake', (3.0, 2.2)), ('land', (2.2, 3.0)), ('still', (2.6, 2.0)), ('portrait', (1.8, 2.4))): reg('paint_' + k, dict(w=w, h=h, ppd=70, kind=k, seed=50), painting)
    reg('frame_gold', dict(seed=3), frame_gold)
    reg('pano_CHI', dict(ppd=10), pano_chi); reg('far_ground', dict(size=16, ppd=16, seed=61), far_ground)
    reg('thread', dict(seed=1), thread_tex); reg('scum', dict(ppd=24, seed=71), scum)
    reg('rain_near', dict(seed=54, n=170, len=(70, 150), val=(110, 200), w=(1.4, 2.4), blur=0.8), WX.rain_screen); reg('rain_far', dict(seed=56, n=1100, len=(14, 40), val=(80, 190), w=(0.8, 1.3), blur=0.3), WX.rain_screen)
    reg('sky_CH_RAIN', dict(base='RAIN', sun=(325.0, 50.0), w=WX.SKY_W, seed=5), sky_plain)
    reg('sky_CH_MORN', dict(base='DAWNG', sun=(335.0, 17.0), w=WX.SKY_W, seed=23, cloud=('#f8d6b4', '#ffe6a8', '#c4a8c4'), haze='#ffe0b8'), HX.sky_rich)
    reg('sky_CH_DAY', dict(base='DAY', sun=SUN_DAY, w=WX.SKY_W, seed=21, cloud=('#f0c8b8', '#ffe0a0', '#b6a2cc'), haze='#f6dcbc'), HX.sky_rich)

def hash_s(s): return int(hashlib.sha1(s.encode()).hexdigest()[:6], 16)

def ensure(verbose=True):
    os.makedirs(TEX, exist_ok=True); all_jobs()
    mpath = os.path.join(TEX, 'manifest.json')
    try: man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    except ValueError: man = {}
    man0 = dict(man); out = {}
    for name, (params, fn) in JOBS.items():
        ver = WX.TEX_V + HX.TEX_V + TEX_V if fn in (HX.sky_rich, sky_plain) else TEX_V
        h = hashlib.sha1((ver + fn.__name__ + json.dumps(params, sort_keys=True, default=str)).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            fn(params, png); man[name] = h
            if verbose: print('painted', name, flush=True)
    if man != man0:
        tmp = '%s.%d.tmp' % (mpath, os.getpid()); json.dump(man, open(tmp, 'w'), indent=0, sort_keys=True); os.replace(tmp, mpath)
    for nm in ('pool', 'shaft', 'glint', 'wisp'): out[nm] = os.path.join(DESERT_TEX, nm + '.png')
    return out

if __name__ == '__main__':
    p = ensure(); print(len(p), 'textures')
