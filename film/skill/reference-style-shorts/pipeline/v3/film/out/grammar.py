#!/usr/bin/env python3
"""grammar.py -- recount the plan's grammar on the conformed film (out/frames), with the thresholds and run logic of
PROJ/v3/shots/qa_motion.py (MOVE 12 px/frame, STATIC 0.25 px/frame) and the pop rule of popcheck.py.

The hook's qa_motion works from the Blender camera path, which the conformed film does not have; here the camera motion
of every frame pair is fitted from the PICTURE (LK feature tracks + RANSAC similarity on 360x640 copies), and the
corner speed is the largest displacement that similarity gives a frame corner, in 720x1280 px, as in qa_motion.
Frame pairs across a join (cut, wipe, flash, dissolve) are not fitted.
    python3 grammar.py        -> work/grammar.json and a printed summary
"""
import json, os, sys
import numpy as np
import cv2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "shots"))
from qa_motion import runs, MOVE, STATIC  # noqa: E402

FR = os.path.join(HERE, "frames")
S = 0.5


def gray(g):
    im = cv2.imread(os.path.join(FR, "g_%04d.png" % g), cv2.IMREAD_GRAYSCALE)
    return cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)


def fit(g):
    a, b = gray(g - 1), gray(g)
    pts = cv2.goodFeaturesToTrack(a, 500, 0.005, 8)
    if pts is None or len(pts) < 10:
        return None
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(a, b, pts, None, winSize=(21, 21), maxLevel=4)
    ok = st.ravel() == 1
    if ok.sum() < 10:
        return None
    M, inl = cv2.estimateAffinePartial2D(pts[ok], nxt[ok], method=cv2.RANSAC, ransacReprojThreshold=1.5)
    if M is None:
        return None
    corners = np.array([[0, 0], [359, 0], [0, 639], [359, 639]], np.float32)
    moved = corners @ M[:, :2].T + M[:, 2]
    speed = float(np.linalg.norm(moved - corners, axis=1).max()) / S
    zoom = float(np.hypot(M[0, 0], M[1, 0]))
    return dict(g=g, speed=round(speed, 3), zoom_pct_s=round((zoom - 1) * 30 * 100, 2), inliers=int(inl.sum()) if inl is not None else 0)


def main():
    J = json.load(open(os.path.join(HERE, "work", "joins.json")))
    joins = J["joins"]
    skip = set()
    for j in joins:
        a, b = j["range"]
        for g in range(a, b + 2):
            skip.add(g)
    from multiprocessing import Pool
    gs = [g for g in range(1, 1965) if g not in skip]
    with Pool(3) as P:
        rows = [r for r in P.map(fit, gs, chunksize=20) if r]
    sp = {r["g"]: r["speed"] for r in rows}
    # speed per frame, joins filled with NaN
    arr = np.array([sp.get(g, np.nan) for g in range(1965)])
    filled = np.where(np.isnan(arr), 0.0, arr)
    moves = []
    for a, b in runs(list((filled > MOVE))):
        seg = filled[a:b + 1]
        pk = a + int(np.argmax(seg))
        moves.append(dict(start=a, end=b, peak=pk, start_s=round(a / 30, 2), end_s=round((b + 1) / 30, 2), peak_s=round(pk / 30, 2),
                          peak_px=round(float(seg.max()), 1), frames=b - a + 1))
    valid = ~np.isnan(arr)
    static = [(a, b) for a, b in runs(list(valid & (filled < STATIC)))]
    # linear (constant speed) runs, as qa_motion: relative change < 2 % per frame while moving > 1 px/frame
    lin = []
    rel = np.abs(np.diff(filled)) / np.maximum(filled[:-1], 1e-6)
    for a, b in runs(list((rel < 0.02) & (filled[:-1] > 1.0) & valid[:-1] & valid[1:])):
        lin.append((a, b + 1))
    out = dict(rows=rows, moves=moves, static_runs=static, longest_static=max([b - a + 1 for a, b in static] or [0]),
               linear_runs=lin, longest_linear=max([b - a + 1 for a, b in lin] or [0]))
    json.dump(out, open(os.path.join(HERE, "work", "grammar.json"), "w"), indent=0)
    print("moves > %.0f px/frame:" % MOVE, len(moves))
    for m in moves:
        print("  g %4d-%4d  %.2f-%.2f s  peak %.0f px at %.2f s  (%d f)" % (m["start"], m["end"], m["start_s"], m["end_s"], m["peak_px"], m["peak_s"], m["frames"]))
    print("static runs:", static, "longest", out["longest_static"])
    print("linear runs:", lin, "longest", out["longest_linear"])


if __name__ == "__main__":
    main()
