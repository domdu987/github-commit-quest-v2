"""film 21 textures (numpy + PIL, no bpy): the painted morning sky with flat drawn clouds, weathered timber grain, a brush-stroke meadow tile.
Cached in tex/<name>_v<TEX_V>.png (git-ignored, rebuilt on demand). Every feature is >= 3 texels wide (Cycles has no mip-mapping)."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'tex'); os.makedirs(TEX, exist_ok=True)
TEX_V = 8
def _p(name): return os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
def _rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _lerp(a, b, t): return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))

def sky(name='sky', W=2048, H=1024, sun_az=-45.0):
    """equirect sky: u = azimuth / 360 from +x CCW, v = (elevation + 15) / 105 (image y = (1 - v) * H). Painted gradient, a warm glow toward the sun
    azimuth (south-east = -45 deg), flat drawn cumulus (cream-peach tops, blue-violet undersides), a pale haze band at the horizon."""
    p = _p(name)
    if os.path.exists(p): return p
    top, mid, hor, below = _rgb('#6f9fdc'), _rgb('#a9cbec'), _rgb('#efe2de'), _rgb('#dcd2d2')
    y = np.arange(H)[:, None] * np.ones((1, W)); v = 1 - y / (H - 1); el = v * 105 - 15
    a = np.zeros((H, W, 3))
    for c in range(3):
        t_hi = np.clip((el - 25) / 65.0, 0, 1) ** 0.8; t_lo = np.clip(el / 25.0, 0, 1)
        col = hor[c] * (1 - t_lo) + mid[c] * t_lo; col = col * (1 - t_hi) + top[c] * t_hi
        a[..., c] = np.where(el < 0, below[c], col)
    x = np.arange(W)[None, :] * np.ones((H, 1)); az = x / W * 360.0
    daz = np.abs(((az - (sun_az % 360)) + 180) % 360 - 180)
    glow = np.exp(-(daz / 38.0) ** 2) * np.exp(-(np.clip(el, 0, 90) / 18.0) ** 2) * 0.55
    warm = np.array(_rgb('#ffd7a8')); a = a * (1 - glow[..., None]) + warm * glow[..., None]
    im = Image.fromarray(a.astype(np.uint8)); S = 2
    big = im.resize((W * S, H * S), Image.BILINEAR); d = ImageDraw.Draw(big); r = random.Random(4)
    def y_of(elev): return (1 - (elev + 15) / 105.0) * H * S
    def blob(cx_deg, el0, wdeg, hdeg, seed):
        rr = random.Random(seed); cx = cx_deg / 360.0 * W * S; cy = y_of(el0); ww = wdeg / 360.0 * W * S; hh = hdeg / 105.0 * H * S
        n = rr.randint(7, 10); items = []
        for i in range(n):
            t = (i + 0.5) / n; px = cx + (t - 0.5) * ww; ph = hh * (0.55 + 0.45 * math.sin(math.pi * t)) * rr.uniform(0.7, 1.0)
            items.append((px, cy - ph * 0.25, ph * 0.62))
        for px, py, rad in items:                    # shadow side first (blue-violet), then the sunlit cream tops offset up-left
            d.ellipse([px - rad, py - rad * 0.8 + rad * 0.14, px + rad, py + rad * 0.8 + rad * 0.14], fill=_rgb('#aab4de'))
        for px, py, rad in items:
            d.ellipse([px - rad * 0.96, py - rad * 0.8 - rad * 0.06, px + rad * 0.96, py + rad * 0.74], fill=_rgb('#f6efec'))
        for px, py, rad in items:
            d.ellipse([px - rad * 0.55 - rad * 0.12, py - rad * 0.7 - rad * 0.1, px + rad * 0.55 - rad * 0.12, py + rad * 0.1], fill=_rgb('#fff4e6'))
    for k, (az0, e0, w, h) in enumerate([(-100, 16, 40, 8), (-40, 32, 46, 9), (20, 22, 52, 10), (80, 40, 40, 8), (140, 20, 50, 9), (200, 34, 44, 8), (250, 14, 46, 8), (-150, 44, 36, 7),
                                           (330, 52, 40, 7), (110, 58, 34, 6), (10, 60, 30, 6), (205, 26, 38, 7), (232, 18, 30, 6), (176, 30, 34, 6), (222, 42, 28, 5), (-30, 20, 30, 6), (60, 28, 34, 6), (35, 33, 40, 8), (47, 19, 36, 7), (24, 41, 30, 6), (56, 45, 28, 5), (39, 54, 28, 5), (14, 30, 30, 6)]):
        blob(az0 % 360, e0, w, h, 100 + k)
        if az0 % 360 > 300 or az0 % 360 < 60: blob((az0 % 360) + 360, e0, w, h, 100 + k)
    big = big.resize((W, H), Image.LANCZOS); big.save(p); return p

def wood(name='wood', S=512, seed=3, base='#8a6a45'):
    """weathered timber, grain strokes along v (image y): dark wobbly grain lines, a few cracks, per-tile tone. Seams are the object's own geometry."""
    p = _p(name)
    if os.path.exists(p): return p
    r = random.Random(seed); b = _rgb(base); im = Image.new('RGB', (S, S), b); d = ImageDraw.Draw(im)
    for i in range(14):
        x0 = r.uniform(0, S); w = r.uniform(S * 0.04, S * 0.12); t = r.uniform(0.88, 1.10); d.rectangle([x0, 0, x0 + w, S], fill=tuple(min(255, int(c * t)) for c in b))
    dark = tuple(int(c * 0.72) for c in b); light = tuple(min(255, int(c * 1.18)) for c in b)
    for i in range(34):
        x = r.uniform(0, S); y0 = r.uniform(-S * 0.1, S * 0.8); L = r.uniform(S * 0.2, S * 0.7); ph = r.random() * 6; pts = []
        for k in range(10): pts.append((x + math.sin(k * 0.8 + ph) * 3.5, y0 + L * k / 9))
        d.line(pts, fill=dark if i % 3 else light, width=3)
    for i in range(5):
        x = r.uniform(20, S - 20); y = r.uniform(20, S - 20); d.ellipse([x - 8, y - 13, x + 8, y + 13], outline=dark, width=3)
    im = im.filter(ImageFilter.GaussianBlur(0.6)); im.save(p); return p

def meadow(name='meadow', S=512, seed=5):
    """grayscale (Non-Color) brush-stroke tile, mean 0.5: curved blade strokes in light and dark of several lengths and a few round tussock dabs; used as a luminance
    multiplier on the painted terrain colour (the grass is painted on the ground, not modelled)."""
    p = _p(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('L', (S, S), 128); d = ImageDraw.Draw(im)
    def stroke(x, y, L, a, c, w):
        pts = [(x + math.cos(a) * L * t / 5 + math.sin(t * 1.1 + x) * 2.0, y - math.sin(a) * L * t / 5) for t in range(6)]; d.line(pts, fill=int(c), width=w)
    for i in range(520):                                        # big soft dabs first (tussocks / bare patches)
        x = r.uniform(0, S); y = r.uniform(0, S); rad = r.uniform(10, 26); c = 128 + r.choice((-1, 1)) * r.uniform(10, 24)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S): d.ellipse([x + ox - rad, y + oy - rad * 0.6, x + ox + rad, y + oy + rad * 0.6], fill=int(c))
    for i in range(2600):
        x = r.uniform(0, S); y = r.uniform(0, S); L = r.uniform(16, 46); a = math.radians(r.uniform(-30, 30) + 90); c = 128 + r.choice((-1, 1, 1)) * r.uniform(28, 70)
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                if abs(x + ox - S / 2) < S * 0.8 and abs(y + oy - S / 2) < S * 0.8: stroke(x + ox, y + oy, L, a, c, r.choice((3, 3, 4, 5)))
    im = im.filter(ImageFilter.GaussianBlur(0.7)); im.save(p); return p
