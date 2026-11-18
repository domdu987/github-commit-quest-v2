#!/usr/bin/env python3
"""dairy.py : FULL 3D SET of film 11 ("ไอ้หมอวัว", Jenner, cowpox, Berkeley 1796) as a Blender set (bpy 5.x, Cycles CPU, 720x1280, 1 unit = 1 D = a head).
Three locations, 11 presets (each = location + light + camera + stand points + hooks):

    import dairy as D
    A = D.build('barn_milking')                      # barn: barn_wide | barn_milking | barn_high | barn_door
    A = D.build('garden_hut', light='A')             # village: garden_hut | lane_wide | lane_high | garden_queue
    A = D.build('room_night')                        # cottage: room_day | room_night | room_morning
    cam = D.make_camera(A['cam'])                    # THIS make_camera (far clip, no DOF)
    A['stand']['sarah']                              # {pos (x, y, floor z), role, height, ...}: named floor marks per preset
    D.stage_placeholders(A, 'barn_milking')          # placeholder_actor cards on the stand points (stills and tests only)

Light states: A = golden morning (key sun ~20-34 deg, honey light, blue-violet shade), C = late amber (low sun, deeper shade). One hard key
sun with cast shadows + a no-shadow warm bounce sun. NO depth of field, NO text. Frame-driven animation hooks (cow tail / ears, hens
pecking, swinging lanterns, dust motes, smoke, falling leaves, candle flicker): drivers on `frame`, nothing is keyed.
CLI: python3 dairy.py finals [preset ...] | stills [preset ...] | digest <preset>     (see API.md)"""
import os, sys, math, time, json, random
import numpy as np
import bpy
from mathutils import Vector

import dairy_geo as G
from dairy_geo import (R, sm, ell, bx, post, cone, tri, loft, tube, stamp, mk_obj, drv, hook, strand_tuft, hay_heap, straw_floor, bale, cow, hen, hen_local, cat_local, dog_local,
                       goose_local, pail_local, stool_local, barrel_local, churn_local, basket_local, crate_local, sack_local, fork_local, wheel, wheelbarrow, swing_lantern,
                       grass_tuft, flower_local, scatter_flowers, scatter_grass, tree, drystone, thatch_roof, chimney, casement, door, smoke_puffs, falling_leaves, sway)
import tower as T                                       # noqa: E402
import mine as MN                                       # noqa: E402
import wall as W9                                       # noqa: E402
import dairy_tex as X                                   # noqa: E402
from tower import MB, no_bounce, setup_grade, mat_emit  # noqa: E402
from mine import obox, beam, rod, lumpy, _untoon        # noqa: E402
HERE = G.HERE; STATE = T.STATE; WORK = os.path.join(HERE, 'dairy_work')
FORM = (0.0, -0.05, 0.22)

# ============================================================================= light states
def _base(**k):
    d = dict(toon=1.0, key_desat=0.0, ink='#24160e', night=False, form=FORM, bloom_size=0.05, sun_angle=0.6, wet=0.0, lamps=1.0, grade_saturation=1.18); d.update(k); return d
LIGHTS = dict(
    A=_base(key=(1.95, 1.50, 0.88), key_dir=W9._kdaz(205, 20), shade=(0.102, 0.136, 0.34), shade_tint=(0.087, 0.118, 0.37), shade_mix=0.62, lift=(0.010, 0.018, 0.036),
            grade_offset=(-0.006, -0.01, -0.014), bounce=(1.0, 0.66, 0.36, 0.20), beams=0.03, air=('#f4cf94', 0.30, 14.0, 160.0), sky='day', sun_elev=20),
    C=_base(key=(2.25, 1.28, 0.50), key_dir=W9._kdaz(185, 11), shade=(0.070, 0.105, 0.36), shade_tint=(0.06, 0.10, 0.41), shade_mix=0.8, lift=(0.002, 0.008, 0.026),
            grade_offset=(-0.004, -0.010, -0.008), bounce=(1.0, 0.55, 0.30, 0.10), beams=0.03, air=('#f0a870', 0.34, 14.0, 160.0), sky='eve', sun_angle=0.5, grade_saturation=1.15, sun_elev=11),
)
SKY = dict(day=dict(top='#5a8ae0', mid='#8ab4ee', hor='#f6e2bc', cloud_lit='#fff2dc', cloud_sh='#b6b2e8'),
           eve=dict(top='#4c64c8', mid='#9a98dc', hor='#f8c892', cloud_lit='#ffe2b4', cloud_sh='#9a8ad0'))

# ============================================================================= presets, cameras, stand points
ADULT, BOY = 3.2, 2.3                                    # 1 D = head: adults 3.1-3.4 D, the 8-year-old boy 2.3 D
ROLES = dict(jenner=3.3, boy=BOY, sarah=3.1, maid=3.1, doctor=3.4, mother=3.1, villager=3.2, villager_p=3.2, cow=0.0)
PRESETS = dict(
    barn_wide=dict(loc='barn', light='A', cam='barn_wide', sun=(205, 20), look_az=100),
    barn_milking=dict(loc='barn', light='A', cam='barn_milking', sun=(205, 20), look_az=90),
    barn_high=dict(loc='barn', light='C', cam='barn_high', sun=(185, 11), look_az=70),
    barn_door=dict(loc='barn', light='A', cam='barn_door', sun=(240, 22), look_az=180),
    garden_hut=dict(loc='village', light='A', cam='garden_hut', sun=(300, 34), look_az=165),
    lane_wide=dict(loc='village', light='A', cam='lane_wide', sun=(310, 33), look_az=182),
    lane_high=dict(loc='village', light='A', cam='lane_high', sun=(300, 36), look_az=95),
    garden_queue=dict(loc='village', light='A', cam='garden_queue', sun=(300, 36), look_az=100),
    room_day=dict(loc='cottage', light='A', cam='room_day', sun=(135, 38), look_az=90),
    room_night=dict(loc='cottage', light='C', cam='room_night', sun=(140, 8), look_az=90, candle=True),
    room_morning=dict(loc='cottage', light='A', cam='room_morning', sun=(140, 28), look_az=90),
)
LOC_PRESETS = {l: [k for k, v in PRESETS.items() if v['loc'] == l] for l in ('barn', 'village', 'cottage')}
LOC_LIGHTS = dict(barn=['A', 'C'], village=['A', 'C'], cottage=['A', 'C'])

CAMS = dict(
    barn_wide=dict(loc=(0.0, -1.0, 2.8), look_at=(-0.6, 15.0, -0.9), lens=22),
    barn_milking=dict(loc=(-1.0, 6.2, 1.5), look_at=(-4.6, 15.0, 2.5), lens=22),
    barn_high=dict(loc=(5.4, -3.0, 7.6), look_at=(-3.4, 15.0, -0.2), lens=22),
    barn_door=dict(loc=(5.0, 15.6, 1.1), look_at=(-12.0, 15.6, 3.0), lens=22),
    garden_hut=dict(loc=(3.5, -6.6, 1.5), look_at=(-10.0, 0.8, 2.6), lens=22),
    lane_wide=dict(loc=(34.0, -12.5, 1.7), look_at=(-30.0, -10.0, 4.5), lens=22),
    lane_high=dict(loc=(14.0, -34.0, 14.0), look_at=(-2.0, -10.0, 1.0), lens=22),
    garden_queue=dict(loc=(2.0, -15.0, 3.2), look_at=(-3.0, -2.5, 2.4), lens=22),
    room_day=dict(loc=(2.5, -6.0, 3.2), look_at=(-1.0, 4.0, 2.6), lens=22),
    room_night=dict(loc=(2.5, -6.0, 3.0), look_at=(-1.0, 4.0, 2.6), lens=22),
    room_morning=dict(loc=(2.5, -6.0, 3.2), look_at=(-1.0, 4.0, 2.6), lens=22),
)
CAM_NOTES = dict(
    barn_wide='eye-level wide from the barn front (golden morning): the open door and its sun pool left, the cow stalls right, the hay loft at the back, hens and tools along the whole lower third',
    barn_milking='low medium on the milking nook inside the door: stool and pail at the cow flank, sun pool, the stalls and bg cows behind',
    barn_high='high angle (amber C): the door crowd left against the clear-faced milkmaids in the sun pool, floor props everywhere',
    barn_door='low angle from inside out through the open door: sunny lane, wall, wagon, trees, hills, cumulus, sun shafts',
    garden_hut='Jenner garden: the rustic thatched hut with the boy on his stool, the cottage and church tower behind, flower beds all round',
    lane_wide='the village lane at eye level looking toward the church: stone cottages both sides, villagers, the doctor arrives',
    lane_high='high angle over the lane and green: the crowd in the middle, cottages, church tower, hills',
    garden_queue='side view across the picket fence: the long queue from the gate to the hut door, flower beds, orchard, church tower',
    room_day='Phipps room: bed under the window (left), table, hearth, daylight shaft',
    room_night='same room at late-amber dusk: candle on the table, the open door (right) for the doctor, deep blue-violet shade',
    room_morning='same room in morning sun: the bed, the floor space for the jump out of bed',
)

def _mk(role, pos, face='cam', note='', **kw): d = dict(pos=tuple(pos), role=role, height=ROLES[role], face=face, note=note); d.update(kw); return d
# STAND POINTS: name -> dict(pos=(x, y, floor z), role, height (D), note). z is the CONTACT z (floor, or the stool top for seated figures).
STAND = dict(
    barn_wide=dict(sarah=_mk('sarah', (-3.4, 11.8, 0.0), note='milkmaid Sarah Nelmes, standing in the sun pool by the stool'), maid=_mk('maid', (0.4, 12.6, 0.0), note='2nd milkmaid'),
                   jenner=_mk('jenner', (-6.4, 10.0, 0.0), note='Jenner at the door side'), blossom=_mk('cow', (-1.6, 16.2, 0.0), note='Blossom 2D puppet, side view, head to -x, 4.4 D long', length=4.4),
                   boy=_mk('boy', (2.0, 9.0, 0.0), note='James near the aisle')),
    barn_milking=dict(sarah=_mk('sarah', (-5.2, 13.0, 0.85), seated=True, note='milkmaid SEATED on the milking stool (z = stool top)'), blossom=_mk('cow', (-3.4, 15.4, 0.0), note='Blossom 2D, side view, flank to camera', length=4.4),
                      maid=_mk('maid', (-8.0, 12.0, 0.0), note='2nd milkmaid standing left'), pail=_mk('cow', (-4.0, 13.6, 0.0), note='pail under the udder (3D pail already there)', length=0.0)),
    barn_high=dict(sarah=_mk('sarah', (-3.0, 12.2, 0.0), note='clear-faced milkmaid'), maid=_mk('maid', (-0.8, 13.6, 0.0), note='clear-faced milkmaid 2'),
                   vill_a=_mk('villager_p', (-8.8, 12.4, 0.0), note='pockmarked villager in the door'), vill_b=_mk('villager_p', (-9.6, 15.2, 0.0), note='pockmarked villager in the door'),
                   vill_c=_mk('villager_p', (-8.6, 18.0, 0.0), note='pockmarked villager in the door'), vill_d=_mk('villager', (-11.4, 14.0, 0.0), note='plain villager outside the door'),
                   blossom=_mk('cow', (-4.2, 17.4, 0.0), length=4.4)),
    barn_door=dict(sarah=_mk('sarah', (-3.5, 14.6, 0.0), note='milkmaid in the foreground, back to the light'), jenner=_mk('jenner', (-12.5, 17.0, 0.0), note='Jenner on the lane in the sun'),
                   vill_a=_mk('villager', (-14.5, 13.6, 0.0)), vill_b=_mk('villager_p', (-16.0, 19.0, 0.0)), blossom=_mk('cow', (-2.0, 12.0, 0.0), length=4.4)),
    garden_hut=dict(boy=_mk('boy', (-7.6, -2.2, 0.8), seated=True, note='James SEATED on the stool at the hut door (z = stool top)'), jenner=_mk('jenner', (-6.4, -0.6, 0.0), note='Jenner with the lancet, beside the boy'),
                    sarah=_mk('sarah', (-3.4, -3.6, 0.0), note='milkmaid at the path'), doctor=_mk('doctor', (-0.2, -4.2, 0.0), note='town doctor at the gate')),
    lane_wide=dict(doctor=_mk('doctor', (4.0, -11.4, 0.0), note='town doctor arriving, centre of the lane'), villager_a=_mk('villager', (-1.5, -9.6, 0.0)), villager_b=_mk('villager_p', (11.0, -10.8, 0.0)),
                   villager_c=_mk('villager', (-8.0, -13.0, 0.0)), maid=_mk('maid', (-4.5, -9.0, 0.0)), jenner=_mk('jenner', (-12.0, -9.6, 0.0)), boy=_mk('boy', (7.5, -9.0, 0.0))),
    lane_high=dict(**{'c%d' % i: _mk('villager' if i % 3 else 'villager_p', p, note='crowd slot %d' % i) for i, p in enumerate(
        [(-6.0, -16.0, 0.0), (-3.2, -13.2, 0.0), (-0.4, -16.4, 0.0), (2.4, -13.0, 0.0), (5.2, -16.0, 0.0), (8.0, -13.4, 0.0), (-4.6, -9.6, 0.0), (0.4, -10.4, 0.0), (5.0, -9.6, 0.0)])},
                   doctor=_mk('doctor', (0.8, -19.2, 0.0), note='the mocking doctor at the front of the crowd')),
    garden_queue=dict(**{'q%d' % i: _mk('villager' if i % 3 else 'villager_p', (4.6 - i * 1.9, -3.2, 0.0), note='queue slot %d (0 = near the gate)' % i) for i in range(7)},
                      jenner=_mk('jenner', (-9.0, -1.5, 0.0), note='Jenner at the hut door'), boy=_mk('boy', (-8.0, -3.4, 0.0), note='James first in the queue'), doctor=_mk('doctor', (8.2, -3.6, 0.0), note='the mocker, rolls up his sleeve at the tail')),
    room_day=dict(mother=_mk('mother', (-0.4, 1.6, 0.0), note='mother by the bed'), boy_bed=_mk('boy', (-4.2, 5.2, 1.65), pose='in bed', note='James lying in bed: z = mattress top, pillow at the window end'),
                  jenner=_mk('jenner', (1.9, 0.2, 0.0), note='Jenner at the bedside')),
    room_night=dict(mother=_mk('mother', (-1.2, 1.8, 0.0)), boy_bed=_mk('boy', (-4.2, 5.2, 1.65), pose='in bed', note='feverish in bed'), doctor=_mk('doctor', (5.0, 0.8, 0.0), note='town doctor in the doorway, pointing'),
                    jenner=_mk('jenner', (1.3, 1.2, 0.0), note='Jenner')),
    room_morning=dict(boy=_mk('boy', (-1.8, 2.4, 0.0), note='James jumps out of bed (floor)'), mother=_mk('mother', (1.6, 1.8, 0.0), note='mother'), boy_bed=_mk('boy', (-4.2, 5.2, 1.65), pose='in bed')),
)
STAGING = dict(barn_wide=['sarah', 'maid', 'jenner'], barn_milking=['sarah', 'maid'], barn_high=['sarah', 'maid', 'vill_a', 'vill_b', 'vill_c', 'vill_d'], barn_door=['sarah', 'jenner', 'vill_a'],
               garden_hut=['boy', 'jenner', 'sarah'], lane_wide=['doctor', 'villager_a', 'villager_b', 'villager_c', 'maid'], lane_high=['c%d' % i for i in range(9)] + ['doctor'],
               garden_queue=['q%d' % i for i in (0, 1, 2, 4, 6)] + ['jenner', 'boy'], room_day=['mother', 'boy_bed', 'jenner'], room_night=['mother', 'boy_bed', 'doctor'], room_morning=['boy', 'mother'])
T.PH.update(jenner=('boss', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['jenner']), sarah=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['sarah']),
            maid=('beach_woman', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['maid']), doctor=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), ROLES['doctor']),
            mother=('beach_woman', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['mother']), villager=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['villager']),
            villager_p=('senior_a', dict(yaw=0.4, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['villager_p']), boy=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), BOY))

# ============================================================================= scene setup / materials
def new_scene(lkey, sun=None):
    scene = bpy.context.scene; P = dict(LIGHTS[lkey])
    if sun: P['key_dir'] = W9._kdaz(*sun); P['sun_elev'] = sun[1]
    for ob in list(scene.objects): bpy.data.objects.remove(ob, do_unlink=True)
    for ac in list(bpy.data.actions): bpy.data.actions.remove(ac)
    for coll in (bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)
    for m in list(bpy.data.materials): bpy.data.materials.remove(m)
    STATE.clear(); STATE['P'] = P; STATE['loc'] = 'dairy'; STATE['light'] = lkey; STATE['hooks'] = []
    SET = T._coll('SET', scene); LIG = T._coll('LIGHTS', scene); T._wipe(SET); T._wipe(LIG); STATE['SET'] = SET; STATE['LIGHTS'] = LIG
    w = bpy.data.worlds.get('W_dairy') or bpy.data.worlds.new('W_dairy'); scene.world = w; nt = T._tree(w)
    bg = nt.nodes.new('ShaderNodeBackground'); wo = nt.nodes.new('ShaderNodeOutputWorld'); bg.inputs['Color'].default_value = (0, 0, 0, 1); bg.inputs['Strength'].default_value = 0.0
    nt.links.new(bg.outputs['Background'], wo.inputs['Surface'])
    MN.setup_render(scene, 'final'); scene.frame_start = 1; scene.frame_end = 300; scene.frame_current = 1; scene.render.threads_mode = 'FIXED'; scene.render.threads = 4
    scene.cycles.samples = 12
    pre = 'DY_%s_' % lkey; cache = {}
    def C(hexcol, gain=1.0, sm=1.0, form=True, smix=None):
        k = ('c', hexcol, gain, sm, form, smix)
        if k not in cache: cache[k] = _untoon(T.mat_lit(pre + 'c%d' % len(cache), hexcol, gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
        return cache[k]
    def TX(name, gain=1.0, sm=1.0, form=True, smix=None):
        k = ('t', name, gain, sm, form, smix)
        if k not in cache: cache[k] = _untoon(T.mat_lit(pre + 't%d' % len(cache), image=X.get(name), gain=gain, shade_mul=sm, form=FORM if form else None, shade_mix=smix))
        return cache[k]
    def E(hexcol, k=1.0):
        key = ('e', hexcol, k)
        if key not in cache: cache[key] = mat_emit(pre + 'e%d' % len(cache), hexcol, strength=k)
        return cache[key]
    STATE.update(C=C, TX=TX, E=E)
    kd = Vector(P['key_dir']).normalized(); k = max(P['key'])
    d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key']); d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
    sun_o = bpy.data.objects.new('key_sun', d); LIG.objects.link(sun_o); sun_o.rotation_euler = (-kd).to_track_quat('Z', 'Y').to_euler(); sun_o.location = (0, 0, 60); STATE['sun'] = sun_o
    br, bg_, bb, bk = P['bounce']; bd = Vector((-kd.x * 0.5, -kd.y * 0.5, 0.75)).normalized()
    d2 = bpy.data.lights.new('bounce_sun', 'SUN'); d2.color = (br, bg_, bb); d2.energy = math.pi * k * bk; d2.angle = math.radians(20); d2.use_shadow = False
    o2 = bpy.data.objects.new('bounce_sun', d2); LIG.objects.link(o2); o2.rotation_euler = (-bd).to_track_quat('Z', 'Y').to_euler()
    return scene, SET, P, kd

def finish(scene, SET, P):
    scene.cycles.use_light_tree = False; MN._denoise(scene); setup_grade(scene); W9._air_comp(scene, P)
    for ob in SET.objects: no_bounce(ob)

def mats(C, TX, E):
    return dict(
        oak=TX('planks', 1.0), oak_d=TX('planks_dark', 0.95), silver=TX('planks_silver', 1.0), floorw=TX('wood_floor', 1.0), hay=TX('hay2', 0.92, 1.7, smix=0.3), hayc=TX('hay2', 0.95, 1.8, smix=0.25),
        hayc2=C('#cf9f3c', 0.95, 1.9, smix=0.22), earth=TX('earth', 1.0), lane=TX('lane', 1.0), grass=TX('grass', 1.0), grass_d=TX('grass_d', 0.95), flag=TX('flag', 1.0), cobble=TX('cobble', 1.0),
        stone=TX('stone_wall', 1.0), stone2=TX('stone_grey', 1.0), moss=TX('moss_stone', 1.0), thatch=TX('thatch2', 1.0, 1.3, smix=0.35), thatch_d=TX('thatch_dark', 1.0, 1.3, smix=0.35),
        plaster=TX('plaster2', 1.0), slate=TX('slate', 1.0), hills=TX('hills', 1.0), brick=TX('brick', 1.0), rug=TX('rug', 1.0), quilt=TX('quilt', 1.0),
        cow_a=TX('cow_a', 0.82, 1.3, smix=0.4), cow_b=TX('cow_b', 0.82, 1.3, smix=0.4), cow_white=C('#f0e6cc', 0.85, 1.3, smix=0.4), cow_brown=C('#7a4526', 0.9), cow_dark=C('#3a281c'), cow_pink=C('#e4a090', 0.95), cow_horn=C('#ecdcb0'),
        brown=C('#7a4526'), white=C('#efe4c8'), pink=C('#e8a898'), dark=C('#3e2a1e'), horn=C('#efe2bc'), iron=C('#4c4a58'), wood=C('#a8743c'), wood2=C('#8a5a2e'), twine=C('#6d4a22'),
        milk=C('#f8f0dc'), glow=mat_emit('DY_glow_%s' % STATE['light'], '#ffc46a', strength=7.0), hen=C('#c46a34'), hen2=C('#7a3c1c'), hen_w=C('#efe4c8'), hen_w2=C('#c9b894'), hen_k=C('#4a3a44'), hen_k2=C('#2e2430'),
        comb=C('#d8321e'), beak=C('#e3a63a'), leather=C('#6b3d1e'), brass=C('#d7a43a'), sack=C('#cdb48a'), sack2=C('#b89b6c'), red=C('#b6402e'), green=C('#4a7a38'), door=C('#3f6f7a'),
        cat1=C('#d8873a'), cat2=C('#5a5a68'), catw=C('#efe6d4'), dog=C('#a8743c'), tile=C('#b8553a'), glass=C('#8fb4d0', 1.1), black=C('#2c2430'), straw=C('#e0b84e', 1.0, 1.6, smix=0.3), straw2=C('#c99a3c', 1.0, 1.6, smix=0.3),
        apple=C('#a8c24a'), bloom_w=C('#f7ecdc'), bloom_p=C('#f2b6c8'), wicker=C('#b88a4c'), wicker2=C('#8a6232'), egg=C('#f0e2c4'), cabbage=C('#9cc07a'), shutter=C('#4f7a8a'),
        shaft=mat_emit('DY_shaft_%s' % STATE['light'], '#ffd596', strength=0.20, additive=True, camera_only=True), mote=mat_emit('DY_mote_%s' % STATE['light'], '#fff0c0', strength=3.2),
        cream=C('#efe2bd'), blue=C('#3f5fb8'), violet=C('#7a62c8'), yellow=C('#f0c43a'), orange=C('#e8802a'), rose=C('#d8586a'), lav=C('#8a78d0'), leaf=C('#3f7a34'), leaf2=C('#5c9040'), smoke=C('#f2ead8'),
        gate=C('#3d6a72'), yew=C('#2f5a30'), sheep=C('#f0e8d4'), sheep_f=C('#3a2c28'), cloth=C('#e8dcc0'), cloth2=C('#a8504a'), cloth3=C('#5a78a8'), dress=C('#b05a4a'), copper=C('#c47a3c', 1.0),
        candle=C('#f4e8c4'), flame=mat_emit('DY_flame_%s' % STATE['light'], '#ffcf7a', strength=12.0), ember=mat_emit('DY_ember_%s' % STATE['light'], '#ff8a3a', strength=5.0), blackiron=C('#34303a'), glass_d=C('#6f90b4', 1.0))

def sky_dome(SET, lkey, az0):
    sk = SKY[LIGHTS[lkey]['sky']]; path = X.get_sky(LIGHTS[lkey]['sky'], az0=az0, **sk); m = mat_emit('DY_sky_%s_%d' % (lkey, int(az0 * 100)), image=path, strength=1.0)
    mb = MB(); seg, rings, Rr = 64, 20, 1800.0; mb.pid += 1
    def pt(i, k):
        az = 2 * math.pi * i / seg; el = (math.pi / 2) * k / rings
        return (Rr * math.cos(el) * math.cos(az), Rr * math.cos(el) * math.sin(az), Rr * math.sin(el) - 40)
    for k in range(rings):
        for i in range(seg):
            a0, a1 = i / seg, (i + 1) / seg
            mb.face([pt(i, k), pt(i + 1, k), pt(i + 1, k + 1), pt(i, k + 1)], m, [(a0, k / rings), (a1, k / rings), (a1, (k + 1) / rings), (a0, (k + 1) / rings)])
    ob = mb.obj('sky', SET); ob.visible_shadow = False; STATE['sky_obj'] = ob; return ob

def hill_grid(SET, M, x0, x1, y0, y1, nx, ny, hf, name='hills', uvs=(1.5, 1.5)):
    mb = MB(); mb.pid += 1; pts = [[(x0 + (x1 - x0) * i / nx, y0 + (y1 - y0) * j / ny) for i in range(nx + 1)] for j in range(ny + 1)]; Z = [[hf(*p) for p in row] for row in pts]
    for j in range(ny):
        for i in range(nx):
            q = [(i, j), (i + 1, j), (i + 1, j + 1), (i, j + 1)]
            mb.oface([(pts[b][a][0], pts[b][a][1], Z[b][a]) for a, b in q], M['hills'], [(a / nx * uvs[0], b / ny * uvs[1]) for a, b in q], (0, 0, 1))
    return mb.obj(name, SET)

def make_camera(setup, name='cam', scene=None):
    ob = T.make_camera(setup, name, scene); ob.data.clip_end = 4000.0; ob.data.dof.use_dof = False; return ob

# ============================================================================= prototypes (per scene)
class Protos:
    def __init__(s, M): s.M = M; s.c = {}
    def get(s, key, fn):
        if key not in s.c: s.c[key] = fn()
        return s.c[key]
    def pail(s, milk=False): return s.get(('pail', milk), lambda: pail_local(s.M, milk=milk))
    def stool(s): return s.get('stool', lambda: stool_local(s.M))
    def barrel(s): return s.get('barrel', lambda: barrel_local(s.M))
    def churn(s): return s.get('churn', lambda: churn_local(s.M))
    def basket(s, eggs=False): return s.get(('basket', eggs), lambda: basket_local(s.M, eggs=eggs))
    def crate(s): return s.get('crate', lambda: crate_local(s.M))
    def sack(s, k): return s.get(('sack', k), lambda: sack_local(s.M, 0.8, s.M['sack'] if k % 2 else s.M['sack2'], 200 + k))
    def tool(s, kind): return s.get(('tool', kind), lambda: fork_local(s.M, kind))
    def cat(s, sit, k=0): return s.get(('cat', sit, k), lambda: cat_local(s.M, sit, s.M[('cat1', 'cat2', 'catw')[k % 3]]))
    def dog(s): return s.get('dog', lambda: dog_local(s.M))
    def goose(s): return s.get('goose', lambda: goose_local(s.M))
    def hen(s, v): return s.get(('hen', v), lambda: hen_local(s.M, v))
    def flower(s, kind, seed=0): return s.get(('fl', kind, seed), lambda: flower_local(kind, s.M, R(hash(kind) % 1000 + seed)))

def mote_groups(SET, M, rg, boxes, n=60, groups=4, name='motes', rad=(0.03, 0.06), amp=0.7):
    """Dust motes: `groups` objects, each a cloud of tiny emissive specks inside the given light boxes (x0, x1, y0, y1, z0, z1); drift by drivers."""
    for g in range(groups):
        mb = MB()
        for i in range(n):
            x0, x1, y0, y1, z0, z1 = boxes[rg.randrange(len(boxes))]; mb.sphere((rg.uniform(x0, x1), rg.uniform(y0, y1), rg.uniform(z0, z1)), rg.uniform(*rad), M['mote'], seg=4, rings=3)
        o = mk_obj(mb, '%s_%d' % (name, g), SET, (0, 0, 0), shadow=False)
        drv(o, 'location', 0, '%.2f*sin(frame*0.021+%.2f)' % (amp, g * 1.7)); drv(o, 'location', 1, '%.2f*cos(frame*0.017+%.2f)' % (amp, g * 2.3)); drv(o, 'location', 2, '%.2f*sin(frame*0.013+%.2f)-%.2f*fmod(frame*0.004+%.2f,1.0)+%.2f' % (amp * 0.6, g * 0.9, amp * 0.8, g * 0.25, amp * 0.4)); hook('motes', o)

def finish_layers(mb_flat, SET, name):
    ob = mb_flat.obj(name, SET); return ob

# ============================================================================= BARN
BX0, BX1, BY1 = -10.0, 10.0, 34.0
DOOR = (10.0, 21.0, 5.8)                                        # y0, y1, lintel z on the left wall x = -10

def barn(SET, M, P, kd, lkey, PR):
    rg = R(5); mb = MB(); gm = MB(); fw = MB(); cmb = MB(); hm = MB(); kdv = Vector(kd).normalized()
    # ---------------- ground, floor, yard apron
    mb.quad((-600, -300, -0.05), (1200, 0, 0), (0, 900, 0), M['grass'], (-600 / 9, -300 / 9, 600 / 9, 600 / 9))
    mb.quad((BX0, -1, 0.0), (20, 0, 0), (0, BY1 + 1, 0), M['earth'], (0, 0, 3.3, 5.8))
    mb.quad((-60, 6, 0.01), (50.2, 0, 0), (0, 22, 0), M['lane'], (0, 0, 4.2, 2.4)); mb.quad((-13.6, 9.2, 0.03), (3.6, 0, 0), (0, 13.6, 0), M['flag'], (0, 0, 2.4, 6.4))
    mb.quad((BX0 + 0.1, 9.4, 0.025), (5.4, 0, 0), (0, 13.2, 0), M['flag'], (0, 0, 3.6, 6.4))
    # ---------------- walls: planks with gaps (left has the open door), back and front gables (front: shadow only)
    pw, gap = 0.92, 0.16; y = -0.5; PT = (7.36, 7.0)
    while y < BY1 + 0.5:
        if DOOR[0] - 0.05 < y < DOOR[1] - 0.05: bx(mb, (BX0 - 0.6, y, DOOR[2] + 0.55), (BX0, y + pw, 5.85), M['oak'], PT)
        else: bx(mb, (BX0 - 0.6, y, 0.0), (BX0, y + pw, 5.85), M['oak'], PT)
        bx(mb, (BX1, y, 0.0), (BX1 + 0.6, y + pw, 5.85), M['oak_d'], PT); y += pw + gap
    for yy, mt, th in ((BY1, M['oak_d'], 0.6), (-0.7, M['oak'], 0.6)):
        x = BX0 - 0.6
        while x < BX1 + 0.6:
            xc = x + pw / 2; top = 5.8 + 3.8 * (1 - min(1, abs(xc) / 11.0)) - 0.3; bx(mb if yy > 0 else fw, (x, yy, 0.0), (x + pw, yy + th, max(top, 5.85)), mt, PT); x += pw + 0.1
    bx(mb, (BX0 - 0.7, DOOR[0] - 0.05, DOOR[2]), (BX0 + 0.1, DOOR[1] + 0.05, DOOR[2] + 0.55), M['oak'], (3, 3))
    for yy in (DOOR[0] - 0.45, DOOR[1] + 0.45): post(mb, BX0 + 0.1, yy, 0, DOOR[2], 0.8, M['oak'])
    obox(mb, (BX0 - 1.7, DOOR[0] - 2.1, 2.9), (0.95, 0.3, 0), (-0.3, 0.95, 0), (0, 0, 1), 1.9, 0.16, 2.9, M['oak_d'], 0.4)             # the door leaf swung back
    for sx in (-1, 1): rod(mb, (BX0 - 1.7 + sx * 0.2, DOOR[0] - 2.0, 4.9), (BX0 - 1.7 + sx * 0.2, DOOR[0] - 2.0, 1.0), 0.04, M['iron'], seg=3)
    # ---------------- posts in the walls and the wall plate (vertical / receding lines only: NO tie beams across the frame)
    for yy in np.arange(0.3, BY1, 3.8):
        for xx in (-9.55, 9.55):
            if xx < 0 and DOOR[0] - 0.6 < yy < DOOR[1] + 0.6: continue
            post(mb, xx, yy, 0, 5.8, 0.55, M['oak'])
    for sg in (-1, 1):
        bx(mb, (sg * 9.7 - 0.3, -0.5, 5.6), (sg * 9.7 + 0.3, BY1 + 0.5, 6.1), M['oak'], (3, 3))
    bx(mb, (-0.25, -0.5, 9.5), (0.25, BY1 + 0.5, 10.0), M['oak'], (3, 3))                                                           # ridge beam, receding
    for sg in (-1, 1):
        for t in (0.33, 0.66): xx = sg * 10.2 * (1 - t); zz = 5.0 + (9.5 - 5.0) * t; bx(mb, (xx - 0.14, -0.5, zz - 0.17), (xx + 0.14, BY1 + 0.5, zz + 0.17), M['oak'], (3, 3))   # purlins, receding
    for sg in (-1, 1):                                                                       # roof: boarding below (+ rafters, thin), slates above (blocks the key)
        a = Vector((sg * 11.8, 0, 4.7)); b = Vector((0, 0, 9.9)); dv = (b - a); L = dv.length; dv.normalize(); n = Vector((0, 1, 0)).cross(dv).normalized(); n = n if n.z > 0 else -n
        for off, hz, mt in ((0.45, 0.45, M['oak_d']), (1.15, 0.28, M['slate'])): obox(mb, (a + b) / 2 + n * off + Vector((0, BY1 / 2, 0)), dv, (0, 1, 0), n, L / 2 + 0.5, BY1 / 2 + 1.5, hz, mt, 0.2)
        for yy in np.arange(1.0, BY1, 2.1): obox(mb, (a + b) / 2 + n * -0.02 + Vector((0, yy, 0)), dv, (0, 1, 0), n, L / 2, 0.06, 0.09, M['oak'], 0.5)
    # hanging things from the roof (receding, small): onion strings, herb bundles, rope coils, swallow nests
    for (x_, y_, z_) in ((-3.2, 6.0, 7.9), (3.4, 9.0, 7.6), (-4.5, 14.0, 7.0), (2.5, 21.0, 7.4), (-2.0, 3.0, 8.2)):
        rod(mb, (x_, y_, z_ + 1.0), (x_, y_, z_), 0.015, M['twine'], seg=3)
        for k in range(7): mb.sphere((x_ + 0.08 * math.sin(k * 2), y_, z_ - 0.05 - k * 0.2), 0.12, M['straw2'] if k % 2 else M['orange'], seg=5, rings=3)
    for (x_, y_, z_) in ((1.5, 7.0, 8.4), (-1.2, 12.0, 8.7), (3.0, 3.8, 8.0)):
        rod(mb, (x_, y_, 9.4), (x_, y_, z_ + 0.7), 0.012, M['twine'], seg=3); rod(mb, (x_, y_, z_ + 0.7), (x_, y_, z_), 0.15, M['straw2'], seg=6, r1=0.05); rod(mb, (x_, y_, z_ + 0.7), (x_ - 0.3, y_, z_ - 0.4), 0.05, M['leaf'], seg=3, r1=0.01)
        rod(mb, (x_, y_, z_ + 0.7), (x_ + 0.3, y_, z_ - 0.4), 0.05, M['leaf'], seg=3, r1=0.01)
    for (x_, y_, z_) in ((-9.0, 4.5, 5.2), (9.0, 6.5, 5.4), (-9.0, 31.0, 5.2)):               # swallow nests (mud cups) under the wall plate
        ell(mb, (x_, y_, z_), (0.28, 0.22, 0.22), M['wood2'], seg=6, rings=4)
    # ---------------- hay loft (back) with a ladder, front rail posts, hay in strands
    LY = 22.0
    bx(mb, (BX0, LY, 4.4), (BX1, BY1, 4.8), M['oak'], (4, 4)); bx(mb, (BX0, LY - 0.2, 4.0), (BX1, LY + 0.2, 4.6), M['oak'], (3, 3))
    for xx in (-9.55, -4.8, 0, 4.8, 9.55): post(mb, xx, LY, 0, 4.6, 0.55, M['oak'])
    for xx in np.arange(-9.0, 9.1, 2.0): bx(mb, (xx - 0.15, LY, 3.9), (xx + 0.15, BY1, 4.4), M['oak'], (3, 3))
    for xx in np.arange(-9.5, 9.6, 1.6): rod(mb, (xx, LY + 0.1, 4.8), (xx, LY + 0.1, 5.9), 0.06, M['oak'], seg=4)
    bx(mb, (BX0, LY, 5.9), (BX1, LY + 0.14, 6.1), M['oak'], (3, 3))
    for i, (cx_, cy_) in enumerate(((-6, 25), (-1, 26), (5, 25), (-8, 30), (2, 31), (8, 30), (-4, 32), (6, 28), (-2, 23.2), (3.5, 23.6))): hay_heap(hm, (cx_, cy_, 4.8), M, 2.2, 40 + i * 5, 6)
    hay_heap(hm, (-3.0, LY + 0.5, 4.8), M, 1.5, 99, 4); hay_heap(hm, (4.4, LY + 0.5, 4.8), M, 1.2, 98, 4)
    for i in range(30):                                                                                    # hay hanging over the loft edge
        x_ = rg.uniform(-9, 9); strand_tuft(hm, (x_, LY + 0.1, 4.85), M['straw'], n=5, h=rg.uniform(0.6, 1.4), spread=0.4, lean=0.2, w=0.04, rg=rg, flat=-0.6)
    lx = -7.0
    for sg in (-0.45, 0.45): rod(mb, (lx + sg, LY - 3.0, 0.0), (lx + sg, LY - 0.15, 5.3), 0.09, M['wood2'], seg=5)
    for k in range(1, 10): zz = k * 0.55; yy = LY - 3.0 + (LY - 0.15 - (LY - 3.0)) * zz / 5.3; rod(mb, (lx - 0.45, yy, zz), (lx + 0.45, yy, zz), 0.06, M['wood2'], seg=4)
    # ---------------- stalls along the right wall: partitions, mangers, hay racks, cows
    for yy in (7.6, 12.6, 17.6, 22.6):
        bx(mb, (2.8, yy - 0.09, 0.0), (9.9, yy + 0.09, 3.6), M['oak'], (3, 3)); bx(mb, (2.7, yy - 0.18, 3.45), (9.9, yy + 0.18, 3.75), M['oak_d'], (3, 3)); post(mb, 2.7, yy, 0, 4.2, 0.45, M['oak'])
    for y0, y1 in ((7.6, 12.6), (12.6, 17.6), (17.6, 22.6)):
        bx(mb, (8.9, y0 + 0.2, 0.9), (9.95, y1 - 0.2, 1.7), M['oak_d'], (3, 3)); hay_heap(hm, (9.4, (y0 + y1) / 2, 1.5), M, 0.55, int(y0 * 7), 4)
        for yy in np.arange(y0 + 0.6, y1 - 0.5, 0.55): rod(mb, (9.7, yy, 3.0), (9.4, yy, 4.7), 0.045, M['wood2'], seg=4)
        hay_heap(hm, (4.0, y0 + 1.4, 0.0), M, 0.8, int(y0 * 5), 3); hay_heap(hm, (7.4, y1 - 1.0, 0.0), M, 0.6, int(y1 * 3), 3)
    for yy in (7.6, 12.6, 17.6): bx(mb, (2.7, yy - 0.1, 0.0), (2.85, yy + 5.1, 0.6), M['oak_d'], (3, 3)) if False else None
    cow(SET, cmb, M, (5.3, 10.1, 0.0), 0.0, 'b', 0.35, 0.0, 'cowS1'); cow(SET, cmb, M, (5.4, 15.1, 0.0), 0.0, 'a', 0.0, 1.7, 'cowS2'); cow(SET, cmb, M, (5.2, 20.1, 0.0), 0.0, 'a', 0.5, 3.1, 'cowS3')
    cow(SET, cmb, M, (-5.8, 28.4, 0.0), 1.2, 'b', 0.25, 4.4, 'cowBack', scale=0.62)                               # a calf tethered at the back left
    rod(mb, (-7.3, 27.6, 0.0), (-7.3, 27.6, 2.2), 0.1, M['wood2'], seg=5); rod(mb, (-7.3, 27.6, 1.7), (-6.6, 28.0, 1.4), 0.03, M['twine'], seg=3)
    # ---------------- the milking nook (Blossom is a 2D puppet at the stand point): stool, pail, straw bedding
    P_ = Protos(M); STATE['protos'] = P_
    stamp(mb, P_.stool(), (-4.0, 12.8, 0.0), 0.3); stamp(mb, P_.pail(True), (-2.0, 13.7, 0.0)); stamp(mb, P_.pail(), (-5.4, 11.2, 0.0), 0.4)
    straw_floor(hm, M, rg, [(rg.uniform(-8.6, -0.8), rg.uniform(10.2, 20.5), 0.02) for _ in range(150)], 5, 0.4)
    for (x_, y_) in ((-7.4, 15.5), (-6.8, 17.0), (-2.0, 19.0), (-0.8, 13.6)): hay_heap(hm, (x_, y_, 0.0), M, 0.7, int(x_ * 10 + y_), 3)
    # ---------------- bale stacks, sacks
    for (bxx, byy, bz, yw) in ((6.6, 3.0, 0.7, 0.1), (8.1, 4.1, 0.7, -0.2), (7.2, 3.4, 2.1, 0.15), (4.6, 5.6, 0.7, 0.5), (8.3, 6.4, 0.7, 0.0)): bale(hm, (bxx, byy, bz), M, yw, rg)
    for (bxx, byy, bz, yw) in ((8.4, 25.0, 0.7, 0.0), (8.0, 27.6, 0.7, 0.1), (8.4, 26.2, 2.1, 0.0), (-8.2, 24.0, 0.7, 1.5), (-8.0, 26.5, 0.7, 1.6), (-8.2, 25.2, 2.1, 1.55), (-8.4, 28.5, 0.7, 1.6)): bale(hm, (bxx, byy, bz), M, yw, rg)
    for i, (sx_, sy_) in enumerate(((8.2, 22.9), (9.0, 21.3), (-9.0, 31.0), (-8.0, 32.4), (7.6, 32.5), (-8.8, 5.2), (-8.0, 6.2), (3.4, 2.4))): stamp(mb, P_.sack(i), (sx_, sy_, 0), i * 1.1)
    # ---------------- the whole lower third: small things near the camera (y 1.5..6), bigger ones from y 6 on
    for (x_, y_, sc_, yw) in ((-3.6, 7.0, 0.8, 0.2), (1.6, 6.6, 0.8, 1.0), (-6.4, 6.0, 0.8, 2.0), (3.2, 4.4, 0.7, 0.6), (-1.0, 3.6, 0.65, 2.6)): stamp(mb, P_.stool(), (x_, y_, 0), yw, sc_)
    for (x_, y_, mlk) in ((-3.2, 4.4, False), (-2.0, 2.6, True), (1.2, 4.9, False), (3.0, 2.8, True), (-5.0, 3.4, False), (-7.0, 4.4, True), (0.3, 1.6, False), (5.0, 5.0, False), (-0.6, 5.8, True)): stamp(mb, P_.pail(mlk), (x_, y_, 0), rg.uniform(0, 6), 0.55)
    for (x_, y_) in ((-8.4, 3.6), (-7.2, 4.6), (-8.8, 6.2)): stamp(mb, P_.churn(), (x_, y_, 0), 0.0, 0.85)
    for (x_, y_, h_) in ((-9.0, 9.4, 1.3), (-9.2, 7.6, 1.1), (6.8, 7.0, 1.0)): stamp(mb, P_.barrel(), (x_, y_, 0), 0.0, h_ / 1.3)
    for (x_, y_, yw) in ((-1.6, 3.6, 0.3), (-4.4, 2.2, 1.0), (1.6, 2.6, 0.1), (4.4, 3.8, 0.7)): stamp(mb, P_.basket(True), (x_, y_, 0), yw, 0.8)
    stamp(mb, P_.crate(), (-6.0, 7.6, 0), 0.4); stamp(mb, P_.crate(), (-6.1, 7.5, 0.6), 0.9, 0.8); stamp(mb, P_.crate(), (6.0, 2.7, 0), 0.2, 0.8)
    wheelbarrow(mb, (1.8, 9.2, 0), M, 0.15); hay_heap(hm, (1.8, 9.2, 1.3), M, 0.8, 321, 3)
    wheel(mb, (-9.3, 9.0, 2.0), 2.0, M, (1, 0, 0))
    for (px, py, lean, kind) in ((9.5, 2.6, -0.35, 'fork'), (-9.4, 16.0, 0.0, 'rake'), (9.5, 4.2, -0.3, 'rake'), (-9.2, 6.2, 0.1, 'shovel'), (-9.0, 8.4, 0.1, 'broom')):
        stamp(mb, P_.tool(kind), (px, py, 0), math.pi * (px < 0), pitch=-lean * 0.45 if px > 0 else lean * 0.45 + 0.1)
    stamp(mb, P_.tool('rake'), (-1.0, 3.0, 0.08), 0.6, pitch=1.52); stamp(mb, P_.tool('fork'), (2.6, 3.4, 0.08), 2.2, pitch=1.5); stamp(mb, P_.tool('shovel'), (-4.2, 5.4, 0.08), 1.2, pitch=1.52)
    for (x_, y_) in ((-1.0, 3.8), (2.0, 5.8), (-4.6, 1.8), (4.4, 6.6), (-2.4, 6.4), (0.4, 7.6), (-5.6, 5.0), (3.4, 1.8)): hay_heap(hm, (x_, y_, 0), M, 0.45, int(x_ * 17 + y_ * 3), 3)
    straw_floor(hm, M, rg, [(rg.uniform(-9.4, 9.4), rg.uniform(0.6, 10.0), 0.02) for _ in range(2600)], 5, 0.16)
    for (fx, fy) in [(rg.uniform(-9.6, 9.6), rg.uniform(1.0, 33.0)) for _ in range(700)]:
        a = rg.uniform(0, 6.28); l = rg.uniform(0.3, 0.8); rod(mb, (fx, fy, 0.03), (fx + math.cos(a) * l, fy + math.sin(a) * l, 0.05 + rg.random() * 0.05), 0.011, M['straw'], seg=3)
    for i in range(70):                                                                                     # a few stones and cobbles pushed up through the earth
        lumpy(mb, (rg.uniform(-9.5, 9.5), rg.uniform(0.5, 30), 0.0), rg.uniform(0.12, 0.28), M['moss'], i, seg=6, rings=4, rough=0.2, squash=0.6)
    for (x_, y_, yw, v) in ((-4.6, 8.8, 0.6, 0), (-3.6, 10.0, 2.4, 1), (0.2, 11.6, -0.8, 2), (-1.8, 12.4, 1.4, 0), (3.2, 8.4, 2.0, 1), (-6.2, 5.0, 0.2, 2), (-0.8, 4.4, 3.0, 0), (2.0, 2.6, 5.0, 1), (-2.4, 2.8, 1.0, 0), (6.0, 9.2, 4.0, 2), (-8.0, 9.8, 0.8, 1), (1.4, 10.4, 2.8, 0)):
        hen(SET, M, (x_, y_, 0), yw, v, True, rg.uniform(0, 6.28), 'hen%d' % len(STATE['hooks']), proto=P_.hen(v))
    for (x_, y_, z_, yw, sit, k) in ((6.6, 3.2, 2.8, -2.0, True, 0), (-1.2, 7.6, 0.0, 0.7, False, 1), (-8.4, 26.5, 2.8, 0.0, True, 2), (2.8, 9.4, 0.0, 2.8, True, 0)): stamp(mb, P_.cat(sit, k), (x_, y_, z_), yw)
    stamp(mb, P_.dog(), (-0.2, 7.2, 0.0), 2.2, 0.9)
    c = Vector((-1.6, 9.2, 0)); rod(mb, c, c + Vector((0, 0, 0.5)), 0.7, M['straw'], seg=10, r1=0.9)
    for dx in (-0.25, 0.25): ell(mb, c + Vector((dx, 0, 0.5)), (0.17, 0.12, 0.14), M['white'], seg=6, rings=4)
    for k in range(40): strand_tuft(hm, c + Vector((rg.uniform(-0.8, 0.8), rg.uniform(-0.8, 0.8), 0.3)), M['straw'], n=3, h=0.45, spread=1.0, lean=0.8, w=0.03, rg=rg)
    # ---------------- harness on pegs (back wall), bridles on the stall wall, horse collars
    bx(mb, (-9.0, BY1 - 0.4, 3.6), (9.0, BY1, 3.9), M['oak'], (3, 3))
    for k, xx in enumerate(np.arange(-8.0, 8.1, 2.0)): rod(mb, (xx, BY1 - 0.4, 3.75), (xx, BY1 - 1.3, 3.75), 0.07, M['iron'], seg=4)
    for k, xx in enumerate((-7.0, -3.0, 1.0, 5.0)):
        c = Vector((xx, BY1 - 1.0, 2.6)); n = 14
        for i in range(n):
            t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n; rod(mb, c + Vector((math.cos(t0) * 0.7, 0, math.sin(t0) * 0.9)), c + Vector((math.cos(t1) * 0.7, 0, math.sin(t1) * 0.9)), 0.2, M['leather'], seg=5)
        for i in range(0, n, 3): t0 = 2 * math.pi * i / n; mb.sphere(c + Vector((math.cos(t0) * 0.78, -0.1, math.sin(t0) * 1.0)), 0.13, M['brass'], seg=5, rings=3)
    for xx in (-8.0, -6.0, -2.0, 2.0, 6.0, 8.0): rod(mb, (xx, BY1 - 1.2, 3.75), (xx + 0.15, BY1 - 1.2, 1.7), 0.07, M['leather'], seg=4); mb.sphere((xx + 0.15, BY1 - 1.2, 1.6), 0.14, M['brass'], seg=5, rings=3)
    bx(mb, (9.6, 21.0, 3.5), (9.9, 30.0, 3.7), M['oak'], (3, 3))
    for yy in (21.8, 23.5, 25.2, 27.0, 28.6): rod(mb, (9.6, yy, 3.6), (8.8, yy, 3.6), 0.07, M['iron'], seg=4); rod(mb, (8.9, yy, 3.6), (8.9, yy, 1.6 + rg.random()), 0.07, M['leather'], seg=4)
    # ---------------- lanterns on long chains from the ridge: they swing (hooks)
    for (x_, y_, z_, nm, ph) in ((-0.6, 9.5, 5.8, 'lamp1', 0.0), (3.6, 17.0, 5.4, 'lamp2', 1.9), (0.6, 27.0, 4.6, 'lamp3', 3.3)):
        rod(mb, (x_, y_, 9.5), (x_, y_, z_), 0.022, M['iron'], seg=4); swing_lantern(SET, M, (x_, y_, z_), nm, ph, 1500, 0.09)
    # ---------------- sun shafts (additive wedges along the key) + dust motes
    ke = Vector(kdv); sf = M['shaft']; p0 = Vector((BX0, DOOR[0], 0.3)); t_ = (DOOR[2]) / -ke.z
    def par(p, ex, ey, ez):
        p, ex, ey, ez = map(Vector, (p, ex, ey, ez))
        for a, b, o in ((ex, ey, Vector()), (ex, ey, ez), (ex, ez, Vector()), (ex, ez, ey), (ey, ez, Vector()), (ey, ez, ex)): gm.pid += 1; gm.face([p + o, p + o + a, p + o + a + b, p + o + b], sf)
    par(p0, Vector((0, DOOR[1] - DOOR[0], 0)), Vector((0, 0, DOOR[2] - 0.3)), ke * (t_ * 0.9))
    for yy in (21.4, 23.3, 25.2, 27.1, 29.0, 30.9): tt = 5.4 / -ke.z; par(Vector((BX0, yy, 0.2)), Vector((0, 0.16, 0)), Vector((0, 0, 5.3)), ke * (tt * 0.95))
    boxes = []
    for i in range(6):
        y0 = rg.uniform(DOOR[0], DOOR[1] - 2); z0 = rg.uniform(0.8, DOOR[2] - 1.0); t = rg.uniform(0.5, (z0 - 0.3) / -ke.z * 0.9); pm = Vector((BX0, y0, z0)) + ke * t
        if pm.x < BX1 - 0.3 and pm.z > 0.3: boxes.append((pm.x - 1.6, pm.x + 1.6, pm.y - 1.2, pm.y + 1.2, max(0.4, pm.z - 1.0), pm.z + 1.0))
    boxes = boxes or [(-8, -2, 11, 19, 0.6, 4)]
    mote_groups(SET, M, rg, boxes, 70, 4)
    STATE['fw'] = fw
    ob = mb.obj('barn', SET); ob2 = gm.obj('barn_glow', SET); ob2.visible_shadow = False; fo = fw.obj('frontwall', SET); fo.visible_camera = False
    hob = hm.obj('barn_hay', SET); cob = cmb.obj('barn_cows', SET, smooth=True)
    return mb

def yard_out(SET, M, P, kd):
    """Outside the open door (x < -10): the lane, farmyard stone wall, hay wagon, geese, hens, trees, the field."""
    rg = R(8); mb = MB(); hm = MB(); P_ = STATE['protos']; lv = [M['green'], M['leaf2'], M['leaf']]
    drystone(mb, (-36.0, -8.0), (-36.0, 72.0), 2.4, 1.0, [M['stone'], M['moss'], M['stone2']], rg)
    for yy in np.arange(-6, 70, 4.5): bx(mb, (-37.2, yy, 0), (-36.9, yy + 0.3, 2.9), M['oak'], (1, 1)) if False else None
    for (tx_, ty_, h, r) in ((-44, 8, 9, 5), (-50, 26, 11, 6), (-46, 44, 10, 5.5), (-60, 15, 12, 6.5), (-62, 38, 12, 6.5), (-40, 60, 9, 5), (-52, -4, 10, 5.5), (-34, 28, 6, 3.4)): tree(mb, (tx_, ty_, 0), h, r, M['wood2'], lv, int(ty_ * 3), nclump=18)
    obox(mb, (-24, 24, 1.6), (1, 0, 0), (0, 1, 0), (0, 0, 1), 3.0, 1.5, 0.5, M['oak'], 0.4); wheel(mb, (-24.0, 22.4, 2.0), 1.9, M, (0, 1, 0)); wheel(mb, (-24.0, 25.6, 2.0), 1.9, M, (0, 1, 0))
    for sg in (-1, 1): bx(mb, (-27.0, 24 + sg * 1.4, 2.0), (-21.0, 24 + sg * 1.4 + 0.12, 3.8), M['oak_d'], (2, 2)) if False else None
    hay_heap(hm, (-24, 24, 2.1), M, 2.0, 600, 6); rod(mb, (-29.0, 24, 1.6), (-34.0, 24, 1.0), 0.1, M['wood2'], seg=5)
    hay_heap(hm, (-18, 36, 0.0), M, 3.0, 650, 6); hay_heap(hm, (-16, 6.5, 0.0), M, 1.6, 651, 5)
    for (x_, y_, yw) in ((-14.0, 9.0, 0.4), (-16.5, 10.5, 2.0), (-12.5, 22.5, 3.0), (-20.0, 14.0, 5.2)): stamp(mb, P_.goose(), (x_, y_, 0.03), yw)
    for (x_, y_, yw, v) in ((-13.0, 12.0, 0.4, 0), (-15.0, 19.0, 2.0, 1), (-18.0, 8.0, 3.0, 2), (-13.5, 24.5, 1.0, 0)): hen(SET, M, (x_, y_, 0.0), yw, v, True, rg.uniform(0, 6), 'yhen%d' % len(STATE['hooks']), proto=P_.hen(v))
    stamp(mb, P_.barrel(), (-12.5, 9.2, 0), 0.0); stamp(mb, P_.barrel(), (-12.6, 21.8, 0), 0.0, 0.9); stamp(mb, P_.churn(), (-11.9, 21.9, 0), 0.0)
    tr = MB(); bx(tr, (-1.5, -0.6, 0), (1.5, 0.6, 0.8), M['stone2'], (2, 2)); bx(tr, (-1.3, -0.4, 0.55), (1.3, 0.4, 0.85), M['milk'], (1, 1)); stamp(mb, tr, (-20.0, 6.0, 0), 0.2)         # stone trough
    flw = [P_.flower(k) for k in ('daisy', 'buttercup', 'cowparsley', 'poppy', 'viola')]
    scatter_flowers(mb, rg, flw, (-35.5, -14, -8, 70), 420, hmin=0.6, hmax=1.0, keep=lambda x, y: not (-14 > x > -16 and 8 < y < 23))
    scatter_grass(mb, rg, [M['leaf2'], M['leaf'], M['grass_d']], (-35.5, -10.5, -8, 70), 1300, keep=lambda x, y: not (7 < y < 22 and x > -34))
    mb.obj('yard', SET); hm.obj('yard_hay', SET)
    def hf(x, y): d = max(0.0, -x - 50.0); r_ = sm(0, 300, d); return -0.1 + 30 * r_ ** 1.3 * (0.55 + 0.45 * math.sin(y * 0.008 + 1.3)) + 8 * r_ * math.sin(y * 0.03 + x * 0.01)
    hill_grid(SET, M, -760, -40, -300, 420, 48, 60, hf)

def village(*a): raise NotImplementedError
def room(*a): raise NotImplementedError
# ============================================================================= build / anchors / CLI
def build(preset=None, light=None, clear=True):
    """Build the preset's location with its light, sky, hooks and camera data into the current scene. Returns the anchors dict (API.md)."""
    preset = preset or 'barn_wide'; assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PRc = PRESETS[preset]; loc = PRc['loc']; lkey = light or PRc['light']; assert lkey in LOC_LIGHTS[loc]
    scene, SET, P, kd = new_scene(lkey, PRc['sun']); C, TX, E = STATE['C'], STATE['TX'], STATE['E']; M = mats(C, TX, E); STATE['M'] = M; STATE['preset'] = preset; STATE['loc'] = loc
    sky_dome(SET, lkey, (PRc.get('look_az', 90) % 360) / 360.0)
    if loc == 'barn': barn(SET, M, P, kd, lkey, PRc); yard_out(SET, M, P, kd)
    elif loc == 'village': village(SET, M, P, kd, lkey, PRc)
    else: room(SET, M, P, kd, lkey, PRc)
    finish(scene, SET, P)
    A = anchors(); STATE['A'] = A; return A

def anchors():
    P = STATE['P']; pr = STATE['preset']; PRc = PRESETS[pr]; cams = {k: dict(v) for k, v in CAMS.items() if PRESETS[k]['loc'] == PRc['loc']}
    return dict(location=PRc['loc'], preset=pr, light=STATE['light'], cams=cams, cam=dict(CAMS[PRc['cam']]), cam_name=PRc['cam'], cam_notes={k: CAM_NOTES[k] for k in cams},
                render=dict(samples_final=12, resolution=(720, 1280), threads=4, denoise='OIDN', dof=None), key_dir=tuple(Vector(P['key_dir']).normalized()), sun_elevation_deg=P['sun_elev'],
                heights=dict(ROLES), stand={k: {n: dict(v) for n, v in STAND[k].items()} for k in cams}, staging={k: list(STAGING[k]) for k in cams}, hooks=list(STATE.get('hooks', [])),
                lights=[o.name for o in STATE['LIGHTS'].objects], candle=STATE.get('candle'))

def stage_placeholders(A, preset=None, cam_loc=None, names=None):
    preset = preset or A['preset']; cam_loc = cam_loc or CAMS[PRESETS[preset]['cam']]['loc']; T._clear_actors(); out = []
    for nm in (names or STAGING[preset]):
        s = STAND[preset][nm]; role = s['role']
        if role == 'cow': continue
        pos = Vector(s['pos']); d = Vector(cam_loc) - pos; el = math.degrees(math.atan2(d.z - 1.5, math.hypot(d.x, d.y)))
        out.append(T.placeholder_actor(role, tuple(pos), face_to=cam_loc, tilt=max(0.0, el - 25) * 0.55, name='actor_%s_%s' % (preset, nm)))
    return out

def head_pixels(preset):
    """[(slot, role, pos, head_centre_y_px, head_px, chin_y_px, feet_y_px)] at 720x1280 (caption rule: chin < 880)."""
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy.context.scene; cam = sc.camera; out = []
    for nm in STAGING[preset]:
        s = STAND[preset][nm]
        if s['role'] == 'cow': continue
        h = s['height']; m = Vector(s['pos']); top, hc, bot = m + Vector((0, 0, h)), m + Vector((0, 0, h - 0.5)), m + Vector((0, 0, h - 1.0))
        p, q, b = (world_to_camera_view(sc, cam, v) for v in (hc, top, bot)); f = world_to_camera_view(sc, cam, m)
        out.append((nm, s['role'], tuple(round(v, 1) for v in s['pos']), round((1 - p.y) * 1280), round(abs(q.y - b.y) * 1280), round((1 - b.y) * 1280), round((1 - f.y) * 1280)))
    return out

def _load(): return ' '.join('%.2f' % v for v in os.getloadavg())

def cli_render(specs=None, quality='final', outdir=None, actors=True, samples=None):
    """specs: ['preset' | 'preset:LIGHT']"""
    outdir = outdir or os.path.join(WORK, 'final' if quality == 'final' else 'stills'); os.makedirs(outdir, exist_ok=True); res = {}
    for spec in (specs or list(PRESETS)):
        parts = spec.split(':'); pr = parts[0]; lt = parts[1] if len(parts) > 1 and parts[1] else None
        t0 = time.time(); A = build(pr, light=lt); tb = time.time() - t0; sc = bpy.context.scene; MN.setup_render(sc, quality); sc.render.threads_mode = 'FIXED'; sc.render.threads = 4
        if samples: sc.cycles.samples = samples
        cs = A['cam']; make_camera(cs)
        if actors: stage_placeholders(A, pr, cs['loc'])
        bpy.context.view_layer.update(); hp = head_pixels(pr); tag = pr + ('_' + A['light'] if lt else '')
        w, c = T.render(os.path.join(outdir, tag + '.png')); res[tag] = (round(w, 1), round(c, 1), round(tb, 1), hp)
        print('%s %s: build %.1f s, render %.1f s wall, %.1f s cpu, load %s, heads %s' % (quality, tag, tb, w, c, _load(), [(h[0], h[3], h[4]) for h in hp]), flush=True)
    return res

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'help'; arg = sys.argv[2:]
    if cmd in ('finals', 'stills'):
        r = cli_render(arg or None, 'final' if cmd == 'finals' else 'preview', actors=os.environ.get('ACTORS', '1') == '1')
        if cmd == 'finals': os.makedirs(WORK, exist_ok=True); json.dump({k: dict(wall=v[0], cpu=v[1], build=v[2]) for k, v in r.items()}, open(os.path.join(WORK, 'times_%s.json' % ('_'.join(arg) or 'all').replace(':', '-')), 'w'))
    elif cmd == 'digest':
        A = build(arg[0] if arg else None); bpy.context.view_layer.update(); print('objects', len(bpy.data.objects), 'tris', sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH'))
    else: print(__doc__)
