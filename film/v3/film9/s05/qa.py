#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s*/g_*.json and frames/: head sizes / positions per shot, heads crossing y 880, pops (expected
only at the planned cuts), near-still runs, black / magenta frames, hue rows, s per frame.     python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import take_info as TI
import hue_report as H

allrows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json")))]
allrows = [r for r in allrows if TI.FIRST_G <= r["g"] <= TI.LAST_G]
for sid in TI.SHOTS:
    rows = [r for r in allrows if r["shot"] == sid]
    if not rows:
        continue
    print("shot %d (g %d..%d, %d frames)" % (sid, rows[0]["g"], rows[-1]["g"], len(rows)))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        edge = [g for g, h in hs if h["x"] - h["w"] / 2 < 0 or h["x"] + h["w"] / 2 > 720]
        print("  %-9s head w %4.0f..%4.0f px, x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); below 880: %s; crosses frame edge: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280,
                 (low[0], low[-1], len(low)) if low else "none", (edge[0], edge[-1], len(edge)) if edge else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in allrows]), np.mean([r["cpu"] for r in allrows]),
                                                                       [r["g"] for r in allrows if r.get("retried")]))
fs = [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(TI.FIRST_G, TI.LAST_G + 1)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((TI.FIRST_G + i, TI.FIRST_G + i + 1, round(v, 1)))
print("popcheck: pops (g -> g+1, change):", pops, " expected: the cuts", TI.CUTS)
still = [TI.FIRST_G + i for i, v in enumerate(d) if v < 0.35]
runs, cur = [], []
for g in still:
    if cur and g == cur[-1] + 1:
        cur.append(g)
    else:
        if cur:
            runs.append(cur)
        cur = [g]
if cur:
    runs.append(cur)
print("near-still transitions (< 0.35 levels):", len(still), " longest run:", max([len(r) for r in runs], default=0),
      " runs > 3:", [(r[0], r[-1]) for r in runs if len(r) > 3])
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
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
for sid, (a, b) in TI.SHOT_RANGES.items():
    H.row("%s shot %d (g %d-%d)" % (TI.TAKE, sid, a, b), [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)])
H.row("%s all" % TI.TAKE, fs)
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0062 t0072 (day wide / medium)", [os.path.join(R, "t%04d.jpg" % t) for t in (62, 72)])
