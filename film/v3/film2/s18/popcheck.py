#!/usr/bin/env python3
"""popcheck.py [dir]: mean absolute difference (0-255) between consecutive final frames; lists frames above 3x the median."""
import os, sys, glob
import numpy as np
from PIL import Image
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
fs = sorted(glob.glob(os.path.join(d, "g_*.png")))
prev = None; out = []
for f in fs:
    a = np.asarray(Image.open(f).convert("L").resize((180, 320)), dtype=np.float32)
    if prev is not None:
        out.append((int(os.path.basename(f)[2:6]), float(np.abs(a - prev).mean())))
    prev = a
v = np.array([x for g, x in out]); med = float(np.median(v))
print("frame-to-frame mean abs diff: median %.2f, max %.2f (g %d)" % (med, v.max(), out[int(v.argmax())][0]))
print("above 3 x median:", [(g, round(x, 1)) for g, x in out if x > 3 * med] or "none")
print("near-still transitions (< 0.05):", [g for g, x in out if x < 0.05] or "none")
