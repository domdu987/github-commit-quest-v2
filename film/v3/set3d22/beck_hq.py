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
        obox(rl.mb, c, ax, ay, BN, 1.6, 0.14, 0.035, STATE['C']('#e8b86a', 1.2, 1.3)); rl.done(tuple(c), px=2.5)

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
    mb.frustum((0.4, 5.0, 7.6), (0.4, 5.0, 7.0), 0.25, 0.85, C('#ffd2a0', 1.2, 2.0), seg=14); mb.sphere((0.4, 5.0, 7.1), 0.3, E('bulb3', color='#fff2c0', k=3.0), seg=10, rings=6)
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
    ch = Part('chair', (-3.4, 2.6, 1.5)); mb = ch.mb                                                            # a wooden chair, seat and back, in the open rug area
    mb.box((-4.2, 1.8, 1.7), (-2.6, 3.4, 1.9), wood)
    for lx in (-4.1, -2.7):
        for ly in (1.9, 3.3): rod(mb, (lx, ly, 0), (lx, ly, 1.7), 0.1, dwood, seg=5)
    mb.box((-4.2, 3.3, 1.9), (-4.0, 3.5, 4.1), dwood); mb.box((-2.8, 3.3, 1.9), (-2.6, 3.5, 4.1), dwood); mb.box((-4.2, 3.3, 3.2), (-2.6, 3.5, 4.1), wood)
    mb.box((-3.9, 2.2, 1.9), (-3.0, 3.0, 2.08), C('#c4272f', 1.0, 1.6))
    ch.done((-3.4, 2.6, 2), px=3)
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
