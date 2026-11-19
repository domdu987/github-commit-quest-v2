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
 7: (((-2.3, -0.3, 1.3), (-2.15, 3.3, 1.6), 22), ((-2.2, 0.1, 1.3), (-2.1, 3.3, 1.65), 22)),
 8: (((-2.2, 0.1, 1.3), (-2.0, 3.3, 1.45), 22), ((-1.9, 1.1, 1.45), (-2.0, 3.3, 1.65), 22)),
 9: (((-1.9, 1.3, 1.5), (-1.4, 3.3, 1.75), 24), ((-1.6, 1.45, 1.5), (-1.4, 3.3, 1.8), 24)),
 10: (((-2.1, 0.0, 1.2), (-2.1, 3.2, 1.1), 20.5), ((-2.1, 0.25, 1.2), (-2.1, 3.2, 1.15), 20.5)),
}
def cam_of(shot, g):
    a, b = CAMS[shot]; g0, g1 = RANGES[shot]; x = (g - g0) / float(g1 - g0)
    u = 0.3 * ez(x) + 0.7 * x
    return lerp3(a[0], b[0], u), lerp3(a[1], b[1], u), lerp(a[2], b[2], u)

import puppet
def solve_tip(cast, pose, key, target, it=5):
    """move the arm's hand target so that the index fingertip (prop_tip) lands on `target` (puppet-local D); pose must not be mirrored."""
    pose = dict(pose); arm = dict(pose[key]); h = list(arm['hand'])
    tipkey = 'prop_tip_r' if key == 'arm_r' else 'prop_tip_l'
    for _ in range(it):
        arm['hand'] = tuple(h); pose[key] = arm
        t = puppet.figure(cast, pose, 'sv')['anchors'][tipkey]
        h[0] += target[0] - t[0]; h[1] += target[1] - t[1]
    arm['hand'] = tuple(h); return arm

def pinch_overlay(h, k=1.0):
    """a big readable pinch: thumb and index make a C that nearly closes on a bean-size gap (puppet-local D, ink #3a2832)."""
    x, y = h; r = 0.30 * k
    return ('<g stroke="#3a2832" stroke-width="%.3f" fill="#f1d6c4" stroke-linecap="round" stroke-linejoin="round">'
            '<circle cx="%.3f" cy="%.3f" r="%.3f"/>'
            '<path d="M %.3f %.3f Q %.3f %.3f %.3f %.3f" fill="none"/><path d="M %.3f %.3f Q %.3f %.3f %.3f %.3f" fill="none"/></g>'
            '<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="#c9a24a" stroke="#3a2832" stroke-width="0.012"/>'
            % (0.07 * k, x, y, 0.17 * k,
               x + 0.08 * k, y - 0.08 * k, x + 0.30 * k, y - 0.30 * k, x + 0.52 * k, y - 0.17 * k,
               x + 0.10 * k, y + 0.04 * k, x + 0.38 * k, y + 0.10 * k, x + 0.52 * k, y - 0.07 * k,
               x + 0.525 * k, y - 0.12 * k, 0.045 * k, 0.06 * k))

def finger_overlay(hand, tip, ext, tapping=False):
    """the pointing hand drawn OVER the face (the puppet's head covers its own arm): a fat index finger from the hand to the nose tip, a nose bump, tap marks."""
    k = '#3a2832'; x0, y0 = hand; x1, y1 = tip
    o = ('<ellipse cx="0.045" cy="0.075" rx="0.065" ry="0.05" fill="#d99a86" stroke="%s" stroke-width="0.022"/>' % k)   # the nose bump
    o += ('<g stroke-linecap="round"><line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="0.17"/>'
          '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="#f1d6c4" stroke-width="0.115"/></g>' % (x0, y0, x1, y1, k, x0, y0, x1, y1))
    o += '<circle cx="%.3f" cy="%.3f" r="0.12" fill="#f1d6c4" stroke="%s" stroke-width="0.045"/>' % (x0, y0, k)
    if tapping:
        o += ('<g stroke="%s" stroke-width="0.03" fill="none" stroke-linecap="round"><path d="M %.3f %.3f q -0.05 -0.03 -0.04 -0.10"/><path d="M %.3f %.3f q 0.05 -0.03 0.04 -0.10"/></g>'
              % (k, x1 - 0.05, y1 - 0.09, x1 + 0.09, y1 - 0.09))
    return o

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
    p['lean'] = 2 + 0.8 * sway(g); p['t'] = g / 30.0; p['blink'] = blink(g, 30); p['yaw'] = 0.4
    return c, p

NOSE = (0.045, 0.05)          # nose tip, puppet-local D (uncle, yaw 0.2)
def uncle_pose(shot, g):
    ov = None
    if shot == 7:
        c, p = laugh('uncle_laugh_big', g, 0, 1.4)
    elif shot == 8:
        # unmirrored pose; the CARD is flipped so the pointing arm aims at the farmer on screen-left
        c, p = story('uncle_point_mock'); p['t'] = g / 30.0; p['blink'] = blink(g, 12)
        pn = u_of(g, 513, 523) * (1 - u_of(g, 546, 554))
        p['head_roll'] = p.get('head_roll', 0) + 2 * sway(g)
        if pn > 0:
            hp = (lerp(1.08, 0.78, pn), lerp(0.12, -0.18, pn))
            p['arm_r'] = dict(hand=hp, shape='ball', bend=lerp(-0.5, 0.2, pn), stretch=lerp(1.3, 1.0, pn))
            if pn > 0.55: ov = pinch_overlay(hp, 1.3 + 0.2 * pn)
        else:
            p['arm_r'] = dict(hand=(1.08, 0.12 + 0.03 * sway(g)), shape='point', bend=-0.5, stretch=1.3)
        p = talk(p, g)
    elif shot == 9:
        c, p = story('uncle_arms_akimbo'); p['t'] = g / 30.0; p['blink'] = blink(g, 40)
        up = u_of(g, 606, 626) * (1 - u_of(g, 650, 676))          # hand rises; finger reaches the nose by g630, holds to ~g645, relaxes
        fing = u_of(g, 618, 630) * (1 - u_of(g, 647, 656))
        chest = u_of(g, 566, 600)
        p['lean'] = -5 * chest; p['pitch'] = -0.45 * chest - 0.15; p['squash'] = (1.0, 1.0 + 0.035 * chest)
        p['expr'] = 'smug'
        if up > 0:
            hp = (lerp(0.5, 0.30, up), lerp(0.9, 0.52, up))
            p['arm_r'] = dict(hand=hp, shape='ball', bend=lerp(0.2, 0.9, up), stretch=1.0, layer='front')
            tap = 0.02 * math.sin((g - 630) * 0.95) * u_of(g, 630, 633) * (1 - u_of(g, 645, 648))
            tip = (lerp(hp[0], NOSE[0], fing), lerp(hp[1], NOSE[1] + tap, fing))
            ov = finger_overlay(hp, tip, fing, tapping=(631 <= g <= 645 and math.sin((g - 630) * 0.95) > 0.55))
        p = talk(p, g)
    else:
        c, p = laugh('uncle_laugh_big', g, 5, 1.0); p['yaw'] = 0.0
    return c, p, ov

def frame(T, shot, g):
    loc, look, lens = cam_of(shot, g); T.set_cam(loc, look, lens)
    T.clear(); rep = {}; S = F.STAND
    F.set_fence_stage(1 if shot < 10 else 3)
    ppd = {7: 160, 8: 224, 9: 256, 10: 224}[shot]
    if shot in (7, 8):
        c, p = farmer_hold(g); rep['farmer'] = T.put('farmer', c, p, FM, ppd=ppd, canvas=cast14.CANVAS14[c])
        c, p, ov = uncle_pose(shot, g)
        rep['uncle'] = T.put('uncle', c, p, U, ppd=ppd, canvas=cast14.CANVAS14[c], mirror=(shot == 7), flip=(shot == 8), overlay=ov)
    elif shot == 9:
        c, p, ov = uncle_pose(shot, g); rep['uncle'] = T.put('uncle', c, p, U, ppd=ppd, canvas=cast14.CANVAS14[c], overlay=ov)
    else:
        F.set_crowd_props(0)
        # the farmer is the TARGET: eyes open, embarrassed / stiff smile, holding his hive box; the village faces him, points and laughs
        c, p = farmer_hold(g); p['expr'] = 'worried'; p['mouth'] = 'smile'; p['yaw'] = 0.4; p['gaze'] = (0.9, 0.0); p['lean'] = 1 + 0.8 * sway(g)
        rep['farmer'] = T.put('farmer', c, p, (-3.05, 3.3, 0), ppd=ppd, canvas=cast14.CANVAS14[c])
        # uncle + old man: flipped cards (the pointing arm is the screen-left one), index finger out, held through the shot, laughing
        c, p = story('uncle_point_mock'); p['t'] = g / 30.0; p['blink'] = blink(g, 12); p['expr'] = 'laughing'; p['mouth'] = 'talk_b'
        p['arm_r'] = dict(hand=(1.08, 0.12 + 0.03 * sway(g)), shape='point', bend=-0.5, stretch=1.3); p['lean'] = p.get('lean', 0) + 2.0 * math.sin(g * 0.55); p['gaze'] = (0.9, 0.05)
        rep['uncle'] = T.put('uncle', c, p, (-2.25, 3.2, 0), ppd=ppd, canvas=cast14.CANVAS14[c], flip=True)
        c, p = laugh('villager_oldman_laugh', g, 3); p['expr'] = 'laughing'; p['gaze'] = (0.9, 0.05); p['yaw'] = 0.5
        p['arm_r'] = dict(hand=(0.95 + 0.03 * sway(g), 0.1), shape='point', bend=-0.5, stretch=1.3); p['arm_l'] = dict(hand=(-0.3, 0.8), bend=0.9)
        p.pop('prop_r', None)
        rep['old'] = T.put('old', c, p, (-1.55, 3.7, 0), ppd=ppd, canvas=cast14.CANVAS14[c], flip=True)
        # kid: spoon (stick) in the right hand, pot in the left; bangs in bursts of about 3 hits
        c, p = story('villager_kid_bang_pot'); p['t'] = g / 30.0; p['blink'] = blink(g, 20, 70); p['gaze'] = (0.9, 0.0); p['expr'] = 'laughing'; p['mouth'] = 'talk_b'
        ph = (g - 664) % 36; active = ph < 22
        hit = (math.sin(ph * 0.62) ** 2) if active else 0.0              # about 3 beats per burst
        p['arm_r'] = dict(hand=(0.46, 0.42 - 0.34 * hit), bend=-0.5, stretch=1.1)
        p['prop_r'] = dict(type='spoon14', angle=205 + 40 * (1 - hit) - 20 * hit, scale=0.9); p['prop_l'] = dict(type='pot14', scale=1.0)
        p['lean'] = 2 * hit
        rep['kid'] = T.put('kid', c, p, (-0.95, 3.0, 0), ppd=ppd, canvas=cast14.CANVAS14[c], flip=True)
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
