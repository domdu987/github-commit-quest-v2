#!/usr/bin/env python3
"""deliver11.py -- s11 v2: encode take.mkv (crf 21) from raw/, frame diff (90x160 grey, bilinear, in-shot g 853..943), meta.json."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); FR = os.path.join(HERE, 'raw'); G0, G1, first, last = 853, 944, 853, 951
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(first), '-i', os.path.join(FR, 'g_%04d.png'), '-c:v', 'libx264rgb', '-crf', '21', '-preset', 'slow', os.path.join(HERE, 'take.mkv')], check=True)
G = [np.asarray(Image.open(os.path.join(FR, 'g_%04d.png' % g)).convert('L').resize((90, 160), Image.BILINEAR), np.float32) for g in range(G0, G1)]
d = np.array([np.abs(G[i + 1] - G[i]).mean() for i in range(len(G) - 1)])
fd = dict(median=round(float(np.median(d)), 2), p90=round(float(np.percentile(d, 90)), 2), min=round(float(d.min()), 2), max=round(float(d.max()), 2), n=len(d), frames_lt1=int((d < 1.0).sum()))
m = json.load(open(os.path.join(HERE, 'meta.json'))); m['framediff_median'] = fd['median']; m['framediff_p90'] = fd['p90']; m['framediff'] = fd; m['first_g'] = first
json.dump(m, open(os.path.join(HERE, 'meta.json'), 'w'), indent=1); print(json.dumps(fd))
