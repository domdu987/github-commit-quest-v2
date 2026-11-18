"""splash.py -- painted mud-splash sprites (spray crown with pointed fins, bulb tips, droplets) for s10 shot 12.  PNGs cached in work/."""
import os, math, random
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); WORK = os.path.join(HERE, 'work')
PPD, W_U, H_U = 200, 8.0, 5.6                   # px per unit, card size in units (card origin = bottom centre)
INK, MUD, LIGHT, DARK = (36, 22, 14, 255), (92, 60, 40, 255), (134, 98, 64, 255), (58, 36, 24, 255)
SS = 2

def _fin(d, base, ang, L, w0, bend, bulb):
    """pointed curved fin from base (px) leaning `ang` rad from vertical, length L, base width w0; returns tip."""
    pts_l, pts_r, n = [], [], 14
    dx, dy = math.sin(ang), -math.cos(ang); nx, ny = -dy, dx
    for i in range(n + 1):
        s = i / n; off = bend * L * s * s
        cx, cy = base[0] + dx * L * s + nx * off, base[1] + dy * L * s + ny * off
        w = w0 * (1 - s) ** 0.75 * 0.5
        pts_l.append((cx + nx * w, cy + ny * w)); pts_r.append((cx - nx * w, cy - ny * w))
    poly = pts_l + pts_r[::-1]
    d.polygon(poly, fill=MUD, outline=INK)
    d.line(poly + [poly[0]], fill=INK, width=5)
    # highlight stripe on the light (left) side, shade stripe on the right
    d.polygon([((pts_l[i][0] * 0.55 + pts_r[i][0] * 0.45), (pts_l[i][1] * 0.55 + pts_r[i][1] * 0.45)) for i in range(1, n - 4)] + [((pts_l[i][0] * 0.8 + pts_r[i][0] * 0.2), (pts_l[i][1] * 0.8 + pts_r[i][1] * 0.2)) for i in range(n - 4, 0, -1)], fill=LIGHT)
    tip = (pts_l[n][0], pts_l[n][1])
    if bulb > 0:
        r = bulb; bx, by = tip[0] + dx * r * 0.9, tip[1] + dy * r * 0.9
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=MUD, outline=INK, width=5); d.ellipse([bx - r * .55, by - r * .6, bx - r * .1, by - r * .15], fill=LIGHT)
    return tip

def _drop(d, x, y, r, dxy):
    """teardrop pointing along its motion (dxy) with a light highlight."""
    m = math.hypot(*dxy) or 1.0; ux, uy = dxy[0] / m, dxy[1] / m
    tipx, tipy = x + ux * r * 2.0, y + uy * r * 2.0
    d.polygon([(x - uy * r, y + ux * r), (tipx, tipy), (x + uy * r, y - ux * r)], fill=MUD)
    d.ellipse([x - r, y - r, x + r, y + r], fill=MUD, outline=INK, width=4); d.ellipse([x - r * .55, y - r * .65, x - r * .05, y - r * .15], fill=LIGHT)

def frame(t, kind='crown', seed=5):
    """t 0..1 (rise at 0..0.35, collapse by 1).  kind 'crown' (behind the hero) or 'drops' (in front)."""
    W, H = int(W_U * PPD) * SS, int(H_U * PPD) * SS; im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    u = PPD * SS; base_y = H - 0.25 * u; cx = W / 2; rnd = random.Random(seed)
    peak = math.sin(math.pi * min(1.0, t / 0.95)) ** 0.6 if t > 0 else 0.0
    if t <= 0 or t >= 1.0: return im.resize((W // SS, H // SS), Image.LANCZOS)
    if kind == 'crown':
        Hs = 3.0 * u * peak; Rb = 2.3 * u * (0.35 + 0.65 * min(1, t / 0.5)); n = 9
        # churning base: a flat mud-water ellipse
        d.ellipse([cx - Rb * 1.15, base_y - 0.32 * u * peak, cx + Rb * 1.15, base_y + 0.2 * u], fill=DARK, outline=INK, width=5)
        d.ellipse([cx - Rb * 0.9, base_y - 0.22 * u * peak, cx + Rb * 0.9, base_y + 0.12 * u], fill=MUD)
        order = sorted(range(n), key=lambda i: abs(i - n / 2), reverse=True)
        for i in order:
            r = random.Random(seed * 100 + i); a = (-1.2 + 2.4 * i / (n - 1)) + r.uniform(-0.08, 0.08)
            L = Hs * (0.45 + 0.55 * r.random()) * (1.0 - 0.35 * abs(a) / 1.15); bx = cx + math.sin(a) * Rb * 0.95; by = base_y - 0.1 * u + math.cos(a) * 0.06 * u
            _fin(d, (bx, by), a * 0.7, L, 1.0 * u * (0.75 + 0.4 * r.random()), -0.35 * (1 if a > 0 else -1), 0.13 * u if t > 0.12 else 0)
    else:
        n = 30
        for i in range(n):
            r = random.Random(seed * 1000 + i); a = r.uniform(-1.3, 1.3); sp = r.uniform(4.0, 8.0) * u; tl = t * 1.15 - r.uniform(0, 0.12)
            if tl <= 0: continue
            vx, vy = math.sin(a) * sp * 0.75, -math.cos(a) * sp * 1.05; g = 9.0 * u
            x, y = cx + vx * tl * 0.55, base_y - 0.2 * u + (vy * tl + 0.5 * g * tl * tl) * 0.55
            if y > base_y + 0.3 * u: continue
            _drop(d, x, y, (0.09 + 0.1 * r.random()) * u, (vx * 0.55, vy * 0.55 + g * tl * 0.55))
    return im.resize((W // SS, H // SS), Image.LANCZOS)

def path(g_rel, kind):
    os.makedirs(WORK, exist_ok=True); p = os.path.join(WORK, 'splash_%s_%03d.png' % (kind, g_rel))
    if not os.path.exists(p): frame(g_rel / 26.0, kind).save(p)
    return p

if __name__ == '__main__':
    os.makedirs(WORK, exist_ok=True)
    for k in range(0, 27, 4):
        a = frame(k / 26.0, 'crown'); b = frame(k / 26.0, 'drops'); bg = Image.new('RGBA', a.size, (90, 100, 160, 255)); bg.alpha_composite(a); bg.alpha_composite(b); bg.convert('RGB').save(os.path.join(WORK, 'prev_%02d.jpg' % k))
