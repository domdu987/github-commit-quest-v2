"""flood.py -- a better molasses wave for film 3 shot 19 (take s18), built at runtime over the harbor set (harbor.py untouched).

The set's own flood (a flat-shaded 0.4 D height field) is hidden.  In its place, per film frame g (pure function of u and g):
  * the same flow field (harbor.flood_height) on a finer 0.35 D grid, smooth shaded, with travelling ripples and flow streaks;
  * a rolling lip: a curled sheet along the front that leans forward over the face of the wave and drops back down;
  * spray: glossy blobs thrown forward and up from the lip, falling back into the wave;
  * a glossy molasses material: toon key + real glossy highlight + an amber fresnel rim (thick, wet, reflective).

    import flood as FL
    FL.init()            # after harbor.build; hides the set's flood
    FL.set(u, g)         # state of the wave at flow parameter u (0..1) on film frame g
"""
import math, random
import bpy
import numpy as np
from mathutils import Vector
import fx

H = fx.H
STEP = 0.35
X0, X1, Y0, Y1 = -8.4, 34.4, -62.0, 22.0
NBLOB = 36
GAIN = 1.6                     # the set's crest (7.7 D) x 1.6: a wave taller than the 10-15 D row houses
S = {}


def _grid():
    xs = np.arange(X0, X1 + 1e-6, STEP); ys = np.arange(Y0, Y1 + 1e-6, STEP)
    return np.meshgrid(xs, ys)


def init():
    M = H.STATE['M']
    M['mol'] = fx.mat_glossy('FL_molasses', '#43160a', gloss=0.035, rough=0.30, rim=0.32)
    M['mol_lip'] = fx.mat_glossy('FL_lip', '#4e1a08', gloss=0.06, rough=0.22, rim=0.42)
    H.STATE['flood'].hide_render = True
    X, Y = _grid(); ny, nx = X.shape
    vs = np.stack([X.ravel(), Y.ravel(), np.full(X.size, -0.08)], 1)
    fs = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    me = bpy.data.meshes.new('fl_surface'); me.from_pydata([tuple(v) for v in vs], [], fs); me.update(); me.materials.append(M['mol'])
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    ob = bpy.data.objects.new('fl_surface', me); fx._coll().objects.link(ob); fx.T.no_bounce(ob)
    S.update(ob=ob, X=X, Y=Y, nx=nx, ny=ny)
    # lip: a sheet along x (street only), profile of NP points
    NX, NP = 64, 14
    S['lip_n'] = (NX, NP)
    vs = [(0, 0, 0)] * (NX * NP)
    fs = [(i * NP + k, (i + 1) * NP + k, (i + 1) * NP + (k + 1) % NP, i * NP + (k + 1) % NP) for i in range(NX - 1) for k in range(NP)]
    me = bpy.data.meshes.new('fl_lip'); me.from_pydata(vs, [], fs); me.update(); me.materials.append(M['mol_lip'])
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons))
    lip = bpy.data.objects.new('fl_lip', me); fx._coll().objects.link(lip); fx.T.no_bounce(lip); S['lip'] = lip
    # blobs
    mb = H.MB(); mb.sphere((0, 0, 0), 1.0, M['mol_lip'], seg=12, rings=7); proto = mb.obj('fl_blob_proto', fx._coll(), smooth=True)
    proto.hide_render = True
    r = random.Random(19); S['blobs'] = []
    for i in range(NBLOB):
        ob = bpy.data.objects.new('fl_blob_%02d' % i, proto.data); fx._coll().objects.link(ob); fx.T.no_bounce(ob); ob.visible_shadow = False
        S['blobs'].append(dict(ob=ob, x=r.uniform(-7.6, 7.6), ph=r.uniform(0, 1), per=r.uniform(14, 26), sz=r.uniform(0.08, 0.24),
                               vy=r.uniform(0.6, 1.4), vz=r.uniform(0.8, 1.6), side=r.uniform(-0.3, 0.3)))
    return M


def burst():
    return H.wall_pt(H.TH_B, H.TANK_R)


def front_y(x, u):
    """y of the wave front (street part) at x for state u."""
    B = burst(); sf = 2.5 + 49.5 * u ** 0.8
    d = sf * sf - (x - B.x) ** 2
    return B.y - math.sqrt(max(d, 0.0))


def crest(u):
    return 4.6 + 3.2 * (1 - u) ** 1.5 + 2.0 * math.sin(math.pi * u)


def set(u, g):
    X, Y = S['X'], S['Y']
    h = H.flood_height(u, X, Y)
    h = np.where(h > 0, h * GAIN, h)
    wet = h > 0
    t = g / 30.0
    rip = (0.10 * np.sin(0.9 * X + 1.7 * Y + 9.0 * t) + 0.07 * np.sin(2.3 * X - 0.8 * Y + 13.0 * t)
           + 0.05 * np.sin(4.1 * X + 3.1 * Y - 7.0 * t))
    streak = 0.12 * np.sin(1.6 * X + 0.25 * Y) * np.clip(h / 3.0, 0, 1)
    h2 = np.where(wet, h + (rip + streak) * np.clip(h / 1.5, 0, 1), h)
    co = np.stack([X.ravel(), Y.ravel(), h2.ravel()], 1)
    me = S['ob'].data; me.vertices.foreach_set('co', co.ravel()); me.update()
    S['ob'].hide_render = u <= 1e-4
    # lip along the street front
    NX, NP = S['lip_n']; lip = S['lip']
    sf = 2.5 + 49.5 * u ** 0.8; B = burst()
    show_lip = u > 0.12 and front_y(0.0, u) < -4.0
    lip.hide_render = not show_lip
    if show_lip:
        Hc = crest(u) * GAIN; pts = []
        for i in range(NX):
            x = -7.95 + 15.9 * i / (NX - 1)
            yf = front_y(x, u)
            hc = Hc * (1 + 0.07 * math.sin(0.9 * x + 0.31 * yf + 5 * u))
            rr = hc * (0.24 + 0.03 * math.sin(t * 4.0 + x * 0.7))
            cy = yf + 0.35 - 0.05 * hc; cz = hc * 0.76
            for k in range(NP):
                a = 2 * math.pi * k / NP + t * 2.5                                   # rolling forward (toward -y over the top)
                pts.append((x, cy - rr * math.sin(a) * 1.15, cz + rr * math.cos(a) + 0.04 * math.sin(3 * x + 7 * t + k)))
        lip.data.vertices.foreach_set('co', np.array(pts).ravel()); lip.data.update()
    # spray blobs
    for b in S['blobs']:
        ob = b['ob']
        if not show_lip:
            ob.hide_render = True; continue
        ph = ((g / b['per']) + b['ph']) % 1.0; tt = ph * b['per'] / 30.0      # seconds since thrown
        yf = front_y(b['x'], u); hc = crest(u) * GAIN
        y = yf - 0.25 * hc - b['vy'] * 6.0 * tt
        z = hc * 1.0 + b['vz'] * 6.0 * tt - 0.5 * 30.0 * tt * tt
        if z < hc * 0.25:
            ob.hide_render = True; continue
        s = b['sz'] * (1.0 - 0.3 * ph) * hc / 8.0
        v = Vector((b['side'] * 6, -b['vy'] * 6.0, b['vz'] * 6.0 - 30.0 * tt))
        ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = v.to_track_quat('Z', 'Y')
        ob.location = (b['x'] + b['side'] * tt * 6, y, z); ob.scale = (s * 0.7, s * 0.7, s * (1.6 + 1.2 * min(1.0, v.length / 12.0)))
        ob.hide_render = False
