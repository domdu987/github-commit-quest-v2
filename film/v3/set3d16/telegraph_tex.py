"""telegraph_tex.py : painted textures of set3d16 (numpy + PIL, cached in tex_telegraph/): the unfinished general portrait on the easel, the small
oval portrait of the wife (bonnet, smiling), the Morse register tape (dots and dashes only, no letters). No text anywhere."""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'tex_telegraph'); TEX_V = 1
os.makedirs(OUT, exist_ok=True)

def _paint(img, rr, amt=14):
    a = np.asarray(img, dtype=np.float32); h, w = a.shape[:2]
    n = np.asarray(Image.fromarray((np.random.RandomState(rr).rand(h // 6 + 1, w // 6 + 1) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0
    a = a + (n[..., None] - 0.5) * amt * 2
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def _brush(d, pts, col, w):
    d.line(pts, fill=col, width=w, joint='curve')

def general(path):
    W_, H_ = 512, 680; img = Image.new('RGB', (W_, H_), (226, 210, 176)); d = ImageDraw.Draw(img); rr = random.Random(5)
    # dark olive background wash, left-lower corner left raw (unfinished)
    for i in range(160):
        x = rr.randint(0, W_); y = rr.randint(0, H_); r = rr.randint(40, 120)
        if x < 150 and y > 470: continue
        c = rr.choice([(74, 66, 40), (94, 80, 48), (60, 56, 38), (110, 92, 56)]); d.ellipse([x - r, y - r // 2, x + r, y + r // 2], fill=c)
    d.rectangle([0, 520, 200, H_], fill=(226, 210, 176))
    # coat: Prussian blue, gold epaulettes, white cross-belts, red sash
    d.polygon([(70, 680), (110, 430), (200, 380), (310, 380), (400, 430), (450, 680)], fill=(34, 52, 108))
    d.polygon([(200, 380), (310, 380), (290, 450), (255, 600), (220, 450)], fill=(238, 232, 216))
    for sg in (-1, 1): d.polygon([(255, 600), (255 + sg * 120, 440), (255 + sg * 150, 450), (255 + sg * 40, 640)], fill=(226, 220, 204))
    d.rectangle([110, 600, 400, 640], fill=(170, 40, 44))
    for cx in (105, 405):
        d.ellipse([cx - 44, 410, cx + 44, 450], fill=(214, 168, 56)); d.ellipse([cx - 30, 416, cx + 30, 444], fill=(240, 204, 96))
        for k in range(6): d.line([cx - 38 + k * 14, 450, cx - 38 + k * 14, 480], fill=(214, 168, 56), width=5)
    for k in range(5): d.ellipse([245 - 8, 440 + k * 36, 245 + 8, 456 + k * 36], fill=(224, 182, 70))
    # neck + head: only a flat ochre block-in with a few sketch lines (unfinished, generic)
    d.rectangle([225, 330, 285, 395], fill=(196, 150, 112)); d.ellipse([170, 130, 340, 360], fill=(214, 168, 124))
    d.pieslice([160, 100, 350, 260], 180, 360, fill=(142, 134, 126))               # grey hair
    d.rectangle([160, 190, 175, 280], fill=(142, 134, 126)); d.rectangle([335, 190, 350, 280], fill=(142, 134, 126))
    for (x0, y0, x1, y1) in [(200, 215, 236, 226), (276, 215, 312, 226)]: d.line([x0, y0, x1, y1], fill=(90, 62, 48), width=3)      # sketched brows
    d.ellipse([212, 235, 226, 245], fill=(70, 50, 44)); d.ellipse([286, 235, 300, 245], fill=(70, 50, 44))
    d.line([(255, 245), (250, 285), (262, 290)], fill=(120, 84, 62), width=3); d.arc([225, 300, 285, 330], 20, 160, fill=(130, 70, 62), width=3)
    # charcoal construction lines over the raw canvas
    d.line([(0, 560), (180, 470), (210, 380)], fill=(60, 56, 52), width=2); d.rectangle([20, 20, W_ - 20, H_ - 20], outline=(150, 130, 100), width=1)
    img = img.filter(ImageFilter.GaussianBlur(1.6)); img = _paint(img, 3, 12)
    # visible brush strokes
    d2 = ImageDraw.Draw(img)
    for i in range(260):
        x = rr.randint(0, W_); y = rr.randint(0, H_); px = img.getpixel((min(x, W_ - 1), min(y, H_ - 1)))
        c = tuple(max(0, min(255, v + rr.randint(-18, 18))) for v in px); d2.line([(x, y), (x + rr.randint(-30, 30), y + rr.randint(-12, 12))], fill=c, width=rr.randint(3, 8))
    img.save(path)

def woman(path):
    W_, H_ = 420, 540; img = Image.new('RGB', (W_, H_), (136, 94, 62)); d = ImageDraw.Draw(img)
    for i in range(80):
        x = rr = random.Random(i).randint(0, W_); y = random.Random(i + 99).randint(0, H_); d.ellipse([x - 70, y - 40, x + 70, y + 40], fill=random.Random(i).choice([(150, 106, 70), (118, 80, 54), (160, 118, 80)]))
    d.polygon([(40, 540), (90, 400), (330, 400), (380, 540)], fill=(76, 90, 128))                  # dress
    d.polygon([(150, 400), (270, 400), (250, 450), (210, 480), (170, 450)], fill=(240, 232, 214))    # collar
    d.ellipse([150, 190, 270, 350], fill=(238, 196, 160))                                              # face
    d.rectangle([188, 340, 232, 410], fill=(232, 188, 152))
    d.ellipse([118, 130, 302, 330], outline=None, fill=None)
    d.pieslice([128, 120, 292, 330], 180, 360, fill=(246, 238, 222))                                   # bonnet crown
    d.polygon([(128, 225), (150, 215), (150, 300), (118, 330)], fill=(240, 230, 212)); d.polygon([(292, 225), (270, 215), (270, 300), (302, 330)], fill=(240, 230, 212))
    d.arc([138, 112, 282, 232], 190, 350, fill=(210, 196, 176), width=4)
    d.polygon([(190, 345), (150, 420), (170, 430), (210, 360)], fill=(176, 70, 84)); d.polygon([(230, 345), (270, 420), (250, 430), (210, 360)], fill=(176, 70, 84))   # ribbon
    d.ellipse([186, 345, 234, 372], fill=(196, 84, 98))
    d.arc([182, 296, 238, 326], 15, 165, fill=(168, 76, 70), width=4)                                  # smile
    for sg in (-1, 1): d.ellipse([210 + sg * 28 - 7, 258, 210 + sg * 28 + 7, 270], fill=(58, 44, 40)); d.arc([210 + sg * 28 - 14, 238, 210 + sg * 28 + 14, 254], 190, 350, fill=(90, 62, 48), width=3)
    for sg in (-1, 1): d.ellipse([210 + sg * 44 - 12, 284, 210 + sg * 44 + 12, 304], fill=(236, 150, 130))
    d.polygon([(158, 235), (150, 280), (168, 260)], fill=(80, 56, 44)); d.polygon([(262, 235), (270, 280), (252, 260)], fill=(80, 56, 44))   # hair
    img = img.filter(ImageFilter.GaussianBlur(1.3)); img = _paint(img, 8, 10); img.save(path)

def tape(path):
    W_, H_ = 4096, 64; img = Image.new('RGB', (W_, H_), (244, 234, 208)); d = ImageDraw.Draw(img); rr = random.Random(11)
    x = 30; code = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]
    while x < W_ - 120:
        for _ in range(rr.randint(1, 4)):
            ln = 20 if rr.random() < 0.5 else 62
            d.rounded_rectangle([x, 22, x + ln, 42], radius=9, fill=(30, 26, 40)); x += ln + 20
        x += 56
    # side perforation-free edges: faint edge lines
    d.line([(0, 3), (W_, 3)], fill=(214, 200, 172), width=2); d.line([(0, H_ - 4), (W_, H_ - 4)], fill=(214, 200, 172), width=2)
    img = _paint(img, 4, 6); img.save(path)

def ensure():
    P = dict(general=os.path.join(OUT, 'general_v%d.png' % TEX_V), woman=os.path.join(OUT, 'woman_v%d.png' % TEX_V), tape=os.path.join(OUT, 'tape_v%d.png' % TEX_V))
    for k, f in (('general', general), ('woman', woman), ('tape', tape)):
        if not os.path.exists(P[k]): f(P[k])
    return P
if __name__ == '__main__': print(ensure())

def mule(path):
    """simple side-view mule card (placeholder, facing right): body, long ears, harness, collar, 4 legs, tail; transparent background"""
    W_, H_ = 700, 460; img = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(img); bc = (122, 88, 62, 255); dk = (84, 58, 40, 255)
    d.ellipse([120, 120, 520, 320], fill=bc); d.ellipse([150, 230, 500, 330], fill=(168, 128, 96, 255))
    for x in (170, 220, 430, 480): d.polygon([(x, 290), (x + 36, 290), (x + 30, 440), (x + 4, 440)], fill=dk if x in (220, 480) else bc); d.rectangle([x + 2, 430, x + 32, 450], fill=(40, 30, 28, 255))
    d.polygon([(480, 150), (600, 90), (660, 130), (680, 200), (640, 250), (560, 250), (500, 230)], fill=bc)       # neck + head
    d.polygon([(560, 250), (640, 250), (630, 290), (570, 280)], fill=(206, 176, 146, 255))                       # muzzle
    d.polygon([(560, 100), (590, 20), (606, 40), (596, 104)], fill=dk); d.polygon([(596, 96), (640, 28), (656, 52), (620, 110)], fill=bc)   # ears
    d.ellipse([612, 150, 632, 170], fill=(24, 20, 20, 255))
    d.polygon([(130, 150), (60, 220), (80, 330), (120, 230)], fill=dk)                                          # tail
    d.arc([440, 120, 560, 300], 280, 80, fill=(150, 40, 40, 255), width=22)                                      # collar
    d.line([(520, 200), (380, 160), (200, 190)], fill=(30, 26, 26, 255), width=8); d.line([(380, 160), (380, 300)], fill=(30, 26, 26, 255), width=8)   # harness
    d.ellipse([368, 150, 392, 174], fill=(214, 176, 60, 255))
    img.save(path)
