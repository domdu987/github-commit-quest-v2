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

G0, G1, G_JOIN = 0, 83, 80
PRE = -24                                   # a key before the film start: the ease-in happens before g0, so the film opens already moving
VW = K.preset_pose("valley_wide")
PA = K.POSES["P_A"]
T0 = (G0 - PRE) / float(G_JOIN - PRE); E0 = T0 * T0 * (2 - T0)       # cam_path's ease-in on the first segment at g0


def pre_key():
    f = lambda a, b: (np.array(a, float) - E0 * np.array(b, float)) / (1 - E0)
    return (PRE, tuple(f(VW[0], PA[0])), tuple(f(VW[1], PA[1])), VW[2])


def keys(A):
    return [pre_key(), (G_JOIN,) + tuple(PA), (159,) + tuple(K.preset_pose("hill_over"))]


def main():
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "raw")
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    os.makedirs(out, exist_ok=True)
    A = K.build_world(["valley_wide", "hill_over"], fg=False)
    sc = bpy.context.scene; ks = keys(A)
    knights = [o for o in bpy.data.objects if o.name.startswith("troops_bridge")]
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
