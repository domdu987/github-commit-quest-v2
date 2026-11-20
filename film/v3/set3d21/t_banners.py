#!/usr/bin/env python3
"""banner / smoke check: camp_wide -> camp_bank through the camp (world scene, drafts), banners and smoke near the path hidden with hide_near_banners -> styleboard/banner_strip.jpg"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np, bpy, stirling as K
from PIL import Image
A = K.build_world(['camp_wide', 'camp_bank'], fg=False); keys = [(0, 'camp_wide'), (30, (-60, -70, 9), (-20, -40, 2), 22.0), (60, 'camp_bank')]; pts = [K.cam_path(None, keys, g)['loc'] for g in range(0, 61, 3)]
print('hidden banners, plumes:', K.hide_near_banners(pts, 15.0)); ims = []
for g in (0, 12, 24, 36, 48, 60):
    K.cam_path(None, keys, g); f = os.path.join(HERE, 'styleboard', 'ban_%02d.png' % g); K.render(f, 'draft', 16); ims.append(Image.open(f).convert('RGB').resize((240, 427)))
S = Image.new('RGB', (244 * 6, 427), (18, 18, 22)); [S.paste(im, (i * 244, 0)) for i, im in enumerate(ims)]; S.save(os.path.join(HERE, 'styleboard', 'banner_strip.jpg'), quality=90); print('ok')
