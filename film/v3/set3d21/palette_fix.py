#!/usr/bin/env python3
"""palette check of the far-wide views: valley_wide (preset), P_A and P_TOP (named poses in one world) as drafts 360x640 side by side -> styleboard/palette_fix.jpg, with sat / vivid % / luma
(qa_stats metric at 90x160). usage: python3 palette_fix.py [samples]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, bpy, stirling as K
from PIL import Image, ImageDraw, ImageFont
smp = int(sys.argv[1]) if len(sys.argv) > 1 else 20; out = []; rows = []
def stats(f):
    a = np.asarray(Image.open(f).convert('RGB').resize((90, 160), Image.BILINEAR), float); mx = a.max(-1); mn = a.min(-1); sat = (mx - mn) / (mx + 1e-3); return sat.mean(), (sat > 0.5).mean() * 100, a.mean()
A = K.build_world(['valley_wide'], scots_wide=True)
for n in ('P_A', 'P_TOP'):
    K.cam_path(None, [(0, n), (1, n)], 0); f = os.path.join(HERE, 'styleboard', 'palette_%s.png' % n); K.render(f, 'draft', smp); out.append((n, f))
import subprocess
f = os.path.join(HERE, 'styleboard', 'palette_valley_wide.png'); subprocess.run([sys.executable, os.path.join(HERE, 'stirling.py'), 'render', 'valley_wide', '-', f, 'draft', str(smp)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); out.insert(0, ('valley_wide', f))
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15); S = Image.new('RGB', (360 * 3 + 16, 640), (18, 18, 22))
for i, (n, f) in enumerate(out):
    im = Image.open(f).convert('RGB'); sa, vv, lu = stats(f); ImageDraw.Draw(im).text((6, 6), '%s sat %.2f vivid %.0f%% luma %.0f' % (n, sa, vv, lu), fill=(255, 255, 255), font=F); S.paste(im, (i * 368, 0)); print(n, 'sat %.3f vivid %.1f luma %.1f' % (sa, vv, lu))
S.save(os.path.join(HERE, 'styleboard', 'palette_fix.jpg'), quality=90)
