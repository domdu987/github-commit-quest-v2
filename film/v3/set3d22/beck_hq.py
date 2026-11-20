"""beck_hq.py (builder A): Beck's lodgings (NIGHT), the HQ corridor and the publicity department (EVENING / NIGHT).
Locations: 'lodgings', 'hq_corridor', 'publicity'. Shots: s01, s04, s05 (lodgings) s06, s07 (publicity) s08 (corridor). See API.md."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector as V
import beck as B
from beck import (STATE, Part, plane, facing_card, halo_card, point_light, spot_light, pitched, cast_card, setter, SETTERS, T, obox, rod, lumpy, MB, hull_at)
import beck_london as L

X, Y, Z = V((1, 0, 0)), V((0, 1, 0)), V((0, 0, 1))
RED, BLUE, GREEN, YELLOW = '#e3262b', '#1f49c8', '#12a15a', '#ffc81e'

# ----------------------------------------------------------------------------- lights (added to the shared presets)
B.LIGHTS['HQ_EVENING'] = dict(B.LIGHTS['LODGINGS'], shade=(0.10, 0.14, 0.44), shade_tint=(0.07, 0.13, 0.54), shade_mix=0.88, lift=(0.010, 0.016, 0.058), grade_saturation=1.28)
B.LIGHTS['HQ_NIGHT'] = dict(B.LIGHTS['HQ_EVENING'], shade=(0.08, 0.12, 0.46), lift=(0.006, 0.012, 0.060))

# ============================================================================= LODGINGS
RW, BW, LW, CE = 10.0, 14.0, -10.0, 9.6                    # right wall x, back wall y, left wall x, ceiling z
BOARD_C = V((2.4, 8.0, 2.5)); LZ = 0.54; BTH = math.radians(56)       # drafting board centre and tilt
BU = V((0, math.cos(BTH), math.sin(BTH))); BN = V((0, -math.sin(BTH), math.cos(BTH)))
HW, HS = 3.05, 2.3                                         # board half sizes (x, along the slope)
PAPER = (5.5, 3.94)
CAM_LODGE = dict(loc=(-1.0, -9.5, 5.0), look_at=(1.2, 9.0, 3.0), lens=30)

def board_pt(u, v, lift=0.0):
    """Board paper coordinates (u right, v up the slope, paper centre 0,0; paper 5.5 x 3.94) -> world."""
    return BOARD_C + BN * (0.115 + lift) + X * u + BU * v

# diagram state: per line completeness 0..1, bend angle (deg) of the green diagonal, squeeze 0..1 of the yellow stations, ruler on/off, pen position
LINE_ORDER = ('red', 'blue', 'green', 'yellow')
DIAG = dict(red=1.0, blue=1.0, green=1.0, yellow=1.0, bend=45.0, squeeze=0.0, ruler=None, hot=None)
LCOL = dict(red=RED, blue=BLUE, green=GREEN, yellow=YELLOW)

def line_pts(name, bend=45.0, squeeze=0.0):
    a = math.radians(bend)
    if name == 'red': return [(-2.45, -1.15), (-0.7, -1.15), (0.4, -0.05), (2.45, -0.05)]
    if name == 'blue': return [(-1.55, -1.8), (-1.55, 0.95), (-0.65, 1.85)]
    if name == 'green':
        bx, by = 0.0, 1.0; L_ = 1.55; ex = bx + L_ * math.cos(a); ey = by - L_ * math.sin(a)
        return [(-2.45, 1.0), (bx, by), (ex, ey), (ex, -1.8)]
    if name == 'yellow':
        top = 1.75 - 0.85 * squeeze; bot = -1.8 + 0.7 * squeeze
        return [(2.0, bot), (2.0, top)]
def poly_len(pts): return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
def poly_cut(pts, frac):
    """First `frac` of the polyline -> list of points."""
    tot = poly_len(pts) * max(0.0, min(1.0, frac)); out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        d = math.dist(a, b)
        if tot >= d: out.append(b); tot -= d
        else:
            if tot > 1e-6: out.append((a[0] + (b[0] - a[0]) * tot / d, a[1] + (b[1] - a[1]) * tot / d))
            break
    return out
def seg_isect(p, q, r, s):
    d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
    if abs(d) < 1e-9: return None
    t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d; u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / d
    return (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])) if 0 <= t <= 1 and 0 <= u <= 1 else None

def rebuild_diagram():
    """(Re)build the drawn lines, ticks, interchange rings of the board from DIAG. Called by the setters."""
    for n in ('diagram_lines', 'diagram_rings'):
        o = bpy.data.objects.get(n)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    E = STATE['E']; dl = Part('diagram_lines', ink=False, shadow=False); mb = dl.mb; W = 0.15
    full = {n: line_pts(n, DIAG['bend'], DIAG['squeeze']) for n in LINE_ORDER}
    drawn = {n: poly_cut(full[n], DIAG[n]) for n in LINE_ORDER}
    def P(p, lift): return board_pt(p[0], p[1], lift)
    def quad(p0, p1, w, lift, mat):
        d = V((p1[0] - p0[0], p1[1] - p0[1], 0)); 
        if d.length < 1e-6: return
        d.normalize(); nx, ny = -d.y, d.x
        pts = [P((p0[0] + nx * w / 2, p0[1] + ny * w / 2), lift), P((p1[0] + nx * w / 2, p1[1] + ny * w / 2), lift), P((p1[0] - nx * w / 2, p1[1] - ny * w / 2), lift), P((p0[0] - nx * w / 2, p0[1] - ny * w / 2), lift)]
        mb.pid += 1; mb.face(pts, mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    def disc(c, r, lift, mat, n=14):
        mb.pid += 1; mb.face([P((c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)), lift) for i in range(n)], mat, [(0, 0)] * n)
    ink = E('dg_ink', color='#1a1840', k=0.8)
    for i, n in enumerate(LINE_ORDER):
        pts = drawn[n]; lift = 0.02 + 0.006 * i; mat = E('dg_' + n, color=LCOL[n], k=1.25)
        if len(pts) < 2: continue
        for a, b in zip(pts, pts[1:]): quad(a, b, W, lift, mat)
        for p in pts: disc(p, W / 2, lift, mat)
        tot = poly_len(pts); k = 0.0                                   # station ticks every 0.62
        while k < tot:
            acc = 0.0
            for a, b in zip(pts, pts[1:]):
                d = math.dist(a, b)
                if acc + d >= k:
                    t = (k - acc) / d; c = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t); dx, dy = (b[0] - a[0]) / d, (b[1] - a[1]) / d
                    quad((c[0] - dy * 0.17, c[1] + dx * 0.17), (c[0] + dy * 0.17, c[1] - dx * 0.17), 0.045, lift + 0.003, ink); break
                acc += d
            k += 0.62
    rings = []
    for i, a in enumerate(LINE_ORDER):
        for b in LINE_ORDER[i + 1:]:
            for p, q in zip(drawn[a], drawn[a][1:]):
                for r_, s_ in zip(drawn[b], drawn[b][1:]):
                    c = seg_isect(p, q, r_, s_)
                    if c: rings.append(c)
    for c in rings: disc(c, 0.235, 0.05, ink, 18); disc(c, 0.17, 0.056, E('dg_white', color='#ffffff', k=1.2), 18)
    # the pen tip / hot end of the line being drawn
    if DIAG['hot']:
        n = DIAG['hot']; pts = drawn[n]
        if len(pts) >= 2: disc(pts[-1], 0.1, 0.06, E('dg_hot', color='#1a1840', k=0.9), 10)
    dl.done()
    if DIAG['ruler'] is not None:
        ang, cx, cy = DIAG['ruler']; rl = Part('diagram_ruler', ink=True, shadow=True); a = math.radians(ang)
        c = board_pt(cx, cy, 0.09); ax = (X * math.cos(a) + BU * math.sin(a)); ay = (-X * math.sin(a) + BU * math.cos(a))
        obox(rl.mb, c, ax, ay, BN, 1.25, 0.11, 0.035, STATE['C']('#e8b86a', 1.1, 1.5)); rl.done(tuple(c), px=2.5)

@setter('line_progress')
def set_line_progress(k, order=LINE_ORDER, hot=None):
    """k 0..len(order): lines drawn one after the other in `order` (red, blue, green, yellow by default); the integer part = finished lines.
    `hot` = name of the line whose end carries the pen dot. Lines not in order keep their value."""
    for i, n in enumerate(order): DIAG[n] = max(0.0, min(1.0, k - i))
    DIAG['hot'] = hot or (order[min(len(order) - 1, int(k))] if 0 < k < len(order) else None)
    rebuild_diagram()

@setter('line')
def set_line(name, frac=1.0, hot=False):
    """One line directly: set_line('blue', 0.4)."""
    DIAG[name] = frac; DIAG['hot'] = name if hot else DIAG['hot']; rebuild_diagram()
@setter('bend45')
def set_bend45(t):
    """45 degree bend event of the GREEN diagonal: t 0 = a floppy 27 deg, t 1 = exactly 45 deg (the set square lands)."""
    DIAG['bend'] = 27.0 + 18.0 * max(0.0, min(1.0, t)); rebuild_diagram()
@setter('station_squeeze')
def set_station_squeeze(k):
    """The far stations of the YELLOW line slide inward (the line shortens): k 0..1."""
    DIAG['squeeze'] = max(0.0, min(1.0, k)); rebuild_diagram()
@setter('ruler')
def set_ruler(v):
    """None = off, or (angle_deg, u, v) on the paper: the boxwood ruler lying at that angle."""
    DIAG['ruler'] = v; rebuild_diagram()
@setter('diagram')
def set_diagram(d):
    DIAG.update(d); rebuild_diagram()
def reset_diagram(**kw):
    DIAG.update(dict(red=1.0, blue=1.0, green=1.0, yellow=1.0, bend=45.0, squeeze=0.0, ruler=None, hot=None)); DIAG.update(kw)

def build_lodgings(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(5)
    wp = TX('wallpaper', 1.0, 1.0); wpb = TX('wallpaper_b', 1.0, 1.0); wd = C('#7a3a1a'); wood = C('#8a4a22'); dwood = C('#5a2c12'); cream = C('#e8dcc0', 1.0, 1.4)
    r = Part('room', (0, 7, 3), ink=False); mb = r.mb
    plane(mb, (LW, -12, 0), (20, 0, 0), (0, 26, 0), TX('wood', 1.0, 1.0), (0, 0, 7, 9))
    plane(mb, (LW, BW, 0), (20, 0, 0), (0, 0, CE), wp, (0, 0, 7, 3.0)); plane(mb, (RW, -12, 0), (0, 26, 0), (0, 0, CE), wpb, (0, 0, 8, 3.0))
    plane(mb, (LW, -12, 0), (0, 26, 0), (0, 0, CE), wp, (0, 0, 8, 3.0)); plane(mb, (LW, -12, CE), (20, 0, 0), (0, 26, 0), C('#b8743a', 0.55, 1.0), (0, 0, 1, 1))
    plane(mb, (LW, -12.05, 0), (20, 0, 0), (0, 0, CE), wp, (0, 0, 7, 3.0))      # wall behind the camera (for arcs)
    r.done()
    rug = Part('rug', ink=False); plane(rug.mb, (-7.0, -1.5, 0.03), (11.0, 0, 0), (0, 12.5, 0), TX('rag_rug', 0.62, 1.0), (0, 0, 1, 1)); rug.done()
    sk = Part('skirting', (0, 14, 0.4)); mb = sk.mb
    mb.box((LW, BW - 0.3, 0), (RW, BW, 0.8), wd); mb.box((RW - 0.3, -12, 0), (RW, BW, 0.8), wd); mb.box((LW, -12, 0), (LW + 0.3, BW, 0.8), wd)
    mb.box((LW, BW - 0.2, CE - 1.0), (RW, BW, CE - 0.75), wd); mb.box((LW, BW - 0.3, CE - 0.45), (RW, BW, CE), C('#e8d8ae'))
    sk.done((0, 14, 0.4), px=2)
    # ---- night window with the HQ and the roundel across the street, curtains, sill
    wx0, wx1, wz0, wz1 = 4.5, 8.7, 2.8, 7.2
    wn = Part('window_view', ink=False, shadow=False); plane(wn.mb, (wx0, BW - 0.05, wz0), (wx1 - wx0, 0, 0), (0, 0, wz1 - wz0), E('nightcity', 'night_city', k=1.15), (0.0, 0.0, 0.56, 0.78)); wn.done()
    wf = Part('window_frame', (6.6, 14, 5)); mb = wf.mb; wfm = C('#e8dcc0')
    mb.box((wx0 - 0.4, BW - 0.5, wz0 - 0.4), (wx1 + 0.4, BW + 0.1, wz0), wfm); mb.box((wx0 - 0.4, BW - 0.5, wz1), (wx1 + 0.4, BW + 0.1, wz1 + 0.4), wfm)
    mb.box((wx0 - 0.4, BW - 0.5, wz0), (wx0, BW + 0.1, wz1), wfm); mb.box((wx1, BW - 0.5, wz0), (wx1 + 0.4, BW + 0.1, wz1), wfm)
    xm = (wx0 + wx1) / 2; mb.box((xm - 0.1, BW - 0.4, wz0), (xm + 0.1, BW, wz1), wfm); mb.box((wx0, BW - 0.4, (wz0 + wz1) / 2 - 0.1), (wx1, BW, (wz0 + wz1) / 2 + 0.1), wfm)
    mb.box((wx0 - 0.9, BW - 1.0, wz0 - 0.7), (wx1 + 0.9, BW - 0.2, wz0 - 0.4), wfm)
    for a, b in ((wx0 - 1.5, wx0 + 0.1), (wx1 - 0.1, wx1 + 1.5)): mb.box((a, BW - 1.1, wz0 - 0.5), (b, BW - 0.5, wz1 + 0.9), C('#c4272f', 1.0, 1.4))
    mb.box((wx0 - 1.9, BW - 1.3, wz1 + 0.8), (wx1 + 1.9, BW - 0.6, wz1 + 1.1), C('#6a3a1a'))
    wf.done((6.6, 14, 5), px=2.5)
    # ---- the OLD tangled map (framed, back wall, left) and the cork board of circuits (back wall, middle-left)
    om = Part('old_map', (-6.1, 14, 4.7)); mb = om.mb; mb.box((-8.25, BW - 0.3, 2.95), (-3.95, BW, 6.25), C('#6a3a1a', 1.0, 1.5)); om.done((-6.1, 14, 4.7), px=2.5)
    omp = Part('old_map_img', ink=False); plane(omp.mb, (-8.05, BW - 0.34, 3.15), (3.9, 0, 0), (0, 0, 2.9), TX('old_map', 1.15, 1.0, glow='old_map', glow_k=0.55), (0, 0, 1, 1)); omp.done()
    cb = Part('cork', (-1.2, 14, 4.8)); mb = cb.mb; mb.box((-3.5, BW - 0.3, 3.0), (1.1, BW, 6.6), C('#5a2f14')); cb.done((-1.2, 14, 4.8), px=2.5)
    cbp = Part('cork_img', ink=False); plane(cbp.mb, (-3.3, BW - 0.34, 3.2), (4.2, 0, 0), (0, 0, 3.2), TX('cork', 1.1, 1.0, glow='cork', glow_k=0.4), (0, 0, 1, 1)); cbp.done()
    for i, (x0, z0, w_, h_) in enumerate(((-3.1, 4.2, 1.5, 1.1), (-1.3, 3.5, 1.5, 1.1), (-2.8, 5.3, 1.4, 1.0), (-0.9, 5.0, 1.6, 1.15))):
        c = Part('pinned%d' % i, ink=True); plane(c.mb, (x0, BW - 0.38, z0), (w_, 0, 0), (0, 0, h_), TX('circuit%d' % (i % 3), 1.1, 1.0, glow='circuit%d' % (i % 3), glow_k=0.35), (0, 0, 1, 1)); c.done((x0, BW, z0), px=2)
    sh = Part('shelf', (-1.2, 13.5, 8.2)); mb = sh.mb; mb.box((-3.6, BW - 1.0, 7.4), (1.2, BW, 7.65), wd)
    for i in range(11): bh = 0.8 + rs.random() * .5; mb.box((-3.4 + i * 0.4, BW - 0.8, 7.65), (-3.4 + i * 0.4 + 0.34, BW - 0.2, 7.65 + bh), C(rs.choice(['#e3262b', '#1f49c8', '#12a15a', '#ffc81e', '#7a3a8a', '#d8d0b0']), 1.0, 1.5))
    sh.done((-1.2, 13.5, 8), px=2.5)
    # framed Underground poster and a calendar on the left wall (period dressing)
    pst = Part('wall_posters', ink=True); mb = pst.mb
    for i, (y0, z0) in enumerate(((3.0, 3.2), (8.0, 4.0))):
        mb.pid += 1; mb.face([V((LW + 0.08, y0, z0)), V((LW + 0.08, y0 + 2.4, z0)), V((LW + 0.08, y0 + 2.4, z0 + 3.2)), V((LW + 0.08, y0, z0 + 3.2))], TX('poster%d' % (i + 1), 1.0, 1.0, glow='poster%d' % (i + 1), glow_k=0.3), [(0, 0), (1, 0), (1, 1), (0, 1)])
    pst.done((LW, 6, 5), px=2)
    # ---- drafting board (tilted), legs, ledge, small ink bottles, T-square, set squares
    db = Part('drafting_board', tuple(BOARD_C)); mb = db.mb; c0 = BOARD_C; bx = c0.x
    obox(mb, c0, X, BU, BN, HW + 0.1, HS + 0.1, 0.1, wood)
    for sx in (-1, 1):
        rod(mb, c0 + X * (2.7 * sx) - BU * 1.6 - BN * 0.2, V((bx + 3.1 * sx, 6.2, 0.0)), 0.16, dwood, seg=6); rod(mb, c0 + X * (2.5 * sx) + BU * 1.2 - BN * 0.2, V((bx + 3.0 * sx, 12.0, 0.0)), 0.16, dwood, seg=6)
    mb.box((bx - 3.0, 6.1, LZ - 0.14), (bx + 3.0, 6.9, LZ), wood)
    db.done(tuple(c0), px=3)
    pap = Part('diagram_paper', ink=False); pap.mb.quad(board_pt(-2.75, -1.97, -0.0), X * 5.5, BU * 3.94, TX('paper_grid', 1.0, 1.0, glow='paper_grid', glow_k=0.25), (0, 0, 1, 1)); pap.done()
    ts = Part('tools', tuple(c0)); mb = ts.mb
    obox(mb, c0 + BN * 0.19 + BU * 1.7, X, BU, BN, 2.9, 0.1, 0.04, C('#c8793a', 1.2, 1.3)); obox(mb, c0 + BN * 0.19 + BU * 1.7 - X * 2.85, X, BU, BN, 0.22, 0.9, 0.06, C('#4a2410'))   # T-square
    for sx_, col in ((bx + 2.5, '#38d68a'), (bx + 3.3, '#56e0ff')):
        p = [V((sx_, 6.2, LZ + 0.02)), V((sx_ + 0.7, 6.2, LZ + 0.02)), V((sx_, 6.8, LZ + 0.02))]; mb.pid += 1; mb.face(p, C(col, 1.5, 1.5))
    for i, col in enumerate((RED, BLUE, GREEN, YELLOW)):                                                # small ink bottles (0.35x)
        ix = bx - 1.3 + i * 0.7; rod(mb, (ix, 6.5, LZ), (ix, 6.5, LZ + 0.28), 0.13, C('#222244', 1.0, 1.3), seg=10); rod(mb, (ix, 6.5, LZ), (ix, 6.5, LZ + 0.21), 0.115, C(col, 1.6, 2.0, smix=0.2), seg=10); rod(mb, (ix, 6.5, LZ + 0.28), (ix, 6.5, LZ + 0.4), 0.06, C(col, 1.2, 1.6, smix=0.2), seg=8)
    mb.box((bx - 2.5, 6.15, LZ), (bx - 1.7, 6.7, LZ + 0.08), C('#f6ecd0'))                                   # a pad of paper on the ledge
    ts.done((bx, 7, 2), px=2.5)
    # ---- lamp (green shade, left of the board), pendant, kettle, coat, stove, cot, chair, trunk, table
    lamp = V((5.2, 6.0, 0)); lm = Part('key_lamp', tuple(lamp + Z * 3)); mb = lm.mb; dk = C('#2a2250')
    mb.box((lamp.x - 0.9, lamp.y - 0.9, 0), (lamp.x + 0.9, lamp.y + 0.9, 1.25), wood); mb.box((lamp.x - 1.0, lamp.y - 1.0, 1.25), (lamp.x + 1.0, lamp.y + 1.0, 1.4), dwood)      # little stand
    base = lamp + Z * 1.4
    rod(mb, base, base + Z * 2.4, 0.13, dk, seg=8); mb.frustum(base, base + Z * 0.15, 0.5, 0.45, dk, seg=10)
    mb.frustum(base + Z * 2.5, base + Z * 1.8, 0.2, 1.05, C('#12a15a', 1.0, 1.8, smix=0.2), seg=16, cap0=True, cap1=False); mb.sphere(base + Z * 2.2, 0.3, E('bulb2', color='#fff2c0', k=3.0), seg=10, rings=6)
    lm.done(tuple(base + Z), px=3)
    lg = Part('lamp_glow', ink=False, shadow=False); halo_card(lg.mb, base + Z * 2.0 + V((0, -0.3, 0)), 2.6, E('hlg', 'halo_warm', k=1.1, additive=True)); lg.done()
    point_light('key_lamp_L', base + Z * 2.2 + V((0.3, -0.5, 0)), (1.0, 0.72, 0.38), 1700, 0.35)
    pd = Part('pendant', (0, 6, 7.0), ink=False, shadow=False); mb = pd.mb; rod(mb, (0.4, 5.0, CE), (0.4, 5.0, 7.6), 0.03, C('#222244'), seg=4)
    mb.frustum((0.4, 5.0, 7.6), (0.4, 5.0, 7.0), 0.25, 0.85, C('#ffd2a0', 1.2, 2.0), seg=14); mb.sphere((0.4, 5.0, 7.1), 0.3, E('bulb3', color='#ffc070', k=0.9), seg=10, rings=6)
    pd.done((0.4, 5.0, 7.3), px=3)
    point_light('pendant_L', (0.4, 5.0, 6.8), (1.0, 0.72, 0.4), 700, 0.3)
    point_light('window_rim', (5.5, 13.0, 5.0), (0.28, 0.5, 1.0), 2400, 0.6); point_light('window_rim2', (8.2, 12.8, 4.0), (0.25, 0.45, 1.0), 1400, 0.5)
    st = Part('stove', (9.0, 12.4, 1.5)); mb = st.mb; kc = C('#d8d8e8', 1.3, 1.6)
    mb.box((8.0, 11.6, 0), (9.9, 13.6, 2.3), C('#2a2a50', 1.0, 1.4)); mb.box((8.1, 11.55, 0.6), (9.8, 11.62, 1.6), C('#ff8a3a', 1.6))
    rod(mb, (8.9, 12.6, 2.3), (8.9, 12.6, 3.2), 0.5, kc, r1=0.38, seg=12); rod(mb, (8.9, 12.6, 3.2), (8.9, 12.6, 3.42), 0.18, C('#222244')); rod(mb, (8.4, 12.4, 2.8), (7.8, 12.2, 3.2), 0.09, kc, seg=5)
    st.done((8.9, 12.4, 1.5), px=3)
    cs = Part('coat_hook', (RW - 0.5, 5.0, 5)); mb = cs.mb                                                     # coat + hat on the right wall hook
    mb.box((RW - 0.3, 4.2, 5.4), (RW, 5.8, 5.55), dwood); rod(mb, (RW - 0.5, 5.0, 5.4), (RW - 0.5, 5.0, 5.8), 0.07, dwood, seg=4)
    mb.box((RW - 0.9, 4.1, 2.1), (RW - 0.35, 5.9, 5.5), C('#3a4a8a', 1.0, 1.8, smix=0.2)); mb.box((RW - 1.0, 4.0, 2.1), (RW - 0.8, 6.0, 2.35), C('#2a3468')); lumpy(mb, (RW - 0.7, 5.0, 5.9), 0.4, C('#2a2a50', 1.0, 1.4), 4, seg=8, rings=5, rough=0.1)
    cs.done((RW - 0.6, 5, 4), px=3)
    bd = Part('cot', (-8.0, 1.0, 1.5)); mb = bd.mb                                                              # cot along the left wall (dark foreground layer)
    mb.box((-9.9, -3.4, 0.9), (-5.9, 3.0, 1.6), C('#e8dcc0', 1.0, 1.6)); mb.box((-9.9, 3.0, 0), (-5.9, 3.3, 2.5), dwood); mb.box((-9.9, -3.5, 0), (-5.9, -3.2, 2.2), dwood)
    for lx in (-9.8, -6.0):
        for ly in (-3.3, 3.1): rod(mb, (lx, ly, 0), (lx, ly, 0.95), 0.12, dwood, seg=5)
    mb.box((-9.6, 1.4, 1.6), (-6.2, 2.9, 2.0), C('#fff6e0', 1.2, 2.0, smix=0.2))
    bd.done((-7.9, 0, 1.5), px=3)
    qt = Part('quilt', ink=False); plane(qt.mb, (-9.7, -3.2, 1.62), (3.5, 0, 0), (0, 4.5, 0), TX('quilt', 1.0, 1.3), (0, 0, 1, 1)); qt.done()
    cx_, cy_ = -6.6, 6.6; ch = Part('chair', (cx_, cy_, 1.5)); mb = ch.mb                                    # a wooden chair, in the open rug area
    mb.box((cx_ - 0.8, cy_ - 0.8, 1.7), (cx_ + 0.8, cy_ + 0.8, 1.9), wood)
    for lx in (cx_ - 0.7, cx_ + 0.7):
        for ly in (cy_ - 0.7, cy_ + 0.7): rod(mb, (lx, ly, 0), (lx, ly, 1.7), 0.1, dwood, seg=5)
    mb.box((cx_ - 0.8, cy_ + 0.7, 1.9), (cx_ - 0.6, cy_ + 0.9, 4.1), dwood); mb.box((cx_ + 0.6, cy_ + 0.7, 1.9), (cx_ + 0.8, cy_ + 0.9, 4.1), dwood); mb.box((cx_ - 0.8, cy_ + 0.7, 3.2), (cx_ + 0.8, cy_ + 0.9, 4.1), wood)
    mb.box((cx_ - 0.5, cy_ - 0.5, 1.9), (cx_ + 0.4, cy_ + 0.3, 2.08), C('#c4272f', 1.0, 1.6))
    ch.done((cx_, cy_, 2), px=3)
    tk = Part('trunk', (6.3, 0.8, 0.8)); mb = tk.mb; mb.box((5.2, -0.4, 0), (7.6, 1.8, 1.4), C('#8a4a22', 1.0, 3.0, smix=0.3)); mb.box((5.1, -0.5, 0.55), (7.7, 1.9, 0.7), C('#2a1408')); mb.box((6.2, -0.55, 0.95), (6.6, -0.4, 1.25), C('#e8b84a', 1.4))
    mb.box((5.5, 0.0, 1.4), (7.3, 1.4, 1.55), C('#c4272f', 1.0, 2.0)); tk.done((6.3, 0.8, 0.8), px=3)
    tb = Part('table', (-3.4, 9.8, 1.4)); mb = tb.mb                                                            # small table at the cork with the NOTICE letter and a tea cup
    mb.box((-5.2, 8.9, 2.6), (-1.6, 10.9, 2.85), wood)
    for lx in (-5.0, -1.8):
        for ly in (9.1, 10.7): mb.box((lx - 0.15, ly - 0.15, 0), (lx + 0.15, ly + 0.15, 2.6), dwood)
    rod(mb, (-4.6, 10.3, 2.85), (-4.6, 10.3, 2.98), 0.34, C('#fff0d0', 1.3, 3.0, smix=0.2), r1=0.26, seg=14); rod(mb, (-4.6, 10.3, 2.98), (-4.6, 10.3, 3.3), 0.25, C('#fff0d0', 1.3, 3.0, smix=0.2), r1=0.32, seg=14)
    tb.done((-3.4, 9.8, 2.7), px=3)
    ln = Part('letter', ink=True); ln.mb.quad(V((-3.5, 9.1, 2.9)), V((1.6, 0, 0)), V((0, 1.2, 0.5)), TX('note', 1.1, 1.0, glow='note', glow_k=0.45), (0, 0, 1, 1)); ln.done((-2.7, 9.7, 3.1), px=2)
    rl = Part('rolls', (-8.0, 9.0, 2)); mb = rl.mb                                                            # pot of rolled drawings (left, back)
    rod(mb, (-8.6, 11.6, 0), (-8.6, 11.6, 1.0), 0.8, C('#6a3a1a'), r1=0.65, seg=10)
    for i, (dx, dy, tl) in enumerate(((0.0, 0.0, 0.0), (0.35, 0.25, 0.12), (-0.3, 0.3, -0.1), (0.15, -0.3, 0.05))): rod(mb, (-8.6 + dx, 11.6 + dy, 1.0), (-8.6 + dx + tl * 3, 11.6 + dy, 3.5 + i * 0.1), 0.28, C('#f4eccf', 1.2, 1.7), seg=10)
    rl.done((-8.6, 11.6, 2), px=3)
    wb = Part('basket', (0.0, 4.2, 0.8)); mb = wb.mb
    rod(mb, (-3.4, 6.2, 0), (-3.4, 6.2, 1.4), 0.65, C('#3a1a22', 1.0, 1.4), r1=0.85, seg=14)
    for i in range(7): lumpy(mb, (-3.4 + rs.uniform(-.5, .5), 6.2 + rs.uniform(-.5, .5), 1.4 + rs.uniform(-.1, .35)), rs.uniform(.26, .4), C('#fff6e0', 1.0, 1.6, smix=0.2), i + 3, seg=8, rings=5, rough=0.35)
    for i in range(6): lumpy(mb, (-3.4 + rs.uniform(-1.6, 1.6), 6.2 + rs.uniform(-1.6, 0.4), 0.2), rs.uniform(.22, .34), C('#fff6e0', 1.0, 1.6, smix=0.2), i + 30, seg=8, rings=5, rough=0.35)      # missed throws on the rug
    wb.done((-3.4, 6.2, 1), px=3)
    # floor dressing: slippers, a newspaper, a boot, light pools
    fd = Part('floor_dressing', ink=True); mb = fd.mb
    mb.box((-1.4, 3.0, 0.03), (-0.5, 3.35, 0.32), C('#6a2c28', 1.0, 1.8)); mb.box((-1.1, 3.4, 0.03), (-0.2, 3.75, 0.32), C('#6a2c28', 1.0, 1.8))
    obox(mb, V((3.5, 3.6, 0.07)), V((0.96, 0.27, 0)), V((-0.27, 0.96, 0)), Z, 0.9, 0.62, 0.03, C('#e8dcb8', 1.0, 1.6, smix=0.3)); obox(mb, V((7.6, 6.5, 0.07)), V((0.8, -0.6, 0)), V((0.6, 0.8, 0)), Z, 0.8, 0.55, 0.03, C('#fff0d0', 1.0, 1.6, smix=0.3))
    fd.done((3.5, 3.6, 0.1), px=2)
    for (px, py, k) in ((0.4, 6.0, 0.55), (5.2, 9.5, 0.4), (-4.5, 3.0, 0.3)):
        pl = Part('pool%d' % int(px * 10), ink=False, shadow=False); plane(pl.mb, (px - 3.2, py - 3.2, 0.06), (6.4, 0, 0), (0, 6.4, 0), E('pool', 'halo_warm', k=k, additive=True), (0, 0, 1, 1)); pl.done()
    wl = Part('window_light_pool', ink=False, shadow=False); plane(wl.mb, (4.2, 8.6, 0.065), (4.8, 0, 0), (0, 5.0, 0), E('wpool', 'halo_cool', k=0.5, additive=True), (0, 0, 1, 1)); wl.done()
    rebuild_diagram()

CAMS_NOTE = 'see SHOTS'
LOCATIONS = getattr(sys.modules[__name__], 'LOCATIONS', {})
LOCATIONS['lodgings'] = dict(build=build_lodgings, light='LODGINGS', sky=False, cam=CAM_LODGE)
SHOTS = getattr(sys.modules[__name__], 'SHOTS', {})

# ============================================================================= lodgings shots
def _cam_at(sh, g): return B.cam_eval(sh['cam'], g - sh['f0'])[0]
def hot_tip(name='red', frac=0.5):
    pts = poly_cut(line_pts(name, DIAG['bend'], DIAG['squeeze']), frac); return board_pt(pts[-1][0], pts[-1][1], 0.07)

# marks: (x, y, z, yaw_deg) = floor stand points of the cast (yaw 0 = facing -y toward the front camera)
M_LODGE = dict(s01=dict(beck=(-1.3, 5.2, 0, 0)), s04=dict(beck=(-1.4, 11.2, 0, 0)), s05=dict(beck=(0.0, 6.4, 0, 0)))

def actors_s01(g):
    cam = _cam_at(ALL('s01'), g); u = g / 107.0
    tip = hot_tip('red', DIAG['red'])
    if g < 69: B.place_tip('beck_rule_line', 'pen_r', tip, cam, 0.0, toward_cam=0.09, pose=dict(board=0))
    else: B.place_tip('beck_rule_line', 'pen_r', tip, cam, 0.0, toward_cam=0.09, pose=dict(board=0))
def ALL(n): return B.ALL_SHOTS[n]

SHOTS['s01'] = dict(location='lodgings', light='LODGINGS', f0=0, f1=108, shift_y=0.0,
    cam=[(0, (3.6, -2.6, 2.0), (0.4, 7.0, 3.0), 30), (30, (0.6, 0.9, 2.2), (0.2, 7.2, 3.0), 30), (52, (-3.0, 1.8, 2.6), (0.8, 7.6, 3.4), 30), (69, (-3.4, 3.2, 3.0), (2.0, 8.6, 3.6), 30),
         (90, (3.0, 4.0, 3.9), (5.5, 11.0, 4.6), 30), (100, (6.5, 8.4, 4.8), (6.6, 14.0, 5.0), 30), (107, (6.6, 12.4, 5.0), (6.6, 14.0, 5.0), 30)],
    marks=M_LODGE['s01'], state=dict(diagram=dict(red=0.55, blue=0, green=0, yellow=0, hot='red', ruler=(45.0, -0.3, -0.7))), actors=actors_s01)

def _scene_cam(sh, g): return B.cam_eval(sh['cam'], g - sh['f0'])[0]
def fl(g, f0, f1): return max(0.0, min(1.0, (g - f0) / float(f1 - f0)))

# ---- s04 (frames 324-450): match push from the OLD map pinned in Beck's room, pull back + slide right to Beck, who pins the circuit, reads the NOTICE, leans in
def actors_s04(g):
    sh = ALL('s04'); cam = _scene_cam(sh, g); k = g - sh['f0']
    if k < 70:                                                   # at the cork board: pin / hold the circuit
        story, mark = ('beck_hold_circuit', (-1.4, 11.2, 0)) if k >= 25 else ('beck_hold_circuit', (-1.2, 11.0, 0))
        ob = B.cast_card(story, mark, face_to=cam, rim='#8fb0ff')
    elif k < 95:
        ob = B.cast_card('beck_read_notice', (-2.4, 8.2, 0), face_to=cam, rim='#8fb0ff')
    else:                                                        # picks up the ruler, leans in at the board (pen tip at the start of the blue line)
        tip = board_pt(-1.55, -1.5, 0.07); ob = B.place_tip('beck_rule_line', 'pen_r', tip, cam, 0.0, toward_cam=0.09, pose=dict(board=0, prop_l={'type': 'ruler', 'angle': -8}))
        B.card_shadow(ob)
    if k < 95 and ob: pass
SHOTS['s04'] = dict(location='lodgings', light='LODGINGS', f0=324, f1=450,
    cam=[(0, (-6.1, 7.9, 4.6), (-6.1, 14.0, 4.6), 30), (35, (-5.8, 5.2, 4.4), (-5.2, 14.0, 4.2), 30), (75, (-4.6, 1.6, 3.9), (-2.6, 12.0, 3.6), 30), (125, (-3.0, -1.2, 3.6), (0.4, 8.2, 2.9), 30)],
    marks=dict(beck=(-1.4, 11.2, 0, 0)), state=dict(diagram=dict(red=1.0, blue=0, green=0, yellow=0, hot=None, ruler=None)), actors=actors_s04)

# ---- s05 (frames 450-577): crane up over Beck's shoulder to TOP-DOWN over the board; blue line, green 45 deg bend, yellow squeeze
def s05_state(k):
    d = dict(red=1.0, blue=fl(k, 20, 44), green=fl(k, 46, 66), yellow=fl(k, 70, 90), bend=27.0 + 18.0 * fl(k, 52, 62), squeeze=fl(k, 88, 112), ruler=None, hot=None)
    d['hot'] = 'blue' if 20 < k < 44 else 'green' if 46 < k < 66 else 'yellow' if 70 < k < 90 else None
    if 20 < k < 48: d['ruler'] = (90.0, -1.55 + 0.02, -0.3)
    elif 52 <= k < 70: d['ruler'] = None
    return d
def arm3d(hu, hv, tool='pen', name='beck_arm', reach=1.0):
    """Beck's right arm as 3D geometry coming in from the bottom edge of the board: sleeve (rolled cuff + black garter) -> skin forearm -> hand, with `tool`
    ('pen' | 'finger' | 'square') at paper point (hu, hv). The shoulder is below the frame (off-screen), so nothing floats."""
    C = STATE['C']; ap = Part(name, ink=True); mb = ap.mb
    H = board_pt(hu, hv, 0.30); S = board_pt(hu - 1.1, -3.6, 1.7); Em = board_pt(hu - 0.55, hv - 1.45, 0.95)
    sleeve, skin, garter = C('#f4ecd8', 1.1, 1.6, smix=0.25), C('#f0be94', 1.1, 1.8, smix=0.25), C('#1a1840')
    rod(mb, S, Em, 0.22, sleeve, r1=0.2, seg=12); rod(mb, Em, Em + (H - Em) * 0.62, 0.19, sleeve, r1=0.16, seg=12)
    g0 = Em + (H - Em) * 0.55; rod(mb, g0, g0 + (H - Em) * 0.05, 0.175, garter, seg=12)
    rod(mb, Em + (H - Em) * 0.62, H - (H - Em).normalized() * 0.15, 0.13, skin, r1=0.105, seg=12); mb.sphere(H, 0.17, skin, seg=12, rings=8)
    d = (H - Em).normalized()
    if tool == 'pen':
        rod(mb, H + d * 0.05 + BN * 0.1, board_pt(hu + 0.32, hv + 0.55, 0.06), 0.045, C('#1a2a6a', 1.2, 1.4), r1=0.015, seg=8); rod(mb, H + BN * 0.12, H + BN * 0.12 - BU * 0.5 - X * 0.3, 0.04, C('#e8b84a', 1.4, 1.5), seg=6)
    elif tool == 'finger':
        rod(mb, H, board_pt(hu + 0.25, hv + 0.42, 0.12), 0.075, skin, r1=0.05, seg=8)
    elif tool == 'square':
        c = board_pt(hu + 0.1, hv + 0.15, 0.09); pts = [board_pt(hu - 0.2, hv - 0.2, 0.08), board_pt(hu + 1.3, hv - 0.2, 0.08), board_pt(hu - 0.2, hv + 1.3, 0.08)]
        mb.pid += 1; mb.face(pts, C('#ffb347', 1.5, 1.4, smix=0.2))
    ap.done(tuple(H), px=2.5)

def actors_s05(g):
    sh = ALL('s05'); cam = _scene_cam(sh, g); k = g - sh['f0']
    el = math.degrees(math.atan2(cam.z - 2.6, math.hypot(cam.x - 2.4, cam.y - 7.5)))
    if k < 44:
        story, tip = ('beck_hold_circuit', board_pt(-2.7, -1.8, 0.1)) if k < 20 else ('beck_rule_line', hot_tip('blue', DIAG['blue']))
        anc = 'hand_r' if k < 20 else 'pen_r'
        B.place_tip(story, anc, tip, cam, None, toward_cam=0.22, tilt=max(0.0, min(80.0, el * 0.92)), pose=dict(board=0), rim='#8fb0ff')
    if 20 <= k < 46: arm3d(-1.55, DIAG['blue'] * 3.2 - 1.8, 'pen') if False else None
    if 20 <= k < 46: pts = poly_cut(line_pts('blue'), DIAG['blue']); arm3d(pts[-1][0], pts[-1][1], 'pen')
    elif 46 <= k < 70: arm3d(0.5, 0.4, 'square')
    elif k >= 70: arm3d(2.0, 1.2 - 0.8 * DIAG['squeeze'], 'finger')
SHOTS['s05'] = dict(location='lodgings', light='LODGINGS', f0=450, f1=577,
    cam=[(0, (-3.9, 3.4, 5.0), (0.8, 7.6, 2.8), 30), (45, (-0.5, 3.0, 6.2), (2.4, 7.8, 2.6), 29, -2), (90, (2.0, 3.6, 7.6), (2.4, 7.9, 2.6), 28.5, -6), (126, (2.4, 4.85, 8.7), (2.4, 7.9, 2.6), 28, -10)],
    marks=dict(beck=(-1.3, 6.4, 0, 0)), state=dict(diagram=dict(red=1.0, blue=0, green=0, yellow=0, bend=27.0, squeeze=0.0, hot=None, ruler=None)), actors=actors_s05,
    animate={'diagram': lambda k, n: set_diagram(s05_state(k))})

# ============================================================================= PUBLICITY DEPARTMENT (the room lives inside the HQ block, london coordinates)
PR = L.PUB_ROOM; PX0, PX1 = PR['x']; PY0, PY1 = PR['y']; PZ0, PZ1 = PR['floor'], PR['ceiling']
PW = L.PUB_WIN; PWX0, PWX1 = PW['center'][0] - PW['size'][0] / 2, PW['center'][0] + PW['size'][0] / 2; PWZ0, PWZ1 = PW['center'][2] - PW['size'][1] / 2, PW['center'][2] + PW['size'][1] / 2
OFF_DESK = (0.0, 42.5)                        # official's desk centre (x, y); he sits behind it at y 32.7
PART_Y = 36.0                                 # glass partition line
PUB = dict(drawer=0.0, stamp=0, towers=0.0, crate=1.0, ceiling=True, night=False)

def _desk(mb, x, y, w, d, h, wood, dwood, drawer_side=True):
    mb.box((x - w / 2, y - d / 2, h - 0.2), (x + w / 2, y + d / 2, h), wood)
    for sx in (-1, 1):
        mb.box((x + sx * (w / 2 - 0.3) - 0.25, y - d / 2 + 0.1, 0), (x + sx * (w / 2 - 0.3) + 0.25, y + d / 2 - 0.1, h - 0.2), dwood)
    mb.box((x - w / 2 + 0.6, y + d / 2 - 0.35, 0.4), (x + w / 2 - 0.6, y + d / 2 - 0.1, h - 0.25), dwood)

def build_publicity_room(S, P, embed=False, ceiling=True):
    C, TX, E = S['C'], S['TX'], S['E']; rs = random.Random(31)
    pan = TX('wood_dark', 0.75, 1.0); wd = C('#7a3a1a'); wood = C('#9a5a2a', 1.0, 1.8); dwood = C('#4a2410'); green = C('#12a15a', 1.0, 1.8, smix=0.2); steel = C('#6a7a9a', 1.0, 1.6)
    ceil_m = C('#8a5a6a', 0.45, 1.0)
    r = Part('pub_room', ink=False); mb = r.mb
    W = PX1 - PX0; D = PY1 - PY0; H = PZ1 - PZ0
    plane(mb, (PX0, PY0, PZ0), (W, 0, 0), (0, D, 0), C('#6a2634', 0.9, 1.0), (0, 0, 1, 1))                          # carpet floor
    if ceiling: plane(mb, (PX0, PY0, PZ1), (W, 0, 0), (0, D, 0), ceil_m, (0, 0, 1, 1))
    plane(mb, (PX0, PY1, PZ0), (W, 0, 0), (0, 0, H), pan, (0, 0, 6, 2.2))                                       # back wall
    plane(mb, (PX0, PY0, PZ0), (0, D, 0), (0, 0, H), pan, (0, 0, 4, 2.2)); plane(mb, (PX1, PY0, PZ0), (0, D, 0), (0, 0, H), pan, (0, 0, 4, 2.2))
    # south wall (inside face) with the real window opening
    for (a, b, c, d_) in ((PX0, PX1, PZ0, PWZ0), (PX0, PX1, PWZ1, PZ1), (PX0, PWX0, PWZ0, PWZ1), (PWX1, PX1, PWZ0, PWZ1)):
        if b - a > 0.01 and d_ - c > 0.01: plane(mb, (b, PY0, c), (a - b, 0, 0), (0, 0, d_ - c), pan, (0, 0, (b - a) / 3.5, (d_ - c) / 3.2))
    r.done()
    cr_ = Part('pub_trim', (0, 29, 8)); mb = cr_.mb
    mb.box((PX0, PY1 - 0.3, PZ0), (PX1, PY1, PZ0 + 0.6), dwood); mb.box((PX0, PY0, PZ0), (PX0 + 0.3, PY1, PZ0 + 0.6), dwood); mb.box((PX1 - 0.3, PY0, PZ0), (PX1, PY1, PZ0 + 0.6), dwood)
    mb.box((PX0, PY1 - 0.3, PZ1 - 0.5), (PX1, PY1, PZ1), C('#e8d8ae')); mb.box((PX0, PY0, PZ0), (PWX0, PY0 + 0.3, PZ0 + 0.6), dwood); mb.box((PWX1, PY0, PZ0), (PX1, PY0 + 0.3, PZ0 + 0.6), dwood)
    mb.box((PWX0 - 0.4, PY0 - 0.5, PWZ0 - 0.3), (PWX1 + 0.4, PY0 + 0.4, PWZ0), C('#e8dcc0'))                   # sill
    for xx in (PWX0 - 0.3, PWX1 + 0.1): mb.box((xx, PY0 - 0.5, PWZ0 - 0.3), (xx + 0.2, PY0 + 0.4, PWZ1 + 0.3), C('#e8dcc0'))
    mb.box((PWX0 - 0.4, PY0 - 0.5, PWZ1), (PWX1 + 0.4, PY0 + 0.4, PWZ1 + 0.3), C('#e8dcc0'))
    cr_.done((0, 29, 8), px=2.5)
    if not embed:                                                                                              # the street seen through the window (standalone location)
        sc = Part('pub_street', ink=False, shadow=False); plane(sc.mb, (PWX0 - 6, PY0 - 3.5, PWZ0 - 4), (PWX1 - PWX0 + 12, 0, 0), (0, 0, PWZ1 - PWZ0 + 8), E('pubstreet', 'night_city', k=1.0), (0.0, 0.0, 0.56, 0.78)); sc.done()
    # lamps, light, window light shafts
    pend = Part('pub_lamps', ink=False, shadow=False); mb = pend.mb; pg = Part('pub_lamp_glow', ink=False, shadow=False)
    for (lx, ly) in ((-9, 27), (-3.5, 27), (3.5, 27), (9, 27), (-9, 32), (9, 32), (-4, 42.0), (4, 42.0)):
        if ceiling:
            rod(mb, (lx, ly, PZ1), (lx, ly, PZ1 - 1.0), 0.04, C('#222244'), seg=4)
            mb.frustum((lx, ly, PZ1 - 1.0), (lx, ly, PZ1 - 1.7), 0.2, 0.95, green, seg=14); mb.sphere((lx, ly, PZ1 - 1.65), 0.28, E('pbulb', color='#ffd58a', k=1.3), seg=8, rings=5)
            halo_card(pg.mb, (lx, ly, PZ1 - 1.9), 2.4, E('hpg', 'halo_warm', k=0.9, additive=True))
        point_light('pubL%d_%d' % (lx, ly), (lx, ly, PZ1 - 2.1), (1.0, 0.72, 0.38), 520, 0.4)
    pend.done(); pg.done()
    sh = Part('pub_shafts', ink=False, shadow=False); mb = sh.mb
    for xx in (-4.0, -1.0, 2.0, 5.0):
        mb.pid += 1; mb.face([V((xx, PY0 + 0.1, PWZ1 - 0.2)), V((xx + 1.4, PY0 + 0.1, PWZ1 - 0.2)), V((xx + 3.6, PY0 + 9.0, PZ0 + 0.04)), V((xx + 1.2, PY0 + 9.0, PZ0 + 0.04))], E('shaft', 'beam_warm', k=0.35, additive=True), [(0, 1), (1, 1), (1, 0), (0, 0)])
    sh.done()
    # glass partition of the official's office (x -7..7, y PART_Y) with an open door gap x 2.6..4.8, lettering PUBLICITY DEPT
    gp = Part('pub_partition', (0, PART_Y, 10)); mb = gp.mb
    for xx in (-7.0, -3.5, 2.6, 4.8, 7.0): mb.box((xx - 0.12, PART_Y - 0.1, PZ0), (xx + 0.12, PART_Y + 0.1, PZ0 + 6.2), wood)
    mb.box((-7.1, PART_Y - 0.12, PZ0), (7.1, PART_Y + 0.12, PZ0 + 1.3), wood); mb.box((-7.1, PART_Y - 0.12, PZ0 + 6.0), (7.1, PART_Y + 0.12, PZ0 + 6.3), wood)
    mb.box((7.0, PART_Y, PZ0), (7.2, PY1, PZ0 + 6.3), wood); mb.box((-7.2, PART_Y, PZ0), (-7.0, PY1, PZ0 + 6.3), wood)
    gp.done((0, PART_Y, 9), px=2.5)
    gl = Part('pub_glass', ink=False, shadow=False)
    for (xa, xb) in ((-7.0, 2.6), (4.8, 7.0)): plane(gl.mb, (xa, PART_Y - 0.14, PZ0 + 1.3), (xb - xa, 0, 0), (0, 0, 4.7), E('glass', 'halo_cool', k=0.16, additive=True), (0, 0, 1, 1))
    gl.done()
    sg = Part('pub_glass_sign', ink=False); plane(sg.mb, (-2.9, PART_Y - 0.16, PZ0 + 4.85), (5.8, 0, 0), (0, 0, 1.15), E('pubsign', 'sign_publicity', k=1.4), (0, 0, 1, 1)); sg.done()
    # official's desk with drawer, lamp, in-tray, stamp, blotter, phone; his chair
    dk = Part('off_desk', (OFF_DESK[0], OFF_DESK[1], PZ0 + 1.5)); mb = dk.mb; x, y = OFF_DESK; zt = PZ0 + 2.5
    mb.box((x - 2.3, y - 1.0, zt - 0.25), (x + 2.3, y + 1.0, zt), wood); mb.box((x - 2.4, y - 1.1, zt), (x + 2.4, y + 1.1, zt + 0.06), C('#1f6a46', 1.0, 1.6))   # leather top
    mb.box((x - 2.2, y - 0.9, PZ0), (x - 1.2, y + 0.9, zt - 0.25), dwood); mb.box((x + 1.2, y - 0.9, PZ0), (x + 2.2, y + 0.9, zt - 0.25), dwood); mb.box((x - 1.2, y + 0.75, PZ0 + 0.3), (x + 1.2, y + 0.9, zt - 0.25), dwood)
    for dy_ in (0.0, 0.62, 1.24): mb.box((x + 1.25, y - 0.93, PZ0 + 0.25 + dy_ * 0.9), (x + 2.15, y - 0.88, PZ0 + 0.75 + dy_ * 0.9), wood); rod(mb, (x + 1.7, y - 0.95, PZ0 + 0.5 + dy_ * 0.9), (x + 1.7, y - 1.02, PZ0 + 0.5 + dy_ * 0.9), 0.07, C('#e8b84a', 1.4), seg=6)
    dk.done((x, y, PZ0 + 1.5), px=3)
    dr = Part('off_drawer', (x + 1.7, y - 1.5, PZ0 + 1.9)); mb = dr.mb; o = 0.0        # the open drawer (set_drawer moves the object)
    mb.box((x + 1.3, y - 0.9, zt - 0.62), (x + 2.1, y - 0.2, zt - 0.28), wood); mb.box((x + 1.35, y - 0.85, zt - 0.5), (x + 2.05, y - 0.3, zt - 0.3), C('#2a1408'))
    dro = dr.done((x + 1.7, y - 0.5, zt - 0.4), px=2.5); dro.location = (0, -PUB['drawer'] * 1.3, 0)
    ob_ = Part('off_desk_items', (x, y, zt)); mb = ob_.mb
    lamp = V((x - 1.7, y + 0.4, zt + 0.06)); rod(mb, lamp, lamp + Z * 1.1, 0.06, C('#2a2250'), seg=6); mb.frustum(lamp + Z * 1.2, lamp + Z * 0.85, 0.13, 0.5, green, seg=12, cap1=False); mb.sphere(lamp + Z * 0.95, 0.15, E('dl', color='#fff2c0', k=2.0), seg=8, rings=5)
    mb.box((x - 1.3, y - 0.2, zt + 0.06), (x - 0.6, y + 0.4, zt + 0.12), C('#f6ecd0')); mb.box((x - 1.3, y - 0.2, zt + 0.12), (x - 0.6, y + 0.4, zt + 0.35), C('#caa060', 1.0, 1.6))   # in-tray
    mb.box((x - 0.4, y - 0.7, zt + 0.06), (x + 0.7, y + 0.1, zt + 0.09), C('#f6ecd0'))                                   # blotter / sheet
    rod(mb, (x + 1.1, y - 0.5, zt + 0.06), (x + 1.1, y - 0.5, zt + 0.35), 0.15, C('#6a3a1a'), seg=10); rod(mb, (x + 1.1, y - 0.5, zt + 0.35), (x + 1.1, y - 0.5, zt + 0.5), 0.09, C('#caa060'), seg=8)    # stamp
    mb.box((x + 0.2, y + 0.4, zt + 0.06), (x + 0.8, y + 0.85, zt + 0.45), C('#1a1840', 1.0, 1.6))                          # phone
    ob_.done((x, y, zt), px=2.5)
    point_light('off_lamp', lamp + Z * 1.0, (1.0, 0.72, 0.38), 380, 0.3)
    stp = Part('off_stamp_mark', ink=False, shadow=False)
    if PUB['stamp']: plane(stp.mb, (x - 0.3, y - 0.65, zt + 0.1), (0.8, 0, 0), (0, 0.5, 0), E('stampm', color='#e3262b', k=1.6), (0, 0, 1, 1))
    stp.done()
    ch = Part('off_chair', (x, y + 1.9, PZ0 + 2)); mb = ch.mb; ccx, ccy = x, y + 1.9
    mb.box((ccx - 0.9, ccy - 0.8, PZ0 + 1.6), (ccx + 0.9, ccy + 0.8, PZ0 + 1.85), C('#6a1a1a', 1.0, 1.6)); rod(mb, (ccx, ccy, PZ0), (ccx, ccy, PZ0 + 1.6), 0.12, dwood, seg=6)
    for a_ in range(5): ang = a_ * 2 * math.pi / 5; rod(mb, (ccx, ccy, PZ0 + 0.1), (ccx + 0.9 * math.cos(ang), ccy + 0.9 * math.sin(ang), PZ0 + 0.05), 0.06, dwood, seg=4)
    mb.box((ccx - 0.9, ccy + 0.7, PZ0 + 1.85), (ccx + 0.9, ccy + 0.95, PZ0 + 3.6), C('#6a1a1a', 1.0, 1.6))
    ch.done((ccx, ccy, PZ0 + 1.5), px=3)
    # clerks' desks with typewriters and chairs
    cd = Part('clerk_desks', (0, 26.5, PZ0 + 1.5)); mb = cd.mb
    for (dx, dy_) in ((-9.5, 27.5), (-4.0, 27.5), (2.4, 27.6), (8.0, 27.5), (12.5, 27.8), (-9.0, 31.3), (9.0, 31.0)):
        _desk(mb, dx, dy_, 3.2, 1.7, 2.3, wood, dwood); zt2 = PZ0 + 2.3
        mb.box((dx - 0.8, dy_ - 0.5, zt2), (dx + 0.8, dy_ + 0.5, zt2 + 0.45), C('#2a2a50', 1.0, 1.5)); mb.box((dx - 0.7, dy_ - 0.55, zt2 + 0.3), (dx + 0.7, dy_ - 0.1, zt2 + 0.5), C('#9aa6dc', 1.0, 1.5))    # typewriter
        mb.box((dx - 0.4, dy_ - 0.2, zt2 + 0.45), (dx + 0.4, dy_ + 0.2, zt2 + 0.9), C('#fff6e0', 1.2, 1.7)); mb.box((dx + 1.0, dy_ + 0.5, zt2), (dx + 1.7, dy_ + 0.9, zt2 + 0.5), C('#e3262b', 1.0, 1.6))
        cy_ = dy_ + 1.5; mb.box((dx - 0.6, cy_ - 0.6, PZ0 + 1.5), (dx + 0.6, cy_ + 0.6, PZ0 + 1.7), dwood); mb.box((dx - 0.6, cy_ + 0.5, PZ0 + 1.7), (dx + 0.6, cy_ + 0.65, PZ0 + 3.3), dwood)
        for lx in (-0.5, 0.5):
            for ly in (-0.5, 0.5): mb.box((dx + lx - 0.06, cy_ + ly - 0.06, PZ0), (dx + lx + 0.06, cy_ + ly + 0.06, PZ0 + 1.5), dwood)
    cd.done((0, 26.5, PZ0 + 1.5), px=3)
    # filing cabinets, coat stand, plants, wall clock, posters, pigeonholes, bin, door
    fc = Part('pub_furniture', (0, 30, PZ0 + 2)); mb = fc.mb
    for (fx, fy) in ((-12.6, 45.0), (-10.4, 45.0), (10.4, 45.0), (12.6, 45.0)):
        mb.box((fx - 1.0, fy - 0.8, PZ0), (fx + 1.0, fy + 0.8, PZ0 + 3.4), C('#3a6a5a', 1.0, 1.6))
        for dz_ in (0.2, 1.2, 2.2): mb.box((fx - 0.9, fy - 0.85, PZ0 + dz_ + 0.1), (fx + 0.9, fy - 0.78, PZ0 + dz_ + 0.9), C('#4a8a72', 1.0, 1.6)); mb.box((fx - 0.2, fy - 0.9, PZ0 + dz_ + 0.45), (fx + 0.2, fy - 0.8, PZ0 + dz_ + 0.55), C('#e8b84a', 1.4))
    rod(mb, (13.2, 34.0, PZ0), (13.2, 34.0, PZ0 + 5.8), 0.1, dwood, seg=6)                                              # coat stand + coat + hat
    mb.box((12.7, 33.7, PZ0 + 2.6), (13.7, 34.4, PZ0 + 5.2), C('#3a4a8a', 1.0, 1.8, smix=0.2)); lumpy(mb, (13.2, 34.05, PZ0 + 5.7), 0.45, C('#2a2a50', 1.0, 1.4), 4, seg=8, rings=5, rough=0.1)
    for (px_, py_) in ((-13.2, 26.0), (13.2, 26.0)):
        rod(mb, (px_, py_, PZ0), (px_, py_, PZ0 + 1.0), 0.55, C('#8a3a22'), r1=0.42, seg=10); lumpy(mb, (px_, py_, PZ0 + 1.6), 0.8, C('#1f8a52', 1.0, 1.6), 7 + int(px_), seg=10, rings=6, rough=0.3)
    rod(mb, (-13.0, 34.0, PZ0), (-13.0, 34.0, PZ0 + 1.3), 0.5, C('#3a1a22', 1.0, 1.4), r1=0.62, seg=10)
    mb.box((-13.9, 40.0, PZ0 + 2.2), (-13.5, 44.0, PZ0 + 5.8), dwood)
    fc.done((0, 30, PZ0 + 2), px=3)
    ps = Part('pub_posters', ink=True); mb = ps.mb; UV = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for i, xx in enumerate((-11.5, -7.8, 7.8, 11.5)):
        mb.pid += 1; mb.face([V((xx - 1.4, PY1 - 0.08, PZ0 + 2.6)), V((xx + 1.4, PY1 - 0.08, PZ0 + 2.6)), V((xx + 1.4, PY1 - 0.08, PZ0 + 7.0)), V((xx - 1.4, PY1 - 0.08, PZ0 + 7.0))], TX('poster%d' % i, 1.0, 1.0, glow='poster%d' % i, glow_k=0.3), UV)
    for i, yy in enumerate((28.0, 33.5)):
        mb.pid += 1; mb.face([V((PX1 - 0.08, yy + 2.4, PZ0 + 2.8)), V((PX1 - 0.08, yy, PZ0 + 2.8)), V((PX1 - 0.08, yy, PZ0 + 6.6)), V((PX1 - 0.08, yy + 2.4, PZ0 + 6.6))], TX('poster%d' % (4 + i), 1.0, 1.0, glow='poster%d' % (4 + i), glow_k=0.3), UV)
    mb.pid += 1; mb.face([V((PX0 + 0.08, 29.4), ) if False else V((PX0 + 0.08, 38.0, PZ0 + 3.0)), V((PX0 + 0.08, 40.4, PZ0 + 3.0)), V((PX0 + 0.08, 40.4, PZ0 + 6.6)), V((PX0 + 0.08, 38.0, PZ0 + 6.6))], TX('poster2', 1.0, 1.0, glow='poster2', glow_k=0.3), UV)
    ps.done((0, 33, PZ0 + 5), px=2.5)
    ck = Part('pub_clock', ink=False); plane(ck.mb, (-1.6, PY1 - 0.1, PZ0 + 5.3), (3.2, 0, 0), (0, 0, 3.2), E('pclk', 'clock', k=1.1, alpha=True), (0, 0, 1, 1)); ck.done()
    # the door out (left wall) with a warm corridor light; sign
    dd = Part('pub_door', (PX0, 30.0, PZ0 + 3)); mb = dd.mb
    mb.box((PX0, 29.0, PZ0), (PX0 + 0.5, 31.0, PZ0 + 5.4), C('#ffb352', 1.4)); mb.box((PX0, 28.8, PZ0), (PX0 + 0.55, 29.0, PZ0 + 5.6), wood); mb.box((PX0, 31.0, PZ0), (PX0 + 0.55, 31.2, PZ0 + 5.6), wood); mb.box((PX0, 28.8, PZ0 + 5.4), (PX0 + 0.55, 31.2, PZ0 + 5.7), wood)
    dd.done((PX0, 30, PZ0 + 3), px=2.5)
    dsg = Part('pub_door_sign', ink=False)
    mb = dsg.mb; mb.pid += 1; mb.face([V((PX0 + 0.58, 29.0, PZ0 + 5.8)), V((PX0 + 0.58, 31.0, PZ0 + 5.8)), V((PX0 + 0.58, 31.0, PZ0 + 6.6)), V((PX0 + 0.58, 29.0, PZ0 + 6.6))], E('pdoor', 'sign_dept_door', k=1.4), [(0, 0), (1, 0), (1, 1), (0, 1)]); dsg.done()
    point_light('door_warm', (PX0 + 1.4, 30.0, PZ0 + 3.0), (1.0, 0.65, 0.32), 300, 0.5)
    for (xx, yy, k_) in ((-8, 27, 0.5), (0, 28.2, 0.5), (8, 27, 0.5), (-8, 32, 0.4), (8, 32, 0.4), (0, 42.6, 0.45)):
        pl = Part('pubpool%d_%d' % (xx, int(yy * 10)), ink=False, shadow=False); plane(pl.mb, (xx - 3.5, yy - 3.2, PZ0 + 0.06), (7, 0, 0), (0, 6.4, 0), E('pool', 'halo_warm', k=k_, additive=True), (0, 0, 1, 1)); pl.done()
    rebuild_towers(); rebuild_crate()

def rebuild_towers():
    for n in ('map_towers',):
        o = bpy.data.objects.get(n)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    h = PUB['towers']
    if h <= 0.01: return
    C, TX = STATE['C'], STATE['TX']; rs = random.Random(8); tp = Part('map_towers', ink=True); mb = tp.mb; tm = TX('pocket_map', 1.0, 1.0); top = C('#f6ecd0', 1.1, 1.5, smix=0.2)
    spots = [(a, b + 10.8, c) for (a, b, c) in [(-4.2, 30.8, 7.0), (-3.6, 33.0, 6.0), (4.2, 30.9, 6.4), (3.7, 33.0, 5.6), (-1.8, 33.1, 4.6), (1.9, 33.1, 5.0), (-5.7, 32.0, 4.2), (5.8, 31.9, 4.4), (-6.3, 30.2, 2.8), (6.2, 30.0, 3.0), (-2.6, 30.0, 2.4), (2.8, 29.9, 2.2)]]
    for (sx, sy, mx) in spots:
        nH = max(1, int(mx * h / 0.32)); z = PZ0
        for i in range(nH):
            yaw = rs.uniform(-0.12, 0.12); ax = V((math.cos(yaw), math.sin(yaw), 0)); ay = V((-math.sin(yaw), math.cos(yaw), 0))
            obox(mb, V((sx + rs.uniform(-0.08, 0.08), sy + rs.uniform(-0.08, 0.08), z + 0.16)), ax, ay, Z, 0.62, 0.45, 0.16, tm if i % 2 == 0 else top); z += 0.32
    tp.done((0, 31.5, PZ0 + 3), px=2.5)

def rebuild_crate():
    o = bpy.data.objects.get('map_crate')
    if o: bpy.data.objects.remove(o, do_unlink=True)
    t = PUB['crate']
    if t is None: return
    C, TX = STATE['C'], STATE['TX']; cp = Part('map_crate', ink=True); mb = cp.mb; x0, y0 = 6.8, OFF_DESK[1] - 1.6; z0 = PZ0 + 0.02 + (1.0 - min(1.0, t)) * 9.0
    mb.box((x0 - 1.1, y0 - 0.9, z0), (x0 + 1.1, y0 + 0.9, z0 + 1.6), C('#a86a32', 1.0, 1.8), mats={'front': TX('crate_maps', 1.0, 1.0)})
    mb.box((x0 - 1.15, y0 - 0.95, z0 + 0.7), (x0 + 1.15, y0 + 0.95, z0 + 0.85), C('#5a2c12'))
    cp.done((x0, y0, z0 + 0.8), px=2.5)

@setter('drawer')
def set_drawer(open_):
    """Official's desk drawer: 0 closed .. 1 fully open (the drawer box slides out toward -y 1.3)."""
    PUB['drawer'] = max(0.0, min(1.0, float(open_)))
    o = bpy.data.objects.get('off_drawer')
    if o: o.location = (0, -PUB['drawer'] * 1.3, 0)
@setter('stamp_mark')
def set_stamp_mark(on):
    PUB['stamp'] = 1 if on else 0
    o = bpy.data.objects.get('off_stamp_mark')
    if o: o.hide_render = not on
@setter('map_towers')
def set_map_towers(h): PUB['towers'] = max(0.0, min(1.0, float(h))); rebuild_towers()
@setter('crate')
def set_crate(t):
    """The fresh MAPS crate of s15: t 0 = high above the desk, 1 = landed beside the official; None = absent."""
    PUB['crate'] = None if t is None else float(t); rebuild_crate()

CAM_PUB = dict(loc=(0.0, 28.0, 10.0), look_at=(0.0, 38.0, 9.0), lens=30)
def build_publicity(scene, P):
    build_publicity_room(STATE, P, embed=False, ceiling=PUB['ceiling'])
LOCATIONS['publicity'] = dict(build=build_publicity, light='HQ_EVENING', sky=False, cam=CAM_PUB)

# ---- cast placement helpers for the publicity room: seated official behind the desk, clerks at their desks
def seated(story, x, y, zt, cam, mirror=False, pose=None, rim='#9fb8ff'):
    """A seated cast22 pose behind a desk whose top is at z = zt: the card's head is placed so the 2D desk line of the pose (pose key desk_y, head -> desk top) meets the 3D desk top."""
    sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast22')); import cast22
    c, p = cast22.STORY22[story]; dy = p.get('desk_y', 1.3)
    ob = B.cast_card(story, (x, y, 0.0), face_to=cam, mirror=mirror, pose=dict(desk=0, typewriter=0, **(pose or {})), shadow=False, rim=rim)
    ob.location.z = zt + dy - ob['anc']['head'][1]
    return ob
def off_card(story, cam, dy=1.0, mirror=False, pose=None):
    x, y = OFF_DESK; return seated(story, x, y + dy, PZ0 + 2.5, cam, mirror, pose)
def clerk_card(story, x, y, cam, mirror=False):
    if story.startswith(('clerk_type', 'clerk_sit')): return seated(story, x, y, PZ0 + 2.3, cam, mirror)
    return B.cast_card(story, (x, y + 0.9, PZ0), face_to=cam, mirror=mirror, pose=dict(desk=0, typewriter=0), rim='#9fb8ff')       # standing laughers behind their desks

# ---- s06 (frames 577-823): CUT 1. Through the glass partition, push through the open door to the two-shot, 1 s punch-in on the official at 25.9 s, ease back
def actors_s06(g):
    sh = ALL('s06'); cam = _scene_cam(sh, g); k = g - sh['f0']; t = (g / 30.0) - 0.1
    if t < 20.44: story = 'off_sit_glance'
    elif t < 21.85: story = 'off_stamp'
    elif t < 23.57: story = 'off_laugh_back'
    elif t < 25.93: story = 'off_wave_sheet'
    else: story = 'off_eat_mime'
    off_card(story, cam, 1.0, pose=dict(mouth='flat') if t < 23.5 else None)
    B.cast_card('beck_present_roll', (-1.7, OFF_DESK[1] - 2.7, PZ0), face_to=cam, mirror=False, pose=dict(desk=0), rim='#9fb8ff')
    cl = 'clerk_laugh_point_' if t > 21.8 else 'clerk_type_'
    clerk_card(cl + 'a', -9.5, 28.0, cam, mirror=False); clerk_card(cl + 'b', -4.0, 28.0, cam, mirror=False); clerk_card(cl + 'a', 8.0, 28.0, cam, mirror=True); clerk_card(cl + 'b', 12.5, 28.3, cam, mirror=True)
    clerk_card('clerk_sit_b', -9.0, 31.7, cam); clerk_card('clerk_sit_c', 9.0, 31.4, cam, mirror=True)
SHOTS['s06'] = dict(location='publicity', light='HQ_EVENING', f0=577, f1=823,
    cam=[(0, (3.9, 25.2, 10.8), (1.0, 42.0, 8.7), 22), (60, (3.0, 29.5, 9.5), (0.5, 42.2, 9.0), 23), (115, (3.7, 33.0, 9.5), (-0.6, 42.2, 8.9), 25), (185, (3.9, 34.6, 9.5), (-0.7, 42.4, 8.9), 25),
         (203, (3.6, 34.8, 9.8), (-0.3, 43.0, 9.6), 32), (214, (3.2, 35.0, 10.4), (0.0, 43.5, 10.8), 74), (232, (3.6, 34.8, 9.6), (-0.4, 42.6, 9.1), 30), (245, (3.7, 34.6, 9.5), (-0.7, 42.4, 8.9), 26)],
    marks=dict(beck=(-1.7, OFF_DESK[1] - 2.7, PZ0, 0), official=(OFF_DESK[0], OFF_DESK[1] + 1.0, PZ0 + 1.83, 0)), state=dict(stamp_mark=False), actors=actors_s06,
    animate={'stamp_mark': lambda k, n: set_stamp_mark(k >= 52)})

# ---- s07 (frames 823-938): crane UP and back to the bird's-eye over the whole open office; the drawer slams shut, the clerks laugh, Beck walks out
def actors_s07(g):
    sh = ALL('s07'); cam = _scene_cam(sh, g); k = g - sh['f0']
    off_card('off_toss_drawer', cam, 1.0, pose=dict(desk_drawer=1 if k < 8 else 0))
    u = fl(k, 40, 112); bx = -1.7 + (-14.2 + 1.7 + 2.0) * u; by = OFF_DESK[1] - 2.7 + (30.0 - (OFF_DESK[1] - 2.7)) * u
    B.cast_card('beck_sag', (bx, by, PZ0), face_to=cam, mirror=u > 0.05, rim='#9fb8ff')
    cl = 'clerk_laugh_belly_' if k < 50 else 'clerk_laugh_point_'
    clerk_card(cl + 'a', -9.5, 28.0, cam); clerk_card(cl + 'b', -4.0, 28.0, cam); clerk_card(cl + 'a', 8.0, 28.0, cam, mirror=True); clerk_card(cl + 'b', 12.5, 28.3, cam, mirror=True)
    clerk_card('clerk_laugh_point_b', -9.0, 31.7, cam); clerk_card('clerk_laugh_point_c', 9.0, 31.4, cam, mirror=True)
SHOTS['s07'] = dict(location='publicity', light='HQ_EVENING', f0=823, f1=938,
    cam=[(0, (3.7, 25.6, 10.2), (-0.2, 42.0, 9.0), 24), (50, (3.0, 25.5, 16.0), (0.0, 38.5, 8.0), 23), (114, (0.5, 26.0, 26.0), (0.0, 37.0, 7.4), 22)],
    marks=dict(beck=(-1.7, OFF_DESK[1] - 2.7, PZ0, 0), official=(OFF_DESK[0], OFF_DESK[1] + 1.0, PZ0, 0)), pre=dict(ceiling_off=True), state=dict(drawer=1.0), actors=actors_s07,
    animate={'drawer': lambda k, n: set_drawer(1.0 if k < 8 else 0.0)})
@setter('ceiling_off')
def _ceiling_off(v): PUB['ceiling'] = not v

# ============================================================================= HQ CORRIDOR (own coordinates: along +x, floor y -6..4, back wall y = 4 with the doors, z 0..8.5)
CY0, CY1, CZ = -6.0, 4.0, 8.5
DOOR_X = dict(signals=-14.0, drawing=0.0, publicity=14.0)
COR = dict(hand=0.0)
CAM_COR = dict(loc=(0, -4.5, 3.4), look_at=(4, 1.5, 3.0), lens=26)

def build_corridor(scene, P):
    S = STATE; C, TX, E = S['C'], S['TX'], S['E']; rs = random.Random(12)
    X0, X1 = -44.0, 44.0
    wood = C('#8a4a22', 1.0, 1.8); dwood = C('#4a2410'); cream = C('#e8d8b0', 1.0, 1.6); green = C('#12a15a', 1.0, 1.8, smix=0.2)
    r = Part('cor_room', ink=False); mb = r.mb
    plane(mb, (X0, CY0, 0), (X1 - X0, 0, 0), (0, CY1 - CY0, 0), TX('wood', 0.8, 1.0), (0, 0, 22, 3))                                   # floor boards
    plane(mb, (X0, CY0, CZ), (X1 - X0, 0, 0), (0, CY1 - CY0, 0), C('#8a5a6a', 0.45, 1.0), (0, 0, 1, 1))                              # ceiling
    plane(mb, (X1, CY1, 0), (X0 - X1, 0, 0), (0, 0, CZ), cream, (0, 0, 1, 1))                                                          # back wall upper (cream) - the dado below
    plane(mb, (X0, CY0 + 0.01, 0), (X1 - X0, 0, 0), (0, 0, CZ), cream, (0, 0, 1, 1))                                                    # front wall (behind the camera)
    plane(mb, (X0, CY0, 0), (0, CY1 - CY0, 0), (0, 0, CZ), cream, (0, 0, 1, 1)); plane(mb, (X1, CY0, 0), (0, CY1 - CY0, 0), (0, 0, CZ), cream, (0, 0, 1, 1))
    r.done()
    rg = Part('cor_runner', ink=False); plane(rg.mb, (X0, -1.4, 0.03), (X1 - X0, 0, 0), (0, 3.8, 0), C('#4a1a2a', 0.9, 1.0), (0, 0, 1, 1)); plane(rg.mb, (X0, -1.15, 0.035), (X1 - X0, 0, 0), (0, 0.18, 0), C('#c8982e', 1.0, 1.4), (0, 0, 1, 1)); plane(rg.mb, (X0, 2.2, 0.035), (X1 - X0, 0, 0), (0, 0.18, 0), C('#c8982e', 1.0, 1.4), (0, 0, 1, 1)); rg.done()
    dd = Part('cor_dado', (0, CY1 - 0.2, 1.8)); mb = dd.mb
    mb.box((X0, CY1 - 0.3, 0), (X1, CY1, 3.6), TX('wood_dark', 0.8, 1.0), tile=(8, 4)); mb.box((X0, CY1 - 0.45, 3.5), (X1, CY1, 3.75), wood); mb.box((X0, CY1 - 0.4, 0), (X1, CY1, 0.7), dwood)
    mb.box((X0, CY1 - 0.4, CZ - 0.9), (X1, CY1, CZ), wood)                                                                              # picture rail / cornice
    mb.box((X0, CY0, 0), (X1, CY0 + 0.3, 0.7), dwood); mb.box((X0, CY0, CZ - 0.9), (X1, CY0 + 0.4, CZ), wood)
    dd.done((0, CY1, 2), px=3)
    # doors with plaques: SIGNALS, DRAWING OFFICE, PUBLICITY DEPT (ajar)
    dr = Part('cor_doors', (0, CY1 - 0.3, 3.0)); mb = dr.mb; spec = (('signals', 'sign_signals', 'Signals'), ('drawing', 'sign_drawing', 'Drawing'), ('publicity', 'sign_dept_door', 'Pub'))
    for key, sg, _ in spec:
        x = DOOR_X[key]
        mb.box((x - 1.6, CY1 - 0.45, 0), (x - 1.35, CY1, 6.0), wood); mb.box((x + 1.35, CY1 - 0.45, 0), (x + 1.6, CY1, 6.0), wood); mb.box((x - 1.6, CY1 - 0.45, 5.75), (x + 1.6, CY1, 6.0), wood)
        mb.box((x - 1.35, CY1 - 0.1, 0), (x + 1.35, CY1, 5.75), C('#ffb352', 1.5) if key != 'publicity' else C('#1a1030'))                           # frosted warm glass door / dark gap
        if key != 'publicity':
            mb.box((x - 1.2, CY1 - 0.5, 0.2), (x + 1.2, CY1 - 0.35, 5.6), dwood); mb.box((x - 0.95, CY1 - 0.52, 2.6), (x + 0.95, CY1 - 0.46, 5.3), C('#ffd88a', 1.8)); rod(mb, (x + 0.8, CY1 - 0.55, 2.5), (x + 0.8, CY1 - 0.7, 2.5), 0.09, C('#e8b84a', 1.4), seg=6)
        else:
            mb.box((x - 1.2, CY1 - 0.5, 0.2), (x - 0.2, CY1 - 0.3, 5.6), dwood); mb.box((x + 1.0, CY1 - 0.9, 0.2), (x + 1.2, CY1 - 0.1, 5.6), dwood)                  # door leaf swung open
    dr.done((0, CY1, 3), px=3)
    pl = Part('cor_plaques', ink=False)
    for key, sg, _ in spec: plane(pl.mb, (DOOR_X[key] - 1.5, CY1 - 0.56, 6.1), (3.0, 0, 0), (0, 0, 0.9), E('pl' + key, sg, k=1.4), (0, 0, 1, 1))
    pl.done()
    # posters + clock + notice boards between doors; coat pegs, bench, plants, radiator, fire bucket
    ps = Part('cor_posters', ink=True); mb = ps.mb; UV = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for i, xx in enumerate((-22.0, -7.0, 7.0, 21.0, 28.0, -29.0)):
        mb.pid += 1; mb.face([V((xx - 1.4, CY1 - 0.42, 2.6)), V((xx + 1.4, CY1 - 0.42, 2.6)), V((xx + 1.4, CY1 - 0.42, 6.5)), V((xx - 1.4, CY1 - 0.42, 6.5))], TX('poster%d' % (i % 6), 1.0, 1.0, glow='poster%d' % (i % 6), glow_k=0.3), UV)
    ps.done((0, CY1, 4), px=2.5)
    ck = Part('cor_clock', ink=False); plane(ck.mb, (-9.5, CY1 - 0.5, 6.0), (2.4, 0, 0), (0, 0, 2.4), E('cclk', 'clock', k=1.1, alpha=True), (0, 0, 1, 1)); ck.done()
    nb = Part('cor_notice_boards', (0, CY1, 3)); mb = nb.mb
    for xx in (-4.2, 6.8, 20.5):
        mb.box((xx - 1.4, CY1 - 0.55, 2.4), (xx + 1.4, CY1 - 0.4, 5.2), wood); mb.box((xx - 1.25, CY1 - 0.6, 2.55), (xx + 1.25, CY1 - 0.5, 5.05), C('#5a2f14'))
    nb.done((0, CY1, 3.8), px=2.5)
    for i, xx in enumerate((-4.2, 6.8, 20.5)):
        np_ = Part('cor_notes%d' % i, ink=False)
        for j in range(4): plane(np_.mb, (xx - 1.0 + (j % 2) * 1.1, CY1 - 0.63, 2.7 + (j // 2) * 1.15), (0.9, 0, 0), (0, 0, 1.0), TX('circuit%d' % ((i + j) % 3) if j % 2 == 0 else 'note', 1.1, 1.0), (0, 0, 1, 1))
        np_.done()
    fu = Part('cor_furniture', (0, 2.5, 1.5)); mb = fu.mb
    for xx in (-26.0, 17.5):                                                                                                         # benches
        mb.box((xx - 2.0, CY1 - 1.8, 1.4), (xx + 2.0, CY1 - 0.7, 1.6), wood); mb.box((xx - 2.0, CY1 - 0.8, 1.6), (xx + 2.0, CY1 - 0.65, 3.4), wood)
        for lx in (-1.7, 1.7): mb.box((xx + lx - 0.1, CY1 - 1.7, 0), (xx + lx + 0.1, CY1 - 0.8, 1.4), dwood)
    for xx in (-35.0, 36.0):                                                                                                        # plants
        rod(mb, (xx, CY1 - 1.0, 0), (xx, CY1 - 1.0, 1.2), 0.65, C('#8a3a22'), r1=0.5, seg=10); lumpy(mb, (xx, CY1 - 1.0, 2.0), 0.95, C('#1f8a52', 1.0, 1.6), int(xx), seg=10, rings=6, rough=0.3)
    for xx in (-17.5, 10.5, 25.0):                                                                                                  # coat pegs with coats and hats
        mb.box((xx - 1.0, CY1 - 0.35, 5.0), (xx + 1.0, CY1, 5.2), dwood)
        for j in (-0.6, 0.6): mb.box((xx + j - 0.4, CY1 - 0.9, 2.0), (xx + j + 0.4, CY1 - 0.35, 4.9), C('#3a4a8a' if j < 0 else '#5a3a2a', 1.0, 1.8, smix=0.2)); lumpy(mb, (xx + j, CY1 - 0.6, 5.3), 0.38, C('#2a2a50', 1.0, 1.4), 4, seg=8, rings=5, rough=0.1)
    mb.box((30.0, CY1 - 0.6, 0.4), (33.0, CY1 - 0.35, 2.4), C('#2a2a50', 1.0, 1.4))                                                    # radiator
    for k in range(10): mb.box((30.15 + 0.3 * k, CY1 - 0.7, 0.5), (30.4 + 0.3 * k, CY1 - 0.55, 2.3), C('#4a4a80', 1.0, 1.4))
    rod(mb, (-31.0, CY1 - 0.9, 0), (-31.0, CY1 - 0.9, 1.6), 0.5, C('#c8201e', 1.0, 3.0, smix=0.15), seg=10)                           # fire bucket
    fu.done((0, 2, 2), px=3)
    # ceiling lamps every 7 D (green shades) + halos + lights; window at both ends (blue)
    lp = Part('cor_lamps', ink=False, shadow=False); mb = lp.mb; lg = Part('cor_lamp_glow', ink=False, shadow=False); lxs = list(np.arange(-35.0, 36.0, 7.0))
    for lx in lxs:
        rod(mb, (lx, -1.0, CZ), (lx, -1.0, CZ - 1.3), 0.04, C('#222244'), seg=4); mb.frustum((lx, -1.0, CZ - 1.3), (lx, -1.0, CZ - 2.0), 0.2, 1.0, green, seg=14); mb.sphere((lx, -1.0, CZ - 1.95), 0.3, E('cbulb', color='#ffd58a', k=1.4), seg=8, rings=5)
        halo_card(lg.mb, (lx, -1.0, CZ - 2.2), 2.6, E('hcl', 'halo_warm', k=0.9, additive=True))
    lp.done(); lg.done()
    for lx in lxs[::1]: point_light('corL%d' % lx, (lx, -1.0, CZ - 2.2), (1.0, 0.72, 0.38), 380, 0.4)
    for sx_, nx in ((X0, 1), (X1, -1)):
        wn = Part('cor_end_window%d' % nx, ink=False, shadow=False); mb = wn.mb; mb.pid += 1
        mb.face([V((sx_ + nx * 0.05, -3.0, 2.0)), V((sx_ + nx * 0.05, 1.0, 2.0)), V((sx_ + nx * 0.05, 1.0, 7.0)), V((sx_ + nx * 0.05, -3.0, 7.0))][::nx], E('cwin', 'night_city', k=1.0), [(0, 0), (1, 0), (1, 1), (0, 1)])
        wn.done()
    # floor light pools under each lamp
    for lx in lxs:
        pp = Part('cor_pool%d' % lx, ink=False, shadow=False); plane(pp.mb, (lx - 3.4, -4.4, 0.06), (6.8, 0, 0), (0, 8.0, 0), E('pool', 'halo_warm', k=0.5, additive=True), (0, 0, 1, 1)); pp.done()
    # fg notice-board easels (the foreground frame of the side tracking shot)
    fb = Part('cor_easels', (0, -3.4, 2.6)); mb = fb.mb
    for xx in (-6.0, 3.0, 13.0):
        for sx in (-1, 1): rod(mb, (xx + sx * 1.1, -3.0, 0), (xx + sx * 0.7, -3.0, 4.6), 0.1, dwood, seg=5)
        mb.box((xx - 1.4, -3.15, 1.8), (xx + 1.4, -2.9, 4.8), wood); mb.box((xx - 1.25, -3.2, 1.95), (xx + 1.25, -3.12, 4.65), C('#5a2f14'))
    fb.done((0, -3.4, 3), px=3)
    for i, xx in enumerate((-6.0, 3.0, 13.0)):
        nq = Part('cor_fgnotes%d' % i, ink=False)
        for j in range(4): plane(nq.mb, (xx - 1.15 + (j % 2) * 1.2, -3.23, 2.1 + (j // 2) * 1.35), (1.0, 0, 0), (0, 0, 1.15), TX('note' if (i + j) % 2 else 'circuit%d' % (j % 3), 1.1, 1.0), (0, 0, 1, 1))
        nq.done()
    hnd = Part('cor_hand', ink=True); hnd.done()
    rebuild_hand()

def rebuild_hand():
    o = bpy.data.objects.get('cor_hand')
    if o: bpy.data.objects.remove(o, do_unlink=True)
    t = COR['hand']
    if t <= 0.01: return
    C = STATE['C']; hp = Part('cor_hand', ink=True); mb = hp.mb; x = DOOR_X['publicity']; y0 = CY1 + 0.4; reach = 1.6 * min(1.0, t)
    sleeve, skin = C('#2a3a78', 1.0, 1.6, smix=0.2), C('#f0be94', 1.1, 1.8, smix=0.25)
    rod(mb, (x - 0.2, y0 + 1.5, 3.5), (x - 0.2, CY1 - reach + 0.4, 3.4), 0.24, sleeve, r1=0.2, seg=10); rod(mb, (x - 0.2, CY1 - reach + 0.4, 3.4), (x - 0.2, CY1 - reach - 0.1, 3.38), 0.14, skin, r1=0.12, seg=8)
    mb.sphere((x - 0.2, CY1 - reach - 0.15, 3.36), 0.17, skin, seg=10, rings=6)
    hp.done((x, CY1 - 1, 3.4), px=2.5)
@setter('door_hand')
def set_door_hand(t): COR['hand'] = float(t); rebuild_hand()

def actors_s08(g):
    sh = ALL('s08'); cam = _scene_cam(sh, g); k = g - sh['f0']; bx = beck_x_s08(k)
    sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast22')); import cast22
    if k < 30: ob = B.cast_card(('beck', cast22.walk_carry_roll(k / 28.0)), (bx, 1.4, 0.0), face_to=cam, mirror=False, rim='#ffb070', pose=dict(yaw=0.7))
    else: ob = B.cast_card('beck_knock', (bx, 1.4, 0.0), face_to=cam, mirror=False, rim='#ffb070')
def beck_x_s08(k): return -9.0 + 21.0 * min(1.0, k / 30.0) ** 0.9 if k < 30 else 12.0
SHOTS['s08'] = dict(location='hq_corridor', light='HQ_EVENING', f0=938, f1=1005,
    cam=[(0, (-12.0, -4.6, 3.3), (-8.0, 1.8, 3.2), 26), (30, (0.6, -4.6, 3.3), (4.0, 1.8, 3.1), 26), (66, (9.8, -4.5, 3.4), (13.2, 1.8, 3.1), 26)],
    marks=dict(beck=(-9.0, 1.4, 0.0, 0)), state=dict(door_hand=0.0), actors=actors_s08, animate={'door_hand': lambda k, n: set_door_hand(max(0.0, (k - 56) / 8.0))})
LOCATIONS['hq_corridor'] = dict(build=build_corridor, light='HQ_EVENING', sky=False, cam=CAM_COR)
