#!/usr/bin/env python3
"""s19 (frames 1427-1514): oxen burst out of the holes (dust puffs), tails lit, gallop across the field; dark Qi soldiers behind; WHIP pan at the end.  jimo_out NIGHT.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's19'; G0, G1 = 1427, 1514; H_IN, H_OUT = 6, 6        # cut in, whip out
c = S.SHOTS[SHOT]['cam']; c['loc'] = (11.0, -22.0, 1.4); c['look_at'] = (30.0, -5.0, 9.0); c['lens'] = 18.0
C.motion(SHOT, push=0.06, slide=-35, moves=[dict(t=0.24, d=0.93, dur=4), dict(t=0.50, d=1.06, dur=4), dict(t=0.9, pan=-85, dur=6)])
_p0 = S.pose_at
def _tilt(sh, t):                                            # the whip lands on the herd: tilt down from the sky onto the field while the pan runs
    p = _p0(sh, t); k = min(1.0, max(0.0, (t - 0.88) / 0.08)); k = k * k * (3 - 2 * k)
    la = list(p['look_at']); la[2] = la[2] + (1.2 - la[2]) * k; p['look_at'] = tuple(la); return p
S.pose_at = _tilt
HX = [hx for hx in J.HOLE_X if hx > 0]
rnd = random.Random(19)
OX = []                                                      # (gs, hole x, lane jitter, scale)
for w in range(4):
    for k, hx in enumerate(HX):
        OX.append((G0 - 14 + 2 * k + 15 * w + rnd.randint(-2, 2), hx + rnd.uniform(-0.5, 0.5), rnd.uniform(-0.3, 0.3), rnd.uniform(0.95, 1.05)))
OX = OX[:22]
QI = [(G0 + 22 + 5 * k, HX[k % 6] + rnd.uniform(-0.8, 0.8)) for k in range(6)]
V_OX, V_QI = 15.0, 11.5

def setup(ctx):
    J.set_holes(12)
    M = J.STATE['M']
    try:                                                     # kill the set's dark dust squares: additive material strength -> 0
        for n in M['dust'].node_tree.nodes:
            for i in n.inputs:
                if i.name == 'Strength': i.default_value = 0.0
    except Exception as e: print('dust', e)
    for ob in bpy.data.objects:
        if ob.name.startswith('hglow'): ob.hide_render = True
    import bmesh                                             # drop the 'mist' halo quads (dark translucent squares at the breaches)
    for ob in [o for o in bpy.data.objects if o.type == 'MESH' and (o.name == 'halos' or o.name.startswith('rubble') or o.name.startswith('breach'))]:
        bm = bmesh.new(); bm.from_mesh(ob.data); mi = [i for i, m in enumerate(ob.data.materials) if m is not None and ('mist' in m.name or 'dust' in m.name)]
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in mi], context='FACES'); bm.to_mesh(ob.data); bm.free()

def frame(g, t, camloc, ctx):
    J.set_holes(12)
    for ob in bpy.data.objects:
        if ob.name.startswith('hglow'): ob.hide_render = True
    for j, (gs, hx, jit, sc) in enumerate(OX):
        if g < gs: continue
        y = 4.0 - V_OX * (g - gs) / 30.0
        if y < -150: continue
        pos = (hx + jit, y, 0.0); near = (V(pos) - camloc).length < 16
        ph = int((g - gs) * 12 / 30.0 + j) % 8
        C.put_ox(j, pos, -100, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='front_three_quarter' if (near and j % 3 == 0) else 'three_quarter', gait='gallop', theta=14 if (near and j % 3 == 0) else 30, reed=True, fcard=0.9)
    for j, (gs, x) in enumerate(QI):
        if g < gs: continue
        y = -5.5 - V_QI * (g - gs) / 30.0
        m = C.qi((g - gs) * 12 / 30.0 / 8.0 + j * 0.13, 1)
        C.put_person(m, (x, y, 0), camloc, 3.1, 'qi%d' % j, mirror=(j % 2 == 0), tint=(0.5, 0.5, 0.75), k=0.8)
    for k, hx in enumerate(HX):                              # dust puffs at the hole mouths, growing and fading after the first ox of the hole bursts out
        gs = min(o[0] for o in OX if abs(o[1] - hx) < 1.0); a = g - (gs + 8)
        for q in range(3):
            aq = a - 5 * q
            if aq < 0 or aq > 40: continue
            if os.environ.get('NOPUFF') != '1': C.put_puff((hx + (q - 1) * 1.6, -5.5 - 0.15 * aq, 0.8 + 0.07 * aq), 2.5 + 0.12 * aq, camloc, alpha=(0.55, 0.4, 0.25)[min(2, aq // 14)], name='pf%d_%d' % (k, q))

if __name__ == '__main__':
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:])
