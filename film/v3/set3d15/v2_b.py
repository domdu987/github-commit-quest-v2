#!/usr/bin/env python3
"""v2_b.py : film 15 v2 upgrade of location B (Mexico City 1968 stadium + 1972 day variant). Extension of set15 (nothing in set15*.py is edited).

    import v2_b as B2
    A = B2.build('NIGHT')        # NIGHT (dusk, floodlit, BIGZOOM 2 / T3 / T4) | TENSE (darker, T4 hush / T5) | DAY72 (1972 day, T7)
    ...F.make_camera / SH.* / cast cards as in set15 + cast_test...
See API_v2_b.md. Metres inside builders; cameras / marks in D (1 D = 0.54 m) like set15; B2.M2D(p_m) converts metres -> D."""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'work_v2_b'))
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
import set15 as F
import set15_lib as L
import set15_b as LB
from set15_lib import S, U, DM, STATE, mat, mat_emit, rnd, adopt, root, kdir
import v2_b_tex as TX

TEXD = TX.TEX
if not os.path.exists(os.path.join(TEXD, 'foam_top.png')): TX.make_all()

# ------------------------------------------------------------------ constants of B (see set15_b)
SX, SY = LB.SX, LB.SY
AO = LB.A0 + LB.NROW * LB.RW; BO = LB.B0 + LB.NROW * LB.RW; ZT = 1.0 + LB.NROW * LB.RISE      # outer rim ellipse (89.2 x 61.2 m), top of the last row 21.16 m
ell = LB.ell_pt
FOAM_TOP = LB.FOAM_TOP; FOAM_SURF = FOAM_TOP + 0.056; BAR_Y = LB.BAR_Y_B; PIT = LB.PIT_B
def M2D(p): return tuple(c * U for c in p)

# vivid crowd shirts (S.CROWD_HEX is read by set15_b.build_crowd at build time)
S.CROWD_HEX = ['#ff3b2f', '#ffffff', '#ffd21f', '#2f7bff', '#ff7a1a', '#fff0d8', '#19b9ff', '#2fd06b', '#e8203a', '#f8f0d8', '#ffb01f', '#3a5cff', '#ff5a2a', '#ffffff']

# ------------------------------------------------------------------ light presets (B_NIGHT, B_TENSE2, B_DAY72)
SKY_NIGHT = [(0.0, '#14127a'), (0.30, '#2a2cb0'), (0.44, '#4a3ac0'), (0.485, '#b84a9a'), (0.505, '#ff7a30'), (0.525, '#ffb25a'), (0.56, '#6a3ab8'), (0.66, '#2832b4'), (0.82, '#16168c'), (1.0, '#0c0c64')]
SKY_TENSE = [(0.0, '#100e66'), (0.30, '#1c1c96'), (0.44, '#3a2aa6'), (0.485, '#a03a8c'), (0.505, '#e0661e'), (0.525, '#e89040'), (0.56, '#4a2aa0'), (0.66, '#1c24a0'), (0.82, '#101078'), (1.0, '#08085a')]
SKY_DAY72 = [(0.0, '#2c52ee'), (0.40, '#4a86ff'), (0.5, '#a8d4ff'), (0.54, '#78b4ff'), (0.6, '#4690ff'), (0.7, '#2c6cf4'), (0.84, '#1c52e6'), (1.0, '#1444d8')]
MOUNT = [(3300, 160, 300, '#2a2894'), (4500, 320, 520, '#1e1e82')]
_E = F.LIGHTS['B_EVE']
F.LIGHTS['B_NIGHT'] = dict(_E, name='B_NIGHT', key=(1.55, 0.78, 0.38), key_dir=kdir(-52, 9), sun_elev=9, sun_angle=1.2, shade=(0.075, 0.085, 0.36), shade_tint=(0.07, 0.085, 0.40), lift=(0.006, 0.01, 0.03),
                           floods=1.7, crowd_k=1.0, sky=SKY_NIGHT, sky_k=1.2, glow=('#ff6a28', 0.82, 0.8), hills=MOUNT, hill_k=1.0, grade_saturation=1.22, grade_offset=(-0.004, -0.012, -0.02),
                           beam_k=1.0, windows=3.2, day=False, exposure=0.1, bloom_size=0.06)
F.LIGHTS['B_TENSE2'] = dict(F.LIGHTS['B_NIGHT'], name='B_TENSE2', key=(0.9, 0.42, 0.28), key_dir=kdir(-52, 7), sun_elev=7, shade=(0.055, 0.06, 0.30), shade_tint=(0.05, 0.06, 0.34), floods=2.6, crowd_k=0.42,
                            sky=SKY_TENSE, glow=('#e0561e', 0.85, 0.6), hills=[(3300, 160, 300, '#1e1c80'), (4500, 320, 520, '#16166a')], beam_k=1.15, windows=2.4, exposure=0.0)
F.LIGHTS['B_DAY72'] = dict(F.LIGHTS['B_DAY'], name='B_DAY72', exposure=0.0, key=(1.8, 1.62, 1.3), key_dir=kdir(-36, 46), sun_elev=46, shade=(0.14, 0.13, 0.46), shade_tint=(0.12, 0.12, 0.5), floods=0.0, sky=SKY_DAY72, sky_k=1.15,
                           glow=('#fff4d0', 0.7, 0.25), hills=[(3300, 120, 220, '#5a78e8'), (4500, 240, 400, '#4a66d8')], hill_k=1.0, grade_saturation=1.2, beam_k=0.0, windows=0.0, day=True, crowd_k=1.0)
for k in ('NIGHT', 'TENSE2', 'DAY72'):
    if k not in F.LOC_LIGHTS['B']: F.LOC_LIGHTS['B'].append(k)

# ------------------------------------------------------------------ generic mesh helpers
def _link(ob, cast=True, parent=True):
    STATE['SET'].objects.link(ob)
    if parent: ob.parent = root()
    L.T.no_bounce(ob)
    if not cast: ob.visible_shadow = False
    return ob

def mesh_obj(name, V, Fc, mt, uv=None, attrs=None, cast=False):
    me = bpy.data.meshes.new(name); me.from_pydata(np.asarray(V, dtype=float).tolist(), [], [list(map(int, f)) for f in Fc]); me.update()
    if uv is not None:
        ul = me.uv_layers.new(name='UVMap'); arr = np.asarray(uv, dtype=np.float32).reshape(-1)
        ul.data.foreach_set('uv', arr[:len(ul.data) * 2])
    for k, (typ, arr) in (attrs or {}).items():
        a = me.attributes.new(k, typ, 'POINT')
        if typ == 'FLOAT': a.data.foreach_set('value', np.asarray(arr, dtype=np.float32))
        else: a.data.foreach_set('vector', np.asarray(arr, dtype=np.float32).reshape(-1))
    me.materials.append(mt); ob = bpy.data.objects.new(name, me); return _link(ob, cast)

def boxes_obj(name, centres, sizes, yaws, mt, attrs=None, cast=False):
    centres = np.asarray(centres, dtype=float); sizes = np.asarray(sizes, dtype=float); yaws = np.asarray(yaws, dtype=float)
    V, Fc = LB.boxes(centres, sizes, yaws)
    at = {k: (t, np.repeat(np.asarray(a), 8, axis=0)) for k, (t, a) in (attrs or {}).items()}
    return mesh_obj(name, V, Fc, mt, attrs=at, cast=cast)

def quad_uv(p0, p1, p2, p3, u0=0.0, v0=0.0, u1=1.0, v1=1.0):
    """quad corners (metres) bl, br, tr, tl -> (V, face, uv)"""
    return [p0, p1, p2, p3], [0, 1, 2, 3], [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

def _tex_node(nt, png, ext='CLIP'):
    ti = nt.nodes.new('ShaderNodeTexImage'); ti.image = bpy.data.images.load(png, check_existing=True); ti.interpolation = 'Linear'; ti.extension = ext
    return ti

def mat_emit_tex(name, png, k=1.0, tint=(1, 1, 1)):
    key = 'E2|' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); ti = _tex_node(nt, png); em = N('ShaderNodeEmission'); em.inputs['Strength'].default_value = k
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0; mx.inputs[7].default_value = (*tint, 1.0)
    Lk(ti.outputs['Color'], mx.inputs[6]); Lk(mx.outputs[2], em.inputs['Color']); Lk(em.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def mat_lit_tex(name, png, gain=1.0, smix=0.35, ext='CLIP', shade_mul=1.0):
    """house-look lit material whose albedo is a painted texture (UV)."""
    key = '%s|T|%s' % (STATE['P']['name'], name)
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    ti = _tex_node(nt, png, ext); L._lit_tail(nt, ti.outputs['Color'], gain, shade_mul, smix, True, None); m.cycles.emission_sampling = 'NONE'
    m['lit'] = 1; m['gain'] = float(gain); m['sm'] = float(shade_mul); m['crowd'] = 0; m['mix'] = float(smix); S.MATS[key] = m; return m

def add_emission_to(m, color_socket_fn, strength_socket_fn):
    """add an emission term (built by the two callbacks on the material's node tree) to a lit material's surface"""
    nt = m.node_tree; out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]
    prev = out.inputs['Surface'].links[0].from_socket
    em = nt.nodes.new('ShaderNodeEmission'); ad = nt.nodes.new('ShaderNodeAddShader')
    nt.links.new(color_socket_fn(nt), em.inputs['Color']); nt.links.new(strength_socket_fn(nt), em.inputs['Strength'])
    nt.links.new(prev, ad.inputs[0]); nt.links.new(em.outputs[0], ad.inputs[1]); nt.links.new(ad.outputs[0], out.inputs['Surface'])

def _math(nt, op, a=None, b=None, c=None):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op
    for i, v in enumerate((a, b, c)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[i].default_value = v
        else: nt.links.new(v, n.inputs[i])
    return n.outputs[0]

# ------------------------------------------------------------------ materials of the city / beams / sparkles
def mat_city(name, day):
    key = '%s|city|%s' % (STATE['P']['name'], name)
    if key in S.MATS: return S.MATS[key]
    if day: m = mat('cityw_' + name, '#d8e4ff', '#f4d8b0', 0.035, contrast=0.6, smix=0.3)
    else: m = mat('cityw_' + name, '#3c46c8', '#6a3cb8', 0.03, contrast=0.6, smix=0.6)
    nt = m.node_tree; P = STATE['P']; K = float(P.get('windows', 3.0))
    def color(nt):
        tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs[0])
        u = _math(nt, 'ADD', sp.outputs['X'], sp.outputs['Y'])
        cu = _math(nt, 'FLOOR', _math(nt, 'DIVIDE', u, 3.3)); cz = _math(nt, 'FLOOR', _math(nt, 'DIVIDE', sp.outputs['Z'], 3.4))
        cb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(cu, cb.inputs['X']); nt.links.new(cz, cb.inputs['Y']); nt.links.new(_math(nt, 'FLOOR', _math(nt, 'DIVIDE', sp.outputs['X'], 29.0)), cb.inputs['Z'])
        wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(cb.outputs[0], wn.inputs['Vector'])
        cb2 = nt.nodes.new('ShaderNodeVectorMath'); cb2.operation = 'ADD'; nt.links.new(cb.outputs[0], cb2.inputs[0]); cb2.inputs[1].default_value = (11.3, 5.7, 3.1)
        wn2 = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn2.noise_dimensions = '3D'; nt.links.new(cb2.outputs[0], wn2.inputs['Vector'])
        mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = (1.0, 0.62, 0.18, 1.0); mx.inputs[7].default_value = (0.35, 0.8, 1.0, 1.0)
        nt.links.new(_math(nt, 'GREATER_THAN', wn2.outputs['Value'], 0.72), mx.inputs[0]); return mx.outputs[2]
    def strength(nt):
        tc = nt.nodes.new('ShaderNodeTexCoord'); sp = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(tc.outputs['Object'], sp.inputs[0])
        u = _math(nt, 'ADD', sp.outputs['X'], sp.outputs['Y']); fu = _math(nt, 'FRACT', _math(nt, 'DIVIDE', u, 3.3)); fz = _math(nt, 'FRACT', _math(nt, 'DIVIDE', sp.outputs['Z'], 3.4))
        cu = _math(nt, 'FLOOR', _math(nt, 'DIVIDE', u, 3.3)); cz = _math(nt, 'FLOOR', _math(nt, 'DIVIDE', sp.outputs['Z'], 3.4))
        cb = nt.nodes.new('ShaderNodeCombineXYZ'); nt.links.new(cu, cb.inputs['X']); nt.links.new(cz, cb.inputs['Y']); nt.links.new(_math(nt, 'FLOOR', _math(nt, 'DIVIDE', sp.outputs['X'], 29.0)), cb.inputs['Z'])
        wn = nt.nodes.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; nt.links.new(cb.outputs[0], wn.inputs['Vector'])
        rect = _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', _math(nt, 'GREATER_THAN', fu, 0.2), _math(nt, 'LESS_THAN', fu, 0.8)), _math(nt, 'MULTIPLY', _math(nt, 'GREATER_THAN', fz, 0.28), _math(nt, 'LESS_THAN', fz, 0.82)))
        lit = _math(nt, 'GREATER_THAN', wn.outputs['Value'], 0.5)
        geo = nt.nodes.new('ShaderNodeNewGeometry'); ns = nt.nodes.new('ShaderNodeSeparateXYZ'); nt.links.new(geo.outputs['True Normal'], ns.inputs[0])
        wall = _math(nt, 'LESS_THAN', _math(nt, 'ABSOLUTE', ns.outputs['Z']), 0.5)
        return _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', rect, lit), wall), K)
    if K > 0: add_emission_to(m, color, strength)
    S.MATS[key] = m; return m

def mat_beam(name, color=(1.0, 0.95, 0.82), k=2.2, power=2.2, gain=0.55, fade=0.6, blend=0.4):
    key = 'E3|' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = blend
    core = _math(nt, 'POWER', _math(nt, 'SUBTRACT', 1.0, lw.outputs['Facing']), power)
    tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['Generated'], sp.inputs[0])
    along = _math(nt, 'SUBTRACT', 1.0, _math(nt, 'MULTIPLY', sp.outputs['Z'], fade)); ramp = _math(nt, 'MINIMUM', _math(nt, 'MULTIPLY', sp.outputs['Z'], 12.0), 1.0)
    alpha = _math(nt, 'MINIMUM', _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', _math(nt, 'MULTIPLY', core, along), ramp), gain), 1.0)
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1.0); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); Lk(alpha, mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def mat_glow(name, color, k=3.0, power=3.0, gain=1.0):
    """soft spherical glow: alpha = (1 - facing)^power"""
    key = 'E4|' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    alpha = _math(nt, 'MINIMUM', _math(nt, 'MULTIPLY', _math(nt, 'POWER', _math(nt, 'SUBTRACT', 1.0, lw.outputs['Facing']), power), gain), 1.0)
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1.0); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); Lk(alpha, mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def mat_disc_glow(name, color, k=1.0, gain=1.0, power=2.0):
    """flat ground pool of light on a UV quad: alpha = (1 - r)^power"""
    key = 'E5|' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); uv = N('ShaderNodeUVMap'); vm = N('ShaderNodeVectorMath'); vm.operation = 'SUBTRACT'; Lk(uv.outputs[0], vm.inputs[0]); vm.inputs[1].default_value = (0.5, 0.5, 0.0)
    ln = N('ShaderNodeVectorMath'); ln.operation = 'LENGTH'; Lk(vm.outputs[0], ln.inputs[0])
    r = _math(nt, 'MULTIPLY', ln.outputs['Value'], 2.0); alpha = _math(nt, 'MULTIPLY', _math(nt, 'POWER', _math(nt, 'MAXIMUM', _math(nt, 'SUBTRACT', 1.0, r), 0.0), power), gain)
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*color, 1.0); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); Lk(alpha, mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def mat_sparkle(name, k=160.0, duty=0.05):
    """star flash bulbs: per-vertex 'seed' + frame-driven white noise, invisible when off"""
    key = 'E6|' + name
    if key in S.MATS: return S.MATS[key]
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); at = N('GeometryNodeInputNamedAttribute') if False else N('ShaderNodeAttribute'); at.attribute_name = 'seed'; at.attribute_type = 'GEOMETRY'
    tv = N('ShaderNodeValue'); tv.name = 'frame_v'
    tt = _math(nt, 'FLOOR', _math(nt, 'DIVIDE', _math(nt, 'ADD', tv.outputs[0], _math(nt, 'MULTIPLY', at.outputs['Fac'], 97.0)), 3.0))
    cb = N('ShaderNodeCombineXYZ'); Lk(at.outputs['Fac'], cb.inputs['X']); Lk(tt, cb.inputs['Y'])
    wn = N('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '3D'; Lk(cb.outputs[0], wn.inputs['Vector'])
    on = _math(nt, 'GREATER_THAN', wn.outputs['Value'], 1.0 - duty)
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (1.0, 0.97, 0.85, 1.0); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); Lk(on, mx.inputs[0]); Lk(tr.outputs[0], mx.inputs[1]); Lk(em.outputs[0], mx.inputs[2]); Lk(mx.outputs[0], out.inputs['Surface'])
    d = tv.outputs[0].driver_add('default_value').driver; d.type = 'SCRIPTED'; d.expression = 'frame'
    m.cycles.emission_sampling = 'NONE'; S.MATS[key] = m; return m

def swap_material(old_key_suffix, new_mat):
    """replace a material (by name suffix, e.g. 'tartanB') on every object of the scene"""
    n = 0
    for ob in bpy.data.objects:
        if ob.type != 'MESH': continue
        for i, s in enumerate(ob.material_slots):
            if s.material is not None and s.material.name.endswith('|' + old_key_suffix): s.material = new_mat; n += 1
    return n

# ------------------------------------------------------------------ the city
def _street_cars_and_lamps(rr, R, pitch, day, M):
    """cars (box + head/tail light boxes) and lamp pools along the grid streets"""
    car_c = []; car_s = []; car_y = []; car_k = []; hl_c = []; hl_s = []; hl_y = []; tl_c = []; tl_s = []; tl_y = []
    lamp_q = []
    n = int(R / pitch)
    for i in range(-n, n + 1):
        sx = i * pitch + pitch / 2                       # street at x = sx running along y
        for j in range(-n, n + 1):
            sy = SY + j * pitch + pitch / 2              # street at y = sy running along x
            for lamp in ((sx, SY + j * pitch + pitch / 2), ):
                pass
    # streets along y (x fixed) and along x (y fixed)
    for axis in (0, 1):
        for i in range(-n, n + 1):
            c0 = (i * pitch + pitch / 2) if axis == 0 else (SY + i * pitch + pitch / 2)
            t = -R
            while t < R:
                t += rr.uniform(14, 34)
                x, y = (c0, SY + t) if axis == 0 else (t, c0)
                if (x / (AO + 60)) ** 2 + ((y - SY) / (BO + 60)) ** 2 < 1: continue
                lane = rr.choice((-1, 1)); off = 3.3 * lane; yaw = (math.pi / 2 if axis == 0 else 0.0) + (0 if lane > 0 else math.pi)
                px, py = (x + off, y) if axis == 0 else (x, y + off)
                car_c.append((px, py, 0.8)); car_s.append((4.4, 1.9, 1.5) if axis else (4.4, 1.9, 1.5)); car_y.append(yaw); car_k.append(rr.randrange(5))
                d = Vector((math.cos(yaw), math.sin(yaw), 0)); lat = Vector((-d.y, d.x, 0))
                for sgn in (-1, 1):
                    pf = Vector((px, py, 0.9)) + d * 2.1 + lat * 0.65 * sgn; pb = Vector((px, py, 0.9)) - d * 2.1 + lat * 0.65 * sgn
                    hl_c.append(tuple(pf)); hl_s.append((0.5, 0.7, 0.55)); hl_y.append(yaw); tl_c.append(tuple(pb)); tl_s.append((0.4, 0.6, 0.5)); tl_y.append(yaw)
    return (car_c, car_s, car_y, car_k), (hl_c, hl_s, hl_y), (tl_c, tl_s, tl_y)

def build_city(P, M, day, extent=820.0, seed=68):
    rr = rnd(seed); pitch = 72.0; block = 54.0; n = int(extent / pitch)
    cm = mat_city('near', day); cm_far = mat_city('far', day)
    cen = []; siz = []; yaw = []; far_c = []; far_s = []; far_y = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            bx = i * pitch; by = SY + j * pitch
            if (bx / (AO + 62)) ** 2 + ((by - SY) / (BO + 62)) ** 2 < 1: continue
            if abs(bx) < 36 and by < SY: continue                       # the avenue
            dist = math.hypot(bx, by - SY)
            for lx in (-1, 1):
                for ly in (-1, 1):
                    if rr.random() < 0.06: continue
                    sx = rr.uniform(16, 24); sy = rr.uniform(16, 24); cx = bx + lx * 13.5 + rr.uniform(-1.5, 1.5); cy = by + ly * 13.5 + rr.uniform(-1.5, 1.5)
                    h = 7 + rr.expovariate(1 / 8.0) * (1.0 if dist < 350 else 1.5); h = min(h, 45.0)
                    if dist > 260 and rr.random() < 0.07: h = rr.uniform(55, 110); sx = sy = rr.uniform(14, 20)
                    h = max(h, 6.0)
                    cen.append((cx, cy, h / 2 - 0.05)); siz.append((sx, sy, h)); yaw.append(0.0)
    o1 = boxes_obj('city_near', cen, siz, yaw, cm, cast=False)
    far = 160.0; nf = int(2500 / far)
    for i in range(-nf, nf + 1):
        for j in range(-nf, nf + 1):
            bx = i * far; by = SY + j * far
            if abs(bx) < extent * 0.95 and abs(by - SY) < extent * 0.95: continue
            for k in range(2):
                sx = rr.uniform(40, 90); sy = rr.uniform(40, 90); h = 14 + rr.expovariate(1 / 14.0)
                if rr.random() < 0.08: h = rr.uniform(60, 150)
                far_c.append((bx + rr.uniform(-50, 50), by + rr.uniform(-50, 50), h / 2 - 0.05)); far_s.append((sx, sy, min(h, 160))); far_y.append(0.0)
    o2 = boxes_obj('city_far', far_c, far_s, far_y, cm_far, cast=False)
    # ground
    gm = mat('cityground', '#1c1a6a', '#2c2a86', 0.015, smix=0.7) if not day else mat('cityground', '#9aa4d8', '#aeb8e8', 0.015)
    me = bpy.data.meshes.new('cityground'); R_ = 9000; me.from_pydata([(-R_, -R_ + SY, -0.07), (R_, -R_ + SY, -0.07), (R_, R_ + SY, -0.07), (-R_, R_ + SY, -0.07)], [], [(0, 1, 2, 3)]); me.update(); me.materials.append(gm)
    g = bpy.data.objects.new('cityground', me); _link(g, cast=False)
    # plaza ring around the stadium + avenue
    mb = S.MB('plaza'); pm = mat('plaza', '#6a68c8', '#8480d8', 0.06, smix=0.4) if not day else mat('plaza', '#e6e2f4', '#d8d4ea', 0.06)
    S.ring(mb, pm, SX, SY, AO, BO, AO + 44, BO + 44, 0, 360, 0.0, 3.0)
    am = mat('avenue', '#26248a', '#34329c', 0.05, smix=0.6) if not day else mat('avenue', '#8890c8', '#9aa0d8', 0.05)
    mb.quad(am, [(-22, SY - BO - 40, 0.03), (22, SY - BO - 40, 0.03), (22, -2200, 0.03), (-22, -2200, 0.03)])
    wm = mat('avenue_edge', '#f2ecff', '#e0d8f8', 1.0)
    for sx in (-20.6, 20.6): mb.box(wm, (sx, (SY - BO - 40 - 2200) / 2, 0.05), (0.5, 2200 + BO + 40 - SY, 0.04))
    for k in range(60): mb.box(wm, (0, SY - BO - 55 - k * 28, 0.05), (0.6, 12, 0.04))
    L.fin(mb, cast=False)
    # cars, lamps (night only)
    if not day:
        (cc, cs, cy, ck), (hc, hs, hy), (tc, ts, ty) = _street_cars_and_lamps(rr, 700.0, pitch, day, M)
        carm = [mat('citycar%d' % i, h, h, 1.0) for i, h in enumerate(('#d8e4ff', '#e8203a', '#ffd21f', '#2f7bff', '#1c1a50'))]
        ck = np.array(ck)
        for i, cmt in enumerate(carm):
            idx = np.where(ck == i)[0]
            if len(idx): boxes_obj('citycars%d' % i, [cc[k] for k in idx], [cs[k] for k in idx], [cy[k] for k in idx], cmt, cast=False)
        boxes_obj('car_head', hc, hs, hy, mat_emit('car_head', '#fff2c8', 28.0), cast=False); boxes_obj('car_tail', tc, ts, ty, mat_emit('car_tail', '#ff3020', 14.0), cast=False)
        # ground pools of lamp light + lamp heads on the grid, avenue lamps (bigger)
        pv = []; pf = []; puv = []; lc = []; ls = []
        def pool(x, y, r):
            o = len(pv); pv.extend([(x - r, y - r, 0.06), (x + r, y - r, 0.06), (x + r, y + r, 0.06), (x - r, y + r, 0.06)]); pf.append([o, o + 1, o + 2, o + 3]); puv.extend([(0, 0), (1, 0), (1, 1), (0, 1)])
        nn = int(640 / pitch)
        for axis in (0, 1):
            for i in range(-nn, nn + 1):
                c0 = (i * pitch + pitch / 2) if axis == 0 else (SY + i * pitch + pitch / 2); t = -640.0
                while t < 640:
                    t += 38.0; x, y = (c0 + 7.5 * (1 if int(t) % 2 else -1), SY + t) if axis == 0 else (t, c0 + 7.5 * (1 if int(t) % 2 else -1))
                    if (x / (AO + 60)) ** 2 + ((y - SY) / (BO + 60)) ** 2 < 1: continue
                    pool(x, y, 8.0); lc.append((x, y, 8.0)); ls.append((1.0, 1.0, 0.7))
        for k in range(46):
            y = SY - BO - 50 - k * 30
            for sx in (-23, 23): pool(sx, y, 10.0); lc.append((sx, y, 9.0)); ls.append((1.3, 1.3, 0.9))
        mesh_obj('lamp_pools', pv, pf, mat_disc_glow('lamp_pool', (1.0, 0.7, 0.3), 1.0, 0.8, 2.2), uv=puv)
        boxes_obj('lamp_heads', lc, ls, [0.0] * len(lc), mat_emit('lamp_head', '#ffd890', 40.0), cast=False)
        # avenue banners: alternating red / white pennants on the avenue lamps
        bc = []; bs = []; bm_ = []
        for k in range(46):
            y = SY - BO - 50 - k * 30
            for sx in (-23, 23): bc.append((sx + (-1.1 if sx < 0 else 1.1), y, 6.3)); bs.append((0.12, 1.4, 4.0))
        boxes_obj('avenue_flags', bc, bs, [0.0] * len(bc), mat('avflag', '#ff3b2f', '#ff3b2f', 1.0), cast=False)
    return cen

def build_mountains(P, day):
    """volcano cone + the ridge ring (set15 L.ridges is already built from P['hills'], much larger than v1)"""
    key = 'volc|' + P['name']
    m = bpy.data.materials.new(key); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; Lk = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); Lk(tc.outputs['Generated'], sp.inputs[0])
    mr = N('ShaderNodeMapRange'); mr.inputs['From Min'].default_value = 0.8; mr.inputs['From Max'].default_value = 0.99; Lk(sp.outputs['Z'], mr.inputs['Value'])
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = S.hexc('#5a62d8' if day else '#2c2a98'); mx.inputs[7].default_value = S.hexc('#ffffff' if day else '#ff8a50'); Lk(mr.outputs['Result'], mx.inputs[0])
    Lk(mx.outputs[2], em.inputs['Color']); em.inputs['Strength'].default_value = 1.0; Lk(em.outputs[0], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    for (cx, cy, rad, h) in ((900, 3800, 1700, 520), (-1500, 3500, 1300, 400)):
        n = 28; V = [(cx + rad * math.cos(a) * (1 + 0.06 * math.sin(a * 5)), cy + rad * math.sin(a) * (1 + 0.06 * math.cos(a * 4)), 0) for a in [2 * math.pi * i / n for i in range(n)]]
        V += [(cx, cy, h)]; Fc = [(i, (i + 1) % n, n) for i in range(n)]
        mesh_obj('volcano', V, Fc, m, cast=False)

def build_rim(P, M, day):
    """outer-wall fins + lit concourse slots, rim LED ring, MEXICO 68 rim banners (front textured, back plain), roof glow"""
    fin_c = []; fin_s = []; fin_y = []; win_c = []; win_s = []; win_y = []; step = 3.0
    for k in range(int(360 / step)):
        u = math.radians(k * step); u2 = math.radians(k * step + step / 2); x, y = ell(AO + 0.4, BO + 0.4, u); nn = math.atan2(math.sin(u) / BO, math.cos(u) / AO)
        fin_c.append((x, y, (ZT + 1) / 2)); fin_s.append((0.9, 0.9, ZT + 1.2)); fin_y.append(nn + math.pi / 2)
        xw, yw = ell(AO + 0.2, BO + 0.2, u2); nw = math.atan2(math.sin(u2) / BO, math.cos(u2) / AO)
        for zc, hh in ((4.5, 5.0), (11.5, 5.0), (17.5, 3.6)):
            win_c.append((xw, yw, zc)); win_s.append((0.2, 1.9, hh)); win_y.append(nw + math.pi / 2)
    fm = mat('rimfin', '#2c34b8', '#3c3ccc', 0.4, smix=0.6) if not day else mat('rimfin', '#f4f0ff', '#e4e0f4', 0.4)
    boxes_obj('rim_fins', fin_c, fin_s, fin_y, fm, cast=True)
    boxes_obj('rim_slots', win_c, win_s, win_y, mat_emit('slot_warm', '#ffb050' if not day else '#7aa6ff', 5.5 if not day else 0.5), cast=False)
    # rim LED ring (white-warm) on the parapet and a red band below it
    lc = []; ls = []; ly = []
    for k in range(180):
        u = math.radians(k * 2 + 1); x, y = ell(AO + 0.25, BO + 0.25, u); nn = math.atan2(math.sin(u) / BO, math.cos(u) / AO)
        lc.append((x, y, ZT + 0.55)); ls.append((0.3, 3.6 * (AO / 89.2) + 0.1, 0.5)); ly.append(nn + math.pi / 2)
    boxes_obj('rim_led', lc, ls, ly, mat_emit('rim_led', '#fff0d0' if not day else '#ffffff', 9.0 if not day else 1.0), cast=False)
    # banners: inner face (textured, 4 colourways) + plain back
    bm = mat_emit_tex('banner68', os.path.join(TEXD, 'banner_mexico68.png'), 1.15 if not day else 1.0)
    backm = mat('banner_back', '#1c2488', '#2c34a0', 1.0)
    V = []; Fc = []; UV = []; bV = []; bF = []
    nb = 28
    for k in range(nb):
        uc = 360.0 / nb * (k + 0.5); wdeg = 360.0 / nb * 0.8; u0 = math.radians(uc - wdeg / 2); u1 = math.radians(uc + wdeg / 2)
        rr_ = 0.45; p0 = ell(AO - rr_, BO - rr_, u0); p1 = ell(AO - rr_, BO - rr_, u1); z0 = ZT + 0.2; z1 = ZT + 3.4
        stripe = k % 4; v0 = 1.0 - (stripe + 1) / 4.0; v1 = 1.0 - stripe / 4.0
        o = len(V); V += [(p0[0], p0[1], z0), (p1[0], p1[1], z0), (p1[0], p1[1], z1), (p0[0], p0[1], z1)]; Fc.append([o, o + 1, o + 2, o + 3]); UV += [(1, v0), (0, v0), (0, v1), (1, v1)]
        o = len(bV); q0 = ell(AO - rr_ + 0.12, BO - rr_ + 0.12, u0); q1 = ell(AO - rr_ + 0.12, BO - rr_ + 0.12, u1); bV += [(q0[0], q0[1], z0), (q1[0], q1[1], z0), (q1[0], q1[1], z1), (q0[0], q0[1], z1)]; bF.append([o, o + 1, o + 2, o + 3])
    mesh_obj('rim_banners', V, Fc, bm, uv=UV); mesh_obj('rim_banners_back', bV, bF, backm)
    # outer-wall hanging banners (vertical, 6 big ones over the fins)
    V = []; Fc = []; UV = []
    for k in range(18):
        uc = 20.0 * k + 10; w = math.radians(5.2); u0 = math.radians(uc) - w / 2; u1 = math.radians(uc) + w / 2; p0 = ell(AO + 0.9, BO + 0.9, u0); p1 = ell(AO + 0.9, BO + 0.9, u1)
        stripe = (k + 1) % 4; v0 = 1.0 - (stripe + 1) / 4.0; v1 = 1.0 - stripe / 4.0; z0 = 6.0; z1 = 17.0
        o = len(V); V += [(p0[0], p0[1], z0), (p1[0], p1[1], z0), (p1[0], p1[1], z1), (p0[0], p0[1], z1)]; Fc.append([o, o + 1, o + 2, o + 3])
        # rotated 90: the atlas text reads along the banner's height -> map u along z
        UV += [(0.02, v0), (0.02, v1), (0.98, v1), (0.98, v0)] if False else [(1, v0), (0, v0), (0, v1), (1, v1)]
    # (outer banners keep the horizontal strip, 11 m wide x 3.4 m high band on the wall)
    V = []; Fc = []; UV = []
    for k in range(18):
        uc = 20.0 * k + 10; w = math.radians(10.0); u0 = math.radians(uc) - w / 2; u1 = math.radians(uc) + w / 2; p0 = ell(AO + 0.95, BO + 0.95, u0); p1 = ell(AO + 0.95, BO + 0.95, u1)
        stripe = (k + 2) % 4; v0 = 1.0 - (stripe + 1) / 4.0; v1 = 1.0 - stripe / 4.0; z0 = 13.4; z1 = 17.0 + 0.0
        o = len(V); V += [(p1[0], p1[1], z0), (p0[0], p0[1], z0), (p0[0], p0[1], z1), (p1[0], p1[1], z1)]; Fc.append([o, o + 1, o + 2, o + 3]); UV += [(1, v0), (0, v0), (0, v1), (1, v1)]
    # note: with the winding above the front faces outwards; the texture is mirrored if viewed from inside (never seen)
    mesh_obj('outer_banners', V, Fc, mat_emit_tex('banner68o', os.path.join(TEXD, 'banner_mexico68.png'), 1.1 if not day else 1.0), uv=UV)

# ------------------------------------------------------------------ floodlights + beams
EXTRA_TOWERS = [200, 245, 295, 340]
def build_beams(P, M, day):
    if day: return
    kb = float(P.get('beam_k', 1.0)); bm = mat_beam('beam', (1.0, 0.95, 0.80), 1.6 * kb, 2.4, 0.20, 0.5, 0.45); glow = mat_glow('lamp_glow', (1.0, 0.92, 0.7), 4.0, 2.6, 1.0)
    tw = list(P['towers']) + EXTRA_TOWERS; H_ = 38.0
    mb = S.MB('flood2')
    for tdeg in EXTRA_TOWERS:                          # same tower as set15_b, for the 4 extra positions
        u = math.radians(tdeg); x, y = ell(AO + 9, BO + 9, u); n_ = (math.cos(u) / AO, math.sin(u) / BO); nn = math.hypot(*n_); nx, ny = n_[0] / nn, n_[1] / nn
        for sx, sy in ((-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)): mb.rod(M['steel'], (x + sx * 1.3, y + sy * 1.3, 0), (x + sx * 0.5, y + sy * 0.5, H_), 0.16, 0.1, 6)
        for hz in range(3, 38, 6): mb.rod(M['steel'], (x - 0.9, y - 0.9, hz), (x + 0.8, y + 0.8, hz), 0.05, 0.05, 4)
        yaw = math.atan2(-ny, -nx)
        mb.push(Matrix.Translation((x, y, H_ + 2.0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4())
        mb.box(M['dark'], (0, 0, 0), (0.5, 9.0, 5.6))
        for iy in range(7):
            for iz in range(4): mb.box(M['lamp'], (0.3, -3.9 + iy * 1.3, -2.1 + iz * 1.4), (0.12, 1.0, 1.0))
        mb.pop()
    L.fin(mb)
    tgt0 = Vector((0.0, 12.0, 0.0)); n = 28
    for tdeg in tw:
        u = math.radians(tdeg); x, y = ell(AO + 9, BO + 9, u); head = Vector((x, y, H_ + 2.0)); tgt = Vector((3.0 * math.cos(u) * 0.6, 12.0 + 2.0 * math.sin(u), 0.0))
        d = tgt - head; Ln = d.length * 1.12
        for off, r0, r1, k_ in ((0.0, 1.6, 10.0, 1.0), (0.0, 0.8, 4.5, 1.0)):
            V = [(r0 * math.cos(2 * math.pi * i / n), r0 * math.sin(2 * math.pi * i / n), 0.0) for i in range(n)] + [(r1 * math.cos(2 * math.pi * i / n), r1 * math.sin(2 * math.pi * i / n), Ln) for i in range(n)]
            Fc = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
            ob = mesh_obj('beam%d' % tdeg, V, Fc, bm); ob.location = head; ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); ob.visible_shadow = False
        # lamp flare
        me = bpy.data.meshes.new('flare'); mbm = S.MB('flare'); mbm.ell(glow, (0, 0, 0), (3.6, 3.6, 3.6), (14, 8)); o = L.fin(mbm, cast=False)[0]; o.location = head + Vector((0, 0, 0))
    # halo over the torch
    tx, ty, tz = STATE['torch_pos']
    gm = mat_glow('torch_glow', (1.0, 0.62, 0.2), 6.0, 2.4, 1.0); mbm = S.MB('torchglow'); mbm.ell(gm, (0, 0, 0), (11.0, 11.0, 14.0), (16, 10)); o = L.fin(mbm, cast=False)[0]; o.location = (tx, ty, tz - 1.0)
    gm2 = mat_glow('torch_glow2', (1.0, 0.85, 0.5), 8.0, 3.5, 1.0); mbm = S.MB('torchglow2'); mbm.ell(gm2, (0, 0, 0), (5.0, 5.0, 7.0), (14, 8)); o = L.fin(mbm, cast=False)[0]; o.location = (tx, ty, tz - 1.0)
    # vertical warm column above the torch (smoke-lit heat shaft)
    cm_ = mat_beam('torch_col', (1.0, 0.7, 0.3), 3.0, 2.0, 0.5, 0.8, 0.4)
    V = [(2.4 * math.cos(2 * math.pi * i / 20), 2.4 * math.sin(2 * math.pi * i / 20), 0.0) for i in range(20)] + [(7.0 * math.cos(2 * math.pi * i / 20), 7.0 * math.sin(2 * math.pi * i / 20), 55.0) for i in range(20)]
    Fc = [(i, (i + 1) % 20, 20 + (i + 1) % 20, 20 + i) for i in range(20)]; ob = mesh_obj('torch_col', V, Fc, cm_); ob.location = (tx, ty, tz - 1.0); ob.visible_shadow = False

def build_sparkles(P, day, n=3200):
    if day: return
    rr = rnd(777); c = []; s = []; y = []; sd = []
    for _ in range(n):
        i = rr.randrange(2, LB.NROW - 1); a = LB.A0 + i * LB.RW + 0.5; b = LB.B0 + i * LB.RW + 0.5; t = math.radians(rr.uniform(0, 360)); x_, y_ = ell(a, b, t); z = 1.0 + i * LB.RISE + 1.1
        yw = math.atan2(-math.sin(t) / b, -math.cos(t) / a) + math.pi; seed = rr.random(); sz = rr.uniform(0.5, 0.9)
        for dims in ((sz, sz, sz), (sz * 2.8, 0.08, 0.08), (0.08, 0.08, sz * 2.8)):
            c.append((x_, y_, z)); s.append(dims); y.append(yw); sd.append(seed)
    boxes_obj('sparkles', c, s, y, mat_sparkle('spark', 150.0, 0.045), attrs=dict(seed=('FLOAT', np.array(sd))), cast=False)

# ------------------------------------------------------------------ high jump area + signs
def build_jump_extras(P, M, day):
    # quilted foam mat top (never a blank slab) as a textured plane on the foam
    ft = mat_lit_tex('foamtop2', os.path.join(TEXD, 'foam_top.png'), 1.25, 0.35)
    px, py = PIT; w, h = 6.3, 5.3
    V, Fc, UV = quad_uv((px - w / 2, py - h / 2, FOAM_SURF), (px + w / 2, py - h / 2, FOAM_SURF), (px + w / 2, py + h / 2, FOAM_SURF), (px - w / 2, py + h / 2, FOAM_SURF))
    mesh_obj('foam_mat', V, [Fc], ft, uv=UV)
    # vivid sides instead of the grey-blue blocks
    fm = mat('foamB2', '#2c48d0', '#3a5ae0', 4, contrast=0.8, smix=0.3); fd = mat('foamdkB2', '#e02a2a', '#ee3a34', 4, smix=0.3)
    swap_material('foamB', fm); swap_material('foamdkB', fd)
    swap_material('foamtopB', ft)
    # thick red/white bar, brighter
    swap_material('barW', mat('barW2', '#ffffff', '#ffffff', rough=0.6, emit='#ffffff', emit_k=0.55)); swap_material('barR', mat('barR2', '#e8201a', '#e8201a', rough=0.6, emit='#ff3a20', emit_k=0.5))
    # tartan: hot red
    swap_material('tartanB', mat('tartanB2', '#d8321e', '#ee4a2a', 1.8, contrast=0.8, smix=0.3)); swap_material('tartan2', mat('tartan2b', '#e43a24', '#f85a34', 1.8, contrast=0.8, smix=0.3))
    swap_material('tartan3', mat('tartan3b', '#c82c1a', '#e04226', 1.8, contrast=0.8, smix=0.3))
    # bar-height board "2.24 m" on a post beside the right standard (faces the -y side = the approach camera)
    J = STATE['J']; bx = J['xc'] + J['half'] + 0.95; by = J['y'] - 0.5
    mb = S.MB('boardpost'); mb.rod(M['metal'], (bx - 0.55, by, 0), (bx - 0.55, by, 2.5), 0.03, 0.03, 8); mb.rod(M['metal'], (bx + 0.55, by, 0), (bx + 0.55, by, 2.5), 0.03, 0.03, 8)
    mb.box(M['steel'], (bx, by, 0.02), (1.5, 0.5, 0.04)); mb.box(M['dark'], (bx, by + 0.03, 2.05), (1.35, 0.06, 0.66)); L.fin(mb)
    bm = mat_emit_tex('board224', os.path.join(TEXD, 'board_224.png'), 1.3 if not day else 1.1)
    V, Fc, UV = quad_uv((bx - 0.65, by - 0.02, 1.75), (bx + 0.65, by - 0.02, 1.75), (bx + 0.65, by - 0.02, 2.33), (bx - 0.65, by - 0.02, 2.33)); mesh_obj('board224', V, [Fc], bm, uv=UV)
    STATE['board_224'] = (bx, by - 0.02, 2.04)
    # scoreboard HIGH JUMP overlay on the far-rim board (same transform as set15_b)
    u = math.radians(78); sbx, sby = ell(AO + 1.0, BO + 1.0, u); yaw = math.atan2(-math.sin(u) / BO, -math.cos(u) / AO) + math.pi / 2
    Mt = Matrix.Translation((sbx, sby, ZT + 5.0)) @ Euler((0, 0, yaw)).to_matrix().to_4x4()
    sm = mat_emit_tex('scoreboard', os.path.join(TEXD, 'scoreboard.png'), 1.5 if not day else 1.1)
    pts = [Mt @ Vector(p) for p in ((-7.6, -0.58, -2.9), (7.6, -0.58, -2.9), (7.6, -0.58, 2.9), (-7.6, -0.58, 2.9))]
    V, Fc, UV = quad_uv(*[tuple(p) for p in pts]); mesh_obj('scoreboard_hj', V, [Fc], sm, uv=UV)
    # 1972 banner (DAY72) on poles over the far stand
    if day:
        u = math.radians(104); bx2, by2 = ell(AO - 1.5, BO - 1.5, u); yw = math.atan2(-math.sin(u) / BO, -math.cos(u) / AO) + math.pi / 2
        Mt = Matrix.Translation((bx2, by2, ZT + 1.0)) @ Euler((0, 0, yw)).to_matrix().to_4x4()
        pts = [Mt @ Vector(p) for p in ((-14, -0.3, 6.0), (14, -0.3, 6.0), (14, -0.3, 20.0), (-14, -0.3, 20.0))]
        V, Fc, UV = quad_uv(*[tuple(p) for p in pts]); mesh_obj('banner1972', V, [Fc], mat_emit_tex('b1972', os.path.join(TEXD, 'banner_1972.png'), 1.0), uv=UV)
        mb = S.MB('b1972post')
        for sx in (-13.5, 0.0, 13.5): mb.rod(M['steel'], tuple(Mt @ Vector((sx, 0.2, 0.0))), tuple(Mt @ Vector((sx, 0.2, 20.0))), 0.25, 0.2, 8)
        L.fin(mb)

def build_podium_extras(P, M, day):
    """backdrop with MEXICO 68 behind the podium, step front colours; flower garland; spot light pool"""
    pxp, pyp = -9.0, 10.0
    bm = mat_emit_tex('pback', os.path.join(TEXD, 'podium_back.png'), 1.2 if not day else 1.0)
    V, Fc, UV = quad_uv((pxp - 3.6, pyp + 1.4, 0.2), (pxp + 3.6, pyp + 1.4, 0.2), (pxp + 3.6, pyp + 1.4, 3.6), (pxp - 3.6, pyp + 1.4, 3.6)); mesh_obj('podium_back', V, [Fc], bm, uv=UV)
    mb = S.MB('podium_back_f'); mb.rod(M['steel'], (pxp - 3.6, pyp + 1.35, 0), (pxp - 3.6, pyp + 1.35, 3.7), 0.05, 0.05, 6); mb.rod(M['steel'], (pxp + 3.6, pyp + 1.35, 0), (pxp + 3.6, pyp + 1.35, 3.7), 0.05, 0.05, 6); L.fin(mb)
    swap_material('podium', mat('podium_g', '#fff0c0', '#ffe49a', 2, smix=0.2)); swap_material('podium2', mat('podium2_r', '#e02a2a', '#f04a3a', 2, smix=0.2))
    if not day:
        sp = bpy.data.lights.new('podium_spot', 'SPOT'); sp.color = (1.0, 0.92, 0.75); sp.energy = 1.6e4; sp.spot_size = math.radians(34); sp.spot_blend = 0.6; sp.use_shadow = False
        so = bpy.data.objects.new('podium_spot', sp); STATE['LIGHTS'].objects.link(so); so.parent = root(); so.location = (pxp + 6.0, pyp - 14.0, 12.0)
        so.rotation_euler = (Vector((pxp, pyp, 0.6)) - Vector((pxp + 6.0, pyp - 14.0, 12.0))).to_track_quat('-Z', 'Y').to_euler()

def hide_3d_crowd(center_m, radius_m, zspan=(-2.0, 9.0)):
    """move every 3D crowd figure within radius (m, horizontal) of center_m below the floor (cards take over there). Returns the count."""
    cx, cy, cz = center_m; n = 0
    for ob in STATE.get('crowd_objs', []):
        me = ob.data; co = np.empty(len(me.vertices) * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 8, 3)
        ctr = co.mean(1); m = (np.hypot(ctr[:, 0] - cx, ctr[:, 1] - cy) < radius_m) & (ctr[:, 2] > cz + zspan[0]) & (ctr[:, 2] < cz + zspan[1])
        if m.any():
            co[m, :, 2] -= 400.0; me.vertices.foreach_set('co', co.reshape(-1)); me.update(); n += int(m.sum())
    return n

# ------------------------------------------------------------------ surfaces (analytic) used by the grounding helpers
def stand_pos(row, u_deg, back=0.5):
    """seat point (x, y, z) in metres of stand row `row` at ellipse parameter u_deg; also returns the facing yaw toward the pitch centre"""
    a = LB.A0 + row * LB.RW + back; b = LB.B0 + row * LB.RW + back; t = math.radians(u_deg); x, y = ell(a, b, t)
    return (x, y, 1.0 + row * LB.RISE)

def surface_z(x_m, y_m):
    """height (m) of the walkable / sit-able surface under a metre xy point: foam mat top, podium steps, stand treads, else track 0.012"""
    px, py = PIT
    if abs(x_m - px) < 3.1 and abs(y_m - py) < 2.6: return FOAM_SURF
    pxp, pyp = -9.0, 10.0
    for dx, hh, wd in ((-0.95, 0.55, 0.9), (0.0, 0.85, 1.0), (0.95, 0.35, 0.9)):
        if abs(x_m - (pxp + dx)) < wd / 2 and abs(y_m - pyp) < 0.45: return hh + 0.025
    r = math.sqrt(((x_m - SX) / 1.0) ** 2 + 0.0)
    # ellipse radius parameter: solve for the row from the normalised radius
    k = math.hypot((x_m - SX) / LB.A0, (y_m - SY) / LB.B0)
    for i in range(LB.NROW):
        a = LB.A0 + i * LB.RW; b = LB.B0 + i * LB.RW; a2 = a + LB.RW; b2 = b + LB.RW
        v1 = math.hypot((x_m - SX) / a, (y_m - SY) / b); v2 = math.hypot((x_m - SX) / a2, (y_m - SY) / b2)
        if v1 >= 1.0 and v2 < 1.0: return 1.0 + i * LB.RISE
    return 0.012

# ------------------------------------------------------------------ build
def build(light='NIGHT', city=True, sparkles=True, dress=True, extent=820.0):
    """F.build('B', light) + the v2 extras. light = 'NIGHT' | 'TENSE' | 'DAY72' (| the set15 names EVE / DAY / TENSE keep v1 look)."""
    lk = {'TENSE': 'TENSE2'}.get(light, light)
    A = F.build('B', lk, dress=dress); P = STATE['P']; M = STATE['M']; day = bool(P.get('day', False)); sc = bpy.context.scene
    STATE['v2'] = dict(light=light, day=day)
    lawn = bpy.data.objects.get('lawn')
    if lawn is not None and lk in ('NIGHT', 'TENSE2', 'DAY72'): lawn.scale = (0.28, 0.28, 1.0)
    if lk in ('NIGHT', 'TENSE2', 'DAY72'):
        build_rim(P, M, day); build_jump_extras(P, M, day); build_podium_extras(P, M, day); build_mountains(P, day)
        if city: build_city(P, M, day, extent)
        build_beams(P, M, day)
        if sparkles: build_sparkles(P, day)
    cam = bpy.context.scene.camera
    for ob in bpy.data.cameras: ob.clip_end = 20000.0
    return A

def make_camera_m(loc_m, look_m, lens=22.0, roll=0.0, name='cam'):
    """camera from metre coordinates (the v2 convention for far views); far clip 20 km"""
    ob = F.make_camera(F.cam_from(M2D(loc_m), M2D(look_m), lens=lens, roll=roll), name); ob.data.clip_end = 20000.0; ob.data.clip_start = 0.1; return ob
