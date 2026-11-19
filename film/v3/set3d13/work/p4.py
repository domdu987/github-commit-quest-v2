
def _shop(mb, M, x0, x1, h, facname, y0=0.0, depth=22.0, zb=0.0, side_mat=None, cornice_mat=None):
    fac = M[facname]; sidem = side_mat or M['brick_b']; w = x1 - x0
    mb.box((x0, y0, zb - 1.0), (x1, y0 + depth, zb + h), sidem, mats=dict(front=fac, right=sidem, left=sidem), tile=(6, 6))
    cm = cornice_mat or M['cream']
    sbox(mb, (x0 - 0.3, y0 - 0.9, zb + h - 0.9), (x1 + 0.3, y0 + 0.3, zb + h), cm, 0.3); sbox(mb, (x0 - 0.5, y0 - 1.5, zb + h), (x1 + 0.5, y0 + 0.4, zb + h + 0.5), cm, 0.3)
    for k in range(int(w / 1.5)):
        xk = x0 + 0.4 + k * 1.5; sbox(mb, (xk, y0 - 1.0, zb + h - 0.9), (xk + 0.45, y0 - 0.2, zb + h - 0.3), cm, 0.3)
    sbox(mb, (x0, y0 + depth - 0.4, zb + h), (x1, y0 + depth, zb + h + 1.3), sidem, 1 / 6)

def _neighbours(SET, M, hotel=True):
    mb = MB(); am = MB()
    spec = [('L1', -52.0, -28.0, 21.0, 'fac_c', 1.3), ('L2', -72.0, -52.0, 14.0, 'fac_b', 0.0), ('L3', -90.0, -72.0, 12.5, 'fac_f', 0.0), ('L4', -110.0, -90.0, 17.0, 'fac_a', 0.0),
            ('R1', 20.0, 46.0, 17.0, 'fac_a', 0.5), ('R2', 46.0, 64.0, 15.0, 'fac_d', 0.5), ('R3', 64.0, 86.0, 18.0, 'fac_e', 0.5), ('R4', 86.0, 102.0, 12.5, 'fac_f', 0.5)]
    for (nm, x0, x1, h, fac, zb) in spec:
        side = M['clap_ochre'] if fac == 'fac_b' else (M['clap_teal'] if fac == 'fac_d' else (M['clap_green'] if fac == 'fac_f' else M['brick_b']))
        _shop(mb, M, x0, x1, h, fac, zb=zb, side_mat=side)
        nb = max(1, int((x1 - x0) // 8)); aw = [M['awn_rc'], M['awn_tc'], M['awn_oc']]
        for k in range(nb):
            cx = x0 + (k + 0.5) * (x1 - x0) / nb; _awning(am, cx, 0.0, zb + 4.3, (x1 - x0) / nb * 0.8, 2.0, 1.3, aw[(k + int(abs(x0))) % 3], M)
    for xx in np.arange(-51.0, -29.0, 3.4): sbox(mb, (xx, -0.2, -0.3), (xx + 1.1, 0.9, 0.0), M['timber_d'], 0.3)       # L1 already raised: timber blocks under it
    _obj(mb, 'shops', SET); _obj(am, 'shop_awnings', SET)
    cb = MB()
    for (xx, zz) in ((-58, 0.0), (-66, 0.0), (-80, 0.0), (26, 0.5), (36, 0.5), (50, 0.5), (70, 0.5), (92, 0.5), (-42, 1.3), (-34, 1.3)):
        _crate_stack(cb, (xx, -6.2, zz), M, int(xx) + 11, 3 + int(abs(xx)) % 3); _barrel(cb, (xx + 4.5, -5.2, zz), M, 'wood'); _barrel(cb, (xx + 5.8, -5.6, zz), M, 'wood_d')
    _obj(cb, 'shop_clutter', SET)

def _crate_stack(mb, c, M, seed, n=4):
    r = _rnd(seed); c = Vector(c)
    for k in range(n):
        s = r.uniform(1.0, 1.7); x = c.x + (k % 3) * 1.8 + r.uniform(-0.1, 0.1); y = c.y + r.uniform(-0.2, 0.2); z = c.z if k < 3 else c.z + 1.4
        if k >= 3: x = c.x + (k - 3) * 1.8 + 0.9
        sbox(mb, (x - s / 2, y - s / 2, z), (x + s / 2, y + s / 2, z + s), M['crate'], 0.3)
        for e in (-1, 1): sbox(mb, (x - s / 2 - 0.02, y + e * (s / 2 - 0.05) - 0.06, z + 0.1), (x + s / 2 + 0.02, y + e * (s / 2 - 0.05) + 0.06, z + 0.3), M['wood_d'], 0.3)

def _barrel(mb, c, M, mat='wood', r=0.55, h=1.4):
    c = Vector(c)
    mb.frustum(c, c + Vector((0, 0, h / 2)), r * 0.85, r, M[mat], seg=12, cap1=False); mb.frustum(c + Vector((0, 0, h / 2)), c + Vector((0, 0, h)), r, r * 0.85, M[mat], seg=12, cap0=False)
    mb.frustum(c + Vector((0, 0, h - 0.01)), c + Vector((0, 0, h)), r * 0.85, r * 0.85, M['wood_d'], seg=12, cap0=False)
    for zz in (0.2, h - 0.2): mb.frustum(c + Vector((0, 0, zz - 0.05)), c + Vector((0, 0, zz + 0.05)), r * 0.93, r * 0.93, M['iron'], seg=12, cap0=False, cap1=False)
    mb.frustum(c + Vector((0, 0, h / 2 - 0.05)), c + Vector((0, 0, h / 2 + 0.05)), r * 1.01, r * 1.01, M['iron'], seg=12, cap0=False, cap1=False)

def _sack(mb, c, M, seed=1, s=1.0):
    c = Vector(c); r = _rnd(seed); ell(mb, c + Vector((0, 0, 0.55 * s)), 0.5 * s, 0.38 * s, 0.6 * s, M['sack'], seg=8, rings=5, yaw=r.uniform(0, 3)); mb.frustum(c + Vector((0, 0, 1.05 * s)), c + Vector((0, 0, 1.25 * s)), 0.17 * s, 0.1 * s, M['sack'], seg=6)

def _gas_lamp(mb, fl, c, M, k):
    c = Vector(c); rod(mb, c, c + Vector((0, 0, 5.2)), 0.16, M['iron_d'], seg=6, r1=0.09); mb.frustum(c, c + Vector((0, 0, 0.9)), 0.34, 0.2, M['iron_d'], seg=8)
    rod(mb, c + Vector((0, 0, 3.2)), c + Vector((0.0, 0, 3.4)), 0.3, M['iron_d'], seg=6)
    fl.frustum(c + Vector((0, 0, 5.2)), c + Vector((0, 0, 6.0)), 0.26, 0.36, M['lamp_glass'], seg=6); mb.frustum(c + Vector((0, 0, 6.0)), c + Vector((0, 0, 6.5)), 0.5, 0.06, M['iron_d'], seg=6)
    f = c + Vector((0, 0, 5.6)); _halo(fl, f, 1.2, M)
    if STATE['P'].get('lamps', 0) >= 0.9: D._flame_light('gas_%d_%d' % (int(c.x), int(c.y)), tuple(f), LAMP, 260, radius=0.15)

def _pole(mb, x, y, M, h=15.0):
    rod(mb, (x, y, -0.2), (x, y, h), 0.32, M['wood_d'], seg=7, r1=0.2)
    sbox(mb, (x - 2.4, y - 0.18, h - 1.2), (x + 2.4, y + 0.18, h - 0.9), M['timber_d'], 0.3); sbox(mb, (x - 2.0, y - 0.18, h - 3.0), (x + 2.0, y + 0.18, h - 2.7), M['timber_d'], 0.3)
    for xo in (-2.2, -0.9, 0.9, 2.2):
        for hh in (h - 0.9, h - 2.7): rod(mb, (x + xo, y, hh), (x + xo, y, hh + 0.45), 0.09, M['teal'], seg=5)

def _wheel(mb, c, r, M, yaw=0.0):
    c = Vector(c); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); n = 16
    for i in range(n):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; p0 = c + ey * math.cos(a0) * r + Z * math.sin(a0) * r; p1 = c + ey * math.cos(a1) * r + Z * math.sin(a1) * r
        beam(mb, p0, p1, 0.26, 0.45, M['wood'], up=tuple(ex)); beam(mb, p0, p1, 0.06, 0.5, M['iron_d'], up=tuple(ex))
    for i in range(12):
        a = 2 * math.pi * i / 12; rod(mb, c, c + ey * math.cos(a) * r + Z * math.sin(a) * r, 0.07, M['wood_l'], seg=4)
    rod(mb, c - ex * 0.35, c + ex * 0.35, 0.22, M['wood_d'], seg=8)

def _horse(mb, base, yaw, M, mat='horse', seed=1):
    """draught horse, smoother: overlapping ellipsoids (10 x 7 faces) for chest, barrel, rump, neck, head; jointed legs; mane, tail, collar and straps. +x forward."""
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    R = Matrix((ex, ey, Z)).transposed(); P = lambda x, y, z: b + ex * x + ey * y + Z * z
    mt = M[mat]; md = M['horse_d'] if mat != 'horse_d' else M['wood_d']; Ry = lambda a: R @ Matrix.Rotation(a, 3, 'Y')
    ell(mb, P(0.0, 0, 3.35), 1.75, 0.86, 0.96, mt, seg=14, rings=9, rot=R); ell(mb, P(1.05, 0, 3.4), 0.95, 0.8, 0.98, mt, seg=12, rings=8, rot=R); ell(mb, P(-1.15, 0, 3.5), 1.0, 0.82, 0.94, mt, seg=12, rings=8, rot=R)
    ell(mb, P(1.95, 0, 4.2), 1.05, 0.4, 0.46, mt, seg=12, rings=7, rot=Ry(-0.8)); ell(mb, P(2.5, 0, 4.85), 0.55, 0.36, 0.5, mt, seg=10, rings=6, rot=Ry(-0.6))
    ell(mb, P(3.05, 0, 5.3), 0.72, 0.3, 0.3, mt, seg=12, rings=7, rot=Ry(0.7)); ell(mb, P(3.55, 0, 4.98), 0.32, 0.23, 0.22, md, seg=8, rings=5, rot=Ry(0.7))
    for sg in (-1, 1):
        mb.frustum(P(2.75, sg * 0.2, 5.5), P(2.68, sg * 0.24, 6.0), 0.1, 0.02, md, seg=4); ell(mb, P(3.1, sg * 0.22, 5.42), 0.06, 0.04, 0.05, M['dark'], seg=5, rings=3)
    for k in range(6): ell(mb, P(1.5 + 0.22 * k, 0, 4.0 + 0.2 * k + (0.2 if k > 3 else 0)), 0.2, 0.1, 0.22, md, seg=6, rings=4, rot=Ry(-0.8))
    for (lx, ly, hind) in ((1.45, 0.45, 0), (1.45, -0.45, 0), (-1.45, 0.45, 1), (-1.45, -0.45, 1)):
        top = P(lx, ly, 3.05); knee = P(lx + (0.15 if not hind else -0.25), ly, 1.7); fet = P(lx + (0.05 if not hind else 0.1), ly, 0.5)
        mb.frustum(top, knee, 0.34, 0.2, mt, seg=8); ell(mb, knee, 0.2, 0.19, 0.2, mt, seg=6, rings=4); mb.frustum(knee, fet, 0.17, 0.15, mt, seg=8)
        mb.frustum(fet, fet - Z * 0.5, 0.2, 0.25, md, seg=8)
    mb.frustum(P(-2.0, 0, 4.1), P(-2.5, 0, 2.2), 0.22, 0.06, md, seg=6)
    ring = P(1.6, 0, 3.55); mb.frustum(ring - ex * 0.1, ring + ex * 0.1, 1.0, 1.0, M['wood_d'], seg=12, cap0=False, cap1=False)            # collar
    mb.frustum(P(0.0, 0, 3.35) - Z * 0.0, P(0.1, 0, 3.35), 0.99, 0.99, M['wood_d'], seg=12, cap0=False, cap1=False) if False else None
    for sg in (-1, 1): beam(mb, P(1.5, sg * 0.9, 3.5), P(-0.9, sg * 0.88, 3.0), 0.09, 0.05, M['wood_d'])                                   # traces

def _cart(mb, wm, base, yaw, M, sink=0.6, load='barrels', horse=True, seed=3, hmat='horse'):
    b = Vector(base); ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1))
    P = lambda x, y, z: b + ex * x + ey * y + Z * z; zb = 2.4 - sink
    obox(mb, P(0, 0, zb), ex, ey, Z, 3.6, 1.7, 0.18, M['wood'], 0.3)
    for sg in (-1, 1): obox(mb, P(0, sg * 1.7, zb + 0.55), ex, ey, Z, 3.6, 0.1, 0.5, M['wood_l'], 0.3)
    obox(mb, P(-3.6, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3); obox(mb, P(3.5, 0, zb + 0.55), ex, ey, Z, 0.1, 1.7, 0.5, M['wood_l'], 0.3)
    for sx in (-2.3, 2.3):
        for sg in (-1, 1): _wheel(wm, P(sx, sg * 2.0, 1.5 - sink), 1.9, M, yaw=yaw)
        rod(mb, P(sx, -2.0, 1.5 - sink), P(sx, 2.0, 1.5 - sink), 0.16, M['iron_d'], seg=6)
    if load == 'barrels':
        for (lx, ly, lz) in ((-2.4, -0.7, 0), (-1.0, -0.7, 0), (0.4, -0.7, 0), (1.8, -0.7, 0), (-2.4, 0.8, 0), (-1.0, 0.8, 0), (0.4, 0.8, 0), (1.8, 0.8, 0), (-1.7, 0.0, 1.4), (0.1, 0.0, 1.4), (1.2, 0.1, 1.4)):
            _barrel(mb, P(lx, ly, zb + 0.18 + lz), M, 'wood' if (lx + ly) % 2 < 1 else 'wood_l', r=0.62, h=1.5)
    else:
        for (lx, ly, lz, s) in ((-2.2, -0.6, 0, 1.5), (-0.4, 0.5, 0, 1.6), (1.4, -0.5, 0, 1.4), (-1.2, 0.0, 1.5, 1.3), (0.6, -0.2, 1.6, 1.2)): obox(mb, P(lx, ly, zb + 0.18 + lz + s / 2), ex, ey, Z, s / 2, s / 2, s / 2, M['crate'], 0.3)
    for sg in (-1, 1): beam(mb, P(3.5, sg * 0.9, zb - 0.1), P(8.2, sg * 0.9, zb + 0.9), 0.16, 0.22, M['wood_d'])
    if horse: _horse(mb, P(8.2, 0, 0.0), yaw, M, hmat, seed=seed)

def _mound(SET, M, name, cx, cy, rx, ry, h, seed, mat, mud_z):
    xs = np.linspace(cx - rx, cx + rx, 30); ys = np.linspace(cy - ry, cy + ry, 30); X, Y = np.meshgrid(xs, ys)
    d = np.sqrt(((X - cx) / rx) ** 2 + ((Y - cy) / ry) ** 2); n = 0.07 * np.sin(2.3 * X + seed) * np.cos(1.9 * Y) + 0.05 * np.sin(5.0 * X - 3.1 * Y + seed)
    Z = h * np.clip(1 - d ** 1.7, 0, 1) ** 0.9 * (1 + n) - 0.35 + n * 0.3
    ob = grid_mesh(name, xs, ys, Z, mat, uvs=(0.2, 0.2)); STATE['fill_objs'].append(ob); return ob

def _wheelbarrow(mb, x, y, z, yaw, M):
    ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); P = lambda a, b, c: Vector((x, y, z)) + ex * a + ey * b + Z * c
    obox(mb, P(0.0, 0, 1.0), ex, ey, Z, 0.9, 0.55, 0.28, M['wood'], 0.3)
    for sg in (-1, 1): beam(mb, P(0.8, sg * 0.45, 0.9), P(2.4, sg * 0.4, 0.9), 0.1, 0.12, M['wood_d']); beam(mb, P(-0.8, sg * 0.45, 0.9), P(-0.8, sg * 0.5, 0.0), 0.08, 0.1, M['wood_d'])
    rod(mb, P(1.5, -0.55, 0.55), P(1.5, 0.55, 0.55), 0.4, M['wood_d'], seg=10, r1=0.4)

def _ladder(mb, p0, p1, M, w=0.7):
    p0, p1 = Vector(p0), Vector(p1); d = (p1 - p0); side = Vector((0, 1, 0)) if abs(d.y) < abs(d.x) else Vector((1, 0, 0))
    for sg in (-1, 1): beam(mb, p0 + side * sg * w / 2, p1 + side * sg * w / 2, 0.1, 0.14, M['wood_d'])
    for k in range(1, 9): a = p0.lerp(p1, k / 9); beam(mb, a - side * w / 2, a + side * w / 2, 0.08, 0.1, M['wood_l'])

def _street_dress(SET, M, mud_z, hotel=True):
    mb = MB(); fl = MB(); zq = lambda x, y: float(mud_z(np.array([x]), np.array([y]))[0])
    for k, xx in enumerate((-96, -66, -40, 28, 56, 84)): _gas_lamp(mb, fl, (xx, -8.2 if xx < 0 else -7.7, 1.3 if xx < 0 else 0.5), M, k)
    for xx in (-9.0, 9.0): _gas_lamp(mb, fl, (xx + (-7.0 if xx < 0 else 7.0), -9.6, 0.0), M, 9)
    poles = [(x, -13.0) for x in (-112, -74, -36, 2, 40, 78, 116)]
    for (x, y) in poles: _pole(mb, x, y, M)
    for (a, b) in zip(poles, poles[1:]):
        for dx, dz in ((-2.2, 14.1), (-0.9, 14.1), (0.9, 14.1), (2.2, 14.1), (-2.0, 12.3), (2.0, 12.3)):
            chain_rod(mb, catenary((a[0] + dx, a[1], dz), (b[0] + dx, b[1], dz), 0.9, 8), 0.05, M['iron_d'], seg=3)
    for xx in (-60, -30, 30, 60): rod(mb, (xx, -9.4, 0.0), (xx, -9.4, 2.4), 0.16, M['wood_d'], seg=5); sbox(mb, (xx - 0.7, -9.5, 2.0), (xx + 0.7, -9.3, 2.2), M['wood_d'], 0.3)
    _obj(mb, 'street_furniture', SET); _obj(fl, 'lamps_glass', SET, shadow=False)
    cm = MB(); wm = MB()
    _cart(cm, wm, (-24.0, -35.0, 0.0), math.radians(8), M, sink=0.6, load='barrels', seed=3)                          # the stuck cart (mud_low, street_wide)
    _cart(cm, wm, (17.0, -26.0, 0.0), math.radians(190), M, sink=0.45, load='crates', seed=4, hmat='horse_g')
    _cart(cm, wm, (-46.0, -42.0, 0.0), math.radians(60), M, sink=0.4, load='crates', seed=5, hmat='horse_d')
    _obj(cm, 'carts', SET); _obj(wm, 'cart_wheels', SET); STATE['fill_objs'] += [bpy.data.objects['carts'], bpy.data.objects['cart_wheels']]
    _mound(SET, M, 'pile_a', -34.0, -17.0, 8.0, 4.4, 3.2, 4, M['clay'], mud_z); _mound(SET, M, 'pile_b', 40.0, -14.0, 7.0, 3.8, 2.6, 5, M['clay'], mud_z)
    _mound(SET, M, 'pile_c', 12.0, -38.0, 5.0, 3.2, 1.9, 6, M['gravel'], mud_z); _mound(SET, M, 'pile_e', -8.0, -46.0, 5.0, 3.0, 2.2, 8, M['clay'], mud_z)
    _mound(SET, M, 'pile_d', -50.0, -22.0, 6.0, 3.4, 2.2, 7, M['clay'], mud_z)
    pm = MB()
    for k in range(5): sbox(pm, (-12.0, -15.4 + k * 0.45, 0.0), (-4.0, -15.0 + k * 0.45, 0.35), M['walk'], 0.3)
    for k in range(5): sbox(pm, (24.0, -17.4 + k * 0.45, 0.1), (31.0, -17.0 + k * 0.45, 0.45), M['walk'], 0.3)
    for lvl in range(4):
        for j in range(5 - lvl): sbox(pm, (-62.0 + lvl * 0.5, -22.0 + j * 0.6 + lvl * 0.3, 0.45 * lvl - 0.1), (-54.0 - lvl * 0.5, -21.5 + j * 0.6 + lvl * 0.3, 0.45 * lvl + 0.35), M['timber_w'], 0.3)
    def walk(p0, p1, wdt=3.0):                                                                           # plank walkway across the mud with two stringers
        p0, p1 = Vector(p0), Vector(p1); dv = (p1 - p0).normalized(); pr = Vector((-dv.y, dv.x)); n_ = int((p1 - p0).length / 0.7)
        for k in range(n_):
            c2 = p0 + dv * (k * 0.7); zz = zq(c2.x, c2.y) + 0.12; beam(pm, (c2.x - pr.x * wdt / 2, c2.y - pr.y * wdt / 2, zz), (c2.x + pr.x * wdt / 2, c2.y + pr.y * wdt / 2, zz), 0.58, 0.16, M['walk'], uvk=0.3)
        for sg in (-1, 1): beam(pm, (p0.x + pr.x * (wdt / 2 - 0.2) * sg, p0.y + pr.y * (wdt / 2 - 0.2) * sg, 0.0), (p1.x + pr.x * (wdt / 2 - 0.2) * sg, p1.y + pr.y * (wdt / 2 - 0.2) * sg, 0.0), 0.2, 0.2, M['timber_d'], uvk=0.3)
    walk((-20.0, -50.0), (-8.0, -34.0)); walk((-12.0, -22.0), (0.0, -11.0), 2.6); walk((8.0, -12.0), (8.0, -45.0), 2.4)
    _obj(pm, 'street_planks', SET); STATE['fill_objs'].append(bpy.data.objects['street_planks'])
    bm = MB()
    for (xx, yy) in ((-26, -11.5), (-24.6, -11.0), (-25.4, -12.7), (16, -11.0), (17.4, -11.8), (-2, -44), (-0.6, -44.8), (48, -28), (49.4, -27.4), (-56, -30), (-57.2, -29.4), (-5.0, -20.0),
                     (-22.0, -40.0), (-20.6, -40.8), (-21.6, -41.9), (-13.0, -44.0), (-11.8, -44.5), (-30.0, -45.0), (4.0, -43.0), (5.3, -43.6), (-34.0, -29.0), (36.0, -30.0), (14.0, -18.0)):
        _barrel(bm, (xx, yy, zq(xx, yy) - 0.15), M, 'wood' if int(xx) % 2 else 'wood_l')
    for (xx, yy, s_) in ((-5.0, -42.0, 12), (22.0, -11.0, 8), (-31.0, -12.0, 9), (52.0, -36.0, 10), (-40.0, -41.0, 13), (28.0, -43.0, 14)): _crate_stack(bm, (xx, yy, zq(xx, yy) - 0.1), M, s_, 5)
    for k, (xx, yy) in enumerate(((-18.0, -22.0), (-16.5, -22.6), (-17.4, -21.0), (-3.0, -26.0), (-1.8, -26.6), (22.0, -30.0), (-44.0, -27.0), (30.0, -18.5))): _sack(bm, (xx, yy, zq(xx, yy) - 0.1), M, k, 1.1)
    for (xx, yy) in ((-28.0, -19.5), (36.0, -17.0), (2.0, -31.0)): _wheelbarrow(bm, xx, yy, zq(xx, yy) - 0.1, 0.7 * xx, M)
    _ladder(bm, (-33.0, -4.0, 0.5), (-33.5, -8.5, 6.0), M); _ladder(bm, (9.0, -12.0, 0.0), (11.0, -14.0, 5.5), M) if False else None
    for xx in (-44.0, -30.0, 28.0, 44.0):                                                                  # stakes with a rope round the fill piles
        for k in range(4): rod(bm, (xx + k * 2.2, -23.0, zq(xx + k * 2.2, -23.0) - 0.2), (xx + k * 2.2, -23.0, zq(xx + k * 2.2, -23.0) + 1.4), 0.1, M['wood_d'], seg=5)
    for k in range(5): bm_h = _rnd(k); _bale = (-16.0 + 2.2 * k, -20.5 + 0.3 * (k % 2)); sbox(bm, (_bale[0] - 0.9, _bale[1] - 0.5, zq(*_bale) - 0.1), (_bale[0] + 0.9, _bale[1] + 0.5, zq(*_bale) + 0.8), M['hay'], 0.4) if k < 3 else None
    _obj(bm, 'street_props', SET); STATE['fill_objs'].append(bpy.data.objects['street_props'])
    STATE['marks'].update(
        door=(0.0, -0.9, GF, 1), stair_top=(0.0, -3.0, GF - 0.1, 0), stair_mid=(0.0, -6.5, GF * 0.5, 0), stair_foot=(0.0, -9.6, 0.0, 0), mud_fall=(2.0, -6.4, 0.0, 0), door_b=(-3.5, -0.9, GF, 1),
        walk_a=(-14.0, -41.0, 0.0, 0), walk_b=(-8.0, -35.0, 0.0, 0), walk_c=(8.0, -20.0, 0.0, 0), cart_a=(-21.0, -29.5, 0.0, 0), cart_b=(-27.5, -31.5, 0.0, 0), cart_c=(-14.5, -31.0, 0.0, 0),
        front_a=(-9.0, -13.0, 0.0, 0), front_b=(9.0, -13.5, 0.0, 0), front_c=(-1.5, -17.0, 0.0, 0), pile_a=(-30.0, -20.5, 0.0, 0), pile_b=(5.0, -40.0, 0.0, 0), sidewalk_r=(24.0, -5.6, 0.5, 0), sidewalk_l=(-36.0, -5.6, 1.3, 0))

def _church(SET, M):
    mb = MB(); x, y = 105.0, 210.0
    sbox(mb, (x - 7, y - 7, -0.5), (x + 7, y + 7, 34.0), M['stone_grey'], 0.15)
    for sx in (-1, 1): sbox(mb, (x + sx * 2.8 - 1.0, y - 7.1, 24.0), (x + sx * 2.8 + 1.0, y - 6.8, 31.0), M['dark'], 0.3)
    sbox(mb, (x - 7.6, y - 7.6, 33.5), (x + 7.6, y + 7.6, 34.6), M['cream'], 0.3)
    mb.frustum((x, y, 34.6), (x, y, 66.0), 5.8, 0.25, M['slate'], seg=8); rod(mb, (x, y, 66.0), (x, y, 72.0), 0.12, M['brass'], seg=4); sbox(mb, (x - 1.0, y - 0.06, 69.5), (x + 1.0, y + 0.06, 70.2), M['brass'], 0.3)
    sbox(mb, (x - 17, y - 7, -0.5), (x - 7, y + 20, 20.0), M['brick_d'], 0.15); prism_roof(mb, x - 17.2, x - 6.8, y - 7.3, y + 20.3, 20.0, 7.0, M['slate'])
    _obj(mb, 'church', SET)

def _opposite(SET, M):
    """the row of shops across the street (y -68..-52, facing +y), seen from the suite window."""
    mb = MB()
    spec = [(-70, -46, 24.0, 'fac_a'), (-46, -26, 20.0, 'fac_b'), (-26, -2, 28.0, 'fac_c'), (-2, 18, 22.0, 'fac_d'), (18, 44, 25.0, 'fac_e'), (44, 66, 19.0, 'fac_f'), (66, 90, 26.0, 'fac_a')]
    for (x0, x1, h, fac) in spec:
        mb.box((x0, -68.0, -1.0), (x1, -52.0, h), M['brick_b'], mats=dict(back=M[fac]), tile=(6, 6))
        sbox(mb, (x0 - 0.3, -52.3, h - 0.9), (x1 + 0.3, -50.9, h), M['cream'], 0.3); sbox(mb, (x0, -68.0, h), (x1, -51.8, h + 0.5), M['cream'], 0.3); sbox(mb, (x0 + 3.0, -64.0, h + 0.5), (x0 + 4.6, -62.4, h + 4.0), M['brick_d'], 1 / 6)
    sb = MB(); sbox(sb, (-110, -52.0, 0.0), (110, -47.0, 0.45), M['walk'], 0.2); _obj(sb, 'opp_walk', SET); _obj(mb, 'opp_shops', SET)
