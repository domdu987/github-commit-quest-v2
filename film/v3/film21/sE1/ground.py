#!/usr/bin/env python3
"""ground.py -- QA section K ground check for sE1: builds the same scene as shot.py, poses every 10th frame, ray-casts every card and the e1_props object down."""
import os, sys
import shot as S
import ground_check21 as GC
C, bpy, K = S.C, S.bpy, S.K


def main():
    T = S.make_take()
    items = []
    for nm, a in T.acts.items():
        cast = T.cast[nm]; y1 = C.sprites.DEFAULT_CANVAS[cast][3]            # canvas bottom below the soles (head-D units)
        items.append((nm, a.card, -y1 * C.unit_scale(cast)))
    props = bpy.data.objects.get("e1_props")
    frames = list(range(S.G_FIRST, S.G1 + 1, 10))
    if props is not None:
        items.append(("e1_props", props, 0.0))

    def set_frame(g):
        T.pose([g]); f = T.f(g); bpy.context.scene.frame_set(f); C.actors.sync_all(bpy.context.scene, T.cam)

    rep = GC.check(items, frames, set_frame, out=os.path.join(S.HERE, "GROUND.md"))
    print("fail", rep["fail"], "sunk", rep["sunk"]); print(rep["rows"][:20])


if __name__ == "__main__":
    main()
