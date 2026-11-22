#!/usr/bin/env python3
"""s20 (frames 1515-1595): reveal A, round 14 REDESIGN. High side-tracking crane (5 D up, 14 D from the herd line, pitched down), truck at 92 % of herd speed + push,
two rows of side-view oxen (spacing 2.2 ox lengths, rear row offset half a spacing and 3 D farther), lead ox whole in frame, flames capped 0.8 D tilted up 30 deg.
python3 shot.py measure|draft|final [first_g last_g]"""
import os, sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c18 as C
from c18 import J, S, R2, V, bpy
from bpy_extras.object_utils import world_to_camera_view
os.environ.setdefault('NOPOOL', '1')
SHOT = 's20'; G0, G1 = 1515, 1595; H_IN, H_OUT = 6, 6
V_OX = 16.2; V_CAM = 1.0 * V_OX; XC = 20.0; Y0 = -46.0; DUR = 81 / 30.0; LAT = 11.0; CZ = 4.0
def pose(sh, t):
    y = Y0 - V_CAM * t * DUR; lat = LAT - 0.05 * LAT * t * DUR * 0.0 - 0.14 * LAT * t     # 5 %/s push -> about 14 % over the shot
    w = max(0.0, 1.0 - (t * 81) / 7.0) ** 2
    return dict(loc=(XC, y, CZ), look_at=(XC - lat, y + 2.8 + 30.0 * w, 3.0), lens=30.0)
S.pose_at = pose
rnd = random.Random(20)
R2.POST['s20'] = lambda p: None
SP = 20.0                                                       # row spacing = 2.2 ox lengths (ox about 4.5 D)
FRONT = [(-LAT, 2.65 + SP * n, 1.0) for n in range(-2, 3)]       # lead ox = n 0 at dy 3.0 (head at the left of frame)
REAR = [(-LAT - 3.0, 2.65 + SP * (n + 0.5), 0.95) for n in range(-2, 3)]
REL = FRONT[:2] + [FRONT[2]] + FRONT[3:]                         # keep list order: REL[0] must be the lead
REL = [FRONT[2]] + [f for i, f in enumerate(FRONT) if i != 2] + REAR

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

    pr = random.Random(5)
    for n in range(170):                                                  # dressed field between the camera and the herd (world props, all on the ground)
        px_ = pr.uniform(14.0, 19.0); py_ = pr.uniform(-110, -40)
        if pr.random() < 0.35: (lambda sc_: J.prop_reed_bundle((px_, py_, 0.18 * sc_), (0, 0, pr.uniform(0, 6.28)), scale=sc_, n=40, cd=6.0))(pr.uniform(0.6, 0.9))
        else: J.prop_pot((px_, py_, 0.0), pr.uniform(0, 6.28), kind=pr.choice(('pot', 'jar', 'bowl')), scale=pr.uniform(0.6, 0.9), cd=6)

    for n in range(170):                                                 # round 15: small dark rubble in the mid-ground ground band (in front of the lead row, below every ox head)
        px_ = pr.uniform(10.6, 13.4); py_ = pr.uniform(-112, -40)
        if pr.random() < 0.5: (lambda sc_: J.prop_reed_bundle((px_, py_, 0.18 * sc_), (0, 0, pr.uniform(0, 6.28)), scale=sc_, n=30, cd=6.0))(pr.uniform(0.35, 0.55))
        else: J.prop_pot((px_, py_, 0.0), pr.uniform(0, 6.28), kind=pr.choice(('pot', 'jar', 'bowl')), scale=pr.uniform(0.3, 0.5), cd=6)

def frame(g, t, camloc, ctx):
    J.set_holes(12); k = (g - G0) / 30.0
    for ob in bpy.data.objects:
        if ob.name in ('tufts', 'furrows', 'posts', 'road') or ob.name.startswith(('stk', 'flame_stk', 'flame_road', 'flame_rd', 'flame_far', 'farglow', 'fgstone', 'fgwood')): ob.hide_render = True
    ycam = Y0 - V_OX * k
    for j, (dx, dy, sc) in enumerate(REL):
        pos = (XC + dx, ycam + dy, 0.0)
        pc = world_to_camera_view(bpy.context.scene, bpy.data.objects['cam'], V(pos) + V((0, 0, 1.0)))
        if pc.x < -0.45 or pc.x > 1.45 or pc.z < 0: continue
        if g < G0 + 8 and j in (3, 4): continue                              # during the whip-in these two stand over the water channel (ground_check)                 # V2: oxen outside the frame are not placed (they would stand over the water channel)
        ph = int(k * 12 + j * 3) % 8
        C.put_ox(j, pos, -90, sc, camloc, phase=ph, flame=C.flame_for(g, j), state='dragon', view='three_quarter', gait='gallop', theta=30, reed=True, face='rage', tfx=1.2, lean=60.0)

if __name__ == '__main__':
    KEEP = []
    C.run(SHOT, G0 - H_IN, G1 + H_OUT, frame, setup, sys.argv[1:], keep=KEEP)
