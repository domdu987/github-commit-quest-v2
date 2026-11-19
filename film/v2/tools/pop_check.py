#!/usr/bin/env python3
"""pop_check.py -- frame-to-frame difference of the final frames, to find pops (measuring only: numpy, Pillow).
usage: python3 tools/pop_check.py [frames_dir]      prints the mean absolute difference per frame pair and flags pairs
whose difference is more than 1.8 x both neighbours (a one-frame jump that the frames around it do not share)."""
import os, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "out", "frames")
fs = sorted(f for f in os.listdir(d) if f.endswith(".png"))
prev = None
diffs = []
for f in fs:
    a = np.asarray(Image.open(os.path.join(d, f)).convert("L").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        diffs.append(float(np.abs(a - prev).mean()))
    prev = a
print("mean abs difference between consecutive frames (g -> g+1), 0..255 at 180x320:")
for i in range(0, len(diffs), 15):
    print("  g%3d: " % i + " ".join("%5.1f" % v for v in diffs[i:i + 15]))
flag = [i for i in range(1, len(diffs) - 1) if diffs[i] > 1.8 * diffs[i - 1] and diffs[i] > 1.8 * diffs[i + 1] and diffs[i] > 3.0]
print("isolated jumps (pair g -> g+1):", ", ".join("%d->%d (%.1f)" % (i, i + 1, diffs[i]) for i in flag) or "none")
