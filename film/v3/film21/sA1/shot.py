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
    rs = np.random.RandomState(5); B = K.Batch(88); S = 1.4
    for i, y in enumerate(np.arange(-56.0, 66.0, 4.2)):
        on_deck = -34.0 <= y <= 38.0
        for sx in (-0.95, 0.95):
            x = K.BRIDGE_X + sx
            z = K.DECK_Z if on_deck else max(float(K.ground(x, y)), 0.0) + (0.45 if y > 38 else 0.0)
            m = (("t_red", "t_white"), ("t_red", "t_cream"))[(i + (sx > 0)) % 2]
            K.horse(B, (x, y, z), 90.0, coat=["horse", "horse_dk", "horse"][rs.randint(0, 3)], trap=m[0], trim=m[1], tint=0.9 + 0.2 * rs.rand(), rider=(m[0],), scale=S)
        xm, zm = K.BRIDGE_X, (K.DECK_Z if on_deck else max(float(K.ground(K.BRIDGE_X, y)), 0.0) + (0.45 if y > 38 else 0.0))
        B.rod("wood", (xm, y, zm + 3.2), (xm, y, zm + 6.2), 0.05, seg=4); B.box("gold", (xm + 0.0, y + 0.55, zm + 5.8), (0.05, 1.1, 0.7))     # gold pennon per pair
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
    if cmd == "ground":                                                    # QA §K ground check: the knight column, the Scots line and their banners (every 10 frames)
        import ground_check21 as GC
        items = [(o.name, o, 0.0) for o in bpy.data.objects if o.name.startswith(("troops_col", "scots_wide"))]
        def set_frame(g):
            K.cam_path(None, ks, g)
            for o in knights: o.location.y = 1.3 * g / 30.0
        rep = GC.check(items, list(range(G0, G1 + 1, 10)), set_frame, out=os.path.join(HERE, "GROUND.md")); print("ground:", rep["fail"], "fail", rep["sunk"], "sunk"); return
    mode = "draft" if cmd in ("draft", "probe") else "final"
    for g in gs:
        r = K.cam_path(None, ks, g)
        K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0)
        for o in knights: o.location.y = 1.3 * g / 30.0
        if cmd == "probe":
            print(g, np.round(r["loc"], 1), np.round(r["look"], 1), round(r["lens"], 1), np.round(r["vivid"], 2)); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path): continue
        K.setup_render(sc, mode, samples); sc.render.threads = int(os.environ.get("THREADS", "4")); sc.render.filepath = path
        import time; t = time.time(); bpy.ops.render.render(write_still=True); K.grade(path)
        print("g %d %.1f s loc %s" % (g, time.time() - t, np.round(r["loc"], 1)), flush=True)


if __name__ == "__main__":
    main()
