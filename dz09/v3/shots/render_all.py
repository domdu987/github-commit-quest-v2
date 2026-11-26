#!/usr/bin/env python3
"""render_all.py -- render one take of the film, resumable.

    python3 render_all.py A|B <out_dir> [--scale 1.0] [--samples 16] [--threads 2] [--frames a:b[:step]] [--force]

Every finished frame g leaves two files: <out_dir>/f_%04d.png (number g + 1) and <out_dir>/meta/g_%04d.json (wall and CPU
seconds, camera, heads, registration, written only AFTER the PNG is complete).  A PNG without its json is a half-written
frame of an interrupted run: it is deleted and rendered again.  Run the two takes as two processes (2 threads each).
"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("take"); ap.add_argument("out")
    ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--threads", type=int, default=2); ap.add_argument("--frames", default=None)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    import film
    from probe import parse
    g0, g1 = film.TAKES[a.take]
    gs = [g for g in (parse(a.frames) if a.frames else range(g0, g1 + 1)) if g0 <= g <= g1]
    meta = os.path.join(a.out, "meta")
    os.makedirs(meta, exist_ok=True)
    png = lambda g: os.path.join(a.out, "f_%04d.png" % (g + 1))
    js = lambda g: os.path.join(meta, "g_%04d.json" % g)
    todo = []
    for g in gs:
        done = os.path.exists(png(g)) and os.path.exists(js(g)) and not a.force
        if done:
            try:
                m = json.load(open(js(g)))
                done = (m.get("timing_mtime") == film.T["mtime"] and m.get("scale") == a.scale and m.get("samples") == a.samples)
            except Exception:
                done = False
        if not done:
            for p in (png(g), js(g)):
                if os.path.exists(p):
                    os.remove(p)
            todo.append(g)
    print("render_all: take %s, %d frames to render, %d already finished" % (a.take, len(todo), len(gs) - len(todo)), flush=True)
    if not todo:
        return
    F = film.Film(a.take)
    t0 = time.time()
    F.pose(todo)
    print("render_all: %d frames posed and drawn in %.1f s" % (len(todo), time.time() - t0), flush=True)
    for g in todo:
        st = F.render([g], a.out, scale=a.scale, threads=a.threads, samples=a.samples, verbose=False)[0]
        rep = F.report(g)
        rep.update(wall=round(st["wall"], 3), cpu=round(st["cpu"], 3), scale=a.scale, samples=a.samples, threads=a.threads,
                   timing_mtime=film.T["mtime"], retried=st.get("retried"), still_wrong=st.get("still_wrong"), take=a.take)
        tmp = js(g) + ".tmp"
        json.dump(rep, open(tmp, "w"))
        os.replace(tmp, js(g))
        print("g %3d  %.2f s wall  %.2f s cpu%s" % (g, st["wall"], st["cpu"], "  RETRIED" if st.get("retried") else ""), flush=True)
    print("render_all: take %s finished in %.1f s" % (a.take, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
