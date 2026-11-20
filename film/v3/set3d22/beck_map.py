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

def paper_image(W=1560, H=1080, lw=0.2, title='UNDERGROUND', D=None, ring_names=True, lines=True, river=True, seed=3, paper='#f6ecd2'):
    """The pocket map / mapworld paper: cream, faint grid, pale river, the straight-line diagram with station ticks and ring names."""
    D = D or DIAGRAM; S = 1; cs = W / GW
    img = Image.new('RGB', (W, H), paper); rs = np.random.RandomState(seed)
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
B.LIGHTS['MAPWORLD'] = dict(B.LIGHTS['DUSK_CITY'], key=(1.2, 0.98, 0.7), key_dir=B.kdir(250, 24), shade=(0.14, 0.15, 0.46), shade_tint=(0.10, 0.11, 0.50), shade_mix=0.5,
                            lift=(0.02, 0.026, 0.08), grade_offset=(-0.004, -0.006, 0.0), grade_saturation=1.12)

CITY_MATS = {}
LINE_MATS = {}
HI_MAT = None
CITY_ROOT = {}

def _raise_line(mb, pts_xy, w, h, mat, top_mat, z0=0.0, hi_mat=None):
    for a, b in zip(pts_xy, pts_xy[1:]):
        U.seg_box(mb, (a[0], a[1], z0), (b[0], b[1], z0), w, h, mat)
        U.seg_box(mb, (a[0], a[1], z0 + h), (b[0], b[1], z0 + h), w * 0.72, 0.06, top_mat)
        if hi_mat is not None: U.seg_box(mb, (a[0], a[1], z0 + h + 0.06), (b[0], b[1], z0 + h + 0.06), w * 0.16, 0.04, hi_mat)
    for p in pts_xy:
        rod(mb, (p[0], p[1], z0), (p[0], p[1], z0 + h), w / 2, mat, seg=10)
        rod(mb, (p[0], p[1], z0 + h), (p[0], p[1], z0 + h + 0.06), w * 0.36, top_mat, seg=10)

def build_sheet(name, D, ox, oy, C, TX, E, lit=True, titles=True, cityidx=None, rot=0.0):
    """One diagram sheet at offset (ox, oy): paper plane, raised lines, rings, ticks."""
    k = ox * 0 + 1
    tag = name.replace(' ', '_')
    utex_name = 'paper_' + tag
    U.utex(utex_name, lambda: paper_image(1560, 1080, lw=0.2, title=name, D=D, river=(D is DIAGRAM), seed=abs(hash(tag)) % 97 if D is not DIAGRAM else 3))
    g = U.Pt('paper_' + tag, ink=False); B.plane(g.mb, (ox - GW * CELL / 2, oy - GH * CELL / 2, 0.0), (GW * CELL, 0, 0), (0, GH * CELL, 0), E('pp_' + tag, utex_name, k=0.5), (0, 0, 1, 1)); g.done()
    # frame of the sheet: slightly raised cream border so the sheets read as papers laid on the table
    fr = U.Pt('paperedge_' + tag, (ox, oy, 0), ink=True, hd=70); mb = fr.mb; ec = C('#e8dcb8', 1.0, 1.4)
    mb.box((ox - GW * CELL / 2 - 0.6, oy - GH * CELL / 2 - 0.6, -0.5), (ox + GW * CELL / 2 + 0.6, oy - GH * CELL / 2, 0.15), ec)
    mb.box((ox - GW * CELL / 2 - 0.6, oy + GH * CELL / 2, -0.5), (ox + GW * CELL / 2 + 0.6, oy + GH * CELL / 2 + 0.6, 0.15), ec)
    mb.box((ox - GW * CELL / 2 - 0.6, oy - GH * CELL / 2, -0.5), (ox - GW * CELL / 2, oy + GH * CELL / 2, 0.15), ec)
    mb.box((ox + GW * CELL / 2, oy - GH * CELL / 2, -0.5), (ox + GW * CELL / 2 + 0.6, oy + GH * CELL / 2, 0.15), ec)
    fr.done((ox, oy, 0), px=2.5)
    lp = U.Pt('lines_' + tag, (ox, oy, 0.4), ink=True, hd=40); mb = lp.mb
    tick = C('#1a1840', 1.0, 1.0); wmat = C('#ffffff', 1.1, 1.2); rmat = C('#f6ecd2', 1.0, 1.0)
    for col, pts in D['lines']:
        mat, topm = LINE_MATS[col] if cityidx is None else CITY_MATS[(cityidx, col)]
        _raise_line(mb, [w_xy(u, v, ox, oy) for u, v in pts], 2.6, 0.7, mat, topm, hi_mat=HI_MAT)
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
    g = U.Pt('table', ink=False); B.plane(g.mb, (-1300, -1300, -0.9), (2600, 0, 0), (0, 2600, 0), E('table_wood', 'wood_dark', k=0.75), (0, 0, 22, 22)); g.done()
    build_table_props(C, TX, E)
    # line materials per city (self-lit so they can light up one by one)
    global HI_MAT
    HI_MAT = E('line_hi', color='#fff6e0', k=2.2)
    for col in COL: LINE_MATS[col] = (E('line_%s' % col, color=COL[col], k=0.8), E('linetop_%s' % col, color=COL[col], k=1.55))
    for ci in range(len(CITIES)):
        for col in COL:
            CITY_MATS[(ci, col)] = (E('city%d_%s' % (ci, col), color=COL[col], k=0.8), E('cityt%d_%s' % (ci, col), color=COL[col], k=1.55))
    build_sheet('LONDON', DIAGRAM, 0.0, 0.0, C, TX, E)
    for ci, (nm, (gx, gy), seed) in enumerate(CITIES):
        ox, oy = gx * (GW * CELL + 8), gy * (GH * CELL + 8)
        build_sheet(nm, city_diagram(seed), ox, oy, C, TX, E, cityidx=ci)
    build_bridges(C)
    # "CHANGE HERE" tag at the big ring (BANK), station tag signs, a few lamp posts
    x, y = w_xy(16, 9)
    for nm, (u, v, dy_) in (('CHANGE HERE', (16, 9, 7.2)),):
        U.utex('tag_change', lambda: BX.sign('CHANGE HERE', '#ffc81e', '#1a1840', border='#1a1840', w=900, h=260))
        tg = U.Pt('tag_change', (x, y + dy_, 3), ink=True, hd=40); mb = tg.mb
        rod(mb, (x - 4.5, y + dy_, 0.5), (x - 4.5, y + dy_, 4.2), 0.18, C('#262050'), seg=6); rod(mb, (x + 4.5, y + dy_, 0.5), (x + 4.5, y + dy_, 4.2), 0.18, C('#262050'), seg=6)
        mb.quad(V((x - 5.0, y + dy_ - 0.2, 3.0)), V((10.0, 0, 0)), V((0, 0, 2.9)), E('tagc', 'tag_change', k=1.7), (0, 0, 1, 1)); tg.done((x, y + dy_, 3), px=2.5)
    # the tiny train (cars) on the RED line
    mk_train(C, TX, E); place_train(60.0)
    # tiny passengers around the BANK ring
    mk_passengers(rs); mk_line_trains(C, TX, E); mk_stations(C, TX, E); mk_ring_crowds()

CARS = []
def mk_train(C, TX, E, n=3):
    red = E('trainred', color='#ff5a3a', k=1.05); cream = E('traincream', color='#f6ecd0', k=0.9)
    win = E('twin', color='#ffe2a0', k=2.6)
    for i in range(n):
        p = U.Pt('car%d' % i, (0, 0, 1), ink=True, hd=12); mb = p.mb
        mb.box((-0.75, -2.0, 0.55), (0.75, 2.0, 1.9), red); mb.box((-0.78, -2.0, 1.45), (0.78, 2.0, 1.58), cream); mb.box((-0.7, -2.0, 1.9), (0.7, 2.0, 2.05), E('trainroof', color='#a01820', k=0.9))
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
    br = U.Pt('bridges', (0, 0, 0.4), ink=True, hd=40); mb = br.mb
    specs = [('red', [(120, 0), (gx, 0)]), ('green', [(120, 50), (gx, 50)]), ('blue', [(120, -80), (gx, -80)]), ('yellow', [(80, 80), (80, gy)]), ('brown', [(-120, 0), (-gx, 0)]), ('black', [(-120, 70), (-gx, 70)])]
    for col, pts in specs: _raise_line(mb, pts, 1.7, 0.55, LINE_MATS[col][0], LINE_MATS[col][1], hi_mat=HI_MAT)
    br.done((0, 0, 0.4), px=2.2)

# ----------------------------------------------------------------------------- shots
def _cam_keys_ride():
    """s12: low behind the red train (3 cars), rising slightly; the keys are computed from the red path."""
    xy, cum = line_path('red'); keys = []
    for f in range(0, 75, 6):
        s = train_s12(f); sc = s - 25.0
        (cx, cy), (tx, ty) = path_at(xy, cum, sc); (lx, ly), _ = path_at(xy, cum, s + 16)
        z = 5.0 + 4.0 * (f / 74.0) ** 1.2
        keys.append((f, (cx, cy, z), (lx, ly, -5.0), 22, 0.0))
    return keys

def train_s12(f):
    u = max(0.0, min(1.0, f / 60.0)); e = 0.45 * u + 0.55 * (1 - (1 - u) ** 2)
    return 22.0 + 150.0 * e

def _cam_keys_s14():
    return [(0, (60, 0, 4.2), (110, 0, 1.4), 24, 0.0), (18, (36, -6, 30), (150, 4, 6), 24, 0.0), (44, (-30, -120, 120), (110, 10, 4), 24, 0.0),
            (70, (-50, -300, 260), (40, 20, 0), 24, 0.0), (89, (-30, -300, 250), (0, 150, 10), 24, 0.0)]

def train_s14(f): return 210.0 + 44.0 * f / 89.0 + 0.0

def _s12_marks():
    x0, y0 = w_xy(16, 9)
    m = {'train': (path_at(*line_path('red'), 150.0)[0] + (0.4, 0.0)) if False else (x0 - 14, y0, 0.4, 0.0), 'ring': (x0, y0, 0.8, 0.0), 'tag_change': (x0, y0 + 7.2, 3.0, 0.0)}
    spots = [(-3.0, 5.2), (3.5, 5.6), (-5.4, -5.0), (5.6, -4.6), (0.4, -6.4), (7.2, 2.4), (-7.0, 2.8), (2.6, 8.4), (-2.2, 8.0)]
    for i, (dx, dy) in enumerate(spots): m['passenger_%d' % i] = (x0 + dx, y0 + dy, 0.8, 0.0)
    return m

def _anim_s12(f, n):
    place_train(train_s12(f)); place_line_trains(f); U.face_cards()

def _anim_s14(f, n):
    place_train(train_s14(f), ext=True); place_line_trains(f); set_city_diagrams(min(1.0, max(0.0, (f - 14) / 52.0))); U.face_cards()

def _loc_cam(): return dict(loc=(-60, -60, 8), look_at=(30, 0, 2), lens=24)

LOCATIONS = {'mapworld': dict(build=build_mapworld, light='MAPWORLD', sky=False, cam=_loc_cam())}
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
        u = max(0.0, min(1.0, k * n - ci)); st = 0.35 + 2.8 * (u * u * (3 - 2 * u))
        for col in COL:
            for m in CITY_MATS[(ci, col)]:
                nd = m.node_tree.nodes.get('strength')
                if nd: nd.inputs['Strength'].default_value = st * (1.0 if m is CITY_MATS[(ci, col)][0] else 1.2)


# ----------------------------------------------------------------------------- Beck's drafting table: the far edge of the world
def build_table_props(C, TX, E):
    pr = U.Pt('table_props', (0, 0, 40), ink=True, hd=60); mb = pr.mb
    def bottle(x, y, col, hexc):
        rod(mb, (x, y, 0), (x, y, 70), 34, E('ink_%s' % col, color=hexc, k=0.9), seg=20)
        rod(mb, (x, y, 70), (x, y, 88), 14, C('#1a1a50'), seg=14); rod(mb, (x, y, 88), (x, y, 104), 17, C('#0e0e30'), seg=14)
        mb.box((x - 18, y - 36, 22), (x + 18, y - 35, 52), C('#f6ecd0', 1.2, 1.2))
    for k, (x, y, col) in enumerate(((470, -150, 'red'), (500, -60, 'blue'), (480, 40, 'green'), (505, 140, 'yellow'))): bottle(x, y, col, COL[col])
    for k, (x, y, col) in enumerate(((-120, -430, 'blue'), (-20, -450, 'red'))): bottle(x, y, col, COL[col])
    # giant set square (amber) and ruler standing like monuments on the west side
    A = [V((-480, -40, 0)), V((-480, 120, 0)), V((-480, -40, 0)) + V((0, 0, 0))]
    from mine import obox as ob_
    ob_(mb, V((-470, 40, 70)), V((0, 1, 0)), V((1, 0, 0)), V((0, 0, 1)), 90, 8, 70, C('#c8793a', 1.3, 1.5))
    ob_(mb, V((-470, 40, 150)), V((0, 1, 0)), V((1, 0, 0)), V((0, 0, 1)), 60, 7, 12, C('#c8793a', 1.3, 1.5))
    ob_(mb, V((-470, -140, 120)), V((0, 1, 0)), V((1, 0, 0)), V((0, 0, 1)), 12, 7, 120, C('#f2d48a', 1.3, 1.4))
    for t in range(14): mb.box((-478, -150 + 0.0, 5 + t * 17), (-462, -131, 7 + t * 17), C('#1a1840'))
    pr.done((0, 0, 40), px=3)
    # the green banker's lamp far to the north-east: a warm sun
    lp = U.Pt('giant_lamp', (560, 420, 150), ink=True, hd=80); mb = lp.mb
    rod(mb, (560, 420, 0), (560, 420, 200), 9, C('#1a1a50')); rod(mb, (560, 420, 0), (560, 420, 14), 40, C('#1a1a50'), seg=16)
    mb.frustum((560, 420, 215), (560, 420, 150), 26, 96, C('#12a15a', 1.4, 1.6, smix=0.2), seg=24, cap0=True, cap1=False); mb.sphere((560, 420, 165), 22, E('lamp_bulb', color='#fff0b0', k=2.2), seg=14, rings=8)
    lp.done((560, 420, 150), px=3)
    gh = U.Pt('lamp_halo', ink=False, shadow=False); B.halo_card(gh.mb, (560, 420, 155), 190, E('lamp_halo', 'halo_warm', k=1.2, additive=True)); gh.done()
    U.pl('lamp_sun', (560, 400, 140), (1.0, 0.75, 0.4), 4000000, 20.0)
    # the dark-blue night window: four big night-city walls (the HQ and its roundel across the street)
    for k, (p0, pu) in enumerate((((1250, -1250, 0), (0, 2500, 0)), ((1250, 1250, 0), (-2500, 0, 0)), ((-1250, 1250, 0), (0, -2500, 0)), ((-1250, -1250, 0), (2500, 0, 0)))):
        w = U.Pt('nightwall%d' % k, ink=False, shadow=False); w.mb.pid += 1
        a = V(p0); b = a + V(pu); up = V((0, 0, 1100))
        w.mb.face([a, b, b + up, a + up], E('nightwall%d' % k, 'night_city', k=1.0), [(1, 0.0), (0, 0.0), (0, 1), (1, 1)]); w.done()

def mk_line_trains(C, TX, E):
    for col, s0 in (('blue', 70.0), ('green', 110.0), ('yellow', 60.0), ('brown', 40.0), ('black', 70.0), ('red', 190.0)):
        mat = E('lt_%s' % col, color=COL[col] if col != 'black' else '#6a6aa8', k=1.0); win = E('twin', color='#ffe2a0', k=2.6)
        for i in range(2):
            p = U.Pt('lt_%s_%d' % (col, i), (0, 0, 1), ink=True, hd=14); mb = p.mb
            mb.box((-0.75, -2.0, 0.55), (0.75, 2.0, 1.9), mat); mb.box((-0.7, -2.0, 1.9), (0.7, 2.0, 2.05), E('ltr', color='#fff6e0', k=0.9))
            for sx in (-1, 1):
                x0 = 0.74 if sx > 0 else -0.8
                for j in range(3): mb.box((x0, -1.5 + j * 1.15, 1.0), (x0 + 0.06, -0.85 + j * 1.15, 1.65), win)
            LTRAINS.append((p.done((0, 0, 1), px=2.2), col, s0, i))
    place_line_trains(0)

LTRAINS = []
def place_line_trains(f):
    for ob, col, s0, i in LTRAINS:
        xy, cum = line_path(col); (x, y), (tx, ty) = path_at(xy, cum, (s0 + f * 0.9 - 4.6 * i) % cum[-1])
        ob.location = (x, y, 0.4); ob.rotation_euler = (0, 0, math.atan2(ty, tx) - math.pi / 2)

def mk_stations(C, TX, E):
    pt = U.Pt('platforms', (0, 0, 0.2), ink=True, hd=30); mb = pt.mb; cream = C('#f6ecd0', 1.1, 1.3); names = []
    for k, (col, (u, v), (tx, ty)) in enumerate(stations_on()):
        x, y = w_xy(u, v); nx, ny = -ty, tx; side = 1 if k % 2 else -1
        px, py = x + nx * side * 3.4, y + ny * side * 3.4
        obox(mb, V((px, py, 0.18)), V((nx, ny, 0)), V((tx, ty, 0)), V((0, 0, 1)), 1.0, 2.0, 0.18, cream)
        if k % 3 == 0 and len(names) < 12: names.append((px, py, DIAGRAM['stations'][k % len(DIAGRAM['stations'])]))
    pt.done((0, 0, 0.2), px=2.2)
    tg = U.Pt('name_tags', ink=True, hd=40); mb = tg.mb
    for k, (x, y, nm) in enumerate(names):
        U.utex('tag_%s' % nm.replace(' ', '_'), lambda nm=nm: BX.sign(nm, '#f6ecd0', '#1a1840', border='#1a1840', w=700, h=200))
        rod(mb, (x, y, 0.3), (x, y, 1.6), 0.1, C('#262050'), seg=5)
        mb.pid += 1; mb.face([V((x - 2.4, y, 1.5)), V((x + 2.4, y, 1.5)), V((x + 2.4, y, 2.7)), V((x - 2.4, y, 2.7))], E('tag%d' % k, 'tag_%s' % nm.replace(' ', '_'), k=1.5), [(0, 0), (1, 0), (1, 1), (0, 1)])
    tg.done((0, 0, 2), px=2.2)

def mk_ring_crowds():
    for (u, v) in ((21, 9), (16, 6), (9, 14)):
        x0, y0 = w_xy(u, v)
        for i, (dx, dy) in enumerate(((-2.4, 2.8), (2.6, 3.0), (-3.0, -2.4), (3.1, -2.2), (0.2, 4.4))):
            U.crowd_card('mp%d' % (i + 9 * (u % 3)), i + 5 + u, 'pass_walk', (x0 + dx, y0 + dy, 0.8), scale=0.42, rim='#ffd08a', shadow=True)
