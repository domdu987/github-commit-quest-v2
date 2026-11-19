"""hue check on REAL cast-shadow / shade pixels: the *_shade.png mask written by sb.py is a sun-only render (white override, no bounces,
sky/clouds/hills hidden) -> pixel counts as shade when it is geometry and the sun contribution is ~0. Over those pixels (sat > 0.1) we report
the circular mean hue (acceptable band 225-265), the magenta share of the whole frame (hue 290-340, sat > 0.25, limit 10 %).
usage: python3 hue_check.py [prefix]   (prefix 'd_' = drafts). Writes hue_report.txt (final only)."""
import os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); pre = sys.argv[1] if len(sys.argv) > 1 else ''
rows = []
for n in ('sb1_line_wide', 'sb2_chamber', 'sb3_bottle_close'):
    p = os.path.join(HERE, pre + n + '.jpg')
    if not os.path.exists(p): continue
    hsv = np.asarray(Image.open(p).convert('RGB').convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    m = np.asarray(Image.open(os.path.join(HERE, pre + n + '_shade.png')).convert('L').resize(Image.open(p).size), dtype=np.float32).reshape(-1) > 127
    sel = m & (s > 0.1) & (v > 0.06)
    ang = np.deg2rad(h[sel]); mh = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360
    med = float(np.median(h[sel])); mag = ((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100
    inb = ((h >= 225) & (h <= 265))[sel].mean() * 100
    ok = 225 <= mh <= 265 and mag <= 10
    rows.append('%-18s cast-shadow px %5.1f%% of frame | cast-shadow mean hue %6.1f (median %5.1f, band 225-265) | %4.1f%% of shade px in 225-265 | magenta share %5.2f%% (<=10) | %s' % (n, m.mean() * 100, mh, med, inb, mag, 'OK' if ok else 'OUT'))
txt = '\n'.join(rows) + '\n'; print(txt)
if not pre: open(os.path.join(HERE, 'hue_report.txt'), 'w').write(txt)
