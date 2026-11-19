#!/usr/bin/env python3
"""Hue rows per frame and per light (v3/tools/hue_report.py stats/row) + the SHADE HUE of each frame: the chroma-weighted circular
mean hue of the shaded pixels (value 0.10..0.55, saturation > 0.2, blue >= red: the painted shade, not dark wood or brick).
Client rule: shade hue 240-260. usage: python3 harbour_hue.py <png | folder ...>"""
import sys, os, glob, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
def shade_hue(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); m = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    return m, float(sel.mean())
fs = [f for a in sys.argv[1:] for f in H.files_of(a)]
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
H.row("reference A, whole clip", sorted(glob.glob(H.P + "/ref/a/*.jpg")))
H.row("reference B, whole clip", sorted(glob.glob(H.P + "/ref/b/*.jpg")))
groups = {}
for f in fs:
    H.row(os.path.basename(f)[:-4], [f]); n = os.path.basename(f)
    k = next((L for L in ('SEA_DAY', 'DUSK', 'DAY') if '_' + L in n), 'other'); groups.setdefault(k, []).append(f)
for g, l in groups.items(): H.row('ALL ' + g, l)
H.row('ALL', fs)
print('\nshade hue (target 240-260), shaded fraction:')
for f in fs:
    m, fr = shade_hue(f); print(f"  {os.path.basename(f)[:-4]:50s} {m:6.1f}  {fr:.2f}  {'ok' if 240 <= m <= 260 else 'OUT'}")
