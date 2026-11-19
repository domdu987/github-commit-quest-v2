#!/usr/bin/env python3
"""Hue rows (v3/tools/hue_report.stats) + SHADE HUE (chroma-weighted circular mean hue of shaded pixels, rule 240-260) + the night-brightness
rules of the film-18 brief: middle-band luma (0-255) 70..130 and dark share (V < 0.25) under 0.35. usage: python3 jimo_hue.py <png ...>"""
import sys, os, math
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

def luma(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float); y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
    mid = y[107:213]                                                                  # middle third of the height
    v = im.max(-1) / 255
    return float(y.mean()), float(mid.mean()), float((v < 0.25).mean())

def report(fs):
    out = []
    print(f"{'still':14s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark | shade hue (n)  luma  midband  dark<0.25")
    for f in fs:
        h, s, v, dk = H.stats([f]); sh, fr = shade_hue(f); lm, lmid, dkv = luma(f)
        print(f"{os.path.basename(f)[:-4]:14s} " + " ".join(f"{h[n]:6.1f}" for n in H.NAMES) + f"  {s:.2f} {v:.2f} {dk:.2f} | {sh:6.1f} ({fr:.2f}) {lm:6.1f} {lmid:7.1f}  {dkv:.2f}  " + ('ok' if 240 <= sh <= 260 else 'SHADE-OUT') + (' ' if 70 <= lmid <= 130 else ' MID-OUT') + (' ' if dkv < 0.35 else ' DARK-OUT'))
        out.append(dict(file=os.path.basename(f), hue={n: round(h[n], 1) for n in H.NAMES}, sat=round(s, 3), val=round(v, 3), dark_v025=round(dkv, 3), shade_hue=round(sh, 1), shaded_frac=round(fr, 3),
                        luma_mean=round(lm, 1), luma_mid=round(lmid, 1)))
    return out

if __name__ == '__main__': report(sys.argv[1:])
