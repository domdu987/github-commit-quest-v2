#!/usr/bin/env python3
"""dairy_tex.py : painted textures of the film-11 FULL set (numpy + PIL, deterministic). Builds on the style-board painters
(dairy_board_tex: planks, stone, earth, grass, hills, sky ...) and adds the richer ones: strand thatch, strand hay, brown-and-white cow
hides (two coats), flagstones, rag rug, patchwork quilt, cobbles, plaster. Cached in tex_dairy/ keyed by TEX_V (bump after editing a painter).
No text anywhere. usage: import dairy_tex as X; path = X.get('thatch2'); sky = X.get_sky('day', az0=.5, **SKY['day'])"""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import dairy_board_tex as BX
from dairy_board_tex import H, vn, fbm, lerp, lines

HERE = os.path.dirname(os.path.abspath(__file__)); TD = os.path.join(HERE, 'tex_dairy'); TEX_V = 3
os.makedirs(TD, exist_ok=True)
BX.TD = TD; BX.TEX_V = TEX_V                                  # the board painters now cache here too
save = BX.save

def _im(a): return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
def _ar(im): return np.asarray(im, np.float32) / 255.0

def thatch2():
    """Straw thatch: dense long vertical strands (golden / brown / pale), darker horizontal course lines, sharp."""
    W = Hh = 512; base = lerp(H('#8f6a2c'), H('#d9b25c'), fbm(W, Hh, [(6, 1), (30, .5)], 2)); im = _im(base)
    r = np.random.RandomState(4); d = ImageDraw.Draw(im)
    cols = ['#f0d47c', '#c99a3c', '#a47a2e', '#e2bd62', '#7f5a24', '#d8ae52', '#f6e09a']
    for i in range(5200):
        x, y = r.rand() * W, r.rand() * Hh; l = 20 + r.rand() * 46; a = math.pi / 2 + (r.rand() - .5) * 0.22; c = tuple(int(v * 255) for v in H(cols[r.randint(len(cols))]))
        for oy in (-Hh, 0, Hh):
            for ox in (-W, 0, W): d.line([x + ox, y + oy, x + ox + math.cos(a) * l, y + oy + math.sin(a) * l], fill=c, width=int(r.randint(1, 3)))
    a = _ar(im); yy = np.arange(Hh)[:, None]; band = np.exp(-(((yy % 128) - 6) / 4.5) ** 2)[..., None] * np.ones((1, W, 1)); a = a * (1 - 0.38 * band)
    return a * (0.92 + 0.16 * vn(W, Hh, 12, 12, 8))[..., None]

def hay2():
    W = Hh = 512; im = _im(lerp(H('#c9993a'), H('#e8c46a'), fbm(W, Hh, [(5, 1), (26, .5)], 2))); r = np.random.RandomState(6); d = ImageDraw.Draw(im)
    cols = ['#f4dc8c', '#b8842c', '#f8e8a4', '#9a6c24', '#dcae4c', '#e9c25e', '#c28e30']
    for i in range(6500):
        x, y = r.rand() * W, r.rand() * Hh; l = 22 + r.rand() * 60; a = r.rand() * math.pi; c = tuple(int(v * 255) for v in H(cols[r.randint(len(cols))]))
        for oy in (-Hh, 0, Hh):
            for ox in (-W, 0, W): d.line([x + ox, y + oy, x + ox + math.cos(a) * l, y + oy + math.sin(a) * l], fill=c, width=int(r.randint(1, 3)))
    return _ar(im)

def _blobs(W, Hh, seed, n, rmin, rmax, wrap=True):
    """Organic filled blobs (union of jittered ellipses) as a 0..1 mask; wraps in v (rows) so the hide tiles around the body."""
    r = np.random.RandomState(seed); M = Image.new('L', (W, Hh), 0); d = ImageDraw.Draw(M)
    for i in range(n):
        cx, cy = r.rand() * W, r.rand() * Hh; R = rmin + r.rand() * (rmax - rmin); ang = r.rand() * 6.28
        for j in range(r.randint(4, 8)):
            ex, ey = cx + r.randn() * R * 0.45, cy + r.randn() * R * 0.45; rx, ry = R * (0.45 + r.rand() * 0.6), R * (0.4 + r.rand() * 0.55)
            for oy in ((-Hh, 0, Hh) if wrap else (0,)):
                d.ellipse([ex - rx, ey + oy - ry, ex + rx, ey + oy + ry], fill=255)
    m = _ar(M.filter(ImageFilter.GaussianBlur(5))); w = fbm(W, Hh, [(9, 1), (28, .5)], seed + 3)
    return (m + (w - 0.5) * 0.35 > 0.5).astype(np.float32)

def cow_hide(coat='a'):
    """Hide, 1024 x 1024: u = along the body (0 rump .. 0.63 shoulders, neck beyond), v = around (wraps). a: cream with brown patches,
    b: chestnut with cream patches + blaze. Sharp edges, small speckles, a darker tone inside the patches."""
    W = Hh = 1024
    if coat == 'a': ground, patch, patch2 = H('#f1e6cc'), H('#7a4426'), H('#5c3018'); m = _blobs(W, Hh, 11, 9, 90, 170)
    else: ground, patch, patch2 = H('#8c4e2a'), H('#f1e6cc'), H('#f6ecd6'); m = _blobs(W, Hh, 23, 7, 70, 130)
    m = np.asarray(_im(m).filter(ImageFilter.GaussianBlur(1.4)), np.float32) / 255
    dark = (fbm(W, Hh, [(14, 1), (40, .5)], 31) > 0.62).astype(np.float32) * m
    o = lerp(ground, patch, m); o = o * (1 - 0.0) + (patch2 - patch)[None, None] * (dark[..., None] * 0.55) * (1 if coat == 'a' else 0)
    o *= (0.94 + 0.1 * vn(W, Hh, 80, 80, 5))[..., None]
    return np.clip(o, 0, 1)

def flag():
    """Irregular flagstones (warm grey-brown / buff), dark joints."""
    W = Hh = 512; out = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(17); pal = ['#b6a98c', '#a59a80', '#bfb094', '#98886c', '#aa9a7a', '#b8a280']
    y = 0; nz = fbm(W, Hh, [(8, 1), (40, .5)], 3)
    while y < Hh:
        h = r.randint(70, 130); x = -r.randint(0, 90)
        while x < W:
            w = r.randint(80, 170); c = H(pal[r.randint(len(pal))]) * (0.92 + r.rand() * 0.16)
            x0, x1, y0, y1 = max(x, 0), min(x + w, W), y, min(y + h, Hh); out[y0:y1, x0:x1] = c; out[y0:y1, x0:x0 + 5] *= 0.55; out[y0:y0 + 5, x0:x1] *= 0.55; x += w
        y += h
    return out * (0.88 + 0.22 * nz[..., None])

def cobble():
    W = Hh = 512; out = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(19); pal = ['#a39478', '#b3a386', '#8f8068', '#bba88a', '#9d8e72']
    out[:] = H('#6b5d48'); yy, xx = np.mgrid[0:Hh, 0:W]
    for gy in range(14):
        for gx in range(14):
            cx = (gx + 0.5 + 0.5 * (gy % 2)) * (W / 14) + r.randn() * 2; cy = (gy + 0.5) * (Hh / 14) + r.randn() * 2; rx, ry = W / 14 * 0.46, Hh / 14 * 0.42
            for ox in (-W, 0, W):
                d = ((xx - cx - ox) / rx) ** 2 + ((yy - cy) / ry) ** 2; m = d < 1; c = H(pal[r.randint(len(pal))]) * (0.9 + 0.2 * r.rand())
                shade = 1.1 - 0.35 * np.clip(d, 0, 1)
                out[m] = (c[None] * shade[m][:, None])
    return out * (0.9 + 0.2 * fbm(W, Hh, [(10, 1), (40, .5)], 4)[..., None])

def rug():
    """Rag rug: concentric rows of faded blues, reds, creams, ochres (no pattern that reads as text)."""
    W = Hh = 256; cols = ['#a8503a', '#e0cfa0', '#4f6aa0', '#d8a04a', '#7a9a64', '#c88a7a', '#6a5a90']; o = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(5)
    yy, xx = np.mgrid[0:Hh, 0:W]; d = np.maximum(abs(xx - W / 2) / (W / 2) * 1.0, abs(yy - Hh / 2) / (Hh / 2))
    k = (d * 11).astype(int)
    for i in range(12): o[k == i] = H(cols[(i * 3 + r.randint(2)) % len(cols)])
    o[d >= 1.0] = H(cols[0]); o *= (0.9 + 0.2 * vn(W, Hh, 100, 4, 3))[..., None]; return o

def quilt():
    """Patchwork quilt: 6 x 6 squares of cream / rose / blue-grey / ochre / sage with stitched cross lines."""
    W = Hh = 384; cols = ['#efe2c0', '#d98a86', '#8aa4c4', '#e0b458', '#9ab48a', '#c9786c', '#f4ead0']; o = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(8); n = 6; s = W // n
    for gy in range(n):
        for gx in range(n):
            c = H(cols[(gx + gy * 2 + r.randint(3)) % len(cols)]); o[gy * s:(gy + 1) * s, gx * s:(gx + 1) * s] = c * (0.94 + 0.1 * r.rand())
            o[gy * s:(gy + 1) * s, gx * s:gx * s + 3] *= 0.7; o[gy * s:gy * s + 3, gx * s:(gx + 1) * s] *= 0.7
            cx, cy = gx * s + s // 2, gy * s + s // 2; o[cy - 1:cy + 2, cx - 14:cx + 14] *= 0.82; o[cy - 14:cy + 14, cx - 1:cx + 2] *= 0.82
    return o

def plaster2(): return lerp(H('#eadcb4') * 0.95, H('#f0e4c0'), fbm(256, 256, [(4, 1), (22, .5), (70, .3)], 7))
def wood_floor(): return BX.planks(('#a87c48', '#7e5630'), 6)
def stone_wall(): return BX.stone(('#d4b078', '#c9a56e', '#bd9a66', '#d9bb86', '#b79660', '#cfae7a'), '#9c8660', ch=48)
def moss_stone(): return BX.stone(('#bba57a', '#a8946c', '#b6a276', '#9d8d62'), '#7e7052', ch=40)
def thatch_dark(): return thatch2() * np.array([0.82, 0.78, 0.74], np.float32)
def brick():
    W = Hh = 512; out = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(14); pal = ['#b85a3c', '#a84c32', '#c46a46', '#9c4430', '#bc6240']
    for row in range(Hh // 32):
        x = -r.randint(0, 64) if row % 2 else 0
        while x < W:
            c = H(pal[r.randint(len(pal))]) * (0.9 + 0.2 * r.rand()); x0, x1 = max(x, 0), min(x + 64, W); out[row * 32:(row + 1) * 32, x0:x1] = c; out[row * 32:(row + 1) * 32, x0:x0 + 3] = H('#d8c8a0'); out[row * 32:row * 32 + 3, x0:x1] = H('#d8c8a0'); x += 64
    return out

ALL = dict(thatch2=thatch2, thatch_dark=thatch_dark, hay2=hay2, cow_a=lambda: cow_hide('a'), cow_b=lambda: cow_hide('b'), flag=flag, cobble=cobble, rug=rug, quilt=quilt,
           plaster2=plaster2, wood_floor=wood_floor, stone_wall=stone_wall, moss_stone=moss_stone, brick=brick)
def get(name):
    p = os.path.join(TD, '%s_v%d.png' % (name, TEX_V))
    if os.path.exists(p): return p
    if name in ALL: return save(name, ALL[name]())
    return BX.get(name)
def get_sky(name, az0=0.75, **kw): return BX.get_sky(name, az0=az0, **kw)

if __name__ == '__main__':
    import time
    for k in list(ALL) + list(BX.ALL): t = time.time(); get(k); print(k, round(time.time() - t, 1), flush=True)
