import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shot import *
import ground_check21 as GC
gs = list(range(1709, 1849, 10))
T = c21.Take(["riverbank", "river_low"], quality="draft")
T.workdir = os.path.join(HERE, "work_gc"); os.makedirs(T.workdir, exist_ok=True)
on_g = make_bank(T, gs)
K.setup_render(T.scene, "draft", 4)
items = []
for n, r in T.rigs.items():
    cv = sprites.DEFAULT_CANVAS[r.cast]
    sc = r.scale
    items.append((n, r.a.card, -(cv[3] * sc * (0.5 if n.startswith('H') else 1.0))))
air = {}
for n, (t0, kind, h, sz) in JUMPS.items(): air[n] = range(t0 - 1, t0 + T_AIR + 3)
def set_frame(g):
    T.scene.frame_set(bf(g)); on_g(g)
    actors.sync_all(T.scene, T.cam)
rep = GC.check(items, gs, set_frame, airborne=air, out=os.path.join(HERE, "GROUND.md"))
print("GC", rep["fail"], rep["sunk"], rep["rows"][:12])
