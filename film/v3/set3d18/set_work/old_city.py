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

