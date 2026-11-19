"""h19_ship_land.py : scenery of the ship location (metres, ship frame): cumulus clouds, gulls, rounded hazy headland, far sail, black rocks + fog (rocks),
tropical coast (beach, palms, hills, harbour, boats, fort; Jamaica / Barbados dressings) and rain streaks."""
import os, sys, math, random
import numpy as np
import bpy, bmesh
from mathutils import Vector, Matrix, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h19_kit as K
from h19_kit import mat, mat_emit, MB, hexc, rnd
import h19_ship_hull as HU
from h19_ship_hull import ss, vnoise2, fbm2
import h19_ship_sea as SE
import h19_ship_fx as FX
SC = K.SC

def _mesh_obj(name, verts, faces, mats, midx=None, smooth=True, parent=None):
    ob = HU.mesh_obj(name, verts, faces, mats, midx, smooth)
    if parent is not None: ob.parent = parent
    return ob

# ----------------------------------------------------------------------------- headland: a rounded, hazy green dome with a pale beach line
def land_mat(name, LT, hz=0.38, top='#6f9a78', low='#4f7e68', beach='#e8dcb8', hmax=60.0, zscale=1.0, dist=(300.0, 1100.0), kmax=0.6):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
    def mr(val, a, b, lo=0.0, hi=1.0):
        n = N('ShaderNodeMapRange'); n.inputs['From Min'].default_value = a; n.inputs['From Max'].default_value = b; n.inputs['To Min'].default_value = lo; n.inputs['To Max'].default_value = hi; L(val, n.inputs['Value']); return n.outputs['Result']
    def mix(a, b, f):
        n = N('ShaderNodeMix'); n.data_type = 'RGBA'
        for i, v in ((6, a), (7, b)):
            if hasattr(v, 'node'): L(v, n.inputs[i])
            else: n.inputs[i].default_value = v
        L(f, n.inputs[0]); return n.outputs[2]
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.035 * 60.0 / max(hmax, 1.0) * 1.0; nz.inputs['Detail'].default_value = 5.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    zf = mr(sp.outputs['Z'], 0.0, hmax)
    col = mix(hexc(low), hexc(top), mr(zf, 0.05, 0.75))
    col = mix(col, hexc('#4a7058'), mr(nz.outputs['Fac'], 0.42, 0.6, 0.0, 0.5))
    col = mix(hexc(beach), col, mr(sp.outputs['Z'], 0.25, 1.6))               # pale beach line at the waterline
    cd = N('ShaderNodeCameraData'); dmv = mr(cd.outputs['View Distance'], dist[0] * SC, dist[1] * SC, 0.0, kmax)
    col = mix(col, hexc(LT['haze']), dmv)
    L(col, bs.inputs['Base Color'])
    bs.inputs['Emission Color'].default_value = hexc(LT['haze']); L(_n(nt, 'MULTIPLY', dmv, 0.5), bs.inputs['Emission Strength'])
    L(bs.outputs[0], out.inputs['Surface']); return m
def _n(nt, op, a, b):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; nt.links.new(a, n.inputs[0]); n.inputs[1].default_value = b; return n.outputs[0]

def headland(LT, c, yaw, length, height, depth, seed=3, nx=110, ny=18, name='headland'):
    """rounded smooth dome (sin profile along the length, sin across the depth), several soft lobes; c = waterline centre (x,y); yaw rotates the long axis"""
    rr = np.random.RandomState(seed)
    u = np.linspace(-1, 1, nx); v = np.linspace(0, 1, ny); U, V = np.meshgrid(u, v)
    lobes = [(rr.uniform(-0.7, 0.7), rr.uniform(0.18, 0.4), rr.uniform(0.4, 0.9)) for _ in range(4)]
    prof = np.maximum(0, 1 - np.abs(U) ** 2.0) ** 0.8 * 0.55
    for (cu, w, a) in lobes: prof = prof + a * 0.45 * np.exp(-((U - cu) / w) ** 2)
    prof = prof / prof.max()
    cross = np.sin(np.pi * np.clip(V, 0, 1)) ** 0.75 * (1 - 0.25 * V)
    Z = height * prof * cross * (0.9 + 0.2 * fbm2(U * 3 + 5, V * 3 + 7, seed, 3))
    ca, sa = math.cos(yaw), math.sin(yaw)
    X = U * length / 2; Y = V * depth
    xw = c[0] + X * ca - Y * sa; yw = c[1] + X * sa + Y * ca
    verts = np.stack([xw, yw, Z], -1).reshape(-1, 3)
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    m = land_mat(name, LT, hmax=height)
    ob = _mesh_obj(name, verts, faces, [m], None, True); ob.visible_shadow = False; return ob

# ----------------------------------------------------------------------------- hero scenery (v6 composition mapped into the ship frame)
def scenery(S, P, LT, sea_P, marks):
    kind = P['scenery']; az = LT['az']; el = LT['el']
    kd = kdir_(P['sun_az'], P['sun_el']) if P.get('sun_ship') else SE.v6_dir(kdir_(az, el))
    Pc = dict(cloud=LT['cloud'], key_dir=kd, cloud_k=1.0, cam=dict(loc=P['cam']['loc']))
    FX.cloud_mat6(Pc)
    cl = clouds_for(kind)
    for (nm, pos, size, seed) in cl: FX.cumulus6(Pc, nm, pos, size, seed)
    if kind == 'hero':
        p = SE.v6_pos
        gb = MB('gulls'); mw = mat('gullw', '#f6f5f0', '#e8ecee', scale=6); mt = mat('gullt', '#2e3038')
        for (c, yaw, s, fl) in [((9.2, 30.0, 14.0), 2.2, 0.6, 0.4), ((8.2, 40.0, 28.0), 0.8, 0.55, -0.3), ((-18.5, 50.0, 39.0), 3.4, 0.6, 0.1), ((13.4, 35.0, 9.3), 1.0, 0.45, 0.6), ((11.0, 46.0, 22.0), 2.9, 0.5, 0.0)]:
            FX.gull6(gb, mw, mt, p(c), yaw - SE.PH, s, fl)
        gb.finish(shadow=True)
        # rounded hazy headland on the right horizon + a far two-sail ship
        c0 = p((277.0 + 25 * 4.55, 940.0)); headland(LT, c0, SE.PH * 0 - SE.PH + math.radians(0), 330.0, 40.0, 70.0, seed=3)
        fs = MB('farsail'); x0, y0 = p((150.0, 560.0))[:2]
        sail_m = mat('farcanv', '#e8dcc0', '#dccfae', scale=3, emit='#ffe2a8', emit_k=0.2)
        fs.box(mat('darksail', '#2c2838'), (x0, y0, 0.9), (10.0, 2.2, 1.8), rz=SE.PH + math.radians(0))
        for k, (dx, hh, w) in enumerate(((-2.4, 12.5, 4.0), (1.8, 14.5, 4.3))):
            q = [(dx - w / 2, -0.4, 2.8), (dx + w / 2, -0.4, 2.8), (dx + w * 0.4, -0.4, hh), (dx - w * 0.4, -0.4, hh)]
            ca, sa = math.cos(-SE.PH + math.radians(180)), math.sin(-SE.PH + math.radians(180))
            fs.quad(sail_m, [(x0 + a * ca - b * sa, y0 + a * sa + b * ca, z) for (a, b, z) in q])
        fs.finish(shadow=False)
    elif kind in ('aerial', 'deck', 'rail', 'rocks'):
        generic_gulls(kind)
        H = HEADLANDS[kind]
        if H: headland(LT, H['c'], H['yaw'], H['len'], H['h'], H['d'], seed=H['seed'])
        if kind == 'rocks': rocks(S, P, LT, sea_P)
    elif kind in ('coast', 'shore'):
        coast(S, P, LT, sea_P, marks)
    else:
        raise NotImplementedError(kind)

def kdir_(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

HEADLANDS = dict(
    aerial=dict(c=(380.0, 520.0), yaw=math.radians(-50), len=420.0, h=46.0, d=90.0, seed=5),
    deck=dict(c=(-520.0, -480.0), yaw=math.radians(55), len=360.0, h=34.0, d=80.0, seed=8),
    rail=dict(c=(160.0, 650.0), yaw=math.radians(-80), len=330.0, h=42.0, d=70.0, seed=11),
    rocks=None)

def generic_gulls(kind):
    gb = MB('gulls'); mw = mat('gullw', '#f6f5f0', '#e8ecee', scale=6); mt = mat('gullt', '#2e3038')
    spots = dict(aerial=[((-30, 60, 40), 2.0, 2.4, 0.4), ((20, 30, 55), 0.5, 2.0, -0.3), ((-10, -40, 32), 3.6, 2.2, 0.1)],
                 deck=[((-4, -34, 16), 1.5, 0.9, 0.4), ((7, -48, 22), 5.0, 0.8, -0.2), ((-12, -60, 28), 2.2, 0.8, 0.5)],
                 rail=[((18, 40, 12), 0.8, 0.9, 0.3), ((30, 55, 20), 4.0, 0.8, 0.0), ((14, 62, 26), 2.0, 0.8, 0.5)], rocks=[])
    for (c, yaw, s, fl) in spots.get(kind, []): FX.gull6(gb, mw, mt, c, yaw, s, fl)
    gb.finish(shadow=True)

def clouds_for(kind):
    if kind in ('aerial', 'deck', 'rail', 'rocks', 'coast', 'shore'):
        rr = random.Random({'aerial': 3, 'deck': 5, 'rail': 7, 'rocks': 9, 'coast': 11, 'shore': 12}[kind]); out = []
        for i in range(9):
            a = 2 * math.pi * i / 9 + rr.uniform(-0.15, 0.15); R = rr.uniform(520, 820); z = rr.uniform(50, 210) if kind != 'aerial' else rr.uniform(70, 150)
            out.append(('cl%d' % i, (R * math.cos(a), R * math.sin(a), z), rr.uniform(34, 56), rr.randint(1, 99)))
        return out
    if kind == 'hero':
        return [(nm, SE.v6_pos(c), sz, sd) for (nm, c, sz, sd) in [('cF', (-40, 620, 330), 46, 17), ('cA', (-250, 430, 130), 36, 3), ('cB', (150, 520, 215), 44, 7), ('cC', (-330, 700, 90), 40, 5), ('cD', (380, 560, 70), 30, 11), ('cE', (20, 900, 120), 60, 13)]]
    return []

# ----------------------------------------------------------------------------- rocks (ship_rocks): black jagged rocks near the bow + mist cards
ROCKS = [(13.0, 54.0, 5.0, 7.5, 1), (27.0, 68.0, 4.2, 5.8, 2), (7.0, 80.0, 7.0, 10.5, 3), (-5.0, 62.0, 2.6, 3.4, 4), (21.0, 96.0, 8.0, 12.0, 5), (34.0, 52.0, 2.4, 2.8, 6)]
def rock_obj(mb, m, c, r, h, seed):
    rr = np.random.RandomState(seed)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    for v in bm.verts:
        p = v.co.copy(); n = p.normalized(); k = 1.0 + 0.32 * (rr.rand() - 0.5) + 0.22 * math.sin(3.1 * p.x + 1.7 * p.y + seed) * math.cos(2.3 * p.z)
        top = max(0.0, p.z)
        v.co = Vector((n.x * r * k * (1.0 - 0.35 * top), n.y * r * 0.85 * k * (1.0 - 0.35 * top), (n.z * h * k * (1.05 if n.z > 0 else 0.5)) + h * 0.22))
    me = bpy.data.meshes.new('rock%d' % seed); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = False
    me.materials.append(m); ob = bpy.data.objects.new('rock%d' % seed, me); bpy.context.scene.collection.objects.link(ob); ob.location = (c[0], c[1], -0.4); ob.rotation_euler = (0, 0, seed * 1.3); ob.parent = K.ROOT
    return ob

def mist_card(LT, loc, w, h, k, name):
    m = bpy.data.materials.new('mist_' + name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    def Mth(op, a, b=None, c=None, clamp=False):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
        for i, v in enumerate((a, b, c)):
            if v is None: continue
            if hasattr(v, 'node'): L(v, n.inputs[i])
            else: n.inputs[i].default_value = v
        return n.outputs[0]
    uu = Mth('SUBTRACT', Mth('MULTIPLY', sp.outputs['X'], 2.0), 1.0)
    side = Mth('SUBTRACT', 1.0, Mth('MULTIPLY', uu, uu), clamp=True)
    vv = Mth('POWER', Mth('SUBTRACT', 1.0, sp.outputs['Y'], clamp=True), 1.6)
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.5; L(tc.outputs['Generated'], nz.inputs['Vector'])
    a = Mth('MULTIPLY', Mth('MULTIPLY', side, vv), Mth('MULTIPLY_ADD', nz.outputs['Fac'], 0.9, 0.35))
    L(Mth('MULTIPLY', a, k, clamp=True), mx.inputs[0]); em.inputs['Color'].default_value = hexc(LT['haze']); em.inputs['Strength'].default_value = 1.0
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def rocks(S, P, LT, sea_P):
    mb = MB('rocks'); m = mat('rock', '#25222c', '#3a3644', scale=0.8, rough=0.5, sheen=0.25, contrast=1.2)
    K.ROOT = S['world_root']
    for (x, y, r, h, sd) in ROCKS: rock_obj(mb, m, (x, y), r, h, sd)
    sea_P['rocks'] = [(x, y, r * 0.9, h) for (x, y, r, h, sd) in ROCKS]
    cam = Vector(P['cam']['loc']); look = Vector(P['cam']['look']); d = (look - cam); d.z = 0; d.normalize(); rgt = d.cross(Vector((0, 0, 1)))
    ang = math.atan2(d.y, d.x)
    for i, (dist, hh, k) in enumerate(((38.0, 26.0, 0.30), (70.0, 40.0, 0.38), (120.0, 55.0, 0.42), (220.0, 80.0, 0.5), (400.0, 120.0, 0.6))):
        c = cam + d * dist; w = dist * 1.6
        vs = [c - rgt * w - Vector((0, 0, 6)), c + rgt * w - Vector((0, 0, 6)), c + rgt * w + Vector((0, 0, hh)), c - rgt * w + Vector((0, 0, hh))]
        me = bpy.data.meshes.new('mistc%d' % i); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update()
        uv = me.uv_layers.new(name='UVMap')
        me.materials.append(mist_card(LT, c, w, hh, k * LT.get('fog', 0.0), str(i)))
        ob = bpy.data.objects.new('skyobj_fog%d' % i, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; ob.parent = K.ROOT

# ----------------------------------------------------------------------------- tropical coast (shore east of the ship): terrain, palms, harbour town, fort, boats
def shore_x(y):
    y = np.asarray(y, dtype=np.float64)
    return 215.0 + 20.0 * np.sin(y / 55.0 + 0.7) + 8.0 * np.sin(y / 19.0 + 2.0) + 38.0 * np.exp(-((y + 45.0) / 28.0) ** 2) - 42.0 * np.exp(-((y - 78.0) / 40.0) ** 2) * 0 + 24.0 * np.exp(-((y - 78.0) / 38.0) ** 2)
def shore_sd(px, py): return shore_x(py) - px

def _grad_axis(a, b, c0, c1, h, grow=1.07):
    xs = list(np.arange(c0, c1 + 1e-6, h)); d = h
    while xs[0] > a: d *= grow; xs.insert(0, xs[0] - d)
    d = h
    while xs[-1] < b: d *= grow; xs.append(xs[-1] + d)
    return np.array(xs)

def terrain_h(x, y, kind):
    d = x - shore_x(y)
    rr = fbm2(x / 70.0 + 3.0, y / 70.0 + 9.0, 5, 4); r2 = fbm2(x / 23.0, y / 23.0, 6, 3)
    beach = np.clip(d, -10.0, 70.0) * 0.045 + 0.0
    flat = np.exp(-((y - 80.0) / 60.0) ** 2) * (1 - ss(120.0, 220.0, d))                       # the harbour town sits on a flat shelf
    if kind == 'jamaica':
        h = 135.0 * ss(70.0, 520.0, d) * (0.45 + 0.75 * rr) * (0.7 + 0.5 * np.sin(y / 120.0 + 1.0)) + 9.0 * ss(20.0, 140.0, d) * (0.5 + r2)
        h = h + 26.0 * np.exp(-(((d - 150.0) / 60.0) ** 2 + ((y - 150.0) / 80.0) ** 2))
    else:
        h = 42.0 * ss(90.0, 420.0, d) * (0.5 + 0.7 * rr) + 7.0 * ss(10.0, 120.0, d) * (0.5 + r2)
        h = h + 22.0 * np.exp(-(((d - 110.0) / 55.0) ** 2 + ((y + 70.0) / 55.0) ** 2))         # the garrison hill
        h = h - 0.0
    h = h * (1 - 0.82 * flat) + beach * (d > -10)
    return np.where(d < -10.0, -1.0, h + np.where(d > 0, 0.0, 0.0))

def terrain_mat(LT, kind):
    m = bpy.data.materials.new('terrain'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Object'], sp.inputs[0])
    def mr(val, a, b, lo=0.0, hi=1.0):
        n = N('ShaderNodeMapRange'); n.inputs['From Min'].default_value = a; n.inputs['From Max'].default_value = b; n.inputs['To Min'].default_value = lo; n.inputs['To Max'].default_value = hi; L(val, n.inputs['Value']); return n.outputs['Result']
    def mix(a, b, f):
        n = N('ShaderNodeMix'); n.data_type = 'RGBA'
        for i, v in ((6, a), (7, b)):
            if hasattr(v, 'node'): L(v, n.inputs[i])
            else: n.inputs[i].default_value = v
        (L(f, n.inputs[0]) if hasattr(f, 'node') else n.inputs[0].__setattr__('default_value', f)); return n.outputs[2]
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.05; nz.inputs['Detail'].default_value = 5.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 0.4; nz2.inputs['Detail'].default_value = 3.0; L(tc.outputs['Object'], nz2.inputs['Vector'])
    green_lo = '#6f9a3e' if kind == 'jamaica' else '#9aa848'; green_hi = '#3f7442' if kind == 'jamaica' else '#6f9a46'
    col = mix(hexc(green_lo), hexc(green_hi), mr(nz.outputs['Fac'], 0.42, 0.6))
    col = mix(col, hexc('#bda648' if kind == 'barbados' else '#4c7c40'), mr(nz2.outputs['Fac'], 0.5, 0.65, 0.0, 0.5))
    col = mix(col, hexc('#2f6a4a'), mr(sp.outputs['Z'], 40.0, 130.0, 0.0, 0.55))
    col = mix(hexc('#c89c58'), col, mr(sp.outputs['Z'], 0.9, 2.4))                    # pale sand beach
    col = mix(col, hexc('#000000'), 0.52)
    cd = N('ShaderNodeCameraData'); dmv = mr(cd.outputs['View Distance'], 200.0 * SC, 1000.0 * SC, 0.0, 0.34)
    col = mix(col, hexc('#8fb4b8' if LT.get('fog', 0) < 0.1 else LT['haze']), dmv)
    L(col, bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); return m

def palm(mb, M, base, h, lean, seed):
    rr = random.Random(seed); ang = rr.uniform(0, 6.28); n = 7
    pts = []
    for i in range(n + 1):
        t = i / n; pts.append(Vector((base[0] + lean * math.cos(ang) * t * t * h * 0.35, base[1] + lean * math.sin(ang) * t * t * h * 0.35, base[2] + h * t)))
    for i in range(n): mb.rod(M['trunk'], pts[i], pts[i + 1], 0.20 * (1 - 0.4 * i / n), 0.20 * (1 - 0.4 * (i + 1) / n), 6)
    top = pts[-1]
    for f in range(9):
        a = f * 2 * math.pi / 9 + rr.uniform(-0.2, 0.2); L_ = rr.uniform(3.4, 4.6); drop = rr.uniform(0.55, 1.0)
        prev = top; 
        for sgm in range(5):
            t = (sgm + 1) / 5.0
            nxt = Vector((top.x + math.cos(a) * L_ * t, top.y + math.sin(a) * L_ * t, top.z + L_ * (0.45 * math.sin(math.pi * t * 0.62) - drop * 0.55 * t * t)))
            w0 = 0.55 * (1 - (sgm / 5.0)) + 0.1; w1 = 0.55 * (1 - t) + 0.05
            pa = Vector((-math.sin(a), math.cos(a), 0))
            q = [prev + pa * w0, prev - pa * w0, nxt - pa * w1, nxt + pa * w1]
            mb.quad(M['frond'] if f % 2 else M['frond2'], q); mb.quad(M['frond'] if f % 2 else M['frond2'], q[::-1]); prev = nxt

def house(mb, M, c, w, d, h, yaw, wallm, roofm):
    ca, sa = math.cos(yaw), math.sin(yaw)
    def P(x, y, z): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + z)
    mb.box(wallm, (c[0], c[1], c[2] + h / 2), (w, d, h), rz=yaw)
    rh = h * 0.55; v = [P(-w / 2 - 0.3, -d / 2 - 0.3, h), P(w / 2 + 0.3, -d / 2 - 0.3, h), P(w / 2 + 0.3, 0, h + rh), P(-w / 2 - 0.3, 0, h + rh)]
    v2 = [P(-w / 2 - 0.3, d / 2 + 0.3, h), P(w / 2 + 0.3, d / 2 + 0.3, h), P(w / 2 + 0.3, 0, h + rh), P(-w / 2 - 0.3, 0, h + rh)]
    mb.quad(roofm, v); mb.quad(roofm, v[::-1]); mb.quad(roofm, v2[::-1]); mb.quad(roofm, v2)
    mb.box(M['dark'], P(0, -d / 2 - 0.02, 1.0), (0.9, 0.06, 1.9), rz=yaw) if True else None

def boat(mb, M, c, l, yaw, sail=True, seed=0):
    ca, sa = math.cos(yaw), math.sin(yaw)
    mb.ell(M['boat'], (c[0], c[1], c[2] + 0.1), (l / 2, l * 0.18, l * 0.12), (14, 8), rot=(0, 0, yaw)); mb.ell(M['boatw'], (c[0], c[1], c[2] + 0.22), (l * 0.46, l * 0.15, l * 0.05), (14, 6), rot=(0, 0, yaw))
    if sail:
        mp = (c[0], c[1], c[2] + 0.3); mb.rod(M['trunk'], mp, (mp[0], mp[1], mp[2] + l * 0.9), 0.07, 0.04, 6)
        for sg in (1, -1):
            q = [(mp[0], mp[1], mp[2] + 0.5), (mp[0] - l * 0.38 * ca * 1.0 + 0.0, mp[1] - l * 0.38 * sa, mp[2] + 0.7), (mp[0] - l * 0.12 * ca, mp[1] - l * 0.12 * sa, mp[2] + l * 0.85), (mp[0], mp[1], mp[2] + l * 0.9)]
            mb.quad(M['bsail'], q if sg > 0 else q[::-1])

def fort(mb, M, c, kind):
    wall = M['brick'] if kind == 'jamaica' else M['lime']
    W_, D_, H_ = (26.0, 15.0, 5.2) if kind == 'jamaica' else (20.0, 13.0, 6.4)
    mb.box(wall, (c[0], c[1], c[2] + H_ / 2), (W_, D_, H_))
    mb.box(M['dark'], (c[0], c[1] - D_ / 2 - 0.02, c[2] + 1.3), (2.2, 0.08, 2.6))
    for sx in (-1, 1):
        for sy in (-1, 1):
            mb.box(wall, (c[0] + sx * W_ / 2, c[1] + sy * D_ / 2, c[2] + H_ / 2 + 0.6), (4.2, 4.2, H_ + 1.2))
            mb.box(M['dark'], (c[0] + sx * W_ / 2, c[1] + sy * D_ / 2, c[2] + H_ + 1.25), (4.4, 4.4, 0.3))
    n = int(W_ / 1.4)
    for i in range(n): mb.box(wall, (c[0] - W_ / 2 + 0.7 + 1.4 * i, c[1] - D_ / 2, c[2] + H_ + 0.35), (0.8, 0.6, 0.7))
    if kind == 'barbados':
        mb.cyl(M['lime'], (c[0] + 4.0, c[1] + 1.0, c[2] + H_ + 4.5), 3.2, 9.0, seg=14); mb.cone(M['roofr'], (c[0] + 4.0, c[1] + 1.0, c[2] + H_ + 9.0), 3.6, 0.2, 3.4, 14)
    pole = (c[0] - W_ / 2 + 1.5, c[1] + D_ / 2 - 1.5, c[2] + H_)
    mb.rod(M['trunk'], pole, (pole[0], pole[1], pole[2] + 11.0), 0.12, 0.07, 6)
    fl = [(pole[0], pole[1], pole[2] + 10.8), (pole[0] + 3.4, pole[1] + 0.6, pole[2] + 10.2), (pole[0] + 3.4, pole[1] + 0.6, pole[2] + 8.6), (pole[0], pole[1], pole[2] + 8.8)]
    mb.quad(M['flag'], fl); mb.quad(M['flag'], fl[::-1])
    for i in range(5): mb.rod(M['iron'], (c[0] - 9 + 4.5 * i, c[1] - D_ / 2 - 0.2, c[2] + H_ + 0.55), (c[0] - 9 + 4.5 * i, c[1] - D_ / 2 - 1.8, c[2] + H_ + 0.6), 0.2, 0.17, 7)

def windmill(mb, M, c, h=11.0):
    mb.rod(M['lime'], (c[0], c[1], c[2]), (c[0], c[1], c[2] + h), 2.6, 1.6, 12); mb.cone(M['roofr'], (c[0], c[1], c[2] + h), 1.9, 0.1, 2.4, 12)
    hub = (c[0], c[1] - 1.6, c[2] + h * 0.88)
    for k in range(4):
        a = k * math.pi / 2 + 0.4; mb.rod(M['trunk'], hub, (hub[0] + 8.0 * math.cos(a), hub[1] - 0.2, hub[2] + 8.0 * math.sin(a)), 0.12, 0.09, 4)
        pa = (-math.sin(a), 0, math.cos(a))
        q = [(hub[0] + 2.0 * math.cos(a) - pa[0] * 0.1, hub[1] - 0.2, hub[2] + 2.0 * math.sin(a) - pa[2] * 0.1), (hub[0] + 8.0 * math.cos(a), hub[1] - 0.2, hub[2] + 8.0 * math.sin(a)), (hub[0] + 8.0 * math.cos(a) + pa[0] * 1.9, hub[1] - 0.2, hub[2] + 8.0 * math.sin(a) + pa[2] * 1.9), (hub[0] + 2.0 * math.cos(a) + pa[0] * 1.9, hub[1] - 0.2, hub[2] + 2.0 * math.sin(a) + pa[2] * 1.9)]
        mb.quad(M['bsail'], q); mb.quad(M['bsail'], q[::-1])

def coast(S, P, LT, sea_P, marks):
    kind = S['coast']; K.ROOT = S['world_root']
    sea_P['shore'] = shore_sd; sea_P['shal_w'] = 55.0; sea_P['shal_k'] = 0.95; sea_P['sea_shal'] = '#3ab6a8'
    M = dict(trunk=mat('trunk', '#8a6a48', '#6f5438', scale=6, aniso=(0.3, 0.3, 1.0)), frond=mat('frond', '#4f8a3a', '#3e7a36', scale=3, rough=0.9), frond2=mat('frond2', '#5e9a42', '#4a8a3c', scale=3),
             dark=mat('dkdoor', '#3a2a24'), boat=mat('boat', '#7a4a30', '#8a5a3a', scale=3), boatw=mat('boatw', '#e8dcc0', '#d8ccb0', scale=3), bsail=mat('bsail', '#e8dcc0', '#dccfae', scale=2.5, emit='#ffe2a8', emit_k=0.1),
             brick=mat('brick', '#b4623e', '#a4543a', scale=1.2), lime=mat('lime', '#e8e0cc', '#dcd4bc', scale=1.0), roofr=mat('roofr', '#b05a3a', '#9c4c32', scale=2.0), iron=mat('iron2', '#2a2622', '#38322c', scale=6),
             flag=mat_emit('flagr', '#c8403a', 0.7), wall1=mat('wall1', '#f0e2c0', '#e6d6b0', scale=1.5), wall2=mat('wall2', '#e8c88a', '#dcb878', scale=1.5), wall3=mat('wall3', '#d89a78', '#cc8c6c', scale=1.5),
             quay=mat('quay', '#b8aa90', '#a89c84', scale=1.5), cane=mat('cane', '#a8b84a', '#92a840', scale=0.6))
    # ---- terrain
    xs = _grad_axis(100.0, 1000.0, 190.0, 330.0, 2.2, 1.09); ys = _grad_axis(-520.0, 720.0, -220.0, 340.0, 2.6, 1.09)
    X, Y = np.meshgrid(xs, ys); Z = terrain_h(X, Y, kind)
    nx, ny = len(xs), len(ys)
    verts = np.stack([X, Y, Z], -1).reshape(-1, 3)
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i) for j in range(ny - 1) for i in range(nx - 1)]
    tm = terrain_mat(LT, kind)
    ob = _mesh_obj('terrain', verts, faces, [tm], None, True); ob.visible_shadow = True; ob.parent = K.ROOT
    def gz(x, y): return float(terrain_h(np.array([x]), np.array([y]), kind)[0])
    rr = random.Random(17)
    # ---- palms along the beach and in groves
    mbp = MB('palms')
    for i in range(110):
        y = rr.uniform(-210.0, 330.0); d = rr.uniform(3.0, 46.0) if i < 70 else rr.uniform(20.0, 120.0)
        if 25.0 < y < 125.0 and d < 24.0: continue                                    # keep the quay open
        x = float(shore_x(y)) + d; palm(mbp, M, (x, y, gz(x, y) - 0.2), rr.uniform(6.5, 10.5), rr.uniform(0.3, 1.0), i + 5)
    mbp.finish(shadow=True)
    # ---- harbour town on the flat shelf
    mbh = MB('town')
    for i in range(26):
        y = rr.uniform(25.0, 135.0); x = float(shore_x(y)) + rr.uniform(26.0, 110.0)
        if any(abs(y - py_) < 9 and abs(x - px_) < 10 for (px_, py_) in S.setdefault('_h', [])): continue
        S['_h'].append((x, y))
        house(mbh, M, (x, y, gz(x, y) - 0.3), rr.uniform(6.0, 10.0), rr.uniform(5.0, 7.5), rr.uniform(3.4, 5.2), rr.choice([0.0, 0.0, math.pi / 2, 0.2, -0.2]), M[rr.choice(['wall1', 'wall2', 'wall3', 'wall1'])], M['roofr'])
    # wharf / quay + jetty
    ym0, ym1 = 52.0, 100.0; xq = float(shore_x(76.0))
    mbh.box(M['quay'], (xq - 3.0, 76.0, 0.55), (7.0, ym1 - ym0, 1.9)); mbh.box(M['quay'], (xq - 16.0, 66.0, 0.45), (28.0, 3.4, 1.4))
    for k in range(5): mbh.box(M['trunk'], (xq - 28.0 + 6.5 * k, 64.0, 0.9), (0.35, 0.35, 2.0)); mbh.box(M['trunk'], (xq - 28.0 + 6.5 * k, 68.0, 0.9), (0.35, 0.35, 2.0))
    for (y, w_) in ((60.0, 8.0), (80.0, 9.0), (92.0, 7.0)): house(mbh, M, (xq + 8.0, y, 0.8), w_, 6.5, 4.2, math.pi / 2, M['wall1'], M['roofr'])
    # crates / barrels on the quay
    for k in range(10):
        yy = rr.uniform(56.0, 96.0); mbh.box(M['trunk'], (xq - 2.0 + rr.uniform(-1.5, 1.5), yy, 1.9), (rr.uniform(0.7, 1.3),) * 2 + (rr.uniform(0.7, 1.2),), rz=rr.uniform(0, 3))
    # boats in the harbour
    for i in range(9):
        y = rr.uniform(20.0, 125.0); x = float(shore_x(y)) - rr.uniform(14.0, 90.0)
        if abs(x) < 26 and abs(y) < 40: continue
        boat(mbh, M, (x, y, 0.0), rr.uniform(6.0, 11.0), rr.uniform(0, 6.28), sail=(i % 3 != 2), seed=i)
    mbh.finish(shadow=True)
    # ---- fort + dressing
    mbf = MB('fort')
    if kind == 'jamaica':
        fx, fy = float(shore_x(-45.0)) - 10.0, -45.0
        fort(mbf, M, (fx, fy, 0.9), 'jamaica')
        for i in range(6): house(mbf, M, (fx + 40 + rr.uniform(0, 40), fy + 25 + rr.uniform(-20, 50), 3.0 + gz(fx + 50, fy + 30)), 7, 5.5, 4.2, rr.uniform(-.3, .3), M['wall2'], M['roofr'])
    else:
        hx, hy = float(shore_x(-70.0)) + 110.0, -70.0
        fort(mbf, M, (hx, hy, gz(hx, hy) - 0.5), 'barbados')
        windmill(mbf, M, (float(shore_x(190.0)) + 120.0, 190.0, gz(float(shore_x(190.0)) + 120.0, 190.0) - 0.4)); windmill(mbf, M, (float(shore_x(-150.0)) + 150.0, -150.0, gz(float(shore_x(-150.0)) + 150.0, -150.0) - 0.4), 9.0)
        for i in range(9):                                                                     # sugar-cane patches
            cx = float(shore_x(40.0 * i - 120.0)) + rr.uniform(60, 190); cy = 40.0 * i - 120.0
            mbf.box(M['cane'], (cx, cy, gz(cx, cy) + 0.9), (rr.uniform(14, 24), rr.uniform(14, 24), 1.8))
    mbf.finish(shadow=True)
    # ---- marks on the shore (metres, ship frame; z = ground)
    ya, yb = (rr.uniform(0, 0) + 40.0), 44.0
    S['shore_marks'] = dict(shore_a=(float(shore_x(ya)) + 4.0, ya, gz(float(shore_x(ya)) + 4.0, ya)), shore_b=(float(shore_x(yb)) + 6.0, yb + 2.0, gz(float(shore_x(yb)) + 6.0, yb + 2.0)))
    S['extra_cams'] = {}
    if S['preset'] == 'ship_shore':
        mbd = MB('shoredress'); cx = float(shore_x(40.0)) + 10.5
        for (dx, dy, hh, sd) in ((3.2, 39.0, 8.5, 91), (4.5, 27.5, 7.0, 92), (-2.5, 47.0, 7.5, 93), (14.0, 40.0, 9.0, 94)):
            x = cx - 10.5 + dx + 10.0; y = dy; palm(mbd, M, (x, y, gz(x, y) - 0.2), hh, 0.8, sd)
        boat(mbd, M, (cx - 9.0, 24.8, gz(cx - 9.0, 24.8) + 0.2), 4.6, 0.25, sail=False)
        for k in range(5): mbd.box(M['trunk'], (cx - 7.8 + 0.5 * (k % 2), 42.5 + 0.7 * k, gz(cx - 7.8, 42.5) + 0.45), (0.8, 0.8, 0.8), rz=0.3 * k)
        mbd.finish(shadow=True)

def _rain_build(S, cam):
    rr = np.random.RandomState(7); inv = cam.matrix_world.inverted().to_3x3(); dl = (inv @ Vector((0, 0, -1))).normalized()
    verts = []; faces = []
    layers = ((1.6, 5.0, 110, 0.5), (5.0, 16.0, 420, 0.5), (16.0, 60.0, 900, 0.5))
    for (d0, d1, n, a) in layers:
        for i in range(n):
            d = rr.uniform(d0, d1); hx = math.tan(math.radians(26.0)) * d * 1.12; hy = math.tan(math.radians(40.0)) * d * 1.1
            p = Vector((rr.uniform(-hx, hx), rr.uniform(-hy, hy), -d)); ln = d * 0.05 * rr.uniform(0.7, 1.3); w = max(d * 0.0016, 0.004) * rr.uniform(0.8, 1.3)
            side = dl.cross(Vector((0, 0, -1))).normalized() * w
            q = [p - side, p + side, p + side + dl * ln, p - side + dl * ln]; b = len(verts); verts += [tuple(v) for v in q]; faces.append((b, b + 1, b + 2, b + 3))
    me = bpy.data.meshes.new('rain'); me.from_pydata(verts, [], faces); me.update()
    m = bpy.data.materials.new('rainm'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    em.inputs['Color'].default_value = hexc('#d4dcff'); em.inputs['Strength'].default_value = 1.0; mx.inputs[0].default_value = 0.34
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface']); me.materials.append(m)
    ob = bpy.data.objects.new('rain_streaks', me); bpy.context.scene.collection.objects.link(ob); ob.parent = cam; ob.visible_shadow = False; ob.visible_glossy = False
    ob['dl'] = tuple(dl); return ob

def rain(S, on, frame=None):
    """rain: three depth layers of streak geometry parented to the scene camera (call after make_camera); on = bool or 0..1; per frame with frame= it keys the fall"""
    cam = bpy.context.scene.camera
    if cam is None: return
    ro = S.get('rain')
    if ro is None or ro.parent is not cam:
        if ro is not None: bpy.data.objects.remove(ro)
        ro = _rain_build(S, cam); S['rain'] = ro
    vis = bool(on) and float(on) > 0.0
    K._setv(ro, vis, frame)
    if frame is not None:
        dl = Vector(ro['dl']); ph = (frame * 0.37) % 1.0
        ro.location = dl * (ph * 3.0)
        K._key(ro, 'location', frame, 'LINEAR')
    else:
        ro.location = (0, 0, 0)
