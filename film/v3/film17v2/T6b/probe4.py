import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P, bpy
from mathutils import Vector
K = P.K
A = P.world_build('T6'); P.key_take('T6')
for g in (1600, 1606, 1640):
    fr = P.shot('T6', g, A, cards=False); cam = bpy.context.scene.camera; cl = Vector(cam.location)
    print('g', g, 'cam', [round(x, 2) for x in cl])
    rows = []
    for o in bpy.data.objects:
        if o.type != 'MESH' or not o.visible_get(): continue
        pts = [o.matrix_world @ Vector(c) for c in o.bound_box]; c = sum(pts, Vector()) / 8; d = (c - cl).length
        mn = [min(p[i] for p in pts) for i in range(3)]; mx = [max(p[i] for p in pts) for i in range(3)]
        if d < 2.6: rows.append((d, o.name, [round(v, 2) for v in mn], [round(v, 2) for v in mx], [m.name for m in o.data.materials][:2]))
    for r in sorted(rows)[:12]: print('  ', round(r[0], 2), r[1], r[2], r[3], r[4])
