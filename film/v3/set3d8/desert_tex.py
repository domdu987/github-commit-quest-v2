#!/usr/bin/env python3
"""desert_tex.py : artwork of the film-8 sets (Persia c. 1600: the yakhchal ice works in the desert, the bazaar of the town).
Patterned surfaces are drawn as SVG in Python and rasterised by headless Chromium (PROJ/v3/set3d/raster.js), exactly as
louvre_tex / bakery_tex; the skies (night sky with ~9000 stars and the Milky Way, dawn, noon, summer) are painted with numpy + PIL
(smooth gradients and star fields are cheaper and sharper that way). All cached in v3/set3d8/tex_desert/ by content hash.

    import desert_tex as DT
    paths = DT.ensure()        # {name: png path}
    DT.SIZE[name] -> (w_D, h_D)

Sky images are the sky-dome UV space of louvre._sky_dome: u = azimuth / 360 (0 = +x, counter-clockwise), v = (elevation + 15) / 105.
Deterministic: every random choice comes from random.Random / numpy RandomState with fixed seeds."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower_tex as TT                                                     # noqa: E402
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401
import pagoda_tex as PT                                                    # noqa: E402
import bakery_tex as BT                                                    # noqa: E402
import louvre_tex as LT                                                    # noqa: E402

TEX = os.path.join(HERE, 'tex_desert'); WORK = os.path.join(HERE, 'desert_work')
SIZE = TT.SIZE; job = TT.job
PY = {}                                    # python-painted textures: name -> (params, painter)
SKY_V = 'sky8'                             # bump to repaint the skies

# ============================================================================= ground, walls, dome
def sand(name='sand', base='#d89a5e', seed=3, W=4.0, H=4.0, ppd=96):
    """Desert floor 4 x 4 D: warm sand with wind ripples (soft darker/lighter wavy bands), grit and small pebbles."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for k in range(26):
        y0 = k * H / 26 + r.uniform(-0.03, 0.03); ph = r.uniform(0, 6.3); pts = [(x * W / 40, y0 + 0.05 * math.sin(ph + x * 0.55) + 0.02 * math.sin(x * 1.7)) for x in range(41)]
        o.append(pline(pts, mul(base, 0.86), 0.035, op=0.55)); o.append(pline([(x, y + 0.04) for x, y in pts], mix(base, '#fff2d8', 0.35), 0.02, op=0.5))
    for _ in range(260):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(circ(x, y, r.uniform(0.006, 0.02), r.choice((mul(base, 0.7), mul(base, 0.8), mix(base, '#ffffff', 0.3))), op=0.8))
    for _ in range(24):
        x, y = r.uniform(0, W), r.uniform(0, H); w = r.uniform(0.04, 0.09); c = r.choice(('#9a7a5a', '#b08a62', '#7a6450', '#c8a07a'))
        for xx in _wrap(x, W, w): o.append(ell(xx, y, w, w * 0.65, c, stroke='#5a4030', sw=0.006)); o.append(ell(xx - w * 0.2, y - w * 0.2, w * 0.4, w * 0.25, mix(c, '#ffffff', 0.35), op=0.7))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def earth(name='bank', base='#b88a5a', seed=5, W=4.0, H=4.0, ppd=96, cracks=True):
    """Packed earth of the channel banks / paths 4 x 4 D: trodden clay with crack polygons, footprints, straw bits."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.2, 0.6), r.uniform(0.1, 0.3), r.choice((mul(base, 0.9), mix(base, '#fff0d0', 0.15))), op=0.5))
    if cracks:
        for _ in range(30):
            x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
            for k in range(r.randint(3, 6)): x += r.uniform(-0.25, 0.25); y += r.uniform(-0.25, 0.25); pts.append((x, y))
            o.append(pline(pts, mul(base, 0.55), 0.012, op=0.8))
    for _ in range(14):
        x, y = r.uniform(0.2, W - 0.2), r.uniform(0.2, H - 0.2); a = r.uniform(0, 6.3)
        o.append(f'<g transform="translate({_c(x)} {_c(y)}) rotate({_c(math.degrees(a))})">' + ell(0, 0, 0.09, 0.2, mul(base, 0.8), op=0.6) + ell(0, -0.17, 0.08, 0.07, mul(base, 0.75), op=0.6) + '</g>')
    for _ in range(80):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.3); o.append(line(x, y, x + 0.12 * math.cos(a), y + 0.12 * math.sin(a), '#e8c878', 0.01, op=0.7))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def mudbrick(name='mudbrick', base='#c07c4e', seed=11, W=4.0, H=4.0, ppd=96, plaster=0.35):
    """Sun-dried mud-brick (khesht) wall 4 x 4 D: square-ish bricks in courses with thick mud joints, eroded corners, patches of
    straw-mud plaster (kahgel) over them, rain streaks running down, putlog holes."""
    r = random.Random(seed); J = mul(base, 0.72); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, J)]
    bh = 0.26; y = 0.0; row = 0
    while y < H - 1e-6:
        x = -0.2 if row % 2 else 0.0
        while x < W:
            w = r.uniform(0.42, 0.52); c = mul(r.choice((base, mix(base, '#d8a870', 0.4), mul(base, 0.92), mix(base, '#a87048', 0.4))), r.uniform(0.94, 1.06))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.03, y + 0.03, w - 0.06, bh - 0.06, c, rx=0.04))
                o.append(rect(xx + 0.05, y + 0.04, w - 0.12, 0.04, mix(c, '#ffe8c0', 0.25), op=0.7))
            x += w
        y += bh; row += 1
    for _ in range(7):                                           # plaster patches
        x, y = r.uniform(0, W), r.uniform(0, H); w, h = r.uniform(0.6, 1.6), r.uniform(0.4, 1.0); c = mix(base, '#d8aa78', 0.5)
        pts = [(x + w * math.cos(a) * r.uniform(0.7, 1.0), y + h * math.sin(a) * r.uniform(0.7, 1.0)) for a in [k * 0.5 for k in range(13)]]
        if plaster > 0: o.append(poly(pts, c, op=plaster + 0.4))
    for _ in range(40):
        x = r.uniform(0, W); y = r.uniform(0, H * 0.6); o.append(line(x, y, x + r.uniform(-0.02, 0.02), y + r.uniform(0.3, 1.2), mul(base, 0.8), 0.02, op=0.35))
    for _ in range(3):
        x, y = r.uniform(0.2, W - 0.3), r.uniform(0.2, H - 0.3); o.append(rect(x, y, 0.16, 0.16, '#3a2414')); o.append(rect(x, y, 0.16, 0.04, '#1e120a'))
    for _ in range(120):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.3); o.append(line(x, y, x + 0.08 * math.cos(a), y + 0.08 * math.sin(a), '#e8c070', 0.008, op=0.6))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def kahgel(name='kahgel', base='#c47c50', seed=13, W=4.0, H=4.0, ppd=80):
    """Straw-mud plaster of the dome 4 x 4 D: smooth trowelled mud, hand-swept arcs, straw flecks, darker rain runs, a few cracks."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    for _ in range(36):
        x, y = r.uniform(0, W), r.uniform(0, H); rr = r.uniform(0.2, 0.6); a0 = r.uniform(0, 6.3)
        o.append(path(f'M{_c(x + rr * math.cos(a0))},{_c(y + rr * math.sin(a0))} A{_c(rr)},{_c(rr)} 0 0 1 {_c(x + rr * math.cos(a0 + 1.6))},{_c(y + rr * math.sin(a0 + 1.6))}', 'none', stroke=r.choice((mul(base, 0.88), mix(base, '#f0d0a0', 0.3))), sw=0.05, op=0.5))
    for _ in range(30):
        x = r.uniform(0, W); y = r.uniform(0, H); o.append(line(x, y, x + r.uniform(-0.03, 0.03), y + r.uniform(0.4, 1.5), mul(base, 0.82), 0.03, op=0.35))
    for _ in range(260):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.3); o.append(line(x, y, x + 0.07 * math.cos(a), y + 0.07 * math.sin(a), '#ecc878', 0.008, op=0.75))
    for _ in range(6):
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(5): x += r.uniform(-0.15, 0.15); y += r.uniform(0.05, 0.2); pts.append((x, y))
        o.append(pline(pts, mul(base, 0.5), 0.012, op=0.8))
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= ice, water, mud (the channel states)
def ice_thin(name='ice_thin', seed=21, W=4.0, H=2.0, ppd=160):
    """The first night's ice, 4 x 2 D, TRANSPARENT: a glassy veil (alpha 0.18) over the dark water, feathery frost needles growing
    from seed points (white, alpha 0.8), a whiter rim along both banks (v 0 and 1), a few round air bubbles."""
    r = random.Random(seed); g = '<linearGradient id="e" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4fbff" stop-opacity="0.85"/><stop offset="0.1" stop-color="#e8f4ff" stop-opacity="0.04"/>' \
        '<stop offset="0.9" stop-color="#e8f4ff" stop-opacity="0.04"/><stop offset="1" stop-color="#f4fbff" stop-opacity="0.85"/></linearGradient>'
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#dceeff', op=0.07), rect(-0.1, 0, W + 0.2, H, 'url(#e)')]
    def needle(x, y, a, L, depth, sw):
        x1, y1 = x + L * math.cos(a), y + L * math.sin(a)
        for xx in _wrap(min(x, x1) - 0.01, W, abs(x1 - x) + 0.02):
            dx = xx - (min(x, x1) - 0.01); o.append(line(x + dx, y, x1 + dx, y1, '#ffffff', sw, op=0.75))
        if depth > 0:
            for k in range(1, 4):
                t = k / 4; px, py = x + (x1 - x) * t, y + (y1 - y) * t
                for s in (-1, 1): needle(px, py, a + s * r.uniform(0.6, 1.1), L * r.uniform(0.25, 0.4), depth - 1, sw * 0.65)
    for _ in range(14):
        x, y = r.uniform(0, W), r.choice((r.uniform(0, 0.35), r.uniform(H - 0.35, H), r.uniform(0, H)))
        for k in range(r.randint(3, 6)): needle(x, y, r.uniform(0, 6.3), r.uniform(0.15, 0.45), 2, 0.012)
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(circ(x, y, r.uniform(0.008, 0.025), 'none', stroke='#ffffff', sw=0.005, op=0.7))
    for _ in range(5):                                           # long hair-line fractures across the sheet
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(8): x += r.uniform(0.1, 0.3); y += r.uniform(-0.12, 0.12); pts.append((x, y))
        o.append(pline(pts, '#ffffff', 0.006, op=0.55))
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=g, transparent=True)

def ice_thick(name='ice_thick', seed=23, W=4.0, H=2.0, ppd=128):
    """Night ten's ice, 4 x 2 D, opaque: white-blue slab with milky cloud patches, a pale frost skin, long cracks (blue-dark with a
    white edge), trapped bubble strings, the cut lines of yesterday's harvest."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#bcdcf0')]
    for _ in range(36):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.2, 0.7), r.uniform(0.1, 0.35), r.choice(('#e8f6ff', '#a4cce8', '#f4fbff', '#9cc4e4')), op=0.55))
    for _ in range(9):
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(r.randint(5, 10)): x += r.uniform(0.08, 0.3) * r.choice((1, -1)); y += r.uniform(-0.15, 0.15); pts.append((x, y))
        o.append(pline(pts, '#4a7aa8', 0.016, op=0.8)); o.append(pline([(a + 0.012, b + 0.012) for a, b in pts], '#ffffff', 0.01, op=0.9))
    for _ in range(14):
        x, y = r.uniform(0, W), r.uniform(0, H)
        for k in range(r.randint(3, 8)): o.append(circ(x + k * 0.03, y + r.uniform(-0.015, 0.015), r.uniform(0.008, 0.02), '#ffffff', stroke='#7aa4c8', sw=0.004, op=0.9))
    for x in (1.0, 2.0, 3.0): o.append(line(x, 0, x + 0.02, H, '#7aa8d0', 0.02, op=0.45))
    o.append(rect(-0.1, 0, W + 0.2, 0.08, '#f4fbff', op=0.8)); o.append(rect(-0.1, H - 0.08, W + 0.2, 0.08, '#f4fbff', op=0.8))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def mud(name='mud', seed=25, W=4.0, H=2.0, ppd=128):
    """The overslept channel at noon, 4 x 2 D: brown wet mud and grey slush with sagging leftover ice crumbs, footprints, a dead
    scrap of straw; PUDDLES are transparent holes (the water plane below shows through and reflects the sky)."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#6a4a30')]
    for _ in range(50):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.1, 0.5), r.uniform(0.06, 0.25), r.choice(('#7a5638', '#5a3e28', '#8a6a4a', '#4e3622', '#8a7a68')), op=0.6))
    for _ in range(30):                                          # grey slush crumbs
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.03, 0.1), r.uniform(0.02, 0.06), '#b8c0c0', stroke='#5a4a3a', sw=0.006, op=0.85))
    for _ in range(10):
        x, y = r.uniform(0.2, W - 0.2), r.uniform(0.3, H - 0.3)
        o.append(f'<g transform="translate({_c(x)} {_c(y)}) rotate({_c(r.uniform(0, 360))})">' + ell(0, 0, 0.1, 0.22, '#3e2a18', op=0.7) + ell(0, -0.2, 0.09, 0.08, '#3e2a18', op=0.7) + '</g>')
    msk = []                                                     # puddles (holes), with a light wet rim drawn on the mud
    for _ in range(9):
        x, y = r.uniform(0.2, W - 0.2), r.uniform(0.25, H - 0.25); rx, ry = r.uniform(0.15, 0.45), r.uniform(0.08, 0.22)
        pts = [(x + rx * math.cos(a) * r.uniform(0.75, 1.0), y + ry * math.sin(a) * r.uniform(0.75, 1.0)) for a in [k * 0.45 for k in range(14)]]
        o.append(poly(pts, 'none', stroke='#a89070', sw=0.03, op=0.8)); msk.append(poly(pts, '#000000'))
    d = '<mask id="pm"><rect x="-1" y="-1" width="9" height="9" fill="#fff"/>' + ''.join(msk) + '</mask>'
    job(name, 0, 0, W, H, ppd, '<g mask="url(#pm)">' + ''.join(o) + '</g>', defs=d, transparent=True)

def ice_block(name='ice_block', seed=27, W=2.0, H=2.0, ppd=96):
    """A sawn ice block face 2 x 2 D: blue-white with frozen layers (thin horizontal bands), saw striations, chips at the edges."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#c8e2f2')]
    for k in range(9): y = k * H / 9 + r.uniform(-0.04, 0.04); o.append(rect(-0.1, y, W + 0.2, r.uniform(0.03, 0.09), r.choice(('#e8f6ff', '#a8cce6', '#f6fcff')), op=0.7))
    for _ in range(26): x = r.uniform(0, W); o.append(line(x, 0, x + r.uniform(-0.3, 0.3), H, '#ffffff', 0.008, op=0.4))
    for _ in range(18): o.append(circ(r.uniform(0, W), r.uniform(0, H), r.uniform(0.01, 0.03), '#ffffff', op=0.8))
    for _ in range(4):
        x, y = r.uniform(0, W), r.uniform(0, H); pts = [(x, y)]
        for k in range(5): x += r.uniform(-0.2, 0.2); y += r.uniform(0.05, 0.2); pts.append((x, y))
        o.append(pline(pts, '#5a8ab8', 0.012, op=0.7))
    o.append(rect(0, 0, W, H, 'none', stroke='#f4fbff', sw=0.06, op=0.8))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def wisp(name='wisp', seed=31, W=2.0, H=8.0, ppd=40):
    """Heat wisp 2 x 8 D (transparent, PERIODIC in v): five thin sinuous shimmering ribbons rising, the material scrolls them up and
    fades them at both ends (bakery._mat_add scroll/fade)."""
    r = random.Random(seed); g = '<filter id="b" x="-50%" y="-5%" width="200%" height="110%"><feGaussianBlur stdDeviation="0.035"/></filter>'
    o = []
    for k in range(6):
        x0 = 0.2 + 0.3 * k; ph = r.uniform(0, 6.28); cyc = r.choice((2, 3)); pts = []
        for i in range(-4, 85):
            t = i / 80; y = H - t * H; x = x0 + 0.12 * math.sin(ph + 2 * math.pi * cyc * t) + 0.05 * math.sin(2 * ph + 2 * math.pi * 7 * t); pts.append((x, y))
        dd = 'M' + ' L'.join(f'{_c(x)},{_c(y)}' for x, y in pts)
        o.append(f'<path d="{dd}" fill="none" stroke="#ffffff" stroke-opacity="{_c(0.9 - 0.08 * k)}" stroke-width="{_c(0.07 - 0.006 * k)}" stroke-linecap="round" filter="url(#b)"/>')
    job(name, 0, 0, W, H, ppd, ''.join(o), defs=g, transparent=True)

def straw_mat(name='mat', W=2.0, H=2.0, ppd=96):
    """Reed / straw mat (the dome door curtain, the covers on the ice): woven bands."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#c8a060')]
    for i in range(int(H / 0.08)):
        y = i * 0.08; o.append(rect(-0.1, y, W + 0.2, 0.04, '#b08848' if i % 2 else '#d8b070'))
    for i in range(int(W / 0.3)): o.append(line(i * 0.3, 0, i * 0.3, H, '#7a5a30', 0.012))
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= bazaar
TQ = '#2a9ab0'; TQD = '#1a5a8a'; LAP = '#1e3a7a'; CREAM = '#f0e2c0'; GOLD = '#e0b040'; BRK = '#d8a868'

def pbrick(name='pbrick', base='#d4a46a', seed=41, W=4.0, H=4.0, ppd=96):
    """Persian fired brick 4 x 4 D: long thin yellow bricks in stretcher bond, recessed light joints, a few darker / glazed ones."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mix(base, '#f0e0c0', 0.45))]
    bh = 0.16; y = 0.0; row = 0
    while y < H - 1e-6:
        x = -0.27 if row % 2 else 0.0
        while x < W:
            w = 0.54; c = mul(r.choice((base, mix(base, '#c08048', 0.4), mix(base, '#e8c890', 0.3))), r.uniform(0.93, 1.05))
            if r.random() < 0.02: c = TQ
            for xx in _wrap(x, W, w): o.append(rect(xx + 0.02, y + 0.02, w - 0.04, bh - 0.04, c))
            x += w
        y += bh; row += 1
    job(name, 0, 0, W, H, ppd, ''.join(o))

def _star8(cx, cy, R, fill, stroke=None, sw=0.0):
    pts = []
    for k in range(16):
        a = math.pi * k / 8 + math.pi / 16; rr = R if k % 2 == 0 else R * 0.62; pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, fill, stroke=stroke, sw=sw)

def tile_band(name='tile_band', W=4.0, H=0.6, ppd=160, ground=LAP, seed=43):
    """Glazed tile frieze 4 x 0.6 D: cobalt ground, white-turquoise 8-point stars and crosses (girih), yellow arabesque scrolls,
    framed by turquoise and white rules."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, ground)]
    for i in range(9):
        cx = i * 0.5; o.append(_star8(cx, H / 2, 0.2, '#f4f0e0', stroke=TQ, sw=0.02)); o.append(_star8(cx, H / 2, 0.11, TQ))
        o.append(circ(cx, H / 2, 0.04, GOLD)); x2 = cx + 0.25
        o.append(path(f'M{_c(x2 - 0.12)},{_c(H / 2)} Q{_c(x2)},{_c(H / 2 - 0.18)} {_c(x2 + 0.12)},{_c(H / 2)} Q{_c(x2)},{_c(H / 2 + 0.18)} {_c(x2 - 0.12)},{_c(H / 2)} Z', GOLD, stroke='#f4f0e0', sw=0.01))
    for y in (0.02, H - 0.06): o.append(rect(-0.1, y, W + 0.2, 0.04, TQ)); o.append(rect(-0.1, y + (0.04 if y < 0.1 else -0.015), W + 0.2, 0.015, '#f4f0e0'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def tile_panel(name='tile_panel', W=2.0, H=2.0, ppd=128, ground=TQD, seed=45):
    """Arabesque tile panel 2 x 2 D (arch spandrels, iwan faces): a lattice of 8-point stars and crosses in turquoise / white / cobalt,
    yellow flowers at the nodes, a white rule border."""
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, ground)]
    n = 4; s = W / n
    for i in range(n + 1):
        for j in range(n + 1):
            cx, cy = i * s, j * s; o.append(_star8(cx, cy, s * 0.42, '#f4f0e0')); o.append(_star8(cx, cy, s * 0.3, TQ)); o.append(circ(cx, cy, s * 0.1, GOLD))
            if i < n and j < n:
                mx_, my_ = cx + s / 2, cy + s / 2; o.append(poly([(mx_, my_ - s * 0.22), (mx_ + s * 0.22, my_), (mx_, my_ + s * 0.22), (mx_ - s * 0.22, my_)], LAP, stroke='#f4f0e0', sw=0.015))
                for a in range(4): o.append(circ(mx_ + 0.12 * s * math.cos(a * 1.57), my_ + 0.12 * s * math.sin(a * 1.57), 0.04 * s, '#e86a3a'))
    o.append(rect(0.02, 0.02, W - 0.04, H - 0.04, 'none', stroke='#f4f0e0', sw=0.04))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def carpet(name, field, border, accent, seed, W=2.0, H=3.0, ppd=110, style=0):
    """Persian carpet W x H D: field colour with a central medallion (style 0), an all-over boteh / lattice (1) or stripes of
    guls (2); main border with a running vine between two guard stripes; fringes at both ends."""
    r = random.Random(seed); o = [rect(0, 0, W, H, field)]
    bw = 0.22; o.append(rect(0.05, 0.08, W - 0.1, H - 0.16, 'none', stroke=border, sw=bw))
    o.append(rect(0.05 + bw / 2 + 0.02, 0.08 + bw / 2 + 0.02, W - 0.14 - bw, H - 0.2 - bw, 'none', stroke=accent, sw=0.025))
    o.append(rect(0.05 - bw / 2 + 0.01, 0.08 - bw / 2 + 0.01, W - 0.12 + bw, H - 0.18 + bw, 'none', stroke=accent, sw=0.02))
    for k in range(int((W + H) * 2 / 0.25)):                     # vine dots in the border
        t = k * 0.25; per = 2 * (W - 0.1) + 2 * (H - 0.16)
        t %= per
        if t < W - 0.1: x, y = 0.05 + t, 0.08
        elif t < W - 0.1 + H - 0.16: x, y = W - 0.05, 0.08 + t - (W - 0.1)
        elif t < 2 * (W - 0.1) + H - 0.16: x, y = W - 0.05 - (t - (W - 0.1) - (H - 0.16)), H - 0.08
        else: x, y = 0.05, H - 0.08 - (t - 2 * (W - 0.1) - (H - 0.16))
        o.append(circ(x, y, 0.04, accent)); o.append(circ(x, y, 0.017, field))
    cx, cy = W / 2, H / 2; ix0, iy0, iw, ih = 0.3, 0.33, W - 0.6, H - 0.66
    if style == 0:
        o.append(poly([(cx, cy - ih * 0.36), (cx + iw * 0.36, cy), (cx, cy + ih * 0.36), (cx - iw * 0.36, cy)], border, stroke=accent, sw=0.03))
        o.append(poly([(cx, cy - ih * 0.22), (cx + iw * 0.22, cy), (cx, cy + ih * 0.22), (cx - iw * 0.22, cy)], accent))
        o.append(_star8(cx, cy, iw * 0.12, field)); o.append(circ(cx, cy, iw * 0.04, border))
        for sx in (-1, 1):
            for sy in (-1, 1): o.append(path(f'M{_c(cx + sx * iw / 2)},{_c(cy + sy * ih / 2)} l{_c(-sx * iw * 0.22)},0 q{_c(sx * iw * 0.1)},{_c(-sy * ih * 0.08)} {_c(sx * iw * 0.22)},{_c(-sy * ih * 0.18)} Z', border, stroke=accent, sw=0.02))
    elif style == 1:
        for i in range(5):
            for j in range(8):
                x = ix0 + (i + 0.5 + 0.5 * (j % 2)) * iw / 5.5; y = iy0 + (j + 0.5) * ih / 8
                o.append(path(f'M{_c(x)},{_c(y + 0.09)} q{_c(-0.09)},{_c(-0.05)} {_c(-0.01)},{_c(-0.15)} q{_c(0.05)},{_c(-0.05)} {_c(0.06)},{_c(0.0)} q{_c(0.04)},{_c(0.1)} {_c(-0.05)},{_c(0.15)} Z', r.choice((accent, border, '#f0e2c0'))))
    else:
        for j in range(5):
            y = iy0 + (j + 0.5) * ih / 5; o.append(rect(ix0, y - 0.03, iw, 0.06, accent, op=0.6))
            for i in range(3):
                x = ix0 + (i + 0.5) * iw / 3; o.append(poly([(x, y - 0.17), (x + 0.22, y), (x, y + 0.17), (x - 0.22, y)], border, stroke=accent, sw=0.02)); o.append(circ(x, y, 0.05, accent))
    for e in (0.0, H - 0.08):
        for k in range(int(W / 0.05)): o.append(rect(k * 0.05 + 0.01, e, 0.025, 0.08, '#f0e6d0'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def kilim(name='kilim', seed=51, W=2.0, H=2.0, ppd=96):
    """Flat-woven kilim 2 x 2 D (stall covers, cushions): bands of stepped lozenges, red / orange / indigo / cream."""
    r = random.Random(seed); cols = ('#b8382a', '#e08a30', '#2a3a6a', '#f0e2c0', '#6a2a2a', '#3a6a5a'); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#8a2a22')]
    y = 0.0
    while y < H:
        h = r.uniform(0.15, 0.35); c = r.choice(cols); o.append(rect(-0.1, y, W + 0.2, h, c)); c2 = r.choice(cols)
        for i in range(int(W / 0.3) + 1): x = i * 0.3 + 0.15; o.append(poly([(x, y + 0.03), (x + 0.1, y + h / 2), (x, y + h - 0.03), (x - 0.1, y + h / 2)], c2))
        y += h
    job(name, 0, 0, W, H, ppd, ''.join(o))

def pavers(name='pavers', seed=53, W=4.0, H=4.0, ppd=80):
    """Bazaar floor 4 x 4 D: square fired-brick pavers laid on the diagonal-free grid, worn, dusty, straw and peel litter."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#9a7454')]
    s = 0.5
    for i in range(8):
        for j in range(8):
            c = mul(r.choice(('#c89a6a', '#d0a674', '#b88a5c', '#c4946a', '#d8b080')), r.uniform(0.92, 1.05)); o.append(rect(i * s + 0.025, j * s + 0.025, s - 0.05, s - 0.05, c, rx=0.03))
            o.append(rect(i * s + 0.05, j * s + 0.04, s - 0.12, 0.05, mix(c, '#fff0d0', 0.3), op=0.6))
    for _ in range(18): o.append(ell(r.uniform(0, W), r.uniform(0, H), r.uniform(0.2, 0.6), r.uniform(0.1, 0.3), '#e8c890', op=0.25))
    for _ in range(60):
        x, y = r.uniform(0, W), r.uniform(0, H); a = r.uniform(0, 6.3); o.append(line(x, y, x + 0.1 * math.cos(a), y + 0.1 * math.sin(a), '#e8c878', 0.01, op=0.7))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def lattice(name='lattice', W=1.0, H=1.0, ppd=160):
    """Wooden window lattice (mashrabiya-like) 1 x 1 D, transparent holes."""
    o = [rect(0, 0, W, H, 'none', stroke='#4a2a18', sw=0.06)]
    for i in range(1, 6):
        t = i / 6; o.append(line(t, 0, t, H, '#4a2a18', 0.03)); o.append(line(0, t, W, t, '#4a2a18', 0.03))
    for i in range(5):
        for j in range(5): o.append(circ((i + 1) / 6, (j + 1) / 6, 0.035, '#4a2a18'))
    job(name, 0, 0, W, H, ppd, ''.join(o), transparent=True)

def shopfront(name, seed, W=3.0, H=3.6, ppd=72):
    """Back wall of a shop niche 3 x 3.6 D (seen through the arch, in lamp glow): shelves of copper, jars, bolts of cloth, sacks."""
    r = random.Random(seed); o = [rect(0, 0, W, H, '#5a3a24')]
    for k, y in enumerate((0.9, 1.75, 2.6)):
        o.append(rect(0, H - y, W, 0.07, '#8a5a34'))
        x = 0.1
        while x < W - 0.25:
            kind = r.choice(('pot', 'jar', 'cloth', 'bowl', 'pot')); w = r.uniform(0.22, 0.42)
            if kind == 'pot': c = r.choice(('#c06a30', '#d8843c', '#a85a2a')); o.append(ell(x + w / 2, H - y - w * 0.4, w / 2, w * 0.4, c, stroke='#3a1e10', sw=0.012)); o.append(ell(x + w * 0.38, H - y - w * 0.52, w * 0.12, w * 0.08, '#ffd0a0', op=0.8))
            elif kind == 'jar': c = r.choice(('#b86a40', '#c88a5a', '#2a7a9a')); o.append(path(f'M{_c(x + w * 0.3)},{_c(H - y)} q{_c(-w * 0.3)},{_c(-w * 0.5)} {_c(w * 0.1)},{_c(-w * 1.0)} l{_c(w * 0.3)},0 q{_c(w * 0.4)},{_c(w * 0.5)} {_c(w * 0.1)},{_c(w * 1.0)} Z', c, stroke='#3a1e10', sw=0.012))
            elif kind == 'cloth': c = r.choice(('#a82a2a', '#2a4a8a', '#e0a030', '#3a7a4a', '#7a2a6a')); o.append(rect(x, H - y - 0.5, w, 0.5, c, stroke='#2a1a10', sw=0.01)); o.append(rect(x, H - y - 0.42, w, 0.04, mix(c, '#ffffff', 0.4)))
            else: o.append(ell(x + w / 2, H - y - 0.06, w / 2, 0.07, '#e0b050', stroke='#3a1e10', sw=0.01))
            x += w + 0.04
    o.append(rect(0, H - 0.4, W, 0.4, '#3a2416'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def lantern_tex(name='lantern_p', W=1.0, H=1.0, ppd=128):
    """Pierced-brass lantern glass (emission): warm glow with dark pierced star pattern (the brass shell)."""
    o = [rect(0, 0, W, H, '#3a2210')]
    for i in range(5):
        for j in range(5):
            cx, cy = (i + 0.5) / 5, (j + 0.5) / 5; o.append(_star8(cx, cy, 0.07, '#ffd890')); o.append(circ(cx, cy, 0.025, '#fff4d0'))
    for i in range(4):
        for j in range(4): o.append(circ((i + 1) / 5, (j + 1) / 5, 0.022, '#ffb860'))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def calligraphy(name='kufic', W=4.0, H=0.5, ppd=160):
    """Square-kufic-like ornamental band 4 x 0.5 D (NOT readable text: an abstract interlace of verticals and hooks, cream on cobalt)."""
    r = random.Random(61); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, LAP)]
    x = 0.05
    while x < W:
        h = r.choice((0.3, 0.2, 0.35)); o.append(rect(x, H - 0.08 - h, 0.04, h, '#f4ecd0'))
        if r.random() < 0.5: o.append(rect(x, H - 0.12, r.uniform(0.08, 0.2), 0.04, '#f4ecd0'))
        if r.random() < 0.3: o.append(circ(x + 0.06, 0.12, 0.025, GOLD))
        x += r.uniform(0.07, 0.13)
    o.append(rect(-0.1, H - 0.05, W + 0.2, 0.03, TQ)); o.append(rect(-0.1, 0.02, W + 0.2, 0.03, TQ))
    job(name, 0, 0, W, H, ppd, ''.join(o))

# ============================================================================= panoramas (painted rings at R 120, transparent above)
PANO_R = 120.0; PANO_Z0, PANO_Z1 = -1.5, 34.0
PAN = dict(
    NIGHT=dict(far='#1e2a5a', mid='#182250', near='#141c40', town='#1a2048', win='#ffb048', win_p=0.35, dune='#2a3466', rim='#4a5aa0', palm='#10163a'),
    DAWN=dict(far='#a86a8a', mid='#8a5a74', near='#6a4a60', town='#7a4e5e', win='#ffb860', win_p=0.15, dune='#d08a6a', rim='#ffc890', palm='#3a2a3a'),
    NOON=dict(far='#a8a4c0', mid='#c09a7a', near='#b4845a', town='#d8b88a', win='#3a2a20', win_p=0.0, dune='#e0b47a', rim='#fff0d0', palm='#4a6a3a'),
    SUMMER=dict(far='#d8c8c0', mid='#d8b490', near='#c8986a', town='#e4c494', win='#3a2a20', win_p=0.0, dune='#ecc488', rim='#fff8e0', palm='#5a6a3a'),
)

def pano_desert(mode, town=0.25):
    """Desert ring: far blue Zagros ranges, mid ridges, dunes; the mud town (a cluster of domes, windcatchers / badgirs, a minaret
    and palm trees) round azimuth `town` (fraction of the ring); at NIGHT a few warm lamp windows."""
    c = PAN[mode]; r = random.Random(301); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def Y(z): return PANO_Z1 - z
    def ridge(base, amp, n, col, seed, peaks=1.0):
        rr = random.Random(seed); pts = []
        for i in range(n + 1):
            x = W * i / n; z = base + amp * (0.5 + 0.5 * math.sin(i * 0.37 + seed) * math.sin(i * 0.11 + 2 * seed)) * peaks + rr.uniform(0, amp * 0.25)
            pts.append((x, Y(z)))
        pts[-1] = (W, pts[0][1])
        o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], col))
    ridge(5.0, 10.0, 90, c['far'], 3); ridge(3.0, 5.0, 120, c['mid'], 7); ridge(0.6, 1.6, 160, c['dune'], 11)
    # the town
    tx = W * town
    def town_at(cx, s, seed):
        rr = random.Random(seed); x = cx - 26 * s
        while x < cx + 26 * s:
            w = rr.uniform(2.5, 5.0) * s; h = rr.uniform(1.5, 3.2) * s
            o.append(rect(x, Y(h), w, h + 2, c['town'], stroke=mul(c['town'], 0.7), sw=0.08))
            for k in range(int(w / 1.0)):
                if rr.random() < c['win_p']: o.append(rect(x + 0.3 + k * 1.0, Y(h * 0.6), 0.35 * s, 0.45 * s, c['win']))
            if rr.random() < 0.35:                                   # badgir (windcatcher)
                bw = 0.9 * s; o.append(rect(x + w * 0.4, Y(h + 2.6 * s), bw, 2.6 * s, c['town'], stroke=mul(c['town'], 0.7), sw=0.06))
                for k in range(3): o.append(rect(x + w * 0.4 + 0.12 * s + k * 0.26 * s, Y(h + 2.4 * s), 0.12 * s, 1.0 * s, mul(c['town'], 0.6)))
            if rr.random() < 0.3:                                    # dome
                dr = rr.uniform(1.0, 1.8) * s; o.append(path(f'M{_c(x + w / 2 - dr)},{_c(Y(h))} Q{_c(x + w / 2 - dr)},{_c(Y(h + dr * 1.5))} {_c(x + w / 2)},{_c(Y(h + dr * 1.7))} Q{_c(x + w / 2 + dr)},{_c(Y(h + dr * 1.5))} {_c(x + w / 2 + dr)},{_c(Y(h))} Z', c['town'], stroke=mul(c['town'], 0.7), sw=0.06))
            x += w
        o.append(rect(cx + 4 * s, Y(9 * s), 0.8 * s, 9 * s, c['town'], stroke=mul(c['town'], 0.7), sw=0.06)); o.append(rect(cx + 3.7 * s, Y(8 * s), 1.4 * s, 0.4 * s, mul(c['town'], 0.85)))
        dr = 4 * s; o.append(path(f'M{_c(cx - 8 * s - dr)},{_c(Y(4 * s))} Q{_c(cx - 8 * s - dr)},{_c(Y(4 * s + dr * 1.6))} {_c(cx - 8 * s)},{_c(Y(4 * s + dr * 1.9))} Q{_c(cx - 8 * s + dr)},{_c(Y(4 * s + dr * 1.6))} {_c(cx - 8 * s + dr)},{_c(Y(4 * s))} Z', mix(c['town'], '#2a8aa0', 0.35 if mode != 'NIGHT' else 0.15), stroke=mul(c['town'], 0.7), sw=0.08))
        for k in range(7):                                           # palms
            px = cx + rr.uniform(-30, 30) * s; ph = rr.uniform(3, 5) * s; o.append(line(px, Y(0), px + 0.3 * s, Y(ph), c['palm'], 0.25 * s))
            for a in range(7):
                ang = math.pi * (0.1 + 0.8 * a / 6); o.append(path(f'M{_c(px + 0.3 * s)},{_c(Y(ph))} q{_c(1.2 * s * math.cos(ang))},{_c(-1.0 * s * math.sin(ang))} {_c(2.0 * s * math.cos(ang))},{_c(0.3 * s)}', 'none', stroke=c['palm'], sw=0.2 * s))
    town_at(tx, 0.9, 41); town_at(tx + W * 0.47, 0.5, 43)
    for k in range(int(W / 4)):                                      # dune crest highlights
        x = r.uniform(0, W); z = r.uniform(0.0, 1.0); o.append(line(x, Y(z), x + r.uniform(2, 6), Y(z + 0.3), c['rim'], 0.06, op=0.35))
    job('pano_' + mode, 0, 0, W, H, 7.0, ''.join(o), transparent=True)

def pano_town(mode):
    """Bazaar ring: the town wall with round towers and crenels, behind it turquoise domes, minarets, windcatchers, far mountains."""
    c = PAN[mode]; r = random.Random(331); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def Y(z): return PANO_Z1 - z
    pts = [(W * i / 80, Y(8 + 8 * (0.5 + 0.5 * math.sin(i * 0.41) * math.sin(i * 0.13)))) for i in range(81)]; pts[-1] = (W, pts[0][1])
    o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], c['far']))
    x = 0.0
    while x < W:
        w = r.uniform(3, 7); h = r.uniform(5, 11); col = mix(c['town'], c['far'], 0.25)
        o.append(rect(x, Y(h), w, h + 2, col))
        if r.random() < 0.3:
            dr = r.uniform(1.6, 3.2); tq = mix(col, '#2aa0b8', 0.55 if mode != 'NIGHT' else 0.25)
            o.append(path(f'M{_c(x + w / 2 - dr)},{_c(Y(h))} Q{_c(x + w / 2 - dr)},{_c(Y(h + dr * 1.5))} {_c(x + w / 2)},{_c(Y(h + dr * 1.9))} Q{_c(x + w / 2 + dr)},{_c(Y(h + dr * 1.5))} {_c(x + w / 2 + dr)},{_c(Y(h))} Z', tq, stroke=mul(tq, 0.6), sw=0.1))
        if r.random() < 0.12: o.append(rect(x + w * 0.7, Y(h + 9), 0.9, 9, col, stroke=mul(col, 0.7), sw=0.06)); o.append(rect(x + w * 0.7 - 0.3, Y(h + 7.5), 1.5, 0.5, mul(col, 0.8)))
        if r.random() < 0.3: o.append(rect(x + w * 0.2, Y(h + 2.5), 1.0, 2.5, col)); o.append(rect(x + w * 0.2 + 0.15, Y(h + 2.2), 0.7, 1.0, mul(col, 0.55)))
        for k in range(int(w)):
            if r.random() < c['win_p']: o.append(rect(x + 0.4 + k, Y(h * 0.5), 0.4, 0.5, c['win']))
        x += w
    wc = c['town']; o.append(rect(-1, Y(5.0), W + 2, 7, wc, stroke=mul(wc, 0.7), sw=0.08))   # the town wall
    for i in range(int(W / 1.4)): o.append(rect(i * 1.4, Y(5.8), 0.8, 0.8, wc))
    for i in range(int(W / 14)):
        tx_ = i * 14 + 3; o.append(rect(tx_, Y(7.0), 3.0, 9, mul(wc, 0.95), stroke=mul(wc, 0.7), sw=0.08))
        for k in range(3): o.append(rect(tx_ + k * 1.1, Y(7.8), 0.7, 0.8, mul(wc, 0.95)))
    job('pano_town_' + mode, 0, 0, W, H, 7.0, ''.join(o), transparent=True)

# ============================================================================= skies (numpy + PIL)
SKY_W = dict(NIGHT=8192, DAWN=4096, NOON=4096, SUMMER=4096)

def _vnoise(rs, H, W, cell):
    """Smooth value noise (bicubic-upsampled random grid), periodic in x."""
    import numpy as np
    from PIL import Image
    gw, gh = max(2, W // cell), max(2, H // cell + 2)
    g = rs.rand(gh, gw).astype('float32')
    g = np.concatenate([g, g[:, :3]], 1)
    im = Image.fromarray(g, mode='F').resize((int(W * (gw + 3) / gw), H), Image.BICUBIC)
    return np.asarray(im)[:, :W]

def _fbm(rs, H, W, cell, oct_=4):
    import numpy as np
    a = np.zeros((H, W), 'float32'); amp = 1.0; tot = 0
    for k in range(oct_): a += amp * _vnoise(rs, H, W, max(4, cell >> k)); tot += amp; amp *= 0.5
    return a / tot

def _sky_paint(mode, out):
    import numpy as np
    from PIL import Image
    W = SKY_W[mode]; H = int(round(W * 105 / 360)); rs = np.random.RandomState({'NIGHT': 7, 'DAWN': 9, 'NOON': 11, 'SUMMER': 13}[mode])
    el = 90.0 - (np.arange(H, dtype='float32') + 0.5) / H * 105.0                 # row 0 = zenith
    az = (np.arange(W, dtype='float32') + 0.5) / W * 2 * math.pi
    E = np.radians(el)[:, None] * np.ones((1, W), 'float32'); A = np.ones((H, 1), 'float32') * az[None, :]
    dx, dy, dz = np.cos(E) * np.cos(A), np.cos(E) * np.sin(A), np.sin(E)
    def grad(stops):
        e = np.clip(el, -15, 90); xs = [s[0] for s in stops]; out_ = np.zeros((H, 3), 'float32')
        for ch in range(3): out_[:, ch] = np.interp(e, xs, [s[1][ch] for s in stops])
        return np.repeat(out_[:, None, :], W, 1)
    def hexf(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def sun_glow(azd, eld, rad, col, k):
        sx, sy, sz = math.cos(math.radians(eld)) * math.cos(math.radians(azd)), math.cos(math.radians(eld)) * math.sin(math.radians(azd)), math.sin(math.radians(eld))
        d = np.degrees(np.arccos(np.clip(dx * sx + dy * sy + dz * sz, -1, 1))); g = np.exp(-(d / rad) ** 2) * k
        return g[..., None] * np.array(hexf(col), 'float32')[None, None, :], d
    if mode == 'NIGHT':
        img = grad([(-15, hexf('#0e1638')), (-1, hexf('#2a4684')), (2, hexf('#3e62a8')), (8, hexf('#2c4c92')), (22, hexf('#1a3070')), (50, hexf('#111f52')), (90, hexf('#0a1440'))])
        g, _ = sun_glow(200.0, -8.0, 40.0, '#3a7ab0', 0.35); img += g                             # faint blue twilight left over in the west
        # the Milky Way: a great circle tilted across the sky (pole n), with fbm clouds, dark dust lanes, a warm core
        n = np.array([-0.55, 0.79, 0.27], 'float32'); n /= np.linalg.norm(n)
        d = dx * n[0] + dy * n[1] + dz * n[2]
        cl = _fbm(rs, H, W, 220, 5); cl2 = _fbm(rs, H, W, 90, 4); lane = _fbm(rs, H, W, 140, 4)
        band = np.exp(-(d / 0.16) ** 2) * (0.55 + 0.9 * (cl - 0.35)) + 0.5 * np.exp(-(d / 0.07) ** 2) * cl2
        dust = np.clip((lane - 0.48) * 4.5, 0, 1) * np.exp(-((d - 0.02) / 0.06) ** 2)
        band = np.clip(band * (1 - 0.85 * dust), 0, None)
        cx_, cy_, cz_ = 0.0, 0.0, 0.0
        cdir = np.array([math.cos(math.radians(22)) * math.cos(math.radians(40)), math.cos(math.radians(22)) * math.sin(math.radians(40)), math.sin(math.radians(22))], 'float32')
        core = np.exp(-((dx * cdir[0] + dy * cdir[1] + dz * cdir[2] - 1) / 0.35) ** 2)
        horizon_fade = np.clip((el[:, None] - 1) / 12, 0, 1)
        mw = (band * horizon_fade)[..., None] * (np.array(hexf('#8aa6e0'), 'float32') * (1 - core[..., None]) + np.array(hexf('#f0d0b0'), 'float32') * core[..., None])
        img += mw * 0.62
        # stars: power-law brightness, a few colour tints, more of them in the band
        sm = np.zeros((H, W), 'float32'); col = np.zeros((H, W, 3), 'float32')
        N = 9000; ys = rs.rand(N); xs = rs.rand(N); bri = rs.pareto(1.7, N) * 0.18 + 0.12
        extra = 4000; ye = rs.rand(extra * 3); xe = rs.rand(extra * 3)
        rows = (ye * H).astype(int).clip(0, H - 1); cols_ = (xe * W).astype(int).clip(0, W - 1)
        keep = np.exp(-(d[rows, cols_] / 0.12) ** 2) > rs.rand(extra * 3)
        ys = np.concatenate([ys, ye[keep][:extra]]); xs = np.concatenate([xs, xe[keep][:extra]]); bri = np.concatenate([bri, rs.pareto(2.2, keep.sum())[:extra] * 0.1 + 0.08])
        tints = [hexf('#ffffff'), hexf('#cfe0ff'), hexf('#fff0d0'), hexf('#ffd8b0'), hexf('#b8d0ff')]
        img_s = np.zeros((H, W, 3), 'float32')
        for y_, x_, b_ in zip(ys, xs, bri):
            Y_ = y_ * H; X_ = x_ * W; e_ = 90 - Y_ / H * 105
            if e_ < 0.5: continue
            b_ = min(b_, 3.0) * (0.4 + 0.6 * min(1, (e_ - 0.5) / 10))
            rad = 0.7 + 0.55 * min(b_, 2.2)
            t = np.array(tints[int(x_ * 1e6) % len(tints)], 'float32')
            x0, x1 = int(X_ - 3 * rad) - 1, int(X_ + 3 * rad) + 2; y0, y1 = max(0, int(Y_ - 3 * rad) - 1), min(H, int(Y_ + 3 * rad) + 2)
            if x0 < 0 or x1 > W: continue
            gx = np.arange(x0, x1) + 0.5 - X_; gy = np.arange(y0, y1) + 0.5 - Y_
            g2 = np.exp(-(gy[:, None] ** 2 + gx[None, :] ** 2) / (2 * (rad * 0.55) ** 2)) * b_
            if b_ > 1.2:                                                                       # sparkle cross on the brightest
                L = int(4 + 4 * b_)
                xa, xb = max(0, int(X_) - L), min(W, int(X_) + L + 1); ya, yb = max(0, int(Y_) - L), min(H, int(Y_) + L + 1)
                img_s[int(Y_), xa:xb] += (np.exp(-np.abs(np.arange(xa, xb) - X_) / (1.5 + b_)) * b_ * 0.5)[:, None] * t
                img_s[ya:yb, int(X_)] += (np.exp(-np.abs(np.arange(ya, yb) - Y_) / (1.5 + b_)) * b_ * 0.5)[:, None] * t
            img_s[y0:y1, x0:x1] += g2[..., None] * t
        img += img_s
    elif mode == 'DAWN':
        img = grad([(-15, hexf('#6a3a5a')), (0, hexf('#f0a070')), (4, hexf('#f4b884')), (12, hexf('#d89a9a')), (25, hexf('#8a7ab8')), (50, hexf('#3e5aa0')), (90, hexf('#1e3478'))])
        g, dd = sun_glow(0.0, 1.0, 22.0, '#ffd090', 0.9); img += g
        g, _ = sun_glow(0.0, 1.0, 60.0, '#ff9a60', 0.35); img += g
        img += (np.exp(-(dd / 2.4) ** 2) * 2.0)[..., None] * np.array(hexf('#fff4d8'), 'float32')
        # long thin pink cloud streaks lit from below
        cl = _fbm(rs, H, W, 200, 4)
        streak = np.clip((cl - 0.55) * 5, 0, 1) * np.exp(-((el[:, None] - 9) / 6) ** 2)
        img = img * (1 - 0.8 * streak[..., None]) + streak[..., None] * np.array(hexf('#ff9a7a'), 'float32') * (0.8 + 0.6 * np.exp(-(dd / 40) ** 2))[..., None]
        # last stars in the west
        img_s = np.zeros_like(img)
        for k in range(2500):
            y_, x_ = rs.rand() * H, rs.rand() * W; e_ = 90 - y_ / H * 105; az_ = x_ / W * 360
            vis = np.clip((e_ - 20) / 50, 0, 1) * np.clip((abs(((az_ + 180) % 360) - 180) - 60) / 80, 0, 1)
            if vis <= 0: continue
            img_s[int(y_), int(x_)] += vis * (0.25 + rs.pareto(2.5) * 0.15)
        img += img_s
    else:
        hot = mode == 'SUMMER'
        if hot: img = grad([(-15, hexf('#d8c8b0')), (0, hexf('#f4ead8')), (6, hexf('#e8e4dc')), (18, hexf('#a8c4e0')), (45, hexf('#5a8ccc')), (90, hexf('#3a6ab8'))])
        else: img = grad([(-15, hexf('#c8c0b8')), (0, hexf('#e8e6e2')), (6, hexf('#c8daec')), (20, hexf('#7aaee0')), (50, hexf('#3e7ccc')), (90, hexf('#2458b0'))])
        sel = 72.0 if hot else 50.0; saz = 270.0                                                # the sun in the south (-y)
        g, dd = sun_glow(saz, sel, 18.0, '#fff4d0', 0.9 if hot else 0.6); img += g
        img += (np.exp(-(dd / 1.6) ** 2) * 3.0)[..., None] * np.array(hexf('#fffaf0'), 'float32')
        if not hot:                                                                             # a few small flat desert clouds
            cl = _fbm(rs, H, W, 160, 5); m = np.clip((cl - 0.6) * 6, 0, 1) * np.clip((el[:, None] - 6) / 6, 0, 1) * np.clip((40 - el[:, None]) / 15, 0, 1)
            img = img * (1 - m[..., None]) + m[..., None] * np.array(hexf('#fbf6ee'), 'float32')
        else:                                                                                   # heat haze: whitened, slightly wavy horizon band
            hz = _fbm(rs, H, W, 60, 3); band = np.exp(-((el[:, None] - 2 - 2 * hz) / 5) ** 2) * 0.4
            img = img * (1 - band[..., None]) + band[..., None] * np.array(hexf('#fff6e4'), 'float32')
    a = np.clip(img, 0, 1) ** (1 / 1.0)
    Image.fromarray((a * 255 + 0.5).astype('uint8'), 'RGB').save(out, optimize=False)

def _py(name, params, fn):
    PY[name] = (json.dumps(params, sort_keys=True), fn); SIZE[name] = (360.0, 105.0)

# ============================================================================= registry
LIGHT_MODES = ('NIGHT', 'DAWN', 'NOON', 'SUMMER')
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear(); PY.clear()
    sand(); sand('sand_d', '#c48650', 4); earth(); earth('path', '#c49464', 6, cracks=False); mudbrick(); mudbrick('mudbrick_d', '#a87650', 12, plaster=0.2); kahgel(); kahgel('kahgel_in', '#a8784e', 14)
    ice_thin(); ice_thick(); mud(); ice_block(); wisp(); straw_mat()
    pbrick(); pbrick('pbrick_l', '#e0b47a', 42); tile_band(); tile_band('tile_band_t', ground=TQD, seed=44); tile_panel(); tile_panel('tile_panel_l', ground=LAP, seed=46); calligraphy()
    for k, (f, b, a, st) in enumerate((('#9a2a24', '#1e2a5a', '#e8c070', 0), ('#1e3460', '#9a2a24', '#f0e0c0', 1), ('#7a1e2a', '#e8b050', '#1e2a4a', 2), ('#c8582a', '#2a1e3a', '#f0d890', 0),
                                       ('#2a4a3a', '#a83424', '#e8c070', 1), ('#e8d8b0', '#8a2a24', '#1e3460', 0))):
        carpet('carpet%d' % k, f, b, a, 900 + k, style=st)
    kilim(); kilim('kilim2', 52); pavers(); lattice(); lantern_tex()
    for k in range(4): shopfront('shop%d' % k, 960 + k)
    BT.awning('awn_red', '#b8302a', '#f2e6cc'); BT.awning('awn_blue', '#1e4a8a', '#f2e6cc'); BT.awning('awn_green', '#2a6a4a', '#f0d890'); BT.awning('awn_ochre', '#d89a30', '#7a2a22')
    BT.shaft('shaft'); PT.pool(); LT.glint(); BT.cloth('cloth_w', '#ece2cc', '#a8b4c0', 182); BT.planks('planks', '#8a6040', 65, n=5); BT.crate('crate', 171)
    for m in LIGHT_MODES:
        pano_desert(m); pano_town(m); _py('sky_' + m, dict(v=SKY_V, mode=m, w=SKY_W[m]), _sky_paint)

def ensure(verbose=True):
    """Draw every texture, rasterise the changed SVGs (one Chromium launch), paint the changed skies; return {name: png path}."""
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
        r = subprocess.run(['node', TT.RASTER, jp], env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')), capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('texture raster failed: ' + r.stderr[-2000:])
        for t in todo:
            try: os.remove(t['src'])
            except OSError: pass
        if verbose: print('textures rasterised:', ', '.join(os.path.basename(t['out']) for t in todo))
    for name, (params, fn) in PY.items():
        h = hashlib.sha1(params.encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            fn(json.loads(params)['mode'], png); man[name] = h
            if verbose: print('painted', name)
    json.dump(man, open(mpath, 'w'), indent=0, sort_keys=True)
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: (os.path.basename(v), SIZE.get(k)) for k, v in p.items()}, indent=0))
