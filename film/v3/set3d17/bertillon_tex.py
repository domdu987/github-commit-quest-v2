"""film 17 textures (numpy + PIL, no bpy). Drawn flat-colour artwork in the style of the approved sets: plank seams #432219, flat tonal
planks (texture std 7-8 grey levels), drawn panels and ashlar courses, a Bertillon card with no readable text. Every feature is >= 3 texels
wide and the tiles are 512 px, so a texel is never much finer than a screen pixel (Cycles has no mip-mapping: fine grain would shimmer).
Cached in tex/<name>_v<TEX_V>.png (git-ignored, rebuilt on demand, about 3 MB)."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__)); TEX = os.path.join(HERE, 'tex'); os.makedirs(TEX, exist_ok=True)
TEX_V = 3
SEAM = (0x43, 0x22, 0x19)
def _p(name): return os.path.join(TEX, '%s_v%d.png' % (name, TEX_V))
def _hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def _blotch(S, seed, scale=64, amp=1.0):
    """smooth low-frequency noise in [-1, 1] (a few big soft blotches; sampled by bilinear upsampling)."""
    r = np.random.RandomState(seed); g = r.randn(S // scale + 2, S // scale + 2)
    im = Image.fromarray(g.astype(np.float32), mode='F').resize((S, S), Image.BICUBIC); a = np.asarray(im)
    return np.clip(a / (abs(a).max() + 1e-9), -1, 1) * amp
def _fin(arr, name):
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(_p(name)); return _p(name)
def _std(arr, target, seed, scale=48):
    """add the blotch field so the grey-level std of the texture is about `target`."""
    b = _blotch(arr.shape[0], seed, scale); return arr + (b * target * 1.6)[..., None]

def planks(name, base, n=5, seed=1, std=7.5, S=512, joints=1, seam_w=5, knots=2, grain=5):
    """floor / board texture: n boards across the tile (vertical seams lines run along v), flat tone per board, drawn grain strokes."""
    p = _p(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('RGB', (S, S), base); d = ImageDraw.Draw(im); pw = S / n
    for i in range(n):
        t = r.uniform(0.90, 1.10); col = tuple(int(c * t) for c in base); d.rectangle([i * pw, 0, (i + 1) * pw, S], fill=col)
        dark = tuple(int(c * 0.82) for c in col)
        for _ in range(grain):                                              # drawn grain strokes: long thin wobbly lines
            x = i * pw + r.uniform(0.15, 0.85) * pw; y0 = r.uniform(0, S); L = r.uniform(S * 0.25, S * 0.8); pts = []
            for k in range(8): pts.append((x + math.sin(k * 0.9 + r.random()) * 2.0, y0 + L * k / 7))
            d.line(pts, fill=dark, width=3)
        for _ in range(joints):                                             # butt joints
            y = r.uniform(0.1, 0.9) * S; d.rectangle([i * pw + 3, y, (i + 1) * pw - 3, y + seam_w - 1], fill=SEAM)
        for _ in range(knots):
            kx = i * pw + r.uniform(0.3, 0.7) * pw; ky = r.uniform(0, S); d.ellipse([kx - 7, ky - 11, kx + 7, ky + 11], outline=dark, width=3)
    for i in range(n): d.rectangle([i * pw - seam_w // 2, 0, i * pw + seam_w // 2, S], fill=SEAM)
    a = _std(np.asarray(im, dtype=float), std, seed + 3, 64); return _fin(a, name)

def wain_panels(name, base, S=512, seed=2, std=6):
    """wainscot: 2 tall raised panels per tile across, rails top / bottom; light top-left edges, dark bottom-right (drawn bevel)."""
    p = _p(name)
    if os.path.exists(p): return p
    im = Image.new('RGB', (S, S), base); d = ImageDraw.Draw(im); lo = tuple(int(c * 0.55) for c in base); hi = tuple(min(255, int(c * 1.45) + 8) for c in base)
    mid = tuple(int(c * 1.08) for c in base)
    for i in range(2):
        x0 = i * S / 2 + 40; x1 = (i + 1) * S / 2 - 40; y0, y1 = 70, S - 70
        d.rectangle([x0 - 8, y0 - 8, x1 + 8, y1 + 8], fill=lo)                  # groove
        d.rectangle([x0, y0, x1, y1], fill=mid)
        d.polygon([(x0, y0), (x1, y0), (x1 - 12, y0 + 12), (x0 + 12, y0 + 12), (x0 + 12, y1 - 12), (x0, y1)], fill=hi)
        d.polygon([(x1, y1), (x0, y1), (x0 + 12, y1 - 12), (x1 - 12, y1 - 12), (x1 - 12, y0 + 12), (x1, y0)], fill=lo)
        d.rectangle([x0 + 12, y0 + 12, x1 - 12, y1 - 12], fill=mid)
    d.rectangle([0, 0, S, 14], fill=hi); d.rectangle([0, S - 14, S, S], fill=lo)
    a = _std(np.asarray(im, dtype=float), std, seed, 64); return _fin(a, name)

def plaster(name, base, seed=3, S=512, std=6.5):
    """painted wall: flat colour + a few soft blotches (the only variation)."""
    p = _p(name)
    if os.path.exists(p): return p
    a = np.ones((S, S, 3)) * np.array(base, float); b = _blotch(S, seed, 96)[..., None] * (std * 1.8); b2 = _blotch(S, seed + 1, 32)[..., None] * (std * 0.7)
    return _fin(a + b + b2, name)

def boards(name, base, S=512, seed=5, n=4, std=7.5):
    """vertical boarding (cabinet carcass, doors, crates): flat boards, seams, 2 grain strokes each."""
    return planks(name, base, n=n, seed=seed, std=std, S=S, joints=0, knots=1, grain=3)

def ashlar(name, base, S=512, seed=6, std=6.5, courses=4, seam=(0x5a, 0x3a, 0x28)):
    """cut-stone facade: courses of blocks with drawn joints, per-block tone (std ~7), tile = 2 m x 2 m (0.5 m courses)."""
    p = _p(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('RGB', (S, S), base); d = ImageDraw.Draw(im); ch = S / courses
    for c in range(courses):
        nb = 2 if c % 2 == 0 else 3; off = 0 if c % 2 == 0 else r.uniform(0, 1) * S / nb
        w = S / nb
        for k in range(nb + 1):
            x0 = off + k * w - w; t = r.uniform(0.93, 1.07); col = tuple(int(v * t) for v in base); d.rectangle([x0, c * ch, x0 + w, (c + 1) * ch], fill=col)
            d.rectangle([x0 - 2, c * ch, x0 + 2, (c + 1) * ch], fill=seam)
        d.rectangle([0, c * ch - 2, S, c * ch + 2], fill=seam)
    a = _std(np.asarray(im, dtype=float), std * 0.6, seed + 2, 96); return _fin(a, name)

def cobbles(name, base, S=512, seed=7, n=9, std=6.0):
    """pave setts: offset rows of rounded blocks, dark joints (>= 4 texels), per-stone tone. tile = 4 m (0.44 m setts)."""
    p = _p(name)
    if os.path.exists(p): return p
    r = random.Random(seed); im = Image.new('RGB', (S, S), tuple(int(c * 0.55) for c in base)); d = ImageDraw.Draw(im); h = S / n
    for row in range(n):
        off = (row % 2) * (S / n) * 0.5; w = S / n * 1.0
        for k in range(n + 1):
            x0 = off + k * w - w * 0.5; t = r.uniform(0.84, 1.12); col = tuple(int(c * t) for c in base)
            d.rounded_rectangle([x0 + 3, row * h + 3, x0 + w - 3, row * h + h - 3], radius=10, fill=col)
    a = _std(np.asarray(im, dtype=float), std * 0.5, seed + 1, 96); return _fin(a, name)

def zinc(name, base, S=512, seed=8, std=5):
    """mansard zinc / slate roof: standing seams every 1/8 tile, flat tone."""
    p = _p(name)
    if os.path.exists(p): return p
    im = Image.new('RGB', (S, S), base); d = ImageDraw.Draw(im); lo = tuple(int(c * 0.72) for c in base)
    for i in range(8): d.rectangle([i * S / 8 - 2, 0, i * S / 8 + 2, S], fill=lo)
    for j in range(4):
        for i in range(8): d.rectangle([i * S / 8, j * S / 4 - 2 + (i % 2) * S / 8, (i + 1) * S / 8, j * S / 4 + 1 + (i % 2) * S / 8], fill=lo) if False else None
    a = _std(np.asarray(im, dtype=float), std, seed, 96); return _fin(a, name)

def runner(name, S=512, seed=9):
    """navy runner with a red border and a gold lozenge row; u across (0..1 = full width 1.0 tile), v along."""
    p = _p(name)
    if os.path.exists(p): return p
    navy = _hexrgb('#2f3f66'); red = _hexrgb('#7a3036'); gold = _hexrgb('#c89a4a'); im = Image.new('RGB', (S, S), navy); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 52, S], fill=red); d.rectangle([S - 53, 0, S, S], fill=red)
    d.rectangle([60, 0, 66, S], fill=gold); d.rectangle([S - 67, 0, S - 61, S], fill=gold)
    for k in range(2):                                                    # two lozenge medallions per tile
        cy = S * (0.25 + 0.5 * k); cx = S / 2
        d.polygon([(cx, cy - 120), (cx + 80, cy), (cx, cy + 120), (cx - 80, cy)], outline=gold, width=7)
        d.polygon([(cx, cy - 56), (cx + 38, cy), (cx, cy + 56), (cx - 38, cy)], fill=red)
    a = _std(np.asarray(im, dtype=float), 4, seed, 64); return _fin(a, name)

def frieze(name, S=512, seed=10, bg='#5a1c18', fg='#c8903c'):
    """wall frieze strip: gold lozenges and dots on dark red (tile 1.0 m wide, strip 0.3 m high uses the top 0.3 of v)."""
    p = _p(name)
    if os.path.exists(p): return p
    im = Image.new('RGB', (S, S), _hexrgb(bg)); d = ImageDraw.Draw(im); f = _hexrgb(fg)
    for k in range(4):
        cx = S * (k + 0.5) / 4; cy = S / 2
        d.polygon([(cx, cy - 90), (cx + 60, cy), (cx, cy + 90), (cx - 60, cy)], outline=f, width=9); d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=f)
    d.rectangle([0, 18, S, 32], fill=f); d.rectangle([0, S - 32, S, S - 18], fill=f)
    return _fin(np.asarray(im, dtype=float), name)

def _squig(d, x0, y0, x1, y1, rng, w=4, col=(70, 55, 70)):
    x = x0; pts = []
    while x < x1:
        pts.append((x, (y0 + y1) / 2 + rng.uniform(-1, 1) * (y1 - y0) * 0.42)); x += rng.uniform(7, 15)
    if len(pts) > 1: d.line(pts, fill=col, width=w, joint='curve')
def _face(d, cx, cy, r, profile, ink=(58, 40, 50), fill=(254, 247, 246), w=5):
    """flat-style drawn head: near-white fill, plum ink, dot eyes, a hair cap."""
    if not profile:
        d.ellipse([cx - r, cy - r * 1.15, cx + r, cy + r * 1.15], fill=fill, outline=ink, width=w)
        d.pieslice([cx - r, cy - r * 1.15, cx + r, cy + r * 1.1], 180, 360, fill=ink)
        d.ellipse([cx - r * 0.42, cy - r * 0.12, cx - r * 0.2, cy + r * 0.1], fill=ink); d.ellipse([cx + r * 0.2, cy - r * 0.12, cx + r * 0.42, cy + r * 0.1], fill=ink)
        d.line([(cx, cy + r * 0.05), (cx - r * 0.06, cy + r * 0.38), (cx + r * 0.1, cy + r * 0.4)], fill=ink, width=w - 1); d.arc([cx - r * 0.3, cy + r * 0.5, cx + r * 0.3, cy + r * 0.8], 20, 160, fill=ink, width=w - 1)
        d.ellipse([cx - r * 1.12, cy - r * 0.1, cx - r * 0.92, cy + r * 0.35], fill=fill, outline=ink, width=w - 1); d.ellipse([cx + r * 0.92, cy - r * 0.1, cx + r * 1.12, cy + r * 0.35], fill=fill, outline=ink, width=w - 1)
    else:
        d.ellipse([cx - r * 1.05, cy - r * 1.15, cx + r * 0.95, cy + r * 1.1], fill=fill, outline=ink, width=w)
        d.polygon([(cx + r * 0.85, cy - r * 0.1), (cx + r * 1.3, cy + r * 0.25), (cx + r * 0.9, cy + r * 0.32)], fill=fill, outline=ink)
        d.pieslice([cx - r * 1.05, cy - r * 1.15, cx + r * 0.95, cy + r * 1.1], 150, 330, fill=ink)
        d.ellipse([cx + r * 0.38, cy - r * 0.12, cx + r * 0.56, cy + r * 0.08], fill=ink); d.ellipse([cx - r * 0.35, cy - r * 0.05, cx - r * 0.05, cy + r * 0.35], outline=ink, width=w - 1)
def card(name='card', kind='bertillon', seed=7, W=768, H=512):
    """kind bertillon: two portrait frames (front + profile), a ruled grid of measurement rows with squiggle digits, an ear sketch
    and a hand outline. NO readable text. kind notice: portrait wanted-bill with a framed face and greeked lines."""
    p = _p(name)
    if os.path.exists(p): return p
    rng = random.Random(seed); INK = (150, 70, 66); PL = (58, 40, 50)
    if kind == 'bertillon':
        im = Image.new('RGB', (W, H), (243, 231, 200)); d = ImageDraw.Draw(im)
        d.rectangle([8, 8, W - 8, H - 8], outline=INK, width=7); d.rectangle([22, 22, W - 22, 66], fill=(228, 200, 168)); _squig(d, 40, 28, 400, 60, rng, 6, PL)
        for k, (x0, prof) in enumerate(((34, False), (250, True))):
            d.rectangle([x0, 80, x0 + 190, 290], fill=(112, 124, 160), outline=INK, width=6); _face(d, x0 + 95, 190, 58, prof)
            d.rectangle([x0 + 40, 258, x0 + 150, 284], fill=(243, 231, 200), outline=PL, width=3)
        d.ellipse([470, 86, 600, 216], outline=PL, width=6); d.arc([490, 106, 580, 196], 30, 300, fill=PL, width=6); d.arc([508, 126, 562, 176], 60, 280, fill=PL, width=5)   # ear sketch
        d.polygon([(630, 220), (640, 120), (656, 120), (660, 190), (676, 100), (692, 104), (686, 200), (706, 130), (722, 136), (708, 230), (736, 190), (746, 204), (714, 270), (650, 276)], outline=PL, fill=(236, 214, 184), width=4)  # hand
        y = 310
        for i in range(6):
            d.line([(24, y), (W - 24, y)], fill=INK, width=4)
            for cx in (24, 170, 316, 462, 608, W - 24): d.line([(cx, y), (cx, y + 30)], fill=INK, width=4)
            for cx in (36, 182, 328, 474, 620):
                if rng.random() < 0.9: _squig(d, cx, y + 6, cx + rng.randint(50, 110), y + 26, rng, 5, PL)
            y += 30
        d.line([(24, y), (W - 24, y)], fill=INK, width=4); d.line([(24, 300), (W - 24, 300)], fill=INK, width=7)
    else:
        W, H = 512, 700; im = Image.new('RGB', (W, H), (232, 214, 172)); d = ImageDraw.Draw(im)
        d.rectangle([14, 14, W - 14, H - 14], outline=(100, 60, 56), width=8); _squig(d, 50, 40, 460, 110, rng, 14, PL)
        d.rectangle([140, 140, 372, 380], fill=(112, 124, 160), outline=INK, width=6); _face(d, 256, 262, 70, False)
        for i in range(9): _squig(d, 50, 410 + i * 28, rng.randint(300, 462), 432 + i * 28, rng, 7, PL)
    im.save(p); return p

def frame_art(name='portrait', seed=11):
    """framed portrait / photograph plate for the walls (drawn face, matte, no text)."""
    p = _p(name)
    if os.path.exists(p): return p
    S = 256; im = Image.new('RGB', (S, S), (230, 214, 178)); d = ImageDraw.Draw(im); d.rectangle([30, 24, S - 30, S - 24], fill=(112, 124, 160)); _face(d, S // 2, 128, 44, seed % 2 == 0, w=4)
    im.save(p); return p

def sunset(name, top, mid, bot, S=256):
    """vertical gradient strip for skies (used by the street / window cards through emission)."""
    p = _p(name)
    if os.path.exists(p): return p
    t = np.linspace(0, 1, S)[:, None, None]; a = np.array(top, float); m = np.array(mid, float); b = np.array(bot, float)
    g = np.where(t < 0.5, a + (m - a) * (t / 0.5), m + (b - m) * ((t - 0.5) / 0.5)); g = np.repeat(g, 8, axis=1)
    return _fin(g, name)
