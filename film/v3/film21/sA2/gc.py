#!/usr/bin/env python3
"""gc.py -- ground check (QA_TEAM §K) for this segment: every cast card must touch the ground (frames every 10)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "set3d21"))
import shot as S, bpy
import ground_check21 as GC
Tk = S.Seg()
gs = list(range(S.G0, S.G1 + 1, 10)) + [S.G1]
Tk.plan(gs)
items = [a for a in Tk.acts.values()] + [m["a"] for m in getattr(Tk, "par", [])]
def set_frame(g):
    Tk.scene.frame_set(g + 1); bpy.context.view_layer.update()
rep = GC.check(items, frames=gs, set_frame=set_frame, airborne={}, out=os.path.join(HERE, "GROUND.md"))
print("GROUND", rep.get("fail"), rep.get("warn", ""))
