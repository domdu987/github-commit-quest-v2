#!/usr/bin/env python3
"""Colour numbers of a still (QA_TEAM section G / I): mean saturation (max-min)/max and vivid share (qa_stats2.py: 90x160, channel mean luma), mean luma (0-255),
hue families (v3/tools/hue_report.stats, caption band excluded), magenta share, SHADE HUE (chroma-weighted circular mean hue of shaded pixels, rule 240-260),
dark share (V < 0.25).   usage: python3 ghost_hue.py <png ...>"""
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

def qa(f):
    a = np.asarray(Image.open(f).convert('RGB').resize((90, 160), Image.BILINEAR), dtype=np.float32)
    mx = a.max(-1); mn = a.min(-1); sp = (mx - mn) / (mx + 1e-3)
    return float(sp.mean()), float((sp > 0.5).mean() * 100), float(a.mean(-1).mean())

def report(fs, quiet=False):
    out = []
    for f in fs:
        h, s, v, dk = H.stats([f]); sh, fr = shade_hue(f); sat, viv, lum = qa(f)
        im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float); y = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
        row = dict(file=os.path.basename(f), sat_qa=round(sat, 3), vivid_pct=round(viv, 1), luma_qa=round(lum, 1), luma_709=round(float(y.mean()), 1), magenta_pct=round(h['magenta'], 1),
                   hue={n: round(h[n], 1) for n in H.NAMES}, sat_hue_report=round(s, 3), dark_v025=round(dk, 3), shade_hue=round(sh, 1), shaded_frac=round(fr, 3))
        out.append(row)
        if not quiet: print('%-18s sat %.3f vivid %4.1f%% luma %5.1f (709 %5.1f) magenta %4.1f%% shade_hue %5.1f (%.2f) dark %.2f | ' % (row['file'], sat, viv, lum, row['luma_709'], h['magenta'], sh, fr, dk) + ' '.join('%s %.0f' % (n[:3], h[n]) for n in H.NAMES))
    return out

if __name__ == '__main__': report(sys.argv[1:])
