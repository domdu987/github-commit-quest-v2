#!/usr/bin/env python3
"""deliver.py: encode take.mkv from frames/, run qa_auto + qa_stats2, contact.jpg (every 6th frame, cyan line y 880), frame-diff numbers.
usage: python3 deliver.py FIRST_G LAST_G CUTS(comma, may be empty)"""
import sys, os, subprocess, glob, json
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
f0, f1 = int(sys.argv[1]), int(sys.argv[2]); cuts = sys.argv[3] if len(sys.argv) > 3 else ''
fr = os.path.join(HERE, 'frames')
missing = [g for g in range(f0, f1 + 1) if not os.path.exists(os.path.join(fr, 'g_%04d.png' % g))]
if missing: sys.exit('missing frames %s' % missing[:10])
mkv = os.path.join(HERE, 'take.mkv')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(f0), '-i', os.path.join(fr, 'g_%04d.png'), '-frames:v', str(f1 - f0 + 1),
                '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', mkv], check=True)
print('take.mkv', os.path.getsize(mkv) / 1e6, 'MB')
r = subprocess.run(['python3', os.path.join(PROJ, 'qa_auto.py'), mkv, '--first_g', str(f0)] + (['--cuts', cuts] if cuts else []), capture_output=True, text=True)
print(r.stdout[-2500:], r.stderr[-500:])
r = subprocess.run(['python3', os.path.join(PROJ, 'qa_stats2.py'), mkv], capture_output=True, text=True); print(r.stdout, r.stderr[-300:])
# contact sheet
gs = list(range(f0, f1 + 1, 6)); cols = 8; w, h = 180, 320; rows = (len(gs) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(fr, 'g_%04d.png' % g)).convert('RGB').resize((w, h)); d = ImageDraw.Draw(im)
    d.line([(0, int(880 / 4)), (w, int(880 / 4))], fill=(0, 255, 255)); d.text((3, 3), str(g), fill=(255, 255, 0)); S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(os.path.join(HERE, 'contact.jpg'), quality=85)
# in-shot frame diff on 90x160 grey, excluding the handle frames' neighbours of cuts
a = np.array([np.asarray(Image.open(os.path.join(fr, 'g_%04d.png' % g)).convert('L').resize((90, 160)), dtype=np.float32) for g in range(f0, f1 + 1)])
d = np.abs(np.diff(a, axis=0)).mean((1, 2))
print('frame-diff 90x160 grey: median %.2f p90 %.2f min %.2f (n=%d)' % (np.median(d), np.percentile(d, 90), d.min(), len(d)))
json.dump(dict(median=float(np.median(d)), p90=float(np.percentile(d, 90))), open(os.path.join(HERE, 'framediff.json'), 'w'))
