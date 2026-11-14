#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s1 + raw/s2 g_*.json and frames/: head sizes / positions, heads below the caption band
(y 880), pops (the cut at g 75 is expected), black / magenta frames, hue rows, s per frame.  python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H

allrows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s[34567]", "g_*.json")))]
for sid, nm in ((3, "shot 3 crane g 172..257 incl. in-handle"), (4, "shot 4 well g 258..357"), (5, "shot 5 merchant g 358..431"),
                (6, "shot 6 two-shot g 432..540"), (7, "shot 7 jeering wide g 541..613 incl. handle")):
  rows = [r for r in allrows if r["shot"] == sid]
  print("set-up %d (%s, %d frames)" % (sid, nm, len(rows)))
  for n in sorted({n for r in rows for n in r["heads"]}):
    hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
    w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
    low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
    print("  %-6s head w %5.0f..%5.0f px, centre x %4.0f..%4.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); head bottom below 880: %s"
          % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
rows = allrows
print("  render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                          [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
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
        pops.append((i, i + 1, round(v, 1)))
print("popcheck: pops (g -> g+1, change):", [(a + 172, b + 172, v) for a, b, v in pops], " (expected: the cuts 257->258, 357->358, 431->432, 540->541)")
print("near-still transitions (< 0.35 levels), g:", [i + 172 for i, v in enumerate(d) if v < 0.35])
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
for sid, (a, b) in ((3, (172, 257)), (4, (258, 357)), (5, (358, 431)), (6, (432, 540)), (7, (541, 613))):
    H.row("s03 shot %d (g %d-%d)" % (sid, a, b), fr(a, b))
H.row("s03 all (g 172-613)", fr(172, 613))
R = os.path.join(HERE, "..", "..", "..", "ref")
H.row("ref a t0069 (lit set, day)", [os.path.join(R, "a", "t0069.jpg")])
H.row("ref b t0029 t0033 (day medium)", [os.path.join(R, "b", "t%04d.jpg" % t) for t in (29, 33)])
