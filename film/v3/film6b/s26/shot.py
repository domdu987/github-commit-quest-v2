#!/usr/bin/env python3
"""shot.py -- film 6b take s26: shots 26-28 (48.60-56.80 s = g 1458..1703) + 6-frame handles (g 1452..1709).

    DIAGRAM (internal shot 26, g 1452..1592): a clean cool-blue blueprint backdrop inside Blender, every piece an emission card.
      A 2D cutaway loaf (sliced: brown crust ring, cream crumb with air holes) sits on the left pan of a 2D diagram balance.
      Tiny blue water drops sit in the crumb, leave it through the crust and rise; above the loaf each drop turns into a
      white steam puff (the "smoke" of the morning).
        26a g 1452..1485  loaf + rising puffs, slow push; "ควัน" label stamped with a red X on "ไม่ใช่ควัน" (g 1461)
        26b g 1486..1530  punch-in on the crumb: the drops pulse, label "น้ำ" points into the crumb on "มันคือน้ำใน" (g 1488)
        26c g 1531..1553  the drops race out of the crust and tilt up with them into the steam: label "ไอน้ำ" ("ระเหยหนีไป" g 1532)
        27  g 1554..1592  pull back: the whole balance; drops keep escaping (no new ones), the crumb dries paler, the loaf shrinks,
                          the loaf pan RISES (beam 0 -> +9 deg loaf side up), the tag flips "500 ก." -> "480 ก." on "ก็ยิ่งเบา" (g 1574)
    BAKERY (internal shot 28, g 1593..1709), MORNING, the hand balance on the counter:
        28a g 1593..1648  ECU of the loaf pan holding a little basket of 12 (beam +7 = loaf side up: light); the pale 13th loaf
                          drops in on "ก้อนที่สิบสาม" (lands g 1606), the beam swings level, a "+1" badge pops (g 1610)
        28b g 1649..1709  wider on the whole balance, level, the "+1" badge; little blue drops keep rising off the basket into
                          the steam: "ชดเชยน้ำหนัก ที่หายไปกับไอน้ำ"
No people in this take (mouth rule trivially kept).  NO depth of field anywhere (client rule).  Thai labels: Kanit Black via
PIL + raqm (correct Thai shaping), ink outline.

    python3 shot.py probe 26|28 a:b[:step]
    python3 shot.py stills 26|28 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 26|28 a:b[:step] [scale] [samples]          (26 and 28 need separate processes: two scenes)
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
sys.path.insert(0, FILM6)
import common as C                                       # noqa: E402  (paths, cast6 first, bpy, bakery, stage)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageFilter  # noqa: E402

B, actors, camrig, cast6, render = C.B, C.actors, C.camrig, C.cast6, C.render
lerp, clamp, ez = C.lerp, C.clamp, C.ez
TMP = os.path.join(HERE, "work")
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
INK = "#3a2832"


# ----------------------------------------------------------------------------- film 6b clock
def g_of(t):
    return int(round((t + 0.10) * 30))


def g_bound(t):
    return int(round(t * 30))


G0, G1 = g_bound(48.60), g_bound(56.80)           # 1458, 1704
G27, G28 = g_bound(51.80), g_bound(53.11)         # 1554, 1593
H = 6
RANGES = {26: (G0 - H, G28 - 1), 28: (G28, G1 - 1 + H)}
CUT_B, CUT_C = 1486, 1531                         # 26a | 26b | 26c
CUT_28B = 1649
EV = dict(not_smoke=g_of(48.6), water=g_of(49.49), evap=g_of(50.96), afternoon=g_of(51.77), lighter=g_of(52.37),
          thirteenth=g_of(53.08), compensate=g_of(54.53), steam=g_of(56.33))


def bf(shot, g):
    return int(g) - 1400 + (0 if shot == 26 else 1000)


def framing(shot, g):
    if shot == 26:
        if g < CUT_B:
            return "26a"
        if g < CUT_C:
            return "26b"
        if g < G27:
            return "26c"
        return "27"
    return "28a" if g < CUT_28B else "28b"


# ----------------------------------------------------------------------------- 2D pieces (SVG in D units, rasterised by Chromium)
def loaf_cut_svg(k):
    """the sliced loaf, base line y = 0 (origin = centre of the base), width 2.4, top y -1.0.  k 0 moist, 1, 2 dried paler."""
    crust = ["#b0602a", "#bb6c33", "#c67a3f"][k]
    crust_hi = ["#d88c48", "#e09a58", "#e8a868"][k]
    crumb = ["#f3d79c", "#f7e3b6", "#fbefd2"][k]
    hole = ["#dcb874", "#e6c995", "#efdcb6"][k]
    outer = "M -1.17 0.0 C -1.30 -0.55, -0.72 -1.0, 0 -1.0 C 0.72 -1.0, 1.30 -0.55, 1.17 0.0 Q 0 0.10 -1.17 0.0 Z"
    inner = "M -1.0 -0.07 C -1.10 -0.52, -0.62 -0.86, 0 -0.86 C 0.62 -0.86, 1.10 -0.52, 1.0 -0.07 Q 0 0.0 -1.0 -0.07 Z"
    rnd = random.Random(7)
    holes = []
    for i in range(30):
        x = rnd.uniform(-0.85, 0.85)
        ymax = 0.72 * math.sqrt(max(0.0, 1 - (x / 0.98) ** 2))
        y = -rnd.uniform(0.12, max(0.15, ymax - 0.06))
        rx = rnd.uniform(0.025, 0.07)
        holes.append('<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="%s" transform="rotate(%d %.3f %.3f)"/>'
                     % (x, y, rx, rx * rnd.uniform(0.55, 0.9), hole, rnd.randint(-30, 30), x, y))
    scores = "".join('<path d="M %.2f %.2f q 0.10 -0.05 0.20 0" stroke="%s" stroke-width="0.035" fill="none" stroke-linecap="round"/>'
                     % (x, -0.93 + abs(x) * 0.12, crust_hi, ) for x in (-0.5, -0.15, 0.2))
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.06" stroke-linejoin="round"/>'
            '<path d="M -0.95 -0.55 C -0.80 -0.85, -0.40 -0.95, -0.05 -0.96" stroke="%s" stroke-width="0.05" fill="none" stroke-linecap="round" opacity="0.8"/>'
            '%s<path d="%s" fill="%s" stroke="%s" stroke-width="0.025"/>%s'
            % (outer, crust, INK, crust_hi, scores, inner, crumb, "#a8703a", "".join(holes)))


LOAF_BOX = (-1.32, -1.08, 1.32, 0.14)


def drop_svg(k):
    """a water drop pointing up: pale-blue body, white glint, plum ink outline.  Box (-0.5,-0.75,0.5,0.55)."""
    sq = [1.0, 0.92, 1.08][k]
    w = 0.36 * sq
    path = ("M 0 -0.62 C %.3f -0.36, %.3f -0.12, %.3f 0.10 A %.3f %.3f 0 1 1 %.3f 0.10 C %.3f -0.12, %.3f -0.36, 0 -0.62 Z"
            % (0.12 * sq, w, w, w, w, -w, -w, -0.12 * sq))
    return ('<defs><radialGradient id="dg%d" cx="0.38" cy="0.35" r="0.75"><stop offset="0" stop-color="#e6f7ff"/>'
            '<stop offset="0.45" stop-color="#5cc0ff"/><stop offset="1" stop-color="#1f74d6"/></radialGradient></defs>'
            '<path d="%s" fill="url(#dg%d)" stroke="%s" stroke-width="0.085" stroke-linejoin="round"/>'
            '<ellipse cx="%.3f" cy="0.02" rx="0.07" ry="0.13" fill="#ffffff" transform="rotate(18 %.3f 0.02)"/>'
            '<circle cx="%.3f" cy="-0.16" r="0.035" fill="#ffffff"/>'
            % (k, path, k, INK, -0.14 * sq, -0.14 * sq, -0.06 * sq))


DROP_BOX = (-0.5, -0.75, 0.5, 0.55)


def puff_svg(k):
    """a white steam puff (union of circles: a pale-blue rim drawn under the white fills).  Box (-0.62,-0.55,0.62,0.45)."""
    rnd = random.Random(40 + k)
    cs = [(0.0, 0.0, 0.30)] + [(rnd.uniform(-0.32, 0.32), rnd.uniform(-0.22, 0.14), rnd.uniform(0.16, 0.24)) for _ in range(5)]
    rim = "".join('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#b8dcf6" stroke="#8fbfe6" stroke-width="0.05"/>' % c for c in cs)
    fill = "".join('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#ffffff"/>' % (x, y, r - 0.035) for x, y, r in cs)
    shine = '<circle cx="-0.10" cy="-0.12" r="0.08" fill="#f2fbff"/>'
    return rim + fill + shine


PUFF_BOX = (-0.62, -0.55, 0.62, 0.45)


def post_svg():
    """balance post: pivot (0, 0) down to a stepped base at y 3.95.  Box (-1.1,-0.25,1.1,4.1)."""
    return ('<rect x="-0.09" y="0" width="0.18" height="3.75" fill="#e6b445" stroke="%s" stroke-width="0.05"/>'
            '<rect x="-0.05" y="0.1" width="0.04" height="3.5" fill="#fbe39a"/>'
            '<path d="M -0.55 3.62 L 0.55 3.62 L 0.70 3.80 L -0.70 3.80 Z" fill="#b8823a" stroke="%s" stroke-width="0.05" stroke-linejoin="round"/>'
            '<rect x="-1.0" y="3.80" width="2.0" height="0.22" rx="0.06" fill="#8a5a2c" stroke="%s" stroke-width="0.05"/>'
            '<path d="M -1.6 -1.05 A 1.6 1.6 0 0 1 1.6 -1.05" fill="none"/>' % (INK, INK, INK))


POST_BOX = (-1.1, -0.25, 1.1, 4.1)


def dial_svg():
    """the arc scale behind the pointer (pivot at (0,0)), ticks every 5 deg, centre tick long.  Box (-0.75,-1.35,0.75,-0.55)."""
    o = ['<path d="M -0.55 -0.98 A 1.12 1.12 0 0 1 0.55 -0.98" stroke="%s" stroke-width="0.16" fill="none" stroke-linecap="round"/>' % INK,
         '<path d="M -0.55 -0.98 A 1.12 1.12 0 0 1 0.55 -0.98" stroke="#fff6dc" stroke-width="0.09" fill="none" stroke-linecap="round"/>']
    for d in range(-25, 30, 5):
        a = math.radians(d)
        r0, r1 = (1.0, 1.28) if d == 0 else (1.05, 1.20)
        o.append('<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="%s" stroke-width="%.3f" stroke-linecap="round"/>'
                 % (r0 * math.sin(a), -r0 * math.cos(a), r1 * math.sin(a), -r1 * math.cos(a), "#d23a2a" if d == 0 else INK,
                    0.05 if d == 0 else 0.03))
    return "".join(o)


DIAL_BOX = (-0.75, -1.38, 0.75, -0.55)


def beam_svg():
    """beam: length 4.6 (ends +-2.3, hooks), pivot knob, pointer up 1.05 (rotates with the beam).  Box (-2.5,-1.2,2.5,0.3)."""
    return ('<path d="M 0 -1.02 L 0.05 -0.1 L -0.05 -0.1 Z" fill="#d23a2a" stroke="%s" stroke-width="0.03" stroke-linejoin="round"/>'
            '<path d="M -2.30 -0.07 L 2.30 -0.07 L 2.18 0.09 L -2.18 0.09 Z" fill="#e6b445" stroke="%s" stroke-width="0.05" stroke-linejoin="round"/>'
            '<line x1="-2.1" y1="-0.03" x2="2.1" y2="-0.03" stroke="#fbe39a" stroke-width="0.035"/>'
            '<circle cx="-2.3" cy="0" r="0.10" fill="#e6b445" stroke="%s" stroke-width="0.045"/>'
            '<circle cx="2.3" cy="0" r="0.10" fill="#e6b445" stroke="%s" stroke-width="0.045"/>'
            '<circle cx="0" cy="0" r="0.17" fill="#c98f2e" stroke="%s" stroke-width="0.05"/>'
            '<circle cx="0" cy="0" r="0.06" fill="%s"/>' % (INK, INK, INK, INK, INK, INK))


BEAM_BOX = (-2.5, -1.2, 2.5, 0.3)


def pan_svg():
    """a pan hanging from its hook (0, 0): three cords down to a dish whose top is at y 1.55.  Box (-1.2,-0.1,1.2,1.85)."""
    return ('<g stroke="%s" stroke-width="0.035" stroke-linecap="round"><line x1="0" y1="0" x2="-1.0" y2="1.53"/>'
            '<line x1="0" y1="0" x2="1.0" y2="1.53"/><line x1="0" y1="0" x2="0" y2="1.53"/></g>'
            '<path d="M -1.10 1.52 L 1.10 1.52 Q 0.95 1.80 0 1.80 Q -0.95 1.80 -1.10 1.52 Z" fill="#e6b445" stroke="%s" '
            'stroke-width="0.05" stroke-linejoin="round"/><path d="M -0.8 1.62 Q 0 1.70 0.8 1.62" stroke="#fbe39a" stroke-width="0.04" fill="none"/>'
            '<circle cx="0" cy="0" r="0.06" fill="%s"/>' % (INK, INK, INK))


PAN_BOX = (-1.2, -0.1, 1.2, 1.85)


def weights_svg():
    """brass weights stacked on the right pan: base line y 0.  Box (-0.9,-1.05,0.9,0.05)."""
    return ('<path d="M -0.75 0 L 0.75 0 L 0.62 -0.45 L -0.62 -0.45 Z" fill="#c98f2e" stroke="%s" stroke-width="0.05" stroke-linejoin="round"/>'
            '<path d="M -0.45 -0.45 L 0.45 -0.45 L 0.36 -0.78 L -0.36 -0.78 Z" fill="#e6b445" stroke="%s" stroke-width="0.05" stroke-linejoin="round"/>'
            '<rect x="-0.10" y="-0.95" width="0.20" height="0.17" rx="0.05" fill="#c98f2e" stroke="%s" stroke-width="0.04"/>'
            '<path d="M -0.55 -0.10 L -0.45 -0.38" stroke="#fbe39a" stroke-width="0.05" stroke-linecap="round"/>' % (INK, INK, INK))


WEIGHTS_BOX = (-0.9, -1.05, 0.9, 0.05)


# ----------------------------------------------------------------------------- Thai labels (PIL + raqm), cached
def _font(px):
    return ImageFont.truetype(FONT, px, layout_engine=ImageFont.Layout.RAQM)


def label_png(name, text, bg="#ffffff", fg=INK, px=110, pad=(34, 18), stroke=7, pointer=None, cross=False, out=None, tag=False,
              radius=34):
    """a rounded label card with a Thai word (ink outline).  pointer: None | 'bl' | 'br' | 'b' (a little speech-box tail).
    cross: a red X stamped over the word.  tag: a paper luggage tag with a hole.  Returns (png path, w px, h px)."""
    out = out or os.path.join(TMP, "labels")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "%s.png" % name)
    f = _font(px)
    l, t, r, b = f.getbbox(text)
    tw, th = r - l, b - t
    tail = 46 if pointer else 0
    hole = 60 if tag else 0
    W, Hh = tw + 2 * pad[0] + 2 * stroke + 16 + hole, th + 2 * pad[1] + 2 * stroke + 16 + tail
    im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = 8, 8, W - 8, Hh - 8 - tail
    d.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=bg, outline=INK, width=10)
    if pointer:
        cx = {"bl": x0 + 70, "br": x1 - 70, "b": (x0 + x1) // 2}[pointer]
        d.polygon([(cx - 30, y1 - 6), (cx + 30, y1 - 6), (cx + (-24 if pointer == "bl" else 24 if pointer == "br" else 0), y1 + tail)],
                  fill=bg, outline=INK)
        d.line([(cx - 30, y1 - 4), (cx + (-24 if pointer == "bl" else 24 if pointer == "br" else 0), y1 + tail),
                (cx + 30, y1 - 4)], fill=INK, width=10, joint="curve")
        d.line([(cx - 24, y1 - 5), (cx + 24, y1 - 5)], fill=bg, width=10)
    if tag:
        d.ellipse((x0 + 22, (y0 + y1) // 2 - 16, x0 + 54, (y0 + y1) // 2 + 16), fill=(0, 0, 0, 0), outline=INK, width=8)
    # text: outline layer (closed to fill the small glyph counters), then the fill
    tx, ty = x0 + pad[0] + stroke + hole - l, y0 + pad[1] + stroke - t
    m = Image.new("L", (W, Hh), 0)
    ImageDraw.Draw(m).text((tx, ty), text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    ink = Image.new("RGBA", (W, Hh), INK)
    im.paste(ink, (0, 0), m)
    ImageDraw.Draw(im).text((tx, ty), text, font=f, fill=fg)
    if cross:
        c = (214, 44, 36, 255)
        for (a, b2) in (((x0 + 18, y0 + 10), (x1 - 18, y1 - 10)), ((x0 + 18, y1 - 10), (x1 - 18, y0 + 10))):
            d2 = ImageDraw.Draw(im)
            d2.line([a, b2], fill=INK, width=24)
            d2.line([a, b2], fill=c, width=13)
    im.save(path)
    return path, W, Hh


def badge_png(name, text, out=None, px=150):
    """a round yellow burst badge with text (e.g. "+1")."""
    out = out or os.path.join(TMP, "labels")
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "%s.png" % name)
    S = 360
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(32):
        a = 2 * math.pi * i / 32
        r = 168 if i % 2 == 0 else 138
        pts.append((S / 2 + r * math.cos(a), S / 2 + r * math.sin(a)))
    d.polygon(pts, fill="#ffd23c", outline=INK)
    d.line(pts + [pts[0]], fill=INK, width=10, joint="curve")
    f = _font(px)
    l, t, r, b = f.getbbox(text)
    tx, ty = S / 2 - (r + l) / 2, S / 2 - (b + t) / 2 - 6
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).text((tx, ty), text, font=f, fill=255, stroke_width=9, stroke_fill=255)
    im.paste(Image.new("RGBA", (S, S), INK), (0, 0), m)
    ImageDraw.Draw(im).text((tx, ty), text, font=f, fill="#d8322a")
    im.save(path)
    return path, S, S


def backdrop_png():
    """the cool-blue blueprint backdrop (radial gradient, faint grid, a few + marks)."""
    path = os.path.join(TMP, "labels", "backdrop.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return path
    import numpy as np
    W, Hh = 1400, 2400
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W * 0.5) / (W * 0.62)) ** 2 + ((yy - Hh * 0.45) / (Hh * 0.55)) ** 2)
    r = np.clip(r, 0, 1.4) / 1.4
    c0, c1 = np.array([74, 150, 226], np.float32), np.array([20, 52, 118], np.float32)
    img = c0[None, None, :] * (1 - r[..., None] ** 1.3) + c1[None, None, :] * (r[..., None] ** 1.3)
    grid = ((xx % 70) < 3) | ((yy % 70) < 3)
    img[grid] = img[grid] * 0.8 + np.array([150, 200, 250], np.float32) * 0.2
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(im)
    rnd = random.Random(3)
    for _ in range(40):
        x, y = rnd.randrange(60, W - 60), rnd.randrange(60, Hh - 60)
        d.line([(x - 12, y), (x + 12, y)], fill=(170, 215, 250), width=4)
        d.line([(x, y - 12), (x, y + 12)], fill=(170, 215, 250), width=4)
    im.save(path)
    return path


def png_card(name, path, ppd, shadow=False, anchor="c"):
    """a PropCard from a PIL PNG; ppd = px per D; anchor 'c' (centre) or 'b' (bottom centre) at the card origin."""
    w, h = Image.open(path).size
    hw, hh = w / 2.0 / ppd, h / float(ppd)
    box = (-hw, -hh / 2, hw, hh / 2) if anchor == "c" else (-hw, -hh, hw, 0.0)
    return C.PropCard(name, [path], box, scale=1.0, shadow=shadow)


# ----------------------------------------------------------------------------- per-frame helpers for cards
def _key_card(pc, f, loc, s, on, rot_y=None):
    ob_list = pc.cards
    pc.root.location = Vector(loc)
    pc.root.scale = (max(s, 0.0001),) * 3
    if rot_y is not None:
        pc.root.rotation_euler = (0.0, rot_y, 0.0)
        pc.root.keyframe_insert("rotation_euler", frame=f)
    pc.root.keyframe_insert("location", frame=f)
    pc.root.keyframe_insert("scale", frame=f)
    for ob in ob_list:
        ob.keyframe_insert("hide_render", frame=f)


def _show(pc, i, f):
    """variant i visible (None hides), keyed constant."""
    for k, ob in enumerate(pc.cards):
        ob.hide_render = (i is None) or (k != i)


def _constant(pcs):
    for pc in pcs:
        for ob in pc.cards:
            fc = C._fcurve(ob, "hide_render")
            if fc is not None:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"


def pop(g, g0, dur=5, over=1.18):
    """pop-in scale: 0 -> over -> 1."""
    if g < g0:
        return 0.0
    u = (g - g0) / float(dur)
    if u >= 1.6:
        return 1.0
    if u < 1.0:
        return over * ez(u, "sine")
    return lerp(over, 1.0, ez((u - 1.0) / 0.6))


# ============================================================================= DIAGRAM (internal shot 26)
PIVOT = Vector((0.0, 0.0, 3.0))
ARM = 2.3
PAN_DROP = 1.55
Y_BACK, Y_POST, Y_PAN, Y_LOAF, Y_DROP, Y_PUFF, Y_LABEL = 3.0, 0.20, 0.10, 0.0, -0.06, -0.10, -0.16


def tilt_at(g):
    """beam tilt (deg, + = the loaf pan rises)."""
    if g < G27 + 4:
        return 0.0
    return 9.0 * ez((g - (G27 + 4)) / 30.0, "sine")


def loaf_scale_at(g):
    return lerp(1.0, 0.92, ez((g - (G27 + 2)) / 32.0)) if g > G27 + 2 else 1.0


def loaf_variant(g):
    if g < G27 + 10:
        return 0
    return 1 if g < G27 + 24 else 2


def hooks(g):
    th = math.radians(tilt_at(g))
    l = PIVOT + Vector((-ARM * math.cos(th), 0.0, ARM * math.sin(th)))
    r = PIVOT + Vector((ARM * math.cos(th), 0.0, -ARM * math.sin(th)))
    return l, r


def loaf_origin(g):
    l, _ = hooks(g)
    return Vector((l.x, Y_LOAF, l.z - PAN_DROP))


D_CAMS = {  # framing: (g_a, loc_a, look_a, g_b, loc_b, look_b, lens)
    "26a": (RANGES[26][0], (-2.30, -6.4, 2.40), (-2.30, 0.0, 2.40), CUT_B - 1, (-2.18, -5.5, 2.36), (-2.22, 0.0, 2.36), 35.0),
    "26b": (CUT_B, (-1.95, -3.7, 1.86), (-1.98, 0.0, 1.86), CUT_C - 1, (-2.05, -3.3, 1.84), (-2.05, 0.0, 1.84), 35.0),
    "26c": (CUT_C, (-2.35, -4.6, 2.15), (-2.30, 0.0, 2.15), G27 - 1, (-2.30, -4.9, 2.95), (-2.30, 0.0, 2.95), 35.0),
    "27": (G27, (-0.9, -9.8, 2.0), (-0.85, 0.0, 2.0), RANGES[26][1], (-0.12, -12.2, 1.75), (-0.10, 0.0, 1.75), 35.0),
}


def d_cam(g):
    fr = framing(26, g)
    a, la, ka, b, lb, kb, lens = D_CAMS[fr]
    v = clamp((g - a) / float(max(1, b - a)))
    u = ez(v, "sine") if fr != "27" else 1 - (1 - v) ** 2                 # 27: fast pull back, easing out
    return Vector(lerp(la, lb, u)), Vector(lerp(ka, kb, u)), lens


class DropSim(object):
    """the water drops in the crumb: each has a home (loaf-local x, z), a birth, a leave frame; after leaving it rises out of the
    crust and turns into a steam puff at z_puff.  Deterministic."""

    def __init__(self, seed=26):
        rnd = random.Random(seed)
        self.rnd = rnd
        self.drops = []

        def home():
            x = rnd.uniform(-0.82, 0.82)
            zmax = 0.70 * math.sqrt(max(0.0, 1 - (x / 0.98) ** 2))
            return x, rnd.uniform(0.14, max(0.18, zmax - 0.04))
        for i in range(24):
            self.drops.append(dict(home=home(), birth=-999, leave=None, var=rnd.randrange(3), ph=rnd.uniform(0, 6.3),
                                   size=rnd.uniform(0.11, 0.14)))
        acc = 0.0
        g = RANGES[26][0] - 40                                      # pre-roll: steam already rising at the first frame
        while g <= RANGES[26][1]:
            rate = 0.30 if g < EV["evap"] else (0.75 if g < G27 + 30 else 0.4)
            acc += rate
            while acc >= 1.0:
                acc -= 1.0
                sit = [d for d in self.drops if d["leave"] is None and d["birth"] <= g - 6]
                if not sit:
                    break
                d = rnd.choice(sit)
                d["leave"] = g
                d["vz"] = rnd.uniform(0.020, 0.030)
                d["acc"] = rnd.uniform(0.0006, 0.0012)
                d["sway"] = rnd.uniform(0.02, 0.05)
                d["zp"] = rnd.uniform(1.18, 1.45)
                if g < G27:                                          # replacement: the crumb stays wet until the afternoon
                    self.drops.append(dict(home=home(), birth=g, leave=None, var=rnd.randrange(3), ph=rnd.uniform(0, 6.3),
                                           size=rnd.uniform(0.11, 0.14)))
            g += 1
        for d in self.drops:                                         # the puff each leaving drop turns into
            if d["leave"] is not None:
                z, t = d["home"][1], 0
                while z < d["zp"] and t < 200:
                    t += 1
                    z = d["home"][1] + d["vz"] * t + d["acc"] * t * t
                d["g_puff"] = d["leave"] + t
                d["puff_var"] = rnd.randrange(3)
                d["puff_life"] = rnd.randint(40, 54)
                d["puff_s"] = rnd.uniform(0.60, 0.85)
                d["puff_dx"] = rnd.uniform(-0.010, 0.010)

    def drop_state(self, d, g):
        """loaf-local (x, z), scale, or None."""
        if g < d["birth"]:
            return None
        hx, hz = d["home"]
        s = d["size"] * min(1.0, (g - d["birth"]) / 5.0) if d["birth"] > -999 else d["size"]
        if d["leave"] is None or g < d["leave"]:
            # sitting: tiny jiggle; on "น้ำ" they pulse
            k = 1.0 + (0.18 * max(0.0, math.sin((g - EV["water"]) * 0.45 + d["ph"])) if EV["water"] <= g < CUT_C else 0.0)
            return (hx + 0.008 * math.sin(g * 0.3 + d["ph"]), hz + 0.008 * math.cos(g * 0.27 + d["ph"])), s * k
        t = g - d["leave"]
        z = hz + d["vz"] * t + d["acc"] * t * t
        if g >= d["g_puff"]:
            return None
        x = hx + d["sway"] * math.sin(0.22 * t + d["ph"]) + 0.06 * hx * (z - hz)
        return (x, z), s

    def puff_state(self, d, g):
        if d["leave"] is None or g < d["g_puff"]:
            return None
        t = g - d["g_puff"]
        if t > d["puff_life"]:
            return None
        hx = d["home"][0]
        x = hx + d["sway"] * math.sin(0.22 * (d["g_puff"] - d["leave"]) + d["ph"]) + 0.06 * hx * (d["zp"] - d["home"][1])
        x += d["puff_dx"] * t
        z = d["zp"] + 0.022 * t
        grow = ez(min(1.0, t / 7.0), "sine")
        die = 1.0 - ez(max(0.0, (t - (d["puff_life"] - 10)) / 10.0), "sine")
        return (x, z), d["puff_s"] * (0.35 + 0.65 * grow) * (1.0 + 0.012 * t) * die


class DiagramTake(object):
    def __init__(self, quality="preview"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        render.setup(scene, "final", bloom=False, samples=12, threads=2)
        scene.frame_start, scene.frame_end = 1, 9000
        self.cam = camrig.make_camera(scene, name="cam_s26", lens=35.0)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 200
        self.cam.data.dof.use_dof = False
        self.sim = DropSim()
        sv = os.path.join(TMP, "props")
        items = ([(loaf_cut_svg(k), LOAF_BOX, 256) for k in range(3)] + [(drop_svg(k), DROP_BOX, 192) for k in range(3)] +
                 [(puff_svg(k), PUFF_BOX, 192) for k in range(3)] +
                 [(post_svg(), POST_BOX, 160), (dial_svg(), DIAL_BOX, 256), (beam_svg(), BEAM_BOX, 192), (pan_svg(), PAN_BOX, 192),
                  (weights_svg(), WEIGHTS_BOX, 192)])
        P = C.svg_pngs(items, sv)
        self.loaf = C.PropCard("loaf", P[0:3], LOAF_BOX, shadow=False)
        self.post = C.PropCard("post", [P[9]], POST_BOX, shadow=False)
        self.dial = C.PropCard("dial", [P[10]], DIAL_BOX, shadow=False)
        self.beam = C.PropCard("beam", [P[11]], BEAM_BOX, shadow=False)
        self.pan_l = C.PropCard("pan_l", [P[12]], PAN_BOX, shadow=False)
        self.pan_r = C.PropCard("pan_r", [P[12]], PAN_BOX, shadow=False)
        self.weights = C.PropCard("weights", [P[13]], WEIGHTS_BOX, shadow=False)
        self.post.put((0, Y_POST, PIVOT.z))
        self.dial.put((0, Y_POST + 0.02, PIVOT.z))
        # labels
        lb = os.path.join(TMP, "labels")
        smoke = label_png("smoke_x", "ควัน", bg="#ffffff", fg="#7a8a9a", px=120, cross=True, out=lb)[0]
        water = label_png("water", "น้ำ", bg="#ffffff", fg="#1f74d6", px=130, pointer="bl", out=lb)[0]
        vapour = label_png("vapour", "ไอน้ำ", bg="#ffffff", fg="#1f74d6", px=120, pointer="b", out=lb)[0]
        t500 = label_png("t500", "500 ก.", bg="#fff6dc", fg=INK, px=110, tag=True, out=lb, radius=18)[0]
        t480 = label_png("t480", "480 ก.", bg="#fff6dc", fg="#d8322a", px=110, tag=True, out=lb, radius=18)[0]
        w500 = label_png("w500", "500 ก.", bg="#e6b445", fg=INK, px=90, out=lb, radius=18)[0]
        self.l_smoke = png_card("l_smoke", smoke, 300)
        self.l_water = png_card("l_water", water, 330)
        self.l_vapour = png_card("l_vapour", vapour, 300)
        self.tag = C.PropCard("tag", [t500, t480], self._box(t500, 300), shadow=False)
        self.l_w500 = png_card("l_w500", w500, 330)
        # backdrop (emission plane, far behind)
        self.back = C.PropCard("backdrop", [backdrop_png()], (-14.0, -24.0, 14.0, 24.0), shadow=False)
        self.back.put((0.0, Y_BACK, 2.5))
        # drops + puffs
        self.dcards = []
        for i, d in enumerate(self.sim.drops):
            pc = C.PropCard("drop%03d" % i, [P[3 + d["var"]]], DROP_BOX, scale=0.0001, shadow=False)
            self.dcards.append(pc)
        self.pcards = []
        for i, d in enumerate(self.sim.drops):
            if d["leave"] is not None:
                pc = C.PropCard("puff%03d" % i, [P[6 + d["puff_var"]]], PUFF_BOX, scale=0.0001, shadow=False)
                self.pcards.append((d, pc))
        self.actors = {}

    @staticmethod
    def _box(path, ppd):
        w, h = Image.open(path).size
        return (-w / 2.0 / ppd, -h / 2.0 / ppd, w / 2.0 / ppd, h / 2.0 / ppd)

    def pose(self, shot, gs):
        far = (0.0, -60.0, -40.0)
        for g in gs:
            f = bf(26, g)
            loc, look, lens = d_cam(g)
            camrig.key_camera(f, loc, look, cam=self.cam, lens=lens, interp="LINEAR", easing="AUTO")
            th = math.radians(tilt_at(g))
            hl, hr = hooks(g)
            _key_card(self.beam, f, (PIVOT.x, Y_POST - 0.03, PIVOT.z), 1.0, True, rot_y=th)
            _key_card(self.pan_l, f, (hl.x, Y_PAN, hl.z), 1.0, True)
            _key_card(self.pan_r, f, (hr.x, Y_PAN, hr.z), 1.0, True)
            _key_card(self.weights, f, (hr.x, Y_LOAF, hr.z - PAN_DROP), 1.0, True)
            _key_card(self.l_w500, f, (hr.x, Y_LABEL, hr.z - PAN_DROP - 0.40), 1.5, True)
            lo = loaf_origin(g)
            ls = loaf_scale_at(g)
            _show(self.loaf, loaf_variant(g), f)
            _key_card(self.loaf, f, (lo.x, Y_LOAF, lo.z), ls, True)
            # labels
            s = pop(g, EV["not_smoke"] + 2) if g < CUT_B else 0.0
            _show(self.l_smoke, 0 if s > 0.003 else None, f)
            _key_card(self.l_smoke, f, (lo.x + 0.55, Y_LABEL, lo.z + 2.15 + 0.004 * (g - EV["not_smoke"])) if s > 0 else far,
                      s * 1.25, s > 0)
            s = pop(g, EV["water"] + 1) if CUT_B <= g < CUT_C else 0.0
            _show(self.l_water, 0 if s > 0.003 else None, f)
            _key_card(self.l_water, f, (lo.x + 0.50, Y_LABEL, lo.z + 0.80) if s > 0 else far, s * 0.85, s > 0)
            s = pop(g, EV["evap"] + 3) if CUT_C <= g < G27 else 0.0
            _show(self.l_vapour, 0 if s > 0.003 else None, f)
            _key_card(self.l_vapour, f, (lo.x - 0.05, Y_LABEL, lo.z + 2.75 + 0.006 * (g - EV["evap"])) if s > 0 else far,
                      s * 1.10, s > 0)
            on = g >= G27
            s = (pop(g, EV["lighter"], dur=4, over=1.3) if g >= EV["lighter"] else pop(g, G27 + 2)) if on else 0.0
            _show(self.tag, (1 if g >= EV["lighter"] else 0) if s > 0.003 else None, f)
            _key_card(self.tag, f, (lo.x + 0.95, Y_LABEL - 0.05, lo.z + 2.45) if s > 0 else far, s * 1.9, s > 0)
            # drops / puffs
            for d, pc in zip(self.sim.drops, self.dcards):
                st = self.sim.drop_state(d, g)
                if st is None:
                    _show(pc, None, f)
                    _key_card(pc, f, far, 0.0001, False)
                else:
                    (x, z), sc = st
                    _show(pc, 0, f)
                    _key_card(pc, f, (lo.x + x * ls, Y_DROP, lo.z + z * ls), sc * ls, True)
            for pi, (d, pc) in enumerate(self.pcards):
                st = self.sim.puff_state(d, g)
                if st is None:
                    _show(pc, None, f)
                    _key_card(pc, f, far, 0.0001, False)
                else:
                    (x, z), sc = st
                    _show(pc, 0, f)
                    _key_card(pc, f, (lo.x + x * ls, Y_PUFF - 0.0015 * (pi % 40), lo.z + z * ls), sc, True)
        _constant([self.loaf, self.l_smoke, self.l_water, self.l_vapour, self.tag] + self.dcards + [pc for d, pc in self.pcards])

    def report(self, shot, g):
        f = bf(26, g)
        self.scene.frame_set(f)
        loc, look, lens = d_cam(g)
        lo = loaf_origin(g)
        live = sum(1 for d in self.sim.drops if self.sim.drop_state(d, g) is not None)
        puffs = sum(1 for d, pc in self.pcards if self.sim.puff_state(d, g) is not None)
        out = dict(shot=26, g=g, framing=framing(26, g), cam=[round(c, 3) for c in loc], tilt=round(tilt_at(g), 2), drops=live,
                   puffs=puffs, loaf_variant=loaf_variant(g))
        out["loaf_base_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(lo), f)[:2]]
        out["loaf_top_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(lo + Vector((0, 0, 1.0))), f)[:2]]
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        self.cam.data.dof.use_dof = False
        self.scene.cycles.samples = samples
        return render.render_frames([bf(26, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False, sync=False, check=False)


# ============================================================================= BAKERY (internal shot 28)
STEAM = 0.30
BASKET_SCALE = 0.40
BASKET_BOX = (-0.56, -0.06, 0.56, 0.72)
LAND = 1606
G_BADGE = 1610
LOAF13_R = 0.075                 # drawn loaf half width in the basket at scale 0.40 (basket loaves r 0.10 x 0.4 ... a bit bigger)


def pale_svg(svg, k=0.55, to=(255, 244, 222)):
    """recolour a cast6 bread drawing paler (the 13th loaf): every BREAD colour blended toward cream (cast6 tint is a no-op)."""
    for v in set(cast6.BREAD.values()):
        if isinstance(v, str) and v.startswith("#") and len(v) == 7:
            r, g, b = int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)
            n = "#%02x%02x%02x" % tuple(int(round(a + (c - a) * k)) for a, c in zip((r, g, b), to))
            svg = svg.replace(v, n).replace(v.upper(), n)
    return svg


def scale_angle_28(g):
    """+ = loaf pan down (set_scale).  Before the 13th: -7 (loaf side up = light).  Lands g LAND: swing to level."""
    if g <= LAND:
        return -7.0 + 0.4 * math.sin(g * 0.2)
    d = g - LAND
    return -7.0 * math.exp(-d / 6.0) * math.cos(d * 0.38)


B_CAMS = {  # (g_a, loc_a, look_a, g_b, loc_b, look_b, lens)
    "28a": (G28, (1.62, 1.55, 1.98), (1.90, 0.75, 1.72), CUT_28B - 1, (1.68, 1.38, 1.93), (1.90, 0.75, 1.72), 26.0),
    "28b": (CUT_28B, (2.32, 3.30, 2.05), (2.30, 0.75, 1.84), RANGES[28][1], (2.28, 2.90, 2.02), (2.26, 0.75, 1.86), 26.0),
}


def b_cam(g):
    a, la, ka, b, lb, kb, lens = B_CAMS[framing(28, g)]
    u = ez((g - a) / float(max(1, b - a)), "sine")
    return Vector(lerp(la, lb, u)), Vector(lerp(ka, kb, u)), lens


class Drop28(object):
    """little blue drops rising off the basket into the air (28b continuity with the diagram)."""

    def __init__(self, rnd, g0):
        self.g0 = g0
        self.life = rnd.randint(26, 36)
        self.dx = rnd.uniform(-0.12, 0.12)
        self.vz = rnd.uniform(0.010, 0.015)
        self.ph = rnd.uniform(0, 6.3)
        self.size = rnd.uniform(0.030, 0.042)
        self.var = rnd.randrange(3)

    def state(self, g, base):
        t = g - self.g0
        if t < 0 or t > self.life:
            return None
        p = base + Vector((self.dx + 0.015 * math.sin(0.25 * t + self.ph), -0.03, 0.10 + self.vz * t + 0.0002 * t * t))
        k = ez(min(1.0, t / 4.0) * min(1.0, (self.life - t) / 7.0), "sine")
        return p, self.size * k


class BakeryTake(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=26.0, name="cam_s28")
        sv = os.path.join(TMP, "props")
        items = [(cast6.basket_svg("bk12_26", loaves=12)[0], BASKET_BOX, 640),
                 (pale_svg(cast6.loaf_svg("pale13", r=0.17)), (-0.22, -0.22, 0.22, 0.14), 640)]
        items += [(drop_svg(k), DROP_BOX, 192) for k in range(3)]
        P = C.svg_pngs(items, sv)
        self.basket = C.PropCard("basket", [P[0]], BASKET_BOX, scale=BASKET_SCALE, shadow=True)
        self.loaf13 = C.PropCard("loaf13", [P[1]], (-0.22, -0.22, 0.22, 0.14), scale=1.0, shadow=True)
        bp = badge_png("plus1", "+1")[0]
        self.badge = C.PropCard("badge", [bp], (-0.5, -0.5, 0.5, 0.5), scale=0.0001, shadow=False)
        rnd = random.Random(28)
        self.drops, g, acc = [], CUT_28B - 20, 0.0
        while g <= RANGES[28][1]:
            acc += 0.55
            while acc >= 1.0:
                acc -= 1.0
                self.drops.append(Drop28(rnd, g))
            g += 1
        self.dcards = [C.PropCard("d28_%03d" % i, [P[2 + d.var]], DROP_BOX, scale=0.0001, shadow=False) for i, d in enumerate(self.drops)]
        self.pan_cache = {}

    def pan_top(self, g):
        if g not in self.pan_cache:
            B.set_scale(scale_angle_28(g))
            bpy.context.view_layer.update()
            pe = B.STATE["small"]["pans"][0]
            self.pan_cache[g] = pe.matrix_world.translation.copy() + Vector((0.0, 0.0, -0.62 + 0.05))
        return self.pan_cache[g]

    def loaf13_at(self, g):
        """(world centre, visible) of the pale 13th loaf (r 0.17 x scale 0.40 = 0.068 D) falling into the basket."""
        top = self.pan_top(g) + Vector((0.01, 0.05, 0.66 * BASKET_SCALE - 0.40 * BASKET_SCALE + 0.050))      # +y = toward the camera
        if g >= LAND:
            return top, True
        t0 = LAND - 9
        if g < t0:
            return top + Vector((0, 0, 1.2)), False
        u = (g - t0) / 9.0
        return top + Vector((0, 0, 0.75 * (1 - u * u))), True

    def pose(self, shot, gs):
        far = Vector((0, -60, -40))
        for g in gs:
            f = bf(28, g)
            loc, look, lens = b_cam(g)
            self.key_cam(f, loc, look, lens)
            self.key_set(f, steam=STEAM, oven=1.0)
            B.set_scale(scale_angle_28(g), frame=f)
            B.set_scale_loaf(False, frame=f)
        for g in gs:
            f = bf(28, g)
            loc, look, lens = b_cam(g)
            pt = self.pan_top(g)
            B.set_scale(scale_angle_28(g))
            self.basket.put(pt + Vector((0, 0.02, 0.66 * BASKET_SCALE)), face=tuple(loc), frame=f)
            p13, vis = self.loaf13_at(g)
            sq = 1.0
            if LAND <= g < LAND + 4:
                sq = [0.8, 1.1, 0.95, 1.0][g - LAND]
            k13 = 0.30
            self.loaf13.root.scale = (k13 / sq ** 0.5, k13, k13 * sq)
            self.loaf13.put(p13 if vis else far, face=tuple(loc), frame=f)
            self.loaf13.root.keyframe_insert("scale", frame=f)
            # +1 badge
            s = pop(g, G_BADGE, dur=5, over=1.3) * (0.20 if g < CUT_28B else 0.30)
            bpos = pt + Vector((-0.15, 0.10, 0.44)) if g < CUT_28B else pt + Vector((0.08, 0.10, 0.62))
            self.badge.root.scale = (max(s, 0.0001),) * 3
            self.badge.put(bpos if s > 0 else far, face=tuple(loc), frame=f)
            self.badge.root.keyframe_insert("scale", frame=f)
            self.badge.cards[0].hide_render = s <= 0.001
            self.badge.cards[0].keyframe_insert("hide_render", frame=f)
            base = pt + Vector((0, 0, 0.66 * BASKET_SCALE - 0.40 * BASKET_SCALE))
            for d, pc in zip(self.drops, self.dcards):
                st = d.state(g, base) if g >= CUT_28B - 20 else None
                ob = pc.cards[0]
                if st is None or st[1] < 0.003:
                    ob.hide_render = True
                    pc.root.scale = (0.0001,) * 3
                    pc.put(far, face=tuple(loc), frame=f)
                else:
                    ob.hide_render = False
                    pc.root.scale = (st[1],) * 3
                    pc.put(st[0], face=tuple(loc), frame=f)
                pc.root.keyframe_insert("scale", frame=f)
                ob.keyframe_insert("hide_render", frame=f)
        _constant([self.badge] + self.dcards)

    def report(self, shot, g):
        f = bf(28, g)
        self.scene.frame_set(f)
        loc, look, lens = b_cam(g)
        pt = self.pan_top(g)
        out = dict(shot=28, g=g, framing=framing(28, g), cam=[round(c, 3) for c in loc], scale_deg=round(scale_angle_28(g), 2))
        out["pan_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(pt), f)[:2]]
        p13, vis = self.loaf13_at(g)
        out["loaf13_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(p13), f)[:2]] if vis else None
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(28, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def make_take(shot, quality):
    return DiagramTake(quality) if shot == 26 else BakeryTake(quality)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if len(shots) != 1:
        raise SystemExit("one internal shot (26 or 28) per process")
    shot = shots[0]
    if cmd in ("probe", "stills"):
        Tk = make_take(shot, "preview")
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]
                os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: make_take(shot, q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
