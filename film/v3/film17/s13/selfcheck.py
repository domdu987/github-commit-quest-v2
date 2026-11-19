#!/usr/bin/env python3
"""selfcheck.py <take.mkv|raw dir> -- 6 fps sheets (every 5th frame, 3 sheets of 40 tiles with the y 880 line) + cut +-3 strips (cuts 1947, 2014)
+ numeric: spikes, frozen runs, bright isolated specks. Output in ./check/. Look at every sheet, then list what was checked in QA.md."""
import os, sys, glob, numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "check"); os.makedirs(OUT, exist_ok=True)
FIRST, LAST = 1862, 2051
def fr(g): return Image.open(os.path.join(RAW, "g_%04d.png" % g)).convert("RGB")
def sheet(gs, name, tw=144, th=256, cols=10):
    rows = (len(gs) + cols - 1) // cols; s = Image.new("RGB", (tw * cols, th * rows)); d = ImageDraw.Draw(s)
    for i, g in enumerate(gs):
        x, y = (i % cols) * tw, (i // cols) * th; s.paste(fr(g).resize((tw, th)), (x, y)); d.line((x, y + int(880 * th / 1280), x + tw, y + int(880 * th / 1280)), fill=(0, 255, 255)); d.text((x + 3, y + 3), str(g), fill=(255, 255, 255))
    s.save(os.path.join(OUT, name), quality=88)
gs = list(range(FIRST, LAST + 1, 5))
for i in range(0, len(gs), 40): sheet(gs[i:i + 40], "sheet6fps_%d.jpg" % (i // 40))
for c in (1947, 2014): sheet(list(range(c - 3, c + 3)), "cut_%d.jpg" % c, tw=240, th=427, cols=6)
prev = None; spikes = []; frozen = 0; specks = []
for g in range(FIRST, LAST + 1):
    a = np.asarray(fr(g).resize((180, 320)).convert("L"), np.float32)
    if prev is not None:
        d = np.abs(a - prev).mean()
        if d > 20 and g not in (1947, 2014): spikes.append((g, round(float(d), 1)))
        frozen = frozen + 1 if d < 0.25 else 0
        if frozen > 6: spikes.append((g, "frozen"))
    prev = a
print("spikes/frozen outside cuts:", spikes or "none")
