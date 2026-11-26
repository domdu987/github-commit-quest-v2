"""check.py -- title frames against icons13, per-frame cost (cold / cached), ink extent, flash frame, longest still stretch."""
import os, sys, time, shutil
import numpy as np
import picto15 as C
IC = C.IC
T = C.T
bad = []
for g in range(int(np.ceil(T.TITLE * 24 - 1e-6)) - 1, 1280):
    a, b = C.overlay(g, 720, 1280), IC.overlay(g, 720, 1280)
    d = int(np.abs(a.astype(int) - b.astype(int)).max())
    if d: bad.append((g, d))
print("first title frame g %d (T.TITLE %.3f); frames from g %d differing from icons13.overlay (g, max diff): %s" % (int(np.ceil(T.TITLE * 24 - 1e-6)), T.TITLE, int(np.ceil(T.TITLE * 24 - 1e-6)) - 1, bad))
keep = C.CACHE
C.CACHE = os.path.join(C.HERE, "tmp", "cache_cold"); shutil.rmtree(C.CACHE, ignore_errors=True)
C.overlay(30, 720, 1280)
if "--quick" in sys.argv: bad = None
z = np.zeros((1280, 720, 3), np.uint8)
for lab in ("cold", "cached"):
    ts = []
    for g in range(1, 1280, 5):
        t = time.time(); C.over(z, g); ts.append(time.time() - t)
    ts = np.array(ts); print("%s: mean %.3f s, max %.3f s over %d frames" % (lab, ts.mean(), ts.max(), len(ts)))
shutil.rmtree(C.CACHE, ignore_errors=True)
C.CACHE = keep
# ink extent, stillness, emptiness
x1 = y1 = 0; ymin = 9999; over_ = []; prev = None; still = 0; worst = (0, 0); empty = []
for g in range(0, 1205):
    a = C.overlay(g, 720, 1280)
    al = a[..., 3]
    ys, xs = np.nonzero(al > 24)
    if len(ys):
        x1 = max(x1, xs.max()); ymin = min(ymin, ys.min()); y1 = max(y1, ys.max())
        if xs.max() > 396 or ys.min() < 90 or ys.max() > 290:
            over_.append((g, int(xs.max()), int(ys.min()), int(ys.max())))
        if prev is not None and np.abs(a.astype(int) - prev.astype(int)).max() < 8:
            still += 1
            if still > worst[0]: worst = (still, g)
        else:
            still = 0
    else:
        empty.append(g); still = 0
    prev = a
print("ink (frames 0-1204): x max %d (%.0f %%), y %d..%d" % (x1, 100 * x1 / 720., ymin, y1))
runs = []
for g, x, a, b in over_:
    if runs and g == runs[-1][1] + 1: runs[-1] = (runs[-1][0], g, max(runs[-1][2], x), min(runs[-1][3], a), max(runs[-1][4], b))
    else: runs.append((g, g, x, a, b))
print("frames outside x<=396 / y 90..290 (g0, g1, x max, y min, y max):", runs)
print("longest run of identical consecutive frames: %d frames ending g %d" % worst)
e = []
for g in empty:
    if e and g == e[-1][1] + 1: e[-1] = (e[-1][0], g)
    else: e.append((g, g))
print("empty stretches (s):", [("%.2f" % (a / 24.), "%.2f" % (b / 24.)) for a, b in e])
C.close(); IC.close()
