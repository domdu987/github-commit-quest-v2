#!/usr/bin/env python3
"""qa_trackend.py -- independent image check of the registration target: on the actor-free plates (raw/plate) the end
of the red track is found in the rendered pixels and compared with the pixel the pencil point was solved to (meta
"want" = the projected office3d.track_point(line)).  Prints, per plate frame, how far the red ink reaches beyond the
target along the track (px) and the sideways offset of the ink end from the target (px).

    python3 qa_trackend.py <raw_dir> [out.json]
"""
import glob, json, os, sys
import numpy as np
from PIL import Image


def main(argv):
    raw = argv[0]
    rows = []
    for p in sorted(glob.glob(os.path.join(raw, "plate", "f_*.png"))):
        g = int(os.path.basename(p)[2:6]) - 1
        m = json.load(open(os.path.join(raw, "meta", "g_%04d.json" % g)))
        if "reg" not in m or m["reg"]["who"] != "hero" or m["line"] >= 0.999 or m["line"] < 0.03:
            continue
        x0, y0 = m["reg"]["want"]
        a = np.asarray(Image.open(p).convert("RGB"), np.int16)
        red = (a[..., 0] > 150) & (a[..., 1] < 60) & (a[..., 2] < 60)
        ys, xs = np.where(red)
        d = np.hypot(xs - x0, ys - y0)
        near = d < 70
        if near.sum() < 30:
            continue
        pts = np.stack([xs[near] - x0, ys[near] - y0], 1).astype(float)
        c = pts.mean(0)
        u, s, vt = np.linalg.svd(pts - c, full_matrices=False)
        ax = vt[0]
        if ax @ c > 0:                       # the ink lies behind the end: the axis must point from the ink to the end
            ax = -ax
        along = pts @ ax
        side = pts @ np.array([-ax[1], ax[0]])
        tip = along > along.max() - 1.5      # the last 1.5 px of ink along the track
        width = float(np.percentile(side, 97) - np.percentile(side, 3))
        rows.append(dict(g=g, line=m["line"], beyond_px=round(float(along.max()), 2), side_px=round(float(side[tip].mean()), 2), ink_width_px=round(width, 1)))
    for r in rows:
        print(r)
    if rows:
        print("frames %d: ink end beyond the target %.2f px mean (%.2f to %.2f); sideways %.2f px mean abs (max %.2f)" % (
            len(rows), np.mean([r["beyond_px"] for r in rows]), min(r["beyond_px"] for r in rows), max(r["beyond_px"] for r in rows),
            np.mean([abs(r["side_px"]) for r in rows]), max(abs(r["side_px"]) for r in rows)))
    if len(argv) > 1:
        json.dump(rows, open(argv[1], "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
