#!/usr/bin/env python3
"""textures.py : flat per-surface artwork for the 3D office, drawn with the v2 set's SVG code and palette
(v2/sets/office.py is imported, never copied) and rasterised by headless Chromium.

    import textures as T
    paths = T.ensure()            # {name: png path}; cached in v3/set3d/tex/ by content hash
    T.SIZE[name] -> (w_D, h_D)    # size of one image (or one tile) in D

Every texture is drawn in the colours the surface shows in neutral light; the lit material turns that
into the shade and sun looks (see office3d.py)."""
import os, sys, json, math, random, hashlib, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(PROJ, 'v2', 'sets'))
import office as O                                          # noqa: E402  (v2 drawing code + palette)
# colour pass (v3/out/COLOUR.md): the v2 palette leaned rose / purple / steel-violet; the reference interiors are crimson-terracotta,
# orange-brown wood and saturated navy. The v2 module is only read: these names are re-bound in memory for the 3D set's artwork.
COLOUR = dict(FRIEZE='#6a2a1e', FLOOR='#a6764e', SEAM='#2e1d22', STEEL='#34508c', STEEL_HI='#42609e', NAVY='#283a74',
              WOOD='#5e3018', PANEL='#7c4620')
for _k, _v in COLOUR.items(): setattr(O, _k, _v)
TEX = os.path.join(HERE, 'tex'); TMP = os.path.join(PROJ, 'v3', 'tmp', 'set3d')
rect, line, poly, pline, circ, ell, text, mul, mix, det = O.rect, O.line, O.poly, O.pline, O.circ, O.ell, O.text, O.mul, O.mix, O.det
INK, W_OBJ, W_DET = O.INK, O.W_OBJ, O.W_DET
JOBS = {}          # name -> dict(svg=str, w=px, h=px, transparent=bool)
SIZE = {}          # name -> (w_D, h_D)

def doc(x0, y0, w, h, ppd, body, defs='', bg=None):
    """SVG document showing the D-rectangle (x0, y0, w, h) (v2 convention: y down) at ppd pixels per D."""
    W, H = int(round(w * ppd)), int(round(h * ppd)); K = O.K
    b = f'<rect x="{x0 * K:g}" y="{y0 * K:g}" width="{w * K:g}" height="{h * K:g}" fill="{bg}"/>' if bg else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="{x0 * K:g} {y0 * K:g} {w * K:g} {h * K:g}" '
            f'preserveAspectRatio="none" style="display:block"><defs>{defs}</defs>{b}{body}</svg>'), W, H

def job(name, x0, y0, w, h, ppd, body, defs='', bg=None, transparent=False):
    svg, W, H = doc(x0, y0, w, h, ppd, body, defs, bg)
    JOBS[name] = dict(svg=svg, w=W, h=H, transparent=transparent); SIZE[name] = (w, h)

# ----------------------------------------------------------------------------- surfaces
WALL3 = '#aa3e2c'       # colour pass: crimson-terracotta (was #9c4a50 rose)
WALL3_OLD = '#9c4a50'       # review: the v2 paper #9c3139 clipped to pure red (green = 0) in the sun patch after the grade and read 59 of 255 in shade
                        # behind the heads; this is close to the spec's wallpaper colour #9c5257
def wallpaper():
    """One tile of the v2 rose paper with the stencilled sprig (0.32 x 0.76 D), seamless."""
    W_, H_ = 0.32, 0.76; WALL, HI = WALL3, O.WALL_HI; t = [rect(-0.1, -0.1, W_ + 0.2, H_ + 0.2, WALL, stroke=None, sw=0)]
    for x in (0.0, 0.28, 0.32): t.append(rect(x, -0.1, 0.04, H_ + 0.2, mul(WALL, 0.82), stroke=None, sw=0))
    t.append(rect(0.12, -0.1, 0.08, H_ + 0.2, mul(WALL, 0.82), stroke=None, sw=0))
    for x in (0.12, 0.28): t.append(line(x, -0.1, x, H_ + 0.1, det(WALL, 0.72), 0.007))
    for x in (0.0, 0.16, 0.32): t.append(line(x, -0.1, x, H_ + 0.1, mul(WALL, 1.12), 0.005))
    for cx, cy in ((0.08, 0.19), (0.24, 0.57)):
        t.append(poly([(cx, cy - 0.07), (cx + 0.031, cy), (cx, cy + 0.07), (cx - 0.031, cy)], HI, stroke=det(WALL, 0.5), sw=0.009))
        t.append(poly([(cx, cy - 0.034), (cx + 0.013, cy), (cx, cy + 0.034), (cx - 0.013, cy)], mul(WALL, 1.1), stroke=None, sw=0))
        for dx in (-0.043, 0.043): t.append(circ(cx + dx, cy + 0.026, 0.0145, HI, stroke=det(WALL, 0.5), sw=0.008))
        t.append(line(cx - 0.036, cy + 0.092, cx + 0.036, cy + 0.092, mix(WALL, HI, 0.8), 0.011)); t.append(circ(cx, cy - 0.1, 0.0105, mix(WALL, HI, 0.8), stroke=None, sw=0))
    job('wallpaper', 0, 0, W_, H_, 1000, ''.join(t))

def frieze():
    F = O.FRIEZE
    # review: bolder (the 1 px lines and the x 1.25 lozenges vanished at 5 D)
    f = [rect(-0.1, -0.1, 0.6, 0.7, F, stroke=None, sw=0), line(-0.1, 0.07, 0.5, 0.07, det(F, 0.5), 0.02), line(-0.1, 0.43, 0.5, 0.43, det(F, 0.5), 0.02),
         poly([(0.2, 0.14), (0.28, 0.25), (0.2, 0.36), (0.12, 0.25)], mul(F, 1.6), stroke=det(F, 0.45), sw=0.014)]
    for x in (0.0, 0.4): f.append(circ(x, 0.25, 0.034, mul(F, 1.6), stroke=det(F, 0.45), sw=0.012))
    f += [line(0.05, 0.25, 0.1, 0.25, det(F, 0.5), 0.014), line(0.3, 0.25, 0.35, 0.25, det(F, 0.5), 0.014)]
    job('frieze', 0, 0, 0.4, 0.5, 800, ''.join(f))

def wainscot(pw=0.76, ph=1.02):
    """One raised-panel bay of the walnut wainscot (drawn panel; the rails are real geometry)."""
    W, P = O.WOOD, O.PANEL; o = [rect(-0.1, -0.1, pw + 0.2, ph + 0.2, W, stroke=None, sw=0)]
    x, y, w_, h_ = 0.07, 0.07, pw - 0.14, ph - 0.14
    o.append(rect(x, y, w_, h_, P, stroke=mul(W, 0.5), sw=W_DET * 1.3))
    o.append(rect(x + 0.05, y + 0.05, w_ - 0.1, h_ - 0.1, mul(P, 1.1), stroke=mul(W, 0.55), sw=W_DET))
    o.append(pline([(x + 0.012, y + h_ - 0.012), (x + 0.012, y + 0.012), (x + w_ - 0.012, y + 0.012)], mul(P, 1.75), W_DET))
    o.append(pline([(x + 0.062, y + h_ - 0.062), (x + w_ - 0.062, y + h_ - 0.062), (x + w_ - 0.062, y + 0.062)], mul(P, 1.6), W_DET * 0.8))
    r = random.Random(4)
    for i in range(15):                                     # grain inside the panel (review: 7 faint 1 px lines did not read in a medium shot)
        gx = x + 0.1 + r.uniform(0, w_ - 0.2); gy = y + 0.1 + r.uniform(0, h_ - 0.45); o.append(line(gx, gy, gx + r.uniform(-0.01, 0.01), gy + r.uniform(0.12, 0.3), mul(P, r.choice((0.72, 0.78, 1.32))), 0.011))
    for sx in (0.0, pw): o.append(line(sx, -0.1, sx, ph + 0.1, mul(W, 0.55), W_DET * 1.2))          # stile joint
    job('wainscot', 0, 0, pw, ph, 700, ''.join(o))

def planks(n=14, L=6.0, pw=0.28, ppd=400):
    """Seamless plank tile: n planks of 0.28 D running along the image's vertical axis (toward the map wall)."""
    r = random.Random(8); F, SEAM = O.FLOOR, O.SEAM; o = []
    for i in range(n):
        c = mul(F, r.uniform(0.82, 1.1)); a = i * pw
        o.append(rect(a, -0.1, pw, L + 0.2, c, stroke=None, sw=0))
        for _ in range(7):
            gx = a + r.uniform(0.05, 0.23); z = r.uniform(0.1, L - 1.2); l = r.uniform(0.3, 1.0)
            o.append(line(gx, z, gx + r.uniform(-0.02, 0.02), z + l, mul(c, r.choice((0.84, 0.88, 1.1))), W_DET))
        for _ in range(r.choice((1, 2, 2))):
            z = r.uniform(0.2, L - 0.2); o.append(line(a, z, a + pw, z, mul(SEAM, 0.7), 0.018))
            for dz in (-0.06, 0.06):
                for dx in (0.07, 0.21): o.append(circ(a + dx, z + dz, 0.011, mul(SEAM, 0.9), stroke=None, sw=0))
        if r.random() < 0.6:
            z = r.uniform(0.3, L - 0.3); o.append(ell(a + r.uniform(0.08, 0.2), z, 0.018, 0.035, mul(c, 0.72), stroke=mul(c, 0.55), sw=W_DET * 0.8))
    for i in range(n + 1): o.append(rect(i * pw - 0.013, -0.1, 0.026, L + 0.2, mul(SEAM, 0.62), stroke=None, sw=0))      # review: darker seams, they must survive the shade
    job('planks', 0, 0, n * pw, L, ppd, ''.join(o))

def _rug_body(RX, y0, y1, end=False):
    NAVY, RED, GOLD = O.NAVY, O.RUGRED, O.GOLD; o = []
    def q(xa, xb, ya, yb, fill, stroke=None, sw=0): return rect(xa, ya, xb - xa, yb - ya, fill, stroke=stroke, sw=sw)
    def dia(X, Y, a, b, fill, stroke, sw=W_DET): return poly([(X, Y - b), (X + a, Y), (X, Y + b), (X - a, Y)], fill, stroke=stroke, sw=sw)
    ya = y0 if end else y0 - 0.5
    o.append(q(-RX, RX, ya, y1 + 0.5, RED, stroke=INK, sw=W_OBJ)); o.append(q(-RX + 0.07, RX - 0.07, ya + 0.07, y1 + 0.5, 'none', stroke=GOLD, sw=W_DET * 1.3))
    o.append(q(-RX + 0.3, RX - 0.3, ya + 0.3, y1 + 0.5, GOLD)); o.append(q(-RX + 0.34, RX - 0.34, ya + 0.34, y1 + 0.5, NAVY, stroke=mul(NAVY, 0.55), sw=W_DET))
    o.append(q(-RX + 0.44, RX - 0.44, ya + 0.44, y1 + 0.5, 'none', stroke=mix(NAVY, GOLD, 0.55), sw=W_DET))
    return o, q, dia

def rug_tile(RX=1.2, L=2.0, ppd=400):
    """Seamless 2.0 D repeat of the navy runner (width 2.4 D, length along the image's vertical axis)."""
    NAVY, RED, GOLD = O.NAVY, O.RUGRED, O.GOLD; o, q, dia = _rug_body(RX, 0.0, L)
    for sx in (-1, 1):
        for k in range(-1, 6):
            z = k * 0.4 + 0.1; o.append(dia(sx * (RX - 0.185), z, 0.075, 0.12, NAVY, GOLD)); o.append(dia(sx * (RX - 0.185), z + 0.2, 0.026, 0.04, GOLD, None))
    zi = 0
    for k_ in range(-1, 9):
        z = k_ * 0.25 + 0.125
        for k in range(-3, 4):
            X = k * 0.3 + (0.15 if zi % 2 else 0)
            if abs(X) < RX - 0.5: o.append(ell(X, z, 0.022, 0.014, '#d9c9a8' if (k + zi) % 3 else GOLD, stroke=None, sw=0))
        zi += 1
    s = 0.62; Zc = L / 2
    o.append(dia(0, Zc, 0.95 * s, 0.72 * s, RED, GOLD, W_DET * 1.5)); o.append(dia(0, Zc, 0.7 * s, 0.53 * s, NAVY, mix(NAVY, GOLD, 0.6)))
    o.append(dia(0, Zc, 0.32 * s, 0.24 * s, GOLD, mul(GOLD, 0.6))); o.append(dia(0, Zc, 0.13 * s, 0.1 * s, RED, None))
    job('rug', -RX, 0, 2 * RX, L, ppd, ''.join(o))

def rug_end(RX=1.2, L=0.9, ppd=400):
    """The end of the runner next to the map wall: cross border, corner lozenges, fringe (image top = wall side)."""
    NAVY, RED, GOLD = O.NAVY, O.RUGRED, O.GOLD; r = random.Random(8); o = []
    for k in range(49):
        x = -RX + 0.02 + k * (2 * RX - 0.04) / 48; o.append(line(x, 0.1, x + r.uniform(-0.01, 0.01), 0.015, '#d9c9a8', W_DET * 1.2))
    b, q, dia = _rug_body(RX, 0.1, L, end=True); o += b
    x = -RX + 0.4
    while x < RX - 0.3:
        o.append(dia(x, 0.1 + 0.185, 0.12, 0.075, NAVY, GOLD)); o.append(dia(x + 0.2, 0.1 + 0.185, 0.04, 0.026, GOLD, None)); x += 0.4
    for sx in (-1, 1):
        z = 0.1 + 0.5
        while z < L + 0.2: o.append(dia(sx * (RX - 0.185), z, 0.075, 0.12, NAVY, GOLD)); z += 0.4
    job('rug_end', -RX, 0, 2 * RX, L, ppd, ''.join(o), transparent=True)

def ceiling(n=10, L=3.0, bw=0.37):
    """Seamless ceiling boards running toward the map wall, dark seams wide enough to read from the floor."""
    r = random.Random(3); C = '#8c5030'; o = []               # colour pass: orange-brown boards (was #7d4350 plum)
                  # review: lighter boards than v2's #64323c, darker seams: nothing on the old ceiling survived as an edge
    for i in range(n):
        o.append(rect(i * bw, -0.1, bw, L + 0.2, mul(C, 0.78 + (r.uniform(0.84, 1.14) - 0.84) * 1.5), stroke=None, sw=0))
        for _ in range(4):
            gx = i * bw + r.uniform(0.06, bw - 0.06); z = r.uniform(0, L - 1.0); o.append(line(gx, z, gx, z + r.uniform(0.3, 0.9), mul(C, r.choice((0.62, 1.4))), 0.014))
        z = r.uniform(0.3, L - 0.3); o.append(line(i * bw, z, (i + 1) * bw, z, mul(C, 0.24), 0.026))
    for i in range(n + 1):
        o.append(rect(i * bw - 0.026, -0.1, 0.052, L + 0.2, mul(C, 0.2), stroke=None, sw=0)); o.append(rect(i * bw + 0.026, -0.1, 0.018, L + 0.2, mul(C, 1.6), stroke=None, sw=0))
    job('ceiling', 0, 0, n * bw, L, 300, ''.join(o))

def beam(L=7.6, h=0.37):
    """Side face of one ceiling cross beam (whole length): light arris at the lower edge, grain checks, two iron straps with bolts."""
    r = random.Random(11); B = '#4a2616'; o = [rect(-0.1, -0.1, L + 0.2, h + 0.2, B, stroke=None, sw=0)]
    o.append(rect(-0.1, h - 0.045, L + 0.2, 0.06, mul(B, 1.7), stroke=None, sw=0)); o.append(line(-0.1, h - 0.055, L + 0.1, h - 0.055, mul(B, 0.4), 0.014))
    o.append(rect(-0.1, -0.1, L + 0.2, 0.16, mul(B, 0.6), stroke=None, sw=0))
    for _ in range(26):
        x = r.uniform(0, L - 0.9); y = r.uniform(0.09, h - 0.09); o.append(line(x, y, x + r.uniform(0.3, 1.1), y + r.uniform(-0.012, 0.012), mul(B, r.choice((0.5, 0.55, 1.5))), 0.014))
    for sx in (1.9, 5.7):
        o.append(rect(sx - 0.09, -0.1, 0.18, h + 0.2, '#22222e', stroke='#14111a', sw=W_DET * 1.3))
        for by in (0.11, 0.27): o.append(circ(sx, by, 0.03, '#6f7488', stroke='#14111a', sw=W_DET))
    job('beam', 0, 0, L, h, 300, ''.join(o))

def wall_map(ppd=1000):
    """The printed map sheet without the red track (paper area only: the frame is real geometry)."""
    u = 'm3'; x0, y0, x1, y1 = O.MAP_IN
    body = O.draw_map(u, dict(line=0.0, erase=0.0, t=0.0), hi=True)
    job('map', x0, y0, x1 - x0, y1 - y0, ppd, body, defs=O.map_defs(u) + O.room_defs(u), bg=O.PAPER)

def wall_props():
    u = 'p3'; d = O.room_defs(u)
    job('sign', -1.52, -4.36, 3.04, 0.48, 600, _sign(), defs=d, transparent=True)
    job('clock', -0.5, -0.5, 1.0, 1.0, 700, O.clock_svg(0, 0, 0.42, 0.0), defs=d, transparent=True)
    job('calendar', 0, 0, 0.66, 0.9, 700, O.calendar_svg(0.02, 0.02, 0.62, 0.86), defs=d, transparent=True)
    job('pinboard', 0, 0, 1.0, 1.3, 600, O.pinboard_svg(0.02, 0.02, 0.96, 1.26), defs=d, transparent=True)
    job('barometer', -0.4, -0.05, 0.8, 1.6, 600, O.barometer_svg(0, 0), defs=d, transparent=True)
    job('certificate', 0, 0, 0.5, 0.64, 600, O.certificate_svg(0.015, 0.015, 0.47, 0.61), defs=d, transparent=True)

def _sign():
    x, y, w, h = -1.5, -4.34, 3.0, 0.44; G = O.GOLD; o = []
    o.append(rect(x, y, w, h, '#3d1c12', sw=W_OBJ * 1.25)); o.append(rect(x + 0.035, y + 0.035, w - 0.07, h - 0.07, '#1c403d', stroke=G, sw=W_DET * 1.6))
    o.append(rect(x + 0.07, y + 0.07, w - 0.14, h - 0.14, 'none', stroke=mul('#1c403d', 1.9), sw=W_DET * 0.8))
    o.append(text(0, y + 0.292, 'U.S. WEATHER BUREAU', 0.19, '#e9d9b0', extra=O.fit(2.42)))
    for sx in (x + 0.17, x + w - 0.17): o.append(poly([(sx, y + 0.16), (sx + 0.045, y + 0.22), (sx, y + 0.28), (sx - 0.045, y + 0.22)], G, sw=W_DET))
    return ''.join(o)

def sky(ppd=60):
    """What the window looks out on: grey-blue sky gradient with soft clouds and a low roofline."""
    g = ('<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5f79b4"/><stop offset="0.55" stop-color="#93a9cf"/>'
         '<stop offset="1" stop-color="#cfd6e2"/></linearGradient>')
    r = random.Random(5); K = O.K; o = [f'<rect x="0" y="0" width="{16 * K}" height="{9 * K}" fill="url(#sk)"/>']
    for i in range(9):
        cx, cy = r.uniform(0, 16), r.uniform(1.0, 5.5)
        for j in range(4): o.append(ell(cx + j * 0.5 + r.uniform(-0.2, 0.2), cy + r.uniform(-0.12, 0.12), r.uniform(0.5, 0.9), r.uniform(0.2, 0.34), '#eef1f6', stroke=None, sw=0, extra='opacity="0.55"'))
    x = 0.0
    while x < 16:                                            # roofline silhouettes
        w = r.uniform(0.7, 1.8); h = r.uniform(0.8, 2.6); c = mix('#6d7fa8', '#8fa0c4', r.random())
        o.append(rect(x, 9 - h, w, h + 0.1, c, stroke=None, sw=0))
        for k in range(int(w / 0.3)):
            for m in range(int(h / 0.4)): o.append(rect(x + 0.08 + k * 0.3, 9 - h + 0.12 + m * 0.4, 0.12, 0.2, mul(c, 0.82), stroke=None, sw=0))
        x += w + r.uniform(0.0, 0.3)
    job('sky', 0, 0, 16, 9, ppd, ''.join(o), defs=g)


def furniture():
    u = 'f3'; d = O.room_defs(u); S1, S2, BR = O.STEEL, O.STEEL_HI, O.BRASS
    # filing cabinet front (one cabinet, 4 drawers): v2 drawing, cropped to the carcass
    yt = -3.0; yb = O.MID_BASE
    job('cab_front', 0, yt, 0.75, yb - yt, 600, O.cabinets_svg(0, 0.75, yt, k=1), defs=d, bg=S1)
    # desk: sitter's side (two drawer pedestals + knee-hole apron) 2.2 x 1.25 D
    D1, D2 = '#4f2617', '#7d4e2e'; o = [rect(-0.1, -0.1, 2.4, 1.5, D1, stroke=None, sw=0)]
    for x0 in (0.06, 1.56):
        for j in range(3):
            y = 0.06 + j * 0.39; o.append(rect(x0, y, 0.58, 0.34, mul(D1, 1.22), stroke=mul(D1, 0.5), sw=W_DET * 1.3))
            o.append(pline([(x0 + 0.02, y + 0.32), (x0 + 0.02, y + 0.02), (x0 + 0.56, y + 0.02)], mul(D1, 1.75), W_DET))
            o.append(rect(x0 + 0.19, y + 0.13, 0.2, 0.05, BR, sw=W_DET, rx=0.015)); o.append(line(x0 + 0.21, y + 0.143, x0 + 0.37, y + 0.143, '#fff0b0', W_DET * 0.7))
    o.append(rect(0.7, 0.06, 0.8, 0.2, mul(D1, 1.22), stroke=mul(D1, 0.5), sw=W_DET * 1.3)); o.append(circ(1.1, 0.16, 0.03, BR, sw=W_DET))
    o.append(rect(0.7, 0.3, 0.8, 1.2, mul(D1, 0.45), stroke=mul(D1, 0.4), sw=W_DET * 1.3))            # knee-hole
    job('desk_front', 0, 0, 2.2, 1.25, 500, ''.join(o))
    # desk top: boards, a green blotter with paper, the warm pool of the banker's lamp painted in
    o = [rect(-0.1, -0.1, 2.5, 1.5, D2, stroke=None, sw=0)]
    for j in range(6): o.append(line(-0.1, 0.1 + j * 0.21, 2.5, 0.1 + j * 0.21, mul(D2, 0.8 if j % 2 else 1.18), W_DET))
    o.append('<radialGradient id="lp" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#ffd27a" stop-opacity="0.75"/><stop offset="0.6" stop-color="#f0a04f" stop-opacity="0.3"/><stop offset="1" stop-color="#e08a3c" stop-opacity="0"/></radialGradient>')
    o.append(rect(0.62, 0.52, 1.0, 0.62, '#2f5a45', sw=W_DET * 1.5, rx=0.02)); o.append(rect(0.62, 0.52, 0.1, 0.62, '#4f2617', sw=W_DET)); o.append(rect(1.52, 0.52, 0.1, 0.62, '#4f2617', sw=W_DET))
    o.append(ell(1.55, 0.5, 0.95, 0.62, 'url(#lp)', stroke=None, sw=0))
    job('desk_top', 0, 0, 2.3, 1.3, 500, ''.join(o))
    # a sheet of typed paper (used on the desk, the cabinets, the teletype)
    r = random.Random(6); o = [rect(-0.1, -0.1, 0.8, 0.9, '#f6efe2', stroke=None, sw=0), rect(0.004, 0.004, 0.492, 0.642, 'none', sw=W_DET * 1.2)]
    o.append(line(0.06, 0.08, 0.36, 0.08, O.PRINT_D, W_DET * 1.8))
    for j in range(11): o.append(O.greek(0.05, 0.14 + j * 0.043, 0.4 - r.uniform(0, 0.1), '#9a8f86', W_DET * 0.9, r))
    job('paper', 0, 0, 0.5, 0.65, 500, ''.join(o))
    # teletype front (v2 drawing cropped to the machine body)
    x, w, ytt = 0.0, 0.9, -1.2
    job('teletype', x, ytt - 0.64, w, 0.60, 600, O.teletype_svg(x, w, 0.0), defs=d, bg='#20263c')
    # coat stand with trench coat and fedora (alpha card)
    job('coatstand', -0.42, -3.4, 0.84, 3.4 + O.MID_BASE + 0.02, 400, O.coatstand_svg(0.0).split('/>', 1)[1], defs=d, transparent=True)
    # radiator front
    C = '#5d6478'; k = 12; o = []
    for i in range(k):
        xx = i * 0.105; o.append(rect(xx, 0.0, 0.105, 0.9, C if i % 2 else mul(C, 1.08), sw=W_DET * 1.4, rx=0.04))
        o.append(line(xx + 0.03, 0.06, xx + 0.03, 0.82, mul(C, 1.5), W_DET)); o.append(line(xx + 0.08, 0.07, xx + 0.08, 0.83, mul(C, 0.62), W_DET))
    o.append(rect(-0.01, 0.1, k * 0.105 + 0.02, 0.05, mul(C, 0.8), sw=W_DET)); o.append(rect(-0.01, 0.73, k * 0.105 + 0.02, 0.05, mul(C, 0.8), sw=W_DET))
    job('radiator', 0, 0, k * 0.105, 0.9, 500, ''.join(o), bg=mul(C, 0.7))

ALL = [wallpaper, frieze, wainscot, planks, rug_tile, rug_end, ceiling, beam, wall_map, wall_props, sky, furniture]

def ensure(verbose=True):
    """Draw every texture, rasterise the ones whose SVG changed, return {name: png path}."""
    os.makedirs(TEX, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    JOBS.clear()
    for f in ALL: f()
    mpath = os.path.join(TEX, 'manifest.json'); man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    todo = []; out = {}
    for name, j in JOBS.items():
        h = hashlib.sha1((j['svg'] + str(j['transparent'])).encode()).hexdigest(); png = os.path.join(TEX, name + '.png'); out[name] = png
        if man.get(name) != h or not os.path.exists(png):
            sp = os.path.join(TMP, name + '.svg'); open(sp, 'w').write(j['svg'])
            todo.append(dict(src=sp, out=png, w=j['w'], h=j['h'], transparent=j['transparent'])); man[name] = h
    if todo:
        jp = os.path.join(TMP, 'tex_jobs.json'); json.dump(todo, open(jp, 'w'))
        r = subprocess.run(['node', os.path.join(HERE, 'raster.js'), jp], env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')),
                           capture_output=True, text=True)
        if r.returncode != 0: raise RuntimeError('texture raster failed: ' + r.stderr[-2000:])
        if verbose: print('textures rasterised:', ', '.join(os.path.basename(t['out']) for t in todo))
        json.dump(man, open(mpath, 'w'), indent=0)
    return out

if __name__ == '__main__':
    p = ensure(); print(json.dumps({k: (v, SIZE[k]) for k, v in p.items()}, indent=1))
