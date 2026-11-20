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

