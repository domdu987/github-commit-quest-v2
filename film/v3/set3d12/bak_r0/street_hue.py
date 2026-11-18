#!/usr/bin/env python3
"""Hue rows (v3/tools/hue_report.py stats/row, imported) + the SHADE HUE of each still (chroma-weighted circular mean hue of the shaded
pixels: value 0.10..0.55, saturation > 0.2, blue >= red; target 240-260) + the magenta share (target <= 10 %). Writes styleboard/hue.txt.
usage: python3 street_hue.py [png ...]   (default: the three styleboard stills)"""
import sys, os, math, io, contextlib
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
if __name__ == '__main__':
    sb = os.path.join(HERE, 'styleboard'); fs = sys.argv[1:] or [os.path.join(sb, n) for n in ('sb1_street_wide.png', 'sb2_coach_low.png', 'sb3_street_high.png')]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'still':26s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for f in fs: H.row(os.path.basename(f)[:-4], [f])
        H.row('ALL', fs)
        print('\nshade hue (target 240-260), shaded fraction, magenta share (target <= 10 %):')
        for f in fs:
            m, fr = shade_hue(f); mag = H.stats([f])[0]['magenta']
            print(f"  {os.path.basename(f)[:-4]:26s} shade hue {m:6.1f}  shaded {fr:.2f}  magenta {mag:5.1f} %  {'ok' if 240 <= m <= 260 and mag <= 10 else 'OUT'}")
    txt = buf.getvalue(); print(txt); open(os.path.join(sb, 'hue.txt'), 'w').write(txt)
