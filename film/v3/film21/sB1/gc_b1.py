import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'set3d21'))
import b1 as B
import ground_check21 as GC
W = B.World('draft', 4)
items = [(nm, a.card, 0.0) for nm, a in W.actors.items()]
def sf(g):
    W.pose([g]); f = g - B.G0 + 1 if hasattr(W, 'f0') else None
    B.bpy.context.view_layer.update(); B.actors.sync_all(B.bpy.context.scene, W.cam)
air = {nm: range(159, 236) for nm in W.actors if nm.startswith('r')}
rep = GC.check(items, list(range(159, 302, 10)), sf, airborne=air, out=os.path.join(HERE, 'GROUND.md'))
print('fail', rep['fail'], 'sunk', rep['sunk']); print(rep['rows'][:12])
