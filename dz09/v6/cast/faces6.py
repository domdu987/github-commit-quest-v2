"""faces6.py -- PIL textures for the v6 cast (no bpy): face decals, jacket/shirt atlases, gauge, hair strokes.

Face decals live in ANGULAR sphere space (same mapping as v5/kong3d/faces.py, which this adapts):
    u = 0.5 + theta / (2 A),  v = 0.5 + phi / (2 A),  A = FACE_A deg
theta = azimuth from the face centre, + toward the character's LEFT (+X); phi = elevation.
On the D = 1 sphere 1 D of arc = 114.6 deg, so the ref D sizes convert as:
    eye 0.08 x 0.05 D = 9.2 x 5.7 deg, brow 0.17 x 0.035 D = 19.5 x 4.0 deg, mouth arc 0.12 D = 13.8 deg,
    shout mouth 0.16 x 0.11 D = 18.3 x 12.6 deg, stubble dot 0.01 D = 1.15 deg.

Body atlases are CYLINDRICAL: u = 0.5 + azimuth/360 (front = 0.5, + toward +X), v = (z - z0) / (z1 - z0).
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
FACE_A = 63.0
N = 2048
INK = (22, 15, 19, 255)          # ref outline colour #160f12
RED_IN = (142, 36, 48, 255)      # #8E2430
TONGUE = (233, 134, 143, 255)    # #E9868F
WHITE = (252, 251, 247, 255)

EXPRS = {
    "kong": ["determined", "neutral", "tired", "guilty", "alarmed", "shouting", "blink"],
    "crew": ["neutral", "shouting", "scared", "blink"],
    "driver": ["still", "head_lift", "lunge"],
}
SWEAT = {("kong", "alarmed"), ("kong", "guilty"), ("crew", "scared")}


def _P(th, ph):
    k = N / (2 * FACE_A)
    return (N / 2 + th * k, N / 2 - ph * k)


def _deg(d):
    return d * N / (2 * FACE_A)


def _ell(dr, th, ph, w, h, fill=None, outline=None, width=0):
    x, y = _P(th, ph); a, b = _deg(w) / 2, _deg(h) / 2
    dr.ellipse([x - a, y - b, x + a, y + b], fill=fill, outline=outline, width=int(_deg(width)) if width else 0)


def _line(dr, pts, w, col=INK):
    P = [_P(*p) for p in pts]
    dr.line(P, fill=col, width=max(1, int(_deg(w))), joint="curve")
    r = _deg(w) / 2
    for x, y in (P[0], P[-1]):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)


def _curve(a, c, b, n=18):
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
                    (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]))
    return out


def _bar(dr, s, inner, outer, w=4.0):
    """brow bar from the inner end to the outer end (degrees), rounded ends, 0.035 D thick."""
    _line(dr, [(s * inner[0], inner[1]), (s * outer[0], outer[1])], w)


def _lidded(dr, s, th=17.0, ph=2.0, w=9.2, h=5.7, lid_drop=0.0, look_dy=0.0):
    """ref D heavy-lidded eye: a straight lid line on top, a black half oval below it."""
    x, y = _P(s * th, ph - lid_drop)
    a, b = _deg(w) / 2, _deg(h)
    dr.chord([x - a, y - b + _deg(look_dy), x + a, y + b + _deg(look_dy)], 0, 180, fill=INK)
    _line(dr, [(s * th - w * 0.62, ph - lid_drop + 0.4), (s * th + w * 0.62, ph - lid_drop + 0.4)], 1.5)


def _ring_eye(dr, s, th=17.0, ph=3.0, d=10.5, pupil=3.0, pcol=INK, fill=WHITE):
    _ell(dr, s * th, ph, d, d * 1.05, fill=fill, outline=INK, width=1.4)
    _ell(dr, s * th, ph, pupil, pupil, fill=pcol)


def _stubble(dr, seed=11, n_want=25, col=(128, 126, 132, 255)):
    rng = random.Random(seed); n = 0; tries = 0
    while n < n_want and tries < 5000:
        tries += 1
        th = rng.uniform(-34, 34); ph = rng.uniform(-40, -24)
        if abs(th) < 11 and ph > -31: continue
        if (th / 36) ** 2 + ((ph + 22) / 20) ** 2 > 1.0: continue
        _ell(dr, th, ph, 1.15, 1.15, fill=col); n += 1


def _blush(img, th, ph, a=55, col=(236, 128, 140)):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for s in (-1, 1):
        _ell(d, s * th, ph, 9, 5, fill=col + (a,))
    lay = lay.filter(ImageFilter.GaussianBlur(_deg(1.0)))
    return Image.alpha_composite(img, lay)


def _wavy(dr, cx, cy, w, amp, n=3, lw=2.0):
    pts = [(cx - w / 2 + w * i / 40, cy + amp * math.sin(i / 40 * n * 2 * math.pi)) for i in range(41)]
    _line(dr, pts, lw)


def _open_D(dr, cx, top, w, h, tongue=True, teeth=False):
    """open D mouth: straight top, round bottom, dark-red inside, pink tongue."""
    pts = [(cx - w / 2, top), (cx + w / 2, top)] + [
        (cx + w / 2 * math.cos(k / 24 * math.pi), top - h * math.sin(k / 24 * math.pi)) for k in range(25)]
    img_pts = [_P(*p) for p in pts]
    dr.polygon(img_pts, fill=RED_IN)
    if tongue:
        _ell(dr, cx, top - h * 0.78, w * 0.55, h * 0.42, fill=TONGUE)
    if teeth:
        for k in range(-3, 4):
            x = cx + k * w / 8.2
            dr.polygon([_P(x - w / 18, top - 0.3), _P(x + w / 18, top - 0.3), _P(x, top - h * 0.28)], fill=WHITE)
            dr.polygon([_P(x - w / 18 + w / 16, top - h * 0.97), _P(x + w / 18 + w / 16, top - h * 0.97),
                        _P(x + w / 16, top - h * 0.70)], fill=WHITE)
    dr.line(img_pts + [img_pts[0]], fill=INK, width=int(_deg(1.9)), joint="curve")


def draw_face(who="kong", expr="determined"):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    if who in ("kong", "crew") and expr not in ("blink",):
        img = _blush(img, 27, -10, 38 if who == "kong" else 50)
    d = ImageDraw.Draw(img)
    if who == "kong":
        _stubble(d)
    if who in ("kong", "crew"):
        if expr in ("determined", "neutral"):
            for s in (-1, 1):
                _lidded(d, s)
                if expr == "determined" and who == "kong":
                    _bar(d, s, (7.5, 9.5), (27, 15.5))
                else:
                    _bar(d, s, (8, 13.5), (27, 14.0))
            if expr == "determined" and who == "kong":
                _line(d, _curve((-7, -20.5), (0, -23.5), (7.5, -20.0)), 2.3)
            else:
                _line(d, _curve((-6.5, -21), (0, -23.5), (6.5, -21)), 2.3)
        elif expr == "blink":
            for s in (-1, 1):
                _line(d, _curve((s * 22, 1.0), (s * 17, -1.6), (s * 12, 1.0), 8), 1.8)
                _bar(d, s, (8, 13), (27, 13.5))
            _line(d, [(-6, -21.5), (6, -21.5)], 2.2)
        elif expr == "tired":
            for s in (-1, 1):
                _lidded(d, s, h=4.0, lid_drop=1.6)
                _line(d, _curve((s * 21.5, -5.2), (s * 17, -7.3), (s * 12.5, -5.2), 8), 1.0, (96, 92, 110, 255))
                _bar(d, s, (8, 12.5), (26.5, 9.5), 3.6)
            _line(d, _curve((-6.5, -22.5), (0, -21.2), (6.5, -22.8)), 2.2)
        elif expr == "guilty":
            for s in (-1, 1):
                _lidded(d, s, h=4.6, lid_drop=0.8, look_dy=-1.2)
                _bar(d, s, (7.5, 15.5), (26.5, 11.0), 3.8)
            _wavy(d, 0, -22.5, 11, 0.9, 2, 2.0)
        elif expr in ("alarmed", "scared"):
            for s in (-1, 1):
                _ring_eye(d, s)
                _bar(d, s, (8, 16.5), (26, 19.5), 3.6) if expr == "alarmed" else _bar(d, s, (7.5, 18), (26, 14.5), 3.6)
            if expr == "alarmed":
                _ell(d, 0, -24, 5.0, 6.2, fill=RED_IN, outline=INK, width=1.6)
            else:
                _wavy(d, 0, -22.5, 12, 1.1, 3, 2.0)
        elif expr == "shouting":
            for s in (-1, 1):
                _lidded(d, s, h=5.2, lid_drop=0.4)
                _bar(d, s, (7.0, 7.5), (27, 15.5), 4.2)
            _open_D(d, 0, -15.5, 18.3, 12.6)
    elif who == "driver":
        UL = (70, 84, 70, 255)
        if expr == "still":
            for s in (-1, 1):
                _line(d, [(s * 22, 1.5), (s * 11, 0.6)], 1.8)
                _ell(d, s * 16, -0.2, 2.0, 1.4, fill=(170, 20, 25, 255))
                _line(d, _curve((s * 22, -4.0), (s * 16.5, -7.0), (s * 11, -4.0), 8), 1.2, UL)
                _bar(d, s, (8, 10.5), (25, 9.0), 3.0)
            _ell(d, 1.5, -24, 6.0, 3.0, fill=(60, 26, 30, 255), outline=INK, width=0.9)
        else:
            for s in (-1, 1):
                _ring_eye(d, s, d=10.0 if expr == "head_lift" else 12.0, pupil=1.8, pcol=(200, 16, 22, 255),
                          fill=(246, 244, 230, 255))
                _line(d, _curve((s * 23, -4.8), (s * 17, -9.0), (s * 11, -4.8), 8), 1.2, UL)
            if expr == "lunge":
                for s in (-1, 1): _bar(d, s, (7, 9), (26, 15.5), 3.8)
                _open_D(d, 0, -15.0, 20, 15, tongue=False, teeth=True)
            else:
                for s in (-1, 1): _bar(d, s, (8, 13.5), (25, 13.0), 3.0)
                _ell(d, 0, -24, 6.0, 6.5, fill=(70, 20, 26, 255), outline=INK, width=1.2)
    return img.resize((N // 2, N // 2), Image.LANCZOS)


def _fresh(p):
    return os.path.exists(p) and os.path.getmtime(p) > os.path.getmtime(__file__)


def face_png(who="kong", expr="determined"):
    os.makedirs(TEX, exist_ok=True)
    p = os.path.join(TEX, f"face_{who}_{expr}.png")
    if not _fresh(p):
        draw_face(who, expr).save(p)
    return p


# --------------------------------------------------------------------------------------------------- body atlases
AW, AH = 2304, 1024


def _font(sz):
    return ImageFont.truetype(FONT, sz)


class Atlas:
    """cylindrical atlas painter. z0/z1: bean bottom/top (D). rfun(z) -> x radius, sy = depth ratio."""

    def __init__(self, z0, z1, rfun, sy, base):
        self.z0, self.z1, self.r, self.sy = z0, z1, rfun, sy
        self.img = Image.new("RGBA", (AW, AH), base + (255,))
        self.mask = Image.new("L", (AW, AH), 0)       # 255 = reflective band (roughness/spec), 128 = raised strap
        self.d = ImageDraw.Draw(self.img); self.md = ImageDraw.Draw(self.mask)

    def xy(self, a_deg, z):
        return ((0.5 + a_deg / 360.0) * AW, (1 - (z - self.z0) / (self.z1 - self.z0)) * AH)

    def px_per_D_h(self, a_deg, z):
        a = math.radians(a_deg); R = max(self.r(z), 0.05)
        ds = R * math.sqrt(math.cos(a) ** 2 + (self.sy * math.sin(a)) ** 2)       # D per radian
        return AW / (2 * math.pi) / ds

    def px_per_D_v(self):
        return AH / (self.z1 - self.z0)

    def band(self, za, zb, col, mask=0):
        y0 = self.xy(0, zb)[1]; y1 = self.xy(0, za)[1]
        self.d.rectangle([0, y0, AW, y1], fill=col)
        if mask: self.md.rectangle([0, y0, AW, y1], fill=mask)

    def vline(self, a, za, zb, wD, col, mask=0):
        x, y0 = self.xy(a, zb); _, y1 = self.xy(a, za)
        w = wD * self.px_per_D_h(a, (za + zb) / 2)
        self.d.rectangle([x - w / 2, y0, x + w / 2, y1], fill=col)
        if mask: self.md.rectangle([x - w / 2, y0, x + w / 2, y1], fill=mask)

    def paste(self, im, a, z, wD, hD):
        x, y = self.xy(a, z)
        w = int(wD * self.px_per_D_h(a, z)); h = int(hD * self.px_per_D_v())
        im = im.resize((w, h), Image.LANCZOS)
        self.img.alpha_composite(im, (int(x - w / 2), int(y - h / 2)))

    def hline(self, a0, a1, z, wD, col):
        p0 = self.xy(a0, z); p1 = self.xy(a1, z)
        self.d.line([p0, p1], fill=col, width=max(2, int(wD * self.px_per_D_v())))

    def cloth_noise(self, seed=3, amp=0.05, folds=None, fold_col=(0, 0, 0)):
        rng = np.random.default_rng(seed)
        arr = np.asarray(self.img).astype(np.float32)
        n = rng.normal(0, 1, (AH // 16, AW // 16)).astype(np.float32)
        n = np.asarray(Image.fromarray(n).resize((AW, AH), Image.BICUBIC))
        n2 = rng.normal(0, 1, (AH // 4, AW // 4)).astype(np.float32)
        n2 = np.asarray(Image.fromarray(n2).resize((AW, AH), Image.BICUBIC))
        k = 1 + amp * (0.7 * n + 0.3 * n2)
        arr[..., :3] *= k[..., None]
        self.img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
        self.d = ImageDraw.Draw(self.img)
        if folds:
            lay = Image.new("RGBA", (AW, AH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
            for (a0, z0, a1, z1, a2, z2) in folds:
                pts = []
                for i in range(21):
                    t = i / 20
                    a = (1 - t) ** 2 * a0 + 2 * (1 - t) * t * a1 + t * t * a2
                    z = (1 - t) ** 2 * z0 + 2 * (1 - t) * t * z1 + t * t * z2
                    pts.append(self.xy(a, z))
                ld.line(pts, fill=fold_col + (40,), width=14, joint="curve")
            lay = lay.filter(ImageFilter.GaussianBlur(6))
            self.img = Image.alpha_composite(self.img, lay); self.d = ImageDraw.Draw(self.img)

    def save(self, name):
        p = os.path.join(TEX, name + ".png"); pm = os.path.join(TEX, name + "_mask.png")
        self.img.convert("RGB").save(p); self.mask.save(pm)
        return p, pm


def rescue_patch():
    W, H = 900, 300
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([3, 3, W - 4, H - 4], 34, fill=(30, 29, 35, 255), outline=(22, 15, 19, 255), width=14)
    f = _font(176)
    d.text((W / 2, H / 2 + 4), "RESCUE", font=f, fill=(244, 244, 238, 255), anchor="mm")
    return im


def flag_patch():
    W, H = 540, 360
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(165, 25, 49), (244, 245, 248), (45, 42, 74), (45, 42, 74), (244, 245, 248), (165, 25, 49)]
    for i, c in enumerate(cols):
        d.rectangle([0, i * H / 6, W, (i + 1) * H / 6], fill=c + (255,))
    d.rectangle([0, 0, W - 1, H - 1], outline=(22, 15, 19, 255), width=16)
    return im


def uniform_atlas(name, z0, z1, rfun, sy, wet=False, straps=True, seed=3):
    """orange rescue jacket bean: one cloth colour, black hem band (= the trousers), two matte silver bands,
    RESCUE patch, Thai flag on the screen-left upper side, zip, pockets, seams at half ink weight."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p) and _fresh(os.path.join(TEX, name + "_mask.png")):
        return p, os.path.join(TEX, name + "_mask.png")
    os.makedirs(TEX, exist_ok=True)
    orange = (200, 88, 27) if wet else (232, 115, 42)
    A = Atlas(z0, z1, rfun, sy, orange)
    H = z1 - z0
    seam = (120, 52, 18, 255) if not wet else (100, 42, 14, 255)
    # silver reflective bands (matte, not chrome)
    for zc in (z0 + 0.36 * H, z0 + 0.50 * H):
        A.band(zc - 0.035, zc + 0.035, (200, 204, 211, 255), mask=255)
    # zip + pockets + side seams (half ink weight 0.012 D)
    A.vline(0, z0 + 0.12, z1 - 0.05, 0.014, seam)
    for s in (-1, 1):
        A.hline(s * 18, s * 50, z0 + 0.26 * H, 0.012, seam)
        A.vline(s * 50, z0 + 0.15, z0 + 0.26 * H, 0.012, seam)
        A.vline(s * 90, z0 + 0.1, z1 - 0.2, 0.012, seam)
    # hem band: black trousers + belt + buckle
    A.band(z0 - 0.01, z0 + 0.14, (26, 26, 31, 255))
    A.band(z0 + 0.12, z0 + 0.165, (14, 13, 17, 255))
    A.vline(0, z0 + 0.115, z0 + 0.17, 0.07, (176, 180, 188, 255), mask=200)
    if straps:
        for s in (-1, 1):
            A.vline(s * 30, z0 + 0.62 * H, z1 + 0.05, 0.075, (43, 43, 49, 255), mask=128)
            A.vline(s * 150, z0 + 0.55 * H, z1 + 0.05, 0.075, (43, 43, 49, 255), mask=128)
    A.paste(rescue_patch(), 14, z0 + 0.71 * H, 0.33, 0.11)
    A.paste(flag_patch(), -62, z0 + 0.74 * H, 0.17, 0.115)
    A.cloth_noise(seed, 0.022, folds=[(-40, z0 + 0.9, -25, z0 + 0.75, -32, z0 + 0.55),
                                     (35, z0 + 0.95, 22, z0 + 0.8, 30, z0 + 0.6),
                                     (-12, z0 + 0.35, 0, z0 + 0.3, 14, z0 + 0.37),
                                     (120, z0 + 1.0, 135, z0 + 0.7, 125, z0 + 0.45),
                                     (-120, z0 + 1.0, -135, z0 + 0.7, -125, z0 + 0.45)])
    return A.save(name)


def shirt_atlas(name, z0, z1, rfun, sy, seed=5):
    """infected driver: light-blue office shirt, loosened dark-red tie, jagged torn hem over grey trousers,
    rips showing grey-green skin, stains at the collar."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p, os.path.join(TEX, name + "_mask.png")
    os.makedirs(TEX, exist_ok=True)
    A = Atlas(z0, z1, rfun, sy, (166, 190, 214))
    H = z1 - z0
    rng = random.Random(seed)
    # grey trousers + jagged shirt hem
    A.band(z0 - 0.01, z0 + 0.22, (88, 92, 100, 255))
    pts = []
    for i in range(0, 73):
        a = -180 + i * 5
        z = z0 + 0.22 + (0.05 if i % 2 else -0.0) + rng.uniform(-0.02, 0.03)
        pts.append(A.xy(a, z))
    pts += [A.xy(180, z0 + 0.12), A.xy(-180, z0 + 0.12)]
    A.d.polygon(pts, fill=(88, 92, 100, 255))
    A.d.line(pts[:-2], fill=(70, 80, 96, 255), width=8)
    # placket buttons
    A.vline(0, z0 + 0.2, z1 - 0.12, 0.012, (110, 132, 158, 255))
    for k in range(4):
        x, y = A.xy(4, z0 + 0.35 + k * 0.22)
        A.d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(236, 238, 240, 255), outline=(90, 100, 120, 255), width=3)
    # collar V + loosened tie
    for s in (-1, 1):
        A.d.polygon([A.xy(0, z1 - 0.18), A.xy(s * 34, z1 - 0.02), A.xy(s * 30, z1 - 0.28)], fill=(186, 206, 226, 255),
                    outline=(70, 90, 116, 255))
    A.d.polygon([A.xy(-4.5, z1 - 0.26), A.xy(4.5, z1 - 0.26), A.xy(7.5, z1 - 0.72), A.xy(-1, z1 - 0.86),
                 A.xy(-6, z1 - 0.70)], fill=(125, 42, 48, 255), outline=(22, 15, 19, 255))
    A.d.polygon([A.xy(-6, z1 - 0.15), A.xy(6, z1 - 0.15), A.xy(4, z1 - 0.27), A.xy(-4, z1 - 0.27)],
                fill=(125, 42, 48, 255), outline=(22, 15, 19, 255))
    # rips (skin showing) and stains
    skin = (150, 165, 138, 255)
    for (a, z, w, h) in [(-42, z0 + 0.50, 14, 0.09), (150, z0 + 0.6, 16, 0.10)]:
        poly = []
        for k in range(12):
            t = k / 12 * 2 * math.pi
            rr = 1 + 0.25 * (k % 2)
            poly.append(A.xy(a + w / 2 * math.cos(t) * rr, z + h / 2 * math.sin(t) * rr))
        A.d.polygon(poly, fill=(112, 124, 104, 255), outline=(40, 34, 38, 255), width=6)
    lay = Image.new("RGBA", (AW, AH), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for (a, z, r, c) in [(-20, z1 - 0.3, 60, (110, 70, 52, 90)), (25, z1 - 0.45, 45, (120, 40, 40, 80)),
                         (-60, z0 + 0.4, 70, (90, 90, 70, 70)), (70, z0 + 0.5, 50, (110, 60, 50, 70))]:
        x, y = A.xy(a, z); ld.ellipse([x - r * 1.4, y - r, x + r * 1.4, y + r], fill=c)
    lay = lay.filter(ImageFilter.GaussianBlur(14))
    A.img = Image.alpha_composite(A.img, lay); A.d = ImageDraw.Draw(A.img)
    A.cloth_noise(seed, 0.02, folds=[(-40, z0 + 1.0, -25, z0 + 0.75, -32, z0 + 0.5),
                                    (35, z0 + 1.0, 22, z0 + 0.8, 30, z0 + 0.55)])
    return A.save(name)


def gauge_png(bars=3):
    p = os.path.join(TEX, f"gauge_{bars}.png")
    if _fresh(p): return p
    os.makedirs(TEX, exist_ok=True)
    W, H = 600, 240
    im = Image.new("RGBA", (W, H), (14, 14, 18, 255)); d = ImageDraw.Draw(im)
    on = {3: (31, 214, 85), 2: (255, 200, 40), 1: (255, 42, 26)}.get(bars, (31, 214, 85))
    for i in range(3):
        c = on if i < bars else (46, 46, 54)
        d.rounded_rectangle([36 + i * 182, 40, 36 + i * 182 + 160, 200], 18, fill=c + (255,))
    im.save(p); return p


def hair_strokes(name="hair_strokes", base=(20, 20, 24), seed=7):
    """painted strand strokes at ~10 % contrast (like the ref hat hatching), tileable-ish, used in object space."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p
    W = 1024
    im = Image.new("RGB", (W, W), base); d = ImageDraw.Draw(im); rng = random.Random(seed)
    for _ in range(260):
        x = rng.uniform(0, W); y = rng.uniform(0, W); L = rng.uniform(40, 120); a = rng.uniform(-0.5, 0.5) - math.pi / 2
        c = tuple(int(v * rng.uniform(1.25, 1.7)) + 6 for v in base)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=c, width=rng.choice([3, 4, 5]))
    im = im.filter(ImageFilter.GaussianBlur(1.2)); im.save(p); return p


if __name__ == "__main__":
    tiles = []
    for who, ex in EXPRS.items():
        for e in ex:
            im = Image.open(face_png(who, e))
            bg = Image.new("RGBA", im.size, (184, 195, 168, 255) if who == "driver" else (247, 242, 234, 255))
            tiles.append(Image.alpha_composite(bg, im).resize((256, 256)))
    sheet = Image.new("RGB", (256 * 7, 256 * 3), (40, 40, 40))
    i = 0
    for r, (who, ex) in enumerate(EXPRS.items()):
        for c, e in enumerate(ex):
            sheet.paste(tiles[i].convert("RGB"), (256 * c, 256 * r)); i += 1
    sheet.save(os.path.join(TEX, "faces_sheet.png"))
    for b in (1, 2, 3): gauge_png(b)
    hair_strokes()
    print("ok")
