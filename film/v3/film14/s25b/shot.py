#!/usr/bin/env python3
"""film 14 take s25: shots 25-30 (herd flees, dawn, the uncle's field at night, sheepish uncle, stung on the stool, the swollen nose).
usage: python3 shot.py render SHOT g0:g1[:step] OUTDIR scale samples [threads]      (SHOT 25..30; one location per process)
       python3 shot.py probe SHOT g                                                (prints placements / head pixels, no render)
Frames g = film frames; narration clock g = round((t + 0.10) * 30), shot bounds round(t * 30).
Hooks are immediate and called for every frame; the camera, every card and every hook are re-set per frame (no keyframes)."""
import sys, os, math, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, cast14, bpy, Vector, lerp, lerp3, ez, mixu, story, put, card, cam_set, screen, MPD
import numpy as np

def gb(t): return int(round(t * 30))
def ge(t): return int(round((t + 0.10) * 30))
B = {25: (gb(55.92), gb(58.81)), 26: (gb(58.81), gb(61.34)), 27: (gb(61.34), gb(63.79)), 28: (gb(63.79), gb(65.39)), 29: (gb(65.39), gb(67.74)), 30: (gb(67.74), 2104)}
# frames each shot must be rendered for (take handle 6 before 1678; dissolves into 26 (8 f) and 28 (6 f) are baked in the take: both shots overlap +-4 / +-3)
RANGES = {25: (B[25][0] - 6, B[26][0] + 6), 26: (B[26][0] - 4, B[26][1]), 27: (B[27][0], B[28][0] + 5), 28: (B[28][0] - 3, B[28][1]), 29: (B[29][0], B[29][1]), 30: (B[30][0], 2104)}
BLINK_SEED = {'matriarch': 0, 'elephant_b': 17, 'elephant_c': 33, 'elephant_d': 51, 'calf': 70}

# ------------------------------------------------------------------------------------------------ shot 25: the herd turns and flees AWAY along the fence (NIGHT, low camera at the right end of the fence)
# v2: the camera sits at the right end of the front fence and looks along it to the left, so the herd that runs left RECEDES in depth (scale 1.0 -> 0.4)
CAM25 = lambda g: (lerp3((6.0, 6.6, 1.45), (5.3, 6.5, 1.45), mixu((g - 1672) / 100.0)), lerp3((-6.0, -10.0, -3.4), (-10.0, -11.0, -3.3), mixu((g - 1672) / 100.0)), 22.0)
HERD = [  # cast, x0, y0 (at the virtual start gs), gs, run speed   -- s25b v2: the herd is ALREADY turned and running at g1672 (shot 24 ends on the trumpet)
    ('elephant_b', 4.2, 0.2, 1664, 1.6), ('calf', 0.9, 1.4, 1664, 1.6), ('matriarch', 2.4, 2.6, 1664, 1.6), ('elephant_c', -0.6, 2.2, 1664, 1.6), ('elephant_d', -2.4, 3.2, 1664, 1.6)]
RUND = (-0.78, -0.62)   # run direction: away from the fence and the camera (into depth), drifting to the left
PPD25 = 96
TURN = 0            # s25b: NO cross-fade turn: the frontal card is swapped for the running side card on ONE frame, behind a dust crown
RUNK = 1.7          # the herd runs 2.2x the original distance per cycle frame (panic gallop): it must visibly LEAVE
def run_dist(cast, speed, g, gs):
    """metres run since the swap at frame gs, with a short ramp-up; and the cycle phase (no foot slip: phase advances with distance)"""
    cyc_m = cast14.cycle_distance(cast, 'run', speed) * MPD; x = 0.0; ph = 0.0
    for k in range(gs, g):
        v = RUNK * cyc_m / 28.0 * min(1.0, 0.3 + 0.7 * (k - gs + 1) / 8.0); x += v; ph += v / cyc_m
    return x, ph
DUSTS = {}
def yaw_to(cam, m):
    return math.atan2(cam[0] - m[0], -(cam[1] - m[1]))
def shot25(g, rep):
    sc = bpy.context.scene; loc, look, lens = CAM25(g); cam_set(loc, look, lens)
    for cast, x0, y0, gs, spd in HERD:
        d = DUSTS.setdefault(cast, (C.Dust(seed=7 + len(DUSTS)), C.Dust(seed=70 + len(DUSTS))))
        cyc_m = cast14.cycle_distance(cast, 'run', spd) * MPD
        pos = lambda k: (x0 + RUND[0] * run_dist(cast, spd, k, gs)[0], y0 + RUND[1] * run_dist(cast, spd, k, gs)[0])
        if not getattr(d[0], 'done', False):        # emit the whole history once (deterministic)
            d[0].done = True; last = -9
            for k in range(gs - 5, 1830):
                if k == gs - 4: d[0].burst(k, x0 + 0.4, n=70, dirx=-1.0, power=1.2)        # the crown that covers the turn
                if k in (gs + 6, gs + 14, gs + 24) and k <= gs + 24: d[0].burst(k, x0 + RUND[0] * run_dist(cast, spd, k, gs)[0] + 0.8, n=26, dirx=-1.0, power=0.55)
                if k >= gs:
                    xr, ph = run_dist(cast, spd, k, gs); xk = x0 + RUND[0] * xr
                    if int(ph * 2) != int(run_dist(cast, spd, k - 1, gs)[1] * 2) and k - last >= 5:   # every foot strike: a crown of droplets + wisps
                        last = k; d[0].burst(k, xk + 0.8, n=70, dirx=-1.0, power=1.0)
                    d[1].trail(k, xk + 0.9, dirx=-1.0, power=1.3 * (0.5 + 0.5 * min(1, (k - gs) / 12)), n=14)
        if g < gs - TURN:
            r = put('s25_' + cast, cast, story('%s_ears_flared' % cast, t=0.1 + 0.05 * (g - 1672))[1], (x0, y0, 0), loc, ppd=PPD25, canvas=cast14.CANVAS14_FRONT[cast])
            cur = (x0, y0)
        elif g < gs:                                 # keyed turn: the frontal card swings away (yaw -> -75 deg, fades), the side card swings in (+75 deg -> 0, fades in)
            u = ez((g - (gs - TURN)) / float(TURN), 'smooth'); pose = dict(story('%s_turn' % cast)[1]); pose['head_turn'] = lerp(0.0, 0.8, u); pose['t'] = 0.1 + 0.07 * (g - 1672)
            r = put('s25_f_' + cast, cast, pose, (x0, y0, 0), loc, ppd=PPD25, canvas=cast14.CANVAS14_FRONT[cast], yaw_extra=-75 * u, fade=1.0 - u)
            base = story('%s_flee' % cast)[1]; pp = cast14.cycle(cast, 0.0, 'run', -1, {k: v for k, v in base.items() if k not in ('phase', 'stride', 'gait', 'mirror', 'view')}, speed=spd); pp['t'] = 0.1
            r2 = put('s25_s_' + cast, cast, pp, (x0, y0, 0), loc, ppd=PPD25, mirror=True, yaw_extra=75 * (1 - u), fade=u)
            cur = (x0, y0)
        else:
            xr, ph = run_dist(cast, spd, g, gs); base = story('%s_flee' % cast)[1]
            pp = cast14.cycle(cast, ph, 'run', -1, {k: v for k, v in base.items() if k not in ('phase', 'stride', 'gait', 'mirror', 'view')}, speed=spd)
            pp['t'] = (g - gs) * 0.12; pp['dust'] = 0.5; pp['blink'] = cast14.blink_at(g, 96, BLINK_SEED[cast])
            cur = (x0 + RUND[0] * xr, y0 + RUND[1] * xr); r = put('s25_' + cast, cast, pp, (cur[0], cur[1], 0), loc, ppd=PPD25, mirror=True)
        rep[cast] = dict(head=screen(r['world'](r['anchors']['head'])), feet=screen(r['world'](r['anchors']['feet'])))
        # dust: cards that face the camera, centred on the elephant (card x = path x - elephant x); the crown in front of the feet, the trail behind
        yw = yaw_to(loc, (cur[0], cur[1]))
        cx, cy = cur if g >= gs else (x0, y0)
        for di, (dd, off) in enumerate(((d[0], -0.5), (d[1], 0.5))):
            p, n = dd.paint(g, cx - 7.5, cx + 7.5, 5.0, tag='%s%d' % (cast, di), light_k=1.0)
            if n and not os.environ.get('NODUST'):
                dx, dy = math.sin(yw) * off, -math.cos(yw) * off
                C.card('s25_dust_%s_%d' % (cast, di), p, -7.5, 0, 7.5, 5.0, (cx + dx, cy + dy, 0.0), yaw=yw, k=1.0)
    F.set_wire_push(1.0); F.set_bees(0.82, 0.22)
    F.STATE['wire_ob'].hide_render = True; F.STATE['wire_ob'].hide_viewport = True        # the wire passes 1 m from the lens and crosses the herd's faces: hidden in this shot
    for n in ('hive_3', 'bar_3', 'hive_4', 'bar_4', 'hive_5', 'bar_5'):          # s25b v2: the camera stands inside the fence in the gap of units 3/4: their hives are hidden (the hooks re-show them every call)
        o = bpy.data.objects.get(n)
        if o is not None: o.hide_render = True

# ------------------------------------------------------------------------------------------------ shot 26: dawn, the farmer proud by the fence (MORNING, crane down)
FARMER26 = (-1.7, 3.3, 0.0)
def cam26(g):
    u = mixu((g - 1760) / 82.0); return lerp3((-2.4, -5.8, 3.6), (-3.4, -0.9, 1.8), u), lerp3((-1.7, 5.2, 1.5), (-1.9, 4.3, 2.25), u), 22.0
def shot26(g, rep):
    loc, look, lens = cam26(g); cam_set(loc, look, lens)
    c, p = story('farmer_proud'); p = dict(p); s = math.sin(g * 0.11); p.update(blink=cast14.blink_at(g, 90, 11), head_roll=-5 + 1.4 * s, squash=[1.0, 1.02 + 0.006 * math.sin(g * 0.15)], gaze=[0.6 + 0.2 * math.sin(g * 0.05), -0.3])
    r = put('s26_farmer', c, p, FARMER26, loc, ppd=128, yaw_fixed=None)
    rep['farmer'] = dict(head=screen(r['world'](r['anchors']['head'])), feet=screen(r['world'](r['anchors']['feet'])))
    F.set_bees(-1)

# ------------------------------------------------------------------------------------------------ shot 27: the herd raids the uncle's field (NIGHT)
CAM27 = lambda g: (lerp3((-32.4, 0.2, 2.4), (-34.4, 0.4, 2.45), mixu((g - 1840) / 78.0)), lerp3((-33.4, 12.0, 1.55), (-34.4, 12.0, 1.55), mixu((g - 1840) / 78.0)), 20.0)
EAT = [('matriarch', -31.8, 9.8, -1, 0.9), ('elephant_b', -35.6, 8.9, -1, 0.85), ('elephant_c', -28.6, 8.2, -1, 0.9), ('elephant_d', -33.4, 13.4, -1, 0.8), ('calf', -30.2, 7.3, -1, 1.0)]
def eat_pos(cast, g):
    """the herd walks LEFT through the rows (rows run along y): a real walk, the phase advances with the distance (no foot slip)"""
    c, x0, y, face, spd = [e for e in EAT if e[0] == cast][0]; cyc = cast14.cycle_distance(cast, 'walk', spd) * MPD; k = g - 1840; dist = 0.0; ph = 0.0
    for q in range(k):
        v = 2.1 * (0.7 + 0.3 * math.sin(q * 0.07 + len(cast)) ** 2) / 30.0; dist += v; ph += v / cyc
    return x0 + face * dist, y, face, ph
def shot27(g, rep):
    loc, look, lens = CAM27(g); cam_set(loc, look, lens)
    for cast, x0, y, face, spd in EAT:
        xx, yy, fc, ph = eat_pos(cast, g); k = g - 1840
        tr = ('reach' if (k // 14 + len(cast)) % 2 == 0 else 'sniff')
        base = dict(expr='curious', trunk=tr, ear_flare=0.15, head_dip=2 + 3 * math.sin(k * 0.3 + len(cast)), mouth_open=0.35 if (k // 5 + len(cast)) % 2 == 0 else 0.0, blink=cast14.blink_at(g, 96, BLINK_SEED[cast]))
        pp = cast14.cycle(cast, ph, 'walk', fc, base, speed=spd); pp['t'] = k * 0.1; pp['expr'] = 'curious'
        r = put('s27_' + cast, cast, pp, (xx, yy, 0), loc, ppd=96, yaw_fixed=0.0, mirror=(fc < 0))
        rep[cast] = dict(head=screen(r['world'](r['anchors']['head'])), feet=screen(r['world'](r['anchors']['feet'])))
    F.set_uncle_field(min(1.0, max(0.0, (g - 1838) / 56.0)))      # stalks fall visibly over g 1840-1894

# ------------------------------------------------------------------------------------------------ shot 28: the sheepish uncle asks the farmer (MORNING)
def cam28(g):
    u = mixu((g - 1911) / 54.0); return lerp3((-2.6, -3.0, 1.40), (-2.2, -2.15, 1.38), u), lerp3((-2.2, 1.5, 0.75), (-2.2, 1.2, 0.95), u), 22.0
def shot28(g, rep):
    loc, look, lens = cam28(g); cam_set(loc, look, lens); k = g - 1911
    c, p = story('farmer_calm_smile' if False else 'farmer_proud'); p = dict(p); p.update(expr='smug', mouth='smile', arm_r='akimbo', arm_l='akimbo', yaw=0.3, gaze=[0.7, 0.0], head_roll=-4 + 1.5 * math.sin(k * 0.12), pitch=-0.2 + 0.05 * math.sin(k * 0.09), blink=cast14.blink_at(g, 90, 7), squash=[1.0, 1.0 + 0.01 * math.sin(k * 0.2)])
    rf = put('s28_farmer', c, p, (-3.1, 1.15, 0), loc, ppd=128, yaw_fixed=None); rep['farmer'] = dict(head=screen(rf['world'](rf['anchors']['head'])))
    c, p = story('uncle_ask_sheepish'); p = dict(p); sc_ = math.sin(k * 0.35)
    p.update(blink=cast14.blink_at(g, 80, 3), head_roll=6 + 2 * math.sin(k * 0.1), gaze=[-0.6 + 0.2 * math.sin(k * 0.07), 0.2], arm_l=dict(p['arm_l'], hand=[-0.4 + 0.07 * sc_, -0.3 + 0.05 * math.cos(k * 0.35)]), squash=[1.0, 1.0 + 0.01 * math.sin(k * 0.2 + 1)])
    ru = put('s28_uncle', c, p, (-1.35, 1.15, 0), loc, ppd=128, yaw_fixed=None); rep['uncle'] = dict(head=screen(ru['world'](ru['anchors']['head'])))
    F.set_uncle_field(1.0)

# ------------------------------------------------------------------------------------------------ shots 29 + 30: on the stool, the sting, the nose (MORNING)
HOOK = (-23.0, 5.0 - F.WIRE_OFF, 2.0)       # where the hive hangs on the uncle's wire
UNC = [-22.7, 4.45, 0.455]                  # card base = stool top (the stool is drawn by the pose: stool=1, so the person and the stool are one card: no sliding)
G_HANG = 1982; G_STING = ge(66.23); G_SW0 = ge(68.07); G_SW1 = ge(69.48)
def hang_pose(g):
    """uncle_stool_hang -> hand raises the hive to the wire (hang), then the sting reaction."""
    c, a = story('uncle_stool_hang'); a = dict(a, stool=1); a.pop('prop_r', None); k = g - B[29][0]
    a['arm_r'] = dict(a['arm_r'], hand=[lerp(0.66, 0.92, ez((g - 1962) / 20.0)), lerp(0.25, -0.30, ez((g - 1962) / 20.0))])
    a['t'] = k * 0.1
    return c, a
def sting_pose(g):
    c, a = story('uncle_stung_start'); a = dict(a, stool=1); return c, a
def pose29(g):
    k = g - B[29][0]
    if g < G_STING: c, p = hang_pose(g)
    else:
        c, p0 = hang_pose(G_STING - 1); c, p1 = sting_pose(g); u = ez((g - G_STING) / 5.0)
        p = cast14.lerp_pose(c, p0, p1, u); p['stool'] = 1
        p['nose_swell'] = lerp(0.0, 0.07, ez((g - G_STING) / 6.0)) + 0.05 * ez((g - G_STING) / 40.0)
        p['t'] = k * 0.1; p['squash'] = [1.0, 1.02 + 0.03 * math.sin((g - G_STING) * 1.3) * math.exp(-(g - G_STING) / 9.0)]
    p['blink'] = cast14.blink_at(g, 70, 5) if g < G_STING else 0
    return c, p
def cam29(g):
    u = mixu((g - 1962) / 70.0); return lerp3((-21.5, 0.35, 1.75), (-22.1, 1.45, 1.95), u), lerp3((-22.9, 3.9, 2.05), (-22.8, 3.8, 2.05), u), 22.0
def fix_unc():
    """place the stool card so that the raised hand (final hang pose) is exactly under the hook of the uncle's wire"""
    c, p = hang_pose(1982); loc = (-21.5, 0.35, 1.75)
    r = put('fix', c, p, (UNC[0], UNC[1], UNC[2]), loc, ppd=64, canvas=cast14.CANVAS14_STOOL['uncle14'], yaw_fixed=0.0, mirror=True, anchor_ground=('hand_r', (HOOK[0], HOOK[1] - 0.40)), shadow=False)
    UNC[0], UNC[1] = r['mark'].x, r['mark'].y; C.begin_frame(); print('UNC', UNC, flush=True)
def pin_hive(hand_w, g=0):
    h = F.STATE['uhive']; h.hide_viewport = False; h.hide_render = False; h.rotation_euler = (0, 0, 0)
    u = ez((g - G_STING) / 4.0, 'lin') if g >= G_STING else 0.0          # the hand lets go: the hive hangs on its hook
    held = Vector((hand_w.x, hand_w.y + 0.40, hand_w.z - 0.02)); h.location = held.lerp(Vector(HOOK), u)
def bee_path(g):
    """bee darts from the hive entrance to the nose over G_STING-9 .. G_STING, then buzzes off up and away"""
    return None
def shot29(g, rep):
    loc, look, lens = cam29(g); cam_set(loc, look, lens); c, p = pose29(g)
    r = put('s29_uncle', c, p, UNC, loc, ppd=128, canvas=cast14.CANVAS14_STOOL['uncle14'], yaw_fixed=0.0, mirror=True, anchor_ground=None)
    hand = r['world'](r['anchors']['hand_r']); head = r['world'](r['anchors']['head'])
    F.set_uncle_hive(1.0); pin_hive(hand, g)
    # the bee
    if G_STING - 10 <= g <= G_STING + 26:
        ent = Vector((-22.75, 4.72, 1.55)); nose = head + Vector((-0.30, -0.10, -0.12))
        if g <= G_STING: u = (g - (G_STING - 10)) / 10.0; pos = ent.lerp(nose, ez(u, 'lin')) + Vector((0.12 * math.sin(u * 9), 0, 0.1 * math.sin(u * 7)))
        else: u = (g - G_STING) / 26.0; pos = nose + Vector((-0.9 * u * u * 3, -0.35 * u, 0.7 * u + 0.12 * math.sin(u * 14)))
        cb, pb = story('bee_fly'); pb = dict(pb); pb.update(size=0.55, t=g * 0.45, angle=-12 + 25 * math.sin(g * 0.5), blur=0.7)
        put('s29_bee', cb, pb, (pos.x, pos.y, pos.z - 0.30), loc, ppd=256, yaw_fixed=0.0, shadow=False, canvas=cast14.CANVAS14['bee'])
    rep['uncle'] = dict(head=screen(head), hand=screen(hand), feet=screen(r['world'](r['anchors']['feet'])))

def pose30(g):
    c, p = story('uncle_stung_close'); p = dict(p); p.pop('prop_r', None)
    k = g - 2032; u = ez((g - G_SW0) / float(G_SW1 - G_SW0), 'sine'); u = 1 - (1 - min(1.0, max(0.0, (g - G_SW0) / float(G_SW1 - G_SW0)))) ** 2   # ease-out
    base = lerp(0.11, 0.15, min(1.0, k / 13.0)) if g < G_SW0 else 0.15
    p['nose_swell'] = base + (1.0 - base) * u if g >= G_SW0 else base
    p['t'] = k * 0.09; p['blink'] = 0
    p['squash'] = [1.0, 1.0 + 0.012 * math.sin(k * 0.3)]; p['head_roll'] = p.get('head_roll', -4) + 1.6 * math.sin(k * 0.17)
    return c, p
CAM30N = lambda g: None
def shot30(g, rep):
    c, p = pose30(g); k = g - 2032; u = mixu(k / 72.0)
    Hz = UNC[2] + 1.58; dist = lerp(1.95, 1.72, u)
    loc = (UNC[0] - 0.28 + 0.07 * u, UNC[1] - dist, Hz - 0.35)
    look = [UNC[0] + 0.04, UNC[1], Hz - 0.9]
    r = put('s30_uncle', c, p, UNC, loc, ppd=256, canvas=(-2.1875, -4.0, 2.5, 0.125), yaw_fixed=0.0, mirror=True)
    head = r['world'](r['anchors']['head']); hand = r['world'](r['anchors']['hand_r'])
    for _ in range(5):
        cam_set(loc, tuple(look), 22.0); yy = screen(head)[1]; look[2] -= (yy - 280) * dist / 782.0
    cam_set(loc, tuple(look), 22.0)
    F.set_uncle_hive(1.0); pin_hive(hand, 9999)
    # nose tip estimate: lowest opaque pixel row of the sprite -> screen
    rep['uncle'] = dict(head=screen(head), hand=screen(hand), nose_swell=round(p['nose_swell'], 3))

# ------------------------------------------------------------------------------------------------ setup / CLI
def prepare(shot):
    PR = F.PRESETS; CM = F.CAMS
    if shot == 25: F.STATE.get('x', None); CM['field_night_wide'] = dict(loc=CAM25(1700)[0], look=CAM25(1700)[1], lens=22); PR['field_night_wide'] = dict(light='NIGHT', state='fs3', staging=[]); return 'field_night_wide', 'NIGHT'
    if shot == 26: F.STAND['s26_farmer'] = FARMER26; CM['fence_line'] = dict(loc=(-3.4, -0.9, 1.8), look=(-1.9, 4.3, 2.25), lens=22); PR['fence_line'] = dict(light='MORNING', state='fs3', wire_r=0.07, staging=[('hero', 's26_farmer')]); return 'fence_line', 'MORNING'
    if shot == 27: CM['uncle_field_morning'] = dict(loc=CAM27(1840)[0], look=CAM27(1840)[1], lens=20); PR['uncle_field_morning'] = dict(light='NIGHT', state='fs3,uf0', staging=[]); return 'uncle_field_morning', 'NIGHT'
    if shot == 28: return 'yard_two_shot', 'MORNING'
    if shot in (29, 30): PR['uncle_hang'] = dict(light='MORNING', state='fs3,uf1,uh1', staging=[]); return 'uncle_hang', 'MORNING'
SHOTFN = {25: shot25, 26: shot26, 27: shot27, 28: shot28, 29: shot29, 30: shot30}

def matte_wire():
    m = F.STATE['M']['wire']
    for n in m.node_tree.nodes:
        if n.type == 'MIX' and getattr(n, 'data_type', '') == 'RGBA': n.inputs[6].default_value = (0.50, 0.52, 0.56, 1); n.inputs[7].default_value = (0.40, 0.42, 0.47, 1)
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Roughness'].default_value = 0.75
            if 'Emission Strength' in n.inputs: n.inputs['Emission Strength'].default_value = 0.0
            if 'Emission Color' in n.inputs: n.inputs['Emission Color'].default_value = (0, 0, 0, 1)

def setup(shot, quality, samples=None, threads=2, scale=1.0):
    pr, light = prepare(shot)
    _gb = F.ImageFilter.GaussianBlur; F.ImageFilter.GaussianBlur = lambda r=2: _gb(12)      # soft path / grass edges in the ground mask (no hard-edged pale-green patch)
    A = F.build(pr, light); F.STATE['wire_r'] = 0.03; sc = bpy.context.scene; F.setup_render(sc, 'final')
    sc.cycles.samples = samples or 24; sc.cycles.transparent_max_bounces = 40; sc.render.threads = threads; sc.render.resolution_x = int(720 * scale); sc.render.resolution_y = int(1280 * scale)
    C.cam_make(); matte_wire(); F._update_fence(); bpy.context.view_layer.update()
    if shot == 27:                                  # radiate the destruction outward from the elephants (plants nearest the herd fall first)
        rs = np.random.RandomState(5); pts = np.array([(e[1], e[2]) for e in EAT])
        for p in F.STATE['uplants']:
            d = float(np.min(np.hypot(pts[:, 0] - p['loc'][0], pts[:, 1] - p['loc'][1]))); p['thr'] = float(np.clip(0.03 + 0.80 * (d / 14.0) ** 0.9 + rs.uniform(-0.05, 0.08), 0.03, 0.9))
        for fp in F.STATE['ufoot']:
            d = float(np.min(np.hypot(pts[:, 0] - fp['ob'].location.x, pts[:, 1] - fp['ob'].location.y))); fp['thr'] = float(np.clip(d / 14.0 * 0.8, 0.0, 0.7))
            if fp['ob'].location.y < 11.0: fp['thr'] = 9.0          # no pads / mud rings in the foreground
        for cn in F.STATE['ucans']: cn['ob'].hide_render = True; cn['ob'].hide_viewport = True; cn['brk'] = False
        d0 = None
    if shot == 25:
        C.cut_named(['posts_', 'roof'], [(0.3, 11.6, 3.5, 6.3, -1, 9)])
        for o in bpy.data.objects:
            if o.name.startswith('mz') and -2.0 < o.location.x < 14.0 and 5.5 < o.location.y < 14.0: o.hide_render = True; o.hide_viewport = True
    if shot == 27: C.cut_tree33()
    if shot in (29, 30): fix_unc()
    if shot in (29, 30):                            # the set's own stool is replaced by the stool drawn by the pose (one card: the uncle never slides on it)
        C.cut_stool()
    return A

def render_frame(shot, g, path):
    C.begin_frame(); rep = {}; SHOTFN[shot](g, rep); bpy.context.view_layer.update(); w, cpu = F.render(path)
    for f in os.listdir(C.SPR):
        if f.startswith('dust_') and ('_%d_' % os.getpid()) in f:
            try: os.remove(os.path.join(C.SPR, f))
            except OSError: pass
    return rep, w, cpu

def parse(spec):
    out = []
    for part in spec.split(','):
        a = [int(v) for v in part.split(':')]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else [a[0]]
    return out

if __name__ == '__main__':
    cmd = sys.argv[1]; shot = int(sys.argv[2])
    if cmd == 'render':
        gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]; out = sys.argv[4]; scale = float(sys.argv[5]); samples = int(sys.argv[6]); threads = int(sys.argv[7]) if len(sys.argv) > 7 else 2
        os.makedirs(out, exist_ok=True); todo = []
        for g in gs:
            png = os.path.join(out, 's%d_g_%04d.png' % (shot, g)); js = png[:-4] + '.json'
            if os.path.exists(png) and os.path.exists(js):
                m = json.load(open(js))
                if m.get('scale') == scale and m.get('samples') == samples: continue
            todo.append(g)
        print('shot %d: %d to render' % (shot, len(todo)), flush=True)
        if todo:
            setup(shot, 'final', samples, threads, scale)
            for g in todo:
                png = os.path.join(out, 's%d_g_%04d.png' % (shot, g)); rep, w, cpu = render_frame(shot, g, png)
                rep.update(wall=round(w, 1), cpu=round(cpu, 1), scale=scale, samples=samples); json.dump(rep, open(png[:-4] + '.json.tmp', 'w')); os.replace(png[:-4] + '.json.tmp', png[:-4] + '.json')
                print('shot %d g %d %.1f s wall %.1f cpu %s' % (shot, g, w, cpu, json.dumps({k: v for k, v in rep.items() if k not in ('wall', 'cpu', 'scale', 'samples')})), flush=True)
