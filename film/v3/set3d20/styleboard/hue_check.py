"""hue check on REAL cast-shadow pixels: the *_shade.png mask written by sb.py is a sun-only render (white override, no bounces, sky hidden):
a pixel is cast shadow when it is geometry, the sun contribution is ~0 and it would be lit with shadows off. Over those pixels (sat > 0.1) we report
the circular mean hue (target 240-260, accepted 225-265), the magenta share of the whole frame (hue 290-340, sat > 0.25, limit 10 %), and the
overall hue shares of chroma (red/orange/yellow/green/blue/violet/magenta, sat > 0.2).  usage: python3 hue_check.py [prefix]  (prefix 'd_' = drafts)"""
import os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); pre = sys.argv[1] if len(sys.argv) > 1 else ''
rows = []
for n in ('sb1_site', 'sb2_tower_dusk', 'sb3_resto'):
    p = os.path.join(HERE, pre + n + '.jpg')
    if not os.path.exists(p): continue
    hsv = np.asarray(Image.open(p).convert('RGB').convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    m = np.asarray(Image.open(os.path.join(HERE, pre + n + '_shade.png')).convert('L').resize(Image.open(p).size), dtype=np.float32).reshape(-1) > 127
    sel = m & (s > 0.1) & (v > 0.06)
    ang = np.deg2rad(h[sel]); mh = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360 if sel.sum() else float('nan')
    med = float(np.median(h[sel])) if sel.sum() else float('nan'); mag = ((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100
    inb = ((h >= 225) & (h <= 265))[sel].mean() * 100 if sel.sum() else 0
    c = s > 0.2; tot = max(c.sum(), 1)
    bands = [('red', (h >= 345) | (h < 15)), ('orange', (h >= 15) & (h < 45)), ('yellow', (h >= 45) & (h < 70)), ('green', (h >= 70) & (h < 170)), ('blue', (h >= 190) & (h < 265)), ('violet', (h >= 265) & (h < 290)), ('magenta', (h >= 290) & (h < 345))]
    shares = ' '.join('%s %4.1f' % (k, (b & c).sum() / tot * 100) for k, b in bands)
    L = (0.299 * np.asarray(Image.open(p).convert('RGB'), dtype=float)[..., 0] + 0.587 * np.asarray(Image.open(p).convert('RGB'), dtype=float)[..., 1] + 0.114 * np.asarray(Image.open(p).convert('RGB'), dtype=float)[..., 2]); hh = L.shape[0] // 8
    br = 'luma top1/8 %.0f mid-band %.0f bottom1/8 %.0f | V>0.95 %.1f%% | dark V<0.25 %.1f%%' % (L[:hh].mean(), L[hh * 3:hh * 5].mean(), L[-hh:].mean(), (v > 0.95).mean() * 100, (v < 0.25).mean() * 100)
    ok = 225 <= mh <= 265 and mag <= 10
    rows.append('%-16s cast-shadow px %5.1f%% of frame | shade mean hue %6.1f (median %5.1f; target 240-260) | %4.1f%% of shade px in 225-265 | magenta share %5.2f%% (<=10) | %s\n%-16s hue shares of chroma %%: %s | mean sat %.2f val %.2f\n%-16s %s' % (n, m.mean() * 100, mh, med, inb, mag, 'OK' if ok else 'OUT', '', shares, s.mean(), v.mean(), '', br))
txt = '\n'.join(rows) + '\n'; print(txt)
if not pre: open(os.path.join(HERE, 'hue_report.txt'), 'w').write(txt)
