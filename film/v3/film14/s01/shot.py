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
 1: (((-8.6, 1.0, 3.3), (-6.05, 4.6, 1.75), 26), ((-8.0, 1.8, 3.3), (-5.95, 4.6, 1.8), 26)),
 2: (((-3.3, 0.9, 2.3), (-6.0, 4.4, 1.1), 21), ((-3.7, 1.3, 2.3), (-6.1, 4.4, 1.15), 21)),
 3: (((-8.5, 1.1, 2.3), (-5.2, 4.6, 2.15), 20), ((-8.3, 1.2, 2.3), (-5.6, 4.6, 2.25), 20)),
}
def cam_of(shot, g):
    a, b = CAMS[shot]; g0, g1 = RANGES[shot]; x = (g - g0) / float(g1 - g0)
    u = 0.3 * ez(x) + 0.7 * x
    return lerp3(a[0], b[0], u), lerp3(a[1], b[1], u), lerp(a[2], b[2], u)

# ------------------------------------------------------------------ poses
def sway(g, k=1.0): return math.sin(g * 0.21) * k

HOLD = (-0.6, 0.0, 0.0)
G_REL0, G_REL1 = 30, 44
MARK1 = (-6.0, 3.85, 0.67)                   # soles on the ladder rung z 0.64 (rung y 3.845)                      # release: the bar travels from the hand onto the hook over these frames

def hand_xy(g):
    """arm_r hand param: carry (lift) -> hands stay on the bar while it travels to the hook (G_REL0..G_REL1) -> relax after the hook"""
    up = u_of(g, 0, 30); rel_ = u_of(g, G_REL0, G_REL1); rest = u_of(g, G_REL1 + 2, G_REL1 + 14)
    hx = lerp(0.72, 0.9, up); hy = lerp(0.30, -0.12, up)
    hx = lerp(hx, 0.70, rel_); hy = lerp(hy, 0.05, rel_)
    return lerp(hx, 0.9, rest), lerp(hy, -0.2, rest)

def pose_farmer1(g):
    c, p = story('farmer_hang_hive'); p.pop('prop_r', None)
    up = u_of(g, 0, 30); hx, hy = hand_xy(g)
    p['arm_r'] = dict(hand=(hx, hy), bend=-0.5, stretch=1.2, layer='front')
    p['lean'] = lerp(1.0, 3.0, up) + 0.6 * sway(g)
    p['t'] = g / 30.0; p['blink'] = blink(g, 20)
    return c, p

def hand_world(hx, hy):          # hand_r anchor of the card at MARK1 (affine fit of measured anchors)
    return (0.373 * hx + 0.055 * hy - 5.95, 0.0, -0.069 * hx - 0.488 * hy + 2.913 + (MARK1[2] - 1.35))

def carry_at(g):
    hx, hy = hand_xy(min(g, G_REL0)); hw = hand_world(hx, hy)
    return Vector((hw[0] + HOLD[0], MARK1[1] - 0.45 + 0.0, hw[2] + 0.12))

def hang_hive(g):
    """ONE hive: the set's own hive + bar, held at the hand until G_REL0, then tweened onto the hook (G_REL0..G_REL1); returns its centre for the bees"""
    h = F.STATE['hive'][1]; b = F.STATE['bar'][1]
    hook = F._pivot(1, -1.0, F.STATE['push_s0'])
    if g < G_REL0: P = carry_at(g) + Vector((0.04 * sway(g), 0, 0.02 * sway(g + 3)))
    elif g < G_REL1:
        u = u_of(g, G_REL0, G_REL1); P = carry_at(G_REL0).lerp(hook, u); P.z += 0.06 * math.sin(math.pi * u)
    else: P = hook.copy()
    h.location = P; b.location = P
    h.rotation_euler = (0.0, 0.0, F.UNITS[1]['yaw']); b.rotation_euler = h.rotation_euler
    b.scale = (1.0, 1.0, lerp(0.3, 1.0, u_of(g, G_REL0, G_REL1)))
    bpy.context.view_layer.update()
    return (P.x, P.y - 0.12, P.z - 0.45)

def rel(shot, d, r):
    """floor point d m ahead of / r m to the right of the shot's first camera (villagers stay put while the camera moves)"""
    loc, look, _ = CAMS[shot][0]; fx, fy = look[0] - loc[0], look[1] - loc[1]; n = math.hypot(fx, fy); fx, fy = fx / n, fy / n
    return (loc[0] + fx * d + fy * r, loc[1] + fy * d - fx * r, 0.0)

def hive_centre(g, fr):
    if fr is not None and g < G_HANG:
        a = fr['anchors']; k = 'hive_c_r' if 'hive_c_r' in a else 'hive_bottom_r'
        return tuple(fr['world'](a[k]))
    h = F.STATE['hive'][1]; m = h.matrix_world.translation
    return (m.x, m.y - 0.2, m.z)

def pose_laugh(name, g, ph, k=1.0, up=False):
    c, p = story(name); p['t'] = 0.3 + (g + ph) / 30.0
    p['lean'] = p.get('lean', 0) + 2.2 * k * math.sin((g + ph) * 0.62)
    p['head_roll'] = p.get('head_roll', 0) + 3.0 * k * math.sin((g + ph) * 0.47)
    sq = 1.0 + 0.018 * k * math.sin((g + ph) * 0.62 + 1.2); p['squash'] = (1.0 / sq, sq)
    p['blink'] = blink(g, ph + 10, 70)
    if up and 'arm_r' in p:
        p['arm_r'] = dict(p['arm_r']); p['arm_r']['hand'] = (0.52 + 0.04 * math.sin((g + ph) * 0.5), -0.52); p['arm_r']['shape'] = 'point'
        p['pitch'] = -0.5
    return c, p

class Run(C.Take):
    pass

def frame(T, shot, g):
    loc, look, lens = cam_of(shot, g); T.set_cam(loc, look, lens)
    T.clear(); rep = {}
    S = F.STAND
    if shot == 1:
        F.set_fence_stage(1)
        c, p = pose_farmer1(g); rep['farmer'] = T.put('farmer', c, p, MARK1, ppd=128, canvas=(-2.9, -5.0, 2.9, 0.125))
        for tag, nm, (d, r), ph, mir in (('woman', 'villager_woman_laugh', (6.6, 1.9), 0, True), ('kid', 'villager_kid_laugh_point', (5.4, 1.0), 7, True)):
            c, p = pose_laugh(nm, g, ph, up=True); rep[tag] = T.put(tag, c, p, rel(1, d, r), ppd=128, mirror=mir, canvas=cast14.CANVAS14[c])
    if shot == 2:
        F.set_fence_stage(1)
        c, p = pose_farmer1(80); p['t'] = g / 30.0; p['blink'] = blink(g, 20); p['lean'] = 3.0 + 0.6 * sway(g)
        p['arm_r'] = dict(hand=(0.95, -0.35), bend=-0.4, stretch=1.2); rep['farmer'] = T.put('farmer', c, p, MARK1, ppd=128, canvas=cast14.CANVAS14['farmer14'])
        for tag, nm, (d, r), ph, mir, up in (('old', 'villager_oldman_laugh', (6.6, -2.3), 3, False, False), ('woman', 'villager_woman_laugh', (6.4, 2.3), 0, True, False),
                                         ('youth', 'villager_youth_point_laugh', (5.2, 1.2), 11, True, True), ('kid', 'villager_kid_laugh_point', (5.2, -1.2), 7, False, True)):
            c, p = pose_laugh(nm, g, ph, up=up); rep[tag] = T.put(tag, c, p, rel(2, d, r), ppd=128, mirror=mir, canvas=cast14.CANVAS14[c])
    if shot == 3:
        F.set_fence_stage(1)
        a = story('farmer_calm_smile')[1]; b = story('farmer_proud')[1]; d = story('farmer_boast')[1]
        a.pop('prop_r', None); a['arm_r'] = dict(hand=(0.4, 1.0), bend=0.3)
        u1 = u_of(g, 123, 140); u2 = u_of(g, 148, 164)
        p = cast14.lerp_pose('farmer14', a, b, u1); p = cast14.lerp_pose('farmer14', p, d, u2)
        sw = u_of(g, 150, 178)
        p['t'] = g / 30.0; p['blink'] = blink(g, 150); p['lean'] = p.get('lean', 0) + 1.2 * sway(g)
        if g >= 146:
            # real sweep toward the peak (screen-left, card mirrored): 3 keyed hand poses tweened over 16 frames, then HELD (full arm up, pointing)
            K = [(0.45, 0.70), (0.85, 0.0), (0.95, -1.0)]; x = clamp((g - 148) / 16.0); seg = min(int(x * 2), 1); lu = ez(x * 2 - seg)
            hx = lerp(K[seg][0], K[seg + 1][0], lu); hy = lerp(K[seg][1], K[seg + 1][1], lu)
            if g > 168: hx += 0.03 * math.sin((g - 168) * 0.5); hy += 0.03 * math.sin((g - 168) * 0.37)
            p['arm_r'] = dict(hand=(hx, hy), shape='point' if x > 0.5 else 'open', bend=-0.3, stretch=1.35, layer='front')
            p['lean'] = p.get('lean', 0) - 3.0 * ez(x); p['pitch'] = lerp(p.get('pitch', -0.2), -0.5, ez(x))
        rep['farmer'] = T.put('farmer', 'farmer14', p, (-5.0, 3.3, 0.0), ppd=170, mirror=True, canvas=cast14.CANVAS14['farmer14'], contact=(0.55, 0.28))
    F.set_crowd_props(0)
    F.set_wire_push(-1.0)
    bpy.context.view_layer.update(); F.set_bees(-1.0)
    if shot == 1: T.bees(hang_hive(g), 9, g)
    else: T.bees(hive_centre(g, None), 7 if shot == 2 else 8, g, seed=5)
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
