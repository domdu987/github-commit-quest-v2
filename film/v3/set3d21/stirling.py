"""film 21 set kit, "Stirling" (the Forth valley on a sunny morning, 11 Sept 1297). bpy 5.x, Cycles CPU. 1 unit = 1 m, Z up; a grown person = 1.7 units = 1 D.
Series light model (copied from the film 17 set): one hard warm key (sun) lights a matte Diffuse; the blue-violet ambient is injected as emission with a
per-surface shade multiplier, a navy lift and a (1 + N.form) sky term; no glossy, no depth of field, no readable text. Exteriors add distance haze.
Geography (x east, y north, water level z 0): the main river runs west to east through y 0 (38 m wide); the wooden bridge crosses it along x 0 (y -34..38);
north of it a river loop (a 30 m wide channel round a 80 m meadow, centre (0, 120)) leaves the main river at x -33 and rejoins it at x +33, so the
meadow is a bottle and the bridge + causeway its neck. Abbey Craig (the hill) rises north-east (185, 175); the English camp lies on the south bank
(y < -20); Stirling's castle rock is far south-west; the Ochil hills and a hazy ring close the valley. See API.md."""
import os, sys, math, random, contextlib, time, json
import numpy as np
import bpy, bmesh
from PIL import Image
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import stirling_tex as TX

D = 1.7
HEIGHT = {'scot': 1.70, 'wallace': 1.92, 'moray': 1.80, 'cressingham': 1.78, 'surrey': 1.66, 'knight': 1.78, 'foot': 1.68, 'archer': 1.66, 'squire': 1.55}
STATE = {'P': None, 'ink_t': 0.012, 'anim': {}, 'loc': None, 'preset': None, 'cam': (0, 0, 0)}
CACHE = os.path.join(HERE, 'cache'); os.makedirs(CACHE, exist_ok=True)
TERRAIN_V = 29

def hex_lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)
def hex_rgb(h): h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255.0
def lin_arr(c): c = np.asarray(c, float); return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

# ---------------------------------------------------------------- light preset (the series model, exterior morning)
LIGHTS = {
    'MORNING': dict(key=(2.35, 1.82, 0.98), sun_dir=(-0.646, 0.646, -0.407), sun_angle=0.9, shade=(0.17, 0.14, 0.40), tint=(0.135, 0.105, 0.29), mix=0.85,
                    lift=(0.010, 0.009, 0.032), form=(0.0, -0.05, 0.28), gain=1.0, ink='#2e1a26', haze='#a39cec', haze_d=(120.0, 1400.0), haze_max=0.25, sun_k=1.0),
}
SUN_STRENGTH = 3.94

# ---------------------------------------------------------------- materials
def _pal():
    pl = {}
    def add(k, col, **o):
        d = dict(col=col, tex=None, tile=1.0, tint=False, sm=(1, 1, 1), ink=False, gain=1.0, mix=None, afl=0.12, vc=False, detail=None, rot=0.0, haze=True)
        d.update(o); pl[k] = d
    wood = TX.wood('wood'); wooddk = TX.wood('wood_dk', seed=9, base='#5e4630'); meadow = TX.meadow('meadow')
    add('terrain', '#ffffff', vc=True, detail='terrain', sm=(0.8, 1.0, 1.15), afl=0.2, tex=meadow)
    add('terrain_far', '#ffffff', vc=True, sm=(0.8, 1.0, 1.15), afl=0.2)
    add('wood', '#8a6a45', tex=wood, tile=1.5, tint=True, ink=True, sm=(0.8, 1.0, 1.12))
    add('wood_dk', '#5e4630', tex=wooddk, tile=1.5, tint=True, ink=True, sm=(0.8, 1.0, 1.12))
    add('deck', '#8c6c48', tex=wood, tile=1.5, tint=True, ink=False, sm=(0.8, 1.0, 1.12), rot=90.0)
    add('rock', '#77737f', tint=True, ink=False, sm=(0.85, 0.98, 1.1), afl=0.15)
    add('rock_warm', '#85766d', tint=True, ink=False, sm=(0.85, 0.98, 1.1))
    add('heather', '#7a4f72', tint=True, sm=(0.6, 1.05, 1.0), afl=0.18)
    add('bracken', '#b0742f', tint=True, sm=(0.85, 1.0, 1.15))
    add('grass', '#6c9a3a', tint=True, sm=(0.75, 1.0, 1.15), afl=0.2)
    add('sprig', '#ffffff', tint=True, sm=(0.75, 1.0, 1.2), afl=0.22)
    add('gorse', '#566f2a', tint=True, sm=(0.75, 1.0, 1.15))
    add('gorse_fl', '#f3c61f', tint=True, mix=0.6, afl=0.5, sm=(1, 1, 1))
    add('pine_trunk', '#94603f', tint=True, ink=True, sm=(0.85, 1.0, 1.2))
    add('pine_leaf', '#2e5a4c', tint=True, sm=(0.7, 1.0, 1.3), afl=0.18)
    add('leaf', '#5f8c3a', tint=True, sm=(0.75, 1.0, 1.2), afl=0.2)
    add('bark', '#5a4234', tint=True, ink=True, sm=(0.85, 1.0, 1.15))
    add('reed', '#9aa84a', tint=True, sm=(0.75, 1.0, 1.15), afl=0.25)
    add('cattail', '#6b4128', tint=True)
    add('flower', '#f4e6a0', tint=True, mix=0.6, afl=0.5)
    # canvas, cloth, metal
    add('t_red', '#c8383a', tint=True, ink=True, sm=(0.95, 0.9, 1.18), mix=0.8)
    add('t_cream', '#efe2bb', tint=True, ink=True, sm=(0.85, 0.95, 1.18), mix=0.8)
    add('t_blue', '#2f58ad', tint=True, ink=True, sm=(0.85, 0.95, 1.2), mix=0.8)
    add('t_saltire', '#153d9c', tint=True, ink=True, sm=(0.85, 0.95, 1.2), mix=0.8)
    add('t_gold', '#dcae3a', tint=True, ink=True, sm=(0.9, 0.95, 1.2), mix=0.8)
    add('t_green', '#3f7d4c', tint=True, ink=True, mix=0.8)
    add('t_brown', '#7a5a3a', tint=True, ink=True)
    add('t_white', '#f2ece0', tint=True, ink=True, mix=0.7)
    add('t_dark', '#3b3346', tint=True, ink=True, mix=0.7)
    add('rope', '#b59b6a', tint=True, mix=0.5)
    add('iron', '#474b5e', tint=True, ink=True, mix=0.5)
    add('steel', '#9aa6bf', tint=True, ink=True, mix=0.5)
    add('gold', '#e4b43d', tint=True, ink=True, mix=0.45, afl=0.4)
    add('silver', '#cfd5e2', tint=True, ink=False, mix=0.5, afl=0.4)
    add('cloth_red', '#8c2c34', tint=True, ink=True, mix=0.8)
    add('leather', '#6a3b22', tint=True, ink=True)
    add('cream', '#e5d3a2', tint=True, mix=0.5)
    add('barrel', '#8b5a30', tint=True, ink=True, sm=(0.85, 1.0, 1.12))
    add('sack', '#c8b186', tint=True, ink=True)
    add('stone', '#9d9aa2', tint=True, ink=True, mix=0.8)
    add('castle', '#b9aea4', tint=True, ink=True, mix=0.8)
    add('thatch', '#b8923e', tint=True, ink=True)
    add('hay', '#d1b050', tint=True)
    add('horse', '#7a4a2c', tint=True, ink=True, sm=(0.9, 0.95, 1.2))
    add('horse_dk', '#3a3036', tint=True, ink=True)
    add('mane', '#2e2530', tint=True)
    add('smoke', '#d8cfc8', mix=0.9, afl=0.7, haze=True)
    add('dirt', '#a98b60', tint=True, sm=(0.8, 1.0, 1.15))
    add('foam', '#f1f5f0', tint=True, mix=0.8, afl=0.5, sm=(0.85, 1.0, 1.15), haze=True)
    add('flame', '#ffb23a', mix=1.0, afl=1.0)
    add('glass', '#7fa6a8', mix=0.6)
    return pl
_MATS = {}
def get_mat(key):
    if key in _MATS: return _MATS[key]
    if key.startswith('glow'): m = _glow_mat(key)
    elif key == 'smoke': m = _glow_mat('glow_smoke')
    elif key == 'ink_hull': m = _ink_mat()
    elif key == 'sky': m = _sky_mat()
    elif key == 'water': m = _water_mat()
    elif key.startswith('ph_'): m = _ph_mat(key)
    elif key == 'flame': m = _glow_mat('glow_flame')
    else: m = _lit_mat(key, STATE['PAL'][key])
    _MATS[key] = m; return m
def _mk_tree(m):
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt
def _vs(nt, vec, scal):
    """vector * scalar (socket or float)"""
    n = nt.nodes.new('ShaderNodeVectorMath'); n.operation = 'SCALE'; nt.links.new(vec, n.inputs[0]) if not isinstance(vec, tuple) else None
    if isinstance(vec, tuple): n.inputs[0].default_value = vec
    if isinstance(scal, (int, float)): n.inputs['Scale'].default_value = scal
    else: nt.links.new(scal, n.inputs['Scale'])
    return n.outputs['Vector']
def _vadd(nt, a, b):
    n = nt.nodes.new('ShaderNodeVectorMath'); n.operation = 'ADD'
    for i, x in enumerate((a, b)):
        if isinstance(x, tuple): n.inputs[i].default_value = x
        else: nt.links.new(x, n.inputs[i])
    return n.outputs['Vector']
def _haze_out(nt, shader):
    """mix the surface shader toward the haze colour with the camera distance (aerial perspective)."""
    P = STATE['P']; N = nt.nodes.new; L = nt.links.new
    cd = N('ShaderNodeCameraData'); mr = N('ShaderNodeMapRange'); mr.clamp = True; mr.inputs['From Min'].default_value = P['haze_d'][0]; mr.inputs['From Max'].default_value = P['haze_d'][1]
    mr.inputs['To Min'].default_value = 0.0; mr.inputs['To Max'].default_value = P['haze_max']; L(cd.outputs['View Distance'], mr.inputs['Value'])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*hex_lin(P['haze']), 1); em.inputs['Strength'].default_value = 1.0
    mx = N('ShaderNodeMixShader'); L(mr.outputs['Result'], mx.inputs['Fac']); L(shader, mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2]); return mx.outputs['Shader']
def _lit_core(nt, art, s, geo=None):
    """Diffuse(art) lit by the sun + Emission(ambient shade): the series light model. art = colour socket."""
    P = STATE['P']; N = nt.nodes.new; L = nt.links.new
    geo = geo or N('ShaderNodeNewGeometry'); bw = N('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
    dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 1.0
    gk = _vs(nt, art, P['gain']); L(gk, dif.inputs['Color'])
    mix = P['mix'] if s['mix'] is None else s['mix']; sm = s['sm']; smm = sum(sm) / 3.0
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0; L(art, ms.inputs[6]); ms.inputs[7].default_value = (*[a * b for a, b in zip(P['shade'], sm)], 1)
    sa = _vs(nt, ms.outputs[2], 1.0 - mix)
    lm = N('ShaderNodeMath'); lm.operation = 'MULTIPLY_ADD'; lm.inputs[1].default_value = 1.0 - s['afl']; lm.inputs[2].default_value = s['afl']; L(bw.outputs[0], lm.inputs[0])
    tb = _vs(nt, tuple(x * mix * smm for x in P['tint']), lm.outputs[0])
    amb = _vadd(nt, _vadd(nt, sa, tb), tuple(P['lift']))
    fd = N('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(P['form']); L(geo.outputs['Normal'], fd.inputs[0])
    fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
    amb = _vs(nt, amb, fa.outputs[0]); em = N('ShaderNodeEmission'); L(amb, em.inputs['Color']); em.inputs['Strength'].default_value = 1.0
    ad = N('ShaderNodeAddShader'); L(dif.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1]); return ad.outputs['Shader']
def _lit_mat(key, s):
    m = bpy.data.materials.new(key); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new; out = N('ShaderNodeOutputMaterial')
    geo = N('ShaderNodeNewGeometry')
    if s['vc']:
        at = N('ShaderNodeAttribute'); at.attribute_name = 'col'; at.attribute_type = 'GEOMETRY'; art = at.outputs['Color']
        if s['detail'] == 'terrain':
            tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 3.0, 1 / 3.0, 1 / 3.0); L(tc.outputs['Object'], mp.inputs[0])
            it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(s['tex'], check_existing=True); it.image.colorspace_settings.name = 'Non-Color'; it.interpolation = 'Linear'; L(mp.outputs[0], it.inputs[0])
            nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.11; nz.inputs['Detail'].default_value = 1.0; L(tc.outputs['Object'], nz.inputs['Vector'])
            cr = N('ShaderNodeValToRGB'); cr.color_ramp.interpolation = 'CONSTANT'; cr.color_ramp.elements[0].color = (0.93, 0.93, 0.93, 1)
            e1 = cr.color_ramp.elements.new(0.42); e1.color = (1.0, 1.0, 1.0, 1); e2 = cr.color_ramp.elements.new(0.62); e2.color = (1.05, 1.05, 1.05, 1); L(nz.outputs['Fac'], cr.inputs[0])
            cd = N('ShaderNodeCameraData'); fd_ = N('ShaderNodeMapRange'); fd_.clamp = True; fd_.inputs['From Min'].default_value = 30.0; fd_.inputs['From Max'].default_value = 130.0; fd_.inputs['To Min'].default_value = 1.0; fd_.inputs['To Max'].default_value = 0.0
            L(cd.outputs['View Distance'], fd_.inputs['Value'])
            bwt = N('ShaderNodeRGBToBW'); L(it.outputs['Color'], bwt.inputs[0])
            amt = N('ShaderNodeMath'); amt.operation = 'MULTIPLY'; amt.inputs[1].default_value = 1.25; L(fd_.outputs['Result'], amt.inputs[0])
            sub = N('ShaderNodeMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = 0.5; L(bwt.outputs[0], sub.inputs[0])
            mm = N('ShaderNodeMath'); mm.operation = 'MULTIPLY'; L(sub.outputs[0], mm.inputs[0]); L(amt.outputs[0], mm.inputs[1])
            ad1 = N('ShaderNodeMath'); ad1.operation = 'ADD'; ad1.inputs[1].default_value = 1.0; L(mm.outputs[0], ad1.inputs[0])
            pf = N('ShaderNodeMath'); pf.operation = 'MULTIPLY'; L(ad1.outputs[0], pf.inputs[0]); pcol = N('ShaderNodeRGBToBW'); L(cr.outputs['Color'], pcol.inputs[0]); L(pcol.outputs[0], pf.inputs[1])
            art = _vs(nt, art, pf.outputs[0])
    elif s['tex']:
        it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(s['tex'], check_existing=True); it.interpolation = 'Linear'; it.projection = 'BOX'; it.projection_blend = 0.2
        tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); k = 1.0 / s['tile']; mp.inputs['Scale'].default_value = (k, k, k); mp.inputs['Rotation'].default_value = (0, 0, math.radians(s['rot']))
        L(tc.outputs['Object'], mp.inputs[0]); L(mp.outputs[0], it.inputs[0]); art = it.outputs['Color']
    else:
        rgb = N('ShaderNodeRGB'); rgb.outputs[0].default_value = (*hex_lin(s['col']), 1); art = rgb.outputs[0]
    if s['tint']:
        at = N('ShaderNodeAttribute'); at.attribute_name = 'tint'; at.attribute_type = 'GEOMETRY'
        mt = N('ShaderNodeMix'); mt.data_type = 'RGBA'; mt.blend_type = 'MULTIPLY'; mt.inputs[0].default_value = 1; L(art, mt.inputs[6]); L(at.outputs['Color'], mt.inputs[7]); art = mt.outputs[2]
    sh = _lit_core(nt, art, s, geo)
    if s['haze']: sh = _haze_out(nt, sh)
    L(sh, out.inputs['Surface']); return m
def _glow_mat(key):
    spec = {'glow_flame': ('#ffb040', 6.0), 'glow_ember': ('#ff8a30', 4.0), 'glow_sun': ('#fff2cc', 6.0), 'glow_smoke': ('#cdbfc0', 0.85), 'glow_spray': ('#f6f8fb', 1.0), 'glow_spray2': ('#f2f6fa', 1.0)}[key]
    m = bpy.data.materials.new(key); nt = _mk_tree(m); out = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); e.name = 'strength'
    e.inputs[0].default_value = (*hex_lin(spec[0]), 1); e.inputs[1].default_value = spec[1]; nt.links.new(e.outputs[0], out.inputs[0]); return m
def _ink_mat():
    P = STATE['P']; m = bpy.data.materials.new('ink_hull'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); lp = N('ShaderNodeLightPath'); emi = N('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(P['ink']), 1)
    tr = N('ShaderNodeBsdfTransparent'); mix = N('ShaderNodeMixShader'); notcam = N('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = N('ShaderNodeMath'); fac.operation = 'MAXIMUM'; L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    return m
def _sky_mat():
    """painted equirect sky (drawn clouds): direction of the dome point -> u = azimuth / 360, v = (elevation + 15) / 105."""
    path = TX.sky('sky'); m = bpy.data.materials.new('sky'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tc = N('ShaderNodeTexCoord'); nm = N('ShaderNodeVectorMath'); nm.operation = 'NORMALIZE'; L(tc.outputs['Object'], nm.inputs[0])
    sp = N('ShaderNodeSeparateXYZ'); L(nm.outputs[0], sp.inputs[0])
    at = N('ShaderNodeMath'); at.operation = 'ARCTAN2'; L(sp.outputs['Y'], at.inputs[0]); L(sp.outputs['X'], at.inputs[1])
    u = N('ShaderNodeMath'); u.operation = 'MULTIPLY_ADD'; u.inputs[1].default_value = 1.0 / (2 * math.pi); u.inputs[2].default_value = 0.0; L(at.outputs[0], u.inputs[0])
    uw = N('ShaderNodeMath'); uw.operation = 'WRAP'; uw.inputs[1].default_value = 1.0; uw.inputs[2].default_value = 0.0; L(u.outputs[0], uw.inputs[0])
    asn = N('ShaderNodeMath'); asn.operation = 'ARCSINE'; L(sp.outputs['Z'], asn.inputs[0])
    v = N('ShaderNodeMath'); v.operation = 'MULTIPLY_ADD'; v.inputs[1].default_value = 1.0 / math.radians(105.0); v.inputs[2].default_value = 15.0 / 105.0; L(asn.outputs[0], v.inputs[0])
    cb = N('ShaderNodeCombineXYZ'); L(uw.outputs[0], cb.inputs['X']); L(v.outputs[0], cb.inputs['Y'])
    it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(path, check_existing=True); it.interpolation = 'Linear'; it.extension = 'EXTEND'; L(cb.outputs[0], it.inputs[0])
    e = N('ShaderNodeEmission'); L(it.outputs['Color'], e.inputs[0]); e.inputs[1].default_value = 1.0; L(e.outputs[0], out.inputs[0]); return m
PH_COL = {'scot': '#6e5a3c', 'wallace': '#5a4a34', 'moray': '#3f6a4a', 'cressingham': '#b03a38', 'surrey': '#34548e', 'knight': '#b8323a', 'knight_b': '#2f56a8', 'knight_g': '#d9a93a',
          'foot': '#9a8c70', 'foot_r': '#a84a40', 'archer': '#3f6a4a', 'squire': '#6a5a7a', 'scot_b': '#8c4a30', 'scot_o': '#b08a3c', 'scot_m': '#5a6a3a'}
def _ph_mat(key):
    hexc = '#fef7f6' if key == 'ph_head' else '#4a2a4a' if key == 'ph_ring' else PH_COL[key[3:]]
    m = bpy.data.materials.new(key); nt = _mk_tree(m); e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*hex_lin(hexc), 1); o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); return m

# ---------------------------------------------------------------- batched geometry (copied from the film 17 kit)
def rotm(rx=0, ry=0, rz=0):
    a, b, c = map(math.radians, (rx, ry, rz)); ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    Rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]]); Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]]); Rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def _m4(loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
    m = np.eye(4); m[:3, :3] = rotm(*rot) * scale; m[:3, 3] = loc; return m
_CUBE_F = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
_ICO = None
def _ico():
    global _ICO
    if _ICO: return _ICO
    t = (1 + 5 ** 0.5) / 2; v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
         (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    v = [tuple(np.array(p) / np.linalg.norm(p)) for p in v]; cache = {}; nf = []
    def mid(a, b):
        k = (min(a, b), max(a, b))
        if k not in cache: p = (np.array(v[a]) + np.array(v[b])) / 2; v.append(tuple(p / np.linalg.norm(p))); cache[k] = len(v) - 1
        return cache[k]
    for a, b, c in f: ab, bc, ca = mid(a, b), mid(b, c), mid(c, a); nf += [(a, ab, ca), (b, bc, ab), (c, ca, bc), (ab, bc, ca)]
    _ICO = (np.array(v), nf); return _ICO
class Batch:
    """accumulates boxes / cylinders / spheres / meshes per material; finalize() makes one Blender object per material (plus its ink hull)."""
    def __init__(self, seed=5): self.d = {}; self.stack = [np.eye(4)]; self.rng = random.Random(seed)
    @contextlib.contextmanager
    def xf(self, loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
        self.stack.append(self.stack[-1] @ _m4(loc, rot, scale))
        try: yield
        finally: self.stack.pop()
    def wpt(self, p): return tuple(self.stack[-1][:3, :3] @ np.array(p, float) + self.stack[-1][:3, 3])
    def _put(self, mat, v, faces, smooth, tint):
        v = np.asarray(v, float); v = (self.stack[-1][:3, :3] @ v.T).T + self.stack[-1][:3, 3]
        Dd = self.d.setdefault(mat, dict(v=[], f=[], s=[], t=[], n=0))
        Dd['f'] += [tuple(i + Dd['n'] for i in f) for f in faces]; Dd['s'] += [smooth] * len(faces); Dd['v'].append(v); Dd['n'] += len(v)
        t = tint if isinstance(tint, (tuple, list)) else (tint, tint, tint); Dd['t'].append(np.tile(np.array([*t, 1.0]), (len(v), 1)))
    def box(self, mat, c, s, rot=(0, 0, 0), tint=1.0):
        h = np.array(s, float) / 2; u = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]], float) * h
        self._put(mat, (rotm(*rot) @ u.T).T + np.array(c), _CUBE_F, False, tint)
    def cyl(self, mat, c, r, h, axis='z', r2=None, seg=16, rot=(0, 0, 0), tint=1.0, smooth=True, caps=True):
        r2 = r if r2 is None else r2; a = np.linspace(0, 2 * math.pi, seg, endpoint=False); R = {'z': (0, 0, 0), 'x': (0, 90, 0), 'y': (90, 0, 0)}[axis]
        lo = np.stack([r * np.cos(a), r * np.sin(a), -h / 2 * np.ones(seg)], 1); hi = np.stack([r2 * np.cos(a), r2 * np.sin(a), h / 2 * np.ones(seg)], 1)
        v = np.concatenate([lo, hi]); f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]; Rm = rotm(*rot) @ rotm(*R)
        self._put(mat, (Rm @ v.T).T + np.array(c), f, smooth, tint)
        if caps:
            for z, rr, rev in ((-h / 2, r, True), (h / 2, r2, False)):
                if rr <= 0: continue
                cv = np.concatenate([np.stack([rr * np.cos(a), rr * np.sin(a), z * np.ones(seg)], 1), [[0, 0, z]]])
                ff = [(i, (i + 1) % seg, seg) for i in range(seg)]; ff = [(b_, a_, c_) for a_, b_, c_ in ff] if rev else ff
                self._put(mat, (Rm @ cv.T).T + np.array(c), ff, False, tint)
    def sphere(self, mat, c, r, seg=14, rings=8, scale=(1, 1, 1), tint=1.0, rot=(0, 0, 0)):
        v = [(0, 0, -1)]
        for j in range(1, rings):
            p = -math.pi / 2 + math.pi * j / rings
            for i in range(seg): a = 2 * math.pi * i / seg; v.append((math.cos(p) * math.cos(a), math.cos(p) * math.sin(a), math.sin(p)))
        v.append((0, 0, 1)); f = []
        for i in range(seg): f.append((0, 1 + (i + 1) % seg, 1 + i))
        for j in range(rings - 2):
            for i in range(seg): a = 1 + j * seg + i; b = 1 + j * seg + (i + 1) % seg; f.append((a, b, b + seg, a + seg))
        top = len(v) - 1
        for i in range(seg): f.append((top, 1 + (rings - 2) * seg + i, 1 + (rings - 2) * seg + (i + 1) % seg))
        V = (rotm(*rot) @ (np.array(v) * np.array(scale) * r).T).T + np.array(c); self._put(mat, V, [tuple(x) for x in f], True, tint)
    def rock(self, mat, c, size, seed=0, tint=1.0, rot=(0, 0, 0), flat=0.7, jag=0.30):
        """faceted boulder: icosphere (80 faces) with seeded radial jitter, flat shaded, sunk flat bottom."""
        v, f = _ico(); r = np.random.RandomState(seed); k = 1 + jag * (r.rand(len(v)) - 0.5) * 2; V = v * k[:, None]; V = V * np.array(size) / 2.0
        V[:, 2] = np.where(V[:, 2] < 0, V[:, 2] * flat, V[:, 2]); V = (rotm(*rot) @ V.T).T + np.array(c); self._put(mat, V, f, False, tint)
    def mesh(self, mat, v, faces, smooth=True, tint=1.0): self._put(mat, v, faces, smooth, tint)
    def quad(self, mat, p0, p1, p2, p3, tint=1.0): self._put(mat, [p0, p1, p2, p3], [(0, 1, 2, 3)], False, tint)
    def tri(self, mat, p0, p1, p2, tint=1.0): self._put(mat, [p0, p1, p2], [(0, 1, 2)], False, tint)
    def prism_roof(self, mat, c, w, d, h, rot_z=0, ridge_frac=1.0, tint=1.0):
        hw, hd = w / 2, d / 2; rl = hw * ridge_frac
        v = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0), (-rl, 0, h), (rl, 0, h)]
        f = [(0, 1, 5, 4), (2, 3, 4, 5), (3, 0, 4), (1, 2, 5), (3, 2, 1, 0)]
        with self.xf(c, (0, 0, rot_z)): self._put(mat, v, f, False, tint)
    def finalize(self, prefix='set', loc=(0, 0, 0), parent=None, ink=True, ink_t=None, shadow=True):
        objs = []; coll = bpy.context.scene.collection
        for key, Dd in self.d.items():
            V = np.concatenate(Dd['v']); me = bpy.data.meshes.new('%s_%s' % (prefix, key)); me.from_pydata(V.tolist(), [], Dd['f']); me.update()
            me.polygons.foreach_set('use_smooth', Dd['s'])
            bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
            ca = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.concatenate(Dd['t']).ravel())
            ob = bpy.data.objects.new('%s_%s' % (prefix, key), me); coll.objects.link(ob); ob.location = loc; ob.data.materials.append(get_mat(key))
            if parent is not None: ob.parent = parent
            if key.startswith('glow') or key in ('sky', 'flame', 'water', 'smoke'): ob.visible_shadow = False
            if key in ('sky',): ob.visible_diffuse = ob.visible_glossy = False
            if not shadow: ob.visible_shadow = False
            objs.append(ob)
            it_ = STATE['ink_t'] if ink_t is None else ink_t
            if ink and key in STATE['PAL'] and STATE['PAL'][key]['ink'] and it_ > 0: add_hull(ob, it_)
        self.d = {}; return objs
def add_hull(ob, t):
    ob.data.materials.append(get_mat('ink_hull'))
    md = ob.modifiers.new('ink', 'SOLIDIFY'); md.thickness = t; md.offset = 1.0; md.use_flip_normals = True; md.use_rim = False; md.use_even_offset = True
    md.material_offset = len(ob.data.materials) - 1; return ob

# ---------------------------------------------------------------- scene, lights, camera
def new_scene(light='MORNING', over=None):
    bpy.ops.wm.read_factory_settings(use_empty=True); _MATS.clear(); STATE['anim'] = {}
    for im in list(bpy.data.images): bpy.data.images.remove(im)
    STATE['P'] = dict(LIGHTS[light], **(over or {})); STATE['light'] = light; STATE['PAL'] = _pal(); P = STATE['P']
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (0.30, 0.40, 0.62, 1); bg.inputs[1].default_value = P.get('world', 0.3)
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0; sc.render.film_transparent = False
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 0; sc.cycles.transmission_bounces = 0; sc.cycles.transparent_max_bounces = 12
    sc.cycles.sample_clamp_indirect = 8.0; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
    sc.render.fps = 30; return sc
def sun(strength=None):
    P = STATE['P']; k = np.array(P['key']); s = float(k.max()); d = bpy.data.lights.new('key', 'SUN'); d.energy = SUN_STRENGTH * s * (strength or 1.0) * P.get('sun_k', 1.0); d.color = tuple(k / s); d.angle = math.radians(P['sun_angle'])
    ob = bpy.data.objects.new('key', d); bpy.context.scene.collection.objects.link(ob); ob.rotation_euler = Vector(P['sun_dir']).normalized().to_track_quat('-Z', 'Y').to_euler(); return ob
def camera(loc, target, lens=22.0, roll=0.0):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'AUTO'; c.dof.use_dof = False; c.clip_end = 9000; c.clip_start = 0.1
    ob = bpy.data.objects.new('cam', c); bpy.context.scene.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); bpy.context.scene.camera = ob; return ob
def sky_dome(radius=6000.0):
    b = Batch(); b.sphere('sky', (0, 0, 0), radius, seg=48, rings=24); return b.finalize('sky', ink=False)

# ================================================================ TERRAIN: analytic fields (river sdf, hills, colours)
def vnoise(x, y, seed=0):
    xi = np.floor(x); yi = np.floor(y); xf = x - xi; yf = y - yi
    def h(ix, iy): s = np.sin(ix * 127.1 + iy * 311.7 + seed * 74.7) * 43758.5453; return s - np.floor(s)
    u = xf * xf * (3 - 2 * xf); v = yf * yf * (3 - 2 * yf)
    a = h(xi, yi); b = h(xi + 1, yi); c = h(xi, yi + 1); d = h(xi + 1, yi + 1)
    return (a + (b - a) * u) * (1 - v) + (c + (d - c) * u) * v
def fbm(x, y, seed=0, octs=3):
    t = 0; a = 1.0; tot = 0
    for o in range(octs): t = t + a * vnoise(x * 2 ** o, y * 2 ** o, seed + o * 17); tot += a; a *= 0.5
    return t / tot
def smooth(e0, e1, x): t = np.clip((x - e0) / (e1 - e0), 0, 1); return t * t * (3 - 2 * t)
def spline(pts, widths, step=1.5):
    pts = np.array(pts, float); P = np.vstack([2 * pts[0] - pts[1], pts, 2 * pts[-1] - pts[-2]]); out = []; ws = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]; n = max(2, int(np.linalg.norm(p2 - p1) / step)); t = np.linspace(0, 1, n, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3)); ws.append(widths[i - 1] + (widths[i] - widths[i - 1]) * t[:, 0])
    out.append(pts[-1][None]); ws.append(np.array([widths[-1]])); return np.vstack(out), np.concatenate(ws)
BRIDGE_X = 0.0; BRIDGE_Y0, BRIDGE_Y1 = -34.0, 38.0; DECK_Z = 1.75
LOOP_C = (0.0, 120.0); LOOP_R = 95.0; HALF_W_MAIN = 19.0; HALF_W_LOOP = 15.0; WATER_EDGE = 1.2
HILL_C = (200.0, 190.0); HILL_A = 72.0; CAMP_C = (0.0, -58.0); CASTLE_C = (-330.0, -480.0); SHELF = (131.0, 131.0, 15.0); PAD = (158.0, 148.0, 4.5, 44.0); PAD2 = (137.0, 137.0, 13.0, 19.0)         # the Scots' ledge under the hill_over lens
_RIVER = {}
def river():
    if _RIVER: return _RIVER
    main_pts = [(-1400, -160), (-900, -95), (-520, -40), (-330, 12), (-215, -10), (-110, 10), (-33, 0), (0, 0), (33, 0), (100, -12), (190, -34), (290, -12), (520, 36), (900, 80), (1400, 150)]
    main_w = [30, 34, 40, 46, 40, 36, 38, 38, 38, 42, 46, 40, 40, 34, 30]
    mp, mw = spline(main_pts, main_w, 1.5)
    # the loop: a pear / egg shaped meander that narrows smoothly into the neck at the bridge (no circle, no right angles), channel width varying +-20 %
    ring = [(-33.0, 0.0), (-31.0, 16.0), (-37.0, 36.0), (-52.0, 58.0), (-70.0, 82.0), (-82.0, 108.0), (-86.0, 134.0), (-78.0, 160.0), (-60.0, 184.0), (-34.0, 203.0), (-2.0, 210.0),
            (30.0, 203.0), (58.0, 190.0), (76.0, 168.0), (84.0, 142.0), (82.0, 114.0), (72.0, 88.0), (56.0, 62.0), (40.0, 38.0), (32.0, 18.0), (33.0, 0.0)]
    rwid = [30, 28, 26, 28, 31, 35, 33, 30, 27, 25, 26, 28, 31, 34, 31, 27, 28, 30, 32, 30, 30]
    rp, rw = spline(ring, rwid, 1.5)
    def arcs(p): d = np.r_[0, np.cumsum(np.hypot(*np.diff(p, axis=0).T))]; return d
    _RIVER.update(main=(mp, mw, arcs(mp)), ring=(rp, rw, arcs(rp)))
    return _RIVER
def river_query(X, Y):
    """sd (distance to the waterline circle: < 0 in the channel; = distance to the centreline minus half the width), s (arc length along the nearest centreline),
    t (signed lateral offset), flow (dx, dy) of the nearest centreline."""
    R = river(); shp = X.shape; xf = X.ravel(); yf = Y.ravel(); n = len(xf)
    best = np.full(n, 1e9); bs = np.zeros(n); bt = np.zeros(n); bfx = np.zeros(n); bfy = np.zeros(n)
    for name in ('main', 'ring'):
        p, w, s = R[name]; tang = np.gradient(p, axis=0); tang /= np.linalg.norm(tang, axis=1)[:, None] + 1e-9
        for i0 in range(0, n, 3000):
            sl = slice(i0, min(n, i0 + 3000)); xs = xf[sl]; ys = yf[sl]; ar = np.arange(len(xs))
            dx = xs[:, None] - p[None, :, 0]; dy = ys[:, None] - p[None, :, 1]; d2 = dx * dx + dy * dy; j = np.argmin(d2, axis=1); dm = np.sqrt(d2[ar, j]); sdp = dm - w[j] / 2.0
            upd = sdp < best[sl]; tj = tang[j]; tt = tj[:, 0] * dy[ar, j] - tj[:, 1] * dx[ar, j]
            best[sl] = np.where(upd, sdp, best[sl]); bs[sl] = np.where(upd, s[j], bs[sl]); bt[sl] = np.where(upd, tt, bt[sl]); bfx[sl] = np.where(upd, tj[:, 0], bfx[sl]); bfy[sl] = np.where(upd, tj[:, 1], bfy[sl])
    r = lambda a: a.reshape(shp); return r(best), r(bs), r(bt), r(bfx), r(bfy)
def _hill_raw(X, Y, C, A, Ru, Rv, ang, expo=1.3):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang)); u = (X - C[0]) * c + (Y - C[1]) * s; v = -(X - C[0]) * s + (Y - C[1]) * c
    r2 = (u / Ru) ** 2 + (v / Rv) ** 2; return A * np.clip(1 - r2, 0, 1) ** expo, r2, u, v
def hill_h(X, Y):
    """Abbey Craig: a whaleback of crag and tail. Terraced crags (stairs) on the steep north-west face and the summit."""
    h, r2, u, v = _hill_raw(X, Y, HILL_C, HILL_A, 105.0, 78.0, 35.0)
    n = fbm(X / 28.0, Y / 28.0, 11, 3); h = h * (0.88 + 0.24 * n)
    st = 5.5 * (np.floor(h / 5.5) + smooth(0.55, 0.82, h / 5.5 - np.floor(h / 5.5)))
    cm = smooth(0.3, 0.7, np.clip(-((X - HILL_C[0]) * 0.86 + (Y - HILL_C[1]) * 0.51) / 80.0 + 0.3 * n + 0.1, 0, 1)) * smooth(8, 22, h)
    h = h * (1 - cm) + st * cm
    dx, dy = X - SHELF[0], Y - SHELF[1]; al = (dx - dy) / 1.4142; ac = (dx + dy) / 1.4142; sh = np.exp(-(((al / 30.0) ** 2 + (ac / 13.0) ** 2)) ** 1.6)
    h = h * (1 - sh) + SHELF[2] * sh
    pd = smooth(PAD[2] + 9.0, PAD[2], np.hypot(X - PAD[0], Y - PAD[1])); h = h * (1 - pd) + PAD[3] * pd
    p2 = smooth(PAD2[2] + 8.0, PAD2[2], np.hypot(X - PAD2[0], Y - PAD2[1])); return h * (1 - p2) + PAD2[3] * p2, cm
def castle_h(X, Y):
    """Stirling's castle rock: a steep crag with a flat top, sheer on the west and north faces."""
    h, r2, u, v = _hill_raw(X, Y, CASTLE_C, 52.0, 52.0, 31.0, 20.0, 0.38)
    n = fbm(X / 14.0, Y / 14.0, 5, 3); h = h * (0.92 + 0.16 * n); st = 8 * (np.floor(h / 8) + smooth(0.45, 0.75, h / 8 - np.floor(h / 8)))
    return h * 0.45 + st * 0.55
def land_height(X, Y, sdr):
    n_big = fbm(X / 150.0, Y / 150.0, 3, 3) - 0.5; n_small = fbm(X / 24.0, Y / 24.0, 5, 3) - 0.5
    base = 1.0 + 1.3 * n_big + 0.45 * n_small
    dm = np.hypot(X - LOOP_C[0], Y - LOOP_C[1]); fl = smooth(LOOP_R - 12, LOOP_R - 50, dm)          # the bottle meadow is flat
    base = base * (1 - fl) + (1.1 + 0.14 * n_small) * fl
    hh, cm = hill_h(X, Y)
    base = base + hh + castle_h(X, Y) + far_fields(X, Y) * smooth(15.0, 300.0, sdr)
    cause = 0.45 * (1 - smooth(5.0, 11.0, np.abs(X - BRIDGE_X))) * (smooth(-62, -36, Y) * (1 - smooth(-24, -17, Y)) + smooth(17, 24, Y) * (1 - smooth(62, 84, Y)))
    return base + cause, hh, cm
def fields(X, Y, full=True):
    """z, art colour (sRGB 0-1), sd, s, t, flow for arrays X, Y."""
    sd, s, t, fx, fy = river_query(X, Y); Lh, hh, cm = land_height(X, Y, sd)
    u = smooth(-6.0, 2.0, sd); z = -1.7 + (Lh + 1.7) * u
    return z, sd, s, t, fx, fy, hh, cm, Lh
def camp_tramp(X, Y):
    cx, cy = CAMP_C; return smooth(1.0, 0.4, np.hypot((X - cx) / 125.0, (Y - cy) / 40.0))
FARMS = [(-150.0, -105.0), (118.0, -118.0), (-205.0, 72.0), (215.0, -40.0), (-135.0, 262.0), (110.0, 290.0), (-30.0, 330.0), (255.0, 330.0), (-260.0, -20.0), (60.0, -170.0)]
def vor_fields(X, Y, cell=42.0):
    """irregular field cells (domain-warped jittered Voronoi): returns (field id 0..1, hedge distance d2 - d1 in m)."""
    Xw = X + 16.0 * (fbm(X / 60.0, Y / 60.0, 81, 2) - 0.5); Yw = Y + 16.0 * (fbm(X / 60.0, Y / 60.0, 82, 2) - 0.5); ci = np.floor(Xw / cell); cj = np.floor(Yw / cell)
    d1 = np.full(X.shape, 1e9); d2 = np.full(X.shape, 1e9); fid = np.zeros(X.shape)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            gi = ci + di; gj = cj + dj; h1 = np.sin(gi * 12.9898 + gj * 78.233) * 43758.5453; h1 -= np.floor(h1); h2 = np.sin(gi * 39.346 + gj * 11.135) * 24634.6345; h2 -= np.floor(h2)
            h3 = np.sin(gi * 63.7 + gj * 17.3) * 9137.1; h3 -= np.floor(h3); sx = (gi + 0.2 + 0.6 * h1) * cell; sy = (gj + 0.2 + 0.6 * h2) * cell; d = np.hypot(Xw - sx, Yw - sy)
            new1 = d < d1; d2 = np.where(new1, d1, np.minimum(d2, d)); fid = np.where(new1, h3, fid); d1 = np.where(new1, d, d1)
    return fid, d2 - d1
def lane_w(X, Y):
    """dirt lanes from each farmstead to the road (bridge road x 0 / the camp), 3 m wide."""
    w = np.zeros(X.shape)
    for (fx, fy) in FARMS:
        tx, ty = (0.0, -60.0) if fy < 0 else (0.0, 215.0) if abs(fx) < 80 else ((0.0, 30.0))
        P0 = np.array([fx, fy]); P1 = np.array([tx, ty]); mid = (P0 + P1) / 2 + np.array([-(P1 - P0)[1], (P1 - P0)[0]]) * 0.12
        for a, b in ((P0, mid), (mid, P1)):
            ab = b - a; t = np.clip(((X - a[0]) * ab[0] + (Y - a[1]) * ab[1]) / (ab @ ab), 0, 1); d = np.hypot(X - (a[0] + t * ab[0]), Y - (a[1] + t * ab[1]) + 3.0 * np.sin(t * 9 + fx))
            w = np.maximum(w, smooth(1.8, 0.8, d))
    return w
def terrain_colour(X, Y, z, sd, hh, cm):
    m1 = fbm(X / 38.0, Y / 38.0, 7, 3); m2 = fbm(X / 13.0, Y / 13.0, 9, 3); m3 = fbm(X / 5.0, Y / 5.0, 21, 2)
    G1, G2, G3, G4 = hex_rgb('#b49a44'), hex_rgb('#c8a64a'), hex_rgb('#7c9a38'), hex_rgb('#b8a840')
    col = G1 + (G2 - G1) * smooth(0.5, 0.78, m1)[..., None]
    col = col + (G3 - col) * (smooth(0.58, 0.78, m2) * 0.55)[..., None]; col = col + (G4 - col) * (smooth(0.62, 0.8, m3) * 0.4)[..., None]
    # river margins: lush, then mud
    wet = smooth(7.0, 1.5, sd); col = col + (hex_rgb('#4d7f3c') - col) * (wet * 0.4)[..., None]
    mud = smooth(1.6 + 1.2 * m2, 0.2, sd) * (0.65 + 0.35 * m2); col = col + (hex_rgb('#8a7456') - col) * mud[..., None]; shg = smooth(1.2, 0.3, sd) * smooth(0.45, 0.7, m3); col = col + (hex_rgb('#b9ab8e') - col) * (shg * 0.7)[..., None]
    bed = smooth(-1.0, -2.6, sd); col = col + (hex_rgb('#3a5a60') - col) * bed[..., None]
    # patchwork fields: irregular cells of 6 tints (green-gold, ochre, heather brown, pale green, gold, plough) with hedgerows and furrows
    fid, he = vor_fields(X, Y)
    pal = np.array([hex_rgb('#8fb83e'), hex_rgb('#cfa94c'), hex_rgb('#b08a4e'), hex_rgb('#a8c84a'), hex_rgb('#dcc04c'), hex_rgb('#6fa63c'), hex_rgb('#c8903e'), hex_rgb('#86a840')]); fc = pal[np.minimum((fid * 8).astype(int), 7)]
    ang = fid * 6.28; fur = 0.5 + 0.5 * np.sin((X * np.cos(ang) + Y * np.sin(ang)) * 1.1); fc = fc * (0.93 + 0.12 * m3[..., None]) * (0.93 + 0.12 * fur[..., None] * (fid > 0.55)[..., None])
    hedge = smooth(2.2, 0.4, he); fc = fc + (hex_rgb('#3a6a2e') - fc) * hedge[..., None] * 0.9
    ex = (X / 80.0) ** 2 + ((Y - 125.0) / 92.0) ** 2; fw = smooth(0.9, 1.15, ex) * smooth(5.0, 11.0, sd) * smooth(6.0, 1.0, np.maximum(hh, 0))
    col = col + (fc - col) * (fw * (1 - np.clip(camp_tramp(X, Y) * 1.7, 0, 1)))[..., None]
    for (fx, fy) in FARMS: col = col + (hex_rgb('#a89468') - col) * (smooth(15.0, 8.0, np.hypot(X - fx, Y - fy)) * 0.8)[..., None]
    lw = lane_w(X, Y) * smooth(4.0, 9.0, sd) * (1 - smooth(1, 6, np.maximum(hh, 0))); col = col + (hex_rgb('#a88f66') - col) * (lw * 0.85)[..., None]
    # tracks: the road over the bridge (x 0) south into the camp and north up the neck; the camp trample
    rx = BRIDGE_X + 1.5 * np.sin(Y / 30.0)
    road = smooth(5.0, 2.4, np.abs(X - rx)) * (smooth(-150, -34, Y) * (1 - smooth(-26, -20, Y)) + smooth(20, 26, Y) * (1 - smooth(50, 62, Y)))
    byy = bank_y(X); bp = smooth(2.6, 1.0, np.abs(Y - (byy - 9.5) - 2.5 * np.sin(X / 13.0))) * smooth(0.2, 0.45, m2) * smooth(-230, -200, X) * (1 - smooth(-50, -10, X)); road = np.maximum(road, bp * 0.9)
    seg = np.array([-160.0, -148.0]); ab = np.array([-140.0, -148.0]); t_ = np.clip(((X - 160.0) * ab[0] + (Y - 150.0) * ab[1]) / (ab @ ab), 0, 1); dd_ = np.hypot(X - (160.0 + t_ * ab[0]) + 2.0 * np.sin(t_ * 8), Y - (150.0 + t_ * ab[1])); road = np.maximum(road, smooth(2.4, 1.1, dd_) * smooth(0.0, 1.0, t_) * (1 - smooth(0.9, 1.0, t_)) * 0.9)
    tramp = camp_tramp(X, Y)
    dirt = hex_rgb('#a08a68') * (0.92 + 0.16 * m3[..., None]); w = np.clip(road * 0.9 + tramp * (0.22 + 0.5 * smooth(0.55, 0.9, m2)), 0, 0.92) * smooth(0.5, -1.0, -sd - 0.0 + 0.0 * sd)
    w = w * smooth(-0.5, 1.0, sd); col = col + (dirt - col) * w[..., None]
    # hill: heather, bracken, grass skirt, rock
    h2 = np.maximum(hh, 0); wh = smooth(1.0, 10.0, h2)
    H1, H2, H3, BR = hex_rgb('#86583c'), hex_rgb('#946040'), hex_rgb('#6c4a34'), hex_rgb('#c0802c')
    hc = H1 + (H2 - H1) * smooth(0.4, 0.7, m2)[..., None]; hc = hc + (H3 - hc) * (smooth(0.55, 0.8, m3) * 0.6)[..., None]; hc = hc + (BR - hc) * (smooth(0.5, 0.7, fbm(X / 11.0, Y / 11.0, 33, 3)) * 0.85)[..., None]
    grass_skirt = smooth(24.0, 6.0, h2) * 0.6; hc = hc + (col - hc) * grass_skirt[..., None]
    col = col + (hc - col) * wh[..., None]
    e = 0.6; hx = (hill_h(X + e, Y)[0] - hill_h(X - e, Y)[0]) / (2 * e); hy = (hill_h(X, Y + e)[0] - hill_h(X, Y - e)[0]) / (2 * e); slope = np.hypot(hx, hy)
    rk = smooth(0.62, 1.05, slope) * smooth(6, 16, h2) + cm * 0.85 * smooth(12, 30, h2); rk = np.clip(rk, 0, 1)
    R1, R2 = hex_rgb('#9a97a2'), hex_rgb('#77727e'); rc = R1 + (R2 - R1) * smooth(0.4, 0.75, m2)[..., None]; rc = rc + (hex_rgb('#a9a79a') - rc) * (smooth(0.62, 0.8, m3) * 0.6)[..., None]
    rk = rk * (1 - smooth(PAD[2] + 12.0, PAD[2] + 2.0, np.hypot(X - PAD[0], Y - PAD[1])) * 0.95); col = col + (rc - col) * rk[..., None]
    # castle rock
    ch = castle_h(X, Y); crk = smooth(4.0, 25.0, ch); cg = rc * 0.95 + (hex_rgb('#7a9a46') - rc * 0.95) * (smooth(0.5, 0.7, m1) * 0.2)[..., None]
    col = col + (cg - col) * crk[..., None]
    r = np.hypot(X, Y); col = col + (far_colour(X, Y, z) - col) * (smooth(380, 700, r) * 0.5)[..., None]
    return col
def far_fields(X, Y):
    """outer ring of hills: the Ochils north, hills east and west, the Campsies south-west (zero inside r 420)."""
    r = np.hypot(X, Y); n = fbm(X / 420.0, Y / 420.0, 41, 3); n2 = fbm(X / 120.0, Y / 120.0, 43, 3)
    north = smooth(500, 1500, Y) * (210 + 140 * fbm(X / 600.0, 3.3, 51, 3)); south = smooth(-300, -1100, Y) * (120 + 90 * fbm(X / 500.0, 7.7, 52, 3))
    east = smooth(600, 1500, X) * (150 + 90 * n); west = smooth(-800, -1600, X) * (160 + 110 * n)
    return (north + south + east + west) * (0.8 + 0.4 * n2) * smooth(420, 900, r) + 10 * (n2 - 0.5) * smooth(400, 700, r)
def far_colour(X, Y, z):
    """far hills: 3 calm tint bands by height (olive-gold foot, green-brown mid, grey-blue top), very little mottling."""
    n = fbm(X / 260.0, Y / 260.0, 61, 2)
    lo = hex_rgb('#8fa04c') + (hex_rgb('#b0a04e') - hex_rgb('#8fa04c')) * smooth(0.45, 0.6, n)[..., None]
    mid = hex_rgb('#6f8a56'); hi = hex_rgb('#7f8896')
    col = lo + (mid - lo) * smooth(20, 90, z)[..., None]; col = col + (hi - col) * smooth(120, 260, z)[..., None]; return col
LEVELS = [('A', -240.0, 340.0, -200.0, 340.0, 1.6), ('M', -760.0, 760.0, -760.0, 760.0, 4.0), ('B', -2800.0, 2800.0, -2800.0, 2800.0, 16.0)]
_TERR = {}
def terrain_data(key='A'):
    if key in _TERR: return _TERR[key]
    lv = [l for l in LEVELS if l[0] == key][0]; _, x0, x1, y0, y1, st = lv; xs = np.arange(x0, x1 + 1e-6, st); ys = np.arange(y0, y1 + 1e-6, st); cf = os.path.join(CACHE, 'terrain%s_v%d.npz' % (key, TERRAIN_V))
    if os.path.exists(cf):
        z = np.load(cf); d = {k: z[k] for k in z.files}
    else:
        X, Y = np.meshgrid(xs, ys); z, sd, s, t, fx, fy, hh, cm, Lh = fields(X, Y); col = terrain_colour(X, Y, z, sd, hh, cm)
        d = dict(z=z, sd=sd, s=s, t=t, fx=fx, fy=fy, col=col); np.savez_compressed(cf, **{k: v.astype(np.float32) for k, v in d.items()})
    d['xs'] = xs; d['ys'] = ys; d['step'] = st; _TERR[key] = d; return d
def ground(x, y):
    """terrain height (bilinear on the fine mesh grid A, so props sit exactly on the mesh); scalars and arrays."""
    T = terrain_data('A'); st = T['step']; fx = (np.asarray(x, float) - T['xs'][0]) / st; fy = (np.asarray(y, float) - T['ys'][0]) / st
    fx = np.clip(fx, 0, len(T['xs']) - 1.001); fy = np.clip(fy, 0, len(T['ys']) - 1.001); i = np.floor(fx).astype(int); j = np.floor(fy).astype(int); a = fx - i; b = fy - j; Z = T['z']
    return (Z[j, i] * (1 - a) + Z[j, i + 1] * a) * (1 - b) + (Z[j + 1, i] * (1 - a) + Z[j + 1, i + 1] * a) * b
def sd_at(x, y):
    T = terrain_data('A'); st = T['step']; fx = np.clip((np.asarray(x, float) - T['xs'][0]) / st, 0, len(T['xs']) - 1.001); fy = np.clip((np.asarray(y, float) - T['ys'][0]) / st, 0, len(T['ys']) - 1.001)
    return T['sd'][np.floor(fy).astype(int), np.floor(fx).astype(int)]
def _grid_mesh(name, X, Y, Z, attrs, mat, mask=None, smooth_=True):
    ny, nx = X.shape; idx = np.arange(nx * ny).reshape(ny, nx); q = np.stack([idx[:-1, :-1], idx[:-1, 1:], idx[1:, 1:], idx[1:, :-1]], -1).reshape(-1, 4)
    if mask is not None:
        mq = (mask[:-1, :-1] | mask[:-1, 1:] | mask[1:, 1:] | mask[1:, :-1]).ravel(); q = q[mq]
    used = np.zeros(nx * ny, bool); used[q.ravel()] = True; remap = np.cumsum(used) - 1; q = remap[q]
    V = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)[used]; me = bpy.data.meshes.new(name); me.from_pydata(V.tolist(), [], q.tolist()); me.update()
    me.polygons.foreach_set('use_smooth', [smooth_] * len(me.polygons))
    for k, arr in attrs.items():
        a = np.asarray(arr).reshape(nx * ny, -1)[used]; a = np.concatenate([a, np.ones((len(a), 4 - a.shape[1]))], 1) if a.shape[1] < 4 else a
        ca = me.color_attributes.new(k, 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', a.astype(np.float32).ravel())
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.data.materials.append(get_mat(mat) if isinstance(mat, str) else mat); return ob
def _inside_prev(X, Y, k, margin):
    if k == 0: return np.zeros(X.shape, bool)
    _, x0, x1, y0, y1, st = LEVELS[k - 1]; return (X > x0 + margin) & (X < x1 - margin) & (Y > y0 + margin) & (Y < y1 - margin)
def build_terrain():
    objs = []
    for k, lv in enumerate(LEVELS):
        T = terrain_data(lv[0]); X, Y = np.meshgrid(T['xs'], T['ys']); inside = _inside_prev(X, Y, k, 3 * lv[5]); z = np.where(inside, T['z'] - 0.5, T['z'])
        # the coarse levels sit a little lower under the finer one's footprint
        objs.append(_grid_mesh('terrain_' + lv[0], X, Y, z, {'col': lin_arr(T['col'])}, 'terrain' if k == 0 else 'terrain_far', mask=~inside))
    return objs
def build_water():
    objs = []
    for k, lv in enumerate(LEVELS):
        T = terrain_data(lv[0]); X, Y = np.meshgrid(T['xs'], T['ys']); sd = T['sd']; inside = _inside_prev(X, Y, k, 3 * lv[5]); mask = (sd < 3.0) & ~inside
        if not mask.any(): continue
        sdw = -(sd + WATER_EDGE); depth = np.clip((sdw - 0.5) / 9.0 + 0.45 * (fbm(X / 22.0, Y / 22.0, 71, 3) - 0.5) + 0.12 * np.sin(T['s'] / 17.0), 0, 1); shore = np.clip(sdw, -1.5, 6.0)
        fuv = np.stack([T['s'], T['t'], np.zeros_like(T['s'])], -1)
        ob = _grid_mesh('water_' + lv[0], X, Y, np.zeros_like(X), {'wattr': np.stack([depth, shore, np.zeros_like(depth)], -1), 'fuv': fuv}, 'water', mask=mask, smooth_=True); ob.visible_shadow = False; objs.append(ob)
    return objs
def _water_mat():
    """smooth layered water: depth gradient (turquoise shallows to deep teal-blue), posterised bands stretched along the flow, thin foam streaks, shore foam,
    sky sheen at grazing angles and sun glitter (emission only: no glossy bounce). Flow = the 'fuv' offset (animate with set_flow)."""
    P = STATE['P']; m = bpy.data.materials.new('water'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new; out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry')
    wa = N('ShaderNodeAttribute'); wa.attribute_name = 'wattr'; wa.attribute_type = 'GEOMETRY'; fa = N('ShaderNodeAttribute'); fa.attribute_name = 'fuv'; fa.attribute_type = 'GEOMETRY'
    sp = N('ShaderNodeSeparateXYZ'); L(wa.outputs['Vector'], sp.inputs[0])
    ramp = N('ShaderNodeValToRGB'); L(sp.outputs['X'], ramp.inputs[0]); cr = ramp.color_ramp; cr.elements[0].position = 0.0; cr.elements[0].color = (*hex_lin(P.get('shallow', '#5cc8b4')), 1)
    cr.elements[1].position = 1.0; cr.elements[1].color = (*hex_lin('#0f5e74'), 1); e = cr.elements.new(0.3); e.color = (*hex_lin('#2fa8a4'), 1); e = cr.elements.new(0.6); e.color = (*hex_lin('#1a8392'), 1)
    off = N('ShaderNodeMapping'); L(fa.outputs['Vector'], off.inputs[0]); off.name = 'flow_off'; off.inputs['Scale'].default_value = (0.045, 0.30, 1.0)
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.0; nz.inputs['Detail'].default_value = 2.0; nz.inputs['Roughness'].default_value = 0.5; L(off.outputs[0], nz.inputs['Vector'])
    bands = N('ShaderNodeValToRGB'); bands.color_ramp.interpolation = 'CONSTANT'; be = bands.color_ramp.elements; be[0].color = (0.78, 0.82, 0.86, 1); be[1].position = 0.42; be[1].color = (1, 1, 1, 1)
    e = bands.color_ramp.elements.new(0.66); e.color = (1.22, 1.2, 1.1, 1); L(nz.outputs['Fac'], bands.inputs[0])
    bandf = N('ShaderNodeRGBToBW'); L(bands.outputs['Color'], bandf.inputs[0]); art = _vs(nt, ramp.outputs['Color'], bandf.outputs[0])
    # foam streaks along the flow (thin, crisp) and shore foam
    off2 = N('ShaderNodeMapping'); L(fa.outputs['Vector'], off2.inputs[0]); off2.name = 'flow_off2'; off2.inputs['Scale'].default_value = (0.11, 0.9, 1.0)
    nz2 = N('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 1.4; nz2.inputs['Detail'].default_value = 1.0; L(off2.outputs[0], nz2.inputs['Vector'])
    st = N('ShaderNodeValToRGB'); st.color_ramp.interpolation = 'CONSTANT'; st.color_ramp.elements[0].color = (0, 0, 0, 1); st.color_ramp.elements[1].position = 0.7; st.color_ramp.elements[1].color = (1, 1, 1, 1); L(nz2.outputs['Fac'], st.inputs[0])
    nz3 = N('ShaderNodeTexNoise'); nz3.inputs['Scale'].default_value = 0.35; L(off2.outputs[0], nz3.inputs['Vector'])
    gate = N('ShaderNodeValToRGB'); gate.color_ramp.interpolation = 'CONSTANT'; gate.color_ramp.elements[0].color = (0, 0, 0, 1); gate.color_ramp.elements[1].position = 0.56; gate.color_ramp.elements[1].color = (1, 1, 1, 1); L(nz3.outputs['Fac'], gate.inputs[0])
    sg = N('ShaderNodeMath'); sg.operation = 'MULTIPLY'; L(st.outputs['Color'], sg.inputs[0]) if False else None
    stb = N('ShaderNodeRGBToBW'); L(st.outputs['Color'], stb.inputs[0]); gtb = N('ShaderNodeRGBToBW'); L(gate.outputs['Color'], gtb.inputs[0]); L(stb.outputs[0], sg.inputs[0]); L(gtb.outputs[0], sg.inputs[1])
    # shore foam: a crisp irregular band at the waterline, fading to streaks a few metres out
    nz4 = N('ShaderNodeTexNoise'); nz4.inputs['Scale'].default_value = 1.1; nz4.inputs['Detail'].default_value = 2.0; L(fa.outputs['Vector'], nz4.inputs['Vector'])
    wob = N('ShaderNodeMath'); wob.operation = 'MULTIPLY_ADD'; wob.inputs[1].default_value = 0.55 * P.get('foam_k', 1.0); L(nz4.outputs['Fac'], wob.inputs[0]); wob.inputs[2].default_value = 0.08 * P.get('foam_k', 1.0)
    cmp_ = N('ShaderNodeMath'); cmp_.operation = 'LESS_THAN'; L(sp.outputs['Y'], cmp_.inputs[0]); L(wob.outputs[0], cmp_.inputs[1])
    sh = N('ShaderNodeMath'); sh.operation = 'MAXIMUM'; L(cmp_.outputs[0], sh.inputs[0]); L(sg.outputs[0], sh.inputs[1])
    # keep streaks off the very deep centre
    dm = N('ShaderNodeMath'); dm.operation = 'LESS_THAN'; dm.inputs[1].default_value = 0.95; L(sp.outputs['X'], dm.inputs[0])
    shm = N('ShaderNodeMath'); shm.operation = 'MULTIPLY'; L(sh.outputs[0], shm.inputs[0]); L(dm.outputs[0], shm.inputs[1])
    foamc = N('ShaderNodeMix'); foamc.data_type = 'RGBA'; L(shm.outputs[0], foamc.inputs[0]); L(art, foamc.inputs[6]); foamc.inputs[7].default_value = (*hex_lin('#e8f4ee'), 1); art2 = foamc.outputs[2]
    core = _lit_core(nt, art2, dict(mix=0.7, sm=(0.7, 1.0, 1.2), afl=0.25), geo)
    # sky sheen at grazing angles
    lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35; sheen = N('ShaderNodeEmission'); sheen.inputs['Color'].default_value = (*hex_lin('#bcd4ee'), 1)
    km = N('ShaderNodeMath'); km.operation = 'MULTIPLY'; km.inputs[1].default_value = 0.22 * P.get('sheen_k', 1.0); L(lw.outputs['Facing'], km.inputs[0])
    kf = N('ShaderNodeMath'); kf.operation = 'MULTIPLY'; L(km.outputs[0], kf.inputs[0]); nfoam = N('ShaderNodeMath'); nfoam.operation = 'SUBTRACT'; nfoam.inputs[0].default_value = 1.0; L(shm.outputs[0], nfoam.inputs[1]); L(nfoam.outputs[0], kf.inputs[1])
    L(kf.outputs[0], sheen.inputs['Strength']); a1 = N('ShaderNodeAddShader'); L(core, a1.inputs[0]); L(sheen.outputs['Emission'], a1.inputs[1])
    # sun glitter: small bright cells where a rippled normal reflects the sun toward the camera
    sd_ = Vector(P['sun_dir']).normalized(); tsun = (-sd_.x, -sd_.y, -sd_.z)
    vr = N('ShaderNodeTexVoronoi'); vr.feature = 'F1'; vr.inputs['Scale'].default_value = 1.6; L(fa.outputs['Vector'], vr.inputs['Vector'])
    tcw = N('ShaderNodeTexCoord'); vr2 = N('ShaderNodeTexVoronoi'); vr2.name = 'glit_vor'; vr2.voronoi_dimensions = '4D'; vr2.inputs['Scale'].default_value = P.get('glit_s', 2.1); vr2.feature = 'F1'; L(tcw.outputs['Object'], vr2.inputs['Vector'])
    gl = N('ShaderNodeMath'); gl.operation = 'LESS_THAN'; gl.inputs[1].default_value = P.get('glit_t', 0.1); L(vr2.outputs['Distance'], gl.inputs[0])
    rnd = N('ShaderNodeTexNoise'); rnd.name = 'glit_noise'; rnd.noise_dimensions = '4D'; rnd.inputs['Scale'].default_value = 0.8; L(tcw.outputs['Object'], rnd.inputs['Vector'])
    rg = N('ShaderNodeMath'); rg.operation = 'GREATER_THAN'; rg.inputs[1].default_value = 0.5; L(rnd.outputs['Fac'], rg.inputs[0])
    g2 = N('ShaderNodeMath'); g2.operation = 'MULTIPLY'; L(gl.outputs[0], g2.inputs[0]); L(rg.outputs[0], g2.inputs[1])
    # facing the sun glint path: view direction (incoming) dotted with sun direction (towards the sun), wide lobe
    dp = N('ShaderNodeVectorMath'); dp.operation = 'DOT_PRODUCT'; dp.inputs[1].default_value = tsun; L(geo.outputs['Incoming'], dp.inputs[0])
    gp = N('ShaderNodeMapRange'); gp.clamp = True; gp.inputs['From Min'].default_value = 0.45; gp.inputs['From Max'].default_value = 0.98; L(dp.outputs['Value'], gp.inputs['Value'])
    nsr = N('ShaderNodeTexNoise'); nsr.inputs['Scale'].default_value = P.get('glit_ns', 0.012); L(tcw.outputs['Object'], nsr.inputs['Vector'])
    mrg = N('ShaderNodeMapRange'); mrg.clamp = True; mrg.inputs['From Min'].default_value = 0.5; mrg.inputs['From Max'].default_value = 0.58; mrg.inputs['To Max'].default_value = P.get('glit_stretch', 0.0); L(nsr.outputs['Fac'], mrg.inputs['Value'])
    gmx = N('ShaderNodeMath'); gmx.operation = 'MAXIMUM'; L(gp.outputs['Result'], gmx.inputs[0]); L(mrg.outputs['Result'], gmx.inputs[1])
    g3 = N('ShaderNodeMath'); g3.operation = 'MULTIPLY'; L(g2.outputs[0], g3.inputs[0]); L(gmx.outputs[0], g3.inputs[1])
    ge = N('ShaderNodeEmission'); ge.inputs['Color'].default_value = (*hex_lin('#fff3c8'), 1); ge.inputs['Strength'].default_value = 3.0
    gsm = N('ShaderNodeMath'); gsm.operation = 'MULTIPLY'; L(g3.outputs[0], gsm.inputs[0]); gsm.inputs[1].default_value = 1.0; L(gsm.outputs[0], ge.inputs['Strength'])
    nstr = N('ShaderNodeMath'); nstr.operation = 'MULTIPLY'; nstr.inputs[1].default_value = 6.0; L(g3.outputs[0], nstr.inputs[0]); L(nstr.outputs[0], ge.inputs['Strength'])
    a2 = N('ShaderNodeAddShader'); L(a1.outputs['Shader'], a2.inputs[0]); L(ge.outputs['Emission'], a2.inputs[1])
    L(_haze_out(nt, a2.outputs['Shader']), out.inputs['Surface']); return m

# ================================================================ BUILD / RENDER GLUE (props are added below)
PRESETS = {}
BUILDERS = []                         # prop builders registered by the sections below: fn(A, cam) -> None
def project(cam, p, w=720, h=1280):
    from bpy_extras.object_utils import world_to_camera_view
    v = world_to_camera_view(bpy.context.scene, cam, Vector(p)); return v.x * w, (1 - v.y) * h, v.z
def build(preset=None, light='MORNING', ink=True, fg=True, location=None):
    pr = PRESETS.get(preset) if preset else None
    sc = new_scene(light, (pr or {}).get('over')); STATE['preset'] = preset; STATE['loc'] = (pr or {}).get('loc', location)
    if pr and pr.get('cam_dz') is not None: ref = pr.get('cam_ref', pr['cam'][:2]); pr['cam'] = (pr['cam'][0], pr['cam'][1], float(ground(ref[0], ref[1])) + pr['cam_dz'])
    cam_loc = pr['cam'] if pr else (0, -60, 40); look = pr['look'] if pr else (0, 0, 0); STATE['cam'] = cam_loc
    sd_ = pr.get('sd', 12.0) if pr else 12.0; STATE['ink_t'] = float(np.clip(0.0035 * sd_, 0.01, 0.05)) if ink else 0.0
    A = dict(marks={}, location=STATE['loc'], preset=preset, light=light)
    build_terrain(); build_water(); sky_dome(); sun()
    for fn in BUILDERS: fn(A, pr)
    if pr:
        cam = camera(cam_loc, look, pr.get('lens', 22.0)); A['cam'] = dict(loc=tuple(cam_loc), look=tuple(look), lens=pr.get('lens', 22.0))
        if pr.get('marks'): A['marks'].update(pr['marks'](A))
    return A
def setup_render(sc, mode='final', samples=None):
    r = sc.render; r.image_settings.file_format = 'PNG'; r.threads_mode = 'FIXED'; r.threads = 4
    if mode == 'draft': r.resolution_x, r.resolution_y, r.resolution_percentage = 360, 640, 100; n = samples or 20
    else: r.resolution_x, r.resolution_y, r.resolution_percentage = 720, 1280, 100; n = samples or 64
    sc.cycles.samples = n; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.preview_samples = 8; STATE['scale'] = r.resolution_x / 720.0
def _gblur(a, rad):
    rad = max(float(rad), 0.3); k = int(rad * 3) + 1; x = np.arange(-k, k + 1); g = np.exp(-x * x / (2 * rad * rad)); g /= g.sum()
    def conv(arr, axis):
        p = np.pad(arr, [(k, k) if i == axis else (0, 0) for i in range(arr.ndim)], mode='edge'); out = np.zeros_like(arr, dtype=np.float32)
        for i, w in enumerate(g): out += w * np.take(p, np.arange(i, i + arr.shape[axis]), axis=axis)
        return out
    return conv(conv(a.astype(np.float32), 0), 1)
def grade(path, sat=1.07, bloom=0.5, scale=None, gamma=1.28):
    """final grade: bloom halo around real emitters only (min channel >= 252), then a saturation boost. Nothing else."""
    scale = scale or STATE.get('scale', 1.0)
    im = np.asarray(Image.open(path).convert('RGB'), dtype=np.float32) / 255
    if bloom:
        m = (im.min(-1) >= 252 / 255).astype(np.float32)
        if m.sum() > 4:
            from PIL import ImageFilter
            ring = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7 if scale < 1 else 13)), dtype=np.float32) / 255 - m
            ringc = _gblur(im * ring[..., None], 6 * scale) / (_gblur(ring, 6 * scale)[..., None] + 1e-4); ringc = ringc / (ringc.max(-1, keepdims=True) + 1e-4)
            core = _gblur(m, 7 * scale); wide = _gblur(m, 16 * scale); halo = (0.6 * core + 0.5 * wide)[..., None] * ringc; im = np.clip(im + bloom * halo, 0, 1)
    im = np.clip(im, 0, 1) ** gamma; mx = im.max(-1, keepdims=True); im = np.clip(mx - (mx - im) * sat, 0, 1)
    # VIVID stage (QA_TEAM.md §G, client 2026-11-20): per-preset (gamma, sat) fitted on the SET-gate tiles so frame saturation >= 0.47
    # (qa_stats.py measure) and mean luma about 85-110, like film 2 (0.49 / 94). Fixed per preset -> no flicker. STATE['vivid'] overrides.
    vg, vs = STATE.get('vivid') or VIVID.get(STATE.get('preset'), (1.4, 1.3))
    im = np.clip(im, 0, 1) ** vg; mx = im.max(-1, keepdims=True); im = np.clip(mx - (mx - im) * vs, 0, 1)
    Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(path)
VIVID = {'bridge_deck': (1.78, 1.15), 'bridge_end_north': (1.38, 1.23), 'bridge_end_south': (1.9, 1.15), 'bridge_high': (1.9, 1.15),
         'camp_bank': (1.52, 1.3), 'camp_table': (1.05, 1.1), 'camp_wide': (1.9, 1.15), 'hill_eye': (0.8, 1.31), 'hill_low': (1.38, 1.15),
         'hill_over': (1.48, 1.15), 'river_low': (1.9, 1.3), 'riverbank': (1.5, 1.6), 'valley_loop': (1.07, 1.71), 'valley_river': (2.28, 1.18),
         'valley_wide': (1.11, 1.83)}
def render(path, mode='final', samples=None, do_grade=True):
    sc = bpy.context.scene; setup_render(sc, mode, samples); sc.render.filepath = path; t = time.time(); bpy.ops.render.render(write_still=True); dt = time.time() - t
    if do_grade: grade(path)
    return dt

# ================================================================ PRIMITIVES FOR PROPS
def _bulk(self, mat, V, F, smooth_=False, tint=None):
    """append already-world-space vertex arrays (N,3) + faces (list of tuples) in one go (stack applied)."""
    V = np.asarray(V, float); V = (self.stack[-1][:3, :3] @ V.T).T + self.stack[-1][:3, 3]
    Dd = self.d.setdefault(mat, dict(v=[], f=[], s=[], t=[], n=0)); n = Dd['n']
    Dd['f'] += [tuple(i + n for i in f) for f in F]; Dd['s'] += [smooth_] * len(F); Dd['v'].append(V); Dd['n'] += len(V)
    Dd['t'].append(np.ones((len(V), 4)) if tint is None else np.concatenate([np.asarray(tint, float), np.ones((len(V), 1))], 1))
Batch.bulk = _bulk
def _rod(self, mat, p0, p1, r=0.03, seg=6, tint=1.0, caps=False, r2=None):
    p0 = np.array(p0, float); p1 = np.array(p1, float); d = p1 - p0; L = np.linalg.norm(d)
    if L < 1e-6: return
    z = d / L; a = np.array([1.0, 0, 0]) if abs(z[0]) < 0.9 else np.array([0, 1.0, 0]); x = np.cross(z, a); x /= np.linalg.norm(x); y = np.cross(z, x)
    th = np.linspace(0, 2 * math.pi, seg, endpoint=False); ring = np.stack([np.cos(th), np.sin(th)], 1)
    r2 = r if r2 is None else r2; lo = p0 + r * (ring[:, :1] * x + ring[:, 1:] * y); hi = p1 + r2 * (ring[:, :1] * x + ring[:, 1:] * y)
    f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]; self._put(mat, np.concatenate([lo, hi]), f, False, tint)
Batch.rod = _rod
def _cone(self, mat, c, r, h, seg=8, tint=1.0, smooth_=False):
    th = np.linspace(0, 2 * math.pi, seg, endpoint=False); V = np.concatenate([np.stack([r * np.cos(th), r * np.sin(th), np.zeros(seg)], 1), [[0, 0, h]], [[0, 0, 0]]]) + np.array(c)
    f = [(i, (i + 1) % seg, seg) for i in range(seg)] + [((i + 1) % seg, i, seg + 1) for i in range(seg)]; self._put(mat, V, f, smooth_, tint)
Batch.cone = _cone
def _blob(self, mat, c, r, tint=1.0):
    V = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], float) * r + np.array(c)
    F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]; self._put(mat, V, F, False, tint)
Batch.blob = _blob
def jit(rng_, base, amp):
    """tint jitter (r,g,b) around a base multiplier"""
    t = 1 + (rng_.rand() - 0.5) * amp; return (t, t, t)
def tuft_arrays(rs, pts, hs, tints, blades=5, wid=0.03):
    """(N,3) base points -> vertices (N*blades*3, 3), faces, tint: grass tufts of `blades` leaning triangles each."""
    N = len(pts); a = rs.rand(N, blades) * 2 * math.pi; lean = (0.08 + 0.18 * rs.rand(N, blades)) * hs[:, None]; hh = hs[:, None] * (0.7 + 0.45 * rs.rand(N, blades)); w = wid * hs[:, None] / 0.3 + 0.006
    cx, cy = np.cos(a), np.sin(a); ox = rs.randn(N, blades) * 0.04; oy = rs.randn(N, blades) * 0.04
    bx = pts[:, 0:1] + ox; by = pts[:, 1:2] + oy; bz = pts[:, 2:3] - 0.02 + np.zeros((N, blades))
    p0 = np.stack([bx - cy * w, by + cx * w, bz + 0 * w], -1); p1 = np.stack([bx + cy * w, by - cx * w, bz + 0 * w], -1); p2 = np.stack([bx + cx * lean, by + cy * lean, bz + hh], -1)
    V = np.stack([p0, p1, p2], 2).reshape(-1, 3); F = [(3 * i, 3 * i + 1, 3 * i + 2) for i in range(N * blades)]
    t = np.repeat(tints, blades * 3, axis=0); return V, F, t
def sample_wedge(rs, n, cam, look, r0, r1, half_deg, extra_r=5.0):
    """n random xy points in the annulus [r0, r1] around the camera, inside a wedge of +-half_deg around the view azimuth (plus everything within extra_r)."""
    az = math.atan2(look[1] - cam[1], look[0] - cam[0]); r = np.sqrt(rs.uniform(r0 * r0, r1 * r1, n)); a = az + np.radians(rs.uniform(-half_deg, half_deg, n))
    return cam[0] + r * np.cos(a), cam[1] + r * np.sin(a)
_ICO0 = [None]
def _ico0():
    if _ICO0[0] is None:
        t = (1 + 5 ** 0.5) / 2; v = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
        f = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
        _ICO0[0] = (np.array([np.array(p) / np.linalg.norm(p) for p in v]), f)
    return _ICO0[0]
def ground_col(x, y):
    T = terrain_data('A'); st = T['step']; i = np.clip(np.round((np.asarray(x) - T['xs'][0]) / st).astype(int), 0, len(T['xs']) - 1); j = np.clip(np.round((np.asarray(y) - T['ys'][0]) / st).astype(int), 0, len(T['ys']) - 1); return lin_arr(T['col'][j, i])
def blobs_bulk(B, mat, pos, rad, sq, tint, rs, base=None):
    """many icosahedron blobs at pos (N,3) with radius rad (N,), vertical squash sq, per-instance tint (N,3), random yaw, in one bulk call."""
    v0, f0 = base or _ico0(); N = len(pos); a = rs.rand(N) * 6.28; ca, sa = np.cos(a), np.sin(a); V = v0[None] * np.stack([rad, rad, rad * sq], 1)[:, None, :]
    X = V[..., 0] * ca[:, None] - V[..., 1] * sa[:, None]; Y = V[..., 0] * sa[:, None] + V[..., 1] * ca[:, None]; V = np.stack([X, Y, V[..., 2]], -1) + pos[:, None, :]
    nv = len(v0); F = [tuple(int(k) + i * nv for k in f) for i in range(N) for f in f0]; B.bulk(mat, V.reshape(-1, 3), F, False, np.repeat(tint, nv, axis=0))
def dirt_w(X, Y):
    rx = BRIDGE_X + 1.5 * np.sin(Y / 30.0)
    road = smooth(5.0, 2.4, np.abs(X - rx)) * (smooth(-150, -34, Y) * (1 - smooth(-26, -20, Y)) + smooth(20, 26, Y) * (1 - smooth(50, 62, Y)))
    return np.clip(road * 0.9 + camp_tramp(X, Y) * 0.3, 0, 1)

# ---------------------------------------------------------------- vegetation, rocks, trees
def veg_near(A, pr):
    """cam-wedge vegetation: grass tufts, flowers, heather, bracken, gorse, reeds, small rocks, density falling with distance. Everything sits on the mesh."""
    if not pr or not pr.get('veg'): return
    cam = pr['cam']; look = pr['look']; cfg = pr['veg']; rs = np.random.RandomState(cfg.get('seed', 3)); half = cfg.get('half', 38); B = Batch(11); Bh = Batch(12); Bg = Batch(13); Br = Batch(14)
    # grass: tussock blobs (cartoon low poly, tinted from the painted ground) + a few blade shards + octahedral wildflowers, in bands
    for (r0, r1, n, hlo, hhi) in cfg.get('grass', [(1.5, 10, 5000, 0.1, 0.17), (10, 40, 4000, 0.18, 0.3), (40, 90, 2500, 0.35, 0.6)]):
        x, y = sample_wedge(rs, n, cam, look, r0, r1, half); z = ground(x, y); sd = sd_at(x, y); hh, _ = hill_h(x, y); dw = dirt_w(x, y)
        ok = ~in_corridor(pr, x, y) & (sd > 0.6) & (rs.rand(n) > dw * 1.1) & ((hh < 4.0 + 8 * rs.rand(n)) | (rs.rand(n) < cfg.get('hill_grass', 0.0)))
        x, y, z = x[ok], y[ok], z[ok]; n2 = len(x)
        if n2 == 0: continue
        rad = rs.uniform(hlo, hhi, n2); gc = ground_col(x, y) * (0.8 + 0.45 * rs.rand(n2))[:, None]
        gold = rs.rand(n2) < 0.25; gc = np.where(gold[:, None], np.array(hex_lin('#c9b04e')) * (0.8 + 0.4 * rs.rand(n2))[:, None], gc)
        V, F, T_ = tuft_arrays(rs, np.stack([x, y, z], 1), rad * cfg.get('tuft_k', 2.4), gc * cfg.get('tuft_gain', 1.35), blades=9, wid=0.02); B.bulk('sprig', V, F, False, T_)
    x, y = sample_wedge(rs, cfg.get('flowers', 1800) // 3, cam, look, 2, 38, half); z = ground(x, y); sd = sd_at(x, y); hh, _ = hill_h(x, y); ok = (sd > 1.5) & (hh < 3) & (dirt_w(x, y) < 0.3)
    x, y, z = x[ok], y[ok], z[ok]; n = len(x); cols = [hex_lin(h) for h in ('#ffe05a', '#fffaf0', '#ffe05a', '#ffb347', '#f4d0b8')]
    for i in range(n): Bg.blob('gorse_fl', (x[i], y[i], z[i] + 0.12 + 0.08 * rs.rand()), 0.035 + 0.03 * rs.rand(), tint=tuple(np.array(cols[rs.randint(0, 5)]) / np.array(hex_lin('#f3c61f'))))
    # heather clumps / bracken / gorse on the hill
    hz_ = cfg.get('heather'); Bp = Batch(15)
    if hz_:
        PAL = [hex_lin(h) for h in ('#7a5048', '#80563f', '#6e5242', '#7a5446', '#704c46', '#66463e', '#78604c', '#7a4a4c')]; BR = [hex_lin(h) for h in ('#b0782f', '#9a6a2c', '#c08a3c')]; v0, f0 = _ico()
        for (r0, r1, n, slo, shi) in hz_:
            x, y = sample_wedge(rs, n, cam, look, r0, r1, half); z = ground(x, y); hh, cm = hill_h(x, y); sd = sd_at(x, y); e = 0.8
            slope = np.hypot((hill_h(x + e, y)[0] - hill_h(x - e, y)[0]) / (2 * e), (hill_h(x, y + e)[0] - hill_h(x, y - e)[0]) / (2 * e)); ok = (hh > 3) & (slope < 1.0) & (sd > 2) & ~in_corridor(pr, x, y)
            x, y, z = x[ok], y[ok], z[ok]; n2 = len(x); kind = rs.rand(n2)
            if n2 == 0: continue
            if r1 <= cfg.get('sprig_to', 0):                      # near field: purple sprigs (leaning blades) + pink flower dots + bracken fans
                hs = np.where(kind < 0.86, rs.uniform(slo, shi, n2) * 0.85, rs.uniform(slo, shi, n2) * 1.5); col = np.array([PAL[i] for i in rs.randint(0, len(PAL), n2)]) * (0.8 + 0.4 * rs.rand(n2))[:, None]
                col = np.where((kind >= 0.86)[:, None], np.array([BR[i] for i in rs.randint(0, 3, n2)]) * (0.8 + 0.4 * rs.rand(n2))[:, None], col)
                V, F, T = tuft_arrays(rs, np.stack([x, y, z], 1), hs, col, blades=7, wid=0.07); Bp.bulk('sprig', V, F, False, T)
                m = (kind < 0.86) & (not cfg.get('no_chips')); fx, fy, fz = x[m], y[m], z[m]; k = len(fx)
                if k == 0: continue
                sz = 0.03 + 0.02 * rs.rand(k); hz2 = hs[m] * 0.8; V = np.zeros((k * 4, 3)); a_ = rs.rand(k) * 6.28
                for q, (ox, oy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))): V[q::4] = np.stack([fx + sz * (ox * np.cos(a_) - oy * np.sin(a_)), fy + sz * (ox * np.sin(a_) + oy * np.cos(a_)), fz + hz2], 1)
                Bg.bulk('flower', V, [(4 * i, 4 * i + 1, 4 * i + 2, 4 * i + 3) for i in range(k)], False, np.repeat(np.array([hex_lin('#e8b8a8')] * k) * (0.85 + 0.3 * rs.rand(k))[:, None], 4, axis=0))
            else:
                sc = rs.uniform(slo, shi, n2); col = np.array([PAL[i] for i in rs.randint(0, len(PAL), n2)]) * (0.8 + 0.4 * rs.rand(n2))[:, None]
                for i in range(n2):
                    if kind[i] < 0.95: s_ = sc[i]; V = v0 * np.array([s_ * 1.1, s_ * 1.0, s_ * 0.55]) + np.array([x[i], y[i], z[i] + s_ * 0.12]); Bh.bulk('heather', V, f0, False, np.tile(col[i] / np.array(hex_lin('#7a4f72')), (len(V), 1)))
                    else: s_ = sc[i] * 1.2; V = v0 * np.array([s_ * 1.1, s_ * 1.1, s_ * 0.6]) + np.array([x[i], y[i], z[i] + s_ * 0.1]); Bh.bulk('bracken', V, f0, False, np.tile(np.array([1.0, 0.85, 0.7]) * (0.8 + 0.4 * rs.rand()), (len(V), 1)))
    gz = cfg.get('gorse')
    if gz:
        for (r0, r1, n) in gz:
            x, y = sample_wedge(rs, n, cam, look, r0, r1, half); z = ground(x, y); hh, cm = hill_h(x, y); sd = sd_at(x, y); ok = (hh > 1.5) & (sd > 2) & ~in_corridor(pr, x, y); x, y, z = x[ok], y[ok], z[ok]
            for i in range(len(x)): gorse(Bg, (x[i], y[i], z[i]), rs.uniform(0.4, 0.8), rs)
    # reeds along the water edge
    rz = cfg.get('reeds')
    if rz:
        for (r0, r1, n) in rz:
            x, y = sample_wedge(rs, n * 4, cam, look, r0, r1, half + 10); sd = sd_at(x, y); ok = (sd > -1.8) & (sd < 1.4); x, y = x[ok][:n], y[ok][:n]; z = ground(x, y)
            for i in range(len(x)): reed_cluster(Br, (x[i], y[i], z[i]), rs)
    for b, nm in ((B, 'grass'), (Bh, 'heather'), (Bg, 'gorse'), (Br, 'reed'), (Bp, 'sprig')): b.finalize('veg_' + nm, ink=False)
def gorse(B, c, s, rs):
    """a prickly mound of olive green with scattered yellow flowers."""
    x, y, z = c; v0, f0 = _ico()
    for k in range(rs.randint(3, 5)):
        ox, oy = rs.uniform(-0.45, 0.45, 2) * s; r = rs.uniform(0.38, 0.6) * s; V = v0 * np.array([r, r, r * 0.8]) + np.array([x + ox, y + oy, z + r * 0.45])
        B.bulk('gorse', V, f0, False, np.tile(np.array([0.9, 1.0, 0.8]) * (0.75 + 0.5 * rs.rand()), (len(V), 1)))
        for j in range(14):
            p = v0[rs.randint(0, len(v0))]; p = p * np.array([1, 1, 1]); 
            if p[2] < 0.0: continue
            q = np.array([x + ox, y + oy, z + r * 0.45]) + p * np.array([r, r, r * 0.8]) * 1.0; B.blob('gorse_fl', q, 0.07 * s, tint=(0.85 + 0.3 * rs.rand(),) * 3)

def reed_cluster(B, c, rs):
    x, y, z = c; n = rs.randint(6, 11); h0 = rs.uniform(0.9, 1.9) * STATE['P'].get('reed_k', 1.0)
    for i in range(n):
        a = rs.rand() * 6.28; r = rs.rand() * 0.35; bx, by = x + r * math.cos(a), y + r * math.sin(a); h = h0 * rs.uniform(0.7, 1.15); lean = rs.uniform(0.05, 0.35) * h; la = rs.rand() * 6.28; w = 0.075
        B.tri('reed', (bx - w, by, z - 0.15), (bx + w, by, z - 0.05), (bx + lean * math.cos(la), by + lean * math.sin(la), z + h), tint=(0.8 + 0.4 * rs.rand(),) * 3)
        if i == 0 and rs.rand() < 0.5: B.cyl('cattail', (bx + lean * math.cos(la) * 0.8, by + lean * math.sin(la) * 0.8, z + h * 0.8), 0.028, 0.15, seg=5)
def pine(B, x, y, z, h, rs, lean=0.0):
    """Scots pine: a tall bare orange-brown trunk, a flat irregular crown of dark blue-green pads at the top."""
    la = rs.rand() * 6.28; tx, ty = math.cos(la) * lean * h, math.sin(la) * lean * h; tt = rs.uniform(0.9, 1.1)
    B.rod('pine_trunk', (x, y, z - 0.3), (x + tx, y + ty, z + h), 0.36 * h / 10.0, seg=7, tint=(tt, tt, tt))
    B.cone('pine_trunk', (x - 0.0, y - 0.0, z - 0.3), 0.55 * h / 10.0, 0.9, seg=7)
    for k in range(rs.randint(2, 4)):                                       # a couple of bare side branches
        zz = z + h * rs.uniform(0.55, 0.85); a = rs.rand() * 6.28; B.rod('pine_trunk', (x + tx * (zz - z) / h, y + ty * (zz - z) / h, zz), (x + tx * (zz - z) / h + math.cos(a) * h * 0.18, y + ty * (zz - z) / h + math.sin(a) * h * 0.18, zz + h * 0.12), 0.11 * h / 10, seg=5)
    ncl = rs.randint(4, 7)
    for k in range(ncl):
        a = rs.rand() * 6.28; rr = h * 0.2 * rs.uniform(0.3, 1.0); cz = z + h * (0.86 + 0.14 * rs.rand()) + h * 0.03 * k; pr = h * rs.uniform(0.16, 0.26)
        cx_, cy_ = x + tx + rr * math.cos(a), y + ty + rr * math.sin(a); t = rs.uniform(0.85, 1.15)
        B.sphere('pine_leaf', (cx_, cy_, cz), pr, seg=9, rings=5, scale=(1, 1, 0.5), tint=(t, t, t * 1.05))
def oak(B, x, y, z, h, rs):
    """broadleaf tree: short brown trunk, a clump of 4-6 round leaf blobs in fresh greens."""
    B.rod('bark', (x, y, z - 0.2), (x, y, z + h * 0.45), 0.2 * h / 6, seg=7)
    for k in range(rs.randint(4, 7)):
        a = rs.rand() * 6.28; rr = h * 0.22 * rs.rand(); r = h * rs.uniform(0.22, 0.34); t = rs.uniform(0.8, 1.2); g = (t * rs.uniform(0.9, 1.1), t, t * rs.uniform(0.7, 1.0))
        B.sphere('leaf', (x + rr * math.cos(a), y + rr * math.sin(a), z + h * (0.55 + 0.2 * rs.rand())), r, seg=9, rings=5, scale=(1, 1, 0.85), tint=g)
def boulder(B, x, y, z, s, rs, mat='rock'):
    t = rs.uniform(0.82, 1.12); B.rock(mat, (x, y, z), (s * rs.uniform(1.0, 1.5), s * rs.uniform(0.9, 1.3), s * rs.uniform(0.6, 1.0)), seed=rs.randint(0, 9999), tint=(t, t, t * rs.uniform(0.95, 1.05)), rot=(0, 0, rs.uniform(0, 360)))
def crag_group(B, x, y, rs, n=6, spread=3.0, s=1.4, mat='rock'):
    for i in range(n):
        ox, oy = rs.uniform(-spread, spread, 2); zz = float(ground(x + ox, y + oy)); boulder(B, x + ox, y + oy, zz, s * rs.uniform(0.5, 1.6), rs, mat if rs.rand() < 0.75 else 'rock_warm')
def spear(B, base, tilt=(0, 0), h=2.6, head=True):
    """a spear: ash shaft with a small steel leaf head; tilt = lean (dx, dy) of the tip."""
    x, y, z = base; tip = (x + tilt[0], y + tilt[1], z + h); B.rod('wood', (x, y, z), tip, 0.022, seg=5)
    if head:
        d = np.array([tilt[0], tilt[1], h]); d = d / np.linalg.norm(d); p = np.array(tip); B.rod('steel', p, p + d * 0.28, 0.03, seg=4); B.rod('steel', p + d * 0.28, p + d * 0.46, 0.012, seg=4)

# ---------------------------------------------------------------- the bridge (wooden trestle, 2.6 m deck, rails, piers in the water)
def foam_ring(B, x, y, r0, r1, rs, wake=0.0, z=0.03):
    """irregular foam collar round a pier post, plus an optional downstream wake streak (+x is downstream on the main river)."""
    seg = 18; th = np.linspace(0, 2 * math.pi, seg, endpoint=False); ro = r1 * (0.85 + 0.35 * rs.rand(seg)); V = [(x, y, z)]
    V += [(x + r0 * math.cos(t), y + r0 * math.sin(t), z) for t in th]; V += [(x + o * math.cos(t), y + o * math.sin(t), z) for t, o in zip(th, ro)]
    F = [(1 + i, 1 + (i + 1) % seg, 1 + seg + (i + 1) % seg, 1 + seg + i) for i in range(seg)]; B.mesh('foam', V, F, False)
    if wake > 0:                                                  # one short V foam trail per pier: two tapering arms diverging downstream
        L = wake * STATE['P'].get('wake_k', 1.0)
        for sg in (-1, 1):
            B.mesh('foam', [(x + 0.1, y + sg * r0 * 0.6, z), (x + 0.1, y + sg * r0 * 1.5, z), (x + L, y + sg * (r0 * 1.2 + L * 0.34), z), (x + L * 0.55, y + sg * (r0 * 0.7 + L * 0.17), z)], [(0, 1, 2, 3)], False, tint=(0.95, 0.95, 0.95))
def build_bridge(A, pr):
    B = Batch(21); Bf = Batch(22); rs = np.random.RandomState(7); x0 = BRIDGE_X; y0, y1 = BRIDGE_Y0, BRIDGE_Y1; W = 2.6; dz = DECK_Z
    y = y0; 
    while y < y1 - 0.02:                                                # deck planks (across the deck), each its own tone
        pw = 0.24 + 0.06 * rs.rand(); t = 0.82 + 0.3 * rs.rand(); B.box('deck', (x0, y + pw / 2, dz - 0.06), (W, pw - 0.012, 0.12), tint=(t, t * 0.98, t * 0.94)); y += pw
    for ox in (-1.05, -0.35, 0.35, 1.05): B.box('wood_dk', (x0 + ox, (y0 + y1) / 2, dz - 0.27), (0.22, y1 - y0, 0.3))                      # stringers
    for sx in (-1, 1):                                                   # side kerb, posts, two rails
        B.box('wood', (x0 + sx * 1.38, (y0 + y1) / 2, dz + 0.06), (0.16, y1 - y0, 0.14))
        yy = y0 + 0.4
        while yy <= y1 - 0.3:
            B.box('wood', (x0 + sx * 1.40, yy, dz + 0.58), (0.17, 0.17, 1.12)); yy += 2.4
        B.box('wood', (x0 + sx * 1.40, (y0 + y1) / 2, dz + 1.08), (0.14, y1 - y0, 0.11)); B.box('wood', (x0 + sx * 1.40, (y0 + y1) / 2, dz + 0.62), (0.10, y1 - y0, 0.09))
    yb = y0 + 1.0; k = 0
    while yb < y1:                                                        # trestle bents
        for sx in (-1, 1):
            xp = x0 + sx * 1.15; zb = float(ground(xp, yb)) - 0.35; hgt = dz - 0.4 - zb
            B.box('wood_dk', (xp, yb, zb + hgt / 2), (0.34, 0.34, hgt)); B.rod('wood_dk', (xp + sx * 0.05, yb - 0.5, zb), (xp + sx * 0.5, yb, dz - 0.5), 0.12, seg=5)
            if zb < 0.2: foam_ring(Bf, xp, yb, 0.22, 0.55 + 0.1 * rs.rand(), rs, wake=2.5 + 2 * rs.rand())
        B.box('wood', (x0, yb, dz - 0.5), (3.3, 0.3, 0.26)); B.rod('wood', (x0 - 1.15, yb, max(0.9, float(ground(x0 - 1.15, yb)) + 0.9)), (x0 + 1.15, yb, dz - 1.2), 0.07, seg=4)
        B.box('wood', (x0, yb, max(0.9, float(ground(x0, yb)) + 0.9)), (2.4, 0.13, 0.13)) if float(ground(x0 - 1.15, yb)) < 0.2 else None
        yb += 6.0; k += 1
    # rail ends: gate posts (carved caps) at both ends
    for yy in (y0 + 0.1, y1 - 0.1):
        for sx in (-1, 1): B.box('wood', (x0 + sx * 1.45, yy, dz + 0.78), (0.24, 0.24, 1.5)); B.box('wood_dk', (x0 + sx * 1.45, yy, dz + 1.58), (0.30, 0.30, 0.1))
    B.finalize('bridge'); Bf.finalize('bridge_foam', ink=False, shadow=False)

# ---------------------------------------------------------------- horses and riders (3D low poly, local +x forward)
def horse(B, c, yaw=0.0, coat='horse', trap=None, trim=None, tint=1.0, rider=None, scale=1.0, bob=0.0):
    """a 15-hand horse, rest pose (bob lowers the head). trap/trim = caparison cloth materials; rider = (surcoat mat, helm?) tiny 3D rider for crowds."""
    t = tint if isinstance(tint, tuple) else (tint,) * 3
    with B.xf(c, (0, 0, yaw), scale):
        B.sphere(coat, (0, 0, 1.1), 0.5, seg=12, rings=7, scale=(2.0, 0.62, 0.8), tint=t); B.sphere(coat, (0.7, 0, 1.18), 0.42, seg=10, rings=6, scale=(1, 0.8, 1.0), tint=t)
        B.rod(coat, (0.8, 0, 1.3), (1.18, 0, 1.82 - bob), 0.19, seg=8, r2=0.12, tint=t); B.rod(coat, (1.16, 0, 1.84 - bob), (1.62, 0, 1.55 - bob * 1.2), 0.14, seg=7, r2=0.075, tint=t)
        for sy in (-1, 1): B.cone(coat, (1.2, sy * 0.07, 1.84 - bob), 0.05, 0.16, seg=4, tint=t)
        B.rod('mane', (0.78, 0, 1.52), (1.14, 0, 1.97 - bob), 0.06, seg=5)
        for sy in (-1, 1):
            for fx_ in (0.62, -0.64):
                if fx_ > 0: B.rod(coat, (fx_, sy * 0.17, 0.98), (fx_ + 0.02, sy * 0.17, 0.08), 0.085, seg=6, r2=0.05, tint=t)
                else: B.rod(coat, (fx_, sy * 0.18, 1.0), (fx_ - 0.17, sy * 0.17, 0.52), 0.1, seg=6, r2=0.06, tint=t); B.rod(coat, (fx_ - 0.17, sy * 0.17, 0.52), (fx_ - 0.02, sy * 0.17, 0.08), 0.06, seg=6, r2=0.045, tint=t)
                B.cyl('horse_dk', (fx_ + (0.02 if fx_ > 0 else -0.02), sy * 0.17, 0.045), 0.06, 0.09, seg=6)
        B.rod('mane', (-0.98, 0, 1.3), (-1.22, 0, 0.5), 0.08, seg=6, r2=0.035)
        B.box('leather', (0.05, 0, 1.52), (0.52, 0.42, 0.09))
        if trap:
            B.box(trap, (0.0, 0, 1.04), (1.72, 0.84, 0.6)); B.box(trim or trap, (0.0, 0, 0.77), (1.76, 0.86, 0.07)); B.box(trap, (0.98, 0, 1.0), (0.14, 0.7, 0.66)); B.box(trim or trap, (-1.02, 0, 0.98), (0.12, 0.74, 0.62))
            B.box(trim or trap, (0.0, 0, 1.36), (1.74, 0.87, 0.05))
        if rider:
            sur, steel = rider[0], 'steel'
            B.cyl(sur, (-0.05, 0, 1.93), 0.21, 0.62, seg=8, r2=0.17); B.sphere('steel', (-0.05, 0, 2.38), 0.14, seg=8, rings=5, scale=(1, 1, 1.12)); B.box(sur, (-0.05, 0, 1.62), (0.5, 0.6, 0.3))
            for sy in (-1, 1): B.rod('steel', (-0.05, sy * 0.3, 1.45), (0.1, sy * 0.36, 1.0), 0.07, seg=5)
def knight_pair_column(B, y_list, x, rs, mats):
    """two-by-two column of mounted knights along +y (facing north) on the deck."""
    for i, yy in enumerate(y_list):
        for sx in (-0.62, 0.62):
            m = mats[(i + (0 if sx < 0 else 1)) % len(mats)]; horse(B, (x + sx, yy, DECK_Z), 90.0, coat=['horse', 'horse_dk', 'horse'][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.85 + 0.3 * rs.rand(), rider=(m[0],))
KNIGHT_MATS = [('t_red', 't_gold'), ('t_blue', 't_gold'), ('t_cream', 't_red'), ('t_red', 't_white'), ('t_blue', 't_white')]

# ---------------------------------------------------------------- camp props
def ropes(B, c, r, hroof, hwall, n, rs, peg_r=1.9):
    for i in range(n):
        a = 2 * math.pi * (i + 0.3 * rs.rand()) / n; ex, ey = c[0] + r * 1.05 * math.cos(a), c[1] + r * 1.05 * math.sin(a); px, py = c[0] + (r + peg_r) * math.cos(a), c[1] + (r + peg_r) * math.sin(a)
        pz = float(ground(px, py)); B.rod('rope', (ex, ey, c[2] + hwall + 0.1), (px, py, pz + 0.1), 0.022, seg=4); B.rod('wood', (px, py, pz - 0.05), (px + 0.1 * math.cos(a), py + 0.1 * math.sin(a), pz + 0.32), 0.035, seg=4)
def pavilion(B, c, r, mats, yaw=0.0, hw=1.9, hr=2.6, seg=12, banner_pole=True, rs=None):
    """round pavilion: striped wall (alternating panels), striped conical roof, scalloped valance, a finial and guy ropes; c = ground centre."""
    rs = rs or np.random.RandomState(1); x, y, z = c; th = [2 * math.pi * i / seg + math.radians(yaw) for i in range(seg + 1)]
    for i in range(seg):
        m = mats[i % 2]; a0, a1 = th[i], th[i + 1]; p = lambda a, h, rr=r: (x + rr * math.cos(a), y + rr * math.sin(a), z + h)
        B.quad(m, p(a0, 0), p(a1, 0), p(a1, hw), p(a0, hw)); B.tri(m, p(a0, hw), p(a1, hw), (x + 0, y + 0, z + hw + hr), tint=1.0) if False else None
        rr2 = r * 1.18; B.mesh(m, [p(a0, hw, r), p(a1, hw, r), (x + rr2 * math.cos(a1), y + rr2 * math.sin(a1), z + hw - 0.0), (x + rr2 * math.cos(a0), y + rr2 * math.sin(a0), z + hw)], [(0, 1, 2, 3)], False)
        B.mesh(m, [(x + rr2 * math.cos(a0), y + rr2 * math.sin(a0), z + hw), (x + rr2 * math.cos(a1), y + rr2 * math.sin(a1), z + hw), (x, y, z + hw + hr)], [(0, 1, 2)], False)
        am = (a0 + a1) / 2; B.mesh(mats[(i + 1) % 2], [(x + rr2 * math.cos(a0), y + rr2 * math.sin(a0), z + hw - 0.02), (x + rr2 * math.cos(a1), y + rr2 * math.sin(a1), z + hw - 0.02), (x + (rr2 * 1.0) * math.cos(am), y + rr2 * math.sin(am), z + hw - 0.42)], [(0, 1, 2)], False)
    for i in range(seg):                                          # dark inner valance ring under the roof edge (reads as a tent from above)
        a0, a1 = th[i], th[i + 1]; rr2 = r * 1.18
        B.mesh('t_dark', [(x + rr2 * math.cos(a0), y + rr2 * math.sin(a0), z + hw - 0.03), (x + rr2 * math.cos(a1), y + rr2 * math.sin(a1), z + hw - 0.03), (x + r * 0.96 * math.cos(a1), y + r * 0.96 * math.sin(a1), z + hw - 0.5), (x + r * 0.96 * math.cos(a0), y + r * 0.96 * math.sin(a0), z + hw - 0.5)], [(0, 1, 2, 3)], False)
    da = math.radians(yaw) + 0.5 * 2 * math.pi / seg; B.quad('t_dark', (x + r * 1.01 * math.cos(da - 0.18), y + r * 1.01 * math.sin(da - 0.18), z), (x + r * 1.01 * math.cos(da + 0.18), y + r * 1.01 * math.sin(da + 0.18), z),
                                                       (x + r * 1.01 * math.cos(da + 0.12), y + r * 1.01 * math.sin(da + 0.12), z + 1.5), (x + r * 1.01 * math.cos(da - 0.12), y + r * 1.01 * math.sin(da - 0.12), z + 1.5))
    B.rod('wood', (x, y, z + hw + hr), (x, y, z + hw + hr + 1.6), 0.05, seg=5); B.sphere('gold', (x, y, z + hw + hr + 1.65), 0.16, seg=8, rings=5)
    pa = math.radians(yaw + 40); pc = (x, y, z + hw + hr + 1.5); pm = mats[0] if mats[0] != 't_cream' else mats[1]
    B.mesh(pm, [pc, (pc[0] + 1.5 * math.cos(pa), pc[1] + 1.5 * math.sin(pa), pc[2] - 0.15), (pc[0], pc[1], pc[2] - 0.55)], [(0, 1, 2)], False); B.mesh(pm, [pc, (pc[0], pc[1], pc[2] - 0.55), (pc[0] + 1.5 * math.cos(pa), pc[1] + 1.5 * math.sin(pa), pc[2] - 0.15)], [(0, 1, 2)], False)
    ropes(B, (x, y, z), r * 1.18, hr, hw, 8, rs)
def ridge_tent(B, c, w, d, h, mat, yaw=0.0, mat2=None):
    x, y, z = c; B.prism_roof(mat, (x, y, z), w, d, h, rot_z=yaw); 
    with B.xf((x, y, z), (0, 0, yaw)):
        for sy in (-1, 1): B.rod('wood', (0, sy * d / 2, 0), (0, sy * d / 2, h + 0.25), 0.04, seg=4)
        B.rod('wood', (-w / 2, 0, h + 0.2), (w / 2, 0, h + 0.2), 0.035, seg=4) if False else None
        B.quad('t_dark', (-0.01 - w * 0.12, -d / 2 - 0.01, 0), (w * 0.12, -d / 2 - 0.01, 0), (w * 0.08, -d / 2 - 0.01, h * 0.62), (-w * 0.08, -d / 2 - 0.01, h * 0.62))
def flag_live(base, h, yaw, field, charge, shape, rs, size):
    """a banner whose cloth can flutter per frame: built in local space (origin = the pole top) and given a Wave modifier; set_flutter(t) keys the phase."""
    Bl = Batch(rs.randint(0, 999)); Bl._local = True; x, y, z = base; banner(Bl, (0, 0, -h), h, 0.0, field, charge, shape, rs, size, wave=0.0)
    for ob in Bl.finalize('flag', loc=(x, y, z + h), ink=False, shadow=False):
        ob.rotation_euler = (0, 0, math.radians(yaw)); md = ob.modifiers.new('flutter', 'WAVE'); md.use_normal = True; md.use_x = True; md.use_y = False; md.height = 0.16 * size[1] / 1.3; md.width = 1.1; md.narrowness = 1.6; md.speed = 0.25
        md.start_position_x = -0.5; md.falloff_radius = 0.0; md.time_offset = 0.0; STATE['anim'].setdefault('flags', []).append((ob.name, md.name, rs.uniform(0, 6.28), md.height))
def banner(B, base, h, yaw, field, charge, shape, rs, size=(1.9, 1.3), wave=0.12):
    if not getattr(B, '_local', False) and STATE['P'].get('live_banners', True): return flag_live(base, h, yaw, field, charge, shape, rs, size)
    """a banner on a pole: swallow-tailed cloth with a simple charge (chevron, bend stripes, cross, bars); no text. Rippled mesh so it reads as blown."""
    x, y, z = base; B.rod('wood', (x, y, z - 0.1), (x, y, z + h), 0.055, seg=6); B.sphere('gold', (x, y, z + h + 0.08), 0.1, seg=6, rings=4)
    ca, sa = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); fw, fh = size; zt = z + h - 0.15; nx = 8
    def pt(u, v, ph=0.0):                     # u 0..1 along the flag (from the pole), v 0..1 down; wave displaces sideways
        w_ = wave * math.sin(u * 5.0 + ph) * u * fw * 0.5; return (x + (u * fw) * ca - w_ * sa, y + (u * fw) * sa + w_ * ca, zt - v * fh - 0.04 * u * math.sin(u * 4 + ph))
    ph = rs.rand() * 6
    def strip(mat, v0, v1, u0=0.0, u1=1.0, tail=True):
        us = np.linspace(u0, u1, nx + 1)
        for i in range(nx):
            ua, ub = us[i], us[i + 1]; B.mesh(mat, [pt(ua, v0, ph), pt(ub, v0, ph), pt(ub, v1, ph), pt(ua, v1, ph)], [(0, 1, 2, 3)], False)
    def notch(mat):                           # the swallow-tail notch drawn as a sky-side triangle is skipped; the tail is cut by the last strip
        pass
    strip(field, 0.0, 1.0, 0.0, 0.88)
    B.mesh(field, [pt(0.88, 0.0, ph), pt(1.0, 0.0, ph), pt(0.9, 0.5, ph), pt(1.0, 1.0, ph), pt(0.88, 1.0, ph)], [(0, 1, 2, 4), (4, 2, 3)], False)
    e = 0.012
    def over(mat, quads):
        for q in quads: B.mesh(mat, [(*pt(*p_, ph),) for p_ in q], [(0, 1, 2, 3)], False)
    if shape == 'chevron':
        over(charge, [[(0.0, 0.2), (0.45, 0.55), (0.45, 0.78), (0.0, 0.43)], [(0.45, 0.55), (0.9, 0.2), (0.9, 0.43), (0.45, 0.78)]])
    elif shape == 'bars':
        for k in range(3): over(charge, [[(0.0, 0.14 + 0.3 * k), (0.86, 0.14 + 0.3 * k), (0.86, 0.26 + 0.3 * k), (0.0, 0.26 + 0.3 * k)]])
    elif shape == 'cross':
        over(charge, [[(0.0, 0.40), (0.88, 0.40), (0.88, 0.60), (0.0, 0.60)], [(0.30, 0.0), (0.46, 0.0), (0.46, 1.0), (0.30, 1.0)]])
    elif shape == 'bend':
        over(charge, [[(0.0, 0.0), (0.3, 0.0), (0.9, 0.8), (0.9, 1.0), (0.6, 1.0), (0.0, 0.2)][:4] and [(0.0, 0.05), (0.28, 0.0), (0.88, 0.92), (0.6, 0.98)]])
    elif shape == 'saltire':                  # the Scots' blue banner: a white diagonal cross
        over(charge, [[(0.0, 0.0), (0.14, 0.0), (0.88, 1.0), (0.74, 1.0)], [(0.74, 0.0), (0.88, 0.0), (0.14, 1.0), (0.0, 1.0)]])
    elif shape == 'lion':                      # a rampant-lion stand-in: a gold block body, head and three small legs, no detail
        over(charge, [[(0.18, 0.25), (0.55, 0.25), (0.55, 0.75), (0.18, 0.75)], [(0.55, 0.2), (0.75, 0.2), (0.75, 0.42), (0.55, 0.42)], [(0.3, 0.75), (0.4, 0.75), (0.4, 0.95), (0.3, 0.95)], [(0.5, 0.75), (0.6, 0.75), (0.6, 0.95), (0.5, 0.95)]])
def barrel(B, c, r=0.34, h=0.85, rs=None):
    x, y, z = c; B.cyl('barrel', (x, y, z + h / 2), r, h, seg=12, r2=r, smooth=True); B.cyl('barrel', (x, y, z + h / 2), r * 1.08, h * 0.5, seg=12, r2=r * 1.08, caps=False)
    for zz in (0.12, 0.38, 0.62): B.cyl('iron', (x, y, z + h * zz / 0.75 * 0.75 + 0.02), r * 1.1, 0.045, seg=12, caps=False)
def sacks(B, c, n, rs):
    x, y, z = c
    for i in range(n):
        ox, oy = rs.uniform(-0.5, 0.5, 2); B.sphere('sack', (x + ox, y + oy, z + 0.22 + 0.3 * (i // 3)), 0.3, seg=8, rings=5, scale=(1, 0.85, 0.85), tint=(0.85 + 0.3 * rs.rand(),) * 3)
def cart(B, c, yaw, rs, cover=True):
    x, y, z = c
    with B.xf((x, y, z), (0, 0, yaw)):
        B.box('wood', (0, 0, 0.95), (2.8, 1.5, 0.12)); B.box('wood', (0, 0.74, 1.25), (2.8, 0.07, 0.5)); B.box('wood', (0, -0.74, 1.25), (2.8, 0.07, 0.5)); B.box('wood', (1.4, 0, 1.25), (0.07, 1.5, 0.5)); B.box('wood', (-1.4, 0, 1.25), (0.07, 1.5, 0.5))
        B.rod('wood_dk', (-1.4, 0, 0.62), (1.4, 0, 0.62), 0.05, seg=5); B.rod('wood_dk', (1.4, 0, 0.9), (3.4, 0, 0.55), 0.06, seg=5); B.rod('wood_dk', (1.4, 0.3, 0.9), (3.4, 0.3, 0.55), 0.04, seg=5)
        for sy in (-1, 1):
            cy = sy * 0.92; B.cyl('wood_dk', (0, cy, 0.62), 0.62, 0.1, axis='y', seg=14, smooth=False); B.cyl('iron', (0, cy + sy * 0.02, 0.62), 0.655, 0.05, axis='y', seg=14, smooth=False, caps=False)
            for k in range(4): a = k * 45; B.box('wood', (0, cy, 0.62), (1.2, 0.07, 0.07), rot=(0, a, 0))
        if cover:
            for k in range(5): xx = -1.1 + k * 0.55; B.rod('wood', (xx, -0.72, 1.5), (xx, 0, 2.1), 0.03, seg=4); B.rod('wood', (xx, 0.72, 1.5), (xx, 0, 2.1), 0.03, seg=4)
            for sy in (-1, 1): B.mesh('t_cream', [(-1.3, sy * 0.74, 1.5), (1.3, sy * 0.74, 1.5), (1.3, 0, 2.15), (-1.3, 0, 2.15)], [(0, 1, 2, 3)], False)
        else:
            for k in range(5): B.sphere('sack', (-0.8 + k * 0.4, 0.2 * (k % 2), 1.3), 0.3, seg=7, rings=4, scale=(1, 1, 0.8))
def weapon_rack(B, c, yaw, rs, n=7):
    x, y, z = c
    with B.xf((x, y, z), (0, 0, yaw)):
        for sx in (-1.0, 1.0): B.rod('wood', (sx, -0.3, 0), (sx, 0, 1.55), 0.05, seg=5); B.rod('wood', (sx, 0.3, 0), (sx, 0, 1.55), 0.05, seg=5)
        B.rod('wood', (-1.0, 0, 1.5), (1.0, 0, 1.5), 0.045, seg=5); B.rod('wood', (-1.0, 0, 0.6), (1.0, 0, 0.6), 0.04, seg=5)
        for i in range(n): xx = -0.85 + i * 1.7 / (n - 1); spear(B, (xx, rs.uniform(-0.05, 0.05), 0.02), tilt=(rs.uniform(-0.2, 0.2), rs.uniform(-0.1, 0.1)), h=2.5)
        for i in range(2): B.cyl('t_red' if i == 0 else 't_blue', (-0.4 + i * 0.8, -0.22, 0.45), 0.34, 0.06, axis='y', seg=12, smooth=False)
def campfire(B, Bs, c, rs, puffs=True):
    x, y, z = c
    for i in range(9): a = i * 2 * math.pi / 9; boulder(B, x + 0.62 * math.cos(a), y + 0.62 * math.sin(a), z, 0.26, rs, 'rock')
    for i in range(4): a = i * 45 + 10; B.rod('bark', (x + 0.4 * math.cos(math.radians(a)), y + 0.4 * math.sin(math.radians(a)), z + 0.12), (x - 0.4 * math.cos(math.radians(a)), y - 0.4 * math.sin(math.radians(a)), z + 0.28), 0.07, seg=5)
    for k in range(3): B.cone('flame', (x + rs.uniform(-0.12, 0.12), y + rs.uniform(-0.12, 0.12), z + 0.2), 0.2 - 0.04 * k, 0.75 + 0.3 * rs.rand() - 0.1 * k, seg=6)
    for sy in range(3): a = sy * 2.1; B.rod('wood', (x + 1.0 * math.cos(a), y + 1.0 * math.sin(a), z), (x + 0.05 * math.cos(a), y + 0.05 * math.sin(a), z + 2.0), 0.04, seg=5)
    B.rod('iron', (x, y, z + 1.9), (x, y, z + 1.0), 0.012, seg=4); B.sphere('iron', (x, y, z + 0.85), 0.26, seg=10, rings=6, scale=(1, 1, 0.85)); B.cyl('iron', (x, y, z + 1.05), 0.2, 0.05, seg=10)
    if puffs: smoke_column(Bs, x, y, z, rs, h=7.0, r0=0.2, n=7)
    for i in range(0):
        t = i / 6.0; Bs.sphere('smoke', (x + 0.4 + 2.2 * t * t + rs.uniform(-0.2, 0.2), y + 0.3 + 1.6 * t * t, z + 2.6 + 5.8 * t), 0.22 + 0.4 * t, seg=9, rings=5, tint=(1.0 - 0.1 * t,) * 3)
def table_set(A, B, c, yaw, rs):
    """Cressingham's money table under a striped canopy: red-clothed trestle table, iron-banded coin chest (lid on its own hinge object), balance scales (beam on its
    own pivot object), coin stacks, loose coins, a blank open ledger. c = ground point under the table centre, local +x along the table's length."""
    x, y, z = c; Bl = Batch(31); Bs = Batch(32); ca_, sa_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    tw = lambda p: (x + p[0] * ca_ - p[1] * sa_, y + p[0] * sa_ + p[1] * ca_, z + p[2])           # table-local -> world
    with B.xf((x, y, z), (0, 0, yaw)):
        for sx in (-0.9, 0.9):
            for sy in (-0.4, 0.4): B.rod('wood', (sx + sx * 0.05, sy * 1.2, 0), (sx, sy, 0.9), 0.045, seg=5)
        B.box('wood', (0, 0, 0.93), (2.3, 1.0, 0.07)); B.box('cloth_red', (0, 0, 0.985), (2.38, 1.06, 0.035)); B.box('cloth_red', (0, -0.53, 0.8), (2.38, 0.035, 0.3)); B.box('gold', (0, -0.545, 0.69), (2.38, 0.02, 0.05)); B.box('gold', (0, 0.0, 1.01), (2.38, 0.05, 0.012))
        # chest + coins
        cx, cy_ = -0.92, -0.05; B.box('barrel', (cx, cy_, 1.22), (1.0, 0.62, 0.46)); B.box('iron', (cx + 0.2, cy_ - 0.32, 1.22), (0.07, 0.02, 0.48)); B.box('iron', (cx - 0.2, cy_ - 0.32, 1.22), (0.07, 0.02, 0.48)); B.box('gold', (cx, cy_ - 0.325, 1.32), (0.12, 0.02, 0.14)); B.box('iron', (cx + 0.34, cy_, 1.225), (0.08, 0.64, 0.48)); B.box('iron', (cx - 0.34, cy_, 1.225), (0.08, 0.64, 0.48))
        B.box('gold', (cx, cy_, 1.46), (0.88, 0.5, 0.05))
        for i in range(10): B.sphere('gold', (cx + rs.uniform(-0.34, 0.34), cy_ + rs.uniform(-0.2, 0.2), 1.5 + 0.03 * rs.rand()), 0.09, seg=6, rings=4, scale=(1, 1, 0.5))
        # coin stacks in neat rows
        for i in range(8):
            for j, m in enumerate(('gold', 'silver')):
                if rs.rand() < 0.15: continue
                n = rs.randint(2, 8); px, py = 0.15 + i * 0.13, 0.28 - j * 0.2
                B.cyl(m, (px, py, 1.0 + n * 0.0115), 0.052, n * 0.023, seg=10)
        for i in range(10): B.cyl('gold', (rs.uniform(0.1, 1.05), rs.uniform(-0.42, 0.42), 1.012), 0.05, 0.008, seg=8)
        # ledger (no text): cover + two pages
        B.box('leather', (0.55, -0.22, 1.012), (0.6, 0.4, 0.03)); B.box('cream', (0.42, -0.22, 1.032), (0.28, 0.36, 0.015), rot=(0, 0, 2)); B.box('cream', (0.68, -0.22, 1.032), (0.28, 0.36, 0.015), rot=(0, 0, -2))
        for i in range(5): B.box('gold', (0.55, -0.4 + i * 0.1, 0.86), (0.0, 0.0, 0.0)) if False else None
        # canopy: four poles + a striped roof (its own batch: the roof casts no shadow, so the table is lit)
        Bc = Batch(34); Bc.stack[-1] = B.stack[-1].copy()
        for sx in (-1.5, 1.5):
            for sy in (-1.2, 1.2): B.rod('wood', (sx, sy, -0.1), (sx, sy, 3.5), 0.055, seg=6)
        seg = 8; r = 2.5; hz = 3.5
        for i in range(seg):
            a0 = 2 * math.pi * i / seg + math.pi / 4; a1 = 2 * math.pi * (i + 1) / seg + math.pi / 4; m = ('t_blue', 't_gold')[i % 2]
            Bc.mesh(m, [(r * 1.0 * math.cos(a0) * 1.0, r * 0.82 * math.sin(a0), hz), (r * math.cos(a1), r * 0.82 * math.sin(a1), hz), (0, 0, hz + 0.9)], [(0, 1, 2)], False)
            Bc.mesh(m, [(r * math.cos(a0), r * 0.82 * math.sin(a0), hz), (r * math.cos(a1), r * 0.82 * math.sin(a1), hz), (r * math.cos(a1), r * 0.82 * math.sin(a1), hz - 0.5), (r * math.cos(a0), r * 0.82 * math.sin(a0), hz - 0.5)], [(0, 1, 2, 3)], False)
        Bc.sphere('gold', (0, 0, hz + 1.0), 0.14, seg=8, rings=5)
        with Bl.xf((0, 0, 0)): pass
    Bc.finalize('table_canopy', shadow=False)
    # chest lid: own object, hinge at the back-top edge of the chest, open 72 degrees
    cx, cy_ = -0.92, -0.05; hp = tw((cx, cy_ + 0.31, 1.47)); Bl.box('barrel', (0, -0.31, 0.045), (1.0, 0.64, 0.09)); Bl.box('iron', (0.34, -0.31, 0.055), (0.08, 0.66, 0.11)); Bl.box('iron', (-0.34, -0.31, 0.055), (0.08, 0.66, 0.11)); Bl.box('gold', (0, -0.31, 0.1), (0.8, 0.5, 0.02))
    lid = Bl.finalize('chest_lid', loc=hp)[0]; lid.rotation_euler = (math.radians(-72), 0, math.radians(yaw)); lid.rotation_mode = 'XYZ'
    A['chest_lid'] = lid.name; A['chest_lid_hinge'] = hp
    # scales: stand on the table, beam on a pivot object
    sp = tw((1.30, -0.12, 1.0)); Bs.rod('wood_dk', (0, 0, 0), (0, 0, 0.8), 0.05, seg=6); Bs.box('wood_dk', (0, 0, 0.0), (0.3, 0.3, 0.06)); Bs.sphere('gold', (0, 0, 0.83), 0.07, seg=6, rings=4)
    Bs.finalize('scale_stand', loc=sp); Bb = Batch(33); Bb.box('gold', (0, 0, 0), (1.0, 0.055, 0.055))
    for sxx in (-0.5, 0.5): Bb.rod('rope', (sxx, 0, 0), (sxx, 0, -0.34), 0.012, seg=3); Bb.cyl('steel', (sxx, 0, -0.37), 0.18, 0.03, seg=14, r2=0.18)
    beam = Bb.finalize('scale_beam', loc=(sp[0], sp[1], sp[2] + 0.83), ink=True)[0]; beam.rotation_euler = (0, math.radians(0), math.radians(yaw)); A['scale_beam'] = beam.name

# ================================================================ SCENE: castle, hill, meadow, camp
def bank_y(x):
    R = river(); p, w, _ = R['main']; yc = np.interp(x, p[:, 0], p[:, 1]); hw = np.interp(x, p[:, 0], w) / 2.0; return yc - hw + WATER_EDGE      # south waterline
def build_castle(A, pr):
    """Stirling castle, seen small and far (13th c.): a curtain wall with round corner towers and conical roofs, a keep and a gatehouse on the rock top."""
    B = Batch(41); wx, wy = CASTLE_C; z0w = float(land_height(np.array([wx]), np.array([wy]), np.array([1e3]))[0][0]) - 0.5; cx = cy = z0 = 0.0; rs = np.random.RandomState(4); B.stack.append(_m4((wx, wy, z0w), (0, 0, 0), 0.72))
    hs = [(-22, -16), (22, -16), (24, 14), (-20, 16)]
    for i in range(4):
        a, b = hs[i], hs[(i + 1) % 4]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; L = math.hypot(b[0] - a[0], b[1] - a[1]); ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        B.box('castle', (cx + mx, cy + my, z0 + 5), (L, 2.4, 10), rot=(0, 0, ang))
        for k in range(int(L / 3)): B.box('castle', (cx + a[0] + (b[0] - a[0]) * (k + 0.5) / int(L / 3), cy + a[1] + (b[1] - a[1]) * (k + 0.5) / int(L / 3), z0 + 10.8), (1.6, 2.6, 1.4), rot=(0, 0, ang))
    for (tx, ty), h in zip(hs, (16, 14, 17, 14)):
        B.cyl('castle', (cx + tx, cy + ty, z0 + h / 2), 3.6, h, seg=12); B.cone('t_dark', (cx + tx, cy + ty, z0 + h), 4.3, 7.5, seg=12); B.rod('wood', (cx + tx, cy + ty, z0 + h + 7.5), (cx + tx, cy + ty, z0 + h + 10), 0.1, seg=4)
    B.box('castle', (cx + 2, cy + 3, z0 + 12), (13, 12, 24)); B.cone('t_dark', (cx + 2, cy + 3, z0 + 24), 10, 6, seg=4); B.box('castle', (cx - 12, cy - 17, z0 + 7), (8, 6, 14)); B.cone('t_dark', (cx - 12, cy - 17, z0 + 14), 6, 6, seg=4)
    B.finalize('castle', ink=False)
def hill_dress(A, pr):
    """Abbey Craig: Scots pines on the skirts and crags, boulders and crag groups, bracken, a few birches."""
    if pr and pr.get('hill2'): return
    B = Batch(42); Br = Batch(43); rs = np.random.RandomState(9)
    n = 0; tries = 0
    while n < 90 and tries < 4000:
        tries += 1; x = HILL_C[0] + rs.uniform(-120, 105); y = HILL_C[1] + rs.uniform(-95, 90); hh, cm = hill_h(np.array([x]), np.array([y])); hh = float(hh[0]); sd = float(sd_at(x, y))
        if hh < 3 or sd < 4: continue
        e = 1.0; sl = math.hypot(float((hill_h(np.array([x + e]), np.array([y]))[0] - hill_h(np.array([x - e]), np.array([y]))[0])[0]) / (2 * e), float((hill_h(np.array([x]), np.array([y + e]))[0] - hill_h(np.array([x]), np.array([y - e]))[0])[0]) / (2 * e))
        if sl > 0.8: continue
        clear = pr and pr.get('clear_hill') and math.hypot(x - pr['clear_hill'][0], y - pr['clear_hill'][1]) < pr['clear_hill'][2]
        if clear: continue
        if rs.rand() < 0.55 and hh < 22: continue
        z = float(ground(x, y)); pine(B, x, y, z, rs.uniform(8, 14), rs, lean=rs.uniform(0, 0.12)); n += 1
    for i in range(45):                                         # lone oaks / birch on the lower skirts
        x = HILL_C[0] + rs.uniform(-115, 20); y = HILL_C[1] + rs.uniform(-95, 20); hh = float(hill_h(np.array([x]), np.array([y]))[0][0])
        if 0.5 < hh < 9 and float(sd_at(x, y)) > 5: oak(B, x, y, float(ground(x, y)), rs.uniform(5, 8), rs)
    for i in range(70):                                         # boulders and crag groups over the hill
        x = HILL_C[0] + rs.uniform(-110, 100); y = HILL_C[1] + rs.uniform(-90, 85); hh, cm = hill_h(np.array([x]), np.array([y]))
        if float(hh[0]) > 4 and float(sd_at(x, y)) > 3:
            if float(cm[0]) > 0.15 or rs.rand() < 0.25: crag_group(Br, x, y, rs, n=rs.randint(3, 8), spread=rs.uniform(2, 5), s=rs.uniform(1.4, 3.2))
            else: boulder(Br, x, y, float(ground(x, y)), rs.uniform(0.7, 2.0), rs)
    B.finalize('hill_trees', ink=False); Br.finalize('hill_rocks', ink=False)
def meadow_dress(A, pr):
    """the bottle meadow, the neck and the riverbanks: oaks along the water, hay stacks, a few cairns, willows at the loop water, woodlots on the plains."""
    B = Batch(44); rs = np.random.RandomState(12); Br = Batch(45)
    for i in range(46):                                         # trees along the loop's outer bank and in the plains
        a = rs.uniform(0, 2 * math.pi); r = LOOP_R + rs.uniform(24, 70); x = LOOP_C[0] + r * math.cos(a); y = LOOP_C[1] + r * math.sin(a) * 1.0
        hh = float(hill_h(np.array([x]), np.array([y]))[0][0])
        if float(sd_at(x, y)) > 6 and hh < 1.0 and y > 22: oak(B, x, y, float(ground(x, y)), rs.uniform(5, 9), rs)
    for i in range(34):                                         # inner bank trees on the meadow
        a = rs.uniform(0, 2 * math.pi); r = LOOP_R - 22 - rs.uniform(0, 10); x = LOOP_C[0] + r * math.cos(a); y = LOOP_C[1] + r * math.sin(a)
        if y > 52 and float(sd_at(x, y)) > 5: oak(B, x, y, float(ground(x, y)), rs.uniform(4, 7), rs)
    for i in range(70):                                         # plains woodlots: groups of 3-6 trees, far off
        x = rs.uniform(-230, 330); y = rs.uniform(-190, 330); hh = float(hill_h(np.array([x]), np.array([y]))[0][0])
        if float(sd_at(x, y)) < 12 or hh > 1.0 or (y > 20 and math.hypot(x - LOOP_C[0], y - LOOP_C[1]) < LOOP_R + 26) or (-100 < y < 2 and abs(x) < 25) or (abs(x) < 130 and -110 < y < -22): continue
        for k in range(rs.randint(2, 6)):
            xx = x + rs.uniform(-9, 9); yy = y + rs.uniform(-9, 9)
            if float(sd_at(xx, yy)) > 6: (pine if rs.rand() < 0.25 else oak)(B, xx, yy, float(ground(xx, yy)), rs.uniform(5, 11), rs) if False else oak(B, xx, yy, float(ground(xx, yy)), rs.uniform(5, 9), rs)
    for i in range(8):                                          # hay stacks on the meadow
        a = rs.uniform(0, 2 * math.pi); r = rs.uniform(30, 62); x = LOOP_C[0] + r * math.cos(a); y = LOOP_C[1] + r * math.sin(a)
        if y > 60: z = float(ground(x, y)); B.cone('hay', (x, y, z - 0.1), 1.5, 2.2, seg=8, smooth_=True) if False else B.sphere('hay', (x, y, z + 0.9), 1.4, seg=10, rings=6, scale=(1, 1, 0.9)); B.rod('wood', (x, y, z), (x, y, z + 2.6), 0.05, seg=4)
    for i in range(30): x = rs.uniform(-120, 120); y = rs.uniform(-130, -24); boulder(Br, x, y, float(ground(x, y)), rs.uniform(0.4, 1.0), rs) if (float(sd_at(x, y)) > 5 and abs(x) > 12) else None
    B.finalize('meadow_trees', ink=False); Br.finalize('meadow_rocks', ink=False)
def build_camp(A, pr):
    """the English camp along the south bank: pavilions (red/cream, blue/gold), ridge tents, banners, horse lines, carts, a campfire with a pot and smoke, weapon racks,
    barrels and sacks, Cressingham's money table by the road. Anchors in A['camp']."""
    B = Batch(51); Bs = Batch(52); Bh = Batch(53); rs = np.random.RandomState(5); camp = {}; bn = (lambda *a_, **k_: None) if (pr or {}).get('camp_banners') is False else banner; clear = (pr or {}).get('clear', [])
    free = lambda x, y, r=0.0: all(math.hypot(x - cx, y - cy) > cr + r for cx, cy, cr in clear)
    PAV = [(-96, 8, 3.6), (-72, 10, 4.0), (-48, 8, 3.8), (-26, 22, 4.4), (24, 9, 4.0), (48, 12, 3.8), (74, 8, 4.2), (98, 11, 3.6), (-60, 30, 3.6), (-12, 36, 5.0), (30, 34, 4.4), (66, 36, 3.8), (-86, 34, 3.6), (92, 36, 3.6)]
    for i, (x, off, r) in enumerate(PAV):
        by = float(bank_y(x)); y = by - off - r; z = float(ground(x, y)); mats = (('t_red', 't_cream'), ('t_blue', 't_gold'))[i % 2]
        if not free(x, y, r + 2): continue
        pavilion(B, (x, y, z), r, mats, yaw=rs.uniform(0, 30), rs=rs, hw=1.8 + 0.2 * rs.rand(), hr=3.2 + 0.7 * rs.rand())
        if i % 2 == 0 or r > 4.3: bn(Bh, (x + r * 0.6, y + r * 0.2, z), 6.5 + rs.rand() * 1.5, rs.uniform(-20, 60), *[('t_red', 't_gold', 'chevron'), ('t_blue', 't_gold', 'bars'), ('t_cream', 't_red', 'cross'), ('t_gold', 't_red', 'lion'), ('t_green', 't_cream', 'bend')][i % 5], rs)
        sacks(B, (x + r + 1.0, y - 1.5, z), 3, rs); barrel(B, (x - r - 0.8, y - 2.0, z), rs=rs)
    camp['pav'] = PAV
    for i, (x, y, r) in enumerate([(-24.0, -38.0, 3.6), (-14.0, -44.0, 3.9), (-38.0, -58.0, 4.2), (-6.0, -62.0, 4.6), (-6.0, -35.5, 4.2)]):          # the plaza pavilions
        if not free(x, y, r + 2): continue
        z = float(ground(x, y)); pavilion(B, (x, y, z), r, (('t_blue', 't_gold'), ('t_red', 't_cream'))[i % 2], yaw=rs.uniform(0, 30), rs=rs, hw=1.9, hr=3.4)
        bn(Bh, (x + r * 0.7, y - r * 0.3, z), 7.0, rs.uniform(10, 70), *[('t_gold', 't_red', 'lion'), ('t_blue', 't_gold', 'bars'), ('t_red', 't_gold', 'chevron'), ('t_cream', 't_red', 'cross')][i % 4], rs)
        sacks(B, (x + r + 1.0, y - 1.0, z), 3, rs); barrel(B, (x - r - 0.9, y - 1.5, z), rs=rs)
    for (x, y, yaw) in [(-31.0, -42.0, 20), (-19.0, -50.0, 80), (-45.0, -46.0, 10)]:
        if free(x, y, 4): cart(B, (x, y, float(ground(x, y))), yaw, rs, cover=rs.rand() < 0.5)
    for (x, y, yaw) in [(-20.0, -33.0, 70), (-9.0, -52.0, 10)]:
        if free(x, y, 3): weapon_rack(B, (x, y, float(ground(x, y))), yaw, rs)
    for (x, y, yaw) in [(-44.0, -36.0, 30), (-34.0, -33.0, -20), (-47.0, -54.0, 0)]:
        if free(x, y, 4): ridge_tent(B, (x, y, float(ground(x, y))), 3.6, 3.0, 2.0, ['t_cream', 't_white', 't_brown'][int(abs(x)) % 3], yaw=yaw)
    if free(-28.0, -52.0, 3): campfire(B, Bs, (-28.0, -52.0, float(ground(-28.0, -52.0))), rs)
    cl = [(-100, 30), (-62, 62), (-20, 46), (28, 40), (66, 70), (104, 36), (-84, 98), (60, 112)]           # tent clusters with lanes between them
    for ci, (cx_, off_) in enumerate(cl):
        for i in range(rs.randint(14, 22)):
            x = cx_ + rs.uniform(-13, 13); off = off_ + rs.uniform(-9, 9); y = float(bank_y(x)) - off
            if abs(x) < 9 or float(sd_at(x, y)) < 5 or not free(x, y, 3): continue
            z = float(ground(x, y)); m = ['t_cream', 't_brown', 't_cream', 't_gold', 't_red', 't_white', 't_green'][rs.randint(0, 7)]; sz = rs.uniform(0.8, 1.35)
            if rs.rand() < 0.35: bell_tent(B, (x, y, z), 1.8 * sz, 2.8 * sz, m, rs)
            else: ridge_tent(B, (x, y, z), 3.6 * sz, 2.9 * sz, 2.0 * sz, m, yaw=rs.choice([0, 90, 20, -25, 70]) + rs.uniform(-8, 8))
    for i, (x, off) in enumerate([(-130, 24), (-110, 6), (116, 12), (130, 34), (-60, 52), (50, 58), (4, 62), (-34, 60)]):          # more banners on the skirts
        y = float(bank_y(x)) - off; bn(Bh, (x, y, float(ground(x, y))), 7.0, rs.uniform(-20, 60), *[('t_red', 't_gold', 'chevron'), ('t_blue', 't_gold', 'bars'), ('t_cream', 't_red', 'cross'), ('t_gold', 't_red', 'lion')][i % 4], rs)
    for (x, off, yaw) in [(-34, 26, 20), (44, 24, -10), (84, 28, 80), (-76, 28, 5), (10, 40, 30)]:
        y = float(bank_y(x)) - off
        if free(x, y, 4): cart(B, (x, y, float(ground(x, y))), yaw, rs, cover=rs.rand() < 0.6)
    for (x, off, yaw) in [(-14, 14, 90), (16, 14, 90), (-42, 18, 10), (58, 20, -10)]:
        y = float(bank_y(x)) - off
        if free(x, y, 3): weapon_rack(B, (x, y, float(ground(x, y))), yaw, rs)
    for (x, off) in [(-18, 34), (34, 46)]:
        y = float(bank_y(x)) - off
        if free(x, y, 3): campfire(B, Bs, (x, y, float(ground(x, y))), rs); camp.setdefault('fires', []).append((x, y))
    # horse lines: a rope between stakes with 7 tethered horses, alternating coats, a few caparisoned
    for ly, (x0_, x1_) in enumerate([(52, 96), (-100, -58)]):
        off = 52 + 8 * ly; y = float(bank_y((x0_ + x1_) / 2)) - off; n = 7; xs = np.linspace(x0_, x1_, n)
        zl = [float(ground(x_, y)) for x_ in xs]
        for i, x_ in enumerate(xs):
            B.rod('wood', (x_ - 2.6, y + 0.2, zl[i]), (x_ - 2.6, y + 0.2, zl[i] + 1.6), 0.06, seg=5)
            horse(B, (x_, y + (1.2 if i % 2 else -0.2), zl[i]), rs.uniform(70, 110) if i % 2 == 0 else rs.uniform(250, 290), coat=['horse', 'horse_dk', 'horse', 'horse'][rs.randint(0, 4)], trap=(None, 't_red', None, 't_blue', 't_cream', None, 't_red')[i], trim='t_gold', tint=0.8 + 0.4 * rs.rand(), bob=rs.uniform(0, 0.25))
        B.rod('rope', (xs[0] - 2.6, y + 0.2, zl[0] + 1.5), (xs[-1] - 2.6, y + 0.2, zl[-1] + 1.5), 0.02, seg=3)
    # Cressingham's money table by the road, west side, facing the river
    tx, toff = -13.0, 8.5; ty = float(bank_y(tx)) - toff; tz = float(ground(tx, ty)); table_set(A, B, (tx, ty, tz), 0.0, rs); camp['table'] = (tx, ty, tz)
    barrel(B, (tx + 3.5, ty + 0.5, tz))
    for (x, off) in [(-72, 20), (70, 26), (-104, 44), (40, 70), (96, 50)]:
        y = float(bank_y(x)) - off
        if free(x, y, 3): campfire(B, Bs, (x, y, float(ground(x, y))), rs); smoke_column(Bs, x, y, float(ground(x, y)), rs, h=24.0, r0=0.5); camp.setdefault('fires', []).append((x, y))
    A['camp'] = camp; B.finalize('camp'); Bs.finalize('camp_smoke', ink=False); Bh.finalize('camp_banner', shadow=False)
def bell_tent(B, c, r, h, mat, rs, seg=9):
    """a small round bell tent: conical cloth, a door slit, a centre pole with a tip."""
    x, y, z = c; a0 = rs.uniform(0, 6.28)
    for i in range(seg):
        a, b = a0 + 2 * math.pi * i / seg, a0 + 2 * math.pi * (i + 1) / seg; m = mat if i % 3 else 't_brown' if mat == 't_cream' else 't_cream'
        B.mesh(m, [(x + r * math.cos(a), y + r * math.sin(a), z), (x + r * math.cos(b), y + r * math.sin(b), z), (x + r * 0.55 * math.cos(b), y + r * 0.55 * math.sin(b), z + h * 0.62), (x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), z + h * 0.62)], [(0, 1, 2, 3)], False)
        B.mesh(m, [(x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a), z + h * 0.62), (x + r * 0.55 * math.cos(b), y + r * 0.55 * math.sin(b), z + h * 0.62), (x, y, z + h)], [(0, 1, 2)], False)
    B.rod('wood', (x, y, z + h), (x, y, z + h + 0.5), 0.04, seg=4)
_PL_RINGS, _PL_SEG = 14, 9
def smoke_column(Bs, x, y, z, rs, h=26.0, r0=0.25, n=10):
    """a soft tapered smoke plume: one smooth tube that widens and thins out to a point at the top, leaning down-wind; set_smoke(t) makes it billow and drift."""
    R, G = _PL_RINGS, _PL_SEG; me = bpy.data.meshes.new('smoke_col'); me.from_pydata(np.zeros((R * G + 1, 3)).tolist(), [], [(i * G + j, i * G + (j + 1) % G, (i + 1) * G + (j + 1) % G, (i + 1) * G + j) for i in range(R - 1) for j in range(G)] + [((R - 1) * G + j, (R - 1) * G + (j + 1) % G, R * G) for j in range(G)]); me.update()
    me.polygons.foreach_set('use_smooth', [True] * len(me.polygons)); ca = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.ones((R * G + 1) * 4, np.float32))
    ob = bpy.data.objects.new('smoke_col', me); bpy.context.scene.collection.objects.link(ob); ob.data.materials.append(get_mat('smoke')); ob.visible_shadow = False
    STATE['anim'].setdefault('smoke', []).append(dict(ob=ob.name, base=(x, y, z), h=h, r0=r0, n=n, seed=float(rs.uniform(0, 6.28)))); _smoke_pose(STATE['anim']['smoke'][-1], 0.0)
def _smoke_pose(c, t, speed=0.12):
    R, G = _PL_RINGS, _PL_SEG; ob = bpy.data.objects[c['ob']]; x, y, z = c['base']; h = c['h']; out = np.empty((R * G + 1, 3)); ph = c['seed'] + t * speed * 6.28 * 2
    for i in range(R):
        s_ = i / (R - 1.0); w = 0.5 * s_ * s_ * h * 0.5; cx = x + 0.4 + 0.45 * h * s_ * s_ + 0.5 * math.sin(5.0 * s_ - ph) * s_ * (h / 14.0) ** 0.5; cy = y + 0.3 + 0.25 * h * s_ * s_ + 0.4 * math.cos(4.0 * s_ - 1.3 * ph) * s_ * (h / 14.0) ** 0.5
        rr = max(c['r0'] * (0.6 + 4.2 * s_ ** 0.8) * (1.0 - s_ ** 3) * (h / 14.0) ** 0.4, 0.02) * (1 + 0.12 * math.sin(7 * s_ + ph)); cz = z + 2.0 + h * s_
        for j in range(G): a = 2 * math.pi * j / G; out[i * G + j] = (cx + rr * math.cos(a), cy + rr * math.sin(a), cz)
    out[R * G] = (x + 0.4 + 0.45 * h, y + 0.3 + 0.25 * h, z + 2.0 + h * 1.02); ob.data.vertices.foreach_set('co', out.ravel()); ob.data.update()
def farmstead(B, Bs, x, y, rs, yaw=None):
    """a small farm: cream walls with a thatch or red-tile roof, a barn, a haystack, a few trees and a smoke column."""
    yaw = rs.uniform(0, 90) if yaw is None else yaw; z = float(ground(x, y))
    with B.xf((x, y, z), (0, 0, yaw)):
        B.box('castle', (0, 0, 1.6), (9.0, 5.0, 3.2)); B.prism_roof('thatch' if rs.rand() < 0.5 else 't_red', (0, 0, 3.1), 10.4, 6.2, 2.8, rot_z=0)
        B.box('t_dark', (0, -2.52, 1.0), (1.2, 0.1, 2.0)); B.box('wood', (-6.5, 4.5, 1.8), (6.0, 4.0, 3.6)); B.prism_roof('t_brown', (-6.5, 4.5, 3.5), 7.0, 5.0, 2.4, rot_z=0)
        B.box('cream', (3.0, 0.0, 4.0), (0.8, 0.8, 2.4)); B.sphere('hay', (6.5, 5.5, 1.2), 1.7, seg=9, rings=6, scale=(1, 1, 0.9)); B.sphere('hay', (9.0, 3.5, 1.0), 1.4, seg=9, rings=6, scale=(1, 1, 0.9))
    for k in range(4): xx = x + rs.uniform(-12, 12); yy = y + rs.uniform(-12, 12); oak(B, xx, yy, float(ground(xx, yy)), rs.uniform(5, 8), rs)
    smoke_column(Bs, x + 3.0 * math.cos(math.radians(yaw)), y + 3.0 * math.sin(math.radians(yaw)), z + 4.6, rs, h=22.0, r0=0.5)
def far_dress(A, pr):
    """the farmland: farmsteads, hedgerow lines on the field borders (small leaf mounds), tree lines, woodlots, haystacks on the fields."""
    if not pr or not pr.get('farms'): return
    B = Batch(46); Bs = Batch(47); rs = np.random.RandomState(14)
    for (fx, fy) in FARMS: farmstead(B, Bs, fx, fy, rs)
    rg = np.random.RandomState(15); X = rg.uniform(-300, 460, 900000); Y = rg.uniform(-240, 640, 900000); fid, he = vor_fields(X, Y); sd = river_query(X, Y)[0]
    hh = hill_h(X, Y)[0]; ex = (X / 80.0) ** 2 + ((Y - 125.0) / 92.0) ** 2; ok = (he < 0.5) & (sd > 6) & (hh < 2) & (ex > 1.2) & (~((np.abs(X) < 140) & (Y < -20) & (Y > -150))) & (np.hypot(X - 200, Y - 190) > 80)
    for (fx, fy) in FARMS: ok &= np.hypot(X - fx, Y - fy) > 14
    idx = np.nonzero(ok)[0]; rg.shuffle(idx); idx = idx[:3200]; v0, f0 = _ico()
    for i in idx:
        x, y = X[i], Y[i]; z = float(ground(x, y)); r = rg.uniform(1.0, 1.7)
        if rg.rand() < 0.3: oak(B, x, y, z, rg.uniform(6, 11), rg); continue
        V = v0 * np.array([r * 1.4, r * 1.4, r * 0.9]) + np.array([x, y, z + r * 0.45]); B.mesh('leaf', V, f0, False, tint=(0.55 + 0.25 * rg.rand(), 0.6 + 0.3 * rg.rand(), 0.5))
    for i in range(46):                                         # haystacks dotted on the fields
        x = rs.uniform(-280, 420); y = rs.uniform(-220, 420); fid2, he2 = vor_fields(np.array([x]), np.array([y]))
        if float(river_query(np.array([x]), np.array([y]))[0][0]) > 8 and float(hill_h(np.array([x]), np.array([y]))[0][0]) < 1 and (abs(x) > 150 or y > 230 or y < -170): B.sphere('hay', (x, y, float(ground(x, y)) + 0.9), 1.5, seg=8, rings=5, scale=(1, 1, 0.9))
    B.finalize('farms', ink=False); Bs.finalize('farm_smoke', ink=False)
def in_corridor(pr, X, Y, k=1.0):
    """True where a prop would block the view corridor from the lens toward its target (pr['corridor'] = (length, half-width at the lens))."""
    c = pr.get('corridor')
    if not c: return np.zeros(np.shape(X), bool)
    cam, look = pr['cam'], pr['look']; az = math.atan2(look[1] - cam[1], look[0] - cam[0]); fx, fy = math.cos(az), math.sin(az); d = (X - cam[0]) * fx + (Y - cam[1]) * fy; lat = (X - cam[0]) * fy - (Y - cam[1]) * fx
    return (d > (c[3] if len(c) > 3 else 10.0)) & (d < c[0]) & (np.abs(lat) < k * ((c[2] if len(c) > 2 else 0.28) * np.maximum(d, 0) + c[1]))
def hill_dress2(A, pr):
    """Abbey Craig, dressed for the distance: heather mounds in purple-brown and brown, bracken, gorse with yellow flowers, big grey crag blocks on the south-west face,
    pine clumps with red trunks. Placed from the analytic hill field so they sit on the mesh."""
    if not pr or pr.get('hill2') is False: return
    rs = np.random.RandomState(19); B = Batch(48); Bg = Batch(49); Br = Batch(50); Bt = Batch(54); v0, f0 = _ico(); n0 = 7000
    X = HILL_C[0] + rs.uniform(-125, 105, n0); Y = HILL_C[1] + rs.uniform(-100, 95, n0); hh, cm = hill_h(X, Y); sd = river_query(X, Y)[0]; e = 1.0
    sl = np.hypot((hill_h(X + e, Y)[0] - hill_h(X - e, Y)[0]) / (2 * e), (hill_h(X, Y + e)[0] - hill_h(X, Y - e)[0]) / (2 * e)); ok = (hh > 2.5) & (sd > 3)
    clear = pr.get('clear_hill'); ok &= ~in_corridor(pr, X, Y, 1.8)
    if pr.get('dress_min') and pr.get('cam'): ok &= np.hypot(X - pr['cam'][0], Y - pr['cam'][1]) > pr['dress_min']
    if clear: ok &= np.hypot(X - clear[0], Y - clear[1]) > clear[2]
    PAL = [hex_lin(h) for h in ('#7a4c42', '#845a44', '#6c4a3c', '#8a5446', '#6c4650', '#7a5a40')]; idx = np.nonzero(ok & (sl < 1.15))[0][:int(pr.get('heather_n', 650))]
    for i in idx:
        x, y = X[i], Y[i]; z = float(ground(x, y)); r = rs.uniform(0.5, 1.0); c = np.array(PAL[rs.randint(0, 6)]) / np.array(hex_lin('#7a4f72')) * (0.8 + 0.4 * rs.rand())
        V = v0 * np.array([r * 1.3, r * 1.1, r * 0.6]) + np.array([x, y, z + r * 0.2]); B.mesh('heather', V, f0, False, tint=tuple(c))
    idx = np.nonzero(ok & (sl < 1.0) & (hh < 40))[0][700:700 + int(pr.get('gorse_n', 150))]
    for i in idx:
        x, y = X[i], Y[i]; z = float(ground(x, y)); r = rs.uniform(0.8, 1.5)
        for k in range(2): ox, oy = rs.uniform(-0.6, 0.6, 2) * r; V = v0 * np.array([r * 0.8, r * 0.8, r * 0.65]) + np.array([x + ox, y + oy, z + r * 0.4]); Bg.mesh('gorse', V, f0, False, tint=(0.9 + 0.2 * rs.rand(),) * 3)
        for j in range(9): p = v0[rs.randint(0, len(v0))]; q = np.array([x, y, z + r * 0.4]) + p * np.array([r * 0.85, r * 0.85, r * 0.7]) * np.array([1, 1, 1 if p[2] > -0.2 else 0.2]); Bg.blob('gorse_fl', q, 0.22 * r, tint=(0.9 + 0.2 * rs.rand(),) * 3)
    # crag blocks: big grey boulders and stacked slabs on the crag face
    idx = np.nonzero((cm > 0.25) & (hh > 8) & (sd > 3) & ~in_corridor(pr, X, Y, 3.0))[0][:int(pr.get('crag_n', 110))]
    for i in idx:
        x, y = X[i], Y[i]; z = float(ground(x, y)); s_ = rs.uniform(2.2, 6.0)
        if clear is not None and math.hypot(x - clear[0], y - clear[1]) < clear[2]: continue
        boulder(Br, x, y, z - 0.2, s_, rs, 'rock' if rs.rand() < 0.7 else 'rock_warm')
        if rs.rand() < 0.5: boulder(Br, x + rs.uniform(-1, 1), y + rs.uniform(-1, 1), z + s_ * 0.45, s_ * 0.6, rs)
    # pine clumps
    idx = np.nonzero(ok & (sl < 0.7) & (hh > 14))[0][:int(pr.get('pine_n', 40))]
    for i in idx:
        x, y = X[i], Y[i]
        for k in range(rs.randint(1, 4)):
            xx = x + rs.uniform(-4, 4); yy = y + rs.uniform(-4, 4)
            if float(hill_h(np.array([xx]), np.array([yy]))[0][0]) > 4: pine(Bt, xx, yy, float(ground(xx, yy)), rs.uniform(7, 15), rs, lean=rs.uniform(0, 0.1))
    B.finalize('hill_heather', ink=False); Bg.finalize('hill_gorse', ink=False); Br.finalize('hill_crag', ink=False); Bt.finalize('hill_pines2', ink=False)
for _f in (build_castle, hill_dress, hill_dress2, far_dress, meadow_dress, build_bridge, build_camp): BUILDERS.append(_f)
BUILDERS.insert(0, lambda A, pr: None)
BUILDERS.append(veg_near)

# ================================================================ placeholders and crowds
def _disc(B, mat, cx, cz, rx, rz, yy, seg=20):
    a = np.linspace(0, 2 * math.pi, seg, endpoint=False); v = [(cx, yy, cz)] + [(cx + rx * math.cos(t), yy, cz + rz * math.sin(t)) for t in a]; B.mesh(mat, v, [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)], False)
def stage_placeholders(A, cam=None, marks=None, only=None):
    """flat stand-in cast cards: near-white head #fef7f6 with a plum ring on a flat coloured body, turned to the camera. marks: name -> (x, y, z, facing, type)."""
    cam = cam or bpy.context.scene.camera; cl = cam.location; out = {}
    for nm, (x, y, z, fz, who) in (marks or A['marks']).items():
        if only and nm not in only: continue
        key = who.split(':')[0]; H = HEIGHT.get(key, 1.7); hd = H * 0.3; hc = H - hd * 0.52; bw = H * 0.36; B = Batch(); col = who.split(':')[1] if ':' in who else key
        _disc(B, 'ph_ring', 0, hc, hd * 0.5 * 1.06, hd * 0.5 * 1.06, 0.0); _disc(B, 'ph_head', 0, hc, hd * 0.5, hd * 0.5, 0.003)
        B.mesh('ph_' + col, [(-bw / 2, 0.001, 0), (bw / 2, 0.001, 0), (bw * 0.36, 0.001, H - hd * 1.0), (-bw * 0.36, 0.001, H - hd * 1.0)], [(0, 1, 2, 3)], False)
        ob = B.finalize('ph_' + nm, loc=(x, y, z), ink=False, shadow=False)
        for o in ob: o.rotation_euler = (0, 0, math.atan2(-(cl.x - x), (cl.y - y)))
        out[nm] = ob
    return out
def head_report(A, cam=None, W=720, Hh=1280):
    cam = cam or bpy.context.scene.camera; res = {}
    for nm, (x, y, z, fz, who) in A['marks'].items():
        key = who.split(':')[0]; H = HEIGHT.get(key, 1.7); hd = H * 0.3; px, py, dz = project(cam, (x, y, z + H - hd * 0.52), W, Hh); res[nm] = dict(cx=round(px), cy=round(py), chin=round(py + hd * 0.5 * 782.2 / dz), dist=round(dz, 1))
    return res
def stage_crowd(items, cam=None, seg=10, shadow=True):
    """many small placeholder cards in one go. items: (x, y, z, kind, scale) with kind a ph_ colour key ('foot', 'foot_r', 'knight', 'scot', ...). One object per colour."""
    cam = cam or bpy.context.scene.camera; cl = cam.location; B = Batch(77)
    for (x, y, z, kind, sc) in items:
        H = HEIGHT.get(kind.split('_')[0], 1.7) * sc; hd = H * 0.3; hc = H - hd * 0.52; bw = H * 0.36; yaw = math.atan2(-(cl.x - x), (cl.y - y))
        with B.xf((x, y, z), (0, 0, math.degrees(yaw))):
            _disc(B, 'ph_ring', 0, hc, hd * 0.5 * 1.06, hd * 0.5 * 1.06, 0.0, seg); _disc(B, 'ph_head', 0, hc, hd * 0.5, hd * 0.5, 0.003, seg)
            B.mesh('ph_' + kind, [(-bw / 2, 0.001, 0), (bw / 2, 0.001, 0), (bw * 0.36, 0.001, H - hd * 1.0), (-bw * 0.36, 0.001, H - hd * 1.0)], [(0, 1, 2, 3)], False)
    return B.finalize('crowd', ink=False, shadow=shadow)

# ================================================================ PRESETS, hooks, CLI
def rel_xy(cam, look, dist, lat):
    """ground point `dist` m ahead of the camera along the view azimuth and `lat` m to the right of it."""
    az = math.atan2(look[1] - cam[1], look[0] - cam[0]); fx, fy = math.cos(az), math.sin(az); rx, ry = fy, -fx
    return cam[0] + fx * dist + rx * lat, cam[1] + fy * dist + ry * lat
def mark_at(cam, look, dist, lat, typ, dz=0.0):
    x, y = rel_xy(cam, look, dist, lat); return (x, y, float(ground(x, y)) + dz, 0.0, typ)
def bridge_pairs(y0=-28.0, y1=32.0, step=6.0): return [y0 + i * step for i in range(int((y1 - y0) / step) + 1)]
def fg_hill(A, pr):
    """foreground of hill_over: spear shafts, a gorse bush, heather and a boulder 1-2 m from the lens."""
    cam = np.array(pr['cam']); look = np.array(pr['look']); B = Batch(61); rs = np.random.RandomState(21)
    for (d, lat, lean) in pr['fg_spears']:
        x, y = rel_xy(cam, look, d, lat); z = float(ground(x, y)); spear(B, (x, y, z), tilt=(lean[0], lean[1]), h=3.4)
    for (d, lat, s) in pr['fg_gorse']: x, y = rel_xy(cam, look, d, lat); g = Batch(62); gorse(g, (x, y, float(ground(x, y))), s, rs); g.finalize('fg_gorse', ink=False)
    for (d, lat, s) in pr['fg_rocks']: x, y = rel_xy(cam, look, d, lat); boulder(B, x, y, float(ground(x, y)), s, rs)
    Bt = Batch(64)
    for (d, lat, h) in pr.get('dress_pines', []): x, y = rel_xy(cam, look, d, lat); pine(Bt, x, y, float(ground(x, y)), h, rs, lean=0.04)
    for (d, lat, n, sp, sz) in pr.get('dress_crags', []): x, y = rel_xy(cam, look, d, lat); crag_group(Bt, x, y, rs, n=n, spread=sp, s=sz)
    for (d, lat, s_) in pr.get('dress_gorse', []): x, y = rel_xy(cam, look, d, lat); gorse(Bt, (x, y, float(ground(x, y))), s_, rs)
    Bt.finalize('hill_dress', ink=False); B.finalize('fg_hill')
def fg_bank(A, pr):
    """foreground of camp_bank: a banner pole with a pennant, a tent rope and peg, a spear stand, barrels."""
    cam = np.array(pr['cam']); look = np.array(pr['look']); B = Batch(63); rs = np.random.RandomState(22)
    d, lat = pr['fg_banner']; x, y = rel_xy(cam, look, d, lat); banner(B, (x, y, float(ground(x, y))), 6.0, pr['fg_banner_yaw'], 't_red', 't_gold', 'chevron', rs, size=(2.2, 1.5))
    for (d, lat) in pr['fg_spears']: x, y = rel_xy(cam, look, d, lat); spear(B, (x, y, float(ground(x, y))), tilt=(0.05, 0.1), h=3.0)
    for (d, lat) in pr.get('fg_barrels', []): x, y = rel_xy(cam, look, d, lat); barrel(B, (x, y, float(ground(x, y))), rs=rs)
    B.finalize('fg_bank', shadow=False)
def scots_slope_line(n, ranks, scale, rs, spear_h=3.4, a0=188.0, a1=258.0, hh0=9.0):
    """the Scots' line on Abbey Craig's lower south-west slope: lit tan/ochre/moss tunics (scaled for the distance), dark caps, light-catching steel spear tips."""
    B = Batch(82); mats = ['thatch', 't_brown', 'hay', 't_green', 'cloth_red']; cnt = 0
    for rank in range(ranks):
        for k in range(n):
            a = math.radians(a0 + (a1 - a0) * k / max(n - 1, 1) + rs.uniform(-1.5, 1.5))
            for r_ in np.arange(30, 110, 1.0):
                x = HILL_C[0] + r_ * math.cos(a) * 1.05; y = HILL_C[1] + r_ * 0.9 * math.sin(a)
                if float(hill_h(np.array([x]), np.array([y]))[0][0]) < hh0 + 2.2 * rank: break
            z = float(ground(x, y)); m = mats[(k + rank) % 5]
            B.box(m, (x, y, z + 0.8 * scale), (0.75 * scale, 0.55 * scale, 1.5 * scale), tint=0.95 + 0.3 * rs.rand()); B.sphere('iron', (x, y, z + 1.68 * scale), 0.2 * scale, seg=6, rings=4)
            tl = (rs.uniform(-0.25, 0.25), rs.uniform(-0.25, 0.25)); spear(B, (x + 0.38 * scale, y, z), tilt=tl, h=spear_h * scale); cnt += 1
            if scale > 1.2: B.sphere('gold', (x + 0.38 * scale + tl[0], y + tl[1], z + spear_h * scale + 0.1), 0.32 * scale, seg=5, rings=3)
    B.finalize('scots_line', ink=False)
    Bp = Batch(86)
    for k in range(2, n, max(n // 4, 1)):                                                         # blue saltire banners on poles along the line
        a = math.radians(a0 + (a1 - a0) * k / max(n - 1, 1))
        for r_ in np.arange(30, 110, 1.0):
            x = HILL_C[0] + r_ * math.cos(a) * 1.05; y = HILL_C[1] + r_ * 0.9 * math.sin(a)
            if float(hill_h(np.array([x]), np.array([y]))[0][0]) < hh0 - 1.0: break
        banner(Bp, (x, y, float(ground(x, y))), 5.5 * scale, rs.uniform(150, 200), 't_saltire', 't_white', 'saltire', rs, size=(2.2 * scale, 1.5 * scale))
    Bp.finalize('scots_banners'); return cnt
def spear_wall(n, ranks, rs, y0=27.0, half=9.0):
    """the cork: a wall of Scots across the north end of the bridge (the neck), spears level."""
    B = Batch(83); cnt = 0
    for rank in range(ranks):
        for k in range(n):
            x = -half + 2 * half * k / max(n - 1, 1); y = y0 + 1.1 * rank; z = float(ground(x, y)); B.box('thatch' if k % 2 else 't_brown', (x, y, z + 0.85), (0.8, 0.6, 1.6)); B.sphere('iron', (x, y, z + 1.78), 0.21, seg=6, rings=4)
            spear(B, (x, y - 0.4, z), tilt=(0.0, -0.9), h=2.4); cnt += 1
    B.finalize('spear_wall', ink=False)
    Bp = Batch(87)
    for sx in (-half - 1.0, half + 1.0): banner(Bp, (sx, y0 - 0.5, float(ground(sx, y0))), 5.0, 190, 't_saltire', 't_white', 'saltire', rs, size=(2.2, 1.5))
    Bp.finalize('wall_banners'); return cnt
def crowd_loop(A, pr):
    """~120 tiny placeholder troops for valley_loop: English inside the loop meadow and the neck, a two-by-two column of mounted knights on the bridge, a queue and
    groups on the south bank; Scots along the hill's lower slope."""
    rs = np.random.RandomState(31); items = []; B = Batch(78)
    kinds = ['foot', 'foot_r', 'foot', 'knight_b', 'foot_r']
    # bridge column of horses
    knight_pair_column(B, bridge_pairs(-30, 33, 6.5), BRIDGE_X, rs, KNIGHT_MATS)
    # meadow: the army jammed in ranks at the neck (south half of the bulb), the rest thinner behind
    for r in range(8):
        for c in range(12):
            x = -18 + c * 3.3 + rs.uniform(-0.5, 0.5) + (1.6 if r % 2 else 0); y = 44 + r * 4.6 + rs.uniform(-0.5, 0.5)
            if math.hypot(x - LOOP_C[0], y - LOOP_C[1]) < LOOP_R - 20 and float(sd_at(x, y)) > 3: items.append((x, y, float(ground(x, y)), kinds[(r + c) % 5] if (r + c) % 7 else 'knight', 1.0))
    n = 0
    while n < 34:
        x = rs.uniform(-60, 60); y = rs.uniform(92, 160)
        if math.hypot(x - LOOP_C[0], y - LOOP_C[1]) > LOOP_R - 22 or float(sd_at(x, y)) < 3: continue
        items.append((x, y, float(ground(x, y)), kinds[rs.randint(0, 5)], 1.0)); n += 1
    for i in range(5):
        x = rs.uniform(-30, 30); y = rs.uniform(95, 140); horse(B, (x, y, float(ground(x, y))), rs.uniform(0, 360), coat='horse', trap=KNIGHT_MATS[i % 5][0], trim=KNIGHT_MATS[i % 5][1], rider=(KNIGHT_MATS[i % 5][0],), tint=0.9)
    # south bank queue along the road and groups by the table
    for i in range(24): y = -36 - i * 2.4; x = (-1.2 if i % 2 else 1.2) + rs.uniform(-0.3, 0.3); items.append((x, y, float(ground(x, y)), kinds[rs.randint(0, 5)], 1.0))
    for i in range(20):
        x = rs.uniform(-70, 70); y = float(bank_y(x)) - rs.uniform(4, 30)
        if abs(x) < 9: continue
        items.append((x, y, float(ground(x, y)), kinds[rs.randint(0, 5)], 1.0))
    # the Scots along the hill's lower slope, looking down
    for i in range(26):
        t = i / 25.0; a = math.radians(205 + 52 * t - 26); r = 66 + 5 * math.sin(i * 1.7); x = HILL_C[0] + r * 1.0 * math.cos(a) * 1.05; y = HILL_C[1] + r * 0.9 * math.sin(a)
        items.append((x, y, float(ground(x, y)), ['scot', 'scot_b', 'scot_o', 'scot_m'][i % 4], 1.0))
    A['scots_line'] = scots_slope_line(30, 3, 1.0, rs, spear_h=4.0) + spear_wall(14, 2, rs)
    Bb = Batch(80)
    for i, (x, y, f, c, sh) in enumerate([(-30, 66, 't_red', 't_gold', 'chevron'), (22, 72, 't_blue', 't_gold', 'bars'), (-8, 96, 't_cream', 't_red', 'cross'), (34, 104, 't_gold', 't_red', 'lion'), (-34, 112, 't_blue', 't_white', 'chevron'),
                                           (4, 126, 't_red', 't_cream', 'bars'), (-60, -52, 't_red', 't_gold', 'chevron'), (52, -48, 't_blue', 't_gold', 'bars'), (8, -80, 't_gold', 't_red', 'lion')]):
        banner(Bb, (x, y, float(ground(x, y))), 11.0, 20 + 25 * i % 70, f, c, sh, rs, size=(4.4, 3.0))
    for i, (a, f, c, sh) in enumerate([(220, 't_blue', 't_white', 'cross'), (242, 't_red', 't_gold', 'lion')]):
        x = HILL_C[0] + 66 * math.cos(math.radians(a)) * 1.05; y = HILL_C[1] + 66 * 0.9 * math.sin(math.radians(a)); banner(Bb, (x, y, float(ground(x, y))), 11.0, 30, f, c, sh, rs, size=(4.4, 3.0))
    Bb.finalize('crowd_banners', shadow=False); B.finalize('crowd_horses'); stage_crowd(items)
def px_lat(lens, d, x_px): return (x_px - 360.0) / (1280.0 * lens / 36.0) * d
def mark_px(cam, look, lens, d, x_px, typ, dz=0.0): return mark_at(cam, look, d, px_lat(lens, d, x_px), typ, dz)
def mk_hill_over(A):
    pr = PRESETS['hill_over']; cam, look, ln = pr['cam'], pr['look'], pr['lens']
    return {'s1': mark_px(cam, look, ln, 3.0, 70, 'scot:scot_b'), 's2': mark_px(cam, look, ln, 3.4, 610, 'wallace'), 's3': mark_px(cam, look, ln, 5.0, 650, 'scot:scot_o'),
            's4': mark_px(cam, look, ln, 5.6, 115, 'scot:scot_m'), 's5': mark_px(cam, look, ln, 7.0, 40, 'scot')}
def mk_camp_bank(A):
    pr = PRESETS['camp_bank']; cam, look, ln = pr['cam'], pr['look'], pr['lens']
    m = {'cress': mark_px(cam, look, ln, 3.6, 190, 'cressingham'), 'surrey': mark_px(cam, look, ln, 5.8, 640, 'surrey')}
    for i, (d, xp) in enumerate([(9.0, 55), (11.0, 335), (13.0, 440), (10.0, 540), (14.0, 610)]): m['e%d' % i] = mark_px(cam, look, ln, d, xp, ['foot', 'foot:foot_r', 'knight:knight_b'][i % 3])
    return m
def camp_fg(A, pr):
    """camp_bank foreground camp: pavilions with pennants on the right, bell/ridge tents, a cook fire, a cart, a weapon rack, a horse line, small pegs. Nothing on the water."""
    cam = np.array(pr['cam']); look = np.array(pr['look']); B = Batch(65); Bs = Batch(66); rs = np.random.RandomState(23); lens = pr['lens']
    def at(d, xp): return rel_xy(cam, look, d, px_lat(lens, d, xp))
    dry = lambda x, y, m=3.5: float(sd_at(x, y)) > m
    mats = (('t_red', 't_cream'), ('t_blue', 't_gold'), ('t_red', 't_cream'), ('t_blue', 't_gold'), ('t_red', 't_cream'), ('t_blue', 't_gold'))
    for i, (d, xp, r) in enumerate([(26.0, 770, 4.0), (40.0, 700, 3.6), (32.0, 715, 4.4), (46.0, 700, 4.0), (60.0, 705, 4.6), (78.0, 690, 4.2)]):
        x, y = at(d, xp)
        if not dry(x, y, 6): continue
        z0 = float(ground(x, y)); pavilion(B, (x, y, z0), r, mats[i], yaw=rs.uniform(0, 30), rs=rs, hw=1.9, hr=3.4)
        bx, by = x + r * 0.7, y + r * 0.3; banner(B, (bx, by, float(ground(bx, by))), 7.5, rs.uniform(-30, 40), *[('t_red', 't_gold', 'chevron'), ('t_blue', 't_gold', 'bars'), ('t_gold', 't_red', 'lion')][i % 3], rs)
        sacks(B, (x - r - 1.0, y - 1.5, z0), 3, rs); barrel(B, (x + r + 0.9, y - 2.0, z0), rs=rs)
    for i, (d, xp) in enumerate([(12, 760), (17, 40), (19, 20), (24, 700), (26, 60), (33, 120), (38, 540), (46, 90), (52, 735), (58, 20), (64, 640), (70, 520), (80, 430)]):
        x, y = at(d, xp)
        if not dry(x, y, 6): continue
        bell_tent(B, (x, y, float(ground(x, y))), 1.7 + 0.5 * rs.rand(), 2.7, ['t_cream', 't_gold', 't_cream', 't_brown'][i % 4], rs) if i % 3 else ridge_tent(B, (x, y, float(ground(x, y))), 3.6, 3.0, 2.0, ['t_cream', 't_white', 't_brown'][i % 3], yaw=rs.uniform(-30, 30))
    for (d, xp, fn) in [(9.5, 45, 'fire'), (17.0, 130, 'cart'), (11.0, 36, 'rack'), (10.5, 690, 'fire')]:
        x, y = at(d, xp)
        if not dry(x, y, 5): continue
        z = float(ground(x, y))
        if fn == 'fire': campfire(B, Bs, (x, y, z), rs, puffs=False)
        elif fn == 'cart': cart(B, (x, y, z), 35, rs, cover=True)
        else: weapon_rack(B, (x, y, z), 70, rs)
    for i in range(6):                                          # horse line
        x, y = at(19 + 2.0 * i, 720 + 6 * i)
        if not dry(x, y, 5): continue
        horse(B, (x, y, float(ground(x, y))), 95 + rs.uniform(-15, 15), coat=['horse', 'horse_dk', 'horse'][i % 3], trap=(None, 't_red', None, 't_blue', 't_cream', None)[i], trim='t_gold', tint=0.8 + 0.4 * rs.rand(), bob=rs.uniform(0, 0.25))
    B.finalize('camp_fg', shadow=False); Bs.finalize('camp_fg_smoke', ink=False)
def crowd_hill(A, pr):
    """hill_over: tiny English column on the bridge (knights two by two + a few foot), foot soldiers at the camp, the Scots line below the lens with spears."""
    rs = np.random.RandomState(32); B = Batch(79); items = []; Bsp = Batch(81)
    knight_pair_column(B, bridge_pairs(-26, 28, 5.0), BRIDGE_X, rs, KNIGHT_MATS)
    for i in range(18): x = rs.uniform(-34, 34); y = float(bank_y(x)) - rs.uniform(3, 28); items.append((x, y, float(ground(x, y)), ['foot', 'foot_r', 'knight_b'][i % 3], 1.0))
    for i in range(14): y = -38 - i * 2.8; items.append((1.0 if i % 2 else -1.0, y, float(ground(0.0, y)), 'foot_r' if i % 3 else 'foot', 1.0))
    cam, look = pr['cam'], pr['look']
    for i in range(22):                                          # Scots on the slope below and beside the lens
        d = rs.uniform(10, 30); xp = rs.choice([rs.uniform(-120, 230), rs.uniform(500, 850)]); x, y = rel_xy(cam, look, d, px_lat(pr['lens'], d, xp)); z = float(ground(x, y))
        items.append((x, y, z, ['scot', 'scot_b', 'scot_o', 'scot_m'][i % 4], 1.0)); spear(Bsp, (x + 0.35, y, z), tilt=(rs.uniform(-0.3, 0.3), rs.uniform(-0.3, 0.3)), h=3.0)
    B.finalize('crowd_horses'); Bsp.finalize('crowd_spears'); stage_crowd(items)
PRESETS['hill_over'] = dict(loc='hill', shafts='pines', corridor=(70.0, 0.6, 0.2, 7.0), dress_min=26.0, cam=(160.0, 150.0, 0.0), cam_dz=2.7, cam_ref=(160.0, 150.0), look=(0.0, 2.0, -20.0), sd=8.0, lens=32.0, marks=mk_hill_over, hill2=True,
    over=dict(glit_stretch=1.0, glit_s=1.0, foam_k=2.0, wake_k=2.0, sun_k=2.0),
    veg=dict(seed=5, half=24, no_chips=True, hill_grass=0.4, grass=[(2, 14, 1100, 0.1, 0.17), (14, 40, 1100, 0.2, 0.34)], flowers=300, sprig_to=60, heather=[(1.5, 8, 700, 0.09, 0.15), (8, 17, 1000, 0.12, 0.2), (17, 40, 1400, 0.18, 0.3), (40, 100, 1000, 0.5, 0.9)], gorse=[(3, 14, 8), (14, 40, 26)], reeds=None),
    fg_spears=[(1.8, -0.55, (0.08, 0.1)), (1.6, 0.5, (-0.1, 0.1))], fg_gorse=[(2.4, -0.9, 0.55), (2.2, 0.8, 0.5)], fg_rocks=[(2.0, 0.0, 0.7)],
    dress_pines=[(20.0, -5.4, 12.0)], dress_crags=[(6, 2.8, 4, 1.2, 0.7)],
    dress_gorse=[(7, -2, 0.7), (6, 2, 0.6), (10, 2.5, 0.8), (11, -3.5, 0.9), (12, 4, 0.9), (13, -2, 0.7), (9, 3.5, 0.7), (15, -4.5, 1.0), (14, 3.5, 0.8), (20, 5, 1.1)], clear_hill=(160.0, 150.0, 6.0))
PRESETS['camp_bank'] = dict(loc='camp', signs=['stirling'], shafts='smoke', cam=(-95.0, -15.0, 0.0), cam_dz=2.0, look=(-2.3, 22.5, -16.5), sd=6.0, lens=26.0, camp_banners=False, marks=mk_camp_bank, hill2=True, far_scots=True, bridge_pairs=(-26.0, 26.0, 6.0),
    over=dict(glit_stretch=1.0, glit_s=0.9, foam_k=2.0, wake_k=2.0, sun_k=2.1, reed_k=0.5),
    veg=dict(seed=6, half=20, tuft_k=1.3, tuft_gain=1.5, grass=[(1.5, 9, 420, 0.08, 0.13), (9, 40, 700, 0.12, 0.2)], flowers=700, reeds=[(6, 70, 500)]),
    fg_banner=(7.0, 2.3), clear=[(-95.0, -15.0, 9.0)], fg_banner_yaw=30, fg_spears=[], fg_barrels=[(3.0, 1.7)], fg_rope=True, camp_fg=camp_fg)
PRESETS['valley_loop'] = dict(loc='valley', cam=(-72.0, -133.0, 229.0), look=(12.0, 36.0, 0.0), sd=300.0, lens=21.0, marks=lambda A: {}, veg=None, farms=True, hill2=True, heather_n=900, gorse_n=200, crag_n=140, pine_n=60,
    over=dict(foam_k=3.0, glit_s=0.35, glit_t=0.12, glit_stretch=1.0, wake_k=4.0, haze_max=0.2, world=0.0, lift=(0.03, 0.028, 0.07), key=(2.05, 1.58, 0.84), shade=(0.12, 0.10, 0.30), tint=(0.065, 0.052, 0.15), sun_dir=(-0.68, 0.68, -0.28)))
for _n, _fn in (('hill_over', fg_hill), ('camp_bank', fg_bank)): PRESETS[_n]['fg'] = _fn
PRESETS['hill_over']['crowd'] = crowd_hill; PRESETS['valley_loop']['crowd'] = crowd_loop

# ================================================================ HOOKS (keyable per frame; every hook takes film seconds t or a plain value and only sets scene values)
def set_flutter(t, amp=1.0):
    """banner flutter: keys the Wave modifier phase (and the amplitude, amp 1 = normal) of every live banner (t in seconds)."""
    n = 0
    for (obn, mdn, ph, h0) in STATE['anim'].get('flags', []):
        ob = bpy.data.objects.get(obn)
        if ob: md = ob.modifiers[mdn]; md.time_offset = -(t * 30.0 + ph * 4.0); md.height = h0 * amp; n += 1
    return n
def set_smoke(t, speed=0.12):
    """smoke columns: puffs rise, grow and fade in a loop (one cycle = 1/speed seconds)."""
    for c in STATE['anim'].get('smoke', []): _smoke_pose(c, t, speed)
    return len(STATE['anim'].get('smoke', []))
def set_flow(t, speed=1.0):
    """water: shifts the current streaks, foam streaks and the sun glitter (glitter cells twinkle through the 4th noise dimension)."""
    nt = get_mat('water').node_tree; nt.nodes['flow_off'].inputs['Location'].default_value = (-t * 0.9 * speed, 0, 0); nt.nodes['flow_off2'].inputs['Location'].default_value = (-t * 2.2 * speed, 0, 0)
    nt.nodes['glit_vor'].inputs['W'].default_value = t * 1.7; nt.nodes['glit_noise'].inputs['W'].default_value = t * 0.9
def set_scale_tip(A, deg):
    """Cressingham's coin scale: tips the balance beam about its pivot (deg, + = right pan down). Needs a build that has the camp (every preset has)."""
    ob = bpy.data.objects[A['scale_beam']]; e = ob.rotation_euler; ob.rotation_euler = (e[0], math.radians(deg), e[2])
def set_chest_lid(A, deg_open):
    """coin chest lid: 72 = open, 0 = shut (hinge at the back edge)."""
    ob = bpy.data.objects[A['chest_lid']]; e = ob.rotation_euler; ob.rotation_euler = (math.radians(-deg_open), e[1], e[2])
def _del_prefix(pfx):
    for ob in [o for o in bpy.data.objects if o.name.startswith(pfx)]: bpy.data.objects.remove(ob, do_unlink=True)
def splash(x, y, age, size=1.0, z=0.0, name='a', seed=0):
    """a spray crown at (x, y) on the water, `age` seconds after impact (age < 0 or > 1.6 = nothing). White emission-lit foam (no shading, never lilac): 15 separate tapered
    spikes that flare outward 30-45 deg and each end in a bead, 8 shorter inner spikes, a thick central column (0.2 m, up to 3 m tall) with a bead cap, a low ring of mist
    discs and a thin expanding foam ring on the water, and 80 ballistic droplets (r 0.06-0.14 m). size 1 = a man jumping: crown 1.5 m tall at age 0.3. Re-calling with the same
    name replaces it (never stacks). Returns the number of objects made."""
    _del_prefix('splash_' + name + '_')
    if age < 0 or age > 1.6: return 0
    rs = np.random.RandomState(seed); B = Batch(91); k = size; M = 'glow_spray'; M2 = 'glow_spray2'; tau = min(age / 0.85, 1.0)
    R0 = k * (0.22 + 0.45 * tau); Hc = k * 1.6 * math.sin(math.pi * min(tau, 1.0)) ** 0.75 * (1 - 0.25 * tau) if age < 0.9 else 0.0
    if Hc > 0.05:
        for ring, (n, hs, rr) in enumerate(((15, 1.0, 1.0), (8, 0.55, 0.55))):
            for i in range(n):
                a = 2 * math.pi * (i + 0.5 * ring + rs.uniform(-0.15, 0.15)) / n; hh = Hc * hs * rs.uniform(0.75, 1.15); fl = math.radians(rs.uniform(30, 45)); r_b = R0 * rr
                p0 = (x + r_b * math.cos(a), y + r_b * math.sin(a), z); pm = (x + (r_b + 0.25 * hh * math.tan(fl)) * math.cos(a), y + (r_b + 0.25 * hh * math.tan(fl)) * math.sin(a), z + 0.6 * hh)
                p1 = (x + (r_b + hh * math.tan(fl)) * math.cos(a), y + (r_b + hh * math.tan(fl)) * math.sin(a), z + hh)
                B.rod(M, p0, pm, 0.065 * k, seg=5, r2=0.05 * k); B.rod(M, pm, p1, 0.05 * k, seg=5, r2=0.015 * k); B.sphere(M, p1, 0.1 * k * rs.uniform(0.8, 1.2), seg=6, rings=4)
    if age < 0.85 and Hc > 0.05:                                              # a tapered column no taller than 1.2x the crown, with 3-5 droplets breaking off its tip
        hs = 1.2 * Hc; B.rod(M, (x, y, z), (x, y, z + hs), 0.09 * k, seg=8, r2=0.012 * k)
        for j in range(rs.randint(3, 6)): B.sphere(M, (x + rs.uniform(-0.15, 0.15) * k, y + rs.uniform(-0.15, 0.15) * k, z + hs + (0.12 + 0.16 * j) * k), rs.uniform(0.05, 0.09) * k, seg=5, rings=3)
    ro = R0 * 1.5 + k * 0.6 * tau; wd = max(0.03, 0.25 * k * (1 - age / 1.6)); n = 24; th = [2 * math.pi * i / n for i in range(n)]
    B.mesh(M2, [(x + (ro - wd) * math.cos(t_), y + (ro - wd) * math.sin(t_), z + 0.05) for t_ in th] + [(x + ro * math.cos(t_), y + ro * math.sin(t_), z + 0.05) for t_ in th], [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)], False)
    for i in range(8):                                                       # low mist: flat white discs round the base
        a = rs.uniform(0, 6.28); rr = R0 * rs.uniform(0.6, 1.3); _disc(B, M2, 0, 0, 0.0, 0.0, 0.0) if False else B.cyl(M2, (x + rr * math.cos(a), y + rr * math.sin(a), z + 0.1 + 0.1 * rs.rand()), 0.28 * k * (1 - 0.4 * tau), 0.04, seg=8)
    for i in range(80):
        a = rs.uniform(0, 2 * math.pi); vh = rs.uniform(1.0, 3.6) * math.sqrt(k); vz = rs.uniform(2.6, 6.0) * math.sqrt(k); px = x + vh * math.cos(a) * age; py = y + vh * math.sin(a) * age; pz = z + 0.15 + vz * age - 4.9 * age * age
        if pz > z + 0.03 and age > 0.02: B.sphere(M, (px, py, pz), rs.uniform(0.06, 0.14) * k ** 0.9, seg=5, rings=3)
    return len(B.finalize('splash_' + name + '_', ink=False, shadow=False))

def place_troops(A, where, n, kind=None, seed=0, cb=None, horses=True):
    """English troops by COUNT. where = 'bridge' (n mounted knights, two by two along the deck, 3D horses unless horses=False), 'causeway' (n foot soldiers, 3 abreast on the
    north causeway y 40..90), 'meadow' (n foot soldiers in ranks in the loop meadow), 'south' (n foot soldiers queued on the south road).
    Returns the list of (x, y, z, kind, scale) stand points. With cb the list is handed to cb(items) so a team can place real cast sprites; without cb the default
    placeholder cards are staged (on the bridge the 3D riders are the default). Calling again with the same `where` replaces the previous set."""
    _del_prefix('troops_' + where); rs = np.random.RandomState(seed); items = []
    if where == 'bridge':
        ys = [-30.0 + 5.4 * i for i in range(12)]
        for i in range(n): pair = i // 2; yy = ys[min(pair, len(ys) - 1)]; sx = -0.62 if i % 2 == 0 else 0.62; items.append((BRIDGE_X + sx, yy, DECK_Z, kind or 'knight', 1.0))
        if horses and n:
            B = Batch(85)
            for (x, y, z, k_, s_) in items: m = KNIGHT_MATS[int(abs(y * 7 + x * 3)) % 5]; horse(B, (x, y, z), 90.0, coat=['horse', 'horse_dk', 'horse'][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.85 + 0.3 * rs.rand(), rider=(m[0],))
            B.finalize('troops_bridge')
    elif where == 'causeway':
        for i in range(n): x = (-1.8, 0.0, 1.8)[i % 3] + rs.uniform(-0.25, 0.25); y = 40.0 + 1.5 * (i // 3) + rs.uniform(-0.2, 0.2); items.append((x, y, float(ground(x, y)), kind or ['foot', 'foot_r'][i % 2], 1.0))
    elif where == 'meadow':
        for i in range(n):
            r_, c_ = divmod(i, 14); x = -22.0 + c_ * 3.2 + (1.6 if r_ % 2 else 0) + rs.uniform(-0.4, 0.4); y = 46.0 + r_ * 3.6 + rs.uniform(-0.4, 0.4); items.append((x, y, float(ground(x, y)), kind or ['foot', 'foot_r', 'foot', 'knight_b'][(r_ + c_) % 4], 1.0))
    elif where == 'south':
        for i in range(n): x = (-1.0 if i % 2 else 1.0) + rs.uniform(-0.3, 0.3); y = -38.0 - 1.2 * i; items.append((x, y, float(ground(x, y)), kind or 'foot', 1.0))
    if items and cb: cb(items)
    elif items and not (where == 'bridge' and horses):
        for o in stage_crowd(items, cam=bpy.context.scene.camera): o.name = 'troops_%s_%s' % (where, o.name)
    A.setdefault('troops', {})[where] = items; return items

# ================================================================ the other presets (generic spec -> cam, marks, foreground props)
def at_px(pr, d, xp):
    return rel_xy(np.array(pr['cam'], float), np.array(pr['look'], float), d, px_lat(pr['lens'], d, xp))
def marks_from_spec(pr):
    def f(A):
        out = {}
        for sp in pr['marks_spec']:
            nm, who, d, xp = sp[:4]; dz = sp[4] if len(sp) > 4 else 0.0; x, y = at_px(pr, d, xp); z = pr.get('stand_z')
            out[nm] = (x, y, (float(ground(x, y)) if z is None else z) + dz, 0.0, who)
        return out
    return f
def fg_generic(A, pr):
    """foreground props 1-2 m from the lens, from pr['fg_list']: ('spear', d, xp, lean) | ('gorse', d, xp, s) | ('rock', d, xp, s) | ('reeds', d, xp) | ('heather', d, xp, s) |
    ('post', d, xp) rail post | ('pole', d, xp) banner pole | ('rope', d, xp) tent rope + peg | ('chest', d, xp) coin chest | ('barrel', d, xp) | ('bollard', d, xp)."""
    rs = np.random.RandomState(pr.get('fg_seed', 41)); B = Batch(92); Bg = Batch(93); Br = Batch(94)
    for sp in pr.get('fg_list', []):
        k, d, xp = sp[:3]; x, y = at_px(pr, d, xp); z = float(ground(x, y)); zz = pr.get('fg_z'); z = z if zz is None else zz
        if k == 'spear': spear(B, (x, y, z), tilt=sp[3] if len(sp) > 3 else (0.08, 0.1), h=3.4)
        elif k == 'gorse': gorse(Bg, (x, y, z), sp[3] if len(sp) > 3 else 0.6, rs)
        elif k == 'rock': boulder(Br, x, y, z, sp[3] if len(sp) > 3 else 0.7, rs)
        elif k == 'reeds':
            for j in range(4): reed_cluster(Bg, (x + rs.uniform(-0.5, 0.5), y + rs.uniform(-0.5, 0.5), z), rs)
        elif k == 'heather': v0, f0 = _ico(); r_ = sp[3] if len(sp) > 3 else 0.6; Br.mesh('heather', v0 * np.array([r_ * 1.3, r_, r_ * 0.6]) + np.array([x, y, z + r_ * 0.2]), f0, False, tint=(1.0, 0.75, 0.7))
        elif k == 'post': B.box('wood', (x, y, z + 0.58), (0.17, 0.17, 1.12)); B.box('wood_dk', (x, y, z + 1.18), (0.22, 0.22, 0.1))
        elif k == 'pole': banner(B, (x, y, z), 6.0, rs.uniform(-20, 40), 't_red', 't_gold', 'chevron', rs, size=(2.2, 1.5))
        elif k == 'rope': B.rod('wood', (x, y, z - 0.05), (x + 0.05, y, z + 0.3), 0.04, seg=4); B.rod('rope', (x, y, z + 0.25), (x + 1.6, y + 0.5, z + 1.7), 0.025, seg=3)
        elif k == 'chest': B.box('wood_dk', (x, y, z + 0.35), (1.0, 0.6, 0.7)); B.box('iron', (x, y, z + 0.36), (1.02, 0.08, 0.72)); B.box('gold', (x, y, z + 0.72), (0.86, 0.46, 0.04))
        elif k == 'barrel': barrel(B, (x, y, z), rs=rs)
        elif k == 'bollard': B.cyl('wood_dk', (x, y, z + 0.5), 0.16, 1.0, seg=8)
    B.finalize('fg_generic'); Bg.finalize('fg_generic_g', ink=False); Br.finalize('fg_generic_r', ink=False)
def horses_parade(A, pr):
    """camp_wide: caparisoned knights on horses walking past the tents (3D riders), positions pr['parade'] = [(d, px)]."""
    B = Batch(95); rs = np.random.RandomState(12)
    for i, (d, xp) in enumerate(pr['parade']):
        x, y = at_px(pr, d, xp); m = KNIGHT_MATS[i % 5]; horse(B, (x, y, float(ground(x, y))), pr.get('parade_yaw', 0.0) + rs.uniform(-8, 8), coat=['horse', 'horse_dk', 'horse'][i % 3], trap=m[0], trim=m[1], tint=0.9, rider=(m[0],))
    B.finalize('parade')
def _mk(name, **kw):
    pr = dict(loc=kw.pop('loc'), sd=kw.pop('sd', 8.0), lens=kw.pop('lens', 22.0), veg=kw.pop('veg', None), hill2=kw.pop('hill2', True)); pr.update(kw)
    pr['marks'] = marks_from_spec(pr) if 'marks_spec' in pr else (lambda A: {})
    if 'fg_list' in pr: pr['fg'] = fg_generic
    if 'parade' in pr: pr['camp_fg'] = horses_parade
    PRESETS[name] = pr; return pr
_VEG = dict(seed=7, half=26, tuft_k=1.3, tuft_gain=1.5, grass=[(1.5, 9, 450, 0.08, 0.13), (9, 40, 800, 0.12, 0.2)], flowers=500)
_OVR = dict(glit_stretch=1.0, glit_s=0.9, foam_k=2.0, wake_k=2.0, sun_k=1.6)
_HV = dict(seed=5, half=30, no_chips=True, hill_grass=0.5, grass=[(2, 14, 900, 0.1, 0.17), (14, 40, 900, 0.2, 0.34)], flowers=200, sprig_to=40, heather=[(1.5, 8, 500, 0.09, 0.14), (8, 20, 700, 0.12, 0.2), (20, 60, 900, 0.2, 0.4)], gorse=[(3, 14, 6), (14, 40, 14)])
_VOVR = dict(foam_k=3.0, glit_s=0.35, glit_t=0.12, glit_stretch=1.0, wake_k=4.0, haze_max=0.2, world=0.0, lift=(0.03, 0.028, 0.07), key=(2.05, 1.58, 0.84), shade=(0.12, 0.10, 0.30), tint=(0.065, 0.052, 0.15), sun_dir=(-0.68, 0.68, -0.28))
# hill_eye / hill_low: on the Scots' shelf (x 131, y 131, 15 m up), looking up the slope at the line
_mk('hill_eye', loc='hill', shafts='pines', cam=(128.0, 128.0, 0.0), cam_dz=1.75, cam_ref=(128.0, 128.0), look=(144.0, 144.0, 20.5), lens=22.0, sd=9.0, over=dict(_OVR),
    marks_spec=[('s1', 'scot:scot_b', 5.2, 150), ('s2', 'scot:scot_o', 6.0, 265), ('w', 'wallace', 5.6, 370), ('s3', 'scot:scot_m', 6.4, 500), ('s4', 'scot', 5.4, 590)],
    veg=dict(_HV), fg_list=[('spear', 2.6, 690, (-0.7, 0.2)), ('gorse', 2.4, 640, 0.55)], dress_min=6.0, drift='slide 40 px/s; snap push x1.4 on s2')
_mk('hill_low', loc='hill', shafts='pines', cam=(118.0, 112.0, 0.0), cam_dz=1.4, cam_ref=(118.0, 112.0), look=(140.0, 134.0, 19.0), lens=22.0, sd=9.0, over=dict(_OVR),
    marks_spec=[('s1', 'scot:scot_b', 7.0, 90), ('s2', 'scot', 8.5, 230), ('horn', 'scot:scot_o', 7.5, 390), ('w', 'wallace', 9.5, 530), ('s3', 'scot:scot_m', 9.0, 640)],
    veg=dict(_HV), fg_list=[('gorse', 1.6, 80, 0.6), ('gorse', 1.9, 620, 0.6), ('rock', 2.2, 360, 0.6), ('spear', 1.8, 30, (0.7, 0.1))], dress_min=6.0, drift='pull-out 7 %/s, tilted up 14 deg')
# the bridge presets (cam z is absolute: the deck is DECK_Z = 1.75)
_mk('bridge_deck', loc='bridge', cam=(-2.7, -2.4, 3.0), look=(0.6, 1.6, 2.9), lens=22.0, sd=4.0, over=dict(_OVR), stand_z=DECK_Z, hill2=False,
    marks_spec=[('k1', 'knight', 3.2, 190), ('k2', 'knight:knight_b', 3.6, 520)], fg_list=[('post', 1.1, 20)], fg_z=DECK_Z, drift='push 8 %/s')
_mk('bridge_high', loc='bridge', signs=['stirling'], cam=(-5.0, -62.0, 24.0), look=(0.0, 6.0, 1.0), lens=22.0, sd=40.0, over=dict(_OVR, wake_k=3.0), hill2=False, marks_spec=[], troops=dict(bridge=16),
    fg_list=[], fg_z=22.0, drift='push along the bridge 8 %/s; snap pull-out x0.7')
_mk('bridge_end_south', loc='bridge', signs=['stirling'], cam=(-2.0, -37.5, 2.6), look=(0.0, -31.0, 2.6), lens=22.0, sd=6.0, over=dict(_OVR), stand_z=DECK_Z, hill2=False, clear=[(0.0, -44.0, 14.0)],
    marks_spec=[('k1', 'knight', 5.0, 215), ('k2', 'knight:knight_b', 5.6, 505)], fg_list=[('spear', 2.4, 40, (0.7, 0.0))], drift='snap push x1.4 (16 f)')
_mk('bridge_end_north', loc='bridge', cam=(-2.0, 50.0, 4.6), look=(0.0, 22.0, 1.8), lens=22.0, sd=14.0, over=dict(_OVR), hill2=False,
    marks_spec=[('e1', 'foot', 7.0, 170), ('e2', 'foot:foot_r', 9.0, 420), ('e3', 'foot', 8.0, 600), ('e4', 'foot:foot_r', 11.0, 300)], troops=dict(bridge=10, causeway=12),
    fg_list=[('gorse', 2.0, 650, 0.5), ('reeds', 2.0, 60)], veg=dict(_VEG, reeds=[(6, 40, 160)]), drift='push 8 %/s')
# valley
_mk('valley_wide', loc='valley', cam=(445.0, 244.0, 361.0), look=(64.0, 44.0, 0.0), lens=22.0, sd=300.0, farms=True, over=dict(_VOVR), marks_spec=[], troops=dict(bridge=14, meadow=60, causeway=10),
    heather_n=900, gorse_n=200, crag_n=140, pine_n=60, scots_line=True, drift='crane down + push 6 %/s')
_mk('valley_river', loc='valley', cam=(38.0, -24.0, 0.0), cam_dz=2.1, look=(105.0, 28.0, 4.0), lens=22.0, sd=12.0, over=dict(_OVR, reed_k=0.6), farms=True, scots_line=True,
    marks_spec=[('e1', 'foot', 22.0, 130), ('e2', 'foot:foot_r', 10.0, 600)], fg_list=[('reeds', 2.2, 90), ('reeds', 2.0, 640), ('rock', 2.4, 400, 0.5)], veg=dict(_VEG, half=30, reeds=[(4, 70, 700)]), drift='push 7 %/s + slide')
# camp
_mk('camp_wide', loc='camp', signs=['english'], shafts='smoke', cam=(-78.0, -96.0, 13.0), look=(12.0, -52.0, 2.0), lens=22.0, sd=40.0, over=dict(_OVR), parade=[(12, 110), (17, 330), (22, 520), (30, 640)], parade_yaw=35.0,
    marks_spec=[('k1', 'knight', 46.0, 200), ('k2', 'knight:knight_b', 52.0, 520)], fg_list=[('rope', 1.8, 60), ('pole', 2.2, 650)], drift='slide 50 px/s + push')
def table_extras(A, pr):
    """camp_table: Cressingham's stool with his cloak over its back (stays when he is not staged: the empty ending table) and a worn rug in front of the table."""
    tx, ty, tz = A['camp']['table']; B = Batch(97); rs = np.random.RandomState(2)
    sx, sy = tx + 0.15, ty + 0.95
    B.box('wood', (sx, sy, tz + 0.46), (0.5, 0.42, 0.06))
    for ox in (-0.2, 0.2):
        for oy in (-0.17, 0.17): B.rod('wood', (sx + ox, sy + oy, tz), (sx + ox * 0.9, sy + oy * 0.9, tz + 0.46), 0.03, seg=5)
    B.box('wood', (sx, sy + 0.2, tz + 0.78), (0.5, 0.05, 0.6)); B.box('cloth_red', (sx, sy + 0.25, tz + 0.72), (0.58, 0.07, 0.8)); B.box('gold', (sx, sy + 0.285, tz + 1.1), (0.4, 0.02, 0.05))
    B.box('cloth_red', (tx, ty - 1.15, tz + 0.015), (3.4, 1.2, 0.03)); B.box('gold', (tx, ty - 0.57, tz + 0.03), (3.4, 0.06, 0.01)); B.box('gold', (tx, ty - 1.73, tz + 0.03), (3.4, 0.06, 0.01))
    for sgn in (-1, 1): B.box('gold', (tx + sgn * 1.7, ty - 1.15, tz + 0.03), (0.07, 1.2, 0.01))
    for i in range(6): B.box('t_gold', (tx - 1.3 + 0.52 * i, ty - 1.15, tz + 0.032), (0.2, 0.9, 0.005))
    B.finalize('table_extras')
_mk('camp_table', loc='camp', signs=['treasury'], lantern=True, shafts='smoke', cam=(-13.0, -30.0, 0.0), cam_dz=1.3, look=(-13.0, -26.5, 1.70), lens=22.0, sd=5.0, over=dict(_OVR), camp_fg=table_extras, samples=40,
    marks_spec=[('cress', 'cressingham', 4.0, 365)], fg_list=[('barrel', 2.4, 820)], veg=dict(_VEG, half=22), drift='push 8 %/s; hooks: set_scale_tip(A, deg), set_chest_lid(A, deg)')
_mk('riverbank', loc='riverbank', cam=(-27.0, 54.0, 0.0), cam_dz=1.8, look=(-28.0, 22.0, -3.5), lens=22.0, sd=10.0, over=dict(_OVR, reed_k=0.6, foam_k=0.5),
    marks_spec=[('e1', 'foot', 4.5, 80), ('e2', 'foot:foot_r', 6.0, 215), ('e3', 'foot', 8.5, 130), ('e4', 'knight:knight_b', 11.0, 45)], fg_list=[('reeds', 1.7, 30), ('gorse', 2.2, 380, 0.4)],
    veg=dict(_VEG, half=30, reeds=[(2, 40, 90)]), drift='slide 40 px/s + push; the channel is on the right: splash() points in PRESETS["riverbank"]["splashes"]')
PRESETS['riverbank']['splashes'] = [at_px(PRESETS['riverbank'], d, xp) + (0.0,) for d, xp in ((9.0, 520), (11.0, 640), (13.0, 380))]
PRESETS['riverbank']['splash_size'] = 1.5; PRESETS['riverbank']['splash_ages'] = [0.2, 0.35, 0.5]
_mk('river_low', loc='riverbank', cam=(-26.0, 46.0, 0.0), cam_dz=0.9, look=(-44.0, 44.0, 0.9), lens=22.0, sd=10.0, over=dict(_OVR, reed_k=0.4, foam_k=0.6, sun_k=0.75, shallow='#2a8c86', sheen_k=0.25),
    marks_spec=[], fg_list=[('reeds', 1.4, 60), ('reeds', 1.6, 670), ('rock', 1.8, 380, 0.3)], veg=dict(_VEG, half=34, reeds=[(2, 40, 160)]), splash_size=1.8, splash_ages=[0.15, 0.3, 0.45], drift='quick push; splash() crowns at pr["splashes"]')
PRESETS['river_low']['splashes'] = [at_px(PRESETS['river_low'], d, xp) + (0.0,) for d, xp in ((9.0, 150), (10.5, 380), (9.5, 610))]

# ================================================================ SIGNS, LIGHT SHAFTS, LANTERN (client rule 2026-11-20: in-world signs; motivated light)
def _img_mat(key, path, afl=0.55):
    """lit material with an image on UV (the sign boards): the same Diffuse + ambient emission model, art = the image."""
    if key in _MATS: return _MATS[key]
    m = bpy.data.materials.new(key); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new; out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); uv = N('ShaderNodeUVMap')
    it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(path, check_existing=True); it.interpolation = 'Cubic'; it.extension = 'EXTEND'; L(uv.outputs['UV'], it.inputs['Vector'])
    sh = _lit_core(nt, it.outputs['Color'], dict(mix=0.8, sm=(0.85, 0.95, 1.15), afl=afl), geo); L(sh, out.inputs['Surface']); _MATS[key] = m; return m
def _quad_obj(name, corners, mat, uvs=((0, 0), (1, 0), (1, 1), (0, 1)), shadow=False):
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(c) for c in corners], [], [(0, 1, 2, 3)]); me.update(); uvl = me.uv_layers.new(name='UVMap')
    for li, loop in enumerate(me.polygons[0].loop_indices): uvl.data[loop].uv = uvs[li]
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.data.materials.append(mat); ob.visible_shadow = shadow; return ob
def face_yaw(frm, to):
    """yaw (deg) that turns a sign's front (local -y) toward the point `to`, for a sign standing at `frm`."""
    th = math.atan2(to[1] - frm[1], to[0] - frm[0]); return math.degrees(th) + 90.0
def make_sign(name, center, yaw, w, h, lines, posts=0.0, slab=True):
    """a painted sign board at `center` (board centre), turned by yaw (front = local -y). posts > 0: two posts from the ground to the board's top. Returns the textured quad."""
    path = TX.sign(name, lines, int(w * 360), int(h * 360)); B = Batch(98); cx, cy, cz = center
    with B.xf(center, (0, 0, yaw)):
        if slab: B.box('wood_dk', (0, 0.02, 0), (w + 0.16, 0.12, h + 0.16))
        if posts > 0:
            for sx in (-w / 2 + 0.25, w / 2 - 0.25): B.box('wood', (sx, 0.05, (float(ground(cx, cy)) + cz + h / 2) / 2 - cz), (0.2, 0.2, cz + h / 2 - float(ground(cx, cy))))
        T4 = B.stack[-1].copy()
    B.finalize('sign_frame_' + name)
    ca, sa = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    def wp(x, y, z): return (cx + x * ca - y * sa, cy + x * sa + y * ca, cz + z)
    q = [wp(-w / 2, -0.075, -h / 2), wp(w / 2, -0.075, -h / 2), wp(w / 2, -0.075, h / 2), wp(-w / 2, -0.075, h / 2)]
    ob = _quad_obj('sign_' + name, q, _img_mat('sign:' + name, path)); return ob
def signs_build(A, pr):
    """pr['signs'] = subset of ('stirling', 'treasury', 'english'). The only text in the set."""
    sg = pr.get('signs') or []
    if 'stirling' in sg:        # a gantry over the south end of the bridge, facing the camp
        sx_, sy_ = -2.15, -27.5; make_sign('stirling2', (sx_, sy_, float(ground(sx_, sy_)) + 3.4), face_yaw((sx_, sy_), (-2.5, -45.0)), 1.9, 1.15, ['STIRLING', 'BRIDGE'], posts=1.0)
    if 'treasury' in sg and A.get('camp', {}).get('table'):      # painted on the front of Cressingham's coin chest
        tx, ty, tz = A['camp']['table']; make_sign('treasury', (tx - 0.92, ty - 0.05 - 0.322, tz + 1.2), 0.0, 0.8, 0.34, ["KING'S", 'TREASURY'], slab=False)
    if 'english' in sg:         # the camp entrance board by the road
        cam = pr.get('cam') or (-78.0, -96.0, 13.0); x, y = (pr['sign_at'] if pr.get('sign_at') else (-56.0, -84.0)); z0 = float(ground(x, y))
        make_sign('english', (x, y, z0 + 4.6), face_yaw((x, y), cam), 5.8, 2.3, ['ENGLISH', 'CAMP'], posts=1.0)
def _shaft_mat():
    if 'shaft' in _MATS: return _MATS['shaft']
    m = bpy.data.materials.new('shaft'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new; out = N('ShaderNodeOutputMaterial'); uv = N('ShaderNodeUVMap'); sp = N('ShaderNodeSeparateXYZ'); L(uv.outputs['UV'], sp.inputs[0])
    mu = N('ShaderNodeMath'); mu.operation = 'MULTIPLY'; mu.inputs[1].default_value = math.pi; L(sp.outputs['X'], mu.inputs[0]); sn = N('ShaderNodeMath'); sn.operation = 'SINE'; L(mu.outputs[0], sn.inputs[0])
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 2.0; L(sn.outputs[0], pw.inputs[0])                      # soft across the width
    fv = N('ShaderNodeMath'); fv.operation = 'SUBTRACT'; fv.inputs[0].default_value = 1.0; L(sp.outputs['Y'], fv.inputs[1]); pv = N('ShaderNodeMath'); pv.operation = 'POWER'; pv.inputs[1].default_value = 0.9; L(fv.outputs[0], pv.inputs[0])   # fades to the ground
    tp = N('ShaderNodeMath'); tp.operation = 'MULTIPLY'; tp.inputs[1].default_value = 3.0; L(sp.outputs['Y'], tp.inputs[0]); tq = N('ShaderNodeMath'); tq.operation = 'SMOOTH_MIN'; tq.inputs[1].default_value = 1.0; tq.inputs[2].default_value = 0.0; L(tp.outputs[0], tq.inputs[0])
    nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 6.0; nz.inputs['Detail'].default_value = 0.0; L(uv.outputs['UV'], nz.inputs['Vector']); nm = N('ShaderNodeMath'); nm.operation = 'MULTIPLY_ADD'; nm.inputs[1].default_value = 0.8; nm.inputs[2].default_value = 0.45; L(nz.outputs['Fac'], nm.inputs[0])
    a1 = N('ShaderNodeMath'); a1.operation = 'MULTIPLY'; L(pw.outputs[0], a1.inputs[0]); L(pv.outputs[0], a1.inputs[1]); a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; L(a1.outputs[0], a2.inputs[0]); L(nm.outputs[0], a2.inputs[1])
    a3 = N('ShaderNodeMath'); a3.operation = 'MULTIPLY'; a3.inputs[1].default_value = STATE['P'].get('shaft_k', 0.6); L(a2.outputs[0], a3.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*hex_lin('#ffe0a0'), 1); em.inputs['Strength'].default_value = 1.7; tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(a3.outputs[0], mx.inputs['Fac']); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    _MATS['shaft'] = m; return m
def add_shaft(top, ground_pt, width=4.0):
    """a soft god-ray: two crossed emission strips (additive look, transparent mix, no volume) from `top` down to `ground_pt`; cast no shadow."""
    t = np.array(top, float); g = np.array(ground_pt, float); d = g - t; d /= np.linalg.norm(d); up = np.array([0, 0, 1.0]); p1 = np.cross(d, up); p1 /= (np.linalg.norm(p1) + 1e-9); p2 = np.cross(d, p1); p2 /= (np.linalg.norm(p2) + 1e-9); mat = _shaft_mat(); obs = []
    for k, p in enumerate((p1, p2)):
        w = width * (0.5 if k else 0.5)
        obs.append(_quad_obj('shaft_%d' % k, [t - p * w * 0.5, t + p * w * 0.5, g + p * w * 1.0, g - p * w * 1.0], mat, uvs=((0, 0), (1, 0), (1, 1), (0, 1))))
    return obs
def light_shafts(A, pr):
    """pr['shafts'] = 'pines' (rays through the Scots pines on Abbey Craig) | 'smoke' (rays through the campfire smoke columns) | 'both'. Along the sun direction, additive soft strips."""
    kind = pr.get('shafts'); rs = np.random.RandomState(pr.get('shaft_seed', 6)); sd = -np.array(STATE['P']['sun_dir'], float); sd /= np.linalg.norm(sd); n = 0; hw = np.array([sd[0], sd[1], 0.0]); hw /= np.linalg.norm(hw) + 1e-9
    if kind in ('pines', 'both'):
        for i in range(10):
            x = 138 + rs.uniform(-24, 26); y = 143 + rs.uniform(-22, 26); z = float(ground(x, y)); H = 13 + rs.uniform(0, 7)
            top = (x + sd[0] * H / sd[2], y + sd[1] * H / sd[2], z + H); add_shaft(top, (x, y, z), width=rs.uniform(5.0, 9.0)); n += 1
    if kind in ('smoke', 'both'):
        fires = list((A.get('camp') or {}).get('fires', [])) + [(-18.0, -52.0), (-28.0, -52.0), (-72.0, -20.0)]
        for (fx, fy) in fires[:8]:
            z = float(ground(fx, fy)); H = 12; top = (fx + 3 + sd[0] * H / sd[2], fy + 2 + sd[1] * H / sd[2], z + H); add_shaft(top, (fx + 3, fy + 2, z), width=rs.uniform(2.5, 4.0)); n += 1
    A['shafts'] = n
def table_lantern(A, pr):
    """a lantern hanging from the money-table canopy: a real emitter (bloom) plus a warm point light on the table."""
    tx, ty, tz = A['camp']['table']; B = Batch(99); lx, ly, lz = tx + 0.05, ty + 0.15, tz + 2.75
    B.rod('iron', (lx, ly, tz + 3.5), (lx, ly, lz + 0.22), 0.012, seg=4); B.cyl('iron', (lx, ly, lz + 0.18), 0.1, 0.04, seg=8); B.cyl('iron', (lx, ly, lz - 0.2), 0.1, 0.03, seg=8)
    for a_ in range(4): B.rod('iron', (lx + 0.09 * math.cos(a_ * 1.57), ly + 0.09 * math.sin(a_ * 1.57), lz - 0.2), (lx + 0.09 * math.cos(a_ * 1.57), ly + 0.09 * math.sin(a_ * 1.57), lz + 0.18), 0.008, seg=4)
    B.finalize('lantern'); G = Batch(100); G.sphere('glow_flame', (lx, ly, lz), 0.075, seg=8, rings=5); G.finalize('lantern_glow', ink=False, shadow=False)
    ld = bpy.data.lights.new('lantern', 'POINT'); ld.energy = 140.0; ld.color = (1.0, 0.7, 0.38); ld.shadow_soft_size = 0.12; ob = bpy.data.objects.new('lantern', ld); bpy.context.scene.collection.objects.link(ob); ob.location = (lx, ly, lz)
def preset_extras(A, pr):
    if pr.get('signs'): signs_build(A, pr)
    if pr.get('shafts'): light_shafts(A, pr)
    if pr.get('lantern') and A.get('camp', {}).get('table'): table_lantern(A, pr)

# ================================================================ CONNECTED WORLD + CAMERA PATH (client rule 2026-11-20: the camera travels instead of cutting)
WORLD_OVR = dict(glit_stretch=1.0, glit_s=0.6, glit_t=0.11, foam_k=2.5, wake_k=3.0, sun_k=1.8, reed_k=0.6, haze_max=0.2)
POSES = {'P_A': ((290.0, 205.0, 170.0), (120.0, 110.0, 10.0), 22.0), 'P_NECK': ((-2.0, 50.0, 4.6), (0.0, 22.0, 1.8), 22.0), 'P_TOP': ((-10.0, -40.0, 120.0), (0.0, 80.0, 0.0), 22.0),
         'P_CAMP': 'camp_wide', 'P_BANK': 'camp_bank'}          # named join poses (loc, look, lens) for cam_path keys; P_CAMP / P_BANK are the camp_wide / camp_bank presets
RIM_GOLD = '#ffc766'
def with_rim(pose, color=RIM_GOLD):
    """default warm-gold rim for a cast card: returns a copy of the pose dict with the puppet `rim` key set (v2/puppet/API.md: a light halo behind arms, hands, legs and feet where they
    leave the body silhouette). The scene cannot light an emission card, so every cast pose a render team builds should go through this (or set rim='#ffc766' itself)."""
    d = dict(pose); d.setdefault('rim', color); return d
def preset_pose(name):
    if name in POSES:
        v = POSES[name]
        if isinstance(v, str): return preset_pose(v)
        return v
    """(loc, look, lens) of a preset with the camera height resolved on the terrain (cam_dz)."""
    pr = PRESETS[name]
    if pr.get('cam_dz') is not None: ref = pr.get('cam_ref', pr['cam'][:2]); pr['cam'] = (pr['cam'][0], pr['cam'][1], float(ground(ref[0], ref[1])) + pr['cam_dz'])
    return tuple(pr['cam']), tuple(pr['look']), pr.get('lens', 22.0)
def build_world(presets, light='MORNING', fg=True, hide=(), over=None, placeholders=False):
    """ONE scene with the whole valley (terrain, river, loop, bridge, camp, Abbey Craig, castle, farms) plus the near-camera dressing of every preset in `presets`
    (foreground props, grass, reeds, heather, the money table extras, camp dressing, the Scots line, troops, signs, shafts, lantern). A camera can fly from one preset's pose
    to another's in this scene (see cam_path). fg = True builds every listed preset's foreground props, False none, or a list of preset names that keep them; `hide` = preset
    names whose foreground props are skipped (so props the camera passes through do not block the path). Returns A with A['marks'][preset] (stand points) and A['cams'][preset]
    = (loc, look, lens). Keep `presets` to the 2-3 a segment needs: every preset adds 3-40 s of build and some render time."""
    presets = list(presets); ov = dict(WORLD_OVR); ov.update(over or {})
    new_scene(light, ov); STATE['preset'] = presets[0] if presets else None; STATE['loc'] = 'world'; STATE['ink_t'] = 0.02
    A = dict(marks={}, cams={}, preset='world', presets=presets, light=light, location='world'); P0 = dict(farms=True, hill2=True, heather_n=800, gorse_n=170, crag_n=120, pine_n=55, clear=[], signs=[], troops={}, shafts=None)
    for p in presets:
        pr = PRESETS[p]; P0['clear'] = P0['clear'] + list(pr.get('clear', [])); P0['signs'] = sorted(set(P0['signs']) | set(pr.get('signs') or []))
        for w_, n_ in (pr.get('troops') or {}).items(): P0['troops'][w_] = max(P0['troops'].get(w_, 0), n_)
        if pr.get('shafts'): P0['shafts'] = 'both' if P0['shafts'] and P0['shafts'] != pr['shafts'] else pr['shafts']
    build_terrain(); build_water(); sky_dome(); sun()
    for fn in BUILDERS: fn(A, P0)
    keep = (lambda p: True) if fg is True else (lambda p: False) if fg is False else (lambda p: p in fg)
    for p in presets:
        pr = PRESETS[p]; A['cams'][p] = preset_pose(p); has_fg = keep(p) and p not in hide
        if pr.get('veg'): veg_near(A, pr)
        if has_fg:
            if pr.get('fg'): pr['fg'](A, pr)
            if pr.get('camp_fg'): pr['camp_fg'](A, pr)
            if pr.get('splashes'):
                for i_, (sx_, sy_, sa_) in enumerate(pr['splashes']): splash(sx_, sy_, (pr.get('splash_ages') or [0.35, 0.55, 0.8])[i_ % 3], pr.get('splash_size', 1.0), name='%s%d' % (p, i_), seed=i_)
        if pr.get('far_scots'): A['far_scots'] = scots_slope_line(22, 1, 1.45, np.random.RandomState(8), spear_h=3.2, a0=200, a1=250, hh0=7.0)
        if pr.get('bridge_pairs'):
            Bk = Batch(84); y0_, y1_, st_ = pr['bridge_pairs']; knight_pair_column(Bk, bridge_pairs(y0_, y1_, st_), BRIDGE_X, np.random.RandomState(9), KNIGHT_MATS); Bk.finalize('bridge_knights')
    if any(PRESETS[p].get('scots_line') for p in presets): A['scots_line'] = scots_slope_line(30, 3, 1.0, np.random.RandomState(3), spear_h=4.0) + spear_wall(14, 2, np.random.RandomState(4))
    first = presets[0] if presets else None
    cam0 = A['cams'][first] if first else ((0, -60, 40), (0, 0, 0), 22.0); camera(cam0[0], cam0[1], cam0[2]); cam = bpy.context.scene.camera
    for p in presets:
        pr = PRESETS[p]
        if pr.get('marks'): A['marks'][p] = pr['marks'](A)
        if pr.get('crowd') and keep(p) and p not in hide: pr['crowd'](A, pr)
    for where_, n_ in P0['troops'].items(): place_troops(A, where_, n_, seed=1)
    preset_extras(A, dict(P0, signs=P0['signs'], cam=A['cams'][first][0] if first else None, lantern=any(PRESETS[p].get('lantern') for p in presets), shafts=P0['shafts']))
    if placeholders:
        for p in presets:
            if A['marks'].get(p): stage_placeholders(A, cam=cam, marks=A['marks'][p])
    STATE['A'] = A; STATE['cams'] = A['cams']; return A

def _cr(p0, p1, p2, p3, t, dt0, dt1, dt2):
    """Catmull-Rom between p1 and p2 for non-uniform key times (tangents scaled by the segment length): smooth, passes through every key."""
    m1 = (p2 - p0) / (dt0 + dt1) * dt1 if dt0 + dt1 > 0 else np.zeros_like(p1); m2 = (p3 - p1) / (dt1 + dt2) * dt1 if dt1 + dt2 > 0 else np.zeros_like(p1)
    t2, t3 = t * t, t * t * t; return (2 * t3 - 3 * t2 + 1) * p1 + (t3 - 2 * t2 + t) * m1 + (-2 * t3 + 3 * t2) * p2 + (t3 - t2) * m2
def _nearest_vivid(loc):
    best = None
    for n in PRESETS:
        c = STATE.get('cams', {}).get(n) or preset_pose(n); d = float(np.linalg.norm(np.array(c[0]) - np.array(loc)))
        if best is None or d < best[0]: best = (d, n)
    return VIVID.get(best[1], (1.4, 1.3)), best[1]
def cam_path(cam, keys, g, clearance=1.2):
    """Fly the camera: keys = [(frame, loc, look, lens), ...] or [(frame, 'preset_name'), ...] (mixed is fine). Position = a smooth Catmull-Rom curve through the keys, the look
    target and the lens follow the same curve, with an ease-in on the first segment and an ease-out on the last one and no stops in between. STATE['vivid'] is eased between the
    VIVID entries of the presets the keys name (or the nearest preset for a free key) so the grade never jumps. Sets the camera object `cam` (None = the scene camera) for frame g and
    returns dict(loc, look, lens, vivid)."""
    ks = []
    for k in keys:
        if isinstance(k[1], str): loc, look, lens = (STATE.get('cams') or {}).get(k[1]) or preset_pose(k[1]); nm_ = POSES[k[1]] if isinstance(POSES.get(k[1]), str) else k[1]; viv = VIVID.get(nm_) or _nearest_vivid(loc)[0]
        else: loc, look, lens = k[1], k[2], k[3]; viv = _nearest_vivid(loc)[0]
        ks.append((float(k[0]), np.array(loc, float), np.array(look, float), float(lens), viv))
    ks.sort(key=lambda a: a[0]); n = len(ks); g = float(np.clip(g, ks[0][0], ks[-1][0])); i = 0
    while i < n - 2 and g > ks[i + 1][0]: i += 1
    f0, f1 = ks[i][0], ks[i + 1][0]; t = (g - f0) / max(f1 - f0, 1e-9)
    if n == 2: te = t * t * (3 - 2 * t)
    elif i == 0: te = t * t * (2 - t)                       # ease in on the first segment only (velocity 0 at the start, matches the next segment at its end)
    elif i == n - 2: te = 1 - (1 - t) ** 2 * (1 + t)        # ease out on the last segment (velocity 1 at its start, 0 at the end)
    else: te = t
    def at(j): return ks[min(max(j, 0), n - 1)]
    dts = [max(at(j + 1)[0] - at(j)[0], 1e-6) if 0 <= j < n - 1 else max(f1 - f0, 1e-6) for j in (i - 1, i, i + 1)]
    out = []
    for comp in (1, 2, 3):
        vals = [np.atleast_1d(np.array(at(j)[comp], float)) for j in (i - 1, i, i + 1, i + 2)]
        if i == 0: vals[0] = 2 * vals[1] - vals[2]
        if i == n - 2: vals[3] = 2 * vals[2] - vals[1]
        out.append(_cr(vals[0], vals[1], vals[2], vals[3], te, dts[0], dts[1], dts[2]))
    loc, look, lens = out[0], out[1], float(out[2][0]); v0, v1 = ks[i][4], ks[i + 1][4]; tv = te
    viv = (math.exp((1 - tv) * math.log(v0[0]) + tv * math.log(v1[0])), (1 - tv) * v0[1] + tv * v1[1]); STATE['vivid'] = viv
    cam = cam or bpy.context.scene.camera
    gz = max(float(ground(loc[0], loc[1])), 0.0) + clearance; loc = np.array([loc[0], loc[1], loc[2] + (gz - loc[2]) * (1 / (1 + math.exp(-(gz - loc[2]) * 4.0))) if loc[2] < gz + 1.5 else loc[2]])   # keep the lens above the terrain (soft)
    cam.location = tuple(loc); cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
    return dict(loc=tuple(loc), look=tuple(look), lens=lens, vivid=viv)


def build_for_cli(preset, light='MORNING', placeholders=True):
    A = build(preset=preset, light=light); pr = PRESETS[preset]
    nofg = os.environ.get('DBG') == 'nofg'
    if pr.get('fg') and not nofg: pr['fg'](A, pr)
    if pr.get('camp_fg') and not nofg: pr['camp_fg'](A, pr)
    if not nofg: preset_extras(A, pr)
    for where_, n_ in (pr.get('troops') or {}).items():
        if not nofg: place_troops(A, where_, n_, seed=pr.get('troop_seed', 1))
    if pr.get('scots_line') and not nofg and preset != 'valley_loop': A['scots_line'] = scots_slope_line(30, 3, 1.0, np.random.RandomState(3), spear_h=4.0) + spear_wall(14, 2, np.random.RandomState(4))
    for i_, (sx_, sy_, sa_) in enumerate(pr.get('splashes') or []):
        if not nofg: splash(sx_, sy_, (pr.get('splash_ages') or [0.35, 0.55, 0.8])[i_ % 3], pr.get('splash_size', 1.0), name=str(i_), seed=i_)
    if pr.get('far_scots') and not nofg: rs_ = np.random.RandomState(8); A['far_scots'] = scots_slope_line(22, 1, 1.45, rs_, spear_h=3.2, a0=200, a1=250, hh0=7.0)
    if pr.get('bridge_pairs') and not nofg:
        Bk = Batch(84); y0_, y1_, st_ = pr['bridge_pairs']; knight_pair_column(Bk, bridge_pairs(y0_, y1_, st_), BRIDGE_X, np.random.RandomState(9), KNIGHT_MATS); Bk.finalize('bridge_knights')
    if pr.get('crowd') and not nofg: pr['crowd'](A, pr)
    if placeholders and A['marks'] and not nofg: stage_placeholders(A)
    return A
def cli_render(preset, light='MORNING', out=None, mode='final', samples=None, placeholders=True):
    samples = samples or PRESETS[preset].get('samples') if mode == 'final' else samples
    t0 = time.time(); A = build_for_cli(preset, light, placeholders); tb = time.time() - t0; dt = render(out, mode, samples)
    cam = bpy.context.scene.camera; heads = head_report(A, cam)
    info = dict(preset=preset, light=light, build_s=round(tb, 2), render_s=round(dt, 2), mode=mode, samples=bpy.context.scene.cycles.samples, heads=heads, objects=len(bpy.data.objects),
                tris=int(sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH')))
    json.dump(info, open(out + '.json', 'w'), default=float); return dt, info
if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'render':
        if len(a) < 3: sys.exit('usage: python3 stirling.py render <preset> [-|MORNING] <out.png> [final|draft] [samples] | list')
        preset = a[1]; rest = a[2:]
        if rest[0] == '-' or rest[0] in LIGHTS: rest = rest[1:]              # '-' (or the light name) is a no-op placeholder: there is one light
        if not rest: sys.exit('missing <out.png>')
        out = rest[0]; mode = rest[1] if len(rest) > 1 else 'final'; samples = int(rest[2]) if len(rest) > 2 and rest[2].isdigit() else None
        if mode not in ('final', 'draft'): sys.exit("error: mode must be 'final' or 'draft', got %r" % mode)
        if preset not in PRESETS: sys.exit('error: unknown preset %r (python3 stirling.py list)' % preset)
        dt, info = cli_render(preset, 'MORNING', out, mode, samples); print('%s %.1fs build %.1fs tris %d heads %s' % (preset, dt, info['build_s'], info['tris'], {k: (v['cx'], v['cy']) for k, v in info['heads'].items()}))
    elif a and a[0] == 'list':
        for k, v in PRESETS.items(): print('%-16s %-8s cam %s -> %s' % (k, v['loc'], v['cam'], v['look']))
    else: print('usage: python3 stirling.py render <preset> [-|MORNING] <out.png> [final|draft] [samples] | list')
