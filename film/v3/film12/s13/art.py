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

def _poly_finger(d, P, ph, ln, w0, tone, u, W, base_y, alpha=222):
    th = min(1.0, ph); tt = max(0.0, min(1.0, ph - ln))
    if th <= 0.01 or tt >= 1.0: return None
    n = 12; pts = [_path(P, tt + (th - tt) * i / n) for i in range(n + 1)]
    L, Rr = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[min(i + 1, n)]; b = pts[max(i - 1, 0)]; dx, dy = a[0] - b[0], a[1] - b[1]; m = math.hypot(dx, dy) or 1.0; nx, ny = -dy / m, dx / m
        w = w0 * (1 - i / n) ** 0.9 * 0.5; L.append((x + nx * w, y + ny * w)); Rr.append((x - nx * w, y - ny * w))
    px = lambda q: (W / 2 + q[0] * u, base_y - q[1] * u)
    poly = [px(q) for q in L + Rr[::-1]]; d.polygon(poly, fill=tone + (alpha,))
    d.line([px(q) for q in L[:-1]], fill=RIM + (235,), width=max(3, int(0.11 * u)))              # warm rim on the leading edge
    x, y = pts[-1]; ex, ey = pts[-1][0] - pts[-3][0], pts[-1][1] - pts[-3][1]; m = math.hypot(ex, ey) or 1.0
    return pts[-1], (ex / m, ey / m)

def _drop(d, tip, dirv, u, W, base_y, tone, size=0.9):
    """teardrop pointed AWAY from its finger (no round bulb): narrow tail toward the finger, widest 70 % along."""
    x, y = tip; dx, dy = dirv; nx, ny = -dy, dx; l = size; w = size * 0.2
    pts = [(x + dx * 0.05, y + dy * 0.05), (x + dx * l * 0.55 + nx * w, y + dy * l * 0.55 + ny * w), (x + dx * l * 0.85 + nx * w * 0.7, y + dy * l * 0.85 + ny * w * 0.7), (x + dx * l, y + dy * l),
           (x + dx * l * 0.85 - nx * w * 0.7, y + dy * l * 0.85 - ny * w * 0.7), (x + dx * l * 0.55 - nx * w, y + dy * l * 0.55 - ny * w)]
    d.polygon([(W / 2 + p[0] * u, base_y - p[1] * u) for p in pts], fill=tone + (226,))

def crown(rel):
    W, H = int(W_U * PPD) * SS, int(H_U * PPD) * SS; im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    if rel <= 0 or rel > 31: return im.resize((W // SS, H // SS), Image.LANCZOS)
    d = ImageDraw.Draw(im); u = PPD * SS; base_y = H - 0.3 * u; n = 11
    fingers = []
    for i in range(n):
        r = random.Random(900 + i); r2 = random.Random(1900 + i)
        fingers.append(((BASE_DX + r.uniform(-0.5, 0.5), 3.6 + 3.6 * r.random(), 1.4 + 4.6 * r2.random(), -1 if i % 7 else 1), 0.26 * (i / n) * r2.random() + 0.02 * i / n, i))
    for P, dl, i in sorted(fingers, key=lambda f: -f[0][1]):
        ph = rel / 22.0 - dl; tone = TONES[i % 3]
        res = _poly_finger(d, P, ph, 0.46, 1.15, tone, u, W, base_y)
        if res and ph > 0.25 and ph < 1.0: _drop(d, res[0], res[1], u, W, base_y, tone)
    for j in range(26):                                      # streak droplets
        r = random.Random(500 + j); P = (BASE_DX + r.uniform(-0.8, 0.8), 2.0 + 5.5 * r.random(), 0.5 + 6.0 * r.random(), -1 if j % 5 else 1)
        ph = rel / 20.0 - r.uniform(0, 0.3); res = _poly_finger(d, P, ph, 0.09, 0.26, TONES[j % 3], u, W, base_y, alpha=235)
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
