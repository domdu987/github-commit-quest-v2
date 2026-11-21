#!/usr/bin/env python3
"""QA §K ground check for segment J1 (free props: the dressing object, the chest, the table, the lantern is hung so excluded)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "set3d21"))
import shot as S
from shot import C, K, bpy
import ground_check21 as GC
T = C.Take("camp_table", "draft", 6, world=["camp_table"]); A = T.A; S.dress(A)
items = []
for o in bpy.data.objects:
    if o.name in ("s08_dress", "scale_stand_wood_dk", "table_extras_wood", "table_extras_cloth_red"): items.append((o.name, o, 0.0))
frames = list(range(S.G0, S.G1, 10))
def set_frame(g): S.cam_for(g, A); S.hooks(g, A); bpy.context.scene.frame_set(g + 1)
rep = GC.check(items, frames, set_frame, airborne={}, out=os.path.join(HERE, "GROUND.md"))
print("fail", rep["fail"], "sunk", rep["sunk"]); print(rep["rows"][:8])
