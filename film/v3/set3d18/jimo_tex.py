#!/usr/bin/env python3
"""jimo_tex.py : painted artwork of the film-18 set (Jimo, Qi vs Yan, 279 BC): rammed earth, ground, grass, tiles, canvas, planks,
layered night water + reflection streaks, red silk with gold five-colour dragons, the night sky dome, the moon, glow cards.
All painted with numpy + PIL, cached in tex_jimo/ keyed by a hash of (TEX_V, name). Bump TEX_V after editing a painter.

    import jimo_tex as JX
    paths = JX.ensure()          # {name: png path};  JX.TS[name] = (w_D, h_D) tile size in D (1 D = one head)
Sky: sky-dome UV space u = azimuth / 360 (0 = +x, ccw), v = (elevation + 15) / 105. Deterministic (fixed seeds)."""
import os, math, json, hashlib, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex_jimo')
TEX_V = 'j12'
TS = {}                                         # name -> (w_D, h_D)
MOON_AZ, MOON_EL = 58.0, 20.0                  # the moon in the dome (degrees)

def hexf(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)], 'float32')

def save(a, path, alpha=None):
    a = np.clip(a, 0, 1)
    if alpha is None: Image.fromarray((a * 255 + 0.5).astype('uint8'), 'RGB').save(path)
    else: Image.fromarray((np.dstack([a, np.clip(alpha, 0, 1)]) * 255 + 0.5).astype('uint8'), 'RGBA').save(path)

def vn(h, w, cell, seed, periodic=True):
    """Smooth value noise 0..1, periodic in both axes."""
    rs = np.random.RandomState(seed); gh, gw = max(2, h // max(1, cell[0] if isinstance(cell, tuple) else cell)), max(2, w // max(1, cell[1] if isinstance(cell, tuple) else cell))
    g = rs.rand(gh, gw).astype('float32'); g3 = np.tile(g, (3, 3))
    im = Image.fromarray(g3, mode='F').resize((3 * w, 3 * h), Image.BICUBIC)
    return np.asarray(im)[h:2 * h, w:2 * w]

def fbm(h, w, cell, seed, octs=4):
    a = np.zeros((h, w), 'float32'); amp = 1.0; tot = 0
    for k in range(octs):
        c = (max(2, (cell[0] if isinstance(cell, tuple) else cell) >> k), max(2, (cell[1] if isinstance(cell, tuple) else cell) >> k)); a += amp * vn(h, w, c, seed + 17 * k); tot += amp; amp *= 0.5
    return a / tot

def lerp(a, b, t): return a + (b - a) * t

def wd(d, fn, x, y, W, H, m):
    """Call fn(x', y') at the tile-wrapped copies of (x, y) that touch the tile."""
    for dx in (-W, 0, W):
        for dy in (-H, 0, H):
            xx, yy = x + dx, y + dy
            if -m <= xx <= W + m and -m <= yy <= H + m: fn(xx, yy)

# ----------------------------------------------------------------------------- rammed earth
def rammed(path, W=8.0, H=4.0, ppd=80, seed=5):
    w, h = int(W * ppd), int(H * ppd); rs = np.random.RandomState(seed); r = random.Random(seed)
    n = 7; yy = np.arange(h, dtype='float32')[:, None] * np.ones((1, w), 'float32'); xx = np.ones((h, 1), 'float32') * np.arange(w, dtype='float32')[None, :]
    wob = (vn(h, w, (h, 120), seed + 1) - 0.5) * 3.6 + (vn(h, w, (h, 40), seed + 2) - 0.5) * 1.2       # wavy layer joints (per x)
    yw = yy + wob[0:1, :] * 1.0                                                                      # constant over y
    layer = np.floor(yw / (h / n)).astype(int) % n; fr = (yw / (h / n)) % 1.0
    pal = [hexf(c) for c in ('#d08440', '#bc7038', '#dc9448', '#c47a3e', '#e09c52', '#b06a36', '#d48a44')]
    jit = rs.uniform(0.92, 1.06, n)[:, None, None] * np.ones((1, 1, 3), 'float32')
    img = np.zeros((h, w, 3), 'float32')
    for i in range(n): img[layer == i] = (pal[i] * jit[i])
    img *= (0.82 + 0.34 * fr)[..., None]                                                              # darker at the bottom of every layer, pale tamped top
    img *= (0.78 + 0.5 * fbm(h, w, 50, seed + 3, 4))[..., None]                                       # soft mottling
    img += (fbm(h, w, 18, seed + 4, 3)[..., None] - 0.5) * 0.10
    j = np.exp(-((fr - 0.0) / 0.035) ** 2) + np.exp(-((fr - 1.0) / 0.035) ** 2)
    img *= (1 - 0.22 * j)[..., None]                                                                  # dark joint
    img += (np.exp(-((fr - 0.1) / 0.05) ** 2) * 0.04)[..., None] * hexf('#fff0d0')                    # highlight lip under the joint
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(int(W * H * 14)):                                                                  # straw / grit strokes along the layer
        x, y = r.uniform(0, w), r.uniform(0, h); L = r.uniform(6, 20); col = r.choice(((70, 40, 22, 120), (240, 210, 150, 110), (90, 55, 30, 110)))
        wd(d, lambda a, b: d.line([(a, b), (a + L, b + r.uniform(-1, 1))], fill=col, width=1), x, y, w, h, 24)
    for _ in range(int(W * H * 30)):
        x, y = r.uniform(0, w), r.uniform(0, h); rr = r.uniform(0.8, 2.2); col = r.choice(((60, 36, 20, 150), (230, 190, 130, 140), (110, 80, 50, 140)))
        wd(d, lambda a, b: d.ellipse([a - rr, b - rr * 0.7, a + rr, b + rr * 0.7], fill=col), x, y, w, h, 6)
    for _ in range(int(W * 5)):                                                                      # hairline cracks running down across the layers
        x, y = r.uniform(0, w), r.uniform(0, h); pts = [(x, y)]
        for q in range(r.randint(3, 7)): x += r.uniform(-4, 4); y += r.uniform(8, 20); pts.append((x, y))
        wd(d, lambda a, b, pts=pts: d.line([(p[0] - pts[0][0] + a, p[1] - pts[0][1] + b) for p in pts], fill=(70, 38, 20, 150), width=1), x - sum(0 for _ in pts), y, w, h, 120) if False else d.line(pts, fill=(70, 38, 20, 140), width=1)
    for k in range(int(W / 2.5)):                                                                    # form-board seams: short vertical steps at layer joints
        x = (k + 0.5) * w / int(W / 2.5) + r.uniform(-8, 8)
        for i in range(n):
            if r.random() < 0.8: wd(d, lambda a, b: d.line([(a, b), (a + r.uniform(-1.5, 1.5), b + h / n)], fill=(60, 34, 20, 130), width=2), x, i * h / n, w, h, 6)
    im.save(path)

def ground(path, W=8.0, H=8.0, ppd=48, seed=9, base='#9a7248', ruts=False):
    w, h = int(W * ppd), int(H * ppd); r = random.Random(seed)
    b = hexf(base); img = np.ones((h, w, 3), 'float32') * b
    img *= (0.8 + 0.4 * fbm(h, w, 70, seed, 4))[..., None]; img += (fbm(h, w, 14, seed + 1, 3)[..., None] - 0.5) * 0.09
    img *= (1 + 0.14 * (fbm(h, w, 200, seed + 2, 2)[..., None] - 0.5) * np.array([1.0, 0.4, -0.5]))
    if ruts:
        xx = np.ones((h, 1), 'float32') * (np.arange(w, dtype='float32')[None, :] / w)
        for c in (0.3, 0.7): img *= (1 - 0.28 * np.exp(-((xx - c) / 0.03) ** 2))[..., None]
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(int(W * H * 14)):
        x, y = r.uniform(0, w), r.uniform(0, h); s = r.uniform(0.8, 2.6); c = r.choice(((190, 160, 120, 90), (80, 55, 36, 110), (150, 120, 90, 90), (220, 195, 155, 80)))
        wd(d, lambda a, bb: (d.ellipse([a - s, bb - s * 0.7, a + s, bb + s * 0.7], fill=c), d.arc([a - s, bb - s * 0.7, a + s, bb + s * 0.7], 200, 340, fill=(255, 235, 200, 60))), x, y, w, h, 8)
    im.save(path)

def grass(path, W=8.0, H=8.0, ppd=48, seed=11):
    w, h = int(W * ppd), int(H * ppd); r = random.Random(seed)
    img = np.ones((h, w, 3), 'float32') * hexf('#3e6a3a'); img *= (0.7 + 0.5 * fbm(h, w, 60, seed, 4))[..., None]
    img = lerp(img, img * hexf('#c8d890'), (fbm(h, w, 160, seed + 5, 2)[..., None] > 0.55) * 0.5)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    cols = ((34, 70, 38, 255), (60, 110, 52, 255), (96, 140, 66, 255), (150, 170, 80, 255), (28, 52, 40, 255), (190, 190, 110, 230))
    for k in range(int(W * H * 90)):
        x, y = r.uniform(0, w), r.uniform(0, h); L = r.uniform(5, 14); a = math.radians(90 + r.uniform(-38, 38)); c = r.choice(cols)
        wd(d, lambda p, q: d.line([(p, q), (p + L * math.cos(a) * 0.45, q - L * math.sin(a))], fill=c, width=2 if r.random() < 0.5 else 1), x, y, w, h, 16)
    for k in range(int(W * H * 1.1)):                                                                 # little stones and flowers
        x, y = r.uniform(0, w), r.uniform(0, h)
        if r.random() < 0.6: wd(d, lambda p, q: d.ellipse([p - 3, q - 2, p + 3, q + 2], fill=(150, 150, 150, 255), outline=(60, 60, 70, 255)), x, y, w, h, 5)
        else: wd(d, lambda p, q: d.ellipse([p - 1.5, q - 1.5, p + 1.5, q + 1.5], fill=r.choice(((250, 230, 120, 255), (250, 250, 240, 255), (240, 160, 190, 255)))), x, y, w, h, 3)
    im.save(path)

def tiles(path, W=4.0, H=4.0, ppd=64, seed=21, base='#454a60', hi='#7a82a2'):
    w, h = int(W * ppd), int(H * ppd); r = random.Random(seed); cw = w // 16; rh = h // 12
    img = np.ones((h, w, 3), 'float32') * hexf(base)
    im = Image.fromarray((img * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA'); b = hexf(base); hh = hexf(hi)
    for c in range(16):
        x0 = c * cw
        for row in range(12):
            y0 = row * rh; v = r.uniform(0.82, 1.18); col = tuple(int(255 * min(1, x * v)) for x in b)
            d.rectangle([x0, y0, x0 + cw, y0 + rh], fill=col)
            for t in range(cw):                                                                      # convex tile: highlight at 35 %, dark at the valley
                f = (t + 0.5) / cw; k = 0.55 * math.exp(-((f - 0.33) / 0.16) ** 2) - 0.45 * (f > 0.9 or f < 0.07)
                cc = tuple(int(255 * min(1, max(0, b[i] * v * (1 - 0.0) + (hh[i] - b[i]) * max(0, k)) - 0.2 * max(0, -k))) for i in range(3))
                d.line([(x0 + t, y0), (x0 + t, y0 + rh)], fill=cc + (255,))
            d.rectangle([x0, y0 + rh - 3, x0 + cw, y0 + rh], fill=(18, 20, 34, 200))                  # lower rim shadow of each tile
            d.line([(x0, y0 + rh - 4), (x0 + cw, y0 + rh - 4)], fill=(220, 226, 255, 90), width=1)
    d.rectangle([0, 0, w, 0], fill=(18, 20, 34, 200)); im.save(path)

def canvas(path, W=4.0, H=4.0, ppd=64, seed=31, base='#d8c090', stitch='#8a6a44', hide=False):
    w, h = int(W * ppd), int(H * ppd); r = random.Random(seed)
    b = hexf(base); img = np.ones((h, w, 3), 'float32') * b
    img *= (0.84 + 0.3 * fbm(h, w, 40, seed, 4))[..., None]
    wv = (np.sin(np.arange(w) * 1.9)[None, :] * np.sin(np.arange(h) * 1.9)[:, None]) * 0.035; img += wv[..., None]
    if hide: img = lerp(img, img * hexf('#8a5a3c') * 1.3, (fbm(h, w, 80, seed + 3, 3)[..., None] > 0.55) * 0.7)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    sc = tuple(int(255 * x) for x in hexf(stitch))
    for k in range(int(W)):                                                                           # panel seams with stitches
        x = k * ppd
        d.line([(x, 0), (x, h)], fill=(70, 46, 26, 120), width=2)
        for y in range(0, h, 9): d.line([(x - 3, y), (x + 3, y + 3)], fill=sc + (230,), width=1)
    for k in range(int(H / 2)):
        y = k * 2 * ppd; d.line([(0, y), (w, y)], fill=(70, 46, 26, 100), width=2)
    for _ in range(14):                                                                               # patches and stains
        x, y = r.uniform(0, w), r.uniform(0, h); s = r.uniform(10, 24); d.rectangle([x, y, x + s, y + s * 0.8], fill=r.choice(((190, 150, 100, 110), (120, 90, 60, 90))), outline=(80, 56, 34, 150))
    im.save(path)

def planks(path, W=4.0, H=4.0, ppd=64, seed=41, base='#8a5a36'):
    w, h = int(W * ppd), int(H * ppd); r = random.Random(seed); n = 8; b = hexf(base)
    img = np.zeros((h, w, 3), 'float32'); gr = fbm(h, w, (4, 90), seed, 3)
    for i in range(n):
        v = r.uniform(0.8, 1.15); img[i * h // n:(i + 1) * h // n] = b * v
    img *= (0.8 + 0.4 * gr)[..., None]
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for i in range(n):
        y = i * h // n; d.line([(0, y), (w, y)], fill=(30, 18, 10, 200), width=2); d.line([(0, y + 2), (w, y + 2)], fill=(255, 220, 170, 70), width=1)
        for _ in range(3):
            x = r.uniform(0, w); d.line([(x, y + 3), (x + r.uniform(20, 60), y + 3 + r.uniform(-1, 1))], fill=(50, 30, 16, 100), width=1)
        for x in (r.uniform(0, w // 2), r.uniform(w // 2, w)): d.ellipse([x - 2, y + h // n // 2 - 2, x + 2, y + h // n // 2 + 2], fill=(40, 30, 24, 230))
    im.save(path)

# ----------------------------------------------------------------------------- water, streaks, glow
def water(path, W=16.0, H=16.0, ppd=32, seed=51):
    w, h = int(W * ppd), int(H * ppd)
    base = np.ones((h, w, 3), 'float32') * hexf('#1c2c68'); y = (np.arange(h, dtype='float32') / h)[:, None] * np.ones((1, w), 'float32')
    streak = fbm(h, w, (3, 70), seed, 3); streak2 = fbm(h, w, (6, 140), seed + 7, 2)
    bands = np.clip((streak - 0.52) * 7, 0, 1)                                                          # layered horizontal ripple bands
    dark = np.clip((0.46 - streak2) * 6, 0, 1)
    img = lerp(base, hexf('#3a54a8'), bands[..., None] * 0.65); img = lerp(img, hexf('#101a46'), dark[..., None] * 0.55)
    img = lerp(img, hexf('#7a8ad0'), (np.clip((streak - 0.64) * 9, 0, 1))[..., None] * 0.55)
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA'); r = random.Random(seed)
    for _ in range(int(W * H * 4)):                                                                     # glint dashes
        x, yy = r.uniform(0, w), r.uniform(0, h); L = r.uniform(4, 14)
        wd(d, lambda a, b: d.line([(a, b), (a + L, b)], fill=r.choice(((220, 230, 255, 200), (255, 226, 160, 200), (150, 170, 230, 160))), width=1), x, yy, w, h, 16)
    im.save(path)

def streak(path, w=96, h=512, seed=61):
    """Reflection of a light on water: v = 0 at the object, 1 far toward the camera; layered, broken by ripples. White RGB + alpha."""
    r = np.random.RandomState(seed); a = np.zeros((h, w), 'float32'); xs = (np.arange(w, dtype='float32') - w / 2) / (w / 2)
    rowphase = r.rand(h) * 6.28; off = np.cumsum(r.randn(h)) * 0.01; off -= off.mean()
    for j in range(h):
        t = j / h; sp = 0.10 + 0.20 * t; x0 = off[j] * (0.5 + 2 * t)
        band = 0.15 if math.sin(t * 70 + 2 * math.sin(t * 13 + rowphase[j] * 0.0)) < -0.35 else 1.0               # layered: gaps in the reflection
        a[j] = np.exp(-(((xs - x0) / sp) ** 2)) * (1 - t) ** 0.9 * band * (0.7 + 0.3 * math.sin(j * 0.9 + rowphase[j]))
    a = np.clip(a * 1.1, 0, 1); save(np.ones((h, w, 3), 'float32'), path, a)

def glow(path, s=256):
    y, x = np.mgrid[0:s, 0:s].astype('float32'); r = np.hypot(x - s / 2 + 0.5, y - s / 2 + 0.5) / (s / 2)
    a = np.clip(1 - r, 0, 1) ** 2.2 * 0.9 + np.exp(-(r / 0.18) ** 2) * 0.6
    save(np.ones((s, s, 3), 'float32'), path, np.clip(a, 0, 1))

def pool(path, s=256):
    y, x = np.mgrid[0:s, 0:s].astype('float32'); r = np.hypot(x - s / 2 + 0.5, y - s / 2 + 0.5) / (s / 2)
    save(np.ones((s, s, 3), 'float32'), path, np.clip(np.exp(-(r / 0.55) ** 2.4) * (1 - r ** 6), 0, 1))

def moon(path, s=512):
    rs = np.random.RandomState(71); y, x = np.mgrid[0:s, 0:s].astype('float32'); u = (x - s / 2 + 0.5) / (s / 2); v = (y - s / 2 + 0.5) / (s / 2); r = np.hypot(u, v)
    img = np.ones((s, s, 3), 'float32') * hexf('#fff0b8'); img = lerp(img, hexf('#ffd88a'), np.clip(r, 0, 1)[..., None] ** 2 * 0.7)
    for k in range(9):                                                                                  # soft maria and craters
        cx, cy, rr = rs.uniform(-0.55, 0.55), rs.uniform(-0.55, 0.55), rs.uniform(0.1, 0.26)
        if math.hypot(cx, cy) + rr < 0.95: img = lerp(img, hexf('#e8c47a'), (np.exp(-(np.hypot(u - cx, v - cy) / rr) ** 3) * 0.55)[..., None])
    a = np.clip((1 - r) * s / 2 / 1.5, 0, 1); save(img, path, a)

# ----------------------------------------------------------------------------- silk with gold five-colour dragons
def silk(path, W=4.0, H=2.0, ppd=128, seed=81):
    w, h = int(W * ppd), int(H * ppd); S = 2; im = Image.new('RGB', (w * S, h * S), (176, 22, 30)); d = ImageDraw.Draw(im, 'RGBA'); r = random.Random(seed)
    A = np.asarray(im, 'float32') / 255; ww = (np.sin(np.arange(w * S)[None, :] * 0.9) * np.sin(np.arange(h * S)[:, None] * 0.9)) * 0.02
    im = Image.fromarray((np.clip((A * 255 + ww[..., None] * 255), 0, 255)).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    gold = (246, 196, 74, 255); gold_d = (160, 100, 20, 255); five = [(36, 120, 200), (46, 168, 96), (244, 214, 70), (245, 245, 235), (30, 30, 40)]
    bw = int(0.22 * ppd * S)                                                                             # gold border bands (top and bottom)
    for y0 in (0, h * S - bw):
        d.rectangle([0, y0, w * S, y0 + bw], fill=(120, 14, 24, 255))
        for k in range(0, w * S, 14 * S): d.rectangle([k, y0 + bw * 0.3, k + 8 * S, y0 + bw * 0.7], fill=five[(k // (14 * S)) % 5] + (255,))
        d.line([(0, y0 + (bw if y0 == 0 else 0)), (w * S, y0 + (bw if y0 == 0 else 0))], fill=gold, width=3 * S)
    # the dragon: a thick sinuous body with scales, claws, a horned head, five-colour clouds around it
    cy = h * S / 2; amp = 0.30 * h * S; n = 160
    pts = [(i / n * w * S, cy + amp * math.sin(i / n * 2 * math.pi * 2.0 + 0.5) * (0.9 + 0.1 * math.sin(i * 0.3))) for i in range(n + 1)]
    for i in range(n):
        t = i / n; th = (0.085 + 0.05 * math.sin(t * 6.28 * 2)) * h * S
        d.line([pts[i], pts[i + 1]], fill=gold_d, width=int(th + 6 * S)); d.line([pts[i], pts[i + 1]], fill=gold, width=int(th))
    for i in range(0, n, 4):                                                                              # scales (arcs) in the five colours
        x, y = pts[i]; rr = 0.05 * h * S; d.arc([x - rr, y - rr, x + rr, y + rr], 200, 340, fill=five[(i // 4) % 5] + (255,), width=int(2.5 * S))
    for i in range(6, n, 24):                                                                             # claws / spines
        x, y = pts[i]; sgn = 1 if (i // 24) % 2 == 0 else -1
        d.polygon([(x - 6 * S, y), (x + 6 * S, y), (x, y + sgn * 0.17 * h * S)], fill=gold, outline=gold_d)
    hx, hy = pts[n // 5]; hr = 0.13 * h * S                                                              # head
    d.ellipse([hx - hr, hy - hr * 0.8, hx + hr, hy + hr * 0.8], fill=gold, outline=gold_d, width=3 * S); d.ellipse([hx - hr * 0.1, hy - hr * 0.35, hx + hr * 0.25, hy - hr * 0.05], fill=(20, 20, 30, 255))
    d.polygon([(hx - hr * 0.1, hy - hr * 0.7), (hx - hr * 0.5, hy - hr * 1.5), (hx + hr * 0.2, hy - hr * 0.8)], fill=gold_d)
    d.polygon([(hx + hr * 0.2, hy - hr * 0.7), (hx + hr * 0.4, hy - hr * 1.5), (hx + hr * 0.7, hy - hr * 0.6)], fill=gold_d)
    for k in range(int(W * 3)):                                                                           # five-colour scroll clouds
        x, y = r.uniform(0, w * S), r.choice((0.22, 0.78)) * h * S + r.uniform(-0.06, 0.06) * h * S; c = five[k % 5]; rr = r.uniform(0.04, 0.07) * h * S
        for q in range(3): d.arc([x - rr * (1 - 0.28 * q), y - rr * (1 - 0.28 * q), x + rr * (1 - 0.28 * q), y + rr * (1 - 0.28 * q)], 20 + 90 * q, 300 + 90 * q, fill=c + (255,), width=int(2.6 * S))
        d.line([(x - rr * 1.6, y + rr), (x + rr * 1.2, y + rr)], fill=gold, width=2 * S)
    im.resize((w, h), Image.LANCZOS).save(path)

# ----------------------------------------------------------------------------- night sky dome
def sky(path, W=6144, maz=58.0, mel=20.0):
    H = int(W * 105 / 360); rs = np.random.RandomState(7)
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0; az = (np.arange(W, dtype='float32') + 0.5) / W * 360.0
    EL = el[:, None] * np.ones((1, W), 'float32'); AZ = np.ones((H, 1), 'float32') * az[None, :]
    def grad(stops):
        e = np.clip(el, -15, 90); out = np.zeros((H, 3), 'float32')
        for c in range(3): out[:, c] = np.interp(e, [s[0] for s in stops], [hexf(s[1])[c] for s in stops])
        return np.repeat(out[:, None, :], W, 1)
    img = grad([(-15, '#44308f'), (0, '#7456b2'), (3, '#7a5cb8'), (9, '#5a449e'), (22, '#3a2a90'), (45, '#281a78'), (90, '#1e1466')])
    def ang(a0, e0):
        da = (AZ - a0 + 180) % 360 - 180; return np.hypot(da * np.cos(np.radians(e0)), EL - e0)
    dm = ang(maz, mel)
    img += (np.exp(-(dm / 30) ** 2) * 0.28)[..., None] * hexf('#8a78c8') + (np.exp(-(dm / 9) ** 2) * 0.35)[..., None] * hexf('#ffd890')   # moon glow on the sky
    wa = np.exp(-(((AZ - 90 + 180) % 360 - 180) / 70) ** 2) * np.exp(-((EL - 1.5) / 5.5) ** 2)                                           # warm glow of the lit city
    img = lerp(img, hexf('#e08a5a') * 0.85, (wa * 0.55)[..., None])
    # thin cartoon cloud bands: stretched noise thresholded to crisp edges, lit gold/rose on the moon side, violet-blue elsewhere
    for k, (e0, e1, thr, seed) in enumerate(((5, 9.5, 0.50, 1), (11.5, 16, 0.54, 2), (20, 25, 0.56, 3), (30, 34, 0.60, 4), (40, 43, 0.62, 5))):
        n = fbm(H, W, (14 + 5 * k, 520), seed * 11, 3); prof = np.exp(-(((EL - (e0 + e1) / 2) / ((e1 - e0) / 2)) ** 4))
        m = np.clip((n - thr + 0.12 * (prof - 0.5)) * 18, 0, 1) * prof
        edge = np.clip(m - np.roll(m, 3, 0), 0, 1)                                                                                         # lit lower rim
        col = lerp(np.ones((H, W, 3), 'float32') * hexf('#5a54b4'), hexf('#f0b890'), np.clip(np.exp(-(dm / 38) ** 2) * 1.1, 0, 1)[..., None])
        img = lerp(img, col, (m * 0.7)[..., None]); img = lerp(img, hexf('#ffe2b0'), (np.clip(edge * 2.6, 0, 1) * np.exp(-(dm / 55) ** 2))[..., None] * 0.7)
    # stars
    N = 3800; ys = rs.rand(N) * H; xs = rs.rand(N) * W; bri = rs.pareto(1.6, N) * 0.22 + 0.2; st = np.zeros((H, W, 3), 'float32')
    tints = [hexf('#ffffff'), hexf('#d6e4ff'), hexf('#fff0d0'), hexf('#ffd6b8')]
    for y_, x_, b_ in zip(ys, xs, bri):
        e_ = 90 - y_ / H * 105
        if e_ < 5: continue
        vis = min(1.0, (e_ - 5) / 14) * np.exp(-(((x_ / W * 360 - maz + 180) % 360 - 180) ** 2 + (e_ - mel) ** 2) / 900.0 * 0.0)
        b_ = min(b_, 3.0) * vis; rad = 0.9 + 0.5 * min(b_, 2.0); t = tints[int(x_) % 4]
        x0, x1 = int(x_ - 3 * rad) - 1, int(x_ + 3 * rad) + 2; y0, y1 = max(0, int(y_ - 3 * rad) - 1), min(H, int(y_ + 3 * rad) + 2)
        if x0 < 0 or x1 > W: continue
        gx = np.arange(x0, x1) + 0.5 - x_; gy = np.arange(y0, y1) + 0.5 - y_
        st[y0:y1, x0:x1] += (np.exp(-(gy[:, None] ** 2 + gx[None, :] ** 2) / (2 * (rad * 0.5) ** 2)) * b_)[..., None] * t
    dim = np.clip(1 - np.exp(-(dm / 22) ** 2) * 0.95, 0, 1)[..., None]
    img += st * dim
    save(np.clip(img, 0, 1), path)

# ----------------------------------------------------------------------------- registry
def jobs():
    TS.clear()
    J = {}
    def add(name, fn, size, **kw): J[name] = (fn, kw); TS[name] = size
    add('rammed', rammed, (8.0, 4.0)); add('rammed_d', rammed, (8.0, 4.0), seed=15)
    add('earth', ground, (8.0, 8.0), base='#9c7448'); add('road', ground, (8.0, 8.0), seed=19, base='#a88050', ruts=True); add('bank', ground, (8.0, 8.0), seed=23, base='#7a5a3a')
    add('grass', grass, (8.0, 8.0)); add('grass2', grass, (8.0, 8.0), seed=13)
    add('tiles', tiles, (4.0, 4.0)); add('tiles_d', tiles, (4.0, 4.0), seed=22, base='#3a4056', hi='#6a7292')
    add('canvas', canvas, (4.0, 4.0)); add('canvas_red', canvas, (4.0, 4.0), seed=33, base='#a0402e', stitch='#e8c080'); add('hide', canvas, (4.0, 4.0), seed=35, base='#a07048', hide=True)
    add('planks', planks, (4.0, 4.0)); add('planks_d', planks, (4.0, 4.0), seed=43, base='#5a3a24')
    add('water', water, (16.0, 16.0)); add('streak', streak, (1.0, 8.0)); add('glow', glow, (1.0, 1.0)); add('pool', pool, (1.0, 1.0)); add('moon', moon, (1.0, 1.0))
    add('silk', silk, (4.0, 2.0)); add('sky_WALL', sky, (360.0, 105.0), maz=58.0, mel=20.0); add('sky_CAMP', sky, (360.0, 105.0), maz=74.0, mel=19.0); add('sky_HOLES', sky, (360.0, 105.0), maz=250.0, mel=36.0)
    return J

def ensure(verbose=True):
    os.makedirs(TEX, exist_ok=True); out = {}
    for name, (fn, kw) in jobs().items():
        png = os.path.join(TEX, name + '.png'); out[name] = png
        h = hashlib.sha1((TEX_V + name + json.dumps(kw, sort_keys=True)).encode()).hexdigest()[:12]; hp = png + '.h'
        if os.path.exists(png) and os.path.exists(hp) and open(hp).read() == h: continue
        fn(png, **kw); open(hp, 'w').write(h)
        if verbose: print('painted', name, flush=True)
    return out

if __name__ == '__main__':
    p = ensure(); print(len(p), 'textures')
