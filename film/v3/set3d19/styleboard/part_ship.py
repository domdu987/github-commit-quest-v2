
# ================================================================== STILL 2: Royal Navy 50-gun ship, forecastle view over the starboard bow
DECK = 6.0
def hw(y):
    """deck half-beam at y (m): full beam to y=8, narrowing to the stem at y=30 (works on floats and arrays)"""
    t = np.clip((np.asarray(y, dtype=np.float64) - 8.0) / 22.0, 0.0, 1.0)
    r = 3.7 * np.maximum(0.0, 1 - t ** 2.0) ** 0.85
    return float(r) if np.ndim(r) == 0 else r

def ship_mats():
    M = {}
    M['deck1'] = mat('deck1', '#9a7440', '#85632f', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['deck2'] = mat('deck2', '#876530', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['seam'] = mat('seam', '#2c1c20')
    M['hullb'] = mat('hullb', '#262034', '#332c44', scale=2, aniso=(0.3, 0.3, 1))
    M['ochre'] = mat('ochre', '#cf9230', '#bd7f26', scale=3)
    M['bulw'] = mat('bulw', '#a24c2c', '#8f3f28', scale=3, aniso=(0.2, 1, 1))
    M['cap'] = mat('cap', '#2a2230', '#3a2e3c', scale=3)
    M['iron'] = metal_mat('iron', '#2c2a3a', '#3e3c50', rough=0.55, spec=0.3)
    M['carr'] = mat('carr', '#8c4a2a', '#a05a32', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#b8862c', '#d8a842', rough=0.38, spec=0.45)
    M['sail'] = mat('sail', '#e4cc90', '#d6b87c', scale=2.2, contrast=1.1, emit='#ffe6a0', emit_k=0.42)
    M['sailb'] = mat('sailb', '#d4b886', '#c4a674', scale=2.2)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['cream'] = mat('cream', '#efe0b8')
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#7096d0', 0.95)
    M['darksail'] = mat('darksail', '#2c2838')
    return M

def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_quad(mb, m, x0, x1, zb, zt, y, belly, ny=6, nx=8, topx=None):
    """cream square sail seen from astern: grid with forward (+y) belly; double-sided"""
    def P(i, j):
        u = i / nx; v = j / ny
        xl = x0 + (x1 - x0) * u; zz = zb + (zt - zb) * v
        by = belly * math.sin(math.pi * u) * math.sin(math.pi * (0.15 + 0.85 * v)) ** 0.8
        return (xl * (1 + 0.05 * (1 - v)), y + by, zz)
    for i in range(nx):
        for j in range(ny):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            mb.quad(m, q); mb.quad(m, q[::-1])

def build_ship(P):
    M = ship_mats(); mb = MB('ship'); rr = rnd(5)
    Y0, Y1 = -9.0, 30.0
    # ---- deck planks (clipped to the hull outline)
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        ax = abs(x)
        # y where hw(y) = ax
        ylim = 8.0
        if ax < 3.7:
            lo, hi = 8.0, 30.0
            for _ in range(30):
                mid = (lo + hi) / 2
                if hw(mid) > ax: lo = mid
                else: hi = mid
            ylim = lo
        mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (4.0 + ylim) / 2, DECK - 0.08), (0.255, ylim - 4.0, 0.16))
        x += 0.26; k += 1
    mb.box(M['seam'], (0, (Y0 + Y1) / 2, DECK - 0.2), (7.0, Y1 - Y0, 0.1))
    # ---- hull body: black with an ochre wale/stripe; flare widens slightly below the deck
    y = Y0
    while y < Y1:
        yc = y + 0.5; b = hw(yc) + 0.0
        if b > 0.05:
            for s in (-1, 1):
                for (z0, z1, mm, ex) in ((0.0, 2.7, 'hullb', 0.85), (2.7, 3.15, 'ochre', 0.8), (3.15, 5.75, 'hullb', 0.5)):
                    t = ex * (1 - (z0 + z1) / 2 / DECK) * 0 + (0.9 - 0.9 * ((z0 + z1) / 2) / 6.0) if False else (0.55 + 0.45 * (1 - ((z0 + z1) / 2) / 5.8)) * 0.9
                    mb.box(M[mm], (s * (b + t / 2 - 0.0), yc, (z0 + z1) / 2), (t + 0.0, 1.04, z1 - z0))
            mb.box(M['hullb'], (0, yc, 2.9), (2 * b, 1.04, 5.8))
        y += 1.0
    # ---- bulwarks (inner red, black cap) with gun ports cut out
    gun_y = [7.0, 10.8, 14.6, 18.4]; gun_y_port = [7.8, 11.6, 15.4]
    y = Y0
    while y < 29.0:
        yc = y + 0.3; b = hw(yc)
        for s, gy in ((1, gun_y), (-1, gun_y_port)):
            if b < 0.3: continue
            if any(abs(yc - g) < 0.42 for g in gy): continue
            dy = hw(yc + 0.3) - hw(yc - 0.3); ang = math.atan2(-dy * s, 0.6)
            mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 0.3), (0.16, 0.66, 0.6), rz=ang); mb.box(M['ochre'], (s * (b - 0.04), yc, DECK + 0.78), (0.17, 0.66, 0.36), rz=ang); mb.box(M['hullb'], (s * (b - 0.04), yc, DECK + 1.02), (0.16, 0.66, 0.12), rz=ang)
        y += 0.6
    for s in (-1, 1):
        y = Y0
        while y < 29.5:
            yc = y + 0.35; b = hw(yc); dy = hw(yc + 0.35) - hw(yc - 0.35)
            if b > 0.2: mb.box(M['cap'], (s * (b - 0.02), yc, DECK + 1.14), (0.3, 0.74, 0.1), rz=math.atan2(-dy * s, 0.7))
            y += 0.7
    # ---- quarterdeck platform (camera stands here), 2 m above the waist, with a balustrade and a stair gap at the front
    YQ = 4.4; ZQ = 8.0
    mb.box(M['hullb'], (0, (Y0 + YQ) / 2, 7.0), (7.7, YQ - Y0, 2.0)); mb.box(M['ochre'], (0, YQ + 0.005, 7.0), (7.72, 0.04, 0.3)); mb.box(M['ochre'], (3.87, (Y0 + YQ) / 2, 7.0), (0.04, YQ - Y0, 0.3)); mb.box(M['ochre'], (-3.87, (Y0 + YQ) / 2, 7.0), (0.04, YQ - Y0, 0.3))
    for gx in (-2.6, -1.3, 1.3, 2.6): mb.box(M['cap'], (gx, YQ + 0.005, 6.5), (0.5, 0.05, 0.42))
    x = -3.5 + 0.13; k = 0
    while x < 3.6:
        mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (Y0 + YQ) / 2, ZQ - 0.02), (0.255, YQ - Y0, 0.06)); x += 0.26; k += 1
    for s in (-1, 1):
        y = Y0
        while y < YQ:
            mb.box(M['hullb'], (s * 3.66, y + 0.3, ZQ + 0.25), (0.16, 0.62, 0.5)); mb.box(M['ochre'], (s * 3.66, y + 0.3, ZQ + 0.68), (0.17, 0.62, 0.36)); mb.box(M['hullb'], (s * 3.66, y + 0.3, ZQ + 0.93), (0.16, 0.62, 0.14)); y += 0.6
        mb.box(M['cap'], (s * 3.67, (Y0 + YQ) / 2, ZQ + 1.03), (0.3, YQ - Y0, 0.1))
    for xx in np.arange(-3.4, 3.5, 0.45):
        if abs(xx) < 0.75: continue
        mb.box(M['oak'], (xx, YQ - 0.1, ZQ + 0.5), (0.09, 0.09, 1.0))
    for (a, b_) in ((-3.7, -0.75), (0.75, 3.7)): mb.box(M['cap'], ((a + b_) / 2, YQ - 0.1, ZQ + 1.03), (b_ - a, 0.16, 0.1))
    for st in range(3): mb.box(M['deck1'], (0, YQ + 0.3 + 0.3 * st, ZQ - 0.6 - 0.6 * st), (1.3, 0.5, 0.1))
    # ship's wheel (vertical spoked wheel on a drum) and binnacle on the quarterdeck
    wx_, wy_ = -0.45, 2.5
    mb.box(M['oak'], (wx_, wy_, ZQ + 0.45), (0.5, 0.5, 0.9)); gear(mb, M['oak'], (wx_, wy_ - 0.28, ZQ + 1.0), 0.5, nt=8, th=0.07, rim=0.07, spokes=4, tooth=0.1, hub=0.1, n=18)
    for a in range(8): mb.rod(M['oak'], (wx_ + 0.5 * math.cos(a * 0.785), wy_ - 0.28, ZQ + 1.0 + 0.5 * math.sin(a * 0.785)), (wx_ + 0.7 * math.cos(a * 0.785), wy_ - 0.28, ZQ + 1.0 + 0.7 * math.sin(a * 0.785)), 0.035, 0.035, 6)
    bnx, bny = -0.05, 0.95
    mb.box(M['oak'], (bnx, bny, ZQ + 0.38), (0.55, 0.5, 0.76)); mb.box(M['cap'], (bnx, bny, ZQ + 0.8), (0.62, 0.56, 0.06))
    mb.ell(M['brass'], (bnx, bny, ZQ + 0.98), (0.21, 0.21, 0.2), (14, 10)); mb.cyl(M['brass'], (bnx, bny, ZQ + 0.86), 0.24, 0.05, seg=14)
    for (cx, cy, r, n) in [(2.3, 1.1, 0.3, 3), (2.6, 3.0, 0.3, 3)]:
        for l in range(n): ring_xy(mb, M['rope'], (cx, cy, ZQ + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
        mb.cyl(M['rope'], (cx, cy, ZQ + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)
    mb.ell(M['oak'], (-1.7, 3.4, ZQ + 0.45), (0.33, 0.33, 0.47), (14, 10))
    for z in (0.2, 0.45, 0.7): mb.cyl(M['iron'], (-1.7, 3.4, ZQ + z), 0.3, 0.035, seg=14)
    # ---- cannons on carriages
    def cannon(side, y, rr):
        b = hw(y); s = side; zc = DECK + 0.62
        xo = s * (b - 0.1)                                       # muzzle pokes out through the port
        xi = s * (b - 2.0)
        tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.3, y, zc), 0.23, 0.15, 12)
        mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.22, y, zc), 0.19, 0.08, axis='x', seg=12)
        for yy in (-0.3, 0.3):
            mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, DECK + 0.3), (1.6, 0.14, 0.5))
        mb.box(M['carr'], (xi + s * 0.45, y, DECK + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, DECK + 0.46), (0.5, 0.5, 0.06))   # axle block + quoin
        for dx in (-0.35, 0.5):
            mb.cyl(M['oak'], (s * (b - 1.0) + s * dx, y - 0.36, DECK + 0.17), 0.17, 0.1, axis='y', seg=12); mb.cyl(M['oak'], (s * (b - 1.0) + s * dx, y + 0.36, DECK + 0.17), 0.17, 0.1, axis='y', seg=12)
        mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y - 0.7, DECK + 0.9), 0.03, 0.03, 5); mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y + 0.7, DECK + 0.9), 0.03, 0.03, 5)
        mb.rod(M['rope'], (xo, y, zc + 0.2), (s * (b + 0.0), y + 0.5, DECK + 0.9), 0.03, 0.03, 5)
    for g in gun_y: cannon(1, g, rr)
    for g in gun_y_port: cannon(-1, g, rr)
    # ---- foreground deck furniture (nearest 15 % of the frame)
    for (bx, by) in [(-1.6, 6.2), (-2.35, 6.8), (1.3, 8.5)]:                               # barrels
        mb.ell(M['oak'], (bx, by, DECK + 0.45), (0.33, 0.33, 0.47), (14, 10))
        for z in (0.2, 0.45, 0.7): mb.cyl(M['iron'], (bx, by, DECK + z), 0.29 + 0.03 * math.sin(math.pi * (z - 0.0) / 0.9) * 0.5, 0.035, seg=14)
    mb.ell(M['red'], (-0.55, 5.9, DECK + 0.3), (0.0001, 0.0001, 0.0001), (4, 4)) if False else None
    mb.cyl(M['oak'], (-1.3, 10.0, DECK + 0.55), 0.42, 1.1, seg=14); mb.cyl(M['cap'], (-1.3, 10.0, DECK + 1.15), 0.5, 0.1, seg=14)       # capstan
    for a in range(4): mb.rod(M['oak'], (-1.3, 10.0, DECK + 0.9), (-1.3 + 1.0 * math.cos(a * 1.571 + 0.5), 10.0 + 1.0 * math.sin(a * 1.571 + 0.5), DECK + 0.9), 0.05, 0.05, 6)
    for i in range(5):                                                                      # hatch grating
        mb.box(M['oak'], (1.0 + 0.0, 12.6 + 0.3 * i, DECK + 0.05), (1.5, 0.07, 0.09)); mb.box(M['oak'], (0.3 + 0.3 * i, 13.2, DECK + 0.06), (0.07, 1.4, 0.09))
    mb.cyl(M['oak'], (0.8, 6.0, DECK + 0.14), 0.2, 0.28, seg=10); mb.cyl(M['rope'], (0.8, 6.0, DECK + 0.29), 0.17, 0.03, seg=10)          # bucket
    mb.box(M['cap'], (0.0, 17.2, DECK + 0.8), (1.0, 1.0, 1.6))                               # forecastle bitts
    # ---- foremast + rigging
    mx, my = 0.2, 22.0
    tube(mb, M['mast'], (mx, my, DECK), (mx, my, 24.5), 0.52, 0.26, 12); tube(mb, M['mast'], (mx, my, 17.5), (mx, my, 36), 0.3, 0.16, 10)
    mb.box(M['mast'], (mx, my, 17.3), (3.0, 2.2, 0.22))                                    # top platform
    mb.box(M['mast'], (mx, my, 6.8), (1.4, 1.4, 0.1))
    for a in range(10): mb.rod(M['iron'], (mx + 0.5 * math.cos(a * .628), my + 0.5 * math.sin(a * .628), DECK + 1.1), (mx + 0.5 * math.cos(a * .628), my + 0.5 * math.sin(a * .628), DECK + 1.5), 0.04, 0.04, 5)
    for (zy, ln, r) in [(14.6, 13.0, 0.17), (24.6, 9.4, 0.13), (31.0, 6.4, 0.1)]:
        tube(mb, M['mast'], (mx - ln / 2, my, zy), (mx + ln / 2, my, zy), r, r * 0.6, 8)
    sail_quad(mb, M['sail'], mx - 6.0, mx + 6.0, 8.5, 14.4, my + 0.6, 1.5)
    sail_quad(mb, M['sail'], mx - 4.4, mx + 4.4, 18.0, 24.4, my + 0.7, 1.1)
    sail_quad(mb, M['sail'], mx - 3.0, mx + 3.0, 25.0, 30.8, my + 0.8, 0.8)
    for s in (-1, 1):                                                                      # shrouds + ratlines
        for k in range(5):
            yy = my - 1.4 + 0.75 * k; bx = hw(yy) - 0.1
            top = (mx + s * 0.35, my - 0.5 + 0.28 * k - 0.6, 17.3); bot = (s * bx, yy, DECK + 1.1)
            mb.rod(M['rig'], top, bot, 0.035, 0.035, 4)
        for j in range(12):
            t = j / 12
            a = Vector((s * (hw(my - 1.4) - 0.1) * (1 - t) + (mx + s * 0.35) * t, my - 1.4 + (-0.6 + 0.0) * t, DECK + 1.1 + (17.3 - DECK - 1.1) * t))
            b = Vector((s * (hw(my + 1.6) - 0.1) * (1 - t) + (mx + s * 0.35) * t, my + 1.6 - 0.6 * t - 0.0, DECK + 1.1 + (17.3 - DECK - 1.1) * t))
            mb.rod(M['rig'], a, b, 0.022, 0.022, 4)
    tube(mb, M['rig'], (mx, my, 36), (0, 34.0, 11.0), 0.04, 0.04, 4)                       # forestay
    tube(mb, M['rig'], (mx, my, 25.0), (0, 26.6, 8.6), 0.04, 0.04, 4)
    tube(mb, M['rig'], (mx + 0.2, my - 2.2, 17.3), (mx + 0.4, my - 8.0, DECK + 1.3), 0.04, 0.04, 4)   # backstay
    tube(mb, M['mast'], (0, 25.0, 7.2), (0, 40.0, 11.6), 0.26, 0.12, 10)                   # bowsprit
    mb.tri(M['sail'], [(0, 34.0, 11.0), (0, 38.0, 11.2), (0, 29.0, 8.5)]) if False else None
    # jib: triangle on the forestay, billowed
    for o in (0.0, 0.0):
        mb.quad(M['sail'], [(0, 34.0, 11.0), (0.7, 33.4, 9.6), (0, 29.5, 8.5), (0, 29.5, 8.5)]); mb.quad(M['sail'], [(0, 29.5, 8.5), (0, 29.5, 8.5), (0.7, 33.4, 9.6), (0, 34.0, 11.0)])
    mb.quad(M['red'], [(mx, my, 35.8), (mx - 0.2, my, 35.6), (mx - 2.8, my - 0.3, 35.2), (mx - 2.8, my - 0.3, 36.1)])        # pennant
    mb.quad(M['red'], [(mx - 2.8, my - 0.3, 36.1), (mx - 2.8, my - 0.3, 35.2), (mx - 0.2, my, 35.6), (mx, my, 35.8)])
    mb.finish()
    # ---- far dressing: island + a tiny dark sail on the horizon
    ib = MB('isle'); n = 40
    for i in range(n):
        x0 = 380 + i * 8.0; x1 = x0 + 8.0
        f = lambda x: 90 * max(0, math.sin(math.pi * (x - 380) / (n * 8.0))) ** 0.7 + 4 * math.sin((x - 380) / 7.0) ** 2 * math.sin(math.pi * (x - 380) / (n * 8.0))
        ib.quad(M['isle'], [(x0, 1700, -4), (x1, 1700, -4), (x1, 1700, f(x1) + 1), (x0, 1700, f(x0) + 1)])
    ib.finish(shadow=False)
    sb_ = MB('farsail'); sb_.quad(M['darksail'], [(910, 1300, 0.5), (936, 1300, 0.5), (928, 1300, 24), (914, 1300, 28)]); sb_.quad(M['darksail'], [(905, 1300, 0.5), (935, 1300, 0.5), (935, 1300, 3), (905, 1300, 3)]); sb_.finish(shadow=False)
    cm = MB('cards'); card(cm, M['grey'], 0.55, 2.4, w=0.55, z0=8.0); card(cm, M['grey'], 1.25, 3.1, w=0.55, z0=8.0); cm.finish() if not os.environ.get('NOCARDS') else None
    build_sea(P)
    clouds(P)

# ---------------------------------------------------------------- the sea: real wave mesh built per camera pixel, with painted foam, crest tint, haze and sun glitter
def build_sea(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.12, 0.8182
    vh = -f[2] / u[2] / hy; zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.18
    NU, NV = 420, 760
    uu = np.linspace(-1.12, 1.12, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV) ** 1.0
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    rng = np.random.RandomState(11)
    th0 = math.radians(80); waves = []
    spec = [(26, .5), (16, .3), (10.5, .2), (7.2, .13), (5.0, .08), (3.4, .05), (2.4, .03), (1.7, .02), (1.15, .014), (0.8, .01), (0.55, .007), (0.36, .005), (0.24, .004)]
    for (L, A) in spec:
        a = th0 + rng.uniform(-0.95, 0.95); waves.append((L, A, a, rng.uniform(0, 6.28)))
    fpx = t * (2 * hx / 720.0) * 1.1
    h = np.zeros_like(px); gx = np.zeros_like(px); gy = np.zeros_like(px); hm = np.zeros_like(px); gsx = np.zeros_like(px); gsy = np.zeros_like(px)
    for (L, A, a, ph) in waves:
        k = 2 * math.pi / L; kx = k * math.cos(a); ky = k * math.sin(a)
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 2.5) / 5.0, 0, 1)
        th = kx * px + ky * py + ph; s = np.sin(th); cs = np.cos(th)
        q = 0.5 + 0.5 * s; hh = A * (2 * q ** 1.8 - 1.0); dh = A * 2 * 1.8 * q ** 0.8 * 0.5 * cs * k
        if L > 1.0:
            h += hh * fade; gx += dh * math.cos(a) * fade; gy += dh * math.sin(a) * fade
            if L < 11: hm += hh * fade * (1.0 / A)
        else:     # glitter ripples: contribute slopes only (not geometry) with a floor so they survive distance
            gsx += dh * math.cos(a) * 1.6 * (0.35 + 0.65 * fade); gsy += dh * math.sin(a) * 1.6 * (0.35 + 0.65 * fade)
    far = np.clip(1 - t / 2500.0, 0, 1) ** 0.5
    h *= far
    # foam: thin lines where the mid waves peak, plus bow wash / hull wash near the ship outline
    wn = hm / 6.0
    nz = 0.5 + 0.5 * np.sin(px * 0.37 + py * 0.21 + 2.0 * np.sin(py * 0.11)) * np.sin(py * 0.43 - px * 0.17)
    foam = np.clip((wn - 0.20) / 0.10, 0, 1) * (0.55 + 0.45 * nz) * np.clip(1 - t / 900, 0.0, 1)
    crest = np.clip((wn - 0.0) / 0.5, 0, 1)
    d_hull = np.abs(px) - (hw(np.clip(py, -9, 30)) + 0.9); d_hull = np.where((py > -9) & (py < 31), d_hull, 9)
    wash = np.exp(-np.maximum(d_hull, 0) / 1.4) * (0.5 + 0.5 * np.sin(py * 1.7 + px * 2.3)) * (d_hull < 6)
    foam = np.clip(foam + 0.9 * wash * np.clip((nz + 0.4), 0, 1), 0, 1)
    haze = np.clip(1 - np.exp(-t / 1500.0), 0, 1) ** 1.3
    # glitter: reflect the view ray about the (wave + ripple) normal, compare with a virtual sun direction (low enough to hit modest slopes)
    nx_ = -(gx + gsx); ny_ = -(gy + gsy); nz_ = np.ones_like(px); nl = np.sqrt(nx_ ** 2 + ny_ ** 2 + nz_ ** 2); nx_ /= nl; ny_ /= nl; nz_ /= nl
    vx = px - loc[0]; vy = py - loc[1]; vz = h - loc[2]; vl = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2); vx /= vl; vy /= vl; vz /= vl
    dn = vx * nx_ + vy * ny_ + vz * nz_
    Rx = vx - 2 * dn * nx_; Ry = vy - 2 * dn * ny_; Rz = vz - 2 * dn * nz_
    se = math.radians(P['glit_el']); sa = math.radians(P['glit_az'])
    S = np.array([math.sin(sa) * math.cos(se), math.cos(sa) * math.cos(se), math.sin(se)])
    dd = Rx * S[0] + Ry * S[1] + Rz * S[2]
    glit = np.clip((dd - P['glit_lo']) / (P['glit_hi'] - P['glit_lo']), 0, 1) ** 1.2
    az = np.arctan2(px - loc[0], py - loc[1]); daz = az - sa
    glit *= np.exp(-(daz / (0.10 + 0.0 * t)) ** 2) * np.clip(1 - t / 1800, 0.25, 1)
    # mesh
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    quads = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nl_ = len(quads); me.loops.add(nl_ * 4); me.polygons.add(nl_)
    me.loops.foreach_set('vertex_index', quads.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nl_) * 4).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nl_, 4, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nl_, dtype=bool))
    for name, arr in (('foam', foam), ('crest', crest), ('haze', haze), ('glit', glit)):
        at = me.attributes.new(name, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    # material
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.55; bs.inputs['Specular IOR Level'].default_value = 0.0
    def attr(n):
        a = N('ShaderNodeAttribute'); a.attribute_type = 'GEOMETRY'; a.attribute_name = n; return a.outputs['Fac']
    def mix(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = a if not hasattr(a, 'node') else (0, 0, 0, 1); mx.inputs[7].default_value = b if not hasattr(b, 'node') else (0, 0, 0, 1)
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        L(fac, mx.inputs[0]); return mx.outputs[2]
    # slow two-tone variation (painterly bands) from a stretched noise on world coords
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (0.05, 0.22, 1.0); L(tc.outputs['Object'], mp.inputs['Vector'])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Detail'].default_value = 5; L(mp.outputs[0], nz.inputs['Vector']); cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.35; cr.color_ramp.elements[1].position = 0.65; L(nz.outputs['Fac'], cr.inputs[0])
    deep = mix(hexc('#08607f'), hexc('#0e8190'), cr.outputs[0])
    col = mix(deep, hexc('#3cc8b8'), attr('crest'))
    col = mix(col, hexc('#f3f7f2'), attr('foam'))
    col = mix(col, hexc('#7cace0'), attr('haze'))
    L(col, bs.inputs['Base Color'])
    gm = N('ShaderNodeMath'); gm.operation = 'MULTIPLY'; gm.inputs[1].default_value = P.get('glit_k', 6.0); L(attr('glit'), gm.inputs[0])
    bs.inputs['Emission Color'].default_value = hexc('#fff2cc'); L(gm.outputs[0], bs.inputs['Emission Strength'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#b4d0f0'), (0.5, '#a8c8ee'), (0.58, '#82aee6'), (0.78, '#5b88d6'), (1.0, '#4a78cd')], sky_k=1.0,
    key=(1.0, 0.88, 0.7, 7.5), key_dir=kdir(22, 46), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.9), samples=80, dbounce=1,
    cloud=('#fff2dc', '#9aa6e8'), cloud_diffuse=True, cloud_z=(70, 170), ncloud=7, cloud_seed=4, cloud_scale=0.7,
    glit_az=22, glit_el=20, glit_lo=0.9975, glit_hi=0.9995, glit_k=5.0,
    cam=dict(loc=(0.4, -1.0, 11.0), look=(0.4 + 5.6, 39.0, 0.4), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world(P)
