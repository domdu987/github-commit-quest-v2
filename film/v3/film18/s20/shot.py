#!/usr/bin/env python3
"""s20 (frames 1515-1595): reveal A. The camera tracks ALONGSIDE the herd at herd speed: a lead ox in clean profile (35-50 % of frame height) with its flame trailing behind;
every ox runs the same way (-y toward the Yan camp), flames on the tail tips, sparks, tail lights.  jimo_out NIGHT.  Short whip-in.
python3 shot.py draft|final [first_g last_g] [out]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
SHOT = 's20'; G0, G1 = 1515, 1595; H_IN, H_OUT = 6, 6
V_OX = 11.0; XC = 20.0; Y0 = -46.0; DUR = 81 / 30.0
def pose(sh, t):
    """camera rides with the herd: y = Y0 - V*t*DUR; lateral distance 10.5 -> 9.2 (slow push), whip-in during the first 7 frames."""
    y = Y0 - V_OX * t * DUR; lat = 6.4 - 0.5 * min(1.0, max(0.0, t)) + 0.5 * math.sin(t * 25.0); w = max(0.0, 1.0 - (t * 81) / 7.0) ** 2
    return dict(loc=(XC, y, 1.6), look_at=(XC - lat, y + 0.2 + 30.0 * w, 0.1 + 0.1 * t), lens=19.0)
S.pose_at = pose
rnd = random.Random(20)
R2.POST['s20'] = lambda p: None
REL = [(-7.0, 1.0, 1.0, 0.0)]                                   # lead ox in pure profile (n = 0 of the lattice); all rows share the 9.6 D lattice so no flame meets another head
for row, dx in enumerate((-7.0, -11.8, -16.6)):
    for n in range(-2, 3):
        if row == 0 and n == 0: continue
        REL.append((dx + rnd.uniform(-0.3, 0.3), 1.0 + 9.6 * n + rnd.uniform(-0.4, 0.4), rnd.uniform(0.97, 1.03), 0.0))

def setup(ctx):
    J.set_holes(12)
    import bmesh
    ho = bpy.data.objects.get('halos')
    import numpy as np
    for nm in ('wood', 'posts'):
        wo = bpy.data.objects.get(nm)
        if wo is not None:
            me = wo.data; nv = len(me.vertices); co = np.empty(nv * 3, np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
            M = np.array(wo.matrix_world); w = co @ M[:3, :3].T + M[:3, 3]
            pi = np.empty(len(me.polygons) * 0, np.int32); nl = len(me.loops); lv = np.empty(nl, np.int32); me.loops.foreach_get('vertex_index', lv)
            ls = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get('loop_start', ls); lt = np.empty(len(me.polygons), np.int32); me.polygons.foreach_get('loop_total', lt)
            cx = np.add.reduceat(w[lv][:, 0], ls) / lt; cy = np.add.reduceat(w[lv][:, 1], ls) / lt; cz = np.add.reduceat(w[lv][:, 2], ls) / lt
            bad = np.flatnonzero((cy < -25) & (cy > -140) & (cx > 3) & (cx < 16) & (cz < 6))
            if len(bad):
                sink = np.zeros(nv, bool)
                for i in bad: sink[lv[ls[i]:ls[i] + lt[i]]] = True
                co2 = co.copy(); co2[sink, 2] -= 80.0; me.vertices.foreach_set('co', co2.reshape(-1)); me.update()
    if ho is not None:                                   # remove the halo quads of the road tripods / stakes in the field (glow stuck on the lead ox)
        bm = bmesh.new(); bm.from_mesh(ho.data); mw = ho.matrix_world
        bad = [f for f in bm.faces if (lambda c: c.y < -25 and abs(c.x) < 60 and c.y > -135)(mw @ f.calc_center_median())]
        bmesh.ops.delete(bm, geom=bad, context='FACES'); bm.to_mesh(ho.data); bm.free()
    import jimo_dress as _DG; _DG.DENSITY0 = 1.0
    R2.dress(13.5, 19.2, -100.0, -42.0, 160, 31, kinds=('stone', 'hay', 'basket', 'pot', 'rope'), avoid=lambda x, y: False)

BUSH = [(rnd.uniform(14.2, 18.4), rnd.uniform(-102, -42), rnd.uniform(0.9, 1.5)) for _ in range(60)]
def frame(g, t, camloc, ctx):
    J.set_holes(12); k = (g - G0) / 30.0
    for n_, (bx, by, bs) in enumerate(BUSH):
        if abs(by - camloc.y) < 16: C.put_puff((bx, by, bs * 0.38), bs * 1.5, camloc, alpha=0.95, name='bush%d' % n_, tone=(78, 58, 44))
    for ob in bpy.data.objects:
        if ob.name in ('tufts', 'furrows', 'posts', 'road') or ob.name.startswith(('stk', 'flame_stk', 'flame_road', 'flame_rd', 'flame_far', 'farglow', 'fgstone', 'fgwood')): ob.hide_render = True
    for j, (dx, dy, sc, dv) in enumerate(REL):
        ycam = Y0 - V_OX * (g - G0) / 30.0
        pos = (XC + dx, ycam + dy + dv * k, 0.0)
        ph = int(k * 12 + j * 3) % 8
        C.put_ox(j, pos, -90, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='side', gait='gallop', theta=0, reed=True, face='rage', tfx=(0.85 if j == 0 else 0.7), lean=86.0)

if __name__ == '__main__':
    KEEP = [(x, y, 3.2) for x in (13.0, 8.2, 3.4) for y in range(-40, -150, -6)]
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
