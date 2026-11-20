import sys; sys.path.insert(0,'.')
import t4lib as L
from t4lib import bpy, P
A=L.setup()
print([ (o.name, tuple(round(v,2) for v in o.matrix_world.translation)) for o in bpy.data.objects if 'win' in o.name.lower() or 'door' in o.name.lower() or 'cal_' in o.name or 'tally' in o.name.lower()])
print('anim keys', [k for k in P.K.STATE['anim'] if 'win' in k or 'door' in k][:10])
