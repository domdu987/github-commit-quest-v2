"""v2_b_tex.py : PIL-painted sign textures for the v2 location B (banners, scoreboard, bar-height board, foam mat). Written to work_v2_b/tex/."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FI = '/usr/share/fonts/opentype/inter/Inter-Bold.otf'

def _font(sz, path=FB):
    try: return ImageFont.truetype(path, sz)
    except Exception: return ImageFont.truetype(FB, sz)

def _fit(d, text, w, h, path=FB, pad=0.08):
    sz = int(h * 1.2)
    while sz > 8:
        f = _font(sz, path); b = d.textbbox((0, 0), text, font=f)
        if (b[2] - b[0]) <= w * (1 - 2 * pad) and (b[3] - b[1]) <= h * (1 - 2 * pad): return f, b
        sz -= 4
    return _font(8, path), (0, 0, 8, 8)

def text_center(d, box, text, fill, path=FB, pad=0.08, stroke=0, stroke_fill=None):
    x0, y0, x1, y1 = box; f, b = _fit(d, text, x1 - x0, y1 - y0, path, pad)
    tx = x0 + ((x1 - x0) - (b[2] - b[0])) / 2 - b[0]; ty = y0 + ((y1 - y0) - (b[3] - b[1])) / 2 - b[1]
    d.text((tx, ty), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)

def make_all():
    os.makedirs(TEX, exist_ok=True); out = {}
    # --- MEXICO 68 banner atlas: 4 stripes of 1024 x 256 (red / white / blue / yellow)
    W, H = 1024, 256; im = Image.new('RGB', (W, H * 4)); d = ImageDraw.Draw(im)
    cols = [((224, 32, 40), (255, 255, 255)), ((255, 255, 255), (214, 30, 44)), ((28, 70, 220), (255, 226, 60)), ((255, 205, 30), (30, 52, 190))]
    for i, (bg, fg) in enumerate(cols):
        y0 = i * H; d.rectangle([0, y0, W, y0 + H], fill=bg)
        for k in range(4):                                  # op-art ribbon lines along the top and bottom
            d.rectangle([0, y0 + 6 + k * 7, W, y0 + 9 + k * 7], fill=fg); d.rectangle([0, y0 + H - 12 - k * 7, W, y0 + H - 9 - k * 7], fill=fg)
        text_center(d, (20, y0 + 40, W - 20, y0 + H - 40), 'MEXICO 68', fg, pad=0.03)
    p = os.path.join(TEX, 'banner_mexico68.png'); im.save(p); out['banner'] = p
    # --- scoreboard 1024 x 400
    W, H = 1024, 400; im = Image.new('RGB', (W, H), (8, 12, 46)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(255, 190, 40), width=8)
    text_center(d, (30, 20, W - 30, 250), 'HIGH JUMP', (255, 196, 40), pad=0.02)
    d.rectangle([30, 262, W - 30, 270], fill=(214, 30, 44))
    text_center(d, (40, 285, 520, 385), 'MEN FINAL', (255, 255, 255), pad=0.05)
    text_center(d, (540, 285, W - 40, 385), 'BAR 2.24 m', (255, 120, 60), pad=0.05)
    p = os.path.join(TEX, 'scoreboard.png'); im.save(p); out['scoreboard'] = p
    # --- bar-height board 512 x 256
    W, H = 512, 256; im = Image.new('RGB', (W, H), (10, 10, 18)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(240, 40, 40), width=14); d.rectangle([18, 18, W - 19, 54], fill=(240, 40, 40))
    text_center(d, (24, 18, W - 24, 54), 'BAR HEIGHT', (255, 255, 255), pad=0.1)
    text_center(d, (24, 64, W - 24, H - 20), '2.24 m', (255, 214, 40), pad=0.04)
    p = os.path.join(TEX, 'board_224.png'); im.save(p); out['board'] = p
    # --- 1972 banner 1024 x 512
    W, H = 1024, 512; im = Image.new('RGB', (W, H), (255, 214, 30)); d = ImageDraw.Draw(im)
    for k in range(5): d.rectangle([0, 10 + k * 10, W, 14 + k * 10], fill=(220, 30, 40)); d.rectangle([0, H - 14 - k * 10, W, H - 10 - k * 10], fill=(220, 30, 40))
    text_center(d, (20, 70, W - 20, H - 70), '1972', (24, 50, 200), pad=0.02, stroke=6, stroke_fill=(255, 255, 255))
    p = os.path.join(TEX, 'banner_1972.png'); im.save(p); out['b1972'] = p
    # --- foam mat top (quilted blue/white panels, red border, stitches, grain) 1024 x 880 (6.3 x 5.3 m)
    import random
    rr = random.Random(5); W, H = 1260, 1060; im = Image.new('RGB', (W, H), (36, 76, 220)); d = ImageDraw.Draw(im)
    nx, ny = 4, 3; cw, ch = (W - 80) / nx, (H - 80) / ny
    for gx in range(nx):
        for gy in range(ny):
            x0 = 40 + gx * cw; y0 = 40 + gy * ch; c = (32, 70, 214) if (gx + gy) % 2 == 0 else (22, 52, 170)
            d.rectangle([x0 + 5, y0 + 5, x0 + cw - 5, y0 + ch - 5], fill=c)
            for k in range(1, 8): d.line([x0 + 10, y0 + k * ch / 8, x0 + cw - 10, y0 + k * ch / 8], fill=(c[0] + 14, c[1] + 18, min(255, c[2] + 24)), width=3)   # quilt ribs
            d.rectangle([x0 + 5, y0 + 5, x0 + cw - 5, y0 + ch - 5], outline=(235, 240, 255), width=6)
    d.rectangle([0, 0, W - 1, H - 1], outline=(224, 36, 36), width=44)                                   # red border
    d.rectangle([44, 44, W - 45, H - 45], outline=(255, 255, 255), width=6)
    for k in range(0, W, 28): d.line([k, 14, k + 12, 14], fill=(255, 255, 255), width=4); d.line([k, H - 15, k + 12, H - 15], fill=(255, 255, 255), width=4)   # stitch
    for _ in range(9000):                                                                                 # grain
        x = rr.randrange(W); y = rr.randrange(H); v = rr.randint(-26, 26); px = im.getpixel((x, y)); im.putpixel((x, y), tuple(max(0, min(255, c + v)) for c in px))
    p = os.path.join(TEX, 'foam_top.png'); im.save(p); out['foam'] = p
    # --- foam side skirt 1420 x 200 (7.1 x 1.0 m): quilted blue panels, white seams, red base strip, stitches
    W, H = 1420, 200; im = Image.new('RGB', (W, H), (36, 76, 220)); d = ImageDraw.Draw(im)
    for gx in range(4):
        x0 = 10 + gx * 352; c = (34, 74, 220) if gx % 2 == 0 else (24, 56, 178)
        d.rectangle([x0 + 4, 8, x0 + 344, H - 40], fill=c)
        for k in range(1, 5): d.line([x0 + 8, 8 + k * (H - 48) / 5, x0 + 340, 8 + k * (H - 48) / 5], fill=(c[0] + 18, c[1] + 22, min(255, c[2] + 26)), width=3)
        d.rectangle([x0 + 4, 8, x0 + 344, H - 40], outline=(240, 244, 255), width=5)
    d.rectangle([0, H - 40, W, H], fill=(214, 36, 36)); d.line([0, H - 40, W, H - 40], fill=(255, 255, 255), width=4)
    for k in range(0, W, 26): d.line([k, H - 20, k + 12, H - 20], fill=(255, 255, 255), width=3)
    p = os.path.join(TEX, 'foam_side.png'); im.save(p); out['foam_side'] = p
    # --- podium backdrop 1024 x 320
    W, H = 1024, 320; im = Image.new('RGB', (W, H), (28, 60, 210)); d = ImageDraw.Draw(im)
    for k in range(6): d.rectangle([0, 8 + k * 9, W, 12 + k * 9], fill=(255, 226, 60))
    text_center(d, (20, 60, W - 20, H - 40), 'MEXICO 68', (255, 255, 255), pad=0.04)
    p = os.path.join(TEX, 'podium_back.png'); im.save(p); out['pback'] = p
    return out

if __name__ == '__main__':
    print(make_all())
