import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import t6b_stage, prefecture17 as P, bpy
from mathutils import Vector
A = P.world_build('T6')
seen = {}
for o in bpy.data.objects:
    if o.type not in ('MESH', 'LIGHT', 'EMPTY'): continue
    pts = [o.matrix_world @ Vector(c) for c in o.bound_box] if o.type == 'MESH' else [o.matrix_world.translation]
    c = sum(pts, Vector()) / len(pts); sz = max(max(p[i] for p in pts) - min(p[i] for p in pts) for i in range(3))
    if abs(c.x - 16.3) < 1.3 and abs(c.y - 27.5) < 1.3 and 1.1 < c.z < 3.6 and sz < 3:
        seen[o.name] = (o.type, [round(v, 2) for v in c], round(sz, 2), o.parent.name if o.parent else None)
for k, v in sorted(seen.items()): print(k, v)
print(len(seen))
