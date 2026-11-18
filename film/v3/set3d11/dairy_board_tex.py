#!/usr/bin/env python3
"""dairy_board_tex.py : painted textures of the film-11 style board (numpy + PIL). Cached in board/tex/ keyed by TEX_V."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); TD = os.path.join(HERE, 'board', 'tex'); TEX_V = 6
os.makedirs(TD, exist_ok=True)

def H(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32) / 255.0
def vn(w, h, gw, gh, seed):
    r = np.random.RandomState(seed); g = r.rand(gh, gw).astype(np.float32)
    return np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0
def fbm(w, h, cells, seed, ax=1.0, ay=1.0):
    o = np.zeros((h, w), np.float32); tot = 0
    for i, (c, a) in enumerate(cells): o += a * vn(w, h, max(2, int(c * ax)), max(2, int(c * ay)), seed + i * 7); tot += a
    return o / tot
def lerp(c0, c1, t): return c0[None, None] * (1 - t[..., None]) + c1[None, None] * t[..., None]
def save(name, a):
    p = os.path.join(TD, '%s_v%d.png' % (name, TEX_V)); Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(p); return p
def lines(im, n, seed, cols, L=(14, 40), wd=(1, 2), ang=None):
    r = np.random.RandomState(seed); d = ImageDraw.Draw(im); W, Hh = im.size
    for i in range(n):
        x, y = r.rand() * W, r.rand() * Hh; a = r.rand() * math.pi if ang is None else ang + (r.rand() - .5) * 0.5; l = L[0] + r.rand() * (L[1] - L[0])
        c = tuple(int(v * 255) for v in H(cols[r.randint(len(cols))])); dx, dy = math.cos(a) * l, math.sin(a) * l
        for ox in (-W, 0, W):
            for oy in (-Hh, 0, Hh): d.line([x + ox, y + oy, x + ox + dx, y + oy + dy], fill=c, width=int(r.randint(wd[0], wd[1] + 1)))

def planks(tone=('#b98a50', '#8f6234'), n=8):
    W = Hh = 512; bw = W // n; out = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(4)
    c0, c1 = H(tone[0]), H(tone[1])
    for i in range(n):
        t = r.rand() * 0.8; base = c0 * (1 - t) + c1 * t
        g = vn(bw, Hh, 10, 2, 10 + i); ring = np.sin(g * 34 + vn(bw, Hh, 4, 6, 50 + i) * 6) * 0.5 + 0.5
        v = 0.82 + 0.22 * g + 0.10 * ring; blk = base[None, None] * v[..., None]
        blk[:, :3] *= 0.45; blk[:, -2:] *= 0.55
        for _ in range(r.randint(0, 3)):
            ky, kx = r.randint(40, Hh - 40), r.randint(10, bw - 10); yy, xx = np.mgrid[0:Hh, 0:bw]; d = ((xx - kx) / 6.0) ** 2 + ((yy - ky) / 11.0) ** 2
            blk *= (1 - 0.55 * np.exp(-d))[..., None]
        out[:, i * bw:(i + 1) * bw] = blk
    return out
def stone(cols=('#dcbb7c', '#cfae78', '#c4a470', '#d8c08c', '#bfa06c'), mortar='#a99468', ch=64, W=512):
    Hh = 512; out = np.zeros((Hh, W, 3), np.float32); r = np.random.RandomState(9); nz = fbm(W, Hh, [(8, 1), (40, .5)], 3)
    for row in range(Hh // ch):
        x = -r.randint(0, 100)
        while x < W:
            bw = r.randint(int(ch * 1.4), int(ch * 3.0)); c = H(cols[r.randint(len(cols))]) * (0.92 + r.rand() * 0.16)
            x0, x1 = max(x, 0), min(x + bw, W); y0, y1 = row * ch, (row + 1) * ch
            out[y0:y1, x0:x1] = c; out[y1 - 5:y1, x0:x1] *= 0.82; out[y0:y0 + 3, x0:x1] *= 1.08
            out[y0:y1, x0:x0 + 3] = H(mortar); out[y0:y0 + 3, x0:x1] = H(mortar); x += bw
    return out * (0.9 + 0.2 * nz[..., None])
def thatch():
    W = Hh = 512; g = vn(W, Hh, 120, 3, 1); g2 = vn(W, Hh, 40, 2, 2); t = np.clip(g * 0.7 + g2 * 0.5, 0, 1)
    o = lerp(H('#85622a'), H('#d4aa56'), t); yy = np.arange(Hh)[:, None]; band = ((yy % 64) < 5).astype(np.float32) * 0.35
    o *= (1 - band[..., None] * np.ones((1, W, 1))); o *= (0.9 + 0.2 * vn(W, Hh, 14, 14, 5))[..., None]; return o
def hay():
    W = Hh = 512; o = lerp(H('#cf9f3f'), H('#e6c066'), fbm(W, Hh, [(6, 1), (30, .5)], 2)); im = Image.fromarray((o * 255).astype(np.uint8))
    lines(im, 3500, 5, ['#efd27c', '#b8842c', '#f3dd8e', '#9a6c24', '#dcae4c'], (18, 56), (1, 2)); return np.asarray(im, np.float32) / 255
def grass(base=('#5d8c34', '#8bb749'), flow=True):
    W = Hh = 512; o = lerp(H(base[0]), H(base[1]), fbm(W, Hh, [(5, 1), (22, .6), (60, .3)], 3)); im = Image.fromarray((o * 255).astype(np.uint8))
    lines(im, 900, 8, ['#9cc653', '#5a8a30', '#7fb040', '#a8cf62'], (5, 11), (1, 1), ang=-math.pi / 2)
    if flow:
        r = np.random.RandomState(11); d = ImageDraw.Draw(im)
        for i in range(70):
            x, y = r.randint(0, W), r.randint(0, Hh); c = [(250, 246, 226), (252, 218, 70), (246, 160, 190)][r.randint(3)]; d.ellipse([x, y, x + 4, y + 3], fill=c)
    return np.asarray(im, np.float32) / 255
def earth(base=('#8d6c45', '#b08a5c'), straw=True, stones=True):
    # straw flecks: few, short and close in colour to the ground so the barn floor reads as packed earth, not scratches
    W = Hh = 512; o = lerp(H(base[0]), H(base[1]), fbm(W, Hh, [(4, 1), (16, .7), (50, .4)], 6)); im = Image.fromarray((o * 255).astype(np.uint8))
    if straw: lines(im, 380, 7, ['#d8b55a', '#c99a3c', '#e6c670'], (14, 36), (2, 3))
    if stones:
        r = np.random.RandomState(12); d = ImageDraw.Draw(im)
        for i in range(120):
            x, y, s = r.randint(0, W), r.randint(0, Hh), r.randint(3, 9); c = [(184, 170, 140), (150, 134, 108), (206, 192, 160)][r.randint(3)]; d.ellipse([x, y, x + s, y + s * 0.7], fill=c)
    return np.asarray(im, np.float32) / 255
def lane():
    o = earth(('#9a7a50', '#c09a68'), straw=False); W = o.shape[1]; xx = np.arange(W)[None, :]
    rut = np.exp(-((xx % 512 - 130) / 22.0) ** 2) + np.exp(-((xx % 512 - 380) / 22.0) ** 2); return o * (1 - 0.22 * rut[..., None])
def cow(a=('#ece1c8', '#6e3f22')):
    W, Hh = 1024, 512; f = fbm(W, Hh, [(6, 1), (14, .6), (36, .2)], 21); m = (f > 0.52).astype(np.float32)
    m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    return lerp(H(a[0]), H(a[1]), m) * (0.95 + 0.1 * vn(W, Hh, 40, 20, 3))[..., None]
def plaster(c='#eadcb2'): W = Hh = 256; return lerp(H(c) * 0.93, H(c), fbm(W, Hh, [(4, 1), (20, .5)], 7))
def slate():
    return stone(('#b6a47a', '#a69470', '#c2ad80', '#9c8c68', '#b09c74'), '#7d6f52', ch=32)
def hills():
    W, Hh = 1024, 512; r = np.random.RandomState(31); n = 110; sx, sy = r.rand(n) * W, r.rand(n) * Hh
    pal = ['#6c9a3c', '#7fae45', '#5e8c38', '#93b54e', '#a9c04f', '#7aa640', '#4f8036', '#8ab04a']; rare = ['#e0c443', '#9c7848', '#c5b24a', '#3f6b32']
    cols = [H(pal[r.randint(len(pal))]) if r.rand() < 0.86 else H(rare[r.randint(len(rare))]) for _ in range(n)]
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32); warp = fbm(W, Hh, [(5, 1), (16, .5)], 4) * 60
    d1 = np.full((Hh, W), 1e9, np.float32); d2 = d1.copy(); id1 = np.zeros((Hh, W), np.int32)
    for i in range(n):
        d = np.hypot(xx + warp - sx[i], (yy + warp * .6 - sy[i]) * 1.6)
        m = d < d1; d2 = np.where(m, d1, np.minimum(d2, d)); id1 = np.where(m, i, id1); d1 = np.minimum(d, d1)
    o = np.array(cols, np.float32)[id1] * (0.88 + 0.24 * fbm(W, Hh, [(10, 1), (40, .5)], 5))[..., None]
    hedge = np.clip(1 - (d2 - d1) / 3.5, 0, 1); o = o * (1 - hedge[..., None] * 0.7) + hedge[..., None] * 0.7 * H('#35582a')
    return np.asarray(Image.fromarray((np.clip(o, 0, 1) * 255).astype(np.uint8)).resize((2048, 1024), Image.BICUBIC), np.float32) / 255
def sky(top, mid, hor, cloud_lit, cloud_sh, az0=0.75, seed=3, n=9):
    """4096 x 1024 dome texture: u = azimuth / 2pi (+.5), v = elevation / 90. Crisp cartoon cumulus (cel shaded undersides)."""
    W, Hh = 4096, 1024; v = np.linspace(0, 1, Hh)[:, None] * np.ones((1, W)); v = v[::-1]            # row 0 = zenith
    t = np.clip(v, 0, 1); o = np.where(t[..., None] < 0.5, lerp(H(hor), H(mid), np.clip(t * 2, 0, 1)), lerp(H(mid), H(top), np.clip(t * 2 - 1, 0, 1)))
    M = Image.new('L', (W * 2, Hh * 2), 0); r = np.random.RandomState(seed)
    for k in range(n):
        C = Image.new('L', (W * 2, Hh * 2), 0); d = ImageDraw.Draw(C)
        cx = (az0 + (r.rand() - .5) * 0.40) * W * 2; el = 0.08 + r.rand() * 0.55; cy = (1 - el) * Hh * 2; sc = 0.45 + r.rand() * 0.6
        for j in range(int(22 * sc) + 10):
            ex = r.randn() * 150 * sc; ey = -abs(r.randn()) * 95 * sc; rad = (55 + r.rand() * 85) * sc
            hh = rad * 0.85; d.ellipse([cx + ex - rad, cy + ey - hh, cx + ex + rad, cy + ey + hh], fill=255)
        d.rectangle([cx - 900 * sc, cy + 30 * sc, cx + 900 * sc, cy + 400 * sc], fill=0); M = Image.fromarray(np.maximum(np.asarray(M), np.asarray(C)))
    m = np.asarray(M.resize((W, Hh), Image.LANCZOS), np.float32) / 255; ms = np.roll(np.roll(m, -30, 1), -34, 0); sh = np.clip(m - (ms > .5) * 1.0, 0, 1) * (m > .5)
    sh = np.asarray(Image.fromarray((sh * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)), np.float32) / 255 * (m > .5)
    c = lerp(H(cloud_lit), H(cloud_sh), sh); return o * (1 - m[..., None]) + c * m[..., None]

ALL = dict(planks=lambda: planks(), planks_dark=lambda: planks(('#8a5f33', '#5f3f22')), planks_silver=lambda: planks(('#b9a98a', '#8c7d62')), stone=stone, stone_grey=lambda: stone(('#c9b58c', '#bba67e', '#b09b76', '#c6b289'), '#9c8a66'),
           thatch=thatch, hay=hay, grass=grass, grass_d=lambda: grass(('#4f7c2e', '#78a63f'), False), earth=earth, lane=lane, cow=cow, plaster=plaster, slate=slate, hills=hills)
def get(name):
    p = os.path.join(TD, '%s_v%d.png' % (name, TEX_V))
    return p if os.path.exists(p) else save(name, ALL[name]())
def get_sky(name, az0=0.75, **kw):
    p = os.path.join(TD, 'sky_%s_%d_v%d.png' % (name, int(az0 * 100), TEX_V))
    if os.path.exists(p): return p
    a = sky(az0=az0, **kw); Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(p); return p
if __name__ == '__main__':
    import time
    for k in ALL: t = time.time(); get(k); print(k, round(time.time() - t, 1))
