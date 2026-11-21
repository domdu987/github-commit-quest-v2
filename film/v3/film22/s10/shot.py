#!/usr/bin/env python3
"""shot.py -- film 22 take s10 (team 4): the turn.  CUT on "แต่วันนั้น".  Side tracking along the near platform as the red train pulls in out of the dark
tunnel; the official hides behind the foreground bench; passengers unfold their pocket maps all together (41.28 s), glance up, step confidently into
the doors (42.38 s) with nobody lost; pass_child points at the line colour; 1-s PUSH-IN on the official's jaw drop (42.4 s).
    python3 shot.py stills 1197,1250 outdir | draft a:b:step | final a:b [samples]
Frames g 1197..1300 (local 0..103) + handles."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import V, lerp, clamp, ez
import numpy as np
beck, U, BU, bpy = C.beck, C.U, C.BU, C.bpy
G0, G1 = 1197, 1301
JAW_ON = 78                      # official's jaw drops (42.4 s = g 1275 = local 78)
DOORS_ON = 78

CAM = [(0, (-11.2, -5.0, 3.7), (-1.2, 17.0, 2.9), 30),
       (36, (-11.0, -0.6, 3.7), (-2.5, 18.0, 3.0), 30),
       (62, (-10.9, 3.4, 3.6), (-6.0, 12.0, 3.1), 31),
       (74, (-10.7, 5.2, 3.6), (-8.2, 9.0, 2.9), 33),
       (103, (-10.4, 5.8, 3.8), (-8.2, 9.0, 2.6), 37)]
OFF = (-8.4, 9.0, 0.0)

def pre_pose(c, p):
    q = {k: v for k, v in p.items() if k not in ('prop_r', 'prop_l')}
    q.update(expr='neutral', mouth='flat', arm_r=dict(hand=(0.45, 0.98), bend=0.4, layer='front'), prop_r=dict(type='pocketmap'), arm_l='down', gaze=(0.6, 0.2), pitch=0.0, head_roll=0, yaw=0.45)
    return (c, q)

# (name, crowd index or story, mark x, y, switch frame, door y)
WAIT = [('wA', 1, (-5.3, 13.4), 41, 17.0), ('wB', 3, (-6.4, 16.0), 45, 17.0), ('wC', 6, (-4.9, 18.2), 48, 24.5),
        ('wD', 8, (-7.0, 19.5), 43, 24.5), ('wE', 10, (-5.6, 22.5), 52, 24.5), ('wF', 12, (-6.6, 25.5), 46, 24.5)]

JAWS = {}
for _k in range(6):
    _c, _p = C.STORY['off_jaw_drop']; _q = dict(_p); _q['head_dy'] = 0.03 + 0.03 * math.sin(_k * 2 * math.pi / 6); _q['lean'] = 2.0 * math.sin(_k * 2 * math.pi / 6 + 1.0); _q['sweat'] = 1.0
    JAWS['jaw%d' % _k] = (_c, _q)

def hook():
    C.mount(['ribs', 'globes', 'hang_s10', 'clock', 'clock_face', 'liner', 'way_out', 'old_map', 'old_map_img', 'doors_closed', 'doors_open', 'benches_s10', 'roundel_name', 'name_panels', 'posters'])
    C.mount(['tunnel_lamps', 'globe_halos', 'light_pools', 'headlights'], airborne=True)
    sc = bpy.context.scene
    # MIND THE GAP edge plate: hide it (mirrored from this side)
    for nm in ('edge_signs',):
        ob = bpy.data.objects.get(nm)
        if ob: ob.hide_render = True
    # benches: hide the old pink slabs, rebuild slatted wooden benches
    ob = bpy.data.objects.get('benches')
    if ob: ob.hide_render = True
    C_ = BU._cs()[0]; bn = beck.Part('benches_s10', (0, 15, 1), ink=True)
    for (x, y0_, y1_, bk) in ((-BU.RX + 1.1, 24.0, 30.0, -1), (-BU.RX + 1.1, 35.0, 41.0, -1), (-9.2, 1.5, 7.5, -1), (BU.RX - 1.1, 6.0, 12.0, 1), (BU.RX - 1.1, 26.0, 32.0, 1)): C.bench_new(bn.mb, x, y0_, y1_, bk, C_)
    bn.done((0, 15, 1), px=3)
    ob = bpy.data.objects.get('hang_signs')
    if ob: ob.hide_render = True
    E = BU._cs()[2]; UVq = BU.UV_; hs = beck.Part('hang_s10', ink=True); mb = hs.mb
    for (yy, im, xx) in ((28.0, 'sign_to_trains', 7.8),):
        BU.rod(mb, (xx - 1.6, yy, 11.0), (xx - 1.6, yy, 8.6), 0.05, C_('#222244'), seg=4); BU.rod(mb, (xx + 1.6, yy, 11.0), (xx + 1.6, yy, 8.6), 0.05, C_('#222244'), seg=4)
        mb.pid += 1; mb.face([V((xx - 2.2, yy, 7.4)), V((xx + 2.2, yy, 7.4)), V((xx + 2.2, yy, 8.8)), V((xx - 2.2, yy, 8.8))], E('hs_%d' % yy, im, k=1.5), UVq)
        mb.pid += 1; mb.face([V((xx + 2.2, yy + 0.02, 7.4)), V((xx - 2.2, yy + 0.02, 7.4)), V((xx - 2.2, yy + 0.02, 8.8)), V((xx + 2.2, yy + 0.02, 8.8))], E('hs_%d' % yy, im, k=1.5), UVq)
    hs.done((0, 12, 8), px=3)
    print('objects:', sorted(o.name for o in bpy.data.objects if not o.name.startswith(('act_', 'shadow_', 'BK_')))[:60])
    for nm in list(U.ACTORS):
        x, y, z = U.ACTORS[nm]['mark']
        if nm.startswith(('np', 'fp')) and y < 40 and x < 0: C.hide_actor(nm)
    for nm in ('pass_woman', 'pass_man', 'pass_child', 'porter', 'official'): C.hide_actor(nm)
    C.WT = []
    for (nm, i, (x, y), t, dy) in WAIT:
        cc, pp = C.cast22.crowd_member(i, 'pass_unfold_map')
        w = C.Idle(nm, pre_pose(cc, pp), (x, y, 0.0), '#a8bcff' if i % 2 else '#ffb878', period=40, n=6, lean=1.5, roll=2.0, alt=(cc, pp), phase=(i % 5) / 5.0)
        w.t_sw, w.door_y, w.pos = t, dy, (x, y); C.WT.append(w)
    C.WK = [C.Walker('k%d' % k, w[1], '#a8bcff' if w[1] % 2 else '#ffb878', mirror=False) for k, w in enumerate(WAIT)]
    C.CHILD = C.Idle('child', 'pass_smile_board', (-4.8, 10.6, 0.0), '#a8bcff', period=24, n=8, lean=2.5, roll=3.0, phase=0.2)
    C.OFF = C.Idle('off', 'off_peek', OFF, '#a8bcff', period=34, n=8, lean=2.0, roll=2.5, base_over=dict(pillar=0), extra_poses=JAWS)
    C.OFF_JAW = [C.STORY['off_jaw_drop']]
    for k in range(4):
        c, p = C.STORY['off_jaw_drop']; q = dict(p); q['head_dy'] = 0.03 + 0.02 * math.sin(k * 1.6); q['sweat'] = 1.0
        # extra variants appended through U.actor is not possible after creation: jaw variants are built in the Idle as extra poses below

def anim(f, n):
    if not hasattr(C, 'OFF'): return
    U.face_cards()
    BU.set_train(max(6.0, 60.0 - 54.0 * min(1.0, max(0.0, f) / 70.0) ** 0.8)); BU.set_doors(1.0 if f > DOORS_ON else 0.0)
    C.CHILD.update(f)
    for i, w in enumerate(C.WT):
        if f < w.t_sw: w.update(f, alt=False)
        elif f < 66 + i * 2: w.update(f, alt=True)
        else:
            for ob in U.ACTORS[w.name]['poses'].values(): ob.hide_render = True
            sh = bpy.data.objects.get('shadow_act_%s_main' % w.name)
            if sh: sh.hide_render = True
    for i, w in enumerate(C.WT):
        k = C.WK[i]; ts = 66 + i * 2
        if f < ts: k.hide()
        else:
            u = clamp((f - ts) / 24.0)
            if u >= 1.0: k.hide()
            else: k.at(lerp(w.pos[0], -3.3, ez(u)), lerp(w.pos[1], w.door_y, ez(u)), 0.0, (f - ts) / 30.0 * 1.6 / 2.2)
    if f < JAW_ON: C.OFF.update(f)
    else: U.set_pose('off', 'jaw%d' % (((f - JAW_ON) // 3) % 6))

CFG = dict(f0=G0, f1=G1, cam=CAM, animate={'a': anim}, state={'set_train': 60.0})
if __name__ == '__main__':
    C.run('s10', CFG, sys.argv[1:], hook_after_build=hook)
