"""jimo_props.py : round-8 shared props of the film-18 set (exposed as J.prop_* and J.gapfill by jimo.py; see API.md "Round-8 shared assets").

All props are built about their own origin, linked into the scene's SET collection, inked with the 3 px inverted hull (`T.hull(cd)`, cd = the
camera distance the 3 px is tuned for, default 12 D), lit by the set's own materials (so they follow the NIGHT / DUSK / DAWN preset of the
current build) and hidden from bounce rays.  `loc` is a world point, `rot` a Euler (x, y, z) in RADIANS (or one number = yaw about z).
Local frame: +Z up, the long axis / front is +X for the reed bundle, the chariot and the helmet's front is -Y (like the cast cards).
J = the jimo module (bound by jimo.py)."""
import math
import bpy
from mathutils import Vector as V, Matrix, Euler

J = None
_N = [0]


def bind(j):
    global J
    J = j


def _rng(seed):
    return J._rnd(seed)


def _M(hexcol, gain=1.1, sm=1.0):
    """a set-lit flat material of this colour (cached in STATE['M'] under 'p_<hex>')."""
    M = J.STATE['M']; key = 'p_%s_%g_%g' % (hexcol.lstrip('#'), gain, sm)
    if key not in M:
        FORM = tuple(J.STATE['P']['form'])
        M[key] = J._untoon(J.T.mat_lit('%sp_%s_%g_%g' % (J.STATE['pre'], hexcol.lstrip('#'), gain, sm), hexcol, gain=gain, shade_mul=sm, form=FORM))
    return M[key]


def _rot(rot):
    if rot is None: return (0.0, 0.0, 0.0)
    if isinstance(rot, (int, float)): return (0.0, 0.0, float(rot))
    return tuple(rot)


def _finish(mb, name, loc, rot, cd, smooth=False, parent=None, scale=1.0):
    """flush one mesh bank to an object (ink hull, no bounce, shadow on) at loc / rot."""
    ob = mb.obj(name, J.STATE['SET'], hull=J.T.hull(cd) * max(scale, 0.3) ** 0.0)
    if smooth:
        for p in ob.data.polygons: p.use_smooth = True
    J.no_bounce(ob)
    ob.location = loc; ob.rotation_euler = Euler(_rot(rot), 'XYZ')
    if parent is not None: ob.parent = parent
    J.STATE.setdefault('props', []).append(ob)
    return ob


def _name(kind):
    _N[0] += 1
    return 'prop_%s_%d' % (kind, _N[0])


# ----------------------------------------------------------------------------- reed bundle
def prop_reed_bundle(loc=(0, 0, 0), rot=None, scale=1.0, n=60, seed=1, cd=4.0):
    """A bundle of `n` (40-80) thin reed stalks, 1.2 D long and 0.35 D thick at scale 1, tied with 2 red cords, long axis +X.  The bundle is
    fattest in the middle and fanned at one end (the cut stalks splay about 25 %), each stalk a tapered 5-sided rod with its own tone
    (ochre -> straw -> pale) and a little random splay, so it reads as a round bundle of stalks, not a slab.  Returns the object."""
    n = max(40, min(80, int(n))); r = _rng(seed); s = scale
    tones = [_M('#b8821e', 1.0), _M('#c89a38', 1.05), _M('#d8b860', 1.1), _M('#9a6418', 1.0), _M('#c08a2c', 1.05), _M('#d8b04a', 1.1), _M('#a87420', 1.0), _M('#e8cc84', 1.1)]
    red = J.STATE['M']['red']; mb = J.Banks()('x', hull=0.0); L = 1.2
    for i in range(n):
        a = r.uniform(0, 2 * math.pi); rr = 0.150 * math.sqrt(r.uniform(0.02, 1.0))            # a filled disc of stalks (radius 0.15 + stalk radius = 0.35 thick)
        y, z = rr * math.cos(a), rr * math.sin(a)
        x0 = -L / 2 + r.uniform(-0.03, 0.05); x1 = L / 2 + r.uniform(-0.12, 0.03)
        sp0, sp1 = 1.0 + r.uniform(0.0, 0.15), 1.0 + 0.55 * r.uniform(0.3, 1.0)               # tied end: tight; free end: fans out
        mid = (x0 + x1) / 2; bulge = 1.12
        p0 = V((x0, y * sp0, z * sp0)); pm = V((mid, y * bulge, z * bulge)); p1 = V((x1, y * sp1 * 1.4 + r.uniform(-0.03, 0.03), z * sp1 * 1.4 + r.uniform(-0.03, 0.03)))
        rad = r.uniform(0.026, 0.038); m = tones[r.randrange(len(tones))]
        J.rod(mb, p0 * s, pm * s, rad * s, m, seg=5, r1=rad * 1.05 * s); J.rod(mb, pm * s, p1 * s, rad * 1.05 * s, m, seg=5, r1=rad * 0.6 * s)
    for cx, wd in ((-0.20, 0.036), (0.30, 0.036)):                                             # two red cords: rings of short rods round the bundle
        k = 14; R = 0.178
        for j in range(k):
            a0, a1 = 2 * math.pi * j / k, 2 * math.pi * (j + 1) / k
            J.rod(mb, V((cx * s, R * s * math.cos(a0), R * s * math.sin(a0))), V((cx * s, R * s * math.cos(a1), R * s * math.sin(a1))), wd * s, red, seg=5)
        J.rod(mb, V((cx * s, R * s, 0)), V(((cx + 0.04) * s, (R + 0.07) * s, -0.04 * s)), 0.03 * s, red, seg=4)   # the knot's tail
    return _finish(mb, _name('reed_bundle'), loc, rot, cd * 1.0, scale=s)


# ----------------------------------------------------------------------------- lathe pots
def _lathe(mb, prof, seg=22, mat=None, bands=None):
    """prof = [(r, z), ...] from the bottom centre up the outside, over the rim and down the inside; bands = {segment index: material}."""
    mb.pid += 1
    rings = [[V((r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), z)) for i in range(seg)] for (r, z) in prof]
    for k in range(len(prof) - 1):
        m = (bands or {}).get(k, mat)
        for i in range(seg):
            j = (i + 1) % seg
            mb.face([rings[k][i], rings[k][j], rings[k + 1][j], rings[k + 1][i]], m)


def _spline(pts, sub=3):
    """Catmull-Rom through (r, z) points: a smooth profile."""
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        for t in [k / float(sub) for k in range(sub)]:
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * P[i][c]) + (-P[i - 1][c] + P[i + 1][c]) * t + (2 * P[i - 1][c] - 5 * P[i][c] + 4 * P[i + 1][c] - P[i + 2][c]) * t2 + (-P[i - 1][c] + 3 * P[i][c] - 3 * P[i + 1][c] + P[i + 2][c]) * t3) for c in (0, 1)))
    out.append(pts[-1])
    return [(max(0.0, r), z) for r, z in out]


def prop_pot(loc=(0, 0, 0), rot=None, kind='jar', scale=1.0, cd=10.0, seed=1):
    """A lathe-turned terracotta pot (warm clay #b9552a, darker shoulder band, lighter lip), open at the top with a real inner wall.
    kind 'jar' (1.45 D tall, 1.25 D wide: foot, round belly, shoulder, narrow neck, flared lip), 'bowl' (0.5 D tall, 1.25 D wide: foot ring,
    sloped wall, thick rim) or 'pot' (1.0 D tall, 1.3 D wide cooking pot: round belly, short neck, rolled rim, two lug handles).  Returns the object."""
    assert kind in ('jar', 'bowl', 'pot'), kind
    s = scale; body = _M('#b9552a', 1.0); band = _M('#7a3a20', 0.95); lip = _M('#d07a46', 1.05); dark = _M('#5a2e1c', 0.9)
    mb = J.Banks()('x', hull=0.0)
    if kind == 'jar':
        outer = _spline([(0.0, 0.0), (0.30, 0.0), (0.33, 0.07), (0.58, 0.40), (0.63, 0.68), (0.52, 1.02), (0.32, 1.20), (0.27, 1.34), (0.40, 1.43)], 3)
        rim = [(0.44, 1.46), (0.38, 1.47), (0.30, 1.40)]
        inner = [(0.22, 1.30), (0.24, 1.10), (0.46, 0.80), (0.30, 0.50), (0.0, 0.46)]
    elif kind == 'bowl':
        outer = _spline([(0.0, 0.0), (0.26, 0.0), (0.30, 0.05), (0.50, 0.20), (0.62, 0.42)], 3)
        rim = [(0.66, 0.50), (0.60, 0.51)]
        inner = [(0.54, 0.40), (0.38, 0.20), (0.0, 0.12)]
    else:
        outer = _spline([(0.0, 0.0), (0.30, 0.0), (0.36, 0.05), (0.60, 0.30), (0.66, 0.55), (0.52, 0.82), (0.40, 0.94), (0.46, 1.02)], 3)
        rim = [(0.52, 1.06), (0.44, 1.07), (0.36, 0.98)]
        inner = [(0.34, 0.90), (0.50, 0.70), (0.58, 0.45), (0.30, 0.16), (0.0, 0.12)]
    prof = [(r * s, z * s) for r, z in outer + rim + inner]
    bands = {}
    zs = [p[1] for p in prof]; zmax = max(zs)
    for k in range(len(prof) - 1):
        zm = (prof[k][1] + prof[k + 1][1]) / 2 / s; rmid = (prof[k][0] + prof[k + 1][0]) / 2 / s
        zt = {'jar': (0.72, 1.00), 'bowl': (0.30, 0.38), 'pot': (0.62, 0.84)}[kind]
        if k < len(outer) - 1 and zt[0] <= zm <= zt[1] and (rmid > 0.4): bands[k] = band
        if len(outer) - 1 <= k < len(outer) + len(rim) - 1: bands[k] = lip
        if k >= len(outer) + len(rim) - 1: bands[k] = dark if prof[k][1] / s < 0.6 * zmax / s else body
    _lathe(mb, prof, seg=22, mat=body, bands=bands)
    if kind == 'pot':
        for sg in (-1, 1):                                                                  # two lug handles (little loops)
            c = V((sg * 0.64 * s, 0, 0.62 * s)); pts = [c + V((sg * 0.0, 0, -0.10 * s)), c + V((sg * 0.16 * s, 0, -0.06 * s)), c + V((sg * 0.18 * s, 0, 0.08 * s)), c + V((sg * 0.02 * s, 0, 0.12 * s))]
            for a, b in zip(pts[:-1], pts[1:]): J.rod(mb, a, b, 0.045 * s, body, seg=6)
    return _finish(mb, _name('pot_' + kind), loc, rot, cd, smooth=True, scale=s)


# ----------------------------------------------------------------------------- bronze helmet
def prop_helmet(loc=(0, 0, 0), rot=None, scale=1.0, cd=10.0):
    """A bronze Warring-States helmet, front toward -Y, neck-guard edge on z = 0 (brim at z 0.4), about 0.95 D wide and 1.45 D tall with the plume: a domed skull with a
    brow band and rivets, a lamellar NECK GUARD flaring out at the back (4 stacked plates), two short ear flaps, a crown socket and a RED plume
    tuft (a fan of 11 curved strands) that sweeps back.  Hollow (open underneath).  Returns the object."""
    s = scale; M = J.STATE['M']; bronze = _M('#9a6420', 0.8, 1.2); bz_d = _M('#6a4418', 0.9, 1.3); red = _M('#ff4a2a', 1.6, 3.0); red_d = _M('#d03420', 1.4, 2.6)
    mb = J.Banks()('x', hull=0.0); R = 0.46; seg = 24
    pts = [(R * 1.00, 0.0), (R * 1.02, 0.05), (R * 1.0, 0.10)]
    for a in range(10, 91, 10):
        t = math.radians(a); pts.append((R * math.cos(t) * 0.98, 0.10 + 0.46 * math.sin(t)))
    pts[-1] = (0.0, 0.56)
    pts += [(0.0, 0.50), (R * 0.90, 0.12), (R * 0.88, 0.0), (R * 1.0, 0.0)]                  # over the dome, down the inside, closing the brim
    prof = [(r * s, z * s) for r, z in pts]
    _lathe(mb, prof, seg=seg, mat=bronze, bands={0: bz_d, 1: bz_d, 2: bronze, len(prof) - 2: bz_d, len(prof) - 3: bz_d})
    for i in range(12):                                                                       # brow-band rivets
        a = 2 * math.pi * i / 12 + 0.1
        mb.sphere(V((R * 1.035 * s * math.cos(a), R * 1.035 * s * math.sin(a), 0.05 * s)), 0.028 * s, M['gold'], seg=5, rings=3)
    for (z0, z1, r0, r1) in ((0.06, -0.06, 0.50, 0.56), (-0.05, -0.17, 0.56, 0.62), (-0.16, -0.28, 0.62, 0.68), (-0.27, -0.39, 0.67, 0.74)):   # neck guard plates: back arc (+Y side)
        mb.pid += 1; k = 14; a0, a1 = math.radians(20), math.radians(160)
        for i in range(k):
            t0 = a0 + (a1 - a0) * i / k; t1 = a0 + (a1 - a0) * (i + 1) / k
            q = lambda r, z, t: V((r * s * math.cos(t), r * s * math.sin(t), z * s))
            mb.face([q(r0, z0, t0), q(r0, z0, t1), q(r1, z1, t1), q(r1, z1, t0)], bronze if i % 2 else bz_d)
            mb.face([q(r0 - 0.03, z0, t1), q(r0 - 0.03, z0, t0), q(r1 - 0.03, z1, t0), q(r1 - 0.03, z1, t1)], bz_d)
    for sg in (-1, 1):                                                                        # ear flaps
        mb.pid += 1; k = 5; a0, a1 = (math.radians(-18), math.radians(18)) if sg > 0 else (math.radians(162), math.radians(198))
        for i in range(k):
            t0 = a0 + (a1 - a0) * i / k; t1 = a0 + (a1 - a0) * (i + 1) / k
            q = lambda r, z, t: V((r * s * math.cos(t), r * s * math.sin(t), z * s))
            mb.face([q(0.50, 0.06, t0), q(0.50, 0.06, t1), q(0.54, -0.20, t1), q(0.54, -0.20, t0)], bronze)
            mb.face([q(0.47, 0.06, t1), q(0.47, 0.06, t0), q(0.51, -0.20, t0), q(0.51, -0.20, t1)], bz_d)
    J.cyl(mb, V(0, 0, 0.56 * s) if False else V((0, 0, 0.55 * s)), 0.07 * s, 0.14 * s, bz_d, seg=8, r1=0.05 * s)               # crown socket
    r = _rng(5)
    for i in range(11):                                                                       # the plume tuft: strands sweeping up and back (+Y)
        u = (i - 5) / 5.0; ang = u * 0.55
        p0 = V((0.0, 0.0, 0.68 * s)); L = 0.55 + 0.12 * (1 - abs(u)) + r.uniform(-0.03, 0.03)
        d = V((math.sin(ang) * 1.1, 0.30 + 0.1 * (1 - abs(u)), 1.0)).normalized()
        m = red if i % 3 else red_d; prev = p0
        for k in range(1, 4):
            t = k / 3.0; p = p0 + d * (L * t * s) + V((0, 0.14 * t * t * s, -0.16 * t * t * s))
            J.rod(mb, prev, p, (0.050 - 0.012 * k) * s, m, seg=5); prev = p
    mb.v = [(x, y, z + 0.40 * s) for (x, y, z) in mb.v]                                       # the neck guard's lower edge rests on z = 0
    return _finish(mb, _name('helmet'), loc, rot, cd, smooth=True, scale=s)


# ----------------------------------------------------------------------------- chariot
def _wheel(mb, Rw, s, seg=20):
    """a spoked wheel in the XZ plane about its own centre (axle along Y): felloe ring, 12 spokes, a hub with a red end cap and a bronze cap."""
    M = J.STATE['M']; wd = M['wood_d']; wo = M['wood']
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        J.beam(mb, V((Rw * math.cos(a0), 0, Rw * math.sin(a0))), V((Rw * math.cos(a1), 0, Rw * math.sin(a1))), 0.30 * s, 0.34 * s, wd, up=(0, 1, 0))
    for i in range(12):
        a = 2 * math.pi * i / 12
        J.rod(mb, V(0.12 * s * math.cos(a), 0, 0.12 * s * math.sin(a)) if False else V((0.12 * s * math.cos(a), 0, 0.12 * s * math.sin(a))), V(((Rw - 0.1 * s) * math.cos(a), 0, (Rw - 0.1 * s) * math.sin(a))), 0.075 * s, wo, seg=5, r1=0.06 * s)
    mb.frustum(V((0, -0.36 * s, 0)), V((0, 0.36 * s, 0)), 0.22 * s, 0.22 * s, M['red'], seg=10)
    mb.frustum(V((0, -0.40 * s, 0)), V((0, 0.40 * s, 0)), 0.11 * s, 0.11 * s, M['bronze'], seg=8)


def prop_chariot(loc=(0, 0, 0), rot=None, tumble=0.0, scale=1.0, cd=14.0):
    """A two-wheeled wooden WAR CHARIOT (open box with red rails and a gold top rail, a long pole with a yoke, 2 spoked wheels R 1.5 D), forward +X,
    about 8 D long overall, wheel gap 4.2 D.  Returns the ROOT empty (the children are `<root>_body`, `<root>_wheel_a` (y +) and `<root>_wheel_b`).
    tumble 0..1 = how far it has tipped over and rolled: 0 upright on its wheels, ~0.35 tipping, 0.7 the body lies on its side while the near
    wheel rolls off ahead, 1 wrecked on its side with both wheels loose and lying (pose it again with J.prop_chariot_set(root, tumble, frame) to animate)."""
    s = scale; M = J.STATE['M']; name = _name('chariot')
    root = bpy.data.objects.new(name, None); J.STATE['SET'].objects.link(root); root.location = loc; root.rotation_euler = Euler(_rot(rot), 'XYZ')
    bb = J.Banks()('x', hull=0.0); X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1); g = 2.1 * s; Rw = 1.5 * s
    J.rod(bb, V((0, -g - 0.4 * s, Rw)), V((0, g + 0.4 * s, Rw)), 0.12 * s, M['iron'], seg=6)                                      # axle
    J.obox(bb, V((-0.2 * s, 0, 1.95 * s)), X, Y, Z, 1.5 * s, 1.75 * s, 0.12 * s, M['wood'])                                        # floor
    for sy in (-1, 1):
        J.obox(bb, V((0.0, sy * 1.72 * s, 2.85 * s)), X, Y, Z, 1.4 * s, 0.10 * s, 0.85 * s, M['red'])                                # side rails
        J.obox(bb, V((0.0, sy * 1.72 * s, 3.74 * s)), X, Y, Z, 1.44 * s, 0.14 * s, 0.07 * s, M['gold'])
    J.obox(bb, V((1.42 * s, 0, 2.85 * s)), X, Y, Z, 0.10 * s, 1.75 * s, 0.85 * s, M['red']); J.obox(bb, V((1.42 * s, 0, 3.74 * s)), X, Y, Z, 0.14 * s, 1.8 * s, 0.07 * s, M['gold'])
    for sy in (-1, 1): J.rod(bb, V((-1.2 * s, sy * 0.9 * s, 1.9 * s)), V((-1.2 * s, sy * 0.9 * s, Rw)), 0.11 * s, M['wood_d'], seg=5)   # axle blocks
    J.rod(bb, V((-0.3 * s, 0, 2.0 * s)), V((6.3 * s, 0, 2.55 * s)), 0.18 * s, M['wood'], seg=6)                                      # pole
    J.obox(bb, V((6.4 * s, 0, 2.85 * s)), X, Y, Z, 0.15 * s, 1.5 * s, 0.15 * s, M['wood_d'])                                          # yoke
    for sy in (-1, 1): J.rod(bb, V((6.4 * s, sy * 1.0 * s, 2.7 * s)), V((6.4 * s, sy * 1.0 * s, 3.5 * s)), 0.09 * s, M['bronze'], seg=5)
    J.rod(bb, V((-1.45 * s, 0, 2.0 * s)), V((-1.45 * s, 0, 5.2 * s)), 0.10 * s, M['wood_d'], seg=6)                                   # standard pole + red pennant
    bb.face([V((-1.45 * s, 0, 5.2 * s)), V((-1.45 * s, 0, 4.4 * s)), V((-2.6 * s, 0.0, 4.55 * s)), V((-2.6 * s, 0.0, 5.05 * s))], M['red']); bb.face([V((-1.45 * s, 0, 4.4 * s)), V((-1.45 * s, 0, 5.2 * s)), V((-2.6 * s, 0.0, 5.05 * s)), V((-2.6 * s, 0.0, 4.55 * s))], M['red'])
    body = _finish(bb, name + '_body', (0, 0, 0), None, cd, parent=root, scale=s)
    wh = []
    for tag, sy in (('a', 1), ('b', -1)):
        wb = J.Banks()('x', hull=0.0); _wheel(wb, Rw, s)
        wh.append(_finish(wb, '%s_wheel_%s' % (name, tag), (0, sy * g, Rw), None, cd, parent=root, scale=s))
    root['chariot'] = dict(body=body.name, wheel_a=wh[0].name, wheel_b=wh[1].name, s=s)
    J.STATE.setdefault('chariots', []).append(root)
    prop_chariot_set(root, tumble)
    return root


def _sm(t): t = min(1.0, max(0.0, t)); return t * t * (3 - 2 * t)


def prop_chariot_set(root, tumble, frame=None):
    """Pose a prop_chariot at `tumble` 0..1 (keys LINEAR transforms when `frame` is given, so animate with one call per frame).  The body tips about
    the +Y wheel's ground contact (up to 100 deg, ending on its side, pole flung up), wheel a rolls away ahead and topples, wheel b follows the body
    then drops off; everything stays on the ground plane (z >= 0)."""
    d = root['chariot']; s = d['s']; g = 2.1 * s; Rw = 1.5 * s
    body = bpy.data.objects[d['body']]; wa = bpy.data.objects[d['wheel_a']]; wb = bpy.data.objects[d['wheel_b']]
    t = min(1.0, max(0.0, float(tumble))); e = _sm(t * 1.25)
    th = math.radians(100.0) * e
    R = Matrix.Rotation(-th, 4, 'X'); P = V((0, g, 0)); bl = P - (R @ P) + V((0, 0, 0.12 * s * e))
    J._xf(body, loc=tuple(bl), rot=tuple(R.to_euler()), frame=frame)
    u = _sm((t - 0.30) / 0.70)                                                           # wheel a: rolls off ahead (+X), hops, topples
    x = 9.0 * s * u; hop = 1.1 * s * math.sin(math.pi * min(1.0, u * 1.5)) * (1 - u)
    ta = math.radians(78.0) * _sm((u - 0.45) / 0.55)
    A = Matrix.Rotation(-ta, 4, 'X') @ Matrix.Rotation(x / Rw, 4, 'Y')
    zlift = (Rw * math.cos(ta) + 0.18 * s * math.sin(ta)) if ta > 0 else Rw
    J._xf(wa, loc=(x, g + 1.4 * s * u, max(zlift, 0.2 * s) + hop), rot=tuple(A.to_euler()), frame=frame)
    v = _sm((t - 0.60) / 0.40)                                                           # wheel b: carried with the body, then drops and spins off
    Mb = Matrix.Translation(bl) @ R; pb = Mb @ V((0, -g, Rw))
    Bm = R @ Matrix.Rotation(v * 5.0, 4, 'Y') @ Matrix.Rotation(-math.radians(60) * v, 4, 'X')
    pbz = max(pb.z, 0.2 * s) * (1 - 0.3 * v) + 0.0
    J._xf(wb, loc=(pb.x + 3.5 * s * v, pb.y + 0.8 * s * v, pbz), rot=tuple(Bm.to_euler()), frame=frame)
    root['tumble'] = t
    return root


# ----------------------------------------------------------------------------- gapfill
def gapfill(cam=None, frames=None, z=0.026, mat='bank', maxd=130.0, pad=4.0, retint=True, name='gapfill'):
    """Lay a DARK-EARTH ground plane (the lane dirt texture, M[mat], default 'bank', tile 8 D) just above the base ground and the field quads (z 0.026: under the lane quads
    at 0.03, the furrow strips at 0.05, every prop, herd shadow and wall) under any visible gap of the camera: it covers the convex hull of the ground
    the camera sees up to `maxd` D (padded `pad`), so no flat violet / empty band shows between lanes, herd and wall (s02 / s19 / s20).
    cam = camera object (default the scene camera); frames = film frames of a keyed move (up to 40 samples, default the current frame).
    The moat water (jimo_out / yan_camp) is skipped: the plane is cut away over the moat strip.  retint=True also re-tints the violet furrow strips
    (`furrows`, material 'tunnel') of s19 / s20 to dark earth.  Idempotent (a second call replaces the first).  Returns the plane object or None."""
    sc = bpy.context.scene; cam = cam or sc.camera
    if isinstance(cam, str): cam = bpy.data.objects[cam]
    for ob in list(J.STATE['SET'].objects):
        if ob.name.startswith(name): bpy.data.objects.remove(ob, do_unlink=True)
    keep = sc.frame_current
    fl = [keep] if not frames else list(frames)
    if len(fl) > 40: fl = [fl[int(i * (len(fl) - 1) / 39.0)] for i in range(40)]
    pts = []
    for f in fl:
        sc.frame_set(int(f)); bpy.context.view_layer.update()
        mw = cam.matrix_world; o = mw.translation.copy(); fr = cam.data.view_frame(scene=sc)
        for iy in range(0, 11):
            for ix in range(0, 11):
                c = V(fr[2]) + (V(fr[0]) - V(fr[2])) * (iy / 10.0) * 0 ; w = ix / 10.0; h = iy / 10.0
                lo = V(fr[2]) * (1 - w) + V(fr[3]) * w; hi = V(fr[1]) * (1 - w) + V(fr[0]) * w
                p = lo * (1 - h) + hi * h; dr = (mw.to_3x3() @ p).normalized()
                if dr.z >= -0.01: dr = V((dr.x, dr.y, -0.01)).normalized() if iy > 7 else None
                if dr is None: continue
                tt = (z - o.z) / dr.z
                if tt <= 0: continue
                q = o + dr * min(tt, maxd / max(1e-6, math.hypot(dr.x, dr.y)))
                if math.hypot(q.x - o.x, q.y - o.y) > maxd: q = o + V((dr.x, dr.y, 0)).normalized() * maxd; q.z = z
                pts.append((q.x, q.y)); 
        pts.append((o.x, o.y))
    sc.frame_set(keep); bpy.context.view_layer.update()
    if len(pts) < 3: return None
    hull = _hull(pts)
    cx = sum(p[0] for p in hull) / len(hull); cy = sum(p[1] for p in hull) / len(hull)
    hull = [(cx + (x - cx) + pad * (x - cx) / max(1e-6, math.hypot(x - cx, y - cy)), cy + (y - cy) + pad * (y - cy) / max(1e-6, math.hypot(x - cx, y - cy))) for x, y in hull]
    M = J.STATE['M']; m = M[mat]; mb = J.Banks()('x', hull=0.0)
    cuts = []
    if J.STATE.get('loc') in ('jimo_out', 'yan_camp'):
        try: cuts = [tuple(J.MOAT)]
        except Exception: cuts = []
    polys = [hull]
    for (ya, yb) in cuts:                                                                  # cut the moat strip y in [ya, yb] out of the hull
        polys = [q for p in polys for q in _clip_strip(p, ya, yb)]
    mb.pid += 1
    for p in polys:
        if len(p) < 3: continue
        c0 = (sum(x for x, y in p) / len(p), sum(y for x, y in p) / len(p))
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            mb.face([V((c0[0], c0[1], z)), V((a[0], a[1], z)), V((b[0], b[1], z))] if _ccw(c0, a, b) else [V((c0[0], c0[1], z)), V((b[0], b[1], z)), V((a[0], a[1], z))], m,
                    [(c0[0] / 8, c0[1] / 8), (a[0] / 8, a[1] / 8), (b[0] / 8, b[1] / 8)] if _ccw(c0, a, b) else [(c0[0] / 8, c0[1] / 8), (b[0] / 8, b[1] / 8), (a[0] / 8, a[1] / 8)])
    ob = mb.obj(name, J.STATE['SET'], hull=0.0); ob.visible_shadow = False; J.no_bounce(ob)
    if retint:
        dk = M['bank']
        for o2 in J.STATE['SET'].objects:
            if o2.name.startswith('furrows') and o2.type == 'MESH':
                for i, sl in enumerate(o2.material_slots):
                    if sl.material and sl.material.name == M['tunnel'].name: o2.material_slots[i].material = dk
    J.STATE.setdefault('gapfill_objs', []).append(ob)
    return ob


def _ccw(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0


def _hull(pts):
    P = sorted(set((round(x, 3), round(y, 3)) for x, y in pts))
    if len(P) < 3: return P
    cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _clip_strip(poly, ya, yb):
    """the parts of a convex polygon with y < ya and y > yb (the strip ya..yb removed)."""
    def side(p, keep_lt, y0):
        out = []
        for i in range(len(p)):
            a, b = p[i], p[(i + 1) % len(p)]
            ina = (a[1] <= y0) if keep_lt else (a[1] >= y0); inb = (b[1] <= y0) if keep_lt else (b[1] >= y0)
            if ina: out.append(a)
            if ina != inb:
                t = (y0 - a[1]) / (b[1] - a[1]); out.append((a[0] + t * (b[0] - a[0]), y0))
        return out
    return [q for q in (side(poly, True, min(ya, yb)), side(poly, False, max(ya, yb))) if len(q) >= 3]
