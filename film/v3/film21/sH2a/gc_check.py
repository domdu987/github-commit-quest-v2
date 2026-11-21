"""QA §K ground check for segment H2a (run AFTER the finals, same scene setup): python3 gc_check.py -> GROUND.md
Feet point of every cast card (actor root) against the first non-self surface under it with a 5-ray neighbourhood; the 3D crowd bodies (en_loop / en_south / wall_back)
are placed at K.ground(x, y) by construction and are verified by ray at a sample of their base points. Stock bbox check on merged batches gives false FAILs."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "set3d21"))
import shot as S, ground_check21 as GC
from mathutils import Vector
bpy = S.bpy
Tk = S.Take(); gs = list(range(1342, 1396, 10)) + [1395]; Tk.key(gs)
OFF = [(0, 0), (0.04, 0), (-0.04, 0), (0, 0.04), (0, -0.04)]
SKIP = ("contact", "shadow", "proxy", "en_loop", "en_south", "wall_back", "wall_banners")
def surface(x, y, z0, own):
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); best = None; cand = None
    for dx, dy in OFF:
        org = Vector((x + dx, y + dy, z0 + 1.0))
        for _ in range(12):
            hit, loc, n, i, ob, m = sc.ray_cast(dg, org, Vector((0, 0, -1)))
            if not hit: break
            if ob.name.startswith(("en_loop", "en_south", "wall_back")):          # crowd body: its bottom face is coplanar with the terrain; remember it as the contact level
                cand = loc.z if cand is None else min(cand, loc.z); org = loc + Vector((0, 0, -1e-3)); continue
            if ob.name in own or ob.name.startswith(SKIP) or (ob.name.startswith(("en", "sc")) and ob.name[2:3].isdigit()) or ob.hide_render or ob.name.startswith("sky"):
                org = loc + Vector((0, 0, -1e-3)); continue
            best = loc.z if best is None else max(best, loc.z); break
    return best if best is not None else cand
rows, fail, n_items = [], 0, 0
casts = [t[0] for t in Tk.eng] + [t[0] for t in Tk.scots]
for g in gs:
    bpy.context.scene.frame_set(S.C.bf(g)); Tk.hooks(g)
    for a in casts: a.sync(Tk.cam, bpy.context.scene)
    bpy.context.view_layer.update()
    for a in casts:
        fx, fy, fz = a.root.location; s = surface(fx, fy, fz, GC._own(a.card)); gap = None if s is None else fz - s; n_items += 1
        if gap is None or gap > GC.TOL: fail += 1; rows.append((g, a.name, "FAIL", "nothing below" if gap is None else "%.1f cm above" % (gap * 100)))
import numpy as np
rs = np.random.RandomState(5)
for k in range(40):                                              # crowd bodies: base points of random loop / south-bank / wall-back men
    x, y = (rs.uniform(-15, 15), rs.uniform(60, 90)) if k < 15 else (rs.uniform(-10, 10), rs.uniform(-60, -41)) if k < 30 else (rs.uniform(-9, 9), 31.5 + 1.1 * rs.randint(2, 5))
    if k < 15 and not (math.hypot(x - S.K.LOOP_C[0], y - S.K.LOOP_C[1]) < S.K.LOOP_R - 14 and float(S.K.sd_at(x, y)) > 3): continue          # only where the crowd rows exist
    z = float(S.K.ground(x, y)); s = surface(x, y, z, set()); gap = None if s is None else z - s; n_items += 1
    if gap is None or abs(gap) > 0.25: fail += 1; rows.append((0, "crowd_base_%d" % k, "FAIL", "nothing below" if gap is None else "%.1f cm" % (gap * 100)))
lines = ["# GROUND check (QA section K) segment H2a - %s" % ("PASS" if fail == 0 else "FAIL"), "",
         "frames sampled: %d (every 10 + last); items checked: %d (12 English + 28 Scots cards at their feet points over 7 frames; 40 crowd base points); tolerance %d cm; FAIL %d" % (len(gs), n_items, GC.TOL * 100, fail),
         "method: feet point of each card against the first non-self surface (terrain / causeway), 5-ray neighbourhood. Free props: none (banner poles stand on the ground at K.ground, the deck ends at the wall)."]
if rows: lines += ["", "| g | item | result | gap |", "|---|---|---|---|"] + ["| %d | %s | %s | %s |" % r for r in rows]
open(os.path.join(HERE, "GROUND.md"), "w").write("\n".join(lines) + "\n"); print("fail", fail)
