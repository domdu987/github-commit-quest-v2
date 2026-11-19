#!/usr/bin/env python3
"""qa_motion.py -- camera statistics from the true camera path (no rendering).

    python3 qa_motion.py [out.json]

Per output frame g: corner speed (px per frame, the largest displacement the camera gives a frame corner, from the
similarity fitted to projected set points, post.camera_motion), zoom rate (percent per second) and pan.  From that:
  moves           runs of frames faster than MOVE px per frame (snap pushes, the pull-out, the whip): start, peak, end
  static          runs of frames slower than STATIC px per frame (the rule: never more than 6)
  constant speed  runs where the speed changes by less than 2 percent per frame while moving (a linear move)
  per shot        camera height above the floor and pitch (range), from the camera position and aim of every frame
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np

MOVE = 12.0
STATIC = 0.25


def runs(flags):
    out, s = [], None
    for i, f in enumerate(flags):
        if f and s is None:
            s = i
        if (not f) and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, len(flags) - 1))
    return out


def main(argv):
    import film, post
    rows = []
    for take, (g0, g1) in sorted(film.TAKES.items()):
        cam_fn = film.cam_a if take == "A" else film.cam_b
        fn = lambda g: tuple(tuple(v) for v in cam_fn(g))
        for g in range(g0, g1 + 1):
            M1, speed = post.camera_motion(fn, g, g0, g1)
            loc, look = cam_fn(g)
            v = look - loc
            rows.append(dict(g=g, take=take, speed=speed, zoom_pct_s=(float(np.hypot(M1[0, 0], M1[1, 0])) - 1) * 30 * 100,
                             height=loc.z, pitch=math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))),
                             yaw=math.degrees(math.atan2(v.x, v.y)), loc=[round(c, 3) for c in loc]))
    sp = np.array([r["speed"] for r in rows])
    cut = film.G3
    moves = []
    for a, b in runs(sp > MOVE):
        seg = sp[a:b + 1]
        pk = a + int(np.argmax(seg))
        moves.append(dict(start=a, peak=pk, end=b, start_s=round(a / 30.0, 3), peak_s=round(pk / 30.0, 3), end_s=round((b + 1) / 30.0, 3),
                          peak_px=round(float(seg.max()), 1), mean_px=round(float(seg.mean()), 1), contains_cut=bool(a < cut <= b)))
    static = [(a, b) for a, b in runs(sp < STATIC)]
    # constant-speed (linear) runs, measured inside each take, only while the camera is clearly moving
    lin_runs = []
    for take, (g0, g1) in sorted(film.TAKES.items()):
        s = sp[g0:g1 + 1]
        rel = np.abs(np.diff(s)) / np.maximum(s[:-1], 1e-6)
        for a, b in runs((rel < 0.02) & (s[:-1] > 1.0)):
            lin_runs.append((g0 + a, g0 + b + 1))
    shots = {"shot1": (0, film.G2), "shot2": (film.PULL[1], film.G3 - 1), "shot3": (film.G3 + 6, film.N - 1)}
    per = {}
    for n, (a, b) in shots.items():
        rs = [r for r in rows if a <= r["g"] <= b]
        per[n] = dict(frames=[a, b], height=[round(min(r["height"] for r in rs), 2), round(max(r["height"] for r in rs), 2)],
                      pitch=[round(min(r["pitch"] for r in rs), 1), round(max(r["pitch"] for r in rs), 1)],
                      yaw=[round(min(r["yaw"] for r in rs), 1), round(max(r["yaw"] for r in rs), 1)],
                      speed_px=[round(min(r["speed"] for r in rs), 2), round(float(np.median([r["speed"] for r in rs])), 2), round(max(r["speed"] for r in rs), 2)])
    out = dict(moves=moves, cut=cut, cut_s=round(cut / 30.0, 3), static_runs=static, longest_static=max([b - a + 1 for a, b in static] or [0]),
               slowest_px=round(float(sp.min()), 3), linear_runs=lin_runs, longest_linear=max([b - a + 1 for a, b in lin_runs] or [0]),
               per_shot=per, rows=rows)
    if argv:
        json.dump(out, open(argv[0], "w"), indent=0)
    for m in moves:
        print("move g %3d-%3d  %.2f-%.2f s  peak g %3d (%.2f s) %.0f px/frame, peak/mean %.2f%s" % (m["start"], m["end"], m["start_s"], m["end_s"], m["peak"], m["peak_s"], m["peak_px"], m["peak_px"] / m["mean_px"], "  CUT inside" if m["contains_cut"] else ""))
    print("static runs (< %.2f px/frame):" % STATIC, static, " slowest frame %.3f px" % sp.min())
    print("constant-speed runs:", lin_runs)
    for n, d in per.items():
        print(n, d)
    return out


if __name__ == "__main__":
    main(sys.argv[1:])
