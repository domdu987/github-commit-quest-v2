
# ================================================================== STILL 2 (v2): Royal Navy 50-gun ship, forecastle view forward-down over the bow
DECK = 6.0; ZF = 8.0; STEM = 46.0; YF = 27.0          # waist deck z, forecastle deck z, stem y, forecastle starts at YF
def hw(y):
    """deck half-beam at y (m): full beam to y=20, narrowing to the stem at y=46 (floats and arrays)"""
    t = np.clip((np.asarray(y, dtype=np.float64) - 20.0) / (STEM - 20.0), 0.0, 1.0)
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
    M['iron'] = metal_mat('iron', '#2c2a3a', '#3e3c50', rough=0.5, spec=0.35)
    M['carr'] = mat('carr', '#8c4a2a', '#a05a32', scale=4, aniso=(0.2, 1, 1))
    M['oak'] = mat('oak', '#8a5a2c', '#9e6a34', scale=5, aniso=(0.15, 1, 1))
    M['mast'] = mat('mast', '#8a5c34', '#a2703c', scale=3, aniso=(0.2, 0.2, 0.05))
    M['rope'] = mat('rope', '#b8924c', '#9a7638', scale=6)
    M['rig'] = mat('rig', '#2a2030', '#3a2e3a', scale=3)
    M['brass'] = metal_mat('brass', '#cb9f48', '#e6bb5c', rough=0.28, spec=0.8, metallic=0.9)
    M['sail'] = mat('sail', '#e8dcc0', '#dccfae', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.3)
    M['sail2'] = mat('sail2', '#d8c9a6', '#cdbd98', scale=2.2, contrast=1.1, emit='#ffe2a0', emit_k=0.25)
    M['red'] = mat('red', '#b83a32', '#9c2e2c', scale=4)
    M['grey'] = mat('grey', '#a4a8b8')
    M['isle'] = mat_emit('isle', '#6f9a78', 0.9); M['isle2'] = mat_emit('isle2', '#4f7e68', 0.8); M['beach'] = mat_emit('beach', '#e8dcb8', 1.0)
    M['darksail'] = mat('darksail', '#2c2838')
    M['lamp'] = mat_emit('lamp', '#ffd890', 6.0)
    return M

def tube(mb, m, p0, p1, r0, r1=None, seg=8): mb.rod(m, p0, p1, r0, r1, seg=seg, caps=True, smooth=True)

def sail_tri(mb, M, T, C, Hd, bulge, n=8, m=8):
    """billowing triangular jib: luff T->Hd, leech C->Hd, belly sideways (+x) and forward; canvas strips alternate colour"""
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def P(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m
        p = L + (Rr - L) * u
        b = bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.12 + 0.88 * v)) * (1 - 0.5 * v)
        return (p.x + b, p.y + b * 0.4, p.z)
    for i in range(m):
        for j in range(n):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            mm = M['sail'] if i % 2 else M['sail2']
            mb.quad(mm, q); mb.quad(mm, q[::-1])

def sail_quad(mb, M, x0, x1, zb, zt, y, belly, ny=8, nx=10):
    def P(i, j):
        u = i / nx; v = j / ny
        xl = x0 + (x1 - x0) * u; zz = zb + (zt - zb) * v
        by = belly * math.sin(math.pi * u) * math.sin(math.pi * (0.15 + 0.85 * v)) ** 0.8 + 0.25 * math.sin(math.pi * u * 2.0) * 0.0
        return (xl * (1 + 0.05 * (1 - v)), y + by, zz)
    for i in range(nx):
        for j in range(ny):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            mm = M['sail'] if i % 2 else M['sail2']; mb.quad(mm, q); mb.quad(mm, q[::-1])

def build_ship(P):
    M = ship_mats(); mb = MB('ship'); rr = rnd(5)
    Y0 = -6.0
    # ---- waist deck planks (clipped to the outline) + hull body strips (black, ochre wale, tumblehome flare)
    def ylim_for(ax):
        if ax >= 3.699: return 20.0
        lo, hi = 20.0, STEM
        for _ in range(30):
            mid = (lo + hi) / 2
            if hw(mid) > ax: lo = mid
            else: hi = mid
        return lo
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)); mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (Y0 + min(yl, YF + 0.2)) / 2, DECK - 0.08), (0.255, min(yl, YF + 0.2) - Y0, 0.16)); x += 0.26; k += 1
    y = Y0
    while y < STEM:
        yc = y + 0.5; b = hw(yc)
        if b > 0.05:
            for s in (-1, 1):
                for (z0, z1, mm) in ((0.0, 2.7, 'hullb'), (2.7, 3.15, 'ochre'), (3.15, 5.75, 'hullb')):
                    t = (0.55 + 0.45 * (1 - ((z0 + z1) / 2) / 5.8)) * 0.9
                    mb.box(M[mm], (s * (b + t / 2), yc, (z0 + z1) / 2), (t, 1.04, z1 - z0))
            mb.box(M['hullb'], (0, yc, 2.9), (2 * b, 1.04, 5.8))
        y += 1.0
    # ---- forecastle platform (z=ZF) with planks, black/ochre sides, stair gap at the back, low balustrade
    y = YF
    while y < STEM - 0.5:
        yc = y + 0.5; b = hw(yc)
        if b > 0.2:
            mb.box(M['hullb'], (0, yc, 7.0), (2 * b + 0.2, 1.04, 2.0)); mb.box(M['ochre'], (0, yc, 7.0), (2 * b + 0.24, 1.0, 0.3))
        y += 1.0
    k = 0; x = -3.7 + 0.13
    while x < 3.7:
        yl = ylim_for(abs(x)) if abs(x) < 3.699 else 20.0
        if yl > YF + 0.5: mb.box(M['deck1'] if k % 2 else M['deck2'], (x, (YF + yl) / 2, ZF - 0.02), (0.255, yl - YF, 0.06))
        x += 0.26; k += 1
    for xx in np.arange(-3.4, 3.5, 0.45):
        if abs(xx) < 0.75 or abs(xx) > hw(YF) - 0.2: continue
        mb.box(M['oak'], (xx, YF + 0.1, ZF + 0.45), (0.09, 0.09, 0.9))
    for (a, b_) in ((-3.7, -0.75), (0.75, 3.7)): mb.box(M['cap'], ((a + b_) / 2, YF + 0.1, ZF + 0.93), (b_ - a, 0.16, 0.1))
    for st in range(3): mb.box(M['deck1'], (0, YF - 0.3 - 0.3 * st, ZF - 0.6 - 0.6 * st), (1.3, 0.5, 0.1))
    gun_y = [40.4, 43.4]; gun_yp = [42.3]
    for s, gy in ((1, gun_y), (-1, gun_yp)):               # low bulwark with gun ports, black + ochre band
        y = YF
        while y < STEM - 0.3:
            yc = y + 0.3; b = hw(yc)
            if b > 0.15 and not any(abs(yc - g) < 0.42 for g in gy):
                dy = hw(yc + 0.3) - hw(yc - 0.3); ang = math.atan2(-dy * s, 0.6)
                mb.box(M['hullb'], (s * (b - 0.04), yc, ZF + 0.25), (0.16, 0.66, 0.5), rz=ang); mb.box(M['ochre'], (s * (b - 0.04), yc, ZF + 0.63), (0.17, 0.66, 0.3), rz=ang); mb.box(M['hullb'], (s * (b - 0.04), yc, ZF + 0.84), (0.16, 0.66, 0.1), rz=ang)
            y += 0.6
        y = YF
        while y < STEM - 0.3:
            yc = y + 0.35; b = hw(yc); dy = hw(yc + 0.35) - hw(yc - 0.35)
            if b > 0.15: mb.box(M['cap'], (s * (b - 0.02), yc, ZF + 0.92), (0.3, 0.74, 0.1), rz=math.atan2(-dy * s, 0.7))
            y += 0.7
    mb.box(M['cap'], (0, STEM - 1.3, ZF + 0.92), (1.0, 0.3, 0.1))
    # ---- cannons on carriages (forecastle)
    def cannon(side, y):
        b = hw(y); s = side; zc = ZF + 0.62
        xo = s * (b - 0.1); xi = s * (b - 1.6)
        tube(mb, M['iron'], (xi, y, zc), (xo + s * 0.3, y, zc), 0.23, 0.15, 12)
        mb.ell(M['iron'], (xi - s * 0.12, y, zc), (0.17, 0.17, 0.17), (10, 8)); mb.cyl(M['iron'], (xo + s * 0.22, y, zc), 0.19, 0.08, axis='x', seg=12)
        for yy in (-0.3, 0.3): mb.box(M['carr'], ((xi + xo) / 2 - s * 0.05, y + yy, ZF + 0.3), (1.6, 0.14, 0.5))
        mb.box(M['carr'], (xi + s * 0.45, y, ZF + 0.45), (0.14, 0.6, 0.3)); mb.box(M['oak'], (xi - s * 0.55, y, ZF + 0.46), (0.5, 0.5, 0.06))
        for dx in (-0.35, 0.5):
            for yy in (-0.36, 0.36): mb.cyl(M['oak'], (s * (b - 0.9) + s * dx * 0.8, y + yy, ZF + 0.17), 0.17, 0.1, axis='y', seg=12)
        for yy in (-0.7, 0.7): mb.rod(M['rope'], (xi - s * 0.1, y, zc - 0.1), (s * (b - 0.2), y + yy, ZF + 0.8), 0.03, 0.03, 5)
        mb.rod(M['rope'], (xo, y, zc + 0.2), (s * b, y + 0.5, ZF + 0.8), 0.03, 0.03, 5)
    for g in gun_y: cannon(1, g)
    for g in gun_yp: cannon(-1, g)
    # ---- foreground deck furniture (forecastle): binnacle (wooden pedestal + brass hood), coils, bucket, lantern, barrels, capstan
    bx, by = 0.55, 39.3
    mb.box(M['oak'], (bx, by, ZF + 0.4), (0.55, 0.5, 0.8)); mb.box(M['cap'], (bx, by, ZF + 0.83), (0.62, 0.56, 0.06))
    mb.cyl(M['brass'], (bx, by, ZF + 0.95), 0.26, 0.2, seg=16, smooth=True); mb.ell(M['brass'], (bx, by, ZF + 1.05), (0.26, 0.26, 0.24), (16, 10)); mb.cyl(M['brass'], (bx, by, ZF + 0.87), 0.29, 0.05, seg=16)
    mb.ell(M['red'], (bx, by - 0.26, ZF + 0.95), (0.05, 0.02, 0.05), (6, 4))
    for (cx, cy, r, n) in [(-0.55, 39.5, 0.3, 3), (1.05, 39.0, 0.28, 3)]:
        for l in range(n): ring_xy(mb, M['rope'], (cx, cy, ZF + 0.06 + l * 0.1), r * (1 - 0.06 * l), 0.1, 0.1, 16)
        mb.cyl(M['rope'], (cx, cy, ZF + 0.06 + (n - 1) * 0.05), r * 0.8, 0.1 * n, seg=16)
    mb.cyl(M['oak'], (1.6, 39.1, ZF + 0.17), 0.17, 0.34, seg=12, r2=0.21); mb.cyl(M['iron'], (1.6, 39.1, ZF + 0.3), 0.21, 0.03, seg=12)      # bucket
    lx, ly = -0.1, 39.0                                                                    # lantern (emitter)
    mb.box(M['iron'], (lx, ly, ZF + 0.03), (0.22, 0.22, 0.06)); mb.box(M['iron'], (lx, ly, ZF + 0.4), (0.24, 0.24, 0.04))
    for dx, dy in ((-0.1, -0.1), (0.1, -0.1), (-0.1, 0.1), (0.1, 0.1)): mb.box(M['iron'], (lx + dx, ly + dy, ZF + 0.21), (0.025, 0.025, 0.36))
    lm = MB('flame'); lm.box(M['lamp'], (lx, ly, ZF + 0.2), (0.15, 0.15, 0.28)); lm.finish(shadow=False)
    for (bx2, by2) in [(-1.35, 40.2), (-1.0, 41.1)]:
        mb.ell(M['oak'], (bx2, by2, ZF + 0.45), (0.3, 0.3, 0.44), (14, 10))
        for z in (0.2, 0.45, 0.7): mb.cyl(M['iron'], (bx2, by2, ZF + z), 0.27, 0.035, seg=14)
    mb.cyl(M['cap'], (0.9, 44.6, ZF + 0.4), 0.25, 0.8, seg=10)                             # bitts
    # ---- waist guns behind (just visible not at all) skipped. Foremast (behind the camera) with its stays and jibs ahead
    mx, my = 0.2, 22.0
    tube(mb, M['mast'], (mx, my, DECK), (mx, my, 26), 0.52, 0.28, 12); tube(mb, M['mast'], (mx, my, 20), (mx, my, 40), 0.3, 0.16, 10)
    mb.box(M['mast'], (mx, my, 19.8), (3.0, 2.2, 0.22))
    for (zy, ln, r) in [(15.0, 13.0, 0.17), (26.6, 9.4, 0.13)]: tube(mb, M['mast'], (mx - ln / 2, my, zy), (mx + ln / 2, my, zy), r, r * 0.6, 8)
    sail_quad(mb, M, mx - 6.0, mx + 6.0, 8.8, 14.8, my + 0.6, 1.5)
    tube(mb, M['mast'], (0, 44.0, 9.4), (0, 62.0, 14.5), 0.2, 0.1, 10)                    # bowsprit
    mb.box(M['mast'], (0, 46.3, 9.9), (0.9, 0.5, 0.3))
    tube(mb, M['rig'], (mx, my, 40), (0, 61.0, 14.2), 0.045, 0.045, 4)                    # fore-topmast stay
    tube(mb, M['rig'], (mx, my, 33), (0, 56.0, 13.4), 0.045, 0.045, 4)
    tube(mb, M['rig'], (mx, my, 27), (0, 50.0, 12.0), 0.045, 0.045, 4)
    sail_tri(mb, M, (0, 60.5, 13.6), (0, 51.0, 11.8), (0, 55.5, 18.5), 1.1)                # outer jib
    sail_tri(mb, M, (0, 55.0, 12.8), (0, 48.6, 11.0), (0, 51.0, 17.5), 1.0)                # fore-topmast staysail
    sail_tri(mb, M, (0, 50.0, 11.8), (0, 46.6, 10.6), (0, 46.5, 16.5), 0.8)
    tube(mb, M['mast'], (-1.2, 52.0, 10.2), (1.2, 52.0, 10.2), 0.07, 0.07, 6)               # spritsail yard + sail
    sail_quad(mb, M, -1.7, 1.7, 7.0, 10.0, 52.3, 0.45, 6, 8)
    for s in (-1, 1):                                                                      # shrouds visible on the sides far away: skipped (behind camera); extra rigging overhead
        tube(mb, M['rig'], (s * 0.1, 62.0, 14.5), (s * 3.3, 44.0, ZF + 0.9), 0.04, 0.04, 4)   # bobstays/stay lines to the bow
    tube(mb, M['rig'], (0, 62.0, 14.3), (0, 45.5, 7.5), 0.04, 0.04, 4)
    mb.quad(M['red'], [(0, 61.9, 14.9), (0, 61.9, 14.3), (0, 59.0, 14.2), (0, 59.0, 14.9)])
    mb.finish()
    # ---- far dressing: green-headed headland with a pale beach and haze, tiny dark sail
    ib = MB('isle'); n = 48; X0i = 780
    for i in range(n):
        x0 = X0i + i * 7.0; x1 = x0 + 7.0
        f = lambda x: 70 * max(0, math.sin(math.pi * (x - X0i) / (n * 7.0))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 11.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))])
        ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    sb_ = MB('farsail'); sb_.quad(M['darksail'], [(430, 1500, 0.5), (456, 1500, 0.5), (448, 1500, 24), (434, 1500, 28)]); sb_.quad(M['darksail'], [(425, 1500, 0.5), (455, 1500, 0.5), (455, 1500, 3), (425, 1500, 3)]); sb_.finish(shadow=False)
    cm = MB('cards')
    if not os.environ.get('NOCARDS'): card(cm, M['grey'], 0.35, 41.3, w=0.55, z0=ZF); card(cm, M['grey'], 1.05, 42.0, w=0.55, z0=ZF); cm.finish()
    if not os.environ.get('NOSEA'): build_sea(P)
    clouds(P)

# ---------------------------------------------------------------- the sea (v2): long smooth swells built per camera pixel, layered colour, contour foam streaks, bow wave + V-wake, one narrow glitter path
def build_sea(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.12, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.18
    NU, NV = 440, 800
    uu = np.linspace(-1.12, 1.12, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    sdep = np.abs(ray[..., 2]) / np.linalg.norm(ray, axis=-1)
    rng = np.random.RandomState(7)
    th0 = math.radians(95); waves = []
    # (wavelength, amplitude): long rolling swells; steepness 2*pi*A/L about 0.07-0.1
    spec = [(70, 1.0), (42, .62), (26, .4), (16, .22), (10.5, .13), (6.5, .075), (4.2, .04)]
    for (L, A) in spec:
        a = th0 + rng.uniform(-0.55, 0.55); waves.append((L, A, a, rng.uniform(0, 6.28)))
    rip = [(0.9, 0.012), (0.6, 0.008), (0.4, 0.006), (0.27, 0.004)]
    rip = [(L, A, th0 + rng.uniform(-1.2, 1.2), rng.uniform(0, 6.28)) for (L, A) in rip]
    fpx = t * (2 * hx / 720.0) * 1.1
    h = np.zeros_like(px); gx = np.zeros_like(px); gy = np.zeros_like(px)
    wm = np.zeros_like(px); wgx = np.zeros_like(px); wgy = np.zeros_like(px); norm_m = 0.0
    gsx = np.zeros_like(px); gsy = np.zeros_like(px)
    WARP = 3.2 * np.sin(0.021 * px + 1.3 * np.sin(0.03 * py)) + 2.4 * np.sin(0.027 * py + 1.1 * np.sin(0.02 * px)) + 1.6 * np.sin(0.06 * px + 0.04 * py)
    wpx = np.maximum(fpx / np.maximum(sdep, 0.05), 0.02) * 1.6
    brk = 0.5 + 0.5 * np.sin(px * 0.11 + 1.7 * np.sin(py * 0.06)) * np.sin(py * 0.09 + 0.9 * np.sin(px * 0.05))
    lines = np.zeros_like(px)
    for (L, A, a, ph) in waves:
        k = 2 * math.pi / L; kx = k * math.cos(a); ky = k * math.sin(a)
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 5.0) / 9.0, 0, 1)
        th = kx * px + ky * py + ph + WARP; s = np.sin(th); cs = np.cos(th)
        if 9 <= L <= 30:
            lines = np.maximum(lines, np.clip(1 - (1 - s) / np.maximum((k * wpx) ** 2 / 2, 1e-5), 0, 1) ** 1.2 * (0.9 if L < 20 else 0.7))
        q = 0.5 + 0.5 * s; hh = A * (2 * q ** 1.6 - 1.0); dh = A * 2 * 1.6 * q ** 0.6 * 0.5 * cs * k
        h += hh * fade; gx += dh * math.cos(a) * fade; gy += dh * math.sin(a) * fade
        if 6 <= L <= 30:
            wm += hh / A * fade; wgx += dh / A * math.cos(a) * fade; wgy += dh / A * math.sin(a) * fade; norm_m += 1
    for (L, A, a, ph) in rip:
        k = 2 * math.pi / L; th = k * (math.cos(a) * px + math.sin(a) * py) + ph; dh = A * k * np.cos(th)
        gsx += dh * math.cos(a) * 1.5; gsy += dh * math.sin(a) * 1.5
    far = np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    h *= far
    # bow wave: a raised foamy mound ahead of the stem
    sx, sy = 0.0, STEM + 3.0
    h += 0.55 * np.exp(-(((px - sx) / 2.2) ** 2 + ((py - sy) / 3.2) ** 2))
    wmn = wm / max(norm_m, 1); gm = np.sqrt(wgx ** 2 + wgy ** 2) / max(norm_m, 1) + 1e-4
    # smooth contour foam streaks: constant ~2.5 px wide, broken up by long noise, fading with distance
    lines *= np.clip((brk - 0.45) / 0.2, 0, 1) * np.clip(1 - t / 900, 0, 1)
    crest = np.clip((wmn - 0.1) / 0.7, 0, 1) * 0.55
    # hull wash, V-wake arms and bow foam
    hh_ = hw(np.clip(py, -6, STEM)); d_hull = np.abs(px) - (hh_ + 0.9); d_hull = np.where((py > -6) & (py < STEM + 1), d_hull, 9)
    wash = np.exp(-np.maximum(d_hull, 0) / 1.1) * (d_hull < 3) * (0.6 + 0.4 * np.sin(py * 0.22 + px * 0.3)) * 0.6
    dback = np.maximum(STEM - py, 0.0)
    arm = np.zeros_like(px)
    for off in (2.2, 4.8, 7.6):                    # V arms flaring back from the bow, thin broken streaks
        dd = np.abs(np.abs(px) - (hh_ + 0.9 + off * (0.35 + 0.5 * np.clip(dback / 30.0, 0, 1)))); arm = np.maximum(arm, np.clip(1 - dd / (0.4 + 0.08 * off), 0, 1) ** 1.0 * np.clip(1 - dback / (22.0 + 8 * off), 0, 1) * (py < STEM + 4))
    arm *= (0.6 + 0.4 * np.sin(py * 0.25 + np.abs(px) * 0.3) ** 2)
    bow = np.exp(-(((px - sx) / 4.6) ** 2 + ((py - sy) / 6.5) ** 2)) * (0.65 + 0.35 * np.sin(px * 0.6) * np.sin(py * 0.5 + 1.0))
    foam = np.clip(np.maximum.reduce([lines * 0.9, wash * 0.85, arm * 1.0, bow * 1.3]), 0, 1)
    # colour distance bands
    d_mid = np.clip((t - 14.0) / 120.0, 0, 1); haze = np.clip((t - 250.0) / 2400.0, 0, 1) ** 0.8
    # glitter: one narrow path under the (virtual) sun azimuth
    nx_ = -(gx + gsx); ny_ = -(gy + gsy); nz_ = np.ones_like(px); nl = np.sqrt(nx_ ** 2 + ny_ ** 2 + nz_ ** 2); nx_ /= nl; ny_ /= nl; nz_ /= nl
    vx = px - loc[0]; vy = py - loc[1]; vz = h - loc[2]; vl = np.sqrt(vx ** 2 + vy ** 2 + vz ** 2); vx /= vl; vy /= vl; vz /= vl
    dn = vx * nx_ + vy * ny_ + vz * nz_
    Rx = vx - 2 * dn * nx_; Ry = vy - 2 * dn * ny_; Rz = vz - 2 * dn * nz_
    se = math.radians(P['glit_el']); sa = math.radians(P['glit_az'])
    S = np.array([math.sin(sa) * math.cos(se), math.cos(sa) * math.cos(se), math.sin(se)])
    dd = Rx * S[0] + Ry * S[1] + Rz * S[2]
    glit = np.clip((dd - P['glit_lo']) / (P['glit_hi'] - P['glit_lo']), 0, 1) ** 1.5
    az = np.arctan2(px - loc[0], py - loc[1]); daz = az - sa
    glit *= np.exp(-(daz / (0.045 + 0.00004 * t)) ** 2) * np.clip(1 - t / 2200, 0.2, 1) * (1 - 0.6 * foam)
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    quads = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nl_ = len(quads); me.loops.add(nl_ * 4); me.polygons.add(nl_)
    me.loops.foreach_set('vertex_index', quads.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nl_) * 4).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nl_, 4, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nl_, dtype=bool))
    for name, arr in (('foam', foam), ('crest', crest), ('haze', haze), ('dmid', d_mid), ('glit', glit)):
        at = me.attributes.new(name, 'FLOAT', 'POINT'); at.data.foreach_set('value', arr.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.6; bs.inputs['Specular IOR Level'].default_value = 0.0
    def attr(n):
        a = N('ShaderNodeAttribute'); a.attribute_type = 'GEOMETRY'; a.attribute_name = n; return a.outputs['Fac']
    def mix(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    col = mix(hexc(P['sea_deep']), hexc(P['sea_mid']), attr('dmid'))
    col = mix(col, hexc(P['sea_crest']), attr('crest'))
    col = mix(col, hexc(P['sea_haze']), attr('haze'))
    col = mix(col, hexc('#f4f8f4'), attr('foam'))
    L(col, bs.inputs['Base Color'])
    gm_ = N('ShaderNodeMath'); gm_.operation = 'MULTIPLY'; gm_.inputs[1].default_value = P.get('glit_k', 5.0); L(attr('glit'), gm_.inputs[0])
    bs.inputs['Emission Color'].default_value = hexc('#fff2cc'); L(gm_.outputs[0], bs.inputs['Emission Strength'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)

PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#a9c6e6'), (0.5, '#9dbfe6'), (0.58, '#7ea8e2'), (0.78, '#5b88d6'), (1.0, '#4a78cd')], sky_k=1.0,
    key=(1.0, 0.88, 0.7, 7.5), key_dir=kdir(22, 46), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.9), samples=80, dbounce=1,
    cloud=('#fffaf0', '#8c9ce8'), cloud_diffuse=True, cloud_z=(70, 170), ncloud=8, cloud_seed=4, cloud_scale=0.8,
    sea_deep='#0a4452', sea_mid='#2a8a8c', sea_crest='#48aaa0', sea_haze='#9cbccb',
    glit_az=20, glit_el=18, glit_lo=0.9975, glit_hi=0.9996, glit_k=4.0,
    cam=dict(loc=(1.2, 37.0, 12.4), look=(0.5, 61.5, -0.5), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world(P)
