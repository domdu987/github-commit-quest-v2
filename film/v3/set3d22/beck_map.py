#!/usr/bin/env python3
"""beck_map.py (builder B): the MAPWORLD of film 22 (shots s12, s14) and the shared diagram data (the pocket map of the carriage, beck_under.py).

The London diagram is ONE data set (DIAGRAM): the same lines paint the pocket-map texture (`paper_image`) and become the raised glossy lines of the
mapworld (`build_mapworld`), so the push from the pocket map into the paper (s11 -> s12) is a true match.  Cell = 10 D, paper 26 x 18 cells = 260 x 180 D,
paper centre = world origin, +y = top of the paper, +x = right.  City sheets (NEW YORK, TOKYO, PARIS, SYDNEY, BANGKOK ...) lie around it (s14).
Lines only run at 0 / 45 / 90 degrees (`check_diagram()` asserts it)."""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw
import beck as B
import beck_util as U
from beck import V, STATE, BX, T
from mine import obox, rod

CELL = 10.0; GW, GH = 26, 18
RED, BLUE, GREEN, YELLOW, BROWN, BLACK = '#e3262b', '#1f49c8', '#12a15a', '#ffc81e', '#7a4a22', '#25233a'
COL = dict(red=RED, blue=BLUE, green=GREEN, yellow=YELLOW, brown=BROWN, black=BLACK)
# (u, v) in cells, v DOWN from the top of the paper
DIAGRAM = dict(
    lines=[('red', [(1, 5), (9, 5), (13, 9), (25, 9)]), ('blue', [(16, 1), (16, 14), (19, 17), (25, 17)]), ('green', [(1, 14), (11, 14), (21, 4), (25, 4)]),
           ('yellow', [(21, 1), (21, 12), (18, 15), (18, 17)]), ('brown', [(1, 9), (5, 9), (9, 13), (9, 17)]), ('black', [(1, 2), (12, 2), (16, 6)])],
    rings=[(16, 9, 'BANK'), (21, 9, 'EUSTON'), (9, 14, 'OXFORD'), (16, 6, 'ANGEL'), (21, 4, 'KINGS X'), (16, 14, 'WATERLOO'), (21, 12, 'VICTORIA')],
    stations=['PADDINGTON', 'MARBLE ARCH', 'HOLBORN', 'BARBICAN', 'ALDGATE', 'STEPNEY', 'BOW', 'POPLAR', 'KEW', 'EALING', 'HOXTON', 'SOHO', 'MAYFAIR', 'ELEPHANT',
              'BROMLEY', 'ACTON', 'PUTNEY', 'BRIXTON', 'LEWISHAM', 'CAMDEN', 'ANGEL RD', 'TOOTING', 'FULHAM'])

def check_diagram(D=None):
    D = D or DIAGRAM
    for col, pts in D['lines']:
        for a, b in zip(pts, pts[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            assert dx == 0 or dy == 0 or abs(dx) == abs(dy), (col, a, b)
    return True

def w_xy(u, v, ox=0.0, oy=0.0):
    """cell coordinates -> mapworld xy (London paper centred on the origin, y up)."""
    return ((u - GW / 2) * CELL + ox, (GH / 2 - v) * CELL + oy)

def line_path(col='red', D=None):
    """Polyline of a line in WORLD xy (list of (x, y)) and its cumulative length: used by the train / camera / passengers."""
    D = D or DIAGRAM; pts = dict(D['lines'])[col] if False else [p for c, p in D['lines'] if c == col][0]
    xy = [w_xy(*p) for p in pts]; cum = [0.0]
    for a, b in zip(xy, xy[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return xy, cum

def path_at(xy, cum, s):
    """position (x, y) and unit tangent (tx, ty) at distance s along the polyline (clamped, linear extrapolation beyond the ends)."""
    s = max(0.0, min(cum[-1], s))
    for i in range(len(xy) - 1):
        if s <= cum[i + 1] or i == len(xy) - 2:
            a, b = xy[i], xy[i + 1]; L = cum[i + 1] - cum[i]; u = (s - cum[i]) / max(L, 1e-9)
            return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)

def stations_on(D=None, step=2):
    """Station tick positions (cells) along each line, away from rings: [(col, (u, v), (tx, ty))]."""
    D = D or DIAGRAM; rs = [(r[0], r[1]) for r in D['rings']]; out = []
    for col, pts in D['lines']:
        for a, b in zip(pts, pts[1:]):
            L = max(abs(b[0] - a[0]), abs(b[1] - a[1])); dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            for k in range(1, int(L)):
                if k % step: continue
                p = (a[0] + dx * k, a[1] + dy * k)
                if any(abs(p[0] - r[0]) < 1.5 and abs(p[1] - r[1]) < 1.5 for r in rs): continue
                out.append((col, p, (dx, dy)))
    return out

def paper_image(W=1560, H=1080, lw=0.2, title='UNDERGROUND', D=None, ring_names=True, lines=True, river=True, seed=3):
    """The pocket map / mapworld paper: cream, faint grid, pale river, the straight-line diagram with station ticks and ring names."""
    D = D or DIAGRAM; S = 1; cs = W / GW
    img = Image.new('RGB', (W, H), '#f6ecd2'); rs = np.random.RandomState(seed)
    a = np.asarray(img, 'float32') / 255 * (0.95 + BX.noise(rs, H, W, 40, 0.07))[..., None]; img = Image.fromarray((np.clip(a, 0, 1) * 255).astype('uint8')); d = ImageDraw.Draw(img)
    for i in range(GW + 1): d.line((i * cs, 0, i * cs, H), fill='#e8dcb6', width=2)
    for j in range(GH + 1): d.line((0, j * cs, W, j * cs), fill='#e8dcb6', width=2)
    if river and D is DIAGRAM:
        rv = [(0, 11.7), (7, 11.7), (9, 13.6), (14, 13.6), (17.5, 11.2), (26, 11.2)]
        d.line([(x * cs, y * cs) for x, y in rv], fill='#a8d6ee', width=int(cs * 1.1), joint='curve')
    def P(pts): return [(x * cs, y * cs) for x, y in pts]
    if lines:
        for col, pts in D['lines']:
            w = int(cs * lw); p = P(pts); d.line(p, fill=COL[col], width=w, joint='curve')
            for q in (p[0], p[-1]): d.ellipse((q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2), fill=COL[col])
            for q in p[1:-1]: d.ellipse((q[0] - w / 2, q[1] - w / 2, q[0] + w / 2, q[1] + w / 2), fill=COL[col])
        for col, (u, v), (tx, ty) in stations_on(D):
            nx, ny = -ty, tx; r = cs * 0.36; d.line(((u - nx * 0.38) * cs, (v - ny * 0.38) * cs, (u + nx * 0.38) * cs, (v + ny * 0.38) * cs), fill='#1a1840', width=max(4, int(cs * 0.07)))
        R = cs * 0.62
        for (u, v, nm) in D['rings']:
            d.ellipse((u * cs - R, v * cs - R, u * cs + R, v * cs + R), fill='white', outline='#1a1840', width=int(cs * 0.11))
        ft = BX.font(cs * 0.44, BX.FB)
        if ring_names:
            for (u, v, nm) in D['rings']:
                d.text((u * cs + R * 1.05, v * cs - R * 1.0), nm, font=ft, fill='#1a1840', anchor='lb')
            fs = BX.font(cs * 0.34, BX.FN); names = list(D['stations']); k = 0
            for col, (u, v), (tx, ty) in stations_on(D):
                d.text((u * cs + cs * 0.5, v * cs - cs * 0.5), names[k % len(names)], font=fs, fill='#3a3050', anchor='lb'); k += 1
    d.rectangle((6, 6, W - 7, H - 7), outline='#1a1840', width=int(cs * 0.12))
    if title:
        d.rectangle((cs * 0.6, H - cs * 1.9, cs * 9.2, H - cs * 0.7), fill='#1f49c8'); BX.fit_text(d, (cs * 0.8, H - cs * 1.8, cs * 9.0, H - cs * 0.8), title, 'white')
    return img

CITIES = [('NEW YORK', (1, 0), 11), ('PARIS', (-1, 0), 12), ('TOKYO', (0, 1), 13), ('SYDNEY', (0, -1), 14), ('BANGKOK', (1, 1), 15),
          ('MOSCOW', (-1, 1), 16), ('MADRID', (-1, -1), 17), ('CAIRO', (1, -1), 18)]

def city_diagram(seed):
    """A different straight-line diagram in the same 0 / 45 / 90 style: 5 coloured lines (random walks with 45-degree bends), rings where they cross."""
    r = random.Random(seed); lines = []; dirs8 = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    def room(u, v, d):
        m = 99
        if d[0] > 0: m = min(m, 25 - u)
        if d[0] < 0: m = min(m, u - 1)
        if d[1] > 0: m = min(m, 17 - v)
        if d[1] < 0: m = min(m, v - 1)
        return m
    for col in ('red', 'blue', 'green', 'yellow', 'brown'):
        u, v = r.choice([(1, r.randint(2, 16)), (r.randint(2, 24), 1), (25, r.randint(2, 16)), (r.randint(2, 24), 17)])
        d = (1, 0) if u <= 1 else (-1, 0) if u >= 25 else (0, 1) if v <= 1 else (0, -1); pts = [(u, v)]
        for k in range(5):
            m = room(u, v, d)
            if m < 2: break
            L = r.randint(2, min(8, m)); u, v = u + d[0] * L, v + d[1] * L; pts.append((u, v))
            opts = [x for x in dirs8 if x != (-d[0], -d[1]) and x != d and room(u, v, x) >= 2 and abs(x[0] * d[0] + x[1] * d[1]) < 2]
            if not opts: break
            d = r.choice(opts)
        if len(pts) >= 2: lines.append((col, pts))
    rings = []
    for i, (c1, p1) in enumerate(lines):
        for c2, p2 in lines[i + 1:]:
            for a, b in zip(p1, p1[1:]):
                for c, d_ in zip(p2, p2[1:]):
                    for pt in _seg_cross(a, b, c, d_):
                        if all(abs(pt[0] - q[0]) + abs(pt[1] - q[1]) > 2 for q in rings): rings.append(pt)
    return dict(lines=lines, rings=[(p[0], p[1], '') for p in rings[:7]], stations=DIAGRAM['stations'])

def _seg_cross(a, b, c, d):
    out = []
    def pts(a, b):
        L = max(abs(b[0] - a[0]), abs(b[1] - a[1]))
        if L == 0: return [a]
        return [(a[0] + (b[0] - a[0]) * k / L, a[1] + (b[1] - a[1]) * k / L) for k in range(int(L) + 1)]
    A = set((round(x), round(y)) for x, y in pts(a, b))
    for x, y in pts(c, d):
        if (round(x), round(y)) in A: out.append((round(x), round(y)))
    return out

# ----------------------------------------------------------------------------- mapworld build
MAP_LIGHT = 'MAPWORLD'
B.LIGHTS['MAPWORLD'] = dict(B.LIGHTS['DUSK_CITY'], key=(1.5, 0.92, 0.5), key_dir=B.kdir(250, 24), shade=(0.17, 0.17, 0.50), shade_tint=(0.12, 0.13, 0.52), shade_mix=0.55,
                            lift=(0.03, 0.036, 0.10), grade_offset=(-0.004, -0.006, 0.0), grade_saturation=1.12)

CITY_MATS = {}
CITY_ROOT = {}

def _raise_line(mb, pts_xy, w, h, mat, top_mat, z0=0.0):
    for a, b in zip(pts_xy, pts_xy[1:]):
        U.seg_box(mb, (a[0], a[1], z0), (b[0], b[1], z0), w, h, mat)
        U.seg_box(mb, (a[0], a[1], z0 + h), (b[0], b[1], z0 + h), w * 0.34, 0.07, top_mat)
    for p in pts_xy:
        rod(mb, (p[0], p[1], z0), (p[0], p[1], z0 + h), w / 2, mat, seg=10)

def build_sheet(name, D, ox, oy, C, TX, E, lit=True, titles=True, cityidx=None, rot=0.0):
    """One diagram sheet at offset (ox, oy): paper plane, raised lines, rings, ticks."""
    k = ox * 0 + 1
    tag = name.replace(' ', '_')
    utex_name = 'paper_' + tag
    U.utex(utex_name, lambda: paper_image(1560, 1080, lw=0.2, title=name, D=D, river=(D is DIAGRAM), seed=abs(hash(tag)) % 97 if D is not DIAGRAM else 3))
    g = U.Pt('paper_' + tag, ink=False); B.plane(g.mb, (ox - GW * CELL / 2, oy - GH * CELL / 2, 0.0), (GW * CELL, 0, 0), (0, GH * CELL, 0), TX(utex_name, 1.0, 1.0, form=False), (0, 0, 1, 1)); g.done()
    # frame of the sheet: slightly raised cream border so the sheets read as papers laid on the table
    fr = U.Pt('paperedge_' + tag, (ox, oy, 0), ink=True); mb = fr.mb; ec = C('#e8dcb8', 1.0, 1.4)
    mb.box((ox - GW * CELL / 2 - 0.6, oy - GH * CELL / 2 - 0.6, -0.5), (ox + GW * CELL / 2 + 0.6, oy - GH * CELL / 2, 0.15), ec)
    mb.box((ox - GW * CELL / 2 - 0.6, oy + GH * CELL / 2, -0.5), (ox + GW * CELL / 2 + 0.6, oy + GH * CELL / 2 + 0.6, 0.15), ec)
    mb.box((ox - GW * CELL / 2 - 0.6, oy - GH * CELL / 2, -0.5), (ox - GW * CELL / 2, oy + GH * CELL / 2, 0.15), ec)
    mb.box((ox + GW * CELL / 2, oy - GH * CELL / 2, -0.5), (ox + GW * CELL / 2 + 0.6, oy + GH * CELL / 2, 0.15), ec)
    fr.done((ox, oy, 0), px=2.5)
    lp = U.Pt('lines_' + tag, (ox, oy, 0.4), ink=True); mb = lp.mb
    tick = C('#1a1840', 1.0, 1.0); wmat = C('#ffffff', 1.1, 1.2); rmat = C('#f6ecd2', 1.0, 1.0)
    for col, pts in D['lines']:
        mat = (C(COL[col], 1.15, 1.6, smix=0.1) if cityidx is None else CITY_MATS[(cityidx, col)][0]); topm = (C('#ffffff', 1.4, 1.2) if cityidx is None else CITY_MATS[(cityidx, col)][1])
        _raise_line(mb, [w_xy(u, v, ox, oy) for u, v in pts], 1.7, 0.55, mat, topm)
    for col, (u, v), (tx, ty) in stations_on(D):
        x, y = w_xy(u, v, ox, oy); nx, ny = -ty, tx
        obox(mb, V((x, y, 0.35)), V((nx, -ny * -1, 0)).normalized() if False else V((nx, ny, 0)), V((tx, ty, 0)), V((0, 0, 1)), 1.6, 0.28, 0.35, tick)
    for (u, v, nm) in D['rings']:
        x, y = w_xy(u, v, ox, oy)
        rod(mb, (x, y, 0.0), (x, y, 0.62), 4.3, wmat, seg=28); rod(mb, (x, y, 0.62), (x, y, 0.8), 3.1, rmat, seg=28)
    lp.done((ox, oy, 0.4), px=2.2)
    return tag

def build_mapworld(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(12)
    U.set_org(0, 0, 0); U.ensure_u()
    B.sun_light(P)
    # table (deep violet-blue desk) under everything
    g = U.Pt('table', ink=False); B.plane(g.mb, (-1600, -1600, -0.9), (3200, 0, 0), (0, 3200, 0), TX('farground' if False else 'pave', 0.5, 0.7, form=False), (0, 0, 60, 60)); g.done()
    # line materials per city (self-lit so they can light up one by one)
    cols_dim = dict(red='#7a1a20', blue='#13287a', green='#0a5a34', yellow='#8a6c10', brown='#4a2e14', black='#1a1830')
    for ci in range(len(CITIES)):
        for col in COL:
            CITY_MATS[(ci, col)] = (E('city%d_%s' % (ci, col), color=COL[col], k=1.6), E('cityt%d_%s' % (ci, col), color='#ffffff', k=1.8))
    build_sheet('LONDON', DIAGRAM, 0.0, 0.0, C, TX, E)
    for ci, (nm, (gx, gy), seed) in enumerate(CITIES):
        ox, oy = gx * (GW * CELL + 8), gy * (GH * CELL + 8)
        build_sheet(nm, city_diagram(seed), ox, oy, C, TX, E, cityidx=ci)
    build_bridges(C)
    # "CHANGE HERE" tag at the big ring (BANK), station tag signs, a few lamp posts
    x, y = w_xy(16, 9)
    for nm, (u, v, dy_) in (('CHANGE HERE', (16, 9, 7.2)),):
        U.utex('tag_change', lambda: BX.sign('CHANGE HERE', '#ffc81e', '#1a1840', border='#1a1840', w=900, h=260))
        tg = U.Pt('tag_change', (x, y + dy_, 3), ink=True); mb = tg.mb
        rod(mb, (x - 4.5, y + dy_, 0.5), (x - 4.5, y + dy_, 4.2), 0.18, C('#262050'), seg=6); rod(mb, (x + 4.5, y + dy_, 0.5), (x + 4.5, y + dy_, 4.2), 0.18, C('#262050'), seg=6)
        mb.quad(V((x - 5.0, y + dy_ - 0.2, 3.0)), V((10.0, 0, 0)), V((0, 0, 2.9)), E('tagc', 'tag_change', k=1.7), (0, 0, 1, 1)); tg.done((x, y + dy_, 3), px=2.5)
    # the tiny train (cars) on the RED line
    mk_train(C, TX, E); place_train(60.0)
    # tiny passengers around the BANK ring
    mk_passengers(rs)

CARS = []
def mk_train(C, TX, E, n=3):
    red = C('#e3262b', 1.2, 1.6); cream = C('#f6ecd0', 1.0, 1.2)
    win = E('twin', color='#ffe2a0', k=2.6)
    for i in range(n):
        p = U.Pt('car%d' % i, (0, 0, 1), ink=True); mb = p.mb
        mb.box((-0.75, -2.0, 0.55), (0.75, 2.0, 1.9), red); mb.box((-0.78, -2.0, 1.45), (0.78, 2.0, 1.58), cream); mb.box((-0.7, -2.0, 1.9), (0.7, 2.0, 2.05), C('#8a1018'))
        for sx in (-1, 1):
            x0 = 0.74 if sx > 0 else -0.8
            for j in range(3): mb.box((x0, -1.5 + j * 1.15, 1.0), (x0 + 0.06, -0.85 + j * 1.15, 1.65), win)
        if i == 0: mb.box((-0.55, 2.0, 0.9), (0.55, 2.05, 1.5), E('twin2', color='#fff4c4', k=3.2))
        CARS.append(p.done((0, 0, 1), px=2.2))

def red_path_ext():
    xy, cum = line_path('red'); xy = list(xy) + [(268.0, 0.0)]
    cum = [0.0]
    for a, b in zip(xy, xy[1:]): cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return xy, cum

def place_train(s, ext=False):
    xy, cum = red_path_ext() if ext else line_path('red')
    for i, ob in enumerate(CARS):
        (x, y), (tx, ty) = path_at(xy, cum, s - 4.6 * i)
        ob.location = (x, y, 0.4); ob.rotation_euler = (0, 0, math.atan2(ty, tx) - math.pi / 2)

PASS = []
def mk_passengers(rs):
    """Tiny cast22 crowd cards standing around the BANK interchange ring (scale 0.42 -> about 1.3 D tall)."""
    x0, y0 = w_xy(16, 9)
    spots = [(-3.0, 5.2), (3.5, 5.6), (-5.4, -5.0), (5.6, -4.6), (0.4, -6.4), (7.2, 2.4), (-7.0, 2.8), (2.6, 8.4), (-2.2, 8.0)]
    for i, (dx, dy) in enumerate(spots):
        U.crowd_card('mp%d' % i, i + 3, 'pass_walk', (x0 + dx, y0 + dy, 0.8), scale=0.42, rim='#ffd08a', shadow=True)


# ----------------------------------------------------------------------------- bridges (lines run off the London sheet onto the neighbours)
def build_bridges(C):
    """Straight bars from the edge of the London sheet across the gap onto the neighbouring sheets (the diagram style spreads)."""
    gx, gy = GW * CELL + 8, GH * CELL + 8
    br = U.Pt('bridges', (0, 0, 0.4), ink=True); mb = br.mb
    specs = [('red', [(120, 0), (gx, 0)]), ('green', [(120, 50), (gx, 50)]), ('blue', [(120, -80), (gx, -80)]), ('yellow', [(80, 80), (80, gy)]), ('brown', [(-120, 0), (-gx, 0)]), ('black', [(-120, 70), (-gx, 70)])]
    for col, pts in specs: _raise_line(mb, pts, 1.7, 0.55, C(COL[col], 1.15, 1.6, smix=0.1), C('#ffffff', 1.4, 1.2))
    br.done((0, 0, 0.4), px=2.2)

# ----------------------------------------------------------------------------- shots
def _cam_keys_ride():
    """s12: low behind the red train (3 cars), rising slightly; the keys are computed from the red path."""
    xy, cum = line_path('red'); keys = []
    for f in range(0, 75, 6):
        s = train_s12(f); sc = s - 11.0 - 0.0 * f
        (cx, cy), (tx, ty) = path_at(xy, cum, sc); (lx, ly), _ = path_at(xy, cum, s + 14)
        z = 3.2 + 3.4 * (f / 74.0) ** 1.2
        keys.append((f, (cx, cy, z), (lx, ly, 1.3), 24, 0.0))
    return keys

def train_s12(f):
    u = max(0.0, min(1.0, f / 60.0)); e = 0.45 * u + 0.55 * (1 - (1 - u) ** 2)
    return 22.0 + 150.0 * e

def _cam_keys_s14():
    return [(0, (60, 0, 4.2), (110, 0, 1.4), 24, 0.0), (18, (36, -6, 30), (150, 4, 6), 24, 0.0), (44, (-30, -120, 120), (110, 10, 4), 24, 0.0),
            (70, (-50, -300, 260), (40, 20, 0), 24, 0.0), (89, (-24, -340, 330), (0, 30, 0), 24, 0.0)]

def train_s14(f): return 210.0 + 44.0 * f / 89.0 + 0.0

def _s12_marks():
    x0, y0 = w_xy(16, 9)
    m = {'train': (path_at(*line_path('red'), 150.0)[0] + (0.4, 0.0)) if False else (x0 - 14, y0, 0.4, 0.0), 'ring': (x0, y0, 0.8, 0.0), 'tag_change': (x0, y0 + 7.2, 3.0, 0.0)}
    spots = [(-3.0, 5.2), (3.5, 5.6), (-5.4, -5.0), (5.6, -4.6), (0.4, -6.4), (7.2, 2.4), (-7.0, 2.8), (2.6, 8.4), (-2.2, 8.0)]
    for i, (dx, dy) in enumerate(spots): m['passenger_%d' % i] = (x0 + dx, y0 + dy, 0.8, 0.0)
    return m

def _anim_s12(f, n):
    place_train(train_s12(f)); U.face_cards()

def _anim_s14(f, n):
    place_train(train_s14(f), ext=True); set_city_diagrams(min(1.0, max(0.0, (f - 14) / 52.0))); U.face_cards()

def _loc_cam(): return dict(loc=(-60, -60, 8), look_at=(30, 0, 2), lens=24)

LOCATIONS = {'mapworld': dict(build=build_mapworld, light='MAPWORLD', sky=True, cam=_loc_cam())}
SHOTS = {
    's12': dict(location='mapworld', light='MAPWORLD', f0=1485, f1=1559, cam=_cam_keys_ride(), marks=_s12_marks(), state={'set_city_diagrams': 1.0}, animate={'train': _anim_s12}),
    's14': dict(location='mapworld', light='MAPWORLD', f0=1662, f1=1752, cam=_cam_keys_s14(), marks={'train': (210.0 - 130 + 0.0, 0.0, 0.4, 0.0)}, state={'set_city_diagrams': 0.0}, animate={'train': _anim_s14}),
}

# ----------------------------------------------------------------------------- setters
@B.setter('set_map_train')
def set_map_train(s): place_train(float(s))

CITY_OBJ = {}
@B.setter('set_city_diagrams')
def set_city_diagrams(k):
    """k 0..1: the other cities' diagrams light up one by one (city i is lit when k * N > i); lit = strength 1.8, unlit 0.35."""
    k = float(k); n = len(CITIES)
    for ci in range(n):
        u = max(0.0, min(1.0, k * n - ci)); st = 0.30 + 1.6 * (u * u * (3 - 2 * u))
        for col in COL:
            for m in CITY_MATS[(ci, col)]:
                nd = m.node_tree.nodes.get('strength')
                if nd: nd.inputs['Strength'].default_value = st * (1.0 if m is CITY_MATS[(ci, col)][0] else 1.2)
