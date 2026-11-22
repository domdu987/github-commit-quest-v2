def moat_bridge_road(Bk, M):
    wt = Bk('water', shadow=False); wz = WATER_Z; x0, x1 = -200.0, 200.0; y0, y1 = MOAT
    flat(wt, V((x0, y0, wz)), V((x1 - x0, 0, 0)), V((0, y1 - y0, 0)), M['water'], (0, 0, (x1 - x0) / 16, (y1 - y0) / 16))
    bk = Bk('banks')
    # sloped banks: outer (toward the camera) y -22 -> -19.5 down to the water, inner y -9.5 -> -7.2 up to the berm
    flat(bk, V((x0, y1 - 0.0, wz)), V((x1 - x0, 0, 0)), V((0, 2.3, 2.2)), M['bank'], (0, 0, 40, 0.6))
    flat(bk, V((x0, y0, 0.0)), V((x1 - x0, 0, 0)), V((0, 2.5, wz)), M['bank'], (0, 0, 40, 0.6))
    pass
    # approach: packed-earth road from the bridge toward the camera
    rd = Bk('road'); flat(rd, V((-5.5, y0 - 0.0, 0.03)), V((11.0, 0, 0)), V((0, -160.0, 0)), M['road'], (0, 0, 11 / 8, 20))
    rd.face([V((-5.5, y1 + 2.3, 0.03)), V((-5.5, yo(0), 0.03)), V((5.5, yo(0), 0.03)), V((5.5, y1 + 2.3, 0.03))][::-1], M['road'], [(0, 0), (0, 1), (1, 1), (1, 0)][::-1])
    # timber bridge: deck, beams, posts, rails, piles
    br = Bk('bridge', hull=T.hull(60.0)); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
    yb0, yb1 = y0 - 0.5, y1 + 2.3
    obox(br, (0, (yb0 + yb1) / 2, 0.12), X, Y, Z, 4.2, (yb1 - yb0) / 2, 0.14, M['planks'], uvk=0.5)
    for sx in (-3.8, -1.3, 1.3, 3.8): obox(br, (sx, (yb0 + yb1) / 2, -0.45), X, Y, Z, 0.28, (yb1 - yb0) / 2, 0.38, M['wood_d'], uvk=0.5)
    for yy in np.linspace(yb0 + 1.5, yb1 - 1.5, 4):
        for sx in (-3.8, 3.8): rod(br, (sx, yy, WATER_Z - 0.5), (sx, yy, 0.0), 0.34, M['wood_d'], seg=7)
        obox(br, (0, yy, -0.2), X, Y, Z, 4.2, 0.22, 0.2, M['wood_d'])
    for sx in (-4.1, 4.1):
        for yy in np.linspace(yb0 + 0.4, yb1 - 0.4, 6):
            rod(br, (sx, yy, 0.2), (sx, yy, 2.2), 0.2, M['red'], seg=7)
        obox(br, (sx, (yb0 + yb1) / 2, 1.9), X, Y, Z, 0.14, (yb1 - yb0) / 2, 0.16, M['red']); obox(br, (sx, (yb0 + yb1) / 2, 1.0), X, Y, Z, 0.1, (yb1 - yb0) / 2, 0.1, M['wood'])
    for yy in (yb1 - 0.4, yb1 - 6.0):
        for sx in (-4.1, 4.1): oil_lamp(Bk, M, (sx, yy, 0.25), s=0.85, light=(110.0 if yy > yb1 - 1 else 0.0), name='bl%d%d' % (int(sx), int(yy)), halo_r=1.6, h=3.0)
    # reflections: a layered streak of every wall torch / tower lantern on the water + the moon's reflection
    st = Bk('streaks', shadow=False); wz2 = wz + 0.03
    for xt in STATE['marks'].get('wall_torch_x', []):
        cam = V(CAMS['wall']['loc']); xs = xt + (xt - cam.x) * (-0.18)                                           # shifts away from the camera axis a little (perspective of a vertical)
        wd_ = 1.2; L = 19.0
        st.face([V((xs - wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 - L, wz2)), V((xs - wd_, y1 - L, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    for xl in (-9.8, -4.2, 4.2, 9.8): st.face([V((xl - 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 - 16, wz2)), V((xl - 1.0, y1 - 16, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    mx_ = CAMS['wall']['loc'][0] + math.tan(math.radians(JX.MOON_AZ - 90)) * -(0) + (-0.176) * (y1 - 6 - CAMS['wall']['loc'][1]) * 0.9
    for k, (dx, ww, L) in enumerate(((0.0, 1.7, 12.4), (-2.0, 0.9, 9.0), (2.2, 0.8, 8.0))):
        st.face([V((mx_ + dx - ww, y1 - 0.2, wz2 + 0.01 * k)), V((mx_ + dx + ww, y1 - 0.2, wz2 + 0.01 * k)), V((mx_ + dx + ww, y1 - L, wz2 + 0.01 * k)), V((mx_ + dx - ww, y1 - L, wz2 + 0.01 * k))], M['streak_m'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    # mist over the moat
    for k in range(6): halo(Bk('halos', shadow=False), V((-60 + k * 24, -16, 0.5)), 16.0, M['mist'])

