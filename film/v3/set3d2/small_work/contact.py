"""contact.py : small_contact.jpg = every camera x preset still (360x640, placeholder actors) with labels + the reference frames."""
import os, glob
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); SET2 = os.path.dirname(HERE); PROJ = os.path.dirname(os.path.dirname(SET2))
rows = [('vault LANTERN', ['vault_LANTERN_%s' % c for c in ('dolly_barrels', 'stair_high', 'barrel_insert', 'crack_follow')]),
        ('vault BURN', ['vault_BURN_%s' % c for c in ('dolly_barrels', 'stair_high', 'barrel_insert', 'crack_follow')]),
        ('room DAWN / NIGHT', ['room_DAWN_%s' % c for c in ('push_rod', 'book_insert', 'room_wide')] + ['room_NIGHT_push_rod']),
        ('room NIGHT + refs', ['room_NIGHT_book_insert', 'room_NIGHT_room_wide', 'REF a/t0010', 'REF a/t0080']),
        ('refs', ['REF a/t0088', 'REF b/t0049', 'REF b/t0085', 'REF b/t0019'])]
W, H, G = 360, 640, 6; font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
sheet = Image.new('RGB', (4 * (W + G), len(rows) * (H + G)), (24, 22, 28)); d = ImageDraw.Draw(sheet)
for r, (_, names) in enumerate(rows):
    for c, n in enumerate(names):
        p = os.path.join(PROJ, 'ref', n[4:] + '.jpg') if n.startswith('REF') else os.path.join(HERE, 'stills', n + '.png')
        im = Image.open(p).convert('RGB').resize((W, H), Image.LANCZOS); x, y = c * (W + G), r * (H + G); sheet.paste(im, (x, y))
        d.rectangle((x, y, x + W, y + 26), fill=(0, 0, 0)); d.text((x + 6, y + 3), n.replace('_', ' '), fill=(255, 255, 255), font=font)
sheet.save(os.path.join(SET2, 'small_contact.jpg'), quality=86); print(sheet.size)
