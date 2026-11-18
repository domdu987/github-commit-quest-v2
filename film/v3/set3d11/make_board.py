#!/usr/bin/env python3
"""style_board.jpg: the 3 stills (480x853 each) side by side with a label strip under each (latin letters only)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, 'board')
LAB = dict(A='A  cowshed, golden morning (KEY)', B='B  village exterior, low angle', C='C  cowshed, late amber (ALT)')
S = Image.new('RGB', (480 * 3 + 8 * 2, 853 + 56), (28, 24, 36)); d = ImageDraw.Draw(S)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
except Exception: f = ImageFont.load_default()
for i, k in enumerate('ABC'):
    x = i * 488; S.paste(Image.open(os.path.join(B, 'still_%s.png' % k)).convert('RGB').resize((480, 853), Image.LANCZOS), (x, 0)); d.text((x + 12, 853 + 14), LAB[k], fill=(244, 226, 190), font=f)
S.save(os.path.join(B, 'style_board.jpg'), quality=92); print(S.size)
