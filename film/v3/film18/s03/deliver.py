#!/usr/bin/env python3
"""deliver.py <g0> <g1> <first_g> <last_g> <trans_type> <trans_frames> : take.mkv, meta.json, frame-diff numbers, contact.jpg, qa_auto (in-shot numbers -> framediff.json)."""
import sys, os, json, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
g0, g1, first, last = map(int, sys.argv[1:5]); tt = sys.argv[5]; tf = int(sys.argv[6])
fr = os.path.join(HERE, 'frames')
miss = [g for g in range(first, last + 1) if not os.path.exists(os.path.join(fr, 'g_%04d.png' % g))]
assert not miss, 'missing frames %s' % miss[:10]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(first), '-i', os.path.join(fr, 'g_%04d.png'), '-frames:v', str(last - first + 1),
                '-c:v', 'libx264rgb', '-crf', '20', '-preset', 'slow', os.path.join(HERE, 'take.mkv')], check=True)
meta = dict(g0=g0, g1=g1, first_g=first, n_frames=last - first + 1, transition_in=dict(type=tt, frames=tf))
json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w'), indent=1)
def grey(g): return np.asarray(Image.open(os.path.join(fr, 'g_%04d.png' % g)).convert('L').resize((90, 160), Image.BILINEAR), dtype=np.float32)
gs = list(range(g0, g1)); G = [grey(g) for g in gs]
d = np.array([np.abs(G[i + 1] - G[i]).mean() for i in range(len(G) - 1)])
runs = 0; worst = 0
for v in d:
    runs = runs + 1 if v < 0.35 else 0; worst = max(worst, runs)
fd = dict(median=float(np.median(d)), p90=float(np.percentile(d, 90)), min=float(d.min()), max=float(d.max()), longest_near_static_run=worst, n=len(d))
json.dump(fd, open(os.path.join(HERE, 'framediff.json'), 'w'), indent=1); print(fd)
# contact sheet: one tile per 0.5 s of the shot
idx = gs[::15] if len(gs) > 15 else gs; idx = idx[:12]
W, H = 180, 320; sheet = Image.new('RGB', (W * len(idx), H))
for i, g in enumerate(idx): sheet.paste(Image.open(os.path.join(fr, 'g_%04d.png' % g)).resize((W, H)), (i * W, 0))
sheet.save(os.path.join(HERE, 'contact.jpg'), quality=88)
