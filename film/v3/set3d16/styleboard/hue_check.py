"""hue check: darkest-third (by value) pixels with sat>0.1 -> circular mean hue (target 240-260); magenta share (hue 290-340, sat>0.25) <= 10 %.
usage: python3 hue_check.py [prefix]   (prefix 'd_' to check drafts). Writes hue_report.txt"""
import os, sys, numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); pre = sys.argv[1] if len(sys.argv) > 1 else ''
rows = []; ok_all = True
for n in ('sb1_line_wide', 'sb2_chamber', 'sb3_bottle_close'):
    p = os.path.join(HERE, pre + n + '.jpg')
    if not os.path.exists(p): continue
    hsv = np.asarray(Image.open(p).convert('RGB').convert('HSV'), dtype=np.float32).reshape(-1, 3)
    h = hsv[:, 0] * 360 / 255; s = hsv[:, 1] / 255; v = hsv[:, 2] / 255
    thr = np.percentile(v, 100 / 3); dk = (v <= thr) & (s > 0.1)
    ang = np.deg2rad(h[dk]); mh = (np.rad2deg(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) + 360) % 360
    mag = ((h >= 290) & (h <= 340) & (s > 0.25)).mean() * 100
    blue = ((h >= 230) & (h <= 270))[dk].mean() * 100
    ok = 240 <= mh <= 260 and mag <= 10; ok_all &= ok
    rows.append('%-20s dark-third mean hue %6.1f (target 240-260)  dark px used %5.1f%%  share hue230-270 in dark %5.1f%%  magenta share %5.2f%% (<=10)  mean val %.2f  %s' % (n, mh, dk.mean() * 100, blue, mag, v.mean(), 'OK' if ok else 'OUT'))
txt = '\n'.join(rows) + '\n'; print(txt)
if not pre: open(os.path.join(HERE, 'hue_report.txt'), 'w').write(txt)
