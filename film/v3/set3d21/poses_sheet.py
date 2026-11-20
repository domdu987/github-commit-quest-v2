#!/usr/bin/env python3
"""renders one draft of each named join pose (K.POSES) in one world scene -> styleboard/poses.jpg (labelled)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import bpy, stirling as K
from PIL import Image, ImageDraw, ImageFont
A = K.build_world(['camp_wide', 'camp_bank', 'bridge_end_north', 'hill_low'], fg=False); names = ['P_A', 'P_CAMP', 'P_BANK', 'P_NECK', 'P_TOP']; ims = []
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
for n in names:
    K.cam_path(None, [(0, n), (1, n)], 0); f = os.path.join(HERE, 'styleboard', 'pose_%s.png' % n); K.render(f, 'draft', 20); im = Image.open(f).convert('RGB'); ImageDraw.Draw(im).text((8, 8), n, fill=(255, 255, 255), font=F); ims.append(im)
S = Image.new('RGB', (360 * 5 + 16, 640), (18, 18, 22))
for i, im in enumerate(ims): S.paste(im, (i * 364, 0))
S.save(os.path.join(HERE, 'styleboard', 'poses.jpg'), quality=90); print('ok')
