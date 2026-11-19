"""h19_tex.py : painted textures of set3d19 (PIL only, cached in tex_h19/, small PNGs, NO text anywhere):
carpet (greyer navy #2c3558 field, crimson + gold border, medallion, corner motifs, fine field ornament), moon (soft grey painted Moon on a dark ground),
worldmap (parchment, soft landmasses, graticule lines, dots), starchart (dark navy with dots + constellation lines), seascape (a painted ship on a swell)."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'tex_h19'); os.makedirs(OUT, exist_ok=True)
def _h(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _paint(im, amt=10, seed=1, scale=6):
    """painterly mottling: add low-frequency noise to the image"""
    a = np.asarray(im.convert('RGB'), dtype=np.float32); rs = np.random.RandomState(seed); h, w = a.shape[:2]
    n = rs.rand(h // scale + 2, w // scale + 2).astype(np.float32); n = np.asarray(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0 - 0.5
    n2 = rs.rand(h // 2 + 2, w // 2 + 2).astype(np.float32); n2 = np.asarray(Image.fromarray((n2 * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0 - 0.5
    a = a + (n[..., None] * amt + n2[..., None] * amt * 0.4); return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def carpet(path, w=640, h=1000):
    p = path
    if os.path.exists(p): return p
    S = 2; W_, H_ = w * S, h * S; im = Image.new('RGB', (W_, H_), _h('#2c3558')); d = ImageDraw.Draw(im)
    navy, navy2, crim, crim2, gold, cream = _h('#2c3558'), _h('#38446e'), _h('#7a2a34'), _h('#923640'), _h('#c9a24a'), _h('#d8c89c')
    def rect(i0, col):                            # inset rectangle band
        d.rectangle([i0 * S, i0 * S, W_ - 1 - i0 * S, H_ - 1 - i0 * S], fill=col)
    rect(0, gold); rect(5, crim); rect(11, cream); rect(14, crim2); rect(58, cream); rect(61, gold); rect(65, navy)
    # border pattern between inset 14 and 58: gold scroll chain of ellipses + diamonds
    def band(): return range(18 * S, 54 * S)
    step = 46 * S
    for edge in range(4):
        L = (H_ if edge in (0, 2) else W_) - 2 * 20 * S; n = int(L / step)
        for i in range(n):
            t = 20 * S + (i + 0.5) * L / n
            if edge == 0: cx, cy = 36 * S, t
            elif edge == 2: cx, cy = W_ - 36 * S, t
            elif edge == 1: cx, cy = t, 36 * S
            else: cx, cy = t, H_ - 36 * S
            r = 15 * S
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=gold, width=3 * S)
            d.polygon([(cx, cy - 9 * S), (cx + 9 * S, cy), (cx, cy + 9 * S), (cx - 9 * S, cy)], fill=cream)
            d.ellipse([cx - 3 * S, cy - 3 * S, cx + 3 * S, cy + 3 * S], fill=crim)
            for q in (-1, 1):
                if edge in (0, 2): d.ellipse([cx - 4 * S, cy + q * 24 * S - 4 * S, cx + 4 * S, cy + q * 24 * S + 4 * S], fill=gold)
                else: d.ellipse([cx + q * 24 * S - 4 * S, cy - 4 * S, cx + q * 24 * S + 4 * S, cy + 4 * S], fill=gold)
    # corner motifs of the border
    for cx, cy in ((36 * S, 36 * S), (W_ - 36 * S, 36 * S), (36 * S, H_ - 36 * S), (W_ - 36 * S, H_ - 36 * S)):
        d.rectangle([cx - 22 * S, cy - 22 * S, cx + 22 * S, cy + 22 * S], fill=crim2, outline=gold, width=3 * S); d.ellipse([cx - 13 * S, cy - 13 * S, cx + 13 * S, cy + 13 * S], fill=cream); d.ellipse([cx - 7 * S, cy - 7 * S, cx + 7 * S, cy + 7 * S], fill=crim)
    # field: fine diamond lattice + small rosettes
    x0, y0, x1, y1 = 70 * S, 70 * S, W_ - 70 * S, H_ - 70 * S; sp = 38 * S
    for yy in range(y0, y1, sp):
        d.line([(x0, yy), (x1, yy)], fill=navy2, width=S)
    for k in range(-int(H_ / sp), int(W_ / sp) + int(H_ / sp)):
        pass
    ys = list(range(y0 + sp // 2, y1, sp)); xs = list(range(x0 + sp // 2, x1, sp))
    for iy, yy in enumerate(ys):
        for ix, xx in enumerate(xs):
            ox = (sp // 2) if iy % 2 else 0; cx = xx + ox
            if cx > x1 - 8 * S: continue
            d.polygon([(cx, yy - 7 * S), (cx + 7 * S, yy), (cx, yy + 7 * S), (cx - 7 * S, yy)], fill=navy2)
            if (ix + iy) % 3 == 0: d.ellipse([cx - 2.5 * S, yy - 2.5 * S, cx + 2.5 * S, yy + 2.5 * S], fill=crim2)
    # central medallion + two end medallions + spandrels
    def medallion(cx, cy, rx, ry):
        for k, col in enumerate((gold, crim, cream, navy, crim2, gold, navy)):
            f = 1 - k * 0.13; d.ellipse([cx - rx * f, cy - ry * f, cx + rx * f, cy + ry * f], fill=col)
        for a in range(16):
            ang = a * math.pi / 8; px, py = cx + rx * 0.5 * math.cos(ang), cy + ry * 0.5 * math.sin(ang)
            d.ellipse([px - 6 * S, py - 9 * S, px + 6 * S, py + 9 * S], fill=gold if a % 2 else cream)
        d.ellipse([cx - rx * 0.2, cy - ry * 0.2, cx + rx * 0.2, cy + ry * 0.2], fill=crim)
    medallion(W_ / 2, H_ / 2, 190 * S, 250 * S); medallion(W_ / 2, 230 * S, 90 * S, 90 * S); medallion(W_ / 2, H_ - 230 * S, 90 * S, 90 * S)
    for (cx, cy, a0) in ((70 * S, 70 * S, 0), (W_ - 70 * S, 70 * S, 90), (W_ - 70 * S, H_ - 70 * S, 180), (70 * S, H_ - 70 * S, 270)):
        d.pieslice([cx - 150 * S, cy - 150 * S, cx + 150 * S, cy + 150 * S], a0, a0 + 90, fill=crim2, outline=gold, width=3 * S)
        d.pieslice([cx - 105 * S, cy - 105 * S, cx + 105 * S, cy + 105 * S], a0, a0 + 90, fill=navy, outline=cream, width=2 * S)
    im = im.resize((w, h), Image.LANCZOS); im = _paint(im, 9, 3, 5); im.save(p, optimize=True); return p

def moon(path, w=512, h=768):
    if os.path.exists(path): return path
    S = 1; im = Image.new('RGB', (w, h), _h('#1a2034')); a = np.asarray(im, dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); r = np.hypot((xx - w / 2) / (w / 2), (yy - h * 0.46) / (w / 2))
    sky = np.clip(1 - np.hypot((xx - w / 2) / w, (yy - h / 2) / h) * 1.2, 0, 1)[..., None]; a = a * (0.7 + 0.5 * sky)
    glow = np.clip(1.35 - r, 0, 1)[..., None] ** 2.2 * np.array([60, 66, 80], dtype=np.float32); a = a + glow
    disc = np.clip((0.66 - r) / 0.03, 0, 1)[..., None]; shade = np.clip(0.55 + 0.55 * ((xx - w * 0.38) / (w * 0.6)) * -1 + 0.25, 0.55, 1.0)[..., None]
    moonc = np.array([196, 192, 184], dtype=np.float32) * (0.78 + 0.28 * np.clip(1 - r / 0.66, 0, 1)[..., None]) * (0.85 + 0.15 * shade)
    a = a * (1 - disc) + moonc * disc; rs = random.Random(7); im2 = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); dd = ImageDraw.Draw(im2, 'RGBA')
    for k in range(15):                                    # soft craters
        ang = rs.uniform(0, 6.28); rad = rs.uniform(0.0, 0.5) * w * 0.66 * 0.8; cx = w / 2 + rad * math.cos(ang); cy = h * 0.46 + rad * math.sin(ang); cr = rs.uniform(10, 34)
        dd.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(120, 116, 112, 70)); dd.ellipse([cx - cr * 0.8, cy - cr * 0.7, cx + cr * 0.7, cy + cr * 0.8], fill=(168, 164, 158, 60))
    for k in range(4): dd.ellipse([w / 2 - 140 + k * 60, h * 0.46 - 70 + (k % 2) * 90, w / 2 - 60 + k * 60, h * 0.46 + 10 + (k % 2) * 90], fill=(130, 126, 122, 45))
    for k in range(40):
        sx, sy = rs.randint(0, w), rs.randint(0, h)
        if math.hypot((sx - w / 2) / (w / 2), (sy - h * 0.46) / (w / 2)) > 0.8: dd.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(220, 220, 235, 200))
    im2 = im2.filter(ImageFilter.GaussianBlur(1.6)); im2 = _paint(im2, 7, 5, 8); im2.save(path, optimize=True); return path

def worldmap(path, w=512, h=640):
    if os.path.exists(path): return path
    im = Image.new('RGB', (w, h), _h('#d8c490')); d = ImageDraw.Draw(im, 'RGBA'); rs = random.Random(11)
    d.rectangle([0, 0, w, h], fill=_h('#d4be86'))
    for (cx, cy, rx, ry) in ((140, 190, 90, 150), (360, 150, 110, 80), (330, 330, 80, 140), (200, 440, 70, 90), (420, 480, 50, 70), (90, 400, 40, 60)):       # soft landmasses
        for k in range(14):
            ox, oy = rs.uniform(-0.5, 0.5) * rx, rs.uniform(-0.5, 0.5) * ry; r1, r2 = rx * rs.uniform(0.4, 0.8), ry * rs.uniform(0.4, 0.8)
            d.ellipse([cx + ox - r1, cy + oy - r2, cx + ox + r1, cy + oy + r2], fill=(150, 128, 78, 255) if k % 3 else (170, 146, 90, 255))
    sea = Image.new('RGBA', (w, h), (70, 110, 120, 60)); im = Image.alpha_composite(im.convert('RGBA'), sea).convert('RGB'); d = ImageDraw.Draw(im, 'RGBA')
    for gx in range(0, w, 64): d.line([(gx, 0), (gx, h)], fill=(70, 50, 40, 120), width=1)
    for gy in range(0, h, 64): d.line([(0, gy), (w, gy)], fill=(70, 50, 40, 120), width=1)
    cx, cy = w / 2, h / 2
    for k in range(16):                                                      # rhumb lines
        a = k * math.pi / 8; d.line([(cx, cy), (cx + 700 * math.cos(a), cy + 700 * math.sin(a))], fill=(120, 40, 36, 90), width=1)
    d.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], outline=(120, 40, 36, 200), width=2)
    for k in range(40): x, y = rs.randint(10, w - 10), rs.randint(10, h - 10); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(40, 30, 30, 220))
    for k in range(3): d.line([(rs.randint(20, w), rs.randint(20, h)), (rs.randint(20, w), rs.randint(20, h))], fill=(40, 30, 30, 160), width=2)
    im = _paint(im, 14, 9, 7).filter(ImageFilter.GaussianBlur(0.6)); im.save(path, optimize=True); return path

def starchart(path, w=512, h=640):
    if os.path.exists(path): return path
    im = Image.new('RGB', (w, h), _h('#1a2448')); d = ImageDraw.Draw(im, 'RGBA'); rs = random.Random(13)
    for k in range(5):
        cx, cy = rs.randint(60, w - 60), rs.randint(60, h - 60); pts = [(cx + rs.randint(-70, 70), cy + rs.randint(-70, 70)) for _ in range(rs.randint(4, 7))]
        d.line(pts, fill=(200, 210, 240, 150), width=1)
        for p in pts: d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(250, 240, 200, 255))
    for k in range(120): x, y = rs.randint(0, w), rs.randint(0, h); d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(230, 230, 250, 200))
    d.ellipse([w / 2 - 220, h / 2 - 220, w / 2 + 220, h / 2 + 220], outline=(210, 180, 100, 160), width=2); d.ellipse([w / 2 - 150, h / 2 - 150, w / 2 + 150, h / 2 + 150], outline=(210, 180, 100, 110), width=1)
    im = _paint(im, 8, 15, 8); im.save(path, optimize=True); return path

def seascape(path, w=640, h=480):
    if os.path.exists(path): return path
    im = Image.new('RGB', (w, h)); d = ImageDraw.Draw(im, 'RGBA')
    for y in range(h):
        t = y / h
        c = (int(150 + 60 * (1 - t)), int(170 + 40 * (1 - t)), int(200 + 20 * (1 - t))) if y < h * 0.55 else (int(24 + 40 * (t - 0.55)), int(80 + 50 * (t - 0.55)), int(96 + 40 * (t - 0.55)))
        d.line([(0, y), (w, y)], fill=c)
    rs = random.Random(5)
    for k in range(6): x, y = rs.randint(0, w), rs.randint(40, 200); d.ellipse([x - 90, y - 24, x + 90, y + 24], fill=(250, 244, 232, 150))
    d.rectangle([0, 260, w, 266], fill=(120, 150, 170, 255))
    for k in range(40): x, y = rs.randint(0, w), rs.randint(280, h); d.line([(x, y), (x + rs.randint(30, 90), y)], fill=(210, 230, 235, 130), width=2)
    d.polygon([(250, 360), (420, 360), (440, 340), (230, 340)], fill=(40, 34, 30, 255)); d.rectangle([236, 346, 430, 350], fill=(200, 160, 70, 255))
    for mx, ht in ((290, 220), (335, 190), (385, 230)):
        d.line([(mx, 340), (mx, 340 - ht * 0.8)], fill=(60, 44, 30, 255), width=4)
        for k in range(3): yy = 340 - 30 - k * 50; d.polygon([(mx - 34 + k * 3, yy), (mx + 34 - k * 3, yy), (mx + 28 - k * 3, yy - 44), (mx - 28 + k * 3, yy - 44)], fill=(236, 224, 192, 255))
    im = _paint(im, 12, 21, 6).filter(ImageFilter.GaussianBlur(0.8)); im.save(path, optimize=True); return path

def make(name):
    f = dict(carpet=carpet, moon=moon, worldmap=worldmap, starchart=starchart, seascape=seascape)[name]
    return f(os.path.join(OUT, name + '.png'))

if __name__ == '__main__':
    for n in ('carpet', 'moon', 'worldmap', 'starchart', 'seascape'): print(make(n), os.path.getsize(make(n)))
