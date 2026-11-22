#!/usr/bin/env python3
"""deliver.py -- encode take.mkv (handles included), meta.json, frame-diff numbers; run qa_auto separately.
    python3 deliver.py [trans_type trans_frames]"""
import os, sys, json, subprocess, glob
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('shot_consts', os.path.join(HERE, 'shot.py'))
src = open(os.path.join(HERE, 'shot.py')).read()
ns = {}
for line in src.splitlines():                                   # read the constants without importing bpy
    for k in ('NAME', 'G0', 'G1', 'H_IN', 'H_OUT'):
        if line.startswith(k + ',') or line.startswith(k + ' =') or line.startswith('G0, G1'):
            pass
import re
NAME = re.search(r"^NAME = '(\w+)'", src, re.M).group(1)
G0, G1 = [int(x) for x in re.search(r"^G0, G1 = (\d+), (\d+)", src, re.M).groups()]
H_IN, H_OUT = [int(x) for x in re.search(r"^H_IN, H_OUT = (\d+), (\d+)", src, re.M).groups()]
FR = os.path.join(HERE, 'frames')
first, last = G0 - H_IN, G1 + H_OUT - 1
miss = [g for g in range(first, last + 1) if not os.path.exists(os.path.join(FR, 'g_%04d.png' % g))]
assert not miss, 'missing frames %s' % miss[:10]
mkv = os.path.join(HERE, 'take.mkv')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(first), '-i', os.path.join(FR, 'g_%04d.png'),
                '-c:v', 'libx264rgb', '-crf', '21', '-preset', 'slow', mkv], check=True)
# frame diff, in-shot frames only (g0..g1-1), 90x160 grey
def grey(g):
    im = Image.open(os.path.join(FR, 'g_%04d.png' % g)).convert('L').resize((90, 160), Image.BILINEAR)
    return np.asarray(im, np.float32)
gs = list(range(G0, G1))
G = [grey(g) for g in gs]
d = np.array([np.abs(G[i + 1] - G[i]).mean() for i in range(len(G) - 1)])        # mean abs diff x255 (values already 0..255)
st = dict(median=round(float(np.median(d)), 2), p90=round(float(np.percentile(d, 90)), 2), min=round(float(d.min()), 2), max=round(float(d.max()), 2), n=len(d), frames_lt1=int((d < 1.0).sum()))
heads = {}
for g in range(first, last + 1):
    js = os.path.join(FR, 'g_%04d.json' % g)
    if os.path.exists(js):
        for k, v in json.load(open(js)).get('heads', {}).items(): heads[k] = max(heads.get(k, 0), v)
tt = sys.argv[1] if len(sys.argv) > 1 else 'cut'; tf = int(sys.argv[2]) if len(sys.argv) > 2 else 0
cpu = [json.load(open(p)).get('wall', 0) for p in glob.glob(os.path.join(FR, 'g_*.json'))]
meta = dict(shot=NAME, g0=G0, g1=G1, first_g=first, n_frames=last - first + 1, transition_in=dict(type=tt, frames=tf), framediff=st, max_chin_y=heads,
            s_per_frame=round(float(np.mean(cpu)), 1) if cpu else None)
json.dump(meta, open(os.path.join(HERE, 'meta.json'), 'w'), indent=1)
print(json.dumps(meta))
