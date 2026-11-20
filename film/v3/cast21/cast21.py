#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast21.py -- the cast of film 21 ("ไอ้ชาวนาบนเนิน", the Battle of Stirling Bridge, 11 Sept 1297) for the v2 puppet,
as an extension module on top of cast10 (the same chaining pattern as cast17).

    import sys; sys.path.insert(0, ".../v3/cast21"); import cast21     # registers on import (idempotent); import it BEFORE sprites
    import puppet                                                      # same module object, now with the new members
    cast, pose = cast21.STORY21["cressingham_laughing"]
    f = puppet.figure(cast, pose, "f")
    h = puppet.figure("horse", dict(cast21.horse_pose(0.3, "walk", "red")), "h")     # side-view horse card
    r = puppet.figure("knight_a_mtd", dict(cast21.STORY21["knight_a_mounted"][1], gait=0.3), "r")   # rider parented to the horse

Nothing in v2/puppet or v3/cast .. cast10 is edited.  Entries are added to their tables and puppet helpers wrapped on top of
cast10's wrappers (each falls through for everything it does not handle, so every earlier member draws exactly as before):
    cast_ext.COSTUMES  surcoat21 (mail + surcoat: plain / chequy / lion / chevron), robe21 (the treasurer), gambeson21 (quilted
                       footman), tunic21 (Scots knee-length tunic, optional mail + sword on the back)
    cast_ext.HATS      bascinet21, greathelm21, furcap21, ironcap21, coif21, longhair21 (kettlehat / bare7 are reused)
    puppet._prop       spear21 (long), shield21 (round), horn21 (cow horn), sword21, coin21
    puppet._face       puffed cheeks (puff21), grass stalk (stalk21), splutter spray (spit21)
    puppet._norm       the pose keys of this module
    puppet.figure      horse cards, mounted riders, swimming crop cards, floating helmets, colour variants
See API.md.
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
import cast8 as C8      # noqa: E402
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_O21 = {}
_POSE21 = {"puff": 0.0, "stalk": 0.0, "spit": 0.0, "shield": "ochre", "sheath": None, "wet": 0.0, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= palettes (mid-dark: they must read on green, grey rock, teal)
STEEL = dict(light="#e4e9ee", base="#a4aeba", dark="#5e6874", deep="#343c46", shine="#ffffff")
IRON = dict(light="#b8bcc0", base="#7c8288", dark="#464c52", shine="#e8eaec")
GOLD = dict(light="#ffe58a", base="#e8b52e", dark="#a8771a")
WOOD = dict(light="#c8945a", base="#8e5e32", dark="#573518")
CRIMSON = "#a8232c"
FUR = dict(light="#f4eee2", base="#d9d0c0", dark="#9d9484")
LEATHER = dict(light="#a87040", base="#7a4c28", dark="#4a2c16")
LONGB = dict(light="#8a5a34", base="#5e3a1e", dark="#3a2210")

KEEP_FLAGS = dict(C10._FLAGS, _cast21=True)


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _lin(k, name, c0, c1, c2, x0, y0, x1, y1):
    return C10._lin(k, name, c0, c1, c2, x0, y0, x1, y1)


def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


# ============================================================================= hats (head frame, head centre (0, 0), brow about y -0.20)
def _frame(k, outer, inner, fill, sw=0.026):
    d = P._smooth_open(outer) + " L" + P._smooth_open(inner)[1:] + " Z"
    return '<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (d, fill, k.ink, sw), d


def _hat_coif21(k, C, yaw):
    """a mail coif: mail over the head and down to the shoulders, the face in an oval opening."""
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    outer = [(-0.57 + dx, 0.66), (-0.62 + dx, 0.10), (-0.56 + dx, -0.30), (-0.30 + dx, -0.56), (dx, -0.60), (0.30 + dx, -0.56),
             (0.56 + dx, -0.30), (0.62 + dx, 0.10), (0.57 + dx, 0.66)]
    inner = [(0.38 + fx, 0.42), (0.43 + fx, 0.04), (0.38 + fx, -0.22), (fx, -0.32), (-0.38 + fx, -0.22), (-0.43 + fx, 0.04), (-0.38 + fx, 0.42)]
    s, d = _frame(k, outer, inner, C6._mail_pattern(k), 0.028)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"], s]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" opacity="0.55"/>' % (P._smooth_open(inner), k.c(STEEL["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.44, -0.30, dx - 0.36, -0.50, dx - 0.10, -0.56, k.c(STEEL["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.64, 0.1), (dx + 0.64, 0.1), (dx, -0.62), (dx, 0.68)))
    return "".join(o), (dx, -0.60)


def _hat_bascinet21(k, C, yaw):
    """an open-face bascinet: a rounded-pointed steel dome with a brow band over a mail aventail that falls to the shoulders."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.12 * yaw
    outer = [(-0.58 + dx, 0.64), (-0.61 + dx, 0.06), (-0.54 + dx, -0.30), (dx, -0.50), (0.54 + dx, -0.30), (0.61 + dx, 0.06), (0.58 + dx, 0.64)]
    inner = [(0.39 + fx, 0.34), (0.43 + fx, 0.02), (0.37 + fx, -0.24), (fx, -0.31), (-0.37 + fx, -0.24), (-0.43 + fx, 0.02), (-0.39 + fx, 0.34)]
    s, d = _frame(k, outer, inner, C6._mail_pattern(k), 0.026)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"], s]
    g = CE._gradient(k, "ht", col, x0=-0.5, x1=0.5, mid=0.30)
    yb = -0.20
    tipx = dx + 0.06 * yaw
    dome = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.50, yb, dx - 0.54, yb - 0.30, tipx - 0.20, yb - 0.50, tipx, yb - 0.66, tipx + 0.20, yb - 0.50, dx + 0.54, yb - 0.30, dx + 0.50, yb,
        dx, yb + 0.06, dx - 0.50, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.38, yb - 0.04, dx - 0.34, yb - 0.34, tipx - 0.08, yb - 0.56, k.c(col["shine"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.51, yb - 0.07, dx, yb - 0.01, dx + 0.51, yb - 0.07, dx + 0.51, yb + 0.02, dx, yb + 0.08, dx - 0.51, yb + 0.02)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (band, k.c(col["dark"]), k.ink))
    for x in (-0.36, -0.18, 0.0, 0.18, 0.36):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s" stroke="%s" stroke-width="0.005"/>' % (dx + x, yb + 0.005 + 0.03 * (x / 0.4) ** 2 * 0.0 - 0.012 * (1 - (x / 0.4) ** 2), k.c(col["light"]), k.ink))
    if col.get("plume"):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
                 % (tipx - 0.03, yb - 0.64, tipx - 0.20, yb - 0.86, tipx - 0.36, yb - 0.74, tipx - 0.16, yb - 0.72, tipx + 0.03, yb - 0.62, k.c(col["plume"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.62, 0.0), (dx + 0.62, 0.0), (tipx, yb - 0.68), (dx, 0.66)))
    return "".join(o), (tipx, yb - 0.66)


def _hat_greathelm21(k, C, yaw):
    """a great helm, flat-topped: a steel pot over the head with cheek plates and a brow bar; the front is cut away so the
    face stays readable (a face-open variant; the closed helm with slits would hide every expression)."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.12 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.6, x1=0.6, mid=0.28)
    top, bot = -0.68, 0.54
    hw = 0.60
    outer = [(-hw + dx, bot), (-hw - 0.02 + dx, 0.0), (-hw + dx, top + 0.10), (-hw * 0.6 + dx, top + 0.01), (dx, top - 0.01), (hw * 0.6 + dx, top + 0.01),
             (hw + dx, top + 0.10), (hw + 0.02 + dx, 0.0), (hw + dx, bot)]
    inner = [(0.40 + fx, 0.44), (0.44 + fx, 0.10), (0.40 + fx, -0.18), (fx, -0.24), (-0.40 + fx, -0.18), (-0.44 + fx, 0.10), (-0.40 + fx, 0.44)]
    s, d = _frame(k, outer, inner, g, 0.030)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    if col.get("plume"):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                 % (dx - 0.34, top, dx - 0.30, top - 0.34, dx + 0.02, top - 0.40, dx + 0.34, top - 0.30, dx + 0.34, top, k.c(col["plume"]), k.ink))
    o.append(s)
    # crown plate seam, brow bar and rivets
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.8"/>'
             % (dx - hw + 0.04, top + 0.16, dx, top + 0.24, dx + hw - 0.04, top + 0.16, k.c(col["dark"])))
    bar = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - hw, -0.24, dx, -0.30, dx + hw, -0.24, dx + hw, -0.12, dx, -0.19, dx - hw, -0.12)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (bar, k.c(col["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (dx, top, dx, -0.28, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (dx, top + 0.01, dx, -0.28, k.c(col["base"])))
    for x in (-0.48, -0.32, 0.32, 0.48):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s" stroke="%s" stroke-width="0.005"/>' % (dx + x, -0.21, k.c(col["light"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.50, top + 0.14, dx - 0.52, -0.40, dx - 0.50, 0.30, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - hw - 0.03, 0.0), (dx + hw + 0.03, 0.0), (dx, top - (0.42 if col.get("plume") else 0.04)), (dx, bot + 0.02)))
    return "".join(o), (dx, top - 0.02)


def _hat_furcap21(k, C, yaw):
    """the treasurer's cap: a soft crimson crown with a broad fur band, a gold brooch and a short feather."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx - 0.05 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.5, x1=0.5, mid=0.30)
    fur = CE._gradient(k, "hf", dict(light=FUR["light"], base=FUR["base"], dark=FUR["dark"]), x0=-0.55, x1=0.55, mid=0.35)
    yb = -0.24
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    crown = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.50, yb - 0.02, dx - 0.54, yb - 0.40, cx - 0.22, yb - 0.56, cx + 0.02, yb - 0.56, cx + 0.30, yb - 0.56, dx + 0.56, yb - 0.38, dx + 0.50, yb - 0.02,
        dx, yb - 0.08, dx - 0.50, yb - 0.02)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>'
             % (cx - 0.32, yb - 0.20, cx - 0.22, yb - 0.44, cx - 0.04, yb - 0.50, k.c(P._shade(col["base"], 1.35))))
    for i in range(9):
        t = i / 8.0
        x = -0.50 + 1.0 * t
        yy = yb - 0.02 + 0.07 * (1 - (2 * t - 1) ** 2) * 0.9 - 0.06
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.092" ry="0.085" fill="%s" stroke="%s" stroke-width="0.020"/>'
                 % (dx + x, yy, k.c(FUR["base"] if i % 2 else FUR["light"]), k.ink))
    for (x, y) in ((-0.34, -0.04), (-0.12, 0.00), (0.16, -0.02), (0.40, -0.06)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.022" ry="0.012" fill="%s" opacity="0.8"/>' % (dx + x, yb + y - 0.02, k.c("#6a625a")))
    bx = dx + 0.30
    o.append('<circle cx="%.4f" cy="%.4f" r="0.050" fill="%s" stroke="%s" stroke-width="0.014"/>' % (bx, yb - 0.04, k.c(GOLD["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.022" fill="%s" stroke="%s" stroke-width="0.008"/>' % (bx, yb - 0.04, k.c("#c8302c"), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (bx + 0.02, yb - 0.08, bx + 0.12, yb - 0.30, bx + 0.30, yb - 0.46, bx + 0.16, yb - 0.22, bx + 0.05, yb - 0.04, k.c("#e8e2d2"), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.62, yb + 0.1), (dx + 0.62, yb + 0.1), (cx, yb - 0.58), (bx + 0.30, yb - 0.46)))
    return "".join(o), (cx, yb - 0.56)


def _hat_ironcap21(k, C, yaw):
    """a plain iron skull cap with a rim band and rivets."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx - 0.04 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.5, x1=0.5, mid=0.30)
    yb = -0.22
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    dome = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.50, yb, dx - 0.53, yb - 0.34, cx - 0.22, yb - 0.50, cx, yb - 0.50, cx + 0.22, yb - 0.50, dx + 0.53, yb - 0.34, dx + 0.50, yb, dx, yb + 0.07, dx - 0.50, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.38, yb - 0.05, dx - 0.34, yb - 0.32, cx - 0.10, yb - 0.45, k.c(col["shine"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.52, yb - 0.075, dx, yb - 0.02, dx + 0.52, yb - 0.075, dx + 0.52, yb + 0.02, dx, yb + 0.09, dx - 0.52, yb + 0.02)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (band, k.c(col["dark"]), k.ink))
    for x in (-0.38, -0.20, 0.0, 0.20, 0.38):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s" stroke="%s" stroke-width="0.005"/>' % (dx + x, yb + 0.012 - 0.018 * (1 - (x / 0.45) ** 2), k.c(col["light"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.56, yb + 0.06), (dx + 0.56, yb + 0.06), (cx, yb - 0.52)))
    return "".join(o), (cx, yb - 0.50)


def _hat_longhair21(k, C, yaw):
    """Wallace: long brown hair over the crown and falling past the cheeks to the shoulders, face in an oval opening, a thin
    leather brow band."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    outer = [(-0.50 + dx, 0.98), (-0.64 + dx, 0.40), (-0.62 + dx, -0.04), (-0.56 + dx, -0.36), (-0.30 + dx, -0.60), (dx, -0.66), (0.30 + dx, -0.60),
             (0.56 + dx, -0.36), (0.62 + dx, -0.04), (0.64 + dx, 0.40), (0.50 + dx, 0.98)]
    inner = [(0.37 + fx, 0.40), (0.42 + fx, 0.05), (0.38 + fx, -0.20), (fx, -0.30), (-0.38 + fx, -0.20), (-0.42 + fx, 0.05), (-0.37 + fx, 0.40)]
    g = CE._gradient(k, "ht", col, x0=-0.6, x1=0.6, mid=0.32)
    s, d = _frame(k, outer, inner, g, 0.026)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"], s]
    for sd in (-1, 1):
        for (a, b, c_) in ((0.50, 0.60, 0.90), (0.54, 0.64, 0.80), (0.46, 0.56, 0.70)):
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7" stroke-linecap="round"/>'
                     % (dx + sd * a, -0.18, dx + sd * b, 0.30, dx + sd * (a - 0.04), c_, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.05, -0.64, dx - 0.12, -0.50, dx - 0.16, -0.34, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.44, -0.30, dx - 0.34, -0.54, dx - 0.08, -0.62, k.c(col["light"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.66, 0.4), (dx + 0.66, 0.4), (dx, -0.68), (dx - 0.50, 1.0), (dx + 0.50, 1.0)))
    return "".join(o), (dx, -0.66)


HATS21 = {"coif21": _hat_coif21, "bascinet21": _hat_bascinet21, "greathelm21": _hat_greathelm21, "furcap21": _hat_furcap21,
          "ironcap21": _hat_ironcap21, "longhair21": _hat_longhair21}


# ============================================================================= costumes (torso-local)
def _pat_chequy(k, X, y0, y1, hw, c1, sq=0.15):
    o = []
    nx = int(hw / sq) + 2
    ny = int((y1 - y0) / sq) + 2
    for j in range(ny):
        for i in range(-nx, nx):
            if (i + j) % 2:
                continue
            xa, xb = i * sq, (i + 1) * sq
            ya, yb = y0 + j * sq, y0 + (j + 1) * sq
            o.append(_poly_d([X(xa, ya), X(xb, ya), X(xb, yb), X(xa, yb)]))
    return '<path d="%s" fill="%s"/>' % ("".join(o), c1)


def _pat_chevron(k, X, yc, hw, col, w=0.15, rise=0.38):
    pts = [X(0.0, yc), X(hw * 1.05, yc + rise), X(hw * 1.05, yc + rise + w), X(0.0, yc + w), X(-hw * 1.05, yc + rise + w), X(-hw * 1.05, yc + rise)]
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(pts), col, k.ink)


def _clip(k, name, d):
    cid = "%s_c21%s" % (k.uid, name)
    k.defs.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, d))
    return cid


def _belt(k, X, yb, hw, col, buckle=GOLD["base"]):
    o = [_ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.ink, 0.060), _ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.c(col), 0.040)]
    bx, by = X(0.0, yb)
    o.append('<rect x="%.4f" y="%.4f" width="0.070" height="0.056" rx="0.010" fill="none" stroke="%s" stroke-width="0.012"/>' % (bx - 0.035, by - 0.028, k.c(buckle)))
    return "".join(o)


def _sword_back(k, X, hw, yB, col):
    """a long sword carried on the back: leather baldric across the chest (inside), crossguard + grip above the far shoulder and
    the scabbard tip at the near hip (behind the torso)."""
    behind = []
    gx, gy = X(-hw * 1.15, 0.45)
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (gx + 0.28, gy + 0.80, gx - 0.18, gy - 0.30, k.ink))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (gx + 0.28, gy + 0.80, gx - 0.18, gy - 0.30, k.c(LEATHER["base"])))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (gx - 0.18, gy - 0.30, gx - 0.25, gy - 0.50, k.ink))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>' % (gx - 0.18, gy - 0.30, gx - 0.25, gy - 0.50, k.c("#5a3a26")))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (gx - 0.30, gy - 0.22, gx - 0.12, gy - 0.40, k.ink))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (gx - 0.30, gy - 0.22, gx - 0.12, gy - 0.40, k.c(GOLD["base"])))
    behind.append('<circle cx="%.4f" cy="%.4f" r="0.038" fill="%s" stroke="%s" stroke-width="0.012"/>' % (gx - 0.285, gy - 0.54, k.c(GOLD["base"]), k.ink))
    k.ext.append((gx - 0.29, gy - 0.58, 0.05))
    k.ext.append((gx - 0.34, gy - 0.20, 0.04))
    sx, sy = X(hw * 0.70, yB + 0.05)
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (sx - 0.05, sy - 0.30, sx + 0.22, sy + 0.12, k.ink))
    behind.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>' % (sx - 0.05, sy - 0.30, sx + 0.22, sy + 0.12, k.c(LEATHER["base"])))
    behind.append('<circle cx="%.4f" cy="%.4f" r="0.032" fill="%s" stroke="%s" stroke-width="0.010"/>' % (sx + 0.18, sy + 0.12, k.c(GOLD["base"]), k.ink))
    k.ext.append((sx + 0.20, sy + 0.14, 0.05))
    over = _ln([X(hw * 0.70, 0.34), X(-hw * 0.60, yB - 0.06)], k.ink, 0.062) + _ln([X(hw * 0.70, 0.34), X(-hw * 0.60, yB - 0.06)], k.c(LEATHER["base"]), 0.040)
    return "".join(behind), over


def _cos_surcoat21(k, C, m):
    """mail (shirt + skirt, mail sleeves come from the CAST sleeve colour) under a sleeveless surcoat: C pattern 'plain' |
    'chequy' (colors alt = the second tincture) | 'lion' (one gold lion) | 'chevron' (white chevron); belt; optional sword."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    pat = C.get("pattern", "plain")
    tw = C.get("tabard_w", 0.88)
    o = []
    if C.get("mail", True):
        o.append('<rect x="-0.9" y="0.3" width="1.8" height="1.5" fill="%s" opacity="0.95"/>' % C6._mail_pattern(k))
    tab = [X(-tw * hw, 0.36), X(tw * hw, 0.36), X(tw * hw * 1.03, yB + 0.1), X(-tw * hw * 1.03, yB + 0.1)]
    gt = C2._grad(k, "tb", col["base"], -tw * hw, tw * hw)
    o.append(_poly(k, tab, gt, 0.016))
    cid = _clip(k, "tc", _poly_d(tab))
    pp = []
    if pat == "chequy":
        pp.append(_pat_chequy(k, X, 0.30, yB + 0.12, tw * hw, k.c(col["alt"]), 0.15))
    elif pat == "lion":
        c = X(0.0, 0.76)
        pp.append(C6._lion(k, c[0], c[1], 0.46 * min(1.0, hw / 0.40)))
    elif pat == "chevron":
        pp.append(_pat_chevron(k, X, 0.62, tw * hw, k.c(col["alt"])))
    if pp:
        o.append('<g clip-path="url(#%s)">%s</g>' % (cid, "".join(pp)))
    o.append(C6._neckline(k, X, col.get("neck", "#3a2a2a"), 0.395, 0.16, 0.045) if hasattr(C6, "_neckline") else "")
    for s in (-1, 1):
        o.append(_ln([X(s * (tw * hw - 0.025), 0.38), X(s * (tw * hw * 1.03 - 0.025), yB + 0.1)], k.c(col.get("trim", GOLD["base"])), 0.020))
    behind, over_extra = "", ""
    if C.get("sword"):
        behind, over_extra = _sword_back(k, X, hw, yB, col)
    yt = yB - 0.10
    hem = yB + C.get("tabard_len", 0.34)
    ov = []
    if C.get("mail", True):
        ov.append(C2._skirt(k, "mk", X, yt - 0.04, hw * 0.98, yB + C.get("mail_len", 0.24), hw + 0.06, C6._mail_pattern(k), sw=0.024))
    right, hemp, left = C2._skirt_pts(X, yt, tw * hw * 1.02, hem, tw * hw * 1.02 + 0.03)
    sk_d = P._smooth_open(right + hemp + left) + " Z"
    ov.append(C2._skirt(k, "tk", X, yt, tw * hw * 1.02, hem, tw * hw * 1.02 + 0.03, gt, sw=0.024,
                        folds=((-0.06, yt + 0.08, -0.08, hem - 0.03), (0.07, yt + 0.08, 0.09, hem - 0.03)), fold_col=k.c(P._shade(col["base"], 0.62))))
    if pat == "chequy":
        cid2 = _clip(k, "sk", sk_d)
        ov.append('<g clip-path="url(#%s)">%s</g>' % (cid2, _pat_chequy(k, X, yt - 0.02, hem + 0.06, tw * hw + 0.1, k.c(col["alt"]), 0.15)))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_open(right + hemp + left), k.ink))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016"/>'
              % (X(-tw * hw, hem - 0.04) + X(0, hem - 0.015) + X(tw * hw, hem - 0.04) + (k.c(col.get("trim", GOLD["base"])),)))
    ov.append(_belt(k, X, yB - 0.10, hw, col.get("belt", "#3a2620")))
    return "".join(o) + over_extra, behind, "".join(ov)


def _fur_collar(k, X, y, hw, n=9, r=0.075):
    o = []
    for i in range(n):
        t = i / (n - 1.0)
        x = -hw * 0.82 + 2 * hw * 0.82 * t
        yy = y + 0.05 * math.sin(math.pi * t) * 0.0 + 0.045 * (1 - (2 * t - 1) ** 2)
        c = X(x, yy)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (c[0], c[1], r, r * 0.8, k.c(FUR["base"] if i % 2 else FUR["light"]), k.ink))
    return "".join(o)


def _purse(k, X, hw, yb, col):
    """a fat coin purse hanging at the belt (screen-right hip): a round leather bag, gathered neck, gold clasp, a coin showing."""
    c = X(hw * 0.52, yb + 0.20)
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (c[0] - 0.02, yb, c[0] - 0.02, c[1] - 0.12, k.ink),
         '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (c[0] - 0.02, yb, c[0] - 0.02, c[1] - 0.12, k.c(LEATHER["dark"]))]
    bag = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
           % (c[0] - 0.05, c[1] - 0.14, c[0] - 0.24, c[1] - 0.06, c[0] - 0.24, c[1] + 0.22, c[0], c[1] + 0.22,
              c[0] + 0.24, c[1] + 0.22, c[0] + 0.24, c[1] - 0.06, c[0] + 0.05, c[1] - 0.14,
              c[0] + 0.02, c[1] - 0.17, c[0] - 0.02, c[1] - 0.17, c[0] - 0.05, c[1] - 0.14))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (bag, k.c(LEATHER["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
             % (c[0] - 0.15, c[1] - 0.02, c[0] - 0.17, c[1] + 0.12, c[0] - 0.08, c[1] + 0.18, k.c(LEATHER["light"])))
    o.append('<path d="M%.4f,%.4f q0.04,-0.05 0.09,0 M%.4f,%.4f q0.04,-0.05 0.09,0" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (c[0] - 0.12, c[1] - 0.10, c[0] + 0.02, c[1] - 0.10, k.c(LEATHER["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.034" fill="%s" stroke="%s" stroke-width="0.010"/>' % (c[0] + 0.03, c[1] + 0.03, k.c(GOLD["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.050" fill="%s" stroke="%s" stroke-width="0.012"/>' % (c[0] - 0.10, c[1] - 0.17, k.c(GOLD["light"]), k.ink))
    k.ext.append((c[0] - 0.25, c[1] + 0.24, 0.03))
    k.ext.append((c[0] + 0.25, c[1] + 0.24, 0.03))
    return "".join(o)


def _chain21(k, X, hw):
    pts = []
    for i in range(17):
        t = i / 16.0
        x = -hw * 0.62 + 2 * hw * 0.62 * t
        y = 0.40 + 0.36 * (1 - (2 * t - 1) ** 2)
        pts.append(X(x, y))
    o = []
    for i, p in enumerate(pts):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.034" ry="0.024" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%d %.4f %.4f)"/>'
                 % (p[0], p[1], k.c(GOLD["base"] if i % 2 else GOLD["light"]), k.ink, (i - 8) * 8, p[0], p[1]))
    mx, my = X(0.0, 0.86)
    o.append('<circle cx="%.4f" cy="%.4f" r="0.070" fill="%s" stroke="%s" stroke-width="0.016"/>' % (mx, my, k.c(GOLD["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.030" fill="%s" stroke="%s" stroke-width="0.008"/>' % (mx, my, k.c("#3a6ab0"), k.ink))
    return "".join(o)


def _cos_robe21(k, C, m):
    """the treasurer: a rich crimson robe to the shins, gold trim down the front and round the hem, a fur collar, a gold belt,
    a fat purse at the belt and a gold chain."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    o.append(_ln([X(0, 0.40), X(0, yB + 0.1)], k.c(col["dark"]), 0.020))
    for s in (-1, 1):
        o.append(_ln([X(s * 0.10, 0.42), X(s * 0.10, yB + 0.1)], k.c(GOLD["base"]), 0.040))
        o.append(_ln([X(s * 0.10, 0.42), X(s * 0.10, yB + 0.1)], k.ink, 0.008))
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                 % (X(s * 0.36, 0.60) + X(s * 0.28, 0.80) + X(s * 0.34, 1.00) + (k.c(col["dark"]),)))
    o.append(_fur_collar(k, X, 0.42, hw))
    inside = "".join(o)
    yt = yB - 0.08
    hem = yB + C.get("robe_len", 0.66)
    a = hw * 0.99
    b = hw + C.get("robe_flare", 0.22)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "rb", X, yt, a, hem, b, g, sw=0.026,
                    folds=((-0.20, yt + 0.12, -0.28, hem - 0.04), (0.20, yt + 0.12, 0.28, hem - 0.04), (-0.46, yt + 0.12, -0.56, hem - 0.04), (0.46, yt + 0.12, 0.56, hem - 0.04)),
                    fold_col=k.c(col["dark"]))]
    ov.append(_ln([X(0.0, yt), X(0.01, hem + 0.02)], k.c(GOLD["base"]), 0.040))
    ov.append(_ln([X(0.0, yt), X(0.01, hem + 0.02)], k.ink, 0.008))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>'
              % (X(-b * 0.96, hem - 0.04) + X(0, hem + 0.02) + X(b * 0.96, hem - 0.04) + (k.c(GOLD["base"]),)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
              % (X(-b * 0.96, hem - 0.05) + X(0, hem + 0.01) + X(b * 0.96, hem - 0.05) + (k.c(GOLD["dark"]),)))
    yb = yB - 0.12
    ov.append(_belt(k, X, yb, hw, GOLD["dark"], buckle="#ffe58a"))
    ov.append(_chain21(k, X, hw))
    ov.append(_purse(k, X, hw, yb, col))
    return inside, "", "".join(ov)


def _cos_gambeson21(k, C, m):
    """a padded gambeson: vertical quilted channels, a rolled collar, a leather belt, a short skirt to mid-thigh with a stitched hem."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    # quilting: lighter padded strips between dark stitch lines
    for i in range(-5, 6):
        x = i * 0.105
        if abs(x) > hw * 0.98:
            continue
        o.append(_ln([X(x, 0.40), X(x * 1.02, yB + 0.1)], k.c(col["dark"]), 0.010, ' opacity="0.7"'))
    for y in (0.66, 0.90, 1.10):
        if y < yB:
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>'
                     % (X(-hw, y) + X(0, y + 0.03) + X(hw, y) + (k.c(col["dark"]),)))
    for s in (-1, 1):
        o.append(_ln([X(s * 0.14, 0.36), X(s * 0.30, 0.45)], k.c(P._shade(col["base"], 1.2)), 0.040))
    o.append('<path d="M%.4f,0.40 Q%.4f,0.52 %.4f,0.40" fill="none" stroke="%s" stroke-width="0.050"/>' % (X(-0.19, 0.4)[0], X(0, 0.5)[0], X(0.19, 0.4)[0], k.c(col["dark"])))
    o.append(_ln([X(0, 0.50), X(0, yB + 0.1)], k.c(col["dark"]), 0.014))
    for y in (0.62, 0.78, 0.94):
        if y < yB - 0.1:
            o.append(_circ(X(0.0, y), 0.016, k.c(col.get("button", "#d8c890")), k, 0.006))
    inside = "".join(o)
    yt = yB - 0.10
    hem = yB + C.get("tunic_len", 0.30)
    right, hemp, left = C2._skirt_pts(X, yt, hw * 0.99, hem, hw + 0.08)
    sk_d = P._smooth_open(right + hemp + left) + " Z"
    ov = [C2._skirt(k, "gb", X, yt, hw * 0.99, hem, hw + 0.08, "url(#%s_tg)" % k.uid, sw=0.026)]
    cid = _clip(k, "gk", sk_d)
    st = "".join(_ln([X(i * 0.105, yt), X(i * 0.12, hem + 0.02)], k.c(col["dark"]), 0.010, ' opacity="0.7"') for i in range(-5, 6) if abs(i * 0.105) < hw)
    ov.append('<g clip-path="url(#%s)">%s</g>' % (cid, st))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.03 0.02" opacity="0.8"/>'
              % (X(-hw - 0.05, hem - 0.05) + X(0, hem - 0.02) + X(hw + 0.05, hem - 0.05) + (k.c(col["dark"]),)))
    ov.append(_belt(k, X, yB - 0.12, hw, LEATHER["base"], buckle="#c8c8c8"))
    return inside, "", "".join(ov)


def _cos_tunic21(k, C, m):
    """a Scots tunic to the knee (no kilt): wool, a laced neck, a rope or leather belt, a darker hem band.  mail=True: a mail shirt
    over the tunic (Wallace: dark-green tunic, mail to mid-thigh), sword=True: the long sword on the back."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    if C.get("mail"):
        o.append('<rect x="-0.9" y="0.3" width="1.8" height="1.5" fill="%s" opacity="0.97"/>' % C6._mail_pattern(k))
        o.append('<path d="M%.4f,0.40 Q%.4f,0.54 %.4f,0.40" fill="none" stroke="%s" stroke-width="0.040"/>' % (X(-0.18, 0.4)[0], X(0, 0.5)[0], X(0.18, 0.4)[0], k.c(STEEL["dark"])))
    else:
        o.append('<path d="M%.4f,0.40 Q%.4f,0.535 %.4f,0.40" fill="none" stroke="%s" stroke-width="0.044"/>' % (X(-0.17, 0.4)[0], X(0, 0.5)[0], X(0.17, 0.4)[0], k.c(col["dark"])))
        o.append(_poly(k, [X(-0.045, 0.47), X(0.045, 0.47), X(0.0, 0.66)], k.c(col.get("lining", "#c8b890")), 0.013))
        lac = "".join("M%.4f,%.4f L%.4f,%.4f " % (X(-0.03, y) + X(0.03, y + 0.03)) for y in (0.50, 0.555, 0.61))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (lac, k.c(col["dark"])))
        for s in (-1, 1):
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                     % (X(s * 0.30, 0.56) + X(s * 0.22, 0.72) + X(s * 0.26, 0.90) + (k.c(col["dark"]),)))
    behind, over_extra = "", ""
    sw = C.get("sword") if _POSE21["sheath"] is None else _POSE21["sheath"]
    if sw:
        behind, over_extra = _sword_back(k, X, hw, yB, col)
    inside = "".join(o)
    yt = TT + 0.58 * h
    a = hw * 0.985
    hem = yB + C.get("tunic_len", 0.62)
    b = hw + C.get("tunic_flare", 0.12)
    g = "url(#%s_tg)" % k.uid
    ov = []
    if C.get("mail"):
        right, hemp, left = C2._skirt_pts(X, yt, a, hem, b)
        ov.append(C2._skirt(k, "tn", X, yt, a, hem, b, g, sw=0.026, rag=0.02, n_rag=8))
        ov.append(C2._skirt(k, "mk", X, yt - 0.02, hw * 0.98, yB + C.get("mail_len", 0.34), hw + 0.07, C6._mail_pattern(k), sw=0.024))
    else:
        ov.append(C2._skirt(k, "tn", X, yt, a, hem, b, g, sw=0.026, rag=0.02, n_rag=8,
                            folds=((-0.12, yt + 0.12, -0.17, hem - 0.04), (0.14, yt + 0.12, 0.20, hem - 0.05)), fold_col=k.c(col["dark"])))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" opacity="0.8"/>'
              % (X(-b * 0.94, hem - 0.08) + X(0, hem - 0.04) + X(b * 0.94, hem - 0.08) + (k.c(col["dark"]),)))
    yb = TT + 0.60 * h
    belt = [X(-a - 0.01, yb - 0.01), X(-a * 0.5, yb + 0.018), X(0.0, yb + 0.025), X(a * 0.5, yb + 0.018), X(a + 0.01, yb - 0.01)]
    d = P._smooth_open(belt)
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (d, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (d, k.c(col.get("belt", "#8a6a3a"))))
    kx, ky = X(0.10, yb + 0.02)
    for (dx_, ln, cv) in ((-0.025, 0.20, -0.03), (0.020, 0.16, 0.03)):
        e = (kx + dx_ + cv, ky + ln)
        dd = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (kx + dx_ * 0.4, ky, kx + dx_ + cv * 2, ky + ln * 0.5, e[0], e[1])
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (dd, k.ink))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.025" stroke-linecap="round"/>' % (dd, k.c(col.get("belt", "#8a6a3a"))))
        k.ext.append((e[0], e[1] + 0.03, 0.03))
    return inside + over_extra, behind, "".join(ov)


COSTUMES21 = {"surcoat21": _cos_surcoat21, "robe21": _cos_robe21, "gambeson21": _cos_gambeson21, "tunic21": _cos_tunic21}


# ============================================================================= props (own local frames, +x = along the grip direction)
SPEAR_BACK, SPEAR_FRONT = 1.85, 2.0           # spear21: butt 2.0 D behind the hand, point 2.0 D ahead (about 4 D, 1.3 x a man)
SPEAR_GRIP2 = -0.80                          # where the second hand holds the shaft (anchor grip_far_*)
SHIELD_R = 0.50
HORN_TIP = 0.95
SWORD_TIP = 1.35
NEW_PROPS21 = ("spear21", "shield21", "horn21", "sword21", "coin21")
NEW_TIP21 = {"spear21": SPEAR_FRONT, "shield21": 0.0, "horn21": HORN_TIP, "sword21": SWORD_TIP, "coin21": 0.06}
SHIELD_COLS = {"ochre": ("#c8962e", "#8a5e18"), "red": ("#b3363a", "#6e1a20"), "blue": ("#3f66a8", "#1e3c70"), "green": ("#4a7a40", "#264a24"),
               "plain": ("#9a6a3a", "#5e3a1c")}


def _spear_body(k):
    o = []
    b, f = -SPEAR_BACK, SPEAR_FRONT
    sh = "#a97a48"
    o.append('<path d="M%.4f,-0.026 L%.4f,-0.022 L%.4f,0.022 L%.4f,0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (b, f - 0.34, f - 0.34, b, k.c(sh), k.ink))
    o.append('<path d="M%.4f,-0.010 L%.4f,-0.009" stroke="%s" stroke-width="0.009" opacity="0.7"/>' % (b + 0.05, f - 0.40, k.c("#dcb07a")))
    o.append('<path d="M%.4f,-0.034 L%.4f,-0.034 L%.4f,0.034 L%.4f,0.034 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (b, b + 0.07, b + 0.07, b, k.c(IRON["dark"]), k.ink))
    blade = "M%.4f,-0.034 L%.4f,-0.034 Q%.4f,-0.100 %.4f,-0.075 L%.4f,0 L%.4f,0.075 Q%.4f,0.100 %.4f,0.034 L%.4f,0.034 Z" % (
        f - 0.38, f - 0.30, f - 0.24, f - 0.14, f, f - 0.14, f - 0.24, f - 0.30, f - 0.38)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (blade, k.c(STEEL["base"]), k.ink))
    o.append('<path d="M%.4f,-0.004 L%.4f,-0.002" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>' % (f - 0.28, f - 0.04, k.c(STEEL["light"])))
    o.append('<path d="M%.4f,-0.046 L%.4f,0.046" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (f - 0.38, f - 0.38, k.ink))
    return "".join(o)


def _shield_body(k):
    c1, c2 = SHIELD_COLS.get(_POSE21["shield"], SHIELD_COLS["ochre"])
    r = SHIELD_R
    g = _lin(k, "shd", P._shade(c1, 1.18), c1, c2, -r, -r, r, r)
    o = ['<circle cx="0" cy="0" r="%.4f" fill="%s" stroke="%s" stroke-width="0.030"/>' % (r, g, k.ink)]
    for x in (-0.30, -0.10, 0.10, 0.30):
        h = math.sqrt(max(0.0, r * r - x * x)) * 0.94
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.65"/>' % (x, -h, x, h, k.c(c2)))
    o.append('<circle cx="0" cy="0" r="%.4f" fill="none" stroke="%s" stroke-width="0.050"/>' % (r - 0.03, k.c(IRON["base"])))
    o.append('<circle cx="0" cy="0" r="%.4f" fill="none" stroke="%s" stroke-width="0.010"/>' % (r - 0.02, k.c(IRON["light"])))
    for i in range(10):
        a = i * math.pi / 5
        o.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="%s"/>' % ((r - 0.03) * math.cos(a), (r - 0.03) * math.sin(a), k.c(IRON["dark"])))
    o.append('<circle cx="0" cy="0" r="0.115" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(IRON["base"]), k.ink))
    o.append('<path d="M-0.06,-0.06 Q-0.02,-0.09 0.03,-0.075" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.9"/>' % k.c(IRON["shine"]))
    return "".join(o)


def _horn_pts(n=14):
    """centre line of the cow horn: from the mouthpiece (-0.05, 0) curving up to the bell end (0.95, -0.34); with half-widths."""
    pts = []
    for i in range(n + 1):
        t = i / float(n)
        x = -0.05 + 1.0 * t
        y = -0.34 * t * t - 0.0 * t
        w = 0.035 + 0.115 * t ** 1.5
        pts.append((x, y, w))
    return pts


def _horn_body(k):
    cp = _horn_pts()
    left, right = [], []
    for i, (x, y, w) in enumerate(cp):
        a = cp[min(i + 1, len(cp) - 1)]
        b = cp[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    pts = left + right[::-1]
    g = _lin(k, "hn", "#f2e4c0", "#d8c490", "#9a8450", 0, -0.2, 0, 0.2)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), g, k.ink)]
    mp = _poly_d([left[0], left[2], right[2], right[0]])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (mp, k.c("#5a4630"), k.ink))
    for i in (4, 9):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (left[i] + right[i] + (k.c(GOLD["dark"]),)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
             % (left[3][0], left[3][1] + 0.01, left[8][0], left[8][1] + 0.015, left[12][0], left[12][1] + 0.01))
    k.ext.append((cp[-1][0], cp[-1][1], 0.16))
    return "".join(o)


def _sword_body(k):
    g = _lin(k, "sb", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.06, 0, 0.06)
    o = ['<path d="M0.12,-0.050 L1.20,-0.040 L%.4f,0 L1.20,0.040 L0.12,0.050 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (SWORD_TIP, g, k.ink),
         '<path d="M0.16,0 L1.18,0" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % k.c(STEEL["deep"]),
         '<path d="M0.18,-0.026 L1.10,-0.018" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>',
         '<path d="M-0.10,0 L0.12,0" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.10,0 L0.12,0" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % k.c("#5a3a26"),
         '<path d="M0.12,-0.20 L0.12,0.20" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % k.ink,
         '<path d="M0.12,-0.20 L0.12,0.20" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>' % k.c(GOLD["base"]),
         '<circle cx="-0.12" cy="0" r="0.050" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(GOLD["base"]), k.ink)]
    k.ext.append((SWORD_TIP, 0.0, 0.03))
    k.ext.append((0.12, -0.21, 0.03))
    k.ext.append((0.12, 0.21, 0.03))
    return "".join(o)


def _coin_body(k):
    return ('<circle cx="0.07" cy="-0.04" r="0.062" fill="%s" stroke="%s" stroke-width="0.014"/>'
            '<circle cx="0.07" cy="-0.04" r="0.038" fill="none" stroke="%s" stroke-width="0.008"/>'
            '<path d="M0.04,-0.07 q0.03,-0.03 0.06,-0.01" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
            % (k.c(GOLD["base"]), k.ink, k.c(GOLD["dark"])))


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS21:
        return _O21["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    if kind == "shield21":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _shield_body(k))
        k.ext.append((H[0] - SHIELD_R * sc, H[1] - SHIELD_R * sc, 0.04))
        k.ext.append((H[0] + SHIELD_R * sc, H[1] + SHIELD_R * sc, 0.04))
        an["shield_" + key] = H
        return o, H
    body = {"spear21": _spear_body, "horn21": _horn_body, "sword21": _sword_body, "coin21": _coin_body}[kind](k)
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    if kind == "spear21":
        for e in ((-SPEAR_BACK, 0.0), (SPEAR_FRONT, 0.0), (SPEAR_FRONT - 0.15, 0.08), (SPEAR_FRONT - 0.15, -0.08)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        gx, gy = _rot(SPEAR_GRIP2 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        bx, by = _rot(-SPEAR_BACK * sc, 0.0, ang)
        an["spear_butt_" + key] = (H[0] + bx, H[1] + by)
    elif kind == "horn21":
        mx, my = _rot(-0.05 * sc, 0.0, ang)
        an["horn_mouth_" + key] = (H[0] + mx, H[1] + my)
    elif kind == "sword21":
        for e in ((SWORD_TIP, 0.0), (0.12, 0.2), (0.12, -0.2), (-0.12, 0)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(NEW_TIP21[kind] * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[kind.replace("21", "") + "_tip_" + key] = tip
    return o, tip


def _standalone(uid, body, ink, tint):
    k = _ctx(uid, ink, tint)
    b = body(k)
    return '<g id="%s_prop"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), b)


def spear_svg(uid="sp", ink=P.INK, tint=None):
    return _standalone(uid, _spear_body, ink, tint)


def shield_svg(uid="sh", col="ochre", ink=P.INK, tint=None):
    _POSE21["shield"] = col
    return _standalone(uid, _shield_body, ink, tint)


def horn_svg(uid="hn", ink=P.INK, tint=None):
    return _standalone(uid, _horn_body, ink, tint)


def sword_svg(uid="sw", ink=P.INK, tint=None):
    return _standalone(uid, _sword_body, ink, tint)


def coin_svg(uid="cn", ink=P.INK, tint=None):
    return _standalone(uid, _coin_body, ink, tint)


# ============================================================================= face extras: puffed cheeks, grass stalk, splutter spray
def _face(k, C, P_, white):
    svg, L = _O21["_face"](k, C, P_, white)
    if C is None or not C.get("_cast21"):
        return svg, L
    over = []
    side = 1.0 if P_["yaw"] >= 0.0 else -1.0
    mx, my = L["mx"], L["my"]
    pf = _POSE21["puff"]
    if pf > 0.02:
        for sd in (-1, 1):
            cx, cy, r = mx + sd * 0.25, my - 0.005, 0.085 * pf + 0.02
            over.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, cy, r, k.c(P.HEAD_FILL), k.ink))
            over.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.3"/>' % (cx + sd * 0.01, cy + 0.01, r * 0.55, k.c("#f0a090")))
            k.ext.append((cx + sd * r, cy, 0.03))
    st = _POSE21["stalk"]
    if st > 0.02:
        x0, y0 = mx + side * 0.07, my + 0.012
        x1, y1 = x0 + side * 0.40 * st, y0 - 0.20 * st
        over.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x0, y0, x1, y1, k.ink))
        over.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x0, y0, x1, y1, k.c("#c8b840")))
        over.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.016" fill="%s" stroke="%s" stroke-width="0.008" transform="rotate(%.1f %.4f %.4f)"/>'
                    % (x1, y1, k.c("#d8c850"), k.ink, -28 * side, x1, y1))
        k.ext.append((x1, y1, 0.04))
    sp = _POSE21["spit"]
    if sp > 0.02:
        ph = _POSE21["t"] * 2 * math.pi
        for i in range(7):
            a = -0.5 * math.pi + (i - 3) * 0.42 + 0.15 * math.sin(ph + i)
            rr = (0.20 + 0.34 * ((i * 37) % 7) / 7.0 + 0.10 * math.sin(ph * 2 + i * 1.7)) * sp
            x, y = mx + 0.05 * (i - 3) + rr * math.cos(a) * 0.9, my + 0.05 - rr * 0.0 + rr * math.sin(a) * 0.55 + 0.35 * (rr ** 2)
            over.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
                        % (x, y - 0.070, 0.048, 0.048, 0.0, 0.080, -0.048, -0.032, 0.0, -0.080, k.c("#d6f0f8"), k.ink))
            k.ext.append((x, y, 0.04))
    wt = _POSE21["wet"]
    if wt > 0.02:
        ph = _POSE21["t"]
        for i, (x, y) in enumerate(((-0.34, 0.30), (0.10, 0.50), (0.36, 0.26))):
            yy = y + 0.20 * ((ph + i * 0.33) % 1.0)
            over.append('<path d="M%.4f,%.4f q0.026,0.040 0,0.062 q-0.026,-0.022 0,-0.062 Z" fill="%s" stroke="%s" stroke-width="0.008" opacity="%.2f"/>'
                        % (x, yy, k.c("#b8dcea"), k.ink, 0.9 * wt))
            k.ext.append((x, yy + 0.07, 0.03))
    if not over:
        return svg, L
    return svg + "".join(over), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE21["puff"] = _f(g("puff21"), 0.0, 0.0, 1.0)
    _POSE21["stalk"] = _f(g("stalk21"), 0.0, 0.0, 1.0)
    _POSE21["spit"] = _f(g("spit21"), 0.0, 0.0, 1.0)
    _POSE21["wet"] = _f(g("wet21"), 0.0, 0.0, 1.0)
    sc = g("shield21")
    _POSE21["shield"] = sc if isinstance(sc, str) and sc in SHIELD_COLS else "ochre"
    sh = g("sheath21")
    _POSE21["sheath"] = None if sh is None else bool(sh)
    _POSE21["t"] = _f(g("t"), 0.0, -1e6, 1e6)
    return _O21["_norm"](C, pose)


# ============================================================================= cast (head D = 1)
_BOOT = dict(color="#3a2c22", cuff="#4a3a2c", h=0.20, toe=0.14)
GREAT = dict(light="#e4e8ee", base="#9aa4b0", dark="#5a6270", shine="#ffffff")
GREAT_RED = dict(GREAT, plume="#b3262c")
GREAT_BLUE = dict(GREAT, plume="#2a4fa0")
KETTLE = dict(light="#c8ccd2", base="#7c8692", dark="#464e58", shine="#f0f2f4")
IRONCAP = dict(light="#b8bcc0", base="#7c8288", dark="#464c52", shine="#e8eaec")
ENGLISH_RED, ENGLISH_BLUE = "#b3262c", "#2a4fa0"


def _knight(seed, build, tw, th, leg, shoulder, sur, helm, hair, skin_cheek, beard=None, moustache=False, limb=0.062):
    d = dict(
        KEEP_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=CE.PROFILE_PEAR if build != "slim" else CE.PROFILE_ATHLETE, shift_pow=1.1,
        shoulder=shoulder, arm=0.78, hip_x=0.17, leg=leg, stance=0.08, wide=0.30, limb_w=limb,
        eye_y=0.030, brow="stroke", brow_th=0.062, mouth="frown", moustache=moustache, smirk_side=1, cheeks=skin_cheek,
        hat="newsboy", hat_style=helm[0], hat_tilt=-2.0, ear_pencil=False, hat_colors=helm[1],
        hair=hair,
        costume="surcoat21", mail=True, tabard_w=0.88, tabard_len=0.36, mail_len=0.26, sword=False,
        sleeve=dict(color="#8d97a3", dark="#5d6672", cuff="#6d7782", len=0.84, w=0.150),
        shorts=dict(color="#3e3a44", dark="#26222a", cuff="#3e3a44", len=0.86, w=0.12),
        boots=dict(color="#2a2220", cuff="#3e3430", h=0.20, toe=0.14),
    )
    d.update(sur)
    if beard:
        d["beard"] = beard
    return d


SUR_LION = dict(pattern="lion", colors=dict(base=ENGLISH_RED, alt=GOLD["base"], trim=GOLD["base"], neck="#5d6672", belt="#2a1c18"))
SUR_CHEV = dict(pattern="chevron", colors=dict(base=ENGLISH_BLUE, alt="#f2eee4", trim="#f2eee4", neck="#5d6672", belt="#2a1c18"))
SUR_CHEQ = dict(pattern="chequy", tabard_w=0.92, colors=dict(base="#2f4f98", alt="#e8b52e", trim="#e8b52e", neck="#5d6672", belt="#2a1c18"))

NEW_CAST21 = {
    # William Cressingham, the treasurer: stout, ruddy, clean-shaven double chin, crimson robe with gold trim, fur-trimmed cap,
    # gold chain and a fat purse at the belt
    "cressingham": dict(
        KEEP_FLAGS, build="stout", seed=21.1,
        torso_w=1.40, torso_h=1.16, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.78, hip_x=0.19, leg=1.20, stance=0.07, wide=0.30, limb_w=0.070,
        eye_y=0.000, brow="stroke", brow_th=0.080, mouth="smirk", moustache=False, smirk_side=1, cheeks="#ee6f5e", chins=True,
        hat="newsboy", hat_style="furcap21", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#cc4048", base="#a8232c", dark="#6a1219", shine="#f08088"),
        hair=dict(color="#7a5a44", front=0.06, grow=0.18),
        costume="robe21", robe_len=0.62, robe_flare=0.22,
        sleeve=dict(color="#a8232c", dark="#6a1219", cuff="#e8b52e", len=0.84, w=0.200),
        shorts=dict(color="#4a2a30", dark="#2e1a1e", cuff="#4a2a30", len=0.90, w=0.15),
        boots=dict(color="#2a1c18", cuff="#2a1c18", h=0.08, toe=0.17),
        colors=dict(base="#a8232c", dark="#6a1219", pants="#4a2a30"),
    ),
    # John de Warenne, Earl of Surrey: old, tired, a grey beard, mail coif, mail and a gold-and-blue chequered surcoat
    "surrey": _knight(21.2, "regular", 0.88, 1.04, 1.30, (0.33, 0.48), SUR_CHEQ, ("coif21", dict(light="#e4e9ee", base="#a4aeba", dark="#5e6874")),
                      dict(color="#cfcbd0", front=0.0, grow=0.0), "#e8a090", beard=dict(color="#cdc9ce", dark="#8c8892"), limb=0.060),
    # English knights: red surcoat with a gold lion / blue surcoat with a white chevron; great helm or open bascinet
    "knight_a": _knight(21.3, "regular", 1.00, 1.08, 1.32, (0.36, 0.47), SUR_LION, ("greathelm21", GREAT_RED), dict(color="#5a3a26", front=0.0, grow=0.0), "#e8907a"),
    "knight_a_open": _knight(21.3, "regular", 1.00, 1.08, 1.32, (0.36, 0.47), SUR_LION, ("bascinet21", dict(KETTLE, plume="#b3262c")), dict(color="#5a3a26", front=0.0, grow=0.0), "#e8907a",
                             moustache=True),
    "knight_b": _knight(21.4, "slim", 0.78, 1.10, 1.42, (0.30, 0.50), SUR_CHEV, ("bascinet21", KETTLE), dict(color="#2a2222", front=0.0, grow=0.0), "#e8a090", limb=0.058),
    "knight_b_great": _knight(21.4, "slim", 0.78, 1.10, 1.42, (0.30, 0.50), SUR_CHEV, ("greathelm21", GREAT_BLUE), dict(color="#2a2222", front=0.0, grow=0.0), "#e8a090", limb=0.058),
}
for _k in ("knight_b", "knight_b_great"):
    NEW_CAST21[_k]["sleeve"] = dict(color="#8d97a3", dark="#5d6672", cuff="#6d7782", len=0.84, w=0.138)
for _k, _c in (("knight_a", "#b3262c"), ("knight_a_open", "#b3262c")):
    NEW_CAST21[_k]["colors"] = dict(NEW_CAST21[_k]["colors"])


def _footman(seed, build, tw, th, leg, shoulder, gamb, hat, hair, cheeks, moustache=None, beard=None, limb=0.062, profile=None):
    d = dict(
        KEEP_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile or CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=shoulder, arm=0.76, hip_x=0.17, leg=leg, stance=0.08, wide=0.30, limb_w=limb,
        eye_y=0.030, brow="stroke", brow_th=0.060, mouth="frown", moustache=bool(moustache), smirk_side=-1, cheeks=cheeks,
        hat="newsboy", hat_style="kettlehat", hat_tilt=-3.0, ear_pencil=False, hat_colors=hat,
        hair=hair,
        costume="gambeson21", tunic_len=0.30,
        sleeve=dict(color=gamb, dark=P._shade(gamb, 0.62), cuff=P._shade(gamb, 0.80), len=0.84, w=0.15),
        shorts=dict(color="#4a3c34", dark="#2e2620", cuff="#4a3c34", len=0.88, w=0.12),
        boots=dict(color="#2e2420", cuff="#3e3430", h=0.20, toe=0.14),
        colors=dict(base=gamb, dark=P._shade(gamb, 0.62), button="#d8c890", pants="#4a3c34"),
    )
    if moustache:
        d.update(moustache_style=moustache, tache_scale=0.95)
    if beard:
        d["beard"] = beard
    return d


GAMBS = ("#a4482f", "#b8862e", "#3f5a8a", "#7a4a6a", "#6a6a3a")     # russet, ochre, indigo, plum, olive: mid-dark, none equals the teal
NEW_CAST21.update({
    "footman_a": _footman(21.5, "regular", 0.92, 1.00, 1.18, (0.34, 0.47), GAMBS[0], KETTLE, dict(color="#6a4a2a", front=0.08, grow=0.18), "#e8907a",
                          moustache="bushy", limb=0.064),
    "footman_b": _footman(21.6, "slim", 0.72, 1.04, 1.34, (0.28, 0.50), GAMBS[2], dict(KETTLE, light="#d0c8b8", base="#8a8478", dark="#4a463e"),
                          dict(color="#2a2222", front=0.07, grow=0.20), "#e8a090", profile=CE.PROFILE_ATHLETE, limb=0.058),
})


def _scot(seed, build, tw, th, leg, shoulder, tunic, hat, hair, cheeks, moustache=None, beard=None, limb=0.062, hat_style="bare7", profile=None, tl=0.62):
    d = dict(
        KEEP_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile or CE.PROFILE_REGULAR, shift_pow=1.05,
        shoulder=shoulder, arm=0.76, hip_x=0.17, leg=leg, stance=0.08, wide=0.30, limb_w=limb,
        eye_y=0.030, brow="stroke", brow_th=0.060, mouth="dash", moustache=bool(moustache), smirk_side=1, cheeks=cheeks,
        hat="newsboy", hat_style=hat_style, hat_tilt=-2.0, ear_pencil=False, hat_colors=hat,
        hair=hair,
        costume="tunic21", tunic_len=tl, tunic_flare=0.10,
        sleeve=dict(color=tunic, dark=P._shade(tunic, 0.62), cuff=P._shade(tunic, 0.78), len=0.84, w=0.150),
        shorts=dict(color="#5a4634", dark="#3a2c20", cuff="#5a4634", len=0.90, w=0.12),
        boots=dict(color="#3a2c22", cuff="#4a3a2c", h=0.16, toe=0.14),
        colors=dict(base=tunic, dark=P._shade(tunic, 0.62), lining="#d8c8a0", belt="#7a5a32", pants="#5a4634"),
    )
    if moustache:
        d.update(moustache_style=moustache, tache_scale=0.95)
    if beard:
        d["beard"] = beard
    return d


BARE = dict(light="#000000", base="#000000", dark="#000000")
TUNICS = dict(brown="#7a5230", ochre="#b0842c", moss="#5e6b32", red="#a24f48")
NEW_CAST21.update({
    # Wallace: tall, strong, long brown hair, short beard, mail shirt over a dark-green tunic, a long sword on his back
    "wallace": dict(
        _scot(21.7, "regular", 0.96, 1.14, 1.58, (0.36, 0.48), "#2c5a3a", LONGB, dict(color="#5e3a1e", front=0.0, grow=0.0), "#e0907a",
              beard=dict(color="#5a3a22", dark="#3a2212"), limb=0.066, hat_style="longhair21", profile=CE.PROFILE_ATHLETE, tl=0.60),
        costume="tunic21", mail=True, sword=True, mail_len=0.16, tunic_len=0.66,
        sleeve=dict(color="#8d97a3", dark="#5d6672", cuff="#6d7782", len=0.84, w=0.160)),
    # Moray: younger, mail and a green surcoat, a mail coif, a spear
    "moray": dict(
        _knight(21.8, "slim", 0.80, 1.06, 1.40, (0.30, 0.50), dict(pattern="plain", colors=dict(base="#2f6a3c", alt="#2f6a3c", trim="#c8b060", neck="#5d6672", belt="#2a1c18")),
                ("coif21", dict(light="#e4e9ee", base="#a4aeba", dark="#5e6874")), dict(color="#6a4a2a", front=0.0, grow=0.0), "#eea294", limb=0.058),
        tabard_w=0.84, tabard_len=0.42),
    "scot_a": _scot(21.9, "regular", 0.92, 1.02, 1.30, (0.34, 0.47), TUNICS["brown"], BARE, dict(color="#2a2020", front=0.09, grow=0.22), "#e8907a",
                    moustache="bushy", limb=0.064),
    "scot_b": _scot(22.0, "slim", 0.74, 1.06, 1.44, (0.29, 0.50), TUNICS["ochre"], IRONCAP, dict(color="#6a4020", front=0.04, grow=0.12), "#e8a090",
                    hat_style="ironcap21", profile=CE.PROFILE_ATHLETE, limb=0.058),
    "scot_c": _scot(22.1, "stout", 1.12, 1.04, 1.16, (0.40, 0.45), TUNICS["moss"], BARE, dict(color="#b8602a", front=0.10, grow=0.24), "#ee8a76",
                    beard=dict(color="#b8602a", dark="#7a3a14"), limb=0.068, profile=C2.PROFILE_ROUND),
    "scot_horn": _scot(22.2, "regular", 0.84, 1.00, 1.30, (0.32, 0.48), TUNICS["red"], BARE, dict(color="#3a2a22", front=0.09, grow=0.22), "#ee8a76",
                       limb=0.062),
})
EXTRA_COLOURS = {   # colour variants: base key -> [(suffix, dict of overrides)]
    "footman_a": [("v1", GAMBS[1]), ("v2", GAMBS[3]), ("v3", GAMBS[4])],
    "footman_b": [("v1", GAMBS[0]), ("v2", GAMBS[1]), ("v3", GAMBS[3])],
    "scot_a": [("v1", TUNICS["ochre"]), ("v2", TUNICS["red"]), ("v3", TUNICS["moss"])],
    "scot_b": [("v1", TUNICS["brown"]), ("v2", TUNICS["moss"]), ("v3", TUNICS["red"])],
    "scot_c": [("v1", TUNICS["brown"]), ("v2", TUNICS["ochre"]), ("v3", TUNICS["red"])],
}
VARIANTS21 = {}


def _recolour(name, colour):
    d = dict(NEW_CAST21[name])
    d["sleeve"] = dict(d["sleeve"], color=colour, dark=P._shade(colour, 0.62), cuff=P._shade(colour, 0.80))
    d["colors"] = dict(d["colors"], base=colour, dark=P._shade(colour, 0.62))
    return d


for _b, _vs in EXTRA_COLOURS.items():
    VARIANTS21[_b] = [_b]
    for _s, _c in _vs:
        NEW_CAST21["%s_%s" % (_b, _s)] = _recolour(_b, _c)
        VARIANTS21[_b].append("%s_%s" % (_b, _s))

NEW21 = tuple(NEW_CAST21)
CANVAS_SPECIAL21 = {"horse": (-3.0625, -4.25, 3.0625, 0.25), "helmet_float": (-1.625, -1.625, 1.625, 0.4375)}
for _m in ("knight_a_mtd", "knight_a_open_mtd", "knight_b_mtd", "knight_b_great_mtd", "surrey_mtd", "moray_mtd"):
    CANVAS_SPECIAL21[_m] = (-3.0625, -5.4375, 3.0625, 0.25)
HUMANS21 = ("cressingham", "surrey", "knight_a", "knight_a_open", "knight_b", "knight_b_great", "footman_a", "footman_b", "wallace", "moray",
            "scot_a", "scot_b", "scot_c", "scot_horn")
# feet-relative sprite canvases (D), from every STORY21 pose (and mirrored), the walk / march / sneak / run cycles and run_spear, with 0.31 D head room
CANVAS21 = {
    "cressingham": (-3.4375, -4.1250, 3.4375, 0.5625),
    "surrey": (-3.3750, -4.0625, 3.3750, 0.6250),
    "knight_a": (-3.4375, -4.3125, 3.4375, 0.5625),
    "knight_a_open": (-3.4375, -4.3125, 3.4375, 0.5625),
    "knight_b": (-3.3750, -4.4375, 3.3750, 0.5000),
    "knight_b_great": (-3.3750, -4.4375, 3.3750, 0.5000),
    "footman_a": (-3.3750, -4.0625, 3.3750, 0.7500),
    "footman_b": (-3.3125, -4.2500, 3.3125, 0.6250),
    "wallace": (-3.3750, -5.2500, 3.3750, 0.3125),
    "moray": (-3.3750, -4.3750, 3.3750, 0.5625),
    "scot_a": (-3.3750, -4.1875, 3.3750, 0.6250),
    "scot_b": (-3.3125, -4.3750, 3.3125, 0.5625),
    "scot_c": (-3.4375, -4.0625, 3.4375, 0.6875),
    "scot_horn": (-3.3125, -4.1875, 3.3125, 0.6875),
    "footman_a_v1": (-3.3750, -4.0625, 3.3750, 0.7500),
    "footman_a_v2": (-3.3750, -4.0625, 3.3750, 0.7500),
    "footman_a_v3": (-3.3750, -4.0625, 3.3750, 0.7500),
    "footman_b_v1": (-3.3125, -4.2500, 3.3125, 0.6250),
    "footman_b_v2": (-3.3125, -4.2500, 3.3125, 0.6250),
    "footman_b_v3": (-3.3125, -4.2500, 3.3125, 0.6250),
    "scot_a_v1": (-3.3750, -4.1875, 3.3750, 0.6250),
    "scot_a_v2": (-3.3750, -4.1875, 3.3750, 0.6250),
    "scot_a_v3": (-3.3750, -4.1875, 3.3750, 0.6250),
    "scot_b_v1": (-3.3125, -4.3750, 3.3125, 0.5625),
    "scot_b_v2": (-3.3125, -4.3750, 3.3125, 0.5625),
    "scot_b_v3": (-3.3125, -4.3750, 3.3125, 0.5625),
    "scot_c_v1": (-3.4375, -4.0625, 3.4375, 0.6875),
    "scot_c_v2": (-3.4375, -4.0625, 3.4375, 0.6875),
    "scot_c_v3": (-3.4375, -4.0625, 3.4375, 0.6875),
}


# ============================================================================= the horse card (side view, facing +x; ground y = 0, y up is negative)
HORSE_COATS = {   # coat, caparison colours
    "red": dict(coat=("#a06a48", "#7a4a30", "#4e2e1c"), mane="#2a1c18", cloth="#b3262c", cloth_d="#7a141a", trim=GOLD["base"], motif="#e8b52e", pat="diaper"),
    "blue": dict(coat=("#b8b4bc", "#8e8a98", "#5e5a68"), mane="#4a4652", cloth="#2a4fa0", cloth_d="#1a3470", trim="#f2eee4", motif="#f2eee4", pat="bars"),
    "gold": dict(coat=("#b8743c", "#8e5628", "#5a3414"), mane="#3a2414", cloth="#d4a02c", cloth_d="#8e6a14", trim="#b3262c", motif="#b3262c", pat="chequy"),
    "plain": dict(coat=("#a8744c", "#7e5232", "#4e2e1c"), mane="#2a1c18", cloth="#8a6a4a", cloth_d="#5a4028", trim="#c8a060", motif="#c8a060", pat="none"),
}
HORSE_SEAT = (0.30, -2.50)
HORSE_HIPS = {"nf": (1.00, -1.62), "ff": (0.88, -1.66), "nh": (-1.12, -1.70), "fh": (-1.00, -1.72)}
HORSE_OFF = {"nh": 0.0, "nf": 0.25, "fh": 0.50, "ff": 0.75}


def _ik(H, T, a, b, sgn):
    dx, dy = T[0] - H[0], T[1] - H[1]
    d = max(1e-6, min(math.hypot(dx, dy), a + b - 1e-4))
    base = math.atan2(dy, dx)
    cosA = (a * a + d * d - b * b) / (2 * a * d)
    A = math.acos(max(-1.0, min(1.0, cosA)))
    ang = base + sgn * A
    return (H[0] + a * math.cos(ang), H[1] + a * math.sin(ang))


def _leg_target(key, phase, mode, stride=0.64, lift=0.34):
    hx = HORSE_HIPS[key][0]
    if mode != "walk":
        return (hx + (0.10 if key in ("nf", "ff") else -0.08), -0.10)
    u = (phase + HORSE_OFF[key]) % 1.0
    st = 0.62
    if u < st:
        s = u / st
        return (hx + stride * (0.5 - s), -0.10)
    s = (u - st) / (1 - st)
    return (hx + stride * (-0.5 + s), -0.10 - lift * math.sin(math.pi * s) ** 0.9)


def _horse_leg(k, key, phase, mode, shade, coat):
    H = HORSE_HIPS[key]
    T = _leg_target(key, phase, mode)
    fore = key in ("nf", "ff")
    a, b = (0.82, 0.78) if fore else (0.86, 0.80)
    K = _ik(H, T, a, b, -1.0 if fore else 1.0)
    # the lower leg of the hind leg: hock then cannon sloping forward
    col = k.c(P._shade(coat[1], shade))
    dk = k.c(P._shade(coat[2], shade))
    o = []
    for (p0, p1, w) in ((H, K, 0.30), (K, T, 0.17)):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (p0[0], p0[1], p1[0], p1[1], k.ink, w + 0.050))
    for (p0, p1, w) in ((H, K, 0.30), (K, T, 0.17)):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (p0[0], p0[1], p1[0], p1[1], col, w))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.115" fill="%s" stroke="%s" stroke-width="0.024"/>' % (K[0], K[1], col, k.ink))
    # lower leg darker (stockings) and the hoof
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.14" stroke-linecap="round"/>' % (K[0] * 0.3 + T[0] * 0.7, K[1] * 0.3 + T[1] * 0.7, T[0], T[1], dk))
    hx, hy = T
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
             % (hx - 0.10, hy - 0.02, hx + 0.12, hy - 0.02, hx + 0.15, hy + 0.10, hx - 0.12, hy + 0.10, k.c("#2e2420"), k.ink))
    k.ext.append((hx, hy + 0.12, 0.05))
    return "".join(o)


def _horse_body_pts(dy):
    pts = [(0.95, -2.55), (1.22, -2.95), (1.50, -3.26), (1.76, -3.50), (2.02, -3.12), (1.96, -2.75), (1.80, -2.36), (1.56, -1.98), (1.42, -1.66),
           (1.12, -1.40), (0.60, -1.30), (-0.20, -1.28), (-0.90, -1.36), (-1.38, -1.50), (-1.64, -1.86), (-1.66, -2.16), (-1.56, -2.38),
           (-1.10, -2.50), (-0.40, -2.43), (0.30, -2.41)]
    return [(x, y + dy) for (x, y) in pts]


def _horse_head(k, coat, mane, ang, P0, idle):
    """head in its own frame (poll at the origin, nose down-right), rotated by ang degrees about the poll, placed at P0."""
    pts = [(-0.14, 0.04), (0.12, -0.06), (0.42, 0.24), (0.72, 0.62), (0.88, 0.88), (0.94, 1.06), (0.85, 1.15), (0.68, 1.11), (0.40, 0.85),
           (0.10, 0.64), (-0.12, 0.50), (-0.22, 0.30)]
    g = _lin(k, "hhg", coat[0], coat[1], coat[2], 0, 0, 1, 1.1)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f)">' % (P0[0], P0[1], ang)]
    # ears
    o.append('<path d="M-0.10,0.02 L-0.20,-0.44 L0.10,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(coat[2]), k.ink))
    o.append('<path d="M0.02,-0.04 L-0.02,-0.46 L0.22,0.02 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (P._smooth_closed(pts), g, k.ink))
    o.append('<path d="M0.40,0.34 Q0.62,0.66 0.84,0.92" fill="none" stroke="%s" stroke-width="0.014" opacity="0.5"/>' % k.c(coat[0]))
    # bridle: cheek strap, noseband, browband
    br = k.c("#3a2418")
    o.append('<path d="M0.06,-0.02 Q0.20,0.40 0.50,0.80 M0.14,0.02 Q0.30,0.04 0.40,0.12 M0.60,0.78 L0.82,0.94" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % br)
    o.append('<circle cx="0.50" cy="0.80" r="0.032" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(GOLD["base"]), k.ink))
    # eye, nostril, mouth
    o.append('<ellipse cx="0.30" cy="0.30" rx="0.052" ry="0.046" fill="%s"/><circle cx="0.315" cy="0.285" r="0.014" fill="#ffffff"/>' % k.ink)
    o.append('<path d="M0.80,0.96 q0.04,-0.05 0.08,-0.02" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.66,1.10 Q0.78,1.08 0.86,1.12" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % k.ink)
    # forelock
    o.append('<path d="M0.02,-0.04 Q0.30,-0.10 0.34,0.18 Q0.22,0.00 0.00,0.10 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(mane), k.ink))
    o.append('</g>')
    k.ext.append((P0[0] + 1.1, P0[1] + 1.2, 0.05))
    k.ext.append((P0[0] - 0.3, P0[1] - 0.55, 0.05))
    return "".join(o)


def _horse_mane(k, mane, dy, sw):
    top = [(0.98, -2.60), (1.16, -2.92), (1.40, -3.20), (1.62, -3.42), (1.80, -3.54)]
    top = [(x, y + dy) for (x, y) in top]
    low = []
    for i, (x, y) in enumerate(top):
        low.append((x - 0.30 + 0.03 * math.sin(sw * 6.28 + i * 1.3), y + 0.30 + (0.07 if i % 2 else 0.0)))
    pts = top + [(x, y) for (x, y) in low[::-1]]
    o = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(mane), k.ink)
    o += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (top[1][0] - 0.10, top[1][1] + 0.12, top[2][0] - 0.14, top[2][1] + 0.14, top[3][0] - 0.12, top[3][1] + 0.12, k.c(P._shade(mane, 1.9)))
    return o


def _horse_tail(k, mane, dy, sw):
    d0 = (-1.58, -2.30 + dy)
    c = (d0[0] - 0.55 + 0.16 * math.sin(sw * 6.283), d0[1] + 0.55)
    e = (d0[0] - 0.32 + 0.50 * math.sin(sw * 6.283 + 0.6), d0[1] + 1.50)
    pts = []
    for i in range(13):
        t = i / 12.0
        x = (1 - t) ** 2 * d0[0] + 2 * (1 - t) * t * c[0] + t * t * e[0]
        y = (1 - t) ** 2 * d0[1] + 2 * (1 - t) * t * c[1] + t * t * e[1]
        pts.append((x, y))
    L, R = [], []
    for i, (x, y) in enumerate(pts):
        a = pts[min(i + 1, 12)]
        b = pts[max(i - 1, 0)]
        dx, dy_ = a[0] - b[0], a[1] - b[1]
        ln = math.hypot(dx, dy_) or 1.0
        nx, ny = -dy_ / ln, dx / ln
        t = i / 12.0
        w = 0.13 * (1 - t) + 0.07 + 0.05 * math.sin(math.pi * t)
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
    poly = L + R[::-1]
    o = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (P._smooth_closed(poly), k.c(mane), k.ink)
    o += '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6" stroke-linecap="round"/>' % (pts[2][0], pts[2][1], pts[6][0], pts[6][1], pts[10][0], pts[10][1], k.c(P._shade(mane, 1.9)))
    k.ext.append((e[0] - 0.2, e[1] + 0.1, 0.05))
    k.ext.append((e[0] + 0.2, e[1] + 0.1, 0.05))
    return o


def _caparison(k, spec, dy, phase):
    ph = phase * 6.283
    top = [(0.98, -2.52), (0.40, -2.43), (-0.40, -2.46), (-1.10, -2.53), (-1.58, -2.40)]
    rear = [(-1.76, -1.80), (-1.72, -1.10)]
    hem = []
    n = 12
    for i in range(n + 1):
        t = i / float(n)
        x = -1.72 + (1.52 + 1.72) * t
        yb = -0.82 - (0.16 if i % 2 == 0 else 0.0) + 0.035 * math.sin(ph + t * 7.0)
        hem.append((x, yb))
    front = [(1.50, -1.30), (1.42, -1.85), (1.24, -2.30)]
    pts = top + rear + hem + front
    pts = [(x, y + dy) for (x, y) in pts]
    d = "M" + " L".join("%.4f,%.4f" % p for p in pts) + " Z"
    # soften the top and rear: smooth the first part, straight hem points keep the dags
    cloth = spec["cloth"]
    g = _lin(k, "cpg", P._shade(cloth, 1.15), cloth, P._shade(cloth, 0.75), 0, -2.5, 0, -0.8)
    cid = _clip(k, "cap", d)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (d, g, k.ink)]
    pat = []
    mot = k.c(spec["motif"])
    if spec["pat"] == "diaper":
        for j in range(5):
            for i in range(14):
                x = -1.80 + i * 0.26 + (0.13 if j % 2 else 0.0)
                y = -2.30 + j * 0.30 + dy
                pat.append('<path d="M%.3f,%.3f l0.07,0.09 l-0.07,0.09 l-0.07,-0.09 Z" fill="%s" opacity="0.9"/>' % (x, y, mot))
    elif spec["pat"] == "bars":
        for i in range(10):
            x = -1.70 + i * 0.36
            pat.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s"/>' % (x, -2.6 + dy, x + 0.14, -2.6 + dy, x + 0.14, -0.7 + dy, x, -0.7 + dy, mot))
    elif spec["pat"] == "chequy":
        for j in range(8):
            for i in range(14):
                if (i + j) % 2:
                    continue
                x, y = -1.80 + i * 0.26, -2.55 + j * 0.25 + dy
                pat.append('<path d="M%.3f,%.3f h0.26 v0.25 h-0.26 Z" fill="%s"/>' % (x, y, mot))
    o.append('<g clip-path="url(#%s)">%s' % (cid, "".join(pat)))
    # dark gathered folds and a trim band along the hem
    for x in (-1.2, -0.5, 0.2, 0.9):
        o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.5"/>' % (x, -2.2 + dy, x + 0.05, -1.6 + dy, x - 0.04, -1.0 + dy, k.c(spec["cloth_d"])))
    hp = [(x, y + dy) for (x, y) in hem]
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.10"/>' % (" L".join("%.4f,%.4f" % (x, y - 0.07) for (x, y) in hp), k.c(spec["trim"])))
    o.append('</g>')
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % p for p in hp), k.ink))
    return "".join(o)


def horse_parts(uid, phase=0.0, mode="walk", cap="red", t=0.0, ink=P.INK, tint=None, head_bob=None, reins=None):
    """the horse alone: (svg, bbox, anchors).  phase 0..1 = one walk cycle (about 40 frames at 30 fps); mode 'walk' | 'idle' (legs
    planted, head bob + tail swish driven by t 0..1 = one slow loop); cap 'red' | 'blue' | 'gold' | 'plain'."""
    spec = HORSE_COATS.get(cap, HORSE_COATS["plain"])
    k = _ctx(uid, ink, tint)
    ph = _num(phase, 0.0)
    tt = _num(t, 0.0)
    walk = mode == "walk"
    dy = (0.030 * math.cos(4 * math.pi * ph) if walk else 0.012 * math.sin(2 * math.pi * tt))
    if head_bob is None:
        head_bob = (6.0 * math.sin(2 * math.pi * ph + 0.9) if walk else 5.0 * math.sin(2 * math.pi * tt))
    sw = (0.5 * math.sin(2 * math.pi * ph * 1.0) if walk else 0.5 + 0.5 * math.sin(2 * math.pi * tt * 2.0)) * 0.5 + 0.5
    coat = spec["coat"]
    far = "".join(_horse_leg(k, key, ph, "walk" if walk else "idle", 0.74, coat) for key in ("ff", "fh"))
    near = "".join(_horse_leg(k, key, ph, "walk" if walk else "idle", 1.0, coat) for key in ("nh", "nf"))
    g = _lin(k, "hbd", coat[0], coat[1], coat[2], 0, -3.5, 0, -1.2)
    body = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.036" stroke-linejoin="round"/>' % (P._smooth_closed(_horse_body_pts(dy)), g, k.ink)
    body += '<path d="M-1.30,%.4f Q-0.60,%.4f 0.30,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.5"/>' % (-1.55 + dy, -1.42 + dy, -1.45 + dy, k.c(coat[0]))
    P0 = (1.78, -3.48 + dy)
    head = _horse_head(k, coat, spec["mane"], 4.0 + head_bob, P0, not walk)
    mane = _horse_mane(k, spec["mane"], dy, sw)
    tail = _horse_tail(k, spec["mane"], dy, sw)
    capar = _caparison(k, spec, dy, ph)
    # saddle bits and a rein hanging from the bit
    ang = math.radians(4.0 + head_bob)
    bitx = P0[0] + (0.80 * math.cos(ang) - 1.02 * math.sin(ang))
    bity = P0[1] + (0.80 * math.sin(ang) + 1.02 * math.cos(ang))
    rein = '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (
        bitx - 0.04, bity - 0.02, (bitx + 1.0) / 2 + 0.0, bity - 0.15 + 0.35, HORSE_SEAT[0] + 0.55, HORSE_SEAT[1] + dy - 0.10, k.c("#3a2418"))
    sad = ('<path d="M-0.40,%.4f Q-0.50,%.4f -0.62,%.4f L-0.58,%.4f L-0.30,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
           % (-2.40 + dy, -2.62 + dy, -2.50 + dy, -2.30 + dy, -2.38 + dy, k.c(LEATHER["base"]), k.ink))
    sad += ('<path d="M0.70,%.4f Q0.80,%.4f 0.92,%.4f L0.90,%.4f L0.66,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
            % (-2.42 + dy, -2.66 + dy, -2.52 + dy, -2.34 + dy, -2.36 + dy, k.c(LEATHER["base"]), k.ink))
    stir = ('<path d="M0.46,%.4f L0.52,%.4f" stroke="%s" stroke-width="0.030"/><path d="M0.40,%.4f h0.24 v0.04 h-0.24 Z" fill="%s" stroke="%s" stroke-width="0.016"/>'
            % (-2.38 + dy, -1.32 + dy, k.c(LEATHER["dark"]), -1.32 + dy, k.c(IRON["base"]), k.ink))
    svg = '<g id="%s_horse"><defs>%s</defs>' % (k.uid, "@@DEFS@@") + far + tail + body + near + capar + mane + sad + head + rein + stir + "</g>"
    svg = svg.replace("@@DEFS@@", "".join(k.defs))
    xs = [e[0] for e in k.ext] + [-1.8, 2.9]
    ys = [e[1] for e in k.ext] + [-4.0, 0.15]
    bbox = (min(xs) - 0.1, min(ys) - 0.1, max(xs) + 0.1, max(ys) + 0.1)
    seat = (HORSE_SEAT[0], HORSE_SEAT[1] + dy)
    an = dict(feet=(0.0, 0.0), seat=seat, hip=(seat[0], seat[1] + 0.02), head=(P0[0] + 0.45, P0[1] + 0.6), head_top=(P0[0], P0[1] - 0.4), hat_top=(P0[0], P0[1] - 0.5),
              stirrup=(0.52, -1.30 + dy), withers=(0.95, -2.55 + dy), croup=(-1.3, -2.45 + dy), muzzle=(P0[0] + 0.95, P0[1] + 1.05),
              tail_root=(-1.58, -2.30 + dy), hand_r=(1.3, -2.7), hand_l=(1.3, -2.7), mouth=(P0[0] + 0.8, P0[1] + 1.05), foot_r=(0.9, 0.0), foot_l=(-1.1, 0.0))
    return svg, bbox, an


def horse_pose(phase=0.0, mode="walk", cap="red", **kw):
    """a pose dict for puppet.figure("horse", pose)."""
    return dict(gait=phase, mode21=mode, horse21=cap, **kw)


# ============================================================================= figure wrapper: horse cards, riders, swimmers, floating helmets, colour variants
HORSE_KEYS = ("horse",)
MOUNTED = {"%s_mtd" % n: n for n in ("knight_a", "knight_a_open", "knight_b", "knight_b_great", "surrey", "moray")}
SPECIAL21 = HORSE_KEYS + ("helmet_float",) + tuple(MOUNTED)
DEFAULT_CAP = {"knight_a": "red", "knight_a_open": "red", "knight_b": "blue", "knight_b_great": "blue", "surrey": "gold", "moray": "plain"}
RIDER_KEYS = ("gait", "mode21", "horse21", "ride21")


def _mirror_anchors(an, mir):
    if not mir:
        return an
    out = {}
    for n, v in an.items():
        nn = n
        if n.endswith("_r"):
            nn = n[:-2] + "_l"
        elif n.endswith("_l"):
            nn = n[:-2] + "_r"
        out[nn] = (-v[0], v[1])
    return out


def _wrap_card(svg, bbox, an, feet_y, mir):
    if mir:
        svg = '<g transform="scale(-1 1)">%s</g>' % svg
        bbox = (-bbox[2], bbox[1], -bbox[0], bbox[3])
        an = _mirror_anchors(an, True)
    return dict(svg=svg, feet_y=feet_y, bbox=tuple(bbox), anchors=an)


def _horse_card(pose, uid):
    ink = pose.get("ink") if P._is_hex(pose.get("ink")) else P.INK
    tint = pose.get("tint") if P._is_hex(pose.get("tint")) else None
    cap = pose.get("horse21") if isinstance(pose.get("horse21"), str) and pose.get("horse21") in HORSE_COATS else "red"
    mode = "idle" if pose.get("mode21") == "idle" else "walk"
    svg, bb, an = horse_parts(uid, _f(pose.get("gait"), 0.0, -1e6, 1e6), mode, cap, _f(pose.get("t"), 0.0, -1e6, 1e6), ink, tint)
    return _wrap_card(svg, bb, an, 0.0, bool(pose.get("mirror")))


def _rider_pose(base, pose, horse_seat_dy=0.0):
    p = dict((k_, v) for k_, v in pose.items() if k_ not in RIDER_KEYS and k_ != "mirror")
    p.setdefault("yaw", 0.9)
    p.setdefault("expr", "neutral")
    p.setdefault("mouth", "flat")
    p.setdefault("arm_r", dict(hand=(0.80, 0.90), bend=0.3, layer="front"))
    p.setdefault("arm_l", "akimbo")
    if "legs" not in p:
        probe = _O21["figure"](base, dict(p, legs="stand"), "pq")
        hx, hy = probe["anchors"]["hip"]
        p["legs"] = dict(foot_r=(hx + 0.62, hy + 1.04), foot_l=(hx + 0.50, hy + 1.00), knee_r=1.0, knee_l=1.0, toe_r=0.4, toe_l=0.4)
    return p


def _mounted(name, pose, uid):
    base = MOUNTED[name]
    mir = bool(pose.get("mirror"))
    cap = pose.get("horse21") if isinstance(pose.get("horse21"), str) and pose.get("horse21") in HORSE_COATS else DEFAULT_CAP[base]
    mode = "idle" if pose.get("mode21") == "idle" else "walk"
    ink = pose.get("ink") if P._is_hex(pose.get("ink")) else P.INK
    tint = pose.get("tint") if P._is_hex(pose.get("tint")) else None
    hs, hb, han = horse_parts(uid + "h", _f(pose.get("gait"), 0.0, -1e6, 1e6), mode, cap, _f(pose.get("t"), 0.0, -1e6, 1e6), ink, tint)
    rp = _rider_pose(base, pose)
    if mir:
        rp["mirror"] = True
    rf = _O21["figure"](base, rp, uid + "r")
    seat = han["seat"]
    if mir:
        seat = (-seat[0], seat[1])
        hs = '<g transform="scale(-1 1)">%s</g>' % hs
        hb = (-hb[2], hb[1], -hb[0], hb[3])
        han = _mirror_anchors(han, True)
    hx, hy = rf["anchors"]["hip"]
    dx, dy = seat[0] - hx, seat[1] + 0.06 - hy
    svg = hs + '<g transform="translate(%.4f %.4f)">%s</g>' % (dx, dy, rf["svg"])
    an = dict(han)
    for n, v in rf["anchors"].items():
        an[n] = (v[0] + dx, v[1] + dy)
    an["feet"] = (0.0, 0.0)
    an["seat"] = seat
    an["horse_head"] = han.get("head")
    rb = rf["bbox"]
    bb = (min(hb[0], rb[0] + dx), min(hb[1], rb[1] + dy), max(hb[2], rb[2] + dx), max(hb[3], rb[3] + dy))
    return dict(svg=svg, feet_y=0.0, bbox=bb, anchors=an)


def _swim(name, pose, uid):
    depth = _f(pose.get("swim21"), 1.0, 0.4, 2.2)
    p = dict((k_, v) for k_, v in pose.items() if k_ != "swim21")
    f = _O21["figure"](name, p, uid)
    hx, hy = f["anchors"]["head"]
    wl = hy + depth
    cid = uid + "_wl"
    ink = pose.get("ink") if P._is_hex(pose.get("ink")) else P.INK
    k = _ctx(uid + "w", ink, pose.get("tint") if P._is_hex(pose.get("tint")) else None)
    ph = _f(pose.get("t"), 0.0, -1e6, 1e6) * 6.283
    rip = []
    foam = k.c("#f2fbfa")
    deep = k.c("#2a7f8c")
    rip.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="0.15" fill="%s" opacity="0.55"/>' % (hx, wl + 0.03, 0.80 + 0.04 * math.sin(ph), deep))
    for i, (rx, ry, op) in enumerate(((0.62, 0.10, 0.95), (0.88, 0.15, 0.75), (1.20, 0.21, 0.5))):
        w = 1.0 + 0.06 * math.sin(ph + i * 1.6)
        rip.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.032" opacity="%.2f"/>' % (hx, wl + 0.02, rx * w, ry * w, foam, op))
    for i in range(5):
        a = ph + i * 1.3
        rip.append('<path d="M%.4f,%.4f q0.026,0.040 0,0.062 q-0.026,-0.022 0,-0.062 Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
                   % (hx - 0.95 + 0.5 * i + 0.04 * math.sin(a), wl - 0.12 - 0.12 * ((a * 0.4) % 1.0), foam, k.ink))
    svg = ('<defs><clipPath id="%s"><rect x="-6" y="-8" width="12" height="%.4f"/></clipPath>%s</defs><g clip-path="url(#%s)">%s</g>%s'
           % (cid, wl + 8.0, "".join(k.defs), cid, f["svg"], "".join(rip)))
    an = dict(f["anchors"])
    an["feet"] = (hx, wl)
    an["hip"] = (hx, wl - 0.25)
    an["water"] = (hx, wl)
    bb = (min(f["bbox"][0], hx - 1.3), f["bbox"][1], max(f["bbox"][2], hx + 1.3), wl + 0.30)
    return dict(svg=svg, feet_y=wl, bbox=bb, anchors=an)


def _helmet_float(pose, uid):
    kind = pose.get("helm21") if isinstance(pose.get("helm21"), str) and pose.get("helm21") in ("kettle", "bascinet", "great") else "kettle"
    ink = pose.get("ink") if P._is_hex(pose.get("ink")) else P.INK
    k = _ctx(uid, ink, pose.get("tint") if P._is_hex(pose.get("tint")) else None)
    ph = _f(pose.get("t"), 0.0, -1e6, 1e6) * 6.283
    C = dict(hat_colors=KETTLE if kind != "great" else GREAT, hat_tilt=6.0 * math.sin(ph) + _f(pose.get("tilt"), -8.0, -60.0, 60.0))
    fn = {"kettle": C6._hat_kettlehat, "bascinet": _hat_bascinet21, "great": _hat_greathelm21}[kind]
    hat, top = fn(k, C, 0.0)
    wl = 0.0
    bob = 0.03 * math.sin(ph * 1.0 + 1.0)
    lift = {"kettle": 0.16, "bascinet": -0.25, "great": -0.30}[kind]
    foam = k.c("#f2fbfa")
    rip = ['<ellipse cx="0" cy="%.4f" rx="0.95" ry="0.14" fill="%s" opacity="0.55"/>' % (wl + 0.02, k.c("#2a7f8c"))]
    for i, (rx, ry, op) in enumerate(((0.80, 0.11, 0.95), (1.10, 0.17, 0.7), (1.45, 0.23, 0.45))):
        w = 1.0 + 0.06 * math.sin(ph + i * 1.6)
        rip.append('<ellipse cx="0" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.032" opacity="%.2f"/>' % (wl + 0.02, rx * w, ry * w, foam, op))
    cid = uid + "_hc"
    svg = ('<defs><clipPath id="%s"><rect x="-6" y="-8" width="12" height="%.4f"/></clipPath>%s</defs><g clip-path="url(#%s)"><g transform="translate(0 %.4f)">%s</g></g>%s'
           % (cid, wl + 8.0 + 0.0, "".join(k.defs), cid, wl + lift + bob, hat, "".join(rip)))
    bb = (-1.5, wl + lift - 1.2, 1.5, wl + 0.30)
    an = dict(feet=(0.0, wl), hip=(0.0, wl - 0.2), head=(0.0, wl - 0.5), head_top=(0.0, wl - 0.9), hat_top=(0.0, wl - 0.9), mouth=(0.0, wl - 0.3))
    return dict(svg=svg, feet_y=wl, bbox=bb, anchors=an)


def figure(cast_name, pose=None, uid="p"):
    pose_d = pose if isinstance(pose, dict) else {}
    name = cast_name
    if isinstance(name, str) and name in P.CAST:
        v = pose_d.get("variant21")
        if name in VARIANTS21 and isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v):
            name = VARIANTS21[name][int(v) % len(VARIANTS21[name])]
        if name == "horse":
            return _horse_card(pose_d, uid)
        if name == "helmet_float":
            return _helmet_float(pose_d, uid)
        if name in MOUNTED:
            return _mounted(name, pose_d, uid)
        if pose_d.get("swim21") is not None and P.CAST[name].get("_cast21"):
            return _swim(name, pose_d, uid)
    return _O21["figure"](name, pose, uid)


# ============================================================================= expressions, speech, laughing bounce
EXPR21 = {
    "neutral": dict(expr="neutral", mouth="flat"),
    "smug": dict(expr="smug", mouth="smirk", pitch=-0.35),
    "smirk": dict(expr="smirk", mouth="smirk"),
    "laughing": dict(expr="laughing", mouth="talk_b", pitch=-0.5, fx=["tears"]),
    "shocked": dict(expr="shocked", mouth="o"),
    "jawdrop": dict(expr="stunned", mouth=("open", 0.17, 0.22)),
    "worried": dict(expr="worried", mouth="wavy"),
    "sweat": dict(expr="worried", mouth="wavy", fx=["sweat"]),
    "tired": dict(expr="sad", mouth="flat", pitch=0.55),
    "angry": dict(expr="angry", mouth="frown", pitch=-0.4),
}
OPEN_FACES21 = ("laughing", "shocked", "jawdrop")


def with_expr(pose, name, **extra):
    """a copy of pose with one of the named faces (EXPR21: neutral, smug, smirk, laughing, shocked, jawdrop, worried, sweat, tired, angry).
    The mouth stays closed except laughing (fixed laugh drawing), shocked (round) and jawdrop."""
    p = dict(pose)
    p.pop("fx", None)
    p.update(EXPR21.get(name, EXPR21["neutral"]))
    p.update(extra)
    return p


def speak(pose, frame, level=1.0, seed=0, hold=2):
    """the pose with the mouth driven by talk_mouth(frame, level): the ONLY way a mouth opens and closes."""
    return dict(pose, mouth=talk_mouth(frame, level, seed, hold))


def silent(pose):
    return dict(pose, mouth="flat")


def bounce_dy(g, fps=30.0, hz=3.0, amp=0.06, phase=0.0):
    """laughing bounce: the figure's lift in D (up = positive), amp 0.06 D at 3 Hz (one hop every 10 frames at 30 fps)."""
    ph = 2.0 * math.pi * hz * g / fps + phase
    return amp * 0.5 * (1.0 - math.cos(ph))


def laugh(pose, g, fps=30.0, hz=3.0, amp=0.06, phase=0.0):
    """pose + laughing face + bounce at frame g.  Returns (pose, dy): put the card dy D higher (dy >= 0); the squash, the head roll and
    the head_dy bob are already in the pose.  The mouth is the fixed laugh drawing (no lip sync)."""
    ph = 2.0 * math.pi * hz * g / fps + phase
    c = 0.5 * (1.0 - math.cos(ph))
    p = with_expr(pose, "laughing")
    p["squash"] = (1.0 + 0.014 * (1 - c), 1.0 - 0.014 * (1 - c))
    p["head_roll"] = pose.get("head_roll", 0.0) + 4.0 * math.sin(ph * 0.5)
    p["head_dy"] = _clamp(pose.get("head_dy", 0.0) - 0.03 * c, -0.8, 0.8)
    p["t"] = (g * hz / fps) % 1.0
    return p, amp * c


# ============================================================================= story poses
STORY21, STORY21_META = {}, {}
SPEAR21 = dict(type="spear21", angle=-88)
ENGLISH = ("footman_a", "footman_b", "knight_a", "knight_a_open", "knight_b", "knight_b_great")
FOOT_ENG = ("footman_a", "footman_b")
SCOTS3 = ("scot_a", "scot_b", "scot_c")


def _grip_hand(S, name, hand_from="r", bend=0.4, layer="front", stretch=1.1):
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, layer=layer)


def _story():
    S, M = {}, {}
    folded = dict(yaw=0.30, arm_r=dict(hand=(0.52, 0.86), bend=0.5, layer="front"), arm_l=dict(hand=(0.42, 0.98), bend=0.8, layer="front"),
                  prop_r=dict(SPEAR21, angle=-90), legs="stand")
    # ---- the treasurer
    C = "cressingham"
    S["cressingham_neutral"] = (C, dict(yaw=0.25, pitch=-0.2, expr="smug", mouth="smirk", arm_r="hip", arm_l="down", legs="wide"))
    S["cressingham_smug_belt"] = (C, dict(yaw=0.20, pitch=-0.45, expr="smug", mouth="smirk", head_roll=-4, arm_r="akimbo", arm_l="akimbo", legs="wide"))
    S["cressingham_counting"] = (C, dict(yaw=0.45, pitch=0.55, expr="smug", mouth="smirk", lean=7, gaze=(0.3, 0.9),
                                         arm_r=dict(hand=(0.78, 1.00), bend=0.2, layer="front"), prop_r=dict(type="coin21", angle=-30, scale=2.0),
                                         arm_l=dict(hand=(0.30, 1.18), bend=0.6, shape="open", layer="front"), legs="wide"))
    S["cressingham_laughing"] = (C, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-7, t=0.3,
                                         arm_r=dict(hand=(0.52, 1.05), bend=0.9, shape="open", layer="front"), arm_l=dict(hand=(-0.50, 1.05), bend=0.9, shape="open", layer="front"),
                                         legs="wide"))
    S["cressingham_pointing"] = (C, dict(yaw=0.45, pitch=-0.35, expr="smug", mouth="flat", head_roll=6,
                                         arm_r=dict(hand=(1.18, 0.18), shape="point", bend=-0.5, stretch=1.3, layer="front"), arm_l="akimbo", legs="wide"))
    S["cressingham_purse_slap"] = (C, dict(yaw=0.40, pitch=-0.55, expr="smug", mouth="flat", lean=-5,
                                           arm_r=dict(hand=(1.12, -0.05), shape="open", bend=-0.7, stretch=1.3, layer="front"),
                                           arm_l=dict(hand=(0.40, 1.55), bend=0.3, shape="open", layer="front"), legs="wide"))
    S["cressingham_shocked"] = (C, dict(yaw=0.20, pitch=0.05, expr="shocked", mouth="o", fx=["sweat"], lean=-5, head_dy=0.03,
                                        arm_r=dict(hand=(0.88, 0.70), shape="open", bend=0.3), arm_l=dict(hand=(-0.88, 0.70), shape="open", bend=0.3), legs="stand"))
    S["cressingham_sweating"] = (C, dict(yaw=0.25, pitch=0.30, expr="worried", mouth="wavy", fx=["sweat"], gaze=(-0.6, 0.3),
                                         arm_r=dict(hand=(0.10, 0.92), bend=0.8, layer="front"), arm_l=dict(hand=(-0.12, 0.94), bend=0.8, layer="front"), legs="wide"))
    # ---- Earl Surrey
    R_ = "surrey"
    S["surrey_standing"] = (R_, dict(yaw=0.30, pitch=0.25, expr="neutral", mouth="flat", lean=4, head_roll=4, arm_r=dict(hand=(0.14, 1.05), bend=0.7, layer="front"),
                                     arm_l=dict(hand=(-0.14, 1.07), bend=0.7, layer="front"), legs="stand"))
    S["surrey_tired"] = (R_, dict(yaw=0.20, pitch=0.85, expr="sad", mouth="flat", head_roll=-6, head_dy=0.10, lean=10, squash=(1.0, 0.97),
                                  arm_r=dict(hand=(0.34, 1.34), bend=0.4), arm_l=dict(hand=(-0.26, 1.32), bend=0.4), legs="narrow"))
    S["surrey_listening"] = (R_, dict(yaw=0.45, pitch=0.1, expr="unimpressed", mouth="flat", head_roll=5, arm_r=dict(hand=(0.16, 0.62), shape="point", bend=0.8, layer="front"),
                                      arm_l=dict(hand=(0.02, 0.98), bend=0.6, layer="front"), legs="stand"))
    S["surrey_shocked"] = (R_, dict(yaw=0.20, expr="stunned", mouth=("open", 0.15, 0.22), fx=["sweat"], head_dy=0.03, lean=-5,
                                    arm_r=dict(hand=(0.80, 0.84), shape="open", bend=0.3), arm_l=dict(hand=(-0.80, 0.84), shape="open", bend=0.3), legs="stand"))
    S["surrey_worried"] = (R_, dict(yaw=0.30, pitch=0.2, expr="worried", mouth="wavy", fx=["sweat"], arm_r=dict(hand=(0.14, 1.05), bend=0.7), arm_l=dict(hand=(-0.14, 1.07), bend=0.7)))
    # ---- English soldiers and knights on foot
    for c in ENGLISH:
        S[c + "_stand"] = (c, dict(yaw=0.30, expr="neutral", mouth="flat", arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), arm_l="down", legs="stand"))
        S[c + "_stand_arms_down"] = (c, dict(yaw=0.20, expr="neutral", mouth="flat", arm_r="down", arm_l="down", legs="stand"))
        S[c + "_point_laugh"] = (c, dict(yaw=0.45, pitch=-0.5, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.4,
                                         arm_r=dict(hand=(1.12, 0.22), shape="point", bend=-0.5, stretch=1.3, layer="front"), arm_l=dict(hand=(-0.30, 1.0), bend=0.9, shape="open"), legs="wide"))
        S[c + "_laughing"] = (c, dict(yaw=0.20, pitch=-0.75, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.4,
                                      arm_r=dict(hand=(0.38, 1.02), bend=0.9, shape="open"), arm_l=dict(hand=(-0.38, 1.0), bend=0.9, shape="open"), legs="wide"))
        S[c + "_shocked"] = (c, dict(yaw=0.20, expr="shocked", mouth="o", fx=["sweat"], head_dy=0.03, lean=-4,
                                     arm_r=dict(hand=(0.82, 0.86), shape="open", bend=0.3), arm_l=dict(hand=(-0.82, 0.86), shape="open", bend=0.3), legs="stand"))
        S[c + "_worried"] = (c, dict(yaw=0.30, pitch=0.15, expr="worried", mouth="wavy", fx=["sweat"], head_roll=-4,
                                     arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), arm_l="down", legs="stand"))
        S[c + "_yawn"] = (c, dict(yaw=0.30, pitch=-0.2, expr="neutral", mouth=("open", 0.20, 0.20), head_roll=-5, arm_r=dict(hand=(0.30, 0.34), shape="open", bend=0.6, layer="top"),
                                  arm_l="down", legs="stand"))
        S[c + "_tiptoe"] = (c, dict(yaw=0.30, pitch=-0.3, expr="worried", mouth="flat", gaze=(0.8, -0.2), squash=(0.98, 1.03), lean=3,
                                    arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), arm_l=dict(hand=(0.10, 0.50), shape="open", bend=0.5, layer="front"),
                                    legs=dict(preset="stand", lift_r=0.2, lift_l=0.2)))
        S[c + "_bump"] = (c, dict(yaw=0.30, pitch=0.05, expr="shocked", mouth="o", head_roll=12, lean=-9, head_dy=0.04,
                                  arm_r=dict(hand=(0.74, 0.50), shape="open", bend=-0.3), arm_l=dict(hand=(-0.74, 0.62), shape="open", bend=0.2), legs=dict(preset="step", stride=-0.5)))
        # splash / jump poses
        S[c + "_jump_arms_up"] = (c, dict(yaw=0.25, pitch=-0.35, expr="excited", mouth=("open", 0.20, 0.18), head_roll=-5, squash=(0.98, 1.03),
                                          arm_r=dict(hand=(0.72, -0.62), shape="open", bend=-0.4, stretch=1.2, layer="top"),
                                          arm_l=dict(hand=(-0.72, -0.62), shape="open", bend=-0.4, stretch=1.2, layer="top"),
                                          legs=dict(preset="stand", lift_r=1.0, lift_l=0.7, knee_r=0.6, knee_l=0.5, crouch=0.25)))
        S[c + "_jump_pinch_nose"] = (c, dict(yaw=0.30, pitch=0.1, expr="shouting", mouth="flat", head_roll=4, squash=(1.0, 0.99),
                                             arm_r=dict(hand=(0.20, 0.14), bend=0.6, layer="top"), arm_l=dict(hand=(-0.86, 0.60), shape="open", bend=0.2, layer="front"),
                                             legs=dict(preset="stand", lift_r=0.9, lift_l=0.9, knee_r=0.5, knee_l=0.5, crouch=0.35)))
        S[c + "_jump_bomb"] = (c, dict(yaw=0.20, pitch=0.1, expr="shouting", mouth="flat", squash=(1.02, 0.97), lean=3,
                                       arm_r=dict(hand=(0.36, 1.45), bend=0.8, layer="front"), arm_l=dict(hand=(-0.36, 1.45), bend=0.8, layer="front"),
                                       legs=dict(preset="stand", lift_r=1.2, lift_l=1.2, knee_r=0.8, knee_l=0.8, crouch=0.5)))
        S[c + "_splutter"] = (c, dict(yaw=0.20, pitch=0.05, expr="shouting", mouth=("open", 0.22, 0.16), spit21=1.0, wet21=1.0, head_roll=-6, t=0.2,
                                      arm_r=dict(hand=(0.60, 0.90), shape="open", bend=0.4), arm_l=dict(hand=(-0.60, 0.90), shape="open", bend=0.4), legs="stand"))
        S[c + "_swim_bob"] = (c, dict(yaw=0.20, expr="worried", mouth="wavy", swim21=1.0, wet21=1.0, head_roll=-4, t=0.1, arm_r=dict(hand=(0.72, 0.70), bend=0.3), arm_l=dict(hand=(-0.72, 0.70), bend=0.3)))
        S[c + "_swim_splutter"] = (c, dict(yaw=0.20, expr="shouting", mouth=("open", 0.22, 0.16), spit21=1.0, wet21=1.0, swim21=0.95, head_roll=5, t=0.2,
                                           arm_r=dict(hand=(0.78, 0.55), shape="open", bend=0.3), arm_l=dict(hand=(-0.78, 0.55), shape="open", bend=0.3)))
        S[c + "_swim_arms_up"] = (c, dict(yaw=0.20, pitch=-0.2, expr="shocked", mouth="o", swim21=1.05, wet21=1.0, t=0.3,
                                          arm_r=dict(hand=(0.78, -0.50), shape="open", bend=-0.4, stretch=1.2, layer="top"), arm_l=dict(hand=(-0.74, -0.40), shape="open", bend=-0.4, stretch=1.2, layer="top")))
        S[c + "_swim_paddle"] = (c, dict(yaw=0.55, pitch=0.1, expr="worried", mouth="flat", swim21=1.0, wet21=1.0, t=0.4, head_roll=-3,
                                         arm_r=dict(hand=(1.05, 0.62), bend=-0.3, shape="open", layer="front"), arm_l=dict(hand=(-0.70, 0.75), bend=0.3, layer="front")))
    # a farmer mimed with a spear: both hands on the shaft, the point down, hoeing
    for c in FOOT_ENG:
        S[c + "_mime_hoe"] = (c, dict(yaw=0.50, pitch=0.1, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-6, lean=7, t=0.2,
                                      arm_r=dict(hand=(0.72, 1.02), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=62), legs="wide"))
        _grip_hand(S, c + "_mime_hoe")
    # ---- mounted riders (CAST keys base_mtd): the rider is parented to the horse; gait = walk phase
    for base in ("knight_a", "knight_b", "surrey", "moray"):
        key = base + "_mtd"
        S[base + "_mounted"] = (key, dict(yaw=0.9, expr="neutral", mouth="flat", gait=0.0))
        if base == "moray":
            continue                                   # the Scots never open their mouths
        S[base + "_mounted_laughing"] = (key, dict(yaw=0.7, pitch=-0.7, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.3, gait=0.0, mode21="idle"))
        S[base + "_mounted_shocked"] = (key, dict(yaw=0.7, expr="shocked", mouth="o", fx=["sweat"], gait=0.0, mode21="idle", lean=-4))
        S[base + "_mounted_suck_belly"] = (key, dict(yaw=0.8, pitch=0.1, expr="worried", mouth="flat", fx=["sweat"], squash=(0.90, 1.0), lean=-6, gait=0.0, mode21="idle"))
        S[base + "_mounted_yawn"] = (key, dict(yaw=0.8, pitch=-0.2, expr="neutral", mouth=("open", 0.20, 0.20), head_roll=-5, gait=0.0, mode21="idle"))
        S[base + "_mounted_wobble"] = (key, dict(yaw=0.7, expr="shocked", mouth="o", head_roll=14, lean=-10, gait=0.0))
    S["horse_walk"] = ("horse", dict(gait=0.0, horse21="red"))
    S["horse_idle"] = ("horse", dict(mode21="idle", horse21="blue", t=0.25))
    S["helmet_float_kettle"] = ("helmet_float", dict(helm21="kettle", t=0.2))
    S["helmet_float_great"] = ("helmet_float", dict(helm21="great", t=0.5))
    S["helmet_float_bascinet"] = ("helmet_float", dict(helm21="bascinet", t=0.7))
    # ---- Wallace
    W = "wallace"
    S["wallace_calm"] = (W, dict(yaw=0.25, pitch=-0.1, expr="neutral", mouth="flat", arm_r=dict(hand=(-0.40, 0.88), bend=0.7, layer="front"), arm_l=dict(hand=(0.34, 0.92), bend=0.7, layer="front"), legs="wide"))
    S["wallace_eyebrow"] = (W, dict(yaw=0.30, pitch=-0.2, expr="smug", mouth="flat", gaze=(0.5, 0.0), arm_r=dict(hand=(-0.40, 0.88), bend=0.7, layer="front"),
                                    arm_l=dict(hand=(0.34, 0.92), bend=0.7, layer="front"), legs="wide"))
    S["wallace_raise_sword"] = (W, dict(yaw=0.25, pitch=-0.45, expr="determined", mouth="flat", sheath21=0, lean=-4,
                                        arm_r=dict(hand=(0.62, -0.60), bend=-0.7, stretch=1.3, layer="top"), prop_r=dict(type="sword21", angle=-82), arm_l="akimbo", legs="wide"))
    S["wallace_run_sword"] = (W, dict(yaw=0.7, expr="determined", mouth="flat", sheath21=0, arm_r=dict(hand=(0.72, -0.40), bend=-0.6, stretch=1.3, layer="top"),
                                      prop_r=dict(type="sword21", angle=-70)))
    S["wallace_stand_spear"] = (W, dict(folded, expr="neutral", mouth="flat"))
    # ---- Moray
    S["moray_stand_spear"] = ("moray", dict(folded, expr="neutral", mouth="flat"))
    S["moray_calm"] = ("moray", dict(yaw=0.25, expr="determined", mouth="flat", arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), arm_l="akimbo", legs="wide"))
    # ---- Scots (never open their mouths)
    for c in SCOTS3 + ("scot_horn", "moray", "wallace"):
        S[c + "_fold_spear"] = (c, dict(folded, expr="neutral", mouth="flat"))
        S[c + "_spear_wall"] = (c, dict(yaw=0.85, pitch=0.0, expr="determined", mouth="flat", lean=9, arm_r=dict(hand=(0.92, 0.86), bend=0.3, layer="front"),
                                        prop_r=dict(SPEAR21, angle=-4), legs=dict(preset="step", stride=0.8, crouch=0.10)))
        _grip_hand(S, c + "_spear_wall", bend=0.3)
    for c in SCOTS3 + ("scot_horn",):
        S[c + "_chew_grass"] = (c, dict(folded, expr="neutral", mouth="flat", stalk21=1.0, pitch=-0.15, head_roll=-4))
        S[c + "_scratch_nose"] = (c, dict(yaw=0.45, expr="unimpressed", mouth="flat", head_roll=3, arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90),
                                          arm_l=dict(hand=(0.13, 0.16), shape="point", bend=0.7, layer="top"), legs="stand"))
        S[c + "_stand_still"] = (c, dict(yaw=0.30, expr="neutral", mouth="flat", arm_r=dict(hand=(0.54, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), arm_l="down", legs="stand"))
        S[c + "_shield"] = (c, dict(yaw=0.40, expr="determined", mouth="flat", shield21="ochre", arm_l=dict(hand=(-0.50, 0.92), bend=0.3, layer="front"), prop_l=dict(type="shield21"),
                                    arm_r=dict(hand=(0.60, 0.90), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90), legs="wide"))
    S["scot_horn_blow"] = ("scot_horn", dict(yaw=0.55, pitch=-0.25, expr="neutral", mouth="flat", puff21=1.0, lean=-5, head_roll=-3,
                                             arm_r=dict(hand=(0.16, 0.30), bend=-0.5, stretch=1.1, layer="top"), prop_r=dict(type="horn21", angle=-28),
                                             arm_l=dict(hand=(0.55, 0.40), bend=0.0, layer="top"), legs="wide"))
    S["scot_horn_lower"] = ("scot_horn", dict(yaw=0.40, expr="neutral", mouth="flat", arm_r=dict(hand=(0.40, 1.00), bend=0.4, layer="front"), prop_r=dict(type="horn21", angle=-80), arm_l="down", legs="stand"))
    for n, (c, p) in S.items():
        M[n] = dict(note="", lipsync=c == "cressingham" and n in ("cressingham_pointing", "cressingham_purse_slap", "cressingham_smug_belt", "cressingham_neutral"),
                    open_mouth=isinstance(p.get("mouth"), tuple) or p.get("mouth") in ("talk_a", "talk_b", "talk_o", "o"))
    return S, M


def run_spear(cast, phase, facing=1, prop="spear21", speed=1.0):
    """one frame of a run with the spear forward (Scots run down the hill): the spear in the near hand, the other arm swings."""
    base = dict(expr="determined", mouth="flat", yaw=0.75, arm_r=dict(hand=(0.95, 0.80), bend=0.3, layer="front"), prop_r=dict(type=prop, angle=-6))
    return cycle(cast, phase, "run", facing, base=base, arms="l", speed=speed)


def walk_spear(cast, phase, facing=1, mode="march"):
    """a marching / walking frame, spear carried upright in the near hand (English footmen, the column on the bridge)."""
    base = dict(expr="neutral", mouth="flat", yaw=0.75, arm_r=dict(hand=(0.60, 0.95), bend=0.4, layer="front"), prop_r=dict(SPEAR21, angle=-90))
    return cycle(cast, phase, mode, facing, base=base, arms="l")


def pose(name, **extra):
    c, p = STORY21[name]
    return c, dict(p, **extra)


def register():
    if getattr(P, "_cast21_registered", False):
        if not STORY21:
            s_, m_ = _story()
            STORY21.update(s_)
            STORY21_META.update(m_)
        return
    for name in ("_prop", "_face", "_norm", "figure"):
        _O21[name] = getattr(P, name)
    P.figure = figure
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    CE.COSTUMES.update(COSTUMES21)
    CE.HATS.update(HATS21)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS21 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP21)
    for n, c in NEW_CAST21.items():
        P.CAST[n] = c
    for n in SPECIAL21:                     # cards that figure() builds itself still need a CAST entry (sprites / tests look it up)
        P.CAST[n] = dict(NEW_CAST21["knight_a"], _special21=True)
    CE.CANVAS.update(CANVAS21)
    CE.CANVAS.update(CANVAS_SPECIAL21)
    P._cast21_registered = True

    s_, m_ = _story()
    STORY21.update(s_)
    STORY21_META.update(m_)
    P.STORY.update(STORY21)
    CE.register_stage()


register()
