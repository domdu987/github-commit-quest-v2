#!/usr/bin/env python3
"""street_tex.py : artwork of the film-12 set (a Georgian London street in the rain, early 1750s).
numpy + PIL only, supersampled where it matters, deterministic (fixed seeds), cached in v3/set3d12/tex_street/ by a hash of the painter's
parameters + TEX_V (bump TEX_V after editing painter code). The sky painter and noise helpers are imported (never copied) from film 9 / 10.
No lettering anywhere: signs are pictures (boot, teapot, pretzel).

    import street_tex as ST
    tx = ST.ensure()      # {name: png path}
"""
import os, sys, json, math, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d10'), os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8')):
    if p not in sys.path: sys.path.insert(0, p)
import numpy as np                                              # noqa: E402
from PIL import Image, ImageDraw, ImageFilter                   # noqa: E402
import wall_tex as WX                                           # noqa: E402  (film-9 painters: sky, noise)
from wall_tex import hexf, hex8, pnoise, pfbm, save             # noqa: E402
import harbour_tex as HX                                        # noqa: E402  (sky_rich painter)

TEX = os.path.join(HERE, 'tex_street')
TEX_V = 's12.15'
JOBS = {}
def reg(name, params, fn): JOBS[name] = (params, fn)

# period palette
BRICKS = dict(red='#b4593a', ochre='#c0793f', brown='#7c4a36', stock='#b59463', rust='#a34a34', plum='#8a4a46')
CREAM, STONE = '#eadfc0', '#cfc6b0'
GREEN, OXBLOOD, NAVY = '#2f5c46', '#6e2433', '#2b3f66'

def _rgb(a): return np.clip(a, 0, 1)

def _lerp(a, b, t): return a * (1 - t) + b * t

# ----------------------------------------------------------------------------- cobbles / pavement
def cobbles(p, out):
    """Setts (4 x 4 units): individually readable rounded granite setts (0.66 x 0.44 u) laid in running bond with dark wet mortar, per-sett colour
    (grey, violet-grey, ochre, slate) and a pale wet rim on the top-left edge. Also writes <out>_h.png (height, for the bump)."""
    S = 1024; ppd = S / 4.0; rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    sw, sh = 0.8, 0.5                                                              # 5 x 8 setts per tile, wraps cleanly
    row = np.floor(yy / sh); off = (row % 2) * sw * 0.5
    xo = xx + off; u = xo % sw; v = yy % sh; bx = np.floor(xo / sw)
    bid = ((row * 37 + (bx % 5) * 11) % 211).astype(int); r = rs.rand(211, 5)
    # each sett is slightly rotated / uneven: wobble the local coordinates by a per-sett random shear
    cu = (u / sw - 0.5) * 2; cv = (v / sh - 0.5) * 2
    shear = (r[bid, 3] - 0.5) * 0.12
    cu2 = cu + shear * cv; cv2 = cv - shear * cu
    pw = 0.84 + 0.1 * r[bid, 4]; ph_ = 0.8 + 0.1 * r[bid, 2]                       # sett half extents inside the cell (mortar share)
    q = (np.abs(cu2 / pw) ** 4.0 + np.abs(cv2 / ph_) ** 4.0) ** 0.25               # superellipse: 0 centre .. 1 at the sett edge
    inside = np.clip((1.0 - q) / 0.07, 0, 1)                                       # anti-aliased sett mask
    dome = np.clip(1.0 - q, 0, 1) ** 0.55
    pal = np.array([hexf('#8f8c92'), hexf('#7a8294'), hexf('#a08e76'), hexf('#68727f'), hexf('#a4906f'), hexf('#78848f'), hexf('#928076')])
    pick = (r[bid, 0] * len(pal)).astype(int) % len(pal)
    base = pal[pick] * (0.74 + 0.5 * r[bid, 1:2])
    mot = pfbm(rs, S, S, 24, 24, 4)[..., None]
    col = base * (0.86 + 0.28 * mot) * (0.62 + 0.55 * dome[..., None])
    # light from the upper left: pale wet rim on the top-left edge of each sett, dark lower-right edge
    lx = -cu2 * 0.7 + cv2 * 0.7
    rim = np.clip((q - 0.55) / 0.35, 0, 1) * np.clip(lx * 1.4, -1, 1)
    col = col * (1 + 0.38 * np.clip(rim, 0, 1)[..., None]) * (1 - 0.3 * np.clip(-rim, 0, 1)[..., None])
    # speckle (granite) kept low frequency so it does not alias
    col = col * (0.95 + 0.1 * pnoise(rs, S, S, 128, 128)[..., None])
    mort = hexf('#1e1c32')[None, None] * (0.8 + 0.5 * pnoise(rs, S, S, 64, 64)[..., None])
    col = _lerp(mort, col, inside[..., None])
    save(_rgb(col), out)
    h = np.clip(inside * (0.35 + 0.65 * dome ** 0.8), 0, 1) * (0.85 + 0.15 * r[bid, 2])
    save(np.repeat(h[..., None], 3, 2), out[:-4] + '_h.png')

def pave(p, out):
    """Flagstones of the pavement (4 x 4 units): big pale slabs, blue-grey, joints dark, moss/dirt, kerb strip is a separate texture."""
    S = 640; ppd = S / 4.0; rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    sw, sh = 2.0, 1.3; row = np.floor(yy / sh); off = (row % 2) * 0.7
    u = (xx + off) % sw; v = yy % sh; bx = np.floor((xx + off) / sw); bid = ((row * 13 + bx * 5) % 97).astype(int); r = rs.rand(97, 3)
    gap = np.minimum(np.minimum(u, sw - u), np.minimum(v, sh - v))
    pal = [hexf('#9a9ca8'), hexf('#a8a4a0'), hexf('#8c92a6'), hexf('#b0a89a')]
    base = np.stack([pal[i % 4] for i in (r[:, 0] * 4).astype(int)])[bid] * (0.85 + 0.25 * r[bid, 1:2])
    col = base * (0.86 + 0.26 * pfbm(rs, S, S, 12, 12, 5)[..., None])
    col = col * (1 - 0.12 * (1 - np.clip(gap / 0.15, 0, 1))[..., None])
    col = np.where((gap < 0.035)[..., None], hexf('#2e2c40')[None, None], col)
    save(_rgb(col), out)

def kerb(p, out):
    S = 512; ppd = S / 4.0; rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    L = 1.6; u = xx % L; bid = (np.floor(xx / L) * 7 % 31).astype(int); r = rs.rand(31, 2)
    col = hexf('#b4b0b8')[None, None] * (0.85 + 0.25 * r[bid, 0][..., None]) * (0.9 + 0.2 * pfbm(rs, S, S, 10, 10, 4)[..., None])
    col = np.where((np.minimum(u, L - u) < 0.03)[..., None], hexf('#363448')[None, None], col)
    save(_rgb(col), out)

def gutter(p, out):
    """Running water in the gutter channel (u along the flow = 4 units, v across): dark blue-teal, braided long light streaks, little standing
    waves (chevrons) and a pale foam line at both banks."""
    W, H = 1024, 192; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    n = pfbm(rs, H, W, 8, 3, 4); n2 = pfbm(rs, H, W, 16, 4, 3)
    s = np.sin((xx / W * 4 * 2 * math.pi) * 1.0 + n * 7.0 + (yy / H) * 3.0 * (n2 - 0.5))
    base = hexf('#243a68')[None, None] * (0.75 + 0.55 * n[..., None])
    hi = np.clip(s - 0.62, 0, 1) * 2.4; base = base + hexf('#a8c8f0')[None, None] * hi[..., None] * 0.5
    ch = np.abs(((xx / W * 16) % 1.0) - 0.5) * 2 + (np.abs(yy / H - 0.5)) * 1.2
    wave = np.clip(1.0 - np.abs(ch - 0.55) / 0.05, 0, 1) * np.clip(1 - np.abs(yy / H - 0.5) * 2.2, 0, 1) * (n2 > 0.45)
    base = base + hexf('#d8e8ff')[None, None] * wave[..., None] * 0.55
    bank = np.clip(1 - np.minimum(yy, H - yy) / (H * 0.1), 0, 1) ** 1.5
    base = _lerp(base, hexf('#e4ecfa')[None, None] * 0.9, (bank * (0.35 + 0.4 * n))[..., None])
    save(_rgb(base), out)

def puddle_mask(p, out):
    """Puddle decal mask (RGB, non-colour): R = body alpha (irregular blob, soft ~12 % edge), G = thin pale rim line right at the shore,
    B = deep core alpha (smaller, softer). 512 px, the blob fills the square (radius 0.46)."""
    S = 512; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32'); xx = (xx - S / 2) / (S / 2); yy = (yy - S / 2) / (S / 2)
    sx, sy = p.get('sx', 1.0), p.get('sy', 1.0); xx = xx / sx; yy = yy / sy
    ang = np.arctan2(yy, xx); rr = np.sqrt(xx ** 2 + yy ** 2)
    ph = rs.uniform(0, 6.28, 6); amp = [0.09, 0.07, 0.05, 0.035, 0.02, 0.012]
    edge = 0.62 + sum(a * np.sin((k + 2) * ang + ph[k]) for k, a in enumerate(amp)) + (pfbm(rs, S, S, 6, 6, 3) - 0.5) * 0.16
    d = (edge - rr)                                                               # > 0 inside
    body = np.clip(d / 0.07, 0, 1) ** 1.2
    rim = np.clip(1 - np.abs(d - 0.02) / 0.04, 0, 1) ** 1.5 * 0.7 * (0.5 + 0.5 * pnoise(rs, S, S, 18, 18)) * np.clip(body * 2.0, 0, 1)
    core = np.clip((d - 0.12) / 0.2, 0, 1)
    save(np.stack([body, rim, core], -1), out)

def ripples(p, out):
    """Soft ripple rings: pale cool thin rings (anti-aliased, softly blurred) on transparent, several centres per tile; radii fade outward."""
    S = 1024; ss = 2; Sx = S * ss; rs = np.random.RandomState(p['seed'])
    im = Image.new('RGBA', (Sx, Sx), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
    for k in range(p['n']):
        cx, cy = rs.uniform(0.14, 0.86) * Sx, rs.uniform(0.14, 0.86) * Sx; R = rs.uniform(0.06, 0.12) * Sx; nr = rs.randint(2, 4)
        for j in range(nr):
            rr = R * (0.4 + 0.6 * (j + 1) / nr); a = int(255 * (0.95 - 0.55 * j / nr)); w = max(2, int(Sx * 0.0028 * (1 - 0.3 * j / nr)))
            dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(214, 230, 250, a), width=w)
    im = im.filter(ImageFilter.GaussianBlur(2.2)).resize((S, S), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255
    save(a[..., :3], out, alpha=a[..., 3])

# ----------------------------------------------------------------------------- generic tiles
def wood(p, out):
    S = 512; ppd = S / 4.0; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd; base = hexf(p['col']); w = p.get('w', 0.5)
    row = np.floor(yy / w); r = rs.rand(64, 2); seg = np.floor((xx + r[row.astype(int) % 64, 1] * 4) / 2.0); bid = (row * 17 + seg * 5).astype(int) % 64
    grain = np.sin(xx * 14 + pnoise(rs, S, S, 4, 30) * 12)
    col = base * (0.78 + 0.3 * r[bid, :1]) * (0.94 + 0.06 * grain[..., None]) * (0.9 + 0.2 * pfbm(rs, S, S, 3, 3, 4)[..., None])
    v = yy % w; u = (xx + r[row.astype(int) % 64, 1] * 4) % 2.0
    col = np.where(((v < 0.03) | (u < 0.03))[..., None], base * 0.35, col)
    save(_rgb(col), out)

def barrel(p, out):
    """Barrel staves with two iron hoops (u around, v along)."""
    W, H = 256, 256; rs = np.random.RandomState(7); yy, xx = np.mgrid[0:H, 0:W].astype('float32')
    st = np.floor(xx / (W / 10)); r = rs.rand(10, 2); col = hexf(p['col'])[None, None] * (0.8 + 0.3 * r[st.astype(int), 0][..., None])
    col = col * (0.94 + 0.06 * np.sin(yy * 0.5 + st))[..., None]
    col = np.where((np.mod(xx, W / 10) < 1.6)[..., None], col * 0.4, col)
    for y0 in (0.14, 0.34, 0.66, 0.86):
        hoop = np.abs(yy / H - y0) < 0.028; col = np.where(hoop[..., None], hexf('#2c2c34')[None, None] * 1.1, col)
    save(_rgb(col), out)

def slate(p, out):
    S = 512; ppd = S / 4.0; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd; base = hexf(p['col'])
    row = np.floor(yy / 0.45); off = (row % 2) * 0.35; bx = np.floor((xx + off) / 0.7); bid = (row * 31 + bx * 7).astype(int) % 173; r = rs.rand(173, 2)
    u = (xx + off) % 0.7; v = yy % 0.45
    col = base * (0.75 + 0.4 * r[bid, :1]) * (1 - 0.32 * (v / 0.45) ** 3)[..., None]
    col = np.where(((u < 0.03) | (v > 0.42))[..., None], base * 0.4, col)
    col = col * (0.9 + 0.2 * pfbm(rs, S, S, 4, 4, 4)[..., None])
    save(_rgb(col), out)

def stripes(p, out):
    S = 256; yy, xx = np.mgrid[0:S, 0:S].astype('float32'); k = (np.floor(xx / (S / p['n'])) % 2)[..., None]
    rs = np.random.RandomState(3)
    col = _lerp(hexf(p['a'])[None, None], hexf(p['b'])[None, None], k) * (0.92 + 0.12 * pfbm(rs, S, S, 6, 6, 3)[..., None])
    save(_rgb(col), out)

def lace(p, out):
    """Pink lace canopy for the final umbrella: a pink cloth with a ring of cut-out lace, alpha for the holes (u around, v rim..top)."""
    W, H = 512, 128; ss = 2; im = Image.new('RGBA', (W * ss, H * ss), hex8(p['col']) + (255,)); dr = ImageDraw.Draw(im)
    for i in range(32):
        cx = (i + 0.5) / 32 * W * ss
        dr.ellipse([cx - 0.014 * W * ss, 0.34 * H * ss, cx + 0.014 * W * ss, 0.5 * H * ss], fill=(0, 0, 0, 0))
        dr.ellipse([cx - 0.008 * W * ss, 0.58 * H * ss, cx + 0.008 * W * ss, 0.68 * H * ss], fill=(0, 0, 0, 0))
        dr.ellipse([cx - 0.01 * W * ss, 0.12 * H * ss, cx + 0.01 * W * ss, 0.22 * H * ss], fill=(0, 0, 0, 0))
    im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255
    yy = np.mgrid[0:H, 0:W][0].astype('float32')[..., None] / H
    rgb = a[..., :3] * (0.93 + 0.1 * np.sin(np.arange(W)[None, :, None] * 2 * math.pi * 8 / W))
    save(rgb, out, alpha=a[..., 3])

# ----------------------------------------------------------------------------- facades
FACADE_W, FACADE_H, FPPD = 8.0, 20.0, 80
def _px(S, x, z): return (x * S, (FACADE_H - z) * S)

def facade(p, out):
    """One house front, 8 x 20 units (u = x / 8, v = z / 20): brick in running bond with per-brick colour, cream stone plinth, string courses,
    sash windows with glazing bars (lintel + keystone + sill), the ground floor either a house (two windows + panel door with fanlight) or a
    shop (stallriser, pilasters, dark backdrop and fascia band). Window panes carry amber lamp glow in <out>_glow.png (gradient + curtains +
    a lamp), unlit panes reflect the wet sky. Vertical wet streaks under sills and the cornice."""
    ss = 2; S = FPPD * ss; W, H = int(FACADE_W * S), int(FACADE_H * S); rs = np.random.RandomState(p['seed'])
    yy, xx = np.mgrid[0:H, 0:W].astype('float32'); xx /= S; zz = FACADE_H - yy / S; del yy
    ch = 0.42; bl = 1.0                                                   # brick course height / length
    row = np.floor(zz / ch); off = (row % 2) * bl * 0.5; bx = np.floor((xx + off) / bl)
    bid = ((row * 53 + bx * 17 + p['seed']) % 509).astype(int); r = rs.rand(509, 4).astype('float32')
    u = (xx + off) % bl; v = zz % ch
    b1, b2 = hexf(BRICKS[p['brick']]), hexf(BRICKS[p['brick2']])
    base = _lerp(b1[None, None], b2[None, None], r[bid, 0:1][..., None] if False else r[bid, 0][..., None]) * (0.8 + 0.34 * r[bid, 1][..., None])
    base = base * (0.9 + 0.2 * pfbm(rs, H, W, 6, 20, 5)[..., None])
    edge = np.minimum(np.minimum(u, bl - u), np.minimum(v, ch - v))
    col = base * (1 - 0.2 * np.clip(1 - edge / 0.07, 0, 1)[..., None])
    col = np.where((v > ch - 0.045)[..., None], base * 1.12, col)           # lit top face of each course is not visible: a thin highlight under the joint
    mort = (u < 0.05) | (v < 0.05)
    col = np.where(mort[..., None], hexf('#b8a68c')[None, None] * (0.8 + 0.25 * pnoise(rs, H, W, 80, 200)[..., None]), col)
    # wet: vertical dark runs
    streak = pnoise(rs, H, W, 90, 3); streak = np.clip(streak - 0.55, 0, 1) * 2.0
    col = col * (1 - 0.28 * streak[..., None])
    img = Image.fromarray((np.clip(col, 0, 1) * 255).astype('uint8'), 'RGB'); dr = ImageDraw.Draw(img)
    glow = Image.new('RGB', (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glow)
    cream = hex8(CREAM); creamD = tuple(int(c * 0.8) for c in cream); stone = hex8(STONE)
    def rect(x0, z0, x1, z1, fill, d=dr): a = _px(S, x0, z1); b = _px(S, x1, z0); d.rectangle([a[0], a[1], b[0], b[1]], fill=fill)
    def poly(pts, fill, d=dr): d.polygon([_px(S, x, z) for x, z in pts], fill=fill)
    def arc_fill(cx, cz, r_, fill, d=dr, z_floor=None):
        a = _px(S, cx - r_, cz + r_); b = _px(S, cx + r_, cz - r_); d.pieslice([a[0], a[1], b[0], b[1]], 180, 360, fill=fill)
    # plinth, string courses, parapet band, cornice shadow, quoins
    rect(0, 0, 8, 0.95, stone); [rect(0, z, 8, z + 0.03, (90, 84, 96)) for z in (0.5,)]
    for x0 in np.arange(0, 8, 1.6): rect(x0, 0, x0 + 0.03, 0.95, (90, 84, 96))
    rect(0, 5.45, 8, 5.85, cream); rect(0, 5.45, 8, 5.5, creamD)
    rect(0, 10.75, 8, 10.95, cream); rect(0, 15.05, 8, 15.25, cream)
    rect(0, 18.55, 8, 19.35, cream); rect(0, 18.55, 8, 18.62, creamD)          # frieze under the cornice (the 3D cornice sits on top)
    for k in range(int(19.35 / 0.7) + 1):                                      # quoins at both edges
        z0 = 1.0 + k * 0.78; w = 0.62 if k % 2 == 0 else 0.4
        if z0 < 18.5:
            rect(0, z0, w, z0 + 0.72, stone); rect(8 - w, z0, 8, z0 + 0.72, stone)
    for k in range(int(19.35 / 0.7) + 1):
        z0 = 1.0 + k * 0.78
        if z0 < 18.5: rect(0, z0 + 0.72, 0.62, z0 + 0.75, (92, 86, 98)); rect(7.38, z0 + 0.72, 8, z0 + 0.75, (92, 86, 98))
    sash = hex8('#efe7d2'); gl_dark = hex8('#2c2a4c'); gl_ref = hex8('#55689a')
    lit = p['lit']; wi = [0]
    def window(cx, zc, w, h, glow_on, arch=False, rows=3, cols=2):
        x0, x1 = cx - w / 2, cx + w / 2; z0, z1 = zc - h / 2, zc + h / 2
        rect(x0 - 0.28, z1 + 0.04, x1 + 0.28, z1 + 0.44, cream)                       # lintel
        rect(x0 - 0.28, z1 + 0.04, x1 + 0.28, z1 + 0.08, creamD)
        rect(cx - 0.17, z1 + 0.04, cx + 0.17, z1 + 0.56, hex8('#f5ecd0'))             # keystone
        for k in range(1, 6):
            xk = x0 - 0.28 + k * (w + 0.56) / 6; rect(xk, z1 + 0.04, xk + 0.02, z1 + 0.44, creamD)
        rect(x0 - 0.2, z0 - 0.2, x1 + 0.2, z0, cream); rect(x0 - 0.2, z0 - 0.23, x1 + 0.2, z0 - 0.17, creamD)  # sill
        rect(x0 - 0.1, z0, x1 + 0.1, z1 + 0.04, (34, 28, 40))                         # reveal shadow
        rect(x0 - 0.04, z0 + 0.03, x1 + 0.04, z1, sash)
        # glass fields
        gx0, gx1, gz0, gz1 = x0 + 0.07, x1 - 0.07, z0 + 0.1, z1 - 0.07
        rect(gx0, gz0, gx1, gz1, gl_dark)
        if glow_on:
            # amber glow: gradient bright near a lamp, curtain strips, one dark chair/picture silhouette
            a = _px(S, gx0, gz1); b = _px(S, gx1, gz0); gw, gh = int(b[0] - a[0]), int(b[1] - a[1])
            gy, gx = np.mgrid[0:gh, 0:gw].astype('float32'); gx /= gw; gy /= gh
            lx, ly = rs.uniform(0.3, 0.7), rs.uniform(0.15, 0.5)
            d = np.sqrt((gx - lx) ** 2 + ((gy - ly) * 1.2) ** 2)
            amb = np.array([1.0, 0.62 - 0.1 * rs.rand(), 0.22], 'float32')
            g = (0.62 + 0.55 * np.exp(-d * 2.2))[..., None] * amb[None, None]
            g = g * (1 - 0.55 * np.clip((0.2 - np.minimum(gx, 1 - gx)) / 0.2, 0, 1)[..., None] * np.array([0.5, 0.8, 1.0])[None, None])
            if rs.rand() < 0.6: g = np.where((gy > 0.78)[..., None], g * np.array([0.55, 0.4, 0.3])[None, None], g)     # sill-height furniture
            glow.paste(Image.fromarray((np.clip(g, 0, 1.0) * 255).astype('uint8'), 'RGB'), (int(a[0]), int(a[1])))
            # colour map: dim warm glass so the facade still reads when the glow is added
            rect(gx0, gz0, gx1, gz1, (60, 36, 34))
        else:
            # reflection of the wet sky: diagonal pale blue bands
            a = _px(S, gx0, gz1); b = _px(S, gx1, gz0); gw, gh = int(b[0] - a[0]), int(b[1] - a[1])
            gy, gx = np.mgrid[0:gh, 0:gw].astype('float32'); gx /= gw; gy /= gh
            t = np.clip(1.0 - np.abs(((gx + gy * 0.6) % 0.9) - 0.3) / 0.12, 0, 1)
            gc = np.array(gl_dark, 'float32')[None, None] / 255 * (1 - 0.7 * t[..., None]) + np.array(gl_ref, 'float32')[None, None] / 255 * 0.7 * t[..., None]
            gc = gc * (1 - 0.35 * gy[..., None])
            img.paste(Image.fromarray((np.clip(gc, 0, 1) * 255).astype('uint8'), 'RGB'), (int(a[0]), int(a[1])))
        # glazing bars (also cut from the glow)
        bw = 0.055
        for k in range(1, cols): xk = gx0 + k * (gx1 - gx0) / cols; rect(xk - bw / 2, gz0, xk + bw / 2, gz1, sash); rect(xk - bw / 2, gz0, xk + bw / 2, gz1, (0, 0, 0), gd)
        for k in range(1, rows * 2):
            zk = gz0 + k * (gz1 - gz0) / (rows * 2); wk = bw * (1.6 if k == rows else 1.0)
            rect(gx0, zk - wk / 2, gx1, zk + wk / 2, sash); rect(gx0, zk - wk / 2, gx1, zk + wk / 2, (0, 0, 0), gd)
        # sash meeting rail / frame edges cut the glow too
        for (a0, b0, a1, b1) in ((gx0 - 0.1, gz0, gx0, gz1), (gx1, gz0, gx1 + 0.1, gz1), (gx0, gz1, gx1, gz1 + 0.1), (gx0, gz0 - 0.12, gx1, gz0)): rect(a0, b0, a1, b1, (0, 0, 0), gd)
        # wet run below the sill
        rect(x0 - 0.1, z0 - 0.7, x0 + 0.05, z0 - 0.23, tuple(int(c) for c in (60, 40, 40)))
    xs = (1.4, 4.0, 6.6)
    ws = [rs.rand() for _ in range(9)]
    for fi, (zc, h) in enumerate(((8.1, 3.3), (12.7, 3.1), (16.9, 2.4))):
        for bi, cx in enumerate(xs):
            on = rs.rand() < lit
            window(cx, zc, 1.5, h, on, rows=3 if fi < 2 else 2)
    if p['ground'] == 'house':
        db = p['door_bay']; dx = xs[db]
        for bi, cx in enumerate(xs):
            if bi == db: continue
            on = rs.rand() < min(1.0, lit + 0.2); window(cx, 3.1, 1.5, 2.6, on, rows=2)
        dc = hex8(p['door'])
        rect(dx - 0.95, 0.9, dx + 0.95, 4.85, cream)                                   # surround
        rect(dx - 0.95, 4.85, dx + 0.95, 5.05, creamD)
        rect(dx - 0.72, 0.95, dx + 0.72, 4.15, dc)                                    # door
        for (a0, a1) in ((1.2, 2.5), (2.75, 4.0)):
            for (b0, b1) in ((-0.55, -0.05), (0.05, 0.55)):
                rect(dx + b0, a0, dx + b1, a1, tuple(int(c * 0.74) for c in dc)); rect(dx + b0 + 0.03, a0 + 0.03, dx + b1 - 0.03, a1 - 0.03, tuple(min(255, int(c * 1.12)) for c in dc))
        rect(dx - 0.72, 2.6, dx + 0.72, 2.66, tuple(int(c * 0.6) for c in dc))
        ds = p.get('door_style', 'fan')
        if ds == 'fan':
            arc_fill(dx, 4.15, 0.72, sash); arc_fill(dx, 4.15, 0.64, gl_dark)
            arc_fill(dx, 4.15, 0.64, (255, 170, 70), gd)
            for k in range(1, 6):
                ang = math.pi * k / 6; ex, ez = dx + 0.66 * math.cos(ang), 4.15 + 0.66 * math.sin(ang)
                a = _px(S, dx, 4.15); b = _px(S, ex, ez); dr.line([a, b], fill=sash, width=int(S * 0.03)); gd.line([a, b], fill=(0, 0, 0), width=int(S * 0.03))
        elif ds == 'transom':
            rect(dx - 0.72, 4.15, dx + 0.72, 4.75, sash); rect(dx - 0.66, 4.2, dx + 0.66, 4.7, gl_dark); rect(dx - 0.66, 4.2, dx + 0.66, 4.7, (255, 170, 70), gd)
            for k in range(1, 5):
                xk = dx - 0.66 + k * 1.32 / 5; rect(xk - 0.02, 4.2, xk + 0.02, 4.7, sash); rect(xk - 0.02, 4.2, xk + 0.02, 4.7, (0, 0, 0), gd)
            rect(dx - 0.66, 4.43, dx + 0.66, 4.47, sash); rect(dx - 0.66, 4.43, dx + 0.66, 4.47, (0, 0, 0), gd)
        else:                                                                       # 'arch': tall arched light with a sunburst, voussoirs round it
            arc_fill(dx, 4.0, 0.95, creamD); arc_fill(dx, 4.0, 0.8, sash); arc_fill(dx, 4.0, 0.72, gl_dark); arc_fill(dx, 4.0, 0.72, (255, 176, 76), gd)
            for k in range(1, 9):
                ang = math.pi * k / 9; ex, ez = dx + 0.74 * math.cos(ang), 4.0 + 0.74 * math.sin(ang)
                a = _px(S, dx, 4.0); b = _px(S, ex, ez); dr.line([a, b], fill=sash, width=int(S * 0.022)); gd.line([a, b], fill=(0, 0, 0), width=int(S * 0.022))
            for k in range(0, 9):
                ang = math.pi * (k + 0.5) / 9; ex, ez = dx + 0.97 * math.cos(ang), 4.0 + 0.97 * math.sin(ang)
                a = _px(S, dx + 0.8 * math.cos(ang), 4.0 + 0.8 * math.sin(ang)); b = _px(S, ex, ez); dr.line([a, b], fill=hex8('#b8ac90'), width=max(2, int(S * 0.012)))
        rect(dx - 0.72, 4.0 if ds == 'arch' else 4.12, dx + 0.72, 4.08 if ds == 'arch' else 4.2, sash); rect(dx - 0.72, 4.0 if ds == 'arch' else 4.12, dx + 0.72, 4.08 if ds == 'arch' else 4.2, (0, 0, 0), gd)
        # knocker + letterbox + handle
        rect(dx - 0.2, 3.25, dx + 0.2, 3.4, hex8('#d7a843')); rect(dx + 0.38, 2.45, dx + 0.52, 2.58, hex8('#d7a843'))
        rect(dx - 0.25, 1.65, dx + 0.25, 1.75, hex8('#c89a3a'))
    else:
        # shopfront backdrop: stallriser, pilasters, dark glazed interior (the 3D bow window sits in front), fascia
        fc = hex8(p['fascia']); db = p['door_bay']
        rect(0.2, 0.95, 7.8, 4.55, (36, 26, 40)); rect(0.2, 0.95, 7.8, 1.9, tuple(int(c * 0.9) for c in fc))
        rect(0.0, 4.55, 8.0, 5.4, fc); rect(0.0, 4.55, 8.0, 4.62, creamD); rect(0.1, 4.7, 7.9, 4.74, hex8('#d7a843')); rect(0.1, 5.2, 7.9, 5.24, hex8('#d7a843'))
        for px_ in (0.0, 2.4, 7.6): rect(px_, 0.95, px_ + 0.4, 4.55, cream); rect(px_ + 0.04, 1.0, px_ + 0.36, 4.5, tuple(int(c * 0.9) for c in cream))
        dx0 = 0.6 if db == 0 else 5.9
        rect(dx0, 0.95, dx0 + 1.7, 4.4, hex8(p['door'])); rect(dx0 + 0.25, 2.4, dx0 + 1.45, 4.1, gl_dark); rect(dx0 + 0.25, 2.4, dx0 + 1.45, 4.1, (60, 36, 34))
        a = _px(S, dx0 + 0.25, 4.1); b = _px(S, dx0 + 1.45, 2.4); gd.rectangle([a[0], a[1], b[0], b[1]], fill=(255, 168, 66))
        rect(dx0 + 0.8, 2.4, dx0 + 0.9, 4.1, hex8(p['door'])); rect(dx0 + 0.8, 2.4, dx0 + 0.9, 4.1, (0, 0, 0), gd)
    img = img.resize((int(FACADE_W * FPPD), int(FACADE_H * FPPD)), Image.LANCZOS); glow = glow.resize(img.size, Image.LANCZOS)
    a = np.asarray(img).astype('float32') / 255
    # dirt gradient: darker and wetter toward the plinth, soot under the cornice
    zz2 = np.linspace(FACADE_H, 0, a.shape[0])[:, None, None]
    a = a * (0.9 + 0.1 * np.clip(zz2 / 6, 0, 1)) * (1 - 0.1 * np.clip((1.5 - zz2) / 1.5, 0, 1))
    save(a, out); save(np.asarray(glow).astype('float32') / 255, out[:-4] + '_glow.png')

# ----------------------------------------------------------------------------- shop windows (goods), signs
def _shopwin(p, out):
    """Bow-window glass seen from the street: warm lit interior (the whole image is emission), three shelves of goods, glazing bars.
    kind: boots | teapots | pretzels | greens. 5 x 3.4 units."""
    ss = 3; W, H = 640 * ss, 480 * ss; rs = np.random.RandomState(p['seed']); kind = p['kind']
    back = {'boots': (214, 142, 74), 'teapots': (220, 170, 96), 'pretzels': (226, 156, 70), 'greens': (206, 150, 70), 'hats': (222, 156, 96), 'jars': (214, 160, 100)}[kind]
    img = Image.new('RGB', (W, H), back); dr = ImageDraw.Draw(img)
    g = np.asarray(img).astype('float32'); yy, xx = np.mgrid[0:H, 0:W].astype('float32'); xx /= W; yy /= H
    g = g * (0.7 + 0.5 * np.exp(-(((xx - 0.5) * 1.3) ** 2 + ((yy - 0.25) * 1.4) ** 2) * 2.5))[..., None]
    img = Image.fromarray(np.clip(g, 0, 255).astype('uint8'), 'RGB'); dr = ImageDraw.Draw(img)
    shelf_z = (0.36, 0.68, 0.96)
    wood = (96, 56, 30)
    for k, sz in enumerate(shelf_z): dr.rectangle([0, sz * H, W, sz * H + 0.03 * H], fill=wood)
    def item_boot(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.rounded_rectangle([x - 0.2 * sc, y - 0.55 * sc, x + 0.05 * sc, y], radius=int(0.05 * sc), fill=col)               # leg
        dr.rounded_rectangle([x - 0.2 * sc, y - 0.16 * sc, x + 0.32 * sc, y], radius=int(0.07 * sc), fill=col)              # foot
        dr.rectangle([x - 0.2 * sc, y - 0.04 * sc, x + 0.32 * sc, y], fill=(40, 24, 18)); dr.rectangle([x - 0.2 * sc, y - 0.56 * sc, x + 0.05 * sc, y - 0.5 * sc], fill=(238, 220, 170))
    def item_pot(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.ellipse([x - 0.28 * sc, y - 0.42 * sc, x + 0.28 * sc, y], fill=col); dr.ellipse([x - 0.12 * sc, y - 0.52 * sc, x + 0.12 * sc, y - 0.4 * sc], fill=tuple(int(c * 0.8) for c in col))
        dr.polygon([(x + 0.25 * sc, y - 0.32 * sc), (x + 0.46 * sc, y - 0.4 * sc), (x + 0.4 * sc, y - 0.3 * sc), (x + 0.26 * sc, y - 0.14 * sc)], fill=col)
        dr.arc([x - 0.5 * sc, y - 0.36 * sc, x - 0.2 * sc, y - 0.06 * sc], 90, 270, fill=col, width=int(0.07 * sc))
        dr.ellipse([x - 0.05 * sc, y - 0.6 * sc, x + 0.05 * sc, y - 0.5 * sc], fill=(240, 220, 180))
    def item_pretzel(cx, base, s, col):
        x, y = cx * W, base * H - 0.25 * s * H; sc = s * H
        dr.ellipse([x - 0.3 * sc, y - 0.22 * sc, x + 0.05 * sc, y + 0.2 * sc], outline=col, width=int(0.09 * sc)); dr.ellipse([x - 0.05 * sc, y - 0.22 * sc, x + 0.3 * sc, y + 0.2 * sc], outline=col, width=int(0.09 * sc))
        dr.line([(x - 0.2 * sc, y + 0.15 * sc), (x + 0.2 * sc, y - 0.15 * sc)], fill=col, width=int(0.09 * sc)); dr.line([(x + 0.2 * sc, y + 0.15 * sc), (x - 0.2 * sc, y - 0.15 * sc)], fill=col, width=int(0.09 * sc))
    def item_loaf(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.ellipse([x - 0.3 * sc, y - 0.34 * sc, x + 0.3 * sc, y], fill=col)
        for k in (-0.14, 0.0, 0.14): dr.line([(x + k * sc - 0.05 * sc, y - 0.26 * sc), (x + k * sc + 0.04 * sc, y - 0.1 * sc)], fill=tuple(int(c * 0.65) for c in col), width=max(2, int(0.025 * sc)))
    def item_hat(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.polygon([(x - 0.42 * sc, y - 0.12 * sc), (x - 0.12 * sc, y - 0.46 * sc), (x + 0.14 * sc, y - 0.46 * sc), (x + 0.44 * sc, y - 0.12 * sc), (x + 0.3 * sc, y), (x - 0.3 * sc, y)], fill=col)
        dr.line([(x - 0.42 * sc, y - 0.12 * sc), (x - 0.12 * sc, y - 0.46 * sc), (x + 0.14 * sc, y - 0.46 * sc), (x + 0.44 * sc, y - 0.12 * sc)], fill=(222, 190, 90), width=max(2, int(0.03 * sc)))
        dr.ellipse([x - 0.04 * sc, y - 0.42 * sc, x + 0.06 * sc, y - 0.32 * sc], fill=(222, 190, 90))
    def item_jar(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.rounded_rectangle([x - 0.2 * sc, y - 0.42 * sc, x + 0.2 * sc, y], radius=int(0.08 * sc), fill=col); dr.rectangle([x - 0.09 * sc, y - 0.52 * sc, x + 0.09 * sc, y - 0.4 * sc], fill=tuple(int(c * 0.8) for c in col))
        dr.ellipse([x - 0.12 * sc, y - 0.6 * sc, x + 0.12 * sc, y - 0.5 * sc], fill=(150, 100, 60)); dr.rectangle([x - 0.14 * sc, y - 0.3 * sc, x + 0.14 * sc, y - 0.14 * sc], fill=(240, 226, 190))
        dr.rounded_rectangle([x - 0.15 * sc, y - 0.4 * sc, x - 0.1 * sc, y - 0.06 * sc], radius=int(0.02 * sc), fill=tuple(min(255, int(c * 1.3)) for c in col))
    def item_veg(cx, base, s, col):
        x, y = cx * W, base * H; sc = s * H
        dr.ellipse([x - 0.26 * sc, y - 0.5 * sc, x + 0.26 * sc, y], fill=col); dr.arc([x - 0.18 * sc, y - 0.42 * sc, x + 0.18 * sc, y - 0.05 * sc], 200, 340, fill=tuple(int(c * 0.6) for c in col), width=int(0.03 * sc))
    cols = {'boots': [(92, 52, 30), (46, 30, 26), (130, 80, 40), (60, 40, 50)], 'teapots': [(60, 96, 150), (230, 224, 208), (150, 56, 48), (60, 110, 90)],
            'pretzels': [(150, 84, 36), (184, 112, 48), (120, 66, 30), (210, 150, 70)], 'greens': [(64, 130, 58), (210, 90, 36), (150, 40, 50), (222, 196, 70)],
            'hats': [(30, 26, 34), (60, 52, 70), (110, 36, 44), (46, 60, 96)], 'jars': [(60, 150, 120), (170, 60, 90), (70, 100, 190), (220, 170, 50)]}[kind]
    fn = dict(boots=item_boot, teapots=item_pot, pretzels=item_pretzel, greens=item_veg, hats=item_hat, jars=item_jar)[kind]
    for k, sz in enumerate(shelf_z):
        n = 7 if k < 2 else 8; sc = (0.24, 0.24, 0.3)[k]
        for i in range(n):
            cx = (i + 0.5 + rs.uniform(-0.12, 0.12)) / n; c = cols[rs.randint(len(cols))]
            if kind == 'pretzels' and k == 2: item_loaf(cx, sz, sc * 0.95, (176, 108, 48))
            elif kind == 'boots' and k == 0 and i % 2: item_pot(cx, sz, sc * 0.7, c) if False else fn(cx, sz, sc, c)
            else: fn(cx, sz, sc, c)
    # glazing bars: 5 cols x 3 rows, dark wood
    bar = (64, 40, 26)
    for i in range(1, 5): dr.rectangle([i * W / 5 - 0.008 * W, 0, i * W / 5 + 0.008 * W, H], fill=bar)
    dr.rectangle([0, 0, W, 0.02 * H], fill=bar); dr.rectangle([0, 0.99 * H, W, H], fill=bar)
    img = img.resize((640, 480), Image.LANCZOS); save(np.asarray(img).astype('float32') / 255, out)

def sign(p, out):
    """Pictorial hanging sign on a board: no letters. kind: boot | teapot | pretzel. 2 x 2.4 units, alpha cut-out."""
    ss = 3; W, H = 400 * ss, 480 * ss; kind = p['kind']
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(im); bg = hex8(p['bg']); gold = (222, 176, 66, 255)
    dr.rounded_rectangle([0.04 * W, 0.04 * H, 0.96 * W, 0.96 * H], radius=int(0.1 * W), fill=bg + (255,))
    dr.rounded_rectangle([0.07 * W, 0.065 * H, 0.93 * W, 0.935 * H], radius=int(0.08 * W), outline=gold, width=int(0.022 * W))
    cx, cy = 0.5 * W, 0.5 * H; s = 0.6 * W
    if kind == 'boot':
        col = (28, 20, 22, 255); hi = (110, 78, 60, 255)
        dr.rounded_rectangle([cx - 0.28 * s, cy - 0.78 * s, cx + 0.14 * s, cy + 0.38 * s], radius=int(0.08 * s), fill=col)
        dr.rounded_rectangle([cx - 0.28 * s, cy + 0.1 * s, cx + 0.62 * s, cy + 0.48 * s], radius=int(0.16 * s), fill=col)
        dr.rectangle([cx - 0.28 * s, cy + 0.42 * s, cx + 0.62 * s, cy + 0.56 * s], fill=(110, 70, 40, 255))
        dr.rectangle([cx - 0.28 * s, cy - 0.78 * s, cx + 0.14 * s, cy - 0.64 * s], fill=(236, 214, 160, 255))
        dr.rounded_rectangle([cx - 0.2 * s, cy - 0.5 * s, cx - 0.12 * s, cy + 0.2 * s], radius=int(0.03 * s), fill=hi)
    elif kind == 'teapot':
        col = (236, 232, 216, 255); blue = (40, 80, 160, 255)
        dr.ellipse([cx - 0.5 * s, cy - 0.45 * s, cx + 0.5 * s, cy + 0.5 * s], fill=col)
        dr.rectangle([cx - 0.3 * s, cy + 0.38 * s, cx + 0.3 * s, cy + 0.54 * s], fill=col)
        dr.ellipse([cx - 0.28 * s, cy - 0.58 * s, cx + 0.28 * s, cy - 0.3 * s], fill=col); dr.ellipse([cx - 0.09 * s, cy - 0.72 * s, cx + 0.09 * s, cy - 0.58 * s], fill=blue)
        dr.polygon([(cx + 0.4 * s, cy - 0.15 * s), (cx + 0.86 * s, cy - 0.45 * s), (cx + 0.8 * s, cy - 0.3 * s), (cx + 0.42 * s, cy + 0.2 * s)], fill=col)
        dr.arc([cx - 0.95 * s, cy - 0.4 * s, cx - 0.35 * s, cy + 0.25 * s], 90, 270, fill=col, width=int(0.12 * s))
        dr.arc([cx - 0.36 * s, cy - 0.2 * s, cx + 0.36 * s, cy + 0.3 * s], 20, 160, fill=blue, width=int(0.045 * s))
        for k in (-0.22, 0.0, 0.22): dr.ellipse([cx + k * s - 0.04 * s, cy - 0.28 * s, cx + k * s + 0.04 * s, cy - 0.2 * s], fill=blue)
    elif kind == 'hat':
        col = (26, 22, 30, 255)
        dr.polygon([(cx - 0.8 * s, cy + 0.1 * s), (cx - 0.3 * s, cy - 0.5 * s), (cx + 0.3 * s, cy - 0.5 * s), (cx + 0.8 * s, cy + 0.1 * s), (cx + 0.5 * s, cy + 0.34 * s), (cx - 0.5 * s, cy + 0.34 * s)], fill=col)
        dr.line([(cx - 0.8 * s, cy + 0.1 * s), (cx - 0.3 * s, cy - 0.5 * s), (cx + 0.3 * s, cy - 0.5 * s), (cx + 0.8 * s, cy + 0.1 * s)], fill=gold, width=int(0.05 * s))
        dr.ellipse([cx - 0.07 * s, cy - 0.42 * s, cx + 0.07 * s, cy - 0.28 * s], fill=gold)
    elif kind == 'jar':
        glass = (90, 190, 150, 255)
        dr.polygon([(cx - 0.12 * s, cy - 0.7 * s), (cx + 0.12 * s, cy - 0.7 * s), (cx + 0.12 * s, cy - 0.45 * s), (cx + 0.46 * s, cy - 0.1 * s), (cx + 0.46 * s, cy + 0.48 * s), (cx - 0.46 * s, cy + 0.48 * s), (cx - 0.46 * s, cy - 0.1 * s), (cx - 0.12 * s, cy - 0.45 * s)], fill=glass)
        dr.ellipse([cx - 0.16 * s, cy - 0.82 * s, cx + 0.16 * s, cy - 0.66 * s], fill=(150, 100, 60, 255)); dr.rectangle([cx - 0.3 * s, cy + 0.02 * s, cx + 0.3 * s, cy + 0.3 * s], fill=(240, 226, 190, 255))
        dr.rounded_rectangle([cx - 0.38 * s, cy - 0.02 * s, cx - 0.3 * s, cy + 0.42 * s], radius=int(0.03 * s), fill=(190, 240, 215, 255))
    else:
        col = (164, 92, 38, 255); lo = (110, 60, 26, 255); w = int(0.15 * s)
        dr.ellipse([cx - 0.62 * s, cy - 0.48 * s, cx + 0.02 * s, cy + 0.16 * s], outline=col, width=w); dr.ellipse([cx - 0.02 * s, cy - 0.48 * s, cx + 0.62 * s, cy + 0.16 * s], outline=col, width=w)
        dr.line([(cx - 0.35 * s, cy + 0.08 * s), (cx + 0.35 * s, cy - 0.5 * s)], fill=col, width=w); dr.line([(cx + 0.35 * s, cy + 0.08 * s), (cx - 0.35 * s, cy - 0.5 * s)], fill=col, width=w)
        dr.line([(cx - 0.4 * s, cy + 0.1 * s), (cx - 0.7 * s, cy + 0.62 * s)], fill=col, width=w); dr.line([(cx + 0.4 * s, cy + 0.1 * s), (cx + 0.7 * s, cy + 0.62 * s)], fill=col, width=w)
        for i in range(14):
            a = i * 0.8; dr.ellipse([cx - 0.5 * s + 0.07 * s * (i % 7) * 2, cy - 0.12 * s + 0.1 * s * ((i * 3) % 4) - 0.2 * s, cx - 0.47 * s + 0.07 * s * (i % 7) * 2, cy - 0.09 * s + 0.1 * s * ((i * 3) % 4) - 0.2 * s], fill=(236, 220, 180, 255))
    im = im.resize((400, 480), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255
    save(a[..., :3], out, alpha=a[..., 3])

def coach_side(p, out):
    """Hackney-coach body side, 6 x 3.6 units: black-green panels with gold pinstripe, a window with warm glow, a painted crest (shield, no text)."""
    ss = 2; W, H = 480 * ss, 288 * ss; im = Image.new('RGB', (W, H), hex8('#1c3a30')); dr = ImageDraw.Draw(im); gl = Image.new('RGB', (W, H), (0, 0, 0)); gd = ImageDraw.Draw(gl)
    rs = np.random.RandomState(4); a = np.asarray(im).astype('float32')
    yy, xx = np.mgrid[0:H, 0:W].astype('float32'); a = a * (0.92 + 0.14 * np.sin(yy * 0.3 + xx * 0.01 + pnoise(rs, H, W, 4, 8) * 5))[..., None] * (0.9 + 0.2 * pfbm(rs, H, W, 6, 4, 4))[..., None]
    im = Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGB'); dr = ImageDraw.Draw(im)
    gold = (212, 168, 60); dr.rounded_rectangle([0.02 * W, 0.04 * H, 0.98 * W, 0.96 * H], radius=int(0.03 * W), outline=gold, width=int(0.008 * W))
    dr.line([(0.02 * W, 0.58 * H), (0.98 * W, 0.58 * H)], fill=gold, width=int(0.006 * W)); dr.line([(0.02 * W, 0.075 * H), (0.98 * W, 0.075 * H)], fill=(160, 120, 40), width=int(0.004 * W))
    dr.rectangle([0, 0.9 * H, W, H], fill=(16, 24, 22))                                  # skirt
    wx0, wx1, wz0, wz1 = 0.14 * W, 0.86 * W, 0.12 * H, 0.46 * H                          # the glass window with a dark frame
    dr.rounded_rectangle([wx0 - 0.02 * W, wz0 - 0.03 * H, wx1 + 0.02 * W, wz1 + 0.03 * H], radius=int(0.02 * W), fill=(16, 22, 20)); dr.rectangle([wx0, wz0, wx1, wz1], fill=(26, 30, 40))
    dr.rectangle([0.48 * W, wz0, 0.52 * W, wz1], fill=(16, 22, 20))
    # crest on the lower panel: shield with chevron + three studs
    cx, cz = 0.5 * W, 0.78 * H; sw, sh = 0.07 * W, 0.15 * H
    dr.polygon([(cx - sw, cz - sh), (cx + sw, cz - sh), (cx + sw, cz + 0.2 * sh), (cx, cz + sh), (cx - sw, cz + 0.2 * sh)], fill=(140, 36, 40), outline=gold)
    dr.line([(cx - sw, cz - 0.1 * sh), (cx, cz - 0.5 * sh), (cx + sw, cz - 0.1 * sh)], fill=gold, width=int(0.01 * W))
    for k in (-0.4, 0, 0.4): dr.ellipse([cx + k * sw - 0.012 * W, cz + 0.2 * sh - 0.012 * W, cx + k * sw + 0.012 * W, cz + 0.2 * sh + 0.012 * W], fill=gold)
    for sx in (0.22, 0.78):
        dr.ellipse([sx * W - 0.03 * W, cz - 0.04 * H, sx * W + 0.03 * W, cz + 0.06 * H], outline=gold, width=int(0.006 * W))
    im = im.resize((480, 288), Image.LANCZOS); gl = gl.resize((480, 288), Image.LANCZOS)
    save(np.asarray(im).astype('float32') / 255, out); save(np.asarray(gl).astype('float32') / 255, out[:-4] + '_glow.png')

SKY_W = 8192
def _cloud_tile(rs, wpx, hpx, ss=2):
    """One cartoon cumulus (flat-ish bottom, scalloped top) as three crisp masks at wpx x hpx: sil, shade (lower part), rim (upper-left band)."""
    W, H = int(wpx * ss), int(hpx * ss); sil = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sil)
    n = rs.randint(6, 10); base = H * 0.78
    circ = []
    for i in range(n):
        t = (i + rs.uniform(-0.2, 0.2)) / (n - 1); x = W * (0.12 + 0.76 * t); envh = math.sin(math.pi * (0.1 + 0.8 * t)) ** 0.8
        r = H * rs.uniform(0.13, 0.22) * (0.5 + 0.7 * envh); y = base - r * rs.uniform(0.75, 1.0) - envh * H * rs.uniform(0.0, 0.3)
        circ.append((x, y, r))
    # a couple of big domes on top
    for _ in range(2):
        x = W * rs.uniform(0.3, 0.7); r = H * rs.uniform(0.24, 0.32); circ.append((x, base - r * 0.95 - H * 0.12, r))
    for (x, y, r) in circ: d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    d.rounded_rectangle([W * 0.1, base - H * 0.2, W * 0.9, base], radius=int(H * 0.08), fill=255)
    d.rectangle([0, base, W, H], fill=0)                                         # flat bottom
    sil_a = np.asarray(sil).astype('float32') / 255
    def shifted(dx, dy):
        o = Image.new('L', (W, H), 0); od = ImageDraw.Draw(o)
        for (x, y, r) in circ: od.ellipse([x - r + dx, y - r + dy, x + r + dx, y + r + dy], fill=255)
        od.rounded_rectangle([W * 0.1 + dx, base - H * 0.2 + dy, W * 0.9 + dx, base + dy], radius=int(H * 0.08), fill=255); od.rectangle([0, base, W, H], fill=0)
        return np.asarray(o).astype('float32') / 255
    body = shifted(-H * 0.03, -H * 0.055) * sil_a                                 # lit upper-left volume (flat colour)
    rim = shifted(H * 0.016, H * 0.022)
    rim = sil_a * (1 - rim)                                                       # thin band along the top-left edges
    ds = lambda a: np.asarray(Image.fromarray((a * 255).astype('uint8')).resize((int(wpx), int(hpx)), Image.LANCZOS)).astype('float32') / 255
    return ds(sil_a), ds(body), ds(rim)

def splat(p, out):
    """Comic splat decal (RGBA, 512 px): kind 'egg' = irregular white blob with spikes, a golden yolk and little drips; 'cab' = crumpled green leaf pieces with pale veins."""
    S = 512; ss = 2; rs = np.random.RandomState(p['seed']); im = Image.new('RGBA', (S * ss, S * ss), (0, 0, 0, 0)); dr = ImageDraw.Draw(im); c = S * ss / 2
    if p['kind'] == 'egg':
        pts = []
        for i in range(36):
            a = 2 * math.pi * i / 36; r = c * (0.42 + 0.1 * math.sin(3 * a + 1) + 0.05 * math.sin(7 * a)) * (1.25 if i % 6 == 0 else 1.0) * rs.uniform(0.9, 1.1); pts.append((c + r * math.cos(a), c + r * math.sin(a)))
        dr.polygon(pts, fill=(246, 240, 222, 255))
        for k in range(5): a = rs.uniform(0, 6.28); r = c * rs.uniform(0.5, 0.8); dr.ellipse([c + r * math.cos(a) - 14 * ss, c + r * math.sin(a) - 14 * ss, c + r * math.cos(a) + 14 * ss, c + r * math.sin(a) + 14 * ss], fill=(246, 240, 222, 255))
        dr.ellipse([c - c * 0.2, c - c * 0.17, c + c * 0.2, c + c * 0.23], fill=(244, 176, 28, 255)); dr.ellipse([c - c * 0.1, c - c * 0.1, c - c * 0.03, c - c * 0.02], fill=(255, 226, 120, 255))
    else:
        for k in range(9):
            a = 2 * math.pi * k / 9 + rs.uniform(-0.3, 0.3); r = c * rs.uniform(0.15, 0.6); cx, cy = c + r * math.cos(a), c + r * math.sin(a); w, h = c * rs.uniform(0.2, 0.34), c * rs.uniform(0.1, 0.2)
            pts = [(cx + math.cos(t) * w * math.cos(a + 0.5) - math.sin(t) * h * math.sin(a + 0.5), cy + math.cos(t) * w * math.sin(a + 0.5) + math.sin(t) * h * math.cos(a + 0.5)) for t in np.linspace(0, 2 * math.pi, 14)]
            dr.polygon(pts, fill=(96 + int(rs.uniform(0, 40)), 164 + int(rs.uniform(-10, 30)), 70, 255)); dr.line([pts[0], pts[7]], fill=(200, 232, 160, 255), width=3 * ss)
    im = im.resize((S, S), Image.LANCZOS); a = np.asarray(im).astype('float32') / 255; save(a[..., :3], out, alpha=a[..., 3])

def coach_win(p, out):
    """Coach window glass (emission): warm amber lamp-lit interior, a dark pillar in the middle, darker toward the edges (the curtain), 2 : 1."""
    W, H = 256, 128; yy, xx = np.mgrid[0:H, 0:W].astype('float32'); xx /= W; yy /= H
    g = (0.55 + 0.6 * np.exp(-(((xx - 0.5) * 2.2) ** 2 + ((yy - 0.3) * 2.0) ** 2) * 1.2))[..., None] * np.array([1.0, 0.62, 0.24], 'float32')[None, None]
    g = g * (1 - 0.6 * np.clip((0.12 - np.minimum(xx, 1 - xx)) / 0.12, 0, 1))[..., None]
    g = g * np.where(np.abs(xx - 0.5) < 0.025, 0.05, 1.0)[..., None]
    save(np.clip(g, 0, 1.4) / 1.4, out)

def sky_rain(p, out):
    """Sky dome (UV: u = azimuth / 360 from +x CCW, v = (elevation + 15) / 105), 8192 px wide so the edges stay crisp at 720 x 1280.
    Gradient overcast + warm rift at the far end of the street (azimuth 90) + crisp cartoon cumulus drawn as flat shapes: shade, lit body, rim.
    p['mode'] 'rain' (pale slate-lavender day rain) | 'dusk' (deep indigo, orange horizon, peach rims)."""
    W = SKY_W; H = int(round(W * 105 / 360)); rs = np.random.RandomState(p['seed']); dusk = p.get('mode') == 'dusk'
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0; az = (np.arange(W, dtype='float32') + 0.5) / W * 360.0
    def grad(stops):
        e = np.clip(el, -15, 90); o = np.zeros((H, 3), 'float32')
        for ch in range(3): o[:, ch] = np.interp(e, [x[0] for x in stops], [hexf(x[1])[ch] for x in stops])
        return np.repeat(o[:, None, :], W, 1)
    if dusk:
        img = grad([(-15, '#b87c78'), (0, '#f0a468'), (5, '#d890a0'), (14, '#7a78b4'), (40, '#4c58a0'), (90, '#2c3a84')]); gcol, gk = '#ffb870', 0.8
        pal = [('#7c82c0', '#4e5a9c', '#f6b8a0'), ('#6c74b2', '#444e8c', '#f6a67c'), ('#5e66a4', '#3a4480', '#ff9a60')]
    else:
        img = grad([(-15, '#c08878'), (0, '#e8b48c'), (7, '#dca898'), (20, '#aeb4d6'), (45, '#94a4cc'), (90, '#8090bc')]); gcol, gk = '#ffd09a', 0.6
        pal = [('#e6e0ec', '#9ea4d0', '#ffe4c4'), ('#dad8ea', '#929ccc', '#fdd8b8'), ('#ccd0e6', '#8894c4', '#f8cca8')]
    d_az = np.minimum(np.abs(az - 90.0), 360 - np.abs(az - 90.0))[None, :]
    glow = np.exp(-((d_az / 60.0) ** 2) - ((el[:, None] - 4.0) / 22.0) ** 2); img = np.minimum(img + hexf(gcol)[None, None] * glow[..., None] * gk * 0.75, 0.9)    # wide soft glow, capped: no hot spot to mirror as an orb in puddles
    ppd = W / 360.0
    # (elevation range, count, width deg, height factor) far to near layers: small low clouds first, big high clouds last
    layers = [((1.5, 9.0), 26, (14, 26), 0), ((9.0, 22.0), 22, (18, 34), 1), ((22.0, 38.0), 14, (24, 40), 2)]     # nothing above el ~42: the zenith is a plain gradient (no dome-pole arcs)
    for (e0, e1), cnt, (w0, w1), pi_ in layers:
        body_c, shade_c, rim_c = [hexf(c) for c in pal[pi_]]
        for k in range(cnt):
            e = rs.uniform(e0, e1); a = (k + rs.uniform(0.0, 1.0)) / cnt * 360.0; wd = rs.uniform(w0, w1); sc = 1.0 / max(0.45, math.cos(math.radians(min(e, 75))))
            wpx = int(wd * ppd * sc); hpx = int(wpx * rs.uniform(0.34, 0.5))
            if wpx < 40: continue
            sil, bod, rim = _cloud_tile(rs, wpx, hpx)
            cy = int((90 - e) / 105 * H) ; x0 = int(a * ppd - wpx / 2); y0 = cy - int(hpx * 0.78)
            # warm rim stronger toward the glow at azimuth 90
            warm = float(np.exp(-(((a - 90.0 + 180) % 360 - 180) / 90.0) ** 2))
            tile_col = shade_c[None, None] * (1 - bod[..., None]) + body_c[None, None] * bod[..., None]
            tile_col = tile_col * (1 - rim[..., None] * (0.55 + 0.4 * warm)) + rim_c[None, None] * rim[..., None] * (0.55 + 0.4 * warm)
            for sx in (0, -W, W):
                xa = x0 + sx
                xs0, xs1 = max(0, xa), min(W, xa + wpx); ys0, ys1 = max(0, y0), min(H, y0 + hpx)
                if xs1 <= xs0 or ys1 <= ys0: continue
                tx0, ty0 = xs0 - xa, ys0 - y0; sl = (slice(ys0, ys1), slice(xs0, xs1)); tl = (slice(ty0, ty0 + ys1 - ys0), slice(tx0, tx0 + xs1 - xs0))
                m = sil[tl][..., None]; img[sl] = img[sl] * (1 - m) + tile_col[tl] * m
    save(np.clip(img, 0, 1), out)

def brickwall(p, out):
    """Plain brick tile 4 x 4 units (parapets, chimneys, side walls): same bond and mortar as the facades."""
    S = 640; ppd = S / 4.0; rs = np.random.RandomState(p['seed']); yy, xx = np.mgrid[0:S, 0:S].astype('float32') / ppd
    ch, bl = 0.42, 1.0; row = np.floor(yy / ch); off = (row % 2) * bl * 0.5; bx = np.floor((xx + off) / bl)
    bid = ((row * 53 + bx * 17) % 509).astype(int); r = rs.rand(509, 3).astype('float32'); u = (xx + off) % bl; v = yy % ch
    b1, b2 = hexf(BRICKS[p['brick']]), hexf(BRICKS[p['brick2']])
    base = _lerp(b1[None, None], b2[None, None], r[bid, 0][..., None]) * (0.8 + 0.34 * r[bid, 1][..., None]) * (0.9 + 0.2 * pfbm(rs, S, S, 6, 6, 5)[..., None])
    edge = np.minimum(np.minimum(u, bl - u), np.minimum(v, ch - v)); col = base * (1 - 0.2 * np.clip(1 - edge / 0.07, 0, 1)[..., None])
    col = np.where(((u < 0.05) | (v < 0.05))[..., None], hexf('#b8a68c')[None, None] * 0.85, col)
    save(_rgb(col), out)

def halo(p, out):
    S = 256; yy, xx = np.mgrid[0:S, 0:S].astype('float32'); d = np.sqrt(((xx - S / 2) / (S / 2)) ** 2 + ((yy - S / 2) / (S / 2)) ** 2)
    g = np.clip(1 - d, 0, 1) ** 2.2; save(np.repeat(g[..., None], 3, 2), out)

def all_jobs():
    JOBS.clear()
    reg('cobbles', dict(seed=21), cobbles); reg('pave', dict(seed=22), pave); reg('kerb', dict(seed=23), kerb); reg('gutter', dict(seed=24), gutter)
    reg('ripples_a', dict(seed=31, n=7), ripples); reg('ripples_b', dict(seed=32, n=5), ripples)
    for i, (sx, sy) in enumerate(((1.0, 1.0), (1.0, 0.7), (0.75, 1.0), (1.0, 0.85))): reg('pud_' + 'abcd'[i], dict(seed=300 + i, sx=sx, sy=sy), puddle_mask)
    reg('wood', dict(seed=41, col='#8a5e3a', w=0.5), wood); reg('wood_d', dict(seed=42, col='#5e3c26', w=0.4), wood)
    reg('barrel', dict(col='#8c5c34'), barrel); reg('slate', dict(seed=51, col='#44566e'), slate)
    reg('awn_a', dict(n=10, a='#c8483a', b='#efe4cc'), stripes); reg('awn_b', dict(n=8, a='#2f6a52', b='#efe4cc'), stripes)
    reg('lace', dict(col='#f4907e'), lace)
    specs = [('fac_a', 'red', 'ochre', 'house', 1, GREEN, 0.55, 101, 'fan'), ('fac_b', 'brown', 'plum', 'house', 0, OXBLOOD, 0.62, 102, 'transom'), ('fac_c', 'ochre', 'stock', 'house', 2, NAVY, 0.75, 103, 'arch'),
             ('fac_d', 'red', 'rust', 'house', 0, GREEN, 0.6, 104, 'transom'), ('fac_e', 'rust', 'brown', 'house', 1, OXBLOOD, 0.68, 105, 'fan'), ('fac_f', 'plum', 'brown', 'house', 2, GREEN, 0.7, 106, 'arch'),
             ('fac_g', 'stock', 'red', 'house', 1, '#8a2c2c', 0.5, 107, 'arch'), ('fac_h', 'ochre', 'rust', 'house', 0, '#2c4c5c', 0.72, 108, 'fan'), ('fac_i', 'red', 'plum', 'house', 2, '#3a3a52', 0.64, 109, 'transom'),
             ('fac_j', 'brown', 'stock', 'house', 1, '#9a7a2c', 0.58, 110, 'fan'),
             ('fac_s1', 'red', 'ochre', 'shop', 0, GREEN, 0.7, 111, 'fan'), ('fac_s2', 'brown', 'rust', 'shop', 1, OXBLOOD, 0.7, 112, 'fan'), ('fac_s3', 'ochre', 'red', 'shop', 0, NAVY, 0.72, 113, 'fan'),
             ('fac_s4', 'stock', 'ochre', 'shop', 1, GREEN, 0.66, 114, 'fan'), ('fac_s5', 'plum', 'brown', 'shop', 0, '#4a2c5c', 0.7, 115, 'fan'), ('fac_s6', 'rust', 'ochre', 'shop', 1, '#2c4a6a', 0.7, 116, 'fan')]
    fasc = dict(fac_s1='#2f5c46', fac_s2='#6e2433', fac_s3='#2b3f66', fac_s4='#7a5a2c', fac_s5='#4a2c5c', fac_s6='#2c4a6a')
    for nm, b1, b2, g, db, dc, lit, sd, dsty in specs:
        reg(nm, dict(brick=b1, brick2=b2, ground=g, door_bay=db, door=dc, lit=lit, seed=sd, fascia=fasc.get(nm, '#2f5c46'), door_style=dsty), facade)
    for k, sd in (('boots', 61), ('teapots', 62), ('pretzels', 63), ('greens', 64), ('hats', 65), ('jars', 66)): reg('shopwin_' + k, dict(kind=k, seed=sd), _shopwin)
    reg('sign_hat', dict(kind='hat', bg='#6a3a6e'), sign); reg('sign_jar', dict(kind='jar', bg='#2e4a6a'), sign); reg('sign_boot', dict(kind='boot', bg='#2e5a4a'), sign); reg('sign_teapot', dict(kind='teapot', bg='#7a2a34'), sign); reg('sign_pretzel', dict(kind='pretzel', bg='#2b4a7a'), sign)
    reg('brickwall_a', dict(seed=71, brick='red', brick2='ochre'), brickwall); reg('brickwall_b', dict(seed=72, brick='brown', brick2='rust'), brickwall); reg('halo', dict(), halo)
    reg('coach_side', dict(v=2), coach_side); reg('coach_win', dict(v=1), coach_win); reg('splat_egg', dict(seed=5, kind='egg'), splat); reg('splat_cab', dict(seed=6, kind='cab'), splat)
    reg('sky_rain', dict(seed=15, mode='rain'), sky_rain); reg('sky_dusk', dict(seed=17, mode='dusk'), sky_rain)

def ensure(verbose=True, only=None):
    os.makedirs(TEX, exist_ok=True); all_jobs()
    mpath = os.path.join(TEX, 'manifest.json')
    try: man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    except ValueError: man = {}
    out = {}
    for name, (params, fn) in JOBS.items():
        h = hashlib.sha1((TEX_V + fn.__name__ + json.dumps(params, sort_keys=True)).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        out[name + '_glow'] = png[:-4] + '_glow.png'; out[name + '_h'] = png[:-4] + '_h.png'
        if only and name not in only: continue
        if man.get(name) != h or not os.path.exists(png):
            if verbose: print('paint', name, flush=True)
            fn(params, png); man[name] = h
            json.dump(man, open(mpath, 'w'))
    return out

if __name__ == '__main__':
    import time; t = time.time(); ensure(only=sys.argv[1:] or None); print('done %.1fs' % (time.time() - t))
