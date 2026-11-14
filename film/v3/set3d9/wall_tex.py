#!/usr/bin/env python3
"""wall_tex.py : artwork of the film-9 set (Ming city wall under construction, ~1370s).
Everything is painted with numpy + PIL (supersampled, deterministic: fixed seeds) and cached in v3/set3d9/tex_wall/ by a hash
of the painter's parameters + TEX_V. Skies use the sky-dome UV of louvre._sky_dome / desert (u = azimuth / 360 from +x CCW,
v = (elevation + 15) / 105) and desert_tex's periodic fbm; the painted ring has desert_tex.PANO_R / PANO_Z0 / PANO_Z1.
Shared glow images (pool, shaft, glint) are read from v3/set3d8/tex_desert (not copied).

    import wall_tex as WT
    tx = WT.ensure()           # {name: png path}
"""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np                                              # noqa: E402
from PIL import Image, ImageDraw, ImageFilter                    # noqa: E402

TEX = os.path.join(HERE, 'tex_wall')
DESERT_TEX = os.path.join(PROJ, 'v3', 'set3d8', 'tex_desert')
TEX_V = 'w9.6'
PANO_R = 120.0; PANO_Z0, PANO_Z1 = -1.5, 34.0                   # = desert_tex (desert._sky builds the ring with these)
JOBS = {}

def hexf(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], 'float32')
def hex8(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def pnoise(rs, H, W, cx, cy):
    """Periodic (both axes) smooth value noise in [0, 1]: a cy x cx random grid, wrapped, bicubic."""
    g = rs.rand(cy, cx).astype('float32'); p = 3
    gp = np.pad(g, p, mode='wrap')
    big = np.asarray(Image.fromarray(gp, 'F').resize((int(round(W * (cx + 2 * p) / cx)), int(round(H * (cy + 2 * p) / cy))), Image.BICUBIC))
    oy, ox = int(round(H * p / cy)), int(round(W * p / cx))
    return big[oy:oy + H, ox:ox + W]

def pfbm(rs, H, W, cx, cy, oct_=4):
    a = np.zeros((H, W), 'float32'); amp = 1.0; tot = 0.0
    for k in range(oct_): a += amp * pnoise(rs, H, W, cx << k, cy << k); tot += amp; amp *= 0.5
    return a / tot

def save(arr, out, alpha=None):
    a = np.clip(arr, 0, 1)
    if alpha is not None:
        im = np.concatenate([a, np.clip(alpha, 0, 1)[..., None]], 2); Image.fromarray((im * 255 + 0.5).astype('uint8'), 'RGBA').save(out)
    else: Image.fromarray((a * 255 + 0.5).astype('uint8'), 'RGB').save(out)

def reg(name, params, fn): JOBS[name] = (params, fn)

# ============================================================================= bricks
def brick(p, out):
    """4 x 4 D wall tile: 8 courses of 0.5 D, bricks 4/3 D long in running bond. kind 'plain': thin cool grey cement-like mortar
    (recessed: shadow line above, light line below); 'rice': thick creamy ivory sticky-rice mortar, slightly squeezed out (round
    beads proud of the face, soft sheen); 'old': weathered darker bricks with dirt / moss streaks. Also writes <name>_mask.png
    (white = mortar) for the wet / gloss hooks."""
    ppd = p['ppd']; S = int(4 * ppd); rs = np.random.RandomState(p['seed']); kind = p['kind']
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd                     # D units, y down from the tile top
    course = np.floor(yy / 0.5); off = (course % 2) * (2 / 3.0); L = 4 / 3.0
    bx = np.floor((xx + off) / L) % 3; bid = (course * 3 + bx).astype(int)
    u = ((xx + off) % L); v = yy % 0.5
    mw = p['mw']; dist = np.minimum(np.minimum(u, L - u), np.minimum(v, 0.5 - v))
    rnd = rs.rand(64, 4)
    base = hexf(p['brick']); var = np.stack([rnd[bid % 64, 0], rnd[bid % 64, 1], rnd[bid % 64, 2]], -1)
    col = base[None, None, :] * (0.86 + 0.24 * var[..., :1]) + (var[..., 1:2] - 0.5) * np.array([0.03, 0.0, -0.03], 'float32') * 2
    if kind == 'old': col = col * (0.82 + 0.1 * var[..., 2:3])
    n1 = pfbm(rs, S, S, 8, 8, 4); n2 = pnoise(rs, S, S, 64, 64)
    col = col * (0.9 + 0.18 * n1[..., None]) * (0.95 + 0.1 * n2[..., None])
    pits = (pnoise(rs, S, S, 96, 96) > 0.82).astype('float32') * 0.12; col = col * (1 - pits[..., None])
    edge = np.clip(1 - (dist - mw / 2) / 0.05, 0, 1); col = col * (1 - 0.18 * edge[..., None])  # darker brick edges
    jitter = (pnoise(rs, S, S, 40, 40) - 0.5) * (0.02 if kind != 'rice' else 0.035)
    mort = (dist + jitter < mw / 2).astype('float32')
    mcol = hexf(p['mortar'])[None, None, :] * (0.92 + 0.12 * pnoise(rs, S, S, 48, 48)[..., None])
    if kind == 'rice':
        bead = np.clip(1 - np.abs(dist + jitter) / (mw / 2 + 1e-4), 0, 1)                     # rounded bead: light at its crest
        mcol = mcol * (0.9 + 0.16 * bead[..., None]) + 0.05 * (bead[..., None] ** 6)
        sq = (pnoise(rs, S, S, 30, 30) > 0.72).astype('float32') * np.clip(1 - (dist - mw / 2) / 0.05, 0, 1)   # squeeze-out lumps
        mort = np.maximum(mort, sq)
        grains = (pnoise(rs, S, S, 160, 160) > 0.86).astype('float32') * mort; mcol = mcol + 0.05 * grains[..., None]
        smear = np.clip((pfbm(rs, S, S, 12, 12, 3) - 0.5) * 3, 0, 1) * np.clip(1 - (dist - mw / 2) / 0.12, 0, 1) * 0.55
        col = col * (1 - smear[..., None]) + smear[..., None] * hexf('#e8dcc0')
    else:
        top = ((v < mw / 2 + 0.012) & (v > mw / 2 - 0.02) & (u > mw / 2) & (u < L - mw / 2)).astype('float32')
        col = col * (1 - 0.25 * top[..., None])
        mcol = mcol * (1 - 0.28 * ((v < mw / 4) | (v > 0.5 - mw / 4)).astype('float32')[..., None] * (dist < mw / 2)[..., None])
    img = col * (1 - mort[..., None]) + mcol * mort[..., None]
    if kind == 'old':                                                       # dirt streaks from the top, moss low
        st = pnoise(rs, S, S, 24, 2) ; streak = np.clip((st - 0.55) * 3, 0, 1) * 0.25
        img = img * (1 - streak[..., None]) + streak[..., None] * hexf('#3a3630')
        moss = np.clip((pfbm(rs, S, S, 6, 6, 3) - 0.62) * 4, 0, 1) * mort * 0.8
        img = img * (1 - moss[..., None]) + moss[..., None] * hexf('#5a6a32')
    save(img, out)
    Image.fromarray((np.clip(mort, 0, 1) * 255).astype('uint8'), 'L').save(out[:-4] + '_mask.png')

def stone(p, out):
    """Plinth / gate stone: 4 x 2 D tile of large grey granite ashlar blocks (2 rows of 1 D)."""
    ppd = p['ppd']; W, H = int(4 * ppd), int(2 * ppd); rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:H, 0:W].astype('float32') / ppd
    row = np.floor(yy / 1.0); off = (row % 2) * 1.1; L = 2.0
    bid = (row * 7 + np.floor((xx + off) / L)).astype(int) % 32
    u = (xx + off) % L; v = yy % 1.0; d = np.minimum(np.minimum(u, L - u), np.minimum(v, 1 - v))
    rnd = rs.rand(32)
    col = hexf(p['col'])[None, None, :] * (0.85 + 0.25 * rnd[bid][..., None])
    col = col * (0.85 + 0.25 * pfbm(rs, H, W, 12, 6, 4)[..., None]) * (1 - 0.15 * (pnoise(rs, H, W, 140, 70) > 0.8)[..., None])
    col = col * (1 - 0.25 * np.clip(1 - (d - 0.02) / 0.06, 0, 1)[..., None])
    img = np.where((d < 0.025)[..., None], hexf('#5a5852'), col); save(img, out)

def earth(p, out):
    """Ground tile 4 x 4 D: packed earth (site) / field grass, with straw, pebbles, lime splashes or grass tufts."""
    ppd = p['ppd']; S = int(4 * ppd); rs = np.random.RandomState(p['seed'])
    n = pfbm(rs, S, S, 6, 6, 5); n2 = pnoise(rs, S, S, 80, 80)
    a, b = hexf(p['a']), hexf(p['b'])
    img = a[None, None] * (1 - n[..., None]) + b[None, None] * n[..., None]
    img = img * (0.92 + 0.14 * n2[..., None])
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im); r = rs
    for _ in range(p.get('straw', 0)):
        x, y = r.rand() * S, r.rand() * S; ang = r.rand() * math.pi; l = (0.08 + 0.18 * r.rand()) * ppd
        d.line([(x, y), (x + l * math.cos(ang), y + l * math.sin(ang))], fill=hex8(p.get('straw_c', '#d8c070')), width=max(1, int(0.012 * ppd)))
    for _ in range(p.get('pebbles', 0)):
        x, y = r.rand() * S, r.rand() * S; rr = (0.012 + 0.03 * r.rand()) * ppd; c = int(100 + 60 * r.rand())
        d.ellipse([x - rr, y - rr * 0.7, x + rr, y + rr * 0.7], fill=(c, c - 6, c - 14))
    for _ in range(p.get('lime', 0)):
        x, y = r.rand() * S, r.rand() * S; rr = (0.05 + 0.2 * r.rand()) * ppd
        d.ellipse([x - rr, y - rr * 0.6, x + rr, y + rr * 0.6], fill=(226, 222, 206))
    for _ in range(p.get('specks', 0)):
        x, y = r.rand() * S, r.rand() * S; rr = (0.02 + 0.05 * r.rand()) * ppd
        d.ellipse([x - rr, y - rr * 0.6, x + rr, y + rr * 0.6], fill=(196, 188, 170))
    for _ in range(p.get('tufts', 0)):
        x, y = r.rand() * S, r.rand() * S; c = hex8(p.get('tuft_c', '#6a8a30'))
        for k in range(5):
            ang = -math.pi / 2 + (r.rand() - 0.5) * 1.6; l = (0.06 + 0.1 * r.rand()) * ppd
            d.line([(x, y), (x + l * math.cos(ang), y + l * math.sin(ang))], fill=c, width=max(1, int(0.015 * ppd)))
    im.save(out)

def paste(p, out):
    """Paste surfaces 2 x 2 D: lime putty, plain mortar, rice mortar (creamy, glossy swirls), rice soup (milky with grains, bubbles)."""
    ppd = p['ppd']; S = int(2 * ppd); rs = np.random.RandomState(p['seed'])
    n = pfbm(rs, S, S, 4, 4, 5); sw = np.sin((n * 14.0) + pnoise(rs, S, S, 6, 6) * 6)
    img = hexf(p['col'])[None, None] * (0.9 + 0.08 * sw[..., None] + 0.08 * n[..., None])
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(im)
    for _ in range(p.get('grains', 0)):
        x, y = rs.rand() * S, rs.rand() * S; ang = rs.rand() * math.pi; l = 0.035 * ppd
        d.line([(x, y), (x + l * math.cos(ang), y + l * math.sin(ang))], fill=(250, 248, 238), width=max(2, int(0.018 * ppd)))
    for _ in range(p.get('bubbles', 0)):
        x, y = rs.rand() * S, rs.rand() * S; rr = (0.02 + 0.06 * rs.rand()) * ppd
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(255, 255, 250), width=max(1, int(0.01 * ppd)))
    im.save(out)

def tiles(p, out):
    """Chinese roof: rows of grey barrel tiles 2 x 2 D (rows run along u)."""
    ppd = p['ppd']; S = int(2 * ppd); rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    ph = (xx % 0.25) / 0.25; prof = np.sin(ph * math.pi)
    v = (yy % 0.33) / 0.33
    col = hexf(p['col'])[None, None] * (0.6 + 0.5 * prof[..., None]) * (0.85 + 0.2 * (1 - v)[..., None])
    col = col * (0.9 + 0.15 * pnoise(rs, S, S, 10, 10)[..., None]); save(col, out)

def canvas(p, out):
    """Tent / awning cloth 2 x 2 D with stripes and patches."""
    ppd = p['ppd']; S = int(2 * ppd); rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    a, b = hexf(p['a']), hexf(p['b']); st = ((xx % 0.5) < 0.12).astype('float32') * p.get('stripe', 1.0)
    img = a[None, None] * (1 - st[..., None]) + b[None, None] * st[..., None]
    img = img * (0.9 + 0.12 * pfbm(rs, S, S, 4, 4, 4)[..., None])
    img = img * (1 - 0.06 * (np.sin(yy * 60) * 0.5 + 0.5)[..., None]); save(img, out)

def banner(p, out):
    """Vertical war banner 1 x 3 D (alpha): field colour, a border, a swallowtail end, a round emblem (sun disc / tiger stripes)."""
    ppd = p['ppd']; W, H = int(1 * ppd), int(3 * ppd); ss = 3
    im = Image.new('RGBA', (W * ss, H * ss), (0, 0, 0, 0)); d = ImageDraw.Draw(im); s = ppd * ss
    f, b, e = hex8(p['field']), hex8(p['border']), hex8(p['emblem'])
    poly = [(0, 0), (1 * s, 0), (1 * s, 2.7 * s), (0.5 * s, 2.45 * s), (0, 2.7 * s)]
    d.polygon(poly, fill=b + (255,))
    inner = [(0.08 * s, 0.08 * s), (0.92 * s, 0.08 * s), (0.92 * s, 2.55 * s), (0.5 * s, 2.32 * s), (0.08 * s, 2.55 * s)]
    d.polygon(inner, fill=f + (255,))
    for k in range(9):                                                      # border teeth
        y = 0.2 * s + k * 0.25 * s; d.polygon([(0.08 * s, y), (0.2 * s, y + 0.1 * s), (0.08 * s, y + 0.2 * s)], fill=b + (255,)); d.polygon([(0.92 * s, y), (0.8 * s, y + 0.1 * s), (0.92 * s, y + 0.2 * s)], fill=b + (255,))
    cx, cy, R = 0.5 * s, 0.85 * s, 0.3 * s
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=e + (255,)); d.ellipse([cx - R * 0.72, cy - R * 0.72, cx + R * 0.72, cy + R * 0.72], fill=f + (255,))
    if p.get('motif') == 'tiger':
        for k in range(5): d.polygon([(cx - R * 0.5 + k * R * 0.25, cy - R * 0.55), (cx - R * 0.38 + k * R * 0.25, cy), (cx - R * 0.5 + k * R * 0.25, cy + R * 0.55)], fill=e + (255,))
    else:
        d.ellipse([cx - R * 0.42, cy - R * 0.42, cx + R * 0.42, cy + R * 0.42], fill=e + (255,))
    for k in range(3): d.rectangle([0.3 * s, 1.45 * s + k * 0.22 * s, 0.7 * s, 1.52 * s + k * 0.22 * s], fill=e + (230,))
    im.resize((W, H), Image.LANCZOS).save(out)

def lantern(p, out):
    """Chinese paper lantern skin 1 x 1 (wraps round): red paper glowing bright in the middle, darker ribs, gold bands top/bottom."""
    W, H = 128, 128; yy, xx = np.mgrid[0:H, 0:W].astype('float32') / H
    c = hexf(p['col']); glow = np.sin(np.clip(yy, 0, 1) * math.pi) ** 0.6
    img = c[None, None] * (0.55 + 0.75 * glow[..., None]) + np.array([0.25, 0.18, 0.05], 'float32') * (glow[..., None] ** 4)
    ribs = (np.abs(((xx * 12) % 1.0) - 0.5) < 0.06).astype('float32'); img = img * (1 - 0.35 * ribs[..., None])
    band = ((yy < 0.09) | (yy > 0.91)).astype('float32'); img = img * (1 - band[..., None]) + band[..., None] * hexf('#d8a030')
    tas = ((yy > 0.42) & (yy < 0.58) & (np.abs(xx - 0.25) < 0.08)).astype('float32') * 0.0
    save(img, out)

# ============================================================================= cracks, dents, drips (overlays)
def _walk(rs, x, y, ang, length, step, bias_h=0.0, wiggle=0.35):
    pts = [(x, y)]; L = 0.0
    while L < length:
        ang += rs.normal(0, wiggle)
        if bias_h: ang = ang * (1 - bias_h) + bias_h * (0.0 if math.cos(ang) > 0 else math.pi)
        x += step * math.cos(ang); y += step * math.sin(ang); pts.append((x, y)); L += step
    return pts

def cracks(p, out):
    """Crack overlay of a wall section face (W x H D, origin bottom-left = section x0, plinth top). Writes <name>.png (RGBA: dark
    crack core, light chipped lip, alpha) and <name>_ord.png (L: reveal order 0..1 along each crack from its impact; set_cracks
    shows a pixel when order <= level). general: shot 1 star (0.02..0.33), shot 2 long cracks along the courses across the whole
    row (0.34..0.66), shot 3 a network through the slab (0.67..1). lin: only short hairlines round the dents."""
    W, H, ppd = p['W'], p['H'], p['ppd']; ss = 2; s = ppd * ss; Wp, Hp = int(W * s), int(H * s); rs = np.random.RandomState(p['seed'])
    core = Image.new('L', (Wp, Hp), 0); lip = Image.new('L', (Wp, Hp), 0); order = Image.new('L', (Wp, Hp), 255)
    dc, dl, do = ImageDraw.Draw(core), ImageDraw.Draw(lip), ImageDraw.Draw(order)
    def P(x, z): return (x * s, (H - z) * s)
    def draw(pts, o0, o1, w0, w1):
        n = len(pts) - 1
        for i in range(n):
            t = i / max(1, n); w = (w0 + (w1 - w0) * t) * s * p.get('wk', 1.0); o = o0 + (o1 - o0) * t
            a, b = P(*pts[i]), P(*pts[i + 1])
            dl.line([a, b], fill=255, width=max(1, int(w * 3.0))); dc.line([a, b], fill=255, width=max(2, int(w)))
            do.line([a, b], fill=int(o * 254), width=max(1, int(w * 3.2)))
    imp = p['impacts']
    if p['kind'] == 'general':
        x, z = imp[0]                                                        # shot 1: a star
        for k in range(9):
            a = 2 * math.pi * k / 9 + rs.uniform(-0.2, 0.2); pts = _walk(rs, x, z, a, rs.uniform(1.5, 4.0), 0.12)
            draw(pts, 0.02, 0.30, 0.09, 0.02)
            if k % 2 == 0:
                q = pts[len(pts) // 2]; draw(_walk(rs, q[0], q[1], a + rs.choice((-0.8, 0.8)), rs.uniform(0.8, 1.6), 0.1), 0.18, 0.33, 0.04, 0.015)
        x, z = imp[1]                                                        # shot 2: long cracks along the courses, end to end
        for k in range(4):
            zz = z + (k - 1.5) * 0.9 + rs.uniform(-0.2, 0.2)
            for dirn in (0.0, math.pi):
                pts = [(x, zz)]; cx_, cz_ = x, zz
                while 0.2 < cx_ < W - 0.2:
                    cx_ += math.cos(dirn) * rs.uniform(0.3, 0.9)
                    if rs.rand() < 0.35: cz_ += rs.choice((-0.5, 0.5))      # stair-steps up / down a course
                    pts.append((cx_, cz_ + rs.uniform(-0.05, 0.05)))
                draw(pts, 0.34, 0.64, 0.08, 0.035)
        for k in range(8):
            a = 2 * math.pi * k / 8; draw(_walk(rs, x, z, a, rs.uniform(1.0, 2.5), 0.12), 0.34, 0.5, 0.08, 0.02)
        x, z = imp[2]                                                        # shot 3: the whole slab breaks up
        for k in range(26):
            sx, sz = rs.uniform(0.5, W - 0.5), rs.uniform(0.3, H - 0.5)
            draw(_walk(rs, sx, sz, rs.uniform(0, 2 * math.pi), rs.uniform(2.0, 6.0), 0.15, wiggle=0.5), 0.67 + 0.25 * rs.rand(), 0.98, 0.09, 0.03)
        for k in range(10):
            a = 2 * math.pi * k / 10; draw(_walk(rs, x, z, a, rs.uniform(3, 7), 0.15), 0.67, 0.95, 0.12, 0.04)
    else:
        for (x, z) in imp:                                                   # rice mortar: only short hairlines round each dent
            for k in range(6):
                a = 2 * math.pi * k / 6 + rs.uniform(-0.3, 0.3); r0 = 0.55
                pts = _walk(rs, x + r0 * math.cos(a), z + r0 * math.sin(a), a, rs.uniform(0.25, 0.7), 0.06, wiggle=0.5)
                draw(pts, 0.1, 0.6, 0.025, 0.01)
    core = np.asarray(core.resize((int(W * ppd), int(H * ppd)), Image.LANCZOS)).astype('float32') / 255
    lipa = np.asarray(lip.filter(ImageFilter.GaussianBlur(ss)).resize((int(W * ppd), int(H * ppd)), Image.LANCZOS)).astype('float32') / 255
    ordm = np.asarray(order.filter(ImageFilter.MinFilter(3)).resize((int(W * ppd), int(H * ppd)), Image.NEAREST)).astype('float32') / 255
    rgb = hexf('#ece6d8')[None, None] * (1 - core[..., None]) + hexf('#0a0706')[None, None] * core[..., None]
    a = np.clip(core * 1.3 + 0.7 * lipa, 0, 1)
    save(rgb, out, a)
    Image.fromarray((ordm * 255).astype('uint8'), 'L').save(out[:-4] + '_ord.png')

def dent(p, out):
    """Cannonball dent decal 2 x 2 D (alpha): plain = deep dark crater with radial chips; rice = shallow round dent, the face
    pushed in but whole (soft shading, a pale squeezed rim)."""
    S = 256; yy, xx = np.mgrid[0:S, 0:S].astype('float32'); r = np.hypot(xx - S / 2 + 0.5, yy - S / 2 + 0.5) / (S / 2)
    rs = np.random.RandomState(p['seed']); n = pnoise(rs, S, S, 12, 12)
    if p['kind'] == 'plain':
        rr = r * (0.9 + 0.2 * n); a = np.clip((1.0 - rr) * 4, 0, 1)
        sh = np.clip(1 - rr / 0.75, 0, 1); rgb = hexf('#8a8680')[None, None] * (1 - 0.8 * sh[..., None]) + np.array([0.04, 0.03, 0.03]) * sh[..., None]
        rim = np.exp(-((rr - 0.8) / 0.08) ** 2); rgb = rgb + 0.2 * rim[..., None]
    else:
        rr = r * (0.95 + 0.1 * n); a = np.clip((1.0 - rr) * 3, 0, 1) * 0.85
        ny = (yy - S / 2) / (S / 2); sh = np.clip(-ny * (1 - rr) * 1.6, -0.6, 0.8)                       # lit from above: dark top, light bottom
        rgb = hexf('#c8c0ac')[None, None] * (1 - 0.45 * np.clip(sh, 0, 1)[..., None]) + 0.12 * np.clip(-sh, 0, 1)[..., None]
        rim = np.exp(-((rr - 0.86) / 0.07) ** 2); rgb = rgb * (1 - 0.3 * rim[..., None]) + hexf('#f2e8cc') * 0.3 * rim[..., None]
    save(rgb, out, a)

def drips(p, out):
    """Wet rice mortar oozing (alpha) on the 4 x 4 D brick tile: milky runs hanging from the bed joints (course lines every 0.5 D)."""
    ppd = p['ppd']; S = int(4 * ppd); rs = np.random.RandomState(p['seed']); ss = 2
    im = Image.new('L', (S * ss, S * ss), 0); d = ImageDraw.Draw(im); s = ppd * ss
    for c in range(8):
        y0 = (c * 0.5 + 0.05) * s
        for k in range(14):
            x = rs.rand() * 4 * s; l = (0.06 + rs.rand() ** 2 * 0.36) * s; w = (0.025 + 0.03 * rs.rand()) * s
            d.line([(x, y0), (x + rs.uniform(-0.01, 0.01) * s, y0 + l)], fill=230, width=int(w)); d.ellipse([x - w * 0.8, y0 + l - w * 0.8, x + w * 0.8, y0 + l + w * 0.8], fill=240)
        d.rectangle([0, y0 - 0.06 * s, 4 * s, y0 + 0.02 * s], fill=160)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(ss * 0.8)).resize((S, S), Image.LANCZOS)).astype('float32') / 255
    rgb = np.ones((S, S, 3), 'float32') * hexf('#f4ecd6'); save(rgb, out, a)

# ============================================================================= sprites: smoke, dust, steam, rain
def puff(p, out):
    """Soft cloud sprite 1 x 1 (alpha): a lumpy disc of fbm, white (tinted in the material)."""
    S = 256; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32')
    r = np.hypot(xx - S / 2, yy - S / 2) / (S / 2); n = pfbm(rs, S, S, 4, 4, 5)
    a = np.clip((1 - r * (0.75 + 0.5 * n)) * 2.2, 0, 1) ** 1.3
    shade = 0.75 + 0.35 * np.clip(1 - (yy / S) * 0.8 - 0.3 * n, 0, 1)
    save(np.repeat(shade[..., None], 3, 2), out, a)

def column(p, out):
    """Rising column 2 x 8 D (alpha, tiles in v): smoke or steam ribbons, soft fbm; brighter core."""
    W, H = 128, 512; rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:H, 0:W].astype('float32'); n = pfbm(rs, H, W, 3, 12, 5); n2 = pfbm(rs, H, W, 6, 24, 3)
    cx = 0.5 + 0.18 * (pnoise(rs, H, 1, 1, 6)[:, :1] - 0.5) * 2
    dx = np.abs(xx / W - cx) / (0.22 + 0.16 * n)
    a = np.clip(1 - dx, 0, 1) ** 1.2 * (0.55 + 0.6 * n2) * p.get('k', 1.0)
    shade = 0.7 + 0.4 * n
    save(np.repeat(shade[..., None], 3, 2), out, np.clip(a, 0, 1))

def rain_screen(p, out):
    """Screen-space rain layer 720 x 1280 (RGB streaks on black, added in the compositor), tileable in x and y: near = sparse long
    soft streaks, far = dense short fine streaks; a slight slant."""
    W, H = 720, 1280; rs = np.random.RandomState(p['seed']); ss = 2
    im = Image.new('L', (W * ss, H * ss), 0); d = ImageDraw.Draw(im)
    for _ in range(p['n']):
        x, y = rs.rand() * W * ss, rs.rand() * H * ss; l = rs.uniform(*p['len']) * ss; c = int(rs.uniform(*p['val']))
        for ox in (-W * ss, 0, W * ss):
            for oy in (-H * ss, 0, H * ss):
                d.line([(x + ox, y + oy), (x + ox - l * 0.07, y + oy + l)], fill=c, width=max(1, int(ss * rs.uniform(*p['w']))))
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(ss * p.get('blur', 0.4))).resize((W, H), Image.LANCZOS)).astype('float32') / 255
    save(np.repeat(a[..., None], 3, 2), out)

def rain(p, out):
    """Rain streak sheet 4 x 4 (alpha, tiles): thin slanted bright streaks of random length."""
    S = 512; rs = np.random.RandomState(p['seed']); ss = 2
    im = Image.new('L', (S * ss, S * ss), 0); d = ImageDraw.Draw(im)
    for _ in range(p['n']):
        x, y = rs.rand() * S * ss, rs.rand() * S * ss; l = rs.uniform(18, 60) * ss; c = int(rs.uniform(90, 230))
        for oy in (-S * ss, 0, S * ss):
            d.line([(x, y + oy), (x - l * 0.08, y + l + oy)], fill=c, width=max(1, int(ss * rs.uniform(0.7, 1.4))))
    a = np.asarray(im.resize((S, S), Image.LANCZOS)).astype('float32') / 255
    save(np.ones((S, S, 3), 'float32'), out, a)

# ============================================================================= macro (inside the joint)
def macro_clay(p, out):
    """Fired-clay brick seen at macro scale 8 x 8 D: porous grey-buff body, pores, sand grains, firing streaks."""
    S = 512; rs = np.random.RandomState(p['seed'])
    n = pfbm(rs, S, S, 4, 4, 6); n2 = pnoise(rs, S, S, 90, 90); n3 = pnoise(rs, S, S, 30, 30)
    img = hexf(p['col'])[None, None] * (0.78 + 0.35 * n[..., None]) * (0.92 + 0.14 * n2[..., None])
    pores = np.clip((n3 - 0.78) * 8, 0, 1) * 0.6 + np.clip((n2 - 0.85) * 10, 0, 1) * 0.4
    img = img * (1 - 0.6 * pores[..., None])
    grains = (pnoise(rs, S, S, 160, 160) > 0.87).astype('float32'); img = img + 0.12 * grains[..., None]
    save(img, out)

def macro_matrix(p, out):
    """Mortar matrix at macro scale 4 x 4 D: plain (grey, grainy, angular sand) / rice (creamy, smoother, with a faint fibrous
    sheen)."""
    S = 512; rs = np.random.RandomState(p['seed'])
    n = pfbm(rs, S, S, 4, 4, 6); n2 = pnoise(rs, S, S, 120, 120)
    img = hexf(p['col'])[None, None] * (0.82 + 0.3 * n[..., None]) * (0.9 + 0.15 * n2[..., None])
    if p['kind'] == 'rice':
        f = pfbm(rs, S, S, 24, 3, 3); img = img + 0.06 * np.clip((f - 0.5) * 4, 0, 1)[..., None]
    else:
        g = (pnoise(rs, S, S, 70, 70) > 0.8).astype('float32'); img = img * (1 - 0.25 * g[..., None])
    save(img, out)

# ============================================================================= skies and the painted ring
SKY_W = 4096
def sky(p, out):
    import desert_tex as DT
    mode = p['mode']; W = SKY_W; H = int(round(W * 105 / 360)); rs = np.random.RandomState({'DAY': 3, 'DUSK': 5, 'DAWN': 7, 'RAIN': 9, 'BATTLE': 11}[mode])
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0
    az = (np.arange(W, dtype='float32') + 0.5) / W * 2 * math.pi
    E = np.radians(el)[:, None] * np.ones((1, W), 'float32'); A = np.ones((H, 1), 'float32') * az[None, :]
    dx, dy, dz = np.cos(E) * np.cos(A), np.cos(E) * np.sin(A), np.sin(E)
    def grad(stops):
        e = np.clip(el, -15, 90); out_ = np.zeros((H, 3), 'float32')
        for ch in range(3): out_[:, ch] = np.interp(e, [s[0] for s in stops], [hexf(s[1])[ch] for s in stops])
        return np.repeat(out_[:, None, :], W, 1)
    def glow(azd, eld, rad, col, k):
        sx, sy, sz = math.cos(math.radians(eld)) * math.cos(math.radians(azd)), math.cos(math.radians(eld)) * math.sin(math.radians(azd)), math.sin(math.radians(eld))
        d = np.degrees(np.arccos(np.clip(dx * sx + dy * sy + dz * sz, -1, 1))); return (np.exp(-(d / rad) ** 2) * k)[..., None] * hexf(col)[None, None], d
    sun = p['sun']                                                           # (azimuth deg, elevation deg)
    def clouds(col_lit, col_dark, cover, lo, hi, cell=180, k=0.9, lit_dir=None):
        cl = DT._fbm(rs, H, W, cell, 5); m = np.clip((cl - (1 - cover)) * 5, 0, 1) * np.clip((el[:, None] - lo) / 4, 0, 1) * np.clip((hi - el[:, None]) / 10, 0, 1)
        sh = DT._fbm(rs, H, W, cell // 2, 3)
        c = hexf(col_lit)[None, None] * (1 - sh[..., None] * 0.6) + hexf(col_dark)[None, None] * (sh[..., None] * 0.6)
        return m[..., None] * k, c
    if mode == 'DAY':
        img = grad([(-15, '#c8d0d8'), (0, '#e8eef0'), (5, '#cfe0ee'), (18, '#86b8e6'), (45, '#4a8ad8'), (90, '#2a64c0')])
        g, dd = glow(sun[0], sun[1], 16.0, '#fff2d0', 0.7); img += g; img += (np.exp(-(dd / 1.4) ** 2) * 3.0)[..., None] * hexf('#fffaf0')
        m, c = clouds('#ffffff', '#b8c4dc', 0.36, 4, 40, 200); img = img * (1 - m) + c * m
    elif mode in ('DUSK', 'DAWN'):
        if mode == 'DUSK': img = grad([(-15, '#3a3a5a'), (0, '#ffa050'), (5, '#ffb868'), (12, '#f8c088'), (24, '#a8b0c8'), (45, '#5a78b8'), (90, '#26387e')])
        else: img = grad([(-15, '#6a4a6a'), (0, '#ffc89a'), (6, '#f8c0a0'), (16, '#e0b8a8'), (30, '#a8b0d8'), (60, '#5a80c8'), (90, '#3a5aa8')])
        g, dd = glow(sun[0], sun[1], 24.0, '#ffd080', 1.0); img += g
        g2, _ = glow(sun[0], sun[1], 70.0, '#ff8a50', 0.35); img += g2
        img += (np.exp(-(dd / 2.6) ** 2) * 2.5)[..., None] * hexf('#fff0c8')
        cl = DT._fbm(rs, H, W, 220, 4); streak = np.clip((cl - 0.52) * 5, 0, 1) * np.exp(-((el[:, None] - 10) / 7) ** 2)
        img = img * (1 - 0.8 * streak[..., None]) + streak[..., None] * hexf('#ff9a5a' if mode == 'DUSK' else '#ffc0a0') * (0.8 + 0.8 * np.exp(-(dd / 45) ** 2))[..., None]
    elif mode == 'RAIN':
        img = grad([(-15, '#5a6470'), (0, '#9aa4b0'), (8, '#8a96a8'), (30, '#6a7890'), (90, '#4a5670')])
        m, c = clouds('#a8b0bc', '#4a5262', 0.75, -2, 95, 150, 1.0); img = img * (1 - m) + c * m
        m2, c2 = clouds('#c8ccd4', '#68707e', 0.4, 0, 60, 90, 0.6); img = img * (1 - m2) + c2 * m2
    else:                                                                    # BATTLE: smoky red dusk
        img = grad([(-15, '#2a2434'), (0, '#ff7a3a'), (4, '#f07a3a'), (10, '#d87a3a'), (20, '#6a5a58'), (32, '#34446e'), (55, '#20305e'), (90, '#141c46')])
        g, dd = glow(sun[0], sun[1], 22.0, '#ffb060', 1.1); img += g
        img += (np.exp(-(dd / 2.2) ** 2) * 2.4)[..., None] * hexf('#ffe0a0')
        cl = DT._fbm(rs, H, W, 160, 5); sm = np.clip((cl - 0.45) * 3, 0, 1) * np.clip((el[:, None] + 2) / 8, 0, 1) * np.clip((70 - el[:, None]) / 30, 0, 1)
        smc = hexf('#2e2a3a')[None, None] * (1 - DT._fbm(rs, H, W, 80, 3)[..., None] * 0.5) + np.exp(-(dd / 40) ** 2)[..., None] * hexf('#a04a2a') * 0.8
        img = img * (1 - 0.85 * sm[..., None]) + 0.85 * sm[..., None] * smc
    Image.fromarray((np.clip(img, 0, 1) * 255 + 0.5).astype('uint8'), 'RGB').save(out)

PAN = dict(
    DAY=dict(far='#8aa0c8', mid='#6a8aa8', hill='#5a7a4a', tree='#3e5a32', roof='#4a4a58', wall='#c8bca8', pag='#7a6a68', river='#a8c8e0', fog='#dce6f0', win=None),
    DUSK=dict(far='#8a80b0', mid='#5e5a88', hill='#4a4a5e', tree='#2e3446', roof='#2e3040', wall='#c89a88', pag='#5a4050', river='#f0a878', fog='#ffc8a0', win='#ffb048'),
    DAWN=dict(far='#a8acd0', mid='#8090b8', hill='#64707e', tree='#4a5060', roof='#4a4858', wall='#d8c0b8', pag='#6a5868', river='#f8d0b8', fog='#f8e0e0', win='#ffc070'),
    RAIN=dict(far='#7a8494', mid='#68748a', hill='#4e5e58', tree='#3a4a44', roof='#3a3e48', wall='#9a9a9a', pag='#545460', river='#8a96a8', fog='#a8b0bc', win='#ffb048'),
    BATTLE=dict(far='#5a4e7a', mid='#3e3a62', hill='#30304a', tree='#22243a', roof='#22222e', wall='#8a6a68', pag='#3a2a3a', river='#e07a50', fog='#c86a50', win='#ff9a3a'),
)
def pano(p, out):
    """Painted ring (R 120, z -1.5..34): layered blue mountain ranges with mist, wooded hills, a pagoda on a hill (az ~250, behind the
    two_sections / site_wide views over the wall), village roofs and tree lines; at DUSK / DAWN / RAIN / BATTLE warm windows."""
    mode = p['mode']; c = PAN[mode]; ppd = p['ppd']; Wd = 2 * math.pi * PANO_R; Hd = PANO_Z1 - PANO_Z0; W, H = int(Wd * ppd), int(Hd * ppd)
    rs = np.random.RandomState(31); im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def Y(z): return (PANO_Z1 - z) * ppd
    def X(azd): return azd / 360.0 * W
    def ridge(base, amp, n, col, seed, sharp=1.0):
        r = np.random.RandomState(seed); xs = np.linspace(0, W, n + 1); zs = []
        ph = r.rand(4) * 6.3
        for i, x in enumerate(xs):
            t = i / n * 2 * math.pi
            z = base + amp * (0.5 + 0.25 * math.sin(3 * t + ph[0]) + 0.15 * math.sin(7 * t + ph[1]) + 0.1 * math.sin(17 * t + ph[2])) ** sharp + r.uniform(0, amp * 0.12)
            zs.append(z)
        zs[-1] = zs[0]; pts = [(x, Y(z)) for x, z in zip(xs, zs)] + [(W, H), (0, H)]
        d.polygon(pts, fill=hex8(col) + (255,))
        return xs, zs
    def blend(a, b, t): A, B = hexf(a), hexf(b); return '#%02x%02x%02x' % tuple(int(255 * (A[i] * (1 - t) + B[i] * t)) for i in range(3))
    ridge(10.0, 18.0, 160, blend(c['far'], c['fog'], 0.35), 3, 1.6)
    ridge(6.0, 12.0, 220, blend(c['far'], c['fog'], 0.1), 5, 1.4)
    xs, zs = ridge(2.0, 6.0, 300, c['mid'], 7, 1.0)
    ridge(-0.5, 2.6, 400, c['hill'], 9, 1.0)
    # tree lines along the low hills
    for k in range(1600):
        x = rs.rand() * W; z = rs.uniform(-0.6, 1.6); r_ = rs.uniform(0.35, 0.9) * ppd
        d.ellipse([x - r_, Y(z) - r_ * 1.2, x + r_, Y(z) + r_ * 0.4], fill=hex8(blend(c['tree'], c['hill'], rs.rand() * 0.5)) + (255,))
    # pagoda on a hill (behind the wall seen from the site) and a second, smaller one far round
    for (azd, zb, s) in ((252.0, 3.0, 1.0), (118.0, 2.0, 0.6), (300.0, 1.5, 0.45)):
        x0 = X(azd); hill = [(x0 - 18 * ppd * s, Y(-1)), (x0 - 6 * ppd * s, Y(zb)), (x0 + 6 * ppd * s, Y(zb)), (x0 + 18 * ppd * s, Y(-1))]
        d.polygon(hill, fill=hex8(c['hill']) + (255,))
        z = zb; w = 2.4 * s
        for k in range(7):
            h = 1.5 * s; ww = w * (1 - 0.08 * k)
            d.rectangle([x0 - ww / 2 * ppd, Y(z + h), x0 + ww / 2 * ppd, Y(z)], fill=hex8(c['pag']) + (255,))
            if c['win']: d.rectangle([x0 - 0.2 * ppd * s, Y(z + h * 0.7), x0 + 0.2 * ppd * s, Y(z + h * 0.3)], fill=hex8(c['win']) + (255,))
            eave = ww * 0.9 + 1.2 * s
            d.polygon([(x0 - eave * ppd, Y(z + h + 0.15 * s)), (x0 - ww / 2 * ppd, Y(z + h + 0.55 * s)), (x0 + ww / 2 * ppd, Y(z + h + 0.55 * s)), (x0 + eave * ppd, Y(z + h + 0.15 * s))], fill=hex8(c['roof']) + (255,))
            z += h + 0.55 * s
        d.line([(x0, Y(z)), (x0, Y(z + 2.0 * s))], fill=hex8(c['roof']) + (255,), width=max(1, int(0.2 * ppd * s)))
    # villages: low white walls + dark roofs
    for (azd, n) in ((200.0, 14), (235.0, 10), (60.0, 12), (150.0, 8), (330.0, 10)):
        x = X(azd)
        for k in range(n):
            w = rs.uniform(2.0, 4.0) * ppd; h = rs.uniform(0.8, 1.4); z0 = rs.uniform(-0.6, 0.3)
            d.rectangle([x, Y(z0 + h), x + w, Y(z0)], fill=hex8(c['wall']) + (255,))
            d.polygon([(x - 0.4 * ppd, Y(z0 + h)), (x + w / 2, Y(z0 + h + 0.9)), (x + w + 0.4 * ppd, Y(z0 + h))], fill=hex8(c['roof']) + (255,))
            if c['win'] and rs.rand() < 0.5: d.rectangle([x + w * 0.4, Y(z0 + h * 0.7), x + w * 0.55, Y(z0 + h * 0.3)], fill=hex8(c['win']) + (255,))
            x += w + rs.uniform(0.5, 3.0) * ppd
    a = np.asarray(im).astype('float32') / 255                                # mist at the foot of each range (fades up)
    zrow = PANO_Z1 - (np.arange(H) + 0.5) / ppd; fog = np.clip(1 - (zrow - (-1.5)) / 7.0, 0, 1)[:, None, None] * 0.35
    rgb = a[..., :3] * (1 - fog) + hexf(c['fog'])[None, None] * fog
    save(rgb, out, a[..., 3])

# ============================================================================= registry
def all_jobs():
    JOBS.clear()
    reg('brick_plain', dict(kind='plain', ppd=128, seed=11, brick='#7c8188', mortar='#4e5258', mw=0.04), brick)
    reg('brick_rice', dict(kind='rice', ppd=128, seed=11, brick='#a69e90', mortar='#f6ead0', mw=0.12), brick)
    reg('brick_old', dict(kind='old', ppd=96, seed=13, brick='#868682', mortar='#b8b2a4', mw=0.05), brick)
    reg('stone', dict(ppd=64, seed=15, col='#a8a49a'), stone)
    reg('ground', dict(ppd=96, seed=17, a='#94714e', b='#76583c', straw=360, pebbles=90, lime=0, specks=40, straw_c='#c8b070'), earth)
    reg('field', dict(ppd=64, seed=19, a='#8a9a48', b='#6a7a36', tufts=500, pebbles=30, tuft_c='#4a6a28'), earth)
    reg('topbed', dict(ppd=96, seed=21, a='#8a857a', b='#6a665c', pebbles=220, specks=60), earth)
    reg('lime', dict(ppd=96, seed=23, col='#eeeee6'), paste)
    reg('mortar_plain', dict(ppd=96, seed=25, col='#8a8c8e'), paste)
    reg('mortar_rice', dict(ppd=96, seed=27, col='#efe2bc', grains=60), paste)
    reg('soup', dict(ppd=128, seed=29, col='#f2ead2', grains=500, bubbles=60), paste)
    reg('tiles', dict(ppd=96, seed=31, col='#6a6e78'), tiles)
    reg('canvas', dict(ppd=64, seed=33, a='#e8dcc0', b='#c8a878', stripe=0.0), canvas)
    reg('canvas_b', dict(ppd=64, seed=35, a='#d8c8a0', b='#3a5a8a', stripe=1.0), canvas)
    reg('banner_red', dict(ppd=96, field='#c02a24', border='#f0c040', emblem='#f8d860', motif='tiger'), banner)
    reg('banner_blue', dict(ppd=96, field='#244a8a', border='#f0e0b0', emblem='#f8f0d0', motif='sun'), banner)
    reg('banner_black', dict(ppd=96, field='#2a2430', border='#c03a2a', emblem='#e05a3a', motif='sun'), banner)
    reg('lantern_red', dict(col='#e8402a'), lantern)
    reg('dent_plain', dict(kind='plain', seed=41), dent)
    reg('dent_rice', dict(kind='rice', seed=43), dent)
    reg('drips', dict(ppd=96, seed=45), drips)
    reg('rain_near', dict(seed=54, n=170, len=(70, 150), val=(110, 200), w=(1.4, 2.4), blur=0.8), rain_screen)
    reg('rain_far', dict(seed=56, n=1100, len=(14, 40), val=(80, 190), w=(0.8, 1.3), blur=0.3), rain_screen)
    reg('clay_macro', dict(seed=55, col='#8c8c92'), macro_clay)
    reg('matrix_plain', dict(seed=57, kind='plain', col='#8c8e90'), macro_matrix)
    reg('matrix_rice', dict(seed=59, kind='rice', col='#e4d6b2'), macro_matrix)
    for m, s in (('DAY', (135.0, 42.0)), ('DUSK', (35.0, 6.0)), ('DAWN', (200.0, 5.0)), ('RAIN', (90.0, 60.0)), ('BATTLE', (262.0, 5.0))):
        reg('sky_' + m, dict(mode=m, sun=s, w=SKY_W), sky); reg('pano_' + m, dict(mode=m, ppd=8), pano)

def add_cracks(name, kind, W, H, impacts, ppd=40, seed=61):
    reg(name, dict(kind=kind, W=W, H=H, impacts=[list(map(float, i)) for i in impacts], ppd=ppd, seed=seed, wk=1.8 if kind == 'general' else 1.4), cracks)

def ensure(extra=None, verbose=True):
    """Paint every changed texture; return {name: png path} (+ shared desert glow images, + '<name>_mask' / '_ord' companions).
    extra: callable registering more jobs (wall.py adds the crack maps, whose impact points it owns)."""
    os.makedirs(TEX, exist_ok=True); all_jobs()
    if extra: extra()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    out = {}
    for name, (params, fn) in JOBS.items():
        h = hashlib.sha1((TEX_V + fn.__name__ + json.dumps(params, sort_keys=True)).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            fn(params, png); man[name] = h
            if verbose: print('painted', name, flush=True)
        for suf in ('_mask', '_ord'):
            if os.path.exists(png[:-4] + suf + '.png'): out[name + suf] = png[:-4] + suf + '.png'
    json.dump(man, open(mpath, 'w'), indent=0, sort_keys=True)
    for nm in ('pool', 'shaft', 'glint', 'wisp'): out[nm] = os.path.join(DESERT_TEX, nm + '.png')
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: os.path.basename(v) for k, v in p.items()}, indent=0))
