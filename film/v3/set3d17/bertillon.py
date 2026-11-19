"""film 17 set kit, full set ("Bertillon", Paris police 1882-83). bpy 5.x, Cycles CPU. 1 unit = 1 m, Z up; a grown person = 1.7 units = 1 D.
Four locations (measure, records, reveal, street), 17 camera presets, 3 light presets, life hooks. See API.md.
Series light model: a toon-cosine key (sun / gas lamps) + a flat blue-violet ambient injected as emission with per-surface shade_mul
and a navy lift, matte materials only, drawn textures (bertillon_tex.py), inverted-hull ink on man-made props, no depth of field, no text."""
import os, sys, math, random, contextlib, time, json
import numpy as np
import bpy, bmesh
from PIL import Image, ImageDraw
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bertillon_tex as TX

D = 1.7                                     # one character height in units
HEIGHT = {'clerk': 1.78, 'prisoner': 1.68, 'inspector': 1.66, 'gendarme': 1.82, 'prefect': 1.74}
STATE = {'P': None, 'ink_t': 0.012, 'lamps': [], 'glows': [], 'anim': {}, 'loc': None, 'preset': None}

def hex_lin(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)

# ---------------------------------------------------------------- light presets (the series model)
# displayed = art * gain * KEY * vis * toon(cos)  +  ((1-m) art SHADE shade_mul + m lum(art) TINT mean(shade_mul) + LIFT) * (1 + N.form)
LIGHTS = {
    'DAY_INT': dict(key=(2.30, 1.65, 0.74), sun_dir=(0.78, 0.25, -0.56), sun_angle=0.8, sun=True, shade=(0.19, 0.21, 0.52), tint=(0.14, 0.16, 0.34), mix=0.85,
                    lift=(0.004, 0.012, 0.030), form=(0.0, -0.05, 0.22), lamp_k=1.7, sky=('#4a78cd', '#92b7e7', '#92b7e7'), sky_k=1.0, ink='#2e1a26', world=(0.35, 0.5, 0.8),
                    gain=1.0, glow=1.0),
    'EVENING_INT': dict(key=(2.0, 1.12, 0.46), sun_dir=(0.85, 0.15, -0.28), sun_angle=1.2, sun=True, shade=(0.19, 0.19, 0.50), tint=(0.235, 0.22, 0.56), mix=0.75,
                        lift=(0.005, 0.011, 0.032), form=(0.0, -0.05, 0.22), lamp_k=1.0, sky=('#40448f', '#d98a78', '#f6b97c'), sky_k=1.0, ink='#2a1626', world=(0.3, 0.25, 0.4),
                        gain=0.82, glow=1.15),
    'DUSK_EXT': dict(key=(2.0, 1.05, 0.50), sun_dir=(-0.55, -0.80, -0.30), sun_angle=1.0, sun=True, shade=(0.20, 0.20, 0.52), tint=(0.245, 0.23, 0.58), mix=0.75,
                     lift=(0.005, 0.012, 0.034), form=(0.0, -0.05, 0.22), lamp_k=1.0, sky=('#5e5aa8', '#e8837f', '#ffd592'), sky_k=1.0, ink='#2a1626', world=(0.4, 0.3, 0.45),
                     gain=0.9, glow=1.2),
}
SUN_STRENGTH = 3.94          # sun strength per unit of key colour (calibrated, see calibrate())
LAMP_W = 1.0                # watts scale for point lights (calibrated)

# ---------------------------------------------------------------- materials
def _pal():
    pl = {}
    def add(k, col, tex=None, tile=1.0, tint=False, sm=(1, 1, 1), ink=False, gain=1.0, off=(0, 0, 0), mix=None, afl=0.12):
        pl[k] = dict(col=col, tex=tex, tile=tile, tint=tint, sm=sm, ink=ink, gain=gain, off=off, mix=mix, afl=afl)
    add('floor', '#966430', TX.planks('floor', (0x96, 0x64, 0x30), n=6, seed=11), tile=1.5, sm=(0.9, 1.0, 1.15), afl=0.20)
    add('floor_dk', '#5e3320', TX.planks('floor_dk', (0x5c, 0x32, 0x20), n=6, seed=12), tile=1.5, sm=(0.9, 1.0, 1.15), afl=0.20)
    add('wall', '#bd8236', TX.plaster('wall', (0xbd, 0x82, 0x36), seed=3), tile=2.5, mix=0.9, afl=0.20, sm=(0.8, 0.95, 1.15))
    add('wall_ochre', '#b0803a', TX.plaster('wall_ochre', (0xb0, 0x80, 0x3a), seed=4), tile=2.5, mix=0.9, afl=0.20)
    add('wall_dk', '#8e3a2a', TX.plaster('wall_dk', (0x8e, 0x3a, 0x2a), seed=5), tile=2.5, mix=0.9, afl=0.20)
    add('wain', '#552018', TX.wain_panels('wain', (0x55, 0x20, 0x18)), tile=1.0, mix=0.85, afl=0.20)
    add('ceiling', '#6a4326', TX.boards('ceiling', (0x6a, 0x43, 0x26), seed=13), tile=1.5, mix=0.85, afl=0.20)
    add('beam', '#4a2c19', TX.boards('beam', (0x4a, 0x2c, 0x19), seed=14, n=3), tile=1.0, ink=True)
    add('frieze', '#5a1c18', TX.frieze('frieze'), tile=1.0, mix=0.85, afl=0.20)
    add('walnut', '#6e4026', TX.boards('walnut', (0x6e, 0x40, 0x26), seed=15), tile=1.0, tint=True, ink=True, sm=(0.95, 1.0, 1.1))
    add('honey', '#b06a32', TX.boards('honey', (0xb0, 0x6a, 0x32), seed=16, n=3), tile=0.9, tint=True, ink=True, sm=(0.95, 1.0, 1.1))
    add('oak', '#a8703c', TX.boards('oak', (0xa8, 0x70, 0x3c), seed=17, n=2), tile=0.8, tint=True, ink=True, sm=(0.95, 1.0, 1.1))
    add('oxblood', '#7c1f2a', tint=True, ink=True, mix=0.8)
    add('navy', '#26395e', tint=True, ink=True, sm=(0.9, 0.95, 1.2))
    add('baize', '#2f5a44', tint=True, ink=True, mix=0.8)
    add('leather', '#66371f', tint=True, ink=True)
    add('cream', '#f0e2bc', tint=True, ink=False, mix=0.5)
    add('brass', '#d29d38', tint=True, ink=True, mix=0.5)
    add('steel', '#8a9ab6', tint=True, ink=True, mix=0.5)
    add('iron', '#3b3f55', ink=True, mix=0.5)
    add('cloth', '#2a2438', ink=True, mix=0.7)
    add('ink', '#2a2236', mix=0.6)
    add('glass', '#7fa6a8', mix=0.6)
    add('dark', '#34232c', mix=0.6)
    add('runner', '#26395e', TX.runner('runner'), tile=1.4, off=(0.5, 0, 0), sm=(0.9, 0.95, 1.2), mix=0.8)
    add('stone', '#bf9560', TX.ashlar('stone', (0xbf, 0x95, 0x60)), tile=2.0, mix=0.8)
    add('stone_dk', '#a97a4d', TX.ashlar('stone_dk', (0xa9, 0x7a, 0x4d), seed=21), tile=2.0, mix=0.8)
    add('cobble', '#8a7468', TX.cobbles('cobble', (0x8c, 0x76, 0x6a)), tile=4.0, mix=0.8)
    add('zinc', '#6d7c9c', TX.zinc('zinc', (0x6d, 0x7c, 0x9c)), tile=2.0, ink=True, mix=0.6)
    add('terracotta', '#b0502f', ink=True, mix=0.8)
    add('wagon', '#2d3350', tint=True, ink=True, sm=(0.9, 0.95, 1.2))
    add('wagon_red', '#8a2a2e', ink=True)
    add('flat_card', '#5a6480', mix=1.0)
    add('smoke', '#8c86a8', mix=0.9)
    add('cardedge', '#efe0b8', ink=True, mix=0.5)
    return pl
def _mk_tree(m):
    m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    return nt
_MATS = {}
def get_mat(key):
    if key in _MATS: return _MATS[key]
    if key.startswith('glow'): m = _glow_mat(key)
    elif key == 'ink_hull': m = _ink_mat()
    elif key == 'sky': m = _sky_mat()
    elif key == 'beam_fx': m = _beam_mat()
    elif key == 'puddle': m = _puddle_mat()
    elif key.startswith('card_'): m = _card_mat(key)
    elif key.startswith('ph_'): m = _ph_mat(key)
    else: m = _lit_mat(key, STATE['PAL'][key])
    _MATS[key] = m; return m
def _lit_mat(key, s):
    P = STATE['P']; m = bpy.data.materials.new(key); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); dif.inputs['Roughness'].default_value = 1.0
    if s['tex']:
        it = N('ShaderNodeTexImage'); it.image = bpy.data.images.load(s['tex'], check_existing=True); it.interpolation = 'Linear'
        it.projection = 'BOX'; it.projection_blend = 0.2
        tc = N('ShaderNodeTexCoord'); mp = N('ShaderNodeMapping'); k = 1.0 / s['tile']; mp.inputs['Scale'].default_value = (k, k, k); mp.inputs['Location'].default_value = s['off']
        L(tc.outputs['Object'], mp.inputs[0]); L(mp.outputs[0], it.inputs[0]); art = it.outputs['Color']
    else:
        rgb = N('ShaderNodeRGB'); rgb.outputs[0].default_value = (*hex_lin(s['col']), 1); art = rgb.outputs[0]
    if s['tint']:
        at = N('ShaderNodeAttribute'); at.attribute_name = 'tint'; at.attribute_type = 'GEOMETRY'
        mt = N('ShaderNodeMix'); mt.data_type = 'RGBA'; mt.blend_type = 'MULTIPLY'; mt.inputs[0].default_value = 1
        L(art, mt.inputs[6]); L(at.outputs['Color'], mt.inputs[7]); art = mt.outputs[2]
    geo = N('ShaderNodeNewGeometry'); bw = N('ShaderNodeRGBToBW'); L(art, bw.inputs[0])
    dcol = art
    if P['sun'] and P.get('toon'):     # toon key: faces square to the sun get the full key, grazing faces are lifted by 1/max(cos, 0.5)
        kd = Vector(P['sun_dir']).normalized(); dot = N('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'; dot.inputs[1].default_value = (-kd.x, -kd.y, -kd.z); L(geo.outputs['True Normal'], dot.inputs[0])
        mx = N('ShaderNodeMath'); mx.operation = 'MAXIMUM'; mx.inputs[1].default_value = 0.5; L(dot.outputs['Value'], mx.inputs[0])
        inv = N('ShaderNodeMath'); inv.operation = 'DIVIDE'; inv.inputs[0].default_value = 1.0; L(mx.outputs[0], inv.inputs[1])
        gt = N('ShaderNodeMath'); gt.operation = 'GREATER_THAN'; gt.inputs[1].default_value = 0.02; L(dot.outputs['Value'], gt.inputs[0])
        sm_ = N('ShaderNodeMath'); sm_.operation = 'SUBTRACT'; sm_.inputs[1].default_value = 1.0; L(inv.outputs[0], sm_.inputs[0])
        fc = N('ShaderNodeMath'); fc.operation = 'MULTIPLY_ADD'; fc.inputs[2].default_value = s['gain']; L(sm_.outputs[0], fc.inputs[0]); L(gt.outputs[0], fc.inputs[1])
        sc = N('ShaderNodeVectorMath'); sc.operation = 'SCALE'; L(art, sc.inputs[0]); L(fc.outputs[0], sc.inputs['Scale']); dcol = sc.outputs['Vector']
    gk = N('ShaderNodeVectorMath'); gk.operation = 'SCALE'; gk.inputs['Scale'].default_value = P['gain']; L(dcol, gk.inputs[0]); L(gk.outputs['Vector'], dif.inputs['Color'])
    mix = P['mix'] if s['mix'] is None else s['mix']; sm = s['sm']; smm = sum(sm) / 3.0
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0; L(art, ms.inputs[6]); ms.inputs[7].default_value = (*[a * b for a, b in zip(P['shade'], sm)], 1)
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 1.0 - mix; L(ms.outputs[2], sa.inputs[0])
    lm = N('ShaderNodeMath'); lm.operation = 'MULTIPLY_ADD'; lm.inputs[1].default_value = 1.0 - s['afl']; lm.inputs[2].default_value = s['afl']; L(bw.outputs[0], lm.inputs[0])
    tb = N('ShaderNodeVectorMath'); tb.operation = 'SCALE'; L(lm.outputs[0], tb.inputs['Scale']); tb.inputs[0].default_value = tuple(x * mix * smm for x in P['tint'])
    ab = N('ShaderNodeVectorMath'); ab.operation = 'ADD'; L(sa.outputs['Vector'], ab.inputs[0]); L(tb.outputs['Vector'], ab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P['lift']); L(ab.outputs['Vector'], lf.inputs[0]); amb = lf.outputs['Vector']
    fd = N('ShaderNodeVectorMath'); fd.operation = 'DOT_PRODUCT'; fd.inputs[1].default_value = tuple(P['form']); L(geo.outputs['True Normal'], fd.inputs[0])
    fa = N('ShaderNodeMath'); fa.operation = 'ADD'; fa.inputs[1].default_value = 1.0; L(fd.outputs['Value'], fa.inputs[0])
    fs = N('ShaderNodeVectorMath'); fs.operation = 'SCALE'; L(amb, fs.inputs[0]); L(fa.outputs[0], fs.inputs['Scale']); amb = fs.outputs['Vector']
    em = N('ShaderNodeEmission'); L(amb, em.inputs['Color']); em.inputs['Strength'].default_value = 1.0
    ad = N('ShaderNodeAddShader'); L(dif.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1]); L(ad.outputs['Shader'], out.inputs['Surface'])
    return m
def _glow_mat(key):
    """emitters: glow_gas (lamp glass), glow_frost (skylights), glow_win (lit windows), glow_green, glow_door. Strength node named 'strength'."""
    P = STATE['P']
    spec = {'glow_gas': ('#ffc46a', 14.0 * P['glow']), 'glow_frost': ('#d6e4ff', 3.0), 'glow_win': ('#ffcf86', 5.0 * P['glow']), 'glow_green': ('#8ff0a8', 3.0),
            'glow_door': ('#ffd9a0', 4.0), 'glow_dust': ('#fff0c8', 5.0)}[key]
    m = bpy.data.materials.new(key); nt = _mk_tree(m); out = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); e.name = 'strength'
    e.inputs[0].default_value = (*hex_lin(spec[0]), 1); e.inputs[1].default_value = spec[1]; nt.links.new(e.outputs[0], out.inputs[0])
    if key in ('glow_gas', 'glow_win'): STATE['glows'].append((m, spec[1]))
    return m
def _ink_mat():
    P = STATE['P']; m = bpy.data.materials.new('ink_hull'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); geo = N('ShaderNodeNewGeometry'); lp = N('ShaderNodeLightPath'); emi = N('ShaderNodeEmission'); emi.inputs['Color'].default_value = (*hex_lin(P['ink']), 1)
    tr = N('ShaderNodeBsdfTransparent'); mix = N('ShaderNodeMixShader'); notcam = N('ShaderNodeMath'); notcam.operation = 'SUBTRACT'; notcam.inputs[0].default_value = 1.0
    fac = N('ShaderNodeMath'); fac.operation = 'MAXIMUM'; L(lp.outputs['Is Camera Ray'], notcam.inputs[1]); L(geo.outputs['Backfacing'], fac.inputs[0]); L(notcam.outputs[0], fac.inputs[1])
    L(fac.outputs[0], mix.inputs['Fac']); L(emi.outputs['Emission'], mix.inputs[1]); L(tr.outputs['BSDF'], mix.inputs[2]); L(mix.outputs['Shader'], out.inputs['Surface'])
    return m
def _sky_mat():
    """vertical gradient on world z (object coords of the dome at the origin): horizon colour at z 4, deep sky colour at z 95."""
    P = STATE['P']; m = bpy.data.materials.new('sky'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); mr = N('ShaderNodeMapRange'); cr = N('ShaderNodeValToRGB'); e = N('ShaderNodeEmission')
    L(tc.outputs['Object'], sp.inputs[0]); L(sp.outputs['Z'], mr.inputs[0]); mr.inputs[1].default_value = 4.0; mr.inputs[2].default_value = 260.0; mr.inputs[3].default_value = 0.0; mr.inputs[4].default_value = 1.0; mr.clamp = True
    L(mr.outputs[0], cr.inputs[0]); top, mid, bot = P['sky']
    cr.color_ramp.elements[0].position = 0.0; cr.color_ramp.elements[0].color = (*hex_lin(bot), 1); cr.color_ramp.elements[1].position = 1.0; cr.color_ramp.elements[1].color = (*hex_lin(top), 1)
    el = cr.color_ramp.elements.new(0.28); el.color = (*hex_lin(mid), 1)
    L(cr.outputs[0], e.inputs[0]); e.inputs[1].default_value = P['sky_k']; L(e.outputs[0], out.inputs[0]); return m
def _beam_mat():
    """light shaft: additive, camera rays only."""
    m = bpy.data.materials.new('beam_fx'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lp = N('ShaderNodeLightPath'); e = N('ShaderNodeEmission'); tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader')
    e.inputs[0].default_value = (*hex_lin('#ffd890'), 1); e.inputs[1].default_value = 0.035; e.name = 'strength'
    L(tr.outputs[0], ad.inputs[0]); L(e.outputs[0], ad.inputs[1]); mixs = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mixs.inputs['Fac']); L(tr.outputs[0], mixs.inputs[1]); L(ad.outputs[0], mixs.inputs[2])
    L(mixs.outputs[0], out.inputs[0]); return m
def _puddle_mat():
    P = STATE['P']; m = bpy.data.materials.new('puddle'); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); gl = N('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.02; gl.inputs['Color'].default_value = (0.8, 0.82, 0.95, 1)
    df = N('ShaderNodeBsdfDiffuse'); df.inputs['Color'].default_value = (*hex_lin('#3a3050'), 1); mx = N('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 0.8
    L(df.outputs[0], mx.inputs[1]); L(gl.outputs[0], mx.inputs[2]); em = N('ShaderNodeEmission'); em.inputs[0].default_value = tuple(P['lift']) + (1,); em.inputs[1].default_value = 1.0
    ad = N('ShaderNodeAddShader'); L(mx.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs[0]); return m
PH_COL = {'clerk': '#2c2a3c', 'prisoner': '#6a5a52', 'gendarme': '#27365a', 'inspector': '#5a3a3a', 'prefect': '#3a3a52', 'seated': '#5a3a3a'}
def _ph_mat(key):
    hexc = '#fef7f6' if key == 'ph_head' else STATE['P']['ink'] if key == 'ph_ring' else PH_COL[key[8:]]
    m = bpy.data.materials.new(key); nt = _mk_tree(m); e = nt.nodes.new('ShaderNodeEmission'); e.inputs[0].default_value = (*hex_lin(hexc), 1); o = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(e.outputs[0], o.inputs[0]); return m
def _card_mat(key):
    """image card (Bertillon card, notices, portraits): paper lit by the key + ambient shade; UV mapped."""
    path = STATE['cardpaths'][key]; P = STATE['P']; m = bpy.data.materials.new(key); nt = _mk_tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); dif = N('ShaderNodeBsdfDiffuse'); em = N('ShaderNodeEmission'); ad = N('ShaderNodeAddShader'); it = N('ShaderNodeTexImage')
    it.image = bpy.data.images.load(path, check_existing=True); it.interpolation = 'Linear'; tc = N('ShaderNodeTexCoord'); L(tc.outputs['UV'], it.inputs[0])
    gk = N('ShaderNodeVectorMath'); gk.operation = 'SCALE'; gk.inputs['Scale'].default_value = P['gain']; L(it.outputs['Color'], gk.inputs[0]); L(gk.outputs[0], dif.inputs['Color'])
    bw = N('ShaderNodeRGBToBW'); L(it.outputs['Color'], bw.inputs[0]); mu = N('ShaderNodeVectorMath'); mu.operation = 'SCALE'; L(bw.outputs[0], mu.inputs['Scale']); mu.inputs[0].default_value = tuple(x * 0.9 for x in P['tint'])
    ms = N('ShaderNodeMix'); ms.data_type = 'RGBA'; ms.blend_type = 'MULTIPLY'; ms.inputs[0].default_value = 1.0; L(it.outputs['Color'], ms.inputs[6]); ms.inputs[7].default_value = (*P['shade'], 1)
    sa = N('ShaderNodeVectorMath'); sa.operation = 'SCALE'; sa.inputs['Scale'].default_value = 0.4; L(ms.outputs[2], sa.inputs[0]); sb = N('ShaderNodeVectorMath'); sb.operation = 'SCALE'; sb.inputs['Scale'].default_value = 0.6
    L(mu.outputs[0], sb.inputs[0]); ab = N('ShaderNodeVectorMath'); ab.operation = 'ADD'; L(sa.outputs[0], ab.inputs[0]); L(sb.outputs[0], ab.inputs[1])
    lf = N('ShaderNodeVectorMath'); lf.operation = 'ADD'; lf.inputs[1].default_value = tuple(P['lift']); L(ab.outputs[0], lf.inputs[0]); L(lf.outputs[0], em.inputs[0])
    L(dif.outputs[0], ad.inputs[0]); L(em.outputs[0], ad.inputs[1]); L(ad.outputs[0], out.inputs[0]); return m

# ---------------------------------------------------------------- batched geometry
def rotm(rx=0, ry=0, rz=0):
    a, b, c = map(math.radians, (rx, ry, rz)); ca, sa, cb, sb, cc, sc = math.cos(a), math.sin(a), math.cos(b), math.sin(b), math.cos(c), math.sin(c)
    Rx = np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]]); Ry = np.array([[cb, 0, sb], [0, 1, 0], [-sb, 0, cb]]); Rz = np.array([[cc, -sc, 0], [sc, cc, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx
def _m4(loc=(0, 0, 0), rot=(0, 0, 0), scale=1.0):
    m = np.eye(4); m[:3, :3] = rotm(*rot) * scale; m[:3, 3] = loc; return m
def euler_to_z(d):
    """euler degrees that rotate local +z onto direction d."""
    d = np.array(d, float); d /= np.linalg.norm(d); ay = math.degrees(math.acos(max(-1, min(1, d[2])))); az = math.degrees(math.atan2(d[1], d[0]))
    Rm = rotm(0, ay, az); return (math.degrees(math.atan2(Rm[2, 1], Rm[2, 2])), math.degrees(-math.asin(max(-1, min(1, Rm[2, 0])))), math.degrees(math.atan2(Rm[1, 0], Rm[0, 0])))
_CUBE_F = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
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
                ff = [(i, (i + 1) % seg, seg) for i in range(seg)]
                ff = [(b_, a_, c_) for a_, b_, c_ in ff] if rev else ff
                self._put(mat, (Rm @ cv.T).T + np.array(c), [(f_[1], f_[0], f_[2]) if rev else f_ for f_ in ff] if False else ff, False, tint)
    def sphere(self, mat, c, r, seg=18, rings=10, scale=(1, 1, 1), tint=1.0):
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
        self._put(mat, np.array(v) * np.array(scale) * r + np.array(c), [tuple(x) for x in f], True, tint)
    def mesh(self, mat, v, faces, smooth=True, tint=1.0): self._put(mat, v, faces, smooth, tint)
    def quad(self, mat, p0, p1, p2, p3, tint=1.0): self._put(mat, [p0, p1, p2, p3], [(0, 1, 2, 3)], False, tint)
    def prism_roof(self, mat, c, w, d, h, rot_z=0, ridge_frac=1.0, tint=1.0):
        """gable roof: base w x d at z c[2], ridge along local x at height h (ridge_frac < 1 shortens the ridge: hip roof)."""
        hw, hd = w / 2, d / 2; rl = hw * ridge_frac
        v = [(-hw, -hd, 0), (hw, -hd, 0), (hw, hd, 0), (-hw, hd, 0), (-rl, 0, h), (rl, 0, h)]
        f = [(0, 1, 5, 4), (2, 3, 4, 5), (3, 0, 4), (1, 2, 5), (3, 2, 1, 0)]
        with self.xf(c, (0, 0, rot_z)): self._put(mat, v, f, False, tint)
    def finalize(self, prefix='set', loc=(0, 0, 0), parent=None, bevel=0.0, ink=True, ink_t=None):
        objs = []; coll = bpy.context.scene.collection
        for key, Dd in self.d.items():
            V = np.concatenate(Dd['v']); me = bpy.data.meshes.new('%s_%s' % (prefix, key)); me.from_pydata(V.tolist(), [], Dd['f']); me.update()
            me.polygons.foreach_set('use_smooth', Dd['s'])
            bm = bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); bm.to_mesh(me); bm.free()
            ca = me.color_attributes.new('tint', 'FLOAT_COLOR', 'POINT'); ca.data.foreach_set('color', np.concatenate(Dd['t']).ravel())
            ob = bpy.data.objects.new('%s_%s' % (prefix, key), me); coll.objects.link(ob); ob.location = loc; ob.data.materials.append(get_mat(key))
            if parent is not None: ob.parent = parent
            if key.startswith('glow') or key in ('sky', 'beam_fx'): ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
            if key == 'sky': ob.visible_diffuse = ob.visible_glossy = False
            if key == 'beam_fx': ob.visible_diffuse = ob.visible_glossy = ob.visible_transmission = False
            objs.append(ob)
            it_ = STATE['ink_t'] if ink_t is None else ink_t
            if ink and key in STATE['PAL'] and STATE['PAL'][key]['ink'] and it_ > 0: objs.append(add_hull(ob, it_))
        self.d = {}; return objs
def add_hull(ob, t):
    """inverted-hull ink outline (camera rays only): a solidify shell, flipped normals, mat 'ink_hull' (transparent on front faces)."""
    hob = bpy.data.objects.new(ob.name + '_ink', ob.data.copy()); bpy.context.scene.collection.objects.link(hob); hob.location = ob.location; hob.rotation_euler = ob.rotation_euler; hob.parent = ob.parent
    hob.data.materials.clear(); hob.data.materials.append(get_mat('ink_hull'))
    md = hob.modifiers.new('ink', 'SOLIDIFY'); md.thickness = t; md.offset = 1.0; md.use_flip_normals = True; md.use_rim = False; md.use_even_offset = True
    hob.visible_shadow = hob.visible_diffuse = hob.visible_glossy = hob.visible_transmission = hob.visible_volume_scatter = False
    return hob

# ---------------------------------------------------------------- scene, lights, camera
def new_scene(light='DAY_INT', over=None):
    bpy.ops.wm.read_factory_settings(use_empty=True); _MATS.clear(); STATE['lamps'] = []; STATE['glows'] = []; STATE['anim'] = {}; STATE['cardpaths'] = {}
    for im in list(bpy.data.images): bpy.data.images.remove(im)
    STATE['P'] = dict(LIGHTS[light], **(over or {})); STATE['light'] = light; STATE['PAL'] = _pal(); P = STATE['P']
    sc = bpy.context.scene; sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True; bg = w.node_tree.nodes['Background']; bg.inputs[0].default_value = (*[x * 0.5 for x in P['world']], 1); bg.inputs[1].default_value = 0.3
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = 0.0; sc.render.film_transparent = False
    sc.cycles.max_bounces = 6; sc.cycles.diffuse_bounces = 0; sc.cycles.glossy_bounces = 2; sc.cycles.transmission_bounces = 0; sc.cycles.transparent_max_bounces = 16
    sc.cycles.sample_clamp_indirect = 8.0; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.02
    sc.render.fps = 30; return sc
def sun(light=None, strength=None):
    P = STATE['P']; k = np.array(P['key']); s = float(k.max()); d = bpy.data.lights.new('key', 'SUN'); d.energy = SUN_STRENGTH * s * (strength or 1.0); d.color = tuple(k / s); d.angle = math.radians(P['sun_angle'])
    ob = bpy.data.objects.new('key', d); bpy.context.scene.collection.objects.link(ob); ob.rotation_euler = Vector(P['sun_dir']).normalized().to_track_quat('-Z', 'Y').to_euler(); return ob
def point(loc, color=(1.0, 0.82, 0.54), watts=100, radius=0.08, name='lamp', flicker=True):
    P = STATE['P']; d = bpy.data.lights.new(name, 'POINT'); d.energy = watts * LAMP_W * P['lamp_k']; d.color = color; d.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, d); ob.location = loc; bpy.context.scene.collection.objects.link(ob)
    if flicker: STATE['lamps'].append((ob, d.energy))
    return ob
def spot(loc, target, watts=300, angle=60, blend=0.5, color=(1.0, 0.72, 0.4), name='spot', radius=0.06):
    P = STATE['P']; d = bpy.data.lights.new(name, 'SPOT'); d.energy = watts * LAMP_W * P['lamp_k']; d.color = color; d.spot_size = math.radians(angle); d.spot_blend = blend; d.shadow_soft_size = radius
    ob = bpy.data.objects.new(name, d); ob.location = loc; bpy.context.scene.collection.objects.link(ob)
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); return ob
def camera(loc, target, lens=22.0, roll=0.0):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'AUTO'; c.dof.use_dof = False; c.clip_end = 400
    ob = bpy.data.objects.new('cam', c); bpy.context.scene.collection.objects.link(ob); ob.location = loc
    ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); bpy.context.scene.camera = ob; return ob
def sky_dome(radius=150.0):
    b = Batch(); b.sphere('sky', (0, 0, 0), radius, seg=32, rings=16); return b.finalize('sky', ink=False)

# ---------------------------------------------------------------- lamps (gas: glass globe + point light, pipes)
def gas_bracket(B, loc, rot_z=0, watts=14, arm=0.3):
    """wall gas lamp: brass plate, arm, tap, shade ring, frosted globe + point light. loc = wall contact, local +x = out of the wall."""
    with B.xf(loc, (0, 0, rot_z)):
        B.box('brass', (0.03, 0, 0), (0.06, 0.12, 0.2)); B.cyl('brass', (arm / 2, 0, 0), 0.016, arm, axis='x', seg=8)
        B.cyl('brass', (arm, 0, -0.04), 0.02, 0.1, seg=8); B.cyl('brass', (arm, 0, -0.1), 0.05, 0.04, r2=0.034, seg=12)
        B.cyl('brass', (arm, 0, -0.14), 0.05, 0.03, r2=0.075, seg=12); B.sphere('glow_gas', (arm, 0, -0.25), 0.09, scale=(1, 1, 1.2))
        B.cyl('brass', (arm, 0, -0.38), 0.04, 0.03, r2=0.02, seg=10)
        wp = B.wpt((arm, 0, -0.25))
    point(wp, watts=watts, radius=0.09)
def gas_pipe(B, p0, p1, r=0.017):
    """iron gas pipe between two points + collars."""
    p0 = np.array(p0, float); p1 = np.array(p1, float); v = p1 - p0; L = np.linalg.norm(v)
    B.cyl('iron', tuple((p0 + p1) / 2), r, L, rot=euler_to_z(v), seg=8)
    for t in np.arange(0.12, 1.0, 0.3): B.cyl('iron', tuple(p0 + v * t), r * 1.6, 0.03, rot=euler_to_z(v), seg=8)
def gasolier(B, loc, drop=1.0, watts=200, arms=3, r=0.3):
    """hanging gas chandelier: iron pipe from the ceiling, brass body, curved arms with frosted globes (each a point light)."""
    x, y, z = loc; B.cyl('iron', (x, y, z - drop / 2), 0.016, drop, seg=8); B.cyl('brass', (x, y, z - 0.03), 0.07, 0.06, r2=0.04, seg=12); B.sphere('brass', (x, y, z - drop), 0.06)
    B.cyl('brass', (x, y, z - drop - 0.06), 0.05, 0.1, r2=0.02, seg=10)
    for k in range(arms):
        a = k * 2 * math.pi / arms + math.pi / 6; ca, sa = math.cos(a), math.sin(a)
        B.cyl('brass', (x + r * 0.5 * ca, y + r * 0.5 * sa, z - drop - 0.02), 0.011, r, axis='x', rot=(0, 0, math.degrees(a)), seg=6)
        gx, gy, gz = x + r * ca, y + r * sa, z - drop + 0.02
        B.cyl('brass', (gx, gy, gz - 0.02), 0.012, 0.06, seg=6); B.cyl('brass', (gx, gy, gz - 0.07), 0.04, 0.04, r2=0.065, seg=10)
        B.sphere('glow_gas', (gx, gy, gz - 0.17), 0.075, scale=(1, 1, 1.15)); B.cyl('brass', (gx, gy, gz - 0.3), 0.03, 0.03, r2=0.015, seg=8)
        point((gx, gy, gz - 0.17), watts=watts / arms, radius=0.1)
def gas_stand(B, loc, h=1.9, watts=120):
    """standing gas lamp (indoor gas standard): cast-iron foot, fluted post with brass collars, lantern with glass."""
    x, y, z = loc
    B.cyl('iron', (x, y, z + 0.06), 0.2, 0.12, r2=0.14, seg=18); B.cyl('iron', (x, y, z + 0.22), 0.1, 0.22, r2=0.06, seg=14)
    B.cyl('iron', (x, y, z + h * 0.5), 0.045, h * 0.72, seg=12); B.cyl('brass', (x, y, z + h * 0.35), 0.07, 0.05, seg=14); B.cyl('brass', (x, y, z + h * 0.62), 0.065, 0.05, seg=14)
    B.cyl('brass', (x, y, z + h - 0.28), 0.12, 0.06, r2=0.14, seg=16); B.sphere('glow_gas', (x, y, z + h - 0.12), 0.15, scale=(1, 1, 1.25))
    for k in range(4): a = k * math.pi / 2 + math.pi / 4; B.cyl('brass', (x + 0.15 * math.cos(a), y + 0.15 * math.sin(a), z + h - 0.12), 0.009, 0.36, seg=6)
    B.cyl('brass', (x, y, z + h + 0.1), 0.17, 0.05, r2=0.05, seg=16); B.sphere('brass', (x, y, z + h + 0.16), 0.045)
    point((x, y, z + h - 0.12), watts=watts, radius=0.12)
def street_lamp(B, loc, h=4.0, watts=900, rot=0):
    """Paris gas street lamp: fluted cast-iron column, ladder bar, lantern with 4 glass faces, crown."""
    x, y, z = loc
    with B.xf((x, y, z), (0, 0, rot)):
        B.cyl('iron', (0, 0, 0.14), 0.2, 0.28, r2=0.14, seg=14); B.cyl('iron', (0, 0, 0.5), 0.09, 0.5, r2=0.065, seg=12); B.cyl('iron', (0, 0, h * 0.5), 0.055, h - 0.8, seg=12)
        for zz in (0.9, 2.2): B.cyl('iron', (0, 0, zz), 0.09, 0.07, seg=12)
        B.box('iron', (0, 0, h - 0.62), (0.7, 0.04, 0.04)); B.cyl('brass', (0, 0, h - 0.5), 0.11, 0.08, r2=0.16, seg=12)
        B.cyl('iron', (0, 0, h - 0.3), 0.19, 0.05, r2=0.19, seg=8); B.cyl('glow_gas', (0, 0, h - 0.06), 0.17, 0.42, r2=0.2, seg=8, smooth=False)
        B.cyl('iron', (0, 0, h + 0.18), 0.21, 0.05, seg=8); B.cyl('iron', (0, 0, h + 0.3), 0.18, 0.2, r2=0.02, seg=8); B.sphere('brass', (0, 0, h + 0.44), 0.04)
        wp = B.wpt((0, 0, h - 0.06))
    point(wp, watts=watts, radius=0.2, name='street_lamp')

# ---------------------------------------------------------------- furniture & instruments
def table(B, c, size=(1.6, 0.8), h=0.85, mat='oak', rot=0, top='navy'):
    """writing table: board top (+ cloth), apron, 4 turned legs, stretcher, a drawer front."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box(mat, (0, 0, h - 0.03), (size[0], size[1], 0.06))
        if top: B.box(top, (0, 0, h + 0.004), (size[0] - 0.14, size[1] - 0.14, 0.008))
        B.box('walnut', (0, 0, h - 0.11), (size[0] - 0.12, size[1] - 0.12, 0.1)); B.box('brass', (0, -size[1] / 2 + 0.056, h - 0.11), (0.06, 0.008, 0.02))
        for sx in (-1, 1):
            for sy in (-1, 1):
                px, py = sx * (size[0] / 2 - 0.08), sy * (size[1] / 2 - 0.08); B.box('walnut', (px, py, (h - 0.06) / 2), (0.06, 0.06, h - 0.06)); B.cyl('walnut', (px, py, 0.16), 0.042, 0.1, seg=10)
        B.box('walnut', (0, 0, 0.2), (size[0] - 0.18, 0.035, 0.045))
def stool(B, c, h=0.62, rot=0, mat='leather'):
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.cyl(mat, (0, 0, h), 0.2, 0.06, seg=16); B.cyl('walnut', (0, 0, h - 0.06), 0.18, 0.05, seg=16)
        for k in range(3): a = k * 2 * math.pi / 3; B.cyl('walnut', (0.12 * math.cos(a), 0.12 * math.sin(a), h / 2 - 0.04), 0.022, h - 0.08, seg=8, rot=(8 * math.sin(a), -8 * math.cos(a), 0))
def bench(B, c, length=3.0, rot=0, h=0.46):
    """prisoners' bench: seat board, back rail, trestle ends and stretcher. local +y = the seat front."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('oak', (0, 0, h), (length, 0.42, 0.06)); B.box('oak', (0, -0.19, h + 0.32), (length, 0.04, 0.22)); B.box('oak', (0, -0.19, h + 0.62), (length, 0.04, 0.1))
        for px in (-length / 2 + 0.12, 0, length / 2 - 0.12):
            B.box('walnut', (px, 0, h / 2), (0.06, 0.36, h)); B.box('walnut', (px, -0.19, h + 0.2), (0.05, 0.05, 0.7))
        B.box('walnut', (0, 0.05, 0.18), (length - 0.2, 0.04, 0.04)); B.cyl('iron', (-length / 2 + 0.2, 0.0, h + 0.04), 0.03, 0.03, seg=8)
def measuring_chair(B, c, rot=0, head_z=1.32):
    """oak measuring chair on a low dais: seat, high back, arms, tall rear post with ticks + adjustable head rest (brass clamp + screw), foot rail.
    local +y = the sitter's front; head rest centre at z head_z."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('walnut', (0, 0.05, 0.05), (1.1, 1.1, 0.1)); B.box('oak', (0, 0, 0.48), (0.58, 0.52, 0.07)); B.box('leather', (0, 0, 0.53), (0.52, 0.46, 0.05))
        for sx in (-1, 1):
            for sy in (-1, 1): B.box('oak', (sx * 0.25, sy * 0.21, 0.26), (0.06, 0.06, 0.4)); B.cyl('walnut', (sx * 0.25, sy * 0.21, 0.18), 0.04, 0.08, seg=10)
        B.box('oak', (0, -0.04, 0.2), (0.5, 0.04, 0.05)); B.box('oak', (0, 0.32, 0.2), (0.62, 0.1, 0.04))
        B.box('oak', (0, -0.24, 0.98), (0.56, 0.05, 0.92)); B.box('oak', (0, -0.24, 1.46), (0.64, 0.06, 0.06))
        for sx in (-1, 1): B.box('oak', (sx * 0.31, -0.02, 0.74), (0.05, 0.5, 0.05)); B.box('oak', (sx * 0.31, 0.22, 0.63), (0.05, 0.05, 0.22)); B.box('brass', (sx * 0.31, 0.24, 0.76), (0.07, 0.07, 0.03))
        B.box('oak', (0, -0.32, 1.12), (0.12, 0.08, 2.0))
        for z in np.arange(0.3, 2.0, 0.1): B.box('brass', (0, -0.275, z), (0.05 if round(z * 10) % 5 else 0.09, 0.006, 0.01))
        B.box('brass', (0, -0.32, head_z), (0.2, 0.14, 0.07)); B.cyl('brass', (0.12, -0.32, head_z), 0.03, 0.06, axis='x', seg=10)
        B.box('oak', (0, -0.15, head_z), (0.05, 0.32, 0.05)); B.box('leather', (0, 0.02, head_z + 0.04), (0.22, 0.05, 0.3)); B.box('brass', (0, 0.02, head_z + 0.2), (0.24, 0.06, 0.02))
def toise(B, c, rot=0, z0=0.4, z1=2.3, slider=1.66):
    """wall height gauge (toise): oak board with greeked brass tick strips (no numbers) and a sliding brass head-block. local +y = out of the wall."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('oak', (0, 0.02, (z0 + z1) / 2), (0.24, 0.04, z1 - z0 + 0.12)); B.box('walnut', (0.0, 0.045, (z0 + z1) / 2), (0.04, 0.02, z1 - z0 + 0.06))
        for k, z in enumerate(np.arange(z0, z1, 0.05)):
            big = k % 10 == 0; mid = k % 5 == 0; B.box('brass', (-0.06, 0.044, z), (0.08 if big else 0.055 if mid else 0.03, 0.008, 0.012))
        B.box('brass', (0.0, 0.08, slider), (0.16, 0.08, 0.05)); B.box('walnut', (0.0, 0.24, slider), (0.14, 0.34, 0.025)); B.cyl('brass', (0.07, 0.08, slider), 0.02, 0.06, axis='y', seg=10)
        for zz in (z1 + 0.09, z0 - 0.09): B.box('walnut', (0, 0.04, zz), (0.3, 0.06, 0.06))
def arm_span_scale(B, c, rot=0, length=2.0, z=1.4):
    """arm-span scale: a long oak rail along the wall with brass ticks (no numbers), centre pointer and two end stops. local +y = out of wall."""
    with B.xf((c[0], c[1], z), (0, 0, rot)):
        B.box('oak', (0, 0.025, 0), (length + 0.2, 0.05, 0.1)); B.box('walnut', (0, 0.055, 0.03), (length + 0.2, 0.012, 0.02))
        for k, x in enumerate(np.arange(-length / 2, length / 2 + 1e-6, 0.05)): B.box('brass', (x, 0.056, -0.012), (0.01, 0.008, 0.07 if k % 10 == 0 else 0.045 if k % 5 == 0 else 0.028))
        for s in (-1, 1): B.box('brass', (s * (length / 2 + 0.05), 0.07, 0), (0.05, 0.07, 0.16))
        B.box('iron', (0, 0.07, 0.0), (0.022, 0.03, 0.2))
def foot_board(B, c, rot=0):
    """foot-measuring board: low oak plank with a heel stop and a sliding toe-block on a brass rule (greeked). local +y = toe direction."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('oak', (0, 0, 0.03), (0.34, 0.6, 0.06)); B.box('walnut', (0, -0.27, 0.11), (0.34, 0.05, 0.1)); B.box('brass', (0.14, 0.0, 0.066), (0.02, 0.5, 0.008))
        for k in range(10): B.box('iron', (0.115, -0.22 + k * 0.05, 0.068), (0.03 if k % 5 else 0.05, 0.007, 0.006))
        B.box('walnut', (0.0, 0.14, 0.11), (0.34, 0.05, 0.09)); B.cyl('brass', (0.2, 0.14, 0.1), 0.02, 0.04, axis='x', seg=8)
def sliding_calipers(B, c, rot=0, length=0.5, open_=0.18, tilt=(0, 0, 0), scale=1.0):
    """steel sliding (head) calipers: graduated beam, fixed jaw, sliding jaw, brass lock screw. beam along local x; jaws point to -y."""
    with B.xf((c[0], c[1], c[2]), (tilt[0], tilt[1], rot), scale):
        B.box('steel', (0, 0, 0.012), (length, 0.024, 0.024)); B.box('brass', (0, 0, 0.026), (length * 0.96, 0.008, 0.005))
        for k in range(int(length / 0.025)): B.box('iron', (-length / 2 + 0.02 + k * 0.025, -0.012, 0.026), (0.004, 0.01, 0.008 if k % 4 else 0.016))
        B.box('steel', (-length / 2 + 0.012, -0.045, 0.03), (0.024, 0.11, 0.07)); B.box('steel', (-length / 2 + 0.024, -0.11, 0.014), (0.034, 0.06, 0.034), rot=(0, 0, 25))
        sx = -length / 2 + 0.02 + open_; B.box('steel', (sx, -0.02, 0.012), (0.045, 0.055, 0.05)); B.box('steel', (sx, -0.1, 0.03), (0.024, 0.12, 0.07)); B.box('steel', (sx - 0.006, -0.16, 0.014), (0.034, 0.06, 0.034), rot=(0, 0, -25))
        B.cyl('brass', (sx, 0.018, 0.042), 0.016, 0.03, seg=10); B.cyl('brass', (sx, 0.018, 0.064), 0.02, 0.014, seg=10)
def spreading_calipers(B, c, rot=0, span=0.28, leg=0.4, tilt=(0, 0, 0), scale=1.0):
    """compass-style spreading calipers lying flat: pivot ring + two legs with curved tips (box segments), steel; opens toward local +y."""
    with B.xf(c, (tilt[0], tilt[1], rot), scale):
        B.cyl('brass', (0, 0, 0.02), 0.026, 0.018, seg=14); B.cyl('steel', (0, 0, 0.034), 0.013, 0.014, seg=10)
        for s in (-1, 1):
            a = math.atan2(span / 2, leg)
            for j, (f0, f1) in enumerate(((0.0, 0.58), (0.58, 1.0))):
                r_ = leg * 0.5 * (f0 + f1); ang = s * a * (1 if j == 0 else 0.4)
                B.box('steel', (s * math.sin(ang) * r_, math.cos(ang) * r_ * 0.95, 0.013), (0.018, leg * (f1 - f0) * 1.05, 0.014), rot=(0, 0, -math.degrees(ang)))
            B.sphere('steel', (s * span / 2 * 0.95, leg * 0.95, 0.015), 0.014)
def ledger_stack(B, c, n=5, rot=0, w=0.34, d=0.24, mats=('oxblood', 'baize', 'leather', 'navy', 'oxblood')):
    z = c[2]
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        for i in range(n):
            t = 0.045 + 0.02 * (i % 3); m = mats[i % len(mats)]; jx = B.rng.uniform(-0.02, 0.02); jr = B.rng.uniform(-6, 6)
            B.box(m, (jx, 0, z + t / 2), (w, d, t), rot=(0, 0, jr), tint=B.rng.uniform(0.85, 1.1)); B.box('cream', (jx, 0.0, z + t / 2), (w - 0.03, d + 0.008, t - 0.014), rot=(0, 0, jr))
            B.box('brass', (jx - w / 2 + 0.01, 0, z + t / 2), (0.014, d * 0.95, t + 0.004), rot=(0, 0, jr)); z += t
        B.box('brass', (0, 0, z + 0.004), (0.06, 0.04, 0.004))
def open_ledger(B, c, rot=0, w=0.34, d=0.25):
    with B.xf(c, (0, 0, rot)):
        B.box('oxblood', (0, 0, 0.012), (w * 2 + 0.03, d + 0.02, 0.024)); B.box('cream', (-w / 2, 0, 0.04), (w - 0.01, d - 0.01, 0.036), rot=(0, 3, 0)); B.box('cream', (w / 2, 0, 0.04), (w - 0.01, d - 0.01, 0.036), rot=(0, -3, 0))
        for k in range(7):
            B.box('dark', (-w / 2, d / 2 - 0.03 - k * 0.03, 0.06), (w * 0.8 * (1 - 0.3 * (k % 3) / 3), 0.006, 0.002), rot=(0, 3, 0)); B.box('dark', (w / 2, d / 2 - 0.03 - k * 0.03, 0.06), (w * 0.7, 0.006, 0.002), rot=(0, -3, 0))
def inkpot(B, c, quill=True, rot=0):
    x, y, z = c; B.cyl('glass', (x, y, z + 0.03), 0.04, 0.06, seg=14); B.cyl('ink', (x, y, z + 0.032), 0.034, 0.058, seg=12); B.cyl('brass', (x, y, z + 0.07), 0.03, 0.02, seg=12)
    if quill:
        with B.xf((x, y, z + 0.09), (0, 0, rot)): B.cyl('cream', (0.1, 0, 0.13), 0.005, 0.3, rot=(0, 70, 0), seg=6); B.box('cream', (0.17, 0, 0.17), (0.16, 0.03, 0.003), rot=(0, 70, 0))
def kepi(B, c, rot=0, tilt=(0, 0, 0)):
    with B.xf(c, (tilt[0], tilt[1], rot)):
        B.cyl('oxblood', (0, 0, 0.065), 0.09, 0.13, r2=0.105, seg=16); B.cyl('navy', (0, 0, 0.024), 0.093, 0.048, seg=16); B.cyl('oxblood', (0, 0, 0.134), 0.115, 0.014, seg=16)
        B.box('leather', (0.1, 0, 0.012), (0.1, 0.16, 0.01), rot=(0, 10, 0)); B.cyl('brass', (0.098, 0, 0.07), 0.02, 0.01, axis='x', seg=8)
def coat_rack(B, c, rot=0, h=1.95, kepis=3):
    """standing coat rack: foot, post, four brass hooks with kepis, a hanging coat."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.cyl('walnut', (0, 0, 0.05), 0.26, 0.1, r2=0.18, seg=16); B.cyl('walnut', (0, 0, h / 2), 0.045, h, seg=10); B.sphere('brass', (0, 0, h + 0.04), 0.06)
        for k in range(4):
            a = k * 90 + 45; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            B.cyl('brass', (0.12 * ca, 0.12 * sa, h - 0.18), 0.014, 0.26, axis='x', rot=(0, 0, a), seg=6); B.sphere('brass', (0.25 * ca, 0.25 * sa, h - 0.18), 0.024)
        for k in range(kepis):
            a = k * 90 + 45 + (180 if k == 2 else 0); ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a)); kepi(B, (0.25 * ca, 0.25 * sa, h - 0.27), rot=a + 90)
        B.cyl('navy', (0.0, 0.22, h - 0.55), 0.15, 0.9, r2=0.22, seg=12, rot=(10, 0, 0))
def stove(B, c, rot=0, pipe_to=3.6):
    """coal stove: cast-iron drum on a plinth, door with mica glow, brass rail, coal scuttle, stove pipe with elbow to the ceiling. returns the smoke mouth (world)."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('iron', (0, 0, 0.12), (0.62, 0.52, 0.24)); B.cyl('iron', (0, 0, 0.6), 0.28, 0.72, seg=16); B.cyl('iron', (0, 0, 0.99), 0.31, 0.07, seg=16); B.cyl('iron', (0, 0, 1.06), 0.22, 0.07, seg=16)
        B.box('brass', (0, 0.29, 0.5), (0.2, 0.025, 0.22)); B.box('glow_door', (0, 0.305, 0.5), (0.13, 0.01, 0.13)); B.cyl('brass', (0.17, 0.31, 0.52), 0.014, 0.05, axis='y', seg=8)
        B.cyl('brass', (0, 0.0, 0.33), 0.33, 0.025, seg=16); B.cyl('iron', (0, 0, 1.45), 0.07, 0.74, seg=10)
        B.cyl('iron', (0, 0, 2.0), 0.07, 0.5, seg=10); B.cyl('iron', (0, 0, 2.5), 0.075, 0.6, seg=10)
        B.cyl('iron', (0, 0, 0.1), 0.0001, 0.0001, seg=3) if False else None
        mouth = B.wpt((0, 0, pipe_to - 0.3))
        B.cyl('iron', (0.28, 0.1, 0.18), 0.17, 0.24, r2=0.15, seg=12); B.box('iron', (0.28, 0.1, 0.32), (0.22, 0.02, 0.02))       # scuttle
    point(B.wpt((0, 0.45, 0.5)), color=(1.0, 0.55, 0.25), watts=18, radius=0.06, name='stove_glow')
    return mouth
def wall_clock(B, c, rot=0, r=0.28):
    """wall clock without numerals: round case, ring of dots, two hands. local +y = out of the wall. also a regulator case below (pendulum added separately)."""
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        B.cyl('walnut', (0, 0.04, 0), r + 0.05, 0.08, axis='y', seg=24); B.cyl('cream', (0, 0.09, 0), r, 0.02, axis='y', seg=24); B.cyl('brass', (0, 0.1, 0), r + 0.02, 0.012, r2=r + 0.02, axis='y', seg=24) if False else None
        for k in range(12):
            a = k * math.pi / 6; B.sphere('iron', (r * 0.82 * math.sin(a), 0.108, r * 0.82 * math.cos(a)), 0.016 if k % 3 else 0.026, seg=8, rings=5)
        B.box('iron', (0.0, 0.112, r * 0.28), (0.022, 0.008, r * 0.62)); B.box('iron', (r * 0.2, 0.112, r * 0.12), (r * 0.5, 0.008, 0.02), rot=(0, -30, 0)); B.cyl('brass', (0, 0.115, 0), 0.026, 0.016, axis='y', seg=10)
def pendulum_case(B, c, rot=0, h=0.9, w=0.2):
    """slim case under the clock with a glazed slot (the pendulum itself is animated: see add_pendulum)."""
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        B.box('walnut', (0, 0.07, -h / 2), (w, 0.12, h)); B.box('dark', (0, 0.135, -h / 2), (w - 0.07, 0.01, h - 0.1)); B.box('brass', (0, 0.14, -h - 0.02), (w, 0.14, 0.04))
def ledger_shelf(B, c, length=1.8, rot=0, n=2):
    """wall shelf with leather ledgers standing in a row, brass shelf brackets."""
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        for r_ in range(n):
            z = r_ * 0.42; B.box('oak', (0, 0.16, z), (length, 0.3, 0.04))
            for sx in np.arange(-length / 2 + 0.05, length / 2 - 0.1, 0.5): B.box('iron', (sx, 0.04, z - 0.07), (0.03, 0.06, 0.12))
            x = -length / 2 + 0.07
            while x < length / 2 - 0.12:
                w = B.rng.uniform(0.045, 0.085); hh = B.rng.uniform(0.24, 0.34); m = ['oxblood', 'baize', 'leather', 'navy', 'leather'][B.rng.randint(0, 4)]
                B.box(m, (x + w / 2, 0.17, z + 0.02 + hh / 2), (w, 0.22, hh), tint=B.rng.uniform(0.85, 1.1)); B.box('brass', (x + w / 2, 0.285, z + 0.02 + hh * 0.7), (w - 0.012, 0.006, 0.025)); x += w + 0.008
def frame_on_wall(B, name, c, size, rot=0, tilt=0.0):
    """picture / notice frame: oak frame + a card plane (separate object with texture) placed by add_cards after finalize; c on the wall, local +y out."""
    B.box('walnut', (c[0], c[1], c[2]), (size[0] + 0.08, 0.04, size[1] + 0.08), rot=(0, 0, rot))
    B.box('cream', (c[0], c[1], c[2]), (size[0] + 0.01, 0.046, size[1] + 0.01), rot=(0, 0, rot), tint=0.9)
    STATE.setdefault('wall_cards', []).append((name, c, size, rot))
def crate(B, c, size=(0.5, 0.4, 0.35), rot=0, lid=True):
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        B.box('oak', (0, 0, size[2] / 2), size); 
        for sx in (-1, 1): B.box('walnut', (sx * size[0] / 2, 0, size[2] / 2), (0.03, size[1] + 0.012, size[2] + 0.012))
        B.box('walnut', (0, 0, size[2] / 2), (size[0] + 0.012, 0.03, size[2] + 0.012)); B.box('brass', (0, -size[1] / 2 - 0.01, size[2] * 0.7), (0.07, 0.01, 0.035))
def bucket(B, c, r=0.15, h=0.3):
    B.cyl('iron', (c[0], c[1], c[2] + h / 2), r, h, r2=r * 1.15, seg=14); B.cyl('dark', (c[0], c[1], c[2] + h + 0.004), r * 1.1, 0.01, seg=14)
    B.cyl('iron', (c[0], c[1], c[2] + h * 0.5), r * 1.18, 0.02, seg=14) 
def umbrella_stand(B, c):
    x, y, z = c; B.cyl('walnut', (x, y, z + 0.3), 0.15, 0.6, r2=0.18, seg=14); B.cyl('brass', (x, y, z + 0.5), 0.17, 0.03, seg=14)
    for k, (dx, dy, tl) in enumerate(((0.05, 0.02, 6), (-0.05, 0.04, -8), (0.0, -0.05, 3))): B.cyl('leather', (x + dx, y + dy, z + 0.85), 0.018, 0.9, seg=6, rot=(tl, -tl, 0)); B.sphere('brass', (x + dx * 1.5, y + dy * 1.2, z + 1.31), 0.03)
def wastebin(B, c):
    B.cyl('iron', (c[0], c[1], c[2] + 0.2), 0.14, 0.4, r2=0.17, seg=12); B.cyl('dark', (c[0], c[1], c[2] + 0.405), 0.15, 0.01, seg=12)
    for k in range(3): B.box('cream', (c[0] + 0.02 * k, c[1] - 0.02 * k, c[2] + 0.43 + 0.02 * k), (0.12, 0.09, 0.01), rot=(10 * k, 5, 25 * k))
def door(B, c, rot=0, w=1.1, h=2.25, ajar=0.0, glow=True):
    """door in a wall opening: frame + leaf with panels + brass handle; ajar = swing in degrees; a lit corridor glow behind. local +y = into the room, c = floor centre of the opening."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        for sx in (-1, 1): B.box('walnut', (sx * (w / 2 + 0.07), 0, h / 2), (0.14, 0.3, h + 0.0))
        B.box('walnut', (0, 0, h + 0.07), (w + 0.28, 0.3, 0.14)); B.box('walnut', (0, 0.0, h + 0.22), (w + 0.5, 0.34, 0.1))
        if glow: B.box('glow_door', (0, -0.55, h / 2), (w, 0.02, h))
        with B.xf((-w / 2, 0.02, 0), (0, 0, ajar)):
            B.box('oak', (w / 2, 0, h / 2), (w - 0.02, 0.05, h - 0.02))
            for pz in (0.62, 1.62):
                for px in (0.3, 0.8):
                    if px < w - 0.2: B.box('walnut', (px * w / 1.1, 0.03, pz), (0.3 * w / 1.1, 0.02, 0.62 if pz < 1 else 0.55))
            B.cyl('brass', (w - 0.1, 0.05, 1.0), 0.03, 0.05, axis='y', seg=10); B.box('brass', (w - 0.1, 0.07, 1.0), (0.1, 0.02, 0.03))
def barred_window(B, x, ya, yb, za, zb, bars=6, side=-1):
    """window in the wall at x (side -1 = left wall facing +x): frame, mullion, iron bars, sill; the glass pane glows in 'glow' sky from the dome."""
    xc = x - side * 0.0; yc = (ya + yb) / 2; wy = yb - ya
    B.box('walnut', (x + 0.1, yc, za - 0.05), (0.34, wy + 0.24, 0.1)); B.box('walnut', (x + 0.06, yc, zb + 0.05), (0.2, wy + 0.2, 0.1))
    for yy in (ya - 0.05, yb + 0.05): B.box('walnut', (x + 0.06, yy, (za + zb) / 2), (0.2, 0.1, zb - za))
    B.box('walnut', (x + 0.05, yc, (za + zb) / 2), (0.06, 0.06, zb - za))
    for i in range(bars): yy = ya + wy * (i + 0.5) / bars; B.cyl('iron', (x + 0.1, yy, (za + zb) / 2), 0.02, zb - za, seg=8)
    for zz in (za + (zb - za) * 0.4, za + (zb - za) * 0.75): B.box('iron', (x + 0.1, yc, zz), (0.03, wy, 0.03))
    B.box('walnut', (x + 0.02, yc, (za + zb) / 2), (0.04, 0.05, zb - za) ) if False else None

# ---------------------------------------------------------------- outside Paris: mansard roofs and chimneys
def mansard(B, c, w, d, h_wall, h_roof=2.2, rot=0, chimneys=2, seed=1, stone='stone', lit=0.0, dormers=True):
    """Haussmann block: stone body (floors with windows), a two-pitch mansard roof in zinc, dormer windows, terracotta chimney stacks.
    c = floor centre, local x along the front, +y = deep. windows are dark glass; `lit` is the share that glows warm."""
    r = random.Random(seed)
    with B.xf((c[0], c[1], c[2]), (0, 0, rot)):
        B.box(stone, (0, 0, h_wall / 2), (w, d, h_wall))
        B.box('stone_dk', (0, 0, h_wall + 0.1), (w + 0.3, d + 0.3, 0.2)); B.box('stone_dk', (0, 0, h_wall - 0.15), (w + 0.12, d + 0.12, 0.12))
        nfl = max(2, int(h_wall / 3.0)); nw = max(2, int(w / 2.4))
        for fl in range(nfl):
            z = 1.6 + fl * 3.0
            if z > h_wall - 0.8: break
            for k in range(nw):
                x = (k + 0.5) * w / nw - w / 2; on = r.random() < lit
                B.box('glow_win' if on else 'dark', (x, -d / 2 - 0.01, z), (0.85, 0.04, 1.5)); B.box('stone_dk', (x, -d / 2 - 0.02, z + 0.84), (1.05, 0.06, 0.12)); B.box('stone_dk', (x, -d / 2 - 0.03, z - 0.82), (1.1, 0.12, 0.1))
                if fl == 1 or fl == nfl - 1: B.box('iron', (x, -d / 2 - 0.2, z - 0.5), (1.2, 0.03, 0.9)); B.box('iron', (x, -d / 2 - 0.1, z - 0.96), (1.3, 0.22, 0.04))
        hr = h_roof; B.box('zinc', (0, 0, h_wall + 0.2 + hr * 0.3), (w - 0.2, d - 0.2, hr * 0.6))
        B.prism_roof('zinc', (0, 0, h_wall + 0.2 + hr * 0.6), w - 0.2, d - 0.2, hr * 0.4, ridge_frac=0.78)
        if dormers:
            for k in range(nw):
                x = (k + 0.5) * w / nw - w / 2; on = r.random() < lit
                B.box('stone_dk', (x, -d / 2 + 0.05, h_wall + 0.2 + hr * 0.3), (0.8, 0.5, 1.0)); B.box('glow_win' if on else 'dark', (x, -d / 2 - 0.2, h_wall + 0.2 + hr * 0.3), (0.5, 0.03, 0.7))
                B.prism_roof('zinc', (x, -d / 2 + 0.1, h_wall + 0.2 + hr * 0.3 + 0.5), 0.9, 0.7, 0.3, rot_z=90)
        for i in range(chimneys):
            cx = r.uniform(-w * 0.35, w * 0.35); cy = r.uniform(-d * 0.15, d * 0.15); chim(B, (cx, cy, h_wall + 0.2 + hr * 0.95), r)
def chim(B, p, r=None):
    """chimney stack: terracotta shaft, stone cap, two pots."""
    x, y, z = p; B.box('terracotta', (x, y, z + 0.8), (0.7, 0.5, 1.6)); B.box('stone_dk', (x, y, z + 1.65), (0.8, 0.6, 0.1))
    for dx in (-0.15, 0.15): B.cyl('terracotta', (x + dx, y, z + 1.95), 0.1, 0.5, r2=0.085, seg=10)
def paris_roofs(B0, x0, y0, y1, side=-1, depth=12.0, seed=2, count=6, base_z=-3.0):
    """a row of mansard blocks outside a window (side -1: to the left, -x), at distance `depth` from x0 — seen through windows."""
    B = getattr(B0, 'out', B0); r = random.Random(seed)
    for i in range(count):
        yy = y0 + (y1 - y0) * (i + 0.5) / count + r.uniform(-1, 1); w = r.uniform(7, 10); hw = r.uniform(11, 16) + base_z
        mansard(B, (x0 + side * (depth + r.uniform(0, 5)), yy, base_z), w, r.uniform(6, 9), hw, h_roof=r.uniform(2.2, 3.0), rot=90 * (-side), chimneys=2, seed=seed + i, lit=0.0, dormers=False)

# ---------------------------------------------------------------- card cabinets, drawers, ladder, desk props
CELL = (0.30, 0.20)
def cabinet_wall(B, origin, length, height, depth=0.55, rot_z=0, seed=9, reserve=(), bay=5, cornice=True, pilasters=True, dark_cells=True):
    """wall of wooden card cabinets. local frame: x along the wall, y toward the aisle (front face at y = depth), z up.
    plinth, carcass, cornice, pilaster every `bay` columns (1.5 m), rails, and drawers (front, brass label frame with a BLANK cream card, brass pull).
    `reserve` = [(col, row)] cells left empty (an animated drawer goes there; a dark recess is drawn). returns {'cell': fn(col,row)->(x,z) local, 'face': depth}."""
    r = random.Random(seed); cw, ch = CELL; nc = int(length / cw); nr = int((height - 0.2) / ch); z0 = 0.2
    with B.xf(origin, (0, 0, rot_z)):
        B.box('walnut', (length / 2, depth / 2 - 0.02, height / 2), (length, depth, height), tint=0.88)
        B.box('walnut', (length / 2, depth / 2 + 0.05, 0.1), (length + 0.06, depth + 0.1, 0.2), tint=0.8)                       # plinth
        if cornice:
            B.box('walnut', (length / 2, depth / 2 + 0.06, height + 0.09), (length + 0.1, depth + 0.16, 0.18)); B.box('walnut', (length / 2, depth / 2 + 0.1, height + 0.2), (length + 0.14, depth + 0.26, 0.06), tint=0.9)
            B.box('brass', (length / 2, depth + 0.1, height + 0.03), (length, 0.02, 0.03))
        if pilasters:
            for i in range(int(length / (cw * bay)) + 1):
                px = i * cw * bay; B.box('walnut', (px, depth + 0.03, height / 2), (0.12, 0.08, height), tint=0.8); B.box('walnut', (px, depth + 0.07, height - 0.08), (0.16, 0.05, 0.12)); B.box('walnut', (px, depth + 0.07, 0.24), (0.16, 0.05, 0.1))
        for rr in range(0, nr + 1, 7): B.box('walnut', (length / 2, depth + 0.012, z0 + rr * ch), (length, 0.04, 0.035), tint=0.8)
        res = set(reserve)
        for cc in range(nc):
            for rr in range(nr):
                x = (cc + 0.5) * cw; z = z0 + (rr + 0.5) * ch
                if (cc % bay) == 0 and pilasters: pass
                if (cc, rr) in res:
                    if dark_cells: B.box('dark', (x, depth + 0.006, z), (cw - 0.012, 0.004, ch - 0.012))
                    continue
                t = r.uniform(0.82, 1.12); tint = (t, t * r.uniform(0.94, 1.0), t * r.uniform(0.9, 1.0))
                B.box('honey', (x, depth + 0.018, z), (cw - 0.022, 0.036, ch - 0.02), tint=tint)
                B.box('brass', (x, depth + 0.04, z + ch * 0.17), (0.12, 0.006, 0.05)); B.box('cream', (x, depth + 0.044, z + ch * 0.17), (0.1, 0.004, 0.036), tint=r.uniform(0.9, 1.05))
                B.box('brass', (x, depth + 0.05, z - ch * 0.22), (0.07, 0.016, 0.014))
    return dict(face=depth, nc=nc, nr=nr, z0=z0, cell=lambda c, rw: ((c + 0.5) * cw, z0 + (rw + 0.5) * ch))

def _cards_in_drawer(B, w, depth, h, n, r, tilt=-8, tabs=True, ycard0=-0.05, gap=None):
    """standing cards in a drawer body: local y runs out of the cabinet; cards stack from the back (-depth) to the front."""
    gap = gap or (depth - 0.12) / max(n, 1); ch = h * 0.78
    for i in range(n):
        y = -depth + 0.06 + i * gap; t = r.uniform(0.9, 1.06)
        B.box('cream', (0, y, -h / 2 + 0.02 + ch / 2), (w - 0.05, 0.004, ch), rot=(tilt + r.uniform(-1.5, 1.5), 0, 0), tint=(t, t * 0.97, t * 0.88))
        if tabs and i % 4 == 0: B.box(['oxblood', 'baize', 'navy', 'oxblood'][(i // 4) % 4], (-w * 0.25 + (i // 4 % 3) * w * 0.22, y - 0.012, -h / 2 + 0.02 + ch + 0.012), (w * 0.2, 0.005, 0.026), rot=(tilt, 0, 0))
def drawer_assembly(name, pos, rot_z, w=0.27, h=0.18, depth=0.5, travel=0.4, open_=0.0, cards=14, boxes=0, seed=3, front_mat='honey', tabs=True):
    """one animated card drawer. root empty at `pos` = centre of the CLOSED drawer front (the cabinet face), local +y out of the cabinet; a 'slide' empty
    child carries the drawer and moves 0 .. travel along +y with set_drawer(name, open)."""
    r = random.Random(seed); root = bpy.data.objects.new(name + '_root', None); bpy.context.scene.collection.objects.link(root); root.location = pos; root.rotation_euler = (0, 0, math.radians(rot_z))
    slide = bpy.data.objects.new(name + '_slide', None); bpy.context.scene.collection.objects.link(slide); slide.parent = root; slide.location = (0, open_ * travel, 0)
    B = Batch(seed); t = r.uniform(0.95, 1.05)
    B.box(front_mat, (0, 0.018, 0), (w - 0.022, 0.036, h - 0.02), tint=t); B.box('brass', (0, 0.04, h * 0.17), (0.12 if w < 0.5 else 0.2, 0.006, 0.05)); B.box('cream', (0, 0.044, h * 0.17), (0.1 if w < 0.5 else 0.18, 0.004, 0.036))
    B.box('brass', (0, 0.05, -h * 0.22), (0.07 if w < 0.5 else 0.14, 0.016, 0.014))
    B.box('walnut', (-(w - 0.04) / 2, -depth / 2, 0), (0.012, depth, h - 0.03)); B.box('walnut', ((w - 0.04) / 2, -depth / 2, 0), (0.012, depth, h - 0.03))
    B.box('walnut', (0, -depth / 2, -(h - 0.03) / 2 + 0.006), (w - 0.04, depth, 0.012)); B.box('walnut', (0, -depth, 0), (w - 0.04, 0.012, h - 0.03))
    B.box('dark', (0, -depth / 2, -(h - 0.03) / 2 + 0.013), (w - 0.06, depth - 0.02, 0.004))
    _cards_in_drawer(B, w - 0.02, depth, h - 0.03, cards, r, tabs=tabs)
    objs = B.finalize(name, parent=slide, ink_t=STATE['ink_t'] * 0.8)
    STATE['anim'][name] = dict(kind='drawer', root=root, slide=slide, travel=travel, objs=objs); return slide
def card_box(name, pos, rot_z=0, w=0.3, d=0.2, h=0.17, lid=0.0, cards=9, seed=4, parent=None):
    """small wooden card box (hinged lid, brass clasp + blank label); `lid` 0..1 opens the lid (hinge at the back). animated: set_box_lid(name, o)."""
    r = random.Random(seed); root = bpy.data.objects.new(name + '_root', None); bpy.context.scene.collection.objects.link(root); root.location = pos; root.rotation_euler = (0, 0, math.radians(rot_z))
    if parent is not None: root.parent = parent
    B = Batch(seed); B.box('oak', (0, 0, h / 2), (w, d, h)); B.box('walnut', (0, 0, h + 0.003), (w + 0.004, d + 0.004, 0.006)) if False else None
    B.box('dark', (0, 0, h - 0.004), (w - 0.03, d - 0.03, 0.01))
    for i in range(cards):
        y = -d / 2 + 0.03 + i * (d - 0.06) / cards; B.box('cream', (0, y, h * 0.35 + h * 0.22), (w - 0.04, 0.004, h * 0.8), rot=(-6, 0, 0), tint=r.uniform(0.92, 1.05))
        if i % 3 == 0: B.box(['oxblood', 'baize', 'navy'][i // 3 % 3], (-w * 0.2 + (i // 3) * w * 0.15, y - 0.01, h * 0.35 + h * 0.62 + 0.01), (w * 0.14, 0.005, 0.022), rot=(-6, 0, 0))
    B.box('brass', (0, d / 2 + 0.006, h * 0.55), (0.1, 0.008, 0.04)); B.box('cream', (0, d / 2 + 0.011, h * 0.55), (0.082, 0.004, 0.028))
    objs = B.finalize(name, parent=root, ink_t=STATE['ink_t'] * 0.8)
    hinge = bpy.data.objects.new(name + '_hinge', None); bpy.context.scene.collection.objects.link(hinge); hinge.parent = root; hinge.location = (0, -d / 2, h)
    hinge.rotation_euler = (math.radians(-110 * lid), 0, 0)
    L = Batch(seed); L.box('oak', (0, d / 2, 0.012), (w + 0.01, d + 0.01, 0.024)); L.box('walnut', (0, d / 2, 0.028), (w - 0.04, d - 0.04, 0.012)); L.box('brass', (0, d + 0.006, -0.012), (0.06, 0.008, 0.04))
    objs += L.finalize(name + '_lid', parent=hinge, ink_t=STATE['ink_t'] * 0.8)
    STATE['anim'][name] = dict(kind='box', root=root, hinge=hinge, objs=objs); return root
def rolling_ladder(B, base, top, width=0.46, rungs=14):
    """library ladder leaning from a floor point to a rail point (world), with brass rail wheels on top and rubber feet."""
    b = np.array(base, float); t = np.array(top, float); v = t - b; Ln = np.linalg.norm(v); d = v / Ln; ax = np.cross(d, [0, 0, 1]); ax /= np.linalg.norm(ax); az = math.degrees(math.atan2(ax[1], ax[0]))
    for s in (-1, 1): B.box('honey', tuple((b + t) / 2 + ax * s * width / 2), (0.05, 0.035, Ln), rot=euler_to_z(d), tint=0.92)
    for k in range(rungs):
        p = b + d * (0.25 + k * (Ln - 0.45) / (rungs - 1)); B.cyl('walnut', tuple(p), 0.017, width, axis='x', rot=(0, 0, az), seg=8)
    for s in (-1, 1):
        B.cyl('brass', tuple(t + ax * s * width / 2 + np.array([0, 0, 0.0])), 0.05, 0.035, axis='x', rot=(0, 0, az), seg=12); B.box('iron', tuple(b + ax * s * width / 2 + np.array([0, 0, 0.02])), (0.06, 0.05, 0.04))
def banker_lamp(B, c, rot=0, watts=60, color=(1.0, 0.8, 0.5)):
    """brass banker's lamp with a deep green glass shade; green-gold glow + warm point light."""
    x, y, z = c
    with B.xf((x, y, z), (0, 0, rot)):
        B.cyl('brass', (0, 0, 0.017), 0.095, 0.034, r2=0.07, seg=16); B.cyl('brass', (0, 0, 0.17), 0.017, 0.28, seg=10); B.sphere('brass', (0, 0, 0.31), 0.032)
        B.cyl('brass', (0.05, 0, 0.34), 0.02, 0.06, seg=8); B.cyl('baize', (0.07, 0, 0.375), 0.1, 0.18, axis='y', seg=18); B.box('glow_green', (0.07, 0, 0.345), (0.2, 0.16, 0.012))
        wp = B.wpt((0.07, 0.0, 0.32))
    point(wp, color=color, watts=watts, radius=0.07, name='banker')
def fan_cards_static(B, c, n=9, spread=70, r=0.12, rot=0, w=0.15, d=0.1):
    with B.xf(c, (0, 0, rot)):
        for i in range(n):
            a = -spread / 2 + spread * i / (n - 1); B.box('cream', (r * 0.4 * math.cos(math.radians(a + 90)), r * 0.4 * math.sin(math.radians(a + 90)), 0.002 + 0.004 * i), (d, w, 0.003), rot=(0, 0, a), tint=B.rng.uniform(0.93, 1.04))
def cards_fan_objects(name, pos, n=9, w=0.15, d=0.1, rot=0, spread=80):
    """cards on a desk that can fan out: each card is its own object, pivot at the lower end; set_cards_fan(t) 0 = squared stack, 1 = fanned."""
    root = bpy.data.objects.new(name + '_root', None); bpy.context.scene.collection.objects.link(root); root.location = pos; root.rotation_euler = (0, 0, math.radians(rot)); cards = []
    r = random.Random(8)
    for i in range(n):
        piv = bpy.data.objects.new('%s_c%d' % (name, i), None); bpy.context.scene.collection.objects.link(piv); piv.parent = root; piv.location = (0, 0, 0.003 * i)
        B = Batch(i); B.box('cream', (0, d / 2 - 0.01, 0.0015), (w, d, 0.003), tint=r.uniform(0.94, 1.04))
        if i % 3 == 0: B.box(['oxblood', 'baize', 'navy'][i // 3 % 3], (w * 0.35, d - 0.012, 0.004), (w * 0.2, 0.018, 0.002))
        B.finalize('%s_c%d' % (name, i), parent=piv, ink=False); cards.append(piv)
    STATE['anim'][name] = dict(kind='fan', root=root, cards=cards, spread=spread, n=n); return root
def police_wagon(B, c, rot=0):
    """Black Maria prison van: dark navy boxy body on 4 wheels, red cornice line, 2 barred slit windows, rear door + step, driver's box with lantern, shafts (no horse)."""
    with B.xf((c[0], c[1], 0), (0, 0, rot)):
        B.box('wagon', (0, 0, 1.45), (1.75, 3.5, 1.7), tint=0.95); B.box('wagon', (0, 0, 2.38), (1.85, 3.6, 0.16)); B.prism_roof('wagon', (0, 0, 2.46), 1.85, 3.6, 0.3, rot_z=90, ridge_frac=1.0) if False else None
        B.box('wagon_red', (0, 0, 2.5), (1.9, 3.65, 0.07)); B.box('wagon_red', (0, 0, 0.62), (1.82, 3.55, 0.07))
        for sx in (-1, 1):
            for yy in (-0.7, 0.9):
                B.box('dark', (sx * 0.88, yy, 1.8), (0.02, 0.6, 0.28))
                for k in range(4): B.cyl('iron', (sx * 0.895, yy - 0.22 + k * 0.145, 1.8), 0.012, 0.3, seg=6)
        B.box('wagon', (0, -1.9, 1.45), (1.2, 0.2, 1.5)); B.box('dark', (0, -2.0, 1.5), (0.5, 0.02, 0.6)); B.box('brass', (0.4, -2.03, 1.3), (0.06, 0.03, 0.2))
        B.box('iron', (0, -2.1, 0.55), (0.9, 0.3, 0.06)); B.box('iron', (0, 1.55, 2.58), (1.2, 0.8, 0.5)) if False else None
        B.box('wagon', (0, 1.55, 2.0), (1.6, 0.9, 0.12)); B.box('leather', (0, 1.7, 2.12), (1.2, 0.4, 0.2)); B.box('wagon', (0, 1.95, 2.45), (1.5, 0.08, 0.8))       # driver's box + seat back
        for sx in (-1, 1):
            B.box('iron', (sx * 0.4, 2.7, 0.95), (0.06, 2.0, 0.06)); B.box('iron', (sx * 0.4, 3.7, 1.0), (0.1, 0.1, 0.1))                                            # shafts
            for (yy, rr) in ((-1.15, 0.52), (1.1, 0.62)):
                B.cyl('wagon_red', (sx * 0.98, yy, rr), rr, 0.1, axis='x', seg=24); B.cyl('iron', (sx * 0.98, yy, rr), rr * 0.9, 0.12, axis='x', seg=24) if False else None
                B.cyl('brass', (sx * 1.04, yy, rr), 0.07, 0.08, axis='x', seg=10)
                for k in range(8): a = k * 22.5; B.box('iron', (sx * 1.03, yy, rr), (0.04, 0.03, rr * 1.8), rot=(a, 0, 0))
        B.cyl('iron', (0, -1.15, 0.52), 0.045, 2.0, axis='x', seg=8); B.cyl('iron', (0, 1.1, 0.62), 0.045, 2.0, axis='x', seg=8)
        B.cyl('brass', (-0.9, 1.9, 2.25), 0.07, 0.25, seg=8); B.sphere('glow_gas', (-0.9, 1.9, 2.45), 0.1)                                                       # lantern
        wp = B.wpt((-0.9, 1.9, 2.45))
    point(wp, watts=60, radius=0.1, name='wagon_lamp')
def puddles(B, items):
    for (x, y, rx, ry, rot) in items:
        seg = 20; a = np.linspace(0, 2 * math.pi, seg, endpoint=False); rr = 1 + 0.18 * np.sin(a * 3 + x) + 0.1 * np.sin(a * 5 + y)
        v = [(0, 0, 0.006)] + [(rx * rr[i] * math.cos(a[i]), ry * rr[i] * math.sin(a[i]), 0.006) for i in range(seg)]
        with B.xf((x, y, 0), (0, 0, rot)): B.mesh('puddle', v, [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)], smooth=False)
def light_shaft(B, corners, direction, z_end=0.0):
    """additive light shaft: the opening's 4 corners (world, in order) projected along `direction` onto z = z_end; 4 side faces, camera rays only."""
    d = np.array(direction, float); d /= np.linalg.norm(d); top = [np.array(c, float) for c in corners]
    bot = [c + d * ((c[2] - z_end) / -d[2]) for c in top]
    for i in range(4):
        j = (i + 1) % 4; B.quad('beam_fx', tuple(top[i]), tuple(top[j]), tuple(bot[j]), tuple(bot[i]))
    return bot
def wall_box(B, mat, axis, pos, a0, a1, z0, z1, holes=(), out=-1, t=0.3, tint=1.0):
    """a wall plane at `axis`=pos (axis 'x': spans y a0..a1; axis 'y': spans x a0..a1), thickness t toward `out` (+1/-1), z z0..z1, rectangular holes
    [(h_a0, h_a1, h_z0, h_z1)] (non-overlapping). boxes only."""
    cuts = sorted(set([a0, a1] + [h[0] for h in holes] + [h[1] for h in holes]))
    for ca, cb in zip(cuts[:-1], cuts[1:]):
        if cb - ca < 1e-6: continue
        mid = (ca + cb) / 2; hs = [h for h in holes if h[0] <= mid <= h[1]]; spans = [(z0, z1)]
        if hs: h = hs[0]; spans = [s for s in ((z0, h[2]), (h[3], z1)) if s[1] - s[0] > 1e-6]
        for (za, zb) in spans:
            c = (pos + out * t / 2, (ca + cb) / 2, (za + zb) / 2) if axis == 'x' else ((ca + cb) / 2, pos + out * t / 2, (za + zb) / 2)
            sz = (t, cb - ca, zb - za) if axis == 'x' else (cb - ca, t, zb - za)
            B.box(mat, c, sz, tint=tint)

def card_plane(name, c, size, rot=(0, 0, 0), key='card_bertillon', parent=None, ink_t=0.0, thick=0.004):
    """a flat textured card (UV 0..1) facing local +y, plus a thin cream slab behind it (+ink hull). returns the root empty."""
    root = bpy.data.objects.new(name + '_root', None); bpy.context.scene.collection.objects.link(root); root.location = c; root.rotation_euler = [math.radians(a) for a in rot]
    if parent is not None: root.parent = parent
    w, h = size; me = bpy.data.meshes.new(name); me.from_pydata([(-w / 2, 0, -h / 2), (-w / 2, 0, h / 2), (w / 2, 0, h / 2), (w / 2, 0, -h / 2)], [], [(0, 1, 2, 3)]); me.update()
    uv = me.uv_layers.new(name='UVMap'); 
    for i, (u, v) in enumerate(((0, 0), (0, 1), (1, 1), (1, 0))): uv.data[i].uv = (u, v)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob); ob.parent = root; ob.location = (0, thick / 2 + 0.0005, 0); me.materials.append(get_mat(key))
    B = Batch(); B.box('cardedge', (0, 0, 0), (w, thick, h)); objs = B.finalize(name + '_edge', parent=root, ink_t=ink_t if ink_t else STATE['ink_t'] * 0.6)
    STATE['anim'][name] = dict(kind='card', root=root, objs=[ob] + objs); return root
def need_card(key, kind='bertillon', name=None, seed=7):
    STATE['cardpaths'][key] = TX.card(name or key, kind, seed)
    return key

def room_shell(B, x0, x1, y0, y1, h, wain=1.3, windows=(), doors=(), wall='wall', floor='floor', ceil='ceiling', beams=True, frieze=True, t=0.3):
    """floor, ceiling, four walls (holes for windows / doors), dark panelled wainscot to `wain`, skirting + cap rail, frieze under the cornice, beams.
    windows / doors: [(wall 'L'|'R'|'F'|'B', a0, a1, z0, z1)]  (L x0 wall, R x1 wall, F y0 wall, B y1 wall; a = along-wall coordinate)."""
    W = x1 - x0; Dd = y1 - y0; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    Bc = getattr(B, 'ceil', B); B.box(floor, (cx, cy, -0.1), (W + 2 * t, Dd + 2 * t, 0.2)); Bc.box(ceil, (cx, cy, h + 0.1), (W + 2 * t, Dd + 2 * t, 0.2))
    hol = {k: [(a0, a1, z0, z1) for (w_, a0, a1, z0, z1) in list(windows) + list(doors) if w_ == k] for k in 'LRFB'}
    wall_box(B, wall, 'x', x0, y0, y1, 0, h, hol['L'], out=-1, t=t); wall_box(B, wall, 'x', x1, y0, y1, 0, h, hol['R'], out=+1, t=t)
    wall_box(B, wall, 'y', y0, x0, x1, 0, h, hol['F'], out=-1, t=t); wall_box(B, wall, 'y', y1, x0, x1, 0, h, hol['B'], out=+1, t=t)
    dh = {k: [(a0, a1, 0, z1) for (w_, a0, a1, z0, z1) in doors if w_ == k] for k in 'LRFB'}
    # wainscot (proud of the wall by 0.04) with door gaps, cap rail, skirting
    def strip(mat, axis, pos, a0, a1, z0, z1, thick, gaps, out):
        cuts = sorted(set([a0, a1] + [g[0] for g in gaps] + [g[1] for g in gaps]))
        for ca, cb in zip(cuts[:-1], cuts[1:]):
            mid = (ca + cb) / 2
            if any(g[0] <= mid <= g[1] for g in gaps) or cb - ca < 1e-6: continue
            c = (pos - out * thick / 2, mid, (z0 + z1) / 2) if axis == 'x' else (mid, pos - out * thick / 2, (z0 + z1) / 2); sz = (thick, cb - ca, z1 - z0) if axis == 'x' else (cb - ca, thick, z1 - z0)
            B.box(mat, c, sz)
    for (axis, pos, a0, a1, out, k) in (('x', x0, y0, y1, -1, 'L'), ('x', x1, y0, y1, +1, 'R'), ('y', y0, x0, x1, -1, 'F'), ('y', y1, x0, x1, +1, 'B')):
        g = [(a, b) for (a, b, _, _) in dh[k]]
        strip('wain', axis, pos + (-out) * 0.0, a0, a1, 0.0, wain, 0.05, g, -out * -1 if False else -out)
        strip('walnut', axis, pos - out * 0.0, a0, a1, wain, wain + 0.06, 0.09, g, -out); strip('walnut', axis, pos, a0, a1, 0.0, 0.16, 0.07, g, -out)
        if frieze: strip('frieze', axis, pos, a0, a1, h - 0.62, h - 0.2, 0.02, [], -out)
        strip('walnut', axis, pos, a0, a1, h - 0.2, h, 0.14, [], -out); strip('walnut', axis, pos, a0, a1, h - 0.65, h - 0.62, 0.05, [], -out)
    if beams:
        for xx in np.arange(x0 + 0.8, x1, 1.6): Bc.box('beam', (xx, cy, h - 0.12), (0.22, Dd, 0.24))
        for yy in (y0 + Dd * 0.25, y0 + Dd * 0.75): Bc.box('beam', (cx, yy, h - 0.07), (W, 0.18, 0.14))

# ================================================================ A. MEASURING ROOM
MX0, MX1, MY0, MY1, MH = -3.2, 3.2, -4.2, 4.2, 3.8
def build_measure(B):
    A = {'marks': {}, 'objs': {}}
    win = ('L', 0.0, 2.4, 1.95, 3.4); dor = ('R', -3.0, -1.85, 0, 2.25)
    room_shell(B, MX0, MX1, MY0, MY1, MH, wain=1.3, windows=[win], doors=[dor])
    barred_window(B, MX0, 0.0, 2.4, 1.95, 3.4, bars=7)
    paris_roofs(B, MX0 - 0.3, -3.0, 6.0, side=-1, depth=13.0, seed=2, count=6, base_z=-8.5)
    door(B, (MX1 + 0.15, -2.425), rot=90, w=1.1, ajar=-35); A['door'] = (MX1, -2.425)
    # floor dressing: navy rug under the chair / camera area, dais cloth
    B.box('runner', (0.75, 1.5, 0.006), (1.4, 3.6, 0.012))
    # the instruments
    measuring_chair(B, (0.7, 2.4), rot=180, head_z=1.34)
    toise(B, (1.7, MY1 - 0.03), rot=180, slider=1.66)
    arm_span_scale(B, (-1.55, MY1 - 0.03), rot=180, length=2.0, z=1.42)
    foot_board(B, (2.2, 3.3), rot=0)
    # big steel calipers on show, mounted on a plaque on the left wall; and laid out on the small table beside the chair
    with B.xf((MX0 + 0.05, 3.35, 2.15), (0, 0, 90)):
        B.box('walnut', (0, 0.03, 0), (1.3, 0.05, 0.6)); B.box('baize', (0, 0.058, 0), (1.18, 0.012, 0.48))
        sliding_calipers(B, (0, 0.075, -0.1), rot=0, length=0.95, open_=0.34, tilt=(90, 0, 0), scale=1.0)
        spreading_calipers(B, (-0.2, 0.08, 0.2), rot=0, span=0.3, leg=0.36, tilt=(90, 0, 0), scale=0.9)
        for sx in (-0.55, 0.55): B.cyl('brass', (sx, 0.08, 0.2), 0.02, 0.03, axis='y', seg=8)
    table(B, (1.9, 1.55), size=(0.85, 0.55), h=0.8, rot=8, top='baize')
    with B.xf((1.9, 1.55, 0), (0, 0, 8)):
        sliding_calipers(B, (-0.02, -0.05, 0.808), rot=10, length=0.5, open_=0.2); spreading_calipers(B, (0.22, 0.12, 0.808), rot=-35, span=0.26, leg=0.3); inkpot(B, (-0.3, 0.15, 0.808), rot=25)
    # camera on a tripod, aimed at the chair (lens toward +y), black cloth on the back
    camera_tripod(B, (0.95, 0.55), rot=0)
    # the clerk's table at the right wall
    table(B, (2.7, 0.55), size=(1.5, 0.72), h=0.84, rot=90)
    with B.xf((2.7, 0.55, 0), (0, 0, 90)):
        ledger_stack(B, (-0.5, 0.1, 0.848), n=4, rot=15); open_ledger(B, (0.1, -0.05, 0.848), rot=-6); inkpot(B, (0.55, 0.2, 0.848), rot=20); inkpot(B, (0.47, 0.0, 0.848), quill=False)
        banker_lamp(B, (-0.1, 0.22, 0.848), rot=-20, watts=40); sliding_calipers(B, (0.3, -0.2, 0.848), rot=-8, length=0.4, open_=0.12)
    stool(B, (1.95, 0.55), h=0.64, rot=10)
    # bench along the left wall for the waiting prisoners
    bench(B, (-2.88, 1.2), length=2.6, rot=-90)
    # right wall: coat rack with kepis, umbrella stand, frames; back wall: clock + pendulum case, ledger shelf; stove in the corner
    coat_rack(B, (2.9, -0.75), rot=20, kepis=3); umbrella_stand(B, (2.9, -3.5, 0))
    wall_clock(B, (0.2, MY1 - 0.04, 3.05), rot=180, r=0.28); pendulum_case(B, (0.2, MY1 - 0.04, 2.7), rot=180, h=1.1, w=0.22)
    ledger_shelf(B, (-1.55, MY1 - 0.03, 2.2), length=2.1, rot=180, n=1); ledger_shelf(B, (1.3, MY1 - 0.03, 2.75), length=1.6, rot=180, n=1)
    mouth = stove(B, (2.75, 3.4), rot=-90, pipe_to=MH - 0.1); A['smoke_src'] = (2.75, 3.4, 1.15)
    for i, (nm, c, sz, rt, nrm) in enumerate((('n_a', (MX1 - 0.03, 1.9, 2.15), (0.5, 0.7), 90, 'R'), ('n_b', (MX1 - 0.03, 1.2, 2.3), (0.4, 0.55), 90, 'R'), ('n_c', (-0.9, MY1 - 0.03, 1.05), (0.5, 0.4), 180, 'B'))):
        pass
    for nm, c, sz, rt, ky in (('wc0', (MX1 - 0.04, 1.75, 2.15), (0.5, 0.68), -90, 'card_notice'), ('wc1', (MX1 - 0.04, 2.5, 2.2), (0.42, 0.56), -90, 'card_notice'), ('wc2', (0.45, MY1 - 0.04, 1.0), (0.5, 0.36), 180, 'card_portrait'),
                              ('wc3', (-0.3, MY1 - 0.04, 1.05), (0.4, 0.5), 180, 'card_portrait2')):
        B.box('walnut', (c[0], c[1], c[2]), ((sz[0] + 0.08, 0.04, sz[1] + 0.08) if abs(rt) == 180 else (0.04, sz[0] + 0.08, sz[1] + 0.08)))
        STATE.setdefault('wall_cards', []).append((nm, c, sz, rt, ky))
    # gas: gasoliers + brackets + a pipe run along the ceiling and down the walls
    gasolier(B, (-0.35, 1.0, MH - 0.05), drop=1.0, watts=260); gasolier(B, (1.0, -1.4, MH - 0.05), drop=1.0, watts=200)
    gas_bracket(B, (MX0 + 0.02, 3.35, 2.75), rot_z=0, watts=14); gas_bracket(B, (MX1 - 0.02, 2.3, 2.8), rot_z=180, watts=14); gas_bracket(B, (-2.6, MY1 - 0.02, 2.6), rot_z=-90, watts=14)
    gas_pipe(B, (-0.35, 1.0, MH - 0.08), (-0.35, MY1 - 0.1, MH - 0.08)); gas_pipe(B, (-0.35, MY1 - 0.1, MH - 0.08), (-2.6, MY1 - 0.1, MH - 0.08)); gas_pipe(B, (-2.6, MY1 - 0.1, MH - 0.08), (-2.6, MY1 - 0.1, 2.55))
    gas_pipe(B, (1.0, -1.4, MH - 0.08), (MX1 - 0.1, -1.4, MH - 0.08)); gas_pipe(B, (MX1 - 0.1, -1.4, MH - 0.08), (MX1 - 0.1, 2.3, MH - 0.08)); gas_pipe(B, (MX1 - 0.1, 2.3, MH - 0.08), (MX1 - 0.1, 2.3, 2.75))
    # floor clutter
    crate(B, (-2.5, -3.3, 0), size=(0.6, 0.45, 0.4), rot=12); crate(B, (-2.5, -3.3, 0.4), size=(0.5, 0.4, 0.3), rot=-8); crate(B, (-1.85, -3.55, 0), size=(0.45, 0.4, 0.35), rot=20)
    bucket(B, (2.55, -3.45, 0)); wastebin(B, (-0.4, 3.5, 0)); stool(B, (-0.9, -0.6), h=0.55, rot=30); ledger_stack(B, (-0.9, -0.6, 0.58), n=4, rot=10)
    # outside the window: nothing else; the sun shaft comes through it
    P = STATE['P']; d = np.array(P['sun_dir']); d = d / np.linalg.norm(d)
    cs = [(MX0 + 0.02, 0.0, 3.4), (MX0 + 0.02, 2.4, 3.4), (MX0 + 0.02, 2.4, 1.95), (MX0 + 0.02, 0.0, 1.95)]
    A['shaft'] = light_shaft(B, cs, d)
    # nested sun patch bounds for dust motes (centre, along-d length)
    A['dust_box'] = dict(p0=np.array([MX0 + 0.1, 1.2, 2.7]), d=d, L=4.2, w=1.2)
    A['pendulum'] = dict(pivot=(0.2, MY1 - 0.04 - 0.14, 2.62), rot=180, L=0.85)
    # stand points (feet, z = floor): name -> (x, y, z, facing deg, who)
    M = A['marks']
    M['chair'] = (0.7, 2.3, 0.42, 180, 'inspector')          # seated: feet on the dais (dais top 0.1): the card stands on the seat position
    M['clerk'] = (1.45, 1.95, 0.0, 200, 'clerk'); M['clerk_toise'] = (1.7, 3.55, 0.0, 180, 'clerk'); M['prisoner_toise'] = (1.7, 3.1, 0.0, 180, 'prisoner')
    for i, y in enumerate((0.15, 0.85, 1.55, 2.25)): M['bench%d' % i] = (-2.35, y, 0.0, 90, 'prisoner')
    M['queue0'] = (-1.5, -1.0, 0.0, 90, 'prisoner'); M['queue1'] = (-1.9, -0.2, 0.0, 90, 'prisoner')
    M['door_in'] = (2.3, -2.4, 0.0, 180, 'gendarme'); M['door_out'] = (3.0, -2.4, 0.0, 180, 'gendarme'); M['door_mid'] = (1.2, -1.6, 0.0, 200, 'prisoner')
    M['table'] = (2.0, 0.55, 0.0, 180, 'clerk'); M['armspan'] = (-1.55, 3.45, 0.0, 180, 'prisoner'); M['tripod'] = (0.2, 0.35, 0.0, 20, 'clerk')
    return A
def camera_tripod(B, c, rot=0, h=1.45):
    """period studio camera: wooden box + bellows + brass lens on a 3-leg tripod, black cloth draped over the back. lens toward local +y."""
    x, y = c[0], c[1]
    with B.xf((x, y, 0), (0, 0, rot)):
        for k in range(3):
            a = k * 120 + 90; ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            top = np.array([0, 0, h - 0.05]); bot = np.array([0.5 * ca, 0.5 * sa, 0.0]); mid = (top + bot) / 2; v = top - bot; Ln = np.linalg.norm(v)
            B.cyl('walnut', tuple(mid), 0.024, Ln, seg=8, rot=euler_to_z(v)); B.box('brass', tuple(bot + np.array([0, 0, 0.015])), (0.05, 0.05, 0.03))
        B.cyl('brass', (0, 0, h - 0.04), 0.1, 0.06, seg=14); B.box('walnut', (0, 0, h), (0.3, 0.3, 0.04))
        B.box('walnut', (0, -0.17, h + 0.22), (0.36, 0.26, 0.4)); B.box('iron', (0, -0.31, h + 0.22), (0.26, 0.1, 0.32)); B.box('cloth', (0, 0.0, h + 0.22), (0.28, 0.34, 0.28))
        B.box('walnut', (0, 0.18, h + 0.22), (0.3, 0.04, 0.32)); B.cyl('brass', (0, 0.26, h + 0.22), 0.075, 0.14, axis='y', r2=0.06, seg=16); B.cyl('glass', (0, 0.335, h + 0.22), 0.055, 0.01, axis='y', seg=16); B.cyl('brass', (0, 0.35, h + 0.22), 0.08, 0.02, axis='y', seg=16)
        rows, cols = 9, 14; V = []; F = []
        for i in range(rows):
            u = i / (rows - 1)
            for j in range(cols):
                a = math.pi * 2 * (j / (cols - 1)) - math.pi; z = h + 0.46 - 0.95 * u ** 1.3; rr = 0.2 + 0.34 * u ** 1.2 + 0.03 * math.sin(j * 2.4 + i)
                V.append((-0.3 - 0.07 * u + rr * math.cos(a) * 0.35, rr * math.sin(a), z))
        for i in range(rows - 1):
            for j in range(cols - 1): F.append((i * cols + j, i * cols + j + 1, (i + 1) * cols + j + 1, (i + 1) * cols + j))
        B.mesh('cloth', V, F, smooth=True)

# ================================================================ presets, build, render
HEIGHT['seated'] = 0.95
BUILDERS = {'measure': build_measure}
LOC_OVER = {}          # (location, light) -> overrides of the light preset
PRESETS = {}
def project(cam, p, w=720, h=1280):
    from bpy_extras.object_utils import world_to_camera_view
    v = world_to_camera_view(bpy.context.scene, cam, Vector(p)); return v.x * w, (1 - v.y) * h, v.z
def _place_wall_cards():
    for (nm, c, sz, rt, ky) in STATE.pop('wall_cards', []):
        nrm = {'card_notice': 'notice', 'card_portrait': 'portrait', 'card_portrait2': 'portrait'}[ky]
        off = Vector((0, 0.0, 0)); 
        card_plane(nm, (c[0], c[1], c[2]), sz, rot=(0, 0, rt), key=ky, ink_t=0.0, thick=0.004)
        ob = STATE['anim'][nm]['root']
        d = Vector((math.sin(math.radians(rt)) * -1, math.cos(math.radians(rt)), 0)); ob.location = Vector(c) + d * 0.022
def build(location=None, preset=None, light=None, ink=True, clear=True, fg=True):
    pr = PRESETS.get(preset) if preset else None
    if pr: location = location or pr['loc']; light = light or pr['light']
    light = light or 'DAY_INT'; over = dict(LOC_OVER.get((location, light), {}))
    if pr and pr.get('over'): over.update(pr['over'])
    sc = new_scene(light, over); STATE['loc'] = location; STATE['preset'] = preset; P = STATE['P']
    if pr:
        dist = (Vector(pr['cam']) - Vector(pr['look'])).length; STATE['ink_t'] = float(np.clip(0.00384 * pr.get('sd', dist), 0.004, 0.018)) if ink else 0.0
    else: STATE['ink_t'] = 0.012 if ink else 0.0
    for k, kind in (('card_notice', 'notice'), ('card_portrait', 'portrait'), ('card_portrait2', 'portrait2'), ('card_bertillon', 'bertillon')):
        STATE['cardpaths'][k] = TX.card(k, 'notice', 7) if kind == 'notice' else (TX.frame_art(k, 11 if kind == 'portrait' else 12) if kind.startswith('portrait') else TX.card(k, 'bertillon', 7))
    B = Batch(); B.ceil = Batch(); B.out = Batch(); A = BUILDERS[location](B); A['location'] = location; A['light'] = light; A['preset'] = preset
    B.finalize(location); STATE['ceil_objs'] = B.ceil.finalize(location + '_ceil')
    for o in B.out.finalize(location + '_out'): o.visible_shadow = False
    if pr and pr.get('cutaway'):
        for o in STATE['ceil_objs']: o.visible_camera = False
    _place_wall_cards(); sky_dome(); sun()
    if hasattr(sys.modules[__name__], '_init_hooks'): _init_hooks(A)
    if pr and fg and pr.get('fg'): pr['fg'](A)
    if pr:
        cam = camera(pr['cam'], pr['look'], pr.get('lens', 22.0)); A['cam'] = dict(loc=tuple(pr['cam']), look=tuple(pr['look']), lens=pr.get('lens', 22.0))
        if 'state' in pr: apply_state(A, pr['state'])
    return A
def apply_state(A, st): pass
def setup_render(sc, mode='final', samples=None):
    r = sc.render; r.image_settings.file_format = 'PNG'; r.threads_mode = 'FIXED'; r.threads = 4
    if mode == 'draft': r.resolution_x, r.resolution_y, r.resolution_percentage = 360, 640, 100; n = samples or 24
    else: r.resolution_x, r.resolution_y, r.resolution_percentage = 720, 1280, 100; n = samples or 80
    sc.cycles.samples = n; sc.cycles.use_denoising = True; sc.cycles.denoiser = 'OPENIMAGEDENOISE'; sc.cycles.preview_samples = 8
    STATE['scale'] = r.resolution_x / 720.0
def _gblur(a, rad):
    """separable gaussian blur (numpy, FFT-free): a is HxW or HxWxC float."""
    rad = max(float(rad), 0.3); k = int(rad * 3) + 1; x = np.arange(-k, k + 1); g = np.exp(-x * x / (2 * rad * rad)); g /= g.sum()
    def conv(arr, axis):
        p = np.pad(arr, [(k, k) if i == axis else (0, 0) for i in range(arr.ndim)], mode='edge'); out = np.zeros_like(arr, dtype=np.float32)
        for i, w in enumerate(g): out += w * np.take(p, np.arange(i, i + arr.shape[axis]), axis=axis)
        return out
    return conv(conv(a.astype(np.float32), 0), 1)
def grade(path, sat=1.12, bloom=0.5, scale=None):
    """final grade: bloom halo (12-24 px at 720 wide) around the real emitters only (min channel >= 252: lamp cores / skylights; the near-white heads
    are 246 and never bloom), then a saturation boost. Nothing else (no grain, no vignette)."""
    scale = scale or STATE.get('scale', 1.0)
    im = np.asarray(Image.open(path).convert('RGB'), dtype=np.float32) / 255
    if bloom:
        m = (im.min(-1) >= 252 / 255).astype(np.float32)
        if m.sum() > 4:
            from PIL import ImageFilter
            ring = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7 if scale < 1 else 13)), dtype=np.float32) / 255 - m
            ringc = _gblur(im * ring[..., None], 6 * scale) / (_gblur(ring, 6 * scale)[..., None] + 1e-4); ringc = ringc / (ringc.max(-1, keepdims=True) + 1e-4)
            core = _gblur(m, 7 * scale); wide = _gblur(m, 16 * scale); halo = (0.6 * core + 0.5 * wide)[..., None] * ringc
            im = np.clip(im + bloom * halo, 0, 1)
    mx = im.max(-1, keepdims=True); im = np.clip(mx - (mx - im) * sat, 0, 1)
    Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save(path)
def render(path, mode='final', samples=None, do_grade=True):
    sc = bpy.context.scene; setup_render(sc, mode, samples); sc.render.filepath = path; t = time.time(); c0 = time.process_time()
    bpy.ops.render.render(write_still=True); dt = time.time() - t
    if do_grade: grade(path)
    return dt
def stage_placeholders(A, cam=None, marks=None, only=None):
    """flat stand-in cast cards at the stand points, turned to the camera: near-white head #fef7f6 with a plum ring, a coloured body."""
    cam = cam or bpy.context.scene.camera; cl = cam.location; out = {}
    for nm, (x, y, z, fz, who) in (marks or A['marks']).items():
        if only and nm not in only: continue
        key = 'seated' if nm == 'chair' else who; H = HEIGHT[key]; hd = H * 0.3; hc = H - hd * 0.52; bw = H * 0.36
        B = Batch(); seg = 24; a = np.linspace(0, 2 * math.pi, seg, endpoint=False)
        def disc(mat, cx, cz, rx, rz_, yy):
            v = [(cx, yy, cz)] + [(cx + rx * math.cos(t), yy, cz + rz_ * math.sin(t)) for t in a]; B.mesh(mat, v, [(0, 1 + i, 1 + (i + 1) % seg) for i in range(seg)], smooth=False)
        disc('ph_ring', 0, hc, hd * 0.5 * 1.06, hd * 0.5 * 1.06, 0.0); disc('ph_head', 0, hc, hd * 0.5, hd * 0.5, 0.003)
        B.mesh('ph_body_' + key, [(-bw / 2, 0.001, 0), (bw / 2, 0.001, 0), (bw * 0.36, 0.001, H - hd * 1.0), (-bw * 0.36, 0.001, H - hd * 1.0)], [(0, 1, 2, 3)], smooth=False)
        ob = B.finalize('ph_' + nm, loc=(x, y, z), ink=False)
        for o in ob:
            o.rotation_euler = (0, 0, math.atan2(-(cl.x - x), (cl.y - y)))
            if o.name.endswith('ph_head') or o.name.endswith('ph_ring'): o.visible_shadow = False
        out[nm] = ob
    return out
def head_ring_luma(A, img_path, cam=None, marks=None, only=None, W=720, Hh=1280):
    """median luma (0-255) of the background ring around each placeholder head (upper 240 deg of an annulus 1.2-1.8 R) + the head centre / chin pixel."""
    cam = cam or bpy.context.scene.camera; im = np.asarray(Image.open(img_path).convert('L').resize((W, Hh)), dtype=float); res = {}
    yy, xx = np.mgrid[0:Hh, 0:W]
    for nm, (x, y, z, fz, who) in (marks or A['marks']).items():
        if only and nm not in only: continue
        key = 'seated' if nm == 'chair' else who; Hh_ = HEIGHT[key]; hd = Hh_ * 0.3; hc = z + Hh_ - hd * 0.52
        px, py, dz = project(cam, (x, y, hc), W, Hh)
        if dz <= 0: continue
        R = hd * 0.5 * 782.2 * (W / 720) / dz * (1280 / Hh if False else 1)
        cx, cy = px, py; rr = np.hypot(xx - cx, yy - cy); ang = np.degrees(np.arctan2(-(yy - cy), xx - cx))
        sel = (rr > 1.2 * R) & (rr < 1.8 * R) & (ang > -20) & (ang < 200)
        if sel.sum() < 30: continue
        chin = py + R
        res[nm] = dict(luma=float(np.median(im[sel])), cx=px, cy=py, R=R, chin=chin, in_frame=bool(0 <= px < W and 0 <= py < Hh))
    return res

PRESETS['measure_wide'] = dict(loc='measure', light='DAY_INT', cam=(-1.9, -3.9, 1.5), look=(0.8, 2.4, 1.35), lens=22.0)
PRESETS['measure_high'] = dict(loc='measure', light='DAY_INT', cam=(2.9, -3.9, 3.5), look=(-0.4, 1.9, 0.4), lens=22.0, cutaway=True)
