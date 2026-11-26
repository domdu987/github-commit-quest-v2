"""run_ep.py -- render a scene of EP.1: any shots / frame range, any tier and size, resumable, in parallel workers.

    python3 run_ep.py --scene sc02 --tier draft --size 360x640 --spawn 2          supervisor: 2 workers, restarts dead ones
    python3 run_ep.py --scene sc02 --tier final --size 720x1280 --worker 1/4      one worker by hand (--threads 1)
    python3 run_ep.py --scene sc02 --shots S025,S026                              whole shots
    python3 run_ep.py --scene sc02 --frames 120:180                               scene-local frames (end exclusive)
    python3 run_ep.py --scene sc02 --shots S031 --at 0.5 --tag look               stills -> <out>/stills_look/
    python3 run_ep.py --scene sc02 --status [--tier .. --size ..]                 what is done, CPU per shot; writes manifests
    options: --every N  --force  --keep (EXR passes)  --pct N  --spp N  --levels RAIN=0.2,...  --block 6  --order class|cut
             --keep-stale (do not purge frames whose code or timing changed)  --quick (resume check = file exists only)
             --max-frames N (stop after N frames: for tests)   --no-nice

Frames:  OUT/<tier>_<W>x<H>/<scene>/<SHOT>/f_####.png   (#### = frame in the shot + 1; f_####_depth.png beside it)
Logs:    OUT/<tier>_<W>x<H>/<scene>/log_<worker>.jsonl  one line per frame (cpu = CPU seconds of this process and its
         children for the frame), sig.json + manifest.json per shot, logs/worker_<i>.log from the supervisor.
Render class (cut table or the module's CLASS): final tier A = 100 %, B = 75 %, C2 = 75 % and 4 spp; draft = the tier's
own scale for all; C1 = the module's draw(ctx), no Cycles and no Blender in the process unless a 3D shot follows.
Order: C1 first, then B / C2, then A (so the expensive frames are the ones a lost night loses last).
Resume: a frame is done when its PNG opens and has the asked size; PNGs are written under a temporary name and renamed;
a shot whose module, base code, length or looked-up words / mouth values changed is purged and rendered again.
"""
import os, sys, json, time, argparse, resource, glob, fcntl, subprocess, signal
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import epcommon as E

FPS = E.FPS


# ------------------------------------------------------------------------------------------------ bookkeeping
class Lock:
    def __init__(self, d):
        os.makedirs(d, exist_ok=True); self.p = os.path.join(d, ".lock")
    def __enter__(self):
        self.f = open(self.p, "w"); fcntl.flock(self.f, fcntl.LOCK_EX); return self
    def __exit__(self, *a):
        fcntl.flock(self.f, fcntl.LOCK_UN); self.f.close()


def png_ok(p, W, H, quick=False):
    if not os.path.exists(p): return False
    if quick: return os.path.getsize(p) > 0
    try:
        from PIL import Image
        im = Image.open(p)
        if im.size != (W, H): return False
        im.verify()
        return True
    except Exception:
        return False


def dep_now(S, row, key):
    """current value of a recorded dependency, relative to the shot (seconds from its first frame, or a mouth level)."""
    kind, rest = key.split(":", 1)
    t_shot = row["f0"] / float(FPS)
    try:
        if kind == "word":
            sid, r2 = rest.split(":", 1)
            text, n, end = r2.rsplit(":", 2)
            hits = [c for c in S.caps if c["text"] == text and (not sid or c["id"] == sid)]
            c = hits[min(int(n), len(hits) - 1)]
            return round((c["t1"] if int(end) else c["t0"]) - t_shot, 4)
        if kind == "cue":
            return round(float(S.cues[rest]) - t_shot, 4)
        if kind == "mouth":
            who, kk = rest.split(":")
            saved = dict(S.deps)
            v = S.mouth(who, S.g_base + row["f0"] + int(kk))
            S.deps.clear(); S.deps.update(saved)
            return v
    except Exception:
        return None
    return None


def deps_rel(S, row):
    """S.deps (scene seconds / scene-local frames) -> shot-relative, the form stored in sig.json."""
    out = {}
    for k, v in S.deps.items():
        if k.startswith("mouth:"):
            _m, who, kk = k.split(":")
            out["mouth:%s:%d" % (who, int(kk) - row["f0"])] = v
        else:
            out[k] = round(v - row["f0"] / float(FPS), 4)
    return out


def static_sig(mod, row, a, W, H):
    cl = getattr(mod, "CLASS", row["cls"])
    return dict(code=E.code_hash(mod), frames=row["f1"] - row["f0"], cls=cl, tier=a.tier, size=[W, H],
                pct=a.pct or getattr(mod, "PCT", {}).get(a.tier, "tier"), spp=a.spp or getattr(mod, "SPP", {}).get(a.tier, "tier"), levels=a.levels)


def check_sig(S, mod, row, d, a, W, H):
    """under the shot's lock: purge the shot's frames when its signature or a recorded dependency changed.  Returns why."""
    sig_p = os.path.join(d, "sig.json")
    cur = static_sig(mod, row, a, W, H)
    with Lock(d):
        old = json.load(open(sig_p)) if os.path.exists(sig_p) else None
        why = ""
        if old is not None:
            diff = [k for k in cur if old.get("static", {}).get(k) != cur[k]]
            if diff: why = "changed: " + ", ".join(diff)
            elif old.get("f0", row["f0"]) != row["f0"] and not all(
                    png_ok(os.path.join(d, E.frame_name(k) + ".png"), W, H, True) for k in range(row["f1"] - row["f0"])):
                # the shot moved in the scene, so its stage clock t moved (hand-held shake, on-twos phase, blinks, rain):
                # a COMPLETE shot stays consistent with itself and is kept; a partly rendered one would jump where the new frames start
                why = "shot start moved %d -> %d while incomplete" % (old.get("f0"), row["f0"])
            else:
                moved = [k for k, v in old.get("deps", {}).items() if dep_now(S, row, k) != v]
                if moved: why = "timing moved: %s%s" % (moved[0], " (+%d more)" % (len(moved) - 1) if len(moved) > 1 else "")
        if why and a.keep_stale:
            return "STALE kept (%s)" % why
        if why:
            n = 0
            for p in glob.glob(os.path.join(d, "f_*.png")) + glob.glob(os.path.join(d, ".tmp_*")):
                os.remove(p); n += 1
            print("STALE %s: %s -> purged %d files" % (row["id"], why, n), flush=True)
            old = None
        if old is None:
            json.dump(dict(static=cur, deps={}, f0=row["f0"], t=time.time()), open(sig_p, "w"), ensure_ascii=False)
        return why


def add_deps(S, row, d):
    new = deps_rel(S, row)
    sig_p = os.path.join(d, "sig.json")
    with Lock(d):
        sg = json.load(open(sig_p))
        if any(sg["deps"].get(k) != v for k, v in new.items()):
            sg["deps"].update(new)
            tmp = sig_p + ".tmp%d" % os.getpid()
            json.dump(sg, open(tmp, "w"), ensure_ascii=False); os.replace(tmp, sig_p)


def pid_alive(pid):
    try:
        os.kill(int(pid), 0); return True
    except (OSError, ValueError):
        return False


_HELD = []


def hold_lock(path):
    """take an exclusive lock for the life of this process (the kernel drops it when the process dies, however it dies).
    Returns None when it is ours, else the pid written by the process that holds it."""
    f = open(path, "a+")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        f.seek(0); who = f.read().strip() or "?"
        f.close(); return who
    f.seek(0); f.truncate(); f.write(str(os.getpid())); f.flush()
    _HELD.append(f)
    return None


def live_workers(base):
    """pids of render workers still alive on this output folder (they hold .worker_*.lock)."""
    out = []
    for p in sorted(glob.glob(os.path.join(base, ".worker_*.lock"))):
        f = open(p, "a+")
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB); fcntl.flock(f, fcntl.LOCK_UN)
        except OSError:
            f.seek(0); out.append((os.path.basename(p), f.read().strip() or "?"))
        f.close()
    return out


def cpu_now():
    r = resource.getrusage(resource.RUSAGE_SELF); c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime + c.ru_utime + c.ru_stime


def read_logs(base):
    last = {}
    for p in sorted(glob.glob(os.path.join(base, "log_*.jsonl"))):
        for l in open(p):
            try: r = json.loads(l)
            except Exception: continue
            if "tag" in r: continue
            last[(r["shot"], r["k"])] = r
    return last


def status(S, a, W, H, write=True):
    base = E.out_dir(a.tier, W, H, S.name)
    logs = read_logs(base)
    tot = dict(frames=0, done=0, cpu=0.0)
    rows = []
    for row in S.shots:
        d = os.path.join(base, row["id"]); n = row["f1"] - row["f0"]
        done = [k for k in range(n) if png_ok(os.path.join(d, E.frame_name(k) + ".png"), W, H, a.quick)]
        recs = [logs[(row["id"], k)] for k in done if (row["id"], k) in logs]
        cpu = sum(r["cpu"] for r in recs)
        has_mod = E.find_shot_file(S.name, row["id"]) is not None
        m = dict(scene=S.name, shot=row["id"], cls=row["cls"], f0=row["f0"], f1=row["f1"], frames=n, done=len(done), complete=len(done) == n,
                 missing=[k for k in range(n) if k not in set(done)][:50], cpu_s=round(cpu, 1), cpu_s_per_frame=round(cpu / len(recs), 2) if recs else None,
                 wall_s=round(sum(r["wall"] for r in recs), 1), logged=len(recs), module=has_mod, tier=a.tier, size=[W, H], updated=time.strftime("%Y-%m-%d %H:%M:%S"))
        if os.path.exists(os.path.join(d, "sig.json")):
            m["sig"] = json.load(open(os.path.join(d, "sig.json")))["static"]
        if write and os.path.isdir(d):
            json.dump(m, open(os.path.join(d, "manifest.json"), "w"), ensure_ascii=False, indent=1)
        rows.append(m); tot["frames"] += n; tot["done"] += len(done); tot["cpu"] += cpu
    print("%s %s %dx%d: %d / %d frames, %.0f CPU s logged" % (S.name, a.tier, W, H, tot["done"], tot["frames"], tot["cpu"]))
    for m in rows:
        print("  %s %-2s %4d/%-4d %s cpu/frame %s%s" % (m["shot"], m["cls"], m["done"], m["frames"], "done   " if m["complete"] else "MISSING",
                                                      m["cpu_s_per_frame"], "" if m["module"] else "   (no module yet)"))
    if write:
        os.makedirs(base, exist_ok=True)
        json.dump(dict(scene=S.name, tier=a.tier, size=[W, H], frames=tot["frames"], done=tot["done"], cpu_s=round(tot["cpu"], 1), shots=rows),
                  open(os.path.join(base, "manifest.json"), "w"), ensure_ascii=False, indent=1)
    return tot["done"] == tot["frames"], rows


# ------------------------------------------------------------------------------------------------ supervisor
def spawn(a, argv):
    n = a.spawn
    S = E.activate(a.scene)
    W, H = [int(x) for x in a.size.lower().split("x")]
    base = E.out_dir(a.tier, W, H, S.name); os.makedirs(os.path.join(base, "logs"), exist_ok=True)
    rest = []
    skip = False
    for x in argv:
        if skip: skip = False; continue
        if x in ("--spawn", "--worker"): skip = True; continue
        rest.append(x)
    procs = {}; restarts = {i: 0 for i in range(n)}
    who = hold_lock(os.path.join(base, ".supervisor.lock"))
    if who:
        print("another supervisor (pid %s) is rendering %s: nothing started" % (who, base), flush=True); sys.exit(4)
    lw = live_workers(base)
    if lw:
        # a supervisor that was killed leaves its workers rendering (they are their own sessions): starting more would render every frame twice
        print("workers of an earlier run are still rendering %s: %s\n  wait for them (run --status), or kill those pids, then start again" % (
            base, ", ".join("%s pid %s" % x for x in lw)), flush=True)
        sys.exit(4)

    def start(i):
        lf = open(os.path.join(base, "logs", "worker_%d.log" % i), "a")
        cmd = ([] if a.no_nice else ["nice", "-n", "10"]) + [sys.executable, os.path.abspath(__file__)] + rest + ["--worker", "%d/%d" % (i, n)]
        procs[i] = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        print("worker %d/%d pid %d%s" % (i, n, procs[i].pid, " (restart %d)" % restarts[i] if restarts[i] else ""), flush=True)

    def stop(*_):
        for p in procs.values():
            try: os.killpg(p.pid, signal.SIGTERM)
            except Exception: pass
        sys.exit(1)

    signal.signal(signal.SIGTERM, stop); signal.signal(signal.SIGINT, stop)
    for i in range(n): start(i)
    alive = set(range(n)); failed = False
    while alive:
        time.sleep(2.0)
        for i in list(alive):
            rc = procs[i].poll()
            if rc is None: continue
            if rc != 0 and rc != 4 and restarts[i] < a.restarts:
                restarts[i] += 1; print("worker %d died (rc %s)" % (i, rc), flush=True); start(i)
            else:
                alive.discard(i); failed |= rc != 0
                print("worker %d ended rc %s" % (i, rc), flush=True)
    ok, _ = status(S, a, W, H)
    print("spawn finished: %s, restarts %s" % ("complete" if ok else "INCOMPLETE", restarts), flush=True)
    sys.exit(0 if ok and not failed else 2)


# ------------------------------------------------------------------------------------------------ worker
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True); ap.add_argument("--shots", default=""); ap.add_argument("--frames", default="")
    ap.add_argument("--tier", default="draft"); ap.add_argument("--size", default="360x640")
    ap.add_argument("--threads", type=int, default=1); ap.add_argument("--every", type=int, default=1)
    ap.add_argument("--worker", default="0/1"); ap.add_argument("--spawn", type=int, default=0); ap.add_argument("--restarts", type=int, default=3)
    ap.add_argument("--force", action="store_true"); ap.add_argument("--keep", action="store_true"); ap.add_argument("--keep-stale", action="store_true")
    ap.add_argument("--quick", action="store_true"); ap.add_argument("--status", action="store_true"); ap.add_argument("--no-nice", action="store_true")
    ap.add_argument("--at", default=""); ap.add_argument("--tag", default=""); ap.add_argument("--spp", type=int, default=0); ap.add_argument("--pct", type=int, default=0)
    ap.add_argument("--levels", default=""); ap.add_argument("--block", type=int, default=6); ap.add_argument("--order", default="class")
    ap.add_argument("--loc", default=""); ap.add_argument("--max-frames", type=int, default=0)
    a = ap.parse_args()
    if a.spawn:
        return spawn(a, sys.argv[1:])
    S = E.activate(a.scene)
    W, H = [int(x) for x in a.size.lower().split("x")]
    if a.status:
        status(S, a, W, H); return
    base = E.out_dir(a.tier, W, H, S.name)
    wi, wn = [int(x) for x in a.worker.split("/")]
    stills = bool(a.at) or bool(a.tag)
    # ---- which frames
    want = []                                               # (row, k)
    rows = [S.shot(x) for x in a.shots.split(",")] if a.shots else list(S.shots)
    if a.frames:
        for part in a.frames.split(","):
            x, y = part.split(":") if ":" in part else (part, int(part) + 1)
            for k in range(int(x), int(y)):
                r = S.shot_at(k); want.append((r, k - r["f0"]))
    else:
        for r in rows:
            n = r["f1"] - r["f0"]
            ks = [min(n - 1, int(round(float(u) * (n - 1)))) for u in a.at.split(",")] if a.at else range(n)
            want += [(r, k) for k in ks]
    want = sorted(set((r["id"], k) for r, k in want))[::a.every]
    if not stills:
        want = [(sid, k) for sid, k in want if ((S.by_id[sid]["f0"] + k) // a.block) % wn == wi]
    # ---- modules, signatures, what is left
    mods, todo, nomod = {}, [], []
    for sid in sorted(set(s for s, _ in want)):
        m = E.load_shot(S.name, sid, a.tier)
        if m is None: nomod.append(sid); continue
        mods[sid] = m
        if not stills:
            check_sig(S, m, S.by_id[sid], os.path.join(base, sid), a, W, H)
    if nomod:
        print("no shot module yet for: %s" % ",".join(nomod), flush=True)
    for sid, k in want:
        if sid not in mods: continue
        d = os.path.join(base, "stills" + (("_" + a.tag) if a.tag else "")) if stills else os.path.join(base, sid)
        name = ("%s_%s" % (sid, E.frame_name(k))) if stills else E.frame_name(k)
        if a.force or not png_ok(os.path.join(d, name + ".png"), W, H, a.quick):
            todo.append((sid, k, d, name))
    import stage_ep                                         # light: registries only, no bpy
    lkey = lambda m: stage_ep.ALIASES.get(m.LOC, m.LOC)     # two keys of one stage (X1 / X1s) share a Blender process
    if a.loc:
        todo = [x for x in todo if mods[x[0]].CLASS != "C1" and lkey(mods[x[0]]) == a.loc]
    order = (lambda x: (E.CLASSES[mods[x[0]].CLASS]["order"], S.by_id[x[0]]["f0"], x[1])) if a.order == "class" else (lambda x: (S.by_id[x[0]]["f0"], x[1]))
    todo.sort(key=order)
    if a.max_frames: todo = todo[:a.max_frames]
    print("%s worker %d/%d: frames to render %d of %d" % (S.name, wi, wn, len(todo), len(want)), flush=True)
    if not todo:
        return
    os.makedirs(base, exist_ok=True)
    log_p = os.path.join(base, "log_%d.jsonl" % wi)
    if not stills and not a.loc:
        # one live worker per slot i/n of an output folder: a second one would render the same frames
        who = hold_lock(os.path.join(base, ".worker_%dof%d.lock" % (wi, wn)))
        if who:
            print("worker %d/%d is already rendering this folder (pid %s): not started" % (wi, wn, who), flush=True); sys.exit(4)
    for sid in mods:                                        # half-written files of DEAD processes only (the pid is in the name)
        for p in glob.glob(os.path.join(base, sid, ".tmp_w*")):
            pid = os.path.basename(p).split("_")[2].lstrip("p")
            if not pid_alive(pid):
                try: os.remove(p)
                except OSError: pass
    locs = sorted(set(lkey(mods[x[0]]) for x in todo if mods[x[0]].CLASS != "C1"))
    if len(locs) > 1 and not a.loc:
        # one location per Blender process: the drawn frames here, then one child per location
        for loc in [None] + locs:
            if loc is None:
                if any(mods[x[0]].CLASS == "C1" for x in todo): render(S, a, W, H, base, [x for x in todo if mods[x[0]].CLASS == "C1"], mods, wi, log_p, stills)
                continue
            rc = subprocess.call([sys.executable, os.path.abspath(__file__)] + sys.argv[1:] + ["--loc", loc])
            if rc: sys.exit(rc)
        return
    render(S, a, W, H, base, todo, mods, wi, log_p, stills)


def render(S, a, W, H, base, todo, mods, wi, log_p, stills):
    t_all = time.time(); F = None; cur = None; n_all = len(todo)
    for n, (sid, k, d, name) in enumerate(todo):
        mod = mods[sid]; row = S.by_id[sid]
        os.makedirs(d, exist_ok=True)
        g = S.g_base + row["f0"] + k
        tmp = os.path.join(d, ".tmp_w%d_p%d_%s" % (wi, os.getpid(), name)); out = os.path.join(d, name)
        c0 = cpu_now(); w0 = time.time()
        if sid != cur: S.deps.clear()
        rec = dict(scene=S.name, shot=sid, k=k, local=row["f0"] + k, g=g, cls=mod.CLASS, worker=wi)
        if stills: rec["tag"] = a.tag or "at"
        if mod.CLASS == "C1":
            import ep2d
            ctx = ep2d.Ctx(S, row, k, W, H, a.tier, base)
            im = mod.draw(ctx)
            if not hasattr(im, "save"):
                from PIL import Image
                im = Image.fromarray(im)
            if im.size != (W, H): im = im.resize((W, H))
            im.convert("RGB").save(tmp + ".png", compress_level=3)
            os.replace(tmp + ".png", out + ".png")
            cur = sid
            rec.update(pct=None, stage=0.0, cpu=round(cpu_now() - c0, 2), wall=round(time.time() - w0, 2))
        else:
            if F is None:
                import stage_ep
                cast = sorted(set(c for x in todo for c in getattr(mods[x[0]], "CAST", []) if mods[x[0]].CLASS != "C1"))
                if a.levels:
                    import stage  # noqa: puts v11/set on sys.path
                    import post11
                    post11.set_levels(**{kk.strip().upper(): float(v) for kk, v in (kv.split("=") for kv in a.levels.split(","))})
                    print("levels:", post11.LEVELS, flush=True)
                c_b = cpu_now(); w_b = time.time()
                F = stage_ep.build(mod.LOC, a.tier, W, H, threads=a.threads, spp=a.spp or None, cast=cast, pct=a.pct)
                open(log_p, "a").write(json.dumps(dict(scene=S.name, shot="_build", k=0, tag="build", loc=mod.LOC, cpu=round(cpu_now() - c_b, 2),
                                                       wall=round(time.time() - w_b, 2), worker=wi)) + "\n")
                c0 = cpu_now(); w0 = time.time()
            if sid != cur:
                F.begin(mod); cur = sid
            post = F.frame(mod, g); w_stage = time.time() - w0
            gl = post.get("_glare")
            heads = {}
            for a_ in F.cast:
                if a_.visible and a_.posed:
                    x_, y_, z_ = F.screen(a_.head())
                    if z_ > 0.05: heads[a_.name] = [round(x_, 3), round(y_, 3), round(0.5 * a_.a.sc * F.cam.data.lens / 36.0 / z_ * max(W, H) / W, 3), a_.pidx]
            spp_shot = getattr(mod, "SPP", {}).get(a.tier)
            if spp_shot and not a.spp: F.sc.cycles.samples = spp_shot
            r = F.render(tmp, g, post)
            if not a.keep:
                for suf in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_shafts.pkl", "_info.json", "_raw.png"):
                    if os.path.exists(tmp + suf): os.remove(tmp + suf)
            else:
                for suf in ("_rgb.exr", "_z.exr", "_idx.exr", "_env.exr", "_shafts.pkl", "_info.json", "_raw.png"):
                    if os.path.exists(tmp + suf): os.replace(tmp + suf, out + suf)
            if os.path.exists(tmp + "_depth.png"): os.replace(tmp + "_depth.png", out + "_depth.png")
            os.replace(tmp + ".png", out + ".png")          # the frame exists only once it is whole
            rec.update(pct=F.pct, spp=F.sc.cycles.samples, stage=round(w_stage, 2), wall_render=r.get("wall_render"), cpu=round(cpu_now() - c0, 2),
                       wall=round(time.time() - w0, 2), cpu_render=r.get("cpu_render_total"), cpu_post=r.get("cpu_post"), heads=heads,
                       glare=[list(x) for x in gl] if gl else [])
        if not stills: add_deps(S, row, d)
        open(log_p, "a").write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("FRAME %s %s k=%d (scene f %d) %d/%d cpu %.1f wall %.1f" % (S.name, sid, k, row["f0"] + k, n + 1, n_all, rec["cpu"], rec["wall"]), flush=True)
    print("done %d frames in %.0f s" % (n_all, time.time() - t_all), flush=True)


if __name__ == "__main__":
    main()
