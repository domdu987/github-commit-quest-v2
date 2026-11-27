#!/usr/bin/env python3
"""dock.py : channel port (film 25 shot 19): concrete quay, a cargo ship alongside with the shipping crate on its deck, a dock crane with chains + hook, bollards, gulls, the French coast across the water.  Preset: dock_crate (shot 19)."""
import math, time
import numpy as np
from mathutils import Vector
import front as F
import lib25 as L
import tank25 as TK
import factory as FA
from front import S, MB, rnd, mkobj, obox, beam, rod, ell, rot_axes, J

def gull(mb, c, yaw, s=1.0, ph=0.0):
    M = S['M']; c = Vector(c); X, Y, Z = rot_axes(yaw); wm = M['p_white']
    for sg in (-1, 1):
        a = c; b = c + Y * sg * 1.2 * s + X * -0.2 * s + Z * (0.25 + 0.2 * math.sin(ph)) * s; d = b + Y * sg * 1.1 * s + X * -0.4 * s + Z * (-0.3 * s)
        for (p, q, w) in ((a, b, 0.45), (b, d, 0.3)): mb.pid += 1; mb.oface([p + X * 0.25 * s, q + X * 0.15 * s, q - X * (w * s), p - X * 0.25 * s], wm, [(0, 0)] * 4, Z); mb.pid += 1; mb.oface([p - X * 0.25 * s, q - X * (w * s), q + X * 0.15 * s, p + X * 0.25 * s], wm, [(0, 0)] * 4, -Z)
    mb.frustum(c - X * 0.5 * s, c + X * 0.4 * s, 0.14 * s, 0.1 * s, wm, seg=8); mb.sphere(c + X * 0.5 * s, 0.11 * s, wm, 8, 6)
    mb.frustum(c + X * 0.58 * s, c + X * 0.72 * s, 0.04 * s, 0.01 * s, M['p_yellow'], seg=4)

def build(preset, samples=None, quality=None):
    P = PRESETS[preset]; t0 = time.time(); F.begin('dock', preset, P); S.update(flat=True, trenches=[], craters=[], corridors=[], mud_zones=[]); M = S['M']; r = rnd(8)
    def sea(b):
        c = b.coord(); n = b.noise(0.5, 4.0, 0.55, c, None); n2 = b.noise(2.0, 3.0, 0.5, c, None); col = b.mix(b.rng(n, 0.3, 0.7), (0.05, 0.28, 0.42), (0.10, 0.45, 0.58)); b.princ(col, 0.12, 0.0, b.bump(b.math('ADD', n, n2), 0.5, 0.06))
    M['sea'] = F.fmat('sea', sea)
    mb = MB(); mb.pid += 1; mb.oface([(-900, -900, -1.3), (900, -900, -1.3), (900, 40, -1.3), (-900, 40, -1.3)], M['sea'], [(0, 0)] * 4, (0, 0, 1)); mkobj(mb, 'sea')
    mb = MB(); mb.pid += 1; mb.oface([(-120, 0, 0.0), (120, 0, 0.0), (120, 60, 0.0), (-120, 60, 0.0)], M['concrete'], [(0, 0)] * 4, (0, 0, 1)); obox(mb, (0, 0.2, -0.65), (1, 0, 0), (0, 1, 0), (0, 0, 1), 120, 0.6, 0.65, M['cobble'])
    mkobj(mb, 'quay'); mb = MB(); mb.pid += 1; mb.oface([(-600, 60, -0.05), (600, 60, -0.05), (600, 600, -0.05), (-600, 600, -0.05)], M['lawn'], [(0, 0)] * 4, (0, 0, 1)); mkobj(mb, 'land')
    # ship alongside (bow to +x): hull as a loft of boxes + wedge, deck, superstructure, funnel, masts
    mh = MB(); mw = MB(); zd = 3.2; L_ = 70.0; B = 16.0; y0 = -10.0
    obox(mh, (0, y0, 0.9), (1, 0, 0), (0, 1, 0), (0, 0, 1), L_ / 2, B / 2, 2.1, M['p_grey']); obox(mh, (0, y0, 0.2 - 1.3 + 2.4), (1, 0, 0), (0, 1, 0), (0, 0, 1), L_ / 2 + 0.1, B / 2 + 0.1, 0.25, M['p_red'])
    for sg in (-1, 1): mh.pid += 1; mh.oface([(L_ / 2, y0 + sg * B / 2, -1.2), (L_ / 2 + 8, y0, 1.6), (L_ / 2 + 8, y0, zd - 0.1), (L_ / 2, y0 + sg * B / 2, zd - 0.1)], M['p_black'], [(0, 0)] * 4, (1, sg * 0.5, 0)); mh.pid += 1; mh.oface([(L_ / 2, y0 + sg * B / 2, zd - 0.1), (L_ / 2 + 8, y0, zd - 0.1), (L_ / 2, y0, zd - 0.1)], M['floorw'], [(0, 0)] * 3, (0, 0, 1))
    obox(mw, (0, y0, zd - 0.05), (1, 0, 0), (0, 1, 0), (0, 0, 1), L_ / 2, B / 2 - 0.2, 0.1, M['floorw'])
    for k in range(9): obox(mw, (-L_ / 2 + 4 + k * 8, y0 + B / 2 - 0.1, zd + 0.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.08, 0.08, 0.5, M['steel']); obox(mw, (-L_ / 2 + 4 + k * 8, y0 - B / 2 + 0.1, zd + 0.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.08, 0.08, 0.5, M['steel'])
    obox(mw, (-26, y0, zd + 4.0), (1, 0, 0), (0, 1, 0), (0, 0, 1), 7.0, 5.5, 4.0, M['p_cream']); obox(mw, (-26, y0, zd + 8.3), (1, 0, 0), (0, 1, 0), (0, 0, 1), 7.4, 5.9, 0.3, M['p_grey'])
    for k in range(5): obox(mw, (-26 + k * 2.6 - 5, y0 - 5.55, zd + 4.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.7, 0.1, 0.8, M['p_black'])
    mw.frustum((-24, y0, zd + 8.5), (-24, y0, zd + 17), 2.0, 1.5, M['p_black'], seg=16); mw.frustum((-24, y0, zd + 14), (-24, y0, zd + 15.2), 2.02, 1.52, M['p_red'], seg=16)
    for x in (-8, 18): rod(mw, (x, y0, zd), (x, y0, zd + 20), 0.2, M['beam'], 6); rod(mw, (x - 3, y0, zd + 12), (x + 3, y0, zd + 12), 0.1, M['beam'], 5)
    for k in range(3): L.crate_box(mw, (4 + k * 5, y0 + (-2 if k % 2 else 2), zd), 4.0, 3.4, 3.2 + k * 0.4, r.uniform(-0.2, 0.2))
    mkobj(mh, 'ship_hull'); mkobj(mw, 'ship_deck')
    C = FA.shipping_crate(-6, y0, 0.0, 22.0, 9.0, 8.0, 0.0, True); C['root'].location = (-6, y0, zd - 0.2 + P.get('crate_lift', 0.0))
    # dock crane: A-frame tower on the quay, jib out over the ship, chains + hook to the crate
    mc = MB(); cx = 8.0; cy = 16.0
    for (dx, dy) in ((-3, -3), (3, -3), (-3, 3), (3, 3)): beam(mc, (cx + dx, cy + dy, 0), (cx + dx * 0.5, cy + dy * 0.5, 26), 0.6, 0.6, M['frame'])
    for z in (6, 12, 18, 24): beam(mc, (cx - 3 + z * 0.1, cy - 3 + z * 0.1, z), (cx + 3 - z * 0.1, cy + 3 - z * 0.1, z + 3), 0.3, 0.3, M['frame'])
    beam(mc, (cx, cy, 27), (cx - 6.0, y0, 22.5), 0.8, 1.2, M['frame']); beam(mc, (cx, cy, 27), (cx + 14, cy + 6, 27), 0.6, 0.8, M['frame']); obox(mc, (cx, cy, 2.0), (1, 0, 0), (0, 1, 0), (0, 0, 1), 4.0, 4.0, 2.0, M['p_red'])
    hb = Vector((-6, y0, zd + 8.4 + 8.0 + P.get('crate_lift', 0.0) * 0.5)); top = Vector((cx - 6.0, y0, 22.5)); L.chain(mc, top, hb + Vector((0, 0, 0.5)), 0.3, 0.05, M['steel']); obox(mc, hb, (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.6, 0.5, 0.5, M['p_yellow'])
    for sx in (-1, 1):
        for sy in (-1, 1): L.chain(mc, hb, (-6 + sx * 10.0, y0 + sy * 3.8, zd + 8.2 + P.get('crate_lift', 0.0)), 0.3, 0.05, M['steel'])
    for k in range(5): L.bollard(mc, (-40 + k * 20, 3.0)) if hasattr(L, 'bollard') else obox(mc, (-40 + k * 20, 3.0, 0.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 0.4, 0.4, 0.5, M['p_black'])
    mkobj(mc, 'dock_crane')
    mg = MB()
    for k in range(P.get('gulls', 9)): gull(mg, (r.uniform(-25, 25), r.uniform(-30, 5), r.uniform(10, 26)), r.uniform(0, 6.28), r.uniform(0.8, 1.6), k)
    mkobj(mg, 'gulls', shadow=False)
    mf = MB()                                                                           # French coast: low cliffs and green hills across the water
    for k in range(40): J.lump(mf, (-260 + k * 14 + r.uniform(-4, 4), -330 + r.uniform(-20, 20), r.uniform(4, 14)), r.uniform(18, 34), M['fol_b'] if k % 3 else M['dirt'], r.randint(0, 9999), 10, 6, 0.2, 0.5)
    obox(mf, (0, -310, 3), (1, 0, 0), (0, 1, 0), (0, 0, 1), 340, 6, 5, M['gravel']); mkobj(mf, 'coast', smooth=True)
    mb = MB(); L.dress(lambda x, y: 0.0, L.scatter_rect(-100, 62, 100, 200, 700, 3), None, L.scatter_rect(-100, 62, 100, 200, 100, 4), None, 7, 'land', 6, (0.3, 0.7)); mkobj(mb, 'noop')
    cam = P['cam']; S['cam_loc'] = cam['loc']; S['cards'] = []
    for (k, xy, ht) in P.get('cards', []): L.cards([(k, xy, ht)], lambda x, y: 0.0, cam['loc'])
    F.finish(cam, P, samples, quality, sun=P.get('sun')); S['build_s'] = time.time() - t0; return F.anchors()

PRESETS = dict(
    dock_crate=dict(cam=dict(loc=(34.0, 34.0, 13.0), look_at=(-8.0, -14.0, 5.0), lens=22), crate_lift=0.0, cards=[('a', (-18, 12), 3.2)], sun=(-150.0, 30.0), note='shot 19: crate on the cargo ship deck under the dock crane, gulls, the French coast'),
)
