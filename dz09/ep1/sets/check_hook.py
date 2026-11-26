"""check_hook.py -- is a world box inside any hook camera's frame?  (numpy only; frustum test without occlusion, so a
"visible" answer is conservative: the box may still be hidden behind a car.)

    import check_hook as CH
    CH.seen(box_min, box_max) -> [(shot, g, frame-fraction box (x0, y0, x1, y1), nearest depth D, size as a fraction of frame height)]
    python3 check_hook.py           the table for every EP.1 dressing box in out/dress_boxes.json
"""
import os, json, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
CAMS = None


def cams():
    global CAMS
    if CAMS is None: CAMS = json.load(open(os.path.join(HERE, "out", "hook_cams.json")))
    return CAMS


def project(c, pts, W=720, H=1280):
    M = np.array(c["M"]); Mi = np.linalg.inv(M)
    p = (Mi @ np.c_[pts, np.ones(len(pts))].T).T[:, :3]
    z = -p[:, 2]
    f = c["lens"] / 36.0 * max(W, H)                    # 36 mm on the long side
    x = p[:, 0] / np.maximum(z, 1e-6) * f / W + 0.5
    y = 0.5 - p[:, 1] / np.maximum(z, 1e-6) * f / H
    return x, y, z


def seen(bmin, bmax, margin=0.0):
    bmin = np.array(bmin, float); bmax = np.array(bmax, float)
    n = 5
    g = np.array([[bmin[0] + (bmax[0] - bmin[0]) * i / (n - 1), bmin[1] + (bmax[1] - bmin[1]) * j / (n - 1), bmin[2] + (bmax[2] - bmin[2]) * k / (n - 1)]
                  for i in range(n) for j in range(n) for k in range(n)])
    out = []
    for c in cams():
        x, y, z = project(c, g)
        ok = (z > 0.1) & (x > -margin) & (x < 1 + margin) & (y > -margin) & (y < 1 + margin)
        if ok.any():
            zz = z > 0.1
            out.append((c["shot"], c["g"], (round(float(x[ok].min()), 2), round(float(y[ok].min()), 2), round(float(x[ok].max()), 2), round(float(y[ok].max()), 2)),
                        round(float(z[ok].min()), 1), round(float(y[zz].max() - y[zz].min()), 3)))
    return out


if __name__ == "__main__":
    p = os.path.join(HERE, "out", "dress_boxes.json")
    boxes = json.load(open(p)) if os.path.exists(p) else {}
    for a in sys.argv[1:]:
        v = [float(x) for x in a.split(",")]; boxes[a] = [v[:3], v[3:]]
    rows = []
    for name, (b0, b1) in boxes.items():
        s = seen(b0, b1)
        print("%-18s %s" % (name, "never in a hook frame" if not s else ""))
        for r in s: print("    ", r)
        rows.append(dict(name=name, box=[b0, b1], seen=[list(map(str, r)) for r in s]))
    json.dump(rows, open(os.path.join(HERE, "out", "hook_check.json"), "w"), indent=1)
