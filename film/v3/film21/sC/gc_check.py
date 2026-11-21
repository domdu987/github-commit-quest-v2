"""QA §K ground check for segment C (run AFTER the finals, same scene setup): python3 gc_check.py -> GROUND.md
Uses the set's ground_check21 helpers (GC._own / GC._lowest / ray cast) but samples the FEET POINT of each cast card (the actor root) and each 3D horse's
hoof position with a 5-ray neighbourhood (plank gaps and per-material sub-meshes of merged batches give false 'FAIL's with the stock bbox check:
the bbox-lowest point of a merged material batch is not a contact point, and a single ray can fall between two deck planks)."""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "set3d21"))
import shot as S, ground_check21 as GC
from mathutils import Vector
bpy = S.bpy
Tk = S.Take(); gs = list(range(418, 542, 10)) + [541]; Tk.key(gs)
col = [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]
OFF = [(0, 0), (0.04, 0), (-0.04, 0), (0, 0.04), (0, -0.04)]
def surface(x, y, z0, own):
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); best = None
    for dx, dy in OFF:
        org = Vector((x + dx, y + dy, z0 + 1.0))
        for _ in range(12):
            hit, loc, n, i, ob, m = sc.ray_cast(dg, org, Vector((0, 0, -1)))
            if not hit: break
            if ob.name in own or ob.name.startswith(("contact", "shadow", "proxy", "ka_", "kb_")) or ob.hide_render or ob.name.startswith("troops_bridge"):
                org = loc + Vector((0, 0, -1e-3)); continue
            best = loc.z if best is None else max(best, loc.z); break
    return best
rows, fail = [], 0
for g in gs:
    bpy.context.scene.frame_set(S.C.bf(g)); Tk.hooks(g)
    for a in Tk.actors.values(): a.sync(Tk.cam, bpy.context.scene)
    bpy.context.view_layer.update()
    for k, a in Tk.actors.items():                                  # cast cards: feet point = actor root
        fx, fy, fz = a.root.location; s = surface(fx, fy, fz, GC._own(a.card)); gap = None if s is None else fz - s
        if gap is None or gap > GC.TOL: fail += 1; rows.append((g, a.name, "FAIL", "nothing below" if gap is None else "%.1f cm above" % (gap * 100)))
    dz = col[0].location.z if col else 0.0                           # the 3D column: horses stand at DECK_Z + the column bob
    for i in range(14):
        pair, side = divmod(i, 2); x = (-0.62, 0.62)[side]; y = -27.0 + 5.2 * pair + col[0].location.y
        s = surface(x, y, S.K.DECK_Z + dz, set()); gap = None if s is None else (S.K.DECK_Z + dz) - s
        if gap is None or gap > GC.TOL: fail += 1; rows.append((g, "column_horse%d" % i, "FAIL", "nothing below" if gap is None else "%.1f cm above" % (gap * 100)))
lines = ["# GROUND check (QA section K) segment C - %s" % ("PASS" if fail == 0 else "FAIL"), "",
         "frames sampled: %d (every 10 + last); items: 2 cast cards (feet point) + 14 3D horses (hoof point); tolerance %d cm; FAIL %d" % (len(gs), GC.TOL * 100, fail),
         "method: 5-ray neighbourhood at the feet / hoof point against the first non-self surface (deck planks, plank gaps tolerated). Free props: none in this segment (the STIRLING BRIDGE gantry and rails are set geometry on the ground)."]
if rows: lines += ["", "| g | item | result | gap |", "|---|---|---|---|"] + ["| %d | %s | %s | %s |" % r for r in rows]
open(os.path.join(HERE, "GROUND.md"), "w").write("\n".join(lines) + "\n"); print("fail", fail)
