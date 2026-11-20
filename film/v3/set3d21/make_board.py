#!/usr/bin/env python3
"""style board: copies styleboard/<preset>.png to still1..3.png (hill_over, camp_bank, valley_loop) and builds styleboard/board.jpg side by side
(720x1280 each, a label strip, cyan line at y 880 = top of the caption band). usage: python3 make_board.py"""
import os, shutil
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, 'styleboard')
ST = [('hill_over', 'still1.png', '1  hill_over  (hook: over the Scots down to the bridge)'), ('camp_bank', 'still2.png', '2  camp_bank  (Cressingham across the river)'), ('valley_loop', 'still3.png', '3  valley_loop  (the loop is the bottle, the bridge its neck)')]
for p, out, _ in ST: shutil.copyfile(os.path.join(D, p + '.png'), os.path.join(D, out))
W, H, LB, G = 720, 1280, 64, 14
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
S = Image.new('RGB', (W * 3 + G * 2, H + LB), (18, 18, 22)); dr = ImageDraw.Draw(S)
for i, (p, out, lab) in enumerate(ST):
    im = Image.open(os.path.join(D, out)).convert('RGB'); x = i * (W + G); S.paste(im, (x, 0)); dr.line([(x, 880), (x + W, 880)], fill=(0, 230, 255), width=2); dr.line([(x, 950), (x + W, 950)], fill=(0, 230, 255), width=2)
    dr.text((x + 12, H + 16), lab, fill=(230, 230, 235), font=F)
S.save(os.path.join(D, 'board.jpg'), quality=90); print('board.jpg', S.size)
