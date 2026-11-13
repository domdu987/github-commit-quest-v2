#!/usr/bin/env python3
"""louvre.py : sets of film 7 ("the macaroni guy", the Mona Lisa theft, Paris, August 1911) as real 3D Blender sets (bpy 5.3, Cycles CPU).
Three locations, each built by preset (the preset picks the area, the light, the default camera and the set state):

    import louvre as L
    A = L.build('louvre', 'gallery_wide')     # gallery_wide | wall_eye | empty_wall_queue  (the Salon Carre)
                                              # closet | staircase | exit_door            (the service rooms)
    A = L.build('paris', 'street_wide')       # street_wide | kiosk | notre_dame_view      (the street outside, the quai)
    A = L.build('room', 'room_wide')          # room_wide | under_bed_insert (the attic) | dealer_shop (the Florence shop)
    cam = L.make_camera(A['cam'])             # the preset's camera (all cameras of the area are in A['cams'])
    L.set_mona(True, frame=1); L.set_mona(False, frame=40)   # the Mona Lisa on the wall / gone (the four iron hooks remain)
    L.set_mona_lift(0.3, frame=20)            # lift the framed painting off its hooks (D, up and out from the wall)
    L.set_papers(12, frame=10)                # paris: newspapers / posters with her face shown (0..24)
    L.set_door(80, frame=30)                  # exit_door: the locked service door, 0 shut .. 95 wide open (daylight floods in)
    L.set_trunk(pull=0.6, open_deg=70)        # room: the wooden trunk under the bed (pulled out, lid open, the panel inside)
    L.set_flames(1.0, frame=10)               # flicker of every gas jet, lantern and candle (call per frame; deterministic)

World: 1 unit = 1 D (head diameter), Z up, floor z = 0. NO depth of field anywhere (client rule: images sharp); setup_dof is kept
only so shot scripts can call setup_dof(scene, None, None, cam=cam). Built on v3/set3d6/bakery.py -> mine.py -> pagoda.py / tower.py:
materials, mesh builder, render, grade, cameras, keys, actors, haze, denoiser, glow cards are imported, not rewritten. See louvre_API.md.
CLI: python3 louvre.py stills | final <loc> [preset ..] | digest <loc> <preset> | contact"""
import os, sys, math, json, time, random
import bpy
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(PROJ, 'v3', 'set3d2'), os.path.join(PROJ, 'v3', 'set3d4'), os.path.join(PROJ, 'v3', 'set3d5'), os.path.join(PROJ, 'v3', 'set3d6')):
    if p not in sys.path: sys.path.insert(0, p)
import tower as T                                          # noqa: E402
import pagoda as G                                         # noqa: E402
import mine as MN                                          # noqa: E402
import bakery as BK                                        # noqa: E402  (film-6 template: glow cards, candles, halos, Frame, lights)
import louvre_tex as LT                                    # noqa: E402
from tower import MB, no_bounce, setup_grade, make_camera, render, mat_lit, mat_emit   # noqa: E402,F401
from mine import obox, beam, rod, lumpy, catenary, chain_rod, _obj, _untoon, _glossy, vnoise   # noqa: E402,F401
WORK = os.path.join(HERE, 'louvre_work')
T.ACT = os.path.join(WORK, 'actors')
STATE = T.STATE
setup_dof = G.setup_dof; digest = G.digest
Frame = BK.Frame; _halo = BK._halo

def _rnd(seed): return random.Random(seed)
GAS = (1.0, 0.8, 0.5); CANDLE = (1.0, 0.78, 0.47); LANTERN = (1.0, 0.76, 0.44)

# ----------------------------------------------------------------------------- dimensions (D)
GAL = (-13.0, 13.0, 0.0, 22.0); GAL_H = 14.0; CORN = 15.2; LAY_Z = 17.6     # the Salon Carre: x0, x1, y0, y1; wall top, cornice top, laylight
SKY_OPEN = (-8.0, 8.0, 4.5, 17.5)                                           # the skylight opening in the laylight ceiling
MONA_C = (0.0, 21.92, 3.55); MONA_W, MONA_H = 1.0, 1.45; MONA_FW = 0.2     # centre on the back wall (y 22), canvas size, frame width
HOOKS = [(-0.62, 2.62), (0.62, 2.62), (-0.62, 4.62), (0.62, 4.62)]          # the four iron hooks (x, z) on the back wall
SERVICE_DOOR = (8.0, 10.0, 0.0, 4.2)                                        # front wall (y 0): the service door x0, x1, z0, z1
STREET = dict(road=(-4.0, 4.0), walk=(-7.0, 7.0), y=(-12.0, 62.0), quai_y=62.0)
ATTIC = (-4.0, 4.0, 0.0, 6.0); ATTIC_H = 7.0
SHOP = (-6.0, 6.0, 0.0, 9.0); SHOP_H = 7.5

# ----------------------------------------------------------------------------- presets (area, light, camera, state)
_IN = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=(0.0, -0.05, 0.22), bloom_size=0.05, grade_offset=(0.002, 0.003, 0.006))
LIGHTS = dict(
    GALLERY_DAY=dict(_IN, key=(1.55, 1.30, 0.92), key_dir=G._kd((0.22, 0.97), 57), sun_elev=57, sun_angle=0.8, shade=(0.085, 0.095, 0.21), shade_tint=(0.085, 0.11, 0.27),
                     shade_mix=0.78, lift=(0.008, 0.006, 0.014), sky='day', sky_k=1.0, haze=None, grade_saturation=1.12, shaft_k=0.22, fill=1.0, gas=1.0),
    CLOSET_NIGHT=dict(_IN, key=(0.05, 0.05, 0.08), key_dir=G._kd((0.3, 0.9), 40), sun_elev=40, sun_angle=1.0, shade=(0.04, 0.055, 0.11), shade_tint=(0.045, 0.065, 0.15),
                      shade_mix=0.7, lift=(0.004, 0.003, 0.008), sky='dusk', sky_k=0.3, haze=None, grade_saturation=1.15, shaft_k=0.0, fill=0.0, gas=1.0),
    STAIR_MORNING=dict(_IN, key=(1.45, 1.22, 0.90), key_dir=G._kd((0.85, 0.45), 38), sun_elev=38, sun_angle=0.8, shade=(0.075, 0.08, 0.12), shade_tint=(0.075, 0.085, 0.15), grade_offset=(0.001, 0.003, 0.005),
                       shade_mix=0.78, lift=(0.006, 0.005, 0.012), sky='day', sky_k=1.0, haze=None, grade_saturation=1.12, shaft_k=0.3, fill=0.0, gas=1.0),
    CORRIDOR_MORNING=dict(_IN, key=(1.50, 1.28, 0.95), key_dir=G._kd((0.15, -0.99), 30), sun_elev=30, sun_angle=0.8, shade=(0.075, 0.08, 0.12), shade_tint=(0.075, 0.085, 0.15), grade_offset=(0.001, 0.003, 0.005),
                          shade_mix=0.78, lift=(0.006, 0.005, 0.012), sky='day', sky_k=1.0, haze=None, grade_saturation=1.12, shaft_k=0.3, fill=0.0, gas=1.0),
    STREET_GOLDEN=dict(_IN, key=(1.75, 1.12, 0.55), key_dir=G._kd((-0.3, 0.95), 35), sun_elev=35, sun_angle=0.6, shade=(0.13, 0.13, 0.27), shade_tint=(0.15, 0.15, 0.34),
                       shade_mix=0.6, lift=(0.008, 0.006, 0.018), sky='day', sky_k=0.95, pano='day', pano_k=0.95, haze=('#ffd8a8', 0.10), grade_saturation=1.2, shaft_k=0.0, fill=0.0, gas=0.8),
    STREET_DUSK=dict(_IN, key=(1.35, 0.72, 0.42), key_dir=G._kd((0.2, -0.98), 8), sun_elev=8, sun_angle=1.0, shade=(0.11, 0.11, 0.26), shade_tint=(0.13, 0.13, 0.34),
                     shade_mix=0.6, lift=(0.008, 0.006, 0.02), sky='dusk', sky_k=0.95, pano='dusk', pano_k=0.9, haze=('#f0b890', 0.12), grade_saturation=1.2, shaft_k=0.0, fill=0.0, gas=1.2),
    ATTIC_DUSK=dict(_IN, key=(1.60, 1.10, 0.60), key_dir=G._kd((-0.25, -0.97), 14), sun_elev=14, sun_angle=1.0, shade=(0.055, 0.08, 0.15), shade_tint=(0.055, 0.095, 0.20), grade_offset=(0.001, 0.003, 0.005),
                    shade_mix=0.8, lift=(0.006, 0.005, 0.012), sky='dusk', sky_k=1.0, pano='dusk', pano_k=1.0, haze=None, grade_saturation=1.15, shaft_k=0.3, fill=0.0, gas=1.0),
    SHOP_DAY=dict(_IN, key=(1.60, 1.25, 0.80), key_dir=G._kd((-0.92, 0.38), 30), sun_elev=30, sun_angle=0.8, shade=(0.055, 0.08, 0.15), shade_tint=(0.055, 0.095, 0.20), grade_offset=(0.001, 0.003, 0.005),
                  shade_mix=0.8, lift=(0.006, 0.005, 0.012), sky='day', sky_k=1.0, haze=None, grade_saturation=1.15, shaft_k=0.28, fill=0.0, gas=1.0),
)
PRESETS = dict(
    gallery_wide=dict(loc='louvre', area='gallery', light='GALLERY_DAY', cam='gallery_wide', mona=True, queue=False),
    wall_eye=dict(loc='louvre', area='gallery', light='GALLERY_DAY', cam='wall_eye', mona=True, queue=False),
    empty_wall_queue=dict(loc='louvre', area='gallery', light='GALLERY_DAY', cam='empty_wall_queue', mona=False, queue=True),
    closet=dict(loc='louvre', area='closet', light='CLOSET_NIGHT', cam='closet'),
    staircase=dict(loc='louvre', area='stair', light='STAIR_MORNING', cam='staircase', frame_on_stairs=True),
    exit_door=dict(loc='louvre', area='exitdoor', light='CORRIDOR_MORNING', cam='exit_door', door=0.0),
    street_wide=dict(loc='paris', area='street', light='STREET_GOLDEN', cam='street_wide', papers=24),
    kiosk=dict(loc='paris', area='street', light='STREET_GOLDEN', cam='kiosk', papers=24),
    notre_dame_view=dict(loc='paris', area='street', light='STREET_DUSK', cam='notre_dame_view', papers=24),
    room_wide=dict(loc='room', area='attic', light='ATTIC_DUSK', cam='room_wide', trunk=(0.0, 0.0)),
    under_bed_insert=dict(loc='room', area='attic', light='ATTIC_DUSK', cam='under_bed_insert', trunk=(0.45, 0.0)),
    dealer_shop=dict(loc='room', area='shop', light='SHOP_DAY', cam='dealer_shop', panel=True),
)
LOC_PRESETS = dict(louvre=['gallery_wide', 'wall_eye', 'empty_wall_queue', 'closet', 'staircase', 'exit_door'],
                   paris=['street_wide', 'kiosk', 'notre_dame_view'], room=['room_wide', 'under_bed_insert', 'dealer_shop'])

# ----------------------------------------------------------------------------- build
def build(location='louvre', preset=None, clear=True, dress=True, light=None):
    """Build one location ('louvre' | 'paris' | 'room') for a preset (LOC_PRESETS) into the current scene: the preset's area only
    (one area per build keeps the lamp count, and the render cost, down), its light (light= overrides it with a LIGHTS key), world,
    render settings, grade, denoiser, and the preset's set state. Returns the anchors dict (louvre_API.md); A['cam'] is the preset camera."""
    preset = preset or LOC_PRESETS[location][0]
    assert preset in LOC_PRESETS[location], 'preset %s is not one of %s' % (preset, LOC_PRESETS[location])
    PR = PRESETS[preset]; lkey = light or PR['light']
    scene = bpy.context.scene; P = dict(LIGHTS[lkey]); STATE.clear(); STATE['P'] = P; STATE['preset'] = preset; STATE['loc'] = location; STATE['area'] = PR['area']; STATE['light'] = lkey
    if clear:
        for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for me in list(bpy.data.meshes):
        if me.users == 0: bpy.data.meshes.remove(me)
    for li in list(bpy.data.lights):
        if li.users == 0: bpy.data.lights.remove(li)
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    for m in list(bpy.data.materials):
        if m.name.startswith(('LVR_', 'ink')): bpy.data.materials.remove(m)
    tx = LT.ensure(verbose=False); STATE['tx'] = tx
    w = bpy.data.worlds.get('W_louvre') or bpy.data.worlds.new('W_louvre'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_current = 1
    pre = 'LVR_%s_%s_' % (PR['area'], lkey); FORM = tuple(P['form'])
    def _k(v): return 'x'.join('%g' % x for x in v) if isinstance(v, (tuple, list)) else '%g' % v
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        return _untoon(mat_lit('%sc_%s_%g_%s_%d_%s' % (pre, hexcol.lstrip('#'), gain, _k(sm), form, smix), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
    def TX(name, gain=1.0, sm=1.0, form=True, alpha=False, smix=None):
        """smix: per-material shade mix (saturated reds keep their own hue in shade - else red + blue shade reads magenta)."""
        return _untoon(mat_lit('%st_%s_%g_%s_%d_%d_%s' % (pre, name, gain, _k(sm), form, alpha, smix), image=tx[name], gain=gain, shade_mul=sm, form=FORM if form else None, alpha=alpha, shade_mix=smix))
    def E(name, image=None, hexcol='#ffffff', k=1.0, alpha=False): return mat_emit(pre + 'e_' + name + ('_' + image if image else ''), hexcol, image=tx[image] if image else None, strength=k, alpha=alpha)
    STATE.update(C=C, TX=TX, E=E, pre=pre)
    M = _materials(P, C, TX, E, tx, pre); STATE['M'] = M
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun); sun.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun.location = (-20, -40, 40); STATE['sun'] = sun
    STATE['flames'] = []; STATE['flame_mats'] = []; STATE['marks'] = {}; STATE['extra'] = {}
    dict(gallery=_gallery, closet=_closet, stair=_stair, exitdoor=_exitdoor, street=_street, attic=_attic, shop=_shop)[PR['area']](SET, P, M, dress)
    scene.cycles.use_light_tree = False
    MN._denoise(scene)
    setup_grade(scene)
    for ob in SET.objects: no_bounce(ob)
    set_flames(1.0)
    apply_preset_state(preset)
    A = anchors(); STATE['A'] = A
    return A

def setup_render(scene, quality='final'):
    """= mine.setup_render: final 720x1280 12 samples / preview 360x640 6, 2 threads, direct light only, OpenImageDenoise, light tree off.
    No depth of field."""
    MN.setup_render(scene, quality)

def apply_dof(cam_name=None, scene=None, cam=None):
    """Client rule: no depth of field at all (kept for API symmetry)."""
    return None

def _mat_glass(name, rgb=(0.85, 0.92, 1.0), k=0.12):
    """Picture glass / window glass: camera-only faint additive sheen (does not cast shadows, adds a cool glint)."""
    return BK._mat_add(name, STATE['tx']['glint'], rgb, k, node='glass_k')

def _materials(P, C, TX, E, tx, pre):
    gold = _glossy(TX('gold', form=False), (1.0, 0.85, 0.55), 0.55, 0.25)
    M = dict(gold=gold, gold_c=_glossy(C('#c89a3c', 1.0, (2.2, 1.5, 0.6)), (1.0, 0.85, 0.5), 0.6, 0.22), brass=_glossy(C('#c0923e', 1.0, (2.2, 1.5, 0.6)), (1.0, 0.82, 0.5), 0.5, 0.22),
             bronze=_glossy(C('#6a4a2a', 1.0, (1.6, 1.2, 0.7)), (1.0, 0.8, 0.5), 0.45, 0.3), iron=_glossy(C('#2e2c32', 1.0, 1.1), (1.0, 0.9, 0.8), 0.3, 0.3),
             damask=TX('damask_red', 1.0, (1.2, 0.8, 0.7), smix=0.3), damask_g=TX('damask_green'), damask_gold=TX('damask_gold'), damask_dk=TX('damask_red', 1.3, (1.2, 0.8, 0.7), smix=0.3), parquet=_glossy(TX('parquet', form=False), (1.0, 0.9, 0.75), 0.18, 0.3),
             frieze=TX('frieze'), coffer=TX('coffer'), marble=_glossy(TX('marble'), (1, 1, 1), 0.3, 0.12), marble_w=_glossy(TX('marble_w'), (1, 1, 1), 0.3, 0.12),
             skyglass=E('skyglass', 'skyglass', k=1.6), cream=C('#e8dcc0'), cream_d=C('#cfc0a0'), velvet=C('#a8301c', 1.0, (1.3, 0.75, 0.6), smix=0.1), velvet_d=C('#7a2414', 1.0, (1.3, 0.75, 0.6), smix=0.1), rope=C('#b8341c', 1.0, (1.3, 0.75, 0.6), smix=0.1),
             door_gal=TX('door_gal'), plaque=TX('plaque'), mona=TX('mona', form=False), cana=TX('cana', form=False),
             ashlar=TX('ashlar'), ashlar_d=TX('ashlar_d'), plaster=TX('plaster_s'), boards=TX('boards', form=False), shelf=TX('shelf_w'), crate=TX('crate'), rag=TX('rag'),
             flags=TX('flags_s', form=False), timber=TX('timber'), oak_door=TX('oak_door'), wood=C('#8a5e36'), wood_d=C('#5a3a22'), wood_l=C('#b08458'), zinc=_glossy(C('#9aa0a8'), (1, 1, 1), 0.5, 0.2),
             white=C('#f2eee4'), smock=C('#eeeae0'), black=C('#24222a'), red=C('#a83028', 1.0, (1.3, 0.75, 0.6), smix=0.1), green=C('#2e5a3a'), blue=C('#2e4a7a'), yellow=C('#e0b040'), straw=C('#d8b870'),
             glass=_mat_glass(pre + 'glass', (0.9, 0.95, 1.0), 0.35), dark=C('#1e1814', 1.0, 0.6, form=False),
             flame=mat_emit(pre + 'e_flame', '#ffa848', strength=6.0), flame_c=mat_emit(pre + 'e_flamec', '#fff2c4', strength=10.0),
             gasglobe=mat_emit(pre + 'e_globe', '#ffd890', strength=3.2), lamp_glass=mat_emit(pre + 'e_lampglass', '#ffc070', strength=2.6),
             halo=BK._mat_add(pre + 'halo', tx['pool'], (1.0, 0.62, 0.3), 0.55), halo_big=BK._mat_add(pre + 'halo_big', tx['pool'], (1.0, 0.58, 0.26), 0.9, node='fire_glow'),
             pool=BK._mat_add(pre + 'pool', tx['pool'], (1.0, 0.6, 0.3), 0.5, node='pool_k'),
             shaft=BK._mat_add(pre + 'shaft', tx['shaft'], tuple(c / max(P['key']) for c in P['key']), P.get('shaft_k', 0.15), node='shaft_k'),
             haus=[TX('haus%d' % k) for k in range(3)], haus_n=[TX('haus%d_n' % k) for k in range(3)], mansard=TX('mansard', alpha=True), cobbles=TX('cobbles', form=False), pave=TX('pave', form=False),
             seine=_glossy(C('#4a6a78', 1.0, 0.9), (1, 1, 1), 0.6, 0.06), morris=TX('morris'), kiosk=TX('kiosk'), awn_cafe=TX('awn_cafe', alpha=True), awn_green=TX('awn_green', alpha=True),
             sign_cafe=TX('sign_cafe'), sign_dealer=TX('sign_dealer'), sign_prive=TX('sign_prive'), stone_p=C('#e2d2b0'), horse=C('#6a4228'), horse_d=C('#3a2418'), cab=C('#1e2228'),
             wheel=C('#c8a040'), wallpaper=TX('wallpaper'), wallpaper_shop=TX('wallpaper_shop'), quilt=TX('quilt', 1.0, (1.1, 0.9, 0.8), smix=0.35), trunk=TX('trunk'), linen=C('#ece6d6'), pillow=C('#f4f0e6'),
             candle=C('#f2e8cc'), soap=C('#e8e0c0'), basin=_glossy(C('#f0ece4'), (1, 1, 1), 0.4, 0.15), books=[C(c) for c in ('#8a2a22', '#2a4a6a', '#3a5a2a', '#6a4a22', '#4a2a4a')])
    M['news'] = [TX('news%d' % k) for k in range(4)]; M['posters'] = [TX('poster_%s' % k) for k in ('mona', 'mona2', 'choc', 'cirque', 'velo', 'opera')]
    M['atlas'] = [TX('atlas%d' % k, form=False) for k in range(3)]
    STATE['flame_mats'] = [M['flame'], M['flame_c'], M['gasglobe'], M['lamp_glass']]
    return M

def _sky_dome(SET, P, M, E, R=140.0, pano=True):
    """Sky dome (R 140) and, outdoors, the painted Paris rooftop ring (R 120) and the warm haze rings (as bakery._sky)."""
    tx = STATE['tx']; mb = MB(); seg = 64; els = [-15 + 105 * k / 14 for k in range(15)]
    for i in range(seg):
        for k in range(14):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; e0, e1 = math.radians(els[k]), math.radians(els[k + 1])
            pts = [Vector((R * math.cos(e) * math.cos(a), R * math.cos(e) * math.sin(a), R * math.sin(e))) for (a, e) in ((a0, e0), (a1, e0), (a1, e1), (a0, e1))]
            mb.face(pts[::-1], E('sky', 'sky_' + P['sky'], k=P['sky_k']), [(i / seg, k / 14), ((i + 1) / seg, k / 14), ((i + 1) / seg, (k + 1) / 14), (i / seg, (k + 1) / 14)][::-1])
    _obj(mb, 'sky', SET, shadow=False)
    if pano and P.get('pano'):
        mb = MB(); Rp = LT.PANO_R; seg = 128
        for i in range(seg):
            a0, a1 = 2 * math.pi * i / seg, 2 * math.pi * (i + 1) / seg; u0, u1 = i / seg, (i + 1) / seg
            mb.face([Vector((Rp * math.cos(a0), Rp * math.sin(a0), LT.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), LT.PANO_Z0)), Vector((Rp * math.cos(a1), Rp * math.sin(a1), LT.PANO_Z1)), Vector((Rp * math.cos(a0), Rp * math.sin(a0), LT.PANO_Z1))],
                    mat_emit(STATE['pre'] + 'e_pano', image=tx['pano_' + P['pano']], strength=P['pano_k'], alpha=True), [(u0, 0), (u1, 0), (u1, 1), (u0, 1)])
        _obj(mb, 'backdrop', SET, shadow=False)
    if P.get('haze'):
        hm = G._haze_mat(STATE['pre'] + 'haze', P['haze'][0], P['haze'][1], 0.0, 30.0); mb = MB()
        for Rh in (40.0, 70.0, 100.0):
            for i in range(64):
                a0, a1 = 2 * math.pi * i / 64, 2 * math.pi * (i + 1) / 64
                mb.face([Vector((Rh * math.cos(a0), Rh * math.sin(a0), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), -1)), Vector((Rh * math.cos(a1), Rh * math.sin(a1), 40)), Vector((Rh * math.cos(a0), Rh * math.sin(a0), 40))], hm)
        _obj(mb, 'haze', SET, shadow=False)

def _flame_light(name, loc, rgb, energy, radius=0.12, shadow=False):
    """A point lamp registered for set_flames (flicker)."""
    ob = BK._light(name, loc, rgb, energy, radius=radius, shadow=shadow); STATE['flames'].append((ob, energy)); return ob

# ============================================================================= pictures and frames
def _canvas_pts(F, x0, z0, w, h, off, tilt=0.0):
    """Corners (bl, br, tr, tl) of a canvas in a wall frame: local x along the wall, local -y into the room. tilt (deg) leans the top
    forward (salon hang)."""
    t = math.sin(math.radians(tilt)) * h
    return [F.p(x0, -off, z0), F.p(x0 + w, -off, z0), F.p(x0 + w, -off - t, z0 + h * math.cos(math.radians(tilt))), F.p(x0, -off - t, z0 + h * math.cos(math.radians(tilt)))]

def _frame_geo(mb, pts, n, fw, fd, mat, back=0.06, tile=2.0):
    """Mitred gilded frame round the canvas corners pts (bl, br, tr, tl), n = outward normal: an outer cove (v 0..0.5) rising from the
    outer edge to a ridge fd proud, an inner slope (v 0.5..1) down to the sight edge; the outer side back to the wall."""
    n = Vector(n).normalized(); c = sum(pts, Vector()) / 4
    P = [Vector(p) for p in pts]
    def offset(i, d):
        a = P[i]; e_out, e_in = (P[(i + 1) % 4] - a).normalized(), (a - P[i - 1]).normalized()
        bis = (e_in - e_out); bis = (bis - n * bis.dot(n)).normalized()
        s = 1.0 / max(0.3, math.sin(math.acos(max(-1.0, min(1.0, -e_in.dot(e_out)))) / 2))
        return a + bis * d * s
    ring_in = [p + n * 0.02 for p in P]; ring_mid = [offset(i, fw * 0.55) + n * fd for i in range(4)]; ring_out = [offset(i, fw) + n * fd * 0.45 for i in range(4)]
    ring_back = [offset(i, fw) - n * back for i in range(4)]
    for i in range(4):
        j = (i + 1) % 4; L_ = (P[j] - P[i]).length / tile
        mb.oface([ring_out[i], ring_out[j], ring_mid[j], ring_mid[i]], mat, [(0, 0.0), (L_, 0.0), (L_, 0.5), (0, 0.5)], n)
        mb.oface([ring_mid[i], ring_mid[j], ring_in[j], ring_in[i]], mat, [(0, 0.5), (L_, 0.5), (L_, 1.0), (0, 1.0)], n)
        side = (ring_out[i] + ring_out[j]) / 2 - c; side = side - n * side.dot(n)
        mb.oface([ring_back[i], ring_back[j], ring_out[j], ring_out[i]], mat, [(0, 0.0), (L_, 0.0), (L_, 0.12), (0, 0.12)], side)

def _uv_crop(cell, aspect, n=4):
    """UVs (bl, br, tr, tl) of the largest centred crop of atlas cell `cell` with this aspect (w / h)."""
    cx, cy = cell % n, cell // n; u0, u1 = cx / n, (cx + 1) / n; v1, v0 = 1 - cy / n, 1 - (cy + 1) / n
    if aspect >= 1: hh = (v1 - v0) / aspect / 2; vm = (v0 + v1) / 2; v0, v1 = vm - hh, vm + hh
    else: hw = (u1 - u0) * aspect / 2; um = (u0 + u1) / 2; u0, u1 = um - hw, um + hw
    return [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

def _picture(cmb, fmb, F, x0, z0, w, h, M, cell, off=0.1, tilt=0.0, fw=None, fd=None, mat=None, uvs=None):
    pts = _canvas_pts(F, x0, z0, w, h, off, tilt); n = (pts[1] - pts[0]).cross(pts[3] - pts[0]).normalized()
    if n.dot(-F.Y) < 0: n = -n
    if mat is None: mat = M['atlas'][cell // 16]; uvs = _uv_crop(cell % 16, w / h)
    cmb.oface(pts, mat, uvs, n)
    fw = fw or max(0.12, min(0.42, 0.09 * (w + h))); fd = fd or fw * 0.6
    _frame_geo(fmb, pts, n, fw, fd, M['gold'])
    return pts, n

def _salon_hang(cmb, fmb, F, u0, u1, z0, z1, M, seed, reserved=(), rows=None, tilt_above=9.0):
    """Floor-to-ceiling salon hang on a wall frame: rows of gilt-framed pictures of varied sizes, gaps 0.25, skipping the reserved
    (x0, x1, z0, z1) rects; the rows above z = tilt_above lean forward 6 deg. Returns the placed pictures [(x0, z0, w, h)]."""
    r = _rnd(seed); out = []; z = z0; cell = r.randrange(48)
    while z < z1 - 0.8:
        rh = min(r.choice((1.3, 1.6, 2.0, 2.4, 2.8)), z1 - z - 0.2)
        x = u0 + r.uniform(0.1, 0.5)
        while x < u1 - 0.8:
            w = min(r.choice((0.9, 1.2, 1.5, 1.8, 2.2, 2.8, 3.4)) * (rh / 2.0) ** 0.5, u1 - x - 0.15)
            h = rh * r.uniform(0.82, 1.0); zz = z + (rh - h) / 2
            fwid = max(0.12, min(0.36, 0.08 * (w + h)))
            bx0, bx1, bz0, bz1 = x - fwid, x + w + fwid, zz - fwid, zz + h + fwid
            if w > 0.6 and not any(bx1 > a and bx0 < b and bz1 > c and bz0 < d for (a, b, c, d) in reserved):
                _picture(cmb, fmb, F, x, zz, w, h, M, cell % 48, off=0.08, tilt=6.0 if zz > tilt_above else 0.0, fw=fwid)
                out.append((x, zz, w, h)); cell += 7
                x += w + 2 * fwid + 0.22
            else:
                x += 0.4
        z += rh + 0.5
    return out

# ============================================================================= LOUVRE: the Salon Carre
def _gallery(SET, P, M, dress):
    x0, x1, y0, y1 = GAL; tx = STATE['tx']
    # ---- floor, walls (marble dado, damask), cornice, coved ceiling with coffers, laylight with the skylight
    mb = MB(); mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['parquet'], (x0 / 4, y0 / 4, x1 / 4, y1 / 4)); _obj(mb, 'floor', SET)
    walls = [Frame((x0, y1, 0), 0.0), Frame((x1, y1, 0), -90.0), Frame((x1, y0, 0), 180.0), Frame((x0, y0, 0), 90.0)]       # back, right, front, left (local x along, -y into the room)
    STATE['walls'] = walls; wl = MB(); cr = MB()
    for k, F in enumerate(walls):
        L_ = (x1 - x0) if k % 2 == 0 else (y1 - y0)
        F.quad(wl, [(0, 0, 0), (L_, 0, 0), (L_, 0, 1.25), (0, 0, 1.25)], M['marble'], [(0, 0), (L_ / 2, 0), (L_ / 2, 0.62), (0, 0.62)], (0, -1, 0))
        F.quad(wl, [(0, 0, 1.25), (L_, 0, 1.25), (L_, 0, GAL_H), (0, 0, GAL_H)], M['damask'], [(0, 0), (L_ / 1.0, 0), (L_ / 1.0, (GAL_H - 1.25) / 1.4), (0, (GAL_H - 1.25) / 1.4)], (0, -1, 0))
        F.box(cr, (0, -0.25, 1.15), (L_, 0, 1.38), M['marble_w'], 0.5)                                                 # dado rail
        F.box(cr, (0, -0.18, 0), (L_, 0, 0.3), M['marble_w'], 0.5)                                                      # skirting
        F.quad(cr, [(0, -0.3, GAL_H), (L_, -0.3, GAL_H), (L_, -0.3, GAL_H + 1.0), (0, -0.3, GAL_H + 1.0)], M['frieze'], [(0, 0), (L_ / 4, 0), (L_ / 4, 1), (0, 1)], (0, -1, 0))
        F.box(cr, (0, -0.45, GAL_H - 0.12), (L_, 0, GAL_H), M['gold_c'], 0.5)
        F.box(cr, (0, -0.75, GAL_H + 1.0), (L_, 0, CORN), M['cream'], 0.5)                                             # cornice
        F.box(cr, (0, -0.95, CORN - 0.12), (L_, 0, CORN), M['gold_c'], 0.5)
        F.quad(cr, [(0, -0.75, CORN), (L_, -0.75, CORN), (L_ - 2.7, -2.7, LAY_Z), (2.7, -2.7, LAY_Z)], M['coffer'], [(0, 0), (L_ / 2, 0), ((L_ - 2.7) / 2, 1.5), (1.35, 1.5)], (0, -1, -1))   # the cove
    _obj(wl, 'walls', SET); _obj(cr, 'cornice', SET)                       # no ink hull up there (cost; the gilt edges read anyway)
    # flat laylight ceiling round the opening, the opening's well and the glass lantern above
    ce = MB(); a, b, c_, d = SKY_OPEN; xi0, xi1, yi0, yi1 = x0 + 2.7, x1 - 2.7, y0 + 2.7, y1 - 2.7
    for (p0, p1) in (((xi0, yi0), (xi1, c_)), ((xi0, d), (xi1, yi1)), ((xi0, c_), (a, d)), ((b, c_), (xi1, d))):
        ce.quad((p0[0], p0[1], LAY_Z), (0, p1[1] - p0[1], 0), (p1[0] - p0[0], 0, 0), M['coffer'], (0, 0, (p1[1] - p0[1]) / 2, (p1[0] - p0[0]) / 2))
    for (pa, pb) in (((a, c_), (b, c_)), ((b, c_), (b, d)), ((b, d), (a, d)), ((a, d), (a, c_))):
        ce.oface([(pa[0], pa[1], LAY_Z), (pb[0], pb[1], LAY_Z), (pb[0], pb[1], LAY_Z + 2.4), (pa[0], pa[1], LAY_Z + 2.4)], M['cream_d'], [(0, 0), (1, 0), (1, 0.3), (0, 0.3)], Vector(((a + b) / 2 - (pa[0] + pb[0]) / 2, (c_ + d) / 2 - (pa[1] + pb[1]) / 2, 0)))
    ce.box((a - 0.3, c_ - 0.3, LAY_Z - 0.25), (b + 0.3, c_, LAY_Z), M['gold_c']); ce.box((a - 0.3, d, LAY_Z - 0.25), (b + 0.3, d + 0.3, LAY_Z), M['gold_c'])
    ce.box((a - 0.3, c_, LAY_Z - 0.25), (a, d, LAY_Z), M['gold_c']); ce.box((b, c_, LAY_Z - 0.25), (b + 0.3, d, LAY_Z), M['gold_c'])
    _obj(ce, 'ceiling', SET)
    gl = MB(); gl.quad((a, c_, LAY_Z + 2.4), (b - a, 0, 0), (0, d - c_, 0), M['skyglass'], (0, 0, (b - a) / 2, (d - c_) / 2)); o = _obj(gl, 'skylight_glass', SET, shadow=False)
    bars = MB()                                                                                                    # iron glazing bars (cast the patterned shadow)
    for i in range(1, 8): x = a + (b - a) * i / 8; bars.box((x - 0.07, c_, LAY_Z + 2.2), (x + 0.07, d, LAY_Z + 2.35), M['iron'])
    for j in range(1, 6): y = c_ + (d - c_) * j / 6; bars.box((a, y - 0.06, LAY_Z + 2.2), (b, y + 0.06, LAY_Z + 2.35), M['iron'])
    _obj(bars, 'skylight_bars', SET)
    # ---- the pictures
    cm = MB(); fm = MB(); hung = {}
    mc = MONA_C; mona_res = (-1.5, 1.5, 1.3, 6.2)
    reserved_back = [mona_res]
    hung['back'] = _salon_hang(cm, fm, walls[0], 0.4, (x1 - x0) - 0.4, 1.7, GAL_H - 0.4, M, 101, reserved=[(r_[0] - x0, r_[1] - x0, r_[2], r_[3]) for r_ in reserved_back])
    # the two pictures flanking her (as in 1911: a Correggio and a Titian), a bit bigger, at her height
    hung['right'] = _salon_hang(cm, fm, walls[1], 0.4, (y1 - y0) - 0.4, 1.7, GAL_H - 0.4, M, 202)
    sd = SERVICE_DOOR
    hung['front'] = _salon_hang(cm, fm, walls[2], 0.4, (x1 - x0) - 0.4, 1.7, GAL_H - 0.4, M, 303, reserved=[(x1 - sd[1] - 0.6, x1 - sd[0] + 0.6, 0, sd[3] + 1.6)])
    # left wall: the huge Venetian feast at the centre, salon hang round it
    F = walls[3]; cw, ch = 12.0, 8.0; cx0 = (y1 - y0) / 2 - cw / 2
    _picture(cm, fm, F, cx0, 2.6, cw, ch, M, 0, off=0.12, fw=0.55, fd=0.35, mat=M['cana'], uvs=[(0, 0), (1, 0), (1, 1), (0, 1)])
    hung['left'] = _salon_hang(cm, fm, F, 0.4, (y1 - y0) - 0.4, 1.7, GAL_H - 0.4, M, 404, reserved=[(cx0 - 0.9, cx0 + cw + 0.9, 1.5, 2.6 + ch + 0.9)])
    _obj(cm, 'pictures', SET); _obj(fm, 'frames', SET, hull=0.012)
    STATE['hung'] = hung
    _mona(SET, M)
    # ---- the service door in the front wall (painted double door, one leaf ajar), its gilt architrave
    F = walls[2]; dm = MB(); u0, u1 = x1 - sd[1], x1 - sd[0]
    F.quad(dm, [(u0, -0.02, 0), (u1, -0.02, 0), (u1, -0.02, sd[3]), (u0, -0.02, sd[3])], M['door_gal'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    F.box(dm, (u0 - 0.3, -0.18, 0), (u0, 0, sd[3] + 0.3), M['gold_c']); F.box(dm, (u1, -0.18, 0), (u1 + 0.3, 0, sd[3] + 0.3), M['gold_c'])
    F.box(dm, (u0 - 0.45, -0.3, sd[3] + 0.3), (u1 + 0.45, 0, sd[3] + 0.75), M['cream']); F.box(dm, (u0 - 0.55, -0.4, sd[3] + 0.75), (u1 + 0.55, 0, sd[3] + 0.88), M['gold_c'])
    _obj(dm, 'service_door', SET, hull=0.015)
    if dress: _gallery_dressing(SET, P, M)
    _gallery_lights(SET, P, M)

def _mona(SET, M):
    """The Mona Lisa: canvas + gilt frame + her glass (the box Peruggia fitted), on a pivot (set_mona_lift); the four iron hooks on
    the wall (always there); the unfaded damask patch where she hung (seen when she is gone); the brass plaque below."""
    F = STATE['walls'][0]; x1 = GAL[1]; cx, cy, cz = MONA_C; ux = cx - GAL[0]
    piv = G._pivot('mona_pivot', STATE['SET'], (cx, cy, cz))
    cm = MB(); fm = MB()
    pts, n = _picture(cm, fm, F, ux - MONA_W / 2, cz - MONA_H / 2, MONA_W, MONA_H, M, 0, off=0.2, fw=MONA_FW, fd=0.14, mat=M['mona'], uvs=[(0, 0), (1, 0), (1, 1), (0, 1)])
    gb = MB()                                                                                                      # glass box: front glass + its thin dark edges
    g = [p - Vector((0, 0.12, 0)) for p in pts]
    gb.oface(g, M['glass'], [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], n)
    fm.box((cx - MONA_W / 2 - MONA_FW - 0.05, cy - 0.38, cz - MONA_H / 2 - MONA_FW - 0.05), (cx + MONA_W / 2 + MONA_FW + 0.05, cy - 0.3, cz - MONA_H / 2 - MONA_FW), M['bronze'])
    objs = [_obj(cm, 'mona_canvas', SET), _obj(fm, 'mona_frame', SET, hull=0.01), _obj(gb, 'mona_glass', SET, shadow=False)]
    for o in objs: G._parent(o, piv)
    STATE['mona'] = dict(pivot=piv, objs=objs)
    hk = MB()
    for (hx, hz) in HOOKS:
        p = Vector((cx + hx, cy, hz)); rod(hk, p, p - Vector((0, 0.2, 0)), 0.05, M['iron'], seg=6); rod(hk, p - Vector((0, 0.2, 0)), p - Vector((0, 0.2, -0.16)), 0.045, M['iron'], seg=6)
        hk.box((cx + hx - 0.09, cy - 0.03, hz - 0.11), (cx + hx + 0.09, cy, hz + 0.11), M['iron'])
    _obj(hk, 'mona_hooks', SET, hull=0.006)
    pa = MB(); w2, h2 = MONA_W / 2 + MONA_FW + 0.04, MONA_H / 2 + MONA_FW + 0.04
    pa.quad((cx - w2, cy - 0.012, cz - h2), (2 * w2, 0, 0), (0, 0, 2 * h2), M['damask_dk'], (0, 0, 2 * w2, 2 * h2 / 1.4))
    for (lo, hi) in (((cx - w2, cy - 0.03, cz - h2), (cx + w2, cy - 0.012, cz - h2 + 0.05)), ((cx - w2, cy - 0.03, cz + h2 - 0.05), (cx + w2, cy - 0.012, cz + h2)),
                     ((cx - w2, cy - 0.03, cz - h2), (cx - w2 + 0.05, cy - 0.012, cz + h2)), ((cx + w2 - 0.05, cy - 0.03, cz - h2), (cx + w2, cy - 0.012, cz + h2))):
        pa.box(lo, hi, M['dark'])                                                                                    # the dust line round the unfaded patch
    STATE['mona']['patch'] = _obj(pa, 'mona_patch', SET)
    pl = MB(); pl.quad((cx - 0.3, cy - 0.03, cz - MONA_H / 2 - MONA_FW - 0.45), (0.6, 0, 0), (0, 0, 0.2), M['plaque'], (0, 0, 1, 1)); _obj(pl, 'mona_plaque', SET)

def _gallery_dressing(SET, P, M):
    """Central round velvet divan with a bronze urn, two long benches, the velvet rope on brass stanchions before her, the queue lanes
    (set_queue), the guard's chair, two bronze gas torcheres with frosted globes, an easel (the copyist), a picture ladder."""
    mb = MB(); fl = MB(); cards = MB(); rr = _rnd(31)
    c = Vector((0.0, 10.0, 0))
    rod(mb, c, c + Vector((0, 0, 0.35)), 1.9, M['wood_d'], seg=24); rod(mb, c + Vector((0, 0, 0.35)), c + Vector((0, 0, 1.0)), 1.8, M['velvet'], seg=24, r1=1.75)
    lumpy(mb, c + Vector((0, 0, 1.0)), 1.72, M['velvet'], 51, seg=24, rings=4, rough=0.02, squash=0.12)
    rod(mb, c, c + Vector((0, 0, 2.3)), 0.75, M['velvet_d'], seg=18, r1=0.6)
    for k in range(12):
        a = 2 * math.pi * k / 12; mb.sphere(c + Vector((1.78 * math.cos(a), 1.78 * math.sin(a), 0.7)), 0.06, M['gold_c'], seg=6, rings=3)
    rod(mb, c + Vector((0, 0, 2.3)), c + Vector((0, 0, 2.5)), 0.45, M['bronze'], seg=14); lumpy(mb, c + Vector((0, 0, 3.0)), 0.6, M['bronze'], 52, seg=14, rings=6, rough=0.03, squash=1.1)
    rod(mb, c + Vector((0, 0, 3.4)), c + Vector((0, 0, 3.8)), 0.35, M['bronze'], seg=14, r1=0.5)
    for (bx, by) in ((-7.5, 6.0), (7.5, 6.0)):                                                                   # benches
        mb.box((bx - 2.0, by - 0.6, 0.6), (bx + 2.0, by + 0.6, 0.95), M['velvet']); mb.box((bx - 2.05, by - 0.65, 0.5), (bx + 2.05, by + 0.65, 0.6), M['gold_c'])
        for sx in (-1.8, 1.8):
            for sy in (-0.45, 0.45): rod(mb, (bx + sx, by + sy, 0), (bx + sx, by + sy, 0.5), 0.07, M['gold_c'], seg=6, r1=0.05)
    # brass stanchions + red rope before her
    ys = 20.4; xs = [-2.6, -0.9, 0.9, 2.6]; STATE['rope_main'] = []
    for x in xs: _stanchion(mb, (x, ys, 0), M)
    for xa, xb in zip(xs, xs[1:]): chain_rod(mb, catenary((xa, ys, 2.25), (xb, ys, 2.25), 0.35, 8), 0.06, M['rope'], seg=6)
    # guard's chair by the service door
    ch = Vector((6.6, 1.2, 0)); mb.box((ch.x - 0.5, ch.y - 0.5, 1.0), (ch.x + 0.5, ch.y + 0.5, 1.2), M['velvet']); mb.box((ch.x - 0.5, ch.y - 0.6, 1.2), (ch.x + 0.5, ch.y - 0.45, 2.6), M['wood_d'])
    for sx in (-0.42, 0.42):
        for sy in (-0.42, 0.42): rod(mb, (ch.x + sx, ch.y + sy, 0), (ch.x + sx, ch.y + sy, 1.0), 0.05, M['wood_d'], seg=6)
    # gas torcheres (bronze shaft on a marble plinth, five frosted globes) - the warm emitters of the gallery
    STATE['torch'] = []
    for (tx_, ty) in ((-5.2, 20.6), (5.2, 20.6), (-11.6, 2.4), (11.6, 12.0)):
        b = Vector((tx_, ty, 0)); mb.box((tx_ - 0.5, ty - 0.5, 0), (tx_ + 0.5, ty + 0.5, 1.4), M['marble'])
        rod(mb, b + Vector((0, 0, 1.4)), b + Vector((0, 0, 1.7)), 0.35, M['bronze'], seg=12, r1=0.2)
        rod(mb, b + Vector((0, 0, 1.7)), b + Vector((0, 0, 5.4)), 0.11, M['bronze'], seg=10, r1=0.08)
        for z in (2.6, 4.0): rod(mb, b + Vector((0, 0, z)), b + Vector((0, 0, z + 0.2)), 0.18, M['gold_c'], seg=10)
        top = b + Vector((0, 0, 5.6)); fl.sphere(top + Vector((0, 0, 0.25)), 0.32, M['gasglobe'], seg=12, rings=6)
        for k in range(4):
            a = 2 * math.pi * k / 4 + 0.4; q = b + Vector((0.75 * math.cos(a), 0.75 * math.sin(a), 5.1))
            rod(mb, b + Vector((0, 0, 5.0)), q, 0.04, M['bronze'], seg=5); fl.sphere(q + Vector((0, 0, 0.22)), 0.22, M['gasglobe'], seg=10, rings=5)
            _halo(cards, q + Vector((0, 0, 0.22)), 0.55, M)
        _halo(cards, top + Vector((0, 0, 0.25)), 0.9, M); STATE['torch'].append(top + Vector((0, 0, 0.2)))
    # the copyist's easel (left of the divan) with a canvas on it, a stool; a library ladder against the right wall
    e = Vector((-6.2, 13.5, 0))
    for (dx, dy) in ((-0.5, -0.3), (0.5, -0.3), (0.0, 0.5)): beam(mb, e + Vector((dx, dy, 0)), e + Vector((dx * 0.2, dy * 0.2 + 0.05, 4.4)), 0.07, 0.07, M['wood'])
    mb.box((e.x - 0.75, e.y - 0.42, 1.9), (e.x + 0.75, e.y - 0.3, 1.98), M['wood'])
    cmb = MB(); cmb.oface([(e.x - 0.7, e.y - 0.36, 1.98), (e.x + 0.7, e.y - 0.36, 1.98), (e.x + 0.7, e.y - 0.25, 3.6), (e.x - 0.7, e.y - 0.25, 3.6)], M['atlas'][1], _uv_crop(5, 1.4 / 1.6), (0, -1, 0.05))
    rod(mb, (e.x + 0.9, e.y - 1.0, 0), (e.x + 0.9, e.y - 1.0, 1.0), 0.35, M['wood_d'], seg=10)
    lx = GAL[1] - 0.5
    for s in (-0.5, 0.5): beam(mb, (lx - 1.6, 16.0 + s, 0), (lx - 0.1, 16.0 + s, 9.0), 0.1, 0.1, M['wood'])
    for k in range(1, 14): t = k / 14; rod(mb, (lx - 1.6 + 1.5 * t, 15.5, 9.0 * t), (lx - 1.6 + 1.5 * t, 16.5, 9.0 * t), 0.04, M['wood'], seg=5)
    _obj(mb, 'gallery_dressing', SET, hull=0.012); _obj(fl, 'gallery_globes', SET, shadow=False); _obj(cards, 'gallery_halos', SET, shadow=False); _obj(cmb, 'easel_canvas', SET)
    # the queue lanes (reopening day): two more rope lines making a lane to the empty wall
    qb = MB(); lanes = []
    for x in (-2.6, 2.6):
        ys_ = [20.4, 17.5, 14.6]; lanes.append(ys_)
        for y in ys_[1:]: _stanchion(qb, (x, y, 0), M)
        for ya, yb in zip(ys_, ys_[1:]): chain_rod(qb, catenary((x, ya, 2.25), (x, yb, 2.25), 0.35, 8), 0.06, M['rope'], seg=6)
    STATE['queue_obj'] = _obj(qb, 'queue_ropes', SET, hull=0.01)

def _stanchion(mb, p, M):
    p = Vector(p); rod(mb, p, p + Vector((0, 0, 0.08)), 0.32, M['brass'], seg=12); rod(mb, p + Vector((0, 0, 0.08)), p + Vector((0, 0, 2.2)), 0.06, M['brass'], seg=8)
    mb.sphere(p + Vector((0, 0, 2.3)), 0.12, M['brass'], seg=8, rings=4)

def _gallery_lights(SET, P, M):
    """Sun through the skylight (patterned by the bars), a broad warm skylight fill (no shadow), the four torcheres (flicker), and
    camera-only sun shafts slanting from the opening."""
    a, b, c_, d = SKY_OPEN; fk = P.get('fill', 1.0)
    L1 = BK._light('sky_fill', (0.0, 12.0, 12.0), (1.0, 0.86, 0.66), 2600 * fk, radius=4.0, shadow=False)
    L2 = BK._light('sky_fill_front', (0.0, 3.0, 9.0), (1.0, 0.8, 0.6), 700 * fk, radius=3.0, shadow=False)
    for i, t in enumerate(STATE.get('torch', [])): _flame_light('torch_%d' % i, tuple(t), GAS, 140 * P.get('gas', 1.0), radius=0.5, shadow=i < 2)
    kd = Vector(P['key_dir']).normalized(); sb = MB()
    def ext(p): t = (p.z - 0.0) / max(0.05, -kd.z); return p + kd * t
    for k in range(2):                                                                                              # 2 sheets: each costs ~0.9 CPU s
        x = a + 3.5 + k * (b - a - 7.0)
        p0, p1 = Vector((x, c_ + 1.0, LAY_Z + 2.3)), Vector((x, d - 1.0, LAY_Z + 2.3)); q0, q1 = ext(p0), ext(p1)
        sb.face([p0, p1, q1, q0], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sb, 'sun_shafts', SET, shadow=False)
    _sky_dome(SET, P, M, STATE['E'], pano=False)

# ============================================================================= LOUVRE: the service rooms
def _box_room(SET, name, x0, x1, y0, y1, h, M, wall='plaster', floor='boards', ceil='boards', skip=()):
    mb = MB()
    mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M[floor], (x0 / 2, y0 / 2, x1 / 2, y1 / 2))
    mb.quad((x0, y1, h), (x1 - x0, 0, 0), (0, -(y1 - y0), 0), M[ceil], (0, 0, (x1 - x0) / 2, (y1 - y0) / 2))
    for (pts, n, L_, k) in (([(x0, y1, 0), (x1, y1, 0), (x1, y1, h), (x0, y1, h)], (0, -1, 0), x1 - x0, 'back'), ([(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)], (0, 1, 0), x1 - x0, 'front'),
                            ([(x0, y0, 0), (x0, y1, 0), (x0, y1, h), (x0, y0, h)], (1, 0, 0), y1 - y0, 'left'), ([(x1, y0, 0), (x1, y1, 0), (x1, y1, h), (x1, y0, h)], (-1, 0, 0), y1 - y0, 'right')):
        if k in skip: continue
        mb.oface(pts, M[wall], [(0, 0), (L_ / 4, 0), (L_ / 4, h / 4), (0, h / 4)], n)
    return _obj(mb, name, SET)

def _lantern(mb, fl, cards, p, M, hang=True, s=1.0):
    """Hurricane / storm lantern: tin base and cap, glowing glass chimney (emission), wire guard, bail; returns the flame centre."""
    p = Vector(p)
    rod(mb, p, p + Vector((0, 0, 0.12 * s)), 0.22 * s, M['zinc'], seg=12); rod(mb, p + Vector((0, 0, 0.62 * s)), p + Vector((0, 0, 0.72 * s)), 0.2 * s, M['zinc'], seg=12, r1=0.08 * s)
    fl.frustum(p + Vector((0, 0, 0.12 * s)), p + Vector((0, 0, 0.62 * s)), 0.13 * s, 0.1 * s, M['lamp_glass'], seg=10)
    for k in range(4):
        a = 2 * math.pi * k / 4 + 0.3; rod(mb, p + Vector((0.2 * s * math.cos(a), 0.2 * s * math.sin(a), 0.12 * s)), p + Vector((0.17 * s * math.cos(a), 0.17 * s * math.sin(a), 0.62 * s)), 0.012, M['zinc'], seg=4)
    if hang: chain_rod(mb, [p + Vector((-0.2 * s, 0, 0.72 * s)), p + Vector((0, 0, 1.0 * s)), p + Vector((0.2 * s, 0, 0.72 * s))], 0.012, M['iron'])
    f = p + Vector((0, 0, 0.38 * s)); _halo(cards, f, 0.7 * s, M)
    return f

def _gas_bracket(mb, fl, cards, p, n, M, s=1.0):
    """Wall gas bracket: a brass arm from a rose on the wall, a frosted tulip globe (emission); returns the glow centre."""
    p = Vector(p); n = Vector(n).normalized()
    rod(mb, p, p + n * 0.05, 0.14 * s, M['brass'], seg=10); q = p + n * 0.55 * s + Vector((0, 0, 0.15 * s))
    chain_rod(mb, [p + n * 0.05, p + n * 0.35 * s, q - Vector((0, 0, 0.1 * s))], 0.03 * s, M['brass'], seg=6)
    rod(mb, q - Vector((0, 0, 0.12 * s)), q, 0.07 * s, M['brass'], seg=8)
    fl.frustum(q, q + Vector((0, 0, 0.32 * s)), 0.1 * s, 0.2 * s, M['gasglobe'], seg=10)
    f = q + Vector((0, 0, 0.18 * s)); _halo(cards, f, 0.8 * s, M)
    return f

def _smock(mb, top, M, seed, s=1.0):
    """A white worker's smock hanging from a peg: a lumpy cloth body and two sleeves."""
    top = Vector(top); r = _rnd(seed); X = Vector((0, 1, 0)); Y = Vector((1, 0, 0)); Z = Vector((0, 0, 1))
    mb.frustum(top - Vector((0, 0, 0.08)), top - Vector((0, 0, 1.9 * s)), 0.28 * s, 0.55 * s, M['smock'], seg=8)          # the tunic, flaring to the hem
    for sx in (-1, 1): rod(mb, top + Vector((0, sx * 0.25 * s, -0.12 * s)), top + Vector((0.05, sx * 0.5 * s, -1.1 * s)), 0.13 * s, M['smock'], seg=6, r1=0.15 * s)
    rod(mb, top - Vector((0, 0, 0.1)), top + Vector((0, 0, 0.0)), 0.12 * s, M['smock'], seg=8)
    rod(mb, top + Vector((0.15, 0, 0.05)), top + Vector((-0.1, 0, 0.05)), 0.04, M['wood_d'], seg=6)

def _closet(SET, P, M, dress):
    """The storage closet where he hid on Sunday night: 4.4 x 3.2 D, 6 high; shelves of paint tins, jars and rags, brooms and mops,
    zinc buckets, crates, a ladder, white smocks on pegs, a stub of candle; a storm lantern on a crate is the only light (warm,
    flickering); a thin line of gaslight under the door."""
    x0, x1, y0, y1, h = -2.6, 2.6, 0.0, 3.6, 6.0
    _box_room(SET, 'closet_room', x0, x1, y0, y1, h, M)
    mb = MB(); fl = MB(); cards = MB(); rr = _rnd(41)
    for z in (2.2, 3.3, 4.4, 5.4):                                                                                  # shelves on the back wall
        mb.box((x0 + 0.05, y1 - 0.75, z - 0.08), (x1 - 0.05, y1, z), M['shelf'], tile=(2, 2))
        x = x0 + 0.3
        while x < x1 - 0.3:
            k = rr.random()
            if k < 0.35: rod(mb, (x, y1 - 0.4, z), (x, y1 - 0.4, z + 0.42), 0.16, rr.choice((M['zinc'], M['red'], M['blue'], M['green'])), seg=10); x += 0.4
            elif k < 0.6: rod(mb, (x, y1 - 0.4, z), (x, y1 - 0.4, z + 0.5), 0.1, rr.choice((M['glass'], M['green'], M['white'])), seg=8, r1=0.06); x += 0.28
            elif k < 0.8: lumpy(mb, (x + 0.1, y1 - 0.4, z + 0.15), 0.25, M['rag'], int(x * 100 + z * 10), seg=8, rings=4, rough=0.25, squash=0.6); x += 0.55
            else: mb.box((x, y1 - 0.65, z), (x + 0.5, y1 - 0.15, z + 0.35), M['crate'], tile=(1, 1)); x += 0.6
    for x in (x0 + 0.1, x1 - 0.1): mb.box((x - 0.05, y1 - 0.8, 0), (x + 0.05, y1 - 0.7, 5.6), M['wood_d'])
    # brooms and mops leaning in the left corner
    for k, (bx, by, lean) in enumerate(((x0 + 0.35, 0.6, 0.25), (x0 + 0.55, 1.0, 0.18), (x0 + 0.3, 1.5, 0.3), (x0 + 0.5, 2.0, 0.2))):
        top = Vector((bx - lean, by, 4.6)); bot = Vector((bx + 0.15, by, 0.05)); beam(mb, bot, top, 0.06, 0.06, M['wood_l'])
        if k % 2 == 0: lumpy(mb, bot + Vector((0, 0, 0.3)), 0.28, M['straw'], 60 + k, seg=8, rings=4, rough=0.3, squash=1.5)
        else: lumpy(mb, bot + Vector((0, 0, 0.25)), 0.3, M['rag'], 70 + k, seg=8, rings=4, rough=0.35, squash=1.2)
    for (bx, by) in ((x1 - 0.6, 0.7), (x1 - 0.55, 1.5), (0.4, 2.0)):                                                # zinc buckets
        rod(mb, (bx, by, 0), (bx, by, 0.7), 0.32, M['zinc'], seg=12, r1=0.38); chain_rod(mb, [(bx - 0.36, by, 0.7), (bx, by, 1.05), (bx + 0.36, by, 0.7)], 0.015, M['iron'])
    mb.box((-1.4, 1.8, 0), (0.2, 3.0, 1.1), M['crate'], tile=(1, 1)); mb.box((-1.2, 2.0, 1.1), (-0.1, 2.9, 1.9), M['crate'], tile=(1, 1))
    mb.box((0.6, 2.2, 0), (1.9, 3.1, 0.9), M['crate'], tile=(1, 1))
    for k, px in enumerate((x1 - 0.2, )): pass
    for k, (px, py) in enumerate(((x0, 2.6), (x0, 3.2))):                                                        # smocks on pegs (left wall, behind the brooms)
        _smock(mb, (x0 + 0.3, py, 4.6), M, 80 + k)
    f = _lantern(mb, fl, cards, (0.75, 2.6, 0.9), M, hang=True, s=1.0)
    _flame_light('lantern', tuple(f), LANTERN, 150 * P.get('gas', 1.0), radius=0.15, shadow=True)
    pl = MB(); pl.quad((f.x - 2.2, f.y - 2.2, 0.01), (4.4, 0, 0), (0, 4.4, 0), M['pool'], (0, 0, 1, 1)); _obj(pl, 'lantern_pool', SET, shadow=False)
    # door (front wall y 0) with the line of light under it
    mb.box((-0.8, 0.0, 0.0), (0.8, 0.06, 4.0), M['wood_d'], tile=(1, 1)); fl.quad((-0.8, 0.07, 0.0), (1.6, 0, 0), (0, 0, 0.05), M['gasglobe'])
    rod(mb, (0.6, 0.06, 2.0), (0.6, 0.18, 2.0), 0.05, M['brass'], seg=6)
    _obj(mb, 'closet_dressing', SET, hull=0.012); _obj(fl, 'closet_glow', SET, shadow=False); _obj(cards, 'closet_halos', SET, shadow=False)
    STATE['marks'].update(vincenzo_hide=(-0.9, 1.6, 0.0), lantern=tuple(round(v, 3) for v in f))

def _stair(SET, P, M, dress):
    """The service staircase (the Visconti stair's back flight): a straight stone flight rising +y (14 steps, 0.36 rise x 0.6 run)
    between ashlar walls to a landing, an iron handrail, a gas bracket on each wall, a tall narrow window at the landing throwing
    a morning shaft across the steps. set_frame_on_stairs shows the empty gilt frame and the glass box left on the steps."""
    x0, x1 = -2.2, 2.2; n = 14; rise, run = 0.36, 0.6; ytop = n * run; ztop = n * rise; h = ztop + 6.0
    mb = MB(); fl = MB(); cards = MB()
    mb.quad((x0, -3, 0), (x1 - x0, 0, 0), (0, 3, 0), M['flags'], (0, 0, 2, 1.5))
    for i in range(n):
        y = i * run; z = (i + 1) * rise
        mb.box((x0, y, z - rise), (x1, y + run, z), M['ashlar_d'], tile=(4, 4), mats=dict(top=M['flags']))
        mb.box((x0, y - 0.04, z - 0.05), (x1, y + 0.02, z + 0.02), M['ashlar'], tile=(4, 4))
    mb.box((x0, ytop, 0), (x1, ytop + 4.0, ztop), M['ashlar_d'], tile=(4, 4), mats=dict(top=M['flags']))
    win = (x0, ytop + 1.2, ztop + 2.2, ytop + 2.8, ztop + 6.5)                                                      # the window in the left wall
    for (x, nn) in ((x0, 1), (x1, -1)):
        parts = [(-3, ytop + 4, 0, h)] if x == x1 else [(-3, win[1], 0, h), (win[3], ytop + 4, 0, h), (win[1], win[3], 0, win[2]), (win[1], win[3], win[4], h)]
        for (ya, yb_, za, zb) in parts: mb.oface([(x, ya, za), (x, yb_, za), (x, yb_, zb), (x, ya, zb)], M['ashlar'], [(ya / 4, za / 4), (yb_ / 4, za / 4), (yb_ / 4, zb / 4), (ya / 4, zb / 4)], (nn, 0, 0))
    yb = ytop + 4.0
    mb.oface([(x0, yb, 0), (x1, yb, 0), (x1, yb, h), (x0, yb, h)], M['ashlar'], [(0, 0), (1.1, 0), (1.1, h / 4), (0, h / 4)], (0, -1, 0))
    mb.quad((x0, yb, h), (x1 - x0, 0, 0), (0, -(yb + 3), 0), M['plaster'], (0, 0, 1, 3))
    _obj(mb, 'stair_shell', SET)
    dm = MB()
    hr = [Vector((x1 - 0.25, -1.0, 3.0))] + [Vector((x1 - 0.25, i * run, i * rise + 3.0)) for i in range(n + 1)] + [Vector((x1 - 0.25, ytop + 3.5, ztop + 3.0))]
    chain_rod(dm, hr, 0.06, M['wood_d'], seg=8)
    for i in range(0, n + 1, 2): rod(dm, (x1 - 0.25, i * run + 0.3, i * rise + rise), (x1 - 0.25, i * run + 0.3, i * rise + 3.0), 0.025, M['iron'], seg=5)
    gw = MB(); gw.oface([(x0 + 0.02, win[1], win[2]), (x0 + 0.02, win[3], win[2]), (x0 + 0.02, win[3], win[4]), (x0 + 0.02, win[1], win[4])], M['skyglass'], [(0, 0), (0.8, 0), (0.8, 2), (0, 2)], (1, 0, 0))
    for zz in (win[2], win[4]): dm.box((x0, win[1] - 0.15, zz - 0.12), (x0 + 0.25, win[3] + 0.15, zz + 0.12), M['ashlar'])
    for yy in (win[1], win[3]): dm.box((x0, yy - 0.12, win[2]), (x0 + 0.25, yy + 0.12, win[4]), M['ashlar'])
    dm.box((x0, (win[1] + win[3]) / 2 - 0.04, win[2]), (x0 + 0.08, (win[1] + win[3]) / 2 + 0.04, win[4]), M['iron'])
    for k in range(1, 4): zz = win[2] + (win[4] - win[2]) * k / 4; dm.box((x0, win[1], zz - 0.03), (x0 + 0.08, win[3], zz + 0.03), M['iron'])
    _obj(gw, 'stair_window', SET, shadow=False)
    lamps = []
    for (p, nn) in (((x0, 3.0, 2.6 + 3.0), (1, 0, 0)), ((x1, ytop + 2.5, ztop + 3.4), (-1, 0, 0))):
        lamps.append(_gas_bracket(dm, fl, cards, p, nn, M))
    for i, f in enumerate(lamps): _flame_light('gas_%d' % i, tuple(f), GAS, 170 * P.get('gas', 1.0), radius=0.25, shadow=True)
    # the empty frame and her glass box left on the steps (set_frame_on_stairs)
    fr = MB(); s0 = 5; base = Vector((-0.6, s0 * run + 0.15, (s0 + 1) * rise))
    pts = [base, base + Vector((1.44, 0, 0)), base + Vector((1.44, 0.75, 1.75)), base + Vector((0, 0.75, 1.75))]
    nn = (pts[1] - pts[0]).cross(pts[3] - pts[0]).normalized()
    if nn.y > 0: nn = -nn
    inner = [pts[0].lerp(pts[2], 0.0)]
    c = sum(pts, Vector()) / 4; ins = [c + (p - c) * 0.76 for p in pts]
    _frame_geo(fr, ins, nn, 0.22, 0.12, M['gold'])
    fr.oface([p + nn * 0.02 for p in ins], M['dark'], [(0, 0)] * 4, nn)
    gb = Vector((0.9, (s0 + 2) * run + 0.2, (s0 + 3) * rise)); fr.box((gb.x, gb.y, gb.z), (gb.x + 1.1, gb.y + 0.12, gb.z + 1.5), M['glass'])
    STATE['stair_frame'] = [_obj(fr, 'stair_frame', SET, hull=0.01)]
    _obj(dm, 'stair_dressing', SET, hull=0.012); _obj(fl, 'stair_glow', SET, shadow=False); _obj(cards, 'stair_halos', SET, shadow=False)
    kd = Vector(P['key_dir']).normalized(); sb = MB()
    corners = [Vector((x0, win[1], win[2])), Vector((x0, win[3], win[2])), Vector((x0, win[3], win[4])), Vector((x0, win[1], win[4]))]
    def ext(p): t = (p.z - ztop * 0.5) / max(0.05, -kd.z); t = min(t, 9.0); return p + kd * t
    mid = lambda p, q: (p + q) / 2
    sb.face([mid(corners[0], corners[3]), mid(corners[1], corners[2]), ext(mid(corners[1], corners[2])), ext(mid(corners[0], corners[3]))], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    sb.face([mid(corners[0], corners[1]), mid(corners[3], corners[2]), ext(mid(corners[3], corners[2])), ext(mid(corners[0], corners[1]))], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sb, 'sun_shafts', SET, shadow=False)
    STATE['stair'] = dict(n=n, rise=rise, run=run, landing=(0.0, ytop + 2.0, ztop))
    STATE['marks'].update(vincenzo_landing=(0.0, ytop + 1.6, round(ztop, 3)), vincenzo_step8=(0.4, 8 * run + 0.3, 8 * rise))
    _sky_dome(SET, P, M, STATE['E'], pano=False)

def _exitdoor(SET, P, M, dress):
    """The service corridor's end: a locked heavy oak door (iron straps, lock box, the knob missing) under a glazed fanlight with
    morning daylight; ashlar walls, flagstones, a gas bracket each side, a bench, a fire bucket. set_door swings the door inward on its
    left hinge (x -1.1) and reveals the bright courtyard (the Cour du Sphinx: a sunlit painted plate)."""
    x0, x1, y1, h = -3.0, 3.0, 10.0, 7.0; dw, dh = 2.2, 4.4; hx = -dw / 2
    mb = MB(); fl = MB(); cards = MB()
    mb.quad((x0, -2, 0), (x1 - x0, 0, 0), (0, y1 + 2, 0), M['flags'], (0, 0, 1.5, 3))
    mb.quad((x0, y1, h), (x1 - x0, 0, 0), (0, -(y1 + 2), 0), M['plaster'], (0, 0, 1.5, 3))
    for (x, nn) in ((x0, 1), (x1, -1)): mb.oface([(x, -2, 0), (x, y1, 0), (x, y1, h), (x, -2, h)], M['ashlar'], [(0, 0), (3, 0), (3, h / 4), (0, h / 4)], (nn, 0, 0))
    for (a, b, c, d) in ((x0, hx, 0, h), (-hx, x1, 0, h), (hx, -hx, dh + 1.6, h)):
        mb.oface([(a, y1, c), (b, y1, c), (b, y1, d), (a, y1, d)], M['ashlar'], [(a / 4, c / 4), (b / 4, c / 4), (b / 4, d / 4), (a / 4, d / 4)], (0, -1, 0))
    for x in (hx - 0.3, -hx): mb.box((x, y1 - 0.25, 0), (x + 0.3, y1, dh + 1.6), M['ashlar'], tile=(4, 4))
    mb.box((hx - 0.3, y1 - 0.25, dh), (-hx + 0.3, y1, dh + 0.2), M['ashlar'], tile=(4, 4))
    mb.box((hx - 0.4, y1 - 0.35, dh + 1.6), (-hx + 0.4, y1, dh + 1.85), M['ashlar'], tile=(4, 4))
    fg = MB(); fg.oface([(hx, y1 - 0.05, dh + 0.2), (-hx, y1 - 0.05, dh + 0.2), (-hx, y1 - 0.05, dh + 1.6), (hx, y1 - 0.05, dh + 1.6)], M['skyglass'], [(0, 0), (1.1, 0), (1.1, 0.7), (0, 0.7)], (0, -1, 0))
    for k in range(1, 4): xx = hx + dw * k / 4; mb.box((xx - 0.04, y1 - 0.1, dh + 0.2), (xx + 0.04, y1, dh + 1.6), M['iron'])
    _obj(mb, 'corridor', SET); _obj(fg, 'fanlight', SET, shadow=False)
    # beyond the door: the sunlit courtyard plate and its warm floor spill
    by = MB(); by.oface([(hx - 1, y1 + 3.0, -0.5), (-hx + 1, y1 + 3.0, -0.5), (-hx + 1, y1 + 3.0, dh + 1.0), (hx - 1, y1 + 3.0, dh + 1.0)], STATE['E']('court', hexcol='#fff0d0', k=1.6), [(0, 0)] * 4, (0, -1, 0))
    by.quad((hx - 1, y1, 0.002), (dw + 2, 0, 0), (0, 3.0, 0), STATE['E']('court_floor', hexcol='#f0d8b0', k=1.2))
    _obj(by, 'courtyard', SET, shadow=False)
    # the door on its hinge pivot
    piv = G._pivot('door_pivot', SET, (hx, y1 - 0.12, 0.0)); dmb = MB()
    dmb.box((hx, y1 - 0.2, 0.0), (hx + dw, y1 - 0.05, dh), M['oak_door'], mats=dict(front=M['oak_door']))
    rod(dmb, (hx + dw - 0.4, y1 - 0.2, dh * 0.47 + 0.42), (hx + dw - 0.4, y1 - 0.26, dh * 0.47 + 0.42), 0.05, M['iron'], seg=6)
    do = _obj(dmb, 'exit_door', SET, hull=0.012); G._parent(do, piv); STATE['door'] = dict(pivot=piv, obj=do)
    # line of daylight under and round the shut door
    lg = MB(); lg.quad((hx, y1 - 0.04, 0.0), (dw, 0, 0), (0, 0, 0.04), M['skyglass']); _obj(lg, 'door_crack', SET, shadow=False)
    dm = MB(); lamps = []
    for (p, nn) in (((x0, 6.0, 4.6), (1, 0, 0)), ((x1, 6.0, 4.6), (-1, 0, 0))): lamps.append(_gas_bracket(dm, fl, cards, p, nn, M))
    for i, f in enumerate(lamps): _flame_light('gas_%d' % i, tuple(f), GAS, 170 * P.get('gas', 1.0), radius=0.25, shadow=i == 0)
    dm.box((x1 - 0.9, 2.5, 1.0), (x1 - 0.1, 6.0, 1.2), M['wood']); [rod(dm, (x1 - 0.5, y, 0), (x1 - 0.5, y, 1.0), 0.06, M['wood_d'], seg=6) for y in (2.8, 5.7)]
    rod(dm, (x0 + 0.5, 8.6, 0), (x0 + 0.5, 8.6, 0.8), 0.3, M['red'], seg=12, r1=0.36)
    rod(dm, (x0 + 0.05, 5.0, 4.1), (x0 + 0.05, 8.2, 4.1), 0.06, M['wood_d'], seg=6)                                   # coat rail with the workers' white smocks
    for k, y in enumerate((5.4, 6.3, 7.4)): _smock(dm, (x0 + 0.35, y, 4.1), M, 120 + k, s=0.9)
    for k, (y, z) in enumerate(((2.2, 3.0), (1.0, 3.4))):                                                          # framed notices
        dm.box((x0 + 0.02, y - 0.45, z - 0.6), (x0 + 0.1, y + 0.45, z + 0.6), M['wood_d']); nb2 = MB(); nb2.oface([(x0 + 0.11, y - 0.38, z - 0.52), (x0 + 0.11, y + 0.38, z - 0.52), (x0 + 0.11, y + 0.38, z + 0.52), (x0 + 0.11, y - 0.38, z + 0.52)], M['news'][2 + k], [(0, 0), (1, 0), (1, 1), (0, 1)], (1, 0, 0)); _obj(nb2, 'corridor_notice_%d' % k, SET)
    sg = MB(); sg.quad((x1 - 0.02, 7.2, 3.6), (0, 0.9, 0), (0, 0, 0.36), M['sign_prive'], (1, 0, 0, 1)); _obj(sg, 'sign_prive', SET)
    for (z, r_) in ((5.8, 0.09), (6.2, 0.06)):                                                                  # lead water pipes along the right wall (the plumber's)
        rod(dm, (x1 - 0.15, -2.0, z), (x1 - 0.15, y1, z), r_, M['zinc'], seg=8)
        for y in range(-1, 10, 3): rod(dm, (x1 - 0.02, y, z), (x1 - 0.15, y, z), 0.02, M['iron'], seg=4)
    rod(dm, (x1 - 0.15, 8.8, 0.3), (x1 - 0.15, 8.8, 5.8), 0.09, M['zinc'], seg=8); rod(dm, (x1 - 0.15, 8.8, 0.3), (x1 - 0.5, 8.8, 0.3), 0.09, M['zinc'], seg=8)
    rod(dm, (x1 - 0.55, 8.8, 0.0), (x1 - 0.55, 8.8, 0.3), 0.07, M['brass'], seg=8)
    dm.box((x0 + 0.02, 3.4, 2.6), (x0 + 0.08, 4.8, 3.8), M['wood_d']); nb_ = MB(); nb_.oface([(x0 + 0.09, 3.5, 2.7), (x0 + 0.09, 4.7, 2.7), (x0 + 0.09, 4.7, 3.7), (x0 + 0.09, 3.5, 3.7)], M['posters'][4], [(0, 0), (1, 0), (1, 1), (0, 1)], (1, 0, 0)); _obj(nb_, 'corridor_notice', SET)
    _obj(dm, 'corridor_dressing', SET, hull=0.012); _obj(fl, 'corridor_glow', SET, shadow=False); _obj(cards, 'corridor_halos', SET, shadow=False)
    # daylight through the fanlight: a shaft down onto the flags
    kd = Vector(P['key_dir']).normalized(); sb = MB()
    a0, a1 = Vector((hx + 0.2, y1, dh + 0.9)), Vector((-hx - 0.2, y1, dh + 0.9))
    def ext(p): t = p.z / max(0.05, -kd.z); return p + kd * t
    sb.face([a0, a1, ext(a1), ext(a0)], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)]); _obj(sb, 'sun_shafts', SET, shadow=False)
    STATE['door_light'] = BK._light('daylight_in', (0.0, y1 + 1.0, 2.5), (1.0, 0.92, 0.78), 0.0, radius=1.5, shadow=True)
    STATE['marks'].update(vincenzo_door=(0.9, 8.0, 0.0), plumber_enter=(0.4, 11.5, 0.0))
    _sky_dome(SET, P, M, STATE['E'], pano=False)

# ============================================================================= PARIS: the street
def _block(SET, name, F, w, M, k, dusk=False, awn=None, rr=None):
    """Haussmann block front in a frame (front at local y 0 facing -y): the painted facade, 3D continuous balconies (slab + rail rods)
    at the 2nd and 5th floors, the cornice, the zinc mansard with dormers, the party walls."""
    mb = MB(); H = 15.0; tex = (M['haus_n'] if dusk else M['haus'])[k % 3]
    F.quad(mb, [(0, 0, 0), (w, 0, 0), (w, 0, H), (0, 0, H)], tex, [(0, 0), (w / 8.0, 0), (w / 8.0, 1), (0, 1)], (0, -1, 0))
    for zb in (6.4, 13.2):
        F.box(mb, (-0.05, -0.7, zb - 0.18), (w + 0.05, 0, zb), M['stone_p'], 0.5)
        F.box(mb, (0, -0.68, zb + 0.72), (w, -0.62, zb + 0.78), M['iron'])
        for i in range(int(w / 0.35) + 1): rod(mb, F.p(i * 0.35, -0.65, zb), F.p(i * 0.35, -0.65, zb + 0.74), 0.018, M['iron'], seg=4)
    F.box(mb, (-0.05, -0.55, H - 0.1), (w + 0.05, 0, H + 0.35), M['stone_p'], 0.5); F.box(mb, (-0.05, -0.3, 4.4), (w + 0.05, 0, 4.6), M['stone_p'], 0.5)
    F.quad(mb, [(0, -0.4, H + 0.35), (w, -0.4, H + 0.35), (w, 1.6, H + 4.3), (0, 1.6, H + 4.3)], M['mansard'], [(0, 0), (w / 8, 0), (w / 8, 1), (0, 1)], (0, -1, 0.6))
    for x in (0.0, w): F.quad(mb, [(x, 0, 0), (x, 8, 0), (x, 8, H + 3), (x, 0, H + 3)], M['stone_p'], [(0, 0), (2, 0), (2, 4), (0, 4)], (-1 if x == 0 else 1, 0, 0))
    return _obj(mb, name, SET, hull=0.02)

def _gas_lamp(mb, fl, cards, p, M, h=5.6):
    """Cast-iron Paris street lamp: fluted post on a base, a cross-bar, the four-sided lantern with glowing glass and a crown."""
    p = Vector(p); rod(mb, p, p + Vector((0, 0, 0.6)), 0.24, M['iron'], seg=10, r1=0.16); rod(mb, p + Vector((0, 0, 0.6)), p + Vector((0, 0, h)), 0.09, M['iron'], seg=8, r1=0.07)
    rod(mb, p + Vector((-0.4, 0, h - 0.8)), p + Vector((0.4, 0, h - 0.8)), 0.035, M['iron'], seg=5)
    q = p + Vector((0, 0, h)); fl.frustum(q, q + Vector((0, 0, 0.75)), 0.2, 0.32, M['lamp_glass'], seg=4)
    rod(mb, q + Vector((0, 0, 0.75)), q + Vector((0, 0, 0.95)), 0.4, M['iron'], seg=4, r1=0.08); mb.sphere(q + Vector((0, 0, 1.0)), 0.07, M['iron'], seg=6, rings=3)
    f = q + Vector((0, 0, 0.38)); _halo(cards, f, 1.1, M); return f

def _horse_cab(mb, base, yaw, M):
    """Fiacre: black closed cab body on yellow-spoked wheels, the cabby's box, a brown horse in the shafts (all simple solids)."""
    F = Frame(base, yaw)
    F.box(mb, (-0.9, 0.0, 1.2), (0.9, 2.4, 3.2), M['cab']); F.box(mb, (-0.95, -0.2, 3.2), (0.95, 2.6, 3.35), M['cab'])
    F.box(mb, (-0.92, 0.6, 2.2), (0.92, 1.6, 2.95), M['glass']); F.box(mb, (-0.7, -1.0, 2.0), (0.7, 0.0, 2.3), M['cab'])
    for (x, y, r) in ((-1.0, 0.4, 0.75), (1.0, 0.4, 0.75), (-1.0, 2.1, 0.95), (1.0, 2.1, 0.95)):
        c = F.p(x, y, r); rod(mb, c - F.X * 0.06, c + F.X * 0.06, r, M['wheel'], seg=16)
        rod(mb, c - F.X * 0.08, c + F.X * 0.08, r * 0.2, M['cab'], seg=8)
    for s in (-0.55, 0.55): beam(mb, F.p(s, -0.6, 1.6), F.p(s, -4.6, 1.9), 0.06, 0.06, M['wood_d'])
    hb = F.p(0, -3.2, 2.4); lumpy(mb, hb, 0.9, M['horse'], 91, seg=12, rings=6, rough=0.05, squash=0.62)
    T_ = lambda v: F.X * v[0] + F.Y * v[1] + F.Z * v[2]
    obox(mb, hb + T_((0, -1.2, 0.8)), F.X, (F.Y * -0.6 + F.Z * 0.8).normalized(), (F.Y * 0.8 + F.Z * 0.6).normalized(), 0.28, 0.75, 0.32, M['horse'])
    obox(mb, hb + T_((0, -1.75, 1.2)), F.X, (F.Y * -0.9 + F.Z * -0.45).normalized(), (F.Y * -0.45 + F.Z * 0.9).normalized(), 0.22, 0.5, 0.24, M['horse'])
    for (x, y) in ((-0.35, -0.7), (0.35, -0.7), (-0.35, 0.75), (0.35, 0.75)): rod(mb, hb + T_((x, y, -0.3)), hb + T_((x, y, -2.4)), 0.11, M['horse'], seg=6, r1=0.08)
    rod(mb, hb + T_((0, 1.3, 0.2)), hb + T_((0, 1.6, -1.2)), 0.12, M['horse_d'], seg=6, r1=0.04)
    lumpy(mb, hb + T_((0, -1.4, 1.3)), 0.25, M['horse_d'], 92, seg=8, rings=4, rough=0.3, squash=2.0)

def _street(SET, P, M, dress):
    """The rue outside the Louvre, running +y to the quai: wood-block road with tram-free cobbles, pavements with kerbs, rows of
    Haussmann blocks both sides (x -7 facing +x, x +7 facing -x), shopfronts and the Cafe du Louvre awning with tables, gas lamps along
    the kerbs, a Morris column and a green newspaper kiosk with her face on the front pages (set_papers), a fiacre; at the end the quai
    parapet, the river and Notre-Dame's towers on the Ile de la Cite."""
    dusk = P['sky'] == 'dusk'; (ra, rb), (wa, wb) = STREET['road'], STREET['walk']; y0, y1 = STREET['y']
    mb = MB(); mb.quad((ra, y0, 0), (rb - ra, 0, 0), (0, y1 - y0, 0), M['cobbles'], (ra / 4, y0 / 4, rb / 4, y1 / 4))
    for (a, b) in ((wa, ra), (rb, wb)):
        mb.box((a, y0, 0), (b, y1, 0.25), M['pave'], mats=dict(top=M['pave']), tile=(4, 4))
    mb.quad((-80, y1, -0.4), (160, 0, 0), (0, 70, 0), M['seine'], (0, 0, 20, 14))
    mb.box((-80, y1 - 0.8, 0), (80, y1, 1.4), M['stone_p'], tile=(2, 2)); mb.box((-80, y1 - 0.9, 1.4), (80, y1 + 0.1, 1.6), M['stone_p'])
    mb.quad((-80, y1 - 30, -0.01), (160, 0, 0), (0, 29.2, 0), M['cobbles'], (0, 0, 40, 7))
    _obj(mb, 'street_ground', SET)
    # the blocks: west row (front at x = -7 facing +x), east row (front at x = 7 facing -x)
    y = y0; k = 0
    while y < y1 - 4:
        w = 8.0 if y + 8 <= y1 - 6 else y1 - 6 - y
        if w < 3: break
        _block(SET, 'west_%d' % k, Frame((wa, y, 0), 90.0), w, M, k, dusk)
        _block(SET, 'east_%d' % k, Frame((wb, y + w, 0), -90.0), w, M, k + 1, dusk)
        y += w; k += 1
    # corner blocks along the quai (facing the river, behind the camera of notre_dame_view are the rows)
    mb = MB(); fl = MB(); cards = MB(); lamps = []
    for yy in range(int(y0) + 4, int(y1) - 2, 10):
        for x in (ra - 0.5, rb + 0.5): lamps.append(_gas_lamp(mb, fl, cards, (x, yy, 0.25), M))
    for x in (-12, -4, 4, 12): lamps.append(_gas_lamp(mb, fl, cards, (x, y1 - 1.6, 1.6), M, h=4.0))
    for i, f in enumerate(lamps):
        if abs(f.y - 12) < 11 or (dusk and f.y > y1 - 3 and abs(f.x) < 6): _flame_light('lamp_%d' % i, tuple(f), GAS, (140 if dusk else 60) * P.get('gas', 1.0), radius=0.3, shadow=False)
    # cafe awning + tables on the east pavement (y 4..12)
    F = Frame((wb, 12.0, 0), -90.0)
    F.quad(mb, [(0, 0, 4.2), (8, 0, 4.2), (8, -2.6, 3.3), (0, -2.6, 3.3)], M['awn_cafe'], [(0, 0), (4, 0), (4, 1), (0, 1)], (0, -1, 1))
    F.quad(mb, [(0, -0.1, 4.25), (8, -0.1, 4.25), (8, -0.1, 4.6), (0, -0.1, 4.6)], M['sign_cafe'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    for (tx_, ty) in ((5.8, 5.4), (5.8, 8.2), (5.8, 11.0)):
        rod(mb, (tx_, ty, 0.25), (tx_, ty, 1.55), 0.05, M['iron'], seg=6); rod(mb, (tx_, ty, 1.5), (tx_, ty, 1.58), 0.45, M['marble_w'], seg=14); rod(mb, (tx_, ty, 0.25), (tx_, ty, 0.3), 0.3, M['iron'], seg=10)
        rod(mb, (tx_, ty + 0.15, 1.58), (tx_, ty + 0.15, 1.8), 0.08, M['glass'], seg=8)
        for s in (-1, 1):
            cx_ = tx_ - 0.2; cy_ = ty + s * 0.85; rod(mb, (cx_, cy_, 0.25), (cx_, cy_, 1.1), 0.04, M['wood_d'], seg=5); rod(mb, (cx_, cy_, 1.1), (cx_, cy_, 1.16), 0.32, M['straw'], seg=12)
            chain_rod(mb, [Vector((cx_, cy_ + s * 0.3, 1.16)), Vector((cx_, cy_ + s * 0.34, 2.1)), Vector((cx_, cy_ - s * 0.0, 2.25))], 0.035, M['wood_d'])
    # Morris column (east kerb) and the newspaper kiosk (west pavement)
    mc = Vector((rb + 1.4, 16.0, 0.25)); rod(mb, mc, mc + Vector((0, 0, 0.5)), 1.05, M['green'], seg=24)
    mb.frustum(mc + Vector((0, 0, 0.5)), mc + Vector((0, 0, 4.1)), 0.9, 0.9, M['morris'], seg=24, cap0=False, cap1=False, uv_wrap=(1, 1))
    rod(mb, mc + Vector((0, 0, 4.1)), mc + Vector((0, 0, 4.4)), 1.05, M['green'], seg=24); lumpy(mb, mc + Vector((0, 0, 4.4)), 0.95, M['green'], 93, seg=20, rings=6, rough=0.0, squash=0.7)
    rod(mb, mc + Vector((0, 0, 5.0)), mc + Vector((0, 0, 5.5)), 0.12, M['green'], seg=8)
    kc = Vector((ra - 1.6, 10.0, 0.25)); kw, kd_ = 1.4, 1.1
    mb.box((kc.x - kd_, kc.y - kw, kc.z), (kc.x + kd_, kc.y + kw, kc.z + 1.3), M['green'], tile=(1, 1))
    mb.box((kc.x - kd_ + 0.1, kc.y - kw + 0.1, kc.z + 1.3), (kc.x + kd_ - 0.1, kc.y + kw - 0.1, kc.z + 3.2), M['dark'])
    for (sx, sy) in ((-1, -1), (1, -1), (-1, 1), (1, 1)): rod(mb, (kc.x + sx * kd_, kc.y + sy * kw, kc.z), (kc.x + sx * kd_, kc.y + sy * kw, kc.z + 3.4), 0.06, M['green'], seg=6)
    mb.quad((kc.x + kd_ + 0.01, kc.y - kw, kc.z + 3.2), (0, 2 * kw, 0), (0, 0, 0.7), M['kiosk'], (0, 0, 1, 1))
    for s in (-1, 1): mb.oface([(kc.x - kd_ - 0.5, kc.y + s * (kw + 0.5), kc.z + 3.9), (kc.x + kd_ + 0.6, kc.y + s * (kw + 0.5), kc.z + 3.9), (kc.x + kd_ * 0.0, kc.y, kc.z + 4.8)], M['green'], [(0, 0), (1, 0), (0.5, 1)], (0, s, 1))
    mb.oface([(kc.x + kd_ + 0.6, kc.y - kw - 0.5, kc.z + 3.9), (kc.x + kd_ + 0.6, kc.y + kw + 0.5, kc.z + 3.9), (kc.x, kc.y, kc.z + 4.8)], M['green'], [(0, 0), (1, 0), (0.5, 1)], (1, 0, 1))
    mb.oface([(kc.x - kd_ - 0.5, kc.y - kw - 0.5, kc.z + 3.9), (kc.x - kd_ - 0.5, kc.y + kw + 0.5, kc.z + 3.9), (kc.x, kc.y, kc.z + 4.8)], M['green'], [(0, 0), (1, 0), (0.5, 1)], (-1, 0, 1))
    mb.box((kc.x + kd_, kc.y - kw, kc.z + 1.15), (kc.x + kd_ + 0.55, kc.y + kw, kc.z + 1.3), M['wood'])
    for i in range(3): mb.box((kc.x + kd_ + 0.05, kc.y - kw + 0.15 + i * 0.95, kc.z + 1.3), (kc.x + kd_ + 0.5, kc.y - kw + 0.95 + i * 0.95, kc.z + 1.3 + 0.08 + 0.05 * i), M['white'])
    # the papers / posters with her face (set_papers): kiosk front strings, kiosk sides, the column, shop shutters
    pp = []; pm = MB()
    for row, z in enumerate((2.45, 1.4)):
        for i in range(4):
            y = kc.y - kw + 0.12 + i * 0.68; pp.append(('k', [Vector((kc.x + kd_ + 0.08, y, kc.z + z)), Vector((kc.x + kd_ + 0.08, y + 0.58, kc.z + z)), Vector((kc.x + kd_ + 0.08, y + 0.58, kc.z + z + 0.8)), Vector((kc.x + kd_ + 0.08, y, kc.z + z + 0.8))], (1, 0, 0), 'news', i + row))
    for s in (-1, 1):
        for i in range(2):
            x = kc.x - 0.7 + i * 0.75; yy = kc.y + s * (kw + 0.02)
            pp.append(('k', [Vector((x, yy, kc.z + 1.6)), Vector((x + 0.62, yy, kc.z + 1.6)), Vector((x + 0.62, yy, kc.z + 2.45)), Vector((x, yy, kc.z + 2.45))], (0, s, 0), 'news', i + 2))
    for i in range(6):
        a = math.radians(200 + i * 40); c0 = mc + Vector((0.93 * math.cos(a), 0.93 * math.sin(a), 1.4)); t = Vector((-math.sin(a), math.cos(a), 0))
        pp.append(('c', [c0 - t * 0.48, c0 + t * 0.48, c0 + t * 0.48 + Vector((0, 0, 1.35)), c0 - t * 0.48 + Vector((0, 0, 1.35))], (math.cos(a), math.sin(a), 0), 'poster', i % 2))
    for i in range(6):
        side = -1 if i % 2 == 0 else 1; y = 18.5 + (i // 2) * 2.2; x = (wa + 0.02) if side < 0 else (wb - 0.02)
        pp.append(('w', [Vector((x, y, 0.6)), Vector((x, y + 1.0, 0.6)), Vector((x, y + 1.0, 2.0)), Vector((x, y, 2.0))], (-side, 0, 0), 'poster', i % 2))
    STATE['papers'] = []
    for i, (kind, pts, nn, what, var) in enumerate(pp):
        b = MB(); mat = M['news'][var % 4] if what == 'news' else M['posters'][var % 2]
        b.oface(pts, mat, [(0, 0), (1, 0), (1, 1), (0, 1)], nn)
        o = _obj(b, 'paper_%02d' % i, SET); STATE['papers'].append(o)
    # generic posters on the column already in its texture; the fiacre on the road; benches, a tree trunk or two
    _horse_cab(mb, (1.8, 22.0, 0), 180.0, M)
    for (tx_, ty) in ((ra - 1.0, 26.0), (rb + 1.0, 30.0)):
        rod(mb, (tx_, ty, 0.25), (tx_, ty, 4.5), 0.22, M['wood_d'], seg=8)
        for kk in range(5): lumpy(mb, (tx_ + _rnd(kk).uniform(-1, 1), ty + _rnd(kk + 9).uniform(-1, 1), 5.0 + kk * 0.3), 1.2, M['green'], 300 + kk, seg=10, rings=5, rough=0.25, squash=0.8)
    _obj(mb, 'street_dressing', SET, hull=0.02); _obj(fl, 'street_glow', SET, shadow=False); _obj(cards, 'street_halos', SET, shadow=False)
    # Notre-Dame across the river: the painted west front plate (cut-out), facing the street
    nd = MB(); W_, H_ = 72.0, 60.0; cx_, cy_ = 5.0, 108.0
    nd.oface([(cx_ - W_ / 2, cy_, -3.0), (cx_ + W_ / 2, cy_, -3.0), (cx_ + W_ / 2, cy_, H_ - 3.0), (cx_ - W_ / 2, cy_, H_ - 3.0)], mat_emit(STATE['pre'] + 'e_nd', image=STATE['tx']['notredame'], strength=0.95 if not dusk else 0.8, alpha=True),
             [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    _obj(nd, 'notre_dame', SET, shadow=False)
    STATE['marks'].update(kiosk_reader=(round(kc.x + kd_ + 1.6, 3), round(kc.y - 0.6, 3), 0.0), kiosk_side=(round(kc.x + kd_ + 0.5, 3), round(kc.y + kw + 1.0, 3), 0.25),
                          newsboy=(round(ra + 0.6, 3), 13.5, 0.0), cafe=(5.0, 7.0, 0.25), passers=[(-5.2, 18.0, 0.25), (5.2, 20.0, 0.25), (-1.0, 28.0, 0.0)], quai=(0.0, 58.5, 0.25))
    STATE['kiosk'] = dict(centre=tuple(round(v, 3) for v in kc), front_x=kc.x + kd_); STATE['morris'] = tuple(round(v, 3) for v in mc)
    _sky_dome(SET, P, M, STATE['E'], pano=True)

# ============================================================================= ROOM: the attic and the Florence shop
def _attic(SET, P, M, dress):
    """Vincenzo's rented attic room (rue de l'Hopital-Saint-Louis): 8 x 6 D, the mansard slope over the window wall, faded wallpaper,
    bare boards; iron bed with a patchwork quilt, the wooden trunk under it (set_trunk: pulled out / lid open / the panel inside),
    a washstand with basin and jug, a table with a candle, a chair, the cap and the smock on pegs, a shelf, a small mirror; the dormer
    window onto the Paris rooftops at dusk."""
    x0, x1, y0, y1 = ATTIC; h = ATTIC_H; ks = 4.2                                                                  # knee: the slope starts at z 4.2 on the back wall
    mb = MB(); fl = MB(); cards = MB()
    mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['boards'], (x0 / 2, y0 / 2, x1 / 2, y1 / 2))
    wx0, wx1, wz0, wz1 = 0.6, 2.8, 1.9, 4.6                                                                        # the dormer window in the back wall
    for (a, b, c, d) in ((x0, wx0, 0, ks), (wx1, x1, 0, ks), (wx0, wx1, 0, wz0)):
        mb.oface([(a, y1, c), (b, y1, c), (b, y1, d), (a, y1, d)], M['wallpaper'], [(a / 1.2, c / 1.2), (b / 1.2, c / 1.2), (b / 1.2, d / 1.2), (a / 1.2, d / 1.2)], (0, -1, 0))
    ys = y1 - 2.4                                                                                                  # slope from (y1, ks) to (ys, h)
    for (a, b) in ((x0, wx0), (wx1, x1)):
        mb.oface([(a, y1, ks), (b, y1, ks), (b, ys, h), (a, ys, h)], M['plaster'], [(0, 0), ((b - a) / 4, 0), ((b - a) / 4, 0.7), (0, 0.7)], (0, -1, -1))
    for x in (wx0, wx1):                                                                                           # dormer cheeks + its ceiling
        mb.oface([(x, y1, wz0), (x, y1 + 1.0, wz0), (x, y1 + 1.0, wz1 + 0.6), (x, ys, h), (x, y1, ks)], M['plaster'], [(0, 0), (0.25, 0), (0.25, 0.8), (0.6, 1), (0, 0.6)], (1 if x == wx0 else -1, 0, 0))
    mb.oface([(wx0, y1 + 1.0, wz1 + 0.6), (wx1, y1 + 1.0, wz1 + 0.6), (wx1, ys, h), (wx0, ys, h)], M['plaster'], [(0, 0), (0.6, 0), (0.6, 0.6), (0, 0.6)], (0, -1, -1))
    mb.quad((x0, ys, h), (x1 - x0, 0, 0), (0, -(ys - y0), 0), M['plaster'], (0, 0, 2, 1))
    for (x, nn) in ((x0, 1), (x1, -1)):
        mb.oface([(x, y0, 0), (x, y1, 0), (x, y1, ks), (x, ys, h), (x, y0, h)], M['wallpaper'], [(y0 / 1.2, 0), (y1 / 1.2, 0), (y1 / 1.2, ks / 1.2), (ys / 1.2, h / 1.2), (y0 / 1.2, h / 1.2)], (nn, 0, 0))
    mb.oface([(x0, y0, 0), (x1, y0, 0), (x1, y0, h), (x0, y0, h)], M['wallpaper'], [(0, 0), (8 / 1.2, 0), (8 / 1.2, h / 1.2), (0, h / 1.2)], (0, 1, 0))
    _obj(mb, 'attic_shell', SET)
    dm = MB()
    for (zz, a) in ((0.0, 0.25),): dm.box((x0, y0, 0), (x1, y0 + 0.08, 0.3), M['wood_d'])
    dm.box((x0, y1 - 0.08, 0), (x1, y1, 0.3), M['wood_d'])
    # window: frame, glazing bars, the glass (camera-only sheen), a sill with a geranium pot; outside: the sky and the rooftops (pano)
    yw = y1 + 1.0
    for x in (wx0, wx1 - 0.15): dm.box((x, yw - 0.1, wz0), (x + 0.15, yw, wz1), M['wood_l'])
    for z in (wz0, wz1 - 0.15, (wz0 + wz1) / 2): dm.box((wx0, yw - 0.1, z), (wx1, yw, z + 0.12), M['wood_l'])
    dm.box(((wx0 + wx1) / 2 - 0.05, yw - 0.1, wz0), ((wx0 + wx1) / 2 + 0.05, yw, wz1), M['wood_l'])
    dm.box((wx0 - 0.1, y1 - 0.3, wz0 - 0.15), (wx1 + 0.1, yw, wz0), M['wood_l'])
    dm.oface([(wx0, yw, wz1), (wx1, yw, wz1), (wx1, yw, wz1 + 0.62), (wx0, yw, wz1 + 0.62)], M['plaster'], [(0, 0), (0.5, 0), (0.5, 0.15), (0, 0.15)], (0, -1, 0))
    rod(dm, (wx1 - 0.5, y1 + 0.2, wz0), (wx1 - 0.5, y1 + 0.2, wz0 + 0.4), 0.2, M['red'], seg=10, r1=0.25); lumpy(dm, (wx1 - 0.5, y1 + 0.2, wz0 + 0.6), 0.3, M['green'], 44, seg=8, rings=4, rough=0.3)
    gl = MB(); gl.oface([(wx0, yw - 0.05, wz0), (wx1, yw - 0.05, wz0), (wx1, yw - 0.05, wz1), (wx0, yw - 0.05, wz1)], M['glass'], [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], (0, -1, 0))
    _obj(gl, 'attic_glass', SET, shadow=False)
    # iron bed against the left wall (x -4..-1.9, y 0.6..4.4), mattress top z 1.5, clear under it 0.95 D
    bx0, bx1, by0, by1, bz = x0 + 0.1, x0 + 2.2, 0.6, 4.6, 1.2
    for (x, y) in ((bx0, by0), (bx1, by0), (bx0, by1), (bx1, by1)): rod(dm, (x, y, 0), (x, y, 2.9 if y == by1 else 2.2), 0.06, M['iron'], seg=6)
    for y in (by0, by1):
        zt = 2.2 if y == by0 else 2.9
        rod(dm, (bx0, y, zt), (bx1, y, zt), 0.05, M['iron'], seg=6); rod(dm, (bx0, y, 1.1), (bx1, y, 1.1), 0.04, M['iron'], seg=5)
        for k in range(1, 6): xx = bx0 + (bx1 - bx0) * k / 6; rod(dm, (xx, y, 1.1), (xx, y, zt), 0.022, M['iron'], seg=4)
        for xx in (bx0, bx1): dm.sphere((xx, y, zt + 0.08), 0.1, M['brass'], seg=8, rings=4)
    for x in (bx0, bx1): rod(dm, (x, by0, 1.05), (x, by1, 1.05), 0.04, M['iron'], seg=5)
    dm.box((bx0 + 0.05, by0 + 0.05, 1.05), (bx1 - 0.05, by1 - 0.05, bz + 0.25), M['linen'])
    lumpy(dm, ((bx0 + bx1) / 2, by1 - 0.55, bz + 0.45), 0.6, M['pillow'], 21, seg=10, rings=5, rough=0.1, squash=0.35)
    q = MB(); q.quad((bx0 - 0.1, by0 - 0.05, bz + 0.3), (bx1 - bx0 + 0.2, 0, 0), (0, by1 - by0 - 1.2, 0), M['quilt'], (0, 0, 1, 1.4))
    q.quad((bx1 + 0.1, by0 - 0.05, bz + 0.3), (0, 0, -0.42), (0, by1 - by0 - 1.2, 0), M['quilt'], (0, 0, 0.2, 1.4))
    _obj(q, 'quilt', SET)
    # the trunk under the bed (pivot for pull, lid hinge for open)
    tr = dict(c0=Vector(((bx0 + bx1) / 2, 2.6, 0.0)), w=1.5, d=1.0, h=0.62)
    pv = G._pivot('trunk_pivot', SET, tuple(tr['c0'])); tb = MB(); c = tr['c0']; w2, d2 = tr['d'] / 2, tr['w'] / 2
    tb.box((c.x - w2, c.y - d2, 0.0), (c.x + w2, c.y + d2, tr['h']), M['trunk'], tile=(2, 1))
    tb.box((c.x - w2 + 0.06, c.y - d2 + 0.06, tr['h'] - 0.02), (c.x + w2 - 0.06, c.y + d2 - 0.06, tr['h'] + 0.001), M['dark'])
    to = _obj(tb, 'trunk', SET, hull=0.008); G._parent(to, pv)
    lid = G._pivot('trunk_lid', SET, (c.x - w2, c.y, tr['h'])); G._parent(lid, pv); lb = MB()
    lb.box((c.x - w2, c.y - d2, tr['h']), (c.x + w2, c.y + d2, tr['h'] + 0.2), M['trunk'], tile=(2, 1))
    lo = _obj(lb, 'trunk_lid_mesh', SET, hull=0.008); G._parent(lo, lid)
    pb = MB()                                                                                                      # the panel inside, on a red cloth
    lumpy(pb, (c.x, c.y, tr['h'] - 0.3), 0.55, M['red'], 23, seg=10, rings=4, rough=0.2, squash=0.3)
    pb.oface([(c.x - 0.36, c.y - 0.5, tr['h'] - 0.14), (c.x + 0.36, c.y - 0.5, tr['h'] - 0.14), (c.x + 0.36, c.y + 0.55, tr['h'] - 0.1), (c.x - 0.36, c.y + 0.55, tr['h'] - 0.1)],
             M['mona'], [(1, 0), (1, 1), (0, 1), (0, 0)], (0, 0, 1))
    po = _obj(pb, 'trunk_panel', SET); G._parent(po, pv)
    STATE['trunk'] = dict(pivot=pv, lid=lid, panel=po, c0=tuple(tr['c0']))
    # washstand, table + candle, chair, pegs with cap and smock, shelf, mirror, a sardine tin and bread on the table
    ws = Vector((x1 - 1.0, 4.6, 0)); dm.box((ws.x - 0.6, ws.y - 0.5, 0), (ws.x + 0.6, ws.y + 0.5, 1.8), M['wood'], tile=(1, 1)); dm.box((ws.x - 0.65, ws.y - 0.55, 1.8), (ws.x + 0.65, ws.y + 0.55, 1.9), M['marble_w'])
    rod(dm, ws + Vector((0, 0, 1.9)), ws + Vector((0, 0, 2.15)), 0.4, M['basin'], seg=16, r1=0.5); rod(dm, ws + Vector((0.3, 0.2, 1.9)), ws + Vector((0.3, 0.2, 2.55)), 0.16, M['basin'], seg=12, r1=0.12)
    dm.box((ws.x - 0.4, y1 - 0.02, 2.7), (ws.x + 0.4, y1, 3.6), M['gold_c']); dm.box((ws.x - 0.34, y1 - 0.04, 2.76), (ws.x + 0.34, y1 - 0.02, 3.54), M['glass'])
    tb_ = Vector((0.9, 4.7, 0)); dm.box((tb_.x - 0.8, tb_.y - 0.55, 1.45), (tb_.x + 0.8, tb_.y + 0.55, 1.55), M['wood'], tile=(1, 1))
    for (sx, sy) in ((-0.7, -0.45), (0.7, -0.45), (-0.7, 0.45), (0.7, 0.45)): rod(dm, (tb_.x + sx, tb_.y + sy, 0), (tb_.x + sx, tb_.y + sy, 1.45), 0.05, M['wood_d'], seg=6)
    f = BK._candle(dm, fl, (tb_.x + 0.35, tb_.y + 0.1, 1.55), M, h=0.35, r=0.06); _halo(cards, f, 0.45, M)
    dm.box((tb_.x - 0.5, tb_.y - 0.2, 1.55), (tb_.x - 0.1, tb_.y + 0.05, 1.6), M['zinc']); lumpy(dm, (tb_.x - 0.1, tb_.y + 0.3, 1.65), 0.16, M['straw'], 24, seg=8, rings=4, rough=0.1, squash=0.6)
    for k in range(3): dm.box((tb_.x - 0.6 + k * 0.05, tb_.y - 0.45 + k * 0.04, 1.55 + k * 0.012), (tb_.x - 0.1 + k * 0.05, tb_.y - 0.05 + k * 0.04, 1.562 + k * 0.012), M['white'])
    ch = Vector((1.9, 4.5, 0)); dm.box((ch.x - 0.45, ch.y - 0.45, 1.0), (ch.x + 0.45, ch.y + 0.45, 1.1), M['wood'])
    for (sx, sy) in ((-0.4, -0.4), (0.4, -0.4), (-0.4, 0.4), (0.4, 0.4)): rod(dm, (ch.x + sx, ch.y + sy, 0), (ch.x + sx, ch.y + sy, 1.0), 0.04, M['wood_d'], seg=5)
    dm.box((ch.x - 0.45, ch.y - 0.5, 1.1), (ch.x + 0.45, ch.y - 0.4, 2.4), M['wood'])
    for k, y in enumerate((2.5, 3.3)):                                                                               # pegs on the right wall
        rod(dm, (x1, y, 3.9), (x1 - 0.25, y, 3.95), 0.04, M['wood_d'], seg=5)
    _smock(dm, (x1 - 0.3, 2.5, 3.95), M, 31)
    lumpy(dm, (x1 - 0.3, 3.3, 3.75), 0.32, M['black'], 32, seg=10, rings=5, rough=0.05, squash=0.55)
    f2 = BK._candle(dm, fl, (-0.9, 1.6, 0.0), M, h=0.3, r=0.06); _halo(cards, f2, 0.4, M)                                  # a stub of candle on the floor by the bed
    dm.box((x0 + 0.02, 0.2, 4.6), (x0 + 0.5, 3.6, 4.68), M['shelf'])
    for k in range(6): dm.box((x0 + 0.08, 0.4 + k * 0.28, 4.68), (x0 + 0.42, 0.62 + k * 0.28, 5.1 + 0.05 * (k % 3)), M['books'][k % 5])
    rod(dm, (x0 + 0.25, 2.6, 4.68), (x0 + 0.25, 2.6, 5.1), 0.12, M['zinc'], seg=8)
    for (bx_, by_, yaw_) in ((-1.25, 1.0, 0.3), (-1.0, 1.35, 0.1)):                                                 # his boots, a chamber pot, a rolled paper under the bed
        c_ = Vector((bx_, by_, 0)); d_ = Vector((math.cos(yaw_), math.sin(yaw_), 0))
        obox(dm, c_ + Vector((0, 0, 0.12)), d_, Vector((-d_.y, d_.x, 0)), Vector((0, 0, 1)), 0.32, 0.12, 0.12, M['black']); rod(dm, c_ - d_ * 0.18, c_ - d_ * 0.18 + Vector((0, 0, 0.55)), 0.13, M['black'], seg=8)
    rod(dm, (-3.2, 4.0, 0), (-3.2, 4.0, 0.42), 0.26, M['basin'], seg=14, r1=0.3)
    rod(dm, (-2.2, 1.3, 0.08), (-1.6, 1.0, 0.08), 0.08, M['white'], seg=8)
    _obj(dm, 'attic_dressing', SET, hull=0.01); _obj(fl, 'attic_flame', SET, shadow=False); _obj(cards, 'attic_halos', SET, shadow=False)
    _flame_light('candle', tuple(f + Vector((0, 0, 0.05))), CANDLE, 60 * P.get('gas', 1.0), radius=0.08, shadow=True)
    _flame_light('candle_floor', tuple(f2 + Vector((0, 0, 0.05))), CANDLE, 30 * P.get('gas', 1.0), radius=0.08, shadow=True)
    pl2 = MB(); pl2.quad((f2.x - 1.5, f2.y - 1.5, 0.01), (3, 0, 0), (0, 3, 0), M['pool'], (0, 0, 1, 1)); _obj(pl2, 'floor_candle_pool', SET, shadow=False)
    BK._light('window_fill', ((wx0 + wx1) / 2, y1 - 0.6, 3.4), (1.0, 0.8, 0.6), 90, radius=1.2, shadow=False)
    pl = MB(); pl.quad((tb_.x - 2, tb_.y - 2, 1.556), (4, 0, 0), (0, 4, 0), M['pool'], (0, 0, 1, 1)); _obj(pl, 'candle_pool', SET, shadow=False)
    kd = Vector(P['key_dir']).normalized(); sb = MB()
    corners = [Vector((wx0, yw, wz0)), Vector((wx1, yw, wz0)), Vector((wx1, yw, wz1)), Vector((wx0, yw, wz1))]
    def ext(p): t = p.z / max(0.05, -kd.z); t = min(t, 12.0); return p + kd * t
    mid = lambda p, q: (p + q) / 2
    sb.face([mid(corners[0], corners[3]), mid(corners[1], corners[2]), ext(mid(corners[1], corners[2])), ext(mid(corners[0], corners[3]))], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sb, 'sun_shafts', SET, shadow=False)
    STATE['marks'].update(vincenzo_bed=(-0.9, 2.6, 0.0), vincenzo_table=(1.0, 3.2, 0.0), trunk=tuple(round(v, 3) for v in tr['c0']), window=((wx0 + wx1) / 2, y1, wz0))
    _sky_dome(SET, P, M, STATE['E'], pano=True)

def _shop(SET, P, M, dress):
    """The Florence art dealer's shop (1913): green damask walls hung salon-fashion with gilt-framed pictures, gilded empty frames
    leaning, glass cabinets of maiolica and bronzes, a marble bust on a column, a carved desk with a green-shaded oil lamp and the
    panel on it (set_panel), a brass chandelier with candles, the shop window onto Florence (the Duomo)."""
    x0, x1, y0, y1 = SHOP; h = SHOP_H
    mb = MB(); fl = MB(); cards = MB()
    mb.quad((x0, y0, 0), (x1 - x0, 0, 0), (0, y1 - y0, 0), M['parquet'], (x0 / 4, y0 / 4, x1 / 4, y1 / 4))
    mb.quad((x0, y1, h), (x1 - x0, 0, 0), (0, -(y1 - y0), 0), M['coffer'], (0, 0, (x1 - x0) / 2, (y1 - y0) / 2))
    walls = [Frame((x0, y1, 0), 0.0), Frame((x1, y1, 0), -90.0), Frame((x1, y0, 0), 180.0), Frame((x0, y0, 0), 90.0)]
    win = (2.0, 6.5, 1.4, 5.6)                                                                                    # the shop window in the right wall (local u, z)
    for k, F in enumerate(walls):
        L_ = (x1 - x0) if k % 2 == 0 else (y1 - y0)
        F.quad(mb, [(0, 0, 0), (L_, 0, 0), (L_, 0, 1.2), (0, 0, 1.2)], M['wood_d'], [(0, 0), (L_ / 2, 0), (L_ / 2, 0.6), (0, 0.6)], (0, -1, 0))
        if k == 1:
            a, b, c, d = win
            for (u0_, u1_, z0_, z1_) in ((0, a, 1.2, h), (b, L_, 1.2, h), (a, b, 1.2, c), (a, b, d, h)):
                F.quad(mb, [(u0_, 0, z0_), (u1_, 0, z0_), (u1_, 0, z1_), (u0_, 0, z1_)], M['wallpaper_shop'], [(u0_ / 1.2, z0_ / 1.2), (u1_ / 1.2, z0_ / 1.2), (u1_ / 1.2, z1_ / 1.2), (u0_ / 1.2, z1_ / 1.2)], (0, -1, 0))
        else:
            F.quad(mb, [(0, 0, 1.2), (L_, 0, 1.2), (L_, 0, h), (0, 0, h)], M['damask_g'], [(0, 0), (L_, 0), (L_, (h - 1.2) / 1.4), (0, (h - 1.2) / 1.4)], (0, -1, 0))
        F.box(mb, (0, -0.15, 1.12), (L_, 0, 1.3), M['gold_c'], 0.5); F.box(mb, (0, -0.4, h - 0.5), (L_, 0, h), M['cream'], 0.5); F.box(mb, (0, -0.5, h - 0.58), (L_, 0, h - 0.5), M['gold_c'], 0.5)
    _obj(mb, 'shop_shell', SET, hull=0.0)
    F = walls[1]; a, b, c, d = win; wm = MB()
    for u in (a, b - 0.2, (a + b) / 2 - 0.1): F.box(wm, (u, -0.2, c), (u + 0.2, 0.0, d), M['wood_d'])
    for z in (c, d - 0.2, (c + d) / 2): F.box(wm, (a, -0.2, z), (b, 0.0, z + 0.15), M['wood_d'])
    F.box(wm, (a - 0.2, -0.6, c - 0.2), (b + 0.2, 0.0, c), M['wood_d'])
    _obj(wm, 'shop_window', SET, hull=0.01)
    gl = MB(); F.quad(gl, [(a, 0.0, c), (b, 0.0, c), (b, 0.0, d), (a, 0.0, d)], M['glass'], [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], (0, -1, 0)); _obj(gl, 'shop_glass', SET, shadow=False)
    vw = MB(); F2 = Frame((x1 + 14.0, 18.0, -1.0), -90.0)                                                          # Florence beyond (a sunlit plate)
    F2.quad(vw, [(0, 0, 0), (26, 0, 0), (26, 0, 13), (0, 0, 13)], mat_emit(STATE['pre'] + 'e_flo', image=STATE['tx']['florence'], strength=1.0), [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0))
    _obj(vw, 'florence_view', SET, shadow=False)
    cm = MB(); fm = MB()
    _salon_hang(cm, fm, walls[0], 0.3, (x1 - x0) - 0.3, 1.8, h - 0.8, M, 505, tilt_above=99)
    _salon_hang(cm, fm, walls[3], 0.3, (y1 - y0) - 0.3, 1.8, h - 0.8, M, 606, tilt_above=99)
    _obj(cm, 'shop_pictures', SET); _obj(fm, 'shop_frames', SET, hull=0.01)
    dm = MB(); rr = _rnd(71)
    for k in range(4):                                                                                              # empty frames leaning on the left wall
        y = 1.2 + k * 0.5; hh = 1.6 + 0.4 * (k % 2); ww = 1.3 + 0.3 * k
        base = Vector((x0 + 0.25 + 0.1 * k, y, 0.02)); pts = [base, base + Vector((0, ww, 0)), base + Vector((-0.2, ww, hh)), base + Vector((-0.2, 0, hh))]
        pts = [Vector((p.x + 0.0, p.y, p.z)) for p in pts]; _frame_geo(dm, [pts[1], pts[0], pts[3], pts[2]], (1, 0, 0.12), 0.24, 0.12, M['gold'])
    for (cx_, cy_) in ((x0 + 1.0, 7.6), (3.8, y1 - 0.9)):                                                          # glass cabinets with maiolica and bronzes
        dm.box((cx_ - 0.8, cy_ - 0.5, 0), (cx_ + 0.8, cy_ + 0.5, 1.2), M['wood_d']); dm.box((cx_ - 0.8, cy_ - 0.5, 4.2), (cx_ + 0.8, cy_ + 0.5, 4.5), M['wood_d'])
        for (sx, sy) in ((-0.78, -0.48), (0.78, -0.48), (-0.78, 0.48), (0.78, 0.48)): rod(dm, (cx_ + sx, cy_ + sy, 1.2), (cx_ + sx, cy_ + sy, 4.2), 0.04, M['gold_c'], seg=5)
        for z in (2.2, 3.2): dm.box((cx_ - 0.75, cy_ - 0.45, z - 0.03), (cx_ + 0.75, cy_ + 0.45, z), M['glass'])
        for z in (1.2, 2.2, 3.2):
            for i in range(3):
                x = cx_ - 0.5 + i * 0.5; kk = rr.random()
                if kk < 0.5: rod(dm, (x, cy_, z), (x, cy_, z + 0.6), 0.16, rr.choice((M['blue'], M['yellow'], M['white'])), seg=10, r1=0.08)
                else: lumpy(dm, (x, cy_, z + 0.3), 0.2, M['bronze'], int(x * 10 + z * 100), seg=8, rings=5, rough=0.15, squash=1.5)
        F_ = Frame((cx_ - 0.8, cy_ - 0.5, 0), 0.0); F_.quad(cards, [(0.02, -0.01, 1.2), (1.58, -0.01, 1.2), (1.58, -0.01, 4.2), (0.02, -0.01, 4.2)], M['glass'], [(0.1, 0.1), (0.9, 0.1), (0.9, 0.9), (0.1, 0.9)], (0, -1, 0))
    bc = Vector((2.6, 6.8, 0)); rod(dm, bc, bc + Vector((0, 0, 3.0)), 0.35, M['marble_w'], seg=14, r1=0.3); rod(dm, bc + Vector((0, 0, 3.0)), bc + Vector((0, 0, 3.15)), 0.45, M['marble_w'], seg=14)
    lumpy(dm, bc + Vector((0, 0, 3.6)), 0.45, M['marble_w'], 81, seg=12, rings=6, rough=0.08, squash=0.8); lumpy(dm, bc + Vector((0, 0, 4.25)), 0.32, M['marble_w'], 82, seg=12, rings=6, rough=0.05, squash=1.2)
    dk = Vector((-1.2, 3.4, 0))                                                                                     # the desk
    dm.box((dk.x - 1.6, dk.y - 0.8, 1.5), (dk.x + 1.6, dk.y + 0.8, 1.65), M['wood']); dm.box((dk.x - 1.55, dk.y - 0.7, 0), (dk.x - 0.7, dk.y + 0.7, 1.5), M['wood_d'], tile=(1, 1))
    dm.box((dk.x + 0.7, dk.y - 0.7, 0), (dk.x + 1.55, dk.y + 0.7, 1.5), M['wood_d'], tile=(1, 1)); dm.box((dk.x - 1.62, dk.y - 0.82, 1.62), (dk.x + 1.62, dk.y + 0.82, 1.66), M['gold_c'])
    lp = dk + Vector((1.1, 0.4, 1.66)); rod(dm, lp, lp + Vector((0, 0, 0.2)), 0.2, M['brass'], seg=10); rod(dm, lp, lp + Vector((0, 0, 0.75)), 0.05, M['brass'], seg=6)
    fl.sphere(lp + Vector((0, 0, 0.75)), 0.14, M['lamp_glass'], seg=10, rings=5)
    dm.frustum(lp + Vector((0, 0, 0.88)), lp + Vector((0, 0, 1.12)), 0.4, 0.16, M['green'], seg=14, cap0=False, cap1=False)
    lf = lp + Vector((0, 0, 0.75)); _halo(cards, lf, 0.6, M)
    for k in range(3): dm.box((dk.x - 1.3 + k * 0.08, dk.y + 0.3, 1.66 + k * 0.1), (dk.x - 0.6 + k * 0.04, dk.y + 0.75, 1.75 + k * 0.1), M['books'][k])
    pnl = MB(); pnl.oface([(dk.x - 0.5, dk.y - 0.55, 1.68), (dk.x + 0.5, dk.y - 0.55, 1.68), (dk.x + 0.5, dk.y + 0.4, 1.95), (dk.x - 0.5, dk.y + 0.4, 1.95)], M['mona'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -0.3, 1))
    pnl.box((dk.x - 0.55, dk.y - 0.6, 1.65), (dk.x + 0.55, dk.y - 0.52, 1.75), M['red'])
    STATE['shop_panel'] = [_obj(pnl, 'shop_panel', SET)]
    cw = Vector((0.4, 4.6, 5.6)); hoop = [cw + Vector((1.0 * math.cos(2 * math.pi * i / 16), 1.0 * math.sin(2 * math.pi * i / 16), 0)) for i in range(17)]   # chandelier
    chain_rod(dm, hoop, 0.045, M['brass']); rod(dm, cw, (cw.x, cw.y, h), 0.03, M['brass'], seg=5); dm.sphere(cw - Vector((0, 0, 0.2)), 0.2, M['brass'], seg=10, rings=5)
    for i in range(6):
        a_ = 2 * math.pi * i / 6; chain_rod(dm, [cw + Vector((1.0 * math.cos(a_), 1.0 * math.sin(a_), 0)), cw + Vector((0, 0, 0.9))], 0.012, M['brass'])
        f = BK._candle(dm, fl, cw + Vector((1.0 * math.cos(a_), 1.0 * math.sin(a_), 0)), M, h=0.3, r=0.05); _halo(cards, f, 0.35, M)
    for (x, y) in ((x1 - 1.4, 2.0), (-3.6, 1.0)): dm.box((x - 0.4, y - 0.4, 0), (x + 0.4, y + 0.4, 0.9), M['velvet']); dm.box((x - 0.4, y + 0.3, 0.9), (x + 0.4, y + 0.42, 2.2), M['wood_d'])
    sg = MB(); walls[2].quad(sg, [(3.0, -0.02, 5.6), (5.4, -0.02, 5.6), (5.4, -0.02, 6.2), (3.0, -0.02, 6.2)], M['sign_dealer'], [(0, 0), (1, 0), (1, 1), (0, 1)], (0, -1, 0)); _obj(sg, 'dealer_sign', SET)
    _obj(dm, 'shop_dressing', SET, hull=0.01); _obj(fl, 'shop_flames', SET, shadow=False); _obj(cards, 'shop_cards', SET, shadow=False)
    _flame_light('desk_lamp', tuple(lf), LANTERN, 90 * P.get('gas', 1.0), radius=0.15, shadow=True)
    _flame_light('chandelier', tuple(cw + Vector((0, 0, 0.3))), CANDLE, 160 * P.get('gas', 1.0), radius=0.8, shadow=False)
    kd = Vector(P['key_dir']).normalized(); sb = MB(); F = walls[1]
    def ext(p): t = p.z / max(0.05, -kd.z); t = min(t, 14.0); return p + kd * t
    for u in ((a + b) / 2 - 1.0, (a + b) / 2 + 1.0):
        p0, p1 = F.p(u, 0.0, c), F.p(u, 0.0, d); sb.face([p0, p1, ext(p1), ext(p0)], M['shaft'], [(0, 0), (1, 0), (1, 1), (0, 1)])
    _obj(sb, 'sun_shafts', SET, shadow=False)
    STATE['marks'].update(dealer_desk=(-1.6, 5.0, 0.0), vincenzo_shop=(0.9, 3.6, 0.0), police_door=(4.2, 1.0, 0.0))
    STATE['desk'] = tuple(round(v, 3) for v in dk)
    _sky_dome(SET, P, M, STATE['E'], pano=False)

# ============================================================================= hooks
def _flick(frame, seed=0):
    t = float(frame or 0)
    return 1.0 + 0.08 * math.sin(t * 0.83 + seed) + 0.05 * math.sin(t * 2.31 + 1.7 * seed) + 0.04 * math.sin(t * 5.1 + 0.3 * seed)

def set_flames(k=1.0, frame=None):
    """Every gas jet, lantern and candle (light energies and glow materials): 0 out .. 1 normal .. 1.5 bright; deterministic flicker from
    the frame number (call every frame of a shot; keys linear)."""
    k = max(0.0, float(k)); f = frame if frame is not None else bpy.context.scene.frame_current
    for i, (L, base) in enumerate(STATE.get('flames', [])):
        L.data.energy = base * k * _flick(f, i + 1)
        if frame is not None: T._key(L.data, 'energy', frame, 'LINEAR')
    for j, m in enumerate(STATE.get('flame_mats', [])):
        s = m.node_tree.nodes['strength'].inputs['Strength']
        if 'base' not in m: m['base'] = s.default_value
        s.default_value = m['base'] * max(k, 0.0) * _flick(f, 7 + j)
        if frame is not None:
            s.keyframe_insert('default_value', frame=frame)
            for fc in T._fcurves(m.node_tree):
                for kp in fc.keyframe_points: kp.interpolation = 'LINEAR'
    STATE['flames_k'] = k

def set_mona(present, frame=None):
    """The Mona Lisa (canvas, gilt frame, glass box) on the wall (True) or gone (False). The four iron hooks always stay; when she is
    gone the darker unfaded damask rectangle shows where she hung. Visibility keyed constant with frame. Louvre gallery only."""
    if 'mona' not in STATE: return
    T._show(STATE['mona']['objs'], bool(present), frame); T._show([STATE['mona']['patch']], not present, frame)
    STATE['mona_present'] = bool(present)

def set_mona_lift(d, frame=None):
    """Lift the framed painting off its hooks: d (D) up and out from the wall (0 = hanging; 0.3 = clear of the hooks; 0.8 = in his
    hands). Keys the pivot location (Bezier) with frame."""
    if 'mona' not in STATE: return
    piv = STATE['mona']['pivot']; r = Vector(piv['wrest']); piv.location = r + Vector((0.0, -0.9 * d, 0.6 * d))
    if frame is not None: T._key(piv, 'location', frame, 'BEZIER')

def set_queue(on, frame=None):
    """The reopening-day queue ropes (two lanes of stanchions leading to the empty wall). Visibility keyed constant."""
    if STATE.get('queue_obj') is not None: T._show([STATE['queue_obj']], bool(on), frame)

def set_papers(n, frame=None):
    """Paris: how many newspapers / posters with her face are up, 0..24, filled in order: the kiosk front (8), the kiosk sides (4), the
    Morris column (6), the shop shutters (6). Visibility keyed constant."""
    ps = STATE.get('papers', []); n = int(max(0, min(len(ps), n)))
    for i, o in enumerate(ps): T._show([o], i < n, frame)
    STATE['papers_n'] = n

def set_door(angle_deg, frame=None):
    """exit_door: the service door swung inward-left on its hinge, 0 = shut (locked) .. 95 = wide open. The daylight from the courtyard
    (a shadowed area lamp) grows with the opening. Keys Bezier (rotation) / linear (light)."""
    if 'door' not in STATE: return
    a = max(0.0, min(110.0, float(angle_deg))); piv = STATE['door']['pivot']; piv.rotation_euler = (0.0, 0.0, -math.radians(a))
    if frame is not None: T._key(piv, 'rotation_euler', frame, 'BEZIER')
    L = STATE.get('door_light')
    if L is not None:
        L.data.energy = 900.0 * min(1.0, a / 60.0)
        if frame is not None: T._key(L.data, 'energy', frame, 'LINEAR')
    STATE['door_angle'] = a

def set_frame_on_stairs(visible, frame=None):
    """staircase: the empty gilt frame and her glass box left on the steps (visibility keyed constant)."""
    if STATE.get('stair_frame'): T._show(STATE['stair_frame'], bool(visible), frame)

def set_trunk(pull=0.0, open_deg=0.0, panel=True, frame=None):
    """room (attic): the wooden trunk under the bed. pull 0 (under the bed) .. 1 (out in the room, 1.9 D toward +x), open_deg 0 .. 100 the
    lid (it only clears the bed frame once pull > 0.7), panel: the Mona Lisa panel on its red cloth inside. Keys Bezier / constant."""
    if 'trunk' not in STATE: return
    t = STATE['trunk']; r = Vector(t['pivot']['wrest']); t['pivot'].location = r + Vector((1.9 * max(0.0, min(1.0, pull)), 0, 0))
    t['lid'].rotation_euler = (0.0, -math.radians(max(0.0, min(110.0, open_deg))), 0.0)
    if frame is not None: T._key(t['pivot'], 'location', frame, 'BEZIER'); T._key(t['lid'], 'rotation_euler', frame, 'BEZIER')
    T._show([t['panel']], bool(panel), frame)

def set_panel(visible, frame=None):
    """dealer_shop: the panel (on its red cloth) lying on the dealer's desk."""
    if STATE.get('shop_panel'): T._show(STATE['shop_panel'], bool(visible), frame)

def clear_keys():
    """Drop every key the hooks inserted (objects, lamps, materials), so plain set_* calls (no frame) hold again at render time."""
    for idb in list(bpy.data.objects) + list(bpy.data.lights):
        if idb.animation_data: idb.animation_data_clear()
    for m in bpy.data.materials:
        if m.node_tree and m.node_tree.animation_data: m.node_tree.animation_data_clear()

def apply_preset_state(preset):
    """Set state of a preset (also used for the contract stills)."""
    PR = PRESETS[preset]
    if PR['area'] == 'gallery': set_mona(PR.get('mona', True)); set_mona_lift(0.0); set_queue(PR.get('queue', False))
    if PR['area'] == 'street': set_papers(PR.get('papers', 24))
    if PR['area'] == 'exitdoor': set_door(PR.get('door', 0.0))
    if PR['area'] == 'stair': set_frame_on_stairs(PR.get('frame_on_stairs', True))
    if PR['area'] == 'attic': p_, o_ = PR.get('trunk', (0.0, 0.0)); set_trunk(p_, o_)
    if PR['area'] == 'shop': set_panel(PR.get('panel', True))
    set_flames(1.0)

# ============================================================================= cameras, anchors, staging
CAMS = dict(
    gallery=dict(gallery_wide=dict(loc=(9.9, 1.3, 3.6), look_at=(-3.6, 21.0, 4.7), lens=22),
                 wall_eye=dict(loc=(0.6, 14.6, 2.8), look_at=(-0.2, 22.0, 3.5), lens=24),
                 empty_wall_queue=dict(loc=(3.2, 10.0, 6.8), look_at=(-0.3, 22.0, 2.2), lens=22),
                 service_door=dict(loc=(-2.0, 12.0, 3.6), look_at=(8.6, 0.0, 2.6), lens=22)),
    closet=dict(closet=dict(loc=(2.0, 0.45, 3.3), look_at=(-1.3, 3.1, 1.7), lens=20)),
    stair=dict(staircase=dict(loc=(0.9, -2.6, 2.6), look_at=(-0.4, 8.0, 5.4), lens=22)),
    exitdoor=dict(exit_door=dict(loc=(1.5, 3.4, 2.5), look_at=(-0.3, 10.0, 3.1), lens=22)),
    street=dict(street_wide=dict(loc=(-2.4, -9.0, 4.2), look_at=(1.0, 20.0, 5.4), lens=22),
                kiosk=dict(loc=(-1.5, 6.3, 2.6), look_at=(-4.8, 10.6, 2.4), lens=22),
                notre_dame_view=dict(loc=(1.5, 40.0, 3.0), look_at=(3.0, 108.0, 16.0), lens=22)),
    attic=dict(room_wide=dict(loc=(3.7, 0.2, 3.0), look_at=(-0.4, 4.5, 1.5), lens=18),
               under_bed_insert=dict(loc=(1.5, 0.7, 0.95), look_at=(-2.0, 2.9, 0.45), lens=22)),
    shop=dict(dealer_shop=dict(loc=(4.8, 0.4, 4.4), look_at=(-2.2, 6.2, 2.3), lens=20)),
)
CAM_NOTES = dict(
    gallery_wide='from the service-door corner across the Salon Carre: the salon hang floor to ceiling on three walls, the huge feast canvas left, the divan and urn, the skylight with its bars, the patterned sun on the back wall and floor; she is small on the back wall behind the rope',
    wall_eye='eye level at the rope before her: the Mona Lisa small in her gilt frame and glass, the neighbours hung tight round her, the torcheres either side; set_mona / set_mona_lift',
    empty_wall_queue='the reopening: the empty wall with the four hooks and the unfaded patch, the queue lanes of rope, the crowd (staged) staring; set_mona(False)',
    service_door='reverse: from the back across the room to the service door (front wall, right) and the guard chair',
    closet='inside the storage closet by the lantern: shelves of tins, brooms, buckets, the white smocks on pegs, the light under the door; he hides at the back',
    staircase='from the foot of the service stair up the flight: the gas brackets, the morning shaft from the landing window, the empty frame and glass on the steps',
    exit_door='before the locked service door: the fanlight daylight, the lock without its knob, gas brackets; set_door opens it on the bright courtyard',
    street_wide='down the rue toward the quai: Haussmann rows both sides, the cafe awning, the kiosk and Morris column with her face, the fiacre, gas lamps; Notre-Dame far at the end',
    kiosk='close on the green newspaper kiosk: the front pages with her face (set_papers), the Morris column behind',
    notre_dame_view='at dusk near the quai: the river and Notre-Dame\'s two towers standing, lamps lit',
    room_wide='the attic room at dusk from the door corner: the iron bed with the trunk under it, the dormer window on the rooftops, the candle on the table, the smock on its peg',
    under_bed_insert='low at the floor: the wooden trunk under the bed (set_trunk pull / lid / panel)',
    dealer_shop='the Florence dealer\'s shop: salon-hung walls, gilt frames, cabinets, the bust, the desk with the panel on it and the lamp, the window on the Duomo',
)

HEIGHT = dict(vincenzo=2.75, director=3.6, guard=3.2, worker=3.0, plumber=3.0, woman=2.9, man=3.0, painter=3.0, police=3.2, dealer=3.1, newsboy=2.4)
T.PH.update(
    vincenzo=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), HEIGHT['vincenzo']),
    director=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), HEIGHT['director']),
    guard=('senior_a', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['guard']),
    worker=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['worker']),
    plumber=('beach_man', dict(yaw=0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['plumber']),
    woman=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['woman']),
    man=('beach_man', dict(yaw=0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['man']),
    dealer=('boss', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['dealer']),
    newsboy=('beach_kid', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), HEIGHT['newsboy']))
placeholder_actor = T.placeholder_actor

STAGING = dict(
    gallery_wide=[('guard', (4.6, 8.4, 0)), ('woman', (-3.4, 14.6, 0)), ('man', (-1.2, 17.0, 0)), ('director', (2.8, 13.6, 0))],
    wall_eye=[('vincenzo', (1.7, 21.1, 0))],
    empty_wall_queue=[('woman', (-1.1, 19.4, 0)), ('man', (0.9, 18.9, 0)), ('woman', (-0.2, 17.7, 0)), ('man', (1.3, 16.6, 0)), ('woman', (-1.0, 16.2, 0)), ('guard', (4.0, 19.8, 0))],
    service_door=[('guard', (6.6, 2.2, 0))],
    closet=[('vincenzo', (-0.9, 1.6, 0))],
    staircase=[('vincenzo', (0.2, 4.2, 2.88))],
    exit_door=[('vincenzo', (0.9, 8.0, 0))],
    street_wide=[('woman', (-5.2, 8.0, 0.25)), ('man', (5.0, 6.5, 0.25)), ('newsboy', (-3.4, 3.0, 0.0)), ('man', (-1.0, 14.0, 0.0))],
    kiosk=[('man', (-3.3, 13.8, 0.0)), ('newsboy', (-2.3, 12.2, 0.0))],
    notre_dame_view=[('woman', (0.4, 54.0, 0.0)), ('man', (3.0, 56.0, 0.0))],
    room_wide=[('vincenzo', (-0.2, 2.3, 0))],
    under_bed_insert=[],
    dealer_shop=[('dealer', (-1.6, 5.0, 0)), ('vincenzo', (0.9, 3.6, 0))],
)

def anchors():
    P = STATE['P']; area = STATE['area']; cams = {k: dict(v) for k, v in CAMS[area].items()}
    A = dict(location=STATE['loc'], preset=STATE['preset'], area=area, light=STATE['light'], cams=cams, cam=dict(CAMS[area][PRESETS[STATE['preset']]['cam']]),
             cam_name=PRESETS[STATE['preset']]['cam'], cam_notes={k: CAM_NOTES.get(k, '') for k in cams},
             render=dict(samples_final=12, resolution=(720, 1280), threads=2, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()),
             sun_elevation_deg=P['sun_elev'], floor_z=0.0, heights=dict(HEIGHT), marks=dict(STATE.get('marks', {})),
             lights=[o.name for o in STATE['LIGHTS'].objects], staging={k: v for k, v in STAGING.items() if k in cams})
    if area == 'gallery':
        A.update(room=dict(x=GAL[:2], y=GAL[2:], wall_top=GAL_H, cornice=CORN, laylight=LAY_Z, skylight=SKY_OPEN), mona=dict(centre=MONA_C, canvas=(MONA_W, MONA_H), frame_w=MONA_FW, wall_y=GAL[3],
                 hooks=[(MONA_C[0] + hx, GAL[3], hz) for (hx, hz) in HOOKS], lift_dir='(0, -0.9, 0.6) per D of set_mona_lift'), service_door=SERVICE_DOOR,
                 marks=dict(A['marks'], rope_line=dict(y=20.4, x=(-2.6, 2.6)), queue_lanes=dict(x=(-2.6, 2.6), y=(14.6, 20.4)), divan=dict(centre=(0.0, 10.0), r=1.9),
                            guard_chair=(6.6, 1.2, 0.0), mona_viewer=(0.0, 19.6, 0.0), thief_at_wall=(0.9, 21.0, 0.0), director=(3.0, 13.0, 0.0), copyist_easel=(-6.2, 13.5, 0.0)),
                 keep_out='walls |x| > 12.6, y < 0.4, y > 21.6; divan r 1.95 at (0, 10); benches x +-5.5..9.5 y 5.4..6.6; torcheres 0.5 round (+-5.2, 20.6), (-11.6, 2.4), (11.6, 12); easel (-6.2, 13.5); ladder x > 10.9 y 15.5..16.5')
    elif area == 'street':
        A.update(street=dict(STREET), kiosk=STATE['kiosk'], morris=STATE['morris'], papers=len(STATE['papers']), notre_dame=dict(plate_centre=(5.0, 108.0), size=(72.0, 60.0)),
                 keep_out='blocks |x| > 7; kiosk 1.2 round its centre; Morris column r 1.1; fiacre x 0.6..3.0 y 17..25; cafe tables x 5.2..6.6 y 4.5..11.8; lamps along x +-4.5')
    elif area == 'attic':
        A.update(room=dict(x=ATTIC[:2], y=ATTIC[2:], height=ATTIC_H, knee=4.2), trunk=dict(rest=STATE['trunk']['c0'], pull_dir=(1.9, 0, 0), size=(1.0, 1.5, 0.82)),
                 bed=dict(x=(-3.9, -1.8), y=(0.6, 4.6), mattress_z=1.45, clear_under=1.0), keep_out='bed x < -1.7 y 0.5..4.7; table (0.9, 4.7) 0.9; washstand x > 2.3 y 4..5.2; chair (1.9, 4.5)')
    elif area == 'shop':
        A.update(room=dict(x=SHOP[:2], y=SHOP[2:], height=SHOP_H), desk=STATE['desk'], keep_out='desk x -2.8..0.4 y 2.6..4.2; cabinets (-5, 7.6) (3.8, 8.1); bust (2.6, 6.8); chairs (4.6, 2) (-3.6, 1)')
    elif area == 'stair':
        A.update(stair=STATE['stair'], keep_out='walls |x| > 2.0; actors on a step: z = (k + 1) x 0.36 at y in k x 0.6 .. (k + 1) x 0.6')
    elif area == 'exitdoor':
        A.update(door=dict(hinge=(-1.1, 9.88, 0.0), width=2.2, height=4.4, swing='inward-left (-z rotation)'), keep_out='walls |x| > 2.8; bench x > 2.1 y 2.5..6; the door swing r 2.3 round the hinge')
    elif area == 'closet':
        A.update(room=dict(x=(-2.6, 2.6), y=(0.0, 3.6), height=6.0), keep_out='shelves y > 2.85; crates x -1.4..0.2 y 1.8..3; buckets; brooms x < -1.9')
    return A

def stage_placeholders(A, cam_name, cam_loc):
    """Placeholder actors for the contract stills (STAGING[cam_name]); cards face the camera."""
    T._clear_actors(); out = []
    for i, (role, mk) in enumerate(STAGING.get(cam_name, [])):
        d = Vector(cam_loc) - Vector(mk); el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(placeholder_actor(role, mk, face_to=cam_loc, tilt=max(0.0, el - 35) * 0.6, name='actor_%s_%d' % (role, i)))
    return out

def head_pixels(cam_name):
    """[(role, mark, head_centre_y_px, head_px, chin_y_px, feet_y_px)] at 720x1280 for the staged roles (caption rule: chin < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for i, (role, mk) in enumerate(STAGING.get(cam_name, [])):
        h = HEIGHT[role]; m = Vector(mk); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((role, tuple(mk), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

# ----------------------------------------------------------------------------- CLI
def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_render(loc, presets=None, quality='final', outdir=None, actors=True, extra_cams=False):
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for pr in (presets or LOC_PRESETS[loc]):
        A = build(loc, pr); sc = bpy.context.scene; setup_render(sc, quality)
        names = [A['cam_name']] + ([k for k in A['cams'] if k != A['cam_name']] if extra_cams else [])
        for nm in names:
            cs = A['cams'][nm]; make_camera(cs)
            if actors: stage_placeholders(A, nm, cs['loc'])
            bpy.context.view_layer.update(); hp = head_pixels(nm)
            w, c = render(os.path.join(outdir, '%s_%s.png' % (pr, nm) if nm != pr else '%s.png' % pr)); res[(pr, nm)] = (round(w, 1), round(c, 1), hp)
            print('%s %s %s %s: %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, loc, pr, nm, w, c, _load(), hp), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('final', 'stills'):
        cli_render(arg[0] if arg else 'louvre', arg[1:] or None, 'final' if cmd == 'final' else 'preview', extra_cams=os.environ.get('EXTRA') == '1')
    elif cmd == 'digest':
        A = build(arg[0] if arg else 'louvre', arg[1] if len(arg) > 1 else None); bpy.context.view_layer.update(); print('digest', digest())
    else: print(__doc__)
