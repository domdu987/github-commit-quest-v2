"""h19_ship.py : SHIP location of film 19 ("ไอ้ช่างไม้", John Harrison): a 1760s 50-gun warship (HMS Deptford type) at sea, on deck, in a storm, at anchor off a tropical coast.

    import h19_ship as SH
    A = SH.build_ship(SET, 'ship_hero', 'NOON')       # -> dict(cams, cam, marks, ship_root, location)   (called by h19.build)
    SH.set_sea(t, frame=None); SH.set_roll(t, frame=None); SH.set_sun_overhead(k, frame=None); SH.set_rain(on, frame=None)

Presets: ship_hero ship_aerial ship_deck ship_rail ship_rocks ship_coast (+ ship_shore).  Lights: NOON DAY STORM_DUSK.
Authoring is in METRES under scaled empties (D = 1.85 x metres); every camera / mark in the returned dict is in world D.  Ship frame: ship at the origin, bow +y,
starboard +x.  `coast='jamaica'|'barbados'` (option) or the light names DAY_JAMAICA / DAY_BARBADOS dress the coast preset.
All geometry is procedural; no text anywhere; no depth of field."""
import os, sys, math, random
import numpy as np
import bpy
from mathutils import Vector, Matrix, Euler
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import h19_kit as K
from h19_kit import hexc, mat, mat_emit, MB
import h19_ship_hull as HU
import h19_ship_deck as DK
import h19_ship_sea as SE
import h19_ship_fx as FX
import h19_ship_land as LD

SC = K.SC
S = {}                                 # live state of the ship location (rebuilt by build_ship)

def kdir(az, el):
    a = math.radians(az); e = math.radians(el)
    return (-math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), -math.sin(e))

# ----------------------------------------------------------------------------- lights
SKY_NOON = [(0.0, '#6c9ce0'), (0.46, '#b6cfe8'), (0.5, '#b0cbe8'), (0.56, '#8db3e6'), (0.66, '#6a98e0'), (0.78, '#4a7bd6'), (0.88, '#3a67cb'), (1.0, '#2c54b6')]
SKY_DAY = [(0.0, '#7ab0ea'), (0.46, '#c2dbee'), (0.5, '#bcd8ee'), (0.56, '#98c0ee'), (0.66, '#74a6e8'), (0.78, '#5288dc'), (0.88, '#3f72d2'), (1.0, '#315cbc')]
SKY_STORM = [(0.0, '#4a5a74'), (0.46, '#8e9aae'), (0.5, '#8c98ac'), (0.56, '#6e7c96'), (0.66, '#5a6a86'), (0.78, '#485874'), (0.88, '#3a4a68'), (1.0, '#2c3c5a')]
LIGHTS = dict(
    NOON=dict(key=(1.0, 0.92, 0.78, 7.2), az=160, el=46, sun_angle=0.9, sky=SKY_NOON, sky_k=1.0, amb=('#3050FF', 2.4), gloss_sky_k=0.42, exposure=0.1, sat=1.08,
              cloud=('#ffffff', '#98a8ee'), haze='#b0cbe8', sea_amp=1.0, sea_near='#07505e', sea_mid='#157f8e', sea_far='#0b3a5c', foam_k=1.0, wc=(0.74, 1.05), lamp=0.0, rain_ok=False, fog=0.0),
    DAY=dict(key=(1.0, 0.94, 0.80, 7.6), az=200, el=40, sun_angle=0.9, sky=SKY_DAY, sky_k=1.0, amb=('#3a58FF', 2.3), gloss_sky_k=0.5, exposure=0.12, sat=1.1,
             cloud=('#ffffff', '#a0b0f0'), haze='#bcd8ee', sea_amp=0.55, sea_near='#0f6a78', sea_mid='#16808a', sea_far='#10405c', foam_k=0.9, wc=(0.8, 1.1), lamp=0.0, rain_ok=False, fog=0.0),
    STORM_DUSK=dict(key=(1.0, 0.62, 0.45, 2.2), az=250, el=7, sun_angle=2.5, sky=SKY_STORM, sky_k=0.85, amb=('#6c80d8', 1.75), gloss_sky_k=0.55, exposure=-0.1, sat=1.04,
                    cloud=('#98a4b6', '#4c586a'), haze='#7c8898', sea_amp=1.7, sea_near='#16384a', sea_mid='#1a4052', sea_far='#1c2a48', foam_k=1.5, wc=(0.5, 0.9), lamp=1.0, rain_ok=True, fog=1.0),
)
LIGHTS['DAY_JAMAICA'] = dict(LIGHTS['DAY'], coast='jamaica'); LIGHTS['DAY_BARBADOS'] = dict(LIGHTS['DAY'], coast='barbados')
LIGHT_NAMES = ['NOON', 'DAY', 'STORM_DUSK']

# ----------------------------------------------------------------------------- presets (metres, ship frame; cam loc / look in metres; converted to D when returned)
def _hero_cam():
    p = SE.v6_pos((0.0, 0.0, 4.2)); d = SE.v6_dir((0.0, 100.0, 100.0 * math.tan(math.radians(3.0))))
    return dict(loc=p, look=(p[0] + d[0], p[1] + d[1], p[2] + d[2]), lens=22)

PRESETS = dict(
    ship_hero=dict(light='NOON', cam=_hero_cam(), scenery='hero', glint=dict(az=19, el=6, k=40.0, ang=1.8, v6=True), wake=True, samples=12),
    ship_aerial=dict(light='NOON', cam=dict(loc=(-70.0, 95.0, 85.0), look=(2.0, 6.0, 14.0), lens=22), scenery='aerial', glint=dict(az=118, el=34, k=20.0, ang=0.45), sea_amp=0.55, chop=0.22, rough=0.15, wc_k=0.0, sea_nu=470, sea_nv=700, wake=True, samples=10),
    ship_deck=dict(light='NOON', amb_k=0.8, amb_col='#2c64ff', cam=dict(loc=(-0.6, -21.4, DK.ZQ + 1.5), look=(0.6, -9.0, DK.ZQ + 1.2), lens=22), scenery='deck', sun_ship=True, sun_az=-148, sun_el=60, glint=dict(az=170, el=20, k=30.0, ang=2.0), wake=True, sea_nu=360, sea_nv=520, samples=11),
    ship_rail=dict(light='NOON', amb_k=0.8, amb_col='#2c64ff', cam=dict(loc=(3.9, 7.0, DK.ZW + 2.6), look=(8.63, 25.98, DK.ZW + 2.6 - 4.16), lens=22), scenery='rail', sun_ship=True, sun_az=-120, sun_el=76, glint=dict(az=40, el=12, k=34.0, ang=1.4), sea_nu=420, sea_nv=620, wake=True, samples=11),
    ship_rocks=dict(light='STORM_DUSK', amb_col='#3a6cf2', amb_k=2.3, cam=dict(loc=(2.2, 14.2, DK.ZF + 2.4), look=(8.28, 42.79, DK.ZF + 2.4 - 6.75), lens=22), scenery='rocks', lantern=(0.9, 0.3, 0.4), lantern_e=60.0, no_fore_lamp=True, glint=dict(az=250, el=9, k=18.0, ang=3.0), wake=True, samples=12),
    ship_coast=dict(light='DAY_JAMAICA', cam=dict(loc=(float(LD.shore_x(40.0)) + 9.0, 33.0, 2.0), look=(float(LD.shore_x(40.0)) + 9.0 - 60.0, 34.5, -2.2), lens=22), scenery='coast', sun_ship=True, sun_az=115, sun_el=38, glint=dict(az=-80, el=12, k=26.0, ang=2.0), sea_amp=0.45, chop=0.25, wake=False, anchored=True, samples=12),
    ship_shore=dict(light='DAY_JAMAICA', cam=dict(loc=(float(LD.shore_x(40.0)) + 10.5, 33.0, 2.5), look=(float(LD.shore_x(40.0)) - 70.0, 38.0, 4.0), lens=22), scenery='shore', sun_ship=True, sun_az=115, sun_el=38, glint=dict(az=-80, el=12, k=26.0, ang=2.0), wake=False, anchored=True, samples=12),
)
STAGING = dict(      # (role, mark) pairs the placeholder actors stand on, per preset camera
    ship_deck=[('captain', 'captain_wheel'), ('william', 'william_deck'), ('astro', 'astro_quarter')],
    ship_rail=[('william', 'william_rail')],
    ship_rocks=[('captain', 'captain_bow'), ('sailor', 'crew_bow')],
    ship_coast=[('william', 'shore_a'), ('sailor', 'shore_b'), ('astro', 'shore_c')],
)
PRESET_NAMES = ['ship_hero', 'ship_aerial', 'ship_deck', 'ship_rail', 'ship_rocks', 'ship_coast']

# ----------------------------------------------------------------------------- world / sun
def make_world(LT):
    w = bpy.data.worlds.new('sky'); bpy.context.scene.world = w; w.use_nodes = True; nt = w.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    out = N('ShaderNodeOutputWorld'); bg = N('ShaderNodeBackground'); bg.name = 'skybg'; tc = N('ShaderNodeTexCoord'); sp = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sp.inputs[0])
    cr = N('ShaderNodeValToRGB'); cr.name = 'skyramp'; L(sp.outputs['Z'], cr.inputs[0]); stops = LT['sky']
    cr.color_ramp.elements[0].position = stops[0][0]; cr.color_ramp.elements[0].color = hexc(stops[0][1])
    for pos, col in stops[1:-1]:
        e = cr.color_ramp.elements.new(pos); e.color = hexc(col)
    cr.color_ramp.elements[-1].position = stops[-1][0]; cr.color_ramp.elements[-1].color = hexc(stops[-1][1])
    bg.inputs['Strength'].default_value = LT['sky_k']; L(cr.outputs[0], bg.inputs['Color'])
    lp = N('ShaderNodeLightPath'); b2 = N('ShaderNodeBackground'); b2.name = 'ambbg'; b2.inputs['Color'].default_value = hexc(LT['amb'][0]); b2.inputs['Strength'].default_value = LT['amb'][1]
    ad = N('ShaderNodeMath'); ad.operation = 'ADD'; ad.use_clamp = True; L(lp.outputs['Is Camera Ray'], ad.inputs[0]); L(lp.outputs['Is Glossy Ray'], ad.inputs[1])
    bgG = N('ShaderNodeBackground'); bgG.inputs['Strength'].default_value = LT['sky_k'] * LT.get('gloss_sky_k', 1.0); L(cr.outputs[0], bgG.inputs['Color'])
    mxs = N('ShaderNodeMixShader'); L(lp.outputs['Is Camera Ray'], mxs.inputs[0]); L(bgG.outputs[0], mxs.inputs[1]); L(bg.outputs[0], mxs.inputs[2])
    mx = N('ShaderNodeMixShader'); L(ad.outputs[0], mx.inputs[0]); L(b2.outputs[0], mx.inputs[1]); L(mxs.outputs[0], mx.inputs[2]); L(mx.outputs[0], out.inputs['Surface'])
    K.STATE['world'] = w

def sun_dir_local(LT, el=None, az=None):
    a = LT['az'] if az is None else az; e = LT['el'] if el is None else el
    return SE.v6_dir(kdir(a, e))

def make_sun(LT, P):
    az = P.get('sun_az', LT['az']); el = P['sun_el'] if (P.get('sun_el') and LT['el'] > 20) else LT['el']
    d = kdir(az, el) if P.get('sun_ship') else SE.v6_dir(kdir(az, el)); S['sun_az'] = az; S['sun_el0'] = el; S['sun_ship'] = bool(P.get('sun_ship'))
    o = K.sun('ssun_key', LT['key'], LT['key'][3], d, LT['sun_angle']); S['sun'] = o; S['key_dir'] = d
    return o

def _parent_new(before, parent, skip=('ship_root', 'ship_body', 'ship_world')):
    for o in set(bpy.data.objects) - before:
        if o.parent is None and o.type not in ('LIGHT', 'CAMERA') and o.name not in skip: o.parent = parent

def _empty(name, parent=None, loc=(0, 0, 0), scale=1.0):
    o = bpy.data.objects.new(name, None); o.empty_display_size = 1.0; bpy.context.scene.collection.objects.link(o)
    o.location = loc; o.scale = (scale, scale, scale)
    if parent is not None: o.parent = parent
    return o

# ----------------------------------------------------------------------------- build
def build_ship(SET, preset, light=None):
    P = PRESETS[preset]; lname = light or P['light']
    if preset in ('ship_coast', 'ship_shore') and lname in ('DAY', None): lname = 'DAY_' + (K.STATE.get('coast') or 'JAMAICA').upper()
    LT = dict(LIGHTS[lname]); coast = LT.get('coast') or (K.STATE.get('coast') or 'jamaica')
    LTb = LIGHTS['NOON'] if lname == 'NOON' else LT
    scene = bpy.context.scene
    HU.THEME.clear(); HU.THEME['warm'] = preset in ('ship_deck', 'ship_rail', 'ship_rocks'); HU.THEME['no_stern_lamp'] = preset == 'ship_deck'; HU.THEME['sail_k'] = 0.26 if preset == 'ship_rail' else 0.42
    S.clear(); S.update(preset=preset, light=lname, coast=coast, P=P, LT=LT)
    K.STATE['samples'] = P.get('samples', 12); K.STATE['dbounce'] = 0
    world = K.new_root('ship_world'); S['world_root'] = world
    root = _empty('ship_root'); body = _empty('ship_body', root, scale=SC)
    S['root'] = root; S['body'] = body
    before = set(bpy.data.objects)
    # ---- ship
    K.ROOT = body; HU.BODY[0] = body
    M = DK.deck_mats(); S['M'] = M
    HU.build_ship6_into(M) if hasattr(HU, 'build_ship6_into') else HU.build_ship6(dict())
    dobjs, lants = DK.build_deck_all(M, skip_fore_lamp=bool(P.get('no_fore_lamp'))); S['lants'] = lants
    if P.get('lantern'): S['fglamp'] = DK.fg_lantern(M, P['cam'], P['lantern'])
    _parent_new(before, body)
    # marks (empties under the ship_root, D units)
    marks = {}
    mk = DK.marks()
    for nm, p in mk.items():
        e = _empty('mark_' + nm, root, loc=tuple(v * SC for v in p)); marks[nm] = tuple(round(v * SC, 3) for v in p)
    # ---- scenery, sea
    K.ROOT = world
    sea_P = dict(cam=dict(loc=P['cam']['loc'], look=P['cam']['look']), amp=P.get('sea_amp', LT['sea_amp']), chop=P.get('chop', 0.6 if lname != 'STORM_DUSK' else 1.2), wc_k=P.get('wc_k', 0.85), rough=P.get('rough', 0.1), sea_nu=P.get('sea_nu', 560), sea_nv=P.get('sea_nv', 820), sea_near=LT['sea_near'], sea_mid=LT['sea_mid'], sea_far=LT['sea_far'],
                 fresnel_k=0.38, foam_k=LT['foam_k'], wc_min=LT['wc'][0], wc_max=LT['wc'][1], anchored=P.get('anchored', False), ship_foam=True, lift='#9fc2d8',
                 glint=dict(dir=(SE.v6_dir(kdir(P['glint']['az'], P['glint']['el'])) if P['glint'].get('v6') else kdir(P['glint']['az'], P['glint']['el'])), k=P['glint']['k'] * max(0.25, LT['key'][3] / 7.2), ang=P['glint']['ang']))
    LD.scenery(S, P, LT, sea_P, marks)
    b0 = set(bpy.data.objects)
    sea = SE.build_sea(sea_P, world); S['sea'] = sea; S['tsocks'] = list(sea['tsocks'])
    _parent_new(b0, world)
    # ---- bow wave + spray (ride the hull), clouds
    b1 = set(bpy.data.objects)
    bowfx = _empty('bow_fx', body); S['bowfx'] = bowfx
    if not P.get('anchored'):
        Pp, Nn, E, Ll = FX.bow_wave6(dict(cam=dict(loc=P['cam']['loc'])), parent=bowfx); FX.spray6(dict(cam=dict(loc=P['cam']['loc'])), M, Pp, Nn, E, Ll)
        for o in set(bpy.data.objects) - b1:
            if o.parent is None and o.type == 'MESH': o.parent = bowfx
    LTw = dict(LT); LTw['amb'] = (P.get('amb_col', LT['amb'][0]), LT['amb'][1] * P.get('amb_k', 1.0))
    make_world(LTw); make_sun(LT, P)
    S['sun_energy'] = LT['key'][3]
    if S.get('fglamp') is not None: K.point_light('lampfg', S['fglamp'], (1.0, 0.56, 0.26), P.get('lantern_e', 60.0), 0.12).parent = root
    # ---- lights on the ship (lanterns) at dusk
    if LT.get('lamp'):
        for i, c in enumerate(lants):
            K.point_light('lamp%d' % i, c, (1.0, 0.72, 0.4), 90.0 * LT['lamp'], 0.12).parent = root
    scene.view_settings.exposure = LT['exposure']
    K.STATE['grade_sat'] = LT['sat']; K.STATE['sat'] = LT['sat']
    # ---- cameras (D)
    cams = {}
    def cam_D(c): return dict(loc=tuple(round(v * SC, 4) for v in c['loc']), look_at=tuple(round(v * SC, 4) for v in c['look']), lens=c.get('lens', 22))
    cams[preset] = cam_D(P['cam'])
    cams.update({k: cam_D(v) for k, v in S.get('extra_cams', {}).items()})
    for k, v in S.get('shore_marks', {}).items(): marks[k] = tuple(round(c * SC, 3) for c in v)
    set_roll(0.0)
    stg = {preset: [(r, marks[m]) for (r, m) in STAGING.get(preset, []) if m in marks]}
    A = dict(cams=cams, cam=preset, marks=marks, ship_root=root, location='ship', staging=stg)
    S['A'] = A
    return A

# ----------------------------------------------------------------------------- hooks
def _roll_values(t):
    h = float(SE.swell_h(0.0, 0.0, t, S['LT']['sea_amp'] if S else 1.0)); gx, gy = SE.swell_grad(0.0, 0.0, t, S['LT']['sea_amp'] if S else 1.0)
    pitch = 0.22 * math.atan(gy) + math.radians(0.35) * math.sin(0.83 * t + 1.1)
    roll = -0.22 * math.atan(gx) + math.radians(0.5) * math.sin(0.61 * t)
    lim = math.radians(1.9)
    return float(np.clip(pitch, -lim, lim)), float(np.clip(roll, -lim, lim)), 0.8 * h * 0.35 + 0.05 * math.sin(1.7 * t)

def _roll_rel(t):
    """roll values relative to t=0 (the ship is exactly level at t=0, so the marks / cameras of the API are exact there)"""
    if 'roll0' not in S: S['roll0'] = _roll_values(0.0)
    a = _roll_values(t); b = S['roll0']; return a[0] - b[0], a[1] - b[1], a[2] - b[2]

def set_roll(t, frame=None):
    """gentle roll / pitch (<= 2 deg) and bob of the whole ship (ship_root, so every deck mark / card parented to it moves with the deck); t in seconds"""
    root = S['root']; pitch, roll, bob = _roll_rel(t)
    root.rotation_euler = (pitch, roll, 0.0); root.location = (0.0, 0.0, bob * SC)
    K._keyxf(root, frame, loc=True, rot=True)
    bf = S.get('bowfx')
    if bf is not None:
        bf.location = (0.0, 0.0, 0.0)

def set_sea(t, frame=None):
    """swells, chop, foam drift and wake by time t (seconds): the geometry-nodes swell and the foam noise key on sea_t"""
    for sock in S['tsocks']: K._keysock(sock, float(t), frame)
    bf = S.get('bowfx')
    if bf is not None:
        dh = float(SE.swell_h(0.0, 21.0, t, S['LT']['sea_amp'])) - float(SE.swell_h(0.0, 21.0, 0.0, S['LT']['sea_amp']))
        bf.location = (0.0, 0.0, dh * 0.85 / 1.0)                    # the bow sheet rides the swell at the stem (metres, body space)
        K._keyxf(bf, frame, loc=True)

def set_sun_overhead(k, frame=None):
    """k 0..1: the sun climbs from the light's elevation to the zenith (88 deg): the mast shadow shrinks to its foot on the deck"""
    o = S['sun']; el0 = S['sun_el0']; el = el0 + (88.0 - el0) * float(np.clip(k, 0, 1))
    d = kdir(S['sun_az'], el) if S.get('sun_ship') else SE.v6_dir(kdir(S['sun_az'], el)); o.rotation_euler = (-Vector(d).normalized()).to_track_quat('Z', 'Y').to_euler()
    K._keyxf(o, frame, loc=False, rot=True)

def set_rain(on, frame=None):
    """rain streaks (three layers of real streak geometry in front of the scene camera); call after make_camera, per frame for a moving camera"""
    LD.rain(S, on, frame)
