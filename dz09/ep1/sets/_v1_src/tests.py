"""tests.py -- proofs for the EP.1 sets: stills from the planned camera positions, the 24-frame cost test, the sheet.

    python3 tests.py still X1 [--cam S34] [--tier draft|final|finalA] [--size 360x640] [--tag t]
    python3 tests.py cost  X1 [--frames 24]         24 draft frames (360x640, 2 spp, 1 thread) from the set's cost camera
    python3 tests.py final X1                       one final-tier 720x1280 still from the cost camera (class scale of the shot)
    python3 tests.py hookcheck                      are the X1 / X1s additions inside any hook camera's frame?
    python3 tests.py sheet                          out/stills/* -> sets_sheet.png ;   python3 tests.py table -> cost_table.md
Sets: X1 X1S X2 CAB GEAR STAIR UND
"""
import os, sys, json, math, time, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def V3(*a):
    from mathutils import Vector
    return Vector(a[0]) if len(a) == 1 else Vector(a)


# ------------------------------------------------------------------------------------------------------ set tables
def build_set(rig, key):
    import core as K
    A = rig.A
    if key == "X1":
        import x1
        return x1.dress(A)
    if key == "X1S":
        import x1, sedan
        x1.dress(A); return sedan.build(A)
    if key == "X2":
        import x2
        return x2.build(A)
    if key in ("CAB", "GEAR"):
        import x2, cab
        x2.build(A)
        return cab.build(A, at="x2")
    if key in ("STAIR", "UND"):
        import x2, under
        x2.build(A)
        return under.build(A)
    raise SystemExit("unknown set " + key)


def cams_for(key):
    import camdefs
    return camdefs.CAMS[key]


def stage_cam(rig, R, cd, frame=7, u=0.5):
    """pose the set, the puppets and the camera for one camera definition; returns the post options."""
    d = cd["fn"](rig, R, u)
    rig.camera(d["loc"], d["look"], d["lens"], roll=d.get("roll", 0.0), focus=d.get("focus"), k=d.get("k", 7.0), kmax=d.get("kmax", 22.0), clip=d.get("clip", 0.05))
    post = dict(d.get("post", {}))
    rig.apply(exposure=post.get("exposure", 1.6), shadow_at=d.get("shadow_at"), flat=post.pop("flat", None))
    if d.get("late"): d["late"](rig, R)
    return post, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode"); ap.add_argument("set", nargs="?", default="")
    ap.add_argument("--cam", default=""); ap.add_argument("--tier", default="draft"); ap.add_argument("--size", default="")
    ap.add_argument("--frames", type=int, default=24); ap.add_argument("--tag", default=""); ap.add_argument("--frame", type=int, default=7); ap.add_argument("--steady", type=int, default=4)
    a = ap.parse_args()
    if a.mode == "sheet":
        import sheet; sheet.make(); return
    if a.mode == "table":
        import sheet; sheet.table(); return
    import rig as RG
    key = a.set.upper()
    if a.mode == "hookcheck":
        import hookcheck; hookcheck.run(); return
    size = a.size or ("720x1280" if a.mode == "final" or a.tier.startswith("final") else "360x640")
    W, H = [int(x) for x in size.split("x")]
    tier = "final" if a.mode == "final" else a.tier
    rig = RG.Rig(tier, W, H, threads=1)
    import core as K
    c0 = RG.cpu()
    R = build_set(rig, key)
    K.retarget(rig.cam)
    print("set %s built: %.1f CPU s" % (key, RG.cpu() - c0), flush=True)
    for kk in ("anchors", "roof_route", "roof_route_l1", "hidden_rows", "info"):
        if isinstance(R, dict) and kk in R: print("REG", kk, json.dumps(R[kk], default=lambda o: [round(x, 3) for x in o] if hasattr(o, "__iter__") else str(o)), flush=True)
    cams = cams_for(key)
    if a.mode == "still":
        d = os.path.join(OUT, "stills" + ("_" + a.tag if a.tag else "")); os.makedirs(d, exist_ok=True)
        for cd in cams:
            if a.cam and cd["name"] not in a.cam.split(","): continue
            if tier != "draft": rig.set_pct(100 if cd.get("cls", "B") == "A" else 75)
            post, dd = stage_cam(rig, R, cd, a.frame)
            r = rig.render(os.path.join(d, "%s_%s_%s" % (key, cd["name"], tier)), frame=dd.get("frame", a.frame), post=post)
            print("STILL %s %s cpu %.1f wall %.1f" % (key, cd["name"], r["cpu"], r["wall"]), flush=True)
    elif a.mode in ("cost", "final"):
        cd = [c for c in cams if c.get("cost")][0]
        if a.mode == "final":
            cls = cd.get("cls", "B"); rig.set_pct(100 if cls == "A" else 75)
            d = os.path.join(OUT, "final"); os.makedirs(d, exist_ok=True)
            post, dd = stage_cam(rig, R, cd, a.frame)
            r = rig.render(os.path.join(d, "%s_%s_final" % (key, cd["name"])), frame=dd.get("frame", a.frame), post=post)
            rec = dict(set=key, cam=cd["name"], cls=cls, pct=rig.pct, spp=rig.spp, cpu=r["cpu"], wall=r["wall"], cpu_render=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"))
            # the other class scale as well, so both final costs are measured, not extrapolated
            rig.set_pct(75 if cls == "A" else 100)
            post, dd = stage_cam(rig, R, cd, a.frame)
            r2 = rig.render(os.path.join(d, "%s_%s_final_alt" % (key, cd["name"])), frame=dd.get("frame", a.frame), post=post)
            rec["alt"] = dict(pct=rig.pct, cpu=r2["cpu"], wall=r2["wall"])
            # steady state at the class scale: consecutive frames after the first sync (the plan's gate is a run, not one still)
            rig.set_pct(100 if cls == "A" else 75); st = []
            for i in range(a.steady):
                s0 = RG.cpu()
                post, dd = stage_cam(rig, R, cd, 8 + i, (i + 1) / 23.0)
                rig.render(os.path.join(d, "_steady_%s" % key), frame=8 + i, post=post)
                st.append(round(RG.cpu() - s0, 2)); print("STEADY %s %d cpu %.1f" % (key, i, st[-1]), flush=True)
            if st: rec["steady"] = dict(pct=rig.pct, frames=len(st), cpu=st, cpu_mean=round(sum(st) / len(st), 2))
            if os.path.exists(os.path.join(d, "_steady_%s.png" % key)): os.remove(os.path.join(d, "_steady_%s.png" % key))
            json.dump(rec, open(os.path.join(OUT, "final_%s.json" % key), "w"), indent=1)
            print("FINAL", rec, flush=True)
        else:
            d = os.path.join(OUT, "cost", key); os.makedirs(d, exist_ok=True)
            recs = []
            for i in range(a.frames):
                u = i / max(a.frames - 1, 1)
                s0 = RG.cpu(); w0 = time.time()
                post, dd = stage_cam(rig, R, cd, 7 + i, u)
                r = rig.render(os.path.join(d, "f_%04d" % i), frame=7 + i, post=post)
                recs.append(dict(i=i, cpu=round(RG.cpu() - s0, 2), wall=round(time.time() - w0, 2), cpu_render=r.get("cpu_render_total"), cpu_post=r.get("cpu_post")))
                print("COST %s %d cpu %.1f wall %.1f" % (key, i, recs[-1]["cpu"], recs[-1]["wall"]), flush=True)
            n = len(recs)
            rec = dict(set=key, cam=cd["name"], cls=cd.get("cls", "B"), frames=n, tier="draft 360x640 2 spp 1 thread",
                       cpu_mean=round(sum(r["cpu"] for r in recs) / n, 2), cpu_mean_after_first=round(sum(r["cpu"] for r in recs[1:]) / max(n - 1, 1), 2),
                       cpu_first=recs[0]["cpu"], wall_mean=round(sum(r["wall"] for r in recs) / n, 2),
                       build_cpu=round(rig.build_cpu, 1), recs=recs)
            json.dump(rec, open(os.path.join(OUT, "cost_%s.json" % key), "w"), indent=1)
            print("COSTDONE", {k: v for k, v in rec.items() if k != "recs"}, flush=True)


if __name__ == "__main__":
    main()
