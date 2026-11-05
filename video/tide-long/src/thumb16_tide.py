"""YouTube thumbnail 1280×720 for the full 16:9 film, in the EP.1 cover's style (ROD MAI CLUB, the glowing title, a red tag,
the red "อย่ายกมือถือขึ้นถ่าย!" banner) over a clean plate (no captions).
usage: python3 thumb16.py <plate.png> <fonts dir> <out.jpg>"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

plate, fonts, out = sys.argv[1:4]
W, H = 1280, 720
K = lambda n, s: ImageFont.truetype(f"{fonts}/{n}", s)
BLACK, BOLD = "f3.ttf", "f2.ttf"

bg = Image.open(plate).convert("RGB")
import os
sc = float(os.environ.get("SC", "1.15"))     # push in (env SC/OX/OY pick the window on the plate)
bg = bg.resize((int(1280 * sc), int(720 * sc)), Image.LANCZOS)
im = Image.new("RGB", (W, H)); im.paste(bg, (int(os.environ.get("OX", "0")), int(os.environ.get("OY", "-60"))))

# darken the top-left (title) and the bottom (banner) for legibility: alpha = max(top, bottom, left) ramps
import numpy as np
yy, xx = np.mgrid[0:H, 0:W]
a = np.maximum.reduce([np.clip(170 - yy * 0.8, 0, 255), np.clip((yy - 470) * 0.8, 0, 255), np.clip(130 - xx * 0.25, 0, 255) * (yy < 330)])
mask = Image.fromarray(np.clip(a, 0, 200).astype("uint8"), "L")
im = Image.composite(Image.new("RGB", (W, H), (8, 6, 10)), im, mask)
# the burned-in caption and corner badge sit in the bottom band: blur it away before the banner goes on
band = im.crop((0, 548, W, H)).filter(ImageFilter.GaussianBlur(18)); im.paste(band, (0, 548))

def glow_text(base, xy, text, font, fill, glow, stroke=(40, 18, 6), sw=6, gr=16):
    g = Image.new("RGBA", base.size, (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    dg.text(xy, text, font=font, fill=glow + (255,), stroke_width=sw + 6, stroke_fill=glow + (255,))
    g = g.filter(ImageFilter.GaussianBlur(gr))
    base = Image.alpha_composite(base, g)
    t = Image.new("RGBA", base.size, (0, 0, 0, 0)); dt = ImageDraw.Draw(t)
    dt.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)
    return Image.alpha_composite(base, t)

im = im.convert("RGBA")
d = ImageDraw.Draw(im)
d.text((44, 26), "R O D   M A I   C L U B", font=K(BOLD, 24), fill=(244, 236, 216))
im = glow_text(im, (34, 44), "ทะเลลด", K(BLACK, 132), (236, 250, 255), (40, 170, 255))
d = ImageDraw.Draw(im)
# the red tag: เรื่องเต็ม
tag = "ฉบับเต็ม"; ft = K(BOLD, 40); tb = d.textbbox((0, 0), tag, font=ft)
x0, y0 = 46, 236; d.rounded_rectangle((x0, y0, x0 + tb[2] - tb[0] + 36, y0 + 58), 14, fill=(216, 49, 42), outline=(255, 246, 230), width=4)
d.text((x0 + 18 - tb[0], y0 + 6 - tb[1] + 4), tag, font=ft, fill=(255, 255, 255))
# the banner
ban = "ทะเลลด… อย่าลงไปเก็บ!"; fb = K(BLACK, 66); bb = d.textbbox((0, 0), ban, font=fb)
bw, bh = bb[2] - bb[0] + 64, 104; bx, by = 36, H - bh - 34
sh2 = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh2).rounded_rectangle((bx + 8, by + 10, bx + bw + 8, by + bh + 10), 22, fill=(0, 0, 0, 150))
im = Image.alpha_composite(im, sh2.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
d.rounded_rectangle((bx, by, bx + bw, by + bh), 22, fill=(216, 49, 42), outline=(255, 246, 230), width=5)
d.text((bx + 32 - bb[0], by + (bh - (bb[3] - bb[1])) / 2 - bb[1]), ban, font=fb, fill=(255, 255, 255), stroke_width=3, stroke_fill=(120, 16, 12))
im.convert("RGB").save(out, quality=92)
print(out, im.size)
