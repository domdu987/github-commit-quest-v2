#!/usr/bin/env python3
"""beach3d.py : a 1938 Long Island beach colony as a real 3D Blender set (bpy 5.3, Cycles CPU), clip A exterior treatment.

    import beach3d as B
    A = B.build("GREY_DRIZZLE")                 # | "STORM" | "SUMMER_SUN"  -> anchors (API.md section 2)
    cam = B.make_camera(A["cams"]["eye_beach"])
    B.set_fog_bank(0.4, frame=1); B.set_wave(0.0, frame=1); B.set_wave(1.0, frame=90)
    B.set_rain(0.6); B.set_sea(0.0, frame=1); B.set_sea(3.0, frame=90); B.set_wind(0.3)

World: 1 unit = 1 D, Z up, sand z = 0 where actors stand, the sea lies toward +y (shoreline y = SHORE_Y), the cottage row runs along x.
CLI:   python3 beach3d.py stills [final|preview] | timing | review <outdir>
Reuses v3/set3d/office3d.py (mesh builder, ink, camera, render settings, grade) and v3/stage (actor cards) by import."""
import os, sys, math, json, time, random
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(PROJ, 'v3', 'set3d')); sys.path.insert(0, os.path.join(PROJ, 'v3'))
import office3d as S                                       # noqa: E402  (MB, make_camera, setup_render, setup_grade, no_bounce, mat_ink, hex_lin)
import beach_tex as BT                                     # noqa: E402
TMP = os.path.join(PROJ, 'v3', 'tmp', 'beach')

SHORE_Y = 14.0             # still-water line; sea for y > SHORE_Y
SEA_Z = -0.12
FOG_R = 300.0              # radius of the fog-bank ring (from the origin)
WAVE = dict(y_near=SHORE_Y + 3.0, travel=420.0, h_far=9.0, h_near=17.0)
COS_MIN = 0.12

# ----------------------------------------------------------------------------- presets (scene-linear; colours are albedo / display hex)
PRESETS = {
    # clip A noon: hard sun 44 deg, sand shade #605e6e-like blue-violet (A from the spec's per-channel shadow ratio), pale-surface ambient
    'SUMMER_SUN': dict(
        A=(0.10, 0.25, 0.98), A_pale=(0.21, 0.25, 0.51), K=(0.92, 0.80, 0.24), key_dir=(0.55, -0.45, -0.70), sun_angle=1.0,
        shade_tint=(0.22, 0.20, 0.38), shade_mix=0.5, grade_sat=1.04,
        lift=(0.008, 0.010, 0.026), form=(0.05, -0.05, 0.16), obj_sat=1.0,
        sky=[(0.0, '#a9c6ec'), (0.12, '#8ab1ea'), (0.45, '#6898e0'), (1.0, '#4a78cd')], sky_span=0.75,
        cloud=dict(lo='#b7c2ea', hi='#f4f3fb', cover=0.5, soft=0.12, opacity=0.92, scale=0.7), glow=None,
        haze='#a6c2ec', haze_max=0.62, haze_d=(25.0, 420.0),
        sand=('#d47844', '#de8e50', '#e8a462'), wet='#b6765c', sand_far=('#dc7c64', '#e6a28a'),
        sea_near='#3559b0', sea_far='#6f9fe6', sea_band='#b9d3ee', streak='#dfe8fb', streak_amt=0.28, foam='#f4f1fb',
        fog='#d2ccd2', fog_foot='#b9b6c6', fog_alpha=0.95, ink='#2a1712', headland=('#8d78b0', '#7393d0'),
        wave=[(0.0, '#15285e'), (0.30, '#1f4f98'), (0.62, '#2f72b8'), (0.80, '#4d97cc'), (0.88, '#8cc2e2'), (0.93, '#d6ecf6'), (0.97, '#f4f8fe')],
        wave_lite='#7fb4e0', wave_emit=0.62, wave_gain=0.30, foam_shade='#b3c3e6'),
    # the false defeat: a dull grey-blue morning, flat soft light, wet darker sand, everything a little desaturated (judgement, no reference)
    'GREY_DRIZZLE': dict(
        A=(0.54, 0.555, 0.68), A_pale=(0.52, 0.54, 0.67), K=(0.16, 0.16, 0.17), key_dir=(0.25, -0.35, -0.90), sun_angle=14.0,
        shade_tint=(0.50, 0.52, 0.70), shade_mix=0.35, grade_sat=1.16,
        lift=(0.010, 0.013, 0.030), form=(0.04, -0.04, 0.16), obj_sat=0.92,
        sky=[(0.0, '#c0c6da'), (0.15, '#aab3cc'), (0.55, '#8c96b6'), (1.0, '#6f7ba0')], sky_span=0.7,
        cloud=dict(lo='#8c91ad', hi='#c2c4d4', cover=0.75, soft=0.30, opacity=0.55, scale=0.35), glow=None,
        haze='#b8bccf', haze_max=0.80, haze_d=(14.0, 220.0),
        sand=('#b8875a', '#c29264', '#cba070'), wet='#8e6e58', sand_far=('#a98878', '#b5a39a'),
        sea_near='#4c5c80', sea_far='#7d87a8', sea_band='#c3c5d6', streak='#b9bfd3', streak_amt=0.30, foam='#d9dbe6',
        fog='#dcdee6', fog_foot='#b6bacb', fog_alpha=0.97, ink='#2a1d2c', headland=('#9a93b0', '#a3a9c4'),
        wave=[(0.0, '#1f2e55'), (0.32, '#334f86'), (0.64, '#4a6e9e'), (0.80, '#6b8fb6'), (0.88, '#9db8d0'), (0.94, '#e2e8f0')],
        wave_lite='#8fa9c8', wave_emit=0.70, wave_gain=1.2, foam_shade='#a9b1c8'),
    # the arrival: dark slate sky, a low hard warm light breaking under the cloud from +x on the land side (edge-lights the cottages and the wave face)
    'STORM': dict(
        A=(0.06, 0.09, 0.24), A_pale=(0.09, 0.115, 0.26), K=(1.75, 1.08, 0.48), key_dir=(-0.80, 0.48, -0.22), sun_angle=0.8, toon=False,
        shade_tint=(0.08, 0.10, 0.25), shade_mix=0.5, grade_sat=1.08,
        lift=(0.006, 0.010, 0.028), form=(0.06, -0.04, 0.22), obj_sat=0.92,
        sky=[(0.0, '#6672aa'), (0.12, '#43508c'), (0.45, '#27326a'), (1.0, '#0f1534')], sky_span=0.65,
        cloud=dict(lo='#1f2a52', hi='#55628f', cover=0.62, soft=0.16, opacity=0.95, scale=0.45), glow=('#e8a070', 0.35, 40.0),
        haze='#4e5a8e', haze_max=0.55, haze_d=(18.0, 300.0),
        sand=('#9c6a52', '#a6745a', '#b08062'), wet='#6e5458', sand_far=('#7c6478', '#5c6290'),
        sea_near='#102766', sea_far='#2a4890', sea_band='#7684b8', streak='#dfe6fa', streak_amt=0.75, foam='#e6e8f8',
        fog='#8890b4', fog_foot='#5d6690', fog_alpha=0.97, ink='#1d1449', headland=('#454c84', '#525ea0'),
        wave=[(0.0, '#08122e'), (0.30, '#0f2f5e'), (0.60, '#17507f'), (0.78, '#236f9c'), (0.87, '#4d9cc0'), (0.925, '#b7dcea'), (0.965, '#eef6fb')],
        wave_lite='#3f86b0', wave_emit=0.78, wave_gain=0.16, foam_shade='#8d9cc4', foam_emit=1.0),
}
STATE = {}

def lin(h): return S.hex_lin(h)
def _sat(h):
    c = [int(h.lstrip('#')[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]; mx, mn = max(c), min(c)
    return 0.0 if mx == 0 else (mx - mn) / mx

# ----------------------------------------------------------------------------- node helper
class NB(object):
    def __init__(s, nt): s.nt = nt; s.L = nt.links.new
    def n(s, kind, **kw):
        x = s.nt.nodes.new(kind)
        for k, v in kw.items(): setattr(x, k, v)
        return x
    def _in(s, sock, v):
        if v is None: return
        if isinstance(v, (int, float)): sock.default_value = v
        elif isinstance(v, str): s.L(s.rgb(v), sock)
        elif isinstance(v, tuple): sock.default_value = v
        else: s.L(v, sock)
    def math(s, op, a, b=None, c=None, clamp=False):
        x = s.n('ShaderNodeMath', operation=op); x.use_clamp = clamp; s._in(x.inputs[0], a); s._in(x.inputs[1], b); s._in(x.inputs[2], c); return x.outputs[0]
    def vmath(s, op, a, b=None, scale=None):
        x = s.n('ShaderNodeVectorMath', operation=op); s._in(x.inputs[0], a); s._in(x.inputs[1], b)
        if scale is not None: s._in(x.inputs['Scale'], scale)
        return x.outputs['Value'] if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE') else x.outputs['Vector']
    def sep(s, v): x = s.n('ShaderNodeSeparateXYZ'); s._in(x.inputs[0], v); return x.outputs[0], x.outputs[1], x.outputs[2]
    def comb(s, a, b, c): x = s.n('ShaderNodeCombineXYZ'); s._in(x.inputs[0], a); s._in(x.inputs[1], b); s._in(x.inputs[2], c); return x.outputs[0]
    def rgb(s, h): x = s.n('ShaderNodeRGB'); x.outputs[0].default_value = (*lin(h), 1.0); return x.outputs[0]
    def mix(s, fac, a, b, blend='MIX'):
        x = s.n('ShaderNodeMix'); x.data_type = 'RGBA'; x.blend_type = blend; x.clamp_factor = True
        s._in(x.inputs[0], fac)
        for sock, v in ((x.inputs[6], a), (x.inputs[7], b)):
            if isinstance(v, str): sock.default_value = (*lin(v), 1.0)
            elif isinstance(v, tuple): sock.default_value = (*v[:3], 1.0)
            else: s.L(v, sock)
        return x.outputs[2]
    def ramp(s, fac, stops, interp='LINEAR'):
        x = s.n('ShaderNodeValToRGB'); cr = x.color_ramp; cr.interpolation = interp; s._in(x.inputs[0], fac)
        el = cr.elements
        while len(el) > 1: el.remove(el[-1])
        el[0].position = stops[0][0]; el[0].color = (*lin(stops[0][1]), 1.0) if isinstance(stops[0][1], str) else stops[0][1]
        for p, c in stops[1:]:
            e = el.new(p); e.color = (*lin(c), 1.0) if isinstance(c, str) else c
        return x.outputs['Color'], x.outputs['Alpha']
    def mrange(s, v, a, b, c=0.0, d=1.0, clamp=True, interp='LINEAR'):
        x = s.n('ShaderNodeMapRange'); x.clamp = clamp; x.interpolation_type = interp; s._in(x.inputs['Value'], v)
        x.inputs['From Min'].default_value = a; x.inputs['From Max'].default_value = b; x.inputs['To Min'].default_value = c; x.inputs['To Max'].default_value = d
        return x.outputs['Result']
    def noise(s, vec, scale, detail=2.0, rough=0.5, dist=0.0, dims='3D'):
        x = s.n('ShaderNodeTexNoise'); x.noise_dimensions = dims; s._in(x.inputs['Vector'], vec)
        x.inputs['Scale'].default_value = scale; x.inputs['Detail'].default_value = detail; x.inputs['Roughness'].default_value = rough; x.inputs['Distortion'].default_value = dist
        return x.outputs['Fac']
    def wave(s, vec, scale, dist, detail=2.0, direction='Y', phase=None):
        x = s.n('ShaderNodeTexWave'); x.wave_type = 'BANDS'; x.bands_direction = direction; s._in(x.inputs['Vector'], vec)
        x.inputs['Scale'].default_value = scale; x.inputs['Distortion'].default_value = dist; x.inputs['Detail'].default_value = detail
        if phase is not None: s._in(x.inputs['Phase Offset'], phase)
        return x.outputs['Fac']
    def ctl(s, prop, expr=None):
        """Value node driven by a custom property of the control object (beach_ctl)."""
        x = s.n('ShaderNodeValue'); x.outputs[0].default_value = float(STATE['ctl'][prop]); _drive(x.outputs[0], 'default_value', expr or prop, [prop]); return x.outputs[0]

def _drive(owner, path, expr, props, index=-1):
    fc = owner.driver_add(path) if index < 0 else owner.driver_add(path, index)
    d = fc.driver; d.type = 'SCRIPTED'; d.expression = expr
    for p in props:
        v = d.variables.new(); v.name = p; v.type = 'SINGLE_PROP'; t = v.targets[0]; t.id_type = 'OBJECT'; t.id = STATE['ctl']; t.data_path = '["%s"]' % p
    return fc

def _tree(m):
    nt = m.node_tree
    for x in list(nt.nodes): nt.nodes.remove(x)
    return nt

def _newmat(name):
    m = bpy.data.materials.get(name)
    if m is not None: bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name); m.cycles.emission_sampling = 'NONE'; return m

def _img(path):
    im = bpy.data.images.load(path, check_existing=True)
    if path not in STATE.setdefault('imgs', set()): im.reload(); STATE['imgs'].add(path)
    return im

def _haze(nb, shader, amount=1.0, color=None, d=None, hmax=None):
    """aerial perspective: mix toward the haze colour with the view distance (camera rays)."""
    P = STATE['P']; d0, d1 = d or P['haze_d']; cd = nb.n('ShaderNodeCameraData')
    f = nb.math('POWER', nb.mrange(cd.outputs['View Distance'], d0, d1), 0.75)
    f = nb.math('MULTIPLY', f, (hmax if hmax is not None else P['haze_max']) * amount)
    em = nb.n('ShaderNodeEmission'); nb._in(em.inputs['Color'], color or P['haze'])
    mx = nb.n('ShaderNodeMixShader'); nb.L(f, mx.inputs['Fac']); nb.L(shader, mx.inputs[1]); nb.L(em.outputs[0], mx.inputs[2])
    return mx.outputs[0]

def mat_lit(name, color='#808080', image=None, proc=None, pale=None, gain=1.0, shade_mul=1.0, alpha=False, haze=1.0, toon=True, form=True, sat=True):
    """Environment surface (office model): Diffuse(art x gain / cos to the sun) lit by the one key + Emission(art x A x F + LIFT), then haze.
    A is the saturated or the pale-surface ambient (LOOK_SPEC 3.3: albedo saturation under 0.25 takes the pale one)."""
    full = 'BEACH_' + name
    if full in bpy.data.materials: return bpy.data.materials[full]
    P = STATE['P']; m = _newmat(full); nt = _tree(m); nb = NB(nt)
    out = nb.n('ShaderNodeOutputMaterial'); geo = nb.n('ShaderNodeNewGeometry'); tex = None
    if proc is not None: c = proc(nb)
    elif image is not None:
        tex = nb.n('ShaderNodeTexImage'); tex.image = _img(image); tex.interpolation = 'Linear'; c = tex.outputs['Color']
    else: c = nb.rgb(color)
    if pale is None: pale = (color is not None and image is None and proc is None and _sat(color) < 0.25)
    if sat and abs(P['obj_sat'] - 1.0) > 1e-3:
        hs = nb.n('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = P['obj_sat']; nb.L(c, hs.inputs['Color']); c = hs.outputs['Color']
    A = P['A_pale'] if pale else P['A']; kd = Vector(P['key_dir']).normalized()
    dif = nb.n('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 0.0
    if toon and P.get('toon', True):
        cs = nb.math('MAXIMUM', nb.vmath('DOT_PRODUCT', geo.outputs['Normal'], tuple(-kd)), COS_MIN)
        nb.L(nb.vmath('SCALE', c, scale=nb.math('DIVIDE', gain, cs)), dif.inputs['Color'])
    else: nb.L(nb.vmath('SCALE', c, scale=gain), dif.inputs['Color'])
    amb = nb.mix(1.0, c, tuple(a * shade_mul for a in A), blend='MULTIPLY')
    if P.get('shade_mix', 0.0) > 0:                          # pull every shade toward one blue-violet hue (240-260), keep some local colour
        bw = nb.n('ShaderNodeRGBToBW'); nb.L(c, bw.inputs[0])
        tint = nb.vmath('SCALE', tuple(t * shade_mul for t in P['shade_tint']), scale=bw.outputs[0])
        amb = nb.mix(P['shade_mix'], amb, tint)
    amb = nb.vmath('ADD', amb, tuple(P['lift']))
    if form:
        fa = nb.math('ADD', nb.vmath('DOT_PRODUCT', geo.outputs['Normal'], tuple(P['form'])), 1.0)
        amb = nb.vmath('SCALE', amb, scale=fa)
    em = nb.n('ShaderNodeEmission'); nb.L(amb, em.inputs['Color'])
    add = nb.n('ShaderNodeAddShader'); nb.L(dif.outputs[0], add.inputs[0]); nb.L(em.outputs[0], add.inputs[1]); last = add.outputs[0]
    if haze: last = _haze(nb, last, haze)
    if alpha and tex is not None:
        tr = nb.n('ShaderNodeBsdfTransparent'); mx = nb.n('ShaderNodeMixShader'); nb.L(tex.outputs['Alpha'], mx.inputs['Fac']); nb.L(tr.outputs[0], mx.inputs[1]); nb.L(last, mx.inputs[2]); last = mx.outputs[0]
    nb.L(last, out.inputs['Surface'])
    return m

def mat_unlit(name, color, strength=1.0, alpha_fn=None, haze=0.0, camera_only=True, color_fn=None):
    """Painted surface (emission). alpha_fn(nb) -> socket for a soft cut-out."""
    full = 'BEACH_' + name
    if full in bpy.data.materials: return bpy.data.materials[full]
    m = _newmat(full); nt = _tree(m); nb = NB(nt); out = nb.n('ShaderNodeOutputMaterial')
    em = nb.n('ShaderNodeEmission'); em.inputs['Strength'].default_value = strength
    if color_fn is not None: nb.L(color_fn(nb), em.inputs['Color'])
    else: nb._in(em.inputs['Color'], color if not isinstance(color, str) else nb.rgb(color))
    last = em.outputs[0]
    if haze: last = _haze(nb, last, haze)
    if alpha_fn is not None or camera_only:
        a = alpha_fn(nb) if alpha_fn is not None else 1.0
        if camera_only:
            lp = nb.n('ShaderNodeLightPath'); a = nb.math('MULTIPLY', a, lp.outputs['Is Camera Ray'])
        tr = nb.n('ShaderNodeBsdfTransparent'); mx = nb.n('ShaderNodeMixShader'); nb._in(mx.inputs['Fac'], a); nb.L(tr.outputs[0], mx.inputs[1]); nb.L(last, mx.inputs[2]); last = mx.outputs[0]
    nb.L(last, out.inputs['Surface'])
    return m

def ink_mat():
    return S.mat_ink('BEACH_ink', STATE['P']['ink'])

def add_hull(ob, thickness):
    ob.data.materials.append(ink_mat())
    mod = ob.modifiers.new('ink_hull', 'SOLIDIFY'); mod.thickness = thickness; mod.offset = 1.0; mod.use_flip_normals = True
    mod.use_rim = False; mod.material_offset = len(ob.data.materials) - 1; mod.use_even_offset = True
    return mod

def hull_for(p, ref=(1.0, 8.0, 2.0)):
    """3 px ink at the distance of the main shots (0.00384 x distance), clamped."""
    d = (Vector(p) - Vector(ref)).length; return max(0.014, min(0.07, 0.00384 * max(4.0, d)))

def _obj(mb, name, coll, hull=0.0, shadow=True):
    ob = mb.obj(name, coll)
    if hull > 0: add_hull(ob, hull)
    ob.visible_shadow = shadow; S.no_bounce(ob); STATE['objects'][name] = ob
    return ob

# ----------------------------------------------------------------------------- world sky (camera rays only)
def build_world(scene):
    P = STATE['P']; w = bpy.data.worlds.get('W_beach') or bpy.data.worlds.new('W_beach'); scene.world = w; nt = _tree(w); nb = NB(nt)
    try: w.cycles.sampling_method = 'NONE'
    except Exception: pass
    for k in ('diffuse', 'glossy', 'transmission', 'scatter'):            # the sky only exists for camera rays (no shader cost on bounce rays)
        if hasattr(w.cycles_visibility, k): setattr(w.cycles_visibility, k, False)
    tc = nb.n('ShaderNodeTexCoord'); d = nb.vmath('NORMALIZE', tc.outputs['Generated']); dx, dy, dz = nb.sep(d)
    t = nb.mrange(dz, 0.0, P['sky_span'])
    sky, _ = nb.ramp(t, P['sky'])
    # clouds on a sky plane: (x / z, y / z) perspective, stretched along x, faded toward the horizon
    C = P['cloud']; ez = nb.math('MAXIMUM', dz, 0.02)
    u = nb.math('DIVIDE', dx, ez); v = nb.math('DIVIDE', dy, ez)
    vec = nb.comb(nb.math('MULTIPLY', u, 0.30), nb.math('MULTIPLY', v, 0.55), 3.7)
    nz = nb.noise(vec, C['scale'], detail=2.5, rough=0.45, dist=0.2)
    lo = 1.0 - C['cover']; dens = nb.mrange(nz, lo, lo + C['soft'])
    fade = nb.mrange(dz, 0.03, 0.16)
    dens = nb.math('MULTIPLY', nb.math('MULTIPLY', dens, fade), C['opacity'])
    nz2 = nb.noise(nb.vmath('ADD', vec, (0.0, -0.06, 0.0)), C['scale'], detail=2.5, rough=0.45, dist=0.2)    # lighter tops: sample a little further toward the zenith
    top = nb.mrange(nb.math('SUBTRACT', nz, nz2), -0.04, 0.05)
    ccol = nb.mix(top, C['lo'], C['hi'])
    col = nb.mix(dens, sky, ccol)
    if P.get('glow'):
        gh, gs, gp = P['glow']; kd = Vector(P['key_dir']).normalized()
        g = nb.math('POWER', nb.math('MAXIMUM', nb.vmath('DOT_PRODUCT', d, tuple(-kd)), 0.0), gp)
        g = nb.math('MULTIPLY', nb.math('MULTIPLY', g, gs), nb.mrange(dz, 0.25, 0.0)); col = nb.mix(g, col, gh)
    lp = nb.n('ShaderNodeLightPath'); col = nb.mix(lp.outputs['Is Camera Ray'], (0.0, 0.0, 0.0), col)
    bg = nb.n('ShaderNodeBackground'); nb.L(col, bg.inputs['Color']); bg.inputs['Strength'].default_value = 1.0
    wo = nb.n('ShaderNodeOutputWorld'); nb.L(bg.outputs[0], wo.inputs['Surface'])
    return w

# ----------------------------------------------------------------------------- terrain
def ground_z(x, y):
    """height of the sand (D). Flat (0) from the road (y = -12) to y = SHORE_Y - 1.8 (so the surf marks at y 11.6 / 11.9 stand on z = 0);
    dunes inland; slope 1:15 to the still-water line (z = SEA_Z at SHORE_Y) and on under the sea.
    (review fix: the old slope started at y = 10, so actors at surf_a / surf_b floated 0.05 D above the sand.)"""
    if y > SHORE_Y - 1.8: return -(y - (SHORE_Y - 1.8)) * (-SEA_Z / 1.8)
    if y >= -12.0: return 0.0
    r = min(1.0, (-12.0 - y) / 5.0); r = r * r * (3 - 2 * r)
    h = 1.5 + 0.8 * math.sin(x / 7.3) + 0.5 * math.sin(x / 3.1 + 1.3) + 0.35 * math.sin(y / 4.0 + x / 11.0)
    far = min(1.0, max(0.0, (-y - 45.0) / 30.0))
    return r * (h * (1 - far) + 1.3 * far)

def _axis(lo, hi, near_lo, near_hi, step, grow=1.25):
    pts = []; x = near_lo
    while x <= near_hi + 1e-6: pts.append(x); x += step
    s = step; x = near_lo
    while x > lo: s *= grow; x -= s; pts.append(max(x, lo))
    s = step; x = pts[0] + (len([p for p in pts if p >= near_lo]) - 1) * step
    while x < hi: s *= grow; x += s; pts.append(min(x, hi))
    return sorted(set(round(p, 4) for p in pts))

def build_sand(coll, M):
    xs = _axis(-1500, 1500, -70, 110, 1.0, 1.18); ys = _axis(-1500, SHORE_Y + 9, -60, SHORE_Y + 9, 0.8, 1.18)
    ys = sorted(set([y for y in ys if y <= SHORE_Y + 9] + [SHORE_Y - 1.8]))     # a vertex row exactly at the slope break
    me = bpy.data.meshes.new('sand'); V = []; F = []
    for j, y in enumerate(ys):
        for i, x in enumerate(xs): V.append((x, y, ground_z(x, y)))
    nx = len(xs)
    for j in range(len(ys) - 1):
        for i in range(nx - 1): a = j * nx + i; F.append((a, a + 1, a + nx + 1, a + nx))
    me.from_pydata(V, [], F); me.update(); me.materials.append(M['sand'])
    ob = bpy.data.objects.new('sand', me); coll.objects.link(ob); S.no_bounce(ob); STATE['objects']['sand'] = ob
    return ob

def sand_proc(nb):
    """sand albedo: noise ramp of three sands, wind ripples, pebble and shell specks near the camera, the wet band and the swash
    line that follow the surf (set_sea), distance tint toward pink-orange then pale."""
    P = STATE['P']; tc = nb.n('ShaderNodeTexCoord'); pos = tc.outputs['Object']; x, y, z = nb.sep(pos)
    s1, s2, s3 = P['sand']
    n = nb.noise(nb.vmath('MULTIPLY', pos, (1.0, 1.6, 1.0)), 0.35, detail=2.0, rough=0.6)
    c, _ = nb.ramp(n, [(0.35, s1), (0.5, s2), (0.68, s3)])
    rip = nb.wave(nb.vmath('MULTIPLY', pos, (0.35, 1.0, 1.0)), 1.4, 3.0, 0.0, 'Y')
    rip = nb.mrange(rip, 0.0, 1.0, 0.9, 1.0)
    c = nb.mix(0.55, c, nb.comb(rip, rip, rip), blend='MULTIPLY')
    cd = nb.n('ShaderNodeCameraData'); dist = cd.outputs['View Distance']
    # specks: two Voronoi layers, faded with distance (they would alias far away)
    near = nb.mrange(dist, 30.0, 8.0)
    vo = nb.n('ShaderNodeTexVoronoi'); nb._in(vo.inputs['Vector'], pos); vo.inputs['Scale'].default_value = 4.5
    sp = nb.mrange(vo.outputs['Distance'], 0.085, 0.045); rnd = nb.sep(vo.outputs['Color'])[0]
    f = nb.math('MULTIPLY', nb.math('MULTIPLY', sp, nb.math('GREATER_THAN', rnd, 0.3)), nb.math('MULTIPLY', near, 0.8))
    c = nb.mix(f, c, nb.mix(nb.math('GREATER_THAN', rnd, 0.62), '#7a4a3c', '#fff3df'))
    # wet band and swash line, moving with the surf
    t = nb.ctl('sea_t'); surf = nb.math('ADD', nb.math('MULTIPLY', nb.math('SINE', nb.math('MULTIPLY', t, 0.9)), 0.45), nb.math('MULTIPLY', nb.math('SINE', nb.math('MULTIPLY', t, 2.3)), 0.15))
    wig = nb.math('MULTIPLY', nb.math('SUBTRACT', nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.25), 0.0, 0.0), 1.0, 2.0), 0.5), 1.2)
    edge = nb.math('ADD', nb.math('ADD', surf, wig), SHORE_Y)
    dy = nb.math('SUBTRACT', y, edge)                       # 0 at the swash line, negative inland
    wet = nb.mrange(dy, -2.6, -1.6)
    c = nb.mix(wet, c, P['wet'])
    sw = nb.math('MULTIPLY', nb.mrange(dy, -0.55, -0.35), nb.mrange(dy, -0.15, -0.3))
    c = nb.mix(nb.math('MULTIPLY', sw, 0.85), c, P['foam'])
    # distance tint: hue shift with depth (spec 3.3), before the haze
    f1 = nb.mrange(dist, 20.0, 150.0); f2 = nb.mrange(dist, 150.0, 500.0)
    c = nb.mix(nb.math('MULTIPLY', f1, 0.6), c, P['sand_far'][0]); c = nb.mix(nb.math('MULTIPLY', f2, 0.7), c, P['sand_far'][1])
    return c

def mat_sea():
    """painted sea (unlit): near-to-far by the grazing angle, a pale band at the horizon, swell streaks parallel to the shore that drift,
    the surf foam band and two offshore breaker lines moving shoreward (set_sea)."""
    P = STATE['P']; m = _newmat('BEACH_sea'); nt = _tree(m); nb = NB(nt); out = nb.n('ShaderNodeOutputMaterial')
    tc = nb.n('ShaderNodeTexCoord'); pos = tc.outputs['Object']; x, y, z = nb.sep(pos)
    geo = nb.n('ShaderNodeNewGeometry'); iz = nb.sep(geo.outputs['Incoming'])[2]
    g = nb.mrange(iz, 0.004, 0.16); g = nb.math('POWER', g, 0.6)
    c = nb.mix(g, P['sea_far'], P['sea_near'])
    t = nb.ctl('sea_t')
    vec = nb.comb(nb.math('MULTIPLY', x, 0.12), nb.math('ADD', y, nb.math('MULTIPLY', t, -0.35)), 0.0)
    st = nb.wave(vec, 0.42, 4.0, 1.5, 'Y'); st = nb.mrange(st, 0.485, 0.515)
    st = nb.math('MULTIPLY', nb.math('SUBTRACT', 1.0, nb.math('MULTIPLY', nb.math('SUBTRACT', st, 0.5), 2.0, clamp=False)), 1.0)
    br = nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.08), nb.math('MULTIPLY', y, 0.3), 1.0), 1.0, 2.0); br = nb.mrange(br, 0.45, 0.6)
    stm = nb.math('MULTIPLY', nb.math('MULTIPLY', nb.mrange(st, 0.6, 1.0), br), nb.math('MULTIPLY', nb.mrange(iz, 0.01, 0.06), P['streak_amt']))
    c = nb.mix(stm, c, P['streak'])
    band = nb.mrange(iz, 0.0045, 0.0015)
    c = nb.mix(band, c, P['sea_band'])
    # surf foam band at the waterline + lace, and breaker lines
    surf = nb.math('ADD', nb.math('MULTIPLY', nb.math('SINE', nb.math('MULTIPLY', t, 0.9)), 0.45), nb.math('MULTIPLY', nb.math('SINE', nb.math('MULTIPLY', t, 2.3)), 0.15))
    wig = nb.math('MULTIPLY', nb.math('SUBTRACT', nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.25), 0.0, 0.0), 1.0, 2.0), 0.5), 1.2)
    dy = nb.math('SUBTRACT', y, nb.math('ADD', nb.math('ADD', surf, wig), SHORE_Y))
    lace = nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.9), nb.math('MULTIPLY', y, 1.4), 0.0), 1.6, 1.0)
    foam = nb.math('MULTIPLY', nb.mrange(dy, 0.75, 0.45), nb.mrange(dy, -0.6, -0.3))
    foam = nb.math('MAXIMUM', foam, nb.math('MULTIPLY', nb.math('MULTIPLY', nb.mrange(dy, 1.9, 1.5), nb.mrange(dy, 0.8, 1.2)), nb.mrange(lace, 0.55, 0.62)))
    ph = nb.math('FRACT', nb.math('DIVIDE', nb.math('ADD', nb.math('SUBTRACT', y, SHORE_Y), nb.math('MULTIPLY', t, 0.55)), 3.4))
    brk = nb.math('MULTIPLY', nb.mrange(ph, 0.0, 0.03), nb.mrange(ph, 0.11, 0.06))
    brk = nb.math('MULTIPLY', brk, nb.math('MULTIPLY', nb.mrange(dy, 2.0, 3.0), nb.mrange(dy, 13.0, 8.0)))
    brk = nb.math('MULTIPLY', brk, nb.mrange(nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.12), nb.math('MULTIPLY', y, 0.2), 2.0), 1.0, 2.0), 0.42, 0.52))
    c = nb.mix(nb.math('MAXIMUM', foam, nb.math('MULTIPLY', brk, 0.9)), c, P['foam'])
    em = nb.n('ShaderNodeEmission'); nb.L(c, em.inputs['Color'])
    last = _haze(nb, em.outputs[0], 0.5, d=(60.0, 900.0))
    nb.L(last, out.inputs['Surface'])
    return m

# ----------------------------------------------------------------------------- cottages
def _roof_slab(mb, top4, thick, mtop, mbot, medge):
    """slab whose top face is the quad top4 (counter-clockwise seen from above), thickness straight down."""
    t = [Vector(p) for p in top4]; b = [p - Vector((0, 0, thick)) for p in t]; mb.pid += 1; mb._in = True
    L = lambda a, c: ((a - c).length)
    w = L(t[1], t[0]); h = L(t[3], t[0])
    mb.face(t, mtop, [(0, 0), (w / 1.2, 0), (w / 1.2, h / 1.2), (0, h / 1.2)])
    mb.face(b[::-1], mbot)
    for i in range(4):
        j = (i + 1) % 4; mb.face([b[i], b[j], t[j], t[i]], medge)
    mb._in = False

def build_cottage(coll, M, key, cx, yb, scale=1.0, seed=0, name='cottage'):
    """one cottage on short stilts: back wall at y = yb, front (gable, porch, steps) toward the sea (+y). Returns its anchor."""
    r = random.Random(seed); sch = BT.SCHEMES[key]; W, Dp = BT.W_C, BT.D_C
    zf, ze, zr = BT.Z_FLOOR, BT.Z_EAVE, BT.Z_RIDGE
    x0, x1, y0, y1 = cx - W / 2, cx + W / 2, yb, yb + Dp
    trim = mat_lit('trim_' + key, sch['trim']); body = mat_lit('body_' + key, sch['body'])
    roofm = M['roof_maroon'] if sch['roof'] == '#5b211d' else M['roof_slate']
    mb = S.MB(); tx = STATE['tex']
    # walls with artwork
    Ht = zr - zf + 0.05
    front = mat_lit('cotf_' + key, image=tx['cot_%s_front' % key], pale=_sat(sch['body']) < 0.25)
    back = mat_lit('cotb_' + key, image=tx['cot_%s_back' % key], pale=_sat(sch['body']) < 0.25)
    side = mat_lit('cots_' + key, image=tx['cot_%s_side' % key], pale=_sat(sch['body']) < 0.25)
    pent = [(x0, zf), (x0, ze), (cx, zr), (x1, ze), (x1, zf)]
    mb.pid += 1; mb.face([(px, y1, pz) for px, pz in pent], front, [((px - x0) / W, (pz - zf) / Ht) for px, pz in pent])
    mb.pid += 1; mb.face([(px, y0, pz) for px, pz in pent[::-1]], back, [((x1 - px) / W, (pz - zf) / Ht) for px, pz in pent[::-1]])
    mb.quad((x1, y0, zf), (0, Dp, 0), (0, 0, ze - zf), side); mb.quad((x0, y1, zf), (0, -Dp, 0), (0, 0, ze - zf), side)
    # roof: two slabs from the ridge to the eaves with overhangs
    ov, oy, th = 0.32, 0.30, 0.09; sl = (zr - ze) / (W / 2); ez = ze - ov * sl
    soffit = mat_lit('soffit', '#4a2a2a', shade_mul=0.8); fascia = trim
    _roof_slab(mb, [(x0 - ov, y0 - oy, ez + th), (cx, y0 - oy, zr + th), (cx, y1 + oy, zr + th), (x0 - ov, y1 + oy, ez + th)], th, roofm, soffit, fascia)
    _roof_slab(mb, [(cx, y0 - oy, zr + th), (x1 + ov, y0 - oy, ez + th), (x1 + ov, y1 + oy, ez + th), (cx, y1 + oy, zr + th)], th, roofm, soffit, fascia)
    mb.box((cx - 0.06, y0 - oy, zr + th - 0.02), (cx + 0.06, y1 + oy, zr + th + 0.07), mat_lit('ridge', '#3b1a18'))
    # floor platform, stilts, porch, rail, steps
    wood = mat_lit('stilt', '#6d3a1f'); deck = mat_lit('deck', '#a8774f'); pd = 1.45
    mb.box((x0 - 0.05, y0 - 0.05, zf - 0.12), (x1 + 0.05, y1 + pd, zf), deck, mats=dict(front=wood, back=wood, left=wood, right=wood))
    for px in (x0 + 0.05, cx, x1 - 0.05):
        for py in (y0 + 0.05, y1 - 0.1, y1 + pd - 0.1): mb.box((px - 0.07, py - 0.07, 0.0), (px + 0.07, py + 0.07, zf - 0.12), wood)
    for px in (x0 + 0.02, x1 - 0.14):
        mb.box((px, y1 + pd - 0.14, zf), (px + 0.12, y1 + pd - 0.02, ze - 0.05), trim)                 # porch posts
    # porch shed roof
    _roof_slab(mb, [(x0 - 0.15, y1, ze + 0.05), (x1 + 0.15, y1, ze + 0.05), (x1 + 0.15, y1 + pd + 0.2, ze - 0.3), (x0 - 0.15, y1 + pd + 0.2, ze - 0.3)], 0.07, roofm, soffit, fascia)
    sw = 0.9
    for (a, b) in ((x0 + 0.02, cx - sw / 2), (cx + sw / 2, x1 - 0.02)):
        mb.box((a, y1 + pd - 0.1, zf + 0.78), (b, y1 + pd - 0.02, zf + 0.86), trim)                   # top rail
        k = max(2, int((b - a) / 0.22))
        for i in range(k + 1): xx = a + (b - a) * i / k; mb.box((xx - 0.025, y1 + pd - 0.08, zf), (xx + 0.025, y1 + pd - 0.04, zf + 0.8), trim)
    for i in range(3):                                                                                  # steps down to the sand
        z1_ = zf - 0.12 - i * 0.16; mb.box((cx - sw / 2, y1 + pd + i * 0.28, 0.0), (cx + sw / 2, y1 + pd + (i + 1) * 0.28, max(0.06, z1_)), deck, mats=dict(front=wood, left=wood, right=wood))
    # stove pipe
    mb.frustum((x0 + 0.75, y0 + 0.8, ze), (x0 + 0.75, y0 + 0.8, zr + 0.55), 0.09, 0.09, mat_lit('iron', '#3b3442', shade_mul=1.2), seg=8)
    mb.frustum((x0 + 0.75, y0 + 0.8, zr + 0.55), (x0 + 0.75, y0 + 0.8, zr + 0.62), 0.15, 0.15, mat_lit('iron', '#3b3442', shade_mul=1.2), seg=8)
    ob = _obj(mb, name, coll, hull=hull_for((cx, yb + 2, 2)))
    if scale != 1.0:
        ob.location = (cx * (1 - scale), yb * (1 - scale), 0); ob.scale = (scale, scale, scale)
    return dict(name=name, scheme=key, center=(cx, yb + Dp / 2, 0.0), x=(cx - W / 2 * scale, cx + W / 2 * scale), y_back=yb, y_front=yb + Dp * scale,
                porch_front=yb + (Dp + pd) * scale, steps_front=yb + (Dp + pd + 0.84) * scale, size=(W * scale, Dp * scale), eave=ze * scale, ridge=round(zr * scale + 0.09 * scale, 3))

# ----------------------------------------------------------------------------- props
def _tube(mb, pts, r, mat, seg=4):
    for a, b in zip(pts[:-1], pts[1:]): mb.frustum(a, b, r, r, mat, seg=seg, cap0=False, cap1=False)

def _sag(a, b, sag, n=10):
    a, b = Vector(a), Vector(b); return [a.lerp(b, i / n) - Vector((0, 0, sag * 4 * (i / n) * (1 - i / n))) for i in range(n + 1)]

def build_poles(coll, M):
    """telegraph poles between the cottages, beside the boardwalk, every 14 D, with two crossarms, insulators and four sagging wires."""
    mb = S.MB(); wm = S.MB(); wood = mat_lit('pole', '#6d3a1f'); arm = mat_lit('arm', '#7a4a2a'); ins = mat_lit('insul', '#b9d7e4')
    wire = mat_unlit('wire', '#2a1d26', camera_only=False); xs = [-35.0 + 14 * k for k in range(9)]; Y = 2.75; H = 7.4; tops = []
    for x in xs:
        mb.frustum((x, Y, 0), (x, Y, H), 0.13, 0.10, wood, seg=10)
        mb.box((x - 1.1, Y - 0.07, H - 0.55), (x + 1.1, Y + 0.07, H - 0.40), arm); mb.box((x - 0.8, Y - 0.07, H - 1.15), (x + 0.8, Y + 0.07, H - 1.0), arm)
        mb.box((x - 0.5, Y - 0.04, H - 1.0), (x - 0.45, Y + 0.04, H - 0.55), arm)
        pts = [(x + dx, Y, H - 0.40) for dx in (-0.95, -0.4, 0.4, 0.95)] + [(x + dx, Y, H - 1.0) for dx in (-0.65, 0.65)]
        for p in pts: mb.frustum(p, (p[0], p[1], p[2] + 0.16), 0.05, 0.035, ins, seg=6)
        tops.append([(p[0], p[1], p[2] + 0.12) for p in pts])
    for a, b in zip(tops[:-1], tops[1:]):
        for pa, pb in zip(a, b): _tube(wm, _sag(pa, pb, 0.55), 0.016, wire)
    _obj(mb, 'poles', coll, hull=0.03); w = _obj(wm, 'wires', coll); w.visible_shadow = True
    return [(x, Y, 0.0) for x in xs], H

def build_boardwalk(coll, M):
    mb = S.MB(); y0, y1, z = 3.05, 4.65, 0.36; x0, x1 = -60.0, 110.0
    pl = mat_lit('planks', image=STATE['tex']['planks'], pale=False)
    mb.quad((x0, y0, z), (x1 - x0, 0, 0), (0, y1 - y0, 0), pl, (x0 / 2.0, 0.0, x1 / 2.0, 1.0))
    # UVs: u along x in 2 D tiles; the tile is drawn with planks across the walk -> rotate by swapping in the image (planks run along v)
    st = mat_lit('stringer', '#5a3526')
    mb.box((x0, y0 - 0.06, z - 0.22), (x1, y0, z), st); mb.box((x0, y1, z - 0.22), (x1, y1 + 0.06, z), st)
    x = x0
    while x <= x1: mb.box((x - 0.08, y0 + 0.02, 0), (x + 0.08, y0 + 0.16, z - 0.2), st); mb.box((x - 0.08, y1 - 0.16, 0), (x + 0.08, y1 - 0.02, z - 0.2), st); x += 3.0
    ob = _obj(mb, 'boardwalk', coll, hull=0.02)
    # the plank tile has planks across its 2 D length (v); map u (world x) to the tile's v
    uv = ob.data.uv_layers.active.data
    for poly in ob.data.polygons:
        if poly.material_index == 0:
            for li in poly.loop_indices:
                co = ob.data.vertices[ob.data.loops[li].vertex_index].co; uv[li].uv = ((co.y - y0) / 1.6, co.x / 2.0)
    return dict(y0=y0, y1=y1, z=z, x0=x0, x1=x1)

def build_fence(coll, M, gap=(-3.4, -1.2)):
    mb = S.MB(); rm = S.MB(); post = mat_lit('fencepost', '#8a5a35'); rope = mat_lit('rope', '#d9c9a8', haze=1.0)
    Y = 5.75; xs = []; x = -40.0
    while x <= 75.0:
        if not (gap[0] < x < gap[1]): xs.append(x)
        x += 2.5
    for x in xs: mb.box((x - 0.06, Y - 0.06, 0), (x + 0.06, Y + 0.06, 1.35), post); mb.frustum((x, Y, 1.35), (x, Y, 1.42), 0.085, 0.02, post, seg=6)
    for a, b in zip(xs[:-1], xs[1:]):
        if b - a > 3.0: continue
        for zz, sg in ((1.2, 0.22), (0.7, 0.16)): _tube(rm, _sag((a, Y - 0.07, zz), (b, Y - 0.07, zz), sg, 6), 0.022, rope)
    _obj(mb, 'fence', coll, hull=0.022); _obj(rm, 'fence_rope', coll)
    return Y

def build_grass(coll, M, rng):
    """dune-grass tufts (thin blade triangles, no ink) with a shape key 'wind' (blades lean onshore, toward -y)."""
    mats = [mat_lit('grass%d' % i, c, toon=False, gain=1.0) for i, c in enumerate(('#67832c', '#8aa23a', '#4f6b2a'))]
    V = []; F = []; MI = []; W = []
    def tuft(x, y, h, n=5):
        z0 = ground_z(x, y) - 0.03
        for k in range(n):
            a = rng.uniform(0, 2 * math.pi); lean = rng.uniform(0.1, 0.45); hh = h * rng.uniform(0.6, 1.1); w = rng.uniform(0.035, 0.06)
            bx, by = x + 0.08 * math.cos(a), y + 0.08 * math.sin(a); tx, ty = bx + lean * hh * math.cos(a), by + lean * hh * math.sin(a)
            px, py = -math.sin(a) * w, math.cos(a) * w; i = len(V)
            V.extend([(bx - px, by - py, z0), (bx + px, by + py, z0), (tx, ty, z0 + hh)]); F.append((i, i + 1, i + 2)); MI.append(rng.randrange(3))
            W.extend([(0, 0, 0), (0, 0, 0), (rng.uniform(0.15, 0.3) * hh, -rng.uniform(0.45, 0.7) * hh, -0.25 * hh)])
    for _ in range(170):                                  # strip between the boardwalk and the fence, and seaward of it
        x = rng.uniform(-45, 80); y = rng.uniform(4.8, 6.6)
        if -3.6 < x < -1.0: continue
        tuft(x, y, rng.uniform(0.6, 1.0))
    for _ in range(140):                                  # around the stilts and behind the cottages
        x = rng.uniform(-45, 80); y = rng.uniform(-5.5, 2.2); tuft(x, y, rng.uniform(0.5, 0.9), 4)
    for _ in range(260):                                  # dunes inland
        x = rng.uniform(-80, 110); y = rng.uniform(-40, -12.5); tuft(x, y, rng.uniform(0.8, 1.3), 6)
    for _ in range(14):                                   # a few tufts on the open beach, well clear of the marks
        x = rng.choice([rng.uniform(-14, -6), rng.uniform(10, 18)]); y = rng.uniform(6.8, 10.5); tuft(x, y, rng.uniform(0.5, 0.8), 4)
    me = bpy.data.meshes.new('dune_grass'); me.from_pydata(V, [], F); me.update()
    for m in mats: me.materials.append(m)
    for p, mi in zip(me.polygons, MI): p.material_index = mi
    ob = bpy.data.objects.new('dune_grass', me); coll.objects.link(ob); S.no_bounce(ob); STATE['objects']['dune_grass'] = ob
    ob.shape_key_add(name='Basis'); kb = ob.shape_key_add(name='wind'); kb.slider_max = 2.0
    for i, (v, w) in enumerate(zip(V, W)): kb.data[i].co = Vector(v) + Vector(w)
    _drive(kb, 'value', 'wind', ['wind'])
    return ob

def build_umbrella(coll, at=(7.2, 9.4)):
    mb = S.MB(); red = mat_lit('umb_red', '#c2311e'); cr = mat_lit('umb_cream', '#f6efe2'); pole = mat_lit('umb_pole', '#e9dcc0')
    mb.frustum((0, 0, -0.3), (0, 0, 3.45), 0.04, 0.04, pole, seg=8)
    n = 8; R = 1.95; apex = Vector((0, 0, 3.35))
    for i in range(n):
        a0 = 2 * math.pi * i / n; a1 = 2 * math.pi * (i + 1) / n; am = (a0 + a1) / 2
        p0 = Vector((R * math.cos(a0), R * math.sin(a0), 2.72)); p1 = Vector((R * math.cos(a1), R * math.sin(a1), 2.72)); pm = Vector((R * 0.93 * math.cos(am), R * 0.93 * math.sin(am), 2.66))
        m = red if i % 2 == 0 else cr; mb.pid += 1; mb.face([apex, p0, pm], m); mb.face([apex, pm, p1], m)
    mb.sphere((0, 0, 3.42), 0.07, pole, seg=8, rings=4)
    ob = _obj(mb, 'umbrella', coll, hull=0.025); ob.location = (at[0], at[1], 0.0)
    _drive(ob, 'rotation_euler', '0.22*wind+0.035*wind*sin(frame*0.7)', ['wind'], 0)
    return ob

def build_boat(coll, at=(-4.6, 10.9), yaw=62.0):
    """clinker rowing boat pulled up on the sand: lofted hull, cream gunwale band, wooden inside, two thwarts, an oar."""
    out_m = mat_lit('hull', '#c2311e'); band = mat_lit('gunwale', '#f6efe2'); inner = mat_lit('boat_in', '#9a6a42'); seat = mat_lit('thwart', '#7a4a2a')
    L = 4.2; N = 14; secs = []
    for i in range(N + 1):
        t = i / N
        w = 0.78 * (1 - 0.32 * ((0.42 - t) / 0.42) ** 2) if t < 0.42 else 0.78 * max(0.03, 1 - ((t - 0.42) / 0.58) ** 2.2)
        zg = 0.78 + 0.22 * ((t - 0.45) * 2) ** 2; zk = 0.05 + 0.06 * abs(t - 0.5)
        ys = t * L - L / 2
        secs.append([(ys, -w, zg), (ys, -0.97 * w, zg - 0.15), (ys, -0.82 * w, zk + 0.3), (ys, -0.45 * w, zk + 0.07), (ys, 0.0, zk),
                     (ys, 0.45 * w, zk + 0.07), (ys, 0.82 * w, zk + 0.3), (ys, 0.97 * w, zg - 0.15), (ys, w, zg)])
    mb = S.MB(); mb.pid += 1
    for i in range(N):
        A_, B_ = secs[i], secs[i + 1]
        for k in range(len(A_) - 1):
            m = band if k in (0, len(A_) - 2) else out_m
            mb.face([A_[k], A_[k + 1], B_[k + 1], B_[k]], m)
    tr = secs[0]; mb.pid += 1; mb.face(tr[::-1], band)                                                  # transom
    ib = S.MB(); ib.pid += 1
    for i in range(N):
        A_ = [(p[0], p[1] * 0.9, p[2] + 0.05) for p in secs[i]]; B_ = [(p[0], p[1] * 0.9, p[2] + 0.05) for p in secs[i + 1]]
        for k in range(len(A_) - 1): ib.face([B_[k], B_[k + 1], A_[k + 1], A_[k]], inner)
    for yy in (-0.9, 0.5): ib.box((yy - 0.14, -0.66, 0.52), (yy + 0.14, 0.66, 0.6), seat)
    ib.box((-1.6, -0.45, 0.62), (2.1, -0.38, 0.68), seat); ib.box((1.6, -0.55, 0.6), (2.3, -0.32, 0.64), seat)       # oar shaft and blade
    ob = _obj(mb, 'boat', coll, hull=0.025); ob2 = _obj(ib, 'boat_inside', coll)
    for o in (ob, ob2): o.location = (at[0], at[1], 0.0); o.rotation_euler = (0.0, math.radians(7), math.radians(yaw))
    return ob

def build_lifeguard_chair(coll, at=(-9.2, 10.4)):
    mb = S.MB(); wd = mat_lit('chair_white', '#efe6d4'); tx = STATE['tex']
    x, y = at; sh = 2.9
    for dx, dy in ((-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
        mb.frustum((x + dx, y + dy, 0), (x + dx * 0.5, y + dy * 0.5, sh), 0.07, 0.07, wd, seg=6)
    for z in (0.6, 1.3, 2.0): mb.box((x - 0.62 + 0.1 * z / 2, y + 0.6 - 0.1 * z, z), (x + 0.62 - 0.1 * z / 2, y + 0.68 - 0.1 * z, z + 0.08), wd)   # rungs (front, seaward)
    mb.box((x - 0.55, y - 0.5, sh), (x + 0.55, y + 0.5, sh + 0.1), wd)                                  # seat
    mb.box((x - 0.55, y - 0.55, sh + 0.1), (x + 0.55, y - 0.45, sh + 1.15), wd)                         # back (landward)
    for sx in (-0.55, 0.47): mb.box((x + sx, y - 0.5, sh + 0.55), (x + sx + 0.08, y + 0.45, sh + 0.62), wd)
    ob = _obj(mb, 'lifeguard_chair', coll, hull=0.025)
    sg = S.MB(); sg.quad((x - 0.5, y - 0.56, sh + 0.55), (1.0, 0, 0), (0, 0, 0.3), mat_lit('chair_sign', image=tx['chair_sign']), (0, 0, 1, 1)); _obj(sg, 'chair_sign', coll)
    # flag pole and red flag on the chair (wind: shape key 'flap' + yaw)
    fp = S.MB(); fp.frustum((x + 0.62, y - 0.5, sh), (x + 0.62, y - 0.5, sh + 2.4), 0.025, 0.025, mat_lit('flagpole', '#d8ccb4'), seg=6); _obj(fp, 'flagpole', coll, hull=0.012)
    fl = S.MB(); fm = mat_lit('flag', '#c2311e'); nx = 8
    for i in range(nx):
        a, b = i / nx * 0.75, (i + 1) / nx * 0.75
        fl.pid += 1; fl.face([(a, 0, 0), (b, 0, 0), (b, 0, 0.45), (a, 0, 0.45)], fm)
    fo = _obj(fl, 'flag', coll, shadow=True); fo.location = (x + 0.62, y - 0.5, sh + 1.9)
    fo.shape_key_add(name='Basis'); kb = fo.shape_key_add(name='flap')
    for i, v in enumerate(fo.data.vertices): kb.data[i].co = v.co + Vector((0.0, 0.12 * math.sin(v.co.x * 9.0) * v.co.x, -0.05 * v.co.x))
    _drive(kb, 'value', 'wind*(0.6+0.4*sin(frame*0.9))', ['wind'])
    _drive(fo, 'rotation_euler', '-1.25+0.9*min(wind,1)', ['wind'], 2)
    return ob

def build_small_props(coll):
    tx = STATE['tex']; out = {}
    mb = S.MB(); post = mat_lit('signpost', '#6d3a1f'); x, y = -4.9, 6.15                              # BATHING BEACH sign by the fence gap
    for sx in (-0.95, 0.95): mb.box((x + sx - 0.06, y - 0.06, 0), (x + sx + 0.06, y + 0.06, 2.75), post)
    mb.box((x - 1.15, y - 0.03, 1.75), (x + 1.15, y + 0.04, 2.73), mat_lit('signboard', '#f6efe2'))
    _obj(mb, 'sign', coll, hull=0.02)
    sf = S.MB(); sf.quad((x + 1.1, y + 0.045, 1.77), (-2.2, 0, 0), (0, 0, 0.95), mat_lit('sign_face', image=tx['sign']), (0, 0, 1, 1)); _obj(sf, 'sign_face', coll)
    out['sign'] = (x, y, 0.0)
    # deck chair with striped sling
    mb = S.MB(); fr = mat_lit('dc_frame', '#8a5a35'); g1 = mat_lit('dc_green', '#2f6a5a'); g2 = mat_lit('dc_cream', '#efe2c8')
    x, y = 9.6, 8.6
    for sx in (-0.45, 0.45):
        mb.frustum((x + sx, y + 0.7, 0), (x + sx, y - 0.6, 1.5), 0.04, 0.04, fr, seg=6); mb.frustum((x + sx, y - 0.4, 0), (x + sx, y + 0.5, 0.75), 0.04, 0.04, fr, seg=6)
    for k in range(6):
        a = k / 6; b = (k + 1) / 6; p = lambda t, sx: (x + sx, y + 0.55 - 1.05 * t, 0.35 + 1.05 * t - 0.25 * math.sin(math.pi * t))
        mb.pid += 1; mb.face([p(a, -0.42), p(a, 0.42), p(b, 0.42), p(b, -0.42)], g1 if k % 2 else g2)
    _obj(mb, 'deck_chair', coll, hull=0.02); out['deck_chair'] = (x, y, 0.0)
    # towel under the umbrella, bucket and spade, picnic basket, crate by a porch
    mb = S.MB(); x, y = 6.2, 10.0
    for k in range(6): mb.quad((x - 0.8, y - 0.55 + k * 0.19, 0.012), (1.6, 0, 0), (0, 0.19, 0), mat_lit('towel%d' % (k % 2), ('#2f5a8a', '#f6efe2')[k % 2]))
    _obj(mb, 'towel', coll)
    mb = S.MB(); bk = mat_lit('bucket', '#2f5a8a'); x, y = 4.9, 10.7
    mb.frustum((x, y, 0), (x, y, 0.42), 0.17, 0.23, bk, seg=12, cap1=False); _tube(mb, [(x - 0.22, y, 0.42), (x, y, 0.62), (x + 0.22, y, 0.42)], 0.012, mat_lit('iron', '#3b3442'))
    mb.box((x + 0.3, y - 0.03, 0), (x + 0.36, y + 0.03, 0.55), mat_lit('spade', '#c2311e')); _obj(mb, 'bucket', coll, hull=0.015)
    mb = S.MB(); bs = mat_lit('basket', '#b08a52'); x, y = 8.4, 10.3
    mb.box((x - 0.4, y - 0.27, 0), (x + 0.4, y + 0.27, 0.42), bs); mb.box((x - 0.42, y - 0.29, 0.42), (x + 0.42, y + 0.29, 0.48), mat_lit('basket_lid', '#c29a5e'))
    _tube(mb, [(x - 0.3, y, 0.48), (x - 0.2, y, 0.75), (x + 0.2, y, 0.75), (x + 0.3, y, 0.48)], 0.025, bs); _obj(mb, 'picnic_basket', coll, hull=0.015)
    mb = S.MB(); cr = mat_lit('crate', '#a8774f'); x, y = -9.4, 2.5
    mb.box((x - 0.6, y - 0.6, 0), (x + 0.6, y + 0.6, 1.0), cr)
    for z in (0.3, 0.65): mb.box((x - 0.62, y - 0.62, z), (x + 0.62, y + 0.62, z + 0.08), mat_lit('crate_slat', '#8a5a3c'))
    _obj(mb, 'crate', coll, hull=0.02)
    # footprints: shallow darker ovals in the sand from the boardwalk gap toward the water
    mb = S.MB(); fpm = mat_lit('footprint', '#b77c4e', haze=1.0); rr = random.Random(9)
    for k in range(14):
        t = k / 13; fx = -2.3 + 3.2 * t + 0.18 * (1 if k % 2 else -1); fy = 6.3 + 6.8 * t
        if 6.9 < fy < 9.2 and -2.6 < fx < 4.8: continue
        pts = [(fx + 0.09 * math.cos(a), fy + 0.15 * math.sin(a), 0.006) for a in [i * math.pi / 5 for i in range(10)]]
        mb.pid += 1; mb.face(pts, fpm)
    _obj(mb, 'footprints', coll, shadow=False)
    return out

def build_far(coll):
    """far bluffs at both ends of the beach (cards, no ink), hazed into the sky."""
    P = STATE['P']; tx = STATE['tex']
    for i, (x, col, h) in enumerate(((430.0, P['headland'][0], 26.0), (-470.0, P['headland'][1], 20.0))):
        def af(nb, _=None):
            t = nb.n('ShaderNodeTexImage'); t.image = _img(tx['headland']); t.extension = 'CLIP'; return t.outputs['Alpha']
        m = mat_unlit('headland%d' % i, nb_mix_hex(col, P['haze'], 0.35), alpha_fn=af, camera_only=True)
        mb = S.MB(); sgn = 1 if x < 0 else -1
        mb.quad((x, -420.0 if x > 0 else 60.0, -1.0), (0, (480.0 if x > 0 else -480.0), 0), (0, 0, h), m, (0, 0, 1, 1))
        o = _obj(mb, 'headland%d' % i, coll, shadow=False)

def nb_mix_hex(a, b, t):
    A_ = [int(a.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]; B_ = [int(b.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(int(round(A_[i] + (B_[i] - A_[i]) * t)) for i in range(3))

# ----------------------------------------------------------------------------- fog bank, wave, rain
def build_fog(coll):
    """a ring band of radius FOG_R around the origin over the sea half; height and opacity follow ctl['fog']."""
    P = STATE['P']; mb = S.MB(); n = 64; a0, a1 = math.radians(4), math.radians(176)
    def af(nb):
        # review fix: billowing soft top (the edge height itself wanders with a noise along the ring) instead of a hard noisy line
        tc = nb.n('ShaderNodeTexCoord'); u, v, _ = nb.sep(tc.outputs['UV'])
        n_ = nb.noise(nb.comb(nb.math('MULTIPLY', u, 34.0), nb.math('MULTIPLY', v, 1.5), 0.0), 1.0, 2.0, 0.55)
        edge = nb.math('ADD', 0.42, nb.math('MULTIPLY', n_, 0.55))
        a = nb.mrange(nb.math('SUBTRACT', v, edge), 0.06, -0.22)
        a = nb.math('MULTIPLY', a, nb.mrange(v, -0.05, 0.05))
        return nb.math('MULTIPLY', nb.math('MULTIPLY', a, P['fog_alpha']), nb.ctl('fog', 'min(1,fog*3)'))
    def col(nb):                                            # a touch darker at the foot, lighter at the top: a bank, not a stripe
        tc = nb.n('ShaderNodeTexCoord'); v = nb.sep(tc.outputs['UV'])[1]
        return nb.mix(nb.mrange(v, 0.0, 0.7), P['fog_foot'], P['fog'])
    m = mat_unlit('fog', None, alpha_fn=af, camera_only=True, color_fn=col)
    for i in range(n):
        t0 = a0 + (a1 - a0) * i / n; t1 = a0 + (a1 - a0) * (i + 1) / n
        p0 = (FOG_R * math.cos(t0), FOG_R * math.sin(t0)); p1 = (FOG_R * math.cos(t1), FOG_R * math.sin(t1))
        mb.pid += 1; mb.face([(p1[0], p1[1], -0.1), (p0[0], p0[1], -0.1), (p0[0], p0[1], 1.0), (p1[0], p1[1], 1.0)], m, [((i + 1) / n, 0), (i / n, 0), (i / n, 1), ((i + 1) / n, 1)])
    ob = _obj(mb, 'fog_bank', coll, shadow=False)
    _drive(ob, 'scale', '30*max(0.001,fog)**0.75', ['fog'], 2)       # review: a^0.75, so a low amount is already a visible band
    return ob

PROFILE = [(0.0, -0.06), (0.10, 0.16), (0.19, 0.38), (0.23, 0.58), (0.21, 0.74), (0.13, 0.86), (0.02, 0.93), (-0.10, 0.95), (-0.19, 0.91),
           (-0.23, 0.85), (-0.20, 0.95), (-0.12, 1.01), (0.02, 1.04), (0.20, 1.02), (0.45, 0.93), (0.85, 0.72), (1.4, 0.45), (2.2, 0.2), (3.2, 0.02), (3.8, -0.08)]

def mat_wave():
    """the wave face (review rewrite). Painted by height (P['wave'] ramp: dark base, deep blue-teal face, a lighter translucent band
    under the lip, white crest) with streaks running UP the face, foam churn at the toe and spray specks under the lip; mostly self-coloured
    (emission art x wave_emit) plus the preset key (Lambert, art x wave_gain x K) so it reads as water in every preset; hazed to the
    fog colour with distance (far off it is the fog bank). Replaces the horizontal light bands that read as cloud strata."""
    P = STATE['P']; m = _newmat('BEACH_wave'); nt = _tree(m); nb = NB(nt); out = nb.n('ShaderNodeOutputMaterial')
    tc = nb.n('ShaderNodeTexCoord'); x, y, z = nb.sep(tc.outputs['Object'])
    c, _ = nb.ramp(z, P['wave'])
    n = nb.noise(nb.comb(nb.math('MULTIPLY', x, 0.8), nb.math('MULTIPLY', y, 0.3), nb.math('MULTIPLY', z, 1.4)), 1.6, 1.0, 0.5)
    win = nb.math('MULTIPLY', nb.mrange(z, 0.10, 0.40), nb.mrange(z, 0.93, 0.80))
    c = nb.mix(nb.math('MULTIPLY', nb.math('MULTIPLY', nb.mrange(n, 0.56, 0.66), win), 0.5), c, P['wave_lite'])
    c = nb.mix(nb.math('MULTIPLY', nb.math('MULTIPLY', nb.mrange(n, 0.42, 0.33), win), 0.4), c, P['wave'][0][1])
    n2 = nb.noise(nb.comb(nb.math('MULTIPLY', x, 2.2), nb.math('MULTIPLY', y, 2.0), nb.math('MULTIPLY', z, 16.0)), 1.0, 0.0)
    spk = nb.math('MULTIPLY', nb.mrange(n2, 0.63, 0.69), nb.mrange(z, 0.70, 0.86))
    n3 = nb.noise(nb.comb(nb.math('MULTIPLY', x, 3.0), nb.math('MULTIPLY', y, 3.0), nb.math('MULTIPLY', z, 40.0)), 1.0, 1.0)
    churn = nb.math('MAXIMUM', nb.mrange(z, 0.035, 0.015), nb.math('MULTIPLY', nb.mrange(z, 0.085, 0.03), nb.mrange(n3, 0.50, 0.58)))
    c = nb.mix(nb.math('MAXIMUM', spk, churn), c, P['foam'])
    dif = nb.n('ShaderNodeBsdfDiffuse'); nb.L(nb.vmath('SCALE', c, scale=P['wave_gain']), dif.inputs['Color'])
    em = nb.n('ShaderNodeEmission'); nb.L(nb.vmath('ADD', nb.vmath('SCALE', c, scale=P['wave_emit']), tuple(P['lift'])), em.inputs['Color'])
    add = nb.n('ShaderNodeAddShader'); nb.L(dif.outputs[0], add.inputs[0]); nb.L(em.outputs[0], add.inputs[1])
    nb.L(_haze(nb, add.outputs[0], 1.0, color=P['fog'], d=(30.0, 260.0), hmax=0.97), out.inputs['Surface'])
    return m

def mat_wave_foam():
    """foam lip: flat two-tone cartoon foam (white top, blue-grey underside by the normal), unlit, hazed like the wave."""
    P = STATE['P']; m = _newmat('BEACH_wave_foam'); nt = _tree(m); nb = NB(nt); out = nb.n('ShaderNodeOutputMaterial')
    geo = nb.n('ShaderNodeNewGeometry'); nz = nb.sep(geo.outputs['Normal'])[2]
    c = nb.mix(nb.mrange(nz, -0.25, -0.1), P['foam_shade'], P['foam'])
    em = nb.n('ShaderNodeEmission'); nb.L(c, em.inputs['Color']); em.inputs['Strength'].default_value = P.get('foam_emit', 0.95)
    nb.L(_haze(nb, em.outputs[0], 1.0, color=P['fog'], d=(30.0, 260.0), hmax=0.97), out.inputs['Surface'])
    return m

def build_wave(coll):
    """ONE wall of water: a profile (concave face, curling lip, long back) extruded along x with a wavy crest, height-normalised (z 0..1)
    and scaled by the driver of ctl['wave']; a scalloped foam ribbon rides the lip. Lit by the key, no ink, hazed toward the fog colour."""
    P = STATE['P']; m = mat_wave(); foam = mat_wave_foam()
    xs = []; x = -620.0
    while x <= 620.0: xs.append(x); x += 0.5 if abs(x) < 60 else (2.0 if abs(x) < 200 else 10.0)
    V = []; F = []; FV = []; FF = []; ns = len(PROFILE); ring = 10
    for i, x in enumerate(xs):
        hf = 1 + 0.09 * math.sin(x / 9.0) + 0.05 * math.sin(x / 3.7 + 1.0) + 0.03 * math.sin(x / 1.6 + 0.4)
        lip = 1 + 0.25 * math.sin(x / 6.3 + 2.0)
        for (u, v) in PROFILE:
            k = max(0.0, (v - 0.5) / 0.5)
            V.append((x, u * (lip if u < 0 else 1.0), v * (1 + (hf - 1) * k)))
        # review fix: the old ribbon (radius 0.045..0.115 of the height, 3.5 D scallops, lit) read as a row of cumulus clouds.
        # Now a thin, finely scalloped lip of foam (0.5..0.9 D at full height), flat two-tone (mat_wave_foam).
        cx_, cz_ = -0.10 * lip, 0.995 * hf; r = 0.026 + 0.012 * abs(math.sin(x * 1.7)) + 0.008 * abs(math.sin(x * 2.9 + 1.0))
        for j in range(ring):
            a = 2 * math.pi * j / ring; FV.append((x, cx_ + r * 1.6 * math.cos(a), cz_ + 0.01 + r * math.sin(a)))
    for i in range(len(xs) - 1):
        for k in range(ns - 1):
            a = i * ns + k; b = (i + 1) * ns + k; F.append((a, b, b + 1, a + 1))
        for j in range(ring):
            a = i * ring + j; a2 = i * ring + (j + 1) % ring; b = (i + 1) * ring + j; b2 = (i + 1) * ring + (j + 1) % ring; FF.append((a, a2, b2, b))
    me = bpy.data.meshes.new('wave'); me.from_pydata(V, [], F); me.update(); me.materials.append(m)
    ob = bpy.data.objects.new('wave', me); coll.objects.link(ob); S.no_bounce(ob)
    for p in me.polygons: p.use_smooth = True
    fe = bpy.data.meshes.new('wave_foam'); fe.from_pydata(FV, [], FF); fe.update(); fe.materials.append(foam)
    fo = bpy.data.objects.new('wave_foam', fe); coll.objects.link(fo); S.no_bounce(fo); fo.parent = ob
    for p in fe.polygons: p.use_smooth = True
    W_ = WAVE
    _drive(ob, 'location', '%g+%g*(1-wave)**1.7' % (W_['y_near'], W_['travel']), ['wave'], 1)
    _drive(ob, 'location', '%g-(%g+%g*wave)*1.12*max(0,1-wave/0.2)**2' % (SEA_Z - 0.05, W_['h_far'], W_['h_near'] - W_['h_far']), ['wave'], 2)
    for ax in (1, 2): _drive(ob, 'scale', '%g+%g*wave' % (W_['h_far'], W_['h_near'] - W_['h_far']), ['wave'], ax)
    STATE['objects']['wave'] = ob; STATE['objects']['wave_foam'] = fo
    return ob

def wave_state(p):
    """world front (toe) y, crest height and base z of the wave at progress p (what the drivers compute)."""
    W_ = WAVE; h = W_['h_far'] + (W_['h_near'] - W_['h_far']) * p
    return dict(y_toe=W_['y_near'] + W_['travel'] * (1 - p) ** 1.7, lip_y=W_['y_near'] + W_['travel'] * (1 - p) ** 1.7 - 0.23 * 1.25 * h,
                crest=h * 1.04 + SEA_Z - 0.05 - h * 1.12 * max(0.0, 1 - p / 0.2) ** 2, height=h)

RAIN_PERIOD = 12.0
def build_rain(coll):
    """drizzle / rain as geometry: about 1800 thin streak quads (1.2 px wide at their depth, 1.3 to 9 D from the lens) in a camera-parented
    field that falls through drivers on the frame number (fmod, deterministic, no particles). Each streak has a random density rank (UV u):
    it shows when u < ctl['rain'], so the amount sets how many streaks there are; slant follows ctl['wind']. Rays only pay where a streak is."""
    r = random.Random(77); V = []; F = []; UV = []
    hmax = 9.0 * 640.0 / 782.2 * 1.25
    # review: 1300 streaks (was 1800), 1.8..11 D from the lens (was 1.3..9: the nearest ones were fat white bars over the faces),
    # 1 px wide, fainter (opacity 0.18..0.5, near ones halved) and blue-grey, so heads and faces stay readable at amount 1
    for i in range(1300):
        d = 1.8 + 9.2 * r.random() ** 1.4; hw = d * 360.0 / 782.2 * 1.5; hh = d * 640.0 / 782.2 * 1.15
        x = r.uniform(-hw, hw); y = r.uniform(-hh, hh + RAIN_PERIOD); L = d * r.uniform(0.045, 0.10); w = d * 1.0 / 782.2
        for k in (0, 1):                                    # two copies one period apart: the field wraps seamlessly
            yy = y - k * RAIN_PERIOD
            if yy > hh + 0.5 or yy + L < -hh - RAIN_PERIOD - 0.5: continue
            n = len(V); V += [(x - w, yy, -d), (x + w, yy, -d), (x + w + L * 0.04, yy + L, -d), (x - w + L * 0.04, yy + L, -d)]; F.append((n, n + 1, n + 2, n + 3))
            u = r.random(); op = r.uniform(0.18, 0.5) * (0.5 if d < 3.0 else 1.0); UV.append((u, op))
    me = bpy.data.meshes.new('rain'); me.from_pydata(V, [], F); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for p, (u, op) in zip(me.polygons, UV):
        for li in p.loop_indices: uvl.data[li].uv = (u, op)
    def af(nb):
        tc = nb.n('ShaderNodeTexCoord'); u, op, _ = nb.sep(tc.outputs['UV'])
        return nb.math('MULTIPLY', nb.math('LESS_THAN', u, nb.ctl('rain', 'min(rain,1)')), nb.math('MULTIPLY', op, nb.ctl('rain', 'min(1.3,0.6+0.7*rain)')))
    me.materials.append(mat_unlit('rain', STATE['P'].get('rain_col', '#cfd6ec'), strength=1.0, alpha_fn=af, camera_only=True))
    ob = bpy.data.objects.new('rain', me); coll.objects.link(ob); S.no_bounce(ob); ob.visible_shadow = False
    _drive(ob, 'location', '-fmod(frame*0.33,%g)' % RAIN_PERIOD, [], 1)
    _drive(ob, 'rotation_euler', '0.10+0.22*min(wind,1.2)', ['wind'], 2)
    _drive(ob, 'hide_render', 'rain<0.002', ['rain'])
    STATE['rain'] = [ob]
    return [ob]

def attach_rain(cam):
    """parent the rain layers to a camera (done by make_camera; call again if you switch to a camera made elsewhere)."""
    for ob in STATE.get('rain', []): ob.parent = cam; ob.matrix_parent_inverse.identity(); ob.location.x = 0.0; ob.location.z = 0.0

# ----------------------------------------------------------------------------- build
def _ctl(scene, coll):
    ob = bpy.data.objects.new('beach_ctl', None); coll.objects.link(ob)
    for k, v in (('fog', 0.0), ('wave', 0.0), ('rain', 0.0), ('sea_t', 0.0), ('wind', 0.0)): ob[k] = float(v)
    STATE['ctl'] = ob; return ob

def build(preset='GREY_DRIZZLE', clear=True):
    """Build the beach colony into the current scene (collections BEACH, BEACH_FX, LIGHTS), world sky, render settings, grade. Returns anchors."""
    scene = bpy.context.scene; P = dict(PRESETS[preset]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['objects'] = {}
    S.STATE.setdefault('P', {'bloom_size': 0.05})
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    SET = S._coll('BEACH', scene); FX = S._coll('BEACH_FX', scene); LIGHTS = S._coll('LIGHTS', scene)
    for c in (SET, FX, LIGHTS): S._wipe(c)
    for m in list(bpy.data.materials):
        if m.name.startswith('BEACH_'): bpy.data.materials.remove(m)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for li in list(bpy.data.lights):                         # review fix: every build leaked one orphan 'key_sun' light
        if li.users == 0 and li.name.startswith('key_sun'): bpy.data.lights.remove(li)
    STATE['tex'] = BT.ensure(verbose=False)
    _ctl(scene, FX)
    S.setup_render(scene, 'final'); build_world(scene); setup_render(scene, 'final')
    rng = random.Random(1938)
    M = dict(sand=mat_lit('sand', proc=sand_proc, pale=False, sat=False, form=False),
             roof_maroon=mat_lit('roof_maroon', image=STATE['tex']['roof_maroon'], pale=False), roof_slate=mat_lit('roof_slate', image=STATE['tex']['roof_slate'], pale=True))
    build_sand(SET, M)
    mb = S.MB(); mb.quad((-3000, SHORE_Y - 6.0, SEA_Z), (6000, 0, 0), (0, 3000, 0), mat_sea()); sea = _obj(mb, 'sea', SET, shadow=False)
    # cottages: a row along x facing the sea; the nearest (x = 3.5) is the yardstick
    cots = []; keys = list(BT.SCHEMES); xs = [-38.5 + 7.0 * i for i in range(16)]
    order = ['cream', 'red', 'blue', 'cedar', 'yellow', 'blue', 'cream', 'cedar', 'red', 'yellow', 'cream', 'blue', 'red', 'cedar', 'yellow', 'cream']
    for i, x in enumerate(xs):
        sc = 1.0 if abs(x - 3.5) < 1 else rng.uniform(0.94, 1.07)
        yb = -3.2 + (0.0 if abs(x - 3.5) < 1 else rng.uniform(-0.35, 0.35))
        cots.append(build_cottage(SET, M, order[i], x, yb, sc, seed=i, name='cottage_%02d' % i))
    poles, pole_h = build_poles(SET, M); bw = build_boardwalk(SET, M); fy = build_fence(SET, M); build_grass(SET, M, rng)
    umb = build_umbrella(SET); build_boat(SET); build_lifeguard_chair(SET); props = build_small_props(SET); build_far(SET)
    build_fog(FX); build_wave(FX); build_rain(FX)
    # key light
    K = P['K']; k = max(K); kd = Vector(P['key_dir']).normalized()
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in K); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIGHTS.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (0, 0, 30)
    STATE['sun'] = sun
    setup_grade(scene)
    set_fog_bank(0.0); set_wave(0.0); set_rain(0.0); set_sea(0.0); set_wind(0.0)
    A = anchors(cots, poles, pole_h, bw, fy, props); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """office3d.setup_render plus: 12 samples for 'final' (budget), 'preview' 360x640 6 samples 2 threads, long clip, 12 transparent bounces."""
    S.setup_render(scene, 'final' if quality == 'final' else 'preview')
    scene.cycles.transparent_max_bounces = 12; scene.render.use_persistent_data = False
    scene.cycles.seed = 0; scene.cycles.use_animated_seed = False
    if quality == 'final': scene.cycles.samples = 12
    else: scene.cycles.samples = 6
    if scene.world: scene.world.light_settings.distance = 0.001

def setup_grade(scene, bloom=True):
    """office grade (bloom above 1.0, plum CDL black point) with the preset's saturation (exteriors are already saturated)."""
    import warnings
    sys.path.insert(0, os.path.join(PROJ, 'spec')); import grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        ng = G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=0.5 if bloom else 0.0, bloom_size=0.05, saturation=STATE['P'].get('grade_sat', 1.12)))
    scene.render.use_compositing = True
    return ng

def make_camera(setup, name='cam', scene=None):
    cam = S.make_camera(setup, name=name, scene=scene); cam.data.clip_start = 0.05; cam.data.clip_end = 5000.0
    attach_rain(cam); return cam

# ----------------------------------------------------------------------------- animated controls
def _setkey(prop, value, frame):
    ctl = STATE['ctl']; ctl[prop] = float(value)
    if frame is not None:
        ctl.keyframe_insert('["%s"]' % prop, frame=frame); _linear(ctl)

def _linear(ob):
    ad = ob.animation_data
    if not ad or not ad.action: return
    try:
        fcs = list(ad.action.fcurves)
    except Exception:
        fcs = []
        for layer in ad.action.layers:
            for strip in layer.strips:
                cb = strip.channelbag(ad.action_slot)
                if cb: fcs += list(cb.fcurves)
    for fc in fcs:
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def set_fog_bank(amount, frame=None):
    """0 = clear horizon; 1 = a grey band about 30 D high on the horizon ring (radius FOG_R), opaque, soft top."""
    _setkey('fog', max(0.0, min(1.0, amount)), frame)

def set_wave(progress, frame=None):
    """0 = sunk below the sea at 440 D (behind the fog band); 1 = a 14 D wall of water with its toe at y = SHORE_Y + 3, crest above the cottages."""
    _setkey('wave', max(0.0, min(1.0, progress)), frame)

def set_rain(amount, frame=None):
    """0 = none (layers hidden); 1 = full drizzle/rain streaks in front of the camera."""
    _setkey('rain', max(0.0, min(1.5, amount)), frame)

def set_sea(t, frame=None):
    """t in seconds: surf line swash (two sines), swell streak drift, breaker lines moving shoreward. Key two frames for a linear drift."""
    _setkey('sea_t', t, frame)

def set_wind(amount, frame=None):
    """0 = calm; 1 = storm: grass leans onshore, umbrella tilts and shivers, flag flies and flaps, rain slants."""
    _setkey('wind', max(0.0, min(2.0, amount)), frame)

# ----------------------------------------------------------------------------- anchors
def anchors(cots, poles, pole_h, bw, fy, props):
    P = STATE['P']; kd = Vector(P['key_dir']).normalized()
    near = min(cots, key=lambda c: abs(c['center'][0] - 3.5))
    marks = dict(sand_a=(0.0, 7.6, 0.0), sand_b=(2.5, 8.4, 0.0), sand_c=(-2.2, 8.9, 0.0), sand_d=(4.4, 7.1, 0.0), surf_a=(-0.8, 11.6, 0.0), surf_b=(3.0, 11.9, 0.0),
                 road_a=(3.6, -7.2, 0.0), road_b=(0.6, -8.4, 0.0), boardwalk=(1.0, 3.85, bw['z']))
    cams = dict(
        vista_high=dict(loc=(-13.0, 8.2, 6.2), look_at=(30.0, 1.6, 0.6), lens=22),
        low_cottages=dict(loc=(5.4, -11.3, 0.85), look_at=(3.0, 0.0, 3.6), lens=22),
        eye_beach=dict(loc=(3.6, 13.2, 2.75), look_at=(1.0, 7.6, 2.15), lens=22),
        sea_view=dict(loc=(1.0, 4.4, 2.75), look_at=(1.0, 30.0, -1.5), lens=22),
        wave_low=dict(loc=(1.0, 6.4, 0.7), look_at=(1.0, 20.0, 9.5), lens=22),
        boardwalk_eye=dict(loc=(-7.0, 3.85, 2.85), look_at=(30.0, 3.4, 1.6), lens=22),
        surf_side=dict(loc=(-8.0, 12.6, 2.3), look_at=(30.0, 8.6, 0.6), lens=22),
    )
    notes = dict(
        vista_high='8.6 D high, pitched down about 11 degrees, down the colony toward +x: cottages, poles, boardwalk, fence and surf line run to one vanishing point; horizon near 0.37 H (like a/t58.5)',
        low_cottages='0.85 D above the sandy road behind the cottages, pitched up about 13 degrees: an actor at road_a looms near, the nearest cottage and the sky behind it fill the upper frame; the wave rises behind the roofs',
        eye_beach='eye level on the surf side looking back at the group at sand_a / sand_b (heads about 150 px), cottages, porches and poles behind them',
        sea_view='the group\'s point of view: sand, surf, open sea; horizon at 0.40 H, fog band and wave come in here',
        wave_low='0.7 D above the sand behind the group (seaward of the fence), pitched up 33 degrees past actors at surf_a / surf_b: at progress 1 the face, the lip and the foaming crest of the wave fill the frame above them',
        boardwalk_eye='eye level on the boardwalk looking down its length: planks, rails, poles and wires to the vanishing point',
        surf_side='along the surf line toward +x: wet sand, foam lines, the lifeguard chair and boat, the colony at right')
    return dict(
        beach_marks=[marks['sand_a'], marks['sand_b'], marks['sand_c'], marks['sand_d']], marks=marks,
        mark_notes=dict(sand='open beach between the fence and the surf, face the sea (+y) or the camera', surf='the swash zone (wet sand)', road='sandy road behind the cottages (low_cottages)', boardwalk='on the boardwalk deck, z = %.2f' % bw['z']),
        cottages=cots, nearest_cottage=near, cottage_ridge_nearest=near['ridge'],
        poles=poles, pole_height=pole_h, boardwalk=bw, fence_y=fy, props=props,
        shore_y=SHORE_Y, sea_z=SEA_Z, sea_dir=(0.0, 1.0, 0.0), horizon_dir=(0.0, 1.0, 0.0), shore_dir=(1.0, 0.0, 0.0),
        fog_radius=FOG_R, wave=dict(p0=wave_state(0.0), p033=wave_state(0.33), p066=wave_state(0.66), p1=wave_state(1.0)),
        key_dir=tuple(round(v, 4) for v in kd), preset=STATE['preset'], cams=cams, cam_notes=notes,
        render=dict(samples=12, resolution=(720, 1280), A=P['A'], A_pale=P['A_pale'], K=P['K'], sun_angle=P['sun_angle'], lift=P['lift']))

# ----------------------------------------------------------------------------- placeholder actors (stills, timing, review only)
_ACT = {}
POSES = dict(hero=dict(yaw=0.3, expr='determined', arm_l='down', arm_r='hip'), boss=dict(yaw=-0.4, expr='smug', arm_r='hip', arm_l='down'))

def stage_actors(cam, spots, frame=1, ppd=256):
    """two placeholder actors (stage.actors.Actor cards with shadow proxies) at two world points, posed for this camera."""
    from stage import actors, sprites
    sd = os.path.join(TMP, 'sprites')
    if not _ACT or any(a.root is None or a.root.name not in bpy.data.objects for a in _ACT.values()):
        actors.clear_registry(); _ACT.clear()
        for coll_ in (bpy.data.materials, bpy.data.images):    # review fix: orphans of the previous placeholder cards piled up on every rebuild
            for d_ in list(coll_):
                if d_.users == 0 and d_.name.startswith('ph_'): coll_.remove(d_)
        for nm in ('hero', 'boss'):
            a = actors.Actor('ph_' + nm, nm); a.build(sprites.DEFAULT_CANVAS[nm], sd, contact=True); S.no_bounce(a.card); _ACT[nm] = a
    kd = Vector(STATE['P']['key_dir']).normalized(); right = cam.matrix_world.to_3x3() @ Vector((1, 0, 0))
    flip = (-kd).dot(right) > 0                                # key from screen right -> thick ink side and crescent to the lower left
    for nm, p in zip(('hero', 'boss'), spots):
        a = _ACT[nm]
        if p is None: a.set_hidden(True); continue
        a.set_hidden(False); a.head_flip = flip; a.place(frame, p); a.pose(frame, dict(POSES[nm]), camera=cam); a.render_sprites(ppd, frames=[frame])
    actors.sync_all(bpy.context.scene, cam)
    return _ACT

def render_still(path):
    t0 = time.time(); c0 = time.process_time(); bpy.context.scene.render.filepath = path; bpy.ops.render.render(write_still=True)
    return time.time() - t0

STAGING = dict(vista_high=('sand_a', 'sand_b'), low_cottages=('road_a', 'road_b'), eye_beach=('sand_a', 'sand_b'), sea_view=('surf_a', 'surf_b'),
               wave_low=('surf_a', 'surf_b'), boardwalk_eye=('boardwalk', None), surf_side=('surf_a', 'sand_d'))
STATES = dict(SUMMER_SUN=dict(fog=0.0, wave=0.0, rain=0.0, wind=0.15, sea=2.0), GREY_DRIZZLE=dict(fog=0.25, wave=0.0, rain=0.3, wind=0.3, sea=2.0),
              STORM=dict(fog=1.0, wave=1.0, rain=1.0, wind=1.0, sea=2.0))

def apply_state(st):
    set_fog_bank(st['fog']); set_wave(st['wave']); set_rain(st['rain']); set_wind(st['wind']); set_sea(st['sea'])

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_stills(quality='final', presets=None, cams=None, outdir=None, strip=True, actors_on=True):
    outdir = outdir or HERE; os.makedirs(outdir, exist_ok=True); scene = bpy.context.scene
    for pr in (presets or ['SUMMER_SUN', 'GREY_DRIZZLE', 'STORM']):
        _ACT.clear(); A = build(pr); setup_render(scene, quality); apply_state(STATES[pr])
        for nm in (cams or ['vista_high', 'low_cottages', 'eye_beach', 'sea_view']):
            cam = make_camera(A['cams'][nm])
            if actors_on: stage_actors(cam, [A['marks'][k] if k else None for k in STAGING[nm]])
            w = render_still(os.path.join(outdir, 'still_%s_%s.png' % (pr, nm))); print('%s %s: %.1f s, load %s' % (pr, nm, w, _load()), flush=True)
    if strip: cli_strip(quality, outdir)

def cli_strip(quality='final', outdir=None):
    """set_fog_bank and set_wave at 0, 0.33, 0.66, 1: GREY_DRIZZLE sea_view (the fog comes in, the wave rises out of it) and STORM wave_low."""
    from PIL import Image
    outdir = outdir or HERE; scene = bpy.context.scene; tiles = []
    for pr, cn in (('GREY_DRIZZLE', 'sea_view'), ('STORM', 'wave_low')):
        _ACT.clear(); A = build(pr); setup_render(scene, quality); apply_state(STATES[pr]); cam = make_camera(A['cams'][cn])
        stage_actors(cam, [A['marks'][k] for k in STAGING[cn]])
        row = []
        for v in (0.0, 0.33, 0.66, 1.0):
            set_fog_bank(v); set_wave(v)
            p = os.path.join(TMP, 'strip_%s_%s_%03d.png' % (pr, cn, int(v * 100))); os.makedirs(TMP, exist_ok=True); render_still(p); row.append(p)
            print('strip %s %s %.2f' % (pr, cn, v), flush=True)
        tiles.append(row)
    W, H = 360, 640; img = Image.new('RGB', (W * 4, H * 2))
    for j, row in enumerate(tiles):
        for i, p in enumerate(row): img.paste(Image.open(p).convert('RGB').resize((W, H)), (i * W, j * H))
    img.save(os.path.join(outdir, 'still_strip_fog_wave.png')); print('wrote', os.path.join(outdir, 'still_strip_fog_wave.png'))

def cli_timing(n=4, presets=None):
    scene = bpy.context.scene; res = {}
    for pr in (presets or ['GREY_DRIZZLE', 'STORM', 'SUMMER_SUN']):
        _ACT.clear(); A = build(pr); setup_render(scene, 'final'); apply_state(dict(STATES[pr], rain=1.0, wave=0.7 if pr != 'STORM' else 1.0, fog=0.6 if pr != 'STORM' else 1.0))
        cs = dict(A['cams']['sea_view']); cam = make_camera(cs); stage_actors(cam, [A['marks']['surf_a'], A['marks']['surf_b']])
        print('%s: 720x1280, %d samples, %d threads, load before %s' % (pr, scene.cycles.samples, scene.render.threads, _load()), flush=True)
        ts = []
        for i in range(n):
            scene.frame_set(1 + i); cam.location.x += 0.02
            c0 = time.process_time(); w = render_still(os.path.join(TMP, 'timing_%s_%d.png' % (pr, i))); ts.append(w)
            print('  frame %d: %.2f s wall, %.2f s cpu, load %s' % (i, w, time.process_time() - c0, _load()), flush=True)
        ts2 = sorted(ts[1:]); res[pr] = (ts[0], ts2[len(ts2) // 2]); print('TIMING %s first %.2f s, following median %.2f s' % (pr, ts[0], ts2[len(ts2) // 2]), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'stills'; arg = sys.argv[2:]
    if cmd == 'stills': cli_stills(arg[0] if arg else 'final')
    elif cmd == 'timing': cli_timing()
    elif cmd == 'strip': cli_strip(arg[0] if arg else 'final')
    elif cmd == 'review':     # python3 beach3d.py review <outdir> [preset,..] [cam,..]  (preview quality, for the self-review loop)
        cli_stills('preview', presets=arg[1].split(',') if len(arg) > 1 else None, cams=arg[2].split(',') if len(arg) > 2 else None, outdir=arg[0], strip=False)
    else: print(__doc__)
