def gate_tower(Bk, M, zone):
    """Warring-States gate hall: a two-stage timber hall on the wall top with dark-lacquer posts, plain grey hip roofs with near-straight eaves and wadang
    eaves tiles (no curled horns), simple block brackets, bronze standing lamps and braziers instead of paper lanterns, plain dyed banners."""
    wd = Bk('tower', hull=T.hull(62.0 if zone != 'camp' else 100.0)); z0 = WH; cz = 0.0; yc = (yo(WH) + yi(WH)) / 2
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    obox(wd, (cz, yc, z0 + 0.5), X, Y, Z, 10.2, 4.2, 0.5, M['stone'], uvk=0.3)                               # plinth
    for xp in np.linspace(-8.4, 8.4, 7):                                                                      # dark lacquer posts, front and back
        for ys in (-3.4, 3.4): rod(wd, (xp, yc + ys, z0 + 1.0), (xp, yc + ys, z0 + 7.2), 0.40, M['lacq'], seg=10)
    for ys in (-3.4, 3.4):
        for xp in np.linspace(-8.4, 8.4, 6):
            xm = xp + 1.4
            obox(wd, (xm, yc + ys * 0.94, z0 + 4.1), X, Y, Z, 1.4, 0.16, 3.1, M['planks_d'], uvk=0.5)
        for xm in (-4.2, 0.0, 4.2):                                                                            # three lit lattice windows only
            fl = Bk('tw_glow', shadow=False); flat(fl, V((xm - 0.95, yc + ys * 0.99 - (0.02 if ys < 0 else -0.02), z0 + 2.4)), V((1.9, 0, 0)), V((0, 0, 2.6)), M['win'])
            for k in range(1, 4): obox(wd, (xm - 0.95 + k * 0.475, yc + ys * 1.0 - (0.05 if ys < 0 else -0.05), z0 + 3.7), X, Y, Z, 0.05, 0.06, 1.3, M['wood_d'])
            for zz in (2.4, 3.7, 5.0): obox(wd, (xm, yc + ys * 1.0 - (0.05 if ys < 0 else -0.05), z0 + zz), X, Y, Z, 0.95, 0.06, 0.05, M['wood_d'])
    for ys in (-3.4, 3.4): obox(wd, (cz, yc + ys, z0 + 7.4), X, Y, Z, 9.2, 0.4, 0.4, M['lacq'])
    for xp in np.linspace(-8.4, 8.4, 7):                                                                      # plain block bracket sets
        for ys in (-3.7, 3.7): obox(wd, (xp, yc + ys, z0 + 7.9), X, Y, Z, 0.55, 0.5, 0.28, M['wood_l'])
    rf = Bk('roof', hull=T.hull(62.0 if zone != 'camp' else 100.0))
    hip_roof(rf, (cz, yc, z0 + 8.4), 0, 12.8, 6.9, 6.0, 0.0, 2.8, M, lift=0.3, mat=M['tiles'])
    # second stage: a smaller hall
    z1 = z0 + 11.4
    obox(wd, (cz, yc, z1 - 0.3), X, Y, Z, 8.4, 3.9, 0.35, M['wood'], uvk=0.4)
    for xp in np.linspace(-7.2, 7.2, 5):
        for ys in (-3.0, 3.0): rod(wd, (xp, yc + ys, z1), (xp, yc + ys, z1 + 4.6), 0.36, M['lacq'], seg=10)
    for ys in (-3.0, 3.0):
        for xm in (-5.4, -1.8, 1.8, 5.4):
            obox(wd, (xm, yc + ys * 0.95, z1 + 2.3), X, Y, Z, 1.7, 0.14, 2.2, M['planks_d'], uvk=0.5)
        for xm in (-1.8, 1.8):
            fl = Bk('tw_glow', shadow=False); flat(fl, V((xm - 0.9, yc + ys * 0.99 - (0.02 if ys < 0 else -0.02), z1 + 1.2)), V((1.8, 0, 0)), V((0, 0, 2.2)), M['win_c'])
    for sx in (-1, 1): obox(wd, (sx * 7.4, yc, z1 + 2.3), X, Y, Z, 0.2, 3.0, 2.2, M['planks_d'], uvk=0.5)
    obox(wd, (cz, yc - 3.0, z1 + 4.8), X, Y, Z, 7.6, 0.35, 0.35, M['lacq']); obox(wd, (cz, yc + 3.0, z1 + 4.8), X, Y, Z, 7.6, 0.35, 0.35, M['lacq'])
    for xp in np.linspace(-7.2, 7.2, 5):
        for ys in (-3.4, 3.4): obox(wd, (xp, yc + ys, z1 + 5.2), X, Y, Z, 0.6, 0.5, 0.28, M['wood_l'])
    hip_roof(rf, (cz, yc, z1 + 5.4), 0, 10.4, 6.0, 4.4, 0.0, 3.6, M, lift=0.3, mat=M['tiles'])
    # bronze standing lamps on the plinth between the posts, braziers flanking the hall, plain banners
    for xl in (-9.8, -4.2, 4.2, 9.8): oil_lamp(Bk, M, (xl, yc - 3.95, z0 + 1.0), s=0.8, light=(220.0 if abs(xl) < 6 else 0.0), name='tl%d' % int(xl), halo_r=1.8, h=3.0)
    banner(Bk, M, (-10.0, yc - 2.0, z0 + 1.0), 12.0, 4.2, 6.5, M['red_d'], M['gold'], wave=0.5)
    banner(Bk, M, (10.0, yc - 2.0, z0 + 1.0), 12.0, 4.2, 6.5, M['teal'], M['gold'], wave=2.0, yaw=0.0)
    for xt in (-13.5, 13.5): torch_post(Bk, M, (xt, yo(WH) + 1.6, WH), s=1.3, light=800.0, name='tt%d' % int(xt), halo_r=3.6)


def city(Bk, M, zone):
    """Roofs of Jimo peeking above the wall: houses with tiled hip roofs and lit windows, a drum tower, a granary."""
    r = _rnd(31); rf = Bk('cityroof', hull=T.hull(80.0)); bd = Bk('citybody', hull=T.hull(80.0)); gl = Bk('cityglow', shadow=False)
    X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    def house(cx, cy, w, d, h, rise, yaw=0.0):
        F = Frame((cx, cy, 0), yaw)
        obox(bd, F.p(0, 0, h / 2), F.X, F.Y, F.Z, w / 2, d / 2, h / 2, M['plaster'] if r.random() < 0.6 else M['wood_l'], uvk=0.3)
        hip_roof(rf, (cx, cy, h), yaw, w / 2 + 1.3, d / 2 + 1.3, max(0.0, w / 2 - d / 2), 0.0, rise, M, lift=0.25, nx=14, ny=8, mat=M['tiles'], wadang=False)
        for k in range(int(w // 3.2)):
            xx = -w / 2 + 1.6 + k * 3.2; zz = h * 0.55
            if r.random() < 0.8: flat(gl, F.p(xx - 0.5, -d / 2 - 0.03, zz - 0.5), F.X * 1.0, F.Z * 1.2, M['win'])
        return F
    spots = [(-52, 12, 14, 9, 17, 5.5), (-34, 14, 16, 10, 20, 6.0), (-19, 11, 12, 9, 16, 5.0), (19, 12, 14, 9, 18, 5.5), (34, 11, 16, 10, 16, 5.2), (52, 14, 14, 10, 21, 6.0),
             (-70, 15, 14, 10, 18, 5.5), (68, 12, 12, 9, 15, 5.0), (-44, 30, 18, 12, 24, 6.5), (42, 32, 18, 12, 23, 6.5), (0, 40, 20, 14, 26, 7.0), (-8, 20, 12, 8, 19, 5.0), (9, 24, 14, 9, 21, 5.6),
             (-26, 28, 12, 9, 22, 5.5), (26, 26, 12, 9, 21, 5.5)]
    for (cx, cy, w, d, h, rise) in spots: house(cx, cy, w, d, h, rise)
    # the drum tower: three stacked storeys with shrinking roofs; a granary with a tall roof
    def tower(cx, cy, w, floors=3, fh=6.2):
        z = 0.0
        for f in range(floors):
            ww = w * (1.0 - 0.13 * f); obox(bd, (cx, cy, z + fh / 2), X, Y, Z, ww / 2, ww / 2 * 0.8, fh / 2, M['plaster_d'] if f else M['plaster'], uvk=0.3)
            for sx in (-1, 1):
                for sy in (-1, 1): rod(bd, (cx + sx * ww / 2, cy + sy * ww * 0.4, z), (cx + sx * ww / 2, cy + sy * ww * 0.4, z + fh), 0.35, M['red'], seg=8)
            flat(gl, V((cx - 1.2, cy - ww * 0.4 - 0.05, z + fh * 0.3)), V((2.4, 0, 0)), V((0, 0, fh * 0.45)), M['win_c'])
            hip_roof(rf, (cx, cy, z + fh), 0, ww / 2 + 1.8, ww * 0.4 + 1.8, ww / 2 - ww * 0.4, 0.0, 2.2 if f < floors - 1 else 4.4, M, lift=0.3, nx=18, ny=10, mat=M['tiles'], wadang=False)
            z += fh + 1.4
        return z
    tower(-22, 36, 13, 4, 6.8); tower(26, 46, 11, 4, 6.4)
    # warm lamp-glow of the town behind the wall
    for (gx, gy, gr) in ((-30, 20, 28), (6, 22, 24), (40, 24, 24)): halo(gl, V((gx, gy, 14)), gr, M['halo_big'])


def foreground(Bk, M):
    """Nearest 15 % of the frame: dark grass tufts, a cart wheel leaning on its cart, rocks, a stake with a rope."""
    r = _rnd(5); w = Bk('fgwood', hull=T.hull(14.0)); st = Bk('fgstone', hull=T.hull(14.0)); gr = Bk('tufts')
    def wheel(c, R, yaw_deg, lean=0.0):
        F = Frame(c, yaw_deg); n = 20
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            p0, p1 = F.p(R * math.cos(a0), 0, R * math.sin(a0) + R), F.p(R * math.cos(a1), 0, R * math.sin(a1) + R)
            beam(w, p0, p1, 0.5, 0.7, M['wood_d'], up=(F.Y.x, F.Y.y, F.Y.z))
        for i in range(5): a = math.pi * i / 5; rod(w, F.p(R * math.cos(a), 0, R * math.sin(a) + R), F.p(-R * math.cos(a), 0, -R * math.sin(a) + R), 0.2, M['wood'], seg=6)
        rod(w, F.p(0, -0.6, R), F.p(0, 0.6, R), 0.5, M['wood_d'], seg=10); rod(w, F.p(0, -0.9, R), F.p(0, 0.9, R), 0.22, M['iron'], seg=8)
        for i in range(n): a = 2 * math.pi * (i + 0.5) / n; w.sphere(F.p(R * 1.0 * math.cos(a), 0.0, R * 1.0 * math.sin(a) + R), 0.09, M['iron'], seg=5, rings=3)
    wheel((-8.5, -41.5, 0.0), 1.7, 62.0); wheel((-4.0, -38.8, 0.0), 1.35, 18.0)
    obox(w, (-6.2, -40.2, 0.5), (0.94, 0.34, 0), (-0.34, 0.94, 0), (0, 0, 1), 2.6, 0.2, 0.2, M['wood'])                      # cart shaft on the ground
    for (x, y, s_, sd) in ((6.0, -41.5, 1.4, 3), (10.0, -43.5, 1.0, 5), (-15.5, -38.0, 1.1, 7), (12.5, -37.0, 0.7, 9), (2.5, -37.5, 0.5, 11), (-1.0, -44.0, 0.8, 13)):
        lumpy(st, V((x, y, s_ * 0.3)), s_, M['stone'] if sd % 2 else M['stone_d'], sd, seg=9, rings=6, rough=0.28, squash=0.62)
    for i in range(80):                                                                                        # grass tufts: crossed leaf cards (cones)
        x, y = r.uniform(-30, 30), r.uniform(-52, -31); h_ = r.uniform(0.8, 1.8)
        for k in range(3): a = r.uniform(0, 6.28); gr.frustum(V((x, y, 0)), V((x + 0.4 * math.cos(a), y + 0.4 * math.sin(a), h_)), 0.22, 0.0, M['leaf'] if k % 2 else M['grass2'], seg=3, cap1=False)
    # signal fire basket stake at the roadside + a fallen spear
    torch_post(Bk, M, (11.5, -33.0, 0.0), s=1.3, light=260.0, name='road_torch', halo_r=3.0)
    rod(w, V((-17, -37, 0.25)), V((-9.5, -35.0, 0.45)), 0.1, M['wood'], seg=5); w.frustum(V((-9.5, -35.0, 0.45)), V((-8.4, -34.8, 0.5)), 0.2, 0.0, M['steel'], seg=4)

