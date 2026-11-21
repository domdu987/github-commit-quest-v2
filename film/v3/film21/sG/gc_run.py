#!/usr/bin/env python3
"""QA §K ground check for segment G: python3 gc_run.py  (writes GROUND.md)"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "set3d21"))
import shot as S
from shot import C, K, bpy
import ground_check21 as GC
T, items = S.build("draft", 6)
frames = list(range(S.G0, S.G1, 10)) + [1238]
for g in frames:
    S.cam_for(g); S.hooks(g)
    for nm, cst, pn, (x, y, z), grp, i in items:
        T.place(nm, g + 1, (x, y, z + (0.0)))
gc_items = [(nm, T.actors[nm].root, 0.0) for nm, cst, pn, pos, grp, i in items]      # the actor root empty sits exactly on the feet point
for o in T.col:
    if o.name.endswith('_horse'): gc_items.append((o.name, o, 0.0))
def set_frame(g):
    bpy.context.scene.frame_set(g + 1)
rep = GC.check(gc_items, frames, set_frame, airborne={}, out=os.path.join(HERE, "GROUND.md"))
print("fail", rep["fail"], "sunk", rep["sunk"]); print(rep["rows"][:12])
