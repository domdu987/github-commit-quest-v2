"""jimo_vista.py : the Qi plain from high above (DUSK / DAWN): rolling patchwork fields, a river and roads, 60+ small walled towns (plain shapes, NO text), Jimo near (warm lit,
a ring moat, the Yan siege camp beside it) and Ju far (warm lit). set_pennants(k, side) pops black Yan pennants over the towns one by one; set_qi_return(k) turns them to Qi colours
one by one; the two holdout towns stay lit and carry a Qi pennant all along."""
import math, sys
import numpy as np
from mathutils import Vector as V, Matrix

J = None
def bind(j):
    global J; J = j

JIMO = (30.0, -30.0); JU = (-95.0, 330.0)
def river_y(x): return 150.0 - 0.11 * x + 40.0 * math.sin(x / 95.0)

def terrain_h(x, y):
    h = 2.6 * math.sin(x / 46.0 + 0.6) * math.cos(y / 58.0) + 1.8 * math.sin(x / 21.0 - y / 33.0) + 1.0 * math.sin(y / 17.0 + x / 53.0)
    far = max(0.0, (y - 360.0) / 60.0); side = max(0.0, (abs(x) - 330.0) / 60.0); h += 18.0 * min(1.5, far) * (1.0 + 0.4 * math.sin(x / 40.0)) + 16.0 * min(1.5, side)
    d = abs(y - river_y(x)); w = math.exp(-(d / 17.0) ** 2); h = h * (1 - w) + (-1.4) * w
    for (cx, cy) in (JIMO, JU): h *= 1.0 - 0.0
    return h

def build_vista(Bk, M, light):
    J.STATE['pennants'] = []; r = J._rnd(3); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); S = J.STATE; P = S['P']
    import jimo_vista3 as V3; R3 = V3.enabled(); S['r3'] = R3
    if R3: V3.bind(J, sys.modules[__name__]); M = V3.materials(M)
    # ---- terrain (cell 14 D), patchwork fields on two textures
    pre = S['pre']; tx = S['tx']; FM = tuple(P['form'])
    M = dict(M); sm = (1.5, 2.1, 1.0)
    M['fields'] = J._untoon(J.mat_lit(pre + 'vt_fields', image=tx['fields'], gain=1.9, shade_mul=sm, form=None)); M['fields_b'] = J._untoon(J.mat_lit(pre + 'vt_fields_b', image=tx['fields_b'], gain=1.8, shade_mul=sm, form=None))
    tb = Bk('terrain'); x0, x1, y0, y1, c = -460.0, 460.0, -300.0, 520.0, 14.0
    nx, ny = int((x1 - x0) / c), int((y1 - y0) / c)
    H = {(i, j): terrain_h(x0 + i * c, y0 + j * c) for i in range(nx + 1) for j in range(ny + 1)}
    for i in range(nx):
        for j in range(ny):
            xa, ya = x0 + i * c, y0 + j * c; pts = [V((xa, ya, H[i, j])), V((xa + c, ya, H[i + 1, j])), V((xa + c, ya + c, H[i + 1, j + 1])), V((xa, ya + c, H[i, j + 1]))]
            mat = V3.field_mat(M, xa, ya) if R3 else M['fields'] if (int((xa + 900) / 70) * 7 + int((ya + 900) / 70) * 13 + (int((xa + 900) / 35) ^ int((ya + 900) / 35))) % 3 else M['fields_b']
            tb.oface(pts, mat, [(xa / 64, ya / 64), ((xa + c) / 64, ya / 64), ((xa + c) / 64, (ya + c) / 64), (xa / 64, (ya + c) / 64)], (0, 0, 1))
    # ---- river ribbon + roads
    wt = Bk('river', shadow=False); prev = None
    for k in range(0, 66):
        x = x0 + k * 14.0 * 1.0; yc = river_y(x); a = (x, yc - 9.0, -0.55); b = (x, yc + 9.0, -0.55)
        if prev: wt.oface([V(prev[0]), V(prev[1]), V(b), V(a)][::-1], M['vwater'], [(prev[0][0] / 20, 0), (prev[0][0] / 20, 1), (x / 20, 1), (x / 20, 0)][::-1], (0, 0, 1))
        prev = (a, b)
    # ---- the towns: 44 ordinary + 18 far / small + Jimo + Ju; positions: jittered grid avoiding the river, the holdouts and each other
    towns = []; occupied = [JIMO, JU]; occ_r = [78.0, 100.0 if R3 else 46.0]
    def free(x, y, rr): return all(math.hypot(x - ox, y - oy) > rr + orr for (ox, oy), orr in zip(occupied, occ_r)) and abs(y - river_y(x)) > 24 + rr
    if R3:                                                                                        # a clear sight line to Ju from the s03 / s04 / s25 cameras (no ordinary town or pennant in front)
        for (qx, qy) in ((-35.0, 140.0), (-52.0, 185.0), (-66.0, 230.0), (-78.0, 275.0), (-20.0, 100.0)): occupied.append((qx, qy)); occ_r.append(40.0)
    k = 0; tries = 0
    while len(towns) < 62 and tries < 12000:
        tries += 1; x, y = r.uniform(-200, 200), r.uniform(-90, 440); s = r.uniform(20, 26) * (1.0 + max(0.0, y + 90) / 330.0)
        if free(x, y, s * 0.5 + 3): occupied.append((x, y)); occ_r.append(s * 0.5 + 3); towns.append(dict(x=x, y=y, s=s, hold=False))
    towns.append(dict(x=JIMO[0], y=JIMO[1], s=56.0, hold=True, name='jimo')); towns.append(dict(x=JU[0], y=JU[1], s=80.0 if R3 else 40.0, hold=True, name='ju'))
    S['towns'] = towns
    bd = Bk('towns', hull=0.0); rf = Bk('townroofs', hull=0.0); gl = Bk('townglow', shadow=False); hl = Bk('halos', shadow=False)
    def town(t):
        cx, cy, s = t['x'], t['y'], t['s']; z0 = terrain_h(cx, cy) + 0.1; yaw = r.uniform(-14, 14); F = J.Frame((cx, cy, z0), yaw); wh = s * 0.17; hold = t['hold']
        for sgn in (-1, 1):                                                                                      # four curtain walls (rammed earth) with merlon dots
            J.obox(bd, F.p(sgn * s / 2, 0, wh / 2), F.X, F.Y, F.Z, s * 0.035, s / 2, wh / 2, M['rammed'], uvk=0.1); J.obox(bd, F.p(0, sgn * s / 2, wh / 2), F.X, F.Y, F.Z, s / 2, s * 0.035, wh / 2, M['rammed'], uvk=0.1)
        for sx in (-1, 1):
            for sy in (-1, 1):                                                                                   # corner towers with hip roofs
                J.obox(bd, F.p(sx * s / 2, sy * s / 2, wh * 0.75), F.X, F.Y, F.Z, s * 0.07, s * 0.07, wh * 0.75, M['rammed_d'], uvk=0.1)
                J.hip_roof(rf, F.p(sx * s / 2, sy * s / 2, wh * 1.5), yaw, s * 0.1, s * 0.1, 0.0, 0.0, s * 0.07, M, lift=0.0, nx=2, ny=2, mat=M['tiles'], wadang=False)
        J.obox(bd, F.p(0, -s / 2, wh * 0.45), F.X, F.Y, F.Z, s * 0.07, s * 0.05, wh * 0.45, M['r3_gate'] if R3 else M['black'], uvk=0.1)                                     # gate
        J.hip_roof(rf, F.p(0, -s / 2, wh * 1.05), yaw, s * 0.12, s * 0.08, s * 0.04, 0.0, s * 0.06, M, lift=0.0, nx=3, ny=2, mat=M['tiles'], wadang=False)
        n = 10 if hold else 7
        for q in range(n):                                                                                       # houses
            hx, hy = r.uniform(-s * 0.36, s * 0.36), r.uniform(-s * 0.32, s * 0.34); hw, hd = r.uniform(s * 0.1, s * 0.17), r.uniform(s * 0.08, s * 0.13); hh = r.uniform(s * 0.07, s * 0.11)
            J.obox(bd, F.p(hx, hy, hh / 2), F.X, F.Y, F.Z, hw / 2, hd / 2, hh / 2, M['plaster'] if q % 2 else M['plaster_d'], uvk=0.1)
            J.hip_roof(rf, F.p(hx, hy, hh), yaw, hw / 2 + s * 0.02, hd / 2 + s * 0.02, max(0.01, hw / 2 - hd / 2), 0.0, s * 0.05, M, lift=0.0, nx=4, ny=2, mat=M['tiles'], wadang=False)
            if hold or q < 2: J.flat(gl, F.p(hx - hw * 0.3, hy - hd / 2 - 0.05, hh * 0.25), F.X * (hw * 0.6), F.Z * (hh * 0.45), M['win'] if hold else M['win_dim'])
        if hold:
            J.halo(hl, V((cx, cy, z0 + wh + 4)), s * 0.75, M['halo_big']); J.halo(hl, V((cx, cy, z0 + wh + 2)), s * 0.38, M['halo'])        # round 2: small warm halo (no bloom blob)
            for sx in (-1, 1):
                if not (R3 and t.get('name') == 'ju'): J.live_flame(F.p(sx * s * 0.07, -s / 2 - 1.2, 0.0), s * 0.09, s * 0.035, seed=int(cx) + sx, n=2, light=0.0, name='townfire', warm=None)
            J.flat(Bk('townpool', shadow=False), V((cx - s * 0.9, cy - s * 0.9, z0 + 0.3)), V((s * 1.8, 0, 0)), V((0, s * 1.8, 0)), M['pool_w']) if False else None
        if R3 and t.get('name') == 'ju': V3.ju_extras(Bk, M, t, z0, yaw)
        return z0
    for t in towns: t['z0'] = town(t)
    # Jimo: ring moat and the Yan siege camp (tents, fires, black pennants) to its south
    jx, jy = JIMO; z = terrain_h(jx, jy); ring = Bk('river', shadow=False)
    for k in range(48):
        a0, a1 = 2 * math.pi * k / 48, 2 * math.pi * (k + 1) / 48; R0, R1 = (39.0, 44.0) if R3 else (38.0, 46.0)
        ring.oface([V((jx + R0 * math.cos(a0), jy + R0 * math.sin(a0), z + 0.12)), V((jx + R1 * math.cos(a0), jy + R1 * math.sin(a0), z + 0.12)), V((jx + R1 * math.cos(a1), jy + R1 * math.sin(a1), z + 0.12)), V((jx + R0 * math.cos(a1), jy + R0 * math.sin(a1), z + 0.12))], M['vwater'], [(0, 0), (0, 1), (1, 1), (1, 0)], (0, 0, 1))
    tb2 = Bk('siegetents'); tent_pos = []
    for k in range(16):
        x = jx - 34 + (k % 6) * 14 + r.uniform(-3, 3); y = jy - 46 - (k // 6) * 12 - r.uniform(0, 3); h = r.uniform(4, 6); yw_ = r.uniform(-20, 20); F = J.Frame((x, y, terrain_h(x, y)), yw_); w, l = 6.5, 8.0
        tent_pos.append((x, y, h, yw_))
        for sgn in ((-1, 1) if not R3 else ()): tb2.oface([F.p(sgn * w / 2, -l / 2, 0), F.p(sgn * w / 2, l / 2, 0), F.p(0, l / 2, h), F.p(0, -l / 2, h)], M['canvas'] if k % 3 else M['hide'], [(0, 0), (2, 0), (2, 1), (0, 1)], F.X * sgn + F.Z * 0.9)
        for yy_, n_ in (((-l / 2, -1), (l / 2, 1)) if not R3 else ()): tb2.oface([F.p(-w / 2, yy_, 0), F.p(w / 2, yy_, 0), F.p(0, yy_, h)], M['canvas'], [(0, 0), (1, 0), (0.5, 1)], F.Y * n_)
        if k % 4 == 0: J.live_flame(V((x + 5, y - 3, terrain_h(x, y) + 0.2)), 3.4, 0.9, seed=k, n=3, light=0.0, name='siegefire', warm=None); J.halo(hl, V((x + 5, y - 3, terrain_h(x, y) + 3)), 11.0, M['halo'])
        if k % 3 == 0: J.banner(Bk, M, (x - 4, y, terrain_h(x, y)), 12.0, 4.2, 2.4, M['silk_blk'] if R3 else M['black'], M['silk_red'] if R3 else M['red'], wave=k, sw=True)
    # trees: small dark clumps along roads and fields (cones), scattered
    tr = Bk('vtrees')
    for k in range(380 if not R3 else 0):
        x, y = r.uniform(-420, 420), r.uniform(-150, 500)
        if abs(y - river_y(x)) < 14 or any(math.hypot(x - t['x'], y - t['y']) < t['s'] * 0.8 for t in towns): continue
        zt = terrain_h(x, y); h = r.uniform(3, 6); tr.frustum(V((x, y, zt)), V((x, y, zt + h)), r.uniform(1.4, 2.4), 0.2, M['leaf'] if k % 2 else M['grass2'], seg=5, cap0=False)
    # roads: Jimo -> Ju by a chain through the nearest towns, plus spurs
    rd = Bk('vroad'); pts = [JIMO]; rest = [(t['x'], t['y']) for t in towns[:-2]]; cur = JIMO
    for _ in range(14):
        rest.sort(key=lambda p: math.hypot(p[0] - cur[0], p[1] - cur[1]) + 0.6 * math.hypot(p[0] - JU[0], p[1] - JU[1])); cur = rest.pop(0); pts.append(cur)
    pts.append(JU)
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1]); n = max(2, int(L / 12)); prev = None
        for q in range(n + 1):
            t = q / n; x = a[0] + (b[0] - a[0]) * t + 6 * math.sin(t * 6 + a[0]); y = a[1] + (b[1] - a[1]) * t; nx_, ny_ = -(b[1] - a[1]) / L, (b[0] - a[0]) / L; w = 1.5; z = terrain_h(x, y) + 0.2
            e = (V((x - nx_ * w, y - ny_ * w, z)), V((x + nx_ * w, y + ny_ * w, z)))
            if prev: rd.oface([prev[0], prev[1], e[1], e[0]], M['road'], [(0, 0), (0, 1), (1, 1), (1, 0)], (0, 0, 1))
            prev = e
    if R3: S['road_pts'] = pts; V3.dress(Bk, M, towns, pts, tent_pos)
    # ---- pennants: black Yan pennant and the Qi one at each ordinary town (and a Qi one on the holdouts), own objects with the origin at the pole foot
    for i, t in enumerate(towns):
        z0 = t['z0']; s = t['s']; hgt = (10.0 + s * 0.6) * 1.35
        if R3 and t.get('name') == 'ju': hgt = 24.0
        for kind, col, trim in (('yan', M['black'], M['red']), ('qi', M['red'], M['teal'])):
            if t['hold'] and kind == 'yan': continue
            b = Bk('pen_%s_%d' % (kind, i), hull=0.0)
            pb = b; base = V((t['x'], t['y'], z0)); J.rod(pb, base, base + V((0, 0, hgt)), 0.5, M['wood_d'], seg=5); pb.sphere(base + V((0, 0, hgt + 0.4)), 0.6, M['gold'], seg=6, rings=4)
            fw, fh = s * 0.5 * 1.5, s * 0.3 * 1.5; top = hgt - 0.4
            if R3: V3.cloth(Bk, M, 'pcl_%s_%d' % (kind, i), base + V((0, 0, top)), fw, fh, kind, i)
            else:
              for q in range(6):
                x0_, x1_ = fw * q / 6, fw * (q + 1) / 6; sw0 = math.sin(q * 0.9 + i) * 0.25 * (q / 6) * fh; sw1 = math.sin((q + 1) * 0.9 + i) * 0.25 * ((q + 1) / 6) * fh
                bot0 = top - fh * (1 - 0.35 * (q / 6)); bot1 = top - fh * (1 - 0.35 * ((q + 1) / 6))
                pts_ = [base + V((x0_, sw0, top)), base + V((x1_, sw1, top)), base + V((x1_, sw1, bot1)), base + V((x0_, sw0, bot0))]
                pb.oface(pts_, col, [(0, 0)] * 4, (0, -1, 0)); pb.oface(pts_[::-1], col, [(0, 0)] * 4, (0, 1, 0))
                tp = [base + V((x0_, sw0, top)), base + V((x1_, sw1, top)), base + V((x1_, sw1, top - fh * 0.2)), base + V((x0_, sw0, top - fh * 0.2))]
                pb.oface(tp, trim, [(0, 0)] * 4, (0, -1, 0)); pb.oface(tp[::-1], trim, [(0, 0)] * 4, (0, 1, 0))
            S['pennants'].append(dict(town=i, kind=kind, name='pen_%s_%d' % (kind, i), cname='pcl_%s_%d' % (kind, i) if R3 else None, ctop=tuple(base + V((0, 0, top))), base=tuple(base), hold=t['hold'], x=t['x'], y=t['y']))
    def post():
        ob = S['objects']; cam = V(S['cam']['loc'])
        for p in S['pennants']:
            o = ob.get(p['name']); p['ob'] = o
            if o is not None: J.localize(o, p['base'])
            c = ob.get(p['cname']) if p.get('cname') else None; p['cl'] = c
            if c is not None: J.localize(c, p['ctop'])
        order = [p['town'] for p in S['pennants'] if p['kind'] == 'yan']; S['pen_order'] = {}
        pool = [(t['x'], t['y'], i) for i, t in enumerate(towns) if not t['hold']]
        orders = dict(yan=sorted(pool, key=lambda q: J._hash(int(q[0] * 10), int(q[1] * 10))), ltr=sorted(pool, key=lambda q: q[0]), rtl=sorted(pool, key=lambda q: -q[0]),
                      near=sorted(pool, key=lambda q: math.hypot(q[0] - cam.x, q[1] - cam.y)), far=sorted(pool, key=lambda q: -math.hypot(q[0] - cam.x, q[1] - cam.y)))
        S['pen_orders'] = {k: {q[2]: n for n, q in enumerate(v)} for k, v in orders.items()}; S['pen_orders']['qi'] = S['pen_orders']['yan']
        set_pennants(0.0, 'yan'); set_qi_return(0.0)
        if R3: V3.finish()
    S.setdefault('post_flush', []).append(post)
    J.hills(Bk, M, (0.0, 120.0), 700.0, 760.0, 22, 7, (70, 110), z=0.5) if False else None
    S['marks']['jimo'] = (JIMO[0], JIMO[1], terrain_h(*JIMO)); S['marks']['ju'] = (JU[0], JU[1], terrain_h(*JU)); S['marks']['river'] = 'y = 150 - 0.11 x + 40 sin(x / 95)'
    S['marks']['towns'] = [(round(t['x'], 1), round(t['y'], 1), round(t['s'], 1), t['hold']) for t in towns]

def vista_r3(sweep=True):
    """Round-3 finisher (see API.md 'Vista round 3'): idempotent; build('vista') already applies the whole round, call it again after adding your own flame cards / poles."""
    import jimo_vista3 as V3; V3.bind(J, sys.modules[__name__]); return V3.finish(sweep)

def _pop(o, p, frame, cl=None):
    if cl is None: J._vis(o, p > 0.01, frame); J._xf(o, scl=(max(0.01, p),) * 3, frame=frame)
    else:                                                    # round 4: the pole stands as soon as the pennant is on, the cloth grows from the pole top (never flat)
        J._vis(o, p > 0.01, frame); J._vis(cl, p > 0.01, frame); J._xf(cl, scl=(max(0.01, p),) * 3, frame=frame)

def _pop2(p, v, frame): _pop(p['ob'], v, frame, p.get('cl'))

def _cam_xy(cam):
    if cam is None: cam = J.STATE['cam']['loc']
    if hasattr(cam, 'matrix_world'): cam = cam.matrix_world.translation
    elif hasattr(cam, 'location'): cam = cam.location
    return float(cam[0]), float(cam[1])

def vista_pennant_order(cam=None, kind='yan'):
    """Round 4: the ordinary-town pennants sorted NEAR to FAR for camera `cam` (a Blender camera object, a Vector / (x, y, z) or None = the scene camera, ground-plane distance).
    Returns a list of town indices (`idx` for set_pennant_scale; also `S['pennants']` entries with that `town`). Holdouts (Jimo, Ju) are not in it."""
    cx, cy = _cam_xy(cam); T = J.STATE['towns']
    return sorted([i for i, t in enumerate(T) if not t['hold']], key=lambda i: math.hypot(T[i]['x'] - cx, T[i]['y'] - cy))

def set_pennant_scale(idx, k, kind='yan', frame=None):
    """Round 4: pennant of town `idx` (see vista_pennant_order): k 0 .. 1; the pole stands from k > 0 and the cloth grows from the pole top (uniform scale about the attach corner,
    so it only ever hangs, never lies flat or diagonal). Overrides set_pennants for that town until the next set_pennants / set_qi_return call."""
    for p in J.STATE['pennants']:
        if p['town'] == idx and p['kind'] == kind and p.get('ob') is not None: _pop2(p, min(1.0, max(0.0, float(k))), frame)

def set_pennants(k, side='yan', frame=None):
    """Black Yan pennants pop up over the towns one by one: k 0 .. 1 (0 none, 1 all 62 ordinary towns). `side` = the ORDER they pop in: 'yan' (a fixed scattered order, default),
    'ltr' / 'rtl' (left to right / right to left in x), 'near' / 'far' (nearest / farthest from the scene camera). The holdout towns (Jimo, Ju) never get one."""
    S = J.STATE; S['states']['pennants'] = (k, side); order = S['pen_orders'].get(side, S['pen_orders']['yan']); n = len(order); qr = S['states'].get('qi', 0.0)
    for p in S['pennants']:
        if p['kind'] != 'yan' or p.get('ob') is None: continue
        idx = order[p['town']]; pop = min(1.0, max(0.0, k * n - idx)); back = min(1.0, max(0.0, qr * n - S['pen_orders']['qi'][p['town']]))
        _pop2(p, pop * (1.0 - (1.0 if back > 0.5 else 0.0)), frame)

def set_qi_return(k, frame=None):
    """The Yan pennants turn to Qi colours one by one: k 0 .. 1 (the Yan pennant shrinks away and the Qi one pops, 70 % overlap). The holdouts keep their Qi pennant (always up)."""
    S = J.STATE; S['states']['qi'] = k; order = S['pen_orders']['qi']; n = len(order)
    for p in S['pennants']:
        if p.get('ob') is None: continue
        if p['hold']: _pop2(p, 1.0, frame); continue
        idx = order[p['town']]; v = min(1.0, max(0.0, k * n - idx))
        if p['kind'] == 'qi': _pop2(p, v, frame)
        else:
            pk, side = S['states'].get('pennants', (0.0, 'yan')); o2 = S['pen_orders'].get(side, order); pop = min(1.0, max(0.0, pk * n - o2[p['town']])); _pop2(p, pop * (1.0 if v < 0.5 else 0.0), frame)
