#!/usr/bin/env python3
"""bakery_tex.py : artwork of the film-6 set (a medieval English market town, 1260s: Henry's bakery and the market square),
drawn as SVG in Python and rasterised by headless Chromium (PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in
v3/set3d6/tex_bakery/ by content hash. Same route as v3/set3d5/mine_tex.py: tower_tex's SVG helpers and job() registry are imported.

    import bakery_tex as BT
    paths = BT.ensure()        # {name: png path}
    BT.SIZE[name] -> (w_D, h_D) of one image / tile

Every surface is drawn in the colour it shows in neutral light; the lit material makes light and shade of it.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d4'))
import tower_tex as TT                                                     # noqa: E402
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401
import pagoda_tex as PT                                                    # noqa: E402  (pool decal reused)

TEX = os.path.join(HERE, 'tex_bakery'); WORK = os.path.join(HERE, 'bakery_work')
RASTER = TT.RASTER; SIZE = TT.SIZE; job = TT.job
INK = '#2a1a14'

def _txt(x, y, s, size, fill, font='Georgia, serif', weight=700, anchor='middle', extra=''):
    return (f'<text x="{_c(x)}" y="{_c(y)}" font-family="{font}" font-weight="{weight}" font-size="{_c(size)}" '
            f'text-anchor="{anchor}" fill="{fill}"{extra}>{s}</text>')

# ----------------------------------------------------------------------------- interior surfaces
def stone_wall(name='stone_w', seed=11, base='#b4a088', W=4.0, H=4.0):
    """Rubble stone wall 4 x 4 D (tiles): irregular coursed stones with dark mortar, chips, a lit top edge on each stone, soot streaks."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#6e5e4c')]
    y = 0.0
    while y < H:
        h = r.uniform(0.32, 0.55); x = r.uniform(-0.4, 0)
        while x < W:
            w = r.uniform(0.45, 0.95); c = mul(r.choice((base, '#a89478', '#bca88c', '#9c8a70', '#c0ae94')), r.uniform(0.92, 1.06))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.03, y + 0.03, w - 0.06, h - 0.06, c, rx=0.08, stroke=INK, sw=0.012))
                o.append(line(xx + 0.1, y + 0.07, xx + w - 0.12, y + 0.07, mul(c, 1.15), 0.025, op=0.8))
                o.append(line(xx + 0.08, y + h - 0.07, xx + w - 0.1, y + h - 0.07, mul(c, 0.78), 0.03, op=0.7))
                if r.random() < 0.4: o.append(circ(xx + r.uniform(0.1, w - 0.1), y + r.uniform(0.1, h - 0.1), r.uniform(0.02, 0.05), mul(c, 0.72)))
            x += w
        y += h
    for _ in range(10):
        x = r.uniform(0, W); w = r.uniform(0.05, 0.2)
        for xx in _wrap(x, W, w): o.append(rect(xx, r.uniform(0, 1.5), w, r.uniform(0.6, 2.0), '#4a3e36', op=0.15, rx=0.03))
    job(name, 0, 0, W, H, 80, ''.join(o))

def plaster(name='plaster_in', base='#e6d4b2', seed=21, soot=0.3, W=4.0, H=4.0):
    """Lime plaster 4 x 4 D: mottled, hairline cracks, damp stains, a soot shadow toward the top (v 0 = top)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.2, 0.7)
        for xx in _wrap(x - rx, W, 2 * rx): o.append(ell(xx + rx, y, rx, rx * r.uniform(0.4, 0.8), mul(base, r.uniform(0.9, 1.06)), op=0.5))
    for _ in range(9):
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(5): x += r.uniform(-0.15, 0.15); y += r.uniform(0.05, 0.2); pts.append((x, y))
        o.append(pline(pts, mul(base, 0.6), 0.012))
    for _ in range(4):
        x = r.uniform(0, W); w = r.uniform(0.3, 0.8)
        for xx in _wrap(x, W, w): o.append(rect(xx, H - r.uniform(0.3, 1.0), w, 1.2, '#a89070', op=0.25, rx=0.2))
    if soot > 0:
        g = '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2c24" stop-opacity="%.2f"/><stop offset="1" stop-color="#3a2c24" stop-opacity="0"/></linearGradient>' % soot
        o.append(rect(-0.1, -0.1, W + 0.2, 1.6, 'url(#s)'))
    else: g = ''
    job(name, 0, 0, W, H, 64, ''.join(o), defs=g)

def brick(name='brick_oven', seed=31, soot=0.0, W=2.0, H=2.0):
    """Small hand-made bricks 2 x 2 D (0.33 x 0.11), warm reds and orange, pale mortar; soot darkens (oven mouth / dome)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#c8a07a')]
    cols = ['#b8502e', '#c45e34', '#a84628', '#cc6a3a', '#b25832', '#d07440', '#9e4226']
    bh = 0.125; bw = 0.34
    for k in range(int(H / bh) + 1):
        y = k * bh; off = (bw / 2) * (k % 2)
        for i in range(-1, int(W / bw) + 2):
            x = i * bw + off; c = mul(r.choice(cols), r.uniform(0.9, 1.08))
            if soot: c = mix(c, '#2e2220', soot * r.uniform(0.6, 1.0))
            o.append(rect(x + 0.012, y + 0.012, bw - 0.024, bh - 0.024, c, rx=0.012))
            o.append(line(x + 0.03, y + 0.025, x + bw - 0.04, y + 0.025, mul(c, 1.18), 0.012, op=0.7))
    job(name, 0, 0, W, H, 112, ''.join(o))

def flags(name='flags', seed=41, W=4.0, H=4.0, flour=0.6):
    """Flagstone floor 4 x 4 D: big worn slabs, dark joints, flour dust drifts and footprints, a few spilt grains."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#5e5246')]
    y = 0.0
    while y < H - 0.01:
        h = min(r.choice((0.8, 1.0, 1.2)), H - y); x = r.uniform(-0.6, 0)
        while x < W:
            w = r.uniform(0.8, 1.5); c = mul(r.choice(('#a8987e', '#9c8c74', '#b4a488', '#988a72')), r.uniform(0.94, 1.05))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.03, y + 0.03, w - 0.06, h - 0.06, c, rx=0.06, stroke=INK, sw=0.01))
                for _ in range(3): o.append(ell(xx + r.uniform(0.2, w - 0.2), y + r.uniform(0.2, h - 0.2), r.uniform(0.1, 0.3), r.uniform(0.05, 0.15), mul(c, r.uniform(0.88, 1.08)), op=0.6))
            x += w
        y += h
    for _ in range(int(30 * flour)):
        x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.12, 0.4)
        for xx in _wrap(x - rx, W, 2 * rx): o.append(ell(xx + rx, y, rx, rx * 0.5, '#f4eee0', op=r.uniform(0.25, 0.55)))
    for _ in range(int(14 * flour)):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.28)
        o.append(ell(x, y, 0.09, 0.05, '#7a6c5a', op=0.35, extra=f' transform="rotate({_c(math.degrees(a))} {_c(x)} {_c(y)})"'))
    job(name, 0, 0, W, H, 80, ''.join(o))

def timber(name='timber_b', base='#7a5232', seed=51):
    """Oak beam wrap 1 x 2 D (u round, v along): adzed faces, grain, knots, cracks, flour dust on the upper edge."""
    r = random.Random(seed); W, H = 1.0, 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(30):
        x = r.uniform(0, W); w = r.uniform(0.004, 0.018)
        for xx in _wrap(x, W, w): o.append(rect(xx, -0.1, w, H + 0.2, mul(base, r.uniform(0.62, 0.82)), op=0.8))
    for _ in range(14):
        x = r.uniform(0, W); y = r.uniform(0, H)
        o.append(ell(x, y, r.uniform(0.04, 0.1), r.uniform(0.02, 0.04), mul(base, 1.18), op=0.5))
    for _ in range(4):
        x = r.uniform(0, W); y = r.uniform(0, H)
        o.append(ell(x, y, 0.035, 0.08, mul(base, 0.5))); o.append(ell(x, y, 0.016, 0.05, mul(base, 0.35)))
    for _ in range(3):
        x = r.uniform(0, W); y = r.uniform(0, H - 0.6); o.append(line(x, y, x + r.uniform(-0.02, 0.02), y + r.uniform(0.3, 0.7), '#2a1a12', 0.012))
    job(name, 0, 0, W, H, 96, ''.join(o))

def planks(name='table', base='#a8784a', seed=61, W=2.0, H=2.0, n=5, flour=0.0, scraps=False):
    """Plank top 2 x 2 D (u across the boards): n boards with grain, nail heads, knife marks; flour dusting and dough scraps."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.6))]
    bw = W / n
    for i in range(n):
        c = mul(base, r.uniform(0.9, 1.08)); x = i * bw
        o.append(rect(x + 0.012, -0.1, bw - 0.024, H + 0.2, c))
        for _ in range(9): xx = x + r.uniform(0.03, bw - 0.03); o.append(line(xx, -0.1, xx + r.uniform(-0.03, 0.03), H + 0.1, mul(c, 0.82), 0.008, op=0.8))
        for y in (0.15, H - 0.15): o.append(circ(x + bw * 0.3, y, 0.018, '#3a3030')); o.append(circ(x + bw * 0.7, y, 0.018, '#3a3030'))
    for _ in range(int(20 * flour)):
        x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.15, 0.5)
        o.append(ell(x, y, rx, rx * r.uniform(0.4, 0.8), '#f8f2e4', op=r.uniform(0.35, 0.75)))
    for _ in range(int(60 * flour)):
        o.append(circ(r.uniform(0, W), r.uniform(0, H), r.uniform(0.01, 0.03), '#fbf6ea', op=0.8))
    if scraps:
        for _ in range(6):
            x, y = r.uniform(0.2, W - 0.2), r.uniform(0.2, H - 0.2); o.append(ell(x, y, r.uniform(0.04, 0.1), r.uniform(0.03, 0.06), '#ecd8a8', stroke='#b89a68', sw=0.008))
        for _ in range(8):
            x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(-0.6, 0.6)
            o.append(line(x, y, x + 0.25 * math.cos(a), y + 0.25 * math.sin(a), mul(base, 0.6), 0.01, op=0.6))
    job(name, 0, 0, W, H, 96, ''.join(o))

def sack(name='sack', seed=71, mark=True):
    """Flour sack wrap 2 x 1.5 D: coarse burlap weave, flour dust, a stitched seam and the miller's mark (wheat sheaf in a ring)."""
    r = random.Random(seed); W, H = 2.0, 1.5; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#d4c0a0')]
    for i in range(int(W / 0.03)):
        o.append(line(i * 0.03, -0.1, i * 0.03, H + 0.1, '#b8a282', 0.008, op=0.6))
    for j in range(int(H / 0.03)):
        o.append(line(-0.1, j * 0.03, W + 0.1, j * 0.03, '#c4ae8c', 0.008, op=0.5))
    for _ in range(14):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.1, 0.4), r.uniform(0.06, 0.2), '#f6f0e2', op=0.45))
    o.append(line(1.98, -0.1, 1.98, H + 0.1, '#8a7456', 0.02))
    if mark:
        cx, cy = 0.55, 0.75; o.append(circ(cx, cy, 0.26, 'none', stroke='#6a3a22', sw=0.035))
        for a in (-0.5, -0.25, 0, 0.25, 0.5):
            o.append(line(cx, cy + 0.17, cx + 0.2 * math.sin(a), cy - 0.14, '#6a3a22', 0.022))
            o.append(ell(cx + 0.2 * math.sin(a), cy - 0.14, 0.03, 0.06, '#6a3a22'))
        o.append(line(cx - 0.12, cy + 0.06, cx + 0.12, cy + 0.06, '#6a3a22', 0.03))
        o.append(_txt(1.45, 0.86, 'H', 0.42, '#6a3a22'))
    job(name, 0, 0, W, H, 96, ''.join(o))

def loaf(name='loaf', seed=81, base='#c47a34', top='#9a5222'):
    """Round loaf wrap 2 x 1 D (u round, v from the base (0) to the crown (1)): pale floury base, golden sides, dark crown, scoring
    slashes and cracks, flour dust on the crown."""
    r = random.Random(seed); W, H = 2.0, 1.0
    g = (f'<linearGradient id="l" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e8c890"/><stop offset="0.25" stop-color="{base}"/>'
         f'<stop offset="0.75" stop-color="{top}"/><stop offset="1" stop-color="{mul(top, 0.92)}"/></linearGradient>')
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, 'url(#l)')]
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0.0, 0.8); o.append(ell(x, y, r.uniform(0.04, 0.12), r.uniform(0.02, 0.05), mul(top, r.uniform(0.85, 1.25)), op=0.5))
    for k in range(4):                                                                        # four slashes over the crown
        x = 0.25 + k * 0.5
        o.append(path(f'M{_c(x - 0.12)},{_c(0.05)} Q{_c(x)},{_c(0.32)} {_c(x + 0.12)},{_c(0.62)}', 'none', stroke='#f0d8a0', sw=0.07))
        o.append(path(f'M{_c(x - 0.1)},{_c(0.05)} Q{_c(x + 0.02)},{_c(0.3)} {_c(x + 0.13)},{_c(0.6)}', 'none', stroke='#6a3416', sw=0.018))
    for _ in range(22): o.append(circ(r.uniform(0, W), r.uniform(0, 0.35), r.uniform(0.02, 0.07), '#fbf3e0', op=0.6))
    for _ in range(10): o.append(circ(r.uniform(0, W), r.uniform(0.5, 0.9), r.uniform(0.005, 0.012), '#3a2010'))
    job(name, 0, 0, W, H, 128, ''.join(o), defs=g)

def fire(name='fire', seed=91):
    """Oven-mouth fire 2 x 1.4 D (transparent): tongues of flame from a bed of logs, yellow-white core to orange-red tips, sparks."""
    r = random.Random(seed); W, H = 2.0, 1.4
    g = ('<linearGradient id="f" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff4c8"/><stop offset="0.35" stop-color="#ffc248"/>'
         '<stop offset="0.7" stop-color="#ff7a1e"/><stop offset="1" stop-color="#e83a10"/></linearGradient>'
         '<filter id="b"><feGaussianBlur stdDeviation="0.02"/></filter>')
    o = []
    for k in range(13):
        x = 0.1 + k * 0.15 + r.uniform(-0.05, 0.05); h = r.uniform(0.6, 1.25) * (1 - 0.5 * abs(x - 1) / 1.0); w = r.uniform(0.12, 0.22); lean = r.uniform(-0.12, 0.12)
        o.append(path(f'M{_c(x - w)},{_c(H)} C{_c(x - w)},{_c(H - h * 0.5)} {_c(x + lean - w * 0.3)},{_c(H - h * 0.7)} {_c(x + lean)},{_c(H - h)} '
                      f'C{_c(x + lean + w * 0.4)},{_c(H - h * 0.6)} {_c(x + w)},{_c(H - h * 0.45)} {_c(x + w)},{_c(H)} Z', 'url(#f)', extra=' filter="url(#b)"'))
    for k in range(8):
        x = 0.25 + k * 0.22 + r.uniform(-0.05, 0.05); h = r.uniform(0.25, 0.55); w = 0.08
        o.append(path(f'M{_c(x - w)},{_c(H)} Q{_c(x)},{_c(H - h * 1.4)} {_c(x + w)},{_c(H)} Z', '#fff8e0', op=0.9))
    for _ in range(24): o.append(circ(r.uniform(0.1, W - 0.1), r.uniform(0.05, 0.7), r.uniform(0.008, 0.02), '#ffe08a'))
    job(name, 0, 0, W, H, 128, ''.join(o), defs=g, transparent=True)

def embers(name='embers', seed=93):
    """Ember bed 2 x 1 D: glowing coals and burning log ends (emission art)."""
    r = random.Random(seed); W, H = 2.0, 1.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#5a1808')]
    for _ in range(90):
        x, y = r.uniform(0, W), r.uniform(0, H); s = r.uniform(0.04, 0.12)
        o.append(ell(x, y, s, s * 0.7, r.choice(('#ff9a2a', '#ffc04a', '#e05a14', '#ffd878', '#b83a0c')), stroke='#3a0c04', sw=0.008))
    job(name, 0, 0, W, H, 96, ''.join(o))

def steam(name='steam', seed=101):
    """Steam wisp 1 x 3 D (transparent): three soft wavy ribbons, PERIODIC in v (the material scrolls it upward and fades it at both
    ends), white with blurred edges."""
    r = random.Random(seed); W, H = 1.0, 3.0
    g = '<filter id="b" x="-50%" y="-10%" width="200%" height="120%"><feGaussianBlur stdDeviation="0.04"/></filter>'
    o = []
    for k in range(3):
        x0 = 0.3 + 0.2 * k; ph = r.uniform(0, 6.28); pts = []; cyc = r.choice((1, 2))
        for i in range(-4, 45):
            t = i / 40; y = H - t * H; x = x0 + 0.09 * math.sin(ph + 2 * math.pi * cyc * t) + 0.04 * math.sin(2 * ph + 2 * math.pi * 3 * t); pts.append((x, y))
        d = 'M' + ' L'.join(f'{_c(x)},{_c(y)}' for x, y in pts)
        o.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity="{_c(0.85 - 0.15 * k)}" stroke-width="{_c(0.12 - 0.025 * k)}" stroke-linecap="round" filter="url(#b)"/>')
    job(name, 0, 0, W, H, 96, ''.join(o), defs=g, transparent=True)

def shaft(name='shaft'):
    """Light-shaft card 1 x 4 D (transparent): soft-edged across u, fading along v (0 = the window, 1 = the floor end), dust motes."""
    r = random.Random(111); W, H = 1.0, 4.0
    g = ('<linearGradient id="u" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.2" stop-color="#fff" stop-opacity="1"/>'
         '<stop offset="0.8" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         '<linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="0.7" stop-color="#fff" stop-opacity="0.55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
         '<mask id="m"><rect x="0" y="0" width="1" height="4" fill="url(#v)"/></mask>')
    o = [f'<g mask="url(#m)">' + rect(0, 0, W, H, 'url(#u)', op=0.6)]
    for _ in range(60): o.append(circ(r.uniform(0.15, 0.85), r.uniform(0, H * 0.8), r.uniform(0.006, 0.014), '#ffffff'))
    o.append('</g>')
    job(name, 0, 0, W, H, 48, ''.join(o), defs=g, transparent=True)

def leaded(name='leaded'):
    """Leaded diamond-pane window 1 x 1 D (transparent): grey lead cames on a pale greenish glass (alpha 0.35)."""
    o = [rect(0, 0, 1, 1, '#c8dccc', op=0.35)]
    for k in range(-6, 7):
        o.append(line(k * 0.18, 0, k * 0.18 + 1, 1, '#3a3a40', 0.018)); o.append(line(k * 0.18, 1, k * 0.18 + 1, 0, '#3a3a40', 0.018))
    o.append(rect(0, 0, 1, 1, 'none', stroke='#3a3a40', sw=0.05))
    job(name, 0, 0, 1, 1, 128, ''.join(o), transparent=True)

def herbs(name='herbs', seed=121, kind='herb'):
    """Hanging bundle 1 x 1.5 D (transparent, v 0 = top: the string): herbs (green-grey sprigs), onions (a plait) or wheat."""
    r = random.Random(seed); W, H = 1.0, 1.5; o = [line(0.5, 0, 0.5, 0.25, '#6a5236', 0.02)]
    if kind == 'herb':
        o.append(rect(0.42, 0.22, 0.16, 0.08, '#8a6a40'))
        for _ in range(26):
            a = r.uniform(-0.45, 0.45); L = r.uniform(0.7, 1.15); x1 = 0.5 + L * math.sin(a); y1 = 0.28 + L * math.cos(a)
            c = r.choice(('#6a8a4a', '#7a9a5a', '#5a7a46', '#8aa06a', '#9a8a5a'))
            o.append(line(0.5, 0.28, x1, y1, mul(c, 0.7), 0.012))
            for t in (0.4, 0.6, 0.8, 1.0):
                xx = 0.5 + (x1 - 0.5) * t; yy = 0.28 + (y1 - 0.28) * t; o.append(ell(xx, yy, 0.04, 0.018, c, extra=f' transform="rotate({_c(math.degrees(-a) + r.uniform(-50, 50))} {_c(xx)} {_c(yy)})"'))
            if r.random() < 0.3: o.append(circ(x1, y1, 0.025, r.choice(('#c8a0d8', '#e8d070', '#f0f0e0'))))
    elif kind == 'onion':
        for k in range(9):
            y = 0.35 + k * 0.12; x = 0.5 + (0.12 if k % 2 else -0.12)
            o.append(path(f'M{_c(x)},{_c(y - 0.14)} C{_c(x + 0.16)},{_c(y - 0.02)} {_c(x + 0.15)},{_c(y + 0.12)} {_c(x)},{_c(y + 0.13)} C{_c(x - 0.15)},{_c(y + 0.12)} {_c(x - 0.16)},{_c(y - 0.02)} {_c(x)},{_c(y - 0.14)} Z',
                          r.choice(('#c88a3a', '#b8742e', '#d89a4a', '#a85a6a')), stroke='#5a3418', sw=0.012))
            o.append(line(x - 0.05, y, x + 0.04, y + 0.08, '#e8c080', 0.01, op=0.8))
    else:   # wheat
        o.append(rect(0.4, 0.22, 0.2, 0.06, '#b0402a'))
        for _ in range(22):
            a = r.uniform(-0.3, 0.3); L = r.uniform(0.9, 1.15); x1 = 0.5 + L * math.sin(a); y1 = 0.25 + L * math.cos(a)
            o.append(line(0.5, 0.25, x1, y1, '#c8a050', 0.012))
            o.append(ell(0.5 + (x1 - 0.5) * 0.25, 0.25 + (y1 - 0.25) * 0.15, 0.03, 0.08, '#e0b860', stroke='#9a7030', sw=0.008, extra=f' transform="rotate({_c(-math.degrees(a))} {_c(0.5 + (x1 - 0.5) * 0.25)} {_c(0.25 + (y1 - 0.25) * 0.15)})"'))
        o.append(rect(0.38, 0.5, 0.24, 0.07, '#b0402a'))
    job(name, 0, 0, W, H, 128, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- exterior: half-timbered (jettied) houses
PLASTERS = ['#ecdcb8', '#e8c88a', '#e8c0a8', '#e4e0d0', '#d8c098']
TIMBERS = ['#4a3020', '#3a2618', '#5a3a24', '#3e2c22']
def _frame(o, W, H, tc, r, style, tw=0.16):
    """Timber framing on a W x H storey (y 0 = top): sill, top plate, posts, studs and braces (style 0 close studding, 1 square panels,
    2 herringbone, 3 curved braces)."""
    o.append(rect(-0.05, -0.05, W + 0.1, tw * 1.2, tc)); o.append(rect(-0.05, H - tw * 1.2, W + 0.1, tw * 1.3, tc))
    for x in (0.0, W - tw): o.append(rect(x, 0, tw, H, tc))
    n = max(2, int(round(W / 1.5)))
    for i in range(1, n): o.append(rect(W * i / n - tw / 2, 0, tw, H, tc))
    if style == 0:
        for i in range(int(W / 0.45)): o.append(rect(i * 0.45 + 0.15, 0, tw * 0.6, H, tc))
    elif style == 1:
        o.append(rect(-0.05, H * 0.5 - tw / 2, W + 0.1, tw * 0.8, tc))
    elif style == 2:
        for i in range(n):
            x0 = W * i / n; x1 = W * (i + 1) / n
            for k in range(4):
                y = H * (k + 0.5) / 4.5
                o.append(line(x0 + 0.1, y + 0.3, (x0 + x1) / 2, y, tc, tw * 0.6)); o.append(line(x1 - 0.1, y + 0.3, (x0 + x1) / 2, y, tc, tw * 0.6))
    else:
        for i in range(n):
            x0 = W * i / n; x1 = W * (i + 1) / n
            o.append(path(f'M{_c(x0)},{_c(H)} Q{_c(x0 + 0.1)},{_c(H * 0.35)} {_c(x1)},{_c(H * 0.2)}', 'none', stroke=tc, sw=tw * 0.75))
    for i in range(14):                                                               # pegs
        o.append(circ(r.uniform(0, W), r.choice((tw * 0.6, H - tw * 0.6)), 0.025, mul(tc, 0.6)))

_WID = [0]
def _window(o, x, y, w, h, tc, shutters=None, lit=False, r=None):
    o.append(rect(x - 0.08, y - 0.08, w + 0.16, h + 0.16, tc))
    o.append(rect(x, y, w, h, '#ffc870' if lit else '#3a4058'))
    if not lit: o.append(rect(x, y, w, h * 0.45, '#5a6a8a', op=0.6))
    _WID[0] += 1; cid = 'w%d' % _WID[0]
    o.append(f'<clipPath id="{cid}"><rect x="{_c(x)}" y="{_c(y)}" width="{_c(w)}" height="{_c(h)}"/></clipPath><g clip-path="url(#{cid})">')
    for k in range(-12, 12):
        o.append(line(x + k * 0.16, y, x + k * 0.16 + h, y + h, '#2a2a30', 0.014, op=0.8)); o.append(line(x + k * 0.16, y + h, x + k * 0.16 + h, y, '#2a2a30', 0.014, op=0.8))
    o.append('</g>')
    o.append(rect(x - 0.12, y + h, w + 0.24, 0.08, mul(tc, 1.2)))
    if shutters:
        o.append(rect(x - w * 0.5 - 0.1, y, w * 0.5, h, shutters, stroke=INK, sw=0.015)); o.append(rect(x + w + 0.1, y, w * 0.5, h, shutters, stroke=INK, sw=0.015))
        for xx in (x - w * 0.25 - 0.1, x + w + 0.1 + w * 0.25): o.append(line(xx, y + 0.05, xx, y + h - 0.05, mul(shutters, 0.75), 0.02))

def facade(name, W, H, plaster_c, tc, seed, kind='upper', style=0, lit=0.0, shutters=None, shop=None):
    """One storey of a jettied house front, W x H D (y 0 = top). kind 'upper': framing + 1-2 leaded windows (+ shutters, window box);
    'ground': framing, a door, a shop opening with a shutter-board counter (shop = awning colour or None); 'gable': triangle of plaster
    with framing, a small window and a carved bargeboard edge (transparent outside the triangle)."""
    r = random.Random(seed); o = []
    def stains():
        for _ in range(int(W * H * 1.5)):
            x, y = r.uniform(0, W), r.uniform(0, H); rr = r.uniform(0.1, 0.4); o.append(ell(x, y, rr, rr * 0.7, mul(plaster_c, r.uniform(0.88, 1.04)), op=0.45))
    if kind == 'gable':
        o.append(poly([(0, H), (W / 2, 0), (W, H)], plaster_c)); stains()
        o.append(line(W / 2, 0.1, W / 2, H, tc, 0.16)); o.append(line(0.2, H - 0.1, W - 0.2, H - 0.1, tc, 0.18))
        for k in (0.33, 0.66):
            o.append(line(W / 2 - W / 2 * k, H * k, W / 2 + W / 2 * k, H * k, tc, 0.13))
        for s in (-1, 1):
            o.append(line(W / 2 + s * W * 0.12, H * 0.66, W / 2 + s * W * 0.28, H, tc, 0.12))
        _window(o, W / 2 - 0.35, H * 0.62 - 0.5, 0.7, 0.55, tc, lit=lit > 0.5, r=r)
        o.append(pline([(0, H), (W / 2, 0), (W, H)], tc, 0.2))
        job(name, 0, 0, W, H, 56, ''.join(o), transparent=True); return
    o.append(rect(-0.1, -0.1, W + 0.2, H + 0.2, plaster_c)); stains()
    _frame(o, W, H, tc, r, style)
    if kind == 'upper':
        nw = 2 if W > 4.5 else 1
        for i in range(nw):
            cx = W * (i + 0.5) / nw; ww = min(1.5, W / nw - 0.9); hh = 1.25
            _window(o, cx - ww / 2, H * 0.32, ww, hh, tc, shutters=shutters if i == 0 else None, lit=r.random() < lit, r=r)
            if r.random() < 0.6:                                                          # window box with flowers
                y = H * 0.32 + hh + 0.08; o.append(rect(cx - ww / 2 - 0.1, y, ww + 0.2, 0.22, '#6a4428', stroke=INK, sw=0.015))
                for _ in range(10): o.append(circ(cx - ww / 2 + r.uniform(0, ww), y - r.uniform(0, 0.12), 0.07, r.choice(('#d84a3a', '#f0d040', '#e888a0', '#f4f0e8', '#5a9a4a'))))
    else:
        dx = 0.35 if r.random() < 0.5 else W - 1.45
        o.append(path(f'M{_c(dx)},{_c(H)} L{_c(dx)},{_c(H - 2.2)} Q{_c(dx + 0.55)},{_c(H - 2.75)} {_c(dx + 1.1)},{_c(H - 2.2)} L{_c(dx + 1.1)},{_c(H)} Z', '#5a3a22', stroke=tc, sw=0.1))
        for k in range(1, 4): o.append(line(dx + 0.275 * k, H - 2.4, dx + 0.275 * k, H, '#3e2614', 0.02))
        for y in (H - 1.8, H - 0.6): o.append(rect(dx + 0.1, y, 0.8, 0.07, '#2a2a2a')); o.append(circ(dx + 0.85, y + 0.035, 0.04, '#1e1e1e'))
        o.append(circ(dx + 0.95, H - 1.2, 0.05, '#c8a040'))
        sx = 1.7 if dx < 1 else 0.3; sw_ = W - sx - (0.4 if dx < 1 else 1.7)
        if sw_ > 1.2:
            o.append(rect(sx, H - 2.4, sw_, 1.5, '#2a1e18', stroke=tc, sw=0.12))            # shop opening, dark inside
            o.append(rect(sx + 0.05, H - 2.35, sw_ - 0.1, 0.5, '#4a3626', op=0.8))
            for k in range(int(sw_ / 0.5)): o.append(ell(sx + 0.3 + k * 0.5, H - 1.15, 0.18, 0.1, r.choice(('#c88a40', '#a85a3a', '#7a9a4a', '#d8b060')), op=0.9))
            o.append(rect(sx - 0.1, H - 0.9, sw_ + 0.2, 0.16, mul('#8a6440', 1.0), stroke=INK, sw=0.015))   # counter board
            o.append(rect(sx, H - 0.74, sw_, 0.5, '#6a4a2e', stroke=INK, sw=0.015))
            if shop:
                for k in range(int(sw_ / 0.3) + 1): o.append(rect(sx - 0.15 + k * 0.3, H - 2.75, 0.15, 0.32, shop))
                o.append(rect(sx - 0.15, H - 2.75, sw_ + 0.3, 0.32, 'none', stroke=mul(shop, 0.6), sw=0.02))
    job(name, 0, 0, W, H, 56, ''.join(o))

def roof(name='roof_tile', seed=131, base='#a8583a', W=2.0, H=2.0):
    """Clay peg-tile roof 2 x 2 D (u along the eave, v down the slope): staggered rows of small tiles, moss, lichen."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.6))]
    th = 0.16; tw = 0.22
    for k in range(int(H / th) + 1):
        y = k * th; off = tw / 2 * (k % 2)
        for i in range(-1, int(W / tw) + 2):
            x = i * tw + off; c = mul(r.choice((base, '#b4643e', '#98502e', '#bc6c44', '#8e4a2e')), r.uniform(0.9, 1.08))
            o.append(path(f'M{_c(x + 0.01)},{_c(y)} L{_c(x + tw - 0.01)},{_c(y)} L{_c(x + tw - 0.01)},{_c(y + th * 0.8)} Q{_c(x + tw / 2)},{_c(y + th * 1.05)} {_c(x + 0.01)},{_c(y + th * 0.8)} Z', c, stroke=mul(c, 0.55), sw=0.008))
            if r.random() < 0.05: o.append(circ(x + tw / 2, y + th / 2, 0.05, '#8a9a5a', op=0.7))
    job(name, 0, 0, W, H, 96, ''.join(o))

def thatch(name='thatch', seed=141, W=2.0, H=2.0):
    """Straw thatch 2 x 2 D (v down the slope): combed straw strokes, darker weathered bands, a ridge pattern band."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#b89a5a')]
    for _ in range(900):
        x, y = r.uniform(0, W), r.uniform(-0.1, H); L = r.uniform(0.15, 0.35)
        o.append(line(x, y, x + r.uniform(-0.02, 0.02), y + L, r.choice(('#d0b470', '#a8884a', '#c4a660', '#8e7240', '#dcc480')), 0.012, op=0.85))
    for k in range(4): o.append(rect(-0.1, k * 0.5 + 0.42, W + 0.2, 0.06, '#7a6034', op=0.35))
    job(name, 0, 0, W, H, 80, ''.join(o))

def cobbles(name='cobbles', seed=151, W=4.0, H=4.0):
    """Market cobbles 4 x 4 D: rounded setts in loose rows, dirt and straw in the joints, a few puddle-dark stones."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#6a5a48')]
    y = 0.0
    while y < H:
        h = r.uniform(0.22, 0.3); x = r.uniform(-0.3, 0)
        while x < W:
            w = r.uniform(0.22, 0.38); c = mul(r.choice(('#a89c8a', '#988a78', '#b4a892', '#8e8272', '#a4947c', '#9a9488')), r.uniform(0.92, 1.06))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.02, y + 0.02, w - 0.04, h - 0.04, c, rx=0.08, stroke='#3e3226', sw=0.01))
                o.append(ell(xx + w * 0.42, y + h * 0.35, w * 0.25, h * 0.18, mul(c, 1.12), op=0.7))
            x += w
        y += h
    for _ in range(50):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, math.pi)
        o.append(line(x, y, x + 0.18 * math.cos(a), y + 0.18 * math.sin(a), '#d8bc6a', 0.012, op=0.8))
    for _ in range(12):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.3, 0.8), r.uniform(0.2, 0.4), '#5a4a38', op=0.25))
    job(name, 0, 0, W, H, 80, ''.join(o))

def awning(name, c1, c2, W=2.0, H=1.2):
    """Striped canvas awning 2 x 1.2 D (v 0 = the wall edge, 1 = the scalloped front edge; transparent below the scallops)."""
    o = []; n = 8; sw_ = W / n
    for i in range(n):
        o.append(rect(i * sw_, 0, sw_, H - 0.18, c1 if i % 2 == 0 else c2))
        o.append(path(f'M{_c(i * sw_)},{_c(H - 0.2)} L{_c((i + 1) * sw_)},{_c(H - 0.2)} Q{_c((i + 0.5) * sw_)},{_c(H + 0.02)} {_c(i * sw_)},{_c(H - 0.2)} Z', c1 if i % 2 == 0 else c2))
    o.append(rect(0, H - 0.26, W, 0.05, mul(c1, 0.7)))
    for i in range(int(W / 0.04)): o.append(line(i * 0.04, 0, i * 0.04, H - 0.2, '#000000', 0.004, op=0.06))
    job(name, 0, 0, W, H, 96, ''.join(o), transparent=True)

def sign_board(name, kind, W=1.6, H=1.2):
    """Painted hanging shop sign (both faces): a dark-green / red board with a gold border and the trade: 'bread' (round loaves and a
    wheat sheaf), 'pretzel', 'tankard', 'boot', 'fish'."""
    bg = dict(bread='#2e5a3a', pretzel='#8a2a22', tankard='#2a3a6a', boot='#5a2a4a', fish='#2a5a6a')[kind]
    o = [rect(0, 0, W, H, bg, rx=0.1), rect(0.06, 0.06, W - 0.12, H - 0.12, 'none', stroke='#e0b448', sw=0.05, rx=0.07)]
    cx, cy = W / 2, H / 2
    if kind == 'bread':
        for (x, y, s) in ((cx - 0.38, cy + 0.12, 0.26), (cx + 0.38, cy + 0.12, 0.26), (cx, cy - 0.02, 0.32)):
            o.append(ell(x, y, s, s * 0.72, '#d08a3a', stroke=INK, sw=0.03)); o.append(ell(x, y - s * 0.2, s * 0.7, s * 0.35, '#e8b060', op=0.8))
            for k in (-1, 0, 1): o.append(line(x + k * s * 0.35 - 0.06, y - s * 0.45, x + k * s * 0.35 + 0.06, y + s * 0.2, '#f6e0a8', 0.03))
        for a in (-0.6, -0.3, 0, 0.3, 0.6):
            o.append(line(cx, cy + 0.45, cx + 0.42 * math.sin(a), cy - 0.38, '#e8c050', 0.02))
            o.append(ell(cx + 0.42 * math.sin(a), cy - 0.38, 0.04, 0.09, '#f0cc60'))
    elif kind == 'pretzel':
        o.append(path(f'M{_c(cx)},{_c(cy + 0.4)} C{_c(cx - 0.7)},{_c(cy - 0.1)} {_c(cx - 0.3)},{_c(cy - 0.5)} {_c(cx)},{_c(cy)} C{_c(cx + 0.3)},{_c(cy - 0.5)} {_c(cx + 0.7)},{_c(cy - 0.1)} {_c(cx)},{_c(cy + 0.4)}',
                      'none', stroke='#c8782e', sw=0.14)); o.append(circ(cx, cy, 0.05, '#f6e8c8'))
    elif kind == 'tankard':
        o.append(rect(cx - 0.25, cy - 0.3, 0.5, 0.65, '#b8b8c0', stroke=INK, sw=0.03, rx=0.05)); o.append(path(f'M{_c(cx + 0.25)},{_c(cy - 0.15)} q0.25,0 0.25,0.2 q0,0.2 -0.25,0.2', 'none', stroke='#b8b8c0', sw=0.07))
        o.append(ell(cx, cy - 0.32, 0.27, 0.1, '#f8f0d8'))
    elif kind == 'boot':
        o.append(path(f'M{_c(cx - 0.2)},{_c(cy - 0.4)} L{_c(cx + 0.1)},{_c(cy - 0.4)} L{_c(cx + 0.1)},{_c(cy + 0.15)} L{_c(cx + 0.45)},{_c(cy + 0.25)} L{_c(cx + 0.45)},{_c(cy + 0.38)} L{_c(cx - 0.2)},{_c(cy + 0.38)} Z', '#6a3a1e', stroke=INK, sw=0.03))
    else:
        o.append(path(f'M{_c(cx - 0.5)},{_c(cy)} Q{_c(cx)},{_c(cy - 0.35)} {_c(cx + 0.35)},{_c(cy)} Q{_c(cx)},{_c(cy + 0.35)} {_c(cx - 0.5)},{_c(cy)} Z M{_c(cx + 0.35)},{_c(cy)} L{_c(cx + 0.6)},{_c(cy - 0.2)} L{_c(cx + 0.6)},{_c(cy + 0.2)} Z', '#a8c0c8', stroke=INK, sw=0.03))
    job(name, 0, 0, W, H, 128, ''.join(o))

def banner(name, kind, W=1.0, H=2.4):
    """Hanging banner (v 0 = the pole): 'king' red with three gold lions passant and a swallow-tail; 'town' blue with a gold key and
    a castle; 'guild' green with a gold wheat sheaf and crossed peels."""
    bg, fg = dict(king=('#b02a22', '#f0c040'), town=('#2a4a8a', '#f0c040'), guild=('#2e6a3a', '#f0c040'))[kind]
    o = [poly([(0, 0), (W, 0), (W, H), (W / 2, H - 0.35), (0, H)], bg), pline([(0.08, 0.1), (W - 0.08, 0.1), (W - 0.08, H - 0.12), (W / 2, H - 0.45), (0.08, H - 0.12), (0.08, 0.1)], fg, 0.04)]
    if kind == 'king':
        for k in range(3):
            y = 0.45 + k * 0.55; x = 0.2
            o.append(path(f'M{_c(x)},{_c(y + 0.2)} L{_c(x + 0.08)},{_c(y)} L{_c(x + 0.45)},{_c(y + 0.02)} L{_c(x + 0.55)},{_c(y - 0.12)} L{_c(x + 0.62)},{_c(y + 0.02)} '
                          f'L{_c(x + 0.58)},{_c(y + 0.12)} L{_c(x + 0.48)},{_c(y + 0.14)} L{_c(x + 0.5)},{_c(y + 0.3)} L{_c(x + 0.42)},{_c(y + 0.3)} L{_c(x + 0.38)},{_c(y + 0.16)} '
                          f'L{_c(x + 0.16)},{_c(y + 0.16)} L{_c(x + 0.12)},{_c(y + 0.3)} L{_c(x + 0.04)},{_c(y + 0.3)} Z', fg))
            o.append(path(f'M{_c(x + 0.08)},{_c(y + 0.02)} q-0.12,-0.1 -0.05,-0.22', 'none', stroke=fg, sw=0.03))
    elif kind == 'town':
        o.append(rect(0.25, 0.5, 0.5, 0.45, fg)); [o.append(rect(0.25 + k * 0.17, 0.4, 0.1, 0.12, fg)) for k in range(3)]; o.append(path('M0.42,0.95 l0,-0.2 q0.08,-0.1 0.16,0 l0,0.2 Z', bg))
        o.append(circ(0.5, 1.35, 0.12, 'none', stroke=fg, sw=0.05)); o.append(line(0.5, 1.47, 0.5, 1.95, fg, 0.06)); o.append(rect(0.5, 1.75, 0.15, 0.06, fg)); o.append(rect(0.5, 1.86, 0.12, 0.06, fg))
    else:
        for a in (-0.5, -0.25, 0, 0.25, 0.5):
            o.append(line(0.5, 1.4, 0.5 + 0.3 * math.sin(a), 0.6, fg, 0.03)); o.append(ell(0.5 + 0.3 * math.sin(a), 0.6, 0.05, 0.12, fg))
        o.append(rect(0.36, 1.0, 0.28, 0.07, '#b03a2a'))
        o.append(line(0.2, 1.9, 0.8, 1.45, fg, 0.05)); o.append(line(0.8, 1.9, 0.2, 1.45, fg, 0.05))
    for k in range(int(W / 0.08)): o.append(line(0.04 + k * 0.08, 0, 0.04 + k * 0.08, 0.06, fg, 0.03))
    job(name, 0, 0, W, H, 96, ''.join(o), transparent=True)

def notice(name='notice'):
    """Parchment proclamation 1 x 1.3 D nailed to a post: ASSIZE OF BREAD, the royal seal, lines of script."""
    r = random.Random(161); W, H = 1.0, 1.3
    o = [path('M0.03,0.05 L0.97,0.02 L0.96,1.25 L0.04,1.28 Z', '#ecdcb0', stroke='#8a6a3a', sw=0.015)]
    o.append(_txt(0.5, 0.17, 'ASSIZE', 0.11, '#5a1a10')); o.append(_txt(0.5, 0.3, 'of BREAD', 0.09, '#5a1a10'))
    for k in range(9):
        y = 0.42 + k * 0.075; o.append(line(0.12, y, 0.12 + r.uniform(0.6, 0.76), y, '#4a3a2a', 0.018, op=0.75))
    o.append(circ(0.72, 1.12, 0.08, '#b02a22')); o.append(circ(0.72, 1.12, 0.05, '#8a1a14'))
    for (x, y) in ((0.08, 0.08), (0.92, 0.08)): o.append(circ(x, y, 0.025, '#3a3030'))
    job(name, 0, 0, W, H, 160, ''.join(o), transparent=True)

def fascia(name='fascia', W=5.4, H=0.9):
    """Painted fascia board over the shop opening, W x H D: dark green with a gold rope border, the baker's name between two wheat
    sheaves, loaves and pretzels painted along it."""
    o = [rect(0, 0, W, H, '#24503a', rx=0.06), rect(0.05, 0.05, W - 0.1, H - 0.1, 'none', stroke='#e0b448', sw=0.035, rx=0.05)]
    for k in range(int(W / 0.12)): o.append(circ(0.1 + k * 0.12, 0.05, 0.022, '#e0b448'))
    o.append(_txt(W / 2, H * 0.64, 'HENRY &#183; BAKER', 0.27, '#f0d070', extra=' letter-spacing="0.02"'))
    for cx in (0.55, W - 0.55):
        for a in (-0.5, -0.25, 0, 0.25, 0.5):
            o.append(line(cx, H * 0.85, cx + 0.3 * math.sin(a), H * 0.2, '#e8c050', 0.02)); o.append(ell(cx + 0.3 * math.sin(a), H * 0.2, 0.035, 0.08, '#f0cc60'))
        o.append(rect(cx - 0.1, H * 0.55, 0.2, 0.06, '#b03a2a'))
    for cx in (1.05, W - 1.05):
        o.append(ell(cx, H * 0.55, 0.22, 0.16, '#d08a3a', stroke=INK, sw=0.02)); o.append(line(cx - 0.1, H * 0.45, cx + 0.05, H * 0.62, '#f6e0a8', 0.025))
    job(name, 0, 0, W, H, 128, ''.join(o))

def crate(name='crate', seed=171):
    """Wooden crate side 1 x 1 D: slats with gaps, corner battens, nails, a painted mark."""
    r = random.Random(seed); o = [rect(0, 0, 1, 1, '#3a2a1e')]
    for k in range(4): c = mul('#b08a58', r.uniform(0.88, 1.08)); o.append(rect(0.02, 0.02 + k * 0.245, 0.96, 0.2, c, stroke=INK, sw=0.008))
    for x in (0.0, 0.88): o.append(rect(x, 0, 0.12, 1, '#9a7448', stroke=INK, sw=0.01))
    for (x, y) in ((0.06, 0.1), (0.94, 0.1), (0.06, 0.9), (0.94, 0.9)): o.append(circ(x, y, 0.015, '#2a2a2a'))
    o.append(_txt(0.5, 0.58, '&#9880;', 0.25, '#5a2a1a', weight=400))
    job(name, 0, 0, 1, 1, 96, ''.join(o))

def cloth(name, c1, c2, seed=181):
    """Checked cloth 2 x 2 D (stall covers, aprons on lines)."""
    o = [rect(0, 0, 2, 2, c1)]
    for k in range(10):
        o.append(rect(k * 0.2, 0, 0.1, 2, c2, op=0.55)); o.append(rect(0, k * 0.2, 2, 0.1, c2, op=0.55))
    job(name, 0, 0, 2, 2, 64, ''.join(o))

def wood_end(name='log_end'):
    """Sawn log end 1 x 1 D: rings and a crack (log piles for the oven)."""
    o = [circ(0.5, 0.5, 0.5, '#6a4a2e'), circ(0.5, 0.5, 0.44, '#d8b07a')]
    for rr in (0.36, 0.28, 0.2, 0.12, 0.05): o.append(circ(0.5, 0.5, rr, 'none', stroke='#a8804a', sw=0.02))
    o.append(line(0.5, 0.5, 0.88, 0.62, '#5a3a1e', 0.025))
    job(name, 0, 0, 1, 1, 64, ''.join(o))

# ----------------------------------------------------------------------------- sky and the painted backdrop (a medieval town)
SKY = dict(
    afternoon=dict(stops=[(0, '#4a7ac8'), (0.35, '#78a4dc'), (0.62, '#b8cce4'), (0.82, '#f4dcb0'), (1, '#ffd89a')], cloud='#fff8ec', cloud_b='#e8c8b0', sun=('#fff4d0', 205.0, 24.0), glow='#ffd890'),
    morning=dict(stops=[(0, '#6a9ad4'), (0.4, '#a8c4e4'), (0.66, '#dce4ec'), (0.85, '#f8ead4'), (1, '#fff4e0')], cloud='#ffffff', cloud_b='#c8d0e0', sun=('#fffae6', 338.0, 12.0), glow='#fff0c8'),
)
def sky(mode):
    """Sky dome: u = azimuth (0..1 counter-clockwise from +x), v = elevation -15 .. 90 deg; SVG x = azimuth deg, y = 90 - elevation.
    Soft graded sky, the sun with a glow, round cumulus with flat lit-from-below bases (the reference's storybook clouds)."""
    s = SKY[mode]; r = random.Random(191); W, H = 360.0, 105.0
    g = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' + ''.join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in s['stops']) + '</linearGradient>'
    g += '<filter id="b" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="0.18"/></filter>'
    g += f'<radialGradient id="glow"><stop offset="0" stop-color="#fffbe8" stop-opacity="1"/><stop offset="0.3" stop-color="{s["glow"]}" stop-opacity="0.6"/><stop offset="1" stop-color="{s["glow"]}" stop-opacity="0"/></radialGradient>'
    o = [rect(-1, -1, W + 2, H + 2, 'url(#g)')]
    sc, az, el = s['sun']
    for dx in (0, W, -W):
        o.append(ell(az + dx, 90 - el, 60, 30, 'url(#glow)')); o.append(circ(az + dx, 90 - el, 4.0, sc))
    for i in range(26):
        cx = r.uniform(0, W); el2 = r.uniform(6, 40); cy = 90 - el2; w = r.uniform(14, 36) * (1.0 if el2 > 15 else 0.7)
        for xx in _wrap(cx - w / 2, W, w):
            xc = xx + w / 2; grp = []
            for k in range(5):
                t = (k + 0.5) / 5; rk = w * r.uniform(0.11, 0.17) * (1.3 - abs(t - 0.5)); grp.append(circ(xc - w / 2 + w * (0.08 + 0.84 * t), cy - rk * 0.6, rk, s['cloud']))
            grp.append(rect(xc - w / 2, cy - w * 0.07, w, w * 0.07, s['cloud'], rx=w * 0.035)); grp.append(rect(xc - w / 2 + 0.6, cy - w * 0.035, w - 1.2, w * 0.035, s['cloud_b'], rx=w * 0.02))
            o.append('<g filter="url(#b)" opacity="0.95">' + ''.join(grp) + '</g>')
    for _ in range(14):                                                                       # birds
        x = r.uniform(0, W); y = 90 - r.uniform(12, 35); o.append(pline([(x - 0.6, y - 0.3), (x, y), (x + 0.6, y - 0.3)], '#3a3a4a', 0.12))
    job('sky_' + mode, 0, 0, W, H, 4096 / 360.0, ''.join(o), defs=g)

PANO = dict(
    afternoon=dict(hill='#6a9a5a', hill2='#8ab0a0', far='#a8bcd0', plaster=['#ecd8b0', '#e8c890', '#e4c4a8', '#f0e4cc'], roof=['#a85a3a', '#9a5034', '#b86a44', '#8a6a4a'],
                   timber='#4a3020', stone='#c8bca4', haze='#f0d8b4', win='#3a4058', lit=0.05, field=['#c8b058', '#8aa848', '#a8b860']),
    morning=dict(hill='#7a9a7a', hill2='#9ab0b4', far='#b8c8dc', plaster=['#e8dcc4', '#e4d0a8', '#e0ccb8', '#ece4d4'], roof=['#9a6250', '#8e5a48', '#a87058', '#7e6a5a'],
                 timber='#4a3426', stone='#c4c0b4', haze='#e8e4ec', win='#4a5068', lit=0.15, field=['#b8b070', '#8aa060', '#a0b070']))
PANO_R = 120.0; PANO_Z0, PANO_Z1 = -1.5, 40.0

def panorama(mode):
    """Painted ring at R 120 (z -1.5 .. 40), u = azimuth / 360 ccw from +x, transparent above the skyline. Back to front: far blue
    downs, a castle with towers and pennants on a hill, the minster with its spire, patchwork fields and hedges, then two rows of
    jettied town houses (gables, timber framing, tiled and thatched roofs, chimneys with thin smoke), the town wall with a gatehouse."""
    p = PANO[mode]; r = random.Random(201); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def Y(z): return PANO_Z1 - z
    hz = lambda c, k=1.0: mix(c, p['haze'], 0.28 * k)
    pts = [(W * i / 120, Y(9 + 5 * abs(math.sin(i * 0.23)) + 2 * math.sin(i * 0.71))) for i in range(121)]
    o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], hz(p['far'], 1.6)))
    pts = [(W * i / 120, Y(6 + 3 * abs(math.sin(i * 0.37 + 1)) + r.uniform(0, 0.8))) for i in range(121)]
    o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], hz(p['hill2'], 1.2)))
    for k in range(40):                                                                       # fields on the hills
        x = r.uniform(0, W); w = r.uniform(8, 20); z = r.uniform(3.5, 6.5)
        o.append(poly([(x, Y(z)), (x + w, Y(z + r.uniform(-0.5, 0.5))), (x + w + 2, Y(z - 1.2)), (x + 1, Y(z - 1.3))], hz(r.choice(p['field']), 1.1), op=0.8))
        o.append(pline([(x, Y(z)), (x + w, Y(z))], hz('#4a6a3a', 1.0), 0.25, op=0.7))
    for (cx, base) in ((W * 0.18, 7.5), (W * 0.62, 6.8)):                                     # castles on hills
        o.append(ell(cx, Y(base - 1), 22, 6, hz(p['hill'], 1.0)))
        sc = hz(p['stone'], 0.8)
        o.append(rect(cx - 9, Y(base + 6), 18, 6, sc, stroke=hz('#6a6458'), sw=0.15))
        for k in range(10): o.append(rect(cx - 9 + k * 1.9, Y(base + 6.7), 1.0, 0.8, sc))
        for tx_, th_ in ((-9.5, 10), (9.5, 10), (-2.5, 13), (3.5, 11.5)):
            o.append(rect(cx + tx_ - 1.4, Y(base + th_), 2.8, th_, sc, stroke=hz('#6a6458'), sw=0.12))
            o.append(poly([(cx + tx_ - 1.7, Y(base + th_)), (cx + tx_, Y(base + th_ + 3.2)), (cx + tx_ + 1.7, Y(base + th_))], hz('#4a5a8a', 0.8)))
            o.append(line(cx + tx_, Y(base + th_ + 3.2), cx + tx_, Y(base + th_ + 4.6), '#3a3a3a', 0.1)); o.append(poly([(cx + tx_, Y(base + th_ + 4.6)), (cx + tx_ + 1.5, Y(base + th_ + 4.3)), (cx + tx_, Y(base + th_ + 4.0))], '#c83a2a'))
            o.append(rect(cx + tx_ - 0.3, Y(base + th_ - 2), 0.6, 1.0, '#3a3a48'))
        o.append(path(f'M{_c(cx - 1.6)},{_c(Y(base))} L{_c(cx - 1.6)},{_c(Y(base + 2.4))} A1.6 1.6 0 0 1 {_c(cx + 1.6)},{_c(Y(base + 2.4))} L{_c(cx + 1.6)},{_c(Y(base))} Z', '#3a3440'))
    for cx in (W * 0.4, W * 0.86):                                                            # the minster
        sc = hz('#d4c8a8', 0.7); b = 5.0
        o.append(rect(cx - 10, Y(b + 7), 20, 7, sc)); o.append(poly([(cx - 10.5, Y(b + 7)), (cx, Y(b + 10)), (cx + 10.5, Y(b + 7))], hz('#7a7a88', 0.7)))
        o.append(rect(cx - 2, Y(b + 15), 4, 15, sc, stroke=hz('#8a8070'), sw=0.15)); o.append(poly([(cx - 2.2, Y(b + 15)), (cx, Y(b + 26)), (cx + 2.2, Y(b + 15))], hz('#6a7088', 0.6)))
        for k in range(6): o.append(path(f'M{_c(cx - 8.5 + k * 3)},{_c(Y(b + 1.5))} l0,-3 q0.6,-0.9 1.2,0 l0,3 Z', '#4a4458'))
        o.append(circ(cx, Y(b + 11), 1.0, '#4a4458'))
    for band, (zb, sc_, haze) in enumerate(((3.0, 0.8, 1.0), (1.2, 1.0, 0.55), (-0.5, 1.25, 0.25))):   # rows of town houses
        x = r.uniform(-4, 0)
        while x < W:
            w = r.uniform(3.2, 5.2) * sc_; h = r.uniform(4.0, 6.0) * sc_; z0 = zb + 0.6 * math.sin(x * 0.03 + band)
            c = hz(r.choice(p['plaster']), haze); tc = hz(p['timber'], haze * 0.6); rc = hz(r.choice(p['roof']), haze)
            o.append(rect(x, Y(z0 + h), w, h + 2, c, stroke=tc, sw=0.12 * sc_))
            for k in range(1, 4): o.append(line(x + w * k / 4, Y(z0 + h), x + w * k / 4, Y(z0), tc, 0.14 * sc_))
            o.append(line(x, Y(z0 + h * 0.5), x + w, Y(z0 + h * 0.5), tc, 0.18 * sc_))
            for k in range(2): o.append(line(x + w * k / 2 + 0.1, Y(z0 + h * 0.5), x + w * (k + 0.5) / 2, Y(z0 + h - 0.1), tc, 0.1 * sc_))
            for (wx, wz) in ((0.25, 0.62), (0.62, 0.62), (0.3, 0.2)):
                o.append(rect(x + w * wx, Y(z0 + h * wz + 0.9 * sc_), 0.7 * sc_, 0.9 * sc_, '#ffc870' if r.random() < p['lit'] else hz(p['win'], haze)))
            if r.random() < 0.55:
                o.append(poly([(x - 0.3, Y(z0 + h)), (x + w / 2, Y(z0 + h + w * 0.75)), (x + w + 0.3, Y(z0 + h))], rc, stroke=mul(rc, 0.7), sw=0.1))
            else:
                o.append(poly([(x - 0.3, Y(z0 + h)), (x + 0.8, Y(z0 + h + 2.2 * sc_)), (x + w - 0.8, Y(z0 + h + 2.2 * sc_)), (x + w + 0.3, Y(z0 + h))], rc, stroke=mul(rc, 0.7), sw=0.1))
            if r.random() < 0.5:
                cxx = x + w * r.uniform(0.2, 0.8); ch = z0 + h + 1.4 * sc_ + 0.8
                o.append(rect(cxx, Y(ch + 0.8), 0.6 * sc_, 2.2, hz('#9a6a50', haze)))
                for s_ in range(4): o.append(circ(cxx + 0.3 + s_ * 0.5, Y(ch + 1.2 + s_ * 0.8), 0.35 + s_ * 0.25, '#f0ece8', op=0.35 - s_ * 0.07))
            x += w + r.uniform(0.0, 0.6) * sc_
    o.append(rect(0, Y(1.2), W, 2.8, hz('#b8ac94', 0.4)))                                   # the town wall along the front
    for k in range(int(W / 1.6)): o.append(rect(k * 1.6, Y(1.8), 0.9, 0.7, hz('#b8ac94', 0.4)))
    for _ in range(30):                                                                       # trees
        x = r.uniform(0, W); z = r.uniform(1.0, 4.0); s = r.uniform(1.2, 2.4)
        o.append(rect(x - 0.15, Y(z + s), 0.3, s, hz('#5a4030', 0.5))); o.append(circ(x, Y(z + s * 1.4), s * 0.8, hz(r.choice(('#5a8a4a', '#4a7a42', '#6a9a52')), 0.5)))
    job('pano_' + mode, 0, 0, W, H, 8.0, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- registry
MODES = ('afternoon', 'morning')
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear(); _WID[0] = 0
    stone_wall(); stone_wall('stone_ext', 12, '#c4b496'); plaster(); plaster('plaster_ext', '#ecdcb8', 22, soot=0.0)
    brick(); brick('brick_soot', 32, soot=0.75); flags(); flags('flags_clean', 42, flour=0.15)
    timber(); timber('timber_l', '#9a6c40', 52)
    planks('table', '#a8784a', 61, flour=0.55, scraps=True); planks('shelf', '#8a6038', 62, n=4, flour=0.2); planks('floorb', '#7a5a3a', 63, n=8, flour=0.5)
    planks('counter', '#9a6a3e', 64, n=4, flour=0.35)
    sack(); sack('sack_plain', 72, mark=False); loaf(); loaf('loaf_dark', 82, '#a8602a', '#7a3a18'); loaf('loaf_pale', 83, '#d8a050', '#b87a34')
    fire(); embers(); steam(); steam('steam2', 102); shaft(); leaded(); herbs(); herbs('onions', 122, 'onion'); herbs('wheat', 123, 'wheat'); herbs('herbs2', 124)
    for v in range(4):
        pc = PLASTERS[v]; tc = TIMBERS[v]
        facade('ht%d_g' % v, 6.0, 3.6, pc, tc, 300 + v, 'ground', style=v % 4, shop=['#c03a2a', '#2e6a4a', '#d8a030', '#3a5a9a'][v])
        facade('ht%d_u' % v, 6.0, 3.4, pc, tc, 310 + v, 'upper', style=(v + 1) % 4, lit=0.15, shutters=['#3a6a4a', '#8a3a2a', '#3a5a8a', '#6a4a2a'][v])
        facade('ht%d_gab' % v, 6.0, 3.6, pc, tc, 320 + v, 'gable', style=0)
    facade('bk_u', 7.0, 3.4, '#ecd8b0', '#4a3020', 330, 'upper', style=3, lit=0.0, shutters='#2e5a3a')
    facade('bk_gab', 7.0, 3.8, '#ecd8b0', '#4a3020', 331, 'gable')
    roof(); roof('roof_tile2', 132, '#8e5a46'); thatch(); cobbles(); cobbles('cobbles2', 152)
    awning('awn_red', '#c8382a', '#f4ead4'); awning('awn_green', '#2e7a4e', '#f0e4c4'); awning('awn_blue', '#2e5a9a', '#f0d890'); awning('awn_yellow', '#e0a830', '#9a2a22')
    sign_board('sign_bread', 'bread'); sign_board('sign_pretzel', 'pretzel'); sign_board('sign_tankard', 'tankard'); sign_board('sign_boot', 'boot'); sign_board('sign_fish', 'fish')
    banner('ban_king', 'king'); banner('ban_town', 'town'); banner('ban_guild', 'guild')
    notice(); fascia(); crate(); cloth('cloth_red', '#e8dcc4', '#b83a2a'); cloth('cloth_blue', '#e8e0cc', '#3a5a9a'); cloth('cloth_green', '#e8e0c4', '#3a7a4a'); wood_end()
    PT.pool()
    for m in MODES: sky(m); panorama(m)

def ensure(verbose=True):
    """Draw every texture, rasterise the changed ones (one Chromium launch), return {name: png path}."""
    os.makedirs(TEX, exist_ok=True); os.makedirs(WORK, exist_ok=True)
    all_jobs()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    for name, j in TT.JOBS.items():
        h = hashlib.sha1((j['svg'] + str(j['transparent'])).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            sp = os.path.join(WORK, 'tex_' + name + '.svg'); open(sp, 'w').write(j['svg'])
            todo.append(dict(src=sp, out=png, w=j['w'], h=j['h'], transparent=j['transparent'])); man[name] = h
    if todo:
        jp = os.path.join(WORK, 'tex_jobs.json'); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', RASTER, jp], env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')), capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('texture raster failed: ' + r.stderr[-2000:])
        if verbose: print('textures rasterised:', ', '.join(os.path.basename(t['out']) for t in todo))
        json.dump(man, open(mpath, 'w'), indent=0, sort_keys=True)
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: (os.path.basename(v), SIZE[k]) for k, v in p.items()}, indent=0))
