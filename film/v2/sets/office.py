#!/usr/bin/env python3
"""Illustrated 1938 U.S. Weather Bureau office set (pure 2D, procedural SVG, Python stdlib only).

Public API:  build(state, uid)  build_insert_map(state, uid)  compose(built, cam, actors)  layer_transform(cam, parallax)
             track_point(u)  track_slice(u0, u1)  dummy_actors()  measure(png)
World convention: unit = D (head diameter), x right, y DOWN, actors' floor contact line y = 0,
x = 0 is the horizontal centre of the wall map.  See API.md next to this file.
CLI:  python3 office.py frames     (writes the review PNGs + compare.jpg + metrics)
Reviewed and repaired 2026-11-11 (palette, painted shading, map tone, erase continuity, halo): see REVIEW.md; checks in review.py.
"""
import math, random, json, os, sys, subprocess, re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
K = 100.0                       # internal SVG units per D (keeps font sizes and strokes in sane ranges)
INK = '#2a1712'                 # set-object silhouette ink (warm near-black)
W_OBJ = 0.020                   # object silhouette: 3 px at 150 px per D (two-shot)
W_DET = 0.010                   # detail line: 1.5 px at 150 px per D
SLAB = "'DejaVu Serif','Caladea','Liberation Serif',serif"       # slab-like bold capitals (system fonts)
MONO = "'DejaVu Sans Mono','Liberation Mono',monospace"

# ----------------------------------------------------------------------------- colour helpers
def rgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) for i in (0, 2, 4)]
def hx(c): return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(v)))) for v in c)
def mul(h, f): return hx([v * f for v in rgb(h)])
def mix(a, b, t): return hx([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])
def det(fill, f=0.68): return mul(fill, f)          # detail line colour = surface x 0.68

# ----------------------------------------------------------------------------- SVG primitives (inputs in D)
def n(v):
    s = '%.1f' % (v * K)
    if s.endswith('.0'): s = s[:-2]
    return '0' if s == '-0' else s
LW = [1.0]                      # global line-weight multiplier (the insert drawing uses thinner lines)
SHADE = [None]                  # while a build runs: id of the soft top-light / plum-shade gradient laid over every inked shape
def _sh(fill, stroke, sw, extra):
    """True when a shape is an inked object fill that should get the painted two-tone overlay (the reference never leaves a fill flat)."""
    return bool(SHADE[0]) and stroke == INK and sw >= 0.0129 and isinstance(fill, str) and fill[:1] == '#' and 'fill-opacity' not in extra
def _ov(geom, extra): return geom + f' fill="url(#{SHADE[0]})"' + (' ' + extra if extra else '') + '/>'
def _st(fill, stroke, sw, extra=''):
    a = f'fill="{fill}"'
    if stroke and stroke != 'none' and sw: a += f' stroke="{stroke}" stroke-width="{n(sw * LW[0])}" stroke-linejoin="round" stroke-linecap="round"'
    return a + (' ' + extra if extra else '')
def rect(x, y, w, h, fill, stroke=INK, sw=W_OBJ, rx=0, extra='', shade=True):
    g = f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"' + (f' rx="{n(rx)}"' if rx else '')
    return g + ' ' + _st(fill, stroke, sw, extra) + '/>' + (_ov(g, extra) if shade and _sh(fill, stroke, sw, extra) else '')
def poly(pts, fill, stroke=INK, sw=W_OBJ, extra='', shade=True):
    g = '<polygon points="' + ' '.join(f'{n(x)},{n(y)}' for x, y in pts) + '"'
    return g + ' ' + _st(fill, stroke, sw, extra) + '/>' + (_ov(g, extra) if shade and _sh(fill, stroke, sw, extra) else '')
def pline(pts, stroke, sw=W_DET, extra=''):
    return '<polyline points="' + ' '.join(f'{n(x)},{n(y)}' for x, y in pts) + '" ' + _st('none', stroke, sw, extra) + '/>'
def line(x1, y1, x2, y2, stroke=INK, sw=W_DET, extra=''):
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" stroke="{stroke}" stroke-width="{n(sw * LW[0])}" stroke-linecap="round"' + (' ' + extra if extra else '') + '/>'
def circ(x, y, r, fill, stroke=INK, sw=W_OBJ, extra='', shade=True):
    g = f'<circle cx="{n(x)}" cy="{n(y)}" r="{n(r)}"'
    return g + ' ' + _st(fill, stroke, sw, extra) + '/>' + (_ov(g, extra) if shade and _sh(fill, stroke, sw, extra) else '')
def ell(x, y, rx, ry, fill, stroke=INK, sw=W_OBJ, extra='', shade=True):
    g = f'<ellipse cx="{n(x)}" cy="{n(y)}" rx="{n(rx)}" ry="{n(ry)}"'
    return g + ' ' + _st(fill, stroke, sw, extra) + '/>' + (_ov(g, extra) if shade and _sh(fill, stroke, sw, extra) else '')
def pd(*tok):
    """Path data from tokens: command letters and numbers in D (arc flags/rotation are left unscaled)."""
    out = []; cmd = ''; i = 0
    for t in tok:
        if isinstance(t, str): cmd = t; i = 0; out.append(t)
        else:
            if cmd in 'Aa' and (i % 7) in (2, 3, 4): out.append('%g' % t)
            else: out.append(n(t))
            i += 1
    return ' '.join(out)
def path(d, fill, stroke=INK, sw=W_OBJ, extra='', shade=True):
    g = f'<path d="{d}"'
    return g + ' ' + _st(fill, stroke, sw, extra) + '/>' + (_ov(g, extra) if shade and _sh(fill, stroke, sw, extra) else '')
def tone(shape, gid):
    """Lay a soft gradient (id without '#') over a shape drawn by one of the primitives: pass the primitive's own output for a fill-only copy."""
    return re.sub(r' fill="[^"]*"', f' fill="url(#{gid})"', re.sub(r' stroke(-[a-z]+)?="[^"]*"', '', shape.split('/>')[0] + '/>'), count=1)
def text(x, y, s, size, fill, font=SLAB, weight='bold', anchor='middle', ls=0, extra=''):
    return (f'<text x="{n(x)}" y="{n(y)}" font-family="{font}" font-size="{n(size)}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"' + (f' letter-spacing="{n(ls)}"' if ls else '') + (' ' + extra if extra else '') + f'>{s}</text>')
def grp(body, extra=''): return f'<g {extra}>' + (body if isinstance(body, str) else ''.join(body)) + '</g>'
def rot(body, a, cx, cy): return grp(body, f'transform="rotate({a:g} {n(cx)} {n(cy)})"')
def smooth(pts, closed=False, t=0.5):
    """Catmull-Rom spline through pts as cubic Bezier path data (hand-drawn looking coast lines)."""
    P = list(pts); m = len(P)
    if m < 3: return pd('M', *P[0], 'L', *[c for p in P[1:] for c in p])
    g = (lambda i: P[i % m]) if closed else (lambda i: P[max(0, min(m - 1, i))])
    d = ['M', n(P[0][0]), n(P[0][1])]
    for i in range(m if closed else m - 1):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += ['C', n(c1[0]), n(c1[1]), n(c2[0]), n(c2[1]), n(p2[0]), n(p2[1])]
    if closed: d.append('Z')
    return ' '.join(d)
def greek(x, y, w, col, sw=W_DET, rnd=None, gap=0.3):
    """One line of illegible 'text': a dashed bar."""
    r = rnd or random; o = []; cx = x
    while cx < x + w - 0.01:
        l = min(r.uniform(0.03, 0.09), x + w - cx); o.append(line(cx, y, cx + l, y, col, sw)); cx += l + sw * (1 + 4 * gap)
    return ''.join(o)

# ----------------------------------------------------------------------------- room geometry (D)
WORLD = (-4.6, -8.2, 4.6, 4.8)          # x0, y0, x1, y1
VPX, VPY = 0.0, -2.5                    # vanishing point = eye line (head-centre height)
Z0 = 6.0                                # painted camera distance to the actor plane
WALL_BASE, WALL_TOP = -0.40, -5.30      # back wall meets floor / ceiling
WALL_X0, WALL_X1 = -3.7, 3.7
Y_BASEB, Y_CHAIR0, Y_CHAIR1 = -0.54, -1.18, -1.27       # baseboard top, chair rail bottom / top
Y_PRAIL0, Y_PRAIL1 = -4.72, -4.80                       # picture rail
MAP_OUT = (-1.60, -3.68, 1.60, -1.32)   # outer frame of the wall map
MAP_IN = (-1.50, -3.58, 1.50, -1.42)    # paper
GEO_TOP = -3.30                         # below the title strip
NY_REF = (0.05, -2.625)                 # lat 40.7 N, lon 73.95 W
KY, KX = 15.0, 18.66                    # degrees per D
HERO_X, BOSS_X = -0.55, 1.30
LAMPS = [(-1.7, -4.72, 0.20), (1.7, -4.72, 0.20), (0.0, -6.30, 0.27)]    # pendant bulbs: x, y, radius

def fp(X, Z):
    """Floor point: lateral X (measured at the actor line) and true depth Z toward the camera (D)."""
    s = Z0 / (Z0 - Z); return (VPX + (X - VPX) * s, VPY + (0 - VPY) * s)
def fs(Z): return Z0 / (Z0 - Z)                      # perspective scale of things standing at depth Z
def zy(y): return Z0 - Z0 * (0 - VPY) / (y - VPY)    # inverse: depth Z of the floor line at screen y
def geo(lat, lon): return (NY_REF[0] + (lon + 73.95) / KX, NY_REF[1] - (lat - 40.7) / KY)

# ----------------------------------------------------------------------------- map data (lon, lat), hand-simplified
COAST = [(-104, 52), (-68.6, 52), (-68.3, 49.3), (-69.7, 48.15), (-70.9, 47.0), (-71.2, 46.82), (-70.2, 47.2), (-69.4, 47.9), (-68.4, 48.5),
         (-67.2, 48.95), (-65.4, 49.25), (-64.2, 48.8), (-64.6, 48.3), (-66.2, 48.05), (-65.0, 47.8), (-64.7, 47.3), (-65.2, 47.0),
         (-64.6, 46.3), (-63.8, 45.95), (-62.7, 45.7), (-61.9, 45.85), (-61.45, 45.65), (-61.3, 46.3), (-60.6, 47.0), (-60.3, 46.75),
         (-60.1, 46.2), (-59.9, 45.9), (-60.8, 45.5), (-61.2, 45.25), (-63.5, 44.6), (-64.4, 44.15), (-65.6, 43.45), (-66.15, 43.8),
         (-65.9, 44.55), (-64.8, 45.1), (-64.5, 45.65), (-65.1, 45.55), (-66.05, 45.25), (-67.0, 45.1), (-67.4, 44.6), (-68.2, 44.3),
         (-68.9, 44.2), (-69.8, 43.8), (-70.25, 43.65), (-70.7, 43.05), (-70.6, 42.65), (-71.0, 42.35), (-70.65, 41.95), (-70.5, 41.78),
         (-70.0, 41.78), (-69.95, 42.0), (-70.2, 42.08), (-70.05, 41.9), (-69.95, 41.65), (-70.6, 41.55), (-70.95, 41.6), (-71.35, 41.48),
         (-71.5, 41.37), (-72.1, 41.3), (-72.9, 41.25), (-73.4, 41.05), (-73.9, 40.85), (-74.05, 40.65), (-74.0, 40.45), (-74.1, 39.75),
         (-74.4, 39.35), (-74.95, 38.93), (-75.5, 39.5), (-75.1, 38.8), (-75.05, 38.3), (-75.35, 37.9), (-75.95, 37.1), (-76.0, 38.3),
         (-76.1, 39.4), (-76.5, 38.95), (-76.3, 38.0), (-76.3, 37.0), (-76.0, 36.9), (-75.75, 36.2), (-75.5, 35.25), (-76.5, 34.6),
         (-77.95, 33.85), (-78.9, 33.7), (-79.9, 32.75), (-81.1, 32.0), (-81.4, 30.4), (-80.55, 28.45), (-80.03, 26.7), (-80.15, 25.75),
         (-80.6, 25.15), (-81.1, 25.15), (-81.8, 26.1), (-82.2, 26.9), (-82.7, 27.8), (-83.05, 29.1), (-84.0, 30.05), (-85.4, 29.65),
         (-85.7, 30.15), (-87.2, 30.35), (-88.0, 30.25), (-89.1, 30.35), (-89.4, 29.95), (-89.15, 29.0), (-90.2, 29.1), (-91.3, 29.45),
         (-92.2, 29.55), (-93.85, 29.7), (-94.8, 29.3), (-97.2, 27.8), (-97.2, 25.95), (-97.7, 24.0), (-97.8, 22.3), (-97.6, 21.0), (-104, 21)]
LAKES = [[(-92.1, 46.8), (-89.2, 48.4), (-88.0, 48.9), (-86.4, 48.7), (-84.9, 47.95), (-84.4, 46.5), (-84.95, 46.75), (-87.4, 46.55),
          (-87.9, 47.45), (-88.5, 47.05), (-90.9, 46.6)],
         [(-84.9, 45.85), (-85.9, 46.0), (-87.0, 45.75), (-87.9, 44.6), (-87.9, 43.0), (-87.6, 41.85), (-87.2, 41.62), (-86.7, 41.8),
          (-86.3, 43.2), (-86.5, 44.0), (-85.6, 45.0), (-85.1, 45.6)],
         [(-84.5, 45.9), (-83.5, 46.1), (-82.0, 46.1), (-81.0, 45.95), (-80.0, 45.3), (-79.8, 44.75), (-80.9, 44.6), (-81.5, 45.2),
          (-81.75, 43.8), (-82.45, 43.0), (-82.6, 43.7), (-83.0, 44.05), (-83.9, 43.6), (-83.3, 44.3), (-83.4, 45.1), (-84.1, 45.6)],
         [(-83.5, 41.7), (-83.1, 42.05), (-82.5, 42.0), (-80.2, 42.6), (-78.9, 42.87), (-80.1, 42.15), (-81.7, 41.5), (-82.7, 41.45)],
         [(-79.8, 43.3), (-79.4, 43.65), (-77.6, 43.95), (-76.4, 44.15), (-76.4, 43.5), (-77.6, 43.27), (-79.05, 43.27)]]
ISLES = [[(-71.87, 41.07), (-72.3, 41.15), (-73.05, 40.97), (-73.75, 40.84), (-74.02, 40.6), (-73.8, 40.57), (-73.0, 40.66), (-72.5, 40.83)],   # Long Island
         [(-85.0, 21.6), (-84.2, 22.6), (-82.4, 23.15), (-81.2, 23.1), (-79.8, 22.75), (-78.3, 22.4), (-77.0, 21.4), (-76.0, 20.5), (-85, 20)],   # Cuba
         [(-59.3, 47.6), (-57.8, 47.65), (-56.0, 47.55), (-55.4, 46.9), (-54.6, 47.4), (-54.0, 46.8), (-53.1, 46.65), (-52.65, 47.5),
          (-53.2, 48.2), (-53.0, 48.7), (-53.9, 48.9), (-54.3, 49.6), (-55.8, 50.2), (-56.5, 51.5), (-57.6, 51.2), (-58.3, 49.5), (-58.7, 48.5), (-59.4, 48.1)],   # Newfoundland
         [(-64.4, 46.65), (-63.2, 46.5), (-62.0, 46.45), (-62.5, 46.0), (-63.4, 46.2), (-64.1, 46.35)],                                                # P.E.I.
         [(-64.5, 49.85), (-63.0, 49.75), (-61.7, 49.1), (-62.9, 49.2), (-64.2, 49.45)]]                                                               # Anticosti
ISLETS = [(-78.4, 26.65, 0.5, 0.14), (-77.1, 26.4, 0.16, 0.5), (-78.0, 24.45, 0.25, 0.7), (-77.35, 25.05, 0.2, 0.1), (-76.2, 25.1, 0.12, 0.55),
          (-75.2, 23.3, 0.12, 0.45), (-73.6, 21.3, 0.3, 0.12), (-64.75, 32.3, 0.14, 0.1), (-70.05, 41.3, 0.2, 0.08), (-70.6, 41.4, 0.16, 0.08)]   # Bahamas, Bermuda, Nantucket, M.V.
RIVERS = [[(-93.2, 45.0), (-91.2, 43.2), (-90.6, 41.5), (-91.3, 40.2), (-90.2, 38.6), (-89.2, 37.0), (-90.1, 35.1), (-91.1, 32.3), (-91.2, 30.5), (-90.1, 29.95)],
          [(-89.2, 37.0), (-87.5, 37.9), (-85.75, 38.25), (-84.5, 39.1), (-82.5, 38.4), (-80.7, 40.5), (-80.0, 40.45)],
          [(-71.2, 46.82), (-73.6, 45.5), (-75.5, 44.7), (-76.4, 44.2)], [(-73.95, 40.75), (-73.9, 42.0), (-73.75, 42.75)]]
BORDERS = [[(-95.2, 49.0), (-92.0, 48.5), (-89.5, 48.0)], [(-83.0, 45.9), (-82.4, 43.0)], [(-79.0, 43.2), (-74.7, 45.0), (-71.5, 45.0), (-70.3, 46.2), (-69.2, 47.45), (-67.8, 47.05), (-67.8, 45.7), (-67.0, 45.1)],
           [(-94.6, 49.0), (-94.6, 36.5), (-94.0, 33.0), (-93.85, 29.7)], [(-91.2, 36.5), (-75.9, 36.55)], [(-88.2, 35.0), (-88.4, 30.3)], [(-85.6, 35.0), (-85.0, 31.0), (-82.2, 30.6), (-81.5, 30.7)],
           [(-90.3, 35.0), (-83.1, 35.0), (-81.0, 35.1), (-78.55, 33.85)], [(-83.35, 35.0), (-81.1, 32.1)], [(-87.5, 41.7), (-87.5, 38.0)], [(-84.8, 41.75), (-84.8, 39.1)],
           [(-80.5, 42.3), (-80.5, 40.6)], [(-80.5, 39.72), (-75.8, 39.72)], [(-79.76, 42.0), (-75.3, 42.0), (-73.5, 42.05), (-71.4, 42.02)], [(-73.3, 45.0), (-73.45, 42.75), (-73.5, 41.2)]]
STATIONS = [(41.9, -87.6), (38.6, -90.2), (35.1, -90.0), (30.0, -90.1), (33.75, -84.4), (36.15, -86.8), (39.1, -84.5), (40.45, -80.0), (42.9, -78.9),
            (42.35, -83.05), (45.0, -93.2), (39.1, -94.6), (32.8, -96.8), (25.8, -80.2), (30.35, -81.6), (32.8, -79.95), (35.25, -75.55), (38.9, -77.0),
            (42.35, -71.05), (43.65, -70.25), (45.5, -73.6), (44.65, -63.6), (32.3, -64.75), (23.1, -82.4), (25.05, -77.35), (27.95, -82.5),
            (46.8, -92.1), (47.55, -52.7), (46.8, -71.2), (35.2, -80.85), (29.75, -95.4), (41.25, -96.0), (43.05, -87.9), (37.55, -77.45), (34.75, -92.3), (46.5, -84.35)]
TRACK_LL = [(25.6, -70.5), (27.6, -72.6), (30.3, -74.2), (33.3, -74.9), (36.3, -74.55), (38.8, -74.0), (40.62, -73.72)]

def _track_pts(nseg=14):
    """Red forecast track, storm symbol (off Florida) -> New York, as a dense polyline in D."""
    P = [geo(*p) for p in TRACK_LL]; out = []; m = len(P)
    for i in range(m - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(m - 1, i + 2)]
        for k in range(nseg):
            t = k / nseg; t2 = t * t; t3 = t2 * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    out.append(P[-1])
    L = [0.0]
    for a, b in zip(out[:-1], out[1:]): L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    # tiny hand wobble (a pencil line, not a ruled one); end points stay exact
    res = []
    for i, (p, l) in enumerate(zip(out, L)):
        w = 0.006 * math.sin(l * 31.0) * math.sin(math.pi * l / L[-1])
        if 0 < i < len(out) - 1:
            a, b = out[i - 1], out[i + 1]; dx, dy = b[0] - a[0], b[1] - a[1]; q = math.hypot(dx, dy) or 1
            p = (p[0] - dy / q * w, p[1] + dx / q * w)
        res.append((round(p[0], 4), round(p[1], 4)))
    return res
TRACK = _track_pts()
def _cum(pts):
    L = [0.0]
    for a, b in zip(pts[:-1], pts[1:]): L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return L
TRACK_L = _cum(TRACK)
def track_point(u):
    """Point on the track at fraction u (0 = storm symbol, 1 = New York) -> (x, y, heading_deg)."""
    u = max(0.0, min(1.0, u)); s = u * TRACK_L[-1]; i = 0
    while i < len(TRACK) - 2 and TRACK_L[i + 1] < s: i += 1
    a, b = TRACK[i], TRACK[i + 1]; seg = (TRACK_L[i + 1] - TRACK_L[i]) or 1; t = (s - TRACK_L[i]) / seg
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])))
def track_slice(u0, u1):
    """Polyline of the track between fractions u0 and u1."""
    if u1 <= u0: return []
    s0, s1 = u0 * TRACK_L[-1], u1 * TRACK_L[-1]; pts = [track_point(u0)[:2]]
    pts += [p for p, l in zip(TRACK, TRACK_L) if s0 < l < s1]; pts.append(track_point(u1)[:2]); return pts

# ----------------------------------------------------------------------------- the wall map (hero prop)
PAPER, PRINT = '#fff5df', '#836d4e'          # measured text-prop paper and printed ink
PRINT_D = '#574430'                          # same ink, a little darker for small lettering
LAND, SEA, SEA_D = '#c49b58', '#6b9aad', '#4d7f93'       # toned chart (old-gold land, teal sea): nothing large is paler than the heads
RED, RED_D = '#c8301c', '#a32413'

def map_defs(u):
    x0, y0, x1, y1 = MAP_IN
    return (f'<clipPath id="{u}mc"><rect x="{n(x0)}" y="{n(GEO_TOP)}" width="{n(x1 - x0)}" height="{n(y1 - GEO_TOP)}"/></clipPath>'
            f'<radialGradient id="{u}mage" cx="52%" cy="40%" r="78%"><stop offset="0.42" stop-color="#5a2a22" stop-opacity="0"/><stop offset="1" stop-color="#5a2a22" stop-opacity="0.42"/></radialGradient>'
            f'<radialGradient id="{u}mpl"><stop offset="0" stop-color="#fff3d2" stop-opacity="0.2"/><stop offset="1" stop-color="#fff3d2" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="{u}mst" gradientUnits="userSpaceOnUse" x1="0" y1="{n(y0)}" x2="0" y2="{n(y0 + 0.2)}"><stop offset="0" stop-color="#2a1025" stop-opacity="0.3"/><stop offset="1" stop-color="#2a1025" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{u}msl" gradientUnits="userSpaceOnUse" x1="{n(x0)}" y1="0" x2="{n(x0 + 0.16)}" y2="0"><stop offset="0" stop-color="#2a1025" stop-opacity="0.26"/><stop offset="1" stop-color="#2a1025" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="{u}msea" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{SEA}"/><stop offset="1" stop-color="{mix(SEA, SEA_D, 0.45)}"/></linearGradient>'
            f'<pattern id="{u}mw" patternUnits="userSpaceOnUse" width="{n(0.26)}" height="{n(0.13)}">' + line(0.02, 0.035, 0.1, 0.035, mul(SEA_D, 0.88), 0.008) + line(0.15, 0.1, 0.235, 0.1, mul(SEA_D, 0.88), 0.008) + line(0.125, 0.035, 0.15, 0.035, mul(SEA, 1.16), 0.007) + line(0.0, 0.1, 0.03, 0.1, mul(SEA, 1.16), 0.007) + '</pattern>')

def _ring(cx, cy, rx, ry, r, k=12, wob=0.07, ph=0.0):
    return [(cx + rx * (1 + wob * math.sin(3 * a + ph) + wob * 0.5 * r.uniform(-1, 1)) * math.cos(a),
             cy + ry * (1 + wob * math.cos(2 * a + ph)) * math.sin(a)) for a in [2 * math.pi * i / k for i in range(k)]]

def track_svg(st, wr):
    """Red pencil track + arrow head + eraser smudge, from the state."""
    ln = max(0.0, min(1.0, float(st.get('line', 0)))); er = max(0.0, min(1.0, float(st.get('erase', 0)))); o = []
    keep = ln * (1 - er)
    if er > 0 and ln > 0:
        sm = track_slice(keep, ln)
        if len(sm) > 1:
            o.append(pline(sm, '#f0a694', wr * 3.6, 'opacity="0.3"')); o.append(pline(sm, '#e07a66', wr * 1.6, 'opacity="0.26"'))
            o.append(pline(sm, RED, wr * 0.55, f'opacity="0.2" stroke-dasharray="{n(0.012)} {n(0.035)}"'))
            rr = random.Random(5); NS = 34
            for i in range(NS):                                   # rubbing strokes: fixed places on the paper, each fades in as the eraser passes it
                ui = (i + rr.uniform(0.15, 0.85)) / NS; da = rr.uniform(-42, 42); l = rr.uniform(0.028, 0.075); a_ = min(1.0, (ui - keep) / 0.035)
                if ui > ln or a_ <= 0: continue
                x, y, h = track_point(ui); a = math.radians(h + 62 + da)
                o.append(line(x - l * math.cos(a), y - l * math.sin(a), x + l * math.cos(a), y + l * math.sin(a), '#f6d9cf', wr * 0.7, f'opacity="{0.26 * a_:.3f}"'))
    ah = max(0.0, min(1.0, (ln - 0.97) / 0.03))                   # arrow head: drawn as the last flourish (line 0.97..1), rubbed out first (erase 0..0.06)
    ahk = ah * max(0.0, 1.0 - er / 0.06)
    if ah > 0 and er > 0:                                         # its pink ghost stays on the paper
        x, y, h = track_point(1.0)
        for da in (150, -150):
            a = math.radians(h + da); o.append(line(x, y, x + 0.13 * ah * math.cos(a), y + 0.13 * ah * math.sin(a), '#e58d7c', wr * 1.5, f'opacity="{0.3 * min(1.0, er / 0.06):.3f}"'))
    if keep > 0:
        pts = track_slice(0, keep); o.append(pline(pts, RED, wr)); o.append(pline(pts, RED_D, wr * 0.3, f'opacity="0.5" stroke-dasharray="{n(0.05)} {n(0.03)}"'))
        if ahk > 0:
            x, y, h = track_point(keep); h = track_point(1.0)[2]; L = 0.13 * ahk
            for da in (150, -150):
                a = math.radians(h + da); o.append(line(x, y, x + L * math.cos(a), y + L * math.sin(a), RED, wr))
    return ''.join(o)

def draw_map(u, st, hi=False):
    wo, wd = (0.0138, 0.0069) if hi else (W_OBJ, W_DET)
    r = random.Random(11); X0, Y0, X1, Y1 = MAP_OUT; x0, y0, x1, y1 = MAP_IN; o = []; FR = '#3d1c12'
    # frame moulding with trim strip and gold slip
    o.append(rect(X0, Y0, X1 - X0, Y1 - Y0, FR, sw=wo * 1.3))
    o.append(rect(X0 + 0.024, Y0 + 0.024, X1 - X0 - 0.048, Y1 - Y0 - 0.048, 'none', stroke=mul(FR, 1.9), sw=wd))
    if hi: o.append(rect(X0 + 0.05, Y0 + 0.05, X1 - X0 - 0.1, Y1 - Y0 - 0.1, 'none', stroke=mul(FR, 0.55), sw=wd))
    for (a, b), (c, d) in (((X0, Y0), (x0, y0)), ((X1, Y0), (x1, y0)), ((X0, Y1), (x0, y1)), ((X1, Y1), (x1, y1))): o.append(line(a, b, c, d, INK, wd))
    o.append(rect(x0 - 0.03, y0 - 0.03, x1 - x0 + 0.06, y1 - y0 + 0.06, '#cb9f48', stroke=INK, sw=wd))
    o.append(rect(x0, y0, x1 - x0, y1 - y0, PAPER, stroke=INK, sw=wd))
    g = [rect(x0, GEO_TOP, x1 - x0, y1 - GEO_TOP, f'url(#{u}msea)', stroke=None, sw=0), rect(x0, GEO_TOP, x1 - x0, y1 - GEO_TOP, f'url(#{u}mw)', stroke=None, sw=0, extra='opacity="0.85"')]
    land = smooth([geo(la, lo) for lo, la in COAST], closed=True, t=0.4)
    g.append(path(land, 'none', stroke=SEA_D, sw=0.06 if not hi else 0.05, extra='opacity="0.55"'))          # water lining along the coast
    if hi: g.append(path(land, 'none', stroke=mix(SEA_D, PRINT, 0.25), sw=0.1, extra=f'opacity="0.35" stroke-dasharray="{n(0.006)} {n(0.012)}"'))
    g.append(path(land, LAND, stroke=PRINT_D, sw=wd * 1.5))
    for isl in ISLES:
        d = smooth([geo(la, lo) for lo, la in isl], closed=True, t=0.4); g.append(path(d, 'none', stroke=SEA_D, sw=0.04, extra='opacity="0.5"')); g.append(path(d, LAND, stroke=PRINT_D, sw=wd * 1.3))
    for lo, la, a, b in ISLETS:
        x, y = geo(la, lo); g.append(ell(x, y, a / KX * 0.5 + 0.004, b / KY * 0.5 + 0.004, LAND, stroke=PRINT_D, sw=wd))
    for lk in LAKES: g.append(path(smooth([geo(la, lo) for lo, la in lk], closed=True, t=0.4), SEA, stroke=PRINT_D, sw=wd * 1.2))
    for rv in RIVERS: g.append(path(smooth([geo(la, lo) for lo, la in rv]), 'none', stroke=mix(SEA_D, PRINT, 0.3), sw=wd))
    for bd in BORDERS: g.append(pline([geo(la, lo) for lo, la in bd], mix(LAND, PRINT, 0.55), wd * 0.8, f'stroke-dasharray="{n(0.03)} {n(0.018)}"'))
    # graticule
    gc = mix(LAND, PRINT, 0.5); step = 2.5 if hi else 5.0; lo = -100.0
    while lo <= -47:
        major = abs(lo / 5 - round(lo / 5)) < 1e-6; x = geo(40, lo)[0]; g.append(line(x, GEO_TOP, x, y1, gc, wd * (0.8 if major else 0.45), 'opacity="0.7"')); lo += step
    la = 25.0
    while la <= 50:
        major = abs(la / 5 - round(la / 5)) < 1e-6; y = geo(la, -74)[1]; g.append(line(x0, y, x1, y, gc, wd * (0.8 if major else 0.45), 'opacity="0.7"')); la += step
    # isobars: rings round the storm, an Atlantic high, a trough over the land
    ic = PRINT; isea = mix(SEA_D, '#22364a', 0.45); sx, sy = TRACK[0]; iw = wd * (1.15 if hi else 1.0)     # isobars: brown over land, slate over the sea
    for i, rad in enumerate((0.07, 0.125, 0.19) + ((0.27,) if hi else ())):
        g.append(path(smooth(_ring(sx + 0.01 * i, sy - 0.012 * i, rad, rad * 1.08, r, ph=i), closed=True), 'none', stroke=isea, sw=iw * 1.15, extra='opacity="0.9"'))
    hx_, hy_ = geo(33.5, -55.5)
    for i, rad in enumerate((0.16, 0.34, 0.53, 0.73)):
        g.append(path(smooth(_ring(hx_ + 0.03 * i, hy_ - 0.02 * i, rad, rad * 0.8, r, k=14, wob=0.05, ph=1.3 * i), closed=True), 'none', stroke=isea, sw=iw * 1.15, extra='opacity="0.85"'))
    for off, amp in ((-1.42, 0.16), (-1.1, 0.2), (-0.74, 0.22), (-0.34, 0.14)) + (((-0.55, 0.2), (-0.93, 0.21), (-1.27, 0.18)) if hi else ()):
        pts = [(off + amp * math.sin((yy + 3.35) / 2.0 * math.pi * 1.1) + 0.05 * math.sin(yy * 4 + off * 3), yy) for yy in [-3.36 + 0.2 * k for k in range(11)]]
        g.append(path(smooth(pts), 'none', stroke=ic, sw=iw, extra='opacity="0.55"'))
    # weather stations: circle + wind barb
    rs = random.Random(4)
    for k, (la, lo) in enumerate(STATIONS if hi else STATIONS[:26]):
        x, y = geo(la, lo); a = rs.uniform(0, 2 * math.pi); l = 0.05 if hi else 0.06; ex, ey = x + l * math.cos(a), y + l * math.sin(a)
        g.append(line(x, y, ex, ey, PRINT_D, wd * 0.9))
        for j in range(rs.choice((1, 2, 2))):
            bx, by = x + (l - 0.014 * j) * math.cos(a), y + (l - 0.014 * j) * math.sin(a); g.append(line(bx, by, bx + 0.022 * math.cos(a + 1.9), by + 0.022 * math.sin(a + 1.9), PRINT_D, wd * 0.9))
        g.append(circ(x, y, 0.013 if hi else 0.015, PAPER if rs.random() < 0.6 else PRINT_D, stroke=PRINT_D, sw=wd * 0.9))
        if hi:
            g.append(greek(x + 0.02, y - 0.022, rs.uniform(0.04, 0.07), mix(LAND, PRINT_D, 0.8), wd * 0.8, rs)); g.append(greek(x + 0.02, y + 0.03, rs.uniform(0.03, 0.05), mix(LAND, PRINT_D, 0.6), wd * 0.7, rs))
    # past positions of the storm (small dashed ink trail from the south-east) and the storm symbol
    past = [geo(20.3, -58.5), geo(21.6, -62.5), geo(23.2, -66.6), (sx, sy)]
    g.append(path(smooth(past), 'none', stroke=PRINT_D, sw=wd * 1.1, extra=f'stroke-dasharray="{n(0.025)} {n(0.02)}"'))
    for px, py in past[1:3]: g.append(circ(px, py, 0.014, PAPER, stroke=PRINT_D, sw=wd))
    SC = '#8f1f1c'; q = 0.036
    g.append(path(pd('M', sx - q, sy, 'C', sx - q, sy - q * 1.5, sx + q * 0.6, sy - q * 2.1, sx + q * 1.7, sy - q * 1.7), 'none', stroke=SC, sw=wd * 1.7))
    g.append(path(pd('M', sx + q, sy, 'C', sx + q, sy + q * 1.5, sx - q * 0.6, sy + q * 2.1, sx - q * 1.7, sy + q * 1.7), 'none', stroke=SC, sw=wd * 1.7))
    g.append(circ(sx, sy, q, PAPER, stroke=SC, sw=wd * 1.7)); g.append(circ(sx, sy, q * 0.38, SC, stroke=None, sw=0))
    # labels (only these are legible)
    nx, ny = TRACK[-1]; bx, by = geo(42.35, -71.05)
    g.append(circ(nx, ny, 0.02, PAPER, stroke=PRINT_D, sw=wd * 1.4)); g.append(circ(bx, by, 0.013, PRINT_D, stroke=None, sw=0))
    g.append(text(nx + 0.085, ny + 0.115, 'N.Y.', 0.105, PRINT_D, anchor='start', ls=0.006))
    g.append(text(bx + 0.05, by - 0.022, 'BOSTON', 0.066, PRINT_D, anchor='start', ls=0.005))
    g.append(text(-0.085, -1.795, 'FLA.', 0.072, PRINT_D, ls=0.005))
    g.append(text(hx_, hy_ + 0.045, 'H', 0.13, isea, extra='opacity="0.9"'))
    if hi:
        for (la, lo, s, w_) in ((45.3, -66.0, 0, 0.16), (36.0, -79.5, 0, 0.18), (33.0, -83.5, 0, 0.14), (40.8, -89.5, 0, 0.2), (44.5, -98, 0, 0.2), (31.5, -93, 0, 0.16), (37.6, -85, 0, 0.14),
                               (47.2, -76.5, 0, 0.2), (29.5, -62, 0, 0.26), (41.5, -62.5, 0, 0.3), (24.5, -88.5, 0, 0.24), (36.5, -67.5, 0, 0.12)):
            x, y = geo(la, lo); g.append(greek(x, y, w_, mix(LAND, PRINT_D, 0.75), wd * 1.5, rs, gap=0.5))
        for la in (25, 30, 35, 40, 45, 50): g.append(text(x0 + 0.02, geo(la, -74)[1] - 0.012, '%d°' % la, 0.04, PRINT, font=SLAB, weight='normal', anchor='start'))
        for lo in (-100, -90, -80, -70, -60, -50): g.append(text(geo(40, lo)[0] + 0.012, y1 - 0.015, '%d°' % -lo, 0.04, PRINT, weight='normal', anchor='start'))
        for (px, py, s) in ((0.52, -2.93, '1012'), (0.62, -1.72, '1016'), (-1.2, -2.5, '1008'), (0.33, -1.47, '996')): g.append(text(px, py, s, 0.038, PRINT, weight='normal'))
        # legend box + scale bar (greeked) in the Gulf corner, compass in the Atlantic corner
        lx, ly = x0 + 0.05, y1 - 0.4; g.append(rect(lx, ly, 0.52, 0.35, PAPER, stroke=PRINT_D, sw=wd)); g.append(rect(lx + 0.015, ly + 0.015, 0.49, 0.32, 'none', stroke=PRINT, sw=wd * 0.6))
        g.append(greek(lx + 0.06, ly + 0.06, 0.4, PRINT_D, wd * 2, rs, gap=0.6))
        for j in range(4):
            yy = ly + 0.115 + j * 0.052; g.append(circ(lx + 0.06, yy, 0.012, PAPER if j % 2 else PRINT_D, stroke=PRINT_D, sw=wd * 0.8)); g.append(greek(lx + 0.1, yy, rs.uniform(0.2, 0.36), PRINT, wd, rs))
        cx_, cy_ = x1 - 0.2, y1 - 0.2
        for a in range(0, 360, 45):
            rr_ = 0.11 if a % 90 == 0 else 0.065; g.append(line(cx_, cy_, cx_ + rr_ * math.sin(math.radians(a)), cy_ - rr_ * math.cos(math.radians(a)), PRINT_D, wd))
        g.append(circ(cx_, cy_, 0.05, 'none', stroke=PRINT_D, sw=wd * 0.8)); g.append(text(cx_, cy_ - 0.125, 'N', 0.05, PRINT_D))
        for j in range(5): g.append(rect(x1 - 0.95 + j * 0.09, y1 - 0.07, 0.09, 0.018, PRINT_D if j % 2 == 0 else PAPER, stroke=PRINT_D, sw=wd * 0.6))
    g.append(track_svg(st, 0.038 if not hi else 0.035))
    o.append(grp(g, f'clip-path="url(#{u}mc)"'))
    # title strip: rules, one legible line, the rest greeked
    o.append(line(x0, GEO_TOP, x1, GEO_TOP, PRINT_D, wd * 1.3)); o.append(line(x0, GEO_TOP - 0.022, x1, GEO_TOP - 0.022, PRINT, wd * 0.6))
    o.append(text(0.1, y0 + 0.178, 'DAILY WEATHER MAP', 0.104, PRINT, ls=0.016))
    for j, w_ in enumerate((0.4, 0.32, 0.24)): o.append(greek(x0 + 0.06, y0 + 0.075 + j * 0.05, w_, PRINT, wd * (1.6 if j == 0 else 1.0), rs, gap=0.5))
    o.append(circ(x0 + 0.6, y0 + 0.13, 0.055, 'none', stroke=PRINT, sw=wd)); o.append(circ(x0 + 0.6, y0 + 0.13, 0.035, 'none', stroke=PRINT, sw=wd * 0.6))
    for j, w_ in enumerate((0.3, 0.38)): o.append(greek(x1 - 0.5, y0 + 0.2 - j * 0.045 + 0.0, w_, PRINT, wd, rs, gap=0.5))
    # painted light on the sheet: lighter pool up the middle, old-paper corners, soft shade thrown by the frame along the top and left edges
    o.append(ell(0.15, -2.75, 1.25, 0.85, f'url(#{u}mpl)', stroke=None, sw=0)); o.append(rect(x0, y0, x1 - x0, y1 - y0, f'url(#{u}mage)', stroke=None, sw=0))
    o.append(rect(x0, y0, x1 - x0, 0.2, f'url(#{u}mst)', stroke=None, sw=0)); o.append(rect(x0, y0, 0.16, y1 - y0, f'url(#{u}msl)', stroke=None, sw=0))
    # date slip pinned over the top-right corner
    slip = [rect(0.8, -3.84, 0.8, 0.225, PAPER, sw=wd * 1.4), rect(0.816, -3.824, 0.768, 0.193, 'none', stroke=PRINT, sw=wd * 0.6),
            text(1.2, -3.682, 'SEPT 20 1938', 0.08, PRINT_D, ls=0.006), circ(1.2, -3.822, 0.02, '#b61d32', sw=wd), circ(1.194, -3.828, 0.006, '#f3b3a8', stroke=None, sw=0)]
    o.append(rot(slip, -3.5, 1.2, -3.72))
    return ''.join(o)

def ledge_svg(st, hi=False):
    """Pencil ledge under the map: eraser, pencils, and the eraser crumbs that the boss leaves."""
    wo, wd = (0.0138, 0.0069) if hi else (W_OBJ, W_DET); X0, Y0, X1, Y1 = MAP_OUT; o = []; WD = '#7b3b26'; yt = Y1 - 0.005
    for k_, a_ in ((0.16, 0.2), (0.09, 0.2)): o.append(rect(X0 - 0.06, yt + 0.09, X1 - X0 + 0.12, k_, '#1a1025', stroke=None, sw=0, extra=f'opacity="{a_}"'))
    for bx in (X0 + 0.25, X1 - 0.25): o.append(poly([(bx - 0.05, yt + 0.09), (bx + 0.05, yt + 0.09), (bx, yt + 0.2)], mul(WD, 0.75), sw=wd))
    o.append(rect(X0 - 0.09, yt, X1 - X0 + 0.18, 0.1, WD, sw=wo)); o.append(rect(X0 - 0.09, yt, X1 - X0 + 0.18, 0.034, mul(WD, 1.42), sw=wd))
    o.append(line(X0 - 0.07, yt + 0.068, X1 + 0.07, yt + 0.068, mul(WD, 0.6), wd))
    # felt eraser block, pink rubber, two pencils, a chalk stub, a folded cloth
    o.append(rect(-1.32, yt - 0.075, 0.24, 0.075, '#4d3f44', sw=wd * 1.4)); o.append(rect(-1.32, yt - 0.075, 0.24, 0.028, '#b08a52', sw=wd * 1.2))
    o.append(rot(rect(0.74, yt - 0.052, 0.13, 0.052, '#e58d86', sw=wd * 1.3, rx=0.008) + line(0.80, yt - 0.05, 0.80, yt - 0.003, '#b8605c', wd), -4, 0.8, yt))
    o.append(rot(rect(-0.86, yt - 0.03, 0.34, 0.03, '#c8301c', sw=wd * 1.2) + poly([(-0.52, yt - 0.03), (-0.46, yt - 0.015), (-0.52, yt)], '#e9c79a', sw=wd * 1.2), -1.5, -0.7, yt))
    o.append(rect(1.18, yt - 0.028, 0.3, 0.028, '#2f5a8a', sw=wd * 1.2)); o.append(poly([(1.18, yt - 0.028), (1.125, yt - 0.014), (1.18, yt)], '#e9c79a', sw=wd * 1.2))
    o.append(rect(-0.3, yt - 0.034, 0.1, 0.034, PAPER, sw=wd * 1.2))
    er = max(0.0, min(1.0, float(st.get('erase', 0)))) * (1 if float(st.get('line', 0)) > 0 else 0)
    if er > 0:
        rr = random.Random(9); nx = TRACK[-1][0]
        for i in range(int(math.ceil(30 * er))):
            x = nx + rr.gauss(0.02, 0.17); s = rr.uniform(0.006, 0.014)
            o.append(ell(x, yt - s * 0.6, s * 1.3, s * 0.7, rr.choice(('#e9a093', '#dc8375', '#f1cfc0')), stroke=mul('#dc8375', 0.6), sw=wd * 0.6, extra=f'transform="rotate({rr.uniform(-40, 40):.0f} {n(x)} {n(yt)})"'))
    return ''.join(o)

# ----------------------------------------------------------------------------- palette
WALL, WALL_HI = '#9c3139', '#d59a58'        # rose paper + tan-gold motif (the orange-brown paper of the first build merged with wainscot, floor and map)
WOOD, PANEL, RAILC, BASEC = '#5f2a1a', '#7a3a21', '#96502c', '#3b1a12'
FRIEZE, PRAIL = '#7a3037', '#c9a878'
CEIL, BEAM = '#64323c', '#34142a'
FLOOR, SEAM = '#99695c', '#3f2224'
STEEL, STEEL_HI = '#51578f', '#5f66a3'       # filing cabinets: steel-violet (green stays an accent: lamp shades and the sign)
NAVY, RUGRED, GOLD = '#233a68', '#84222a', '#cb9f48'
BRASS, GREEN, GREEN_D = '#e2a630', '#3c7250', '#2d664a'
BULB = '#fffeec'

def room_defs(u):
    d = []; W_, H_ = 0.32, 0.76
    t = [rect(0, 0, W_, H_, WALL, stroke=None, sw=0)]
    for x in (0.0, 0.28): t.append(rect(x, 0, 0.04, H_, mul(WALL, 0.88), stroke=None, sw=0))
    t.append(rect(0.12, 0, 0.08, H_, mul(WALL, 0.88), stroke=None, sw=0))
    for x in (0.12, 0.28): t.append(line(x, 0, x, H_, det(WALL, 0.72), 0.007))
    for x in (0.0, 0.16): t.append(line(x, 0, x, H_, mul(WALL, 1.12), 0.005))
    for cx, cy in ((0.08, 0.19), (0.24, 0.57)):                          # stencilled sprig: lozenge, two buds, a bar and a dot
        t.append(poly([(cx, cy - 0.07), (cx + 0.031, cy), (cx, cy + 0.07), (cx - 0.031, cy)], WALL_HI, stroke=det(WALL, 0.5), sw=0.009))
        t.append(poly([(cx, cy - 0.034), (cx + 0.013, cy), (cx, cy + 0.034), (cx - 0.013, cy)], mul(WALL, 1.1), stroke=None, sw=0))
        for dx in (-0.043, 0.043): t.append(circ(cx + dx, cy + 0.026, 0.0145, WALL_HI, stroke=det(WALL, 0.5), sw=0.008))
        t.append(line(cx - 0.036, cy + 0.092, cx + 0.036, cy + 0.092, mix(WALL, WALL_HI, 0.8), 0.011)); t.append(circ(cx, cy - 0.1, 0.0105, mix(WALL, WALL_HI, 0.8), stroke=None, sw=0))
    d.append(f'<pattern id="{u}wp" patternUnits="userSpaceOnUse" x="0" y="{n(-4.8)}" width="{n(W_)}" height="{n(H_)}">' + ''.join(t) + '</pattern>')
    # frieze stencil
    f = [rect(0, 0, 0.4, 0.5, FRIEZE, stroke=None, sw=0), line(0, 0.07, 0.4, 0.07, det(FRIEZE, 0.62), 0.01), line(0, 0.43, 0.4, 0.43, det(FRIEZE, 0.62), 0.01),
         poly([(0.2, 0.14), (0.28, 0.25), (0.2, 0.36), (0.12, 0.25)], mul(FRIEZE, 1.25), stroke=det(FRIEZE, 0.6), sw=0.009), circ(0.0, 0.25, 0.03, mul(FRIEZE, 1.25), stroke=det(FRIEZE, 0.6), sw=0.008),
         circ(0.4, 0.25, 0.03, mul(FRIEZE, 1.25), stroke=det(FRIEZE, 0.6), sw=0.008), line(0.05, 0.25, 0.1, 0.25, det(FRIEZE, 0.62), 0.008), line(0.3, 0.25, 0.35, 0.25, det(FRIEZE, 0.62), 0.008)]
    d.append(f'<pattern id="{u}fz" patternUnits="userSpaceOnUse" x="0" y="{n(-5.3)}" width="{n(0.4)}" height="{n(0.5)}">' + ''.join(f) + '</pattern>')
    g = lambda i, a: f'<stop offset="{i}" stop-color="#260a38" stop-opacity="{a}"/>'
    hl = lambda i, a, c='#fff0d0': f'<stop offset="{i}" stop-color="{c}" stop-opacity="{a}"/>'
    # painted two-tone overlays in objectBoundingBox units (one definition serves every shape): sv = lit from above, scyl = round form, srad = dial / globe
    d.append(f'<linearGradient id="{u}sv" x1="0.38" y1="0" x2="0.62" y2="1">{hl(0, 0.2)}{hl(0.42, 0)}{g(0.56, 0)}{g(1, 0.3)}</linearGradient>')
    d.append(f'<linearGradient id="{u}svs" x1="0.38" y1="0" x2="0.62" y2="1">{hl(0, 0.3)}{hl(0.5, 0)}{g(0.5, 0)}{g(1, 0.42)}</linearGradient>')
    d.append(f'<linearGradient id="{u}scyl" x1="0" y1="0" x2="1" y2="0">{g(0, 0.36)}{g(0.2, 0)}{hl(0.2, 0)}{hl(0.34, 0.16)}{hl(0.52, 0)}{g(0.52, 0)}{g(1, 0.4)}</linearGradient>')
    d.append(f'<radialGradient id="{u}srad" cx="0.36" cy="0.3" r="0.82">{hl(0, 0.24, "#ffffff")}{hl(0.45, 0, "#ffffff")}{g(0.6, 0)}{g(1, 0.32)}</radialGradient>')
    d.append(f'<linearGradient id="{u}wocc" gradientUnits="userSpaceOnUse" x1="0" y1="{n(Y_PRAIL0)}" x2="0" y2="{n(Y_PRAIL0 + 0.5)}">{g(0, 0.34)}{g(0.35, 0.14)}{g(1, 0)}</linearGradient>')
    d.append(f'<linearGradient id="{u}wocb" gradientUnits="userSpaceOnUse" x1="0" y1="{n(Y_CHAIR1)}" x2="0" y2="{n(Y_CHAIR1 - 0.3)}">{g(0, 0.26)}{g(1, 0)}</linearGradient>')
    d.append(f'<radialGradient id="{u}mott">{hl(0, 0.2, "#7f9df0")}{hl(1, 0, "#7f9df0")}</radialGradient>')
    d.append(f'<radialGradient id="{u}motd">{g(0, 0.26)}{g(1, 0)}</radialGradient>')
    d.append(f'<radialGradient id="{u}motw">{hl(0, 0.16, "#ffd9b0")}{hl(1, 0, "#ffd9b0")}</radialGradient>')
    d.append(f'<linearGradient id="{u}ftop" gradientUnits="userSpaceOnUse" x1="0" y1="{n(-3.9)}" x2="0" y2="{n(-8.2)}">{g(0, 0)}{g(0.2, 0.15)}{g(0.33, 0.27)}{g(1, 0.33)}</linearGradient>')
    d.append(f'<linearGradient id="{u}fbot" gradientUnits="userSpaceOnUse" x1="0" y1="{n(-0.6)}" x2="0" y2="{n(4.8)}">{g(0, 0)}{g(0.25, 0.04)}{g(0.55, 0.26)}{g(1, 0.6)}</linearGradient>')
    d.append(f'<linearGradient id="{u}fl" gradientUnits="userSpaceOnUse" x1="{n(-2.3)}" y1="0" x2="{n(-4.6)}" y2="0">{g(0, 0)}{g(1, 0.5)}</linearGradient>')
    d.append(f'<linearGradient id="{u}fr" gradientUnits="userSpaceOnUse" x1="{n(2.3)}" y1="0" x2="{n(4.6)}" y2="0">{g(0, 0)}{g(1, 0.5)}</linearGradient>')
    d.append(f'<radialGradient id="{u}pool"><stop offset="0" stop-color="#e46a34" stop-opacity="0.46"/><stop offset="0.6" stop-color="#e46a34" stop-opacity="0.25"/><stop offset="1" stop-color="#e46a34" stop-opacity="0"/></radialGradient>')
    d.append(f'<radialGradient id="{u}rugl"><stop offset="0" stop-color="#5f7dff" stop-opacity="0.22"/><stop offset="1" stop-color="#5f7dff" stop-opacity="0"/></radialGradient>')
    d.append(f'<radialGradient id="{u}cone"><stop offset="0" stop-color="#ffd9a0" stop-opacity="0.3"/><stop offset="1" stop-color="#ffd9a0" stop-opacity="0"/></radialGradient>')
    d.append(f'<radialGradient id="{u}halo"><stop offset="0" stop-color="{BULB}" stop-opacity="1"/><stop offset="0.44" stop-color="#fff1c4" stop-opacity="0.95"/><stop offset="0.54" stop-color="#ffd27a" stop-opacity="0.55"/><stop offset="0.74" stop-color="#f0a04f" stop-opacity="0.2"/><stop offset="1" stop-color="#e08a3c" stop-opacity="0"/></radialGradient>')
    d.append(f'<radialGradient id="{u}glow"><stop offset="0" stop-color="#ffe2a8" stop-opacity="0.5"/><stop offset="1" stop-color="#ffe2a8" stop-opacity="0"/></radialGradient>')
    d.append(f'<linearGradient id="{u}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f7fa6"/><stop offset="0.55" stop-color="#a3b0c9"/><stop offset="1" stop-color="#d3d6dc"/></linearGradient>')
    d.append(f'<linearGradient id="{u}shaft" gradientUnits="userSpaceOnUse" x1="{n(-2.9)}" y1="{n(-3.6)}" x2="{n(-0.6)}" y2="{n(0.9)}"><stop offset="0" stop-color="#dfe6ff" stop-opacity="0.2"/><stop offset="0.5" stop-color="#ffe9c0" stop-opacity="0.1"/><stop offset="1" stop-color="#ffe2a8" stop-opacity="0"/></linearGradient>')
    d.append(f'<linearGradient id="{u}fgsh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1025" stop-opacity="0"/><stop offset="1" stop-color="#1a1025" stop-opacity="0.55"/></linearGradient>')
    return ''.join(d)

def vp(x, y, t): return (VPX + (x - VPX) * t, VPY + (y - VPY) * t)      # scale a point about the vanishing point

def shell_svg(u):
    """Ceiling, beams, side walls, back wall with paper / frieze / rails / wainscot."""
    r = random.Random(3); o = []; tmax = (WORLD[1] - VPY) / (WALL_TOP - VPY) + 0.05
    # ceiling boards fan out from the vanishing point
    o.append(poly([(WALL_X0, WALL_TOP), (WALL_X1, WALL_TOP), vp(WALL_X1, WALL_TOP, tmax), vp(WALL_X0, WALL_TOP, tmax)], CEIL, stroke=None, sw=0))
    xs = [WALL_X0 + i * 0.37 for i in range(21)]
    for a, b in zip(xs[:-1], xs[1:]):
        o.append(poly([(a, WALL_TOP), (b, WALL_TOP), vp(b, WALL_TOP, tmax), vp(a, WALL_TOP, tmax)], mul(CEIL, r.uniform(0.86, 1.12)), stroke=None, sw=0))
    for a in xs: o.append(poly([(a - 0.008, WALL_TOP), (a + 0.008, WALL_TOP), vp(a + 0.014, WALL_TOP, tmax), vp(a - 0.014, WALL_TOP, tmax)], mul(CEIL, 0.5), stroke=None, sw=0))
    for t in (1.2, 1.5, 1.95):                                             # cross beams: dark face, lit underside strip
        a = vp(WALL_X0 - 1, WALL_TOP, t); b = vp(WALL_X1 + 1, WALL_TOP, t); h = 0.2 * t
        o.append(rect(a[0], a[1], b[0] - a[0], h, BEAM, sw=W_OBJ * t * 0.8)); o.append(rect(a[0], a[1] + h * 0.72, b[0] - a[0], h * 0.28, '#7c4a36', sw=W_DET * t))
        o.append(line(a[0], a[1] + h * 0.3, b[0], a[1] + h * 0.3, mul(BEAM, 1.9), W_DET * t))
    pa, pb = vp(-2.75, WALL_TOP - 0.06, 1.0), vp(-2.75, WALL_TOP - 0.06, tmax)
    o.append(line(pa[0], pa[1], pb[0], pb[1], INK, 0.11)); o.append(line(pa[0], pa[1], pb[0], pb[1], '#7a6a72', 0.075)); o.append(line(pa[0] - 0.012, pa[1], pb[0] - 0.03, pb[1], '#b3a3a8', W_DET * 1.5))
    for tt in (1.12, 1.4, 1.78): q = vp(-2.75, WALL_TOP - 0.06, tt); o.append(rect(q[0] - 0.07 * tt, q[1] - 0.05 * tt, 0.14 * tt, 0.1 * tt, BRASS, sw=W_DET * 1.3 * tt))
    # side walls (in shade), with wainscot and rails converging
    for sg, X in ((-1, WALL_X0), (1, WALL_X1)):
        t = abs(WORLD[0]) / abs(X) + 0.3; q = lambda y: [(X, y), vp(X, y, t)]
        o.append(poly(q(WALL_TOP) + q(WALL_BASE)[::-1], mul(WALL, 0.74), sw=W_OBJ))
        o.append(poly(q(WALL_TOP) + q(Y_PRAIL0)[::-1], mul(FRIEZE, 0.7), sw=W_DET)); o.append(poly(q(Y_PRAIL1) + q(Y_PRAIL0)[::-1], mul(PRAIL, 0.72), sw=W_DET))
        o.append(poly(q(Y_CHAIR1) + q(WALL_BASE)[::-1], mul(WOOD, 0.8), sw=W_DET)); o.append(poly(q(Y_CHAIR1) + q(Y_CHAIR0)[::-1], mul(RAILC, 0.85), sw=W_DET))
        o.append(poly(q(Y_BASEB) + q(WALL_BASE)[::-1], mul(BASEC, 0.85), sw=W_DET))
        for k in range(1, 8):
            tt = 1 + k * 0.09; a = vp(X, Y_PRAIL0, tt); b = vp(X, Y_CHAIR1, tt); o.append(line(a[0], a[1], b[0], b[1], mul(WALL, 0.55), W_DET))
    # back wall
    wx, ww = WALL_X0, WALL_X1 - WALL_X0
    o.append(rect(wx, WALL_TOP, ww, WALL_BASE - WALL_TOP, f'url(#{u}wp)', sw=W_OBJ))
    o.append(rect(wx, Y_PRAIL0, ww, 0.5, f'url(#{u}wocc)', stroke=None, sw=0)); o.append(rect(wx, Y_CHAIR1 - 0.3, ww, 0.3, f'url(#{u}wocb)', stroke=None, sw=0))
    o.append(rect(wx, WALL_TOP, ww, Y_PRAIL1 - WALL_TOP, f'url(#{u}fz)', sw=W_DET))
    o.append(rect(wx, WALL_TOP - 0.08, ww, 0.1, '#6b3a26', sw=W_OBJ)); o.append(line(wx, WALL_TOP - 0.04, wx + ww, WALL_TOP - 0.04, '#a9623f', W_DET))
    o.append(rect(wx, Y_PRAIL1, ww, Y_PRAIL0 - Y_PRAIL1, PRAIL, sw=W_OBJ * 0.8)); o.append(line(wx, Y_PRAIL1 + 0.03, wx + ww, Y_PRAIL1 + 0.03, det(PRAIL), W_DET * 0.8))
    o.append(rect(wx, Y_CHAIR1, ww, WALL_BASE - Y_CHAIR1, WOOD, sw=W_OBJ))
    pw = 0.74; k = int(ww / pw)
    for i in range(k):
        x = wx + i * pw + 0.07; y = Y_CHAIR0 + 0.07; w_ = pw - 0.14; h_ = Y_BASEB - 0.06 - y
        o.append(rect(x, y, w_, h_, PANEL, stroke=mul(WOOD, 0.5), sw=W_DET * 1.3))
        o.append(rect(x + 0.05, y + 0.05, w_ - 0.1, h_ - 0.1, mul(PANEL, 1.1), stroke=mul(WOOD, 0.55), sw=W_DET))
        o.append(rect(x + 0.05, y + 0.05, w_ - 0.1, h_ - 0.1, f'url(#{u}svs)', stroke=None, sw=0))
        o.append(pline([(x + 0.012, y + h_ - 0.012), (x + 0.012, y + 0.012), (x + w_ - 0.012, y + 0.012)], mul(PANEL, 1.75), W_DET))
        o.append(pline([(x + 0.062, y + h_ - 0.062), (x + w_ - 0.062, y + h_ - 0.062), (x + w_ - 0.062, y + 0.062)], mul(PANEL, 1.6), W_DET * 0.8))
    o.append(rect(wx, Y_CHAIR1, ww, Y_CHAIR0 - Y_CHAIR1, RAILC, sw=W_OBJ * 0.8)); o.append(line(wx, Y_CHAIR1 + 0.028, wx + ww, Y_CHAIR1 + 0.028, mul(RAILC, 1.5), W_DET))
    o.append(rect(wx, Y_BASEB, ww, WALL_BASE - Y_BASEB, BASEC, sw=W_OBJ)); o.append(line(wx, Y_BASEB + 0.035, wx + ww, Y_BASEB + 0.035, mul(BASEC, 1.9), W_DET))
    return ''.join(o)

def floor_svg(u):
    """Plank floor running to the back wall + the navy rug (the one cool block), all in one-point perspective."""
    r = random.Random(8); o = []; Zw, Zb = zy(WALL_BASE), zy(WORLD[3] + 0.4); N = 24
    o.append(poly([fp(-N * 0.28, Zw), fp(N * 0.28, Zw), fp(N * 0.28, Zb), fp(-N * 0.28, Zb)], FLOOR, stroke=None, sw=0))
    for i in range(-N, N):
        c = mul(FLOOR, r.uniform(0.82, 1.1)); a, b = i * 0.28, (i + 1) * 0.28
        if abs(a) > 1.9 or r.random() < 1:   # planks under the rug are hidden, still cheap
            o.append(poly([fp(a, Zw), fp(b, Zw), fp(b, Zb), fp(a, Zb)], c, stroke=None, sw=0))
            for _ in range(5):                                           # grain streaks
                gx = a + r.uniform(0.05, 0.23); z = r.uniform(Zw, Zb - 0.5); l = r.uniform(0.3, 1.0); p, q = fp(gx, z), fp(gx + r.uniform(-0.02, 0.02), z + l)
                o.append(line(p[0], p[1], q[0], q[1], mul(c, r.choice((0.84, 0.88, 1.1))), W_DET * fs(z)))
            for _ in range(r.choice((1, 2, 2))):                         # butt joints
                z = r.uniform(Zw + 0.05, Zb); p, q = fp(a, z), fp(b, z); o.append(line(p[0], p[1], q[0], q[1], SEAM, 0.014 * fs(z)))
                for dz in (-0.06, 0.06):
                    for dx in (0.07, 0.21): k_ = fp(a + dx, z + dz); o.append(circ(k_[0], k_[1], 0.011 * fs(z), mul(SEAM, 0.9), stroke=None, sw=0))
            if r.random() < 0.45:                                        # a knot
                z = r.uniform(Zw, Zb - 0.3); k_ = fp(a + r.uniform(0.08, 0.2), z); o.append(ell(k_[0], k_[1], 0.035 * fs(z), 0.018 * fs(z), mul(c, 0.72), stroke=mul(c, 0.55), sw=W_DET * 0.8 * fs(z)))
    for i in range(-N, N + 1):
        a = i * 0.28; o.append(poly([fp(a - 0.011, Zw), fp(a + 0.011, Zw), fp(a + 0.011, Zb), fp(a - 0.011, Zb)], SEAM, stroke=None, sw=0))
    o.append(line(WORLD[0] - 1, WALL_BASE, WORLD[2] + 1, WALL_BASE, INK, W_OBJ))
    # rug
    RX, Z0r, Z1r = 1.2, -0.92, Zb
    def quad(xa, xb, za, zb, fill, stroke=None, sw=0): return poly([fp(xa, za), fp(xb, za), fp(xb, zb), fp(xa, zb)], fill, stroke=stroke, sw=sw)
    for k in range(41):                                                  # fringe at the far end
        x = -RX + k * 2 * RX / 40; p, q = fp(x, Z0r), fp(x + r.uniform(-0.01, 0.01), Z0r - 0.08); o.append(line(p[0], p[1], q[0], q[1], '#d9c9a8', W_DET))
    o.append(quad(-RX, RX, Z0r, Z1r, RUGRED, stroke=INK, sw=W_OBJ))
    o.append(quad(-RX + 0.07, RX - 0.07, Z0r + 0.07, Z1r, 'none', stroke=GOLD, sw=W_DET * 1.3))
    o.append(quad(-RX + 0.3, RX - 0.3, Z0r + 0.3, Z1r, GOLD, stroke=None)); o.append(quad(-RX + 0.34, RX - 0.34, Z0r + 0.34, Z1r, NAVY, stroke=mul(NAVY, 0.55), sw=W_DET))
    def diamond(X, Z, a, b, fill, stroke, sw=W_DET):
        return poly([fp(X, Z - b), fp(X + a, Z), fp(X, Z + b), fp(X - a, Z)], fill, stroke=stroke, sw=sw * fs(Z))
    for sx in (-1, 1):                                                   # border lozenges down both sides + corner squares
        z = Z0r + 0.185
        while z < Z1r:
            o.append(diamond(sx * (RX - 0.185), z, 0.075, 0.12, NAVY, GOLD)); o.append(diamond(sx * (RX - 0.185), z + 0.2, 0.026, 0.04, GOLD, None)); z += 0.4
    x = -RX + 0.4
    while x < RX - 0.3:
        o.append(diamond(x, Z0r + 0.185, 0.12, 0.075, NAVY, GOLD)); o.append(diamond(x + 0.2, Z0r + 0.185, 0.04, 0.026, GOLD, None)); x += 0.4
    # field: dot lattice, inner gold line, medallions on the centre line
    o.append(quad(-RX + 0.44, RX - 0.44, Z0r + 0.44, Z1r, 'none', stroke=mix(NAVY, GOLD, 0.55), sw=W_DET))
    zi = 0
    z = Z0r + 0.8
    while z < Z1r:
        for k in range(-3, 4):
            X = k * 0.3 + (0.15 if zi % 2 else 0)
            if abs(X) < RX - 0.5: p = fp(X, z); o.append(ell(p[0], p[1], 0.022 * fs(z), 0.012 * fs(z), '#d9c9a8' if (k + zi) % 3 else GOLD, stroke=None, sw=0))
        z += 0.26; zi += 1
    for Zc, s in ((-0.25, 0.42), (0.95, 0.55), (2.1, 0.62), (3.1, 0.55), (3.9, 0.5)):
        o.append(diamond(0, Zc, 0.95 * s, 0.62 * s, RUGRED, GOLD, W_DET * 1.5)); o.append(diamond(0, Zc, 0.7 * s, 0.45 * s, NAVY, mix(NAVY, GOLD, 0.6)))
        o.append(diamond(0, Zc, 0.32 * s, 0.2 * s, GOLD, mul(GOLD, 0.6))); o.append(diamond(0, Zc, 0.13 * s, 0.085 * s, RUGRED, None))
        for sx in (-1, 1): o.append(diamond(sx * 1.18 * s, Zc, 0.1 * s, 0.065 * s, GOLD, None))
    rm = random.Random(44)
    for k in range(26):                                                  # soft lighter / darker patches lying on the floor plane
        X = rm.uniform(-3.4, 3.4); Z = rm.uniform(-0.8, 4.2); a = rm.uniform(0.5, 1.1); c = fp(X, Z); onrug = abs(X) < RX - 0.2 and Z > Z0r + 0.2
        gid = rm.choice(('mott', 'motd', 'mott')) if onrug else rm.choice(('motw', 'motd'))
        o.append(ell(c[0], c[1], a * fs(Z), a * 0.42 * fs(Z), f'url(#{u}{gid})', stroke=None, sw=0))
    return ''.join(o)

def light_warm_svg(u):
    """Warm light pooled on the middle band of the wall, under the pendants, on the ceiling and on the rug (screen)."""
    sc = 'style="mix-blend-mode:screen"'; o = [ell(0, -2.95, 3.6, 2.5, f'url(#{u}pool)', stroke=None, sw=0, extra=sc)]
    for lx, ly, lr in LAMPS[:2]: o.append(ell(lx, ly + 0.45, 1.2, 1.3, f'url(#{u}cone)', stroke=None, sw=0, extra=sc))
    o.append(ell(0, WALL_TOP - 0.45, 4.4, 0.95, f'url(#{u}cone)', stroke=None, sw=0, extra=sc + ' opacity="0.3"'))
    o.append(ell(LAMPS[2][0], LAMPS[2][1] - 0.2, 2.8, 1.2, f'url(#{u}cone)', stroke=None, sw=0, extra=sc + ' opacity="0.6"'))
    o.append(ell(0.3, 0.5, 3.0, 1.4, f'url(#{u}rugl)', stroke=None, sw=0, extra=sc))
    return ''.join(o)

def falloff_svg(u):
    """Plum fall-off toward ceiling, side walls and the camera end of the floor (multiply; world-anchored, never a frame vignette)."""
    x0, y0, x1, y1 = WORLD; W_, H_ = x1 - x0 + 2, y1 - y0 + 2
    return ''.join(rect(x0 - 1, y0 - 1, W_, H_, f'url(#{u}{gid})', stroke=None, sw=0, extra='style="mix-blend-mode:multiply"') for gid in ('ftop', 'fbot', 'fl', 'fr'))

# ----------------------------------------------------------------------------- wall props (bg layer)
def fit(w): return f'textLength="{n(w)}" lengthAdjust="spacingAndGlyphs"'

def sign_svg():
    x, y, w, h = -1.5, -4.34, 3.0, 0.44; o = []
    for sx in (x + 0.3, x + w - 0.3):                                     # chains up to the picture rail
        o.append(line(sx, y, sx, Y_PRAIL0, INK, W_DET * 1.6)); o.append(line(sx, y, sx, Y_PRAIL0, BRASS, W_DET * 0.7, f'stroke-dasharray="{n(0.02)} {n(0.02)}"')); o.append(circ(sx, Y_PRAIL0 + 0.015, 0.022, BRASS, sw=W_DET))
    o.append(rect(x, y, w, h, '#3d1c12', sw=W_OBJ * 1.25)); o.append(rect(x + 0.035, y + 0.035, w - 0.07, h - 0.07, '#1c403d', stroke=GOLD, sw=W_DET * 1.6))
    if SHADE[0]: o.append(rect(x + 0.035, y + 0.035, w - 0.07, h - 0.07, f'url(#{SHADE[0]}s)', stroke=None, sw=0))
    o.append(rect(x + 0.07, y + 0.07, w - 0.14, h - 0.14, 'none', stroke=mul('#1c403d', 1.9), sw=W_DET * 0.8))
    o.append(text(0, y + 0.292, 'U.S. WEATHER BUREAU', 0.19, '#e9d9b0', extra=fit(2.42)))
    for sx in (x + 0.17, x + w - 0.17): o.append(poly([(sx, y + 0.16), (sx + 0.045, y + 0.22), (sx, y + 0.28), (sx - 0.045, y + 0.22)], GOLD, sw=W_DET))
    return ''.join(o)

def clock_svg(cx, cy, r, t):
    o = []; t = float(t)
    # drop case with pendulum
    o.append(path(pd('M', cx - r * 0.42, cy + r * 0.7, 'L', cx - r * 0.42, cy + r * 1.75, 'L', cx, cy + r * 2.02, 'L', cx + r * 0.42, cy + r * 1.75, 'L', cx + r * 0.42, cy + r * 0.7, 'Z'), '#4a2216'))
    o.append(rect(cx - r * 0.28, cy + r * 1.05, r * 0.56, r * 0.62, '#2a1410', stroke=mul('#4a2216', 1.8), sw=W_DET))
    a = math.radians(9 * math.sin(2 * math.pi * t / 1.6)); px, py = cx + r * 0.55 * math.sin(a), cy + r * 1.0 + r * 0.55 * math.cos(a)
    o.append(line(cx, cy + r * 1.0, px, py, BRASS, W_DET)); o.append(circ(px, py, r * 0.1, BRASS, sw=W_DET))
    o.append(circ(cx, cy, r, '#4a2216', sw=W_OBJ * 1.25)); o.append(circ(cx, cy, r * 0.86, BRASS, sw=W_DET * 1.3)); o.append(circ(cx, cy, r * 0.78, '#f3e7c9', sw=W_DET * 1.3))
    if SHADE[0]: o.append(circ(cx, cy, r * 0.78, f'url(#{SHADE[0][:-2]}srad)', stroke=None, sw=0))
    for k in range(60):
        a = math.radians(k * 6); r0 = r * (0.62 if k % 5 == 0 else 0.7)
        if k % 5 == 0 or r > 0.3: o.append(line(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + r * 0.74 * math.sin(a), cy - r * 0.74 * math.cos(a), PRINT_D if k % 5 else INK, W_DET * (1.5 if k % 5 == 0 else 0.6)))
    hh, mm = 9, 41 + t / 60.0
    for ang, L, w_ in (((hh % 12 + mm / 60) * 30, 0.42, 2.4), (mm * 6, 0.64, 1.7)):
        a = math.radians(ang); o.append(line(cx - r * 0.08 * math.sin(a), cy + r * 0.08 * math.cos(a), cx + r * L * math.sin(a), cy - r * L * math.cos(a), INK, W_DET * w_))
    a = math.radians(math.floor(t) * 6 + 150); o.append(line(cx - r * 0.16 * math.sin(a), cy + r * 0.16 * math.cos(a), cx + r * 0.68 * math.sin(a), cy - r * 0.68 * math.cos(a), '#b61d32', W_DET))
    o.append(circ(cx, cy, r * 0.05, BRASS, sw=W_DET)); o.append(path(pd('M', cx - r * 0.55, cy - r * 0.45, 'A', r * 0.7, r * 0.7, 0, 0, 1, cx - r * 0.1, cy - r * 0.7), 'none', stroke='#ffffff', sw=W_DET * 1.5, extra='opacity="0.5"'))
    return ''.join(o)

def calendar_svg(x, y, w, h):
    o = [line(x + w / 2, y - 0.07, x + w / 2, y, INK, W_DET), circ(x + w / 2, y - 0.07, 0.016, BRASS, sw=W_DET)]
    o.append(rect(x + 0.02, y + 0.04, w, h, mul('#f6efe2', 0.8), sw=W_DET))                       # pages behind
    o.append(rect(x, y, w, h, '#f6efe2')); hh = h * 0.27
    o.append(rect(x, y, w, hh, '#b61d32')); o.append(rect(x + 0.025, y + 0.025, w - 0.05, hh - 0.05, 'none', stroke='#f3d9a8', sw=W_DET * 0.7))
    o.append(text(x + w / 2, y + hh * 0.68, 'SEPTEMBER', 0.082, '#f3d9a8', extra=fit(w - 0.11)))
    o.append(text(x + w / 2, y + h * 0.80, '20', 0.4, '#b61d32', extra=fit(w * 0.7)))
    o.append(line(x + 0.06, y + h * 0.87, x + w - 0.06, y + h * 0.87, '#9a8f86', W_DET * 0.8)); o.append(greek(x + 0.1, y + h * 0.93, w - 0.2, '#9a8f86', W_DET, random.Random(2), gap=0.6))
    o.append(greek(x + 0.12, y + hh + 0.05, w - 0.24, '#9a8f86', W_DET, random.Random(3), gap=0.6))
    for sx in (x + w * 0.3, x + w * 0.7): o.append(circ(sx, y + 0.012, 0.014, '#3a2620', sw=W_DET * 0.7))
    o.append(poly([(x + w, y + h - 0.09), (x + w, y + h), (x + w - 0.09, y + h)], mul('#f6efe2', 0.86), sw=W_DET))
    return ''.join(o)

def pinboard_svg(x, y, w, h):
    r = random.Random(21); CORK = '#8f6b3c'; o = [rect(x, y, w, h, '#4a2216'), rect(x + 0.05, y + 0.05, w - 0.1, h - 0.1, CORK, sw=W_DET * 1.3)]
    for _ in range(40):
        px, py = x + 0.07 + r.random() * (w - 0.14), y + 0.07 + r.random() * (h - 0.14); o.append(line(px, py, px + 0.02, py + 0.006, mul(CORK, r.choice((0.72, 1.25))), W_DET * 0.9))
    sheets = ((0.09, 0.1, 0.34, 0.26, -5, '#f1dfa0'), (0.47, 0.09, 0.32, 0.4, 3, '#f6efe2'), (0.1, 0.41, 0.3, 0.36, 4, '#f6efe2'), (0.44, 0.54, 0.36, 0.24, -3, '#f1dfa0'), (0.16, 0.8, 0.5, 0.17, 2, '#e9d3c0'))
    for sx, sy, sw_, sh_, a, col in sheets:
        X, Y, Wd, Ht = x + sx * w, y + sy * h, sw_ * w, sh_ * h; b = [rect(X, Y, Wd, Ht, col, sw=W_DET * 1.3)]
        b.append(line(X + 0.03, Y + 0.045, X + Wd - 0.03, Y + 0.045, PRINT_D, W_DET * 1.8))
        for j in range(int((Ht - 0.08) / 0.042)): b.append(greek(X + 0.03, Y + 0.09 + j * 0.042, Wd - 0.06 - r.uniform(0, 0.08), PRINT, W_DET * 0.9, r))
        b.append(circ(X + Wd / 2, Y + 0.018, 0.017, r.choice(('#b61d32', '#2f5a8a', BRASS)), sw=W_DET * 0.8)); o.append(rot(b, a, X + Wd / 2, Y + Ht / 2))
    return ''.join(o)

def barometer_svg(cx, y):
    o = []; W1 = '#6d3a1f'; dy = y + 0.86; R = 0.2
    o.append(path(pd('M', cx, y, 'C', cx + 0.1, y, cx + 0.1, y + 0.08, cx + 0.085, y + 0.14, 'L', cx + 0.07, y + 0.55, 'C', cx + 0.2, y + 0.6, cx + R + 0.05, y + 0.72, cx + R + 0.05, dy,
                 'A', R + 0.05, R + 0.05, 0, 1, 1, cx - R - 0.05, dy, 'C', cx - R - 0.05, y + 0.72, cx - 0.2, y + 0.6, cx - 0.07, y + 0.55, 'L', cx - 0.085, y + 0.14, 'C', cx - 0.1, y + 0.08, cx - 0.1, y, cx, y, 'Z'), W1))
    o.append(path(pd('M', cx - 0.055, y + 0.12, 'L', cx - 0.045, y + 0.52), 'none', stroke=mul(W1, 1.6), sw=W_DET))
    o.append(rect(cx - 0.035, y + 0.1, 0.07, 0.4, '#f3e7c9', sw=W_DET * 1.2)); o.append(line(cx, y + 0.46, cx, y + 0.22, '#c2311e', W_DET * 1.8)); o.append(circ(cx, y + 0.47, 0.018, '#c2311e', sw=W_DET * 0.7))
    for j in range(7): o.append(line(cx + 0.012, y + 0.15 + j * 0.045, cx + 0.03, y + 0.15 + j * 0.045, PRINT_D, W_DET * 0.7))
    o.append(circ(cx, dy, R, BRASS, sw=W_DET * 1.4)); o.append(circ(cx, dy, R * 0.86, '#f3e7c9', sw=W_DET * 1.2))
    if SHADE[0]: o.append(circ(cx, dy, R * 0.86, f'url(#{SHADE[0][:-2]}srad)', stroke=None, sw=0))
    for a in range(-135, 136, 15):
        ra = math.radians(a); o.append(line(cx + R * 0.66 * math.sin(ra), dy - R * 0.66 * math.cos(ra), cx + R * 0.8 * math.sin(ra), dy - R * 0.8 * math.cos(ra), PRINT_D if a % 45 else INK, W_DET * (0.7 if a % 45 else 1.3)))
    o.append(greek(cx - 0.07, dy + 0.07, 0.14, PRINT, W_DET * 0.9, random.Random(1)))
    ra = math.radians(-58); o.append(line(cx, dy, cx + R * 0.62 * math.sin(ra), dy - R * 0.62 * math.cos(ra), INK, W_DET * 1.6))
    ra = math.radians(-20); o.append(line(cx, dy, cx + R * 0.56 * math.sin(ra), dy - R * 0.56 * math.cos(ra), BRASS, W_DET * 1.2)); o.append(circ(cx, dy, 0.02, BRASS, sw=W_DET))
    return ''.join(o)

def certificate_svg(x, y, w, h):
    r = random.Random(6); o = [rect(x, y, w, h, '#3d1c12'), rect(x + 0.04, y + 0.04, w - 0.08, h - 0.08, PAPER, stroke=GOLD, sw=W_DET * 1.3)]
    o.append(line(x + 0.09, y + 0.12, x + w - 0.09, y + 0.12, PRINT_D, W_DET * 2.2))
    for j in range(5): o.append(greek(x + 0.08, y + 0.18 + j * 0.045, w - 0.16 - (0.08 if j == 4 else 0), PRINT, W_DET * 0.9, r))
    o.append(circ(x + w - 0.13, y + h - 0.12, 0.04, '#b61d32', sw=W_DET)); o.append(line(x + 0.08, y + h - 0.1, x + 0.22, y + h - 0.1, PRINT_D, W_DET))
    return ''.join(o)

def window_svg(u, t):
    x, y, w, h = -3.42, -4.1, 1.17, 2.5; FRM = '#6f3522'; o = []; r = random.Random(12)
    o.append(rect(x - 0.08, y - 0.08, w + 0.16, h + 0.16, FRM)); o.append(rect(x - 0.03, y - 0.03, w + 0.06, h + 0.06, mul(FRM, 0.7), sw=W_DET))
    o.append(rect(x, y, w, h, f'url(#{u}sky)', sw=W_DET * 1.5))
    # grey September sky: flat cloud bands + rooftops with a water tank and a weather vane
    for cy_, cw, ch in ((y + 0.5, 0.9, 0.16), (y + 0.95, 0.7, 0.12), (y + 1.35, 1.0, 0.14)):
        o.append(ell(x + w * 0.5 + r.uniform(-0.2, 0.2), cy_, cw * 0.6, ch, '#8e98b3', stroke=None, sw=0, extra='opacity="0.55"'))
    sk = [(x, y + h), (x, y + h - 0.5), (x + 0.2, y + h - 0.5), (x + 0.2, y + h - 0.72), (x + 0.42, y + h - 0.72), (x + 0.42, y + h - 0.4), (x + 0.62, y + h - 0.4), (x + 0.62, y + h - 0.6),
          (x + 0.7, y + h - 0.68), (x + 0.86, y + h - 0.68), (x + 0.94, y + h - 0.6), (x + 0.94, y + h - 0.32), (x + w, y + h - 0.32), (x + w, y + h)]
    o.append(poly(sk, '#6a6f8f', stroke='#4a4b68', sw=W_DET))
    for wx_, wy_ in ((0.05, 0.4), (0.12, 0.4), (0.25, 0.6), (0.33, 0.6), (0.25, 0.45), (0.5, 0.3), (0.7, 0.5), (0.8, 0.5), (0.7, 0.36), (1.0, 0.22)):
        o.append(rect(x + wx_, y + h - wy_, 0.04, 0.06, '#f3d08a' if (wx_ * 100) % 3 < 1 else '#55597a', stroke=None, sw=0))
    o.append(line(x + 0.31, y + h - 0.72, x + 0.31, y + h - 0.95, '#4a4b68', W_DET * 1.3)); o.append(line(x + 0.25, y + h - 0.9, x + 0.37, y + h - 0.9, '#4a4b68', W_DET * 1.3))
    o.append(line(x + w / 2, y, x + w / 2, y + h, FRM, 0.05)); o.append(line(x, y + h * 0.55, x + w, y + h * 0.55, FRM, 0.06))
    o.append(line(x + w / 2 - 0.025, y, x + w / 2 - 0.025, y + h, INK, W_DET)); o.append(line(x + w / 2 + 0.025, y, x + w / 2 + 0.025, y + h, INK, W_DET))
    o.append(line(x, y + h * 0.55 - 0.03, x + w, y + h * 0.55 - 0.03, INK, W_DET)); o.append(line(x, y + h * 0.55 + 0.03, x + w, y + h * 0.55 + 0.03, INK, W_DET))
    # venetian blind: head rail + slats over the upper sash, cords
    SL = '#e3d2a6'; nb = 15; bh = h * 0.5
    o.append(rect(x - 0.01, y - 0.01, w + 0.02, 0.09, '#c9b88c', sw=W_DET * 1.3))
    for j in range(nb):
        yy = y + 0.09 + j * (bh - 0.09) / nb; o.append(rect(x + 0.01, yy, w - 0.02, (bh - 0.09) / nb * 0.62, SL if j % 2 else mul(SL, 0.93), stroke=det(SL, 0.6), sw=W_DET * 0.9))
    o.append(rect(x, y + bh, w, 0.05, '#c9b88c', sw=W_DET * 1.2))
    for cx_ in (x + 0.2, x + w - 0.2): o.append(line(cx_, y + 0.05, cx_, y + bh, det(SL, 0.55), W_DET))
    o.append(line(x + w - 0.07, y + 0.08, x + w - 0.07, y + h * 0.78, '#d9c9a8', W_DET * 1.2)); o.append(circ(x + w - 0.07, y + h * 0.78, 0.022, '#d9c9a8', sw=W_DET * 0.8))
    o.append(rect(x - 0.14, y + h + 0.06, w + 0.28, 0.09, mul(FRM, 1.3))); o.append(line(x - 0.12, y + h + 0.085, x + w + 0.12, y + h + 0.085, mul(FRM, 1.9), W_DET))
    return ''.join(o)

def pendant_svg(x, y, rb, top):
    """Green enamel shade with a glowing bulb (bulb centre x, y; radius rb), cord up to `top`."""
    s = rb / 0.20; sw_ = 0.45 * s; o = [line(x, top, x, y - 0.45 * s, INK, W_DET * 1.6 * s)]
    o.append(rect(x - 0.035 * s, y - 0.5 * s, 0.07 * s, 0.1 * s, BRASS, sw=W_DET * 1.2 * s))
    o.append(path(pd('M', x - sw_, y - 0.06 * s, 'C', x - sw_ * 0.9, y - 0.3 * s, x - 0.12 * s, y - 0.42 * s, x, y - 0.42 * s, 'C', x + 0.12 * s, y - 0.42 * s, x + sw_ * 0.9, y - 0.3 * s, x + sw_, y - 0.06 * s, 'Z'), GREEN_D, sw=W_OBJ * s))
    if SHADE[0]: o.append(tone(o[-1], SHADE[0][:-2] + 'scyl'))
    o.append(path(pd('M', x - sw_ * 0.72, y - 0.14 * s, 'C', x - sw_ * 0.6, y - 0.27 * s, x - 0.14 * s, y - 0.36 * s, x - 0.04 * s, y - 0.37 * s), 'none', stroke=mul(GREEN_D, 1.7), sw=W_DET * 1.4 * s))
    o.append(ell(x, y - 0.06 * s, sw_, 0.06 * s, '#f1ead2', sw=W_OBJ * 0.8 * s)); o.append(circ(x, y, rb, BULB, stroke='#f0c070', sw=W_DET * s))
    return ''.join(o)

def bg_props_svg(u, st):
    t = st.get('t', 0.0); o = [window_svg(u, t), calendar_svg(-2.09, -4.35, 0.5, 0.66), barometer_svg(-1.88, -3.5), sign_svg()]
    o.append(clock_svg(2.03, -4.1, 0.37, t)); o.append(pinboard_svg(2.62, -4.3, 0.95, 1.12)); o.append(fan_svg(2.0, -6.95, 1.0, t))
    # switch plate and conduit, wall thermometer by the map
    o.append(rect(-1.78, -2.12, 0.1, 0.5, '#f3e7c9', sw=W_DET * 1.3, rx=0.02)); o.append(line(-1.73, -1.72, -1.73, -1.95, '#c2311e', W_DET * 1.6)); o.append(circ(-1.73, -1.69, 0.022, '#c2311e', sw=W_DET * 0.7))
    for j in range(6): o.append(line(-1.71, -2.05 + j * 0.055, -1.695, -2.05 + j * 0.055, PRINT_D, W_DET * 0.7))
    return ''.join(o)

def pendants_svg():
    return ''.join(pendant_svg(lx, ly, lr, top) for (lx, ly, lr), top in zip(LAMPS, (WALL_TOP - 0.55, WALL_TOP - 0.55, WORLD[1] - 0.5)))

# ----------------------------------------------------------------------------- mid layer: furniture behind the actors
MID_BASE = -0.355
def contact(x0, x1, y, a=0.3): return ell((x0 + x1) / 2, y, (x1 - x0) / 2 + 0.06, 0.035, '#1a1025', stroke=None, sw=0, extra=f'opacity="{a}"')

def radiator_svg(x0, x1, yt):
    C = '#6f6372'; yb = MID_BASE; o = [contact(x0, x1, yb)]; k = int((x1 - x0) / 0.105); w = (x1 - x0) / k
    o.append(line(x0 - 0.1, yb - 0.1, x0, yb - 0.1, INK, 0.05)); o.append(line(x0 - 0.1, yb - 0.1, x0, yb - 0.1, '#8a6a3e', 0.03)); o.append(circ(x0 - 0.1, yb - 0.16, 0.035, BRASS, sw=W_DET))
    for i in range(k):
        x = x0 + i * w; o.append(rect(x, yt, w, yb - yt, C if i % 2 else mul(C, 1.08), sw=W_DET * 1.4, rx=0.04))
        o.append(line(x + w * 0.3, yt + 0.06, x + w * 0.3, yb - 0.08, mul(C, 1.5), W_DET)); o.append(line(x + w * 0.75, yt + 0.07, x + w * 0.75, yb - 0.07, mul(C, 0.62), W_DET))
    o.append(rect(x0 - 0.01, yt + 0.1, x1 - x0 + 0.02, 0.05, mul(C, 0.8), sw=W_DET)); o.append(rect(x0 - 0.01, yb - 0.17, x1 - x0 + 0.02, 0.05, mul(C, 0.8), sw=W_DET))
    for x in (x0 + 0.03, x1 - 0.09): o.append(rect(x, yb - 0.02, 0.06, 0.05, mul(C, 0.6), sw=W_DET))
    return ''.join(o)

def teletype_svg(x, w, t):
    """Model-15 style printer on a steel stand, paper rising from the platen, tape spilling to the floor."""
    r = random.Random(17); yb = MID_BASE; yt = -1.2; B = '#2d2239'; o = [contact(x, x + w, yb)]
    for lx in (x + 0.07, x + w - 0.07): o.append(rect(lx - 0.03, yt, 0.06, yb - yt, '#3b3442', sw=W_DET * 1.4)); o.append(line(lx - 0.012, yt + 0.03, lx - 0.012, yb - 0.03, '#6d647a', W_DET * 0.8))
    o.append(rect(x + 0.04, -0.68, w - 0.08, 0.06, '#3b3442', sw=W_DET * 1.3)); o.append(line(x + 0.1, -0.62, x + w - 0.1, yb - 0.02, '#3b3442', W_DET * 2)); o.append(line(x + w - 0.1, -0.62, x + 0.1, yb - 0.02, '#3b3442', W_DET * 2))
    o.append(rect(x - 0.02, yt - 0.06, w + 0.04, 0.09, '#4a4254', sw=W_OBJ)); o.append(line(x, yt - 0.04, x + w, yt - 0.04, '#857a94', W_DET))
    # paper sheet from the platen
    px = x + w * 0.2; pw = w * 0.6; o.append(path(pd('M', px, yt - 0.55, 'L', px, yt - 1.02, 'C', px + pw * 0.3, yt - 1.06, px + pw * 0.7, yt - 0.98, px + pw, yt - 1.03, 'L', px + pw, yt - 0.55, 'Z'), '#f6efe2', sw=W_DET * 1.4))
    for j in range(8): o.append(greek(px + 0.035, yt - 0.96 + j * 0.05, pw - 0.07 - r.uniform(0, 0.12), '#9a8f86', W_DET * 0.9, r))
    # body: base, sloped cover with window, platen knobs, keyboard
    o.append(path(pd('M', x + 0.02, yt - 0.06, 'L', x + 0.02, yt - 0.42, 'L', x + 0.1, yt - 0.62, 'L', x + w - 0.1, yt - 0.62, 'L', x + w - 0.02, yt - 0.42, 'L', x + w - 0.02, yt - 0.06, 'Z'), B))
    o.append(rect(x + 0.13, yt - 0.57, w - 0.26, 0.13, '#17141c', sw=W_DET * 1.2)); o.append(line(x + 0.15, yt - 0.555, x + w * 0.5, yt - 0.555, '#8f86a0', W_DET))
    o.append(line(x + 0.04, yt - 0.42, x + w - 0.04, yt - 0.42, '#6d647a', W_DET)); o.append(rect(x + w * 0.36, yt - 0.37, w * 0.28, 0.07, BRASS, sw=W_DET)); o.append(greek(x + w * 0.39, yt - 0.335, w * 0.2, INK, W_DET * 0.8, r))
    for kx in (x + 0.045, x + w - 0.045): o.append(circ(kx, yt - 0.56, 0.035, '#17141c', sw=W_DET * 1.2))
    o.append(circ(x + w - 0.12, yt - 0.33, 0.022, '#e0452c', sw=W_DET)); o.append(circ(x + 0.12, yt - 0.33, 0.02, '#3f8a5c', sw=W_DET))
    o.append(rect(x + 0.05, yt - 0.25, w - 0.1, 0.17, '#1c1921', sw=W_DET * 1.3))
    for row in range(3):
        for k in range(9): o.append(circ(x + 0.1 + (k + 0.25 * row) * (w - 0.24) / 8.5, yt - 0.215 + row * 0.05, 0.017, '#e9d9b0', sw=W_DET * 0.6))
    # tape spilling from the left side into loose loops on the floor
    tp = pd('M', x + 0.03, yt - 0.3, 'C', x - 0.2, yt - 0.3, x - 0.22, yt + 0.1, x - 0.12, yt + 0.35, 'C', x - 0.02, yt + 0.6, x - 0.26, yt + 0.62, x - 0.2, yb - 0.1, 'C', x - 0.16, yb + 0.02, x + 0.02, yb - 0.02, x - 0.04, yb - 0.09)
    o.append(path(tp, 'none', stroke=INK, sw=0.06)); o.append(path(tp, 'none', stroke='#f1e3c0', sw=0.036)); o.append(path(tp, 'none', stroke='#9a8f86', sw=W_DET * 0.7, extra=f'stroke-dasharray="{n(0.012)} {n(0.03)}"'))
    return ''.join(o)

def cabinets_svg(x, w, yt, k=2, u=''):
    yb = MID_BASE; o = [contact(x, x + w, yb)]; cw = w / k; C1, C2 = STEEL, STEEL_HI
    for i in range(k):
        cx = x + i * cw; o.append(rect(cx, yt, cw, yb - yt, C1, sw=W_OBJ * 1.25)); dh = (yb - yt - 0.14) / 4
        for j in range(4):
            y = yt + 0.05 + j * dh; o.append(rect(cx + 0.045, y, cw - 0.09, dh - 0.045, C2, stroke=mul(C1, 0.55), sw=W_DET * 1.3))
            if SHADE[0]: o.append(rect(cx + 0.045, y, cw - 0.09, dh - 0.045, f'url(#{SHADE[0]}s)', stroke=None, sw=0))
            o.append(pline([(cx + 0.06, y + dh - 0.062), (cx + 0.06, y + 0.016), (cx + cw - 0.06, y + 0.016)], mul(C2, 1.45), W_DET))
            o.append(rect(cx + cw * 0.3, y + dh * 0.16, cw * 0.4, dh * 0.24, '#f3e7c9', sw=W_DET)); o.append(greek(cx + cw * 0.34, y + dh * 0.28, cw * 0.3, PRINT_D, W_DET * 0.8, random.Random(i * 7 + j)))
            o.append(rect(cx + cw * 0.33, y + dh * 0.56, cw * 0.34, dh * 0.13, BRASS, sw=W_DET, rx=0.015)); o.append(line(cx + cw * 0.36, y + dh * 0.585, cx + cw * 0.64, y + dh * 0.585, '#fff0b0', W_DET * 0.7))
        o.append(rect(cx, yb - 0.085, cw, 0.085, mul(C1, 0.6), sw=W_DET * 1.3))
    if u: o.append(rect(x, yt + 0.4, w, yb - yt - 0.4, f'url(#{u}fgsh)', stroke=None, sw=0, extra='opacity="0.6"'))
    o.append(rect(x - 0.02, yt - 0.05, w + 0.04, 0.07, mul(C1, 1.3), sw=W_OBJ * 0.9))
    return ''.join(o)

def barograph_svg(x, y, w, t):
    """Recording barometer: drum with a paper chart and a red trace, bellows, pen arm, glass case."""
    h = w * 0.62; o = [rect(x, y - 0.07, w, 0.07, '#5a2b1b', sw=W_OBJ * 0.9), line(x + 0.02, y - 0.05, x + w - 0.02, y - 0.05, mul('#5a2b1b', 1.8), W_DET)]
    dx, dw = x + w * 0.08, w * 0.4; dt, db = y - h + 0.05, y - 0.1
    o.append(rect(dx, dt, dw, db - dt, '#f6efe2', sw=W_DET * 1.3)); o.append(ell(dx + dw / 2, dt, dw / 2, 0.035, BRASS, sw=W_DET * 1.2)); o.append(ell(dx + dw / 2, db, dw / 2, 0.035, BRASS, sw=W_DET * 1.2))
    for j in range(1, 5): o.append(line(dx + 0.005, dt + j * (db - dt) / 5, dx + dw - 0.005, dt + j * (db - dt) / 5, '#b9a98a', W_DET * 0.6))
    for j in range(1, 6): o.append(line(dx + j * dw / 6, dt + 0.03, dx + j * dw / 6, db - 0.03, '#b9a98a', W_DET * 0.6))
    tr = [(dx + 0.01 + k * (dw - 0.04) / 9, dt + (db - dt) * (0.28 + 0.07 * math.sin(k * 0.9) + 0.045 * k * k / 9)) for k in range(10)]
    o.append(pline(tr, '#c2311e', W_DET * 1.4))
    bx = x + w * 0.74
    for j in range(4): o.append(ell(bx, y - 0.11 - j * 0.045, w * 0.13, 0.026, BRASS if j % 2 else mul(BRASS, 0.82), sw=W_DET))
    o.append(line(bx, y - 0.3, bx, y - h * 0.62, INK, W_DET * 1.6)); o.append(line(bx + 0.04, y - h * 0.62, tr[-1][0], tr[-1][1], INK, W_DET * 1.4)); o.append(circ(bx, y - h * 0.62, 0.02, BRASS, sw=W_DET))
    o.append(rect(x + 0.02, y - h, w - 0.04, h - 0.07, '#cfe3e6', stroke=INK, sw=W_OBJ * 0.9, extra='fill-opacity="0.16"'))
    o.append(line(x + 0.02, y - h, x + w - 0.02, y - h, '#6d3a1f', 0.035)); o.append(line(x + 0.07, y - h + 0.09, x + 0.2, y - h + 0.3, '#ffffff', W_DET * 1.6, 'opacity="0.55"'))
    return ''.join(o)

def basket_svg(x, w, h, charts=True):
    yb = MID_BASE; C = '#8a6a3e'; o = [contact(x, x + w, yb, 0.25)]; r = random.Random(int(x * 10) + 40)
    if charts:
        for i, (dx, ang, L) in enumerate(((0.2, -10, 0.82), (0.45, 5, 0.9), (0.62, 14, 0.78), (0.34, -2, 0.86))):
            cx = x + w * dx; b = [rect(cx - 0.045, yb - L, 0.09, L - 0.1, '#f1e3c0' if i % 2 else '#e6d5ae', sw=W_DET * 1.3), ell(cx, yb - L, 0.045, 0.018, '#c9d9d6', sw=W_DET),
                                  line(cx - 0.02, yb - L + 0.05, cx - 0.02, yb - 0.4, '#b9a98a', W_DET * 0.8)]
            if i == 1: b.append(rect(cx - 0.047, yb - L + 0.3, 0.094, 0.05, '#b61d32', sw=W_DET * 0.8))
            o.append(rot(b, ang, cx, yb - 0.1))
    else:
        o.append(path(pd('M', x + w * 0.2, yb - h, 'C', x + w * 0.25, yb - h - 0.1, x + w * 0.45, yb - h - 0.13, x + w * 0.55, yb - h - 0.05, 'C', x + w * 0.7, yb - h - 0.12, x + w * 0.85, yb - h - 0.06, x + w * 0.8, yb - h, 'Z'), '#f6efe2', sw=W_DET * 1.3))
        o.append(line(x + w * 0.4, yb - h - 0.08, x + w * 0.5, yb - h - 0.01, '#9a8f86', W_DET)); o.append(line(x + w * 0.62, yb - h - 0.07, x + w * 0.7, yb - h - 0.02, '#9a8f86', W_DET))
    o.append(poly([(x, yb - h), (x + w, yb - h), (x + w * 0.86, yb), (x + w * 0.14, yb)], C, sw=W_OBJ))
    if SHADE[0]: o.append(tone(o[-1], SHADE[0][:-2] + 'scyl'))
    for j in range(1, 7): o.append(line(x + w * j / 7, yb - h + 0.02, x + w * (0.14 + 0.72 * j / 7), yb - 0.02, det(C, 0.6), W_DET))
    for j in range(1, 4): o.append(line(x + w * 0.035 * j + 0.01, yb - h + h * j / 4, x + w - w * 0.035 * j - 0.01, yb - h + h * j / 4, det(C, 0.6), W_DET))
    o.append(rect(x - 0.015, yb - h - 0.03, w + 0.03, 0.05, mul(C, 1.3), sw=W_DET * 1.3, rx=0.02))
    return ''.join(o)

def fan_svg(x, y, R, t):
    """Slow ceiling fan seen from below (blades projected to a flat ellipse)."""
    o = [line(x, y - 2.2, x, y - 0.1, INK, 0.07), line(x, y - 2.2, x, y - 0.1, '#6d5a4a', 0.04)]; th0 = 0.5 + 0.9 * float(t); B = '#4a2a1c'
    for k in sorted(range(4), key=lambda k: math.sin(th0 + k * math.pi / 2)):
        th = th0 + k * math.pi / 2; c, s_ = math.cos(th), math.sin(th) * 0.26; pc, ps = -math.sin(th), math.cos(th) * 0.26
        P = lambda r, w: (x + r * c + w * pc, y + r * s_ + w * ps)
        o.append(poly([P(0.12 * R, 0.05 * R), P(0.5 * R, 0.13 * R), P(R, 0.12 * R), P(1.04 * R, 0), P(R, -0.12 * R), P(0.5 * R, -0.13 * R), P(0.12 * R, -0.05 * R)], B if math.sin(th) < 0 else mul(B, 1.45), sw=W_OBJ * 1.3))
        a, b = P(0.2 * R, 0), P(0.95 * R, 0); o.append(line(a[0], a[1], b[0], b[1], mul(B, 2.0), W_DET * 1.2))
    o.append(ell(x, y, 0.17 * R, 0.085 * R, BRASS, sw=W_OBJ * 1.2)); o.append(rect(x - 0.09 * R, y - 0.2 * R, 0.18 * R, 0.16 * R, mul(BRASS, 0.8), sw=W_OBJ)); o.append(ell(x - 0.04 * R, y - 0.01 * R, 0.05 * R, 0.025 * R, '#fff0b0', stroke=None, sw=0))
    return ''.join(o)

def coatstand_svg(px):
    """Bentwood coat stand with a trench coat and a fedora (mid layer, against the wall)."""
    yb = MID_BASE; top = -3.02; P = '#5a2e1b'; wo, wd = W_OBJ, W_DET; o = [contact(px - 0.22, px + 0.22, yb, 0.25)]
    for sg in (-1, 1):
        d = pd('M', px, yb - 0.32, 'C', px + sg * 0.05, yb - 0.1, px + sg * 0.16, yb - 0.06, px + sg * 0.22, yb); o.append(path(d, 'none', stroke=INK, sw=0.07)); o.append(path(d, 'none', stroke=P, sw=0.036))
    o.append(rect(px - 0.032, top, 0.064, yb - top - 0.02, P, sw=wo)); o.append(line(px - 0.01, top + 0.1, px - 0.01, yb - 0.3, mul(P, 1.7), wd)); o.append(circ(px, top - 0.04, 0.055, P, sw=wo))
    for sg in (-1, 1):
        d = pd('M', px, top + 0.2, 'C', px + sg * 0.12, top + 0.22, px + sg * 0.2, top + 0.14, px + sg * 0.23, top + 0.03); o.append(path(d, 'none', stroke=INK, sw=0.06)); o.append(path(d, 'none', stroke=P, sw=0.03))
    CO = '#514a6b'
    o.append(path(pd('M', px - 0.1, top + 0.16, 'C', px - 0.3, top + 0.3, px - 0.31, top + 0.9, px - 0.29, top + 1.72, 'L', px + 0.27, top + 1.72, 'C', px + 0.3, top + 0.9, px + 0.3, top + 0.4, px + 0.16, top + 0.17, 'Z'), CO, sw=wo * 1.2))
    if SHADE[0]: o.append(tone(o[-1], SHADE[0][:-2] + 'scyl'))
    o.append(path(pd('M', px - 0.06, top + 0.2, 'L', px + 0.03, top + 0.7, 'L', px + 0.01, top + 1.7), 'none', stroke=mul(CO, 0.55), sw=wd)); o.append(path(pd('M', px - 0.06, top + 0.2, 'L', px - 0.17, top + 0.5, 'L', px + 0.03, top + 0.7), mul(CO, 1.28), stroke=mul(CO, 0.55), sw=wd))
    o.append(path(pd('M', px + 0.1, top + 0.2, 'L', px + 0.18, top + 0.52, 'L', px + 0.03, top + 0.7), mul(CO, 1.28), stroke=mul(CO, 0.55), sw=wd))
    o.append(path(pd('M', px - 0.25, top + 0.45, 'C', px - 0.24, top + 0.9, px - 0.25, top + 1.2, px - 0.23, top + 1.55), 'none', stroke=mul(CO, 1.5), sw=wd))
    for j in range(3): o.append(circ(px - 0.03, top + 0.86 + j * 0.27, 0.022, mul(CO, 0.5), sw=wd * 0.8))
    o.append(rect(px - 0.27, top + 1.12, 0.54, 0.05, mul(CO, 0.72), sw=wd)); o.append(rect(px + 0.05, top + 1.1, 0.08, 0.09, BRASS, sw=wd))
    HT = '#6b4a36'; hx_, hy_ = px - 0.2, top + 0.04
    b = [path(pd('M', hx_ - 0.15, hy_ - 0.03, 'C', hx_ - 0.15, hy_ - 0.23, hx_ - 0.06, hy_ - 0.28, hx_, hy_ - 0.23, 'C', hx_ + 0.06, hy_ - 0.28, hx_ + 0.15, hy_ - 0.23, hx_ + 0.15, hy_ - 0.03, 'Z'), HT, sw=wo),
         rect(hx_ - 0.15, hy_ - 0.08, 0.3, 0.055, '#2a1c1c', sw=wd), ell(hx_, hy_ - 0.015, 0.27, 0.045, mul(HT, 0.85), sw=wo),
         path(pd('M', hx_ - 0.1, hy_ - 0.15, 'C', hx_ - 0.09, hy_ - 0.2, hx_ - 0.05, hy_ - 0.22, hx_ - 0.01, hy_ - 0.2), 'none', stroke=mul(HT, 1.6), sw=wd)]
    o.append(rot(b, -12, hx_, hy_)); return ''.join(o)

def mid_svg(u, st):
    t = st.get('t', 0.0); o = [radiator_svg(-3.36, -2.56, -1.3), teletype_svg(-2.42, 0.74, t), basket_svg(-1.45, 0.4, 0.5, charts=False)]
    o.append(basket_svg(1.44, 0.4, 0.5)); o.append(coatstand_svg(2.03)); o.append(cabinets_svg(2.42, 1.24, -2.66, u=u))
    o.append(barograph_svg(2.48, -2.71, 0.66, t))
    # box file and paper stack on the second cabinet
    o.append(rect(3.22, -3.02, 0.34, 0.31, '#b08a52')); o.append(rect(3.28, -2.94, 0.22, 0.1, '#f3e7c9', sw=W_DET)); o.append(circ(3.39, -2.79, 0.022, INK, stroke=None, sw=0))
    return ''.join(o)

# ----------------------------------------------------------------------------- fg layer: in front of the actors
def banker_svg(x, y, s):
    """Banker's lamp standing on a desk at (x, y); s = scale (1 = 0.7 D shade)."""
    o = [ell(x, y, 0.2 * s, 0.045 * s, BRASS, sw=W_OBJ * s), rect(x - 0.18 * s, y - 0.06 * s, 0.36 * s, 0.06 * s, BRASS, sw=W_OBJ * s, rx=0.02 * s)]
    o.append(line(x - 0.15 * s, y - 0.04 * s, x + 0.1 * s, y - 0.04 * s, '#fff0b0', W_DET * s))
    o.append(path(pd('M', x, y - 0.06 * s, 'C', x, y - 0.3 * s, x + 0.12 * s, y - 0.32 * s, x + 0.1 * s, y - 0.52 * s), 'none', stroke=INK, sw=0.07 * s)); o.append(path(pd('M', x, y - 0.06 * s, 'C', x, y - 0.3 * s, x + 0.12 * s, y - 0.32 * s, x + 0.1 * s, y - 0.52 * s), 'none', stroke=BRASS, sw=0.04 * s))
    o.append(rect(x - 0.33 * s, y - 0.5 * s, 0.66 * s, 0.05 * s, BULB, stroke='#f0c070', sw=W_DET * s))
    o.append(path(pd('M', x - 0.36 * s, y - 0.5 * s, 'C', x - 0.34 * s, y - 0.68 * s, x - 0.22 * s, y - 0.76 * s, x, y - 0.76 * s, 'C', x + 0.22 * s, y - 0.76 * s, x + 0.34 * s, y - 0.68 * s, x + 0.36 * s, y - 0.5 * s, 'Z'), '#2d7a52', sw=W_OBJ * s))
    o.append(path(pd('M', x - 0.27 * s, y - 0.57 * s, 'C', x - 0.22 * s, y - 0.68 * s, x - 0.1 * s, y - 0.71 * s, x + 0.02 * s, y - 0.71 * s), 'none', stroke='#6fc191', sw=W_DET * 1.5 * s))
    o.append(line(x + 0.3 * s, y - 0.5 * s, x + 0.3 * s, y - 0.36 * s, BRASS, W_DET * s)); o.append(circ(x + 0.3 * s, y - 0.35 * s, 0.018 * s, BRASS, sw=W_DET * s * 0.8))
    return ''.join(o)

def fg_svg(u, st):
    o = []; k = 1.7; wo, wd = W_OBJ * k, W_DET * k; D1, D2 = '#4f2617', '#7d4e2e'
    # --- desk corner, lower left (very near the camera): top, front with drawers, shaded side
    fx, fy = -1.32, 1.18; bx, by = vp(fx, fy, 0.85); H = 5.0
    o.append(poly([(fx, fy), (bx, by), (bx, by + H), (fx, fy + H)], mul(D1, 0.62), sw=wo))
    o.append(poly([(-6, by), (bx, by), (fx, fy), (-6, fy)], D2, sw=wo))
    for j in range(5):
        y = by + (fy - by) * (j + 0.5) / 5; o.append(line(-6, y, bx + (fx - bx) * (j + 0.5) / 5 - 0.03, y, mul(D2, 0.8 if j % 2 else 1.18), wd))
    o.append(rect(-6, fy, 6 + fx, 0.11, '#a56a3c', sw=wo)); o.append(line(-6, fy + 0.035, fx - 0.02, fy + 0.035, '#d39a62', wd))
    o.append(rect(-6, fy + 0.11, 6 + fx, H, D1, sw=wo))
    for j in range(3):
        y = fy + 0.3 + j * 1.05; o.append(rect(-3.0, y, 1.45, 0.9, mul(D1, 1.22), stroke=mul(D1, 0.5), sw=wd * 1.3)); o.append(pline([(-2.96, y + 0.86), (-2.96, y + 0.04), (-1.59, y + 0.04)], mul(D1, 1.75), wd))
        o.append(rect(-2.5, y + 0.36, 0.45, 0.1, BRASS, sw=wd, rx=0.03)); o.append(line(-2.46, y + 0.385, -2.1, y + 0.385, '#fff0b0', wd * 0.7))
    o.append(rect(-6, fy + 0.3, 2.75, 0.5, mul(D1, 1.22), stroke=mul(D1, 0.5), sw=wd * 1.3)); o.append(circ(-4.0, fy + 0.55, 0.07, BRASS, sw=wd))
    o.append(rect(-6, fy + 0.11, 6 + fx, H, f'url(#{u}fgsh)', stroke=None, sw=0))
    # things on the desk: telephone, lamp, papers, ink bottle, red pencil
    ty = by + 0.33; o.append('<g transform="translate(%s 0)">' % n(0.55))
    o.append(path(pd('M', -3.95, ty, 'L', -3.9, ty - 0.3, 'C', -3.85, ty - 0.42, -3.35, ty - 0.42, -3.3, ty - 0.3, 'L', -3.25, ty, 'Z'), '#241a2e', sw=wo))
    o.append(circ(-3.6, ty - 0.17, 0.11, '#3a3442', sw=wd)); o.append(circ(-3.6, ty - 0.17, 0.045, '#e9d9b0', sw=wd * 0.7))
    o.append(path(pd('M', -4.05, ty - 0.46, 'C', -4.05, ty - 0.62, -3.9, ty - 0.5, -3.6, ty - 0.52, 'C', -3.3, ty - 0.5, -3.15, ty - 0.62, -3.15, ty - 0.46, 'C', -3.2, ty - 0.36, -3.3, ty - 0.4, -3.6, ty - 0.42, 'C', -3.9, ty - 0.4, -4.0, ty - 0.36, -4.05, ty - 0.46, 'Z'), '#241a2e', sw=wo))
    o.append(path(pd('M', -3.95, ty - 0.52, 'C', -3.8, ty - 0.56, -3.5, ty - 0.57, -3.3, ty - 0.53), 'none', stroke='#6d647a', sw=wd)); o.append('</g>')
    o.append(banker_svg(-2.12, by + 0.3, 1.75))
    for (px, py, a, col) in ((-1.95, by + 0.28, -7, '#f6efe2'), (-1.72, by + 0.34, 5, '#fff5df')):
        b = [poly([(px - 0.42, py + 0.17), (px + 0.3, py + 0.17), (px + 0.42, py - 0.13), (px - 0.26, py - 0.13)], col, sw=wd * 1.3)]
        for j in range(4): b.append(line(px - 0.3 + j * 0.035, py + 0.11 - j * 0.06, px + 0.26 + j * 0.035, py + 0.11 - j * 0.06, '#9a8f86', wd * 0.8))
        o.append(rot(b, a, px, py))
    o.append(rot(rect(-1.75, by + 0.26, 0.52, 0.045, RED, sw=wd) + poly([(-1.23, by + 0.26), (-1.14, by + 0.2825), (-1.23, by + 0.305)], '#e9c79a', sw=wd), -14, -1.5, by + 0.28))
    o.append(rect(-1.6, by - 0.02, 0.2, 0.22, NAVY, sw=wo, rx=0.03)); o.append(rect(-1.56, by - 0.1, 0.12, 0.09, '#1c1a22', sw=wd)); o.append(rect(-1.585, by + 0.05, 0.17, 0.09, '#f3e7c9', sw=wd * 0.8))
    # --- chair back, lower right
    cx0, cx1, cy = 1.95, 3.25, 1.02; C = '#55291a'
    for sx in (cx0, cx1 - 0.16): o.append(rect(sx, cy + 0.1, 0.16, 5, C, sw=wo))
    for j in range(4): xx = cx0 + 0.34 + j * 0.24; o.append(rect(xx, cy + 0.3, 0.1, 5, mul(C, 1.15), sw=wd * 1.3))
    o.append(path(pd('M', cx0 - 0.08, cy + 0.34, 'C', cx0 - 0.06, cy - 0.02, cx0 + 0.3, cy - 0.06, (cx0 + cx1) / 2, cy - 0.06, 'C', cx1 - 0.3, cy - 0.06, cx1 + 0.06, cy - 0.02, cx1 + 0.08, cy + 0.34, 'Z'), mul(C, 1.3), sw=wo))
    o.append(path(pd('M', cx0 + 0.02, cy + 0.2, 'C', cx0 + 0.1, cy + 0.03, cx0 + 0.4, cy + 0.0, (cx0 + cx1) / 2, cy + 0.0), 'none', stroke=mul(C, 2.3), sw=wd))
    o.append(f'<clipPath id="{u}chc">' + ''.join(rect(sx, cy + 0.1, 0.16, 5, '#000', stroke=None, sw=0) for sx in (cx0, cx1 - 0.16)) + ''.join(rect(cx0 + 0.34 + j * 0.24, cy + 0.3, 0.1, 5, '#000', stroke=None, sw=0) for j in range(4)) + '</clipPath>')
    o.append(rect(cx0 - 0.3, cy + 0.1, 2.2, 5.2, f'url(#{u}fgsh)', stroke=None, sw=0, extra=f'opacity="0.7" clip-path="url(#{u}chc)"'))
    return ''.join(o)

# ----------------------------------------------------------------------------- light layer (screen / additive)
SHAFT = [(-2.3, -3.95), (-2.3, -1.75), (0.35, 1.5), (1.75, 0.35)]
def light_svg(u, st):
    t = float(st.get('t', 0.0)); o = []
    for k, a in ((0.0, 0.7), (0.12, 0.35), (0.26, 0.18)):                 # window shaft: nested quads give a soft edge without a blur filter
        c = [sum(p[0] for p in SHAFT) / 4, sum(p[1] for p in SHAFT) / 4]; pts = [(p[0] + (c[0] - p[0]) * k * (0 if i < 2 else 1), p[1] + (c[1] - p[1]) * k * (0.25 if i < 2 else 1)) for i, p in enumerate(SHAFT)]
        o.append(poly(pts, f'url(#{u}shaft)', stroke=None, sw=0, extra=f'opacity="{a}"'))
    r = random.Random(31)
    for i in range(22):                                                    # dust drifting in the shaft
        a, b = r.random(), r.random(); ph = r.uniform(0, 6.28); sp = r.uniform(0.012, 0.03); a2 = (a + 0.02 * math.sin(0.23 * t + ph)) % 1; b2 = (b - sp * t * 0.25) % 1
        top = (SHAFT[0][0] + (SHAFT[1][0] - SHAFT[0][0]) * a2, SHAFT[0][1] + (SHAFT[1][1] - SHAFT[0][1]) * a2); bot = (SHAFT[3][0] + (SHAFT[2][0] - SHAFT[3][0]) * a2, SHAFT[3][1] + (SHAFT[2][1] - SHAFT[3][1]) * a2)
        x, y = top[0] + (bot[0] - top[0]) * b2, top[1] + (bot[1] - top[1]) * b2; op = (0.14 + 0.22 * r.random()) * math.sin(math.pi * b2) ** 0.6
        o.append(circ(x, y, r.uniform(0.004, 0.009), '#fff3d6', stroke=None, sw=0, extra=f'opacity="{op:.2f}"'))
    for lx, ly, lr in LAMPS: o.append(circ(lx, ly, lr * 2.0, f'url(#{u}halo)', stroke=None, sw=0))     # tight warm halo: 10 percent point 12-23 px beyond the bulb at 110-200 px per D
    return ''.join(o)
def fg_light_svg(u):
    """Glow of the banker's lamp on the fg desk (belongs to the fg plane)."""
    fx, fy = -1.32, 1.18; bx, by = vp(fx, fy, 0.85); x, y, s = -2.12, by + 0.3, 1.75
    return ell(x, y - 0.3 * s, 0.75 * s, 0.42 * s, f'url(#{u}glow)', stroke=None, sw=0) + rect(x - 0.33 * s, y - 0.5 * s, 0.66 * s, 0.05 * s, BULB, stroke=None, sw=0, extra='opacity="0.9"')

# ----------------------------------------------------------------------------- public API
CAMS = dict(cam_wide=(0.0, -1.70, 110.0), cam_two_shot=(0.33, -2.16, 150.0), cam_medium_hero=(-0.20, -2.18, 200.0), cam_push_in=(-0.12, -2.38, 250.0))
PIVOT = (0.0, -1.70)            # parallax pivot = centre of cam_wide (layers register exactly there)
INSERT_CAM = (0.0, -2.16, 218.0)
INSERT_CAM_TIGHT = (0.12, -2.42, 300.0)

def _wrap(s): return f'<g transform="scale({1 / K:g})">' + s + '</g>'
def _state(state):
    st = dict(state or {}); st['line'] = max(0.0, min(1.0, float(st.get('line', 0.0)))); st['erase'] = max(0.0, min(1.0, float(st.get('erase', 0.0)))); st['t'] = float(st.get('t', 0.0)); return st
def _anchors(st):
    fx, fy = -1.32, 1.18; bx, by = vp(fx, fy, 0.85); keep = st['line'] * (1 - st['erase'])
    a = dict(floor_y=0.0, wall_base_y=WALL_BASE, eye_line_y=VPY, map_rect=MAP_OUT, map_paper_rect=MAP_IN, map_track=list(TRACK), map_ny=TRACK[-1], map_storm=TRACK[0],
             pencil_tip=track_point(st['line'])[:2], line_end=track_point(keep)[:2], hero_mark=HERO_X, boss_mark=BOSS_X, hero_shoulder_y=-2.0,
             lamps=[(x, y) for x, y, r in LAMPS], lamp_radius=[r for x, y, r in LAMPS], banker_lamp=(-2.12, round(by + 0.3 - 0.875, 3)),
             desk_top=dict(y_back=round(by, 3), y_front=fy, x_right_front=fx, x_right_back=round(bx, 3), layer='fg'),
             ledge_y=MAP_OUT[3] - 0.005, ledge_x=(MAP_OUT[0] - 0.09, MAP_OUT[2] + 0.09), eraser_on_ledge=(0.805, MAP_OUT[3] - 0.03), red_pencil_on_ledge=(-0.69, MAP_OUT[3] - 0.02),
             window_rect=(-3.42, -4.1, -2.25, -1.6), sign_rect=(-1.5, -4.34, 1.5, -3.9), clock=(2.03, -4.1), calendar_rect=(-2.09, -4.35, -1.59, -3.69),
             parallax_pivot=PIVOT, world=WORLD)
    a.update(CAMS); return a

def build(state=None, uid='of'):
    """Office set as layered SVG fragments in D units. See API.md."""
    st = _state(state); u = uid; SHADE[0] = u + 'sv'
    try:
        bg = shell_svg(u) + floor_svg(u) + light_warm_svg(u) + bg_props_svg(u, st) + falloff_svg(u) + draw_map(u, st) + ledge_svg(st) + pendants_svg()
        mid = mid_svg(u, st); fg = fg_svg(u, st) + fg_light_svg(u); lt = light_svg(u, st)
    finally: SHADE[0] = None
    layers = [dict(name='bg', svg=_wrap(bg), parallax=1.0, depends=('line', 'erase', 't')), dict(name='mid', svg=_wrap(mid), parallax=1.0, depends=()),
              dict(name='fg', svg=_wrap(fg), parallax=1.12, depends=()), dict(name='light', svg=_wrap(lt), parallax=1.0, blend='screen', depends=('t',))]
    return dict(layers=layers, defs='<defs>' + map_defs(u) + room_defs(u) + '</defs>', world=WORLD, anchors=_anchors(st))

def build_insert_map(state=None, uid='ofi'):
    """Full-frame close-up drawing of the wall map (same world coordinates as build(); thinner lines, more map detail)."""
    st = _state(state); u = uid; LW[0] = 0.69; SHADE[0] = u + 'sv'
    try:
        a = shell_svg(u) + floor_svg(u) + light_warm_svg(u)
        LW[0] = 1.0; m = draw_map(u, st, hi=True) + ledge_svg(st, hi=True); LW[0] = 0.69
        b = bg_props_svg(u, st) + falloff_svg(u); pe = pendants_svg(); mid = mid_svg(u, st); lt = light_svg(u, st)
    finally: LW[0] = 1.0; SHADE[0] = None
    an = _anchors(st); an = {k: an[k] for k in ('map_rect', 'map_paper_rect', 'map_track', 'map_ny', 'map_storm', 'pencil_tip', 'line_end', 'ledge_y', 'ledge_x', 'eraser_on_ledge', 'red_pencil_on_ledge', 'world')}
    an.update(cam=INSERT_CAM, cam_insert=INSERT_CAM, cam_insert_tight=INSERT_CAM_TIGHT, parallax_pivot=INSERT_CAM[:2])
    layers = [dict(name='bg', svg=_wrap(a + b + m + pe), parallax=1.0, depends=('line', 'erase', 't')), dict(name='mid', svg=_wrap(mid), parallax=1.0, depends=()), dict(name='light', svg=_wrap(lt), parallax=1.0, blend='screen', depends=('t',))]
    return dict(layers=layers, defs='<defs>' + map_defs(u) + room_defs(u) + '</defs>', world=WORLD, anchors=an)

def layer_transform(cam, parallax=1.0, W=720, H=1280, pivot=PIVOT):
    """SVG transform that places a layer for camera (cx, cy, zoom px per D)."""
    cx, cy, z = cam; ex, ey = pivot[0] + (cx - pivot[0]) * parallax, pivot[1] + (cy - pivot[1]) * parallax
    return f'translate({W / 2:g} {H / 2:g}) scale({z:g}) translate({-ex:.4f} {-ey:.4f})'

def compose(built, cam, actors='', W=720, H=1280, extra_defs=''):
    """Reference compositor: full SVG document for one frame. `actors` = SVG fragment in set world D units."""
    piv = built['anchors'].get('parallax_pivot', PIVOT); o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', built['defs'], extra_defs, f'<rect width="{W}" height="{H}" fill="#1a1016"/>']
    for L in built['layers']:
        if L['name'] in ('fg', 'light') and actors: o.append(f'<g transform="{layer_transform(cam, 1.0, W, H, piv)}">{actors}</g>'); actors = ''
        bl = f' style="mix-blend-mode:{L["blend"]}"' if L.get('blend') else ''
        o.append(f'<g transform="{layer_transform(cam, L["parallax"], W, H, piv)}"{bl}>{L["svg"]}</g>')
    if actors: o.append(f'<g transform="{layer_transform(cam, 1.0, W, H, piv)}">{actors}</g>')
    o.append('</svg>'); return ''.join(o)

def dummy_actors(pose='draw'):
    """Stand-in puppets (white head, plum ink, costume blob) at the two marks: for staging review only."""
    ink = '#3a2832'; o = []
    for x, col, wdt, hat in ((HERO_X, '#3f9c96', 0.6, '#3b3350'), (BOSS_X, '#d9a531', 0.98, '#4a3a2c')):
        for sg in (-1, 1): o.append(f'<path d="M{x + sg * 0.14:.3f},-1.14 L{x + sg * 0.16:.3f},-0.03 l{sg * 0.17:.3f},0" fill="none" stroke="{ink}" stroke-width="0.065" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(f'<rect x="{x - wdt / 2:.3f}" y="-2.14" width="{wdt:.3f}" height="1.04" rx="{wdt * 0.42:.3f}" fill="{col}" stroke="{ink}" stroke-width="0.03"/>')
        o.append(f'<ellipse cx="{x:.3f}" cy="-2.5" rx="0.48" ry="0.47" fill="#fcf8f6" stroke="{ink}" stroke-width="0.045"/>')
        o.append(f'<path d="M{x - 0.4:.3f},-2.8 q0.4,-0.42 0.8,0 z" fill="{hat}" stroke="{ink}" stroke-width="0.03"/>')
        for sg in (-1, 1): o.append(f'<path d="M{x + sg * 0.17 - 0.05:.3f},-2.58 q0.05,-0.05 0.1,0" fill="none" stroke="{ink}" stroke-width="0.03" stroke-linecap="round"/>')
    if pose == 'draw':
        nx, ny = TRACK[-1]; sx, sy = HERO_X + 0.25, -2.02
        o.append(f'<path d="M{sx:.3f},{sy:.3f} Q{(sx + nx) / 2 + 0.14:.3f},{(sy + ny) / 2 + 0.04:.3f} {nx - 0.02:.3f},{ny + 0.05:.3f}" fill="none" stroke="{ink}" stroke-width="0.065" stroke-linecap="round"/><circle cx="{nx - 0.02:.3f}" cy="{ny + 0.05:.3f}" r="0.06" fill="{ink}"/>')
    return ''.join(o)

# ----------------------------------------------------------------------------- review renders + measurements
def _raster(jobs):
    jp = os.path.join(PROJ, 'v2', 'tmp', 'office_jobs.json'); os.makedirs(os.path.dirname(jp), exist_ok=True); json.dump(jobs, open(jp, 'w'))
    subprocess.run(['node', os.path.join(HERE, 'raster.js'), jp], check=True, env=dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')))

def measure(path, heads=None):
    """Acceptance numbers (metrics.py stats + featureless 40 px blocks + luminance zones + ring behind heads)."""
    import importlib.util, numpy as np, cv2
    sp = importlib.util.spec_from_file_location('envmetrics', os.path.join(PROJ, 'ref', 'crops', 'env', 'tools', 'metrics.py')); mm = importlib.util.module_from_spec(sp); sp.loader.exec_module(mm)
    im = mm.load(path); s = {k: round(float(v), 3) for k, v in mm.stats(im).items()}
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32); hp = g - cv2.GaussianBlur(g, (0, 0), 3)
    fl = [hp[y:y + 40, x:x + 40].std() < 3 for y in range(0, 1280, 40) for x in range(0, 720, 40) if not (840 <= y < 960)]
    s['featureless'] = round(float(np.mean(fl)), 3)
    rows = [g[i * 160:(i + 1) * 160].mean() for i in range(8)]; s['lum_top'] = round(float(rows[0]), 1); s['lum_mid'] = round(float(np.mean(rows[3:5])), 1); s['lum_bot'] = round(float(rows[7]), 1); s['lum_rows'] = [int(round(float(v))) for v in rows]   # spec 2.2/2.9: top row, the two central rows, bottom row of an 8-row grid
    cell = lambda r, c: g[r * 160:(r + 1) * 160, c * 144:(c + 1) * 144].mean()
    s['corners'] = round(float(np.mean([cell(0, 0), cell(0, 4), cell(7, 0), cell(7, 4)])), 1); s['centre'] = round(float(np.mean([cell(3, 2), cell(4, 2)])), 1)
    if heads:
        yy, xx = np.mgrid[0:1280, 0:720]; out = []
        for hx_, hy_, d in heads:
            rr = np.hypot(xx - hx_, yy - hy_); m = (rr > 0.55 * d) & (rr < 0.95 * d); out.append(round(float(g[m].mean()), 1)) if m.any() else None
        s['behind_heads'] = out
    return s

def _heads(cam, W=720, H=1280): return [((x - cam[0]) * cam[2] + W / 2, (-2.5 - cam[1]) * cam[2] + H / 2, cam[2]) for x in (HERO_X, BOSS_X)]

def frames():
    from PIL import Image
    T = os.path.join(PROJ, 'v2', 'tmp'); os.makedirs(T, exist_ok=True); jobs = []; st = dict(line=1.0, erase=0.0, t=0.0)
    b = build(st, 'of'); bi = build_insert_map(st, 'ofi')
    shots = (('office_wide', b, CAMS['cam_wide']), ('office_two_shot', b, CAMS['cam_two_shot']), ('office_medium', b, CAMS['cam_medium_hero']), ('office_insert', bi, INSERT_CAM))
    for name, bb, cam in shots:
        p = os.path.join(T, name + '.svg'); open(p, 'w').write(compose(bb, cam)); jobs.append(dict(src=p, out=os.path.join(HERE, name + '.png'), w=720, h=1280))
    for name, cam in (('staged_two_shot', CAMS['cam_two_shot']), ('staged_medium', CAMS['cam_medium_hero']), ('staged_wide', CAMS['cam_wide']), ('staged_push', CAMS['cam_push_in'])):
        p = os.path.join(T, name + '.svg'); open(p, 'w').write(compose(b, cam, dummy_actors())); jobs.append(dict(src=p, out=os.path.join(HERE if name in ('staged_two_shot', 'staged_medium') else T, ('office_' if name in ('staged_two_shot', 'staged_medium') else '') + name + '.png'), w=720, h=1280))
    states = (dict(line=0), dict(line=0.5), dict(line=1), dict(line=1, erase=0.5), dict(line=1, erase=1)); PW, PH = 400, 480
    for i, s_ in enumerate(states):
        p = os.path.join(T, f'state{i}.svg'); open(p, 'w').write(compose(build(s_, f's{i}'), (0.0, -2.42, 118.0), W=PW, H=PH)); jobs.append(dict(src=p, out=os.path.join(T, f'state{i}.png'), w=PW, h=PH))
    _raster(jobs)
    strip = Image.new('RGB', (PW * 5 + 4 * 6, PH), '#1a1016')
    for i in range(5): strip.paste(Image.open(os.path.join(T, f'state{i}.png')).convert('RGB'), (i * (PW + 6), 0))
    strip.save(os.path.join(HERE, 'office_states.png'))
    cmp_ = Image.new('RGB', (720 * 3 + 16, 1280), '#000000')
    for i, p in enumerate((os.path.join(PROJ, 'ref', 'b', 't07.0.jpg'), os.path.join(HERE, 'office_two_shot.png'), os.path.join(PROJ, 'ref', 'b', 't18.5.jpg'))):
        cmp_.paste(Image.open(p).convert('RGB').resize((720, 1280)), (i * 728, 0))
    cmp_.save(os.path.join(HERE, 'compare.jpg'), quality=90)
    res = {}
    for name, bb, cam in shots: res[name] = measure(os.path.join(HERE, name + '.png'), _heads(cam) if name != 'office_insert' else None)
    for name in ('staged_two_shot', 'staged_medium'): res[name] = measure(os.path.join(HERE, 'office_' + name + '.png'))
    for k, v in res.items(): print(k, json.dumps(v))
    json.dump(res, open(os.path.join(HERE, 'metrics.json'), 'w'), indent=1)
    return res

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'frames': frames()
    else: print(__doc__)
