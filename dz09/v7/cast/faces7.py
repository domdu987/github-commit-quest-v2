"""faces7.py -- PIL textures for the v7 cast (no bpy): sheet-style face decals, jacket / sleeve / shirt / trouser atlases.

Faces are DESIGNED in front-view head coordinates measured on uploads/character_sheet.webp (x right, y up, head
radius 0.5, centre 0,0) and stored in ANGULAR sphere space so they wrap with the head in 3D:
    u = 0.5 + theta / (2 A),  v = 0.5 + phi / (2 A),  A = FACE_A deg
    phi = asin(y / 0.5),  theta = asin(x / (0.5 cos phi))      (theta + toward the character's LEFT = +X)
So a front render of the sphere reproduces the sheet drawing 1:1, and a 3/4 view foreshortens it like a real head.

Sheet numbers (Kong, head D = 120 px in the sheet): eyes solid vertical ovals 0.075 x 0.19 D at x = +-0.16, y = 0;
brows bars 0.046 D thick from (0.05, 0.135) to (0.30, 0.21); smile 0.26 D wide at y = -0.25; stubble = short ticks
along the jaw (y -0.36 .. -0.45). Line weight 0.022-0.025 D.
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, "tex")
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FONT = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
FACE_A = 80.0
N = 2048
INK = (22, 15, 19, 255)
RED_IN = (120, 30, 40, 255)
TONGUE = (226, 118, 128, 255)
WHITE = (252, 251, 247, 255)
LW = 0.024          # sheet line weight in D

EXPRS = {
    "kong": ["determined", "neutral", "tired", "guilty", "alarmed", "shouting", "blink"],
    "crew": ["neutral", "shouting", "scared", "blink"],
    "driver": ["still", "head_lift", "lunge"],
}
SWEAT = {("kong", "alarmed"), ("kong", "guilty"), ("crew", "scared")}


# ------------------------------------------------------------------------------------------- front coords -> decal
def P(x, y):
    yy = max(-0.4999, min(0.4999, y))
    ph = math.asin(yy / 0.5)
    c = 0.5 * math.cos(ph)
    th = math.asin(max(-0.999, min(0.999, x / c)))
    k = N / (2 * math.radians(FACE_A))
    return (N / 2 + th * k, N / 2 - ph * k)


def _px(d):           # D -> decal px at the face centre (front)
    return d / 0.5 * N / (2 * math.radians(FACE_A))


def poly(dr, pts, fill=None, outline=None, w=LW):
    q = [P(*p) for p in pts]
    if fill: dr.polygon(q, fill=fill)
    if outline: line(dr, list(pts) + [pts[0]], w, outline)


def line(dr, pts, w=LW, col=INK, n=6):
    dense = []
    for a, b in zip(pts, pts[1:]):
        for i in range(n):
            t = i / n; dense.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
    dense.append(pts[-1])
    q = [P(*p) for p in dense]
    W = max(1, int(_px(w)))
    dr.line(q, fill=col, width=W, joint="curve")
    r = W / 2
    for x, y in (q[0], q[-1]):
        dr.ellipse([x - r, y - r, x + r, y + r], fill=col)


def ell_pts(cx, cy, rx, ry, n=48, a0=0, a1=360, rot=0.0):
    out = []
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        x, y = rx * math.cos(a), ry * math.sin(a)
        out.append((cx + x * cr - y * sr, cy + x * sr + y * cr))
    return out


def ell(dr, cx, cy, rx, ry, fill=None, outline=None, w=LW, rot=0.0):
    pts = ell_pts(cx, cy, rx, ry, rot=rot)
    poly(dr, pts[:-1], fill=fill, outline=outline, w=w)


def quad(a, c, b, n=16):
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * c[0] + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * c[1] + t * t * b[1]) for t in [i / n for i in range(n + 1)]]


def brow(dr, s, inner, outer, w=0.046, col=INK):
    """thick sheet brow: a tapered bar, inner end (near the nose) to outer end. s = +1 character's left (screen right)."""
    (xi, yi), (xo, yo) = inner, outer
    xi, xo = s * xi, s * xo
    dx, dy = xo - xi, yo - yi; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    wi, wo = w * 0.5, w * 0.42
    pts = [(xi + nx * wi, yi + ny * wi), (xo + nx * wo, yo + ny * wo), (xo - nx * wo, yo - ny * wo), (xi - nx * wi, yi - ny * wi)]
    poly(dr, pts, fill=col)
    for (x, y), r in (((xi, yi), wi), ((xo, yo), wo)):
        ell(dr, x, y, r, r, fill=col)


def oval_eye(dr, s, x=0.16, y=0.0, rx=0.038, ry=0.095, col=INK, dy=0.0):
    ell(dr, s * x, y + dy, rx, ry, fill=col)


def ring_eye(dr, s, x=0.16, y=0.01, rx=0.072, ry=0.088, pr=0.026, pcol=INK, fill=WHITE, pdx=0.0, pdy=0.0):
    ell(dr, s * x, y, rx, ry, fill=fill, outline=INK, w=0.02)
    ell(dr, s * x + pdx, y + pdy, pr, pr, fill=pcol)


def stubble(dr, n=15, col=(40, 36, 42, 255)):
    """short ticks along the jaw edge, like the sheet."""
    for i in range(n):
        t = (i + 0.5) / n
        a = math.radians(-152 + 124 * t)            # around the lower rim of the face
        rr = 0.43 + 0.012 * ((i * 7) % 3)
        x, y = rr * math.cos(a), rr * math.sin(a)
        nx, ny = math.cos(a), math.sin(a)
        L = 0.038
        line(dr, [(x - nx * L * 0.5, y - ny * L * 0.5), (x + nx * L * 0.5, y + ny * L * 0.5)], 0.014, col, n=2)


def open_mouth(dr, cx, top, w, h, tongue=True, teeth=False, col=RED_IN, round_top=False):
    """sheet open mouth: flat-ish top, round bottom, dark red inside, pink tongue, ink outline."""
    pts = [(cx - w / 2, top), (cx + w / 2, top)] + [(cx + w / 2 * math.cos(k / 24 * math.pi), top - h * math.sin(k / 24 * math.pi))
                                                    for k in range(25)]
    if round_top:
        pts = [(cx + w / 2 * math.cos(k / 24 * math.pi), top + h * 0.18 * math.sin(k / 24 * math.pi)) for k in range(25)] + pts[2:]
    poly(dr, pts, fill=col)
    if tongue:
        ell(dr, cx, top - h * 0.74, w * 0.28, h * 0.22, fill=TONGUE)
    if teeth:
        k = 6
        for i in range(k):
            x0 = cx - w / 2 + w * (i + 0.15) / k; x1 = cx - w / 2 + w * (i + 0.85) / k
            poly(dr, [(x0, top), (x1, top), ((x0 + x1) / 2, top - h * 0.26)], fill=WHITE)
        for i in range(k - 2):
            x0 = cx - w * 0.36 + w * 0.72 * (i + 0.15) / (k - 2); x1 = cx - w * 0.36 + w * 0.72 * (i + 0.85) / (k - 2)
            poly(dr, [(x0, top - h * 0.95), (x1, top - h * 0.95), ((x0 + x1) / 2, top - h * 0.68)], fill=WHITE)
    poly(dr, pts, outline=INK, w=0.022)


def wavy(dr, cx, cy, w, amp, n=2, lw=0.022):
    pts = [(cx - w / 2 + w * i / 30, cy + amp * math.sin(i / 30 * n * 2 * math.pi)) for i in range(31)]
    line(dr, pts, lw, n=1)


def blush(img, a=40, col=(236, 128, 140)):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for s in (-1, 1): ell(d, s * 0.24, -0.13, 0.06, 0.035, fill=col + (a,))
    return Image.alpha_composite(img, lay.filter(ImageFilter.GaussianBlur(_px(0.015))))


def draw_face(who="kong", expr="determined"):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    if who == "crew" and expr != "blink": img = blush(img, 30)
    d = ImageDraw.Draw(img)
    if who == "kong": stubble(d)
    if who in ("kong", "crew"):
        young = who == "crew"
        bw = 0.048 if young else 0.056
        if expr == "determined":
            for s in (-1, 1):
                oval_eye(d, s); brow(d, s, (0.05, 0.125), (0.30, 0.20), bw)
            line(d, quad((-0.13, -0.235), (0.0, -0.285), (0.13, -0.23)), 0.024)
        elif expr == "neutral":
            for s in (-1, 1):
                oval_eye(d, s, ry=0.085); brow(d, s, (0.06, 0.175), (0.29, 0.19), bw)
            line(d, quad((-0.09, -0.25), (0.0, -0.262), (0.09, -0.248)), 0.022)
        elif expr == "blink":
            for s in (-1, 1):
                line(d, quad((s * 0.10, 0.005), (s * 0.16, -0.035), (s * 0.22, 0.005)), 0.028)
                brow(d, s, (0.06, 0.17), (0.29, 0.185), bw)
            line(d, quad((-0.09, -0.25), (0.0, -0.262), (0.09, -0.248)), 0.022)
        elif expr == "tired":
            for s in (-1, 1):
                # heavy lid: half oval under a straight lid line
                pts = ell_pts(s * 0.16, 0.02, 0.045, 0.07, n=24, a0=180, a1=360)
                poly(d, pts, fill=INK)
                line(d, [(s * 0.095, 0.022), (s * 0.225, 0.016)], 0.026)
                line(d, quad((s * 0.11, -0.085), (s * 0.16, -0.10), (s * 0.21, -0.083)), 0.012, (92, 86, 104, 255))
                brow(d, s, (0.06, 0.14), (0.29, 0.105), bw * 0.9)
            line(d, quad((-0.08, -0.262), (0.0, -0.25), (0.08, -0.266)), 0.022)
        elif expr == "guilty":
            for s in (-1, 1):
                oval_eye(d, s, rx=0.034, ry=0.07, dy=-0.03)
                line(d, [(s * 0.11, 0.06), (s * 0.215, 0.05)], 0.02)          # heavy upper lid
                brow(d, s, (0.05, 0.20), (0.29, 0.135), bw * 0.9)              # worried: inner ends up
            wavy(d, 0, -0.255, 0.16, 0.012, 2)
        elif expr in ("alarmed", "scared"):
            for s in (-1, 1):
                ring_eye(d, s, pr=0.024 if expr == "alarmed" else 0.02, pdy=-0.005)
                if expr == "alarmed": brow(d, s, (0.06, 0.20), (0.30, 0.26), bw * 0.85)
                else: brow(d, s, (0.05, 0.215), (0.29, 0.165), bw * 0.85)
            if expr == "alarmed":
                ell(d, 0, -0.27, 0.045, 0.055, fill=RED_IN, outline=INK, w=0.02)
            else:
                wavy(d, 0, -0.26, 0.17, 0.014, 3, 0.02)
        elif expr == "shouting":
            for s in (-1, 1):
                ell(d, s * 0.16, 0.02, 0.036, 0.07, fill=INK)
                brow(d, s, (0.045, 0.10), (0.30, 0.215), bw * 1.08)
            open_mouth(d, 0, -0.17, 0.30, 0.20)
        else:
            raise KeyError(expr)
    elif who == "driver":
        UL = (70, 84, 66, 255)
        if expr == "still":
            for s in (-1, 1):
                # half-shut slits, a sliver of white, dark under-eye
                pts = ell_pts(s * 0.16, 0.0, 0.06, 0.03, n=24, a0=180, a1=360)
                poly(d, pts, fill=(236, 236, 222, 255))
                ell(d, s * 0.165, -0.012, 0.012, 0.012, fill=(170, 20, 25, 255))
                line(d, [(s * 0.09, 0.006), (s * 0.235, 0.0)], 0.026)
                line(d, quad((s * 0.10, -0.075), (s * 0.16, -0.095), (s * 0.22, -0.075)), 0.016, UL)
                brow(d, s, (0.06, 0.12), (0.28, 0.115), 0.032)
            ell(d, 0.012, -0.27, 0.05, 0.022, fill=(60, 26, 30, 255), outline=INK, w=0.016)
        else:
            lunge = expr == "lunge"
            for s in (-1, 1):
                ring_eye(d, s, rx=0.078 if lunge else 0.068, ry=0.092 if lunge else 0.08, pr=0.014, pcol=(205, 18, 26, 255),
                         fill=(246, 245, 232, 255))
                line(d, quad((s * 0.09, -0.11), (s * 0.16, -0.135), (s * 0.235, -0.11)), 0.016, UL)
                if lunge: brow(d, s, (0.045, 0.11), (0.30, 0.225), 0.04)
                else: brow(d, s, (0.06, 0.155), (0.28, 0.15), 0.032)
            if lunge:
                open_mouth(d, 0, -0.18, 0.32, 0.22, tongue=False, teeth=True, col=(90, 18, 26, 255))
            else:
                ell(d, 0, -0.28, 0.045, 0.06, fill=(70, 20, 26, 255), outline=INK, w=0.018)
            # veins at the temples
            for s in (-1, 1):
                line(d, [(s * 0.33, 0.12), (s * 0.36, 0.06), (s * 0.34, 0.0)], 0.01, (90, 110, 96, 255), n=3)
    return img.resize((N // 2, N // 2), Image.LANCZOS)


def _fresh(p, deps=()):
    if not os.path.exists(p): return False
    t = os.path.getmtime(p)
    return all(t > os.path.getmtime(x) for x in (__file__,) + tuple(deps))


def face_png(who="kong", expr="determined"):
    os.makedirs(TEX, exist_ok=True)
    p = os.path.join(TEX, f"face_{who}_{expr}.png")
    if not _fresh(p): draw_face(who, expr).save(p)
    return p


def front_preview(who, expr, skin=(247, 242, 234), size=400):
    """orthographic front view of the decal on the sphere (for checking against the sheet without Blender)."""
    dec = np.asarray(Image.open(face_png(who, expr)).convert("RGBA")).astype(np.float32) / 255
    M = dec.shape[0]
    out = np.zeros((size, size, 4), np.float32)
    ys, xs = np.mgrid[0:size, 0:size]
    x = (xs + 0.5) / size - 0.5; y = 0.5 - (ys + 0.5) / size
    inside = x * x + y * y < 0.25
    ph = np.arcsin(np.clip(y / 0.5, -1, 1)); c = 0.5 * np.cos(ph)
    th = np.arcsin(np.clip(x / np.maximum(c, 1e-6), -1, 1))
    k = 1 / (2 * math.radians(FACE_A))
    u = 0.5 + th * k; v = 0.5 - ph * k
    ok = inside & (u >= 0) & (u < 1) & (v >= 0) & (v < 1)
    a = np.zeros_like(x); col = np.zeros(x.shape + (3,))
    ui = np.clip((u * M).astype(int), 0, M - 1); vi = np.clip((v * M).astype(int), 0, M - 1)
    a[ok] = dec[vi[ok], ui[ok], 3]; col[ok] = dec[vi[ok], ui[ok], :3]
    base = np.array(skin) / 255
    rgb = base * (1 - a[..., None]) + col * a[..., None]
    out[..., :3] = rgb; out[..., 3] = inside
    im = Image.fromarray((out * 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(im); d.ellipse([1, 1, size - 2, size - 2], outline=INK, width=max(2, int(size * 0.024)))
    return im


# --------------------------------------------------------------------------------------------------- atlases
def _font(sz):
    return ImageFont.truetype(FONT, sz)


class Atlas:
    """painter for a lofted body part: u = 0.5 + azimuth/360 (front = 0.5, + toward +X), v = (z - z0)/(z1 - z0).
    circ(z) -> circumference in D at height z (for D-true horizontal sizes)."""

    def __init__(self, z0, z1, circ, base, W=4096, H=2048):
        self.z0, self.z1, self.circ, self.W, self.H = z0, z1, circ, W, H
        self.img = Image.new("RGBA", (W, H), base + (255,))
        self.d = ImageDraw.Draw(self.img)

    def xy(self, a, z):
        return ((0.5 + a / 360.0) * self.W, (1 - (z - self.z0) / (self.z1 - self.z0)) * self.H)

    def pxD_h(self, z):
        return self.W / max(self.circ(z), 0.2)

    def pxD_v(self):
        return self.H / (self.z1 - self.z0)

    def deg(self, wD, z):          # a width in D -> degrees of azimuth at height z
        return wD / max(self.circ(z), 0.2) * 360

    def band(self, za, zb, col):
        y0 = self.xy(0, zb)[1]; y1 = self.xy(0, za)[1]
        self.d.rectangle([0, y0, self.W, y1], fill=col)

    def vline(self, a, za, zb, wD, col):
        x, y0 = self.xy(a, zb); _, y1 = self.xy(a, za)
        w = wD * self.pxD_h((za + zb) / 2)
        self.d.rectangle([x - w / 2, y0, x + w / 2, y1], fill=col)

    def hline(self, a0, a1, z, wD, col):
        self.d.line([self.xy(a0, z), self.xy(a1, z)], fill=col, width=max(2, int(wD * self.pxD_v())))

    def pline(self, pts, wD, col):
        q = [self.xy(a, z) for a, z in pts]
        w = max(2, int(wD * self.pxD_v()))
        self.d.line(q, fill=col, width=w, joint="curve")
        for x, y in (q[0], q[-1]): self.d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)

    def ppoly(self, pts, fill, outline=None, wD=0.02):
        q = [self.xy(a, z) for a, z in pts]
        self.d.polygon(q, fill=fill)
        if outline: self.pline(list(pts) + [pts[0]], wD, outline)

    def paste(self, im, a, z, wD, hD):
        x, y = self.xy(a, z)
        w = int(wD * self.pxD_h(z)); h = int(hD * self.pxD_v())
        im = im.resize((max(w, 2), max(h, 2)), Image.LANCZOS)
        self.img.alpha_composite(im, (int(x - w / 2), int(y - h / 2)))

    def noise(self, seed=3, amp=0.02):
        rng = np.random.default_rng(seed)
        arr = np.asarray(self.img).astype(np.float32)
        n = rng.normal(0, 1, (self.H // 32, self.W // 32)).astype(np.float32)
        n = np.asarray(Image.fromarray(n).resize((self.W, self.H), Image.BICUBIC))
        arr[..., :3] *= (1 + amp * n)[..., None]
        self.img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)); self.d = ImageDraw.Draw(self.img)

    def save(self, name):
        p = os.path.join(TEX, name + ".png"); self.img.convert("RGB").save(p); return p


def rescue_patch():
    W, H = 900, 300
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([3, 3, W - 4, H - 4], 30, fill=(28, 27, 32, 255), outline=(22, 15, 19, 255), width=12)
    d.text((W / 2, H / 2 + 4), "RESCUE", font=_font(190), fill=(244, 244, 238, 255), anchor="mm")
    return im


def flag_patch():
    W, H = 540, 360
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cols = [(178, 30, 52), (244, 245, 248), (40, 44, 96), (40, 44, 96), (244, 245, 248), (178, 30, 52)]
    for i, c in enumerate(cols): d.rectangle([0, i * H / 6, W, (i + 1) * H / 6], fill=c + (255,))
    d.rectangle([0, 0, W - 1, H - 1], outline=(22, 15, 19, 255), width=22)
    return im


ORANGE = (236, 120, 40); ORANGE_WET = (200, 92, 28)
SILVER = (206, 210, 216)
SEAM = (150, 62, 18, 255)


def jacket_atlas(name, z0, z1, circ, wet=False, straps=True, band_z=None):
    """the sheet's orange rescue jacket (short-sleeve shirt cut): collar points, zip placket, chest pockets,
    one silver reflective band, RESCUE patch on the character's left chest, black backpack straps."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p
    os.makedirs(TEX, exist_ok=True)
    o = ORANGE_WET if wet else ORANGE
    A = Atlas(z0, z1, circ, o)
    seam = (126, 52, 16, 255) if wet else SEAM
    H = z1 - z0
    bz = band_z or (z0 + 0.27 * H)
    A.band(bz - 0.045, bz + 0.045, SILVER + (255,))
    A.hline(-180, 180, bz - 0.045, 0.012, (110, 112, 120, 255)); A.hline(-180, 180, bz + 0.045, 0.012, (110, 112, 120, 255))
    # hem
    A.hline(-180, 180, z0 + 0.03, 0.016, seam)
    # zip placket + collar points (V)
    A.vline(0, z0 + 0.02, z1 - 0.20, 0.016, seam)
    zt = z1 - 0.04
    for s in (-1, 1):
        a_in, a_out = s * 2, s * 34
        A.ppoly([(s * 3, zt - 0.30), (s * 22, zt - 0.16), (s * 16, zt - 0.10), (s * 36, zt + 0.02), (s * 8, zt + 0.02)],
                tuple(int(c * 0.93) for c in o) + (255,), outline=(22, 15, 19, 255), wD=0.02)
        # chest pocket flaps
        a0 = s * 16; a1 = s * 44
        A.pline([(a0, z0 + 0.62 * H), (a1, z0 + 0.62 * H)], 0.014, seam)
        A.pline([(a0, z0 + 0.62 * H), (a0, z0 + 0.44 * H)], 0.012, seam)
        A.pline([(a1, z0 + 0.62 * H), (a1, z0 + 0.44 * H)], 0.012, seam)
        # side seams
        A.vline(s * 92, z0 + 0.02, z1 - 0.08, 0.012, seam)
    if straps:
        for s in (-1, 1):
            A.ppoly([(s * 38, z1 + 0.02), (s * 52, z1 + 0.02), (s * 50, z0 + 0.36 * H), (s * 37, z0 + 0.36 * H)],
                    (34, 34, 40, 255), outline=(22, 15, 19, 255), wD=0.016)
            A.ppoly([(s * 140, z1 + 0.02), (s * 155, z1 + 0.02), (s * 150, z0 + 0.40 * H), (s * 136, z0 + 0.40 * H)],
                    (34, 34, 40, 255))
    A.paste(rescue_patch(), 4, z0 + 0.64 * H, 0.34, 0.12)
    A.noise(3, 0.025)
    return A.save(name)


def sleeve_atlas(name, wet=False, flag=False, band=True, col=None, cuff=None):
    """sleeve tube: u = 0.5 + angle/360 around the arm (0 = the outward side), v = 0 shoulder .. 1 hem."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p
    os.makedirs(TEX, exist_ok=True)
    o = col or (ORANGE_WET if wet else ORANGE)
    W, H = 1024, 1024
    im = Image.new("RGBA", (W, H), o + (255,)); d = ImageDraw.Draw(im)
    if band:
        d.rectangle([0, 0.66 * H, W, 0.80 * H], fill=SILVER + (255,))
        d.line([(0, 0.66 * H), (W, 0.66 * H)], fill=(110, 112, 120, 255), width=4)
        d.line([(0, 0.80 * H), (W, 0.80 * H)], fill=(110, 112, 120, 255), width=4)
    if cuff:
        d.rectangle([0, 0.90 * H, W, H], fill=cuff + (255,))
    d.rectangle([0, 0.955 * H, W, H], fill=tuple(int(c * 0.6) for c in o) + (255,))
    if flag:
        f = flag_patch().resize((int(W * 0.24), int(H * 0.30)), Image.LANCZOS)
        im.alpha_composite(f, (int(W * 0.5 - f.width / 2), int(H * 0.22)))
    A = Atlas(0, 1, lambda z: 1, (0, 0, 0)); A.img = im; A.W, A.H = W, H; A.noise(5, 0.02)
    A.img.convert("RGB").save(p); return p


def shirt_atlas(name, z0, z1, circ, seed=5):
    """infected driver: light-blue office shirt, loosened dark-red tie, collar, buttons, torn jagged hem (the hem
    itself is also cut in the mesh), rips showing grey-green skin, stains."""
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p
    os.makedirs(TEX, exist_ok=True)
    A = Atlas(z0, z1, circ, (170, 196, 222))
    H = z1 - z0; rng = random.Random(seed)
    line_c = (84, 104, 132, 255)
    A.vline(0, z0, z1 - 0.20, 0.014, line_c)
    for k in range(4):
        x, y = A.xy(4, z0 + 0.15 + k * 0.22)
        r = 0.018 * A.pxD_v(); A.d.ellipse([x - r, y - r, x + r, y + r], fill=(236, 238, 240, 255), outline=line_c, width=4)
    zt = z1 - 0.04
    for s in (-1, 1):
        A.ppoly([(s * 3, zt - 0.22), (s * 26, zt - 0.17), (s * 34, zt + 0.02), (s * 6, zt + 0.02)], (192, 212, 232, 255),
                outline=(22, 15, 19, 255), wD=0.02)
        A.vline(s * 92, z0, z1 - 0.08, 0.012, line_c)
    tie = (128, 36, 44, 255)
    A.ppoly([(-5, zt - 0.10), (5, zt - 0.10), (3.5, zt - 0.20), (-3.5, zt - 0.20)], tie, outline=(22, 15, 19, 255), wD=0.016)
    A.ppoly([(-3.5, zt - 0.20), (3.5, zt - 0.20), (8.5, zt - 0.70), (1, zt - 0.80), (-6.5, zt - 0.66)], tie,
            outline=(22, 15, 19, 255), wD=0.016)
    skin = (150, 165, 138, 255)
    for (a, z, w, h) in [(-38, z0 + 0.42 * H, 13, 0.11), (52, z0 + 0.58 * H, 10, 0.08), (150, z0 + 0.5 * H, 16, 0.12)]:
        pts = []
        for k in range(14):
            t = k / 14 * 2 * math.pi; rr = 1 + 0.3 * (k % 2)
            pts.append((a + w / 2 * math.cos(t) * rr, z + h / 2 * math.sin(t) * rr))
        A.ppoly(pts, skin, outline=(22, 15, 19, 255), wD=0.014)
    lay = Image.new("RGBA", (A.W, A.H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
    for (a, z, r, c) in [(-20, z1 - 0.3, 90, (110, 70, 52, 90)), (25, z1 - 0.5, 70, (120, 40, 40, 90)),
                         (-60, z0 + 0.3, 100, (90, 90, 70, 70)), (70, z0 + 0.35, 80, (110, 60, 50, 70))]:
        x, y = A.xy(a, z); ld.ellipse([x - r * 1.4, y - r, x + r * 1.4, y + r], fill=c)
    A.img = Image.alpha_composite(A.img, lay.filter(ImageFilter.GaussianBlur(24))); A.d = ImageDraw.Draw(A.img)
    A.noise(seed, 0.02)
    return A.save(name)


def hair_strokes(name="hair7", base=(22, 22, 27), seed=7):
    p = os.path.join(TEX, name + ".png")
    if _fresh(p): return p
    os.makedirs(TEX, exist_ok=True)
    W = 1024; im = Image.new("RGB", (W, W), base); d = ImageDraw.Draw(im); rng = random.Random(seed)
    for _ in range(220):
        x = rng.uniform(0, W); y = rng.uniform(0, W); L = rng.uniform(60, 160); a = rng.uniform(-0.4, 0.4) - math.pi / 2
        c = tuple(int(v * rng.uniform(1.3, 1.9)) + 6 for v in base)
        d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=c, width=rng.choice([4, 6, 8]))
    im.filter(ImageFilter.GaussianBlur(1.5)).save(p); return p


if __name__ == "__main__":
    tiles = []
    skins = {"kong": (247, 242, 234), "crew": (247, 242, 234), "driver": (184, 195, 168)}
    for who, ex in EXPRS.items():
        for e in ex:
            bg = Image.new("RGBA", (300, 300), (250, 244, 234, 255))
            bg.alpha_composite(front_preview(who, e, skins[who], 300))
            tiles.append(bg)
    sheet = Image.new("RGB", (300 * 7, 300 * 3), (40, 40, 40)); i = 0
    for r, (who, ex) in enumerate(EXPRS.items()):
        for c, e in enumerate(ex):
            sheet.paste(tiles[i].convert("RGB"), (300 * c, 300 * r)); i += 1
    sheet.save(os.path.join(TEX, "faces_front.png")); print("ok")
