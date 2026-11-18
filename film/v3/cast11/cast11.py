#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast11.py -- the cast of film 11 ("ไอ้หมอวัว": Edward Jenner and cowpox, Berkeley, Gloucestershire, May 1796) for the v2 puppet,
as an extension module on top of cast10 (cast10 -> cast9 -> ... -> cast_ext -> v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast11"); import cast11     # registers on import (idempotent); imports cast10 .. cast_ext
    import puppet                                                      # the same module object, now with the new members
    cast, pose = cast11.STORY11["jenner_lancet_up"]
    f = puppet.figure(cast, pose, "f")
    b = puppet.figure("blossom", cast11.STORY11["blossom_chew"][1], "b")   # the cow: same figure() contract (svg, feet_y, bbox, anchors)

Nothing in v2/puppet or v3/cast .. cast10 is edited.  Added to their tables:
    cast_ext.COSTUMES  shirt11 (linen shirt / braces / waistcoat / breeches), gown11 (short gown, striped petticoat, apron, shawl)
    cast_ext.HATS      queue11 (own hair tied back in a queue), wig11 (powdered bob wig + tricorn), mobcap11 (frilled mob cap),
                       bonnet11 (straw hat / bonnet with hair locks), messy11 (mop of hair; cow horns + cow ears gag)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
wrappers on top of cast10's: _norm (pose keys), _face (pockmarks, fever flush), _ink_limb (stockings / bare shins), _prop (new props),
figure (stool, yoke with pails, the cow "blossom").  Every wrapper falls through, so earlier members draw exactly as before.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10    # noqa: E402  (v3/cast10, read-only; imports cast9 .. cast_ext and v2/puppet)
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW11 = ("jenner", "james", "sarah", "milkmaid2", "towndoc", "mother", "villager_a", "villager_b", "villager_c", "villager_d", "villager_e")
COW = "blossom"
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_poly_d = P._poly_d
_f = C6._f
_O11 = {}
_POSE11 = {"seated": False, "sitfront": False, "pocks": None, "flush": 0.0, "horns": 0.0, "ears": 0.0, "hat_off": 0.0, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
GOLD = dict(light="#fff0a8", base="#e2b442", dark="#a07818", deep="#6a4c0c")
STEEL = dict(light="#f0f2f4", base="#b4bcc6", dark="#6c7683")
WOOD = dict(light="#e6bd84", base="#b98450", dark="#74502a")
GLASS = dict(light="#d6efe8", base="#9ccfc4", dark="#5a9a90")
SKIN = dict(light="#fbe2d2", base="#f3cdb6", dark="#d9a58c")
POCK = "#a4524c"
HORN = dict(light="#fff3da", base="#ecd6a8", dark="#b8955a", tip="#8a6a3c")


def _poly(k, pts, fill, sw=0.014):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_poly_d(pts), fill, k.ink, sw)


def _smooth_fill(k, pts, fill, sw=0.014, closed=True):
    d = P._smooth_closed(pts) if closed else P._smooth_open(pts) + "Z"
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (d, fill, k.ink, sw)


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


# ============================================================================= hats (head frame, drawn over the head)
def _hat_queue11(k, C, yaw):
    """Jenner's own hair: grey-brown, swept back off a high forehead, side curls over the ears, tied at the nape with a black
    ribbon into a queue that hangs behind the head (visible when turned)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.10 * yaw
    g = CE._gradient(k, "qh", col, x0=-0.55, x1=0.55, mid=0.36)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    s = -1 if yaw > 0 else 1                       # the back of the head is opposite the facing side
    a = abs(yaw)
    if a > 0.10:
        qa = _smooth(0.10, 0.22, a)
        bx, by = s * (0.44 + 0.02 * a), -0.04
        tail = [(bx, by), (bx + s * 0.10, 0.12), (bx + s * 0.16, 0.30), (bx + s * 0.13, 0.50), (bx + s * 0.06, 0.62)]
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.17" stroke-linecap="round" opacity="%.3f"/>' % (P._smooth_open(tail), k.ink, qa))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.125" stroke-linecap="round" opacity="%.3f"/>' % (P._smooth_open(tail), k.c(col["base"]), qa))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="%.3f"/>'
                 % (P._smooth_open([(bx + s * 0.02, 0.12), (bx + s * 0.09, 0.30), (bx + s * 0.07, 0.52)]), k.c(col["light"]), qa))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.045" fill="%s" stroke="%s" stroke-width="0.012" opacity="%.3f" transform="rotate(%.1f %.4f %.4f)"/>'
                 % (bx + s * 0.075, 0.115, k.c(col["ribbon"]), k.ink, qa, 25 * s, bx + s * 0.075, 0.115))
    # hair mass: crown over the top and down the temples, a receding front hairline
    top = [(dx - 0.47, 0.00), (dx - 0.52, -0.22), (dx - 0.42, -0.45), (dx - 0.18, -0.60), (dx + 0.10, -0.62), (dx + 0.38, -0.50), (dx + 0.51, -0.26), (dx + 0.48, 0.00)]
    inner = [(dx + 0.40 + fx * 0.3, -0.12), (dx + 0.34 + fx, -0.28), (dx + 0.16 + fx, -0.35), (dx + fx - 0.06, -0.37), (dx - 0.20 + fx, -0.34), (dx - 0.36 + fx * 0.6, -0.26), (dx - 0.40, -0.12)]
    d = P._smooth_open(top) + "L" + "L".join("%.4f,%.4f" % p for p in inner) + "Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    # side curls over the ears (a small roll each side)
    for sx in (-1, 1):
        cx = dx + sx * 0.46
        o.append('<ellipse cx="%.4f" cy="0.01" rx="0.085" ry="0.12" fill="%s" stroke="%s" stroke-width="0.018"/>' % (cx, g, k.ink))
        o.append('<path d="M%.4f,-0.05 Q%.4f,0.03 %.4f,0.07" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (cx - 0.03, cx + 0.02, cx - 0.02, k.c(col["dark"])))
    # strands and a few silver-grey streaks
    st = []
    for i in range(6):
        x = dx - 0.30 + 0.12 * i
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x + fx * 0.4, -0.36, x + 0.02, -0.50, x - 0.04, -0.60))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % ("".join(st), k.c(col["light"])))
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.58 %.4f,-0.56" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>' % (dx - 0.22, dx - 0.05, dx + 0.14, k.c(col["streak"])))
    o.append('</g>')
    CE._ext(k, C, ((dx - 0.56, -0.2), (dx + 0.56, -0.2), (dx, -0.64)))
    return "".join(o), (dx, -0.62)


def _wig_curls(k, col, dx, sx, y0, n, rx, ry, dy):
    o = []
    for i in range(n):
        cy = y0 + i * dy
        cx = dx + sx * (0.50 + 0.035 * math.sin(i * 1.7) - 0.02 * i)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, cy, rx, ry, k.c(col["base"]), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
                 % (cx - rx * 0.6, cy - ry * 0.2, cx, cy + ry * 0.4, cx + rx * 0.6, cy - ry * 0.2, k.c(col["dark"])))
    return "".join(o)


def _hat_wig11(k, C, yaw):
    """the town physician: a big powdered bob wig (puffed crown, a centre parting, two tiers of rolled curls each side, the face
    left clear) and, unless pose hat_off=1, a black tricorn with gold lace perched on top."""
    col = C["hat_colors"]
    wc = C["wig_colors"]
    dx = -0.03 * yaw
    fx = 0.10 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "wg", wc, x0=-0.7, x1=0.7, mid=0.34)
    # back curls first (they sit behind the head side)
    for sx in (-1, 1):
        o.append(_wig_curls(k, wc, dx, sx, -0.04, 4, 0.150, 0.100, 0.150))
    crown = [(dx - 0.52, 0.0), (dx - 0.62, -0.28), (dx - 0.50, -0.55), (dx - 0.20, -0.72), (dx + 0.14, -0.74), (dx + 0.46, -0.58), (dx + 0.62, -0.26), (dx + 0.52, 0.0)]
    hairline = [(dx + 0.38, -0.08), (dx + 0.34 + fx, -0.26), (dx + 0.16 + fx, -0.33), (dx + fx, -0.30), (dx - 0.16 + fx, -0.33), (dx - 0.34 + fx, -0.26), (dx - 0.38, -0.08)]
    d = P._smooth_open(crown) + "L" + "L".join("%.4f,%.4f" % p for p in hairline) + "Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    # rolled curls above the ears (the sausage curls)
    for sx in (-1, 1):
        for i, (cx, cy) in enumerate(((0.43, -0.22), (0.50, -0.02))):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.140" ry="0.095" fill="%s" stroke="%s" stroke-width="0.020"/>' % (dx + sx * cx, cy, g, k.ink))
    st = []
    for i in range(7):
        x = dx - 0.42 + 0.14 * i
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x * 0.9 + fx * 0.3, -0.33, x, -0.52, x * 1.15, -0.68))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % ("".join(st), k.c(wc["dark"])))
    o.append('<path d="M%.4f,-0.62 Q%.4f,-0.70 %.4f,-0.66" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.55"/>' % (dx - 0.30, dx - 0.12, dx + 0.12))
    # nape ribbon bow (black), a hint behind
    o.append('</g>')
    CE._ext(k, C, ((dx - 0.70, 0.2), (dx + 0.70, 0.2), (dx, -0.76)))
    top = (dx, -0.74)
    svg = "".join(o)
    if _POSE11["hat_off"] < 0.5 and C.get("tricorn11", True):
        ts, tt = C2._hat_tricorn(k, C, yaw)
        svg += '<g transform="translate(%.3f -0.14) scale(1.14)">%s</g>' % (-0.14 * dx, ts)
        top = (tt[0], tt[1] * 1.14 - 0.14)
        k.ext.append((dx, -0.86, 0.03))
        CE._ext(k, C, ((dx - 0.68, -0.62), (dx + 0.68, -0.62)))
    return svg, top


def _frill(k, pts, col, dark, r):
    """a gathered frill: a row of small puffs along the points."""
    o = []
    for (x, y) in pts:
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (x, y, r, k.c(col), k.ink))
    return "".join(o)


def _hat_mobcap11(k, C, yaw):
    """a linen mob cap: a puffed crown, a gathered frill round the face, a coloured ribbon band with a small bow; the maid's own
    hair (CAST hair colour) shows as a fringe and a wisp under the frill."""
    col = C["hat_colors"]
    hc = C["hair"]["color"]
    dx = -0.03 * yaw
    fx = 0.10 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "mc", col, x0=-0.56, x1=0.56, mid=0.34)
    # hair behind / at the sides (a bun puff at the back on the far side)
    s = -1 if yaw > 0 else 1
    o.append('<ellipse cx="%.4f" cy="-0.10" rx="0.10" ry="0.20" fill="%s" stroke="%s" stroke-width="0.016"/>' % (dx + s * 0.49, k.c(hc), k.ink))
    o.append('<ellipse cx="%.4f" cy="-0.10" rx="0.10" ry="0.20" fill="%s" stroke="%s" stroke-width="0.016"/>' % (dx - s * 0.49, k.c(hc), k.ink))
    # crown
    crown = [(dx - 0.52, -0.04), (dx - 0.58, -0.30), (dx - 0.40, -0.58), (dx - 0.06, -0.69), (dx + 0.30, -0.60), (dx + 0.56, -0.34), (dx + 0.52, -0.04)]
    d = P._smooth_open(crown) + "Q%.4f,%.4f %.4f,%.4f Z" % (dx + fx * 0.5, -0.22, dx - 0.52, -0.04)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M%.4f,-0.60 Q%.4f,-0.46 %.4f,-0.30 M%.4f,-0.62 Q%.4f,-0.46 %.4f,-0.30" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.25, dx - 0.22, dx - 0.18, dx + 0.12, dx + 0.17, dx + 0.20, k.c(col["dark"])))
    # hair fringe under the frill
    fr = []
    for i in range(7):
        x = dx + fx * 0.6 - 0.30 + 0.10 * i
        fr.append((x, -0.22 + 0.025 * math.sin(i * 1.9)))
    o.append('<path d="M%.4f,%.4f %s L%.4f,%.4f Z" fill="%s"/>' % (fr[0][0], -0.30, " ".join("L%.4f,%.4f" % p for p in fr), fr[-1][0], -0.30, k.c(hc)))
    # frill band following the brow line
    pts = []
    n = 12
    for i in range(n + 1):
        t = i / float(n)
        a = math.pi * (1.02 - 1.04 * t)
        x = dx + 0.51 * math.cos(a) * -1 * -1
        y = -0.03 - 0.33 * math.sin(a) * (0.6 + 0.4 * math.sin(a))
        pts.append((x * 1.0 + fx * 0.3 * math.sin(math.pi * t), y))
    o.append(_frill(k, pts, col["light"], col["dark"], 0.055))
    # ribbon band
    o.append('<path d="M%.4f,-0.37 Q%.4f,-0.45 %.4f,-0.37" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (dx - 0.50, dx, dx + 0.50, k.ink))
    o.append('<path d="M%.4f,-0.37 Q%.4f,-0.45 %.4f,-0.37" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (dx - 0.50, dx, dx + 0.50, k.c(col["band"])))
    bx = dx + 0.30 + 0.12 * yaw
    o.append('<path d="M%.4f,-0.42 l0.10,-0.06 l0.01,0.12 Z M%.4f,-0.42 l-0.10,-0.06 l-0.01,0.12 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (bx, bx, k.c(col["band"]), k.ink))
    o.append('<circle cx="%.4f" cy="-0.42" r="0.022" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx, k.c(col["band"]), k.ink))
    o.append('</g>')
    CE._ext(k, C, ((dx - 0.62, -0.1), (dx + 0.62, -0.1), (dx, -0.72)))
    return "".join(o), (dx, -0.69)


def _hat_bonnet11(k, C, yaw):
    """a round straw hat with a coloured ribbon (milkmaid2: golden hair in long locks at the sides; the farm hat: bare, tall crown)."""
    col = C["hat_colors"]
    hc = C["hair"]["color"]
    dx = -0.03 * yaw
    fx = 0.12 * yaw
    lock = C.get("locks", True)
    wide = C.get("brim", 0.78)
    tall = C.get("crown_h", 0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    s = -1 if yaw > 0 else 1
    if lock:
        for sx, ln in ((-1, 0.62), (1, 0.62)):
            far = 1.0 if sx == s else 0.78
            x0 = dx + sx * 0.47
            lk = [(x0, -0.22), (x0 + sx * 0.05, 0.02), (x0 + sx * 0.04, 0.30 * far), (x0 + sx * 0.02, ln * far)]
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.17" stroke-linecap="round"/>' % (P._smooth_open(lk), k.ink))
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.125" stroke-linecap="round"/>' % (P._smooth_open(lk), k.c(hc)))
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
                     % (P._smooth_open([(x0 - sx * 0.02, -0.10), (x0 + sx * 0.02, 0.18), (x0 + sx * 0.0, 0.44 * far)]), k.c(C["hair"].get("shine", "#fff0b0"))))
    # fringe of hair on the forehead
    o.append('<path d="M%.4f,-0.30 Q%.4f,-0.12 %.4f,-0.22 Q%.4f,-0.10 %.4f,-0.24 Q%.4f,-0.12 %.4f,-0.30 Z" fill="%s"/>'
             % (dx - 0.34 + fx * 0.4, dx - 0.2 + fx * 0.4, dx - 0.04 + fx * 0.4, dx + 0.12 + fx * 0.4, dx + 0.28 + fx * 0.4, dx + 0.36 + fx * 0.4, dx + 0.38 + fx * 0.4, k.c(hc))) if lock else None
    g = CE._gradient(k, "bn", col, x0=-0.8, x1=0.8, mid=0.34)
    yb = -0.34
    crown = [(dx - 0.40, yb), (dx - 0.38, yb - tall * 0.7), (dx - 0.22, yb - tall - 0.02), (dx, yb - tall - 0.04), (dx + 0.22, yb - tall - 0.02), (dx + 0.38, yb - tall * 0.7), (dx + 0.40, yb)]
    # brim behind the crown's lower part, then crown, then the ribbon
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="0.150" fill="%s" stroke="%s" stroke-width="0.026"/>' % (dx + fx * 0.5, yb + 0.01, wide, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (dx - wide * 0.8, yb + 0.03, dx, yb + 0.14, dx + wide * 0.8, yb + 0.03, k.c(col["dark"])))
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(crown), g, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.40" ry="0.060" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (dx, yb - tall - 0.01, k.c(col["dark"])))
    st = "".join("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f " % (dx + x * 0.9, yb + 0.0, dx + x, yb - tall * 0.5, dx + x * 0.8, yb - tall) for x in (-0.28, -0.14, 0.0, 0.14, 0.28))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.5"/>' % (st, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (dx - 0.40, yb - 0.02, dx, yb + 0.05, dx + 0.40, yb - 0.02, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.042" stroke-linecap="round"/>' % (dx - 0.40, yb - 0.02, dx, yb + 0.05, dx + 0.40, yb - 0.02, k.c(col["band"])))
    bx = dx - 0.28 - 0.1 * yaw
    o.append('<path d="M%.4f,%.4f l0.10,-0.07 l0.01,0.13 Z M%.4f,%.4f l-0.10,-0.07 l-0.01,0.13 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (bx, yb + 0.02, bx, yb + 0.02, k.c(col["band"]), k.ink))
    o.append('</g>')
    CE._ext(k, C, ((dx - wide - 0.02, yb), (dx + wide + 0.02, yb), (dx, yb - tall - 0.06)))
    return "".join(o), (dx, yb - tall - 0.04)


def _horn(k, sx, x0, y0):
    """one small cow horn rising from the head at (x0, y0), curving outward and up (sx = -1 / +1)."""
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
         % (x0 - sx * 0.07, y0 + 0.02, x0 - sx * 0.06, y0 - 0.10, x0 + sx * 0.06, y0 - 0.16, x0 + sx * 0.20, y0 - 0.24,
            x0 + sx * 0.12, y0 - 0.12, x0 + sx * 0.12, y0 - 0.02, x0 + sx * 0.07, y0 + 0.03))
    g = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(HORN["base"]), k.ink)
    g += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x0 + sx * 0.0, y0 - 0.02, x0 + sx * 0.02, y0 - 0.12, x0 + sx * 0.12, y0 - 0.19, k.c(HORN["light"]))
    g += '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s"/>' % (x0 + sx * 0.14, y0 - 0.20, x0 + sx * 0.20, y0 - 0.24, x0 + sx * 0.115, y0 - 0.13, k.c(HORN["tip"]))
    return g


def _cow_ear(k, sx, x0, y0, rot, col, inner):
    g = '<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (x0, y0, rot)
    d = "M0,-0.05 C%.4f,-0.16 %.4f,-0.14 %.4f,-0.02 C%.4f,0.10 %.4f,0.09 0,0.05 Z" % (sx * 0.12, sx * 0.28, sx * 0.30, sx * 0.28, sx * 0.12)
    g += '<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)
    g += '<path d="M%.4f,-0.01 C%.4f,-0.07 %.4f,-0.06 %.4f,-0.01 C%.4f,0.04 %.4f,0.04 %.4f,0.02 Z" fill="%s"/>' % (sx * 0.06, sx * 0.12, sx * 0.20, sx * 0.24, sx * 0.20, sx * 0.12, sx * 0.06, k.c(inner))
    return g + "</g>"


def _hat_messy11(k, C, yaw):
    """a boy's / man's own mop of hair (CAST hair colour): ragged tufts over the forehead, a cowlick on top.  Pose keys horns (0..1:
    two small cow horns grow out of the hair) and cow_ears (0..1: brown cow ears stick out of the sides) are the 'he'll grow horns'
    gag; they work on every member that wears this style."""
    hc = C["hair"]["color"]
    sh = C["hair"].get("shine", "#9a6a44")
    dk = C["hair"].get("dark", "#4a2c18")
    dx = -0.03 * yaw
    fx = 0.12 * yaw
    hn, ea = _POSE11["horns"], _POSE11["ears"]
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    if ea > 0.02:
        sc = _smooth(0.0, 0.7, ea)
        for sx in (-1, 1):
            far = 1.0 - 0.18 * abs(yaw) * (1 if sx * yaw > 0 else -0.5)
            o.append('<g transform="translate(%.4f 0.02) scale(%.3f %.3f)">%s</g>' % (dx + sx * 0.0, sc * far, sc, _cow_ear(k, sx, sx * 0.44, -0.14, -sx * 18, "#9a5a34", "#f2b0a2")))
    # the mop: lumpy cap with ragged tufts
    top = [(dx - 0.47, 0.02), (dx - 0.54, -0.22), (dx - 0.44, -0.48), (dx - 0.22, -0.62), (dx + 0.06, -0.60), (dx + 0.34, -0.54), (dx + 0.52, -0.30), (dx + 0.48, 0.02)]
    fr = []
    n = 9
    for i in range(n):
        t = i / float(n - 1)
        x = dx + 0.42 + fx * 0.4 - 0.84 * t
        y = -0.20 + (0.07 if i % 2 else -0.02) * (1 + 0.6 * math.sin(i * 2.3)) - 0.06 * math.sin(math.pi * t)
        fr.append((x, y))
    d = P._smooth_open(top) + "L" + "L".join("%.4f,%.4f" % p for p in fr) + "Z"
    g = CE._gradient(k, "ms", dict(light=sh, base=hc, dark=dk), x0=-0.55, x1=0.55, mid=0.4)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, g, k.ink))
    # tufts sticking up
    for (x, ang, ln) in ((-0.28, -35, 0.07), (-0.02, -8, 0.08), (0.24, 28, 0.07)):
        x += dx
        y = -0.58 + 0.03 * abs(x - dx)
        a = math.radians(ang - 90)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                 % (x - 0.05, y + 0.02, x - 0.06 + 0.5 * ln * math.cos(a), y + 0.5 * ln * math.sin(a), x + ln * math.cos(a), y + ln * math.sin(a),
                    x + 0.06 + 0.5 * ln * math.cos(a), y + 0.5 * ln * math.sin(a), x + 0.05, y + 0.02, k.c(hc), k.ink))
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.46 %.4f,-0.34 M%.4f,-0.55 Q%.4f,-0.48 %.4f,-0.40" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.18, dx - 0.22, dx - 0.26, dx + 0.14, dx + 0.12, dx + 0.14, k.c(sh)))
    if hn > 0.02:
        sc = _smooth(0.0, 0.7, hn) * 1.05
        for sx in (-1, 1):
            o.append('<g transform="translate(%.4f %.4f) scale(%.3f)">%s</g>' % (dx + sx * 0.0, -0.50, sc, _horn(k, sx, sx * 0.20, 0.0)))
    o.append('</g>')
    CE._ext(k, C, ((dx - 0.58, -0.3), (dx + 0.58, -0.3), (dx, -0.92 if hn > 0.02 else -0.68)))
    if ea > 0.02:
        CE._ext(k, C, ((dx - 0.84, -0.16), (dx + 0.84, -0.16)))
    if hn > 0.02:
        CE._ext(k, C, ((dx - 0.60, -0.92), (dx + 0.60, -0.92)))
    return "".join(o), (dx, -0.68 if hn < 0.02 else -0.90)


HATS11 = {"queue11": _hat_queue11, "wig11": _hat_wig11, "mobcap11": _hat_mobcap11, "bonnet11": _hat_bonnet11, "messy11": _hat_messy11}


# ============================================================================= costumes (torso-local)
def _cos_shirt11(k, C, m):
    """a countryman's / boy's linen shirt (CAST colors base) with an open laced neck, optional braces (colors brace), optional
    waistcoat (colors vest), a waistband over breeches (colors pants) and an optional patch."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = [CE._bowl(k, col["pants"], yB - 0.11, yB, dip=0.02)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
             % (X(-0.45, yB - 0.13) + X(0.0, yB - 0.10) + X(0.45, yB - 0.13) + (k.c(col.get("pants_d", "#5a4028")),)))
    sk = k.c(SKIN["base"])
    v = C.get("vest_on")
    if v:
        # waistcoat: a dark front panel with a V neck and buttons
        vc = k.c(col["vest"])
        for s in (-1, 1):
            pan = [X(s * 0.06, 0.40), X(s * 0.30, 0.38), X(s * 0.40, 0.70), X(s * 0.42, yB - 0.10), X(s * 0.02, yB - 0.08)]
            o.append(_poly(k, pan, vc, 0.014))
        o.append(_poly(k, [X(-0.14, 0.40), X(0.14, 0.40), X(0.0, 0.62)], k.c(col.get("base", "#efe6d2")), 0.012))
        for i in range(4):
            y = 0.74 + i * 0.12
            if y < yB - 0.14:
                o.append(_circ(X(0.0, y), 0.017, k.c(col.get("button", "#d8c080")), k, 0.007))
    else:
        # open laced neck
        o.append(_poly(k, [X(-0.12, 0.38), X(0.12, 0.38), X(0.0, 0.64)], sk, 0.012))
        for i in range(3):
            y = 0.45 + i * 0.065
            o.append(_ln([X(-0.05, y), X(0.05, y + 0.03)], k.c(col.get("lace", "#b08a5a")), 0.010))
            o.append(_ln([X(0.05, y), X(-0.05, y + 0.03)], k.c(col.get("lace", "#b08a5a")), 0.010))
    if col.get("brace"):
        bc = k.c(col["brace"])
        for s in (-1, 1):
            x0 = s * 0.20 * min(1.0, hw / 0.70) + (0.0)
            strap = [X(x0 - 0.045, 0.30), X(x0 + 0.045, 0.30), X(s * 0.26 + 0.045, yB - 0.10), X(s * 0.26 - 0.045, yB - 0.10)]
            o.append(_poly(k, strap, bc, 0.010))
            c = X(s * 0.26, yB - 0.12)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (c[0], c[1], k.c(col.get("brace_b", "#d8b868")), k.ink))
    if C.get("patch"):
        px = X(0.30, 0.95)
        o.append('<rect x="%.4f" y="%.4f" width="0.12" height="0.11" fill="%s" stroke="%s" stroke-width="0.008" stroke-dasharray="0.02 0.014"/>' % (px[0] - 0.06, px[1], k.c(C["patch"]), k.ink))
    return "".join(o), "", ""


def _stripe_fill(k, name, c1, c2, w=0.07):
    u = k.uid
    k.defs.append('<pattern id="%s_%s" patternUnits="userSpaceOnUse" width="%.4f" height="1" patternTransform="translate(-1.0 0)">'
                  '<rect x="0" y="-2" width="%.4f" height="5" fill="%s"/><rect x="%.4f" y="-2" width="%.4f" height="5" fill="%s"/></pattern>'
                  % (u, name, 2 * w, w, k.c(c1), w, w, k.c(c2)))
    return "url(#%s_%s)" % (u, name)


def _seated_skirt(k, C, m, X, yB, hw, col):
    """the skirt of a woman sitting on a low stool facing screen-right (the _sit() leg geometry): it spreads over the lap, drops over
    the knees and hangs behind to the stool; the apron lies over the lap."""
    fill = _stripe_fill(k, "ps", col["skirt_a"], col["skirt_b"], 0.055) if col.get("skirt_b") else k.c(col["skirt_a"])
    yt = yB - 0.12
    pts = [X(-hw * 0.95, yt), X(hw * 0.95, yt), X(0.62, yB + 0.06), X(0.90, yB + 0.20), X(0.92, yB + 0.50), X(0.60, yB + 0.58), X(0.0, yB + 0.50),
           X(-0.42, yB + 0.46), X(-hw - 0.14, yB + 0.30)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), fill, k.ink)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
             % (X(0.35, yB + 0.05) + X(0.55, yB + 0.30) + X(0.60, yB + 0.52) + X(-0.10, yB + 0.10) + X(-0.18, yB + 0.30) + X(-0.20, yB + 0.48) + (k.c(col.get("skirt_d", "#5a3a30")),)))
    if not C.get("shawl"):
        ap = [X(-0.18, yB - 0.10), X(0.30, yB - 0.10), X(0.74, yB + 0.14), X(0.80, yB + 0.40), X(0.36, yB + 0.30), X(-0.12, yB + 0.20)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(ap), k.c(col["apron"]), k.ink))
        o.append(_ln([X(0.2, yB + 0.02), X(0.58, yB + 0.30)], k.c(col["apron_d"]), 0.012, ' opacity="0.7"'))
    return "".join(o)


def _cos_gown11(k, C, m):
    """a countrywoman: a short gown (CAST colors base) with a white fichu crossed over the bodice, a striped petticoat skirt
    (colors skirt_a / skirt_b) falling over the legs to C['skirt_len'] below the torso, a linen apron (colors apron) with a bib, waist
    ties.  C['shawl'] (colour): a shawl over the shoulders crossed on the chest (the mother)."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    fich = k.c(col.get("fichu", "#f4eee0"))
    if C.get("shawl"):
        sh, shd = k.c(C["shawl"]), k.c(P._shade(C["shawl"], 0.72))
        for s in (-1, 1):
            o.append(_poly(k, [X(s * 0.02, 0.36), X(s * 0.50, 0.34), X(s * 0.46, 0.66), X(s * 0.05, yB - 0.02), X(s * 0.0, 0.80)], sh, 0.016))
        o.append(_ln([X(-0.40, 0.58), X(0.02, 0.80)], shd, 0.012, ' opacity="0.8"'))
        for i in range(5):
            f = X(-0.30 + 0.12 * i, yB - 0.02)
            o.append(_ln([X(-0.30 + 0.12 * i, yB - 0.05), (f[0] + 0.01, f[1] + 0.07)], shd, 0.012))
    else:
        for s in (-1, 1):
            o.append(_poly(k, [X(s * 0.02, 0.36), X(s * 0.30, 0.34), X(s * 0.22, 0.62), X(s * 0.03, 0.88)], fich, 0.014))
        o.append(_poly(k, [X(-0.10, 0.36), X(0.10, 0.36), X(0.0, 0.50)], k.c(SKIN["base"]), 0.010))
        # apron bib
        bib = [X(-0.17, 0.72), X(0.17, 0.72), X(0.24, yB - 0.04), X(-0.24, yB - 0.04)]
        o.append(_poly(k, bib, k.c(col["apron"]), 0.014))
        for s in (-1, 1):
            o.append(_ln([X(s * 0.15, 0.73), X(s * 0.20, 0.44)], k.c(col["apron_d"]), 0.020))
    inside = "".join(o)
    if _POSE11["seated"] and not _POSE11["sitfront"]:
        return inside, "", _seated_skirt(k, C, m, X, yB, hw, col)
    # skirt (petticoat) over the legs
    yt = yB - 0.10
    hem = yB + (0.50 if _POSE11["seated"] else C.get("skirt_len", 0.78))
    a = hw * 0.99
    b = hw + C.get("skirt_flare", 0.26)
    fill = _stripe_fill(k, "ps", col["skirt_a"], col["skirt_b"], 0.055) if col.get("skirt_b") else k.c(col["skirt_a"])
    ov = [C2._skirt(k, "gn", X, yt, a, hem, b, fill, sw=0.026, folds=((-0.14, yt + 0.2, -0.22, hem - 0.04), (0.16, yt + 0.2, 0.26, hem - 0.04)),
                    fold_col=k.c(col.get("skirt_d", "#5a3a30")))]
    if not C.get("shawl"):
        # the short gown: tails over the hips, opened at the front over the petticoat
        gc = "url(#%s_tg)" % k.uid
        for s in (-1, 1):
            tail = [X(s * 0.05, yB - 0.14), X(s * (hw * 0.99), yB - 0.14), X(s * (hw + 0.10), yB + 0.20), X(s * 0.18, yB + 0.16)]
            ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(tail), gc, k.ink))
        # apron skirt
        ap = [X(-0.24, yB - 0.06), X(0.24, yB - 0.06), X(0.40, hem - 0.10), X(-0.40, hem - 0.10)]
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(ap) if False else _poly_d(ap), k.c(col["apron"]), k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(-0.22, yB + 0.2) + X(-0.30, hem - 0.14) + (k.c(col["apron_d"]),)))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(0.22, yB + 0.2) + X(0.30, hem - 0.14) + (k.c(col["apron_d"]),)))
        ov.append(_ln([X(-0.30, yB - 0.08), X(0.30, yB - 0.08)], k.c(col["apron_d"]), 0.026))
        ov.append(_ln([X(0.30, yB - 0.08), X(0.38, yB + 0.10)], k.c(col["apron_d"]), 0.016))
    else:
        ov.append(_ln([X(0.0, yB - 0.1), X(0.04, hem - 0.01)], k.ink, 0.014))
    return inside, "", "".join(ov)


COSTUMES11 = {"shirt11": _cos_shirt11, "gown11": _cos_gown11}


# ============================================================================= face: pockmarks, fever flush
_POCK_SPOTS = ((-0.16, -0.20, 0.034), (0.02, -0.25, 0.030), (0.18, -0.17, 0.034), (-0.30, -0.02, 0.036), (0.30, 0.00, 0.036), (-0.24, 0.10, 0.032),
               (0.22, 0.12, 0.034), (-0.12, 0.20, 0.030), (0.10, 0.26, 0.030), (-0.34, 0.16, 0.026), (0.36, 0.14, 0.026), (0.0, 0.08, 0.028),
               (-0.05, 0.36, 0.026), (0.30, 0.28, 0.026), (-0.22, 0.30, 0.026), (0.06, -0.08, 0.026))


def _pocks(k, L, lev, yaw):
    cx = (L["xL"] + L["xR"]) / 2.0
    cy = L["ey"]
    sq = 1.0 - 0.15 * abs(yaw)
    n = int(round(len(_POCK_SPOTS) * lev))
    o = []
    for i, (x, y, r) in enumerate(_POCK_SPOTS[:n]):
        px, py = cx + x * sq, cy + y
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#e4a396" opacity="0.40"/>' % (px, py, r * 1.45))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (px, py, r * 0.88, k.c(POCK)))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#7a3430" opacity="0.8"/>' % (px + r * 0.12, py + r * 0.14, r * 0.45))
    return "".join(o)


def _flush(k, L, lev, yaw):
    cx = (L["xL"] + L["xR"]) / 2.0
    o = []
    for sx in (-1, 1):
        x = cx + sx * (0.25 - 0.03 * abs(yaw))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.15" ry="0.11" fill="#e8584c" opacity="%.3f"/>' % (x, L["ey"] + 0.15, 0.62 * lev))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.20" ry="0.07" fill="#e8584c" opacity="%.3f"/>' % (cx, L["ey"] - 0.22, 0.32 * lev))
    o.append('<path d="M%.4f,%.4f q0.05,-0.03 0.10,-0.01" fill="none" stroke="#fff6e8" stroke-width="0.016" stroke-linecap="round" opacity="%.3f"/>' % (cx - 0.12, L["ey"] - 0.27, 0.7 * lev))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O11["_face"](k, C, P_, white)
    if C is None or not C.get("_cast11"):
        return svg, L
    lev = _POSE11["pocks"]
    if lev is None:
        lev = _f(C.get("pocks11"), 0.0, 0.0, 1.0)
    over = ""
    if _POSE11["flush"] > 0.02:
        over += _flush(k, L, _POSE11["flush"], P_["yaw"])
    if lev > 0.02:
        over += _pocks(k, L, lev, P_["yaw"])
    return (over + svg), L          # under the eyes, brows and mouth


# ============================================================================= limbs: breeches, stockings, bare shins
def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O11["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if tail is None or C is None or not C.get("_cast11") or not C.get("leg11"):
        return out
    L = C["leg11"]
    c = P._limb_ctrl(S, E, H, kk)
    up = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (c[0] + c[1] + c[2] + c[3])
    lo = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (c[3] + c[4] + c[5] + c[6])
    # stocking / bare shin
    out += '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (lo, k.ink, w * 1.45)
    out += '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (lo, k.c(L["shin"]), w * 1.05)
    if L.get("garter"):
        mx, my = E
        dx, dy = H[0] - E[0], H[1] - E[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        out += ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                % (mx - nx * 0.05, my - ny * 0.05, mx + nx * 0.05, my + ny * 0.05, k.ink, mx - nx * 0.05, my - ny * 0.05, mx + nx * 0.05, my + ny * 0.05, k.c(L["garter"])))
    if L.get("buckle"):
        bx = H[0] + 0.045 * (1.0 if tail[0] >= H[0] else -1.0)
        out += ('<rect x="%.4f" y="%.4f" width="0.046" height="0.044" fill="none" stroke="%s" stroke-width="0.016"/><rect x="%.4f" y="%.4f" width="0.046" height="0.044" fill="none" stroke="%s" stroke-width="0.008"/>'
                % (bx - 0.023, H[1] - 0.018, k.ink, bx - 0.023, H[1] - 0.018, k.c(GOLD["base"])))
    return out


# ============================================================================= props held in the hand
NEW_PROPS11 = ("lancet", "jar", "notebook", "quill", "pail", "candle", "cane", "blister_hand")
NEW_TIP11 = {"lancet": 0.64, "jar": 0.0, "notebook": 0.0, "quill": 0.30, "pail": 0.42, "candle": 0.0, "cane": 1.52, "blister_hand": 0.56}


def _lancet_body(k):
    """Jenner's lancet along +x: tortoiseshell handle (-0.12 .. 0.20), a brass collar, a short steel blade (0.22 .. 0.64) to a point."""
    o = []
    gh = P._shade("#8a5a30", 1.0)
    o.append('<path d="M-0.13,-0.030 Q-0.17,0 -0.13,0.030 L0.20,0.034 L0.20,-0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c("#9a6a38"), k.ink))
    o.append('<path d="M-0.08,-0.012 L0.17,-0.016 M-0.06,0.014 L0.14,0.018" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c("#3a2414"))
    o.append('<rect x="0.19" y="-0.040" width="0.045" height="0.080" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(GOLD["base"]), k.ink))
    o.append('<path d="M0.234,-0.034 L0.50,-0.048 Q0.60,-0.02 0.645,0.0 Q0.56,0.040 0.234,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink))
    o.append('<path d="M0.26,-0.020 L0.52,-0.030 L0.60,-0.006" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(STEEL["light"]))
    return "".join(o)


def _glint(k, x, y, r, rot=0.0):
    pts = []
    for i in range(8):
        a = math.radians(rot + 45 * i)
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return '<path d="%s" fill="#fff8e0" opacity="0.95"/>' % _poly_d(pts)


def _jar_body(k):
    """a small glass specimen jar with a cork, a pale cloudy fluid at half height; centred on (0, 0), 0.22 wide x 0.30 high."""
    g = '%s_jg' % k.uid
    k.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (g, k.c(GLASS["light"]), k.c(GLASS["base"]), k.c(GLASS["dark"])))
    o = []
    o.append('<path d="M-0.075,-0.105 L-0.075,-0.145 L0.075,-0.145 L0.075,-0.105 Q0.115,-0.085 0.115,-0.04 L0.115,0.115 Q0.115,0.155 0.075,0.155 L-0.075,0.155 Q-0.115,0.155 -0.115,0.115 L-0.115,-0.04 Q-0.115,-0.085 -0.075,-0.105 Z" '
             'fill="url(#%s)" stroke="%s" stroke-width="0.022" stroke-linejoin="round" opacity="0.96"/>' % (g, k.ink))
    o.append('<path d="M-0.105,0.02 Q0,0.00 0.105,0.02 L0.105,0.115 Q0.105,0.142 0.075,0.142 L-0.075,0.142 Q-0.105,0.142 -0.105,0.115 Z" fill="%s" opacity="0.92"/>' % k.c("#f0e2a8"))
    o.append('<path d="M-0.098,0.03 Q0,0.012 0.098,0.03" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c("#fff6d0"))
    o.append('<rect x="-0.090" y="-0.185" width="0.180" height="0.052" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c("#c8935a"), k.ink))
    o.append('<path d="M-0.068,-0.040 L-0.068,0.095" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>')
    return "".join(o)


def _notebook_body(k):
    """a small pocket notebook held open towards the viewer (along +x from the hand): leather cover, cream pages with no text, a ribbon."""
    o = []
    o.append('<path d="M0.02,-0.20 L0.36,-0.20 L0.36,0.20 L0.02,0.20 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c("#7a4a2a"), k.ink))
    o.append('<path d="M0.045,-0.175 L0.19,-0.18 L0.19,0.175 L0.045,0.175 Z M0.20,-0.18 L0.335,-0.175 L0.335,0.175 L0.20,0.175 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#f6ecd2"), k.ink))
    o.append('<path d="M0.195,-0.18 L0.195,0.175" stroke="%s" stroke-width="0.012"/>' % k.c("#b8a478"))
    for y in (-0.10, -0.02, 0.06, 0.14):
        o.append('<path d="M0.062,%.3f L0.175,%.3f M0.215,%.3f L0.32,%.3f" stroke="%s" stroke-width="0.007" opacity="0.5"/>' % (y, y, y, y, k.c("#a89870")))
    o.append('<path d="M0.17,0.17 L0.17,0.30 L0.185,0.275 L0.20,0.30 L0.20,0.17 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#b83a3a"), k.ink))
    return "".join(o)


def _quill_body(k):
    """a goose quill, nib at +x (0.30), the feather behind the hand (-0.56 .. -0.04)."""
    o = []
    o.append('<path d="M-0.04,0 L0.26,0.0" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.04,0 L0.26,0.0" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c("#f2e8cc"))
    o.append('<path d="M0.24,-0.008 L0.31,0.012 L0.25,0.014 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#2a2026"), k.ink))
    vane = [(-0.06, 0.0), (-0.20, -0.075), (-0.40, -0.110), (-0.58, -0.080), (-0.50, -0.030), (-0.44, 0.015), (-0.26, 0.040)]
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_open(vane), k.c("#f4eddc"), k.ink))
    o.append('<path d="M-0.06,0 Q-0.30,-0.03 -0.55,-0.075" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % k.c("#c8b890"))
    for x in (-0.16, -0.26, -0.36, -0.46):
        o.append('<path d="M%.3f,%.3f l-0.02,-0.07 M%.3f,%.3f l-0.01,0.05" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (x, -0.014 - (-x - 0.16) * 0.09, x + 0.02, -0.02 - (-x - 0.16) * 0.09, k.c("#b8a880")))
    return "".join(o)


def _pail_body(k, milk=1.0):
    """a wooden milk pail hanging from the hand at (0, 0): the bail arcs from the rim, a stave body with two hoops, milk with foam."""
    wd = WOOD
    o = ['<path d="M-0.17,0.20 Q-0.15,-0.03 0,-0.02 Q0.15,-0.03 0.17,0.20" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.17,0.20 Q-0.15,-0.03 0,-0.02 Q0.15,-0.03 0.17,0.20" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c(WOOD["light"]))
    g = '%s_pg' % k.uid
    k.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="0.4" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (g, k.c(wd["light"]), k.c(wd["base"]), k.c(wd["dark"])))
    o.append('<path d="M-0.20,0.20 L0.20,0.20 L0.165,0.42 Q0,0.45 -0.165,0.42 Z" fill="url(#%s)" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink))
    for x in (-0.10, 0.0, 0.10):
        o.append('<path d="M%.3f,0.215 L%.3f,0.43" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % (x * 1.0, x * 0.82, k.c(wd["dark"])))
    for y, hw in ((0.265, 0.198), (0.37, 0.178)):
        o.append('<path d="M%.3f,%.3f Q0,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (-hw, y, y + 0.03, hw, y, k.ink))
        o.append('<path d="M%.3f,%.3f Q0,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (-hw, y, y + 0.03, hw, y, k.c("#6a4a30")))
    o.append('<ellipse cx="0" cy="0.20" rx="0.20" ry="0.045" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(wd["dark"]), k.ink))
    if milk > 0.05:
        o.append('<ellipse cx="0" cy="0.205" rx="0.17" ry="0.034" fill="%s"/>' % k.c("#f6efdc"))
        for (x, r) in ((-0.07, 0.03), (0.02, 0.036), (0.09, 0.026)):
            o.append('<circle cx="%.3f" cy="0.198" r="%.3f" fill="#fffaec" opacity="0.9"/>' % (x, r))
    return "".join(o)


def _candle_body(k, side, flame=1.0, t=0.0):
    """a brass chamberstick: the ring handle at the hand (0, 0), a round dish beside it, a short candle and a flame with a warm glow."""
    o = []
    cx = side * 0.20
    gid = "%s_cg" % k.uid
    k.defs.append('<radialGradient id="%s"><stop offset="0" stop-color="#ffd870" stop-opacity="0.75"/><stop offset="0.5" stop-color="#ffb040" stop-opacity="0.30"/><stop offset="1" stop-color="#ff9030" stop-opacity="0"/></radialGradient>' % gid)
    if flame > 0.05:
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="url(#%s)"/>' % (cx, -0.40, 0.55 * flame, gid))
    o.append('<ellipse cx="%.3f" cy="-0.01" rx="0.07" ry="0.07" fill="none" stroke="%s" stroke-width="0.030"/>' % (side * 0.02, k.ink))
    o.append('<ellipse cx="%.3f" cy="-0.01" rx="0.07" ry="0.07" fill="none" stroke="%s" stroke-width="0.016"/>' % (side * 0.02, k.c(GOLD["base"])))
    o.append('<path d="M%.3f,-0.01 L%.3f,-0.03" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (side * 0.08, cx - side * 0.10, k.ink))
    o.append('<ellipse cx="%.3f" cy="-0.02" rx="0.150" ry="0.050" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, k.c(GOLD["base"]), k.ink))
    o.append('<ellipse cx="%.3f" cy="-0.03" rx="0.120" ry="0.032" fill="%s"/>' % (cx, k.c(GOLD["dark"])))
    o.append('<rect x="%.3f" y="-0.105" width="0.075" height="0.080" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (cx - 0.0375, k.c(GOLD["base"]), k.ink))
    o.append('<rect x="%.3f" y="-0.340" width="0.060" height="0.240" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018"/>' % (cx - 0.03, k.c("#f4ead0"), k.ink))
    o.append('<path d="M%.3f,-0.32 L%.3f,-0.13" stroke="#fffaee" stroke-width="0.010" opacity="0.8"/>' % (cx - 0.015, cx - 0.015))
    if flame > 0.05:
        sw = 0.012 * math.sin(t * 6.283 * 2)
        fy = -0.340
        o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f Q%.3f,%.3f %.3f,%.3f Q%.3f,%.3f %.3f,%.3f Z" fill="#ff9a30" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (cx, fy + 0.005, cx - 0.055, fy - 0.040, cx + sw, fy - 0.140 * flame, cx + 0.055, fy - 0.040, cx, fy + 0.005, cx, fy + 0.005, cx, fy + 0.005, k.ink))
        o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f Q%.3f,%.3f %.3f,%.3f Z" fill="#ffe27a"/>' % (cx, fy, cx - 0.030, fy - 0.035, cx + sw * 0.6, fy - 0.100 * flame, cx + 0.030, fy - 0.035, cx, fy))
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.012" ry="0.026" fill="#fff6cc"/>' % (cx, fy - 0.025))
    return "".join(o)


def _cane_body(k):
    """a gentleman's cane along +x: a gold knob (-0.12 .. 0.02), a dark ebony shaft to 1.50, a gold ferrule to 1.52."""
    o = []
    o.append('<path d="M0.0,0 L1.46,0" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.0,0 L1.46,0" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.c("#4a2e24"))
    o.append('<path d="M0.12,-0.008 L1.40,-0.008" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % k.c("#8a6a58"))
    o.append('<path d="M1.40,-0.026 L1.52,-0.020 L1.52,0.020 L1.40,0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(GOLD["base"]), k.ink))
    o.append('<path d="M0.02,-0.03 L0.04,-0.045 L0.00,-0.045 Z" fill="none"/>')
    g = '%s_kg' % k.uid
    k.defs.append('<radialGradient id="%s" cx="0.35" cy="0.3" r="0.8"><stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>' % (g, k.c(GOLD["light"]), k.c(GOLD["base"]), k.c(GOLD["dark"])))
    o.append('<ellipse cx="-0.05" cy="0" rx="0.105" ry="0.088" fill="url(#%s)" stroke="%s" stroke-width="0.020"/>' % (g, k.ink))
    o.append('<path d="M0.04,-0.05 L0.04,0.05" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(GOLD["dark"]))
    o.append('<circle cx="-0.085" cy="-0.030" r="0.018" fill="#fff8d0" opacity="0.9"/>')
    return "".join(o)


def _blister_hand_body(k, hot=1.0):
    """an open hand, back to the viewer, fingers along +x, wrist at (0, 0): skin with a faint shade, and big comic cowpox blisters
    (a pale yellow dome in a red halo) on the back of the hand and at two knuckles.  hot 0..1 scales the redness."""
    o = []
    sk = k.c(SKIN["base"])
    shade = k.c(SKIN["dark"])
    palm = [(0.02, -0.15), (0.22, -0.18), (0.40, -0.17), (0.40, 0.17), (0.22, 0.18), (0.02, 0.15)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_closed(palm), sk, k.ink))
    # fingers (four) and thumb
    for i, (y, ln, ang) in enumerate(((-0.125, 0.25, -8), (-0.042, 0.29, -2), (0.042, 0.27, 3), (0.125, 0.21, 11))):
        o.append('<g transform="translate(0.36 %.3f) rotate(%d)"><rect x="-0.02" y="-0.034" width="%.3f" height="0.068" rx="0.034" fill="%s" stroke="%s" stroke-width="0.020"/></g>' % (y, ang, ln, sk, k.ink))
    o.append('<g transform="translate(0.10 -0.14) rotate(-52)"><rect x="-0.02" y="-0.038" width="0.25" height="0.076" rx="0.038" fill="%s" stroke="%s" stroke-width="0.020"/></g>' % (sk, k.ink))
    # re-cover the finger roots with palm fill so the fingers merge into the hand
    o.append('<path d="%s" fill="%s"/>' % (P._smooth_closed([(0.04, -0.13), (0.22, -0.16), (0.38, -0.15), (0.38, 0.15), (0.22, 0.16), (0.04, 0.13)]), sk))
    o.append('<path d="M0.40,-0.05 L0.56,-0.05 M0.40,0.045 L0.58,0.045" stroke="%s" stroke-width="0.008" opacity="0.5"/>' % shade)
    # blisters
    bl = ((0.12, -0.05, 0.050), (0.25, 0.07, 0.056), (0.31, -0.08, 0.044), (0.17, 0.10, 0.040), (0.44, 0.012, 0.036), (0.50, -0.09, 0.030))
    for (x, y, r) in bl:
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" opacity="%.2f"/>' % (x, y, r * 1.55, "#e5584a", 0.55 * hot))
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#f7e7a8" stroke="%s" stroke-width="0.016"/>' % (x, y, r, k.c("#a8483c")))
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#ffd98a" opacity="0.8"/>' % (x + r * 0.15, y + r * 0.22, r * 0.55))
        o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#ffffff" opacity="0.9"/>' % (x - r * 0.35, y - r * 0.38, r * 0.24))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS11:
        return _O11["_prop"](k, kind, H, ang, sc)
    key = C10.C8._side_key()
    an = C10.C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    tint = _POSE11["t"]

    def ext(pts):
        for (x, y) in pts:
            k.ext.append((H[0] + x * sc, H[1] + y * sc, 0.03))

    if kind == "pail":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _pail_body(k))
        ext(((-0.21, 0.20), (0.21, 0.20), (-0.17, 0.45), (0.17, 0.45), (0.0, -0.04)))
        tip = (H[0], H[1] + 0.45 * sc)
        an["pail_bottom_" + key] = tip
        an["pail_rim_" + key] = (H[0], H[1] + 0.20 * sc)
        return o, tip
    if kind == "jar":
        c = (H[0] + side * 0.02 * sc, H[1] - 0.10 * sc)
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (c[0], c[1], sc, _jar_body(k))
        for (x, y) in ((-0.12, -0.19), (0.12, -0.19), (-0.12, 0.16), (0.12, 0.16)):
            k.ext.append((c[0] + x * sc, c[1] + y * sc, 0.03))
        an["jar_" + key] = c
        return o, c
    if kind == "candle":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _candle_body(k, side, _f(_POSE11.get("flame"), 1.0, 0.0, 1.0), tint))
        ext(((side * 0.04, 0.05), (side * 0.36, 0.05), (side * 0.20, -0.50)))
        fl = (H[0] + side * 0.20 * sc, H[1] - 0.40 * sc)
        an["flame_" + key] = fl
        return o, fl
    # the rest follow the forearm / angle
    body = {"lancet": _lancet_body, "notebook": _notebook_body, "quill": _quill_body, "cane": _cane_body, "blister_hand": _blister_hand_body}[kind]
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body(k))
    ext_pts = {"lancet": ((-0.15, 0.0), (0.66, 0.0)), "notebook": ((0.0, -0.22), (0.38, -0.22), (0.38, 0.22), (0.0, 0.32)), "quill": ((-0.60, -0.12), (0.32, 0.02)),
               "cane": ((-0.14, -0.1), (1.55, 0.03)), "blister_hand": ((0.0, -0.2), (0.60, -0.2), (0.60, 0.2), (0.0, 0.2))}[kind]
    for e in ext_pts:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tipx = NEW_TIP11[kind]
    tx, ty = _rot(tipx * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[kind + "_" + key] = tip
    if kind == "lancet":
        gx, gy = _rot(0.62 * sc, -0.0, ang)
        o += _glint(k, H[0] + gx, H[1] + gy, 0.085 * sc, rot=ang)
    return o, tip


# ============================================================================= stool and yoke (figure level)
def _stool_svg(k, cx, ytop, ybot, w):
    """a three-legged milking stool seen from the front and a little above: a round seat at ytop (the sitter's hips rest on it),
    splayed legs to ybot."""
    o = []
    wd = WOOD
    for lx, tx in ((-0.30, -0.36), (0.30, 0.36), (0.0, 0.05)):
        d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (cx + lx * w * 0.8 - 0.035, ytop + 0.04, cx + lx * w * 0.8 + 0.035, ytop + 0.04, cx + tx * w + 0.030, ybot, cx + tx * w - 0.030, ybot)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(wd["dark"] if lx == 0.0 else wd["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (cx - 0.3 * w, ytop + (ybot - ytop) * 0.55, cx + 0.3 * w, ytop + (ybot - ytop) * 0.55, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.024"/>' % (cx, ytop + 0.045, w * 0.5, 0.085, k.c(wd["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (cx, ytop + 0.025, w * 0.44, 0.055, k.c(wd["light"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (cx - w * 0.30, ytop + 0.03, cx, ytop + 0.06, cx + w * 0.3, ytop + 0.03, k.c(wd["dark"])))
    bb = (cx - w * 0.5 - 0.04, ytop - 0.05, cx + w * 0.5 + 0.04, ybot + 0.02)
    return "".join(o), bb


def _yoke_svg(k, cx, y, half, rope, milk=1.0):
    """a shoulder yoke at height y: a curved wooden bar (notch at the neck), a rope at each end and a milk pail on each rope."""
    o = []
    wd = WOOD
    bar = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (cx - half, y - 0.03, cx - half * 0.4, y + 0.10, cx, y + 0.05, cx + half * 0.4, y + 0.10, cx + half, y - 0.03)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.125" stroke-linecap="round"/>' % (bar, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.090" stroke-linecap="round"/>' % (bar, k.c(wd["base"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8" transform="translate(0 -0.025)"/>' % (bar, k.c(wd["light"])))
    pails = []
    for sx in (-1, 1):
        x = cx + sx * (half - 0.04)
        yy = y - 0.01
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (x, yy, x, yy + rope, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x, yy, x, yy + rope, k.c("#d2b98a")))
        pails.append('<g transform="translate(%.4f %.4f)">%s</g>' % (x, yy + rope - 0.02, _pail_body(k, milk)))
    return "".join(o), "".join(pails), (cx - half - 0.12, y - 0.1, cx + half + 0.12, y + rope + 0.46)


def figure(cast_name, pose=None, uid="p"):
    if cast_name == COW:
        return cow_figure(pose, uid)
    f = _O11["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    if cast_name in NEW11:
        a2 = dict(f["anchors"])
        for sd in ("r", "l"):
            s_, e_ = a2["shoulder_" + sd], a2["elbow_" + sd]
            a2["upper_arm_" + sd] = (s_[0] + 0.8 * (e_[0] - s_[0]), s_[1] + 0.8 * (e_[1] - s_[1]))
        f = dict(f, anchors=a2)
    st = _f(pose.get("stool"), 0.0, 0.0, 1.0)
    yk = _f(pose.get("yoke"), 0.0, 0.0, 1.0)
    if st < 0.5 and yk < 0.5:
        return f
    k = P._Ctx(uid + "x", P.INK, None)
    tn = pose.get("tint")
    if P._is_hex(tn):
        k.tint = P._rgb(tn.lstrip("#"))
    behind, front, extra = [], [], []
    b = list(f["bbox"])
    an = dict(f["anchors"])
    if st >= 0.5:
        w = _f(pose.get("stool_w"), 0.95, 0.5, 2.0)
        drop = _f(pose.get("stool_drop"), 0.10, -0.5, 1.0)
        ytop = an["hip"][1] + drop
        s, bb = _stool_svg(k, an["hip"][0] + _f(pose.get("stool_dx"), 0.0, -2.0, 2.0), ytop, f["feet_y"] + 0.01, w)
        behind.append(s)
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["stool_top"] = (an["hip"][0], ytop)
    if yk >= 0.5:
        half = _f(pose.get("yoke_w"), 0.86, 0.4, 1.6)
        rope = _f(pose.get("yoke_rope"), 0.50, 0.2, 1.2)
        ys = (an["shoulder_r"][1] + an["shoulder_l"][1]) / 2.0 + 0.02
        cx = (an["shoulder_r"][0] + an["shoulder_l"][0]) / 2.0
        s, pails, bb = _yoke_svg(k, cx, ys, half, rope, _f(pose.get("milk"), 1.0, 0.0, 1.0))
        front.append(pails + s)
        hr = P.HAND_R * (_num(P.CAST[cast_name].get("limb_w"), P.LW) / P.LW) ** 0.75
        for hh in (an["hand_r"], an["hand_l"]):
            if abs(hh[1] - ys) < 0.22:
                front.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#b7a9b3" opacity="0.7"/>'
                             % (hh[0], hh[1], hr, P.INK, hh[0] - 0.34 * hr, hh[1] - 0.40 * hr, 0.15 * hr, 0.095 * hr))
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["yoke_l"] = (cx - half, ys)
        an["yoke_r"] = (cx + half, ys)
        an["pail_l"] = (cx - half + 0.04, ys + rope + 0.20)
        an["pail_r"] = (cx + half - 0.04, ys + rope + 0.20)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + "".join(behind) + f["svg"] + "".join(front), bbox=tuple(b), anchors=an)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    pk = g("pocks")
    _POSE11["pocks"] = None if pk is None else _f(pk, 0.0, 0.0, 1.0)
    _POSE11["flush"] = _f(g("flush"), 0.0, 0.0, 1.0)
    _POSE11["sitfront"] = _f(g("sit_front"), 0.0, 0.0, 1.0) >= 0.5
    _POSE11["seated"] = _f(g("stool"), 0.0, 0.0, 1.0) >= 0.5 or _f(g("seated"), 0.0, 0.0, 1.0) >= 0.5
    _POSE11["horns"] = _f(g("horns"), 0.0, 0.0, 1.0)
    _POSE11["ears"] = _f(g("cow_ears"), 0.0, 0.0, 1.0)
    _POSE11["hat_off"] = _f(g("hat_off"), 0.0, 0.0, 1.0)
    _POSE11["flame"] = _f(g("flame"), 1.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE11["t"] = t if math.isfinite(t) else 0.0
    return _O11["_norm"](C, pose)


if HERE not in sys.path:
    sys.path.insert(0, HERE)
from cow11 import cow_figure, cow_svg, COW_CAST  # noqa: E402,F401  (the 2D cow, own module)


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast11=True)
_BOY = CE.PROFILE_PEAR
_WOMAN = ((0.62, 0.02), (0.92, 0.1), (1.0, 0.25), (0.93, 0.45), (0.8, 0.62), (0.82, 0.78), (0.86, 0.9), (0.68, 0.97), (0.38, 1.0))
_KIDP = ((0.66, 0.02), (0.93, 0.11), (1.0, 0.27), (1.0, 0.5), (0.99, 0.7), (0.95, 0.85), (0.76, 0.96), (0.42, 1.0))
TRICORN = dict(base="#2b2530", dark="#19141c", light="#4a4350", shine="#9a94a8", lace="#e2b442", cockade="#b8302a", brass="#fff0a8")
MOB = dict(light="#fffaf0", base="#f3ecda", dark="#c9bd9f", band="#c8503c", shine="#ffffff")
_SH = dict(color="#e8dec8", cuff="#efe6d2", dark="#c4b69a", len=0.55, roll=True, w=0.15)


def _gown(base, ska, skb, apron="#f2ead8", fichu="#f6f0e2", skd="#5a3a30"):
    return dict(base=base, dark=P._shade(base, 0.7), skirt_a=ska, skirt_b=skb, skirt_d=skd, apron=apron, apron_d="#cbbd9c", fichu=fichu, pants=ska)


NEW_CAST11 = {
    # Edward Jenner, ~47: country gentleman doctor.  Dark blue tailcoat, buff waistcoat, white cravat, buff breeches, white stockings,
    # black buckled shoes; his own grey-brown hair swept back and tied in a queue; a kind, clever face.
    "jenner": dict(
        _FLAGS, build="regular", seed=11.6,
        torso_w=0.84, torso_h=1.02, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.30, 0.48), arm=0.74, hip_x=0.16, leg=1.24, stance=0.06, wide=0.26, limb_w=0.058,
        eye_y=0.020, brow="stroke", brow_th=0.050, mouth="smile", moustache=False, smirk_side=1, cheeks="#eaa090", age_lines=True,
        hat="newsboy", hat_style="queue11", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#b8a898", base="#8c7c6e", dark="#5e5246", streak="#d8d0c6", ribbon="#1e1a22"),
        hair=dict(color="#8c7c6e", front=0.03, grow=0.05),
        costume="frock7", neck="cravat", coat_len=0.56, coat_flare=0.12, double=False, vest_buttons=5,
        sleeve=dict(color="#2d4a7a", dark="#1a2c4c", cuff="#f4efe2", len=0.84, w=0.17),
        shorts=dict(color="#dcc79a", cuff="#dcc79a", dark="#b4a074", len=0.52, w=0.13),
        boots=dict(color="#241e22", cuff="#241e22", h=0.05, toe=0.15),
        leg11=dict(breeches="#dcc79a", shin="#f4f0e6", garter="#c9a860", buckle=True),
        colors=dict(base="#2d4a7a", dark="#1a2c4c", lapel="#223a62", button="#e2b442", vest="#e4c78e", vest_b="#b89858", shirt="#f6f0e4", collar="#f6f0e4",
                    tie="#f6f0e4", tie_dark="#d8d0bc", pants="#dcc79a"),
    ),
    # James Phipps, 8: gardener's son.  Linen shirt, braces, short brown breeches, bare shins, boots, messy brown hair.  ~2.3 D tall.
    "james": dict(
        _FLAGS, build="boy", seed=8.8,
        torso_w=0.62, torso_h=0.76, profile=_KIDP, shift_pow=1.0,
        shoulder=(0.235, 0.5), arm=0.58, hip_x=0.14, leg=0.72, stance=0.07, wide=0.23, limb_w=0.052,
        eye_y=0.055, brow="dome", brow_th=0.036, mouth="smile", moustache=False, smirk_side=1, cheeks="#f4a090", freckles=True,
        hat="newsboy", hat_style="messy11", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#b0784a", base="#7a4a2a", dark="#4a2c18"),
        hair=dict(color="#7a4a2a", front=0.02, grow=0.04, shine="#b0784a", dark="#4a2c18"),
        costume="shirt11", patch="#a8884e",
        sleeve=dict(color="#efe6d2", cuff="#e0d4ba", dark="#c4b69a", len=0.26, roll=True, w=0.14),
        shorts=dict(color="#8a6a48", cuff="#8a6a48", dark="#5e4630", len=0.50, w=0.12),
        boots=dict(color="#6a4428", cuff="#8a5c38", h=0.11, soft=True, toe=0.13),
        leg11=dict(breeches="#8a6a48", shin="#f3cdb6"),
        colors=dict(base="#efe6d2", dark="#c4b69a", pants="#8a6a48", pants_d="#5e4630", brace="#8a5a38", brace_b="#d8b868", lace="#b08a5a"),
    ),
    # Sarah Nelmes, the milkmaid: mob cap, short gown, striped petticoat, apron, rolled sleeves, rosy CLEAR smooth face.
    "sarah": dict(
        _FLAGS, build="slim", seed=71.9,
        torso_w=0.62, torso_h=0.92, profile=_WOMAN, shift_pow=1.0,
        shoulder=(0.235, 0.52), arm=0.72, hip_x=0.14, leg=1.14, stance=0.05, wide=0.24, limb_w=0.055,
        eye_y=0.040, brow="stroke", brow_th=0.034, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f08878", lashes=True,
        hat="newsboy", hat_style="mobcap11", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(MOB, band="#c8503c"),
        hair=dict(color="#b8683a", front=0.0, grow=0.0),
        costume="gown11", skirt_len=0.72, skirt_flare=0.24,
        sleeve=dict(color="#4f77a8", cuff="#f2ead8", dark="#34527a", len=0.55, roll=True, w=0.15),
        shorts=dict(color="#efe6d6", cuff="#efe6d6", dark="#8a3a2a", len=0.9, w=0.13),
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.06, toe=0.11),
        colors=_gown("#4f77a8", "#d9604a", "#f1e6cf"),
    ),
    "milkmaid2": dict(
        _FLAGS, build="slim", seed=24.3,
        torso_w=0.64, torso_h=0.92, profile=_WOMAN, shift_pow=1.0,
        shoulder=(0.235, 0.52), arm=0.72, hip_x=0.14, leg=1.18, stance=0.05, wide=0.24, limb_w=0.055,
        eye_y=0.045, brow="stroke", brow_th=0.032, mouth="smile", moustache=False, smirk_side=1, cheeks="#f4968a", lashes=True,
        hat="newsboy", hat_style="bonnet11", hat_tilt=5.0, ear_pencil=False, locks=True, brim=0.80, crown_h=0.28,
        hat_colors=dict(light="#f8e4a0", base="#e4c26e", dark="#b0904a", band="#4a78a8"),
        hair=dict(color="#e8bf5a", front=0.0, grow=0.0, shine="#fff0a8"),
        costume="gown11", skirt_len=0.74, skirt_flare=0.26,
        sleeve=dict(color="#5f8f5a", cuff="#f2ead8", dark="#3e6a3e", len=0.55, roll=True, w=0.15),
        shorts=dict(color="#efe6d6", cuff="#efe6d6", dark="#2a4268", len=0.9, w=0.13),
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.06, toe=0.11),
        colors=_gown("#5f8f5a", "#4a6a98", "#efe6d2"),
    ),
    # the mocker: pompous town physician.  Stout, powdered bob wig, plum velvet coat with gold buttons, gold-headed cane, tricorn,
    # ruddy face, double chin.
    "towndoc": dict(
        _FLAGS, build="stout", seed=64.4,
        torso_w=1.46, torso_h=1.20, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.78, hip_x=0.20, leg=1.18, stance=0.07, wide=0.32, limb_w=0.068,
        eye_y=0.000, brow="stroke", brow_th=0.080, mouth="frown", moustache=False, smirk_side=1, cheeks="#ea6250", chins=True, age_lines=True,
        hat="newsboy", hat_style="wig11", hat_tilt=-3.0, ear_pencil=False, tricorn11=True,
        hat_colors=dict(TRICORN), wig_colors=dict(light="#ffffff", base="#f1ece6", dark="#c2bac8"),
        hair=dict(color="#f1ece6", front=0.0, grow=0.0),
        costume="frock7", neck="cravat", coat_len=0.54, coat_flare=0.12, double=True, chain=True, vest_buttons=5,
        sleeve=dict(color="#7c2c4c", dark="#4a1630", cuff="#e2b442", len=0.84, w=0.21),
        shorts=dict(color="#7c2c4c", cuff="#7c2c4c", dark="#4a1630", len=0.52, w=0.15),
        boots=dict(color="#1c161a", cuff="#1c161a", h=0.05, toe=0.17),
        leg11=dict(breeches="#7c2c4c", shin="#f4f0e8", garter="#e2b442", buckle=True),
        colors=dict(base="#7c2c4c", dark="#4a1630", lapel="#5c1e38", button="#e2b442", vest="#ecd9a0", vest_b="#c9a54a", shirt="#f8f2e6", collar="#f8f2e6",
                    tie="#f8f2e6", tie_dark="#d8d0bc", pants="#7c2c4c"),
    ),
    # James's mother: plain working woman, cap, shawl.
    "mother": dict(
        _FLAGS, build="slim", seed=52.7,
        torso_w=0.66, torso_h=0.94, profile=_WOMAN, shift_pow=1.0,
        shoulder=(0.24, 0.52), arm=0.72, hip_x=0.14, leg=1.12, stance=0.05, wide=0.24, limb_w=0.056,
        eye_y=0.045, brow="stroke", brow_th=0.034, mouth="smile", moustache=False, smirk_side=-1, cheeks="#e8a090", age_lines=True,
        hat="newsboy", hat_style="mobcap11", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#f6f0e4", base="#e6decb", dark="#bfb398", band="#8a6a58", shine="#ffffff"),
        hair=dict(color="#8a7868", front=0.0, grow=0.0),
        costume="gown11", shawl="#a8685a", skirt_len=0.80, skirt_flare=0.28,
        sleeve=dict(color="#7a6a58", cuff="#e6decb", dark="#544838", len=0.84, w=0.15),
        shorts=dict(color="#d8cdb8", cuff="#d8cdb8", dark="#3a3028", len=0.9, w=0.13),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.06, toe=0.11),
        colors=_gown("#7a6a58", "#6a5a4a", None),
    ),
    # villagers: a, b, c pockmarked (smallpox scars, comic and clear), d, e plain.
    "villager_a": dict(
        _FLAGS, build="regular", seed=33.1, pocks11=1.0,
        torso_w=0.86, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.31, 0.48), arm=0.74, hip_x=0.15, leg=1.16, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.060, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.8, smirk_side=-1, cheeks="#e4907c",
        hat="newsboy", hat_style="flatcap", hat_tilt=3.0, ear_pencil=False,
        hat_colors=dict(light="#8a8272", base="#6a6254", dark="#3e382e", shine="#aaa292", dot="#4a4438", visor="#3e382e"),
        hair=dict(color="#5a4636", front=0.05, grow=0.12),
        costume="shirt11", vest_on=True, patch=None,
        sleeve=dict(color="#e8dec8", cuff="#efe6d2", dark="#c4b69a", len=0.55, roll=True, w=0.16),
        shorts=dict(color="#7a6a50", cuff="#7a6a50", dark="#4e4230", len=0.52, w=0.13),
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.12, toe=0.14),
        leg11=dict(breeches="#7a6a50", shin="#d8cdb4"),
        colors=dict(base="#e8dec8", dark="#c4b69a", pants="#7a6a50", pants_d="#4e4230", vest="#7a5a3a", button="#d8c080", lace="#b08a5a", moustache="#5a4636", moustache_l="#8a6a4a"),
    ),
    "villager_b": dict(
        _FLAGS, build="slim", seed=18.2, pocks11=1.0,
        torso_w=0.70, torso_h=0.94, profile=_WOMAN, shift_pow=1.0,
        shoulder=(0.25, 0.52), arm=0.72, hip_x=0.14, leg=1.14, stance=0.05, wide=0.24, limb_w=0.056,
        eye_y=0.045, brow="stroke", brow_th=0.036, mouth="smile", moustache=False, smirk_side=1, cheeks="#e89a8a",
        hat="newsboy", hat_style="mobcap11", hat_tilt=4.0, ear_pencil=False,
        hat_colors=dict(MOB, band="#4f77a8"),
        hair=dict(color="#6a4a36", front=0.0, grow=0.0),
        costume="gown11", skirt_len=0.74, skirt_flare=0.28,
        sleeve=dict(color="#c48a3a", cuff="#f2ead8", dark="#8a5a22", len=0.84, w=0.15),
        shorts=dict(color="#efe6d6", cuff="#efe6d6", dark="#4a2a20", len=0.9, w=0.13),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.06, toe=0.11),
        colors=_gown("#c48a3a", "#8a4a3a", "#e8d9b8"),
    ),
    "villager_c": dict(
        _FLAGS, build="regular", seed=47.5, pocks11=1.0,
        torso_w=1.06, torso_h=0.96, profile=C2.PROFILE_ROUND, shift_pow=1.1,
        shoulder=(0.36, 0.46), arm=0.72, hip_x=0.17, leg=0.98, stance=0.06, wide=0.26, limb_w=0.064,
        eye_y=0.010, brow="stroke", brow_th=0.066, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.95, smirk_side=1, cheeks="#e48a78", age_lines=True,
        hat="newsboy", hat_style="baldtuft", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(base="#9a948c", dark="#6a645c", light="#c8c2ba"),
        hair=dict(color="#aaa49c", front=0.09, grow=0.20),
        costume="shirt11", vest_on=True,
        sleeve=dict(color="#d8ccb0", cuff="#e8dec6", dark="#b0a284", len=0.55, roll=True, w=0.18),
        shorts=dict(color="#5a6a4a", cuff="#5a6a4a", dark="#38442c", len=0.52, w=0.14),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.12, toe=0.15),
        leg11=dict(breeches="#5a6a4a", shin="#d8d0bc"),
        colors=dict(base="#d8ccb0", dark="#b0a284", pants="#5a6a4a", pants_d="#38442c", vest="#6a7a52", button="#d8c080", lace="#b08a5a", moustache="#aaa49c", moustache_l="#d8d2ca"),
    ),
    "villager_d": dict(
        _FLAGS, build="slim", seed=29.9,
        torso_w=0.66, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15, leg=1.30, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.030, brow="stroke", brow_th=0.050, mouth="smile", moustache=False, smirk_side=-1, cheeks="#eca090",
        hat="newsboy", hat_style="bonnet11", hat_tilt=-6.0, ear_pencil=False, locks=False, brim=0.66, crown_h=0.36,
        hat_colors=dict(light="#ecd48a", base="#cfae58", dark="#9c7c38", band="#7a4a2a"),
        hair=dict(color="#5a3a26", front=0.06, grow=0.12),
        costume="shirt11",
        sleeve=dict(color="#e2d8bc", cuff="#efe6d2", dark="#bcae8e", len=0.50, roll=True, w=0.14),
        shorts=dict(color="#6a5a8a", cuff="#6a5a8a", dark="#3e3458", len=0.52, w=0.12),
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.12, toe=0.14),
        leg11=dict(breeches="#6a5a8a", shin="#d8cdb4"),
        colors=dict(base="#e2d8bc", dark="#bcae8e", pants="#6a5a8a", pants_d="#3e3458", brace="#b8503a", brace_b="#d8b868", lace="#b08a5a"),
    ),
    "villager_e": dict(
        _FLAGS, build="slim", seed=61.2,
        torso_w=0.60, torso_h=0.88, profile=_WOMAN, shift_pow=1.0,
        shoulder=(0.23, 0.52), arm=0.70, hip_x=0.13, leg=1.06, stance=0.05, wide=0.23, limb_w=0.054,
        eye_y=0.045, brow="stroke", brow_th=0.032, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f0988a", lashes=True,
        hat="newsboy", hat_style="mobcap11", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(MOB, band="#6a9a6a"),
        hair=dict(color="#3a2a22", front=0.0, grow=0.0),
        costume="gown11", skirt_len=0.70, skirt_flare=0.24,
        sleeve=dict(color="#5a8a8a", cuff="#f2ead8", dark="#38605e", len=0.84, w=0.14),
        shorts=dict(color="#efe6d6", cuff="#efe6d6", dark="#522a34", len=0.9, w=0.13),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.06, toe=0.11),
        colors=_gown("#5a8a8a", "#8a4a5a", "#e8d9b8"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1) in D; filled in by the canvas check (see test_cast11.py)
CANVAS11 = {
    "jenner": (-1.75, -4.5, 1.75, 0.125),
    "james": (-1.25, -3.75, 1.25, 0.125),
    "sarah": (-1.75, -4.3125, 1.75, 0.125),
    "milkmaid2": (-1.5, -4.375, 1.5, 0.125),
    "towndoc": (-2.75, -5.375, 2.75, 0.125),
    "mother": (-1.5, -4.3125, 1.5, 0.125),
    "villager_a": (-1.375, -4.375, 1.375, 0.125),
    "villager_b": (-1.5, -4.3125, 1.5, 0.125),
    "villager_c": (-1.375, -4.1875, 1.375, 0.125),
    "villager_d": (-1.25, -4.5625, 1.25, 0.125),
    "villager_e": (-1.25, -4.1875, 1.25, 0.125),
    "blossom": (-4.5625, -3.1875, 4.5625, 0.125),
}
CANVAS11_LIE = {"james": (-1.5, -1.5, 1.5, 0.25)}          # lying in bed (pose lie=90 / -90): pass to Actor.build
CANVAS11_YOKE = {"sarah": (-1.875, -3.5625, 1.875, 0.125), "milkmaid2": (-1.875, -3.5625, 1.875, 0.125)}   # carrying the yoke + pails


SIT = dict(crouch=0.45, foot_r=(0.60, 1.9), foot_l=(0.42, 1.9), knee_r=1, knee_l=1)


def _sit(cast, base_y=None, fx=0.58):
    """legs for sitting on a low stool (feet on the floor under the knees); y of the soles follows the member's hip."""
    hip = {"james": 1.08, "sarah": 1.24, "milkmaid2": 1.24, "mother": 1.26}.get(cast, 1.25)
    fy = hip + (0.62 if cast != "james" else 0.55)
    return dict(crouch=0.45, foot_r=(fx + 0.04, fy), foot_l=(fx - 0.14, fy), knee_r=1, knee_l=1)


def _sit_front(cast):
    """sitting on the stool seen from the front / three-quarter (knees forward to the viewer): the feet under the hips, a short skirt (pose sit_front=1)."""
    hip = {"sarah": 1.24, "milkmaid2": 1.24}.get(cast, 1.25)
    fy = hip + 0.62
    return dict(crouch=0.45, foot_r=(0.17, fy), foot_l=(-0.13, fy), knee_r=0.4, knee_l=-0.4)


def _story():
    S, M = {}, {}
    J, B, SA, M2, T, MO = "jenner", "james", "sarah", "milkmaid2", "towndoc", "mother"
    # ------------------------------------------------------------------ Jenner
    S["jenner_neutral"] = (J, dict(yaw=0.30, expr="neutral", mouth="smile", arm_r="down", arm_l="down", legs="stand"))
    M["jenner_neutral"] = dict(note="standing, kind and calm, arms at his sides")
    S["jenner_explain"] = (J, dict(yaw=0.40, expr="talking", mouth="flat", head_roll=-3, arm_r=dict(hand=(0.78, 0.30), bend=-0.7, shape="open"),
                                   arm_l=dict(hand=(-0.40, 1.00), bend=0.5), legs="stand"))
    M["jenner_explain"] = dict(lipsync=True, note="explaining: right hand open and out, left hand low; set mouth = talk_mouth(g) on quoted lines, else flat")
    S["jenner_lancet_up"] = (J, dict(yaw=0.35, pitch=-0.15, expr="determined", mouth="smile", arm_r=dict(hand=(0.50, -0.05), bend=-0.7, stretch=1.0),
                                     prop_r=dict(type="lancet", angle=-62), arm_l=dict(hand=(-0.40, 1.00), bend=0.5), legs="stand"))
    M["jenner_lancet_up"] = dict(note="the lancet held up beside his head (glint at the tip); anchor lancet_r = the blade tip")
    S["jenner_jar_up"] = (J, dict(yaw=0.35, pitch=-0.10, expr="happy", arm_r=dict(hand=(0.55, 0.20), bend=-0.7), prop_r="jar",
                                  arm_l=dict(hand=(-0.40, 1.00), bend=0.5), legs="stand"))
    M["jenner_jar_up"] = dict(note="holds the small glass jar up to the light; anchor jar_r = jar centre")
    S["jenner_scratch_arm"] = (J, dict(yaw=0.70, pitch=0.35, lean=9, expr="determined", mouth="smile", gaze=(0.8, 0.5), head_dy=0.0,
                                       arm_r=dict(hand=(0.62, 0.98), bend=0.2, stretch=1.0), prop_r=dict(type="lancet", angle=60),
                                       arm_l=dict(hand=(0.30, 0.88), bend=0.4, shape="open"), legs=dict(preset="step", stride=0.2)))
    M["jenner_scratch_arm"] = dict(note="bends towards the boy (screen-right) and scratches his upper arm: put anchor lancet_r (blade tip) on James's "
                                        "anchor upper_arm_l (James faces screen-left in james_sit_sleeve). Move arm_r['hand'] to land it exactly")
    S["jenner_examine_hand"] = (J, dict(yaw=0.65, pitch=0.45, lean=10, expr="determined", mouth="flat", gaze=(0.9, 0.7),
                                        arm_r=dict(hand=(0.66, 0.95), bend=0.1, shape="open"), arm_l=dict(hand=(0.50, 1.02), bend=0.3, shape="open"),
                                        legs="stand"))
    M["jenner_examine_hand"] = dict(note="peering at the milkmaid's hand (screen-right), both hands cupping it; her hand_r (blister_hand) goes between his hands")
    S["jenner_write"] = (J, dict(yaw=0.30, pitch=0.45, expr="determined", mouth="flat", gaze=(0.3, 0.9),
                                 arm_l=dict(hand=(-0.40, 0.95), bend=0.4, stretch=1.0), prop_l=dict(type="notebook", angle=-28),
                                 arm_r=dict(hand=(0.30, 1.00), bend=0.5), prop_r=dict(type="quill", angle=155), legs="stand"))
    M["jenner_write"] = dict(note="writes in his notebook (screen-left hand) with a quill (right hand); anchor quill_r = the nib. No text on the pages")
    S["jenner_proud"] = (J, dict(yaw=0.25, pitch=-0.30, expr="happy", mouth="smile", head_roll=-3, arm_r=dict(hand=(0.30, 0.62), bend=0.7), arm_l="akimbo",
                                 legs="stand"))
    M["jenner_proud"] = dict(note="proud smile, chin up, one hand on his waistcoat, the other on his hip")
    S["jenner_wince"] = (J, dict(yaw=0.20, pitch=0.2, lean=-8, head_roll=6, expr="worried", mouth="clench", sweat=0.6, squash=(1.02, 0.97),
                                 arm_r=dict(hand=(0.62, 0.40), bend=-0.3, shape="open"), arm_l=dict(hand=(-0.55, 0.50), bend=-0.2, shape="open"), legs="narrow"))
    M["jenner_wince"] = dict(note="wince: sucks air through his teeth, hands half up (the day-nine fever worry)")
    S["jenner_walk"] = (J, cycle(J, 0.30, "walk"))
    M["jenner_walk"] = dict(note="one walk frame (phase 0.30); animate with cycle('jenner', frame / 28.0, 'walk')")
    # ------------------------------------------------------------------ James
    S["james_sit_sleeve"] = (B, dict(yaw=-0.45, expr="determined", mouth="flat", gaze=(-0.8, 0.2), stool=1, legs=_sit(B),
                                     arm_l=dict(hand=(-0.20, 1.02), bend=0.6), arm_r=dict(hand=(0.30, 1.10), bend=0.6)))
    M["james_sit_sleeve"] = dict(note="sits on the stool (stool=1) facing screen-left towards Jenner, sleeve rolled to the shoulder; the upper arm to scratch is "
                                      "anchor upper_arm_l. Mirror (mirror=True) for the other side")
    S["james_brave"] = (B, dict(yaw=-0.45, pitch=-0.2, expr="determined", mouth="smile", fx=[], stool=1, legs=_sit(B), head_roll=-3,
                                arm_l=dict(hand=(-0.25, 1.00), bend=0.6), arm_r=dict(hand=(0.10, 1.00), bend=0.6)))
    M["james_brave"] = dict(note="brave: chin up, lips pressed, steady")
    S["james_scared"] = (B, dict(yaw=-0.30, pitch=0.35, expr="worried", sweat=0.5, stool=1, legs=_sit(B), squash=(1.0, 0.97),
                                 arm_l=dict(hand=(-0.05, 0.98), bend=0.7), arm_r=dict(hand=(0.08, 0.98), bend=0.7)))
    M["james_scared"] = dict(note="scared: hunched, worried, a drop of sweat, hands clenched in his lap")
    S["james_in_bed"] = (B, dict(yaw=0.0, expr="sad", flush=1.0, sweat=1.0, lie=90, head_roll=72, t=0.3, arm_r=dict(hand=(0.18, 0.90), bend=0.6),
                                 arm_l=dict(hand=(-0.18, 0.90), bend=0.6), legs="narrow"))
    M["james_in_bed"] = dict(note="sick in bed on his back (lie=90, head to screen-left; for the other side lie=-90 AND head_roll=-72; head_roll=72 keeps the face upright like a head propped on a pillow), flushed cheeks, sweat drops; anchor feet = middle of the body on "
                                  "the mattress line. Canvas CANVAS11_LIE")
    S["james_jump_up"] = (B, dict(yaw=0.0, pitch=-0.2, expr="excited", arm_r="reach_up", arm_l="reach_up", legs=dict(preset="wide", lift_r=0.9, lift_l=0.9), squash=(0.97, 1.05)))
    M["james_jump_up"] = dict(note="jumps out of bed: arms up, both feet off the floor (raise the sprite by hand, or use it as the mid-jump key)")
    S["james_play"] = (B, dict(yaw=0.35, expr="grinning", head_roll=6, arm_r=dict(hand=(0.60, 0.20), bend=-0.7, shape="open"), arm_l=dict(hand=(-0.60, 0.80), bend=0.3, shape="open"),
                               legs=dict(preset="step", stride=0.5, lift_l=0.5)))
    M["james_play"] = dict(note="playing in the garden: a skip with one arm up")
    S["james_run"] = (B, cycle(B, 0.30, "run"))
    M["james_run"] = dict(note="one run frame (phase 0.30); animate with cycle('james', frame / 16.0, 'run')")
    S["james_laugh"] = (B, dict(yaw=0.2, expr="laughing", head_roll=10, arm_r=dict(hand=(0.25, 1.00), bend=0.7), arm_l=dict(hand=(-0.25, 1.00), bend=0.7), legs="wide", fx=["tears"], t=0.3))
    M["james_laugh"] = dict(note="laughing, hands on his tummy")
    S["james_horns"] = (B, dict(yaw=0.20, pitch=-0.1, expr="grinning", horns=1.0, cow_ears=1.0, head_roll=-4, arm_r="hip", arm_l="hip", legs="stand"))
    M["james_horns"] = dict(gag=True, note="GAG: the mocker's imagined 'he will grow horns': small cow horns + brown cow ears. Pose keys horns / cow_ears (0..1) work on any james pose")
    # ------------------------------------------------------------------ Sarah and milkmaid2
    for (n, c, nm) in ((SA, SA, "sarah"), (M2, M2, "milkmaid2")):
        S[nm + "_milk"] = (c, dict(yaw=0.50, pitch=0.35, lean=8, expr="happy", mouth="smile", gaze=(0.8, 0.8), stool=1, sit_front=1, legs=_sit_front(c),
                                   arm_r=dict(hand=(0.54, 1.18), bend=0.3, shape="ball"), arm_l=dict(hand=(0.34, 1.24), bend=0.3), t=0.3))
        M[nm + "_milk"] = dict(note="milking on a stool (stool=1, sit_front=1: three-quarter, knees to the viewer), head and hands towards screen-right, hands at udder height (about 0.65 D above the floor). "
                                    "Plant her feet on the cow's anchor milker_feet (hands then reach the teats teat_l / teat_r; pail on pail_spot). Pace the hands: arm_r / arm_l hand y 1.20 / 1.26, +-0.06 in antiphase")
        S[nm + "_smile"] = (c, dict(yaw=0.25, expr="happy", mouth="smile", arm_r=dict(hand=(0.14, 1.02), bend=0.7), arm_l=dict(hand=(-0.14, 1.02), bend=0.7), legs="stand"))
        M[nm + "_smile"] = dict(note="smiling, hands folded in front of the apron")
        S[nm + "_yoke"] = (c, dict(yaw=0.35, expr="happy", yoke=1, arm_r=dict(hand=(0.66, 0.62), bend=0.3), arm_l=dict(hand=(-0.66, 0.62), bend=0.3), legs=dict(preset="step", stride=0.25)))
        M[nm + "_yoke"] = dict(note="carries two milk pails on a yoke (yoke=1): anchors pail_l / pail_r; yoke_w, yoke_rope, milk keys. Canvas CANVAS11_YOKE")
    S["sarah_show_hand"] = (SA, dict(yaw=0.30, expr="happy", mouth="smile", gaze=(0.8, 0.3), arm_r=dict(hand=(0.74, 0.74), bend=-0.2), prop_r=dict(type="blister_hand", angle=-58, scale=1.25),
                                     arm_l=dict(hand=(-0.14, 1.02), bend=0.7), legs="stand"))
    M["sarah_show_hand"] = dict(note="holds out her right hand, back to us, with the cowpox blisters (prop blister_hand: six big pale blisters in red halos); anchor blister_hand_r = the fingertips. "
                                    "Her face stays clear and smooth")
    S["sarah_show_hand_close"] = (SA, dict(yaw=0.0, expr="worried", mouth="smile", arm_r=dict(hand=(0.55, 0.62), bend=-0.2), prop_r=dict(type="blister_hand", angle=-90, scale=1.3),
                                           arm_l=dict(hand=(-0.14, 1.02), bend=0.7), legs="stand"))
    M["sarah_show_hand_close"] = dict(note="the same, hand straight up and scaled 1.3 for the close reveal (blisters readable at phone size)")
    S["sarah_walk"] = (SA, dict(cycle(SA, 0.30, "walk"), yoke=1))
    M["sarah_walk"] = dict(note="walk frame with the yoke; animate cycle('sarah', f / 28.0, 'walk', base=dict(yoke=1, ...)), arms=None")
    # ------------------------------------------------------------------ the town doctor
    S["towndoc_laugh_big"] = (T, dict(yaw=0.15, pitch=-0.8, lean=-8, expr="laughing", head_roll=-6, fx=["tears"], t=0.3,
                                      arm_r=dict(hand=(0.40, 1.08), bend=0.7), arm_l=dict(hand=(-0.40, 1.08), bend=0.7), legs="wide"))
    M["towndoc_laugh_big"] = dict(note="BIG belly laugh: head thrown back, mouth open wide, tears, hands on the belly (fixed laughing mouth)")
    S["towndoc_point_mock"] = (T, dict(yaw=0.50, pitch=-0.3, expr="smug", mouth="flat", arm_r="point", arm_l=dict(hand=(-0.60, 1.0), bend=0.4), prop_l=dict(type="cane", angle=96), legs="stand"))
    M["towndoc_point_mock"] = dict(lipsync=True, note="points and mocks (screen-right), cane in the other hand. lip-sync: mouth = talk_mouth(g) on his quoted lines, else flat")
    S["towndoc_point_door"] = (T, dict(yaw=0.55, pitch=-0.25, expr="angry", mouth="flat", head_roll=-3, arm_r=dict(hand=(1.05, 0.30), bend=-0.2, shape="point"),
                                       arm_l=dict(hand=(-0.60, 1.0), bend=0.4), prop_l=dict(type="cane", angle=96), legs=dict(preset="step", stride=0.2)))
    M["towndoc_point_door"] = dict(lipsync=True, note="accusing finger out to the door (screen-right), cane planted. lip-sync as above")
    S["towndoc_scoff_crossed"] = (T, dict(yaw=0.25, pitch=-0.35, expr="unimpressed", mouth="flat", head_roll=4,
                                          arm_r=dict(hand=(-0.55, 0.92), bend=0.6, layer="front"), arm_l=dict(hand=(0.55, 0.98), bend=0.6, layer="front"), legs="stand"))
    M["towndoc_scoff_crossed"] = dict(note="scoffs with his arms crossed, nose in the air")
    S["towndoc_shocked"] = (T, dict(yaw=0.20, pitch=0.1, expr="shocked", sweat=0.6, squash=(0.98, 1.03), arm_r=dict(hand=(0.78, 0.50), bend=-0.5, shape="open"),
                                    arm_l=dict(hand=(-0.78, 0.50), bend=-0.5, shape="open"), legs="wide"))
    M["towndoc_shocked"] = dict(note="shocked: jaw dropped, sweat, hands up")
    S["towndoc_sleeve_sheepish"] = (T, dict(yaw=0.30, pitch=0.35, expr="worried", mouth="smirk", fx=["blush"], sweat=0.4, head_roll=5, hat_off=0.0,
                                            arm_l=dict(hand=(-0.12, 0.98), bend=0.7), arm_r=dict(hand=(-0.34, 1.06), bend=0.6, shape="open", layer="front"), legs="narrow"))
    M["towndoc_sleeve_sheepish"] = dict(note="ENDING: sheepishly rolling up his sleeve in the vaccination queue (right hand at the left cuff), blushing")
    S["towndoc_walk"] = (T, cycle(T, 0.30, "walk"))
    M["towndoc_walk"] = dict(note="one walk frame; animate with cycle('towndoc', f / 28.0, 'walk')")
    # ------------------------------------------------------------------ the mother
    S["mother_sit_worried"] = (MO, dict(yaw=0.40, pitch=0.25, expr="worried", stool=1, legs=_sit(MO), gaze=(0.7, 0.6),
                                        arm_r=dict(hand=(0.40, 1.12), bend=0.4), arm_l=dict(hand=(0.22, 1.16), bend=0.5)))
    M["mother_sit_worried"] = dict(note="sits (stool=1) by the bed, hands clasped, worried; yaw 0.4 = looks screen-right (mirror for the other side)")
    S["mother_sit_relieved"] = (MO, dict(yaw=0.40, pitch=-0.05, expr="happy", mouth="smile", stool=1, legs=_sit(MO), head_roll=4, gaze=(0.7, 0.2),
                                         arm_r=dict(hand=(0.28, 0.70), bend=0.7), arm_l=dict(hand=(0.14, 0.82), bend=0.7)))
    M["mother_sit_relieved"] = dict(note="relieved: a smile, one hand to her heart")
    S["mother_stand_worried"] = (MO, dict(yaw=0.20, pitch=0.2, expr="worried", arm_r=dict(hand=(0.14, 1.00), bend=0.7), arm_l=dict(hand=(-0.14, 1.00), bend=0.7), legs="stand"))
    M["mother_stand_worried"] = dict(note="standing, wringing her hands")
    # ------------------------------------------------------------------ villagers
    for nm, st in (("villager_a", 0), ("villager_b", 0), ("villager_c", 0), ("villager_d", 1), ("villager_e", 1)):
        pk = "pocked" if nm in ("villager_a", "villager_b", "villager_c") else "plain"
        S[nm + "_laugh"] = (nm, dict(yaw=0.30, pitch=-0.4, expr="laughing", head_roll=-8, lean=-4, arm_r=dict(hand=(0.30, 0.95), bend=0.7), arm_l=dict(hand=(-0.50, 0.50), bend=-0.2),
                                     legs="wide", fx=["tears"], t=0.3))
        M[nm + "_laugh"] = dict(note="%s villager laughing, head back, hand on the belly" % pk)
        S[nm + "_point"] = (nm, dict(yaw=0.50, pitch=-0.1, expr="grinning", head_roll=-4, arm_r="point", arm_l=dict(hand=(-0.20, 1.0), bend=0.5), legs="stand"))
        M[nm + "_point"] = dict(note="%s villager pointing and jeering (screen-right)" % pk)
        S[nm + "_whisper"] = (nm, dict(yaw=0.65, pitch=0.1, expr="smirk", head_roll=8, lean=6, gaze=(0.9, 0.0), arm_r=dict(hand=(0.28, 0.20), bend=-0.5, shape="open"),
                                       arm_l=dict(hand=(-0.20, 1.0), bend=0.5), legs="stand"))
        M[nm + "_whisper"] = dict(note="%s villager whispering behind a hand to a neighbour (screen-right)" % pk)
        S[nm + "_queue"] = (nm, dict(yaw=-0.30 if st == 0 else 0.30, expr="neutral", mouth="smile" if pk == "plain" else "flat", arm_r="down", arm_l=dict(hand=(-0.2, 1.0), bend=0.5),
                                     legs="stand"))
        M[nm + "_queue"] = dict(note="%s villager standing patiently in the vaccination queue (mirror for the other direction)" % pk)
    # ------------------------------------------------------------------ the cow
    S["blossom_stand"] = (COW, dict(head_turn=0.0, ear=0.0, tail=0.1, blink=0))
    S["blossom_chew"] = (COW, dict(head_turn=0.0, chew=0.25, tail=0.2))
    S["blossom_turn_head"] = (COW, dict(head_turn=1.0, tail=0.2, chew=0.0, chew_amp=0.3))
    S["blossom_ear_flick"] = (COW, dict(head_turn=0.1, ear=1.0, tail=0.3))
    S["blossom_tail_swish"] = (COW, dict(head_turn=0.0, tail=0.9, chew=0.5))
    for n_, t_ in (("blossom_stand", "standing, head down and forward, udder visible"), ("blossom_chew", "chewing: jaw and muzzle move once per unit of the chew phase (pass frame / 12)"),
                   ("blossom_turn_head", "head turned down and back to look at the milkmaid"), ("blossom_ear_flick", "near ear flicked"),
                   ("blossom_tail_swish", "tail swung back, chewing")):
        M[n_] = dict(note=t_)
    return S, M


STORY11, STORY11_META = {}, {}


def register():
    if getattr(P, "_cast11_registered", False):
        CE.register_stage()
        if not STORY11:
            s, m = _story()
            STORY11.update(s)
            STORY11_META.update(m)
        return
    for name in ("_face", "_norm", "_ink_limb", "_prop", "figure"):
        _O11[name] = getattr(P, name)
    P._face = _face
    P._norm = _norm
    P._ink_limb = _ink_limb
    P._prop = _prop
    P.figure = figure
    CE.COSTUMES.update(COSTUMES11)
    CE.HATS.update(HATS11)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS11 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP11)
    for n, c in NEW_CAST11.items():
        P.CAST[n] = c
    P.CAST[COW] = COW_CAST
    CE.CANVAS.update(CANVAS11)
    P._cast11_registered = True
    s, m = _story()
    STORY11.update(s)
    STORY11_META.update(m)
    P.STORY.update(STORY11)
    CE.register_stage()


register()
