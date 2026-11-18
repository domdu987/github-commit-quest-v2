"""art.py -- painted sprites for film-12 takes s10 / s13: cabbage, cabbage leaf, egg, contact shadow, mud spray crown + ripples.  PNGs cached in work/."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'work'); os.makedirs(WORK, exist_ok=True)
INK = (36, 22, 14, 255)

def _cached(name, fn):
    p = os.path.join(WORK, name)
    if not os.path.exists(p): fn().save(p)
    return p

def cabbage():
    def f():
        S = 4; N = 256 * S; im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = N / 2; r = N * 0.42
        d.ellipse([c - r, c - r, c + r, c + r], fill=(104, 176, 62, 255), outline=INK, width=8 * S // 2)
        for k, col in enumerate(((134, 204, 84, 255), (86, 150, 52, 255))):          # leaf lobes
            for a in range(0, 360, 72):
                aa = math.radians(a + 36 * k); x, y = c + math.cos(aa) * r * 0.45, c + math.sin(aa) * r * 0.45; rr = r * (0.5 - 0.08 * k)
                d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=INK, width=5 * S // 2)
        d.ellipse([c - r * 0.55, c - r * 0.55, c + r * 0.55, c + r * 0.55], fill=(150, 214, 96, 255), outline=INK, width=6 * S // 2)
        d.arc([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], 200, 290, fill=(190, 236, 140, 255), width=14 * S // 2)
        return im.resize((256, 256), Image.LANCZOS)
    return _cached('cabbage.png', f)

def leaf():
    def f():
        S = 4; W, H = 320 * S, 220 * S; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([10 * S, 20 * S, W - 10 * S, H - 20 * S], fill=(104, 176, 62, 255), outline=INK, width=8 * S // 2)
        d.ellipse([40 * S, 40 * S, W - 70 * S, H - 80 * S], fill=(140, 208, 88, 255))
        d.line([(20 * S, H / 2), (W - 30 * S, H / 2)], fill=INK, width=6 * S // 2)
        for k in range(-3, 4):
            if k: d.line([(W / 2 + k * 28 * S, H / 2), (W / 2 + k * 55 * S, H / 2 + (-1 if k % 2 else 1) * 70 * S)], fill=(60, 110, 40, 255), width=4 * S // 2)
        return im.resize((320, 220), Image.LANCZOS)
    return _cached('leaf.png', f)

def egg():
    def f():
        S = 4; W, H = 160 * S, 200 * S; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse([20 * S, 14 * S, W - 20 * S, H - 14 * S], fill=(255, 246, 222, 255), outline=INK, width=8 * S // 2)
        d.ellipse([42 * S, 34 * S, 74 * S, 80 * S], fill=(255, 255, 255, 255))
        return im.resize((160, 200), Image.LANCZOS)
    return _cached('egg.png', f)

def shadow():
    def f():
        N = 256; im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.ellipse([20, 70, N - 20, N - 70], fill=(10, 8, 30, 190))
        return im.filter(ImageFilter.GaussianBlur(14))
    return _cached('shadow.png', f)

# ------------------------------------------------------------------ mud spray crown (world units; card origin = bottom centre)
PPD, W_U, H_U, SS = 80, 18.0, 11.0, 2
BASE_DX = 1.6                              # wheel contact is this far right of the card centre
TONES = ((88, 56, 34), (64, 40, 24), (116, 78, 46)); RIM = (200, 142, 80)
def _path(P, tau):
    """ballistic arc in card units: P = (x0, H, R, sgn): horizontal reach R (left if sgn < 0) and apex height H."""
    x0, H, R, sg = P; return x0 + sg * R * tau, 4 * H * tau * (1 - tau)


def _pts(P, a, b, n=10): return [_path(P, a + (b - a) * i / n) for i in range(n + 1)]

def _ribbon(d, pts, wfun, tone, alpha, u, W, base_y, rim=None):
    n = len(pts) - 1; L, Rr = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[min(i + 1, n)]; b = pts[max(i - 1, 0)]; dx, dy = a[0] - b[0], a[1] - b[1]; m = math.hypot(dx, dy) or 1.0; nx, ny = -dy / m, dx / m
        w = wfun(i / n) * 0.5; L.append((x + nx * w, y + ny * w)); Rr.append((x - nx * w, y - ny * w))
    px = lambda q: (W / 2 + q[0] * u, base_y - q[1] * u)
    d.polygon([px(q) for q in L + Rr[::-1]], fill=tone + (int(alpha),))
    if rim: d.line([px(q) for q in L[:-1]], fill=RIM + (int(alpha * 0.8),), width=max(3, int(0.10 * u)))

def fade(rel):
    return 1.0 if rel <= 16 else max(0.0, 1.0 - (rel - 16) / 12.0)          # everything is gone by rel 28 (smooth, no one-frame vanish)

def _finger(d, P, ph, tone, u, W, base_y, rel, w0=1.1, ln=0.46):
    th = min(1.0, ph); tt = max(0.0, min(1.0, ph - ln)); A = 222 * fade(rel)
    if th <= 0.01 or tt >= 1.0 or A <= 2: return
    if ph < 0.4:                                                           # rising: one tapered finger with a pointed teardrop at the tip
        _ribbon(d, _pts(P, tt, th), lambda s: w0 * (1 - s) ** 0.9, tone, A, u, W, base_y, rim=True)
        if ph > 0.2:
            x, y = _path(P, th); x2, y2 = _path(P, max(0.0, th - 0.03)); dx, dy = x - x2, y - y2; m = math.hypot(dx, dy) or 1.0; _drop(d, (x, y), (dx / m, dy / m), u, W, base_y, tone, A)
        return
    g = min(0.85, (ph - 0.4) * 3.2); span = th - tt; k = 5                  # breaking up: separate pointed streaks that fall and fade
    for j in range(k):
        a = tt + span * j / k; b = a + span / k * (1 - g)
        if b <= a: continue
        _ribbon(d, _pts(P, a, min(1.0, b), 6), lambda s: w0 * 0.55 * math.sin(math.pi * s) ** 0.8 + 0.02, tone, A * (1.0 - 0.15 * j / k), u, W, base_y)

def _drop(d, tip, dirv, u, W, base_y, tone, A=226, size=0.85):
    x, y = tip; dx, dy = dirv; nx, ny = -dy, dx; l = size; w = size * 0.2
    pts = [(x + dx * 0.05, y + dy * 0.05), (x + dx * l * 0.55 + nx * w, y + dy * l * 0.55 + ny * w), (x + dx * l, y + dy * l), (x + dx * l * 0.55 - nx * w, y + dy * l * 0.55 - ny * w)]
    d.polygon([(W / 2 + p[0] * u, base_y - p[1] * u) for p in pts], fill=tone + (int(A),))

def crown(rel):
    W, H = int(W_U * PPD) * SS, int(H_U * PPD) * SS; im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if rel <= 0 or rel >= 28: return im.resize((W // SS, H // SS), Image.LANCZOS)
    d = ImageDraw.Draw(im); u = PPD * SS; base_y = H - 0.3 * u; n = 13
    fingers = []
    for i in range(n):
        r = random.Random(900 + i); r2 = random.Random(1900 + i)
        fingers.append(((BASE_DX + r.uniform(-0.4, 0.4), 2.2 + 2.4 * r.random(), 3.0 + 3.4 * r2.random(), -1 if i % 9 else 1), 0.24 * (i / n) * r2.random() + 0.02 * i / n, i))
    for P, dl, i in sorted(fingers, key=lambda f: -f[0][1]):
        _finger(d, P, rel / 22.0 - dl, TONES[i % 3], u, W, base_y, rel)
    for j in range(26):                                                  # streak droplets (short pointed streaks, no rim)
        r = random.Random(500 + j); P = (BASE_DX + r.uniform(-0.8, 0.8), 2.0 + 4.5 * r.random(), 0.5 + 4.0 * r.random(), -1 if j % 5 else 1)
        ph = rel / 20.0 - r.uniform(0, 0.3)
        if 0.02 < ph < 1.0 and fade(rel) > 0.02: _ribbon(d, _pts(P, max(0, ph - 0.09), ph, 4), lambda s: 0.26 * math.sin(math.pi * s) ** 0.8 + 0.02, TONES[j % 3], 235 * fade(rel), u, W, base_y)
    return im.resize((W // SS, H // SS), Image.LANCZOS)

def crown_path(rel):
    p = os.path.join(WORK, 'crown_%03d.png' % rel)
    if not os.path.exists(p): crown(rel).save(p)
    return p

RP_W = 10.0
def ripples(rel):
    """flat ground card (top view, 10 x 10 units, centre = wheel contact): wake smear + three expanding rings."""
    N = 800; im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = N / RP_W; c = N / 2
    if 0 < rel < 30:
        a = max(0.0, 1.0 - rel / 26.0)
        sm = Image.new('RGBA', (N, N), (0, 0, 0, 0)); sd = ImageDraw.Draw(sm); rr = (0.6 + 0.12 * rel) * u
        sd.ellipse([c - rr * 1.5, c - rr * 0.8, c + rr * 1.5, c + rr * 0.8], fill=(96, 62, 38, int(150 * a))); im.alpha_composite(sm.filter(ImageFilter.GaussianBlur(10)))
        for k in range(3):
            t = rel - 3 * k
            if t > 0:
                r = (0.35 + 0.28 * t) * u; al = int(220 * max(0.0, 1 - t / 22.0)); d.ellipse([c - r, c - r, c + r, c + r], outline=(214, 224, 246, al), width=max(3, int(0.09 * u)))
    return im

def ripple_path(rel):
    p = os.path.join(WORK, 'ripple_%03d.png' % rel)
    if not os.path.exists(p): ripples(rel).save(p)
    return p

if __name__ == '__main__':
    bg = Image.new('RGBA', (int(W_U * PPD), int(H_U * PPD)), (96, 108, 170, 255)); tiles = []
    for rel in (2, 4, 7, 10, 14, 20):
        t = bg.copy(); t.alpha_composite(crown(rel)); tiles.append(t.convert('RGB').resize((480, 293)))
    s = Image.new('RGB', (480 * 3, 293 * 2))
    for i, t in enumerate(tiles): s.paste(t, ((i % 3) * 480, (i // 3) * 293))
    s.save(os.path.join(WORK, 'crown_prev.jpg')); cabbage(); leaf(); egg(); shadow()


LAND_W = 6.0
def landing(rel):
    """spray landing ON Hanway (card in front of him, 6 x 6 units, bottom centre at his feet): pointed brown streaks fall onto head / coat, small splat dots where they land."""
    N = 600; im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = N / LAND_W; cx = N / 2
    for i in range(34):
        r = random.Random(77 + i); s0 = 9 + r.uniform(0, 7); x = r.uniform(-1.3, 1.3); y0 = 4.9 + r.random(); yl = r.uniform(0.3, 3.3); t = rel - s0
        if t < 0: continue
        y = y0 - 1.05 * t; tone = TONES[i % 3]
        if y > yl:
            pts = [(cx + (x - 0.04 * t) * u, N - (y + 0.5) * u), (cx + (x + 0.07) * u, N - (y + 0.05) * u), (cx + (x - 0.04 * t) * u + 0.0, N - (y - 0.1) * u), (cx + (x - 0.07) * u, N - (y + 0.05) * u)]
            d.polygon(pts, fill=tone + (235,))
        elif y > yl - 2.2 * 1.05:                                           # a splat where it landed, for a few frames
            rr = 0.13 * u; X, Y = cx + x * u, N - yl * u; d.ellipse([X - rr * 1.6, Y - rr, X + rr * 1.6, Y + rr], fill=tone + (225,))
    return im

def landing_path(rel):
    p = os.path.join(WORK, 'landing_%03d.png' % rel)
    if not os.path.exists(p): landing(rel).save(p)
    return p

NR_W = 9.0
def near_ripples(rel):
    """flat ground card in the NEAR puddle (9 x 9 units): rings + a few tiny pointed droplets landing, g788-805."""
    N = 720; im = Image.new('RGBA', (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im); u = N / NR_W; c = N / 2
    for j in range(7):
        r = random.Random(33 + j); cx, cy = c + r.uniform(-3.2, 3.2) * u, c + r.uniform(-3.0, 3.0) * u; s0 = 3 + 2 * j; t = rel - s0
        if t < 0 or t > 16: continue
        al = int(140 * (1 - t / 16.0)); rr = (0.12 + 0.2 * t) * u
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=(214, 224, 246, al), width=max(3, int(0.05 * u)))
        if t < 3:                                                              # tiny droplet landing
            q = 0.18 * u; d.polygon([(cx, cy - 0.5 * u * (1 - t / 3.0)), (cx + q * 0.4, cy), (cx - q * 0.4, cy)], fill=TONES[j % 3] + (235,))
    return im

def near_path(rel):
    p = os.path.join(WORK, 'near_%03d.png' % rel)
    if not os.path.exists(p): near_ripples(rel).save(p)
    return p
