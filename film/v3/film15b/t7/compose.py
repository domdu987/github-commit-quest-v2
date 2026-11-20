#!/usr/bin/env python3
"""compose.py Q : bakes the sky-to-sky dissolve (g 1938..1965, smoothstep), light violet-shade grade, encodes take.mkv (draft: nearest rendered frame)."""
import sys, os, glob, subprocess, json
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); q = sys.argv[1]
FIRST, LAST, D0, D1 = 1796, 2100, 1938, 1965
def avail(part): return sorted(int(os.path.basename(f)[2:6]) for f in glob.glob('%s/work/%s_%s/g_*.png' % (HERE, part, q)))
AB, AA = avail('B'), avail('A')
def load(part, av, g):
    gg = min(av, key=lambda x: abs(x - g)); return np.asarray(Image.open('%s/work/%s_%s/g_%04d.png' % (HERE, part, q, gg)).convert('RGB')).astype(np.float32) / 255
def grade(a, k):
    l = a.mean(-1, keepdims=True); w = np.clip((0.55 - l) / 0.55, 0, 1) * k
    a = a * np.concatenate([1 + 0.05 * w, 1 - 0.04 * w, 1 + 0.12 * w], -1); return np.clip(a, 0, 1)
out = '%s/work/final_%s' % (HERE, q); os.makedirs(out, exist_ok=True)
for g in range(FIRST, LAST + 1):
    if g < D0: im = load('B', AB, g)
    elif g > D1: im = grade(load('A', AA, g), 1.0)
    else:
        a = smooth = (g - D0) / (D1 - D0); a = a * a * (3 - 2 * a); im = load('B', AB, g) * (1 - a) + grade(load('A', AA, g), 1.0) * a
    Image.fromarray((im * 255 + 0.5).astype(np.uint8)).save('%s/g_%04d.png' % (out, g))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '30', '-start_number', str(FIRST), '-i', out + '/g_%04d.png', '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', '%s/take%s.mkv' % (HERE, '' if q == 'final' else '_draft')], check=True)
print('ok', LAST - FIRST + 1)
