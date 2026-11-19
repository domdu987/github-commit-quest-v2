"""assemble raw/GOLDEN + raw/DAY -> frames/g_%04d.png (season dissolve g 897..907 blended), then take.mkv"""
import os, sys, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); G0, G1, D0, D1 = 483, 939, 897, 907
os.makedirs(os.path.join(HERE, 'frames'), exist_ok=True)
def sm(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)
for g in range(G0, G1 + 1):
    gold = os.path.join(HERE, 'raw', 'GOLDEN', 'g_%04d.png' % g); day = os.path.join(HERE, 'raw', 'DAY', 'g_%04d.png' % g)
    out = os.path.join(HERE, 'frames', 'g_%04d.png' % g)
    if g < D0: src = Image.open(gold).convert('RGB')
    elif g > D1: src = Image.open(day).convert('RGB')
    else:
        u = sm((g - (D0 - 1)) / float(D1 - D0 + 2)); a = np.asarray(Image.open(gold).convert('RGB'), np.float32); b = np.asarray(Image.open(day).convert('RGB'), np.float32)
        src = Image.fromarray(np.clip(a * (1 - u) + b * u + .5, 0, 255).astype(np.uint8))
    src.save(out)
subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-start_number', str(G0), '-i', os.path.join(HERE, 'frames', 'g_%04d.png'), '-c:v', 'libx264rgb', '-crf', '6', '-preset', 'slow', os.path.join(HERE, 'take.mkv')])
print('ok', os.path.getsize(os.path.join(HERE, 'take.mkv')))
