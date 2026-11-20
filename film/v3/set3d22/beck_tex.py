#!/usr/bin/env python3
"""beck_tex.py : painted textures of the film-22 set (numpy + PIL): signs, roundels, the Beck diagram, the old tangled map, facades,
tiles, posters, sky, river, crowd cards. Everything is cached in tex_beck/ keyed by name + TEX_V. Bump TEX_V after editing a painter.
    tx = ensure()   -> dict name -> png path"""
import os, math, random, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tex_beck')
TEX_V = 18
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FN = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FS = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
def font(sz, f=FB): return ImageFont.truetype(f, int(sz))
def hx(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
RED, BLUE, GREEN, YELLOW, BROWN = '#e3262b', '#1f49c8', '#12a15a', '#ffc81e', '#7a4a22'
CREAM, INK = '#f6ecd0', '#1a1840'

def _save(img, name):
    os.makedirs(OUT, exist_ok=True); p = os.path.join(OUT, '%s_v%d.png' % (name, TEX_V)); img.save(p); return p

def text_c(d, xy, s, fnt, fill, anchor='mm'): d.text(xy, s, font=fnt, fill=fill, anchor=anchor)

def fit_text(d, box, s, fill, f=FB, maxsz=400):
    x0, y0, x1, y1 = box; sz = maxsz
    while sz > 6:
        ft = font(sz, f); bb = d.textbbox((0, 0), s, font=ft)
        if bb[2] - bb[0] <= (x1 - x0) and bb[3] - bb[1] <= (y1 - y0): break
        sz -= 2
    ft = font(sz, f); bb = d.textbbox((0, 0), s, font=ft)
    d.text(((x0 + x1) / 2 - (bb[0] + bb[2]) / 2, (y0 + y1) / 2 - (bb[1] + bb[3]) / 2), s, font=ft, fill=fill)

def noise(rs, h, w, cell=8, amp=1.0):
    g = rs.rand(h // cell + 2, w // cell + 2).astype('float32')
    im = Image.fromarray((g * 255).astype('uint8')).resize((w, h), Image.BICUBIC)
    return np.asarray(im, 'float32') / 255 * amp

# ----------------------------------------------------------------------------- signs
def sign(text, bg, fg, border=None, w=1024, h=256, f=FB, radius=0.12, sub=None):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=int(h * radius), fill=bg)
    b = int(h * 0.08)
    if border: d.rounded_rectangle((b, b, w - 1 - b, h - 1 - b), radius=int(h * radius * .7), outline=border, width=max(4, int(h * .045)))
    if sub:
        fit_text(d, (w * .06, h * .1, w * .94, h * .62), text, fg, f); fit_text(d, (w * .1, h * .66, w * .9, h * .9), sub, fg, FN)
    else: fit_text(d, (w * .06, h * .14, w * .94, h * .86), text, fg, f)
    return img

def roundel(text='UNDERGROUND', w=1024):
    h = int(w * 0.62); S = 2; img = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    cx, cy = w * S / 2, h * S * 0.5; R = h * S * 0.48; t = R * 0.26
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=RED); d.ellipse((cx - R + t, cy - R + t, cx + R - t, cy + R - t), fill=(0, 0, 0, 0))
    bw, bh = w * S * 0.96, R * 0.46
    d.rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), fill=BLUE)
    d.rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy - bh / 2 + bh * .06), fill='#6f8cff');
    fit_text(d, (cx - bw * .45, cy - bh * .36, cx + bw * .45, cy + bh * .36), text, 'white', FB)
    return img.resize((w, h), Image.LANCZOS)

# ----------------------------------------------------------------------------- the Beck diagram (straight lines 0/45/90)
def _thick_line(d, pts, w, col):
    d.line(pts, fill=col, width=w, joint='curve')
    for p in (pts[0], pts[-1]): d.ellipse((p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2), fill=col)

def diagram(W=1536, H=1100):
    S = 2; w, h = W * S, H * S; img = Image.new('RGB', (w, h), '#f7efd6'); d = ImageDraw.Draw(img)
    g = 55 * S
    for x in range(0, w, g): d.line((x, 0, x, h), fill='#eadfbd', width=2)
    for y in range(0, h, g): d.line((0, y, w, y), fill='#eadfbd', width=2)
    # river Thames: pale blue stepped band
    rv = [(0, 780), (330, 780), (420, 870), (900, 870), (1000, 770), (1536, 770)]
    d.line([(x * S, y * S) for x, y in rv], fill='#9fd0ee', width=64 * S, joint='curve')
    def P(pts): return [(x * S, y * S) for x, y in pts]
    lw = 17 * S
    lines = [
        (RED,    [(60, 330), (420, 330), (520, 430), (900, 430), (1000, 330), (1480, 330)]),
        (BLUE,   [(100, 960), (420, 960), (700, 680), (700, 150), (1400, 150)]),
        (GREEN,  [(60, 600), (380, 600), (520, 430), (520, 150), (60, 150)]),
        (YELLOW, [(250, 80), (250, 560), (520, 560), (900, 940), (1480, 940)]),
        (BROWN,  [(1000, 330), (1000, 600), (1250, 850), (1480, 850)]),
        ('#222222', [(700, 430), (700, 680), (900, 870), (1250, 870)]),
    ]
    for col, pts in lines: _thick_line(d, P(pts), lw, col)
    # ticks and stations
    rs = random.Random(5); ft = font(34 * S, FB)
    rings = [(520, 430), (700, 430), (1000, 330), (700, 680), (250, 560), (520, 560), (900, 870), (520, 150), (700, 150)]
    for col, pts in lines:
        for a, b in zip(pts, pts[1:]):
            L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L // 90)
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            for k in range(1, n + 1):
                px, py = a[0] + dx * 90 * k, a[1] + dy * 90 * k
                if math.hypot(b[0] - px, b[1] - py) < 30: continue
                if any(math.hypot(px - rx, py - ry) < 50 for rx, ry in rings): continue
                nx, ny = -dy, dx; r = 18
                d.line(((px - nx * r) * S, (py - ny * r) * S, (px + nx * r) * S, (py + ny * r) * S), fill='#1a1840', width=7 * S)
    for rx, ry in rings:
        R = 30 * S; d.ellipse((rx * S - R, ry * S - R, rx * S + R, ry * S + R), fill='white', outline='#1a1840', width=8 * S)
    names = {(520, 430): 'BANK', (700, 430): 'OXFORD', (1000, 330): 'EUSTON', (700, 680): 'WATERLOO', (250, 560): 'EARLS', (520, 560): 'VICTORIA', (900, 870): 'LEWISHAM', (520, 150): 'KINGS X', (700, 150): 'ANGEL'}
    for (rx, ry), nm in names.items():
        d.text(((rx + 38) * S, (ry - 38) * S), nm, font=ft, fill='#1a1840', anchor='ls')
    d.rectangle((24 * S, 24 * S, (W - 24) * S, (H - 24) * S), outline='#1a1840', width=6 * S)
    d.text((70 * S, 1040 * S), 'UNDERGROUND', font=font(46 * S, FB), fill=RED, anchor='ls')
    return img.resize((W, H), Image.LANCZOS)

def old_map(W=1100, H=800):
    S = 2; w, h = W * S, H * S; img = Image.new('RGB', (w, h), '#e8dcae'); d = ImageDraw.Draw(img); rs = np.random.RandomState(9); rr = random.Random(9)
    n = noise(rs, h, w, 40 * S // 2, 0.12); a = np.asarray(img, 'float32') / 255 - n[..., None] * 0.35; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    # river: wiggly blue ribbon; streets: cramped web
    pts = [(0, 520 * S)];
    for i in range(1, 40): pts.append((i * w / 39, (500 + 110 * math.sin(i * .33) + 40 * math.sin(i * .9)) * S))
    d.line(pts, fill='#7ea6c9', width=46 * S, joint='curve')
    for _ in range(170):
        x, y = rr.uniform(0, w), rr.uniform(0, h); ang = rr.uniform(0, 6.28); pl = [(x, y)]
        for k in range(rr.randint(3, 7)): ang += rr.uniform(-.8, .8); x += math.cos(ang) * rr.uniform(40, 120) * S; y += math.sin(ang) * rr.uniform(40, 120) * S; pl.append((x, y))
        d.line(pl, fill='#b9a46a', width=3 * S)
    cols = [RED, BLUE, GREEN, YELLOW, BROWN, '#333']
    for i, c in enumerate(cols * 2):
        x, y = rr.uniform(0, w), rr.uniform(0, h); ang = rr.uniform(0, 6.28); pl = [(x, y)]
        for k in range(14): ang += rr.uniform(-.7, .7); x += math.cos(ang) * 70 * S; y += math.sin(ang) * 70 * S; pl.append((x, y))
        d.line(pl, fill=c, width=7 * S, joint='curve')
        for p in pl[::2]: d.ellipse((p[0] - 7 * S, p[1] - 7 * S, p[0] + 7 * S, p[1] + 7 * S), fill='white', outline='#222', width=2 * S)
    ft = font(11 * S, FN)
    for _ in range(140): d.text((rr.uniform(0, w), rr.uniform(0, h)), rr.choice(['Kings', 'Cross', 'Bank', 'Ealing', 'Hoxton', 'Soho', 'Mayfair', 'Poplar', 'Bow', 'Kew']), font=ft, fill='#3a2a18')
    d.rectangle((6 * S, 6 * S, w - 6 * S, h - 6 * S), outline='#3a2a18', width=5 * S)
    d.rectangle((w * .22, 18 * S, w * .78, 90 * S), fill='#e8dcae'); fit_text(d, (w * .24, 24 * S, w * .76, 84 * S), 'MAP OF LONDON', '#3a2a18', FS)
    a_ = np.asarray(img.convert('RGB'), 'float32'); sep = np.array([196, 160, 104], 'float32'); lum = a_.mean(-1, keepdims=True) / 255; a_ = a_ * 0.55 + (lum * sep + a_ * 0) * 0.45 + a_ * 0.0
    img = Image.fromarray(np.clip(a_, 0, 255).astype('uint8'))
    return img.resize((W, H), Image.LANCZOS)

# ----------------------------------------------------------------------------- facades
def facade(name, w, h, cols, rows, wall, lit_p, seed, trim='#d9c9a3', big=None, door=False, wcol='#10153c'):
    """Returns (rgb image, glow image). big = (col, row, ncols, nrows) a larger lit window (publicity / lodging)."""
    rs = random.Random(seed); nr = np.random.RandomState(seed)
    img = Image.new('RGB', (w, h), wall); g = Image.new('RGB', (w, h), (0, 0, 0)); d = ImageDraw.Draw(img); gd = ImageDraw.Draw(g)
    base = np.asarray(img, 'float32') / 255; base = base * (0.9 + noise(nr, h, w, 6, 0.2))[..., None]
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for y in range(0, h, 14): d.line((0, y, w, y), fill=tuple(int(c * .86) for c in hx(wall)), width=1)
    cw, ch = w / cols, h / rows
    lights = ['#ffc15a', '#ffb347', '#ffd98a', '#ff9d3c', '#ffe9b0']
    for r in range(rows):
        d.rectangle((0, int(r * ch) + 2, w, int(r * ch) + 8), fill=trim)
        for c in range(cols):
            x0, y0 = c * cw + cw * .28, r * ch + ch * .26; x1, y1 = c * cw + cw * .72, r * ch + ch * .8
            if big and big[0] <= c < big[0] + big[2] and big[1] <= r < big[1] + big[3]:
                continue
            d.rectangle((x0 - 5, y0 - 5, x1 + 5, y1 + 5), fill=trim)
            on = rs.random() < lit_p
            if door and r == rows - 1: continue
            if on:
                col = rs.choice(lights); d.rectangle((x0, y0, x1, y1), fill=col); gd.rectangle((x0, y0, x1, y1), fill=col)
                d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill='#7a4a22', width=4); d.line((x0, (y0 + y1) / 2, x1, (y0 + y1) / 2), fill='#7a4a22', width=4)
                if rs.random() < .5: d.rectangle((x0 + 4, y0 + 4, x0 + (x1 - x0) * .4, y1 - 6), fill='#c96a28')
            else:
                d.rectangle((x0, y0, x1, y1), fill=wcol); d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill='#2a3470', width=3)
    if big:
        c0, r0, nc, nrw = big; x0, y0 = c0 * cw + cw * .12, r0 * ch + ch * .14; x1, y1 = (c0 + nc) * cw - cw * .12, (r0 + nrw) * ch - ch * .12
        d.rectangle((x0 - 9, y0 - 9, x1 + 9, y1 + 9), fill=trim); d.rectangle((x0, y0, x1, y1), fill='#ffd27a'); gd.rectangle((x0, y0, x1, y1), fill='#ffd27a')
        # posters / figures inside the big window
        k = 6
        for i in range(k):
            px = x0 + (x1 - x0) * (i + .5) / k; pw = (x1 - x0) / k * .62; pc = [RED, BLUE, GREEN, '#ffffff', YELLOW, '#e3262b'][i % 6]
            d.rectangle((px - pw / 2, y0 + (y1 - y0) * .18, px + pw / 2, y0 + (y1 - y0) * .72), fill=pc, outline='#1a1840', width=3)
            d.ellipse((px - pw * .22, y0 + (y1 - y0) * .3, px + pw * .22, y0 + (y1 - y0) * .5), fill='#ffe2a8')
        for i in range(1, 3): d.line((x0 + (x1 - x0) * i / 3, y0, x0 + (x1 - x0) * i / 3, y1), fill='#7a4a22', width=6)
        d.line((x0, (y0 + y1) / 2 + 40, x1, (y0 + y1) / 2 + 40), fill='#7a4a22', width=6)
    if door:
        d.rectangle((w * .42, h * (rows - 1) / rows + 14, w * .58, h), fill='#5a2a14')
    return img, g

def hq_facade():
    w, h = 1792, 1020
    a, g = facade('hq', w, h, 14, 6, '#c9b48a', 0.7, 11, trim='#efe0b8', big=(5, 2, 4, 2), door=False)
    return a, g

def lodging_facade():
    w, h = 460, 1040; rs = random.Random(3); nr = np.random.RandomState(3)
    img = Image.new('RGB', (w, h), '#a8452c'); d = ImageDraw.Draw(img); gm = Image.new('RGB', (w, h), (0, 0, 0)); gd = ImageDraw.Draw(gm)
    a = np.asarray(img, 'float32') / 255 * (0.88 + noise(nr, h, w, 5, 0.25))[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for y in range(0, h, 13): d.line((0, y, w, y), fill='#7d2f1c', width=2)
    cols, rows = 2, 6; cw, ch = w / cols, h / rows
    for r in range(rows):
        d.rectangle((0, r * ch + 4, w, r * ch + 12), fill='#e8d8ae')
        for c in range(cols):
            x0, y0, x1, y1 = c * cw + cw * .2, r * ch + ch * .18, c * cw + cw * .8, r * ch + ch * .8
            d.rectangle((x0 - 7, y0 - 7, x1 + 7, y1 + 7), fill='#f2e8c8')
            if r == 3 and c == 0:
                d.rectangle((x0, y0, x1, y1), fill='#ffd36e'); gd.rectangle((x0, y0, x1, y1), fill='#ffd36e')
                d.rectangle((x0 + 10, y0 + 20, x0 + 26, y1 - 8), fill='#3aa86a')   # green lamp shade silhouette
                d.rectangle((x0 + 4, (y0 + y1) / 2, x1 - 4, (y0 + y1) / 2 + 7), fill='#7a4a22'); d.rectangle(((x0 + x1) / 2 - 3, y0, (x0 + x1) / 2 + 3, y1), fill='#7a4a22')
            else:
                d.rectangle((x0, y0, x1, y1), fill='#10153c'); d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill='#2a3470', width=3)
                if rs.random() < .3 and r != 3: d.rectangle((x0, y0, x1, y1), fill='#ffb347'); gd.rectangle((x0, y0, x1, y1), fill='#ffb347')
    d.rectangle((w * .36, h - 150, w * .64, h), fill='#2a2a60')
    return img, gm

def plain_brick(name, base, seed, w=512, h=512, line='#7d2f1c'):
    nr = np.random.RandomState(seed); img = Image.new('RGB', (w, h), base); d = ImageDraw.Draw(img)
    for r in range(0, h, 16):
        for c in range(-32 if (r // 16) % 2 else 0, w, 64):
            k = 0.85 + nr.rand() * .3; col = tuple(min(255, int(v * k)) for v in hx(base)); d.rectangle((c + 2, r + 2, c + 62, r + 14), fill=col)
    return img

# ----------------------------------------------------------------------------- city backdrop, sky, river
def dusk_sky(W=2048, H=1024):
    """Equirect-ish: v 0.5 = horizon. Deep blue zenith, warm orange band, stars."""
    y = np.linspace(0, 1, H)[:, None]; t = np.clip((0.5 - y) / 0.5, 0, 1)    # 0 horizon .. 1 zenith
    top = np.array([0.04, 0.07, 0.42]); mid = np.array([0.30, 0.18, 0.62]); hor = np.array([1.0, 0.52, 0.16]); low = np.array([0.95, 0.4, 0.14])
    c = np.zeros((H, 1, 3), 'float32')
    stops = [(0.0, (1.0, 0.55, 0.14)), (0.03, (1.0, 0.45, 0.2)), (0.045, (0.30, 0.15, 0.50)), (0.085, (0.07, 0.10, 0.50)), (0.4, (0.04, 0.07, 0.42)), (1.0, (0.03, 0.05, 0.34))]
    for i in range(H):
        tt = t[i, 0]
        if y[i, 0] > 0.5: c[i, 0] = np.array(stops[0][1]) * (1 - min(1, (y[i, 0] - .5) * 12)) + np.array((0.2, 0.1, 0.4)) * min(1, (y[i, 0] - .5) * 12)
        else:
            for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
                if t0 <= tt <= t1: k = (tt - t0) / (t1 - t0); c[i, 0] = np.array(c0) * (1 - k) + np.array(c1) * k; break
    img = np.repeat(c, W, 1); rs = np.random.RandomState(4)
    for _ in range(0):
        sx, sy = rs.randint(0, W), int(H * (0.5 - rs.uniform(.03, .3)))
        b = rs.uniform(.6, 1.0); img[sy:sy + 2, sx:sx + 2] = np.array((1, 0.95, 0.8), "float32") * b
    return Image.fromarray((np.clip(img, 0, 1) * 255).astype('uint8'))

def night_sky(W=2048, H=1024):
    y = np.linspace(0, 1, H)[:, None]; t = np.clip((0.5 - y) / 0.5, 0, 1); c = np.zeros((H, 1, 3), 'float32')
    stops = [(0.0, (0.46, 0.26, 0.40)), (0.025, (0.30, 0.18, 0.46)), (0.07, (0.07, 0.10, 0.46)), (0.4, (0.035, 0.06, 0.34)), (1.0, (0.02, 0.04, 0.26))]
    for i in range(H):
        tt = t[i, 0]
        if y[i, 0] > 0.5: c[i, 0] = np.array(stops[0][1]) * 0.5
        else:
            for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
                if t0 <= tt <= t1: k = (tt - t0) / (t1 - t0); c[i, 0] = np.array(c0) * (1 - k) + np.array(c1) * k; break
    return Image.fromarray((np.clip(np.repeat(c, W, 1), 0, 1) * 255).astype('uint8'))

def skyline(W=2048, H=512, seed=2):
    """1930s London far skyline cutout (RGBA): low near-black blue roofs, chimneys, 2 spires, the dome, Big Ben, a gasholder, smoke plumes."""
    rs = random.Random(seed); img = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img); base = H; sil = (20, 24, 56, 255)
    x = 0
    while x < W:
        bw = rs.randint(40, 110); bh = rs.randint(40, 100)
        d.rectangle((x, base - bh, x + bw, base), fill=sil)
        k = rs.random()
        if k < .55: d.polygon([(x - 4, base - bh), (x + bw / 2, base - bh - rs.randint(14, 30)), (x + bw + 4, base - bh)], fill=sil)
        for cx in (x + bw * .25, x + bw * .7):
            if rs.random() < .6:
                ch = rs.randint(14, 28); d.rectangle((cx - 4, base - bh - ch - 6, cx + 4, base - bh - 2), fill=sil)
                if rs.random() < .4:
                    for j in range(3): d.ellipse((cx - 10 + j * 8, base - bh - ch - 30 - j * 14, cx + 6 + j * 8, base - bh - ch - 10 - j * 14), fill=(52, 50, 96, 255))
        for yy in range(base - bh + 10, base - 6, 20):
            for xx in range(x + 8, x + bw - 10, 18):
                if rs.random() < .15: d.rectangle((xx, yy, xx + 5, yy + 8), fill=(255, 190, 100, 255))
        x += bw + rs.randint(-4, 4)
    def spire(cx, h, w=14):
        d.polygon([(cx - w / 2, base - 60), (cx, base - 60 - h), (cx + w / 2, base - 60)], fill=sil); d.rectangle((cx - w / 2, base - 100, cx + w / 2, base), fill=sil)
    spire(420, 100); spire(1500, 90)
    # gasholder ring
    gx = 700; d.rectangle((gx - 60, base - 70, gx + 60, base), fill=sil); d.arc((gx - 60, base - 100, gx + 60, base - 40), 180, 360, fill=sil, width=6)
    return img

def river(W=1024, H=1024):
    nr = np.random.RandomState(8); y = np.linspace(0, 1, H)[:, None, None]
    base = np.zeros((H, W, 3), 'float32'); base[:] = np.array([0.10, 0.20, 0.56]) * (1 - y * .3) + np.array([0.9, 0.42, 0.2]) * y * .25
    img = Image.fromarray((np.clip(base, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for _ in range(900):  # ripples
        x, yy = nr.randint(0, W), nr.randint(0, H); l = nr.randint(10, 60)
        d.line((x, yy, x + l, yy), fill=(70, 120, 220) if nr.rand() < .6 else (255, 190, 100), width=2)
    for xx in range(60, W, 170):  # warm lamp / window glitter columns
        for yy in range(0, H, 22):
            if nr.rand() < .75: l = nr.randint(18, 60); x0 = xx + nr.randint(-14, 14); d.rectangle((x0, yy, x0 + l * .5, yy + 7), fill=(255, 200 + nr.randint(0, 50), 110))
    return img

def farground_dark(W=8, H=512):
    a = np.zeros((H, W, 3), 'float32'); a[:] = (0.06, 0.07, 0.22); return Image.fromarray((a * 255).astype('uint8'))

def farground(W=8, H=512):
    y = np.linspace(0, 1, H)[:, None, None]; c0 = np.array([0.30, 0.16, 0.50]); c1 = np.array([1.0, 0.55, 0.2])
    a = c0 * (1 - y ** 1.8) + c1 * y ** 1.8; a = np.repeat(a, W, 1)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def halo(rgb, W=256):
    yy, xx = np.mgrid[0:W, 0:W].astype('float32'); r = np.hypot(xx - W / 2, yy - W / 2) / (W / 2)
    f = np.clip(1 - r, 0, 1) ** 2.2; core = np.clip(1 - r * 3.2, 0, 1)
    a = np.stack([f * rgb[0] + core * .6, f * rgb[1] + core * .6, f * rgb[2] + core * .5], -1)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def beam_glow(rgb, W=256, H=512):
    yy, xx = np.mgrid[0:H, 0:W].astype('float32'); u = (xx / W - .5) * 2; v = yy / H
    f = np.clip(1 - np.abs(u) / (0.15 + .85 * v), 0, 1) ** 1.5 * (1 - v) ** 1.2
    return Image.fromarray((np.clip(np.stack([f * rgb[0], f * rgb[1], f * rgb[2]], -1), 0, 1) * 255).astype('uint8'))

# ----------------------------------------------------------------------------- vehicles, ground
def bus_side(w=1400, h=420):
    img = Image.new('RGB', (w, h), '#c8201e'); d = ImageDraw.Draw(img); gm = Image.new('RGB', (w, h), (0, 0, 0)); gd = ImageDraw.Draw(gm)
    d.rectangle((w - 150, int(h * .55), w, int(h * .92)), fill='#2a0a14'); d.line((w - 140, int(h * .9), w - 20, int(h * .6)), fill='#ffd88a', width=10); d.rectangle((0, int(h * .47), w, int(h * .53)), fill=CREAM); d.rectangle((0, int(h * .93), w, h), fill='#3a0a10')
    for row, (y0, y1) in enumerate(((int(h * .08), int(h * .41)), (int(h * .56), int(h * .86)))):
        n = 11
        for i in range(n):
            x0 = 60 + i * (w - 140) / n; x1 = x0 + (w - 140) / n - 14
            if row == 0 and i in (4, 5, 6): d.rectangle((x0, y0, x1, y1), fill=YELLOW); fit_text(d, (x0 + 6, y0 + 6, x1 - 6, y1 - 6), 'TEA', RED); continue
            if row == 1 and i in (5, 6): d.rectangle((x0, y0, x1, y1), fill=BLUE); fit_text(d, (x0 + 6, y0 + 12, x1 - 6, y1 - 12), 'VIM', 'white'); continue
            d.rectangle((x0, y0, x1, y1), fill='#ffc65a'); gd.rectangle((x0, y0, x1, y1), fill='#ffc65a')
            if (i + row) % 2 == 0: d.ellipse((x0 + 14, y0 + 14, x0 + 44, y0 + 44), fill='#ffe2a8'); d.rectangle((x0 + 8, y0 + 46, x0 + 50, y1), fill=['#2a5a98', '#6a2a60', '#2a7a58'][i % 3])
            d.line(((x0 + x1) / 2, y0, (x0 + x1) / 2, y1), fill=RED, width=5)
    d.rectangle((w - 10 - 150, int(h * .02), w - 10, int(h * .1)), fill='#111'); d.text((w - 160, int(h * .06)), '11 BANK', font=font(22), fill='#ffc65a', anchor='lm')
    return img, gm

def cab_side(w=640, h=260):
    img = Image.new('RGB', (w, h), '#151933'); d = ImageDraw.Draw(img); gm = Image.new('RGB', (w, h), (0, 0, 0)); gd = ImageDraw.Draw(gm)
    d.rectangle((60, 40, w - 220, 140), fill='#ffc65a'); gd.rectangle((60, 40, w - 220, 140), fill='#ffc65a'); d.rectangle((w - 210, 60, w - 40, 140), fill='#ffc65a'); gd.rectangle((w - 210, 60, w - 40, 140), fill='#ffc65a')
    d.line((w / 2 - 60, 40, w / 2 - 60, 140), fill='#151933', width=10); d.rectangle((0, 150, w, 160), fill='#c9a02a')
    return img, gm

def road(W=1024, H=1024):
    nr = np.random.RandomState(7); a = np.zeros((H, W, 3), 'float32'); a[:] = (0.20, 0.22, 0.42); a *= (0.85 + noise(nr, H, W, 4, .3))[..., None]
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for x in range(0, W, 128): d.rectangle((x + 20, H // 2 - 6, x + 90, H // 2 + 6), fill='#f1e6b8')
    return img

def pavement(W=512, H=512, base=(0.55, 0.52, 0.66)):
    nr = np.random.RandomState(6); a = np.zeros((H, W, 3), 'float32'); a[:] = base; a *= (0.88 + noise(nr, H, W, 5, .24))[..., None]
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for x in range(0, W, 64): d.line((x, 0, x, H), fill=(50, 50, 100), width=2)
    for y in range(0, H, 64): d.line((0, y, W, y), fill=(50, 50, 100), width=2)
    return img

def grate(W=512):
    img = Image.new('RGB', (W, W), '#150f1a'); d = ImageDraw.Draw(img); g = Image.new('RGB', (W, W), (0, 0, 0)); gd = ImageDraw.Draw(g)
    for i in range(10):
        x = 30 + i * 46; d.rectangle((x, 24, x + 26, W - 24), fill=(150, 70, 30)); gd.rectangle((x, 24, x + 26, W - 24), fill=(255, 150, 55))
    d.rectangle((0, 0, W - 1, W - 1), outline='#3a3050', width=22)
    return img, g

def slate(W=256, H=256, base='#33407a'):
    nr = np.random.RandomState(2); img = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(img)
    for r in range(0, H, 16):
        for c in range(0, W, 24): k = .8 + nr.rand() * .4; d.rectangle((c + (12 if (r // 16) % 2 else 0) + 1, r + 1, c + 22, r + 14), fill=tuple(min(255, int(v * k)) for v in hx(base)))
    return img

# ----------------------------------------------------------------------------- crowd / actor cards (own painted extras with hats + rim)
def crowd_card(variant, rim=(255, 160, 70), side='r', w=200, h=440, dark=1.0):
    S = 2; img = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    coats = ['#b3262e', '#2f4fb8', '#1f8a52', '#6b3a22', '#7a2a86', '#c98a1a', '#2a2a40', '#d6552a']
    coat = coats[variant % len(coats)]; hat = variant % 4
    cx = w * S / 2; hr = 44 * S; hy = 95 * S
    ink = '#1a1840'; lw = 5 * S
    d.line((cx - 18 * S, 250 * S, cx - 28 * S, 410 * S), fill=ink, width=lw + 2 * S); d.line((cx + 18 * S, 250 * S, cx + 28 * S, 410 * S), fill=ink, width=lw + 2 * S)
    d.rounded_rectangle((cx - 28 * S, 410 * S, cx - 4 * S, 424 * S), radius=6 * S, fill=ink); d.rounded_rectangle((cx + 4 * S, 410 * S, cx + 34 * S, 424 * S), radius=6 * S, fill=ink)
    d.rounded_rectangle((cx - 52 * S, 150 * S, cx + 52 * S, 300 * S), radius=34 * S, fill=coat, outline=ink, width=lw)
    d.line((cx, 160 * S, cx, 296 * S), fill=ink, width=3 * S)
    d.line((cx - 50 * S, 175 * S, cx - 80 * S, 270 * S), fill=coat, width=24 * S); d.line((cx + 50 * S, 175 * S, cx + 80 * S, 270 * S), fill=coat, width=24 * S)
    if variant % 3 == 0: d.rectangle((cx + 62 * S, 262 * S, cx + 106 * S, 296 * S), fill='#5a3a1a', outline=ink, width=3 * S)    # briefcase
    if variant % 3 == 1: d.rectangle((cx - 100 * S, 238 * S, cx - 58 * S, 276 * S), fill='#f6ecd0', outline=ink, width=3 * S); d.line((cx - 92 * S, 250 * S, cx - 66 * S, 250 * S), fill=RED, width=3 * S)  # folded map
    d.ellipse((cx - hr, hy - hr, cx + hr, hy + hr), fill='#fff4e0', outline=ink, width=lw)
    d.ellipse((cx - 22 * S, hy - 6 * S, cx - 12 * S, hy + 8 * S), fill=ink); d.ellipse((cx + 12 * S, hy - 6 * S, cx + 22 * S, hy + 8 * S), fill=ink)
    d.arc((cx - 14 * S, hy + 6 * S, cx + 14 * S, hy + 28 * S), 20, 160, fill=ink, width=3 * S)
    if hat == 0: d.rounded_rectangle((cx - 40 * S, hy - 62 * S, cx + 40 * S, hy - 22 * S), radius=30 * S, fill='#262040', outline=ink, width=lw); d.rectangle((cx - 52 * S, hy - 28 * S, cx + 52 * S, hy - 16 * S), fill='#262040', outline=ink, width=3 * S)   # bowler
    elif hat == 1: d.polygon([(cx - 46 * S, hy - 14 * S), (cx - 34 * S, hy - 62 * S), (cx + 34 * S, hy - 62 * S), (cx + 46 * S, hy - 14 * S)], fill=coats[(variant + 3) % 8], outline=ink); d.rectangle((cx - 52 * S, hy - 24 * S, cx + 52 * S, hy - 12 * S), fill=coats[(variant + 3) % 8], outline=ink, width=3 * S)  # cloche/trilby
    elif hat == 2: d.rectangle((cx - 36 * S, hy - 72 * S, cx + 36 * S, hy - 18 * S), fill='#1c1c30', outline=ink, width=lw); d.rectangle((cx - 54 * S, hy - 24 * S, cx + 54 * S, hy - 12 * S), fill='#1c1c30', outline=ink, width=3 * S)     # top hat
    else: d.pieslice((cx - 46 * S, hy - 62 * S, cx + 46 * S, hy + 4 * S), 180, 360, fill='#5a4a30', outline=ink, width=lw)      # flat cap
    img = img.resize((w, h), Image.LANCZOS)
    if dark < 1.0:
        a = np.asarray(img, 'float32'); a[..., :3] *= dark; img = Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGBA')
    return add_rim(img, rim, side)

def add_rim(img, rim, side='r', px=7, k=1.0):
    """Painted rim light: a bright edge band on the side facing the light, only where the card has alpha."""
    a = np.asarray(img.convert('RGBA'), 'float32'); al = a[..., 3] / 255
    m = Image.fromarray((al * 255).astype('uint8')); sh = np.roll(np.asarray(m, 'float32') / 255, -px if side == 'r' else px, axis=1)
    edge = np.clip(al - sh, 0, 1)
    edge = np.maximum(edge, 0) * (al > 0.5)
    col = np.array(rim, 'float32')
    for c in range(3): a[..., c] = a[..., c] * (1 - edge * k) + col[c] * edge * k
    return Image.fromarray(np.clip(a, 0, 255).astype('uint8'), 'RGBA')

# ----------------------------------------------------------------------------- interior art
def cork_board(W=1024, H=700):
    nr = np.random.RandomState(12); a = np.zeros((H, W, 3), 'float32'); a[:] = (0.78, 0.52, 0.28); a *= (0.8 + noise(nr, H, W, 3, .45))[..., None]
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img); rr = random.Random(12)
    d.rectangle((0, 0, W - 1, H - 1), outline='#5a2f14', width=26)
    pos = [(70, 70), (400, 60), (720, 90), (90, 380), (400, 370), (730, 390)]
    for (x, y) in pos:
        w, h = 270, 260; d.rectangle((x + 6, y + 6, x + w + 6, y + h + 6), fill='#6a4020'); d.rectangle((x, y, x + w, y + h), fill='#f7f1e0', outline='#3a3a60', width=2)
        cc = rr.choice([BLUE, RED, GREEN]); pts = []
        for k in range(8):   # circuit drawing: rectilinear traces, chips, resistors
            x0, y0 = x + rr.randint(20, w - 40), y + rr.randint(20, h - 40); x1 = x + rr.randint(20, w - 40); y1 = y + rr.randint(20, h - 40)
            d.line((x0, y0, x1, y0, x1, y1), fill=cc if k % 2 else '#1a1840', width=4)
            d.rectangle((x0 - 9, y0 - 5, x0 + 9, y0 + 5), fill='white', outline='#1a1840', width=2)
        d.rectangle((x + w * .4, y + h * .4, x + w * .6, y + h * .6), fill='#1a1840')
        for k in range(5): d.line((x + w * .4 + k * 8 + 2, y + h * .36, x + w * .4 + k * 8 + 2, y + h * .4), fill='#1a1840', width=3)
        d.ellipse((x + w / 2 - 8, y - 8, x + w / 2 + 8, y + 8), fill=RED, outline='#5a0a10')
    return img

def wallpaper(W=512, H=512, base='#e0a64a', motif='#a8283a', alt='#2a5a8a'):
    img = Image.new('RGB', (W, H), base); d = ImageDraw.Draw(img)
    for x in range(0, W, 64): d.line((x, 0, x, H), fill=tuple(int(c * .93) for c in hx(base)), width=10)
    for r in range(0, H, 128):
        for c in range(0, W, 128):
            ox = 64 if (r // 128) % 2 else 0; cx, cy = c + ox + 32, r + 64
            for ang in range(0, 360, 60):
                px, py = cx + 18 * math.cos(math.radians(ang)), cy + 18 * math.sin(math.radians(ang)); d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=motif)
            d.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill='#ffe9b0'); d.polygon([(cx, cy + 44), (cx - 12, cy + 64), (cx + 12, cy + 64)], fill=alt)
    return img

def wood(W=512, H=512, base=(0.55, 0.30, 0.14)):
    nr = np.random.RandomState(1); a = np.zeros((H, W, 3), 'float32'); a[:] = base
    n = noise(nr, H, W // 8 + 1, 6, 1.0); n = np.asarray(Image.fromarray((n * 255).astype('uint8')).resize((W, H), Image.BICUBIC), 'float32') / 255
    a *= (0.75 + n * .5)[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for x in range(0, W, 64): d.line((x, 0, x, H), fill=(60, 30, 14), width=3)
    return img

def paper_note(text, w=512, h=360, bg='#f6efd8', stamp='NOTICE', stamp_col=RED):
    img = Image.new('RGB', (w, h), bg); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, w - 1, h - 1), outline='#8a7a50', width=6)
    for i in range(6): d.line((40, 150 + i * 30, w - 40, 150 + i * 30), fill='#8a8a9a', width=4)
    d.text((40, 40), 'Underground Electric Railways', font=font(22, FN), fill='#3a3a60')
    d.rectangle((40, 70, w - 40, 128), outline=stamp_col, width=6); fit_text(d, (50, 76, w - 50, 122), stamp, stamp_col, FB)
    return img

def poster(i, w=400, h=560):
    rs = random.Random(i * 7 + 1); pal = [(RED, CREAM, BLUE), (BLUE, YELLOW, '#ffffff'), (GREEN, CREAM, RED), (YELLOW, BLUE, RED), ('#1a1840', YELLOW, '#ffffff')][i % 5]
    img = Image.new('RGB', (w, h), pal[0]); d = ImageDraw.Draw(img)
    d.ellipse((w * .25, h * .12, w * .75, h * .12 + w * .5), fill=pal[1]); d.polygon([(0, h * .72), (w * .35, h * .45), (w * .65, h * .65), (w, h * .4), (w, h * .8), (0, h * .8)], fill=pal[2])
    d.rectangle((0, h * .76, w, h), fill='#f6ecd0'); t = ['THE ZOO', 'WEMBLEY', 'KEW GARDENS', 'THE THEATRE', 'TO THE SEA'][i % 5]
    fit_text(d, (20, h * .79, w - 20, h * .93), t, '#1a1840'); d.rectangle((6, 6, w - 7, h - 7), outline='#1a1840', width=8)
    return img

def night_city(W=1024, H=1400, hq=True):
    """View out of Beck's window: deep blue night, the lit HQ across the street with a roundel, lamp halos, rooftops, stars."""
    rs = random.Random(21); y = np.linspace(0, 1, H)[:, None, None]
    a = np.zeros((H, W, 3), 'float32'); a[:] = np.array([0.04, 0.08, 0.46]) * (1 - y) + np.array([0.55, 0.25, 0.55]) * y
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for _ in range(160): x, yy = rs.randint(0, W), rs.randint(0, int(H * .5)); d.rectangle((x, yy, x + 3, yy + 3), fill=(255, 245, 210))
    x = 0
    while x < W:  # far roofs
        bw = rs.randint(70, 160); bh = rs.randint(160, 420); d.rectangle((x, H - bh - 260, x + bw, H), fill=(26, 28, 92))
        for yy in range(H - bh - 240, H - 260, 38):
            for xx in range(x + 10, x + bw - 16, 30):
                if rs.random() < .55: d.rectangle((xx, yy, xx + 13, yy + 20), fill=rs.choice([(255, 196, 96), (255, 160, 70), (255, 230, 160)]))
        x += bw + 6
    # the HQ with its roundel across the street
    d.rectangle((20, H - 760, 800, H), fill=(52, 44, 110))
    for r in range(8):
        for c in range(14):
            xx, yy = 40 + c * 54, H - 740 + r * 80
            if rs.random() < .66: d.rectangle((xx, yy, xx + 34, yy + 52), fill=rs.choice([(255, 196, 96), (255, 218, 130), (255, 170, 80)]))
            else: d.rectangle((xx, yy, xx + 34, yy + 52), fill=(20, 22, 70))
    rd = roundel('UNDERGROUND', 380); img.paste(rd, (60, H - 520), rd)
    return img

def station_wall(name, w=1024, h=1024, base='#f2e6c6', band='#8c1c2e', band_y=(0.46, 0.64)):
    """Glazed tiles: 4x4 grid per tile, bevel lines, a maroon band with a cream stripe."""
    img = Image.new('RGB', (w, h), base); d = ImageDraw.Draw(img); nr = np.random.RandomState(3)
    a = np.asarray(img, 'float32') / 255 * (0.94 + noise(nr, h, w, 32, 0.1))[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    ts = w // 8
    for i in range(0, w + 1, ts): d.line((i, 0, i, h), fill='#c9b88e', width=3)
    for j in range(0, h + 1, ts // 2): d.line((0, j, w, j), fill='#c9b88e', width=3)
    if band is None: return img
    y0, y1 = int(h * band_y[0]), int(h * band_y[1]); d.rectangle((0, y0, w, y1), fill=band)
    d.rectangle((0, y0 + 8, w, y0 + 22), fill='#f2e6c6'); d.rectangle((0, y1 - 22, w, y1 - 8), fill='#f2e6c6')
    for i in range(0, w + 1, ts): d.line((i, y0 + 22, i, y1 - 22), fill='#6a1020', width=3)
    return img

def train_side(w=1200, h=420):
    img = Image.new('RGB', (w, h), RED); d = ImageDraw.Draw(img); g = Image.new('RGB', (w, h), (0, 0, 0)); gd = ImageDraw.Draw(g)
    d.rectangle((0, int(h * .5), w, int(h * .58)), fill=CREAM); d.rectangle((0, int(h * .9), w, h), fill='#3a0810')
    for i in range(8):
        x0 = 30 + i * 145; x1 = x0 + 110
        d.rectangle((x0, 60, x1, int(h * .46)), fill='#ffd88a', outline='#1a1840', width=6); gd.rectangle((x0, 60, x1, int(h * .46)), fill='#ffd88a')
        if i % 2 == 0: d.ellipse((x0 + 34, 90, x0 + 76, 132), fill='#ffe9c4'); d.rectangle((x0 + 24, 134, x0 + 86, int(h * .46)), fill=['#2a5a98', '#6a2a60', '#2a7a58', '#8a4a22'][i % 4])
        d.rectangle((x0 + 6, int(h * .62), x1 - 6, int(h * .84)), fill='#c01c24')
    return img, g

def quilt(W=512, H=512):
    rs = random.Random(8); img = Image.new('RGB', (W, H), '#f6ecd0'); d = ImageDraw.Draw(img); cols = [RED, BLUE, GREEN, YELLOW, '#ff7a1e', '#7a3a8a', '#f6ecd0']; n = 8; s = W // n
    for i in range(n):
        for j in range(n):
            c = rs.choice(cols); d.rectangle((i * s, j * s, (i + 1) * s, (j + 1) * s), fill=c)
            if rs.random() < .5: d.polygon([(i * s, j * s), ((i + 1) * s, j * s), ((i + 1) * s, (j + 1) * s)], fill=rs.choice(cols))
            d.rectangle((i * s, j * s, (i + 1) * s, (j + 1) * s), outline='#1a1840', width=3)
    return img

def blob(w=128):
    yy, xx = np.mgrid[0:w, 0:w].astype('float32'); r = np.hypot(xx - w / 2, yy - w / 2) / (w / 2)
    a = np.clip(1 - r, 0, 1) ** 0.8 * 0.9; img = np.zeros((w, w, 4), 'uint8'); img[..., 3] = (a * 255).astype('uint8'); img[..., :3] = (6, 6, 30)
    return Image.fromarray(img, 'RGBA')

def clock_face(w=512):
    img = Image.new('RGBA', (w, w), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = w / 2
    d.ellipse((4, 4, w - 5, w - 5), fill='#1a1840'); d.ellipse((24, 24, w - 25, w - 25), fill='#fff6dc')
    for k in range(12):
        a = math.radians(k * 30); d.line((c + math.sin(a) * c * .78, c - math.cos(a) * c * .78, c + math.sin(a) * c * .9, c - math.cos(a) * c * .9), fill='#1a1840', width=14)
    d.line((c, c, c + c * .25, c - c * .42), fill='#1a1840', width=18); d.line((c, c, c - c * .52, c + c * .12), fill='#1a1840', width=12); d.ellipse((c - 14, c - 14, c + 14, c + 14), fill=RED)
    return img

def train_front(w=600, h=700):
    img = Image.new('RGB', (w, h), RED); d = ImageDraw.Draw(img); g = Image.new('RGB', (w, h), (0, 0, 0)); gd = ImageDraw.Draw(g)
    d.rectangle((0, 0, w, 40), fill='#5a0a14'); d.rectangle((40, 70, w - 40, 330), fill='#ffd88a', outline='#1a1840', width=10); gd.rectangle((40, 70, w - 40, 330), fill='#ffd88a')
    d.line((w / 2, 70, w / 2, 330), fill='#1a1840', width=14); d.rectangle((0, 560, w, h), fill='#3a0810')
    d.rectangle((w * .32, 360, w * .68, 420), fill=CREAM); fit_text(d, (w * .34, 366, w * .66, 414), 'PICCADILLY', '#1a1840')
    return img, g

def floor_platform(W=1024, H=1024):
    nr = np.random.RandomState(5); a = np.zeros((H, W, 3), 'float32'); a[:] = (0.50, 0.48, 0.68); a *= (0.86 + noise(nr, H, W, 6, .3))[..., None]
    img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for x in range(0, W, 128): d.line((x, 0, x, H), fill=(46, 44, 98), width=3)
    for y in range(0, H, 128): d.line((0, y, W, y), fill=(46, 44, 98), width=3)
    return img

def ballast(W=512, H=512):
    nr = np.random.RandomState(9); a = np.zeros((H, W, 3), 'float32'); a[:] = (0.18, 0.18, 0.40); a *= (0.7 + noise(nr, H, W, 3, .7))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def way_out(w=900, h=300):
    img = Image.new('RGB', (w, h), GREEN); d = ImageDraw.Draw(img); d.rectangle((10, 10, w - 11, h - 11), outline='white', width=10)
    fit_text(d, (60, 50, w * .7, h - 50), 'WAY OUT', 'white'); d.polygon([(w * .76, h * .5 - 50), (w * .76 + 90, h * .5 - 50), (w * .76 + 90, h * .5 - 90), (w - 40, h * .5), (w * .76 + 90, h * .5 + 90), (w * .76 + 90, h * .5 + 50), (w * .76, h * .5 + 50)], fill='white')
    return img


def paper_grid(W=1024, H=740):
    img = Image.new('RGB', (W, H), '#f4ead0'); d = ImageDraw.Draw(img); rs = np.random.RandomState(12)
    a = np.asarray(img, 'float32') / 255 * (0.94 + noise(rs, H, W, 30, 0.08))[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for x in range(0, W, 41): d.line((x, 0, x, H), fill='#e2d4ac', width=2)
    for y in range(0, H, 41): d.line((0, y, W, y), fill='#e2d4ac', width=2)
    d.rectangle((10, 10, W - 11, H - 11), outline='#1a1840', width=6)
    d.text((40, H - 40), 'UNDERGROUND', font=font(30, FB), fill='#c8a8a0', anchor='ls')
    return img

def rag_rug(W=512, H=512):
    img = Image.new('RGB', (W, H), '#4a1a2a'); d = ImageDraw.Draw(img); rr = random.Random(3)
    cols = ['#8a2a3a', '#1f3f86', '#c8982e', '#2a6a4e', '#d8c8a0', '#6a2a7a']
    for i in range(9, 0, -1):
        r = i * 27; d.ellipse((W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r), fill=cols[i % len(cols)], outline='#2a1430', width=3)
    a = np.asarray(img, 'float32') / 255; nr = np.random.RandomState(4); a = a * (0.82 + noise(nr, H, W, 4, 0.3))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8'))

def circuit_sheet(W=640, H=460, seed=1):
    img = Image.new('RGB', (W, H), '#1a3a90'); d = ImageDraw.Draw(img); rr = random.Random(seed)
    for x in range(0, W, 32): d.line((x, 0, x, H), fill='#2a52b8', width=1)
    for y in range(0, H, 32): d.line((0, y, W, y), fill='#2a52b8', width=1)
    for k in range(7):
        x, y = rr.randint(1, 8) * 64, rr.randint(1, 6) * 64; pts = [(x, y)]
        for j in range(4):
            if j % 2 == 0: x += rr.choice([-1, 1]) * rr.randint(1, 3) * 64
            else: y += rr.choice([-1, 1]) * rr.randint(1, 2) * 64
            pts.append((min(W - 20, max(20, x)), min(H - 20, max(20, y))))
        d.line(pts, fill='#ffffff', width=7, joint='curve')
        for p in pts: d.ellipse((p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9), fill='#ffd22a', outline='white', width=2)
    d.rectangle((6, 6, W - 7, H - 7), outline='white', width=5)
    d.text((24, H - 20), 'CIRCUIT No.%d' % seed, font=font(26, FB), fill='white', anchor='ls')
    return img

def cork_wall(W=1024, H=700):
    return cork_board(W, H)


def pocket_map(W=512, H=512):
    """Folded pocket map cover: cream card, red-blue roundel, UNDERGROUND, a mini diagram (stack sides / towers / crates)."""
    img = Image.new('RGB', (W, H), '#f4ead0'); d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W - 1, H - 1), outline='#1a1840', width=8)
    d.rectangle((0, 0, W, 90), fill='#12307a'); d.text((W / 2, 46), 'POCKET MAP', font=font(52, FB), fill='#ffffff', anchor='mm')
    cx, cy, R = W / 2, 250, 120
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline='#e3262b', width=34); d.rectangle((cx - R - 40, cy - 28, cx + R + 40, cy + 28), fill='#1f49c8'); d.text((cx, cy), 'UNDERGROUND', font=font(34, FB), fill='white', anchor='mm')
    for (x0, y0, x1, y1, col) in ((40, 420, 470, 420, RED), (110, 380, 110, 490, BLUE), (200, 490, 330, 380, GREEN), (400, 380, 400, 490, YELLOW)):
        d.line((x0, y0, x1, y1), fill=col, width=14)
    return img

# ----------------------------------------------------------------------------- build all
def ensure(verbose=False):
    tx = {}
    def add(name, img, mk=None):
        p = os.path.join(OUT, '%s_v%d.png' % (name, TEX_V))
        if not os.path.exists(p):
            if verbose: print('paint', name)
            _save(img() if callable(img) else img, name)
        tx[name] = p
    os.makedirs(OUT, exist_ok=True)
    def pair(name, fn):
        if not (os.path.exists(os.path.join(OUT, name + '_v%d.png' % TEX_V)) and os.path.exists(os.path.join(OUT, name + '_glow_v%d.png' % TEX_V))):
            a, g = fn(); _save(a, name); _save(g, name + '_glow')
        tx[name] = os.path.join(OUT, name + '_v%d.png' % TEX_V); tx[name + '_glow'] = os.path.join(OUT, name + '_glow_v%d.png' % TEX_V)
    add('roundel', lambda: roundel('UNDERGROUND', 1024)); add('roundel_piccadilly', lambda: roundel('PICCADILLY CIRCUS', 1400))
    add('sign_publicity', lambda: sign('PUBLICITY DEPT', '#12307a', '#fff1c0', border='#ffc81e', w=1024, h=220))
    add('sign_rooms', lambda: sign('ROOMS', '#3a1a10', '#ffd88a', border='#ffd88a', w=512, h=170))
    add('sign_way_out', way_out); add('sign_gap', lambda: sign('MIND THE GAP', '#ffd22a', '#1a1840', border='#1a1840', w=800, h=330)); add('sign_underground_bar', lambda: sign('UNDERGROUND', BLUE, 'white', w=1024, h=200, radius=.04))
    add('sign_tickets', lambda: sign('TICKETS', '#12307a', 'white', border='#ffc81e', w=640, h=200)); add('sign_news', lambda: sign('NEWS', RED, CREAM, border=CREAM, w=512, h=180)); add('sign_flowers', lambda: sign('FLOWERS', '#12724a', CREAM, border=CREAM, w=640, h=180))
    add('diagram', diagram); add('old_map', old_map); add('old_map_small', lambda: old_map(700, 520))
    pair('hq', hq_facade); pair('lodging', lodging_facade)
    pair('fac_a', lambda: facade('a', 896, 760, 7, 5, '#cbbd9a', 0.34, 21, trim='#e8dcb8', door=False)); pair('fac_b', lambda: facade('b', 896, 760, 7, 5, '#8a3a2a', 0.34, 33, trim='#d8c8a0', door=False)); pair('fac_c', lambda: facade('c', 896, 760, 7, 5, '#6a2c28', 0.34, 44, trim='#cbbd9a'))
    add('sky', dusk_sky); add('sky_night', night_sky); add('farground_dark', farground_dark); add('skyline', skyline); add('skyline2', lambda: skyline(2048, 512, 9)); add('river', river)
    add('farground', farground); add('halo_warm', lambda: halo((1.0, 0.62, 0.22))); add('halo_cool', lambda: halo((0.3, 0.5, 1.0))); add('halo_white', lambda: halo((1.0, 0.9, 0.7))); add('halo_green', lambda: halo((0.35, 1.0, 0.5)))
    add('beam_warm', lambda: beam_glow((1.0, 0.8, 0.45)))
    pair('bus', bus_side); pair('cab', cab_side); pair('grate', grate); add('road', road); add('pave', pavement); add('slate', slate); add('slate2', lambda: slate(base='#4a3a7a'))
    add('brick', lambda: plain_brick('b', '#b8532e', 1)); add('brick2', lambda: plain_brick('b', '#c98a58', 2))
    for i in range(10): add('crowd_w%d' % i, lambda i=i: crowd_card(i, (255, 160, 70), 'r' if i % 2 else 'l'))
    for i in range(10): add('crowd_c%d' % i, lambda i=i: crowd_card(i, (110, 170, 255), 'r' if i % 2 else 'l'))
    for i in range(10): add('crowd_t%d' % i, lambda i=i: crowd_card(i, (255, 190, 110), 'l' if i % 2 else 'r'))
    for i in range(6): add('crowd_d%d' % i, lambda i=i: crowd_card(i, (255, 170, 90), 'r', dark=0.3))
    add('cork', cork_board); add('wallpaper', wallpaper); add('wallpaper_b', lambda: wallpaper(base='#d8903c', motif='#b03030', alt='#2a5a8a'))
    add('wood', wood); add('wood_dark', lambda: wood(base=(0.36, 0.18, 0.09)))
    add('note', lambda: paper_note('')); add('night_city', night_city)
    for i in range(6): add('poster%d' % i, lambda i=i: poster(i))
    add('tiles', station_wall('t')); add('tiles_plain', lambda: station_wall('tp', band=None)); add('tiles_cool', lambda: station_wall('tc', base='#9aa6dc')); add('tiles_cool_plain', lambda: station_wall('tcp', base='#6a78c0', band=None)); add('blob', blob); add('quilt', quilt); pair('train_side', train_side); add('tiles_green', lambda: station_wall('tg', band='#14733f'))
    add('crate_maps', lambda: sign('MAPS', '#8a4a22', '#ffe0a0', border='#ffe0a0', w=600, h=360, radius=0.04, sub='REPRINT')); add('sign_dept_door', lambda: sign('PUBLICITY', '#12307a', '#fff1c0', border='#ffc81e', w=700, h=200)); add('sign_signals', lambda: sign('SIGNALS', '#12724a', '#fff1c0', border='#fff1c0', w=700, h=200)); add('sign_drawing', lambda: sign('DRAWING OFFICE', '#7a1a22', '#fff1c0', border='#fff1c0', w=900, h=200)); add('sign_notices', lambda: sign('NOTICES', '#1a1840', '#ffd88a', border='#ffd88a', w=640, h=200)); add('sign_stairs', lambda: sign('STAIRS', '#3a2a6a', '#fff1c0', border='#fff1c0', w=520, h=180))
    add('pocket_map', pocket_map); add('paper_grid', paper_grid); add('rag_rug', rag_rug)
    for i in range(3): add('circuit%d' % i, lambda i=i: circuit_sheet(seed=i + 1))
    add('clock', clock_face); pair('train_front', train_front); add('floor_pf', floor_platform); add('ballast', ballast)
    return tx

if __name__ == '__main__':
    t = ensure(True); print(len(t), 'textures')
