#!/usr/bin/env python3
"""popcheck.py -- frame-to-frame change of a rendered sequence.  python3 popcheck.py <frames_dir> [n]
Prints the mean absolute difference between consecutive frames and flags a pop: a change larger than 1.8 times both
neighbours (the cut at film.G3 is expected)."""
import os, sys
import numpy as np
from PIL import Image


def diffs(d, n=None):
    fs = sorted(f for f in os.listdir(d) if f.startswith("f_") and f.endswith(".png"))
    if n:
        fs = fs[:n]
    prev, out = None, []
    for f in fs:
        a = np.asarray(Image.open(os.path.join(d, f)).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            out.append(float(np.abs(a - prev).mean()))
        prev = a
    return out


if __name__ == "__main__":
    d = sys.argv[1]
    ds = diffs(d, int(sys.argv[2]) if len(sys.argv) > 2 else None)
    pops = []
    for i, v in enumerate(ds):
        a = ds[i - 1] if i > 0 else v
        b = ds[i + 1] if i + 1 < len(ds) else v
        if v > 1.8 * a and v > 1.8 * b and v > 1.0:
            pops.append((i, i + 1, round(v, 2), round(a, 2), round(b, 2)))
    print(" ".join("%d:%.1f" % (i + 1, v) for i, v in enumerate(ds)))
    print("pops (g -> g+1, change, neighbours):", pops)
    still = [i for i, v in enumerate(ds) if v < 0.35]
    print("near-still transitions (change < 0.35 levels):", still)
