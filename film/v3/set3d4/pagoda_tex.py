#!/usr/bin/env python3
"""pagoda_tex.py : artwork of the film-4 set (old-Japan town, five-storey pagoda, the master builder's rigid tower), drawn as SVG
in Python and rasterised by headless Chromium (PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in
v3/set3d4/tex_pagoda/ by content hash. Same route as v3/set3d2/tower_tex.py and v3/set3d3/harbor_tex.py: tower_tex's SVG helpers
and job() registry are imported, not rewritten.

    import pagoda_tex as PT
    paths = PT.ensure()        # {name: png path}
    PT.SIZE[name] -> (w_D, h_D) of one image / tile

Every surface is drawn in the colour it shows in neutral light; the lit material makes sun and shade of it.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2'))
import tower_tex as TT                                                     # noqa: E402
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401

TEX = os.path.join(HERE, 'tex_pagoda'); WORK = os.path.join(HERE, 'pagoda_work')
RASTER = TT.RASTER; SIZE = TT.SIZE; job = TT.job
INKW = '#2a1712'
RED = '#c8382a'; RED_D = '#8e2420'; GOLD = '#e0b04a'; PLASTER = '#f0e8d6'; WOOD = '#5a3622'; WOOD_D = '#3e2418'
TILE = '#7884a4'; TILE_D = '#5e6480'

# ----------------------------------------------------------------------------- roofs
def kawara(name, base, seed, W=2.0, H=2.0):
    """Hongawara tile roof 2 x 2 D (u along the eave, v up the slope, y down = up the slope in the image): alternating round cover
    rows (lit crest, dark gutter) and flat pan rows, tile laps every 0.33 D."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.8))]; pitch = 0.25; n = int(W / pitch)
    for i in range(n):
        x = i * pitch
        o.append(rect(x + 0.02, -0.1, pitch * 0.5, H + 0.2, mul(base, 0.92)))                      # pan
        for k in range(7):
            y = k * H / 6; o.append(line(x + 0.02, y, x + pitch * 0.52, y, mul(base, 0.68), 0.02))
        cx = x + pitch * 0.76; col = mul(base, r.uniform(0.98, 1.06))                                 # round cover row
        o.append(rect(cx - 0.085, -0.1, 0.17, H + 0.2, col))
        o.append(rect(cx - 0.06, -0.1, 0.05, H + 0.2, mul(col, 1.25)))                               # crest highlight
        o.append(rect(cx + 0.055, -0.1, 0.03, H + 0.2, mul(col, 0.6)))
        for k in range(7):
            y = k * H / 6 + 0.02; o.append(ell(cx, y, 0.088, 0.03, mul(col, 0.72)))
    for _ in range(6):                                                                                 # weathering
        x, y = r.uniform(0, W), r.uniform(0, H)
        for xx in _wrap(x - 0.4, W, 0.8): o.append(ell(xx + 0.4, y, r.uniform(0.2, 0.5), r.uniform(0.15, 0.4), r.choice(('#6a6a5a', '#3e4256')), op=0.18))
    job(name, 0, 0, W, H, 128, ''.join(o))

def rafters():
    """Eave soffit 2 x 2 D: closely spaced rafters (u along the eave) over dark boards, white-painted rafter ends near y = 2."""
    o = [rect(-0.1, -0.1, 2.2, 2.2, '#6a3426')]
    for i in range(10):
        x = i * 0.2 + 0.04; o.append(rect(x, -0.1, 0.11, 2.2, '#b8583a')); o.append(rect(x, -0.1, 0.03, 2.2, '#d87a50'))
    for k in range(4): o.append(line(-0.1, k * 0.5 + 0.25, 2.1, k * 0.5 + 0.25, '#24140e', 0.02, op=0.6))
    job('rafters', 0, 0, 2, 2, 96, ''.join(o))

def bracket():
    """Kumimono bracket band under each pagoda eave 3 x 0.8 D (tiles along the eave): vermilion bearing blocks and arms with
    green and white painted ends and gold caps, dark gaps."""
    W, H = 3.0, 0.8; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#22140e')]
    for k in range(3):
        x = k * 1.0 + 0.5
        o.append(rect(x - 0.42, 0.08, 0.84, 0.16, RED)); o.append(rect(x - 0.42, 0.08, 0.84, 0.04, '#e8604a'))
        for dx in (-0.32, 0.0, 0.32):
            o.append(rect(x + dx - 0.09, 0.0, 0.18, 0.1, GOLD)); o.append(rect(x + dx - 0.07, 0.25, 0.14, 0.12, '#3f8a64'))
        o.append(rect(x - 0.28, 0.38, 0.56, 0.14, RED)); o.append(rect(x - 0.1, 0.52, 0.2, 0.22, RED_D)); o.append(rect(x - 0.13, 0.5, 0.26, 0.05, '#f2ead8'))
        o.append(rect(x - 0.5, 0.74, 1.0, 0.07, '#e8d8b8'))
    job('bracket', 0, 0, W, H, 160, ''.join(o))

def door_red():
    """Pagoda bay door 1.6 x 2.4 D: two vermilion leaves, rows of gold studs, dark gap, bronze rings, white sill."""
    W, H = 1.6, 2.4; o = [rect(-0.05, -0.05, W + 0.1, H + 0.1, RED_D)]
    for x0 in (0.06, W / 2 + 0.02):
        o.append(rect(x0, 0.06, W / 2 - 0.08, H - 0.14, RED)); o.append(rect(x0, 0.06, 0.04, H - 0.14, '#e05a44'))
        for j in range(5):
            for i in range(3): o.append(circ(x0 + 0.14 + i * 0.22, 0.3 + j * 0.45, 0.04, GOLD))
    o.append(rect(W / 2 - 0.02, 0.04, 0.04, H - 0.1, '#2a120e'))
    for x in (W / 2 - 0.16, W / 2 + 0.16): o.append(circ(x, H * 0.55, 0.07, 'none', stroke='#c09040', sw=0.025))
    o.append(rect(-0.05, H - 0.1, W + 0.1, 0.15, '#e8dcc0'))
    job('door_red', 0, 0, W, H, 120, ''.join(o))

def renji():
    """Barred window panel 1.6 x 2.4 D: white plaster with a vermilion-framed window of round vertical bars."""
    W, H = 1.6, 2.4; o = [rect(-0.05, -0.05, W + 0.1, H + 0.1, PLASTER)]
    x0, y0, w, h = 0.3, 0.55, 1.0, 1.1
    o.append(rect(x0 - 0.08, y0 - 0.08, w + 0.16, h + 0.16, RED)); o.append(rect(x0, y0, w, h, '#2a1a24'))
    for i in range(7): o.append(rect(x0 + 0.06 + i * 0.14, y0, 0.07, h, '#b0402e')); o.append(rect(x0 + 0.07 + i * 0.14, y0, 0.02, h, '#e2704e'))
    o.append(rect(-0.05, H - 0.62, W + 0.1, 0.62, RED)); o.append(rect(0.1, H - 0.52, W - 0.2, 0.4, RED_D)); o.append(rect(-0.05, H - 0.64, W + 0.1, 0.05, GOLD))
    job('renji', 0, 0, W, H, 120, ''.join(o))

def plaster(name='plaster', base=PLASTER, seed=5):
    r = random.Random(seed); o = [rect(-0.1, -0.1, 2.2, 2.2, base)]
    for _ in range(14):
        x, y = r.uniform(0, 2), r.uniform(0, 2)
        for xx in _wrap(x - 0.4, 2, 0.8): o.append(ell(xx + 0.4, y, r.uniform(0.15, 0.45), r.uniform(0.1, 0.35), mul(base, r.choice((0.95, 0.97, 1.02))), op=0.6))
    job(name, 0, 0, 2, 2, 64, ''.join(o))

# ----------------------------------------------------------------------------- the master's rigid tower: nailed timber and plaster
def tower_wall():
    """4 x 4.2 D storey face (u along the face, y down): heavy dark timber posts, rails, diagonal braces, iron plates with rows of
    nail heads at every joint, cream plaster infill with trowel marks."""
    r = random.Random(7); W, H = 4.0, 4.2; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#e6dcc4')]
    for _ in range(18):
        x, y = r.uniform(0, W), r.uniform(0, H); o.append(ell(x, y, r.uniform(0.2, 0.6), r.uniform(0.1, 0.3), r.choice(('#d8ccb0', '#efe6d2')), op=0.6))
    T = '#4a2e1e'
    def beam(x0, y0, x1, y1, w):
        o.append(line(x0, y0, x1, y1, T, w)); o.append(line(x0, y0, x1, y1, '#6a4430', w * 0.35, op=0.6))
    for x in (0.0, 2.0, 4.0): beam(x, -0.1, x, H + 0.1, 0.3)
    for y in (0.15, 2.1, 4.05): beam(-0.1, y, W + 0.1, y, 0.28)
    beam(0.15, 2.0, 1.85, 0.25, 0.16); beam(2.15, 0.25, 3.85, 2.0, 0.16); beam(0.15, 2.2, 1.85, 3.95, 0.16); beam(3.85, 2.2, 2.15, 3.95, 0.16)
    for (x, y) in ((0, 0.15), (2, 0.15), (4, 0.15), (0, 2.1), (2, 2.1), (4, 2.1), (0, 4.05), (2, 4.05), (4, 4.05)):
        o.append(rect(x - 0.24, y - 0.22, 0.48, 0.44, '#3a3438', stroke='#26222a', sw=0.02))
        for i in range(3):
            for j in range(3): o.append(circ(x - 0.15 + i * 0.15, y - 0.13 + j * 0.13, 0.028, '#8a8490'))
    job('tower_wall', 0, 0, W, H, 110, ''.join(o))

def crack(level):
    """Crack decal 3 x 3 D (alpha), centred on the joint at (1.5, 1.5): 1 hairline, 2 finger-wide, 3 split open (dark gap, broken
    plaster edges, splinters)."""
    r = random.Random(40 + level); o = []
    w = {1: 0.025, 2: 0.07, 3: 0.2}[level]
    pts = [(0.15, 1.42)]; x = 0.15
    while x < 2.85:
        x += r.uniform(0.12, 0.25); pts.append((min(2.85, x), 1.5 + r.uniform(-0.12, 0.12) + (0.15 if level == 3 and 1.2 < x < 1.8 else 0)))
    if level == 3:
        o.append(pline(pts, '#f4ecdc', w + 0.22, op=0.9))                                               # broken plaster rim
    o.append(pline(pts, '#1a0e0c', w))
    for k in range(2 + 2 * level):                                                                       # branches
        i = r.randint(1, len(pts) - 2); p = pts[i]; L = r.uniform(0.2, 0.5) * (0.7 + 0.3 * level); a = r.uniform(-2.4, -0.7) if k % 2 else r.uniform(0.7, 2.4)
        q = (p[0] + L * math.cos(a) * 0.5, p[1] + L * math.sin(a)); m = ((p[0] + q[0]) / 2 + r.uniform(-0.05, 0.05), (p[1] + q[1]) / 2)
        o.append(pline([p, m, q], '#1a0e0c', w * 0.45))
    if level == 3:
        for _ in range(5):
            x = r.uniform(0.5, 2.5); o.append(line(x, 1.5, x + r.uniform(-0.2, 0.2), 1.5 + r.uniform(-0.35, 0.35), '#c8a070', 0.05))
    job('crack_%d' % level, 0, 0, 3, 3, 200, ''.join(o), transparent=True)

def patch(level):
    """Plaster patch decal 3 x 3 D (alpha): a fresh, whiter, trowelled blob over the crack; level 2 is bigger and has a mark of
    the first patch under it."""
    r = random.Random(50 + level); o = []; rx, ry = (0.8, 0.32) if level == 1 else (1.3, 0.55)
    pts = []
    for i in range(16):
        a = 2 * math.pi * i / 16; k = r.uniform(0.85, 1.12); pts.append((1.5 + rx * k * math.cos(a), 1.5 + ry * k * math.sin(a)))
    o.append(poly(pts, '#fbf6ea', stroke='#d6c8a8', sw=0.03))
    for _ in range(6): o.append(path(f'M{_c(1.5 - rx * 0.7)},{_c(1.5 + r.uniform(-ry, ry) * 0.6)} q{_c(rx * 0.7)},{_c(r.uniform(-0.1, 0.1))} {_c(rx * 1.4)},0', 'none', stroke='#e8dfcc', sw=0.03))
    job('patch_%d' % level, 0, 0, 3, 3, 200, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- stone, ground
def ishigaki():
    """Castle-style dry stone wall 4 x 2 D: irregular granite blocks (warm grey / beige), dark joints, lit top edges."""
    r = random.Random(11); W, H = 4.0, 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#4a4048')]
    y = 0.0
    while y < H:
        rh = r.uniform(0.32, 0.5); x = r.uniform(-0.3, 0)
        while x < W:
            w = r.uniform(0.45, 0.9); c = r.choice(('#b8ad9c', '#a89c8e', '#c4b8a4', '#9c9288', '#b4a48c', '#c0b49e'))
            for xx in _wrap(x, W, w):
                pts = [(xx + 0.03 + r.uniform(0, 0.05), y + 0.03), (xx + w - 0.03, y + 0.03 + r.uniform(0, 0.05)), (xx + w - 0.03 - r.uniform(0, 0.05), y + rh - 0.03), (xx + 0.03, y + rh - 0.03 - r.uniform(0, 0.05))]
                o.append(poly(pts, c)); o.append(line(pts[0][0], pts[0][1] + 0.02, pts[1][0], pts[1][1] + 0.02, mul(c, 1.15), 0.035))
            x += w
        y += rh
    job('ishigaki', 0, 0, W, H, 96, ''.join(o))

def earth():
    r = random.Random(13); o = [rect(-0.1, -0.1, 6.2, 6.2, '#c49a64')]
    for _ in range(26):
        x, y = r.uniform(0, 6), r.uniform(0, 6)
        for xx in _wrap(x - 0.7, 6, 1.4): o.append(ell(xx + 0.7, y, r.uniform(0.4, 1.0), r.uniform(0.25, 0.7), r.choice(('#d0a874', '#b48a5a', '#caa06a', '#a8805a')), op=0.65))
    for _ in range(160): o.append(circ(r.uniform(0, 6), r.uniform(0, 6), r.uniform(0.015, 0.05), r.choice(('#8a6a50', '#e2c49a', '#9a7a5c'))))
    job('earth', 0, 0, 6, 6, 64, ''.join(o))

def gravel():
    r = random.Random(17); o = [rect(-0.1, -0.1, 4.2, 4.2, '#d8ccb2')]
    for _ in range(500): o.append(circ(r.uniform(0, 4), r.uniform(0, 4), r.uniform(0.02, 0.05), r.choice(('#c4b498', '#e6dcc6', '#b0a28a', '#ece4d2'))))
    for k in range(8): o.append(line(-0.1, k * 0.5 + 0.25, 4.1, k * 0.5 + 0.25, '#c6b89c', 0.04, op=0.5))     # raked lines
    job('gravel', 0, 0, 4, 4, 80, ''.join(o))

def paving():
    r = random.Random(19); o = [rect(-0.1, -0.1, 4.2, 4.2, '#7a6e6a')]
    for j in range(4):
        x = (j % 2) * 0.5
        while x < 4.6:
            w = r.uniform(0.8, 1.3); c = r.choice(('#b4aca0', '#a89e92', '#c0b6a8', '#9e968c'))
            for xx in _wrap(x, 4, w): o.append(rect(xx + 0.03, j + 0.03, w - 0.06, 0.94, c, rx=0.05))
            x += w
    job('paving', 0, 0, 4, 4, 80, ''.join(o))

# ----------------------------------------------------------------------------- town houses (machiya)
MACHIYA = [  # name, wood, noren, seed, upper plaster
    ('ma_a', '#5a3622', '#2c3c7a', 61, '#efe6d2'),
    ('ma_b', '#6a4028', '#a83030', 62, '#e8dcc4'),
    ('ma_c', '#4a2e20', '#7a5a2a', 63, '#f0e4cc'),
]
MA_W, MA_H, MA_G = 6.0, 5.6, 3.0          # facade width, eave height, ground-floor height (the pent roof sits at 3.0 .. 3.4)

def machiya(name, wood, noren, seed, upl, glow=False):
    """Street front 6 x 5.6 D (y down, y = 0 at the upper eave): upper floor white plaster with slotted mushiko windows between
    timber posts; ground floor dark wooden lattice (koshi) over a warm interior, a noren curtain in the door. glow=True draws the
    night glow mask (lit paper behind the lattice and the slots) instead."""
    r = random.Random(seed); W, H = MA_W, MA_H; yg = H - MA_G; o = []
    if glow:
        o.append(rect(-0.1, -0.1, W + 0.2, H + 0.2, '#000000'))
        if r.random() < 0.8:
            for x0 in (0.5, 3.9): o.append(rect(x0, yg + 0.5, 1.7, 1.8, '#ffb24a'))
        o.append(rect(2.5, yg + 0.3, 1.2, 2.6, '#ff9a3a'))
        if r.random() < 0.6: o.append(rect(1.4, 0.7, 3.2, 0.7, '#ffc066'))
        job(name + '_glow', 0, 0, W, H, 48, ''.join(o)); return
    o.append(rect(-0.1, -0.1, W + 0.2, H + 0.2, upl))
    for _ in range(8): o.append(ell(r.uniform(0, W), r.uniform(0, yg), r.uniform(0.3, 0.8), r.uniform(0.2, 0.5), mul(upl, 0.95), op=0.5))
    for x in (0.0, W): o.append(rect(x - 0.15, -0.1, 0.3, H + 0.2, wood))
    o.append(rect(-0.1, 0.0, W + 0.2, 0.22, wood))
    o.append(rect(1.4, 0.7, 3.2, 0.7, mul(upl, 0.9)))                                                    # mushiko slots
    for i in range(9): o.append(rect(1.55 + i * 0.34, 0.76, 0.16, 0.58, '#2a2030', rx=0.06))
    o.append(rect(-0.1, yg - 0.15, W + 0.2, 0.2, wood))
    # ground floor
    o.append(rect(-0.1, yg, W + 0.2, MA_G + 0.1, mul(wood, 0.7)))
    for x0 in (0.5, 3.9):
        o.append(rect(x0, yg + 0.5, 1.7, 1.8, '#d8b680'))                                                  # paper behind the lattice
        for i in range(14): o.append(rect(x0 + i * 0.123, yg + 0.5, 0.07, 1.8, wood))
        o.append(rect(x0 - 0.08, yg + 0.42, 1.86, 0.1, mul(wood, 0.8))); o.append(rect(x0 - 0.08, yg + 2.28, 1.86, 0.12, mul(wood, 0.8)))
    o.append(rect(2.5, yg + 0.3, 1.2, 2.7, '#2a1a14'))                                                       # door
    o.append(rect(2.42, yg + 0.25, 1.36, 1.0, noren))
    for k in (1, 2): o.append(line(2.42 + k * 0.45, yg + 0.35, 2.42 + k * 0.45, yg + 1.25, mul(noren, 0.6), 0.03))
    o.append(circ(3.1, yg + 0.75, 0.2, 'none', stroke='#efe6d2', sw=0.05))
    for x in (2.4, 3.8, 0.35, W - 0.35): o.append(rect(x - 0.1, yg, 0.2, MA_G, wood))
    o.append(rect(-0.1, H - 0.3, W + 0.2, 0.3, '#8a8078'))                                                  # stone sill
    job(name, 0, 0, W, H, 64, ''.join(o))

def side_wall():
    """House side / back wall 4 x 4 D: dark charred boards (yakisugi) to 2 D, plaster above, a timber rail."""
    o = [rect(-0.1, -0.1, 4.2, 4.2, '#ece2cc')]
    for i in range(17): o.append(rect(i * 0.24, 2.0, 0.22, 2.2, '#3a2a24' if i % 2 else '#42302a'))
    o.append(rect(-0.1, 1.85, 4.2, 0.18, WOOD))
    job('side_wall', 0, 0, 4, 4, 48, ''.join(o))

def pool():
    """Warm light pool decal 4 x 4 D (alpha radial gradient) laid on the ground under a lantern at night."""
    d = '<radialGradient id="p"><stop offset="0" stop-color="#ffb860" stop-opacity="0.75"/><stop offset="0.45" stop-color="#ff9a48" stop-opacity="0.35"/><stop offset="1" stop-color="#ff8a40" stop-opacity="0"/></radialGradient>'
    job('pool', 0, 0, 4, 4, 32, circ(2, 2, 2, 'url(#p)'), defs=d, transparent=True)

def lantern():
    """Paper lantern wrap 2 x 1 D (u round, v up): red paper with horizontal ribs, black top and bottom bands, a white circle."""
    o = [rect(-0.05, -0.05, 2.1, 1.1, '#d83a2a')]
    for k in range(1, 8): o.append(line(-0.05, k * 0.125, 2.05, k * 0.125, '#a82a22', 0.015))
    for y in (0.0, 0.9): o.append(rect(-0.05, y - 0.02, 2.1, 0.12, '#1e1414'))
    for x in (0.5, 1.5): o.append(circ(x, 0.5, 0.2, '#f6ead8')); o.append(circ(x, 0.5, 0.12, '#d83a2a'))
    job('lantern', 0, 0, 2, 1, 128, ''.join(o))

# ----------------------------------------------------------------------------- sky and painted mountain plate
SKY = dict(
    day=dict(stops=[(0, '#2f62b6'), (0.45, '#4f86cc'), (0.8, '#8cb6e6'), (0.9, '#c4d2ea'), (1, '#e8e0d8')], cloud='#fbf8ff', cloud_b='#c6b8e6', n=12, stars=0),
    sunset=dict(stops=[(0, '#d86a7a'), (0.35, '#f08a78'), (0.6, '#ffa468'), (0.8, '#ffc070'), (1, '#ffe0a0')], cloud='#ffe0b8', cloud_b='#b07a9e', n=11, stars=0),
    night=dict(stops=[(0, '#0e1a56'), (0.5, '#1a2e82'), (0.82, '#2c50a6'), (1, '#4064b4')], cloud='#3a50a2', cloud_b='#1e2a66', n=8, stars=260),
    dawn=dict(stops=[(0, '#5a7cc4'), (0.45, '#9ab4dc'), (0.7, '#f0c4aa'), (0.85, '#ffd8a8'), (1, '#fff0c8')], cloud='#fff4e8', cloud_b='#c8b0c4', n=10, stars=0))
SKY_BODY = dict(day=None, sunset=('sun', 200.0, 9.0), night=('moon', 100.0, 36.0), dawn=('sun', 337.0, 12.0))

def sky(mode):
    """Sky dome texture: u = azimuth (0..1 counter-clockwise from +x), v = elevation from -15 deg (bottom) to 90 deg (top);
    SVG x = azimuth deg, y = 90 - elevation. Flat-bottomed lavender-shaded clouds (ref a t0062/t0072), sun with rays at sunset /
    dawn, big moon with a glow and stars at night (ref a t0080)."""
    s = SKY[mode]; r = random.Random(31); W, H = 360.0, 105.0
    g = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' + ''.join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in s['stops']) + '</linearGradient>'
    g += '<filter id="b" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="0.8"/></filter>'
    g += '<radialGradient id="glow"><stop offset="0" stop-color="#fff6d8" stop-opacity="1"/><stop offset="0.3" stop-color="#ffd890" stop-opacity="0.75"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></radialGradient>'
    g += '<radialGradient id="mglow"><stop offset="0" stop-color="#eef2ff" stop-opacity="0.95"/><stop offset="0.3" stop-color="#a8b8f0" stop-opacity="0.4"/><stop offset="1" stop-color="#6070c0" stop-opacity="0"/></radialGradient>'
    o = [rect(-1, -1, W + 2, H + 2, 'url(#g)')]
    body = SKY_BODY[mode]
    for _ in range(s['stars']):
        x, y = r.uniform(0, W), r.uniform(0, 72); o.append(circ(x, y, r.uniform(0.08, 0.22), '#f4f0ff', op=r.uniform(0.4, 1.0)))
    if body:
        kind, az, el = body
        for dx in (0, W, -W):
            cx, cy = az + dx, 90 - el
            if kind == 'sun':
                o.append(ell(cx, cy, 80, 34, 'url(#glow)'))
                for k in range(16):
                    a = -math.pi * (k + 0.5) / 16; o.append(poly([(cx, cy), (cx + 95 * math.cos(a - 0.025), cy + 70 * math.sin(a - 0.025)), (cx + 95 * math.cos(a + 0.025), cy + 70 * math.sin(a + 0.025))], '#fff2cc', op=0.13))
                o.append(circ(cx, cy, 6.5, '#fff8e2'))
            else:
                o.append(circ(cx, cy, 20, 'url(#mglow)')); o.append(circ(cx, cy, 4.6, '#f8f6e8')); o.append(circ(cx - 1.2, cy - 0.8, 1.0, '#dedcca')); o.append(circ(cx + 1.6, cy + 1.2, 0.7, '#dedcca'))
    for i in range(s['n']):
        cx = r.uniform(0, W); el = r.uniform(6, 40); cy = 90 - el; w = r.uniform(16, 36) * (1.0 - 0.006 * el)
        for xx in _wrap(cx - w / 2, W, w):
            xc = xx + w / 2; grp = []; nb = r.randint(3, 5); rs = []
            for k in range(nb):
                t = (k + 0.5) / nb; rk = w * r.uniform(0.12, 0.18) * (1.25 - abs(t - 0.5)); rs.append((xc - w / 2 + w * (0.1 + 0.8 * t), rk))
            for (bx, rk) in rs: grp.append(circ(bx, cy - rk * 0.55, rk, s['cloud']))
            grp.append(rect(xc - w / 2, cy - w * 0.08, w, w * 0.08, s['cloud'], rx=w * 0.04))
            grp.append(rect(xc - w / 2 + 0.6, cy - w * 0.04, w - 1.2, w * 0.04, s['cloud_b'], rx=w * 0.02))
            o.append('<g filter="url(#b)" opacity="0.95">' + ''.join(grp) + '</g>')
    job('sky_' + mode, 0, 0, W, H, 2048 / 360.0, ''.join(o), defs=g)

PANO = dict(
    day=dict(far='#9aa8de', far2='#b4bce8', snow='#f4f6fc', mid='#6f9a5a', mid2='#8aa860', pine='#2e5a3e', town=['#efe6d2', '#e6dac0', '#f2ead8'], roof='#5c6680',
             wood='#7a4a30', shade='#8a86b8', win='#3a3050', lit=0.0, castle='#f2ece0', haze='#c8d0ee'),
    sunset=dict(far='#9a96cc', far2='#d4aaa6', snow='#ffe2c4', mid='#7a6c8c', mid2='#a8786a', pine='#3a2e44', town=['#f4c8a0', '#eab894', '#f6d0a8'], roof='#6a5078',
                wood='#7a4038', shade='#7a6aa6', win='#4a2a48', lit=0.18, castle='#ffd8b4', haze='#f0c0a0'),
    night=dict(far='#2e3c8a', far2='#3a4a9e', snow='#8a9ae0', mid='#1e2c6a', mid2='#24347a', pine='#101a42', town=['#4a5aa6', '#4252a0', '#5262ae'], roof='#262c6a',
               wood='#2a2a5a', shade='#2a3478', win='#1a2050', lit=0.4, castle='#5868b4', haze='#3c4c9c'),
    dawn=dict(far='#a4aad8', far2='#c4c8e2', snow='#fff4e8', mid='#8e94b4', mid2='#b4a49a', pine='#4a5068', town=['#f4dcc8', '#ecd0bc', '#f8e4d0'], roof='#6e7896',
              wood='#8a6650', shade='#8e94c0', win='#5a5a7a', lit=0.0, castle='#fff0e2', haze='#f6dcc0'))
PANO_R = 150.0; PANO_Z0, PANO_Z1 = -1.5, 50.0

def _ridge(a, b, base, amp, seed, n, peaks=False):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        x = a + (b - a) * i / n; h = amp * (0.35 + 0.65 * abs(math.sin(x * 0.006 + seed))) * r.uniform(0.75, 1.15)
        if peaks and i % 2: h *= 1.35
        pts.append((x, base - h))
    return pts

def panorama(mode):
    """The painted ring at R 150 (z -1.5 .. 50), u = azimuth / 360 counter-clockwise from +x, NOT repeated. SVG x = azimuth in D
    of arc, y = 50 - z; transparent above the skyline. Back to front: far jagged blue mountains with snow caps (ref a t0040),
    nearer green-violet hills with terraced fields and pine clumps, a far town band of white walls and blue-grey roofs, a castle keep
    (tenshu) on its stone base to the north-west and a far three-storey pagoda to the north-east, cherry / pine dots."""
    p = PANO[mode]; r = random.Random(57); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def X(az): return (az % 360.0) / 360.0 * W
    def Y(z): return PANO_Z1 - z
    hz = lambda c, k=1.0: mix(c, p['haze'], 0.35 * k)
    # far mountains: two ranges, jagged, with snow caps
    for (base, amp, col, sd, n) in ((Y(6), 34.0, hz(p['far2'], 1.3), 3, 70), (Y(4), 24.0, hz(p['far'], 0.9), 7, 90)):
        pts = _ridge(-2, W + 2, base, amp, sd, n, peaks=True)
        o.append(poly(pts + [(W + 2, Y(-2)), (-2, Y(-2))], col))
        for (x, y), (x1, y1), (x2, y2) in zip(pts[1:-1], pts[:-2], pts[2:]):                          # snow caps on the peaks
            if y < y1 and y < y2 and base - y > amp * 0.75:
                o.append(poly([(x, y), (x + (x2 - x) * 0.32, y + (y2 - y) * 0.32), (x + (x2 - x) * 0.18, y + (y2 - y) * 0.26), (x + (x1 - x) * 0.12, y + (y1 - y) * 0.3), (x + (x1 - x) * 0.3, y + (y1 - y) * 0.3)], p['snow'], op=0.9))
                o.append(line(x, y, x + (x2 - x) * 0.3, y + (y2 - y) * 0.3, mul(col, 0.85), 0.25, op=0.6))
    # near hills
    pts = []
    for i in range(121):
        x = W * i / 120; pts.append((x, Y(5.5 + 4.0 * abs(math.sin(x * 0.013 + 0.7)) + r.uniform(0, 1.0))))
    o.append(poly(pts + [(W, Y(-2)), (0, Y(-2))], p['mid']))
    for _ in range(90):                                                                                   # terraces / fields
        x = r.uniform(0, W); z = r.uniform(1.0, 6.5); w = r.uniform(5, 14)
        o.append(ell(x, Y(z), w / 2, r.uniform(0.25, 0.6), r.choice((p['mid2'], mul(p['mid'], 1.1))), op=0.8))
    for _ in range(160):                                                                                  # pine clumps
        x = r.uniform(0, W); z = r.uniform(1.5, 8.0); s = r.uniform(0.8, 1.8)
        o.append(ell(x, Y(z + s * 0.6), s, s * 0.5, p['pine'])); o.append(ell(x + s * 0.5, Y(z + s * 1.1), s * 0.7, s * 0.35, p['pine']))
    # far town band
    x = 0.0
    while x < W:
        w = r.uniform(2.5, 6.0); h = r.uniform(1.6, 3.0); c = r.choice(p['town'])
        if r.random() < 0.85:
            o.append(rect(x, Y(h), w, h + 1.5, c)); o.append(rect(x + w * 0.72, Y(h), w * 0.28, h + 1.5, p['shade'], op=0.55))
            o.append(rect(x, Y(h * 0.5), w, 0.18, p['wood']))
            lit = p['lit'] and r.random() < p['lit'] * 2
            o.append(rect(x + w * 0.3, Y(h * 0.42), w * 0.4, h * 0.3, '#ffc66a' if lit else p['win']))
            o.append(poly([(x - 0.4, Y(h)), (x + w * 0.5, Y(h + 1.3)), (x + w + 0.4, Y(h))], p['roof']))
        x += w + r.uniform(0.0, 1.5)
    # castle keep on its stone base (north-west) and a far pagoda (north-east)
    cx = X(128); c = p['castle']; base = mix(p['far'], '#9c9288', 0.5)
    o.append(poly([(cx - 9, Y(1)), (cx + 9, Y(1)), (cx + 7, Y(6)), (cx - 7, Y(6))], base))
    for k, (hw, z0, z1) in enumerate(((6.0, 6, 11), (4.6, 11.6, 15.5), (3.4, 16.1, 19.3))):
        o.append(rect(cx - hw, Y(z1), 2 * hw, z1 - z0, c)); o.append(rect(cx + hw * 0.5, Y(z1), hw * 0.5, z1 - z0, p['shade'], op=0.5))
        for i in range(int(hw)): o.append(rect(cx - hw + 0.6 + i * 2 * hw / int(hw), Y(z1 - 1.0), 0.6, 0.9, p['win'] if not p['lit'] else '#ffc66a'))
        o.append(path(f'M{_c(cx - hw - 2.2)},{_c(Y(z1 - 0.2))} Q{_c(cx - hw)},{_c(Y(z1 + 0.2))} {_c(cx - hw * 0.4)},{_c(Y(z1 + 1.4))} L{_c(cx + hw * 0.4)},{_c(Y(z1 + 1.4))} Q{_c(cx + hw)},{_c(Y(z1 + 0.2))} {_c(cx + hw + 2.2)},{_c(Y(z1 - 0.2))} Z', p['roof']))
    o.append(path(f'M{_c(cx - 2.6)},{_c(Y(20.7))} L{_c(cx)},{_c(Y(23))} L{_c(cx + 2.6)},{_c(Y(20.7))} Z', p['roof']))
    for dx in (-2.0, 2.0): o.append(circ(cx + dx, Y(22.2), 0.35, GOLD))
    px = X(62)
    for k in range(3):
        hw = 2.2 - 0.4 * k; z0 = 2 + k * 3.0
        o.append(rect(px - hw * 0.6, Y(z0 + 2.2), hw * 1.2, 2.2, mix(RED, p['haze'], 0.4)))
        o.append(path(f'M{_c(px - hw - 1.4)},{_c(Y(z0 + 2.1))} Q{_c(px - hw)},{_c(Y(z0 + 2.4))} {_c(px - hw * 0.5)},{_c(Y(z0 + 3.0))} L{_c(px + hw * 0.5)},{_c(Y(z0 + 3.0))} Q{_c(px + hw)},{_c(Y(z0 + 2.4))} {_c(px + hw + 1.4)},{_c(Y(z0 + 2.1))} Z', p['roof']))
    o.append(rect(px - 0.12, Y(15), 0.24, 4, GOLD))
    job('pano_' + mode, 0, 0, W, H, 4.0, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- v2 ornament (pagoda_REVIEW2): drapes, banners, carpet, mural, round window, pillar bands
GOLD_L = '#f6d47a'; GOLD_D = '#a8782a'; VEL = '#b0221e'; VEL_D = '#6e1414'; VEL_L = '#d8463a'

def _scroll(cx, cy, r, col, sw, flip=1):
    """A cloud scroll (spiral curl) as a path: one and a half turns inward."""
    pts = []
    for k in range(40):
        t = k / 39.0; a = flip * (t * 3.2 * math.pi); rr = r * (1 - 0.8 * t)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pline(pts, col, sw)

def _cloud(cx, cy, s, fill, edge):
    """Auspicious cloud (kumo): three lobes and two curls."""
    o = []
    for dx, dy, r in ((-0.55, 0.05, 0.32), (0.0, -0.18, 0.42), (0.55, 0.05, 0.32), (0.0, 0.18, 0.3)):
        o.append(circ(cx + dx * s, cy + dy * s, r * s, fill, stroke=edge, sw=0.035 * s))
    o.append(_scroll(cx - 0.55 * s, cy + 0.05 * s, 0.22 * s, edge, 0.04 * s)); o.append(_scroll(cx + 0.55 * s, cy + 0.05 * s, 0.22 * s, edge, 0.04 * s, -1))
    o.append(_scroll(cx, cy - 0.18 * s, 0.3 * s, edge, 0.045 * s))
    return ''.join(o)

def curtain():
    """Red velvet drape 2 x 3 D (u across, y down = from the rod down): deep folds, a gold galloon band and fringe at the hem."""
    W, H = 2.0, 3.0
    d = ('<linearGradient id="f" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0.4" y2="0" spreadMethod="repeat">'
         f'<stop offset="0" stop-color="{VEL_D}"/><stop offset="0.3" stop-color="{VEL}"/><stop offset="0.55" stop-color="{VEL_L}"/><stop offset="0.8" stop-color="{VEL}"/><stop offset="1" stop-color="{VEL_D}"/></linearGradient>')
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, 'url(#f)')]
    o.append(rect(-0.1, -0.1, W + 0.2, 0.18, VEL_D))
    for k in range(10): o.append(circ(0.1 + k * 0.2, 0.06, 0.035, GOLD))                              # rings on the rod
    o.append(rect(-0.1, H - 0.42, W + 0.2, 0.12, GOLD)); o.append(rect(-0.1, H - 0.42, W + 0.2, 0.03, GOLD_L)); o.append(rect(-0.1, H - 0.33, W + 0.2, 0.02, GOLD_D))
    for k in range(40):                                                                                 # fringe
        x = k * 0.05 + 0.02; o.append(rect(x, H - 0.3, 0.025, 0.28, GOLD if k % 2 else GOLD_D))
    for k in range(5): o.append(_cloud(0.2 + k * 0.4, H - 0.62, 0.12, 'none', GOLD))
    job('curtain', 0, 0, W, H, 96, ''.join(o), defs=d)

def valance():
    """Swagged pelmet 3 x 0.9 D (transparent below the swags): three red swags with gold borders, gold tassels between them."""
    W, H = 3.0, 0.9; o = [rect(-0.05, -0.05, W + 0.1, 0.28, VEL_D), rect(-0.05, 0.18, W + 0.1, 0.06, GOLD)]
    for k in range(3):
        x0 = k * 1.0; dd = f'M {x0} 0.22 Q {x0 + 0.5} 0.95 {x0 + 1.0} 0.22 Z'
        o.append(path(dd, VEL, stroke=GOLD, sw=0.05))
        for j in (0.38, 0.52): o.append(path(f'M {x0 + 0.08} 0.25 Q {x0 + 0.5} {j + 0.2} {x0 + 0.92} 0.25', 'none', stroke=VEL_L, sw=0.025))
        o.append(path(f'M {x0 + 0.02} 0.24 Q {x0 + 0.5} 0.86 {x0 + 0.98} 0.24', 'none', stroke=GOLD_L, sw=0.02))
    for k in range(4):
        x = k * 1.0; o.append(circ(x, 0.3, 0.06, GOLD)); o.append(poly([(x - 0.05, 0.34), (x + 0.05, 0.34), (x + 0.08, 0.8), (x - 0.08, 0.8)], GOLD, stroke=GOLD_D, sw=0.01))
        for j in range(5): o.append(line(x - 0.06 + j * 0.03, 0.5, x - 0.07 + j * 0.035, 0.8, GOLD_D, 0.008))
    job('valance', 0, 0, W, H, 160, ''.join(o), transparent=True)

def ban():
    """Buddhist ban banner 0.7 x 3.2 D (transparent around it): gold triangular head with a jewel, red body in panels with gold
    borders and cloud roundels, a gold-and-red tail of streamers."""
    W, H = 0.7, 3.2; o = []
    o.append(poly([(0.35, 0.0), (0.7, 0.35), (0.0, 0.35)], GOLD, stroke=GOLD_D, sw=0.02)); o.append(circ(0.35, 0.22, 0.07, VEL, stroke=GOLD_L, sw=0.015))
    o.append(rect(0.0, 0.35, 0.7, 2.15, VEL)); o.append(rect(0.0, 0.35, 0.7, 2.15, 'none', stroke=GOLD, sw=0.05))
    for k in range(3):
        y = 0.55 + k * 0.68; o.append(rect(0.06, y - 0.1, 0.58, 0.6, VEL_D if k % 2 else VEL, stroke=GOLD_D, sw=0.015))
        o.append(circ(0.35, y + 0.2, 0.2, 'none', stroke=GOLD, sw=0.035)); o.append(_cloud(0.35, y + 0.2, 0.15, GOLD, GOLD_D))
    for k, x in enumerate((0.08, 0.24, 0.46, 0.62)):
        o.append(poly([(x - 0.07, 2.5), (x + 0.07, 2.5), (x + 0.05, 3.1 - 0.08 * (k % 2)), (x, 3.18 - 0.08 * (k % 2)), (x - 0.05, 3.1 - 0.08 * (k % 2))], GOLD if k % 2 else VEL, stroke=GOLD_D, sw=0.01))
    job('ban', 0, 0, W, H, 128, ''.join(o), transparent=True)

def nobori2():
    """Approach banner 0.8 x 2.6 D: red with a gold border band, a white roundel with a red-gold flame jewel, gold ties on the pole side."""
    W, H = 0.8, 2.6; o = [rect(-0.05, -0.05, W + 0.1, H + 0.1, VEL)]
    o.append(rect(0.0, 0.0, W, 0.18, GOLD)); o.append(rect(0.0, H - 0.2, W, 0.2, GOLD)); o.append(rect(0.0, 0.0, 0.06, H, GOLD_D)); o.append(rect(W - 0.06, 0.0, 0.06, H, GOLD))
    o.append(circ(0.4, 0.62, 0.25, '#f6ecd8')); o.append(circ(0.4, 0.62, 0.25, 'none', stroke=GOLD, sw=0.03))
    o.append(path('M 0.4 0.42 Q 0.55 0.6 0.4 0.82 Q 0.25 0.6 0.4 0.42 Z', VEL)); o.append(circ(0.4, 0.68, 0.05, GOLD))
    for k in range(3): y = 1.1 + k * 0.45; o.append(rect(0.2, y, 0.4, 0.06, '#2a1414')); o.append(rect(0.37, y - 0.08, 0.06, 0.3, '#2a1414'))
    for k in range(6): o.append(rect(-0.05, 0.25 + k * 0.4, 0.12, 0.08, '#f6ecd8'))
    job('nobori2', 0, 0, W, H, 96, ''.join(o))

def maku():
    """Gate curtain (maku) 8 x 1.4 D: vertical panels purple-red / white alternating... red with gold crest roundels and a gold top band."""
    W, H = 8.0, 1.4; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, VEL)]
    for k in range(16): o.append(rect(k * 0.5, 0.2, 0.02, H - 0.2, VEL_D))
    o.append(rect(-0.1, -0.1, W + 0.2, 0.3, '#3a1e3a')); o.append(rect(-0.1, 0.18, W + 0.2, 0.05, GOLD))
    for x in (1.0, 4.0, 7.0):
        o.append(circ(x, 0.8, 0.42, '#f6ecd8')); o.append(circ(x, 0.8, 0.42, 'none', stroke=GOLD, sw=0.05))
        for a in range(3):
            aa = a * 2 * math.pi / 3; o.append(_scroll(x + 0.16 * math.cos(aa), 0.8 + 0.16 * math.sin(aa), 0.17, VEL, 0.07))
    for k in range(9): o.append(circ(k * 1.0, 0.12, 0.08, GOLD))
    o.append(rect(-0.1, H - 0.08, W + 0.2, 0.1, GOLD_D))
    job('maku', 0, 0, W, H, 64, ''.join(o))

def carpet():
    """Runner carpet 2 x 4 D (u across, v along, tiles along v): red field, double gold border, gold lozenges and flowers."""
    W, H = 2.0, 4.0; F_ = '#8a3430'; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, F_)]
    for x in (0.06, W - 0.22): o.append(rect(x, -0.1, 0.16, H + 0.2, '#2a1a3a')); o.append(rect(x + 0.02, -0.1, 0.03, H + 0.2, GOLD)); o.append(rect(x + 0.11, -0.1, 0.03, H + 0.2, GOLD))
    for k in range(5):
        y = k * 1.0 + 0.0
        o.append(poly([(1.0, y - 0.38), (1.42, y), (1.0, y + 0.38), (0.58, y)], 'none', stroke=GOLD, sw=0.04))
        o.append(circ(1.0, y, 0.12, GOLD)); o.append(circ(1.0, y, 0.06, F_))
        for dx in (-0.45, 0.45): o.append(circ(1.0 + dx, y + 0.5, 0.06, GOLD_D))
    job('carpet', 0, 0, W, H, 64, ''.join(o))

def mural():
    """Painted wall panel 2 x 2.6 D behind the hero (inside the ground storey): black-lacquer field in a red-and-gold frame, a gold
    dragon coiling through gold clouds, a gold flaming pearl."""
    W, H = 2.0, 2.6; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#2a1414'), rect(0.0, 0.0, W, H, VEL)]
    o.append(rect(0.12, 0.12, W - 0.24, H - 0.24, '#1a1424')); o.append(rect(0.12, 0.12, W - 0.24, H - 0.24, 'none', stroke=GOLD, sw=0.04))
    o.append(rect(0.06, 0.06, W - 0.12, H - 0.12, 'none', stroke=GOLD_D, sw=0.02))
    r = random.Random(17)
    for _ in range(7): o.append(_cloud(r.uniform(0.35, 1.65), r.uniform(0.35, 2.25), r.uniform(0.18, 0.28), '#3a2a3e', GOLD_D))
    pts = []                                                                                          # dragon body (s-curve)
    for k in range(60):
        t = k / 59.0; pts.append((1.0 + 0.55 * math.sin(t * 2.6 * math.pi), 0.45 + 1.8 * t))
    o.append(pline(pts, GOLD_D, 0.2)); o.append(pline(pts, GOLD, 0.15)); o.append(pline(pts, GOLD_L, 0.04))
    for k in range(4, 58, 3):
        x, y = pts[k]; x2, y2 = pts[k + 1]; nx, ny = -(y2 - y), (x2 - x); L_ = math.hypot(nx, ny) or 1
        o.append(poly([(x + nx / L_ * 0.07, y + ny / L_ * 0.07), (x + nx / L_ * 0.17 + (x2 - x), y + ny / L_ * 0.17 + (y2 - y)), (x2 + nx / L_ * 0.07, y2 + ny / L_ * 0.07)], GOLD, stroke=GOLD_D, sw=0.01))
    hx_, hy_ = pts[0]
    o.append(ell(hx_ - 0.05, hy_ - 0.05, 0.2, 0.13, GOLD, stroke=GOLD_D, sw=0.02)); o.append(circ(hx_ - 0.1, hy_ - 0.1, 0.03, VEL))
    o.append(pline([(hx_ - 0.2, hy_ - 0.02), (hx_ - 0.45, hy_ - 0.2), (hx_ - 0.55, hy_ - 0.1)], GOLD, 0.03))
    o.append(pline([(hx_ + 0.05, hy_ - 0.15), (hx_ + 0.2, hy_ - 0.38)], GOLD, 0.04)); o.append(pline([(hx_ - 0.05, hy_ - 0.16), (hx_ - 0.05, hy_ - 0.42)], GOLD, 0.04))
    o.append(circ(0.45, 2.1, 0.15, '#ff9a4a')); o.append(circ(0.45, 2.1, 0.09, '#fff0c0'))
    for a in range(6): aa = a * math.pi / 3; o.append(line(0.45 + 0.17 * math.cos(aa), 2.1 + 0.17 * math.sin(aa), 0.45 + 0.27 * math.cos(aa), 2.1 + 0.27 * math.sin(aa), '#ffb050', 0.03))
    job('mural', 0, 0, W, H, 128, ''.join(o))

def maru():
    """Round lattice window 2 x 2 D (transparent outside the circle): warm paper behind a diamond-and-flower lattice, gold ring."""
    W = 2.0; d = '<radialGradient id="g"><stop offset="0" stop-color="#fff2c8"/><stop offset="0.7" stop-color="#ffcf80"/><stop offset="1" stop-color="#e8a050"/></radialGradient>'
    o = [circ(1, 1, 0.98, 'url(#g)')]
    lat = []
    for k in range(-6, 7):
        t = k * 0.24; lat.append(line(1 + t - 1.2, -0.2, 1 + t + 1.2, 2.2, '#4a2414', 0.05)); lat.append(line(1 + t + 1.2, -0.2, 1 + t - 1.2, 2.2, '#4a2414', 0.05))
    o.append('<g clip-path="url(#c)">' + ''.join(lat) + '</g>')
    for a in range(8):
        aa = a * math.pi / 4; o.append(ell(1 + 0.32 * math.cos(aa), 1 + 0.32 * math.sin(aa), 0.16, 0.08, '#4a2414', extra=f' transform="rotate({math.degrees(aa):.1f} {1 + 0.32 * math.cos(aa):.3f} {1 + 0.32 * math.sin(aa):.3f})"'))
    o.append(circ(1, 1, 0.14, '#4a2414')); o.append(circ(1, 1, 0.07, GOLD))
    o.append(circ(1, 1, 0.94, 'none', stroke='#4a2414', sw=0.1)); o.append(circ(1, 1, 0.97, 'none', stroke=GOLD, sw=0.05))
    job('maru', 0, 0, W, W, 160, ''.join(o), defs='<clipPath id="c"><circle cx="1" cy="1" r="0.95"/></clipPath>' + d, transparent=True)

def cloud_band():
    """Bronze sleeve band round the pillar foot 3 x 0.5 D (u wraps once round r 0.47): gold cloud scrolls in relief on dark bronze,
    beaded rims."""
    W, H = 3.0, 0.5; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#4a3014')]
    for k in range(6):
        o.append(_cloud(0.25 + k * 0.5, 0.25, 0.17, '#c89a3c', '#f8dc8a'))
    for y in (0.03, 0.47):
        o.append(rect(-0.1, y - 0.03, W + 0.2, 0.06, '#d8aa48'))
        for k in range(60): o.append(circ(k * 0.05, y, 0.02, '#fbe6a0'))
    job('cloud_band', 0, 0, W, H, 192, ''.join(o))

def scales():
    """Gold dragon scales 1 x 1 D (tiles): overlapping scallops with bright rims, for the dragon coiled round the pillar foot."""
    o = [rect(-0.1, -0.1, 1.2, 1.2, '#b8862e')]
    for j in range(9):
        for i in range(9):
            x = i * 0.125 + (0.0625 if j % 2 else 0); y = j * 0.125
            o.append(path(f'M {x - 0.07} {y} A 0.07 0.07 0 0 0 {x + 0.07} {y}', '#e8b850', stroke='#7a5418', sw=0.012))
            o.append(path(f'M {x - 0.045} {y + 0.02} A 0.05 0.05 0 0 0 {x + 0.045} {y + 0.02}', 'none', stroke='#fbe2a0', sw=0.01))
    job('scales', 0, 0, 1, 1, 160, ''.join(o))

# ----------------------------------------------------------------------------- registry
MODES = ('day', 'sunset', 'night', 'dawn')
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear()
    kawara('kawara', TILE, 3); kawara('kawara_dark', TILE_D, 4); kawara('kawara_house', '#747a92', 5)
    rafters(); bracket(); door_red(); renji(); plaster(); plaster('plaster_warm', '#eadcc0', 6); tower_wall()
    for lv in (1, 2, 3): crack(lv)
    for lv in (1, 2): patch(lv)
    ishigaki(); earth(); gravel(); paving(); side_wall(); lantern(); pool()
    for m in MACHIYA: machiya(*m); machiya(*m, glow=True)
    for m in MODES: sky(m); panorama(m)
    curtain(); valance(); ban(); nobori2(); maku(); carpet(); mural(); maru(); cloud_band(); scales()

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
