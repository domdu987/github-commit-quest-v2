"""hue check on REAL cast-shadow pixels: the *_shade.png mask written by sb.py is a sun-only render (white override, no bounces, sky/clouds/windows hidden):
a pixel counts as cast shadow when it is geometry the sun reaches in an unshadowed render (D2) but not in the shadowed one (D). Over those pixels (sat > 0.1)
we report the circular mean hue (band 225-265, interiors with warm bounce may sit lower), the magenta share of the whole frame (hue 290-340, sat > 0.25, limit 10 %),
and the project's hue-family make-up (S*V weighted, sat>0.15 & val>0.15, caption band 212-239 of 320 removed, frames at 180x320) like v3/tools/hue_report.py.
usage: python3 hue_check.py [prefix]   (prefix 'd_' = drafts). Writes hue_report.txt (final only)."""
import os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); pre = sys.argv[1] if len(sys.argv) > 1 else ''
FAM = [('red', 345, 20), ('orange', 20, 50), ('yellow', 50, 75), ('green', 75, 165), ('cyan', 165, 200), ('blue', 200, 255), ('violet', 255, 290), ('magenta', 290, 345)]
rows = []
for n in ('sb1_workshop', 'sb2_ship', 'sb3_hall'):
    p = os.path.join(HERE, pre + n + '.jpg')
    if not os.path.exists(p): continue
    im = Image.open(p).convert('RGB'); hsv = np.asarray(im.convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    m = np.asarray(Image.open(os.path.join(HERE, pre + n + '_shade.png')).convert('L').resize(im.size), dtype=np.float32).reshape(-1) > 127
    sel = m & (s > 0.1) & (v > 0.06)
    ang = np.deg2rad(h[sel]); mh = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360 if sel.sum() else float('nan')
    med = float(np.median(h[sel])) if sel.sum() else float('nan'); mag = ((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100
    inb = ((h >= 225) & (h <= 265))[sel].mean() * 100 if sel.sum() else 0.0
    ok = (225 <= mh <= 265) and mag <= 10
    # project-style family make-up
    sm = np.asarray(im.resize((180, 320), Image.BILINEAR).convert('HSV'), dtype=np.float32); sm = np.concatenate([sm[:212], sm[240:]]).reshape(-1, 3)
    hh = sm[:, 0] * 360 / 255; ss = sm[:, 1] / 255; vv = sm[:, 2] / 255; k = (ss > 0.15) & (vv > 0.15); w = (ss * vv)[k]; hk = hh[k]
    fam = {}
    for nm, a, b in FAM:
        sel2 = ((hk >= a) | (hk < b)) if a > b else ((hk >= a) & (hk < b)); fam[nm] = 100 * w[sel2].sum() / max(w.sum(), 1e-9)
    rows.append('%-14s cast-shadow px %5.1f%% of frame | cast-shadow mean hue %6.1f (median %5.1f; band 225-265) | %4.1f%% of shade px in 225-265 | magenta share (frame, S>0.25) %5.2f%% (<=10) | %s\n%-14s families %% of chroma: %s | sat %.2f val %.2f dark(V<.25) %.1f%%' % (
        n, m.mean() * 100, mh, med, inb, mag, 'OK' if ok else 'OUT', '', ' '.join('%s %.1f' % (a, fam[a]) for a, _, _ in FAM), ss[k].mean(), vv[k].mean(), 100 * (vv < 0.25).mean()))
txt = '\n'.join(rows) + '\n'; print(txt)
if not pre: open(os.path.join(HERE, 'hue_report.txt'), 'w').write(txt)
