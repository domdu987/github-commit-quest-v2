#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast24.py -- the cast of film 24 (Korea's turtle ship, Admiral Yi Sun-sin, 1592; comic and bloodless) for the v2 puppet,
as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast24"); import cast24   # registers on import (idempotent)
    import puppet
    cast, pose = cast24.STORY24["yi24_nod"]
    f = puppet.figure(cast, pose, "f")

Nothing older is edited.  Wrapped on top of cast10's wrappers (each falls through for everything it does not handle):
    _norm (pose keys wet24, hat_rot24, hat_dx24, ground24, plank24, spike_n24), _face (goatee, stubble, wet hair),
    _moustache (style neat24), _ink_limb (sode shoulder guards), _prop (katana24 .. oar24), figure (plank24, ground24).
New cast: yi24, jp_cmd24, ashi_a24..d24, kor_a24..d24.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10    # noqa: E402
import cast9 as C9      # noqa: E402
import cast8 as C8      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW24 = ("yi24", "jp_cmd24", "ashi_a24", "ashi_b24", "ashi_c24", "ashi_d24", "kor_a24", "kor_b24", "kor_c24", "kor_d24")
TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O24 = {}
_POSE24 = {"wet": 0.0, "hat_rot": 0.0, "hat_dx": 0.0, "ground": None, "plank": 0.0, "spikes": 5}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
BRASS = dict(light="#fff0a8", base="#e2b442", dark="#a07818", deep="#6a4c0c")
IRON = dict(light="#b4bcc4", base="#78828c", dark="#464e58", deep="#2a3038")
WOOD = dict(light="#e0b47a", base="#b07a44", dark="#6e4a26")
ROPE = dict(base="#d2b98a", dark="#8e7650")
LACQ = dict(light="#4a4650", base="#26222a", dark="#121016")
RED = "#c4283a"
GOLDK = dict(light="#fff0a8", base="#f0c040", dark="#b88a18")


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _drop(k, x, y, s=1.0):
    return ('<path d="M%.4f,%.4f q%.4f,%.4f 0,%.4f q%.4f,%.4f 0,%.4f Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
            % (x, y, -0.030 * s, 0.045 * s, 0.065 * s, 0.030 * s, -0.020 * s, -0.065 * s, k.c("#cfe6f6"), k.c("#4a6a8e")))


# ============================================================================= hats (head frame)
def _hat_gat24(k, C, yaw):
    """Yi's black wide-brim helmet-hat (jeonrip): a domed crown, a wide flat brim, a brass-bead hat band, a red plume
    tassel on top and a red chin cord."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.10 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    yb = -0.30
    g = CE._gradient(k, "g24", dict(light=col["light"], base=col["base"], dark=col["dark"]), x0=-0.8, x1=0.8, mid=0.32)
    # tassel behind the crown (hangs down the back side)
    s = -1.0 if yaw >= 0 else 1.0
    # brim
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.80" ry="0.165" fill="%s" stroke="%s" stroke-width="0.026"/>' % (dx, yb, g, k.ink))
    # crown dome
    crown = [(dx - 0.40, yb - 0.02), (dx - 0.36, yb - 0.24), (dx - 0.20, yb - 0.38), (dx, yb - 0.42), (dx + 0.20, yb - 0.38), (dx + 0.36, yb - 0.24), (dx + 0.40, yb - 0.02)]
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(crown), g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.30, yb - 0.14, dx - 0.22, yb - 0.30, dx - 0.04, yb - 0.36, k.c(col["light"])))
    # brim front edge highlight and band of brass beads
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>'
             % (dx - 0.66, yb + 0.05, dx, yb + 0.17, dx + 0.66, yb + 0.05, k.c(col["light"])))
    for i in range(7):
        t = i / 6.0
        x = dx - 0.37 + 0.74 * t
        yy = yb - 0.02 + 0.045 * math.sin(math.pi * t)
        o.append(_circ((x, yy), 0.026, k.c(BRASS["base"]), k, 0.008))
    # plume: knob and a red tassel hanging to the side
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.040" fill="%s" stroke="%s" stroke-width="0.014"/>' % (dx, yb - 0.44, k.c(BRASS["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (dx, yb - 0.47, dx + s * 0.20, yb - 0.62, dx + s * 0.34, yb - 0.36, dx + s * 0.30, yb - 0.30, dx + s * 0.06, yb - 0.45, k.c(col["tassel"]), k.ink))
    for j in range(4):
        o.append('<path d="M%.4f,%.4f q%.4f,0.05 %.4f,0.14" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
                 % (dx + s * (0.14 + 0.05 * j), yb - 0.42 + 0.01 * j, s * 0.01, s * 0.012 * j, k.c(P._shade(col["tassel"], 0.7))))
    # chin cord
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                 % (dx + sx * 0.54, yb + 0.10, dx + sx * 0.50, 0.15, dx + sx * 0.30, 0.50, k.c(col["tassel"])))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.82, yb), (dx + 0.82, yb), (dx, yb - 0.46), (dx + s * 0.34, yb - 0.30)))
    return "".join(o), (dx, yb - 0.46)


def _hat_kabuto24(k, C, yaw):
    """kabuto: black lacquer bowl with red-laced neck guard flaring at the sides and a tall gold crescent (maedate); pose
    hat_rot24 / hat_dx24 turn it askew, wet24 hangs wet locks and a bit of seaweed from it."""
    col = C["hat_colors"]
    dx = -0.03 * yaw + _POSE24["hat_dx"]
    rot = C["hat_tilt"] + _POSE24["hat_rot"]
    o = ['<g transform="rotate(%.3f)">' % rot]
    g = CE._gradient(k, "kb", dict(light=LACQ["light"], base=LACQ["base"], dark=LACQ["dark"]), x0=-0.6, x1=0.6, mid=0.30)
    yb = -0.20
    # neck guard (shikoro) flaring tiers
    for i, (w, y0, y1) in enumerate(((0.74, -0.24, -0.04), (0.70, -0.20, 0.02))):
        d = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" % (dx - 0.47, y0, dx - w, y1 - 0.02, dx, y1 + 0.02 - 0.0, dx + w, y1 - 0.02, dx + 0.47, y0)
        if i == 0:
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, g, k.ink))
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (dx + sx * 0.52, -0.16, dx + sx * 0.66, -0.01, k.c(col["lace"])))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (dx + sx * 0.60, -0.20, dx + sx * 0.69, -0.04, k.c(col["lace"])))
    # bowl
    bowl = [(dx - 0.48, yb), (dx - 0.46, yb - 0.26), (dx - 0.28, yb - 0.46), (dx, yb - 0.52), (dx + 0.28, yb - 0.46), (dx + 0.46, yb - 0.26), (dx + 0.48, yb)]
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(bowl), g, k.ink))
    # ribs (red lacing lines) and rivets
    for i in range(-2, 3):
        x = dx + i * 0.15
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
                 % (dx + i * 0.04, yb - 0.50, x + i * 0.05, yb - 0.26, x + i * 0.02, yb - 0.01, k.c(col["lace"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.36, yb - 0.16, dx - 0.30, yb - 0.38, dx - 0.10, yb - 0.46, k.c(LACQ["light"])))
    # front brow band (visor) and red lace edge
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (dx - 0.50, yb - 0.02, dx, yb + 0.07, dx + 0.50, yb - 0.02, dx + 0.50, yb + 0.05, dx, yb + 0.15, dx - 0.50, yb + 0.05, k.c(col["lace"]), k.ink))
    # maedate: gold crescent horns on a base plate
    gold = k.c(GOLDK["base"])
    cres = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.06, yb - 0.46, dx - 0.40, yb - 0.50, dx - 0.58, yb - 1.10, dx - 0.40, yb - 0.86, dx - 0.26, yb - 0.80,
               dx - 0.10, yb - 0.74, dx, yb - 0.70, dx + 0.10, yb - 0.74, dx + 0.26, yb - 0.80))
    # symmetric build: left horn, right horn, central boss
    for sx in (-1, 1):
        h = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
             % (dx + sx * 0.04, yb - 0.46, dx + sx * 0.42, yb - 0.50, dx + sx * 0.60, yb - 1.12,
                dx + sx * 0.46, yb - 0.74, dx + sx * 0.30, yb - 0.62, dx + sx * 0.16, yb - 0.60, dx + sx * 0.04, yb - 0.60))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (h, gold, k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
                 % (dx + sx * 0.14, yb - 0.55, dx + sx * 0.44, yb - 0.60, dx + sx * 0.54, yb - 0.98, k.c(GOLDK["light"])))
    o.append(_circ((dx, yb - 0.50), 0.060, gold, k, 0.016))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.022" fill="%s"/>' % (dx, yb - 0.50, k.c(RED)))
    if _POSE24["wet"] > 0.05:
        w = _POSE24["wet"]
        # wet locks hanging under the helmet and drips
        for sx in (-1, 1):
            for j, (x, ln) in enumerate(((0.40, 0.22), (0.30, 0.30))):
                o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
                         % (dx + sx * x, yb + 0.10, sx * 0.02, ln * 0.5, sx * 0.01, ln * w, k.ink))
        o.append(_drop(k, dx - 0.30, yb + 0.30 + 0.0, 1.0))
        o.append(_drop(k, dx + 0.42, 0.06, 0.9))
        # seaweed on the crescent
        o.append('<path d="M%.4f,%.4f q0.05,0.10 -0.03,0.18 q-0.07,0.08 0.00,0.16 q0.06,0.06 0.01,0.12" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
                 % (dx - 0.50, yb - 1.02, k.ink))
        o.append('<path d="M%.4f,%.4f q0.05,0.10 -0.03,0.18 q-0.07,0.08 0.00,0.16 q0.06,0.06 0.01,0.12" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
                 % (dx - 0.50, yb - 1.02, k.c("#4a8a3a")))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.70, 0.0), (dx + 0.70, 0.0), (dx - 0.60, yb - 1.12), (dx + 0.60, yb - 1.12), (dx, yb - 0.55)))
    return "".join(o), (dx, yb - 1.12)


def _hat_jingasa24(k, C, yaw):
    """ashigaru's conical lacquered hat (jingasa): a low cone with a rim, a mon disc and a chin cord."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    yb = -0.26
    h = C.get("cone_h", 0.62)
    rx = C.get("cone_w", 0.76)
    g = CE._gradient(k, "jg", dict(light=col["light"], base=col["base"], dark=col["dark"]), x0=-rx, x1=rx, mid=0.30)
    cone = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - rx, yb, dx, yb + 0.20, dx + rx, yb, dx + rx * 0.45, yb - h * 0.62, dx, yb - h, dx - rx * 0.45, yb - h * 0.62, dx - rx, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (cone, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>'
             % (dx - rx * 0.92, yb - 0.01, dx, yb + 0.15, dx + rx * 0.92, yb - 0.01, k.c(col["dark"])))
    for a in (-0.55, -0.25, 0.0, 0.25, 0.55):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.55"/>' % (dx + a * 0.06, yb - h + 0.03, dx + a * rx * 1.05, yb + 0.07 - 0.07 * abs(a), k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>'
             % (dx - rx * 0.30, yb - h * 0.50, dx - rx * 0.20, yb - h * 0.75, dx - 0.03, yb - h * 0.90, k.c(col["light"])))
    if C.get("mon24"):
        o.append(_circ((dx, yb - h * 0.38), 0.065, k.c(C["mon24"]), k, 0.014))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.026" fill="%s"/>' % (dx, yb - h * 0.38, k.c(col["base"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.012"/>' % (dx, yb - h - 0.005, k.c(IRON["base"]), k.ink))
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                 % (dx + sx * rx * 0.62, yb + 0.06, dx + sx * 0.50, 0.15, dx + sx * 0.28, 0.52, k.ink))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - rx - 0.02, yb), (dx + rx + 0.02, yb), (dx, yb - h - 0.02)))
    return "".join(o), (dx, yb - h)


def _hat_smallhat24(k, C, yaw):
    """a small black horsehair hat (gat): a short drum crown with a flat brim, tied under the chin."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    yb = -0.28
    g = CE._gradient(k, "sh", dict(light=col["light"], base=col["base"], dark=col["dark"]), x0=-0.5, x1=0.5, mid=0.30)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
             % (dx - 0.36, yb, dx - 0.31, yb - 0.30, dx, yb - 0.38, dx + 0.31, yb - 0.30, dx + 0.36, yb, g, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.56" ry="0.105" fill="%s" stroke="%s" stroke-width="0.024"/>' % (dx, yb, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>'
             % (dx - 0.22, yb - 0.18, dx - 0.18, yb - 0.30, dx, yb - 0.34, k.c(col["light"])))
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                 % (dx + sx * 0.42, yb + 0.06, dx + sx * 0.46, 0.20, dx + sx * 0.26, 0.50, k.c(col.get("cord", "#7a2a22"))))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.58, yb), (dx + 0.58, yb), (dx, yb - 0.40)))
    return "".join(o), (dx, yb - 0.39)


HATS24 = {"gat24": _hat_gat24, "kabuto24": _hat_kabuto24, "jingasa24": _hat_jingasa24, "smallhat24": _hat_smallhat24}


# ============================================================================= costumes (torso-local)
def _quilt(k, name, col, dark, w=0.12):
    u = k.uid
    k.defs.append('<pattern id="%s_%s" width="%.3f" height="%.3f" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
                  '<rect width="%.3f" height="%.3f" fill="none"/><path d="M0,0 L%.3f,0 M0,0 L0,%.3f" stroke="%s" stroke-width="0.010" opacity="0.75"/></pattern>'
                  % (u, name, w, w, w, w, w, w, k.c(dark)))
    return "url(#%s_%s)" % (u, name)


def _cos_joseon24(k, C, m):
    """Yi: maroon quilted gambeson coat with rows of brass studs, a blue lining showing at the open collar, a dark belt with a
    brass plate; the coat skirt to the knee, open at the front over its blue lining."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    q = _quilt(k, "q24", col["base"], col["dark"])
    o.append('<rect x="-0.8" y="0.2" width="1.6" height="1.8" fill="%s"/>' % q)
    # blue lining at the collar: a V and a band along the front opening
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (X(-0.22, 0.34) + X(0.22, 0.34) + X(0.0, 0.84) + (k.c(col["lining"]), k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (X(-0.10, 0.34) + X(0.10, 0.34) + X(0.0, 0.52) + (k.c("#f2ead8"), k.ink)))
    for s in (-1, 1):
        lp = [X(s * 0.20, 0.33), X(s * 0.30, 0.36), X(s * 0.08, 0.90), X(s * 0.0, 0.86)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["base"]), k.ink))
    o.append(_ln([X(0.0, 0.86), X(0.0, yB + 0.02)], k.ink, 0.016))
    # brass studs in a grid on both sides
    ys = [0.60 + 0.17 * i for i in range(6)]
    for i, y in enumerate(ys):
        if y > yB - 0.22:
            break
        for xx in (-0.32, -0.20, 0.20, 0.32) if i else (-0.30, 0.30):
            if abs(xx) > hw * 0.80:
                continue
            c = X(xx, y)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (c[0], c[1], k.c(BRASS["base"]), k.ink))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.008" fill="%s"/>' % (c[0] - 0.007, c[1] - 0.007, k.c(BRASS["light"])))
    # shoulder yoke line
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(-hw * 0.8, 0.44) + X(0.0, 0.50) + X(hw * 0.8, 0.44) + (k.c(col["dark"]),)))
    inside = "".join(o)
    yt = yB - 0.16
    hem = yB + C.get("coat_len", 0.50)
    a = hw * 0.985
    b = hw + C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "jc", X, yt, a, hem, b, g, sw=0.026, folds=((-0.20, yt + 0.16, -0.26, hem - 0.04), (0.20, yt + 0.16, 0.26, hem - 0.04)), fold_col=k.c(col["dark"]))]
    # open front showing the blue lining
    sl = [X(-0.045, yt + 0.02), X(0.045, yt + 0.02), X(0.075, hem - 0.01), X(-0.075, hem - 0.01)]
    ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(sl), k.c(col["lining"]), k.ink))
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" opacity="0.8"/>' % (X(-b * 0.92, hem - 0.08) + X(b * 0.92, hem - 0.08) + (k.c(col["lining"]),)))
    # belt
    yw = yB - 0.22
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.150"/>' % (band, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.122"/>' % (band, k.c(col["belt"])))
    bx, by = X(0.0, yw + 0.04)
    ov.append('<rect x="%.4f" y="%.4f" width="0.14" height="0.11" rx="0.02" fill="%s" stroke="%s" stroke-width="0.014"/>' % (bx - 0.07, by - 0.055, k.c(BRASS["base"]), k.ink))
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s"/>' % (bx, by, k.c(BRASS["light"])))
    return inside, "", "".join(ov)


def _scale_rows(k, X, hw, y0, y1, step, plate, lace, lacq_light, ink):
    o = []
    y = y0
    i = 0
    while y < y1 - 0.02:
        yy1 = min(y + step, y1)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012"/>'
                 % (X(-hw, y) + X(0.0, y + 0.02) + X(hw, y) + X(hw, yy1) + X(0.0, yy1 + 0.02) + X(-hw, yy1) + (plate, ink)))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.55"/>'
                 % (X(-hw * 0.9, y + 0.025) + X(0.0, y + 0.045) + X(hw * 0.9, y + 0.025) + (lacq_light,)))
        n = 7
        for j in range(n):
            xx = -hw * 0.86 + 1.72 * hw * j / (n - 1)
            c = X(xx, y)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (c[0], y + 0.01, X(xx, yy1)[0], yy1 - 0.005, lace))
        y = yy1
        i += 1
    return "".join(o)


def _cos_samurai24(k, C, m):
    """the commander's samurai armour: black lacquer plates in rows tied with red lacing, a red cord belt with a brass knot,
    a kimono collar at the neck; four hanging hip plates (kusazuri) in front."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    plate = k.c(col["base"])
    lace = k.c(col["lace"])
    o = ['<rect x="-0.9" y="0.2" width="1.8" height="1.8" fill="%s"/>' % plate]
    # kimono V collar
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (X(-0.22, 0.33) + X(0.22, 0.33) + X(0.0, 0.62) + (k.c(col["kimono"]), k.ink)))
    o.append(_scale_rows(k, X, hw * 0.98, 0.62, yB - 0.15, 0.115, plate, lace, k.c(LACQ["light"]), k.ink))
    # chest plate highlight
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.28"/>'
             % (X(-hw * 0.7, 0.70) + X(-hw * 0.55, 0.9) + X(-hw * 0.6, yB - 0.30)))
    # red cord crossing the chest (agemaki-like) and mon disc
    for s in (-1, 1):
        o.append(_ln([X(s * 0.18, 0.42), X(0.0, 0.70)], k.ink, 0.060))
        o.append(_ln([X(s * 0.18, 0.42), X(0.0, 0.70)], lace, 0.036))
    o.append(_circ(X(0.0, 0.74), 0.050, k.c(BRASS["base"]), k, 0.012))
    inside = "".join(o)
    # over: kusazuri skirt plates + belt
    yt = yB - 0.20
    hem = yB + C.get("skirt_len", 0.30)
    ov = []
    n = 4
    wtot = hw * 1.05
    for i in range(n):
        x0 = -wtot + 2 * wtot * i / n
        x1 = -wtot + 2 * wtot * (i + 1) / n
        d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (X(x0, yt) + X(x1, yt) + X(x1 + 0.03 * (i - 1.5) * 0.3 + 0.015, hem) + X(x0 + 0.03 * (i - 1.5) * 0.3 - 0.015, hem))
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, plate, k.ink))
        for yy in (yt + 0.10, yt + 0.20):
            ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (X(x0 + 0.01, yy) + X(x1 - 0.01, yy) + (lace,)))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (X((x0 + x1) / 2, yt + 0.02) + X((x0 + x1) / 2, hem - 0.02) + (lace,)))
        k.ext.append(X((x0 + x1) / 2, hem) + (0.03,))
    yw = yt + 0.02
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.130"/>' % (band, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.100"/>' % (band, lace))
    bx, by = X(0.0, yw + 0.04)
    ov.append(_circ((bx, by), 0.058, k.c(BRASS["base"]), k, 0.014))
    ov.append('<path d="M%.4f,%.4f q-0.03,0.12 -0.06,0.20 M%.4f,%.4f q0.03,0.12 0.06,0.20" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (bx, by, bx, by, k.ink))
    ov.append('<path d="M%.4f,%.4f q-0.03,0.12 -0.06,0.20 M%.4f,%.4f q0.03,0.12 0.06,0.20" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (bx, by, bx, by, lace))
    return inside, "", "".join(ov)


def _cos_ashigaru24(k, C, m):
    """ashigaru: a plain kimono with a simple chest armour (do) of riveted plates over it, rope ties and a short skirt of
    three plates; the kimono shows at the neck and below."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    do = k.c(col["do"])
    o = []
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (X(-0.22, 0.33) + X(0.22, 0.33) + X(0.0, 0.64) + (k.c(P._shade(col["base"], 0.8)), k.ink)))
    o.append(_ln([X(-0.20, 0.35), X(0.05, 0.62)], k.c(col["collar"]), 0.026))
    o.append(_ln([X(0.20, 0.35), X(-0.02, 0.62)], k.c(col["collar"]), 0.026))
    # chest plate: shoulders straps and a big plate
    for s in (-1, 1):
        st = [X(s * hw * 0.62, TT + 0.10), X(s * hw * 0.34, 0.72)]
        o.append(_ln(st, k.ink, 0.074))
        o.append(_ln(st, do, 0.048))
    pl = [X(-hw * 0.74, 0.74), X(hw * 0.74, 0.74), X(hw * 0.80, yB - 0.10), X(-hw * 0.80, yB - 0.10)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (_poly_d(pl), do, k.ink))
    for i in range(1, 4):
        y = 0.74 + (yB - 0.10 - 0.74) * i / 4.0
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
                 % (X(-hw * 0.76, y) + X(0.0, y + 0.015) + X(hw * 0.76, y) + (k.c(P._shade(col["do"], 0.6)),)))
    for i in range(4):
        for j in range(5):
            xx = -hw * 0.62 + 1.24 * hw * j / 4.0
            y = 0.80 + (yB - 0.18 - 0.80) * i / 3.0
            c = X(xx, y)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.011" fill="%s"/>' % (c[0], c[1], k.c(col["rivet"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(0.0, 0.74) + X(0.0, yB - 0.10) + (k.c(P._shade(col["do"], 0.6)),)))
    inside = "".join(o)
    yt = yB - 0.16
    hem = yB + C.get("skirt_len", 0.20)
    ov = []
    wtot = hw * 0.98
    for i in range(3):
        x0 = -wtot + 2 * wtot * i / 3.0
        x1 = -wtot + 2 * wtot * (i + 1) / 3.0
        d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (X(x0, yt) + X(x1, yt) + X(x1 + 0.01, hem) + X(x0 - 0.01, hem))
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, do, k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (X(x0 + 0.01, yt + 0.09) + X(x1 - 0.01, yt + 0.09) + (k.c(P._shade(col["do"], 0.6)),)))
        k.ext.append(X((x0 + x1) / 2, hem) + (0.03,))
    yw = yt + 0.02
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.03) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.090"/>' % (band, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.062"/>' % (band, k.c(col["sash"])))
    return inside, "", "".join(ov)


def _cos_hanbok24(k, C, m):
    """Korean work clothes: an off-white jeogori jacket with a crossed collar (trim band) and a goreum ribbon tied on the chest,
    a cloth waist-band knot, a few creases; the baji trousers are the legs."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    tr = k.c(col["trim"])
    o = []
    for s in (-1, 1):
        p = [X(s * 0.22, 0.33), X(s * 0.08, 0.36), X(-s * 0.24, 0.82), X(-s * 0.34, 0.80)]
        # crossed collar bands: right-over-left
    o.append(_ln([X(-0.21, 0.34), X(0.20, 0.86)], k.ink, 0.070))
    o.append(_ln([X(-0.21, 0.34), X(0.20, 0.86)], tr, 0.044))
    o.append(_ln([X(0.21, 0.34), X(-0.14, 0.80)], k.ink, 0.070))
    o.append(_ln([X(0.21, 0.34), X(-0.14, 0.80)], tr, 0.044))
    # goreum: bow with two hanging tails
    c = X(-0.02, 0.74)
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f q%.4f,0.07 %.4f,0.0 q%.4f,-0.06 %.4f,0.0 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (c[0], c[1], sx * 0.06, sx * 0.12, sx * -0.05, sx * -0.12, k.c(col["tie"]), k.ink))
    o.append('<path d="M%.4f,%.4f q-0.02,0.12 -0.05,0.22 M%.4f,%.4f q0.02,0.11 0.03,0.20" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (c[0], c[1], c[0], c[1], k.ink))
    o.append('<path d="M%.4f,%.4f q-0.02,0.12 -0.05,0.22 M%.4f,%.4f q0.02,0.11 0.03,0.20" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (c[0], c[1], c[0], c[1], k.c(col["tie"])))
    o.append(_circ(c, 0.022, k.c(col["tie"]), k, 0.008))
    # creases
    for (x, y0, y1) in ((-0.30, 0.95, 1.20), (0.28, 0.98, 1.16), (0.06, 1.05, 1.25)):
        if y1 < yB:
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>'
                     % (X(x, y0) + X(x + 0.03, (y0 + y1) / 2) + X(x - 0.01, y1) + (k.c(col["dark"]),)))
    # waist band with a knot
    yw = yB - 0.12
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.03) + X(hw, yw))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.100"/>' % (band, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.072"/>' % (band, k.c(col["sash"])))
    kx, ky = X(0.12, yw + 0.03)
    o.append('<path d="M%.4f,%.4f q0.08,-0.04 0.10,0.04 q-0.08,0.04 -0.10,-0.04 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (kx, ky, k.c(col["sash"]), k.ink))
    o.append('<path d="M%.4f,%.4f q0.02,0.10 0.0,0.16 M%.4f,%.4f q0.05,0.08 0.06,0.13" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.ink))
    o.append('<path d="M%.4f,%.4f q0.02,0.10 0.0,0.16 M%.4f,%.4f q0.05,0.08 0.06,0.13" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.c(col["sash"])))
    return "".join(o), "", ""


COSTUMES24 = {"joseon24": _cos_joseon24, "samurai24": _cos_samurai24, "ashigaru24": _cos_ashigaru24, "hanbok24": _cos_hanbok24}


# ============================================================================= face: goatee, stubble, neat moustache
def _face(k, C, P_, white):
    svg, L = _O24["_face"](k, C, P_, white)
    if C is None or not C.get("_cast24"):
        return svg, L
    over = []
    mx, my = L["mx"], L["my"]
    if C.get("stubble24"):
        col = k.c(C["stubble24"])
        dots = []
        for i in range(44):
            a, b = _hash(C["seed"], i), _hash(C["seed"], i + 70)
            x = mx - 0.40 + 0.80 * a
            y = my - 0.02 + 0.40 * b
            if (x - mx) ** 2 / 0.16 + (y - 0.05) ** 2 / 0.30 > 1.0 and y > 0.4:
                continue
            dots.append("M%.4f,%.4f l0.012,0.010" % (x, y))
        over.append('<g clip-path="url(#%s_hc)"><path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.85"/></g>' % (k.uid, "".join(dots), col))
    if C.get("goatee24"):
        gcol = C["goatee24"]
        gy = my + 0.075
        d = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
             % (mx - 0.085, gy, mx - 0.09, gy + 0.16, mx, gy + 0.27, mx + 0.09, gy + 0.16, mx + 0.085, gy, mx, gy + 0.045, mx - 0.085, gy))
        over.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(gcol), k.ink))
        over.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.6"/>'
                    % (mx - 0.03, gy + 0.07, mx - 0.02, gy + 0.19, mx + 0.03, gy + 0.07, mx + 0.02, gy + 0.19, k.c(P._shade(gcol, 1.8))))
    if _POSE24["wet"] > 0.05 and C.get("wet_hair24"):
        w = _POSE24["wet"]
        hc = k.c(C["hair"]["color"])
        # plastered fringe strands over the brow + drips from the chin
        for i, x in enumerate((-0.30, -0.15, 0.0, 0.15, 0.30)):
            over.append('<path d="M%.4f,-0.30 q%.4f,0.10 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x, 0.02 * (i - 2), 0.01 * (i - 2), 0.12 + 0.03 * (i % 2), hc))
        over.append(_drop(k, mx - 0.12, 0.46, 1.0))
        over.append(_drop(k, mx + 0.30, 0.20 + 0.1 * (1 - w), 0.8))
    if not over:
        return svg, L
    return svg + "".join(over), L


def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "neat24":
        return _O24["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#1e1a1e")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    # a neat, thin moustache: two slim wings curving down at the ends
    pts = [Q(0.0, -0.045), Q(-0.12, -0.062), Q(-0.24, -0.030), Q(-0.30, 0.050), Q(-0.27, 0.070), Q(-0.20, 0.010), Q(-0.10, 0.008), Q(0.0, 0.020),
           Q(0.10, 0.008), Q(0.20, 0.010), Q(0.27, 0.070), Q(0.30, 0.050), Q(0.24, -0.030), Q(0.12, -0.062)]
    d = P._smooth_closed(pts)
    k.ext.append(Q(-0.30, 0.07) + (0.03,))
    k.ext.append(Q(0.30, 0.07) + (0.03,))
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)


# ============================================================================= arms: sode (samurai shoulder guards)
def _sode(k, S, E, C):
    ang = math.degrees(math.atan2(E[1] - S[1], E[0] - S[0]))
    sz = C.get("sode24", 1.0)
    col = C["colors"]
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (S[0], S[1], ang, sz)]
    for i, x in enumerate((0.20, 0.12, 0.04)):
        d = "M%.4f,-0.20 L%.4f,-0.19 L%.4f,0.20 L%.4f,0.19 Z" % (x - 0.07, x + 0.07, x + 0.08, x - 0.07)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(LACQ["base"]), k.ink))
        o.append('<path d="M%.4f,-0.17 L%.4f,0.17" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x + 0.0, x + 0.0, k.c(col["lace"])))
        o.append('<path d="M%.4f,-0.15 L%.4f,-0.05" stroke="%s" stroke-width="0.012" opacity="0.5"/>' % (x - 0.05, x - 0.05, k.c(LACQ["light"])))
    o.append('<path d="M-0.06,-0.20 Q-0.14,0 -0.06,0.20" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % k.c(BRASS["base"]))
    o.append('</g>')
    for (x, y) in ((-0.12, -0.20), (-0.12, 0.20), (0.30, -0.20), (0.30, 0.20)):
        q = _rot(x * sz, y * sz, ang)
        k.ext.append((S[0] + q[0], S[1] + q[1], 0.03))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O24["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast24"):
        return out
    if tail is None and C.get("sode24"):
        out += _sode(k, S, E, C)
    return out


# ============================================================================= props
NEW_PROPS24 = ("katana24", "yari24", "gunbai24", "ladder24", "ladder_grip24", "spike24", "spike_bundle24", "hammer24", "mallet24", "rope24", "oar24")
NEW_TIP24 = {"katana24": 1.12, "yari24": 1.95, "gunbai24": 1.04, "ladder24": 1.9, "ladder_grip24": 0.0, "spike24": 0.55, "spike_bundle24": 0.55,
             "hammer24": 0.68, "mallet24": 0.62, "rope24": 0.40, "oar24": 2.3}
PROP_EXT24 = {"katana24": ((-0.25, -0.07), (-0.25, 0.07), (1.14, 0.0), (0.16, -0.07), (0.16, 0.07)),
              "yari24": ((-0.55, -0.03), (1.97, 0.0), (1.50, -0.12), (1.50, 0.12), (-0.55, 0.03)),
              "gunbai24": ((-0.27, 0.0), (0.62, -0.44), (0.62, 0.44), (1.06, 0.0)),
              "ladder24": ((-0.52, -0.02), (-0.52, 0.30), (1.92, -0.02), (1.92, 0.30)),
              "ladder_grip24": ((0.0, 0.0),),
              "spike24": ((-0.10, -0.06), (-0.10, 0.06), (0.57, 0.0)),
              "spike_bundle24": ((-0.12, -0.16), (-0.12, 0.16), (0.58, -0.14), (0.58, 0.14)),
              "hammer24": ((-0.28, -0.04), (0.55, -0.15), (0.82, -0.15), (0.82, 0.15), (0.55, 0.15)),
              "mallet24": ((-0.22, -0.04), (0.45, -0.16), (0.80, -0.16), (0.80, 0.16), (0.45, 0.16)),
              "rope24": ((-0.22, -0.02), (0.22, -0.02), (-0.22, 0.46), (0.22, 0.46)),
              "oar24": ((-0.85, -0.04), (2.32, -0.13), (2.32, 0.13), (1.5, 0.13))}


def _spike_body(k, x0=0.0, y=0.0):
    """one iron spike along +x: square head at x0 - 0.10, a tapered shank to a point at x0 + 0.55."""
    g = _lin(k, "sp%d" % int(y * 1000 + 500), IRON["base"], IRON["dark"], IRON["deep"], 0, y - 0.04, 0, y + 0.04)
    return ('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
            % (x0 - 0.10, y - 0.055, x0 - 0.04, y - 0.055, x0 - 0.04, y - 0.024, x0 + 0.55, y, x0 - 0.04, y + 0.024, x0 - 0.04, y + 0.055, x0 - 0.10, y + 0.055, g, k.ink)
            + '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.6"/>' % (x0 - 0.08, y - 0.035, x0 + 0.30, y - 0.006))


def _prop_body(k, kind, nspk=5):
    o = []
    if kind == "katana24":
        gh = _lin(k, "kh", "#4a3a5a", "#2e2438", "#1a141e", 0, -0.04, 0, 0.04)
        o.append('<path d="M-0.24,-0.034 L0.15,-0.034 L0.15,0.034 L-0.24,0.034 Q-0.27,0 -0.24,-0.034 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (gh, k.ink))
        for x in (-0.20, -0.14, -0.08, -0.02, 0.04, 0.10):
            o.append('<path d="M%.4f,-0.034 L%.4f,0.034" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (x, x + 0.03, k.c("#c8b8a0")))
        o.append('<ellipse cx="0.17" cy="0" rx="0.022" ry="0.085" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(BRASS["base"]), k.ink))
        gb = _lin(k, "kb", "#f4f6fa", "#b8c0ca", "#7e8894", 0, -0.04, 0, 0.04)
        o.append('<path d="M0.19,-0.030 Q0.62,-0.056 1.08,-0.062 L1.12,-0.010 Q0.64,0.020 0.19,0.030 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (gb, k.ink))
        o.append('<path d="M0.24,0.006 Q0.64,-0.012 1.06,-0.036" fill="none" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>')
    elif kind == "yari24":
        o.append('<path d="M-0.55,-0.026 L1.52,-0.020 L1.52,0.020 L-0.55,0.026 Q-0.58,0 -0.55,-0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink))
        o.append('<path d="M-0.50,-0.010 L1.48,-0.008" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["light"]))
        o.append('<path d="M1.50,-0.034 L1.58,-0.034 L1.58,0.034 L1.50,0.034 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(IRON["dark"]), k.ink))
        gb = _lin(k, "yb", "#f4f6fa", "#b8c0ca", "#7e8894", 0, -0.08, 0, 0.08)
        o.append('<path d="M1.58,-0.040 Q1.70,-0.090 1.95,0 Q1.70,0.090 1.58,0.040 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (gb, k.ink))
        o.append('<path d="M1.62,0 L1.88,0" stroke="#ffffff" stroke-width="0.008" opacity="0.7"/>')
        # red tassel under the head
        o.append('<path d="M1.46,0 Q1.42,0.12 1.44,0.22 Q1.50,0.14 1.52,0 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(RED), k.ink))
    elif kind == "gunbai24":
        o.append('<path d="M-0.26,-0.026 L0.30,-0.024 L0.30,0.024 L-0.26,0.026 Q-0.29,0 -0.26,-0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#6a3a22"), k.ink))
        o.append('<path d="M0.24,-0.02 L0.36,-0.02 L0.36,0.02 L0.24,0.02 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["base"]), k.ink))
        o.append('<circle cx="0.70" cy="0" r="0.37" fill="%s" stroke="%s" stroke-width="0.030"/>' % (k.c("#f4e6c0"), k.ink))
        o.append('<circle cx="0.70" cy="0" r="0.37" fill="none" stroke="%s" stroke-width="0.040" opacity="0.9"/>' % k.c("#26222a"))
        o.append('<circle cx="0.70" cy="0" r="0.37" fill="none" stroke="%s" stroke-width="0.010"/>' % k.c(BRASS["base"]))
        o.append('<circle cx="0.70" cy="0" r="0.17" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#c4283a"), k.ink))
        o.append('<path d="M0.45,-0.24 Q0.60,-0.34 0.82,-0.33" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>')
    elif kind in ("ladder24", "ladder_grip24"):
        if kind == "ladder24":
            for y in (0.0, 0.30):
                o.append('<path d="M-0.50,%.4f L1.90,%.4f" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % (y, y, k.ink))
                o.append('<path d="M-0.50,%.4f L1.90,%.4f" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>' % (y, y, k.c(WOOD["base"])))
                o.append('<path d="M-0.46,%.4f L1.86,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (y - 0.014, y - 0.014, k.c(WOOD["light"])))
            for i in range(9):
                x = -0.30 + 0.27 * i
                o.append('<path d="M%.4f,0.0 L%.4f,0.30" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (x, x, k.ink))
                o.append('<path d="M%.4f,0.0 L%.4f,0.30" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (x, x, k.c(WOOD["light"])))
    elif kind == "spike24":
        o.append(_spike_body(k))
    elif kind == "spike_bundle24":
        n = max(2, min(8, int(nspk)))
        for i in range(n):
            y = -0.13 + 0.26 * i / (n - 1)
            o.append(_spike_body(k, 0.0 - 0.01 * (i % 2), y))
        o.append('<path d="M0.16,-0.18 L0.16,0.18" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M0.16,-0.18 L0.16,0.18" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.c(ROPE["base"]))
        o.append('<path d="M0.145,-0.17 l0.03,0.04 M0.145,-0.10 l0.03,0.04 M0.145,-0.03 l0.03,0.04 M0.145,0.04 l0.03,0.04 M0.145,0.11 l0.03,0.04" stroke="%s" stroke-width="0.008"/>' % k.c(ROPE["dark"]))
    elif kind == "hammer24":
        o.append('<path d="M-0.27,-0.030 L0.60,-0.026 L0.60,0.026 L-0.27,0.030 Q-0.30,0 -0.27,-0.030 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink))
        gh = _lin(k, "hm", IRON["light"], IRON["base"], IRON["dark"], 0.5, -0.16, 0.5, 0.16)
        o.append('<path d="M0.52,-0.150 L0.84,-0.150 L0.84,0.150 L0.52,0.150 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gh, k.ink))
        o.append('<path d="M0.54,-0.12 L0.82,-0.12" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>')
        o.append('<path d="M0.52,-0.05 L0.84,-0.05" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(IRON["deep"]))
    elif kind == "mallet24":
        o.append('<path d="M-0.22,-0.028 L0.50,-0.024 L0.50,0.024 L-0.22,0.028 Q-0.25,0 -0.22,-0.028 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(WOOD["dark"]), k.ink))
        gh = _lin(k, "ml", WOOD["light"], WOOD["base"], WOOD["dark"], 0.5, -0.16, 0.5, 0.16)
        o.append('<path d="M0.46,-0.150 Q0.64,-0.175 0.82,-0.150 L0.82,0.150 Q0.64,0.175 0.46,0.150 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gh, k.ink))
        for x in (0.50, 0.78):
            o.append('<path d="M%.4f,-0.15 L%.4f,0.15" stroke="%s" stroke-width="0.030" opacity="0.9"/>' % (x, x, k.c(IRON["base"])))
    elif kind == "rope24":
        for i, r in enumerate((0.20, 0.15)):
            o.append('<ellipse cx="0" cy="0.22" rx="%.3f" ry="%.3f" fill="none" stroke="%s" stroke-width="0.048"/>' % (r, r * 1.15, k.ink))
        for i, r in enumerate((0.20, 0.15)):
            o.append('<ellipse cx="0" cy="0.22" rx="%.3f" ry="%.3f" fill="none" stroke="%s" stroke-width="0.030"/>' % (r, r * 1.15, k.c(ROPE["base"])))
        o.append('<path d="M-0.20,0.14 l0.03,0.04 M-0.17,0.30 l0.04,0.02 M0.20,0.16 l-0.03,0.04 M0.0,0.04 l0.04,0.0 M0.0,0.40 l0.04,0.0" stroke="%s" stroke-width="0.008"/>' % k.c(ROPE["dark"]))
        o.append('<path d="M0.18,0.30 q0.10,0.06 0.06,0.16" fill="none" stroke="%s" stroke-width="0.048" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M0.18,0.30 q0.10,0.06 0.06,0.16" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.c(ROPE["base"]))
    elif kind == "oar24":
        o.append('<path d="M-0.85,-0.030 L1.55,-0.034 L1.55,0.034 L-0.85,0.030 Q-0.88,0 -0.85,-0.030 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink))
        o.append(_circ((-0.86, 0.0), 0.040, k.c(WOOD["dark"]), k, 0.012))
        o.append('<path d="M1.50,-0.055 L2.28,-0.130 Q2.34,0 2.28,0.130 L1.50,0.055 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(WOOD["light"]), k.ink))
        o.append('<path d="M1.60,0 L2.24,0" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(WOOD["dark"]))
        o.append('<path d="M0.40,-0.044 L0.48,-0.044 L0.48,0.044 L0.40,0.044 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(ROPE["base"]), k.ink))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS24:
        return _O24["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    upright = kind == "rope24"
    a = 0.0 if upright else ang
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], a, sc, _prop_body(k, kind, _POSE24["spikes"]))
    for (x, y) in PROP_EXT24[kind]:
        qx, qy = _rot(x * sc, y * sc, a)
        k.ext.append((H[0] + qx, H[1] + qy, 0.03))
    tx, ty = _rot(NEW_TIP24[kind] * sc, 0.0, a) if not upright else (0.0, 0.40 * sc)
    tip = (H[0] + tx, H[1] + ty)
    an[kind[:-2] + "_" + key] = tip
    return o, tip


# ============================================================================= figure level: ground, plank
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE24["wet"] = _f(g("wet24"), 0.0, 0.0, 1.0)
    _POSE24["hat_rot"] = _f(g("hat_rot24"), 0.0, -90.0, 90.0)
    _POSE24["hat_dx"] = _f(g("hat_dx24"), 0.0, -0.5, 0.5)
    _POSE24["spikes"] = int(_f(g("spike_n24"), 5.0, 2.0, 8.0))
    return _O24["_norm"](C, pose)


def _plank24_svg(k, cx, y, w, th=0.20):
    """a floating wooden plank, seen from the side: top surface at y, th thick; planks edge-on with end grain, a crack, wet streaks."""
    x0, x1 = cx - w / 2, cx + w / 2
    gt = _lin(k, "pk24", "#d8b07a", "#b08452", "#76542e", x0, 0, x1, 0)
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
         % (x0, y, x1, y, x1 - 0.03, y + th, x0 + 0.03, y + th, gt, k.ink)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (x0 + 0.12, y + th * 0.42, x1 - 0.60, y + th * 0.42, k.c("#5a3e20")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % (x1 - 0.50, y + th * 0.70, x1 - 0.12, y + th * 0.70, k.c("#5a3e20")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>' % (x0 + 0.20, y + 0.020, x1 - 0.30, y + 0.020, k.c("#f2dcb0")))
    # end grain rings and a nail
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.020" ry="0.060" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (x1 - 0.03, y + th / 2, k.c("#5a3e20")))
    o.append(_circ((x0 + 0.30, y + th * 0.5), 0.016, k.c(IRON["base"]), k, 0.006))
    o.append(_circ((x1 - 0.40, y + th * 0.5), 0.016, k.c(IRON["base"]), k, 0.006))
    for x in (x0 + 0.9, x0 + 2.0, x1 - 1.0):
        o.append(_drop(k, x, y + th + 0.01, 0.8))
    return "".join(o), (x0, y, x1, y + th + 0.08)


def figure(cast_name, pose=None, uid="p"):
    f = _O24["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    gr = pose.get("ground24")
    pl = _f(pose.get("plank24"), 0.0, 0.0, 1.0)
    if gr is None and pl < 0.5:
        return f
    an = dict(f["anchors"])
    b = list(f["bbox"])
    svg = f["svg"]
    feet_y = f["feet_y"]
    if gr is not None:
        gy = _f(gr, feet_y, -5.0, 8.0)
        an["ground"] = (an["feet"][0], gy)
        feet_y = gy
        an["feet"] = (an["feet"][0], gy)
    if pl >= 0.5:
        k = P._Ctx(uid + "y", P.INK, None)
        w = _f(pose.get("plank_w24"), 4.6, 1.5, 8.0)
        cx = an["hip"][0] + _f(pose.get("plank_dx24"), 0.9, -3.0, 3.0) * (-1.0 if pose.get("mirror") else 1.0)
        ty = _f(pose.get("plank_top24"), feet_y - 0.20, -5.0, 8.0)
        s, bb = _plank24_svg(k, cx, ty, w)
        defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
        svg = defs + s + svg
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["plank_l"] = (bb[0], ty)
        an["plank_r"] = (bb[2], ty)
        an["plank_top"] = (cx, ty)
        feet_y = ty + 0.20
        an["ground"] = (cx, feet_y)
        an["feet"] = (cx, feet_y)
    return dict(f, svg=svg, bbox=tuple(b), anchors=an, feet_y=feet_y)


# ============================================================================= cast
_FLAGS = dict(_cast24=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)
HAIR = dict(color="#1e1a1e", front=0.06, grow=0.20, shine="#4a4a60")


def _m(**kw):
    d = dict(_FLAGS)
    d.update(kw)
    return d


NEW_CAST24 = {
    # Admiral Yi Sun-sin: calm, tall, slim; maroon quilted armour-coat with brass studs and a blue lining; black wide-brim hat with a
    # red plume; a neat thin moustache and a small goatee
    "yi24": _m(
        build="slim", seed=24.1,
        torso_w=0.66, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.78, hip_x=0.15, leg=1.42, stance=0.07, wide=0.26, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.052, mouth="dash", moustache=True, moustache_style="neat24", tache_scale=1.0, smirk_side=1, cheeks="#eca090",
        goatee24="#1e1a1e",
        hat="newsboy", hat_style="gat24", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#4a4650", base="#26222a", dark="#121016", tassel="#c4283a"),
        hair=dict(HAIR),
        costume="joseon24", coat_len=0.52, coat_flare=0.10,
        sleeve=dict(color="#8a2230", dark="#561420", cuff="#2c4f9a", len=0.84, w=0.170),
        shorts=dict(color="#3a2a34", dark="#221820", cuff="#3a2a34", len=0.92, w=0.14),
        boots=dict(color="#2a1a1e", cuff="#2a1a1e", h=0.12, toe=0.16),
        colors=dict(base="#8a2230", dark="#561420", lining="#2c4f9a", belt="#2a1a1e", pants="#3a2a34", moustache="#1e1a1e"),
    ),
    # the Japanese commander (comic composite): stout, big belly, black lacquer armour with red lacing and big shoulder guards, a
    # kabuto with a tall gold crescent, a bushy black moustache, angry brows
    "jp_cmd24": _m(
        build="stout", seed=91.3,
        torso_w=1.42, torso_h=1.20, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.06, stance=0.07, wide=0.32, limb_w=0.072,
        eye_y=0.000, brow="stroke", brow_th=0.095, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=1.55, smirk_side=1, cheeks="#ee7a68",
        chins=True,
        hat="newsboy", hat_style="kabuto24", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(lace="#c4283a"),
        hair=dict(color="#16121a", front=0.06, grow=0.20, shine="#4a4a60"), wet_hair24=True,
        costume="samurai24", skirt_len=0.34, sode24=1.3,
        sleeve=dict(color="#34428a", dark="#1e2858", cuff="#c4283a", len=0.84, w=0.200),
        shorts=dict(color="#2a2a46", dark="#181830", cuff="#2a2a46", len=0.90, w=0.17),
        boots=dict(color="#5a4a3a", cuff="#8a7a5a", h=0.12, toe=0.16),
        colors=dict(base="#26222a", dark="#121016", lace="#c4283a", kimono="#34428a", pants="#2a2a46", moustache="#16121a"),
    ),
}


def _ashi(name, seed, build, tw, th, profile, leg, arm, lw, hat_col, kimono, do, extra=None, **kw):
    d = _m(build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile, shift_pow=1.05,
           shoulder=(0.25 + 0.2 * (tw - 0.62), 0.48), arm=arm, hip_x=0.14 + 0.05 * (tw - 0.62), leg=leg, stance=0.06, wide=0.26, limb_w=lw,
           eye_y=0.030, brow="stroke", brow_th=0.060, mouth="dash", smirk_side=1, cheeks="#ee9078",
           hat="newsboy", hat_style="jingasa24", hat_tilt=-6.0, ear_pencil=False,
           hat_colors=hat_col, hair=dict(HAIR),
           costume="ashigaru24", skirt_len=0.18,
           sleeve=dict(color=kimono, dark=P._shade(kimono, 0.65), cuff=P._shade(kimono, 0.85), len=0.84, w=0.15 + 0.06 * (tw - 0.62)),
           shorts=dict(color="#4a4048", dark="#2c262c", cuff="#6a5a4a", len=0.80, w=0.14),
           boots=dict(color="#a08a5a", cuff="#a08a5a", h=0.05, toe=0.14, soft=True),
           colors=dict(base=kimono, collar=P._shade(kimono, 1.3), do=do, rivet="#c8c0b0", sash="#7a2a22", pants="#4a4048"))
    d.update(kw)
    return d


NEW_CAST24.update({
    # ashigaru a: tall and slim, blue kimono, dark brown hat, thin black moustache
    "ashi_a24": _ashi("a", 51.2, "slim", 0.62, 1.00, CE.PROFILE_ATHLETE, 1.40, 0.76, 0.056, dict(light="#8a6248", base="#5a3a2a", dark="#341e14"), "#3a5a9a", "#3a3238",
                      moustache=True, moustache_style="bushy", tache_scale=0.62, hat_tilt=-8.0, cone_h=0.60, cone_w=0.74),
    # b: short and round, brown kimono, red-brown hat, grey stubble
    "ashi_b24": _ashi("b", 66.7, "regular", 1.00, 0.92, CE.PROFILE_PEAR, 0.92, 0.70, 0.064, dict(light="#d0684a", base="#a8442c", dark="#6a2416"), "#8a5a3a", "#5a4a3a",
                      stubble24="#5a5660", hat_tilt=7.0, cone_h=0.50, cone_w=0.84, eye_y=0.010, mon24="#f2e6c0"),
    # c: medium, grey kimono, young and clean-faced, pale grey hat with a crest
    "ashi_c24": _ashi("c", 18.9, "regular", 0.78, 0.96, CE.PROFILE_ATHLETE, 1.14, 0.72, 0.058, dict(light="#b4bac4", base="#7a8088", dark="#4a5058"), "#6a7078", "#3a3a44",
                      brow="dome", brow_th=0.040, eye_y=0.050, cheeks="#f2a294", hat_tilt=-3.0, mon24="#c4283a", cone_h=0.56, cone_w=0.78),
    # d: lanky, bushy brows and a drooping moustache, black tall hat, dark teal-blue kimono
    "ashi_d24": _ashi("d", 83.4, "slim", 0.54, 1.08, CE.PROFILE_ATHLETE, 1.56, 0.80, 0.052, dict(light="#4a4650", base="#26222a", dark="#121016"), "#5e6a3a", "#4a4a44",
                      brow_th=0.095, moustache=True, moustache_style="bushy", tache_scale=1.0, hat_tilt=4.0, cone_h=0.78, cone_w=0.70, eye_y=0.020),
})


def _kor(seed, build, tw, th, profile, leg, arm, lw, hat_style, hat_colors, base, trim, tie, sash, pants, **kw):
    d = _m(build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile, shift_pow=1.05,
           shoulder=(0.25 + 0.2 * (tw - 0.62), 0.48), arm=arm, hip_x=0.14 + 0.05 * (tw - 0.62), leg=leg, stance=0.06, wide=0.26, limb_w=lw,
           eye_y=0.030, brow="stroke", brow_th=0.056, mouth="dash", smirk_side=1, cheeks="#ee9078", moustache=False,
           hat="newsboy", hat_style=hat_style, hat_tilt=-3.0, ear_pencil=False, hat_colors=hat_colors, band_tails=True,
           hair=dict(HAIR),
           costume="hanbok24",
           sleeve=dict(color=base, dark="#c8c0ae", cuff="#8a6a4a", len=0.48, w=0.15 + 0.06 * (tw - 0.62), roll=True),
           shorts=dict(color=pants, dark="#c8c0ae", cuff="#8a6a4a", len=0.84, w=0.17),
           boots=dict(color="#4a3a2a", cuff="#4a3a2a", h=0.05, toe=0.14, soft=True),
           colors=dict(base=base, dark="#cfc6b2", trim=trim, tie=tie, sash=sash, pants=pants))
    d.update(kw)
    return d


NEW_CAST24.update({
    # Korean workers: off-white hanbok work clothes, sleeves tied up.  a: topknot, medium; b: stout, small black hat, grey moustache;
    # c: young, short, white headband, freckles; d: tall, topknot with a blue band, stubble
    "kor_a24": _kor(12.6, "regular", 0.72, 0.98, CE.PROFILE_ATHLETE, 1.24, 0.74, 0.058, "topknot9", dict(), "#f4efe2", "#5a6a82", "#a8442c", "#8a6a4a", "#ece6d6"),
    "kor_b24": _kor(37.8, "stout", 1.04, 0.94, CE.PROFILE_PEAR, 0.98, 0.70, 0.066, "smallhat24", dict(light="#4a4650", base="#26222a", dark="#121016", cord="#7a2a22"),
                    "#efe8d6", "#7a4a3a", "#3a5a8a", "#5a6a8a", "#e8e0cc", moustache=True, moustache_style="bushy", tache_scale=0.80,
                    brow_th=0.072, cheeks="#e8826e"),
    "kor_c24": _kor(74.4, "slim", 0.60, 0.86, CE.PROFILE_ATHLETE, 1.06, 0.70, 0.054, "hachimaki", dict(band="#fbf8f0", dark="#b9b2a8"), "#f6f2e6", "#8a6a4a", "#3a8a6a", "#a8442c",
                    "#efe9d8", brow="dome", brow_th=0.040, eye_y=0.050, freckles=True, cheeks="#f2a294"),
    "kor_d24": _kor(29.1, "regular", 0.90, 1.04, CE.PROFILE_ATHLETE, 1.40, 0.78, 0.062, "topknot9", dict(band="#2c4a8a", dark="#18284e"), "#f0ebdc", "#5a4a3a", "#c4283a", "#3a5a8a",
                    "#e6dfcc", stubble24="#3a3640", brow_th=0.066, hat_tilt=5.0),
})

# ============================================================================= story poses
def _anch(c, p):
    return figure(c, p, "q")["anchors"]


def _bone(c):
    a = _anch(c, dict(legs="stand"))
    return math.hypot(a["knee_r"][0] - a["hip"][0], a["knee_r"][1] - a["hip"][1])


KNEE_SIGN = 0.9


def kneel_pose(c, p, front=0.10):
    """both knees on the ground, shins flat behind (side view); sets legs and ground24 (the ground line, head frame)."""
    a = _anch(c, dict(p, legs="stand"))
    hx, hy = a["hip"]
    b = _bone(c)
    g = hy + b * 0.97
    d = dict(p)
    kx = hx + front
    d["legs"] = dict(foot_r=(kx - b * 1.0, g), foot_l=(kx - 0.14 - b * 1.0, g), knee_r=KNEE_SIGN, knee_l=KNEE_SIGN, toe_r=0.2, toe_l=0.2)
    d["ground24"] = g
    return d


def crawl_pose(c, base, fwd="l"):
    """hands-and-knees crawl in side view (head to screen-right).  fwd 'l': left hand + right knee forward; 'r': the opposite."""
    a = _anch(c, base)
    hx, hy = a["hip"]
    sr, sl = a["shoulder_r"], a["shoulder_l"]
    b = _bone(c)
    g = hy + b * 0.93
    kf = 0.30
    if fwd == "l":
        hl, hr, kr, kl = (sl[0] + 0.62, g), (sr[0] - 0.10, g), hx + kf, hx - kf
    else:
        hr, hl, kl, kr = (sr[0] + 0.62, g), (sl[0] - 0.10, g), hx + kf, hx - kf
    d = dict(base)
    d["arm_r"] = dict(hand=hr, stretch=1.3, bend=0.3, layer="front")
    d["arm_l"] = dict(hand=hl, stretch=1.3, bend=0.3, layer="front")
    d["legs"] = dict(foot_r=(kr - b * 1.0, g), foot_l=(kl - b * 1.0, g), knee_r=-0.5, knee_l=-0.5, toe_r=0.2, toe_l=0.2)
    d["ground24"] = g
    return d


def _oar_hand(S, name, dist=0.62, bend=0.4):
    """second hand on the oar shaft, dist along it from the first hand."""
    c, p = S[name]
    f = figure(c, p, "q")
    h = f["anchors"]["hand_r"]
    ang = math.radians(p["prop_r"]["angle"])
    q = (h[0] + dist * math.cos(ang), h[1] + dist * math.sin(ang))
    p["arm_l"] = dict(hand=q, bend=bend, stretch=1.3, layer="top")


def _story():
    S, M = {}, {}
    Y, J = "yi24", "jp_cmd24"
    # --- Admiral Yi
    S["yi24_stand_arms_behind"] = (Y, dict(yaw=0.30, pitch=-0.10, expr="neutral", mouth="flat", arm_r="behind", arm_l="behind", legs="stand"))
    M["yi24_stand_arms_behind"] = dict(note="calm on the quay, arms behind his back (default pose of the film's first shots)")
    S["yi24_nod"] = (Y, dict(yaw=0.30, pitch=0.28, expr="neutral", mouth="flat", head_roll=5, head_dy=0.02, arm_r="behind", arm_l="behind", legs="stand"))
    M["yi24_nod"] = dict(note="the nod: this is the DOWN key (pitch 0.28, head_roll 5, head_dy 0.02). Animate pitch 0 -> 0.28 -> 0 over ~10 frames "
                              "(lerp_pose with the stand pose), mouth stays closed")
    S["yi24_point_forward"] = (Y, dict(yaw=0.45, pitch=-0.15, expr="determined", mouth="flat", head_roll=-3,
                                       arm_r=dict(hand=(1.12, 0.38), shape="point", bend=-0.4, stretch=1.3), arm_l="behind", legs="narrow"))
    M["yi24_point_forward"] = dict(note="command: pointing out ahead (screen-right; mirror=True for left), other arm behind; anchor prop_tip_r = the fingertip")
    S["yi24_satisfied_smile"] = (Y, dict(yaw=0.25, pitch=-0.12, expr="happy", mouth="smile", head_roll=-4, blink=0, arm_r="behind", arm_l="behind", legs="stand"))
    M["yi24_satisfied_smile"] = dict(note="quiet satisfied smile, arms behind")
    S["yi24_walk"] = (Y, cycle(Y, 0.30, "walk", base=dict(expr="neutral", pitch=-0.1)))
    # --- the Japanese commander
    S["jp_cmd24_laugh_big"] = (J, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                       arm_r=dict(hand=(0.44, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.48, 0.98), bend=0.9, shape="open"), legs="wide"))
    M["jp_cmd24_laugh_big"] = dict(note="belly laugh, head back, hands on the belly; open laugh mouth is HELD (no lip-sync). Animate squash (1.02, 0.98) <-> (0.99, 1.01) every 4 frames")
    S["jp_cmd24_point_mock"] = (J, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                        arm_r=dict(hand=(1.10, 0.12), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    M["jp_cmd24_point_mock"] = dict(lipsync=True, note="mocking point to screen-right (mirror=True for left), other hand on hip; LIP-SYNC mouth=talk_mouth(g) in 16.1-21.4 s, 'flat' otherwise")
    S["jp_cmd24_finger_up_promise"] = (J, dict(yaw=0.30, pitch=-0.40, expr="smug", mouth="talk_a", head_roll=-4, lean=-6,
                                               arm_r=dict(hand=(0.88, -0.50), shape="point", bend=-0.5, stretch=1.3),
                                               arm_l=dict(hand=(-0.26, 0.70), bend=0.8, shape="open", layer="front"), legs="wide", squash=(1.01, 0.99)))
    M["jp_cmd24_finger_up_promise"] = dict(lipsync=True, note="'I will crawl home myself!': index finger up, other hand on the chest; LIP-SYNC with talk_mouth()")
    S["jp_cmd24_shout_forward"] = (J, dict(yaw=0.40, pitch=-0.35, expr="shouting", mouth="talk_b", head_roll=6, lean=4,
                                           arm_r=dict(hand=(1.12, 0.10), bend=-0.4, stretch=1.3, layer="front"), prop_r=dict(type="gunbai24", angle=-25),
                                           arm_l="akimbo", legs="wide"))
    M["jp_cmd24_shout_forward"] = dict(lipsync=True, note="shouting 'Follow them, all of you!', arm out forward with the war fan (gunbai24, anchor gunbai_r = the fan's far edge), "
                                                          "other hand on hip; LIP-SYNC with talk_mouth(). Animate the fan angle -25 <-> -40 for emphasis")
    # lying on the plank
    base = dict(yaw=0.70, lean=72, head_roll=-12, expr="worried", mouth="smirk", wet24=1.0, hat_rot24=14, hat_dx24=0.05, fx=["sweat", "blush"], t=0.3)
    a = _anch(J, base)
    sr, sl = a["shoulder_r"], a["shoulder_l"]
    hx, hy = a["hip"]
    pt = 1.12
    pl = dict(base, plank24=1, plank_top24=pt, plank_w24=5.0, plank_dx24=0.6,
              arm_r=dict(hand=(sr[0] + 0.78, pt + 0.14), stretch=1.3, bend=0.3, layer="front"),
              arm_l=dict(hand=(sl[0] + 1.00, pt - 0.02), stretch=1.3, bend=-0.3, layer="top"),
              legs=dict(foot_r=(hx - 1.0, pt - 0.02), foot_l=(hx - 0.95, pt - 0.10), knee_r=-0.6, knee_l=-0.6))
    S["jp_cmd24_plank_cling"] = (J, pl)
    M["jp_cmd24_plank_cling"] = dict(note="lying on his belly along a floating plank, arms around it, wet hair + seaweed on the kabuto, kabuto askew, sheepish. pose key plank24=1 draws the "
                                          "plank (plank_w24 length 5.0 D, plank_top24, plank_dx24). Ground anchor = the plank's UNDERSIDE (the waterline): anchors['ground'] / "
                                          "feet_y. Plank top = anchors['plank_top']. Canvas CANVAS24_POSES")
    S["jp_cmd24_crawl_a"] = (J, crawl_pose(J, dict(yaw=0.70, lean=70, head_roll=-8, expr="worried", mouth="smirk", wet24=1.0, hat_rot24=14, hat_dx24=0.05, fx=["blush"]), "l"))
    S["jp_cmd24_crawl_b"] = (J, crawl_pose(J, dict(yaw=0.70, lean=70, head_roll=-8, expr="worried", mouth="smirk", wet24=1.0, hat_rot24=14, hat_dx24=0.05, fx=["blush"]), "r"))
    M["jp_cmd24_crawl_a"] = dict(note="crawl frame A (head to screen-right): LEFT hand + RIGHT knee forward. Alternate A/B while moving forward (hands and knees on the ground line anchors['ground'])")
    M["jp_cmd24_crawl_b"] = dict(note="crawl frame B: RIGHT hand + LEFT knee forward (the opposite of A)")
    S["jp_cmd24_walk"] = (J, cycle(J, 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    M["jp_cmd24_walk"] = dict(note="one frame of cast24.cycle('jp_cmd24', phase, 'walk')")
    # --- ashigaru
    AS = ("ashi_a24", "ashi_b24", "ashi_c24", "ashi_d24")
    for i, c in enumerate(AS):
        n = c[:-2]
        S[c + "_laugh_point"] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10 - 4 * i, lean=-5, t=0.4 + 0.1 * i,
                                         arm_r=dict(hand=(0.80, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
        S[c + "_sword_raise"] = (c, dict(yaw=0.40, pitch=-0.20, expr="determined" if i % 2 == 0 else "angry", mouth="clench", head_roll=-4, lean=-3,
                                         arm_r=dict(hand=(0.62, -0.46), bend=-0.7, stretch=1.2, layer="front"), prop_r=dict(type="katana24", angle=-78 - 6 * i),
                                         arm_l=dict(hand=(-0.36, 0.95), bend=0.5) if i % 2 else "akimbo", legs="wide"))
        S[c + "_peer_worried"] = (c, dict(yaw=0.45, pitch=0.75, expr="worried", fx=["sweat"], head_roll=4, lean=12, gaze=(0.5, 0.9),
                                          arm_r=dict(hand=(0.46, 1.10), bend=0.4), arm_l=dict(hand=(-0.30, 1.02), bend=0.4), legs=dict(preset="step", stride=0.3, crouch=0.10)))
        S[c + "_step_back"] = (c, dict(yaw=0.40, pitch=-0.10, expr="shocked", fx=["sweat"], head_roll=-6, lean=-9, gaze=(0.8, 0.2),
                                       arm_r=dict(hand=(0.80, 0.30), shape="open", bend=-0.3, stretch=1.2), arm_l=dict(hand=(0.55, 0.65), shape="open", bend=-0.2),
                                       legs=dict(preset="step", stride=-0.65, lift_l=0.15)))
        M[c + "_laugh_point"] = dict(note="pointing and laughing at the turtle ship (screen-right; mirror=True for left); bounce the figure 0.04 D at the hips, feet planted")
        M[c + "_sword_raise"] = dict(note="katana raised, ready to board (prop katana24, anchor katana_r = the blade tip); feet planted")
        M[c + "_peer_worried"] = dict(note="leaning over the rail looking down at the spikes, sweat drop; feet planted")
        M[c + "_step_back"] = dict(note="alarmed: leans back, open hands, one foot stepped back (animate with the walk cycle for the real step)")
        S[c + "_walk"] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
    S["ashi_c24_yari"] = ("ashi_c24", dict(yaw=0.35, expr="smug", head_roll=-3, arm_r=dict(hand=(0.46, 0.46), bend=0.3, stretch=1.1, layer="front"),
                                          prop_r=dict(type="yari24", angle=-86), arm_l="akimbo", legs="wide"))
    M["ashi_c24_yari"] = dict(note="standing guard with a yari (spear) planted upright; anchor yari_r = the spear tip")
    S["ashi_d24_ladder_front"] = ("ashi_d24", dict(yaw=0.55, expr="determined", lean=6, arm_r=dict(hand=(0.55, 0.62), bend=0.2, stretch=1.2, layer="front"),
                                                   prop_r=dict(type="ladder24", angle=-18), arm_l=dict(hand=(0.30, 0.90), bend=0.4, layer="front"), legs=dict(preset="step", stride=0.3)))
    S["ashi_b24_ladder_back"] = ("ashi_b24", dict(yaw=0.55, expr="worried", lean=4, arm_r=dict(hand=(0.55, 0.62), bend=0.2, stretch=1.2, layer="front"),
                                                  prop_r="ladder_grip24", arm_l=dict(hand=(0.30, 0.90), bend=0.4, layer="front"), legs=dict(preset="step", stride=0.3)))
    M["ashi_d24_ladder_front"] = dict(note="front carrier of the ladder: prop ladder24 (2.4 D long, angle -18, anchor ladder_r = far end). Pair with ashi_b24_ladder_back "
                                           "(ladder_grip24 draws nothing; place the back man so his hands meet the ladder at about 1.2 D behind the front man's hand). "
                                           "Both walk with cycle(); same ladder world transform")
    M["ashi_b24_ladder_back"] = dict(note="rear carrier of the ladder: hands only (the front man's ladder24 prop is the one ladder)")
    # --- Korean workers
    KR = ("kor_a24", "kor_b24", "kor_c24", "kor_d24")
    hams = {"kor_a24": "hammer24", "kor_b24": "mallet24", "kor_c24": "hammer24", "kor_d24": "hammer24"}
    for i, c in enumerate(KR):
        kn = kneel_pose(c, dict(yaw=0.65, pitch=0.30, expr="determined", head_roll=-4, lean=6, gaze=(0.4, 0.9), t=0.2,
                                arm_r=dict(hand=(0.60, -0.50), bend=-0.7, stretch=1.2, layer="front"), prop_r=dict(type=hams[c], angle=-70 + 4 * i),
                                arm_l=dict(hand=(0.74, 0.92), bend=0.2, layer="front", shape="open") if i != 2 else dict(hand=(0.90, 0.80), bend=0.2, layer="front"),
                                prop_l=dict(type="spike24", angle=78) if i == 2 else None))
        if i != 2:
            kn.pop("prop_l", None)
        S[c + "_kneel_hammer"] = (c, kn)
        M[c + "_kneel_hammer"] = dict(note="kneeling on the ship roof hammering a spike (screen-right; knees planted: anchors['ground'] = the roof surface under both knees; "
                                           "pose key ground24 sets feet_y/feet to it). Animate ONLY arm_r: raised hand (0.60, -0.50), prop angle -70  ->  strike hand (0.78, 0.62), "
                                           "prop angle 20 (3 frames down, 5 up). Canvas CANVAS24_POSES")
        S[c + "_stand_carry_spikes"] = (c, dict(yaw=0.40, expr="neutral" if i % 2 else "determined", lean=-3, spike_n24=5 + (i % 3),
                                                arm_r=dict(hand=(0.52, 0.80), bend=0.4, stretch=1.1, layer="front"), prop_r=dict(type="spike_bundle24", angle=-80 + 3 * i, scale=1.25),
                                                arm_l=dict(hand=(-0.40, 1.00), bend=0.3) if i != 1 else dict(hand=(0.30, 0.95), bend=0.4, layer="front"),
                                                prop_l=dict(type="rope24") if i == 3 else None, legs="stand"))
        if i != 3:
            S[c + "_stand_carry_spikes"][1].pop("prop_l", None)
        M[c + "_stand_carry_spikes"] = dict(note="standing with a bundle of iron spikes held upright at the shoulder (spike_bundle24; spike_n24 = how many); planted feet")
        S[c + "_row_oar"] = (c, dict(yaw=0.55, pitch=0.05, expr="determined", mouth="clench", head_roll=-4, lean=14, t=0.3,
                                     arm_r=dict(hand=(0.55, 0.50), bend=0.2, stretch=1.2, layer="front"), prop_r=dict(type="oar24", angle=38 - 4 * i),
                                     legs=dict(preset="step", stride=0.35, crouch=0.08)))
        M[c + "_row_oar"] = dict(note="rowing: both hands on the oar (oar24, anchor oar_r = the blade). Animate lean 14 -> 4 and the oar angle 38 -> 20 for the pull; planted feet")
        S[c + "_cheer"] = (c, dict(yaw=0.20, pitch=-0.35, expr="excited" if i % 2 else "happy", mouth=("open", 0.22, 0.17) if i % 2 == 0 else None, head_roll=6 - 3 * i, t=0.3,
                                   arm_r=dict(hand=(0.70, -0.62), shape="open", bend=-0.6, stretch=1.3, layer="top"),
                                   arm_l=dict(hand=(-0.70, -0.55), shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide", squash=(0.99, 1.02)))
        if S[c + "_cheer"][1]["mouth"] is None:
            S[c + "_cheer"][1].pop("mouth")
        M[c + "_cheer"] = dict(note="both arms up cheering; bounce squash (0.99, 1.02) <-> (1.01, 0.98); held mouth, no lip-sync")
        S[c + "_walk"] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
    for c in KR:
        _oar_hand(S, c + "_row_oar")
    S["kor_c24_stand_rope"] = ("kor_c24", dict(yaw=0.35, expr="happy", arm_r=dict(hand=(0.40, 0.95), bend=0.3), prop_r=dict(type="rope24"), arm_l="akimbo", legs="stand"))
    M["kor_c24_stand_rope"] = dict(note="standing with a coil of rope hanging from the hand (rope24, always upright)")
    for n in list(S):
        if n.endswith("_walk"):
            M.setdefault(n, dict(note="one frame (phase 0.30) of cast24.cycle(); animate cycle(cast, frame / 28, 'walk', facing, base, arms)"))
    return S, M


STORY24, STORY24_META = {}, {}
WIDE24 = ("row_oar", "ladder")      # poses whose props reach far: own canvas in CANVAS24_POSES
CANVAS24 = {
    'yi24': (-1.8125, -4.75, 1.8125, 0.125),
    'jp_cmd24': (-2.25, -4.9375, 2.25, 0.125),
    'ashi_a24': (-1.8125, -4.75, 1.8125, 0.125),
    'ashi_b24': (-1.875, -4.125, 1.875, 0.125),
    'ashi_c24': (-1.875, -4.375, 1.875, 0.125),
    'ashi_d24': (-1.8125, -5.0625, 1.8125, 0.125),
    'kor_a24': (-1.8125, -4.5, 1.8125, 0.125),
    'kor_b24': (-1.875, -4.1875, 1.875, 0.125),
    'kor_c24': (-1.8125, -4.1875, 1.8125, 0.125),
    'kor_d24': (-1.875, -4.6875, 1.875, 0.125),
}
# per-pose canvases (feet-relative, D): kneel / crawl / plank / long props. For kneel, crawl and the plank, feet = the GROUND anchor (knees and hands
# on it; the plank's underside), so the canvas bottom is just below it.
CANVAS24_POSES = {
    'jp_cmd24_plank_cling': (-2.5, -3.1875, 2.5, 0.6875),
    'jp_cmd24_crawl_a': (-2.8125, -2.875, 2.8125, 0.9375),
    'jp_cmd24_crawl_b': (-2.8125, -2.875, 2.8125, 0.9375),
    'ashi_d24_ladder_front': (-2.6875, -4.375, 2.6875, 0.125),
    'ashi_b24_ladder_back': (-1.0, -3.375, 1.0, 0.125),
    'kor_a24_kneel_hammer': (-2.4375, -3.5, 2.4375, 0.1875),
    'kor_b24_kneel_hammer': (-2.3125, -3.25, 2.3125, 0.1875),
    'kor_c24_kneel_hammer': (-2.3125, -3.1875, 2.3125, 0.1875),
    'kor_d24_kneel_hammer': (-2.5, -3.625, 2.5, 0.1875),
    'kor_a24_row_oar': (-2.8125, -3.5625, 2.8125, 0.125),
    'kor_b24_row_oar': (-2.9375, -3.25, 2.9375, 0.125),
    'kor_c24_row_oar': (-3.0, -3.25, 3.0, 0.125),
    'kor_d24_row_oar': (-3.0625, -3.8125, 3.0625, 0.125),
}


# ============================================================================= registration
def register():
    if getattr(P, "_cast24_registered", False):
        CE.register_stage()
        if not STORY24:
            sd, md = _story()
            STORY24.update(sd)
            STORY24_META.update(md)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_ink_limb", "figure"):
        _O24[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    P.figure = figure
    CE.COSTUMES.update(COSTUMES24)
    CE.HATS.update(HATS24)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS24 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP24)
    for n, c in NEW_CAST24.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS24)
    P._cast24_registered = True
    sd, md = _story()
    STORY24.update(sd)
    STORY24_META.update(md)
    P.STORY.update(STORY24)
    CE.register_stage()


register()
