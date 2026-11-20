"""board.jpg: the 3 stills side by side, one Latin label line under each."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
items = [('sb1_site', 'SITE: Champ de Mars 1888, first platform rising'),
         ('sb2_tower_dusk', 'TOWER: 1909 dusk, antenna and spark gap'),
         ('sb3_resto', 'RESTO: first-floor restaurant, 1889')]
W, H, LB, G = 720, 1280, 84, 16
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
S = Image.new('RGB', (W * 3 + G * 4, H + LB + G * 2), (22, 22, 26)); d = ImageDraw.Draw(S)
for i, (n, lab) in enumerate(items):
    x = G + i * (W + G); S.paste(Image.open(os.path.join(HERE, n + '.jpg')).convert('RGB'), (x, G))
    d.text((x + 4, G + H + 14), lab, fill=(235, 235, 235), font=F)
S.save(os.path.join(HERE, 'board.jpg'), quality=90); print(S.size)
