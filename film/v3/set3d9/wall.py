#!/usr/bin/env python3
"""wall.py : set of film 9 ("ไอ้ช่างขนม", the sticky-rice mortar of a Ming city wall, ~1370s) as a real 3D Blender set (bpy 5.3, Cycles CPU).
One location, built by preset (the preset picks the area, default light, camera and set state):

    import wall as W
    A = W.build('wall_site', 'two_sections', light='DAY')   # site_wide | cauldron | two_sections | two_sections_out | wall_top | cannon_line
                                                             # mortar_macro | mortar_macro_rice   (the macro area: inside the joint)
    cam = W.make_camera(A['cam'])
    W.set_wall_height('general', 20); W.set_wall_height('lin', 14)    # courses (0.5 D each) of each section
    W.set_cauldron_steam(1.0, frame=n); W.set_rain(1.0, frame=n); W.set_mortar_wet(0.8)
    W.set_cracks('general', 0.66); W.set_impact('general', 0, t, frame=n); W.set_collapse(t, frame=n)
    W.set_smoke(1.0, frame=n); W.set_flames(1.0, frame=n); W.set_army(True); W.set_macro(t, frame=n)

Light presets (build light=): DAY | DUSK | DAWN | RAIN (overcast, wet sheen, rain streaks) | BATTLE (smoky red dusk, fires).
World: 1 unit = 1 D (head diameter), Z up, ground z = 0. The wall runs along x; its OUTER face (field, river, enemy) is y = 0
facing -y, its INNER face (the construction site) y = 5 facing +y. Lin's rice-mortar section x -22..0, the general's plain section
x 0..22, the gate tower x 24..38. NO depth of field anywhere. Built on v3/set3d8/desert.py -> louvre -> bakery -> mine -> pagoda /
tower: helpers are imported, not copied. See wall_API.md.
CLI: python3 wall.py stills | final [spec ...] | digest <preset>     spec = preset[:LIGHT[:state]]"""
import os, sys, math, json, time, random
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'),
          os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402
import louvre as LV                                        # noqa: E402
import desert as D                                         # noqa: E402  (film-8 template: sky dome, water mirror, flames hook, keys)
import wall_tex as WX                                      # noqa: E402
from tower import MB, no_bounce, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, catenary, chain_rod, _obj, _untoon, _glossy   # noqa: E402,F401
WORK = os.path.join(HERE, 'wall_work')
STATE = T.STATE
setup_dof = G.setup_dof; digest = G.digest
Frame = BK.Frame; _halo = BK._halo
set_flames = D.set_flames; set_lanterns = D.set_flames; _keyval = D._keyval

def _rnd(seed): return random.Random(seed)
FIRE = (1.0, 0.58, 0.26); LAMP = (1.0, 0.62, 0.34)

# ----------------------------------------------------------------------------- dimensions (D)
CH = 0.5; PL = 1.0; NMAX = 30; WT = 5.0                       # course height, plinth top, max courses, wall thickness (outer y 0, inner y 5)
SEC = dict(lin=(-22.0, 0.0), general=(0.0, 22.0))            # x ranges: lin = rice mortar, general = plain mortar
KIND = dict(lin='rice', general='plain')
GATE = dict(x=(24.0, 38.0), y=(-1.5, 6.5), h=17.0, cx=31.0, arch_w=4.4, arch_h=7.0)
OLD = dict(x=(-74.0, -22.0), h=16.0)                         # the finished old wall west of Lin's section
STUB = dict(x=(22.0, 24.0), h=16.0)                          # finished wall stub between the general's section and the gate
IMPACTS = dict(general=[(6.0, 7.0), (13.5, 4.5), (9.5, 10.0)], lin=[(16.5, 6.5), (9.0, 4.0), (4.5, 9.0)])   # section-local (x from x0, z from PL)
CANNON_X = [-16.5, -9.5, -2.5, 4.5, 11.5, 18.5]; CANNON_Y = -22.0
SLOT_CANNON = dict(lin=[0, 1, 2], general=[3, 4, 5])
KB = 3                                                        # collapse: the general's section breaks above course KB
RIVER = (-58.0, -46.0)
def top_z(section, n=None): return PL + CH * (STATE.get('heights', {}).get(section, 18) if n is None else n)

# ----------------------------------------------------------------------------- light presets
def _kdaz(az, el):
    """key_dir (travel) for a sun at azimuth az (deg, from +x CCW, the sky-texture convention) and elevation el."""
    return G._kd((-math.cos(math.radians(az)), -math.sin(math.radians(az))), el)
_B = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, grade_offset=(0.002, 0.003, 0.006), sun_angle=0.6, wet=0.0, lamps=1.0)
LIGHTS = dict(
    DAY=dict(_B, key=(1.80, 1.52, 1.08), key_dir=_kdaz(135, 42), sun_elev=42, shade=(0.10, 0.12, 0.30), shade_tint=(0.09, 0.12, 0.34), shade_mix=0.45,
             grade_offset=(-0.01, -0.01, -0.005), lift=(0.006, 0.008, 0.022), sky='DAY', sky_k=0.95, pano='DAY', pano_k=0.95, haze=('#e4ecf8', 0.07), grade_saturation=1.12,
             refl_k=0.7, lamps=0.45, steam_rgb=(1.0, 0.98, 0.95), dust_rgb=(0.92, 0.84, 0.72), smoke_rgb=(0.55, 0.52, 0.5)),
    DUSK=dict(_B, key=(1.75, 0.98, 0.52), key_dir=_kdaz(160, 9), sun_elev=9, sun_angle=0.8, shade=(0.05, 0.095, 0.25), shade_tint=(0.05, 0.11, 0.31), shade_mix=0.8,
              grade_offset=(-0.006, -0.008, -0.004), lift=(0.008, 0.005, 0.02), sky='DUSK', sky_k=1.0, pano='DUSK', pano_k=0.95, haze=('#ffa878', 0.09), grade_saturation=1.12,
              refl_k=0.85, lamps=1.0, steam_rgb=(1.0, 0.86, 0.72), dust_rgb=(0.95, 0.7, 0.5), smoke_rgb=(0.45, 0.35, 0.38)),
    DAWN=dict(_B, key=(1.62, 1.08, 0.80), key_dir=_kdaz(20, 7), sun_elev=7, sun_angle=1.0, shade=(0.07, 0.12, 0.28), shade_tint=(0.07, 0.13, 0.33), shade_mix=0.8,
              grade_offset=(-0.008, -0.008, -0.004), lift=(0.01, 0.008, 0.022), sky='DAWN', sky_k=1.0, pano='DAWN', pano_k=0.95, haze=('#f8c8c0', 0.10), grade_saturation=1.1,
              refl_k=0.85, lamps=0.8, steam_rgb=(1.0, 0.92, 0.88), dust_rgb=(0.95, 0.82, 0.72), smoke_rgb=(0.5, 0.45, 0.5)),
    RAIN=dict(_B, key=(0.82, 0.88, 1.0), key_dir=_kdaz(95, 62), sun_elev=62, sun_angle=28.0, shade=(0.15, 0.17, 0.27), shade_tint=(0.14, 0.17, 0.30), shade_mix=0.5,
              grade_offset=(-0.004, -0.004, -0.002), lift=(0.01, 0.012, 0.02), sky='RAIN', sky_k=0.9, pano='RAIN', pano_k=0.9, haze=('#9aa6b8', 0.12), grade_saturation=1.05,
              refl_k=0.9, lamps=1.0, wet=1.0, ground_k=0.85, steam_rgb=(0.95, 0.96, 1.0), dust_rgb=(0.7, 0.7, 0.72), smoke_rgb=(0.5, 0.5, 0.55)),
    BATTLE=dict(_B, key=(1.60, 1.0, 0.56), key_dir=_kdaz(262, 12), sun_elev=12, sun_angle=1.0, shade=(0.04, 0.08, 0.22), shade_tint=(0.04, 0.09, 0.28), shade_mix=0.82,
                grade_offset=(-0.004, -0.006, -0.002), lift=(0.008, 0.004, 0.018), sky='BATTLE', sky_k=1.0, pano='BATTLE', pano_k=0.9, haze=('#b05a3a', 0.08), grade_saturation=1.12,
                refl_k=0.9, lamps=1.3, steam_rgb=(1.0, 0.8, 0.65), dust_rgb=(0.82, 0.55, 0.38), smoke_rgb=(0.30, 0.24, 0.26)),
)
LIGHT_KEYS = list(LIGHTS)

PRESETS = dict(
    site_wide=dict(area='site', light='DAY', cam='site_wide', heights=(18, 21), steam=1.0),
    cauldron=dict(area='site', light='DAY', cam='cauldron', heights=(18, 21), steam=1.0),
    two_sections=dict(area='site', light='DAY', cam='two_sections', heights=(18, 21), steam=1.0),
    two_sections_out=dict(area='site', light='BATTLE', cam='two_sections_out', heights=(26, 30), army=True, smoke=1.0),
    wall_top=dict(area='site', light='DAY', cam='wall_top', heights=(20, 26), steam=1.0),
    cannon_line=dict(area='site', light='BATTLE', cam='cannon_line', heights=(26, 30), army=True, smoke=1.0),
    mortar_macro=dict(area='macro', light='BATTLE', cam='macro_plain', kind='plain'),
    mortar_macro_rice=dict(area='macro', light='BATTLE', cam='macro_rice', kind='rice'),
)
LOC_PRESETS = dict(wall_site=list(PRESETS))

# ----------------------------------------------------------------------------- build
def build(location='wall_site', preset=None, clear=True, dress=True, light=None):
    """Build the location for a preset (LOC_PRESETS) into the current scene: the preset's area only, its light (light= overrides it:
    DAY | DUSK | DAWN | RAIN | BATTLE), world, render settings, grade, denoiser and the preset's set state (section heights, steam,
    rain at RAIN, army + smoke at BATTLE). Returns the anchors dict (wall_API.md); A['cam'] is the preset camera."""
    preset = preset or 'site_wide'
    assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PR = PRESETS[preset]; lkey = light or PR['light']; scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    if PR['area'] == 'macro':                       # the joint seen from very close: warm fire key from the front-left, deep blue shade
        P.update(key_dir=G._kd((0.8, 0.6), 24), sun_elev=24, sun_angle=2.0, key=(1.55, 0.98, 0.52), shade=(0.05, 0.08, 0.26), shade_tint=(0.05, 0.085, 0.30), shade_mix=0.7)
    STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location; STATE['area'] = PR['area']; STATE['light'] = lkey
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('WAL_', 'ink')): bpy.data.materials.remove(m)
    tx = WX.ensure(extra=_crack_jobs, verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_wall') or bpy.data.worlds.new('W_wall'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'WAL_%s_%s_' % (PR['area'], lkey); FORM = tuple(P['form'])
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
    STATE['flames'] = []; STATE['flame_mats'] = list(M['_flame_mats']); STATE['marks'] = {}; STATE['heights'] = {}
    if PR['area'] == 'site': _site(SET, P, M, dress, PR)
    else: _macro(SET, P, M, PR.get('kind', 'plain'))
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    setup_grade(scene)
    if PR['area'] == 'site': _rain_comp(scene)
    for ob in SET.objects:
        no_bounce(ob)
        if ob.get('glossy_vis'): ob.visible_glossy = True
    set_flames(1.0)
    apply_preset_state(preset)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """= mine.setup_render: final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light, OpenImageDenoise. No DOF."""
    MN.setup_render(scene, quality); scene.cycles.transparent_max_bounces = 24

def apply_dof(cam_name=None, scene=None, cam=None):
    """Client rule: no depth of field at all (kept for API symmetry)."""
    return None

def _crack_jobs():
    for s in SEC:
        WX.add_cracks('cracks_' + s, s, SEC[s][1] - SEC[s][0], NMAX * CH, IMPACTS[s], ppd=40, seed=61 if s == 'general' else 67)

# ============================================================================= materials
def _img_noncolor(path):
    im = T._img(path); im.colorspace_settings.name = 'Non-Color'; return im

def _tex_node(m):
    return [n for n in m.node_tree.nodes if n.bl_idname == 'ShaderNodeTexImage'][0]

def _mat_brick(name, P, tx, kind):
    """Wall brick (world-UV 4 x 4 D tile) lit as every surface. Value 'wet' (set_mortar_wet; rice only): the creamy mortar darkens and
    turns glossy, milky runs (drips overlay) hang from the bed joints. RAIN (P wet): darker bricks and a soft wet sheen for the lamps."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    wetk = P.get('wet', 0.0)
    m = _untoon(mat_lit(name, image=tx['brick_' + kind], gain=1.0 - 0.18 * wetk, form=tuple(P['form']))); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); art = tex.outputs['Color']
    if kind == 'rice':
        wv = D._value(nt, 'wet', 0.0)
        mk = N('ShaderNodeTexImage'); mk.image = _img_noncolor(tx['brick_rice_mask'])
        dr = N('ShaderNodeTexImage'); dr.image = T._img(tx['drips'])
        for n in (mk, dr): L(tex.inputs['Vector'].links[0].from_socket, n.inputs['Vector']) if tex.inputs['Vector'].is_linked else None
        dm = N('ShaderNodeMath'); dm.operation = 'MULTIPLY'; L(dr.outputs['Alpha'], dm.inputs[0]); L(wv.outputs[0], dm.inputs[1])
        mm = N('ShaderNodeMath'); mm.operation = 'MULTIPLY'; L(mk.outputs['Color'], mm.inputs[0]); L(wv.outputs[0], mm.inputs[1])
        dk = N('ShaderNodeMix'); dk.data_type = 'RGBA'; dk.blend_type = 'MULTIPLY'; L(mm.outputs[0], dk.inputs[0]); dk.inputs[7].default_value = (0.72, 0.68, 0.6, 1)
        mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; L(dm.outputs[0], mx.inputs[0]); mx.inputs[7].default_value = (*T.hex_lin('#e8dcc0'), 1)
        D._retarget(nt, art, mx.outputs[2]); L(art, dk.inputs[6]); L(dk.outputs[2], mx.inputs[6])
        def make(nt):
            gl = nt.nodes.new('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = 0.18
            g1 = nt.nodes.new('ShaderNodeMath'); g1.operation = 'MAXIMUM'; L(mm.outputs[0], g1.inputs[0]); L(dm.outputs[0], g1.inputs[1])
            g2 = nt.nodes.new('ShaderNodeMath'); g2.operation = 'MULTIPLY'; g2.inputs[1].default_value = 0.6; L(g1.outputs[0], g2.inputs[0])
            cc = nt.nodes.new('ShaderNodeCombineColor'); L(g2.outputs[0], cc.inputs[0]); L(g2.outputs[0], cc.inputs[1]); L(g2.outputs[0], cc.inputs[2])
            L(cc.outputs[0], gl.inputs['Color']); return gl.outputs['BSDF']
        MN._append_shader(m, make)
    if wetk > 0: _glossy(m, (0.75, 0.8, 0.9), 0.22 * wetk, 0.25)
    return m

def _mat_overlay(name, P, image, order, rgb_gain=1.0):
    """Crack overlay (set_cracks): lit like the wall (dark core, light chipped lip), alpha = image alpha x (order <= 'lvl') x
    (world z <= 'top_z') - the cracks grow from each impact as the level rises and never show above the wall top."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, image=image, gain=rgb_gain, alpha=True, form=tuple(P['form']))); nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    tex = _tex_node(m); mixsh = tex.outputs['Alpha'].links[0].to_node
    od = N('ShaderNodeTexImage'); od.image = _img_noncolor(order); od.interpolation = 'Closest'
    lv = D._value(nt, 'lvl', 0.0); tz = D._value(nt, 'top_z', 99.0)
    c1 = N('ShaderNodeMath'); c1.operation = 'LESS_THAN'; L(od.outputs['Color'], c1.inputs[0]); L(lv.outputs[0], c1.inputs[1])
    geo = N('ShaderNodeNewGeometry'); sp = N('ShaderNodeSeparateXYZ'); L(geo.outputs['Position'], sp.inputs[0])
    c2 = N('ShaderNodeMath'); c2.operation = 'LESS_THAN'; L(sp.outputs['Z'], c2.inputs[0]); L(tz.outputs[0], c2.inputs[1])
    a1 = N('ShaderNodeMath'); a1.operation = 'MULTIPLY'; L(tex.outputs['Alpha'], a1.inputs[0]); L(c1.outputs[0], a1.inputs[1])
    a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; L(a1.outputs[0], a2.inputs[0]); L(c2.outputs[0], a2.inputs[1])
    for l in list(tex.outputs['Alpha'].links): nt.links.remove(l)
    L(a2.outputs[0], mixsh.inputs['Fac'])
    return m

def _mat_decal(name, P, image):
    """Impact dent decal: lit, alpha x Value 'vis'."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = _untoon(mat_lit(name, image=image, alpha=True, form=tuple(P['form'])))
    return D._mat_alpha_k(m, 'vis', 0.0)

def _mat_dust(name, rgb, k=1.0):
    """Billowing dust / smoke ball (camera-only): soft edge from the facing ratio x object-space noise, alpha-over emission rgb x k.
    Value 'op' = opacity (keyed by the hooks)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); lw = N('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.5
    f = N('ShaderNodeMath'); f.operation = 'SUBTRACT'; f.inputs[0].default_value = 1.0; L(lw.outputs['Facing'], f.inputs[1])
    f2 = N('ShaderNodeMath'); f2.operation = 'POWER'; f2.inputs[1].default_value = 2.4; L(f.outputs[0], f2.inputs[0])
    tc = N('ShaderNodeTexCoord'); nz = N('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 2.2; nz.inputs['Detail'].default_value = 4.0; L(tc.outputs['Object'], nz.inputs['Vector'])
    n2 = N('ShaderNodeMapRange'); n2.inputs['From Min'].default_value = 0.3; n2.inputs['From Max'].default_value = 0.7; L(nz.outputs['Fac'], n2.inputs['Value'])
    a = N('ShaderNodeMath'); a.operation = 'MULTIPLY'; L(f2.outputs[0], a.inputs[0]); L(n2.outputs['Result'], a.inputs[1])
    op = D._value(nt, 'op', 1.0); a2 = N('ShaderNodeMath'); a2.operation = 'MULTIPLY'; a2.use_clamp = True; L(a.outputs[0], a2.inputs[0]); L(op.outputs[0], a2.inputs[1])
    sh = N('ShaderNodeMapRange'); sh.inputs['To Min'].default_value = 0.62; sh.inputs['To Max'].default_value = 1.15; L(nz.outputs['Fac'], sh.inputs['Value'])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(sh.outputs['Result'], em.inputs['Strength'])
    sc = N('ShaderNodeMath'); sc.operation = 'MULTIPLY'; sc.inputs[1].default_value = k; L(sh.outputs['Result'], sc.inputs[0]); L(sc.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(a2.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx2 = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2]); L(mx2.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_crack_ribbon(name, rgb, k=1.0):
    """Macro crack ribbon: emission rgb (dark core / light dust lip), visible where UV.x (reveal order) <= Value 'lvl'."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); uv = N('ShaderNodeUVMap'); sp = N('ShaderNodeSeparateXYZ'); L(uv.outputs['UV'], sp.inputs[0])
    lv = D._value(nt, 'lvl', 0.0); c = N('ShaderNodeMath'); c.operation = 'LESS_THAN'; L(sp.outputs['X'], c.inputs[0]); L(lv.outputs[0], c.inputs[1])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); L(c.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    L(mx.outputs['Shader'], out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _glow_add(m, rgb, k):
    """Add a constant emission lobe (cool inner glow of the lime crystals in the macro)."""
    def make(nt):
        em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = k; return em.outputs['Emission']
    return MN._append_shader(m, make)

def _materials(P, C, TX, E, tx, pre):
    lk = P.get('lamps', 1.0); gk = P.get('ground_k', 1.0); wet = P.get('wet', 0.0)
    def wetg(m, k=0.25): return _glossy(m, (0.75, 0.8, 0.9), k * wet, 0.2) if wet > 0 else m
    M = dict(brick_plain=_mat_brick(pre + 'brick_plain', P, tx, 'plain'), brick_rice=_mat_brick(pre + 'brick_rice', P, tx, 'rice'),
             brick_old=wetg(TX('brick_old', 1.0 - 0.15 * wet)), stone=wetg(TX('stone', 1.0 - 0.15 * wet)), topbed=TX('topbed', form=False),
             ground=wetg(TX('ground', gk * (1 - 0.2 * wet), form=False), 0.35), field=TX('field', gk * (1 - 0.15 * wet), form=False),
             lime=TX('lime', form=False), mortar_plain=TX('mortar_plain', form=False), mortar_rice=_glossy(TX('mortar_rice', form=False), (1.0, 0.95, 0.85), 0.25, 0.2),
             soup=_glossy(TX('soup', 1.05, form=False), (1.0, 0.95, 0.85), 0.3, 0.15), tiles=wetg(TX('tiles'), 0.4), canvas=TX('canvas', smix=0.3), canvas_b=TX('canvas_b', smix=0.3),
             banner_red=TX('banner_red', 1.0, (1.4, 0.8, 0.7), alpha=True, smix=0.2), banner_blue=TX('banner_blue', alpha=True, smix=0.3), banner_black=TX('banner_black', alpha=True, smix=0.3),
             wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b08458'), bamboo=C('#c8b070'), bamboo_d=C('#9a8448'), rope=C('#c8a868'),
             iron=_glossy(C('#34323a', 1.0, 1.1), (1.0, 0.85, 0.7), 0.35, 0.28), bronze=_glossy(C('#8a6a3a', 1.0, (2.0, 1.4, 0.6), smix=0.2), (1.0, 0.8, 0.5), 0.5, 0.25),
             red=C('#b02a22', 1.0, (1.4, 0.8, 0.7), smix=0.2), red_d=C('#7a1a18', 1.0, (1.4, 0.8, 0.7), smix=0.2), gold=_glossy(C('#d8a840', 1.0, (2.2, 1.5, 0.6)), (1.0, 0.85, 0.5), 0.5, 0.2),
             green=C('#3e6a3a'), green_d=C('#2e4e2e'), leaf=C('#4a7a3a'), trunk=C('#6a4a32'), sack=C('#d8c49a'), straw=C('#d8b870'), rock=C('#8a8680'),
             dark=C('#1a1416', 1.0, 0.5, form=False), white=C('#ece6d8'), cloth_b=C('#2a4a7a'), lattice=C('#6a2a1e'), plaster=C('#d8ccb4'),
             flame=mat_emit(pre + 'e_flame', '#ffa040', strength=6.0), flame_c=mat_emit(pre + 'e_flamec', '#fff0c0', strength=10.0), ember=mat_emit(pre + 'e_ember', '#ff6a20', strength=3.0),
             lantern=mat_emit(pre + 'e_lantern', image=tx['lantern_red'], strength=2.6 * max(0.5, lk)), stove_glow=mat_emit(pre + 'e_stove', '#ff7a2a', strength=3.5),
             win_glow=mat_emit(pre + 'e_win', '#ffb060', strength=1.2 * max(0.4, lk)), tent_glow=mat_emit(pre + 'e_tentglow', '#ffb870', strength=0.9 * lk), door_dark=mat_emit(pre + 'e_dark', '#140e12', strength=1.0),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.55, 0.28), 0.55 * lk), halo_big=BK._mat_add(pre + 'halo_big', tx['pool'], (1.0, 0.5, 0.22), 0.9 * max(0.6, lk), node='fire_glow'),
             web=mat_emit(pre + 'e_web', '#ffdc96', strength=1.8), fire=MN._mat_fire(pre + 'fire'), flash=mat_emit(pre + 'e_flash', '#fff2c8', strength=0.0),
             crystal=_glow_add(_glossy(C('#e8f2fa', 1.0, (1.0, 1.15, 1.4), smix=0.6), (1.0, 0.95, 0.9), 0.9, 0.06), (0.55, 0.8, 1.0), 0.12), clay=TX('clay_macro'), clay_d=TX('clay_macro', 0.8),
             matrix_plain=TX('matrix_plain', form=False), matrix_rice=_glossy(TX('matrix_rice', form=False), (1.0, 0.92, 0.8), 0.18, 0.25),
             
             dust=_mat_dust(pre + 'dust', P['dust_rgb'], 1.0), mdust=_mat_dust(pre + 'mdust', P['smoke_rgb'], 1.0),
             water=D._mat_water(pre + 'water', P, base='#2a4050', murk='#5a4a34'), puddle=D._mat_water(pre + 'puddle', P, base='#3a3a3e', murk='#5a4a34'))
    M['cannonball'] = _glossy(C('#2a2a30', 1.0, 0.9), (1.0, 0.8, 0.6), 0.3, 0.45)
    M['_flame_mats'] = [M['flame'], M['flame_c'], M['ember'], M['lantern'], M['stove_glow'], M['halo'], M['win_glow'], M['tent_glow']]
    for nm in ('halo', 'halo_big'):                                 # _mat_add keeps its strength in a Value; expose an Emission named 'strength' for set_flames
        pass
    M['_flame_mats'] = [M['flame'], M['flame_c'], M['ember'], M['lantern'], M['stove_glow'], M['win_glow'], M['tent_glow']]
    M['sky'] = D._mat_sky(pre + 'sky_' + P['sky'], dict(P, star_k=0.0), tx['sky_' + P['sky']], P['sky_k'])
    return M

# ============================================================================= helpers
def _flame_light(name, loc, rgb, energy, radius=0.12, shadow=False): return D._flame_light(name, loc, rgb, energy, radius, shadow)

def _bamboo(mb, p0, p1, M, r=0.075):
    p0, p1 = Vector(p0), Vector(p1); rod(mb, p0, p1, r, M['bamboo'], seg=6)
    L_ = (p1 - p0).length; n = int(L_ / 1.3)
    for k in range(1, n + 1):
        q = p0.lerp(p1, k / (n + 1)); d = (p1 - p0).normalized() * 0.03; rod(mb, q - d, q + d, r * 1.25, M['bamboo_d'], seg=6)

def _cn_lantern(mb, fl, cards, p, M, s=1.0, hang=0.6):
    """Chinese red paper lantern: glowing ellipsoid skin, gold caps, red tassel, hanging cord; returns the flame centre."""
    p = Vector(p)
    lumpy(fl, p, 0.42 * s, M['lantern'], 5, seg=14, rings=7, rough=0.0, squash=0.85)
    for z in (0.33, -0.33): rod(mb, p + Vector((0, 0, z * s)), p + Vector((0, 0, (z + (0.08 if z > 0 else -0.08)) * s)), 0.2 * s, M['gold'], seg=10)
    rod(mb, p + Vector((0, 0, -0.42 * s)), p + Vector((0, 0, -0.85 * s)), 0.04 * s, M['red'], seg=5, r1=0.07 * s)
    if hang: rod(mb, p + Vector((0, 0, 0.41 * s)), p + Vector((0, 0, (0.41 + hang) * s)), 0.012, M['dark'], seg=4)
    _halo(cards, p, 1.0 * s, M)
    return p

def _lantern_pole(mb, fl, cards, base, M, h=4.2, arm=(0.9, 0.0)):
    b = Vector(base); rod(mb, b, b + Vector((0, 0, h)), 0.08, M['wood_d'], seg=6)
    a = Vector((arm[0], arm[1], 0)); beam(mb, b + Vector((0, 0, h - 0.15)), b + a + Vector((0, 0, h - 0.15)), 0.08, 0.08, M['wood_d'])
    return _cn_lantern(mb, fl, cards, b + a * 0.85 + Vector((0, 0, h - 1.05)), M, s=1.0, hang=0.45)

def _cn_roof(mb, cx, cy, hx, hy, z0, rise, over, lift, M, ridge=True):
    """Chinese hip roof with concave slopes and swept-up corners: eave rectangle (hx + over, hy + over) at z0 (corners lifted by
    `lift`), ridge line along x at z0 + rise; grey barrel tiles, red fascia, ridge with curled end ornaments."""
    ns, nv = 12, 6; rx = max(0.0, hx - hy)
    def eave(side, s):
        if side in (0, 1):
            sg = -1 if side == 0 else 1; return Vector((cx + s * (hx + over), cy + sg * (hy + over), z0 + lift * abs(s) ** 3))
        sg = -1 if side == 2 else 1; return Vector((cx + sg * (hx + over), cy + s * (hy + over), z0 + lift * abs(s) ** 3))
    def ridgep(side, s):
        if side in (0, 1): return Vector((cx + s * rx, cy, z0 + rise))
        return Vector((cx + (-1 if side == 2 else 1) * rx, cy, z0 + rise))
    for side, nrm in ((0, (0, -1, 1)), (1, (0, 1, 1)), (2, (-1, 0, 1)), (3, (1, 0, 1))):
        for i in range(ns):
            s0, s1 = -1 + 2 * i / ns, -1 + 2 * (i + 1) / ns
            for j in range(nv):
                v0, v1 = j / nv, (j + 1) / nv
                def P_(s, v):
                    e, r = eave(side, s), ridgep(side, s); q = e.lerp(r, v); q.z = e.z + (r.z - e.z) * v ** 1.7; return q
                q = [P_(s0, v0), P_(s1, v0), P_(s1, v1), P_(s0, v1)]
                mb.oface(q, M['tiles'], [(s0 * 2, v0 * 2), (s1 * 2, v0 * 2), (s1 * 2, v1 * 2), (s0 * 2, v1 * 2)], nrm)
            a, b = eave(side, s0), eave(side, s1); fz = Vector((0, 0, 0.28))
            mb.oface([a - fz, b - fz, b, a], M['red_d'], [(0, 0)] * 4, (nrm[0], nrm[1], 0))
    if ridge:
        a, b = Vector((cx - rx, cy, z0 + rise)), Vector((cx + rx, cy, z0 + rise)); beam(mb, a - Vector((0.3, 0, 0)), b + Vector((0.3, 0, 0)), 0.35, 0.45, M['tiles'])
        for sg in (-1, 1):
            e = Vector((cx + sg * (rx + 0.3), cy, z0 + rise + 0.2)); rod(mb, e, e + Vector((sg * 0.15, 0, 0.9)), 0.22, M['tiles'], seg=6, r1=0.1)
            lumpy(mb, e + Vector((-sg * 0.1, 0, 0.95)), 0.22, M['tiles'], 3, seg=8, rings=4, rough=0.0)
        for sg in (-1, 1):                                                        # hip ridges
            for sy in (-1, 1):
                c0 = Vector((cx + sg * (hx + over), cy + sy * (hy + over), z0 + lift)); c1 = Vector((cx + sg * rx, cy, z0 + rise))
                pts = [c0.lerp(c1, t) for t in (0, 0.33, 0.66, 1.0)]
                for k, (p0, p1) in enumerate(zip(pts, pts[1:])):
                    t0, t1 = k / 3, (k + 1) / 3; p0 = Vector((p0.x, p0.y, c0.z + (c1.z - c0.z) * t0 ** 1.7 + 0.12)); p1 = Vector((p1.x, p1.y, c0.z + (c1.z - c0.z) * t1 ** 1.7 + 0.12))
                    rod(mb, p0, p1, 0.13, M['tiles'], seg=6)
                rod(mb, c0 + Vector((0, 0, 0.1)), c0 + Vector((sg * 0.3, sy * 0.3, 0.55)), 0.13, M['tiles'], seg=6, r1=0.05)

def _tree(mb, base, M, h=6.0, seed=0, willow=False):
    r = _rnd(seed); b = Vector(base); top = b + Vector((r.uniform(-0.5, 0.5), r.uniform(-0.5, 0.5), h * 0.65))
    rod(mb, b, top, 0.3, M['trunk'], seg=7, r1=0.18)
    for k in range(4 if not willow else 5):
        c = top + Vector((r.uniform(-1.4, 1.4), r.uniform(-1.4, 1.4), r.uniform(0.0, h * 0.35)))
        lumpy(mb, c, r.uniform(1.3, 2.0) * h / 6, M['leaf'] if k % 2 else M['green'], 900 + seed * 7 + k, seg=10, rings=6, rough=0.3, squash=1.2 if willow else 0.85)

def _tent(mb, cards, F, w, d, h, M, mat, glow=None):
    """Ridge tent on poles (local x along the ridge, front opening at -y local end... the front gable faces local -x)."""
    def P_(x, y, z): return F.p(x, y, z)
    for sy in (-1, 1):
        mb.oface([P_(-w / 2, sy * d / 2, 0.2), P_(w / 2, sy * d / 2, 0.2), P_(w / 2, 0, h), P_(-w / 2, 0, h)], mat, [(0, 0), (w / 2, 0), (w / 2, 1.5), (0, 1.5)], tuple(F.Y * sy + F.Z))
    for sx in (-1, 1):
        mb.oface([P_(sx * w / 2, -d / 2, 0.2), P_(sx * w / 2, d / 2, 0.2), P_(sx * w / 2, 0, h)], mat, [(0, 0), (1, 0), (0.5, 1)], tuple(F.X * sx))
        if glow is not None and sx < 0:
            mb.oface([P_(sx * w / 2 - 0.02, -d / 4, 0.0), P_(sx * w / 2 - 0.02, d / 4, 0.0), P_(sx * w / 2 - 0.02, 0, h * 0.6)], glow, [(0, 0)] * 3, tuple(F.X * sx))
    rod(mb, P_(-w / 2 - 0.3, 0, 0), P_(-w / 2 - 0.3, 0, h + 0.4), 0.06, M['wood_d']); rod(mb, P_(w / 2 + 0.3, 0, 0), P_(w / 2 + 0.3, 0, h + 0.4), 0.06, M['wood_d'])

def _cart(mb, base, yaw, M, bricks=True, kind='plain'):
    F = Frame(base, yaw)
    F.box(mb, (-1.4, -0.9, 1.0), (1.4, 0.9, 1.2), M['wood'])
    for sy in (-1, 1): F.box(mb, (-1.4, sy * 0.9 - 0.05, 1.2), (1.4, sy * 0.9 + 0.05, 1.6), M['wood_d'])
    for sy in (-1, 1):
        c = F.p(0, sy * 1.05, 0.95); ax = F.Y * sy
        mb.frustum(c - ax * 0.08, c + ax * 0.08, 0.95, 0.95, M['wood_d'], seg=16)
        rod(mb, c - ax * 0.1, c + ax * 0.12, 0.18, M['iron'], seg=8)
    for sy in (-0.6, 0.6): beam(mb, F.p(1.4, sy, 1.1), F.p(3.4, sy * 0.8, 0.9), 0.1, 0.1, M['wood_d'])
    if bricks:
        mat = M['brick_' + kind]
        for k in range(3):
            for j in range(2): F.box(mb, (-1.2 + k * 0.85, -0.75 + j * 0.78, 1.2), (-0.45 + k * 0.85, -0.05 + j * 0.78, 1.55 + 0.1 * ((k + j) % 2)), mat)

def _brick_pile(mb, c, M, kind='plain', nx=4, ny=3, nz=4, seed=0):
    r = _rnd(seed); c = Vector(c); mat = M['brick_' + kind]; bw, bd, bh = 0.66, 0.34, 0.25
    mb.box((c.x - nx * bw / 2 - 0.1, c.y - ny * bd - 0.1, 0), (c.x + nx * bw / 2 + 0.1, c.y + ny * bd + 0.1, 0.12), M['wood_d'])
    for z in range(nz):
        for i in range(nx):
            for j in range(ny * 2):
                if z == nz - 1 and r.random() < 0.35: continue
                x0 = c.x - nx * bw / 2 + i * bw + (0.02 if z % 2 else 0.0); y0 = c.y - ny * bd + j * bd
                mb.box((x0 + 0.01, y0 + 0.01, 0.12 + z * bh), (x0 + bw - 0.02, y0 + bd - 0.01, 0.12 + (z + 1) * bh - 0.01), mat, tile=(4, 4))

def _trough(mb, c, w, d, M, paste):
    c = Vector(c); x0, x1, y0, y1 = c.x - w / 2, c.x + w / 2, c.y - d / 2, c.y + d / 2
    for (a, b) in (((x0, y0 - 0.12), (x1, y0)), ((x0, y1), (x1, y1 + 0.12))): mb.box((a[0], a[1], 0), (b[0], b[1], 0.7), M['wood'])
    for (a, b) in (((x0 - 0.12, y0 - 0.12), (x0, y1 + 0.12)), ((x1, y0 - 0.12), (x1 + 0.12, y1 + 0.12))): mb.box((a[0], a[1], 0), (b[0], b[1], 0.7), M['wood'])
    mb.quad((x0, y0, 0.55), (w, 0, 0), (0, d, 0), paste, (0, 0, w / 2, d / 2))

# ============================================================================= the wall
def _wall(SET, P, M):
    """Plinth, the two sections as stacks of course objects (set_wall_height shows / hides them), top dressing per section, the
    finished old wall (west) with crenels, the stub and the gate tower (east); crack overlays and impact decals."""
    pb = MB(); x0, x1 = OLD['x'][0], GATE['x'][1]
    pb.box((x0, -0.35, 0), (x1, WT + 0.35, PL), M['stone'], tile=(4, 2))
    _obj(pb, 'plinth', SET)
    STATE['courses'] = {}; STATE['topdress'] = {}
    for s, (a, b) in SEC.items():
        lst = []
        for k in range(NMAX):
            mb = MB(); z0 = PL + k * CH; mb.box((a, 0, z0), (b, WT, z0 + CH), M['brick_' + KIND[s]], tile=(4, 4))
            o = _obj(mb, 'course_%s_%02d' % (s, k), SET); lst.append(o)
        STATE['courses'][s] = lst
        # top dressing (moves with the height): rubble fill bed, a half-laid course of loose bricks with wet mortar, a mortar tub, tools
        td = MB(); r = _rnd(3 if s == 'lin' else 4); paste = M['mortar_' + KIND[s]]
        td.quad((a + 0.6, 0.8, 0.004), (b - a - 1.2, 0, 0), (0, WT - 1.6, 0), M['topbed'], (a / 4, 0.2, b / 4, (WT - 0.8) / 4))
        td.quad((a + 0.2, 0.15, 0.008), (b - a - 0.4, 0, 0), (0, 0.55, 0), paste, (0, 0, (b - a) / 2, 0.3))
        x = a + 0.4
        while x < b - 6:
            if r.random() < 0.75:
                td.box((x, 0.05, 0.0), (x + 1.28, 0.7, CH * 0.95), M['brick_' + KIND[s]], tile=(4, 4))
            x += 1.333
        for k in range(3):
            c = Vector((a + 3 + k * 6.5 + r.uniform(-1, 1), 3.2 + r.uniform(-0.8, 0.8), 0))
            for j in range(3): td.box((c.x + j * 0.7, c.y, 0.0), (c.x + j * 0.7 + 0.62, c.y + 0.32, 0.26), M['brick_' + KIND[s]], tile=(4, 4))
        D._bucket(td, (b - 4.5, 2.5, 0), M); td.quad((b - 4.75, 2.25, 0.5), (0.5, 0, 0), (0, 0.5, 0), paste)
        beam(td, (b - 3.4, 1.4, 0.04), (b - 2.8, 1.6, 0.04), 0.18, 0.03, M['iron']); beam(td, (b - 2.8, 1.6, 0.05), (b - 2.4, 1.75, 0.1), 0.05, 0.05, M['wood'])
        hx = b - 2.6 if s == 'lin' else a + 2.6                                     # a bamboo shear-leg hoist leaning out over the inner face
        top = Vector((hx, WT + 1.3, 4.2))
        for (dx, dy) in ((-1.1, 0.0), (1.1, 0.0)): _bamboo(td, (hx + dx, WT - 1.6, 0), top, M, r=0.06)
        _bamboo(td, (hx, 1.0, 0), top, M, r=0.06); rod(td, top - Vector((0, 0, 0.1)), top - Vector((0, 0, 2.6)), 0.015, M['rope'], seg=4)
        rod(td, top + Vector((-0.12, 0, -0.1)), top + Vector((0.12, 0, -0.1)), 0.16, M['wood_d'], seg=10)
        BK._basket(td, top - Vector((0, 0, 3.3)), 0.38, 0.5, dict(M, basket=M['straw'], basket_d=M['wood'], loaf=M['wood'], loaf_d=M['wood'], loaf_p=M['wood']), seed=3)
        bn = M['banner_red'] if s == 'general' else M['banner_blue']
        for x in ((a + 1.5, a + 7.0, a + 20.5) if s == 'general' else (a + 6.0, a + 15.0)):
            rod(td, (x, 0.45, 0), (x, 0.45, 6.5), 0.08, M['wood_d']); lumpy(td, (x, 0.45, 6.6), 0.14, M['gold'], 1, seg=8, rings=4, rough=0.0)
            for yy, nn in ((0.4, (0, -1, 0)), (0.5, (0, 1, 0))):
                td.oface([(x + 0.06, yy, 6.3), (x + 1.45, yy, 6.3), (x + 1.45, yy, 2.0), (x + 0.06, yy, 2.0)], bn, [(0, 1), (1, 1), (1, 0), (0, 0)], nn)
        o = _obj(td, 'top_' + s, SET, hull=0.015); STATE['topdress'][s] = o
    # finished old wall (west) and the stub (east) with crenels and a walkway
    ow = MB()
    for (xa, xb, h) in ((OLD['x'][0], OLD['x'][1], OLD['h']), (STUB['x'][0], STUB['x'][1], STUB['h'])):
        ow.box((xa, 0, PL), (xb, WT, h), M['brick_old'], tile=(4, 4))
        for yy in (0.0, WT - 0.5):
            x = xa
            while x < xb - 0.3:
                ow.box((x, yy, h), (min(xb, x + 0.5), yy + 0.5, h + 0.9), M['brick_old'], tile=(4, 4)); ow.box((x, yy, h + 0.9), (min(xb, x + 1.2), yy + 0.5, h + 1.0), M['brick_old'], tile=(4, 4))
                x += 1.2 if yy == 0.0 else 1.2
            ow.box((xa, yy, h), (xb, yy + 0.5, h + 0.45), M['brick_old'], tile=(4, 4))
        ow.quad((xa, 0.5, h + 0.002), (xb - xa, 0, 0), (0, WT - 1.0, 0), M['stone'], (xa / 4, 0, xb / 4, 1))
    # toothing at the west end of Lin's section (stepped bricks of the old wall)
    for k in range(int((OLD['h'] - PL) / CH)):
        z = PL + k * CH
        if k % 2 == 0: ow.box((OLD['x'][1], 0, z), (OLD['x'][1] + 0.66, WT, z + CH), M['brick_old'], tile=(4, 4))
    _obj(ow, 'old_wall', SET, hull=0.02)
    _gate(SET, P, M)
    # crack overlays (outer and inner face of each section) and the impact decals
    STATE['crack_mats'] = {}; STATE['decals'] = {}
    for s, (a, b) in SEC.items():
        cm = _mat_overlay(STATE['pre'] + 'cracks_' + s, P, STATE['tx']['cracks_' + s], STATE['tx']['cracks_%s_ord' % s]); STATE['crack_mats'][s] = cm
        ob = MB(); Hh = NMAX * CH
        ob.oface([(a, -0.015, PL), (b, -0.015, PL), (b, -0.015, PL + Hh), (a, -0.015, PL + Hh)], cm, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
        ob.oface([(a, WT + 0.015, PL), (b, WT + 0.015, PL), (b, WT + 0.015, PL + Hh), (a, WT + 0.015, PL + Hh)], cm, [(1, 0), (0, 0), (0, 1), (1, 1)], (0, 1, 0))
        o = _obj(ob, 'cracks_' + s, SET, shadow=False); STATE.setdefault('crack_objs', {})[s] = o
        dm = _mat_decal(STATE['pre'] + 'dent_' + s, P, STATE['tx']['dent_' + ('plain' if s == 'general' else 'rice')])
        lst = []
        for i, (lx, lz) in enumerate(IMPACTS[s]):
            c = Vector((a + lx, -0.025, PL + lz)); R = 1.15 if s == 'general' else 0.95
            dm_i = dm.copy(); dm_i.name = '%sdent_%s_%d' % (STATE['pre'], s, i)
            db = MB(); db.oface([c + Vector((-R, 0, -R)), c + Vector((R, 0, -R)), c + Vector((R, 0, R)), c + Vector((-R, 0, R))], dm_i, [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
            o = _obj(db, 'dent_%s_%d' % (s, i), SET, shadow=False)
            bb = MB(); bb.sphere(c + Vector((0, 0.12, 0)), 0.42, M['cannonball'], seg=14, rings=8); ball_fixed = _obj(bb, 'ball_in_%s_%d' % (s, i), SET)
            lst.append(dict(decal=o, mat=dm_i, c=c, ball_in=ball_fixed))
        STATE['decals'][s] = lst

def _gate(SET, P, M):
    """Gate tower: a battered brick base 15 D high over an arched tunnel (dark, a warm lantern glow inside), crenellated parapet, a red
    two-storey pavilion with lattice windows glowing warm, double-eave hip roofs with swept corners, lanterns at the eaves."""
    (xa, xb), (ya, yb), H = GATE['x'], GATE['y'], GATE['h']; cx = GATE['cx']; aw, ah = GATE['arch_w'], GATE['arch_h']
    mb = MB(); fl = MB(); cards = MB()
    # base: two piers and the lintel block above the arch (the arch is a rounded opening)
    mb.box((xa, ya, PL), (cx - aw / 2, yb, H), M['brick_old'], tile=(4, 4)); mb.box((cx + aw / 2, ya, PL), (xb, yb, H), M['brick_old'], tile=(4, 4))
    mb.box((cx - aw / 2, ya, PL + ah + aw / 2), (cx + aw / 2, yb, H), M['brick_old'], tile=(4, 4))
    mb.box((xa - 0.4, ya - 0.4, 0), (xb + 0.4, yb + 0.4, PL), M['stone'], tile=(4, 2))
    for yy, nn in ((ya - 0.01, (0, -1, 0)), (yb + 0.01, (0, 1, 0))):                    # arch spandrels on both faces + the soffit
        n = 12; pts = [(cx + aw / 2 * math.cos(math.pi * k / n), PL + ah + aw / 2 * math.sin(math.pi * k / n)) for k in range(n + 1)]
        for k in range(n):
            (x0_, z0_), (x1_, z1_) = pts[k], pts[k + 1]
            mb.oface([(x0_, yy, z0_), (x1_, yy, z1_), (x1_, yy, PL + ah + aw / 2), (x0_, yy, PL + ah + aw / 2)], M['brick_old'], [(x0_ / 4, z0_ / 4), (x1_ / 4, z1_ / 4), (x1_ / 4, (PL + ah + aw / 2) / 4), (x0_ / 4, (PL + ah + aw / 2) / 4)], nn)
            mb.oface([(x0_, ya, z0_), (x1_, ya, z1_), (x1_, yb, z1_), (x0_, yb, z0_)], M['stone'], [(0, 0), (0.3, 0), (0.3, 2), (0, 2)], (-(x0_ + x1_ - 2 * cx), 0, -(z0_ + z1_ - 2 * (PL + ah))))
        for k in range(n + 1):                                                       # voussoir ring (stone)
            x_, z_ = pts[k]; d_ = Vector((x_ - cx, 0, z_ - PL - ah)).normalized()
            mb.box((x_ - 0.15, yy - 0.08 * (1 if nn[1] < 0 else -1) - 0.04, z_ - 0.15), (x_ + 0.15, yy + 0.04, z_ + 0.15), M['stone'])
    for sx in (-1, 1): mb.oface([(cx + sx * aw / 2, ya, PL), (cx + sx * aw / 2, yb, PL), (cx + sx * aw / 2, yb, PL + ah), (cx + sx * aw / 2, ya, PL + ah)], M['stone'], [(0, 0), (2, 0), (2, 2), (0, 2)], (-sx, 0, 0))
    mb.quad((cx - aw / 2, ya, PL), (aw, 0, 0), (0, yb - ya, 0), M['stone'], (0, 0, 1, 2))
    # the gate doors (half open, studded) and the warm glow of the inner yard through the tunnel
    for sx in (-1, 1):
        xa_, xb_ = sorted((cx + sx * (aw / 2 - 0.18), cx + sx * aw / 2)); mb.box((xa_, (ya + yb) / 2 - 0.1, PL), (xb_, (ya + yb) / 2 + 1.9, PL + ah), M['red_d'])
    # parapet with crenels
    for (u0, u1, v) in ((xa, xb, ya), (xa, xb, yb - 0.5)):
        x = u0
        while x < u1 - 0.3: mb.box((x, v, H), (min(u1, x + 0.6), v + 0.5, H + 1.0), M['brick_old'], tile=(4, 4)); x += 1.25
        mb.box((u0, v, H), (u1, v + 0.5, H + 0.5), M['brick_old'], tile=(4, 4))
    mb.quad((xa, ya, H + 0.002), (xb - xa, 0, 0), (0, yb - ya, 0), M['stone'], (0, 0, 3, 2))
    # pavilion: platform, red columns, walls with lattice windows (glowing), double roof
    px0, px1, py0, py1 = xa + 2.0, xb - 2.0, ya + 1.6, yb - 1.6; zf = H + 0.3
    mb.box((px0 - 0.4, py0 - 0.4, H), (px1 + 0.4, py1 + 0.4, zf), M['stone'])
    ncol = 6
    for i in range(ncol):
        x = px0 + (px1 - px0) * i / (ncol - 1)
        for y in (py0, py1): rod(mb, (x, y, zf), (x, y, zf + 4.0), 0.22, M['red'], seg=8)
    for (y, nn) in ((py0 + 0.3, (0, -1, 0)), (py1 - 0.3, (0, 1, 0))):
        mb.oface([(px0, y, zf), (px1, y, zf), (px1, y, zf + 4.0), (px0, y, zf + 4.0)], M['red_d'], [(0, 0)] * 4, nn)
        for i in range(ncol - 1):
            x0_ = px0 + (px1 - px0) * i / (ncol - 1) + 0.35; x1_ = px0 + (px1 - px0) * (i + 1) / (ncol - 1) - 0.35; dy = -0.02 if nn[1] < 0 else 0.02
            fl.oface([(x0_, y + dy, zf + 1.2), (x1_, y + dy, zf + 1.2), (x1_, y + dy, zf + 3.4), (x0_, y + dy, zf + 3.4)], M['win_glow'], [(0, 0)] * 4, nn)
            for k in range(5):
                xx = x0_ + (x1_ - x0_) * (k + 0.5) / 5; mb.box((xx - 0.035, y + dy * 2 - 0.03, zf + 1.2), (xx + 0.035, y + dy * 2 + 0.03, zf + 3.4), M['lattice'])
            for k in range(4):
                zz = zf + 1.2 + 2.2 * (k + 0.5) / 4; mb.box((x0_, y + dy * 2 - 0.03, zz - 0.035), (x1_, y + dy * 2 + 0.03, zz + 0.035), M['lattice'])
    for x in (px0 + 0.3, px1 - 0.3): mb.oface([(x, py0, zf), (x, py1, zf), (x, py1, zf + 4), (x, py0, zf + 4)], M['red_d'], [(0, 0)] * 4, (1 if x > cx else -1, 0, 0))
    beam(mb, (px0 - 0.2, py0, zf + 4.0), (px1 + 0.2, py0, zf + 4.0), 0.35, 0.4, M['red_d']); beam(mb, (px0 - 0.2, py1, zf + 4.0), (px1 + 0.2, py1, zf + 4.0), 0.35, 0.4, M['red_d'])
    hx, hy = (px1 - px0) / 2, (py1 - py0) / 2
    _cn_roof(mb, cx, (py0 + py1) / 2, hx, hy, zf + 4.1, 1.3, 1.6, 0.9, M, ridge=False)
    mb.box((px0 + 1.0, py0 + 0.8, zf + 4.4), (px1 - 1.0, py1 - 0.8, zf + 6.4), M['red_d'])
    for i in range(4):
        x = px0 + 1.0 + (px1 - px0 - 2.0) * (i + 0.5) / 4
        fl.oface([(x - 0.7, py0 + 0.78, zf + 4.8), (x + 0.7, py0 + 0.78, zf + 4.8), (x + 0.7, py0 + 0.78, zf + 6.0), (x - 0.7, py0 + 0.78, zf + 6.0)], M['win_glow'], [(0, 0)] * 4, (0, -1, 0))
    _cn_roof(mb, cx, (py0 + py1) / 2, hx - 1.0, hy - 0.8, zf + 6.4, 2.6, 1.8, 1.0, M, ridge=True)
    lamps = []
    for (x, y) in ((px0 - 1.0, py0 - 1.2), (px1 + 1.0, py0 - 1.2), (px0 - 1.0, py1 + 1.2), (px1 + 1.0, py1 + 1.2)):
        lamps.append(_cn_lantern(mb, fl, cards, (x, y, zf + 3.0), M, s=0.9, hang=0.9))
    for (x, y) in ((cx - aw / 2 - 1.0, ya - 0.5), (cx + aw / 2 + 1.0, ya - 0.5), (cx - aw / 2 - 1.0, yb + 0.5), (cx + aw / 2 + 1.0, yb + 0.5)):
        beam(mb, (x, y + (0.5 if y < 0 else -0.5), PL + 6.0), (x, y, PL + 6.0), 0.08, 0.08, M['wood_d'])
        lamps.append(_cn_lantern(mb, fl, cards, (x, y, PL + 5.1), M, s=0.85, hang=0.5))
    # banners on the parapet
    for x in (xa + 1.0, xb - 1.0):
        rod(mb, (x, ya + 0.25, H + 0.5), (x, ya + 0.25, H + 6.5), 0.07, M['wood_d']); mb.oface([(x + 0.05, ya + 0.25, H + 6.3), (x + 1.25, ya + 0.25, H + 6.3), (x + 1.25, ya + 0.25, H + 2.7), (x + 0.05, ya + 0.25, H + 2.7)], M['banner_red'], [(0, 1), (1, 1), (1, 0), (0, 0)], (0, -1, 0))
    _obj(mb, 'gate_tower', SET, hull=0.02); _obj(fl, 'gate_glow', SET, shadow=False); _obj(cards, 'gate_halos', SET, shadow=False)
    lk = P['lamps']
    _flame_light('gate_lamp_out', (cx, ya - 1.8, PL + 4.8), LAMP, 120.0 * lk, radius=0.5); _flame_light('gate_lamp_in', (cx, yb + 1.8, PL + 4.8), LAMP, 120.0 * lk, radius=0.5)
    _flame_light('gate_pavilion', (cx, py0 - 1.6, zf + 2.6), LAMP, 90.0 * lk, radius=0.5)
    STATE['marks']['gate'] = (cx, yb + 2.0, 0.0)

# ============================================================================= ground, field, river, scenery
def _ground(SET, P, M):
    g = MB(); R = 150.0
    def q(a, b, c, d, mat, tile=4.0, z=0.0): g.quad((a, c, z), (b - a, 0, 0), (0, d - c, 0), mat, (a / tile, c / tile, b / tile, d / tile))
    y0, y1 = RIVER
    q(-R, R, y1, -0.3, M['field'], 6.0); q(-R, R, -R, y0, M['field'], 6.0)
    q(-R, R, WT + 0.3, R, M['field'], 6.0); q(-R, R, -0.3, WT + 0.3, M['field'], 6.0)
    _obj(g, 'field', SET)
    s = MB(); r = _rnd(77)
    pts = []
    for i in range(48):                                                            # the trodden site: an irregular blob inside the wall
        a = 2 * math.pi * i / 48; rx, ry = 44.0, 24.0; k = 1 + 0.08 * math.sin(5 * a) + r.uniform(-0.04, 0.04)
        pts.append(Vector((3.0 + rx * k * math.cos(a), 20.0 + ry * k * math.sin(a), 0.004)))
    pts = [Vector((p.x, max(WT + 0.3, p.y), p.z)) for p in pts]
    s.face(pts, M['ground'], [(p.x / 4, p.y / 4) for p in pts])
    s.quad((-60.0, -6.0, 0.004), (100.0, 0, 0), (0, 5.7, 0), M['ground'], (-15, -1.5, 10, 0))      # trodden strip outside the wall
    s.quad((GATE['cx'] - 2.5, y1 + 0.5, 0.005), (5.0, 0, 0), (0, -6.0 - y1 - 0.5, 0), M['ground'], (0, 0, 1.25, 10))   # the road to the river
    _obj(s, 'site_ground', SET)
    w = MB(); w.quad((-R, y0, -0.25), (2 * R, 0, 0), (0, y1 - y0, 0), M['water'], (0, 0, 2 * R / 4, (y1 - y0) / 4)); _obj(w, 'river', SET, shadow=False)
    b = MB()
    for yy, n in ((y0, (0, 1, 0)), (y1, (0, -1, 0))): b.oface([(-R, yy, -0.6), (R, yy, -0.6), (R, yy, 0.0), (-R, yy, 0.0)], M['ground'], [(0, 0), (60, 0), (60, 0.2), (0, 0.2)], n)
    _obj(b, 'river_banks', SET)
    # trees along the river and round the site, a bridge
    t = MB(); r = _rnd(5)
    for k in range(22):
        x = -70 + k * 7.0 + r.uniform(-2, 2); _tree(t, (x, y1 + 2.5 + r.uniform(0, 3), 0), M, h=r.uniform(5, 8), seed=k, willow=True)
    for k in range(10):
        x = -60 + k * 13 + r.uniform(-3, 3); _tree(t, (x, y0 - 3 - r.uniform(0, 4), 0), M, h=r.uniform(5, 8), seed=40 + k)
    for (x, y) in ((-38, 34), (-30, 42), (38, 30), (44, 22), (-46, 18), (26, 44), (-12, 47), (8, 49)): _tree(t, (x, y, 0), M, h=r.uniform(6, 9), seed=int(x * 3 + y))
    bx = GATE['cx']
    t.box((bx - 2.4, y0 - 1.0, 0.3), (bx + 2.4, y1 + 1.0, 0.65), M['wood'])
    for yy in (y0 + 2, (y0 + y1) / 2, y1 - 2):
        for sx in (-1.8, 1.8): rod(t, (bx + sx, yy, -0.8), (bx + sx, yy, 0.4), 0.18, M['wood_d'])
    for yy in (y0 - 1.0, y1 + 1.0): pass
    for sx in (-2.3, 2.3): beam(t, (bx + sx, y0 - 1.0, 1.4), (bx + sx, y1 + 1.0, 1.4), 0.1, 0.12, M['red_d'])
    _obj(t, 'scenery', SET, hull=0.03)
    if P.get('wet', 0) > 0:                                                         # RAIN: puddles mirror the sky
        pb = MB(); r = _rnd(31)
        for k in range(26):
            c = Vector((r.uniform(-28, 26), r.uniform(6.5, 30) if k < 18 else r.uniform(-14, -1.5), 0.012)); n = 14; rr = r.uniform(0.8, 2.4)
            pts = [c + Vector((rr * (1 + 0.25 * math.sin(3 * a + k)) * math.cos(a) * 1.5, rr * (1 + 0.2 * math.cos(2 * a + k)) * math.sin(a), 0)) for a in [2 * math.pi * i / n for i in range(n)]]
            pb.face(pts, M['puddle'], [(p.x / 4, p.y / 4) for p in pts])
        _obj(pb, 'puddles', SET, shadow=False)

# ============================================================================= the construction site
def _scaffold(mb, M, x0, x1, top, plats):
    """Bamboo scaffold along the inner face (y 5.4 .. 7.2): standards every 2.6 D, ledgers, braces, plank platforms at `plats`."""
    ys = (WT + 0.45, WT + 2.1); n = int((x1 - x0) / 2.6)
    xs = [x0 + (x1 - x0) * i / n for i in range(n + 1)]
    for x in xs:
        for y in ys: _bamboo(mb, (x, y, 0), (x, y, top), M)
    z = 2.0
    while z < top - 0.5:
        for y in ys: _bamboo(mb, (x0 - 0.3, y, z), (x1 + 0.3, y, z), M, r=0.06)
        z += 2.0
    for i in range(0, n, 2): _bamboo(mb, (xs[i], ys[1] + 0.08, 0.3), (xs[i + 1], ys[1] + 0.08, min(top, 6.0)), M, r=0.055)
    for zp in plats:
        for k in range(4): mb.box((x0, ys[0] + 0.05 + k * 0.42, zp), (x1, ys[0] + 0.43 + k * 0.42, zp + 0.08), M['wood_l'] if k % 2 else M['wood'])
        for x in xs[::2]: mb.box((x - 0.05, ys[0], zp + 0.08), (x + 0.05, ys[1], zp + 0.12), M['rope'])

def _cauldron(SET, P, M, mb, fl, cards, lamps):
    """The giant rice-soup cauldron: a round brick stove with a glowing fire mouth (facing +y, the camera side) and fire licking round
    the rim, a huge iron wok of milky rice soup with a paddle, Lin's stirring platform on the wall side, sacks of rice, firewood."""
    c = Vector((-11.0, 13.5, 0)); Rs = 3.0; hs = 1.7
    rod(mb, c, c + Vector((0, 0, hs)), Rs, M['brick_old'], seg=28, uv=(2 * math.pi * Rs / 4, hs / 4))
    for k in range(10):                                                            # the fire mouth (an arch of glowing embers + a dark lintel)
        a = math.pi / 2 + (k - 4.5) * 0.08
    F = Frame(c + Vector((0, Rs - 0.02, 0)), 180.0)
    fl.oface([F.p(-0.9, -0.03, 0.15), F.p(0.9, -0.03, 0.15), F.p(0.9, -0.03, 1.15), F.p(0, -0.03, 1.45), F.p(-0.9, -0.03, 1.15)], M['stove_glow'], [(0, 0)] * 5, tuple(-F.Y))
    for k in range(6):
        q = F.p(-0.65 + 0.26 * k, -0.15, 0.55 + 0.12 * (k % 2)); lumpy(fl, q, 0.22 + 0.06 * (k % 3), M['fire'], 40 + k, seg=8, rings=6, rough=0.35, squash=2.0)
    beam(mb, F.p(-1.2, -0.12, 1.5), F.p(1.2, -0.12, 1.5), 0.3, 0.3, M['stone'])
    for k in range(5): beam(mb, F.p(-0.7 + 0.35 * k, -0.4, 0.15), F.p(-0.5 + 0.3 * k, -1.6, 0.12), 0.18, 0.18, M['wood_d'])
    # flames licking round the rim
    r = _rnd(12)
    fl.frustum(c + Vector((0, 0, hs)), c + Vector((0, 0, hs + 0.22)), Rs - 0.12, Rs - 0.35, M['stove_glow'], seg=32, cap0=False, cap1=False)   # glowing gap under the wok
    for k in range(8):                                                        # little tongues of fire licking out of the gap
        a = 2 * math.pi * k / 8 + r.uniform(0, 0.25); q = c + Vector(((Rs - 0.2) * math.cos(a), (Rs - 0.2) * math.sin(a), hs + 0.12))
        lumpy(fl, q, r.uniform(0.09, 0.15), M['fire'], 60 + k, seg=8, rings=6, rough=0.35, squash=2.4)
    # the wok: lathe of rings (outer iron, inner dark), the soup surface
    prof = [(hs - 0.2, 1.0), (hs + 0.2, 1.9), (hs + 0.6, 2.45), (hs + 1.0, 2.75), (hs + 1.15, 2.85)]
    for (z0, r0), (z1, r1) in zip(prof, prof[1:]):
        mb.frustum(c + Vector((0, 0, z0)), c + Vector((0, 0, z1)), r0, r1, M['iron'], seg=32, cap0=False, cap1=False)
    mb.frustum(c + Vector((0, 0, hs + 1.15)), c + Vector((0, 0, hs + 1.3)), 2.95, 2.95, M['iron'], seg=32, cap0=False, cap1=False)
    for (ra, rb_) in ((2.85, 2.95),):
        n_ = 32
        for i in range(n_):
            a0, a1 = 2 * math.pi * i / n_, 2 * math.pi * (i + 1) / n_
            mb.face([c + Vector((ra * math.cos(a0), ra * math.sin(a0), hs + 1.3)), c + Vector((rb_ * math.cos(a0), rb_ * math.sin(a0), hs + 1.3)), c + Vector((rb_ * math.cos(a1), rb_ * math.sin(a1), hs + 1.3)), c + Vector((ra * math.cos(a1), ra * math.sin(a1), hs + 1.3))], M['iron'])
    for sx in (-1, 1): rod(mb, c + Vector((sx * 2.9, 0, hs + 1.1)), c + Vector((sx * 3.4, 0, hs + 1.15)), 0.12, M['iron'], seg=6)
    sp = MB(); zs = hs + 0.95; n = 32
    sp.face([c + Vector((2.68 * math.cos(2 * math.pi * i / n), 2.68 * math.sin(2 * math.pi * i / n), zs)) for i in range(n)], M['soup'],
            [(0.5 + 0.9 * math.cos(2 * math.pi * i / n), 0.5 + 0.9 * math.sin(2 * math.pi * i / n)) for i in range(n)])
    for k in range(9):                                                             # bubbles / lumps of rice
        a = r.uniform(0, 6.28); d = r.uniform(0.2, 2.2); lumpy(sp, c + Vector((d * math.cos(a), d * math.sin(a), zs)), r.uniform(0.08, 0.2), M['soup'], 30 + k, seg=8, rings=4, rough=0.1, squash=0.5)
    o = _obj(sp, 'soup', SET); o['glossy_vis'] = 1
    # the paddle (resting in the soup, leaning toward Lin's platform) and the platform
    p0 = c + Vector((-0.9, -0.2, zs - 0.3)); p1 = c + Vector((-3.6, 0.1, 5.6)); rod(mb, p0, p1, 0.09, M['wood_l'], seg=6)
    beam(mb, p0 - Vector((0, 0, 0.3)), p0 + Vector((-0.35, 0.0, 0.4)), 0.6, 0.08, M['wood_l'])
    pf0 = c + Vector((-Rs - 2.0, -1.6, 0)); mb.box(pf0, pf0 + Vector((1.7, 3.2, 1.5)), M['wood'])     # Lin's platform beside the wok (-x side)
    for k in range(3): mb.box(pf0 + Vector((0.15, 3.2 + 0.5 * k, 0)), pf0 + Vector((1.55, 3.7 + 0.5 * k, 1.5 - 0.5 * k)), M['wood_l'])
    STATE['marks']['lin_stir'] = tuple(round(v, 3) for v in (pf0.x + 0.85, pf0.y + 1.4, 1.5))
    # rice sacks, baskets, firewood, a bucket of rice soup, ladles
    for k, (dx, dy) in enumerate(((-4.6, 3.6), (-5.4, 2.6), (-3.8, 4.3), (-5.8, 3.9), (-4.9, 5.0))):
        lumpy(mb, c + Vector((dx, dy, 0.55)), 0.62, M['sack'], 50 + k, seg=10, rings=6, rough=0.12, squash=1.1)
    for k in range(3): D._bucket(mb, c + Vector((3.8 + k * 0.7, -2.0 + 0.4 * k, 0)), M); fl.quad(c + Vector((3.55 + k * 0.7, -2.25 + 0.4 * k, 0.52)), (0.5, 0, 0), (0, 0.5, 0), M['soup']) if False else None
    for k in range(3): mb.quad(c + Vector((3.55 + k * 0.7, -2.25 + 0.4 * k, 0.5)), (0.5, 0, 0), (0, 0.5, 0), M['soup'])
    for k in range(12):
        z = 0.18 + 0.32 * (k // 4); y = c.y - 3.6 + (k % 4) * 0.34
        rod(mb, (c.x + 3.0, y, z), (c.x + 5.5, y, z), 0.16, M['wood_d'] if k % 2 else M['trunk'], seg=6)
    lamps.append(('fire', c + Vector((0, Rs + 0.6, 0.9)), 300.0, FIRE, True))
    lamps.append(('fire', c + Vector((0, 0, hs + 1.8)), 120.0, FIRE, False))
    _halo(cards, c + Vector((0, Rs + 0.3, 0.8)), 2.2, M, key='halo_big')
    # steam over the soup (set_cauldron_steam): soft white billows rising and swelling from the soup, recycled while tiny
    sm = _mat_dust(STATE['pre'] + 'steam_balls', P['steam_rgb'], 1.15); balls = []
    for j in range(9):
        bb = MB(); lumpy(bb, (0, 0, 0), 1.0, sm, 820 + j, seg=14, rings=9, rough=0.3); o = _smooth(_obj(bb, 'steam_%d' % j, SET, shadow=False))
        a_ = 2 * math.pi * j / 9; balls.append(dict(ob=o, base=c + Vector((1.2 * math.cos(a_), 1.2 * math.sin(a_), zs)), H=7.5, ph=j / 9.0 + r.uniform(0, 0.05), size=r.uniform(0.9, 1.3), drift=Vector((r.uniform(0.5, 1.5), r.uniform(-1.2, 0.0), 0))))
    STATE['steam'] = balls; STATE['steam_mat'] = sm
    STATE['cauldron'] = dict(centre=tuple(c), rim_z=hs + 1.3, soup_z=zs, radius=2.85)

def _site(SET, P, M, dress, PR):
    _ground(SET, P, M); _wall(SET, P, M)
    mb = MB(); fl = MB(); cards = MB(); lamps = []
    if dress:
        _cauldron(SET, P, M, mb, fl, cards, lamps)
        _scaffold(mb, M, -21.0, -12.0, 14.5, (5.0, 10.0)); _scaffold(mb, M, 12.5, 21.5, 17.0, (6.0, 12.0))
        # plank ramp up the general's scaffold
        a, b = Vector((3.5, 8.0, 0.0)), Vector((11.3, 8.0, 6.0)); d = (b - a).normalized()
        for k in range(3): beam(mb, a + Vector((0, -0.45 + 0.45 * k, 0.05)), b + Vector((0, -0.45 + 0.45 * k, 0.05)), 0.4, 0.08, M['wood'])
        for k in range(10): q = a.lerp(b, (k + 0.5) / 10); beam(mb, q + Vector((0, -0.7, 0.12)), q + Vector((0, 0.7, 0.12)), 0.08, 0.06, M['wood_d'])
        for t_ in (0.35, 0.7): q = a.lerp(b, t_); rod(mb, q + Vector((0, -0.6, -q.z)), q + Vector((0, -0.6, 0)), 0.08, M['wood_d']); rod(mb, q + Vector((0, 0.6, -q.z)), q + Vector((0, 0.6, 0)), 0.08, M['wood_d'])
        for (x, kind) in ((-2.6, 'rice'), (3.0, 'plain')):                         # ladders against the inner face near the seam
            top = 9.5 if kind == 'rice' else 11.0
            for sx in (-0.45, 0.45): _bamboo(mb, (x + sx, WT + 3.0, 0), (x + sx, WT + 0.15, top), M, r=0.06)
            for k in range(int(top / 0.9)):
                t_ = (k + 0.5) / int(top / 0.9); q = Vector((x, WT + 3.0 - 2.85 * t_, top * t_)); _bamboo(mb, q - Vector((0.45, 0, 0)), q + Vector((0.45, 0, 0)), M, r=0.035)
        # mortar troughs and lime pits: Lin's creamy rice mortar, the general's grey mortar
        _trough(mb, (-5.2, 9.6), 3.2, 1.6, M, M['mortar_rice']); _trough(mb, (8.2, 9.8), 3.2, 1.6, M, M['mortar_plain'])
        for (cx_, cy_, w_, d_) in ((-18.0, 10.5, 3.6, 2.4), (17.2, 11.5, 3.6, 2.4)):
            mb.box((cx_ - w_ / 2 - 0.3, cy_ - d_ / 2 - 0.3, 0), (cx_ + w_ / 2 + 0.3, cy_ + d_ / 2 + 0.3, 0.35), M['stone'])
            mb.quad((cx_ - w_ / 2, cy_ - d_ / 2, 0.3), (w_, 0, 0), (0, d_, 0), M['lime'], (0, 0, w_ / 2, d_ / 2))
            beam(mb, (cx_ - 1.0, cy_ - 0.2, 0.32), (cx_ + 1.8, cy_ + 2.4, 2.0), 0.08, 0.08, M['wood'])
        D._bucket(mb, (-3.0, 8.8, 0), M); mb.quad((-3.25, 8.55, 0.5), (0.5, 0, 0), (0, 0.5, 0), M['soup'])
        _brick_pile(mb, (-1.5, 12.5), M, 'rice', seed=1); _brick_pile(mb, (4.0, 13.0), M, 'plain', nx=5, seed=2); _brick_pile(mb, (13.5, 14.0), M, 'plain', seed=3); _brick_pile(mb, (-20.0, 14.5), M, 'rice', nx=3, seed=4)
        _cart(mb, (-21.5, 15.0, 0), 75.0, M, kind='rice'); _cart(mb, (16.0, 17.5, 0), -20.0, M, kind='plain')
        for k, (x, y) in enumerate(((-13.6, 8.2), (-12.6, 8.0), (14.0, 9.6))): _bamboo(mb, (x, y, 0), (x + 0.3, y - 0.2, 3.4), M, r=0.05)
        # tents (workers) and the general's command tent
        for k, (x, y, yaw) in enumerate(((-24.0, 26.0, 90.0), (-17.0, 28.5, 90.0), (-10.0, 27.0, 90.0), (16.0, 27.5, 90.0), (23.0, 25.5, 90.0))):
            _tent(mb, cards, Frame((x, y, 0), yaw), 4.0, 3.6, 2.8, M, M['canvas'], glow=M['tent_glow'])
        _tent(mb, cards, Frame((5.0, 28.0, 0), 90.0), 5.5, 5.0, 3.8, M, M['canvas_b'], glow=M['tent_glow'])
        # lantern poles along the path, braziers, torches on the scaffolds
        for k, x in enumerate((-27.0, -20.0, -2.5, 7.5, 16.0, 25.0)):
            f = _lantern_pole(mb, fl, cards, (x, 19.0, 0), M, arm=(0.9 if k % 2 else -0.9, 0.0)); lamps.append(('lamp', f, 40.0, LAMP, False))
        for (x, y) in ((-3.0, 14.8), (11.0, 18.5), (-22.0, 19.5)):
            f = D._brazier(mb, fl, cards, (x, y, 0), M, s=1.1); lamps.append(('fire', f, 150.0, FIRE, (x, y) == (11.0, 18.5)))
        for (x, z) in ((-16.0, 9.6), (16.5, 11.6)):
            p = Vector((x, WT + 2.2, z)); rod(mb, p, p + Vector((0, 0.3, 1.2)), 0.05, M['wood_d']); q = p + Vector((0, 0.32, 1.3))
            fl.frustum(q, q + Vector((0, 0, 0.6)), 0.14, 0.0, M['flame'], seg=6, cap1=False); _halo(cards, q + Vector((0, 0, 0.3)), 0.9, M); lamps.append(('lamp', q + Vector((0, 0, 0.3)), 35.0, FIRE, False))
        # baskets, jars, rakes along the foot of the wall (outside too)
        r = _rnd(21)
        for k in range(10):
            x = r.uniform(-20, 20); y = r.uniform(7.6, 8.4); BK._basket(mb, (x, y, 0), 0.45, 0.5, dict(M, basket=M['straw'], basket_d=M['wood'], loaf=M['brick_old'], loaf_d=M['brick_old'], loaf_p=M['brick_old']), seed=k)
        for k in range(4): D._jar(mb, (-8.0 + 0.9 * k, 12.4 + 0.2 * (k % 2), 0), dict(M, terra=C_terra(), terra_d=C_terra(True), dark=M['dark']), h=1.3, r=0.45)
    _obj(mb, 'site_props', SET, hull=0.015); _obj(fl, 'site_glow', SET, shadow=False); _obj(cards, 'site_halos', SET, shadow=False)
    for i, (kind, f, e, rgb, sh) in enumerate(lamps):
        _flame_light('%s_%d' % (kind, i), tuple(f), rgb, e * (P['lamps'] if kind != 'fire' else max(0.5, P['lamps'])), radius=0.3 if kind == 'fire' else 0.15, shadow=sh)
    _army(SET, P, M)
    _fx(SET, P, M)
    _sky_and_haze(SET, P, M)
    STATE['marks'].update(lin_trough=(-5.2, 11.2, 0.0), general_trough=(8.2, 11.4, 0.0), lin_wallfoot=(-4.5, 8.4, 0.0), general_wallfoot=(5.0, 8.6, 0.0),
                          workers=[(-2.6, 10.8, 0.0), (5.8, 14.6, 0.0), (7.4, 14.0, 0.0)], general_cauldron=(-6.4, 15.0, 0.0), ramp=[(3.5, 8.0, 0.0), (11.3, 8.0, 6.0)],
                          outer_foot=[(-11.0, -3.0, 0.0), (11.0, -3.0, 0.0)])

def C_terra(dark=False): return STATE['C']('#8a4a2a' if dark else '#b8683e', 1.0, (1.4, 1.0, 0.8), smix=0.4)

def _sky_and_haze(SET, P, M):
    D._sky(SET, dict(P, haze=None), M)
    if P.get('haze'):
        hm = G._haze_mat(STATE['pre'] + 'haze', P['haze'][0], P['haze'][1], 0.0, 26.0); mb = MB()
        for Rh in (90.0, 112.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64
                mb.face([Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        _obj(mb, 'haze', SET, shadow=False)

# ============================================================================= the enemy army (field side)
def _cannon(mb, fl, base, M, i):
    b = Vector(base); F = Frame(b, 0.0)                                   # barrel along +y
    for sx in (-1, 1): F.box(mb, (sx * 0.55 - 0.1, -1.6, 0.25), (sx * 0.55 + 0.1, 1.2, 1.15), M['wood'])
    F.box(mb, (-0.55, -1.0, 0.35), (0.55, 0.8, 0.55), M['wood_d']); beam(mb, F.p(0, -1.6, 0.4), F.p(0, -3.2, 0.05), 0.35, 0.2, M['wood'])
    for sx in (-1, 1):
        c = F.p(sx * 0.82, 0.1, 0.8); ax = Vector((sx, 0, 0))
        mb.frustum(c - ax * 0.09, c + ax * 0.09, 0.8, 0.8, M['wood_d'], seg=16)
        for k in range(6):
            a = math.pi * k / 6; d = Vector((0, math.cos(a), math.sin(a))) * 0.78; rod(mb, c - d, c + d, 0.045, M['wood'], seg=4)
        rod(mb, c - ax * 0.12, c + ax * 0.15, 0.18, M['iron'], seg=8)
    p0, p1 = F.p(0, -1.2, 1.25), F.p(0, 1.9, 1.45)
    mb.frustum(p0, p1, 0.42, 0.3, M['bronze'], seg=14); rod(mb, p1, p1 + (p1 - p0).normalized() * 0.18, 0.36, M['bronze'], seg=14)
    lumpy(mb, p0 - (p1 - p0).normalized() * 0.15, 0.3, M['bronze'], 3, seg=10, rings=5, rough=0.0)
    for t_ in (0.25, 0.6): q = p0.lerp(p1, t_); rod(mb, q - (p1 - p0).normalized() * 0.06, q + (p1 - p0).normalized() * 0.06, 0.4 - 0.1 * t_, M['bronze'], seg=14)
    rod(mb, p1 + (p1 - p0).normalized() * 0.17, p1 + (p1 - p0).normalized() * 0.19, 0.2, M['dark'], seg=10)
    for k in range(5): lumpy(mb, F.p(1.5 + 0.35 * (k % 3), -0.8 + 0.35 * (k // 3), 0.22 + 0.0), 0.22, M['cannonball'], 70 + k, seg=8, rings=5, rough=0.0)
    D._bucket(mb, F.p(-1.6, -1.2, 0), M); rod(mb, F.p(-1.4, -0.2, 0), F.p(-1.6, 0.6, 2.6), 0.035, M['wood'])
    return p1 + (p1 - p0).normalized() * 0.2

def _army(SET, P, M):
    """The enemy: six bronze cannons on wheeled carriages in a line facing the wall (y -22), shot piles, wicker gabions, black and red
    banners, the camp beyond (tents, camp fires) - shown by set_army(True) (BATTLE presets)."""
    mb = MB(); fl = MB(); cards = MB(); muzzles = []; lamps = []
    for i, x in enumerate(CANNON_X):
        muzzles.append(tuple(_cannon(mb, fl, (x, CANNON_Y, 0), M, i)))
        for sx in (-1.6, 1.6): rod(mb, (x + sx, CANNON_Y + 2.6, 0), (x + sx, CANNON_Y + 2.6, 1.3), 0.5, M['straw'], seg=10)
    r = _rnd(8)
    for k, x in enumerate((-13.0, 1.0, 15.0, 24.0)):
        rod(mb, (x, CANNON_Y - 1.0, 0), (x, CANNON_Y - 1.0, 8.0), 0.08, M['wood_d'])
        mb.oface([(x + 0.06, CANNON_Y - 1.0, 7.8), (x + 1.4, CANNON_Y - 1.0, 7.8), (x + 1.4, CANNON_Y - 1.0, 3.6), (x + 0.06, CANNON_Y - 1.0, 3.6)], M['banner_black'], [(0, 1), (1, 1), (1, 0), (0, 0)], (0, -1, 0))
    for k, (x, y) in enumerate(((-24.0, -46.0), (-14.0, -48.0), (-2.0, -46.5), (10.0, -48.5), (21.0, -46.0))):
        _tent(mb, cards, Frame((x, y, 0), 0.0), 4.2, 3.6, 2.9, M, M['canvas'], glow=M['tent_glow'])
    for (x, y) in ((-19.0, -38.0), (4.0, -39.5), (16.0, -38.5)):
        f = D._brazier(mb, fl, cards, (x, y, 0), M, s=1.3); lamps.append((f, 200.0))
    for i, x in enumerate(CANNON_X):                                          # fire pots for the linstocks beside each gun
        f = D._brazier(mb, fl, cards, (x - 1.7, CANNON_Y - 0.6, 0), M, s=0.55)
        if i % 2 == 0: lamps.append((f, 70.0))
    for k in range(30):                                                       # spear racks / soldiers' stakes as silhouettes
        x = r.uniform(-30, 30); y = r.uniform(-53, -49); rod(mb, (x, y, 0), (x + r.uniform(-0.2, 0.2), y, 3.2), 0.03, M['wood_d'], seg=4)
    o1 = _obj(mb, 'army', SET, hull=0.02); o2 = _obj(fl, 'army_glow', SET, shadow=False); o3 = _obj(cards, 'army_halos', SET, shadow=False)
    ls = [_flame_light('camp_fire_%d' % i, tuple(f), FIRE, e * P['lamps'], radius=0.4) for i, (f, e) in enumerate(lamps)]
    STATE['army'] = [o1, o2, o3] + ls; STATE['muzzles'] = muzzles
    STATE['marks'].update(gunners=[(x + 1.3, CANNON_Y - 1.6, 0.0) for x in CANNON_X], cannons=[(x, CANNON_Y, 0.0) for x in CANNON_X])

# ============================================================================= effects: balls, flashes, dust, smoke, rain
def _fx(SET, P, M):
    """Per impact slot: the flying ball, a flash light, a dust burst (camera-only billow balls); per cannon: muzzle flash + smoke
    puff; the collapse debris (chunks), rubble mound and dust cloud; smoke columns over the battlefield."""
    STATE['slots'] = {}
    for s in SEC:
        lst = []
        for i in range(3):
            d = STATE['decals'][s][i]
            bb = MB(); bb.sphere((0, 0, 0), 0.42, M['cannonball'], seg=12, rings=7); ball = _obj(bb, 'ball_%s_%d' % (s, i), SET)
            dm = _mat_dust('%sdust_%s_%d' % (STATE['pre'], s, i), P['dust_rgb'], 1.1); pb = MB(); r = _rnd(100 + i + (10 if s == 'lin' else 0))
            for k in range(7): lumpy(pb, (r.uniform(-1.0, 1.0), r.uniform(-1.2, -0.2), r.uniform(-0.6, 1.0)), r.uniform(0.6, 1.1), dm, 300 + k, seg=14, rings=9, rough=0.25)
            puff = _smooth(_obj(pb, 'impact_dust_%s_%d' % (s, i), SET, shadow=False)); puff.location = d['c']
            fls = MB(); fls.sphere((0, 0, 0), 0.6, M['flash'], seg=10, rings=6); fo = _obj(fls, 'impact_flash_%s_%d' % (s, i), SET, shadow=False); fo.location = d['c'] - Vector((0, 0.4, 0))
            L = BK._light('impact_%s_%d' % (s, i), tuple(d['c'] - Vector((0, 2.0, 0))), (1.0, 0.75, 0.45), 0.0, radius=0.5, shadow=False)
            lst.append(dict(ball=ball, dust=puff, dmat=dm, flash=fo, light=L, cannon=SLOT_CANNON[s][i]))
        STATE['slots'][s] = lst
    STATE['muzzle_fx'] = []
    for i, mz in enumerate(STATE['muzzles']):
        sm = _mat_dust('%smsmoke_%d' % (STATE['pre'], i), tuple(min(1.0, c * 1.5) for c in P['smoke_rgb']), 1.0); pb = MB(); r = _rnd(200 + i)
        for k in range(6): lumpy(pb, (r.uniform(-0.7, 0.7), r.uniform(0.2, 2.6), r.uniform(-0.3, 0.9)), r.uniform(0.6, 1.1), sm, 400 + k, seg=14, rings=9, rough=0.25)
        so = _smooth(_obj(pb, 'muzzle_smoke_%d' % i, SET, shadow=False)); so.location = mz
        fb = MB(); fb.sphere((0, 0.6, 0), 0.55, M['flash'], seg=10, rings=6); fo = _obj(fb, 'muzzle_flash_%d' % i, SET, shadow=False); fo.location = mz
        L = BK._light('muzzle_%d' % i, tuple(Vector(mz) + Vector((0, 1.0, 0.5))), (1.0, 0.7, 0.4), 0.0, radius=0.4, shadow=False)
        STATE['muzzle_fx'].append(dict(smoke=so, smat=sm, flash=fo, light=L))
    _collapse_parts(SET, P, M)
    # smoke columns over the battlefield (set_smoke): stacks of soft billow balls that rise and swell, recycled bottom to top
    sm = _mat_dust(STATE['pre'] + 'smoke_balls', P['smoke_rgb'], 1.0); r = _rnd(13); balls = []
    spots = [(x + 0.5, CANNON_Y + 1.5) for x in CANNON_X[::2]] + [(-19.0, -38.0), (4.0, -39.5), (16.0, -38.5), (-34.0, -14.0), (30.0, -12.0), (-6.0, -40.0), (24.0, -42.0)]
    for k, (x, y) in enumerate(spots):
        H = r.uniform(14, 22); n = 7
        for j in range(n):
            bb = MB(); lumpy(bb, (0, 0, 0), 1.0, sm, 700 + 10 * k + j, seg=14, rings=9, rough=0.28); o = _obj(bb, 'smoke_%02d_%d' % (k, j), SET, shadow=False); _smooth(o)
            balls.append(dict(ob=o, base=Vector((x, y, 0.0)), H=H, ph=(j + r.uniform(0, 0.4)) / n, size=r.uniform(1.6, 2.6), drift=Vector((r.uniform(2, 5), r.uniform(-1, 2), 0))))
    STATE['smoke'] = balls; STATE['smoke_mat'] = sm

def _collapse_parts(SET, P, M):
    """Debris chunks of the general's section (2-course bands, 2.2 D long, outer / inner half of the thickness), the rubble mound
    (rises out of the dust) and the dust cloud balls. Positions are precomputed; set_collapse moves them."""
    a, b = SEC['general']; r = _rnd(55); chunks = []
    for band in range((NMAX - KB + 1) // 2):
        z0 = PL + (KB + 2 * band) * CH; zc = z0 + CH
        for i in range(10):
            x = a + 0.1 + i * 2.19
            for half in (0, 1):
                y0, y1 = (0.0, 2.5) if half == 0 else (2.5, WT)
                cb = MB(); hx, hy, hz = 1.05 * r.uniform(0.85, 1.0), 1.2 * r.uniform(0.85, 1.0), 0.5 * r.uniform(0.85, 1.0)
                cb.box((-hx, -hy, -hz), (hx, hy, hz), M['brick_plain'], tile=(4, 4))
                o = _obj(cb, 'chunk_%02d_%d_%d' % (band, i, half), SET); s = Vector((x + 1.05, (y0 + y1) / 2, zc)); o.location = s; o.hide_render = True
                out = -1 if half == 0 else 1; dy = out * r.uniform(2.5, 9.0); ex = s.x + r.uniform(-1.5, 1.5); ey = (WT / 2) + dy + (0 if out < 0 else 0)
                ez = max(0.5, _pile_h(ey) * r.uniform(0.75, 1.05) + 0.4)
                chunks.append(dict(ob=o, s=s, e=Vector((ex, ey, ez)), band=band, spin=(r.uniform(-2.4, 2.4), r.uniform(-2.4, 2.4), r.uniform(-1.2, 1.2)), j=r.uniform(0, 0.06)))
    STATE['chunks'] = chunks
    # rubble mound along the section: lumpy brick-textured heaps
    rb = MB()
    for k in range(70):
        x = r.uniform(a + 0.5, b - 0.5); y = r.uniform(-8.0, WT + 8.0); h = _pile_h(y)
        if h < 0.4: continue
        lumpy(rb, (x, y, h * 0.35), r.uniform(1.4, 2.6), M['brick_plain'], 500 + k, seg=10, rings=6, rough=0.35, squash=max(0.3, h / 4.5))
    for k in range(60):
        x = r.uniform(a + 0.3, b - 0.3); y = r.uniform(-7.0, WT + 7.0); z = _pile_h(y) * 0.8
        rb.box((x - 0.33, y - 0.17, z), (x + 0.33, y + 0.17, z + 0.25), M['brick_plain'], tile=(4, 4))
    ro = _obj(rb, 'rubble', SET, hull=0.0); ro.hide_render = True; ro.scale = (1, 1, 0.02)
    STATE['rubble'] = ro
    # dust cloud: big billow balls rising from the base of the section
    dm = _mat_dust(STATE['pre'] + 'cdust', P['dust_rgb'], 1.05); dust = []
    for k in range(18):
        c = Vector((r.uniform(a + 1, b - 1), r.uniform(-6.0, WT + 6.0), r.uniform(0.5, 3.0)))
        db = MB(); lumpy(db, (0, 0, 0), 1.0, dm, 600 + k, seg=16, rings=10, rough=0.3)
        o = _smooth(_obj(db, 'collapse_dust_%02d' % k, SET, shadow=False)); o.location = c; o.hide_render = True
        dust.append(dict(ob=o, c=c, size=r.uniform(3.0, 5.5), t0=r.uniform(0.08, 0.35), rise=r.uniform(2.0, 7.0)))
    STATE['cdust'] = dust; STATE['cdust_mat'] = dm

def _pile_h(y): return 5.2 * math.exp(-((y - WT / 2) / 5.0) ** 2)

def _rain_comp(scene):
    """Rain streaks in the compositor (render cost 0): two screen layers (near: long soft streaks, far: dense fine ones) scrolled down
    with Translate (repeat) and added after the grade. set_rain keys their strength and scroll."""
    ng = scene.compositing_node_group; out = [n for n in ng.nodes if n.bl_idname == 'NodeGroupOutput'][0]
    last = out.inputs[0].links[0].from_socket; tx = STATE['tx']; layers = []
    for k, nm in enumerate(('rain_far', 'rain_near')):
        im = ng.nodes.new('CompositorNodeImage'); im.image = T._img(tx[nm])
        tr = ng.nodes.new('CompositorNodeTranslate'); tr.name = 'rain_tr_%d' % k
        for sk in ('Extension X', 'Extension Y'): tr.inputs[sk].default_value = 'Repeat'
        ng.links.new(im.outputs['Image'], tr.inputs['Image'])
        mx = ng.nodes.new('ShaderNodeMix'); mx.name = 'rain_mix_%d' % k; mx.data_type = 'RGBA'; mx.blend_type = 'ADD'; mx.inputs[0].default_value = 0.0
        ng.links.new(last, mx.inputs[6]); ng.links.new(tr.outputs['Image'], mx.inputs[7]); last = mx.outputs[2]
        layers.append((mx, tr, (9.0, 26.0)[k]))
    ng.links.new(last, out.inputs[0])
    STATE['rain'] = dict(ng=ng, layers=layers)

# ============================================================================= the macro area (inside the mortar joint)
MAC = dict(bed=(-1.2, 1.2), face_y=0.22, impact=(1.5, 0.0), xr=(-16.0, 34.0))

def _macro(SET, P, M, kind):
    """Macro of the bed joint between two bricks (1 D here ~ 2 mm): big porous fired-clay bricks (bevelled) above and below a recessed
    mortar joint whose face is packed with angular lime crystals. kind 'plain': grey grainy matrix; the impact sends a brittle crack
    racing through the joint and up / down into the bricks, shards and dust spray out. kind 'rice': creamy matrix with a fine glowing
    sticky web of starch strands wrapped round the crystals; the impact dents the face, the web stretches and glows brighter, flexes
    and holds. A head joint rises from the bed joint at x -3. Warm fire key from the front-left, deep blue shade, two flickering fire
    lamps and a cool rim."""
    r = _rnd(7 if kind == 'plain' else 7); z0, z1 = MAC['bed']; fy = MAC['face_y']; xa, xb = MAC['xr']
    bricks = MB()
    for (lo, hi) in (((xa, 0.0, -7.0), (6.0, 12.0, z0)), ((6.0 + 2.4, 0.0, -7.0), (xb, 12.0, z0)), ((xa, 0.0, z1), (-3.0 - 1.2, 12.0, 7.0)), ((-3.0 + 1.2, 0.0, z1), (xb, 12.0, 7.0)),
                     ((xa, 0.0, 9.4), (xb, 12.0, 16.0)), ((xa, 0.0, -16.0), (xb, 12.0, -9.4))):
        bricks.box(lo, hi, M['clay'], tile=(8, 8))
    bo = _obj(bricks, 'macro_bricks', SET)
    bv = bo.modifiers.new('bevel', 'BEVEL'); bv.width = 0.35; bv.segments = 3; bv.limit_method = 'ANGLE'
    # back fill of the upper/lower thin joints (plain mortar surfaces, recessed)
    jb = MB(); mat = M['matrix_' + kind]
    for (za, zb) in ((7.0, 9.4), (-9.4, -7.0)): jb.quad((xa, fy, za), (xb - xa, 0, 0), (0, 0, zb - za), mat, (xa / 4, za / 4, xb / 4, zb / 4))
    jb.quad((6.0, fy, -7.0), (2.4, 0, 0), (0, 0, 7.0 + z0), mat, (0, 0, 0.6, 1.5)); jb.quad((-4.2, fy, z1), (2.4, 0, 0), (0, 0, 7.0 - z1), mat, (0, 0, 0.6, 1.5))
    _obj(jb, 'macro_backjoints', SET)
    # the bed-joint face: a subdivided grid with a 'dent' shape key (pushed in round the impact)
    ix, iz = MAC['impact']; nx, nz = 150, 12; gb = MB(); xs = [xa + (xb - xa) * i / nx for i in range(nx + 1)]; zs = [z0 + (z1 - z0) * k / nz for k in range(nz + 1)]
    for i in range(nx):
        for k in range(nz):
            gb._in = True
            gb.face([(xs[i], fy, zs[k]), (xs[i + 1], fy, zs[k]), (xs[i + 1], fy, zs[k + 1]), (xs[i], fy, zs[k + 1])], mat, [(xs[i] / 4, zs[k] / 4), (xs[i + 1] / 4, zs[k] / 4), (xs[i + 1] / 4, zs[k + 1] / 4), (xs[i] / 4, zs[k + 1] / 4)])
    face = _obj(gb, 'macro_joint', SET)
    def dent(p, k=1.0, R=1.7): d2 = (p.x - ix) ** 2 + (p.z - iz) ** 2; return Vector((0, 0.55 * k * math.exp(-d2 / R ** 2), 0))
    _shape_key(face, 'dent', lambda p: dent(p))
    # crystals (calcite rhombs) partly embedded in the face, denser round the hero area; same layout for both kinds
    cb = MB(); crys = []
    for k in range(380):
        x = r.uniform(xa + 1, xb - 1) if k > 220 else r.uniform(-7.0, 12.0); z = r.uniform(z0 + 0.1, z1 - 0.1); s = r.uniform(0.035, 0.11) * (1.0 if k > 30 else 1.6)
        c = Vector((x, fy - s * r.uniform(0.05, 0.4), z)); X = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))).normalized()
        Y = X.cross(Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1)))).normalized(); Z = X.cross(Y)
        Y = (Y + X * 0.35).normalized()                                                  # sheared box = rhombohedron
        obox(cb, c, X, Y, Z, s, s * 0.8, s * 0.7, M['crystal']); crys.append(c)
    # the head joint (vertical) at x -3 above the bed joint: crystals too
    for k in range(60):
        x = r.uniform(-4.1, -1.9); z = r.uniform(z1 + 0.2, 6.8); s = r.uniform(0.035, 0.1); c = Vector((x, fy - s * 0.3, z))
        X = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))).normalized(); Y = X.cross(Vector((0.3, 0.2, 1))).normalized(); Z = X.cross(Y)
        obox(cb, c, X, Y, Z, s, s * 0.8, s * 0.7, M['crystal']); crys.append(c)
    cr = _obj(cb, 'macro_crystals', SET); cr['glossy_vis'] = 1
    _shape_key(cr, 'dent', lambda p: dent(p, 1.0))
    STATE['macro'] = dict(kind=kind, face=face, crystals=cr, impact=Vector((ix, fy, iz)))
    if kind == 'rice':
        # the sticky web: strands between neighbouring crystals (sagging, bowed out of the face) + loose loops; emission gold
        wb = MB(); nb = 0
        for i, a in enumerate(crys):
            near = sorted(((b - a).length, j) for j, b in enumerate(crys) if j != i and (b - a).length < 0.75)[:5]
            for dlen, j in near:
                if j < i and r.random() < 0.5: continue
                b = crys[j]; n = 5; rr = r.uniform(0.006, 0.013); bow = r.uniform(0.04, 0.16)
                pts = [a.lerp(b, t) + Vector((0, -bow * 4 * t * (1 - t), -0.06 * 4 * t * (1 - t))) for t in [q / n for q in range(n + 1)]]
                for p0, p1 in zip(pts, pts[1:]): wb.frustum(p0, p1, rr, rr, M['web'], seg=4, cap0=False, cap1=False)
                nb += 1
        for k in range(120):                                                            # fine loops wrapping single crystals
            a = crys[r.randrange(len(crys))]
            if a.x < -1.5: continue
            R = r.uniform(0.1, 0.22); n = 8; ph = r.uniform(0, 6.28); tilt = r.uniform(-0.5, 0.5)
            pts = [a + Vector((R * math.cos(ph + 2 * math.pi * q / n), -0.05 - 0.05 * math.sin(ph + q), R * math.sin(ph + 2 * math.pi * q / n) * 0.7 + tilt * 0.1)) for q in range(n + 1)]
            for p0, p1 in zip(pts, pts[1:]): wb.frustum(p0, p1, 0.005, 0.005, M['web'], seg=4, cap0=False, cap1=False)
        wo = _obj(wb, 'macro_web', SET, shadow=False)
        _shape_key(wo, 'dent', lambda p: dent(p, 0.9, 1.8))
        _shape_key(wo, 'flex', lambda p: Vector((0.0, -0.22 * math.exp(-((p.x - ix) ** 2 + (p.z - iz) ** 2) / 4.0), 0.0)) + (Vector((p.x - ix, 0, p.z - iz)) * 0.06 * math.exp(-((p.x - ix) ** 2 + (p.z - iz) ** 2) / 6.0)))
        STATE['macro'].update(web=wo, strands=nb)
    else:
        # crack ribbons: from the impact along the joint (both ways), branching up / down through the bricks; reveal order in UV.x
        core = _mat_crack_ribbon(STATE['pre'] + 'crack_core', (0.0, 0.0, 0.0), 1.0); lip = _mat_crack_ribbon(STATE['pre'] + 'crack_lip', (0.85, 0.78, 0.7), 0.18)
        kb = MB()
        def surf_y(z): return fy - 0.03 if z0 < z < z1 else -0.025
        def ribbon(pts, o0, o1, w0, w1):
            n = len(pts) - 1
            for i in range(n):
                t0, t1 = i / n, (i + 1) / n; p0, p1 = pts[i], pts[i + 1]; d = (p1 - p0); nrm = Vector((-d.z, 0, d.x)).normalized()
                for (mat, wk, dy) in ((lip, 1.7, 0.002), (core, 1.0, 0.012)):
                    wa, wb_ = (w0 + (w1 - w0) * t0) * wk, (w0 + (w1 - w0) * t1) * wk
                    q = [p0 - nrm * wa, p1 - nrm * wb_, p1 + nrm * wb_, p0 + nrm * wa]
                    q = [Vector((v.x, surf_y(v.z) - dy, v.z)) for v in q]
                    kb.face(q, mat, [(o0 + (o1 - o0) * t0, 0), (o0 + (o1 - o0) * t1, 0), (o0 + (o1 - o0) * t1, 1), (o0 + (o1 - o0) * t0, 1)])
        def walk(x, z, ang, length, step=0.18, wig=0.4, zlim=None):
            pts = [Vector((x, 0, z))]; L_ = 0.0
            while L_ < length:
                ang += r.gauss(0, wig); x += step * math.cos(ang); z += step * math.sin(ang)
                if zlim: z = max(zlim[0], min(zlim[1], z))
                pts.append(Vector((x, 0, z))); L_ += step
            return pts
        for dirn in (0.0, math.pi):                                                   # along the joint, end to end
            for k in range(2):
                pts = walk(ix, iz + (k - 0.5) * 0.4, dirn, 26.0, 0.22, 0.25, zlim=(z0 + 0.15, z1 - 0.15)); ribbon(pts, 0.02 + 0.03 * k, 0.75, 0.11, 0.05)
        for k in range(10):                                                           # the star at the impact
            a = 2 * math.pi * k / 10 + r.uniform(-0.2, 0.2); ribbon(walk(ix, iz, a, r.uniform(1.0, 2.2), 0.12, 0.3), 0.0, 0.25, 0.09, 0.02)
        for k in range(9):                                                            # into the bricks, up and down
            x = ix + r.uniform(-9, 14); up = 1 if k % 2 else -1; o0 = 0.25 + 0.4 * abs(x - ix) / 14
            ribbon(walk(x, up * (z1 - 0.1), up * math.pi / 2 + r.uniform(-0.4, 0.4), r.uniform(3.0, 7.0), 0.22, 0.35), o0, min(1.0, o0 + 0.4), 0.08, 0.025)
        ko = _obj(kb, 'macro_cracks', SET, shadow=False)
        # shards that spall off and fly toward the camera, dust spray
        sb = []; dm = _mat_dust(STATE['pre'] + 'mdustp', (0.85, 0.8, 0.72), 1.1)
        for k in range(36):
            s = r.uniform(0.06, 0.2); c = Vector((ix + r.uniform(-1.2, 1.2), fy - 0.1, iz + r.uniform(-0.9, 0.9)))
            b_ = MB(); X = Vector((r.uniform(-1, 1), r.uniform(-1, 1), r.uniform(-1, 1))).normalized(); Y = X.cross(Vector((0, 0, 1))).normalized(); Z = X.cross(Y)
            obox(b_, (0, 0, 0), X, Y, Z, s, s * 0.6, s * 0.4, M['matrix_plain'] if k % 3 else M['crystal'])
            o = _obj(b_, 'shard_%02d' % k, SET, shadow=False); o.location = c; o.hide_render = True
            v = Vector((r.uniform(-3, 3), r.uniform(-7, -3), r.uniform(-1, 3)))
            sb.append(dict(ob=o, c=c, v=v, spin=(r.uniform(-8, 8), r.uniform(-8, 8), r.uniform(-8, 8))))
        pb = MB()
        for k in range(8): lumpy(pb, (r.uniform(-1.4, 1.4), r.uniform(-2.0, -0.2), r.uniform(-0.8, 0.8)), r.uniform(0.5, 1.0), dm, 900 + k, seg=14, rings=9, rough=0.25)
        po = _smooth(_obj(pb, 'macro_dust', SET, shadow=False)); po.location = Vector((ix, fy, iz)); po.hide_render = True
        STATE['macro'].update(cracks=ko, mats=[core, lip], shards=sb, dust=po, dust_mat=dm)
    # the cannonball
    bb = MB(); bb.sphere((0, 0, 0), 1.3, M['cannonball'], seg=24, rings=14); ball = _smooth(_obj(bb, 'macro_ball', SET)); ball.hide_render = True
    STATE['macro']['ball'] = ball
    # light: two flickering fire lamps front-left, a cool rim from above-right, a warm bounce under the joint
    _flame_light('macro_fire_0', (-4.5, -4.5, -2.6), FIRE, 650.0, radius=1.0, shadow=True)
    _flame_light('macro_fire_1', (4.0, -3.5, -3.6), FIRE, 300.0, radius=0.8, shadow=False)
    BK._light('macro_rim', (12.0, -5.0, 9.0), (0.45, 0.65, 1.0), 2600.0, radius=2.0, shadow=False)
    BK._light('macro_cool', (-2.0, -6.0, 6.5), (0.4, 0.6, 1.0), 800.0, radius=2.0, shadow=False)
    BK._light('macro_impact', (ix, fy - 2.0, iz), (1.0, 0.8, 0.5), 0.0, radius=0.4, shadow=False); STATE['macro']['light'] = bpy.data.objects['L_macro_impact']
    # a dark warm void behind the camera side and a far glow: the macro sits in a lit cavity
    vb = MB(); vm = mat_emit(STATE['pre'] + 'e_void', '#1a0e10', strength=1.0)
    vb.box((xa - 30, -40, -30), (xb + 30, 14, 30), vm); _obj(vb, 'macro_void', SET, shadow=False)
    STATE['marks'].update(macro_impact=(ix, fy, iz))

def _smooth(o):
    for p in o.data.polygons: p.use_smooth = True
    return o

def _shape_key(ob, name, fn):
    if ob.data.shape_keys is None: ob.shape_key_add(name='Basis', from_mix=False)
    sk = ob.shape_key_add(name=name, from_mix=False)
    for v in ob.data.vertices: sk.data[v.index].co = v.co + fn(v.co)
    sk.value = 0.0
    return sk

# ============================================================================= hooks
def _ss(a, b, x): t = max(0.0, min(1.0, (x - a) / (b - a))); return t * t * (3 - 2 * t)
def _keyp(ob, path, frame, interp='LINEAR'):
    if frame is not None: T._key(ob, path, frame, interp)

def set_wall_height(section, courses, frame=None):
    """Courses (0.5 D each, 0..26) of a section ('lin' rice mortar | 'general' plain mortar): courses above are hidden, the top
    dressing (rubble bed, half-laid course, mortar tub, trowel) sits on the top, the crack overlay is clipped there. Keys constant."""
    if section == 'both':
        for s in SEC: set_wall_height(s, courses, frame)
        return
    if 'courses' not in STATE: return
    n = max(0, min(NMAX, int(round(courses)))); STATE['heights'][section] = n
    for k, o in enumerate(STATE['courses'][section]): T._show([o], k < n, frame)
    td = STATE['topdress'][section]; td.location.z = PL + n * CH; _keyp(td, 'location', frame, 'CONSTANT'); T._show([td], n > 0, frame)
    _keyval(STATE['crack_mats'][section], 'top_z', PL + n * CH, frame, 'CONSTANT')

def set_cauldron_steam(level, frame=None, speed=1.0):
    """Steam from the rice soup: soft white billows rising, swelling and drifting from the soup; 0 none .. 1 full .. 1.5 thick.
    Call every frame (keys linear)."""
    if 'steam_mat' not in STATE: return
    _billows(STATE['steam'], STATE['steam_mat'], 0.55 * max(0.0, float(level)), level > 0.001, frame, 0.007 * speed)

def _billows(balls, mat, op, vis, frame, rate):
    f = frame if frame is not None else bpy.context.scene.frame_current
    _keyval(mat, 'op', min(1.0, op), frame)
    for b in balls:
        ph = (b['ph'] + rate * f) % 1.0; o = b['ob']
        o.location = b['base'] + Vector((0, 0, b['H'] * ph)) + b['drift'] * ph; s = max(0.001, b['size'] * (0.35 + 1.4 * ph) * math.sin(math.pi * min(1.0, ph * 1.15)) ** 0.5)
        o.scale = (s, s, s * 0.85); _keyp(o, 'location', frame); _keyp(o, 'scale', frame); T._show([o], vis, frame)

def set_smoke(level, frame=None, speed=1.0):
    """Smoke columns over the battlefield (cannon line, camp fires, burning spots): soft billow balls rising and swelling from each
    fire, drifting with the wind, recycled bottom to top while tiny. 0 none .. 1 normal .. 1.5 thick. Call every frame (keys linear)."""
    if 'smoke_mat' not in STATE: return
    _billows(STATE['smoke'], STATE['smoke_mat'], 0.75 * max(0.0, float(level)), level > 0.001, frame, 0.004 * speed)

def set_rain(level, frame=None, speed=1.0):
    """Rain streaks (compositor overlay, no render cost): 0 none .. 1 steady .. 1.5 downpour; the streaks fall with the frame number
    (call every frame; keys linear). The wet sheen, darker wet brick and sky-mirror puddles come with the RAIN light preset."""
    R_ = STATE.get('rain')
    if not R_: return
    f = frame if frame is not None else bpy.context.scene.frame_current; lv = max(0.0, float(level))
    for k, (mx, tr, spd) in enumerate(R_['layers']):
        mx.inputs[0].default_value = (0.32 if k == 0 else 0.42) * lv; tr.inputs['Y'].default_value = -(spd * speed * f) % 1280.0; tr.inputs['X'].default_value = (spd * 0.07 * speed * f) % 720.0
        if frame is not None:
            mx.inputs[0].keyframe_insert('default_value', frame=frame); tr.inputs['Y'].keyframe_insert('default_value', frame=frame); tr.inputs['X'].keyframe_insert('default_value', frame=frame)
    if frame is not None:
        for fc in T._fcurves(R_['ng']):
            for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials, the rain overlay), so plain set_* calls hold again."""
    D.clear_keys()
    ng = bpy.context.scene.compositing_node_group
    if ng is not None and ng.animation_data: ng.animation_data_clear()

def set_mortar_wet(k, frame=None):
    """Lin's rice mortar soft and wet in the rain (the false payoff): 0 dry cream .. 1 dark, glossy, milky runs hanging from every
    bed joint (also the trough paste). Keys linear."""
    m = STATE.get('M', {}).get('brick_rice')
    if m is None: return
    _keyval(m, 'wet', max(0.0, min(1.5, float(k))), frame)

def set_cracks(section, level, frame=None):
    """Crack overlay of a section, both faces. general (plain mortar): 0 none .. 0.33 shot 1: a star round impact 0 .. 0.66 shot 2:
    long cracks along the courses across the whole row .. 1 shot 3: the whole slab broken up. lin (rice): only short hairlines
    round the dents (0..1). Keys linear (cracks grow outward from the impacts)."""
    if 'crack_mats' not in STATE: return
    _keyval(STATE['crack_mats'][section], 'lvl', max(0.0, min(1.0, float(level))) + (0.004 if level > 0 else 0.0), frame)

def set_army(on, frame=None):
    """The enemy cannons, gunners' kit, banners, camp and camp fires (BATTLE presets show them)."""
    if 'army' not in STATE: return
    T._show(STATE['army'], bool(on), frame); STATE['army_on'] = bool(on)

def set_impact(section, slot, t, frame=None):
    """One cannon shot at impact slot 0..2 of a section (IMPACTS): t 0 nothing; 0..0.06 muzzle flash + smoke puff at its cannon (the
    smoke drifts and thins to t 1); 0.06..0.35 the ball flies (arc) to the wall; 0.35 hit: flash + light burst on the wall, a dust
    burst grows and fades (to 1); the decal (general: deep crater; lin: a shallow dent, the face whole) appears and stays, the ball
    stays embedded. Call every frame of the shot (keys linear / constant)."""
    if 'slots' not in STATE: return
    t = max(0.0, min(1.0, float(t))); S = STATE['slots'][section][slot]; Dd = STATE['decals'][section][slot]; c = Dd['c']
    mz = Vector(STATE['muzzles'][S['cannon']]); MF = STATE['muzzle_fx'][S['cannon']]
    # muzzle
    fk = math.exp(-((t - 0.02) / 0.03) ** 2) if t > 0 else 0.0
    MF['flash'].scale = (0.3 + 1.5 * fk,) * 3; _keyp(MF['flash'], 'scale', frame); T._show([MF['flash']], fk > 0.05, frame)
    MF['light'].data.energy = 3000.0 * fk; _keyp(MF['light'].data, 'energy', frame)
    st = _ss(0.0, 0.6, t); so = MF['smoke']; so.scale = (0.4 + 1.8 * st,) * 3; so.location = mz + Vector((0.8 * st, 1.0 * st, 1.6 * st)); _keyp(so, 'scale', frame); _keyp(so, 'location', frame)
    _keyval(MF['smat'], 'op', (1.0 - 0.75 * _ss(0.3, 1.0, t)) if t > 0 else 0.0, frame); T._show([so], t > 0.0 and t < 0.999, frame)
    # flight
    fly = 0.06 < t < 0.35; u = _ss(0.06, 0.35, t) if fly else 0.0; u = (t - 0.06) / 0.29 if fly else 0.0
    p = mz.lerp(c, u) + Vector((0, 0, 3.0 * 4 * u * (1 - u))); S['ball'].location = p; _keyp(S['ball'], 'location', frame); T._show([S['ball']], fly, frame)
    hit = t >= 0.35; T._show([Dd['ball_in']], hit, frame); _keyval(Dd['mat'], 'vis', 1.0 if hit else 0.0, frame, 'CONSTANT')
    hk = math.exp(-((t - 0.37) / 0.05) ** 2) if t >= 0.33 else 0.0
    S['flash'].scale = (0.2 + 2.2 * hk,) * 3; _keyp(S['flash'], 'scale', frame); T._show([S['flash']], hk > 0.05, frame)
    S['light'].data.energy = 2500.0 * hk; _keyp(S['light'].data, 'energy', frame)
    dt = _ss(0.35, 0.8, t); S['dust'].scale = (0.3 + 1.8 * dt,) * 3; S['dust'].location = c + Vector((0, -0.6 - 1.2 * dt, 0.6 * dt)); _keyp(S['dust'], 'scale', frame); _keyp(S['dust'], 'location', frame)
    _keyval(S['dmat'], 'op', (1.0 - _ss(0.55, 1.0, t)) if hit else 0.0, frame); T._show([S['dust']], hit and t < 0.999, frame)
    for o in (S['flash'], MF['flash']):
        for mm in o.data.materials: mm.node_tree.nodes['strength'].inputs['Strength'].default_value = 14.0

def _impact_reset():
    for s in STATE.get('slots', {}):
        for i in range(3): set_impact(s, i, 0.0)

def set_collapse(t, frame=None):
    """The general's section collapses (shot 3): t 0 standing; 0.05..0.4 the courses above course KB break into chunks band by band
    (bottom bands a little later), which tumble outward to both sides with spin and land on the rubble mound (0.3..0.8); the mound
    rises out of the dust (0.35..0.85); a big dust cloud billows up from the base (0.08..1) and hangs. Crack overlay and dents of
    the section hide when it breaks. Call every frame (keys linear / constant)."""
    if 'chunks' not in STATE: return
    t = max(0.0, min(1.0, float(t))); STATE['collapse'] = t; n = STATE['heights'].get('general', 0); nb = max(0, (n - KB + 1) // 2)
    starts = {}
    for c in STATE['chunks']:
        if c['band'] >= nb: T._show([c['ob']], False, frame); continue
        zrel = c['band'] / max(1, nb - 1); t0 = 0.05 + 0.12 * (1 - zrel) + c['j']; starts[c['band']] = min(starts.get(c['band'], 9), t0)
        tau = max(0.0, min(1.0, (t - t0) / 0.38)); vis = t >= t0
        p = c['s'].lerp(c['e'], tau); p.z = c['s'].z + (c['e'].z - c['s'].z) * tau * tau + 1.2 * math.sin(math.pi * tau) * (1 - tau)
        c['ob'].location = p; c['ob'].rotation_euler = tuple(x * tau for x in c['spin']); _keyp(c['ob'], 'location', frame); _keyp(c['ob'], 'rotation_euler', frame)
        T._show([c['ob']], vis, frame)
    for k, o in enumerate(STATE['courses']['general']):
        band = (k - KB) // 2 if k >= KB else -1
        gone = band >= 0 and band < nb and t >= starts.get(band, 9)
        T._show([o], k < n and not gone, frame)
    broke = t >= 0.05
    T._show([STATE['topdress']['general']], n > 0 and not broke, frame)
    T._show([STATE['crack_objs']['general']], not broke, frame)
    for d in STATE['decals']['general']:
        T._show([d['decal']], not broke, frame)
        if broke: T._show([d['ball_in']], False, frame)
    g = _ss(0.35, 0.85, t); ro = STATE['rubble']; ro.scale = (1.0, 1.0, max(0.02, g)); _keyp(ro, 'scale', frame); T._show([ro], t >= 0.35, frame)
    for d in STATE['cdust']:
        u = max(0.0, min(1.0, (t - d['t0']) / 0.45)); s = max(0.001, d['size'] * (0.25 + 0.75 * u))
        d['ob'].scale = (s, s, s * 0.85); d['ob'].location = d['c'] + Vector((0, 0, d['rise'] * u)); _keyp(d['ob'], 'scale', frame); _keyp(d['ob'], 'location', frame)
        T._show([d['ob']], t > d['t0'], frame)
    _keyval(STATE['cdust_mat'], 'op', 0.9 * (1.0 - 0.35 * _ss(0.7, 1.0, t)), frame)

def set_macro(t, frame=None):
    """mortar_macro / mortar_macro_rice: the cannonball hit seen inside the joint. t 0 calm .. 0.3 the ball flies in from the front-
    left and strikes the joint face .. 1 after.  plain: a brittle crack shoots from the impact along the whole joint and up / down
    into the bricks (0.3..0.75), the cracks gape, shards spall toward the camera and a dust puff blows out; the ball stays wedged.
    rice: the face dents in (0.3..0.4) and the glowing web stretches and flares (2.4x), flexes back in a damped spring and holds,
    glowing a little brighter (0.4..1); the ball bounces back out and drops away. Call every frame (keys linear)."""
    Mc = STATE.get('macro')
    if not Mc: return
    t = max(0.0, min(1.0, float(t))); imp = Mc['impact']; ball = Mc['ball']; R = 1.3
    hitp = imp + Vector((-0.6, -R + 0.25, 0.25))
    start = imp + Vector((-9.0, -12.0, 3.5))
    if t < 0.3: u = t / 0.3; p = start.lerp(hitp, u * u * 0.3 + u * 0.7)
    elif Mc['kind'] == 'rice':
        u = _ss(0.36, 0.95, t); back = hitp + Vector((-3.0, -6.0, 0.0)); p = hitp.lerp(back, u) + Vector((0, 0, -9.0 * u * u))
    else:
        u = _ss(0.4, 0.9, t); p = hitp + Vector((0, 0.15 * _ss(0.3, 0.36, t), 0)) + Vector((-1.0, -2.5, 0)) * u + Vector((0, 0, -10.0 * u * u))
    ball.location = p; ball.rotation_euler = (t * 6.0, t * 3.0, 0.0); _keyp(ball, 'location', frame); _keyp(ball, 'rotation_euler', frame)
    T._show([ball], 0.02 < t < 0.97, frame)
    hk = math.exp(-((t - 0.32) / 0.04) ** 2) if t > 0.25 else 0.0
    Mc['light'].data.energy = 1800.0 * hk; _keyp(Mc['light'].data, 'energy', frame)
    if Mc['kind'] == 'rice':
        if t < 0.3: d = 0.0; fx = 0.0
        else:
            s = t - 0.3; d = min(1.0, s / 0.06) * (0.75 + 0.25 * math.exp(-s * 6) * math.cos(s * 40)); fx = math.exp(-s * 5.0) * math.sin(min(1.0, s / 0.05) * math.pi / 2 + s * 32) * 1.0 + 0.3 * min(1.0, s / 0.06)
        for o in (Mc['face'], Mc['crystals'], Mc['web']):
            kb = o.data.shape_keys.key_blocks['dent']; kb.value = d * 0.8
            if frame is not None: kb.keyframe_insert('value', frame=frame)
        kf = Mc['web'].data.shape_keys.key_blocks['flex']; kf.value = fx
        if frame is not None: kf.keyframe_insert('value', frame=frame)
        web = STATE['M']['web']; g = 1.8 * (1.0 + 1.4 * math.exp(-((t - 0.36) / 0.1) ** 2) + 0.25 * _ss(0.3, 0.6, t))
        sk = web.node_tree.nodes['strength'].inputs['Strength']; sk.default_value = g
        if frame is not None: sk.keyframe_insert('default_value', frame=frame)
    else:
        lv = 0.0 if t < 0.3 else min(1.0, (t - 0.3) / 0.45) ** 0.8
        for m in Mc['mats']: _keyval(m, 'lvl', lv, frame)
        d = _ss(0.3, 0.36, t) * 0.55
        for o in (Mc['face'], Mc['crystals']):
            kb = o.data.shape_keys.key_blocks['dent']; kb.value = d
            if frame is not None: kb.keyframe_insert('value', frame=frame)
        for s in Mc['shards']:
            u = max(0.0, t - 0.31); vis = 0.31 < t
            s['ob'].location = s['c'] + s['v'] * u + Vector((0, 0, -9.0 * u * u)); s['ob'].rotation_euler = tuple(x * u for x in s['spin'])
            _keyp(s['ob'], 'location', frame); _keyp(s['ob'], 'rotation_euler', frame); T._show([s['ob']], vis, frame)
        dt = _ss(0.3, 0.6, t); Mc['dust'].scale = (0.3 + 1.1 * dt,) * 3; Mc['dust'].location = imp + Vector((0, -0.8 - 1.5 * dt, 0.3 * dt)); _keyp(Mc['dust'], 'scale', frame); _keyp(Mc['dust'], 'location', frame)
        _keyval(Mc['dust_mat'], 'op', 0.8 * (1.0 - _ss(0.42, 0.7, t)), frame); T._show([Mc['dust']], 0.3 < t < 0.7, frame)
    STATE['macro_t'] = t

def apply_preset_state(preset):
    PR = PRESETS[preset]
    if PR['area'] == 'site':
        hl, hg = PR.get('heights', (18, 21)); set_wall_height('lin', hl); set_wall_height('general', hg)
        set_cracks('lin', 0.0); set_cracks('general', 0.0); _impact_reset(); set_collapse(0.0)
        set_cauldron_steam(PR.get('steam', 1.0) if STATE['light'] != 'BATTLE' else 0.4)
        battle = STATE['light'] == 'BATTLE'
        set_army(PR.get('army', False) or battle); set_smoke(PR.get('smoke', 1.0 if battle else 0.0) if battle or PR.get('smoke') else 0.0)
        set_mortar_wet(0.8 if STATE['light'] == 'RAIN' else 0.0)
        set_rain(1.0 if STATE['light'] == 'RAIN' else 0.0)
    else:
        set_macro(0.0)
    set_flames(1.0)

# ============================================================================= cameras, anchors, staging
CAMS = dict(
    site=dict(site_wide=dict(loc=(-21.0, 36.0, 17.0), look_at=(4.0, 3.0, 6.6), lens=20),
              cauldron=dict(loc=(-6.2, 23.0, 7.6), look_at=(-11.4, 11.0, 3.4), lens=22),
              two_sections=dict(loc=(0.4, 25.0, 7.6), look_at=(0.0, 5.0, 6.7), lens=20),
              two_sections_out=dict(loc=(2.0, -19.0, 3.0), look_at=(2.0, 0.0, 9.0), lens=20),
              wall_top=dict(loc=(17.5, 2.7, 18.0), look_at=(3.0, 2.2, 13.6), lens=20),
              cannon_line=dict(loc=(-23.0, -28.5, 3.4), look_at=(5.0, -13.0, 5.4), lens=20)),
    macro=dict(macro_plain=dict(loc=(-4.6, -4.4, 0.9), look_at=(2.6, 0.2, -0.15), lens=22),
               macro_rice=dict(loc=(-4.6, -4.4, 0.9), look_at=(2.6, 0.2, -0.15), lens=22),
               macro_front=dict(loc=(1.0, -9.5, 0.4), look_at=(1.2, 0.2, 0.0), lens=22)),
)
CAM_NOTES = dict(
    site_wide='high crane from inside the city: tents and lantern path in front, the cauldron, both sections with scaffolds and banners, the gate tower right, over the wall the river plain, mountains, a pagoda',
    cauldron='medium on the giant cauldron from the camp side: the glowing stove mouth, the steaming soup, the paddle; Lin on his platform behind it, the wall (his rice section) behind',
    two_sections='front view of both sections from the site: Lin\'s creamy-mortar section (left) and the general\'s grey taller section (right) meeting at x 0, troughs, banners, scaffolds at the far ends',
    two_sections_out='the outer faces from the field (between the cannons and the wall): impacts, dents, cracks and the collapse read here',
    wall_top='on top of the general\'s section: the general stands on its top, Lin\'s lower section beyond / below, the site and the field to either side',
    cannon_line='behind the enemy cannon line on the field: six bronze cannons in a row toward both sections, gunners, black banners, smoke, the gate tower right',
    macro_plain='inside the plain-mortar bed joint, along it: crystals in grey matrix between two huge bricks; set_macro: the brittle crack races through',
    macro_rice='inside the rice-mortar bed joint: crystals wrapped in the glowing sticky web; set_macro: the face dents, the web flexes and holds',
    macro_front='square-on to the joint face at the impact point (either kind)',
)
HEIGHT = dict(lin=3.0, general=3.3, worker=2.9, gunner=2.9)
T.PH.update(
    lin=('beach_man', dict(yaw=0.25, expr='determined', arm_l='down', arm_r='down', legs='stand'), HEIGHT['lin']),
    general=('boss', dict(yaw=0.3, head_roll=-4, expr='smug', arm_l='hip', arm_r='hip', legs='stand'), HEIGHT['general']),
    worker=('senior_a', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['worker']),
    gunner=('senior_b', dict(yaw=-0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['gunner']))
placeholder_actor = T.placeholder_actor

STAGING = dict(
    site_wide=[('lin', 'lin_stir'), ('worker', (-2.6, 10.8, 0.0)), ('general', (6.4, 14.8, 0.0))],
    cauldron=[('lin', 'lin_stir'), ('general', (-7.4, 10.6, 0.0))],
    two_sections=[('lin', (-2.8, 10.0, 0.0)), ('general', (4.6, 10.4, 0.0)), ('worker', (10.6, 9.4, 0.0))],
    two_sections_out=[],
    wall_top=[('general', 'general_top')],
    cannon_line=[('gunner', (-1.2, CANNON_Y - 1.6, 0.0)), ('gunner', (5.8, CANNON_Y - 1.6, 0.0))],
    macro_plain=[], macro_rice=[], macro_front=[],
)

def _staging(cam_name):
    out = []
    for role, mk in STAGING.get(cam_name, []):
        if mk == 'general_top': mk = (8.0, 2.4, top_z('general'))
        elif isinstance(mk, str): mk = STATE['marks'][mk]
        out.append((role, tuple(mk)))
    return out

def anchors():
    P = STATE['P']; area = STATE['area']; cams = {k: dict(v) for k, v in CAMS[area].items()}
    A = dict(location=STATE['loc'], preset=STATE['preset'], area=area, light=STATE['light'], cams=cams, cam=dict(CAMS[area][PRESETS[STATE['preset']]['cam']]),
             cam_name=PRESETS[STATE['preset']]['cam'], cam_notes={k: CAM_NOTES.get(k, '') for k in cams},
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()),
             sun_elevation_deg=P['sun_elev'], floor_z=0.0, heights=dict(HEIGHT), marks=dict(STATE.get('marks', {})),
             lights=[o.name for o in STATE['LIGHTS'].objects], staging={k: _staging(k) for k in cams})
    if area == 'site':
        A.update(wall=dict(course=CH, plinth_top=PL, max_courses=NMAX, thickness=WT, outer_y=0.0, inner_y=WT, sections=dict(SEC), kind=dict(KIND),
                           courses=dict(STATE['heights']), top_z={s: top_z(s) for s in SEC}, impacts={s: [tuple(round(v, 3) for v in d['c']) for d in STATE['decals'][s]] for s in SEC},
                           collapse_break_z=PL + KB * CH),
                 gate=dict(GATE), cannons=dict(x=CANNON_X, y=CANNON_Y, muzzles=STATE.get('muzzles')), cauldron=STATE.get('cauldron'),
                 slide_out=[(8.0, 2.4, top_z('general')), (8.0, -1.5, 4.6), (8.0, -5.0, 2.0), (8.0, -8.5, 0.2)],
                 slide_in=[(8.0, 2.6, top_z('general')), (8.0, 6.5, 4.6), (8.0, 9.5, 2.0), (8.0, 12.0, 0.2)],
                 keep_out='wall y -0.4..5.4 (stand on its top at z = top_z); scaffolds x -21..-11 and 11.5..21.5, y 5.4..7.3; cauldron r 3.2 round (-11, 13.5) (Lin on the platform y 8.9..10.4, z 1.0); troughs (-5.2, 9.6) / (8.2, 9.8) 3.4 x 1.8; lime pits (-18, 10.5) / (17.2, 11.5); banner poles y 9; ramp x 3.5..11.3 y 7.4..8.6; cannons x +-1.2 round CANNON_X, y -25..-20')
    else:
        A.update(macro=dict(kind=STATE['macro']['kind'], impact=tuple(STATE['macro']['impact']), bed_joint_z=MAC['bed'], face_y=MAC['face_y'], strands=STATE['macro'].get('strands')))
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
        out.append((role, tuple(round(v, 2) for v in mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def apply_spec_state(state):
    """CLI state strings (comma separated): h<lin>/<gen> heights, wet<k>, crack<g>, crackl<l>, imp<sec><slot>@<t>, col<t>, smoke<k>,
    rain<k>, steam<k>, macro<t>, army0/1."""
    for tok in [s for s in (state or '').split(',') if s]:
        if tok.startswith('h') and '/' in tok: a, b = tok[1:].split('/'); set_wall_height('lin', int(a)); set_wall_height('general', int(b))
        elif tok.startswith('wet'): set_mortar_wet(float(tok[3:]))
        elif tok.startswith('crackl'): set_cracks('lin', float(tok[6:]))
        elif tok.startswith('crack'): set_cracks('general', float(tok[5:]))
        elif tok.startswith('imp'):
            sec = 'general' if tok[3] == 'g' else 'lin'; sl, tt = tok[4:].split('@'); set_impact(sec, int(sl), float(tt))
        elif tok.startswith('col'): set_collapse(float(tok[3:]))
        elif tok.startswith('smoke'): set_smoke(float(tok[5:]))
        elif tok.startswith('rain'): set_rain(float(tok[4:]))
        elif tok.startswith('steam'): set_cauldron_steam(float(tok[5:]))
        elif tok.startswith('macro'): set_macro(float(tok[5:]))
        elif tok.startswith('army'): set_army(tok[4:] == '1')

def cli_render(specs=None, quality='final', outdir=None, actors=True, cam_override=None):
    """specs: ['preset' | 'preset:LIGHT' | 'preset:LIGHT:state' (see apply_spec_state) | 'preset:LIGHT:state:cam']"""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        parts = spec.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None; st = parts[2] if len(parts) > 2 else ''
        A = build('wall_site', pr, light=lt); sc = bpy.context.scene; setup_render(sc, quality)
        nm = parts[3] if len(parts) > 3 and parts[3] else A['cam_name']; cs = A['cams'][nm]; make_camera(cs)
        apply_spec_state(st)
        if actors: stage_placeholders(A, nm, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(nm)
        tag = '%s_%s' % (pr if nm == A['cam_name'] else nm, A['light']) + ('_' + st.replace(',', '_').replace('/', '-').replace('@', 'at') if st else '')
        w, c = render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(c, 1), hp)
        print('%s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'):
        cli_render(arg or None, 'final' if cmd == 'final' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
    elif cmd == 'digest':
        A = build('wall_site', arg[0] if arg else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)
