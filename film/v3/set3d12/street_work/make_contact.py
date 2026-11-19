"""contact.jpg (5 columns, 720x1280 tiles, label strip UNDER each, cyan y-880 line) + contact_small.jpg (1/3) from final/ in render_tiles.TILES order; hue rows -> hue_rows.txt."""
import os, sys, io, contextlib
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from render_tiles import TILES
import street_hue as SH
W, H, LB, C = 720, 1280, 56, 5
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
tl = [t for t in TILES if os.path.exists(os.path.join(HERE, 'final', t[0] + '.png'))]
LAB = lambda t: t[7]
rows = (len(tl) + C - 1) // C; S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, t in enumerate(tl):
    im = Image.open(os.path.join(HERE, 'final', t[0] + '.png')).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
    S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2); d.text((x + 10, y + H + 12), '%s  %s' % (t[0][:2], t[7]), fill=(235, 235, 235), font=F)
S.save(os.path.join(os.path.dirname(HERE), 'contact.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(os.path.dirname(HERE), 'contact_small.jpg'), quality=88)
print(S.size, len(tl))
fl = [os.path.join(HERE, 'final', t[0] + '.png') for t in tl]; print(SH.main(fl, os.path.join(HERE, 'hue_rows.txt')))
