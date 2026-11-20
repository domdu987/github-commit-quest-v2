#!/usr/bin/env python3
"""splash strip: river_low with ONE crown (size 1.8) rendered at ages 0.1 / 0.25 / 0.4 / 0.6 / 0.9 (draft 360x640, 40 samples), side by side -> styleboard/splash_strip.jpg"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, stirling as K
from PIL import Image
A = K.build_for_cli('river_low'); pr = K.PRESETS['river_low']
for o in [o for o in bpy.data.objects if o.name.startswith('splash_')]: bpy.data.objects.remove(o, do_unlink=True)
x, y, _ = pr['splashes'][1]; ages = [0.1, 0.25, 0.4, 0.6, 0.9]; ims = []
for a in ages:
    K.splash(x, y, a, 1.8, name='s', seed=3); out = os.path.join(HERE, 'styleboard', 'splash_%02d.png' % int(a * 100)); K.render(out, 'draft', 40); ims.append(Image.open(out).convert('RGB'))
S = Image.new('RGB', (360 * 5 + 16, 640), (18, 18, 22))
for i, im in enumerate(ims): S.paste(im, (i * 364, 0))
S.save(os.path.join(HERE, 'styleboard', 'splash_strip.jpg'), quality=90); print('ok')
