"""bc_face.py -- flat decal faces for the blocky cast, drawn by code with PIL (no bpy).

    path_col, path_emit = face_png(kind, expr="determined", mouth=None, blink=0, gaze=(0, 0))

The PNG covers exactly the FRONT face of the head cube (width w x height h of the cube, aspect kept); the head
shader maps it by object coordinates, so u = -1..1 is the character's RIGHT..LEFT (screen left..right from the
front) and v = -1..1 is chin..crown.  `mouth` = level 0..1 or (shape, level) with shape a / o / e, as the puppets.
`blink` 0 open, 1 half, 2 shut.  Zombie eyes are drawn white into the colour image AND into the emission mask
(_e.png, white = glow).  Files are cached by a hash of the drawing state in tex/faces/.
"""
import os, math, hashlib, json, random
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tex", "faces")
SS = 2                     # supersampling
W0 = 768                   # output width (px across the cube's front face)

INK = (14, 12, 12, 255)
INK_SOFT = (26, 20, 18, 255)

# face layouts in face units (u, v in -1..1).  Measured on the sheet fronts (proportions.md, "face" rows).
FACES = {
    "kong": dict(aspect=0.92, eye_u=0.40, eye_v=-0.06, eye_rx=0.095, eye_ry=0.145, brow_v=0.19, brow_in=0.14, brow_out=0.64,
                 brow_th=0.115, mouth_v=-0.46, mouth_w=0.27, stubble=True, scars=True, skin=(233, 164, 108), zombie=False),
    "crew": dict(aspect=0.92, eye_u=0.38, eye_v=-0.05, eye_rx=0.080, eye_ry=0.120, brow_v=0.17, brow_in=0.16, brow_out=0.60,
                 brow_th=0.070, mouth_v=-0.45, mouth_w=0.24, stubble=False, scars=False, skin=(236, 172, 120), zombie=False),
    "z_office": dict(aspect=0.92, eye_u=0.40, eye_v=0.10, eye_rx=0.170, eye_ry=0.125, brow_v=0.33, brow_in=0.10, brow_out=0.72,
                     brow_th=0.130, mouth_v=-0.47, mouth_w=0.46, stubble=False, scars=False, skin=(170, 172, 152), zombie=True),
}
FACES["z_rescue"] = dict(FACES["z_office"])

# expression -> (brow (inner dv, outer dv, tilt style), eyes, mouth default)
#   brows: inner / outer height offsets (face units); eyes: "oval" | "wide" | "narrow" | "shut" | "lid" (half lid) | "squeeze"
EXPR = {
    # Kong (sheet row: determined, angry, surprised, worried, sad, pain) + the hook's names mapped onto them
    "determined": dict(brow=(-0.07, 0.06), eyes="oval", mouth=("flat", -0.05)),
    "angry": dict(brow=(-0.12, 0.09), eyes="narrow", mouth=("shout", 0.85)),
    "surprised": dict(brow=(0.13, 0.12), eyes="wide", mouth=("o", 0.65), arch=True),
    "worried": dict(brow=(0.10, -0.06), eyes="oval", mouth=("flat", -0.10), wavy=True),
    "sad": dict(brow=(0.09, -0.08), eyes="lid", mouth=("flat", -0.22)),
    "pain": dict(brow=(-0.13, 0.08), eyes="squeeze", mouth=("grit", 0.6)),
    "neutral": dict(brow=(0.0, 0.0), eyes="oval", mouth=("flat", 0.0)),
    "serious": dict(brow=(-0.05, 0.04), eyes="oval", mouth=("flat", -0.03)),
    "guilty": dict(brow=(0.08, -0.05), eyes="oval", mouth=("flat", -0.12), gaze=(0.0, -0.35)),
    "tired": dict(brow=(0.05, -0.05), eyes="lid", mouth=("flat", -0.08)),
    "alarmed": dict(brow=(0.11, 0.10), eyes="wide", mouth=("o", 0.5), arch=True),
    "shouting": dict(brow=(-0.10, 0.08), eyes="oval", mouth=("shout", 0.9)),
    "scared": dict(brow=(0.12, -0.02), eyes="wide", mouth=("o", 0.75), arch=True),
    "joy": dict(brow=(0.04, 0.04), eyes="oval", mouth=("smile", 0.5)),
    "blink": dict(brow=(0.0, 0.0), eyes="shut", mouth=("flat", 0.0)),
    # zombie (sheet row: attack, scream, growl, detect, idle); roar = the sheet's scream
    "idle": dict(brow=(-0.08, 0.05), eyes="glow", mouth=("zopen", 0.55)),
    "roar": dict(brow=(-0.04, 0.10), eyes="glow", mouth=("zopen", 1.0)),
    "attack": dict(brow=(-0.12, 0.08), eyes="glow", mouth=("zopen", 0.80)),
    "growl": dict(brow=(-0.13, 0.06), eyes="glow_narrow", mouth=("zgrit", 0.5)),
    # the hook's driver names
    "still": dict(brow=(-0.02, 0.02), eyes="zshut", mouth=("zopen", 0.18)),
    "head_lift": dict(brow=(-0.10, 0.06), eyes="glow", mouth=("zopen", 0.45)),
    "lunge": dict(brow=(-0.12, 0.08), eyes="glow", mouth=("zopen", 0.85)),
    "bite": dict(brow=(-0.04, 0.10), eyes="glow", mouth=("zopen", 1.0)),
}
KONG_SHEET_ROW = ["determined", "angry", "surprised", "worried", "sad", "pain"]
ZOMBIE_SHEET_ROW = ["idle", "roar", "attack", "growl"]


class _C:
    """face-unit -> pixel mapping on the supersampled canvas."""

    def __init__(self, aspect):
        self.W = W0 * SS; self.H = int(round(W0 * aspect)) * SS

    def p(self, u, v):
        return ((u + 1) * 0.5 * self.W, (1 - v) * 0.5 * self.H)

    def s(self, du):                      # face units (u) -> px
        return du * 0.5 * self.W

    def sv(self, dv):
        return dv * 0.5 * self.H


def _poly_line(d, C, pts, col, w):
    P = [C.p(u, v) for u, v in pts]
    d.line(P, fill=col, width=max(1, int(C.s(w))), joint="curve")
    r = C.s(w) / 2
    for x, y in (P[0], P[-1]):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def _quad(p0, p1, p2, n=16):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in [i / float(n - 1) for i in range(n)]]


def _ell(d, C, u, v, rx, ry, fill, rot=0.0):
    if abs(rot) < 1e-3:
        x0, y0 = C.p(u - rx, v + ry); x1, y1 = C.p(u + rx, v - ry)
        d.ellipse([x0, y0, x1, y1], fill=fill)
        return
    pts = [(u + rx * math.cos(a) * math.cos(rot) - ry * math.sin(a) * math.sin(rot), v + rx * math.cos(a) * math.sin(rot) + ry * math.sin(a) * math.cos(rot))
           for a in [i * 2 * math.pi / 40 for i in range(40)]]
    d.polygon([C.p(*q) for q in pts], fill=fill)


def _brow(d, C, F, side, inner_dv, outer_dv, arch=False, wavy=False, zombie=False):
    """thick dark angled bar: side -1 = the character's right (screen left)."""
    ui, uo = side * F["brow_in"], side * F["brow_out"]
    vi, vo = F["brow_v"] + inner_dv, F["brow_v"] + outer_dv
    th = F["brow_th"]
    if arch:
        mid = (0.5 * (ui + uo), 0.5 * (vi + vo) + 0.06)
        pts = _quad((ui, vi), mid, (uo, vo))
    elif wavy:
        mid = (0.5 * (ui + uo), 0.5 * (vi + vo) - 0.015)
        pts = _quad((ui, vi), mid, (uo, vo))
    else:
        pts = [(ui, vi), (uo, vo)]
    # tapered bar: thick at the inner end
    n = 24
    if len(pts) == 2:
        pts = [(pts[0][0] + (pts[1][0] - pts[0][0]) * t / (n - 1), pts[0][1] + (pts[1][1] - pts[0][1]) * t / (n - 1)) for t in range(n)]
    top, bot = [], []
    for i, (u, v) in enumerate(pts):
        t = i / float(len(pts) - 1)
        w = th * (1.0 - 0.35 * t) * (1.15 if zombie else 1.0)
        top.append((u, v + w * 0.5)); bot.append((u, v - w * 0.5))
    poly = top + bot[::-1]
    d.polygon([C.p(*q) for q in poly], fill=INK)
    if zombie:                                      # deep brow ridge shadow under the bar
        sh = [(u, v - th * 0.5) for u, v in pts] + [(u, v - th * 1.15) for u, v in pts[::-1]]
        d.polygon([C.p(*q) for q in sh], fill=(40, 34, 30, 120))


def _eyes(d, de, C, F, kind, gaze, blink):
    gu, gv = gaze[0] * 0.07, gaze[1] * 0.05
    for side in (-1, 1):
        u, v = side * F["eye_u"] + gu, F["eye_v"] + gv
        rx, ry = F["eye_rx"], F["eye_ry"]
        if kind in ("glow", "glow_narrow"):
            u, v = side * F["eye_u"], F["eye_v"]
            if kind == "glow_narrow": ry *= 0.72
            if blink == 2:
                _poly_line(d, C, [(u - rx, v), (u + rx, v - 0.01)], INK, 0.03); continue
            if blink == 1: ry *= 0.5
            _ell(d, C, u, v - 0.01, rx * 1.28, ry * 1.45, (52, 40, 36, 230))          # dark socket
            _ell(d, C, u, v, rx, ry, (246, 248, 244, 255))
            _ell(de, C, u, v, rx * 0.98, ry * 0.98, 255)
            _ell(d, C, u - rx * 0.25, v + ry * 0.25, rx * 0.35, ry * 0.30, (255, 255, 255, 255))
            continue
        if kind == "zshut":                          # the driver before the reveal: dark lids, no glow
            u, v = side * F["eye_u"], F["eye_v"]
            _ell(d, C, u, v - 0.01, rx * 1.25, ry * 1.4, (60, 48, 44, 220))
            _poly_line(d, C, _quad((u - rx, v + 0.005), (u, v - ry * 0.6), (u + rx, v + 0.005)), INK, 0.028)
            continue
        if kind == "shut" or blink == 2:
            _poly_line(d, C, _quad((u - rx * 1.1, v), (u, v - ry * 0.5), (u + rx * 1.1, v)), INK, 0.032)
            continue
        if kind == "squeeze":                        # > <
            a = 1 if side < 0 else -1
            _poly_line(d, C, [(u - a * rx * 1.1, v + ry * 0.7), (u + a * rx * 0.9, v), (u - a * rx * 1.1, v - ry * 0.7)], INK, 0.035)
            continue
        if kind == "wide": rx, ry = rx * 1.12, ry * 1.12
        if kind == "narrow": ry *= 0.78
        if kind == "lid" or blink == 1:              # half lid: the top of the oval cut flat
            ry2 = ry * (0.55 if kind == "lid" else 0.45)
            _ell(d, C, u, v - ry * 0.35, rx, ry2, INK)
            _poly_line(d, C, [(u - rx * 1.2, v - ry * 0.35 + ry2 * 0.9), (u + rx * 1.2, v - ry * 0.35 + ry2 * 0.9)], INK, 0.028)
            continue
        _ell(d, C, u, v, rx, ry, INK)
        _ell(d, C, u - rx * 0.30, v + ry * 0.38, rx * 0.26, ry * 0.18, (235, 235, 235, 200))     # catch light


def _mouth(d, C, F, shape, level, zombie=False):
    mv, mw = F["mouth_v"], F["mouth_w"]
    lv = max(0.0, min(1.0, float(level)))
    if shape == "flat":                              # level = curvature (+ smile, - frown)
        c = level
        pts = _quad((-mw, mv - 0.25 * c * 0.3), (0, mv + c * 0.30), (mw, mv - 0.25 * c * 0.3))
        _poly_line(d, C, pts, INK, 0.045)
        return
    if shape == "smile":
        pts = _quad((-mw, mv + 0.05), (0, mv - 0.16 * lv), (mw, mv + 0.05))
        top = [(u, v + 0.005) for u, v in pts]
        d.polygon([C.p(*q) for q in pts + [(mw * 0.8, mv + 0.04), (-mw * 0.8, mv + 0.04)]], fill=(70, 18, 20, 255))
        _poly_line(d, C, pts, INK, 0.04); _poly_line(d, C, [(-mw, mv + 0.05), (mw, mv + 0.05)], INK, 0.04)
        return
    if shape in ("o",):
        rx = 0.07 + 0.08 * lv; ry = 0.05 + 0.17 * lv
        _ell(d, C, 0, mv, rx + 0.025, ry + 0.025, INK)
        _ell(d, C, 0, mv, rx, ry, (92, 22, 24, 255))
        _ell(d, C, 0, mv - ry * 0.45, rx * 0.65, ry * 0.42, (178, 70, 72, 255))
        return
    if shape == "grit":                              # clenched teeth (pain)
        w, h = mw * 1.05, 0.10 + 0.08 * lv
        x0, y0 = C.p(-w, mv + h); x1, y1 = C.p(w, mv - h)
        d.rounded_rectangle([x0, y0, x1, y1], radius=C.s(0.04), fill=INK)
        ix0, iy0 = C.p(-w + 0.03, mv + h - 0.03); ix1, iy1 = C.p(w - 0.03, mv - h + 0.03)
        d.rounded_rectangle([ix0, iy0, ix1, iy1], radius=C.s(0.025), fill=(244, 240, 228, 255))
        _poly_line(d, C, [(-w + 0.03, mv), (w - 0.03, mv)], INK, 0.018)
        for k in range(1, 7):
            u = -w + 2 * w * k / 7.0
            _poly_line(d, C, [(u, mv + h - 0.03), (u, mv - h + 0.03)], INK, 0.012)
        return
    if shape in ("zopen", "zgrit"):
        _zmouth(d, C, F, shape, lv); return
    # "a" / "e" / "shout": an open mouth whose upper lip arches (corners lower than the middle), so an open mouth
    # never reads as a grin; "shout" is wider and taller, "e" wide and low
    if shape == "e": w = mw * 0.95; h = 0.04 + 0.14 * lv; arch = 0.03
    elif shape == "shout": w = mw * (0.85 + 0.12 * lv); h = 0.10 + 0.22 * lv; arch = 0.10
    else: w = mw * (0.42 + 0.20 * lv); h = 0.035 + 0.21 * lv; arch = 0.03 + 0.05 * lv
    if lv <= 0.01:
        _poly_line(d, C, [(-mw * 0.8, mv), (mw * 0.8, mv)], INK, 0.045); return
    top = mv + 0.02
    n = 14
    upper = [(-w + 2 * w * i / (n - 1), top + arch * math.sin(math.pi * i / (n - 1)) - arch * 0.5) for i in range(n)]
    lower = [(w * math.cos(a), top - arch * 0.5 - h * (0.45 + 0.55 * max(0.0, math.sin(a)) ** 0.6)) for a in [i * math.pi / (n - 1) for i in range(n)]]
    lower = [(u * (0.80 if shape == "shout" else 0.92), v) for u, v in lower]
    outline = upper + lower
    pad = [(u * 1.10, mv + (v - mv) * 1.10 + 0.004) for u, v in outline]
    d.polygon([C.p(*q) for q in pad], fill=INK)
    d.polygon([C.p(*q) for q in outline], fill=(62, 14, 16, 255))
    if lv >= 0.45 or shape in ("e", "shout"):        # upper teeth under the arch
        tb = min(0.07, h * 0.28)
        tpts = [(u * 0.9, v - 0.004) for u, v in upper] + [(u * 0.84, v - tb) for u, v in upper[::-1]]
        d.polygon([C.p(*q) for q in tpts], fill=(238, 232, 220, 255))
    if lv >= 0.3:                                    # tongue
        _ell(d, C, 0, top - h * 0.95, w * 0.50, h * 0.24, (168, 58, 62, 255))


def _zmouth(d, C, F, shape, lv):
    """the zombie snarl: dark wet interior, yellow irregular teeth top and bottom, blood at the lips."""
    mv, mw = F["mouth_v"], F["mouth_w"]
    rnd = random.Random(7)
    if shape == "zgrit":
        w, h = mw * 1.05, 0.12 + 0.06 * lv
    else:
        w = mw * (0.70 + 0.32 * lv); h = 0.07 + 0.36 * lv
    top = mv + h * 0.45; bot = mv - h * 0.55
    # jagged lip outline
    outline = []
    for i in range(21):
        t = i / 20.0; u = -w + 2 * w * t
        outline.append((u, top - 0.02 * math.sin(t * math.pi) + 0.012 * (rnd.random() - 0.5)))
    for i in range(21):
        t = i / 20.0; u = w - 2 * w * t
        outline.append((u, bot + (0.06 if shape == "zopen" else 0.02) * math.sin(t * math.pi) * (1 if shape == "zgrit" else -1) + 0.012 * (rnd.random() - 0.5)))
    pad = [(u * 1.10, mv + (v - mv) * 1.16) for u, v in outline]
    d.polygon([C.p(*q) for q in pad], fill=(30, 10, 10, 255))
    d.polygon([C.p(*q) for q in outline], fill=(48, 6, 8, 255))
    # teeth
    nT = 8 if shape == "zgrit" else 7
    th = min(0.09, h * (0.45 if shape == "zgrit" else 0.24))
    for row, (y0, sgn) in enumerate(((top - 0.01, -1), (bot + 0.012 + (0.03 if shape == "zopen" else 0.0), 1))):
        for k in range(nT):
            u0 = -w * 0.86 + (2 * w * 0.86) * k / nT
            u1 = u0 + 2 * w * 0.86 / nT * 0.86
            ln = th * (0.65 + 0.5 * rnd.random())
            if shape == "zopen" and k in (0, nT - 1): ln *= 1.5          # fangs at the corners
            col = (206 + rnd.randint(-14, 10), 176 + rnd.randint(-16, 10), 96 + rnd.randint(-20, 14), 255)
            pts = [(u0, y0), (u1, y0), (u1 - 0.006, y0 + sgn * ln), ((u0 + u1) / 2, y0 + sgn * ln * 1.12), (u0 + 0.006, y0 + sgn * ln)]
            d.polygon([C.p(*q) for q in pts], fill=col)
            d.line([C.p(u1, y0), C.p(u1 - 0.006, y0 + sgn * ln)], fill=(120, 90, 50, 255), width=max(1, int(C.s(0.008))))
    if shape == "zgrit":
        _poly_line(d, C, [(-w * 0.9, mv), (w * 0.9, mv)], (40, 8, 8, 255), 0.012)


def _stubble(d, C, F, seed=3):
    rnd = random.Random(seed)
    n = 0
    while n < 150:
        u = rnd.uniform(-0.88, 0.88); v = rnd.uniform(-0.98, -0.22)
        if v > -0.62 + 0.45 * (abs(u) - 0.35) / 0.55 and abs(u) > 0.35: continue    # jaw band: low under the mouth, rising toward the cheek edges
        if abs(u) <= 0.35 and v > -0.56: continue                   # not on the upper lip
        dm = ((u / (F["mouth_w"] + 0.06)) ** 2 + ((v - F["mouth_v"]) / 0.10) ** 2)
        if dm < 1.0: continue
        r = rnd.uniform(0.007, 0.013)
        a = rnd.randint(60, 130)
        _ell(d, C, u, v, r, r * 1.1, (48, 30, 22, a))
        n += 1


def _scars(d, C, F):
    red = (176, 30, 26, 235); dk = (120, 16, 14, 255)
    # an X on the character's right cheek (screen left) and a short slash below it
    cu, cv = -0.60, -0.16
    _poly_line(d, C, [(cu - 0.09, cv + 0.08), (cu + 0.08, cv - 0.08)], red, 0.026)
    _poly_line(d, C, [(cu - 0.07, cv - 0.08), (cu + 0.07, cv + 0.07)], red, 0.022)
    _poly_line(d, C, [(-0.50, -0.38), (-0.40, -0.26)], dk, 0.022)
    _poly_line(d, C, [(-0.47, -0.42), (-0.39, -0.32)], red, 0.014)


def _zblood(d, C, F, shape, lv):
    """blood from the mouth corners down the chin, a streak from the right eye, a smear on the brow."""
    rnd = random.Random(11)
    bl = (122, 10, 12, 225); bd = (80, 4, 6, 240)
    mv, mw = F["mouth_v"], F["mouth_w"]
    w = mw * (0.70 + 0.32 * lv)
    for sx, ln in ((-1, 0.55), (1, 0.42), (-0.4, 0.30), (0.5, 0.36)):
        u0 = sx * w * 0.9 if abs(sx) == 1 else sx * w
        v0 = mv - 0.05 - 0.15 * lv
        pts = [(u0, v0)]
        u, v = u0, v0
        for k in range(10):
            v -= ln / 10.0; u += 0.006 * (rnd.random() - 0.5)
            pts.append((u, v))
        for i, (a, b) in enumerate(zip(pts[:-1], pts[1:])):
            wdt = 0.035 * (1 - i / 12.0)
            _poly_line(d, C, [a, b], bl, wdt)
        _ell(d, C, pts[-1][0], pts[-1][1], 0.022, 0.03, bd)
    # eye streak (character's right eye = screen left)
    u0, v0 = -F["eye_u"] - 0.06, F["eye_v"] - F["eye_ry"] - 0.02
    _poly_line(d, C, [(u0, v0), (u0 - 0.02, v0 - 0.25), (u0 - 0.015, v0 - 0.48)], (130, 14, 14, 190), 0.03)
    # smears
    for k in range(18):
        u = rnd.uniform(-0.8, 0.8); v = rnd.uniform(-0.95, 0.75)
        if abs(v - F["eye_v"]) < 0.14 and abs(abs(u) - F["eye_u"]) < 0.2: continue
        r = rnd.uniform(0.01, 0.05)
        _ell(d, C, u, v, r, r * rnd.uniform(0.6, 1.4), (110, 14, 14, rnd.randint(80, 170)))


def _zveins(d, C, F):
    rnd = random.Random(5)
    for k in range(9):
        u = rnd.choice((-1, 1)) * rnd.uniform(0.55, 0.85); v = rnd.uniform(-0.6, 0.5)
        pts = [(u, v)]
        for i in range(5):
            u += rnd.uniform(-0.05, 0.05); v += rnd.uniform(-0.07, 0.07); pts.append((u, v))
        _poly_line(d, C, pts, (78, 84, 70, 90), 0.010)
    for k in range(60):                                   # grime freckles
        u = rnd.uniform(-0.9, 0.9); v = rnd.uniform(-0.95, 0.9)
        r = rnd.uniform(0.005, 0.02)
        _ell(d, C, u, v, r, r, (64, 58, 48, rnd.randint(40, 110)))


def norm_mouth(m):
    """the puppets' mouth key -> (shape, level) or None."""
    if m is None: return None
    if isinstance(m, (tuple, list)): return (str(m[0]), round(float(m[1]) * 4) / 4.0)
    return ("a", round(float(m) * 4) / 4.0)


def face_png(kind, expr="determined", mouth=None, blink=0, gaze=(0.0, 0.0), scars=None):
    F = FACES[kind]
    E = EXPR.get(expr) or EXPR["neutral" if not F["zombie"] else "idle"]
    if F["zombie"] and expr in EXPR and EXPR[expr]["eyes"] not in ("glow", "glow_narrow", "zshut"):
        E = dict(E, eyes="glow")
    gz = E.get("gaze", (0, 0)) if gaze in (None, (0, 0), (0.0, 0.0)) else gaze
    gz = (round(gz[0] * 10) / 10.0, round(gz[1] * 10) / 10.0)
    m = norm_mouth(mouth)
    ms, ml = E["mouth"]
    if m is not None:
        shp, lv = m
        if F["zombie"]:
            ms, ml = ("zopen", max(lv, 0.15))
        elif lv > 0:
            ms, ml = (shp if shp in ("a", "o", "e") else "a", lv)
    blink = int(blink or 0)
    key = json.dumps([kind, expr, ms, ml, blink, gz, E["brow"], E["eyes"], scars, 8], sort_keys=True)
    h = hashlib.sha1(key.encode()).hexdigest()[:16]
    os.makedirs(OUT, exist_ok=True)
    pc, pe = os.path.join(OUT, "%s_%s.png" % (kind, h)), os.path.join(OUT, "%s_%s_e.png" % (kind, h))
    if os.path.exists(pc) and os.path.exists(pe):
        return pc, pe
    C = _C(F["aspect"])
    im = Image.new("RGBA", (C.W, C.H), (0, 0, 0, 0))
    em = Image.new("L", (C.W, C.H), 0)
    d = ImageDraw.Draw(im, "RGBA"); de = ImageDraw.Draw(em)
    if F["zombie"]:
        _zveins(d, C, F)
    if F.get("stubble"):
        _stubble(d, C, F)
    if F.get("scars") if scars is None else scars:
        _scars(d, C, F)
    if F["zombie"]:
        _zblood(d, C, F, ms, ml)
    _brow(d, C, F, -1, *E["brow"], arch=E.get("arch", False), wavy=E.get("wavy", False), zombie=F["zombie"])
    _brow(d, C, F, 1, *E["brow"], arch=E.get("arch", False), wavy=E.get("wavy", False), zombie=F["zombie"])
    _eyes(d, de, C, F, E["eyes"], gz, blink)
    _mouth(d, C, F, ms, ml, F["zombie"])
    im = im.resize((C.W // SS, C.H // SS), Image.LANCZOS)
    em = em.filter(ImageFilter.GaussianBlur(SS * 1.5)).resize((C.W // SS, C.H // SS), Image.LANCZOS)
    tmp = pc + ".tmp.png"; im.save(tmp); os.replace(tmp, pc)
    tmp = pe + ".tmp.png"; em.save(tmp); os.replace(tmp, pe)
    return pc, pe


def preview(path, kinds=("kong", "z_office")):
    """flat preview of every expression and the 5 lip-sync levels on the skin colour (no 3D)."""
    rows = []
    for k in kinds:
        F = FACES[k]
        names = KONG_SHEET_ROW + ["neutral", "guilty"] if not F["zombie"] else ZOMBIE_SHEET_ROW + ["still", "head_lift"]
        cells = []
        for e in names:
            cells.append(face_png(k, e))
        base = "serious" if not F["zombie"] else "idle"
        for lv in (0, 0.25, 0.5, 0.75, 1.0):
            cells.append(face_png(k, base, mouth=lv))
        if not F["zombie"]:
            cells.append(face_png(k, base, mouth=("o", 0.75))); cells.append(face_png(k, base, blink=2))
        rows.append((F, cells))
    cw = 256; ch = int(cw * 0.92)
    out = Image.new("RGB", (cw * max(len(c) for _, c in rows), ch * len(rows)), (240, 236, 228))
    for r, (F, cells) in enumerate(rows):
        for i, (pc, pe) in enumerate(cells):
            bg = Image.new("RGBA", (cw, ch), F["skin"] + (255,))
            fc = Image.open(pc).resize((cw, ch), Image.LANCZOS)
            bg.alpha_composite(fc)
            out.paste(bg.convert("RGB"), (i * cw, r * ch))
    out.save(path)


if __name__ == "__main__":
    preview(os.path.join(HERE, "out", "faces_flat.png"))
