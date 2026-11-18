"""contact.jpg (8 columns, 720x1280 tiles, label strip UNDER each image, cyan y-880 line) + contact_small.jpg (1/3) from farm_work/final/ in farm_work/contact_order.txt order (spec|label).
usage: python3 make_contact.py"""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.join(HERE, 'farm_work')
rows_ = [l.strip().split('|') for l in open(os.path.join(WK, 'contact_order.txt')) if l.strip()]
def tag(spec):
    p = spec.split(':'); return '%s_%s_%s' % (p[0], p[1], p[2].replace(',', '_').replace('/', '-')) if len(p) > 2 else '%s_%s' % (p[0], p[1])
W, H, LB, C = 720, 1280, 56, 8
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
rows = (len(rows_) + C - 1) // C
S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S)
for i, (spec, lab) in enumerate(rows_):
    im = Image.open(os.path.join(WK, 'final', tag(spec) + '.png')).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
    S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2); d.text((x + 10, y + H + 12), lab, fill=(235, 235, 235), font=F)
S.save(os.path.join(HERE, 'contact.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=88)
print(S.size, len(rows_))
