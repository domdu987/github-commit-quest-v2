#!/usr/bin/env python3
"""shot.py -- film 21 segment F (FALSE PAYOFF, camp_bank): g 1044..1141, CUT in, no handles, ONE travelling camera.
The English on the south bank laugh and point across the river, bouncing out of phase, while the camera side-tracks along them (east -> west) and settles on
Cressingham; CU2 = a fast push into his smug face (thumbs in his belt), lip-sync "เห็นไหม กลัวจนขยับไม่ได้!" (narration 36.32-37.89 = g 1093..1140 only).
World: K.build_world(['camp_bank']).
    python3 shot.py probe|draft|final <a:b[:step]> [out_dir] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C
import numpy as np, bpy
import stirling as K
import cast21
ST = cast21.STORY21
G0, G1 = 1044, 1141
G_SPEAK = (1093, 1140)          # narration 36.32-37.89 (+0.10 s, x30)
G_LAUGH_END = 1096
WORK = os.path.join(HERE, "work")

# camera keys: side-track along the bank (east -> west), medium on the group, medium on Cressingham, then the CU push (last ~1 s)
KEYS = [(1044, (-74.5, -22.5, 2.5), (-83.5, -11.5, 1.55), 26.0),
        (1078, (-90.0, -21.5, 2.4), (-88.8, -11.5, 1.6), 26.0),
        (1106, (-92.6, -18.5, 2.15), (-91.6, -12.5, 1.75), 26.0),
        (1141, (-92.35, -14.9, 2.45), (-91.9, -13.0, 2.4), 26.0)]

# who stands where: (mark, cast, pose, variant, phase)
CAST = [("cress", "cressingham", "cressingham_smug_belt", 0, 0.0), ("surrey", "surrey", "surrey_tired", 0, 0.0),
        ("e0", "footman_a", "footman_a_point_laugh", 0, 0.0), ("e1", "footman_b", "footman_b_laughing", 0, 1.7),
        ("e2", "knight_b", "knight_b_point_laugh", 0, 3.1), ("e3", "footman_a", "footman_a_laughing", 1, 4.4), ("e4", "footman_b", "footman_b_point_laugh", 0, 5.3)]
SCALE = {"cressingham": 0.551, "surrey": 0.519, "footman_a": 0.553, "footman_b": 0.519, "knight_b": 0.546}
PPD = {"cress": 320, "surrey": 192}


def pose_of(mark, cast, story, var, phase, g):
    p = dict(ST[story][1]); dy = 0.0
    if var: p["variant21"] = var
    if mark == "cress":
        p["lean"] = 1.2 * math.sin(g * 0.11); p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.07)
        if G_SPEAK[0] <= g <= G_SPEAK[1]: p = cast21.speak(p, g)
    elif mark == "surrey":
        p["lean"] = 1.5 * math.sin(g * 0.09 + 1.0); p["head_roll"] = 2.0 * math.sin(g * 0.06)
    else:
        if g <= G_LAUGH_END: p, dy = cast21.laugh(p, g, phase=phase)
        else:
            p["lean"] = 2.0 * math.sin(g * 0.13 + phase); p["head_roll"] = 3.0 * math.sin(g * 0.1 + phase)
    p["blink"] = C.blink(g, [1060 + int(phase * 7), 1115 + int(phase * 3)])
    p["t"] = g / 30.0
    return p, dy


def main():
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "raw")
    samples = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    os.makedirs(out, exist_ok=True)
    T = C.Take(["camp_bank"], WORK, fg=True)
    M = T.A["marks"]["camp_bank"]; mode = "draft" if cmd in ("draft", "probe") else "final"
    K.setup_render(T.scene, "final" if cmd == "probe" else mode, 8)
    for mark, cast, story, var, phase in CAST: T.actor("c_" + mark, cast, ppd=PPD.get(mark, 160))
    viv = {}
    for g in gs:
        f = g + 1; r = K.cam_path(None, KEYS, g); viv[f] = r["vivid"][0]
        for mark, cast, story, var, phase in CAST:
            x, y, z = M[mark][:3]; p, dy = pose_of(mark, cast, story, var, phase, g)
            T.place("c_" + mark, f, (x, y, z + dy * SCALE[cast]), scale=SCALE[cast]); T.pose("c_" + mark, f, p)
    T.sprites_for({n: [g + 1 for g in gs] for n in T.actors}, vivid=lambda f: viv[f])
    used = list(T.actors)
    for g in gs:
        f = g + 1; r = K.cam_path(None, KEYS, g)
        K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0)
        if cmd == "probe":
            print(g, np.round(r["loc"], 1), T.heads(f), flush=True); continue
        path = os.path.join(out, "g_%04d.png" % g)
        if mode == "final" and os.path.exists(path): continue
        dt = T.render(f, path, samples=samples, mode=mode, used=used)
        json.dump(dict(g=g, wall=round(dt, 1), heads=T.heads(f), cam=[round(v, 2) for v in r["loc"]]), open(path[:-4] + ".json", "w"))
        print("g %d %.1f s heads %s" % (g, dt, T.heads(f)), flush=True)


if __name__ == "__main__":
    main()
