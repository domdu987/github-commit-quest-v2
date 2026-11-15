#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s*/g_*.json and frames/: head sizes / positions vs the caption band (y 880), pops (planned cuts
listed in TAKE.json), near-still runs, black / magenta frames, sharpness (Laplacian variance), hue rows.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
import cv2
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
T = json.load(open(os.path.join(HERE, "TAKE.json")))
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json")))]
for sid in sorted({r["shot"] for r in rows}):
    rr = [r for r in rows if r["shot"] == sid]
    print("set-up %d (%d frames, g %d..%d)" % (sid, len(rr), rr[0]["g"], rr[-1]["g"]))
    for n in sorted({n for r in rr for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rr if n in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-4s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
      [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
gof = lambda f: int(os.path.basename(f)[2:6])
prev = None; d = []; sharp = []; bad = []
for f in fs:
    im = Image.open(f).convert("RGB")
    a = np.asarray(im.resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append((gof(f) - 1, float(np.abs(a - prev).mean())))
    prev = a
    g8 = cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2GRAY)
    sharp.append(cv2.Laplacian(g8, cv2.CV_64F).var())
    b = np.asarray(im.resize((90, 160)), dtype=np.int16)
    if ((b[..., 0] > 200) & (b[..., 1] < 40) & (b[..., 2] > 200)).mean() > 0.002 or (b.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
v = [x for _, x in d]
pops = []
for i, (g, x) in enumerate(d):
    p = v[i - 1] if i else x; n = v[i + 1] if i + 1 < len(v) else x
    if x > 1.8 * p and x > 1.8 * n and x > 1.0:
        pops.append((g, g + 1, round(x, 1)))
print("popcheck: pops (g -> g+1, change):", pops, " planned cuts at:", T["cuts"])
still = [g for g, x in d if x < 0.35]
runs, cur = [], []
for g in still:
    if cur and g == cur[-1] + 1: cur.append(g)
    else:
        if len(cur) > 1: runs.append((cur[0], cur[-1]))
        cur = [g]
if len(cur) > 1: runs.append((cur[0], cur[-1]))
print("near-still transitions (< 0.35 levels): %d, runs > 1: %s" % (len(still), runs))
print("frame change median %.2f, max %.2f levels" % (float(np.median(v)), max(v)))
print("sharpness (Laplacian var, full res): min %.0f median %.0f" % (min(sharp), float(np.median(sharp))))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
for nm, (a, b) in T["shot_of"].items():
    H.row("%s %s (g %d-%d)" % (T["meta"]["take"], nm, a, b), [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)])
