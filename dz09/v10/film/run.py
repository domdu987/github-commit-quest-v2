"""run.py -- render any shot / frame range of the EP.1 hook film at any size, aspect and tier.  Resumable.

    python3 run.py --shots S06,S07                 whole shots
    python3 run.py --frames 266:302                global film frames (0-based, end exclusive); the shot is looked up
    python3 run.py --all --tier draft --size 360x640 --worker 0/4 --threads 1
    python3 run.py --shots S18 --at 0.5            one still per shot at 50 % of its length -> out/<tier>/stills/
    options: --tier draft|preview|final|final8   --size WxH (720x1280, 360x640, 1280x720 ...)   --every N
             --levels RAIN=0.6,DOF=0.5 (post11.LEVELS for this run; --levels v1 = draft-v1 look)   --pct N (render scale)
             --force (re-render existing frames)  --keep (keep the EXR passes for re-grading with render11.repost)

Frames go to out/<tier>_<W>x<H>/<shot>/f_####.png (#### = film frame + 1) with f_####_depth.png (16-bit) beside them.
"""
import os, sys, json, time, argparse, importlib, resource, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C


def out_dir(tier, W, H):
    return os.path.join(HERE, "out", "%s_%dx%d" % (tier, W, H))


def shot_module(sid):
    return importlib.import_module("shots." + sid.lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", default=""); ap.add_argument("--frames", default=""); ap.add_argument("--all", action="store_true")
    ap.add_argument("--tier", default="draft"); ap.add_argument("--size", default="360x640")
    ap.add_argument("--threads", type=int, default=4); ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--worker", default="0/1"); ap.add_argument("--force", action="store_true"); ap.add_argument("--keep", action="store_true")
    ap.add_argument("--at", default=""); ap.add_argument("--spp", type=int, default=0); ap.add_argument("--tag", default="")
    ap.add_argument("--levels", default="", help="clarity levels for this run, e.g. RAIN=0.6,DOF=0.5 (see post11.LEVELS); 'v1' = the draft-v1 look")
    ap.add_argument("--pct", type=int, default=0, help="render scale in percent (overrides the tier's; final = 75)")
    a = ap.parse_args()
    W, H = [int(x) for x in a.size.lower().split("x")]
    frames = []
    if a.all:
        frames = list(range(C.NF))
    if a.shots:
        for sid in a.shots.upper().split(","):
            g0, g1 = C.shot_range(sid)
            if a.at:
                frames += [min(g1 - 1, g0 + int(round(float(u) * (g1 - g0 - 1)))) for u in a.at.split(",")]
            else:
                frames += list(range(g0, g1))
    if a.frames:
        for part in a.frames.split(","):
            if ":" in part:
                x, y = part.split(":"); frames += list(range(int(x), int(y)))
            else:
                frames.append(int(part))
    frames = sorted(set(frames))[::a.every]
    wi, wn = [int(x) for x in a.worker.split("/")]
    frames = [g for g in frames if (g // 6) % wn == wi]
    stills = bool(a.at) or bool(a.tag)
    base = out_dir(a.tier, W, H)
    todo = []
    for g in frames:
        sid = C.shot_of(g)
        d = os.path.join(base, "stills" + (("_" + a.tag) if a.tag else "")) if stills else os.path.join(base, sid)
        name = ("%s_f%04d" % (sid, g + 1)) if stills else ("f_%04d" % (g + 1))
        if a.force or not os.path.exists(os.path.join(d, name + ".png")):
            todo.append((g, sid, d, name))
    print("frames to render: %d of %d" % (len(todo), len(frames)), flush=True)
    if not todo:
        return
    import stage
    if a.pct: stage.PCT_FORCE = a.pct
    if a.levels:
        import post11
        if a.levels.lower() == "v1": post11.LEVELS.update(post11.LEVELS_V1)
        elif a.levels.lower() == "v2": post11.LEVELS.update(post11.LEVELS_V2)
        else: post11.set_levels(**{k.strip().upper(): float(v) for k, v in (kv.split("=") for kv in a.levels.split(","))})
        print("levels:", post11.LEVELS, flush=True)
    F = stage.Stage(a.tier, W, H, threads=a.threads, spp=a.spp or None)
    cur = None
    log_p = os.path.join(base, "log_%d.jsonl" % wi)
    os.makedirs(base, exist_ok=True)
    t_all = time.time()
    for n, (g, sid, d, name) in enumerate(todo):
        os.makedirs(d, exist_ok=True)
        if sid != cur:
            mod = shot_module(sid)
            F.begin(mod); cur = sid
        r0 = resource.getrusage(resource.RUSAGE_SELF); w0 = time.time()
        post = F.frame(mod, g); w_stage = time.time() - w0
        gl = post.get("_glare")
        heads = {}                                          # head centre (x, y in frame fractions, y down) and radius / W of every visible principal
        for a_ in F.cast:
            if a_.visible and a_.posed:
                x_, y_, z_ = F.screen(a_.head())
                if z_ > 0.05: heads[a_.name] = [round(x_, 3), round(y_, 3), round(0.5 * a_.a.sc * F.cam.data.lens / 36.0 / z_ * max(W, H) / W, 3), a_.pidx]
        out = os.path.join(d, name)
        spp_shot = getattr(mod, "SPP", {}).get(a.tier)
        if spp_shot and not a.spp: F.sc.cycles.samples = spp_shot
        r = F.render(out, g, post)
        r1 = resource.getrusage(resource.RUSAGE_SELF)
        cpu = (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime)
        if not a.keep:
            for suf in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_shafts.pkl", "_info.json", "_raw.png"):
                p = out + suf
                if os.path.exists(p): os.remove(p)
        rec = dict(g=g, shot=sid, pct=F.pct, stage=round(w_stage, 2), wall_render=r.get("wall_render"), cpu=round(cpu, 2), wall=round(time.time() - w0, 2), cpu_render=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"),
                   heads=heads, glare=[list(x) for x in gl] if gl else [])
        open(log_p, "a").write(json.dumps(rec) + "\n")
        print("FRAME %s g=%d %d/%d cpu %.1f wall %.1f (stage %.1f render %s post %s) glare %s" % (sid, g, n + 1, len(todo), cpu, rec["wall"], w_stage, r.get("wall_render"), r.get("cpu_post"), gl or "-"), flush=True)
    print("done %d frames in %.0f s" % (len(todo), time.time() - t_all), flush=True)


if __name__ == "__main__":
    main()
