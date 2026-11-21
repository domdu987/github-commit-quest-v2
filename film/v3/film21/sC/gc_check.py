"""QA §K ground check for segment C (run AFTER the finals, same scene setup): python3 gc_check.py -> GROUND.md"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "set3d21"))
import shot as S, ground_check21 as GC
Tk = S.Take(); gs = list(range(418, 542, 10)) + [541]; Tk.key(gs)
col = [o for o in S.bpy.data.objects if o.name.startswith("troops_bridge")]
def set_frame(g):
    S.bpy.context.scene.frame_set(S.C.bf(g)); Tk.hooks(g)
    for a in Tk.actors.values(): a.sync(Tk.cam, S.bpy.context.scene)
items = list(Tk.actors.values()) + [(o.name, o, 0.0) for o in col]
rep = GC.check(items, gs, set_frame, out=os.path.join(HERE, "GROUND.md")); print("fail", rep["fail"], "sunk", rep["sunk"])
