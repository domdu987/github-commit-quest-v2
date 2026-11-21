#!/usr/bin/env python3
"""shot.py -- film 22 take s09 (team 4): the ticket hall.  Crane DOWN from the ceiling lamps to the leaflet stand (porter sets the tiny TRIAL stack,
hands a few maps out), then low through walking passers-by toward the pillar: the official peeks out (36.19 s) and rubs his hands, smug, with
Q2 lip-sync 37.38-39.90 (frames 1122..1197).
    python3 shot.py stills 1005,1100 outdir | draft a:b:step | final a:b [samples]
Frames g 1005..1196 (local 0..191) + handles."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
from c22 import V, lerp, clamp, ez
import numpy as np
beck, U, BU, bpy = C.beck, C.U, C.BU, C.bpy
G0, G1 = 1005, 1197
Q2_ON = C.g_of(37.38) - G0          # local frame the lip-sync starts (about 119)
PEEK_ON = C.g_of(36.19) - G0        # 83: the official peeks out
OFF_HIDE = (-10.3, 16.4)            # behind the pillar
OFF_POS = (-11.7, 15.5)             # peek position (left of the pillar edge)

CAM = [(0, (2.0, -8.0, 12.5), (0.0, 10.0, 5.0), 26),
       (40, (3.0, -4.5, 8.0), (0.0, 10.0, 4.4), 28),
       (75, (4.2, -2.0, 3.6), (0.5, 11.0, 4.0), 30),
       (110, (1.5, 1.0, 2.6), (-6.0, 15.0, 3.2), 30),
       (150, (-4.2, 5.8, 2.2), (-10.3, 16.0, 3.4), 31),
       (191, (-7.4, 9.6, 1.9), (-11.4, 15.8, 3.2), 32)]

# ---- crowd walkers: (crowd index, (x0, y0) -> (x1, y1) over the take, mirror)
WALKS = [(2, (-18.0, 4.0), (-16.5, 14.0), False), (7, (15.0, 5.0), (6.5, 5.0), True), (11, (14.0, 14.0), (6.0, 15.0), True),
         (4, (-4.0, 24.0), (-14.0, 22.0), True), (13, (16.0, 22.0), (9.0, 21.0), True), (9, (-17.0, 20.0), (-17.0, 8.0), False)]

def ground_fixes():
    # QA section K: nothing floats.  (1) pendant globes hang on their cords from the ceiling -> mounted; (2) the entrance WAY OUT sign is behind the
    # camera and hovers above the door frame -> hidden; (3) the TRIAL sign gets real struts from its rods back to the stand cap; (4) floor light pools
    # sit on the floor (lowered 4 cm)
    for n in ('lamps', 'lamp_halos'):
        ob = bpy.data.objects.get(n)
        if ob: ob['mounted'] = True
    ob = bpy.data.objects.get('way_out_sign')
    if ob: ob.hide_render = True
    ob = bpy.data.objects.get('pools_h')
    if ob: ob.location = (ob.location[0], ob.location[1], ob.location[2] - 0.04)
    C_ = BU._cs()[0]; sx, sy = BU.STAND; br = beck.Part('stand_struts', (sx, sy, 6.5), ink=True); dark = C_('#4a2410', 1.0, 1.8)
    for dx in (-2.0, 2.0):
        br.mb.box((sx + dx - 0.12, sy - 1.2, 6.38), (sx + dx + 0.12, sy + 0.9, 6.62), dark)
    ob = br.done((sx, sy, 6.5), px=3); ob['mounted'] = True   # struts run back into the cap strip of the stand (seen touching)
    for n in ('stand_sign_trial', 'stand_sign_real'):
        o2 = bpy.data.objects.get(n)
        if o2: o2['mounted'] = True   # sign rods stand on the struts

def hook():
    ground_fixes()
    # people: named cast restaged away from the camera-to-pillar line
    for nm in ('beck', 'porter2', 'pass_man', 'pass_woman', 'porter', 'pass_child', 'official'): C.hide_actor(nm)
    C.POR = C.Idle('por', 'porter_hand_map', (1.6, 7.9, 0.0), '#ffb878', period=30, n=8, lean=2.0, roll=3.0)
    C.PMN = C.Idle('pmn', 'pass_read_map', (-3.0, 14.5, 0.0), '#a8bcff', period=46, n=8, lean=1.5, roll=2.5, phase=0.3)
    C.PWM = C.Idle('pwm', 'pass_tap_map', (3.4, 5.6, 0.0), '#ffb878', period=38, n=8, lean=1.5, roll=3.0, phase=0.6)
    C.PCH = C.Idle('pch', 'pass_smile_board', (5.2, 3.6, 0.0), '#a8bcff', period=28, n=8, lean=2.0, roll=3.0, phase=0.1)
    # the official: peek (idle) then the smug rub with Q2 mouths (4 mouths x 2 hand phases)
    c, p = C.STORY['off_smug_rub']; pk = C.STORY['off_peek'][1]
    extra = {}
    for mi, mo in enumerate(('flat', 'talk_a', 'talk_b', 'talk_o')):
        for hp in (0, 1):
            q = dict(p); q['mouth'] = mo; d = 0.05 if hp else -0.05
            q['arm_r'] = dict(p['arm_r'], hand=(p['arm_r']['hand'][0] + d, p['arm_r']['hand'][1])); q['arm_l'] = dict(p['arm_l'], hand=(p['arm_l']['hand'][0] - d, p['arm_l']['hand'][1]))
            q['head_roll'] = p.get('head_roll', 0) + (1.5 if hp else -1.0); q['pillar'] = 0
            extra['r%d%d' % (mi, hp)] = (c, q)
    C.OFF = C.Idle('off', 'off_peek', (OFF_HIDE[0], OFF_HIDE[1], 0.0), '#a8bcff', period=36, n=8, lean=1.5, roll=3.0, base_over=dict(pillar=0), extra_poses=extra)
    # crowd: hide the static hall crowd near the camera path / sight line; walkers replace them
    keys = [beck.cam_eval(CAM, f)[0] for f in range(0, 192, 6)]
    off_ = V((OFF_POS[0], OFF_POS[1], 1.5))
    def near(x, y, z):
        for k in keys:
            if math.hypot(x - k.x, y - k.y) < 7.5: return True
        for k in keys[18:]:
            ab = off_ - k; ap = V((x, y, 1.5)) - k; t = clamp(ap.dot(ab) / ab.length_squared)
            if (ap - ab * t).length < 2.6: return True
        return False
    n = 0
    for nm in list(U.ACTORS):
        if nm.startswith('hc'):
            x, y, z = U.ACTORS[nm]['mark']
            if near(x, y, z): C.hide_actor(nm); n += 1
    C.WK = [C.Walker('w%d' % i, w[0], '#ffb878' if i % 2 else '#a8bcff', mirror=w[3]) for i, w in enumerate(WALKS)]

def anim(f, n):
    if not hasattr(C, 'WK'): return
    U.face_cards(); BU.set_trial_stack(0 if f < 6 else 1 if f < 30 else 2)
    for o in (C.POR, C.PMN, C.PWM, C.PCH): o.update(f)
    # official
    d = U.ACTORS['off']
    if f < PEEK_ON - 6:
        for ob in d['poses'].values(): ob.hide_render = True
        sh = bpy.data.objects.get('shadow_act_off_main')
        if sh: sh.hide_render = True
    else:
        sh = bpy.data.objects.get('shadow_act_off_main')
        if sh: sh.hide_render = False
        u = ez((f - (PEEK_ON - 6)) / 12.0)
        C.move_actor('off', (lerp(OFF_HIDE[0], OFF_POS[0], u), lerp(OFF_HIDE[1], OFF_POS[1], u), 0.0))
        if f < Q2_ON - 2: C.OFF.update(f)
        else:
            g = G0 + f; lev = C.cast22.talk_mouth(g, 1.0, hold=2)
            mi = ('flat', 'talk_a', 'talk_b', 'talk_o').index(lev); hp = (f // 5) % 2
            U.set_pose('off', 'r%d%d' % (mi, hp))
    for i, w in enumerate(WALKS):
        t = f / 191.0; x = lerp(w[1][0], w[2][0], t); y = lerp(w[1][1], w[2][1], t)
        sp = math.hypot(w[2][0] - w[1][0], w[2][1] - w[1][1]) / (191 / 30.0)
        C.WK[i].at(x, y, 0.0, f / 30.0 * sp / 2.2)

CFG = dict(f0=G0, f1=G1, cam=CAM, animate={'a': anim},
           state={'set_rack': 0.0, 'set_crowd': (34, 3), 'set_stand_sign': 'trial'})
if __name__ == '__main__':
    C.run('s09', CFG, sys.argv[1:], hook_after_build=hook)
