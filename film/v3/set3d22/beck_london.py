"""beck_london.py (builder A): london exterior, DUSK + NIGHT. JOIN COORDINATES are exported here (see API.md).
Locations: 'london' (light DUSK for s02, NIGHT for s15). Shots s02 and s15. The publicity room is built inside the HQ block (beck_hq.build_publicity_room)."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector as V
import beck as B
from beck import (STATE, Part, plane, facing_card, halo_card, point_light, pitched, setter, SETTERS, T, obox, rod, lumpy, MB, hull_at, sun_light)

# ---- joins (london world frame: 1 unit = 1 D, Z up, street ground z = 0, +y is away from the near pavement; HQ and station entrance row is y 24..34)
GROUND_Z = 0.0
GRATE_XY = (8.0, 19.0)                 # centre of the pavement grate; the grate quad spans x 4..12, y 15.5..22.5 at z 0.06. B's shaft top = this xy, z 0 (lid opening 8 x 7)
GRATE_SIZE = (8.0, 7.0)
LODGE_WIN = dict(center=(-30.5, -4.0, 10.4), size=(4.2, 4.4), normal=(0, 1, 0))     # Beck's window in london (house x -34..-20, y -16..-4, front faces +y). Pane plane y = -4.0
ROOM_WIN = dict(center=(6.6, 14.0, 5.0), size=(4.2, 4.4), normal=(0, 1, 0))        # the same window seen from inside the lodgings room (beck_hq room frame); room->london offset (-37.1, -18.0, 5.4)
PUB_WIN = dict(center=(0.0, 24.0, 10.96), size=(11.8, 6.4), normal=(0, -1, 0))     # PUBLICITY DEPT window in the HQ front wall (real opening). The publicity room is inside the HQ block, in london coordinates
PUB_ROOM = dict(x=(-14.0, 14.0), y=(24.8, 46.0), floor=7.4, ceiling=14.5)          # publicity room box (same coordinates in the london scene and in the beck_hq 'publicity' location)
HQ_BOX = dict(x=(-22.0, 22.0), y=(24.0, 48.0), z=(0.0, 22.0))        # the block is 22 deep so the publicity room behind the window is real
ENTRANCE_XY = (-33.0, 19.0)            # UNDERGROUND station entrance stair top
SHOTS = {}
LOCATIONS = {}


def hq_block(S, rs):
    """The Underground HQ: stone block 44 x 24 x 22 with a REAL opening for the PUBLICITY window (the camera flies through it) and the publicity room inside."""
    C, TX, E = S['C'], S['TX'], S['E']; X0, X1 = HQ_BOX['x']; Y0, Y1 = HQ_BOX['y']; Z0, Z1 = HQ_BOX['z']
    fac = TX('hq', 1.0, glow='hq_glow', glow_k=1.5); stone = C('#e4d2a4', 1.0); roofm = C('#3a4690')
    h = Part('hq', (0, 28, 12)); mb = h.mb
    mb.box((X0, Y0, Z0), (X1, Y1, Z1), stone, skip='front,top')
    wx0, wx1 = PUB_WIN['center'][0] - PUB_WIN['size'][0] / 2, PUB_WIN['center'][0] + PUB_WIN['size'][0] / 2
    wz0, wz1 = PUB_WIN['center'][2] - PUB_WIN['size'][1] / 2, PUB_WIN['center'][2] + PUB_WIN['size'][1] / 2; T_ = 0.8
    def piece(a, b, c, d):                                                              # front face slice with the matching UVs of the facade texture
        if b - a > 0.01 and d - c > 0.01: mb.pid += 1; mb.quad((a, Y0, c), (b - a, 0, 0), (0, 0, d - c), fac, ((a - X0) / (X1 - X0), c / Z1, (b - X0) / (X1 - X0), d / Z1))
    piece(X0, X1, Z0, wz0); piece(X0, X1, wz1, Z1); piece(X0, wx0, wz0, wz1); piece(wx1, X1, wz0, wz1)
    cr = C('#efe0b8', 1.0, 1.4)
    mb.pid += 1; mb.quad((wx0, Y0, wz0), (wx1 - wx0, 0, 0), (0, T_, 0), cr); mb.pid += 1; mb.quad((wx0, Y0 + T_, wz1), (wx1 - wx0, 0, 0), (0, -T_, 0), cr)
    mb.pid += 1; mb.quad((wx0, Y0 + T_, wz0), (0, -T_, 0), (0, 0, wz1 - wz0), cr); mb.pid += 1; mb.quad((wx1, Y0, wz0), (0, T_, 0), (0, 0, wz1 - wz0), cr)
    mb.box((wx0 - 0.5, Y0 - 0.35, wz0 - 0.5), (wx1 + 0.5, Y0 + 0.05, wz0), stone); mb.box((wx0 - 0.5, Y0 - 0.35, wz1), (wx1 + 0.5, Y0 + 0.05, wz1 + 0.5), stone)     # sill and lintel
    mb.box((X0 - 1, Y0 - 1, Z1), (X1 + 1, Y1 + 1, Z1 + 1.4), stone); mb.box((X0 - 1.4, Y0 - 1.4, Z1 + 1.4), (X1 + 1.4, Y1 + 1.4, Z1 + 2.2), C('#cdb888'))              # cornice
    mb.box((X0, Y0, Z1 + 2.2), (X1, Y1, Z1 + 3.0), roofm)
    for i in range(9): mb.box((-21 + i * 5.2, Y0 - 0.8, Z1 + 1.4), (-20 + i * 5.2, Y0, Z1 + 2.6), stone)                       # parapet balusters
    mb.box((-6, 27, Z1 + 3.0), (6, 32, Z1 + 6), C('#c9b080')); mb.box((12, 27, Z1 + 3.0), (18, 32, Z1 + 8), C('#7a4a2a')); rod(mb, (15, 29.5, Z1 + 8), (15, 29.5, Z1 + 11), 0.4, C('#262050'))
    mb.box((-20, Y0 - 0.6, 0), (20, Y0, 1.4), C('#8f7d5e'))                                                                     # plinth
    for i in range(7): mb.box((-20 + i * 6.6, Y0 - 0.8, 1.4), (-19.2 + i * 6.6, Y0, 7.5), C('#dccaa0'))                         # pilasters
    h.done((0, 28, 14))
    pl = Part('sign_publicity', (0, 24, 17), ink=False); plane(pl.mb, (-8.8, Y0 - 0.9, 14.9), (17.6, 0, 0), (0, 0, 2.9), E('pub', 'sign_publicity', k=1.9), (0, 0, 1, 1)); pl.done()
    import beck_hq as H
    H.build_publicity_room(S, S['P'], embed=True, ceiling=True)

def lodging_house(S):
    """Beck's lodging house: end of the near terrace x -34..-20, y -16..-4, front (the +y face, toward the HQ) with a REAL window opening LODGE_WIN."""
    C, TX, E = S['C'], S['TX'], S['E']; X0, X1, Y0, Y1, H = -34.0, -20.0, -16.0, -4.0, 25.0
    cx, cz = LODGE_WIN['center'][0], LODGE_WIN['center'][2]; w, h_ = LODGE_WIN['size']; wx0, wx1, wz0, wz1 = cx - w / 2, cx + w / 2, cz - h_ / 2, cz + h_ / 2
    brick = TX('brick', 1.0, 1.0); fr = TX('lodging', 1.0, 1.0, glow='lodging_glow', glow_k=2.2); cream = C('#f2e8c8', 1.0, 1.4)
    lh = Part('lodging', (-27, -10, 12)); mb = lh.mb
    mb.box((X0, Y0, 0), (X1, Y1, H), brick, skip='back,top')
    for (a, b, c, d) in ((X0, X1, 0, wz0), (X0, X1, wz1, H), (X0, wx0, wz0, wz1), (wx1, X1, wz0, wz1)):                # +y face: origin at the +x end so the normal faces +y
        if b - a > 0.01 and d - c > 0.01: mb.pid += 1; mb.quad((b, Y1, c), (a - b, 0, 0), (0, 0, d - c), fr, ((b - X0) / (X1 - X0), c / H, (a - X0) / (X1 - X0), d / H))
    T_ = 0.7
    mb.pid += 1; mb.quad((wx0, Y1 - T_, wz0), (wx1 - wx0, 0, 0), (0, T_, 0), cream); mb.pid += 1; mb.quad((wx0, Y1, wz1), (wx1 - wx0, 0, 0), (0, -T_, 0), cream)
    mb.pid += 1; mb.quad((wx0, Y1, wz0), (0, -T_, 0), (0, 0, wz1 - wz0), cream); mb.pid += 1; mb.quad((wx1, Y1 - T_, wz0), (0, T_, 0), (0, 0, wz1 - wz0), cream)
    mb.box((wx0 - 0.5, Y1, wz0 - 0.5), (wx1 + 0.5, Y1 + 0.5, wz0), cream); mb.box((wx0 - 0.5, Y1, wz1), (wx1 + 0.5, Y1 + 0.35, wz1 + 0.45), cream)                 # sill (a window box of red flowers on it) and lintel
    mb.box((wx0, Y1, wz0), (wx1, Y1 + 0.5, wz0 + 0.5), C('#6a3a1a')); 
    for i in range(6): lumpy(mb, (wx0 + 0.4 + i * 0.7, Y1 + 0.3, wz0 + 0.8), 0.28, C(['#e3262b', '#ffc81e', '#d1409a'][i % 3]), i, seg=6, rings=4)
    mb.box((X0 - 0.6, Y1 - 0.2, H), (X1 + 0.6, Y1 + 0.4, H + 1.0), C('#e8d8ae'))
    pitched(mb, X0 - 0.4, X1 + 0.4, Y0 - 0.4, Y1 + 0.4, H + 1.0, H + 1.0, 5.0, brick, C('#7a3a6a'))
    for cx_ in (-31, -23): mb.box((cx_ - .8, -12, H + 5.5), (cx_ + .8, -10, H + 9.5), brick); mb.box((cx_ - 1.0, -12.2, H + 9.5), (cx_ + 1.0, -9.8, H + 10.2), C('#4a3a30'))
    lh.done((-27, -10, 12))
    sg = Part('sign_rooms', ink=False); plane(sg.mb, (-30.0, Y1 + 0.08, 4.0), (5.2, 0, 0), (0, 0, 1.7), E('rooms', 'sign_rooms', k=1.7), (0, 0, 1, 1)); sg.done()
    point_light('lodge_in', (cx, -9.0, cz), (1.0, 0.7, 0.35), 600, 0.8); point_light('lodge_out', (cx, Y1 + 1.5, cz), (1.0, 0.7, 0.35), 700, 0.8)
    bw = Part('beck_window_glow', ink=False, shadow=False); halo_card(bw.mb, (cx, Y1 + 1.6, cz), 3.0, E('hbw', 'halo_warm', k=0.5, additive=True)); bw.done()


def build_london_world(scene, P):
    S = STATE; C, TX, E, CARD = S['C'], S['TX'], S['E'], S['CARD']; rs = random.Random(22)
    sun_light(P)
    # ---- ground: road, pavements, kerbs
    g = Part('ground', (0, 10, 0), ink=False); mb = g.mb
    plane(mb, (-160, -80, -0.05), (320, 0, 0), (0, 80, 0), TX('pave', 0.8), (0, 0, 40, 10))                     # far foreground ground
    plane(mb, (-160, -8, 0.0), (320, 0, 0), (0, 6, 0), TX('pave', 1.0), (0, 0, 40, 1))                          # near pavement
    plane(mb, (-160, -2, 0.0), (320, 0, 0), (0, 16, 0), TX('road', 1.0), (0, 0, 40, 2))                         # road
    plane(mb, (-160, 14, 0.0), (120, 0, 0), (0, 10, 0), TX('pave', 1.0), (0, 0, 15, 1)); plane(mb, (-26, 14, 0.0), (186, 0, 0), (0, 10, 0), TX('pave', 1.0), (0, 0, 22, 1))
    plane(mb, (-40, 14, 0.0), (14, 0, 0), (0, 0.5, 0), TX('pave', 1.0), (0, 0, 2, 1)); plane(mb, (-40, 22.5, 0.0), (14, 0, 0), (0, 1.5, 0), TX('pave', 1.0), (0, 0, 2, 1))   # far pavement with the stair well
    plane(mb, (-160, 24, -0.02), (320, 0, 0), (0, 52, 0), TX('pave', 0.8), (0, 0, 40, 6)); plane(mb, (-160, 110, -0.02), (320, 0, 0), (0, 26, 0), TX('pave', 0.8), (0, 0, 40, 3))   # ground behind HQ (river gap y 76-98)
    g.done()
    k = Part('kerbs', (0, 6, 0)); mb = k.mb; kc = C('#b8a890')
    mb.box((-160, -2.4, 0), (160, -2.0, 0.5), kc); mb.box((-160, 13.6, 0), (160, 14.0, 0.5), kc); k.done()
    hq_block(S, rs)
    # ---- station entrance: stone block, big roundel, lit canopy, steps down
    e = Part('entrance', (-33, 24, 8)); mb = e.mb; stone2 = C('#d8c498')
    mb.box((-44, 24, 0), (-22, 34, 18), stone2, mats={'front': TX('fac_a', 1.0, glow='fac_a_glow', glow_k=1.2)}, skip='top'); mb.box((-44.6, 23.4, 18), (-21.4, 34.6, 19.2), C('#cdb888'))
    mb.box((-44, 24, 0), (-41, 24.6, 7), C('#9a8868')); mb.box((-25, 24, 0), (-22, 24.6, 7), C('#9a8868'))
    mb.box((-41, 23.7, 0), (-25, 24.1, 6.6), C('#ffb352', 1.6))                                                        # lit doorway
    mb.box((-41.6, 23.0, 6.4), (-24.4, 24.4, 7.2), C('#9a8868'))                                                       # lintel
    for x in (-41.4, -24.6): rod(mb, (x, 13.6, 0), (x, 13.6, 6.5), 0.35, C('#262050'))                                  # canopy posts
    e.done((-33, 24, 10))
    cp = Part('canopy', (-33, 19, 6.8)); mb = cp.mb
    mb.box((-42.4, 13.2, 6.5), (-23.6, 23.6, 7.2), C('#1c2a68')); mb.box((-42.4, 13.0, 7.2), (-23.6, 23.8, 7.7), C('#e3262b'))
    cp.done((-33, 18, 7))
    cg = Part('canopy_glow', ink=False, shadow=False); plane(cg.mb, (-42.0, 13.4, 6.48), (18, 0, 0), (0, 10, 0), E('canopy', color='#ffc46a', k=2.2), (0, 0, 1, 1)); cg.done()
    rg = Part('roundel', ink=False); plane(rg.mb, (-40.4, 23.6, 8.2), (14.8, 0, 0), (0, 0, 9.2), E('roundel', 'roundel', k=1.5, alpha=True), (0, 0, 1, 1)); rg.done()
    bar = Part('canopy_bar', ink=False); plane(bar.mb, (-41.5, 13.1, 6.7), (17, 0, 0), (0, 0, 0.75), E('ugbar', 'sign_underground_bar', k=1.6), (0, 0, 1, 1)); bar.done()
    # steps down into the pit: dark walls, warm lit risers (the pavement has a hole here)
    st = Part('stairs', (-33, 19, 0)); mb = st.mb; wmat = C('#3a2a58')
    mb.box((-40, 14.5, -9.0), (-26, 22.5, -8.6), C('#12102a'))
    for i in range(9):
        z = -0.4 - i * 0.95; y0 = 14.5 + i * 0.9
        mb.box((-39.4, y0, z - 0.5), (-26.6, y0 + 0.9, z), C('#ffb352', 1.5 if i % 2 == 0 else 1.0))
    mb.box((-40.6, 14.0, -9), (-39.4, 23, 0), wmat); mb.box((-26.6, 14.0, -9), (-25.4, 23, 0), wmat); mb.box((-40.6, 22.4, -9), (-25.4, 23.4, 0), wmat)
    st.done((-33, 19, 0))
    pg = Part('pit_glow', ink=False, shadow=False); halo_card(pg.mb, (-33, 18.5, 1.5), 7.0, E('hpit', 'halo_warm', k=1.4, additive=True)); pg.done()
    point_light('pit_up', (-33, 19, 1.0), (1.0, 0.62, 0.3), 1200, 0.8)
    # ---- grate (pavement, warm light from below) near the middle of the far pavement
    gr = Part('grate', (8, 19, 0.1), ink=False); plane(gr.mb, (4, 15.5, 0.06), (8, 0, 0), (0, 7, 0), TX('grate', 1.0, glow='grate_glow', glow_k=0.9), (0, 0, 1, 1)); gr.done()
    gh = Part('grate_glow', ink=False, shadow=False); halo_card(gh.mb, (8, 19, 3.0), 4.5, E('hgr', 'halo_warm', k=0.25, additive=True)); plane(gh.mb, (-1.0, 13.5, 0.09), (18, 0, 0), (0, 11, 0), E('hgr2', 'halo_warm', k=0.5, additive=True), (0, 0, 1, 1)); gh.done()
    point_light('grate_up', (8, 19, 0.6), (1.0, 0.6, 0.25), 450, 0.8)
    lodging_house(S)
    # near-side terrace (roofs seen from above: dark foreground) x -80..-38
    tr = Part('terrace', (-60, -9, 12)); mb = tr.mb
    for i, x0 in enumerate(range(-102, -38, 8)):
        hgt = 19 + (i % 3) * 2.5
        pitched(mb, x0, x0 + 8, -14, -4, 0, hgt, 4.2, C(['#a8452c', '#b9764a', '#8f3a28'][i % 3]), C('#c4482c' if i % 2 else '#8a3a5a'), tx_front=TX(['fac_b', 'fac_a', 'fac_b'][i % 3], 1.0, glow=['fac_b_glow', 'fac_a_glow', 'fac_b_glow'][i % 3], glow_k=1.3))
        for cxo in (2.2, 5.8): mb.box((x0 + cxo - .6, -10.6, hgt + 2.2), (x0 + cxo + .6, -9.4, hgt + 5), C('#6a3020')); mb.box((x0 + cxo - .8, -10.8, hgt + 5), (x0 + cxo + .8, -9.2, hgt + 5.6), C('#3a2a30'))
    tr.done((-60, -9, 14))
    # ---- far side buildings flanking the HQ
    fl = Part('flank', (0, 30, 12)); mb = fl.mb
    xs = [(-90, -66, 15, 'fac_b'), (-66, -44, 17, 'fac_c'), (22, 44, 17, 'fac_b'), (44, 68, 18, 'fac_a'), (68, 96, 15, 'fac_c')]
    for x0, x1, hgt, t in xs:
        pitched(mb, x0, x1, 24, 33, 0, hgt, 3.0, C('#a8452c'), C('#c4482c'), tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
        for cx in np.linspace(x0 + 3, x1 - 3, 3): mb.box((cx - .7, 31, hgt + 2), (cx + .7, 32.4, hgt + 5.2), C('#6a3020')); mb.box((cx - .9, 30.8, hgt + 5.2), (cx + .9, 32.6, hgt + 5.8), C('#3a2a30'))
    fl.done((30, 30, 14))
    # ---- rooftop city beyond: rows of gabled blocks with chimneys (smoke)
    ct = Part('city', (0, 70, 12)); mb = ct.mb; chim = []
    for row, (y0, y1) in enumerate(((40, 52),)):
        x = -130 + rs.uniform(0, 6)
        while x < 130:
            w = rs.uniform(9, 17); hg = rs.uniform(7, 12)
            if (-23 < x < 23 and row == 0) or (x < -22 and x + w > -46 and row == 0) or (x < 0 < x + w and row == 0): x += w + 0.6; continue
            t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
            pitched(mb, x, x + w, y0, y1, 0, hg, rs.uniform(3, 5), C(rs.choice(['#a8452c', '#c08050', '#d9c49a', '#8f5a9a'])), C(rs.choice(['#c4482c', '#8a3a5a', '#4a56a0', '#b8742c'])), ridge_x=rs.random() < .7, tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
            for cx in (x + w * .3, x + w * .7):
                if rs.random() < .55: mb.box((cx - .6, (y0 + y1) / 2 - .6, hg + 2.6), (cx + .6, (y0 + y1) / 2 + .6, hg + 5.2), C('#7a3a2a')); chim.append((cx, (y0 + y1) / 2, hg + 5.4))
            x += w + rs.uniform(0.2, 1.2)
    ct.done((0, 70, 14))
    sm = Part('smoke', ink=False, shadow=False); mb = sm.mb; smat = C('#efe4f6', 1.3, 2.6, smix=0.2)
    sel = [c for i, c in enumerate(chim) if i % 2 == 0][:20]
    for (cx, cy, cz) in sel:
        for k in range(4):
            lumpy(mb, (cx + 1.0 * k + rs.uniform(-.3, .3), cy, cz + 1.6 + k * 2.0), 1.0 + k * 0.55, smat, rs.randint(1, 99), seg=8, rings=5, rough=0.18)
    sm.done()
    # ---- river, embankments, bridges
    rv = Part('river', ink=False, shadow=False); plane(rv.mb, (-300, 64, -1.0), (600, 0, 0), (0, 30, 0), E('river', 'river', k=1.1), (0, 0, 9, 1)); rv.done()
    em = Part('embank', (0, 110, 0)); mb = em.mb; ec = C('#9a8ab8')
    mb.box((-300, 62, -1.4), (300, 64, 2.0), ec); mb.box((-300, 94, -1.4), (300, 96, 2.0), ec)
    em.done((0, 70, 0), px=4)
    br = Part('bridge', (30, 74, 3)); mb = br.mb; bc = C('#e8d8b0'); bd = C('#2a2a60')
    mb.box((24, 60, 1.4), (36, 98, 2.6), bc); mb.box((23.4, 60, 2.6), (24.4, 98, 4.0), bd); mb.box((35.6, 60, 2.6), (36.6, 98, 4.0), bd)
    for y in (68, 79, 90): mb.box((25, y - 1.4, -1.2), (35, y + 1.4, 1.4), bc); mb.box((24.4, y - 2.4, 0.4), (35.6, y + 2.4, 1.4), C('#c8b890'))
    for y in (62, 72, 82, 92):
        for x in (24.0, 36.0): rod(mb, (x, y, 4.0), (x, y, 9.5), 0.28, C('#262050'))
    br.done((30, 74, 3), px=3)
    # second bridge (far, simple lattice) at x -70
    b2 = Part('bridge2', (-70, 74, 3)); mb = b2.mb
    mb.box((-76, 60, 1.4), (-64, 98, 2.4), C('#c04a3a'));
    for y in (66, 79, 92): mb.box((-76, y - .6, 2.4), (-75.2, y + .6, 12), C('#c04a3a')); mb.box((-64.8, y - .6, 2.4), (-64, y + .6, 12), C('#c04a3a')); mb.box((-76, y - .6, 12), (-64, y + .6, 12.8), C('#c04a3a'))
    b2.done((-70, 74, 3))
    bg = Part('bridge_lamps', ink=False, shadow=False); mb = bg.mb
    for y in (62, 72, 82, 92):
        for x in (24.0, 36.0): halo_card(mb, (x, y, 9.8), 2.4, E('hb', 'halo_warm', k=1.9, additive=True))
    bg.done()
    bg2 = Part('bridge_lamps2', ink=False, shadow=False)
    for y in (66, 79, 92): halo_card(bg2.mb, (-70, y, 13.2), 2.6, E('hb', 'halo_warm', k=1.9, additive=True))
    bg2.done()
    # south bank buildings
    sb = Part('southbank', (0, 92, 10)); mb = sb.mb
    x = -150
    while x < 150:
        w = rs.uniform(10, 18); hg = rs.uniform(8, 13); t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
        pitched(mb, x, x + w, 86, 98, 0, hg, 3.6, C('#b8603a'), C('#3a3550'), tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.6))
        for cx in (x + w * .3, x + w * .7):
            mb.box((cx - .5, 91, hg + 2), (cx + .5, 92, hg + 4.8), C('#7a3a2a'))
            for j in (-.25, .25): rod(mb, (cx + j, 91.5, hg + 4.8), (cx + j, 91.5, hg + 5.7), 0.22, C('#c4562a'), seg=6)
        x += w + 0.4
    sb.done((0, 92, 10), px=4)
    # dome (St Paul's-ish) and clock tower with a lit clock
    dm = Part('dome', (-45, 108, 20)); mb = dm.mb; dc = C('#cfc4a8', 1.0, 1.6, smix=0.4); dg = C('#e8b24a', 1.3)
    mb.box((-61, 98, 0), (-29, 122, 12), C('#e4d2a4'), mats={'front': TX('fac_a', 1.0, glow='fac_a_glow', glow_k=1.5)})
    mb.frustum((-45, 111, 12), (-45, 111, 26), 11, 10.5, dc, seg=24);
    for i in range(12): a = 2 * math.pi * i / 12; rod(mb, (-45 + 10.7 * math.cos(a), 111 + 10.7 * math.sin(a), 12.4), (-45 + 10.7 * math.cos(a), 111 + 10.7 * math.sin(a), 25), 0.45, C('#f0e4c8'), seg=5)
    mb.sphere((-45, 111, 26), 10.5, dc, seg=24, rings=10); mb.frustum((-45, 111, 36.5), (-45, 111, 41), 2.6, 2.4, C('#e4d2a4'), seg=12); mb.sphere((-45, 111, 43), 2.6, dg, seg=12, rings=8); rod(mb, (-45, 111, 45), (-45, 111, 50), 0.35, dg)
    for i in range(16):                                                                                                    # meridian ribs of the dome + a gold cornice ring + drum windows
        a = 2 * math.pi * i / 16; pts = [(-45 + 10.55 * math.sin(t_) * math.cos(a), 111 + 10.55 * math.sin(t_) * math.sin(a), 26 + 10.55 * math.cos(t_)) for t_ in np.linspace(0.1, 1.5, 7)]
        for p0, p1 in zip(pts, pts[1:]): rod(mb, p0, p1, 0.16, C('#e8dcc0'), seg=4)
    rod(mb, (-45, 111, 12.0), (-45, 111, 12.6), 11.4, C('#bfae88'), seg=24)
    dm.done((-45, 108, 20), px=3)
    ck = Part('clocktower', (52, 104, 25)); mb = ck.mb; tw = TX('fac_c', 1.0, glow='fac_c_glow', glow_k=1.6)
    mb.box((44, 96, 0), (60, 112, 30), C('#e4d2a4'), mats={'front': tw}); mb.box((45, 97, 30), (59, 111, 44), C('#d8c498')); mb.box((44, 96, 44), (60, 112, 46), C('#c8b080'))
    mb.box((46.5, 98.5, 46), (57.5, 109.5, 54), C('#c8b080')); mb.frustum((52, 104, 54), (52, 104, 68), 6.2, 0.2, C('#3a6a98'), seg=4); rod(mb, (52, 104, 68), (52, 104, 73), 0.3, dg)
    for px_, py_ in ((44.6, 96.6), (59.4, 96.6), (44.6, 111.4), (59.4, 111.4)): mb.frustum((px_, py_, 44), (px_, py_, 52), 1.0, 0.1, C('#c8b080'), seg=4); rod(mb, (px_, py_, 52), (px_, py_, 54), 0.1, dg)
    mb.box((45.4, 95.6, 31.4), (58.6, 96.0, 44.6), dg)
    ck.done((52, 104, 25), px=3)
    cf = Part('clockface', ink=False); plane(cf.mb, (46.6, 95.5, 33), (10.8, 0, 0), (0, 0, 10.8), E('clk', 'clock', k=1.5, alpha=True), (0, 0, 1, 1)); cf.done()
    # far field: filler rows of blocks, a glowing far ground, two skyline cards, so there is city all the way to the horizon
    ff = Part('farfield', (0, 200, 12), ink=False); mb = ff.mb
    plane(mb, (-3000, 100, -0.6), (6000, 0, 0), (0, 2600, 0), E('farground', 'farground_dark', k=1.0), (0, 0, 1, 1))
    for (y0, y1, hmin, hmax) in ((100, 114, 8, 12), (118, 134, 8, 13), (140, 160, 9, 14), (170, 196, 9, 14), (210, 244, 9, 14)):
        x = -260
        while x < 260:
            w = rs.uniform(12, 24); hg = rs.uniform(hmin, hmax); t = rs.choice(['fac_a', 'fac_b', 'fac_c'])
            if not (y0 == 100 and -66 < x < -26 or y0 == 100 and 40 < x < 64):
                pitched(mb, x, x + w, y0, y1, 0, hg, rs.uniform(2.4, 4), C('#8a3a2a'), C(rs.choice(['#3a3550', '#4a3a58', '#5a3a3a'])), ridge_x=rs.random() < .75, tx_front=TX(t, 1.0, glow=t + '_glow', glow_k=1.4))
                for cx in (x + w * .25, x + w * .6, x + w * .85):
                    if rs.random() < .6:
                        mb.box((cx - .4, (y0 + y1) / 2 - .4, hg + 2), (cx + .4, (y0 + y1) / 2 + .4, hg + 4.5), C('#7a3a2a'))
                        for j in (-.18, .18): rod(mb, (cx + j, (y0 + y1) / 2, hg + 4.5), (cx + j, (y0 + y1) / 2, hg + 5.3), 0.2, C('#c4562a'), seg=6)
            x += w + rs.uniform(0.3, 1.5)
    ff.done()
    sk = Part('skyline', ink=False, shadow=False)
    plane(sk.mb, (-340, 330, 0), (680, 0, 0), (0, 0, 105), E('sky1', 'skyline', k=1.15, alpha=True), (0, 0, 1, 1))
    plane(sk.mb, (-700, 600, 0), (1400, 0, 0), (0, 0, 150), E('sky2', 'skyline2', k=1.0, alpha=True), (0, 0, 1, 1)); sk.done()
    for n in ('river', 'embank', 'bridge', 'bridge2', 'bridge_lamps', 'bridge_lamps2'):
        bpy.data.objects[n].location.y += 12
    for n in ('bridge', 'bridge_lamps'): bpy.data.objects[n].location.x -= 46
    for n in ('bridge2', 'bridge_lamps2'): bpy.data.objects[n].location.x += 124
    stars = Part('stars', ink=False, shadow=False)
    for i in range(46):
        az = math.radians(rs.uniform(-34, 30)); el = math.radians(rs.uniform(3.5, 16)); d = 1500
        halo_card(stars.mb, (-13 + d * math.sin(az) * math.cos(el) * 0.0 + d * math.sin(az), -46 + d * math.cos(az) * math.cos(el), 70 + d * math.sin(el)), rs.uniform(3.0, 6.0), E('star', 'halo_white', k=2.6, additive=True))
    stars.done()
    for n in ('southbank', 'dome', 'clocktower', 'clockface', 'farfield'):
        bpy.data.objects[n].location.y += 24
    # ---- vehicles: red double-decker bus, black cabs
    bus = Part('bus', (-4, 4, 4)); mb = bus.mb; bm = TX('bus', 1.0, 6.0, glow='bus_glow', glow_k=1.6, smix=0.15); bred = C('#c8201e', 1.0, 6.0, smix=0.15)
    mb.box((-16, 1.2, 0.8), (8, 6.2, 10.4), bred, mats={'front': bm, 'back': bm, 'top': C('#e03a30', 1.2, 7.0, smix=0.15)}, skip='')
    mb.box((-16.2, 1.0, 10.4), (8.2, 6.4, 10.8), C('#9a1614', 1.0, 4.0, smix=0.15)); mb.box((-16, 1.2, 0.2), (8, 6.2, 1.2), C('#3a0a10', 1.0, 3.0))
    mb.box((-16.1, 2.0, 4.6), (-15.9, 5.4, 5.2), C('#fff2c0', 1.8))                                                       # route board
    mb.box((7.0, 1.0, 0.8), (8.6, 1.5, 10.4), C('#2a0a14')); mb.box((7.0, 5.9, 0.8), (8.6, 6.4, 10.4), C('#2a0a14'))     # open rear platform posts
    for wx in (-12, -9.5, 3.0):
        for wy in (1.6, 5.8): mb.frustum((wx, wy - .35, 1.1), (wx, wy + .35, 1.1), 1.15, 1.15, C('#14143a'), seg=12)
    bus.done((-4, 4, 4))
    point_light('bus_warm', (-4, -3, 6), (1.0, 0.7, 0.4), 5200, 1.0)
    bl = Part('bus_lamps', ink=False, shadow=False); halo_card(bl.mb, (-16.4, 2.4, 2.2), 2.4, E('hl', 'halo_white', k=1.8, additive=True)); halo_card(bl.mb, (-16.4, 5.0, 2.2), 2.4, E('hl', 'halo_white', k=1.8, additive=True)); bl.done()
    cabs = [((14, 0.6), 1), ((26, 11.2), -1), ((-26, 11.4), -1), ((38, 0.8), 1)]
    cb = Part('cabs', (20, 6, 3)); mb = cb.mb; cm = TX('cab', 1.0, 2.0, glow='cab_glow', glow_k=1.6, smix=0.3); cbk = C('#1d2250', 1.0, 1.6)
    for (cx, cy), d in cabs:
        mb.box((cx - 3.6, cy, 0.7), (cx + 3.6, cy + 3.6, 3.2), cbk, mats={'front': cm, 'back': cm}); mb.box((cx - 2.2 * d - 1.4 + (0 if d > 0 else 0.0), cy + 0.25, 3.2), (cx - 2.2 * d + 1.4 + (0), cy + 3.35, 5.0), cbk, mats={'front': cm, 'back': cm})
        for wx in (cx - 2.2, cx + 2.2):
            for wy in (cy + 0.1, cy + 3.5): mb.frustum((wx, wy - .25, 0.7), (wx, wy + .25, 0.7), 0.7, 0.7, C('#0e0e28'), seg=10)
    cb.done((20, 6, 3))
    ch = Part('cab_lamps', ink=False, shadow=False)
    for (cx, cy), d in cabs: halo_card(ch.mb, (cx - 3.9 * d, cy + 0.8, 1.9), 1.5, E('hl', 'halo_white', k=1.7, additive=True)); halo_card(ch.mb, (cx - 3.9 * d, cy + 2.8, 1.9), 1.5, E('hl', 'halo_white', k=1.7, additive=True))
    ch.done()
    # ---- street furniture: lamp posts + halos, kiosk, flower stall, bollards, railings
    lp = Part('lamps', (0, 6, 7)); mb = lp.mb; lc = C('#26204e'); bulb = E('bulb', color='#ffd98a', k=2.2)
    lamps = [(-52, -3.3), (-20, -3.3), (14, -3.3), (44, -3.3), (-52, 24.5 - 9.6), (-12, 24.5 - 9.6), (30, 24.5 - 9.6), (56, 24.5 - 9.6)]
    lamps = [(-18, -3.3), (12, -3.3), (40, -3.3), (66, -3.3), (-24, 15.2), (-6, 15.2), (32, 15.2), (56, 15.2)]
    for (lx, ly) in lamps:
        rod(mb, (lx, ly, 0), (lx, ly, 12.5), 0.34, lc, r1=0.22, seg=8); mb.box((lx - .8, ly - .8, 0), (lx + .8, ly + .8, 1.5), lc); mb.box((lx - 1.0, ly - 1.0, 12.5), (lx + 1.0, ly + 1.0, 13.0), lc)
        mb.frustum((lx, ly, 13.0), (lx, ly, 13.8), 0.9, 0.6, lc, seg=8); mb.sphere((lx, ly, 15.0), 1.4, bulb, seg=12, rings=8)
    lp.done((0, 6, 7))
    lh_ = Part('lamp_halos', ink=False, shadow=False)
    for (lx, ly) in lamps:
        halo_card(lh_.mb, (lx, ly, 13.9), 4.4, E('hh', 'halo_warm', k=1.9, additive=True)); plane(lh_.mb, (lx - 5, ly - 5, 0.07), (10, 0, 0), (0, 10, 0), E('hp', 'halo_warm', k=0.9, additive=True), (0, 0, 1, 1))
    lh_.done()
    for i, (lx, ly) in enumerate(lamps[:4]): point_light('lamp%d' % i, (lx, ly, 13.2), (1.0, 0.68, 0.34), 2200, 0.6)
    ks = Part('kiosk', (-16, 20, 3)); mb = ks.mb
    mb.box((-19, 17.5, 0), (-13, 21.5, 4.6), C('#1f8a52'), mats={'front': C('#1f8a52')}); mb.box((-19.6, 17.0, 4.6), (-12.4, 22, 5.6), C('#e3262b')); mb.box((-18.4, 17.1, 1.6), (-13.6, 17.5, 3.4), C('#ffc65a', 1.5))
    ks.done((-16, 20, 3))
    ksg = Part('kiosk_sign', ink=False); plane(ksg.mb, (-21.0, 16.8, 5.6), (9.0, 0, 0), (0, 0, 2.7), E('news', 'sign_news', k=1.7), (0, 0, 1, 1)); ksg.done()
    fs = Part('flowers', (20, 21, 2)); mb = fs.mb
    mb.box((17, 19.5, 0), (23, 22, 1.8), C('#6a3a1a')); mb.box((16.6, 19.2, 1.8), (23.4, 22.4, 2.0), C('#f0e4c8'))
    for i in range(6): lumpy(mb, (17.6 + i * 1.0, 20.7, 2.5), 0.55, C(['#e3262b', '#ffc81e', '#d1409a', '#ffffff', '#ff7a1e', '#e3262b'][i]), i, seg=8, rings=5)
    mb.box((15.8, 18.8, 5.0), (24.2, 22.8, 5.3), C('#12724a')); rod(mb, (16, 19, 2), (16, 19, 5), 0.2, lc); rod(mb, (24, 19, 2), (24, 19, 5), 0.2, lc)
    fs.done((20, 21, 2))
    fgn = Part('flower_sign', ink=False); plane(fgn.mb, (15.4, 18.6, 5.5), (9.0, 0, 0), (0, 0, 2.5), E('flw', 'sign_flowers', k=1.4), (0, 0, 1, 1)); fgn.done()
    bol = Part('bollards', (0, -1, 1)); mb = bol.mb
    for bx in range(-30, 60, 7): rod(mb, (bx, -2.8, 0), (bx, -2.8, 1.4), 0.4, C('#e8e0c8'), seg=8)
    bol.done((0, -1, 1))
    # tall iron railings on the near embankment edge dark foreground + traffic signal
    rl = Part('railings', (6, -9, 2)); mb = rl.mb; rc = C('#1e1a46')
    for rx in np.arange(2, 70, 1.6): rod(mb, (rx, -8.2, 0), (rx, -8.2, 3.0), 0.12, rc, seg=4)
    mb.box((2, -8.4, 2.8), (70, -8.0, 3.2), rc); mb.box((2, -8.4, 0.6), (70, -8.0, 0.9), rc)
    rl.done((6, -9, 2))
    pb = Part('phoneboxes', (10, -5, 3)); mb = pb.mb; red = C('#e3262b', 1.0, 3.2, smix=0.22)
    for bx in (-8, 26):
        mb.box((bx - 1.4, -6.8, 0), (bx + 1.4, -4.2, 6.4), red); mb.box((bx - 1.6, -7.0, 6.4), (bx + 1.6, -4.0, 6.9), red)
        mb.box((bx - 1.0, -7.05, 1.2), (bx + 1.0, -6.75, 5.4), C('#ffd88a', 1.6)); 
    for bx in (4, 48): rod(mb, (bx, -5.2, 0), (bx, -5.2, 4.2), 1.1, red, seg=12); mb.frustum((bx, -5.2, 4.2), (bx, -5.2, 4.8), 1.2, 0.8, red, seg=12)
    pb.done((10, -5, 3))
    pg2 = Part('phone_glow', ink=False, shadow=False)
    for bx in (-8, 26): halo_card(pg2.mb, (bx, -7.4, 3.4), 3.6, E('hph', 'halo_warm', k=1.2, additive=True))
    pg2.done()
    # ---- crowds (painted placeholder cards with hats, rim light)
    cr = Part('crowd', ink=False); mb = cr.mb; cam = STATE['cam']
    PEOPLE = []
    def person(x, y, k, rimset='w', h=4.1, z=0.0):
        card = CARD('crowd_%s%d' % (rimset, k % 10)); w = h * 200 / 440; facing_card(mb, (x, y, z), w, h, card, cam, tilt=5.0); PEOPLE.append((x, y, w))
    n = 0
    for (x0, x1, y0, y1, num, rimset) in ((-30, -2, 15.5, 22.5, 18, 'w'), (-6, 40, 15.6, 22.5, 16, 'w'), (0, 66, 14.5, 23, 12, 'w'), (-30, 66, -7, -3, 14, 'c'), (-8, 22, 1.0, 12.5, 6, 'w'), (-20, 60, -8, -4.5, 12, 't')):
        for i in range(num): person(rs.uniform(x0, x1), rs.uniform(y0, y1), n, rimset, h=rs.uniform(5.6, 6.6)); n += 1
    for i in range(9): person(-39 + i * 1.6, 16.5 + (i % 3) * 1.6, n, 't', 6.0); n += 1        # queue at the entrance
    for (x0, x1, y0, y1, num, rimset) in ((24, 70, -7.5, -3.5, 16, 't'), (20, 66, 0.5, 12, 8, 'c'), (-70, -40, 15.5, 22.5, 10, 'w')):
        for i in range(num): person(rs.uniform(x0, x1), rs.uniform(y0, y1), n, rimset, h=rs.uniform(5.6, 6.6)); n += 1
    cr.done()
    bsh = Part('contact_shadows', ink=False, shadow=False)
    for (bx, by, bw_) in PEOPLE: plane(bsh.mb, (bx - bw_ * 0.7, by - 0.7, 0.09), (bw_ * 1.4, 0, 0), (0, 1.4, 0), E('blob', 'blob', alpha=True), (0, 0, 1, 1))
    bsh.done()
    bl2 = Part('blobs', ink=False, shadow=False); mb = bl2.mb
    # ---- foreground dark prop: big lamp post at the bottom right, in the nearest 15 %
    fg = Part('fg_post', (10, -26, 8)); mb = fg.mb; fc = C('#1c1850', 0.8)
    rod(mb, (12, -22, 0), (12, -22, 15), 0.55, fc, r1=0.3, seg=10); mb.box((11, -23, 0), (13, -21, 2.2), fc); mb.box((10.6, -22.6, 15), (13.4, -21.4, 16))  if False else None
    mb.frustum((12, -22, 15), (12, -22, 16.2), 1.8, 1.0, fc, seg=10); mb.sphere((12, -22, 18.0), 1.7, bulb, seg=14, rings=9)
    fg.done((12, -22, 10))
    fh = Part('fg_halo', ink=False, shadow=False); halo_card(fh.mb, (12, -22, 17.6), 5.0, E('hh', 'halo_warm', k=2.0, additive=True)); fh.done()



CAM_LONDON = dict(loc=(-13, -46, 70), look_at=(-3, 44, 0), lens=22, shift_y=0.14)
def build_london(scene, P):
    build_london_world(scene, P)
LOCATIONS['london'] = dict(build=build_london, light='DUSK_CITY', sky=True, cam=CAM_LONDON)


# ============================================================================= shots
SHOTS['s02'] = dict(location='london', light='DUSK', f0=107, f1=192, shift_y=0.12,
    cam=[(0, (-30.5, -5.6, 10.4), (-18.0, 24.0, 11.0), 30), (9, (-30.5, -2.9, 10.6), (-18.0, 24.0, 12.5), 28), (30, (-27.0, -24.0, 46.0), (-6.0, 42.0, 0.0), 24), (46, (-13.0, -46.0, 70.0), (-3.0, 44.0, 0.0), 22),
         (60, (-4.0, -32.0, 62.0), (6.0, 22.0, 0.0), 24), (74, (7.5, 0.0, 26.0), (8.0, 19.0, 0.0), 27), (84, (8.0, 18.7, 6.0), (8.0, 19.0, 0.0), 30)],
    marks=dict(), state=dict())
SHOTS['s15'] = dict(location='london', light='NIGHT', f0=1752, f1=1890, shift_y=0.12,
    cam=[(0, (-13.0, -46.0, 70.0), (-3.0, 44.0, 0.0), 22), (40, (-6.0, -30.0, 52.0), (0.0, 24.0, 11.0), 24), (80, (0.0, 1.0, 19.0), (0.0, 24.0, 11.0), 26), (100, (0.0, 13.5, 11.8), (0.0, 34.0, 10.0), 28), (112, (0.0, 22.0, 10.9), (0.0, 38.0, 9.7), 30), (137, (0.0, 34.0, 10.0), (0.0, 42.6, 9.2), 34)],
    marks=dict(official=(0.0, 43.5, 9.23, 0)), state=dict(map_towers=1.0, crate=1.0), actors=lambda g: actors_s15(g))

def actors_s15(g):
    import beck_hq as H
    sh = B.ALL_SHOTS['s15']; cam = B.cam_eval(sh['cam'], g - sh['f0'])[0]; k = g - sh['f0']
    H.off_card('off_buried_eat', cam, 1.0)
