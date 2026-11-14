"""Textures for the Part-2 3D look (PIL, drawn): barrel planks + lid, barrel faces, suit front, the insurance paper, coin, sky clouds."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'tex'); FD = os.path.join(os.path.dirname(HERE), 'fonts')
INK = (40, 26, 22)
def KAN(s): return ImageFont.truetype(os.path.join(FD, 'Kanit_900Black.ttf'), s)
def HAND(s): return ImageFont.truetype(os.path.join(FD, 'sriracha.ttf'), s)

def planks(rng, W=512, H=512, n=5):
    im = Image.new('RGB', (W, H), (178, 124, 72)); d = ImageDraw.Draw(im); pw = W / n
    for k in range(n):
        base = (int(176 + rng.uniform(-14, 14)), int(122 + rng.uniform(-10, 10)), int(70 + rng.uniform(-8, 8)))
        d.rectangle((k * pw, 0, (k + 1) * pw, H), fill=base)
        for q in range(26):                                       # grain
            x = k * pw + rng.uniform(6, pw - 6); y0 = rng.uniform(0, H); L = rng.uniform(40, 200)
            d.line((x, y0, x + rng.uniform(-3, 3), y0 + L), fill=tuple(int(c * rng.uniform(0.82, 0.92)) for c in base), width=rng.choice((1, 2, 2, 3)))
        for q in range(2):                                        # knots
            cx, cy = k * pw + rng.uniform(15, pw - 15), rng.uniform(20, H - 20)
            d.ellipse((cx - 7, cy - 11, cx + 7, cy + 11), fill=tuple(int(c * 0.7) for c in base))
        d.line((k * pw, 0, k * pw, H), fill=(92, 58, 32), width=5)
    im = im.filter(ImageFilter.GaussianBlur(0.8)); d = ImageDraw.Draw(im)
    for y in (int(H * 0.16), int(H * 0.84)):                      # nail heads where the bands go
        for k in range(n): d.ellipse((k * pw + pw / 2 - 5, y - 5, k * pw + pw / 2 + 5, y + 5), fill=(70, 70, 76))
    return im

def lid(rng, W=512):
    im = planks(rng, W, W, 6).rotate(90); d = ImageDraw.Draw(im)
    d.ellipse((W / 2 - 30, W / 2 - 30, W / 2 + 30, W / 2 + 30), outline=(92, 58, 32), width=6); return im

def face(expr, W=512, H=512):
    """Transparent decal for the barrel front: two round eyes + a mouth (scared: big open D, determined: flat line, shout: open)."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for ex in (160, 352):
        if expr == 'blink': d.arc((ex - 52, 170, ex + 52, 240), 200, 340, fill=(28, 18, 16, 255), width=18)
        else:
            d.ellipse((ex - 46, 150, ex + 46, 256), fill=(28, 18, 16, 255))
            d.ellipse((ex - 18, 166, ex + 6, 192), fill=(255, 255, 255, 235))
    if expr == 'determined':
        for ex, s in ((160, 1), (352, -1)): d.line((ex - 58, 112 - 20 * s, ex + 58, 112 + 20 * s), fill=(28, 18, 16, 255), width=20)
        d.rounded_rectangle((176, 332, 336, 360), 12, fill=(28, 18, 16, 255))
    elif expr in ('scared', 'shout'):
        d.chord((176, 280, 336, 420), 180, 360, fill=(110, 26, 28, 255)) if False else None
        d.ellipse((150, 280, 362, 450), fill=(28, 18, 16, 255)); d.ellipse((168, 298, 344, 436), fill=(150, 34, 40, 255))
        d.ellipse((206, 370, 306, 432), fill=(226, 92, 100, 255))
        if expr == 'scared':
            for ex, s in ((160, 1), (352, -1)): d.line((ex - 52, 110 + 22 * s, ex + 52, 110 - 22 * s), fill=(28, 18, 16, 255), width=18)
    return im

def suit_front(W=512, H=640):
    im = Image.new('RGB', (W, H), (34, 50, 104)); d = ImageDraw.Draw(im)
    d.polygon([(W * 0.32, 0), (W * 0.68, 0), (W * 0.5, H * 0.55)], fill=(246, 246, 240))             # shirt V
    d.polygon([(W * 0.46, 30), (W * 0.54, 30), (W * 0.57, H * 0.45), (W * 0.5, H * 0.52), (W * 0.43, H * 0.45)], fill=(232, 176, 40))   # tie
    d.polygon([(W * 0.45, 0), (W * 0.55, 0), (W * 0.53, 34), (W * 0.47, 34)], fill=(200, 146, 30))
    for s in (-1, 1):                                                                                  # lapels
        x0 = W * 0.5 + s * W * 0.18; d.polygon([(x0, 0), (W * 0.5 + s * W * 0.02, H * 0.55), (W * 0.5 + s * W * 0.3, H * 0.2)], fill=(26, 38, 82))
    for y in (H * 0.66, H * 0.8): d.ellipse((W * 0.5 - 9, y - 9, W * 0.5 + 9, y + 9), fill=(20, 24, 40))
    d.rectangle((W * 0.64, H * 0.6, W * 0.86, H * 0.64), fill=(22, 32, 70))                            # pocket
    return im

def paper(W=512, H=640):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(4)
    pts = [(14 + r.uniform(-6, 6), 20 + r.uniform(-6, 6)), (W - 14 + r.uniform(-6, 6), 14), (W - 20, H - 18), (18, H - 12)]
    d.polygon(pts, fill=(246, 232, 196, 255))
    for k in range(9): d.line((40, 330 + k * 30, W - 40 - r.uniform(0, 120), 330 + k * 30), fill=(196, 170, 120, 255), width=6)
    d.polygon([(W / 2, 92), (W / 2 + 108, 280), (W / 2 - 108, 280)], fill=(236, 54, 40, 255))
    d.polygon([(W / 2, 128), (W / 2 + 76, 260), (W / 2 - 76, 260)], fill=(255, 196, 40, 255))
    d.rounded_rectangle((W / 2 - 10, 160, W / 2 + 10, 222), 6, fill=(30, 20, 18, 255)); d.ellipse((W / 2 - 12, 232, W / 2 + 12, 254), fill=(30, 20, 18, 255))
    d.text((W / 2, 46), 'ใบประกัน', font=KAN(44), fill=(120, 60, 30, 255), anchor='mm')
    d.text((W / 2, 600), 'สาขา 112', font=HAND(40), fill=(150, 70, 40, 255), anchor='mm')
    im = im.filter(ImageFilter.GaussianBlur(0.5)); return im

def cloud(seed, W=1024, H=384, col=(196, 168, 236)):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); r = random.Random(seed)
    for k in range(9):
        cx = r.uniform(W * 0.2, W * 0.8); cy = r.uniform(H * 0.45, H * 0.6); rx = r.uniform(120, 260); ry = r.uniform(50, 110)
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=col + (255,))
    d.rectangle((0, H * 0.62, W, H), fill=(0, 0, 0, 0))
    return im.filter(ImageFilter.GaussianBlur(6))

def build_all():
    os.makedirs(OUT, exist_ok=True); r = random.Random(112); P = {}
    T = dict(planks=planks(r), lid=lid(r), suit=suit_front(), paper=paper(), cloud_a=cloud(1), cloud_b=cloud(2, col=(252, 232, 206)))
    for e in ('scared', 'determined', 'shout', 'blink'): T['face_' + e] = face(e)
    for k, im in T.items():
        p = os.path.join(OUT, k + '.png')
        if not os.path.exists(p): im.save(p)
        P[k] = p
    return P

if __name__ == '__main__':
    for k in os.listdir(OUT) if os.path.isdir(OUT) else []: os.remove(os.path.join(OUT, k))
    print(len(build_all()))
