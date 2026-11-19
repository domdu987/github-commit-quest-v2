"""contact.jpg (5 columns, 720x1280 tiles, label strip UNDER each, cyan y-880 line) + contact_small.jpg (1/3) from work/final/ in work/contact_order.txt order;
also hue_rows.txt (hue families + shade hue per tile, via chicago_hue.py)."""
import os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chicago_hue as HU
rows_ = [l.strip().split('|') for l in open(os.path.join(HERE, 'work/contact_order.txt')) if l.strip()]
W, H, LB, C = 720, 1280, 56, 5
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
rows = (len(rows_) + C - 1) // C; S = Image.new('RGB', (W * C, (H + LB) * rows), (16, 16, 20)); d = ImageDraw.Draw(S); out = []
for i, (spec, lab) in enumerate(rows_):
    f = os.path.join(HERE, 'work/final', spec.replace(':', '_').replace(',', '-') + '.png')
    im = Image.open(f).convert('RGB'); x, y = (i % C) * W, (i // C) * (H + LB)
    S.paste(im, (x, y)); d.line([(x, y + 880), (x + W, y + 880)], fill=(0, 230, 255), width=2); d.text((x + 10, y + H + 10), lab, fill=(235, 235, 235), font=F)
    m, fr = HU.shade_hue(f); fam = HU.families(f)
    mg = fam['magenta']; out.append('%-36s shade hue %6.1f (shaded %.2f) %s | magenta %4.1f%% %s | %s' % (spec, m, fr, 'ok' if 240 <= m <= 260 else 'OUT', mg, 'ok' if mg <= 10 else 'OVER', ' '.join('%s %.0f' % (k[:3], v) for k, v in fam.items())))
S.save(os.path.join(HERE, 'contact.jpg'), quality=88); S.resize((S.width // 3, S.height // 3), Image.LANCZOS).save(os.path.join(HERE, 'contact_small.jpg'), quality=88)
open(os.path.join(HERE, 'hue_rows.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out)); print(S.size, len(rows_))
