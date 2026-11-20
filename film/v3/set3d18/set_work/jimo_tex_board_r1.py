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
TEX_V = 'j15'
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

# ----------------------------------------------------------------------------- rammed earth (below)
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

def rammed(path, W=8.0, H=4.0, ppd=80, seed=5):
    """Ochre loess rammed earth: courses 0.57 D tall (jittered ochre), dark tamping joints #8e6438 0.12 D tall, wash stains, erosion runnels,
    repaired patches, straw/grit strokes, hairline cracks, form-board seams.  Base #b8874e (H 32 S 0.58)."""
    w, h = int(W * ppd), int(H * ppd); rs = np.random.RandomState(seed); r = random.Random(seed)
    n = 7; yy = np.arange(h, dtype='float32')[:, None] * np.ones((1, w), 'float32')
    wob = (vn(h, w, (h, 120), seed + 1) - 0.5) * 3.2 + (vn(h, w, (h, 40), seed + 2) - 0.5) * 1.0
    yw = yy + wob[0:1, :]; ch = h / n
    layer = np.floor(yw / ch).astype(int) % n; fr = (yw / ch) % 1.0
    pal = [hexf(c) for c in ('#b8874e', '#c0904f', '#ae7e48', '#b98a52', '#c4944f', '#a97945', '#bd8c4c')]
    img = np.zeros((h, w, 3), 'float32')
    for i in range(n): img[layer == i] = pal[i] * rs.uniform(0.95, 1.05)
    img *= (0.88 + 0.22 * fr)[..., None]                                                               # darker under each course, pale tamped top
    img *= (0.80 + 0.40 * fbm(h, w, 50, seed + 3, 4))[..., None]                                       # soft mottling
    img += (fbm(h, w, 18, seed + 4, 3)[..., None] - 0.5) * 0.08
    jw = 0.12 * ppd / ch                                                                               # joint band 0.12 D tall (fraction of a course)
    j = np.clip(1 - np.minimum(fr, 1 - fr) / (jw * 0.5 + 1e-6), 0, 1) ** 0.6                           # 1 at the joint centre
    img = lerp(img, np.ones_like(img) * hexf('#8e6438') * (0.9 + 0.2 * fbm(h, w, 20, seed + 6, 2))[..., None], (j * 0.85)[..., None])
    img += (np.exp(-((fr - 0.12) / 0.05) ** 2) * 0.05)[..., None] * hexf('#fff0c8')                    # lit lip just above the joint
    # wash stains: tall soft vertical streaks (rain wash, salt) and big darker blotches
    st = fbm(h, w, (h, 10), seed + 8, 3); st2 = fbm(h, w, (h // 2, 24), seed + 9, 3)
    img *= (1 - np.clip((st - 0.55) * 2.2, 0, 1) * 0.30)[..., None]
    img = lerp(img, img * hexf('#9a7a62') * 1.18, (np.clip((st2 - 0.60) * 3.0, 0, 1) * 0.55)[..., None])
    img = lerp(img, img * 1.12 * hexf('#ffe2b0'), (np.clip((0.38 - st2) * 3.0, 0, 1) * 0.35)[..., None])
    # erosion runnels: thin dark vertical lines widening downward and fading
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for _ in range(int(W * 3)):
        x = r.uniform(0, w); y0 = r.uniform(0, h * 0.6); L = r.uniform(h * 0.15, h * 0.55); k = 14
        for q in range(k):
            t = q / k; xx = x + math.sin(t * 5 + x) * 2 + t * r.uniform(-2, 2) * 0.3
            d.line([(xx, y0 + L * t), (xx + 0.5, y0 + L * (t + 1.0 / k))], fill=(80, 52, 28, int(150 * (1 - t) ** 0.7)), width=1 + int(2.2 * t))
    for _ in range(3):                                                                                # repaired patches: slightly different earth, dark rim
        x, y = r.uniform(30, w - 100), r.uniform(20, h - 60); pw, ph = r.uniform(40, 90), r.uniform(20, 40)
        d.rectangle([x, y, x + pw, y + ph], fill=r.choice(((205, 160, 100, 120), (150, 110, 70, 120))), outline=(95, 62, 34, 170), width=2)
        for k in range(5): d.line([(x + k * pw / 5, y), (x + k * pw / 5 + 2, y + ph)], fill=(95, 62, 34, 90), width=1)
    for _ in range(int(W * H * 14)):                                                                  # straw / grit strokes
        x, y = r.uniform(0, w), r.uniform(0, h); L = r.uniform(6, 20); col = r.choice(((100, 62, 30, 110), (230, 190, 120, 105), (120, 80, 40, 100)))
        wd(d, lambda a, b: d.line([(a, b), (a + L, b + r.uniform(-1, 1))], fill=col, width=1), x, y, w, h, 24)
    for _ in range(int(W * H * 30)):
        x, y = r.uniform(0, w), r.uniform(0, h); rr = r.uniform(0.8, 2.2); col = r.choice(((90, 56, 28, 140), (225, 185, 120, 130), (130, 94, 56, 130)))
        wd(d, lambda a, b: d.ellipse([a - rr, b - rr * 0.7, a + rr, b + rr * 0.7], fill=col), x, y, w, h, 6)
    for _ in range(int(W * 5)):
        x, y = r.uniform(0, w), r.uniform(0, h); pts = [(x, y)]
        for q in range(r.randint(3, 7)): x += r.uniform(-4, 4); y += r.uniform(8, 20); pts.append((x, y))
        d.line(pts, fill=(80, 48, 24, 150), width=1)
    for k in range(int(W / 2.5)):
        x = (k + 0.5) * w / int(W / 2.5) + r.uniform(-8, 8)
        for i in range(n):
            if r.random() < 0.8: wd(d, lambda a, b: d.line([(a, b), (a + r.uniform(-1.5, 1.5), b + h / n)], fill=(80, 52, 28, 130), width=2), x, i * h / n, w, h, 6)
    im.save(path)

def rain(path, w=256, h=512, seed=3):
    """Dark rain streaks hanging under a parapet / eaves: alpha card, dark blue-violet, v = 0 at the top (strongest)."""
    rs = np.random.RandomState(seed); a = np.zeros((h, w), 'float32'); yv = (np.arange(h, dtype='float32') / h)[:, None]
    for k in range(34):
        x = rs.randint(0, w); ww = rs.uniform(2, 9); L = rs.uniform(0.25, 1.0); s = rs.uniform(0.3, 0.9)
        xs = np.arange(w, dtype='float32')[None, :]; col = np.exp(-((xs - x) / ww) ** 2) * np.clip(1 - yv / L, 0, 1) ** 1.4 * s
        a = np.maximum(a, col)
    a *= (0.6 + 0.8 * fbm(h, w, (30, 8), seed, 2)); img = np.ones((h, w, 3), 'float32') * hexf('#1c1840'); save(img, path, np.clip(a * 0.85, 0, 1))

# ----------------------------------------------------------------------------- moon
def moon(path, s=512):
    rs = np.random.RandomState(71); y, x = np.mgrid[0:s, 0:s].astype('float32'); u = (x - s / 2 + 0.5) / (s / 2); v = (y - s / 2 + 0.5) / (s / 2); r = np.hypot(u, v)
    img = np.ones((s, s, 3), 'float32') * hexf('#f2f6ff'); img = lerp(img, hexf('#c8d8f8'), np.clip(r, 0, 1)[..., None] ** 2 * 0.6)
    for k in range(9):
        cx, cy, rr = rs.uniform(-0.55, 0.55), rs.uniform(-0.55, 0.55), rs.uniform(0.1, 0.26)
        if math.hypot(cx, cy) + rr < 0.95: img = lerp(img, hexf('#aab8e0'), (np.exp(-(np.hypot(u - cx, v - cy) / rr) ** 3) * 0.5)[..., None])
    a = np.clip((1 - r) * s / 2 / 1.5, 0, 1); save(img, path, a)

# ----------------------------------------------------------------------------- red silk with large painted five-colour dragons (the fire ox's coat)
def silk(path, W=4.0, H=2.0, ppd=128, seed=81):
    """Crimson silk #a8142a..#c42a2a; u 0..1 along the ox, v 0..1 from the spine (0) down to the hem (1). Two large readable motifs: a coiling gold
    dragon (green-teal mane, white claws) on the flank and a medallion of clouds near the shoulder; gold lined hem with a scalloped scroll border."""
    w, h = int(W * ppd), int(H * ppd); S = 2; r = random.Random(seed)
    A = np.ones((h * S, w * S, 3), 'float32') * hexf('#b8182a'); yy = np.linspace(0, 1, h * S)[:, None]
    A *= (0.94 + 0.12 * fbm(h * S, w * S, 60, seed, 3))[..., None]; A = lerp(A, A * hexf('#d83a30'), (np.sin(np.arange(w * S)[None, :] * 0.5) * 0.5 + 0.5)[..., None] * 0.05)
    im = Image.fromarray((np.clip(A, 0, 1) * 255).astype('uint8'), 'RGB'); d = ImageDraw.Draw(im, 'RGBA')
    gold = (224, 176, 74, 255); gold_d = (150, 96, 28, 255); teal = (62, 143, 122, 255); cream = (240, 230, 208, 255); blue = (44, 90, 160, 255)
    W2, H2 = w * S, h * S
    # hem: gold line + scallops
    hy = int(H2 * 0.90)
    d.rectangle([0, hy, W2, H2], fill=(122, 14, 30, 255)); d.line([(0, hy), (W2, hy)], fill=gold, width=4 * S)
    sc = W2 // 26
    for k in range(26): d.pieslice([k * sc, hy - sc // 3, (k + 1) * sc, hy + sc // 1.5], 0, 180, fill=gold if k % 2 else teal)
    # big dragon: S-curve along the flank, thick, scaled
    n = 200; pts = []
    for i in range(n + 1):
        t = i / n; x = (0.10 + 0.80 * t) * W2; y = H2 * (0.42 + 0.20 * math.sin(t * 2 * math.pi * 1.25 + 0.4) + 0.04 * math.sin(t * 17))
        pts.append((x, y))
    for i in range(n):
        t = i / n; th = (0.035 + 0.075 * math.sin(math.pi * min(1, t * 1.25 + 0.1)) ** 0.8 * (1 - 0.45 * t)) * H2
        d.line([pts[i], pts[i + 1]], fill=gold_d, width=int(th + 8 * S)); d.line([pts[i], pts[i + 1]], fill=gold, width=int(th))
    for i in range(0, n, 3):
        x, y = pts[i]; rr = (0.035 + 0.04 * math.sin(math.pi * min(1, i / n * 1.25 + 0.1))) * H2
        d.arc([x - rr, y - rr, x + rr, y + rr], 200, 340, fill=[teal, cream, blue][(i // 3) % 3], width=3 * S)
    for i in range(10, n - 5, 22):                                                                   # mane / dorsal flames (teal) and claws (cream)
        x, y = pts[i]; sg = -1 if (i // 22) % 2 == 0 else 1; ln = 0.14 * H2
        d.polygon([(x - 8 * S, y), (x + 8 * S, y), (x + sg * 4 * S, y + sg * ln)], fill=teal if sg < 0 else cream, outline=gold_d)
    hx, hy2 = pts[int(n * 0.12)]; hr = 0.16 * H2                                                       # head (left end), horns, whiskers, eye, jaw
    d.ellipse([hx - hr * 1.3, hy2 - hr * 0.8, hx + hr * 0.9, hy2 + hr * 0.8], fill=gold, outline=gold_d, width=4 * S)
    d.polygon([(hx - hr * 1.3, hy2), (hx - hr * 2.0, hy2 + hr * 0.2), (hx - hr * 1.4, hy2 + hr * 0.6)], fill=gold, outline=gold_d)
    d.ellipse([hx - hr * 0.5, hy2 - hr * 0.45, hx - hr * 0.1, hy2 - hr * 0.1], fill=(20, 18, 30, 255)); d.ellipse([hx - hr * 0.4, hy2 - hr * 0.4, hx - hr * 0.25, hy2 - hr * 0.25], fill=cream)
    for sg in (-1, 1): d.polygon([(hx + hr * 0.1, hy2 - hr * 0.6), (hx + hr * 0.0 + sg * hr * 0.3, hy2 - hr * 1.7), (hx + hr * 0.5, hy2 - hr * 0.7)], fill=teal, outline=gold_d)
    for sg in (-1, 1): d.line([(hx - hr * 1.5, hy2 + sg * hr * 0.15), (hx - hr * 2.6, hy2 + sg * hr * 0.9), (hx - hr * 3.0, hy2 + sg * hr * 0.3)], fill=cream, width=3 * S)
    # five-colour scroll clouds (spirals) filling the field, 2 sizes
    five = [blue, teal, gold, cream, (30, 30, 44, 255)]
    for (cx, cy, rr) in ((0.20, 0.16, 0.09), (0.50, 0.12, 0.08), (0.80, 0.16, 0.09), (0.32, 0.80, 0.09), (0.64, 0.80, 0.10), (0.90, 0.75, 0.07), (0.07, 0.75, 0.07)):
        x, y, R = cx * W2, cy * H2, rr * H2
        for q in range(4): d.arc([x - R * (1 - 0.24 * q), y - R * (1 - 0.24 * q), x + R * (1 - 0.24 * q), y + R * (1 - 0.24 * q)], 20 + 70 * q, 320 + 70 * q, fill=five[q % 5], width=int(3.4 * S))
        d.line([(x - R * 1.7, y + R * 0.9), (x + R * 1.3, y + R * 0.9)], fill=gold, width=3 * S)
    im.resize((w, h), Image.LANCZOS).save(path)

# ----------------------------------------------------------------------------- night sky dome
def sky(path, W=6144, maz=58.0, mel=20.0):
    """Bible 5.4 night: zenith #1e2e7b -> 60 % #1748ae -> horizon #204c8f, a low violet band under the horizon, cool clouds #8fa0d8, blue moon halo."""
    H = int(W * 105 / 360); rs = np.random.RandomState(7)
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0; az = (np.arange(W, dtype='float32') + 0.5) / W * 360.0
    EL = el[:, None] * np.ones((1, W), 'float32'); AZ = np.ones((H, 1), 'float32') * az[None, :]
    def grad(stops):
        e = np.clip(el, -15, 90); out = np.zeros((H, 3), 'float32')
        for c in range(3): out[:, c] = np.interp(e, [s[0] for s in stops], [hexf(s[1])[c] for s in stops])
        return np.repeat(out[:, None, :], W, 1)
    img = grad([(-15, '#3c3a94'), (-4, '#33449a'), (0, '#204c8f'), (12, '#1a4ca0'), (36, '#1748ae'), (62, '#1b3a96'), (90, '#1e2e7b')])
    def ang(a0, e0):
        da = (AZ - a0 + 180) % 360 - 180; return np.hypot(da * np.cos(np.radians(e0)), EL - e0)
    dm = ang(maz, mel)
    lum = (img * np.array([0.2126, 0.7152, 0.0722], 'float32')).sum(-1, keepdims=True); img = lerp(img, lum * np.array([1.0, 1.05, 1.25], 'float32'), 0.30) + np.array([0.075, 0.035, 0.0], 'float32')    # pre-compensate the grade's saturation / black point
    img += (np.exp(-(dm / 26) ** 2) * 0.22)[..., None] * hexf('#3a5ac8') + (np.exp(-(dm / 8) ** 2) * 0.30)[..., None] * hexf('#8ab0ff')      # blue moon halo
    wa = np.exp(-(((AZ - 90 + 180) % 360 - 180) / 60) ** 2) * np.exp(-((EL - 1.0) / 4.0) ** 2)                                          # faint warm city glow at the horizon
    img = lerp(img, hexf('#c8805a') * 0.8, (wa * 0.22)[..., None])
    for k, (e0, e1, thr, seed) in enumerate(((5, 9.5, 0.50, 1), (11.5, 16, 0.54, 2), (20, 25, 0.56, 3), (30, 34, 0.60, 4), (40, 43, 0.62, 5))):
        n = fbm(H, W, (14 + 5 * k, 520), seed * 11, 3); prof = np.exp(-(((EL - (e0 + e1) / 2) / ((e1 - e0) / 2)) ** 4))
        m = np.clip((n - thr + 0.12 * (prof - 0.5)) * 18, 0, 1) * prof
        edge = np.clip(m - np.roll(m, 3, 0), 0, 1)
        col = lerp(np.ones((H, W, 3), 'float32') * hexf('#4a62b8'), hexf('#8fa0d8'), np.clip(0.55 + np.exp(-(dm / 40) ** 2), 0, 1)[..., None])
        img = lerp(img, col, (m * 0.62)[..., None]); img = lerp(img, hexf('#e0a880'), (np.clip(edge * 2.6, 0, 1) * wa)[..., None] * 0.5)
        img = lerp(img, hexf('#b8c8f4'), (np.clip(edge * 2.6, 0, 1) * np.exp(-(dm / 50) ** 2))[..., None] * 0.55)
    N = 3800; ys = rs.rand(N) * H; xs = rs.rand(N) * W; bri = rs.pareto(1.6, N) * 0.22 + 0.2; st = np.zeros((H, W, 3), 'float32')
    tints = [hexf('#ffffff'), hexf('#d6e4ff'), hexf('#fff0d0'), hexf('#ffd6b8')]
    for y_, x_, b_ in zip(ys, xs, bri):
        e_ = 90 - y_ / H * 105
        if e_ < 5: continue
        vis = min(1.0, (e_ - 5) / 14); b_ = min(b_, 3.0) * vis; rad = 0.9 + 0.5 * min(b_, 2.0); t = tints[int(x_) % 4]
        x0, x1 = int(x_ - 3 * rad) - 1, int(x_ + 3 * rad) + 2; y0, y1 = max(0, int(y_ - 3 * rad) - 1), min(H, int(y_ + 3 * rad) + 2)
        if x0 < 0 or x1 > W: continue
        gx = np.arange(x0, x1) + 0.5 - x_; gy = np.arange(y0, y1) + 0.5 - y_
        st[y0:y1, x0:x1] += (np.exp(-(gy[:, None] ** 2 + gx[None, :] ** 2) / (2 * (rad * 0.5) ** 2)) * b_)[..., None] * t
    img += st * np.clip(1 - np.exp(-(dm / 22) ** 2) * 0.95, 0, 1)[..., None]
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
    add('silk', silk, (4.0, 2.0)); add('rain', rain, (2.0, 4.0)); add('sky_WALL', sky, (360.0, 105.0), maz=58.0, mel=20.0); add('sky_CAMP', sky, (360.0, 105.0), maz=74.0, mel=19.0); add('sky_HOLES', sky, (360.0, 105.0), maz=250.0, mel=36.0)
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
