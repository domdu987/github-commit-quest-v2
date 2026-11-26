"""faces.py -- face decals and patch textures for the 3D cast (PIL, no bpy).

Face decals are drawn in ANGULAR space so they can be wrapped on a sphere without stretching:
  u = 0.5 + theta / (2 A),  v = 0.5 + phi / (2 A),  A = FACE_A deg
theta = horizontal angle from the face centre (atan2(x, -y), + toward the character's left = +X),
phi   = elevation (asin(z / r)). The bpy side (kong3d.face_material) uses the same mapping.
"""
import os, math, random, hashlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
FACE_A = 63.0          # half range in degrees covered by the decal
N = 2048               # supersampled canvas, saved at 1024
INK = (18, 17, 22, 255)

EXPRS = {"kong": ["determined", "tired", "alarmed", "shouting", "neutral"],
         "driver": ["still", "head_lift", "lunge"]}


def _P(th, ph):
    k = N / (2 * FACE_A)
    return (N / 2 + th * k, N / 2 - ph * k)


def _deg(d):  # degrees -> px on the canvas
    return d * N / (2 * FACE_A)


def _ell(dr, th, ph, w, h, fill=None, outline=None, width=0):
    x, y = _P(th, ph); a, b = _deg(w) / 2, _deg(h) / 2
    dr.ellipse([x - a, y - b, x + a, y + b], fill=fill, outline=outline, width=int(_deg(width)) if width else 0)


def _line(dr, pts, w, col=INK):
    P = [_P(*p) for p in pts]
    dr.line(P, fill=col, width=int(_deg(w)), joint="curve")
    r = _deg(w) / 2
    for x, y in (P[0], P[-1]):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)


def _curve(a, c, b, n=16):
    """quadratic bezier a -> b with control c, in degrees."""
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
                    (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]))
    return out


def _stubble(dr, seed=11, col=(88, 86, 98, 210)):
    rng = random.Random(seed)
    n = 0
    while n < 130:
        th = rng.uniform(-46, 46); ph = rng.uniform(-52, -15)
        # jaw band: denser on the chin and jaw line, keep clear of the mouth
        if abs(th) < 13 and -29 < ph < -15: continue
        edge = (th / 48) ** 2 + ((ph + 12) / 42) ** 2
        if edge > 1.05 or (edge < 0.30 and ph > -27): continue
        _ell(dr, th, ph, 0.85, 0.85, fill=col); n += 1


def _blush(img, th, ph, a=60):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for s in (-1, 1):
        _ell(d, s * th, ph, 10, 5.5, fill=(236, 120, 130, a))
    lay = lay.filter(ImageFilter.GaussianBlur(_deg(1.2)))
    return Image.alpha_composite(img, lay)


def draw_face(who="kong", expr="determined"):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    if who == "kong":
        img = _blush(img, 27, -11, 50)
    elif who == "driver":
        img = _blush(img, 26, -10, 0)
    d = ImageDraw.Draw(img)
    if who == "kong":
        _stubble(d)
        if expr in ("determined", "neutral"):
            for s in (-1, 1):
                _ell(d, s * 15.5, 2.5, 5.6, 9.0, fill=INK)
                _ell(d, s * 15.5 + 1.2, 4.6, 1.5, 1.8, fill=(255, 255, 255, 255))
            if expr == "determined":
                for s in (-1, 1):
                    _line(d, [(s * 27, 15), (s * 17, 12.5), (s * 6.5, 8.0)], 3.4)
                _line(d, _curve((-9, -21.5), (0, -24.5), (9.5, -20.0)), 1.9)
            else:
                for s in (-1, 1):
                    _line(d, [(s * 26, 13), (s * 7, 13)], 3.0)
                _line(d, [(-8, -22), (8, -22)], 1.8)
        elif expr == "tired":
            for s in (-1, 1):
                # half-closed: lower half of the eye under a heavy lid line
                x, y = _P(s * 15.5, 1.0); a, b = _deg(5.6) / 2, _deg(7.5) / 2
                d.chord([x - a, y - b, x + a, y + b], 0, 180, fill=INK)
                _line(d, [(s * 22, 1.6), (s * 9, 1.0)], 1.7)
                _line(d, _curve((s * 20, -5.5), (s * 15.5, -7.8), (s * 11, -5.5), 8), 0.9, (70, 68, 80, 255))
                _line(d, [(s * 26, 10.5), (s * 16, 12.5), (s * 7, 13.8)], 2.8)
            _line(d, _curve((-8, -23.0), (0, -20.8), (8, -23.0)), 1.8)
        elif expr == "alarmed":
            for s in (-1, 1):
                _ell(d, s * 15.5, 3.0, 10.5, 11.0, fill=(255, 255, 255, 255), outline=INK, width=1.5)
                _ell(d, s * 15.5, 3.0, 2.8, 3.0, fill=INK)
                _line(d, _curve((s * 25, 17), (s * 17, 22.5), (s * 8, 18.5)), 2.6)
            _ell(d, 0, -25, 6.0, 7.4, fill=INK)
            _ell(d, 0, -25.6, 3.6, 4.4, fill=(120, 30, 40, 255))
            # sweat drop by the brow
            x, y = _P(33, 14)
            r = _deg(2.6)
            d.polygon([(x, y - 2.2 * r), (x - r, y), (x + r, y)], fill=(150, 205, 240, 255))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 205, 240, 255), outline=None)
            d.arc([x - r, y - r, x + r, y + r], 0, 180, fill=INK, width=int(_deg(0.6)))
        elif expr == "shouting":
            for s in (-1, 1):
                _line(d, [(s * 21, 7.5), (s * 12, 3.0), (s * 21, -1.5)], 2.6)       # squeezed > <
                _line(d, [(s * 28, 18.5), (s * 17, 13.5), (s * 5.5, 7.0)], 3.6)
            mouth = [(-14, -16.5), (14, -16.5)] + [(14 * math.cos(t), -16.5 - 19 * math.sin(t))
                                                     for t in [k / 20 * math.pi for k in range(0, 21)]]
            mouth = [(-14, -16.5), (14, -16.5)] + [(14 * math.cos(k / 20 * math.pi), -16.5 - 19 * math.sin(k / 20 * math.pi))
                                                   for k in range(21)]
            d.polygon([_P(*p) for p in mouth], fill=(80, 18, 26, 255), outline=INK, width=int(_deg(1.6)))
            d.polygon([_P(*p) for p in [(-12.6, -18), (12.6, -18), (11.5, -21.5), (-11.5, -21.5)]], fill=(250, 250, 250, 255))
            _ell(d, 0, -31.5, 13, 6.5, fill=(214, 92, 104, 255))
            d.line([_P(-14, -16.5), _P(14, -16.5)], fill=INK, width=int(_deg(1.6)))
    elif who == "driver":
        UL = (60, 70, 62, 255)
        if expr == "still":
            for s in (-1, 1):
                _line(d, [(s * 22, 2.0), (s * 9.5, 1.0)], 1.9)
                _ell(d, s * 15.5, 0.6, 2.2, 1.6, fill=(170, 20, 25, 255))
                _line(d, _curve((s * 22, -3.5), (s * 15.5, -7.0), (s * 9, -3.5), 8), 1.1, UL)
                _line(d, [(s * 25, 10.5), (s * 8, 9.0)], 2.2)
            _ell(d, 1.5, -24, 7.0, 3.2, fill=(50, 25, 28, 255))
        else:
            for s in (-1, 1):
                _ell(d, s * 15.5, 3.0, 10, 9.5, fill=(250, 248, 236, 255), outline=INK, width=1.3)
                _ell(d, s * 15.5, 3.0, 1.6, 1.6, fill=(200, 16, 22, 255))
                _line(d, _curve((s * 22, -4.5), (s * 15.5, -8.5), (s * 9, -4.5), 8), 1.1, UL)
            if expr == "lunge":
                d.polygon([_P(*p) for p in [(-11, -17), (11, -17), (8, -33), (-8, -33)]], fill=(70, 14, 20, 255), outline=INK,
                          width=int(_deg(1.4)))
                for k in range(-3, 4):
                    _ell(d, k * 3.0, -18.8, 2.4, 3.0, fill=(240, 236, 220, 255))
            else:
                _ell(d, 0, -24, 6.5, 6.0, fill=(60, 20, 24, 255))
    return img.resize((N // 2, N // 2), Image.LANCZOS)


def face_png(who="kong", expr="determined"):
    os.makedirs(TEX, exist_ok=True)
    p = os.path.join(TEX, f"face_{who}_{expr}.png")
    if not os.path.exists(p) or os.path.getmtime(p) < os.path.getmtime(__file__):
        draw_face(who, expr).save(p)
    return p


def rescue_png():
    p = os.path.join(TEX, "patch_rescue.png")
    if os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(__file__): return p
    os.makedirs(TEX, exist_ok=True)
    W, H = 1024, 340
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, W - 5, H - 5], 46, fill=(29, 28, 34, 255), outline=(150, 156, 166, 255), width=10)
    f = ImageFont.truetype(FONT, 190)
    bb = d.textbbox((0, 0), "RESCUE", font=f)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], (H - (bb[3] - bb[1])) / 2 - bb[1]), "RESCUE", font=f, fill=(246, 246, 240, 255))
    im.save(p); return p


def flag_png():
    p = os.path.join(TEX, "patch_flag_th.png")
    if os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(__file__): return p
    os.makedirs(TEX, exist_ok=True)
    W, H = 540, 360
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(165, 25, 49), (244, 245, 248), (45, 42, 74), (45, 42, 74), (244, 245, 248), (165, 25, 49)]
    for i, c in enumerate(cols):
        d.rectangle([0, i * H / 6, W, (i + 1) * H / 6], fill=c + (255,))
    d.rectangle([0, 0, W - 1, H - 1], outline=(25, 25, 30, 255), width=14)
    im.save(p); return p


def gauge_png(bars=3):
    """the cutter's battery gauge face: 3 bars + DZ-9 (emission mask in R, colour in the material)."""
    p = os.path.join(TEX, f"gauge_{bars}.png")
    if os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(__file__): return p
    os.makedirs(TEX, exist_ok=True)
    W, H = 600, 260
    im = Image.new("RGBA", (W, H), (12, 12, 16, 255)); d = ImageDraw.Draw(im)
    on = {3: (31, 214, 85), 2: (255, 210, 63), 1: (255, 42, 26)}.get(bars, (31, 214, 85))
    for i in range(3):
        c = on if i < bars else (52, 52, 60)
        d.rounded_rectangle([40 + i * 180, 34, 40 + i * 180 + 160, 150], 16, fill=c + (255,))
    f = ImageFont.truetype(FONT, 70)
    d.text((W / 2, 205), "DZ-9", font=f, fill=(150, 156, 166, 255), anchor="mm")
    im.save(p); return p


if __name__ == "__main__":
    tiles = []
    for who, ex in EXPRS.items():
        for e in ex:
            im = Image.open(face_png(who, e))
            bg = Image.new("RGBA", im.size, (251, 250, 245, 255) if who == "kong" else (184, 195, 168, 255))
            tiles.append(Image.alpha_composite(bg, im).resize((384, 384)))
    sheet = Image.new("RGB", (384 * len(tiles), 384))
    for i, t in enumerate(tiles): sheet.paste(t.convert("RGB"), (384 * i, 0))
    sheet.save(os.path.join(TEX, "faces_sheet.png"))
    rescue_png(); flag_png(); gauge_png(3)
    print("ok")
