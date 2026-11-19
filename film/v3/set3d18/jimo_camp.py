"""jimo_camp.py : the Yan camp at night (zone 'camp' of jimo.py): canvas / hide tents with ox-blood red trims, the general's pavilion, four
campfires, black-and-red pennants, spear racks, a war chariot, drums, wine jars and cups on a low table, a wooden palisade, horses, fodder.
camp(J, Bk, M): J = the jimo module (helpers), Bk = mesh banks, M = materials."""
import math
from mathutils import Vector as V


def camp(J, Bk, M):
    r = J._rnd(18); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    # trampled earth under the camp
    g = Bk('campground'); J.flat(g, V((-95, -135, 0.03)), V((190, 0, 0)), V((0, 98, 0)), M['bank'], (0, 0, 190 / 8, 98 / 8))
    J.moat_bridge_road(Bk, M)
    cam = V(J.CAMS['camp']['loc'])
    def dist(c): return math.hypot(c[0] - cam.x, c[1] - cam.y)

    # ------------------------------------------------------------------ tents
    def tent(c, yaw, w, l, h, trim=True, hide=False, name='tent', flaps=True):
        F = J.Frame((c[0], c[1], 0), yaw); tb = Bk('tents', hull=J.T.hull(max(14.0, dist(c)))); mat = M['hide'] if hide else M['canvas']
        sl = math.hypot(w / 2, h)
        for sgn in (-1, 1):
            tb.oface([F.p(sgn * w / 2, -l / 2, 0), F.p(sgn * w / 2, l / 2, 0), F.p(0, l / 2, h), F.p(0, -l / 2, h)], mat, [(0, 0), (l / 4, 0), (l / 4, sl / 4), (0, sl / 4)], F.X * sgn + F.Z * (w / 2 / h))
            if trim:
                for t0, t1 in ((0.0, 0.14),):                                                                  # ox-blood valance along the eave
                    p = lambda t, yy: F.p(sgn * w / 2 * (1 - t) + sgn * 0.04, yy, h * t)
                    tb.oface([p(t0, -l / 2), p(t0, l / 2), p(t1, l / 2), p(t1, -l / 2)], M['red_d'], [(0, 0)] * 4, F.X * sgn + F.Z * 0.4)
                for yy in (-l / 2, l / 2):
                    p = lambda t: F.p(sgn * w / 2 * (1 - t) + sgn * 0.04, yy, h * t)
        for yy, nrm in ((-l / 2, -1), (l / 2, 1)):                                                             # gables (door at the camera-facing -y end)
            tb.oface([F.p(-w / 2, yy, 0), F.p(w / 2, yy, 0), F.p(0, yy, h)], mat, [(0, 0), (1, 0), (0.5, 1)], F.Y * nrm)
        d0 = -l / 2 - 0.05                                                                                      # door opening with the dark interior + red trim frame + two tied-back flaps
        tb.oface([F.p(-w * 0.2, d0, 0), F.p(w * 0.2, d0, 0), F.p(w * 0.2, d0, h * 0.5), F.p(0, d0, h * 0.78), F.p(-w * 0.2, d0, h * 0.5)], M['black'], [(0, 0)] * 5, F.Y * -1)
        fl = Bk('campglow', shadow=False); J.flat(fl, F.p(-w * 0.12, d0 - 0.02, 0.0), F.X * (w * 0.24), F.Z * (h * 0.42), M['win'])
        for sx in (-1, 1):
            tb.oface([F.p(sx * w * 0.2, d0 - 0.02, 0), F.p(sx * w * 0.2, d0 - 0.02, h * 0.5), F.p(sx * w * 0.2 + sx * w * 0.2, d0 - 0.02, h * 0.28), F.p(sx * w * 0.2 + sx * w * 0.2, d0 - 0.02, 0)], M['canvas_red'], [(0, 0), (0, 1), (1, 1), (1, 0)], F.Y * -1)
        rod(tb, F.p(0, -l / 2 - 1.1, h + 0.1), F.p(0, l / 2 + 1.1, h + 0.1), 0.2, M['wood_d'], seg=6) if False else J.rod(tb, F.p(0, -l / 2 - 1.1, h + 0.1), F.p(0, l / 2 + 1.1, h + 0.1), 0.2, M['wood_d'], seg=6)
        J.obox(tb, F.p(0, 0, h + 0.05), F.X, F.Y, F.Z, 0.3, l / 2, 0.22, M['red_d'])
        tb.sphere(F.p(0, -l / 2 - 1.2, h + 0.1), 0.34, M['gold'], seg=8, rings=5); tb.sphere(F.p(0, l / 2 + 1.2, h + 0.1), 0.34, M['gold'], seg=8, rings=5)
        for sgn in (-1, 1):                                                                                     # guy ropes and pegs
            for yy in (-l / 2, l / 2):
                a, b = F.p(sgn * w / 2, yy, 0.25), F.p(sgn * (w / 2 + 2.6), yy * 1.15, 0.1)
                J.rod(tb, a, b, 0.05, M['straw_d'], seg=3); J.rod(tb, b, b + V((0, 0, 0.5)), 0.1, M['wood_d'], seg=4)
        return F
    for (x, y, w, l, h, yaw, hide) in ((-11.5, -90, 9, 11, 5.4, 10, False), (12.5, -89, 9, 11, 5.4, -10, True), (-13.5, -76, 12, 14, 7.0, 6, True), (14.5, -75, 12, 14, 7.0, -6, False),
                                       (-15.0, -58, 12, 13, 6.6, 8, False), (16.0, -57, 12, 13, 6.6, -8, True), (-30, -70, 11, 13, 6.2, 15, False), (32, -68, 11, 13, 6.2, -15, False),
                                       (-9, -49, 8, 9, 4.6, 0, True), (24, -48, 10, 12, 5.8, 3, False), (-47, -58, 10, 12, 5.8, 6, False), (48, -58, 10, 12, 5.8, -6, False), (-27, -88, 9, 11, 5.4, -14, False), (30, -87, 9, 11, 5.4, 14, False)):
        tent((x, y), yaw, w, l, h, hide=hide)
    # the general's pavilion (large, red-trimmed, raised awning on two poles) at the back-left
    F = tent((-27, -47), 0, 15, 15, 8.2, hide=False)
    tb = Bk('tents', hull=J.T.hull(60.0))
    for sx in (-1, 1):
        J.rod(tb, F.p(sx * 6.5, -10.5, 0), F.p(sx * 6.5, -10.5, 6.4), 0.28, M['red'], seg=8)
        J.rod(tb, F.p(sx * 6.5, -10.5, 6.4), F.p(sx * 3.2, -7.5, 8.0), 0.18, M['wood_d'], seg=6)
    tb.oface([F.p(-7.4, -10.6, 6.5), F.p(7.4, -10.6, 6.5), F.p(7.4, -7.4, 8.0), F.p(-7.4, -7.4, 8.0)], M['canvas_red'], [(0, 0), (4, 0), (4, 1), (0, 1)], (0, 0, 1))
    tb.oface([F.p(-7.4, -10.6, 6.5), F.p(7.4, -10.6, 6.5), F.p(7.4, -10.5, 5.6), F.p(-7.4, -10.5, 5.6)], M['red_d'], [(0, 0)] * 4, (0, -1, 0))
    for k in range(9): tb.sphere(F.p(-7.0 + k * 1.75, -10.6, 5.5), 0.22, M['gold'], seg=6, rings=4)

    # ------------------------------------------------------------------ fires with seats and pots
    def fire(c, s=1.0, light=1500.0, name='f'):
        c = V((c[0], c[1], 0.0)); f = Bk('fire', shadow=False); st = Bk('firestone', hull=J.T.hull(max(10.0, dist(c)))); lg = Bk('logs', hull=J.T.hull(max(10.0, dist(c))))
        for k in range(10):
            a = 2 * math.pi * k / 10; J.lumpy(st, c + V((1.25 * s * math.cos(a), 1.25 * s * math.sin(a), 0.2 * s)), 0.38 * s, M['stone'] if k % 2 else M['stone_d'], 40 + k, seg=7, rings=4, rough=0.2, squash=0.7)
        for k in range(5):
            a = 2 * math.pi * k / 5 + 0.3; J.rod(lg, c + V((1.0 * s * math.cos(a), 1.0 * s * math.sin(a), 0.25 * s)), c + V((-0.2 * s * math.cos(a), -0.2 * s * math.sin(a), 0.75 * s)), 0.18 * s, M['wood_d'], seg=6, r1=0.14 * s)
        rr = J._rnd(int(c.x * 3 + c.y));
        for k in range(7):
            a = rr.uniform(0, 6.28); dx, dy = 0.45 * s * math.cos(a), 0.45 * s * math.sin(a); hh = rr.uniform(1.6, 3.0) * s
            f.frustum(c + V((dx, dy, 0.5 * s)), c + V((dx * 0.4 + rr.uniform(-0.2, 0.2), dy * 0.4, 0.5 * s + hh)), 0.5 * s, 0.0, M['flame'], seg=6, cap1=False)
        for k in range(3):
            a = rr.uniform(0, 6.28); f.frustum(c + V((0.15 * s * math.cos(a), 0.15 * s * math.sin(a), 0.5 * s)), c + V((0.05 * s, 0, 0.5 * s + rr.uniform(1.4, 2.0) * s)), 0.32 * s, 0.0, M['flame_c'], seg=6, cap1=False)
        for k in range(14): f.sphere(c + V((rr.uniform(-1.4, 1.4) * s, rr.uniform(-1.4, 1.4) * s, rr.uniform(2.6, 5.0) * s)), 0.06 * s, M['ember'], seg=4, rings=3)   # sparks
        h = Bk('halos', shadow=False); J.halo(h, c + V((0, 0, 1.4 * s)), 4.4 * s, M['halo'])
        pl = Bk('pools', shadow=False); R = 7.5 * s; J.flat(pl, c + V((-R, -R, 0.07)), V((2 * R, 0, 0)), V((0, 2 * R, 0)), M['pool'])
        J.lamp(name, c + V((0, 0, 1.6 * s)), light * 0.7 * s, J.FIRE, r=0.5, shadow=False)
        for k in range(3):                                                                                      # log seats around it
            a = 2 * math.pi * k / 3 + 1.0; p = c + V((3.2 * s * math.cos(a), 3.2 * s * math.sin(a), 0.0)); J.cyl(lg, p, 0.32 * s, 0.6 * s, M['wood'], seg=8)
        return c
    # fire 1 low and near, fire 2/3 mid, fire 4 far; one with a pot on a tripod
    f1 = fire((5.5, -85.0), 0.9, 1500.0, 'fire1'); f2 = fire((-6.0, -72.0), 1.1, 1700.0, 'fire2'); f3 = fire((7.0, -68.0), 1.1, 1700.0, 'fire3'); f4 = fire((-4.0, -57.0), 1.0, 1500.0, 'fire4')
    f0 = fire((1.4, -104.6), 0.7, 1300.0, 'fire0')
    for c in (f2, f3, f4):
        tp = Bk('props', hull=J.T.hull(30.0))
        for k in range(3):
            a = 2 * math.pi * k / 3; J.rod(tp, c + V((2.2 * math.cos(a), 2.2 * math.sin(a), 0)), c + V((0.1 * math.cos(a), 0.1 * math.sin(a), 4.0)), 0.1, M['wood_d'], seg=5)
        J.ellipsoid(tp, c + V((0, 0, 2.3)), 0.95, 0.95, 0.8, M['iron'], seg=12, rings=7); J.cyl(tp, c + V((0, 0, 3.0)), 0.85, 0.18, M['iron'], seg=12)

    # ------------------------------------------------------------------ the general's toast: low table with wine jars, cups, a bowl, stools (foreground left)
    pr = Bk('props', hull=J.T.hull(11.0)); F = J.Frame((-2.6, -104.6, 0), 22)
    pr.box((-2.1, -1.1, 0.0), (2.1, 1.1, 0.0), M['red']) if False else None
    J.obox(pr, F.p(0, 0, 1.15), F.X, F.Y, F.Z, 2.3, 1.25, 0.14, M['red']); J.obox(pr, F.p(0, 0, 1.0), F.X, F.Y, F.Z, 2.4, 1.35, 0.08, M['gold'])
    for sx in (-1, 1):
        for sy in (-1, 1): J.obox(pr, F.p(sx * 1.9, sy * 1.0, 0.55), F.X, F.Y, F.Z, 0.18, 0.18, 0.55, M['red_d'])
    for k, (jx, jy, js) in enumerate(((-1.5, 0.3, 1.0), (-0.5, -0.5, 0.85), (1.7, 0.4, 1.0), (0.2, 0.6, 0.8))):                                  # wine jars on the table
        p = F.p(jx, jy, 1.3); J.ellipsoid(pr, p + V((0, 0, 0.55 * js)), 0.55 * js, 0.55 * js, 0.62 * js, M['clay'], seg=12, rings=8, rough=0.04, seed=k)
        J.cyl(pr, p + V((0, 0, 1.05 * js)), 0.28 * js, 0.28 * js, M['clay_d'], seg=10, r1=0.34 * js); J.cyl(pr, p + V((0, 0, 1.33 * js)), 0.4 * js, 0.16 * js, M['red'], seg=10)
        J.cyl(pr, p + V((0, 0, 0.45 * js)), 0.585 * js, 0.12 * js, M['gold'], seg=12) if False else None
    for k in range(6):                                                                                          # bronze cups (jue) and a bowl
        p = F.p(-1.9 + k * 0.7, -0.75 + (k % 2) * 0.1, 1.27)
        J.cyl(pr, p, 0.2, 0.34, M['bronze'], seg=8, r1=0.3); J.cyl(pr, p + V((0, 0, -0.04)), 0.1, 0.06, M['bronze'], seg=6)
    J.ellipsoid(pr, F.p(0.9, -0.3, 1.5), 0.55, 0.55, 0.36, M['bronze'], seg=12, rings=6, th=(math.pi / 2, math.pi))
    J.lantern(Bk, M, tuple(F.p(1.0, 0.0, 2.2)), s=0.8, light=260.0, name='table_lamp', halo_r=2.2, hang=0.0)
    # large jars on the ground beside it (straw-bound necks), a barrel, a crate
    for k, (jx, jy, js) in enumerate(((-4.6, 0.8, 1.1), (-5.4, -0.6, 1.0), (-3.6, -1.0, 0.8), (4.2, 1.4, 1.0))):
        p = F.p(jx, jy, 0.0); J.ellipsoid(pr, p + V((0, 0, 0.9 * js)), 0.75 * js, 0.75 * js, 0.95 * js, M['clay'] if k % 2 else M['clay_d'], seg=12, rings=8, rough=0.05, seed=20 + k)
        J.cyl(pr, p + V((0, 0, 1.75 * js)), 0.42 * js, 0.45 * js, M['clay_d'], seg=10, r1=0.5 * js); J.cyl(pr, p + V((0, 0, 2.15 * js)), 0.55 * js, 0.2 * js, M['red'], seg=10)
        J.cyl(pr, p + V((0, 0, 1.5 * js)), 0.46 * js, 0.2 * js, M['straw'], seg=10, cap=False)
    for k, sx in enumerate((-2.2, 3.2)):                                                                        # low round stools with red cushions
        J.cyl(pr, F.p(sx, -2.6, 0.0), 0.5, 0.5, M['wood'], seg=10); J.cyl(pr, F.p(sx, -2.6, 0.5), 0.58, 0.1, M['red'], seg=10)

    # ------------------------------------------------------------------ war chariot (foreground right)
    def chariot(c, yaw, s=1.0, cd=11.0):
        F = J.Frame((c[0], c[1], 0), yaw); ch = Bk('chariot', hull=J.T.hull(cd))
        for sy in (-1, 1):                                                                                      # two spoked wheels, R 1.6
            Rw = 1.6 * s
            for i in range(20):
                a0, a1 = 2 * math.pi * i / 20, 2 * math.pi * (i + 1) / 20
                J.beam(ch, F.p(0, sy * 2.35 * s, Rw + Rw * math.sin(a0)) + F.X * (Rw * math.cos(a0)), F.p(0, sy * 2.35 * s, Rw + Rw * math.sin(a1)) + F.X * (Rw * math.cos(a1)), 0.34 * s, 0.5 * s, M['wood_d'], up=(0, 1, 0))
            for i in range(9):
                a = math.pi * i / 9; J.rod(ch, F.p(Rw * math.cos(a), sy * 2.35 * s, Rw + Rw * math.sin(a)), F.p(-Rw * math.cos(a), sy * 2.35 * s, Rw - Rw * math.sin(a)), 0.1 * s, M['wood'], seg=5)
            J.rod(ch, F.p(0, sy * 2.0 * s, Rw), F.p(0, sy * 2.8 * s, Rw), 0.38 * s, M['red'], seg=8)
        J.rod(ch, F.p(0, -2.9 * s, 1.6 * s), F.p(0, 2.9 * s, 1.6 * s), 0.12 * s, M['iron'], seg=6)
        J.obox(ch, F.p(-0.3 * s, 0, 2.0 * s), F.X, F.Y, F.Z, 1.5 * s, 1.9 * s, 0.12 * s, M['wood'])                                 # floor
        for sy in (-1, 1): J.obox(ch, F.p(0.0, sy * 1.85 * s, 2.9 * s), F.X, F.Y, F.Z, 1.4 * s, 0.1 * s, 0.9 * s, M['red'])      # side rails
        J.obox(ch, F.p(1.45 * s, 0, 2.9 * s), F.X, F.Y, F.Z, 0.1 * s, 1.9 * s, 0.9 * s, M['red']); J.obox(ch, F.p(1.45 * s, 0, 3.85 * s), F.X, F.Y, F.Z, 0.14 * s, 1.95 * s, 0.1 * s, M['gold'])
        J.rod(ch, F.p(-0.2 * s, 0, 2.1 * s), F.p(6.5 * s, 0, 2.6 * s), 0.2 * s, M['wood'], seg=6)                                   # pole
        J.obox(ch, F.p(6.6 * s, 0, 2.9 * s), F.X, F.Y, F.Z, 0.15 * s, 1.5 * s, 0.15 * s, M['wood_d'])
        J.rod(ch, F.p(-0.4 * s, 0.0, 2.1 * s), F.p(-0.4 * s, 0.0, 6.6 * s), 0.12 * s, M['wood_d'], seg=6)                         # canopy pole and cone
        ch.frustum(F.p(-0.4 * s, 0, 5.8 * s), F.p(-0.4 * s, 0, 7.6 * s), 2.3 * s, 0.1 * s, M['canvas_red'], seg=14, cap0=False)
        ch.sphere(F.p(-0.4 * s, 0, 7.75 * s), 0.2 * s, M['gold'], seg=6, rings=4)
        for k in range(14): a = 2 * math.pi * k / 14; ch.sphere(F.p(-0.4 * s + 2.3 * s * math.cos(a), 2.3 * s * math.sin(a), 5.75 * s), 0.1 * s, M['gold'], seg=4, rings=3)
    chariot((6.6, -103.0), 28, 0.9, 9.0); chariot((-21.5, -83), 150, 0.9, 40.0)

    # ------------------------------------------------------------------ drums, spear racks, shields, fodder, barrels, horses, pennants
    def drum(c, s=1.0, cd=40.0):
        c = V((c[0], c[1], 0.0)); d = Bk('props', hull=J.T.hull(cd))
        for sx in (-1, 1): J.beam(d, c + V((sx * 1.1 * s, 0, 0)), c + V((-sx * 0.4 * s, 0, 2.6 * s)), 0.25 * s, 0.25 * s, M['wood_d'])
        d.frustum(c + V((0, 0, 0.8 * s)), c + V((0, 0, 1.4 * s)), 0.95 * s, 1.25 * s, M['red'], seg=14, cap0=False, cap1=False)
        d.frustum(c + V((0, 0, 1.4 * s)), c + V((0, 0, 2.1 * s)), 1.25 * s, 0.95 * s, M['red'], seg=14, cap0=False, cap1=False)
        d.frustum(c + V((0, 0, 2.1 * s)), c + V((0, 0, 2.2 * s)), 0.95 * s, 0.95 * s, M['cream'], seg=14)
        for k in range(14):
            a = 2 * math.pi * k / 14; d.sphere(c + V((0.96 * s * math.cos(a), 0.96 * s * math.sin(a), 2.12 * s)), 0.07 * s, M['gold'], seg=4, rings=3)
        d.frustum(c + V((0, 0, 1.38 * s)), c + V((0, 0, 1.46 * s)), 1.27 * s, 1.27 * s, M['gold'], seg=14, cap0=False, cap1=False)
        for sx in (-1, 1): J.rod(d, c + V((sx * 0.3 * s, 0.4 * s, 2.35 * s)), c + V((sx * 0.9 * s, -0.4 * s, 2.5 * s)), 0.06 * s, M['wood'], seg=4)
    drum((-6.5, -82.0), 1.1, 30.0); drum((8.5, -79.0), 1.0, 32.0)
    def rack(c, yaw, cd=35.0):
        F = J.Frame((c[0], c[1], 0), yaw); rk = Bk('props', hull=J.T.hull(cd))
        for sx in (-1, 1): J.obox(rk, F.p(sx * 2.4, 0, 1.9), F.X, F.Y, F.Z, 0.18, 0.18, 1.9, M['wood_d'])
        for z in (1.1, 2.7): J.obox(rk, F.p(0, 0, z), F.X, F.Y, F.Z, 2.5, 0.14, 0.12, M['wood'])
        for k in range(9):
            x = -2.0 + k * 0.5; top = F.p(x * 0.8 + 0.2, 0.55, 6.0 + 0.3 * math.sin(k)); base = F.p(x, 1.1, 0.0)
            J.rod(rk, base, top, 0.05, M['wood'], seg=4)
            tipd = (top - base).normalized(); rk.frustum(top, top + tipd * 0.9, 0.12, 0.0, M['steel'], seg=4, cap0=True)
            if k % 3 == 0: rk.frustum(top - tipd * 0.35, top - tipd * 0.5, 0.2, 0.2, M['red'], seg=6)
    rack((-9.5, -81.0), 5, 30.0); rack((10.8, -73.0), -8, 40.0); rack((23.0, -62.0), 10, 50.0)
    def shield(c, yaw, cd=35.0):
        F = J.Frame((c[0], c[1], 0), yaw); sb = Bk('props', hull=J.T.hull(cd))
        J.rod(sb, F.p(-0.8, 0.0, 0.0), F.p(-0.3, -0.3, 2.6), 0.1, M['wood_d'], seg=4); J.rod(sb, F.p(0.8, 0.0, 0.0), F.p(0.3, -0.3, 2.6), 0.1, M['wood_d'], seg=4)
        J.ellipsoid(sb, F.p(0, -0.45, 2.5), 1.25, 0.28, 1.25, M['hide'], seg=16, rings=8, th=(0, math.pi))
        J.ellipsoid(sb, F.p(0, -0.78, 2.5), 0.4, 0.16, 0.4, M['gold'], seg=10, rings=5, th=(0, math.pi))
        sb.frustum(F.p(-1.25, -0.4, 2.5), F.p(-1.25, -0.5, 2.5), 0.0, 0.0, M['red'], seg=3)
        for k in range(18):
            a = 2 * math.pi * k / 18; sb.sphere(F.p(1.22 * math.cos(a), -0.52, 2.5 + 1.22 * math.sin(a)), 0.09, M['red'], seg=4, rings=3)
    for (x, y, yw) in ((-1.5, -66.0, 8), (1.2, -65.5, -6), (8.0, -62.5, 16), (-8.0, -64.0, -10)): shield((x, y), yw)
    def haystack(c, s=1.0, cd=30.0):
        c = V((c[0], c[1], 0.0)); hb = Bk('hay', hull=J.T.hull(cd))
        hb.frustum(c, c + V((0, 0, 3.4 * s)), 2.4 * s, 0.35 * s, M['hay'], seg=9)
        J.cyl(hb, c + V((0, 0, 0.1 * s)), 2.5 * s, 0.7 * s, M['straw_d'], seg=9)
        for k in range(8): a = 2 * math.pi * k / 8; J.rod(hb, c + V((0.3 * s * math.cos(a), 0.3 * s * math.sin(a), 3.0 * s)), c + V((1.6 * s * math.cos(a), 1.6 * s * math.sin(a), 0.2 * s)), 0.05 * s, M['straw'], seg=3)
    for (x, y, s_) in ((27.0, -82.0, 1.2), (-27.0, -84.0, 1.1), (38.0, -58.0, 1.3), (-38.0, -56.0, 1.2)): haystack((x, y), s_)
    def bundles(c, n=4, cd=30.0):
        bb = Bk('hay', hull=J.T.hull(cd))
        for k in range(n):
            p = V((c[0], c[1], 0.0)) + V((k * 1.0 - n / 2, (k % 2) * 0.6, 0.0)); J.cyl(bb, p, 0.5, 2.4, M['hay'], seg=8); J.cyl(bb, p + V((0, 0, 0.8)), 0.53, 0.14, M['red_d'], seg=8); J.cyl(bb, p + V((0, 0, 1.7)), 0.53, 0.14, M['red_d'], seg=8)
    bundles((28.0, -60.0), 5, 55.0); bundles((-23.0, -60.0), 4, 55.0)
    def barrel(c, cd=30.0):
        c = V((c[0], c[1], 0.0)); bb = Bk('props', hull=J.T.hull(cd)); bb.frustum(c, c + V((0, 0, 1.0)), 0.7, 0.85, M['wood'], seg=10); bb.frustum(c + V((0, 0, 1.0)), c + V((0, 0, 2.0)), 0.85, 0.7, M['wood'], seg=10)
        for z in (0.35, 1.0, 1.65): J.cyl(bb, c + V((0, 0, z)), 0.88 if z == 1.0 else 0.78, 0.1, M['iron'], seg=10, cap=False)
    for (x, y) in ((9.5, -74.5), (10.9, -73.6), (-5.0, -62.0), (-22.0, -77.0)): barrel((x, y))
    cr = Bk('props', hull=J.T.hull(30.0))
    for (x, y, s_) in ((-8.0, -66.5, 1.0), (-6.7, -66.0, 0.8), (-4.8, -66.8, 0.9)): J.obox(cr, (x, y, s_ * 0.9), X, Y, Z, 0.9 * s_, 0.9 * s_, 0.9 * s_, M['planks'], uvk=0.6)

    def horse(c, yaw, col, s=1.0, cd=40.0):
        F = J.Frame((c[0], c[1], 0), yaw); hb = Bk('horses', hull=J.T.hull(cd))
        J.ellipsoid(hb, F.p(0, 0, 3.0 * s), 1.7 * s, 0.7 * s, 0.85 * s, col, seg=12, rings=8, rough=0.03, seed=4)
        J.ellipsoid(hb, F.p(1.2 * s, 0, 3.3 * s), 0.85 * s, 0.62 * s, 0.8 * s, col, seg=10, rings=6)
        hb.frustum(F.p(1.6 * s, 0, 3.4 * s), F.p(2.5 * s, 0, 4.9 * s), 0.5 * s, 0.33 * s, col, seg=8)
        J.ellipsoid(hb, F.p(2.95 * s, 0, 5.05 * s), 0.75 * s, 0.32 * s, 0.4 * s, col, seg=10, rings=6, fn=None)
        for sx in (-1, 1): hb.frustum(F.p(2.35 * s, sx * 0.15 * s, 5.4 * s), F.p(2.3 * s, sx * 0.25 * s, 5.95 * s), 0.13 * s, 0.0, col, seg=4)
        for k in range(5): J.rod(hb, F.p(2.0 * s - k * 0.15 * s, 0, 5.0 * s - k * 0.35 * s), F.p(1.8 * s - k * 0.15 * s, 0, 4.4 * s - k * 0.35 * s), 0.22 * s, M['black'], seg=4)
        for (lx, ly) in ((1.2, 0.4), (1.2, -0.4), (-1.2, 0.4), (-1.2, -0.4)):
            J.rod(hb, F.p(lx * s, ly * s, 2.6 * s), F.p(lx * s * 1.05, ly * s * 1.1, 0.25 * s), 0.17 * s, col, seg=6, r1=0.11 * s); J.cyl(hb, F.p(lx * s * 1.05, ly * s * 1.1, 0.0), 0.15 * s, 0.25 * s, M['black'], seg=6)
        J.rod(hb, F.p(-1.7 * s, 0, 3.4 * s), F.p(-2.5 * s, 0, 1.4 * s), 0.18 * s, M['black'], seg=5, r1=0.06 * s)
        J.rod(hb, F.p(-1.7 * s, 0, 3.4 * s), F.p(-2.1 * s, 0.1 * s, 1.6 * s), 0.12 * s, M['black'], seg=5, r1=0.05 * s)
        J.obox(hb, F.p(0.3 * s, 0, 3.9 * s), F.X, F.Y, F.Z, 0.9 * s, 0.76 * s, 0.07 * s, M['red'])                                    # saddle cloth with gold trim
    horse((-13.5, -69.5), 40, M['ox'], 1.0, 42.0); horse((13.5, -66.5), 150, M['straw_d'], 1.0, 45.0); horse((3.5, -51.5), 200, M['ox_d'], 0.95, 60.0)

    def pennant(c, h, cd=40.0, col=None):
        J.banner(Bk, M, c, h, 4.2, 2.4, col or M['black'], M['red'], wave=c[0], yaw=(c[0] * 7) % 40 - 20, sw=True)
    for (x, y) in ((-15.5, -84), (16.5, -82), (-23, -70), (25, -68), (-8, -60), (9, -58), (-14, -50), (16, -50), (-36, -60), (38, -58), (-42, -50), (44, -48), (-50, -70), (52, -70)):
        pennant((x, y, 0.0), 13.0 + (x % 5))

    # ------------------------------------------------------------------ palisade with a central gap and watch posts
    pl = Bk('palisade', hull=0.0); rr = J._rnd(3); y0 = -40.0
    for k in range(-122, 123):
        x = k * 0.62 + rr.uniform(-0.04, 0.04)
        if abs(x) < 6.2: continue
        h = 5.6 + rr.uniform(-0.4, 0.6); yy = y0 + rr.uniform(-0.12, 0.12)
        pl.frustum(V((x, yy, 0)), V((x, yy, h)), 0.30, 0.30, M['wood'] if k % 3 else M['wood_d'], seg=6, cap0=False, cap1=False)
        pl.frustum(V((x, yy, h)), V((x, yy, h + 1.0)), 0.30, 0.0, M['wood'] if k % 3 else M['wood_d'], seg=6, cap0=False, cap1=False)
    for z in (1.6, 4.0):
        for xa, xb in ((-76, -6.4), (6.4, 76)): J.obox(pl, ((xa + xb) / 2, y0 + 0.4, z), X, Y, Z, (xb - xa) / 2, 0.14, 0.18, M['wood_d'])
    for sx in (-1, 1):                                                                                          # gate posts with a lintel, red tassels, torches
        J.rod(pl, V((sx * 6.6, y0, 0)), V((sx * 6.6, y0, 8.4)), 0.45, M['red'], seg=8)
        J.torch_post(Bk, M, (sx * 8.4, y0 - 1.2, 0.0), s=1.5, light=1100.0, name='pg%d' % sx, halo_r=3.0)
    J.obox(pl, (0, y0, 8.4), X, Y, Z, 7.2, 0.35, 0.4, M['red']); J.obox(pl, (0, y0, 7.6), X, Y, Z, 6.7, 0.2, 0.22, M['wood_d'])
    for (xt, s_) in ((-30.0, 1.0), (30.0, 1.0), (-52.0, 1.0), (52.0, 1.0)):
        J.torch_post(Bk, M, (xt, y0 - 1.3, 0.0), s=1.6, light=1000.0, name='pt%d' % int(xt), halo_r=3.0)
    # a few extra warm lanterns on tent poles and the pavilion
    for (x, y, z) in ((-6.0, -79.0, 6.4), (8.0, -75.0, 6.4), (-20.0, -70.0, 6.2), (21.0, -66.0, 6.2)):
        J.lantern(Bk, M, (x, y, z), s=1.0, light=0.0, halo_r=2.0, hang=0.8)
    sc = Bk('scatter', hull=J.T.hull(10.0)); rr2 = J._rnd(77)
    J.rod(sc, V((-3.0, -101.0, 0.12)), V((-9.0, -99.0, 0.14)), 0.07, M['wood'], seg=4); sc.frustum(V((-3.0, -101.0, 0.12)), V((-1.8, -101.4, 0.14)), 0.1, 0.0, M['steel'], seg=4)
    J.ellipsoid(sc, V((-0.2, -102.0, 0.35)), 0.55, 0.55, 0.42, M['iron'], seg=10, rings=6, th=(math.pi / 2, math.pi)); sc.sphere(V((-0.2, -102.0, 0.78)), 0.1, M['red'], seg=5, rings=3)
    for k in range(14): J.lumpy(sc, V((rr2.uniform(-7, 9), rr2.uniform(-108, -96), 0.1)), rr2.uniform(0.15, 0.45), M['stone_d'], 90 + k, seg=6, rings=4, rough=0.25, squash=0.6)
    for k in range(16):
        p0 = V((rr2.uniform(-8, 9), rr2.uniform(-107, -95), 0.0)); sc.frustum(p0, p0 + V((rr2.uniform(-0.6, 0.6), rr2.uniform(-0.6, 0.6), 0.06)), 0.05, 0.05, M['straw'], seg=3)
    for k in range(7):                                                                                        # firewood pile at the bottom edge
        a = rr2.uniform(-0.5, 0.5); p0 = V((2.2 + 0.5 * (k % 4), -107.4 + 0.35 * (k // 4), 0.22 + 0.4 * (k // 4)))
        J.rod(sc, p0, p0 + V((math.cos(a) * 2.2, math.sin(a) * 2.2, 0.0)), 0.22, M['wood_d'] if k % 2 else M['wood'], seg=6)
    for k in range(7): J.cyl(sc, V((rr2.uniform(1.5, 5.5), rr2.uniform(-100.5, -97.5), 0.0)), 0.28, 0.22, M['bronze'], seg=8, r1=0.38)
    J.STATE['marks'].update(table=(-6.5, -95.0), chariot=(10.5, -95.5), fires=[tuple(f1), tuple(f2), tuple(f3), tuple(f4)])
