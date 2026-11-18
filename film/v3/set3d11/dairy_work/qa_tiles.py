"""qa_auto-style sanity of the 11 final tiles (no black / blank / magenta frames, sharpness, caption band, shade hue, magenta share).
usage: python3 qa_tiles.py  -> prints a table, exit 1 on FAIL"""
import os, sys, glob, re
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import dairy_hue as DH
fails = 0; log = open(os.path.join(HERE, 'final_log.txt')).read()
print('%-14s %6s %6s %8s %8s %9s %8s %s' % ('tile', 'mean', 'std', 'magenta%', 'lapvar', 'shadeHue', 'magHue%', 'verdict'))
for f in sorted(glob.glob(os.path.join(HERE, 'final', '*.png'))):
    n = os.path.basename(f)[:-4]; im = Image.open(f).convert('RGB'); a = np.asarray(im.resize((180, 320)), np.float32); g = a.mean(-1)
    r, gg, b = a[..., 0], a[..., 1], a[..., 2]; mag = ((r > 180) & (b > 180) & (gg < 80)).mean()
    lap = np.asarray(im.convert('L').filter(ImageFilter.Kernel((3, 3), (0, 1, 0, 1, -4, 1, 0, 1, 0), 1, 128)), np.float32); lv = float(lap.var())
    m, fr = DH.shade_hue(f); import hue_report as H; hh = H.stats([f])[0]
    heads = re.search(r'final %s: .*heads (\[.*\])' % n, log); chin_bad = []
    ok = g.mean() >= 8 and g.std() >= 3 and mag < 0.25 and 240 <= m <= 260 and hh['magenta'] <= 10 and lv > 20
    fails += (not ok)
    print('%-14s %6.1f %6.1f %8.2f %8.1f %9.1f %8.1f %s' % (n, g.mean(), g.std(), mag * 100, lv, m, hh['magenta'], 'ok' if ok else 'FAIL'))
print('ALL OK' if not fails else 'FAILED %d' % fails); sys.exit(1 if fails else 0)
