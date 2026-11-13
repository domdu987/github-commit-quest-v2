#!/usr/bin/env python3
"""qa.py -- numbers for QA.md (same file in s02 / s03 / s04): head sizes / positions per set-up, heads below the caption band (y 880),
pops between frames (framing changes expected), black / magenta frames, hue rows, s per frame.   python3 qa.py > work/qa.txt"""
import os, sys, json, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
meta = json.load(open(os.path.join(HERE, "meta.json")))
allrows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw", "s*", "g_*.json")))]
for sid, su in meta["setups"].items():
    rows = [r for r in allrows if str(r["shot"]) == sid and su["g"][0] <= r["g"] <= su["g"][1]]
    print("set-up %s (g %d..%d, %d frames): %s" % (sid, su["g"][0], su["g"][1], len(rows), su["set"][:70]))
    for n in sorted({n for r in rows for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rows if n in r["heads"]]
        vis = [(g, h) for g, h in hs if -h["w"] / 2 < h["x"] < 720 + h["w"] / 2 and -h["w"] / 2 < h["y"] < 1280 + h["w"] / 2]
        if not vis:
            print("  %-9s never on screen" % n); continue
        w = [h["w"] for g, h in vis]; y = [h["y"] for g, h in vis]; x = [h["x"] for g, h in vis]
        low = [g for g, h in vis if h["y"] + h["w"] / 2 > 880]
        print("  %-9s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
              % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[0], low[-1], len(low)) if low else "none"))
    if rows and "mouth" in rows[0]:
        print("  director mouths: %s" % ", ".join("%d:%s" % (r["g"], r["mouth"]) for r in rows if r.get("mouth")))
print("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean([r["wall"] for r in allrows]), np.mean([r["cpu"] for r in allrows]),
                                                                         [r["g"] for r in allrows if r.get("retried")]))
fs = sorted(glob.glob(os.path.join(HERE, "frames", "g_*.png")))
g_first = meta["first_g"]
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
        pops.append((g_first + i, g_first + i + 1, round(v, 1)))
cuts = [int(s["g"][0]) for s in meta["setups"].values()][1:]
print("popcheck (g -> g+1, change):", pops, " expected framing changes at:", cuts)
print("near-still transitions (< 0.35 levels):", [g_first + i for i, v in enumerate(d) if v < 0.35])
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
for sid, su in meta["setups"].items():
    H.row("%s id %s (g %d-%d)" % (meta["take"], sid, su["g"][0], su["g"][1]), [os.path.join(HERE, "frames", "g_%04d.png" % g) for g in range(su["g"][0], su["g"][1] + 1, 2)])
H.row("%s all" % meta["take"], fs[::3])
