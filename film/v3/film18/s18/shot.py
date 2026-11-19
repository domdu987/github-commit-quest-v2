#!/usr/bin/env python3
"""s18 (frames 1388-1426): Tian Dan raises a torch; on "จุดไฟ" (47.13 s = g1417) the tails light in a ripple, nearest ox first (one every 2 frames).  NO tail flame before g1417.  jimo_in NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's18'; G0, G1 = 1388, 1426; H_IN, H_OUT = 6, 6; G_FIRE = 1417
C.motion(SHOT, push=0.07, slide=-25, moves=[dict(t=0.16, pan=6, dur=4), dict(t=0.34, pan=-6, dur=4), dict(t=0.52, d=0.93, dur=4), dict(t=0.74, d=0.94, dur=5)])
R2.SKIP['s18'] = [(-22.0, 21.0, 3.0), (-14.0, 9.5, 2.5), (-30.0, 9.0, 2.5), (-44.0, 9.5, 2.5)]
TORCH = []

def setup(ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name in ('jars', 'reeds'): ob.hide_render = True; ob.location.z = -200; ob.hide_viewport = True
    R2.dress(-52, -20, 13.0, 22.0, 10, 23, kinds=('basket', 'hay', 'rope', 'pot'), avoid=lambda x, y: False)
    d = bpy.data.lights.new('torchL', 'POINT'); d.color = J.FIRE; d.energy = 0.0; d.shadow_soft_size = 0.4; d.use_shadow = False
    o = bpy.data.objects.new('torchL', d); J.STATE['LIGHTS'].objects.link(o); o.visible_camera = False; TORCH.append(o)

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    marks = S.marks_for(SHOT)
    n = len(marks['ox'])
    for i, m in enumerate(marks['ox']):
        rank = n - 1 - i                                  # nearest to the lens (x -13.5) is index 5 -> rank 0
        lit_at = G_FIRE + 2 * rank
        fl = C.flame_for(g, i) if g >= lit_at else -1
        bob = 0.05 * abs(math.sin((g + i * 4) * math.pi / 6.0)) + (0.06 * abs(math.sin((g - lit_at) * 1.1)) if g >= lit_at else 0)   # a startled hop as the tail lights
        C.put_ox(i, (m[0], m[1], m[2] + bob), -90, 1.0, camloc, phase=0, flame=fl, state='dragon', view='three_quarter', gait='stand', theta=50, reed=True)
    m = (-13.0, 12.0)
    ff = -1 if g < G_FIRE - 4 else (g // 2) % 3
    meta = C.person('tiandan_raise_torch', {'fire_frame': ff, 'lean': -4 + (g // 5) % 2 * 3})
    C.put_person(meta, (m[0], m[1], 0), camloc, 3.0, 'td')
    TORCH[0].location = (m[0] + 0.9, m[1] + 0.2, 3.9); TORCH[0].data.energy = 0.0 if ff < 0 else 500.0 + 120 * ff

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
