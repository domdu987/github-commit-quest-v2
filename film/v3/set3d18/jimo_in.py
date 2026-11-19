"""jimo_in.py : inside Jimo: the inner face of the wall, the ox yard with pens and torch stands, the ring lane, the market (stalls, the clerk's counter), houses with tiled roofs,
dig props (picks, baskets, earth heaps), reed-bundle jars, hanging lamps, the far town. Marks for the puppets are in jimo_shots.py."""
import math
import numpy as np
from mathutils import Vector as V, Matrix

def bind(J):
    g = globals()
    for k, v in vars(J).items():
        if not k.startswith('__'): g.setdefault(k, v)

XX, YY, ZZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)

def house(Bk, M, cx, cy, w, d, h, rise, yaw, seed, cd=70.0, gate=True, lit=0.8):
    """Tiled commoner house, front facing -y (toward the lane / wall): plaster or rammed body, dark timber posts, a door, lit lattice windows, hip roof with eave tiles;
    optionally a courtyard wall with a tiled gate in front (a gate opening townsfolk lead oxen through)."""
    r = _rnd(seed); F = Frame((cx, cy, 0), yaw); bd = Bk('housebody', hull=T.hull(cd)); rf = Bk('houseroof', hull=T.hull(cd)); gl = Bk('houseglow', shadow=False)
    mat = M['plaster'] if r.random() < 0.55 else M['rammed_d']
    obox(bd, F.p(0, 0, h / 2), F.X, F.Y, F.Z, w / 2, d / 2, h / 2, mat, uvk=0.2); obox(bd, F.p(0, 0, 0.3), F.X, F.Y, F.Z, w / 2 + 0.15, d / 2 + 0.15, 0.3, M['stone_d'], uvk=0.3)
    nb = max(2, int(w // 3.4))
    for k in range(nb + 1):
        x = -w / 2 + w * k / nb; rod(bd, F.p(x, -d / 2 - 0.08, 0.3), F.p(x, -d / 2 - 0.08, h), 0.24, M['lacq'], seg=6)
    for z in (h - 0.15,): obox(bd, F.p(0, -d / 2 - 0.1, z), F.X, F.Y, F.Z, w / 2 + 0.2, 0.2, 0.22, M['lacq'])
    dk = r.randint(0, nb - 1)
    for k in range(nb):
        x0 = -w / 2 + w * k / nb; x1 = x0 + w / nb
        if k == dk: bd.oface([F.p(x0 + 0.5, -d / 2 - 0.06, 0.3), F.p(x1 - 0.5, -d / 2 - 0.06, 0.3), F.p(x1 - 0.5, -d / 2 - 0.06, h * 0.72), F.p(x0 + 0.5, -d / 2 - 0.06, h * 0.72)], M['black'], [(0, 0)] * 4, F.Y * -1)
        elif r.random() < lit:
            flat(gl, F.p(x0 + 0.55, -d / 2 - 0.1, h * 0.38), F.X * (x1 - x0 - 1.1), F.Z * (h * 0.4), M['win'])
            for q in range(1, 4): obox(bd, F.p(x0 + 0.55 + q * (x1 - x0 - 1.1) / 4, -d / 2 - 0.14, h * 0.58), F.X, F.Y, F.Z, 0.04, 0.05, h * 0.2, M['wood_d'])
    hip_roof(rf, (F.p(0, 0, h)), yaw, w / 2 + 1.5, d / 2 + 1.5, max(0.2, w / 2 - d / 2 + 0.4), 0.0, rise, M, lift=0.3, nx=14, ny=8, mat=M['tiles'])
    if gate:                                                                                                      # courtyard wall with a gate
        gy = -d / 2 - 5.5; ww = w + 3.0
        for sg_ in (-1, 1):
            obox(bd, F.p(sg_ * (ww / 2 + 1.3) / 1.0 * 0.5 + sg_ * 1.4, gy, 1.5), F.X, F.Y, F.Z, (ww / 2 - 2.4) / 2 + 0.01, 0.3, 1.5, M['rammed_d'], uvk=0.3) if False else None
        obox(bd, F.p(-(ww / 2 + 2.6) / 2, gy, 1.5), F.X, F.Y, F.Z, (ww / 2 - 2.6) / 2, 0.3, 1.5, M['rammed_d'], uvk=0.3); obox(bd, F.p((ww / 2 + 2.6) / 2, gy, 1.5), F.X, F.Y, F.Z, (ww / 2 - 2.6) / 2, 0.3, 1.5, M['rammed_d'], uvk=0.3)
        for sg_ in (-1, 1):
            rod(bd, F.p(sg_ * 2.3, gy - 0.2, 0), F.p(sg_ * 2.3, gy - 0.2, 4.2), 0.26, M['lacq'], seg=7)
        obox(bd, F.p(0, gy - 0.2, 4.35), F.X, F.Y, F.Z, 2.7, 0.35, 0.2, M['lacq'])
        bd.oface([F.p(-2.0, gy - 0.1, 0), F.p(2.0, gy - 0.1, 0), F.p(2.0, gy - 0.1, 4.0), F.p(-2.0, gy - 0.1, 4.0)], M['black'], [(0, 0)] * 4, F.Y * -1)
        hip_roof(rf, F.p(0, gy, 4.6), yaw, 3.3, 1.5, 1.4, 0.0, 1.3, M, lift=0.2, nx=8, ny=4, mat=M['tiles'], wadang=False)
        STATE.setdefault('gates', []).append(tuple(F.p(0, gy - 1.5, 0)))
    return F

def stall(Bk, M, cx, cy, yaw, awn, w=6.0, d=3.6, seed=0, cd=45.0, clerk=False, cloth=False):
    """Market stall facing -y: four posts, a canvas awning on a slope, a plank counter with baskets / jars / tally slips, a bronze lamp."""
    r = _rnd(seed); F = Frame((cx, cy, 0), yaw); sb = Bk('stalls', hull=T.hull(cd)); X, Y, Z = F.X, F.Y, F.Z
    for sx in (-1, 1):
        for sy in (-1, 1): rod(sb, F.p(sx * w / 2, sy * d / 2, 0), F.p(sx * w / 2, sy * d / 2, 4.2 if sy > 0 else 3.4), 0.14, M['wood_d'], seg=5)
    sb.oface([F.p(-w / 2 - 0.3, -d / 2 - 0.5, 3.35), F.p(w / 2 + 0.3, -d / 2 - 0.5, 3.35), F.p(w / 2 + 0.3, d / 2, 4.3), F.p(-w / 2 - 0.3, d / 2, 4.3)], awn, [(0, 0), (w / 4, 0), (w / 4, 1), (0, 1)], (0, -0.4, 1))
    sb.oface([F.p(-w / 2 - 0.3, -d / 2 - 0.5, 3.35), F.p(w / 2 + 0.3, -d / 2 - 0.5, 3.35), F.p(w / 2 + 0.3, d / 2, 4.3), F.p(-w / 2 - 0.3, d / 2, 4.3)], M['canvas'], [(0, 0), (w / 4, 0), (w / 4, 1), (0, 1)], (0, 0.4, -1))
    for k in range(int(w / 0.8) + 1): sb.oface([F.p(-w / 2 - 0.3 + k * 0.8, -d / 2 - 0.5, 3.35), F.p(-w / 2 - 0.3 + k * 0.8 + 0.4, -d / 2 - 0.5, 3.35), F.p(-w / 2 - 0.3 + k * 0.8 + 0.2, -d / 2 - 0.5, 2.8)], M['red_d'] if k % 2 else awn, [(0, 0)] * 3, F.Y * -1)
    obox(sb, F.p(0, -d / 2 + 0.2, 1.5), X, Y, Z, w / 2, 0.5, 0.1, M['planks'], uvk=0.4); obox(sb, F.p(0, -d / 2 + 0.2, 0.75), X, Y, Z, w / 2 - 0.1, 0.4, 0.75, M['wood_d'], uvk=0.4)
    for k in range(int(w / 1.1)):
        x = -w / 2 + 0.7 + k * 1.1 + r.uniform(-0.1, 0.1); t = r.random()
        if t < 0.35: sb.frustum(F.p(x, -d / 2 + 0.2, 1.6), F.p(x, -d / 2 + 0.2, 2.1), 0.42, 0.34, M['straw_d'], seg=8); lumpy(sb, F.p(x, -d / 2 + 0.2, 2.1), 0.36, M['hay'] if k % 2 else M['jade'], seed * 9 + k, seg=6, rings=4, rough=0.2, squash=0.6)
        elif t < 0.65: ellipsoid(sb, F.p(x, -d / 2 + 0.2, 2.0), 0.4, 0.4, 0.45, M['clay'] if k % 2 else M['clay_d'], seg=9, rings=6); cyl(sb, F.p(x, -d / 2 + 0.2, 2.4), 0.2, 0.16, M['clay_d'], seg=8)
        else: obox(sb, F.p(x, -d / 2 + 0.2, 1.8), X, Y, Z, 0.4, 0.3, 0.12, [M['indigo'], M['red'], M['teal'], M['cream']][k % 4])
    if cloth:
        for k in range(5): sb.oface([F.p(-w / 2 + 0.6 + k * 1.1, d / 2 - 0.1, 3.3), F.p(-w / 2 + 1.5 + k * 1.1, d / 2 - 0.1, 3.3), F.p(-w / 2 + 1.5 + k * 1.1, d / 2 - 0.1, 1.5), F.p(-w / 2 + 0.6 + k * 1.1, d / 2 - 0.1, 1.5)], [M['red'], M['teal'], M['cream'], M['indigo'], M['gold']][k % 5], [(0, 0)] * 4, F.Y * -1)
    if clerk:                                                                                                    # the clerk's counter: bundles of bamboo tally slips, a ruled counting board, a brush stand
        for k in range(6):
            p0 = F.p(-w / 2 + 0.6 + k * 0.5, -d / 2 + 0.1, 1.62); rod(sb, p0, p0 + F.X * 0.0 + F.Y * 0.0 + V((0, 0, 0.0)), 0.01, M['straw'], seg=3)
            for q in range(7): rod(sb, F.p(-w / 2 + 0.5 + k * 0.5 + q * 0.05, -d / 2 + 0.05, 1.6), F.p(-w / 2 + 0.5 + k * 0.5 + q * 0.05, -d / 2 + 0.05, 2.5), 0.025, M['straw'], seg=3)
            cyl(sb, F.p(-w / 2 + 0.65 + k * 0.5, -d / 2 + 0.05, 1.95), 0.2, 0.08, M['red_d'], seg=8, cap=False)
        obox(sb, F.p(1.6, -d / 2 + 0.2, 1.64), X, Y, Z, 1.0, 0.45, 0.04, M['wood_l'])
        for k in range(1, 5): obox(sb, F.p(1.6, -d / 2 + 0.2, 1.7), X, Y, Z, 0.01, 0.45, 0.01, M['black']); obox(sb, F.p(0.8 + k * 0.4, -d / 2 + 0.2, 1.7), X, Y, Z, 0.012, 0.45, 0.012, M['black'])
    oil_lamp(Bk, M, tuple(F.p(w / 2 - 0.5, -d / 2 + 0.3, 1.6)), s=0.55, light=0.0, name='stl%d' % seed, halo_r=1.4, h=2.6)
    return F

def pen(Bk, M, cx, cy, w, d, yaw=0.0, gap=3.2, cd=60.0):
    F = Frame((cx, cy, 0), yaw); pb = Bk('pens', hull=T.hull(cd))
    for side, (a, b) in enumerate((((-w / 2, -d / 2), (w / 2, -d / 2)), ((w / 2, -d / 2), (w / 2, d / 2)), ((w / 2, d / 2), (-w / 2, d / 2)), ((-w / 2, d / 2), (-w / 2, -d / 2)))):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = int(L / 2.2)
        for k in range(n + 1):
            t = k / max(1, n); x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
            if side == 0 and abs(x) < gap / 2: continue
            rod(pb, F.p(x, y, 0), F.p(x, y, 2.5), 0.15, M['wood_d'], seg=5)
        for z in (1.0, 1.9):
            if side == 0: continue
            for q in range(n): 
                t0, t1 = q / n, (q + 1) / n; rod(pb, F.p(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0, z), F.p(a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1, z), 0.07, M['wood'], seg=4)
        if side == 0:
            for sx, (u0, u1) in ((1, (gap / 2, w / 2)), (-1, (-w / 2, -gap / 2))):
                for z in (1.0, 1.9): rod(pb, F.p(u0, -d / 2, z), F.p(u1, -d / 2, z), 0.07, M['wood'], seg=4)
    return F

def trough_hay(Bk, M, p, yaw=0.0, cd=40.0):
    F = Frame(p, yaw); tb = Bk('props', hull=T.hull(cd)); obox(tb, F.p(0, 0, 0.45), F.X, F.Y, F.Z, 1.6, 0.5, 0.12, M['wood_d']); obox(tb, F.p(0, 0.45, 0.8), F.X, F.Y, F.Z, 1.6, 0.06, 0.4, M['wood']); obox(tb, F.p(0, -0.45, 0.8), F.X, F.Y, F.Z, 1.6, 0.06, 0.4, M['wood'])
    lumpy(tb, F.p(0, 0, 1.0), 1.2, M['hay'], int(p[0] * 3), seg=8, rings=4, rough=0.25, squash=0.4)

def reed_jar(Bk, M, p, s=1.0, cd=30.0, reeds=7):
    """Big clay jar with straw-bound neck and a bundle of reeds standing in the fat (reed-bundle jars)."""
    p = V(p); b = Bk('jars', hull=T.hull(cd)); r = _rnd(int(p.x * 7 + p.y))
    ellipsoid(b, p + V((0, 0, 0.95 * s)), 0.85 * s, 0.85 * s, 1.0 * s, M['clay'] if int(p.x) % 2 else M['clay_d'], seg=12, rings=8, rough=0.05, seed=int(p.x)); cyl(b, p + V((0, 0, 1.8 * s)), 0.5 * s, 0.4 * s, M['clay_d'], seg=10, r1=0.6 * s)
    cyl(b, p + V((0, 0, 1.55 * s)), 0.62 * s, 0.22 * s, M['straw'], seg=10, cap=False)
    for k in range(reeds):
        a = 2 * math.pi * k / reeds; rod(b, p + V((0.18 * s * math.cos(a), 0.18 * s * math.sin(a), 1.9 * s)), p + V((0.5 * s * math.cos(a) + r.uniform(-0.1, 0.1), 0.5 * s * math.sin(a), 4.2 * s + r.uniform(0, 0.5))), 0.07 * s, M['hay'] if k % 2 else M['straw'], seg=4)
    cyl(b, p + V((0, 0, 3.0 * s)), 0.5 * s, 0.12 * s, M['red_d'], seg=8, cap=False)

def reed_bundles(Bk, M, p, n=4, cd=30.0):
    b = Bk('reeds', hull=T.hull(cd)); p = V(p)
    for k in range(n):
        q = p + V((k * 0.7, (k % 2) * 0.4, 0)); rod(b, q + V((0, 0, 0.1)), q + V((-0.4, 0.3, 2.6)), 0.4, M['hay'], seg=8); cyl(b, q + V((-0.12, 0.09, 0.9)), 0.42, 0.14, M['red_d'], seg=8, cap=False); cyl(b, q + V((-0.26, 0.2, 1.8)), 0.42, 0.14, M['red_d'], seg=8, cap=False)

def pick_prop(Bk, M, p, yaw, cd=30.0, kind='pick'):
    F = Frame(p, yaw); b = Bk('digtools', hull=T.hull(cd)); rod(b, F.p(0, 0, 0.16), F.p(3.2, 0.2, 0.45), 0.09, M['wood'], seg=5)
    if kind == 'pick': obox(b, F.p(3.2, 0.2, 0.5), F.X, F.Y, F.Z, 0.08, 0.6, 0.1, M['iron']); b.frustum(F.p(3.2, 0.8, 0.5), F.p(3.2, 1.2, 0.5), 0.07, 0.0, M['iron'], seg=4)
    else: obox(b, F.p(3.3, 0.2, 0.3), F.X, F.Y, F.Z, 0.3, 0.38, 0.05, M['iron'])

def build_in(Bk, M, light):
    r = _rnd(5); loc = 'jimo_in'
    # ---- ground: ring lane (packed earth with ruts), the yard (darker trampled earth with straw), the rest earth
    g = Bk('ground'); S_ = 340.0
    flat(g, V((-S_, yi(0) - 0.5, 0)), V((2 * S_, 0, 0)), V((0, S_, 0)), M['earth'], (-S_ / 8, 0, S_ / 8, S_ / 8))
    flat(g, V((-S_, -S_ + yi(0), -0.02)), V((2 * S_, 0, 0)), V((0, S_, 0)), M['grass'], (-S_ / 8, 0, S_ / 8, S_ / 8))
    ln = Bk('lane'); flat(ln, V((-92, yi(0) + 0.2, 0.03)), V((184, 0, 0)), V((0, 8.5, 0)), M['road'], (-92 / 8, 0, 92 / 8, 1.1)); flat(ln, V((-50, 12.7, 0.035)), V((100, 0, 0)), V((0, 14, 0)), M['bank'], (-50 / 8, 0, 50 / 8, 1.75))
    flat(ln, V((-86, 12.7, 0.035)), V((32, 0, 0)), V((0, 44, 0)), M['road'], (-86 / 8, 0, -54 / 8, 5.5))
    sc = Bk('straw', shadow=False)
    for k in range(60):
        x, y = r.uniform(-46, 46), r.uniform(6, 26); p0 = V((x, y, 0.06)); a = r.uniform(0, 6.28)
        sc.face([p0, p0 + V((math.cos(a) * 1.4, math.sin(a) * 1.4, 0)), p0 + V((math.cos(a) * 1.4 + 0.15, math.sin(a) * 1.4, 0.0))], M['straw'], [(0, 0)] * 3)
    # ---- the wall (inner face visible), gate hall behind it, torches along the walk
    WL.build_wall(Bk, M, loc)
    # ---- torch stands (iron / bronze tripod braziers) across the yard and at the wall foot
    for (x, y, lt) in ((-44, 9.5, 900.0), (-30, 9.0, 1100.0), (-14, 9.5, 1100.0), (14, 9.5, 1100.0), (30, 9.0, 1100.0), (44, 9.5, 900.0), (-22, 21.0, 800.0), (22, 21.0, 800.0), (0, 24.0, 700.0), (-60, 11.0, 800.0), (60, 11.0, 800.0)):
        brazier(Bk, M, (x, y, 0.0), s=1.0, light=lt, name='yt%d' % int(x), halo_r=3.4, tall=2.6, warm=None)
    for xl in (-38, -22, -6, 6, 22, 38):                                                                       # iron wall baskets on the face with a lamp each
        c = V((xl, yi(7.0) - 0.8, 7.0)); w = Bk('wood', hull=T.hull(40.0)); obox(w, tuple(c + V((0, 0.2, -0.5))), XX, YY, ZZ, 0.5, 0.45, 0.08, M['iron']); live_flame(c + V((0, 0.1, -0.3)), 1.5, 0.45, seed=xl, n=3, light=500.0, name='wb%d' % xl, warm=(3.0, 0.8))
    # ---- the ox yard: pens along the north side, troughs, hay, sheds
    for i, x in enumerate((-36, -12, 12, 36)):
        pen(Bk, M, x, 36.0, 20.0, 9.0, 0.0, cd=60.0)
    for i, x in enumerate((-26, 0, 26)): trough_hay(Bk, M, (x, 31.5, 0), 0, 50.0)
    hb = Bk('hay', hull=T.hull(60.0))
    for (x, y, s_) in ((-46, 30, 1.2), (47, 31, 1.3), (-8, 44, 1.1), (8, 44, 1.2)): hb.frustum(V((x, y, 0)), V((x, y, 3.2 * s_)), 2.2 * s_, 0.3 * s_, M['hay'], seg=9); cyl(hb, V((x, y, 0.1)), 2.3 * s_, 0.6 * s_, M['straw_d'], seg=9)
    # reed-bundle jars and bundles, water jars, sacks along the wall foot and by the holes
    for k, x in enumerate((-40, -33, -26, -19, -12, 12, 19, 26, 33, 40)): reed_jar(Bk, M, (x + 1.8, 15.5 + (k % 3) * 0.8, 0), s=1.0, cd=40.0)
    for x in (-23, 23, 0): reed_bundles(Bk, M, (x, 17.0, 0), 5, 40.0)
    # dig props: picks, baskets, earth heaps (keyed by set_holes, the dig<i> objects hold the heap / pick / basket per hole); loose ones in the foreground of the lane
    for k, (x, y, yw) in enumerate(((-30, 7.8, 25), (-16, 7.0, 150), (16, 7.5, 20), (31, 7.3, 200), (-4, 7.2, 70))): pick_prop(Bk, M, (x, y, 0), yw, 60.0, 'pick' if k % 2 else 'spade')
    for (x, y, s_) in ((-24, 7.0, 1.0), (-9, 7.5, 0.9), (9, 7.2, 1.0), (24, 7.4, 0.9)):
        b = Bk('baskets', hull=T.hull(40.0)); b.frustum(V((x, y, 0)), V((x, y, 1.0 * s_)), 0.5 * s_, 0.78 * s_, M['straw_d'], seg=10); lumpy(b, V((x, y, 1.0 * s_)), 0.7 * s_, M['bank'], int(x * 5), seg=8, rings=4, rough=0.2, squash=0.4)
    # ---- houses: the east quarter along the ring lane (gates on the lane side), two rows north of the pens
    for (x, y, w, d, h, rise) in ((58, 33, 13, 9, 6.2, 3.4), (74, 33, 13, 9, 6.0, 3.2), (89, 33, 12, 9, 6.2, 3.3), (58, 56, 13, 9, 6.4, 3.4), (74, 56, 13, 9, 6.0, 3.2), (89, 56, 12, 9, 6.2, 3.3),
                                  (-40, 62, 14, 9, 6.4, 3.4), (-22, 62, 14, 9, 6.2, 3.3), (-4, 64, 14, 10, 6.6, 3.6), (14, 62, 14, 9, 6.0, 3.2), (32, 62, 14, 9, 6.4, 3.4), (50, 62, 13, 9, 6.0, 3.2),
                                  (-90, 70, 12, 9, 6.0, 3.2), (-52, 84, 14, 10, 7.6, 3.8)):
        house(Bk, M, x, y, w, d, h, rise, 0, int(x * 3 + y), gate=True)
    for (x, y, w, d, h, rise) in ((-70, 88, 16, 10, 8.0, 4.0), (-24, 84, 16, 10, 8.0, 4.0), (4, 88, 16, 10, 8.0, 4.0), (30, 84, 16, 10, 8.0, 4.0), (56, 82, 16, 10, 8.0, 4.0), (82, 80, 14, 10, 7.6, 3.6)):
        house(Bk, M, x, y, w, d, h, rise, 0, int(x + y), gate=False)
    # ---- market (west): two rows of stalls along a lane, awnings in red / ochre / indigo / teal
    awn = [M['canvas_red'], M['hide'], M['indigo'], M['teal'], M['canvas_red'], M['canvas']]
    for k in range(7):
        y = 14 + k * 8.0
        stall(Bk, M, -77, y, 90, awn[k % 6], seed=k, clerk=(k == 1), cloth=(k % 3 == 0)); stall(Bk, M, -61, y + 3, -90, awn[(k + 3) % 6], seed=40 + k, cloth=(k % 3 == 1))
    for (x, y) in ((-69, 17), (-69, 33), (-69, 49)): brazier(Bk, M, (x, y, 0.0), s=0.9, light=700.0, name='mk%d' % int(y), halo_r=3.0, tall=2.4, warm=None)
    for k in range(5): oil_lamp(Bk, M, (-69 + (k % 2) * 3 - 1.5, 21 + k * 8, 0.0), s=0.8, light=0.0, h=3.0, halo_r=1.6)
    # ---- far town: drum tower and roofs behind, so the lanes end in lit shapes
    for (cx, cy, w, fl) in ((-69, 104, 14, 4), (34, 112, 13, 4)):
        z = 0.0
        for f in range(fl):
            ww = w * (1.0 - 0.13 * f); obox(Bk('citybody', hull=T.hull(90.0)), (cx, cy, z + 3.1), XX, YY, ZZ, ww / 2, ww / 2 * 0.8, 3.1, M['plaster'] if f == 0 else M['plaster_d'], uvk=0.3)
            flat(Bk('cityglow', shadow=False), V((cx - 1.2, cy - ww * 0.4 - 0.05, z + 1.5)), V((2.4, 0, 0)), V((0, 0, 3.0)), M['win_c'])
            hip_roof(Bk('cityroof', hull=T.hull(90.0)), (cx, cy, z + 6.2), 0, ww / 2 + 1.8, ww * 0.4 + 1.8, ww / 2 - ww * 0.4, 0.0, 2.2 if f < fl - 1 else 4.4, M, lift=0.3, nx=18, ny=10, mat=M['tiles'], wadang=False); z += 7.6
    for (gx, gy, gr) in ((-30, 50, 30), (0, 55, 30), (40, 50, 28), (-69, 50, 24)): halo(Bk('cityglow', shadow=False), V((gx, gy, 6)), gr, M['halo_big'])
    hills(Bk, M, (0.0, 40.0), 190.0, 240.0, 26, 11, (40, 66))
    STATE['marks']['wall_inner'] = 'y=%.1f at z0 (battered, +y at the base)' % yi(0)
