#!/usr/bin/env python3
"""mine_tex.py : artwork of the film-5 set (a British coal mine about 1905: the tunnel underground and the pithead at the surface),
drawn as SVG in Python and rasterised by headless Chromium (PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in
v3/set3d5/tex_mine/ by content hash. Same route as v3/set3d4/pagoda_tex.py: tower_tex's SVG helpers and job() registry are imported.

    import mine_tex as MT
    paths = MT.ensure()        # {name: png path}
    MT.SIZE[name] -> (w_D, h_D) of one image / tile

Every surface is drawn in the colour it shows in neutral light; the lit material makes lamp light and shade of it.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2')); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d4'))
import tower_tex as TT                                                     # noqa: E402
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401
import pagoda_tex as PT                                                    # noqa: E402  (pool decal reused)

TEX = os.path.join(HERE, 'tex_mine'); WORK = os.path.join(HERE, 'mine_work')
RASTER = TT.RASTER; SIZE = TT.SIZE; job = TT.job
INK = '#1e1626'

# ----------------------------------------------------------------------------- underground
def coal(name='coal', seed=11, W=4.0, H=4.0, face=False):
    """Rough coal wall 4 x 4 D (u along the tunnel, v round the section, tiles both ways): strata of dull shale and bright coal
    bands with vertical cleat cracks, pick marks, a few pyrite / mica specks (the glittering seams; the material adds the sparkle)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#384052')]
    y = 0.0; bands = []
    while y < H:
        h = r.uniform(0.18, 0.62); kind = r.choice(('coal', 'coal', 'shale', 'dirt')); bands.append((y, h, kind)); y += h
    bands[-1] = (bands[-1][0], H - bands[-1][0], bands[-1][2])
    for (y0, h, kind) in bands:
        col = dict(coal='#2a3040', shale='#4e586e', dirt='#464e5c')[kind]
        o.append(rect(-0.1, y0, W + 0.2, h, mul(col, r.uniform(0.92, 1.08))))
        if kind == 'coal':
            for _ in range(int(W * 6)):                                                      # cleat: short vertical cracks with a bright lip
                x = r.uniform(0, W); hh = r.uniform(0.3, 1.0) * h
                for xx in _wrap(x, W, 0.02):
                    o.append(line(xx, y0 + r.uniform(0, h - hh), xx, y0 + hh, '#141822', 0.018))
                    o.append(line(xx + 0.02, y0 + 0.02, xx + 0.02, y0 + hh * 0.8, '#6a7896', 0.01, op=0.8))
            for _ in range(int(W * 5)):                                                      # glossy lumps
                x = r.uniform(0, W); yy = y0 + r.uniform(0.05, h - 0.05); w = r.uniform(0.08, 0.3)
                for xx in _wrap(x, W, w): o.append(ell(xx + w / 2, yy, w / 2, r.uniform(0.03, 0.07), '#42506a', op=0.8))
        else:
            for _ in range(int(W * 3)):
                x = r.uniform(0, W); w = r.uniform(0.2, 0.8)
                for xx in _wrap(x, W, w): o.append(line(xx, y0 + r.uniform(0, h), xx + w, y0 + r.uniform(0, h), mul(col, 0.8), 0.02, op=0.7))
        o.append(line(-0.1, y0, W + 0.1, y0, '#181c26', 0.03, op=0.9))
    for _ in range(int(W * H * 2.2)):                                                         # pick marks
        x = r.uniform(0, W); yy = r.uniform(0, H); a = r.uniform(-0.6, 0.6); L = r.uniform(0.12, 0.3)
        for xx in _wrap(x, W, L): o.append(line(xx, yy, xx + L * math.cos(a), yy + L * math.sin(a), '#1a1e2a', 0.025, op=0.75))
    for _ in range(int(W * H * 6)):                                                           # specks (pyrite gold / mica blue-white)
        x = r.uniform(0, W); yy = r.uniform(0, H)
        o.append(circ(x, yy, r.uniform(0.01, 0.025), r.choice(('#d8c070', '#c8d8f4', '#e8f0ff', '#b8caf0'))))
    if face:
        for k in range(3):                                                                    # undercut slot at the foot of the face
            o.append(rect(-0.1, H - 0.35, W + 0.2, 0.25, '#10141c'))
    job(name, 0, 0, W, H, 112, ''.join(o))

def glint(name='glint', seed=11, W=4.0, H=4.0):
    """Sparkle mask on the coal UVs (black background, white specks along the coal bands): the glossy weight of the glittering seams."""
    r = random.Random(seed + 500); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#000000')]
    for _ in range(int(W * H * 22)):
        x = r.uniform(0, W); y = r.uniform(0, H); s = r.uniform(0.012, 0.035)
        o.append(circ(x, y, s, '#ffffff' if r.random() < 0.5 else '#9a9a9a'))
    for _ in range(int(W * 4)):                                                               # seam lines that glint
        y = r.uniform(0, H); x = r.uniform(0, W); L = r.uniform(0.4, 1.6)
        for xx in _wrap(x, W, L): o.append(line(xx, y, xx + L, y + r.uniform(-0.05, 0.05), '#d0d0d0', 0.018))
    job(name, 0, 0, W, H, 112, ''.join(o))

def floor():
    """Roadway floor 4 x 4 D: trodden coal dust and grit, lighter stone-dust patches, small lumps, boot prints, wet dark patches."""
    r = random.Random(21); W = H = 4.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#444b58')]
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.3, 1.0); ry = r.uniform(0.2, 0.6)
        for xx in _wrap(x - rx, W, 2 * rx):
            for yy in _wrap(y - ry, H, 2 * ry): o.append(ell(xx + rx, yy + ry, rx, ry, r.choice(('#58606e', '#383e4a', '#666c78', '#323844')), op=0.55))
    for _ in range(520):
        x, y = r.uniform(0, W), r.uniform(0, H); s = r.uniform(0.015, 0.06)
        o.append(poly([(x - s, y), (x, y - s * 0.8), (x + s, y + s * 0.2), (x + s * 0.2, y + s)], r.choice(('#222830', '#2c323c', '#767c86', '#565e6a'))))
    for _ in range(12):                                                                       # boot prints
        x, y = r.uniform(0.2, W - 0.4), r.uniform(0.2, H - 0.4)
        o.append(ell(x, y, 0.08, 0.15, '#323842', op=0.6)); o.append(ell(x + 0.12, y + 0.32, 0.08, 0.15, '#323842', op=0.6))
    job('floor', 0, 0, W, H, 80, ''.join(o))

def timber(name='timber', base='#9a6a40', seed=31):
    """Pit prop / bar wrap 1 x 2 D (u round, v along): sawn larch with bark strips, grain, splits and a coal-dust bloom."""
    r = random.Random(seed); W, H = 1.0, 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(26):
        x = r.uniform(0, W); w = r.uniform(0.005, 0.02)
        for xx in _wrap(x, W, w): o.append(rect(xx, -0.1, w, H + 0.2, mul(base, r.uniform(0.7, 0.85)), op=0.8))
    for _ in range(7):                                                                        # bark left on the prop
        x = r.uniform(0, W); w = r.uniform(0.08, 0.22); y = r.uniform(-0.2, H); h = r.uniform(0.5, 1.4)
        for xx in _wrap(x, W, w): o.append(rect(xx, y, w, h, mul('#6a4e30', r.uniform(0.9, 1.1)), rx=0.04))
    for _ in range(5):
        x = r.uniform(0, W); y = r.uniform(0, H)
        o.append(ell(x, y, 0.04, 0.08, mul(base, 0.55))); o.append(ell(x, y, 0.02, 0.05, mul(base, 0.4)))
    o.append(rect(-0.1, -0.1, W + 0.2, 0.25, '#363c46', op=0.35)); o.append(rect(-0.1, H - 0.4, W + 0.2, 0.5, '#282c34', op=0.4))
    job(name, 0, 0, W, H, 96, ''.join(o))

def planks(name='planks', base='#8a6040', seed=41, W=2.0, H=2.0, n=8, dirty=0.35):
    """Boards 2 x 2 D, horizontal (lagging, tubs, hut walls): plank colour jitter, gaps, grain, nail heads, dust."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.45))]; ph = H / n
    for k in range(n):
        c = mul(base, r.uniform(0.85, 1.12)); o.append(rect(-0.1, k * ph + 0.012, W + 0.2, ph - 0.024, c))
        for _ in range(4): yy = k * ph + r.uniform(0.03, ph - 0.03); o.append(line(-0.1, yy, W + 0.1, yy + r.uniform(-0.02, 0.02), mul(c, 0.82), 0.008))
        for x in (0.15, 1.15): o.append(circ(x, k * ph + ph / 2, 0.018, '#3a3232'))
    o.append(rect(-0.1, H * 0.6, W + 0.2, H * 0.45, '#2c3038', op=dirty))
    job(name, 0, 0, W, H, 96, ''.join(o))

def canvas():
    """Brattice / ventilation-door canvas 3 x 4 D: tarred hessian, weave, patched, stitched seams, a stencilled warning."""
    r = random.Random(51); W, H = 3.0, 4.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#7a6a52')]
    for i in range(0, 300):
        x = i * 0.01; o.append(line(x, -0.1, x, H + 0.1, '#6a5a44', 0.004, op=0.5))
    for k in range(3):
        x = 0.95 + k * 1.0; o.append(line(x, -0.1, x, H + 0.1, '#4a3e30', 0.02)); o.append(pline([(x + 0.03, y * 0.08) for y in range(52)], '#d8c8a0', 0.008, op=0.6))
    for _ in range(6):
        x, y = r.uniform(0.1, W - 0.6), r.uniform(0.2, H - 0.8); w, h = r.uniform(0.3, 0.6), r.uniform(0.3, 0.7)
        o.append(rect(x, y, w, h, r.choice(('#8a7a5a', '#6a5e4a', '#94845e')), stroke='#3a3024', sw=0.015))
    for _ in range(9):
        x = r.uniform(0, W); o.append(rect(x, r.uniform(1.5, 3.0), r.uniform(0.05, 0.15), r.uniform(0.6, 1.4), '#2c3036', op=0.35))
    o.append(rect(0.5, 1.25, 2.0, 0.55, '#e8dcc0', op=0.85))
    o.append(f'<text x="1.5" y="1.5" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="0.22" text-anchor="middle" fill="#8a2018">KEEP THIS DOOR</text>')
    o.append(f'<text x="1.5" y="1.74" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="0.22" text-anchor="middle" fill="#8a2018">SHUT</text>')
    o.append(rect(-0.1, H - 0.6, W + 0.2, 0.7, '#282a30', op=0.45))
    job('canvas', 0, 0, W, H, 96, ''.join(o))

def whitewash():
    """Pit-bottom wall 4 x 4 D: whitewashed brick lining, dusty grey toward the floor, drips and soot."""
    r = random.Random(61); W = H = 4.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#e8e4dc')]
    for k in range(25):
        y = k * 0.16; off = 0.2 * (k % 2); o.append(line(-0.1, y, W + 0.1, y, '#b8b4b4', 0.014))
        for i in range(-1, 11):
            x = i * 0.4 + off; o.append(line(x, y, x, y + 0.16, '#c0bcbc', 0.012))
    for _ in range(18):
        x = r.uniform(0, W); w = r.uniform(0.04, 0.12)
        for xx in _wrap(x, W, w): o.append(rect(xx, r.uniform(0, 1.0), w, r.uniform(0.6, 2.2), '#9298a4', op=0.3, rx=0.03))
    o.append(rect(-0.1, H - 1.2, W + 0.2, 1.3, '#646a76', op=0.45)); o.append(rect(-0.1, H - 0.5, W + 0.2, 0.6, '#363c46', op=0.4))
    job('whitewash', 0, 0, W, H, 64, ''.join(o))

def sign(name, lines_, bg='#e8dcb8', fg='#1e1a1a', W=2.0, H=0.8, border='#3a2a20'):
    o = [rect(0, 0, W, H, bg, stroke=border, sw=0.06)]
    n = len(lines_)
    for i, (t, sz, col) in enumerate(lines_):
        y = H * (i + 0.5) / n + sz * 0.36
        o.append(f'<text x="{_c(W / 2)}" y="{_c(y)}" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{_c(sz)}" text-anchor="middle" fill="{col or fg}">{t}</text>')
    for x in (0.08, W - 0.08):
        o.append(circ(x, 0.1, 0.03, '#4a4040')); o.append(circ(x, H - 0.1, 0.03, '#4a4040'))
    job(name, 0, 0, W, H, 160, ''.join(o))

def gauze():
    """Safety-lamp wire gauze 1 x 1 D (alpha): fine brass mesh."""
    o = []
    for i in range(41):
        o.append(line(i * 0.025, 0, i * 0.025, 1, '#c8b890', 0.006)); o.append(line(0, i * 0.025, 1, i * 0.025, '#b0a080', 0.006))
    job('gauze', 0, 0, 1, 1, 256, ''.join(o), transparent=True)

def tub():
    """Coal tub side 2 x 1.4 D: oak boards painted rust red, iron corner straps and bands with rivets, a chalked number, coal dust."""
    r = random.Random(71); W, H = 2.0, 1.4; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#7a3a2a')]
    for k in range(5):
        c = mul('#8e4630', r.uniform(0.85, 1.1)); o.append(rect(-0.1, k * 0.28 + 0.01, W + 0.2, 0.26, c))
    for x in (0.0, 0.62, 1.38, 1.9):
        o.append(rect(x, -0.1, 0.1, H + 0.2, '#3e3a44'))
        for k in range(6): o.append(circ(x + 0.05, 0.1 + k * 0.24, 0.018, '#6a6670'))
    for y in (0.04, 1.28): o.append(rect(-0.1, y, W + 0.2, 0.08, '#3e3a44'))
    o.append(f'<text x="1.0" y="0.85" font-family="Arial, sans-serif" font-weight="700" font-size="0.32" text-anchor="middle" fill="#e8e0d0" opacity="0.8">{r.randint(12, 89)}</text>')
    o.append(rect(-0.1, 0.9, W + 0.2, 0.6, '#1c2028', op=0.4))
    job('tub', 0, 0, W, H, 128, ''.join(o))

def coal_lumps(name='lumps', seed=81, W=2.0, H=2.0, base='#20262f'):
    """Heaped coal 2 x 2 D: packed angular lumps with bright facets (heaps, tub loads)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.6))]
    for _ in range(int(W * H * 70)):
        x, y = r.uniform(0, W), r.uniform(0, H); s = r.uniform(0.04, 0.12); a = r.uniform(0, 6.28)
        pts = [(x + s * math.cos(a + k * 2.1 + r.uniform(-0.3, 0.3)) * r.uniform(0.7, 1.2), y + s * math.sin(a + k * 2.1) * r.uniform(0.7, 1.2)) for k in range(3)]
        o.append(poly(pts, mul(base, r.uniform(0.8, 1.4))))
        o.append(line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], '#7088a8', 0.008, op=0.7))
    job(name, 0, 0, W, H, 96, ''.join(o))

# ----------------------------------------------------------------------------- the surface
BRICK_UK = ['#a8452e', '#9a3c28', '#b25236', '#8e3826', '#a04a32', '#b85a3a', '#943e2c']
def brick(name='brick', seed=91, soot=0.0):
    """English bond red brick 2 x 1.92 D (12 courses), lime mortar, soot staining (engine house, chimney)."""
    r = random.Random(seed); W, H = 2.0, 1.92; ch = 0.16; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#c8b49a')]
    for k in range(12):
        y = k * ch; header = k % 2; bl = 0.2 if header else 0.4; off = 0.1 * (k // 2 % 2) if header else 0.0
        for i in range(-1, int(W / bl) + 2):
            x = i * bl + off; c = mul(r.choice(BRICK_UK), r.uniform(0.92, 1.06))
            for xx in _wrap(x + 0.01, W, bl - 0.02):
                o.append(rect(xx, y + 0.012, bl - 0.02, ch - 0.024, c, rx=0.008))
                if r.random() < 0.25: o.append(rect(xx + 0.02, y + 0.02, bl - 0.06, 0.02, mul(c, 1.15), rx=0.006))
    if soot > 0:
        for _ in range(10):
            x = r.uniform(0, W); w = r.uniform(0.1, 0.4)
            for xx in _wrap(x, W, w): o.append(rect(xx, r.uniform(-0.5, 0.6), w, r.uniform(0.6, 1.6), '#2a2028', op=0.25 * soot, rx=0.05))
    job(name, 0, 0, W, H, 192, ''.join(o))

def slate():
    """Welsh slate roof 2 x 2 D: blue-grey slates in courses, staggered, some lighter."""
    r = random.Random(101); W = H = 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#2e3240')]
    for k in range(10):
        y = k * 0.2; off = 0.15 * (k % 2)
        for i in range(-1, 8):
            x = i * 0.3 + off; c = mul('#4e5468', r.uniform(0.85, 1.15))
            for xx in _wrap(x + 0.01, W, 0.28): o.append(rect(xx, y + 0.01, 0.28, 0.19, c)); o.append(rect(xx, y + 0.16, 0.28, 0.035, mul(c, 0.7)))
    job('slate', 0, 0, W, H, 96, ''.join(o))

def yard():
    """Pithead yard 4 x 4 D: black cinder and ash, puddle-dark ruts, spilled coal, stones."""
    r = random.Random(111); W = H = 4.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#545a66')]
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, H); rx = r.uniform(0.2, 0.9); ry = rx * r.uniform(0.3, 0.7)
        for xx in _wrap(x - rx, W, 2 * rx):
            for yy in _wrap(y - ry, H, 2 * ry): o.append(ell(xx + rx, yy + ry, rx, ry, r.choice(('#646a76', '#424852', '#787470', '#383e48')), op=0.5))
    for _ in range(600):
        x, y = r.uniform(0, W), r.uniform(0, H); s = r.uniform(0.012, 0.05)
        o.append(circ(x, y, s, r.choice(('#22282e', '#868a90', '#2c323a', '#9a8a7a'))))
    job('yard', 0, 0, W, H, 64, ''.join(o))

def hut():
    """First-aid hut walls 2 x 2 D: green-painted weatherboard, vertical cover strips at 1 D."""
    r = random.Random(121); W = H = 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#2a4436')]
    for k in range(10):
        c = mul('#4a7a5a', r.uniform(0.92, 1.06)); o.append(rect(-0.1, k * 0.2 + 0.01, W + 0.2, 0.18, c)); o.append(rect(-0.1, k * 0.2 + 0.15, W + 0.2, 0.04, mul(c, 0.7)))
    for _ in range(14):
        x = r.uniform(0, W); o.append(rect(x, r.uniform(0, H), r.uniform(0.05, 0.2), 0.04, '#c8c0a0', op=0.4))
    o.append(rect(-0.1, H - 0.35, W + 0.2, 0.45, '#282c34', op=0.35))
    job('hut', 0, 0, W, H, 96, ''.join(o))

def firstaid():
    o = [rect(0, 0, 2.4, 0.9, '#f2ece0', stroke='#2a2a2a', sw=0.05), rect(0.18, 0.2, 0.5, 0.5, '#ffffff'),
         rect(0.36, 0.22, 0.14, 0.46, '#c82a22'), rect(0.2, 0.38, 0.46, 0.14, '#c82a22')]
    o.append('<text x="1.55" y="0.6" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="0.32" text-anchor="middle" fill="#1e2a22">FIRST AID</text>')
    job('firstaid', 0, 0, 2.4, 0.9, 160, ''.join(o))

def oxy_panel():
    """Front of the brass oxygen resuscitation box 1.2 x 0.8 D: engraved brass with an enamel plate OXYGEN and a pressure dial."""
    o = [rect(0, 0, 1.2, 0.8, '#c8963c'), rect(0.03, 0.03, 1.14, 0.74, 'none', stroke='#7a5418', sw=0.02)]
    for k in range(9): o.append(line(0.05, 0.08 + k * 0.08, 1.15, 0.08 + k * 0.08, '#e6b85a', 0.006, op=0.6))
    o.append(rect(0.12, 0.08, 0.96, 0.16, '#f4f0e4', stroke='#5a3c14', sw=0.012, rx=0.03))
    o.append('<text x="0.6" y="0.205" font-family="Georgia, serif" font-weight="700" font-size="0.12" text-anchor="middle" fill="#1e2a6a">OXYGEN</text>')
    o.append(circ(0.3, 0.52, 0.17, '#f6f2e6', stroke='#5a3c14', sw=0.025))
    for k in range(9):
        a = math.radians(-220 + k * 32.5); o.append(line(0.3 + 0.12 * math.cos(a), 0.52 + 0.12 * math.sin(a), 0.3 + 0.15 * math.cos(a), 0.52 + 0.15 * math.sin(a), '#222', 0.01))
    o.append(line(0.3, 0.52, 0.3 + 0.12 * math.cos(math.radians(-60)), 0.52 + 0.12 * math.sin(math.radians(-60)), '#a82020', 0.014)); o.append(circ(0.3, 0.52, 0.018, '#222'))
    for x in (0.08, 1.12):
        for y in (0.08, 0.72): o.append(circ(x, y, 0.018, '#7a5418'))
    job('oxy_panel', 0, 0, 1.2, 0.8, 320, ''.join(o))

def winding_label():
    o = [rect(0, 0, 3.0, 0.7, '#1e2430', stroke='#c8a050', sw=0.05)]
    o.append('<text x="1.5" y="0.47" font-family="Georgia, serif" font-weight="700" font-size="0.36" text-anchor="middle" fill="#e8c870">No. 2 PIT</text>')
    job('pit_label', 0, 0, 3.0, 0.7, 128, ''.join(o))

# ----------------------------------------------------------------------------- sky and the painted backdrop (terraced rows)
SKY = dict(
    dusk=dict(stops=[(0, '#1c3070'), (0.32, '#3e5a9c'), (0.55, '#b08a80'), (0.74, '#f08a48'), (0.9, '#ffa850'), (1, '#ffc878')], smoke='#4a5068', smoke_l='#a8988e', cloud='#ffbc84', cloud_b='#6a6e92', sun=('#fff0c0', 195.0, 5.0)),
    dawn=dict(stops=[(0, '#6688c0'), (0.4, '#a8bcda'), (0.66, '#e4dcd4'), (0.85, '#fbe6c4'), (1, '#fff6e0')], smoke='#8a90a4', smoke_l='#d0ccc8', cloud='#ffffff', cloud_b='#b4bccc', sun=('#fff8dc', 345.0, 6.0)))

def sky(mode):
    """Sky dome: u = azimuth (0..1 counter-clockwise from +x), v = elevation -15 .. 90 deg; SVG x = azimuth deg, y = 90 - elevation.
    Smoky industrial sky: graded colour, the low sun with a glow, long flat bands of smoke and flat-bottomed clouds."""
    s = SKY[mode]; r = random.Random(131); W, H = 360.0, 105.0
    g = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' + ''.join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in s['stops']) + '</linearGradient>'
    g += '<filter id="b" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="0.9"/></filter>'
    g += '<radialGradient id="glow"><stop offset="0" stop-color="#fff6d8" stop-opacity="1"/><stop offset="0.3" stop-color="#ffd890" stop-opacity="0.7"/><stop offset="1" stop-color="#ffa060" stop-opacity="0"/></radialGradient>'
    o = [rect(-1, -1, W + 2, H + 2, 'url(#g)')]
    sc, az, el = s['sun']
    for dx in (0, W, -W):
        o.append(ell(az + dx, 90 - el, 70, 26, 'url(#glow)')); o.append(circ(az + dx, 90 - el, 5.0, sc))
    for i in range(16):                                                                       # long smoke bands
        y = 90 - r.uniform(4, 30); x = r.uniform(0, W); w = r.uniform(60, 160); h = r.uniform(1.2, 3.5)
        for xx in _wrap(x, W, w):
            o.append(f'<g filter="url(#b)" opacity="{_c(r.uniform(0.35, 0.6))}">' + ell(xx + w / 2, y, w / 2, h, r.choice((s['smoke'], s['smoke_l']))) + '</g>')
    for i in range(10):
        cx = r.uniform(0, W); el2 = r.uniform(10, 42); cy = 90 - el2; w = r.uniform(18, 34)
        for xx in _wrap(cx - w / 2, W, w):
            xc = xx + w / 2; grp = []
            for k in range(4):
                t = (k + 0.5) / 4; rk = w * r.uniform(0.12, 0.17) * (1.25 - abs(t - 0.5)); grp.append(circ(xc - w / 2 + w * (0.1 + 0.8 * t), cy - rk * 0.55, rk, s['cloud']))
            grp.append(rect(xc - w / 2, cy - w * 0.08, w, w * 0.08, s['cloud'], rx=w * 0.04)); grp.append(rect(xc - w / 2 + 0.6, cy - w * 0.04, w - 1.2, w * 0.04, s['cloud_b'], rx=w * 0.02))
            o.append('<g filter="url(#b)" opacity="0.9">' + ''.join(grp) + '</g>')
    job('sky_' + mode, 0, 0, W, H, 2048 / 360.0, ''.join(o), defs=g)

PANO = dict(
    dusk=dict(hill='#4a5478', hill2='#66708e', brick=['#9a5644', '#8a4e42', '#a45e48'], roof='#343a5a', shade='#4a4e7a', win='#2e3040', lit=0.45, smoke='#787a8a', haze='#e0a07a', tip='#2a2e3e'),
    dawn=dict(hill='#7a84a8', hill2='#9aa0b8', brick=['#b07a68', '#a87262', '#b88674'], roof='#5a6482', shade='#7a80a8', win='#4a4e66', lit=0.12, smoke='#aeb0bc', haze='#f0d4bc', tip='#4a4e62'))
PANO_R = 120.0; PANO_Z0, PANO_Z1 = -1.5, 40.0

def panorama(mode):
    """Painted ring at R 120 (z -1.5 .. 40), u = azimuth / 360 ccw from +x, transparent above the skyline. Back to front: far hills
    with other headframes and a spoil tip, smoke plumes, then rows of brick terraced houses climbing the hill (slate roofs, chimney
    stacks with smoke, lit windows at dusk), a chapel, gas lamps."""
    p = PANO[mode]; r = random.Random(141); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def Y(z): return PANO_Z1 - z
    hz = lambda c, k=1.0: mix(c, p['haze'], 0.3 * k)
    pts = [(W * i / 90, Y(7 + 4 * abs(math.sin(i * 0.31)) + r.uniform(0, 1.5))) for i in range(91)]
    o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], hz(p['hill2'], 1.4)))
    for k in range(7):                                                                        # far spoil tips and headframes
        x = r.uniform(0, W); o.append(poly([(x - 9, Y(5)), (x, Y(12 + r.uniform(0, 4))), (x + 9, Y(5))], hz(p['tip'], 1.0)))
        hx_ = x + r.uniform(12, 30); hh = r.uniform(7, 10)
        o.append(line(hx_ - 1.2, Y(4), hx_, Y(hh), hz(p['tip']), 0.3)); o.append(line(hx_ + 1.2, Y(4), hx_, Y(hh), hz(p['tip']), 0.3)); o.append(circ(hx_, Y(hh), 0.8, 'none', stroke=hz(p['tip']), sw=0.2))
        cx_ = hx_ + 6; o.append(rect(cx_, Y(16), 0.9, 12, hz(p['tip'])))
        for j in range(5): o.append(circ(cx_ + 0.5 + j * 2.2, Y(16.5 + j * 1.3), 1.2 + j * 0.5, p['smoke'], op=0.45 - j * 0.06))
    for band, (zb, step) in enumerate(((4.5, 2.6), (2.6, 2.4), (0.8, 2.2))):                    # three rows of terraces
        x = r.uniform(-3, 0)
        while x < W:
            n = r.randint(6, 12); c = hz(r.choice(p['brick']), 1.0 - 0.3 * band); hh = 2.6 + 0.3 * band; z0 = zb + 1.5 * math.sin(x * 0.02 + band)
            w = n * 1.6
            o.append(rect(x, Y(z0 + hh), w, hh + 2, c)); o.append(rect(x + w - 1.0, Y(z0 + hh), 1.0, hh + 2, p['shade'], op=0.4))
            o.append(poly([(x - 0.3, Y(z0 + hh)), (x + 0.6, Y(z0 + hh + 1.3)), (x + w - 0.6, Y(z0 + hh + 1.3)), (x + w + 0.3, Y(z0 + hh))], p['roof']))
            for j in range(n):
                hx_ = x + j * 1.6
                for (wx, wz) in ((0.3, 0.5), (0.9, 0.5), (0.3, 1.7), (0.9, 1.7)):
                    lit = r.random() < p['lit']; o.append(rect(hx_ + wx, Y(z0 + wz + 0.65), 0.35, 0.6, '#ffc060' if lit else p['win']))
                if j % 2 == 0:
                    o.append(rect(hx_ + 1.4, Y(z0 + hh + 2.0), 0.45, 0.9, mul(c, 0.8)))
                    if r.random() < 0.6:
                        for s_ in range(4): o.append(circ(hx_ + 1.7 + s_ * 0.9, Y(z0 + hh + 2.4 + s_ * 0.7), 0.4 + s_ * 0.3, p['smoke'], op=0.4 - s_ * 0.08))
            x += w + r.uniform(0.6, 3.0)
    for k in range(3):                                                                        # chapels
        x = r.uniform(0, W); c = hz('#8a8070'); o.append(rect(x, Y(9), 6, 9, c)); o.append(poly([(x - 0.5, Y(9)), (x + 3, Y(12)), (x + 6.5, Y(9))], p['roof']))
        o.append(path(f'M{_c(x + 2.2)},{_c(Y(3))} L{_c(x + 2.2)},{_c(Y(6.5))} A0.8 0.8 0 0 1 {_c(x + 3.8)},{_c(Y(6.5))} L{_c(x + 3.8)},{_c(Y(3))} Z', '#ffc060' if p['lit'] > 0.2 else p['win']))
    job('pano_' + mode, 0, 0, W, H, 4.0, ''.join(o), transparent=True)

def smoke_puff():
    """Soft smoke puff sprite 2 x 2 D (alpha), grey-violet."""
    d = '<radialGradient id="s"><stop offset="0" stop-color="#ffffff" stop-opacity="0.9"/><stop offset="0.55" stop-color="#ffffff" stop-opacity="0.5"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>'
    o = ''.join(circ(1 + 0.45 * math.cos(a), 1 + 0.35 * math.sin(a), 0.55, 'url(#s)') for a in (0.3, 2.0, 3.9, 5.3)) + circ(1, 1, 0.75, 'url(#s)')
    job('puff', 0, 0, 2, 2, 64, o, defs=d, transparent=True)

# ----------------------------------------------------------------------------- registry
MODES = ('dusk', 'dawn')
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear()
    coal(); coal('coal_face', 12, face=True); glint(); floor(); timber('timber', '#b08a4c', 31); timber('timber_d', '#94703e', 32)
    planks('planks', '#9a7444', 41); planks('lagging', '#8a6a3e', 42, dirty=0.5); canvas(); whitewash(); gauze(); tub(); coal_lumps(); coal_lumps('lumps_heap', 82, 4.0, 4.0, '#242a34')
    sign('sign_pit', [('PIT BOTTOM', 0.26, None), ('No. 2 SHAFT', 0.18, '#8a2018')])
    sign('sign_danger', [('DANGER', 0.3, '#b02018'), ('NO NAKED LIGHTS', 0.15, None)], bg='#f0e8d0', W=1.6, H=0.7)
    sign('sign_heading', [('No. 4 HEADING', 0.2, None)], bg='#d8ccb0', W=1.6, H=0.45)
    brick(); brick('brick_soot', 92, soot=1.0); slate(); yard(); hut(); firstaid(); oxy_panel(); winding_label(); smoke_puff()
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
