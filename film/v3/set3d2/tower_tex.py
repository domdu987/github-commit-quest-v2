#!/usr/bin/env python3
"""tower_tex.py : artwork of the bell-tower set, drawn as SVG in Python and rasterised by headless Chromium
(PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in v3/set3d2/tex_tower/ by content hash.

    import tower_tex as TT
    paths = TT.ensure()        # {name: png path}
    TT.SIZE[name] -> (w_D, h_D) of one image / tile;  TT.WINDOWS[name] -> window rectangles (D, y down) of a facade

Every surface is drawn in the colour it shows in neutral light; the lit material makes sun and shade of it.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
TEX = os.path.join(HERE, 'tex_tower'); WORK = os.path.join(HERE, 'tower_work')
RASTER = os.path.join(PROJ, 'v3', 'set3d', 'raster.js')
JOBS = {}; SIZE = {}; WINDOWS = {}

# ----------------------------------------------------------------------------- svg helpers (D units, y down)
def _c(v): return '%.4g' % v
def rect(x, y, w, h, fill, stroke=None, sw=0.0, rx=0.0, op=None, extra=''):
    s = f'<rect x="{_c(x)}" y="{_c(y)}" width="{_c(w)}" height="{_c(h)}" fill="{fill}"'
    if rx: s += f' rx="{_c(rx)}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{_c(sw)}"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + extra + '/>'
def poly(pts, fill, stroke=None, sw=0.0, op=None, extra=''):
    s = '<polygon points="' + ' '.join(f'{_c(x)},{_c(y)}' for x, y in pts) + f'" fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{_c(sw)}" stroke-linejoin="round"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + extra + '/>'
def pline(pts, stroke, sw, op=None, fill='none'):
    s = '<polyline points="' + ' '.join(f'{_c(x)},{_c(y)}' for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{_c(sw)}" stroke-linecap="round" stroke-linejoin="round"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + '/>'
def line(x0, y0, x1, y1, stroke, sw, op=None):
    s = f'<line x1="{_c(x0)}" y1="{_c(y0)}" x2="{_c(x1)}" y2="{_c(y1)}" stroke="{stroke}" stroke-width="{_c(sw)}" stroke-linecap="round"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + '/>'
def circ(cx, cy, r, fill, stroke=None, sw=0.0, op=None, extra=''):
    s = f'<circle cx="{_c(cx)}" cy="{_c(cy)}" r="{_c(r)}" fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{_c(sw)}"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + extra + '/>'
def ell(cx, cy, rx, ry, fill, stroke=None, sw=0.0, op=None, extra=''):
    s = f'<ellipse cx="{_c(cx)}" cy="{_c(cy)}" rx="{_c(rx)}" ry="{_c(ry)}" fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{_c(sw)}"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + extra + '/>'
def path(d, fill, stroke=None, sw=0.0, op=None, extra=''):
    s = f'<path d="{d}" fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{_c(sw)}" stroke-linejoin="round" stroke-linecap="round"'
    if op is not None: s += f' opacity="{_c(op)}"'
    return s + extra + '/>'

def hx(c):
    c = c.lstrip('#'); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
def mul(c, k):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v * k)))) for v in hx(c))
def mix(a, b, t):
    A, B = hx(a), hx(b); return '#%02x%02x%02x' % tuple(int(round(x + (y - x) * t)) for x, y in zip(A, B))

def job(name, x0, y0, w, h, ppd, body, defs='', bg=None, transparent=False):
    """SVG of the D rectangle (x0, y0, w, h) at ppd pixels per D."""
    W, H = int(round(w * ppd)), int(round(h * ppd))
    b = rect(x0, y0, w, h, bg) if bg else ''
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{_c(x0)} {_c(y0)} {_c(w)} {_c(h)}" '
           f'preserveAspectRatio="none" style="display:block"><defs>{defs}</defs>{b}{body}</svg>')
    JOBS[name] = dict(svg=svg, w=W, h=H, transparent=transparent); SIZE[name] = (w, h)

def _wrap(x, W, w):
    """x positions of a shape of width w starting at x so that it tiles seamlessly in [0, W]."""
    out = [x]
    if x + w > W: out.append(x - W)
    if x < 0: out.append(x + W)
    return out

# ----------------------------------------------------------------------------- palette (display colours in neutral light)
BRICK = ['#d0803c', '#c47034', '#da9446', '#b8622e', '#d48a42', '#e2a050', '#c87838', '#cc7434', '#bf6a30']
MORTAR = '#e2b07c'
STONE = '#e6c894'; STONE_J = '#a87e52'
INKW = '#3b1f1a'

# ----------------------------------------------------------------------------- wall surfaces
def brick(name='brick', seed=1, dark=1.0):
    """Seamless brick tile 2.0 x 1.92 D: 12 courses of 0.16 D, bricks 0.40 D, half bond, warm terracotta / ochre."""
    r = random.Random(seed); W, H = 2.0, 1.92; ch = 0.16; bl = 0.40; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(MORTAR, dark))]
    for k in range(12):
        y = k * ch; off = (bl / 2) * (k % 2)
        for i in range(-1, 6):
            x = i * bl + off
            c = mul(r.choice(BRICK), dark * r.uniform(0.94, 1.06))
            for xx in _wrap(x + 0.012, W, bl - 0.024):
                o.append(rect(xx, y + 0.014, bl - 0.024, ch - 0.028, c, rx=0.01))
                if r.random() < 0.35: o.append(rect(xx + 0.02, y + 0.02, bl - 0.07, 0.022, mul(c, 1.12), rx=0.008))      # sun-worn top edge
                if r.random() < 0.18: o.append(rect(xx + r.uniform(0.05, 0.25), y + 0.05, 0.08, 0.05, mul(c, 0.86), rx=0.02))   # chip
    for k in range(13): o.append(line(-0.1, k * ch + 0.003, W + 0.1, k * ch + 0.003, mul(MORTAR, 0.78 * dark), 0.006))
    for _ in range(4):                                                          # weather streaks
        x = r.uniform(0.1, 1.9); y = r.uniform(0, 1.2)
        o.append(rect(x, y, r.uniform(0.04, 0.09), r.uniform(0.4, 0.8), '#7a3a26', op=0.13, rx=0.03))
    job(name, 0, 0, W, H, 256, ''.join(o))

def stone(name='stone', seed=2, base=STONE, ppd=200):
    """Seamless travertine ashlar 2 x 2 D: courses 0.5 D, blocks 0.6 to 1.0 D, pitted."""
    r = random.Random(seed); W = H = 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, mul(base, 0.9))]
    for k in range(4):
        y = k * 0.5; x = r.uniform(0, 0.5)
        while x < W + 0.5:
            w = r.uniform(0.6, 1.0); c = mul(base, r.uniform(0.94, 1.05))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.015, y + 0.015, w - 0.03, 0.47, c, rx=0.02))
                o.append(line(xx + 0.03, y + 0.035, xx + w - 0.05, y + 0.035, mul(c, 1.1), 0.02))
                for _ in range(5): o.append(ell(xx + r.uniform(0.05, w - 0.05), y + r.uniform(0.08, 0.45), r.uniform(0.01, 0.03), r.uniform(0.006, 0.012), mul(c, 0.78)))
            x += w
        o.append(line(-0.1, y + 0.002, W + 0.1, y + 0.002, STONE_J, 0.014))
    job(name, 0, 0, W, H, ppd, ''.join(o))

def plaster(name, base, seed):
    """Seamless lime plaster 2 x 2 D with soft stains, a few cracks and patches of brick showing."""
    r = random.Random(seed); W = H = 2.0; o = [rect(-0.1, -0.1, 2.2, 2.2, base)]
    for _ in range(7):
        x, y = r.uniform(0, 2), r.uniform(0, 2); c = mul(base, r.choice((0.9, 0.93, 1.06)))
        for xx in _wrap(x - 0.3, W, 0.6): o.append(ell(xx + 0.3, y, r.uniform(0.15, 0.35), r.uniform(0.1, 0.3), c, op=0.55))
    for _ in range(2):
        x, y = r.uniform(0.2, 1.6), r.uniform(0.2, 1.6); o.append(rect(x, y, 0.3, 0.17, mul(base, 0.95), stroke=mul(base, 0.72), sw=0.012, rx=0.03))
        for j in range(2): o.append(rect(x + 0.03 + 0.13 * j, y + 0.03, 0.11, 0.05, '#b8573a')); o.append(rect(x + 0.09 + 0.13 * j - 0.06, y + 0.09, 0.11, 0.05, '#c46a40'))
    for _ in range(3):
        x, y = r.uniform(0.1, 1.9), r.uniform(0.1, 1.9); pts = [(x, y)]
        for _k in range(4): x += r.uniform(-0.06, 0.06); y += r.uniform(0.04, 0.1); pts.append((x, y))
        o.append(pline(pts, mul(base, 0.62), 0.008))
    job(name, 0, 0, W, H, 160, ''.join(o))

def archetti():
    """Lombard band of small hanging arches (archetti pensili), 1.0 x 0.5 D per two arches, stone on a brick shadow."""
    o = [rect(-0.1, -0.1, 1.2, 0.7, '#8e3f28')]
    for i in range(2):
        cx = 0.25 + i * 0.5
        o.append(path(f'M{cx - 0.22},0.5 L{cx - 0.22},0.26 A0.22,0.22 0 0 1 {cx + 0.22},0.26 L{cx + 0.22},0.5 Z', '#7a3322'))
        o.append(path(f'M{cx - 0.25},0 L{cx + 0.25},0 L{cx + 0.25},0.5 L{cx + 0.2},0.5 L{cx + 0.2},0.27 A0.2,0.2 0 0 0 {cx - 0.2},0.27 L{cx - 0.2},0.5 L{cx - 0.25},0.5 Z',
                      STONE, stroke=INKW, sw=0.012))
        o.append(path(f'M{cx - 0.16},0.3 A0.16,0.16 0 0 1 {cx + 0.16},0.3', 'none', stroke=mul(STONE, 1.1), sw=0.02))
        o.append(rect(cx - 0.035, 0.42, 0.07, 0.08, mul(STONE, 0.82), stroke=INKW, sw=0.01))        # little corbel
    o.append(line(-0.1, 0.012, 1.1, 0.012, INKW, 0.02))
    job('archetti', 0, 0, 1.0, 0.5, 256, ''.join(o))

def coppi(name='roof', base='#b9532f', seed=3):
    """Seamless Italian canal-tile roof 2 x 2 D: tile rows run down the slope (v), 0.22 D wide channels."""
    r = random.Random(seed); W = H = 2.0; n = 9; tw = W / n; o = [rect(-0.1, -0.1, 2.2, 2.2, mul(base, 0.55))]
    for i in range(n):
        x = i * tw; yo = r.uniform(0, 0.4)
        for j in range(-1, 6):
            y = yo + j * 0.4; c = mul(base, r.uniform(0.9, 1.12))
            for yy in _wrap(y, H, 0.42):
                o.append(rect(x + 0.02, yy, tw - 0.04, 0.42, c, rx=0.06))
                o.append(rect(x + 0.05, yy + 0.03, 0.045, 0.34, mul(c, 1.22), rx=0.02))
                o.append(rect(x + tw - 0.08, yy + 0.03, 0.04, 0.36, mul(c, 0.72), rx=0.02))
                o.append(line(x + 0.03, yy + 0.415, x + tw - 0.03, yy + 0.415, mul(c, 0.5), 0.016))
                if r.random() < 0.08: o.append(ell(x + tw / 2, yy + 0.2, 0.06, 0.04, '#6f7d3a', op=0.7))       # moss
    job(name, 0, 0, W, H, 200, ''.join(o))

def scales():
    """Fish-scale terracotta tiles of the spire, 1 x 1 D tile."""
    o = [rect(-0.1, -0.1, 1.2, 1.2, '#7c3322')]; r = random.Random(5)
    for j in range(7):
        y = j * 0.16; off = 0.0625 * (j % 2)
        for i in range(-1, 9):
            x = off + i * 0.125; c = r.choice(('#b8532f', '#c4643a', '#a94a2b', '#cf7a48'))
            for xx in _wrap(x, 1.0, 0.125):
                o.append(path(f'M{xx},{y} L{xx + 0.125},{y} L{xx + 0.125},{y + 0.1} A0.0625,0.0625 0 0 1 {xx},{y + 0.1} Z', c, stroke='#5a2418', sw=0.008))
                o.append(path(f'M{xx + 0.02},{y + 0.1} A0.045,0.045 0 0 0 {xx + 0.06},{y + 0.145}', 'none', stroke=mul(c, 1.25), sw=0.01))
    job('scales', 0, 0, 1.0, 1.12, 256, ''.join(o))

def cobbles():
    """Seamless cobble paving 2 x 2 D: rounded setts in warm grey-ochre, dark joints (ref a/t0080 floor)."""
    r = random.Random(7); W = H = 2.0; o = [rect(-0.1, -0.1, 2.2, 2.2, '#6e4c3c')]
    rows = 9; rh = H / rows
    for j in range(rows):
        y = j * rh + rh / 2; x = r.uniform(0, 0.2)
        while x < W:
            w = r.uniform(0.16, 0.26); c = r.choice(('#b89272', '#a8806a', '#c4a27c', '#9c7764', '#b48a66', '#c79a6c'))
            for xx in _wrap(x, W, w):
                o.append(ell(xx + w / 2, y, w / 2 - 0.012, rh / 2 - 0.016, c, stroke='#5a3a30', sw=0.008))
                o.append(ell(xx + w / 2 - 0.02, y - 0.02, w / 2 - 0.05, rh / 2 - 0.05, mul(c, 1.1)))
            x += w
    for _ in range(3):                                         # damp patches
        x, y = r.uniform(0.2, 1.6), r.uniform(0.2, 1.6); o.append(ell(x, y, 0.3, 0.2, '#4a3436', op=0.15))
    job('cobbles', 0, 0, W, H, 256, ''.join(o))

def planks(name='planks', base='#8c5232', seed=9):
    """Seamless floor boards 2 x 2 D, 0.25 D wide, running along v; worn centre."""
    r = random.Random(seed); W = H = 2.0; n = 8; pw = W / n; o = [rect(-0.1, -0.1, 2.2, 2.2, mul(base, 0.5))]
    for i in range(n):
        x = i * pw; c = mul(base, r.uniform(0.88, 1.1)); o.append(rect(x + 0.008, -0.1, pw - 0.016, 2.2, c))
        for _ in range(3):
            gx = x + r.uniform(0.04, pw - 0.04); o.append(line(gx, -0.1, gx + r.uniform(-0.02, 0.02), 2.1, mul(c, r.choice((0.82, 1.14))), 0.008))
        yb = r.uniform(0, 2)
        for yy in (yb, yb - 2): o.append(line(x + 0.01, yy, x + pw - 0.01, yy, mul(base, 0.45), 0.014))
        if r.random() < 0.5:
            ky = r.uniform(0.2, 1.8); o.append(ell(x + pw / 2, ky, 0.03, 0.05, mul(c, 0.6)))
        for yy in (0.2, 1.0, 1.8): o.append(circ(x + 0.04, yy + r.uniform(-0.1, 0.1), 0.012, '#3a2a28'))
    job(name, 0, 0, W, H, 200, ''.join(o))

def wood_beam():
    """Hewn beam side 2 x 0.5 D: grain, checks, iron nails."""
    r = random.Random(11); o = [rect(-0.1, -0.1, 2.2, 0.7, '#7a4428')]
    for _ in range(12):
        y = r.uniform(0.04, 0.46); x = r.uniform(-0.2, 1.6); o.append(line(x, y, x + r.uniform(0.3, 0.8), y + r.uniform(-0.02, 0.02), r.choice(('#5e321e', '#94603a')), 0.012))
    for _ in range(3):
        x = r.uniform(0.1, 1.7); o.append(line(x, 0.2, x + 0.25, 0.22, '#3a1e14', 0.02))
    o.append(line(-0.1, 0.02, 2.1, 0.02, '#a8744a', 0.03)); o.append(line(-0.1, 0.48, 2.1, 0.48, '#4a2616', 0.03))
    job('beam', 0, 0, 2.0, 0.5, 200, ''.join(o))

def clock_face():
    """Painted tower clock 1.6 D: Roman-ish ticks, sun-yellow ring, one hand (old Italian six-hour dial)."""
    o = [circ(0.8, 0.8, 0.78, '#2a3a7a', stroke=INKW, sw=0.03), circ(0.8, 0.8, 0.66, '#f1dfae', stroke='#b08a3a', sw=0.03)]
    for i in range(24):
        a = 2 * math.pi * i / 24; l = 0.12 if i % 2 == 0 else 0.06
        o.append(line(0.8 + 0.6 * math.cos(a), 0.8 + 0.6 * math.sin(a), 0.8 + (0.6 - l) * math.cos(a), 0.8 + (0.6 - l) * math.sin(a), '#3b2a22', 0.022))
    for i in range(12):
        a = 2 * math.pi * i / 12; o.append(circ(0.8 + 0.71 * math.cos(a), 0.8 + 0.71 * math.sin(a), 0.03, '#f2c24a'))
    o.append(circ(0.8, 0.8, 0.22, '#e8a33a', stroke='#8a5a20', sw=0.02))
    for i in range(12):
        a = 2 * math.pi * i / 12; o.append(line(0.8 + 0.22 * math.cos(a), 0.8 + 0.22 * math.sin(a), 0.8 + 0.3 * math.cos(a), 0.8 + 0.3 * math.sin(a), '#e8a33a', 0.03))
    o.append(poly([(0.8, 0.8 - 0.02), (0.8 + 0.48, 0.8 - 0.3), (0.8 + 0.02, 0.8 + 0.03)], '#2b1d18'))
    o.append(circ(0.8, 0.8, 0.04, '#2b1d18'))
    job('clock', 0, 0, 1.6, 1.6, 256, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- facades
SHUTTER = ['#3f7a4a', '#2f6a5a', '#5a7f3a', '#3a6a8a']
def house_facade(name, w, h, base, floors, seed, shutter, door_style='arch', shop=False):
    """Front of a town house, w x h D (h = eave height). Windows with open shutters, flower boxes with geraniums,
    string courses, a door, stains. WINDOWS[name] = [(x, y, w, h)] of the glazing (y down from the eave) for night glow."""
    r = random.Random(seed); o = []; win = []
    o.append(rect(-0.1, -0.1, w + 0.2, h + 0.2, base))
    for _ in range(9):                                         # plaster stains, darker toward the ground
        x, y = r.uniform(0, w), r.uniform(0, h); o.append(ell(x, y, r.uniform(0.3, 0.9), r.uniform(0.2, 0.6), mul(base, r.choice((0.9, 0.93, 1.05))), op=0.6))
    o.append(rect(-0.1, h - 1.2, w + 0.2, 1.3, mul(base, 0.86)))                     # rising damp / plinth band
    o.append(rect(-0.1, h - 0.35, w + 0.2, 0.45, mul(base, 0.68)))
    o.append(rect(-0.1, -0.1, w + 0.2, 0.45, mul(base, 0.8)))                         # under the eave, darker
    for k in range(0, int(w / 0.5) + 1): o.append(rect(k * 0.5 + 0.1, 0.05, 0.16, 0.2, mul(base, 0.55), rx=0.02))   # rafter ends painted under the eave
    gf = 3.0                                                                            # ground floor height
    fl_h = (h - gf - 0.6) / floors
    o.append(rect(-0.1, h - gf - 0.12, w + 0.2, 0.16, mul(base, 1.12), stroke=mul(base, 0.6), sw=0.02))   # string course
    nwin = max(2, int(w / 1.7))
    xs = [w * (i + 0.5) / nwin for i in range(nwin)]
    for f in range(floors):
        top = 0.6 + f * fl_h; wy = top + 0.35; wh = min(1.55, fl_h - 0.75); ww = 0.72
        for xc in xs:
            x0 = xc - ww / 2
            o.append(rect(x0 - 0.1, wy - 0.1, ww + 0.2, wh + 0.15, mul(base, 1.18), stroke=mul(base, 0.6), sw=0.02))   # stucco frame
            o.append(rect(x0, wy, ww, wh, '#2a2238'))
            o.append(rect(x0 + 0.04, wy + 0.04, ww / 2 - 0.06, wh - 0.08, '#3c4a7a')); o.append(rect(x0 + ww / 2 + 0.02, wy + 0.04, ww / 2 - 0.06, wh - 0.08, '#3c4a7a'))
            o.append(line(x0 + 0.06, wy + wh * 0.45, x0 + ww - 0.06, wy + wh * 0.45, '#2a2238', 0.03))
            o.append(line(x0 + 0.08, wy + 0.1, x0 + 0.2, wy + 0.3, '#8fa8de', 0.03))        # glint
            win.append((x0, wy, ww, wh))
            c = shutter; sw_ = ww * 0.52
            open_ = r.random() < 0.75
            if open_:
                for sx in (x0 - sw_ - 0.04, x0 + ww + 0.04):
                    o.append(rect(sx, wy - 0.04, sw_, wh + 0.04, c, stroke=INKW, sw=0.02))
                    for k in range(int(wh / 0.1)): o.append(line(sx + 0.05, wy + 0.06 + k * 0.1, sx + sw_ - 0.05, wy + 0.06 + k * 0.1, mul(c, 0.7), 0.025))
            else:
                o.append(rect(x0 - 0.02, wy - 0.02, ww + 0.04, wh + 0.04, c, stroke=INKW, sw=0.02))
                for k in range(int(wh / 0.1)): o.append(line(x0 + 0.04, wy + 0.06 + k * 0.1, x0 + ww - 0.04, wy + 0.06 + k * 0.1, mul(c, 0.7), 0.025))
                o.append(line(x0 + ww / 2, wy, x0 + ww / 2, wy + wh, INKW, 0.02)); win.pop()
            o.append(rect(x0 - 0.12, wy + wh + 0.02, ww + 0.24, 0.07, mul(base, 1.2), stroke=mul(base, 0.6), sw=0.015))      # sill
            if r.random() < 0.7:                                                               # flower box with geraniums
                bx = x0 - 0.08; by = wy + wh + 0.09
                o.append(rect(bx, by, ww + 0.16, 0.2, '#8a4a2a', stroke=INKW, sw=0.02))
                for k in range(7):
                    fx = bx + 0.06 + k * (ww + 0.04) / 6; fy = by - r.uniform(0.02, 0.12)
                    o.append(circ(fx, fy, 0.075, '#3f7a3a'))
                for k in range(6):
                    fx = bx + 0.1 + k * (ww - 0.04) / 5 + r.uniform(-0.03, 0.03); fy = by - r.uniform(0.06, 0.18)
                    o.append(circ(fx, fy, 0.06, r.choice(('#e8343a', '#f04a5a', '#d82a4a', '#ff7a8a'))))
                for k in range(3): o.append(path(f'M{bx + 0.1 + k * 0.25},{by + 0.2} q0.03,0.15 -0.02,0.28', 'none', stroke='#3f7a3a', sw=0.03))
    # ground floor: door + shop arch or window
    dw = 1.25; dx = xs[0] if not shop else xs[-1]; dx -= dw / 2; dy = h - 2.45
    if door_style == 'arch':
        o.append(path(f'M{dx - 0.18},{h} L{dx - 0.18},{dy + 0.6} A{dw / 2 + 0.18},{dw / 2 + 0.18} 0 0 1 {dx + dw + 0.18},{dy + 0.6} L{dx + dw + 0.18},{h} Z', STONE, stroke=INKW, sw=0.025))
        o.append(path(f'M{dx},{h} L{dx},{dy + 0.6} A{dw / 2},{dw / 2} 0 0 1 {dx + dw},{dy + 0.6} L{dx + dw},{h} Z', '#6a3a22', stroke=INKW, sw=0.02))
    else:
        o.append(rect(dx - 0.15, dy - 0.15, dw + 0.3, h - dy + 0.15, STONE, stroke=INKW, sw=0.025)); o.append(rect(dx, dy, dw, h - dy, '#6a3a22', stroke=INKW, sw=0.02))
    for k in range(1, 4): o.append(line(dx + dw * k / 4, dy + 0.4, dx + dw * k / 4, h - 0.05, '#4a2616', 0.02))
    o.append(circ(dx + dw * 0.7, dy + 1.3, 0.045, '#e0b040'))
    if shop:
        sx = xs[0] - 0.9
        o.append(path(f'M{sx},{h} L{sx},{h - 1.8} A0.9,0.9 0 0 1 {sx + 1.8},{h - 1.8} L{sx + 1.8},{h} Z', STONE, stroke=INKW, sw=0.025))
        o.append(path(f'M{sx + 0.12},{h} L{sx + 0.12},{h - 1.8} A0.78,0.78 0 0 1 {sx + 1.68},{h - 1.8} L{sx + 1.68},{h} Z', '#2a2238'))
        win.append((sx + 0.2, h - 2.4, 1.4, 2.3))
        o.append(rect(sx - 0.1, h - 2.95, 2.0, 0.32, '#e8d7a8', stroke=INKW, sw=0.02))           # shop sign with a painted loaf
        o.append(ell(sx + 0.9, h - 2.79, 0.35, 0.1, '#c88a3a', stroke=INKW, sw=0.015))
        for k in range(3): o.append(rect(sx + 0.2 + k * 0.5, h - 0.75, 0.38, 0.3, '#c88a3a', stroke=INKW, sw=0.015, rx=0.08))
    elif nwin > 2:
        for xc in xs[1:]:
            o.append(rect(xc - 0.4, h - 2.2, 0.8, 1.1, '#2a2238', stroke=mul(base, 0.55), sw=0.05)); win.append((xc - 0.4, h - 2.2, 0.8, 1.1))
            for k in range(5): o.append(line(xc - 0.4 + k * 0.2, h - 2.2, xc - 0.4 + k * 0.2, h - 1.1, '#3a2a2a', 0.03))
    o.append(rect(-0.1, -0.1, w + 0.2, h + 0.2, 'none', stroke=mul(base, 0.55), sw=0.08))
    job(name, 0, 0, w, h, 72, ''.join(o)); WINDOWS[name] = win

def church_facade():
    """Church of San Nazaro: facade 9.4 x 13.6 D (gable apex at the top centre; the outline is cut by the geometry).
    Pilasters, portal with lunette fresco, rose window, niches with saints, oculus, inscription band."""
    W, H = 9.4, 13.6; eave = 9.6; base = '#ecd2a0'; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, base)]
    r = random.Random(13)
    for _ in range(14):
        x, y = r.uniform(0, W), r.uniform(3, H); o.append(ell(x, y, r.uniform(0.3, 1.0), r.uniform(0.2, 0.6), mul(base, r.choice((0.92, 0.95, 1.04))), op=0.6))
    o.append(rect(-0.1, H - 1.4, W + 0.2, 1.5, mul(base, 0.86)))
    for px in (0.0, 2.6, W - 3.0, W - 0.4):                                              # pilasters
        o.append(rect(px, H - eave, 0.4, eave, mul(base, 1.08), stroke=mul(base, 0.6), sw=0.03))
        o.append(rect(px - 0.08, H - eave, 0.56, 0.35, mul(base, 1.12), stroke=mul(base, 0.6), sw=0.03))
        o.append(rect(px - 0.08, H - 0.6, 0.56, 0.6, mul(base, 0.95), stroke=mul(base, 0.6), sw=0.03))
    o.append(rect(-0.1, H - eave - 0.4, W + 0.2, 0.42, mul(base, 1.12), stroke=mul(base, 0.6), sw=0.03))          # entablature
    o.append(rect(0.5, H - eave - 0.32, W - 1.0, 0.26, '#d9bd84'))
    for k, ch in enumerate('D.O.M. S. NAZARII'):
        pass
    for k in range(18): o.append(rect(0.9 + k * 0.42, H - eave - 0.26, 0.24, 0.14, '#8a6a3a', op=0.8))          # inscription as letter blocks
    # portal: stone frame, wooden door with studs, lunette fresco, steps drawn by geometry
    cx = W / 2; dw = 2.0; dh = 3.6; dy = H - dh
    o.append(path(f'M{cx - dw / 2 - 0.4},{H} L{cx - dw / 2 - 0.4},{dy - 0.2} L{cx + dw / 2 + 0.4},{dy - 0.2} L{cx + dw / 2 + 0.4},{H} Z', STONE, stroke=INKW, sw=0.04))
    o.append(rect(cx - dw / 2, dy, dw, dh, '#6b3520', stroke=INKW, sw=0.03))
    for k in range(2):
        for j in range(4):
            o.append(rect(cx - dw / 2 + 0.12 + k * dw / 2, dy + 0.15 + j * 0.85, dw / 2 - 0.24, 0.7, '#7d4228', stroke='#4a2414', sw=0.025))
            for q in range(3): o.append(circ(cx - dw / 2 + 0.3 + k * dw / 2 + q * 0.25, dy + 0.5 + j * 0.85, 0.03, '#d8a848'))
    o.append(line(cx, dy, cx, H, '#3a1a10', 0.04))
    o.append(path(f'M{cx - dw / 2 - 0.4},{dy - 0.2} A{dw / 2 + 0.4},{dw / 2 + 0.4} 0 0 1 {cx + dw / 2 + 0.4},{dy - 0.2} Z', STONE, stroke=INKW, sw=0.04))
    o.append(path(f'M{cx - dw / 2},{dy - 0.25} A{dw / 2},{dw / 2} 0 0 1 {cx + dw / 2},{dy - 0.25} Z', '#2f4a8a', stroke=INKW, sw=0.03))       # lunette fresco: blue ground, saint with gold halo
    o.append(circ(cx, dy - 0.75, 0.22, '#f0c040', stroke=INKW, sw=0.02)); o.append(circ(cx, dy - 0.75, 0.13, '#f3dcc0'))
    o.append(path(f'M{cx - 0.35},{dy - 0.25} L{cx - 0.2},{dy - 0.6} L{cx + 0.2},{dy - 0.6} L{cx + 0.35},{dy - 0.25} Z', '#b8342a'))
    o.append(rect(cx - dw / 2 - 0.6, dy - 1.7, dw + 1.2, 0.25, mul(base, 1.12), stroke=mul(base, 0.6), sw=0.03))     # portal cornice
    o.append(poly([(cx - dw / 2 - 0.7, dy - 1.7), (cx, dy - 2.5), (cx + dw / 2 + 0.7, dy - 1.7)], mul(base, 1.05), stroke=mul(base, 0.55), sw=0.04))
    # niches with saints left and right
    for nx in (1.3, W - 1.3):
        ny = H - 6.6
        o.append(path(f'M{nx - 0.5},{ny + 2.2} L{nx - 0.5},{ny + 0.5} A0.5,0.5 0 0 1 {nx + 0.5},{ny + 0.5} L{nx + 0.5},{ny + 2.2} Z', '#7a5a8a', stroke=INKW, sw=0.03))
        o.append(path(f'M{nx - 0.5},{ny + 0.5} A0.5,0.5 0 0 1 {nx + 0.5},{ny + 0.5} L{nx},{ny + 0.5} Z', '#e8b24a', stroke=INKW, sw=0.02))
        o.append(path(f'M{nx - 0.25},{ny + 2.15} L{nx - 0.2},{ny + 1.0} Q{nx},{ny + 0.85} {nx + 0.2},{ny + 1.0} L{nx + 0.25},{ny + 2.15} Z', '#f0e2c4', stroke=INKW, sw=0.02))
        o.append(circ(nx, ny + 0.8, 0.17, '#f0e2c4', stroke=INKW, sw=0.02))
        o.append(rect(nx - 0.6, ny + 2.2, 1.2, 0.15, mul(base, 1.12), stroke=mul(base, 0.6), sw=0.02))
        o.append(rect(nx - 0.45, ny - 1.6, 0.9, 1.4, '#2a2238', stroke=mul(base, 0.55), sw=0.08))      # upper window
        o.append(path(f'M{nx - 0.45},{ny - 1.6} A0.45,0.45 0 0 1 {nx + 0.45},{ny - 1.6} Z', '#2a2238', stroke=mul(base, 0.55), sw=0.08))
    WINDOWS['church_facade'] = [(1.3 - 0.45, H - 6.6 - 1.6, 0.9, 1.4), (W - 1.3 - 0.45, H - 6.6 - 1.6, 0.9, 1.4)]
    # rose window
    ry = H - eave + 2.6; rr = 1.25
    o.append(circ(cx, ry, rr + 0.25, STONE, stroke=INKW, sw=0.05))
    o.append(circ(cx, ry, rr, '#2a3a8a', stroke=INKW, sw=0.03))
    cols = ['#d83a3a', '#f0c040', '#3a8ad8', '#3aa860', '#e07a2a', '#9a4ad0']
    for i in range(12):
        a = 2 * math.pi * i / 12; a2 = 2 * math.pi * (i + 0.5) / 12
        o.append(circ(cx + 0.8 * math.cos(a), ry + 0.8 * math.sin(a), 0.27, cols[i % 6], stroke=STONE, sw=0.07))
        o.append(line(cx + 0.25 * math.cos(a2), ry + 0.25 * math.sin(a2), cx + rr * math.cos(a2), ry + rr * math.sin(a2), STONE, 0.07))
    o.append(circ(cx, ry, 0.3, '#f0c040', stroke=STONE, sw=0.08)); o.append(circ(cx, ry, 0.12, '#d83a3a'))
    WINDOWS['church_rose'] = [(cx - rr, ry - rr, 2 * rr, 2 * rr)]
    # gable: oculus and a painted band of the raking cornice (the geometry cuts the outline)
    o.append(circ(cx, H - eave - 2.2, 0.45, STONE, stroke=INKW, sw=0.04)); o.append(circ(cx, H - eave - 2.2, 0.3, '#2a2238'))
    o.append(rect(-0.1, -0.1, W + 0.2, H + 0.2, 'none', stroke=mul(base, 0.55), sw=0.1))
    job('church_facade', 0, 0, W, H, 80, ''.join(o))

def drum_windows():
    """Spire drum band 1 x 1.4 D: a little arched window between brick piers (tiles around the octagon)."""
    o = [rect(-0.1, -0.1, 1.2, 1.6, '#c4683c')]
    for k in range(9): o.append(line(-0.1, k * 0.16 + 0.05, 1.1, k * 0.16 + 0.05, '#e2b07c', 0.012))
    o.append(path('M0.3,1.2 L0.3,0.5 A0.2,0.2 0 0 1 0.7,0.5 L0.7,1.2 Z', STONE, stroke=INKW, sw=0.02))
    o.append(path('M0.36,1.15 L0.36,0.5 A0.14,0.14 0 0 1 0.64,0.5 L0.64,1.15 Z', '#1f1a34'))
    o.append(rect(0.0, 0.0, 1.0, 0.12, STONE, stroke=INKW, sw=0.015)); o.append(rect(0.0, 1.28, 1.0, 0.12, STONE, stroke=INKW, sw=0.015))
    job('drum', 0, 0, 1.0, 1.4, 256, ''.join(o))

def bell_band():
    """Bronze bell surface along the profile (u around, v = profile from the rim (0) to the crown (1)): two raised rings,
    an inscription band, a relief of a cross and fleurons, green patina streaks."""
    r = random.Random(17); W, H = 4.0, 1.0; B = '#b77d3e'
    o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, B)]
    for _ in range(14):
        x = r.uniform(0, W); o.append(rect(x, r.uniform(0.2, 0.6), r.uniform(0.02, 0.05), r.uniform(0.15, 0.4), '#5f9a7a', op=0.45, rx=0.02))
    for (y, hh, c) in ((0.88, 0.05, '#d7a35a'), (0.82, 0.02, '#7a4a20'), (0.14, 0.04, '#d7a35a'), (0.2, 0.02, '#7a4a20'), (0.6, 0.03, '#d7a35a')):
        o.append(rect(-0.1, H - y - hh, W + 0.2, hh, c))
    for k in range(16):                                         # inscription band between the rings
        o.append(rect(0.1 + k * 0.245, H - 0.78, 0.15, 0.06, '#7a4a20', op=0.9))
    for k in range(4):
        x = 0.5 + k * 1.0; y = H - 0.45
        o.append(rect(x - 0.02, y - 0.12, 0.04, 0.24, '#e0b060')); o.append(rect(x - 0.08, y - 0.06, 0.16, 0.04, '#e0b060'))
        o.append(circ(x + 0.5, y + 0.02, 0.05, '#e0b060'))
    o.append(rect(-0.1, H - 0.06, W + 0.2, 0.08, '#e9bc6e'))
    job('bell', 0, 0, W, H, 256, ''.join(o))

# ----------------------------------------------------------------------------- painted plate (ring) and sky
MODES = ('day', 'dusk', 'night')
PAL = dict(
    day=dict(far='#9aa6dc', far2='#b7bce6', mid='#86a34e', mid2='#b9a650', field='#d5b55e', cyp='#2f5a3a', cyp_s='#21402c',
             wall=['#eab27a', '#e29a62', '#f0cc90', '#de8a5c', '#f1d6a6'], shade=['#a87aa4', '#9a72a0'], roof='#c45a34', roof_s='#8a3a3a',
             tower='#d98a52', win='#5a4a7a', lit=0.0, haze='#c8cdee'),
    dusk=dict(far='#b48ab8', far2='#d6a0b4', mid='#8a6a6a', mid2='#b07a62', field='#d49060', cyp='#3a2e46', cyp_s='#2a2238',
              wall=['#f0a070', '#e88a64', '#f6b880', '#e07a5e', '#f4c28c'], shade=['#8a5a8e', '#7a5288'], roof='#c8543a', roof_s='#7a3448',
              tower='#e88a58', win='#5a3a5a', lit=0.15, haze='#f0b8a8'),
    night=dict(far='#2c3a86', far2='#38489a', mid='#1f3070', mid2='#283a7c', field='#2e4282', cyp='#121c46', cyp_s='#0e163a',
               wall=['#4a5aa6', '#4252a0', '#5262ae', '#3e4e98', '#5868b4'], shade=['#2a3478', '#26306e'], roof='#33397e', roof_s='#22286a',
               tower='#4c5aa8', win='#1a2050', lit=0.35, haze='#3c4c9c'))

def _hill(x0, x1, ybase, amp, seed, n=12):
    r = random.Random(seed); pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; pts.append((x, ybase - amp * (0.4 + 0.6 * abs(math.sin(i * 0.9 + seed))) - r.uniform(0, amp * 0.3)))
    pts[-1] = (pts[-1][0], pts[0][1])                            # seamless: both ends at the same height
    d = f'M{_c(pts[0][0])},{_c(pts[0][1])} ' + ' '.join(f'Q{_c((a[0] + b[0]) / 2)},{_c(min(a[1], b[1]) - amp * 0.15)} {_c(b[0])},{_c(b[1])}' for a, b in zip(pts, pts[1:]))
    return d

def panorama(mode):
    """The painted town plate: 220 x 55 D, wraps seamlessly in u (the ring repeats it twice). Plate y = 0 is z = 53,
    y = 55 is z = -2. Transparent above the hills (the sky dome shows). Far hills in haze, mid hills with fields,
    cypress rows and villas, a dense band of roofs, towers, domes and cypresses with a lit and a shaded side."""
    p = PAL[mode]; r = random.Random(23); W, H = 220.0, 55.0; o = []
    blur = '<filter id="hz" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="0.25"/></filter>'
    for (yb, amp, col, sd) in ((33.0, 9.0, p['far2'], 3), (36.0, 8.0, p['far'], 7)):
        for off in (0, -W):
            d = _hill(off, off + W, yb, amp, sd, n=14) + f' L{_c(off + W)},{H} L{_c(off)},{H} Z'
            o.append(path(d, col))
    # mid hills with field stripes and cypress rows
    for off in (0, -W):
        d = _hill(off, off + W, 41.0, 6.0, 11, n=18) + f' L{_c(off + W)},{H} L{_c(off)},{H} Z'
        o.append(path(d, p['mid']))
    for i in range(40):
        x = r.uniform(0, W); y = r.uniform(37, 44); w = r.uniform(3, 7)
        for xx in _wrap(x, W, w): o.append(ell(xx + w / 2, y, w / 2, r.uniform(0.4, 0.8), r.choice((p['field'], p['mid2'])), op=0.85))
    for i in range(22):                                        # villas on the hills
        x = r.uniform(0, W); y = r.uniform(37.5, 44)
        for xx in _wrap(x, W, 1.2):
            o.append(rect(xx, y - 0.7, 1.1, 0.7, p['wall'][i % 5])); o.append(rect(xx + 0.75, y - 0.7, 0.35, 0.7, p['shade'][0], op=0.8))
            o.append(poly([(xx - 0.1, y - 0.7), (xx + 0.55, y - 1.1), (xx + 1.2, y - 0.7)], p['roof']))
            if p['lit'] and r.random() < p['lit'] * 1.5: o.append(rect(xx + 0.3, y - 0.45, 0.15, 0.2, '#ffcf6a'))
    for i in range(70):                                        # cypresses on the hills
        x = r.uniform(0, W); y = r.uniform(36, 46); h = r.uniform(1.2, 2.2)
        for xx in _wrap(x - 0.2, W, 0.4): o.append(path(f'M{_c(xx + 0.2)},{_c(y - h)} Q{_c(xx + 0.45)},{_c(y - h * 0.4)} {_c(xx + 0.25)},{_c(y)} L{_c(xx + 0.15)},{_c(y)} Q{_c(xx - 0.05)},{_c(y - h * 0.4)} {_c(xx + 0.2)},{_c(y - h)} Z', p['cyp']))
    # town band: back to front rows of houses; towers and domes in between
    o.append(rect(-0.1, 46.5, W + 0.2, 9, p['roof_s']))
    for row in range(4):
        yb = 47.0 + row * 2.4; x = r.uniform(-1, 0)
        while x < W:
            w = r.uniform(2.0, 4.2); h = r.uniform(2.0, 3.6) + row * 0.3; c = r.choice(p['wall'])
            for xx in _wrap(x, W, w):
                o.append(rect(xx, yb - h, w, h + 3, c, stroke=p['roof_s'], sw=0.06))
                o.append(rect(xx + w * 0.7, yb - h, w * 0.3, h + 3, r.choice(p['shade']), op=0.75))
                for k in range(int(w / 0.8)):
                    wx = xx + 0.3 + k * 0.8; lit = p['lit'] and r.random() < p['lit']
                    o.append(rect(wx, yb - h + 0.6, 0.28, 0.42, '#ffd27a' if lit else p['win']))
                    if not lit and mode == 'day': o.append(rect(wx - 0.1, yb - h + 0.58, 0.08, 0.46, SHUTTER[k % 4])); o.append(rect(wx + 0.3, yb - h + 0.58, 0.08, 0.46, SHUTTER[k % 4]))
                roof_h = r.uniform(0.6, 1.0)
                if r.random() < 0.6: o.append(poly([(xx - 0.15, yb - h), (xx + w * 0.5, yb - h - roof_h), (xx + w + 0.15, yb - h)], p['roof'], stroke=p['roof_s'], sw=0.06))
                else: o.append(poly([(xx - 0.15, yb - h), (xx + 0.25, yb - h - roof_h * 0.6), (xx + w - 0.25, yb - h - roof_h * 0.6), (xx + w + 0.15, yb - h)], p['roof'], stroke=p['roof_s'], sw=0.06))
                for k in range(int(w / 0.3)): o.append(line(xx + 0.1 + k * 0.3, yb - h - 0.05, xx + 0.1 + k * 0.3, yb - h - roof_h * 0.45, p['roof_s'], 0.04, op=0.5))
            x += w + r.uniform(-0.2, 0.4)
        if row == 0:
            for i in range(9):                                 # other towers and domes behind the first row
                tx = r.uniform(0, W); th = r.uniform(7, 13); tw = r.uniform(1.1, 1.8)
                for xx in _wrap(tx, W, tw):
                    if i % 3 == 2:
                        o.append(rect(xx - 0.6, yb - 4.5, tw + 1.2, 4.5, p['wall'][2], stroke=p['roof_s'], sw=0.06))
                        o.append(path(f'M{_c(xx - 0.6)},{_c(yb - 4.5)} A{_c(tw / 2 + 0.6)},{_c(tw / 2 + 1.0)} 0 0 1 {_c(xx + tw + 0.6)},{_c(yb - 4.5)} Z', p['roof'], stroke=p['roof_s'], sw=0.06))
                        o.append(rect(xx + tw / 2 - 0.15, yb - 4.5 - tw / 2 - 1.6, 0.3, 0.6, p['wall'][4]))
                    else:
                        o.append(rect(xx, yb - th, tw, th, p['tower'], stroke=p['roof_s'], sw=0.06))
                        o.append(rect(xx + tw * 0.65, yb - th, tw * 0.35, th, p['shade'][1], op=0.7))
                        o.append(path(f'M{_c(xx + 0.2)},{_c(yb - th + 1.6)} L{_c(xx + 0.2)},{_c(yb - th + 0.8)} A{_c(tw / 2 - 0.2)},{_c(tw / 2 - 0.2)} 0 0 1 {_c(xx + tw - 0.2)},{_c(yb - th + 0.8)} L{_c(xx + tw - 0.2)},{_c(yb - th + 1.6)} Z', p['win']))
                        o.append(poly([(xx - 0.15, yb - th), (xx + tw / 2, yb - th - 2.2), (xx + tw + 0.15, yb - th)], p['roof'], stroke=p['roof_s'], sw=0.06))
        for i in range(12):                                    # cypresses between the rows
            x = r.uniform(0, W); h = r.uniform(3.0, 5.5)
            for xx in _wrap(x - 0.35, W, 0.7):
                o.append(path(f'M{_c(xx + 0.35)},{_c(yb - h)} Q{_c(xx + 0.8)},{_c(yb - h * 0.45)} {_c(xx + 0.45)},{_c(yb + 0.5)} L{_c(xx + 0.25)},{_c(yb + 0.5)} Q{_c(xx - 0.1)},{_c(yb - h * 0.45)} {_c(xx + 0.35)},{_c(yb - h)} Z', p['cyp'], stroke=p['cyp_s'], sw=0.05))
    # haze over the far layers is in their colours; a thin light line on the hill crests
    job('pano_' + mode, 0, 0, W, H, 18.62, ''.join(o), defs=blur, transparent=True)

SKY = dict(
    day=dict(stops=[(0, '#3a5ea6'), (0.45, '#5a84c6'), (0.8, '#8cb0e0'), (0.88, '#c4c8e0'), (1, '#e6d4c4')], cloud='#f6f2fb', cloud_b='#c4b4e4', n=16, dark=False),
    dusk=dict(stops=[(0, '#4a4aa6'), (0.4, '#7a66b6'), (0.62, '#e0907c'), (0.8, '#f8b47a'), (0.9, '#ffd690'), (1, '#ffe2a8')], cloud='#ffd4a8', cloud_b='#7a64b0', n=12, dark=False),
    storm=dict(stops=[(0, '#0c1030'), (0.5, '#182050'), (0.8, '#283270'), (1, '#36428a')], cloud='#262c62', cloud_b='#12163a', n=34, dark=True),
    night=dict(stops=[(0, '#101c5a'), (0.5, '#1a2e82'), (0.82, '#2a4ca0'), (1, '#3a5cae')], cloud='#34489a', cloud_b='#1e2a66', n=9, dark=True))

def sky(mode):
    """Sky dome texture: u = azimuth (0..1 counter-clockwise from +x), v = elevation from -15 deg (bottom) to 90 deg (top).
    SVG 360 x 105 units: x = azimuth in degrees, y = 90 - elevation. Soft clouds (flat lavender bottoms), sun glow,
    moon, stars, storm masses. Azimuths: dusk sun at 190 deg (west, just south), moon at 215 deg."""
    s = SKY[mode]; r = random.Random(31); W, H = 360.0, 105.0
    g = '<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">' + ''.join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in s['stops']) + '</linearGradient>'
    g += '<filter id="b" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="0.9"/></filter>'
    g += '<filter id="b2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
    g += '<radialGradient id="glow"><stop offset="0" stop-color="#fff4d0" stop-opacity="1"/><stop offset="0.25" stop-color="#ffd890" stop-opacity="0.8"/><stop offset="1" stop-color="#ffb070" stop-opacity="0"/></radialGradient>'
    g += '<radialGradient id="mglow"><stop offset="0" stop-color="#e8eeff" stop-opacity="0.9"/><stop offset="0.3" stop-color="#a8b8f0" stop-opacity="0.35"/><stop offset="1" stop-color="#6070c0" stop-opacity="0"/></radialGradient>'
    o = [rect(-1, -1, W + 2, H + 2, 'url(#g)')]
    if mode == 'dusk':
        o.append(ell(190, 90 - 8, 70, 30, 'url(#glow)'))
        o.append(circ(190, 90 - 7, 4.5, '#fff6dc'))
        for k in range(14):                                    # painted sun rays (ref a/t0062)
            a = -math.pi * (k + 0.5) / 14; o.append(poly([(190, 83), (190 + 90 * math.cos(a - 0.03), 83 + 60 * math.sin(a - 0.03)), (190 + 90 * math.cos(a + 0.03), 83 + 60 * math.sin(a + 0.03))], '#fff0c8', op=0.12))
    if mode in ('night', 'storm'):
        for _ in range(260 if mode == 'night' else 60):
            x, y = r.uniform(0, W), r.uniform(0, 70); o.append(circ(x, y, r.uniform(0.08, 0.22), '#f4f0ff', op=r.uniform(0.4, 1.0)))
        if mode == 'night':
            o.append(circ(215, 90 - 38, 16, 'url(#mglow)')); o.append(circ(215, 90 - 38, 3.6, '#f6f4e6')); o.append(circ(214, 90 - 38.6, 0.9, '#d8d6c6')); o.append(circ(216.4, 90 - 37, 0.6, '#d8d6c6'))
        else:
            o.append(circ(215, 90 - 38, 26, 'url(#mglow)', op=0.7))
    # clouds: flat bottom, rounded overlapping puffs on top, blurred edge, lavender underside (ref a/t0062, a/t0072)
    for i in range(s['n']):
        cx = r.uniform(0, W); el = r.uniform(5, 38) if mode != 'storm' else r.uniform(3, 55); cy = 90 - el
        w = r.uniform(16, 34) * (2.0 if mode == 'storm' else 1.0) * (1.0 - 0.006 * el)
        for xx in _wrap(cx - w / 2, W, w):
            xc = xx + w / 2; grp = []; nb = r.randint(3, 5); rs = []
            for k in range(nb):
                t = (k + 0.5) / nb; rk = w * r.uniform(0.13, 0.2) * (1.25 - abs(t - 0.5)); rs.append((xc - w / 2 + w * (0.1 + 0.8 * t), rk))
            top = s['cloud']; under = s['cloud_b']
            for (bx, rk) in rs: grp.append(circ(bx, cy - rk * 0.55, rk, top))
            grp.append(rect(xc - w / 2, cy - w * 0.09, w, w * 0.09, top, rx=w * 0.04))
            grp.append(rect(xc - w / 2 + 0.6, cy - w * 0.045, w - 1.2, w * 0.045, under, rx=w * 0.02))
            if mode == 'storm':
                for (bx, rk) in rs: grp.append(circ(bx - rk * 0.2, cy - rk * 1.2, rk * 0.35, '#4a54a0', op=0.55))
            o.append('<g filter="url(#b)" opacity="%.2f">' % (0.96 if mode != 'storm' else 0.92) + ''.join(grp) + '</g>')
    if mode == 'storm':
        for i in range(8):                                     # low storm band over the horizon
            x = i * 45 + r.uniform(0, 20); o.append('<g filter="url(#b2)">' + ell(x, 90 - 3, 40, 9, '#0a0e28', op=0.85) + '</g>')
    job('sky_' + mode, 0, 0, W, H, 2048 / 360.0, ''.join(o), defs=g)

def ground():
    """Far ground disc between the town houses and the plate: gardens, lanes, roofs seen from above (10 x 10 D tile)."""
    r = random.Random(41); o = [rect(-0.1, -0.1, 10.2, 10.2, '#a89a58')]
    for _ in range(26):
        x, y = r.uniform(0, 10), r.uniform(0, 10); w, h = r.uniform(0.8, 2.4), r.uniform(0.8, 2.0)
        for xx in _wrap(x, 10, w): o.append(rect(xx, y, w, h, r.choice(('#8f9a48', '#b8a45c', '#c8935a', '#7f8c44', '#c2724a')), rx=0.1))
    for _ in range(30):
        x, y = r.uniform(0, 10), r.uniform(0, 10); o.append(circ(x, y, r.uniform(0.2, 0.5), '#4a6a34'))
    job('ground', 0, 0, 10, 10, 64, ''.join(o))

def lantern_glass():
    o = [rect(0, 0, 1, 1, '#ffd890'), rect(0.1, 0.1, 0.8, 0.8, '#fff2c0'), line(0.5, 0, 0.5, 1, '#6a4a2a', 0.06)]
    job('lantern', 0, 0, 1, 1, 64, ''.join(o))


def voussoirs():
    """Archivolt ring strip 1.0 x 0.3 D (u along the arc, v across): wedge stones with ink joints and edges."""
    o = [rect(-0.1, -0.1, 1.2, 0.5, STONE)]
    for k in range(4):
        x = k * 0.25; c = mul(STONE, (1.04, 0.95, 1.0, 0.91)[k])
        o.append(rect(x + 0.01, 0.02, 0.23, 0.26, c)); o.append(line(x + 0.03, 0.06, x + 0.21, 0.06, mul(c, 1.1), 0.02))
        o.append(line(x, 0, x, 0.3, INKW, 0.016))
    o.append(line(-0.1, 0.008, 1.1, 0.008, INKW, 0.03)); o.append(line(-0.1, 0.292, 1.1, 0.292, INKW, 0.03))
    job('vous', 0, 0, 1.0, 0.3, 256, ''.join(o))

def town_wall(name, base, seed, night=False):
    """Mid-town house wall tile 2.4 x 3.0 D: plaster, one window with shutters and sill, a string line; night version:
    some windows lit (and the matching glow mask name + '_glow')."""
    r = random.Random(seed); o = [rect(-0.1, -0.1, 2.6, 3.2, base)]; g = [rect(-0.1, -0.1, 2.6, 3.2, '#000000')]
    for _ in range(4): o.append(ell(r.uniform(0, 2.4), r.uniform(0, 3), r.uniform(0.2, 0.6), r.uniform(0.2, 0.5), mul(base, r.choice((0.9, 1.06))), op=0.6))
    o.append(line(-0.1, 2.95, 2.5, 2.95, mul(base, 0.75), 0.05))
    for (x, y) in ((0.35, 0.8), (1.45, 0.8)):
        lit = night and r.random() < 0.45
        o.append(rect(x - 0.08, y - 0.08, 0.76, 1.26, mul(base, 1.15)))
        o.append(rect(x, y, 0.6, 1.1, '#ffc96a' if lit else '#2a2238'))
        if lit: g.append(rect(x, y, 0.6, 1.1, '#ffc060'))
        o.append(line(x + 0.3, y, x + 0.3, y + 1.1, '#3a2a2a', 0.04))
        o.append(rect(x - 0.32, y, 0.3, 1.1, SHUTTER[seed % 4], stroke=INKW, sw=0.02)); o.append(rect(x + 0.62, y, 0.3, 1.1, SHUTTER[seed % 4], stroke=INKW, sw=0.02))
        o.append(rect(x - 0.1, y + 1.12, 0.8, 0.08, mul(base, 1.2)))
    job(name, 0, 0, 2.4, 3.0, 64, ''.join(o))
    if night: job(name + '_glow', 0, 0, 2.4, 3.0, 32, ''.join(g))

HOUSES = [  # name, width, eave height, depth, plaster colour, floors, seed, shutter, door, shop
    ('house_a', 5.2, 9.0, 6.0, '#d8743e', 2, 51, SHUTTER[0], 'arch', True),
    ('house_b', 4.6, 10.6, 6.0, '#e6b24c', 3, 52, SHUTTER[1], 'rect', False),
    ('house_c', 4.8, 8.4, 6.0, '#e09078', 2, 53, SHUTTER[2], 'arch', False),
    ('house_d', 6.0, 9.6, 5.0, '#eac48a', 2, 54, SHUTTER[3], 'rect', True),
    ('house_e', 5.0, 8.0, 5.0, '#c9603a', 2, 55, SHUTTER[0], 'arch', False),
]
PLASTERS = dict(pl_terra='#d8743e', pl_ochre='#e6b24c', pl_pink='#e09078', pl_cream='#eac48a', pl_red='#c9603a')

def all_jobs():
    JOBS.clear(); SIZE.clear(); WINDOWS.clear()
    brick(); brick('brick_in', seed=4, dark=0.8); stone(); archetti(); coppi(); coppi('roof_b', '#a84a30', 6); scales(); cobbles(); planks(); wood_beam(); clock_face()
    for n, c in PLASTERS.items(): plaster(n, c, hash(n) % 1000 if False else sum(map(ord, n)))
    for (n, w, h, d, c, f, sd, sh, door, shop) in HOUSES: house_facade(n, w, h, c, f, sd, sh, door, shop)
    voussoirs()
    for i, (n, c) in enumerate(PLASTERS.items()): town_wall('tw_' + n[3:], c, 60 + i); town_wall('tw_' + n[3:] + '_n', c, 60 + i, night=True)
    church_facade(); drum_windows(); bell_band(); ground(); lantern_glass()
    for m in MODES: panorama(m)
    for m in SKY: sky(m)

def ensure(verbose=True):
    """Draw every texture, rasterise the changed ones (one Chromium launch), return {name: png path}."""
    os.makedirs(TEX, exist_ok=True); os.makedirs(WORK, exist_ok=True)
    all_jobs()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    for name, j in JOBS.items():
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
