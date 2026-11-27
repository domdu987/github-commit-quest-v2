#!/usr/bin/env python3
"""contact sheet of finals/*.png : label under each tile, cyan line at y 880 (caption band).  python3 contact.py [out.jpg] [preset ...]"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1] if len(sys.argv) > 1 else H + '/contact.jpg'
sys.path.insert(0, H); import set25
names = sys.argv[2:] or [n for n in set25.registry() if os.path.exists(f'{H}/finals/{n}.png')]
tw, th, lab, cols = 240, 427, 22, 6; rows = (len(names) + cols - 1) // cols
W = Image.new('RGB', (cols * tw, rows * (th + lab)), (24, 24, 24)); d = ImageDraw.Draw(W)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 13)
except Exception: f = ImageFont.load_default()
for i, n in enumerate(names):
    im = Image.open(f'{H}/finals/{n}.png').convert('RGB').resize((tw, th), Image.LANCZOS); x, y = (i % cols) * tw, (i // cols) * (th + lab); W.paste(im, (x, y))
    d.line([(x, y + round(880 * th / 1280)), (x + tw, y + round(880 * th / 1280))], fill=(0, 255, 255), width=1); d.text((x + 4, y + th + 3), n, fill=(255, 255, 255), font=f)
W.save(out, quality=88); print(out, len(names))
