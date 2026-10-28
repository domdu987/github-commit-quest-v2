# headline.py OUT.png "LINE1" "LINE2(red)" [y] : a series-style paper strip headline (Kanit Black), transparent 1080x1920, for the cold-open hook / covers
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W = "/tmp/claude-0/-home-user-github-commit-quest-v2/49762ff1-991c-52d3-b168-9c16af55ac24/scratchpad/work"
out, l1, l2 = sys.argv[1], sys.argv[2], sys.argv[3]
y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 250
big = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
x0 = int(sys.argv[6]) if len(sys.argv) > 6 else None
F = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f3.ttf", int(92 * big), layout_engine=ImageFont.Layout.RAQM)
F2 = ImageFont.truetype(f"{W}/hf/fence1/assets/fonts/f3.ttf", int(118 * big), layout_engine=ImageFont.Layout.RAQM)
canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
# measure
d0 = ImageDraw.Draw(canvas)
b1 = d0.textbbox((0, 0), l1, font=F, language="th"); b2 = d0.textbbox((0, 0), l2, font=F2, language="th")
w = max(b1[2] - b1[0], b2[2] - b2[0]) + 110; h = (b1[3] - b1[1]) + (b2[3] - b2[1]) + 120
card = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
# paper with a torn bottom edge, soft shadow, tape
import random; random.seed(3)
pts = [(30, 30), (30 + w, 30)] + [(30 + w - k * w / 24, 30 + h + random.uniform(-7, 7)) for k in range(25)]
sh = Image.new("RGBA", card.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 8, y + 12) for x, y in pts], fill=(0, 0, 0, 120)); sh = sh.filter(ImageFilter.GaussianBlur(10))
card = Image.alpha_composite(card, sh); cd = ImageDraw.Draw(card)
cd.polygon(pts, fill=(246, 238, 220, 255), outline=(60, 50, 40, 255))
for yy in range(30 + 46, 30 + h, 46): cd.line([(40, yy), (20 + w, yy)], fill=(160, 190, 220, 90), width=2)   # ruled lines
cd.line([(30 + 70, 30), (30 + 70, 30 + h)], fill=(220, 120, 110, 120), width=3)                               # margin
tx = 30 + 55
cd.text((tx - b1[0], 30 + 30 - b1[1]), l1, font=F, fill=(40, 34, 30, 255), language="th")
y2 = 30 + 30 + (b1[3] - b1[1]) + 22
cd.text((tx - b2[0] + 3, y2 - b2[1] + 4), l2, font=F2, fill=(120, 20, 20, 120), language="th")
cd.text((tx - b2[0], y2 - b2[1]), l2, font=F2, fill=(214, 40, 40, 255), language="th")
# red underline scribble under line 2
uy = y2 + (b2[3] - b2[1]) + 14
cd.line([(tx, uy), (tx + (b2[2] - b2[0]), uy - 6)], fill=(214, 40, 40, 230), width=7)
for (tx0, ang) in ((30 + w * 0.12, -8), (30 + w * 0.82, 7)):
    tape = Image.new("RGBA", (int(150 * big), int(46 * big)), (232, 214, 160, 200)); tape = tape.rotate(ang, expand=True)
    card.alpha_composite(tape, (int(tx0) - int(75 * big), 4))
card = card.rotate(-2.2, resample=Image.BICUBIC, expand=True)
canvas.alpha_composite(card, ((1080 - card.width) // 2 if x0 is None else x0, y0))
canvas.save(out); print(out, card.size)
