"""qa.py -- hue rows per shot (hue_report.stats), static-run check, head sizes/centres from raw json.  -> work/qa.txt"""
import sys, os, json, glob, importlib.util
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("hr", os.path.join(HERE, "..", "..", "tools", "hue_report.py"))
src = open(spec.origin).read().split("\nrow(")[0]                     # functions only (the module body prints reference rows)
hr = {}; exec(compile(src.split("def row(")[0], "hue_report", "exec"), hr)
R = {13: (616, 734), 14: (735, 796), 15: (797, 878), 16: (879, 969)}
out = []
for s, (a, b) in R.items():
    fl = ["frames/g_%04d.png" % g for g in range(a, b + 1, 3)]
    h, sat, val, dk = hr["stats"](fl)
    out.append("shot %d  " % s + " ".join("%s %.1f" % (k, v) for k, v in h.items()) + "  sat %.2f val %.2f dark %.2f" % (sat, val, dk))
prev = None; run = 0; worst = 0; diffs = []
for g in range(616, 970):
    im = np.asarray(Image.open("frames/g_%04d.png" % g).convert("L").resize((180, 320)), float)
    if prev is not None:
        d = np.abs(im - prev).mean(); diffs.append(d)
        run = run + 1 if d < 0.4 else 0; worst = max(worst, run)
    prev = im
out.append("frame-to-frame mean abs diff: median %.2f max %.2f; longest near-still run %d frames" % (np.median(diffs), max(diffs), worst))
for s, (a, b) in R.items():
    hs = {}
    for g in range(a, b + 1):
        for n, v in json.load(open("raw/s%d/g_%04d.json" % (s, g)))["heads"].items():
            if 0 <= v["x"] <= 720 and v["y"] + v["w"] / 2 > 0:
                hs.setdefault(n, []).append((v["w"], v["y"], v["y"] + v["w"] / 2))
    out.append("shot %d heads: " % s + "; ".join("%s w %d-%d px, centre y %.2f-%.2f H, bottom max %d" % (
        n, min(x[0] for x in L), max(x[0] for x in L), min(x[1] for x in L) / 1280, max(x[1] for x in L) / 1280, max(x[2] for x in L)) for n, L in hs.items()))
open(os.path.join(HERE, "work", "qa.txt"), "w").write("\n".join(out) + "\n"); print("\n".join(out))
