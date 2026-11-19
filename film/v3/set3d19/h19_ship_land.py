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
    kd = SE.v6_dir(kdir_(az, el)) if True else None
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
    else:
        raise NotImplementedError(kind)

def kdir_(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

def clouds_for(kind):
    if kind == 'hero':
        return [(nm, SE.v6_pos(c), sz, sd) for (nm, c, sz, sd) in [('cF', (-40, 620, 330), 46, 17), ('cA', (-250, 430, 130), 36, 3), ('cB', (150, 520, 215), 44, 7), ('cC', (-330, 700, 90), 40, 5), ('cD', (380, 560, 70), 30, 11), ('cE', (20, 900, 120), 60, 13)]]
    return []

def rain(S, on, frame=None):
    pass
