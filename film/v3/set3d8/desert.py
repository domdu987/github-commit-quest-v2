#!/usr/bin/env python3
"""desert.py : sets of film 8 ("ไอ้บ้าน้ำแข็ง", the ice-maker of the Persian desert, c. 1600) as real 3D Blender sets (bpy 5.3, Cycles CPU).
Two locations, each built by preset (the preset picks the area, the default light, the camera and the set state):

    import desert as D
    A = D.build('desert_ice', 'channels_wide')            # channels_wide | channel_ecu | wall_low | dome_wide | sky_reveal  (the plain)
                                                          # dome_interior                                                   (inside the yakhchal)
    A = D.build('bazaar', 'bazaar_wide', light='SUMMER')  # bazaar_wide | merchant_stall | well_eye
    cam = D.make_camera(A['cam'])
    D.set_ice(0.25)                 # channel state: 0 open water .. 0.25 thin sheet (night 1) .. 1 thick white-blue (night 10)
    D.set_ice(1.0, melt=1.0)        # melted to mud by noon (also D.set_ice('water' | 'thin' | 'thick' | 'mud'))
    D.set_heat_wisps(1.0, frame=n)  # reveal: faint shimmering heat wisps rising from the channels to the stars (call per frame)
    D.set_flames(1.0, frame=n)      # lantern / fire / lamp flicker (call per frame; deterministic)
    D.set_stars(1.0, twinkle=0.4, frame=n)   # star brilliance (bloom) and twinkle (NIGHT / DAWN sky)

Light presets (build light=): NIGHT (cool moon + starlight, Milky Way, warm lanterns and fire), DAWN (pink-gold sunrise in the east),
NOON (harsh warm winter-noon sun, blue shade under the wall), SUMMER (white-hot high sun, heat haze).
World: 1 unit = 1 D (head diameter), Z up, ground z = 0, +x = east, +y = north. NO depth of field anywhere (client rule: sharp).
Built on v3/set3d7/louvre.py -> bakery.py -> mine.py -> pagoda.py / tower.py: materials, mesh builder, render, grade, cameras, keys,
actors, haze, denoiser, glow cards are imported, not rewritten. See desert_API.md.
CLI: python3 desert.py stills | final <loc> [preset[:LIGHT] ..] | digest <loc> <preset>"""
import os, sys, math, json, time, random
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import louvre as LV                                        # noqa: E402  (film-7 template: sky dome, flame lights, staging, head pixels)
import desert_tex as DT                                    # noqa: E402
from tower import MB, no_bounce, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, catenary, chain_rod, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
WORK = os.path.join(HERE, 'desert_work')
STATE = T.STATE
setup_dof = G.setup_dof; digest = G.digest
Frame = BK.Frame; _halo = BK._halo

def _rnd(seed): return random.Random(seed)
FIRE = (1.0, 0.62, 0.3); LAMP = (1.0, 0.74, 0.42)

# ----------------------------------------------------------------------------- dimensions (D)
WALL = dict(x=(-30.0, 30.0), y=(-2.4, -0.8), h=15.0)                   # the shade wall: south of the channels, 3 storeys
CH_X = (-26.0, 26.0); CH_W = 2.0; CH_Y = [1.8, 4.6, 7.4, 10.2, 13.0]      # five channels: x run, width, centre lines y
CH_Z = dict(floor=-0.32, water=-0.13, ice0=-0.11, mud=-0.085)          # trench floor, water, ice (rises with thickness), mud
CUT = (-1.6, 0.0)                                                       # the sawn hole in channel 2 (index 1): x0, x1
DOME = dict(c=(38.0, 8.0), R=12.5, H=27.0, steps=13, door_dir=(-1.0, 0.0))
PIT = dict(r=9.0, z=-6.0, walk=(9.0, 11.6))                             # inside: the ice pit radius, depth, the walkway ring
STREET = dict(x=(-4.5, 4.5), y=(-14.0, 30.0), mod=4.5, H=10.5, sq=(30.0, 46.0), sq_x=(-13.0, 13.0))

# ----------------------------------------------------------------------------- light presets
_B = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, grade_offset=(0.002, 0.003, 0.006), sun_angle=0.6)
LIGHTS = dict(
    NIGHT=dict(_B, key=(0.24, 0.34, 0.72), key_dir=G._kd((0.45, -0.89), 38), sun_elev=38, key_desat=0.25, ink='#141a3e', night=True,
               shade=(0.055, 0.085, 0.24), shade_tint=(0.06, 0.095, 0.30), shade_mix=0.72, lift=(0.004, 0.007, 0.024), sky='NIGHT', sky_k=1.0, star_k=1.0, ground_k=0.55,
               pano='NIGHT', pano_k=0.95, haze=('#3a5aa0', 0.06), grade_saturation=1.12, refl_k=0.9, lamps=1.0, shaft_k=0.12, wisp_rgb=(0.7, 0.85, 1.0)),
    DAWN=dict(_B, key=(1.70, 0.98, 0.62), key_dir=G._kd((-0.97, 0.22), 7), sun_elev=7, sun_angle=1.0,
              shade=(0.10, 0.12, 0.28), shade_tint=(0.10, 0.13, 0.32), shade_mix=0.55, grade_offset=(-0.008, -0.008, -0.004), lift=(0.008, 0.006, 0.02), sky='DAWN', sky_k=1.0, star_k=0.6,
              pano='DAWN', pano_k=0.95, haze=('#ffb48a', 0.12), grade_saturation=1.12, refl_k=0.8, lamps=0.7, shaft_k=0.25, wisp_rgb=(1.0, 0.85, 0.75)),
    NOON=dict(_B, key=(1.80, 1.52, 1.08), key_dir=G._kd((0.18, 0.98), 44), sun_elev=44, sun_angle=0.5,
              shade=(0.10, 0.12, 0.30), shade_tint=(0.09, 0.12, 0.34), shade_mix=0.45, grade_offset=(-0.012, -0.011, -0.006), lift=(0.006, 0.008, 0.022), sky='NOON', sky_k=0.95, star_k=0.0,
              pano='NOON', pano_k=0.95, haze=('#fff0d8', 0.10), grade_saturation=1.15, refl_k=0.7, lamps=0.35, shaft_k=0.3, wisp_rgb=(1.0, 0.95, 0.85)),
    SUMMER=dict(_B, key=(1.92, 1.72, 1.18), ground_k=0.9, key_dir=G._kd((0.12, 0.99), 70), sun_elev=70, sun_angle=0.5,
                shade=(0.12, 0.13, 0.29), shade_tint=(0.11, 0.13, 0.32), shade_mix=0.45, grade_offset=(-0.012, -0.011, -0.006), lift=(0.008, 0.008, 0.018), sky='SUMMER', sky_k=0.95, star_k=0.0,
                pano='SUMMER', pano_k=0.95, haze=('#fff4dc', 0.16), grade_saturation=1.06, refl_k=0.7, lamps=0.3, shaft_k=0.35, wisp_rgb=(1.0, 0.96, 0.88)),
)
# bazaar: the street runs north (+y); the sun comes from the south-west so the east row is lit and the west row is in blue shade
BAZAAR_KD = dict(NIGHT=G._kd((0.5, -0.86), 40), DAWN=G._kd((-0.97, 0.22), 9), NOON=G._kd((0.55, 0.84), 56), SUMMER=G._kd((0.45, 0.89), 72))

PRESETS = dict(
    channels_wide=dict(loc='desert_ice', area='plain', light='NIGHT', cam='channels_wide', ice=0.25),
    channel_ecu=dict(loc='desert_ice', area='plain', light='NIGHT', cam='channel_ecu', ice=0.25),
    wall_low=dict(loc='desert_ice', area='plain', light='NOON', cam='wall_low', ice=1.0),
    dome_wide=dict(loc='desert_ice', area='plain', light='NIGHT', cam='dome_wide', ice=1.0),
    sky_reveal=dict(loc='desert_ice', area='plain', light='NIGHT', cam='sky_reveal', ice=0.6, wisps=1.0),
    dome_interior=dict(loc='desert_ice', area='dome_in', light='NIGHT', cam='dome_interior'),
    bazaar_wide=dict(loc='bazaar', area='bazaar', light='NOON', cam='bazaar_wide'),
    merchant_stall=dict(loc='bazaar', area='bazaar', light='NOON', cam='merchant_stall'),
    well_eye=dict(loc='bazaar', area='bazaar', light='NOON', cam='well_eye'),
)
LOC_PRESETS = dict(desert_ice=['channels_wide', 'channel_ecu', 'wall_low', 'dome_wide', 'sky_reveal', 'dome_interior'],
                   bazaar=['bazaar_wide', 'merchant_stall', 'well_eye'])

# ----------------------------------------------------------------------------- build
def build(location='desert_ice', preset=None, clear=True, dress=True, light=None):
    """Build one location ('desert_ice' | 'bazaar') for a preset (LOC_PRESETS) into the current scene: the preset's area only, its
    light (light= overrides it: NIGHT | DAWN | NOON | SUMMER), world, render settings, grade, denoiser, and the preset's set state
    (ice level, wisps). Returns the anchors dict (desert_API.md); A['cam'] is the preset camera."""
    preset = preset or LOC_PRESETS[location][0]
    assert preset in LOC_PRESETS[location], 'preset %s is not one of %s' % (preset, LOC_PRESETS[location])
    PR = PRESETS[preset]; lkey = light or PR['light']
    scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    if PR['area'] == 'bazaar': P['key_dir'] = BAZAAR_KD[lkey]; P['pano'] = 'town_' + lkey
    if PR['area'] == 'dome_in':                     # lamp-lit interior: shade pushed to hue ~225 (the lamps' complement) - red mud + violet shade reads magenta
        P.update(shade=(0.05, 0.10, 0.16), shade_tint=(0.05, 0.11, 0.18), shade_mix=0.8)
    STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location; STATE['area'] = PR['area']; STATE['light'] = lkey
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for li in list(bpy.data.lights):
        if li.users == 0: bpy.data.lights.remove(li)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('DSR_', 'ink')): bpy.data.materials.remove(m)
    tx = DT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_desert') or bpy.data.worlds.new('W_desert'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'DSR_%s_%s_' % (PR['area'], lkey); FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s' % (pre, name, gain, _k(sm), form, alpha, smix), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None, alpha=alpha, shade_mix=smix))
    def E(name, image=None, hexcol='#ffffff', k=1.0, alpha=False): return mat_emit(pre + 'e_' + name + ('_' + image if image else ''), hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    STATE.update(C=C, TX=TX, E=E, pre=pre)
    M = _materials(P, C, TX, E, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    STATE['flames'] = []; STATE['flame_mats'] = list(M['_flame_mats']); STATE['marks'] = {}; STATE['extra'] = {}
    dict(plain=_plain, dome_in=_dome_in, bazaar=_bazaar)[PR['area']](SET, P, M, dress)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    setup_grade(scene)
    for ob in SET.objects: no_bounce(ob)
    set_flames(1.0)
    apply_preset_state(preset)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """= mine.setup_render: final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light only, OpenImageDenoise. No DOF."""
    MN.setup_render(scene, quality)

def apply_dof(cam_name=None, scene=None, cam=None):
    """Client rule: no depth of field at all (kept for API symmetry)."""
    return None

# ============================================================================= materials
def _nodes(m): return m.node_tree.nodes

def _value(nt, name, v):
    n = nt.nodes.new('ShaderNodeValue'); n.name = name; n.outputs[0].default_value = v; return n

def _sky_lookup(nt, image, vec_socket):
    """Image lookup of a sky texture (sky-dome UV space: u = azimuth / 2 pi from +x, v = (elevation + 15 deg) / 105 deg) along a
    world direction socket -> TexImage node."""
    N = nt.nodes.new; L = nt.links.new
    sp = N('ShaderNodeSeparateXYZ'); L(vec_socket, sp.inputs[0])
    at = N('ShaderNodeMath'); at.operation = 'ARCTAN2'; L(sp.outputs['Y'], at.inputs[0]); L(sp.outputs['X'], at.inputs[1])
    u0 = N('ShaderNodeMath'); u0.operation = 'MULTIPLY_ADD'; u0.inputs[1].default_value = 1 / (2 * math.pi); u0.inputs[2].default_value = 1.0; L(at.outputs[0], u0.inputs[0])
    u = N('ShaderNodeMath'); u.operation = 'FRACT'; L(u0.outputs[0], u.inputs[0])
    cz = N('ShaderNodeMath'); cz.operation = 'MINIMUM'; cz.inputs[1].default_value = 1.0; L(sp.outputs['Z'], cz.inputs[0])
    asn = N('ShaderNodeMath'); asn.operation = 'ARCSINE'; L(cz.outputs[0], asn.inputs[0])
    v = N('ShaderNodeMath'); v.operation = 'MULTIPLY_ADD'; v.inputs[1].default_value = 180 / math.pi / 105.0; v.inputs[2].default_value = 15 / 105.0; L(asn.outputs[0], v.inputs[0])
    cb = N('ShaderNodeCombineXYZ'); L(u.outputs[0], cb.inputs[0]); L(v.outputs[0], cb.inputs[1])
    t = N('ShaderNodeTexImage'); t.image = T._img(image); t.extension = 'EXTEND'; L(cb.outputs[0], t.inputs['Vector'])
    return t

def _mat_water(name, P, base='#183650', murk='#4a3624'):
    """Channel water: dark lit base + a fake mirror of the sky (the sky texture looked up along the reflected view ray, with a little
    ripple), x a Fresnel-ish factor x refl_k. Value node 'murk' (0..1) turns it into brown mud water (set_ice melt)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, base)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    def make(nt):
        geo = N('ShaderNodeNewGeometry'); neg = N('ShaderNodeVectorMath'); neg.operation = 'SCALE'; neg.inputs['Scale'].default_value = -1.0; L(geo.outputs['Incoming'], neg.inputs[0])
        tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 1.4; nz.inputs['Detail'].default_value = 2.0; L(tc.outputs['Object'], nz.inputs['Vector'])
        sub = N('ShaderNodeVectorMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = (0.5, 0.5, 0.5); L(nz.outputs['Color'], sub.inputs[0])
        sc = N('ShaderNodeVectorMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = (0.05, 0.05, 0.0); L(sub.outputs[0], sc.inputs[0])
        nn = N('ShaderNodeVectorMath'); nn.operation = 'ADD'; nn.inputs[1].default_value = (0, 0, 1); L(sc.outputs[0], nn.inputs[0])
        nrm = N('ShaderNodeVectorMath'); nrm.operation = 'NORMALIZE'; L(nn.outputs[0], nrm.inputs[0])
        rf = N('ShaderNodeVectorMath'); rf.operation = 'REFLECT'; L(neg.outputs[0], rf.inputs[0]); L(nrm.outputs[0], rf.inputs[1])
        t = _sky_lookup(nt, STATE['tx']['sky_' + P['sky']], rf.outputs[0])
        fr = N('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = 0.35
        f2 = N('ShaderNodeMath'); f2.operation = 'MULTIPLY_ADD'; f2.inputs[1].default_value = 0.6; f2.inputs[2].default_value = 0.4; L(fr.outputs['Fresnel'], f2.inputs[0])
        mk = _value(nt, 'murk', 0.0)
        inv = N('ShaderNodeMath'); inv.operation = 'MULTIPLY_ADD'; inv.inputs[1].default_value = -0.65; inv.inputs[2].default_value = 1.0; L(mk.outputs[0], inv.inputs[0])
        k = N('ShaderNodeMath'); k.operation = 'MULTIPLY'; L(f2.outputs[0], k.inputs[0]); L(inv.outputs[0], k.inputs[1])
        k2 = N('ShaderNodeMath'); k2.operation = 'MULTIPLY'; k2.inputs[1].default_value = P.get('refl_k', 0.8); L(k.outputs[0], k2.inputs[0])
        tint = N('ShaderNodeMix'); tint.data_type = 'RGBA'; tint.blend_type = 'MULTIPLY'; L(mk.outputs[0], tint.inputs[0]); L(t.outputs['Color'], tint.inputs[6]); tint.inputs[7].default_value = (0.75, 0.55, 0.38, 1)
        em = N('ShaderNodeEmission'); L(tint.outputs[2], em.inputs['Color']); L(k2.outputs[0], em.inputs['Strength'])
        return em.outputs['Emission']
    MN._append_shader(m, make)
    # murk also browns the diffuse base
    rgb = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeRGB'][0]; mk = nt.nodes['murk']
    mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(mk.outputs[0], mx.inputs[0]); mx.inputs[7].default_value = (*T.hex_lin(murk), 1)
    for l in list(rgb.outputs[0].links): to = l.to_socket; nt.links.remove(l); L(mx.outputs[2], to)
    L(rgb.outputs[0], mx.inputs[6])
    return m

def _retarget(nt, old_socket, new_socket):
    for l in list(old_socket.links):
        to = l.to_socket; nt.links.remove(l); nt.links.new(new_socket, to)

def _mat_ice(name, P, tx):
    """Channel ice: one material for every thickness. Value 'ice_k' 0 (thin first-night sheet: a glassy veil of alpha ~0.2 with white
    frost needles, the water and its sky mirror show through) .. 1 (thick opaque white-blue slab with cracks and bubbles); value
    'ice_vis' fades it out (melt). Lit like every surface, plus a glossy lobe for the lantern glints."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, image=tx['ice_thick'], alpha=True, form=tuple(P['form']), shade_mul=(1.1, 1.15, 1.25), shade_mix=0.5)); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    thick = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
    thin = N('ShaderNodeTexImage'); thin.image = T._img(tx['ice_thin'])
    ik = _value(nt, 'ice_k', 1.0); iv = _value(nt, 'ice_vis', 1.0)
    sm = N('ShaderNodeMapRange'); sm.interpolation_type = 'SMOOTHSTEP'; sm.inputs['From Min'].default_value = 0.2; sm.inputs['From Max'].default_value = 0.85; L(ik.outputs[0], sm.inputs['Value'])
    cm = N('ShaderNodeMix'); cm.data_type = 'RGBA'; L(sm.outputs['Result'], cm.inputs[0]); L(thin.outputs['Color'], cm.inputs[6])
    mixsh = thick.outputs['Alpha'].links[0].to_node
    _retarget(nt, thick.outputs['Color'], cm.outputs[2]); L(thick.outputs['Color'], cm.inputs[7])
    am = N('ShaderNodeMix'); am.data_type = 'FLOAT'; L(sm.outputs['Result'], am.inputs[0]); L(thin.outputs['Alpha'], am.inputs[2]); am.inputs[3].default_value = 1.0
    av = N('ShaderNodeMath'); av.operation = 'MULTIPLY'; L(am.outputs[0], av.inputs[0]); L(iv.outputs[0], av.inputs[1])
    for l in list(thick.outputs['Alpha'].links): nt.links.remove(l)
    L(av.outputs[0], mixsh.inputs['Fac'])
    return _glossy(m, (0.85, 0.92, 1.0), 0.22, 0.12)

def _mat_alpha_k(m, node='vis', v=1.0):
    """Multiply the alpha (Mix shader Fac fed by the texture alpha) of a lit material by a Value node."""
    nt = m.node_tree; tx_ = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
    if node in nt.nodes: return m
    k = _value(nt, node, v); mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY'
    l = tx_.outputs['Alpha'].links[0]; to = l.to_socket; nt.links.remove(l); nt.links.new(tx_.outputs['Alpha'], mu.inputs[0]); nt.links.new(k.outputs[0], mu.inputs[1]); nt.links.new(mu.outputs[0], to)
    return m

def _mat_sky(name, P, image, k):
    """Sky dome: emission of the painted sky x sky_k, with the bright stars boosted over 1 (they feed the bloom) x star_k x a twinkle
    noise (4D noise whose W set_stars keys with the frame)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = mat_emit(name, image=image, strength=k); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    em = nt.nodes['strength']; tex = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]
    bw = N('ShaderNodeRGBToBW'); L(tex.outputs['Color'], bw.inputs[0])
    s1 = N('ShaderNodeMath'); s1.operation = 'SUBTRACT'; s1.inputs[1].default_value = 0.42; L(bw.outputs[0], s1.inputs[0])
    s2 = N('ShaderNodeMath'); s2.operation = 'MAXIMUM'; s2.inputs[1].default_value = 0.0; L(s1.outputs[0], s2.inputs[0])
    s3 = N('ShaderNodeMath'); s3.operation = 'MULTIPLY'; s3.inputs[1].default_value = 7.0; L(s2.outputs[0], s3.inputs[0])
    sk = _value(nt, 'star_k', P.get('star_k', 0.0))
    s4 = N('ShaderNodeMath'); s4.operation = 'MULTIPLY'; L(s3.outputs[0], s4.inputs[0]); L(sk.outputs[0], s4.inputs[1])
    uv = N('ShaderNodeUVMap'); mp = N('ShaderNodeVectorMath'); mp.operation = 'MULTIPLY'; mp.inputs[1].default_value = (1100.0, 320.0, 1.0); L(uv.outputs['UV'], mp.inputs[0])
    nz = N('ShaderNodeTexNoise'); nz.noise_dimensions = '4D'; nz.name = 'twinkle'; nz.inputs['Scale'].default_value = 1.0; nz.inputs['Detail'].default_value = 0.0; L(mp.outputs[0], nz.inputs['Vector'])
    tw = _value(nt, 'twinkle_k', 0.35)
    t1 = N('ShaderNodeMath'); t1.operation = 'SUBTRACT'; t1.inputs[1].default_value = 0.5; L(nz.outputs['Fac'], t1.inputs[0])
    t2 = N('ShaderNodeMath'); t2.operation = 'MULTIPLY'; L(t1.outputs[0], t2.inputs[0]); L(tw.outputs[0], t2.inputs[1])
    t3 = N('ShaderNodeMath'); t3.operation = 'MULTIPLY_ADD'; t3.inputs[1].default_value = 2.5; t3.inputs[2].default_value = 1.0; L(t2.outputs[0], t3.inputs[0])
    s5 = N('ShaderNodeMath'); s5.operation = 'MULTIPLY'; L(s4.outputs[0], s5.inputs[0]); L(t3.outputs[0], s5.inputs[1])
    s6 = N('ShaderNodeMath'); s6.operation = 'ADD'; s6.inputs[1].default_value = k; L(s5.outputs[0], s6.inputs[0])
    L(s6.outputs[0], em.inputs['Strength'])
    return m

def _materials(P, C, TX, E, tx, pre):
    lamp_k = P.get('lamps', 1.0)
    gk = P.get('ground_k', 1.0)
    M = dict(sand=TX('sand', gk, form=False), sand_d=TX('sand_d', gk, form=False), bank=TX('bank', gk, form=False), path=TX('path', form=False),
             mudbrick=TX('mudbrick'), mudbrick_d=TX('mudbrick_d'), kahgel=TX('kahgel'), kahgel_in=TX('kahgel_in', 1.25), trench=TX('bank', 0.75, form=False),
             ice_block=_glossy(TX('ice_block', 1.0, (1.1, 1.15, 1.25), smix=0.5), (0.85, 0.92, 1.0), 0.45, 0.15), mat=TX('mat'),
             wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b08458'), iron=_glossy(C('#2e2c32', 1.0, 1.1), (1.0, 0.9, 0.8), 0.3, 0.3),
             brass=_glossy(C('#c0923e', 1.0, (2.2, 1.5, 0.6)), (1.0, 0.82, 0.5), 0.5, 0.22), copper=_glossy(C('#c06a34', 1.0, (2.0, 1.2, 0.7), smix=0.3), (1.0, 0.7, 0.45), 0.6, 0.2),
             terra=C('#b8683e', 1.0, (1.4, 1.0, 0.8), smix=0.4), terra_l=C('#d0a070'), terra_d=C('#8a4a2a', 1.0, (1.4, 1.0, 0.8), smix=0.4),
             cloth=TX('cloth_w'), white=C('#f2eee4'), black=C('#24222a'), dark=C('#1e1814', 1.0, 0.6, form=False), red=C('#a83028', 1.0, (1.3, 0.75, 0.6), smix=0.15),
             palm=C('#4a6a2a'), palm_d=C('#3a5222'), trunk=C('#7a5a3a'), shrub=C('#7a7a3a'), rock=C('#a08470'), rope=C('#c8a868'), straw=C('#d8b870'), planks=TX('planks', form=False),
             tq=_glossy(C('#2a9ab0', 1.0, (0.8, 1.1, 1.2)), (0.9, 1.0, 1.0), 0.35, 0.15), lapis=_glossy(C('#1e3a7a'), (0.9, 1.0, 1.0), 0.35, 0.15), cream=C('#ecdcb8'), plaster=C('#e0c8a0'),
             gold=_glossy(C('#d8a840', 1.0, (2.2, 1.5, 0.6)), (1.0, 0.85, 0.5), 0.6, 0.2),
             flame=mat_emit(pre + 'e_flame', '#ffa040', strength=6.0), flame_c=mat_emit(pre + 'e_flamec', '#fff0c0', strength=10.0), ember=mat_emit(pre + 'e_ember', '#ff6a20', strength=3.0),
             lamp_glass=mat_emit(pre + 'e_lampp', image=tx['lantern_p'], strength=3.0 * max(0.35, lamp_k)), lamp_glow=mat_emit(pre + 'e_lampglow', '#ffc070', strength=3.0 * max(0.35, lamp_k)),
             door_glow=mat_emit(pre + 'e_doorglow', '#ff9a48', strength=1.4 * lamp_k), door_dark=mat_emit(pre + 'e_doordark', '#1a1018', strength=1.0),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.62, 0.3), 0.55 * lamp_k), halo_big=BK._mat_add(pre + 'halo_big', tx['pool'], (1.0, 0.55, 0.24), 0.9 * lamp_k, node='fire_glow'),
             pool=BK._mat_add(pre + 'pool', tx['pool'], (1.0, 0.6, 0.3), 0.5 * lamp_k, node='pool_k'),
             shaft=BK._mat_add(pre + 'shaft', tx['shaft'], tuple(c / max(P['key']) for c in P['key']), P.get('shaft_k', 0.15), node='shaft_k'),
             wisp=BK._mat_add(pre + 'wisp', tx['wisp'], P.get('wisp_rgb', (0.8, 0.9, 1.0)), 0.0, node='wisp_k', scroll=True, fade=True),
             water=_mat_water(pre + 'water', P), ice=_mat_ice(pre + 'ice', P, tx), mud=_mat_alpha_k(TX('mud', alpha=True, form=False), 'mud_k', 0.0))
    # bazaar
    M.update(pbrick=TX('pbrick'), pbrick_l=TX('pbrick_l'), tile_band=TX('tile_band', 1.0, (0.8, 1.0, 1.2)), tile_band_t=TX('tile_band_t', 1.0, (0.8, 1.0, 1.2)),
             tile_panel=TX('tile_panel', 1.0, (0.8, 1.0, 1.2)), tile_panel_l=TX('tile_panel_l', 1.0, (0.8, 1.0, 1.2)), kufic=TX('kufic'), pavers=TX('pavers', form=False),
             lattice=TX('lattice', alpha=True), kilim=[TX('kilim', smix=0.35), TX('kilim2', smix=0.35)],
             carpets=[TX('carpet%d' % k, 1.0, (1.2, 0.9, 0.8), smix=0.35) for k in range(6)],
             shops=[mat_emit(pre + 'e_shop%d' % k, image=tx['shop%d' % k], strength=0.55 + 0.25 * (P['sky'] == 'NIGHT')) for k in range(4)],
             awn=[TX('awn_%s' % c, alpha=True, smix=0.35) for c in ('red', 'blue', 'green', 'ochre')],
             spice=[C(c, 1.0, (1.3, 0.9, 0.7), smix=0.3) for c in ('#c0301e', '#e8a820', '#d86a1e', '#7a8a2a', '#8a4a24', '#e8d070')],
             fruit=[C(c, 1.0, (1.3, 0.8, 0.7), smix=0.2) for c in ('#b02a30', '#5a3418', '#d8b040', '#6a9a3a')], basket=C('#b08850'), basket_d=C('#7a5a30'))
    M['_flame_mats'] = [M['flame'], M['flame_c'], M['ember'], M['lamp_glass'], M['lamp_glow'], M['door_glow']] + M['shops']
    M['sky'] = _mat_sky(pre + 'sky_' + P['sky'], P, tx['sky_' + P['sky']], P['sky_k'])
    return M

# ============================================================================= sky, pano, haze
def _sky(SET, P, M, R=160.0):
    """Sky dome (R 160, the sky-dome UV of louvre._sky_dome) with the star/twinkle material; the painted ring at R 120; haze rings."""
    tx = STATE['tx']; mb = MB(); seg = 72; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o
    mb = MB(); Rp = DT.PANO_R; seg = 128
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
        mb.face([Vector((Rp * math.cos(a0), Rp * math.sin(a0), DT.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), DT.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), DT.PANO_Z1)), Vector((Rp * math.cos(a0), Rp * math.sin(a0), DT.PANO_Z1))],
                mat_emit(STATE['pre'] + 'e_pano', image=tx['pano_' + P['pano']], strength=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
    _obj(mb, 'backdrop', SET, shadow=False)
    if P.get('haze'):
        hm = G._haze_mat(STATE['pre'] + 'haze', P['haze'][0], P['haze'][1], 0.0, 26.0); mb = MB()
        for Rh in (45.0, 75.0, 105.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64
                mb.face([Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        _obj(mb, 'haze', SET, shadow=False)

def _flame_light(name, loc, rgb, energy, radius=0.12, shadow=False):
    ob = BK._light(name, loc, rgb, energy, radius=radius, shadow=shadow); STATE['flames'].append((ob, energy)); return ob

# ============================================================================= props
def _lantern(mb, fl, cards, p, M, s=1.0, hang=True):
    """Persian pierced-brass lantern: a six-sided body of glowing pierced panels (emission), a brass base, an onion cap and finial,
    a ring; returns the flame centre."""
    p = Vector(p)
    rod(mb, p, p + Vector((0, 0, 0.1 * s)), 0.24 * s, M['brass'], seg=6, r1=0.2 * s)
    fl.frustum(p + Vector((0, 0, 0.1 * s)), p + Vector((0, 0, 0.62 * s)), 0.2 * s, 0.23 * s, M['lamp_glass'], seg=6, uv_wrap=(3, 1))
    for k in range(6):
        a = 2 * math.pi * k / 6; rod(mb, p + Vector((0.205 * s * math.cos(a), 0.205 * s * math.sin(a), 0.1 * s)), p + Vector((0.235 * s * math.cos(a), 0.235 * s * math.sin(a), 0.62 * s)), 0.022 * s, M['brass'], seg=4)
    lumpy(mb, p + Vector((0, 0, 0.7 * s)), 0.25 * s, M['brass'], 77, seg=6, rings=4, rough=0.0, squash=0.55)
    rod(mb, p + Vector((0, 0, 0.8 * s)), p + Vector((0, 0, 1.0 * s)), 0.05 * s, M['brass'], seg=6, r1=0.01)
    if hang: chain_rod(mb, [p + Vector((-0.12 * s, 0, 0.9 * s)), p + Vector((0, 0, 1.12 * s)), p + Vector((0.12 * s, 0, 0.9 * s))], 0.012, M['iron'])
    f = p + Vector((0, 0, 0.38 * s)); _halo(cards, f, 0.9 * s, M)
    return f

def _lantern_post(mb, fl, cards, base, M, h=3.4):
    """A wooden pole with an arm and a hanging lantern (along the channel banks)."""
    b = Vector(base); rod(mb, b, b + Vector((0, 0, h)), 0.07, M['wood_d'], seg=6); beam(mb, b + Vector((0, 0, h - 0.1)), b + Vector((0.8, 0, h - 0.1)), 0.08, 0.08, M['wood_d'])
    chain_rod(mb, [b + Vector((0.7, 0, h - 0.15)), b + Vector((0.7, 0, h - 0.55))], 0.012, M['iron'])
    return _lantern(mb, fl, cards, b + Vector((0.7, 0, h - 1.55)), M, s=1.0, hang=False)

def _brazier(mb, fl, cards, base, M, s=1.0):
    """Iron fire bowl on three legs with a crackling fire (flame cones, embers): returns the fire centre."""
    b = Vector(base)
    for k in range(3):
        a = 2 * math.pi * k / 3; rod(mb, b + Vector((0.55 * s * math.cos(a), 0.55 * s * math.sin(a), 0)), b + Vector((0.35 * s * math.cos(a), 0.35 * s * math.sin(a), 0.8 * s)), 0.04 * s, M['iron'], seg=4)
    rod(mb, b + Vector((0, 0, 0.6 * s)), b + Vector((0, 0, 0.95 * s)), 0.25 * s, M['iron'], seg=12, r1=0.55 * s)
    lumpy(fl, b + Vector((0, 0, 0.95 * s)), 0.45 * s, M['ember'], 81, seg=10, rings=4, rough=0.25, squash=0.35)
    r = _rnd(int(b.x * 10 + b.y))
    for k in range(7):
        a = 2 * math.pi * k / 7 + r.uniform(0, 0.5); d = r.uniform(0.05, 0.28) * s; h = r.uniform(0.5, 1.1) * s
        q = b + Vector((d * math.cos(a), d * math.sin(a), 0.95 * s))
        fl.frustum(q, q + Vector((r.uniform(-0.08, 0.08), r.uniform(-0.08, 0.08), h)), r.uniform(0.1, 0.18) * s, 0.0, M['flame'] if k % 3 else M['flame_c'], seg=6, cap1=False)
    for k in range(4): beam(mb, b + Vector((-0.3 * s, (k - 1.5) * 0.12 * s, 1.0 * s)), b + Vector((0.3 * s, (k - 1.5) * 0.14 * s, 1.08 * s)), 0.08 * s, 0.08 * s, M['wood_d'])
    f = b + Vector((0, 0, 1.4 * s)); _halo(cards, f, 1.8 * s, M, key='halo_big')
    return f

def _bucket(mb, base, M, s=1.0, water=False):
    b = Vector(base); rod(mb, b, b + Vector((0, 0, 0.55 * s)), 0.26 * s, M['wood'], seg=10, r1=0.3 * s)
    for z in (0.08, 0.45): rod(mb, b + Vector((0, 0, z * s)), b + Vector((0, 0, (z + 0.05) * s)), (0.27 + 0.05 * z) * s, M['iron'], seg=10)
    chain_rod(mb, [b + Vector((-0.3 * s, 0, 0.55 * s)), b + Vector((0, 0, 0.95 * s)), b + Vector((0.3 * s, 0, 0.55 * s))], 0.015 * s, M['iron'])

def _jar(mb, base, M, h=1.6, r=0.55, mat=None, seed=0, neck=True):
    """Terracotta water jar (khomreh): a swelling body (lathe of rings), short neck and lip; mat defaults to terracotta."""
    b = Vector(base); mat = mat or M['terra']; prof = [(0.0, 0.45), (0.12, 0.7), (0.35, 0.98), (0.58, 1.0), (0.78, 0.8), (0.88, 0.48), (0.93, 0.4), (1.0, 0.5)]
    for (z0, r0), (z1, r1_) in zip(prof, prof[1:]): mb.frustum(b + Vector((0, 0, z0 * h)), b + Vector((0, 0, z1 * h)), r0 * r, r1_ * r, mat, seg=14, cap0=z0 == 0, cap1=False)
    rod(mb, b + Vector((0, 0, h * 0.995)), b + Vector((0, 0, h * 1.0)), 0.5 * r, M['dark'], seg=10)
    rod(mb, b + Vector((0, 0, 0.6 * h)), b + Vector((0, 0, 0.62 * h)), 1.005 * r, M['terra_d'], seg=14)

def _pot(mb, base, M, r=0.4, mat=None):
    """Copper pot: round belly, flared rim (glossy copper)."""
    b = Vector(base); mat = mat or M['copper']
    lumpy(mb, b + Vector((0, 0, r * 0.8)), r, mat, 31, seg=12, rings=6, rough=0.0, squash=0.8); rod(mb, b + Vector((0, 0, r * 1.4)), b + Vector((0, 0, r * 1.7)), r * 0.55, mat, seg=12, r1=r * 0.7)

def _palm(mb, base, M, h=7.0, seed=0):
    """Date palm: a ringed leaning trunk, a crown of drooping fronds (thin bent quads) and date clusters."""
    r = _rnd(seed); b = Vector(base); lean = Vector((r.uniform(-0.4, 0.4), r.uniform(-0.4, 0.4), 0)); pts = [b + lean * (t * t) + Vector((0, 0, h * t)) for t in [k / 8 for k in range(9)]]
    for i, (a, c) in enumerate(zip(pts, pts[1:])): mb.frustum(a, c, 0.32 - 0.015 * i, 0.31 - 0.015 * (i + 1), M['trunk'], seg=8)
    top = pts[-1]
    for k in range(14):
        a = 2 * math.pi * k / 14 + r.uniform(0, 0.3); up = r.uniform(-0.2, 0.6); L_ = r.uniform(3.0, 4.2)
        d = Vector((math.cos(a), math.sin(a), 0)); side = Vector((-math.sin(a), math.cos(a), 0))
        prev = top; mat = M['palm'] if k % 2 else M['palm_d']
        for j in range(1, 6):
            t = j / 5; q = top + d * L_ * t + Vector((0, 0, (up * t - 1.4 * t * t) * L_ * 0.6)); w = 0.55 * math.sin(math.pi * min(1, t + 0.1)) + 0.05
            mb.face([prev - side * w, q - side * w * 0.8, q + side * w * 0.8, prev + side * w], mat); prev = q
    for k in range(3): lumpy(mb, top + Vector((0.4 * math.cos(k * 2.1), 0.4 * math.sin(k * 2.1), -0.6)), 0.35, M['fruit'][2], 600 + k, seg=6, rings=4, rough=0.3, squash=1.3)

def _shrub(mb, c, M, seed, s=1.0):
    r = _rnd(seed)
    for k in range(3): lumpy(mb, Vector(c) + Vector((r.uniform(-0.4, 0.4) * s, r.uniform(-0.4, 0.4) * s, 0.2 * s)), r.uniform(0.3, 0.55) * s, M['shrub'], 700 + seed * 3 + k, seg=8, rings=4, rough=0.35, squash=0.6)

# ============================================================================= DESERT: the plain (channels, wall, dome)
def _ground(SET, M):
    """Desert floor (z 0) round the channel field, the banks between the channels, the trench sides and floors."""
    gb = MB(); x0, x1 = CH_X; ys = [(c - CH_W / 2, c + CH_W / 2) for c in CH_Y]; Rg = 150.0
    def q(a, b, c, d, mat, tile=4.0): gb.quad((a, c, 0), (b - a, 0, 0), (0, d - c, 0), mat, (a / tile, c / tile, b / tile, d / tile))
    q(-Rg, Rg, -Rg, ys[0][0], M['sand']); q(-Rg, Rg, ys[-1][1], Rg, M['sand'])
    q(-Rg, x0, ys[0][0], ys[-1][1], M['sand']); q(x1, Rg, ys[0][0], ys[-1][1], M['sand'])
    for (a, b), (c, d) in zip(ys, ys[1:]): q(x0, x1, b, c, M['bank'])
    _obj(gb, 'ground', SET)
    tb = MB(); zf = CH_Z['floor']
    for (a, b) in ys:
        tb.quad((x0, a, zf), (x1 - x0, 0, 0), (0, b - a, 0), M['trench'], (0, 0, (x1 - x0) / 4, 0.5))
        tb.oface([(x0, a, zf), (x1, a, zf), (x1, a, 0), (x0, a, 0)], M['trench'], [(0, 0), (13, 0), (13, 0.1), (0, 0.1)], (0, 1, 0))
        tb.oface([(x0, b, zf), (x1, b, zf), (x1, b, 0), (x0, b, 0)], M['trench'], [(0, 0), (13, 0), (13, 0.1), (0, 0.1)], (0, -1, 0))
        for x in (x0, x1): tb.oface([(x, a, zf), (x, b, zf), (x, b, 0), (x, a, 0)], M['trench'], [(0, 0), (0.5, 0), (0.5, 0.1), (0, 0.1)], (1 if x == x0 else -1, 0, 0))
    # low raked earth ridges along the bank tops (the lips that hold the water)
    for c in CH_Y:
        for s in (-1, 1):
            y = c + s * (CH_W / 2 + 0.12); tb.box((x0, y - 0.1, 0), (x1, y + 0.1, 0.09), M['bank'], tile=(4, 4))
    _obj(tb, 'trenches', SET)

def _channels(SET, M):
    """The water, ice and mud surfaces of the five channels (set_ice), with the sawn hole in channel 2 (its cut faces show the
    thickness of the ice)."""
    x0, x1 = CH_X; wb = MB(); ib = MB(); mb = MB(); hb = MB()
    for i, c in enumerate(CH_Y):
        a, b = c - CH_W / 2, c + CH_W / 2
        wb.quad((x0, a, CH_Z['water']), (x1 - x0, 0, 0), (0, b - a, 0), M['water'], (0, 0, (x1 - x0) / 4, 1))
        mb.quad((x0, a, CH_Z['mud'] - CH_Z['ice0']), (x1 - x0, 0, 0), (0, b - a, 0), M['mud'], (x0 / 4, 0, x1 / 4, 1))
        if i == 1:                                                # the hole: ice in three pieces round it
            h0, h1 = CUT; m0, m1 = a + 0.3, b - 0.25
            for (u0, u1, v0, v1) in ((x0, h0, a, b), (h1, x1, a, b), (h0, h1, a, m0), (h0, h1, m1, b)):
                ib.quad((u0, v0, 0), (u1 - u0, 0, 0), (0, v1 - v0, 0), M['ice'], (u0 / 4, (v0 - a) / 2, u1 / 4, (v1 - a) / 2))
            for (p0, p1, n) in (((h0, m0), (h1, m0), (0, 1, 0)), ((h1, m1), (h0, m1), (0, -1, 0)), ((h0, m1), (h0, m0), (1, 0, 0)), ((h1, m0), (h1, m1), (-1, 0, 0))):
                hb.oface([(p0[0], p0[1], -1.0), (p1[0], p1[1], -1.0), (p1[0], p1[1], 0), (p0[0], p0[1], 0)], M['ice_block'], [(0, 0), (1, 0), (1, 0.5), (0, 0.5)], n)
        else:
            ib.quad((x0, a, 0), (x1 - x0, 0, 0), (0, b - a, 0), M['ice'], (x0 / 4, 0, x1 / 4, 1))
    _obj(wb, 'water', SET, shadow=False)
    ice = _obj(ib, 'ice', SET); ice.location.z = CH_Z['ice0']
    hole = _obj(hb, 'ice_cut_faces', SET); hole.location.z = CH_Z['ice0']; hole.scale.z = 0.02
    mud = _obj(mb, 'mud', SET); mud.location.z = CH_Z['ice0']
    STATE['ice'] = dict(ice=ice, hole=hole, mud=mud, water=wb)

def _wall(SET, M):
    """The shade wall: 60 D long, 15 D (3 storeys) high, battered (1.6 D thick at the foot, 0.9 at the top), mud-brick with pilaster
    strips on the north face, a stepped crenel crest, putlog holes, a mud ramp-stair up the west end and a ladder."""
    (xa, xb), (ya, yb), H = WALL['x'], WALL['y'], WALL['h']; mb = MB(); t = 0.7          # batter: the north face leans in by t
    N0, N1 = Vector((xa, yb, 0)), Vector((xb, yb, 0))
    def nf(x, z): return Vector((x, yb - t * z / H, z))
    L_ = xb - xa
    mb.oface([nf(xa, 0), nf(xb, 0), nf(xb, H), nf(xa, H)], M['mudbrick'], [(0, 0), (L_ / 4, 0), (L_ / 4, H / 4), (0, H / 4)], (0, 1, 0.05))
    mb.oface([(xa, ya, 0), (xb, ya, 0), (xb, ya + 0.2, H), (xa, ya + 0.2, H)], M['mudbrick_d'], [(0, 0), (L_ / 4, 0), (L_ / 4, H / 4), (0, H / 4)], (0, -1, 0.05))
    for x in (xa, xb): mb.oface([(x, ya, 0), (x, yb, 0), (x, yb - t, H), (x, ya + 0.2, H)], M['mudbrick'], [(0, 0), (0.4, 0), (0.4, H / 4), (0, H / 4)], (1 if x == xb else -1, 0, 0))
    mb.oface([(xa, ya + 0.2, H), (xb, ya + 0.2, H), (xb, yb - t, H), (xa, yb - t, H)], M['kahgel'], [(0, 0), (L_ / 4, 0), (L_ / 4, 0.2), (0, 0.2)], (0, 0, 1))
    # pilaster strips and the stepped crest
    x = xa + 3.0
    while x < xb - 2:
        p0 = nf(x - 0.45, 0); mb.box((x - 0.45, yb - 0.02 - t * 0.0, 0), (x + 0.45, yb + 0.35, 0.8), M['mudbrick'], tile=(4, 4))
        for z0, z1 in ((0.8, 5.0), (5.0, 10.0), (10.0, H)):
            obox(mb, (x, yb - t * (z0 + z1) / 2 / H + 0.12, (z0 + z1) / 2), (1, 0, 0), (0, 1, 0), (0, -t / H, 1), 0.42, 0.14, (z1 - z0) / 2, M['mudbrick'], 0.25)
        x += 6.0
    for k in range(int(L_ / 1.5)):                               # crest: stepped merlons
        cx = xa + 0.75 + 1.5 * k; yy = (ya + 0.2 + yb - t) / 2
        mb.box((cx - 0.5, yy - 0.42, H), (cx + 0.5, yy + 0.42, H + 0.7), M['kahgel'], tile=(4, 4)); mb.box((cx - 0.3, yy - 0.3, H + 0.7), (cx + 0.3, yy + 0.3, H + 1.1), M['kahgel'], tile=(4, 4))
    for z in (4.6, 9.6):                                         # storey ledges (wooden beam ends)
        for k in range(int(L_ / 2.0)):
            p = nf(xa + 1 + 2 * k, z); beam(mb, p - Vector((0, 0.05, 0)), p + Vector((0, 0.35, 0)), 0.16, 0.16, M['wood_d'])
    _obj(mb, 'wall', SET, hull=0.02)
    # ramp-stair at the west end (north side) and a ladder
    st = MB()
    for k in range(10):
        z = 0.5 * (k + 1); st.box((xa + 0.2 + k * 0.9, yb, 0), (xa + 1.1 + k * 0.9, yb + 1.6, z), M['mudbrick'], tile=(4, 4))
    _obj(st, 'wall_stair', SET, hull=0.02)

def _dome(SET, M, interior_glow=True):
    """The yakhchal: a stepped conical mud dome (R 12.5 at the foot, 27 D high, 13 steps), a chimney cap, a buttressed base ring, and
    the small arched entrance porch facing the channels (its door glows warm at night - the lantern inside)."""
    cx, cy = DOME['c']; R, H, n = DOME['R'], DOME['H'], DOME['steps']; seg = 64; mb = MB()
    def rr(z): return R * (1 - z / (H + 1.2)) ** 0.82
    zs = [H * (k / n) ** 1.08 for k in range(n + 1)]
    for k in range(n):
        z0, z1 = zs[k], zs[k + 1]; r0, r1 = rr(z0), rr(z1); rs = r0 - (r0 - r1) * 0.35
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
            P_ = lambda r, z, c, s: Vector((cx + r * c, cy + r * s, z))
            u0, u1 = i / seg * 2 * math.pi * r0 / 4, (i + 1) / seg * 2 * math.pi * r0 / 4
            mb.face([P_(r0, z0, c0, s0), P_(r0, z0, c1, s1), P_(rs, z1, c1, s1), P_(rs, z1, c0, s0)], M['kahgel'], [(u0, z0 / 4), (u1, z0 / 4), (u1, z1 / 4), (u0, z1 / 4)])
            mb.face([P_(rs, z1, c0, s0), P_(rs, z1, c1, s1), P_(r1, z1, c1, s1), P_(r1, z1, c0, s0)], M['kahgel'], [(u0, z1 / 4), (u1, z1 / 4), (u1, z1 / 4 + 0.1), (u0, z1 / 4 + 0.1)])
    top = Vector((cx, cy, zs[-1])); rt = rr(zs[-1])
    rod(mb, top, top + Vector((0, 0, 1.6)), rt, M['kahgel'], seg=24, r1=rt * 0.8)
    _obj(mb, 'dome', SET, hull=0.03)
    vb = MB(); rod(vb, top + Vector((0, 0, 1.55)), top + Vector((0, 0, 1.62)), rt * 0.6, M['door_dark'], seg=20); _obj(vb, 'dome_vent', SET, shadow=False)
    # base ring (a low buttressed plinth) and the entrance porch facing -x
    bb = MB()
    for i in range(24):
        a = 2 * math.pi * i / 24; p = Vector((cx + (R + 0.3) * math.cos(a), cy + (R + 0.3) * math.sin(a), 0))
        if math.cos(a) < -0.95: continue
        obox(bb, p + Vector((0, 0, 1.0)), (math.cos(a), math.sin(a), 0), (-math.sin(a), math.cos(a), 0), (0, 0, 1), 0.8, 0.7, 1.0, M['mudbrick'], 0.25)
    F = Frame((cx - R + 0.6, cy, 0), -90.0)            # porch: local x along the face (+y world), -y local = facing -x world
    w, d, hh = 3.4, 3.2, 5.0
    F.box(bb, (-w / 2 - 0.6, -d, 0), (-w / 2, 0.5, hh), M['mudbrick']); F.box(bb, (w / 2, -d, 0), (w / 2 + 0.6, 0.5, hh), M['mudbrick'])
    F.box(bb, (-w / 2 - 0.6, -d, hh - 1.2), (w / 2 + 0.6, 0.5, hh + 0.6), M['mudbrick'])
    F2 = Frame(F.p(0, -d, 0), -90.0)                    # the porch front: a wall with a pointed arch, the warm-lit passage behind
    _arch_face(bb, F2, -w / 2 - 0.6, w / 2 + 0.6, 0.0, hh + 0.6, 0.0, 1.8, 2.3, M['mudbrick'], M['kahgel'], depth=0.6, inner=(M['door_glow'] if interior_glow else M['door_dark'], 1.2))
    _obj(bb, 'dome_base', SET, hull=0.02)
    door = F.p(0, -d - 0.6, 0); STATE['marks']['dome_door'] = tuple(round(v, 3) for v in (door.x - 0.8, door.y + 1.2, 0.0))
    return F.p(0, -d - 0.3, 2.4)

def _qanat(SET, M):
    """The qanat outlet at the west end: a mud arch over the inflow, the feeder ditch along x -27.5 to the channel heads, a little
    wooden sluice per channel, and the line of qanat shaft mounds (rings of spoil) marching away west-north-west."""
    mb = MB(); x = CH_X[0] - 1.5
    mb.box((x - 0.5, 0.6, -0.2), (x + 0.5, CH_Y[-1] + 1.4, 0.02), M['trench'])
    for c in CH_Y: beam(mb, (CH_X[0] - 0.05, c - 1.1, 0.5), (CH_X[0] - 0.05, c + 1.1, 0.5), 0.12, 0.12, M['wood_d']); rod(mb, (CH_X[0] - 0.05, c - 1.0, 0), (CH_X[0] - 0.05, c - 1.0, 0.7), 0.06, M['wood_d'])
    F = Frame((x - 1.6, CH_Y[-1] + 2.5, 0), 180.0)
    F.box(mb, (-1.2, -0.6, 0), (-0.8, 0.6, 1.8), M['mudbrick']); F.box(mb, (0.8, -0.6, 0), (1.2, 0.6, 1.8), M['mudbrick']); F.box(mb, (-1.2, -0.6, 1.8), (1.2, 0.6, 2.4), M['mudbrick'])
    F.quad(mb, [(-0.8, -0.61, 0), (0.8, -0.61, 0), (0.8, -0.61, 1.8), (-0.8, -0.61, 1.8)], M['door_dark'], [(0, 0)] * 4, (0, -1, 0))
    r = _rnd(5)
    for k in range(12):
        c = Vector((x - 8 - k * 9.0, CH_Y[-1] + 6 + k * 3.2 + r.uniform(-1, 1), 0)); R_ = 1.6 + r.uniform(-0.2, 0.4)
        lumpy(mb, c, R_, M['sand_d'], 400 + k, seg=14, rings=5, rough=0.12, squash=0.32)
        rod(mb, c + Vector((0, 0, 0.2)), c + Vector((0, 0, 0.55)), 0.45, M['door_dark'], seg=10)
    _obj(mb, 'qanat', SET, hull=0.02)

def _camp(SET, M):
    """Farid's camp by the west end of the wall: a reed lean-to on poles, the brazier fire, buckets, the ice saw and pick, three
    cut blocks on a straw mat, a wooden sledge, lantern posts along the banks (warm practicals), palms and shrubs at the qanat."""
    mb = MB(); fl = MB(); cards = MB(); lamps = []
    # lean-to against the wall (north face, x -24..-19)
    x0, x1 = -25.5, -20.5; yw = WALL['y'][1] - 0.3; yo = yw + 3.2
    for x in (x0, (x0 + x1) / 2, x1): rod(mb, (x, yo, 0), (x, yo, 2.6), 0.07, M['wood_d'], seg=6); beam(mb, (x, yo, 2.6), (x, yw, 3.6), 0.08, 0.08, M['wood_d'])
    mb.oface([(x0 - 0.3, yo + 0.3, 2.5), (x1 + 0.3, yo + 0.3, 2.5), (x1 + 0.3, yw, 3.7), (x0 - 0.3, yw, 3.7)], M['mat'], [(0, 0), (3, 0), (3, 2), (0, 2)], (0, 1, 1))
    mb.box((x0 + 0.3, yw + 0.3, 0), (x0 + 2.4, yw + 1.6, 0.25), M['kilim'][0])
    f = _brazier(mb, fl, cards, (-18.4, 0.0, 0), M)
    lamps.append(('fire', f, 220.0, FIRE, True))
    for (x, y) in ((-16.6, -0.1), (-16.0, 0.3)): _bucket(mb, (x, y, 0), M)
    beam(mb, (-17.4, 0.5, 0.05), (-15.6, 0.15, 0.05), 0.5, 0.06, M['iron'])                          # the ice saw blade + handle
    beam(mb, (-17.6, 0.55, 0.05), (-17.3, 0.5, 0.05), 0.12, 0.25, M['wood'])
    rod(mb, (-14.8, -0.2, 0.05), (-13.2, 0.4, 0.3), 0.05, M['wood']); beam(mb, (-13.4, 0.15, 0.35), (-13.0, 0.75, 0.1), 0.08, 0.08, M['iron'])
    mb.box((-12.6, -0.4, 0), (-9.4, 0.5, 0.04), M['mat'], tile=(2, 2))
    for k, (x, z) in enumerate(((-12.3, 0.04), (-11.0, 0.04), (-11.7, 0.84))): mb.box((x, -0.25, z), (x + 1.2, 0.35, z + 0.8), M['ice_block'])
    for s in (-0.45, 0.45): beam(mb, (-8.6, 0.0 + s, 0.12), (-6.2, 0.0 + s, 0.12), 0.12, 0.16, M['wood']); beam(mb, (-6.2, s, 0.12), (-5.9, s, 0.35), 0.12, 0.12, M['wood'])
    for k in range(4): beam(mb, (-8.4 + 0.6 * k, -0.6, 0.27), (-8.4 + 0.6 * k, 0.6, 0.27), 0.18, 0.06, M['wood_l'])
    # lantern posts on the banks (between the channels), going into depth
    for (x, i) in ((-20.0, 0), (-9.0, 2), (2.0, 1), (12.0, 3), (22.0, 0)):
        y = (CH_Y[i] + CH_Y[i + 1]) / 2 if i < 4 else CH_Y[-1] + 1.6
        lamps.append(('lamp', _lantern_post(mb, fl, cards, (x, y, 0), M), 50.0, LAMP, False))
    # a lantern on the ground by the cut hole and one at the dome door
    lamps.append(('lamp', _lantern(mb, fl, cards, (CUT[1] + 0.6, CH_Y[1] + CH_W / 2 + 0.55, 0.0), M, s=0.9, hang=False), 22.0, LAMP, True))
    STATE['lamp_specs'] = lamps
    r = _rnd(9)
    for k, (x, y) in enumerate(((-38, 24), (-42.5, 21.5), (-36.5, 28), (-46, 14), (44, 25), (52, -6))): _palm(mb, (x, y, 0), M, h=r.uniform(6.5, 8.5), seed=k)
    for k in range(40):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(30, 70); c = (d * math.cos(a), d * math.sin(a), 0)
        if abs(c[0] - DOME['c'][0]) < 15 and abs(c[1] - DOME['c'][1]) < 15: continue
        _shrub(mb, c, M, k, s=r.uniform(0.7, 1.3))
    for k in range(30):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(20, 60); lumpy(mb, (d * math.cos(a), d * math.sin(a), 0.1), r.uniform(0.2, 0.6), M['rock'], 800 + k, seg=8, rings=4, rough=0.3, squash=0.6)
    _obj(mb, 'camp', SET, hull=0.015); _obj(fl, 'camp_glow', SET, shadow=False); _obj(cards, 'camp_halos', SET, shadow=False)
    STATE['marks'].update(farid_camp=(-18.4, 1.6, 0.0), farid_cut=(CUT[0] - 0.2, CH_Y[1] + CH_W / 2 + 0.5, 0.0), farid_pour=(-6.0, (CH_Y[2] + CH_Y[3]) / 2, 0.0),
                          merchant_watch=(-12.0, CH_Y[-1] + 4.0, 0.0), townsfolk=[(-14.5, CH_Y[-1] + 3.4, 0.0), (-9.5, CH_Y[-1] + 4.6, 0.0)],
                          wall_foot=(4.0, 0.25, 0.0), bank_lanes=[round((a + b) / 2, 3) for a, b in zip(CH_Y, CH_Y[1:])])

def _wisps(SET, M):
    """Heat wisps (set_heat_wisps): crossed camera-only cards over the channels, 2.4 x 26 D, scrolling up, faded at both ends."""
    wb = MB(); r = _rnd(17)
    for i, c in enumerate(CH_Y):
        for k in range(6):
            x = CH_X[0] + 3 + k * 8.4 + r.uniform(-1.5, 1.5); y = c + r.uniform(-0.4, 0.4); h = r.uniform(14, 22); w = 1.6; u0 = r.uniform(0, 1)
            for (dx, dy) in ((1, 0), (0, 1)):
                wb.face([(x - dx * w / 2, y - dy * w / 2, -0.05), (x + dx * w / 2, y + dy * w / 2, -0.05), (x + dx * w / 2, y + dy * w / 2, h), (x - dx * w / 2, y - dy * w / 2, h)], M['wisp'], [(u0, 0), (u0 + 0.8, 0), (u0 + 0.8, 1), (u0, 1)])
    o = _obj(wb, 'heat_wisps', SET, shadow=False); STATE['wisps'] = o

def _plain_lights(SET, P, M):
    for i, (kind, f, e, rgb, sh) in enumerate(STATE.get('lamp_specs', [])):
        _flame_light('%s_%d' % (kind, i), tuple(f), rgb, e * (P['lamps'] if kind != 'fire' else max(0.4, P['lamps'])), radius=0.3 if kind == 'fire' else 0.15, shadow=sh)
    if 'door_light' in STATE: _flame_light('dome_door', STATE['door_light'], LAMP, 60.0 * P['lamps'], radius=0.4)

def _plain(SET, P, M, dress):
    _ground(SET, M); _channels(SET, M); _wall(SET, M)
    STATE['door_light'] = tuple(_dome(SET, M, interior_glow=P['lamps'] > 0.5))
    _qanat(SET, M)
    if dress: _camp(SET, M)
    _wisps(SET, M); _plain_lights(SET, P, M); _sky(SET, P, M)

# ============================================================================= DESERT: inside the dome
def _dome_in(SET, P, M, dress):
    """Inside the yakhchal: the corbelled inner cone (mud-brick rings) rising to the oculus, the walkway ring (z 0) round the ice pit
    (r 9, 6 D deep) stacked with sawn ice blocks in straw-separated layers, the arched door with the night outside, a lantern on the
    walkway, a ladder down into the pit; the moon (or the sun) through the oculus lays a shaft on the ice."""
    R0, H = 11.6, 25.0; seg = 56; mb = MB(); fl = MB(); cards = MB()
    def rr(z): return R0 * (1 - z / (H + 0.6)) ** 0.85
    zs = [H * k / 22 for k in range(23)]; ocu = rr(H)
    for k in range(22):
        z0, z1 = zs[k], zs[k + 1]
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
            p = [Vector((rr(z) * math.cos(a), rr(z) * math.sin(a), z)) for (a, z) in ((a0, z0), (a1, z0), (a1, z1), (a0, z1))]
            mb.face(p[::-1], M['kahgel_in'] if k % 3 else M['mudbrick_d'], [(i / seg * 9, z0 / 3), ((i + 1) / seg * 9, z0 / 3), ((i + 1) / seg * 9, z1 / 3), (i / seg * 9, z1 / 3)][::-1])
    # walkway ring and the pit
    wr0, wr1 = PIT['walk']; zp = PIT['z']
    for i in range(seg):
        a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg
        c0, s0, c1, s1 = math.cos(a0), math.sin(a0), math.cos(a1), math.sin(a1)
        mb.face([(wr0 * c0, wr0 * s0, 0), (wr0 * c1, wr0 * s1, 0), (wr1 * c1, wr1 * s1, 0), (wr1 * c0, wr1 * s0, 0)], M['path'], [(c0 * 3, s0 * 3), (c1 * 3, s1 * 3), (c1 * 3.6, s1 * 3.6), (c0 * 3.6, s0 * 3.6)])
        mb.face([(wr0 * c0, wr0 * s0, zp), (wr0 * c1, wr0 * s1, zp), (wr0 * c1, wr0 * s1, 0), (wr0 * c0, wr0 * s0, 0)], M['mudbrick_d'], [(i / seg * 14, 0), ((i + 1) / seg * 14, 0), ((i + 1) / seg * 14, 1.5), (i / seg * 14, 1.5)])
        mb.face([(wr1 * c0, wr1 * s0, -0.01), (wr1 * c1, wr1 * s1, -0.01), (R0 * c1, R0 * s1, 0.0), (R0 * c0, R0 * s0, 0.0)], M['path'])
    _obj(mb, 'dome_inner', SET)
    # the ice stack: a solid mass of blocks to z -1.6 (block faces on its side), then a top layer of separate blocks, part cut away
    ib = MB(); r = _rnd(41); top = -1.6; bw, bd, bh = 1.6, 1.0, 0.8
    nseg = 40
    for i in range(nseg):
        a0, a1 = 2 * math.pi * i / nseg, 2 * math.pi * (i + 1) / nseg; rr_ = PIT['r'] - 0.25
        ib.face([(rr_ * math.cos(a0), rr_ * math.sin(a0), zp), (rr_ * math.cos(a1), rr_ * math.sin(a1), zp), (rr_ * math.cos(a1), rr_ * math.sin(a1), top), (rr_ * math.cos(a0), rr_ * math.sin(a0), top)], M['ice_block'],
                [(i * 0.8, 0), ((i + 1) * 0.8, 0), ((i + 1) * 0.8, 2.2), (i * 0.8, 2.2)])
    ib.face([(PIT['r'] * math.cos(2 * math.pi * i / nseg) * 0.97, PIT['r'] * math.sin(2 * math.pi * i / nseg) * 0.97, top) for i in range(nseg)], M['mat'], [(0.5 + 0.5 * math.cos(2 * math.pi * i / nseg) * 4, 0.5 + 0.5 * math.sin(2 * math.pi * i / nseg) * 4) for i in range(nseg)])
    for gx in range(-6, 6):
        for gy in range(-9, 9):
            x, y = gx * (bw + 0.08) + 0.3, gy * (bd + 0.08)
            if math.hypot(x + bw / 2, y + bd / 2) > PIT['r'] - 1.0: continue
            if (x > 2.5 and y < -1.0 and r.random() < 0.85): continue                  # the corner already taken out
            hh = bh * r.uniform(0.95, 1.05); ib.box((x, y, top), (x + bw, y + bd, top + hh), M['ice_block'], tile=(2, 2))
            if r.random() < 0.18 and x < 1: ib.box((x + 0.1, y + 0.05, top + hh), (x + bw - 0.1, y + bd - 0.05, top + hh + bh), M['ice_block'], tile=(2, 2))
    for k in range(5): ib.box((-0.2 + k * 0.3, -0.6 - k * 0.2, top + bh), (0.9 + k * 0.3, -0.1 - k * 0.2, top + bh + 0.05), M['straw'])
    _obj(ib, 'ice_stack', SET, hull=0.012)
    # door (west, -x) with the night outside, a ladder, the lantern, a sledge and blocks on the walkway
    d = MB(); F = Frame((-R0 + 0.05, 0.0, 0), 90.0)        # local -y = into the room (+x)
    ar = [(0.95 * math.cos(math.pi * (1 - k / 12)), 2.6 + 1.3 * math.sin(math.pi * (1 - k / 12)) ** 0.8 + 0.35 * (1 - abs(2 * k / 12 - 1)) ** 4) for k in range(13)]
    sky_door = mat_emit(STATE['pre'] + 'e_doorsky', image=STATE['tx']['sky_' + P['sky']], strength=P['sky_k'] * 0.9)
    F.quad(d, [(-0.95, 0.3, 0)] + [(x, 0.3, z) for x, z in ar] + [(0.95, 0.3, 0)], sky_door, [(0.62, 0.15)] + [(0.62 + x * 0.01, 0.15 + z * 0.012) for x, z in ar] + [(0.63, 0.15)], (0, -1, 0))
    for s in (-1, 1): F.box(d, (s * 0.95 - (0.25 if s > 0 else -0.0) - (0 if s > 0 else 0.25), -0.3, 0), (s * 0.95 + (0.0 if s > 0 else 0.0) + (0.25 if s > 0 else 0), 0.3, 3.9), M['mudbrick'])
    for s in (-0.5, 0.5): beam(d, (wr0 * 0.98 * math.cos(0.5), wr0 * 0.98 * math.sin(0.5) + s, 0.4), (PIT['r'] * 0.84 * math.cos(0.5), PIT['r'] * 0.84 * math.sin(0.5) + s, top + 0.9), 0.1, 0.1, M['wood'])
    for k in range(1, 8):
        t = k / 8; a = Vector((wr0 * 0.98 * math.cos(0.5), wr0 * 0.98 * math.sin(0.5), 0.4)).lerp(Vector((PIT['r'] * 0.84 * math.cos(0.5), PIT['r'] * 0.84 * math.sin(0.5), top + 0.9)), t)
        rod(d, a - Vector((0, 0.5, 0)), a + Vector((0, 0.5, 0)), 0.04, M['wood'])
    lp = _lantern(d, fl, cards, (-5.6, 0.9, -0.8), M, s=1.0, hang=False)
    lp2 = _lantern(d, fl, cards, (9.9, 3.5, 0.0), M, s=0.9, hang=False)
    for s in (-0.4, 0.4): beam(d, (-9.6, -5.0 + s, 0.12), (-8.0, -6.1 + s, 0.12), 0.1, 0.14, M['wood'])
    d.box((-9.3, -5.9, 0.2), (-8.3, -5.1, 0.95), M['ice_block']); d.box((-10.6, 1.8, 0), (-9.5, 2.6, 0.8), M['ice_block']); d.box((-10.5, 1.9, 0.8), (-9.6, 2.5, 1.5), M['ice_block'])
    _bucket(d, (-10.2, -1.8, 0), M); beam(d, (-10.4, 3.6, 0.04), (-9.0, 3.4, 0.04), 0.45, 0.05, M['iron'])
    _obj(d, 'dome_in_dressing', SET, hull=0.012); _obj(fl, 'dome_in_glow', SET, shadow=False); _obj(cards, 'dome_in_halos', SET, shadow=False)
    _flame_light('lantern_0', tuple(lp), (1.0, 0.66, 0.3), 150.0, radius=0.15, shadow=True); _flame_light('lantern_1', tuple(lp2), (1.0, 0.66, 0.3), 70.0, radius=0.15, shadow=False)
    BK._light('door_fill', (-R0 + 1.5, 0.0, 2.6), tuple(c / max(P['key']) for c in P['key']), 60.0 * (0.6 if P['night'] else 2.0), radius=1.2, shadow=False)
    BK._light('oculus_fill', (0.0, 0.0, 19.0), (0.62, 0.8, 1.0) if P['night'] else (1.0, 0.95, 0.62), 2600.0 if P['night'] else 3200.0, radius=2.0, shadow=False)
    lp3 = _lantern(d, fl, cards, (-1.8, -6.6, -0.8), M, s=0.9, hang=False); _flame_light('lantern_2', tuple(lp3), (1.0, 0.66, 0.3), 90.0, radius=0.15, shadow=False)
    # the shaft from the oculus (camera-only card) along the key direction, and the sky disc seen through the oculus
    kd = Vector(P['key_dir']).normalized(); sb = MB(); o = Vector((0, 0, H))
    if kd.z < -0.3:
        t = (o.z - top) / -kd.z; q = o + kd * t; side = kd.cross(Vector((0, 0, 1))).normalized() * ocu * 1.1
        sb.face([o - side, o + side, q + side, q - side], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        _obj(sb, 'oculus_shaft', SET, shadow=False)
    ob = MB(); ob.face([Vector((ocu * math.cos(2 * math.pi * i / 16), ocu * math.sin(2 * math.pi * i / 16), H + 0.5)) for i in range(16)], M['sky'], [(0.3 + 0.004 * math.cos(2 * math.pi * i / 16), 0.95 + 0.01 * math.sin(2 * math.pi * i / 16)) for i in range(16)])
    _obj(ob, 'oculus_sky', SET, shadow=False)
    STATE['marks'].update(farid_walk=(-9.6, -2.4, 0.0), farid_pit=(-1.5, 2.0, top + 0.8), farid_on_ice=(-4.2, -0.9, top + 0.8), merchant_on_ice=(-2.6, 2.4, top + 0.8), merchant_walk=(-9.8, 2.6, 0.0), lantern=tuple(round(v, 3) for v in lp))

# ============================================================================= BAZAAR
def _arch_pts(cx, w, spring, rise=None, n=12):
    """Two-centred pointed arch from (cx - w/2, spring) to (cx + w/2, spring) through the apex: list of (u, z)."""
    rr = w * 0.68; h0 = w / 2; apex = math.sqrt(rr * rr - (rr - h0) ** 2); out = []
    for k in range(n + 1):
        t = k / n
        if t <= 0.5: c = cx - h0 + rr; a0 = math.pi; a1 = math.acos((cx - c) / rr); a = a0 + (a1 - a0) * (t / 0.5); out.append((c + rr * math.cos(a), spring + rr * abs(math.sin(a))))
        else: c = cx + h0 - rr; a0 = math.acos((cx - c) / rr); a1 = 0.0; a = a0 + (a1 - a0) * ((t - 0.5) / 0.5); out.append((c + rr * math.cos(a), spring + rr * abs(math.sin(a))))
    return out, apex

def _arch_face(mb, F, u0, u1, z0, z1, cx, w, spring, wall_mat, span_mat, depth=0.6, soffit=None, frame_mat=None, inner=None):
    """A wall panel (local x u0..u1, z z0..z1, front at y 0) pierced by a pointed arch (centre cx, width w, springing z): piers, the
    spandrel polygon (span_mat, tiled) under a rectangular frame (alfiz), wall above, the soffit strips `depth` deep."""
    arc, apex = _arch_pts(cx, w, spring); a, b = cx - w / 2, cx + w / 2; ztop = min(z1, spring + apex + 0.35)
    def uv(u, z, s=2.0): return (u / s, z / s)
    F.quad(mb, [(u0, 0, z0), (a, 0, z0), (a, 0, ztop), (u0, 0, ztop)], wall_mat, [uv(u0, z0, 4), uv(a, z0, 4), uv(a, ztop, 4), uv(u0, ztop, 4)], (0, -1, 0))
    F.quad(mb, [(b, 0, z0), (u1, 0, z0), (u1, 0, ztop), (b, 0, ztop)], wall_mat, [uv(b, z0, 4), uv(u1, z0, 4), uv(u1, ztop, 4), uv(b, ztop, 4)], (0, -1, 0))
    pts = [(a, 0, spring)] + [(u, 0, z) for u, z in arc] + [(b, 0, spring), (b, 0, ztop), (a, 0, ztop)]
    F.quad(mb, pts, span_mat, [uv(p[0], p[2]) for p in pts], (0, -1, 0))
    if ztop < z1: F.quad(mb, [(u0, 0, ztop), (u1, 0, ztop), (u1, 0, z1), (u0, 0, z1)], wall_mat, [uv(u0, ztop, 4), uv(u1, ztop, 4), uv(u1, z1, 4), uv(u0, z1, 4)], (0, -1, 0))
    sm = soffit or wall_mat
    for x in (a, b): F.quad(mb, [(x, 0, z0), (x, depth, z0), (x, depth, spring), (x, 0, spring)], sm, [(0, 0), (depth / 2, 0), (depth / 2, spring / 2), (0, spring / 2)], (1 if x == a else -1, 0, 0))
    for (p, q) in zip(arc, arc[1:]): F.quad(mb, [(p[0], 0, p[1]), (q[0], 0, q[1]), (q[0], depth, q[1]), (p[0], depth, p[1])], sm, [(0, 0), (0.3, 0), (0.3, depth / 2), (0, depth / 2)], (0, 0, -1))
    if frame_mat is not None:                                   # the alfiz: a thin turquoise frame round the spandrels
        for (lo, hi) in (((a - 0.14, -0.06, z0), (a, 0.0, ztop)), ((b, -0.06, z0), (b + 0.14, 0.0, ztop)), ((a - 0.14, -0.06, ztop - 0.02), (b + 0.14, 0.0, ztop + 0.12))):
            F.box(mb, lo, hi, frame_mat)
    if inner is not None:                                       # the back of the niche (lit goods wall), sized to the arch
        F.quad(mb, [(a - 0.1, depth + inner[1], z0), (b + 0.1, depth + inner[1], z0), (b + 0.1, depth + inner[1], spring + apex), (a - 0.1, depth + inner[1], spring + apex)], inner[0], [(0, 0), (1, 0), (1, (spring + apex) / 3.6), (0, (spring + apex) / 3.6)], (0, -1, 0))
    return arc, apex

def _shop_module(SET, mb, gm, F, u0, M, r, row, k, merchant=False):
    """One bazaar shop bay (4.5 D) in frame F (front y 0, the street at -y): the ground arch onto the lamp-lit niche (raised floor,
    goods wall), the upper storey with a lattice window niche, tile band, kufic band, crest; goods out front (random by seed)."""
    W = STREET['mod']; H = STREET['H']; u1 = u0 + W; cx = u0 + W / 2
    bg = M['shops'][(k + row) % 4]
    _arch_face(mb, F, u0, u1, 0.0, 5.0, cx, 3.3, 2.9, M['pbrick'], M['tile_panel'] if (k + row) % 2 else M['tile_panel_l'], depth=0.7, soffit=M['pbrick_l'], frame_mat=M['tq'], inner=(bg, 3.0))
    # niche box behind the arch (side walls dark, floor raised 0.8, ceiling)
    a, b = cx - 1.75, cx + 1.75
    F.box(mb, (a, 0.7, 0), (b, 3.7, 0.8), M['planks']); F.quad(mb, [(a, 0.7, 4.9), (b, 0.7, 4.9), (b, 3.7, 4.9), (a, 3.7, 4.9)], M['dark'], [(0, 0)] * 4, (0, 0, -1))
    for x in (a, b): F.quad(mb, [(x, 0.7, 0), (x, 3.7, 0), (x, 3.7, 4.9), (x, 0.7, 4.9)], M['pbrick_l'], [(0, 0), (1, 0), (1, 1.2), (0, 1.2)], (1 if x == a else -1, 0, 0))
    F.quad(mb, [(u0, 0, 5.0), (u1, 0, 5.0), (u1, 0, 5.6), (u0, 0, 5.6)], M['tile_band'], [(u0 / 4, 0), (u1 / 4, 0), (u1 / 4, 1), (u0 / 4, 1)], (0, -1, 0))
    F.box(mb, (u0, -0.25, 5.0), (u1, 0.0, 5.08), M['cream'])
    # upper storey: a smaller arched window niche with a lattice and a little balcony
    arc, apex = _arch_face(mb, F, u0, u1, 5.6, H - 1.1, cx, 1.8, 7.2, M['pbrick'], M['tile_panel_l'] if (k + row) % 2 else M['tile_panel'], depth=0.45, soffit=M['pbrick_l'], frame_mat=M['tq'])
    F.quad(mb, [(cx - 0.9, 0.45, 5.6), (cx + 0.9, 0.45, 5.6), (cx + 0.9, 0.45, 7.2 + apex), (cx - 0.9, 0.45, 7.2 + apex)], M['dark'], [(0, 0)] * 4, (0, -1, 0))
    F.quad(gm, [(cx - 0.9, 0.3, 5.6), (cx + 0.9, 0.3, 5.6), (cx + 0.9, 0.3, 7.6), (cx - 0.9, 0.3, 7.6)], M['lattice'], [(0, 0), (1.8, 0), (1.8, 2), (0, 2)], (0, -1, 0))
    F.box(mb, (cx - 1.2, -0.5, 5.6), (cx + 1.2, 0.0, 5.75), M['wood_d'])
    F.quad(mb, [(u0, 0, H - 1.1), (u1, 0, H - 1.1), (u1, 0, H - 0.5), (u0, 0, H - 0.5)], M['kufic'], [(u0 / 4, 0), (u1 / 4, 0), (u1 / 4, 1), (u0 / 4, 1)], (0, -1, 0))
    F.quad(mb, [(u0, 0, H - 0.5), (u1, 0, H - 0.5), (u1, 0, H), (u0, 0, H)], M['pbrick'], [(0, 0), (1, 0), (1, 0.1), (0, 0.1)], (0, -1, 0))
    F.box(mb, (u0, -0.3, H), (u1, 4.0, H + 0.2), M['cream'])
    for j in range(3): F.box(mb, (u0 + 0.3 + j * 1.5, -0.2, H + 0.2), (u0 + 1.1 + j * 1.5, 0.2, H + 0.9), M['pbrick'])
    if merchant: return
    # awning on two poles over the goods
    aw = M['awn'][(k * 3 + row + r.randrange(2)) % 4]
    F.quad(gm, [(cx - 1.7, -0.05, 4.7), (cx + 1.7, -0.05, 4.7), (cx + 1.7, -2.0, 3.9), (cx - 1.7, -2.0, 3.9)], aw, [(0, 0), (2, 0), (2, 1), (0, 1)], (0, -1, 1))
    for s in (-1, 1): rod(mb, F.p(cx + s * 1.6, -1.95, 0), F.p(cx + s * 1.6, -1.95, 3.95), 0.05, M['wood_d'], seg=5)
    kind = r.choice(('carpet', 'copper', 'jars', 'spice', 'fruit', 'carpet', 'copper', 'spice'))
    if kind == 'carpet':
        for j in range(r.randint(1, 2)):
            cm = M['carpets'][r.randrange(6)]; x0 = u0 + 0.05 + j * 0.05 if j == 0 else u1 - 1.65
            F.quad(mb, [(x0, -0.06 - 0.02 * j, 0.6), (x0 + 1.55, -0.06 - 0.02 * j, 0.6), (x0 + 1.55, -0.06 - 0.02 * j, 3.0), (x0, -0.06 - 0.02 * j, 3.0)], cm, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        for j in range(r.randint(3, 6)):
            c = M['carpets'][r.randrange(6)]; h = 0.14; F.box(mb, (cx - 1.0 + r.uniform(-0.1, 0.1), -1.9, j * h), (cx + 1.0 + r.uniform(-0.1, 0.1), -0.6, (j + 1) * h), c)
    elif kind == 'copper':
        for j in range(5): _pot(mb, F.p(cx - 1.6 + j * 0.8, -1.2 + 0.3 * (j % 2), 0), M, r=r.uniform(0.25, 0.42))
        for j in range(4): rod(mb, F.p(u0 + 0.3 + j * 0.35 + (W - 1.6) * (j // 2), -0.06, 3.6 - 0.5 * (j % 2)), F.p(u0 + 0.3 + j * 0.35 + (W - 1.6) * (j // 2), -0.1, 3.6 - 0.5 * (j % 2)), 0.3, M['copper'], seg=14)
        F.box(mb, (cx - 1.3, -1.0, 0.0), (cx + 1.3, -0.3, 0.7), M['wood'])
        for j in range(4): _pot(mb, F.p(cx - 1.0 + j * 0.65, -0.65, 0.7), M, r=0.2, mat=M['brass'] if j % 2 else M['copper'])
    elif kind == 'jars':
        for j in range(4): _jar(mb, F.p(cx - 1.5 + j * 1.0, -1.0 - 0.3 * (j % 2), 0), M, h=r.uniform(1.1, 1.6), r=r.uniform(0.35, 0.5), mat=r.choice((M['terra'], M['terra_l'], M['tq'])))
    elif kind == 'spice':
        F.box(mb, (cx - 1.8, -1.6, 0), (cx + 1.8, -0.3, 0.75), M['wood'])
        for j in range(8):
            p = F.p(cx - 1.5 + (j % 4) * 1.0, -1.25 + 0.6 * (j // 4), 0.75); rod(mb, p, p + Vector((0, 0, 0.3)), 0.36, M['basket'], seg=12, r1=0.4)
            mb.frustum(p + Vector((0, 0, 0.3)), p + Vector((0, 0, 0.75)), 0.38, 0.02, M['spice'][(j + k) % 6], seg=12, cap1=False)
        for j in range(3): rod(mb, F.p(u0 + 0.4 + j * 0.3, -0.08, 3.4), F.p(u0 + 0.4 + j * 0.3, -0.08, 2.2), 0.08, M['spice'][(j + 2) % 6], seg=5)
    else:
        for j in range(3):
            p = F.p(cx - 1.3 + j * 1.3, -1.0, 0); F.box(mb, (cx - 1.8 + j * 1.3, -1.5, 0), (cx - 0.8 + j * 1.3, -0.5, 0.6), M['basket_d'])
            for q in range(7): mb.sphere(p + Vector((r.uniform(-0.3, 0.3), r.uniform(-0.3, 0.3), 0.7 + r.uniform(0, 0.15))), 0.17, M['fruit'][(j + q) % 4 if j != 1 else 1], seg=8, rings=5)

def _merchant_stall(SET, mb, gm, fl, cards, F, u0, M, lamps):
    """The richest water merchant's stall (two bays wide, front y 0 of frame F): a raised carpet-covered takht with bolsters, a canopy
    of a great carpet on four turned posts with lanterns, a row of huge glazed water jars and copper cups, the coin chest."""
    W = 2 * STREET['mod']; cx = u0 + W / 2
    F.box(mb, (u0 + 0.4, -2.6, 0), (u0 + W - 0.4, -0.2, 0.9), M['wood_d'])
    F.quad(mb, [(u0 + 0.4, -2.6, 0.91), (u0 + W - 0.4, -2.6, 0.91), (u0 + W - 0.4, -0.2, 0.91), (u0 + 0.4, -0.2, 0.91)], M['carpets'][3], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    F.quad(mb, [(u0 + 0.6, -2.62, 0.15), (u0 + W - 0.6, -2.62, 0.15), (u0 + W - 0.6, -2.62, 0.88), (u0 + 0.6, -2.62, 0.88)], M['kilim'][1], [(0, 0), (3, 0), (3, 0.4), (0, 0.4)], (0, -1, 0))
    for j in range(3): rod(mb, F.p(u0 + 1.5 + j * 1.2, -0.6, 1.25), F.p(u0 + 2.4 + j * 1.2, -0.6, 1.25), 0.32, M['red'] if j % 2 else M['kilim'][0], seg=10)
    for (x, y) in ((u0 + 0.5, -2.5), (u0 + W - 0.5, -2.5), (u0 + 0.5, -0.3), (u0 + W - 0.5, -0.3)):
        rod(mb, F.p(x, y, 0.9), F.p(x, y, 4.8), 0.1, M['wood'], seg=8)
        for z in (1.4, 3.0, 4.4): rod(mb, F.p(x, y, z), F.p(x, y, z + 0.15), 0.15, M['gold'], seg=8)
    F.quad(mb, [(u0 + 0.2, -2.8, 4.8), (u0 + W - 0.2, -2.8, 4.8), (u0 + W - 0.2, -0.1, 5.2), (u0 + 0.2, -0.1, 5.2)], M['carpets'][0], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, -1))
    F.quad(mb, [(u0 + 0.2, -2.8, 4.2), (u0 + W - 0.2, -2.8, 4.2), (u0 + W - 0.2, -2.8, 4.8), (u0 + 0.2, -2.8, 4.8)], M['kilim'][0], [(0, 0), (4, 0), (4, 0.3), (0, 0.3)], (0, -1, 0))
    for j in range(2):
        f = _lantern(mb, fl, cards, F.p(u0 + 2.4 + j * 4.2, -1.5, 3.4), M, s=1.1); chain_rod(mb, [f + Vector((0, 0, 0.8)), f + Vector((0, 0, 1.6))], 0.012, M['iron']); lamps.append(f)
    # the great jars: a row in front (glazed turquoise and terracotta), copper cups on a tray, a brass ewer, the chest
    for j in range(5): _jar(mb, F.p(u0 + 0.9 + j * 1.75, -3.3 - 0.15 * (j % 2), 0), M, h=2.0 if j % 2 == 0 else 1.7, r=0.6, mat=M['tq'] if j in (1, 3) else M['terra'])
    rod(mb, F.p(cx - 2.6, -1.9, 0.9), F.p(cx - 2.6, -1.9, 0.95), 0.6, M['brass'], seg=16)
    for j in range(6): a = j * 1.05; rod(mb, F.p(cx - 2.6 + 0.38 * math.cos(a), -1.9 + 0.38 * math.sin(a), 0.95), F.p(cx - 2.6 + 0.38 * math.cos(a), -1.9 + 0.38 * math.sin(a), 1.12), 0.08, M['copper'], seg=8, r1=0.1)
    _pot(mb, F.p(cx + 2.8, -1.9, 0.9), M, r=0.3, mat=M['brass'])
    F.box(mb, (cx + 1.2, -1.6, 0.9), (cx + 2.3, -0.9, 1.6), M['wood_d']); F.box(mb, (cx + 1.15, -1.65, 1.35), (cx + 2.35, -0.85, 1.45), M['gold'])
    for j in range(6): mb.sphere(F.p(cx + 1.4 + 0.15 * j, -1.25, 1.62), 0.07, M['gold'], seg=6, rings=3)
    STATE['marks']['merchant'] = tuple(round(v, 3) for v in F.p(cx + 0.4, -1.2, 0.9))
    STATE['marks']['merchant_front'] = tuple(round(v, 3) for v in F.p(cx - 1.2, -4.6, 0.0))

def _well(SET, mb, fl, cards, c, M):
    """The town well / fountain in the square: an octagonal tiled parapet with a stone rim, the water inside (sky mirror), a timber
    frame with a pulley wheel, rope and bucket, water jars round it."""
    c = Vector(c); R = 1.8; n = 8
    for i in range(n):
        a0, a1 = 2 * math.pi * (i + 0.5) / n, 2 * math.pi * (i + 1.5) / n
        p0, p1 = c + Vector((R * math.cos(a0), R * math.sin(a0), 0)), c + Vector((R * math.cos(a1), R * math.sin(a1), 0))
        nn = ((p0 + p1) / 2 - c).normalized()
        mb.oface([p0, p1, p1 + Vector((0, 0, 1.1)), p0 + Vector((0, 0, 1.1))], M['tile_panel'], [(0, 0), (0.7, 0), (0.7, 0.55), (0, 0.55)], nn)
        q0, q1 = c + (p0 - c) * 0.82, c + (p1 - c) * 0.82
        mb.oface([p0 + Vector((0, 0, 1.1)), p1 + Vector((0, 0, 1.1)), q1 + Vector((0, 0, 1.1)), q0 + Vector((0, 0, 1.1))], M['cream'], [(0, 0)] * 4, (0, 0, 1))
        mb.oface([q0, q1, q1 + Vector((0, 0, 1.1)), q0 + Vector((0, 0, 1.1))], M['pbrick'], [(0, 0), (0.7, 0), (0.7, 0.3), (0, 0.3)], -nn)
    mb.box(tuple(c + Vector((-R - 0.25, -R - 0.25, 0))), tuple(c + Vector((R + 0.25, R + 0.25, 0.12))), M['cream'])
    wm = MB(); wm.face([c + Vector((R * 0.82 * math.cos(2 * math.pi * (i + 0.5) / n), R * 0.82 * math.sin(2 * math.pi * (i + 0.5) / n), 0.6)) for i in range(n)], M['water']); _obj(wm, 'well_water', SET, shadow=False)
    for s in (-1, 1): beam(mb, c + Vector((s * 1.5, -0.2, 1.1)), c + Vector((s * 0.3, -0.2, 4.2)), 0.16, 0.16, M['wood']); beam(mb, c + Vector((s * 1.5, 0.2, 1.1)), c + Vector((s * 0.3, 0.2, 4.2)), 0.16, 0.16, M['wood'])
    beam(mb, c + Vector((-0.6, 0, 4.2)), c + Vector((0.6, 0, 4.2)), 0.2, 0.5, M['wood_d'])
    rod(mb, c + Vector((0, -0.12, 3.7)), c + Vector((0, 0.12, 3.7)), 0.4, M['wood_l'], seg=14); rod(mb, c + Vector((0, -0.14, 3.7)), c + Vector((0, 0.14, 3.7)), 0.08, M['iron'], seg=6)
    rod(mb, c + Vector((0.4, 0, 3.7)), c + Vector((0.4, 0, 1.8)), 0.025, M['rope'], seg=4); _bucket(mb, c + Vector((0.4, 0, 1.2)), M, s=0.9)
    for k, a in enumerate((0.4, 2.2, 3.9, 5.2)): _jar(mb, c + Vector((2.6 * math.cos(a), 2.6 * math.sin(a), 0)), M, h=1.2 + 0.2 * (k % 2), r=0.4, mat=M['terra_l'] if k % 2 else M['terra'])

def _iwan(SET, mb, F, M):
    """The great portal (iwan) of the mosque closing the square: a tall tiled frame (pishtaq) with a pointed arch half-dome niche,
    tile panels, kufic band, two minarets with balconies, and the turquoise onion dome behind on its drum."""
    W, H = 14.0, 19.0; cx = 0.0
    _arch_face(mb, F, -W / 2, W / 2, 0.0, H, cx, 7.6, 9.0, M['tile_panel_l'], M['tile_panel'], depth=3.0, soffit=M['tile_panel'], frame_mat=M['tq'])
    F.quad(mb, [(-W / 2, -0.02, H - 2.2), (W / 2, -0.02, H - 2.2), (W / 2, -0.02, H - 1.2), (-W / 2, -0.02, H - 1.2)], M['kufic'], [(0, 0), (3.5, 0), (3.5, 1), (0, 1)], (0, -1, 0))
    F.box(mb, (-W / 2 - 0.3, -0.4, H), (W / 2 + 0.3, 0.6, H + 0.6), M['cream'])
    F.box(mb, (-3.8, 3.0, 0), (3.8, 3.2, 9.0), M['tile_panel_l']); F.quad(mb, [(-1.0, 2.95, 0), (1.0, 2.95, 0), (1.0, 2.95, 3.5), (-1.0, 2.95, 3.5)], M['door_dark'], [(0, 0)] * 4, (0, -1, 0))
    for s in (-1, 1):
        b = F.p(s * (W / 2 + 0.2), 0.8, 0); rod(mb, b, b + Vector((0, 0, 28)), 1.0, M['pbrick'], seg=12, r1=0.8)
        for z in (12.0, 20.0, 27.0): rod(mb, b + Vector((0, 0, z)), b + Vector((0, 0, z + 0.9)), 0.95, M['tile_band_t'], seg=12)
        rod(mb, b + Vector((0, 0, 24)), b + Vector((0, 0, 24.5)), 1.5, M['wood_d'], seg=12)
        lumpy(mb, b + Vector((0, 0, 28.6)), 0.9, M['tq'], 91 + s, seg=12, rings=6, rough=0.0, squash=1.3); rod(mb, b + Vector((0, 0, 29.6)), b + Vector((0, 0, 30.6)), 0.06, M['gold'], seg=5)
    dc = F.p(0, 14.0, 0); rod(mb, dc, dc + Vector((0, 0, 20)), 7.0, M['pbrick'], seg=24); rod(mb, dc + Vector((0, 0, 19)), dc + Vector((0, 0, 21)), 7.1, M['tile_band_t'], seg=24)
    lumpy(mb, dc + Vector((0, 0, 23.5)), 7.6, M['tq'], 95, seg=28, rings=10, rough=0.0, squash=0.95); rod(mb, dc + Vector((0, 0, 30.4)), dc + Vector((0, 0, 33.0)), 0.12, M['gold'], seg=6)

def _bazaar(SET, P, M, dress):
    """The bazaar street of the town (running north, +y): two rows of brick arcades with tiled spandrels (shops in lamp-lit niches,
    goods out front under striped awnings), strings of pierced-brass lanterns across the street, the water merchant's rich stall on
    the east row, the square with the well, and the mosque iwan with its turquoise dome and minarets closing the view; the town wall,
    domes and windcatchers on the painted ring."""
    (xa, xb), (y0, y1) = STREET['x'], STREET['y']; (sy0, sy1), (sx0, sx1) = STREET['sq'], STREET['sq_x']; Wm = STREET['mod']
    g = MB(); g.quad((-60, -60, 0), (120, 0, 0), (0, 160, 0), M['pavers'], (-15, -15, 15, 25)); _obj(g, 'bazaar_floor', SET)
    mb = MB(); gm = MB(); fl = MB(); cards = MB(); r = _rnd(77); lamps = []
    n = int((y1 - y0) / Wm); mstall = (4, 5)                     # the merchant: east row bays 4-5 (y 4..13)
    for row, (x, yaw) in enumerate(((xa, -90.0), (xb, 90.0))):  # west row faces +x (front at x = -4.5), east row faces -x
        for k in range(n):
            u0 = k * Wm
            # yaw 90: local x along +y, the front faces +x (west row); yaw -90: local x along -y, the front faces -x (east row)
            if row == 0: F = Frame((x, y0, 0), 90.0); base_u = u0
            else: F = Frame((x, y1, 0), -90.0); base_u = (y1 - y0) - u0 - Wm
            if row == 1 and k in mstall:
                _shop_module(SET, mb, gm, F, base_u, M, r, row, k, merchant=True)
                if k == mstall[0]: _merchant_stall(SET, mb, gm, fl, cards, F, base_u - Wm, M, lamps)
                continue
            _shop_module(SET, mb, gm, F, base_u, M, r, row, k)
    # the square: facades on its sides (short rows facing in), the well, the iwan at the north end
    for row, (x, yaw) in enumerate(((sx0, 90.0), (sx1, -90.0))):
        for k in range(int((sy1 - sy0) / Wm) - 0):
            if row == 0: F = Frame((x, sy0, 0), 90.0); bu = k * Wm
            else: F = Frame((x, sy1, 0), -90.0); bu = k * Wm
            _shop_module(SET, mb, gm, F, bu, M, r, row, k + 20)
    for (xa_, xb_) in ((sx0, xa), (xb, sx1)):                    # square corner walls (south side), facing north
        F = Frame((xb_, sy0, 0), 180.0)
        F.quad(mb, [(0, 0, 0), (xb_ - xa_, 0, 0), (xb_ - xa_, 0, STREET['H']), (0, 0, STREET['H'])], M['pbrick'], [(0, 0), ((xb_ - xa_) / 4, 0), ((xb_ - xa_) / 4, STREET['H'] / 4), (0, STREET['H'] / 4)], (0, -1, 0))
        F.quad(mb, [(0, -0.02, 5.0), (xb_ - xa_, -0.02, 5.0), (xb_ - xa_, -0.02, 5.6), (0, -0.02, 5.6)], M['tile_band'], [(0, 0), (2, 0), (2, 1), (0, 1)], (0, -1, 0))
    _iwan(SET, mb, Frame((0, sy1, 0), 0.0), M)
    _well(SET, mb, fl, cards, (1.5, 37.5, 0), M)
    STATE['marks']['well'] = (1.5, 37.5, 0.0)
    # lantern strings across the street (every 9 D), three lanterns on each
    for k in range(5):
        y = y0 + 8.0 + k * 9.0
        if y > y1 - 2: break
        pts = catenary((xa + 0.2, y, 9.2), (xb - 0.2, y, 9.2), 1.0, 8); chain_rod(mb, pts, 0.02, M['rope'])
        for j, t in enumerate((0.25, 0.5, 0.75)):
            p = pts[int(t * 8)]; f = _lantern(mb, fl, cards, p - Vector((0, 0, 1.25)), M, s=0.8)
            if j == 1 and k < 3: lamps.append(f)
        for x in (xa, xb):                                        # wall lamps on brackets between the bays
            q = Vector((x + (0.5 if x < 0 else -0.5), y + 2.2, 4.3)); beam(mb, Vector((x, q.y, 4.6)), q + Vector((0, 0, 0.3)), 0.06, 0.06, M['iron'])
            _lantern(mb, fl, cards, q - Vector((0, 0, 0.8)), M, s=0.6)
    # townsfolk props: a donkey-cart of melons near the square, sacks
    for (x, y) in ((-2.6, 26.0), (3.2, 22.5), (-3.0, 8.0)):
        for j in range(3): lumpy(mb, (x + j * 0.5, y, 0.35), 0.4, M['straw'], 900 + j + int(y), seg=8, rings=5, rough=0.15, squash=1.0)
    _obj(mb, 'bazaar', SET, hull=0.015); _obj(gm, 'bazaar_cloth', SET, hull=0.0); _obj(fl, 'bazaar_glow', SET, shadow=False); _obj(cards, 'bazaar_halos', SET, shadow=False)
    lk = P['lamps']
    for i, f in enumerate(lamps[:6]): _flame_light('lamp_%d' % i, tuple(f), LAMP, 90.0 * lk, radius=0.2, shadow=False)
    STATE['marks'].update(street_centre=(0.0, 8.0, 0.0), passers=[(-2.0, 2.0, 0.0), (1.6, 12.0, 0.0), (-1.4, 22.0, 0.0)], well_woman=(3.6, 35.4, 0.0), boy=(-0.8, 34.4, 0.0), oldman=(-3.6, 36.6, 0.0))
    _sky(SET, P, M)

# ============================================================================= hooks
def _flick(frame, seed=0): return LV._flick(frame, seed)

def set_flames(k=1.0, frame=None):
    """Every lantern, fire, lamp-lit shop niche and the dome door glow: lamp energies and glow materials, 0 out .. 1 normal .. 1.5
    bright, with a deterministic flicker from the frame number (call every frame of a shot; keys linear)."""
    k = max(0.0, float(k)); f = frame if frame is not None else bpy.context.scene.frame_current
    for i, (L, base) in enumerate(STATE.get('flames', [])):
        L.data.energy = base * k * _flick(f, i + 1)
        if frame is not None: T._key(L.data, 'energy', frame, 'LINEAR')
    for j, m in enumerate(STATE.get('flame_mats', [])):
        s = m.node_tree.nodes['strength'].inputs['Strength']
        if 'base' not in m: m['base'] = s.default_value
        s.default_value = m['base'] * k * (_flick(f, 7 + j) if j < 6 else 1.0)
        if frame is not None:
            s.keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(m.node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    STATE['flames_k'] = k
set_lanterns = set_flames

ICE_STATES = dict(water=(0.0, 0.0), thin=(0.25, 0.0), thick=(1.0, 0.0), mud=(1.0, 1.0))

def _keyval(m, node, v, frame, interp='LINEAR'):
    s = m.node_tree.nodes[node].outputs[0]; s.default_value = v
    if frame is not None:
        s.keyframe_insert('default_value', frame=frame)
        for fc in T._fcurves(m.node_tree):
            for kp in fc.keyframe_points:
                if int(round(kp.co.x)) == int(frame): kp.interpolation = interp

def set_ice(level, melt=0.0, frame=None):
    """desert_ice plain: the state of every channel. level 0 open water (dark, mirroring the sky) .. 0.25 the first night's thin
    translucent sheet (water and stars show through, frost needles) .. 1 the thick white-blue slab (night 10; the sawn hole shows its
    thickness). melt 0..1 fades the ice away into brown mud and slush with puddles (the overslept noon). A string ('water' | 'thin' |
    'thick' | 'mud') sets both. Keys linear with frame."""
    if isinstance(level, str): level, melt = ICE_STATES[level]
    if 'ice' not in STATE: return
    level = max(0.0, min(1.0, float(level))); melt = max(0.0, min(1.0, float(melt))); M = STATE['M']; I = STATE['ice']
    vis = (min(1.0, level / 0.08)) * (1.0 - melt)
    _keyval(M['ice'], 'ice_k', level, frame); _keyval(M['ice'], 'ice_vis', vis, frame)
    _keyval(M['mud'], 'mud_k', melt, frame); _keyval(M['water'], 'murk', melt, frame)
    I['ice'].location.z = CH_Z['ice0'] + 0.08 * level; I['hole'].location.z = I['ice'].location.z; I['hole'].scale.z = max(0.001, (0.015 + 0.17 * level) * (1 - melt))
    I['mud'].location.z = CH_Z['mud']
    if frame is not None:
        T._key(I['ice'], 'location', frame, 'LINEAR'); T._key(I['hole'], 'location', frame, 'LINEAR'); T._key(I['hole'], 'scale', frame, 'LINEAR')
    T._show([I['hole']], level > 0.02 and melt < 0.95, frame)
    STATE['ice_state'] = (level, melt)

def set_heat_wisps(level, frame=None, speed=1.0):
    """Reveal: faint shimmering heat wisps rising from every channel toward the stars (camera-only cards). level 0 none .. 1 clear ..
    1.5 strong. The ribbons drift upward with the frame number (call it every frame; keys linear)."""
    if 'wisps' not in STATE: return
    m = STATE['M']['wisp']; nt = m.node_tree; f = frame if frame is not None else bpy.context.scene.frame_current
    k = nt.nodes['wisp_k'].outputs[0]; k.default_value = 0.22 * max(0.0, float(level))
    sc = nt.nodes['scroll'].inputs['Location']; sc.default_value = (0.0, -0.012 * speed * f, 0.0)
    if frame is not None:
        k.keyframe_insert('default_value', frame=frame); sc.keyframe_insert('default_value', frame=frame)
        for fc in T._fcurves(nt):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    T._show([STATE['wisps']], level > 0.001, frame)
    STATE['wisps_k'] = level

def set_stars(k=1.0, twinkle=0.35, frame=None):
    """Star brilliance: k scales the boost of the bright stars above 1 (they bloom) - 0 flat painted stars .. 1 normal .. 2 brilliant;
    twinkle 0..1 the per-star flicker, animated by the frame number (call per frame for twinkling; keys linear)."""
    m = STATE['M'].get('sky') if 'M' in STATE else None
    if m is None: return
    nt = m.node_tree; f = frame if frame is not None else bpy.context.scene.frame_current
    _keyval(m, 'star_k', float(k) * (1.0 if STATE['P'].get('star_k', 0) > 0 else 0.0), frame); _keyval(m, 'twinkle_k', float(twinkle), frame)
    w = nt.nodes['twinkle'].inputs['W']; w.default_value = 0.11 * f
    if frame is not None:
        w.keyframe_insert('default_value', frame=frame)
        for fc in T._fcurves(nt):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials), so plain set_* calls (no frame) hold again at render time."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights):
        if idb.animation_data: idb.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()

def apply_preset_state(preset):
    PR = PRESETS[preset]
    if PR['area'] == 'plain':
        set_ice(PR.get('ice', 0.25), PR.get('melt', 0.0)); set_heat_wisps(PR.get('wisps', 0.0))
    set_stars(1.0)
    set_flames(1.0)

# ============================================================================= cameras, anchors, staging
CAMS = dict(
    plain=dict(channels_wide=dict(loc=(-33.0, 17.0, 9.0), look_at=(10.0, 3.0, 2.6), lens=20),
               channel_ecu=dict(loc=(-4.2, CH_Y[1] - 0.2, 1.05), look_at=(5.0, CH_Y[1] + 1.4, -0.35), lens=22),
               wall_low=dict(loc=(-7.0, 14.5, 2.0), look_at=(0.5, -1.0, 7.0), lens=20),
               dome_wide=dict(loc=(4.0, 1.4, 2.8), look_at=(38.0, 9.5, 10.0), lens=22),
               sky_reveal=dict(loc=(-2.0, CH_Y[0] - 0.4, 0.5), look_at=(18.0, 10.0, 9.0), lens=18)),
    dome_in=dict(dome_interior=dict(loc=(-9.0, -0.6, 2.9), look_at=(3.0, 2.2, -0.4), lens=18)),
    bazaar=dict(bazaar_wide=dict(loc=(0.4, -12.0, 6.4), look_at=(0.0, 30.0, 4.4), lens=20),
                merchant_stall=dict(loc=(-3.0, 0.5, 3.3), look_at=(4.2, 9.6, 2.7), lens=22),
                well_eye=dict(loc=(-4.2, 26.0, 2.6), look_at=(1.6, 40.0, 4.6), lens=22)),
)
CAM_NOTES = dict(
    channels_wide='from just north of the wall, high, along the five channels toward the dome: lantern posts into depth, the camp fire, the dome door glow, the sky (Milky Way at NIGHT)',
    channel_ecu='low over channel 2 at the sawn hole: the ice surface fills the bottom (set_ice reads clearly: water / thin / thick / mud), the cut faces show the thickness, the lantern on the bank',
    wall_low='from the channels low up at the 15 D shade wall: pilasters, beam ends, crest, the stair; sky above',
    dome_wide='the yakhchal dome across the channels: its stepped cone, the porch door (warm at night), palms; Milky Way left at NIGHT',
    sky_reveal='low in the channels looking up north: ice in the foreground, heat wisps (set_heat_wisps) rising from every channel to the stars and the Milky Way',
    dome_interior='inside the dome from the walkway by the door: the ice pit stacked with blocks, the lantern (warm) against the cool ice, the shaft from the oculus, the inner cone',
    bazaar_wide='high down the bazaar street: arcades both sides, awnings, goods, lantern strings, the merchant stall right, the square, the well and the mosque iwan with its turquoise dome at the end',
    merchant_stall='the water merchant\'s stall: the carpet canopy and lanterns, the takht, the great jars, the chest; he stands on the takht',
    well_eye='eye level in the square at the well: the tiled parapet, pulley, jars; the iwan, minarets and dome behind',
)
HEIGHT = dict(farid=3.0, merchant=3.2, woman=2.9, oldman=2.9, boy=2.3)
T.PH.update(
    farid=('beach_man', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), HEIGHT['farid']),
    merchant=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), HEIGHT['merchant']),
    woman=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['woman']),
    oldman=('senior_a', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['oldman']),
    boy=('beach_kid', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['boy']))
placeholder_actor = T.placeholder_actor

STAGING = dict(
    channels_wide=[('farid', (-16.0, (CH_Y[2] + CH_Y[3]) / 2, 0.0))],
    channel_ecu=[('farid', (2.2, CH_Y[1] + CH_W / 2 + 0.75, 0.0))],
    wall_low=[('farid', (-2.2, 0.9, 0.0))],
    dome_wide=[('farid', (21.5, 7.4, 0.0))],
    sky_reveal=[],
    dome_interior=[('farid', (-4.2, -0.9, -0.8)), ('merchant', (-2.6, 2.4, -0.8))],
    bazaar_wide=[('woman', (-2.4, 4.0, 0.0)), ('boy', (1.0, 8.0, 0.0)), ('oldman', (-1.6, 15.0, 0.0)), ('farid', (1.4, 19.0, 0.0))],
    merchant_stall=[('merchant', None), ('farid', (0.4, 6.2, 0.0))],
    well_eye=[('woman', (3.4, 35.0, 0.0)), ('boy', (-1.2, 34.2, 0.0)), ('oldman', (-2.8, 38.5, 0.0))],
)

def _staging(cam_name):
    out = []
    for role, mk in STAGING.get(cam_name, []):
        if mk is None: mk = STATE['marks'].get('merchant', (6.0, 9.0, 0.9))
        out.append((role, tuple(mk)))
    return out

def anchors():
    P = STATE['P']; area = STATE['area']; cams = {k: dict(v) for k, v in CAMS[area].items()}
    A = dict(location=STATE['loc'], preset=STATE['preset'], area=area, light=STATE['light'], cams=cams, cam=dict(CAMS[area][PRESETS[STATE['preset']]['cam']]),
             cam_name=PRESETS[STATE['preset']]['cam'], cam_notes={k: CAM_NOTES.get(k, '') for k in cams},
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()),
             sun_elevation_deg=P['sun_elev'], floor_z=0.0, heights=dict(HEIGHT), marks=dict(STATE.get('marks', {})),
             lights=[o.name for o in STATE['LIGHTS'].objects], staging={k: _staging(k) for k in cams})
    if area == 'plain':
        A.update(wall=dict(WALL), channels=dict(x=CH_X, width=CH_W, centres=CH_Y, z=dict(CH_Z), cut_hole=dict(channel=1, x=CUT)), dome=dict(DOME),
                 keep_out='channels: |y - c| < 1.0 for c in centres, x -26..26 (stand on the banks between them); wall y < -0.4; dome r 13.3 round (38, 8); camp x -26..-20 y -0.8..3; brazier (-18.4, 0) r 0.7; ice blocks x -12.6..-9.4 y -0.4..0.5')
    elif area == 'dome_in':
        A.update(pit=dict(PIT), cone=dict(R0=11.6, H=25.0), keep_out='walk on the ring r 9.0..11.4 (z 0); the pit r < 9 (ice top z -1.6..-0.8); door at x -11.6')
    elif area == 'bazaar':
        A.update(street=dict(STREET), keep_out='street walkable x -2.0..2.0 (goods and awnings fill |x| > 2.1); merchant takht x 1.9..4.3 y 4.4..12.6 at z 0.9 (stand on it); jars y 4..13 x 0.7..1.8; takht x 1.9..4.3; the well r 2.2 round (1.5, 37.5); iwan y > 46')
    return A

def stage_placeholders(A, cam_name, cam_loc):
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(cam_name):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px)] at 720x1280 for the staged roles (caption rule: chin < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk) in enumerate(_staging(cam_name)):
        h = HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_render(loc, specs=None, quality='final', outdir=None, actors=True):
    """specs: ['preset' or 'preset:LIGHT' or 'preset:LIGHT:ice' (ice: water|thin|thick|mud|<level>)]"""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or LOC_PRESETS[loc]):
        parts = spec.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None; ice = parts[2] if len(parts) > 2 else None
        A = build(loc, pr, light=lt); sc = bpy.context.scene; setup_render(sc, quality)
        if ice: set_ice(ice if ice in ICE_STATES else float(ice))
        if len(parts) > 3: set_heat_wisps(float(parts[3]))
        nm = A['cam_name']; cs = A['cams'][nm]; make_camera(cs)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm)
        tag = '%s_%s' % (pr, A['light']) + ('_' + ice if ice else '')
        w, c = render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(c, 1), hp)
        print('%s %s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, loc, tag, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'):
        cli_render(arg[0] if arg else 'desert_ice', arg[1:] or None, 'final' if cmd == 'final' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'desert_ice', arg[1] if len(arg) > 1 else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)
