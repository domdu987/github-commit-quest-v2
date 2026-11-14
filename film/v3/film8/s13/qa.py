#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s*/g_*.json and frames/ (reads meta.json for the range): head sizes / positions per set-up,
heads below the caption band (y 880), pops, near-still runs, black / magenta frames, hue rows, s per frame.
    python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H

meta = json.load(open(os.path.join(HERE, "meta.json")))
g_first, n = meta["first_g"], meta["n_frames"]
src = meta["frame_source"]
allrows = []
for g in range(g_first, g_first + n):
    for sid in src[str(g)].split("+"):
        allrows.append(json.load(open(os.path.join(HERE, "raw", "s%s" % sid, "g_%04d.json" % g))))
for sid in sorted({r["shot"] for r in allrows}):
    rows = [r for r in allrows if r["shot"] == sid]
    print("set-up %d (%d frames, g %d..%d)" % (sid, len(rows), rows[0]["g"], rows[-1]["g"]))
    for nm in sorted({k for r in rows for k in r["heads"]}):
        hs = [(r["g"], r["heads"][nm]) for r in rows if nm in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-4s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
              % (nm, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in allrows]), np.mean([r["cpu"] for r in allrows]),
                                                                         [r["g"] for r in allrows if r.get("retried")]))
fs = [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(g_first, g_first + n)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; q = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * q and v > 1.0:
        pops.append((g_first + i, g_first + i + 1, round(v, 1)))
print("popcheck (g -> g+1, change):", pops, " expected cuts:", [t["at"] for t in meta["transitions"] if t["type"] == "cut"])
still = [g_first + i for i, v in enumerate(d) if v < 0.35]
runs, cur = [], []
for g in still:
    if cur and g == cur[-1] + 1:
        cur.append(g)
    else:
        if cur: runs.append((cur[0], cur[-1]))
        cur = [g]
if cur: runs.append((cur[0], cur[-1]))
print("near-still transitions (< 0.35 levels):", len(still), "runs:", runs)
print("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    mag = ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean()
    blk = (a.max(axis=2) < 6).mean()
    if mag > 0.002 or blk > 0.2:
        bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print()
print(f"{'set':44s} " + " ".join(f"{nm[:6]:>6s}" for nm in H.NAMES) + "   sat  val dark")
for k, (a, b) in meta["shot_ranges"].items():
    H.row("%s shot %s (g %d-%d)" % (meta["take"], k, a, b), [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)])
H.row("%s all" % meta["take"], fs)
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0061 t0069 t0077 t0081", [os.path.join(R, "t%04d.jpg" % t) for t in (61, 69, 77, 81)])
