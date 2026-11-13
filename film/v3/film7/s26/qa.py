#!/usr/bin/env python3
"""qa.py -- numbers for QA.md from raw/s*/g_*.json + frames/ (uses meta.json): heads per set-up (size, centre, below y 880), pops,
near-still pairs, black / magenta frames, hue rows, s per frame.   python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
meta = json.load(open(os.path.join(HERE, "meta.json")))
src = meta["frame_source"]
rows = []
for g, sid in sorted(src.items(), key=lambda kv: int(kv[0])):
    for s in sid.split("+"):
        rows.append(json.load(open(os.path.join(HERE, "raw", "s%s" % s, "g_%04d.json" % int(g)))))
for sid in sorted({r["shot"] for r in rows}):
    rr = [r for r in rows if r["shot"] == sid]
    print("set-up %d (g %d..%d, %d frames)" % (sid, rr[0]["g"], rr[-1]["g"], len(rr)))
    for n in sorted({n for r in rr for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rr if n in r["heads"] and -60 < r["heads"][n]["x"] < 780 and r["heads"][n]["y"] < 1400]
        if not hs:
            continue
        w = [h["w"] for g, h in hs]; y = [h["y"] for g, h in hs]; x = [h["x"] for g, h in hs]
        low = [g for g, h in hs if h["y"] + h["w"] / 2 > 880]
        print("  %-7s head w %4.0f..%4.0f px, x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]),
                                                                        [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
g0 = meta["first_g"]
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((g0 + i, g0 + i + 1, round(v, 1)))
print("popcheck (g -> g+1, change):", pops, " cuts:", [t["at"] for t in meta["transitions"] if t["type"] == "cut"])
print("near-still transitions (< 0.35 levels):", [g0 + i for i, v in enumerate(d) if v < 0.35])
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
for sid, (a, b) in sorted(meta["setups"].items()):
    pass
for k, v in sorted(meta["setups"].items(), key=lambda kv: int(kv[0])):
    a, b = v["g"]
    H.row("%s set-up %s (g %d-%d)" % (meta["take"], k, a, b), fr(max(a, g0), min(b, g0 + len(fs) - 1)))
H.row("%s all" % meta["take"], fs)
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
for t in meta.get("qa_refs", [15, 45]):
    H.row("ref a t%04d" % t, [os.path.join(R, "t%04d.jpg" % t)])
