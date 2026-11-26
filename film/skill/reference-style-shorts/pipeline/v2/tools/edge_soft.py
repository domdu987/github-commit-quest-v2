#!/usr/bin/env python3
"""edge_soft.py -- measure edge softness (10-90 percent rise width in px) of the strongest ink edges of a frame.
usage: python3 edge_soft.py img [img ...]      (measuring only: numpy + cv2)
For every strong, high-contrast edge pixel (white fill against ink) the luma profile is sampled along the gradient and
the distance between the 10 and 90 percent levels is taken; the median over all such edges is reported."""
import sys, numpy as np, cv2


def edge_width(path, cap_band=(840, 965), contrast=110, n=4000, seed=1):
    im = cv2.imread(path)
    if im is None:
        raise SystemExit("cannot read " + path)
    if im.shape[1] != 720:
        im = cv2.resize(im, (720, 1280), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    mag = np.hypot(gx, gy)
    mag[cap_band[0]:cap_band[1]] = 0            # the caption has its own edges
    mag[:8] = 0; mag[-8:] = 0; mag[:, :8] = 0; mag[:, -8:] = 0
    thr = np.percentile(mag, 99.0)
    ys, xs = np.where(mag >= thr)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(ys))[:n * 4]
    ws = []
    t = np.arange(-6, 6.01, 0.25, dtype=np.float32)
    for i in idx:
        y, x = ys[i], xs[i]
        m = mag[y, x]
        dx, dy = gx[y, x] / m, gy[y, x] / m
        px = (x + t * dx).astype(np.float32).reshape(1, -1)
        py = (y + t * dy).astype(np.float32).reshape(1, -1)
        prof = cv2.remap(g, px, py, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)[0]
        c = len(t) // 2
        # walk outwards from the centre while the profile keeps rising / falling: the two plateaus
        lo_i = c
        while lo_i > 0 and prof[lo_i - 1] < prof[lo_i] - 0.15: lo_i -= 1
        hi_i = c
        while hi_i < len(t) - 1 and prof[hi_i + 1] > prof[hi_i] + 0.15: hi_i += 1
        lo, hi = prof[lo_i], prof[hi_i]
        if hi - lo < contrast or hi < 200:      # white fill against ink only
            continue
        seg = prof[lo_i:hi_i + 1]
        ts = t[lo_i:hi_i + 1]
        a = np.interp(lo + 0.1 * (hi - lo), seg, ts)
        b = np.interp(lo + 0.9 * (hi - lo), seg, ts)
        ws.append(b - a)
        if len(ws) >= n:
            break
    ws = np.array(ws)
    lap = cv2.Laplacian(g, cv2.CV_32F)
    lap[cap_band[0]:cap_band[1]] = 0
    return dict(n=len(ws), w50=float(np.median(ws)) if len(ws) else float('nan'), w25=float(np.percentile(ws, 25)) if len(ws) else float('nan'),
                w75=float(np.percentile(ws, 75)) if len(ws) else float('nan'), gmax=float(np.percentile(mag, 99.9)), lap=float(lap.var()))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        r = edge_width(p)
        print("%-64s n=%5d  rise10-90 median %.2f px (q25 %.2f, q75 %.2f)  grad p99.9 %.1f  laplacian var %.0f" % (p[-64:], r["n"], r["w50"], r["w25"], r["w75"], r["gmax"], r["lap"]))
