"""make_tex.py -- textures for the animatic set: rain streaks, distant city, phone screens, Namnuea avatar."""
import os, random, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(HERE, "tex")
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
os.makedirs(TEX, exist_ok=True)


def font(sz):
    return ImageFont.truetype(FONT, sz, layout_engine=ImageFont.Layout.RAQM)


def rain():
    W, H = 512, 1024
    a = np.zeros((H, W), np.float32)
    rng = np.random.default_rng(3)
    for _ in range(260):
        x = rng.integers(0, W); y = rng.integers(0, H); L = rng.integers(40, 140); op = rng.uniform(0.25, 0.9)
        for k in range(L):
            yy = (y + k) % H
            xx = (x + k // 14) % W
            a[yy, xx] = max(a[yy, xx], op * (k / L))
    a = np.clip(a, 0, 1)
    im = np.zeros((H, W, 4), np.uint8)
    im[..., 0] = 200; im[..., 1] = 215; im[..., 2] = 240
    im[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(im, "RGBA").filter(ImageFilter.GaussianBlur(0.6)).save(os.path.join(TEX, "rain.png"))


def city():
    W, H = 2048, 540
    rng = np.random.default_rng(7)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # sky glow band
    glow = np.zeros((H, W, 4), np.uint8)
    for y in range(H):
        t = y / H
        g = max(0.0, 1 - abs(t - 0.55) / 0.45)
        glow[y, :, 0] = 40; glow[y, :, 1] = 45; glow[y, :, 2] = 80; glow[y, :, 3] = int(120 * g * g)
    im = Image.alpha_composite(im, Image.fromarray(glow, "RGBA"))
    d = ImageDraw.Draw(im)
    x = 0
    while x < W:
        bw = int(rng.integers(18, 70)); bh = int(rng.integers(40, 300))
        top = H - 60 - bh
        d.rectangle([x, top, x + bw, H], fill=(12, 15, 26, 255))
        for wy in range(top + 6, H - 60, 9):
            for wx in range(x + 4, x + bw - 4, 7):
                if rng.random() < 0.28:
                    c = (255, 190, 120) if rng.random() < 0.6 else (190, 210, 255)
                    k = rng.uniform(0.35, 1.0)
                    d.rectangle([wx, wy, wx + 2, wy + 3], fill=(int(c[0] * k), int(c[1] * k), int(c[2] * k), 255))
        if rng.random() < 0.2:
            d.ellipse([x + bw // 2 - 3, top - 6, x + bw // 2 + 3, top], fill=(255, 40, 30, 255))
        x += bw + int(rng.integers(0, 10))
    # street-level glow strip
    for i in range(1500):
        px = int(rng.integers(0, W)); py = int(rng.integers(H - 70, H - 20))
        c = (255, 170, 90) if rng.random() < 0.7 else (255, 255, 255)
        d.point((px, py), fill=c + (255,))
    im.save(os.path.join(TEX, "city.png"))


def avatar(size=220):
    sp = Image.open(os.path.join(HERE, "sprites", "namnuea_smile.png")).convert("RGBA")
    meta = json.load(open(os.path.join(HERE, "sprites", "meta.json")))["namnuea_smile"]
    ppd = meta["ppd"]; x0, y0 = meta["canvas"][0], meta["canvas"][1]
    cx, cy = (0 - x0) * ppd, (0.25 - y0) * ppd
    r = 0.95 * ppd
    crop = sp.crop((int(cx - r), int(cy - r), int(cx + r), int(cy + r))).resize((size, size), Image.LANCZOS)
    bg = Image.new("RGBA", (size, size), (233, 162, 59, 255))
    bg.alpha_composite(crop)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    out.save(os.path.join(TEX, "avatar.png"))
    return out


def screen(state):
    W, H = 540, 1000
    im = Image.new("RGBA", (W, H), (18, 22, 34, 255))
    d = ImageDraw.Draw(im)
    av = Image.open(os.path.join(TEX, "avatar.png"))
    d.text((W // 2, 70), "21:47", font=font(64), fill=(240, 240, 245), anchor="mm")
    if state == "missed":
        im.alpha_composite(av, (W // 2 - 110, 170))
        d.text((W // 2, 450), "น้ำเหนือ", font=font(72), fill=(255, 255, 255), anchor="mm")
        d.rounded_rectangle([60, 540, W - 60, 700], 30, fill=(226, 69, 59))
        d.text((W // 2, 590), "4 สาย", font=font(70), fill=(255, 255, 255), anchor="mm")
        d.text((W // 2, 660), "ที่ไม่ได้รับ", font=font(46), fill=(255, 235, 230), anchor="mm")
        for i in range(3):
            y = 750 + i * 70
            d.rounded_rectangle([60, y, W - 60, y + 56], 16, fill=(36, 42, 58))
            d.text((90, y + 28), "น้ำเหนือ  ·  21:%02d" % (44 - i * 3), font=font(30), fill=(255, 120, 110), anchor="lm")
    elif state == "incoming":
        im.alpha_composite(av, (W // 2 - 110, 200))
        d.text((W // 2, 480), "น้ำเหนือ", font=font(80), fill=(255, 255, 255), anchor="mm")
        d.text((W // 2, 560), "ลูกสาว", font=font(44), fill=(170, 190, 220), anchor="mm")
        d.ellipse([90, 760, 210, 880], fill=(226, 69, 59))
        d.ellipse([W - 210, 760, W - 90, 880], fill=(47, 191, 63))
    elif state == "ended":
        im = Image.new("RGBA", (W, H), (12, 14, 20, 255))
        d = ImageDraw.Draw(im)
        g = av.convert("LA").convert("RGBA")
        im.alpha_composite(g, (W // 2 - 110, 200))
        d.text((W // 2, 480), "น้ำเหนือ", font=font(80), fill=(150, 150, 160), anchor="mm")
        d.text((W // 2, 570), "วางสายแล้ว", font=font(56), fill=(226, 69, 59), anchor="mm")
        d.text((W // 2, 640), "00:41", font=font(44), fill=(120, 125, 140), anchor="mm")
    im = im.convert("RGB").convert("RGBA")
    # rounded corners
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, H - 1], 50, fill=255)
    im.putalpha(mask)
    im.save(os.path.join(TEX, "screen_%s.png" % state))


def vest():
    W, H = 512, 512
    im = Image.new("RGBA", (W, H), (150, 60, 18, 255))
    d = ImageDraw.Draw(im)
    for y in (150, 330):
        d.rectangle([0, y, W, y + 40], fill=(175, 182, 192, 255))
    rng = np.random.default_rng(2)
    for _ in range(200):
        x = int(rng.integers(0, W)); y = int(rng.integers(0, H))
        d.ellipse([x, y, x + 5, y + 7], fill=(200, 120, 70, 255))
    im.save(os.path.join(TEX, "vest.png"))


if __name__ == "__main__":
    rain(); city(); avatar(); vest()
    for s in ("missed", "incoming", "ended"):
        screen(s)
    print(sorted(os.listdir(TEX)))
