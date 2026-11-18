"""side-by-side elephants_test.jpg (3 stills, one-line label under each, cyan line at y 880 like the contact sheet) + phone-size version"""
import os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
T = [('s1_NIGHT.png', 'fence_low_night NIGHT: matriarch arrives, herd + calf'), ('s2_NIGHT.png', 'push_side NIGHT push 0.5: chest on the wire, bees'), ('s3_NIGHT.png', 'trunk_close NIGHT: alarmed, bee swarm at eye + trunk')]
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except Exception: f = ImageFont.load_default()
G = 16; LH = 56; W = 3 * 720 + 4 * G; Hh = 1280 + LH + 2 * G
sh = Image.new('RGB', (W, Hh), (24, 22, 30)); d = ImageDraw.Draw(sh)
for i, (fn, lab) in enumerate(T):
    im = Image.open(os.path.join(H, fn)).convert('RGB'); x = G + i * (720 + G); sh.paste(im, (x, G)); d.line([(x, G + 880), (x + 719, G + 880)], fill=(0, 220, 230), width=1)
    d.text((x + 6, G + 1280 + 12), lab, fill=(235, 235, 240), font=f)
sh.save(os.path.join(H, 'elephants_test.jpg'), quality=93)
sh.resize((W // 3, Hh // 3), Image.LANCZOS).save(os.path.join(H, 'elephants_test_small.jpg'), quality=90)
# phone size: each still at 360x640
ph = Image.new('RGB', (3 * 360 + 4 * 8, 640 + 8 * 2), (24, 22, 30))
for i, (fn, _) in enumerate(T): ph.paste(Image.open(os.path.join(H, fn)).convert('RGB').resize((360, 640), Image.LANCZOS), (8 + i * 368, 8))
ph.save(os.path.join(H, 'elephants_phone.jpg'), quality=92)
