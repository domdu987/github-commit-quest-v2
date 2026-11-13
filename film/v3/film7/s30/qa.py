#!/usr/bin/env python3
"""qa.py -- numbers for QA.md of this take (works in s30 and s31): heads below y 880, pops, near-still runs, black / magenta frames,
hue rows, s per frame.   python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json")))]
low = [(r["g"], k) for r in rows for k, h in (r.get("heads_below_880") or {}).items()]
low += [(r["g"], k) for r in rows for k, h in (r.get("heads") or {}).items() if k != "refl" and 0 <= h["x"] <= 720 and h["y"] + h["w"] / 2 > 880]
print("frames %d; heads with bottom below y 880 (on screen): %s" % (len(rows), low or "none"))
if any("n_heads" in r for r in rows):
    print("crowd heads on the card list per frame: %d..%d" % (min(r["n_heads"] for r in rows), max(r["n_heads"] for r in rows)))
if any("mona_face" in r for r in rows):
    ys = [r["mona_face"][1] for r in rows]; print("her face centre y %.0f..%.0f (%.2f..%.2f H)" % (min(ys), max(ys), min(ys) / 1280, max(ys) / 1280))
    rf = [r for r in rows if r.get("refl", 0) > 0 and "refl" in r["heads"]]
    if rf: print("reflection on g %d..%d, its head w %.0f..%.0f px, y %.0f..%.0f" % (rf[0]["g"], rf[-1]["g"], min(r["heads"]["refl"]["w"] for r in rf), max(r["heads"]["refl"]["w"] for r in rf), min(r["heads"]["refl"]["y"] for r in rf), max(r["heads"]["refl"]["y"] for r in rf)))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in rows]), np.mean([r["cpu"] for r in rows]), [r["g"] for r in rows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
g0 = int(os.path.basename(fs[0])[2:6])
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None: d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = [(g0 + i, g0 + i + 1, round(v, 1)) for i, v in enumerate(d) if v > 1.8 * (d[i - 1] if i else v) and v > 1.8 * (d[i + 1] if i + 1 < len(d) else v) and v > 1.0]
print("popcheck (g -> g+1, change):", pops)
st = [g0 + i for i, v in enumerate(d) if v < 0.15]
print("near-still transitions (< 0.15 levels): %d %s; frame change median %.2f, max %.2f" % (len(st), st[:20], float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2: bad.append(os.path.basename(f))
print("magenta / black frames:", bad)
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
H.row(os.path.basename(HERE) + " all", fs)
R = os.path.join(HERE, "..", "..", "..", "ref", "a")
H.row("ref a t0040 t0046 t0051", [os.path.join(R, "t%04d.jpg" % t) for t in (40, 46, 51)])
