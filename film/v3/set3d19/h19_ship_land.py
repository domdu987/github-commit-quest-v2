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
        floating_spar(S, P, sea_P)
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

def floating_spar(S, P, sea_P):
    """foreground of the hero: a floating spar (a broken yard with a rope end) and a long swell crest with a thin broken foam line, 8-14 m from the lens"""
    c = np.array(P['cam']['loc'][:2], dtype=np.float64); lk = np.array(P['cam']['look'][:2], dtype=np.float64); f = lk - c; f /= np.linalg.norm(f); r = np.array([f[1], -f[0]])
    A = c + f * 7.6 + r * (-3.0); B = c + f * 10.6 + r * (0.8)
    cr0 = c + f * 13.5 + r * (-5.5); cr1 = c + f * 12.0 + r * (6.5)
    sea_P['streaks'] = [((A[0], A[1]), (B[0], B[1]), 0.75, 0.95), ((cr0[0], cr0[1]), (cr1[0], cr1[1]), 0.5, 0.8)]
    mb = MB('spar'); wood = mat('spar', '#5e4630', '#76583a', scale=3, aniso=(0.2, 0.2, 1.0)); rope = mat('sparrope', '#b8924c', '#9a7638', scale=6); iron = mat('sparband', '#2a2622', '#38322c', scale=6)
    za = float(SE.swell_h(A[0], A[1])) + 0.04; zb = float(SE.swell_h(B[0], B[1])) + 0.04
    mb.rod(wood, (A[0], A[1], za + 0.05), (B[0], B[1], zb + 0.05), 0.24, 0.19, 12, True, True)
    d = (B - A) / np.linalg.norm(B - A)
    for tt in (0.12, 0.5, 0.86):                                      # iron bands + a short broken stub and a rope end
        q = A + (B - A) * tt; zq = za + (zb - za) * tt + 0.05
        mb.rod(iron, (q[0] - d[0] * 0.05, q[1] - d[1] * 0.05, zq), (q[0] + d[0] * 0.05, q[1] + d[1] * 0.05, zq), 0.27, 0.27, 12)
    q = A + (B - A) * 0.55; mb.rod(wood, (q[0], q[1], za + 0.1 + 0.55 * (zb - za)), (q[0] - d[1] * 0.9, q[1] + d[0] * 0.9, za + 0.2 + 0.55 * (zb - za)), 0.07, 0.06, 8)
    q = A + (B - A) * 0.3
    for k in range(4): mb.ell(rope, (q[0] + 0.25 * math.cos(k * 1.7), q[1] + 0.25 * math.sin(k * 1.7), za + 0.05 + 0.3 * (zb - za)), (0.16, 0.05, 0.05), (8, 5), rot=(0, 0, k * 1.7))
    K.ROOT = S['world_root']; mb.finish(shadow=True)

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
    if kind == 'rocks': return []
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
ROCKS = [(13.0, 54.0, 5.0, 7.5, 1), (27.0, 68.0, 4.2, 5.8, 2), (7.0, 80.0, 7.0, 10.5, 3), (-5.0, 62.0, 2.6, 3.4, 4), (21.0, 96.0, 8.0, 12.0, 5), (34.0, 52.0, 2.4, 2.8, 6),
         (4.0, 44.0, 2.2, 2.4, 7), (-12.0, 74.0, 3.4, 4.6, 8)]
def rock_obj(mb, m, c, r, h, seed):
    """rounded black basalt boulder: smooth icosphere, low-frequency lumps, flattened shoulder, submerged base"""
    rr = np.random.RandomState(seed); ph = rr.uniform(0, 6.28, 6)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    for v in bm.verts:
        n = v.co.normalized()
        k = 1.0 + 0.15 * math.sin(2.1 * n.x + ph[0]) * math.cos(1.7 * n.y + ph[1]) + 0.11 * math.sin(3.3 * n.z + ph[2] + 2.0 * n.x) + 0.04 * math.sin(7.0 * n.x + 5.0 * n.y + ph[3])
        top = max(0.0, n.z); sq = 1.0 - 0.18 * top * top
        z = n.z * h * k * (1.0 if n.z > 0 else 0.5) * (1.0 - 0.12 * max(0.0, n.z - 0.75))
        v.co = Vector((n.x * r * k * sq, n.y * r * 0.88 * k * sq, z + h * 0.18))
    me = bpy.data.meshes.new('rock%d' % seed); bm.to_mesh(me); bm.free()
    for p in me.polygons: p.use_smooth = True
    me.materials.append(m); ob = bpy.data.objects.new('rock%d' % seed, me); bpy.context.scene.collection.objects.link(ob); ob.location = (c[0], c[1], -0.5); ob.rotation_euler = (0, 0, seed * 1.3); ob.parent = K.ROOT
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
    a = Mth('MULTIPLY', Mth('MULTIPLY', side, vv), Mth('MULTIPLY_ADD', nz.outputs['Fac'], 1.7, -0.15, clamp=True))
    L(Mth('MULTIPLY', a, k, clamp=True), mx.inputs[0]); em.inputs['Color'].default_value = hexc(LT['haze']); em.inputs['Strength'].default_value = 1.0
    L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    return m

def storm_deck(LT, name='stormdeck', z=240.0, size=6000.0, dark='#4a5666', light='#98a4b4', scale=0.0035, k=1.0):
    """a low layered storm-cloud ceiling: a huge plane seen from below, emission of stretched fbm noise (dark slate belly, lighter torn edges), faded into the haze at the horizon"""
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (scale, scale * 1.9, scale); L(tc.outputs['Object'], mp.inputs['Vector'])
    n1 = N('ShaderNodeTexNoise'); n1.inputs['Scale'].default_value = 1.0; n1.inputs['Detail'].default_value = 6.0; n1.inputs['Roughness'].default_value = 0.62; L(mp.outputs[0], n1.inputs['Vector'])
    mp2 = N('ShaderNodeMapping'); mp2.inputs['Scale'].default_value = (4.0, 4.0, 4.0); mp2.inputs['Location'].default_value = (5.0, 3.0, 1.0); L(mp.outputs[0], mp2.inputs['Vector'])
    n2 = N('ShaderNodeTexNoise'); n2.inputs['Scale'].default_value = 1.0; n2.inputs['Detail'].default_value = 3.0; L(mp2.outputs[0], n2.inputs['Vector'])
    def mr(v, a, b, lo=0.0, hi=1.0):
        n = N('ShaderNodeMapRange'); n.inputs['From Min'].default_value = a; n.inputs['From Max'].default_value = b; n.inputs['To Min'].default_value = lo; n.inputs['To Max'].default_value = hi; L(v, n.inputs['Value']); return n.outputs['Result']
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = hexc(dark); cr.color_ramp.elements[1].position = 1.0; cr.color_ramp.elements[1].color = hexc(light)
    mid = cr.color_ramp.elements.new(0.45); mid.color = hexc('#6a7686')
    nn = N('ShaderNodeMath'); nn.operation = 'MULTIPLY_ADD'; nn.inputs[1].default_value = 0.35; L(n2.outputs['Fac'], nn.inputs[0]); L(n1.outputs['Fac'], nn.inputs[2])
    L(mr(nn.outputs[0], 0.35, 0.78), cr.inputs['Fac'])
    cd = N('ShaderNodeCameraData'); hz = mr(cd.outputs['View Distance'], 700.0 * SC, 3200.0 * SC, 0.0, 0.88)
    mxc = N('ShaderNodeMix'); mxc.data_type = 'RGBA'; L(cr.outputs[0], mxc.inputs[6]); mxc.inputs[7].default_value = hexc(LT['haze']); L(hz, mxc.inputs[0])
    em.inputs['Strength'].default_value = k; L(mxc.outputs[2], em.inputs['Color'])
    L(mr(n1.outputs['Fac'], 0.12, 0.34), mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    # a second, higher and darker layer under the first one is not needed: the near plane is opaque where the noise is above 0.34 and torn elsewhere
    verts = [(-size, -size, z), (size, -size, z), (size, size, z), (-size, size, z)]
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], [(0, 1, 2, 3)]); me.update(); me.materials.append(m)
    ob = bpy.data.objects.new('skyobj_' + name, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; ob.visible_glossy = True; ob.visible_diffuse = False; ob.parent = K.ROOT      # diffuse rays pass through to the blue world ambient (the deck keeps its blue-violet shade)
    return ob

def rocks(S, P, LT, sea_P):
    mb = MB('rocks'); m = mat('rock', '#18181c', '#26262c', scale=0.7, rough=0.26, sheen=0.7, contrast=1.1)
    K.ROOT = S['world_root']
    for (x, y, r, h, sd) in ROCKS: rock_obj(mb, m, (x, y), r, h, sd)
    sea_P['rocks'] = [(x, y, r * 1.05, h) for (x, y, r, h, sd) in ROCKS]
    cam = Vector(P['cam']['loc']); look = Vector(P['cam']['look']); d = (look - cam); d.z = 0; d.normalize(); rgt = d.cross(Vector((0, 0, 1)))
    # storm deck (low) + a torn higher deck; two fog layers: a bank on the water round the rocks and a far one that eats the horizon
    storm_deck(LT, 'stormdeck_lo', z=180.0, dark=LT['cloud'][1], light=LT['cloud'][0], scale=0.0042, k=1.0)
    fk = max(LT.get('fog', 0.0), 0.7)
    for i, (dist, hh, k) in enumerate(((46.0, 15.0, 0.55), (150.0, 55.0, 0.62))):
        c = cam + d * dist; w = dist * 1.7
        vs = [c - rgt * w - Vector((0, 0, 6)), c + rgt * w - Vector((0, 0, 6)), c + rgt * w + Vector((0, 0, hh)), c - rgt * w + Vector((0, 0, hh))]
        me = bpy.data.meshes.new('mistc%d' % i); me.from_pydata([tuple(v) for v in vs], [], [(0, 1, 2, 3)]); me.update()
        uv = me.uv_layers.new(name='UVMap')
        me.materials.append(mist_card(LT, c, w, hh, k * fk, str(i)))
        ob = bpy.data.objects.new('skyobj_fog%d' % i, me); bpy.context.scene.collection.objects.link(ob); ob.visible_shadow = False; ob.visible_diffuse = False; ob.parent = K.ROOT

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
        # jungle ridges on both points of the bay (exactly zero round the beach marks, y 0-70 m): irregular, lumpy crests
        rough = 0.75 + 0.5 * fbm2(x / 18.0 + 11.0, y / 18.0 + 4.0, 9, 4)
        h = h + 34.0 * rough * np.exp(-(((d - 60.0) / 45.0) ** 2 + ((y - 215.0) / 55.0) ** 2)) * ss(95.0, 140.0, y)
        h = h + 22.0 * rough * np.exp(-(((d - 75.0) / 40.0) ** 2 + ((y + 105.0) / 45.0) ** 2)) * ss(-35.0, -65.0, y)
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
    jam = kind == 'jamaica'
    green_lo = '#5a9a2e' if jam else '#9aa848'; green_hi = '#2f7a38' if jam else '#6f9a46'
    col = mix(hexc(green_lo), hexc(green_hi), mr(nz.outputs['Fac'], 0.42, 0.6))
    col = mix(col, hexc('#bda648' if kind == 'barbados' else '#7aa832'), mr(nz2.outputs['Fac'], 0.5, 0.65, 0.0, 0.5))
    if jam:                                                                                            # bare red-earth / rock patches and dark scrub mottling
        nz3 = N('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 0.11; nz3.inputs['Detail'].default_value = 6.0; nz3.inputs['Roughness'].default_value = 0.7; L(tc.outputs['Object'], nz3.inputs['Vector'])
        col = mix(col, hexc('#a0603a'), mr(nz3.outputs['Fac'], 0.6, 0.68, 0.0, 0.85))
        vo = N('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 0.6; L(tc.outputs['Object'], vo.inputs['Vector'])
        col = mix(col, hexc('#1f5a2a'), mr(vo.outputs['Distance'], 0.35, 0.15, 0.0, 0.6))
    col = mix(col, hexc('#2f6a4a'), mr(sp.outputs['Z'], 40.0, 130.0, 0.0, 0.55))
    col = mix(col, hexc('#000000'), 0.30 if jam else 0.52)
    sn1 = N('ShaderNodeTexNoise'); sn1.inputs['Scale'].default_value = 0.9; sn1.inputs['Detail'].default_value = 4.0; L(tc.outputs['Object'], sn1.inputs['Vector'])
    sn2 = N('ShaderNodeTexNoise'); sn2.inputs['Scale'].default_value = 6.0; sn2.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], sn2.inputs['Vector'])
    sand_c = ('#d6a040', '#c28c36', '#b07c32', '#946630') if jam else ('#d8a848', '#c69238', '#b4823a', '#946630')       # deep gold sand (Barbados a touch paler, 2026-11-20 §G)
    dry = mix(hexc(sand_c[0]), hexc(sand_c[1]), mr(sn1.outputs['Fac'], 0.4, 0.62))                  # dry sand, two tones
    dry = mix(dry, hexc(sand_c[2]), mr(sn2.outputs['Fac'], 0.52, 0.7, 0.0, 0.5))                       # fine grain
    if True:                                                                                           # wind ripples (both coasts)
        rw = N('ShaderNodeTexWave'); rw.wave_type = 'BANDS'; rw.bands_direction = 'X'; rw.inputs['Scale'].default_value = 2 * math.pi / (20.0 * 0.22); rw.inputs['Distortion'].default_value = 3.0; rw.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], rw.inputs['Vector'])
        dry = mix(dry, hexc('#a87430'), mr(rw.outputs['Fac'], 0.75, 1.0, 0.0, 0.3))
    sand = mix(hexc(sand_c[3]), dry, mr(sp.outputs['Z'], 0.02, 0.14))                                  # wet sand darkens towards the waterline
    col = mix(sand, col, mr(sp.outputs['Z'], 0.9, 2.4))                                                # pale sand beach
    cd = N('ShaderNodeCameraData'); dmv = mr(cd.outputs['View Distance'], 200.0 * SC, 1000.0 * SC, 0.0, 0.34)
    col = mix(col, hexc('#8fb4b8' if LT.get('fog', 0) < 0.1 else LT['haze']), dmv)
    L(col, bs.inputs['Base Color']); L(bs.outputs[0], out.inputs['Surface']); return m

def leaf_mat(name, A, B, scale=3.0, glow='#2e6a1e', glow_k=0.10, trans='#9ad048', tk=0.35):
    """palm / bush leaves: two-tone painterly diffuse mixed with a translucent layer (the sun shines through a frond, so its underside
    reads yellow-green instead of a black hole) and a faint dark-green self-light for the parts no light reaches"""
    if name in K.MATS: return K.MATS[name]
    m = mat(name + '_base', A, B, scale=scale, rough=0.85, emit=glow, emit_k=glow_k); m = m.copy(); m.name = name; nt = m.node_tree
    N = nt.nodes.new; L = nt.links.new; out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'][0]; bs = nt.nodes['bsdf']
    tr = N('ShaderNodeBsdfTranslucent'); tr.inputs['Color'].default_value = hexc(trans)
    mx = N('ShaderNodeMixShader'); mx.inputs[0].default_value = tk; L(bs.outputs[0], mx.inputs[1]); L(tr.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    K.MATS[name] = m; return m

def trunk_mat(name='trunk'):
    """palm trunk: grey-brown with darker leaf-scar rings along the trunk"""
    if name in K.MATS: return K.MATS[name]
    m = mat(name + '_base', '#9a7a56', '#7a5e40', scale=6, aniso=(0.3, 0.3, 1.0)).copy(); m.name = name; nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    bs = nt.nodes['bsdf']; src = bs.inputs['Base Color'].links[0].from_socket
    tc = N('ShaderNodeTexCoord'); wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.inputs['Scale'].default_value = 2 * math.pi / (20.0 * 0.28); wv.inputs['Distortion'].default_value = 0.4; L(tc.outputs['Object'], wv.inputs['Vector'])
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.15; cr.color_ramp.elements[0].color = hexc('#4a3626'); cr.color_ramp.elements[1].position = 0.45; cr.color_ramp.elements[1].color = (1, 1, 1, 1); L(wv.outputs['Fac'], cr.inputs['Fac'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0; L(src, mx.inputs[6]); L(cr.outputs[0], mx.inputs[7]); L(mx.outputs[2], bs.inputs['Base Color'])
    K.MATS[name] = m; return m

def palm(mb, M, base, h, lean, seed, ang=None, nf=10):
    """coconut palm: ringed tapering trunk, a crown boss with coconuts, nf feathered fronds (a rib + drooping leaflets on both sides)"""
    rr = random.Random(seed); ang = rr.uniform(0, 6.28) if ang is None else ang; n = 7
    pts = []
    for i in range(n + 1):
        t = i / n; pts.append(Vector((base[0] + lean * math.cos(ang) * t * t * h * 0.35, base[1] + lean * math.sin(ang) * t * t * h * 0.35, base[2] + h * t)))
    for i in range(n): mb.rod(M['trunk'], pts[i], pts[i + 1], 0.22 * (1 - 0.4 * i / n), 0.22 * (1 - 0.4 * (i + 1) / n), 7)
    top = pts[-1]
    mb.ell(M['frond2'], (top.x, top.y, top.z + 0.05), (0.35, 0.35, 0.45), (8, 6))
    for k in range(4):
        a = k * 1.7 + rr.uniform(0, 1); mb.ell(M['nut'], (top.x + 0.28 * math.cos(a), top.y + 0.28 * math.sin(a), top.z - 0.25), (0.16, 0.16, 0.18), (6, 4))
    for f in range(nf):
        a = f * 2 * math.pi / nf + rr.uniform(-0.25, 0.25); L_ = rr.uniform(3.4, 4.8); drop = rr.uniform(0.5, 1.05); fm = M['frond'] if f % 2 else M['frond2']
        prev = top.copy(); pa = Vector((-math.sin(a), math.cos(a), 0)); ns = 6
        rib = [top.copy()]
        for sgm in range(ns):
            t = (sgm + 1) / ns
            rib.append(Vector((top.x + math.cos(a) * L_ * t, top.y + math.sin(a) * L_ * t, top.z + L_ * (0.42 * math.sin(math.pi * t * 0.62) - drop * 0.55 * t * t))))
        for sgm in range(ns):
            p0, p1 = rib[sgm], rib[sgm + 1]; t0 = sgm / ns; t1 = (sgm + 1) / ns
            rq = [p0 + pa * 0.05, p0 - pa * 0.05, p1 - pa * 0.04, p1 + pa * 0.04]; mb.quad(fm, rq); mb.quad(fm, rq[::-1])     # the rib
            for j in range(3):                                                                                     # leaflets: long, narrow, drooping
                u = (j + 0.5) / 3.0; c0 = p0.lerp(p1, u); tt = t0 + (t1 - t0) * u
                ll = 1.25 * math.sin(math.pi * min(1.0, 0.15 + tt * 0.95)) + 0.25; dz = -0.45 * ll - 0.25 * tt
                for sd in (1, -1):
                    tip = c0 + pa * (sd * ll) + (p1 - p0).normalized() * 0.35 * ll + Vector((0, 0, dz))
                    w_ = 0.10 * (1 - 0.5 * tt) + 0.04; dv = (p1 - p0).normalized() * w_
                    q = [c0 - dv, c0 + dv, tip + dv * 0.3, tip - dv * 0.3]
                    mb.quad(fm, q); mb.quad(fm, q[::-1])

def tile_mat(name, A, B, row=0.32, dark='#5a2216', straw=False):
    """roof covering: rows of tiles (or thatch courses) along the object Z, each row broken into tiles by a noise, two tones + dark grooves"""
    if name in K.MATS: return K.MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); bs = N('ShaderNodeBsdfPrincipled'); bs.inputs['Roughness'].default_value = 0.9; bs.inputs['Specular IOR Level'].default_value = 0.0
    tc = N('ShaderNodeTexCoord')
    wv = N('ShaderNodeTexWave'); wv.wave_type = 'BANDS'; wv.bands_direction = 'Z'; wv.wave_profile = 'SAW'; wv.inputs['Scale'].default_value = 2 * math.pi / (20.0 * row)
    wv.inputs['Distortion'].default_value = 0.6 if straw else 0.15; wv.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], wv.inputs['Vector'])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.6 if not straw else 0.7; nz.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    vo = N('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 2.2 if not straw else 9.0; L(tc.outputs['Object'], vo.inputs['Vector'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = hexc(A); mx.inputs[7].default_value = hexc(B); L(vo.outputs['Distance'] if 'Distance' in vo.outputs else vo.outputs[0], mx.inputs[0])
    cr = N('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = hexc(dark); cr.color_ramp.elements[1].position = 0.28 if not straw else 0.45; cr.color_ramp.elements[1].color = (1, 1, 1, 1)
    L(wv.outputs['Fac'], cr.inputs['Fac'])
    mul = N('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'; mul.inputs[0].default_value = 1.0; L(mx.outputs[2], mul.inputs[6]); L(cr.outputs[0], mul.inputs[7])
    mx2 = N('ShaderNodeMix'); mx2.data_type = 'RGBA'; mx2.blend_type = 'MULTIPLY'; L(mul.outputs[2], mx2.inputs[6]); mx2.inputs[7].default_value = hexc('#c8c0b0'); L(nz.outputs['Fac'], mx2.inputs[0])
    L(mx2.outputs[2], bs.inputs['Base Color'])
    bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.6; bp.inputs['Distance'].default_value = 0.05; L(wv.outputs['Fac'], bp.inputs['Height']); L(bp.outputs['Normal'], bs.inputs['Normal'])
    L(bs.outputs[0], out.inputs['Surface']); K.MATS[name] = m; return m

def house(mb, M, c, w, d, h, yaw, wallm, roofm, seed=0, hip=False, door_side=-1):
    """a colonial house: plastered walls on a darker plinth, a tiled (or thatched) gable / hip roof with eaves and a ridge, a door, shuttered
    windows on both long sides, a chimney on some.  door_side -1/+1 = the long side (local -y / +y) with the door."""
    rr = random.Random(seed); ca, sa = math.cos(yaw), math.sin(yaw)
    def P(x, y, z): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + z)
    mb.box(wallm, (c[0], c[1], c[2] + h / 2), (w, d, h), rz=yaw)
    mb.box(M['dark'], P(0, 0, 0.18), (w + 0.12, d + 0.12, 0.36), rz=yaw)                                   # plinth
    o = 0.45; rh = min(w, d) * 0.42 + 0.4; z0 = h - 0.05
    if hip:
        a, b = w / 2 + o, d / 2 + o; t = max(a - b, 0.3)
        v = [P(-a, -b, z0), P(a, -b, z0), P(t, 0, z0 + rh), P(-t, 0, z0 + rh)]; v2 = [P(a, b, z0), P(-a, b, z0), P(-t, 0, z0 + rh), P(t, 0, z0 + rh)]
        e1 = [P(-a, b, z0), P(-a, -b, z0), P(-t, 0, z0 + rh)]; e2 = [P(a, -b, z0), P(a, b, z0), P(t, 0, z0 + rh)]
        for q in (v, v2, e1, e2): mb.quad(roofm, q); mb.quad(roofm, q[::-1])
        ridge = (P(-t, 0, z0 + rh + 0.06), P(t, 0, z0 + rh + 0.06))
    else:
        a, b = w / 2 + o, d / 2 + o
        v = [P(-a, -b, z0), P(a, -b, z0), P(a, 0, z0 + rh), P(-a, 0, z0 + rh)]; v2 = [P(a, b, z0), P(-a, b, z0), P(-a, 0, z0 + rh), P(a, 0, z0 + rh)]
        for q in (v, v2): mb.quad(roofm, q); mb.quad(roofm, q[::-1])
        for sx in (-1, 1):                                                                                       # gable triangles (wall colour)
            g = [P(sx * w / 2, -d / 2, h), P(sx * w / 2, d / 2, h), P(sx * w / 2, 0, h + rh - 0.1)]; mb.quad(wallm, g); mb.quad(wallm, g[::-1])
        ridge = (P(-a, 0, z0 + rh + 0.06), P(a, 0, z0 + rh + 0.06))
    mb.rod(M['ridge'], ridge[0], ridge[1], 0.13, 0.13, 6)
    # door + windows with shutters
    sh = M[rr.choice(['shut1', 'shut2', 'shut3'])]
    dx = rr.uniform(-w * 0.25, w * 0.25)
    mb.box(M['dark'], P(dx, door_side * (d / 2 + 0.02), 1.0), (1.0, 0.08, 2.0), rz=yaw); mb.box(M['trim'], P(dx, door_side * (d / 2 + 0.04), 2.08), (1.3, 0.1, 0.16), rz=yaw)
    nwin = max(1, int(w / 2.6))
    for side in (-1, 1):
        for k in range(nwin):
            wx = -w / 2 + (k + 0.5) * w / nwin
            if side == door_side and abs(wx - dx) < 1.2: continue
            wz = h * 0.58 if h > 3.6 else 1.7
            mb.box(M['win'], P(wx, side * (d / 2 + 0.03), wz), (0.75, 0.06, 1.0), rz=yaw)
            for s2 in (-1, 1): mb.box(sh, P(wx + s2 * 0.6, side * (d / 2 + 0.05), wz), (0.42, 0.06, 1.05), rz=yaw)
    if rr.random() < 0.45:
        cx_ = rr.uniform(-w * 0.3, w * 0.3); mb.box(M['brick'], P(cx_, d * 0.18, h + rh * 0.7), (0.7, 0.7, rh * 1.0 + 0.6), rz=yaw)

def boat(mb, M, c, l, yaw, sail=True, seed=0, sm=None):
    ca, sa = math.cos(yaw), math.sin(yaw)
    mb.ell(M['boat'], (c[0], c[1], c[2] + 0.1), (l / 2, l * 0.18, l * 0.12), (14, 8), rot=(0, 0, yaw)); mb.ell(M['boatw'], (c[0], c[1], c[2] + 0.22), (l * 0.46, l * 0.15, l * 0.05), (14, 6), rot=(0, 0, yaw))
    if sail:
        mp = (c[0], c[1], c[2] + 0.3); mb.rod(M['trunk'], mp, (mp[0], mp[1], mp[2] + l * 0.9), 0.07, 0.04, 6)
        for sg in (1, -1):
            q = [(mp[0], mp[1], mp[2] + 0.5), (mp[0] - l * 0.38 * ca * 1.0 + 0.0, mp[1] - l * 0.38 * sa, mp[2] + 0.7), (mp[0] - l * 0.12 * ca, mp[1] - l * 0.12 * sa, mp[2] + l * 0.85), (mp[0], mp[1], mp[2] + l * 0.9)]
            mb.quad(sm or M['bsail'], q if sg > 0 else q[::-1])

def fort(mb, M, c, kind):
    wall = M.get('fstone', M['brick']) if kind == 'jamaica' else M['lime']
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

def rock(mb, m, c, r, h, seed, rz=0.0):
    """an irregular weathered boulder (lumpy icosphere, flat-ish top), base sunk below c[2]"""
    rr = np.random.RandomState(seed); ph = rr.uniform(0, 6.28, 6)
    bm = mb._b(m); res = bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
    M_ = Matrix.Translation(c) @ Euler((0, 0, rz)).to_matrix().to_4x4()
    for v in res['verts']:
        n = v.co.normalized()
        k = 1.0 + 0.2 * math.sin(2.3 * n.x + ph[0]) * math.cos(1.9 * n.y + ph[1]) + 0.14 * math.sin(3.7 * n.z + ph[2] + 2.0 * n.x) + 0.07 * math.sin(7.0 * n.x + 5.0 * n.y + ph[3])
        z = n.z * h * k * (1.0 if n.z > 0 else 0.6) * (1.0 - 0.2 * max(0.0, n.z - 0.7))
        v.co = mb.T @ (M_ @ Vector((n.x * r * k, n.y * r * 0.85 * k, z)))

def bush(mb, ms, c, r, rr, n=4):
    """a scrub bush: a few overlapping leaf blobs"""
    for k in range(n):
        a = rr.uniform(0, 6.28); d = rr.uniform(0.0, 0.6) * r; rk = r * rr.uniform(0.55, 0.9)
        mb.ell(ms[k % len(ms)], (c[0] + d * math.cos(a), c[1] + d * math.sin(a), c[2] + rk * 0.55), (rk, rk * rr.uniform(0.8, 1.0), rk * 0.8), (8, 6))

def tree(mb, M, ms, c, h, rr):
    """a broadleaf tropical tree: a short leaning trunk, two branches, a crown of 4-6 leaf blobs"""
    top = (c[0] + rr.uniform(-0.6, 0.6), c[1] + rr.uniform(-0.6, 0.6), c[2] + h * 0.62)
    mb.rod(M['bark'], (c[0], c[1], c[2] - 0.3), top, 0.32 * h / 8.0 + 0.12, 0.2, 7)
    R_ = h * 0.33
    for k in range(rr.randint(4, 6)):
        a = rr.uniform(0, 6.28); d = rr.uniform(0.2, 0.75) * R_; rk = R_ * rr.uniform(0.55, 0.85)
        mb.ell(ms[k % len(ms)], (top[0] + d * math.cos(a), top[1] + d * math.sin(a), top[2] + R_ * 0.35 + rr.uniform(-0.2, 0.5) * R_), (rk, rk, rk * 0.75), (10, 7))

def crate(mb, M, c, s, rz=0.0, h=None):
    """a plank crate: box + darker edge battens"""
    h = s if h is None else h
    mb.box(M['crate'], (c[0], c[1], c[2] + h / 2), (s, s, h), rz=rz)
    ca, sa = math.cos(rz), math.sin(rz)
    for (ex, ey) in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        x = c[0] + (ex * ca - ey * sa) * s / 2; y = c[1] + (ex * sa + ey * ca) * s / 2
        mb.box(M['batten'], (x, y, c[2] + h / 2), (0.07, 0.07, h + 0.02), rz=rz)
    for zz in (0.04, h - 0.04):
        mb.box(M['batten'], (c[0], c[1], c[2] + zz), (s + 0.04, s + 0.04, 0.07), rz=rz)

def barrel(mb, M, c, r, h, lying=False, rz=0.0):
    """a bulged stave barrel with iron hoops (standing, or lying on its side)"""
    if lying:
        ca, sa = math.cos(rz), math.sin(rz); d = Vector((ca, sa, 0)); cc = Vector((c[0], c[1], c[2] + r))
        for k in range(6):
            t0, t1 = -0.5 + k / 6.0, -0.5 + (k + 1) / 6.0; b0 = 1.0 + 0.12 * math.cos(math.pi * (t0 + t1)); 
            mb.rod(M['barrel'], cc + d * (t0 * h), cc + d * (t1 * h), r * (1 + 0.12 * math.cos(math.pi * 2 * t0)) * 0.9, r * (1 + 0.12 * math.cos(math.pi * 2 * t1)) * 0.9, 12)
        for t in (-0.38, -0.12, 0.12, 0.38): mb.rod(M['iron'], cc + d * (t * h - 0.025), cc + d * (t * h + 0.025), r * 1.0, r * 1.0, 12)
        return
    for k in range(6):
        t0, t1 = k / 6.0, (k + 1) / 6.0
        mb.rod(M['barrel'], (c[0], c[1], c[2] + t0 * h), (c[0], c[1], c[2] + t1 * h), r * (0.88 + 0.12 * math.sin(math.pi * t0)), r * (0.88 + 0.12 * math.sin(math.pi * t1)), 12)
    for t in (0.1, 0.32, 0.68, 0.9): mb.rod(M['iron'], (c[0], c[1], c[2] + t * h - 0.025), (c[0], c[1], c[2] + t * h + 0.025), r * (0.9 + 0.12 * math.sin(math.pi * t)), None, 12)
    mb.cyl(M['barrel_top'], (c[0], c[1], c[2] + h - 0.01), r * 0.86, 0.03, seg=12)

def text_mesh(name, body, size, m, loc, yaw, depth=0.02):
    """an in-world sign text: a font curve converted to a real mesh (Blender's built-in font), standing up, facing direction yaw"""
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body; cu.size = size; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.extrude = depth; cu.space_character = 1.08
    try:
        fp = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
        if os.path.exists(fp): cu.font = bpy.data.fonts.load(fp, check_existing=True)
    except Exception: pass
    ob = bpy.data.objects.new(name + '_c', cu); bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (math.pi / 2, 0, yaw + math.pi / 2); ob.location = loc; ob.parent = K.ROOT
    bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg)); mo = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(mo)
    mo.matrix_world = ob.matrix_world.copy(); mo.parent = K.ROOT; mo.matrix_parent_inverse = K.ROOT.matrix_world.inverted()
    me.materials.clear(); me.materials.append(m); bpy.data.objects.remove(ob); bpy.data.curves.remove(cu)
    return mo

def sign(mb, M, c, yaw, body='PORT ROYAL', w=1.9, hb=0.62, z0=1.55, size=0.34):
    """a painted landing sign: two posts, a red board with a cream border, the name in cream letters on BOTH faces"""
    ca, sa = math.cos(yaw), math.sin(yaw)
    def P(x, y, z): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + z)
    for sx in (-1, 1): mb.rod(M['post'], P(0, sx * (w / 2 - 0.12), -0.4), P(0, sx * (w / 2 - 0.12), z0 + hb + 0.25), 0.07, 0.06, 7)
    mb.box(M['signbd'], P(0, 0, z0 + hb / 2), (0.07, w, hb), rz=yaw)
    for sx in (-1, 1):
        mb.box(M['signtr'], P(0, 0, z0 + hb / 2 + sx * (hb / 2 - 0.03)), (0.09, w + 0.04, 0.06), rz=yaw)
        mb.box(M['signtr'], P(0, sx * (w / 2 - 0.0), z0 + hb / 2), (0.09, 0.06, hb), rz=yaw)
    for side in (1, -1):
        text_mesh('sign_txt%d' % side, body, size, M['signtx'], P(side * 0.045, 0, z0 + hb / 2 - 0.01), yaw if side > 0 else yaw + math.pi, 0.012)

def footprints(mb, m, pts, rr, step=0.62, w=0.06, l=0.12, gz=None):
    """a trail of alternating bare-foot prints along the polyline pts (x, y): slightly darker, damp little hollows on the sand"""
    for (a, b) in zip(pts[:-1], pts[1:]):
        a = Vector((a[0], a[1], 0)); b = Vector((b[0], b[1], 0)); d = b - a; ln = d.length; d.normalize(); n_ = Vector((-d.y, d.x, 0))
        for k in range(int(ln / step)):
            p = a + d * (k * step + rr.uniform(-0.05, 0.05)) + n_ * (0.11 if k % 2 else -0.11)
            z = gz(p.x, p.y) + 0.012
            mb.ell(m, (p.x, p.y, z - 0.006), (l, w, 0.008), (8, 3), rot=(0, 0, math.atan2(d.y, d.x) + rr.uniform(-0.15, 0.15)))

def net(mb, m, c, w, d, sag, rz, n=9):
    """a fishing net draped over two oars: a sagging grid of thin cords"""
    ca, sa = math.cos(rz), math.sin(rz)
    def P(x, y): z = c[2] + sag * (1 - (2 * x / w) ** 2) * 0.5 + 0.02; return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, z)
    for i in range(n + 1):
        x = -w / 2 + w * i / n; mb.rod(m, P(x, -d / 2), P(x, d / 2), 0.012, 0.012, 4, caps=False)
        y = -d / 2 + d * i / n; pts = [P(-w / 2 + w * k / 6, y) for k in range(7)]
        for a, b in zip(pts[:-1], pts[1:]): mb.rod(m, a, b, 0.012, 0.012, 4, caps=False)

_SPH = {}
def _unit_sphere(nu, nv):
    """UV-sphere verts (poles + rings) and quad/tri faces, cached per resolution"""
    if (nu, nv) not in _SPH:
        vs = [(0.0, 0.0, -1.0)]
        for j in range(1, nv):
            th = math.pi * j / nv - math.pi / 2
            for i in range(nu): a = 2 * math.pi * i / nu; vs.append((math.cos(th) * math.cos(a), math.cos(th) * math.sin(a), math.sin(th)))
        vs.append((0.0, 0.0, 1.0)); top = len(vs) - 1; fs = []
        for i in range(nu): fs.append((0, 1 + (i + 1) % nu, 1 + i))
        for j in range(nv - 2):
            b0, b1 = 1 + j * nu, 1 + (j + 1) * nu
            for i in range(nu): i2 = (i + 1) % nu; fs.append((b0 + i, b0 + i2, b1 + i2, b1 + i))
        b0 = 1 + (nv - 2) * nu
        for i in range(nu): fs.append((b0 + i, b0 + (i + 1) % nu, top))
        _SPH[(nu, nv)] = (np.array(vs), fs)
    return _SPH[(nu, nv)]

class MBF(MB):
    """MB whose ell() is batched in numpy (MB.ell = a bmesh op on a growing mesh, about 0.1 s per call with thousands of blobs):
    the ellipsoids of each material become one extra smooth object '<name>_<material>_e' at finish()."""
    def __init__(self, name): MB.__init__(self, name); self.E = {}
    def ell(self, m, c, r, seg=(12, 8), rot=(0, 0, 0)):
        M_ = self.T @ Matrix.Translation(c) @ Euler(rot).to_matrix().to_4x4() @ Matrix.Diagonal((r[0], r[1], r[2], 1))
        self.E.setdefault(m, []).append((np.array(M_), seg))
    def finish(self, coll=None, shadow=True, parent=None):
        objs = MB.finish(self, coll, shadow, parent); par = parent if parent is not None else K.ROOT
        for m, lst in self.E.items():
            V = []; F = []; n0 = 0
            for (Mx, seg) in lst:
                vs, fs = _unit_sphere(*seg); vw = vs @ Mx[:3, :3].T + Mx[:3, 3]; V.append(vw); F += [tuple(i + n0 for i in f) for f in fs]; n0 += len(vs)
            me = bpy.data.meshes.new('%s_%s_e' % (self.name, m.name)); me.from_pydata(np.concatenate(V).tolist(), [], F); me.update()
            me.polygons.foreach_set('use_smooth', np.ones(len(me.polygons), dtype=bool)); me.materials.append(m)
            ob = bpy.data.objects.new('%s_%s_e' % (self.name, m.name), me); (coll or bpy.context.scene.collection).objects.link(ob); ob.visible_shadow = shadow
            if par is not None: ob.parent = par
            objs.append(ob)
        self.E = {}; return objs

def coast(S, P, LT, sea_P, marks):
    kind = S['coast']; K.ROOT = S['world_root']; jam = kind == 'jamaica'
    sea_P['shore'] = shore_sd; sea_P['shal_w'] = 55.0; sea_P['shal_k'] = 0.95; sea_P['sea_shal'] = '#3ab6a8'
    M = dict(trunk=trunk_mat(), frond=leaf_mat('frond', '#4f9a34', '#3e8a30'), frond2=leaf_mat('frond2', '#64a83c', '#4f9636'), nut=mat('nut', '#6a8a2a', '#8a7a30', scale=8),
             dark=mat('dkdoor', '#3a2a24'), boat=mat('boat', '#7a4a30', '#8a5a3a', scale=3), boatw=mat('boatw', '#e8dcc0', '#d8ccb0', scale=3), bsail=mat('bsail', '#e8dcc0', '#dccfae', scale=2.5, emit='#ffe2a8', emit_k=0.1),
             bsail2=mat('bsail2', '#e8742c', '#d8602a', scale=2.5, emit='#ff9a50', emit_k=0.08),
             brick=mat('brick', '#b4623e', '#a4543a', scale=1.2), lime=mat('lime', '#e8e0cc', '#dcd4bc', scale=1.0), roofr=tile_mat('rooft', '#c4532e', '#a8402a'), iron=mat('iron2', '#2a2622', '#38322c', scale=6),
             flag=mat_emit('flagr', '#c8403a', 0.7), wall1=mat('wall1', '#f0e2c0', '#e6d6b0', scale=1.5, zgrad=(0.0, 1.2, '#b8a888')), wall2=mat('wall2', '#eac070', '#dcb060', scale=1.5, zgrad=(0.0, 1.2, '#a88a50')),
             wall3=mat('wall3', '#e48a6c', '#d47c60', scale=1.5, zgrad=(0.0, 1.2, '#a86a54')), wall4=mat('wall4', '#8cc0dc', '#7cb0d0', scale=1.5, zgrad=(0.0, 1.2, '#6a8aa0')),
             wall5=mat('wall5', '#a6d8b0', '#94c8a0', scale=1.5, zgrad=(0.0, 1.2, '#78a080')),
             quay=mat('quay', '#8a6a48', '#6e5238', scale=2.0, wave=(1.6, '#4e3a28')), cane=mat('cane', '#a8b84a', '#92a840', scale=0.6),
             tar=mat('tar', '#3a2a20', '#4a3626', scale=4, aniso=(1, 0.3, 0.3)), wale=mat('wale', '#b07a34', '#c28a40', scale=4), boatin=mat('boatin', '#9a7a52', '#8a6a46', scale=4, aniso=(0.3, 1, 1)), rope2=mat('rope2', '#c89a4c', '#a87c38', scale=6),
             ridge=mat('ridge', '#8a3420', '#7a2c1c', scale=3), trim=mat('trim', '#f4ecd8'), win=mat('win', '#2a2a3a'), shut1=mat('shut1', '#2e7a5a', '#286a50', scale=3), shut2=mat('shut2', '#2c5aa8', '#264e94', scale=3),
             shut3=mat('shut3', '#a8402e', '#963828', scale=3), thatch=tile_mat('thatch', '#c8a052', '#b08a40', row=0.24, dark='#6a5028', straw=True),
             bark=mat('bark', '#6a5038', '#54402c', scale=4, aniso=(0.3, 0.3, 1.0)), leaf1=leaf_mat('leaf1', '#2f8a34', '#3c9a3a', scale=1.2, glow='#1a4a1a', glow_k=0.06, tk=0.2),
             leaf2=leaf_mat('leaf2', '#4aa83a', '#3a9032', scale=1.2, glow='#1a4a1a', glow_k=0.06, tk=0.2), leaf3=leaf_mat('leaf3', '#287040', '#2f8040', scale=1.2, glow='#143a1a', glow_k=0.06, tk=0.2),
             rock=mat('rockc', '#8a7a68', '#6a5e52', scale=0.9, rough=0.9, zgrad=(-0.5, 1.5, '#4a4038')), crate=mat('crate', '#b08048', '#9a6c3a', scale=2.5, wave=(2.2, '#6a4a2a')), batten=mat('batten', '#6a4a2c', '#5a3e26', scale=4),
             barrel=mat('barrel', '#9a6a3c', '#7e5630', scale=3, aniso=(0.3, 0.3, 2.0)), barrel_top=mat('barrel_top', '#b08450', '#9a7444', scale=3), print=mat('fprint', '#b88038', '#ae7834', scale=4),
             drag=mat('dragtr', '#7e5228', '#6e4824', scale=2), post=mat('post', '#7a5a3a', '#5e4430', scale=4, aniso=(0.3, 0.3, 1)), signbd=mat('signbd', '#b8281e', '#a8241c', scale=3),
             signtr=mat('signtr', '#f2e2b8'), lamp=mat_emit('lampg', '#ffc060', 3.0), grass=leaf_mat('grass', '#7ab838', '#5a9a2e', scale=4, glow='#2a5a1a', glow_k=0.08, tk=0.3), signtx=mat('signtx', '#fff4d6', None, emit='#fff4d6', emit_k=0.35), netc=mat('netc', '#d8c8a0', '#c8b890', scale=6), gullw=mat('gullw', '#f6f5f0', '#e8ecee', scale=6), gullt=mat('gullt', '#2e3038'))
    if jam: M['fstone'] = mat('fstone', '#d8b880', '#c4a06a', scale=1.4, zgrad=(0.0, 2.5, '#8a7a5a'))
    if not jam: M['quay'] = mat('quay_b', '#b8aa90', '#a89c84', scale=1.5)
    M['oarb'] = mat('oarblade', '#e8dcc0', '#d8ccb0', scale=3)          # oar blades apart from 'shoredress_boatw' (render teams hide that object: the shells)
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
    lane = S['P'].get('lane') if jam else None                 # (y0, y1, d1): the BIGZOOM street, kept free of palms / houses (Jamaica)
    # ---- palms along the beach and in groves
    mbp = MBF('palms')
    for i in range(110 if not jam else 150):
        y = rr.uniform(-210.0, 330.0); d = rr.uniform(3.0, 46.0) if i < 70 else rr.uniform(20.0, 120.0)
        if 25.0 < y < 125.0 and d < 24.0: continue                                    # keep the quay open
        if jam and -27.0 < y < 137.0 and 20.0 < d < 100.0 and i >= 70: continue      # the town
        if lane and lane[0] - 6.0 < y < lane[1] + 6.0 and d < lane[2]: continue
        x = float(shore_x(y)) + d; palm(mbp, M, (x, y, gz(x, y) - 0.2), rr.uniform(6.5, 10.5), rr.uniform(0.3, 1.0), i + 5)
    mbp.finish(shadow=True)
    if jam: port_royal(S, P, LT, M, gz, lane)
    else:
        # ---- harbour town on the flat shelf
        mbh = MBF('town')
        for i in range(26):
            y = rr.uniform(25.0, 135.0); x = float(shore_x(y)) + rr.uniform(26.0, 110.0)
            if any(abs(y - py_) < 9 and abs(x - px_) < 10 for (px_, py_) in S.setdefault('_h', [])): continue
            S['_h'].append((x, y))
            house(mbh, M, (x, y, gz(x, y) - 0.3), rr.uniform(6.0, 10.0), rr.uniform(5.0, 7.5), rr.uniform(3.4, 5.2), rr.choice([0.0, 0.0, math.pi / 2, 0.2, -0.2]), M[rr.choice(['wall1', 'wall2', 'wall3', 'wall1'])], M['roofr'], seed=i)
        # wharf / quay + jetty
        ym0, ym1 = 52.0, 100.0; xq = float(shore_x(76.0))
        mbh.box(M['quay'], (xq - 3.0, 76.0, 0.55), (7.0, ym1 - ym0, 1.9)); mbh.box(M['quay'], (xq - 16.0, 66.0, 0.45), (28.0, 3.4, 1.4))
        for k in range(5): mbh.box(M['trunk'], (xq - 28.0 + 6.5 * k, 64.0, 0.9), (0.35, 0.35, 2.0)); mbh.box(M['trunk'], (xq - 28.0 + 6.5 * k, 68.0, 0.9), (0.35, 0.35, 2.0))
        for (y, w_) in ((60.0, 8.0), (80.0, 9.0), (92.0, 7.0)): house(mbh, M, (xq + 8.0, y, 0.8), w_, 6.5, 4.2, math.pi / 2, M['wall1'], M['roofr'], seed=int(y))
        for k in range(10):
            yy = rr.uniform(56.0, 96.0); mbh.box(M['trunk'], (xq - 2.0 + rr.uniform(-1.5, 1.5), yy, 1.9), (rr.uniform(0.7, 1.3),) * 2 + (rr.uniform(0.7, 1.2),), rz=rr.uniform(0, 3))
        # boats in the harbour
        for i in range(9):
            y = rr.uniform(20.0, 125.0); x = float(shore_x(y)) - rr.uniform(14.0, 90.0)
            if abs(x) < 26 and abs(y) < 40: continue
            bl, by_ = rr.uniform(6.0, 11.0), rr.uniform(0, 6.28)
            if S.get('preset') == 'ship_coast' and i % 3 == 2: continue            # the sail-less hulls read as brown discs floating on the sea (coast QA)
            boat(mbh, M, (x, y, 0.0), bl, by_, sail=(i % 3 != 2), seed=i)
        mbh.finish(shadow=True)
    # ---- fort + dressing
    mbf = MBF('fort')
    if jam:
        fy = -12.0; fx = float(shore_x(fy)) - 4.0                                               # on the near point of the bay, in the BIGZOOM wide
        fort(mbf, M, (fx, fy, 0.9), 'jamaica')
        pole = (fx + 13.0 - 1.5, fy - 7.5 + 1.5, 0.9 + 5.2)                                   # a second flag on the sea corner
        mbf.rod(M['trunk'], pole, (pole[0], pole[1], pole[2] + 9.0), 0.12, 0.07, 6)
        fl = [(pole[0], pole[1], pole[2] + 8.8), (pole[0] + 0.4, pole[1] + 3.3, pole[2] + 8.4), (pole[0] + 0.4, pole[1] + 3.3, pole[2] + 6.8), (pole[0], pole[1], pole[2] + 7.0)]
        mbf.quad(M['flag'], fl); mbf.quad(M['flag'], fl[::-1])
    else:
        hx, hy = float(shore_x(-70.0)) + 110.0, -70.0
        fort(mbf, M, (hx, hy, gz(hx, hy) - 0.5), 'barbados')
        windmill(mbf, M, (float(shore_x(190.0)) + 120.0, 190.0, gz(float(shore_x(190.0)) + 120.0, 190.0) - 0.4)); windmill(mbf, M, (float(shore_x(-150.0)) + 150.0, -150.0, gz(float(shore_x(-150.0)) + 150.0, -150.0) - 0.4), 9.0)
        for i in range(9):                                                                     # sugar-cane patches
            cx = float(shore_x(40.0 * i - 120.0)) + rr.uniform(60, 190); cy = 40.0 * i - 120.0
            mbf.box(M['cane'], (cx, cy, gz(cx, cy) + 0.9), (rr.uniform(14, 24), rr.uniform(14, 24), 1.8))
    mbf.finish(shadow=True)
    # ---- marks on the shore (metres, ship frame; z = ground): three standing places 4-7 m in front of the camera on the dry sand
    cam = np.array(P['cam']['loc'], dtype=np.float64); look = np.array(P['cam']['look'], dtype=np.float64)
    f = look - cam; f[2] = 0; f /= np.linalg.norm(f); r = np.array([f[1], -f[0], 0.0])
    def at(fw, rt):
        p = cam[:2] + f[:2] * fw + r[:2] * rt; return (float(p[0]), float(p[1]), gz(float(p[0]), float(p[1])))
    S['shore_marks'] = dict(shore_a=at(4.4, 0.55), shore_b=at(5.6, 2.0), shore_c=at(6.6, -0.9))
    S['extra_cams'] = {}
    # ---- beach dressing near the camera: a longboat hauled up on the left, oars, driftwood, two palms leaning in on the right, wet-sand darkening is in the terrain material
    mbd = MBF('shoredress'); ang = math.atan2(f[1], f[0])
    bp = at(7.4, -3.4); longboat(mbd, M, (bp[0], bp[1], bp[2] + 0.05), 5.6, ang + 0.42)
    for k, (fw, rt, ln, yw) in enumerate(((3.6, -3.0, 2.6, 0.3), (8.8, 2.7, 3.4, -0.5), (3.2, 3.6, 1.8, 0.9))):                      # driftwood logs
        p = at(fw, rt); mbd.rod(M['trunk'], (p[0] - ln / 2 * math.cos(ang + yw), p[1] - ln / 2 * math.sin(ang + yw), p[2] + 0.16), (p[0] + ln / 2 * math.cos(ang + yw), p[1] + ln / 2 * math.sin(ang + yw), p[2] + 0.2), 0.17, 0.13, 8)
    for (fw, rt, hh, sd) in ((7.6, 3.9, 7.0, 91), (11.0, 7.6, 9.0, 92)):
        p = at(fw, rt); palm(mbd, M, (p[0], p[1], p[2] - 0.2), hh, 0.9, sd)
    if not jam:
        for k in range(7):                                                                                                      # shells / stones on the sand
            p = at(2.6 + 0.9 * (k % 4), -1.6 + 0.9 * k); mbd.ell(M['boatw'], (p[0], p[1], p[2] + 0.04), (0.1, 0.07, 0.04), (6, 4))
        barbados_life(M, mbd, at, gz)
    else:
        beach_life(S, P, M, mbd, at, gz, ang); beach_mid(M, mbd, gz)
    mbd.finish(shadow=True)
    if S['preset'] == 'ship_coast':
        headland(LT, (-430.0, 55.0), math.radians(95), 420.0, 58.0, 90.0, seed=14, name='headland_coast')

def stall(mb, M, c, yaw, w=2.6, d=1.8, h=2.3, aw='awn1'):
    """a market stall: four posts, a sloping striped awning, a counter with fruit / cloth bundles"""
    ca, sa = math.cos(yaw), math.sin(yaw)
    def P(x, y, z): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + z)
    for sx in (-1, 1):
        for sy in (-1, 1): mb.rod(M['post'], P(sx * w / 2, sy * d / 2, 0), P(sx * w / 2, sy * d / 2, h + (0.35 if sy > 0 else 0.0)), 0.09, 0.08, 6)
    q = [P(-w / 2 - 0.2, -d / 2 - 0.3, h - 0.05), P(w / 2 + 0.2, -d / 2 - 0.3, h - 0.05), P(w / 2 + 0.2, d / 2 + 0.1, h + 0.4), P(-w / 2 - 0.2, d / 2 + 0.1, h + 0.4)]
    mb.quad(M[aw], q); mb.quad(M[aw], q[::-1])
    mb.box(M['crate'], P(0, -d / 2 + 0.35, 0.45), (w * 0.9, 0.6, 0.9), rz=yaw)
    rr = random.Random(int(abs(c[0] * 7 + c[1] * 13)))
    for k in range(6):
        mb.ell(M[rr.choice(['fruit1', 'fruit2', 'fruit3'])], P(rr.uniform(-w * 0.4, w * 0.4), -d / 2 + 0.35 + rr.uniform(-0.15, 0.15), 0.95), (0.16, 0.16, 0.12), (6, 4))

def port_royal(S, P, LT, M, gz, lane):
    """Jamaica: Port Royal behind the beach -- five rows of plastered houses (red tile or thatch roofs, doors, shuttered windows, chimneys)
    along streets parallel to the shore, a church tower, a planked quay with a jetty, warehouses, market stalls along the BIGZOOM street
    (lane), boats with cream and orange sails in the bay.  The lane (y0, y1, d1) stays open so the camera can fly down it to the beach."""
    rr = random.Random(23); mb = MBF('town'); S['_h'] = []
    for nm, a, b in (('awn1', '#d82a1a', '#f8d040'), ('awn2', '#f0a010', '#d82a1a'), ('awn3', '#1a58d0', '#f8d040')):
        M[nm] = mat(nm, a, None, wave=(3.2, b)); M[nm].node_tree.nodes['bsdf'].inputs['Emission Color'].default_value = hexc(a); M[nm].node_tree.nodes['bsdf'].inputs['Emission Strength'].default_value = 0.08
    M['fruit1'] = mat('fruit1', '#f0a020'); M['fruit2'] = mat('fruit2', '#d8402a'); M['fruit3'] = mat('fruit3', '#7ab030')
    walls = ['wall1', 'wall2', 'wall3', 'wall4', 'wall5', 'wall1', 'wall2', 'wall3']
    rows = [(25.0, 9.0), (38.0, 10.0), (52.0, 9.0), (65.0, 10.0), (79.0, 9.0), (92.0, 9.0)]
    church = (2, 70.0)
    for ri, (d0, dep) in enumerate(rows):
        y = -26.0 + rr.uniform(0, 4)
        while y < 138.0:
            wy = rr.uniform(7.0, 10.5); yc = y + wy / 2
            if lane and yc + wy / 2 > lane[0] - 0.5 and yc - wy / 2 < lane[1] + 0.5 and d0 < lane[2]:
                y = lane[1] + 0.5 + rr.uniform(0, 1.0); continue
            if ri == church[0] and abs(yc - church[1]) < 8:
                x = float(shore_x(yc)) + d0 + dep / 2; z = gz(x, yc) - 0.3
                house(mb, M, (x, yc, z), 9.0, dep, 6.5, math.pi / 2, M['wall1'], M['roofr'], seed=999)
                tx = x + dep / 2 - 2.0; mb.box(M['wall1'], (tx, yc, z + 6.5), (3.6, 3.6, 13.0)); mb.box(M['trim'], (tx, yc, z + 13.1), (4.0, 4.0, 0.4))
                mb.cone(M['roofr'], (tx, yc, z + 13.3), 2.6, 0.05, 4.2, 4)
                for sx in (-1, 1): mb.box(M['win'], (tx + sx * 1.82, yc, z + 10.5), (0.06, 0.9, 1.6))
                y = church[1] + 9.0; continue
            if rr.random() < 0.07: y += wy + 3.0; continue                                  # a yard
            x = float(shore_x(yc)) + d0 + dep / 2 + rr.uniform(-0.6, 0.6)
            h = rr.choice([3.6, 4.0, 4.4, 5.0, 6.6]) + rr.uniform(-0.2, 0.2)
            roof = M['thatch'] if rr.random() < 0.18 else M['roofr']
            house(mb, M, (x, yc, gz(x, yc) - 0.3), wy - 0.8, dep - rr.uniform(1.0, 2.5), h, math.pi / 2 + rr.uniform(-0.05, 0.05), M[rr.choice(walls)], roof, seed=ri * 100 + int(y), hip=rr.random() < 0.4, door_side=rr.choice([-1, 1]))
            S['_h'].append((x, yc)); y += wy + rr.uniform(0.2, 0.8)
    # the lane: market stalls along both edges, barrels, a hand cart
    if lane:
        yc = 0.5 * (lane[0] + lane[1]); hw = 0.5 * (lane[1] - lane[0])
        for k in range(7):
            yy = yc + rr.choice([-1, 1]) * (hw - rr.uniform(0.4, 0.9)); dd = rr.uniform(24.0, 62.0); x = float(shore_x(yy)) + dd
            barrel(mb, M, (x, yy, gz(x, yy) - 0.05), 0.33, 0.9)
    # quay (planked) + jetty, warehouses
    ym0, ym1 = 52.0, 100.0; xq = float(shore_x(76.0))
    mb.box(M['quay'], (xq - 3.0, 76.0, 0.55), (7.0, ym1 - ym0, 1.9)); mb.box(M['quay'], (xq - 16.0, 66.0, 0.45), (28.0, 3.4, 1.4))
    for k in range(5): mb.box(M['post'], (xq - 28.0 + 6.5 * k, 64.0, 0.4), (0.35, 0.35, 2.6)); mb.box(M['post'], (xq - 28.0 + 6.5 * k, 68.0, 0.4), (0.35, 0.35, 2.6))
    for (y, w_) in ((60.0, 8.0), (80.0, 9.0), (92.0, 7.0)): house(mb, M, (xq + 8.0, y, 0.8), w_, 6.5, 4.6, math.pi / 2, M['wall2'], M['roofr'], seed=int(y), door_side=1)
    for k in range(14):
        yy = rr.uniform(56.0, 96.0); xx = xq - 2.0 + rr.uniform(-2.2, 2.2)
        (crate(mb, M, (xx, yy, 1.5), rr.uniform(0.8, 1.2), rr.uniform(0, 3)) if k % 2 else barrel(mb, M, (xx, yy, 1.5), 0.35, 0.95))
    # boats in the bay: fishing boats and sloops with cream / orange sails
    for i in range(14):
        y = rr.uniform(-60.0, 170.0); x = float(shore_x(y)) - rr.uniform(16.0, 140.0)
        if abs(x) < 30 and abs(y) < 45: continue
        if abs(y - 33.0) < 12 and x > 200: continue                                           # keep the water behind the cast clear
        boat(mb, M, (x, y, 0.0), rr.uniform(6.0, 11.0), rr.uniform(0, 6.28), sail=True, seed=i, sm=M['bsail2'] if i % 3 == 0 else M['bsail'])
    mb.finish(shadow=True)
    # jungle: scrub, broadleaf trees and boulders on the slopes behind the town and on both points of the bay; rocks at the waterline
    jb = MBF('jungle'); jr = random.Random(41); ms = [M['leaf1'], M['leaf2'], M['leaf3']]
    for i in range(900):
        y = jr.uniform(-260.0, 360.0); d = jr.uniform(8.0, 230.0) ** 1.0
        if -28.0 < y < 140.0 and 20.0 < d < 103.0: continue                                   # the town
        if lane and lane[0] - 6.0 < y < lane[1] + 6.0 and d < lane[2] + 10.0: continue
        if d < 16.0 and not (y < -30.0 or y > 120.0): continue                                 # the open beach in front of the town
        x = float(shore_x(y)) + d; z = gz(x, y)
        if z < 0.3: continue
        if jr.random() < 0.3: tree(jb, M, ms, (x, y, z), jr.uniform(6.0, 11.0), jr)
        else: bush(jb, ms, (x, y, z - 0.2), jr.uniform(1.2, 3.0), jr)
    rk = MBF('rocks_coast')
    for (y0, y1, n) in ((-75.0, 2.0, 30), (110.0, 175.0, 26), (190.0, 300.0, 18)):
        for k in range(n):
            y = jr.uniform(y0, y1); d = jr.uniform(-4.0, 9.0); x = float(shore_x(y)) + d
            rock(rk, M['rock'], (x, y, max(gz(x, y), -0.6) - 0.2), jr.uniform(0.8, 3.2), jr.uniform(0.7, 2.2), 300 + k + int(y0), jr.uniform(0, 6.28))
    for k in range(40):
        y = jr.uniform(-200.0, 320.0); d = jr.uniform(30.0, 200.0)
        if -28.0 < y < 140.0 and d < 103.0: continue
        x = float(shore_x(y)) + d; rock(rk, M['rock'], (x, y, gz(x, y) - 0.4), jr.uniform(1.5, 4.0), jr.uniform(1.0, 2.5), 500 + k, jr.uniform(0, 6.28))
    jb.finish(shadow=True); rk.finish(shadow=True)
    for nm, (x, y, h, sd) in (P.get('zoom_palms') or {}).items():                                # the palms the BIGZOOM passes (1-2 D from the lens)
        zp = MBF('zoompalm_' + nm); palm(zp, M, (x, y, gz(x, y) - 0.2), h, 0.5, sd, nf=11); zp.finish(shadow=True)

def barbados_life(M, mb, at, gz):
    """Barbados landing (2026-11-20, QA-art r9: the lower frame was bare sand): footprints to the crew, a crate stack and barrels at the
    frame sides in the near foreground, a rope coil; no sign (the PORT ROYAL sign is Jamaica only)"""
    rr = random.Random(53)
    def xy(fw, rt): p = at(fw, rt); return (p[0], p[1])
    footprints(mb, M['print'], [xy(8.4, -2.4), xy(6.8, -1.4), xy(5.4, -0.4), xy(4.6, 0.4)], rr, gz=gz)
    footprints(mb, M['print'], [xy(3.0, 2.4), xy(4.2, 1.6), xy(5.4, 1.9)], rr, gz=gz)
    for (fw, rt, s_, rz) in ((4.6, -2.0, 0.75, 0.3), (5.0, -2.6, 0.6, 1.1), (4.8, 2.3, 0.7, -0.4)):
        p = at(fw, rt); crate(mb, M, (p[0], p[1], p[2] - 0.03), s_, rz)
    p = at(4.75, -2.25); crate(mb, M, (p[0], p[1], p[2] + 0.72), 0.55, 0.7)
    p = at(4.2, 1.85); barrel(mb, M, (p[0], p[1], p[2] - 0.03), 0.3, 0.85)
    p = at(5.6, 3.0); barrel(mb, M, (p[0], p[1], p[2] - 0.02), 0.28, 0.6, lying=True, rz=0.9)
    p = at(3.9, -1.1)
    for l_ in range(4): ring_xy(mb, M['rope2'], (p[0], p[1], p[2] + 0.03 + 0.05 * l_), 0.24 - 0.03 * l_, 0.06, 0.06, 16)

def beach_life(S, P, M, mb, at, gz, ang):
    """Jamaica landing: footprints from the longboat to the crew and up the beach, the longboat's drag track down to the water, crates,
    barrels, a rope coil, a net over the oars, the PORT ROYAL sign, gulls"""
    rr = random.Random(77)
    def xy(fw, rt): p = at(fw, rt); return (p[0], p[1])
    gzf = lambda x, y: gz(x, y)
    # drag track: the keel groove + two side ruts from the boat's stern to the waterline
    b0 = Vector(at(7.4, -3.4)); dbt = Vector((math.cos(ang + 0.42), math.sin(ang + 0.42), 0)); st = b0 + dbt * 2.7
    for k in range(18):
        p = st + dbt * (0.5 * k)
        for off, wd in ((0.0, 0.28), (0.55, 0.12), (-0.55, 0.12)):
            q = p + Vector((-dbt.y, dbt.x, 0)) * off
            mb.ell(M['drag'], (q.x, q.y, gz(q.x, q.y) + 0.008), (0.32, wd, 0.012), (8, 3), rot=(0, 0, ang + 0.42))
    footprints(mb, M['print'], [xy(8.2, -2.0), xy(6.6, -1.2), xy(5.2, -0.3), xy(4.7, 0.3)], rr, gz=gzf)
    footprints(mb, M['print'], [xy(8.6, -1.4), xy(6.8, -0.2), xy(5.4, 1.0), xy(4.9, 1.4)], rr, gz=gzf)
    footprints(mb, M['print'], [xy(4.1, 0.6), xy(3.0, 0.1), xy(1.4, -0.4), xy(-2.0, -1.0), xy(-6.0, -1.2)], rr, gz=gzf)
    footprints(mb, M['print'], [xy(4.3, -0.4), xy(3.1, -1.1), xy(1.0, -2.2), xy(-3.0, -3.0)], rr, gz=gzf)
    footprints(mb, M['print'], [xy(3.4, 1.8), xy(1.8, 2.6), xy(-1.5, 3.4)], rr, gz=gzf)
    # cargo by the boat
    for (fw, rt, s_, rz) in ((6.2, -2.35, 0.62, 0.3), (6.5, -2.95, 0.55, 0.9), (6.35, -2.65, 0.5, 0.5)):
        p = at(fw, rt); crate(mb, M, (p[0], p[1], p[2] - 0.03 + (0.6 if (fw, rt) == (6.35, -2.65) else 0.0)), s_, rz)
    p = at(5.6, -2.6); barrel(mb, M, (p[0], p[1], p[2] - 0.03), 0.3, 0.85)
    p = at(5.9, 2.75); barrel(mb, M, (p[0], p[1], p[2] - 0.02), 0.28, 0.6, lying=True, rz=ang + 1.2)
    p = at(6.8, 2.4); crate(mb, M, (p[0], p[1], p[2] - 0.03), 0.6, 0.4)
    # rope coils: one in the foreground left, one by the crates right
    for (fw, rt, r_) in ((6.3, 1.95, 0.24),):
        p = at(fw, rt)
        for l_ in range(4): ring_xy(mb, M['rope2'], (p[0], p[1], p[2] + 0.03 + 0.05 * l_), r_ - 0.03 * l_, 0.06, 0.06, 16)
    # a net hung over two upright oars beside the boat
    p = at(8.9, -1.9)
    for sx in (-1, 1):
        q = (p[0] + sx * 0.9 * math.sin(ang), p[1] - sx * 0.9 * math.cos(ang))
        mb.rod(M['trunk'], (q[0], q[1], gz(*q) - 0.3), (q[0], q[1], gz(*q) + 1.6), 0.04, 0.035, 6)
    net(mb, M['netc'], (p[0], p[1], p[2] + 1.05), 1.8, 0.05, -0.9, ang + math.pi / 2)
    # the landing sign: PORT ROYAL, facing up the beach (towards the town and the camera)
    sp = at(*S['P'].get('sign_at', (8.8, -2.25)))
    sign(mb, M, sp, ang + math.pi)
    # gulls over the beach and the bay
    for (fw, rt, z, yw, s_, fl) in ((14.0, -3.5, 7.5, 1.0, 0.42, 0.5), (19.0, 2.5, 10.5, 2.6, 0.45, -0.2), (24.0, -6.0, 12.0, 0.3, 0.5, 0.2), (11.0, 4.0, 5.6, 3.6, 0.38, 0.7),
                                    (-20.0, 6.0, 26.0, 1.5, 0.9, 0.3), (-35.0, -10.0, 33.0, 4.0, 0.9, -0.3), (-12.0, -18.0, 22.0, 2.2, 0.8, 0.6)):
        p = at(fw, rt); FX.gull6(mb, M['gullw'], M['gullt'], (p[0], p[1], z), yw, s_, fl)

def tuft(mb, m, c, rr, n=7, h=0.55):
    """a clump of beach grass: thin leaning blades"""
    for k in range(n):
        a = rr.uniform(0, 6.28); l = h * rr.uniform(0.6, 1.1); tip = (c[0] + 0.35 * l * math.cos(a), c[1] + 0.35 * l * math.sin(a), c[2] + l)
        pa = (-math.sin(a) * 0.035, math.cos(a) * 0.035)
        q = [(c[0] - pa[0], c[1] - pa[1], c[2] - 0.05), (c[0] + pa[0], c[1] + pa[1], c[2] - 0.05), tip]; mb.quad(m, q); mb.quad(m, q[::-1])

def beach_mid(M, mb, gz):
    """Jamaica: the beach the BIGZOOM crosses (x 236-262 m, y 10-55 m): a second boat drawn up, cargo stacks, a cannon on its carriage,
    a net drying on poles, coconuts, driftwood and beach-grass tufts, so the sand between the town and the cast is never bare"""
    rr = random.Random(91)
    def G(x, y): return (x, y, gz(x, y))
    for (x, y, yw, l_) in ((249.0, 47.5, 2.6, 5.0), (240.5, 17.0, 3.5, 4.4)):
        c = G(x, y); longboat(mb, M, (c[0], c[1], c[2] + 0.05), l_, yw)
    for (x, y) in ((252.5, 21.0), (247.0, 52.5), (256.0, 44.0), (244.5, 13.0)):
        c = G(x, y)
        for k in range(rr.randint(3, 5)):
            dx, dy = rr.uniform(-1.2, 1.2), rr.uniform(-1.2, 1.2); cc = G(c[0] + dx, c[1] + dy)
            (crate(mb, M, (cc[0], cc[1], cc[2] - 0.03), rr.uniform(0.55, 0.85), rr.uniform(0, 3)) if rr.random() < 0.5 else barrel(mb, M, (cc[0], cc[1], cc[2] - 0.03), 0.3, 0.85))
        if rr.random() < 0.6: cc = G(c[0] + 0.3, c[1] + 0.2); crate(mb, M, (cc[0], cc[1], cc[2] + 0.7), 0.6, rr.uniform(0, 3))
    c = G(251.0, 30.5); ca = math.pi                                                           # cannon pointing out to sea
    mb.box(M['batten'], (c[0], c[1], c[2] + 0.35), (1.6, 0.9, 0.35)); 
    for sy in (-1, 1):
        for sx in (-1, 1): mb.cyl(M['batten'], (c[0] + sx * 0.55, c[1] + sy * 0.5, c[2] + 0.28), 0.28, 0.12, axis='y', seg=10)
    mb.rod(M['iron'], (c[0] + 0.7, c[1], c[2] + 0.75), (c[0] - 1.6, c[1], c[2] + 0.7), 0.24, 0.17, 12)
    for k in range(5): cc = G(c[0] + 0.9 + 0.22 * k, c[1] + 0.8); mb.ell(M['iron'], (cc[0], cc[1], cc[2] + 0.12), (0.12, 0.12, 0.12), (8, 5))
    for (x, y) in ((246.5, 24.0), (250.5, 25.5)):                                              # net drying on two poles
        mb.rod(M['post'], G(x, y), (x, y, gz(x, y) + 2.0), 0.05, 0.04, 6)
    a0 = G(246.5, 24.0); net(mb, M['netc'], (248.5, 24.75, a0[2] + 1.9), 4.2, 0.05, -1.4, math.atan2(1.5, 4.0))
    # right under the descent (x 245-250 m, behind the medium-shot camera): sea chest, lantern, rope, an anchor, a lying barrel
    c = G(247.6, 30.6); mb.box(M['barrel'], (c[0], c[1], c[2] + 0.28), (0.95, 0.6, 0.56), rz=0.3); mb.box(M['batten'], (c[0], c[1], c[2] + 0.6), (1.0, 0.64, 0.1), rz=0.3)   # sea chest
    for k in (-0.3, 0.3): mb.box(M['iron'], (c[0] + k * math.cos(0.3), c[1] + k * math.sin(0.3), c[2] + 0.33), (0.07, 0.66, 0.6), rz=0.3)
    c = G(248.8, 35.6); crate(mb, M, (c[0], c[1], c[2] - 0.03), 0.7, 0.5); mb.cyl(M['iron'], (c[0], c[1], c[2] + 0.85), 0.11, 0.3, seg=8); mb.ell(M['lamp'], (c[0], c[1], c[2] + 0.85), (0.08, 0.08, 0.12), (8, 5))
    c = G(246.0, 35.3)
    for l_ in range(4): ring_xy(mb, M['rope2'], (c[0], c[1], c[2] + 0.03 + 0.05 * l_), 0.32 - 0.03 * l_, 0.06, 0.06, 16)
    c = G(249.8, 33.4); mb.rod(M['iron'], (c[0] - 1.1, c[1], c[2] + 0.12), (c[0] + 0.6, c[1], c[2] + 0.12), 0.08, 0.08, 8)       # anchor
    mb.rod(M['iron'], (c[0] - 1.1, c[1] - 0.7, c[2] + 0.12), (c[0] - 1.1, c[1] + 0.7, c[2] + 0.12), 0.07, 0.07, 8); mb.rod(M['iron'], (c[0] + 0.6, c[1] - 0.6, c[2] + 0.12), (c[0] + 0.6, c[1] + 0.6, c[2] + 0.12), 0.06, 0.06, 8)
    c = G(245.3, 29.0); barrel(mb, M, (c[0], c[1], c[2] - 0.02), 0.3, 0.85, lying=True, rz=1.1)
    for k in range(60):                                                                        # grass tufts + coconuts + driftwood on the dry sand
        y = rr.uniform(5.0, 60.0); x = float(shore_x(y)) + rr.uniform(9.0, 24.0)
        if abs(y - 33.0) < 4.0 and x < 250.0: continue
        c = G(x, y)
        r_ = rr.random()
        if r_ < 0.6: tuft(mb, M['grass'], c, rr, n=rr.randint(6, 11), h=rr.uniform(0.4, 0.8))
        elif r_ < 0.85: mb.ell(M['nut'], (c[0], c[1], c[2] + 0.1), (0.17, 0.15, 0.13), (8, 5))
        else:
            yw = rr.uniform(0, 6.28); ln = rr.uniform(1.2, 2.6)
            mb.rod(M['trunk'], (c[0] - ln / 2 * math.cos(yw), c[1] - ln / 2 * math.sin(yw), c[2] + 0.1), (c[0] + ln / 2 * math.cos(yw), c[1] + ln / 2 * math.sin(yw), c[2] + 0.14), 0.12, 0.09, 7)

def longboat(mb, M, c, l, yaw):
    """a ship's longboat hauled up on the sand: lofted planked hull (tarred outside, light wale strip, pale inside), gunwale, thwarts, oars, a coil of rope, a boat hook"""
    ca, sa = math.cos(yaw), math.sin(yaw)
    def P(x, y, z): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca, c[2] + z)
    nt, ns = 14, 6; hl = l / 2
    def sec(t, s):
        u = 2 * t - 1; w = 0.95 * (1 - abs(u) ** 2.2) ** 0.7 + 0.04; zk = 0.25 + 0.1 * u * u; zg = 0.95 + 0.42 * abs(u) ** 2.4
        return (w * s ** 0.8, u * hl, zk + (zg - zk) * s ** 1.5)
    for t in range(nt):
        for s in range(ns):
            for sd in (-1, 1):
                p = [sec(t / nt, s / ns), sec((t + 1) / nt, s / ns), sec((t + 1) / nt, (s + 1) / ns), sec(t / nt, (s + 1) / ns)]
                q = [P(sd * a, b, z) for (a, b, z) in p]; qi = [P(sd * a * 0.94, b, z + 0.06) for (a, b, z) in p]
                mat_ = M['wale'] if s == ns - 2 else M['tar']
                mb.quad(mat_, q if sd > 0 else q[::-1]); mb.quad(M['boatin'], qi[::-1] if sd > 0 else qi)
    for t in range(nt):                                                                                                       # gunwale strip
        for sd in (-1, 1):
            a0 = sec(t / nt, 1.0); a1 = sec((t + 1) / nt, 1.0)
            q = [P(sd * a0[0], a0[1], a0[2] + 0.02), P(sd * a1[0], a1[1], a1[2] + 0.02), P(sd * a1[0] * 0.9, a1[1], a1[2] + 0.04), P(sd * a0[0] * 0.9, a0[1], a0[2] + 0.04)]
            mb.quad(M['wale'], q); mb.quad(M['wale'], q[::-1])
    for tt in (-0.55, -0.15, 0.25, 0.62):
        w = sec(0.5 + tt / 2, 1.0)[0] * 0.9
        mb.box(M['boatin'], P(0, tt * hl * 2 * 0.5 + 0.0, 0.72), (2 * w, 0.28, 0.06), rz=yaw)
    for sd in (-1, 1):                                                                                                        # oars laid across the thwarts
        for k, tt in enumerate((-0.35, 0.05)):
            x0, y0, z0 = P(sd * 0.1, tt * l * 0.5, 0.82); x1, y1, z1 = P(sd * 2.5, tt * l * 0.5 + 0.9 * sd, 0.55)
            mb.rod(M['trunk'], (x0, y0, z0), (x1, y1, z1), 0.04, 0.03, 6); mb.box(M.get('oarb', M['boatw']), (x1, y1, z1 - 0.01), (0.12, 0.5, 0.03), rz=yaw + 0.3)
    mb.rod(M['trunk'], P(-0.1, hl * 0.7, 0.9), P(0.1, -hl * 0.6, 1.0), 0.03, 0.03, 6)
    for l_ in range(3): ring_xy(mb, M['rope2'], P(0.0, -hl * 0.35, 0.52 + 0.06 * l_), 0.28 - 0.02 * l_, 0.07, 0.07, 14)

def ring_xy(mb, m, c, r, w, h, n=14):
    for i in range(n):
        a = 2 * math.pi * (i + .5) / n; seg = 2 * math.pi * r / n * 1.2
        mb.box(m, (c[0] + r * math.cos(a), c[1] + r * math.sin(a), c[2]), (seg, w, h), rz=a + math.pi / 2)

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
