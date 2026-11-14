"""signs.py -- Thai text cards for take s13 (PIL + raqm shaping, font film/fonts/Kanit_900Black.ttf).  Pure PIL, no bpy."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "..", "..", "fonts", "Kanit_900Black.ttf")
INK = (42, 26, 46, 255)          # plum ink like the cast


def _font(px):
    return ImageFont.truetype(FONT, px, layout_engine=ImageFont.Layout.RAQM)


def _text_box(d, txt, f, sw):
    return d.textbbox((0, 0), txt, font=f, stroke_width=sw, language="th")


def plank(txt, out, px=120, fill=(255, 238, 196, 255), wood=(150, 100, 56, 255), pad=(70, 40)):
    """a wooden notice board with bold Thai text (cream letters, ink outline), two rope eyes on top."""
    f = _font(px)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = _text_box(tmp, txt, f, 8)
    w, h = x1 - x0 + 2 * pad[0], y1 - y0 + 2 * pad[1]
    im = Image.new("RGBA", (w + 24, h + 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((12, 12, 12 + w, 12 + h), radius=28, fill=wood, outline=INK, width=12)
    for k in range(3):                                   # planks
        yy = 12 + h * (k + 1) / 3.0
        if k < 2:
            d.line((24, yy, w, yy), fill=(110, 70, 36, 255), width=6)
    for sx in (0.12, 0.88):                              # nails
        d.ellipse((12 + w * sx - 12, 30, 12 + w * sx + 12, 54), fill=(80, 76, 90, 255), outline=INK, width=4)
    d.text((12 + pad[0] - x0, 12 + pad[1] - y0), txt, font=f, fill=fill, stroke_width=8, stroke_fill=INK, language="th")
    im.save(out)
    return im.size


def pop(txt, out, px=150, fill=(255, 214, 64, 255)):
    """a bold comic word (yellow, thick ink outline + a white outer rim) for the count pops."""
    f = _font(px)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = _text_box(tmp, txt, f, 22)
    im = Image.new("RGBA", (x1 - x0 + 40, y1 - y0 + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((20 - x0, 20 - y0), txt, font=f, fill=(255, 255, 255, 255), stroke_width=22, stroke_fill=(255, 255, 255, 255), language="th")
    d.text((20 - x0, 20 - y0), txt, font=f, fill=fill, stroke_width=11, stroke_fill=INK, language="th")
    im.save(out)
    return im.size


def bubble(txt, out, px=110, tail="left"):
    """a white speech bubble with ink outline and a tail (bottom-left or bottom-right), black Thai text."""
    f = _font(px)
    tmp = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = _text_box(tmp, txt, f, 0)
    w, h = x1 - x0 + 120, y1 - y0 + 80
    im = Image.new("RGBA", (w + 40, h + 110), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    tx = 20 + (w * 0.25 if tail == "left" else w * 0.75)
    tip = (tx - 60, h + 100) if tail == "left" else (tx + 60, h + 100)
    d.polygon([(tx - 30, 20 + h - 20), (tx + 30, 20 + h - 20), tip], fill=INK)
    d.ellipse((20, 20, 20 + w, 20 + h), fill=INK)
    d.ellipse((30, 30, 10 + w, 10 + h), fill=(255, 255, 255, 255))
    d.polygon([(tx - 18, 20 + h - 26), (tx + 18, 20 + h - 26), (tip[0] + (9 if tail == "left" else -9), tip[1] - 16)], fill=(255, 255, 255, 255))
    d.text((20 + 60 - x0, 20 + 40 - y0), txt, font=f, fill=INK, language="th")
    im.save(out)
    return im.size


if __name__ == "__main__":
    o = os.path.join(HERE, "work", "signs"); os.makedirs(o, exist_ok=True)
    print(plank("ห้ามขายขาดน้ำหนัก!", os.path.join(o, "plank.png")))
    for i, t in enumerate(("หนึ่ง!", "สอง!", "สาม!")):
        print(pop(t, os.path.join(o, "pop%d.png" % i)))
    print(bubble("ชั่งเป๊ะ!", os.path.join(o, "bubble.png")))
