# ================================================================== v6: HERO SHIP seen from the sea (low camera, three-quarter view, bow wave sheet, lacy wake, smooth cumulus)
import numpy as _np
YS, YB = -21.0, 21.0; BH = 5.6                       # stern / bow at the waterline (local y), max half beam
def ss(a, b, x):
    t = np.clip((np.asarray(x, dtype=np.float64) - a) / (b - a), 0.0, 1.0); return t * t * (3 - 2 * t)
def w_wl(t):
    t = np.asarray(t, dtype=np.float64)
    bow = BH * np.maximum(0.0, 1 - np.maximum(0.0, (t - 0.5) / 0.5) ** 2.3) ** 0.9
    ster = BH * (1 - 0.42 * np.maximum(0.0, (0.5 - t) / 0.5) ** 2)
    return np.where(t > 0.5, bow, ster)
def ztop(t):
    t = np.asarray(t, dtype=np.float64)
    return 6.2 + 2.3 * ss(0.30, 0.20, t) + 0.9 * ss(0.82, 0.92, t) + 0.5 * (2 * t - 1) ** 2
def hull_y(t, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return a + np.asarray(t) * (b - a)
def hull_t(y, z):
    zc = np.clip(z, 0, None) / 7.0; a = YS - 1.6 * zc; b = YB + 3.2 * zc; return (np.asarray(y) - a) / (b - a)
def hull_x(t, z):
    t = np.asarray(t, dtype=np.float64); z = np.asarray(z, dtype=np.float64); zp = np.clip(z, 0, None)
    flare = 0.32 * ss(0.5, 1.0, t); tumble = 0.16 * (1 - ss(0.5, 1.0, t)) + 0.06
    up = 1 + flare * zp / 6.0 - tumble * (zp / 7.0) ** 2
    dn = np.sqrt(np.clip(1 - (np.clip(-z, 0, None) / 2.45) ** 2, 0.0, 1.0))
    return w_wl(t) * np.where(z >= 0, up, dn)
def deck_z(y): return float(ztop(np.clip((y - YS) / (YB - YS), 0, 1))) - 0.95

def vnoise2(x, y, seed=1):
    G = np.random.RandomState(seed).rand(64, 64).astype(np.float32)
    x = np.asarray(x, dtype=np.float32); y = np.asarray(y, dtype=np.float32)
    xi = np.floor(x).astype(np.int32); yi = np.floor(y).astype(np.int32); fx = x - xi; fy = y - yi
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    a = G[xi & 63, yi & 63]; b = G[(xi + 1) & 63, yi & 63]; c = G[xi & 63, (yi + 1) & 63]; d = G[(xi + 1) & 63, (yi + 1) & 63]
    return a * (1 - fx) * (1 - fy) + b * fx * (1 - fy) + c * (1 - fx) * fy + d * fx * fy
def fbm2(x, y, seed=1, octs=3):
    s = 0.0; a = 1.0; tot = 0.0; f = 1.0
    for i in range(octs):
        s = s + a * vnoise2(x * f + 17.0 * i, y * f + 31.0 * i, seed + i); tot += a; a *= 0.5; f *= 2.03
    return s / tot

def mesh_obj(name, verts, faces, mats, midx=None, smooth=True):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(v) for v in verts], [], [tuple(f) for f in faces]); me.update()
    for m in mats: me.materials.append(m)
    for i, p in enumerate(me.polygons):
        p.use_smooth = smooth
        if midx is not None: p.material_index = int(midx[i])
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); return ob

def S6(): return SHIP6
def loc2w(p):
    s = SHIP6; ph = math.radians(180.0 - s['theta']); x, y, z = p
    return Vector((s['cx'] + x * math.cos(ph) - y * math.sin(ph), s['cy'] + x * math.sin(ph) + y * math.cos(ph), z))
SHIP6 = dict(cx=4.5, cy=67.0, theta=36.0)

def ship6_mats():
    M = ship_mats()
    M['hull6'] = mat('hull6', '#2c2824', '#3a342d', scale=2.5, aniso=(0.25, 0.25, 4.5), contrast=1.2)
    M['ochre6'] = mat('ochre6', '#d89a34', '#c4832a', scale=3, aniso=(0.3, 0.3, 2.0))
    M['cap6'] = mat('cap6', '#2e2824', '#403830', scale=3)
    M['port6'] = mat('port6', '#241410', '#3a1c16', scale=3)
    M['deck6'] = mat('deck6', '#b48a50', '#a07a40', scale=3, aniso=(0.12, 1, 1), contrast=1.4)
    M['canv'] = mat('canv', '#e8dcc0', '#dccfae', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a0', emit_k=0.10)
    M['canv2'] = mat('canv2', '#e2d5b4', '#d6c8a4', scale=2.2, aniso=(1.3, 1, 0.8), contrast=0.8, emit='#ffe2a0', emit_k=0.08)
    M['gold'] = mat('gold', '#d8a840', '#c08c30', scale=4, sheen=0.3)
    M['pen'] = mat('pen', '#c0392f', '#a8302a', scale=4)
    M['rig6'] = mat('rig6', '#2c2430', '#40343e', scale=3)
    return M

def build_hull6(M):
    nt = 130; T = np.linspace(0.0, 1.0, nt)
    base = [-2.35, -1.6, -0.9, -0.35, 0.0, 0.5, 1.2, 2.0, 3.1, 3.6, 4.4, 5.3, 5.7]
    zt = ztop(T)
    Z = np.zeros((nt, len(base) + 3))
    Z[:, :len(base)] = np.array(base)[None, :]; Z[:, len(base)] = 5.7 + (zt - 5.7) * 0.5; Z[:, len(base) + 1] = zt; Z[:, len(base) + 2] = zt + 0.16
    Kc = Z.shape[1]; Tm = T[:, None] * np.ones((1, Kc))
    X = hull_x(Tm, Z); Y = hull_y(Tm, Z)
    X[:, -1] = hull_x(T, zt) + 0.12; Y[:, -1] = hull_y(T, zt) + 0.0; Y[:, -2] = hull_y(T, zt)
    verts = []; faces = []; midx = []
    for s in (-1, 1):
        for i in range(nt):
            for j in range(Kc): verts.append((s * X[i, j], Y[i, j], Z[i, j]))
    ctr = np.array([0, 0, 2.5])
    for si, s in enumerate((-1, 1)):
        off = si * nt * Kc
        for i in range(nt - 1):
            for j in range(Kc - 1):
                a = off + i * Kc + j; b = off + (i + 1) * Kc + j; c = off + (i + 1) * Kc + j + 1; d = off + i * Kc + j + 1
                zm = 0.5 * (Z[i, j] + Z[i, j + 1])
                if j == Kc - 2: mi = 2
                elif (3.1 <= zm <= 3.6) or (5.3 <= zm <= 5.7): mi = 1
                else: mi = 0
                if s == 1: faces.append((a, b, c, d))
                else: faces.append((d, c, b, a))
                midx.append(mi)
    # transom (stern) and flat keel closure
    off0 = 0; off1 = nt * Kc
    for j in range(Kc - 1):
        faces.append((off0 + j, off1 + j, off1 + j + 1, off0 + j + 1)); midx.append(1 if j == Kc - 2 else 0)
    ob = mesh_obj('ship6_hull', verts, faces, [M['hull6'], M['ochre6'], M['cap6']], midx, True)
    # deck fill (barely visible from the low camera, closes the hull for shadows)
    dv = []; df = []
    for i in range(nt):
        zd = zt[i] - 0.95; bd = hull_x(T[i], zd) * 0.97; yd = hull_y(T[i], zd)
        for xx in (-1.0, -0.33, 0.33, 1.0): dv.append((xx * bd, yd, zd))
    for i in range(nt - 1):
        for c in range(3): a = i * 4 + c; df.append((a, a + 1, a + 5, a + 4))
    mesh_obj('ship6_deck', dv, df, [M['deck6']], None, False)
    # gun ports (two rows) as flat frames on the hull side, ochre frame + dark port
    mb = MB('ship6_ports')
    def pquad(m, y0, y1, z0, z1, s, off):
        pts = []
        for (yy, zz) in ((y0, z0), (y1, z0), (y1, z1), (y0, z1)):
            t = float(hull_t(yy, zz)); pts.append((s * (float(hull_x(t, zz)) + off), yy, zz))
        mb.quad(m, pts)
    for zc in (2.55, 4.45):
        y = -15.2
        while y < 16.0:
            for s in (-1, 1):
                pquad(M['ochre6'], y - 0.58, y + 0.58, zc - 0.50, zc + 0.46, s, 0.03)
                pquad(M['port6'], y - 0.44, y + 0.44, zc - 0.38, zc + 0.34, s, 0.06)
            y += 2.4
    mb.finish()
    return ob

def sq_sail(M, name, my, zb, zt_, hw_top, hw_foot, belly, nx=22, ny=16, yoff=0.55):
    def PF(i, j):
        u = 2.0 * i / nx - 1.0; v = j / ny
        hwv = hw_foot + (hw_top - hw_foot) * v
        by = belly * (1 - abs(u) ** 2.3) ** 0.8 * math.sin(math.pi * (0.07 + 0.86 * v)) ** 0.85 * (1 + 0.05 * math.sin(u * 8.0 + v * 3.0))
        z = zb + (zt_ - zb) * v + 0.05 * (zt_ - zb) * (1 - u * u) * (1 - v) ** 2
        return (u * hwv, my + yoff + by, z)
    return sail_obj(M, name, PF, nx, ny, 0.04)

def spanker(M, name, my, z0, H):
    A = Vector((0, my - 0.7, z0 + 0.52 * H)); B = Vector((0, my - 8.6, z0 + 0.60 * H)); C = Vector((0, my - 11.8, z0 + 0.09 * H)); D = Vector((0, my - 0.7, z0 + 0.09 * H))
    nx, ny = 14, 12
    def PF(i, j):
        u = i / nx; v = j / ny
        P = (D * (1 - u) + C * u) * (1 - v) + (A * (1 - u) + B * u) * v
        b = -1.6 * math.sin(math.pi * u) ** 0.8 * math.sin(math.pi * (0.1 + 0.8 * v))
        return (P.x + b, P.y, P.z)
    return sail_obj(M, name, PF, nx, ny, 0.04)

def jib(M, name, T, C, Hd, bulge, n=10, m=10):
    T = Vector(T); C = Vector(C); Hd = Vector(Hd)
    def PF(i, j):
        v = j / n; L = T + (Hd - T) * v; Rr = C + (Hd - C) * v; u = i / m; p = L + (Rr - L) * u
        b = -bulge * math.sin(math.pi * u) * math.sin(math.pi * min(1, 0.1 + 0.9 * v)) * (1 - 0.4 * v)
        return (p.x + b, p.y, p.z)
    return sail_obj(M, name, PF, m, n, 0.04)

def rigging6(mb, M, my, z0, H, s_sides=(-1, 1), nshr=5):
    top = z0 + 0.41 * H
    for s in s_sides:
        for k in range(nshr):
            yy = my - 1.8 + 0.9 * k; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
            a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * k, top))
            mb.rod(M['rig6'], a, b, 0.05, 0.04, 4)
        for q in np.linspace(0.08, 0.92, 15):
            for k in range(nshr - 1):
                def pt(kk):
                    yy = my - 1.8 + 0.9 * kk; tt = float(hull_t(yy, 4.4)); bx = s * (float(hull_x(tt, 4.4)) + 0.35)
                    a = Vector((bx, yy, deck_z(yy) - 0.7)); b = Vector((s * 1.0, my - 0.7 + 0.35 * kk, top)); return a + (b - a) * q
                mb.rod(M['rig6'], pt(k), pt(k + 1), 0.026, 0.026, 4)
        for k in range(3):           # topmast shrouds
            mb.rod(M['rig6'], Vector((s * 0.9, my - 0.6 + 0.4 * k, top + 0.2)), Vector((s * 0.12, my - 0.3, z0 + 0.77 * H)), 0.035, 0.03, 4)
        mb.rod(M['rig6'], Vector((s * 0.2, my - 0.4, z0 + 0.77 * H)), Vector((s * (float(hull_x(float(hull_t(my - 7.0, 4.4)), 4.4)) + 0.4), my - 7.0, deck_z(my - 7.0) - 0.6)), 0.04, 0.035, 4)    # backstay

def mast6(mb, M, my, H, yards):
    z0 = deck_z(my)
    tube(mb, M['mast'], (0, my, z0 - 0.5), (0, my, z0 + 0.52 * H), 0.58, 0.36, 12)
    tube(mb, M['mast'], (0, my, z0 + 0.40 * H), (0, my, z0 + 0.80 * H), 0.30, 0.19, 10)
    tube(mb, M['mast'], (0, my, z0 + 0.76 * H), (0, my, z0 + H), 0.17, 0.08, 8)
    mb.box(M['mast'], (0, my - 0.2, z0 + 0.41 * H), (3.2, 2.6, 0.22)); mb.box(M['rig6'], (0, my - 0.2, z0 + 0.41 * H - 0.13), (3.3, 2.7, 0.04))
    for (fz, ln, r) in yards:
        zy = z0 + fz * H; tube(mb, M['mast'], (-ln / 2, my, zy), (ln / 2, my, zy), r, r * 0.55, 8)
        for s in (-1, 1): mb.rod(M['rig6'], (s * ln / 2, my, zy), (s * 0.4, my, zy + 0.18 * H * (0.8 if fz < 0.6 else 0.55)), 0.025, 0.025, 4)
    # pennant at the truck
    mb.quad(M['pen'], [(0, my, z0 + H), (0.0, my - 5.5, z0 + H - 0.2), (0.0, my - 5.2, z0 + H - 0.75), (0, my, z0 + H - 0.5)])
    mb.quad(M['pen'], [(0, my, z0 + H - 0.5), (0.0, my - 5.2, z0 + H - 0.75), (0.0, my - 5.5, z0 + H - 0.2), (0, my, z0 + H)])
    rigging6(mb, M, my, z0, H)

def build_ship6(P):
    before = set(bpy.data.objects)
    M = ship6_mats(); mb = MB('ship6'); sc = bpy.context.scene
    build_hull6(M)
    # quarter gallery + stern lantern + beakhead + figurehead
    for s in (-1, 1):
        mb.box(M['ochre6'], (s * 4.3, -16.6, 7.9), (1.4, 4.0, 3.2)); mb.box(M['hull6'], (s * 4.3, -16.6, 9.62), (1.5, 4.1, 0.2))
        for k in range(3): mb.box(M['port6'], (s * 5.04, -18.0 + 1.4 * k, 8.0), (0.06, 0.8, 1.2))
    mb.box(M['gold'], (0, -21.2, 10.2), (1.2, 1.2, 1.8)); mb.cyl(M['gold'], (0, -21.2, 11.3), 0.5, 0.5, seg=10)
    tube(mb, M['gold'], (0, YB + 2.2, 4.6), (0, YB + 4.8, 5.8), 0.36, 0.22, 8); mb.ell(M['gold'], (0, YB + 5.0, 5.9), (0.3, 0.55, 0.38), (10, 6))
    for s in (-1, 1): tube(mb, M['ochre6'], (s * 0.15, YB + 1.0, 4.9), (s * 0.5, YB + 4.8, 5.4), 0.1, 0.07, 6)
    # three masts: fore, main, mizzen
    mast6(mb, M, 11.5, 36.0, [(0.27, 15.5, 0.20), (0.55, 12.2, 0.16), (0.77, 8.8, 0.12), (0.91, 5.8, 0.09)])
    mast6(mb, M, -0.5, 40.0, [(0.27, 17.8, 0.22), (0.55, 13.6, 0.17), (0.77, 9.8, 0.13), (0.91, 6.4, 0.09)])
    mast6(mb, M, -12.5, 29.0, [(0.27, 12.5, 0.17), (0.52, 10.0, 0.13), (0.74, 7.2, 0.10)])
    # square sails (head on the yard, foot above the deck), billowing forward
    for (nm, my, H, spec) in (('fore', 11.5, 36.0, [(0.27, 0.07, 7.2, 8.0, 2.0), (0.55, 0.31, 5.6, 6.4, 1.7), (0.77, 0.58, 4.0, 4.5, 1.2), (0.91, 0.80, 2.6, 3.0, 0.7)]),
                              ('main', -0.5, 40.0, [(0.27, 0.07, 8.0, 8.9, 2.3), (0.55, 0.31, 6.2, 7.0, 1.9), (0.77, 0.58, 4.4, 4.9, 1.3), (0.91, 0.80, 2.8, 3.2, 0.8)]),
                              ('miz', -12.5, 29.0, [(0.52, 0.30, 4.8, 5.4, 1.4), (0.74, 0.55, 3.4, 3.8, 1.0)])):
        z0 = deck_z(my)
        for k, (fy, ff, hwt, hwf, bel) in enumerate(spec): sq_sail(M, 'ship6_sail_%s%d' % (nm, k), my, z0 + ff * H, z0 + fy * H, hwt, hwf, bel)
    spanker(M, 'ship6_spanker', -12.5, deck_z(-12.5), 29.0)
    # bowsprit, jib boom, spritsail yard, stays, jibs
    tube(mb, M['mast'], (0, YB - 4.0, 5.2), (0, YB + 12.5, 11.6), 0.42, 0.20, 10); tube(mb, M['mast'], (0, YB + 12.0, 11.4), (0, YB + 18.5, 13.6), 0.16, 0.08, 8)
    z0f = deck_z(11.5); z0m = deck_z(-0.5)
    fore_top = Vector((0, 11.5, z0f + 0.80 * 36.0)); fore_t2 = Vector((0, 11.5, z0f + 0.45 * 36.0)); main_top = Vector((0, -0.5, z0m + 0.80 * 40.0)); miz_top = Vector((0, -12.5, deck_z(-12.5) + 0.78 * 29.0))
    for (a, b) in ((Vector((0, YB + 18.5, 13.6)), fore_top), (Vector((0, YB + 12.3, 11.6)), fore_t2), (fore_top, main_top), (fore_t2, Vector((0, -0.5, z0m + 0.45 * 40.0))), (main_top, miz_top), (Vector((0, -0.5, z0m + 0.45 * 40.0)), Vector((0, -12.5, deck_z(-12.5) + 0.42 * 29.0)))):
        mb.rod(M['rig6'], a, b, 0.05, 0.05, 4)
    jib(M, 'ship6_jib1', (0, YB + 18.0, 13.5), (0, YB + 11.0, 9.2), (0, 31.2, z0f + 0.78 * 36.0), 1.5)
    jib(M, 'ship6_jib2', (0, YB + 11.6, 11.4), (0, YB + 4.6, 7.8), (0, 28.6, z0f + 0.52 * 36.0), 1.3)
    jib(M, 'ship6_jib3', (0, YB + 4.0, 7.4), (0, YB - 3.0, 6.9), (0, 24.0, z0f + 0.40 * 36.0), 1.0)
    # square spritsail under the bowsprit
    tube(mb, M['mast'], (-3.4, YB + 4.6, 8.0), (3.4, YB + 4.6, 8.0), 0.12, 0.08, 6)
    sq_sail(M, 'ship6_sprit', YB + 4.6, 5.0, 8.0, 3.0, 3.3, 0.9, 10, 8, 0.2)
    mb.finish()
    for o in set(bpy.data.objects) - before: o.parent = None
    return M, before

def sea_swell_params():
    rng = np.random.RandomState(3); sw = []; ch = []
    for (L, A, deg) in [(52, 0.85, 80), (31, 0.55, 112), (19, 0.34, 70)]:
        a = math.radians(deg + rng.uniform(-8, 8)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28); sw.append((k, math.cos(a), math.sin(a), ph, A))
    for (L, A) in [(7.4, .10), (4.8, .06), (3.1, .04), (2.0, .026), (1.3, .016)]:
        a = math.radians(80 + rng.uniform(-50, 50)); k = 2 * math.pi / L; ph = rng.uniform(0, 6.28); ch.append((k, math.cos(a), math.sin(a), ph, A, L))
    return sw, ch
def swell_h(px, py):
    sw, _ = sea_swell_params(); h = np.zeros_like(np.asarray(px, dtype=np.float64))
    for (k, ca, sa, ph, A) in sw:
        q = 0.5 + 0.5 * np.sin(k * (ca * px + sa * py) + ph); h = h + A * (2 * q ** 1.5 - 1.0)
    return h

def catmull(Pc, n):
    Pc = np.asarray(Pc, dtype=np.float64); Pp = np.vstack([Pc[0] * 2 - Pc[1], Pc, Pc[-1] * 2 - Pc[-2]]); m = len(Pp) - 3; out = []
    for k in range(n):
        u = k / (n - 1) * m; i = min(int(u), m - 1); f = u - i; p0, p1, p2, p3 = Pp[i:i + 4]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * f + (2 * p0 - 5 * p1 + 4 * p2 - p3) * f * f + (-p0 + 3 * p1 - 3 * p2 + p3) * f ** 3))
    return np.array(out)

def foam_sheet_mat(name, lacy=1.0, alpha_k=0.97):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeAttribute'); sp.attribute_type = 'GEOMETRY'; sp.attribute_name = 'sp'
    hz = N('ShaderNodeAttribute'); hz.attribute_type = 'GEOMETRY'; hz.attribute_name = 'hz'
    ln = N('ShaderNodeAttribute'); ln.attribute_type = 'GEOMETRY'; ln.attribute_name = 'lp'
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 7.0; nz.inputs['Roughness'].default_value = 0.62; L(tc.outputs['Object'], nz.inputs['Vector'])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 7.0; nz2.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz2.inputs['Vector'])
    # lacy outer edge: s + (noise-.5)*k - c  -> 0..1
    a1 = N('ShaderNodeMath'); a1.operation = 'SUBTRACT'; a1.inputs[1].default_value = 0.5; L(nz.outputs['Fac'], a1.inputs[0])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; a2.inputs[1].default_value = 0.62 * lacy; L(a1.outputs[0], a2.inputs[0])
    a3 = N('ShaderNodeMath'); a3.operation = 'ADD'; L(sp.outputs['Fac'], a3.inputs[0]); L(a2.outputs[0], a3.inputs[1])
    a4 = N('ShaderNodeMath'); a4.operation = 'SUBTRACT'; a4.inputs[1].default_value = 0.10; L(a3.outputs[0], a4.inputs[0])
    am = N('ShaderNodeMapRange'); am.inputs['From Min'].default_value = 0.0; am.inputs['From Max'].default_value = 0.16; L(a4.outputs[0], am.inputs['Value'])
    # fine speckle holes in the thin parts
    sk = N('ShaderNodeMapRange'); sk.inputs['From Min'].default_value = 0.30; sk.inputs['From Max'].default_value = 0.46; L(nz2.outputs['Fac'], sk.inputs['Value'])
    sk2 = N('ShaderNodeMath'); sk2.operation = 'MAXIMUM'; L(sk.outputs['Result'], sk2.inputs[0]); L(sp.outputs['Fac'], sk2.inputs[1])
    # lip end / tail fade
    le = N('ShaderNodeMath'); le.operation = 'SUBTRACT'; le.inputs[0].default_value = 1.0; L(sp.outputs['Fac'], le.inputs[1])
    le2 = N('ShaderNodeMapRange'); le2.inputs['From Min'].default_value = 0.0; le2.inputs['From Max'].default_value = 0.05; L(le.outputs[0], le2.inputs['Value'])
    tf = N('ShaderNodeMapRange'); tf.inputs['From Min'].default_value = 1.0; tf.inputs['From Max'].default_value = 0.82; L(ln.outputs['Fac'], tf.inputs['Value'])
    al = N('ShaderNodeMath'); al.operation = 'MULTIPLY'; L(am.outputs['Result'], al.inputs[0]); L(le2.outputs['Result'], al.inputs[1])
    al2 = N('ShaderNodeMath'); al2.operation = 'MULTIPLY'; L(al.outputs[0], al2.inputs[0]); L(tf.outputs['Result'], al2.inputs[1])
    al3 = N('ShaderNodeMath'); al3.operation = 'MULTIPLY'; L(al2.outputs[0], al3.inputs[0]); L(sk2.outputs[0], al3.inputs[1])
    al4 = N('ShaderNodeMath'); al4.operation = 'MULTIPLY'; al4.inputs[1].default_value = alpha_k; al4.use_clamp = True; L(al3.outputs[0], al4.inputs[0])
    # colour: white top, aqua toward the water; underside turquoise
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; cm.inputs[6].default_value = hexc('#9fe0da'); cm.inputs[7].default_value = hexc('#fbfefc'); L(hz.outputs['Fac'], cm.inputs[0])
    cb = N('ShaderNodeMix'); cb.data_type = 'RGBA'; cb.inputs[7].default_value = hexc('#22b5ad'); L(cm.outputs[2], cb.inputs[6]); L(geo.outputs['Backfacing'], cb.inputs[0])
    es = N('ShaderNodeMath'); es.operation = 'MULTIPLY_ADD'; es.inputs[1].default_value = 0.55; es.inputs[2].default_value = 0.16; L(geo.outputs['Backfacing'], es.inputs[0])
    bs.inputs['Roughness'].default_value = 0.55; bs.inputs['Specular IOR Level'].default_value = 0.2
    L(cb.outputs[2], bs.inputs['Base Color']); L(cb.outputs[2], bs.inputs['Emission Color']); L(es.outputs[0], bs.inputs['Emission Strength'])
    L(al4.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(bs.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); return m

def bow_wave6(P):
    rr = np.random.RandomState(11)
    ts = np.linspace(0.58, 1.0, 100); xs = w_wl(ts); ys = YS + ts * (YB - YS)
    port = np.stack([-xs, ys], 1); d = np.diff(port, axis=0); d = np.vstack([d, d[-1]]); d /= np.linalg.norm(d, axis=1, keepdims=True); npt = np.stack([-d[:, 1], d[:, 0]], 1)
    stb = np.stack([xs[::-1], ys[::-1]], 1); d2 = np.diff(stb, axis=0); d2 = np.vstack([d2, d2[-1]]); d2 /= np.linalg.norm(d2, axis=1, keepdims=True); nst = np.stack([-d2[:, 1], d2[:, 0]], 1)
    seg = np.linalg.norm(np.diff(port, axis=0), axis=1); lp = -np.concatenate([np.cumsum(seg[::-1])[::-1], [0.0]])      # arclength from the tip, negative on the port side
    a0 = math.atan2(npt[-1, 1], npt[-1, 0]); a1 = math.atan2(nst[0, 1], nst[0, 0])
    fan = [(YB * 0 + 0.0, YB) for _ in range(14)]; fan_n = [(math.cos(a0 + (a1 - a0) * k / 13.0), math.sin(a0 + (a1 - a0) * k / 13.0)) for k in range(14)]
    Pp = np.vstack([port, np.array(fan), stb]); Nn = np.vstack([npt, np.array(fan_n), nst]); Ll = np.concatenate([lp, np.linspace(-0.2, 0.2, 14), -lp[::-1]])
    prof = [(3.0, -0.28), (2.35, -0.05), (1.85, 0.38), (1.4, 0.95), (1.0, 1.55), (0.6, 2.0), (0.2, 2.25), (-0.2, 2.2), (-0.52, 1.92), (-0.7, 1.55), (-0.66, 1.22)]
    nK = 26; pr = catmull(prof, nK); sp_ = np.linspace(0, 1, nK)
    verts = []; sp = []; hz = []; lp_ = []
    al = np.abs(Ll)
    E = np.exp(-(np.maximum(al - 2.4, 0) / 6.2) ** 2) * (0.74 + 0.26 * ss(0.0, 2.4, al))
    nzh = 1 + 0.26 * (vnoise2(Ll * 0.8 + 40, np.zeros_like(Ll) + 3.0, 5) - 0.5) * 2; nzd = 0.22 * (vnoise2(Ll * 1.3 + 90, np.zeros_like(Ll) + 8.0, 6) - 0.5) * 2
    for j in range(len(Pp)):
        D = 1.15 + 0.11 * al[j] + nzd[j]; Hs = 1.18 * E[j] * nzh[j]; Wsc = 0.55 + 0.45 * E[j] + 0.25 * ss(6, 14, al[j])
        for k in range(nK):
            dn, zz = pr[k]; pxl = Pp[j, 0] + Nn[j, 0] * (D + dn * Wsc); pyl = Pp[j, 1] + Nn[j, 1] * (D + dn * Wsc)
            wp = loc2w((pxl, pyl, 0)); zb = float(swell_h(wp.x, wp.y)) * 0.92
            verts.append((pxl, pyl, zb + zz * Hs + (0.03 if E[j] < 0.05 else 0.0)))
            sp.append(sp_[k]); hz.append(float(np.clip(zz / 2.25, 0, 1))); lp_.append(float(al[j] / 16.0))
    faces = []; nJ = len(Pp)
    for j in range(nJ - 1):
        for k in range(nK - 1):
            a = j * nK + k; b = (j + 1) * nK + k; c = (j + 1) * nK + k + 1; dd = j * nK + k + 1; faces.append((a, b, c, dd))
    # orientation: the middle of the rising slope must face outward+up
    jm = 20; k = 8; a, b, c, dd = faces[jm * (nK - 1) + k]
    va = Vector(verts[a]); n = (Vector(verts[b]) - va).cross(Vector(verts[dd]) - va); want = Vector((Nn[jm, 0], Nn[jm, 1], 1.0))
    if n.dot(want) < 0: faces = [(f[3], f[2], f[1], f[0]) for f in faces]
    me = bpy.data.meshes.new('wave6'); me.from_pydata(verts, [], faces); me.update()
    for p in me.polygons: p.use_smooth = True
    for nm, arr in (('sp', sp), ('hz', hz), ('lp', lp_)):
        at = me.attributes.new(nm, 'FLOAT', 'POINT'); at.data.foreach_set('value', np.array(arr, dtype=np.float32))
    ob = bpy.data.objects.new('ship6_wave', me); bpy.context.scene.collection.objects.link(ob); me.materials.append(foam_sheet_mat('wave6')); ob.visible_shadow = False
    return Pp, Nn, E, Ll

def spray6(P, M, Pp, Nn, E, Ll):
    rr = random.Random(21); sp = MB('ship6_fleck'); tq = M['spray']
    for _ in range(420):
        j = rr.randrange(len(Pp)); al = abs(Ll[j]); 
        if E[j] < 0.15: continue
        D = 1.0 + 0.11 * al; r = rr.uniform(-0.6, 3.2); hgt = rr.uniform(0.0, 1.0) ** 1.6 * 3.6 * E[j] + 1.2 * E[j]
        px_ = Pp[j, 0] + Nn[j, 0] * (D + r); py_ = Pp[j, 1] + Nn[j, 1] * (D + r)
        wp = loc2w((px_, py_, 0)); zb = float(swell_h(wp.x, wp.y))
        rad = rr.uniform(0.05, 0.14) * (1.0 if hgt < 2.4 else 0.75); sp.ell(tq, (px_, py_, zb + 1.2 + hgt), (rad, rad, rad * 0.9), (6, 4))
    sp.finish(shadow=False)
    # soft mist billboards above the crest, facing the camera
    cam = Vector(P['cam']['loc']); mm = bpy.data.materials.new('mist'); mm.use_nodes = True; nt = mm.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (2, 2, 2); mp.inputs['Location'].default_value = (-1, -1, 0); L(tc.outputs['Generated'], mp.inputs['Vector'])
    gr = N('ShaderNodeTexGradient'); gr.gradient_type = 'SPHERICAL'; L(mp.outputs[0], gr.inputs['Vector'])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 1.6; L(gr.outputs['Fac'], pw.inputs[0])
    sc_ = N('ShaderNodeMath'); sc_.operation = 'MULTIPLY'; sc_.inputs[1].default_value = P.get('mist_a', 0.30); L(pw.outputs[0], sc_.inputs[0])
    em.inputs['Color'].default_value = hexc('#f4fafa'); em.inputs['Strength'].default_value = 1.1
    L(sc_.outputs[0], mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    rr = random.Random(33)
    for _ in range(26):
        j = rr.randrange(8, len(Pp) - 8)
        if E[j] < 0.25: continue
        D = 1.0 + 0.11 * abs(Ll[j]); p = loc2w((Pp[j, 0] + Nn[j, 0] * (D + rr.uniform(-0.2, 1.4)), Pp[j, 1] + Nn[j, 1] * (D + 0.5), 0)); p.z = float(swell_h(p.x, p.y)) + rr.uniform(1.8, 4.2) * E[j] + 0.6
        tcam = (cam - p).normalized(); rgt = Vector((0, 0, 1)).cross(tcam).normalized(); up = tcam.cross(rgt).normalized(); sz = rr.uniform(1.2, 2.6)
        vs = [p + rgt * (-sz) + up * (-sz * 0.7), p + rgt * sz + up * (-sz * 0.7), p + rgt * sz + up * (sz * 0.7), p + rgt * (-sz) + up * (sz * 0.7)]
        me = bpy.data.meshes.new('mist'); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update(); me.materials.append(mm)
        ob = bpy.data.objects.new('skyobj_mist', me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False

# ---- smooth cumulus: metaball union (one smooth surface), flat soft bottom, emission gradient material
def cumulus6(P, name, c, size, seed, nballs=70, squash=0.9):
    rr = random.Random(seed); mbd = bpy.data.metaballs.new(name); mbd.resolution = 0.07; mbd.render_resolution = 0.07; mbd.threshold = 0.55
    balls = []
    nb = int(nballs * 0.35)
    for i in range(nb):                       # wide base row
        x = rr.uniform(-2.6, 2.6); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.0, 0.5), rr.uniform(0.75, 1.1)))
    for i in range(int(nballs * 0.4)):        # body
        x = rr.uniform(-2.0, 2.0); balls.append((x, rr.uniform(-0.5, 0.5), rr.uniform(0.6, 1.5), rr.uniform(0.7, 1.05) * (1.1 - abs(x) * 0.12)))
    for i in range(int(nballs * 0.3)):        # towers
        x = rr.uniform(-1.3, 1.5); balls.append((x, rr.uniform(-0.4, 0.4), rr.uniform(1.4, 2.5) * (1.1 - abs(x) * 0.18), rr.uniform(0.5, 0.85)))
    for (x, y, z, r) in balls:
        e = mbd.elements.new(type='BALL'); e.co = (x, y, z); e.radius = r; e.stiffness = 2.2
    ob = bpy.data.objects.new(name, mbd); bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get(); me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); bpy.data.objects.remove(ob)
    co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    zmin = 0.35; co[:, 2] = np.where(co[:, 2] < zmin, zmin + (co[:, 2] - zmin) * 0.18, co[:, 2]); co[:, 1] *= squash
    me.vertices.foreach_set('co', co.ravel()); me.update()
    for p in me.polygons: p.use_smooth = True
    ob2 = bpy.data.objects.new('clouds_' + name, me); bpy.context.scene.collection.objects.link(ob2); ob2.data.materials.append(cloud_mat(P) if 'cloudG' not in MATS else MATS['cloudG'])
    ob2.location = c; ob2.scale = (size, size, size * 0.85); ob2.visible_shadow = False
    return ob2

def clouds6(P):
    cm = cloud_mat(P)
    for (nm, c, sz, sd) in P['clouds6']: cumulus6(P, nm, c, sz, sd)

def gull6(mb, m, mt, c, yaw, s, flap):
    mb.push(Matrix.Translation(c) @ Euler((0, 0, yaw)).to_matrix().to_4x4() @ Matrix.Diagonal((s, s, s, 1)))
    mb.ell(m, (0, 0, 0), (0.12, 0.42, 0.11), (10, 6)); mb.ell(m, (0, 0.40, 0.03), (0.075, 0.12, 0.07), (8, 5)); mb.ell(m, (0, -0.42, 0.0), (0.06, 0.2, 0.03), (8, 4))
    for sd in (-1, 1):
        pts = [(0.08, 0.15, 0.02), (0.75, 0.22 - 0.12 * flap, 0.12 + 0.34 * flap), (1.45, 0.02 - 0.2 * flap, 0.14 + 0.62 * flap), (1.95, -0.30 - 0.3 * flap, 0.0 + 0.6 * flap)]
        pb = [(0.08, -0.22, 0.0), (0.72, -0.12 - 0.1 * flap, 0.10 + 0.3 * flap), (1.35, -0.38 - 0.2 * flap, 0.1 + 0.55 * flap), (1.95, -0.58 - 0.3 * flap, 0.0 + 0.55 * flap)]
        for i in range(3):
            q = [(sd * pb[i][0], pb[i][1], pb[i][2]), (sd * pb[i + 1][0], pb[i + 1][1], pb[i + 1][2]), (sd * pts[i + 1][0], pts[i + 1][1], pts[i + 1][2]), (sd * pts[i][0], pts[i][1], pts[i][2])]
            mb.quad(mt if i == 2 else m, q); mb.quad(mt if i == 2 else m, q[::-1])
    mb.pop()

def far_dressing6(P, M):
    ib = MB('isle'); n = 56; X0i = 524.0; stp = 8.6
    for i in range(n):
        x0 = X0i + i * stp; x1 = x0 + stp
        f = lambda x: 66 * max(0, math.sin(math.pi * (x - X0i) / (n * stp))) ** 0.6 * (0.8 + 0.2 * math.sin((x - X0i) / 13.0)) + 6
        ib.quad(M['isle'] if i % 3 else M['isle2'], [(x0, 1800, 0), (x1, 1800, 0), (x1, 1800, f(x1)), (x0, 1800, f(x0))]); ib.quad(M['beach'], [(x0, 1799, -0.5), (x1, 1799, -0.5), (x1, 1799, 3.5), (x0, 1799, 3.5)])
    ib.finish(shadow=False)
    fs = MB('farsail'); x0, y0 = 205.0, 720.0
    fs.box(M['darksail'], (x0, y0, 1.2), (14.0, 3.0, 2.4))
    for k, (dx, hh, w) in enumerate(((-3.2, 17.0, 5.4), (2.4, 20.0, 5.8))):
        fs.quad(M['canv'], [(x0 + dx - w / 2, y0 - 0.4, 2.8), (x0 + dx + w / 2, y0 - 0.4, 2.8), (x0 + dx + w * 0.4, y0 - 0.4, hh), (x0 + dx - w * 0.4, y0 - 0.4, hh)])
    fs.finish(shadow=False)
    gm = MB('gulls'); gm.finish()
    gb = MB('gulls'); mw = mat('gullw', '#f6f5f0', '#e8ecee', scale=6); mt = mat('gullt', '#2e3038')
    for (c, yaw, s, fl) in P['gulls']: gull6(gb, mw, mt, c, yaw, s, fl)
    gb.finish(shadow=True)

def build_ship6_all(P):
    M, before = build_ship6(P)
    s = SHIP6; root = bpy.data.objects.new('shiproot', None); bpy.context.scene.collection.objects.link(root)
    root.location = (s['cx'], s['cy'], 0.0); root.rotation_euler = (0, 0, math.radians(180.0 - s['theta']))
    Pp, Nn, E, Ll = bow_wave6(P); spray6(P, M, Pp, Nn, E, Ll)
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.parent is None and (o.name.startswith('ship6') or o.name.startswith('shiproot')) : o.parent = root
    far_dressing6(P, M)
    if not os.environ.get('NOSEA'): build_sea6(P)
    clouds6(P)

# ---------------------------------------------------------------- the v6 sea: SAME swells, material and glitter as v5 (kept exactly); only the grid density, the ship-local foam field and a small bow hump are new
def build_sea6(P):
    c = P['cam']; loc = np.array(c['loc'], dtype=np.float64); look = np.array(c['look'], dtype=np.float64)
    f = look - loc; f /= np.linalg.norm(f); r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    hx, hy = 0.4602 * 1.15, 0.8182
    zfar = loc[2] / 7000.0
    vmax = (-zfar - f[2]) / (u[2] * hy); vmin = -1.3
    NU, NV = P.get('sea_nu', 800), P.get('sea_nv', 1100)
    uu = np.linspace(-1.0, 1.0, NU); vv = vmin + (vmax - vmin) * np.linspace(0, 1, NV)
    UU, VV = np.meshgrid(uu, vv)
    ray = f[None, None, :] + r[None, None, :] * (UU * hx)[..., None] + u[None, None, :] * (VV * hy)[..., None]
    t = -loc[2] / ray[..., 2]; px = loc[0] + ray[..., 0] * t; py = loc[1] + ray[..., 1] * t
    fpx = t * (2 * hx / 720.0) * 1.1
    sw, ch = sea_swell_params()
    h = np.zeros_like(px)
    for (k, ca, sa, ph, A) in sw:
        q = 0.5 + 0.5 * np.sin(k * (ca * px + sa * py) + ph); h += A * (2 * q ** 1.5 - 1.0)
    for (k, ca, sa, ph, A, L) in ch:
        fade = np.clip((L / np.maximum(fpx, 1e-6) - 4.0) / 7.0, 0, 1) * np.clip(1 - t / 260.0, 0, 1)
        h += A * np.sin(k * (ca * px + sa * py) + ph) * fade
    h *= np.clip(1 - t / 3500.0, 0, 1) ** 0.5
    # ---- ship-local frame
    s = SHIP6; ph_ = math.radians(180.0 - s['theta']); dx = px - s['cx']; dy = py - s['cy']
    lx = dx * math.cos(ph_) + dy * math.sin(ph_); ly = -dx * math.sin(ph_) + dy * math.cos(ph_)
    tt = np.clip((ly - YS) / (YB - YS), 0, 1); bw = w_wl(tt)
    ax = np.abs(lx)
    dh = np.where(ly >= YB, np.hypot(lx, ly - YB), ax - bw)           # distance from the hull waterline (negative = under the hull)
    dback = np.maximum(YS - ly, 0.0)
    ahead = ss(YB + 6.0, YB - 2.0, ly)
    # small bow hump + hull-side swell pushed up
    hump = 0.38 * np.exp(-((np.maximum(dh, 0) - 1.6) / 2.4) ** 2) * ss(YB - 16.0, YB - 2.0, ly) * ss(YB + 5.0, YB, ly) * (dh > -1.0)
    h += hump
    # ---- foam field: three lacy bands along the hull (3:1 patches, noise-thresholded), V wake from the stern with a turbulent core, bow ring under the wave
    def patches(n, thr, soft=0.11): return np.clip((n - thr) / soft, 0, 1)
    sideok = (ly > YS - 3.0) & (ly < YB + 8.0)
    n1 = 0.80 * fbm2(ly / 10.0, ax / 3.2, 4, 3) + 0.20 * vnoise2(ly * 0.9, ax * 1.1, 9)
    band = np.zeros_like(px)
    for (off, wd, amp, sd) in ((1.9, 1.7, 1.0, 4), (6.2, 2.4, 0.9, 14), (11.0, 3.0, 0.8, 24)):
        env = np.clip(1 - np.abs(dh - off) / wd, 0, 1); env = env * env * (3 - 2 * env)
        n = 0.78 * fbm2(ly / 9.0 + sd, ax / 2.9, 4 + sd, 3) + 0.22 * vnoise2(ly * 1.0 + sd, ax * 1.2, 9 + sd)
        band = np.maximum(band, patches(n, 0.58 - 0.26 * env) * env * amp)
    band *= sideok * ss(YB + 4.0, YB - 8.0, ly) * np.clip(1 - dback / 9.0, 0, 1) ** 0.5 * ss(-0.6, 0.5, dh)
    # wake behind the stern: widening V (arms ~ 3:1 patches along the track) + turbulent core
    wake = np.zeros_like(px); bws = float(w_wl(0.0))
    for (slope, wd0, wd1, amp, sd) in ((0.30, 1.5, 0.16, 1.0, 40), (0.13, 1.3, 0.10, 0.85, 50), (0.52, 1.9, 0.20, 0.7, 60)):
        xarm = bws * 0.9 + slope * dback; wd = wd0 + wd1 * dback
        env = np.clip(1 - np.abs(ax - xarm) / wd, 0, 1); env = env * env * (3 - 2 * env)
        n = 0.78 * fbm2(dback / 9.0 + sd, (ax - xarm) / 2.6, 4 + sd, 3) + 0.22 * vnoise2(dback * 0.8, ax * 1.2, 20 + sd)
        wake = np.maximum(wake, patches(n, 0.58 - 0.25 * env) * env * amp * np.exp(-dback / 78.0))
    core = np.exp(-(lx / (bws * 0.95 + 0.07 * dback)) ** 2) * np.exp(-dback / 34.0)
    nc = 0.78 * fbm2(dback / 6.0 + 70, lx / 1.7, 3, 3) + 0.22 * vnoise2(dback * 1.1, lx * 1.3, 8)
    wake = np.maximum(wake, patches(nc, 0.60 - 0.22 * core) * core)
    wake *= (ly < YS + 3.0) * ss(YS + 3.0, YS - 1.0, ly)
    # bow ring: foam where the wave sheet falls back, strongest at the stem
    ringenv = ss(0.0, 1.4, dh) * (1 - ss(3.2, 6.0, dh)) * ss(YB - 15.0, YB - 2.0, ly) * ss(YB + 7.0, YB + 1.0, ly)
    nb = 0.75 * fbm2(ly / 3.6 + 90, ax / 2.0 + 10, 7, 3) + 0.25 * vnoise2(ly * 1.5, ax * 1.5, 12)
    bow = patches(nb, 0.50 - 0.2 * ringenv) * ringenv
    foam = np.nan_to_num(np.clip(np.maximum(np.maximum(band, wake), bow), 0, 1))
    verts = np.stack([px, py, h], -1).reshape(-1, 3).astype(np.float32)
    idx = np.arange(NU * NV).reshape(NV, NU)
    a_ = idx[:-1, :-1]; b_ = idx[:-1, 1:]; c_ = idx[1:, 1:]; d_ = idx[1:, :-1]
    alt = ((np.arange(NU - 1)[None, :] + np.arange(NV - 1)[:, None]) % 2).astype(bool)
    t1 = np.where(alt[..., None], np.stack([a_, b_, c_], -1), np.stack([a_, b_, d_], -1)); t2 = np.where(alt[..., None], np.stack([a_, c_, d_], -1), np.stack([b_, c_, d_], -1))
    tris = np.concatenate([t1.reshape(-1, 3), t2.reshape(-1, 3)])
    me = bpy.data.meshes.new('sea'); me.vertices.add(len(verts)); me.vertices.foreach_set('co', verts.ravel())
    nt_ = len(tris); me.loops.add(nt_ * 3); me.polygons.add(nt_)
    me.loops.foreach_set('vertex_index', tris.ravel().astype(np.int32)); me.polygons.foreach_set('loop_start', (np.arange(nt_) * 3).astype(np.int32)); me.polygons.foreach_set('loop_total', np.full(nt_, 3, dtype=np.int32))
    me.update(calc_edges=True); me.polygons.foreach_set('use_smooth', np.ones(nt_, dtype=bool))
    at = me.attributes.new('foam', 'FLOAT', 'POINT'); at.data.foreach_set('value', foam.reshape(-1).astype(np.float32))
    ob = bpy.data.objects.new('sea', me); bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new('sea'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled')
    bs.inputs['Roughness'].default_value = 0.1; bs.inputs['IOR'].default_value = 1.33; bs.inputs['Specular IOR Level'].default_value = 0.5
    cdv = N('ShaderNodeCameraData'); msp = N('ShaderNodeMapRange'); msp.inputs['From Min'].default_value = 20.0; msp.inputs['From Max'].default_value = 120.0; msp.inputs['To Min'].default_value = 0.22; msp.inputs['To Max'].default_value = 0.5; L(cdv.outputs['View Distance'], msp.inputs['Value']); L(msp.outputs['Result'], bs.inputs['Specular IOR Level'])
    def mixc(a, b, fac):
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'
        if hasattr(a, 'node'): L(a, mx.inputs[6])
        else: mx.inputs[6].default_value = a
        if hasattr(b, 'node'): L(b, mx.inputs[7])
        else: mx.inputs[7].default_value = b
        L(fac, mx.inputs[0]); return mx.outputs[2]
    cd = N('ShaderNodeCameraData'); mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 22.0; mr.inputs['From Max'].default_value = 220.0; L(cd.outputs['View Distance'], mr.inputs['Value'])
    col = mixc(hexc(P['sea_near']), hexc(P['sea_far']), mr.outputs['Result'])
    gp = N('ShaderNodeNewGeometry'); spz = N('ShaderNodeSeparateXYZ'); L(gp.outputs['Position'], spz.inputs[0])
    cr = N('ShaderNodeMapRange'); cr.inputs['From Min'].default_value = 0.55; cr.inputs['From Max'].default_value = 0.9; L(spz.outputs['Z'], cr.inputs['Value'])
    tcw = N('ShaderNodeTexCoord'); mpw = N('ShaderNodeMapping'); mpw.inputs['Scale'].default_value = (1.1, 0.7, 1.0); L(tcw.outputs['Object'], mpw.inputs['Vector'])
    nzw = N('ShaderNodeTexNoise'); nzw.inputs['Scale'].default_value = 1.0; nzw.inputs['Detail'].default_value = 2.0; L(mpw.outputs[0], nzw.inputs['Vector'])
    sp2 = N('ShaderNodeMapRange'); sp2.inputs['From Min'].default_value = 0.52; sp2.inputs['From Max'].default_value = 0.64; L(nzw.outputs['Fac'], sp2.inputs['Value'])
    wc = N('ShaderNodeMath'); wc.operation = 'MULTIPLY'; wc.use_clamp = True; L(cr.outputs['Result'], wc.inputs[0]); L(sp2.outputs['Result'], wc.inputs[1])
    col = mixc(col, hexc('#e4eeec'), wc.outputs[0])
    fa = N('ShaderNodeAttribute'); fa.attribute_type = 'GEOMETRY'; fa.attribute_name = 'foam'
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 1.6; nz2.inputs['Detail'].default_value = 1.0; mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (2.4, 2.4, 1.0); L(tcw.outputs['Object'], mp2.inputs['Vector']); L(mp2.outputs[0], nz2.inputs['Vector'])
    br = N('ShaderNodeMapRange'); br.inputs['From Min'].default_value = -2.0; br.inputs['From Max'].default_value = -1.0; L(nz2.outputs['Fac'], br.inputs['Value'])
    fm = N('ShaderNodeMath'); fm.operation = 'MULTIPLY'; fm.use_clamp = True; L(fa.outputs['Fac'], fm.inputs[0]); L(br.outputs['Result'], fm.inputs[1])
    fm2 = N('ShaderNodeMath'); fm2.operation = 'MULTIPLY'; fm2.use_clamp = True; fm2.inputs[1].default_value = 1.25; L(fm.outputs[0], fm2.inputs[0])
    col = mixc(col, hexc('#f0f6f2'), fm2.outputs[0])
    L(col, bs.inputs['Base Color'])
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.3
    mrn = N('ShaderNodeMapRange'); mrn.inputs['From Min'].default_value = 20.0; mrn.inputs['From Max'].default_value = 120.0; mrn.inputs['To Min'].default_value = 0.12; mrn.inputs['To Max'].default_value = 1.0; L(cd.outputs['View Distance'], mrn.inputs['Value'])
    fk = N('ShaderNodeMath'); fk.operation = 'MULTIPLY'; fk.inputs[1].default_value = P.get('fresnel_k', 0.7); L(mrn.outputs['Result'], fk.inputs[0])
    em = N('ShaderNodeMath'); em.operation = 'MULTIPLY'; L(lw.outputs['Fresnel'], em.inputs[0]); L(fk.outputs[0], em.inputs[1])
    bs.inputs['Emission Color'].default_value = hexc('#9fc2d8'); L(em.outputs[0], bs.inputs['Emission Strength'])
    nzb = N('ShaderNodeTexNoise'); nzb.inputs['Scale'].default_value = 1.8; nzb.inputs['Detail'].default_value = 0.0; L(tcw.outputs['Object'], nzb.inputs['Vector'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.2; bp.inputs['Distance'].default_value = 0.2; L(nzb.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface']); ob.data.materials.append(m)
    # glossy-only virtual sun (light-linked to the sea): the sharp glitter lobe lands under it, ahead-left of the camera
    coll = bpy.data.collections.new('seacoll'); bpy.context.scene.collection.children.link(coll); coll.objects.link(ob)
    kd = Vector(kdir(P['glit_az'], P['glit_el'])).normalized(); d = bpy.data.lights.new('glint', 'SUN'); d.color = (1.0, 0.86, 0.62); d.energy = P.get('glit_k', 14.0); d.angle = math.radians(0.6)
    o = bpy.data.objects.new('glint', d); bpy.context.scene.collection.objects.link(o); o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler()
    o.visible_diffuse = False; o.light_linking.receiver_collection = coll


build_ship = build_ship6_all
PRESETS['ship'] = dict(
    sky=[(0.0, '#6c9ce0'), (0.46, '#b6cfe8'), (0.5, '#b0cbe8'), (0.56, '#8db3e6'), (0.66, '#6a98e0'), (0.78, '#4a7bd6'), (0.88, '#3a67cb'), (1.0, '#2c54b6')], sky_k=1.0,
    key=(1.0, 0.92, 0.78, 7.2), key_dir=kdir(160, 42), sun_angle=0.9, exposure=0.1, sat=1.08, amb=('#3050FF', 1.7), samples=80, dbounce=1, gloss=2,
    cloud=('#ffffff', '#8c9ce8'), cloud_diffuse=True,
    clouds6=[('cF', (-40, 620, 330), 46, 17), ('cA', (-250, 430, 130), 36, 3), ('cB', (150, 520, 215), 44, 7), ('cC', (-330, 700, 90), 40, 5), ('cD', (380, 560, 70), 30, 11), ('cE', (20, 900, 120), 60, 13)],
    gulls=[((9.2, 30.0, 14.0), 2.2, 0.6, 0.4), ((8.2, 40.0, 28.0), 0.8, 0.55, -0.3), ((-18.5, 50.0, 39.0), 3.4, 0.6, 0.1), ((13.4, 35.0, 9.3), 1.0, 0.45, 0.6), ((11.0, 46.0, 22.0), 2.9, 0.5, 0.0)],
    sea_near='#0a4a58', sea_far='#0a2c4c', fresnel_k=0.7,
    glit_az=12, glit_el=9, glit_k=30.0,
    cam=dict(loc=(0.0, 0.0, 5.0), look=(0.0, 100.0, 5.0 + 100.0 * math.tan(math.radians(3.0))), lens=22))

def lights_ship(P):
    sun_light(P); w = sky_world2(P)
