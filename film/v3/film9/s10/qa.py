#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s1 + raw/s2 g_*.json and frames/: head sizes / positions per set-up, heads crossing the caption
band (head bottom > 880), pops (only the planned cut expected), near-still runs, black / magenta frames, sharpness (Laplacian variance),
hue rows, s per frame.   python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import take_conf as K                                      # noqa: E402
import hue_report as H                                     # noqa: E402
import cv2                                                 # noqa: E402

allrows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s[12]", "g_*.json")))]
for sid in (1, 2):
    rows = [r for r in allrows if r["shot"] == sid]
    print("set-up %d = shot %d (%s, %d frames)" % (sid, K.SHOTS[sid - 1], K.SETUPS[sid]["name"], len(rows)))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-5s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H), max bottom %4.0f; below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, max(h["y"] + h["w"] / 2 for g, h in hs),
                 (low[0], low[-1], len(low)) if low else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in allrows]), np.mean([r["cpu"] for r in allrows]),
                                                                       [r["g"] for r in allrows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
gs = [int(os.path.basename(f)[2:6]) for f in fs]
prev = None; d = []; sharp = []; bad = []
for f in fs:
    im = Image.open(f).convert("RGB")
    a = np.asarray(im.resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
    gray = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    sharp.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))
    s = np.asarray(im.resize((90, 160)), dtype=np.int16)
    if ((s[..., 0] > 200) & (s[..., 1] < 40) & (s[..., 2] > 200)).mean() > 0.002 or (s.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((gs[i], gs[i + 1], round(v, 1)))
print("popcheck: pops (g -> g+1, change):", pops, " (expected: the cut %d -> %d)" % (K.G_CUT - 1, K.G_CUT))
still = [gs[i] for i, v in enumerate(d) if v < 0.35]
runs, cur = [], []
for g in still:
    if cur and g == cur[-1] + 1:
        cur.append(g)
    else:
        if len(cur) > 1: runs.append((cur[0], cur[-1]))
        cur = [g]
if len(cur) > 1: runs.append((cur[0], cur[-1]))
print("near-still transitions (< 0.35 levels): %d, runs > 1: %s" % (len(still), runs))
print("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
print("sharpness (Laplacian var, full res): min %.0f median %.0f" % (min(sharp), float(np.median(sharp))))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
H.row("%s shot %d (g %d-%d)" % (K.TAKE, K.SHOTS[0], K.G0, K.G_CUT - 1), fr(K.G0, K.G_CUT - 1))
H.row("%s shot %d (g %d-%d)" % (K.TAKE, K.SHOTS[1], K.G_CUT, K.G1 - 1), fr(K.G_CUT, K.G1 - 1))
H.row("%s all (g %d-%d)" % (K.TAKE, K.FIRST, K.LAST), fr(K.FIRST, K.LAST))
