"""QA §K ground check for segment H2a (run AFTER the finals, same scene setup): python3 gc_check.py -> GROUND.md"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "set3d21"))
import shot as S, ground_check21 as GC
Tk = S.Take(); gs = list(range(1342, 1396, 10)) + [1395]; Tk.key(gs)
def set_frame(g):
    S.bpy.context.scene.frame_set(S.C.bf(g)); Tk.hooks(g)
    for a in S.actors.REGISTRY: a.sync(Tk.cam, S.bpy.context.scene)
items = [t[0] for t in Tk.eng] + [t[0] for t in Tk.scots] + [(o.name, o, 0.0) for o in S.bpy.data.objects if o.name.startswith(("wall_back", "en_loop", "en_south", "wall_banners"))]
rep = GC.check(items, gs, set_frame, out=os.path.join(HERE, "GROUND.md")); print("fail", rep["fail"], "sunk", rep["sunk"])
