#!/usr/bin/env python3
"""harbor_tex.py : artwork of the molasses-tank set (Boston waterfront, January 1919), drawn as SVG in Python and rasterised by
headless Chromium (PROJ/v3/set3d/raster.js, one launch for all changed textures). Cached in v3/set3d3/tex_harbor/ by content hash.
Same route as v3/set3d2/tower_tex.py, whose SVG helpers, job() registry, cobbles and sky painter are imported and reused.

    import harbor_tex as HT
    paths = HT.ensure()        # {name: png path}
    HT.SIZE[name] -> (w_D, h_D) of one image / tile

Every surface is drawn in the colour it shows in neutral light; the lit material makes sun and shade of it.
Deterministic: every random choice comes from random.Random(fixed seed)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d2'))
import tower_tex as TT                                                     # noqa: E402  (helpers, job registry, sky painter)
from tower_tex import rect, poly, pline, line, circ, ell, path, mul, mix, _wrap, _c   # noqa: E402,F401

TEX = os.path.join(HERE, 'tex_harbor'); WORK = os.path.join(HERE, 'harbor_work')
RASTER = TT.RASTER
SIZE = TT.SIZE
job = TT.job
INKW = '#3b1f1a'

# ----------------------------------------------------------------------------- the tank (dimensions shared with harbor.py)
TANK_R = 13.0; TANK_H = 24.0; COURSE = 3.0; NPL = 12            # 6 courses of 3 D, 12 plates round
PW = 2 * math.pi * TANK_R / NPL                                  # plate width along the wall (6.81 D)
TILE_W = 3 * PW                                                  # one texture tile = 3 plates (repeats 4 times round)
SEAM_U = PW                                                      # the bucket seam: vertical seam of the lowest course at u = PW
STEEL = ['#7e7c88', '#868290', '#78768a', '#8a8484', '#807c8c']
PAINT = ['#704626', '#6c4324', '#754a28', '#6a4224']
MOL = '#3a1a0a'

def _rivet(o, x, y, base, r=0.042):
    o.append(circ(x + 0.012, y + 0.014, r, mul(base, 0.55)))           # shadow side (lower right)
    o.append(circ(x, y, r, mul(base, 1.08)))
    o.append(circ(x - 0.012, y - 0.012, r * 0.45, mul(base, 1.32)))     # glint

def tank_art(state, seed=11):
    """Body of the tank tile (TILE_W x TANK_H D, y down: y = 0 is the top of the wall). state 0: weathered grey steel with dark
    molasses streaks under the seams; 1: painted brown, no streaks."""
    r = random.Random(seed); W, H = TILE_W, TANK_H; o = []; pal = STEEL if state == 0 else PAINT
    o.append(rect(-0.2, -0.2, W + 0.4, H + 0.4, pal[0]))
    nco = int(H / COURSE)
    for c in range(nco):                                                 # plates: course c from the bottom
        y0 = H - (c + 1) * COURSE; off = (c % 2) * PW / 2
        for k in range(-1, 4):
            x0 = k * PW + off; col = mul(r.choice(pal), r.uniform(0.96, 1.04))
            for xx in _wrap(x0, W, PW): o.append(rect(xx, y0, PW, COURSE, col))
            for _ in range(5):                                           # mill scale / brush mottling
                cx, cy = x0 + r.uniform(0.3, PW - 0.3), y0 + r.uniform(0.3, COURSE - 0.3)
                for xx in _wrap(cx - 0.8, W, 1.6): o.append(ell(xx + 0.8, cy, r.uniform(0.4, 1.1), r.uniform(0.15, 0.5), mul(col, r.choice((0.93, 1.06))), op=0.5))
            if state == 1:
                for _ in range(10):                                      # brush strokes
                    cx, cy = x0 + r.uniform(0, PW), y0 + r.uniform(0.1, COURSE - 0.1)
                    for xx in _wrap(cx, W, 1.2): o.append(line(xx, cy, xx + r.uniform(0.6, 1.2), cy + r.uniform(-0.03, 0.03), mul(col, r.choice((0.9, 1.1))), 0.04, op=0.6))
            elif r.random() < 0.6:                                       # rust blush on the grey steel (warm accent)
                cx, cy = x0 + r.uniform(0.5, PW - 0.5), y0 + r.uniform(0.6, COURSE - 0.4)
                for xx in _wrap(cx - 0.6, W, 1.2): o.append(ell(xx + 0.6, cy, r.uniform(0.3, 0.7), r.uniform(0.2, 0.5), '#a8603a', op=0.28))
    # streaks first (under the rivet heads), state 0 only
    if state == 0:
        def streak(x, y, L, w, op):
            pts = f'M{_c(x - w / 2)},{_c(y)} L{_c(x + w / 2)},{_c(y)} Q{_c(x + w * 0.35)},{_c(y + L * 0.6)} {_c(x + w * 0.12)},{_c(y + L)} L{_c(x - w * 0.12)},{_c(y + L)} Q{_c(x - w * 0.35)},{_c(y + L * 0.6)} {_c(x - w / 2)},{_c(y)} Z'
            for dx in (0, W, -W):
                if -1 < x + dx < W + 1:
                    o.append(path(pts.replace('M', 'M', 1), MOL, op=op, extra=f' transform="translate({_c(dx)},0)"'))
                    o.append(ell(x + dx, y + L, w * 0.22, w * 0.3, MOL, op=min(1, op + 0.1)))
        for c in range(1, nco):                                          # under the horizontal seams, denser low down
            ys = H - c * COURSE + 0.14; n = int((14, 11, 8, 6, 5, 4, 3)[c - 1] * W / TILE_W)
            for _ in range(n):
                x = r.uniform(0, W); L = r.uniform(0.3, 1.0 + 1.8 * (nco - c) / nco); streak(x, ys, L, r.uniform(0.04, 0.12), r.uniform(0.55, 0.9))
        for c in range(nco):                                             # down the vertical seams
            y0 = H - (c + 1) * COURSE; off = (c % 2) * PW / 2
            for k in range(3):
                xs = (k * PW + off) % W
                for _ in range(2 if c < 3 else 1):
                    y = y0 + r.uniform(0.1, COURSE - 0.8); streak(xs + r.choice((-0.11, 0.11)), y, r.uniform(0.3, 1.2), r.uniform(0.04, 0.09), r.uniform(0.5, 0.85))
        streak(SEAM_U, H - COURSE + 0.14, 2.3, 0.16, 0.95)               # the bucket seam: a long run down to the bucket
        streak(SEAM_U + 0.1, H - COURSE + 0.9, 1.6, 0.08, 0.9)
        streak(SEAM_U - 0.12, H - 2 * COURSE + 0.14, 1.4, 0.1, 0.85)
    # seams: lap lines and two rivet rows on the horizontal seams, butt line and two rivet columns on the vertical seams
    for c in range(1, nco):
        ys = H - c * COURSE; base = mul(pal[0], 1.0)
        o.append(line(-0.2, ys + 0.03, W + 0.2, ys + 0.03, mul(base, 0.45), 0.05))
        o.append(line(-0.2, ys - 0.02, W + 0.2, ys - 0.02, mul(base, 1.25), 0.025))
        for dy in (-0.14, 0.15):
            n = int(W / 0.25)
            for i in range(n): _rivet(o, (i + 0.5) * W / n, ys + dy, base)
    for c in range(nco):
        y0 = H - (c + 1) * COURSE; off = (c % 2) * PW / 2; base = pal[0]
        for k in range(3):
            xs = (k * PW + off) % W
            for xx in (xs, xs + W, xs - W):
                if -1 < xx < W + 1:
                    o.append(line(xx, y0 + 0.2, xx, y0 + COURSE - 0.2, mul(base, 0.45), 0.04)); o.append(line(xx - 0.03, y0 + 0.2, xx - 0.03, y0 + COURSE - 0.2, mul(base, 1.22), 0.02))
                    for dx in (-0.13, 0.13):
                        for i in range(11): _rivet(o, xx + dx, y0 + 0.3 + i * (COURSE - 0.6) / 10, base)
    o.append(rect(-0.2, -0.2, W + 0.4, 0.32, mul(pal[0], 0.82)))       # top angle ring shadow band
    o.append(rect(-0.2, H - 0.25, W + 0.4, 0.45, mul(pal[0], 0.72)))     # foot, splashed
    return ''.join(o)

def tank_textures():
    for st, nm in ((0, 'tank_grey'), (1, 'tank_brown')):
        body = tank_art(st)
        job(nm, 0, 0, TILE_W, TANK_H, 60, body)
        job(nm + '_patch', SEAM_U - 3.0, TANK_H - 7.0, 6.0, 7.0, 150, body)   # hero patch round the bucket seam (z 0..7)

# ----------------------------------------------------------------------------- trestle (elevated railway), dark green riveted steel
GREEN = '#2f5d40'; GREEN_D = '#244a34'
def girder():
    """Plate girder face 6 x 1.4 D (tile along the length): web, flange angles top and bottom, stiffener angles, rivets, soot."""
    r = random.Random(5); W, H = 6.0, 1.4; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, GREEN)]
    for _ in range(10):
        x = r.uniform(0, W); y = r.uniform(0.2, 1.2)
        for xx in _wrap(x - 0.5, W, 1.0): o.append(ell(xx + 0.5, y, r.uniform(0.2, 0.6), r.uniform(0.1, 0.3), mul(GREEN, r.choice((0.85, 1.12))), op=0.6))
    for y0 in (0.0, H - 0.26):
        o.append(rect(-0.1, y0, W + 0.2, 0.26, mul(GREEN, 1.14))); o.append(line(-0.1, y0 + (0.25 if y0 == 0 else 0.01), W + 0.1, y0 + (0.25 if y0 == 0 else 0.01), mul(GREEN, 0.5), 0.025))
        for i in range(48): _rivet(o, (i + 0.5) * W / 48, y0 + 0.13, GREEN, r=0.03)
    for k in range(4):
        x = k * 1.5 + 0.75; o.append(rect(x - 0.1, 0.26, 0.2, H - 0.52, mul(GREEN, 1.12))); o.append(line(x + 0.1, 0.26, x + 0.1, H - 0.26, mul(GREEN, 0.5), 0.025))
        for i in range(6): _rivet(o, x, 0.36 + i * 0.14, GREEN, r=0.028)
    for _ in range(5):                                                   # rust weeping from the rivets
        x = r.uniform(0, W); o.append(rect(x, 0.3, 0.05, r.uniform(0.2, 0.6), '#8a4a2a', op=0.35, rx=0.02))
    job('girder', 0, 0, W, H, 110, ''.join(o))

def column():
    """Latticed column face 0.6 x 2 D: two channel flanges and laced diagonal bars over a dark gap."""
    W, H = 0.6, 2.0; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#14241c')]
    o.append(rect(0, -0.1, 0.13, H + 0.2, mul(GREEN, 1.1))); o.append(rect(W - 0.13, -0.1, 0.13, H + 0.2, mul(GREEN, 1.0)))
    for k in range(-1, 5):
        y = k * 0.5
        o.append(line(0.08, y, W - 0.08, y + 0.5, GREEN, 0.06)); o.append(line(W - 0.08, y + 0.25, 0.08, y + 0.75, mul(GREEN, 0.9), 0.06))
    for i in range(12): _rivet(o, 0.065, (i + 0.5) * H / 12, GREEN, r=0.022); _rivet(o, W - 0.065, (i + 0.5) * H / 12, GREEN, r=0.022)
    job('column', 0, 0, W, H, 160, ''.join(o))

# ----------------------------------------------------------------------------- facades (Boston 1919: red brick rows, ochre warehouses)
def _brick_defs(pid, base, mortar, ch=0.22, bl=0.5):
    return (f'<pattern id="{pid}" width="{_c(bl)}" height="{_c(2 * ch)}" patternUnits="userSpaceOnUse">'
            f'{rect(0, 0, bl, 2 * ch, mortar)}{rect(0.012, 0.012, bl - 0.024, ch - 0.024, base)}'
            f'{rect(-bl / 2 + 0.012, ch + 0.012, bl - 0.024, ch - 0.024, mul(base, 0.95))}{rect(bl / 2 + 0.012, ch + 0.012, bl - 0.024, ch - 0.024, mul(base, 1.04))}</pattern>')

def facade(name, w, h, base, kind, floors, seed, trim='#e8dcc4', door='#3e5a3a', sign='#2f4a3a'):
    """Street front w x h D (h = parapet/eave height). kind 'row' (tenement: sash windows, granite lintels, shop front with sign
    board and awning band, stoop door), 'ware' (warehouse: tall arched windows with green frames, loading doors, hoist door,
    painted sign band). Brick drawn as a pattern; stains darker toward the ground."""
    r = random.Random(seed); o = []; mort = mix(base, '#d8c8b0', 0.55)
    defs = _brick_defs('b' + name, base, mort)
    o.append(rect(-0.1, -0.1, w + 0.2, h + 0.2, f'url(#b{name})'))
    for _ in range(10):
        x, y = r.uniform(0, w), r.uniform(0, h); o.append(ell(x, y, r.uniform(0.5, 1.5), r.uniform(0.3, 1.0), mul(base, r.choice((0.86, 0.9, 1.1))), op=0.35))
    o.append(rect(-0.1, h - 1.0, w + 0.2, 1.1, '#3a2228', op=0.18))
    o.append(rect(-0.1, -0.1, w + 0.2, 0.55, mul(base, 0.7)))                       # cornice shadow band
    gf = 4.0; fl = (h - gf - 0.8) / floors
    nwin = max(2, int(round(w / (2.3 if kind == 'row' else 2.8))))
    xs = [w * (i + 0.5) / nwin for i in range(nwin)]
    for f in range(floors):
        top = 0.8 + f * fl; ww = 0.95 if kind == 'row' else 1.25; wh = min(fl - 0.9, 1.9)
        wy = top + (fl - wh) * 0.45
        for xc in xs:
            x0 = xc - ww / 2
            if kind == 'row':
                o.append(rect(x0 - 0.12, wy - 0.28, ww + 0.24, 0.26, '#d6c8ae', stroke=mul('#d6c8ae', 0.6), sw=0.02))   # granite lintel
                o.append(rect(x0 - 0.1, wy + wh, ww + 0.2, 0.12, '#d6c8ae', stroke=mul('#d6c8ae', 0.6), sw=0.02))     # sill
                o.append(rect(x0, wy, ww, wh, trim))
                for (py, ph) in ((wy + 0.07, wh / 2 - 0.1), (wy + wh / 2 + 0.03, wh / 2 - 0.1)):
                    for (px, pw_) in ((x0 + 0.07, ww / 2 - 0.1), (x0 + ww / 2 + 0.03, ww / 2 - 0.1)):
                        o.append(rect(px, py, pw_, ph, '#2c3058')); o.append(line(px + 0.05, py + 0.08, px + pw_ * 0.6, py + ph * 0.5, '#8aa4d8', 0.03, op=0.7))
                if r.random() < 0.3: o.append(rect(x0 + 0.06, wy + 0.06, ww - 0.12, wh * 0.42, '#efe2c4'))     # drawn blind
            else:
                rr = ww / 2
                o.append(path(f'M{_c(x0 - 0.14)},{_c(wy + wh)} L{_c(x0 - 0.14)},{_c(wy + rr)} A{_c(rr + 0.14)},{_c(rr + 0.14)} 0 0 1 {_c(x0 + ww + 0.14)},{_c(wy + rr)} L{_c(x0 + ww + 0.14)},{_c(wy + wh)} Z', mul(base, 0.78)))
                o.append(path(f'M{_c(x0)},{_c(wy + wh)} L{_c(x0)},{_c(wy + rr)} A{_c(rr)},{_c(rr)} 0 0 1 {_c(x0 + ww)},{_c(wy + rr)} L{_c(x0 + ww)},{_c(wy + wh)} Z', '#3f6a48'))
                for (py, ph) in ((wy + rr * 0.6, wh * 0.36), (wy + rr * 0.6 + wh * 0.4, wh * 0.36)):
                    for j in range(3): o.append(rect(x0 + 0.08 + j * (ww - 0.16) / 3 + 0.02, max(py, wy + 0.25), (ww - 0.16) / 3 - 0.04, ph - 0.05, '#2a2c50'))
                o.append(rect(x0 - 0.1, wy + wh, ww + 0.2, 0.12, '#d6c8ae'))
    # ground floor
    o.append(rect(-0.1, h - gf - 0.2, w + 0.2, 0.22, '#d6c8ae', stroke=mul('#d6c8ae', 0.6), sw=0.02))   # granite belt course
    if kind == 'row':
        sw_ = w * 0.55; sx = 0.4
        o.append(rect(sx, h - gf + 0.1, sw_, 0.6, sign, stroke=INKW, sw=0.03))                       # sign board with gilt blocks
        for k in range(int(sw_ / 0.5) - 1): o.append(rect(sx + 0.35 + k * 0.5, h - gf + 0.27, 0.32, 0.26, '#e0b450', rx=0.04))
        o.append(rect(sx, h - gf + 0.75, sw_, 0.35, r.choice(('#c43c32', '#2f6a8a', '#3f7a4a')))) # awning band
        for k in range(int(sw_ / 0.4)): o.append(rect(sx + k * 0.4, h - gf + 0.75, 0.2, 0.35, '#efe6d0', op=0.9))
        o.append(rect(sx + 0.2, h - gf + 1.25, sw_ - 0.4, 2.15, '#2c3058', stroke=trim, sw=0.12))   # shop window
        for k in range(1, 4): o.append(line(sx + 0.2 + k * (sw_ - 0.4) / 4, h - gf + 1.25, sx + 0.2 + k * (sw_ - 0.4) / 4, h - 0.6, trim, 0.06))
        o.append(line(sx + 0.5, h - gf + 1.5, sx + 1.4, h - gf + 2.6, '#8aa4d8', 0.05, op=0.6))
        o.append(rect(sx + 0.2, h - 0.6, sw_ - 0.4, 0.6, mul(base, 0.8)))
        dx = sx + sw_ + 0.6; dw = 1.25
        o.append(rect(dx - 0.18, h - 3.2, dw + 0.36, 3.2, '#d6c8ae', stroke=INKW, sw=0.03)); o.append(rect(dx, h - 3.0, dw, 2.7, door, stroke=INKW, sw=0.03))
        o.append(rect(dx + 0.12, h - 2.85, dw - 0.24, 0.9, '#2c3058')); o.append(circ(dx + dw * 0.8, h - 1.6, 0.05, '#e0b450'))
        for k in range(3): o.append(rect(dx - 0.3 - k * 0.1, h - 0.3 + k * 0.1 - 0.2, dw + 0.6 + k * 0.2, 0.1, '#c8bca4', stroke=mul('#c8bca4', 0.6), sw=0.015))
        if dx + dw + 0.8 < w - 1.0:
            for xc in [x for x in xs if x > dx + dw + 0.9]:
                o.append(rect(xc - 0.5, h - gf + 0.8, 1.0, 1.8, trim)); o.append(rect(xc - 0.42, h - gf + 0.88, 0.84, 1.64, '#2c3058'))
    else:
        o.append(rect(0.3, h - gf - 1.2, w - 0.6, 0.85, sign, stroke=INKW, sw=0.03))                 # painted sign band
        for k in range(int((w - 1.2) / 0.6)): o.append(rect(0.7 + k * 0.6, h - gf - 1.05, 0.4, 0.55, '#ead8a8', rx=0.03))
        for i, xc in enumerate(xs):
            if i % 2 == 0:                                                                           # loading door
                o.append(rect(xc - 1.15, h - 3.4, 2.3, 3.4, mul(base, 0.75))); o.append(rect(xc - 1.0, h - 3.25, 2.0, 3.25, door, stroke=INKW, sw=0.03))
                for k in range(1, 6): o.append(line(xc - 1.0 + k * 2.0 / 6, h - 3.25, xc - 1.0 + k * 2.0 / 6, h, mul(door, 0.7), 0.03))
                o.append(line(xc - 1.0, h - 3.25, xc + 1.0, h, mul(door, 0.7), 0.05)); o.append(line(xc + 1.0, h - 3.25, xc - 1.0, h, mul(door, 0.7), 0.05))
            else:
                o.append(rect(xc - 0.7, h - 3.0, 1.4, 1.9, '#2a2c50', stroke='#3f6a48', sw=0.1))
        if nwin >= 3:                                                                                # hoist door and beam high up
            xc = xs[1]; o.append(rect(xc - 0.6, 1.0, 1.2, 2.0, door, stroke=INKW, sw=0.03)); o.append(rect(xc - 0.08, 0.55, 0.16, 0.5, '#4a3020'))
    o.append(rect(-0.1, -0.1, w + 0.2, h + 0.2, 'none', stroke=mul(base, 0.5), sw=0.1))
    job(name, 0, 0, w, h, 56, ''.join(o), defs=defs)

FACADES = [  # name, w, h, base, kind, floors, seed, door, sign
    ('fa_row_a', 11.0, 13.0, '#a8442e', 'row', 3, 101, '#3e5a3a', '#2f4a3a'),
    ('fa_row_b', 9.0, 11.0, '#b85a36', 'row', 2, 102, '#6a2a22', '#5a2430'),
    ('fa_row_c', 12.0, 14.5, '#94402e', 'row', 3, 103, '#2a3e5a', '#3a2a4a'),
    ('fa_row_d', 10.0, 12.0, '#c0663c', 'row', 3, 104, '#3e5a3a', '#2a4a5a'),
    ('fa_ware_a', 16.0, 12.0, '#d29a48', 'ware', 2, 111, '#3f6a48', '#5a2a22'),
    ('fa_ware_b', 13.0, 10.0, '#c88a40', 'ware', 2, 112, '#6a3a22', '#2f4a3a'),
    ('fa_ware_c', 18.0, 15.0, '#b45a34', 'ware', 3, 113, '#3f6a48', '#2a3a5a'),
]

def side_wall(name, base, seed):
    """Plain side/back wall tile 6 x 6 D: brick pattern, one window, a painted ghost sign stain."""
    r = random.Random(seed); defs = _brick_defs('s' + name, base, mix(base, '#d8c8b0', 0.55)); o = [rect(-0.1, -0.1, 6.2, 6.2, f'url(#s{name})')]
    for _ in range(4): o.append(ell(r.uniform(0, 6), r.uniform(0, 6), r.uniform(0.6, 1.4), r.uniform(0.4, 1.0), mul(base, r.choice((0.86, 1.1))), op=0.35))
    o.append(rect(2.4, 1.6, 1.0, 1.7, '#d6c8ae')); o.append(rect(2.48, 1.68, 0.84, 1.54, '#2c3058'))
    job(name, 0, 0, 6, 6, 40, ''.join(o), defs=defs)

def stable():
    """Horse stable front 9 x 6.5 D (gable included above the eave at 4.2): red board-and-batten, white trim, big double door with
    a cross brace, hay-loft door, two small windows, a horseshoe."""
    W, H = 9.0, 6.5; e = 2.3; o = [rect(-0.1, -0.1, W + 0.2, H + 0.2, '#a63c2c')]
    for k in range(int(W / 0.35) + 1): o.append(line(k * 0.35, 0, k * 0.35, H, '#7a2a20', 0.05))
    o.append(poly([(-0.1, e), (W / 2, -0.1), (W + 0.1, e)], 'none', stroke='#f0e6d0', sw=0.18))
    dx, dw = 2.8, 3.4
    o.append(rect(dx - 0.15, H - 3.6, dw + 0.3, 3.7, '#f0e6d0')); o.append(rect(dx, H - 3.45, dw, 3.45, '#8a2e22'))
    for (a, b) in ((dx, dx + dw / 2), (dx + dw / 2, dx + dw)):
        o.append(rect(a + 0.05, H - 3.4, b - a - 0.1, 3.35, 'none', stroke='#f0e6d0', sw=0.12)); o.append(line(a + 0.1, H - 3.35, b - 0.1, H - 0.1, '#f0e6d0', 0.12)); o.append(line(b - 0.1, H - 3.35, a + 0.1, H - 0.1, '#f0e6d0', 0.12))
    o.append(rect(W / 2 - 0.7, 0.9, 1.4, 1.3, '#5a1e18', stroke='#f0e6d0', sw=0.12))
    for x in (1.0, W - 2.0): o.append(rect(x, H - 3.0, 1.0, 0.9, '#2c3058', stroke='#f0e6d0', sw=0.1))
    o.append(path(f'M{W / 2 - 0.25},{H - 4.0} a0.25,0.3 0 1 1 0.5,0', 'none', stroke='#c8c0b8', sw=0.08))
    job('stable', 0, 0, W, H, 64, ''.join(o))

# ----------------------------------------------------------------------------- ground, roofs, ship, water
def setts():
    """Granite setts of Commercial Street 2 x 2 D (warm grey-brown, brick-bond rows, dark joints, a trace of slush)."""
    r = random.Random(17); W = H = 2.0; o = [rect(-0.1, -0.1, 2.2, 2.2, '#5a4440')]; rows = 8; rh = H / rows
    for j in range(rows):
        y = j * rh; x = (j % 2) * 0.17
        while x < W + 0.3:
            w = r.uniform(0.28, 0.4); c = r.choice(('#a08878', '#94807a', '#b0907a', '#8c7870', '#a89080', '#9a7c6a', '#b49a84'))
            for xx in _wrap(x, W, w):
                o.append(rect(xx + 0.015, y + 0.015, w - 0.03, rh - 0.03, c, rx=0.04)); o.append(rect(xx + 0.04, y + 0.03, w - 0.1, 0.04, mul(c, 1.14), rx=0.02))
            x += w
    for _ in range(3):
        x, y = r.uniform(0.2, 1.6), r.uniform(0.2, 1.6); o.append(ell(x, y, 0.35, 0.2, '#3a2c34', op=0.18))
    job('setts', 0, 0, W, H, 200, ''.join(o))

def pavers():
    """Brick sidewalk 2 x 2 D, herringbone-ish running bond of red pavers, granite kerb not included."""
    r = random.Random(19); o = [rect(-0.1, -0.1, 2.2, 2.2, '#8a5a48')]
    for j in range(10):
        y = j * 0.2
        for i in range(-1, 6):
            x = i * 0.4 + (j % 2) * 0.2; c = r.choice(('#b8583a', '#a84e36', '#c4663e', '#b05a40'))
            for xx in _wrap(x, 2, 0.4): o.append(rect(xx + 0.012, y + 0.012, 0.376, 0.176, c, rx=0.015))
    job('pavers', 0, 0, 2, 2, 160, ''.join(o))

def yard():
    """Packed earth of the tank yard 4 x 4 D: ochre-brown dirt, gravel, wheel ruts, molasses spots."""
    r = random.Random(23); o = [rect(-0.1, -0.1, 4.2, 4.2, '#a98060')]
    for _ in range(18):
        x, y = r.uniform(0, 4), r.uniform(0, 4)
        for xx in _wrap(x - 0.5, 4, 1.0): o.append(ell(xx + 0.5, y, r.uniform(0.3, 0.8), r.uniform(0.2, 0.6), r.choice(('#b88e68', '#9a7254', '#b08a5e', '#8e6a52')), op=0.7))
    for _ in range(140):
        o.append(circ(r.uniform(0, 4), r.uniform(0, 4), r.uniform(0.015, 0.045), r.choice(('#7a6058', '#c8b49a', '#6a5048', '#d2c0a4'))))
    for _ in range(4):
        x, y = r.uniform(0.3, 3.7), r.uniform(0.3, 3.7); o.append(ell(x, y, r.uniform(0.08, 0.2), r.uniform(0.06, 0.14), MOL, op=0.6))
    job('yard', 0, 0, 4, 4, 96, ''.join(o))

def tarroof():
    r = random.Random(29); o = [rect(-0.1, -0.1, 4.2, 4.2, '#5a4a52')]
    for _ in range(12):
        x, y = r.uniform(0, 4), r.uniform(0, 4)
        for xx in _wrap(x - 0.6, 4, 1.2): o.append(ell(xx + 0.6, y, r.uniform(0.3, 0.9), r.uniform(0.2, 0.5), r.choice(('#4a3c46', '#665660', '#544650')), op=0.7))
    for k in range(5): o.append(line(-0.1, k * 0.8 + 0.4, 4.1, k * 0.8 + 0.4, '#3e3240', 0.03))
    job('tarroof', 0, 0, 4, 4, 48, ''.join(o))

def slate():
    r = random.Random(31); o = [rect(-0.1, -0.1, 2.2, 2.2, '#4a4458')]
    for j in range(8):
        y = j * 0.25
        for i in range(-1, 9):
            x = i * 0.25 + (j % 2) * 0.125; c = r.choice(('#5a5470', '#4e4864', '#605a74', '#545068'))
            for xx in _wrap(x, 2, 0.25): o.append(rect(xx + 0.01, y + 0.01, 0.23, 0.23, c, rx=0.02))
    job('slate', 0, 0, 2, 2, 120, ''.join(o))

def water():
    """Harbour water 24 x 24 D tile, painted: deep blue with pale swell streaks and darker ripples."""
    r = random.Random(37); W = 24.0; o = [rect(-0.2, -0.2, W + 0.4, W + 0.4, '#2f58b4')]
    for _ in range(60):
        x, y = r.uniform(0, W), r.uniform(0, W); w = r.uniform(1.5, 5.0)
        for xx in _wrap(x, W, w): o.append(ell(xx + w / 2, y, w / 2, r.uniform(0.05, 0.14), r.choice(('#6c9ae0', '#4a78cc', '#9cc0f0')), op=r.uniform(0.4, 0.8)))
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, W); w = r.uniform(1.0, 3.0)
        for xx in _wrap(x, W, w): o.append(ell(xx + w / 2, y, w / 2, 0.08, '#1e3c8c', op=0.5))
    job('water', 0, 0, W, W, 24, ''.join(o))

def hull_tex():
    """Freighter hull side 70 x 9 D (y = 0 at the deck edge, the waterline at y = 7.8): black topsides with plate lines and rivets,
    white sheer line, portholes, red boot topping, rust streaks from the hawse and scuppers."""
    r = random.Random(41); W, H = 70.0, 9.0; o = [rect(-0.2, -0.2, W + 0.4, H + 0.4, '#2a2630')]
    for k in range(1, 4): o.append(line(0, k * 1.9, W, k * 1.9, '#1c1a22', 0.05))
    for i in range(int(W / 2.6)): o.append(line(i * 2.6, 0.3, i * 2.6, 7.6, '#1c1a22', 0.04))
    o.append(rect(-0.2, 0.15, W + 0.4, 0.16, '#efe6d6'))
    for i in range(30):
        x = 4 + i * 2.1; o.append(circ(x, 1.4, 0.18, '#d8c8a0', stroke='#bfb090', sw=0.05)); o.append(circ(x, 1.4, 0.12, '#2c3058'))
    o.append(rect(-0.2, 6.9, W + 0.4, 2.3, '#a8342a'))
    for _ in range(18):
        x = r.uniform(1, W - 1); o.append(rect(x, r.uniform(0.4, 2.5), r.uniform(0.08, 0.2), r.uniform(1.0, 4.5), '#7a3c26', op=0.45, rx=0.05))
    job('hull', 0, 0, W, H, 20, ''.join(o))

def ship_house():
    """Freighter deckhouse wall 6 x 3 D: cream steel with portholes / windows, rivet lines."""
    o = [rect(-0.1, -0.1, 6.2, 3.2, '#ead9b8')]
    for k in range(4): o.append(rect(0.5 + k * 1.4, 0.9, 0.7, 0.9, '#2c3058', stroke='#a89878', sw=0.06))
    o.append(rect(-0.1, 2.6, 6.2, 0.5, '#c8b08a')); o.append(line(-0.1, 0.25, 6.1, 0.25, '#b8a080', 0.05))
    job('ship_house', 0, 0, 6, 3, 40, ''.join(o))

# ----------------------------------------------------------------------------- sky and painted plate
TT.SKY['winter'] = dict(stops=[(0, '#2f58aa'), (0.45, '#4c7cc8'), (0.78, '#86b0e6'), (0.88, '#b8cdea'), (1, '#d6dcec')], cloud='#f6f6fc', cloud_b='#b8b4e0', n=9, dark=False)
TT.SKY['warm'] = dict(stops=[(0, '#4670ba'), (0.45, '#6a92d0'), (0.76, '#a2bce2'), (0.87, '#dcd0d0'), (1, '#f0dcc4')], cloud='#fff6ee', cloud_b='#c6b2d6', n=17, dark=False)

PANO = dict(
    winter=dict(far='#8e98d4', far2='#a8b2e2', shore='#7a84c4', water='#5a88d6', bldg=['#c07a5c', '#b0684e', '#d09068', '#c88c6a', '#a86a58'], shade='#7a6aa6',
                roof='#6a5a82', steeple='#ece6dc', haze='#c6d0ec', hz=0.35),
    warm=dict(far='#a6a0d4', far2='#c2b8de', shore='#9690c6', water='#6a92d6', bldg=['#cc8a68', '#bc7a5e', '#d8a078', '#d29a76', '#b87c66'], shade='#8a78ac',
              roof='#7a6a8e', steeple='#f0e8dc', haze='#e2d6dc', hz=0.5))
PANO_R = 150.0; PANO_Z0, PANO_Z1 = -1.5, 45.0

def panorama(mode):
    """The painted ring at R 150 (z -1.5 .. 45), u = azimuth / 360 counter-clockwise from +x, NOT repeated. Harbour side (azimuth
    -45..115 deg: north-east, the far shore of Charlestown / East Boston with low hills, wharves, cranes, ships' masts, the Bunker Hill
    obelisk) and city side (115..315 deg: dense brick roofs, chimneys, the white Old North steeple, the Custom House tower, gas holder).
    SVG units: x = azimuth in D of arc, y = 45 - z. Transparent above the skyline."""
    p = PANO[mode]; r = random.Random(53); W = 2 * math.pi * PANO_R; H = PANO_Z1 - PANO_Z0; o = []
    def X(az): return (az % 360.0) / 360.0 * W
    def Y(z): return PANO_Z1 - z
    hz = lambda c, k=1.0: mix(c, p['haze'], p['hz'] * k)
    o.append(rect(-1, Y(0.6), W + 2, H, hz(p['water'], 0.3)))             # water / ground band at the foot of the plate
    # harbour side: far hills, shoreline buildings, cranes, masts, obelisk
    for seg_ in ((X(315), W), (0.0, X(115))):
        a, b = seg_
        if b <= a: continue
        pts = []; n = int((b - a) / 14) + 2
        for i in range(n + 1):
            x = a + (b - a) * i / n; pts.append((x, Y(4.5 + 3.5 * abs(math.sin(x * 0.011 + 1.3)) + r.uniform(0, 1.2))))
        o.append(poly(pts + [(b, Y(0.5)), (a, Y(0.5))], hz(p['far2'], 1.2)))
        pts = []
        for i in range(n + 1):
            x = a + (b - a) * i / n; pts.append((x, Y(2.2 + 1.8 * abs(math.sin(x * 0.017 + 0.4)) + r.uniform(0, 0.8))))
        o.append(poly(pts + [(b, Y(0.5)), (a, Y(0.5))], hz(p['far'])))
        x = a
        while x < b:
            w = r.uniform(2.0, 6.0); h = r.uniform(1.0, 3.2); c = hz(r.choice(p['bldg']), 0.9)
            o.append(rect(x, Y(0.5 + h), w, h, c)); o.append(rect(x + w * 0.7, Y(0.5 + h), w * 0.3, h, hz(p['shade']), op=0.7))
            if r.random() < 0.5: o.append(poly([(x, Y(0.5 + h)), (x + w / 2, Y(1.2 + h)), (x + w, Y(0.5 + h))], hz(p['roof'])))
            x += w + r.uniform(0, 3.0)
        for i in range(int((b - a) / 40)):
            cx = r.uniform(a, b); kind = r.random(); col = hz('#4a4a6a', 0.9)
            if kind < 0.4:                                                # crane
                o.append(rect(cx, Y(9), 0.35, 8.5, col)); o.append(line(cx, Y(9), cx + 5, Y(7.5), col, 0.25)); o.append(line(cx + 5, Y(7.5), cx + 5, Y(4), col, 0.08))
            else:                                                         # masts of a ship at the far wharf
                o.append(rect(cx - 6, Y(1.6), 12, 1.2, hz('#2a2630', 0.8))); o.append(rect(cx - 1, Y(3.2), 3, 1.6, hz('#ead9b8', 0.8)))
                for dx in (-4, 4): o.append(rect(cx + dx, Y(9), 0.2, 7.4, col))
    ob = X(100); o.append(poly([(ob - 0.9, Y(2.5)), (ob + 0.9, Y(2.5)), (ob + 0.45, Y(15.5)), (ob, Y(16.5)), (ob - 0.45, Y(15.5))], hz('#d8d0e0', 0.6)))   # obelisk
    # city side: four rows of roofs, steeples, the Custom House tower, a gas holder
    a, b = X(115), X(315)
    for row in range(4):
        base_z = 0.5 + row * 0.2; x = a - 2; k_h = 1.0 - 0.15 * row
        while x < b + 2:
            w = r.uniform(3.0, 8.0); h = (r.uniform(4.0, 11.0) - row * 1.2) * k_h; c = hz(r.choice(p['bldg']), 1.0 - row * 0.2)
            o.append(rect(x, Y(base_z + h), w, h, c)); o.append(rect(x + w * 0.72, Y(base_z + h), w * 0.28, h, hz(p['shade'], 1 - row * 0.2), op=0.75))
            for wy in range(int(h / 2.2)):
                for wx in range(int(w / 1.5)):
                    o.append(rect(x + 0.5 + wx * 1.5, Y(base_z + h - 1.0 - wy * 2.2), 0.6, 0.9, hz('#3a3a64', 1 - row * 0.2)))
            if r.random() < 0.5:
                for cxk in range(r.randint(1, 3)): o.append(rect(x + r.uniform(0.3, w - 0.8), Y(base_z + h + 1.2), 0.5, 1.2, hz('#7a4438', 1 - row * 0.2)))
            x += w + r.uniform(-0.5, 0.8)
    for az in (148.0, 205.0):                                             # white wooden steeples
        cx = X(az); o.append(rect(cx - 1.2, Y(13), 2.4, 13, hz(p['steeple'], 0.5))); o.append(rect(cx - 0.8, Y(17), 1.6, 4, hz(p['steeple'], 0.5)))
        o.append(poly([(cx - 0.9, Y(17)), (cx, Y(25)), (cx + 0.9, Y(17))], hz(p['steeple'], 0.5))); o.append(rect(cx - 0.4, Y(15.5), 0.8, 1.2, hz('#3a3a64', 0.6)))
    cx = X(250); col = hz('#d8cab4', 0.6)                                 # Custom House tower (1915)
    o.append(rect(cx - 3, Y(30), 6, 30, col)); o.append(rect(cx + 1.2, Y(30), 1.8, 30, hz(p['shade'], 0.6), op=0.7))
    for k in range(8): o.append(rect(cx - 2.4, Y(28 - k * 3.2), 0.6, 2.2, hz('#3a3a64', 0.6))); o.append(rect(cx - 0.3, Y(28 - k * 3.2), 0.6, 2.2, hz('#3a3a64', 0.6)))
    o.append(rect(cx - 3.4, Y(33), 6.8, 3, col)); o.append(circ(cx, Y(31.5), 1.1, hz('#f2ecdc', 0.4), stroke=hz('#3a3a64', 0.6), sw=0.15))
    o.append(poly([(cx - 3.4, Y(33)), (cx, Y(39)), (cx + 3.4, Y(33))], hz('#6a8a7a', 0.6)))
    gx = X(285); o.append(rect(gx - 6, Y(8), 12, 7.5, hz('#7a6a7a', 0.7))); o.append(ell(gx, Y(8), 6, 0.8, hz('#8a7a8a', 0.7)))
    for k in range(5): o.append(line(gx - 6 + k * 3, Y(8), gx - 6 + k * 3, Y(0.5), hz('#5a4a5a', 0.7), 0.25))
    job('pano_' + mode, 0, 0, W, H, 5.0, ''.join(o), transparent=True)

# ----------------------------------------------------------------------------- registry
def all_jobs():
    TT.JOBS.clear(); TT.SIZE.clear()
    tank_textures(); girder(); column(); stable(); setts(); pavers(); yard(); tarroof(); slate(); water(); hull_tex(); ship_house()
    for f in FACADES: facade(f[0], f[1], f[2], f[3], f[4], f[5], f[6], door=f[7], sign=f[8])
    side_wall('side_red', '#a8482e', 121); side_wall('side_ochre', '#c88c44', 122)
    for m in ('winter', 'warm'): TT.sky(m); panorama(m)

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
