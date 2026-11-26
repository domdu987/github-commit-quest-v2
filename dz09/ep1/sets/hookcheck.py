"""hookcheck.py -- which EP.1 additions of X1 / X1s could a hook camera see?  Builds the deck with the dressing, then for
each of the hook's 72 dumped cameras (first / middle / last frame of S01-S24, out/hook_cams.json) projects every vertex
of every added object, keeps those inside the 720x1280 frame (plus a 4 % margin for hand-held shake), and ray-casts
from the camera to tell whether the set hides them.  Writes out/hook_check.json and out/hook_check.md.
Glass counts as an occluder here only when it is the dark opaque car glass; the hero car's clear glass is skipped."""
import os, json, math
HERE = os.path.dirname(os.path.abspath(__file__))


def run():
    import rig as RG, core as K, x1, sedan
    import bpy, numpy as np
    from mathutils import Vector
    import check_hook as CH
    r = RG.Rig("draft", 360, 640, threads=1, puppets=False)
    R1 = x1.dress(r.A); x1.alarm(True)
    R2 = sedan.build(r.A)
    bpy.context.view_layer.update()
    groups = {
        "truck hardware (x1)": [o for o in R1["parts"] if o.name.startswith("x1_") and "puddle" not in o.name and "alarm" not in o.name],
        "puddles at the truck (x1)": [o for o in R1["parts"] if "puddle" in o.name],
        "alarm lamps on %s (x1)" % R1["anchors"]["alarm_car"]: x1._S["alarm"]["ind"],
        "overturned sedan (x1s)": [o for o in K.tree(R2["root"]) if o.type == "MESH"],
        "sedan debris (x1s)": [o for o in R2["parts"] if o.type == "MESH" and "steam" not in o.name],
        "sedan steam card (x1s)": [o for o in R2["parts"] if "steam" in o.name],
    }
    cams = CH.cams()
    dg = bpy.context.evaluated_depsgraph_get()
    sc = bpy.context.scene
    own = set()
    for obs in groups.values():
        for o in obs: own.add(o.name)
    rows = []
    for gname, obs in groups.items():
        pts = []
        for o in obs:
            if o.type != "MESH": continue
            M = o.matrix_world
            vs = [M @ v.co for v in o.data.vertices]
            step = max(1, len(vs) // 400)
            pts += [(tuple(p), o.name) for p in vs[::step]]
        if not pts:                                   # an empty group (the truck's puddles were removed) used to crash project()
            rows.append(dict(group=gname, objects=0, samples=0, shots={})); continue
        P = np.array([p for p, _ in pts])
        per = {}
        for c in cams:
            x, y, z = CH.project(c, P)
            m = 0.04
            inside = (z > 0.1) & (x > -m) & (x < 1 + m) & (y > -m) & (y < 1 + m)
            n_in = int(inside.sum())
            if not n_in: continue
            cl = Vector(np.array(c["M"])[:3, 3])
            vis = 0; zmin = 1e9; xs = []; ys = []
            for i in np.nonzero(inside)[0]:
                p = Vector(P[i]); d = p - cl; dist = d.length
                hit, loc, n, fi, ob, mm = sc.ray_cast(dg, cl + d.normalized() * 0.06, d.normalized(), distance=dist - 0.08)
                tries = 0
                while hit and ob is not None and (ob.name in own or "glass" in ob.name or ob.name.startswith(("hero_car_cabin", "steam", "smoke", "plume", "flood_beam"))) and tries < 6:
                    start = loc + d.normalized() * 0.02
                    rem = dist - (start - cl).length - 0.08
                    if rem <= 0: hit = False; break
                    hit, loc, n, fi, ob, mm = sc.ray_cast(dg, start, d.normalized(), distance=rem); tries += 1
                if not hit:
                    vis += 1; zmin = min(zmin, float(z[i])); xs.append(float(x[i])); ys.append(float(y[i]))
            s = per.setdefault(c["shot"], dict(in_frame=0, unoccluded=0, nearest=None, px=0))
            s["in_frame"] = max(s["in_frame"], n_in); s["unoccluded"] = max(s["unoccluded"], vis)
            if vis:
                s["nearest"] = round(min(zmin, s["nearest"] or 1e9), 1)
                s["px"] = max(s["px"], int(max((max(xs) - min(xs)) * 720, (max(ys) - min(ys)) * 1280)))
        rows.append(dict(group=gname, objects=len(obs), samples=len(pts), shots=per))
        print(gname, {k: v for k, v in per.items()}, flush=True)
    json.dump(rows, open(os.path.join(HERE, "out", "hook_check.json"), "w"), indent=1)
    L = ["| Added by EP.1 | Objects | Hook shots whose frame holds any of it | Shots where it is not hidden by the set (largest extent on a 720x1280 frame, nearest distance) |", "|---|---|---|---|"]
    for r_ in rows:
        inf = ", ".join(sorted(r_["shots"])) or "none"
        vis = ", ".join("%s (%d px, %.0f D)" % (k, v["px"], v["nearest"]) for k, v in sorted(r_["shots"].items()) if v["unoccluded"]) or "none"
        L.append("| %s | %d | %s | %s |" % (r_["group"], r_["objects"], inf, vis))
    open(os.path.join(HERE, "out", "hook_check.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))
