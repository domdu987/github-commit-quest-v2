#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast25.py -- the cast of film 25 (Britain's first tank, Mark I, 1915-16, ending at Flers 15 Sep 1916; comic and bloodless) for
the v2 puppet, as an extension module on top of cast24 (which chains cast10 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast25"); import cast25     # registers on import (idempotent)
    import puppet
    cast, pose = cast25.STORY25["general25_laugh"]
    f = puppet.figure(cast, pose, "f")

Nothing older is edited.  Wrapped on top of cast24's wrappers (each falls through for everything it does not handle):
    _norm (pose keys hat_off25, hat_up25, mg_gy25, paint_col25, plan_dx25), _face (big beard), _moustache (walrus25, kaiser25,
    kitchener25, brush25), _ink_limb (puttees), _prop (hammer25 .. mg25), figure (nothing extra: ground stays the soles).
New cast: general25, engineer25, worker_a25..c25, tommy_a25..d25, german_a25..c25, pilot25.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast24")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast24 as C24    # noqa: E402
import cast10 as C10    # noqa: E402
import cast9 as C9      # noqa: E402
import cast8 as C8      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW25 = ("general25", "engineer25", "worker_a25", "worker_b25", "worker_c25", "tommy_a25", "tommy_b25", "tommy_c25", "tommy_d25",
         "german_a25", "german_b25", "german_c25", "pilot25")
TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_hash = C24._hash
_O25 = {}
_POSE25 = {"hat_off": 0.0, "hat_up": 0.0, "mg_gy": None, "paint": "white", "t": 0.0, "plan_dx": 1.25, "pour": 0.0, "dirt": 0.0, "swing": 0.0, "fire": 0.0, "glasses_dy": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
BRASS = dict(light="#fff6b0", base="#f6c21c", dark="#b8820a", deep="#6e4c06")
STEEL = dict(light="#b4bcc4", base="#78828c", dark="#464e58", deep="#2a3038")
GALV = dict(light="#eef2f4", base="#a9b4bc", dark="#66727c")
WOOD = dict(light="#e0b47a", base="#b07a44", dark="#6e4a26")
LEATHER = dict(light="#b8743c", base="#7a4624", dark="#4a2a14")
EARTH = dict(light="#b07c46", base="#7c5230", dark="#4c3018")
PAINTS = {"white": "#f4f0e4", "black": "#1c1a20", "red": "#e02a22", "green": "#3a8a4a", "grey": "#8a8e96"}


def _gl(k, name, light, base, dark, x0=-0.5, x1=0.5, mid=0.32):
    return CE._gradient(k, name, dict(light=light, base=base, dark=dark), x0=x0, x1=x1, mid=mid)


def _strap_chin(k, dx, col, y0=-0.26, x0=0.52, x1=0.30, y1=0.50, w=0.020):
    o = []
    for sx in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round"/>'
                 % (dx + sx * x0, y0, dx + sx * (x0 - 0.04), 0.20, dx + sx * x1, y1, col, w))
    return "".join(o)


# ============================================================================= hats (head frame)
def _bare(C):
    return "", (0.0, -0.484)


def _wrap(o, C, up):
    return '<g transform="translate(0 %.4f) rotate(%.3f)">' % (-up, C["hat_tilt"]) + "".join(o) + "</g>"


def _hat_brodie25(k, C, yaw):
    """Brodie steel helmet (1915-16 'soup plate'): a shallow bowl on a wide flat brim, matt drab-green steel with a rolled edge, a
    rivet at the crown, a leather chin strap; C['cover25'] = 'hessian' adds a hessian cover (cross-hatched weave)."""
    if _POSE25["hat_off"] > 0.5:
        return _bare(C)
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.10 * yaw
    o = []
    g = _gl(k, "bd", col["light"], col["base"], col["dark"], -0.66, 0.66, 0.30)
    yr = -0.30
    # brim (flat, wide), its front edge dipping over the brow
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.68" ry="0.125" fill="%s" stroke="%s" stroke-width="0.026"/>' % (dx, yr, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.62, yr + 0.03, fx, yr + 0.115, dx + 0.62, yr + 0.03, k.c(col["dark"])))
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.43, yr + 0.01, dx - 0.45, yr - 0.20, dx - 0.22, yr - 0.32, dx, yr - 0.32, dx + 0.22, yr - 0.32, dx + 0.45, yr - 0.20, dx + 0.43, yr + 0.01,
               fx, yr + 0.075, dx - 0.43, yr + 0.01))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (dome, g, k.ink))
    if C.get("cover25") == "hessian":
        k.defs.append('<clipPath id="%s_bc"><path d="%s"/></clipPath>' % (k.uid, dome))
        ln = []
        for i in range(-7, 8):
            ln.append("M%.4f,%.4f l0.26,-0.26 M%.4f,%.4f l0.26,0.26" % (dx + i * 0.09 - 0.13, yr + 0.03, dx + i * 0.09 - 0.13, yr - 0.29))
        o.append('<g clip-path="url(#%s_bc)"><path d="%s" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
                 '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.55"/></g>'
                 % (k.uid, "".join(ln), k.c(col["light"]), dx - 0.45, yr - 0.02, dx + 0.45, yr - 0.02, dx + 0.45, yr + 0.04, dx - 0.45, yr + 0.04, k.c(col["dark"])))
    else:
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>'
                 % (dx - 0.33, yr - 0.07, dx - 0.26, yr - 0.24, dx - 0.04, yr - 0.29, k.c(col["light"])))
        o.append(_circ((dx + 0.02, yr - 0.285), 0.018, k.c(col["dark"]), k, 0.008))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.42, yr - 0.005, fx, yr + 0.07, dx + 0.42, yr - 0.005, k.c(col["dark"])))
    for sx in (-1, 1):
        o.append(_circ((dx + sx * 0.58, yr + 0.01), 0.016, k.c(BRASS["dark"]), k, 0.006))
    h = _wrap(o, C, _POSE25["hat_up"])
    h = _strap_chin(k, dx, k.c(LEATHER["base"])) + h
    C4._ext_hat(k, C, ((dx - 0.70, yr), (dx + 0.70, yr), (dx, yr - 0.34), (fx, yr + 0.16)))
    return h, (dx, yr - 0.32 - _POSE25["hat_up"])


def _hat_pickel25(k, C, yaw):
    """Pickelhaube under its grey cloth field cover: a tall rounded bowl, a short brass spike through the cover, a stiff black
    leather peak in front, brass side bosses and a black chin strap; C['patch25'] = a plain colour patch on the front of the cover."""
    if _POSE25["hat_off"] > 0.5:
        return _bare(C)
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.12 * yaw
    yb = -0.27
    ht = C.get("hat_h", 0.50)
    o = []
    g = _gl(k, "pk", col["light"], col["base"], col["dark"], -0.5, 0.5, 0.30)
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.46, yb, dx - 0.50, yb - ht * 0.55, dx - 0.26, yb - ht, dx, yb - ht, dx + 0.26, yb - ht, dx + 0.50, yb - ht * 0.55, dx + 0.46, yb, fx, yb + 0.055, dx - 0.46, yb))
    # neck guard peeking at the sides, then the peak (front), then the bowl
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (dx - 0.48, yb - 0.02, dx - 0.56, yb + 0.07, dx + 0.56, yb + 0.07, dx + 0.48, yb - 0.02, k.c("#26222a"), k.ink))
    vis = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
           % (fx - 0.46, yb - 0.01, fx, yb + 0.055, fx + 0.46, yb - 0.01, fx + 0.40, yb + 0.14, fx, yb + 0.17, fx - 0.40, yb + 0.14, fx - 0.46, yb - 0.01))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (vis, k.c("#2a262e"), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.4"/>'
             % (fx - 0.26, yb + 0.085, fx - 0.10, yb + 0.12, fx + 0.06, yb + 0.12))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (dome, g, k.ink))
    # seams of the cloth cover: a centre seam and two side seams, short stitches
    for u in (-0.55, 0.0, 0.55):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.03 0.02" opacity="0.8"/>'
                 % (dx + u * 0.06, yb - ht + 0.03, dx + u * 0.34, yb - ht * 0.55, dx + u * 0.44 + 0.10 * yaw, yb - 0.01, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.65"/>'
             % (dx - 0.38, yb - 0.10, dx - 0.36, yb - ht * 0.75, dx - 0.10, yb - ht + 0.03, k.c(col["light"])))
    if C.get("patch25"):
        px = fx
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (px - 0.09, yb - 0.22, px + 0.09, yb - 0.22, px + 0.08, yb - 0.10, px - 0.08, yb - 0.10, k.c(C["patch25"]), k.ink))
    # base band + side bosses
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
             % (dx - 0.46, yb - 0.005, fx, yb + 0.06, dx + 0.46, yb - 0.005, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
             % (dx - 0.46, yb - 0.005, fx, yb + 0.06, dx + 0.46, yb - 0.005, k.c("#3a342e")))
    for sx in (-1, 1):
        o.append(_circ((dx + sx * 0.47, yb - 0.03), 0.030, k.c(BRASS["base"]), k, 0.009))
    # spike through the cover
    yt = yb - ht
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (dx - 0.060, yt + 0.025, dx - 0.018, yt - 0.01, dx, yt - 0.17, dx + 0.018, yt - 0.01, dx + 0.060, yt + 0.025, k.c(BRASS["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.026" fill="%s" stroke="%s" stroke-width="0.012"/>' % (dx, yt + 0.018, k.c(BRASS["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (dx - 0.010, yt - 0.01, dx - 0.004, yt - 0.12, k.c(BRASS["light"])))
    h = _wrap(o, C, _POSE25["hat_up"])
    h = _strap_chin(k, dx, k.c("#1e1a20"), y0=-0.22, x0=0.50, x1=0.28) + h
    C4._ext_hat(k, C, ((dx - 0.58, yb + 0.08), (dx + 0.58, yb + 0.08), (dx, yt - 0.18), (fx, yb + 0.18)))
    return h, (dx, yt - 0.17 - _POSE25["hat_up"])


def _hat_peakcap25(k, C, yaw):
    """British staff officer's service cap: khaki crown flaring up to a wide, forward-sloping top, a broad scarlet band with two brass
    buttons and a small plain brass badge, a stiff dark peak with a gold edge line, a leather chin strap across the peak."""
    if _POSE25["hat_off"] > 0.5:
        return _bare(C)
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.12 * yaw
    tx = dx * 1.4 + 0.05
    yb0, yb1 = -0.47, -0.27
    ytop = -0.70
    cr = dict(light=col["crown_l"], base=col["crown"], dark=col["crown_d"])
    g = _gl(k, "pc", cr["light"], cr["base"], cr["dark"], -0.7, 0.7, 0.34)
    o = []
    side = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" % (dx - 0.46, yb0 + 0.02, tx - 0.68, ytop + 0.04, tx, ytop + 0.22, tx + 0.68, ytop + 0.04, dx + 0.46, yb0 + 0.02)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (side, g, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.68" ry="0.125" fill="%s" stroke="%s" stroke-width="0.026"/>' % (tx, ytop, g, k.ink))
    o.append('<path d="M%.4f,%.4f A0.60,0.09 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
             % (tx - 0.54, ytop - 0.005, tx + 0.15, ytop - 0.09, k.c(cr["light"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (tx, ytop + 0.12, fx, yb0, k.c(cr["dark"])))
    o.append(_circ((tx, ytop - 0.005), 0.022, k.c(BRASS["base"]), k, 0.008))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (dx - 0.47, yb0, fx, yb0 + 0.05, dx + 0.47, yb0, dx + 0.47, yb1, fx, yb1 + 0.05, dx - 0.47, yb1)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    for yy in (yb0 + 0.035, yb1 - 0.035):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>'
                 % (dx - 0.45, yy, fx, yy + 0.05, dx + 0.45, yy, k.c(col["band_d"])))
    by = (yb0 + yb1) / 2 + 0.03
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.058" fill="%s" stroke="%s" stroke-width="0.012"/>' % (fx, by, k.c(BRASS["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.026" ry="0.026" fill="%s"/>' % (fx, by, k.c(col["band"])))
    # peak (patent, dark brown-black) with a gold edge line, and a strap across it with two brass buttons
    vis = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
           % (fx - 0.44, yb1 - 0.01, fx, yb1 + 0.05, fx + 0.44, yb1 - 0.01, fx + 0.34, yb1 + 0.14, fx, yb1 + 0.165, fx - 0.34, yb1 + 0.14, fx - 0.44, yb1 - 0.01))
    gv = _gl(k, "pv", "#5a4a44", "#2a2024", "#1a1216", -0.4, 0.4, 0.3)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (vis, gv, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
             % (fx - 0.31, yb1 + 0.125, fx, yb1 + 0.150, fx + 0.31, yb1 + 0.125, k.c(BRASS["base"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.4"/>'
             % (fx - 0.26, yb1 + 0.07, fx - 0.10, yb1 + 0.10, fx + 0.06, yb1 + 0.10))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
             % (dx - 0.46, yb1 - 0.01, fx, yb1 + 0.075, dx + 0.46, yb1 - 0.01, k.c(LEATHER["base"])))
    for sx in (-1, 1):
        o.append(_circ((dx + sx * 0.46, yb1 - 0.01), 0.020, k.c(BRASS["base"]), k, 0.008))
    h = _wrap(o, C, _POSE25["hat_up"] + 0.05)
    C4._ext_hat(k, C, ((tx - 0.70, ytop - 0.05), (tx + 0.70, ytop - 0.05), (tx, ytop - 0.18), (fx - 0.44, yb1 + 0.10), (fx + 0.44, yb1 + 0.10)))
    return h, (tx, ytop - 0.175 - _POSE25["hat_up"])


def _hat_flatcap25(k, C, yaw):
    """workers' / engineer's flat cap in three cuts: C['cap_style'] 'baggy' (big soft dome overhanging the sides, short peak),
    'neat' (compact eight-panel cap with a stitched peak and a button), 'docker' (low and tight, long flat peak).  Tweed flecks."""
    if _POSE25["hat_off"] > 0.5:
        return _bare(C)
    col = C["hat_colors"]
    st = C.get("cap_style", "neat")
    dx = -0.03 * yaw
    vx = 0.26 * yaw
    P_ = dict(baggy=dict(xr=0.55, yb=-0.25, top=-0.62, vw=0.34, vd=0.17, puff=0.10),
              neat=dict(xr=0.47, yb=-0.27, top=-0.58, vw=0.33, vd=0.15, puff=0.05),
              docker=dict(xr=0.50, yb=-0.25, top=-0.50, vw=0.42, vd=0.12, puff=0.02))[st]
    xr, yb, top, vw, vd, pf = P_["xr"], P_["yb"], P_["top"], P_["vw"], P_["vd"], P_["puff"]
    o = []
    # peak
    vy0 = yb - 0.002
    vr = 'transform="rotate(%.3f %.4f %.4f)"' % (8.0 * yaw, vx, yb)
    o.append('<path %s d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (vr, vx - vw, vy0, vx, vy0 + 0.04, vx + vw, vy0, vx + vw * 0.8, yb + vd, vx - vw * 0.8, yb + vd, vx - vw, vy0, k.c(col["visor"]), k.ink))
    o.append('<path %s d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round" opacity="0.8"/>'
             % (vr, vx - vw * 0.55, yb + vd * 0.66, vx, yb + vd * 0.66 + 0.035, vx + vw * 0.55, yb + vd * 0.66, k.c(col["seam"])))
    g = _gl(k, "fc", col["light"], col["base"], col["dark"], -0.5, 0.5, 0.36)
    xl = dx - xr
    xr2 = dx + xr
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl, yb, xl - pf - 0.02, yb - 0.14, dx - 0.30, top, dx + 0.02, top, dx + 0.34, top - 0.02, xr2 + pf + 0.02, yb - 0.14, xr2, yb, vx * 0.5, yb + 0.05, xl, yb))
    k.defs.append('<clipPath id="%s_fd"><path d="%s"/></clipPath>' % (k.uid, dome))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>'
             % (xl + 0.04, yb + 0.012, vx * 0.5, yb + 0.07, xr2 - 0.04, yb + 0.012, k.c(col["band"])))
    o.append('<path d="%s" fill="%s"/>' % (dome, g))
    o.append('<g clip-path="url(#%s_fd)">' % k.uid)
    for i in range(14):
        a, b = _hash(C["seed"], i), _hash(C["seed"], i + 40)
        x, y = dx - xr + 2 * xr * a, top + (yb - top) * b
        o.append('<path d="M%.4f,%.4f l0.022,-0.010" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (x, y, k.c(col["check"])))
    for u in (-0.8, -0.4, 0.0, 0.4, 0.8):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.011" opacity="0.8"/>'
                 % (dx + 0.02, top + 0.02, dx + xr * 0.8 * u * 0.9, top + 0.12, dx + (xr + pf) * u, yb + 0.05, k.c(col["seam"])))
    o.append('</g>')
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (dome, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.034" ry="0.016" fill="%s" stroke="%s" stroke-width="0.012"/>' % (dx + 0.02, top + 0.006, k.c(col["light"]), k.ink))
    if C.get("pencil25"):
        pass
    h = _wrap(o, C, _POSE25["hat_up"])
    C4._ext_hat(k, C, ((xl - pf - 0.03, yb - 0.10), (xr2 + pf + 0.03, yb - 0.10), (dx, top - 0.01), (vx - vw, yb + vd), (vx + vw, yb + vd)))
    return h, (dx, top - _POSE25["hat_up"])


def _hat_flyhelm25(k, C, yaw):
    """RFC flying helmet: close-fitting brown leather cap with panel seams, ear flaps with a chin strap and buckle, goggles pushed up
    on the forehead (leather strap, brass-ringed lenses with a glint)."""
    if _POSE25["hat_off"] > 0.5:
        return _bare(C)
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.14 * yaw
    o = []
    g = _gl(k, "fh", col["light"], col["base"], col["dark"], -0.5, 0.5, 0.34)
    # simpler, robust outline: helmet bowl + two ear flaps
    bowl = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.47, -0.17, dx - 0.55, -0.42, dx - 0.30, -0.64, dx, -0.64, dx + 0.30, -0.64, dx + 0.55, -0.42, dx + 0.47, -0.17, fx, -0.30, dx - 0.47, -0.17))
    for sx in (-1, 1):
        fl = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f L%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
              % (dx + sx * 0.44, -0.30, dx + sx * 0.54, -0.10, dx + sx * 0.54, 0.16, dx + sx * 0.46, 0.24, dx + sx * 0.38, 0.22, dx + sx * 0.34, 0.16, dx + sx * 0.36, -0.02, dx + sx * 0.36, -0.20))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (fl, g, k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (bowl, g, k.ink))
    for u in (-0.6, 0.0, 0.6):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-dasharray="0.03 0.02" opacity="0.85"/>'
                 % (dx + u * 0.05, -0.62, dx + u * 0.34, -0.45, dx + u * 0.46 + 0.1 * yaw, -0.22, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.40, -0.30, dx - 0.36, -0.52, dx - 0.12, -0.60, k.c(col["light"])))
    # goggles on the forehead: strap, bridge, two lenses
    gy = -0.30
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (dx - 0.46, gy + 0.02, fx, gy + 0.08, dx + 0.46, gy + 0.02, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (dx - 0.46, gy + 0.02, fx, gy + 0.08, dx + 0.46, gy + 0.02, k.c("#3a2a22")))
    k.defs.append('<radialGradient id="%s_gl" cx="0.36" cy="0.32" r="0.8"><stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  % (k.uid, k.c("#c8e4f2"), k.c("#4a7aa8"), k.c("#1c3250")))
    for sx in (-1, 1):
        cx = fx + sx * 0.17
        o.append('<circle cx="%.4f" cy="%.4f" r="0.125" fill="%s" stroke="%s" stroke-width="0.024"/>' % (cx, gy + 0.03, k.c(BRASS["base"]), k.ink))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.092" fill="url(#%s_gl)" stroke="%s" stroke-width="0.012"/>' % (cx, gy + 0.03, k.uid, k.ink))
        o.append('<path d="M%.4f,%.4f A0.05,0.05 0 0 1 %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.85"/>'
                 % (cx - 0.055, gy + 0.005, cx - 0.01, gy - 0.04))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (fx - 0.05, gy + 0.03, fx, gy + 0.01, fx + 0.05, gy + 0.03, k.c(BRASS["dark"])))
    # chin strap with a brass buckle
    for sx in (-1, 1):
        o.append('<path d="M%.4f,0.24 Q%.4f,0.40 %.4f,0.50" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (dx + sx * 0.44, dx + sx * 0.42, dx + sx * 0.20, k.c(LEATHER["dark"])))
    o.append('<rect x="%.4f" y="0.332" width="0.05" height="0.05" fill="none" stroke="%s" stroke-width="0.014"/>' % (dx - 0.417, k.c(BRASS["base"])))
    h = _wrap(o, C, _POSE25["hat_up"])
    C4._ext_hat(k, C, ((dx - 0.58, -0.40), (dx + 0.58, -0.40), (dx, -0.66), (dx - 0.52, 0.26), (dx + 0.52, 0.26)))
    return h, (dx, -0.64 - _POSE25["hat_up"])


HATS25 = {"brodie25": _hat_brodie25, "pickel25": _hat_pickel25, "peakcap25": _hat_peakcap25, "flatcap25": _hat_flatcap25, "flyhelm25": _hat_flyhelm25}


# ============================================================================= costumes (torso-local)
def _band(k, X, y, hw, th, col, bow=0.04, edge=0.026):
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, y) + X(0.0, y + bow) + X(hw, y))
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/><path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>'
            % (d, k.ink, th + edge, d, col, th))


def _button(k, c, r=0.026):
    return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>'
            % (c[0], c[1], r, k.c(BRASS["base"]), k.ink, c[0] - r * 0.3, c[1] - r * 0.3, r * 0.3, k.c(BRASS["light"])))


def _flap(k, X, x, y, w, h, col, edge, btn=True):
    d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (X(x - w, y) + X(x + w, y) + X(x + w, y + h) + X(x - w, y + h))
    o = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)
    o += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (X(x - w, y + h * 0.35) + X(x + w, y + h * 0.35) + (k.c(edge),))
    if btn:
        o += _button(k, X(x, y + h * 0.70), 0.016)
    return o


def _cos_staff25(k, C, m):
    """the general's khaki service dress: open turn-down collar over a khaki shirt and brown tie, scarlet gorget tabs with brass
    buttons, rows of medal ribbons (plain colour bars) on the left breast, box-pleat patch pockets, a Sam Browne belt with its
    cross strap, brass buttons down the belly; a short flared skirt of the tunic over the breeches."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    fw = min(1.0, hw / 0.70)
    o = []
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (X(-0.20, 0.36) + X(0.20, 0.36) + X(0.0, 0.74) + (k.c(col["shirt"]), k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (X(-0.035, 0.42) + X(0.035, 0.42) + X(0.04, 0.66) + X(-0.04, 0.66) + (k.c(col["tie"]), k.ink)))
    for s in (-1, 1):
        lp = [X(s * 0.17, 0.35), X(s * 0.38, 0.39), X(s * 0.30, 0.50), X(s * 0.40, 0.56), X(s * 0.08, 0.78), X(s * 0.05, 0.60)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["lapel"]), k.ink))
        tab = [X(s * 0.30, 0.40), X(s * 0.41, 0.42), X(s * 0.36, 0.52), X(s * 0.25, 0.50)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(tab), k.c(col["tab"]), k.ink))
        o.append(_button(k, X(s * 0.335, 0.465), 0.016))
    o.append(_ln([X(0.05, 0.60), X(0.03, yB + 0.02)], k.ink, 0.014))
    for y in (0.84, 1.00, 1.16, 1.32):
        if y < yB - 0.24:
            o.append(_button(k, X(0.03, y)))
    # medal ribbons on the left breast (screen-right): three rows of plain colour bars
    rb = (("#c8302a", "#2a4a9a"), ("#f0c040", "#2a7a4a"), ("#6a2a8a", "#e8e0d0"), ("#2a4a9a", "#c8302a"),
          ("#2a7a4a", "#f0c040"), ("#c8302a", "#e8e0d0"), ("#e8e0d0", "#6a2a8a"), ("#2a4a9a", "#f0c040"),
          ("#f0c040", "#c8302a"), ("#6a2a8a", "#2a7a4a"), ("#2a7a4a", "#2a4a9a"), ("#c8302a", "#f0c040"))
    for i, (c1, c2) in enumerate(rb):
        r, cidx = divmod(i, 4)
        x0, y0 = X(0.14 * fw + cidx * 0.078, 0.58 + r * 0.050)
        o.append('<rect x="%.4f" y="%.4f" width="0.074" height="0.046" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x0, y0, k.c(c1), k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.026" height="0.046" fill="%s"/>' % (x0 + 0.024, y0, k.c(c2)))
    # patch pockets with box pleats
    px = 0.42 * fw
    o.append(_flap(k, X, -px, 0.78, 0.13, 0.085, col["base"], col["dark"]))
    o.append(_flap(k, X, px - 0.02, 0.85, 0.13, 0.085, col["base"], col["dark"]))
    for sx in (-1, 1):
        o.append(_flap(k, X, sx * 0.50 * fw, yB - 0.44, 0.14, 0.09, col["base"], col["dark"]))
    # Sam Browne cross strap (over the right shoulder, screen-left, down to the belt)
    st = [X(-0.30, 0.37), X(0.20, yB - 0.30)]
    o.append(_ln(st, k.ink, 0.092))
    o.append(_ln(st, k.c(LEATHER["base"]), 0.066))
    o.append(_ln([(st[0][0] + 0.018, st[0][1] + 0.01), (st[1][0] + 0.018, st[1][1] - 0.01)], k.c(LEATHER["light"]), 0.012, ' opacity="0.7"'))
    o.append(_ln([X(-0.34, 0.37), X(-0.26, 0.37)], k.c(BRASS["base"]), 0.018))
    inside = "".join(o)
    yt = yB - 0.20
    hem = yB + C.get("coat_len", 0.20)
    a = hw * 0.985
    b = hw + C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "sg", X, yt, a, hem, b, g, sw=0.026, folds=((-0.20, yt + 0.10, -0.26, hem - 0.03), (0.28, yt + 0.10, 0.34, hem - 0.03)), fold_col=k.c(col["dark"]))]
    yw = yB - 0.22
    ov.append(_band(k, X, yw, hw, 0.095, k.c(LEATHER["base"]), 0.05))
    bx, by = X(0.0, yw + 0.05)
    ov.append('<rect x="%.4f" y="%.4f" width="0.15" height="0.115" rx="0.02" fill="%s" stroke="%s" stroke-width="0.014"/><rect x="%.4f" y="%.4f" width="0.09" height="0.06" fill="%s" stroke="%s" stroke-width="0.010"/>'
              % (bx - 0.075, by - 0.057, k.c(BRASS["base"]), k.ink, bx - 0.045, by - 0.03, k.c(LEATHER["base"]), k.ink))
    rx, ry = X(0.22, yw + 0.03)
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.032" fill="none" stroke="%s" stroke-width="0.016"/>' % (rx, ry, k.c(BRASS["base"])))
    return inside, "", "".join(ov)


def _cos_tunic25(k, C, m):
    """British infantry 1916: khaki tunic with a stand collar, five brass buttons, four patch pockets with flaps, shoulder straps;
    1908 pattern webbing in pale buff: braces to a belt, two ammunition pouches either side; C['kit25'] a tuple of extras:
    'bottle' (blue-enamel water bottle at the hip), 'scarf' (knotted wool muffler), 'pack' (haversack on the hip), 'tool' (entrenching tool)."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    fw = min(1.0, hw / 0.70)
    kit = C.get("kit25", ())
    web, webd = k.c(col["web"]), k.c(col["web_d"])
    o = []
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (X(-0.20, 0.33) + X(0.0, 0.40) + X(0.20, 0.33) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (X(-0.20, 0.33) + X(0.0, 0.40) + X(0.20, 0.33) + (k.c(col["dark"]),)))
    o.append(_ln([X(0.0, 0.44), X(0.0, yB)], k.ink, 0.012, ' opacity="0.7"'))
    for y in (0.58, 0.76, 0.94, 1.12):
        if y < yB - 0.30:
            o.append(_button(k, X(0.0, y), 0.022))
    for s in (-1, 1):
        o.append(_flap(k, X, s * 0.40 * fw, 0.64, 0.12, 0.085, col["base"], col["dark"]))
        o.append(_flap(k, X, s * 0.46 * fw, yB - 0.52, 0.13, 0.095, col["base"], col["dark"]))
        o.append(_ln([X(s * 0.18, 0.37), X(s * 0.42 * fw, 0.40)], k.ink, 0.058))
        o.append(_ln([X(s * 0.18, 0.37), X(s * 0.42 * fw, 0.40)], k.c(col["dark"]), 0.034))
    for s in (-1, 1):
        st = [X(s * 0.26, 0.34), X(s * 0.24, 0.80), X(s * 0.27 * fw, yB - 0.26)]
        o.append(_ln(st, k.ink, 0.100))
        o.append(_ln(st, web, 0.074))
        o.append(_ln([(st[0][0] - s * 0.020, st[0][1] + 0.05), (st[1][0] - s * 0.020, st[1][1]), (st[2][0] - s * 0.020, st[2][1] - 0.03)], webd, 0.010, ' opacity="0.7"'))
        for j in (0, 1):
            cx = s * (0.18 + 0.19 * j) * fw
            d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (X(cx - 0.075, yB - 0.46) + X(cx + 0.075, yB - 0.46) + X(cx + 0.075, yB - 0.22) + X(cx - 0.075, yB - 0.22))
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (d, webd, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (X(cx - 0.075, yB - 0.38) + X(cx + 0.075, yB - 0.38) + (k.ink,)))
            o.append(_circ(X(cx, yB - 0.31), 0.014, k.c(BRASS["base"]), k, 0.006))
    inside = "".join(o)
    ov = []
    yt = yB - 0.16
    hem = yB + C.get("coat_len", 0.10)
    a = hw * 0.985
    b = hw + C.get("coat_flare", 0.05)
    g = "url(#%s_tg)" % k.uid
    ov.append(C2._skirt(k, "tn", X, yt, a, hem, b, g, sw=0.024, folds=((-0.16, yt + 0.04, -0.20, hem - 0.02), (0.20, yt + 0.04, 0.24, hem - 0.02)), fold_col=k.c(col["dark"])))
    ov.append(_band(k, X, yB - 0.19, hw, 0.095, web, 0.04))
    bx, by = X(0.0, yB - 0.15)
    ov.append('<rect x="%.4f" y="%.4f" width="0.10" height="0.075" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx - 0.05, by - 0.037, k.c(BRASS["base"]), k.ink))
    if "bottle" in kit:
        cx, cy = X(-hw * 0.92, yB - 0.10)
        ov.append('<path d="M%.4f,%.4f q-0.02,-0.14 0.07,-0.20 q0.10,0.04 0.09,0.20 q-0.07,0.06 -0.16,0 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (cx - 0.02, cy + 0.04, k.c("#3a5a7a"), k.ink))
        ov.append('<path d="M%.4f,%.4f l0,-0.04" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (cx + 0.05, cy - 0.15, k.ink))
        ov.append('<path d="M%.4f,%.4f l0,-0.04" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (cx + 0.05, cy - 0.15, k.c("#c8a070")))
    if "pack" in kit:
        cx, cy = X(hw * 0.96, yB - 0.08)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (cx - 0.14, cy - 0.20, cx + 0.07, cy - 0.20, cx + 0.07, cy + 0.07, cx - 0.14, cy + 0.07, webd, k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (cx - 0.14, cy - 0.10, cx + 0.07, cy - 0.10, k.ink))
        ov.append(_circ((cx - 0.035, cy - 0.10), 0.014, k.c(BRASS["base"]), k, 0.006))
    if "tool" in kit:
        cx, cy = X(hw * 0.90, yB - 0.05)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.060" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>'
                  % (cx, cy - 0.26, cx + 0.02, cy + 0.08, k.ink, cx, cy - 0.26, cx + 0.02, cy + 0.08, k.c(WOOD["base"])))
    if "scarf" in kit:
        sc = k.c(col["scarf"])
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.28, 0.32) + X(0.0, 0.54) + X(0.28, 0.32))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.158" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.124" stroke-linecap="round"/>' % (d, k.ink, d, sc))
        for xx in (-0.15, -0.05, 0.06, 0.16):
            ov.append('<path d="M%.4f,%.4f l0.02,0.07" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (X(xx, 0.42)[0], 0.42 + 0.06 * (1 - abs(xx) * 3), k.c(col["scarf_d"])))
        kx, ky = X(0.10, 0.62)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (kx - 0.05, ky - 0.10, kx + 0.07, ky - 0.08, kx + 0.12, ky + 0.20, kx - 0.02, ky + 0.22, sc, k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (kx - 0.01, ky + 0.0, kx + 0.05, ky + 0.19, k.c(col["scarf_d"])))
    return inside, "", "".join(ov)


def _cos_waist25(k, C, m):
    """the engineer: a dark teal waistcoat over a collarless cream shirt (brass stud at the neck, sleeves rolled to the elbow), brass
    buttons, welt pockets, a brass watch chain looped across to a pocket; dark trousers."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    fw = min(1.0, hw / 0.70)
    o = [CE._bowl(k, col["pants"], yB - 0.09, yB, dip=0.02)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (X(-0.19, 0.34) + X(0.19, 0.34) + X(0.0, 0.86) + (k.c(col["shirt"]), k.ink)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (X(-0.17, 0.35) + X(0.0, 0.42) + X(0.17, 0.35) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (X(-0.17, 0.35) + X(0.0, 0.42) + X(0.17, 0.35) + (k.c(col["shirt"]),)))
    o.append(_circ(X(0.0, 0.43), 0.014, k.c(BRASS["base"]), k, 0.006))
    for s in (-1, 1):
        lp = [X(s * 0.19, 0.34), X(s * 0.40, 0.38), X(s * 0.36, 0.60), X(s * 0.14, 0.86), X(s * 0.04, 0.86)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["base"]), k.ink))
        o.append(_ln([X(s * 0.30, 0.50), X(s * 0.12, 0.82)], k.c(col["dark"]), 0.010, ' opacity="0.8"'))
    o.append(_ln([X(0.04, 0.86), X(0.02, yB + 0.02)], k.ink, 0.014))
    for y in (0.90, 1.04, 1.18):
        if y < yB - 0.08:
            o.append(_button(k, X(0.0, y), 0.020))
    for s in (-1, 1):
        x0, y0 = s * 0.30 * fw, yB - 0.30
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (X(x0 - 0.09, y0 + 0.02) + X(x0 + 0.09, y0 - 0.02) + (k.ink,)))
    cx0, cy0 = X(0.0, 0.98)
    cx1, cy1 = X(-0.30 * fw, yB - 0.30)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (cx0, cy0, (cx0 + cx1) / 2, cy1 + 0.16, cx1, cy1, k.c(BRASS["base"])))
    o.append(_circ((cx1, cy1), 0.020, k.c(BRASS["base"]), k, 0.008))
    return "".join(o), "", ""


def _cos_work25(k, C, m):
    """Lincoln factory clothes, C['work_style']:  'bib' denim bib overalls with a rag in the pocket over a rust shirt;
    'apron' a long leather apron over a grey collarless shirt with braces;  'boiler' a one-piece olive boiler suit with a big
    chest pocket, brass buttons and a rope belt."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    fw = min(1.0, hw / 0.70)
    st = C.get("work_style", "bib")
    o = []
    if st == "bib":
        o.append(CE._bowl(k, col["denim"], yB - 0.40, yB, dip=0.03))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (X(-0.28, 0.66) + X(0.28, 0.66) + X(0.30 * fw, yB - 0.38) + X(-0.30 * fw, yB - 0.38) + (k.c(col["denim"]), k.ink)))
        for s in (-1, 1):
            sp = [X(s * 0.27, 0.66), X(s * 0.24, 0.40), X(s * 0.20, 0.34)]
            o.append(_ln(sp, k.ink, 0.074))
            o.append(_ln(sp, k.c(col["denim"]), 0.048))
            o.append(_circ(X(s * 0.27, 0.665), 0.024, k.c(BRASS["base"]), k, 0.008))
        o.append('<rect x="%.4f" y="%.4f" width="0.20" height="0.13" fill="%s" stroke="%s" stroke-width="0.012"/>' % (X(-0.10, 0.74)[0], 0.74, k.c(col["denim_d"]), k.ink))
        o.append('<path d="M%.4f,0.74 L%.4f,0.80" stroke="%s" stroke-width="0.008" stroke-dasharray="0.02 0.015" opacity="0.8"/>' % (X(0.0, 0.74)[0], X(0.0, 0.80)[0], k.c(col["stitch"])))
        rx = X(0.12, 0.74)[0]
        o.append('<path d="M%.4f,0.75 q0.04,-0.12 0.10,-0.04 q0.02,0.03 -0.02,0.05 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (rx, k.c("#c8402a"), k.ink))
        o.append(_ln([X(-0.28, 0.66), X(0.28, 0.66)], k.c(col["stitch"]), 0.008, ' stroke-dasharray="0.02 0.014"'))
    elif st == "apron":
        o.append(CE._bowl(k, col["pants"], yB - 0.10, yB, dip=0.02))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (X(-0.19, 0.34) + X(0.19, 0.34) + X(0.0, 0.66) + (k.c(col["collar"]), k.ink)))
        for s in (-1, 1):
            sp = [X(s * 0.24, 0.60), X(s * 0.26, 0.36), X(s * 0.12, 0.33)]
            o.append(_ln(sp, k.ink, 0.070))
            o.append(_ln(sp, k.c(col["strap"]), 0.044))
        ap = [X(-0.30 * fw, 0.62), X(0.30 * fw, 0.62), X(0.52 * fw, yB + 0.1), X(-0.52 * fw, yB + 0.1)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (_poly_d(ap), k.c(col["denim"]), k.ink))
        o.append(_ln([X(-0.26 * fw, 0.66), X(-0.46 * fw, yB + 0.06)], k.c(col["stitch"]), 0.008, ' stroke-dasharray="0.02 0.014"'))
        o.append(_ln([X(0.26 * fw, 0.66), X(0.46 * fw, yB + 0.06)], k.c(col["stitch"]), 0.008, ' stroke-dasharray="0.02 0.014"'))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(-0.17, 0.98) + X(0.17, 0.98) + X(0.15, 1.18) + X(-0.15, 1.18) + (k.c(col["denim_d"]), k.ink)))
        o.append(_circ(X(-0.30 * fw, 0.62), 0.018, k.c(BRASS["base"]), k, 0.008))
        o.append(_circ(X(0.30 * fw, 0.62), 0.018, k.c(BRASS["base"]), k, 0.008))
    else:
        o.append(_ln([X(0.0, 0.44), X(0.0, yB)], k.ink, 0.014))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (X(-0.20, 0.33) + X(0.0, 0.40) + X(0.20, 0.33) + (k.ink,)))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>' % (X(-0.20, 0.33) + X(0.0, 0.40) + X(0.20, 0.33) + (k.c(col["dark"]),)))
        for y in (0.56, 0.74, 0.92, 1.10):
            if y < yB - 0.2:
                o.append(_button(k, X(0.0, y), 0.020))
        o.append(_flap(k, X, -0.32 * fw, 0.62, 0.16, 0.16, col["denim"], col["dark"], False))
        for sx in (-1, 1):
            o.append(_flap(k, X, sx * 0.40 * fw, yB - 0.46, 0.14, 0.15, col["denim"], col["dark"], False))
        o.append('<path d="M%.4f,0.60 L%.4f,0.74" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M%.4f,0.60 L%.4f,0.74" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                 % (X(-0.28 * fw, 0.60)[0], X(-0.30 * fw, 0.74)[0], k.ink, X(-0.28 * fw, 0.60)[0], X(-0.30 * fw, 0.74)[0], k.c(STEEL["base"])))
        yw = yB - 0.16
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.070"/><path d="%s" fill="none" stroke="%s" stroke-width="0.044"/>' % (d, k.ink, d, k.c("#d2b98a")))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-dasharray="0.03 0.03"/>' % (d, k.c("#8e7650")))
        kx, ky = X(0.14, yw + 0.04)
        o.append('<path d="M%.4f,%.4f q0.01,0.12 -0.03,0.22 M%.4f,%.4f q0.04,0.10 0.06,0.18" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.ink))
        o.append('<path d="M%.4f,%.4f q0.01,0.12 -0.03,0.22 M%.4f,%.4f q0.04,0.10 0.06,0.18" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.c("#d2b98a")))
        o.append(_circ((kx, ky), 0.026, k.c("#d2b98a"), k, 0.008))
    return "".join(o), "", ""


def _cos_feld25(k, C, m):
    """German infantry 1916 (M1915 feldgrau tunic): a plain turn-down collar with red piping, a placket with hidden buttons, shoulder
    straps with red piping, a black leather belt with a round brass plate, two brown ammunition pouches either side, Y-straps;
    C['kit25']: 'bread' (haversack at the hip), 'roll' (greatcoat roll over one shoulder), 'flask'."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    fw = min(1.0, hw / 0.70)
    kit = C.get("kit25", ())
    o = []
    pip = k.c(col["pipe"])
    for s in (-1, 1):
        cl = [X(s * 0.20, 0.34), X(s * 0.38, 0.38), X(s * 0.24, 0.56), X(s * 0.03, 0.46)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(cl), k.c(col["collar"]), k.ink))
        o.append(_ln([X(s * 0.20, 0.35), X(s * 0.37, 0.39), X(s * 0.24, 0.55)], pip, 0.010))
        sp = [X(s * 0.18, 0.36), X(s * 0.42 * fw, 0.40)]
        o.append(_ln(sp, k.ink, 0.062))
        o.append(_ln(sp, k.c(col["dark"]), 0.038))
        o.append(_ln(sp, pip, 0.010))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012"/>' % (X(0.0, 0.46) + X(0.0, yB) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" opacity="0.5"/>' % (X(0.02, 0.50) + X(0.02, yB - 0.2) + (k.c(col["dark"]),)))
    for y in (0.62, 0.82, 1.02):
        if y < yB - 0.3:
            o.append(_circ(X(0.0, y), 0.015, k.c(col["dark"]), k, 0.006))
    for s in (-1, 1):
        o.append(_flap(k, X, s * 0.44 * fw, yB - 0.54, 0.12, 0.09, col["base"], col["dark"], False))
        st = [X(s * 0.24, 0.34), X(s * 0.22, 0.74), X(s * 0.16 * fw, yB - 0.24)]
        o.append(_ln(st, k.ink, 0.062))
        o.append(_ln(st, k.c("#2a2024"), 0.040))
        for j in (0, 1):
            cx = s * (0.17 + 0.18 * j) * fw
            d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (X(cx - 0.070, yB - 0.44) + X(cx + 0.070, yB - 0.44) + X(cx + 0.070, yB - 0.22) + X(cx - 0.070, yB - 0.22))
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (d, k.c(LEATHER["base"]), k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008"/>' % (X(cx - 0.070, yB - 0.37) + X(cx + 0.070, yB - 0.37) + (k.ink,)))
            o.append(_circ(X(cx, yB - 0.30), 0.012, k.c(BRASS["base"]), k, 0.005))
    if "roll" in kit:
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.34, 0.34) + X(-0.46 * fw, 0.90) + X(0.34, yB - 0.30))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.150"/><path d="%s" fill="none" stroke="%s" stroke-width="0.118"/>' % (d, k.ink, d, k.c(col["roll"])))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-dasharray="0.03 0.07" opacity="0.8"/>' % (d, k.c(col["dark"])))
    inside = "".join(o)
    ov = []
    yt = yB - 0.16
    hem = yB + C.get("coat_len", 0.14)
    a = hw * 0.985
    b = hw + C.get("coat_flare", 0.06)
    g = "url(#%s_tg)" % k.uid
    ov.append(C2._skirt(k, "fd", X, yt, a, hem, b, g, sw=0.024, folds=((-0.18, yt + 0.04, -0.22, hem - 0.02), (0.20, yt + 0.04, 0.24, hem - 0.02)), fold_col=k.c(col["dark"])))
    ov.append(_band(k, X, yB - 0.20, hw, 0.085, k.c("#2a2024"), 0.04))
    bx, by = X(0.0, yB - 0.16)
    ov.append(_circ((bx, by), 0.060, k.c(BRASS["base"]), k, 0.014))
    ov.append(_circ((bx, by), 0.030, k.c(BRASS["dark"]), k, 0.008))
    if "bread" in kit:
        cx, cy = X(hw * 0.94, yB - 0.12)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (cx - 0.15, cy - 0.20, cx + 0.07, cy - 0.20, cx + 0.07, cy + 0.07, cx - 0.15, cy + 0.07, k.c("#9a8a5a"), k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010"/>' % (cx - 0.15, cy - 0.12, cx + 0.07, cy - 0.12, k.ink))
    if "flask" in kit:
        cx, cy = X(-hw * 0.94, yB - 0.08)
        ov.append('<path d="M%.4f,%.4f q-0.02,-0.14 0.07,-0.20 q0.10,0.04 0.09,0.20 q-0.07,0.06 -0.16,0 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (cx - 0.02, cy + 0.04, k.c("#6a6a4a"), k.ink))
    return inside, "", "".join(ov)


def _cos_coat25(k, C, m):
    """RFC pilot: a brown leather flying coat, double-breasted with a big turned-up fur collar (cream), a belt, a long cream silk scarf
    knotted at the neck with two ends streaming."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    hw = m.hwa
    o = []
    o.append(_ln([X(0.10, 0.60), X(0.12, yB + 0.02)], k.ink, 0.014))
    for y in (0.80, 0.98, 1.16):
        for s in (-1, 1):
            if y < yB - 0.2:
                o.append(_circ(X(s * 0.24 + 0.06, y), 0.026, k.c("#3a2418"), k, 0.010))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.030" stroke-linecap="round" opacity="0.18"/>' % (X(-0.40, 0.62) + X(-0.46, 0.90) + X(-0.38, yB - 0.10)))
    inside = "".join(o)
    ov = []
    yt = yB - 0.12
    hem = yB + C.get("coat_len", 0.46)
    a = hw * 0.985
    b = hw + C.get("coat_flare", 0.12)
    g = "url(#%s_tg)" % k.uid
    ov.append(C2._skirt(k, "pl", X, yt, a, hem, b, g, sw=0.026, folds=((-0.12, yt + 0.12, -0.18, hem - 0.04), (0.32, yt + 0.12, 0.38, hem - 0.04)), fold_col=k.c(col["dark"])))
    ov.append(_band(k, X, yB - 0.22, hw, 0.078, k.c(LEATHER["dark"]), 0.04))
    bx, by = X(0.06, yB - 0.18)
    ov.append('<rect x="%.4f" y="%.4f" width="0.09" height="0.07" rx="0.012" fill="none" stroke="%s" stroke-width="0.030"/><rect x="%.4f" y="%.4f" width="0.09" height="0.07" rx="0.012" fill="none" stroke="%s" stroke-width="0.016"/>'
              % (bx - 0.045, by - 0.035, k.ink, bx - 0.045, by - 0.035, k.c(BRASS["base"])))
    fur = k.c(col["fur"])
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.30, 0.31) + X(0.0, 0.54) + X(0.30, 0.31))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.186" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.152" stroke-linecap="round"/>' % (d, k.ink, d, fur))
    for i in range(7):
        t = i / 6.0
        px, py = X(-0.28 + 0.56 * t, 0.31 + 0.23 * math.sin(math.pi * t))
        ov.append('<path d="M%.4f,%.4f q%.4f,0.05 %.4f,0.09" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % (px, py - 0.02, 0.01 * (t - 0.5), 0.02 * (t - 0.5), k.c(col["fur_d"])))
    sc = k.c(col["scarf"])
    kx, ky = X(0.04, 0.62)
    for (ex, ey, wv) in ((kx - 0.16, ky + 0.62, 0.05), (kx + 0.16, ky + 0.46, -0.06)):
        d = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (kx, ky, kx + wv * 3, ky + 0.2, ex - wv * 2, ey - 0.2, ex, ey)
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.130" stroke-linecap="butt"/><path d="%s" fill="none" stroke="%s" stroke-width="0.100" stroke-linecap="butt"/>' % (d, k.ink, d, sc))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (ex - 0.04, ey - 0.02, ex + 0.04, ey - 0.02, k.c(col["scarf_d"])))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.058" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, sc, k.ink))
    return inside, "", "".join(ov)


COSTUMES25 = {"staff25": _cos_staff25, "tunic25": _cos_tunic25, "waist25": _cos_waist25, "work25": _cos_work25, "feld25": _cos_feld25, "coat25": _cos_coat25}


# ============================================================================= face: moustaches, big beard
def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    st = C.get("moustache_style") if C else None
    if st not in ("walrus25", "kaiser25", "kitchener25", "brush25"):
        return _O25["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#3a2a20")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    o = []
    if st == "walrus25":
        pts = [Q(0.0, -0.060), Q(-0.12, -0.085), Q(-0.24, -0.050), Q(-0.33, 0.030), Q(-0.36, 0.150), Q(-0.31, 0.215), Q(-0.25, 0.130), Q(-0.18, 0.115),
               Q(-0.10, 0.130), Q(-0.05, 0.085), Q(0.0, 0.100), Q(0.05, 0.085), Q(0.10, 0.130), Q(0.18, 0.115), Q(0.25, 0.130), Q(0.31, 0.215),
               Q(0.36, 0.150), Q(0.33, 0.030), Q(0.24, -0.050), Q(0.12, -0.085)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        st_ = "".join("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (Q(x * 0.8, -0.04) + Q(x * 1.05, 0.04) + Q(x * 1.15, 0.13 + abs(x) * 0.4)) for x in (-0.28, -0.21, -0.14, -0.07, 0.07, 0.14, 0.21, 0.28))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % (st_, k.c(C["colors"].get("moustache_l", "#b4abb7"))))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (Q(0.0, -0.056) + Q(0.0, 0.02) + (k.ink,)))
        k.ext.append(Q(-0.36, 0.215) + (0.03,))
        k.ext.append(Q(0.36, 0.215) + (0.03,))
    elif st == "kaiser25":
        pts = [Q(0.0, -0.048), Q(-0.10, -0.066), Q(-0.20, -0.070), Q(-0.29, -0.100), Q(-0.36, -0.170), Q(-0.39, -0.250), Q(-0.37, -0.255), Q(-0.32, -0.150),
               Q(-0.25, -0.080), Q(-0.18, -0.020), Q(-0.09, -0.010), Q(0.0, 0.004), Q(0.09, -0.010), Q(0.18, -0.020), Q(0.25, -0.080), Q(0.32, -0.150),
               Q(0.37, -0.255), Q(0.39, -0.250), Q(0.36, -0.170), Q(0.29, -0.100), Q(0.20, -0.070), Q(0.10, -0.066)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (Q(0.0, -0.036) + Q(0.0, 0.020) + (k.ink,)))
        k.ext.append(Q(-0.39, -0.25) + (0.03,))
        k.ext.append(Q(0.39, -0.25) + (0.03,))
    elif st == "kitchener25":
        pts = [Q(0.0, -0.060), Q(-0.12, -0.082), Q(-0.25, -0.060), Q(-0.34, 0.000), Q(-0.37, 0.085), Q(-0.33, 0.120), Q(-0.27, 0.060), Q(-0.18, 0.070),
               Q(-0.08, 0.085), Q(0.0, 0.050), Q(0.08, 0.085), Q(0.18, 0.070), Q(0.27, 0.060), Q(0.33, 0.120), Q(0.37, 0.085), Q(0.34, 0.000), Q(0.25, -0.060), Q(0.12, -0.082)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.017" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        st_ = "".join("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (Q(x * 0.8, -0.03) + Q(x * 1.05, 0.03) + Q(x * 1.1, 0.075)) for x in (-0.26, -0.18, -0.10, 0.10, 0.18, 0.26))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round" opacity="0.8"/>' % (st_, k.c(C["colors"].get("moustache_l", "#7a5a3a"))))
        k.ext.append(Q(-0.37, 0.12) + (0.03,))
        k.ext.append(Q(0.37, 0.12) + (0.03,))
    else:
        pts = [Q(-0.13, -0.050), Q(0.0, -0.062), Q(0.13, -0.050), Q(0.14, 0.030), Q(0.0, 0.040), Q(-0.14, 0.030)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.015" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
    return "".join(o)


def _bigbeard25(k, C, P_, L):
    B = C["bigbeard25"]
    mx, my = L["mx"], L["my"]
    col = k.c(B["color"])
    # explicit smooth outline: cheeks, chin, cheeks, then the upper edge above the moustache
    pts = [(mx - 0.50, -0.06), (mx - 0.55, 0.16), (mx - 0.50, 0.40), (mx - 0.34, 0.62), (mx - 0.14, 0.80), (mx, 0.86), (mx + 0.14, 0.80), (mx + 0.34, 0.62),
           (mx + 0.50, 0.40), (mx + 0.55, 0.16), (mx + 0.50, -0.06), (mx + 0.36, my - 0.12), (mx + 0.22, my - 0.07), (mx, my - 0.10), (mx - 0.22, my - 0.07), (mx - 0.36, my - 0.12)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, col, k.ink)]
    hs = []
    for i in range(9):
        x = -0.40 + 0.10 * i
        hs.append("M%.4f,%.4f q%.4f,0.07 %.4f,0.14" % (mx + x, my + 0.14 + 0.16 * (1 - abs(x) * 1.2), 0.02 * x, 0.04 * x))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % ("".join(hs), k.c(B.get("dark", "#2a1a10"))))
    o.append('<path d="M%.4f,0.10 Q%.4f,0.40 %.4f,0.70" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.45"/>' % (mx - 0.42, mx - 0.38, mx - 0.18, k.c(B.get("light", "#8a6a4a"))))
    k.ext.append((mx, 0.88, 0.03))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O25["_face"](k, C, P_, white)
    if C is None or not C.get("_cast25"):
        return svg, L
    under = []
    if C.get("bigbeard25"):
        under.append(_bigbeard25(k, C, P_, L))
    if not under:
        return svg, L
    return "".join(under) + svg, L


# ============================================================================= legs: puttees
def _puttee(k, S, E, H, kk, w, col, dark):
    pts = C3._limb_pts(S, E, H, kk)
    n = len(pts)
    cum = [0.0]
    for i in range(1, n):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1]
    if tot < 1e-6:
        return ""
    # the lower leg = the second half of the path (knee to ankle); wrap the part from the ankle up to 60 percent of it
    half = tot * 0.5
    L0 = tot - 0.07 * 1.0
    L1 = half - 0.02
    sel = []
    for i in range(n):
        if L1 <= cum[i] <= L0:
            sel.append(pts[i])
    if len(sel) < 2:
        return ""
    ww = 0.100 + 0.2 * (w - 0.15)
    d = "M" + " L".join("%.4f,%.4f" % p for p in sel)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.ink, ww + 0.030)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.c(col), ww))
    # diagonal wraps every 0.058 along the path
    tl = cum[n - 1]
    pos = L1 + 0.03
    while pos < L0 - 0.01:
        j = max(1, next(i for i in range(n) if cum[i] >= pos))
        a, b = pts[j - 1], pts[j]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        tx, ty = tx / ln, ty / ln
        nx, ny = -ty, tx
        h = ww / 2
        cx, cy = b
        sl = 0.45
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.85"/>'
                 % (cx - nx * h - tx * sl * h, cy - ny * h - ty * sl * h, cx + nx * h + tx * sl * h, cy + ny * h + ty * sl * h, k.c(dark)))
        pos += 0.058
    # tape tie at the top
    j = next(i for i in range(n) if cum[i] >= L1)
    a, b = pts[max(0, j - 1)], pts[j]
    tx, ty = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(tx, ty) or 1.0
    nx, ny = -ty / ln, tx / ln
    h = ww / 2 + 0.008
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (b[0] - nx * h, b[1] - ny * h, b[0] + nx * h, b[1] + ny * h, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (b[0] - nx * h, b[1] - ny * h, b[0] + nx * h, b[1] + ny * h, k.c(dark)))
    k.ext.append((sel[0][0], sel[0][1], ww / 2 + 0.02))
    k.ext.append((sel[-1][0], sel[-1][1], ww / 2 + 0.02))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O25["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast25"):
        return out
    if tail is not None and C.get("puttee25"):
        cw = C["shorts"].get("w", 0.15) if C.get("shorts") else w
        out += _puttee(k, S, E, H, kk, cw, C["puttee25"], P._shade(C["puttee25"], 0.55))
    return out


# ============================================================================= props
def _wood_grad(k, name, y0=-0.04, y1=0.04):
    return _lin(k, name, WOOD["light"], WOOD["base"], WOOD["dark"], 0, y0, 0, y1)


def _helmet_side(k, cx, cy, up_deg, sc, col, cover=False):
    """a Brodie seen from the side, dome pointing along the direction up_deg (screen angle); brim a thin ellipse."""
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (cx, cy, up_deg + 90.0, sc)]
    g = _gl(k, "hs%d" % int(abs(cx * 1000 + cy * 1000)), col["light"], col["base"], col["dark"], -0.6, 0.6, 0.30)
    o.append('<path d="M-0.40,0 C-0.42,-0.20 -0.22,-0.34 0,-0.34 C0.22,-0.34 0.42,-0.20 0.40,0 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<ellipse cx="0" cy="0.005" rx="0.62" ry="0.075" fill="%s" stroke="%s" stroke-width="0.024"/>' % (g, k.ink))
    o.append('<path d="M-0.30,-0.07 Q-0.24,-0.24 -0.04,-0.29" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.7"/>' % k.c(col["light"]))
    o.append(_circ((0.02, -0.30), 0.016, k.c(col["dark"]), k, 0.007))
    o.append('</g>')
    return "".join(o)


CAN_ROSE = (0.66, 0.05)         # the rose of the watering can, can frame (hand at the origin, spout to +x), before the pour tilt
CAN_TILT = 64.0                 # degrees of tilt at pour25 = 1
BOARD_TANK = (-0.80, 0.10)      # the chalk tank on the board (board frame: hand at the origin, board to -x)


def _can_body(k):
    """galvanised watering can (upright, spout to +x): cylinder body, arched top handle gripped at the origin, rear loop handle, long
    spout rising to a round rose with holes.  No letters."""
    o = []
    g = _lin(k, "wc", GALV["light"], GALV["base"], GALV["dark"], -0.23, 0, 0.23, 0)
    # rear loop handle (behind the body)
    o.append('<path d="M-0.20,0.22 Q-0.46,0.20 -0.44,0.36 Q-0.42,0.50 -0.20,0.46" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.20,0.22 Q-0.46,0.20 -0.44,0.36 Q-0.42,0.50 -0.20,0.46" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.c(GALV["base"]))
    # spout: a tapered tube from the low front of the body up to the rose
    sp = "M0.17,0.36 L0.58,0.02 L0.68,0.10 L0.20,0.52 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (sp, _lin(k, "ws", GALV["light"], GALV["base"], GALV["dark"], 0.3, -0.1, 0.5, 0.5), k.ink))
    o.append('<path d="M0.24,0.38 L0.58,0.08" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.75"/>')
    o.append('<path d="M0.30,0.455 L0.40,0.37" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(GALV["dark"]))
    # body
    o.append('<path d="M-0.225,0.17 L0.225,0.17 L0.205,0.55 Q0,0.58 -0.205,0.55 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink))
    for y in (0.30, 0.43):
        o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.75"/>' % (-0.222 + (y - 0.17) * 0.05, y, y + 0.03, 0.222 - (y - 0.17) * 0.05, y, k.c(GALV["dark"])))
    o.append('<ellipse cx="0" cy="0.17" rx="0.225" ry="0.048" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(GALV["dark"]), k.ink))
    o.append('<ellipse cx="0" cy="0.178" rx="0.190" ry="0.030" fill="%s"/>' % k.c("#5a9acc"))
    o.append('<path d="M-0.19,0.22 Q-0.21,0.38 -0.195,0.50" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.55"/>')
    # top handle: an arch over the body from the rear rim to the spout side, the hand grips its crown at the origin
    arch = "M-0.20,0.17 Q-0.20,-0.07 0,-0.06 Q0.20,-0.07 0.26,0.20"
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (arch, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (arch, k.c(GALV["light"])))
    # rose: a flared dish across the end of the spout, with holes
    o.append('<g transform="translate(0.66 0.05) rotate(-42)"><path d="M-0.03,-0.050 L0.07,-0.115 Q0.115,0 0.07,0.115 L-0.03,0.050 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             '<ellipse cx="0.075" cy="0" rx="0.030" ry="0.108" fill="%s" stroke="%s" stroke-width="0.012"/>'
             '<circle cx="0.078" cy="-0.060" r="0.010" fill="%s"/><circle cx="0.078" cy="-0.020" r="0.010" fill="%s"/><circle cx="0.078" cy="0.020" r="0.010" fill="%s"/><circle cx="0.078" cy="0.060" r="0.010" fill="%s"/></g>'
             % (_lin(k, "wr", GALV["light"], GALV["base"], GALV["dark"], 0, -0.1, 0, 0.1), k.ink, k.c(GALV["dark"]), k.ink, k.ink, k.ink, k.ink, k.ink))
    return "".join(o)


def _can_stream(k, x0, y0, L, t):
    """a thin stream of water falling straight down (screen) from (x0, y0), length L, drops running down with t."""
    if L < 0.02:
        return ""
    o = []
    for i, dx in enumerate((-0.030, 0.0, 0.030)):
        xs = x0 + dx * 0.6
        xe = x0 + dx * 1.6 + 0.05 * (L / 1.0)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" stroke-dasharray="0.10 0.035" stroke-dashoffset="%.4f" opacity="0.95"/>'
                 % (xs, y0, (xs + xe) / 2 + 0.01, y0 + L * 0.55, xe, y0 + L, k.c("#78c4ec"), -((t * 0.9 + i * 0.043) % 0.135)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
             % (x0, y0, x0 + 0.03, y0 + L * 0.55, x0 + 0.05 * L + 0.01, y0 + L))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.016" fill="%s" opacity="0.8"/>' % (x0 + 0.05 * L + 0.01, y0 + L + 0.006, k.c("#78c4ec")))
    return "".join(o)


def _toy_tank_body(k, swing):
    """a tin toy Mark I (rhomboid) hanging by a string from the hand (origin); the whole thing swings by `swing` degrees about the hand."""
    o = ['<g transform="rotate(%.3f)">' % swing]
    o.append('<path d="M0,0 L0,0.40" stroke="%s" stroke-width="0.026" stroke-linecap="round"/><path d="M0,0 L0,0.40" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (k.ink, k.c("#efe2b8")))
    o.append('<g transform="translate(0 0.40) scale(0.86)">')
    # track loop = the rhomboid outline (front steeper than the tail), then the hull, sponson, cab, gun, tail wheel
    loop = "M-0.34,0.27 Q-0.40,0.27 -0.36,0.21 L-0.19,0.035 Q-0.16,0.0 -0.11,0.0 L0.16,-0.01 Q0.21,-0.01 0.24,0.035 L0.38,0.21 Q0.43,0.27 0.36,0.27 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.075" stroke-linejoin="round"/>' % (loop, k.c("#46522a"), k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.052" stroke-linejoin="round"/>' % (loop, k.c("#5c6c34")))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.052" stroke-linejoin="round" stroke-dasharray="0.014 0.030"/>' % (loop, k.c("#9aae58")))
    hull = "M-0.24,0.20 L-0.12,0.06 L0.17,0.05 L0.30,0.20 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (hull, _lin(k, "ty", "#a4b858", "#7a9238", "#566c24", 0, 0.05, 0, 0.20), k.ink))
    o.append('<path d="M-0.04,-0.005 L-0.03,-0.085 L0.10,-0.085 L0.12,-0.005 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#6c8430"), k.ink))
    o.append('<path d="M0.0,-0.060 L0.085,-0.060" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.10,0.085 L0.12,0.085 L0.12,0.185 L-0.10,0.185 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#8aa240"), k.ink))
    o.append('<path d="M0.12,0.125 L0.30,0.125" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M0.12,0.125 L0.30,0.125" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (k.ink, k.c("#6a7480")))
    o.append('<path d="M-0.34,0.265 L-0.46,0.20" stroke="%s" stroke-width="0.034" stroke-linecap="round"/><circle cx="-0.47" cy="0.20" r="0.050" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.ink, k.c("#caa030"), k.ink))
    o.append('<path d="M-0.18,0.06 L-0.04,0.045" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>')
    o.append('</g></g>')
    return "".join(o)


def _chalk(k, pts, w=0.030, closed=False, wob=0.006, seed=0.0):
    """a chalk stroke through pts: slightly wobbly, a second thin pass for the grain.  White lines only."""
    q = []
    for i, (x, y) in enumerate(pts):
        q.append((x + wob * math.sin(i * 2.3 + seed), y + wob * math.cos(i * 1.7 + seed * 1.3)))
    d = "M%.4f,%.4f" % q[0] + "".join("L%.4f,%.4f" % p for p in q[1:]) + ("Z" if closed else "")
    d2 = "M%.4f,%.4f" % (q[0][0] + 0.004, q[0][1] - 0.004) + "".join("L%.4f,%.4f" % (p[0] - 0.004, p[1] + 0.004) for p in q[1:]) + ("Z" if closed else "")
    return ('<path d="%s" fill="none" stroke="#f6f4ea" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round" opacity="0.96"/>'
            '<path d="%s" fill="none" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round" opacity="0.45" stroke-dasharray="0.06 0.03"/>' % (d, w, d2, w * 0.45))


def _chalkboard_body(k):
    """a held slate: wooden frame 1.6 x 1.1 D, the hand (origin) grips the right edge, the board hangs to -x.  The drawing is white chalk
    lines only: two ground lines, the trench between them, and a side-on rhomboid tank straddling the gap.  No letters, no arrows."""
    x0, x1, y0, y1 = -1.60, 0.0, -0.46, 0.64
    o = []
    fr = _lin(k, "cbf", WOOD["light"], WOOD["base"], WOOD["dark"], 0, y0, 0, y1)
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.045" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (x0, y0, x1 - x0, y1 - y0, fr, k.ink))
    fi = 0.075
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.018" fill="%s" stroke="%s" stroke-width="0.014"/>' % (x0 + fi, y0 + fi, x1 - x0 - 2 * fi, y1 - y0 - 2 * fi,
                                                                                                                         _lin(k, "cbs", "#2f4238", "#1e2e26", "#141e19", 0, y0, 0, y1), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (x0 + 0.03, y0 + 0.03, x1 - 0.03, y0 + 0.03, x0 + 0.03, y0 + 0.05, x0 + 0.03, y1 - 0.03, k.c(WOOD["light"])))
    # rubbed-out smudges (dust, no shapes that read as marks)
    o.append('<ellipse cx="-0.50" cy="0.40" rx="0.30" ry="0.10" fill="#ffffff" opacity="0.045"/><ellipse cx="-1.18" cy="-0.22" rx="0.26" ry="0.07" fill="#ffffff" opacity="0.04"/>')
    # ground lines either side of the trench, and the trench itself (a U between them)
    o.append(_chalk(k, [(-1.47, 0.20), (-1.26, 0.195), (-1.06, 0.19)], 0.032, seed=1.0))
    o.append(_chalk(k, [(-0.54, 0.19), (-0.34, 0.195), (-0.13, 0.20)], 0.032, seed=2.0))
    o.append(_chalk(k, [(-1.06, 0.19), (-1.02, 0.40), (-0.98, 0.50), (-0.62, 0.50), (-0.58, 0.40), (-0.54, 0.19)], 0.026, seed=3.0))
    # the tank: a side-on rhomboid (track loop outline, steeper nose), tilted nose-up across the gap
    cx, cy, tl = -0.80, -0.02, -8.0
    ca, sa = math.cos(math.radians(tl)), math.sin(math.radians(tl))

    def T(p):
        dx, dy = p[0] - cx, p[1] - cy
        return (cx + dx * ca - dy * sa, cy + dx * sa + dy * ca)
    loop = [(-1.30, 0.16), (-1.24, 0.12), (-1.04, -0.12), (-0.96, -0.16), (-0.62, -0.20), (-0.52, -0.17), (-0.34, 0.06), (-0.30, 0.13), (-0.34, 0.17), (-1.26, 0.17)]
    o.append(_chalk(k, [T(p) for p in loop], 0.030, closed=True, wob=0.004, seed=4.0))
    inner = [(-1.12, 0.09), (-0.99, -0.08), (-0.64, -0.12), (-0.50, 0.08)]
    o.append(_chalk(k, [T(p) for p in inner], 0.018, seed=5.0))
    o.append(_chalk(k, [T(p) for p in [(-0.90, 0.02), (-0.90, -0.05), (-0.72, -0.05), (-0.72, 0.02), (-0.90, 0.02)]], 0.018, seed=6.0))
    o.append(_chalk(k, [T(p) for p in [(-0.72, -0.015), (-0.44, -0.03)]], 0.024, seed=7.0))
    o.append(_chalk(k, [T(p) for p in [(-0.80, -0.05), (-0.82, -0.19), (-0.70, -0.19), (-0.69, -0.12)]], 0.018, seed=8.0))
    # a lip with a stub of chalk resting on it
    o.append('<path d="M-1.45,0.585 L-1.18,0.585" stroke="#e8e6dc" stroke-width="0.030" stroke-linecap="round"/>')
    return "".join(o)


def _prop_body(k, kind, ang=0.0):
    o = []
    if kind == "hammer25":
        o.append('<path d="M-0.22,-0.028 L0.40,-0.022 L0.40,0.022 L-0.22,0.028 Q-0.25,0 -0.22,-0.028 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_wood_grad(k, "hw"), k.ink))
        o.append('<path d="M-0.18,-0.010 L0.36,-0.008" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["light"]))
        gs = _lin(k, "hh", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.12, 0, 0.12)
        o.append('<path d="M0.38,-0.085 L0.56,-0.085 L0.56,-0.125 L0.66,-0.125 L0.66,0.125 L0.56,0.125 L0.56,0.085 L0.38,0.085 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (gs, k.ink))
        o.append('<circle cx="0.33" cy="0" r="0.095" fill="%s" stroke="%s" stroke-width="0.020"/>' % (gs, k.ink))
        o.append('<path d="M0.41,-0.050 L0.54,-0.052 M0.28,-0.05 Q0.30,-0.07 0.33,-0.07" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.7" fill="none"/>')
        o.append('<path d="M0.56,-0.085 L0.56,0.085" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c(STEEL["deep"]))
    elif kind == "spanner25":
        gs = _lin(k, "sp", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.06, 0, 0.06)
        o.append('<path d="M-0.14,-0.034 Q-0.18,0 -0.14,0.034 L0.60,0.030 L0.64,0.085 Q0.72,0.135 0.80,0.090 L0.82,0.030 L0.74,0.030 L0.74,-0.030 L0.82,-0.030 L0.80,-0.090 Q0.72,-0.135 0.64,-0.085 L0.60,-0.030 Z" '
                 'fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gs, k.ink))
        o.append('<path d="M-0.10,-0.016 L0.56,-0.014" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>')
        o.append('<circle cx="-0.10" cy="0" r="0.012" fill="%s" stroke="%s" stroke-width="0.006"/>' % (k.c(STEEL["dark"]), k.ink))
    elif kind == "paint_brush25":
        pc = PAINTS.get(_POSE25["paint"], PAINTS["white"])
        o.append('<path d="M-0.24,-0.022 L0.30,-0.030 L0.30,0.030 L-0.24,0.022 Q-0.27,0 -0.24,-0.022 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_wood_grad(k, "bw"), k.ink))
        o.append('<path d="M0.40,-0.060 L0.62,-0.095 Q0.66,0 0.62,0.095 L0.40,0.060 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(pc), k.ink))
        st = "".join("M0.44,%.4f L0.61,%.4f " % (y * 0.6, y * 1.4) for y in (-0.04, -0.02, 0, 0.02, 0.04))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.007" opacity="0.5"/>' % (st, k.c("#808080")))
        gf = _lin(k, "bf", GALV["light"], GALV["base"], GALV["dark"], 0, -0.06, 0, 0.06)
        o.append('<path d="M0.28,-0.040 L0.42,-0.066 L0.42,0.066 L0.28,0.040 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (gf, k.ink))
        o.append('<path d="M0.34,-0.052 L0.34,0.052" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(GALV["dark"]))
        o.append('<path d="M0.64,0.04 q0.012,0.05 0,0.07 q-0.014,-0.02 0,-0.07 Z" fill="%s" stroke="%s" stroke-width="0.007"/>' % (k.c(pc), k.ink))
    elif kind == "ladle25":
        o.append('<path d="M-0.12,-0.024 L0.84,-0.016 L0.84,0.016 L-0.12,0.024 Q-0.15,0 -0.12,-0.024 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_wood_grad(k, "lw"), k.ink))
        o.append('<path d="M-0.08,-0.008 L0.80,-0.006" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["light"]))
        gs = _lin(k, "lb", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.12, 0, 0.12)
        o.append('<path d="M0.82,-0.030 L0.90,-0.115 Q1.06,-0.150 1.12,0 Q1.06,0.150 0.90,0.115 L0.82,0.030 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gs, k.ink))
        o.append('<ellipse cx="1.01" cy="0" rx="0.050" ry="0.095" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(STEEL["deep"]), k.ink))
        o.append('<path d="M0.92,-0.090 Q1.02,-0.120 1.07,-0.070" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>')
    elif kind == "swagger25":
        o.append('<path d="M-0.18,-0.020 L0.92,-0.014 L0.92,0.014 L-0.18,0.020 Q-0.21,0 -0.18,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#4a2a18"), k.ink))
        o.append('<path d="M-0.14,-0.008 L0.88,-0.005" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c("#9a6a44"))
        o.append(_circ((-0.20, 0), 0.040, k.c(BRASS["base"]), k, 0.012))
        o.append('<path d="M0.88,-0.024 L0.99,-0.018 L0.99,0.018 L0.88,0.024 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
        o.append('<path d="M-0.05,0.016 q0.03,0.12 0.06,0.02 q-0.01,-0.05 -0.03,-0.04" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(LEATHER["base"]))
    elif kind == "flag25":
        o.append('<path d="M-0.20,-0.016 L0.84,-0.012 L0.84,0.012 L-0.20,0.016 Q-0.22,0 -0.20,-0.016 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_wood_grad(k, "fw", -0.02, 0.02), k.ink))
        o.append(_circ((0.87, 0), 0.032, k.c(BRASS["base"]), k, 0.010))
        ph = 2 * math.pi * _POSE25["t"]
        top, bot = [], []
        L = 0.56
        for i in range(9):
            s = i / 8.0
            w1 = 0.04 * math.sin(ph - s * 5.0) * s
            top.append((0.80 + w1 * 0.8, 0.012 + L * s))
            bot.append((0.40 - w1 * 0.8, 0.012 + L * s))
        notch = (0.60 + 0.03 * math.sin(ph - 4.2), L - 0.15)
        pts = top + [notch] + bot[::-1]
        fl = _poly_d(pts)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (fl, k.c("#ee2a1e"), k.ink))
        for i in range(1, 8, 2):
            a, b = top[i], bot[i]
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (a[0], a[1], b[0], b[1], k.c("#9a1410")))
        o.append('<path d="M0.80,0.04 L0.44,0.04" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.4"/>')
    elif kind == "helmet_stick25":
        o.append('<path d="M-0.30,-0.020 L1.98,-0.016 L1.98,0.016 L-0.30,0.020 Q-0.33,0 -0.30,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_wood_grad(k, "ss", -0.02, 0.02), k.ink))
        o.append('<path d="M-0.26,-0.007 L1.94,-0.005" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["light"]))
        o.append(_helmet_side(k, 2.0, 0.0, 0.0, 1.0, dict(light="#a2a45a", base="#7c8040", dark="#4e5228")).replace("rotate(90.000)", "rotate(90.000)"))
    elif kind == "plan25":
        W = _POSE25["plan_dx"]
        gp = _lin(k, "pp", "#4a82c4", "#2c5f9e", "#1c4478", 0, 0, 0, 0.9)
        wl = "#d8e8f8"
        d = "M0,0 L%.4f,0 L%.4f,0.88 Q%.4f,0.94 %.4f,0.86 Q%.4f,0.80 %.4f,0.90 Q%.4f,0.84 0,0.80 Z" % (-W, -W, -W * 0.8, -W * 0.6, -W * 0.45, -W * 0.28, -W * 0.12)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, gp, k.ink))
        # plain white lines: border, a grid, and the side profile of a rhomboid tank (lines only)
        o.append('<path d="M%.4f,0.07 L%.4f,0.07 L%.4f,0.72 L%.4f,0.72 Z" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (-0.07, -W + 0.07, -W + 0.07, -0.07, wl))
        for i in range(1, 6):
            o.append('<path d="M%.4f,0.07 L%.4f,0.72" stroke="%s" stroke-width="0.005" opacity="0.5"/>' % (-W * i / 6.0, -W * i / 6.0, wl))
        for j in (0.24, 0.40, 0.56):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.005" opacity="0.5"/>' % (-0.07, j, -W + 0.07, j, wl))
        tx = -W * 0.5
        o.append('<path d="M%.4f,0.52 L%.4f,0.30 L%.4f,0.26 L%.4f,0.26 L%.4f,0.38 L%.4f,0.52 Z" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (tx - 0.36, tx - 0.18, tx - 0.04, tx + 0.18, tx + 0.34, tx + 0.30, wl))
        o.append('<path d="M%.4f,0.54 Q%.4f,0.46 %.4f,0.54 M%.4f,0.54 Q%.4f,0.46 %.4f,0.54" fill="none" stroke="%s" stroke-width="0.010"/>' % (tx - 0.26, tx - 0.20, tx - 0.14, tx + 0.06, tx + 0.12, tx + 0.18, wl))
        gr = _lin(k, "pr", "#ffffff", "#e4dcc4", "#b8b098", 0, -0.04, 0, 0.05)
        o.append('<rect x="%.4f" y="-0.045" width="%.4f" height="0.090" rx="0.045" fill="%s" stroke="%s" stroke-width="0.016"/>' % (-W - 0.02, W + 0.04, gr, k.ink))
        o.append('<ellipse cx="%.4f" cy="0" rx="0.022" ry="0.045" fill="%s" stroke="%s" stroke-width="0.008"/>' % (-W - 0.02, k.c("#c8c0a8"), k.ink))
    elif kind == "mg25":
        gs = _lin(k, "mj", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.09, 0, 0.10)
        o.append('<path d="M0.10,-0.085 L1.00,-0.085 L1.00,0.085 L0.10,0.085 Q0.04,0 0.10,-0.085 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gs, k.ink))
        for x in (0.22, 0.36, 0.50, 0.64, 0.78, 0.92):
            o.append('<path d="M%.4f,-0.080 L%.4f,0.080" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (x, x, k.c(STEEL["deep"])))
        o.append('<path d="M1.00,-0.040 L1.14,-0.032 L1.14,0.032 L1.00,0.040 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(STEEL["dark"]), k.ink))
        o.append('<path d="M0.16,-0.060 L0.98,-0.062" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>')
        o.append('<path d="M-0.14,-0.070 L0.10,-0.085 L0.10,0.100 L-0.14,0.110 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(STEEL["dark"]), k.ink))
        for sy in (-0.05, 0.06):
            o.append('<path d="M-0.02,%.4f L-0.10,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M-0.02,%.4f L-0.10,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>'
                     % (sy, sy, k.ink, sy, sy, k.c(WOOD["dark"])))
        o.append('<rect x="0.16" y="0.05" width="0.20" height="0.13" fill="%s" stroke="%s" stroke-width="0.014"/><path d="M0.18,0.09 L0.34,0.09" stroke="%s" stroke-width="0.012"/>' % (k.c("#5a6a3a"), k.ink, k.c(BRASS["base"])))
        drop = _POSE25.get("mg_drop", 0.52)
        o.append('<path d="M0.12,0.085 L0.02,%.4f M0.78,0.085 L0.88,%.4f" stroke="%s" stroke-width="0.056" stroke-linecap="round"/><path d="M0.12,0.085 L0.02,%.4f M0.78,0.085 L0.88,%.4f" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>'
                 % (drop - 0.03, drop - 0.03, k.ink, drop - 0.03, drop - 0.03, k.c(STEEL["base"])))
        o.append('<path d="M-0.10,%.4f L1.02,%.4f" stroke="%s" stroke-width="0.060" stroke-linecap="round"/><path d="M-0.10,%.4f L1.02,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>'
                 % (drop, drop, k.ink, drop, drop, k.c(STEEL["dark"])))
    elif kind == "shovel25":
        # trench spade: wooden D-handle at the hand (origin), long ash shaft, steel socket and a broad rounded blade (face on);
        # pose key dirt25 0..1 heaps a clump of earth on the blade (the clump sits on the -y side = the 'up' side of the blade)
        o.append('<path d="M0.10,-0.026 L1.10,-0.022 L1.10,0.022 L0.10,0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_wood_grad(k, "sw", -0.03, 0.03), k.ink))
        o.append('<path d="M0.16,-0.010 L1.04,-0.008" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["light"]))
        o.append('<path d="M0.16,-0.040 L0.07,-0.145 Q-0.02,-0.175 -0.085,-0.125 L-0.085,0.125 Q-0.02,0.175 0.07,0.145 L0.16,0.040 Z M0.07,-0.085 L-0.03,-0.085 L-0.03,0.085 L0.07,0.085 Z" '
                 'fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_wood_grad(k, "sd", -0.15, 0.15), k.ink))
        o.append('<path d="M-0.065,-0.105 L-0.065,0.105" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(WOOD["light"]))
        gs = _lin(k, "sb", "#c4ccd4", "#8896a2", "#4e5a66", 0, -0.17, 0, 0.17)
        o.append('<path d="M1.06,-0.042 L1.20,-0.080 L1.20,0.080 L1.06,0.042 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(STEEL["dark"]), k.ink))
        o.append('<path d="M1.18,-0.165 L1.56,-0.165 Q1.74,-0.115 1.78,0 Q1.74,0.115 1.56,0.165 L1.18,0.165 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (gs, k.ink))
        o.append('<path d="M1.24,-0.125 L1.58,-0.125 Q1.68,-0.100 1.71,-0.040" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.75"/>')
        o.append('<path d="M1.22,0.0 L1.66,0.0" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % k.c(STEEL["deep"]))
        o.append(_circ((1.24, -0.10), 0.014, k.c(STEEL["deep"]), k, 0.005) + _circ((1.24, 0.10), 0.014, k.c(STEEL["deep"]), k, 0.005))
        dd = _POSE25["dirt"]
        if dd > 0.02:
            lump = [(1.14, 0.04), (1.14, -0.06), (1.20, -0.14), (1.31, -0.28), (1.44, -0.35), (1.56, -0.30), (1.66, -0.19), (1.74, -0.07), (1.74, 0.04), (1.45, 0.06)]
            pts = [(x, 0.04 + (y - 0.04) * (0.25 + 0.75 * dd)) if y < 0.04 else (x, y) for (x, y) in lump]
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(EARTH["base"]), k.ink))
            for (x, y, r, c) in ((1.30, -0.12, 0.034, "dark"), (1.50, -0.16, 0.040, "light"), (1.62, -0.07, 0.026, "dark"), (1.40, -0.04, 0.024, "light"), (1.24, -0.04, 0.020, "dark")):
                o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.85"/>' % (x, 0.04 + (y - 0.04) * (0.25 + 0.75 * dd), r * (0.6 + 0.4 * dd), k.c(EARTH[c])))
            if dd > 0.5:
                for (x, y, r) in ((1.38, -0.52, 0.030), (1.60, -0.58, 0.022), (1.50, -0.70, 0.016), (1.28, -0.62, 0.018)):
                    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008" opacity="%.2f"/>' % (x, y * (0.6 + 0.4 * dd), r, k.c(EARTH["base"]), k.ink, min(1.0, (dd - 0.5) * 4)))
    elif kind == "tin_cup25":
        # enamel tin mug, mouth up (-y), the handle on the hand's side (origin = the handle), the body to +x
        ge = _lin(k, "tc", "#ffffff", "#efe9d4", "#b9b39c", 0.08, 0, 0.40, 0)
        o.append('<path d="M0.10,-0.080 Q-0.10,-0.100 -0.09,0.0 Q-0.10,0.105 0.11,0.085" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M0.10,-0.080 Q-0.10,-0.100 -0.09,0.0 Q-0.10,0.105 0.11,0.085" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % k.c("#efe9d4"))
        o.append('<path d="M0.08,-0.150 L0.40,-0.150 L0.375,0.150 Q0.24,0.185 0.105,0.150 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (ge, k.ink))
        o.append('<path d="M0.081,-0.150 L0.399,-0.150 L0.396,-0.108 Q0.24,-0.082 0.084,-0.108 Z" fill="%s" opacity="0.95"/>' % k.c("#2a5cc8"))
        o.append('<path d="M0.10,0.115 Q0.24,0.145 0.36,0.115" fill="none" stroke="%s" stroke-width="0.014" opacity="0.9"/>' % k.c("#2a5cc8"))
        o.append('<ellipse cx="0.24" cy="-0.150" rx="0.160" ry="0.036" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#6c3a1a"), k.ink))
        o.append('<path d="M0.12,-0.152 Q0.24,-0.138 0.36,-0.152" fill="none" stroke="#ffffff" stroke-width="0.008" opacity="0.35"/>')
        o.append('<path d="M0.115,-0.080 Q0.110,0.0 0.125,0.090" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>')
        for (x, y) in ((0.30, 0.060), (0.34, 0.010), (0.19, 0.095)):
            o.append('<circle cx="%.3f" cy="%.3f" r="0.011" fill="%s"/>' % (x, y, k.c("#4a4a52")))
    return "".join(o)


def _upright_body(k, kind):
    o = []
    if kind == "bucket25":
        o.append('<path d="M-0.205,0.17 Q-0.200,-0.070 0,-0.060 Q0.200,-0.070 0.205,0.17" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M-0.205,0.17 Q-0.200,-0.070 0,-0.060 Q0.200,-0.070 0.205,0.17" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c(GALV["light"]))
        g = _lin(k, "bk", GALV["light"], GALV["base"], GALV["dark"], -0.22, 0, 0.22, 0)
        o.append('<path d="M-0.225,0.17 L0.225,0.17 L0.170,0.50 Q0,0.525 -0.170,0.50 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink))
        for y in (0.27, 0.38, 0.47):
            o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.75"/>' % (-0.225 + (y - 0.17) * 0.16, y, y + 0.03, 0.225 - (y - 0.17) * 0.16, y, k.c(GALV["dark"])))
        o.append('<ellipse cx="0" cy="0.17" rx="0.225" ry="0.050" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(GALV["dark"]), k.ink))
        o.append('<ellipse cx="0" cy="0.178" rx="0.190" ry="0.034" fill="%s"/>' % k.c("#5a9acc"))
        o.append('<path d="M-0.12,0.172 Q-0.04,0.162 0.06,0.170" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>')
        o.append('<ellipse cx="0.09" cy="0.186" rx="0.040" ry="0.010" fill="none" stroke="#ffffff" stroke-width="0.007" opacity="0.7"/>')
        o.append('<path d="M-0.20,0.15 Q-0.22,0.31 -0.205,0.41" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.5"/>')
        for sx in (-1, 1):
            o.append('<circle cx="%.4f" cy="0.17" r="0.014" fill="%s" stroke="%s" stroke-width="0.006"/>' % (sx * 0.225, k.c(GALV["light"]), k.ink))
    elif kind == "paint_pot25":
        pc = PAINTS.get(_POSE25["paint"], PAINTS["white"])
        o.append('<path d="M-0.130,0.11 Q-0.120,-0.040 0,-0.030 Q0.120,-0.040 0.130,0.11" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M-0.130,0.11 Q-0.120,-0.040 0,-0.030 Q0.120,-0.040 0.130,0.11" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % k.c(GALV["light"]))
        g = _lin(k, "pt", "#c8d0d6", "#8e9aa4", "#56626c", -0.14, 0, 0.14, 0)
        o.append('<path d="M-0.145,0.11 L0.145,0.11 L0.130,0.33 Q0,0.35 -0.130,0.33 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink))
        o.append('<ellipse cx="0" cy="0.11" rx="0.145" ry="0.036" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c(pc), k.ink))
        o.append('<path d="M-0.08,0.105 Q-0.02,0.095 0.05,0.103" fill="none" stroke="#ffffff" stroke-width="0.009" stroke-linecap="round" opacity="0.7"/>')
        for (x, ln) in ((-0.10, 0.11), (0.0, 0.17), (0.09, 0.08)):
            o.append('<path d="M%.4f,0.13 L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M%.4f,0.13 L%.4f,%.4f" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>'
                     % (x, x * 0.97, 0.13 + ln, k.ink, x, x * 0.97, 0.13 + ln, k.c(pc)))
        o.append('<path d="M-0.140,0.19 Q0,0.215 0.140,0.19" fill="none" stroke="%s" stroke-width="0.009" opacity="0.7"/>' % k.c(GALV["dark"]))
    elif kind == "helmet25":
        # a Brodie held in the hand, dome up, grip under the brim
        o.append(_helmet_side(k, 0.0, 0.0, -90.0, 0.80, dict(light="#a2a45a", base="#7c8040", dark="#4e5228")))
    elif kind == "watering_can25":
        o.append(_can_body(k))
    elif kind == "toy_tank25":
        o.append(_toy_tank_body(k, _POSE25["swing"]))
    elif kind == "chalkboard25":
        o.append(_chalkboard_body(k))
    return "".join(o)


NEW_PROPS25 = ("hammer25", "spanner25", "paint_brush25", "paint_pot25", "bucket25", "ladle25", "swagger25", "flag25", "helmet_stick25", "helmet25", "plan25", "mg25",
               "watering_can25", "shovel25", "tin_cup25", "toy_tank25", "chalkboard25")
NEW_TIP25 = {"hammer25": 0.66, "spanner25": 0.82, "paint_brush25": 0.66, "paint_pot25": 0.0, "bucket25": 0.0, "ladle25": 1.12, "swagger25": 0.99, "flag25": 0.88,
             "helmet_stick25": 2.35, "helmet25": 0.0, "plan25": 0.0, "mg25": 1.14, "watering_can25": 0.0, "shovel25": 1.78, "tin_cup25": 0.24, "toy_tank25": 0.0, "chalkboard25": 0.0}
TIP_XY25 = {"tin_cup25": (0.24, -0.15)}       # working point (hand frame) for the props whose tip is not on the prop axis
HUNG25 = ("watering_can25", "toy_tank25", "chalkboard25")   # held at one point and always upright (screen), not along the arm; drawn flipped for the left hand
UPRIGHT25 = ("bucket25", "paint_pot25", "helmet25")
PROP_EXT25 = {"hammer25": ((-0.25, -0.03), (0.66, -0.09), (0.66, 0.09), (0.33, 0.09)),
              "spanner25": ((-0.16, -0.04), (0.84, -0.14), (0.84, 0.14), (0.60, 0.05)),
              "paint_brush25": ((-0.27, -0.03), (0.66, -0.10), (0.66, 0.10), (0.4, 0.07)),
              "ladle25": ((-0.15, -0.03), (1.13, -0.16), (1.13, 0.16), (0.84, 0.0)),
              "swagger25": ((-0.25, -0.04), (-0.25, 0.04), (1.0, 0.0)),
              "flag25": ((-0.22, 0.0), (0.92, 0.0), (0.92, 0.62), (0.38, 0.62), (0.40, 0.0)),
              "helmet_stick25": ((-0.34, 0.0), (2.40, 0.0), (2.0, -0.62), (2.0, 0.62)),
              "plan25": ((0.05, -0.05), (-1.4, -0.06), (-1.4, 0.95), (-0.1, 0.95)),
              "mg25": ((-0.15, -0.10), (1.15, -0.09), (1.15, 0.52), (-0.12, 0.62)),
              "shovel25": ((-0.10, -0.18), (1.80, -0.18), (1.80, 0.18), (-0.10, 0.18)),
              "tin_cup25": ((-0.12, -0.17), (0.42, -0.17), (0.42, 0.19), (-0.12, 0.19))}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS25:
        return _O25["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    nm = kind[:-2]
    if kind in HUNG25:
        return _hung_prop(k, kind, H, sc, key, side, an, nm)
    if kind in UPRIGHT25:
        cx, cy = H[0], H[1]
        if kind == "helmet25":
            cy = H[1] - 0.02
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (cx, cy, sc, _upright_body(k, kind))
        ext = {"bucket25": ((-0.23, 0.17), (0.23, 0.17), (-0.17, 0.52), (0.17, 0.52), (0.0, -0.07)),
               "paint_pot25": ((-0.15, 0.11), (0.15, 0.11), (-0.13, 0.35), (0.13, 0.35), (0.0, -0.04)),
               "helmet25": ((-0.50, -0.02), (0.50, -0.02), (0.0, -0.30))}[kind]
        for (x, y) in ext:
            k.ext.append((cx + x * sc, cy + y * sc, 0.03))
        tip = (cx, cy + (0.52 if kind == "bucket25" else 0.35 if kind == "paint_pot25" else -0.28) * sc)
        an[nm + "_" + key] = tip
        return o, tip
    if kind == "plan25":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _prop_body(k, kind, 0.0) if side > 0 else
                                                                         '<g transform="scale(-1 1)">%s</g>' % _prop_body(k, kind, 0.0))
        W = _POSE25["plan_dx"]
        for (x, y) in ((0.05, -0.05), (-W - 0.04, -0.05), (-W - 0.02, 0.92), (-0.1, 0.92)):
            k.ext.append((H[0] + side * x * sc, H[1] + y * sc, 0.03))
        far = (H[0] - side * (W + 0.02) * sc, H[1])
        an["plan_far_" + key] = far
        an["plan_" + key] = (H[0] - side * W * 0.5 * sc, H[1] + 0.5 * sc)
        return o, (H[0] - side * W * 0.5 * sc, H[1] + 0.5 * sc)
    if kind == "mg25":
        gy = _POSE25["mg_gy"]
        _POSE25["mg_drop"] = 0.52 if gy is None else max(0.12, (gy - H[1]) / sc)
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _prop_body(k, kind, ang))
    for (x, y) in PROP_EXT25.get(kind, ((0.0, 0.0), (NEW_TIP25[kind], 0.0))):
        qx, qy = _rot(x * sc, y * sc, ang)
        k.ext.append((H[0] + qx, H[1] + qy, 0.03))
    if kind == "mg25":
        gy = _POSE25["mg_gy"]
        if gy is not None:
            k.ext.append((H[0], gy, 0.04))
    if kind == "shovel25" and _POSE25["dirt"] > 0.02:
        qx, qy = _rot(1.45 * sc, -(0.40 if _POSE25["dirt"] < 0.5 else 0.70) * sc, ang)
        k.ext.append((H[0] + qx, H[1] + qy, 0.03))
    tx, ty = _rot(TIP_XY25.get(kind, (NEW_TIP25[kind], 0.0))[0] * sc, TIP_XY25.get(kind, (0.0, 0.0))[1] * sc, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[nm + "_" + key] = tip
    return o, tip


def _hung_prop(k, kind, H, sc, key, side, an, nm):
    """watering_can25 (tilted by pour25, stream at pour > 0.5), toy_tank25 (swings with t), chalkboard25: held at one point of the hand,
    always upright on the screen; the body is drawn flipped for the left hand so the spout / board points the same way round the body."""
    sx = side * sc
    if kind == "watering_can25":
        tilt = _POSE25["pour"] * CAN_TILT
        o = '<g transform="translate(%.4f %.4f) scale(%.4f %.4f) rotate(%.3f)">%s</g>' % (H[0], H[1], sx, sc, tilt, _can_body(k))
        for (x, y) in ((-0.46, 0.20), (0.70, 0.0), (0.22, 0.58), (-0.23, 0.58), (0.0, -0.08)):
            qx, qy = _rot(x, y, tilt)
            k.ext.append((H[0] + side * qx * sc, H[1] + qy * sc, 0.03))
        rx, ry = _rot(CAN_ROSE[0] + 0.05, CAN_ROSE[1], tilt)
        tip = (H[0] + side * rx * sc, H[1] + ry * sc)
        pr = _POSE25["pour"]
        if pr > 0.5:
            L = 1.25 * sc * min(1.0, (pr - 0.5) / 0.2)
            o += _can_stream(k, tip[0], tip[1], L, _POSE25["t"])
            k.ext.append((tip[0] + 0.06 * L, tip[1] + L, 0.04))
    elif kind == "toy_tank25":
        sw = _POSE25["swing"]
        o = '<g transform="translate(%.4f %.4f) scale(%.4f %.4f)">%s</g>' % (H[0], H[1], sx, sc, _toy_tank_body(k, sw))
        for (x, y) in ((-0.52, 0.55), (0.46, 0.55), (0.0, 0.30), (0.0, 0.76)):
            qx, qy = _rot(x, y, sw)
            k.ext.append((H[0] + side * qx * sc, H[1] + qy * sc, 0.03))
        qx, qy = _rot(0.0, 0.40 + 0.12, sw)
        tip = (H[0] + side * qx * sc, H[1] + qy * sc)
    else:
        o = '<g transform="translate(%.4f %.4f) scale(%.4f %.4f)">%s</g>' % (H[0], H[1], sx, sc, _chalkboard_body(k))
        for (x, y) in ((0.02, -0.48), (-1.62, -0.48), (-1.62, 0.66), (0.02, 0.66)):
            k.ext.append((H[0] + side * x * sc, H[1] + y * sc, 0.03))
        tip = (H[0] + side * BOARD_TANK[0] * sc, H[1] + BOARD_TANK[1] * sc)
    an[nm + "_" + key] = tip
    return o, tip


# ============================================================================= pose keys
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE25["hat_off"] = _f(g("hat_off25"), 0.0, 0.0, 1.0)
    _POSE25["hat_up"] = _f(g("hat_up25"), 0.0, -0.5, 1.5)
    gy = g("mg_gy25")
    _POSE25["mg_gy"] = None if gy is None else _f(gy, 0.52, 0.1, 2.5)
    pc = g("paint_col25")
    _POSE25["paint"] = pc if isinstance(pc, str) and pc in PAINTS else "white"
    _POSE25["t"] = _f(g("t"), 0.0, -1000.0, 1000.0)
    _POSE25["plan_dx"] = _f(g("plan_w25"), 1.25, 0.6, 2.0)
    _POSE25["pour"] = _f(g("pour25"), 0.0, 0.0, 1.0)
    _POSE25["dirt"] = _f(g("dirt25"), 0.0, 0.0, 1.0)
    _POSE25["swing"] = 16.0 * math.sin(2.0 * math.pi * _POSE25["t"])
    _POSE25["fire"] = _f(g("fire25"), 0.0, 0.0, 1.0)
    _POSE25["glasses_dy"] = _f(g("glasses_dy25"), 0.0, 0.0, 1.0)
    return _O25["_norm"](C, pose)


# ============================================================================= cast
_FLAGS = dict(_cast25=True, _cast24=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)


def _m(**kw):
    d = dict(_FLAGS)
    d.update(kw)
    return d


KHAKI = dict(light="#b3a45a", base="#8f813f", dark="#645a24")
INK_HAIR = "#2a221e"
NEW_CAST25 = {
    # THE MOCKER: stout, big belly, red cheeks, huge white walrus moustache, khaki service dress with a Sam Browne belt, scarlet gorget
    # tabs and rows of medal ribbons, a khaki peaked cap with a scarlet band, polished brown boots
    "general25": _m(
        build="stout", seed=25.1,
        torso_w=1.52, torso_h=1.26, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.14, stance=0.07, wide=0.32, limb_w=0.072,
        eye_y=0.000, brow="stroke", brow_th=0.088, mouth="frown", moustache=True, moustache_style="walrus25", tache_scale=1.0,
        smirk_side=1, cheeks="#f23a2e", chins=True, age_lines=True,
        hat="newsboy", hat_style="peakcap25", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(crown="#8f813f", crown_l="#b3a35c", crown_d="#645a24", band="#ee2418", band_d="#a8120e"),
        hair=dict(color="#ecebee", front=0.06, grow=0.20),
        costume="staff25", coat_len=0.20, coat_flare=0.10,
        sleeve=dict(color="#8f813f", dark="#645a24", cuff="#6a5c28", len=0.84, w=0.215),
        shorts=dict(color="#8f813f", dark="#645a24", cuff="#8f813f", len=0.52, w=0.205),
        boots=dict(color="#7a4020", cuff="#9a5a30", h=0.42, toe=0.18),
        colors=dict(base="#8f813f", dark="#645a24", lapel="#a09050", shirt="#b9a964", tie="#5a3a22", tab="#ee2418", pants="#8f813f",
                    moustache="#f6f4f0", moustache_l="#c4c0ca"),
    ),
    # THE QUIET HERO: slim, young, clean-shaven, a rust flat cap with a red pencil behind the ear, a teal waistcoat over a cream shirt with
    # the sleeves rolled up, dark trousers, brown work boots
    "engineer25": _m(
        build="slim", seed=25.2,
        torso_w=0.60, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.76, hip_x=0.15, leg=1.40, stance=0.07, wide=0.26, limb_w=0.054,
        eye_y=0.040, brow="dome", brow_th=0.040, mouth="dash", moustache=False, smirk_side=1, cheeks="#eca090",
        hat="newsboy", hat_style="flatcap25", cap_style="neat", hat_tilt=-6.0, ear_pencil=True,
        hat_colors=dict(light="#ee8a40", base="#cc5a1a", dark="#8e3a0c", visor="#8a4210", band="#3a2014", check="#f4b070", seam="#5a2c0c"),
        hair=dict(color="#7a5230", front=0.08, grow=0.22),
        costume="waist25",
        sleeve=dict(color="#d2c192", dark="#a8986a", cuff="#e6d8aa", len=0.50, roll=True, w=0.140),
        shorts=dict(color="#3a3430", dark="#241f1c", cuff="#3a3430", len=0.90, w=0.125),
        boots=dict(color="#4a3220", cuff="#4a3220", h=0.10, toe=0.15),
        colors=dict(base="#08909c", dark="#065a64", shirt="#d2c192", pants="#3a3430", pencil="#d5392f"),
    ),
    # Lincoln factory workers.  a: big black beard, stocky, bib overalls, baggy mustard cap;  b: short and round, bald with a ginger fringe,
    # ginger moustache, leather apron;  c: tall and lanky, boiler suit, tight slate-blue cap, big brows
    "worker_a25": _m(
        build="regular", seed=25.31,
        torso_w=0.92, torso_h=0.98, profile=CE.PROFILE_REGULAR, shift_pow=1.05,
        shoulder=(0.31, 0.48), arm=0.72, hip_x=0.16, leg=1.18, stance=0.06, wide=0.27, limb_w=0.064,
        eye_y=0.010, brow="stroke", brow_th=0.078, mouth="dash", moustache=False, smirk_side=1, cheeks="#e48a74",
        bigbeard25=dict(color="#3a2418", dark="#1e1008", light="#7a5638"),
        hat="newsboy", hat_style="flatcap25", cap_style="baggy", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(light="#f4c838", base="#dca412", dark="#a47404", visor="#9a6c08", band="#4a3014", check="#fbe07a", seam="#7a5006"),
        hair=dict(color="#3a2418", front=0.06, grow=0.20),
        costume="work25", work_style="bib",
        sleeve=dict(color="#c4521c", dark="#823012", cuff="#dc6a34", len=0.50, roll=True, w=0.160),
        shorts=dict(color="#2458d0", dark="#173c98", cuff="#2458d0", len=0.90, w=0.150),
        boots=dict(color="#3a2a22", cuff="#3a2a22", h=0.11, toe=0.16),
        colors=dict(base="#c4521c", dark="#823012", denim="#2458d0", denim_d="#173c98", stitch="#f4cc6a", pants="#2458d0"),
    ),
    "worker_b25": _m(
        build="regular", seed=25.32,
        torso_w=1.08, torso_h=0.88, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.34, 0.47), arm=0.68, hip_x=0.17, leg=0.94, stance=0.06, wide=0.27, limb_w=0.066,
        eye_y=0.010, brow="stroke", brow_th=0.066, mouth="smirk", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=-1, cheeks="#ee8a74",
        hat="newsboy", hat_style="bare7", hat_tilt=0.0, ear_pencil=False,
        hair=dict(color="#d86a1c", front=0.0, grow=0.24),
        costume="work25", work_style="apron",
        sleeve=dict(color="#6a7a5a", dark="#465238", cuff="#8a9a76", len=0.50, roll=True, w=0.175),
        shorts=dict(color="#4a3a30", dark="#2e241e", cuff="#4a3a30", len=0.90, w=0.165),
        boots=dict(color="#4a3224", cuff="#4a3224", h=0.10, toe=0.16),
        colors=dict(base="#6a7a5a", dark="#465238", collar="#7e8e6c", strap="#5a3418", denim="#7a4a28", denim_d="#4e2e16", stitch="#e0b868", pants="#4a3a30",
                    moustache="#d86a1c", moustache_l="#f4a45a"),
    ),
    "worker_c25": _m(
        build="slim", seed=25.33,
        torso_w=0.56, torso_h=1.06, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.22, 0.52), arm=0.80, hip_x=0.14, leg=1.62, stance=0.06, wide=0.24, limb_w=0.052,
        eye_y=0.030, brow="stroke", brow_th=0.100, mouth="dash", moustache=False, smirk_side=1, cheeks="#eca090",
        hat="newsboy", hat_style="flatcap25", cap_style="docker", hat_tilt=4.0, ear_pencil=False,
        hat_colors=dict(light="#5a86bc", base="#3a5f95", dark="#243e68", visor="#2a4670", band="#1c2e4c", check="#8ab0dc", seam="#1c2e4c"),
        hair=dict(color="#2a221e", front=0.06, grow=0.18),
        costume="work25", work_style="boiler",
        sleeve=dict(color="#4a6a3a", dark="#2e4624", cuff="#5e8248", len=0.55, roll=True, w=0.125),
        shorts=dict(color="#4a6a3a", dark="#2e4624", cuff="#4a6a3a", len=0.90, w=0.115),
        boots=dict(color="#2e2420", cuff="#2e2420", h=0.12, toe=0.16),
        colors=dict(base="#4a6a3a", dark="#2e4624", denim="#5a7e46", stitch="#d8c070", pants="#4a6a3a"),
    ),
}


def _tommy(name, seed, build, tw, th, profile, leg, arm, lw, khaki, web, cover, hat_col, hat_tilt, kit, puttee, **kw):
    sh = (0.25 + 0.2 * (tw - 0.62), 0.48)
    d = _m(build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile, shift_pow=1.05,
           shoulder=sh, arm=arm, hip_x=0.14 + 0.05 * (tw - 0.62), leg=leg, stance=0.06, wide=0.26, limb_w=lw,
           eye_y=0.030, brow="stroke", brow_th=0.060, mouth="dash", smirk_side=1, cheeks="#ee9078", moustache=False,
           hat="newsboy", hat_style="brodie25", hat_tilt=hat_tilt, ear_pencil=False, cover25=cover, hat_colors=hat_col,
           hair=dict(color="#4a3226", front=0.06, grow=0.20),
           costume="tunic25", kit25=kit, puttee25=puttee, coat_len=0.05, coat_flare=0.02,
           sleeve=dict(color=khaki, dark=P._shade(khaki, 0.65), cuff=P._shade(khaki, 0.80), len=0.84, w=0.150 + 0.06 * (tw - 0.62)),
           shorts=dict(color=khaki, dark=P._shade(khaki, 0.65), cuff=khaki, len=0.50, w=0.150),
           boots=dict(color="#3a2a22", cuff="#3a2a22", h=0.08, toe=0.16),
           colors=dict(base=khaki, dark=P._shade(khaki, 0.68), web=web, web_d=P._shade(web, 0.76), scarf="#e41e1a", scarf_d="#900e0e", pants=khaki))
    d.update(kw)
    return d


NEW_CAST25.update({
    # Tommies: a medium, freckled, ginger, bottle on the hip;  b tall and thin, sandy khaki, big drooping Kitchener moustache, hessian cover;
    # c short and round, red muffler, tan helmet;  d broad, black bushy moustache and stubble, dark helmet worn crooked, entrenching tool
    "tommy_a25": _tommy("a", 25.41, "regular", 0.78, 1.00, CE.PROFILE_ATHLETE, 1.30, 0.74, 0.058, "#8a7d3c", "#b8a870",
                        None, dict(light="#8cab4a", base="#5f8c2a", dark="#3a5c16"), -4.0, ("bottle",), "#6c6a34",
                        freckles=True, hair=dict(color="#d4601e", front=0.08, grow=0.22), eye_y=0.040),
    "tommy_b25": _tommy("b", 25.42, "slim", 0.62, 1.04, CE.PROFILE_ATHLETE, 1.52, 0.78, 0.052, "#a08a54", "#c4b884",
           "hessian", dict(light="#bca276", base="#97805a", dark="#6a5638"), 3.0, ("pack",), "#84703c",
           moustache=True, moustache_style="kitchener25", tache_scale=1.0, hair=dict(color="#3a2a22", front=0.05, grow=0.18), brow_th=0.070, eye_y=0.020),
    "tommy_c25": _tommy("c", 25.43, "regular", 1.02, 0.90, CE.PROFILE_PEAR, 0.98, 0.70, 0.066, "#7a7a3c", "#b0a870",
                        None, dict(light="#a2ac52", base="#7e9838", dark="#566e1e"), -7.0, ("scarf", "bottle"), "#5e6030",
                        hair=dict(color="#7a4a2a", front=0.06, grow=0.20), cheeks="#e8806a", eye_y=0.010, brow="dome", brow_th=0.044),
    "tommy_d25": _tommy("d", 25.44, "regular", 0.92, 1.04, CE.PROFILE_REGULAR, 1.28, 0.76, 0.062, "#8a6c3a", "#b8a068",
                        None, dict(light="#5e9644", base="#3a7a28", dark="#1e4c12"), 8.0, ("tool", "bottle"), "#6a5430",
                        moustache=True, moustache_style="bushy", tache_scale=1.05, stubble24="#2a2220",
                        hair=dict(color="#1e1a1e", front=0.05, grow=0.18), brow_th=0.080, eye_y=0.000, cheeks="#e0806a"),
})


def _german(seed, build, tw, th, profile, leg, arm, lw, base, cover, patch, kit, hat_h, tilt, **kw):
    sh = (0.25 + 0.2 * (tw - 0.62), 0.48)
    d = _m(build=build, seed=seed, torso_w=tw, torso_h=th, profile=profile, shift_pow=1.05,
           shoulder=sh, arm=arm, hip_x=0.14 + 0.05 * (tw - 0.62), leg=leg, stance=0.06, wide=0.26, limb_w=lw,
           eye_y=0.030, brow="stroke", brow_th=0.062, mouth="dash", smirk_side=1, cheeks="#ee9078", moustache=False,
           hat="newsboy", hat_style="pickel25", hat_tilt=tilt, ear_pencil=False, hat_colors=cover, patch25=patch, hat_h=hat_h,
           hair=dict(color="#6a4a2a", front=0.06, grow=0.20),
           costume="feld25", kit25=kit, coat_len=0.08, coat_flare=0.03,
           sleeve=dict(color=base, dark=P._shade(base, 0.62), cuff=P._shade(base, 0.82), len=0.84, w=0.150 + 0.06 * (tw - 0.62)),
           shorts=dict(color=P._shade(base, 0.90), dark=P._shade(base, 0.60), cuff=P._shade(base, 0.90), len=0.90, w=0.125),
           boots=dict(color="#1e1a1c", cuff="#2c2628", h=0.26, toe=0.17),
           colors=dict(base=base, dark=P._shade(base, 0.64), collar=P._shade(base, 1.10), pipe="#ee2a20", roll="#8a8470", pants=P._shade(base, 0.90)))
    d.update(kw)
    return d


NEW_CAST25.update({
    # Germans: a slim, upturned Kaiser moustache, red patch;  b tall and lanky, round glasses, greatcoat roll, green patch;
    # c short and stout, double chin, black toothbrush moustache, plain pale cover
    "german_a25": _german(25.51, "slim", 0.66, 1.00, CE.PROFILE_ATHLETE, 1.36, 0.76, 0.054, "#527a72", dict(light="#aaa488", base="#8a8468", dark="#5e5a44"), "#ee2a20",
            ("bread",), 0.50, -3.0, moustache=True, moustache_style="kaiser25", tache_scale=1.0),
    "german_b25": _german(25.52, "slim", 0.58, 1.06, CE.PROFILE_ATHLETE, 1.58, 0.80, 0.050, "#587a74", dict(light="#b4ae90", base="#9a9478", dark="#6e6a52"), "#3a8a4a",
                          ("roll", "flask"), 0.46, 4.0, glasses=True, hair=dict(color="#c8a050", front=0.06, grow=0.20), brow_th=0.052, eye_y=0.040, cheeks="#f0a090"),
    "german_c25": _german(25.53, "stout", 1.12, 0.94, C2.PROFILE_ROUND, 0.96, 0.70, 0.068, "#466e66", dict(light="#98947a", base="#78745c", dark="#504c3a"), None,
                          ("bread", "flask"), 0.56, 6.0, moustache=True, moustache_style="brush25", tache_scale=1.0, chins=True,
                          hair=dict(color="#2a2224", front=0.05, grow=0.18), brow_th=0.082, eye_y=0.000, cheeks="#e8806a"),
    # the RFC pilot: brown leather flying helmet with goggles pushed up, a pencil moustache, a leather flying coat with a fur collar and
    # a long cream silk scarf
    "pilot25": _m(
        build="regular", seed=25.6,
        torso_w=0.80, torso_h=1.00, profile=CE.PROFILE_REGULAR, shift_pow=1.05,
        shoulder=(0.28, 0.48), arm=0.74, hip_x=0.15, leg=1.30, stance=0.06, wide=0.26, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.054, mouth="smirk", moustache=False, pencil_moustache=True, smirk_side=1, cheeks="#eca090",
        hat="newsboy", hat_style="flyhelm25", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#b0763c", base="#85502a", dark="#54301a"),
        hair=dict(color="#3a2a22", front=0.04, grow=0.16),
        costume="coat25", coat_len=0.42, coat_flare=0.12,
        sleeve=dict(color="#7a4a28", dark="#4a2a14", cuff="#4a2a14", len=0.84, w=0.170),
        shorts=dict(color="#8a7a4c", dark="#5a4e2c", cuff="#8a7a4c", len=0.90, w=0.140),
        boots=dict(color="#4a2a14", cuff="#6a4020", h=0.24, toe=0.16),
        colors=dict(base="#7a4a28", dark="#4a2a14", fur="#e6dcc0", fur_d="#b0a280", scarf="#fff8de", scarf_d="#d8c894", pants="#8a7a4c"),
    ),
})


# ============================================================================= canvases (feet-relative, D); checked by test_cast25.py canvas
CANVAS25 = {
    "general25": (-2.125, -4.8125, 2.125, 0.125),
    "engineer25": (-1.9375, -4.8125, 1.9375, 0.125),
    "worker_a25": (-2.0, -4.4375, 2.0, 0.125),
    "worker_b25": (-2.0625, -4.125, 2.0625, 0.125),
    "worker_c25": (-2.1875, -5.125, 2.1875, 0.125),
    "tommy_a25": (-1.9375, -4.625, 1.9375, 0.125),
    "tommy_b25": (-1.9375, -5.0, 1.9375, 0.125),
    "tommy_c25": (-2.0625, -4.125, 2.0625, 0.125),
    "tommy_d25": (-2.0, -4.6875, 2.0, 0.125),
    "german_a25": (-1.9375, -4.8125, 1.9375, 0.125),
    "german_b25": (-1.9375, -5.125, 1.9375, 0.125),
    "german_c25": (-2.0625, -4.1875, 2.0625, 0.125),
    "pilot25": (-1.9375, -4.625, 1.9375, 0.125),
}
CANVAS25_POSES = {
    "general25_march_flag": (-2.125, -4.8125, 2.125, 0.125),
    "engineer25_blueprint": (-1.9375, -4.8125, 1.9375, 0.125),
    "tommy_c25_ladle_tap": (-2.0625, -4.125, 2.0625, 0.125),
    "pilot25_lean_look": (-1.625, -3.125, 1.625, -0.75),
    "tommy_a25_helmet_on_stick": (-1.9375, -5.375, 1.9375, 0.125),
    "tommy_b25_helmet_on_stick": (-1.9375, -5.5, 1.9375, 0.125),
    "tommy_c25_helmet_on_stick": (-2.0625, -5.0, 2.0625, 0.125),
    "tommy_d25_helmet_on_stick": (-2.0, -5.3125, 2.0, 0.125),
    "german_a25_mg_crouch": (-2.25, -4.8125, 2.25, 0.125),
    "german_b25_mg_crouch": (-2.25, -5.125, 2.25, 0.125),
    "german_c25_mg_crouch": (-2.25, -4.1875, 2.25, 0.125),
}
SPECIAL25 = ("general25_march_flag", "engineer25_blueprint", "tommy_c25_ladle_tap", "pilot25_lean_look",
             "tommy_a25_helmet_on_stick", "tommy_b25_helmet_on_stick", "tommy_c25_helmet_on_stick", "tommy_d25_helmet_on_stick",
             "german_a25_mg_crouch", "german_b25_mg_crouch", "german_c25_mg_crouch")   # poses with their own canvas in CANVAS25_POSES
STORY25, STORY25_META = {}, {}


def _anch(c, p):
    return P.figure(c, p, "q")["anchors"]


def _feet_y(c, p):
    return P.figure(c, p, "q")["feet_y"]


def _two_hands(S, name, key="r", bend=0.5, shape="ball", layer="top", stretch=1.3, anchor="grip_far"):
    c, p = S[name]
    an = _anch(c, p)
    other = "l" if key == "r" else "r"
    gx, gy = an["%s_%s" % (anchor, key)]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _bino_to_eyes(S, name, key="r", it=5):
    c, p = S[name]
    for _ in range(it):
        an = _anch(c, p)
        bx, by = an["binoc_" + key]
        ex = (an["eye_l"][0] + an["eye_r"][0]) / 2
        ey = (an["eye_l"][1] + an["eye_r"][1]) / 2
        h = p["arm_" + key]["hand"]
        p["arm_" + key]["hand"] = (h[0] + ex - bx, h[1] + ey - by)


def _hand_on_stick(S, name, dist=0.5, bend=0.4):
    """left hand on the shaft of a held stick-like prop, dist along it from the right hand."""
    c, p = S[name]
    h = _anch(c, p)["hand_r"]
    ang = math.radians(p["prop_r"]["angle"])
    p["arm_l"] = dict(hand=(h[0] + dist * math.cos(ang), h[1] + dist * math.sin(ang)), bend=bend, stretch=1.3, layer="top")


def march_flag25(phase, facing=1, t=None):
    """the general marching behind the tank: knees high, little flag waving overhead (phase 0..1 per two steps; t: flag wave phase, default phase*2)."""
    base = dict(expr="excited", mouth=("open", 0.24, 0.17), yaw=0.60, pitch=-0.25, head_roll=-4, t=(phase * 2.0 if t is None else t),
                arm_r=dict(hand=(0.50, -0.78), bend=-0.5, stretch=1.25, layer="top"), prop_r=dict(type="flag25", angle=-82 + 6 * math.sin(2 * math.pi * phase * 2.0)))
    p = cycle("general25", phase, "march", facing=facing, base=base, arms="l")
    lg = dict(p["legs"])
    for kk in ("lift_r", "lift_l"):
        lg[kk] = min(1.5, lg.get(kk, 0.0) * 2.0)
    lg["knee_r"] = 0.9
    lg["knee_l"] = 0.9
    p["legs"] = lg
    return p


def run_away25(member, phase, facing=1, flail=1.0, hat_up=0.0):
    """a comic flee: run cycle with both arms flailing overhead and the helmet bouncing (phase 0..1; hat_up in D lifts the helmet off the head)."""
    p = cycle(member, phase, "run", facing=facing, base=dict(expr="shouting", fx=["sweat"], t=phase, hat_up25=hat_up + 0.06 * math.sin(2 * math.pi * phase * 2), yaw=0.75), arms="none")
    s = math.sin(2 * math.pi * phase)
    c = math.cos(2 * math.pi * phase)
    p["arm_r"] = dict(hand=(0.55 + 0.25 * s * flail, -0.55 - 0.18 * c * flail), bend=-0.6, stretch=1.3, shape="open", layer="top")
    p["arm_l"] = dict(hand=(-0.25 - 0.25 * s * flail, -0.40 + 0.20 * c * flail), bend=-0.6, stretch=1.3, shape="open", layer="top")
    return p


def _story():
    S, M = {}, {}
    G, E = "general25", "engineer25"
    # ---------------------------------------------------------------- the general
    sw = dict(type="swagger25", angle=62)
    S["general25_stand_smug"] = (G, dict(yaw=0.25, pitch=-0.25, expr="smug", mouth="flat", arm_r=dict(hand=(0.50, 0.90), bend=0.7, layer="front"), prop_r=dict(sw), arm_l="akimbo", legs="wide"))
    M["general25_stand_smug"] = dict(note="arrives at the trial park: chest out, swagger stick under the arm, other fist on the hip, smug")
    S["general25_walk"] = (G, cycle(G, 0.30, "walk", base=dict(expr="smug", pitch=-0.25, arm_r=dict(hand=(0.50, 0.90), bend=0.7, layer="front"), prop_r=dict(sw)), arms="l"))
    M["general25_walk"] = dict(note="one frame of cast25.cycle('general25', phase, 'walk', facing, base, arms='l'): stick stays under the right arm, the left arm swings")
    S["general25_point_stick"] = (G, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                         arm_r=dict(hand=(0.95, 0.12), bend=-0.5, stretch=1.3, layer="front"), prop_r=dict(type="swagger25", angle=-6), arm_l="akimbo", legs="wide"))
    M["general25_point_stick"] = dict(lipsync=True, note="mocking: points the swagger stick at the tank (screen-right; mirror=True for left; anchor swagger_r = the tip), other fist on the hip. "
                                                         "LIP-SYNC mouth=talk_mouth(g) inside his quotes (18.39-25.30 s, 44.37-46.40 s), 'flat' outside")
    S["general25_laugh"] = (G, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                    arm_r=dict(hand=(0.46, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.50, 0.98), bend=0.9, shape="open"), legs="wide"))
    M["general25_laugh"] = dict(note="LAUGH_BELLY: head back, hands on the belly, open laugh mouth HELD (no lip-sync). Bounce loop: alternate with general25_laugh_b every 3-4 frames "
                                     "(squash (1.02, 0.98) <-> (0.99, 1.02)), feet planted")
    S["general25_laugh_b"] = (G, dict(S["general25_laugh"][1], pitch=-0.60, head_roll=-4, lean=-3, squash=(0.99, 1.02), arm_r=dict(hand=(0.46, 0.94), bend=0.9, shape="open"),
                                      arm_l=dict(hand=(-0.50, 0.92), bend=0.9, shape="open")))
    M["general25_laugh_b"] = dict(note="second frame of the belly-laugh bounce (squash (0.99, 1.02), head up a little)")
    S["general25_march_flag"] = (G, march_flag25(0.30))
    M["general25_march_flag"] = dict(note="MARCH BEHIND: knees up, little plain flag waving overhead (prop flag25, wave driven by pose key t), left arm swinging. Animate with "
                                          "cast25.march_flag25(frame / 24.0 [, facing]) (24 frames per two steps); feet planted every frame via anchors['feet']")
    fg = (G, dict(yaw=0.35, pitch=-0.10, expr="determined", mouth="flat", arm_r=dict(hand=(0.28, 0.12), bend=-0.6, stretch=1.2, layer="top"), prop_r="binoculars", legs="wide"))
    S["general25_field_glasses"] = fg
    M["general25_field_glasses"] = dict(note="FIELD GLASSES at his eyes, both hands on them (the glasses face the viewer); anchor binoc_r = the glasses; observation post")
    S["general25_glasses_laugh"] = (G, dict(yaw=0.30, pitch=-0.60, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.3,
                                            arm_r=dict(hand=(1.00, -0.05), shape="point", bend=-0.5, stretch=1.3), arm_l=dict(hand=(-0.50, 0.95), bend=0.4), prop_l=dict(type="binoculars", scale=1.15), legs="wide"))
    M["general25_glasses_laugh"] = dict(lipsync=True, note="'See? The leaky water-tank is finished!': roaring with laughter, field glasses in the left hand, other hand pointing out at the mud. "
                                                          "LIP-SYNC 44.37-46.40 s (talk_mouth(g)); tears + head back")
    S["general25_cheer"] = (G, dict(yaw=0.15, pitch=-0.45, expr="excited", mouth=("open", 0.26, 0.18), head_roll=5, t=0.3, squash=(0.99, 1.02),
                                    arm_r=dict(hand=(0.75, -0.62), shape="open", bend=-0.6, stretch=1.3, layer="top"), arm_l=dict(hand=(-0.75, -0.55), shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide"))
    M["general25_cheer"] = dict(note="both arms up cheering at Flers; held mouth; bounce squash (0.99, 1.02) <-> (1.01, 0.99)")
    S["general25_shocked"] = (G, dict(yaw=0.30, pitch=0.10, expr="stunned", mouth=("open", 0.16, 0.20), head_dy=0.03, gaze=(0.8, 0.0), fx=["sweat"], arm_r="down", arm_l="down", legs="wide"))
    M["general25_shocked"] = dict(note="jaw dropped when the tank crosses the trench: held open mouth, sweat drop, arms hanging")
    # ---------------------------------------------------------------- the engineer (never speaks: mouth always flat/closed)
    S["engineer25_stand"] = (E, dict(yaw=0.25, expr="neutral", mouth="flat", arm_r="down", arm_l="hip", legs="stand"))
    S["engineer25_walk"] = (E, cycle(E, 0.30, "walk", base=dict(expr="neutral", mouth="flat")))
    S["engineer25_point"] = (E, dict(yaw=0.45, pitch=-0.05, expr="determined", mouth="flat", arm_r=dict(hand=(1.05, 0.30), shape="point", bend=-0.4, stretch=1.3), arm_l="hip", legs="narrow"))
    S["engineer25_blueprint"] = (E, dict(yaw=0.30, pitch=0.25, expr="determined", mouth="flat", arm_r=dict(hand=(0.55, 0.75), bend=0.2, stretch=1.2, layer="front"), prop_r="plan25", legs="narrow"))
    S["engineer25_sleeves_roll"] = (E, dict(yaw=0.20, pitch=0.55, expr="determined", mouth="flat", head_roll=-3, gaze=(0.0, 0.9),
                                            arm_l=dict(hand=(-0.55, 0.60), bend=0.4, stretch=1.0, layer="front"), arm_r=dict(hand=(-0.38, 0.72), bend=-0.2, stretch=1.1, layer="top", shape="open"), legs="stand"))
    S["engineer25_whisper"] = (E, dict(yaw=0.50, pitch=-0.05, head_roll=5, expr="smirk", mouth="flat", gaze=(0.9, 0.0),
                                       arm_r=dict(hand=(0.36, 0.30), bend=-0.7, stretch=1.0, layer="top", shape="open"), arm_l="down", legs="stand"))
    M["engineer25_stand"] = dict(note="standing, calm; one hand on the hip. He NEVER speaks: every pose has mouth 'flat'")
    M["engineer25_walk"] = dict(note="one walk frame (cast25.cycle)")
    M["engineer25_point"] = dict(note="points at the hull / the workers (screen-right; mirror=True for left)")
    M["engineer25_blueprint"] = dict(note="holds a rolled-out plan (prop plan25: blue sheet, white plain lines, a rhomboid tank profile, NO text). The left hand is on the far roll "
                                          "(anchor plan_far_r); pose key plan_w25 = sheet width (1.25). The plan hangs from the right hand to its left")
    M["engineer25_sleeves_roll"] = dict(note="rolls up his sleeve: head down on the cuff, right hand on the left forearm (sleeves are already rolled to the elbow in the drawing)")
    M["engineer25_whisper"] = dict(note="hand beside the mouth, whispering to a worker (screen-right; mouth stays closed), sideways glance")
    # ---------------------------------------------------------------- workers
    WK = ("worker_a25", "worker_b25", "worker_c25")
    arms_stand = (("hip", "down"), ("down", "akimbo"), ("akimbo", "down"))
    for i, c in enumerate(WK):
        S[c + "_stand"] = (c, dict(yaw=0.30, expr=("neutral", "smirk", "neutral")[i], mouth="flat", arm_r=arms_stand[i][0], arm_l=arms_stand[i][1], legs="stand"))
        S[c + "_walk"] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral", mouth="flat")))
        S[c + "_nod"] = (c, dict(yaw=0.30, pitch=0.30, expr="neutral", mouth="flat", head_roll=4, head_dy=0.02, arm_r=arms_stand[i][0], arm_l=arms_stand[i][1], legs="stand"))
        M[c + "_stand"] = dict(note="standing, arms relaxed (mouth flat)")
        M[c + "_walk"] = dict(note="one walk frame (cast25.cycle)")
        M[c + "_nod"] = dict(note="the DOWN key of a nod (pitch 0.30, head_roll 4): animate pitch 0 -> 0.30 -> 0 over ~10 frames")
    S["worker_a25_rivet"] = ("worker_a25", dict(yaw=0.55, pitch=-0.05, expr="determined", mouth="clench", lean=4, t=0.2,
                                                arm_r=dict(hand=(0.62, -0.38), bend=-0.7, stretch=1.2, layer="front"), prop_r=dict(type="hammer25", angle=-62, scale=1.3),
                                                arm_l=dict(hand=(0.50, 0.80), bend=0.3, layer="front"), legs="wide"))
    S["worker_a25_rivet_strike"] = ("worker_a25", dict(S["worker_a25_rivet"][1], lean=8, arm_r=dict(hand=(0.88, 0.45), bend=-0.3, stretch=1.2, layer="front"), prop_r=dict(type="hammer25", angle=10, scale=1.3)))
    M["worker_a25_rivet"] = dict(note="riveting: hammer25 raised (screen-right; mirror for left). Animate arm_r between this frame and worker_a25_rivet_strike (3 frames down, 5 up); "
                                     "anchor hammer_r = the hammer face")
    M["worker_a25_rivet_strike"] = dict(note="the strike frame of the riveting loop (hammer face on the rivet row at anchors['hammer_r'])")
    S["worker_a25_carry_bucket"] = ("worker_a25", dict(yaw=0.40, expr="neutral", mouth="flat", arm_r=dict(hand=(0.45, 0.88), bend=0.3, layer="front"), prop_r="bucket25", arm_l="hip", legs="stand"))
    M["worker_a25_carry_bucket"] = dict(note="carries a plain galvanised water bucket (bucket25, always upright, water surface visible; anchor bucket_r = the bottom); animate with cycle(base=...)")
    S["worker_b25_paint"] = ("worker_b25", dict(yaw=0.55, pitch=-0.10, expr="determined", mouth="flat", t=0.2, paint_col25="white",
                                               arm_r=dict(hand=(0.88, -0.05), bend=-0.5, stretch=1.3, layer="front"), prop_r=dict(type="paint_brush25", angle=-20),
                                               arm_l=dict(hand=(-0.50, 0.95), bend=0.3), prop_l=dict(type="paint_pot25", scale=1.3), legs="wide"))
    M["worker_b25_paint"] = dict(note="paints the stencil: long paint_brush25 (paint_col25: white / black / red / green / grey) reaching to screen-right, paint_pot25 hanging from the "
                                      "other hand. Animate the brush by moving arm_r hand (0.88, -0.05) <-> (0.88, 0.30) and angle -20 <-> 10; anchor paint_brush_r = bristles")
    S["worker_b25_carry_pot"] = ("worker_b25", dict(yaw=0.40, expr="smirk", mouth="flat", arm_r=dict(hand=(0.45, 0.80), bend=0.3), prop_r=dict(type="paint_pot25", scale=1.3), arm_l="hip", legs="stand"))
    M["worker_b25_carry_pot"] = dict(note="carries the paint pot (upright, anchor paint_pot_r = its bottom)")
    S["worker_c25_spanner"] = ("worker_c25", dict(yaw=0.55, pitch=0.10, expr="determined", mouth="clench", lean=8, t=0.2,
                                                  arm_r=dict(hand=(0.78, 0.62), bend=-0.3, stretch=1.2, layer="front"), prop_r=dict(type="spanner25", angle=-30, scale=1.4),
                                                  arm_l=dict(hand=(0.55, 0.55), bend=0.2, layer="front"), legs=dict(preset="step", stride=0.3, crouch=0.06)))
    M["worker_c25_spanner"] = dict(note="turning a big spanner on a bolt (spanner25, anchor spanner_r = the jaws); animate the angle -30 <-> -8 with a lean of 8 <-> 12")
    S["worker_c25_carry_bucket"] = ("worker_c25", dict(yaw=0.40, expr="happy", mouth="smile", arm_r=dict(hand=(0.45, 0.95), bend=0.3, layer="front"), prop_r="bucket25", arm_l="down", legs="stand"))
    M["worker_c25_carry_bucket"] = dict(note="the tall worker carries a bucket of water")
    S["worker_c25_pat_hull"] = ("worker_c25", dict(yaw=0.65, pitch=0.0, expr="grinning", mouth="smile", lean=6, arm_r=dict(hand=(1.02, 0.45), bend=-0.2, stretch=1.3, shape="open", layer="front"), arm_l="hip", legs="narrow"))
    M["worker_c25_pat_hull"] = dict(note="pats the hull with an open hand (screen-right; hand anchor hand_r is the contact point)")
    S["worker_c25_mime_drink"] = ("worker_c25", dict(yaw=0.35, pitch=-0.35, expr="happy", mouth="o", gaze=(0.0, -0.5), head_roll=-4,
                                                    arm_r=dict(hand=(0.28, 0.42), bend=-0.8, stretch=1.0, shape="ball", layer="top"), arm_l=dict(hand=(-0.45, 0.85), bend=0.5), legs="stand"))
    M["worker_c25_mime_drink"] = dict(note="mimes drinking water: fist at the mouth, head tipped back, empty hand otherwise (add prop_r='bucket25' only if the set wants a mug)")
    # ---------------------------------------------------------------- Tommies
    TM = ("tommy_a25", "tommy_b25", "tommy_c25", "tommy_d25")
    stand_arms = (("hip", "down"), ("down", "down"), ("akimbo", "akimbo"), ("down", "hip"))
    effort = ("shouting", "determined", "angry", "shouting")
    for i, c in enumerate(TM):
        S[c + "_stand"] = (c, dict(yaw=0.30, expr=("neutral", "smirk", "happy", "unimpressed")[i], mouth="flat" if i != 2 else "smile", arm_r=stand_arms[i][0], arm_l=stand_arms[i][1], legs=("stand", "narrow", "wide", "stand")[i]))
        S[c + "_walk"] = (c, cycle(c, 0.30 + 0.07 * i, "walk", base=dict(expr="neutral")))
        S[c + "_laugh_point"] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10 - 5 * i, lean=-5, t=0.4 + 0.1 * i,
                                         arm_r=dict(hand=(0.82, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.90), bend=0.9) if i % 2 == 0 else "hip", legs="wide"))
        hand_up = i in (0, 3)
        ch = dict(yaw=0.20, pitch=-0.35, expr="excited" if i % 2 else "happy", mouth=("open", 0.24, 0.18), head_roll=6 - 3 * i, t=0.3, squash=(0.99, 1.02),
                  arm_r=dict(hand=(0.72, -0.66), shape="open", bend=-0.6, stretch=1.3, layer="top"), arm_l=dict(hand=(-0.70, -0.55), shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide")
        if i in (0, 3):
            ch.update(hat_off25=1.0, prop_r="helmet25")
            ch["arm_r"] = dict(hand=(0.72, -0.60), bend=-0.6, stretch=1.3, layer="top")
        elif i == 1:
            ch.update(hat_off25=1.0, prop_l="helmet25")
            ch["arm_l"] = dict(hand=(-0.72, -0.60), bend=-0.6, stretch=1.3, layer="top")
        else:
            ch.update(hat_up25=0.40)
        S[c + "_cheer"] = (c, ch)
        S[c + "_march"] = (c, cycle(c, 0.20 + 0.09 * i, "march", base=dict(expr="happy" if i % 2 == 0 else "grinning", mouth=("open", 0.2, 0.14), yaw=0.7)))
        S[c + "_push"] = (c, dict(yaw=0.70, pitch=0.05, expr=effort[i], mouth="clench" if effort[i] != "shouting" else None, fx=["sweat"], lean=26 + 2 * i, head_roll=-4, t=0.2,
                                  arm_r=dict(hand=(1.12, 0.60), bend=-0.1, stretch=1.3, layer="front"), arm_l=dict(hand=(1.0, 0.80), bend=-0.1, stretch=1.3, layer="front"),
                                  legs=dict(preset="step", stride=0.8, crouch=0.14)))
        if S[c + "_push"][1]["mouth"] is None:
            S[c + "_push"][1].pop("mouth")
        S[c + "_duck"] = (c, dict(yaw=0.45, pitch=0.45, expr="worried", fx=["sweat"], lean=16, head_roll=6, gaze=(0.6, 0.5),
                                  arm_r=dict(hand=(0.45, -0.10), bend=-0.7, stretch=1.0, layer="top"), arm_l=dict(hand=(0.30, 0.95), bend=0.4), legs=dict(preset="stand", crouch=0.62, spread=0.1)))
        hs = ("helmet_stick25", dict(type="helmet_stick25", angle=-80 + 3 * i))
        S[c + "_helmet_on_stick"] = (c, dict(yaw=0.40, pitch=-0.15, expr="grinning", hat_off25=1.0, lean=-4, head_roll=-5 + 3 * i,
                                             arm_r=dict(hand=(0.52, -0.30), bend=-0.5, stretch=1.2, layer="top"), prop_r=dict(type="helmet_stick25", angle=-80 + 3 * i),
                                             legs=dict(preset="stand", crouch=0.28, spread=0.1)))
        M[c + "_stand"] = dict(note="standing at ease (mouth held)")
        M[c + "_walk"] = dict(note="one frame of cast25.cycle(%r, phase, 'walk')" % c)
        M[c + "_laugh_point"] = dict(note="points and laughs at the tank (screen-right; mirror=True for left); bounce 0.04 D at the hips, feet planted")
        M[c + "_cheer"] = dict(note="arms up cheering; " + ("helmet held up in the hand (hat_off25=1 + prop helmet25)" if i != 2 else "both arms up and the helmet floats above the head (hat_up25 0.40)") + "; bounce squash (0.99, 1.02) <-> (1.01, 0.99)")
        M[c + "_march"] = dict(note="one frame of cast25.cycle(%r, phase, 'march') (24 frames per two steps), facing the tank's tail" % c)
        M[c + "_push"] = dict(note="pushing the stuck tank: leaning 26+ degrees, both hands on it at screen-right (hands at (1.12, 0.60) / (1.0, 0.80); move them with the card), strain face + sweat. Feet planted; animate lean +-3")
        M[c + "_duck"] = dict(note="crouched behind the parapet, hand pressing the helmet, worried. feet_y is the soles (crouch lowers the figure); the stage parapet should cover everything below the eyes")
        M[c + "_helmet_on_stick"] = dict(note="helmet-on-a-stick trick: the soldier is crouched (head bare) and holds the stick (prop helmet_stick25, 2 D long, helmet at the top; anchor helmet_stick_r = the "
                                              "helmet top) up over the parapet; set hat_off25=1 stays. Raise/wiggle by animating arm_r hand y -0.30 <-> -0.55 and the angle -80 <-> -88")
    S["tommy_c25_ladle_tap"] = ("tommy_c25", dict(yaw=0.50, pitch=-0.10, expr="laughing", fx=["tears"], head_roll=6, t=0.3,
                                                  arm_r=dict(hand=(0.80, 0.30), bend=-0.3, stretch=1.3, layer="front"), prop_r=dict(type="ladle25", angle=-10), arm_l=dict(hand=(-0.30, 0.95), bend=0.9), legs="wide"))
    M["tommy_c25_ladle_tap"] = dict(note="taps the tank with a ladle like a bucket: ladle25 (anchor ladle_r = the cup); animate the angle -10 <-> -28 each 4 frames")
    # ---------------------------------------------------------------- Germans
    GR = ("german_a25", "german_b25", "german_c25")
    for i, c in enumerate(GR):
        S[c + "_stand"] = (c, dict(yaw=0.30, expr=("neutral", "unimpressed", "smug")[i], mouth="flat", arm_r=("down", "hip", "akimbo")[i], arm_l=("down", "down", "akimbo")[i], legs=("stand", "narrow", "wide")[i]))
        S[c + "_walk"] = (c, cycle(c, 0.30 + 0.1 * i, "walk", base=dict(expr="neutral")))
        S[c + "_run_away"] = (c, run_away25(c, 0.25 + 0.12 * i, 1, flail=1.0 - 0.1 * i, hat_up=(0.0, 0.18, 0.0)[i]))
        S[c + "_surprised"] = (c, dict(yaw=0.20, pitch=-0.10, expr="shocked", fx=["sweat"], head_roll=-4 + 4 * i, hat_up25=(0.0, 0.0, 0.14)[i], squash=(0.98, 1.03),
                                       arm_r=dict(hand=(0.80, -0.20), shape="open", bend=-0.4, stretch=1.2, layer="front"), arm_l=dict(hand=(-0.70, 0.05 + 0.1 * i), shape="open", bend=-0.4, stretch=1.2, layer="front"),
                                       legs=dict(preset="step", stride=-0.55, lift_l=0.15)))
        mg = dict(yaw=0.55, pitch=0.0, expr="shouting" if i != 1 else "determined", lean=12, t=0.2,
                  legs=dict(preset="stand", crouch=0.42, spread=0.12))
        gy = _feet_y(c, mg)
        mg["mg_gy25"] = gy
        mg["arm_r"] = dict(hand=(0.78, gy - 0.80), bend=0.1, stretch=1.3, layer="front")
        mg["prop_r"] = dict(type="mg25", angle=0)
        mg["arm_l"] = dict(hand=(0.66, gy - 0.80), bend=0.2, stretch=1.3, layer="front")
        S[c + "_mg_crouch"] = (c, mg)
        M[c + "_stand"] = dict(note="standing, mouth held")
        M[c + "_walk"] = dict(note="one walk frame (cast25.cycle)")
        M[c + "_run_away"] = dict(note="comic flee: run cycle, arms flailing, helmet bouncing; animate with cast25.run_away25(%r, frame / 16.0, facing [, flail, hat_up]) (16 frames per cycle). "
                                       "The head turns toward the viewer; mirror via facing=-1" % c)
        M[c + "_surprised"] = dict(note="startled: both hands up with open fingers, sweat, a step back (hat_up25 lifts the helmet off the head for a double-take)")
        M[c + "_mg_crouch"] = dict(note="crouched behind a Maxim machine gun (prop mg25 on its sledge: sledge skids on the ground line thanks to mg_gy25; both hands on the spade grips); "
                                        "gun points to screen-right; mirror=True for left; shouting")
    # ---------------------------------------------------------------- pilot
    Pl = "pilot25"
    S["pilot25_stand"] = (Pl, dict(yaw=0.30, expr="smug", mouth="smirk", arm_r="hip", arm_l="down", legs="stand"))
    S["pilot25_walk"] = (Pl, cycle(Pl, 0.30, "walk", base=dict(expr="smug", mouth="smirk")))
    S["pilot25_lean_look"] = (Pl, dict(yaw=0.80, pitch=0.60, expr="excited", mouth="talk_a", gaze=(0.8, 0.9), lean=38, head_roll=12, head_dx=-0.05,
                                       arm_r=dict(hand=(0.95, 1.40), shape="point", bend=-0.2, stretch=1.35, layer="front"), arm_l=dict(hand=(0.30, 1.00), bend=0.2, layer="front"), legs=dict(preset="stand", crouch=0.2)))
    M["pilot25_stand"] = dict(note="standing on the airfield")
    M["pilot25_walk"] = dict(note="one walk frame (cast25.cycle)")
    M["pilot25_lean_look"] = dict(note="COCKPIT: leaning out over the cockpit rim pointing down at the tank (screen-right; mirror=True for left). Upper body only is meant to show: crop the sprite "
                                       "at the cockpit rim (CANVAS25_POSES['pilot25_lean_look'] ends just below the belt); the legs are inside the aircraft. Goggles are pushed up on the helmet")
    for n in list(S):
        if n.endswith("_walk"):
            M.setdefault(n, dict(note="one frame of cast25.cycle()"))
    # field glasses: the glasses go on the eyes, the second hand on the other barrel
    _two_hands(S, "general25_field_glasses", bend=-0.4, layer="top", stretch=1.2)
    _bino_to_eyes(S, "general25_field_glasses")
    _two_hands(S, "general25_field_glasses", bend=-0.4, layer="top", stretch=1.2)
    _two_hands(S, "engineer25_blueprint", key="r", bend=0.2, layer="front", stretch=1.3, anchor="plan_far")
    for c in TM:
        _hand_on_stick(S, c + "_helmet_on_stick", dist=0.55)
    return S, M


def register():
    if getattr(P, "_cast25_registered", False):
        CE.register_stage()
        if not STORY25:
            sd, md = _story()
            STORY25.update(sd)
            STORY25_META.update(md)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_ink_limb"):
        _O25[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    CE.COSTUMES.update(COSTUMES25)
    CE.HATS.update(HATS25)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS25 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP25)
    for n, c in NEW_CAST25.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS25)
    P._cast25_registered = True
    sd, md = _story()
    STORY25.update(sd)
    STORY25_META.update(md)
    P.STORY.update(STORY25)
    CE.register_stage()


register()
