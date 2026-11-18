#!/usr/bin/env python3
"""film 14 take s11: shots 11-14 (the count): day 1 one hive / day 2 ten hives / day 3 one wire through every hive / the whole ring on one wire.
g 759..1000 (+6 handle frames each side: 753..1006).  One shot per process (one location per process):
    python3 shot.py <shot 11|12|13|14> <a:b[:step]> <out_dir> [draft|final]
"""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, put, story, lerp, clamp, sm, blink_at, cast14, Vector, bpy
import numpy as np

GR = {11: (753, 820), 12: (821, 863), 13: (864, 929), 14: (930, 1006)}      # shot 11: 759..820 (+6 in), 12: 821..863, 13: 864..929, 14: 930..1000 (+6 out)
BOUND = {11: (759, 820), 12: (821, 863), 13: (864, 929), 14: (930, 1000)}

F.CAMS['p11'] = dict(loc=(-10.2, 0.9, 1.45), look=(-6.2, 4.8, 1.75), lens=22)
F.PRESETS['p11'] = dict(light='DAY', state='fs1', staging=[])
F.CAMS['p12'] = dict(loc=(-1.5, -12.5, 18.0), look=(-1.5, 15.0, -1.5), lens=20)
F.PRESETS['p12'] = dict(light='DAY', state='fs2', wire_r=0.12, staging=[])
F.CAMS['p13'] = dict(loc=(-9.7, 2.4, 1.2), look=(-5.2, 5.0, 1.8), lens=24)
F.PRESETS['p13'] = dict(light='DUSK', state='fs3,bees-1', staging=[])
F.CAMS['p14'] = dict(loc=(-1.5, -12.5, 18.0), look=(-1.5, 15.0, -1.5), lens=20)
F.PRESETS['p14'] = dict(light='DUSK', state='fs3', wire_r=0.12, staging=[])

def cam11(g):
    x = (g - 759) / 61.0                          # slow dolly in along the fence, a little rise
    return (lerp(-9.0, -7.9, x), lerp(1.0, 2.0, x), lerp(1.40, 1.55, x)), (lerp(-6.2, -5.9, x), 4.8, lerp(1.80, 1.95, x)), 22
def cam12(g):
    x = (g - 821) / 42.0                          # slow crane DOWN toward the ring, ten hives
    return (lerp(-3.0, -0.5, x), lerp(-14.5, -12.0, x), lerp(22.0, 16.5, x)), (lerp(-1.5, -1.5, x), 15.0, lerp(-1.5, -1.0, x)), 20
def cam13(g):
    x = (g - 864) / 65.0                          # dolly along the fence, the wire running away to the right
    return (lerp(-9.4, -8.2, x), lerp(2.6, 3.0, x), lerp(1.25, 1.40, x)), (lerp(-5.0, -3.6, x), 5.0, lerp(1.9, 2.0, x)), 24
def cam14(g):
    x = (g - 930) / 70.0                          # the camera RISES over the ring (and drifts back to take in all four sides)
    return (lerp(-1.5, -1.5, x), lerp(-12.5, -15.5, x), lerp(15.5, 24.0, x)), (-1.5, 15.0, lerp(-1.5, -2.5, x)), 20

# ---------------------------------------------------------------- the farmer on the ladder, tying the wire
LADDER_MARK = {}
def farmer_pose(g, shot):
    c, p = story('farmer_tie_wire'); p = dict(p)
    w = g * 0.55
    p['arm_r'] = dict(p['arm_r'], hand=(0.86 + 0.05 * math.sin(w), 0.0 + 0.06 * math.cos(w * 1.3)), bend=-0.3)       # twisting the wire
    p['lean'] = 3.0 + 1.5 * math.sin(g * 0.1); p['head_roll'] = -3 + 1.5 * math.sin(g * 0.07); p['blink'] = blink_at(g, 80, 11); p['t'] = g / 30.0
    p['expr'] = 'determined' if shot == 11 else 'happy'
    return c, p

def rod(a, b, r, mat, name='actor_stub'):
    a = Vector(a); b = Vector(b); d = b - a; L = d.length
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=r, depth=max(L, 1e-3), location=(a + b) / 2)
    o = bpy.context.active_object; o.name = name; o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler(); o.data.materials.append(mat); o.visible_shadow = False
    return o

STOOL = (-5.65, 4.2, 0.49)                       # the farmer's own stool (seat top z 0.49) just right of hive 1: he stands ON it, fixed for the whole shot (no sliding)
def farmer_on_stool(g, loc, shot):
    c, p = farmer_pose(g, shot)
    return put(c, p, STOOL, loc, ppd=128, mirror=True, contact=False)

# ---------------------------------------------------------------- shot 11 / 13: the ladder + hive 1
def build_hive(preset):
    def b():
        A = F.build(preset); cam = F.make_camera(F.CAMS[preset])
        if preset in ('p11', 'p13'): print('ladder cut', C.cut_region('props', [(-6.4, -5.6, 3.4, 4.9, 2.7)])); mb = C.G.MB('s_stool'); C.G.stool(mb, F.STATE['M'], (STOOL[0], STOOL[1], 0.0), 0.3); mb.finish()
        return dict(cam=cam)
    return b
def hive_pivot():
    u = F.UNITS[1]; return Vector((u['pos'][0], u['pos'][1] - F.WIRE_OFF, F.WIRE_Z))
def frame11(st, g):
    loc, look, lens = cam11(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(1); F.set_wire_push(-1)
    r = farmer_on_stool(g, loc, 11); hand = r['world']('hand_l')
    rod(hand, (hand.x - 0.1, hive_pivot().y, 2.0), 0.03, F.STATE['M']['wire'])
    return dict(cam=[round(v, 2) for v in loc], head=C.screen(r['world']('head')), top=C.screen(r['world']('head_top')), hand=[round(v, 2) for v in hand], feet=[round(v, 2) for v in r['world']('feet')])
def frame13(st, g):
    loc, look, lens = cam13(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(3); F.set_wire_push(-1)
    r = farmer_on_stool(g, loc, 13); hand = r['world']('hand_l')
    rod(hand, (hand.x - 0.1, hive_pivot().y, 2.0), 0.03, F.STATE['M']['wire'])
    return dict(cam=[round(v, 2) for v in loc], head=C.screen(r['world']('head')), top=C.screen(r['world']('head_top')), hand=[round(v, 2) for v in hand])

# ---------------------------------------------------------------- shot 12 / 14: the ring from above
def frame12(st, g):
    loc, look, lens = cam12(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(2); F.set_wire_push(-1)
    return dict(cam=[round(v, 2) for v in loc])
def wire_point(s):
    W = F.STATE['wire']; S = W['S']; base = W['base']; s = s % F.S_TOT
    i = int(np.searchsorted(S, s, side='right') - 1); i = max(0, min(i, len(S) - 2)); u = (s - S[i]) / max(S[i + 1] - S[i], 1e-9)
    return Vector(base[i]) * (1 - u) + Vector(base[i + 1]) * u
def frame14(st, g):
    """the whole ring, every hive on ONE wire: three warm beads of light run along the single wire round the ring (a pulse of 'current'), camera rising."""
    loc, look, lens = cam14(g); C.set_cam(st['cam'], loc, look, lens); F.set_fence_stage(3); F.set_wire_push(-1)
    for k in range(3):
        s = 3.0 + k * F.S_TOT / 3.0 + (g - 930) * 0.9
        for q, (dq, r) in enumerate(((0.0, 0.36), (-0.9, 0.24), (-1.7, 0.15))):                 # a bright head and a fading tail
            p = wire_point(s + dq); o = bpy.data.objects.new('actor_bead', bpy.data.meshes.new('bd'))
            bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=8, radius=r, location=p); b = bpy.context.active_object; b.name = 'actor_bead'
            b.data.materials.append(C.G.mat_emit('bead%d' % q, '#ffd27a', 9.0 - 2.5 * q)); b.visible_shadow = False; bpy.data.objects.remove(o)
    return dict(cam=[round(v, 2) for v in loc])

BUILD = {11: (build_hive('p11'), frame11), 12: (build_hive('p12'), frame12), 13: (build_hive('p13'), frame13), 14: (build_hive('p14'), frame14)}
if __name__ == '__main__':
    shot = int(sys.argv[1]); gs = [g for g in C.parse(sys.argv[2]) if GR[shot][0] <= g <= GR[shot][1]]; out = sys.argv[3]; q = sys.argv[4] if len(sys.argv) > 4 else 'draft'
    b, f = BUILD[shot]; C.run(b, f, out, gs, quality=q)
