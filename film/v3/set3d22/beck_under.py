#!/usr/bin/env python3
"""beck_under.py (builder B): the UNDERGROUND of film 22.  Locations: 'under' (grate shaft + noodle-tunnel cutaway + platform hall, s03), 'platform' (s10),
'hall' (ticket hall, s09 / s13), 'carriage' (s11).  Shots s03, s09, s10, s11, s13.  See API.md (section B) for coordinates, marks, cameras and setters.
Build local coordinates (1 D = head):  platform hall: x +-12 (platforms |x| 3.4 .. 12, track trough between), y -14 .. 44 (end wall with the tunnel hole), floor z 0, vault crown 12.5.
In 'under' the hall is shifted by ORG_HALL = (GX, GY - 54, -62) so its tunnel hole is at world y GY - 10, z -59.6, under the street grate xy GRATE_XY."""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw
import bpy
import beck as B
import beck_util as U
from beck import V, STATE, BX, T
from mine import obox, rod, lumpy

try:
    import beck_london as L
    GRATE_XY = tuple(L.GRATE_XY); GRATE_SIZE = tuple(L.GRATE_SIZE)
except Exception:
    GRATE_XY = (8.0, 19.0); GRATE_SIZE = (8.0, 7.0)
GX, GY = GRATE_XY
ORG_HALL = (GX, GY - 54.0, -62.0)

# hall dimensions (local)
RX, SPR, RZ, YA, YB = 12.0, 6.0, 6.5, -14.0, 44.0
PE, TZ, CX, CZ, CR = 3.4, -1.4, 0.0, 2.4, 4.3

# light presets (point-lamp interiors; see beck.LIGHTS['PLATFORM'])
B.LIGHTS['UNDER'] = dict(B.LIGHTS['PLATFORM'], shade=(0.07, 0.12, 0.46), shade_tint=(0.05, 0.11, 0.58), shade_mix=0.92, lift=(0.016, 0.03, 0.10), grade_saturation=1.3)
B.LIGHTS['HALL'] = dict(B.LIGHTS['PLATFORM'], shade=(0.05, 0.14, 0.47), shade_tint=(0.03, 0.14, 0.56), shade_mix=0.95, lift=(0.008, 0.016, 0.06), grade_saturation=1.3)
B.LIGHTS['CARRIAGE'] = dict(B.LIGHTS['PLATFORM'], shade=(0.06, 0.11, 0.46), shade_tint=(0.04, 0.10, 0.58), shade_mix=0.95, lift=(0.006, 0.012, 0.05), grade_saturation=1.3)

TRAIN = dict(objs=[], base=[], y0=0.0, doors_open=[], doors_closed=[], lights=[])
CUR = {}

def _cs(): return STATE['C'], STATE['TX'], STATE['E'], STATE['CARD']

# ============================================================================= bench / pillar / small props
def bench(mb, x, y0, y1, back):
    """Slatted wooden bench along y at x, back toward the side `back` (+1 / -1 in x). Iron end frames."""
    C, TX, E, CARD = _cs(); wood = TX('wood_slats', 1.0, 1.6, form=False); iron = C('#1d1a45', 1.0, 1.2); dw = C('#5a2c12')
    for k in range(3): mb.box((x - 0.8, y0, 1.45 + 0.0), (x + 0.8, y1, 1.62), wood) if k == 0 else None
    for dz in (0.0, 0.22, 0.44):
        mb.box((x + back * 0.7 - 0.07, y0, 1.7 + dz + 0.2), (x + back * 0.7 + 0.07, y1, 1.7 + dz + 0.38), wood)
    for yy in (y0 + 0.2, y1 - 0.3):
        mb.box((x - 0.78, yy, 0.0), (x - 0.62, yy + 0.1, 1.45), iron); mb.box((x + 0.62, yy, 0.0), (x + 0.78, yy + 0.1, 1.45), iron)
        mb.box((x + back * 0.7 - 0.06, yy, 1.45), (x + back * 0.7 + 0.06, yy + 0.1, 2.5), iron)

def column(mb, x, y, w=1.1, h=11.0, mat=None, cap=None):
    mb.box((x - w / 2, y - w / 2, 0), (x + w / 2, y + w / 2, h), mat)
    mb.box((x - w / 2 - 0.12, y - w / 2 - 0.12, 0), (x + w / 2 + 0.12, y + w / 2 + 0.12, 0.5), cap)
    mb.box((x - w / 2 - 0.12, y - w / 2 - 0.12, h - 0.4), (x + w / 2 + 0.12, y + w / 2 + 0.12, h), cap)

def bin_(mb, x, y, C):
    rod(mb, (x, y, 0), (x, y, 1.6), 0.5, C('#2f6a4a', 1.0, 1.4), r1=0.42, seg=10); rod(mb, (x, y, 1.6), (x, y, 1.75), 0.55, C('#1d1a45'), seg=10)

def luggage(mb, x, y, C, k=0, rot=0.0):
    cols = ['#8a4a22', '#1f49c8', '#12724a', '#7a2a30', '#c98a1a']
    ax = V((math.cos(rot), math.sin(rot), 0)); ay = V((-math.sin(rot), math.cos(rot), 0)); Z = V((0, 0, 1))
    w, d, h = [(1.5, 0.8, 1.0), (1.2, 0.7, 0.8), (1.8, 0.9, 1.3), (1.0, 0.7, 0.9)][k % 4]
    obox(mb, V((x, y, h / 2)), ax, ay, Z, w / 2, d / 2, h / 2, C(cols[k % 5], 1.0, 2.2, smix=0.3))
    obox(mb, V((x, y, h * 0.55)), ax, ay, Z, w / 2 + 0.04, d / 2 + 0.04, 0.05, C('#2a1408'))

def newspaper(mb, x, y, rot, C):
    ax = V((math.cos(rot), math.sin(rot), 0)); ay = V((-math.sin(rot), math.cos(rot), 0)); obox(mb, V((x, y, 0.05)), ax, ay, V((0, 0, 1)), 0.5, 0.36, 0.03, C('#efe4c0', 1.0, 1.6, smix=0.3))

# ============================================================================= the platform hall
def build_hall(scene, P, with_train=True, crowd=True, shot=None):
    """Platform hall in local coords (+ORG). Everything static; the train is moved with set_train(y_front)."""
    C, TX, E, CARD = _cs(); rs = random.Random(33); Y = V((0, 1, 0)); Z = V((0, 0, 1)); X = V((1, 0, 0))
    U.view((-8, 4, 4))
    outl = [(-RX, 0.0), (-RX, SPR)]; N = 30
    for i in range(1, N): th = math.pi * (1 - i / N); outl.append((RX * math.cos(th), SPR + RZ * math.sin(th)))
    outl += [(RX, SPR), (RX, 0.0)]
    vt = U.Pt('vault', ink=False); mb = vt.mb; tw = TX('tiles_cool', 1.0, 1.0); tp = TX('tiles_cool_plain', 0.62, 1.0); s_acc = 0.0
    for (x0, z0), (x1, z1) in zip(outl, outl[1:]):
        Lh = math.hypot(x1 - x0, z1 - z0); mat = tw if z1 <= SPR + 1e-6 and z0 <= SPR + 1e-6 else tp
        v0, v1 = (s_acc / 8.0, (s_acc + Lh) / 8.0) if mat is tw else ((s_acc - SPR) / 8.0, (s_acc + Lh - SPR) / 8.0)
        mb.pid += 1; mb.face([V((x0, YA, z0)), V((x1, YA, z1)), V((x1, YB, z1)), V((x0, YB, z0))], mat, [(YA / 4, v0), (YA / 4, v1), (YB / 4, v1), (YB / 4, v0)]); s_acc += Lh
    # end wall with the round tunnel hole
    outer = [(-RX, -2.4)] + outl + [(RX, -2.4)] + [(x, -2.4) for x in (8.0, 0.0, -8.0)]
    inner = [(CX + CR * math.cos(2 * math.pi * i / 40), CZ + CR * math.sin(2 * math.pi * i / 40)) for i in range(40)]
    ang = lambda p: math.atan2(p[1] - CZ, p[0] - CX)
    O = sorted(outer, key=ang); I_ = sorted(inner, key=ang); n_, m_ = len(O), len(I_); i = j = 0
    def tri(a, b, c): mb.pid += 1; mb.face([V((p[0], YB, p[1])) for p in (a, b, c)], tw, [(p[0] / 4, p[1] / 8) for p in (a, b, c)])
    while i < n_ or j < m_:
        ai = ang(O[(i + 1) % n_]) + (2 * math.pi if i + 1 >= n_ else 0); aj = ang(I_[(j + 1) % m_]) + (2 * math.pi if j + 1 >= m_ else 0)
        if i < n_ and (j >= m_ or ai <= aj): tri(O[i], O[(i + 1) % n_], I_[j % m_]); i += 1
        else: tri(I_[j], I_[(j + 1) % m_], O[i % n_]); j += 1
    # near end (y = YA): a wall with a stair arch (WAY OUT) so the hall is closed behind the camera
    mb.pid += 1; mb.face([V((-RX, YA, 0)), V((RX, YA, 0)), V((RX, YA, SPR))] + [V((x, YA, z)) for (x, z) in reversed(outl[2:-2])] + [V((-RX, YA, SPR))], tw, [(0, 0)] * (4 + len(outl[2:-2])))
    vt.done()
    # tunnel tube behind the hole
    tb = U.Pt('tube', ink=False); mb = tb.mb; tube = E('tube', color='#0f2a6a', k=1.5); TL = 60.0
    for k in range(24):
        a0, a1 = 2 * math.pi * k / 24, 2 * math.pi * (k + 1) / 24; rr = CR + 0.15
        mb.pid += 1; mb.face([V((CX + rr * math.cos(a0), YB, CZ + rr * math.sin(a0))), V((CX + rr * math.cos(a1), YB, CZ + rr * math.sin(a1))), V((CX + rr * math.cos(a1), YB + TL, CZ + rr * math.sin(a1))), V((CX + rr * math.cos(a0), YB + TL, CZ + rr * math.sin(a0)))], tube, [(0, 0)] * 4)
    if not CUR.get('open_tube'): mb.pid += 1; mb.face([V((CX + 4.8 * math.cos(2 * math.pi * k / 24), YB + TL, CZ + 4.8 * math.sin(2 * math.pi * k / 24))) for k in range(24)], E('tube_end', color='#02061c', k=1.0), [(0, 0)] * 24)
    tb.done()
    tl = U.Pt('tunnel_lamps', ink=False, shadow=False)
    for yy in (52.0, 62.0, 72.0): B.halo_card(tl.mb, (0, yy, 5.4), 2.4, E('htl', 'halo_cool', k=1.2, additive=True))
    tl.done()
    # ---- floors, track
    fl = U.Pt('floor', ink=False); mb = fl.mb
    B.plane(mb, (-RX, YA, 0), (RX - PE, 0, 0), (0, YB - YA, 0), TX('floor_pf', 1.0, 1.0), (0, 0, 4, 14)); B.plane(mb, (PE, YA, 0), (RX - PE, 0, 0), (0, YB - YA, 0), TX('floor_pf', 1.0, 1.0), (0, 0, 4, 14))
    B.plane(mb, (-PE, YA, TZ), (2 * PE, 0, 0), (0, YB - YA + 60, 0), TX('ballast', 1.0, 1.0), (0, 0, 4, 22))
    B.plane(mb, (-PE, YA, TZ), (0, 0, -TZ), (0, YB - YA, 0), tw, (YA / 4, 0.0, YB / 4, 0.2)); B.plane(mb, (PE, YA, TZ), (0, 0, -TZ), (0, YB - YA, 0), tw, (YA / 4, 0.0, YB / 4, 0.2))
    fl.done()
    ed = U.Pt('edges', (0, 15, 0.1)); mb = ed.mb; yl = C('#ffd22a', 1.3, 2.0, smix=0.2)
    mb.box((-PE - 0.8, YA, 0), (-PE, YB, 0.12), yl); mb.box((PE, YA, 0), (PE + 0.8, YB, 0.12), yl); mb.box((-PE - 0.25, YA, -0.05), (-PE, YB, 0.0), C('#2a2060')); mb.box((PE, YA, -0.05), (PE + 0.25, YB, 0.0), C('#2a2060'))
    ed.done((0, 15, 0.1), px=2.5)
    rl = U.Pt('rails', (0, 15, TZ)); mb = rl.mb; steel = C('#c8d0ff', 2.0, 3.0, smix=0.1); slp = C('#4a2a1a', 1.0, 1.6)
    for rx in (-0.9, 0.9): mb.box((rx - 0.1, YA, TZ + 0.1), (rx + 0.1, YB + 60, TZ + 0.42), steel)
    mb.box((2.0, YA, TZ + 0.1), (2.25, YB + 60, TZ + 0.3), C('#ff8a3a', 1.6, 2.0))
    for yy in np.arange(YA, YB + 40, 1.4): mb.box((-1.5, yy, TZ), (1.5, yy + 0.4, TZ + 0.12), slp)
    rl.done((0, 15, TZ), px=2.5)
    # ---- vault ribs, globe lamps
    rb = U.Pt('ribs', (0, 15, 12)); mb = rb.mb; rm = C('#a82838', 1.0, 1.6, smix=0.3)
    for yy in (0.0, 12.0, 24.0, 36.0):
        for (x0, z0), (x1, z1) in zip(outl[1:-1], outl[2:-1]):
            c = V(((x0 + x1) / 2, yy, (z0 + z1) / 2)); tg = V((x1 - x0, 0, z1 - z0)); Lg = tg.length; tg.normalize(); nrm = V((-tg.z, 0, tg.x))
            obox(mb, c, tg, Y, nrm, Lg / 2 + 0.05, 0.4, 0.28, rm)
    rb.done((0, 15, 12), px=3)
    gl = U.Pt('globes', (0, 15, 11)); mb = gl.mb; gm = E('globe', color='#ffd890', k=1.1); lcol = C('#2a2250')
    gh = U.Pt('globe_halos', ink=False, shadow=False); gpos = []
    for yy in (4.0, 14.0, 24.0, 34.0):
        for gx in (-5.6, 5.6):
            gz = 10.0; gpos.append((gx, yy, gz)); rod(mb, (gx, yy, gz + 1.8), (gx, yy, gz + 0.5), 0.05, lcol, seg=5); mb.sphere((gx, yy, gz), 0.6, gm, seg=14, rings=9)
            B.halo_card(gh.mb, (gx, yy, gz), 2.0, E('hg', 'halo_warm', k=0.8, additive=True))
    gl.done((0, 15, 11), px=3); gh.done()
    for i, (gx, yy, gz) in enumerate(gpos): U.pl('globe%d' % i, (gx, yy, gz - 0.6), (1.0, 0.7, 0.36), 1400 if yy < 30 else 1050, 0.5)
    for yy in (8.0, 22.0, 36.0):
        for wx_, sgn in ((-RX + 0.5, 1), (RX - 0.5, -1)): U.pl('wall%d_%d' % (yy, sgn), (wx_ + sgn * 0.4, yy, 5.2), (1.0, 0.68, 0.34), 520, 0.4)
    # ---- end wall: liner ring, station roundel, WAY OUT, clock; the OLD map on the near-left wall (facing +x)
    lr = U.Pt('liner', (0, YB, 2.4)); mb = lr.mb; lc_ = C('#3a2a6a', 1.0, 1.6)
    for i in range(32):
        a0, a1 = 2 * math.pi * i / 32, 2 * math.pi * (i + 1) / 32; am = (a0 + a1) / 2; c = V((CX + (CR + 0.5) * math.cos(am), YB - 0.5, CZ + (CR + 0.5) * math.sin(am)))
        tg = V((-math.sin(am), 0, math.cos(am))); nr = V((math.cos(am), 0, math.sin(am))); obox(mb, c, tg, Y, nr, (CR + 0.5) * math.pi / 32 + 0.04, 0.5, 0.5, lc_)
    lr.done((0, YB, 2.4), px=3)
    rd = U.Pt('roundel_name', ink=False); B.plane(rd.mb, (-6.0, YB - 0.1, 7.6), (12.0, 0, 0), (0, 0, 4.0), E('rndl', 'roundel_piccadilly', k=1.5, alpha=True), (0, 0, 1, 1)); rd.done()
    wo = U.Pt('way_out', ink=True); B.plane(wo.mb, (6.2, YB - 0.12, 1.0), (5.0, 0, 0), (0, 0, 1.7), E('wayout', 'sign_way_out', k=1.6), (0, 0, 1, 1)); wo.done((9, YB, 2), px=3)
    # side-wall name panels (PICCADILLY) opposite each platform, un-mirrored
    nm = U.Pt('name_panels', ink=True); mb = nm.mb; UV = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for yy in (4.0, 34.0):
        mb.pid += 1; mb.face([V((RX - 0.06, yy + 6.0, 3.0)), V((RX - 0.06, yy, 3.0)), V((RX - 0.06, yy, 4.6)), V((RX - 0.06, yy + 6.0, 4.6))], E('np_a%d' % yy, 'sign_piccadilly', k=1.5), UV)
    nm.done((RX, 20, 4), px=2.5)
    # the OLD cramped map, big, on the near-left wall at y 11 .. 20 (faces +x); frame
    om = U.Pt('old_map', ink=True); mb = om.mb
    mb.box((-RX + 0.02, 11.9, 2.3), (-RX + 0.4, 20.1, 8.5), C('#6a3a1a', 1.0, 1.6)); om.done((-RX, 16, 5), px=2.5)
    omi = U.Pt('old_map_img', ink=False); mb = omi.mb; mb.pid += 1
    mb.face([V((-RX + 0.44, 12.2, 2.6)), V((-RX + 0.44, 19.8, 2.6)), V((-RX + 0.44, 19.8, 8.2)), V((-RX + 0.44, 12.2, 8.2))], old_map_mat(), [(0, 0), (1, 0), (1, 1), (0, 1)]); omi.done()
    # posters on both walls (un-mirrored UVs)
    ps = U.Pt('posters', ink=True); mb = ps.mb
    for (yy, im) in ((24.0, 'poster0'), (28.0, 'poster1'), (32.0, 'poster2'), (3.0, 'poster3'), (7.0, 'poster5')):
        mb.pid += 1; mb.face([V((-RX + 0.06, yy, 2.4)), V((-RX + 0.06, yy + 3.2, 2.4)), V((-RX + 0.06, yy + 3.2, 6.4)), V((-RX + 0.06, yy, 6.4))], TX(im, 1.0, 1.0, glow=im, glow_k=0.35), UV)
    for (yy, im) in ((10.0, 'poster4'), (16.0, 'poster1'), (22.0, 'poster0'), (28.0, 'poster3'), (-2.0, 'poster2')):
        mb.pid += 1; mb.face([V((RX - 0.06, yy + 4.0, 2.0)), V((RX - 0.06, yy, 2.0)), V((RX - 0.06, yy, 6.4)), V((RX - 0.06, yy + 4.0, 6.4))], TX(im, 1.0, 1.0, glow=im, glow_k=0.35), UV)
    ps.done((0, 12, 4), px=2.5)
    # hanging TO TRAINS / WAY OUT signs over the platform, clock
    hs = U.Pt('hang_signs', ink=True); mb = hs.mb
    for (yy, im, xx) in ((2.0, 'sign_to_trains', -8.0), (18.0, 'sign_exit', -7.6), (28.0, 'sign_to_trains', 7.8)):
        rod(mb, (xx - 1.6, yy, 11.0), (xx - 1.6, yy, 8.6), 0.05, C('#222244'), seg=4); rod(mb, (xx + 1.6, yy, 11.0), (xx + 1.6, yy, 8.6), 0.05, C('#222244'), seg=4)
        mb.pid += 1; mb.face([V((xx - 2.2, yy, 7.4)), V((xx + 2.2, yy, 7.4)), V((xx + 2.2, yy, 8.8)), V((xx - 2.2, yy, 8.8))], E('hs_%d' % yy, im, k=1.5), UV_)
        mb.pid += 1; mb.face([V((xx + 2.2, yy + 0.02, 7.4)), V((xx - 2.2, yy + 0.02, 7.4)), V((xx - 2.2, yy + 0.02, 8.8)), V((xx + 2.2, yy + 0.02, 8.8))], E('hs_%d' % yy, im, k=1.5), UV_)
    hs.done((0, 12, 8), px=3)
    ck = U.Pt('clock', (8, 12, 10)); mb = ck.mb; mb.frustum((6.0, 38.0, 9.6), (6.0, 38.3, 9.6), 1.5, 1.5, C('#1a1840'), seg=20); ck.done((6, 38, 9.6), px=3)
    cf = U.Pt('clock_face', ink=False); B.plane(cf.mb, (4.6, 37.95, 8.2), (2.8, 0, 0), (0, 0, 2.8), E('clk', 'clock', k=1.4, alpha=True), (0, 0, 1, 1)); cf.done()
    # ---- furniture: benches (slatted, iron legs), columns, bins, trolley, vending machine, luggage, newspapers, A-frame
    bn = U.Pt('benches', (0, 15, 1)); mb = bn.mb
    for (y0_, y1_) in ((24.0, 30.0), (35.0, 41.0)): bench(mb, -RX + 1.1, y0_, y1_, -1)
    bench(mb, -9.2, 1.5, 7.5, -1); bench(mb, -RX + 1.1, 21.0, 22.0 + 4.0 - 1.0, -1) if False else None
    for (y0_, y1_) in ((6.0, 12.0), (26.0, 32.0)): bench(mb, RX - 1.1, y0_, y1_, 1)
    bn.done((0, 15, 1), px=2.5)
    cl = U.Pt('columns', (0, 15, 5)); mb = cl.mb; cm = TX('tiles_cool', 1.0, 1.0, form=False); cap = C('#a82838', 1.0, 1.5)
    for (x, y) in ((-7.2, 18.0), (-7.2, 33.0), (7.6, 0.0), (7.6, 22.0), (7.6, 38.0)): column(mb, x, y, 1.1, 11.0, cm, cap)
    cl.done((0, 15, 5), px=2.5)
    bi = U.Pt('bins', (0, 15, 1)); mb = bi.mb
    for (x, y) in ((-RX + 0.8, 9.0), (RX - 0.8, 3.0), (RX - 0.8, 34.0)): bin_(mb, x, y, C)
    bi.done((0, 15, 1), px=3)
    tm = U.Pt('machine', (-RX + 1, 32.9, 2)); mb = tm.mb
    mb.box((-RX + 0.1, 30.7, 0), (-RX + 1.6, 32.8, 4.2), C('#c8201e', 1.0, 2.6, smix=0.15)); mb.box((-RX + 1.55, 30.9, 2.0), (-RX + 1.7, 32.6, 3.6), C('#ffd88a', 1.8)); mb.box((-RX + 1.55, 31.0, 0.6), (-RX + 1.7, 32.5, 1.2), C('#3a0a10'))
    mb.box((-RX + 1.0, 32.9, 0), (-RX + 1.6, 35.9, 4.6), C('#12724a', 1.0, 2.4, smix=0.15)); mb.box((-RX + 1.55, 33.1, 1.0), (-RX + 1.7, 35.7, 3.4), C('#ffe9b0', 1.7))
    tm.done((-RX + 1, 15, 2), px=3)
    tl2 = U.Pt('trolley', (-9.0, 10.5, 1.5)); mb = tl2.mb
    mb.box((-9.9, 8.2, 1.0), (-8.2, 11.0, 1.2), C('#3a2a1a', 1.0, 2.0)); rod(mb, (-8.2, 8.4, 1.2), (-8.2, 8.4, 3.2), 0.1, C('#222244'), seg=5); rod(mb, (-8.2, 10.8, 1.2), (-8.2, 10.8, 3.2), 0.1, C('#222244'), seg=5); mb.box((-8.3, 8.3, 3.1), (-8.1, 10.9, 3.3), C('#222244'))
    for wy in (8.4, 10.8): mb.frustum((-9.6, wy, 0.5), (-9.6, wy + 0.2, 0.5), 0.5, 0.5, C('#14143a'), seg=10)
    mb.box((-9.8, 8.4, 1.2), (-8.5, 9.6, 2.4), C('#8a4a22', 1.0, 3.0, smix=0.3)); mb.box((-9.7, 9.8, 1.2), (-8.6, 10.9, 2.0), C('#1f49c8', 1.0, 3.0, smix=0.3)); mb.box((-9.7, 8.5, 2.4), (-8.7, 9.5, 3.1), C('#12724a', 1.0, 3.0, smix=0.3))
    _o = tl2.done((-9.0, 9.5, 1.5), px=3); _o.location.y += 24.0
    lg = U.Pt('luggage', (-8, 10, 1)); mb = lg.mb
    for (x, y, k, r) in ((-8.6, 29.0, 0, 0.3), (-7.4, 30.4, 2, -0.5), (9.6, 8.0, 1, 0.4), (-10.2, 9.5, 3, 0.9), (8.8, 24.5, 0, -0.2), (-6.4, 39.0, 2, 0.2), (-10.2, 34.0, 1, 0.1)): luggage(mb, x, y, C, k, r)
    for (x, y, r) in ((-7.0, 6.5, 0.5), (-5.8, 20.0, -0.4), (-10.4, 22.5, 1.0), (7.4, 14.0, 0.3), (6.0, 30.0, 0.9), (-8.5, 31.0, 0.2), (-6.5, 35.5, -0.8)): newspaper(mb, x, y, r, C)
    lg.done((-8, 15, 1), px=2.5)
    ab = U.Pt('aframe', (-8.6, 15.5, 1.5)); mb = ab.mb
    for sgn in (-1, 1):
        mb.pid += 1; mb.face([V((-5.4, 36.5 + 0, 0)), V((-3.8 - 0.2, 36.5, 0)), V((-4.0, 36.5 + 0.55 * sgn, 3.0)), V((-5.2, 36.5 + 0.55 * sgn, 3.0))], TX('sign_gap', 1.0, 2.0, glow='sign_gap', glow_k=0.3) if sgn < 0 else C('#ffd22a', 1.0, 2.0), UV_)
    ab.done((-4.6, 36.5, 1.5), px=3)
    # MIND THE GAP edge boards, fire bucket, a wall lamp box
    kd = U.Pt('edge_signs', (0, 15, 1)); mb = kd.mb
    for yy in (10.0, 30.0): mb.pid += 1; mb.face([V((-PE - 0.1, yy, 0.12)), V((-PE - 0.1, yy + 2.4, 0.12)), V((-PE - 0.1, yy + 2.4, 0.6)), V((-PE - 0.1, yy, 0.6))], E('gapb%d' % yy, 'sign_gap', k=1.3), [(1, 0), (0, 0), (0, 1), (1, 1)])
    kd.done((0, 15, 1), px=2.5)
    # light pools on the floor
    pools = U.Pt('light_pools', ink=False, shadow=False)
    for (gx, yy, gz) in gpos: B.plane(pools.mb, (gx - 4.5, yy - 4.5, 0.07), (9, 0, 0), (0, 9, 0), E('pool', 'halo_warm', k=0.42, additive=True), (0, 0, 1, 1))
    pools.done()
    CUR['gpos'] = gpos
    # ---- the red train (moves with set_train); only the tunnel is behind the hole
    if with_train: build_train()
    if crowd: build_platform_people(shot)

UV_ = [(0, 0), (1, 0), (1, 1), (0, 1)]

def old_map_mat():
    """Same material as the lodgings old map (beck_hq: TX('old_map', 1.15, 1.0, glow='old_map', glow_k=0.55) under the LODGINGS preset): built while STATE['P'] is the LODGINGS preset so the tone matches s04."""
    from mine import _untoon
    keep = STATE['P']; STATE['P'] = dict(B.LIGHTS['LODGINGS'])
    try: m = _untoon(T.mat_lit('BK_oldmap_lodg', image=STATE['tx']['old_map'], gain=1.15, shade_mul=1.0, form=tuple(STATE['P']['form']), glow=STATE['tx']['old_map'], glow_k=0.55))
    finally: STATE['P'] = keep
    return m

def build_train(y_front=60.0, n_cars=3, car=15.0):
    C, TX, E, CARD = _cs(); L_ = n_cars * car; X = V((1, 0, 0))
    tf = TX('train_front', 1.0, 1.4, glow='train_front_glow', glow_k=0.7, smix=0.15); ts_ = TX('train_side', 1.0, 2.2, glow='train_side_glow', glow_k=0.9, smix=0.15)
    red = C('#e3262b', 1.0, 2.8, smix=0.15); dark = C('#8a1018', 1.0, 2.0); HW = 2.7; z0, z1 = -0.9, 4.9
    tr = U.Pt('train', (0, y_front, 2), hd=10); mb = tr.mb
    mb.box((-HW, y_front, z0), (HW, y_front + L_, z1), red, mats={'front': tf}, skip='left,right'); mb.box((-HW - 0.2, y_front - 0.1, z1), (HW + 0.2, y_front + L_, z1 + 0.25), dark)
    mb.box((-HW - 0.1, y_front, z0 - 0.3), (HW + 0.1, y_front + L_, z0 + 0.4), dark)
    # side faces with the windowed texture, repeated once per car (u runs along y; the -x side is seen from the near platform)
    mb.pid += 1; mb.face([V((HW, y_front, z0)), V((HW, y_front + L_, z0)), V((HW, y_front + L_, z1)), V((HW, y_front, z1))], ts_, [(0, 0), (n_cars, 0), (n_cars, 1), (0, 1)])
    mb.pid += 1; mb.face([V((-HW, y_front + L_, z0)), V((-HW, y_front, z0)), V((-HW, y_front, z1)), V((-HW, y_front + L_, z1))], ts_, [(n_cars, 0), (0, 0), (0, 1), (n_cars, 1)])
    o = tr.done((0, y_front, 2), px=3); TRAIN['objs'].append(o); TRAIN['base'].append(V(o.location)); TRAIN['y0'] = y_front
    # doors: closed (red panel + cream frame) and open (warm lit interior), two per car on both sides, at car-local 3.5 and 11.0
    dc = U.Pt('doors_closed', ink=False, shadow=False); do = U.Pt('doors_open', ink=False, shadow=False)
    for k in range(n_cars):
        for off in (3.5, 11.0):
            for sx in (-1, 1):
                y_a = y_front + k * car + off - 1.0; xx = sx * (HW + 0.05); zz0, zz1 = z0 + 0.55, z1 - 0.9
                for part, mat in ((dc, C('#fff0c8', 1.1, 1.5)), (do, E('door_open', color='#ffc870', k=1.0))):
                    pts = [V((xx, y_a, zz0)), V((xx, y_a + 2.0, zz0)), V((xx, y_a + 2.0, zz1)), V((xx, y_a, zz1))]
                    if sx < 0: pts = pts[::-1]
                    part.mb.pid += 1; part.mb.face(pts, mat, UV_)
    for part in (dc, do):
        o = part.done((0, y_front + L_ / 2, 2), px=2.5); TRAIN['objs'].append(o); TRAIN['base'].append(V(o.location))
    TRAIN['doors_closed'] = [TRAIN['objs'][-2]]; TRAIN['doors_open'] = [TRAIN['objs'][-1]]; TRAIN['doors_open'][0].hide_render = True
    hl = U.Pt('headlights', ink=False, shadow=False); mb = hl.mb
    for hx_ in (-1.6, 1.6):
        mb.pid += 1; mb.face([V((hx_ + 0.5 * math.cos(2 * math.pi * i / 16), y_front - 0.1, 2.4 + 0.5 * math.sin(2 * math.pi * i / 16))) for i in range(16)], E('headl', color='#ffe9b0', k=1.6), [(0, 0)] * 16)
        B.halo_card(mb, (hx_, y_front - 0.3, 2.4), 4.6, E('hh2', 'halo_warm', k=0.7, additive=True)); B.halo_card(mb, (hx_, y_front - 0.3, 2.4), 2.2, E('hh3', 'halo_white', k=0.7, additive=True))
    B.plane(mb, (-3.6, y_front - 30.0, TZ + 0.06), (7.2, 0, 0), (0, 30.0, 0), E('spill', 'halo_warm', k=0.8, additive=True), (0, 0, 1, 1))
    o = hl.done(); TRAIN['objs'].append(o); TRAIN['base'].append(V(o.location))
    sp = U.spot('headlamp', (0, y_front - 1.5, 2.6), (-5.0, y_front - 22.0, 1.0), (1.0, 0.78, 0.45), 14000, 55, 0.5, 0.5)
    TRAIN['lights'].append((sp, V(sp.location)))
    pl_ = U.pl('train_cab', (0, y_front + 4.0, 4.0), (1.0, 0.8, 0.5), 700, 0.5); TRAIN['lights'].append((pl_, V(pl_.location)))

def set_train(y_front):
    """Move the train so its front is at hall y = y_front (start 60 = inside the tunnel, stopped at the platform: 6)."""
    dy = float(y_front) - TRAIN['y0']
    for o, b in zip(TRAIN['objs'], TRAIN['base']): o.location = b + V((0, dy, 0))
    for o, b in TRAIN['lights']: o.location = b + V((0, dy, 0))

def set_doors(k):
    """k 0..1: doors open (warm lit interior) when k > 0.5."""
    for o in TRAIN['doors_open']: o.hide_render = not (k > 0.5)
    for o in TRAIN['doors_closed']: o.hide_render = (k > 0.5)

# ----------------------------------------------------------------------------- people on the platform
def crowd(prefix, i, pose, mark, **kw):
    """cast22 crowd member i (pass_walk or a STORY22 pose name) as a camera-facing card; the raster cache is shared by variant (name = variant)."""
    sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast22')); sys.path.insert(0, os.path.join(B.PROJ, 'v3', 'cast'))
    import cast22
    c, p = cast22.crowd_member(i, pose)
    return U.actor('%s%02d' % (prefix, len(U.ACTORS)), (c, p), mark, **kw)

def build_platform_people(shot):
    """Platform life.  Named cast22 cards sit at MARKS (s10 and s03 end); the rest is crowd.  All face the camera."""
    U.view((-9, 3, 4)); rim = '#a8bcff'; rw = '#ffb878'
    rs = random.Random(5)
    # near platform (x -7 .. -4.4)
    for k, y in enumerate(np.arange(8.0 if shot != 's03' else 15.0, 38.0, 3.1)):
        crowd('np', (k * 5 + 3) % 16, 'pass_walk' if k % 3 else 'pass_tap_map', (-5.0 - rs.uniform(0, 1.8), y + rs.uniform(-.4, .4), 0.0), rim=rim if k % 2 else rw)
    # far platform (x 4.6 .. 10)
    for k, y in enumerate(np.arange(0.0, 40.0, 3.4)):
        crowd('fp', (k * 7 + 1) % 16, 'pass_walk', (5.2 + rs.uniform(0, 4.6), y + rs.uniform(-.4, .4), 0.0), rim=rim if k % 2 else rw, mirror=(k % 2 == 0))
    U.actor('sit_p1', 'clerk_sit_b', (10.9, 8.0, 1.45), rim='#ffb878', pose=dict(desk=0, typewriter=0)); U.actor('sit_p2', 'clerk_sit_c', (10.9, 10.4, 1.45), rim='#a8bcff', pose=dict(desk=0, typewriter=0))
    for nm, story, mk, kw in PEOPLE.get(shot, []):
        U.actor(nm, story, mk, **kw)

# named people per shot: (name, story, mark (x, y, z), kwargs)
PEOPLE = {
    's10': [('pass_woman', 'pass_unfold_map', (-5.2, 14.5, 0.0), dict(poses={'smile': 'pass_smile_board_woman'}, rim='#a8bcff')),
            ('pass_man', 'pass_read_map', (-6.4, 20.5, 0.0), dict(rim='#ffb878')), ('pass_child', 'pass_smile_board', (-4.9, 10.8, 0.0), dict(rim='#a8bcff')),
            ('porter', 'porter_walk', (-6.0, 30.0, 0.0), dict(rim='#ffb878')), ('official', 'off_peek', (-7.6, 12.4, 0.0), dict(poses={'jaw': 'off_jaw_drop'}, rim='#a8bcff', pose=dict(pillar=0)))],
    's03': [('old_gent', 'old_squint', (-10.3, 11.4, 0.0), dict(rim='#ffb878')), ('pass_man', 'pass_squint', (-11.0, 9.4, 0.0), dict(poses={'bump': 'pass_bump'}, rim='#a8bcff')),
            ('pass_woman', 'pass_unfold_map', (-6.6, 17.5, 0.0), dict(rim='#a8bcff')), ('porter', 'porter_walk', (-5.9, 30.0, 0.0), dict(rim='#ffb878'))],
}

# ============================================================================= the shaft, the cavern and the noodle tunnels ('under' world, s03)
def mat_tube(name, hexcol, k=2.2):
    """Translucent neon tube wall: transparent in the middle, glowing at the silhouette (layer weight facing), colour = the line colour."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.45
    mx = N('ShaderNodeMath'); mx.operation = 'MAXIMUM'; mx.inputs[1].default_value = 0.06
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*T.hex_lin(hexcol), 1.0); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mix = N('ShaderNodeMixShader')
    Lk(lw.outputs['Facing'], mx.inputs[0]); Lk(mx.outputs[0], mix.inputs['Fac']); Lk(tr.outputs['BSDF'], mix.inputs[1]); Lk(em.outputs['Emission'], mix.inputs[2]); Lk(mix.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def catmull(pts, n=10):
    P = [V(p) for p in pts]; out = []
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n; t2 = t * t; t3 = t2 * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2]); return out

def sweep(mb, pts, r, mat, n=14, uv_len=6.0):
    """Tube mesh along a polyline: rings of n points (parallel transport frame)."""
    T0 = (pts[1] - pts[0]).normalized(); ref = V((0, 0, 1)) if abs(T0.z) < 0.9 else V((1, 0, 0)); Nn = T0.cross(ref).normalized(); rings = []; s_ = 0.0; svals = []
    prev = pts[0]
    for i, p in enumerate(pts):
        t = ((pts[min(i + 1, len(pts) - 1)] - pts[max(i - 1, 0)])).normalized()
        Nn = (Nn - t * Nn.dot(t)).normalized(); Bn = t.cross(Nn)
        rings.append([p + (Nn * math.cos(2 * math.pi * k / n) + Bn * math.sin(2 * math.pi * k / n)) * r for k in range(n)]); s_ += (p - prev).length; svals.append(s_); prev = p
    mb.pid += 1
    for i in range(len(pts) - 1):
        for k in range(n):
            k2 = (k + 1) % n; mb.face([rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]], mat, [(k / n, svals[i] / uv_len), ((k + 1) / n, svals[i] / uv_len), ((k + 1) / n, svals[i + 1] / uv_len), (k / n, svals[i + 1] / uv_len)])

def noodle_curves():
    """The tangle: the platform tunnel's far end coils up through the cavern; 9 more tubes cross it at odd angles (seeded)."""
    rs = random.Random(17); cx, cy, cz = GX, GY + 38.0, -44.0; curves = []
    # the platform tube: straight, then coiling up into the knot
    curves.append(('green', [(GX, GY + 48, -59.6), (GX, GY + 58, -59.6), (GX + 14, GY + 70, -54), (GX + 30, GY + 62, -46), (GX + 40, GY + 76, -40)]))
    cols = ['blue', 'green', 'yellow', 'brown', 'black', 'red', 'blue', 'green', 'yellow']
    for i, col in enumerate(cols):
        n = rs.randint(6, 8); pts = []
        x, y, z = cx + rs.uniform(-55, 55), cy + rs.uniform(-30, 40), cz + rs.uniform(-14, 14)
        for k in range(n):
            pts.append((x, y, z)); x += rs.uniform(-28, 28); y += rs.uniform(-22, 22); z = max(-76, min(-30, z + rs.uniform(-12, 12))); x = max(GX - 96, min(GX + 96, x)); y = max(GY - 4, min(GY + 100, y))
        curves.append((col, pts))
    # two coils (helices)
    for j, (col, hx, hy) in enumerate((('blue', GX - 40, GY + 50), ('yellow', GX + 42, GY + 34))):
        pts = [(hx + 16 * math.cos(a), hy + 16 * math.sin(a), -66 + a * 1.4) for a in np.linspace(0, 6.5 * math.pi, 40)]; curves.append((col, pts))
    return curves

TUBE_RGB = dict(red='#ff3a40', blue='#3a6cff', green='#22d17a', yellow='#ffd23a', brown='#c8782a', black='#8a8aff')

def build_cavern(scene, P):
    C, TX, E, CARD = _cs(); rs = random.Random(9); U.set_org(0, 0, 0); U.view((GX, GY + 20, -40))
    # grate lid + pavement around it (the join with london: z 0 ground, opening GRATE_SIZE at GRATE_XY)
    hx, hy = GRATE_SIZE[0] / 2, GRATE_SIZE[1] / 2
    pv = U.Pt('pavement', ink=False, shadow=False); mb = pv.mb; ptx = TX('pave', 1.0, 1.0, form=False)
    B.plane(mb, (GX - 60, GY - 60, 0), (120, 0, 0), (0, 60 - hy, 0), ptx, (0, 0, 24, 12)); B.plane(mb, (GX - 60, GY + hy, 0), (120, 0, 0), (0, 60 - hy, 0), ptx, (0, 0, 24, 12))
    B.plane(mb, (GX - 60, GY - hy, 0), (60 - hx, 0, 0), (0, 2 * hy, 0), ptx, (0, 0, 12, 1.5)); B.plane(mb, (GX + hx, GY - hy, 0), (60 - hx, 0, 0), (0, 2 * hy, 0), ptx, (0, 0, 12, 1.5)); pv.done()
    gr = U.Pt('grate', (GX, GY, 0.1), ink=False); B.plane(gr.mb, (GX - hx, GY - hy, 0.06), (2 * hx, 0, 0), (0, 2 * hy, 0), TX('grate', 1.0, glow='grate_glow', glow_k=0.3), (0, 0, 1, 1)); gr.done()
    ba = U.Pt('grate_beams', (GX, GY, -0.4), hd=8); mb = ba.mb; iron = C('#26204e', 1.0, 1.2)
    for k in range(5): xx = GX - hx + (k + 0.5) * (2 * hx / 5); mb.box((xx - 0.2, GY - hy, -0.9), (xx + 0.2, GY + hy, -0.3), iron)
    ba.done((GX, GY, -0.4), px=3)
    sky = U.Pt('street_glow', ink=False, shadow=False); B.plane(sky.mb, (GX - hx, GY - hy, 0.5), (2 * hx, 0, 0), (0, 2 * hy, 0), E('sg', 'halo_warm', k=0.2, additive=True), (0, 0, 1, 1)); sky.done()
    U.pl('street_light', (GX, GY, 2.0), (1.0, 0.7, 0.4), 700, 1.0)
    # shaft: brick walls, iron ring ribs, ladder, cables, lamps
    ZB = -26.0; sh = U.Pt('shaft', (GX, GY, -12), ink=False); mb = sh.mb; bt = TX('brick', 1.0, 1.4, form=False)
    for (p0, pu, n_) in (((GX - hx, GY - hy, ZB), (2 * hx, 0, 0), 0), ((GX + hx, GY - hy, ZB), (0, 2 * hy, 0), 1), ((GX + hx, GY + hy, ZB), (-2 * hx, 0, 0), 2), ((GX - hx, GY + hy, ZB), (0, -2 * hy, 0), 3)):
        B.plane(mb, p0, pu, (0, 0, -ZB), bt, (0, 0, 4, 6))
    sh.done()
    rb = U.Pt('shaft_ribs', (GX, GY, -12), hd=8); mb = rb.mb; ric = C('#2f2b66', 1.0, 1.4); amber = C('#ffb352', 1.4)
    for z in np.arange(-3.0, ZB, -4.0):
        mb.box((GX - hx - 0.05, GY - hy - 0.05, z - 0.3), (GX + hx + 0.05, GY - hy + 0.5, z + 0.3), ric); mb.box((GX - hx - 0.05, GY + hy - 0.5, z - 0.3), (GX + hx + 0.05, GY + hy + 0.05, z + 0.3), ric)
        mb.box((GX - hx - 0.05, GY - hy, z - 0.3), (GX - hx + 0.5, GY + hy, z + 0.3), ric); mb.box((GX + hx - 0.5, GY - hy, z - 0.3), (GX + hx + 0.05, GY + hy, z + 0.3), ric)
    for xx in (GX - 1.1, GX + 1.1): rod(mb, (xx, GY + hy - 0.5, -0.5), (xx, GY + hy - 0.5, ZB + 0.5), 0.11, C('#c8d0ff', 2.0, 2.5), seg=5)    # ladder rails
    for z in np.arange(-1.0, ZB, -1.1): rod(mb, (GX - 1.1, GY + hy - 0.5, z), (GX + 1.1, GY + hy - 0.5, z), 0.07, C('#c8d0ff', 2.0, 2.5), seg=4)
    for (xx, yy, col) in ((GX - hx + 0.4, GY - 1.4, '#ff8a3a'), (GX - hx + 0.4, GY - 0.8, '#c8201e'), (GX + hx - 0.4, GY + 1.0, '#ffd22a'), (GX + hx - 0.4, GY + 1.6, '#1f49c8')):
        rod(mb, (xx, yy, -0.5), (xx, yy, ZB + 0.5), 0.14, C(col, 1.3, 2.0), seg=6)
    rb.done((GX, GY, -12), px=3)
    lh = U.Pt('shaft_lamps', ink=False, shadow=False); mb = lh.mb
    for z in np.arange(-5.0, ZB, -5.5):
        for (xx, yy) in ((GX - hx + 0.5, GY), (GX + hx - 0.5, GY)):
            mb.sphere((xx, yy, z), 0.4, E('shl', color='#ffd890', k=1.6), seg=8, rings=6); B.halo_card(mb, (xx, yy, z), 2.0, E('hsl', 'halo_warm', k=1.4, additive=True))
        U.pl('shaftL%d' % int(z), (GX, GY - 1.0, z), (1.0, 0.72, 0.4), 1500, 0.4)
    lh.done()
    # cavern: earth room (inside faces, strata), ceiling hole for the shaft; hall end wall is the front wall
    rm = U.Pt('cavern', ink=False); mb = rm.mb; st = E('strata_e', 'strata', k=1.6); y0, y1, x0, x1, z0, z1 = GY - 9.9, GY + 150.0, GX - 150.0, GX + 150.0, -96.0, ZB
    B.plane(mb, (x0, y0, z0), (x1 - x0, 0, 0), (0, y1 - y0, 0), st, (0, 0, 8, 4)); mb.pid += 1
    mb.face([V((x0, y0, z1)), V((x0, y1, z1)), V((x1, y1, z1)), V((x1, y0, z1))][::1] if False else [V((x0, y0, z1)), V((x1, y0, z1)), V((GX + hx, GY - hy, z1)), V((GX - hx, GY - hy, z1))], st, [(0, 0)] * 4)
    for (a, b, c_, d_) in (((x1, y0, z1), (x1, y1, z1), (GX + hx, GY + hy, z1), (GX + hx, GY - hy, z1)), ((x1, y1, z1), (x0, y1, z1), (GX - hx, GY + hy, z1), (GX + hx, GY + hy, z1)), ((x0, y1, z1), (x0, y0, z1), (GX - hx, GY - hy, z1), (GX - hx, GY + hy, z1))):
        mb.pid += 1; mb.face([V(a), V(b), V(c_), V(d_)], st, [(0, 0)] * 4)
    B.plane(mb, (x0, y0, z0), (0, y1 - y0, 0), (0, 0, z1 - z0), st, (0, 0, 4, 2)); B.plane(mb, (x1, y0, z0), (0, y1 - y0, 0), (0, 0, z1 - z0), st, (0, 0, 4, 2)); B.plane(mb, (x0, y1, z0), (x1 - x0, 0, 0), (0, 0, z1 - z0), st, (0, 0, 8, 2)); B.plane(mb, (x0, y0, z0), (x1 - x0, 0, 0), (0, 0, z1 - z0), st, (0, 0, 8, 2))
    rm.done()
    # cool and warm fills for the cavern
    for i, (xx, yy, zz, col, en) in enumerate(((GX - 30, GY + 30, -34, (0.35, 0.5, 1.0), 26000), (GX + 30, GY + 55, -44, (1.0, 0.65, 0.3), 26000), (GX, GY + 20, -55, (0.4, 0.55, 1.0), 20000), (GX + 10, GY + 80, -60, (1.0, 0.7, 0.35), 24000), (GX - 40, GY + 80, -48, (0.5, 0.5, 1.0), 20000), (GX, GY + 40, -40, (0.4, 0.55, 1.0), 20000))):
        U.pl('cav%d' % i, (xx, yy, zz), col, en, 2.0)
    # noodle tubes + trains inside
    nd = U.Pt('noodles', ink=False, shadow=False); mb = nd.mb
    for ci, (col, pts) in enumerate(noodle_curves()):
        path = catmull(pts, 8); sweep(mb, path, 1.7 if ci else 4.0, mat_tube('tube_%s_%d' % (col, ci), TUBE_RGB[col], 1.5), n=14)
    sweep(mb, [V((GX, y_, -59.6)) for y_ in np.linspace(GY - 10.0, GY + 52.0, 14)], 4.8, mat_tube('tube_platform', '#3a8cff', 1.6), n=16)
    nd.done()
    tr = U.Pt('noodle_trains', ink=False, shadow=False); mb = tr.mb; red = E('nt_red', color='#ff4048', k=1.5); win = E('nt_win', color='#ffe6a0', k=3.4)
    for ci, (col, pts) in enumerate(noodle_curves()):
        path = catmull(pts, 8)
        for frac in ((0.2, 0.5, 0.8) if ci % 2 else (0.3, 0.7)):
            i = int(frac * (len(path) - 2)); t = (path[i + 1] - path[i - 1]).normalized(); p = path[i]; up = V((0, 0, 1)); sd = t.cross(up)
            if sd.length < 1e-3: continue
            sd.normalize(); up2 = sd.cross(t)
            obox(mb, p + up2 * -0.3, t, sd, up2, 3.4, 1.0, 0.9, E('nt_%s' % col, color=TUBE_RGB[col], k=1.3))
            obox(mb, p + up2 * 0.1, t, sd, up2, 3.0, 1.04, 0.25, win)
    tr.done()
    sl = U.Pt('signal_lamps', ink=False, shadow=False); mbs = sl.mb
    for ci, (col, pts) in enumerate(noodle_curves()):
        path = catmull(pts, 8)
        for frac in (0.1, 0.4, 0.65, 0.9):
            p = path[int(frac * (len(path) - 1))]; hc = E('sig%d' % ((ci + int(frac * 10)) % 3), color=['#ff7a3a', '#ffd060', '#7affc0'][(ci + int(frac * 10)) % 3], k=1.6)
            mbs.sphere(p + V((0, 0, 2.3)), 0.35, hc, seg=8, rings=6); B.halo_card(mbs, p + V((0, 0, 2.3)), 2.2, E('hsig', 'halo_warm', k=0.5, additive=True))
    sl.done()
    # earth detail: pipes, cables, iron props through the cavern, pebbles of light
    pp = U.Pt('props', ink=True, hd=18); mb = pp.mb
    for k in range(8):
        x = GX + rs.uniform(-70, 70); y = GY + rs.uniform(20, 110); rod(mb, (x, y, -26), (x, y, -96), 1.1, C('#3a3a88', 1.2, 1.6), seg=10); rod(mb, (x, y, -60), (x, y, -58.5), 1.7, C('#5a5ab8', 1.2, 1.6), seg=10)
    pp.done((GX, GY + 60, -60), px=3)
    # the platform hall, 62 D lower: its end wall is the cavern's front wall
    U.set_org(*ORG_HALL); CUR['open_tube'] = True
    build_hall(scene, P, with_train=False, crowd=True, shot='s03'); U.set_org(0, 0, 0)
    # tunnel lamps: a string of lights down the straight tube (world)
    tl = U.Pt('tube_lamps', ink=False, shadow=False)
    for k, yy in enumerate(np.arange(GY - 4.0, GY + 52.0, 3.0)): B.halo_card(tl.mb, (GX + (2.4 if k % 2 else -2.4), yy, -62.0 + 5.2), 2.2, E('tl%d' % (k % 2), 'halo_warm', k=1.3, additive=True))
    tl.done()
    [U.pl('tube_%d' % k, (GX, yy, -57.5), (1.0, 0.7, 0.4), 4000, 0.5) for k, yy in enumerate((GY + 44, GY + 30, GY + 16, GY + 2))]

def build_under_loc(scene, P):
    U.set_org(0, 0, 0); U.ensure_u(); build_cavern(scene, P)

# ============================================================================= the ticket hall (s09, s13)
HALL = dict(rack=[], stacks=[], crates=[], crowd=[], hi=6.0)
HX0, HX1, HY0, HY1, HZ = -22.0, 22.0, -12.0, 30.0, 14.0
STAND = (0.0, 10.0)

def pocket_box(mb, x, y, z, w, d, h, mat):
    mb.box((x - w / 2, y - d / 2, z), (x + w / 2, y + d / 2, z + h), mat)

def build_hall_loc(scene, P):
    C, TX, E, CARD = _cs(); rs = random.Random(8); U.set_org(0, 0, 0); U.ensure_u(); Y = V((0, 1, 0)); Z = V((0, 0, 1)); U.view((4, 0, 5))
    tw = TX('tiles', 0.7, 1.0, form=False); UVq = UV_
    r = U.Pt('room', ink=False); mb = r.mb
    B.plane(mb, (HX0, HY0, 0), (HX1 - HX0, 0, 0), (0, HY1 - HY0, 0), TX('hall_floor', 0.45, 1.2, form=False), (0, 0, 11, 10))
    B.plane(mb, (HX0, HY0, HZ), (HX1 - HX0, 0, 0), (0, HY1 - HY0, 0), TX('ceiling_tile', 0.8, 1.2, form=False), (0, 0, 11, 10))
    B.plane(mb, (HX0, HY1, 0), (HX1 - HX0, 0, 0), (0, 0, HZ), tw, (0, 0, 11, 3.5)); B.plane(mb, (HX0, HY0, 0), (HX1 - HX0, 0, 0), (0, 0, HZ), tw, (0, 0, 11, 3.5))
    B.plane(mb, (HX0, HY0, 0), (0, HY1 - HY0, 0), (0, 0, HZ), tw, (0, 0, 10, 3.5)); B.plane(mb, (HX1, HY0, 0), (0, HY1 - HY0, 0), (0, 0, HZ), tw, (0, 0, 10, 3.5))
    r.done()
    bm = U.Pt('beams', (0, 10, 12.5)); mb = bm.mb; mar = C('#8a2a58', 1.0, 1.6, smix=0.3)
    for yy in (-6.0, 4.0, 14.0, 24.0): mb.box((HX0, yy - 0.6, HZ - 1.2), (HX1, yy + 0.6, HZ), mar)
    for xx in (-14.0, 0.0, 14.0): mb.box((xx - 0.5, HY0, HZ - 0.8), (xx + 0.5, HY1, HZ), mar)
    mb.box((HX0, HY1 - 0.1, 5.2), (HX1, HY1 + 0.0, 5.8), mar); mb.box((HX0, HY0 + 0.1, 5.2), (HX1, HY0 + 0.2, 5.8), mar)
    bm.done((0, 10, 12.5), px=3)
    gl = U.Pt('lamps', (0, 10, 11), ink=True); mb = gl.mb; gh = U.Pt('lamp_halos', ink=False, shadow=False); gm = E('globe_h', color='#ffd890', k=1.1); gp = []
    for yy in (9.0, 18.0, 26.0):
        for xx in (-15.0, -7.5, 0.0, 7.5, 15.0):
            rod(mb, (xx, yy, HZ), (xx, yy, 10.6), 0.05, C('#2a2250'), seg=4); mb.sphere((xx, yy, 10.0), 0.55, gm, seg=12, rings=8); B.halo_card(gh.mb, (xx, yy, 10.0), 1.9, E('hgh', 'halo_warm', k=0.8, additive=True)); gp.append((xx, yy))
    gl.done((0, 10, 11), px=3); gh.done()
    for i, (xx, yy) in enumerate(gp):
        if i % 2 == 0 or yy in (9.0,): U.pl('hl%d' % i, (xx, yy, 9.2), (1.0, 0.72, 0.38), 800, 0.5)
    U.pl('hall_fill', (0, 4, 6), (0.5, 0.6, 1.0), 900, 2.0)
    # entrance (front wall, y = HY0): glowing dusk-blue/orange doorway + WAY OUT
    en = U.Pt('entrance', ink=False, shadow=False); B.plane(en.mb, (-6, HY0 + 0.05, 0.0), (12, 0, 0), (0, 0, 8.5), E('dusk_door', color='#4a62d8', k=1.5), (0, 0, 1, 1)); B.plane(en.mb, (-6, HY0 + 0.08, 0.0), (12, 0, 0), (0, 0, 2.6), E('dusk_door2', color='#ffa24a', k=1.4), (0, 0, 1, 1)); en.done()
    ef = U.Pt('entrance_frame', (0, HY0, 4)); mb = ef.mb; stn = C('#d8c498', 1.0, 1.4)
    mb.box((-7.0, HY0, 0), (-6.0, HY0 + 1.0, 9.5), stn); mb.box((6.0, HY0, 0), (7.0, HY0 + 1.0, 9.5), stn); mb.box((-7.0, HY0, 8.5), (7.0, HY0 + 1.0, 9.5), stn); ef.done((0, HY0, 4), px=3)
    ws = U.Pt('way_out_sign', ink=True); mb = ws.mb; mb.pid += 1
    mb.face([V((-3.2, HY0 + 1.1, 9.8)), V((3.2, HY0 + 1.1, 9.8)), V((3.2, HY0 + 1.1, 11.5)), V((-3.2, HY0 + 1.1, 11.5))], E('exit_sign', 'sign_exit', k=1.6), UVq); ws.done((0, HY0, 10), px=3)
    # back wall: ticket booths + TICKETS signs; escalator heads TO TRAINS
    tb = U.Pt('ticket_booths', (-10, HY1 - 2, 3)); mb = tb.mb; wood = C('#8a4a22', 1.0, 2.0, smix=0.3); dwood = C('#4a2410', 1.0, 1.8)
    mb.box((-19.0, HY1 - 2.6, 0), (-1.0, HY1 - 0.2, 3.6), wood); mb.box((-19.4, HY1 - 3.0, 3.6), (-0.6, HY1 - 0.1, 4.0), dwood)
    for k in range(4):
        x0 = -17.5 + k * 4.2; mb.box((x0, HY1 - 2.75, 1.0), (x0 + 3.0, HY1 - 2.55, 3.4), C('#ffd88a', 1.8)); mb.box((x0 - 0.12, HY1 - 2.8, 0.95), (x0 + 3.12, HY1 - 2.5, 1.15), dwood)
    tb.done((-10, HY1 - 2, 3), px=3)
    ts = U.Pt('tickets_signs', ink=True); mb = ts.mb
    for k in range(2):
        x0 = -18.5 + k * 8.2; mb.pid += 1; mb.face([V((x0, HY1 - 3.1, 4.1)), V((x0 + 6.0, HY1 - 3.1, 4.1)), V((x0 + 6.0, HY1 - 3.1, 5.5)), V((x0, HY1 - 3.1, 5.5))], E('tk%d' % k, 'sign_tickets', k=1.6), UVq)
    mb.pid += 1; mb.face([V((6.0, HY1 - 0.1, 7.8)), V((16.0, HY1 - 0.1, 7.8)), V((16.0, HY1 - 0.1, 10.0)), V((6.0, HY1 - 0.1, 10.0))], E('tt', 'sign_to_trains', k=1.6), UVq); ts.done((0, HY1, 6), px=3)
    esc = U.Pt('escalators', (11, HY1 - 4, 2)); mb = esc.mb; stl = C('#c8d0ff', 1.8, 2.0, smix=0.1); dk = C('#14143a')
    for x0 in (6.5, 12.0):
        mb.box((x0, HY1 - 9.0, -0.2), (x0 + 3.4, HY1, 0.1), dk)
        for k in range(8): mb.box((x0 + 0.1, HY1 - 8.5 + k * 1.0, 0.1 - k * 0.0), (x0 + 3.3, HY1 - 7.6 + k * 1.0, 0.45 - k * 0.0), C('#5a5a8a', 1.4, 1.6))
        mb.box((x0 - 0.15, HY1 - 9.0, 0.1), (x0 + 0.1, HY1, 3.0), stl); mb.box((x0 + 3.3, HY1 - 9.0, 0.1), (x0 + 3.55, HY1, 3.0), stl)
        mb.box((x0 + 0.1, HY1 - 0.4, 0), (x0 + 3.3, HY1, 8.0), dk)
    esc.done((11, HY1 - 4, 2), px=3)
    # side walls: posters, a big pocket-map notice, MAPS sign
    ps = U.Pt('posters_h', ink=True); mb = ps.mb
    for k, yy in enumerate((2.0, 8.0, 14.0, 20.0, 26.0)):
        mb.pid += 1; mb.face([V((HX0 + 0.08, yy, 3.0)), V((HX0 + 0.08, yy + 4.0, 3.0)), V((HX0 + 0.08, yy + 4.0, 8.2)), V((HX0 + 0.08, yy, 8.2))], TX('poster%d' % (k % 6), 1.0, 1.0, glow='poster%d' % (k % 6), glow_k=0.35), UVq)
        mb.pid += 1; mb.face([V((HX1 - 0.08, yy + 4.0, 3.0)), V((HX1 - 0.08, yy, 3.0)), V((HX1 - 0.08, yy, 8.2)), V((HX1 - 0.08, yy + 4.0, 8.2))], TX('poster%d' % ((k + 3) % 6), 1.0, 1.0, glow='poster%d' % ((k + 3) % 6), glow_k=0.35), UVq)
    ps.done((0, 14, 5), px=3)
    # the leaflet stand: wood unit, shelf, rack of pockets, sign TRIAL MAP
    sx, sy = STAND; st = U.Pt('stand', (sx, sy, 2.5)); mb = st.mb
    mb.box((sx - 3.2, sy - 1.0, 0), (sx + 3.2, sy + 1.0, 1.9), wood); mb.box((sx - 3.4, sy - 1.15, 1.9), (sx + 3.4, sy + 1.15, 2.1), dwood)
    mb.box((sx - 3.2, sy + 0.9, 2.1), (sx + 3.2, sy + 1.1, 6.2), wood); mb.box((sx - 3.4, sy + 0.8, 6.2), (sx + 3.4, sy + 1.2, 6.5), dwood)
    for r_ in range(5):
        mb.box((sx - 3.0, sy + 0.2, 2.4 + r_ * 0.78), (sx + 3.0, sy + 0.95, 2.45 + r_ * 0.78), dwood)
    st.done((sx, sy, 2.5), px=3)
    for key, im in (('trial', 'sign_trial'), ('real', 'sign_new_pocket')):
        sg = U.Pt('stand_sign_' + key, ink=True); B_ = sg.mb; B_.pid += 1
        B_.face([V((sx - 2.4, sy - 1.2, 6.7)), V((sx + 2.4, sy - 1.2, 6.7)), V((sx + 2.4, sy - 1.2, 8.5)), V((sx - 2.4, sy - 1.2, 8.5))], E('ss_' + key, im, k=1.7), UVq)
        rod(B_, (sx - 2.0, sy - 1.1, 6.5), (sx - 2.0, sy - 1.1, 6.8), 0.08, C('#222244')); rod(B_, (sx + 2.0, sy - 1.1, 6.5), (sx + 2.0, sy - 1.1, 6.8), 0.08, C('#222244')); HALL.setdefault('signs', {})[key] = sg.done((sx, sy, 7.5), px=3)
    cover = TX('pocket_cover', 1.1, 1.2, form=False)
    for r_ in range(5):
        for c_ in range(10):
            o = U.Pt('rack_%d_%d' % (r_, c_), ink=False); o.mb.pid += 1
            x0 = sx - 2.8 + c_ * 0.62; z0 = 2.5 + r_ * 0.78; o.mb.face([V((x0, sy + 0.18, z0)), V((x0 + 0.5, sy + 0.18, z0)), V((x0 + 0.5, sy + 0.18, z0 + 0.66)), V((x0, sy + 0.18, z0 + 0.66))], cover, UVq)
            HALL['rack'].append(o.done())
    for k, (dx, n) in enumerate(((-2.2, 3), (0.0, 2), (2.2, 3))):
        o = U.Pt('stack_%d' % k, ink=True, hd=8); mb = o.mb
        for j in range(n): pocket_box(mb, sx + dx, sy - 0.2, 2.1 + j * 0.16, 0.9, 0.7, 0.15, C('#f6ecd0', 1.1, 1.4)); mb.box((sx + dx - 0.45, sy - 0.55, 2.1 + j * 0.16 + 0.05), (sx + dx + 0.45, sy - 0.54, 2.1 + j * 0.16 + 0.12), C('#e3262b', 1.2, 1.5))
        HALL['stacks'].append(o.done((sx + dx, sy, 2.4), px=2.5))
    # columns, kiosk, benches, bins, luggage, crates
    cl = U.Pt('columns_h', (0, 14, 5)); mb = cl.mb; cm = TX('tiles', 1.0, 1.0, form=False); cap = C('#a82838', 1.0, 1.5)
    for (x, y) in ((-10.0, 4.0), (10.0, 4.0), (-9.6, 15.9), (10.0, 18.0), (-10.0, 26.0), (10.0, 26.0)): column(mb, x, y, 1.5, HZ - 0.4, cm, cap)
    cl.done((0, 14, 5), px=3)
    ki = U.Pt('kiosk', (-17, 5, 3)); mb = ki.mb
    mb.box((-20.6, 2.0, 0), (-16.2, 6.5, 3.2), C('#2f6a4a', 1.0, 2.0, smix=0.2)); mb.box((-20.9, 1.7, 3.2), (-15.9, 6.8, 3.6), C('#e3262b', 1.0, 1.6)); mb.box((-16.3, 2.4, 1.2), (-16.1, 6.1, 2.8), C('#ffd88a', 1.8))
    for k in range(5): mb.box((-16.3, 2.6 + k * 0.7, 1.0), (-16.0, 3.2 + k * 0.7, 1.6), C(['#f6ecd0', '#ffc81e', '#e3262b', '#fff6e0', '#bcd0ff'][k], 1.2, 1.4))
    mb.pid += 1; mb.face([V((-16.2, 2.4, 3.7)), V((-16.2, 6.4, 3.7)), V((-16.2, 6.4, 5.0)), V((-16.2, 2.4, 5.0))], E('kiosk_news', 'sign_news', k=1.6), UVq); ki.done((-17, 5, 3), px=3)
    bn = U.Pt('benches_h', (0, 14, 1)); mb = bn.mb
    for (x, y0_, y1_, bk) in ((-20.6, 12.0, 18.0, -1), (20.6, 12.0, 18.0, 1), (-6.0, 24.0, 30.0 - 6.5, 1)): bench(mb, x, y0_, y1_, bk)
    bn.done((0, 14, 1), px=3)
    lg = U.Pt('luggage_h', (0, 10, 1)); mb = lg.mb
    for (x, y, k, r_) in ((-14.0, 12.5, 0, 0.3), (-13.0, 14.0, 2, -0.4), (14.5, 8.0, 1, 0.5), (16.0, 12.0, 3, 0.1), (-4.0, 18.0, 2, 0.8), (6.0, 22.0, 0, 0.2), (-18.0, 20.0, 1, 0.6), (18.0, 22.0, 3, 0.0)): luggage(mb, x, y, C, k, r_)
    for (x, y, r_) in ((-6.0, 5.0, 0.4), (8.0, 14.0, -0.3), (-2.0, 20.0, 0.9), (12.0, 6.0, 0.1), (-12.0, 8.0, 1.2), (4.0, 2.0, -0.7)): newspaper(mb, x, y, r_, C)
    for (x, y) in ((-20.0, 10.0), (20.0, 10.0), (20.0, 24.0)): bin_(mb, x, y, C)
    lg.done((0, 10, 1), px=3)
    for k, (cx, cy) in enumerate(((-6.5, 5.0), (-4.2, 6.2), (-6.0, 7.4), (-5.0, 5.8))):
        o = U.Pt('crate_%d' % k, ink=True, hd=8); mb = o.mb; cmat = TX('crate_reprint', 1.0, 1.6, form=False)
        zz = 0.0 if k < 3 else 2.0; mb.box((cx - 1.0, cy - 0.8, zz), (cx + 1.0, cy + 0.8, zz + 1.9), cmat, mats={'right': cmat, 'front': cmat, 'left': cmat, 'back': cmat}); HALL['crates'].append(o.done((cx, cy, 1), px=3))
    pools = U.Pt('pools_h', ink=False, shadow=False)
    for (xx, yy) in gp: B.plane(pools.mb, (xx - 4.0, yy - 4.0, 0.06), (8, 0, 0), (0, 8, 0), E('pool_h', 'halo_warm', k=0.34, additive=True), (0, 0, 1, 1))
    pools.done()
    # people
    rm = '#ffb878'; rc = '#a8bcff'
    for nm, story, mk, kw in HALL_PEOPLE: U.actor(nm, story, mk, **kw)
    for k in range(34):
        x = rs.uniform(-17, 17); y = rs.uniform(-6, 24)
        if abs(x - STAND[0]) < 5 and abs(y - STAND[1]) < 3.2: x += 7 if x >= 0 else -7
        c = crowd('hc', (k * 5 + 2) % 16, 'pass_walk', (x, y, 0.0), rim=rm if k % 2 else rc, mirror=(k % 3 == 0)); HALL['crowd'].append('hc%02d' % (len(U.ACTORS) - 1))
    for k in range(6):
        o = U.Pt('flutter_%d' % k, ink=False, shadow=False); o.mb.pid += 1
        o.mb.face([V((-0.45, -0.33, 0)), V((0.45, -0.33, 0)), V((0.45, 0.33, 0)), V((-0.45, 0.33, 0))], cover, UVq); fo = o.done(); fo.hide_render = True; HALL.setdefault('flutter', []).append(fo)
    HALL['crate_base'] = [V(c.location) for c in HALL['crates']]
    set_trial_stack(0); set_rack(0.0); set_reprint_crates(0); set_stand_sign('trial')
    U.actor('sit_h1', 'clerk_sit_a', (-19.4, 13.2, 1.45), rim='#a8bcff', pose=dict(desk=0, typewriter=0))
    U.actor('sit_h2', 'clerk_sit_c', (-19.4, 16.6, 1.45), rim='#ffb878', pose=dict(desk=0, typewriter=0))

HALL_PEOPLE = [('porter', 'porter_hand_map', (1.8, 7.6, 0.0), dict(rim='#ffb878')), ('pass_man', 'pass_read_map', (-5.0, 8.5, 0.0), dict(rim='#a8bcff')),
               ('pass_woman', 'pass_tap_map', (3.6, 6.2, 0.0), dict(rim='#ffb878')), ('official', 'off_peek', (-10.9, 17.4, 0.0), dict(poses={'rub': 'off_smug_rub'}, rim='#a8bcff', pose=dict(pillar=0))),
               ('beck', 'beck_proud', (8.0, 11.5, 0.0), dict(rim='#ffb878')), ('porter2', 'porter_push_crate', (-9.0, 4.0, 0.0), dict(rim='#ffb878', cast='porter')),
               ('pass_child', 'pass_smile_board', (5.4, 4.2, 0.0), dict(rim='#a8bcff'))]

def set_stand_sign(k):
    for n, o in HALL['signs'].items(): o.hide_render = (n != k)
B.SETTERS['set_stand_sign'] = set_stand_sign

def set_trial_stack(n):
    for i, o in enumerate(HALL['stacks']): o.hide_render = not (i < int(n))
@B.setter('set_trial_stack')
def _sts(n): set_trial_stack(n)
def set_rack(f):
    n = len(HALL['rack']); k = int(round(float(f) * n))
    for i, o in enumerate(HALL['rack']): o.hide_render = not (i < k)
B.SETTERS['set_rack'] = set_rack
def set_reprint_crates(n):
    for i, o in enumerate(HALL['crates']): o.hide_render = not (i < int(n))
B.SETTERS['set_reprint_crates'] = set_reprint_crates
def set_crowd(v):
    n, seed = (v if isinstance(v, (tuple, list)) else (v, 1)); names = list(HALL['crowd']); random.Random(seed).shuffle(names)
    for i, nm in enumerate(names):
        for ob in U.ACTORS[nm]['poses'].values(): ob.hide_render = not (i < int(n)); 
B.SETTERS['set_crowd'] = set_crowd

def _anim_s09(f, n):
    U.face_cards(); set_pose = U.set_pose
    set_pose('official', 'rub' if f >= 117 else 'main'); set_trial_stack(0 if f < 14 else 1 if f < 28 else 3)
def _anim_s13(f, n):
    U.face_cards(); set_rack(1.0 if f < 20 else max(0.0, 1.0 - (f - 20) / 35.0))
    for k, fo in enumerate(HALL['flutter']):
        t0 = 30 + k * 4; u = (f - t0) / 14.0
        if u < 0: fo.hide_render = True; continue
        u = min(1.0, u); fo.hide_render = False
        x0, y0, z0 = STAND[0] - 2.0 + k * 0.8, STAND[1] - 1.3, 4.0 - (k % 3) * 0.5
        fo.location = (x0 + (k - 2.5) * 0.5 * u, y0 - (2.0 + k * 0.3) * u, 0.07 + z0 * (1 - u) ** 1.6); fo.rotation_euler = (0.0 if u >= 1 else 1.1 * math.sin(u * 7 + k), 0.0, k * 0.9 + (0 if u >= 1 else u * 5))
    for k, (c, b) in enumerate(zip(HALL['crates'], HALL['crate_base'])):
        u = max(0.0, min(1.0, (f - 75 - k * 4) / 18.0)); c.hide_render = (f < 75 + k * 4); c.location = b + V((-22.0 * (1 - u), 0, 0))

# ============================================================================= the carriage (s11)
CAR = dict(map_objs={}, scroll=None, glow={})
def build_carriage_loc(scene, P):
    import beck_map as M
    C, TX, E, CARD = _cs(); rs = random.Random(11); U.set_org(0, 0, 0); U.ensure_u(); U.view((0, 0, 3)); UVq = UV_
    W2, Y0, Y1, WZ = 3.6, -12.0, 18.0, 3.7
    outl = [(-W2, 0.0), (-W2, WZ)] + [(W2 * math.cos(math.pi * (1 - i / 10.0)), WZ + 1.6 * math.sin(math.pi * (1 - i / 10.0))) for i in range(1, 10)] + [(W2, WZ), (W2, 0.0)]
    r = U.Pt('shell', ink=False); mb = r.mb; cream = C('#efe2bc', 0.4, 1.2, form=False); wn = C('#b87a3a', 1.0, 1.4)
    for (x0, z0), (x1, z1) in zip(outl, outl[1:]):
        mat = wn if z1 < 2.3 else cream
        mb.pid += 1; mb.face([V((x0, Y0, z0)), V((x1, Y0, z1)), V((x1, Y1, z1)), V((x0, Y1, z0))], mat, [(0, 0)] * 4)
    B.plane(mb, (-W2, Y0, 0), (2 * W2, 0, 0), (0, Y1 - Y0, 0), TX('wood_slats', 1.0, 1.5, form=False), (0, 0, 3, 14))
    B.plane(mb, (-W2, Y1, 0), (2 * W2, 0, 0), (0, 0, WZ + 1.6), C('#8a1018', 1.0, 1.6), (0, 0, 1, 1)); B.plane(mb, (-W2, Y0, 0), (2 * W2, 0, 0), (0, 0, WZ + 1.6), C('#8a1018', 1.0, 1.6), (0, 0, 1, 1)); r.done()
    # windows: black tunnel rushing past (scrolling streak texture), window frames
    m = bpy.data.materials.new('streak_mat'); nt = T._tree(m); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); tx = N('ShaderNodeTexImage'); em = N('ShaderNodeEmission'); tx.image = T._img(STATE['tx']['streak']); tx.extension = 'REPEAT'
    em.inputs['Strength'].default_value = 1.0; Lk(tc.outputs['UV'], mp.inputs['Vector']); Lk(mp.outputs['Vector'], tx.inputs['Vector']); Lk(tx.outputs['Color'], em.inputs['Color']); Lk(em.outputs['Emission'], out.inputs['Surface']); CAR['scroll'] = mp
    wp = U.Pt('windows', ink=False, shadow=False); mb = wp.mb
    wf = U.Pt('window_frames', (0, 3, 3)); fb = wf.mb; fm = C('#6a3a1a', 1.0, 1.6)
    for k in range(7):
        y0 = Y0 + 1.0 + k * 4.2
        for sx in (-1, 1):
            xx = sx * (W2 - 0.03); pts = [V((xx, y0, 2.4)), V((xx, y0 + 3.2, 2.4)), V((xx, y0 + 3.2, 4.1)), V((xx, y0, 4.1))]
            if sx > 0: pts = pts[::-1]
            mb.pid += 1; mb.face(pts, m, [(0, 0), (1, 0), (1, 1), (0, 1)] if sx < 0 else [(1, 0), (0, 0), (0, 1), (1, 1)])
            fb.box((xx - 0.08, y0 - 0.12, 2.3), (xx + 0.08, y0 + 3.32, 2.4), fm); fb.box((xx - 0.08, y0 - 0.12, 4.1), (xx + 0.08, y0 + 3.32, 4.2), fm); fb.box((xx - 0.08, y0 - 0.12, 2.3), (xx + 0.08, y0 + 0.02, 4.2), fm); fb.box((xx - 0.08, y0 + 3.18, 2.3), (xx + 0.08, y0 + 3.32, 4.2), fm)
    wp.done(); wf.done((0, 3, 3), px=3)
    # seats (moquette), backs, poles, straps, rails, lamps, line diagram strips, ads
    U.utex('line_strip', lambda: line_strip())
    sb = U.Pt('seats', (0, 3, 1)); mb = sb.mb; mq = TX('moquette', 1.1, 1.8, form=False)
    for sx in (-1, 1):
        for k in range(5):
            y0 = Y0 + 1.0 + k * 5.6; xs = sx * W2
            mb.box((xs - sx * 1.5 - (0 if sx > 0 else 0), y0, 0.8), (xs - 0.0, y0 + 5.2, 1.25) if sx > 0 else (xs + 1.5, y0 + 5.2, 1.25), mq) if False else None
            lo, hi = (W2 - 1.5, W2) if sx > 0 else (-W2, -W2 + 1.5)
            mb.box((lo, y0, 0.0), (hi, y0 + 5.2, 1.1), C('#3a2a1a')); mb.box((lo, y0, 1.1), (hi, y0 + 5.2, 1.4), mq); mb.box((hi - 0.2 if sx > 0 else lo, y0, 1.4), (hi if sx > 0 else lo + 0.2, y0 + 5.2, 2.5), mq)
    sb.done((0, 3, 1), px=3)
    po = U.Pt('poles', (0, 3, 3)); mb = po.mb; chrome = C('#d0d8ff', 2.0, 2.4, smix=0.1)
    for k in range(7):
        y = Y0 + 2.0 + k * 4.4
        for x in (-1.3, 1.3): rod(mb, (x, y, 0), (x, y, 4.6), 0.07, chrome, seg=6)
    for x in (-1.3, 1.3): rod(mb, (x, Y0, 4.6), (x, Y1, 4.6), 0.07, chrome, seg=6)
    for k in range(18):
        y = Y0 + 1.0 + k * 1.7; x = -1.3 if k % 2 else 1.3
        rod(mb, (x, y, 4.6), (x, y, 3.8), 0.03, C('#222244'), seg=4); mb.frustum((x, y, 3.8), (x, y + 0.02, 3.8), 0.17, 0.17, C('#8a5a2a', 1.0, 1.6), seg=8)
    po.done((0, 3, 3), px=3)
    lp = U.Pt('lamp_strips', ink=False, shadow=False); mb = lp.mb; lm = E('strip_l', color='#ffd890', k=0.9)
    for k in range(8):
        y = Y0 + 1.5 + k * 3.9; mb.box((-0.4, y, 5.15), (0.4, y + 1.8, 5.22), lm); B.halo_card(mb, (0, y + 0.9, 5.0), 3.2, E('hcl', 'halo_warm', k=0.3, additive=True))
        if k % 2 == 0: U.pl('cl%d' % k, (0, y + 0.9, 4.6), (1.0, 0.76, 0.46), 120, 0.4)
    lp.done()
    ds = U.Pt('diagram_strips', ink=True); mb = ds.mb
    for sx in (-1, 1):
        xx = sx * (W2 - 0.12) * 0.995; pts = [V((xx, Y0 + 1, 4.25)), V((xx, Y1 - 1, 4.25)), V((xx, Y1 - 1, 4.75)), V((xx, Y0 + 1, 4.75))]
        if sx > 0: pts = [V((xx, Y1 - 1, 4.25)), V((xx, Y0 + 1, 4.25)), V((xx, Y0 + 1, 4.75)), V((xx, Y1 - 1, 4.75))]
        mb.pid += 1; mb.face(pts, E('strip%d' % sx, 'line_strip', k=1.4), UVq)
        for k in range(4):
            y0 = Y0 + 2.5 + k * 7.0; p2 = [V((xx, y0, 1.5 + 0)), V((xx, y0 + 1.4, 0.0 + 1.5)), V((xx, y0 + 1.4, 3.0)), V((xx, y0, 3.0))] if False else None
    ds.done((0, 3, 4.4), px=2.5)
    # the pocket map in the hands of pass_woman: plane facing -y, texture = the mapworld paper
    U.utex('pocket_map', lambda: M.paper_image(1560, 1080, lw=0.36, title='UNDERGROUND', ring_names=True, paper='#e6cf9a'))
    mx, my, mz, mw, mh = -0.35, 9.0, 3.1, 1.9, 1.32
    mo = U.Pt('pocket_map', ink=True, hd=6); mo.mb.pid += 1
    mo.mb.face([V((mx - mw / 2, my, mz - mh / 2)), V((mx + mw / 2, my, mz - mh / 2)), V((mx + mw / 2, my, mz + mh / 2)), V((mx - mw / 2, my, mz + mh / 2))], E('pmap', 'pocket_map', k=0.55), UVq); CAR['map'] = mo.done((mx, my, mz), px=2.5)
    def uv2w(u, v): return (mx - mw / 2 + u / M.GW * mw, mz + mh / 2 - v / M.GH * mh)
    gl_r = U.Pt('glow_red', ink=False, shadow=False); mb = gl_r.mb; gm_ = E('mapglow', color='#ff7a6a', k=3.2, additive=True)
    pts = [uv2w(*p) for p in dict(M.DIAGRAM['lines'])['red']] if False else [uv2w(*p) for p in [l for l in M.DIAGRAM['lines'] if l[0] == 'red'][0][1]]
    for a, b in zip(pts, pts[1:]):
        d = V((b[0] - a[0], 0, b[1] - a[1])); Lr = d.length; d.normalize(); n_ = V((-d.z, 0, d.x)) * 0.05
        mb.pid += 1; mb.face([V((a[0], my - 0.02, a[1])) - n_, V((b[0], my - 0.02, b[1])) - n_, V((b[0], my - 0.02, b[1])) + n_, V((a[0], my - 0.02, a[1])) + n_], gm_, UVq)
    CAR['glow']['red'] = gl_r.done()
    gl_i = U.Pt('glow_ring', ink=False, shadow=False); x, z = uv2w(16, 9); B.halo_card(gl_i.mb, (x, my - 0.05, z), 0.55, E('mapglow2', 'halo_warm', k=2.6, additive=True)); CAR['glow']['ring'] = gl_i.done()
    gl_s = U.Pt('glow_station', ink=False, shadow=False); x, z = uv2w(5, 5); B.halo_card(gl_s.mb, (x, my - 0.05, z), 0.42, E('mapglow3', 'halo_white', k=2.6, additive=True)); CAR['glow']['station'] = gl_s.done()
    U.pl('mapl', (mx, my - 1.2, mz + 0.4), (1.0, 0.85, 0.6), 160, 0.3)
    set_map_glow(None)
    # people
    for nm, story, mk, kw in CAR_PEOPLE: U.actor(nm, story, mk, **kw)
    for k, (x, y, st) in enumerate(((-2.9, -4.5, 'clerk_sit_b'), (2.9, 1.0, 'clerk_sit_a'), (-2.9, 12.5, 'clerk_sit_c'))):
        U.actor('sit_c%d' % k, st, (x, y, 1.35), rim='#ffb878' if k % 2 else '#a8bcff', pose=dict(desk=0, typewriter=0))
    rm = '#ffb878'; rc = '#a8bcff'
    for k, (x, y) in enumerate(((-2.4, -6.0), (2.5, -3.0), (-2.5, -1.0), (1.0, 3.5), (-1.6, 13.0), (2.3, 12.0), (0.2, -9.0), (2.4, 15.5), (-2.4, 16.0), (-0.2, 1.2))):
        crowd('cc', (k * 3 + 1) % 16, 'pass_walk' if k % 2 else 'pass_read_paper', (x, y, 0.0), rim=rm if k % 2 else rc, mirror=(k % 2 == 0))

CAR_PEOPLE = [('pass_man', 'pass_squint', (2.4, 6.0, 0.0), dict(rim='#a8bcff', poses={'shrug': 'pass_read_map'})), ('pass_woman', 'pass_unfold_map', (-0.6, 11.0, 0.0), dict(rim='#ffb878', poses={'tap': 'pass_tap_map'}))]

def line_strip(W=2400, H=300):
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (W, H), '#f6ecd0'); d = ImageDraw.Draw(img); d.rectangle((0, 0, W, 24), fill='#e3262b'); d.rectangle((0, H - 24, W, H), fill='#e3262b')
    d.line((40, H // 2, W - 40, H // 2), fill='#e3262b', width=26); ft = BX.font(34, BX.FB)
    for k, nm in enumerate(['EALING', 'ACTON', 'KEW', 'BANK', 'OXFORD', 'EUSTON', 'ANGEL', 'BOW']):
        x = 160 + k * 290; d.ellipse((x - 26, H // 2 - 26, x + 26, H // 2 + 26), fill='white', outline='#1a1840', width=8); d.text((x, H // 2 - 56), nm, font=ft, fill='#1a1840', anchor='mb')
    return img

def set_map_glow(which, k=1.0):
    """which = None | 'red' | 'ring' | 'station' (the three taps of s11)."""
    for n, o in CAR['glow'].items(): o.hide_render = (n != which)
B.SETTERS['set_map_glow'] = lambda v: set_map_glow(*(v if isinstance(v, (tuple, list)) else (v,)))

def set_carriage_rock(t):
    """t in seconds: scrolls the tunnel streaks past the windows and rocks the camera (roll +-0.7 deg, bob 0.04 D)."""
    mp = CAR['scroll']
    if mp is not None: mp.inputs['Location'].default_value = (-(float(t) * 1.6) % 1.0, 0.0, 0.0)
    cam = bpy.context.scene.camera
    if cam is not None and not cam.animation_data:
        e = cam.rotation_euler.copy(); e.rotate_axis('Z', math.radians(0.7 * math.sin(float(t) * 7.0)) if False else 0.0)
        cam.location.z += 0.04 * math.sin(float(t) * 9.0); cam.rotation_euler = e
        cam.rotation_euler.rotate_axis('Y', math.radians(0.7 * math.sin(float(t) * 7.0)))
B.SETTERS['set_carriage_rock'] = set_carriage_rock

def _anim_s11(f, n):
    U.face_cards(); t = f / 30.0; set_carriage_rock(t)
    U.set_pose('pass_man', 'main' if f < 56 else 'shrug' if f > 66 else 'main'); U.set_pose('pass_woman', 'tap' if f > 114 else 'main')
    set_map_glow('red' if 120 <= f < 138 else 'ring' if 138 <= f < 156 else 'station' if f >= 156 else None)

def build_platform_loc(scene, P):
    U.set_org(0, 0, 0); U.ensure_u(); CUR['open_tube'] = False
    B.point_light('fill_dummy', (0, 0, 0.0), (0, 0, 0), 0, 0.1)
    build_hall(scene, P, shot='s10')

LOCATIONS = {'under': dict(build=build_under_loc, light='UNDER', sky=False, cam=dict(loc=(GX, GY, 6.0), look_at=(GX, GY, -30), lens=22)),
             'platform': dict(build=build_platform_loc, light='UNDER', sky=False, cam=dict(loc=(-10.5, 0.0, 3.6), look_at=(3, 14, 2.6), lens=30))}
SHOTS = {'s10': dict(location='platform', light='UNDER', f0=1197, f1=1301, cam=[(0, (-11.2, -3.0, 3.8), (3, 16, 2.6), 30), (103, (-11.0, 7.0, 3.9), (3, 26, 2.6), 30)], marks={}, state={'set_train': 6.0})}
B.SETTERS['set_train'] = set_train
B.SETTERS['set_doors'] = set_doors

def _s03_cam():
    hl = lambda x, y, z: (ORG_HALL[0] + x, ORG_HALL[1] + y, ORG_HALL[2] + z)
    kn = (GX, GY + 40, -46.0)
    return [(0, (GX, GY, 6.0), (GX, GY, -60.0), 22), (10, (GX, GY, -11.0), (GX, GY, -60.0), 22), (20, (GX, GY + 1, -25.0), (GX, GY + 20, -40.0), 24),
            (31, (GX - 31.4, GY + 19.3, -46.5), kn, 26), (41, (GX - 41.6, GY + 21.4, -45.2), kn, 26), (52, (GX + 6, GY + 30, -41.0), (GX - 4, GY + 62, -54.0), 26), (62, (GX, GY + 54, -58.4), (GX, GY + 20, -59.6), 24),
            (80, (GX, GY + 20, -59.6), (GX, GY - 20, -59.6), 22), (94, hl(0.5, 40.0, 2.6), hl(-4.0, 20.0, 2.8), 24), (112, hl(-2.0, 22.0, 5.0), hl(-10.0, 14.0, 3.2), 28), (131, hl(-3.9, 8.5, 5.0), hl(-10.4, 13.2, 3.2), 30)]
SHOTS['s03'] = dict(location='under', light='UNDER', f0=192, f1=324, cam=_s03_cam(), marks={}, state={})

LOCATIONS['hall'] = dict(build=build_hall_loc, light='HALL', sky=False, cam=dict(loc=(2, -8, 12.5), look_at=(0, 10, 5), lens=26))
LOCATIONS['carriage'] = dict(build=build_carriage_loc, light='CARRIAGE', sky=False, cam=dict(loc=(-1.4, -9, 2.9), look_at=(0.5, 4, 2.8), lens=28))
SHOTS['s09'] = dict(location='hall', light='HALL', f0=1005, f1=1197, animate={'a': lambda f, n: _anim_s09(f, n)}, state={'set_rack': 0.0, 'set_crowd': (22, 3), 'set_stand_sign': 'trial'}, marks={},
    cam=[(0, (2, -8, 12.5), (0, 10, 5), 26), (60, (3, -2, 6.5), (0, 10, 3.2), 28), (100, (4, -1, 3.0), (0, 11, 3.4), 30), (150, (3.0, 0.5, 2.3), (-9.5, 17, 3.2), 30), (191, (2.0, 2.5, 2.1), (-10.8, 17.4, 3.2), 32)])
SHOTS['s11'] = dict(location='carriage', light='CARRIAGE', f0=1301, f1=1485, animate={'a': lambda f, n: _anim_s11(f, n)}, state={}, marks={},
    cam=[(0, (-1.4, -9, 2.9), (0.5, 4, 2.8), 28), (50, (-1.0, -2, 2.9), (0.8, 6, 2.9), 28), (90, (-1.0, 3.5, 3.4), (-0.3, 9, 3.0), 30), (150, (-0.4, 7.2, 3.5), (-0.3, 9.2, 3.1), 34), (183, (-0.3, 8.4, 3.15), (-0.3, 9.2, 3.1), 44)])
SHOTS['s13'] = dict(location='hall', light='HALL', f0=1559, f1=1662, animate={'a': lambda f, n: _anim_s13(f, n)}, state={'set_rack': 1.0, 'set_crowd': (34, 5), 'set_stand_sign': 'real'}, marks={},
    cam=[(0, (3, 2, 3.6), (0, 10, 4.6), 28), (50, (6, -2, 8), (0, 12, 2.5), 28), (102, (9, -7, 10.5), (0, 12, 1.5), 26)])
SHOTS['s10'].update(animate={'a': lambda f, n: (set_train(max(6.0, 60.0 - 54.0 * min(1.0, f / 70.0) ** 0.8)), set_doors(1.0 if f > 78 else 0.0), U.set_pose('official', 'jaw' if f > 78 else 'main'), U.face_cards())})
SHOTS['s03']['animate'] = {'a': lambda f, n: (U.face_cards(), U.set_pose('pass_man', 'bump' if f > 95 else 'main'))}
