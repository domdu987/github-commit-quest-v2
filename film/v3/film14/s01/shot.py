#!/usr/bin/env python3
"""shot.py -- film 14 take s01: shots 1-3 (hook), g 0..180 + 6 out-handle frames g 181..186.
 1 g  0..65   hook_close DAY: farmer on the ladder hangs his first hive, villagers laugh in front
 2 g 66..122  yard_crowd DAY: reverse, the laughing villagers point at the fence, slow push
 3 g123..186  fence_line DAY fs1: farmer proud by the one hive, sweeps his hand to the hills on "ไล่ช้างได้ทั้งฝูง"
usage: python3 shot.py stills <shot> a:b:step outdir [scale samples]   |   python3 shot.py final <shot> a:b outdir [samples]
One location per process."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import lerp, lerp3, clamp, u_of, ez, story, cast14, F
import bpy
from mathutils import Vector

G1, G2, G3, GE = 66, 123, 181, 187           # shot starts, end (exclusive, incl. 6 handle frames)
RANGES = {1: (0, G2 - 1 - (G2 - G1)), 2: (G1, G2 - 1), 3: (G2, GE - 1)}
RANGES = {1: (0, G1 - 1), 2: (G1, G2 - 1), 3: (G2, GE - 1)}
PRESET = {1: 'hook_close', 2: 'yard_crowd', 3: 'fence_line'}
LIGHT = 'DAY'
G_HANG = 44                                  # shot 1: the hive is let go / hung (fence stage 0 -> 1)

def blink(g, offs, period=96):
    return cast14.blink_at(g, period, offs)

# ------------------------------------------------------------------ cameras: (loc, look, lens) at t = 0 / 1
CAMS = {
 1: (((-3.2, -1.6, 1.35), (-5.3, 4.0, 1.7), 20), ((-5.6, 0.2, 1.35), (-6.0, 4.0, 1.9), 20)),
 2: (((-2.6, -4.8, 1.4), (-4.4, 2.0, 1.55), 22), ((-3.9, -3.0, 1.4), (-4.7, 2.0, 1.6), 22)),
 3: (((-9.9, 0.9, 1.45), (-5.0, 5.0, 1.75), 22), ((-8.9, 1.3, 1.5), (-4.8, 5.0, 1.9), 22)),
}
def cam_of(shot, g):
    a, b = CAMS[shot]; g0, g1 = RANGES[shot]; x = (g - g0) / float(g1 - g0)
    u = 0.3 * ez(x) + 0.7 * x
    return lerp3(a[0], b[0], u), lerp3(a[1], b[1], u), lerp(a[2], b[2], u)

# ------------------------------------------------------------------ poses
def sway(g, k=1.0): return math.sin(g * 0.21) * k

def pose_farmer1(g):
    c, p = story('farmer_hang_hive')
    up = u_of(g, 0, 30)                           # lifts the hive up to the hook
    p['arm_r'] = dict(p['arm_r'])
    p['lean'] = lerp(1.0, 3.0, up) + 0.6 * sway(g)
    p['t'] = g / 30.0; p['blink'] = blink(g, 20)
    if g >= G_HANG: p.pop('prop_r', None); p['arm_r'] = dict(hand=(0.9, -0.2), bend=-0.4, stretch=1.2)
    return c, p

def pose_laugh(name, g, ph, k=1.0):
    c, p = story(name); p['t'] = 0.3 + (g + ph) / 30.0
    p['lean'] = p.get('lean', 0) + 2.2 * k * math.sin((g + ph) * 0.62)
    p['head_roll'] = p.get('head_roll', 0) + 3.0 * k * math.sin((g + ph) * 0.47)
    sq = 1.0 + 0.018 * k * math.sin((g + ph) * 0.62 + 1.2); p['squash'] = (1.0 / sq, sq)
    p['blink'] = blink(g, ph + 10, 70)
    return c, p

class Run(C.Take):
    pass

def frame(T, shot, g):
    loc, look, lens = cam_of(shot, g); T.set_cam(loc, look, lens)
    T.clear(); rep = {}
    S = F.STAND
    if shot == 1:
        F.set_fence_stage(0 if g < G_HANG else 1)
        c, p = pose_farmer1(g); rep['farmer'] = T.put('farmer', c, p, S['hero_ladder'], ppd=128, canvas=cast14.CANVAS14['farmer14'])
        for tag, nm, mk, ph in (('woman', 'villager_woman_laugh', (-4.6, 2.4, 0), 0), ('kid', 'villager_kid_laugh_point', (-3.7, 2.9, 0), 7), ('old', 'villager_oldman_laugh', (-7.3, 2.4, 0), 3), ('youth', 'villager_youth_point_laugh', (-8.3, 1.7, 0), 11)):
            c, p = pose_laugh(nm, g, ph); rep[tag] = T.put(tag, c, p, mk, ppd=160, canvas=cast14.CANVAS14[c])
    if shot == 2:
        F.set_fence_stage(1)
        for tag, nm, mk, ph, mir in (('old', 'villager_oldman_laugh', (-5.6, 1.0, 0), 3, False), ('woman', 'villager_woman_laugh', (-4.3, 0.2, 0), 0, False),
                                     ('youth', 'villager_youth_point_laugh', (-2.9, 0.9, 0), 11, True), ('kid', 'villager_kid_laugh_point', (-3.6, 1.8, 0), 7, True)):
            c, p = pose_laugh(nm, g, ph); rep[tag] = T.put(tag, c, p, mk, ppd=160, mirror=mir, canvas=cast14.CANVAS14[c])
    if shot == 3:
        F.set_fence_stage(1)
        a = story('farmer_calm_smile')[1]; b = story('farmer_proud')[1]; d = story('farmer_boast')[1]
        a.pop('prop_r', None); a['arm_r'] = dict(hand=(0.4, 1.0), bend=0.3)
        u1 = u_of(g, 123, 140); u2 = u_of(g, 148, 164)
        p = cast14.lerp_pose('farmer14', a, b, u1); p = cast14.lerp_pose('farmer14', p, d, u2)
        sw = u_of(g, 160, 181)
        p['t'] = g / 30.0; p['blink'] = blink(g, 150); p['lean'] = p.get('lean', 0) + 1.2 * sway(g)
        if u2 > 0.5: p['arm_r'] = dict(hand=(lerp(0.95, 1.12, sw), lerp(0.05, -0.28, sw)), shape='point', bend=-0.5, stretch=1.3)
        rep['farmer'] = T.put('farmer', 'farmer14', p, F.STAND['hero_hive'], ppd=192, canvas=cast14.CANVAS14['farmer14'])
    F.set_wire_push(-1.0)
    bpy.context.view_layer.update(); F.set_bees(-1.0)
    return rep

def report(T, shot, g, rep):
    heads = {k: T.head_screen(v) for k, v in rep.items()}
    return dict(shot=shot, g=g, cam=[round(x, 2) for x in T.cam.location], heads={k: [h[0][1], h[1][1]] for k, h in heads.items()})

if __name__ == '__main__':
    cmd = sys.argv[1]; shot = int(sys.argv[2]); a, b, *st = (sys.argv[3] + ':1').split(':'); out = sys.argv[4]
    os.makedirs(out, exist_ok=True)
    q = 'preview' if cmd == 'stills' else 'final'
    samples = int(sys.argv[5]) if len(sys.argv) > 5 else None
    T = C.Take(os.path.join(HERE, 'work'), PRESET[shot], LIGHT, quality=q, samples=samples)
    for g in range(int(a), int(b) + 1, int(st[0]) if st else 1):
        png = os.path.join(out, 'g_%04d.png' % g)
        if cmd == 'final' and os.path.exists(png) and os.path.exists(png[:-4] + '.json'): continue
        rep = frame(T, shot, g); r = report(T, shot, g, rep)
        w, cpu = T.render(png); r.update(wall=round(w, 1), cpu=round(cpu, 1)); json.dump(r, open(png[:-4] + '.json', 'w'))
        print(json.dumps(r), flush=True)
