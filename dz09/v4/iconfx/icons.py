"""icons.py -- DEAD ZONE 09 icon effects as SVG, generated in Python.  Pure functions: same arguments -> same SVG text.

Every icon is drawn in design units: a box (0, 0, w, h), by default 100 x 100, anchored at `anchor` (the point the
pop scales about and that placement puts on the target).  An icon function takes `t` (seconds on the icon's own
clock, 0 = first frame of its pop-in) and keyword options, and returns an `Icon(body, w, h, anchor)`.

    from icons import ICONS, make, to_svg
    ic = make("sound_rings", t=0.4, mode="arcs")
    svg = to_svg(ic, px=200)                       # standalone transparent SVG, 100 design units = 200 px
    svg = to_svg(ic, px=200, scale=1.15, rot=-5)   # one frame of a pop

Finish (matched to the new reference's graphics and to the puppets' ink):
  * flat fill, no gradients; ink outline #1f1d24 about 4 % of the icon (puppet ink), rounded joins and caps;
  * hand-drawn wobble baked into closed outlines with a fixed seed per icon (no filter noise: nothing swims);
  * a thin pale rim (#f4f1ea, 1.4 units) round the whole silhouette -- the reference's green check has one; it keeps
    the ink edge readable on the night set;
  * a slight soft drop shadow (offset 1.6, 2.6 units, blur 1.6, ink at 40 %);
  * the reference's own marks (red X, green check, yellow tape label, white swoosh arc, yellow draw-on arcs) are
    built the same way; the X has no ink outline, exactly as in the reference.
"""
import math, random
from collections import namedtuple

from anim import clamp, ease_out, ease_in_out

# ---- palette (BRIEF_camera_and_icons.md) ----------------------------------------------------------------------------
RED = "#e2453b"        # emergency red
YELLOW = "#ffd23f"     # warning yellow
INFECT = "#8fa37a"     # infected green-grey
WHITE = "#f4f1ea"
INK = "#1f1d24"
GREEN = "#2fbf3f"      # check / full battery (reference check measured #24c434; brief has no green, this is it)
SWEAT, SWEAT_HI, SWEAT_INK = "#b6e3ff", "#def9ff", "#5c647a"   # LOOK_SPEC 2.9
SLATE, SCREEN = "#39404f", "#9cc3e6"
OW = 4.0               # ink outline width, design units

Icon = namedtuple("Icon", "body w h anchor")

_uid = [0]


def _id(prefix):
    _uid[0] += 1
    return "%s%d" % (prefix, _uid[0])


def f(x):
    return ("%.2f" % x).rstrip("0").rstrip(".")


# ---- geometry helpers ------------------------------------------------------------------------------------------------
def circle_pts(cx, cy, r, n=48, a0=0.0):
    return [(cx + r * math.cos(a0 + 2 * math.pi * i / n), cy + r * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


def dense(poly, step=3.0, closed=True):
    out = []
    m = len(poly) if closed else len(poly) - 1
    for i in range(m):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % len(poly)]
        n = max(1, int(math.hypot(x1 - x0, y1 - y0) / step))
        out += [(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(n)]
    if not closed:
        out.append(poly[-1])
    return out


def rrect_pts(x0, y0, x1, y1, r, step=3.0):
    pts = []
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    for cx, cy, a in corners:
        for k in range(7):
            aa = math.radians(a + 90 * k / 6)
            pts.append((cx + r * math.cos(aa), cy + r * math.sin(aa)))
    return dense(pts, step)


def wobble(pts, seed, amp=0.7, closed=True):
    """displace points along their normal by a smooth seeded noise (3 sines over the outline length)."""
    if amp <= 0:
        return pts
    rnd = random.Random(seed)
    waves = [(rnd.uniform(2, 4), rnd.uniform(0, 6.283), 1.0), (rnd.uniform(5, 8), rnd.uniform(0, 6.283), 0.5),
             (rnd.uniform(9, 13), rnd.uniform(0, 6.283), 0.25)]
    n = len(pts)
    L = [0.0]
    for i in range(1, n):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = L[-1] or 1.0
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        b = pts[(i + 1) % n] if (closed or i < n - 1) else pts[i]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        s = L[i] / tot
        d = amp * sum(w * math.sin(2 * math.pi * fr * s + ph) for fr, ph, w in waves) / 1.75
        out.append((x + nx * d, y + ny * d))
    return out


def path_cr(pts, closed=True):
    """Catmull-Rom through the points as cubic Beziers."""
    n = len(pts)
    if n < 3:
        return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts)
    d = ["M%s,%s" % (f(pts[0][0]), f(pts[0][1]))]
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append("C%s,%s %s,%s %s,%s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1])))
    return " ".join(d) + (" Z" if closed else "")


def poly_d(pts, closed=True):
    return "M" + " L".join("%s,%s" % (f(x), f(y)) for x, y in pts) + (" Z" if closed else "")


def shape(d, fill, ow=OW, ink=INK, extra=""):
    if ow > 0:
        return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (d, fill, ink, f(ow), extra)
    return '<path d="%s" fill="%s"%s/>' % (d, fill, extra)


def stroke2(d, col, w, ow=OW * 0.6, ink=INK, cap="round", extra=""):
    """a coloured stroke with an ink outline (ink stroke w + 2 ow drawn first)."""
    s = ""
    if ow > 0:
        s += '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"%s/>' % (
            d, ink, f(w + 2 * ow), cap, extra)
    s += '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"%s/>' % (
        d, col, f(w), cap, extra)
    return s


def text(x, y, s, size, fill=WHITE, family="WS", ow=0.0, ink=INK, anchor="middle", extra=""):
    st = ' stroke="%s" stroke-width="%s" stroke-linejoin="round" paint-order="stroke"' % (ink, f(ow)) if ow > 0 else ""
    fam = "WS" if family == "WS" else "Kanit"
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return '<text x="%s" y="%s" font-family="%s" font-size="%s" text-anchor="%s" fill="%s"%s%s>%s</text>' % (
        f(x), f(y), fam, f(size), anchor, fill, st, extra, s)


def text_width(s, size, family="WS"):
    """width in design units of `s` at font size `size` (PIL + raqm with the same TTF the page uses)."""
    from PIL import ImageFont
    import os
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "fonts",
                        "WorkSans-Black.ttf" if family == "WS" else "Kanit_900Black.ttf")
    fnt = ImageFont.truetype(path, 200)
    return fnt.getlength(s) * size / 200.0


def arc_d(cx, cy, r, a0, a1):
    """SVG arc from angle a0 to a1 (degrees, 0 = right, clockwise positive since y is down)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return "M%s,%s A%s,%s 0 %d %d %s,%s" % (f(x0), f(y0), f(r), f(r), large, sweep, f(x1), f(y1))


def grp(body, tf="", extra=""):
    return '<g%s%s>%s</g>' % (' transform="%s"' % tf if tf else "", extra, body)


# ---- the icons -------------------------------------------------------------------------------------------------------
def battery(t=0.0, level=3, blink_hz=2.5, seed=11):
    """bars 3 / 2 / 1 (green, yellow, red); level 1 and 0 blink.  `level` may be a function of t."""
    lvl = level(t) if callable(level) else level
    lvl = int(max(0, min(3, lvl)))
    col = {3: GREEN, 2: YELLOW, 1: RED, 0: RED}[lvl]
    b = shape(path_cr(wobble(rrect_pts(8, 28, 80, 72, 10), seed, 0.6)), WHITE, OW + 0.5)
    b += shape(path_cr(rrect_pts(80, 40, 91, 60, 3.5, 2)), INK, 0)
    on = (int(t * blink_hz * 2) % 2 == 0) if lvl <= 1 else True
    for i in range(3):
        x = 16 + i * 20.5
        if i < lvl:
            op = "" if on else ' opacity="0.22"'
            b += shape(path_cr(rrect_pts(x, 36, x + 16.5, 64, 3, 2)), col, 2.2, extra=op)
        else:
            b += shape(path_cr(rrect_pts(x, 36, x + 16.5, 64, 3, 2)), "#d9d3c8", 0, extra=' opacity="0.8"')
    if lvl == 0 and on:
        b += shape(poly_d([(52, 30), (36, 53), (48, 53), (42, 72), (62, 45), (50, 45), (56, 30)]), YELLOW, 2.6)
    return Icon(b, 100, 100, (50, 50))


def phone(t=0.0, n=4, buzz=True, seed=12):
    """phone with a red missed-call badge; buzzes (rotation 6 deg at 14 Hz, 0.45 s of every 0.8 s) with buzz arcs."""
    buzzing = buzz and (t % 0.8) < 0.45
    ang = 6.0 * math.sin(2 * math.pi * 14 * t) if buzzing else 0.0
    b = shape(path_cr(wobble(rrect_pts(28, 12, 72, 88, 9), seed, 0.5)), SLATE, OW + 0.5)
    b += shape(path_cr(rrect_pts(33, 21, 67, 76, 3, 2)), SCREEN, 0)
    for k, w in enumerate((24, 18, 21)):
        y = 33 + k * 11
        b += '<path d="M38,%s h%s" stroke="%s" stroke-width="4" stroke-linecap="round" opacity="0.9"/>' % (y, w, WHITE)
    b += '<path d="M45,16.5 h10" stroke="%s" stroke-width="2.2" stroke-linecap="round"/>' % INK
    b += '<circle cx="50" cy="82" r="2.6" fill="%s"/>' % INK
    body = grp(b, "rotate(%s 50 50)" % f(ang))
    if buzzing:
        for s_ in (-1, 1):
            for k in range(2):
                r = 30 + k * 8
                a0, a1 = (155, 205) if s_ < 0 else (-25, 25)
                body += '<path d="%s" fill="none" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>' % (
                    arc_d(50, 50, r + 14, a0, a1), INK)
    badge = shape(path_cr(circle_pts(71, 21, 14, 40)), RED, 3.2)
    badge += text(71, 28.5, str(n), 20, WHITE)
    return Icon(body + grp(badge, "rotate(%s 50 50)" % f(ang)), 100, 100, (50, 50))


def _heart_pts(cx=50, cy=50, k=2.55, n=96):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + k * x, cy - k * y - 4))
    return pts


def heart(t=0.0, crack_at=0.15, split_dur=0.25, seed=13):
    """red heart; a zigzag crack draws on (0..crack_at s), then the halves split and tilt apart."""
    hp = wobble(_heart_pts(), seed, 0.6)
    d = path_cr(hp)
    ys = [p[1] for p in hp]
    top, bot = 50 - 2.55 * 5 - 4 + 2, max(ys) - 1          # notch is at y = cy - k*(13-5-2-1) - 4
    zig = [(50, top), (43, 38), (56, 50), (44, 61), (54, 72), (50, bot)]
    zd = poly_d(zig, False)
    crack = clamp(t / crack_at) if crack_at > 0 else 1.0
    sp = ease_out((t - crack_at) / split_dur) if t > crack_at else 0.0
    hi = '<ellipse cx="33" cy="33" rx="7" ry="4.5" transform="rotate(-35 33 33)" fill="%s" opacity="0.6"/>' % WHITE
    whole = shape(d, RED, OW + 0.5) + hi
    if sp <= 0:
        cl = '<path d="%s" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round" stroke-linecap="round" ' \
             'pathLength="1" stroke-dasharray="%s 1"/>' % (zd, INK, f(crack))
        return Icon(whole + cl, 100, 100, (50, 55))
    cl_id, cr_id = _id("hl"), _id("hr")
    left = poly_d(zig + [(-10, 110), (-10, -10)])
    right = poly_d(zig + [(110, 110), (110, -10)])
    defs = '<defs><clipPath id="%s"><path d="%s"/></clipPath><clipPath id="%s"><path d="%s"/></clipPath></defs>' % (
        cl_id, left, cr_id, right)
    edge = '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (zd, INK, f(OW))
    piece = shape(d, RED, OW + 0.5) + hi + edge
    L = grp(grp(piece, "", ' clip-path="url(#%s)"' % cl_id), "translate(%s %s) rotate(%s 50 %s)" % (
        f(-9 * sp), f(3 * sp), f(-12 * sp), f(bot)))
    R = grp(grp(shape(d, RED, OW + 0.5) + edge, "", ' clip-path="url(#%s)"' % cr_id),
            "translate(%s %s) rotate(%s 50 %s)" % (f(9 * sp), f(3 * sp), f(12 * sp), f(bot)))
    return Icon(defs + L + R, 100, 100, (50, 55))


def pinky(t=0.0, split_at=0.3, split_dur=0.25):
    """two hooked little fingers (the father-daughter promise); after split_at they pull apart and red crack ticks fly."""
    sp = ease_out((t - split_at) / split_dur) if t > split_at else 0.0
    dl = "M16,90 C16,62 30,46 48,44 C59,43 61,55 51,57"
    dr = "M84,10 C84,38 70,54 52,56 C41,57 39,45 49,43"
    fing = lambda d_: stroke2(d_, WHITE, 12, 3.2)
    L = grp(fing(dl), "translate(%s %s) rotate(%s 16 90)" % (f(-11 * sp), f(5 * sp), f(-14 * sp)))
    R = grp(fing(dr), "translate(%s %s) rotate(%s 84 10)" % (f(11 * sp), f(-5 * sp), f(-14 * sp)))
    b = L + R
    if sp > 0:
        for a in (-20, 70, 160, 250):
            r0, r1 = 14 + 14 * sp, 20 + 20 * sp
            x0, y0 = 50 + r0 * math.cos(math.radians(a)), 50 + r0 * math.sin(math.radians(a))
            x1, y1 = 50 + r1 * math.cos(math.radians(a)), 50 + r1 * math.sin(math.radians(a))
            b += stroke2("M%s,%s L%s,%s" % (f(x0), f(y0), f(x1), f(y1)), RED, 4.0, 1.6)
    return Icon(b, 100, 100, (50, 50))


def sound_rings(t=0.0, mode="arcs", period=0.9, n=3, color=RED, span=40, dot=False):
    """expanding rings (world rule 3: noise attracts the infected).  mode "arcs" = ((( ))) to both sides,
    "circle" = full rings.  A ring is born every period/n s, grows 10 -> 48 units ease-out, thins and fades."""
    b = ""
    for i in range(n):
        age = t / period - i / float(n)
        if age < 0:
            continue
        a = age % 1.0
        r = 10 + 38 * ease_out(a)
        op = (1 - a) ** 1.5
        w = 6.0 * (1 - 0.55 * a)
        if mode == "circle":
            ds = [path_cr(circle_pts(50, 50, r, 64))]
        else:
            ds = [arc_d(50, 50, r, -span, span), arc_d(50, 50, r, 180 - span, 180 + span)]
        for d in ds:
            b += stroke2(d, color, w, 2.0, extra=' opacity="%s"' % f(op))
    if dot:
        b += shape(path_cr(circle_pts(50, 50, 5, 24)), color, 2.4)
    return Icon(b, 100, 100, (50, 50))


def eye(t=0.0, open_t=0.12, ticks=True, seed=14):
    """white eye, dark iris, glowing red pupil that contracts (10 -> 6 units at 0.25-0.45 s); lid opens first."""
    lid = max(0.08, ease_out(t / open_t)) if open_t > 0 else 1.0
    cid = _id("eye")
    outline = path_cr(wobble(dense([(8, 50), (50, 21), (92, 50), (50, 79)], 2.5), seed, 0.0))
    al = "M8,50 C26,18 74,18 92,50 C74,82 26,82 8,50 Z"
    veins = ""
    for (x0, y0, x1, y1, x2, y2) in ((12, 50, 24, 46, 30, 41), (12, 51, 23, 55, 29, 60), (88, 50, 76, 45, 70, 40),
                                     (88, 51, 77, 56, 72, 62)):
        veins += '<path d="M%d,%d Q%d,%d %d,%d" fill="none" stroke="%s" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>' % (
            x0, y0, x1, y1, x2, y2, RED)
    pr = 10 - 4 * ease_in_out((t - 0.25) / 0.2)
    inner = '<path d="%s" fill="%s"/>' % (al, WHITE) + veins
    inner += '<circle cx="50" cy="50" r="18" fill="#2a1d22" stroke="%s" stroke-width="2.5"/>' % INK
    inner += '<circle cx="50" cy="50" r="%s" fill="%s" opacity="0.45" filter="url(#ifx_glow)"/>' % (f(pr + 4), RED)
    inner += '<circle cx="50" cy="50" r="%s" fill="%s"/>' % (f(pr), RED)
    inner += '<circle cx="43" cy="43" r="3.6" fill="%s"/>' % WHITE
    body = '<defs><clipPath id="%s"><path d="%s"/></clipPath></defs>' % (cid, al)
    body += grp(grp(inner, "", ' clip-path="url(#%s)"' % cid) +
                '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (al, INK, f(OW + 0.5)),
                "translate(0 50) scale(1 %s) translate(0 -50)" % f(lid))
    if ticks and t > 0.15:
        g = ease_out((t - 0.15) / 0.1)
        for a in (-125, -90, -55):
            r0, r1 = 34, 34 + 10 * g
            x0, y0 = 50 + r0 * math.cos(math.radians(a)), 50 + r0 * math.sin(math.radians(a)) - 2
            x1, y1 = 50 + r1 * math.cos(math.radians(a)), 50 + r1 * math.sin(math.radians(a)) - 2
            body += '<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="3.6" stroke-linecap="round"/>' % (
                f(x0), f(y0), f(x1), f(y1), INK)
    return Icon(body, 100, 100, (50, 50))


def stopwatch(t=0.0, total=60.0, elapsed=None, speed=1.0, number=True, seed=15):
    """60 s stopwatch: red wedge and hand sweep clockwise from 12 o'clock; the number counts down.
    elapsed (s) overrides t * speed (use speed > 1 to compress the 60 s rule into a short beat)."""
    e = elapsed if elapsed is not None else t * speed
    fr = clamp(e / total)
    cx, cy, R = 50, 57, 33
    b = shape(path_cr(rrect_pts(43, 7, 57, 15, 3, 2)), WHITE, 3.0)
    b += shape("M47,15 h6 v8 h-6 Z", INK, 0)
    b += grp(shape(path_cr(rrect_pts(46, 17, 54, 24, 2, 2)), WHITE, 2.6), "rotate(45 %d %d)" % (cx, cy - R + 3) +
             " translate(0 -2)")
    b += shape(path_cr(wobble(circle_pts(cx, cy, R, 72), seed, 0.5)), WHITE, OW + 0.5)
    if fr >= 0.999:
        b += '<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="0.92"/>' % (cx, cy, R - 4, RED)
    elif fr > 0:
        a1 = -90 + 360 * fr
        b += '<path d="M%d,%d L%s Z" fill="%s" opacity="0.92"/>' % (
            cx, cy, arc_d(cx, cy, R - 4, -90, a1)[1:].replace(" A", " A"), RED)
    for k in range(12):
        a = math.radians(-90 + 30 * k)
        r0 = R - (9 if k % 3 == 0 else 6)
        b += '<path d="M%s,%s L%s,%s" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            f(cx + r0 * math.cos(a)), f(cy + r0 * math.sin(a)), f(cx + (R - 3) * math.cos(a)),
            f(cy + (R - 3) * math.sin(a)), INK, "3" if k % 3 == 0 else "2")
    if number:
        rem = int(math.ceil(total - e - 1e-6)) if e < total else 0
        b += text(cx, cy + 20, str(rem), 12, INK, ow=3.0, ink=WHITE)
    a = math.radians(-90 + 360 * fr)
    b += stroke2("M%d,%d L%s,%s" % (cx, cy, f(cx + (R - 6) * math.cos(a)), f(cy + (R - 6) * math.sin(a))), RED, 3.2, 1.4)
    b += '<circle cx="%d" cy="%d" r="3.8" fill="%s"/>' % (cx, cy, INK)
    return Icon(b, 100, 100, (50, 55))


def _bio_mask(cx, cy, s, mid):
    """biohazard symbol as an SVG mask (white = ink).  s = overall radius."""
    w = '<g fill="white">'
    k = '<g fill="black">'
    for i in range(3):
        a = math.radians(-90 + 120 * i)
        ux, uy = math.cos(a), math.sin(a)
        w += '<circle cx="%s" cy="%s" r="%s"/>' % (f(cx + ux * 0.40 * s), f(cy + uy * 0.40 * s), f(0.50 * s))
        k += '<circle cx="%s" cy="%s" r="%s"/>' % (f(cx + ux * 0.52 * s), f(cy + uy * 0.52 * s), f(0.36 * s))
        # gap where the ring crosses the crescent tips
        k += '<path d="M%s,%s L%s,%s" stroke="black" stroke-width="%s"/>' % (
            f(cx), f(cy), f(cx + ux * 0.25 * s), f(cy + uy * 0.25 * s), f(0.07 * s))
    w += '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="white" stroke-width="%s"/>' % (
        f(cx), f(cy), f(0.42 * s), f(0.13 * s))
    k += '<circle cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(0.13 * s))
    w += "</g>"
    k += "</g>"
    return '<mask id="%s" maskUnits="userSpaceOnUse" x="-50" y="-50" width="250" height="250">%s%s</mask>' % (mid, w, k)


def biohazard_symbol(cx, cy, s, fill=INK, outline=None):
    mid = _id("bio")
    b = "<defs>%s</defs>" % _bio_mask(cx, cy, s, mid)
    rect = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" mask="url(#%s)"/>' % (
        f(cx - 1.2 * s), f(cy - 1.2 * s), f(2.4 * s), f(2.4 * s), fill, mid)
    if outline:
        b += grp(rect, "", ' filter="url(#ifx_ol)"')
    else:
        b += rect
    return b


def biohazard(t=0.0, disc=True, spin=0.0, color=INK, seed=16):
    """biohazard sign: ink symbol on a yellow disc (disc=False: the symbol alone in `color` with an ink outline)."""
    b = ""
    if disc:
        b += shape(path_cr(wobble(circle_pts(50, 50, 44, 72), seed, 0.6)), YELLOW, OW + 0.5)
    sym = biohazard_symbol(50, 50, 34 if disc else 44, color if not disc else INK,
                           outline=None if disc else INK)
    b += grp(sym, "rotate(%s 50 50)" % f(spin * t)) if spin else sym
    return Icon(b, 100, 100, (50, 50))


def warning(t=0.0, symbol="!", color=YELLOW, pulse=True, seed=17):
    """rounded warning triangle; symbol "!" or "bio"; color YELLOW (ink symbol) or RED (white symbol)."""
    sc = 1.0 + (0.04 * math.sin(2 * math.pi * 2.0 * t) if pulse else 0.0)
    tri = dense([(50, 9), (93, 85), (7, 85)], 2.0)
    # round the corners: average each point with its neighbours a few times
    for _ in range(4):
        tri = [((tri[i - 1][0] + 2 * tri[i][0] + tri[(i + 1) % len(tri)][0]) / 4,
                (tri[i - 1][1] + 2 * tri[i][1] + tri[(i + 1) % len(tri)][1]) / 4) for i in range(len(tri))]
    b = shape(path_cr(wobble(tri, seed, 0.6)), color, OW + 1.0)
    sym_col = INK if color != RED else WHITE
    if symbol == "bio":
        b += biohazard_symbol(50, 60, 21, sym_col)
    else:
        b += '<path d="M50,34 L50,58" stroke="%s" stroke-width="10" stroke-linecap="round"/>' % sym_col
        b += '<circle cx="50" cy="72" r="5.6" fill="%s"/>' % sym_col
    return Icon(grp(b, "translate(50 55) scale(%s) translate(-50 -55)" % f(sc)), 100, 100, (50, 55))


def exclaim_sparks(t=0.0, color=YELLOW, spread=36, bang=False, shake=True):
    """three yellow spark strokes fanning up from the anchor (put the anchor on the top of the head); they shoot out in
    0.12 s, then breathe.  bang=True adds a yellow "!" in the middle."""
    g = ease_out(t / 0.12)
    br = 1 + 0.07 * math.sin(2 * math.pi * 3 * t)
    jx = (1.2 if int(t * 30) % 2 else -1.2) if (shake and t < 0.4) else 0.0
    b = ""
    for k, a in enumerate((-spread, 0, spread)):
        aa = math.radians(-90 + a)
        r0 = 26 + (6 if a == 0 else 0)
        r1 = r0 + (34 if a == 0 else 28) * g * br
        b += stroke2("M%s,%s L%s,%s" % (f(50 + r0 * math.cos(aa)), f(92 + r0 * math.sin(aa)),
                                         f(50 + r1 * math.cos(aa)), f(92 + r1 * math.sin(aa))), color, 7.5, 2.4)
    if bang:
        b += text(50, 70, "!", 34, color, ow=5, extra=' font-style="normal"')
    return Icon(grp(b, "translate(%s 0)" % f(jx)), 100, 100, (50, 92))


def question(t=0.0, seed=18):
    """scribble swirl (turning -200 deg/s) beside a white "?" that rocks +-8 deg."""
    pts = []
    for i in range(80):
        s = i / 79.0
        a = s * 2.3 * 2 * math.pi
        r = 2 + 15 * s
        pts.append((33 + r * math.cos(a), 48 + r * math.sin(a) * 0.85))
    pts = wobble(pts, seed, 0.8, closed=False)
    sw = '<path d="%s" fill="none" stroke="%s" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>' % (
        path_cr(pts, False), INK)
    b = grp(sw, "rotate(%s 33 48)" % f(-200 * t))
    rock = 8 * math.sin(2 * math.pi * 1.2 * t)
    b += grp(text(68, 70, "?", 56, WHITE, ow=6.0), "rotate(%s 68 52)" % f(rock))
    return Icon(b, 100, 100, (50, 60))


def sweat(t=0.0, slide=8.0, period=1.2, seed=19):
    """LOOK_SPEC 2.9 sweat drop (#b6e3ff, light #def9ff, slate outline #5c647a); slides down `slide` units per period."""
    k = ease_in_out((t % period) / period)
    dy = slide * k
    st = 1 + 0.06 * k
    d = "M50,10 C57,28 72,42 72,60 A22,22 0 1 1 28,60 C28,42 43,28 50,10 Z"
    b = shape(d, SWEAT, 3.6, SWEAT_INK)
    b += '<ellipse cx="40" cy="62" rx="5" ry="9" fill="%s"/>' % SWEAT_HI
    b += '<circle cx="44" cy="45" r="2.6" fill="%s"/>' % SWEAT_HI
    return Icon(grp(b, "translate(0 %s) translate(50 82) scale(1 %s) translate(-50 -82)" % (f(dy), f(st))), 100, 100, (50, 50))


def light_rays(t=0.0, n=12, color=RED, hz=2.0, spin=25.0, beacon=True):
    """emergency light rays: n wedges (narrow at the centre), turning `spin` deg/s, opacity pulsing at `hz`."""
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.cos(2 * math.pi * hz * t))
    rot = spin * t
    b = ""
    for i in range(n):
        a = 360.0 * i / n + rot
        p = []
        for aa, r in ((a - 2.5, 16), (a - 7.5, 49), (a + 7.5, 49), (a + 2.5, 16)):
            p.append((50 + r * math.cos(math.radians(aa)), 50 + r * math.sin(math.radians(aa))))
        b += shape(poly_d(p), color, 1.6, extra=' opacity="%s"' % f(pulse if i % 2 == 0 else pulse * 0.75))
    if beacon:
        b += shape(path_cr(circle_pts(50, 50, 12, 40)), color, OW)
        b += '<ellipse cx="46" cy="45" rx="4" ry="2.6" fill="%s" opacity="0.8"/>' % WHITE
    return Icon(b, 100, 100, (50, 50))


# ---- the reference's own marks --------------------------------------------------------------------------------------
def x_mark(t=0.0, color=RED, outline=0.0, strike=False):
    """red X (reference: flat, no ink outline, square-ish ends).  strike=True draws the two bars one after the other
    (4 frames each) instead of popping."""
    p1 = clamp(t / 0.133) if strike else 1.0
    p2 = clamp((t - 0.133) / 0.133) if strike else 1.0
    b = ""
    for (x0, y0, x1, y1), p in (((16, 16, 84, 84), p1), ((84, 16, 16, 84), p2)):
        if p <= 0:
            continue
        d = "M%s,%s L%s,%s" % (f(x0), f(y0), f(x0 + (x1 - x0) * p), f(y0 + (y1 - y0) * p))
        b += stroke2(d, color, 17, outline, cap="square" if outline == 0 else "round")
    return Icon(b, 100, 100, (50, 50))


def check(t=0.0, color=GREEN, draw=False):
    """green tick with ink outline and round caps (reference); draw=True strokes it on in 0.2 s."""
    p = clamp(t / 0.2) if draw else 1.0
    d = "M16,54 L40,77 L86,25"
    ex = ' pathLength="1" stroke-dasharray="%s 2"' % f(p) if draw else ""
    return Icon(stroke2(d, color, 15, 2.8, extra=ex), 100, 100, (50, 50))


def tape_label(t=0.0, label="0.9 MILE", family="WS", size=24, color=YELLOW):
    """the reference's yellow measuring-tape label: rounded yellow box, ink border, ink capitals.  Thai text: Kanit."""
    tw = text_width(label, size, family)
    w = tw + 26
    h = size * 1.55
    b = shape(path_cr(rrect_pts(3, 3, w - 3, h - 3, 5, 2)), color, 3.2)
    b += text(w / 2, h / 2 + size * (0.36 if family == "WS" else 0.33), label, size, INK, family)
    return Icon(b, w, h, (w / 2, h / 2))


def tape(t=0.0, length=200.0, grow=0.5, unit=20.0, start_num=0, color=YELLOW):
    """a measuring-tape strip (horizontal, length units long) that rolls out in `grow` s.  Ticks every unit/5, numbers
    every unit, red diamond at the start.  Lay it flat on the ground in 3D (blender_card.add_card(flat=True))."""
    vis = length * ease_out(t / grow) if grow > 0 else length
    H = 22.0
    cid = _id("tp")
    b = '<defs><clipPath id="%s"><rect x="-5" y="-5" width="%s" height="%s"/></clipPath></defs>' % (cid, f(vis + 8), f(H + 10))
    s = shape("M2,2 H%s V%s H2 Z" % (f(length + 2), f(H)), color, 2.6)
    k = 0
    x = 2.0
    while x <= length + 2 + 1e-6:
        big = k % 5 == 0
        s += '<path d="M%s,2 V%s" stroke="%s" stroke-width="%s"/>' % (f(x), f(10 if big else 6.5), INK, "1.6" if big else "1")
        if big and k > 0:
            s += text(x - 3, 19, str(start_num + k // 5), 8, INK, anchor="end")
        x += unit / 5.0
        k += 1
    s += '<path d="M2,%s l4,-4 l4,4 l-4,4 Z" fill="%s"/>' % (f(H - 5), RED)
    b += grp(s, "", ' clip-path="url(#%s)"' % cid)
    return Icon(b, length + 4, H + 2, (2, H / 2))


def swoosh(t=0.0, r=40.0, a0=200.0, a1=-30.0, dur=0.22, lag=0.14, width=8.0, color="#fffaf0"):
    """the reference's white glowing arc around a character: the head runs from a0 to a1 (deg, 0 = right, clockwise)
    in `dur` s, the tail follows `lag` s later, then it fades.  Tapered: 0 at the tail, `width` at the head."""
    h = a0 + (a1 - a0) * ease_out(t / dur)
    tl = a0 + (a1 - a0) * ease_out((t - lag) / dur)
    fade = 1 - clamp((t - dur - lag) / 0.15)
    if abs(h - tl) < 0.5 or fade <= 0:
        return Icon("", 100, 100, (50, 50))
    n = 40
    outer, inner = [], []
    for i in range(n + 1):
        s = i / float(n)
        a = math.radians(tl + (h - tl) * s)
        w = width * (s ** 0.8) * 0.5
        outer.append((50 + (r + w) * math.cos(a), 50 + (r + w) * math.sin(a)))
        inner.append((50 + (r - w) * math.cos(a), 50 + (r - w) * math.sin(a)))
    d = poly_d(outer + inner[::-1])
    b = '<path d="%s" fill="%s" opacity="%s" filter="url(#ifx_glow)"/>' % (d, color, f(0.9 * fade))
    b += '<path d="%s" fill="%s" opacity="%s"/>' % (d, color, f(fade))
    return Icon(b, 100, 100, (50, 50))


def arc_fan(t=0.0, n=6, src=(12, 94), color=YELLOW, dur=0.35, stagger=0.05, width=2.4, seed=21):
    """the reference's yellow trajectory arcs: n curves from `src` to points across the top, drawn on one after the
    other (stroke-dashoffset)."""
    rnd = random.Random(seed)
    b = ""
    for i in range(n):
        p = ease_out((t - i * stagger) / dur)
        if p <= 0:
            continue
        tx, ty = 38 + i * (58.0 / max(1, n - 1)), 10 + rnd.uniform(0, 26)
        cx, cy = (src[0] + tx) / 2 - 4, min(src[1], ty) - 22
        d = "M%s,%s Q%s,%s %s,%s" % (f(src[0]), f(src[1]), f(cx), f(cy), f(tx), f(ty))
        b += '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" pathLength="1" ' \
             'stroke-dasharray="%s 2"/>' % (d, color, f(width), f(p))
    return Icon(b, 100, 100, src)


ICONS = {
    "battery": battery, "phone": phone, "heart": heart, "pinky": pinky, "sound_rings": sound_rings, "eye": eye,
    "stopwatch": stopwatch, "biohazard": biohazard, "warning": warning, "exclaim_sparks": exclaim_sparks,
    "question": question, "sweat": sweat, "light_rays": light_rays,
    "x_mark": x_mark, "check": check, "tape_label": tape_label, "tape": tape, "swoosh": swoosh, "arc_fan": arc_fan,
}

# meaning, suggested sound accent (label only; the SFX are chosen at the conform), finish flags
META = {
    "battery": ("cutter power (EP.6 setup)", "electronic blip, lower pitch per bar", {}),
    "phone": ("missed calls = the broken promise", "phone buzz x2", {}),
    "heart": ("the promise between father and daughter", "glass crack, soft", {}),
    "pinky": ("the promise, broken", "small snap", {}),
    "sound_rings": ("noise attracts the infected (rule 3)", "rides on the source sound; low thump", {"rim": False}),
    "eye": ("an infected one has noticed", "wet click + low sting", {}),
    "stopwatch": ("bite-to-turn, 60 s (rule 1)", "clock tick per second", {}),
    "biohazard": ("outbreak / danger zone 09", "alarm sting", {}),
    "warning": ("danger zone", "alarm beep", {}),
    "exclaim_sparks": ("surprise / alarm", "pop + whoosh", {}),
    "question": ("confusion / doubt", "boing, soft", {}),
    "sweat": ("fear / pressure", "drip", {}),
    "light_rays": ("danger pulse; emphasis", "siren whoop", {"rim": False}),
    "x_mark": ("wrong / no (reference mark)", "buzzer, short", {}),
    "check": ("right / yes (reference mark)", "ding", {}),
    "tape_label": ("distance label (reference mark)", "tape zip", {}),
    "tape": ("measuring tape strip (reference mark)", "tape zip", {"rim": False}),
    "swoosh": ("action arc round a character (reference)", "whoosh", {"rim": False, "shadow": False}),
    "arc_fan": ("trajectory arcs (reference)", "whoosh x n", {"rim": False, "shadow": False}),
}


def make(name, t=0.0, **kw):
    return ICONS[name](t, **kw)


# ---- finish + wrappers -----------------------------------------------------------------------------------------------
def defs(rim=1.4, rim_col=WHITE, shadow=(1.6, 2.6, 1.6, 0.40), rim_op=0.9):
    """the shared filters: ifx_fin (pale rim + drop shadow), ifx_fin_s (shadow only), ifx_glow, ifx_ol (ink outline)."""
    dx, dy, blur, op = shadow
    return (
        '<defs>'
        '<filter id="ifx_fin" x="-40%%" y="-40%%" width="180%%" height="180%%" color-interpolation-filters="sRGB">'
        '<feMorphology in="SourceAlpha" operator="dilate" radius="%s" result="d"/>'
        '<feFlood flood-color="%s" flood-opacity="%s"/><feComposite in2="d" operator="in" result="rim"/>'
        '<feGaussianBlur in="d" stdDeviation="%s" result="b"/><feOffset in="b" dx="%s" dy="%s" result="o"/>'
        '<feFlood flood-color="#0b0a10" flood-opacity="%s"/><feComposite in2="o" operator="in" result="sh"/>'
        '<feMerge><feMergeNode in="sh"/><feMergeNode in="rim"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="ifx_fin_s" x="-40%%" y="-40%%" width="180%%" height="180%%" color-interpolation-filters="sRGB">'
        '<feGaussianBlur in="SourceAlpha" stdDeviation="%s" result="b"/><feOffset in="b" dx="%s" dy="%s" result="o"/>'
        '<feFlood flood-color="#0b0a10" flood-opacity="%s"/><feComposite in2="o" operator="in" result="sh"/>'
        '<feMerge><feMergeNode in="sh"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '<filter id="ifx_glow" x="-50%%" y="-50%%" width="200%%" height="200%%"><feGaussianBlur stdDeviation="2.6"/></filter>'
        '<filter id="ifx_ol" x="-20%%" y="-20%%" width="140%%" height="140%%">'
        '<feMorphology in="SourceAlpha" operator="dilate" radius="2.2" result="d"/>'
        '<feFlood flood-color="%s"/><feComposite in2="d" operator="in" result="ink"/>'
        '<feMerge><feMergeNode in="ink"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        '</defs>') % (f(rim), rim_col, f(rim_op), f(blur), f(dx), f(dy), f(op), f(blur), f(dx), f(dy), f(op), INK)


def _finish_attr(name, rim=None, shadow=None):
    fl = META.get(name, ("", "", {}))[2] if name else {}
    rim = fl.get("rim", True) if rim is None else rim
    shadow = fl.get("shadow", True) if shadow is None else shadow
    if rim:
        return ' filter="url(#ifx_fin)"'
    if shadow:
        return ' filter="url(#ifx_fin_s)"'
    return ""


def placed(ic, x, y, px, scale=1.0, rot=0.0, opacity=1.0, name=None, rim=None, shadow=None):
    """<g> that puts icon `ic` with its anchor on (x, y) of the parent (pixels), 100 units = px pixels, popped by
    scale / rot / opacity.  Needs defs() once in the parent SVG."""
    k = px / 100.0
    ax, ay = ic.anchor
    tf = "translate(%s %s) rotate(%s) scale(%s) translate(%s %s)" % (f(x), f(y), f(rot), f(k * scale), f(-ax), f(-ay))
    op = ' opacity="%s"' % f(opacity) if opacity < 1 else ""
    return '<g transform="%s"%s><g%s>%s</g></g>' % (tf, op, _finish_attr(name, rim, shadow), ic.body)


def canvas_size(ic, px, pad=0.25):
    k = px / 100.0
    m = pad * max(ic.w, ic.h)
    return int(math.ceil((ic.w + 2 * m) * k)), int(math.ceil((ic.h + 2 * m) * k)), m


def to_svg(ic, px=200, scale=1.0, rot=0.0, opacity=1.0, pad=0.25, name=None, rim=None, shadow=None, bg=None):
    """standalone SVG of one icon on a transparent canvas big enough for a 115 % overshoot, rim and shadow.
    The anchor sits at (pad*max(w,h) + anchor) * px/100 pixels.  Returns (svg_text, w_px, h_px, anchor_px)."""
    W, H, m = canvas_size(ic, px, pad)
    k = px / 100.0
    ax, ay = (m + ic.anchor[0]) * k, (m + ic.anchor[1]) * k
    s = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)
    s += defs()
    if bg:
        s += '<rect width="%d" height="%d" fill="%s"/>' % (W, H, bg)
    s += placed(ic, ax, ay, px, scale, rot, opacity, name, rim, shadow)
    return s + "</svg>", W, H, (ax, ay)
