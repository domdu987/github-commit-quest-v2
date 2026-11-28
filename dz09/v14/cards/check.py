import os, sys, time, shutil
import numpy as np
from PIL import Image
import cards14 as C
IC = C.IC
# 1. title frames identical to icons13
bad = []
for g in range(1216, 1280):
    a, b = C.overlay(g, 720, 1280), IC.overlay(g, 720, 1280)
    d = np.abs(a.astype(int) - b.astype(int)).max()
    if d: bad.append((g, int(d)))
print("title frames differing from icons13 (g, max diff):", bad)
# 2. cold cost: fresh cache dir
C.CACHE = os.path.join(C.HERE, "tmp", "cache_cold"); shutil.rmtree(C.CACHE, ignore_errors=True)
C.overlay(30, 720, 1280)
ts = []
for g in range(0, 1280, 7):
    t = time.time(); C.over(np.zeros((1280, 720, 3), np.uint8), g); ts.append(time.time() - t)
ts = np.array(ts); print("cold: mean %.3f s, max %.3f s over %d frames" % (ts.mean(), ts.max(), len(ts)))
ts = []
for g in range(0, 1280, 7):
    t = time.time(); C.over(np.zeros((1280, 720, 3), np.uint8), g); ts.append(time.time() - t)
ts = np.array(ts); print("cached: mean %.4f s, max %.4f s" % (ts.mean(), ts.max()))
shutil.rmtree(C.CACHE, ignore_errors=True)
# 3. ink extent over the whole film (every 2nd frame), 9:16
C.CACHE = os.path.join(C.HERE, "cache")
x1 = y1 = 0; ymin = 9999
for g in range(0, 1205):
    a = C.overlay(g, 720, 1280)[..., 3]
    ys, xs = np.nonzero(a > 8)
    if len(ys): x1 = max(x1, xs.max()); ymin = min(ymin, ys.min()); y1 = max(y1, ys.max())
print("ink (frames 0-1204): x max %d (%.0f %%), y %d..%d" % (x1, 100 * x1 / 720., ymin, y1))
