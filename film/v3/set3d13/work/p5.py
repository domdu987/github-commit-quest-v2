
# ============================================================================= cellar (crawlspace under the hotel)
CX0, CX1, CY0, CY1 = -9.0, 19.0, -4.0, 68.0
CZ_B = 3.5      # underside of the cross beams = top of the jack pads (at lift 0)
UX = [-6.0 + 2.6 * k for k in range(10)]; UY = [6.0 + 2.7 * k for k in range(23)]       # jack grid: 230 jacks
VENTS = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0]
def _under(SET, P, M):
    _sky(SET, P, M, 1100.0); _far_ground(SET, M); r = _rnd(11)
    xs_g = np.unique(np.round(np.concatenate([np.arange(-70, -12, 4.0), np.arange(-12, 24, 0.6), np.arange(24, 71, 4.0)]), 3)); ys_g = np.unique(np.round(np.concatenate([np.arange(-30, -8, 4.0), np.arange(-8, 72, 0.6), np.arange(72, 101, 4.0)]), 3))
    X, Y = np.meshgrid(xs_g, ys_g); Z = 0.12 * np.sin(0.7 * X + 0.3 * Y) * np.cos(0.5 * Y) + 0.07 * np.sin(2.1 * X + 1.0 * Y) + 0.05 * np.sin(4.3 * X - 2.0 * Y)
    inside = (X > CX0) & (X < CX1) & (Y > CY0 + 1) & (Y < CY1)
    for (cx, cy, rr, h) in ((-6.0, 12.0, 1.8, 0.5), (14.0, 26.0, 2.0, 0.45), (2.0, 45.0, 2.5, 0.55), (15.5, 55.0, 1.6, 0.4)): Z = Z + h * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / rr ** 2)    # earth lumps
    grid_mesh('floor', xs_g, ys_g, Z, M['dirt'], uvs=(0.1, 0.1))
    fb = MB()                                                                                       # a worn plank walkway down the middle aisle
    for k in range(3): sbox(fb, (0.6 + k * 1.2, CY0, 0.02), (1.6 + k * 1.2, CY1 - 3, 0.1), M['plank_f'], 0.2)
    for yy in np.arange(0.0, CY1 - 3, 4.1): sbox(fb, (0.4, yy, 0.02), (4.4, yy + 0.3, 0.18), M['timber_d'], 0.3)
    _obj(fb, 'walkway', SET)
    wb = MB(); zt = CZ_B + 2.6
    sbox(wb, (CX0 - 1.0, CY0, -0.6), (CX0, CY1 + 1.0, zt), M['brick_d'], 1 / 6); sbox(wb, (CX0, CY1, -0.6), (CX1 + 1.2, CY1 + 1.0, zt), M['brick_d'], 1 / 6)
    ys_v = [CY0] + [v for yv in VENTS for v in (yv - 0.9, yv + 0.9)] + [CY1]                              # right wall with 6 ventilation slots (z 0.9..4.0)
    for i in range(0, len(ys_v), 2):
        sbox(wb, (CX1, ys_v[i], -0.6), (CX1 + 1.2, ys_v[i + 1], zt), M['brick_d'], 1 / 6)
    for yv in VENTS: sbox(wb, (CX1, yv - 0.9, -0.6), (CX1 + 1.2, yv + 0.9, 0.7), M['brick_d'], 1 / 6); sbox(wb, (CX1, yv - 0.9, 3.0), (CX1 + 1.2, yv + 0.9, zt), M['brick_d'], 1 / 6)
    for yy in np.arange(CY0 + 2.0, CY1, 8.0): sbox(wb, (CX0, yy, 0.0), (CX0 + 0.3, yy + 0.5, 4.8), M['timber_d'], 0.3)           # pilasters on the left wall
    _obj(wb, 'cellar_walls', SET)
    pb = MB()                                                                                       # front: timber posts + cribs at the open front (y -4)
    for xx in (CX0 + 0.5, 1.0, 6.5, 12.0, CX1 - 0.5): sbox(pb, (xx - 0.5, CY0 - 0.5, -0.1), (xx + 0.5, CY0 + 0.5, CZ_B + 0.2), M['timber_d'], 0.3)
    _obj(pb, 'front_posts', SET)
    bm = MB(); kd = Vector(P['key_dir'])
    for y in UY:
        sbox(bm, (CX0, y - 0.5, 0.0), (CX1 + 1.0, y + 0.5, 1.2), M['timber_w'], 0.25)                      # heavy cross beams (rel z 0 = underside)
        sbox(bm, (CX0, y - 0.58, 0.8), (CX0 + 0.8, y + 0.58, 1.4), M['iron_k'], 0.3)
    for xj in np.arange(CX0, CX1 + 1.5, 2.0): sbox(bm, (xj - 0.28, CY0, 1.2), (xj + 0.28, CY1, 2.1), M['timber'], 0.25)
    sbox(bm, (CX0, CY0, 2.1), (CX1 + 1.0, CY1, 2.3), M['plank_d'], 0.2)
    bo = _obj(bm, 'floor_beams', SET); STATE['movers'].append((bo, CZ_B)); STATE['cut_objs'].append(bo)
    so, mo, nj = _jackfield(SET, M, UX, UY, 'jf', 0.0, 1, 3.3, CZ_B, hd=1.0); STATE['njacks'] = nj
    pr = MB()
    for (xx, yy) in ((-7.0, 3.0), (-7.5, 20.0), (17.0, 14.0), (16.0, 36.0), (-7.0, 52.0), (16.5, 62.0)): _crate_stack(pr, (xx, yy, 0.0), M, int(yy), 4)
    for (xx, yy) in ((-7.0, 8.0), (3.0, 4.5), (15.5, 25.0), (-7.2, 33.0), (17.0, 46.0), (-7.0, 60.0)): _barrel(pr, (xx, yy, 0.0), M, 'wood')
    for (xx, yy) in ((-7.4, 14.0), (17.5, 30.0), (3.0, 3.0)): rod(pr, (xx, yy, 0.0), (xx, yy, 0.8), 0.4, M['iron'], seg=8, r1=0.5)
    for yy in (9.4, 20.2, 31.0, 42.0):                                                                 # long turning bars leaning on the beams
        rod(pr, (3.2, yy, 0.0), (4.0, yy + 0.3, 3.3), 0.08, M['iron_bar'], seg=4)
    for k, (xx, yy) in enumerate(((2.2, 6.0), (3.0, 16.0), (4.5, 27.0), (2.6, 38.0))): _sack(pr, (xx, yy, 0.0), M, k, 1.0)
    _obj(pr, 'cellar_props', SET)
    lamps = [(1.5, 9.0, 2.6), (9.0, 17.0, 2.6), (3.0, 26.0, 2.6), (10.0, 34.0, 2.6), (2.0, 44.0, 2.6), (9.0, 54.0, 2.6), (4.0, 63.0, 2.6)]
    fl = MB()
    for k, (xl, yl, zl) in enumerate(lamps):
        c = Vector((xl, yl, zl)); rod(fl, c + Vector((0, 0, 0.5)), c + Vector((0, 0, CZ_B + 0.0 - zl)), 0.03, M['iron_d'], seg=4)
        fl.frustum(c - Vector((0, 0, 0.5)), c + Vector((0, 0, 0.5)), 0.26, 0.34, M['lamp_glass'], seg=7); fl.frustum(c + Vector((0, 0, 0.5)), c + Vector((0, 0, 0.8)), 0.38, 0.05, M['iron_d'], seg=7)
        _halo(fl, c, 2.4, M); D._flame_light('oil_%d' % k, tuple(c), LAMP, 1500 if k < 5 else 900, radius=0.15, shadow=(k % 2 == 0))
        pool = MB(); pool.face([Vector((xl - 5.5, yl - 5.5, 0.12)), Vector((xl + 5.5, yl - 5.5, 0.12)), Vector((xl + 5.5, yl + 5.5, 0.12)), Vector((xl - 5.5, yl + 5.5, 0.12))], M['pool'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        _obj(pool, 'pool_%d' % k, SET, shadow=False)
    _obj(fl, 'cellar_lamps', SET, shadow=False)
    sh = MB(); kn = kd.normalized()                                                                 # dusty shafts of light through the vents (additive cards along the key direction)
    for yv in VENTS:
        for sg in (-1, 1):
            a = Vector((CX1, yv + sg * 0.9, 3.0)); b = Vector((CX1, yv + sg * 0.9, 0.7)); ta = a.z / max(0.05, -kn.z); tb = b.z / max(0.05, -kn.z)
            sh.face([a, b, b + kn * tb, a + kn * ta], M['shaft'], [(0, 1), (0, 0), (1, 0), (1, 1)])
    _obj(sh, 'shafts', SET, shadow=False)
    # stand points: aisles between the jack columns (x = column + 1.3), between beam rows
    for k in range(4):
        for j, yy in enumerate((9.35, 17.45, 28.25, 41.75)): STATE['marks']['aisle_%d_%d' % (k, j)] = (UX[2 * k + 1] + 1.3 if 2 * k + 1 < len(UX) else UX[-1] + 1.3, yy, 0.0, 0)
    STATE['marks'].update(foreman=(0.0, 7.4, 0.0, 0), worker_a=(3.6, 12.0, 0.0, 0), worker_b=(9.4, 19.0, 0.0, 0), worker_c=(1.0, 24.4, 0.0, 0), worker_d=(6.2, 30.0, 0.0, 0), jack_hands=(7.0, 15.3, 0.0, 0))

# ============================================================================= suite (rich guest's top-floor room, window looks down on the muddy street)
RX0, RX1, RY1 = -11.0, 11.0, 18.0
ZF = 30.0; RH = 6.2
TEA = dict(x=-1.4, y=2.5, top=ZF + 1.5)
def _cup(mb, tea_mb, cx, cy, z0, s):
    """a proper teacup on a saucer (lathe profiles, 20 segments): saucer dish, foot, bowl with an inner wall, rim, a looped handle; the tea disc is a separate flat mesh just under the rim."""
    seg = 20
    prof = [(0.0, 0.0), (0.2, 0.0), (0.36, 0.035), (0.58, 0.13), (0.62, 0.15)]                              # saucer outer (r, z) * s
    def lathe(pts, mat, flip=False):
        for (r0, h0), (r1, h1) in zip(pts, pts[1:]):
            for i in range(seg):
                a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
                q = [Vector((cx + r0 * s * math.cos(a0), cy + r0 * s * math.sin(a0), z0 + h0 * s)), Vector((cx + r0 * s * math.cos(a1), cy + r0 * s * math.sin(a1), z0 + h0 * s)),
                     Vector((cx + r1 * s * math.cos(a1), cy + r1 * s * math.sin(a1), z0 + h1 * s)), Vector((cx + r1 * s * math.cos(a0), cy + r1 * s * math.sin(a0), z0 + h1 * s))]
                mb.face(q[::-1] if flip else q, mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
    mb.pid += 1
    lathe(prof, STATE['M']['white']); lathe([(0.62, 0.15), (0.6, 0.165), (0.5, 0.11), (0.3, 0.07), (0.0, 0.07)], STATE['M']['white'])    # saucer rim and dish
    cp = [(0.2, 0.07), (0.22, 0.12), (0.3, 0.26), (0.4, 0.5), (0.45, 0.62)]                                    # cup outer wall
    lathe(cp, STATE['M']['white']); lathe([(0.45, 0.62), (0.44, 0.63), (0.39, 0.5)], STATE['M']['white']); lathe([(0.39, 0.5), (0.3, 0.26), (0.23, 0.15), (0.0, 0.13)], STATE['M']['wood_l'])     # rim + inner glaze
    for k in range(7):                                                                                       # handle: a loop of small segments on the +x side
        t0, t1 = math.pi * 0.15 + k * math.pi * 0.7 / 7, math.pi * 0.15 + (k + 1) * math.pi * 0.7 / 7
        p0 = Vector((cx + (0.45 + 0.2 * math.sin(t0)) * s, cy, z0 + (0.4 + 0.2 * math.cos(t0) * 1.0) * s)); p1 = Vector((cx + (0.45 + 0.2 * math.sin(t1)) * s, cy, z0 + (0.4 + 0.2 * math.cos(t1)) * s))
        mb.frustum(p0, p1, 0.035 * s, 0.035 * s, STATE['M']['white'], seg=6, cap0=False, cap1=False)
    tea_mb.pid += 1; zt = z0 + 0.5 * s; R_ = 0.4 * s                                                          # flat tea surface (fan of 28 triangles)
    pts = [Vector((cx + R_ * math.cos(2 * math.pi * j / 28), cy + R_ * math.sin(2 * math.pi * j / 28), zt)) for j in range(28)]
    for j in range(28): tea_mb.face([Vector((cx, cy, zt)), pts[j], pts[(j + 1) % 28]], STATE['M']['tea'], [(0.5, 0.5), (0.5 + 0.5 * math.cos(2 * math.pi * j / 28), 0.5 + 0.5 * math.sin(2 * math.pi * j / 28)), (0.5, 0.5)])

def _suite(SET, P, M):
    mud_z = _street(SET, P, M, hotel=False, opp=True)
    mb = MB(); WX0, WX1, WZ0, WZ1 = -5.0, 5.0, ZF + 0.08, ZF + 5.6; t = 0.8; wp = M['wallpaper']
    fm = MB(); sbox(fm, (RX0, 0, ZF - 0.6), (RX1, RY1, ZF), M['parquet'], 1 / 8); _obj(fm, 'floor_room', SET)
    rg = MB(); rg.face([Vector((-8.0, 1.0, ZF + 0.03)), Vector((6.0, 1.0, ZF + 0.03)), Vector((6.0, 11.0, ZF + 0.03)), Vector((-8.0, 11.0, ZF + 0.03))], M['rug'], [(0, 0), (1, 0), (1, 1), (0, 1)]); _obj(rg, 'rug', SET)
    sbox(mb, (RX0 - t, -t, ZF + RH), (RX1 + t, RY1 + t, ZF + RH + 0.6), M['cream'], 0.2)                                      # ceiling slab
    sbox(mb, (RX0 - t, 0, ZF - 0.6), (RX0, RY1 + t, ZF + RH + 0.6), wp, 0.25); sbox(mb, (RX1, 0, ZF - 0.6), (RX1 + t, RY1 + t, ZF + RH + 0.6), wp, 0.25); sbox(mb, (RX0, RY1, ZF - 0.6), (RX1, RY1 + t, ZF + RH + 0.6), wp, 0.25)
    sbox(mb, (RX0 - t, -t, ZF - 0.6), (WX0, 0, ZF + RH + 0.6), M['brick'], 1 / 6); sbox(mb, (WX1, -t, ZF - 0.6), (RX1 + t, 0, ZF + RH + 0.6), M['brick'], 1 / 6)
    sbox(mb, (WX0, -t, ZF + RH - 0.6), (WX1, 0, ZF + RH + 0.6), M['brick'], 1 / 6); sbox(mb, (WX0, -t, WZ1), (WX1, 0, ZF + RH - 0.6), M['brick'], 1 / 6); sbox(mb, (WX0, -t, ZF - 0.6), (WX1, 0, WZ0), M['brick'], 1 / 6)
    for (a, b, z0, z1) in ((RX0, WX0, ZF, ZF + RH), (WX1, RX1, ZF, ZF + RH), (WX0, WX1, WZ1, ZF + RH)): sbox(mb, (a, 0.0, z0), (b, 0.5, z1), wp, 0.25)
    sbox(mb, (WX0 - 0.3, -0.7, WZ0 - 0.4), (WX1 + 0.3, 0.6, WZ0), M['ash'], 0.3); sbox(mb, (WX0 - 0.3, -0.4, WZ1), (WX1 + 0.3, 0.6, WZ1 + 0.4), M['ash'], 0.3)           # threshold + head
    for xx in (WX0, WX1): sbox(mb, (xx - 0.18, -0.1, WZ0), (xx + 0.18, 0.5, WZ1), M['white'], 0.3)
    for xx in (-2.5, 0.0, 2.5): sbox(mb, (xx - 0.07, 0.1, WZ0), (xx + 0.07, 0.25, WZ1), M['white'], 0.3)
    for zz in (ZF + 4.1, WZ1 - 0.1): sbox(mb, (WX0, 0.1, zz - 0.08), (WX1, 0.25, zz + 0.08), M['white'], 0.3)
    sbox(mb, (WX0 - 0.6, -1.0, ZF - 0.4), (WX1 + 0.6, 0.0, ZF + 0.05), M['ash'], 0.3)                                              # Juliet balcony ledge + see-through iron rail
    for k in range(int((WX1 - WX0 + 1.2) / 0.55) + 1):
        xx = WX0 - 0.6 + k * 0.55; rod(mb, (xx, -0.9, ZF + 0.05), (xx, -0.9, ZF + 2.3), 0.05, M['iron_d'], seg=4)
    beam(mb, (WX0 - 0.6, -0.9, ZF + 2.3), (WX1 + 0.6, -0.9, ZF + 2.3), 0.12, 0.12, M['iron_d']); beam(mb, (WX0 - 0.6, -0.9, ZF + 0.3), (WX1 + 0.6, -0.9, ZF + 0.3), 0.08, 0.08, M['iron_d'])
    for (x0, x1, y0, y1) in ((RX0, RX0 + 0.35, 0.5, RY1), (RX1 - 0.35, RX1, 0.5, RY1)): sbox(mb, (x0, y0, ZF), (x1, y1, ZF + 2.0), M['plank_f'], 0.2); sbox(mb, (x0 - 0.1, y0, ZF + 2.0), (x1 + 0.1, y1, ZF + 2.2), M['cream'], 0.3)
    sbox(mb, (RX0, RY1 - 0.35, ZF), (RX1, RY1, ZF + 2.0), M['plank_f'], 0.2); sbox(mb, (RX0, RY1 - 0.5, ZF + 2.0), (RX1, RY1, ZF + 2.2), M['cream'], 0.3)
    sbox(mb, (RX0, 0, ZF + RH - 0.9), (RX1, 0.5, ZF + RH), M['cream'], 0.3); sbox(mb, (RX0, 0, ZF + RH - 0.6), (RX0 + 0.6, RY1, ZF + RH), M['cream'], 0.3)
    sbox(mb, (RX1 - 0.6, 0, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3); sbox(mb, (RX0, RY1 - 0.6, ZF + RH - 0.6), (RX1, RY1, ZF + RH), M['cream'], 0.3)
    cm = MB()
    for sg in (-1, 1):                                                                                                        # velvet drapes either side, tied back
        for k in range(5):
            x0 = sg * (WX1 + 0.15) + sg * k * 0.38; sbox(cm, (min(x0, x0 + sg * 0.42), 0.45, ZF + 0.3 + 0.12 * (k % 2)), (max(x0, x0 + sg * 0.42), 1.0 + 0.1 * (k % 2), ZF + 5.9), M['velvet_red'], 0.4)
        ell(cm, (sg * (WX1 + 0.5), 0.4, ZF + 2.4), 0.25, 0.3, 0.25, M['brass'], seg=6, rings=4)
    rod(cm, (WX0 - 2.2, 0.75, ZF + 6.0), (WX1 + 2.2, 0.75, ZF + 6.0), 0.1, M['brass'], seg=6); sbox(cm, (WX0 - 1.0, 0.45, ZF + 5.7), (WX1 + 1.0, 1.2, ZF + 6.15), M['velvet_red'], 0.4)
    _obj(cm, 'curtains', SET); _obj(mb, 'room', SET)
    pf = MB()
    def picture(mat, x, y, z, w, h, face):
        if face == 'x+':
            sbox(pf, (x, y - w / 2 - 0.2, z - h / 2 - 0.2), (x + 0.22, y + w / 2 + 0.2, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x + 0.23, y - w / 2, z - h / 2), (x + 0.23, y + w / 2, z - h / 2), (x + 0.23, y + w / 2, z + h / 2), (x + 0.23, y - w / 2, z + h / 2)], mat, [(1, 0), (0, 0), (0, 1), (1, 1)], (1, 0, 0))
        elif face == 'y+':
            sbox(pf, (x - w / 2 - 0.2, y, z - h / 2 - 0.2), (x + w / 2 + 0.2, y + 0.22, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x + w / 2, y + 0.23, z - h / 2), (x - w / 2, y + 0.23, z - h / 2), (x - w / 2, y + 0.23, z + h / 2), (x + w / 2, y + 0.23, z + h / 2)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 0))
        else:
            sbox(pf, (x - w / 2 - 0.2, y - 0.22, z - h / 2 - 0.2), (x + w / 2 + 0.2, y, z + h / 2 + 0.2), M['frame'], 0.3)
            pf.oface([(x - w / 2, y - 0.23, z - h / 2), (x + w / 2, y - 0.23, z - h / 2), (x + w / 2, y - 0.23, z + h / 2), (x - w / 2, y - 0.23, z + h / 2)], mat, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    picture(M['p_lake'], RX0 + 0.35, 9.0, ZF + 3.9, 3.0, 2.2, 'x+'); picture(M['p_land'], RX0 + 0.35, 4.6, ZF + 3.8, 2.2, 3.0, 'x+'); picture(M['p_portrait'], RX0 + 0.35, 13.5, ZF + 3.9, 1.8, 2.4, 'x+')
    picture(M['p_still'], -5.5, RY1 - 0.35, ZF + 3.8, 2.6, 2.0, 'y-'); picture(M['p_land'], 0.0, RY1 - 0.35, ZF + 3.7, 2.2, 3.0, 'y-'); picture(M['p_portrait'], 5.5, RY1 - 0.35, ZF + 3.8, 1.8, 2.4, 'y-')
    picture(M['p_portrait'], 8.0, 0.5, ZF + 3.6, 1.8, 2.4, 'y+'); picture(M['p_lake'], -8.2, 0.5, ZF + 3.6, 3.0, 2.2, 'y+')
    _obj(pf, 'paintings', SET)
    fb = MB(); tmb = MB(); _furniture(fb, tmb, M); _obj(fb, 'furniture', SET); to = _obj(tmb, 'tea', SET, shadow=False); STATE['tea_obj'] = to
    ch = MB(); fl = MB(); c = Vector((-1.2, 5.0, ZF + 4.4)); rod(ch, (c.x, c.y, ZF + RH), c + Vector((0, 0, 0.3)), 0.06, M['brass'], seg=6)
    ell(ch, c, 0.5, 0.5, 0.5, M['brass'], seg=8, rings=5); rod(ch, c + Vector((0, 0, -0.5)), c + Vector((0, 0, -1.0)), 0.04, M['brass'], seg=5); ell(ch, c + Vector((0, 0, -1.05)), 0.2, 0.2, 0.2, M['brass'], seg=6, rings=4)
    for k in range(6):
        a = 2 * math.pi * k / 6; e = c + Vector((1.5 * math.cos(a), 1.5 * math.sin(a), -0.1))
        ch.frustum(c + Vector((0, 0, -0.05)), e, 0.05, 0.05, M['brass'], seg=4); rod(ch, e, e + Vector((0, 0, 0.5)), 0.08, M['brass'], seg=6); rod(ch, e + Vector((0, 0, 0.5)), e + Vector((0, 0, 0.9)), 0.07, M['white'], seg=6)
        fl.frustum(e + Vector((0, 0, 0.9)), e + Vector((0, 0, 1.05)), 0.07, 0.01, M['glass_cand'], seg=5); _halo(fl, e + Vector((0, 0, 1.0)), 0.5, M)
        for j in range(3): rod(ch, e + Vector((0.08 * j, 0, 0.0)), e + Vector((0.08 * j, 0, -0.55 - 0.1 * j)), 0.02, M['white'], seg=3)
    D._flame_light('chandelier', tuple(c + Vector((0, 0, 0.5))), LAMP, 700, radius=0.3, shadow=True)
    _obj(ch, 'chandelier', SET); _obj(fl, 'candles', SET, shadow=False)
    STATE['marks'].update(window=(0.4, 1.4, ZF, 0), window_l=(-3.2, 1.6, ZF, 0), window_r=(3.4, 1.6, ZF, 0), tea_side=(-3.6, 3.8, ZF, 0), chair_side=(3.2, 5.8, ZF, 0), room_c=(-1.0, 8.0, ZF, 0))
    STATE['tea_xyz'] = (TEA['x'] - 0.2, TEA['y'] - 0.5, TEA['top'] + 0.03)
    # a busy street below: carts (street dress) + a crowd of workers and townsfolk standing in the mud and on the plank walks
    crowd(30, [(-34, 34, -46, -20)], seed=21, ground=lambda x, y: float(mud_z(np.array([x]), np.array([y]))[0]))
    crowd(8, [(-30, 30, -8.2, -3.5)], seed=33, ground=lambda x, y: 0.4)

def _furniture(mb, tmb, M):
    """red velvet armchair (visible), teal armchair, round tea table with cup / saucer / pot / plate, side table with vase, sideboard."""
    def chair(cx, cy, yaw, mat):
        ex = Vector((math.cos(yaw), math.sin(yaw), 0)); ey = Vector((-math.sin(yaw), math.cos(yaw), 0)); Z = Vector((0, 0, 1)); P = lambda x, y, z: Vector((cx, cy, ZF)) + ex * x + ey * y + Z * z
        obox(mb, P(0, 0, 1.0), ex, ey, Z, 1.4, 1.35, 0.45, mat, 0.4); obox(mb, P(0, 1.2, 2.5), ex, ey, Z, 1.4, 0.28, 1.45, mat, 0.4)
        for sg in (-1, 1): obox(mb, P(sg * 1.5, 0, 1.55), ex, ey, Z, 0.28, 1.35, 0.55, mat, 0.4); ell(mb, P(sg * 1.5, -1.3, 2.15), 0.34, 0.34, 0.34, mat, seg=10, rings=6)
        ell(mb, P(0, 1.2, 4.05), 1.4, 0.3, 0.2, mat, seg=12, rings=5, yaw=yaw)
        for sx in (-1, 1):
            for sy in (-1, 1): rod(mb, P(sx * 1.25, sy * 1.2, 0.0), P(sx * 1.25, sy * 1.2, 0.6), 0.16, M['wood_d'], seg=6, r1=0.1)
        obox(mb, P(0, -1.38, 1.1), ex, ey, Z, 1.42, 0.05, 0.12, M['brass'], 0.4)
        for k in range(5): ell(mb, P(-1.0 + 0.5 * k, -1.45, 1.1), 0.08, 0.08, 0.08, M['brass'], seg=5, rings=3)       # brass studs along the seat front
    chair(4.2, 4.2, math.radians(-150), M['velvet_red']); chair(-7.4, 6.4, math.radians(-40), M['velvet_teal'])
    tx, ty = TEA['x'], TEA['y']; zt = TEA['top']
    mb.frustum((tx, ty, ZF), (tx, ty, zt - 0.1), 0.25, 0.2, M['wood_d'], seg=8); mb.frustum((tx, ty, zt - 0.1), (tx, ty, zt), 1.5, 1.5, M['wood'], seg=20)
    for k in range(3): a = k * 2 * math.pi / 3 + 0.4; mb.frustum((tx, ty, ZF + 0.15), (tx + 1.2 * math.cos(a), ty + 1.2 * math.sin(a), ZF), 0.14, 0.1, M['wood_d'], seg=5)
    mb.frustum((tx, ty, zt), (tx, ty, zt + 0.03), 1.1, 1.1, M['white'], seg=20)
    _cup(mb, tmb, tx - 0.2, ty - 0.5, zt + 0.03, 1.5); _cup(mb, tmb, tx + 0.7, ty + 0.35, zt + 0.03, 1.5)
    mb.frustum((tx - 0.6, ty + 0.5, zt + 0.03), (tx - 0.6, ty + 0.5, zt + 0.7), 0.26, 0.36, M['white'], seg=12); ell(mb, (tx - 0.6, ty + 0.5, zt + 0.74), 0.3, 0.3, 0.14, M['white'], seg=10, rings=5)
    mb.frustum((tx - 0.4, ty + 0.5, zt + 0.5), (tx, ty + 0.55, zt + 0.72), 0.05, 0.03, M['white'], seg=4)
    mb.frustum((tx + 0.35, ty - 0.55, zt + 0.03), (tx + 0.35, ty - 0.55, zt + 0.08), 0.42, 0.42, M['brass'], seg=12)
    for k in range(3): ell(mb, (tx + 0.25 + 0.2 * k, ty - 0.55 + 0.1 * (k % 2), zt + 0.18), 0.13, 0.13, 0.1, M['clay'], seg=6, rings=4)
    mb.frustum((7.5, 12.0, ZF), (7.5, 12.0, ZF + 1.6), 0.18, 0.2, M['wood_d'], seg=6); mb.frustum((7.5, 12.0, ZF + 1.6), (7.5, 12.0, ZF + 1.72), 0.8, 0.8, M['wood'], seg=12)
    ell(mb, (7.5, 12.0, ZF + 2.3), 0.35, 0.35, 0.55, M['teal'], seg=8, rings=5); mb.frustum((7.5, 12.0, ZF + 2.7), (7.5, 12.0, ZF + 3.2), 0.12, 0.2, M['teal'], seg=7)
    sbox(mb, (RX1 - 2.2, 2.0, ZF), (RX1 - 0.4, 7.5, ZF + 2.5), M['plank_f'], 0.2); sbox(mb, (RX1 - 2.35, 1.9, ZF + 2.5), (RX1 - 0.3, 7.6, ZF + 2.7), M['ash'], 0.3)
    ell(mb, (RX1 - 1.2, 3.5, ZF + 3.1), 0.35, 0.35, 0.4, M['brass'], seg=8, rings=5); ell(mb, (RX1 - 1.2, 6.0, ZF + 3.0), 0.3, 0.3, 0.3, M['red'], seg=8, rings=5)
