"""YouTube thumbnail 1280×720 for มือพราย ฉบับเต็ม, in the ทะเลลด long's style (ROD MAI CLUB, the glowing title, a red tag
"ฉบับเต็ม", a red banner) over a clean plate of the EP.1 hook (no captions or badge; the พราย's hand at full opacity).
usage: SC=1.2 OX=-40 OY=-120 python3 thumb16_phrai.py <plate.png> <fonts dir> <out.jpg>"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

plate, fonts, out = sys.argv[1:4]
W, H = 1280, 720
K = lambda n, s: ImageFont.truetype(f"{fonts}/{n}", s)
BLACK, BOLD = "f3.ttf", "f2.ttf"
sc = float(os.environ.get("SC", "1.2"))
bg = Image.open(plate).convert("RGB").resize((int(1280 * sc), int(720 * sc)), Image.LANCZOS)
im = Image.new("RGB", (W, H)); im.paste(bg, (int(os.environ.get("OX", "-40")), int(os.environ.get("OY", "-120"))))
# darken the top-left (title) and the bottom-left (banner) only: the krathong and the hand on the right stay as lit
yy, xx = np.mgrid[0:H, 0:W]
fx = lambda x0, x1: np.clip((x1 - xx) / (x1 - x0), 0, 1)   # 1 left of x0, 0 right of x1 (soft)
fy = lambda y0, y1: np.clip((y1 - yy) / (y1 - y0), 0, 1)
a = np.maximum.reduce([np.clip(150 - yy * 0.7, 0, 255) * fx(640, 980), np.clip((yy - 500) * 0.9, 0, 255) * fx(640, 900),
                       np.clip(120 - xx * 0.22, 0, 255) * fy(260, 420)])
mask = Image.fromarray(np.clip(a, 0, 190).astype("uint8"), "L")
im = Image.composite(Image.new("RGB", (W, H), (6, 8, 14)), im, mask)


def glow_text(base, xy, text, font, fill, glow, stroke=(10, 30, 32), sw=6, gr=16):
    g = Image.new("RGBA", base.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    dg.text(xy, text, font=font, fill=glow + (255,), stroke_width=sw + 6, stroke_fill=glow + (255,))
    base = Image.alpha_composite(base, g.filter(ImageFilter.GaussianBlur(gr)))
    t = Image.new("RGBA", base.size, (0, 0, 0, 0)); ImageDraw.Draw(t).text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return Image.alpha_composite(base, t)


im = im.convert("RGBA")
d = ImageDraw.Draw(im)
d.text((44, 26), "R O D   M A I   C L U B", font=K(BOLD, 24), fill=(244, 236, 216))
im = glow_text(im, (34, 40), "มือพราย", K(BLACK, 132), (246, 238, 220), (50, 200, 180))
d = ImageDraw.Draw(im)
tag = "ฉบับเต็ม"; ft = K(BOLD, 40); tb = d.textbbox((0, 0), tag, font=ft)
x0, y0 = 46, 236; d.rounded_rectangle((x0, y0, x0 + tb[2] - tb[0] + 36, y0 + 58), 14, fill=(216, 49, 42), outline=(255, 246, 230), width=4)
d.text((x0 + 18 - tb[0], y0 + 6 - tb[1] + 4), tag, font=ft, fill=(255, 255, 255))
ban = os.environ.get("BANNER", "อย่าก้มลงไปเก็บ!"); fb = K(BLACK, 66); bb = d.textbbox((0, 0), ban, font=fb)
bw, bh = bb[2] - bb[0] + 64, 104; bx, by = 36, H - bh - 34
sh2 = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh2).rounded_rectangle((bx + 8, by + 10, bx + bw + 8, by + bh + 10), 22, fill=(0, 0, 0, 150))
im = Image.alpha_composite(im, sh2.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
d.rounded_rectangle((bx, by, bx + bw, by + bh), 22, fill=(216, 49, 42), outline=(255, 246, 230), width=5)
d.text((bx + 32 - bb[0], by + (bh - (bb[3] - bb[1])) / 2 - bb[1]), ban, font=fb, fill=(255, 255, 255), stroke_width=3, stroke_fill=(120, 16, 12))
im.convert("RGB").save(out, quality=92)
print(out, im.size, "banner", bx, by, bx + bw, by + bh)
