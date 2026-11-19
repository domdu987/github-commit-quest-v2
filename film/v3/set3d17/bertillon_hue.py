#!/usr/bin/env python3
"""film 17 colour numbers per frame: tools/hue_report.py stats (hue families, sat, val, dark), the SHADE HUE (chroma-weighted mean hue of the shaded
pixels: V 0.10-0.55, S > 0.2, B >= R; band 240-260), black point (luma p1, band 0.08-0.12), vivid blue share (S > 0.6, H 200-245; band < 1.5 %),
the hue of the dim pixels (V 0.12-0.40, S > 0.15: share in 240-260 and share in 0-45) and the median luma of the background ring around each
placeholder head (band ~95-165).  usage: python3 bertillon_hue.py <png | folder ...>   (also importable: frame_stats(path))"""
import sys, os, glob, math
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
def _hsv(im):
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    return np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60, s, mx
def frame_stats(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])      # caption band out
    h, s, v = _hsv(im); r, g, b = im[..., 0], im[..., 1], im[..., 2]
    sel = (v > 0.10) & (v < 0.55) & (s > 0.2) & (b >= r); w = (s * v)[sel]
    shade = float('nan')
    if w.sum() > 0: a = np.radians(h[sel]); shade = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b; p1 = float(np.percentile(luma, 1))
    dim = (v > 0.12) & (v < 0.40) & (s > 0.15); n = max(dim.sum(), 1); d_blue = float(((h >= 240) & (h <= 260) & dim).sum() / n); d_warm = float(((h <= 45) & dim).sum() / n)
    vivid = float(((s > 0.6) & (h >= 200) & (h <= 245) & (v > 0.2)).mean())
    hs, sat, val, dark = H.stats([f])
    return dict(fam=hs, sat=sat, val=val, dark=dark, shade=shade, shade_frac=float(sel.mean()), p1=p1, dim_blue=d_blue, dim_warm=d_warm, vivid=vivid)
def check(st):
    bad = []
    if not (240 <= st['shade'] <= 260): bad.append('shade')
    if not (0.08 <= st['p1'] <= 0.12): bad.append('p1')
    if not (14 <= st['fam']['blue'] <= 30): bad.append('blue')
    if st['fam']['magenta'] > 10: bad.append('magenta')
    if st['vivid'] > 0.015: bad.append('vivid')
    return bad
def row(label, st):
    f = st['fam']; bad = check(st)
    print(f"{label[:30]:30s} red {f['red']:5.1f} ora {f['orange']:5.1f} blu {f['blue']:5.1f} mag {f['magenta']:5.1f} | shade {st['shade']:6.1f} p1 {st['p1']:.3f} vivid {st['vivid']*100:4.1f}% dim240-260 {st['dim_blue']*100:3.0f}% dim0-45 {st['dim_warm']*100:3.0f}% | val {st['val']:.2f} dark {st['dark']:.2f}  " + ('OUT: ' + ','.join(bad) if bad else 'ok'))
if __name__ == '__main__':
    for a in sys.argv[1:]:
        for f in H.files_of(a): row(os.path.basename(f)[:-4], frame_stats(f))
