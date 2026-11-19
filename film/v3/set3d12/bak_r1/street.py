#!/usr/bin/env python3
"""street.py : the FULL set of film 12 (Jonas Hanway and the first umbrella, London early 1750s): a Georgian London street in the rain as a real 3D
Blender set (bpy 5.x, Cycles CPU). One hard warm key, blue-violet shade, warm practicals, wide 22 mm cameras, no depth of field, no text anywhere.
Read API.md first (presets, lights, states, stand points, cameras, CLI, cost). Quick use:

    import street as S
    A = S.shot('street_wide', light='RAIN')           # builds the set, the preset camera, rain, halos, lights, placeholder cards  -> anchors dict
    S.set_crowd_umbrellas(0.5); S.render('/abs/out.png')
CLI:  python3 street.py final street_wide [RAIN|DUSK_RAIN]     (720x1280 -> street_work/final/)     python3 street.py contact    (the contact sheet)

World: 1 unit = 1 head (adults ~3.2), Z up, street along +y, roadway x -5.9..5.9 (crown z 0), pavements to x +-9.8 (z 0.28), house fronts x = +-9.8,
cornices z 19.35. Right row (x > 0) faces the key (warm), left row is in blue shade. Hackney coach rank on the right kerb (4 coaches, y 22..71.5).
Imports (never copies) the film 2 / 5 / 6 / 8 / 9 / 10 helpers like harbour.py does."""
import os, sys, math, json, time, random
import numpy as np
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d10'), os.path.join(PROJ, 'v3', 'set3d9'), os.path.join(PROJ, 'v3', 'set3d8'), os.path.join(PROJ, 'v3', 'set3d2'),
          os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6'), os.path.join(PROJ, 'v3', 'set3d7')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import mine as MN                                          # noqa: E402
import wall as W9                                          # noqa: E402  (film-9 set: air / mist compositor)
import street_tex as ST                                    # noqa: E402
import street_parts as PT                                  # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, _obj, _untoon, _append_shader, _light   # noqa: E402,F401
WORK = os.path.join(HERE, 'street_work')
T.ACT = os.path.join(WORK, 'actors')                       # placeholder actor art stays inside this folder
STATE = T.STATE
def _rnd(seed): return random.Random(seed)

# ----------------------------------------------------------------------------- light
def _kdaz(az, el):
    e = math.radians(el); a = math.radians(az)
    return (-math.cos(a) * math.cos(e), -math.sin(a) * math.cos(e), -math.sin(e))

P_RAIN = dict(toon=1.0, key_desat=0.08, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, sun_angle=0.6, wet=1.0, lamps=1.0, lamp_k=1.0,
              key=(2.0, 1.16, 0.5), key_dir=_kdaz(205, 60), sun_elev=60, shade=(0.17, 0.165, 0.46), shade_tint=(0.16, 0.15, 0.46), shade_mix=0.78,
              grade_offset=(0.0, -0.004, -0.008), lift=(0.008, 0.008, 0.026), sky='sky_rain', sky_k=1.0, grade_saturation=1.14,
              bounce=(1.0, 0.7, 0.45, 0.07), air=('#d8b8a8', 0.5, 60.0, 260.0), beams=0.0, rain=1.0)
P_DUSK_RAIN = dict(P_RAIN, key=(1.55, 0.86, 0.38), key_dir=_kdaz(205, 40), sun_elev=40, shade=(0.105, 0.115, 0.36), shade_tint=(0.10, 0.10, 0.40), shade_mix=0.8,
                   lamps=1.6, lamp_k=1.7, sky='sky_dusk', sky_k=0.95, grade_saturation=1.1, lift=(0.006, 0.007, 0.03), air=('#a49cc8', 0.5, 60.0, 260.0), bounce=(0.9, 0.6, 0.5, 0.06))
LIGHTS = dict(RAIN=P_RAIN, DUSK_RAIN=P_DUSK_RAIN)

X0 = 9.8                    # house front
XK = 5.9                    # roadway edge (kerb face)
XP = 6.3                    # pavement edge
ZP = 0.28                   # pavement level
Y0, Y1 = -56.0, 112.0       # row extent
LOT = 8.0
H_FAC = 19.35               # cornice base (top of the painted facade)
RANK_X = 3.55; RANK_Y = (22.0, 38.5, 55.0, 71.5)          # coach origins (coaches face -y; the horse stands at y - 5.6)
BOX_Z = 4.22                                              # standing height of a coachman on the box seat

# ----------------------------------------------------------------------------- cameras, presets, stand points
def _cam(a, b, la, lb, lens=22): return dict(loc=a, look_at=la, lens=lens, loc_b=b, look_b=lb)
CAMS = dict(
    street_wide=_cam((1.0, -14.0, 3.4), (0.6, -4.0, 3.3), (0.3, 40.0, 3.2), (0.3, 40.0, 3.5)),
    street_high=_cam((-3.0, -20.0, 32.0), (-2.0, -9.0, 17.0), (0.5, 34.0, 1.0), (0.5, 32.0, 2.0)),
    coach_low=_cam((-3.6, 4.2, 1.35), (-1.0, 7.5, 1.5), (3.6, 19.0, 3.3), (3.55, 19.5, 3.9)),
    hero_track=_cam((-3.8, 0.4, 2.2), (-3.6, 10.2, 2.2), (-0.6, 8.0, 3.3), (-0.6, 17.8, 3.3)),
    box_seat=_cam((-1.6, 10.0, 1.5), (0.2, 12.4, 2.3), (3.2, 18.6, 5.9), (3.4, 18.6, 6.3)),
    market=_cam((0.4, 0.4, 2.0), (-0.8, 3.0, 2.1), (-6.0, 11.0, 2.9), (-6.4, 11.5, 3.0)),
    puddle_low=_cam((-5.3, 3.6, 0.75), (-5.3, 4.6, 0.7), (-1.8, 12.6, 2.0), (-2.2, 12.6, 2.2)),
    rank_rush=_cam((-3.4, 4.0, 3.0), (-3.4, 10.0, 3.6), (3.4, 28.0, 3.4), (3.4, 36.0, 3.4)),
)
PRESETS = list(CAMS)
LIGHT_NAMES = list(LIGHTS)

def _stand(x, y, z=0.0, lx=0.0, ly=-1.0, note=''): return dict(pos=(x, y, z), look=(lx, ly), note=note)
# global named actor stand points (feet; z is the floor under the feet). look = the direction the actor faces on the ground (unit-ish); a card faces it
# with yaw = atan2(lx, -ly) about z (that is what tower.placeholder_actor does for face_to). heading_deg = atan2(ly, lx) (0 = +x, 90 = +y, -90 = toward street_wide).
STAND = {
    # --- the hero (Hanway walks the roadway under his umbrella)
    'hanway_a':      _stand(-0.9, 3.0, 0.0, 0.0, -1.0, 'street_wide: walks toward the camera down the left of the crown'),
    'hanway_b':      _stand(-1.2, 8.0, 0.0, 0.2, -1.0, 'hero_track start: medium, rank behind right'),
    'hanway_c':      _stand(-1.2, 17.8, 0.0, 0.2, -1.0, 'hero_track end (walk a -> b -> c along +y, face the camera)'),
    'hanway_low':    _stand(-2.4, 12.5, 0.0, 0.5, -1.0, 'coach_low: passes below the first coach'),
    'hanway_market': _stand(-2.6, 10.5, 0.0, 0.5, -1.0, 'market: passes the barrow corner'),
    'hanway_mud':    _stand(-3.8, 14.2, 0.0, 0.5, -1.0, 'puddle_low: beside the big puddle, the splash target (faces the camera)'),
    'hanway_crowd':  _stand(-1.0, 16.0, 0.0, 0.0, -1.0, 'street_high: the one umbrella among many'),
    # --- the three coachmen on their boxes (feet on the seat plank, z 4.22; the coaches face -y)
    'box_a':         _stand(RANK_X, RANK_Y[0] - 3.4, BOX_Z, -0.5, -0.85, 'HEAD coachman (coach_0 box)'),
    'box_b':         _stand(RANK_X, RANK_Y[1] - 3.4, BOX_Z, -0.6, -0.8, 'coachman_b (coach_1 box)'),
    'box_c':         _stand(RANK_X, RANK_Y[2] - 3.4, BOX_Z, -0.6, -0.8, 'coachman_c (coach_2 box)'),
    'box_d':         _stand(RANK_X, RANK_Y[3] - 3.4, BOX_Z, -0.6, -0.8, 'coachman_d (coach_3 box)'),
    # --- road / pavement people
    'man_road_1':    _stand(-4.2, 16.0, 0.0, 0.5, -1.0, 'passer-by on the left of the road'),
    'man_road_2':    _stand(0.2, 22.0, 0.0, 0.0, -1.0, 'passer-by mid road'),
    'lady_market':   _stand(-4.4, 8.0, 0.0, 0.5, -1.0, 'market: the dry lady under a parasol-umbrella'),
    'gent_wet':      _stand(-5.4, 11.8, 0.0, 0.7, -0.7, 'market: the soaked gentleman (wrings his wig)'),
    'seller':        _stand(-7.9, 12.6, ZP, 0.8, -0.6, 'market: stall holder behind the barrow'),
    'jeer_a':        _stand(-7.0, 7.0, ZP, 0.8, -0.5, 'market jeerer on the pavement'),
    'jeer_b':        _stand(-4.5, 11.6, 0.0, 0.8, -0.6, 'market jeerer in the road (the thrower)'),
    'pave_L1':       _stand(-7.4, 4.0, ZP, 0.6, -1.0, 'left pavement, street_wide foreground'),
    'pave_R1':       _stand(7.7, 6.0, ZP, -0.4, -1.0, 'right pavement, street_wide foreground'),
    'pave_R2':       _stand(7.6, 20.5, ZP, -0.5, -1.0, 'right pavement'),
    'pave_L2':       _stand(-7.4, 21.0, ZP, 0.5, -1.0, 'left pavement'),
    # --- passengers' side of the rank: the crowd rushes here (see A['rush'])
    'queue_a':       _stand(1.0, 22.0, 0.0, 0.9, 0.0, 'by the head coach street-side door (coach_0), faces the coach'),
    'mud_wheel':     _stand(-1.7, 12.2, 0.0, 0.0, -1.0, 'mud_splash: the wheel contact point (a position, not an actor)'),
}
STAGE = {                   # placeholder cards staged by stage_placeholders (name, role, umbrella)
    'street_wide': [('hanway_a', 'hero', 'umb_dark'), ('man_road_1', 'man', 'umb_brown'), ('box_a', 'coachman', None), ('pave_R1', 'woman', 'umb_blue')],
    'street_high': [('hanway_crowd', 'hero', 'umb_dark'), ('box_a', 'coachman', None)],
    'coach_low': [('box_a', 'coachman', None), ('box_b', 'man', None), ('hanway_low', 'hero', 'umb_dark')],
    'hero_track': [('hanway_b', 'hero', 'umb_dark'), ('hanway_c', 'hero', 'umb_dark'), ('box_a', 'coachman', None), ('box_b', 'man', None)],
    'box_seat': [('box_a', 'coachman', None)],
    'market': [('hanway_market', 'hero', 'umb_dark'), ('lady_market', 'woman', 'umb_green'), ('gent_wet', 'man', None), ('seller', 'coachman', None)],
    'puddle_low': [('hanway_mud', 'hero', 'umb_dark')],
    'rank_rush': [('box_a', 'coachman', None), ('box_b', 'man', None)],
}
STAGE_B = {                 # which stand points are valid (in frame, heads above y 880) at the END pose B of the camera move; default = all of STAGE
    'street_wide': ['hanway_a', 'man_road_1', 'box_a'], 'coach_low': ['box_a', 'box_b'], 'hero_track': ['hanway_c'], 'rank_rush': ['box_b'], 'market': ['hanway_market', 'lady_market', 'gent_wet', 'seller']}
PH_ROLES = dict(hero=('priest', 3.1), man=('extra_a', 2.9), coachman=('extra_c', 3.0), woman=('extra_b', 2.9))

# ----------------------------------------------------------------------------- materials
def _wetgloss(m, k, rough, hmap=None, hscale=1.0, bump=0.25, fres=True, tint=(1.0, 0.95, 0.9)):
    """Glossy lobe with Fresnel-weighted strength (wet stone / water): the reflection of the lit windows, lamps and sky."""
    def make(nt):
        N = nt.nodes.new; L = nt.links.new
        gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
        if fres:
            fr = N('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.38
            mx = N('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs[6].default_value = (*(c * k * 0.3 for c in tint), 1); mx.inputs[7].default_value = (*(c * k for c in tint), 1)
            L(fr.outputs['Fac'], mx.inputs[0]); L(mx.outputs[2], gl.inputs['Color'])
        else: gl.inputs['Color'].default_value = (*(c * k for c in tint), 1)
        if hmap:
            tx = N('ShaderNodeTexImage'); tx.image = T._img(hmap); tx.image.colorspace_settings.name = 'Non-Color'
            bp = N('ShaderNodeBump'); bp.inputs['Strength'].default_value = bump; bp.inputs['Distance'].default_value = 0.05
            L(tx.outputs['Color'], bp.inputs['Height']); L(bp.outputs['Normal'], gl.inputs['Normal'])
        return gl.outputs['BSDF']
    return _append_shader(m, make)


def _mat_pud(name, tex, layer, TXf, tint=(0.5, 0.55, 0.8), k=0.8, rough=0.04, strength=1.0):
    """Puddle layer as an OPAQUE wet-setts shader (the road texture, darkened and tinted, under a Fresnel mirror) whose alpha is the decal mask (only the soft shore
    band is stochastic, no noisy see-through film inside). Mask RGB (non-colour): R body alpha, G shore line, B deep core. The road texture is sampled with the
    mesh's 2nd UV map 'UVW' (world / road tile). layer: 'shallow' | 'core' | 'halo'."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    base = TXf('cobbles', form=False, sm=tint); m = base.copy(); m.name = name; nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
    uvn = N('ShaderNodeUVMap'); uvn.uv_map = 'UVW'
    for n in list(nt.nodes):
        if n.bl_idname == 'ShaderNodeTexImage': L(uvn.outputs['UV'], n.inputs['Vector'])
    out = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeOutputMaterial'][0]; last = out.inputs['Surface'].links[0].from_socket
    if layer != 'halo':
        def make(nt_):
            gl = nt_.nodes.new('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
            fr = nt_.nodes.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.33
            mp = nt_.nodes.new('ShaderNodeMath'); mp.operation = 'MULTIPLY_ADD'; mp.inputs[1].default_value = 0.85 * k; mp.inputs[2].default_value = 0.12 * k; mp.use_clamp = True
            nt_.links.new(fr.outputs['Fac'], mp.inputs[0]); gc = nt_.nodes.new('ShaderNodeMix'); gc.data_type = 'RGBA'; gc.inputs[6].default_value = (0, 0, 0, 1); gc.inputs[7].default_value = (1, 1, 1, 1)
            nt_.links.new(mp.outputs[0], gc.inputs[0]); nt_.links.new(gc.outputs[2], gl.inputs['Color']); return gl.outputs['BSDF']
        ad = N('ShaderNodeAddShader'); L(last, ad.inputs[0]); L(make(nt), ad.inputs[1]); last = ad.outputs['Shader']
    tx = N('ShaderNodeTexImage'); tx.image = T._img(tex); tx.image.colorspace_settings.name = 'Non-Color'
    sp = N('ShaderNodeSeparateColor'); L(tx.outputs['Color'], sp.inputs['Color']); tr = N('ShaderNodeBsdfTransparent')
    fac = N('ShaderNodeMath'); fac.operation = 'MULTIPLY'; fac.use_clamp = True
    if layer == 'core': L(sp.outputs[2], fac.inputs[0]); fac.inputs[1].default_value = 1.0
    else: L(sp.outputs[0], fac.inputs[0]); fac.inputs[1].default_value = 0.9 if layer == 'halo' else 1.0
    mx = N('ShaderNodeMixShader'); L(fac.outputs[0], mx.inputs['Fac']); L(tr.outputs['BSDF'], mx.inputs[1]); L(last, mx.inputs[2]); last = mx.outputs['Shader']
    if layer == 'shallow':                                                      # pale shore line, a thin glint (emission), weighted by the G channel
        rim = N('ShaderNodeEmission'); rim.inputs['Color'].default_value = (0.6, 0.68, 0.95, 1); rm = N('ShaderNodeMath'); rm.operation = 'MULTIPLY'; rm.inputs[1].default_value = 0.12 * strength
        L(sp.outputs[1], rm.inputs[0]); L(rm.outputs[0], rim.inputs['Strength']); a2 = N('ShaderNodeAddShader'); L(last, a2.inputs[0]); L(rim.outputs['Emission'], a2.inputs[1]); last = a2.outputs['Shader']
    L(last, out.inputs['Surface']); m.cycles.emission_sampling = 'NONE'
    return m

def _mat_water(name, base='#1d2a58', rough=0.05, k=0.9, deep=0.0, body=0.3):
    """Gutter water strip: a see-through dark blue film plus a Fresnel-weighted mirror."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*T.hex_lin(base), 1); em.inputs['Strength'].default_value = 1.0
    tr = N('ShaderNodeBsdfTransparent'); mb_ = N('ShaderNodeMixShader'); mb_.inputs['Fac'].default_value = body; L(tr.outputs['BSDF'], mb_.inputs[1]); L(em.outputs['Emission'], mb_.inputs[2])
    gl = N('ShaderNodeBsdfGlossy'); gl.distribution = 'GGX'; gl.inputs['Roughness'].default_value = rough
    fr = N('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.33
    mp = N('ShaderNodeMath'); mp.operation = 'MULTIPLY_ADD'; mp.inputs[1].default_value = 0.9 * k; mp.inputs[2].default_value = 0.12 + deep; mp.use_clamp = True; L(fr.outputs['Fac'], mp.inputs[0])
    gc = N('ShaderNodeMix'); gc.data_type = 'RGBA'; gc.inputs[6].default_value = (0, 0, 0, 1); gc.inputs[7].default_value = (1, 1, 1, 1); L(mp.outputs[0], gc.inputs[0]); L(gc.outputs[2], gl.inputs['Color'])
    ad = N('ShaderNodeAddShader'); L(mb_.outputs['Shader'], ad.inputs[0]); L(gl.outputs['BSDF'], ad.inputs[1]); L(ad.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_streak(name, rgb=(0.78, 0.86, 1.0), k=1.6, opacity=0.5):
    """Rain / drip streak: camera-only, a pale cool emission mixed over what is behind (crisp, not additive-blurred)."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); em.inputs['Strength'].default_value = k
    tr = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = opacity
    lp = N('ShaderNodeLightPath'); mx2 = N('ShaderNodeMixShader'); tr2 = N('ShaderNodeBsdfTransparent')
    L(tr.outputs['BSDF'], mx.inputs[1]); L(em.outputs['Emission'], mx.inputs[2])
    L(lp.outputs['Is Camera Ray'], mx2.inputs['Fac']); L(tr2.outputs['BSDF'], mx2.inputs[1]); L(mx.outputs['Shader'], mx2.inputs[2]); L(mx2.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m

def _mat_halo(name, image, rgb, k):
    """Camera-only additive lamp halo card."""
    if name in bpy.data.materials: return bpy.data.materials[name]
    m = bpy.data.materials.new(name); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputMaterial'); tx = N('ShaderNodeTexImage'); tx.image = T._img(image)
    bw = N('ShaderNodeRGBToBW'); L(tx.outputs['Color'], bw.inputs[0]); st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = k; L(bw.outputs[0], st.inputs[0])
    em = N('ShaderNodeEmission'); em.inputs['Color'].default_value = (*rgb, 1); L(st.outputs[0], em.inputs['Strength'])
    tr = N('ShaderNodeBsdfTransparent'); ad = N('ShaderNodeAddShader'); L(tr.outputs['BSDF'], ad.inputs[0]); L(em.outputs['Emission'], ad.inputs[1])
    lp = N('ShaderNodeLightPath'); tr2 = N('ShaderNodeBsdfTransparent'); mx = N('ShaderNodeMixShader')
    L(lp.outputs['Is Camera Ray'], mx.inputs['Fac']); L(tr2.outputs['BSDF'], mx.inputs[1]); L(ad.outputs['Shader'], mx.inputs[2]); L(mx.outputs['Shader'], out.inputs['Surface'])
    m.cycles.emission_sampling = 'NONE'
    return m


def _materials(P, C, TX, tx, pre):
    M = {}
    M['cobbles'] = _wetgloss(TX('cobbles', form=False), 0.16, 0.3, hmap=tx['cobbles_h'], bump=0.7)
    M['pave'] = _wetgloss(TX('pave', form=False), 0.3, 0.14)
    M['kerb'] = _wetgloss(TX('kerb'), 0.22, 0.14)
    M['gutter_flow'] = _wetgloss(TX('gutter', form=False, glow='gutter', glow_k=0.18), 0.55, 0.08, fres=True, tint=(0.9, 0.95, 1.0))
    M['gutter'] = M['gutter_flow']
    for k in ('fac_a', 'fac_b', 'fac_c', 'fac_d', 'fac_e', 'fac_f', 'fac_g', 'fac_h', 'fac_i', 'fac_j', 'fac_s1', 'fac_s2', 'fac_s3', 'fac_s4', 'fac_s5', 'fac_s6'):
        M[k] = TX(k, glow=k + '_glow', glow_k=1.25 * P['lamps'])
    M['brick_a'] = TX('brickwall_a'); M['brick_b'] = TX('brickwall_b')
    M['slate'] = TX('slate'); M['wood'] = TX('wood'); M['wood_d'] = TX('wood_d')
    M['barrel'] = TX('barrel'); M['awn_a'] = TX('awn_a', sm=(1.2, 1.0, 1.0)); M['awn_b'] = TX('awn_b')
    M['cream'] = C('#eadfc0'); M['stone'] = C('#cfc6b0'); M['stone_d'] = C('#9a94a0')
    M['iron'] = _wetgloss(C('#26262e', 1.0, 1.2), 0.5, 0.25, fres=False)
    M['iron_b'] = C('#1c1c24', 1.0, 1.2)
    M['brass'] = _wetgloss(C('#c4902c', 1.0, (2.0, 1.4, 0.6), smix=0.2), 0.6, 0.25, fres=False, tint=(1.0, 0.8, 0.5))
    M['green'] = C('#2f5c46'); M['oxblood'] = C('#6e2433'); M['navy'] = C('#2b3f66'); M['cream_w'] = C('#f2ead4'); M['plum'] = C('#4a2c5c')
    M['lead'] = C('#5a5e6c', 1.0, 1.1); M['pot'] = C('#b8683c')
    M['coach_green'] = C('#2c5c48', 1.0, 1.3); M['coach_green_d'] = C('#18322a', 1.0, 1.3); M['coach_ox'] = C('#7c2c38', 1.0, 1.3); M['coach_ox_d'] = C('#3a141c', 1.0, 1.3)
    M['coach_navy'] = C('#2e4880', 1.0, 1.3); M['coach_navy_d'] = C('#161e3c', 1.0, 1.3); M['coach_ochre'] = C('#b88a3c', 1.0, 1.3); M['coach_ochre_d'] = C('#4a3418', 1.0, 1.3)
    M['coach_gold'] = C('#d8b048', 1.0, (1.6, 1.3, 0.7), smix=0.2); M['coach_crest'] = C('#9c2c34', 1.0, 1.2)
    M['wheel'] = C('#3a2a1c', 1.0, 1.1); M['wheel_r'] = C('#8a3028', 1.0, (1.3, 0.9, 0.8), smix=0.8); M['wheel_r2'] = C('#6a2420', 1.0, (1.3, 0.9, 0.8), smix=0.8)
    M['cloth'] = C('#7a2434', 1.0, (1.4, 0.8, 0.8), smix=0.8); M['leather'] = C('#3a2a22', 1.0, 1.1); M['passenger'] = C('#0e1018', 1.0, 0.8)
    M['horse'] = C('#8a4a28', 1.0, (1.3, 1.0, 0.9), smix=0.65); M['horse_b'] = C('#5c3220', 1.0, (1.3, 1.0, 0.9), smix=0.65); M['horse_c'] = C('#a8a4b4', 1.0, (1.1, 1.1, 1.1), smix=0.65)
    M['horse_k'] = C('#26222a', 1.0, (1.2, 1.1, 1.2), smix=0.65)
    M['horse_d'] = C('#2e1c14'); M['horse_dk'] = C('#1c1820'); M['horse_wm'] = C('#e8e2d4'); M['horse_w'] = C('#f0e6d4'); M['hoof'] = C('#1c1a1e')
    M['canvas'] = C('#d4c298'); M['sack'] = C('#b8a070'); M['umb_dark'] = C('#141622', 0.8, 1.0)
    M['umb_brown'] = C('#6a4632'); M['umb_green'] = C('#2c5a46'); M['umb_blue'] = C('#2a3e78'); M['umb_red'] = C('#8a2a32'); M['umb_ochre'] = C('#a07a30'); M['umb_grey'] = C('#58586a')
    M['pink'] = mat_emit(pre + 'e_pink', image=tx['lace'], strength=0.95, alpha=True)
    M['cabbage'] = C('#5c9a4a', 1.0, (1.2, 1.1, 1.0), smix=0.5); M['carrot'] = C('#e07a2a', 1.0, (1.3, 0.9, 0.8), smix=0.6); M['apple'] = C('#b8302a', 1.0, (1.3, 0.8, 0.8), smix=0.7)
    M['turnip'] = C('#e8dcc8'); M['onion'] = C('#c89a50'); M['turnip_top'] = C('#8a4a8a'); M['egg'] = C('#f4ecd8', 1.0, 1.2)
    M['fig_a'] = C('#3a3a5c', 1.0, 1.2); M['fig_b'] = C('#5c4630', 1.0, 1.2); M['fig_c'] = C('#2c4a3c', 1.0, 1.2); M['fig_d'] = C('#6c3438', 1.0, 1.2); M['fig_e'] = C('#6a6a7c', 1.0, 1.2)
    M['fig_skin'] = C('#e4bc98', 1.0, (1.1, 1.0, 1.0), smix=0.3); M['fig_leg'] = C('#2c2830'); M['fig_hat'] = C('#1c1a22')
    M['mud'] = mat_emit(pre + 'e_mud', '#8a6840', strength=0.75); M['mud_hi'] = mat_emit(pre + 'e_mudhi', '#dcc490', strength=0.9)
    M['glass_lamp'] = mat_emit(pre + 'e_lamp', '#ffd890', strength=4.2); M['lantern'] = mat_emit(pre + 'e_lantern', '#ffc070', strength=3.4)
    M['shopwin'] = {k: mat_emit(pre + 'e_sw_' + k, image=tx['shopwin_' + k], strength=1.25) for k in ('boots', 'teapots', 'pretzels', 'greens', 'hats', 'jars')}
    M['sign'] = {k: TX('sign_' + k, form=False, alpha=True) for k in ('boot', 'teapot', 'pretzel', 'hat', 'jar')}
    M['pud_s'] = {k: _mat_pud(pre + 'pud_s' + k, tx['pud_' + k], 'shallow', TX, (0.46, 0.5, 0.82), 0.8, 0.07) for k in 'abcd'}
    M['pud_c'] = {k: _mat_pud(pre + 'pud_c' + k, tx['pud_' + k], 'core', TX, (0.28, 0.32, 0.62), 1.0, 0.05) for k in 'abcd'}
    M['pud_h'] = {k: _mat_pud(pre + 'pud_h' + k, tx['pud_' + k], 'halo', TX, (0.62, 0.64, 0.82)) for k in 'abcd'}
    M['ripple'] = {k: mat_emit(pre + 'e_rip_' + k, image=tx['ripples_' + k], strength=0.55, alpha=True) for k in ('a', 'b')}
    M['rain'] = _mat_streak(pre + 'rain', (0.84, 0.91, 1.0), 1.5, 0.34); M['drip'] = _mat_streak(pre + 'drip', (0.86, 0.92, 1.0), 1.5, 0.5)
    M['halo'] = _mat_halo(pre + 'halo', tx['halo'], (1.0, 0.62, 0.26), 1.3); M['halo_w'] = _mat_halo(pre + 'halo_w', tx['halo'], (1.0, 0.7, 0.4), 0.7)
    M['sky'] = mat_emit(pre + 'sky', image=tx[P['sky']], strength=P['sky_k'])
    M['flame'] = mat_emit(pre + 'e_flame', '#ffe8a8', strength=7.0)
    M['splat_egg'] = TX('splat_egg', form=False, alpha=True); M['splat_cab'] = TX('splat_cab', form=False, alpha=True)
    return M

# ----------------------------------------------------------------------------- tiny geometry helpers
# ----------------------------------------------------------------------------- tiny geometry helpers
def qface(mb, p0, pu, pv, mat, uv, normal):
    p0, pu, pv = Vector(p0), Vector(pu), Vector(pv); u0, v0, u1, v1 = uv
    mb.oface([p0, p0 + pu, p0 + pu + pv, p0 + pv], mat, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)], normal)

def bx(mb, lo, hi, mat, **kw):
    mb.box(lo, hi, mat, **kw)

def cyl(mb, p0, p1, r, mat, seg=8, r1=None, caps=True):
    mb.frustum(p0, p1, r, r if r1 is None else r1, mat, seg=seg, cap0=caps, cap1=caps)

def streak_poly(mb, mat, p, d, side, L, w):
    """Pointed ribbon centred at p along unit d, half width w/2 along unit side."""
    p = Vector(p); a = p - d * (L / 2); b = p + d * (L / 2); s = side * (w / 2)
    mb.face([a, p - s * 0.9 + d * (-L * 0.15), p - s + d * (L * 0.15), b, p + s + d * (L * 0.15), p + s * 0.9 + d * (-L * 0.15)][::-1] if False else [a, p + s + d * (-L * 0.1), b, p - s + d * (-L * 0.1)], mat)


# ----------------------------------------------------------------------------- the ground
def _ground(SET, M):
    mb = MB(); T4 = ROAD_TILE
    def ground_quad(x0, x1, y0, y1, z, mat, tile=T4):
        qface(mb, (x0, y0, z), (x1 - x0, 0, 0), (0, y1 - y0, 0), mat, (x0 / tile, y0 / tile, x1 / tile, y1 / tile), (0, 0, 1))
    ground_quad(-XK, XK, Y0 - 40, Y1 + 120, 0.0, M['cobbles'])
    ground_quad(-60, -XK, 44, 52, 0.0, M['cobbles'])
    _obj(mb, 'road', SET)
    pv = MB()
    for s in (-1, 1):
        x0, x1 = (XP, X0 + 0.6) if s > 0 else (-X0 - 0.6, -XP)
        qface(pv, (x0, Y0 - 40, ZP), (x1 - x0, 0, 0), (0, Y1 + 160 - Y0, 0), M['pave'], (x0 / 4, (Y0 - 40) / 4, x1 / 4, (Y1 + 120) / 4), (0, 0, 1))
        lo = (XK, Y0 - 40, 0.0) if s > 0 else (-XP, Y0 - 40, 0.0); hi = (XP, Y1 + 120, ZP) if s > 0 else (-XK, Y1 + 120, ZP)
        pv.box(lo, hi, M['kerb'], tile=(4, 4))
    _obj(pv, 'pavement', SET)
    ln = MB(); qface(ln, (-X0 - 0.6, 44, ZP + 0.01), (X0 + 0.6 - XP, 0, 0), (0, 8, 0), M['cobbles'], ((-X0 - 0.6) / ROAD_TILE, 40 / ROAD_TILE, -XP / ROAD_TILE, 48 / ROAD_TILE), (0, 0, 1)); _obj(ln, 'lane_floor', SET)
    gb = MB(); qface(gb, (-90, Y0 - 40, -0.05), (180, 0, 0), (0, Y1 - Y0 + 160, 0), M['cobbles'], (-20, 0, 20, 40), (0, 0, 1)); _obj(gb, 'ground_far', SET)
    # gutters: a channel of running water next to each kerb (flow texture + glossy film, with a pale bank line)
    gt = MB(); gm = MB(); L_ = Y1 + 120 - Y0 + 40
    for s in (-1, 1):
        xa, xb = (XK - 0.85, XK - 0.04) if s > 0 else (-XK + 0.04, -XK + 0.85)
        qface(gt, (xa, Y0 - 40, 0.03), (xb - xa, 0, 0), (0, L_, 0), M['gutter_flow'], (0, 0, 1, L_ / 4), (0, 0, 1))
    _obj(gt, 'gutters', SET)
    # gully gratings: a few dark slotted plates at the kerb (iron, with slots)
    gg = MB()
    for y in (-20.0, 6.0, 33.0, 60.0, 88.0):
        for s in (-1, 1):
            xc = s * (XK - 0.45)
            gg.box((xc - 0.42, y - 0.5, 0.037), (xc + 0.42, y + 0.5, 0.06), M['iron_b'])
            for k in range(5): gg.box((xc - 0.36, y - 0.4 + 0.2 * k, 0.062), (xc + 0.36, y - 0.4 + 0.2 * k + 0.06, 0.066), M['gutter'])
    _obj(gg, 'gratings', SET)

def _puddles(SET, M):
    """Layered puddle DECALS (no fan triangles): per puddle a soft dark wet halo on the setts, a see-through shallow film with a pale shore line and a deeper,
    darker core (all from one 512 px mask, irregular outline, soft edge), plus soft ripple rings that appear with the rain intensity. Returns the list of
    (x, y, radius) incl. the named big ones: BIG puddle (puddle_low) at (-1.5, 12.0)."""
    rs = _rnd(5)
    spots = [(-1.7, 12.4, 3.3), (-4.2, 6.6, 2.0), (-0.2, 6.8, 1.6), (2.6, 8.6, 1.7), (-4.1, 18.5, 2.1), (1.2, 27.0, 2.3), (-1.8, 34.0, 2.5), (-3.2, -4.0, 2.2), (1.8, -9.0, 2.6),
             (-0.6, 19.5, 1.6), (4.4, 2.0, 1.5), (-4.6, 26.0, 1.7), (0.4, 44.0, 2.4), (-2.4, 52.0, 2.2), (2.0, 62.0, 2.2), (-3.6, 70.0, 2.0), (0.0, -16.0, 2.4)]
    for i in range(44):
        y = rs.uniform(-14, 80); side = rs.choice([-1, 1]); x = rs.choice([rs.uniform(-4.0, 4.0), side * rs.uniform(3.4, 5.0)]); r = rs.uniform(0.7, 1.8) * (1.3 if rs.random() < 0.2 else 1.0)
        if all((x - a) ** 2 + (y - b) ** 2 > (r + c + 0.6) ** 2 for a, b, c in spots): spots.append((x, y, r))
    halo = {k: MB() for k in 'abcd'}; shal = {k: MB() for k in 'abcd'}; core = {k: MB() for k in 'abcd'}; rip = [MB() for _ in range(4)]
    for (x, y, r) in spots:
        if abs(x) > XK - 0.35: x = math.copysign(XK - 0.35 - 0.2 * r, x)
        k = 'abcd'[rs.randrange(4)]; yaw = rs.uniform(0, 6.28); c, s_ = math.cos(yaw), math.sin(yaw)
        def quad(mb, hs, z):
            pts = [(-hs, -hs), (hs, -hs), (hs, hs), (-hs, hs)]
            w = [Vector((x + px * c - py * s_, y + px * s_ + py * c, z)) for px, py in pts]
            mb.oface(w, M['pud_s'][k], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
        hs = r / 0.62
        quad(halo[k], hs * 1.45, 0.008); quad(shal[k], hs, 0.012); quad(core[k], hs, 0.016)
        for j in range(rs.choice([1, 2, 3])):
            rx, ry = x + rs.uniform(-0.4, 0.4) * r, y + rs.uniform(-0.4, 0.4) * r; sz = rs.uniform(0.3, 0.55) * min(r, 1.7) * 1.4; mt = 'ab'[rs.randrange(2)]
            rip[rs.randrange(4)].oface([Vector((rx - sz, ry - sz, 0.02)), Vector((rx + sz, ry - sz, 0.02)), Vector((rx + sz, ry + sz, 0.02)), Vector((rx - sz, ry + sz, 0.02))], M['ripple'][mt],
                                       [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
    for k in 'abcd':
        for mb, nm, mat in ((halo[k], 'pud_halo_', M['pud_h'][k]), (shal[k], 'pud_shallow_', M['pud_s'][k]), (core[k], 'pud_core_', M['pud_c'][k])):
            if mb.f:
                mb.mats = [mat]; mb.mi = [0] * len(mb.f); o_ = _obj(mb, nm + k, SET, shadow=False); me = o_.data; uvw = me.uv_layers.new(name='UVW')
                for li, lp in enumerate(me.loops): co = me.vertices[lp.vertex_index].co; uvw.data[li].uv = (co.x / ROAD_TILE, co.y / ROAD_TILE)
    ro = []
    for i, mb in enumerate(rip):
        if mb.f: ro.append(_obj(mb, 'ripples_%d' % i, SET, shadow=False))
    STATE['ripple_objs'] = ro; ctrl = _ctrl()
    for i, o in enumerate(ro): _drv(o, 'hide_render', 'k <= %g' % (i / 4.0), {'k': (ctrl, '["rain"]')})
    return spots
# ----------------------------------------------------------------------------- houses
ROAD_TILE = 3.2                                       # world units per cobble tile (5 x 8 setts: 0.64 x 0.4)
LANE = (40.0, 48.0)                                   # the cross lane on the left (a gap in the left terrace)
LEFT_SEQ = ['fac_b', 'fac_s2', 'fac_h', 'fac_a', 'fac_s5', 'fac_f', 'fac_s1', 'fac_e', 'fac_i', 'fac_s3', 'fac_g', 'fac_c', None, 'fac_j', 'fac_s4', 'fac_a', 'fac_d', 'fac_s6', 'fac_h', 'fac_b', 'fac_f', 'fac_s2']
RIGHT_SEQ = ['fac_d', 'fac_a', 'fac_s1', 'fac_g', 'fac_c', 'fac_s5', 'fac_b', 'fac_i', 'fac_s3', 'fac_f', 'fac_h', 'fac_s4', 'fac_e', 'fac_s2', 'fac_j', 'fac_a', 'fac_s6', 'fac_c', 'fac_d', 'fac_e', 'fac_s1', 'fac_b']
SHOPKIND = dict(fac_s1='boots', fac_s2='teapots', fac_s3='pretzels', fac_s4='greens', fac_s5='hats', fac_s6='jars')
SIGNKIND = dict(fac_s1='boot', fac_s2='teapot', fac_s3='pretzel', fac_s4=None, fac_s5='hat', fac_s6='jar')
SHOP_DOOR = dict(fac_s1=0, fac_s2=1, fac_s3=0, fac_s4=1, fac_s5=0, fac_s6=1)
SHOP_FASCIA = dict(fac_s1='green', fac_s2='oxblood', fac_s3='navy', fac_s4='wood', fac_s5='plum', fac_s6='navy')
DOORBAY = dict(fac_a=1, fac_b=0, fac_c=2, fac_d=0, fac_e=1, fac_f=2, fac_g=1, fac_h=0, fac_i=2, fac_j=1)
DOORSTYLE = dict(fac_a='fan', fac_b='transom', fac_c='arch', fac_d='transom', fac_e='fan', fac_f='arch', fac_g='arch', fac_h='fan', fac_i='transom', fac_j='fan')

class Row:
    """Collects the geometry of one terrace side into a few merged meshes (one per kind) so the scene stays light."""
    def __init__(s, name): s.name = name; s.fac = MB(); s.trim = MB(); s.roof = MB(); s.brk = MB(); s.iron = MB(); s.misc = MB(); s.glass = MB(); s.awn = MB(); s.sign = MB()

def _house(R, M, side, y0, fac, rs, lot_i):
    """One terrace house. side +1: right row (front at x = +X0, faces -x). y0 = the lot's low-y edge."""
    s = side; xf = s * X0; dirn = -s                              # outward normal of the front (toward the street)
    nrm = (dirn, 0, 0)
    # frame helpers: u along the front runs along -y for the right row (seen from the street, left to right), +y for the left row
    def Y(u): return y0 + (LOT - u if s > 0 else u)               # world y of texture coordinate u (units from the left edge as seen from the street)
    def box_f(u0, u1, z0, z1, depth, mat, d0=0.0, **kw):          # box protruding from the front by depth (from d0)
        ya, yb = sorted((Y(u0), Y(u1))); xa, xb = sorted((xf + dirn * d0, xf + dirn * (d0 + depth)))
        R.trim.box((xa, ya, z0), (xb, yb, z1), mat, **kw)
    # painted facade quad: u = x/8, v = z/20
    mat = M[fac]
    z1 = H_FAC; v1 = z1 / ST.FACADE_H
    p0 = (xf, Y(0), 0.0); pu = (0, Y(LOT) - Y(0), 0); pv = (0, 0, z1)
    qface(R.fac, p0, pu, pv, mat, (0, 0, 1, v1), nrm)
    # string courses and plinth, cornice, parapet
    box_f(0, 8, 5.45, 5.85, 0.16, M['cream']); box_f(0, 8, 10.75, 10.95, 0.1, M['cream']); box_f(0, 8, 15.05, 15.25, 0.1, M['cream'])
    box_f(0, 8, 0.0, 0.95, 0.12, M['stone'])
    box_f(0, 8, 19.35, 19.62, 0.95, M['cream']); box_f(0, 8, 19.62, 19.9, 0.7, M['cream_w'])
    ph = rs.choice([0.7, 1.0, 1.4, 1.8]) if rs.random() < 0.35 else 1.0
    box_f(0, 8, 19.9, 19.9 + ph, 0.0, M['brick_a' if rs.random() < 0.6 else 'brick_b'], d0=0.1) if False else None
    # parapet as a thin brick wall with stone coping
    ya, yb = sorted((Y(0), Y(8))); xa, xb = sorted((xf - dirn * 0.02, xf - dirn * 0.55))
    pw = M['brick_a' if lot_i % 2 else 'brick_b']
    R.brk.box((min(xa, xb), ya, 19.9), (max(xa, xb), yb, 19.9 + ph), pw, tile=(4, 4))
    xa2, xb2 = sorted((xf + dirn * 0.15, xf - dirn * 0.75)); R.trim.box((xa2, ya, 19.9 + ph), (xb2, yb, 19.9 + ph + 0.22), M['stone'])
    # window sills and lintels (painted too; the relief catches the key)
    xs = (1.4, 4.0, 6.6)
    for fi, (zc, h) in enumerate(((8.1, 3.3), (12.7, 3.1), (16.9, 2.4))):
        for cx in xs:
            box_f(cx - 0.95, cx + 0.95, zc - h / 2 - 0.2, zc - h / 2, 0.32, M['cream'])
            box_f(cx - 1.0, cx + 1.0, zc + h / 2 + 0.04, zc + h / 2 + 0.44, 0.14, M['cream'])
    shop = fac in SHOPKIND
    if not shop and lot_i % 3 == 1: _balcony(R, M, Y, xf, dirn, 0.5, 7.5, 6.35)
    if not shop:
        db = DOORBAY[fac]; dx = xs[db]
        for cx in xs:
            if cx == dx: continue
            box_f(cx - 0.95, cx + 0.95, 1.65, 1.85, 0.3, M['cream']); box_f(cx - 1.0, cx + 1.0, 4.4, 4.8, 0.14, M['cream'])
        # door surround: pilasters, entablature, triangular pediment, three steps, a lamp bracket
        box_f(dx - 1.0, dx - 0.72, 0.95, 4.9, 0.34, M['cream']); box_f(dx + 0.72, dx + 1.0, 0.95, 4.9, 0.34, M['cream'])
        box_f(dx - 1.15, dx + 1.15, 4.9, 5.2, 0.5, M['cream_w'])
        y_a, y_b = Y(dx - 1.15), Y(dx + 1.15); yc = (y_a + y_b) / 2
        pts = [(xf + dirn * 0.5, y_a, 5.2), (xf + dirn * 0.5, y_b, 5.2), (xf + dirn * 0.5, yc, 5.2 + 0.7)]
        for k in range(3):
            d0 = 0.35 + 0.3 * k; box_f(dx - 1.05 - 0.1 * (2 - k), dx + 1.05 + 0.1 * (2 - k), ZP * 0 + 0.0, 0.3 + 0.0 * k, 0.0, M['stone']) if False else None
        for k in range(3):
            d0 = 0.12 + 0.34 * k; zt = ZP + 0.0
            box_f(dx - 1.05, dx + 1.05, 0.0, 0.28 - 0.0 * k + 0.0, 0.0, M['stone']) if False else None
        # the pavement is z 0.28; steps rise to the door sill (z 0.95)
        for k in range(3):
            d0 = 0.15 + 0.4 * (2 - k); box_f(dx - 1.0, dx + 1.0, 0.0, ZP + 0.22 * (k + 1), 0.45, M['stone'], d0=d0 - 0.0)
        ds = DOORSTYLE[fac]
        if ds == 'fan':
            # triangular pediment: 3 faces (front = painted via cream) as a prism
            d_f = 0.5; xp = xf + dirn * d_f
            R.trim.face([(xf + dirn * 0.1, y_a, 5.2), (xf + dirn * 0.1, y_b, 5.2), (xf + dirn * 0.1, yc, 5.9)], M['cream_w'])
            R.trim.oface([(xp, y_a, 5.2), (xp, y_b, 5.2), (xp, yc, 5.9)], M['cream_w'], [(0, 0), (1, 0), (0.5, 0.5)], nrm)
            R.trim.oface([(xf + dirn * 0.1, y_a, 5.2), (xp, y_a, 5.2), (xp, yc, 5.9), (xf + dirn * 0.1, yc, 5.9)], M['cream'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 1))
            R.trim.oface([(xf + dirn * 0.1, y_b, 5.2), (xp, y_b, 5.2), (xp, yc, 5.9), (xf + dirn * 0.1, yc, 5.9)], M['cream'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 1, 1))
        elif ds == 'transom':                                   # flat hood on two console brackets
            box_f(dx - 1.3, dx + 1.3, 5.2, 5.38, 0.85, M['cream_w'])
            for sg in (-1, 1):
                box_f(dx + sg * 1.05 - 0.1, dx + sg * 1.05 + 0.1, 4.55, 5.2, 0.7, M['cream']); box_f(dx + sg * 1.05 - 0.07, dx + sg * 1.05 + 0.07, 4.35, 4.55, 0.45, M['cream'])
        else:                                                   # portico: two round columns carry a flat entablature with a stepped parapet
            for sg in (-1, 1):
                cc = Vector((xf + dirn * 1.15, Y(dx + sg * 1.12), 0.0)); R.trim.frustum(cc + Vector((0, 0, ZP + 0.3)), cc + Vector((0, 0, 5.0)), 0.2, 0.17, M['cream_w'], seg=8)
                R.trim.frustum(cc + Vector((0, 0, ZP + 0.3)), cc + Vector((0, 0, ZP + 0.6)), 0.3, 0.3, M['stone'], seg=8); R.trim.frustum(cc + Vector((0, 0, 4.9)), cc + Vector((0, 0, 5.15)), 0.3, 0.3, M['cream'], seg=8)
            box_f(dx - 1.45, dx + 1.45, 5.15, 5.55, 1.5, M['cream_w']); box_f(dx - 1.45, dx + 1.45, 5.55, 5.7, 1.5, M['cream'])
        # lamp over the door: brass bracket + a small glass lantern
        lam = Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.0)); R.glass.sphere(lam, 0.17, M['glass_lamp'], seg=8, rings=5)
        R.iron.frustum(Vector((xf + dirn * 0.05, Y(dx + 1.35), 5.4)), Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.4)), 0.035, 0.035, M['iron'], seg=4)
        R.iron.frustum(Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.4)), Vector((xf + dirn * 0.95, Y(dx + 1.35), 5.2)), 0.03, 0.03, M['iron'], seg=4)
        # area railings in front of the ground-floor windows
        for cx in xs:
            if cx == dx: continue
            _railing(R.iron, M, xf + dirn * 0.95 + 0.0, Y(cx - 1.25), Y(cx + 1.25), ZP, 1.7, s)
    else:
        kind = SHOPKIND[fac]; db = SHOP_DOOR[fac]
        u0, u1 = (2.6, 7.7) if db == 0 else (0.3, 5.6)
        _bow(R, M, s, y0, u0, u1, xf, dirn, Y, kind, fac)
        # fascia projection
        box_f(0, 8, 4.55, 5.45, 0.3, M[SHOP_FASCIA[fac]])
        box_f(0, 8, 5.45, 5.5, 0.34, M['brass']) if False else None
        # shop door steps and a lamp
        dx0 = 0.6 if db == 0 else 5.9
        for k in range(2):
            box_f(dx0 - 0.1, dx0 + 1.8, 0.0, ZP + 0.2 * (k + 1), 0.4, M['stone'], d0=0.1 + 0.4 * (1 - k))
        # hanging sign on an iron bracket at the pavement end of the fascia
        sk = SIGNKIND[fac]
        if sk:
            _sign(R, M, s, Y(7.5 if db == 0 else 0.5), xf, dirn, sk, rs)
        if fac == 'fac_s3' or fac == 'fac_s4':
            _awning(R, M, s, Y, xf, dirn, 'awn_a' if fac == 'fac_s3' else 'awn_b', u0, u1)
    # rainwater pipe at the left edge (as seen from the street) and a hopper head
    yp = Y(0.15); R.iron.frustum(Vector((xf + dirn * 0.18, yp, 0.3)), Vector((xf + dirn * 0.18, yp, 19.1)), 0.11, 0.11, M['lead'], seg=6)
    R.iron.box if False else None
    for zc in (4.0, 9.0, 14.0): R.iron.frustum(Vector((xf + dirn * 0.18, yp, zc)), Vector((xf + dirn * 0.18, yp, zc + 0.14)), 0.16, 0.16, M['iron_b'], seg=6)
    R.trim.box((min(xf + dirn * 0.0, xf + dirn * 0.5), yp - 0.3, 18.5), (max(xf + dirn * 0.0, xf + dirn * 0.5), yp + 0.3, 19.3), M['lead'])
    # chimneys + roof
    _roof(R, M, s, y0, xf, dirn, ph, rs, lot_i)

def _railing(mb, M, x, ya, yb, z0, h, s):
    """Iron area railing along y from ya to yb at x: spear-top rods every 0.45, two rails."""
    lo, hi = min(ya, yb), max(ya, yb); n = max(2, int((hi - lo) / 0.45))
    for i in range(n + 1):
        y = lo + (hi - lo) * i / n
        mb.frustum(Vector((x, y, z0)), Vector((x, y, z0 + h)), 0.035, 0.035, M['iron'], seg=4, cap0=False, cap1=False)
        mb.frustum(Vector((x, y, z0 + h)), Vector((x, y, z0 + h + 0.2)), 0.07, 0.0, M['iron'], seg=4, cap0=True, cap1=False)
    for zr in (z0 + 0.25, z0 + h - 0.2): mb.frustum(Vector((x, lo, zr)), Vector((x, hi, zr)), 0.035, 0.035, M['iron'], seg=4)
    for y in (lo, hi): mb.frustum(Vector((x, y, z0)), Vector((x, y, z0 + h + 0.1)), 0.075, 0.075, M['iron'], seg=5)

def _bow(R, M, s, y0, u0, u1, xf, dirn, Y, kind, fac):
    """Bow shop window: a 6-facet curve in front of the shopfront, glass painted with the goods (lit from inside), stallriser,
    mullions, a transom board and a cornice shelf. u0..u1: the window span along the front (as seen from the street)."""
    n = 6; depth = 1.05; zb, zt = 1.35, 4.15; M_w = M['shopwin'][kind]
    pts = []
    for i in range(n + 1):
        t = i / n; u = u0 + (u1 - u0) * t; d = depth * (1 - (2 * t - 1) ** 2) ** 0.7 if 0 < i < n else 0.0
        d = depth * math.sin(math.pi * t) ** 0.6 if 0 < i < n else 0.0
        pts.append((Y(u), xf + dirn * (0.1 + d)))
    for i in range(n):
        (ya, xa), (yb, xb) = pts[i], pts[i + 1]
        mat = M_w
        R.glass.oface([(xa, ya, zb), (xb, yb, zb), (xb, yb, zt), (xa, ya, zt)], mat, [(i / n, 0), ((i + 1) / n, 0), ((i + 1) / n, 1), (i / n, 1)], (dirn, 0, 0))
        # stallriser (painted board) and transom board, flat sides
        R.trim.oface([(xa, ya, 0.0), (xb, yb, 0.0), (xb, yb, zb), (xa, ya, zb)], M['wood_d'], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
        R.trim.oface([(xa, ya, zt), (xb, yb, zt), (xb, yb, 4.55), (xa, ya, 4.55)], M['wood_d'], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
    for i in range(n + 1):
        ya, xa = pts[i]; R.trim.box((xa - 0.07, ya - 0.07, 0.0), (xa + 0.07, ya + 0.07, 4.55), M['cream_w'])
    # window shelf / sill (counter) and top cornice shelf
    for i in range(n):
        (ya, xa), (yb, xb) = pts[i], pts[i + 1]
        R.trim.oface([(xa, ya, zb - 0.0), (xb, yb, zb), (xb + dirn * 0.12, yb, zb), (xa + dirn * 0.12, ya, zb)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
        R.trim.oface([(xa, ya, 4.55), (xb, yb, 4.55), (xb + dirn * 0.2, yb, 4.55), (xa + dirn * 0.2, ya, 4.55)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1))
        R.trim.oface([(xa, ya, zt), (xb, yb, zt), (xb, yb, zt - 0.0), (xa, ya, zt)], M['cream_w'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, 0, 1)) if False else None
    # a window lamp glow: warm light spilling out onto the pavement (real light, small)
    ym = (pts[n // 2][0]); xm = pts[n // 2][1] + dirn * 1.2
    STATE.setdefault('shop_lights', []).append((Vector((xm, ym, 2.6)), kind))

def _sign(R, M, s, y_wall, xf, dirn, kind, rs):
    """Iron bracket from the wall with a scroll ring, two short chains, a board hanging on them: a picture, no letters."""
    arm = 2.7; z = 6.3; y = y_wall; mat = M['sign'][kind]
    R.iron.frustum(Vector((xf + dirn * 0.1, y, z)), Vector((xf + dirn * (0.1 + arm), y, z)), 0.055, 0.055, M['iron'], seg=5)
    R.iron.frustum(Vector((xf + dirn * 0.1, y, z - 1.1)), Vector((xf + dirn * (0.1 + arm * 0.85), y, z - 0.05)), 0.04, 0.04, M['iron'], seg=4)
    # scroll: a ring under the arm
    for i in range(10):
        a0, a1 = 2 * math.pi * i / 10, 2 * math.pi * (i + 1) / 10; r0 = 0.45
        c = Vector((xf + dirn * (0.1 + arm * 0.45), y, z - 0.55))
        R.iron.frustum(c + Vector((dirn * r0 * math.cos(a0), 0, r0 * math.sin(a0))), c + Vector((dirn * r0 * math.cos(a1), 0, r0 * math.sin(a1))), 0.03, 0.03, M['iron'], seg=4, cap0=False, cap1=False)
    # board: its broad faces look along the street (normal +-y), hangs 0.6 below the arm; width 2.0 (into the street), height 2.4
    xb0 = xf + dirn * (0.55); xb1 = xf + dirn * (0.55 + 2.0); xa, xb = min(xb0, xb1), max(xb0, xb1); zt = z - 0.55; zb = zt - 2.4
    ym0, ym1 = y - 0.07, y + 0.07
    R.sign.box((xa, ym0, zb), (xb, ym1, zt), M['wood_d'], mats=dict(front=mat, back=mat))
    # the board is built with box(): front face (-y) uses UV 0..1 along +x. Mirror for the left row so the picture is not reversed on the viewer's side
    for xe in (xa + 0.25, xb - 0.25): R.iron.frustum(Vector((xe, y, zt)), Vector((xe, y, z)), 0.025, 0.025, M['iron'], seg=3)

def _awning(R, M, s, Y, xf, dirn, mat, u0, u1):
    """Striped canvas awning over the bow window: slopes from the fascia down toward the street, side triangles."""
    ya, yb = Y(u0 - 0.2), Y(u1 + 0.2); zt0, zt1 = 4.65, 3.95; d = 2.4
    xa = xf + dirn * 0.3; xb = xf + dirn * (0.3 + d)
    R.awn.oface([(xa, ya, zt0), (xa, yb, zt0), (xb, yb, zt1), (xb, ya, zt1)], M[mat], [(0, 0), (1, 0), (1, 1), (0, 1)], (dirn * 0.5, 0, 1))
    R.awn.oface([(xb, ya, zt1), (xb, yb, zt1), (xb, yb, zt1 - 0.45), (xb, ya, zt1 - 0.45)], M[mat], [(0, 0), (1, 0), (1, 0.4), (0, 0.4)], (dirn, 0, 0))
    for yy in (ya, yb):
        R.awn.face([Vector((xa, yy, zt0)), Vector((xb, yy, zt1)), Vector((xb, yy, zt1 - 0.0))], M[mat])
    for yy in (ya, yb): R.iron.frustum(Vector((xa, yy, zt0 - 0.1)), Vector((xb, yy, zt1 - 0.1)), 0.04, 0.04, M['iron'], seg=4)

def _roof(R, M, s, y0, xf, dirn, ph, rs, lot_i):
    """Slate roof behind the parapet (two pitches, ridge parallel to the street) and two chimney stacks with pots."""
    depth = 11.5; ridge_h = 4.6; zt = 19.9 + ph
    xa = xf - dirn * 0.5; xr = xf - dirn * (0.5 + depth / 2); xb = xf - dirn * (0.5 + depth)
    ya, yb = y0, y0 + LOT
    R.roof.oface([(xa, ya, zt - 0.3), (xa, yb, zt - 0.3), (xr, yb, zt + ridge_h), (xr, ya, zt + ridge_h)], M['slate'], [(0, 0), (LOT / 4, 0), (LOT / 4, 1.3), (0, 1.3)], (-dirn * 0.6, 0, 1))
    R.roof.oface([(xr, ya, zt + ridge_h), (xr, yb, zt + ridge_h), (xb, yb, zt - 0.3), (xb, ya, zt - 0.3)], M['slate'], [(0, 0), (LOT / 4, 0), (LOT / 4, 1.3), (0, 1.3)], (dirn * 0.6, 0, 1))
    # gable ends: simple dark brick triangles on the party walls (seen from the high camera)
    for yy, nn in ((ya, (0, -1, 0)), (yb, (0, 1, 0))):
        R.brk.oface([(xa, yy, zt - 0.3), (xb, yy, zt - 0.3), (xr, yy, zt + ridge_h)], M['brick_b'], [(0, 0), (3, 0), (1.5, 1.3)], nn)
    # chimneys on the ridge line near the party walls
    for (yy, k) in ((ya + 0.7, 0), (yb - 0.7, 1)):
        if rs.random() < 0.15: continue
        hh = rs.uniform(3.0, 4.2); c0 = Vector((xr + dirn * rs.uniform(-0.8, 0.8), yy, zt + ridge_h - 0.4)); w = 0.85
        R.brk.box((c0.x - w / 2, c0.y - w / 2, c0.z), (c0.x + w / 2, c0.y + w / 2, c0.z + hh), M['brick_b' if k else 'brick_a'], tile=(4, 4))
        R.trim.box((c0.x - w / 2 - 0.1, c0.y - w / 2 - 0.1, c0.z + hh), (c0.x + w / 2 + 0.1, c0.y + w / 2 + 0.1, c0.z + hh + 0.18), M['stone'])
        for dxp in (-0.2, 0.2):
            R.misc.frustum(Vector((c0.x + dxp * 0.0, c0.y + dxp, c0.z + hh + 0.18)), Vector((c0.x, c0.y + dxp, c0.z + hh + 0.18 + 0.95)), 0.2, 0.15, M['pot'], seg=8)

def _row_finish(SET, R, side):
    out = []
    for nm, mb in (('fac', R.fac), ('trim', R.trim), ('roof', R.roof), ('brk', R.brk), ('iron', R.iron), ('misc', R.misc), ('glass', R.glass), ('awn', R.awn), ('sign', R.sign)):
        if mb.f:
            o = _obj(mb, 'row%+d_%s' % (side, nm), SET); out.append(o)
    return out

def _lane_walls(SET, M, rs):
    """Side walls of the two houses flanking the cross lane on the left, and the backdrop houses beyond (sunlit through the lane)."""
    mb = MB(); y_a, y_b = LANE
    for (yy, nn) in ((y_a, (0, 1, 0)), (y_b, (0, -1, 0))):
        qface(mb, (-X0, yy, 0), (-12.0, 0, 0), (0, 0, H_FAC + 1.2), M['brick_a'], (0, 0, 3, 5), nn)
    # lane end wall + a backdrop house front
    qface(mb, (-24.0, y_a, 0), (0, y_b - y_a, 0), (0, 0, 22), M['brick_b'], (0, 0, 2, 5), (1, 0, 0))
    _obj(mb, 'lane_walls', SET)
    # lane: a hanging lantern across and a barrel
    return

def _end_block(SET, M):
    """A terrace closing the far end of the street (y = Y0 + 22 lots): seven fronts across, cornice, parapet, slate roof and chimneys."""
    ye = Y0 + 22 * LOT + 0.4; fb = MB(); tb = MB(); rb = MB(); kb = MB(); rs = _rnd(31)
    for k, fac in enumerate(('fac_c', 'fac_a', 'fac_e', 'fac_s3', 'fac_b', 'fac_f', 'fac_d', 'fac_a', 'fac_c')):
        x0 = -36.0 + k * LOT
        qface(fb, (x0, ye, 0), (LOT, 0, 0), (0, 0, H_FAC), M[fac], (0, 0, 1, H_FAC / ST.FACADE_H), (0, -1, 0))
        tb.box((x0, ye - 0.95, 19.35), (x0 + LOT, ye, 19.62), M['cream']); tb.box((x0, ye - 0.7, 19.62), (x0 + LOT, ye, 19.9), M['cream_w'])
        tb.box((x0, ye - 0.16, 5.45), (x0 + LOT, ye, 5.85), M['cream'])
        kb.box((x0, ye, 19.9), (x0 + LOT, ye + 0.55, 20.9), M['brick_a' if k % 2 else 'brick_b'], tile=(4, 4))
        qface(rb, (x0, ye + 0.5, 19.6), (LOT, 0, 0), (0, 11.5 / 2, 4.6 + 0.3), M['slate'], (0, 0, LOT / 4, 1.3), (0, -0.6, 1))
        for xx in (x0 + 0.7, x0 + LOT - 0.7):
            kb.box((xx - 0.45, ye + 4.0, 22.0), (xx + 0.45, ye + 4.9, 25.2), M['brick_b']); tb.frustum(Vector((xx, ye + 4.45, 25.2)), Vector((xx, ye + 4.45, 26.1)), 0.2, 0.15, M['pot'], seg=8)
    for nm, mb in (('end_fac', fb), ('end_trim', tb), ('end_roof', rb), ('end_brick', kb)): _obj(mb, nm, SET)


def _balcony(R, M, Y, xf, dirn, u0, u1, z):
    """Wrought-iron balcony across the first-floor windows: slab, front and side rails with spear-top bars, scroll panels."""
    d = 0.75; ya, yb = sorted((Y(u0), Y(u1))); xa, xb = sorted((xf + dirn * 0.1, xf + dirn * (0.1 + d)))
    R.trim.box((xa, ya, z - 0.2), (xb, yb, z), M['stone'])
    xr = xf + dirn * (0.1 + d - 0.05); n = int((yb - ya) / 0.38)
    for i in range(n + 1):
        y = ya + (yb - ya) * i / n; R.iron.frustum(Vector((xr, y, z)), Vector((xr, y, z + 1.0)), 0.03, 0.03, M['iron'], seg=4, cap0=False, cap1=False)
        R.iron.frustum(Vector((xr, y, z + 1.0)), Vector((xr, y, z + 1.16)), 0.06, 0.0, M['iron'], seg=4, cap0=True, cap1=False)
    for zr in (z + 0.12, z + 0.55, z + 1.02): R.iron.frustum(Vector((xr, ya, zr)), Vector((xr, yb, zr)), 0.03, 0.03, M['iron'], seg=4)
    for y in (ya, yb):
        R.iron.frustum(Vector((xf + dirn * 0.1, y, z + 1.02)), Vector((xr, y, z + 1.02)), 0.03, 0.03, M['iron'], seg=4); R.iron.frustum(Vector((xr, y, z)), Vector((xr, y, z + 1.1)), 0.06, 0.06, M['iron'], seg=5)
    for i in range(n):                                      # small scroll rings between the bars
        y = ya + (yb - ya) * (i + 0.5) / n; c = Vector((xr, y, z + 0.4))
        for k in range(8):
            a0, a1 = 2 * math.pi * k / 8, 2 * math.pi * (k + 1) / 8
            R.iron.frustum(c + Vector((0, 0.13 * math.cos(a0), 0.13 * math.sin(a0))), c + Vector((0, 0.13 * math.cos(a1), 0.13 * math.sin(a1))), 0.018, 0.018, M['iron'], seg=3, cap0=False, cap1=False)

# ----------------------------------------------------------------------------- street furniture
# ----------------------------------------------------------------------------- street furniture
def _lamp_post(R, M, x, y, h=7.8, side=1):
    """Cast-iron oil lamp: fluted post on a plinth, a glass lantern with a cap and a finial, a scrolled bracket arm, a ladder bar."""
    I = M['iron']; mb = R['iron']; gl = R['glass']
    mb.frustum(Vector((x, y, ZP)), Vector((x, y, ZP + 0.7)), 0.38, 0.32, I, seg=8); mb.frustum(Vector((x, y, ZP + 0.7)), Vector((x, y, h - 1.2)), 0.2, 0.13, I, seg=8)
    mb.frustum(Vector((x, y, ZP + 0.7)), Vector((x, y, ZP + 0.95)), 0.3, 0.3, I, seg=8); mb.frustum(Vector((x, y, h - 1.2)), Vector((x, y, h - 1.0)), 0.25, 0.25, I, seg=8)
    mb.box((x - 0.55, y - 0.04, h - 2.6), (x + 0.55, y + 0.04, h - 2.52), I) if False else None
    mb.frustum(Vector((x - 0.45, y, h - 2.4)), Vector((x + 0.45, y, h - 2.4)), 0.04, 0.04, I, seg=4)          # ladder bar
    # lantern
    gl.frustum(Vector((x, y, h - 1.0)), Vector((x, y, h + 0.35)), 0.42, 0.5, M['glass_lamp'], seg=8, cap0=False, cap1=False)
    for k in range(8):
        a = 2 * math.pi * k / 8; mb.frustum(Vector((x + 0.43 * math.cos(a), y + 0.43 * math.sin(a), h - 1.0)), Vector((x + 0.5 * math.cos(a), y + 0.5 * math.sin(a), h + 0.35)), 0.025, 0.025, I, seg=3)
    mb.frustum(Vector((x, y, h + 0.35)), Vector((x, y, h + 0.8)), 0.62, 0.12, I, seg=8); mb.frustum(Vector((x, y, h + 0.8)), Vector((x, y, h + 1.1)), 0.06, 0.02, I, seg=4)
    mb.frustum(Vector((x, y, h - 1.0)), Vector((x, y, h - 1.12)), 0.5, 0.3, I, seg=8)
    return Vector((x, y, h - 0.35))

def _barrel(mb, M, c, r=0.7, h=1.7, lying=False, yaw=0.0):
    c = Vector(c); seg = 12
    if not lying:
        mb.frustum(c, c + Vector((0, 0, h * 0.5)), r * 0.82, r, M['barrel'], seg=seg, cap0=True, cap1=False, uv_wrap=(1.0, 1.0))
        mb.frustum(c + Vector((0, 0, h * 0.5)), c + Vector((0, 0, h)), r, r * 0.82, M['barrel'], seg=seg, cap0=False, cap1=True, uv_wrap=(1.0, 1.0))
    else:
        a = Vector((math.cos(yaw), math.sin(yaw), 0)); mb.frustum(c - a * h / 2, c, r * 0.82, r, M['barrel'], seg=seg, uv_wrap=(1.0, 1.0)); mb.frustum(c, c + a * h / 2, r, r * 0.82, M['barrel'], seg=seg, uv_wrap=(1.0, 1.0))

def _crate(mb, M, c, sx=1.2, sy=1.2, sz=1.0, yaw=0.0, mat='wood'):
    obox(mb, Vector(c) + Vector((0, 0, sz / 2)), Vector((math.cos(yaw), math.sin(yaw), 0)), Vector((-math.sin(yaw), math.cos(yaw), 0)), Vector((0, 0, 1)), sx / 2, sy / 2, sz / 2, M[mat], uvk=0.5)

def _barrow(mb, M, c, yaw, rs):
    """Market barrow: a wooden tray on two shafts and one big wheel, heaped with cabbages, turnips, carrots, apples, onions."""
    c = Vector(c); f = Vector((math.cos(yaw), math.sin(yaw), 0)); sd = Vector((-math.sin(yaw), math.cos(yaw), 0)); up = Vector((0, 0, 1))
    obox(mb, c + up * 1.15, f, sd, up, 1.5, 0.95, 0.16, M['wood'], uvk=0.5)                              # floor
    for sgn in (-1, 1):
        obox(mb, c + up * 1.55 + sd * sgn * 0.95, f, sd, up, 1.5, 0.07, 0.36, M['wood_d'], uvk=0.5)         # sides
        beam(mb, c + up * 1.0 + sd * sgn * 0.6 - f * 3.1, c + up * 1.1 + sd * sgn * 0.6 + f * 1.5, 0.12, 0.12, M['wood_d'])  # shafts
    obox(mb, c + up * 1.55 - f * 1.5, f, sd, up, 0.07, 0.95, 0.36, M['wood_d'], uvk=0.5); obox(mb, c + up * 1.7 + f * 1.5, f, sd, up, 0.07, 0.95, 0.5, M['wood_d'], uvk=0.5)
    for sgn in (-1, 1):                                                                                  # legs and the wheel
        rod(mb, c + sd * sgn * 0.7 - f * 1.2 + up * 1.0, c + sd * sgn * 0.7 - f * 1.2, 0.07, M['wood_d'])
    wc = c + f * 1.55 + up * 0.62
    for sgn in (-0.3, 0.3):
        mb.frustum(wc + sd * sgn - sd * 0.04, wc + sd * sgn + sd * 0.04, 0.62, 0.62, M['wheel'], seg=14)
    rod(mb, wc - sd * 0.5, wc + sd * 0.5, 0.06, M['iron_b'])
    # produce: heaps (lumpy spheres)
    kinds = [('cabbage', 0.34), ('turnip', 0.24), ('carrot', 0.14), ('apple', 0.2), ('onion', 0.2)]
    for i in range(46):
        u = rs.uniform(-1.3, 1.3); v = rs.uniform(-0.8, 0.8); kind, r = kinds[(i // 6) % len(kinds)] if rs.random() < 0.7 else kinds[rs.randrange(len(kinds))]
        pos = c + f * u + sd * v + up * (1.3 + r * 0.8 + 0.28 * (1 - (abs(u) / 1.5) ** 2) * (1 - (abs(v) / 0.95) ** 2) * 1.6)
        if kind == 'carrot':
            d = (f * rs.uniform(-1, 1) + sd * rs.uniform(-1, 1)).normalized(); rod(mb, pos - d * 0.4 + up * 0.1, pos + d * 0.4, 0.07, M['carrot'], seg=5, r1=0.025)
        else:
            lumpy(mb, pos, r, M[kind], rs.randint(1, 999), seg=8, rings=5, rough=0.12)
            if kind == 'turnip': mb.sphere(pos + up * r * 0.7, r * 0.5, M['turnip_top'], seg=6, rings=4)


def _umbrella(mb, M, top, **kw): PT.umbrella(mb, M, top, **kw)

def _market(SET, M):
    """Market corner on the left pavement (y 2..16): a stall with a striped awning on two poles, a trestle table heaped with produce, two barrows, baskets, sacks, crates."""
    mb = MB(); rs = _rnd(13); cx, cy = -8.15, 14.6
    X = Vector((1, 0, 0)); Y = Vector((0, 1, 0)); Zv = Vector((0, 0, 1))
    obox(mb, Vector((cx, cy, ZP + 1.5)), X, Y, Zv, 0.85, 1.9, 0.1, M['wood'], uvk=0.5)                          # table top
    for sx in (-0.7, 0.7):
        for sy in (-1.6, 1.6): rod(mb, Vector((cx + sx, cy + sy, ZP)), Vector((cx + sx, cy + sy, ZP + 1.5)), 0.08, M['wood_d'], seg=5)
    obox(mb, Vector((cx + 0.6, cy, ZP + 0.6)), X, Y, Zv, 0.07, 1.6, 0.4, M['wood_d'], uvk=0.5)                    # front board
    kinds = [('cabbage', 0.34), ('apple', 0.2), ('onion', 0.2), ('turnip', 0.24), ('carrot', 0.14)]
    for i in range(50):
        u = rs.uniform(-0.65, 0.65); v = rs.uniform(-1.7, 1.7); kind, r = kinds[(int((v + 1.8) / 0.75)) % 5]
        pos = Vector((cx + u, cy + v, ZP + 1.6 + r * 0.8 + 0.08))
        if kind == 'carrot':
            d = (X * rs.uniform(-1, 1) + Y * rs.uniform(-1, 1)).normalized(); rod(mb, pos - d * 0.4 + Zv * 0.05, pos + d * 0.4, 0.07, M['carrot'], seg=5, r1=0.025)
        else: lumpy(mb, pos, r, M[kind], rs.randint(1, 999), seg=8, rings=5, rough=0.12)
    # awning poles and slanted striped canvas
    for sy in (-2.0, 2.0): rod(mb, Vector((cx - 0.9, cy + sy, ZP)), Vector((cx - 0.9, cy + sy, ZP + 5.6)), 0.09, M['wood_d'], seg=5); rod(mb, Vector((cx + 1.35, cy + sy, ZP)), Vector((cx + 1.35, cy + sy, ZP + 4.5)), 0.09, M['wood_d'], seg=5)
    aw = MB()
    aw.oface([Vector((cx - 1.0, cy - 2.2, ZP + 5.7)), Vector((cx - 1.0, cy + 2.2, ZP + 5.7)), Vector((cx + 1.6, cy + 2.2, ZP + 4.6)), Vector((cx + 1.6, cy - 2.2, ZP + 4.6))], M['awn_a'],
             [(0, 0), (1, 0), (1, 1), (0, 1)], (0.4, 0, 1))
    aw.oface([Vector((cx + 1.6, cy - 2.2, ZP + 4.6)), Vector((cx + 1.6, cy + 2.2, ZP + 4.6)), Vector((cx + 1.6, cy + 2.2, ZP + 4.15)), Vector((cx + 1.6, cy - 2.2, ZP + 4.15))], M['awn_a'], [(0, 0), (1, 0), (1, 0.3), (0, 0.3)], (1, 0, 0))
    _obj(aw, 'stall_awning', SET)
    # baskets and sacks and crates around
    for (bx, by) in ((-7.4, 8.8), (-8.9, 9.6), (-7.0, 17.6)):
        mb.frustum(Vector((bx, by, ZP)), Vector((bx, by, ZP + 0.8)), 0.42, 0.55, M['wood'], seg=10, cap1=False)
        for k in range(6): lumpy(mb, Vector((bx + rs.uniform(-0.2, 0.2), by + rs.uniform(-0.2, 0.2), ZP + 0.85)), 0.22, M[['cabbage', 'apple', 'onion'][k % 3]], rs.randint(1, 99), seg=7, rings=4)
    for (bx, by) in ((-9.0, 17.9), (-8.6, 6.4)):
        lumpy(mb, Vector((bx, by, ZP + 0.45)), 0.62, M['sack'], rs.randint(1, 99), seg=9, rings=6, rough=0.12, squash=0.85)
    _barrow(mb, M, Vector((-8.1, 6.5, ZP)), math.radians(100), _rnd(4))
    _obj(mb, 'market', SET)

def _rank_props(SET, M):
    """Rank furniture between the coaches: a stone water trough with a bucket, hay bags, a ranking post with a lantern."""
    mb = MB(); X = Vector((1, 0, 0)); Y = Vector((0, 1, 0)); Zv = Vector((0, 0, 1))
    for yc in (RANK_Y[0] + 5.0, RANK_Y[1] + 5.0, RANK_Y[2] + 5.0):
        x = 5.0; yt = yc - 0.4
        obox(mb, Vector((x, yt, 0.5)), X, Y, Zv, 0.55, 1.2, 0.5, M['stone_d'], uvk=0.5); obox(mb, Vector((x, yt, 1.02)), X, Y, Zv, 0.62, 1.28, 0.06, M['stone'], uvk=0.5)
        mb.frustum(Vector((x - 0.35, yt + 0.3, 1.08)), Vector((x - 0.35, yt + 0.3, 1.5)), 0.22, 0.26, M['wood'], seg=8, cap1=False)
        lumpy(mb, Vector((x + 0.2, yt - 1.7, 0.45)), 0.5, M['sack'], int(yc), seg=8, rings=5, rough=0.12, squash=0.9)
    _obj(mb, 'rank_props', SET)

# ----------------------------------------------------------------------------- the animation controller and driver helpers
def _ctrl():
    ob = bpy.data.objects.get('CTRL')
    if ob is None:
        ob = bpy.data.objects.new('CTRL', None); bpy.context.scene.collection.objects.link(ob)
        for k in ('umb', 'rush', 'busy', 'pink', 'rain', 'mud'): ob[k] = 0.0
        ob['rain'] = 1.0; ob['busy'] = 1.0
    return ob

def _drv(target, path, expr, vars_, index=-1):
    """Scripted driver on target (object / node tree / data-block) path, vars_ = {name: (id, data_path)}."""
    fc = target.driver_add(path, index) if index >= 0 else target.driver_add(path)
    d = fc.driver; d.type = 'SCRIPTED'; d.expression = expr
    for nm, (idb, dp) in vars_.items():
        v = d.variables.new(); v.name = nm; v.type = 'SINGLE_PROP'; v.targets[0].id = idb; v.targets[0].data_path = dp
    return fc

def _pop_scale(ob, ctrl, prop, thr, w=0.05, floor=0.001):
    """Scale 0 -> 1 pop when ctrl[prop] passes thr (width w); z leads a little (springy)."""
    s = 'min(1,max(0,(k-%g)/%g))' % (thr, w)
    for i, e in enumerate(('max(%g,%s)' % (floor, s), 'max(%g,%s)' % (floor, s), 'max(%g,min(1,1.5*%s))' % (floor, s))):
        _drv(ob, 'scale', e, {'k': (ctrl, '["%s"]' % prop)}, i)

def _parent(ob, par):
    ob.parent = par; ob.matrix_parent_inverse = Matrix.Identity(4)

def _empty(name, loc, rot_z=0.0, coll=None):
    ob = bpy.data.objects.new(name, None); (coll or STATE['SET']).objects.link(ob); ob.location = loc; ob.rotation_euler = (0, 0, math.radians(rot_z)); ob.empty_display_size = 1.0
    return ob

# ----------------------------------------------------------------------------- coaches
COACH_SPEC = [('green', 'horse', 'up', False), ('oxblood', 'horse_b', 'down', True), ('navy', 'horse_c', 'up', False), ('ochre', 'horse_k', 'down', True), ('green', 'horse_b', 'up', False)]

def _wheel_obj(SET, M, name, root, loc, R_, w, y0):
    mb = MB(); PT.wheel(mb, M, Vector((0, 0, 0)), (1, 0, 0), R_, w=w); ob = _obj(mb, name, SET); ob.location = loc; _parent(ob, root)
    ctrl = _ctrl(); _drv(ob, 'rotation_euler', '(ry-%g)/%g' % (y0, R_), {'ry': (root, 'location[1]')}, 0)
    return ob

def _coach(SET, M, i, loc_xy, yaw=180.0, name=None):
    """One hackney coach with its horse as a rig: empty `coach_i` (move / rotate it to drive the coach) with children body, glass (windows lit), passengers,
    lanterns (lit), 4 wheels (they roll with the empty's y travel by drivers), horse (bobs with travel). Returns the data dict."""
    style, coat, head, trunk = COACH_SPEC[i]; name = name or 'coach_%d' % i; ctrl = _ctrl(); pre = STATE['pre']; rs = _rnd(40 + i)
    root = _empty(name, (loc_xy[0], loc_xy[1], 0.0), yaw)
    mb = MB(); anc = PT.coach_body(mb, M, style, trunk); body = _obj(mb, name + '_body', SET); _parent(body, root)
    win = mat_emit(pre + 'e_cwin%d' % i, image=STATE['tx']['coach_win'], strength=1.5)
    gb = MB(); panes = PT.coach_glass(gb, win); glass = _obj(gb, name + '_glass', SET); _parent(glass, root)
    lam = mat_emit(pre + 'e_clamp%d' % i, '#ffc070', strength=3.4)
    lb = MB()
    for sg in (-1, 1):
        c = Vector((sg * (PT.HW + 0.1), 4.3, 4.8)); lb.frustum(c - Vector((0, 0, 0.35)), c + Vector((0, 0, 0.35)), 0.26, 0.3, lam, seg=6, cap0=False, cap1=False)
        lb.frustum(c + Vector((0, 0, 0.35)), c + Vector((0, 0, 0.62)), 0.34, 0.06, M['iron_b'], seg=6); lb.frustum(c - Vector((0, 0, 0.35)), c - Vector((0, 0, 0.45)), 0.3, 0.2, M['iron_b'], seg=6)
        beam(lb, c + Vector((-sg * 0.12, 0, -0.45)), c + Vector((-sg * 0.12, 0, -1.0)), 0.1, 0.1, M['iron_b'])
    lamps = _obj(lb, name + '_lamps', SET); _parent(lamps, root)
    thr = i / 4.0                                               # coach i is full when busy > i/4 (busy 0 = all empty, 1 = all full)
    for nm, mat, lo in ((win, win, 0.28), (lam, lam, 0.0)):    # windows dim, lanterns out when the coach is empty
        for sock in mat.node_tree.nodes:
            if sock.name == 'strength':
                base = sock.inputs['Strength'].default_value
                _drv(mat.node_tree, 'nodes["strength"].inputs[1].default_value', '%g*(%g+%g*min(1,max(0,(k-%g)/0.05)))' % (base, lo / base if base else 0, 1 - (lo / base if base else 0), thr), {'k': (ctrl, '["busy"]')})
    # passengers: dark head-and-shoulders in the panes (not in the pane at the front, one per door window; two in the door window)
    pb = MB()
    for j, (sg, y, z, wd) in enumerate(panes):
        if (j % 3) == 0: continue
        n = 2 if (j % 3) == 1 else 1
        for q in range(n): PT.passenger(pb, M, sg, y + (q - (n - 1) / 2) * 0.62, z, hat=((i + j + q) % 2 == 0))
    pas = _obj(pb, name + '_pass', SET); _parent(pas, root); _pop_scale(pas, ctrl, 'busy', thr, 0.05)
    pas.location = Vector((0, 0, 0))
    wheels = [_wheel_obj(SET, M, name + '_w_rl', root, (-2.0, -1.3, 2.3), 2.3, 0.32, loc_xy[1]), _wheel_obj(SET, M, name + '_w_rr', root, (2.0, -1.3, 2.3), 2.3, 0.32, loc_xy[1]),
              _wheel_obj(SET, M, name + '_w_fl', root, (-1.9, 2.3, 1.5), 1.5, 0.3, loc_xy[1]), _wheel_obj(SET, M, name + '_w_fr', root, (1.9, 2.3, 1.5), 1.5, 0.3, loc_xy[1])]
    hb = MB(); hinfo = PT.horse(hb, M, Vector((0, 0, 0)), coat=coat, mane='horse_d' if coat != 'horse_c' else 'horse_dk', head=head, blaze=(i % 2 == 0)); horse = _obj(hb, name + '_horse', SET)
    horse.location = (0, 5.6, 0); _parent(horse, root); _drv(horse, 'location', '0.1*abs(sin((ry-%g)*0.9))' % loc_xy[1], {'ry': (root, 'location[1]')}, 2)
    # reins: from the bit back to the box (thin dark rods), parented to the root
    rb = MB(); bit = Vector((0, 5.6, 0)) + Vector((0, hinfo['bit'].y, hinfo['bit'].z)); hand = Vector((0.0, 3.5, 5.3))
    for sg in (-1, 1): rod(rb, bit + Vector((sg * 0.18, 0, 0)), hand + Vector((sg * 0.25, 0, 0)), 0.025, M['leather'], seg=3)
    reins = _obj(rb, name + '_reins', SET); _parent(reins, root)
    ang = math.radians(yaw); rot = lambda v: Vector((v.x * math.cos(ang) - v.y * math.sin(ang), v.x * math.sin(ang) + v.y * math.cos(ang), v.z))
    base = Vector((loc_xy[0], loc_xy[1], 0.0))
    d = dict(i=i, name=name, root=root, body=body, glass=glass, lamps=lamps, pass_=pas, wheels=wheels, horse=horse, win_mat=win, lamp_mat=lam, thr=thr, y0=loc_xy[1],
             box=base + rot(Vector((0, 3.4, BOX_Z))), lamp_pts=[base + rot(Vector((sg * (PT.HW + 0.1), 4.3, 4.8))) for sg in (-1, 1)],
             door_street=base + rot(Vector((-PT.HW, 0.0, 0.0))), door_kerb=base + rot(Vector((PT.HW, 0.0, 0.0))), horse_head=base + rot(Vector((0, 5.6 + hinfo['nose'].y, hinfo['nose'].z))))
    return d

# ----------------------------------------------------------------------------- crowd slots (umbrellas, rush)
def _umb_slots():
    rs = _rnd(21); slots = []
    cols = ['umb_dark'] * 5 + ['umb_brown', 'umb_green', 'umb_blue', 'umb_red', 'umb_ochre', 'umb_grey']
    keep = [(c['loc'][0], c['loc'][1], 2.4) for c in CAMS.values()] + [(c['loc_b'][0], c['loc_b'][1], 2.4) for c in CAMS.values()] + [(s['pos'][0], s['pos'][1], 1.6) for s in STAND.values()]
    def add(x, y, z, thr):
        if any((x - a) ** 2 + (y - b) ** 2 < r * r for a, b, r in keep): return
        look = (rs.uniform(-0.6, 0.6), -1.0); slots.append(dict(i=len(slots), pos=(x, y, z), look=look, thr=min(0.96, thr), mat=cols[rs.randrange(len(cols))], r=rs.uniform(1.8, 2.3)))
    for s in (-1, 1):
        for j, y in enumerate(np.arange(-10.0, 76.0, 3.7)):
            x = s * (7.0 if j % 2 == 0 else 8.7); y = float(y) + rs.uniform(-0.5, 0.5)
            add(x, y, ZP, 0.03 + 0.55 * abs(y - 12.0) / 70.0 + rs.uniform(0, 0.08))
    pts = []                                                     # the roadway fills later: Poisson-disc, min 3.3 apart, rank side (x > 1.4, y > 8) left to the coaches
    for _ in range(900):
        x = rs.uniform(-5.0, 4.6); y = rs.uniform(-8.0, 76.0)
        if x > 1.4 and y > 8.0: continue
        if all((x - a) ** 2 + (y - b) ** 2 > 3.3 ** 2 for a, b in pts): pts.append((x, y))
    for (x, y) in pts: add(x, y, 0.0, 0.42 + 0.5 * abs(y - 12.0) / 70.0 + rs.uniform(0, 0.08))
    return slots

def _rush_slots():
    rs = _rnd(22); out = []
    for ci, yc in enumerate(RANK_Y):
        ring = [(0.9, yc - 1.8), (0.55, yc - 0.3), (1.15, yc + 1.2), (-0.1, yc - 2.6), (-0.35, yc + 0.5), (-0.45, yc + 2.2)]
        for j, (x1, y1) in enumerate(ring):
            p0 = (-5.2 + 0.5 * (j % 3), yc - 12.0 + 3.2 * j + rs.uniform(-1, 1)); d = 0.04 * j + 0.05 * ci
            out.append(dict(name='rush_%d_%d' % (ci, j), coach=ci, p0=p0 + (0.0,), p1=(x1, y1, 0.0), look=(0.95, 0.1), delay=d))
    return out

# ----------------------------------------------------------------------------- sky
def _sky(SET, M, R=900.0):
    mb = MB(); seg = 96; nk = 20; els = [-15 + 105 * k / nk for k in range(nk + 1)]
    for i in range(seg):
        for k in range(nk):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], M['sky'], [(i / seg, k / nk), ((i + 1) / seg, k / nk), ((i + 1) / seg, (k + 1) / nk), (i / seg, (k + 1) / nk)][::-1])
    o = _obj(mb, 'sky', SET, shadow=False); STATE['sky_obj'] = o; o.visible_glossy = True

# ----------------------------------------------------------------------------- camera-dependent things: rain (parented to the camera), halos, drips, lights
def _camera_basis(cam):
    m = cam.matrix_world.to_quaternion(); fwd = m @ Vector((0, 0, -1)); right = m @ Vector((1, 0, 0)); up = m @ Vector((0, 1, 0))
    return cam.matrix_world.translation.copy(), fwd, right, up

RAIN_BANDS = [(2.5, 4.5, 70), (4.5, 8.0, 110), (8.0, 14.0, 160), (14.0, 25.0, 190), (25.0, 48.0, 170)]       # (near, far, visible streaks at intensity 1)
RAIN_SPEED = 0.9                                                                                                 # world units per frame

def _rain(coll, M, cam):
    """Crisp rain streaks, ~700 at intensity 1 (the board had 1000). The streaks are camera-local geometry (parent = the camera), 5 depth bands x 4 intensity tiers;
    each band is periodic along the fall direction and its object slides down with `frame` (driver), so rain moves in animation and keeps ~2 px width."""
    ctrl = _ctrl(); rs = _rnd(9); fx = 782.2; th, tv = math.tan(math.radians(24.7)), math.tan(math.radians(39.3))
    Rinv = cam.matrix_world.to_3x3().inverted(); dw = (Vector((0, 0, -1)) + Vector((0.16, 0, 0))).normalized(); dl = (Rinv @ dw).normalized()
    f = Vector((0, 0, -1)); ea = dl.cross(f)
    if ea.length < 1e-3: ea = Vector((1, 0, 0))
    ea.normalize(); out = []
    for bi, (lo, hi, cnt) in enumerate(RAIN_BANDS):
        Vb = 2 * tv * hi * 1.25; frac = min(1.0, (2 * tv * (lo + hi) / 2) / Vb) * 0.85                                  # fraction of the generated streaks that is in view
        ngen = int(cnt / 4 / frac)
        for tier in range(4):
            mb = MB()
            for k in range(ngen):
                d = (lo ** 3 + (hi ** 3 - lo ** 3) * rs.random()) ** (1 / 3); a = rs.uniform(-1.2, 1.2) * th * d * 1.05; b = rs.uniform(-Vb / 2, Vb / 2)
                p = f * d + ea * a + dl * b
                to_cam = (-p).normalized(); side = dl.cross(to_cam)
                if side.length < 1e-3: continue
                side.normalize(); Lpx = rs.uniform(26, 56) if d > 6 else rs.uniform(40, 80); wpx = rs.uniform(1.4, 2.2) if d > 10 else rs.uniform(2.0, 3.0)
                L = Lpx * d / fx; w = wpx * d / fx
                for off in (0.0, -Vb):
                    q = p + dl * off; A_ = q - dl * L / 2; B_ = q + dl * L / 2; s_ = side * (w / 2)
                    mb.face([A_, q + s_ - dl * (L * 0.15), B_, q - s_ - dl * (L * 0.15)], M['rain'])
            o = _obj(mb, 'rain_%d_%d' % (bi, tier), coll, shadow=False); o.visible_diffuse = False; o.visible_glossy = False; o.visible_transmission = False
            _parent(o, cam)
            for ax in range(3): _drv(o, 'location', '%g*fmod(frame*%g,%g)' % (dl[ax], RAIN_SPEED, Vb), {}, ax)
            _drv(o, 'hide_render', 'k <= %g' % (tier / 4.0), {'k': (ctrl, '["rain"]')}); out.append(o)
    return out

def _drips(coll, M):
    """Eave drips: crossed thin ribbons that fall 3 units from the cornice lines and restart (driver on frame): 6 phase groups over both rows."""
    rs = _rnd(77); groups = [MB() for _ in range(6)]
    for s in (-1, 1):
        for y0 in np.arange(Y0, Y1, LOT):
            for k in range(4):
                y = float(y0) + rs.uniform(0.3, LOT - 0.3); x = s * (X0 - 1.0); L = rs.uniform(0.5, 1.1); g = groups[rs.randrange(6)]; zc = 19.2 - L / 2
                for ang in (0.0, math.pi / 2):
                    sd = Vector((math.cos(ang), math.sin(ang), 0)) * 0.035
                    g.face([Vector((x, y, zc + L / 2)) + sd * 0.3, Vector((x, y, zc + L / 2)) - sd * 0.3, Vector((x, y, zc - L / 2)) - sd, Vector((x, y, zc - L / 2)) + sd][::-1], M['drip'])
    out = []
    for i, g in enumerate(groups):
        if g.f:
            o = _obj(g, 'drips_%d' % i, coll, shadow=False); o.visible_glossy = False; _drv(o, 'location', '-fmod(frame*0.45+%g,3.0)' % (i * 0.5), {}, 2); out.append(o)
    return out

def _halo_quad(coll, M, pos, size, mat, ctrl=None, thr=None, cam=None, name='halo'):
    mb = MB(); h = size / 2
    mb.face([Vector((-h, -h, 0)), Vector((h, -h, 0)), Vector((h, h, 0)), Vector((-h, h, 0))], M[mat], [(0, 0), (1, 0), (1, 1), (0, 1)])
    o = _obj(mb, name, coll, shadow=False); o.location = pos; o.visible_glossy = False
    cn = o.constraints.new('COPY_ROTATION'); cn.target = cam
    if ctrl is not None: _pop_scale(o, ctrl, 'busy', thr, 0.05)
    return o

def _shot_extras(cam, preset):
    """Everything that depends on the camera: rain, eave drips, lamp / lantern halos (face the camera by constraint), the warm point lights near the shot."""
    SHOT = STATE['SHOT']; LIG = STATE['LIGHTS']; M = STATE['M']; P = STATE['P']; ctrl = _ctrl()
    cs = CAMS[preset]; mid = (Vector(cs['loc']) + Vector(cs['loc_b'])) / 2; cen = Vector(cs['look_at'])
    _rain(SHOT, M, cam); _drips(SHOT, M)
    lk = P['lamp_k']
    pts = sorted(STATE.get('lamp_pts', []), key=lambda p: (p - mid).length)
    for i, p in enumerate(pts[:7]): _light('lamp_%d' % i, p, (1.0, 0.64, 0.3), 1500.0 * lk, radius=0.35)
    for p in [q for q in pts if (q - mid).length < 140]: _halo_quad(SHOT, M, p, 3.6 * (1 + 0.25 * (lk - 1)), 'halo', cam=cam, name='halo_lamp')
    sl = sorted(STATE.get('shop_lights', []), key=lambda t: (t[0] - mid).length)[:6]
    for i, (p, kind) in enumerate(sl): _light('shop_%d' % i, p, (1.0, 0.66, 0.34), 1000.0 * lk, radius=0.5)
    for cd in STATE['coach_data'][:4]:
        for j, lp in enumerate(cd['lamp_pts']):
            if (lp - mid).length < 60 or (lp - cen).length < 40:
                lt = _light('clamp_%d_%d' % (cd['i'], j), lp, (1.0, 0.62, 0.28), 380.0 * lk, radius=0.2)
                _drv(lt.data, 'energy', '%g*min(1,max(0,(k-%g)/0.05))' % (380.0 * lk, cd['thr']), {'k': (ctrl, '["busy"]')})
            _halo_quad(SHOT, M, lp, 1.5, 'halo', ctrl=ctrl, thr=cd['thr'], cam=cam, name='halo_coach')
    for ob in SHOT.objects: no_bounce(ob); ob.visible_glossy = False

# ----------------------------------------------------------------------------- build
def _grade(scene, P, bloom=0.22):
    sys.path.insert(0, os.path.join(PROJ, 'spec'))
    import warnings, grade_compositor as G
    for ng in list(bpy.data.node_groups):
        if ng.name.startswith('GradeCLP'): bpy.data.node_groups.remove(ng)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        G.build(scene, preset=dict(vignette_strength=0.0, bloom_strength=bloom, bloom_size=P.get('bloom_size', 0.05), offset=tuple(P['grade_offset']), saturation=float(P['grade_saturation'])))
    scene.render.use_compositing = True
    ng = [g for g in bpy.data.node_groups if g.name.startswith('GradeCLP')][-1]; _hue_guard(ng)

def _hue_guard(ng):
    """Colour rule (client: magenta share <= 10 %): a Hue Correct in the grade pulls the magenta band (hue 290-345) toward blue-violet; pink / red and blue stay.
    Warm key + blue shade mix to magenta on dark surfaces in partial light; this keeps them blue-violet."""
    hs = [n for n in ng.nodes if n.bl_idname == 'CompositorNodeHueSat'][0]; mx = [n for n in ng.nodes if n.bl_idname == 'ShaderNodeMix'][0]
    hc = ng.nodes.new('CompositorNodeHueCorrect'); hc.location = (-200, 0)
    cv = hc.mapping.curves[0]
    for x, y in ((0.70, 0.48), (0.75, 0.45), (0.80, 0.41), (0.875, 0.35), (0.92, 0.32), (0.955, 0.41), (0.985, 0.5)):
        near = [p for p in cv.points if abs(p.location[0] - x) < 0.02]
        if near: near[0].location = (x, y)
        else: cv.points.new(x, y)
    hc.mapping.update()
    lk = hs.outputs['Image'].links[0]; dst = lk.to_socket; ng.links.remove(lk); ng.links.new(hs.outputs['Image'], hc.inputs['Image']); ng.links.new(hc.outputs['Image'], dst)

def setup_render(scene, quality='final'):
    MN.setup_render(scene, quality); c = scene.cycles; c.transparent_max_bounces = 24; c.glossy_bounces = 1; c.max_bounces = 2
    scene.render.threads = int(os.environ.get('THREADS', '2')); c.denoising_prefilter = 'ACCURATE'; c.sample_clamp_direct = float(os.environ.get('CLAMPD', '12'))
    if os.environ.get('SAMPLES'): c.samples = int(os.environ['SAMPLES'])
    elif quality == 'final': c.samples = 14
    elif quality == 'hq': c.samples = 16

def build(preset='street_wide', light='RAIN', clear=True):
    """Build the whole street (identical for every preset; `preset` only picks the camera, extras and placeholder staging in shot()). light: RAIN | DUSK_RAIN."""
    assert light in LIGHTS, 'light %s is not one of %s' % (light, LIGHT_NAMES)
    scene = bpy.context.scene; P = dict(LIGHTS[light]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['light'] = light; STATE['loc'] = 'street'; STATE['area'] = 'street'
    for h in (bpy.app.handlers.render_pre, bpy.app.handlers.frame_change_post):
        for f in list(h):
            if getattr(f, '__name__', '') in ('_pov_follow', '_sun_screen', '_cards_face'): h.remove(f)
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.curves, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    SHOT = T._coll('SHOT', scene); T._wipe(SHOT); STATE['SHOT'] = SHOT; CROWD = T._coll('CROWD', scene); T._wipe(CROWD); STATE['CROWD'] = CROWD
    for m in list(bpy.data.materials):
        if m.name.startswith(('ST_', 'ink')): bpy.data.materials.remove(m)
    tx = ST.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_street') or bpy.data.worlds.new('W_street'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_end = 1785; scene.frame_current = 1
    pre = 'ST_street_%s_' % light; FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None, glow=None, glow_k=0.0):
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s_%g' % (pre, name, gain, _k(sm), form, alpha, smix, glow_k), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None,
                               alpha=alpha, shade_mix=smix, glow=tx[glow] if glow else None, glow_k=glow_k))
    STATE.update(C=C, TX=TX, pre=pre)
    M = _materials(P, C, TX, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
    d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
    o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    STATE['shop_lights'] = []; STATE['coach_data'] = []; STATE['lamp_pts'] = []
    ctrl = _ctrl(); STATE['ctrl'] = ctrl
    _street(SET, LIG, P, M)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    _grade(scene, P)
    W9._air_comp(scene, P)
    for ob in SET.objects: no_bounce(ob); ob.visible_glossy = not ob.name.startswith(('rain', 'drips'))
    for ob in CROWD.objects: no_bounce(ob); ob.visible_glossy = False
    A = dict(preset=preset, light=light, cams=CAMS, key_dir=tuple(kd), units='1 unit = 1 head; z up; street along +y', stand=STAND, coaches=[_coach_anchor(cd) for cd in STATE['coach_data']],
             umbrella_slots=STATE['umb_slots'], rush=STATE['rush_slots'], puddles=STATE['puddles'], pink_hand=(RANK_X + 0.2, RANK_Y[0] - 3.55, 6.0), mud=dict(STATE['mud_info']))
    STATE['A'] = A
    return A

def _coach_anchor(cd):
    return dict(name=cd['name'], i=cd['i'], box_seat=tuple(cd['box']), door_street=tuple(cd['door_street']), door_kerb=tuple(cd['door_kerb']), horse_head=tuple(cd['horse_head']),
                lamps=[tuple(p) for p in cd['lamp_pts']], root=cd['name'])

def _street(SET, LIG, P, M):
    rs = _rnd(11); CROWD = STATE['CROWD']; ctrl = STATE['ctrl']
    _sky(SET, M); _ground(SET, M)
    STATE['puddles'] = _puddles(SET, M)
    rows = {}
    for side, seq in ((-1, LEFT_SEQ), (1, RIGHT_SEQ)):
        R = Row('L' if side < 0 else 'R'); rows[side] = R
        for i, fac in enumerate(seq):
            if fac is None: continue
            _house(R, M, side, Y0 + i * LOT, fac, _rnd(100 + i * 7 + (side + 1) * 31), i)
    LP = dict(iron=MB(), glass=MB())
    for i, y in enumerate([-34, -18, -2, 14, 30, 46, 62, 78, 94]):
        for s in (-1, 1):
            if (i + (s > 0)) % 2: continue
            STATE['lamp_pts'].append(_lamp_post(LP, M, s * (XP + 0.35), y + (3 if s > 0 else 0), 7.8, s))
    for key in ('iron', 'glass'): _obj(LP[key], 'lamps_' + key, SET)
    dm = MB()
    for (x, y, k) in ((-8.6, 25.5, 0), (-8.8, 0.5, 1), (8.6, 9.0, 0), (-8.4, 36.0, 1), (8.8, 62.0, 0), (-8.8, 60.0, 1)):
        _barrel(dm, M, Vector((x, y, ZP)), r=0.72, h=1.8, lying=False); _barrel(dm, M, Vector((x + 0.3 * (1 if x < 0 else -1), y + 1.5, ZP)), r=0.7, h=1.7, lying=bool(k), yaw=1.3)
    for (x, y) in ((-8.5, 23.0), (8.7, 14.5), (-8.7, 40.5), (8.5, 48.0)):
        _crate(dm, M, Vector((x, y, ZP)), 1.3, 1.3, 1.0, 0.2); _crate(dm, M, Vector((x - (0.1 if x > 0 else -0.1), y + 0.2, ZP + 1.0)), 1.1, 1.1, 0.9, 0.5)
    _obj(dm, 'barrels_crates', SET)
    _market(SET, M); _rank_props(SET, M)
    for side, R in rows.items(): _row_finish(SET, R, side)
    _lane_walls(SET, M, rs); _end_block(SET, M)
    STATE['rows'] = rows
    # coaches: the rank (4) on the right kerb facing -y, plus the running coach (parked far up the street; drive it with run_coach)
    for i, y in enumerate(RANK_Y): STATE['coach_data'].append(_coach(SET, M, i, (RANK_X, y)))
    STATE['coach_data'].append(_coach(SET, M, 4, (0.2, 140.0), name='coach_run'))
    # crowd: umbrella slots (umbrellas popped by `umb`, placeholder people in CROWD), rush figures, pink umbrella, mud splash
    _crowd_objects(SET, CROWD, M, ctrl); _pink_umbrella(SET, M, ctrl); _mud_objects(SET, M, ctrl)

def _crowd_objects(SET, CROWD, M, ctrl):
    slots = _umb_slots(); STATE['umb_slots'] = []
    for sl in slots:
        x, y, z = sl['pos']; hand = Vector((x, y, z + 1.95))
        mb = MB(); PT.umbrella(mb, M, Vector((0, 0, 2.35)), r=sl['r'], h=0.85, mat=sl['mat'], n=10, pole_to=Vector((0, 0, 0)), tilt=(sl['look'][0] * 0.15, 0.0))
        o = _obj(mb, 'umb_%02d' % sl['i'], SET); o.location = hand; _pop_scale(o, ctrl, 'umb', sl['thr'], 0.05)
        fb = MB(); PT.figure(fb, M, Vector((x, y, z)), h=3.2, coat='fig_' + 'abcde'[sl['i'] % 5], hat=True); fo = _obj(fb, 'crowd_%02d' % sl['i'], CROWD)
        STATE['umb_slots'].append(dict(i=sl['i'], feet=(round(x, 2), round(y, 2), z), look=(round(sl['look'][0], 2), round(sl['look'][1], 2)), hand=tuple(round(v, 2) for v in hand),
                                       open_at=round(sl['thr'], 2), radius=round(sl['r'], 2), colour=sl['mat']))
    rsl = _rush_slots(); STATE['rush_slots'] = []
    for j, r in enumerate(rsl):
        fb = MB(); PT.figure(fb, M, Vector((0, 0, 0)), h=3.0 + 0.3 * (j % 3) * 0.3, coat='fig_' + 'abcde'[(j + 2) % 5], hat=(j % 3 != 2)); fo = _obj(fb, r['name'], CROWD)
        p0, p1 = Vector(r['p0']), Vector(r['p1']); dly = r['delay']
        for ax in range(2):
            _drv(fo, 'location', '%g+(%g)*e' % (p0[ax], p1[ax] - p0[ax]), {'k': (ctrl, '["rush"]')}, ax) if False else None
        e = 'min(1,max(0,(k-%g)/%g))' % (dly, 1 - dly)
        _drv(fo, 'location', '%g+(%g)*%s' % (p0.x, p1.x - p0.x, e), {'k': (ctrl, '["rush"]')}, 0); _drv(fo, 'location', '%g+(%g)*%s' % (p0.y, p1.y - p0.y, e), {'k': (ctrl, '["rush"]')}, 1)
        _drv(fo, 'location', '0.3*abs(sin(frame*0.8+%g))*(%s>0.01)*(%s<0.99)' % (j, e, e), {'k': (ctrl, '["rush"]')}, 2)
        _drv(fo, 'rotation_euler', '0', {}, 2)
        STATE['rush_slots'].append(dict(name=r['name'], coach=r['coach'], start=tuple(round(v, 2) for v in p0), end=tuple(round(v, 2) for v in p1), look=r['look'], delay=round(dly, 2)))

def _pink_umbrella(SET, M, ctrl):
    mb = MB(); PT.umbrella(mb, M, Vector((0, 0, 2.7)), r=2.45, h=0.95, n=14, canopy_mat=M['pink'], pole_to=Vector((0, 0, 0)))
    for k in range(14):                                          # frill: small pale rosettes round the rim
        a = 2 * math.pi * k / 14; mb.sphere(Vector((2.45 * 0.97 * math.cos(a), 2.45 * 0.97 * math.sin(a), 2.7 - 0.95)), 0.16, M['cream_w'], seg=5, rings=3)
    o = _obj(mb, 'pink_umbrella', SET); o.location = (RANK_X + 0.2, RANK_Y[0] - 3.55, 6.0); _pop_scale(o, ctrl, 'pink', 0.0, 1.0)
    STATE['pink_obj'] = o

def _mud_objects(SET, M, ctrl):
    """Big comic mud-water wave: 13 curved fins in a fan + bulb tips + droplets, built at full size in a frame whose +x points along the throw; scale drivers on
    CTRL['mud'] (0..1): rise, peak at ~0.35, collapse by 1."""
    src = Vector((-1.7, 12.2, 0.0)); tgt = Vector((-3.8, 14.2, 1.2)); dxy = (tgt - src); dxy.z = 0; ang = math.atan2(dxy.y, dxy.x); rs = _rnd(66)
    mb = MB(); X = Vector((1, 0, 0))
    for j in range(13):
        phi = math.radians(-58 + 116 * j / 12) + rs.uniform(-0.05, 0.05); Hh = 3.9 * (1 - 0.45 * abs(phi) / 1.0) * rs.uniform(0.8, 1.1); Rr = 4.2 * (1 - 0.3 * abs(phi)) * rs.uniform(0.85, 1.1)
        dirh = Vector((math.cos(phi), math.sin(phi), 0)); lat = Vector((-math.sin(phi), math.cos(phi), 0)); pts = []; rad = []
        for n in range(8):
            t = n / 7.0; pts.append(dirh * (Rr * 0.85 * t ** 0.8) + Vector((0, 0, Hh * (1 - (1 - t) ** 2.2) + 0.1))); rad.append((0.7 * (1 - 0.6 * t), 0.2 * (1 - 0.4 * t)))
        PT.tube(mb, pts, rad, M['mud'], seg=6, up=lat)
        mb.sphere(pts[-1] + Vector((0, 0, 0.15)), rs.uniform(0.5, 0.75), M['mud_hi'], seg=7, rings=5)
    PT.loft(mb, [(Vector((0, 0, 0.12)), Vector((1, 0, 0)), Vector((0, 1, 0)), 1.6, 1.6), (Vector((0, 0, 0.9)), Vector((1, 0, 0)), Vector((0, 1, 0)), 0.9, 0.9)], M['mud'], seg=12)     # the boiling base
    o = _obj(mb, 'mud_wave', SET); o.location = src + Vector((0, 0, 0.02)); o.rotation_euler = (0, 0, ang)
    env = 'min(1,k/0.3)*(1-min(1,max(0,(k-0.55)/0.45)))'
    for ax, e in enumerate(('max(0.001,%s*(0.4+0.9*min(1,k/0.5)))' % env, 'max(0.001,%s*(0.4+0.9*min(1,k/0.5)))' % env, 'max(0.001,%s)' % env)): _drv(o, 'scale', e, {'k': (ctrl, '["mud"]')}, ax)
    for q in range(16):                                           # droplets on parabolas (world space)
        vx = rs.uniform(2.0, 7.0); vy = rs.uniform(-2.5, 2.5); vz = rs.uniform(4.0, 9.0); r_ = rs.uniform(0.12, 0.3); mb2 = MB(); mb2.sphere(Vector((0, 0, 0)), r_, M['mud_hi'] if q % 3 == 0 else M['mud'], seg=6, rings=4)
        do = _obj(mb2, 'mud_drop_%02d' % q, SET); ca, sa = math.cos(ang), math.sin(ang); wx = vx * ca - vy * sa; wy = vx * sa + vy * ca
        T_ = 'min(1.6,k*2.2)'
        _drv(do, 'location', '%g+%g*%s' % (src.x, wx, T_), {'k': (ctrl, '["mud"]')}, 0); _drv(do, 'location', '%g+%g*%s' % (src.y, wy, T_), {'k': (ctrl, '["mud"]')}, 1)
        _drv(do, 'location', '0.2+%g*%s-4.5*%s*%s' % (vz, T_, T_, T_), {'k': (ctrl, '["mud"]')}, 2)
        s_ = 'max(0.001,min(1,k*20)*(1-min(1,max(0,(k-0.8)/0.2)))*(location[2]>0))' if False else 'max(0.001,min(1,k*20)*(1-min(1,max(0,(k-0.85)/0.15))))'
        for ax in range(3): _drv(do, 'scale', s_, {'k': (ctrl, '["mud"]')}, ax)
    STATE['mud_info'] = dict(wheel_contact=(src.x, src.y, 0.0), toward=(round(math.cos(ang), 3), round(math.sin(ang), 3)), target_stand='hanway_mud', t_peak=0.35,
                             note='drive coach_run along x 0.2 (run_coach(f0, f1, y0, y1, x=0.2)): its left wheels (x -1.7) cross the puddle at y 12.2 when the origin is at y 14.5; key mud_splash(0)->(1) over ~1 s from that moment')

# ----------------------------------------------------------------------------- hooks (all frame-keyable: pass frame=N to key, omit to set the value now)
def _fcs(idb):
    """All F-curves of an ID's action (Blender 5 slotted actions: layers > strips > channelbags; older: action.fcurves) as (owner_collection, fcurve)."""
    ad = getattr(idb, 'animation_data', None); out = []
    if not ad or not ad.action: return out
    act = ad.action
    if hasattr(act, 'fcurves'): return [(act.fcurves, fc) for fc in act.fcurves]
    for ly in act.layers:
        for st in ly.strips:
            for cb in st.channelbags: out += [(cb.fcurves, fc) for fc in cb.fcurves]
    return out

def _setprop(prop, v, frame=None):
    ctrl = _ctrl()
    if frame is None:
        for owner, fc in _fcs(ctrl):
            if fc.data_path == '["%s"]' % prop: owner.remove(fc)
        ctrl[prop] = float(v)
    else:
        ctrl[prop] = float(v); ctrl.keyframe_insert('["%s"]' % prop, frame=int(frame))
    ctrl.update_tag(); bpy.context.view_layer.update()

def set_crowd_umbrellas(k, frame=None):
    """k 0..1: umbrellas pop open (staggered: pavements near Hanway first, then outward, the roadway last); every umbrella has its own threshold
    (A['umbrella_slots'][i]['open_at']). Key k=0 at f0 and k=1 at f1 and they pop one by one in between."""
    _setprop('umb', k, frame)

def set_rush(k, frame=None):
    """k 0..1: the placeholder crowd runs from the left kerb to the coach doors (A['rush'] start -> end, staggered); 0 = at the start points."""
    _setprop('rush', k, frame)

def set_rank_busy(k, frame=None):
    """k 0..1: coach i is full (passenger silhouettes, lit windows, lanterns lit) when k > i/4; k 0 = every coach empty (lamps off, windows dim)."""
    _setprop('busy', k, frame)

def set_pink_umbrella(on, frame=None):
    """The wife's pink frilled lace umbrella over the head coachman's box (pops open when `on` passes 0.5; key 0 -> 1 over a few frames for a pop)."""
    _setprop('pink', 1.0 if on is True else (0.0 if on is False else on), frame)

def rain(intensity=1.0, frame=None):
    """Rain intensity 0..1 (4 tiers of streaks and of puddle ripples). 1.0 is the full rain used in the contact sheet."""
    _setprop('rain', intensity, frame)
    for o in STATE.get('ripple_objs', []): pass

def mud_splash(t, frame=None):
    """Big comic mud-water wave from the wheel contact A['mud']['wheel_contact'] toward the Hanway stand 'hanway_mud'; t 0 = none, ~0.35 peak, 1 = collapsed."""
    _setprop('mud', t, frame)

def run_coach(f0, f1, y0=40.0, y1=-14.0, x=0.2):
    """Drive the running coach `coach_run` (with its horse) along the roadway from y0 to y1 between frames f0 and f1 (wheels roll, horse bobs). It faces -y."""
    r = bpy.data.objects['coach_run']
    for f, y in ((f0, y0), (f1, y1)):
        r.location = (x, y, 0.0); r.keyframe_insert('location', frame=int(f))
    for _, fc in _fcs(r):
        for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    bpy.context.view_layer.update()

def crowd_figures(on=True):
    """Show / hide the 3D placeholder people: True or 'all', 'umb' (the umbrella holders), 'rush' (the rush crowd), False. Hide them when the cast cards occupy the slots."""
    which = 'all' if on is True else on                        # True / 'all' | 'umb' | 'rush' | False
    for ob in STATE['CROWD'].objects:
        ob.hide_render = not (which == 'all' or (which == 'umb' and ob.name.startswith('crowd_')) or (which == 'rush' and ob.name.startswith('rush_')))

def throw(prop, p0, p1, t0, t1, normal=(0, 0, 1), arc=2.2, bounce=None, splat=True, name=None):
    """A cabbage ('cabbage') or egg ('egg') flies a parabola from p0 to p1 between frames t0 and t1 (spinning), then hits: a splat decal (egg yolk / cabbage leaves) appears at p1
    on the surface with the given normal (default up = an umbrella top) and stays; a cabbage may `bounce`=(dx, dy) away over 10 frames. Returns the prop object."""
    SET = STATE['SET']; M = STATE['M']; name = name or '%s_%d' % (prop, int(t0)); p0 = Vector(p0); p1 = Vector(p1); mb = MB(); rs = _rnd(int(t0) + 3)
    if prop == 'cabbage':
        lumpy(mb, Vector((0, 0, 0)), 0.5, M['cabbage'], 7, seg=9, rings=6, rough=0.18)
        for k in range(5): mb.sphere(Vector((0.5 * math.cos(k * 1.26), 0.5 * math.sin(k * 1.26), 0.0)), 0.22, M['cabbage'], seg=5, rings=3)
    else: PT.ell(mb, Vector((0, 0, 0)), 0.2, 0.2, 0.28, M['egg'], seg=8, rings=6)
    o = _obj(mb, name, SET); n = max(2, int(t1 - t0)); span = float(t1 - t0)
    def pos(u): return p0.lerp(p1, u) + Vector((0, 0, arc * 4 * u * (1 - u)))
    o.hide_render = True; o.keyframe_insert('hide_render', frame=int(t0) - 1)
    for f in range(int(t0), int(t1) + 1, 2 if span > 4 else 1):
        u = (f - t0) / span; o.location = pos(u); o.rotation_euler = (u * 9.0, u * 5.0, 0); o.hide_render = False
        o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_euler', frame=f); o.keyframe_insert('hide_render', frame=f)
    end = int(t1)
    if bounce:
        b = Vector((bounce[0], bounce[1], 0.0))
        for q, f in enumerate(range(end + 2, end + 12, 2)):
            u = (q + 1) / 5.0; o.location = p1 + b * u + Vector((0, 0, 1.1 * 4 * u * (1 - u) - 0.0 * u)); o.rotation_euler = (u * 9.0 + 9, u * 5.0, 0)
            o.keyframe_insert('location', frame=f); o.keyframe_insert('rotation_euler', frame=f)
        end = end + 11
    o.location = p1; o.hide_render = True; o.keyframe_insert('hide_render', frame=end + 1)
    for _, fc in _fcs(o):
        for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT' if fc.data_path == 'hide_render' else 'LINEAR'
    if splat:
        sm = MB(); sz = 0.9 if prop == 'egg' else 1.3
        sm.face([Vector((-sz, -sz, 0)), Vector((sz, -sz, 0)), Vector((sz, sz, 0)), Vector((-sz, sz, 0))], M['splat_egg' if prop == 'egg' else 'splat_cab'], [(0, 0), (1, 0), (1, 1), (0, 1)])
        so = _obj(sm, name + '_splat', SET, shadow=False); nv = Vector(normal).normalized(); so.location = p1 + nv * 0.04; so.rotation_euler = nv.to_track_quat('Z', 'Y').to_euler()
        so.rotation_euler.rotate_axis('Z', rs.uniform(0, 6.28)); so.visible_glossy = False
        so.hide_render = True; so.keyframe_insert('hide_render', frame=int(t1) - 1); so.hide_render = False; so.keyframe_insert('hide_render', frame=int(t1))
        for _, fc in _fcs(so):
            for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    return o

# ----------------------------------------------------------------------------- cameras
def camera_pose(preset, u=0.0):
    cs = CAMS[preset]; u = max(0.0, min(1.0, u)); e = u * u * (3 - 2 * u)
    lerp = lambda a, b: tuple(x + (y - x) * e for x, y in zip(a, b))
    return dict(loc=lerp(cs['loc'], cs['loc_b']), look_at=lerp(cs['look_at'], cs['look_b']), lens=cs['lens'])

def make_camera(setup, name='cam', scene=None):
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 3000.0; ob.data.dof.use_dof = False
    return ob

def key_camera(preset, f0, f1, cam=None):
    """Key the preset camera's A pose at f0 and its B pose (the 'move') at f1, smooth ease; returns the camera. The rain / halos follow it (parented / constrained)."""
    cam = cam or bpy.context.scene.camera
    for f, u in ((f0, 0.0), (f1, 1.0)):
        make_camera(camera_pose(preset, u)); cam.keyframe_insert('location', frame=int(f)); cam.keyframe_insert('rotation_euler', frame=int(f))
    return cam

def project_px(cam, p, W=720, H=1280):
    sc = bpy.context.scene; from bpy_extras.object_utils import world_to_camera_view
    v = world_to_camera_view(sc, cam, Vector(p)); return v.x * W, (1 - v.y) * H, v.z

# ----------------------------------------------------------------------------- placeholders
def _placeholder(role, mark, face_to, name, tilt=0.0):
    ob = T.placeholder_actor(PH_ROLES[role][0], mark, face_to=face_to, tilt=tilt, name=name); ob.visible_glossy = True
    return ob

def staged(preset, u=0.0):
    """The (stand point, role, umbrella) list staged for a preset at move position u (A: STAGE; B (u >= 0.5): STAGE_B names only; hero_track A skips hanway_c, B skips hanway_b)."""
    L = list(STAGE[preset])
    if preset == 'hero_track': L = [s for s in L if s[0] != ('hanway_c' if u < 0.5 else 'hanway_b') and (u < 0.5 or s[0] == 'hanway_c')]
    elif u >= 0.5 and preset in STAGE_B: L = [s for s in L if s[0] in STAGE_B[preset]]
    return L

def stage_placeholders(preset=None, names=None, figures=True, tilt=None, u=0.0):
    """Placeholder actor cards (1 unit = 1 head, adults 2.9-3.1) at the stand points of the preset (STAGE) facing the camera, umbrellas for those who hold one,
    plus the 3D placeholder crowd figures (figures=True). Returns the card objects."""
    scene = bpy.context.scene; cam = scene.camera; cl = cam.matrix_world.translation; M = STATE['M']; SET = STATE['SHOT']; out = []
    preset = preset or STATE.get('preset'); crowd_figures(figures)
    for (nm, role, umb) in staged(preset, u):
        if names and nm not in names: continue
        st = STAND[nm]; x, y, z = st['pos']; tl = 0.0 if tilt is None else tilt
        if preset == 'street_high' and tilt is None: tl = 22.0
        out.append(_placeholder(role, (x, y, z), cl, 'actor_%s' % nm, tilt=tl))
        if umb:
            um = MB(); h = PH_ROLES[role][1]; PT.umbrella(um, M, Vector((0.05, 0.0, z + h + 1.0)) + Vector((x, y, 0)), r=2.2, h=0.8, mat=umb, pole_to=Vector((x + 0.55, y - 0.05, z + 1.9))); _obj(um, 'ph_umbrella_%s' % nm, SET)
    for ob in SET.objects: no_bounce(ob); ob.visible_glossy = ob.name.startswith(('ph_umb',))
    for o in out: o.visible_glossy = True
    return out

def shot(preset='street_wide', light='RAIN', u=0.0, placeholders=True, figures=False, quality='final'):
    """Build the set (light), the preset camera at move position u (0 = A, 1 = B), the camera-dependent extras and (optionally) the placeholder cards. Returns the anchors dict A,
    A['cam'] = the camera object."""
    A = build(preset, light); sc = bpy.context.scene; setup_render(sc, quality)
    cam = make_camera(camera_pose(preset, u)); bpy.context.view_layer.update(); A['cam'] = cam
    _shot_extras(cam, preset)
    if placeholders: stage_placeholders(preset, figures=figures, u=u)
    bpy.context.view_layer.update()
    return A

def render(path, scene=None):
    return T.render(path, scene)

# ----------------------------------------------------------------------------- states for stills / contact tiles
def apply_state(st):
    """st: dict of hook values: umb, busy, pink, rush, rain, mud (all static values at the current frame)."""
    if 'umb' in st: set_crowd_umbrellas(st['umb'])
    if 'busy' in st: set_rank_busy(st['busy'])
    if 'pink' in st: set_pink_umbrella(st['pink'])
    if 'rush' in st: set_rush(st['rush'])
    if 'rain' in st: rain(st['rain'])
    if 'mud' in st: mud_splash(st['mud'])

def render_preset(preset, out, quality='final', light='RAIN', state=None, u=0.0, extra=None):
    A = shot(preset, light, u=u, quality=quality)
    if state: apply_state(state)
    if extra: extra(A)
    bpy.context.view_layer.update()
    return render(out, bpy.context.scene)

# ----------------------------------------------------------------------------- CLI
if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('stills', 'final'):
        q = 'preview' if cmd == 'stills' else 'final'; names = [a for a in arg if a in CAMS] or PRESETS; light = ([a for a in arg if a in LIGHTS] or ['RAIN'])[0]
        outdir = os.path.join(WORK, 'stills' if cmd == 'stills' else 'final'); os.makedirs(outdir, exist_ok=True)
        for pr in names:
            w, c = render_preset(pr, os.path.join(outdir, '%s_%s_%s.png' % (pr, light, q)), q, light)
            print('%s %s %s: %.1f s wall, %.1f s cpu' % (q, pr, light, w, c), flush=True)
    else: print(__doc__)
