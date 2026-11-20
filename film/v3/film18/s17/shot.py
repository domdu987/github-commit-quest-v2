#!/usr/bin/env python3
"""s17 (frames 1309-1387): reed bundles soaked from a jar are tied to the oxen's tails, oxen nose-first at the holes. NO lit tail (fire comes at 47.13 s = g1417). jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's17'; G0, G1 = 1309, 1387; H_IN, H_OUT = 6, 6
c = S.SHOTS[SHOT]['cam']; c['loc'] = (-22.0, 17.0, 1.8); c['look_at'] = (-27.0, 8.4, 2.9); c['lens'] = 19.0
C.motion(SHOT, push=0.05, slide=-60, moves=[dict(t=0.55, d=0.93, dur=7)])
_p0 = S.pose_at
def _sway(sh, t):
    p = _p0(sh, t); sw = 2.2 * math.sin(t * 15.0); p['loc'] = (p['loc'][0] + sw, p['loc'][1], p['loc'][2]); la = list(p['look_at']); la[0] += 0.7 * sw; p['look_at'] = tuple(la); return p
S.pose_at = _sway

R2.SKIP['s17'] = [(-22.0, 21.0, 3.0), (-14.0, 9.5, 2.5), (-30.0, 9.0, 2.5), (-44.0, 9.5, 2.5)]

def setup(ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name in ('jars', 'reeds'): ob.hide_render = True; ob.location.z = -200; ob.hide_viewport = True
    for ob_ in J.STATE.get('fg_objs', []): ob_.hide_render = True; ob_.scale = (0.0, 0.0, 0.0)
    cam = bpy.data.objects['cam']; bpy.context.view_layer.update()
    rb = J.prop_reed_bundle((0, 0, 0), None, scale=0.5, n=60, cd=3.0); mw = cam.matrix_world
    rb.parent = cam; rb.location = (-0.42, -0.78, -1.5); rb.rotation_euler = (1.4, 0.2, 0.3)
    emm = bpy.data.materials.new('reedglow'); emm.use_nodes = True; nt = emm.node_tree; nt.nodes.clear(); em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.8, 0.58, 0.2, 1); em.inputs['Strength'].default_value = 0.5
    o2 = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(em.outputs[0], o2.inputs[0])
    for i_ in range(len(rb.data.materials)):
        if 'cord' not in rb.data.materials[i_].name and 'red' not in rb.data.materials[i_].name.lower() and 'ink' not in rb.data.materials[i_].name: rb.data.materials[i_] = emm

HL = []
def frame(g, t, camloc, ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name.startswith(('rubble', 'dig')): ob.hide_render = True
    if not HL:
        for i, hx in enumerate(J.HOLE_X):
            d = bpy.data.lights.new('hl%d' % i, 'POINT'); d.color = J.FIRE; d.energy = 900.0; d.shadow_soft_size = 1.2; d.use_shadow = False
            o = bpy.data.objects.new('hl%d' % i, d); J.STATE['LIGHTS'].objects.link(o); o.location = (hx, 4.4, 1.9); o.visible_camera = False; HL.append(o)
    for i, hx in enumerate(J.HOLE_X):
        if -42 < hx < -10: C.put_puff((hx, 4.9, 2.0), 3.4, camloc, alpha=0.9, name='hg%d' % i, tone=(255, 150, 60))
    for ob in bpy.data.objects:
        if ob.name in ('rainstreaks', 'streaks', 'streak'): ob.hide_render = True
    XS = [-36.0, -31.4, -26.8, -22.2, -17.6, -13.0]
    obs = []
    for i, x in enumerate(XS):
        bob = 0.04 * abs(math.sin((g + i * 4) * math.pi / 6.0))
        obs.append(C.put_ox(i, (x, 8.4 + (0.8 if i % 2 else 0.0), bob), -90, 1.0, camloc, phase=0, flame=-1, state='dragon', view='three_quarter', gait='stand', theta=58, reed=True))
    # an old man bends and ties a reed bundle to the tail of ox 3 (his reed_tail_l anchor sits on the ox's tail tip), large enough for a phone
    C.tie_reeds(obs[3], 'dragon', 'three_quarter', 'stand', 0, 1.0, camloc, height=3.5, over={'lean': (42, 46, 50, 46)[(g // 3) % 4]})
    C.put_person(C.person('woman_carry_basket', {'lean': 4 + 4 * ((g // 4) % 2)}), (XS[4] + 3.2, 11.8, 0), camloc, 3.0, 'wm', lift=0.04 * abs(math.sin(g * 0.6)))
    C.put_person(C.person('tiandan_point', {'lean': (g // 6) % 2 * 3}), (XS[1] - 1.2, 11.6, 0), camloc, 3.0, 'td')

if __name__ == '__main__':
    KEEP = [(x, 11.0, 2.6) for x in (-37.0 + 4.6 * i + 3.3 for i in range(6))] + [(-19.0, 12.6, 2.5)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
