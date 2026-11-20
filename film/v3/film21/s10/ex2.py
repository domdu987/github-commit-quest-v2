import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c21
from c21 import *
A = K.build_world(['valley_loop', 'camp_bank'], fg=['valley_loop'])
camp = A.get('camp'); print(type(camp), (camp.keys() if isinstance(camp, dict) else None))
pav = camp.get('pav') if isinstance(camp, dict) else None
print('pav', pav[:40] if pav else None)
fl = K.STATE['anim'].get('flags'); print('flags', len(fl))
for o in fl[:60]:
    try: print(o.name, tuple(round(v,1) for v in o.location), tuple(round(v,1) for v in o.matrix_world.translation))
    except Exception as e: print(o, e)
import bpy
print([ (o.name) for o in bpy.data.objects if any(k in o.name.lower() for k in ('banner','flag','pole','pennant','sign'))][:40])
from mathutils import Vector
names = {}
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
    ctr = sum(bb, Vector()) / 8; sz = max(b.x for b in bb) - min(b.x for b in bb)
    if abs(ctr.x + 80) < 90 and ctr.y < -15 and ctr.y > -90 and sz < 40:
        print(o.name, [round(v) for v in ctr], round(sz))
