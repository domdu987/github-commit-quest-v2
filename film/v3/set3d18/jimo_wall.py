"""jimo_wall.py : the Jimo wall (rammed earth, both faces, subdivided so the fire-lit OCHRE / moon-shade BLUE split is smooth), the gate hall with swinging leaves,
12 breaches (plug + ragged breach + dig props, keyed by set_holes), city roofs behind it, the moat (water near the gate, a dry silted ditch beside it), bridge, road, fields and
the far Yan camp (jimo_out).  Every function reaches the jimo module through bind(J) (its names are copied into this namespace)."""
import math
import numpy as np
from mathutils import Vector as V, Matrix

def bind(J):
    g = globals()
    for k, v in vars(J).items():
        if not k.startswith('__'): g.setdefault(k, v)

X0, X1 = -95.0, 95.0
XX, YY, ZZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)

def openings():
    return sorted([(0.0, GATE_W * 2, GATE_H)] + [(x, HOLE_W, HOLE_H) for x in HOLE_X])

def _grid(mb, pf, x0, x1, z0, z1, mat, uk, vk, nrm, cell=2.0):
    nx = max(1, int(math.ceil((x1 - x0) / cell))); nz = max(1, int(math.ceil((z1 - z0) / cell)))
    for i in range(nx):
        xa = x0 + (x1 - x0) * i / nx; xb = x0 + (x1 - x0) * (i + 1) / nx
        for j in range(nz):
            za = z0 + (z1 - z0) * j / nz; zb = z0 + (z1 - z0) * (j + 1) / nz
            mb.oface([pf(xa, za), pf(xb, za), pf(xb, zb), pf(xa, zb)], mat, [(xa * uk, za * vk), (xb * uk, za * vk), (xb * uk, zb * vk), (xa * uk, zb * vk)], nrm)

def prism_g(mb, x0, x1, z0, z1, mo, mi, mt, mend=None, ends=True, outer=True, inner=True):
    """Wedge wall piece (outer face battered yo(z), inner face yi(z)), both faces on a 2 D grid, a top (walk planks `mt`), underside, end caps (`mend`)."""
    mend = mend or mi
    if outer: _grid(mb, lambda x, z: V((x, yo(z), z)), x0, x1, z0, z1, mo, 1 / 8, 0.2516, (0, -1, 0.12))
    if inner: _grid(mb, lambda x, z: V((x, yi(z), z)), x0, x1, z0, z1, mi, 1 / 8, 0.2504, (0, 1, 0.06))
    if z1 >= WH - 0.01: mb.oface([V((x0, yo(z1), z1)), V((x1, yo(z1), z1)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))], mt, [(x0 / 8, 0), (x1 / 8, 0), (x1 / 8, 0.8), (x0 / 8, 0.8)], (0, 0, 1))
    else: mb.oface([V((x0, yo(z1), z1)), V((x1, yo(z1), z1)), V((x1, yi(z1), z1)), V((x0, yi(z1), z1))], mend, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    if z0 > 0: mb.oface([V((x0, yo(z0), z0)), V((x1, yo(z0), z0)), V((x1, yi(z0), z0)), V((x0, yi(z0), z0))], mend, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, -1))
    if ends:
        for xe, nx in ((x0, -1), (x1, 1)):
            mb.oface([V((xe, yo(z0), z0)), V((xe, yi(z0), z0)), V((xe, yi(z1), z1)), V((xe, yo(z1), z1))], mend, [(0, z0 / 4.0), (0.9, z0 / 4.0), (0.9, z1 / 4.0), (0, z1 / 4.0)], (nx, 0, 0))

def wall_shell(Bk, M, loc):
    """The wall with the gate passage and the 12 breach openings (each closed by a plug until set_holes opens it)."""
    hd = T.hull(62.0 if loc != 'yan_camp' else 100.0); wl = Bk('wall', hull=hd); ops = openings(); x = X0
    for (xc, w, h) in ops:
        a, b = xc - w / 2, xc + w / 2
        prism_g(wl, x, a, 0.0, WH, M['rammed'], M['rammed'], M['planks_d'], M['rammed_d']); prism_g(wl, a, b, h, WH, M['rammed'], M['rammed'], M['planks_d'], M['tunnel']); x = b
    prism_g(wl, x, X1, 0.0, WH, M['rammed'], M['rammed'], M['planks_d'], M['rammed_d'])
    STATE['holes'] = ops; STATE['warm_names'] = ['wall']
    plugs = []
    for i, hx in enumerate(HOLE_X):
        pb = Bk('plug%d' % i, hull=hd); prism_g(pb, hx - HOLE_W / 2, hx + HOLE_W / 2, 0.0, HOLE_H, M['rammed'], M['rammed'], M['rammed_d'], M['rammed_d'], ends=False); STATE['warm_names'].append('plug%d' % i)
    # parapet (outer side) of earth merlons with a timber coping; a timber rail on the inner side of the walk
    mr = Bk('merlons', hull=hd); yv = yo(WH) + 0.05; xm = X0 + 1.0
    while xm < X1 - 2:
        obox(mr, (xm + 1.0, yv + 0.65, WH + 1.2), XX, YY, ZZ, 1.0, 0.65, 1.2, M['rammed'], uvk=0.2); obox(mr, (xm + 1.0, yv + 0.65, WH + 2.5), XX, YY, ZZ, 1.18, 0.82, 0.14, M['wood_d'], uvk=0.4); xm += 3.4
    wd = Bk('wood', hull=hd)
    for (xa, xb_) in ((X0 + 2, -22.0), (22.0, X1 - 2)):                                                         # timber rail along the inner edge of the walk
        for xp in np.arange(xa, xb_, 4.0): rod(wd, V((xp, yi(WH) - 0.2, WH)), V((xp, yi(WH) - 0.2, WH + 1.9)), 0.11, M['wood_d'], seg=5)
        obox(wd, ((xa + xb_) / 2, yi(WH) - 0.2, WH + 1.9), XX, YY, ZZ, (xb_ - xa) / 2, 0.1, 0.1, M['wood_d']); obox(wd, ((xa + xb_) / 2, yi(WH) - 0.2, WH + 1.0), XX, YY, ZZ, (xb_ - xa) / 2, 0.08, 0.08, M['wood'])
    # gate: tunnel lintel + two heavy leaves that swing (set_gate), a warm glow plane inside the passage seen through the crack
    gx, gw, gh = 0.0, GATE_W * 2, GATE_H; y0, y1 = yo(gh) - 0.1, yi(gh) + 0.1
    obox(wd, (gx, (y0 + y1) / 2, gh + 0.35), XX, YY, ZZ, gw / 2 + 0.7, (y1 - y0) / 2 + 0.2, 0.42, M['wood_d'], uvk=0.5)
    for sx in (gx - gw / 2 - 0.35, gx + gw / 2 + 0.35):
        for ys in (yo(gh * 0.5) - 0.12, yi(gh * 0.5) + 0.12): obox(wd, (sx, ys, gh / 2), XX, YY, ZZ, 0.35, 0.35, gh / 2, M['wood_d'], uvk=0.5)
    if loc == 'jimo_out': fl = Bk('gateglow', shadow=False); flat(fl, V((gx - gw / 2, -0.4, 0.2)), V((gw, 0, 0)), V((0, 0, gh - 0.3)), M['gate_glow'])
    STATE['gate_leaves'] = []
    for sgn in (-1, 1):
        hx = gx + sgn * gw / 2; lb = MB()
        def P_(dx, y, z): return V((hx - sgn * dx, y, z))
        yy = yo(gh * 0.5) + 1.3; w2 = gw / 2 - 0.08
        obox(lb, (hx - sgn * w2 / 2, yy, gh / 2), XX, YY, ZZ, w2 / 2, 0.28, gh / 2 - 0.1, M['planks_d'], uvk=0.5)
        for zz in (gh * 0.22, gh * 0.52, gh * 0.8): obox(lb, (hx - sgn * w2 / 2, yy - 0.3, zz), XX, YY, ZZ, w2 / 2 - 0.05, 0.1, 0.16, M['iron'])
        for ix in range(4):
            for iz in range(5): lb.sphere(V((hx - sgn * (0.5 + ix * 0.8), yy - 0.32, 1.0 + iz * 1.6)), 0.1, M['bronze'], seg=6, rings=4)
        ob = _obj(lb, 'gate_leaf_%s' % ('L' if sgn < 0 else 'R'), STATE['SET'], hull=T.hull(60.0)); localize(ob, (hx, yy, 0.0)); STATE['gate_leaves'].append((ob, sgn, hx, yy))
    STATE['holes_state'] = {}

def breach_decor(Bk, M, i, hx):
    """Breach i: ragged rim (stepped chamfer blocks + clods on both faces), rubble fan + raw props outside, a heap of dug earth with a pick + basket inside."""
    r = _rnd(100 + i); w, h = HOLE_W, HOLE_H; hd = T.hull(40.0)
    rm = Bk('breach%d' % i, hull=hd); rb = Bk('rubble%d' % i, hull=hd); dg = Bk('dig%d' % i, hull=hd)
    for (yf, sg) in ((yo(h), -1), (yi(h), 1)):                                                                   # both faces
        for sx in (-1, 1):
            for k, (dz, dx_) in enumerate(((0.0, 0.0), (-0.9, 0.5), (-1.9, 0.85))):
                obox(rm, (hx + sx * (w / 2 - 0.2 - dx_ * 0.35), yf + sg * 0.3, h + dz - 0.1), XX, YY, ZZ, 0.5 + r.uniform(0, 0.35), 0.5, 0.42 + r.uniform(0, 0.25), M['rammed'], uvk=0.3)
        for k in range(8):
            z = r.uniform(0.3, h + 0.5); side = r.choice((-1, 1)); x = hx + side * (w / 2 + r.uniform(-0.25, 0.25)) if z < h else hx + r.uniform(-w / 2, w / 2)
            lumpy(rm, V((x, (yo(z) if sg < 0 else yi(z)) + sg * 0.25, z)), r.uniform(0.3, 0.65), M['rammed'], i * 20 + k + (0 if sg < 0 else 400), seg=7, rings=4, rough=0.35, squash=0.8)
    for k in range(22):                                                                                          # rubble fan outside
        x = hx + r.gauss(0, w * 0.55); y = yo(0) - r.uniform(0.3, 5.0); s_ = r.uniform(0.2, 0.75) * (1.2 - (yo(0) - y) / 8.0)
        lumpy(rb, V((x, y, s_ * 0.35)), max(0.18, s_), M['rammed'] if k % 3 else M['bank'], i * 50 + k, seg=7, rings=4, rough=0.32, squash=0.6)
    for sx in (-1, 1):                                                                                           # raw timber props
        rod(rb, V((hx + sx * (w / 2 + 0.15), yo(0) - 0.35, 0.0)), V((hx + sx * (w / 2 + 0.15), yo(h) - 0.2, h + 0.15)), 0.22, M['wood_d'], seg=6)
        rod(rb, V((hx + sx * (w / 2 + 0.15), yi(0) + 0.35, 0.0)), V((hx + sx * (w / 2 + 0.15), yi(h) + 0.2, h + 0.15)), 0.22, M['wood_d'], seg=6)
    rod(rb, V((hx - w / 2 - 0.3, yo(h) - 0.25, h + 0.05)), V((hx + w / 2 + 0.5, yo(h) - 0.1, h - 0.35)), 0.2, M['wood_d'], seg=6)
    for k in range(5):                                                                                           # inside: the heap of dug earth, a basket, a pick
        lumpy(dg, V((hx + r.uniform(-1.3, 1.3), yi(0) + 1.2 + r.uniform(0, 1.6), 0.5 + 0.3 * (k == 0))), r.uniform(0.9, 1.5) if k < 2 else r.uniform(0.3, 0.7), M['bank'] if k % 2 else M['rammed'], 700 + i * 9 + k, seg=8, rings=5, rough=0.3, squash=0.55)
    bx = hx + (1.6 if i % 2 else -1.6); by = yi(0) + 3.2
    dg.frustum(V((bx, by, 0)), V((bx, by, 1.0)), 0.5, 0.78, M['straw_d'], seg=10); lumpy(dg, V((bx, by, 1.0)), 0.72, M['bank'], 800 + i, seg=8, rings=4, rough=0.2, squash=0.4)
    F = Frame((hx + (-1.5 if i % 2 else 1.5), yi(0) + 2.4, 0.0), r.uniform(0, 360))
    rod(dg, F.p(0, 0, 0.18), F.p(2.4, 0, 0.5), 0.1, M['wood'], seg=5); obox(dg, F.p(2.4, 0, 0.5), F.X, F.Y, F.Z, 0.08, 0.5, 0.12, M['iron'])
    STATE.setdefault('breach_names', []).append(i)

def gate_tunnel_extras(Bk, M, loc): pass

def build_wall(Bk, M, loc):
    wall_shell(Bk, M, loc)
    for i, hx in enumerate(HOLE_X): breach_decor(Bk, M, i, hx)
    wall_dress(Bk, M, loc)
    gate_tower(Bk, M, loc)

def wall_dress(Bk, M, loc):
    """Wall detail on the visible face(s): torches with warm pools, bronze lamps, banners, shields on the merlons, rain streaks, hanging ropes, ladders, a repair scaffold,
    patches, putlog holes, timber lacing, guards on the walk, ramps.  face = 'out' (jimo_out, yan_camp) or 'in' (jimo_in)."""
    hd = T.hull(62.0 if loc != 'yan_camp' else 100.0); r = _rnd(41); wd = Bk('wood', hull=hd); ops = STATE['holes']
    face = 'in' if loc == 'jimo_in' else 'out'; fy = yi if face == 'in' else yo; sg = 1 if face == 'in' else -1
    def clear(xp, z, pad=1.2): return not any(abs(xp - hc) < hw_ / 2 + pad and z < hh_ + pad for hc, hw_, hh_ in ops)
    nrm_out = 'out' == face
    # --- putlog holes + lacing beams + buttress posts
    ph = Bk('putlog', shadow=False)
    for z in (3.0, 7.0, 11.0, 14.0):
        for xp in np.arange(-93.0, 94.0, 4.0):
            if not clear(xp, z): continue
            yy = fy(z) + sg * 0.06; flat(ph, V((xp - 0.3, yy, z - 0.3)), V((0.6, 0, 0)), V((0, 0, 0.6)), M['black'])
    for z in (5.0, 10.0):
        for xp in np.arange(-91.0, 92.0, 22.0): obox(wd, (xp, fy(z) + sg * 0.1, z), XX, YY, ZZ, 6.0, 0.14, 0.16, M['wood_d'], uvk=0.5)
    for xb in np.arange(-88, 90, 11.0):
        if abs(xb) < 13 or not clear(xb, 4): continue
        for z in (3.5, 9.5): obox(wd, (xb, fy(z) + sg * 0.05, z), XX, YY, ZZ, 0.3, 0.14, 0.2, M['wood_d'], uvk=0.5)
    # --- torches along the wall walk: warm pools on the face (painted decal + the wall material's warm weight)
    for xt in (-72, -60, -48, -36, -26, -17, 17, 26, 36, 48, 60, 72):
        ty = (yo(WH) + 1.4) if face == 'out' else (yi(WH) - 1.4)
        c = torch_post(Bk, M, (xt, ty, WH), s=1.5, light=(450.0 if abs(xt) < 50 else 300.0), name='tw%d' % xt, halo_r=3.4, warm=None)
        lamp('ww%d' % xt, (xt, fy(WH) + sg * 1.8, WH - 2.4), 260.0 if abs(xt) < 50 else 160.0, FIRE, r=1.0, shadow=False)
        STATE['warm'].append((V((xt, fy(WH - 2.2), WH - 2.2)), 3.6, 0.9))
        pl = Bk('wallpools', shadow=False); zc = WH - 3.2; yy = fy(zc) + sg * 0.12
        flat(pl, V((xt - 3.6, yy, zc - 3.4)), V((7.2, 0, 0)), V((0, 0, 7.0)), M['pool_w'])
    for xl in (-65, -54, -42, -31, 31, 42, 54, 65):
        oil_lamp(Bk, M, (xl, (yo(WH) + 1.3) if face == 'out' else (yi(WH) - 1.3), WH), s=0.9, light=0.0, h=3.2, halo_r=1.8)
    for i, xb in enumerate((-58, -44, -30, 30, 44, 58)):
        banner(Bk, M, (xb, (yo(WH) + 2.0) if face == 'out' else (yi(WH) - 0.5), WH), 8.5, 3.4, 5.0, M['red'] if i % 2 == 0 else M['teal'], M['gold'], wave=i, yaw=0.0)
    # --- shields on every second merlon
    sh = Bk('shields', hull=hd); yv = yo(WH); x = -93.0 + 1.0; k = 0
    while x < 93:
        if k % 2 == 0 and abs(x) > 14:
            ellipsoid(sh, V((x + 1.0, yv - 0.15, WH + 1.35)), 0.95, 0.22, 0.95, M['hide'] if k % 4 else M['red_d'], seg=12, rings=6, th=(0, math.pi)); sh.sphere(V((x + 1.0, yv - 0.38, WH + 1.35)), 0.2, M['bronze'], seg=6, rings=4)
        x += 3.4; k += 1
    rn = Bk('rainstreaks', shadow=False)
    for xr in np.arange(-90, 90, 9.0):
        if abs(xr) < 12: continue
        flat(rn, V((xr, fy(WH - 7.0) + sg * 0.1, WH - 7.4)), V((9.0, 0, 0)), V((0, 0, 7.4)), M['rain'], (0, 1, 1, 0) if (int(xr) % 2) else (1, 1, 0, 0))
    for (xa, zb) in ((-80, 15.0), (-46.5, 12.0), (24, 14.0), (62, 15.0), (84, 13.0)):
        rod(wd, V((xa, fy(WH) + sg * 0.05, WH + 0.2)), V((xa + 0.2, fy(zb) + sg * 0.2, zb)), 0.1, M['straw_d'], seg=4)
        for kk in range(4): wd.sphere(V((xa + 0.1, fy(zb + kk * 0.9) + sg * 0.15, zb + kk * 0.9)), 0.15, M['straw_d'], seg=4, rings=3)
    for xl in (-38.0, 38.0, 67.0, -67.0):                                                                           # ladders leaning on the face
        if not clear(xl, 6): continue
        zt = 13.5; yb = fy(0) + sg * 3.0
        for sx in (-0.55, 0.55): rod(wd, V((xl + sx, yb, 0.0)), V((xl + sx, fy(zt) + sg * 0.15, zt)), 0.13, M['wood'], seg=5)
        for zz in np.arange(1.0, zt - 0.5, 1.1): yy = yb + (fy(zt) + sg * 0.15 - yb) * zz / zt; rod(wd, V((xl - 0.55, yy, zz)), V((xl + 0.55, yy, zz)), 0.07, M['wood_l'], seg=4)
    xs0 = 52.0 if loc != 'jimo_in' else -56.0                                                                       # repair scaffold at the base
    for sx in (-3.0, 0.0, 3.0): rod(wd, V((xs0 + sx, fy(0) + sg * 2.4, 0.0)), V((xs0 + sx, fy(0) + sg * 2.4, 7.2)), 0.16, M['wood'], seg=5)
    for zz in (3.0, 6.4):
        obox(wd, (xs0, fy(zz) + sg * 1.0, zz), XX, YY, ZZ, 3.6, 1.2, 0.12, M['planks'], uvk=0.5); rod(wd, V((xs0 - 3.0, fy(0) + sg * 2.4, zz - 0.2)), V((xs0 + 3.0, fy(0) + sg * 2.4, zz - 0.2)), 0.12, M['wood_d'], seg=4)
    for xr in (xs0 - 2.2, xs0 + 2.0): rod(wd, V((xr, fy(3.0) + sg * 1.0, 3.1)), V((xr + 0.2, fy(3.0) + sg * 0.9, 5.4)), 0.35, M['hay'], seg=6)
    pt = Bk('patches', hull=hd)
    for k in range(22):
        xp = r.choice((-1, 1)) * r.uniform(14, 90); zp = r.uniform(2.0, 13.0); pw, ph_ = r.uniform(1.6, 3.4), r.uniform(1.0, 2.0)
        if not clear(xp, zp, 2.5) or (abs(xp) < 12 and zp < 11): continue
        obox(pt, (xp, fy(zp) + sg * 0.06, zp), XX, YY, ZZ, pw / 2, 0.07, ph_ / 2, M['rammed_d'] if k % 2 else M['bank'], uvk=0.4)
        for dz_ in (ph_ / 2, -ph_ / 2): obox(pt, (xp, fy(zp + dz_) + sg * 0.1, zp + dz_), XX, YY, ZZ, pw / 2, 0.06, 0.06, M['wood_d'], uvk=0.5)
    # --- ramp up the face at the far end (timber steps on a slope) and, on the inner face, the earth ramps
    xr = 76.0 if face == 'out' else -76.0
    if face == 'out':
        for sx in (-1.6, 1.6): beam(wd, V((xr + sx, yo(0) - 7.0, 0.1)), V((xr + sx, yo(WH * 0.8) - 0.4, WH * 0.8)), 0.25, 0.3, M['wood_d'], up=(0, 1, 0))
        for kk in range(12):
            t = (kk + 0.5) / 12; obox(wd, (xr, yo(0) - 7.0 + (yo(WH * 0.8) - 0.4 - yo(0) + 7.0) * t, WH * 0.8 * t + 0.1), XX, YY, ZZ, 1.8, 0.45, 0.06, M['planks'], uvk=0.5)
    else:
        for xr_ in (-62.0, 62.0):
            for sx in (-2.2, 2.2): beam(wd, V((xr_ + sx, yi(0) + 15.0, 0.1)), V((xr_ + sx, yi(WH) + 0.3, WH)), 0.3, 0.35, M['wood_d'], up=(0, 1, 0))
            for kk in range(26):
                t = (kk + 0.5) / 26; obox(wd, (xr_, yi(0) + 15.0 + (yi(WH) + 0.3 - yi(0) - 15.0) * t, WH * t + 0.1), XX, YY, ZZ, 2.2, 0.35, 0.07, M['planks'], uvk=0.5)

def gate_tower(Bk, M, zone):
    """Warring-States gate hall: a two-stage timber hall on the wall top with dark-lacquer posts, plain grey hip roofs with near-straight eaves and wadang
    eaves tiles (no curled horns), simple block brackets, bronze standing lamps and braziers instead of paper lanterns, plain dyed banners."""
    wd = Bk('tower', hull=T.hull(62.0 if zone != 'yan_camp' else 100.0)); z0 = WH; cz = 0.0; yc = (yo(WH) + yi(WH)) / 2
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
    rf = Bk('roof', hull=T.hull(62.0 if zone != 'yan_camp' else 100.0))
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


# ----------------------------------------------------------------------------- moat (water near the gate / beyond |x| 46, a dry silted ditch between), bridge, road, fields, far camp
WATER_X = [(-260.0, -46.0), (-12.5, 12.5), (46.0, 260.0)]; DRY_X = [(-46.0, -12.5), (12.5, 46.0)]
def over_water(x): return any(a <= x <= b for a, b in WATER_X)

def moat_road(Bk, M, loc, far=-300.0):
    y0, y1 = MOAT; wz = WATER_Z; bk = Bk('banks'); wt = Bk('water', shadow=False); X, Y, Z = XX, YY, ZZ
    for (xa, xb) in WATER_X:
        flat(wt, V((xa, y0, wz)), V((xb - xa, 0, 0)), V((0, y1 - y0, 0)), M['water'], (0, 0, (xb - xa) / 16, (y1 - y0) / 16))
        flat(bk, V((xa, y1, wz)), V((xb - xa, 0, 0)), V((0, 2.3, -wz)), M['bank'], (0, 0, (xb - xa) / 8, 0.6)); flat(bk, V((xa, y0, 0.0)), V((xb - xa, 0, 0)), V((0, 2.5, wz)), M['bank'], (0, 0, (xb - xa) / 8, 0.6))
    for (xa, xb) in DRY_X:                                                                                        # dry ditch: sloped banks + a muddy floor with reed tufts
        fz = -1.2
        flat(bk, V((xa, y1, fz)), V((xb - xa, 0, 0)), V((0, 2.3, -fz)), M['bank'], (0, 0, (xb - xa) / 8, 0.6)); flat(bk, V((xa, y0, 0.0)), V((xb - xa, 0, 0)), V((0, 2.5, fz)), M['bank'], (0, 0, (xb - xa) / 8, 0.6))
        flat(bk, V((xa, y0 + 2.5, fz)), V((xb - xa, 0, 0)), V((0, y1 - y0 - 4.8, 0)), M['earth'], (0, 0, (xb - xa) / 8, 2.0))
        r = _rnd(int(xa)); gr = Bk('tufts')
        for k in range(36):
            x, y = r.uniform(xa, xb), r.uniform(y0 + 3, y1 - 2)
            for kk in range(3): a = r.uniform(0, 6.28); gr.frustum(V((x, y, fz)), V((x + 0.3 * math.cos(a), y + 0.3 * math.sin(a), fz + r.uniform(0.7, 1.4))), 0.16, 0.0, M['leaf'] if kk % 2 else M['grass2'], seg=3, cap1=False)
    rd = Bk('road'); flat(rd, V((-5.5, y0, 0.03)), V((11.0, 0, 0)), V((0, far - y0, 0)), M['road'], (0, 0, 11 / 8, (y0 - far) / 8))
    rd.face([V((-5.5, y1 + 2.3, 0.03)), V((-5.5, yo(0), 0.03)), V((5.5, yo(0), 0.03)), V((5.5, y1 + 2.3, 0.03))][::-1], M['road'], [(0, 0), (0, 1), (1, 1), (1, 0)][::-1])
    br = Bk('bridge', hull=T.hull(60.0)); yb0, yb1 = y0 - 0.5, y1 + 2.3                                              # timber bridge: deck, beams, posts, rails, piles
    obox(br, (0, (yb0 + yb1) / 2, 0.12), X, Y, Z, 4.2, (yb1 - yb0) / 2, 0.14, M['planks'], uvk=0.5)
    for sx in (-3.8, -1.3, 1.3, 3.8): obox(br, (sx, (yb0 + yb1) / 2, -0.45), X, Y, Z, 0.28, (yb1 - yb0) / 2, 0.38, M['wood_d'], uvk=0.5)
    for yy in np.linspace(yb0 + 1.5, yb1 - 1.5, 4):
        for sx in (-3.8, 3.8): rod(br, (sx, yy, WATER_Z - 0.5), (sx, yy, 0.0), 0.34, M['wood_d'], seg=7)
        obox(br, (0, yy, -0.2), X, Y, Z, 4.2, 0.22, 0.2, M['wood_d'])
    for sx in (-4.1, 4.1):
        for yy in np.linspace(yb0 + 0.4, yb1 - 0.4, 6): rod(br, (sx, yy, 0.2), (sx, yy, 2.2), 0.2, M['red'], seg=7)
        obox(br, (sx, (yb0 + yb1) / 2, 1.9), X, Y, Z, 0.14, (yb1 - yb0) / 2, 0.16, M['red']); obox(br, (sx, (yb0 + yb1) / 2, 1.0), X, Y, Z, 0.1, (yb1 - yb0) / 2, 0.1, M['wood'])
    for yy in (yb1 - 0.4, yb1 - 6.0):
        for sx in (-4.1, 4.1): oil_lamp(Bk, M, (sx, yy, 0.25), s=0.85, light=(110.0 if yy > yb1 - 1 else 0.0), name='bl%d%d' % (int(sx), int(yy)), halo_r=1.6, h=3.0)
    st = Bk('streaks', shadow=False); wz2 = wz + 0.03; cam = V(STATE['cam']['loc'])
    for xt in (-72, -60, -48, 48, 60, 72):                                                                           # wall torch reflections on the water beyond |x| 46
        if not over_water(xt): continue
        xs = xt + (xt - cam.x) * (-0.18); wd_ = 1.2; L = 19.0
        st.face([V((xs - wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 + 0.05, wz2)), V((xs + wd_, y1 - L, wz2)), V((xs - wd_, y1 - L, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    for xl in (-9.8, -4.2, 4.2, 9.8): st.face([V((xl - 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 + 0.05, wz2)), V((xl + 1.0, y1 - 16, wz2)), V((xl - 1.0, y1 - 16, wz2))], M['streak'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    for k in range(6): halo(Bk('halos', shadow=False), V((-60 + k * 24, -16, 0.5)), 16.0, M['mist'])

def tree(Bk, M, p, s=1.0, seed=0, cd=60.0):
    r = _rnd(seed); tb = Bk('trees', hull=T.hull(cd)); p = V(p)
    rod(tb, p, p + V((0, 0, 3.2 * s)), 0.28 * s, M['wood_d'], seg=6, r1=0.18 * s)
    for k in range(4): lumpy(tb, p + V((r.uniform(-0.6, 0.6) * s, r.uniform(-0.6, 0.6) * s, (3.4 + 1.0 * k) * s)), (2.0 - 0.28 * k) * s, M['leaf'] if (seed + k) % 2 else M['grass2'], seed * 7 + k, seg=8, rings=5, rough=0.25, squash=0.8)

def fields_and_road(Bk, M, loc, light, far=-300.0):
    g = Bk('ground'); S_ = 330.0
    flat(g, V((-S_, MOAT[0] - 270, 0)), V((2 * S_, 0, 0)), V((0, 270, 0)), M['grass'], (-S_ / 8, 0, S_ / 8, 270 / 8))                                   # grass beyond the moat
    flat(g, V((-S_, MOAT[1] + 2.3, 0)), V((2 * S_, 0, 0)), V((0, 400, 0)), M['earth'], (-S_ / 8, 0, S_ / 8, 400 / 8))                                   # berm and the city side
    fd = Bk('fields')
    for (x0, x1, mat) in ((-S_, -9.0, 'fields'), (9.0, S_, 'fields_b')):
        pass
    fl = STATE['M']['fields']; fl2 = STATE['M']['fields_b']
    flat(fd, V((-S_, MOAT[0] - 270, 0.02)), V((S_ - 8.0, 0, 0)), V((0, 270 - 14, 0)), fl, (-S_ / 64, 0, -8.0 / 64, (270 - 14) / 64))
    flat(fd, V((8.0, MOAT[0] - 270, 0.02)), V((S_ - 8.0, 0, 0)), V((0, 270 - 14, 0)), fl2, (8.0 / 64, 0, S_ / 64, (270 - 14) / 64))
    r = _rnd(12)
    for k in range(70):                                                                                          # trees: clumps and hedge lines away from the road
        x = r.choice((-1, 1)) * (r.uniform(16, 140) if k % 3 else r.uniform(70, 200)); y = r.uniform(-250, -40)
        tree(Bk, M, (x, y, 0), s=r.uniform(0.8, 1.5), seed=k, cd=max(40.0, abs(y)))
    hb = Bk('hay', hull=T.hull(60.0))
    for k in range(18):
        x = r.choice((-1, 1)) * r.uniform(14, 70); y = r.uniform(-130, -40); c = V((x, y, 0)); hb.frustum(c, c + V((0, 0, 2.4)), 1.8, 0.3, M['hay'], seg=8); cyl(hb, c + V((0, 0, 0.1)), 1.9, 0.5, M['straw_d'], seg=8)
    for k in range(12):                                                                                          # wooden fence posts and rails beside the road
        pass
    sk = Bk('posts', hull=T.hull(60.0)); lt = light != 'DAWN'
    for k, y in enumerate(range(-45, -190, -24)):
        for sx in (-9.5, 9.5):
            rod(sk, V((sx, y, 0)), V((sx, y, 2.4)), 0.16, M['wood_d'], seg=5)
            if lt and k < 4 and sx > 0: torch_post(Bk, M, (sx, y, 0.0), s=1.2, light=260.0, name='rd%d' % k, halo_r=3.0)
    # dropped things on the road shoulder (the camp is near, the road is used): a cart wheel and a broken spear
    return g

def far_camp(Bk, M, loc, light, y0=-150.0):
    """The Yan camp seen from the wall: tents, fires, a palisade line, pennants (cheap silhouettes + live flames without lights)."""
    r = _rnd(77); tb = Bk('fartents', hull=T.hull(150.0)); gl = Bk('farglow', shadow=False); hl = Bk('halos', shadow=False)
    for k in range(34):
        x = -70 + (k % 9) * 17.5 + r.uniform(-4, 4); y = y0 - 6 - (k // 9) * 16 - r.uniform(0, 5); w, l, h = r.uniform(8, 11), r.uniform(10, 13), r.uniform(5, 7)
        F = Frame((x, y, 0), r.uniform(-12, 12)); mat = M['hide'] if k % 3 == 0 else M['canvas']
        for sgn in (-1, 1): tb.oface([F.p(sgn * w / 2, -l / 2, 0), F.p(sgn * w / 2, l / 2, 0), F.p(0, l / 2, h), F.p(0, -l / 2, h)], mat, [(0, 0), (l / 4, 0), (l / 4, 1.5), (0, 1.5)], F.X * sgn + F.Z * 0.9)
        for yy_, n_ in ((-l / 2, -1), (l / 2, 1)): tb.oface([F.p(-w / 2, yy_, 0), F.p(w / 2, yy_, 0), F.p(0, yy_, h)], mat, [(0, 0), (1, 0), (0.5, 1)], F.Y * n_)
        if k % 2 == 0: flat(gl, F.p(-w * 0.12, -l / 2 - 0.1, 0.0), F.X * (w * 0.24), F.Z * (h * 0.42), M['win'])
    for k in range(9):
        x = -60 + k * 15 + r.uniform(-3, 3); y = y0 + r.uniform(-3, 8)
        if light != 'DAWN': live_flame(V((x, y, 0.2)), 3.0, 0.8, lean=(0.2, 0.1), seed=k, n=3, spread=0.4, light=0.0, name='farfire', warm=None); halo(hl, V((x, y, 2.0)), 9.0, M['halo'])
    pl = Bk('palisade', hull=0.0)
    for k in range(-90, 91):
        x = k * 0.9; h = 5.6 + r.uniform(-0.4, 0.6); pl.frustum(V((x, y0 + 12 + r.uniform(-0.1, 0.1), 0)), V((x, y0 + 12, h)), 0.3, 0.3, M['wood'] if k % 3 else M['wood_d'], seg=5, cap0=False, cap1=False)
    for k in range(10):
        x = -66 + k * 15; banner(Bk, M, (x, y0 + 10 + r.uniform(-2, 2), 0.0), 14.0, 4.2, 2.4, M['black'], M['red'], wave=k, yaw=r.uniform(-20, 20))

def build_out(Bk, M, light):
    loc = 'jimo_out'
    build_wall(Bk, M, loc); city(Bk, M, loc); moat_road(Bk, M, loc); fields_and_road(Bk, M, loc, light); far_camp(Bk, M, loc, light)
    foreground(Bk, M); hills(Bk, M, (0.0, -80.0), 230.0, 290.0, 26, 7, (40, 70))
