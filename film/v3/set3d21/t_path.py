#!/usr/bin/env python3
"""camera-path test: one world scene (build_world), the camera flies valley_wide -> camp_wide -> hill_low with cam_path; 12 draft frames -> styleboard/path_strip.jpg
(checks: smooth positions, no jump in the VIVID grade, scene stays one piece). Prints the max step in position per frame and the vivid values."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, bpy, stirling as K
from PIL import Image
A = K.build_world(['valley_wide', 'camp_wide', 'hill_low'], fg=False)
keys = [(0, 'valley_wide'), (45, 'camp_wide'), (90, 'hill_low')]; frames = [int(round(i * 90 / 11)) for i in range(12)]; ims = []; last = None; steps = []; viv = []
for g in frames:
    r = K.cam_path(None, keys, g); p = np.array(r['loc']); steps.append(0 if last is None else float(np.linalg.norm(p - last))); last = p; viv.append(r['vivid'])
    f = os.path.join(HERE, 'styleboard', 'path_%02d.png' % g); K.render(f, 'draft', 16); ims.append(Image.open(f).convert('RGB').resize((180, 320), Image.LANCZOS))
S = Image.new('RGB', (180 * 12 + 11 * 4, 320), (18, 18, 22))
for i, im in enumerate(ims): S.paste(im, (i * 184, 0))
S.save(os.path.join(HERE, 'styleboard', 'path_strip.jpg'), quality=90)
print('frames', frames); print('steps', [round(x, 1) for x in steps]); print('vivid', [(round(a, 2), round(b, 2)) for a, b in viv]); print('ok')
