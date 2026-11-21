#!/usr/bin/env python3
"""shot.py -- film 21 segment A1 (BIGZOOM 1, first half): g 0..80 (+3 handle frames g81..83 continuing the move), film start, ONE travelling camera.
EXTREME WIDE and high over the Forth valley (loop, bridge with the English column, camp, Abbey Craig with tiny Scots), already moving at g0, one eased swoop
that ENDS EXACTLY at pose P_A at g80 (A2, team 5, continues from there by D6).  World: K.build_world(['valley_wide','hill_over']).
    python3 shot.py probe|draft|final <a:b[:step]> [out_dir] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C
import numpy as np, bpy
import stirling as K

SCOTS_TOWARD = tuple(float(v) for v in os.environ.get("TOWARD", "120,-300").split(","))
SCOTS_SCALE = float(os.environ.get("SSCALE", "2.2"))
TRAVEL = 1.0                                 # the column walks north 1.0 m over the segment (0.36 m/s), only where the support height does not change
G0, G1, G_JOIN = 0, 83, 80
PRE = -40                                   # a key before the film start: the ease-in happens before g0, so the film opens already moving
VW = K.preset_pose("P_HOOK")
PA = K.POSES["P_A"]
T0 = (G0 - PRE) / float(G_JOIN - PRE); E0 = T0 * T0 * (2 - T0)       # cam_path's ease-in on the first segment at g0


def pre_key():
    f = lambda a, b: (np.array(a, float) - E0 * np.array(b, float)) / (1 - E0)
    return (PRE, tuple(f(VW[0], PA[0])), tuple(f(VW[1], PA[1])), VW[2])


def keys(A):
    return [pre_key(), (G_JOIN, "P_A"), (159,) + tuple(K.preset_pose("hill_over"))]


def build_column():
    """the whole bridge deck and both causeways full of knight PAIRS: crimson/white caparisons, a riding knight each, one gold pennon per pair (oversized so they read from 230 m)."""
    import numpy as np
    rs = np.random.RandomState(5); B = K.Batch(88); B2 = K.Batch(87); S = 1.4; global COL_PTS; COL_PTS = []
    import bpy
    from mathutils import Vector
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get()
    def support(x, y):
        """z of the first surface under (x, y) (deck, causeway or terrain): the horses stand exactly on it (QA §K ground check)."""
        hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, Vector((x, y, 14.0)), Vector((0, 0, -1)))
        return float(loc.z) if hit else float(K.ground(x, y))
    for i, y in enumerate(np.arange(-56.0, 66.0, 4.2)):
        zs = []; deck = -30.0 <= y <= 34.0; Bc = B if deck else B2      # deck pairs walk; causeway pairs stand (static batch, so nothing floats on the ramp)
        if deck and any(abs(support(K.BRIDGE_X + s_, y + TRAVEL) - support(K.BRIDGE_X + s_, y)) > 0.02 for s_ in (-0.95, 0.95)): continue      # a pair that would cross a step while walking is left out (it would float)
        for sx in (-0.95, 0.95):
            x = K.BRIDGE_X + sx; z = support(x, y); zs.append(z)
            m = (("t_red", "t_white"), ("t_red", "t_cream"))[(i + (sx > 0)) % 2]
            COL_PTS.append((x, y, z)); K.horse(Bc, (x, y, z), 90.0, coat=["horse", "horse_dk", "horse"][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.9 + 0.2 * rs.rand(), rider=(m[0],), scale=S)
        xm, zm = K.BRIDGE_X, float(np.mean(zs))
        Bc.rod("wood", (xm, y, zm + 3.2), (xm, y, zm + 6.2), 0.05, seg=4); Bc.box("gold", (xm + 0.0, y + 0.55, zm + 5.8), (0.05, 1.1, 0.7))     # gold pennon per pair
    B2.finalize("troops_cws")
    return B.finalize("troops_col")


def main():
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "raw")
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    os.makedirs(out, exist_ok=True)
    A = K.build_world(["valley_wide"], fg=False, scots_wide=False)
    K.scots_wide_line(n=26, banners=5, scale=SCOTS_SCALE, toward=SCOTS_TOWARD)        # the visible Scots line, facing the south camera
    sc = bpy.context.scene; ks = keys(A)
    for o in [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]: bpy.data.objects.remove(o, do_unlink=True)
    knights = build_column()
    if cmd == "ground":                                    # QA §K: the column / Scots objects are merged meshes, so the check ray-casts at each horse's support point
        from mathutils import Vector
        for o in bpy.data.objects:
            if o.name.startswith(("troops_c", "scots_wide")): o.hide_viewport = True
        bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get(); rows = []; fail = 0
        for (x, y, z) in COL_PTS:                          # the horses stand at z; the first surface below z + 0.5 must be within 2 cm
            hit, loc, nrm, idx, ob, mtx = bpy.context.scene.ray_cast(dg, Vector((x, y, z + 0.5)), Vector((0, 0, -1)))
            gap = None if not hit else z - loc.z
            if gap is None or abs(gap) > 0.02: fail += 1; rows.append((x, y, z, "nothing below" if gap is None else "%.1f cm" % (gap * 100)))
        lines = ["# GROUND check (QA §K) - %s" % ("PASS" if fail == 0 else "FAIL"), "", "sA1 has no cards. Checked: %d knight/horse support points of the column (deck, causeways, south bank): FAIL %d (tolerance 2 cm). `GC.check` on the merged Scots/column meshes is meaningless (one object per material), so the horses are ray-cast at their support points instead; the Scots line and banners are placed with `K.ground(x, y)` by the set (`scots_wide_line`)." % (len(COL_PTS), fail), ""]
        lines += ["| x | y | z | gap |", "|---|---|---|---|"] + ["| %.1f | %.1f | %.2f | %s |" % r for r in rows]
        open(os.path.join(HERE, "GROUND.md"), "w").write("\n".join(lines) + "\n"); print("ground:", fail, "fail of", len(COL_PTS)); return
    mode = "draft" if cmd in ("draft", "probe") else "final"
    for g in gs:
        r = K.cam_path(None, ks, g)
        K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0)
        for o in knights: o.location.y = TRAVEL * g / 83.0
        if cmd == "probe":
            print(g, np.round(r["loc"], 1), np.round(r["look"], 1), round(r["lens"], 1), np.round(r["vivid"], 2)); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path): continue
        K.setup_render(sc, mode, samples); sc.render.threads = int(os.environ.get("THREADS", "4")); sc.render.filepath = path
        import time; t = time.time(); bpy.ops.render.render(write_still=True); K.grade(path)
        print("g %d %.1f s loc %s" % (g, time.time() - t, np.round(r["loc"], 1)), flush=True)


if __name__ == "__main__":
    main()
