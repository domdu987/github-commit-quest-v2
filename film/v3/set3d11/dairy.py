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
    barn_wide=dict(loc='barn', light='A', cam='barn_wide', sun=(240, 24), look_az=100),
    barn_milking=dict(loc='barn', light='A', cam='barn_milking', sun=(215, 24), look_az=90),
    barn_high=dict(loc='barn', light='C', cam='barn_high', sun=(185, 11), look_az=70),
    barn_door=dict(loc='barn', light='A', cam='barn_door', sun=(240, 22), look_az=180),
    garden_hut=dict(loc='village', light='A', cam='garden_hut', sun=(300, 34), look_az=165),
    lane_wide=dict(loc='village', light='A', cam='lane_wide', sun=(300, 40), look_az=182),
    lane_high=dict(loc='village', light='A', cam='lane_high', sun=(300, 36), look_az=95),
    garden_queue=dict(loc='village', light='A', cam='garden_queue', sun=(300, 36), look_az=100),
    room_day=dict(loc='cottage', light='A', cam='room_day', sun=(163, 26), look_az=90, P=dict(shade=(0.176, 0.235, 0.58), lift=(0.03, 0.045, 0.08))),
    room_night=dict(loc='cottage', light='C', cam='room_night', sun=(166, 9), look_az=90, candle=True, P=dict(shade=(0.12, 0.175, 0.52), lift=(0.015, 0.025, 0.065))),
    room_morning=dict(loc='cottage', light='A', cam='room_morning', sun=(160, 19), look_az=90, P=dict(shade=(0.176, 0.235, 0.58), lift=(0.03, 0.045, 0.08))),
)
LOC_PRESETS = {l: [k for k, v in PRESETS.items() if v['loc'] == l] for l in ('barn', 'village', 'cottage')}
LOC_LIGHTS = dict(barn=['A', 'C'], village=['A', 'C'], cottage=['A', 'C'])

CAMS = dict(
    barn_wide=dict(loc=(1.0, -1.0, 2.8), look_at=(0.0, 15.0, -0.9), lens=22),
    barn_milking=dict(loc=(-1.6, 6.0, 1.5), look_at=(-3.2, 15.0, 2.0), lens=22),
    barn_high=dict(loc=(3.2, 4.0, 6.6), look_at=(-6.0, 14.0, 0.4), lens=22),
    barn_door=dict(loc=(1.2, 15.0, 1.2), look_at=(-12.0, 15.8, 3.0), lens=22),
    garden_hut=dict(loc=(3.5, -6.6, 1.5), look_at=(-10.0, 0.8, 2.6), lens=22),
    lane_wide=dict(loc=(41.0, -12.3, 1.7), look_at=(-40.0, -9.2, 4.6), lens=22),
    lane_high=dict(loc=(8.0, -34.0, 13.0), look_at=(-1.0, -11.0, 1.0), lens=22),
    garden_queue=dict(loc=(2.0, -15.0, 3.2), look_at=(-3.0, -2.5, 2.4), lens=22),
    room_day=dict(loc=(1.6, -2.6, 2.7), look_at=(-1.0, 5.0, 1.3), lens=22),
    room_night=dict(loc=(1.6, -2.6, 2.7), look_at=(-1.0, 5.0, 1.3), lens=22),
    room_morning=dict(loc=(1.6, -2.6, 2.7), look_at=(-1.0, 5.0, 1.3), lens=22),
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
    garden_hut=dict(boy=_mk('boy', (-8.0, -3.4, 0.8), seated=True, note='James SEATED on the stool at the hut door (z = stool top)'), jenner=_mk('jenner', (-6.2, -0.8, 0.0), note='Jenner with the lancet, beside the boy'),
                    sarah=_mk('sarah', (-3.0, 0.2, 0.0), note='milkmaid at the bed edge'), doctor=_mk('doctor', (-1.4, -5.2, 0.0), note='town doctor at the gate')),
    lane_wide=dict(doctor=_mk('doctor', (27.0, -11.6, 0.0), note='town doctor arriving, centre of the lane'), villager_a=_mk('villager', (23.0, -9.4, 0.0)), villager_b=_mk('villager_p', (31.5, -13.0, 0.0)),
                   villager_c=_mk('villager', (20.0, -12.8, 0.0)), maid=_mk('maid', (29.0, -9.2, 0.0)), jenner=_mk('jenner', (17.5, -10.6, 0.0)), boy=_mk('boy', (24.6, -13.6, 0.0))),
    lane_high=dict(**{'c%d' % i: _mk('villager' if i % 3 else 'villager_p', p, note='crowd slot %d' % i) for i, p in enumerate(
        [(-6.0, -16.0, 0.0), (-3.2, -13.2, 0.0), (-0.4, -16.4, 0.0), (2.4, -13.0, 0.0), (5.2, -16.0, 0.0), (8.0, -13.4, 0.0), (-4.6, -9.6, 0.0), (0.4, -10.4, 0.0), (5.0, -9.6, 0.0)])},
                   doctor=_mk('doctor', (0.8, -19.2, 0.0), note='the mocking doctor at the front of the crowd')),
    garden_queue=dict(**{'q%d' % i: _mk('villager' if i % 3 else 'villager_p', (4.6 - i * 1.9, -3.2, 0.0), note='queue slot %d (0 = near the gate)' % i) for i in range(7)},
                      jenner=_mk('jenner', (-9.0, -1.5, 0.0), note='Jenner at the hut door'), boy=_mk('boy', (-8.0, -3.4, 0.0), note='James first in the queue'), doctor=_mk('doctor', (8.2, -3.6, 0.0), note='the mocker, rolls up his sleeve at the tail')),
    room_day=dict(mother=_mk('mother', (-0.8, 3.0, 0.0), note='mother by the bed'), boy_bed=_mk('boy', (-5.2, 7.2, 1.7), pose='in bed', note='James lying in bed: z = mattress top, pillow at the window end'),
                  jenner=_mk('jenner', (1.6, 1.8, 0.0), note='Jenner at the bedside')),
    room_night=dict(mother=_mk('mother', (-1.4, 3.0, 0.0)), boy_bed=_mk('boy', (-5.2, 7.2, 1.7), pose='in bed', note='feverish in bed'), doctor=_mk('doctor', (6.4, 4.8, 0.0), note='town doctor in the doorway, pointing (door opening y 3.0..6.6, x 7.5)'),
                    jenner=_mk('jenner', (1.2, 2.2, 0.0), note='Jenner')),
    room_morning=dict(boy=_mk('boy', (-2.0, 3.2, 0.0), note='James jumps out of bed (floor)'), mother=_mk('mother', (1.6, 2.6, 0.0), note='mother'), boy_bed=_mk('boy', (-5.2, 7.2, 1.7), pose='in bed')),
)
STAGING = dict(barn_wide=['sarah', 'maid', 'jenner'], barn_milking=['sarah', 'maid'], barn_high=['sarah', 'maid', 'vill_a', 'vill_b', 'vill_c', 'vill_d'], barn_door=['sarah', 'jenner', 'vill_a'],
               garden_hut=['boy', 'jenner', 'sarah', 'doctor'], lane_wide=['doctor', 'villager_a', 'villager_b', 'villager_c', 'maid'], lane_high=['c%d' % i for i in range(9)] + ['doctor'],
               garden_queue=['q%d' % i for i in (0, 1, 2, 4, 6)] + ['jenner', 'boy'], room_day=['mother', 'boy_bed', 'jenner'], room_night=['mother', 'boy_bed', 'doctor'], room_morning=['boy', 'mother'])
T.PH.update(jenner=('boss', dict(yaw=0.3, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['jenner']), sarah=('beach_woman', dict(yaw=-0.25, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['sarah']),
            maid=('beach_woman', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['maid']), doctor=('boss', dict(yaw=0.35, head_roll=-4, expr='smug', arm_l='down', arm_r='hip', legs='stand'), ROLES['doctor']),
            mother=('beach_woman', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['mother']), villager=('senior_b', dict(yaw=0.2, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['villager']),
            villager_p=('senior_a', dict(yaw=0.4, expr='neutral', arm_l='down', arm_r='down', legs='stand'), ROLES['villager_p']), boy=('beach_kid', dict(yaw=-0.3, expr='determined', arm_r='down', arm_l='down', legs='stand'), BOY))

# ============================================================================= scene setup / materials
def new_scene(lkey, sun=None, over=None):
    scene = bpy.context.scene; P = dict(LIGHTS[lkey]); P.update(over or {})
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
        oak=TX('planks', 1.0), oak_d=TX('planks_dark', 0.95), silver=TX('planks_silver', 1.0), floorw=TX('wood_floor', 1.0), hay=TX('hay2', 0.95, 1.8, smix=0.3), hayc=C('#dcae4a', 0.95, 1.9, smix=0.22),
        hayc2=C('#cf9f3c', 0.95, 1.9, smix=0.22), earth=TX('earth', 1.0), lane=TX('lane2', 1.0), grass=TX('grass', 1.0), grass_d=TX('grass_d', 0.95), flag=TX('flag', 1.0), cobble=TX('cobble', 1.0),
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
        gate=C('#3d6a72'), pebble=C('#b4a486'), pebble2=C('#8e8068'), pond=C('#6f9fb8', 1.0), yew=C('#2f5a30'), sheep=C('#f0e8d4'), sheep_f=C('#3a2c28'), cloth=C('#e8dcc0'), cloth2=C('#a8504a'), cloth3=C('#5a78a8'), dress=C('#b05a4a'), copper=C('#c47a3c', 1.0),
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
    rg = R(5); mb = MB(); gm = MB(); fw = MB(); cmb = MB(); hm = MB(); kdv = Vector(kd).normalized(); cxy = CAMS[PR['cam']]['loc']; CLR = 3.6
    def okp(p): return math.hypot(p[0] - cxy[0], p[1] - cxy[1]) > CLR or abs(cxy[2] - 1.0) > 3.0 and math.hypot(p[0] - cxy[0], p[1] - cxy[1]) > 1.5
    def stamp(mb_, proto, pos=(0, 0, 0), *a, **k): return G.stamp(mb_, proto, pos, *a, **k) if okp(pos) else None          # keep the camera's own spot clear
    def hay_heap(mb_, c, *a, **k): return G.hay_heap(mb_, c, *a, **k) if okp(c) else None
    def wheelbarrow(mb_, c, *a, **k): return G.wheelbarrow(mb_, c, *a, **k) if okp(c) else None
    def bale(mb_, c, *a, **k): return G.bale(mb_, c, *a, **k) if okp(c) else None
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
            xc = x + pw / 2; top = 5.8 + 3.8 * (1 - min(1, abs(xc) / 11.0)) - 0.3; z0_ = 5.7 if (yy < 0 and -8.4 < xc < 8.4) else 0.0; bx(mb if yy > 0 else fw, (x, yy, z0_), (x + pw, yy + th, max(top, 5.85)), mt, PT); x += pw + 0.1
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
    for yy in (7.6, 12.6, 17.6, 22.6):                                                   # open stalls: low boards, two thin rails, posts at the ends (the cows stay visible)
        bx(mb, (1.8, yy - 0.08, 0.0), (9.9, yy + 0.08, 0.9), M['oak'], (3, 3)); post(mb, 1.8, yy, 0, 3.6, 0.4, M['oak']); post(mb, 9.8, yy, 0, 3.6, 0.4, M['oak'])
        for zr_ in (1.9, 2.9): bx(mb, (1.8, yy - 0.06, zr_), (9.9, yy + 0.06, zr_ + 0.14), M['oak_d'], (3, 3))
    for y0, y1 in ((7.6, 12.6), (12.6, 17.6), (17.6, 22.6)):
        bx(mb, (8.9, y0 + 0.2, 0.9), (9.95, y1 - 0.2, 1.7), M['oak_d'], (3, 3)); hay_heap(hm, (9.4, (y0 + y1) / 2, 1.5), M, 0.55, int(y0 * 7), 4)
        for yy in np.arange(y0 + 0.6, y1 - 0.5, 0.55): rod(mb, (9.7, yy, 3.0), (9.4, yy, 4.7), 0.045, M['wood2'], seg=4)
        hay_heap(hm, (4.0, y0 + 1.4, 0.0), M, 0.8, int(y0 * 5), 3); hay_heap(hm, (7.4, y1 - 1.0, 0.0), M, 0.6, int(y1 * 3), 3)
    for yy in (7.6, 12.6, 17.6): bx(mb, (2.7, yy - 0.1, 0.0), (2.85, yy + 5.1, 0.6), M['oak_d'], (3, 3)) if False else None
    cow(SET, cmb, M, (5.6, 10.1, 0.0), 0.0, 'b', 0.35, 0.0, 'cowS1'); cow(SET, cmb, M, (5.7, 15.1, 0.0), 0.0, 'a', 0.0, 1.7, 'cowS2'); cow(SET, cmb, M, (5.5, 20.1, 0.0), 0.0, 'a', 0.5, 3.1, 'cowS3')
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
        lumpy(mb, (rg.uniform(-9.5, 9.5), rg.uniform(0.5, 30), 0.0), rg.uniform(0.12, 0.28), M['pebble'] if i % 2 else M['pebble2'], i, seg=6, rings=4, rough=0.2, squash=0.6)
    for (x_, y_, yw, v) in ((-4.6, 8.8, 0.6, 0), (-3.6, 10.0, 2.4, 1), (0.2, 11.6, -0.8, 2), (-1.8, 12.4, 1.4, 0), (3.2, 8.4, 2.0, 1), (-6.2, 5.0, 0.2, 2), (-0.8, 4.4, 3.0, 0), (2.0, 2.6, 5.0, 1), (-2.4, 2.8, 1.0, 0), (6.0, 9.2, 4.0, 2), (-8.0, 9.8, 0.8, 1), (1.4, 10.4, 2.8, 0)):
        hen(SET, M, (x_, y_, 0), yw, v, True, rg.uniform(0, 6.28), 'hen%d' % len(STATE['hooks']), proto=P_.hen(v))
    for (x_, y_, z_, yw, sit, k) in ((6.6, 3.2, 2.8, -2.0, True, 0), (-1.2, 7.6, 0.0, 0.7, False, 1), (-8.4, 26.5, 2.8, 0.0, True, 2), (2.8, 9.4, 0.0, 2.8, True, 0)): stamp(mb, P_.cat(sit, k), (x_, y_, z_), yw)
    stamp(mb, P_.dog(), (-0.2, 7.2, 0.0), 2.2, 0.9)
    c = Vector((-1.6, 9.2, 0))
    if okp(c):
        rod(mb, c, c + Vector((0, 0, 0.5)), 0.7, M['straw'], seg=10, r1=0.9)
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

def room(*a): raise NotImplementedError
# ============================================================================= VILLAGE
def house(mb, M, x0, x1, y0, y1, ze, zr, face, seed, wall='stone', roof='thatch', chim=(0.3,), door_at=0.3, dormers=1, roses=True, shutters=False, win_z=2.7):
    """Cottage block: footprint [x0,x1] x [y0,y1], ridge along x, facade on y0 (face -1) or y1 (face +1). Returns the chimney tops [(x, y, z)]."""
    rg = R(seed); wm = dict(stone=M['stone'], plaster=M['plaster'], brick=M['brick'], moss=M['moss'])[wall]; yf = y0 if face < 0 else y1; L = x1 - x0
    bx(mb, (x0, y0, 0), (x1, y1, ze), wm, (7, 7)); bx(mb, (x0 - 0.15, y0 - 0.12, 0), (x1 + 0.15, y1 + 0.12, 0.45), M['stone2'], (6, 6))
    if roof == 'thatch': thatch_roof(mb, M, x0, x1, (y0 + y1) / 2, (y1 - y0) / 2, ze, zr, rg=rg, gable_mat=wm)
    else:
        for sg in (-1, 1):
            a = Vector((0, (y0 + y1) / 2 + sg * ((y1 - y0) / 2 + 0.9), ze - 0.3)); b = Vector((0, (y0 + y1) / 2, zr)); dv = b - a; Lr = dv.length; dv.normalize(); n = Vector((1, 0, 0)).cross(dv).normalized(); n = n if n.z > 0 else -n
            obox(mb, (a + b) / 2 + Vector(((x0 + x1) / 2, 0, 0)) + n * 0.2, (1, 0, 0), dv, n, L / 2 + 0.5, Lr / 2, 0.22, M['tile'], 0.25)
        for xe, nx_ in ((x0 - 0.3, -1), (x1 + 0.3, 1)): mb.oface([(xe, y0 - 0.9, ze - 0.3), (xe, y1 + 0.9, ze - 0.3), (xe, (y0 + y1) / 2, zr)], wm, [(0, 0), (1, 0), (0.5, 1)], (nx_, 0, 0))
    tops = []
    for c in chim:
        cx = x0 + L * c; chimney(mb, cx, (y0 + y1) / 2 + (1.2 if face < 0 else -1.2), ze - 0.4, zr + 1.6, M); tops.append((cx, (y0 + y1) / 2 + (1.2 if face < 0 else -1.2), zr + 2.4))
    if wall == 'plaster':
        n = max(2, int(L / 2.6)); fo = -0.1 * face
        for k in range(n + 1): xx = x0 + L * k / n; bx(mb, (xx - 0.14, min(yf, yf + face * -0.14) - (0.1 if face < 0 else 0), 0.45), (xx + 0.14, max(yf, yf) + (0.1 if face > 0 else 0) + (0 if face > 0 else 0), ze), M['oak_d'], (1, 4))
        for zz in (2.9, ze - 0.3): bx(mb, (x0, yf - (0.12 if face < 0 else 0), zz), (x1, yf + (0.12 if face > 0 else 0), zz + 0.25), M['oak_d'], (4, 1))
    nwin = max(2, int(L / 5.5)); xs = [x0 + L * (k + 0.5) / nwin for k in range(nwin)]; dk = min(range(nwin), key=lambda k: abs(xs[k] - (x0 + L * door_at)))
    for k, cx_ in enumerate(xs):
        if k == dk: door(mb, M, cx_, yf, 2.0, 3.9, face, M['door'] if seed % 2 else M['gate']); continue
        casement(mb, M, cx_, yf, win_z, 1.9, 2.2, face, True, rg, shutters)
        if ze > 5.0 and rg.random() < 0.5: casement(mb, M, cx_, yf, ze - 0.55, 1.5, 1.2, face, False, rg) if False else None
    for k in range(dormers):
        cx_ = x0 + L * (0.22 + 0.56 * k / max(1, dormers - 1) if dormers > 1 else 0.5); yy = (y0 + yf) / 2 + face * ((y1 - y0) / 2 - 0.2) if False else yf
        lumpy(mb, (cx_, yf - face * -0.2 + (0.1 * face), ze + 2.3), 1.7, M['thatch'], seed * 7 + k, seg=10, rings=6, rough=0.08, squash=0.6) if roof == 'thatch' else None
        casement(mb, M, cx_, yf - face * 0.55 * 0 + face * -0.9 * -1 if False else yf + face * -0.0, ze + 1.3, 1.5, 1.2, face, False, rg) if False else None
    if roses:
        for k in range(14):
            px = x0 + rg.uniform(0.3, L - 0.3); pz = rg.uniform(0.4, ze - 0.5); lumpy(mb, (px, yf + face * -0.35 * -1 + face * 0.15 * 0 - 0.4 * (face < 0) + 0.4 * (face > 0), pz), 0.34, M['leaf2'] if k % 3 else M['leaf'], seed * 11 + k, seg=6, rings=4, rough=0.25)
            if k % 2 == 0: mb.sphere((px + 0.1, yf + (-0.62 if face < 0 else 0.62), pz + 0.1), 0.13, M['rose'] if k % 4 else M['red'], seg=5, rings=3)
    return tops

def picket(mb, M, x0, x1, y, rg, gap=(-2.6, -0.4), h=1.4):
    for xx in np.arange(x0, x1, 0.6):
        if gap[0] - 0.1 < xx < gap[1] + 0.1: continue
        hh = h + 0.06 * math.sin(xx * 3); bx(mb, (xx - 0.15, y - 0.05, 0), (xx + 0.15, y + 0.05, hh), M['cream'], (1.2, 2)); cone(mb, (xx, y, hh), 0.17, 0.26, M['cream'], 4)
    for zz in (0.4, 1.0): bx(mb, (x0, y - 0.12, zz), (gap[0] - 0.1, y - 0.02, zz + 0.16), M['cream'], (3, 3)); bx(mb, (gap[1] + 0.1, y - 0.12, zz), (x1, y - 0.02, zz + 0.16), M['cream'], (3, 3))
    for xx in (gap[0] - 0.2, gap[1] + 0.2): post(mb, xx, y, 0, 2.3, 0.34, M['cream']); mb.sphere((xx, y, 2.42), 0.23, M['cream'], seg=6, rings=4)
    for xx in np.arange(gap[0] + 0.2, gap[1] - 0.1, 0.4): bx(mb, (xx - 0.09, y - 0.08, 0.3), (xx + 0.09, y - 0.03, 1.5 + 0.15 * math.sin(xx * 9)), M['gate'], (1, 2))

def church(mb, M, cx, cy, S=1.0):
    w = 6.5 * S; h = 38 * S; hm = M['church']
    bx(mb, (cx - w, cy - w, 0), (cx + w, cy + w, h), hm, (9, 9)); bx(mb, (cx - w - 0.6, cy - w - 0.6, h - 4.5 * S), (cx + w + 0.6, cy + w + 0.6, h - 3.2 * S), M['stone2'], (9, 9)); bx(mb, (cx - w - 0.7, cy - w - 0.7, h), (cx + w + 0.7, cy + w + 0.7, h + 2.0 * S), hm, (9, 9))
    for sx_ in (-1, 1):
        for sy_ in (-1, 1):
            bx(mb, (cx + sx_ * w - 1.0 * S, cy + sy_ * w - 1.0 * S, h + 2.0 * S), (cx + sx_ * w + 1.0 * S, cy + sy_ * w + 1.0 * S, h + 7.0 * S), hm, (9, 9)); cone(mb, (cx + sx_ * w, cy + sy_ * w, h + 7.0 * S), 1.1 * S, 3.0 * S, hm, 4)
            bx(mb, (cx + sx_ * (w + 0.9) - 0.9 * S, cy + sy_ * (w + 0.9) - 0.9 * S, 0), (cx + sx_ * (w + 0.9) + 0.9 * S, cy + sy_ * (w + 0.9) + 0.9 * S, 11 * S), M['stone2'], (6, 6))
    for dz in (14, 24): bx(mb, (cx - 1.2 * S, cy - w - 0.4, dz * S), (cx + 1.2 * S, cy - w, (dz + 6) * S), M['black'], (2, 2)); bx(mb, (cx - w - 0.4, cy - 1.2 * S, dz * S), (cx - w, cy + 1.2 * S, (dz + 6) * S), M['black'], (2, 2))
    bx(mb, (cx - 1.7 * S, cy - w - 0.4, h - 12 * S), (cx + 1.7 * S, cy - w, h - 4.0 * S), M['black'], (2, 2)); bx(mb, (cx - 1.6 * S, cy - w - 0.3, 0), (cx + 1.6 * S, cy - w, 5 * S), M['door'], (2, 2))
    bx(mb, (cx - 16 * S, cy + w * 0.4 - 7.5 * S, 0), (cx - w + 0.1, cy + w * 0.4 + 7.5 * S, 13 * S), hm, (9, 9)); zr = 13 * S; hw = 7.5 * S; xa, xb = cx - 17 * S, cx - w + 0.1; cy2 = cy + w * 0.4
    for sg in (-1, 1):
        a = Vector((0, cy2 + sg * (hw + 0.8), zr - 0.2)); b = Vector((0, cy2, zr + 5.2 * S)); dv = b - a; L = dv.length; dv.normalize(); nn = Vector((1, 0, 0)).cross(dv).normalized(); nn = nn if nn.z > 0 else -nn
        obox(mb, (a + b) / 2 + Vector(((xa + xb) / 2, 0, 0)) + nn * 0.3, (1, 0, 0), dv, nn, (xb - xa) / 2 + 0.4, L / 2 + 0.2, 0.3, M['churchr'], 0.2)
    for k in range(4): bx(mb, (cx - 15 * S + k * 3.6 * S, cy2 - hw - 0.1, 3 * S), (cx - 15 * S + k * 3.6 * S + 1.4 * S, cy2 - hw, 9 * S), M['black'], (1, 1))

def woodpile(mb, c, M, yaw=0.0, n=3, L=2.2):
    c = Vector(c); f = Vector((math.cos(yaw), math.sin(yaw), 0)); sd = Vector((-f.y, f.x, 0))
    for r_ in range(n):
        for k in range(n - r_ + 2): p = c + sd * ((k - (n - r_ + 1) / 2) * 0.36) + Vector((0, 0, 0.2 + r_ * 0.32)); rod(mb, p - f * L / 2, p + f * L / 2, 0.17, M['wood2'] if (k + r_) % 2 else M['wood'], seg=6)

def bench(mb, c, M, yaw=0.0, L=2.2):
    c = Vector(c); f = Vector((math.cos(yaw), math.sin(yaw), 0)); sd = Vector((-f.y, f.x, 0)); obox(mb, c + Vector((0, 0, 0.8)), f, sd, (0, 0, 1), L / 2, 0.3, 0.07, M['oak'], 0.5)
    for sg in (-1, 1): rod(mb, c + f * sg * (L / 2 - 0.2) + sd * 0.2, c + f * sg * (L / 2 - 0.25) + Vector((0, 0, 0.8)), 0.06, M['wood2'], seg=4); rod(mb, c + f * sg * (L / 2 - 0.2) - sd * 0.2, c + f * sg * (L / 2 - 0.25) + Vector((0, 0, 0.8)), 0.06, M['wood2'], seg=4)

def pot(mb, c, M, flower, rg, s=1.0):
    rod(mb, c, (c[0], c[1], c[2] + 0.5 * s), 0.3 * s, M['tile'], seg=8, r1=0.38 * s); stamp(mb, flower, (c[0], c[1], c[2] + 0.45 * s), rg.uniform(0, 6), 0.7 * s)

def facade_dress(mb, hm, M, P_, rg, x0, x1, yf, face, okp, n=7):
    """Doorstep life along a house front: barrels, pails, crates, baskets, benches, woodpiles, flower pots, churns, hay, a cobbled apron."""
    fl = [P_.flower(k) for k in ('marigold', 'viola', 'daisy', 'lavender')]
    mb.quad((x0 - 0.5, yf + (face * 0.0 if face > 0 else -2.2), 0.025), (x1 - x0 + 1.0, 0, 0), (0, 2.2, 0), M['cobble'], (0, 0, (x1 - x0) / 4, 0.55))
    for k in range(n):
        x = rg.uniform(x0 + 0.8, x1 - 0.8); y = yf + face * rg.uniform(0.9, 2.0); p = (x, y, 0.0); kind = rg.randrange(8)
        if not okp(p, 3.2): continue
        if kind == 0: stamp(mb, P_.barrel(), p, rg.uniform(0, 6), rg.uniform(0.7, 1.0))
        elif kind == 1: stamp(mb, P_.pail(rg.random() < 0.4), p, rg.uniform(0, 6), 0.7)
        elif kind == 2: stamp(mb, P_.crate(), p, rg.uniform(0, 3), 0.9)
        elif kind == 3: stamp(mb, P_.basket(rg.random() < 0.5), p, rg.uniform(0, 6), 0.9)
        elif kind == 4: bench(mb, p, M, 0.0 if face < 0 else 3.14159, 2.4)
        elif kind == 5: woodpile(mb, p, M, 0.0)
        elif kind == 6: pot(mb, p, M, fl[rg.randrange(len(fl))], rg, 1.0); pot(mb, (p[0] + 0.7, p[1], 0), M, fl[rg.randrange(len(fl))], rg, 0.8)
        else: stamp(mb, P_.churn(), p, 0, 0.7)
    for k in range(int((x1 - x0) * 2.0)): grass_tuft(hm, (rg.uniform(x0, x1), yf + face * rg.uniform(0.2, 1.2), 0.0), M['leaf2'], 0.3, 5, rg, 0.025)

def litter(mb, hm, M, P_, rg, rect, n, okp, nobar=()):
    """Small things on the ground (stones, droppings, straw, apples, fallen sticks, a dropped pail ...) so no floor is bare."""
    x0, x1, y0, y1 = rect
    for i in range(n):
        x, y = rg.uniform(x0, x1), rg.uniform(y0, y1)
        if not okp((x, y), 1.6): continue
        k = i % 6
        if k < 3: lumpy(mb, (x, y, 0.0), rg.uniform(0.08, 0.24), M['pebble'] if i % 2 else M['pebble2'], i, seg=6, rings=4, rough=0.25, squash=0.6)
        elif k == 3: strand_tuft(hm, (x, y, 0.02), M['straw'], n=5, h=0.25, spread=1.5, lean=1.0, w=0.014, rg=rg, flat=0.6)
        elif k == 4: lumpy(mb, (x, y, 0.0), 0.12, M['brown'], i, seg=5, rings=3, rough=0.3, squash=0.6)
        else: rod(mb, (x, y, 0.03), (x + rg.uniform(-0.7, 0.7), y + rg.uniform(-0.7, 0.7), 0.05), 0.025, M['wood2'], seg=3)

def fg_props(mb, hm, M, P_, SET, rg, cam, items, hooks=True):
    """Foreground dressing relative to the camera: items = [(kind, right, forward, yaw, scale)] placed on the floor at `forward` D ahead of the camera
    (along its ground heading) and `right` D to its right, so the lower third of every frame is never an empty floor."""
    cx, cy = cam['loc'][0], cam['loc'][1]; fx, fy = cam['look_at'][0] - cx, cam['look_at'][1] - cy; L = math.hypot(fx, fy); fx, fy = fx / L, fy / L; rx, ry = fy, -fx
    for (kind, r_, f_, yw, sc) in items:
        p = (cx + fx * f_ + rx * r_, cy + fy * f_ + ry * r_, 0.0)
        if kind == 'barrel': stamp(mb, P_.barrel(), p, yw, sc)
        elif kind == 'crate': stamp(mb, P_.crate(), p, yw, sc)
        elif kind == 'basket': stamp(mb, P_.basket(True), p, yw, sc)
        elif kind == 'pail': stamp(mb, P_.pail(False), p, yw, sc)
        elif kind == 'milk': stamp(mb, P_.pail(True), p, yw, sc)
        elif kind == 'stool': stamp(mb, P_.stool(), p, yw, sc)
        elif kind == 'churn': stamp(mb, P_.churn(), p, yw, sc)
        elif kind == 'sack': stamp(mb, P_.sack(int(abs(r_ * 7))), p, yw, sc)
        elif kind == 'hay': hay_heap(hm, p, M, sc, int(abs(r_ * 13 + f_)), 4)
        elif kind == 'wheelbarrow': wheelbarrow(mb, p, M, yw); hay_heap(hm, (p[0], p[1], 1.3), M, 0.6, 77, 3)
        elif kind == 'bench': bench(mb, p, M, yw, 2.2 * sc)
        elif kind == 'wood': woodpile(mb, p, M, yw)
        elif kind == 'rake': stamp(mb, P_.tool('rake'), (p[0], p[1], 0.08), yw, sc, pitch=1.52)
        elif kind == 'fork': stamp(mb, P_.tool('fork'), (p[0], p[1], 0.08), yw, sc, pitch=1.5)
        elif kind == 'goose': stamp(mb, P_.goose(), p, yw, sc)
        elif kind == 'dog': stamp(mb, P_.dog(), p, yw, sc)
        elif kind == 'cat': stamp(mb, P_.cat(True, int(abs(r_)) % 3), p, yw, sc)
        elif kind == 'pot': pot(mb, p, M, P_.flower('marigold'), rg, sc)
        elif kind == 'hen': hen(SET, M, p, yw, int(abs(f_)) % 3, True, rg.uniform(0, 6), 'fghen%d' % len(STATE['hooks']), proto=P_.hen(int(abs(f_)) % 3))

def village(SET, M, P, kd, lkey, PR):
    rg = R(11); mb = MB(); hm = MB(); fm = MB(); P_ = Protos(M); STATE['protos'] = P_; M['church'] = M['stone']; M['churchr'] = M['slate']; cxy = CAMS[PR['cam']]['loc']
    def okp(p, r=3.0): return math.hypot(p[0] - cxy[0], p[1] - cxy[1]) > r
    # ---------------- ground: grass, the lane, the green, flagged paths
    mb.quad((-700, -700, -0.05), (1400, 0, 0), (0, 1400, 0), M['grass'], (-700 / 8, -700 / 8, 700 / 8, 700 / 8))
    mb.quad((-150, -15.2, 0.0), (300, 0, 0), (0, 7.2, 0), M['lane'], (0, 0, 37.5, 1.0)); mb.quad((-150, -8.0, 0.0), (300, 0, 0), (0, 0.001, 0.0), M['lane'], (0, 0, 1, 1)) if False else None
    mb.quad((-60, -50, 0.0), (120, 0, 0), (0, 35, 0), M['grass_d'], (0, 0, 20, 6)); mb.quad((-60, -8.0, 0.0), (120, 0, 0), (0, 16.4, 0), M['grass_d'], (0, 0, 20, 3))
    mb.quad((-2.9, -8.0, 0.03), (2.4, 0, 0), (0, 17.0, 0), M['flag'], (0, 0, 1, 7)); mb.quad((-8.9, -3.9, 0.03), (6.6, 0, 0), (0, 2.1, 0), M['flag'], (0, 0, 3, 1))
    # ---------------- Jenner's cottage (honey stone, deep layered thatch, two chimneys, a kitchen wing)
    tops = house(mb, M, -10.0, 10.0, 9.0, 17.0, 5.6, 10.4, -1, 3, 'stone', 'thatch', (0.14, 0.7), 2, True, False)
    tops2 = house(mb, M, 10.0, 17.0, 9.5, 15.5, 4.2, 7.6, -1, 5, 'stone', 'thatch', (0.5,), 0, False, False)
    for k, (tx_, ty_, tz_) in enumerate(tops + tops2): smoke_puffs(SET, M, (tx_, ty_, tz_), 6, 12.0, (1.2, 0.3), 0.010, 'smoke%d' % k, k)
    bx(mb, (-4.2, 6.7, 4.1), (0.2, 9.1, 4.5), M['thatch_d'], (3, 3)); post(mb, -4.0, 7.0, 0, 4.1, 0.2, M['oak']); post(mb, 0.0, 7.0, 0, 4.1, 0.2, M['oak'])
    # ---------------- picket fence on the lane side, stone walls east and west, hedge, orchard gate
    picket(mb, M, -22.0, 22.0, -8.0, rg, (-2.6, -0.4))
    drystone(mb, (22.5, -8.0), (22.5, 30.0), 2.0, 1.0, [M['stone'], M['moss'], M['stone2']], rg); drystone(mb, (-22.5, -8.0), (-22.5, 30.0), 2.0, 1.0, [M['stone'], M['moss'], M['stone2']], rg)
    drystone(mb, (10.0, 18.0), (22.5, 18.0), 1.8, 0.9, [M['stone'], M['moss']], rg); drystone(mb, (-22.5, 22.0), (22.5, 22.0), 2.0, 1.0, [M['stone'], M['moss'], M['stone2']], rg)
    # ---------------- the rustic hut (round, woven walls, a deep layered conical thatch), door facing the garden
    hx, hy, hr = -12.0, -2.5, 2.8; da = math.radians(-20)
    rod(mb, (hx, hy, 0), (hx, hy, 3.3), hr, M['oak'], seg=14, r1=hr, uv=(5, 1))
    for k in range(10):                                                                  # roof of stepped straw rings
        z0_ = 3.2 + k * 0.38; r0 = hr + 1.05 - k * 0.3; rod(mb, (hx, hy, z0_), (hx, hy, z0_ + 0.45), r0, M['thatch'], seg=14, r1=max(0.2, r0 - 0.25), uv=(6, 1)); rod(mb, (hx, hy, z0_ - 0.02), (hx, hy, z0_ + 0.01), r0 + 0.05, M['thatch_d'], seg=14, r1=r0 + 0.05)
        for j in range(16): a = 6.2832 * (j + (k % 2) * 0.5) / 16; strand_tuft(hm, (hx + math.cos(a) * (r0 + 0.02), hy + math.sin(a) * (r0 + 0.02), z0_), M['straw2'], n=2, h=0.3, spread=0.3, lean=0.2, w=0.04, rg=rg, flat=-0.9)
    rod(mb, (hx, hy, 6.9), (hx, hy, 8.0), 0.5, M['thatch_d'], seg=8, r1=0.0); rod(mb, (hx, hy, 6.9), (hx, hy, 7.3), 0.35, M['thatch_d'], seg=8, r1=0.35)
    for k in range(10): a = k * 0.628 + 0.2; post(mb, hx + math.cos(a) * hr, hy + math.sin(a) * hr, 0, 3.4, 0.28, M['wood2'])
    dx, dy = hx + math.cos(da) * (hr + 0.1), hy + math.sin(da) * (hr + 0.1)
    dm = MB(); bx(dm, (-0.05, -0.8, 0), (0.25, 0.8, 2.7), M['door'], (2, 2)); bx(dm, (-0.1, -1.0, 2.7), (0.35, 1.0, 2.9), M['oak'], (2, 2)); bx(dm, (0.0, -1.1, 0), (1.3, 1.1, 0.16), M['stone2'], (2, 2)); stamp(mb, dm, (dx, dy, 0), da)
    stamp(mb, P_.stool(), (-8.0, -3.4, 0), 0.5, 0.95); bx(mb, (-9.6, -4.6, 0.0), (-8.2, -4.0, 0.7), M['oak'], (2, 2))                                # the boy's stool, a bench
    # ---------------- flower beds (cottage garden): back = tall, front = low, edged with stones
    flw_t = [P_.flower(k) for k in ('hollyhock', 'delphinium', 'foxglove', 'lupin')]; flw_m = [P_.flower(k) for k in ('lavender', 'marigold', 'rose', 'poppy')]; flw_l = [P_.flower(k) for k in ('daisy', 'viola', 'buttercup', 'marigold')]
    def bed(x0, x1, y0, y1, n):
        bx(mb, (x0, y0, 0), (x1, y1, 0.14), M['earth'], (4, 4)); drystone(mb, (x0, y0), (x1, y0), 0.35, 0.4, [M['stone2'], M['moss']], rg); drystone(mb, (x0, y1), (x1, y1), 0.35, 0.4, [M['stone2'], M['moss']], rg)
        h = y1 - y0
        for i in range(n):
            x, y = rg.uniform(x0 + 0.2, x1 - 0.2), rg.uniform(y0 + 0.3, y1 - 0.3); t = (y - y0) / h; fam = flw_l if t < 0.3 else (flw_m if t < 0.62 else flw_t)
            if okp((x, y), 2.0): stamp(hm, fam[rg.randrange(len(fam))], (x, y, 0.1), rg.uniform(0, 6.28), rg.uniform(0.8, 1.2))
        for i in range(int(n * 0.6)): grass_tuft(hm, (rg.uniform(x0, x1), rg.uniform(y0, y1), 0.1), M['leaf2'] if i % 2 else M['leaf'], 0.35, 6, rg, 0.025)
    bed(-8.2, -3.5, 0.0, 8.0, 150); bed(0.6, 8.0, -6.5, 7.8, 230); bed(8.4, 12.0, -6.5, 1.0, 90); bed(-20.5, -14.0, -6.8, -1.0, 80); bed(-20.5, -14.0, 1.5, 8.0, 80)
    for (x0_, x1_, y0_, y1_) in ((12.6, 21.5, -6.5, -2.0),):                                         # vegetable patch: cabbages and bean poles
        bx(mb, (x0_, y0_, 0), (x1_, y1_, 0.14), M['earth'], (4, 4))
        for i in range(36): stamp(hm, P_.flower('cabbage'), (x0_ + 0.8 + (i % 9) * 0.95, y0_ + 0.8 + (i // 9) * 1.0, 0.1), rg.uniform(0, 6), rg.uniform(0.8, 1.2))
    for (px, py) in ((15.0, 3.0), (17.5, 3.4), (19.5, 2.4)):
        for k in range(4): a = k * 1.57; rod(mb, (px + math.cos(a) * 0.8, py + math.sin(a) * 0.8, 0), (px, py, 4.3), 0.04, M['wood2'], seg=4)
        lumpy(mb, (px, py, 2.0), 0.9, M['leaf'], int(px * 10), seg=8, rings=5, rough=0.3, squash=2.0)
        for k in range(6): mb.sphere((px + rg.uniform(-0.6, 0.6), py + rg.uniform(-0.6, 0.6), rg.uniform(1.0, 3.6)), 0.09, M['red'], seg=4, rings=3)
    for (px, py) in ((7.0, -3.4), (8.7, -3.0), (6.0, -2.4)):                                       # bee skeps on a bench
        bx(mb, (px - 0.8, py - 0.4, 0.0), (px + 0.8, py + 0.4, 0.5), M['oak'], (1, 1)); rod(mb, (px, py, 0.5), (px, py, 1.1), 0.55, M['straw'], seg=10, r1=0.6); cone(mb, (px, py, 1.1), 0.52, 0.5, M['straw'], 10)
    rod(mb, (-21.0, -6.0, 0), (-21.0, -6.0, 2.0), 0.8, M['wood2'], seg=10); rod(mb, (-21.0, -6.0, 0.5), (-21.0, -6.0, 0.6), 0.85, M['iron'], seg=10)          # water butt
    for (x_, y_, yw, v) in ((-2.0, -6.0, 0.5, 0), (1.5, -5.2, 2.5, 1), (-5.0, -5.4, -1.0, 2), (4.0, -4.6, 1.0, 0), (9.0, 4.6, 0.2, 1), (-7.0, 3.0, 4.0, 2), (-16.0, 4.0, 1.0, 0), (13.5, -0.2, 3.0, 1)):
        if okp((x_, y_), 4.6): hen(SET, M, (x_, y_, 0), yw, v, True, rg.uniform(0, 6.28), 'vhen%d' % len(STATE['hooks']), proto=P_.hen(v))
    stamp(mb, P_.cat(True, 0), (22.0, 4.0, 2.0), 3.5); stamp(mb, P_.cat(False, 1), (-3.6, 9.4, 0.0), 0.3)
    if okp((3.0, -5.8), 4.5): stamp(mb, P_.dog(), (3.0, -5.8, 0.0), 2.6, 0.95)
    # washing line with sheets (they sway)
    for xx in (-19.5, -13.5): post(mb, xx, 9.5, 0, 6.0, 0.18, M['wood2'])
    rod(mb, (-19.5, 9.5, 5.8), (-13.5, 9.5, 5.8), 0.012, M['twine'], seg=3)
    for k, (sx_, cm) in enumerate(((-18.9, M['cloth']), (-17.4, M['cloth2']), (-15.9, M['cloth3']))):
        cl = MB(); cl.pid += 1; cl.face([Vector((0, 0, 0)), Vector((1.1, 0, 0)), Vector((1.1, 0, -1.8)), Vector((0, 0, -1.8))], cm, [(0, 0), (1, 0), (1, 1), (0, 1)]); o = mk_obj(cl, 'sheet%d' % k, SET, (sx_, 9.5, 5.8)); sway(o, 0.12, k * 1.3, (0, 1), 0.09); hook('cloth', o)
    # ---------------- orchard (west), the grazing cow, blossom and fruit, falling petals
    for i, (tx_, ty_) in enumerate(((-26, 3), (-30, 14), (-34, 6), (-38, 18), (-30, -4), (-44, 8), (-26, 26), (-36, 28), (-50, 20), (-48, -2), (-22, 14), (-24, -2))):
        tree(mb, (tx_, ty_, 0), 7.5 + (i % 3), 4.2 + (i % 2), M['wood2'], [M['leaf2'], M['leaf'], M['green']], 50 + i, blossom=[M['bloom_p'], M['bloom_w']], fruit=M['apple'] if i % 2 else None, nclump=16)
    cmb = MB(); cow(SET, cmb, M, (-31.0, 9.0, 0.0), 2.4, 'a', 0.85, 0.7, 'cowGraze'); cmb.obj('graze_cow', SET, smooth=True)
    falling_leaves(SET, M, (-30, -8, -6, 14), 30, 3, 11.0, 'petals', [M['bloom_p'], M['bloom_w']], 3, 0.14)
    scatter_grass(hm, rg, [M['leaf2'], M['leaf'], M['grass_d']], (-60, 60, -50, 8), 3200, 0.3, keep=lambda x, y: not (-15.2 < y < -8.0) and okp((x, y), 2.0) and not (-3.0 < x < -0.2 and y > -8.0)) if False else None
    fl = [P_.flower(k) for k in ('daisy', 'buttercup', 'cowparsley', 'poppy', 'viola')]
    # ---------------- lane verges: tufts, wild flowers, stones (fine, small)
    for (ya, yb) in ((-8.0, -6.8), (-16.0, -15.2)): scatter_grass(hm, rg, [M['leaf2'], M['leaf'], M['grass_d']], (-60, 60, ya, yb), 700, (0.2, 0.42), keep=lambda x, y: okp((x, y), 1.2))
    scatter_flowers(hm, rg, fl, (-60, 60, -16.0, -15.0), 160, 0.6, 0.95); scatter_flowers(hm, rg, fl, (-60, 60, -8.8, -8.0), 140, 0.6, 0.95)
    scatter_grass(hm, rg, [M['leaf2'], M['leaf'], M['grass_d']], (-36, 36, -50, -16), 2800, (0.2, 0.4), keep=lambda x, y: okp((x, y), 1.2) and not (math.hypot(x + 18, y + 32) < 6.5))
    scatter_flowers(hm, rg, fl, (-36, 36, -50, -16), 520, 0.6, 0.95, keep=lambda x, y: not (math.hypot(x + 18, y + 32) < 6.5))
    for i in range(160): lumpy(mb, (rg.uniform(-40, 40), rg.uniform(-15.0, -8.4), 0.0), rg.uniform(0.1, 0.25), M['moss'], i, seg=6, rings=4, rough=0.2, squash=0.6) if okp((0, 0), 0) else None
    # ---------------- the green: pond with reeds and ducks, the old oak, a stone well, a handcart and a wain, barrels
    pnd = MB(); pnd.pid += 1; pts = [(-18 + math.cos(a * 6.2832 / 24) * (6.0 + 0.7 * math.sin(a * 2.3)), -32 + math.sin(a * 6.2832 / 24) * (4.4 + 0.5 * math.sin(a * 1.7))) for a in range(24)]
    pnd.face([Vector((x, y, 0.04)) for x, y in pts], M['pond'], [(0, 0)] * 24); pnd.obj('pond', SET).visible_shadow = False
    for k in range(24):
        x, y = pts[k][0] * 1.0, pts[k][1]; lumpy(mb, (x, y, 0.0), rg.uniform(0.35, 0.6), M['moss'], k, seg=6, rings=4, rough=0.2, squash=0.6)
        if k % 2 == 0: [rod(mb, (x + rg.uniform(-0.3, 0.3), y + 0.5, 0), (x + rg.uniform(-0.5, 0.5), y + 0.5, rg.uniform(1.0, 1.8)), 0.03, M['leaf'], seg=3, r1=0.01) for _ in range(5)]
    for i, (x, y, yw) in enumerate(((-16.0, -31.0, 0.4), (-20.0, -33.0, 2.0), (-18.0, -29.8, 3.9))): stamp(mb, P_.goose(), (x, y, 0.06), yw, 0.62)
    tree(mb, (30.0, -32.0, 0), 13, 8.5, M['wood2'], [M['leaf2'], M['leaf'], M['green']], 91, nclump=28); tree(mb, (-36.0, -40.0, 0), 11, 6.5, M['wood2'], [M['leaf2'], M['leaf']], 92, nclump=22)
    rod(mb, (-6.0, -22.0, 0), (-6.0, -22.0, 1.0), 1.1, M['stone2'], seg=10, r1=1.2); rod(mb, (-6.0, -22.0, 1.0), (-6.0, -22.0, 1.2), 1.3, M['stone'], seg=10)
    for sg in (-1, 1): post(mb, -6.0 + sg * 1.0, -22.0, 1.0, 3.0, 0.2, M['oak'])
    bx(mb, (-7.2, -22.2, 3.0), (-4.8, -21.8, 3.2), M['oak'], (2, 1)); rod(mb, (-6.0, -22.0, 3.0), (-6.0, -22.0, 1.6), 0.015, M['twine'], seg=3); stamp(mb, P_.pail(), (-6.0, -22.0, 1.4), 0, 0.4)
    obox(mb, (9.0, -20.5, 1.5), (1, 0, 0), (0, 1, 0), (0, 0, 1), 2.6, 1.3, 0.35, M['oak'], 0.4); wheel(mb, (9.0, -19.2, 1.5), 1.4, M, (0, 1, 0)); wheel(mb, (9.0, -21.8, 1.5), 1.4, M, (0, 1, 0))
    for k in range(5): stamp(mb, P_.barrel(), (7.4 + k * 0.9, -20.5, 1.85), 0.0, 0.7)
    stamp(mb, P_.barrel(), (-12.0, -17.5, 0), 0, 1.0); stamp(mb, P_.barrel(), (-13.0, -17.8, 0), 0, 0.9); stamp(mb, P_.crate(), (-11.0, -17.6, 0), 0.4, 1.0)
    # ---------------- terraces along the lane (north and south), the church at the end of the lane
    row = [(22, 38, -6.2, 1.8, -1, 21, 'stone', 'thatch'), (-44, -26, -6.2, 1.8, -1, 22, 'plaster', 'thatch'), (-66, -48, -6.0, 2.4, -1, 23, 'stone', 'tile'), (-90, -70, -6.2, 2.0, -1, 24, 'moss', 'thatch'),
           (18, 38, -30.0, -22.0, 1, 25, 'plaster', 'thatch'), (-34, -14, -30.0, -22.2, 1, 26, 'stone', 'thatch'), (-58, -38, -30.0, -22.0, 1, 27, 'moss', 'thatch'), (-84, -62, -30.0, -22.2, 1, 28, 'plaster', 'tile'), (42, 62, -30.0, -22.0, 1, 29, 'stone', 'thatch'), (42, 64, -6.2, 1.8, -1, 30, 'stone', 'thatch')]
    for k, (x0, x1, y0, y1, fc, sd, wl, rf) in enumerate(row):
        t_ = house(mb, M, x0, x1, y0, y1, 5.4 + (k % 3) * 0.3, 10.0 + (k % 4) * 0.5, fc, sd, wl, rf, (0.2 + 0.5 * (k % 2),), 1, True, k % 2 == 0)
        if k % 3 == 0: smoke_puffs(SET, M, t_[0], 5, 11.0, (1.2, 0.3), 0.009, 'hsmoke%d' % k, k + 20)
        facade_dress(mb, hm, M, P_, rg, x0, x1, y0 if fc < 0 else y1, fc, okp, 6)
    litter(mb, hm, M, P_, rg, (-60, 60, -15.0, -8.2), 520, okp); litter(mb, hm, M, P_, rg, (-30, 30, -48, -22), 300, okp)
    for (x_, y_, yw) in ((26.0, -12.0, 0.3), (12.0, -10.0, 2.2), (-8.0, -9.4, 4.0), (-4.0, -14.0, 1.0), (3.0, -9.0, 5.2), (34.0, -10.0, 3.0)): stamp(mb, P_.goose(), (x_, y_, 0.0), yw, 0.85) if okp((x_, y_), 4.0) else None
    for (x_, y_, yw, v) in ((18.0, -13.5, 0.4, 0), (-14.0, -11.0, 2.0, 1), (30.0, -9.0, 3.0, 2), (6.0, -14.0, 1.0, 0), (-20.0, -9.5, 5.0, 1)): hen(SET, M, (x_, y_, 0), yw, v, True, rg.uniform(0, 6.28), 'lhen%d' % len(STATE['hooks']), proto=P_.hen(v)) if okp((x_, y_), 4.5) else None
    for (x_, y_, yw) in ((-24.0, -13.0, 0.1), (13.0, -9.6, 3.0)):                                                         # a parked hay cart and a handcart in the lane
        if okp((x_, y_), 4.5):
            obox(mb, (x_, y_, 1.7), (1, 0, 0), (0, 1, 0), (0, 0, 1), 2.8, 1.4, 0.4, M['oak'], 0.4); wheel(mb, (x_ + 0.5, y_ - 1.5, 1.5), 1.5, M, (0, 1, 0)); wheel(mb, (x_ + 0.5, y_ + 1.5, 1.5), 1.5, M, (0, 1, 0)); hay_heap(hm, (x_, y_, 2.0), M, 1.8, int(x_ * 3), 5)
            rod(mb, (x_ + 2.8, y_, 1.6), (x_ + 6.2, y_, 0.9), 0.1, M['wood2'], seg=5)
    stamp(mb, P_.dog(), (-3.0, -12.4, 0.0), 2.6, 0.95) if okp((-3.0, -12.4), 4.0) else None
    drystone(mb, (-100, -26.0), (-12, -26.0), 1.6, 0.9, [M['stone'], M['moss']], rg) if False else None
    church(mb, M, -108.0, -2.0, 1.4)
    for k, (x_, y_) in enumerate(((-96, -16), (-100, 12), (-120, 14), (-124, -12), (-90, 8))): tree(mb, (x_, y_, 0), 11, 3.6, M['wood2'], [M['yew']], 300 + k, nclump=10)
    for k in range(34): bx(mb, (-100 + (k % 8) * 3.0, -24 + (k // 8) * 3.0, 0), (-99.2 + (k % 8) * 3.0, -23.6 + (k // 8) * 3.0, 1.6 + 0.4 * (k % 3)), M['moss'], (1, 1)) if False else None
    drystone(mb, (-132, -20.0), (-84, -20.0), 1.4, 0.8, [M['stone'], M['moss']], rg); drystone(mb, (-132, 16.0), (-84, 16.0), 1.4, 0.8, [M['stone'], M['moss']], rg)
    # distant trees, sheep and hedged fields on the hills
    for (tx_, ty_, h_, r_) in ((60, 30, 11, 6), (90, 40, 12, 7), (-70, 26, 10, 6), (-60, 44, 11, 6.5), (110, -10, 11, 6.5), (80, -60, 12, 7), (-80, -50, 11, 6.5), (-30, 56, 11, 6), (30, 60, 12, 6.5), (0, -80, 12, 7)): tree(mb, (tx_, ty_, 0), h_, r_, M['wood2'], [M['leaf2'], M['leaf'], M['green']], int(tx_ + ty_), nclump=20)
    sh = MB(); ell(sh, (0, 0, 0.7), (0.7, 0.5, 0.45), M['sheep'], seg=7, rings=4); ell(sh, (0.62, 0, 0.7), (0.22, 0.18, 0.2), M['sheep_f'], seg=6, rings=3)
    for sg in (-1, 1):
        for x in (0.3, -0.3): rod(sh, (x, sg * 0.2, 0.4), (x, sg * 0.2, 0.0), 0.05, M['sheep_f'], seg=4)
    for i in range(50): x, y = rg.uniform(-60, 120), rg.uniform(30, 110); stamp(mb, sh, (x, y, 0.0), rg.uniform(0, 6.28), 1.0)
    for i in range(24): x, y = rg.uniform(-30, 40), rg.uniform(-46, -22); stamp(mb, sh, (x, y, 0.0), rg.uniform(0, 6.28), 1.0) if okp((x, y), 3.5) and math.hypot(x + 18, y + 32) > 8 else None
    def hf(x, y):
        r_ = math.hypot(x * 0.9, y + 8); k = sm(130, 480, r_); return -0.12 + 85 * k ** 1.15 * (0.55 + 0.45 * math.sin(x * 0.011 + 1.3) * math.cos(y * 0.009)) + 9 * k * math.sin(x * 0.03 + y * 0.012)
    hill_grid(SET, M, -720, 720, -720, 720, 120, 120, hf, uvs=(1.6, 1.6))
    FG = dict(
        garden_hut=[('pot', -2.2, 3.6, 0, 1.0), ('hen', 1.5, 4.8, 2.0, 1.0), ('basket', 2.4, 3.9, 0.3, 0.9), ('hay', -2.7, 5.0, 0, 0.45), ('wood', 3.2, 6.0, 1.0, 0.9), ('pail', 0.3, 3.2, 0, 0.7), ('goose', -1.0, 6.4, 5.0, 0.9)],
        lane_wide=[('barrel', -2.6, 5.0, 0, 1.0), ('crate', -2.0, 5.2, 0.5, 0.9), ('wheelbarrow', 2.5, 6.5, 2.8, 1.0), ('goose', 0.2, 4.2, 1.0, 0.9), ('hen', -0.6, 8.0, 2.0, 1.0), ('sack', 2.8, 4.0, 0.3, 0.9), ('hay', -2.5, 8.0, 0, 0.6)],
        lane_high=[('barrel', -5.0, 8.0, 0, 1.0), ('hay', 4.5, 7.0, 0, 0.8), ('goose', 1.5, 6.0, 2.0, 1.0), ('crate', -3.2, 6.0, 0.3, 0.9), ('hen', -1.0, 9.0, 3.0, 1.0), ('basket', 3.0, 5.2, 0.2, 0.9)],
        garden_queue=[('barrel', -3.2, 4.5, 0, 1.0), ('crate', -2.4, 4.8, 0.5, 0.9), ('hay', 3.0, 4.6, 0, 0.7), ('wheelbarrow', 3.0, 7.0, 3.3, 1.0), ('goose', 0.5, 3.8, 1.0, 0.9), ('sack', -1.0, 4.0, 0.3, 0.9), ('dog', 1.0, 6.2, 2.6, 0.95), ('basket', -3.4, 7.0, 0.3, 0.9), ('hen', -1.6, 6.0, 4.0, 1.0)])
    fg_props(mb, hm, M, P_, SET, rg, CAMS[PR['cam']], FG[PR['cam']])
    mb.obj('village', SET); hm.obj('village_flora', SET)

# ============================================================================= COTTAGE ROOM (the Phipps family room)
RX0, RX1, RY0, RY1, RZ = -7.5, 7.5, -3.6, 12.0, 5.6

def room(SET, M, P, kd, lkey, PR):
    rg = R(17); mb = MB(); gm = MB(); hm = MB(); fw = MB(); P_ = Protos(M); STATE['protos'] = P_; kdv = Vector(kd).normalized(); cxy = CAMS[PR['cam']]['loc']; night = bool(PR.get('candle'))
    def okp(p, r=3.0): return math.hypot(p[0] - cxy[0], p[1] - cxy[1]) > r
    sky_m = mat_emit('DY_win_%s' % lkey, '#d6e6f6' if lkey == 'A' else '#f2c898', strength=1.15); STATE['skym'] = sky_m
    # ---------------- floor, walls (plaster with timber posts), openings: left window over the bed, back window, right door
    mb.quad((-300, -300, -0.05), (600, 0, 0), (0, 600, 0), M['grass'], (-300 / 9, -300 / 9, 300 / 9, 300 / 9))
    mb.quad((RX0, RY0, 0.0), (15, 0, 0), (0, RY1 - RY0, 0), M['floorw'], (0, 0, 2.5, 4.1)); mb.quad((1.2, 8.6, 0.012), (6.3, 0, 0), (0, 3.4, 0), M['flag'], (0, 0, 1.6, 0.9)); mb.quad((5.4, 2.6, 0.012), (2.2, 0, 0), (0, 4.4, 0), M['flag'], (0, 0, 0.6, 1.1))
    mb.quad((-2.4, 0.2, 0.02), (4.8, 0, 0), (0, 6.6, 0), M['rug'], (0, 0, 1, 1)); mb.quad((-6.8, -3.4, 0.02), (3.4, 0, 0), (0, 2.6, 0), M['rug'], (0, 0, 1, 0.7))
    mb.quad((RX0, RY0, RZ), (15, 0, 0), (0, RY1 - RY0, 0), M['oak_d'], (0, 0, 3, 4))                                    # ceiling boards
    WT = 0.5
    def wall_x(xa, xb, y0, y1, hole=None):                           # a wall slab in the x = const plane (left x=RX0 or right x=RX1) with an optional hole (ya, yb, za, zb)
        if not hole: bx(mb, (xa, y0, 0), (xb, y1, RZ), M['plaster'], (6, 6)); return
        ya, yb, za, zb = hole; bx(mb, (xa, y0, 0), (xb, ya, RZ), M['plaster'], (6, 6)); bx(mb, (xa, yb, 0), (xb, y1, RZ), M['plaster'], (6, 6)); bx(mb, (xa, ya, 0), (xb, yb, za), M['plaster'], (6, 6)); bx(mb, (xa, ya, zb), (xb, yb, RZ), M['plaster'], (6, 6))
    WIN1 = (4.0, 9.0, 2.3, 5.2); DOOR_ = (3.0, 6.6, 0.0, 4.6)
    wall_x(RX0 - WT, RX0, RY0, RY1, WIN1); wall_x(RX1, RX1 + WT, RY0, RY1, (DOOR_[0], DOOR_[1], 0.0, DOOR_[3]) if True else None)
    bx(mb, (RX0, 12.0, 0), (RX1, 12.0 + WT, RZ), M['plaster'], (6, 6)) if False else None
    ya, yb, za, zb = (0.8, 4.2, 2.6, 5.3)                                                                           # back window (x range 0.8..4.2)
    bx(mb, (RX0 - WT, RY1, 0), (ya, RY1 + WT, RZ), M['plaster'], (6, 6)); bx(mb, (yb, RY1, 0), (RX1 + WT, RY1 + WT, RZ), M['plaster'], (6, 6)); bx(mb, (ya, RY1, 0), (yb, RY1 + WT, za), M['plaster'], (6, 6)); bx(mb, (ya, RY1, zb), (yb, RY1 + WT, RZ), M['plaster'], (6, 6))
    bx(fw, (RX0 - WT, RY0 - WT, 0), (RX1 + WT, RY0, RZ + 0.5), M['plaster'], (6, 6))                                    # front wall: hidden from the camera, still shades
    # window plates (bright outside), frames, mullions, sills, curtains
    wp = MB(); wp.pid += 1; wp.face([Vector((RX0 - 1.6, 4.0, 2.3)), Vector((RX0 - 1.6, 9.0, 2.3)), Vector((RX0 - 1.6, 9.0, 5.2)), Vector((RX0 - 1.6, 4.0, 5.2))], sky_m)
    wp.pid += 1; wp.face([Vector((0.8, RY1 + 1.6, 2.6)), Vector((4.2, RY1 + 1.6, 2.6)), Vector((4.2, RY1 + 1.6, 5.3)), Vector((0.8, RY1 + 1.6, 5.3))], sky_m); o = wp.obj('window_plates', SET); o.visible_shadow = False
    for (ya_, yb_, za_, zb_, x_, ax) in ((4.0, 9.0, 2.3, 5.2, RX0, 'x'), (0.8, 4.2, 2.6, 5.3, RY1, 'y')):
        if ax == 'x':
            for z_ in (za_ - 0.2, zb_): bx(mb, (RX0 - 0.1, ya_ - 0.25, z_), (RX0 + 0.5, yb_ + 0.25, z_ + 0.25), M['cream'], (2, 1))
            for y_ in (ya_ - 0.25, yb_): bx(mb, (RX0 - 0.1, y_, za_ - 0.2), (RX0 + 0.5, y_ + 0.25, zb_ + 0.25), M['cream'], (1, 2))
            for y_ in np.linspace(ya_, yb_, 4)[1:-1]: bx(mb, (RX0 - 0.1, y_ - 0.06, za_), (RX0 + 0.3, y_ + 0.06, zb_), M['cream'], (1, 2))
            bx(mb, (RX0 - 0.1, (ya_ + yb_) / 2 - 0.06, za_), (RX0 + 0.3, (ya_ + yb_) / 2 + 0.06, zb_), M['cream'], (1, 2)); bx(mb, (RX0 - 0.1, ya_, (za_ + zb_) / 2 - 0.06), (RX0 + 0.3, yb_, (za_ + zb_) / 2 + 0.06), M['cream'], (1, 2))
            bx(mb, (RX0, ya_ - 0.5, za_ - 0.35), (RX0 + 0.9, yb_ + 0.5, za_ - 0.1), M['oak'], (2, 1))
            for sg, y_ in ((-1, ya_ - 0.3), (1, yb_ + 0.3)): cl = MB(); bx(cl, (0, -0.35, -2.6), (0.2, 0.35, 0.0), M['cloth2'], (1, 2)); o = mk_obj(cl, 'curtainL%d' % sg, SET, (RX0 + 0.1, y_, zb_ + 0.2)); sway(o, 0.03, sg, (1,), 0.05); hook('curtain', o)
        else:
            for z_ in (za_ - 0.2, zb_): bx(mb, (ya_ - 0.25, RY1 - 0.1, z_), (yb_ + 0.25, RY1 + 0.5, z_ + 0.25), M['cream'], (2, 1))
            for x__ in (ya_ - 0.25, yb_): bx(mb, (x__, RY1 - 0.1, za_ - 0.2), (x__ + 0.25, RY1 + 0.5, zb_ + 0.25), M['cream'], (1, 2))
            for x__ in np.linspace(ya_, yb_, 3)[1:-1]: bx(mb, (x__ - 0.06, RY1 - 0.1, za_), (x__ + 0.06, RY1 + 0.3, zb_), M['cream'], (1, 2))
            bx(mb, (ya_, RY1 - 0.1, (za_ + zb_) / 2 - 0.06), (yb_, RY1 + 0.3, (za_ + zb_) / 2 + 0.06), M['cream'], (1, 2)); bx(mb, (ya_ - 0.5, RY1 - 0.9, za_ - 0.35), (yb_ + 0.5, RY1, za_ - 0.1), M['oak'], (2, 1))
    # posts and wall plates (vertical / receding only), the ceiling beams run along y
    for y_ in np.arange(-5.0, 12.0, 4.2):
        for x_ in (RX0 + 0.25, RX1 - 0.25):
            if x_ > 0 and DOOR_[0] - 0.8 < y_ < DOOR_[1] + 0.8: continue
            if x_ < 0 and WIN1[0] - 0.6 < y_ < WIN1[1] + 0.6: continue
            post(mb, x_, y_, 0, RZ, 0.5, M['oak'])
    for x_ in (RX0 + 0.1, RX1 - 0.4): bx(mb, (x_, RY0, RZ - 0.7), (x_ + 0.3, RY1, RZ), M['oak'], (3, 3))
    for x_ in (-4.0, 0.0, 4.0): bx(mb, (x_ - 0.28, RY0, RZ - 0.55), (x_ + 0.28, RY1, RZ), M['oak'], (3, 3))
    for (x_, y_) in ((RX0 + 0.25, 2.2), (RX1 - 0.25, 2.2), (RX1 - 0.25, 7.6)): pass
    # door frame, an open leaf, a step; the yard outside
    bx(mb, (RX1 - 0.15, DOOR_[0] - 0.35, 0), (RX1 + 0.6, DOOR_[0], DOOR_[3] + 0.3), M['oak'], (1, 3)); bx(mb, (RX1 - 0.15, DOOR_[1], 0), (RX1 + 0.6, DOOR_[1] + 0.35, DOOR_[3] + 0.3), M['oak'], (1, 3)); bx(mb, (RX1 - 0.15, DOOR_[0] - 0.35, DOOR_[3]), (RX1 + 0.6, DOOR_[1] + 0.35, DOOR_[3] + 0.4), M['oak'], (3, 1))
    obox(mb, (RX1 - 2.1, DOOR_[0] + 1.6, 2.3), (0.3, 0.95, 0), (-0.95, 0.3, 0), (0, 0, 1), 1.75, 0.09, 2.3, M['door'], 0.4) if False else None
    leaf = MB(); bx(leaf, (-0.1, 0, 0), (0.1, 3.3, 4.3), M['door'], (2, 2)); [bx(leaf, (-0.12, 0, z_), (0.12, 3.3, z_ + 0.14), M['iron'], (1, 1)) for z_ in (0.8, 3.2)]; o = mk_obj(leaf, 'door_leaf', SET, (RX1 - 0.1, DOOR_[0], 0), math.radians(-72))
    bx(mb, (RX1, DOOR_[0] - 0.8, 0), (RX1 + 2.2, DOOR_[1] + 0.8, 0.25), M['stone2'], (2, 2)); mb.quad((RX1 + 2.0, -20, 0.01), (14, 0, 0), (0, 60, 0), M['lane'], (0, 0, 2, 6))
    for (tx_, ty_, h_, r_) in ((RX1 + 22, 10, 9, 5), (RX1 + 30, -4, 10, 6), (RX1 + 18, 26, 9, 5)): tree(mb, (tx_, ty_, 0), h_, r_, M['wood2'], [M['leaf2'], M['leaf']], int(tx_ * 3 + ty_), nclump=14)
    # ---------------- the bed under the window: oak frame, tall head, quilted cover, pillow, a rag rug and slippers
    bx(mb, (-7.3, 2.4, 0.5), (-3.2, 8.8, 1.2), M['oak_d'], (2, 3)); bx(mb, (-7.2, 2.5, 1.2), (-3.3, 8.7, 1.62), M['hay'], (2, 3))
    bx(mb, (-7.25, 2.45, 1.62), (-3.25, 8.75, 1.68), M['quilt'], (4, 6)); bx(mb, (-7.2, 2.45, 1.6), (-3.2, 8.8, 1.7), M['quilt'], (4, 6)) if False else None
    lq = MB(); lq.box((-7.3, 2.4, 1.2), (-3.2, 6.6, 1.78), M['quilt'], tile=(4, 4))
    for (x_, y_) in ((-7.3, 2.4), (-3.2, 2.4), (-7.3, 8.8), (-3.2, 8.8)): post(mb, x_, y_, 0, 1.3 if y_ < 5 else 3.3, 0.34, M['wood2']); mb.sphere((x_, y_, 1.4 if y_ < 5 else 3.4), 0.2, M['wood'], seg=6, rings=4)
    bx(mb, (-7.35, 8.7, 0.5), (-3.15, 8.95, 3.2), M['oak'], (3, 3)); bx(mb, (-7.35, 2.35, 0.5), (-3.15, 2.6, 1.55), M['oak'], (3, 3))
    ell(mb, (-5.2, 8.0, 1.95), (0.9, 0.55, 0.28), M['cloth'], 1.57, 0.0, seg=9, rings=5); ell(mb, (-5.2, 7.9, 1.8), (0.95, 0.6, 0.2), M['cloth'], 1.57, seg=8, rings=4) if False else None
    for k in range(5): rod(mb, (-3.35, 2.8 + k * 0.9, 1.7), (-3.2, 2.8 + k * 0.9, 1.12), 0.02, M['twine'], seg=3)
    stamp(mb, P_.basket(False), (-2.4, 3.2, 0.0), 0.4, 0.8)
    # ---------------- the hearth: stone surround, hood, mantel, iron crane and pot, a fire
    bx(mb, (1.0, 11.0, 0.0), (7.3, 12.0, 0.25), M['flag'], (3, 1)); bx(mb, (1.2, 11.2, 0.25), (1.9, 12.0, 4.6), M['stone'], (1, 3)); bx(mb, (5.9, 11.2, 0.25), (6.6, 12.0, 4.6), M['stone'], (1, 3)); bx(mb, (1.0, 11.0, 4.6), (7.0, 12.0, 5.2), M['stone'], (4, 1))
    bx(mb, (1.6, 11.3, 5.2), (6.2, 12.0, RZ), M['stone'], (4, 3)); bx(mb, (0.9, 10.8, 4.5), (7.1, 11.6, 4.85), M['oak'], (4, 1)); bx(mb, (1.9, 11.9, 0.25), (5.9, 12.0, 4.6), M['blackiron'], (3, 3))
    flames = MB(); [cone(flames, (2.9 + k * 0.7, 11.5, 0.3), 0.34, 0.9 + 0.3 * (k % 2), M['flame'], 5) for k in range(4)]; [lumpy(flames, (2.7 + k * 0.7, 11.5, 0.3), 0.3, M['ember'], k, seg=6, rings=3, rough=0.2, squash=0.6) for k in range(5)]
    fo = mk_obj(flames, 'fire', SET, (0, 0, 0), shadow=False); drv(fo, 'scale', 2, '1.0+0.12*sin(frame*0.9)+0.07*sin(frame*1.7+1)'); hook('fire', fo)
    for k in range(4): rod(mb, (2.4 + k * 0.9, 11.2, 0.4), (2.7 + k * 0.9, 11.9, 0.4), 0.14, M['wood2'], seg=6)
    rod(mb, (6.0, 11.4, 0.4), (6.0, 11.4, 4.2), 0.06, M['blackiron'], seg=4); rod(mb, (6.0, 11.4, 4.2), (4.2, 11.4, 4.0), 0.06, M['blackiron'], seg=4); rod(mb, (4.2, 11.4, 4.0), (4.2, 11.4, 2.4), 0.03, M['blackiron'], seg=3)
    rod(mb, (4.2, 11.4, 1.7), (4.2, 11.4, 2.4), 0.5, M['blackiron'], seg=10, r1=0.62); ell(mb, (4.2, 11.4, 1.6), (0.62, 0.62, 0.45), M['blackiron'], seg=10, rings=5)
    for k, (x_, nm) in enumerate(((1.5, 'jug'), (2.4, 'cup'), (3.3, 'jug'), (4.2, 'cup'), (5.1, 'jug'), (6.0, 'cup'))): rod(mb, (x_ + 0.4, 11.2, 4.85), (x_ + 0.4, 11.2, 5.5 + 0.15 * (k % 2)), 0.2 if nm == 'jug' else 0.16, M['copper'] if k % 2 else M['cream'], seg=8, r1=0.14)
    stamp(mb, P_.basket(False), (1.2, 9.2, 0), 0.5, 0.8)
    for k in range(10): rod(mb, (7.0, 9.0 + k * 0.2, 0.2 + (k // 5) * 0.34), (7.4, 9.1 + k * 0.2, 0.2 + (k // 5) * 0.34), 0.16, M['wood2'], seg=5) if False else None
    woodpile(mb, (6.6, 9.4, 0), M, 1.57, 3, 1.6); stamp(mb, P_.cat(False, 0), (4.5, 10.2, 0.02), 2.4); stamp(mb, P_.dog(), (3.6, 9.6, 0.0), 3.6, 0.9)
    bx(mb, (2.0, 9.8, 0.02), (4.6, 10.6, 0.06), M['rug'], (1, 1)) if False else None
    # ---------------- the table with bench, chairs, bowls, a loaf and the candlestick
    tx_, ty_ = 3.2, 5.2
    bx(mb, (tx_ - 1.5, ty_ - 0.9, 1.95), (tx_ + 1.5, ty_ + 0.9, 2.1), M['oak'], (3, 2)); [post(mb, tx_ + sx * 1.3, ty_ + sy * 0.7, 0, 1.95, 0.18, M['wood2']) for sx in (-1, 1) for sy in (-1, 1)]
    bx(mb, (tx_ - 1.3, ty_ - 0.5, 0.45), (tx_ + 1.3, ty_ - 0.42, 0.6), M['wood2'], (2, 1)) if False else None
    bench(mb, (tx_, ty_ - 1.5, 0), M, 0.0, 2.8); bench(mb, (tx_, ty_ + 1.5, 0), M, 0.0, 2.8)
    cl = MB(); bx(cl, (tx_ - 1.0, ty_ - 0.25, 2.1), (tx_ + 1.0, ty_ + 0.25, 2.12), M['cloth'], (1, 1)); cl.obj('runner', SET)
    for (dx, dy, kk) in ((-0.9, 0.3, 0), (0.1, -0.3, 1), (0.9, 0.2, 2)):
        if kk == 0: rod(mb, (tx_ + dx, ty_ + dy, 2.1), (tx_ + dx, ty_ + dy, 2.3), 0.35, M['cream'], seg=10, r1=0.2)
        elif kk == 1: lumpy(mb, (tx_ + dx, ty_ + dy, 2.28), 0.22, M['straw2'], 5, seg=7, rings=4, rough=0.1, squash=0.6)
        else: rod(mb, (tx_ + dx, ty_ + dy, 2.1), (tx_ + dx, ty_ + dy, 2.55), 0.18, M['copper'], seg=8, r1=0.14)
    cx_c, cy_c = tx_ + 0.2, ty_ + 0.3; rod(mb, (cx_c, cy_c, 2.1), (cx_c, cy_c, 2.2), 0.28, M['brass'], seg=8, r1=0.18); rod(mb, (cx_c, cy_c, 2.2), (cx_c, cy_c, 2.7), 0.06, M['brass'], seg=6); rod(mb, (cx_c, cy_c, 2.7), (cx_c, cy_c, 3.1), 0.09, M['candle'], seg=6)
    STATE['candle'] = (cx_c, cy_c, 3.15)
    if night:
        fl = MB(); ell(fl, (0, 0, 0.0), (0.07, 0.07, 0.17), M['flame'], seg=6, rings=4); fo2 = mk_obj(fl, 'candle_flame', SET, (cx_c, cy_c, 3.2), shadow=False)
        drv(fo2, 'scale', 2, '1.0+0.18*sin(frame*0.8)+0.1*sin(frame*1.9+2)'); drv(fo2, 'scale', 0, '1.0+0.1*sin(frame*1.3)'); hook('candle', fo2)
        li = MN._light('candle_light', (cx_c, cy_c, 3.3), (1.0, 0.62, 0.30), 260.0, 0.12); drv(li.data, 'energy', -1, '260*(1.0+0.1*sin(frame*0.8)+0.06*sin(frame*2.1+1))') if False else None
        fc = li.data.driver_add('energy'); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '260*(1.0+0.1*sin(frame*0.8)+0.06*sin(frame*2.1+1))'; hook('candle_light', li)
        li2 = MN._light('hearth_light', (4.0, 10.6, 1.6), (1.0, 0.55, 0.22), 520.0, 0.4); fc = li2.data.driver_add('energy'); fc.driver.type = 'SCRIPTED'; fc.driver.expression = '520*(1.0+0.12*sin(frame*0.7)+0.08*sin(frame*1.9))'
    for (x_, y_, yw) in ((1.0, 4.4, 1.0), (5.5, 6.4, 3.0)):                                                              # two chairs
        c_ = MB(); bx(c_, (-0.45, -0.45, 1.0), (0.45, 0.45, 1.12), M['wood'], (1, 1)); [post(c_, sx * 0.38, sy * 0.38, 0, 1.0, 0.12, M['wood2']) for sx in (-1, 1) for sy in (-1, 1)]
        [post(c_, sx * 0.38, 0.4, 1.0, 2.6, 0.12, M['wood2']) for sx in (-1, 1)]; [bx(c_, (-0.4, 0.38, z_), (0.4, 0.44, z_ + 0.14), M['wood2'], (1, 1)) for z_ in (1.7, 2.2)]; stamp(mb, c_, (x_, y_, 0), yw)
    # ---------------- dresser with plates, the spinning wheel, shelves with jars, hanging herbs and hams
    bx(mb, (-2.6, 11.2, 0.0), (0.4, 12.0, 4.6), M['oak'], (3, 3)); bx(mb, (-2.7, 10.9, 0.0), (0.5, 11.3, 1.9), M['oak_d'], (3, 2))
    for k, z_ in enumerate((2.0, 3.2, 4.2)):
        bx(mb, (-2.6, 11.2, z_), (0.4, 11.9, z_ + 0.1), M['oak_d'], (3, 1))
        for j in range(5):
            x_ = -2.2 + j * 0.62
            if (j + k) % 3 == 1: rod(mb, (x_, 11.35, z_ + 0.1), (x_, 11.35, z_ + 0.7), 0.17, M['cream'], seg=8, r1=0.11)
            else: rod(mb, (x_, 11.7, z_ + 0.3), (x_, 11.78, z_ + 0.3), 0.3, M['cream'] if (j + k) % 2 else M['blue'], seg=12); rod(mb, (x_, 11.7, z_ + 0.3), (x_, 11.72, z_ + 0.3), 0.2, M['blue'] if (j + k) % 2 else M['cream'], seg=12)
    for sg, rr in ((1, 0.8),): wheel(mb, (6.2, 7.6, 1.9), 1.3, M, (0, 1, 0), 8); bx(mb, (5.2, 7.2, 0.0), (7.0, 8.0, 0.14), M['oak'], (1, 1))
    rod(mb, (6.2, 7.6, 1.9), (6.2, 8.9, 2.3), 0.06, M['wood2'], seg=4); post(mb, 5.4, 8.0, 0, 1.9, 0.14, M['wood2']); post(mb, 7.0, 8.0, 0, 1.9, 0.14, M['wood2'])
    for k in range(3): bx(mb, (RX1 - 0.9, 7.2 + k * 1.2, 3.8 + k * 0.0), (RX1, 7.8 + k * 1.2, 3.9), M['oak'], (1, 1)) if False else None
    bx(mb, (-3.0, 10.9, 4.6), (-3.0 + 0.1, 12.0, 4.6 + 0.1), M['oak'], (1, 1)) if False else None
    for (x_, y_, z_) in ((-1.2, 3.0, 5.6), (1.6, 6.5, 5.5), (-2.2, 8.0, 5.6), (4.8, 2.6, 5.5), (0.2, 1.0, 5.4)):
        rod(mb, (x_, y_, RZ - 0.5), (x_, y_, z_ + 0.7), 0.012, M['twine'], seg=3); rod(mb, (x_, y_, z_ + 0.7), (x_, y_, z_), 0.18, M['straw2'] if x_ > 0 else M['leaf'], seg=6, r1=0.06)
    for (x_, y_) in ((-3.0, 9.0), (0.8, 3.5)): rod(mb, (x_, y_, RZ - 0.5), (x_, y_, 4.6), 0.012, M['twine'], seg=3); lumpy(mb, (x_, y_, 4.2), 0.35, M['pink'], int(x_ * 10), seg=7, rings=5, rough=0.1, squash=1.4)
    for k in range(8): mb.sphere((RX1 - 0.4, 2.0 + k * 0.0, 0), 0.01, M['dark'], seg=3, rings=2) if False else None
    for k in range(3): bx(mb, (RX1 - 0.7, 8.0 + k * 1.1, 2.8 + k * 0.5), (RX1, 8.5 + k * 1.1, 2.9 + k * 0.5), M['oak'], (1, 1)) if False else None
    for k in range(5): rod(mb, (RX1 - 0.1, 7.6 + k * 0.7, 3.8), (RX1 - 0.6, 7.6 + k * 0.7, 3.8), 0.05, M['iron'], seg=4); cl_ = MB(); (bx(cl_, (-0.1, -0.2, -1.6), (0.1, 0.2, 0.0), M['cloth2'] if k % 2 else M['cloth3'], (1, 1)), mk_obj(cl_, 'coat%d' % k, SET, (RX1 - 0.65, 7.6 + k * 0.7, 3.8)))
    for (x_, y_, yw) in ((-6.2, -2.8, 0.6), (-4.8, -4.4, 2.0), (5.0, -3.2, 1.0)): stamp(mb, P_.stool(), (x_, y_, 0), yw, 0.9)
    for (x_, y_) in ((-6.8, 0.8), (4.6, 0.2), (-1.0, -3.2), (6.4, -4.8)): stamp(mb, P_.pail(False), (x_, y_, 0), 0.3, 0.6)
    for (x_, y_, yw, k) in ((-3.8, -2.2, 0.4, 1), (3.6, -3.6, 2.4, 0)): stamp(mb, P_.cat(False, k), (x_, y_, 0.02), yw, 0.8)
    for (x_, y_) in ((-6.4, -5.6), (-2.6, -5.4), (1.5, -5.8), (5.4, -5.6)): stamp(mb, P_.basket(True), (x_, y_, 0.0), x_, 0.9) if okp((x_, y_), 1.2) else None
    # sun shafts + motes in the window light
    ke = Vector(kdv); sf = mat_emit('DY_rshaft_%s' % lkey, '#ffd596', strength=0.07, additive=True, camera_only=True)
    def par(p, ex, ey, ez):
        p, ex, ey, ez = map(Vector, (p, ex, ey, ez))
        for a, b, o in ((ex, ey, Vector()), (ex, ey, ez), (ex, ez, Vector()), (ex, ez, ey), (ey, ez, Vector()), (ey, ez, ex)): gm.pid += 1; gm.face([p + o, p + o + a, p + o + a + b, p + o + b], sf)
    t1 = 2.6 / max(0.05, -ke.z); par(Vector((RX0, WIN1[0], WIN1[2])), Vector((0, WIN1[1] - WIN1[0], 0)), Vector((0, 0, WIN1[3] - WIN1[2])), ke * min(t1, 9.0))
    if ke.y < -0.05: par(Vector((0.8, RY1, 2.6)), Vector((3.4, 0, 0)), Vector((0, 0, 2.7)), ke * min(5.0 / max(0.05, -ke.z), 8.0))
    boxes = []
    for (p0, ex, ey, ez) in (((RX0, WIN1[0], WIN1[2]), (0, 4.0, 0), (0, 0, 2.6), None),):
        for t in (3.0, 6.0, 9.0):
            pm = Vector((RX0 + 0.5, 6.6, 4.2)) + ke * t
            if RX0 < pm.x < RX1 and 0.4 < pm.z < RZ: boxes.append((pm.x - 1.3, pm.x + 1.3, pm.y - 1.3, pm.y + 1.3, max(0.4, pm.z - 1.0), pm.z + 1.0))
    mote_groups(SET, M, rg, boxes or [(-3, 2, 3, 8, 0.8, 4)], 60, 3, amp=0.5)
    STATE['fw'] = fw
    mb.obj('room', SET); gm.obj('room_glow', SET).visible_shadow = False; hm.obj('room_straw', SET); fo = fw.obj('frontwall', SET); fo.visible_camera = False
    def hf(x, y): d = max(0.0, x - 50.0); r_ = sm(0, 300, d); return -0.1 + 40 * r_ ** 1.3 * (0.55 + 0.45 * math.sin(y * 0.008 + 1.3)) + 9 * r_ * math.sin(y * 0.03 + x * 0.01)
    hill_grid(SET, M, 40, 760, -420, 420, 48, 60, hf)

# ============================================================================= build / anchors / CLI
def build(preset=None, light=None, clear=True):
    """Build the preset's location with its light, sky, hooks and camera data into the current scene. Returns the anchors dict (API.md)."""
    preset = preset or 'barn_wide'; assert preset in PRESETS, 'preset %s is not one of %s' % (preset, list(PRESETS))
    PRc = PRESETS[preset]; loc = PRc['loc']; lkey = light or PRc['light']; assert lkey in LOC_LIGHTS[loc]
    scene, SET, P, kd = new_scene(lkey, PRc['sun'], PRc.get('P')); C, TX, E = STATE['C'], STATE['TX'], STATE['E']; M = mats(C, TX, E); STATE['M'] = M; STATE['preset'] = preset; STATE['loc'] = loc
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
