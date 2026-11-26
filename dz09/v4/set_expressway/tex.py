"""tex.py -- code-drawn textures for the EP.1 expressway set (numpy + PIL, no bpy).

Every function returns a PNG path inside ./tex/, cached by name + VERSION (delete tex/ to redraw).
Thai text is set in Kanit (PROJ/fonts) through PIL with libraqm, so vowels and tone marks stack correctly.
Nothing here imitates a real operator, foundation or brand: sign names are place names, plates are fake numbers,
the rescue livery is our own "RESCUE 09" design.
"""
import os, math, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
TEX = os.path.join(HERE, "tex")
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
FONT_LATIN = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
VERSION = "v6"
os.makedirs(TEX, exist_ok=True)


def _path(name):
    return os.path.join(TEX, f"{name}_{VERSION}.png")


def _cached(name):
    p = _path(name)
    return p if os.path.exists(p) else None


def font(size, latin=False):
    return ImageFont.truetype(FONT_LATIN if latin else FONT, size, layout_engine=ImageFont.Layout.RAQM)


def _ctext(d, xy, text, f, fill):
    """centre text at xy."""
    bb = d.textbbox((0, 0), text, font=f)
    d.text((xy[0] - (bb[0] + bb[2]) / 2, xy[1] - (bb[1] + bb[3]) / 2), text, font=f, fill=fill)


def _noise(h, w, scale, seed, octaves=4):
    """smooth value noise in 0..1 (bilinear upsampled random grids)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o in range(octaves):
        gh, gw = max(2, int(h / scale * 2 ** o) + 2), max(2, int(w / scale * 2 ** o) + 2)
        g = rng.random((gh, gw)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, np.float32) / 255 * amp; tot += amp; amp *= 0.5
    return out / tot


# ---------------------------------------------------------------------------------------------------------------- signs
def sign_panel(key):
    """green overhead direction sign. key in SIGNS. 1024 x 512, white border, Thai + English + arrow."""
    name = f"sign_{key}"
    if _cached(name): return _path(name)
    th, en, arrow, exitno = SIGNS[key]
    W, H = 1024, 512
    im = Image.new("RGB", (W, H), (14, 98, 58)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, W - 10, H - 10), 26, outline=(236, 240, 236), width=12)
    if exitno:
        d.rounded_rectangle((W - 260, 34, W - 40, 120), 14, fill=(236, 240, 236))
        _ctext(d, (W - 150, 78), exitno, font(54, True), (14, 98, 58))
    _ctext(d, (W / 2 - (60 if exitno else 0), 170), th, font(150), (240, 244, 240))
    _ctext(d, (W / 2 - (60 if exitno else 0), 300), en, font(76, True), (240, 244, 240))
    # arrow(s)
    cx = W / 2
    for k, a in enumerate(arrow):
        x = cx + (k - (len(arrow) - 1) / 2) * 200
        if a == "down":
            d.rectangle((x - 18, 360, x + 18, 430), fill=(240, 244, 240)); d.polygon([(x - 52, 425), (x + 52, 425), (x, 488)], fill=(240, 244, 240))
        elif a == "up_left":
            d.line((x + 40, 480, x - 20, 400), fill=(240, 244, 240), width=34); d.polygon([(x - 70, 372), (x + 6, 362), (x - 46, 432)], fill=(240, 244, 240))
        elif a == "up_right":
            d.line((x - 40, 480, x + 20, 400), fill=(240, 244, 240), width=34); d.polygon([(x + 70, 372), (x - 6, 362), (x + 46, 432)], fill=(240, 244, 240))
    # weathering: soft grime from the top, a few streaks
    a = np.asarray(im, np.float32) / 255
    n = _noise(H, W, 90, 11)
    streak = np.asarray(Image.fromarray((np.random.default_rng(3).random((8, W)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    dirt = 0.80 + 0.2 * n - 0.10 * np.clip(streak - 0.55, 0, 1) * np.linspace(1, 0.2, H)[:, None]
    a = np.clip(a * dirt[..., None], 0, 1)
    Image.fromarray((a * 255).astype(np.uint8)).save(_path(name))
    return _path(name)


SIGNS = {
    "dindaeng": ("ดินแดง", "Din Daeng", ["up_left"], "2-04"),
    "rama9":    ("พระราม 9", "Rama IX", ["down", "down"], None),
    "bangna":   ("บางนา", "Bang Na", ["down"], None),
}


def led_board():
    """amber dot-matrix variable message sign: 'อุบัติเหตุข้างหน้า' / 'ACCIDENT AHEAD'. 1024 x 256 emission map."""
    name = "led_board_r1"          # review: word gaps in the latin line (it read "ACCIDENTAHEAD")
    if _cached(name): return _path(name)
    W, H = 1024, 256
    txt = Image.new("L", (W // 4, H // 4), 0); d = ImageDraw.Draw(txt)
    _ctext(d, (W // 8, 20), "อุบัติเหตุข้างหน้า", font(30), 255)
    fl = font(14, True); x = 8; y = 41
    words = ["ACCIDENT", "AHEAD", "SLOW"]
    ws = [d.textlength(wd, font=fl) for wd in words]; gap = 9
    x = (W // 4 - (sum(ws) + gap * (len(words) - 1))) / 2
    for wd, w_ in zip(words, ws):
        d.text((x, y), wd, font=fl, fill=255); x += w_ + gap
    m = np.asarray(txt, np.float32) / 255
    big = np.kron(m, np.ones((4, 4), np.float32))
    yy, xx = np.mgrid[0:H, 0:W]
    dots = (((xx % 4) - 1.5) ** 2 + ((yy % 4) - 1.5) ** 2) < 2.4
    on = (big > 0.4) & dots
    im = np.zeros((H, W, 3), np.float32)
    im[dots] = (0.06, 0.04, 0.02)
    im[on] = (1.0, 0.62, 0.12)
    Image.fromarray((im * 255).astype(np.uint8)).save(_path(name))
    return _path(name)


def plate(i):
    """generic Thai private-car plate: white, black text, fake number, province line. 512 x 240."""
    name = f"plate_{i}"
    if _cached(name): return _path(name)
    rng = np.random.default_rng(100 + i)
    letters = "กขคงจฉชฌญฐฒณดตถทธนบปผพฟภมยรลวศษสหฬอฮ"
    reg = f"{rng.integers(1, 9)}{letters[rng.integers(len(letters))]}{letters[rng.integers(len(letters))]} {rng.integers(1000, 9999)}"
    W, H = 512, 240
    im = Image.new("RGB", (W, H), (236, 234, 226)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, W - 6, H - 6), 18, outline=(20, 20, 24), width=8)
    _ctext(d, (W / 2, 92), reg, font(104), (18, 18, 22))
    _ctext(d, (W / 2, 190), "กรุงเทพมหานคร", font(52), (18, 18, 22))
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    im.save(_path(name)); return _path(name)


def livery():
    """rescue canopy side, 1024 x 512: white body, orange + red chevron band, RESCUE / กู้ภัย 09, 1669 (Thai EMS number)."""
    name = "livery"
    if _cached(name): return _path(name)
    W, H = 1024, 512
    im = Image.new("RGB", (W, H), (226, 226, 222)); d = ImageDraw.Draw(im)
    d.rectangle((0, 300, W, 380), fill=(226, 92, 28))
    for k in range(-2, 16):
        x = k * 80
        d.polygon([(x, 380), (x + 40, 380), (x + 80, 300), (x + 40, 300)], fill=(196, 34, 30))
    d.rectangle((0, 380, W, 400), fill=(30, 30, 36))
    _ctext(d, (W * 0.42, 150), "RESCUE", font(170, True), (196, 34, 30))
    _ctext(d, (W * 0.42, 262), "กู้ภัย 09  •  1669", font(64), (32, 32, 40))
    # star-ish cross badge, our own
    cx, cy = W * 0.87, 170
    d.ellipse((cx - 90, cy - 90, cx + 90, cy + 90), fill=(196, 34, 30))
    d.rectangle((cx - 22, cy - 62, cx + 22, cy + 62), fill=(240, 240, 236)); d.rectangle((cx - 62, cy - 22, cx + 62, cy + 22), fill=(240, 240, 236))
    a = np.asarray(im, np.float32) / 255
    n = _noise(H, W, 60, 21)
    a *= (0.86 + 0.14 * n)[..., None]
    a[int(H * 0.82):] *= 0.75
    Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).save(_path(name)); return _path(name)


def delivery_box():
    """green food-delivery box side, generic: white scooter pictogram, no brand. 512 x 512."""
    name = "delivery_box"
    if _cached(name): return _path(name)
    W = 512
    im = Image.new("RGB", (W, W), (28, 150, 64)); d = ImageDraw.Draw(im)
    d.rectangle((0, 0, W - 1, W - 1), outline=(18, 100, 44), width=18)
    c = (236, 244, 236)
    d.ellipse((130, 300, 210, 380), outline=c, width=18); d.ellipse((310, 300, 390, 380), outline=c, width=18)
    d.polygon([(170, 300), (230, 230), (340, 230), (360, 300)], fill=c)
    d.rectangle((300, 160, 330, 240), fill=c); d.rectangle((280, 150, 360, 172), fill=c)
    d.rectangle((150, 190, 240, 240), fill=c)
    a = np.asarray(im, np.float32) / 255 * (0.85 + 0.15 * _noise(W, W, 50, 5))[..., None]
    Image.fromarray((a * 255).astype(np.uint8)).save(_path(name)); return _path(name)


# ---------------------------------------------------------------------------------------------------------------- city
def tower_windows(k):
    """facade with a window grid; 5-15 % lit, warm and cool. RGB = emission colour (already dim), 512 x 1024."""
    name = f"tower_{k}"
    if _cached(name): return _path(name)
    rng = np.random.default_rng(500 + k)
    W, H = 512, 1024
    cols, rows = int(rng.integers(10, 18)), int(rng.integers(40, 70))
    im = np.zeros((H, W, 3), np.float32)
    base = np.array([0.006, 0.0065, 0.011]) * (0.8 + 0.4 * rng.random())
    im[:] = base
    cw, rh = W / cols, H / rows
    lit_p = 0.05 + 0.10 * rng.random()
    for r in range(rows):
        band = rng.random() < 0.15        # whole lit floors (offices)
        for c in range(cols):
            x0, y0 = int(c * cw + cw * 0.18), int(r * rh + rh * 0.22)
            x1, y1 = int((c + 1) * cw - cw * 0.18), int((r + 1) * rh - rh * 0.18)
            if rng.random() < (lit_p * (3.0 if band else 1.0)):
                warm = rng.random() < 0.65
                col = np.array([1.0, 0.62, 0.28]) if warm else np.array([0.62, 0.78, 1.0])
                im[y0:y1, x0:x1] = col * (0.35 + 0.65 * rng.random())
            else:
                im[y0:y1, x0:x1] = base * 1.8 + 0.003 * rng.random()
    Image.fromarray((np.clip(im, 0, 1) ** (1 / 2.2) * 255).astype(np.uint8)).save(_path(name)); return _path(name)


def city_ground():
    """the city under the deck: dark blocks, sodium street lines, sparse windows. 2048 x 2048 (tiles 600 D)."""
    name = "city_ground"
    if _cached(name): return _path(name)
    rng = np.random.default_rng(77)
    N = 2048
    im = np.zeros((N, N, 3), np.float32); im[:] = (0.010, 0.011, 0.018)
    n = _noise(N, N, 200, 8)
    im *= (0.6 + 0.8 * n)[..., None]
    # streets: irregular grid
    xs = np.cumsum(rng.integers(60, 180, 30)); ys = np.cumsum(rng.integers(60, 180, 30))
    for x in xs[xs < N]:
        im[:, x:x + 5] = (0.05, 0.03, 0.015)
        for y in range(0, N, 22): im[y:y + 3, x + 1:x + 4] = (1.0, 0.55, 0.18)
    for y in ys[ys < N]:
        im[y:y + 5, :] = (0.05, 0.03, 0.015)
        for x in range(0, N, 22): im[y + 1:y + 4, x:x + 3] = (1.0, 0.55, 0.18)
    # windows of low buildings
    k = rng.integers(0, N, (5000, 2))
    for (y, x) in k:
        if rng.random() < 0.3:
            im[y:y + 2, x:x + 3] = (0.9, 0.7, 0.4) if rng.random() < 0.6 else (0.5, 0.7, 0.9)
    Image.fromarray((np.clip(im, 0, 1) ** (1 / 2.2) * 255).astype(np.uint8)).save(_path(name)); return _path(name)


# ---------------------------------------------------------------------------------------------------------------- fx cards
def crack():
    """spiderweb windscreen crack, RGBA (white lines, alpha), 1024 x 1024; impact at (0.62, 0.42)."""
    name = "crack"
    if _cached(name): return _path(name)
    rng = np.random.default_rng(9)
    N = 1024
    im = Image.new("L", (N, N), 0); d = ImageDraw.Draw(im)
    cx, cy = 0.62 * N, 0.42 * N
    rays = []
    for k in range(17):
        a = k / 17 * 2 * math.pi + rng.normal(0, 0.12)
        L = rng.uniform(0.25, 0.75) * N
        pts = [(cx, cy)]; x, y = cx, cy; aa = a
        for s in range(14):
            aa += rng.normal(0, 0.10); st = L / 14
            x += math.cos(aa) * st; y += math.sin(aa) * st; pts.append((x, y))
        rays.append(pts)
        d.line(pts, fill=255, width=int(rng.integers(2, 5)))
        # side cracks
        for s in range(3, 13, 3):
            px, py = pts[s]; b = aa + rng.choice([-1, 1]) * rng.uniform(0.6, 1.1); l2 = rng.uniform(20, 90)
            d.line([(px, py), (px + math.cos(b) * l2, py + math.sin(b) * l2)], fill=200, width=2)
    for ring in (40, 95, 170, 260):
        for k in range(len(rays)):
            p0 = rays[k][min(len(rays[k]) - 1, int(ring / (0.05 * N)) + 1)]
            p1 = rays[(k + 1) % len(rays)][min(len(rays[(k + 1) % len(rays)]) - 1, int(ring / (0.05 * N)) + 1)]
            if rng.random() < 0.8:
                mid = ((p0[0] + p1[0]) / 2 + rng.normal(0, 8), (p0[1] + p1[1]) / 2 + rng.normal(0, 8))
                d.line([p0, mid, p1], fill=220, width=2)
    d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=255)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(0.8)), np.float32) / 255
    glow = np.asarray(im.filter(ImageFilter.GaussianBlur(6)), np.float32) / 255
    alpha = np.clip(a * 1.0 + glow * 0.35, 0, 1)
    out = np.dstack([np.full_like(alpha, 0.92), np.full_like(alpha, 0.94), np.full_like(alpha, 1.0), alpha])
    Image.fromarray((out * 255).astype(np.uint8), "RGBA").save(_path(name)); return _path(name)


def droplets():
    """rain droplets on glass as a height map (grey), 1024 x 1024, tileable enough."""
    name = "droplets"
    if _cached(name): return _path(name)
    rng = np.random.default_rng(12)
    N = 1024
    h = np.zeros((N, N), np.float32)
    yy, xx = np.mgrid[0:N, 0:N]
    for k in range(900):
        x, y, r = rng.integers(0, N), rng.integers(0, N), rng.uniform(2, 9)
        x0, x1, y0, y1 = max(0, int(x - r - 1)), min(N, int(x + r + 2)), max(0, int(y - r * 1.4 - 1)), min(N, int(y + r * 1.4 + 2))
        sub = 1 - ((xx[y0:y1, x0:x1] - x) / r) ** 2 - ((yy[y0:y1, x0:x1] - y) / (r * 1.3)) ** 2
        h[y0:y1, x0:x1] = np.maximum(h[y0:y1, x0:x1], np.sqrt(np.clip(sub, 0, 1)))
    # a few runs
    for k in range(40):
        x, y = rng.integers(0, N), rng.integers(0, N - 200); w = rng.uniform(1.5, 3)
        L = int(rng.uniform(60, 200))
        for t in range(L):
            xi = int(x + 4 * math.sin(t / 25)); yi = y + t
            h[yi, max(0, xi - int(w)):xi + int(w)] = np.maximum(h[yi, max(0, xi - int(w)):xi + int(w)], 0.5)
    Image.fromarray((h * 255).astype(np.uint8)).save(_path(name)); return _path(name)


def smoke(k):
    """smoke / steam puff, RGBA white with alpha, densest at the base, fading upward. 512 x 1024."""
    name = f"smoke_{k}"
    if _cached(name): return _path(name)
    W, H = 512, 1024
    n1 = _noise(H, W, 120, 40 + k, 5); n2 = _noise(H, W, 40, 60 + k, 4)
    yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    t = 1 - yy                         # 0 at the bottom, 1 at the top
    width = 0.12 + 0.30 * t ** 0.7
    sh = np.exp(-((xx - 0.5 - 0.08 * np.sin(t * 5 + k)) / width) ** 2 * 1.4)
    dens = sh * (0.25 + 0.75 * n1) * (0.6 + 0.4 * n2) * np.clip(1.25 - t, 0, 1) ** 1.2 * np.clip(t * 6, 0, 1)
    a = np.clip(dens * 1.5, 0, 1)
    out = np.dstack([np.ones_like(a) * 0.9, np.ones_like(a) * 0.9, np.ones_like(a), a])
    Image.fromarray((out * 255).astype(np.uint8), "RGBA").save(_path(name)); return _path(name)


def fire(k):
    """flame card, RGBA, emission colour in RGB. 256 x 512."""
    name = f"fire_{k}"
    if _cached(name): return _path(name)
    W, H = 256, 512
    n = _noise(H, W, 40, 90 + k, 4)
    yy, xx = np.mgrid[0:H, 0:W] / np.array([H, W])[:, None, None]
    t = 1 - yy
    width = 0.42 * (1 - t) ** 0.6 + 0.02
    core = np.exp(-((xx - 0.5 + 0.05 * np.sin(t * 9 + k)) / width) ** 2)
    f = np.clip(core * (0.5 + 0.8 * n) - t * 0.75, 0, 1)
    a = np.clip(f * 2.2, 0, 1)
    hot = np.clip(f * 2 - 0.3, 0, 1)
    rgb = np.dstack([np.ones_like(f), 0.45 + 0.5 * hot, 0.12 + 0.6 * hot ** 2])
    out = np.dstack([rgb, a])
    Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "RGBA").save(_path(name)); return _path(name)


def panel_lines(kind, seams_u, top_u, side_v, w=1024, h=512):
    """car panel-line map in loft UV space (u = 0 rear .. 1 front, v = 0..1 round the cross-section).
    seams_u: door/body shut lines (vertical on the sides), top_u: hood/boot shut lines across the top,
    side_v: (v_lo, v_hi) of each side of the body below the window line. Lines 3 texels, white on black."""
    name = f"panel_{kind}"
    if _cached(name): return _path(name)
    im = Image.new("L", (w, h), 0); d = ImageDraw.Draw(im)
    for (v0, v1) in side_v:
        for u in seams_u:
            d.line(((u * w, v0 * h), (u * w, v1 * h)), fill=255, width=3)
    for (u, va, vb) in top_u:
        d.line(((u * w, va * h), (u * w, vb * h)), fill=255, width=3)
    im.save(_path(name)); return _path(name)


def all_static():
    out = [sign_panel(k) for k in SIGNS] + [led_board(), livery(), delivery_box(), crack(), droplets(), city_ground()]
    out += [plate(i) for i in range(6)] + [tower_windows(k) for k in range(6)] + [smoke(k) for k in range(4)] + [fire(k) for k in range(2)]
    return out


if __name__ == "__main__":
    import time; t = time.time()
    for p in all_static(): print(p)
    print("%.1f s" % (time.time() - t))
