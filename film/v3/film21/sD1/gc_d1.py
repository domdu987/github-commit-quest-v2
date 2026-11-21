#!/usr/bin/env python3
"""gc_d1.py -- QA §K ground check for D1: Cressingham's card and the free props of the money table (frames every 10)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "set3d21"))
import c21 as C, shot as S, bpy
import ground_check21 as GC
K = C.K
bpy.ops.wm.read_factory_settings(use_empty=True)
A = K.build_world(["camp_table"])
class Wrap(C.Take):
    def __init__(self): pass
T = Wrap(); T.A = A; T.cam = bpy.context.scene.camera; T.g0 = S.G0
T.cam_fn, T.act_fn = S.cam_fn(A), S.act_fn(A); T.cast = {"cre": "cressingham"}; T.vivid = {}
a = C.actors.Actor("cre", "cressingham"); a.build(C.sprites.DEFAULT_CANVAS["cressingham"], os.path.join(S.HERE, "work", "sprites"), contact=True); a.head_flip = False
T.acts = {"cre": a}
tx, ty, tz = A["camp"]["table"]
props = []
for o in bpy.data.objects:
    if o.type == "MESH" and (o.name in ("chest_lid", "scale_stand") or o.name.startswith("table_extras")):      # the canopy ROOF is overhead on its poles by design, not a free prop
        props.append((o.name, o, 0.0))
print("props:", [p[0] for p in props])
def set_frame(g):
    T.pose([g])
items = [("cre", a.card, -0.31)] + props           # -0.31 m = the transparent padding below the soles in the Cressingham sprite (measured: SUNK 31.0 cm at the soles)
airborne = {"cre": range(S.G_LAUGH, S.G1 + 1)}            # laugh bounce lifts the card by design (cast21.laugh)
rep = GC.check(items, range(S.G0, S.G1 + 1, 10), set_frame, airborne=airborne, out=os.path.join(S.HERE, "GROUND.md"))
print("fail", rep["fail"], "sunk", rep["sunk"]); print(rep["rows"][:12])
