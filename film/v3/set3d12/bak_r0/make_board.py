#!/usr/bin/env python3
"""styleboard/board.jpg: the three stills side by side (2160 x 1280) with a thin label under each. usage: python3 make_board.py"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sb = os.path.join(HERE, 'styleboard')
items = [('sb1_street_wide.png', 'sb1  street_wide: hook, eye level, hero under the umbrella, coach rank right'),
         ('sb2_coach_low.png', 'sb2  coach_low: low angle at the coach rank, puddle reflections'),
         ('sb3_street_high.png', 'sb3  street_high: high angle, roofs, chimneys, umbrellas (the later whole-street shot)')]
board = Image.new('RGB', (2160, 1280), (16, 14, 24)); dr = ImageDraw.Draw(board)
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
except Exception: font = ImageFont.load_default()
for i, (fn, lab) in enumerate(items):
    im = Image.open(os.path.join(sb, fn)).convert('RGB'); h = 1244; w = round(im.width * h / im.height); im = im.resize((w, h), Image.LANCZOS)
    board.paste(im, (i * 720 + (720 - w) // 2, 0)); dr.text((i * 720 + 12, 1244 + 10), lab, fill=(226, 214, 196), font=font)
board.save(os.path.join(sb, 'board.jpg'), quality=90)
print('board.jpg', board.size)
