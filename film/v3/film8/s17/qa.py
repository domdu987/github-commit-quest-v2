#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s17..s19 json + frames/: pops, near-still runs, black / magenta frames, hue rows, s per frame.
    python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
for sid in (17, 18, 19):
    rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s%d" % sid, "g_*.json")))]
    print("set-up %d: %d frames, wall %.2f s, cpu %.2f s per frame; retried %s" % (sid, len(rows), np.mean([r["wall"] for r in rows]),
          np.mean([r["cpu"] for r in rows]), [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
g0 = int(os.path.basename(fs[0])[2:6])
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
        pops.append((g0 + i, g0 + i + 1, round(v, 1)))
print("popcheck: pops (g -> g+1, change):", pops, " (expected: none; the two shot changes are dissolves)")
still = [g0 + i for i, v in enumerate(d) if v < 0.35]
run, best = 0, 0
for i, v in enumerate(d):
    run = run + 1 if v < 0.35 else 0; best = max(best, run)
print("near-still transitions (< 0.35 levels): %d, longest run %d: %s" % (len(still), best, still[:40]))
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
fr = lambda a, b: [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(a, b + 1)]
H.row("s17 shot 17 sky reveal (g 1347-1473)", fr(1347, 1473))
H.row("s17 shot 18 wall noon (g 1484-1555)", fr(1484, 1555))
H.row("s17 shot 19 frost ecu (g 1566-1666)", fr(1566, 1666))
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0072 t0073 (night wide)", [os.path.join(R, "t%04d.jpg" % t) for t in (72, 73)])
H.row("ref a t0061 (day sun)", [os.path.join(R, "t%04d.jpg" % t) for t in (61,)])
