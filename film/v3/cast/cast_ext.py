#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast_ext.py -- six more cast members for the v2 puppet system (read-only: v2/puppet/puppet.py is never edited).

    import sys; sys.path.insert(0, ".../v3/cast"); import cast_ext      # registers on import (idempotent)
    import puppet                                                       # the same module object cast_ext extended
    f = puppet.figure("senior_a", {"yaw": 0.5, "expr": "smug"}, "sa")

New names in puppet.CAST:  senior_a, senior_b, clerk, beach_man, beach_woman, beach_kid
New prop types:            bucket, newspaper, forecast, mug      (puppet.PROP_TYPES / PROP_TIP extended)
New arm preset:            "shade" (hand shading the eyes, for every build); new builds "regular" and "child"
Stage:                     sprites.DEFAULT_CANVAS gets an entry per new member, whatever the import order.

How it plugs in.  puppet.figure() looks its helpers up as module globals at call time, so this module wraps a few of them
(each wrapper falls through to the original for hero and boss, whose drawings stay bit-identical):
    _torso        new costumes (and a skirt drawn over the torso bottom)       dispatch on CAST[name]["costume"]
    _hat_newsboy  new hats (fedora, bowler, eyeshade, boater, sunhat, sailor)   dispatch on CAST[name]["hat_style"]
                  (every new member has hat="newsboy" as the dispatch slot; the real hat is hat_style)
    _face         glasses, pencil moustache, lashes, freckles, cheeks drawn over the face
    _moustache    walrus moustache (moustache_style="walrus")
    _hair         hair styles "cap" (hair over the crown above an eyeshade) and "curl" (fringe lock)
    _ink_limb     sleeve garters on the upper arms (garters=True)
    _prop         the new props
    _norm         remembers the cast being drawn (for the two hooks above that do not receive it)

Command line:
    python3 cast_ext.py sheet     sheet.svg + sheet.png (every new member: 3 views, 4 expressions, 3 poses)
    python3 cast_ext.py lineup    lineup.png (all eight members, same scale, office wall and sand, head 110 and 220 px)
    python3 cast_ext.py test      robustness (v2 test_puppet.py run on the new names) + determinism
See API.md next to this file.
"""
import importlib
import importlib.abc
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
V2P = os.path.join(PROJ, "v2", "puppet")
if V2P not in sys.path:
    sys.path.insert(0, V2P)
import puppet as P  # noqa: E402  (v2, read-only)

NEW = ("senior_a", "senior_b", "clerk", "beach_man", "beach_woman", "beach_kid")
TMP = os.path.join(PROJ, "v3", "tmp", "cast")

_clamp, _lerp, _smooth, _rot = P._clamp, P._lerp, P._smooth, P._rot
_poly, _poly_d = P._poly, P._poly_d
TT = P.TORSO_TOP
SKIN = P.HEAD_FILL           # bare skin (neck opening, arm holes) = the head's white

# ============================================================================= state shared by the hooks
_CUR = [None]                # cast dict being drawn (set by the _norm wrapper; figure() calls _norm first)
_O = {}                      # originals


# ============================================================================= helpers
def _X(m):
    def X(x, y):
        return (m.x(x, y), y)
    return X


def _ln(pts, col, w, extra=""):
    return '<path d="M%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"%s/>' % (
        " L".join("%.4f,%.4f" % p for p in pts), col, w, extra)


def _circ(c, r, fill, k, sw=0.013):
    return '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (c[0], c[1], r, fill, k.ink, sw)


def _bowl(k, col, yb, yB, sw=0.022, dip=0.03):
    return ('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f L-0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="%.4f"/>'
            % (yb, yb + dip, yb, yB + 0.1, yB + 0.1, k.c(col), k.ink, sw))


# ============================================================================= costumes (torso-local, inside the torso clip)
def _cos_tweed(k, C, m):
    """senior_a: brown herringbone-tweed waistcoat, single-breasted with four horn buttons, pale-blue shirt and pointed collar,
    navy tie with mustard bars, chest welt pocket with a fountain pen, two flapped lower pockets, grey flannel trousers."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_hb" width="0.070" height="0.036" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<path d="M0,0.036 L0.035,0 L0.070,0.036" fill="none" stroke="%s" stroke-width="0.0085"/></pattern>'
                  % (u, m.c, k.c(col["fleck"])))
    o = ['<rect x="-0.7" y="0.3" width="1.4" height="1.3" fill="url(#%s_hb)" opacity="0.55"/>' % u]
    vt, vb, vw = 0.43, 0.76, 0.135
    # lower flapped pockets
    for s in (-1, 1):
        x = s * 0.205
        o.append(_poly(k, [X(x - 0.095, 1.035), X(x + 0.095, 1.035), X(x + 0.095, 1.120), X(x - 0.095, 1.120)], k.c(col["pocket"]), 0.012))
        o.append(_poly(k, [X(x - 0.100, 1.025), X(x + 0.100, 1.025), X(x + 0.092, 1.075), X(x - 0.092, 1.075)], k.c(col["dark"]), 0.013))
    # chest welt pocket (screen-left) with a fountain pen
    px = -0.215
    o.append(_poly(k, [X(px - 0.020, 0.600), X(px + 0.012, 0.600), X(px + 0.012, 0.712), X(px - 0.020, 0.712)], k.c(col["pen"]), 0.011))
    o.append(_ln([X(px + 0.004, 0.615), X(px + 0.004, 0.690)], k.c(col["pen_clip"]), 0.010))
    o.append(_poly(k, [X(px - 0.085, 0.700), X(px + 0.080, 0.700), X(px + 0.080, 0.735), X(px - 0.085, 0.735)], k.c(col["dark"]), 0.013))
    # front edge (centre line) from the V down to the hem
    o.append(_ln([X(0.0, vb), X(0.0, yb + 0.01)], k.c(col["dark"]), 0.016))
    # shirt V, pointed collar, tie
    o.append(_poly(k, [X(-vw, vt), X(vw, vt), X(0, vb)], k.c(col["shirt"]), 0.016))
    o.append(_poly(k, [X(-0.026, 0.535), X(0.026, 0.535), X(0.036, 0.640), X(0.0, vb - 0.005), X(-0.036, 0.640)], k.c(col["tie"]), 0.013))
    for y in (0.585, 0.655):
        o.append(_ln([X(-0.030, y), X(0.030, y + 0.022)], k.c(col["tie_stripe"]), 0.011))
    o.append(_poly(k, [X(-0.030, 0.500), X(0.030, 0.500), X(0.024, 0.545), X(-0.024, 0.545)], k.c(col["tie_dark"]), 0.011))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.125, 0.430), X(s * 0.020, 0.505), X(s * 0.105, 0.585)], k.c(col["collar"]), 0.013))
    # four horn buttons on the centre line
    for y in (0.815, 0.920, 1.025, 1.130):
        o.append(_circ(X(0.0, y), 0.031, k.c(col["button"]), k, 0.014))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.009" fill="%s"/>' % (m.x(0.0, y) - 0.008, y - 0.009, k.c(col["button_l"])))
    o.append(_bowl(k, col["pants"], yb, yB))
    return "".join(o)


def _cos_cardigan(k, C, m):
    """senior_b: burgundy rib-knit cardigan with a shawl collar and button band, three leather buttons, two patch pockets
    (a briar pipe in the screen-right one), ribbed hem, white shirt, navy knit tie, charcoal trousers."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_rb" width="0.052" height="0.4" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0.020" y="0" width="0.011" height="0.4" fill="%s"/></pattern>' % (u, m.c, k.c(col["rib"])))
    o = ['<rect x="-0.75" y="0.3" width="1.5" height="1.3" fill="url(#%s_rb)" opacity="0.45"/>' % u]
    vt, vb, vw = 0.42, 0.81, 0.150
    # patch pockets with ribbed tops, briar pipe in the right one
    for s in (-1, 1):
        x = s * 0.300
        o.append(_poly(k, [X(x - 0.100, 0.935), X(x + 0.100, 0.935), X(x + 0.095, 1.090), X(x - 0.095, 1.090)], k.c(col["pocket"]), 0.013))
        o.append(_poly(k, [X(x - 0.100, 0.935), X(x + 0.100, 0.935), X(x + 0.100, 0.968), X(x - 0.100, 0.968)], k.c(col["band"]), 0.012))
    bx, by = m.x(0.315, 0.900), 0.900
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>'
             % (bx - 0.005, by + 0.03, bx - 0.05, by - 0.005, bx - 0.095, by - 0.060, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
             % (bx - 0.005, by + 0.03, bx - 0.05, by - 0.005, bx - 0.095, by - 0.060, k.c(col["stem"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
             % (bx - 0.020, by - 0.020, bx + 0.042, by - 0.024, bx + 0.046, by + 0.050, bx + 0.010, by + 0.055, bx - 0.022, by + 0.040,
                k.c(col["pipe"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.029" ry="0.008" fill="%s"/>' % (bx + 0.011, by - 0.020, k.c("#2a1c18")))
    # ribbed hem band
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f L-0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013"/>'
             % (yb - 0.085, yb - 0.065, yb - 0.085, yb + 0.03, yb + 0.03, k.c(col["band"]), k.ink))
    dd = "".join("M%.4f,%.4f L%.4f,%.4f" % (X(x, yb - 0.066) + X(x, yb + 0.01)) for x in [i * 0.06 - 0.48 for i in range(17)])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" opacity="0.8"/>' % (dd, k.c(col["dark"])))
    # button band below the V
    o.append(_poly(k, [X(-0.060, vb - 0.02), X(0.060, vb - 0.02), X(0.060, yb - 0.075), X(-0.060, yb - 0.075)], k.c(col["band"]), 0.013))
    o.append(_ln([X(0.0, vb + 0.03), X(0.0, yb - 0.08)], k.c(col["dark"]), 0.009))
    # shirt V, collar points, navy knit tie
    o.append(_poly(k, [X(-vw, vt), X(vw, vt), X(0, vb)], k.c(col["shirt"]), 0.016))
    o.append(_poly(k, [X(-0.026, 0.530), X(0.026, 0.530), X(0.032, vb - 0.04), X(0.0, vb - 0.005), X(-0.032, vb - 0.04)], k.c(col["tie"]), 0.013))
    o.append(_poly(k, [X(-0.030, 0.495), X(0.030, 0.495), X(0.024, 0.540), X(-0.024, 0.540)], k.c(col["tie_dark"]), 0.011))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.140, 0.425), X(s * 0.020, 0.495), X(s * 0.112, 0.570)], k.c(col["shirt"]), 0.013))
    # shawl collar: a wide ribbed band along both edges of the V
    for s in (-1, 1):
        o.append(_poly(k, [X(s * vw, vt - 0.02), X(s * (vw + 0.095), vt - 0.02), X(s * 0.075, vb + 0.035), X(s * 0.006, vb + 0.0)],
                       k.c(col["band"]), 0.014))
        o.append(_ln([X(s * (vw + 0.048), vt), X(s * 0.040, vb + 0.0)], k.c(col["dark"]), 0.008, ' opacity="0.8"'))
    # three leather buttons
    for y in (0.880, 0.975, 1.070):
        o.append(_circ(X(0.0, y), 0.036, k.c(col["button"]), k, 0.014))
        c = X(0.0, y)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" fill="none"/>'
                 % (c[0] - 0.016, c[1] - 0.016, c[0] + 0.016, c[1] + 0.016, c[0] + 0.016, c[1] - 0.016, c[0] - 0.016, c[1] + 0.016,
                    k.c(col["button_l"])))
    o.append(_bowl(k, col["pants"], yb + 0.03, yB, dip=0.02))
    return "".join(o)


def _cos_clerk(k, C, m):
    """clerk: blue-pinstriped shirt, white pointed collar, burnt-orange tie with a brass clip, chest pocket with two pencils,
    pearl buttons, brown belt with a brass buckle, grey trousers (sleeve garters are drawn on the arms)."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_ps" width="0.062" height="0.4" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0.026" y="0" width="0.010" height="0.4" fill="%s"/></pattern>' % (u, m.c, k.c(col["stripe"])))
    o = ['<rect x="-0.7" y="0.3" width="1.4" height="1.3" fill="url(#%s_ps)" opacity="0.75"/>' % u]
    # placket and pearl buttons
    o.append(_ln([X(0.0, 0.84), X(0.0, yb - 0.06)], k.c(col["dark"]), 0.010))
    for y in (0.930, 1.040):
        o.append(_circ(X(0.0, y), 0.018, k.c(col["button"]), k, 0.010))
    # chest pocket (screen-left) with two pencils
    px = -0.150
    for dx, c, h in ((-0.030, "pencil1", 0.650), (0.012, "pencil2", 0.672)):
        x = px + dx
        o.append(_poly(k, [X(x - 0.013, h + 0.03), X(x, h), X(x + 0.013, h + 0.03), X(x + 0.013, 0.78), X(x - 0.013, 0.78)], k.c(col[c]), 0.009))
    o.append(_poly(k, [X(px - 0.075, 0.735), X(px + 0.070, 0.735), X(px + 0.066, 0.860), X(px - 0.071, 0.860)], k.c(col["pocket"]), 0.012))
    o.append(_ln([X(px - 0.075, 0.760), X(px + 0.070, 0.760)], k.c(col["dark"]), 0.008))
    # tie, brass clip, collar
    o.append(_poly(k, [X(-0.024, 0.545), X(0.024, 0.545), X(0.034, 0.80), X(0.0, 0.850), X(-0.034, 0.80)], k.c(col["tie"]), 0.013))
    o.append(_ln([X(-0.006, 0.57), X(-0.010, 0.79)], k.c(col["tie_dark"]), 0.009, ' opacity="0.7"'))
    o.append(_poly(k, [X(-0.052, 0.690), X(0.052, 0.690), X(0.052, 0.708), X(-0.052, 0.708)], k.c(col["clip"]), 0.008))
    o.append(_poly(k, [X(-0.028, 0.505), X(0.028, 0.505), X(0.022, 0.552), X(-0.022, 0.552)], k.c(col["tie_dark"]), 0.011))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.120, 0.420), X(s * 0.018, 0.508), X(s * 0.110, 0.600)], k.c(col["collar"]), 0.014))
    # belt + buckle, trousers
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f Q0,%.4f -0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013"/>'
             % (yb - 0.055, yb - 0.025, yb - 0.055, yb + 0.005, yb + 0.035, yb + 0.005, k.c(col["belt"]), k.ink))
    c = X(0.0, yb - 0.008)
    o.append('<rect x="%.4f" y="%.4f" width="0.074" height="0.060" rx="0.010" fill="none" stroke="%s" stroke-width="0.016"/>'
             % (c[0] - 0.037, c[1] - 0.030, k.c(col["buckle"])))
    o.append('<rect x="%.4f" y="%.4f" width="0.090" height="0.076" rx="0.014" fill="none" stroke="%s" stroke-width="0.007"/>'
             % (c[0] - 0.045, c[1] - 0.038, k.ink))
    return "".join(o)


def _cos_bathing(k, C, m):
    """beach_man: 1930s one-piece bathing suit: navy with cream hoops, scoop neck and deep arm holes (bare skin = head white),
    red club badge with a white anchor, white canvas belt with a brass buckle, navy trunks."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    o = []
    for y in (0.62, 0.73, 0.84, 0.95, 1.06):
        o.append('<path d="M-0.75,%.4f Q%.4f,%.4f 0.75,%.4f L0.75,%.4f Q%.4f,%.4f -0.75,%.4f Z" fill="%s"/>'
                 % (y, m.x(0, y), y + 0.035, y, y + 0.052, m.x(0, y), y + 0.087, y + 0.052, k.c(col["stripe"])))
    skin = k.c(SKIN)
    for s in (-1, 1):            # arm holes
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (X(s * 0.205, 0.30) + X(s * 0.205, 0.40) + X(s * 0.215, 0.60) + X(s * 0.33, 0.655) + X(s * 0.40, 0.66)
                    + X(s * 0.52, 0.645) + X(s * 0.60, 0.30) + (skin, k.ink)))
    # scoop neck
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (X(-0.150, 0.30) + X(-0.140, 0.43) + X(-0.120, 0.580) + X(0.0, 0.585) + X(0.120, 0.580) + X(0.140, 0.43) + X(0.150, 0.30) + (skin, k.ink)))
    # club badge with an anchor
    c = X(-0.150, 0.740)
    o.append(_circ(c, 0.052, k.c(col["badge"]), k, 0.013))
    w = k.c(col["stripe"])
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
             % (c[0], c[1] - 0.030, c[0], c[1] + 0.030, c[0] - 0.016, c[1] - 0.016, c[0] + 0.016, c[1] - 0.016,
                c[0] - 0.026, c[1] + 0.008, c[0] - 0.022, c[1] + 0.034, c[0], c[1] + 0.032, c[0] + 0.022, c[1] + 0.034, c[0] + 0.026, c[1] + 0.008, w))
    # trunks, belt, buckle
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f Q0,%.4f -0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013"/>'
             % (yb - 0.060, yb - 0.030, yb - 0.060, yb + 0.002, yb + 0.032, yb + 0.002, k.c(col["belt"]), k.ink))
    c = X(0.0, yb - 0.012)
    o.append('<rect x="%.4f" y="%.4f" width="0.070" height="0.058" rx="0.008" fill="%s" stroke="%s" stroke-width="0.012"/>'
             % (c[0] - 0.035, c[1] - 0.029, k.c(col["buckle"]), k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="0.030" height="0.022" fill="%s"/>' % (c[0] - 0.015, c[1] - 0.011, k.c(col["belt"])))
    return "".join(o)


def _cos_dress(k, C, m):
    """beach_woman: coral polka-dot summer dress: white Peter Pan collar, three white buttons, navy sash with a side bow,
    flared skirt (drawn OVER the torso bottom and the hips) with a white hem trim and two folds."""
    X = _X(m)
    col = C["colors"]
    u = k.uid
    yw = C.get("waist_y", 0.97)
    hem = TT + C["torso_h"] + C.get("skirt_len", 0.55)
    k.defs.append('<pattern id="%s_pd" width="0.120" height="0.120" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<circle cx="0.030" cy="0.030" r="0.020" fill="%s"/><circle cx="0.090" cy="0.090" r="0.020" fill="%s"/></pattern>'
                  % (u, m.c, k.c(col["dot"]), k.c(col["dot"])))
    inside = ['<rect x="-0.7" y="0.3" width="1.4" height="1.3" fill="url(#%s_pd)"/>' % u]
    for y in (0.680, 0.770, 0.860):
        inside.append(_circ(X(0.0, y), 0.020, k.c(col["button"]), k, 0.010))
    for s in (-1, 1):            # Peter Pan collar: two round flaps meeting at the centre
        inside.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                      % (X(s * 0.008, 0.470) + X(s * 0.030, 0.640) + X(s * 0.150, 0.590) + X(s * 0.255, 0.540) + X(s * 0.180, 0.440) + (k.c(col["collar"]), k.ink)))
    # skirt (over): A-line from the sash to the hem, the torso's own lower end and the hips are under it
    a = 0.235
    b = C.get("skirt_w", 0.50)
    sk = [X(-a, yw - 0.02), X(a, yw - 0.02), X(b * 0.62, yw + 0.30), X(b, hem - 0.02), X(b * 0.50, hem + 0.025), X(0.0, hem),
          X(-b * 0.50, hem + 0.025), X(-b, hem - 0.02), X(-b * 0.62, yw + 0.30)]
    d = ("M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (sk[0] + sk[1] + sk[2] + sk[3] + (sk[3][0] * 0.75 + sk[5][0] * 0.25, hem + 0.040) + sk[5]
            + (sk[7][0] * 0.75 + sk[5][0] * 0.25, hem + 0.040) + sk[7] + sk[8] + sk[0]))
    hw = m.hwa
    k.defs.append('<clipPath id="%s_sk"><path d="%s"/></clipPath>' % (u, d))
    over = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (d, k.ink, k.ink),
            '<g clip-path="url(#%s_sk)"><rect x="-0.9" y="0.5" width="1.8" height="2.0" fill="url(#%s_tg)"/>'
            '<rect x="-0.9" y="0.5" width="1.8" height="2.0" fill="url(#%s_pd)"/>' % (u, u, u)]
    # folds and white hem trim
    for s in (-1, 1):
        over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
                    % (X(s * 0.10, yw + 0.10) + X(s * 0.15, yw + 0.40) + X(s * 0.24, hem - 0.05) + (k.c(col["dark"]),)))
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.046"/>'
                % (X(-b - 0.05, hem - 0.075) + X(-b * 0.5, hem - 0.03) + X(0.0, hem - 0.050) + X(b * 0.5, hem - 0.03) + X(b + 0.05, hem - 0.075) + (k.c(col["trim"]),)))
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010"/>'
                % (X(-b - 0.05, hem - 0.100) + X(-b * 0.5, hem - 0.055) + X(0.0, hem - 0.075) + X(b * 0.5, hem - 0.055) + X(b + 0.05, hem - 0.100) + (k.ink,)))
    over.append('</g>')
    # sash with a bow at the screen-right hip
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                % (X(-a - 0.012, yw - 0.075) + X(0.0, yw - 0.055) + X(a + 0.012, yw - 0.075) + X(a + 0.012, yw - 0.010) + X(0.0, yw + 0.010)
                   + X(-a - 0.012, yw - 0.010) + (k.c(col["sash"]), k.ink)))
    bx, by = X(0.150, yw - 0.040)
    for s in (-1, 1):
        over.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                    % (bx, by, bx + s * 0.075, by - 0.045, bx + s * 0.075, by + 0.040, k.c(col["sash"]), k.ink))
    for s in (-1, 1):
        over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
                    % (bx, by + 0.01, bx + s * 0.03, by + 0.08, bx + s * 0.02 + 0.01, by + 0.165, bx + s * 0.05 + 0.01, by + 0.150,
                       bx + s * 0.045, by + 0.07, bx + s * 0.012, by + 0.01, k.c(col["sash_dark"]), k.ink))
    over.append(_circ((bx, by), 0.024, k.c(col["sash_dark"]), k, 0.011))
    for p in (sk[3], sk[7], (sk[5][0], hem + 0.03)):
        k.ext.append((p[0], p[1], 0.04))
    return "".join(inside), "", "".join(over)


def _cos_sailor(k, C, m):
    """beach_kid: white middy blouse, navy sailor collar with two white stripes, red neckerchief knot and tails, gold star,
    navy waistband, navy shorts with a two-button front flap."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.12
    nv = k.c(col["navy"])
    o = []
    # waistband + shorts with a button flap
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f L-0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022"/>'
             % (yb - 0.04, yb - 0.015, yb - 0.04, yB + 0.1, yB + 0.1, nv, k.ink))
    o.append(_ln([X(-0.10, yb + 0.005), X(-0.08, yB + 0.05)], k.c(col["navy_l"]), 0.010))
    o.append(_ln([X(0.10, yb + 0.005), X(0.08, yB + 0.05)], k.c(col["navy_l"]), 0.010))
    for s in (-1, 1):
        o.append(_circ(X(s * 0.080, yb + 0.030), 0.017, k.c(col["button"]), k, 0.008))
    # gold star on the chest (screen-left)
    c = X(-0.130, 0.800)
    pts = []
    for i in range(10):
        r = 0.040 if i % 2 == 0 else 0.017
        a = math.radians(-90 + 36 * i)
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    o.append(_poly(k, pts, k.c(col["star"]), 0.009))
    # sailor collar: navy bib with two white stripes, white dickey in the V
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.30, 0.30), X(s * 0.30, 0.47), X(s * 0.012, 0.735), X(s * 0.010, 0.60), X(s * 0.105, 0.36), X(s * 0.105, 0.30)], nv, 0.014))
        for off in (0.030, 0.058):
            o.append(_ln([X(s * (0.30 - off), 0.43 + off * 0.2), X(s * (0.012 + off * 0.4), 0.735 - off * 1.25)], k.c(col["base"]), 0.011))
    o.append(_poly(k, [X(-0.105, 0.36), X(0.105, 0.36), X(0.0, 0.60)], k.c(col["base"]), 0.012))
    # neckerchief knot and tails
    c = X(0.0, 0.690)
    for s in (-1, 1):
        o.append(_poly(k, [(c[0] + s * 0.010, c[1]), (c[0] + s * 0.060, c[1] + 0.145), (c[0] + s * 0.020, c[1] + 0.125), (c[0] + s * 0.004, c[1] + 0.150)],
                       k.c(col["kerchief"]), 0.012))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.032" fill="%s" stroke="%s" stroke-width="0.013"/>' % (c[0], c[1], k.c(col["kerchief_d"]), k.ink))
    return "".join(o)


COSTUMES = {"tweed": _cos_tweed, "cardigan": _cos_cardigan, "clerk_shirt": _cos_clerk, "bathing": _cos_bathing,
            "dress": _cos_dress, "sailor": _cos_sailor}


def _torso(k, C, m):
    """costume dispatch; the outline, clip and gradient are those of puppet._torso."""
    fn = COSTUMES.get(C.get("costume"))
    if fn is None:
        return _O["_torso"](k, C, m)
    G = P._torso_geom(C["torso_w"], C["torso_h"], C["profile"], C["seed"])
    nf = m.nf
    outer = P._smooth_closed([(g[0] * nf + g[2] * g[5], g[1] + g[3] * g[5]) for g in G])
    inner = P._smooth_closed([(g[0] * nf - g[2] * (g[4] + g[6]), g[1] - g[3] * (g[4] + g[6])) for g in G])
    u = k.uid
    base = C["colors"]["base"]
    hw = m.hwa
    k.defs.append('<linearGradient id="%s_tg" gradientUnits="userSpaceOnUse" x1="%.4f" y1="0" x2="%.4f" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  '<clipPath id="%s_tc"><path d="%s"/></clipPath>'
                  % (u, -hw, hw, k.c(P._shade(base, 1.12)), k.c(base), k.c(P._shade(base, 0.72)), u, inner))
    r = fn(k, C, m)
    inside, behind, over = r if isinstance(r, tuple) else (r, "", "")
    return ('%s<path d="%s" fill="%s"/><g clip-path="url(#%s_tc)"><rect x="-0.75" y="0.2" width="1.5" height="1.5" fill="url(#%s_tg)"/>%s</g>%s'
            % (behind, outer, k.ink, u, u, inside, over))


# ============================================================================= hats (head frame, drawn over the head)
def _gradient(k, name, col, x0=-0.45, x1=0.45, mid=0.32):
    u = k.uid
    k.defs.append('<linearGradient id="%s_%s" gradientUnits="userSpaceOnUse" x1="%.3f" y1="0" x2="%.3f" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="%.2f" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, name, x0, x1, k.c(col["light"]), mid, k.c(col["base"]), k.c(col["dark"])))
    return "url(#%s_%s)" % (u, name)


def _ext(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_fedora(k, C, yaw):
    """senior_a: camel felt fedora: tapered crown with a centre crease and a pinched front, dark band with a side knot,
    snap brim 1.24 D wide that stays flat at the tips (no curl) and dips over the brows in front."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = -0.09 * yaw + dx
    fdx = 0.20 * yaw
    g = _gradient(k, "ht", col, mid=0.30)
    crown = ("M%.4f,-0.36 C%.4f,-0.50 %.4f,-0.615 %.4f,-0.665 Q%.4f,-0.725 %.4f,-0.690 Q%.4f,-0.655 %.4f,-0.690 Q%.4f,-0.725 %.4f,-0.665 "
             "C%.4f,-0.615 %.4f,-0.50 %.4f,-0.36 Z"
             % (-0.405 + dx, -0.415 + dx, -0.370 + dx, -0.315 + dx, -0.20 + dx, cx - 0.06, cx, cx + 0.06, 0.20 + dx, 0.315 + dx,
                0.370 + dx, 0.415 + dx, 0.405 + dx))
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="%s"/>' % (crown, g))
    # centre crease and the two front pinches
    o.append('<path d="M%.4f,-0.672 Q%.4f,-0.610 %.4f,-0.560" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
             % (cx, cx + 0.010, cx - 0.004, k.c(col["dark"])))
    for s in (-1, 1):
        o.append('<path d="M%.4f,-0.655 Q%.4f,-0.585 %.4f,-0.505" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.75"/>'
                 % (cx + s * 0.165, cx + s * 0.125, cx + s * 0.140, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.520 Q%.4f,-0.630 %.4f,-0.665" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>'
             % (-0.335 + dx, -0.315 + dx, -0.250 + dx, k.c(col["shine"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (crown, k.ink))
    # band with a small knot on the screen-left
    o.append('<path d="M%.4f,-0.455 Q%.4f,-0.430 %.4f,-0.455 L%.4f,-0.360 L%.4f,-0.360 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (-0.418 + dx, dx, 0.418 + dx, 0.405 + dx, -0.405 + dx, k.c(col["band"]), k.ink))
    kx = -0.30 + 0.12 * yaw
    o.append('<path d="M%.4f,-0.452 L%.4f,-0.440 L%.4f,-0.372 L%.4f,-0.366 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (kx - 0.035, kx + 0.030, kx + 0.028, kx - 0.037, k.c(col["band_l"]), k.ink))
    # snap brim
    o.append('<path d="M-0.625,-0.372 Q-0.615,-0.318 -0.44,-0.305 Q%.4f,-0.225 0.44,-0.305 Q0.615,-0.318 0.625,-0.372 Q0.32,-0.352 %.4f,-0.355 '
             'Q-0.32,-0.352 -0.625,-0.372 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (fdx, fdx * 0.3, k.c(col["brim"]), k.ink))
    o.append('<path d="M-0.45,-0.330 Q%.4f,-0.262 0.43,-0.330" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.85"/>'
             % (fdx, k.c(col["edge"])))
    o.append('</g>')
    _ext(k, C, ((-0.66, -0.36), (0.66, -0.36), (-0.3, -0.73), (0.3, -0.73)))
    return "".join(o), (cx, -0.70)


def _tufts(k, yaw, ytop=-0.26):
    """senior_b: white tufts of hair poking out under the hat on both sides (the one on the side the face turns to shrinks)."""
    o_ink, o_w = [], []
    for s in (-1, 1):
        g = _clamp(1.0 + 0.45 * max(0.0, -s * yaw) - 0.75 * max(0.0, s * yaw), 0.2, 1.5)
        for (x, y, r) in ((0.455, ytop + 0.03, 0.062), (0.505, ytop + 0.11, 0.070), (0.475, ytop + 0.20, 0.058), (0.420, ytop + 0.25, 0.040)):
            xx = s * (0.40 + (x - 0.40) * g)
            rr = r * (0.55 + 0.45 * g)
            o_ink.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (xx, y, rr + 0.018, k.ink))
            o_w.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (xx, y, rr, k.c("#f4f1f3")))
            k.ext.append((xx, y, rr + 0.02))
        o_w.append('<path d="M%.4f,%.4f q%.4f,0.04 0,0.08" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                   % (s * (0.40 + 0.10 * g), ytop + 0.07, s * 0.03, k.c("#c9c1cb")))
    return "".join(o_ink) + "".join(o_w)


def _hat_bowler(k, C, yaw):
    """senior_b: pale dove-grey bowler (LOOK_SPEC 2.6 recipe): dome = upper half of an ellipse rx 0.42 ry 0.31 on y = -0.37,
    narrow black band, brim crescent -0.56..0.56 dipping to -0.25, curled tips, one highlight streak; white tufts under it."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fdx = 0.20 * yaw
    g = _gradient(k, "ht", col, x0=-0.42, x1=0.42, mid=0.30)
    o = [_tufts(k, yaw)]
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    dome = "M%.4f,-0.370 A0.420,0.310 0 0 1 %.4f,-0.370 Z" % (-0.42 + dx, 0.42 + dx)
    o.append('<path d="%s" fill="%s"/>' % (dome, g))
    o.append('<path d="M%.4f,-0.500 Q%.4f,-0.615 %.4f,-0.640" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.9"/>'
             % (-0.30 + dx, -0.20 + dx, 0.05 + dx, k.c(col["shine"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.035" stroke-linejoin="round"/>' % (dome, k.ink))
    o.append('<path d="M%.4f,-0.432 Q%.4f,-0.410 %.4f,-0.432 L%.4f,-0.370 L%.4f,-0.370 Z" fill="%s" stroke="%s" stroke-width="0.011"/>'
             % (-0.413 + dx, dx, 0.413 + dx, 0.420 + dx, -0.420 + dx, k.c(col["band"]), k.ink))
    o.append('<path d="M-0.56,-0.385 Q-0.585,-0.322 -0.40,-0.310 Q%.4f,-0.225 0.40,-0.310 Q0.585,-0.322 0.56,-0.385 Q0.30,-0.340 %.4f,-0.345 '
             'Q-0.30,-0.340 -0.56,-0.385 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (fdx, fdx * 0.3, k.c(col["brim"]), k.ink))
    o.append('<path d="M-0.41,-0.333 Q%.4f,-0.262 0.39,-0.333" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.9"/>'
             % (fdx, k.c(col["edge"])))
    o.append('</g>')
    _ext(k, C, ((-0.60, -0.37), (0.60, -0.37), (-0.25, -0.69), (0.25, -0.69)))
    return "".join(o), (dx, -0.685)


def _hat_eyeshade(k, C, yaw):
    """clerk: green celluloid eyeshade (LOOK_SPEC 2.6): dark band 0.05 tall at y = -0.27 and a translucent green visor
    0.80 wide reaching y = -0.13 that slides to the facing side.  The hair over the crown is the hair style "cap"."""
    col = C["hat_colors"]
    vx = 0.26 * yaw
    hv = 0.40 - 0.07 * abs(yaw)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="M-0.488,-0.285 Q0,-0.335 0.488,-0.285 L0.482,-0.225 Q0,-0.275 -0.482,-0.225 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (k.c(col["band"]), k.ink))
    vis = ("M%.4f,-0.262 Q%.4f,-0.282 %.4f,-0.262 Q%.4f,-0.130 %.4f,-0.118 Q%.4f,-0.130 %.4f,-0.262 Z"
           % (vx - hv, vx, vx + hv, vx + hv * 0.80, vx, vx - hv * 0.80, vx - hv))
    o.append('<path d="%s" fill="%s" opacity="0.80"/>' % (vis, k.c(col["visor"])))
    o.append('<path d="M%.4f,-0.245 Q%.4f,-0.140 %.4f,-0.140" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.6"/>'
             % (vx - hv * 0.72, vx - hv * 0.55, vx - hv * 0.15, k.c(col["visor_l"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (vis, k.ink))
    o.append('</g>')
    _ext(k, C, ((-0.50, -0.29), (0.50, -0.29), (vx - hv - 0.01, -0.25), (vx + hv + 0.01, -0.25), (vx, -0.11)))
    return "".join(o), (0.0, -0.48)


def _hat_boater(k, C, yaw):
    """beach_man: straw boater: flat-topped cylinder crown 0.76 wide with its top face showing, red ribbon with two navy
    stripes and a flat side bow, flat brim ellipse 1.26 x 0.18; straw weave lines."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    g = _gradient(k, "ht", col, x0=-0.40, x1=0.40, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    by, brx, bry = -0.350, 0.630, 0.090
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.028"/>'
             % (dx * 0.5, by, brx, bry, k.c(col["brim"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
             % (dx * 0.5, by, brx * 0.82, bry * 0.66, k.c(col["weave"])))
    crown = "M%.4f,-0.590 L%.4f,-0.372 Q%.4f,-0.335 %.4f,-0.372 L%.4f,-0.590 Z" % (-0.380 + dx, -0.380 + dx, dx, 0.380 + dx, 0.380 + dx)
    o.append('<path d="%s" fill="%s"/>' % (crown, g))
    for y in (-0.555, -0.520, -0.485):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>'
                 % (-0.38 + dx, y, dx, y + 0.03, 0.38 + dx, y, k.c(col["weave"])))
    # ribbon with two navy stripes
    o.append('<path d="M%.4f,-0.470 Q%.4f,-0.440 %.4f,-0.470 L%.4f,-0.372 Q%.4f,-0.335 %.4f,-0.372 Z" fill="%s"/>'
             % (-0.380 + dx, dx, 0.380 + dx, 0.380 + dx, dx, -0.380 + dx, k.c(col["band"])))
    for y in (-0.442, -0.400):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016"/>'
                 % (-0.38 + dx, y, dx, y + 0.032, 0.38 + dx, y, k.c(col["stripe"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (crown, k.ink))
    o.append('<ellipse cx="%.4f" cy="-0.590" rx="0.380" ry="0.045" fill="%s" stroke="%s" stroke-width="0.022"/>' % (dx, k.c(col["light"]), k.ink))
    kx = -0.28 + 0.12 * yaw
    o.append('<path d="M%.4f,-0.468 L%.4f,-0.462 L%.4f,-0.378 L%.4f,-0.372 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (kx - 0.040, kx + 0.036, kx + 0.034, kx - 0.042, k.c(col["band"]), k.ink))
    # front half of the brim over the crown base
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 0 %.4f,%.4f" fill="%s" stroke="%s" stroke-width="0.028"/>'
             % (dx * 0.5 - brx, by, brx, bry, dx * 0.5 + brx, by, k.c(col["brim"]), k.ink))
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 0 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
             % (dx * 0.5 - brx * 0.82, by, brx * 0.82, bry * 0.66, dx * 0.5 + brx * 0.82, by, k.c(col["weave"])))
    o.append('</g>')
    _ext(k, C, ((-0.66, -0.35), (0.66, -0.35), (-0.38, -0.64), (0.38, -0.64)))
    return "".join(o), (dx, -0.635)


def _bob(k, yaw, col):
    """beach_woman: chin-length waved bob outside the head contour, under the hat brim."""
    o = []
    for s in (-1, 1):
        g = _clamp(1.0 + 0.35 * max(0.0, -s * yaw) - 0.45 * max(0.0, s * yaw), 0.4, 1.4)
        def Q(x, y):
            return (s * (0.36 + (x - 0.36) * g), y)
        pts = [Q(0.30, -0.30), Q(0.52, -0.25), Q(0.585, -0.06), Q(0.565, 0.12), Q(0.600, 0.235), Q(0.500, 0.300), Q(0.425, 0.230),
               Q(0.455, 0.05), Q(0.395, -0.15)]
        d = P._smooth_closed(pts)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
                 % (Q(0.47, -0.18) + Q(0.53, 0.02) + Q(0.51, 0.20) + (k.c(P._shade(col, 0.72)),)))
        for p in pts:
            k.ext.append((p[0], p[1], 0.03))
    return "".join(o)


def _ribbon_sides(yaw):
    """[(side, opacity)] for things that hang behind the head (ribbons, hat bow): screen-left for yaw >= 0, screen-right for
    yaw <= -0.16, cross-faded in between so turning through the front view never pops."""
    wl = _smooth(-0.16, 0.0, yaw)
    return [(sd, w) for sd, w in ((-1.0, wl), (1.0, 1.0 - wl)) if w > 0.001]


def _hat_sunhat(k, C, yaw):
    """beach_woman: wide cream sun hat (1.56 D) with a low round crown, floppy brim drooping at the sides, navy ribbon and a
    bow whose two tails stream behind the head; the waved bob is drawn under it."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fdx = 0.18 * yaw
    o = [_bob(k, yaw, C["hair"]["color"])]
    g = _gradient(k, "ht", col, x0=-0.70, x1=0.70, mid=0.35)
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    # ribbon tails behind the head, on the side away from the face; they cross-fade between the sides over yaw -0.16..0
    # (a hard switch at yaw = 0 measured as a pop in the turn strip)
    sides = _ribbon_sides(yaw)
    for bs, wgt in sides:
        bsx = bs * (0.30 + 0.06 * _clamp(abs(yaw) * 4.0, 0.0, 1.0))
        o.append('<g opacity="%.3f">' % wgt if wgt < 0.999 else "<g>")
        for j, (ex, ey) in enumerate(((0.66, -0.06), (0.52, 0.02))):
            tx = bsx + bs * (ex - 0.30)
            o.append('<path d="M%.4f,-0.40 Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,-0.37 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                     % (bsx, (bsx + tx) / 2 + 0.03, -0.25 + j * 0.03, tx, ey, tx + bs * 0.015, ey + 0.05, tx - 0.04 * bs, ey + 0.02,
                        (bsx + tx) / 2 - 0.02, -0.22 + j * 0.03, bsx - 0.02 * bs, k.c(col["band_d"]), k.ink))
            k.ext.append((tx, ey + 0.05, 0.04))
        o.append("</g>")
    brim = ("M-0.78,-0.275 C-0.72,-0.415 -0.42,-0.455 %.4f,-0.448 C0.42,-0.455 0.72,-0.415 0.78,-0.275 C0.76,-0.205 0.64,-0.200 0.52,-0.240 "
            "Q0.26,-0.195 %.4f,-0.210 Q-0.26,-0.195 -0.52,-0.240 C-0.64,-0.200 -0.76,-0.205 -0.78,-0.275 Z" % (dx, fdx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (brim, g, k.ink))
    o.append('<path d="M-0.66,-0.262 C-0.52,-0.262 -0.30,-0.238 %.4f,-0.248 C0.30,-0.238 0.52,-0.262 0.66,-0.262" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (fdx, k.c(col["dark"])))
    crown = "M%.4f,-0.370 C%.4f,-0.520 %.4f,-0.610 %.4f,-0.610 C%.4f,-0.610 %.4f,-0.520 %.4f,-0.370 Z" % (
        -0.39 + dx, -0.40 + dx, -0.20 + dx, dx, 0.20 + dx, 0.40 + dx, 0.39 + dx)
    o.append('<path d="%s" fill="%s"/>' % (crown, g))
    o.append('<path d="M%.4f,-0.470 Q%.4f,-0.585 %.4f,-0.600" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.9"/>'
             % (-0.30 + dx, -0.22 + dx, -0.08 + dx, k.c(col["shine"])))
    o.append('<path d="M%.4f,-0.448 Q%.4f,-0.418 %.4f,-0.448 L%.4f,-0.366 Q%.4f,-0.336 %.4f,-0.366 Z" fill="%s"/>'
             % (-0.397 + dx, dx, 0.397 + dx, 0.392 + dx, dx, -0.392 + dx, k.c(col["band"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, k.ink))
    o.append('<path d="M%.4f,-0.366 Q%.4f,-0.336 %.4f,-0.366" fill="none" stroke="%s" stroke-width="0.012"/>' % (-0.392 + dx, dx, 0.392 + dx, k.ink))
    # bow (same cross-fade as the tails)
    for bs, wgt in sides:
        bsx = bs * (0.30 + 0.06 * _clamp(abs(yaw) * 4.0, 0.0, 1.0))
        o.append('<g opacity="%.3f">' % wgt if wgt < 0.999 else "<g>")
        for sg in (-1, 1):
            o.append('<path d="M%.4f,-0.405 L%.4f,-0.455 L%.4f,-0.355 Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
                     % (bsx, bsx + sg * 0.075, bsx + sg * 0.070, k.c(col["band"]), k.ink))
        o.append('<circle cx="%.4f" cy="-0.405" r="0.024" fill="%s" stroke="%s" stroke-width="0.010"/></g>' % (bsx, k.c(col["band_d"]), k.ink))
    o.append('</g>')
    _ext(k, C, ((-0.80, -0.27), (0.80, -0.27), (-0.3, -0.63), (0.3, -0.63)))
    return "".join(o), (dx, -0.615)


def _hat_sailor(k, C, yaw):
    """beach_kid: sailor's flat cap: white flat top overhanging a navy band with a gold stripe, two navy ribbon tails at
    the back with notched ends; worn tipped back."""
    col = C["hat_colors"]
    dx = -0.04 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    for bs, wgt in _ribbon_sides(yaw):
        o.append('<g opacity="%.3f">' % wgt if wgt < 0.999 else "<g>")
        for j in range(2):
            x0 = bs * (0.30 + 0.05 * j)
            x1 = bs * (0.42 + 0.10 * j)
            y1 = -0.04 + 0.05 * j
            o.append('<path d="M%.4f,-0.34 Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,-0.34 Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
                     % (x0, x0 + bs * 0.06, -0.20, x1, y1, x1 + bs * 0.010, y1 + 0.060, x1 - bs * 0.045, y1 + 0.030, x0 - bs * 0.01, -0.18, x0 - bs * 0.055,
                        k.c(col["band"]), k.ink))
            k.ext.append((x1, y1 + 0.06, 0.03))
        o.append("</g>")
    o.append('<path d="M%.4f,-0.430 Q%.4f,-0.405 %.4f,-0.430 L%.4f,-0.300 Q%.4f,-0.268 %.4f,-0.300 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (-0.440 + dx, dx, 0.440 + dx, 0.452 + dx, dx, -0.452 + dx, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,-0.362 Q%.4f,-0.334 %.4f,-0.362" fill="none" stroke="%s" stroke-width="0.016"/>' % (-0.44 + dx, dx, 0.44 + dx, k.c(col["gold"])))
    g = _gradient(k, "ht", col, x0=-0.52, x1=0.52, mid=0.35)
    o.append('<ellipse cx="%.4f" cy="-0.480" rx="0.540" ry="0.105" fill="%s" stroke="%s" stroke-width="0.026"/>' % (dx * 1.3, g, k.ink))
    o.append('<path d="M%.4f,-0.465 A0.470,0.070 0 0 0 %.4f,-0.465" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
             % (dx * 1.3 - 0.47, dx * 1.3 + 0.47, k.c(col["dark"])))
    o.append('</g>')
    _ext(k, C, ((-0.57, -0.48), (0.57, -0.48), (0.0, -0.60), (-0.47, -0.30), (0.47, -0.30)))
    return "".join(o), (dx * 1.3, -0.585)


HATS = {"fedora": _hat_fedora, "bowler": _hat_bowler, "eyeshade": _hat_eyeshade, "boater": _hat_boater, "sunhat": _hat_sunhat,
        "sailor": _hat_sailor}


def _hat_newsboy(k, C, yaw):
    fn = HATS.get(C.get("hat_style"))
    if fn is None:
        return _O["_hat_newsboy"](k, C, yaw)
    return fn(k, C, yaw)


# ============================================================================= face additions
def _glasses(k, C, L):
    """round wire spectacles over the eyes; rims narrow with the eye spacing when the head turns."""
    xL, xR, ey, sL, sR = L["xL"], L["xR"], L["ey"], L["sL"], L["sR"]
    half = (xR - xL) / 2.0
    rx = min(0.118, half - 0.010)
    o = []
    for x, s, sd in ((xL, sL, -1), (xR, sR, 1)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="%.4f"/>'
                 % (x, ey, rx * s, 0.112 * s, k.c("#d9ecf7"), k.ink, 0.021 * s))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.85"/>'
                 % (x - 0.060 * s, ey - 0.040 * s, x - 0.030 * s, ey - 0.072 * s))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                 % (x + sd * rx * s, ey - 0.020, sd * 0.445, ey - 0.055, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.017" stroke-linecap="round"/>'
             % (xL + rx * sL, ey - 0.020, (xL + xR) / 2, ey - 0.055, xR - rx * sR, ey - 0.020, k.ink))
    return "".join(o)


def _lashes(k, C, P_, L):
    eyes = (P.EXPRESSIONS.get(P_["expr"]) or P.EXPRESSIONS["neutral"])["eyes"]
    if P_["blink"] >= 2 or eyes not in ("half", "ring", "dot", "wink"):
        return ""
    o = []
    ring = eyes == "ring"
    for x, s, sd in ((L["xL"], L["sL"], -1), (L["xR"], L["sR"], 1)):
        bx, by = (x + sd * 0.080 * s, L["ey"] - 0.060 * s) if ring else (x + sd * 0.070 * s, L["ey"] - 0.036 * s)
        for a, ln in ((-35.0, 0.050), (-5.0, 0.042)):
            vx, vy = math.cos(math.radians(a)) * sd, math.sin(math.radians(a))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
                     % (bx, by, bx + vx * ln * s, by + vy * ln * s, k.ink))
    return "".join(o)


def _pencil_tache(k, L):
    mx, my = L["mx"], L["my"]
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>'
            % (mx - 0.012, my - 0.050, mx - 0.050, my - 0.066, mx - 0.105, my - 0.040, mx + 0.012, my - 0.050, mx + 0.050, my - 0.066, mx + 0.105, my - 0.040, k.ink))


def _cheeks(k, L, col):
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.070" ry="0.040" fill="%s" opacity="0.55"/><ellipse cx="%.4f" cy="%.4f" rx="0.070" ry="0.040" fill="%s" opacity="0.55"/>'
            % (L["xL"] - 0.035, L["ey"] + 0.095, k.c(col), L["xR"] + 0.035, L["ey"] + 0.095, k.c(col)))


def _freckles(k, L):
    o = []
    for x, sd in ((L["xL"], -1), (L["xR"], 1)):
        for dx, dy in ((-0.03, 0.090), (0.0, 0.112), (0.03, 0.092)):
            o.append('<circle cx="%.4f" cy="%.4f" r="0.0115" fill="%s"/>' % (x + sd * 0.02 + dx, L["ey"] + dy, k.c("#c98a5c")))
    return "".join(o)


def _age_lines(k, C, P_, L):
    """review addition: under-eye bags (one soft ink arc per eye) and a cheek crease beside the mouth, so the seniors read
    older than the hero and the clerk at a 110 px head.  Inside the lens (shorter) with spectacles; none with ring eyes
    (wide-open surprise has no room under the ring)."""
    eyes = (P.EXPRESSIONS.get(P_["expr"]) or P.EXPRESSIONS["neutral"])["eyes"]
    low, hw = (0.074, 0.042) if C.get("glasses") else (0.092, 0.058)
    o = []
    if eyes != "ring":
        for x, s, sd in ((L["xL"], L["sL"], -1), (L["xR"], L["sR"], 1)):
            y = L["ey"] + low * s
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.55"/>'
                     % (x - hw * s, y, x + sd * 0.006 * s, y + 0.024 * s, x + hw * s, y, k.ink, 0.015 * s))
    if not C.get("moustache"):
        mx, my = L["mx"], L["my"]
        for sd, s in ((-1, L["sL"]), (1, L["sR"])):
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.45"/>'
                     % (mx + sd * 0.150 * s, my - 0.050, mx + sd * 0.180 * s, my, mx + sd * 0.160 * s, my + 0.045, k.ink, 0.013 * s))
    return "".join(o)


def _face(k, C, P_, white):
    _CUR[0] = C
    svg, L = _O["_face"](k, C, P_, white)
    add_under, add_over = [], []
    if C.get("age_lines"):
        add_over.append(_age_lines(k, C, P_, L))
    if C.get("cheeks"):
        add_under.append(_cheeks(k, L, C["cheeks"]))
    if C.get("freckles"):
        add_under.append(_freckles(k, L))
    if C.get("lashes"):
        add_over.append(_lashes(k, C, P_, L))
    if C.get("pencil_moustache"):
        add_over.append(_pencil_tache(k, L))
    if C.get("glasses"):
        add_over.append(_glasses(k, C, L))
    if not add_under and not add_over:
        return svg, L
    return "".join(add_under) + svg + "".join(add_over), L


def _moustache(k, mx, my, s=1.0):
    C = _CUR[0]
    if not C or C.get("moustache_style") != "walrus":
        return _O["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#ece8ec")
    def Q(x, y):
        return (mx + x * s, my + y * s)
    pts = [Q(0.0, -0.052), Q(-0.110, -0.068), Q(-0.200, -0.040), Q(-0.240, 0.035), Q(-0.222, 0.112), Q(-0.170, 0.082), Q(-0.120, 0.098),
           Q(-0.070, 0.060), Q(0.0, 0.074), Q(0.070, 0.060), Q(0.120, 0.098), Q(0.170, 0.082), Q(0.222, 0.112), Q(0.240, 0.035),
           Q(0.200, -0.040), Q(0.110, -0.068)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.017" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)]
    st = []
    for x in (-0.17, -0.11, -0.05, 0.05, 0.11, 0.17):
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (Q(x * 0.8, -0.03) + Q(x * 1.05, 0.02) + Q(x * 1.12, 0.065)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % ("".join(st), k.c("#b4abb7")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (Q(0.0, -0.048) + Q(0.0, 0.010) + (k.ink,)))
    return "".join(o)


# ============================================================================= hair styles, garters, cast memory
def _hair(k, C, yaw):
    base = _O["_hair"](k, C, yaw)
    H = C["hair"]
    st = H.get("style")
    if st == "cap":
        # hair over the crown above the eyeshade band: ragged lower edge, a lighter side parting that slides with yaw
        col = k.c(H["color"])
        pts = []
        for i in range(13):
            x = -0.52 + i * (1.04 / 12)
            pts.append((x, -0.255 + 0.012 * math.sin(i * 2.3 + C["seed"])))
        d = "M-0.6,-0.7 L" + " L".join("%.4f,%.4f" % p for p in pts) + " L0.6,-0.7 Z"
        px = 0.12 - 0.20 * yaw
        base += '<path d="%s" fill="%s"/>' % (d, col)
        base += ('<path d="M%.4f,-0.47 Q%.4f,-0.40 %.4f,-0.31" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                 % (px, px - 0.03, px - 0.09, k.c(H.get("shine", "#7a5040"))))
    elif st == "curl":
        col = k.c(H["color"])
        cx = 0.06 + 0.10 * yaw
        base += ('<path d="M%.4f,-0.30 Q%.4f,-0.18 %.4f,-0.17 Q%.4f,-0.16 %.4f,-0.22 Q%.4f,-0.20 %.4f,-0.24 Z" fill="%s"/>'
                 % (cx - 0.10, cx - 0.07, cx - 0.01, cx + 0.04, cx + 0.03, cx + 0.07, cx + 0.10, col))
    return base


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = _CUR[0]
    if tail is None and C and C.get("garters"):
        sd = C["seed"] * 1.7
        if abs(seed - (sd + 2.3)) < 1e-9 or abs(seed - (sd + 4.6)) < 1e-9:
            dx, dy = E[0] - S[0], E[1] - S[1]
            ln = math.hypot(dx, dy)
            if ln > 0.06:
                ux, uy = dx / ln, dy / ln
                cx, cy = S[0] + dx * 0.62, S[1] + dy * 0.62
                hl = 0.85 * w + 0.012           # half length across the arm
                nx, ny = -uy, ux
                col = k.c(C["colors"].get("garter", "#b8322a"))
                out += ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>'
                        '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>'
                        '<circle cx="%.4f" cy="%.4f" r="0.012" fill="%s"/>'
                        % (cx - nx * hl, cy - ny * hl, cx + nx * hl, cy + ny * hl, k.ink,
                           cx - nx * hl, cy - ny * hl, cx + nx * hl, cy + ny * hl, col,
                           cx + nx * hl * 0.4, cy + ny * hl * 0.4, k.c("#e0c063")))
    return out


def _norm(C, pose):
    _CUR[0] = C
    return _O["_norm"](C, pose)


# ============================================================================= props
NEW_PROPS = ("bucket", "newspaper", "forecast", "mug")
NEW_TIP = {"bucket": 0.47, "newspaper": 0.44, "forecast": 0.52, "mug": 0.0}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS:
        return _O["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    if kind == "bucket":
        # tin sand pail hanging from the hand by its bail: always upright (gravity), whatever the arm angle
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        o.append('<path d="M-0.160,0.215 Q-0.150,-0.030 0,-0.020 Q0.150,-0.030 0.160,0.215" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % ink)
        o.append('<path d="M-0.160,0.215 Q-0.150,-0.030 0,-0.020 Q0.150,-0.030 0.160,0.215" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c("#c3cad3"))
        k.defs.append('<linearGradient id="%s_bk" gradientUnits="userSpaceOnUse" x1="-0.17" y1="0" x2="0.17" y2="0"><stop offset="0" stop-color="%s"/>'
                      '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (k.uid, k.c("#ef7a45"), k.c("#d9572b"), k.c("#9c3a1a")))
        o.append('<path d="M-0.170,0.215 L0.170,0.215 L0.130,0.470 Q0,0.490 -0.130,0.470 Z" fill="url(#%s_bk)" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.uid, ink))
        o.append('<path d="M-0.158,0.290 L0.158,0.290 L0.149,0.350 L-0.149,0.350 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#f0c64a"), ink))
        for x in (-0.09, 0.0, 0.09):
            o.append('<circle cx="%.4f" cy="0.320" r="0.014" fill="%s"/>' % (x, k.c("#2f5fa8")))
        o.append('<ellipse cx="0" cy="0.215" rx="0.172" ry="0.034" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#c9ced6"), ink))
        o.append('<ellipse cx="0" cy="0.219" rx="0.140" ry="0.020" fill="%s"/>' % k.c("#d9b27a"))
        for x in (-0.160, 0.160):
            o.append('<circle cx="%.4f" cy="0.215" r="0.016" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, k.c("#c9ced6"), ink))
        o.append('</g>')
        for e in ((-0.18, 0.2), (0.18, 0.2), (-0.14, 0.49), (0.14, 0.49), (0.0, -0.03)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0], H[1] + 0.47 * sc)
    if kind == "mug":
        # enamel coffee mug held upright, the hand ball in front of it, handle on the +x side, a wisp of steam
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        o.append('<path d="M0.080,-0.110 Q0.165,-0.110 0.160,-0.040 Q0.155,0.020 0.080,0.020" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % ink)
        o.append('<path d="M0.080,-0.110 Q0.165,-0.110 0.160,-0.040 Q0.155,0.020 0.080,0.020" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c("#efe8d8"))
        o.append('<path d="M-0.095,-0.150 L0.095,-0.150 L0.088,0.060 Q0,0.075 -0.088,0.060 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c("#efe8d8"), ink))
        o.append('<path d="M-0.094,-0.150 L0.094,-0.150 L0.093,-0.118 L-0.093,-0.118 Z" fill="%s"/>' % k.c("#3f63a8"))
        o.append('<ellipse cx="0" cy="-0.150" rx="0.095" ry="0.022" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#5a3a26"), ink))
        o.append('<path d="M-0.020,-0.185 Q-0.055,-0.235 -0.015,-0.275 Q0.020,-0.310 -0.010,-0.350 M0.035,-0.190 Q0.005,-0.230 0.035,-0.265" fill="none" '
                 'stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.75"/>' % k.c("#f6f1ea"))
        o.append('</g>')
        for e in ((-0.10, -0.16), (0.17, -0.11), (0.1, 0.07), (-0.1, 0.07), (0.0, -0.35)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0], H[1])
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind == "newspaper":
        # folded daily paper 0.47 x 0.32 held by its near edge: masthead bar, a headline, a photo box, text columns
        o.append('<path d="M-0.030,-0.160 L0.440,-0.160 L0.440,0.160 L-0.030,0.160 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#ece4d2"), ink))
        o.append('<path d="M0.410,-0.160 L0.440,-0.130 L0.440,0.130 L0.410,0.160" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#d6ccb6"), ink))
        o.append('<path d="M0.020,-0.120 L0.380,-0.120" stroke="%s" stroke-width="0.040"/>' % k.c("#3d3540"))
        o.append('<path d="M0.020,-0.065 L0.300,-0.065" stroke="%s" stroke-width="0.022"/>' % k.c("#6d6470"))
        o.append('<rect x="0.240" y="-0.035" width="0.140" height="0.110" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#a49aa0"), ink))
        d = "".join("M0.020,%.3f L0.200,%.3f" % (y, y) for y in (-0.025, 0.005, 0.035, 0.065, 0.095, 0.125))
        d += "".join("M0.240,%.3f L0.380,%.3f" % (y, y) for y in (0.100, 0.128))
        o.append('<path d="%s" stroke="%s" stroke-width="0.010" fill="none" opacity="0.8"/>' % (d, k.c("#8d8089")))
        ends = ((-0.03, -0.16), (0.44, -0.16), (0.44, 0.16), (-0.03, 0.16))
        tip = NEW_TIP["newspaper"]
    elif kind == "forecast":
        # Weather Bureau forecast sheet 0.55 x 0.42: blue header band, rain cloud, the word RAIN, table lines
        o.append('<path d="M-0.030,-0.210 L0.520,-0.210 L0.520,0.150 L0.460,0.210 L-0.030,0.210 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#fbf5e4"), ink))
        o.append('<path d="M0.520,0.150 L0.460,0.150 L0.460,0.210 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#e2d7bd"), ink))
        o.append('<rect x="0.000" y="-0.185" width="0.490" height="0.070" fill="%s"/>' % k.c("#35538f"))
        o.append('<text x="0.245" y="-0.135" font-family="Georgia, serif" font-size="0.042" font-weight="700" fill="%s" text-anchor="middle">FORECAST</text>' % k.c("#fbf5e4"))
        o.append('<path d="M0.050,0.000 Q0.040,-0.060 0.090,-0.060 Q0.110,-0.095 0.150,-0.075 Q0.190,-0.080 0.190,-0.040 Q0.215,-0.020 0.190,0.000 Z" '
                 'fill="%s" stroke="%s" stroke-width="0.009" stroke-linejoin="round"/>' % (k.c("#a7b1c4"), ink))
        o.append('<path d="M0.080,0.020 L0.070,0.055 M0.120,0.020 L0.110,0.055 M0.160,0.020 L0.150,0.055" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c("#35538f"))
        o.append('<text x="0.355" y="0.025" font-family="Georgia, serif" font-size="0.090" font-weight="700" fill="%s" text-anchor="middle">RAIN</text>' % k.c("#2b2530"))
        d = "".join("M0.030,%.3f L0.430,%.3f" % (y, y) for y in (0.095, 0.130, 0.165))
        o.append('<path d="%s" stroke="%s" stroke-width="0.009" fill="none" opacity="0.8"/>' % (d, k.c("#8d8089")))
        ends = ((-0.03, -0.21), (0.52, -0.21), (0.52, 0.21), (-0.03, 0.21))
        tip = NEW_TIP["forecast"]
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(tip * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


# ============================================================================= builds, arm presets
PROFILE_REGULAR = ((0.55, 0.02), (0.86, 0.10), (0.95, 0.25), (0.99, 0.42), (1.00, 0.62), (0.97, 0.80), (0.88, 0.90), (0.70, 0.96), (0.40, 1.00))
PROFILE_PEAR = ((0.44, 0.02), (0.72, 0.10), (0.87, 0.25), (0.96, 0.42), (1.00, 0.62), (0.99, 0.78), (0.93, 0.88), (0.72, 0.96), (0.40, 1.00))
PROFILE_ATHLETE = ((0.68, 0.02), (0.95, 0.10), (1.00, 0.24), (0.97, 0.42), (0.91, 0.60), (0.88, 0.76), (0.84, 0.88), (0.66, 0.97), (0.36, 1.00))
PROFILE_HOURGLASS = ((0.62, 0.02), (0.92, 0.10), (1.00, 0.25), (0.93, 0.45), (0.80, 0.62), (0.82, 0.78), (0.86, 0.90), (0.68, 0.97), (0.38, 1.00))
PROFILE_CHILD = ((0.62, 0.02), (0.90, 0.11), (0.98, 0.27), (1.00, 0.50), (1.00, 0.70), (0.96, 0.85), (0.76, 0.96), (0.42, 1.00))
CHILD_ARM = 0.54

SHADE = {"slim": (0.065, -0.660, -1.0, "top", "open", 0.35, 1.0), "stout": (-0.050, -0.570, -1.0, "top", "open", 0.35, 1.0),
         "regular": (0.010, -0.600, -1.0, "top", "open", 0.35, 1.0), "child": (0.060, -0.540, -1.0, "top", "open", 0.35, 1.04)}


def _build_presets():
    A = P.ARM_PRESETS
    sl, so = A["slim"], A["stout"]
    if "regular" not in A:
        A["regular"] = dict((n, ((sl[n][0] + so[n][0]) / 2, (sl[n][1] + so[n][1]) / 2, (sl[n][2] + so[n][2]) / 2, sl[n][3], sl[n][4],
                                 (sl[n][5] + so[n][5]) / 2, (sl[n][6] + so[n][6]) / 2)) for n in sl if n in so)
    if "child" not in A:
        f = CHILD_ARM / 0.74
        A["child"] = dict((n, (v[0] * f, v[1] * f) + tuple(v[2:])) for n, v in sl.items())
    for b, v in SHADE.items():
        A[b].setdefault("shade", v)


# ============================================================================= cast definitions
# seeds: the head wobble depends on the seed; each one was chosen so that the head reads round like hero / boss
# (ink-to-ink width on the centre row 0.98..1.02 D, lower-arc wobble rms below 1.25 percent D: see head_seed_metrics())
NEW_CAST = {
    # older senior forecaster, regular build: camel fedora, round spectacles, brown herringbone tweed waistcoat, navy tie
    "senior_a": dict(
        build="regular", seed=4.9,
        torso_w=0.78, torso_h=1.04, profile=PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.30, 0.47), arm=0.74, hip_x=0.17, leg=1.30, stance=0.07, wide=0.28, limb_w=0.062,
        eye_y=0.020, brow="stroke", brow_th=0.054, mouth="frown", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="fedora", hat_tilt=-3.0, ear_pencil=False, glasses=True, age_lines=True,
        hat_colors=dict(light="#dcb27a", base="#b8854c", dark="#7c5530", shine="#f1dcb2", band="#3b2a22", band_l="#5a4030",
                        brim="#a77543", edge="#dcb985"),
        hair=dict(color="#bdb5b8", front=0.09, grow=0.22),            # review: silver (was #968a86, read as brown-grey)
        costume="tweed",
        colors=dict(base="#7b4f33", dark="#4b2f1f", fleck="#b98d62", pocket="#6a432b", shirt="#d7e3f1", collar="#eef3f8",
                    tie="#2f4f8a", tie_dark="#1f3563", tie_stripe="#e2b44a", button="#e0bd84", button_l="#f4e2bd",
                    pen="#9e2b25", pen_clip="#e8c86a", pants="#575264"),
    ),
    # older senior forecaster, short and round: pale grey bowler, white tufts, white walrus moustache, burgundy cardigan, pipe
    "senior_b": dict(
        build="stout", seed=18.4,
        torso_w=1.06, torso_h=0.98, profile=PROFILE_PEAR, shift_pow=1.25,
        shoulder=(0.35, 0.46), arm=0.74, hip_x=0.15, leg=1.16, stance=0.05, wide=0.24, limb_w=0.068,
        eye_y=0.005, brow="stroke", brow_th=0.052, mouth="dash", moustache=True, moustache_style="walrus", smirk_side=-1,
        hat="newsboy", hat_style="bowler", hat_tilt=-5.0, ear_pencil=False, age_lines=True,
        hat_colors=dict(light="#d6d1d6", base="#aca6ad", dark="#6f6973", shine="#f6f3f7", band="#2f2a33", brim="#958f97", edge="#dcd7dd"),
        hair=dict(color="#d4ccd6", front=0.07, grow=0.20),
        costume="cardigan",
        colors=dict(base="#a8383f", dark="#5c1820", rib="#7c2630", band="#76222b", pocket="#862a32", shirt="#f0ebe6", tie="#283a62",
                    tie_dark="#18233f", button="#7a4a2a", button_l="#b07a50", pipe="#6b3d26", stem="#3a2a2a", pants="#3d3a46",
                    moustache="#efebef"),
    ),
    # young office junior: tall and slim, green eyeshade over slicked hair, pinstriped shirt, orange tie, sleeve garters
    "clerk": dict(
        build="slim", seed=11.7,
        torso_w=0.55, torso_h=1.00, profile=P.PROFILE_SLIM, shift_pow=1.0,
        shoulder=(0.230, 0.54), arm=0.74, hip_x=0.20, leg=1.30, stance=0.09, wide=0.34, limb_w=0.055,   # review: leg 1.18 -> 1.30 (lanky, apart from the hero)
        eye_y=0.060, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="eyeshade", hat_tilt=-1.0, ear_pencil=False, garters=True,
        hat_colors=dict(band="#2f2a36", visor="#2f8a58", visor_l="#9fe0b8"),
        hair=dict(color="#4b2c20", front=0.085, grow=0.22, style="cap", shine="#7d5040"),
        costume="clerk_shirt",
        colors=dict(base="#e6ebf1", dark="#8a96a8", stripe="#7a9bd0", collar="#fbfcfd", tie="#d65a2c", tie_dark="#9e3c1a",
                    clip="#e3c46a", pocket="#d6dee8", pencil1="#efc13a", pencil2="#cf3b2c", button="#fbfbfb", belt="#5b3a26",
                    buckle="#e3c46a", pants="#5e5868", garter="#c0332a"),
    ),
    # Long Island family, 1938: the father
    "beach_man": dict(
        build="regular", seed=13.2,
        torso_w=0.70, torso_h=1.00, profile=PROFILE_ATHLETE, shift_pow=1.1,
        shoulder=(0.28, 0.50), arm=0.74, hip_x=0.17, leg=1.24, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.035, brow="stroke", brow_th=0.044, mouth="dash", moustache=False, pencil_moustache=True, smirk_side=1,
        hat="newsboy", hat_style="boater", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(light="#f7e8b4", base="#ead17e", dark="#b8954a", brim="#ecd58a", weave="#b8984e", band="#c7362c", stripe="#22336a"),
        hair=dict(color="#5a3826", front=0.085, grow=0.22),
        costume="bathing",
        colors=dict(base="#354b8e", stripe="#f1e8d4", badge="#c7362c", belt="#f4ecdb", buckle="#d9b95c", pants="#1f2c57"),
    ),
    # the mother
    "beach_woman": dict(
        build="slim", seed=19.7,
        torso_w=0.52, torso_h=0.90, profile=PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.215, 0.52), arm=0.72, hip_x=0.135, leg=1.16, stance=0.05, wide=0.24, limb_w=0.055,   # review: was 0.050, below LOOK_SPEC 2.2 (0.055-0.075)
        eye_y=0.050, brow="stroke", brow_th=0.032, mouth="smile", moustache=False, smirk_side=-1, lashes=True, cheeks="#f4b9b6",
        hat="newsboy", hat_style="sunhat", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(light="#fffaee", base="#f2e6c8", dark="#c9b48a", shine="#ffffff", band="#2c4a8a", band_d="#1d3263"),
        hair=dict(color="#7a4630", front=0.10, grow=0.24),
        costume="dress", waist_y=0.965, skirt_len=0.56, skirt_w=0.50,
        colors=dict(base="#d84a3a", dark="#9c2c22", dot="#fbf2e6", collar="#fcf7ef", button="#fcf7ef", sash="#2c4a8a",
                    sash_dark="#1d3263", trim="#fbf2e6", pants="#d84a3a"),
    ),
    # the child (draw it at 0.8 of the adults' scale: CAST["beach_kid"]["scale_hint"]; standing height 2.2 D -> 1.76 D)
    "beach_kid": dict(
        build="child", seed=20.4, scale_hint=0.8,
        torso_w=0.50, torso_h=0.72, profile=PROFILE_CHILD, shift_pow=1.0,
        shoulder=(0.200, 0.48), arm=CHILD_ARM, hip_x=0.15, leg=0.70, stance=0.07, wide=0.22, limb_w=0.057,   # review: was 0.050 (forearm measured 0.046 on the 400 px/D render)
        eye_y=0.060, brow="dome", brow_th=0.034, mouth="smile", moustache=False, smirk_side=1, freckles=True, cheeks="#f6c3c0",
        hat="newsboy", hat_style="sailor", hat_tilt=-9.0, ear_pencil=False,
        hat_colors=dict(light="#ffffff", base="#f3f1ea", dark="#c8c4ba", band="#24366b", gold="#e3c04f"),
        hair=dict(color="#e0ad4a", front=0.07, grow=0.18, style="curl"),
        costume="sailor",
        colors=dict(base="#f3f0e8", navy="#24366b", navy_l="#3e528c", kerchief="#d23b2e", kerchief_d="#9c2a20", star="#e8c04a",
                    button="#f3f0e8", pants="#24366b"),
    ),
}

# feet-relative sprite canvases for the stage (sprites.DEFAULT_CANVAS), measured with canvas_check(): every arm preset with
# every prop at yaw +/-0.6, squash 0.8..1.15, crouch, wide legs, steam + Z + sweat + tears.  Head room above that pose range is
# 0.32 D or more, the same margin the hero / boss defaults keep (their room for the upper-body stretch).  Snapped to 1/16 D.
CANVAS = {
    "senior_a": (-1.8750, -4.6250, 1.8750, 0.1250),
    "senior_b": (-1.9375, -4.3750, 1.9375, 0.1250),
    "clerk": (-1.8125, -4.5625, 1.8125, 0.1250),          # review: taller for the longer legs (was -4.4375)
    "beach_man": (-1.8125, -4.5000, 1.8125, 0.1250),
    "beach_woman": (-1.8125, -4.3125, 1.8125, 0.1250),
    "beach_kid": (-1.4375, -3.6250, 1.4375, 0.1250),
}

# poses for the sheet / tests
STORY_EXT = {
    "seniors_agree": ("senior_a", dict(yaw=0.4, expr="smug", arm_r="hip", arm_l="point", head_roll=-6)),
    "walrus_scoffs": ("senior_b", dict(yaw=-0.4, expr="smug", arm_r="behind", arm_l="behind", head_roll=8, lean=-4)),
    "clerk_runs_in": ("clerk", dict(yaw=0.9, expr="shocked", fx=["sweat"], legs=dict(preset="step", stride=1.0), arm_r="raised",
                                    prop_l=dict(type="newspaper", angle=-60), arm_l="forward", lean=8)),
    "father_looks": ("beach_man", dict(yaw=0.6, pitch=-0.2, expr="neutral", arm_r="shade", arm_l="hip")),
    "kid_bucket": ("beach_kid", dict(yaw=-0.3, expr="happy", arm_r="down", prop_r="bucket", arm_l="wave")),
}


def head_seed_metrics(seed):
    """(ink-to-ink width on the head's centre row, fill-edge wobble rms in percent D) of the head drawn with this seed."""
    raw = []
    for i in range(720):
        d = i * 0.5
        th = math.radians(d)
        rf = P._fill_r(th, seed)
        ro = rf + P._outline_w(d) + 0.005 * P._wob(th, seed + 2.3) + 0.0016 * P._rough(th, seed)
        raw.append((d, math.cos(th), math.sin(th), rf, ro))
    cx, cy, r = P._circle_fit([(c * rf, s * rf) for (d, c, s, rf, ro) in raw if 25 <= d <= 155])
    g = P.R_FILL / r
    xs = [(c * rf - cx) * g + c * (ro - rf) for (d, c, s, rf, ro) in raw if abs((s * rf - cy) * g + s * (ro - rf) + P.FC[1]) < 0.01]
    rr = [math.hypot((c * rf - cx) * g, (s * rf - cy) * g) for (d, c, s, rf, ro) in raw if d <= 60 or d >= 330 or 120 <= d <= 210]
    m = sum(rr) / len(rr)
    return max(xs) - min(xs), 100.0 * (sum((v - m) ** 2 for v in rr) / len(rr)) ** 0.5


# ============================================================================= registration
class _StageHook(importlib.abc.MetaPathFinder):
    """adds CANVAS to sprites.DEFAULT_CANVAS of any `sprites` / `stage.sprites` module imported after this one."""
    def find_spec(self, name, path, target=None):
        if name not in ("sprites", "stage.sprites"):
            return None
        sys.meta_path.remove(self)
        try:
            spec = importlib.util.find_spec(name)
        finally:
            sys.meta_path.insert(0, self)
        if spec is None or spec.loader is None or not hasattr(spec.loader, "exec_module"):
            return spec
        loader = spec.loader
        orig = loader.exec_module

        class _L(importlib.abc.Loader):
            def create_module(self, s):
                return loader.create_module(s) if hasattr(loader, "create_module") else None

            def exec_module(self, module):
                orig(module)
                register_stage(module)
        spec.loader = _L()
        return spec


def register_stage(mod=None):
    """put the new canvases into sprites.DEFAULT_CANVAS (the module given, or every sprites module already imported)."""
    mods = [mod] if mod is not None else [sys.modules[n] for n in ("sprites", "stage.sprites") if n in sys.modules]
    for m in mods:
        dc = getattr(m, "DEFAULT_CANVAS", None)
        if isinstance(dc, dict):
            for n, c in CANVAS.items():
                dc.setdefault(n, c)


def register():
    if getattr(P, "_cast_ext_registered", False):
        register_stage()
        return
    for name in ("_torso", "_hat_newsboy", "_face", "_moustache", "_hair", "_ink_limb", "_prop", "_norm"):
        _O[name] = getattr(P, name)
    P._torso = _torso
    P._hat_newsboy = _hat_newsboy
    P._face = _face
    P._moustache = _moustache
    P._hair = _hair
    P._ink_limb = _ink_limb
    P._prop = _prop
    P._norm = _norm
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP)
    _build_presets()
    for n, c in NEW_CAST.items():
        P.CAST[n] = c
    P.STORY.update(STORY_EXT)
    P._cast_ext_registered = True
    if not any(isinstance(f, _StageHook) for f in sys.meta_path):
        sys.meta_path.insert(0, _StageHook())
    register_stage()


register()


# ============================================================================= command line: sheet, lineup, test
WALL_LIT, WALL_SHADE, OFFICE_FLOOR = "#b5484c", "#62284e", "#8a5a3c"
SAND, SEA, SKY = "#d9b27a", "#5d7fa3", "#9aa3b5"
LABEL = P._label


def _place(cast, pose, uid, D, x, y, anchor="feet", shadow=0.0):
    sc = NEW_CAST.get(cast, {}).get("scale_hint", 1.0) if anchor == "feet" else 1.0
    return P._place(cast, pose, uid, D * sc, x, y, anchor, shadow)


VIEWS = ((0.0, "front"), (0.5, "3/4"), (1.0, "near-profile"))
EXPRS = (("neutral", {}), ("smug", {"yaw": 0.25}), ("worried", {"fx": ["sweat"], "pitch": 0.4}), ("shocked", {"fx": ["sweat"], "head_roll": -6}))
AMUSED = {"senior_b": "laughing", "beach_woman": "happy", "beach_kid": "grinning"}
POSES = {
    "senior_a": (("standing", dict(arm_r="hip", arm_l="down", yaw=-0.2)),
                 ("pointing", dict(yaw=0.6, expr="determined", arm_r="point", arm_l="hip", head_roll=4)),
                 ("startled", dict(yaw=-0.3, expr="shocked", fx=["sweat"], arm_r="shrug", arm_l="shrug", legs="wide", squash=(0.97, 1.04), head_roll=-7))),
    "senior_b": (("standing", dict(arm_r="behind", arm_l="behind", yaw=0.2, expr="smug")),
                 ("pointing", dict(yaw=-0.6, expr="talking", arm_l="point", arm_r="hip", head_roll=-6)),
                 ("startled", dict(yaw=0.3, expr="shocked", fx=["sweat"], arm_r="raised", arm_l="raised", legs="wide", squash=(0.96, 1.05)))),
    "clerk": (("standing, mug", dict(yaw=0.3, arm_r=dict(preset="forward", hand=(0.45, 0.80)), prop_r="mug", arm_l="down", expr="smirk")),
              ("pointing", dict(yaw=0.7, expr="excited", arm_r="point", arm_l=dict(preset="forward"), prop_l=dict(type="newspaper", angle=-70))),
              ("startled", STORY_EXT["clerk_runs_in"][1])),
    "beach_man": (("standing", dict(arm_r="akimbo", arm_l="akimbo", expr="smirk")),
                  ("shading the eyes", STORY_EXT["father_looks"][1]),
                  ("startled", dict(yaw=0.5, expr="shocked", fx=["sweat"], arm_r="raised", arm_l="shrug", legs=dict(preset="step", stride=-0.6), lean=-8))),
    "beach_woman": (("standing", dict(arm_r="hip", arm_l="down", yaw=-0.25, expr="happy")),
                    ("shading the eyes", dict(yaw=0.6, pitch=-0.2, expr="neutral", arm_r="shade", arm_l="down")),
                    ("startled", dict(yaw=-0.4, expr="shocked", fx=["sweat"], arm_r="chin", arm_l="shrug", legs="narrow", head_roll=-8))),
    "beach_kid": (("standing, bucket", STORY_EXT["kid_bucket"][1]),
                  ("pointing out to sea", dict(yaw=0.7, expr="excited", arm_r="point", arm_l="down", prop_l="bucket")),
                  ("startled", dict(yaw=-0.2, expr="shocked", fx=["sweat"], arm_r="raised", arm_l="raised", legs="wide", squash=(0.95, 1.06)))),
}
BGS = {"senior_a": (WALL_LIT, WALL_SHADE), "senior_b": (WALL_SHADE, WALL_LIT), "clerk": (WALL_LIT, WALL_SHADE),
       "beach_man": (SAND, SKY), "beach_woman": (SKY, SAND), "beach_kid": (SAND, SEA)}


def build_sheet():
    cw, ch = 270, 560
    W = cw * 10
    o = []
    uid = [0]

    def nid():
        uid[0] += 1
        return "e%d" % uid[0]

    y = 0
    for name in NEW:
        b0, b1 = BGS[name]
        office = name in ("senior_a", "senior_b", "clerk")
        ground = OFFICE_FLOOR if office else SAND
        sea_band = (not office)
        cells = []
        for yw, nm in VIEWS:
            cells.append(("full", "%s %s" % (name, nm), dict(yaw=yw, arm_r="down", arm_l="down", expr="neutral")))
        for ex, extra in EXPRS:
            e = AMUSED.get(name, ex) if ex == "smug" else ex
            p = dict(expr=e)
            p.update(extra)
            cells.append(("head", "%s: %s" % (name, e), p))
        for nm, p in POSES[name]:
            cells.append(("full", "%s: %s" % (name, nm), p))
        for i, (kind, lab, p) in enumerate(cells):
            x0 = i * cw
            bg = b0 if i % 2 == 0 else b1
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, cw, ch, bg))
            if kind == "full":
                fl = y + ch - 50
                if sea_band:
                    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, fl - 120, cw, 70, SEA))
                o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, fl - 50, cw, ch - (fl - 50 - y), ground))
                o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y, cw, ch, x0, y, cw, ch))
                g, f = _place(name, p, nid(), 120, x0 + cw / 2, fl, shadow=0.9)
                o.append(g + "</svg>")
            else:
                o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d">' % (x0, y, cw, ch, cw, ch))
                g, f = _place(name, p, nid(), 210, cw / 2, ch * 0.42, anchor="head")
                o.append(g + "</svg>")
            o.append(LABEL(x0 + 8, y + 20, lab, 14))
        y += ch
    H = y
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, H, W, H, "".join(o)), W, H


LINEUP = ("hero", "boss", "senior_a", "senior_b", "clerk", "beach_man", "beach_woman", "beach_kid")
LINEUP_POSE = {"hero": dict(arm_l="hip", yaw=0.2), "boss": dict(arm_r="hip", yaw=-0.2), "senior_a": dict(arm_r="hip", yaw=0.2),
               "senior_b": dict(arm_r="behind", arm_l="behind", yaw=-0.15), "clerk": dict(yaw=0.2), "beach_man": dict(arm_r="akimbo", yaw=-0.1),
               "beach_woman": dict(arm_l="hip", yaw=0.2), "beach_kid": dict(prop_r="bucket", yaw=-0.2)}


def build_lineup():
    o = []
    y = 0
    W = 0
    n = 0
    for D in (110, 220):
        for bg, ground, nm in ((WALL_LIT, OFFICE_FLOOR, "office wall %s" % WALL_LIT), (SAND, SAND, "sand %s" % SAND)):
            step = int(1.25 * D)
            h = int(4.25 * D)
            w = step * len(LINEUP) + int(0.6 * D)
            W = max(W, w)
            o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y, 2 * 1400, h, bg))
            if ground != bg:
                o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y + h - int(0.35 * D), 2 * 1400, int(0.35 * D), ground))
            for i, c in enumerate(LINEUP):
                n += 1
                g, f = _place(c, dict(LINEUP_POSE[c], expr="neutral"), "l%d" % n, D, int(0.3 * D) + step * i + step / 2, y + h - int(0.2 * D), shadow=0.9)
                o.append(g)
                o.append(LABEL(int(0.3 * D) + step * i + 6, y + 18, c, 13))
            o.append(LABEL(8, y + h - 8, "%s, head D = %d px" % (nm, D), 14))
            y += h
    W = max(W, 1400)
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, y, W, y, "".join(o)), W, y


def _write_raster(svg, w, h, base, scale=1):
    sp = os.path.join(HERE, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(HERE, base + ".png")
    rc = P._raster(sp, out, w, h, scale)
    print("%s -> %s (%dx%d) rc=%d" % (sp, out, w, h, rc))
    return out


def canvas_check(verbose=True):
    """bbox of a wide pose range relative to the feet, per new member (used to set CANVAS); returns {name: (canvas, clipped)}."""
    res = {}
    for name in NEW:
        poses = [{}]
        for a in sorted(P.ARM_PRESETS[NEW_CAST[name]["build"]]):
            for pr in (None, "pencil", "eraser", "paper", "bucket", "newspaper", "forecast", "mug"):
                poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
                poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
        poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep"), dict(yaw=1.2), dict(yaw=-1.2)]
        x0 = y0 = 1e9
        x1 = y1 = -1e9
        for p in poses:
            f = P.figure(name, p, "c")
            fx, fy = f["anchors"]["feet"][0], f["feet_y"]
            b = f["bbox"]
            x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
        c = CANVAS[name]
        clipped = x0 < c[0] or y0 - 0.30 < c[1] or x1 > c[2] or y1 > c[3]
        res[name] = ((x0, y0, x1, y1), clipped)
        if verbose:
            print("%-12s pose range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok"))
    return res


def run_tests(quick=True):
    import test_puppet as T
    T.CASTS = NEW
    rc = T.main(["--quick"] if quick else [])
    canvas_check()
    return rc


def main(argv):
    cmd = argv[0] if argv else "sheet"
    if cmd == "sheet":
        svg, W, H = build_sheet()
        _write_raster(svg, W, H, "sheet")
    elif cmd == "lineup":
        svg, W, H = build_lineup()
        _write_raster(svg, W, H, "lineup")
    elif cmd == "test":
        return run_tests("--full" not in argv)
    elif cmd == "canvas":
        canvas_check()
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
