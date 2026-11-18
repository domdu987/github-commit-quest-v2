#!/usr/bin/env python3
"""Hue rows (v3/tools/hue_report.py stats) per frame + the SHADE HUE of each frame (chroma-weighted circular mean hue of the shaded pixels:
value 0.10..0.55, saturation > 0.2, blue >= red = the painted shade, not dark wood) and the MAGENTA share. Client rules: shade hue 240-260,
magenta <= 10 %. usage: python3 dairy_hue.py <png | folder ...> ; writes dairy_work/hue_rows.txt and dairy_work/hue.json"""
import sys, os, glob, math, json, io, contextlib
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
import hue_report as H
def shade_hue(f):
    im = np.asarray(Image.open(f).convert('RGB').resize((180, 320)), dtype=float) / 255; im = np.concatenate([im[:212], im[240:]])      # skip the caption band rows 212..240 of 320 (y 848..960)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]; mx = im.max(-1); mn = im.min(-1); d = mx - mn; s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    hr = ((g - b) / np.maximum(d, 1e-9)) % 6; hg = (b - r) / np.maximum(d, 1e-9) + 2; hb = (r - g) / np.maximum(d, 1e-9) + 4
    h = np.where(mx == r, hr, np.where(mx == g, hg, hb)) * 60
    sel = (mx > 0.10) & (mx < 0.55) & (s > 0.2) & (b >= r); w = (s * mx)[sel]
    if w.sum() == 0: return float('nan'), 0.0
    a = np.radians(h[sel]); m = math.degrees(math.atan2((np.sin(a) * w).sum(), (np.cos(a) * w).sum())) % 360
    return m, float(sel.mean())
if __name__ == '__main__':
    fs = [f for a in (sys.argv[1:] or [os.path.join(HERE, 'dairy_work', 'final')]) for f in H.files_of(a)]; out = []; buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'frame':34s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for f in fs:
            H.row(os.path.basename(f)[:-4], [f]); hh, sat, val, dk = H.stats([f]); m, fr = shade_hue(f)
            out.append(dict(file=os.path.basename(f), shade_hue=round(m, 1), shaded_frac=round(fr, 2), magenta=round(hh['magenta'], 1), violet=round(hh['violet'], 1), blue=round(hh['blue'], 1), red=round(hh['red'], 1), orange=round(hh['orange'], 1), sat=round(sat, 2), val=round(val, 2), dark=round(dk, 2)))
        print('\nshade hue (target 240-260), shaded fraction, magenta share (target <= 10 %):')
        for o in out: print('  %-30s shade hue %6.1f  shaded %.2f  magenta %5.1f %%  %s' % (o['file'][:-4], o['shade_hue'], o['shaded_frac'], o['magenta'], 'ok' if 240 <= o['shade_hue'] <= 260 and o['magenta'] <= 10 else 'OUT'))
    txt = buf.getvalue(); print(txt); os.makedirs(os.path.join(HERE, 'dairy_work'), exist_ok=True)
    open(os.path.join(HERE, 'dairy_work', 'hue_rows.txt'), 'w').write(txt); json.dump(out, open(os.path.join(HERE, 'dairy_work', 'hue.json'), 'w'), indent=1)
