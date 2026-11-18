#!/usr/bin/env python3
"""shot.py -- film 14 take s07: shots 7-10 (boss quote, nickname), g 403..764 (6 handle frames each side).
 7 g409..460  yard_two_shot DAY fs1: uncle bursts out laughing at the farmer holding a hive
 8 g461..563  yard_two_shot push-in on uncle: LIP-SYNC quote 1, pinches a bean-size gap
 9 g564..663  medium close on uncle: LIP-SYNC quote 2, arms akimbo -> taps his nose
10 g664..758  yard_crowd DUSK: the village laughs along; the kid bangs a pot
Mouth: uncle talks ONLY inside g 464..665 (narration 15.38-22.07 s); everybody else holds a shape.
usage: python3 shot.py stills <shot> a:b:step outdir | final <shot> a:b outdir [samples]; one location per process."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import lerp, lerp3, clamp, u_of, ez, story, cast14, F
import bpy

G7, G8, G9, G10, GE = 409, 461, 564, 664, 759
H = 6
RANGES = {7: (G7 - H, G8 - 1), 8: (G8, G9 - 1), 9: (G9, G10 - 1), 10: (G10, GE - 1 + H)}
PRESET = {7: 'yard_two_shot', 8: 'yard_two_shot', 9: 'yard_two_shot', 10: 'yard_crowd'}
LIGHT = {7: 'DAY', 8: 'DAY', 9: 'DAY', 10: 'DUSK'}
TALK = (C.g_of(15.38), C.g_of(22.07))           # 464..665
G_PINCH = C.g_of(17.41)                          # "ตัวเท่าเม็ดถั่ว"
G_NOSE = C.g_of(21.04)                           # "ต่อยจมูกข้า"
def blink(g, o, period=96): return cast14.blink_at(g, period, o)
def sway(g, k=1.0): return math.sin(g * 0.21) * k

U = (-1.4, 3.2, 0.0); FM = (-2.9, 3.4, 0.0)       # uncle / farmer: near the maize wall so the frame is filled by field and village, not sky

CUT = [(-12, 6, -8, 5.6, 2.2)]                   # clear ALL yard clutter (tubs, pumpkins, fowl, sacks, stools) in front of the maize wall
CAMS = {
 7: (((-2.3, -0.3, 1.3), (-2.1, 3.3, 1.05), 22), ((-2.2, 0.1, 1.3), (-2.1, 3.3, 1.1), 22)),
 8: (((-2.2, 0.1, 1.3), (-1.7, 3.3, 1.1), 22), ((-1.7, 1.2, 1.45), (-1.4, 3.3, 1.25), 22)),
 9: (((-1.9, 1.3, 1.5), (-1.4, 3.3, 1.35), 24), ((-1.6, 1.45, 1.5), (-1.4, 3.3, 1.4), 24)),
 10: (((-2.1, -1.9, 1.25), (-2.1, 3.2, 1.1), 22), ((-2.1, -1.3, 1.3), (-2.1, 3.2, 1.15), 22)),
}
def cam_of(shot, g):
    a, b = CAMS[shot]; g0, g1 = RANGES[shot]; x = (g - g0) / float(g1 - g0)
    u = 0.3 * ez(x) + 0.7 * x
    return lerp3(a[0], b[0], u), lerp3(a[1], b[1], u), lerp(a[2], b[2], u)

def talk(p, g):
    if TALK[0] <= g <= TALK[1]: p['mouth'] = cast14.talk_mouth(g, 1.0)
    return p

def laugh(name, g, ph, k=1.0):
    c, p = story(name); p['t'] = 0.3 + (g + ph) / 30.0
    p['lean'] = p.get('lean', 0) + 2.2 * k * math.sin((g + ph) * 0.62)
    p['head_roll'] = p.get('head_roll', 0) + 3.0 * k * math.sin((g + ph) * 0.47)
    sq = 1.0 + 0.018 * k * math.sin((g + ph) * 0.62 + 1.2); p['squash'] = (1.0 / sq, sq)
    p['blink'] = blink(g, ph + 10, 70)
    return c, p

def pointy(p, look=0.9):
    p['arm_r'] = dict(hand=(0.9, 0.05), shape='point', bend=-0.5, stretch=1.3)
    p['arm_l'] = dict(hand=(-0.25, 0.75), bend=0.9)
    p['gaze'] = (look, 0.05); p['yaw'] = 0.5; p['mouth'] = 'talk_b'
    return p

def farmer_hold(g):
    c, p = story('farmer_hang_hive'); p['arm_r'] = dict(hand=(0.62, 0.7), bend=0.5, stretch=1.0, layer='front')
    p['prop_r'] = dict(type='tophive', scale=0.85); p['expr'] = 'worried'; p['mouth'] = 'smile'; p['gaze'] = (0.9, 0.0)
    p['lean'] = 2 + 0.8 * sway(g); p['t'] = g / 30.0; p['blink'] = blink(g, 30); p['yaw'] = -0.35
    return c, p

def uncle_pose(shot, g):
    if shot == 7:
        c, p = laugh('uncle_laugh_big', g, 0, 1.4)
    elif shot == 8:
        c, p = story('uncle_point_mock'); p['t'] = g / 30.0; p['blink'] = blink(g, 12)
        pn = u_of(g, G_PINCH - 12, G_PINCH - 2) * (1 - u_of(g, G_PINCH + 22, G_PINCH + 34))
        if pn > 0:           # hand up in front of the face, index up: the bean-size gap
            p['arm_r'] = dict(hand=(lerp(1.08, 0.62, pn), lerp(0.12, -0.35, pn)), shape='point', bend=lerp(-0.5, 0.6, pn), stretch=lerp(1.3, 1.0, pn))
        p['head_roll'] = p.get('head_roll', 0) + 2 * sway(g)
        p = talk(p, g)
    elif shot == 9:
        c, p = story('uncle_arms_akimbo'); p['t'] = g / 30.0; p['blink'] = blink(g, 40)
        tp = u_of(g, G_NOSE - 10, G_NOSE)
        p['lean'] = -4 * u_of(g, 566, 590) - 3 * tp; p['squash'] = (1.0, 1.0 + 0.02 * u_of(g, 566, 590))
        p['expr'] = 'smug'
        if tp > 0:           # taps his own nose with the pointing finger
            tap = 0.04 * sway(g * 2.2) * tp
            p['arm_r'] = dict(hand=(lerp(0.5, 0.18, tp), lerp(0.6, -0.12, tp) + tap), shape='point', bend=lerp(0.2, 0.8, tp), stretch=lerp(1.0, 0.9, tp))
        p = talk(p, g)
    else:
        c, p = laugh('uncle_laugh_big', g, 5, 1.0)
        p['yaw'] = 0.0
    return c, p

def frame(T, shot, g):
    loc, look, lens = cam_of(shot, g); T.set_cam(loc, look, lens)
    T.clear(); rep = {}; S = F.STAND
    F.set_fence_stage(1 if shot < 10 else 3)
    ppd = {7: 160, 8: 192, 9: 256, 10: 160}[shot]
    if shot in (7, 8):
        c, p = farmer_hold(g); rep['farmer'] = T.put('farmer', c, p, FM, ppd=ppd, canvas=cast14.CANVAS14[c])
        c, p = uncle_pose(shot, g); rep['uncle'] = T.put('uncle', c, p, U, ppd=ppd, canvas=cast14.CANVAS14[c], mirror=(shot == 7))
    elif shot == 9:
        c, p = uncle_pose(shot, g); rep['uncle'] = T.put('uncle', c, p, U, ppd=ppd, canvas=cast14.CANVAS14[c])
    else:
        F.set_crowd_props(0)
        # a laughing crowd round the uncle, everyone looks / points toward the farmer (screen-left, mirrored cards)
        c, p = uncle_pose(10, g); p = pointy(p); p['expr'] = 'laughing'
        rep['uncle'] = T.put('uncle', c, p, (-1.6, 3.0, 0), ppd=ppd, canvas=cast14.CANVAS14[c], mirror=True)
        for tag, nm, mk, ph, pt in (('old', 'villager_oldman_laugh', (-3.3, 3.5, 0), 3, False), ('woman', 'villager_woman_laugh', (-2.5, 2.4, 0), 0, True),
                                    ('woman2', 'villager_woman_laugh', (-0.7, 3.6, 0), 9, True), ('youth', 'villager_youth_point_laugh', (-0.2, 2.5, 0), 11, True)):
            c, p = laugh(nm, g, ph)
            if pt: p = pointy(p)
            p['gaze'] = (0.9, 0.05)
            rep[tag] = T.put(tag, c, p, mk, ppd=ppd, canvas=cast14.CANVAS14[c], mirror=True)
        c, p = story('villager_kid_bang_pot'); p['t'] = g / 30.0 * 2; p['lean'] = 2 * math.sin(g * 0.9); p['blink'] = blink(g, 20, 70); p['gaze'] = (0.9, 0.0)
        rep['kid'] = T.put('kid', c, p, (-1.0, 2.2, 0), ppd=ppd, canvas=cast14.CANVAS14[c], mirror=True)
    F.set_wire_push(-1.0); bpy.context.view_layer.update(); F.set_bees(-1.0)
    return rep

def report(T, shot, g, rep):
    heads = {k: T.head_screen(v) for k, v in rep.items()}
    return dict(shot=shot, g=g, cam=[round(x, 2) for x in T.cam.location], heads={k: [h[0][1], h[1][1]] for k, h in heads.items()}, mouth_window=TALK[0] <= g <= TALK[1])

if __name__ == '__main__':
    cmd = sys.argv[1]; shot = int(sys.argv[2]); a, b, *st = (sys.argv[3] + ':1').split(':'); out = sys.argv[4]
    os.makedirs(out, exist_ok=True); q = 'preview' if cmd == 'stills' else 'final'
    samples = int(sys.argv[5]) if len(sys.argv) > 5 else None
    T = C.Take(os.path.join(HERE, 'work'), PRESET[shot], LIGHT[shot], quality=q, samples=samples, dress=False, cut=CUT)
    for g in range(int(a), int(b) + 1, int(st[0]) if st else 1):
        png = os.path.join(out, 'g_%04d.png' % g)
        if cmd == 'final' and os.path.exists(png) and os.path.exists(png[:-4] + '.json'): continue
        rep = frame(T, shot, g); r = report(T, shot, g, rep)
        w, cpu = T.render(png); r.update(wall=round(w, 1), cpu=round(cpu, 1)); json.dump(r, open(png[:-4] + '.json', 'w'))
        print(json.dumps(r), flush=True)
