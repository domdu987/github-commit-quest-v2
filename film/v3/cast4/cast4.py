#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast4.py -- the cast of film 4 ("the drunk pagoda", old Japan) for the v2 puppet, as an extension module.

    import sys; sys.path.insert(0, ".../v3/cast4"); import cast4      # registers on import (idempotent); imports cast3/cast2/cast_ext
    import puppet                                                     # the same module object, now with the new members
    f = puppet.figure("kenta", cast4.STORY4["kenta_hammer"][1], "k")

Nothing in v2/puppet, v3/cast, v3/cast2 or v3/cast3 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  happi, kimono, mastercoat                         (dispatch: CAST[name]["costume"])
    cast_ext.HATS      hachimaki, squarecap, chonmage, hairbun, sugegasa  (dispatch: CAST[name]["hat_style"])
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps two puppet helpers on top of cast3's wrappers (each falls through for everything it does not handle):
    _ink_limb   kimono sleeves on the arms (CAST key "ksleeve": wide sleeve whose bag hangs under the arm), short trousers /
                leggings on the legs (CAST key "shorts"), straw sandals (CAST key "sandals")
    _prop       mallet, chain, chain_up, plank, plaster_trowel, lantern2
New cast:  kenta, master, merchant, woman2, farmer.
STORY4 / STORY4_META: the story poses (see API.md).  rubble_svg(): the pile of tower timber the master stands on.

Command line (QA):  python3 test_cast4.py        lineup.png, poses.png, canvas + head_flip checks, robustness run
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
for _d in (os.path.join(PROJ, "v3", "cast3"), os.path.join(PROJ, "v3", "cast2"), os.path.join(PROJ, "v3", "cast")):
    if _d not in sys.path:
        sys.path.insert(0, _d)
import cast3 as C3      # noqa: E402  (v3/cast3, read-only; imports cast2, cast_ext and v2/puppet)
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW4 = ("kenta", "master", "merchant", "woman2", "farmer")
TT = P.TORSO_TOP
_clamp, _rot = P._clamp, P._rot
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_O4 = {}                      # the helpers this module wrapped


def _cur():
    return CE._CUR[0]


# ============================================================================= geometry helpers
def _hull(pts):
    """convex hull (monotone chain), counter-clockwise; continuous in its input points."""
    p = sorted(set((round(a, 6), round(b, 6)) for a, b in pts))
    if len(p) < 3:
        return p

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in p:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(p):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def _arm_part(S, E, H, kk, frac):
    """points of the rubber-hose centre line from the root up to `frac` of its length, plus the unit tangent at the end."""
    pts = C3._limb_pts(S, E, H, kk)
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1]
    if tot < 1e-6:
        return None, None, 0.0
    L = frac * tot
    sel = [pts[0]]
    for i in range(1, len(pts)):
        if cum[i] >= L:
            f = (L - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            sel.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f))
            break
        sel.append(pts[i])
    a, e = (sel[-2] if len(sel) > 1 else S), sel[-1]
    tx, ty = e[0] - a[0], e[1] - a[1]
    tl = math.hypot(tx, ty)
    tan = (tx / tl, ty / tl) if tl > 1e-9 else (0.0, 1.0)
    return sel, tan, L


# ============================================================================= kimono sleeves, short trousers, sandals
def _ksleeve(k, S, E, H, kk, SL):
    """wide kimono / happi sleeve over the first SL["len"] of the arm: a tube SL["w"] wide along the rubber hose plus the sleeve
    bag hanging under it (convex hull of the outer half of the tube and the same points dropped by SL["drop"] x how horizontal
    the arm is), ink outline round the merged shape, a lining band at the opening.  roll=True: tied-up work sleeve (no bag)."""
    sel, tan, L = _arm_part(S, E, H, kk, SL.get("len", 0.5))
    if sel is None or len(sel) < 2:
        return ""
    sw = SL.get("w", 0.16)
    hw = sw / 2.0
    col, dk = k.c(SL["color"]), k.c(SL.get("dark", P._shade(SL["color"], 0.7)))
    d = "M" + " L".join("%.4f,%.4f" % p for p in sel)
    end = sel[-1]
    nx, ny = -tan[1], tan[0]
    drop = 0.0 if SL.get("roll") else SL.get("drop", 0.12) * (0.25 + 0.75 * abs(tan[0]))
    o = []
    hull = None
    if drop > 0.0:
        n = len(sel)
        bag = []
        for p in sel[n // 3:]:
            for s in (-1, 1):
                q = (p[0] + s * nx * hw, p[1] + s * ny * hw)
                bag.append(q)
                bag.append((q[0], q[1] + drop))
        hull = _hull(bag)
        if len(hull) >= 3:
            hd = P._smooth_closed(hull) if len(hull) >= 4 else _poly_d(hull)
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (hd, col, k.ink))
        else:
            hull = None
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, k.ink, sw + 0.034))
    if hull:
        o.append('<path d="%s" fill="%s"/>' % (hd, col))
        # the fold where the bag hangs from the sleeve
        m = sel[len(sel) * 2 // 3]
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>'
                 % (m[0], m[1] + hw * 0.4, m[0] + tan[0] * 0.05, m[1] + hw + drop * 0.5, end[0], end[1] + hw * 0.5 + drop * 0.6, dk))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, col, sw))
    if L > 0.12:
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.55" transform="translate(%.4f %.4f)"/>'
                 % ("M" + " L".join("%.4f,%.4f" % p for p in (sel[1:-1] or sel)), dk, hw * 0.45, hw * 0.25))
    # opening: lining band across the end (white edge for the happi, cuff roll for tied-up sleeves)
    cw = hw + (0.022 if SL.get("roll") else 0.006)
    cl = 0.07 if SL.get("roll") else 0.035
    c0 = (end[0] - tan[0] * cl, end[1] - tan[1] * cl)
    cuff = [(c0[0] + nx * cw, c0[1] + ny * cw), (end[0] + nx * cw, end[1] + ny * cw), (end[0] - nx * cw, end[1] - ny * cw), (c0[0] - nx * cw, c0[1] - ny * cw)]
    if SL.get("roll"):
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(cuff), k.c(SL.get("cuff", SL["color"])), k.ink))
    else:
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(cuff), k.c(SL.get("cuff", SL["color"])), k.ink))
    for p in (S, end):
        k.ext.append((p[0], p[1], hw + 0.03))
    if hull:
        for p in hull:
            k.ext.append((p[0], p[1], 0.02))
    return "".join(o)


def _sandal(k, A, T, w, SD):
    """waraji: flat straw sole under the foot (heel to toe on the sole line), two cream straps over the foot, a cord at the ankle."""
    tx = T[0] - A[0]
    s = 1.0 if tx >= 0 else -1.0
    a = min(1.0, abs(tx) / P.FOOT_LEN)
    sole = A[1] + w / 2 + 0.008
    heel = A[0] - s * (0.055 + 0.01 * a)
    tip = A[0] + s * (0.055 + 0.13 * a)
    th = 0.032
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (heel, sole - th / 2, tip, sole - th / 2, k.ink, th + 0.022),
         '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (heel, sole - th / 2, tip, sole - th / 2, k.c(SD.get("color", "#c9a35c")), th)]
    # straw weave ticks
    n = 4
    tk = "".join("M%.4f,%.4f l0,%.4f " % (heel + (tip - heel) * (i + 0.5) / n, sole - th + 0.006, th - 0.012) for i in range(n))
    o.append('<path d="%s" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % (tk, k.c(SD.get("dark", "#8a6a34"))))
    st = k.c(SD.get("strap", "#efe6d0"))
    xm = A[0] + s * 0.035 * (0.4 + a)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>'
             % (A[0] - s * 0.03, A[1] - 0.025, xm + s * 0.04, sole - th, A[0] + s * 0.03, A[1] - 0.03, heel + s * 0.01, sole - th, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
             % (A[0] - s * 0.03, A[1] - 0.025, xm + s * 0.04, sole - th, A[0] + s * 0.03, A[1] - 0.03, heel + s * 0.01, sole - th, st))
    k.ext.append((tip + s * 0.02, sole - 0.01, 0.01))
    k.ext.append((heel - s * 0.02, sole - 0.01, 0.01))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O4["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = _cur()
    if C is None or not C.get("_cast4"):
        return out
    if tail is None:
        if C.get("ksleeve"):
            out += _ksleeve(k, S, E, H, kk, C["ksleeve"])
    else:
        if C.get("shorts"):
            out += C3._sleeve(k, S, E, H, 0.55, w, C["shorts"])
        if C.get("sandals"):
            out += _sandal(k, H, tail, w, C["sandals"])
    return out


# ============================================================================= costumes (torso-local)
def _collar_y(k, X, col, y0, y1, xs, band=0.052, cross=0.80, under=None):
    """kimono collar worn left over right, seen from the front: a 'y' -- the short stroke from the viewer's upper left to the
    crossing, the long stroke from the viewer's upper right down past it to the left.  under: fill of the V above the crossing."""
    o = []
    xc, yc = X(-0.02, cross)
    if under:
        o.append(_poly(k, [X(-xs, y0), X(xs, y0), (xc, yc)], k.c(under), 0.0, "none"))
    a, b = X(-xs, y0), (xc + 0.02, yc + 0.02)
    o.append(_ln([a, b], k.ink, band + 0.026))
    o.append(_ln([a, b], k.c(col), band))
    c, d = X(xs, y0), X(-0.30, y1)
    o.append(_ln([c, d], k.ink, band + 0.026))
    o.append(_ln([c, d], k.c(col), band))
    return "".join(o)


def _obi(k, X, a, y, h, col, dark, knot=None):
    """sash round the waist (y = centre), h high, slightly curved; knot: None, 'cord' (thin cord with a bow) or 'flat'."""
    o = ['<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
         % (X(-a - 0.012, y - h / 2) + X(0, y - h / 2 + 0.02) + X(a + 0.012, y - h / 2) + X(a + 0.012, y + h / 2) + X(0, y + h / 2 + 0.02)
            + X(-a - 0.012, y + h / 2) + (k.c(col), k.ink))]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (X(-a, y + h * 0.28) + X(0, y + h * 0.28 + 0.02) + X(a, y + h * 0.28) + (k.c(dark),)))
    if knot == "cord":
        kx, ky = X(0.02, y + 0.012)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>'
                 % (X(-a, y + 0.005) + (kx, ky + 0.02) + X(a, y + 0.005) + (k.c(dark),)))
        for s in (-1, 1):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.024" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%d %.4f %.4f)"/>'
                     % (kx + s * 0.035, ky, k.c(dark), k.ink, s * 20, kx + s * 0.035, ky))
    return "".join(o)


def _pattern(k, C, m, col):
    """kimono cloth pattern: 'stripe' (thin vertical pinstripes) or 'flower' (five-dot blossoms + dots), in user space under the
    torso clip; it slides with the costume centre line (m.c)."""
    u = k.uid
    kind = col.get("pattern")
    if kind == "stripe":
        k.defs.append('<pattern id="%s_ks" width="0.075" height="1" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                      '<rect x="0.030" width="0.012" height="1" fill="%s"/></pattern>' % (u, m.c, k.c(col["pat"])))
        return "url(#%s_ks)" % u
    if kind == "flower":
        pc, pd = k.c(col["pat"]), k.c(col.get("pat2", col["pat"]))
        fl = "".join('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s"/>' % (0.08 + 0.03 * math.cos(i * 1.2566), 0.08 + 0.03 * math.sin(i * 1.2566), pc) for i in range(5))
        fl += '<circle cx="0.08" cy="0.08" r="0.013" fill="%s"/>' % pd
        fl += '<circle cx="0.21" cy="0.20" r="0.012" fill="%s"/>' % pc
        k.defs.append('<pattern id="%s_kf" width="0.26" height="0.26" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0) rotate(8)">%s</pattern>'
                      % (u, m.c, fl))
        return "url(#%s_kf)" % u
    return None


def _cos_happi(k, C, m):
    """kenta: short indigo happi jacket closed left over right, white collar bands, white 'maru ni igeta' crest (well-frame in a
    ring) on the chest, rust cord belt, the jacket skirt over the hips with two white bands near the hem; short trousers below."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    o.append(_collar_y(k, X, col["collar"], 0.39, yb + 0.06, 0.15, band=0.050, cross=0.66, under=col["under"]))
    # crest on the viewer's right chest
    cx, cy = X(0.20, 0.68)
    r = 0.075
    cw = k.c(col["crest"])
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.020"/>' % (cx, cy, r, cw))
    g = 0.026
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
             % (cx - g, cy - 0.050, cx - g, cy + 0.050, cx + g, cy - 0.050, cx + g, cy + 0.050, cx - 0.050, cy - g, cx + 0.050, cy - g,
                cx - 0.050, cy + g, cx + 0.050, cy + g, cw))
    inside = "".join(o)
    yt = TT + 0.66 * h
    a = m.hwa * 0.985
    hem = yB + C.get("jacket_len", 0.12)
    b = m.hwa + C.get("jacket_flare", 0.06)
    gr = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "hp", X, yt, a, hem, b, gr, sw=0.026, folds=((-0.10, yt + 0.08, -0.13, hem - 0.03),), fold_col=k.c(col["dark"]))]
    for dy in (0.055, 0.095):
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018"/>'
                  % (X(-b + 0.018, hem - dy) + X(0, hem - dy + 0.022) + X(b - 0.018, hem - dy) + (k.c(col["crest"]),)))
    # the collar band continues down the front edge of the top panel
    ov.append(_ln([X(-0.20, yt - 0.01), X(-0.24, hem + 0.01)], k.ink, 0.074))
    ov.append(_ln([X(-0.20, yt - 0.01), X(-0.24, hem + 0.01)], k.c(col["collar"]), 0.048))
    ov.append(_obi(k, X, a, yt + 0.01, 0.06, col["belt"], col["belt_d"], knot="cord"))
    return inside, "", "".join(ov)


def _cos_kimono(k, C, m):
    """townspeople: kimono worn left over right ('y' collar in a contrast colour, under-kimono V at the throat), cloth pattern
    (stripe / flower / plain), obi sash (wide with a cord for the woman), skirt to the ankles (kimono_len='long') or to mid-thigh
    (farmer's work kimono); optional money pouch (kinchaku) hanging from the obi (colors["pouch"])."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    pat = _pattern(k, C, m, col)
    o = []
    if pat:
        o.append('<rect x="-0.8" y="0.3" width="1.6" height="1.5" fill="%s" opacity="%.2f"/>' % (pat, col.get("pat_op", 0.8)))
    o.append(CE._bowl(k, col["pants"], yb, yB))
    o.append(_collar_y(k, X, col["collar"], 0.39, yB, 0.16, band=0.048, cross=0.70, under=col["under"]))
    inside = "".join(o)
    obi_h = C.get("obi_h", 0.09)
    yt = TT + C.get("obi_y", 0.66) * h
    a = m.hwa * 0.975
    if C.get("kimono_len", "long") == "long":
        hem = yB - 0.04 + C["leg"] * C.get("hem_frac", 0.80)
    else:
        hem = yB + C.get("kimono_len", 0.20)
    b = m.hwa + C.get("skirt_flare", 0.07)
    g = "url(#%s_tg)" % k.uid
    folds = ((-0.16, yt + 0.20, -0.22, hem - 0.06), (0.20, yt + 0.20, 0.26, hem - 0.06))
    ov = [C2._skirt(k, "km", X, yt, a, hem, b, g, sw=0.030, folds=folds, fold_col=k.c(col["dark"]))]
    if pat:
        u = k.uid
        rp, hp, lp = C2._skirt_pts(X, yt, a, hem, b)
        k.defs.append('<clipPath id="%s_kk"><path d="%s Z"/></clipPath>' % (u, P._smooth_open(rp + hp + lp)))
        ov.append('<g clip-path="url(#%s_kk)"><rect x="-1.2" y="%.4f" width="2.4" height="%.4f" fill="%s" opacity="%.2f"/></g>'
                  % (u, yt - 0.05, hem - yt + 0.1, pat, col.get("pat_op", 0.8)))
    # the top panel's front edge runs down the skirt to the hem (viewer's left of the centre)
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
              % (X(-0.10, yt) + X(-0.13, (yt + hem) / 2) + X(-0.16, hem + 0.02) + (k.c(col["dark"]),)))
    if col.get("hem"):
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030"/>'
                  % (X(-b + 0.02, hem - 0.035) + X(0, hem - 0.005) + X(b - 0.02, hem - 0.035) + (k.c(col["hem"]),)))
    ov.append(_obi(k, X, a, yt, obi_h, col["obi"], col["obi_d"], knot=C.get("obi_knot")))
    if C.get("obi_cord"):
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
                  % (X(-a, yt + 0.004) + X(0, yt + 0.026) + X(a, yt + 0.004) + (k.c(C["obi_cord"]),)))
        ov.append(_circ(X(0.0, yt + 0.016), 0.022, k.c(C["obi_cord"]), k, 0.008))
    if col.get("pouch"):
        # kinchaku: drawstring purse on a cord tucked into the obi (viewer's right), a gold coin mark on it
        px, py = X(0.24, yt + obi_h / 2)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012"/>' % (px, py, px + 0.01, py + 0.07, k.ink))
        bag = [(px - 0.035, py + 0.07), (px + 0.055, py + 0.07), (px + 0.10, py + 0.17), (px + 0.075, py + 0.235), (px - 0.055, py + 0.235), (px - 0.08, py + 0.17)]
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (P._smooth_closed(bag), k.c(col["pouch"]), k.ink))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
                  % (px - 0.04, py + 0.085, px + 0.01, py + 0.10, px + 0.06, py + 0.085, k.c(col["pouch_d"])))
        ov.append('<circle cx="%.4f" cy="%.4f" r="0.026" fill="%s" stroke="%s" stroke-width="0.008"/>' % (px + 0.01, py + 0.165, k.c("#e2b84a"), k.ink))
        ov.append('<rect x="%.4f" y="%.4f" width="0.014" height="0.014" fill="%s"/>' % (px + 0.003, py + 0.158, k.c(col["pouch_d"])))
        k.ext.append((px + 0.10, py + 0.24, 0.02))
    return inside, "", "".join(ov)


def _cos_mastercoat(k, C, m):
    """master: long dark-brown coat open over a grey kimono -- grey strip down the middle with the 'y' collar and a black obi,
    dark coat lapel bands down both front edges to the hem, white family crests on the coat's chest; coat to the ankles."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    kw = 0.24
    o = [CE._bowl(k, col["pants"], yb, yB)]
    o.append(_poly(k, [X(-kw, 0.36), X(kw, 0.36), X(kw + 0.02, yB + 0.1), X(-kw - 0.02, yB + 0.1)], k.c(col["kimono"]), 0.0, "none"))
    o.append(_collar_y(k, X, col["collar"], 0.39, yB, 0.13, band=0.046, cross=0.66, under=col["under"]))
    for s in (-1, 1):
        o.append(_ln([X(s * (kw - 0.005), 0.37), X(s * (kw + 0.02), yB + 0.1)], k.ink, 0.082))
        o.append(_ln([X(s * (kw - 0.005), 0.37), X(s * (kw + 0.02), yB + 0.1)], k.c(col["lapel"]), 0.058))
        c = X(s * 0.43, 0.62)
        o.append('<circle cx="%.4f" cy="%.4f" r="0.042" fill="none" stroke="%s" stroke-width="0.012"/>' % (c[0], c[1], k.c(col["crest"])))
        o.append('<path d="M%.4f,%.4f l0,-0.03 M%.4f,%.4f l-0.026,0.016 M%.4f,%.4f l0.026,0.016" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                 % (c[0], c[1], c[0], c[1], c[0], c[1], k.c(col["crest"])))
    yo = TT + 0.70 * h
    o.append(_poly(k, [X(-kw + 0.03, yo - 0.05), X(kw - 0.03, yo - 0.05), X(kw - 0.03, yo + 0.05), X(-kw + 0.03, yo + 0.05)], k.c(col["obi"]), 0.014))
    inside = "".join(o)
    yt = TT + 0.72 * h
    a = m.hwa * 0.975
    hem = yB - 0.04 + C["leg"] * C.get("hem_frac", 0.82)
    b = m.hwa + C.get("skirt_flare", 0.08)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "mc", X, yt, a, hem, b, g, sw=0.032,
                    folds=((-0.30, yt + 0.25, -0.40, hem - 0.06), (0.32, yt + 0.25, 0.42, hem - 0.06)), fold_col=k.c(col["dark"]))]
    # grey kimono strip down the opening, the lapel bands either side
    gk = [X(-kw + 0.01, yt), X(kw - 0.01, yt), X(kw + 0.05, hem + 0.02), X(-kw - 0.05, hem + 0.02)]
    ov.append(_poly(k, gk, k.c(col["kimono"]), 0.0, "none"))
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" opacity="0.7"/>' % (X(-0.02, yt + 0.02) + X(-0.05, hem) + (k.c(col["kimono_d"]),)))
    for s in (-1, 1):
        ov.append(_ln([X(s * (kw - 0.005), yt), X(s * (kw + 0.055), hem + 0.01)], k.ink, 0.082))
        ov.append(_ln([X(s * (kw - 0.005), yt), X(s * (kw + 0.055), hem + 0.01)], k.c(col["lapel"]), 0.058))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round" opacity="0.45"/>'
              % (X(-a * 0.85, yt + 0.10) + X(-b * 0.92, (yt + hem) / 2) + X(-b * 0.93, hem - 0.10) + (k.c(col["sheen"]),)))
    # coat tie cords at the chest (himo), hanging over the opening
    cy = 0.80
    for s in (-1, 1):
        ov.append(_ln([X(s * (kw + 0.01), cy), X(s * 0.05, cy + 0.06)], k.c(col["himo"]), 0.020))
    ov.append(_circ(X(0.0, cy + 0.07), 0.034, k.c(col["himo"]), k, 0.010))
    ov.append(_ln([X(-0.01, cy + 0.10), X(-0.02, cy + 0.22)], k.c(col["himo"]), 0.016))
    ov.append(_ln([X(0.02, cy + 0.10), X(0.04, cy + 0.20)], k.c(col["himo"]), 0.016))
    return inside, "", "".join(ov)


COSTUMES4 = {"happi": _cos_happi, "kimono": _cos_kimono, "mastercoat": _cos_mastercoat}


# ============================================================================= hats (head frame)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hair_dome(k, C, dx, yb, top, spikes=0, col=None):
    """hair over the crown down to yb (head frame): a dome with an optional spiky top."""
    hc = k.c(col or C["hair"]["color"])
    xl, xr = -0.475 + dx, 0.475 + dx
    pts = [(xl, yb), (xl - 0.01, yb - 0.10), (dx - 0.36, top + 0.10)]
    if spikes:
        for i in range(spikes):
            t = (i + 0.5) / spikes
            x = dx - 0.30 + 0.60 * t
            yy = top - 0.02 * math.sin(math.pi * t)
            pts.append((x - 0.06, yy + 0.04))
            pts.append((x + 0.03 * (t - 0.5), yy - 0.075 - 0.03 * math.sin(math.pi * t)))
    else:
        pts.append((dx, top))
    pts += [(dx + 0.36, top + 0.10), (xr + 0.01, yb - 0.10), (xr, yb)]
    d = "M" + " L".join("%.4f,%.4f" % p for p in pts) + " Q%.4f,%.4f %.4f,%.4f Z" % (dx, yb + 0.03, xl, yb)
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (d, hc, k.ink),
            min(p[1] for p in pts))


def _hat_hachimaki(k, C, yaw):
    """kenta: spiky black hair over the crown, a white twisted headband round the forehead, knot on the back side (away from the
    face) with two short tails flicking out."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    hair, top = _hair_dome(k, C, dx, -0.22, -0.56, spikes=5)
    o.append(hair)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.32, -0.36, dx - 0.22, -0.50, dx - 0.05, -0.53, k.c(C["hair"].get("shine", "#5a5a70"))))
    yb = -0.235
    band = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (-0.485 + dx, yb - 0.05, dx, yb - 0.01, 0.485 + dx, yb - 0.05, 0.48 + dx, yb + 0.045, dx, yb + 0.085, -0.48 + dx, yb + 0.045))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    tw = "".join("M%.4f,%.4f l0.035,0.05 " % (dx + x, yb - 0.035 + 0.04 * (x / 0.45) ** 2) for x in (-0.36, -0.22, -0.08, 0.06, 0.20, 0.34))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (tw, k.c(col["dark"])))
    # knot + tails on the side away from the face
    s = -1.0 if yaw >= 0 else 1.0
    f = _clamp(0.35 + abs(yaw), 0.35, 1.0)
    kx, ky = s * (0.47 - 0.10 * (1 - f)) + dx, yb + 0.02
    for (ang, ln) in ((25.0, 0.22), (60.0, 0.18)):
        ex, ey = kx + s * ln * math.cos(math.radians(ang)) * f, ky + ln * math.sin(math.radians(ang))
        tail = [(kx, ky - 0.025), (ex + s * 0.02, ey - 0.02), (ex, ey + 0.025), (kx, ky + 0.025)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(tail), k.c(col["band"]), k.ink))
        k.ext.append((ex + s * 0.02, ey, 0.03))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.040" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, k.c(col["band"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((-0.50 + dx, -0.25), (0.50 + dx, -0.25), (dx, top - 0.02)))
    return "".join(o), (dx, top)


def _hat_squarecap(k, C, yaw):
    """master: square black cap -- a stiff box with a flat top and straight, slightly flaring sides, sitting on top of the head
    over a grey-haired brim line; a front fold and a corner edge that slides with yaw; no pin, no net, no stripes."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    ex = 0.16 * yaw                       # the visible side face: the box's front edge slides to the facing side
    yb, top = -0.30, -0.74
    hb, ht = 0.43, 0.36
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    box = [(-hb + dx, yb), (-ht + dx, top), (ht + dx, top), (hb + dx, yb)]
    g = CE._gradient(k, "ht", col, x0=-0.45, x1=0.45, mid=0.30)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (_poly_d(box), g, k.ink))
    # flat top seen slightly from below: a thin lighter band at the top edge
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>' % (-ht + dx + 0.03, top + 0.03, ht + dx - 0.03, top + 0.03, k.c(col["shine"])))
    # corner edge (front/side boundary)
    xe = dx + ex
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" opacity="0.85"/>' % (xe * 1.15, yb - 0.01, xe * 0.95, top + 0.01, k.c(col["edge"])))
    # front fold / seam and a stiff band at the bottom
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (dx - 0.22 + ex * 0.5, top + 0.06, dx - 0.26 + ex * 0.5, -0.50, dx - 0.30 + ex * 0.5, yb - 0.06, k.c(col["edge"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (-hb + dx - 0.01, yb - 0.065, hb + dx + 0.01, yb - 0.065, hb + dx + 0.015, yb + 0.012, -hb + dx - 0.015, yb + 0.012, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
             % (-hb + dx + 0.04, yb - 0.045, -0.05 + dx, yb - 0.045, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((-hb + dx - 0.03, yb), (hb + dx + 0.03, yb), (-ht + dx, top - 0.02), (ht + dx, top - 0.02)))
    return "".join(o), (dx, top)


def _hat_chonmage(k, C, yaw):
    """merchant: shaved pate (the white head shows on top), dark hair at the sides and back up to the temples, the folded topknot
    (mage) lying forward along the crown, tied with a white cord."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    hc = k.c(C["hair"]["color"])
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    for s in (-1, 1):
        g = _clamp(1.0 - 0.7 * max(0.0, s * yaw), 0.3, 1.0)
        x0 = s * 0.475 + dx
        side = [(x0 + s * 0.012, -0.04), (x0 + s * 0.018, -0.24), (x0 - s * 0.04 * g, -0.40), (x0 - s * 0.11 * g, -0.37), (x0 - s * 0.07 * g, -0.20), (x0 - s * 0.045 * g, -0.03)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(side), hc, k.ink))
        k.ext.append((x0 + s * 0.03, -0.25, 0.03))
    # the shaved pate: a faint blue-grey tone on the crown
    o.append('<path d="M%.4f,-0.41 Q%.4f,-0.53 %.4f,-0.41 Q%.4f,-0.36 %.4f,-0.41 Z" fill="%s" opacity="0.55"/>'
             % (dx - 0.30, dx, dx + 0.30, dx, dx - 0.30, k.c(col["pate"])))
    # topknot: folded tube from the back of the crown forward
    fx = 0.10 * yaw
    mx0, mx1 = dx - 0.10 + fx * 0.3, dx + 0.14 + fx
    knot = [(mx0 - 0.07, -0.43), (mx0 - 0.01, -0.53), (mx1 - 0.04, -0.585), (mx1 + 0.05, -0.60), (mx1 + 0.08, -0.565), (mx1 + 0.01, -0.53), (mx0 + 0.07, -0.44)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(knot), hc, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (mx0 - 0.005, -0.545, mx0 + 0.055, -0.475, k.c(col["cord"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
             % (mx0 + 0.07, -0.555, mx1 - 0.05, -0.60, mx1 + 0.05, -0.61, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((mx0 - 0.08, -0.43), (mx1 + 0.10, -0.61), (dx, -0.50)))
    return "".join(o), (mx1, -0.60)


def _hat_hairbun(k, C, yaw):
    """woman2: black hair swept up over the head into a big round bun on top (shimada-like), side wings over the ears, a red
    lacquered comb in front of the bun and a pair of short coral sticks (no long pin, no bead)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    bx = dx - 0.06 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    hc = k.c(C["hair"]["color"])
    # side wings
    for s in (-1, 1):
        g = _clamp(1.0 - 0.6 * max(0.0, s * yaw), 0.35, 1.0)
        x0 = s * 0.47 + dx
        wing = [(x0 - s * 0.10 * g, -0.36), (x0 + s * 0.06, -0.30), (x0 + s * 0.07, -0.12), (x0 + s * 0.01, -0.02), (x0 - s * 0.07 * g, -0.10)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(wing), hc, k.ink))
        k.ext.append((x0 + s * 0.09, -0.15, 0.03))
    # bun (drawn first: the front hair covers its base)
    o.append('<ellipse cx="%.4f" cy="-0.66" rx="0.24" ry="0.16" fill="%s" stroke="%s" stroke-width="0.026"/>' % (bx, hc, k.ink))
    o.append('<path d="M%.4f,-0.66 Q%.4f,-0.76 %.4f,-0.72" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (bx - 0.16, bx - 0.05, bx + 0.10, k.c(col["shine"])))
    for s in (-1, 1):
        o.append('<path d="M%.4f,-0.66 L%.4f,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (bx + s * 0.18, bx + s * 0.31, -0.74, k.ink))
        o.append('<path d="M%.4f,-0.66 L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (bx + s * 0.18, bx + s * 0.31, -0.74, k.c(col["stick"])))
    hair, top = _hair_dome(k, C, dx, -0.20, -0.54)
    o.append(hair)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.34, -0.30, dx - 0.26, -0.46, dx - 0.08, -0.50, k.c(col["shine"])))
    o.append('<path d="M%.4f,-0.21 Q%.4f,-0.33 %.4f,-0.48" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (dx + 0.12 * yaw + 0.05, dx + 0.12 * yaw, dx, k.c(col["shine"])))
    # comb
    o.append('<path d="M%.4f,-0.585 Q%.4f,-0.66 %.4f,-0.585 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (bx - 0.17, bx, bx + 0.17, k.c(col["comb"]), k.ink))
    o.append('<path d="M%.4f,-0.60 Q%.4f,-0.635 %.4f,-0.60" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (bx - 0.11, bx, bx + 0.11, k.c(col["comb_l"])))
    o.append('</g>')
    _ext_hat(k, C, ((bx - 0.33, -0.76), (bx + 0.33, -0.76), (bx, -0.83)))
    return "".join(o), (bx, -0.82)


def _hat_sugegasa(k, C, yaw):
    """farmer: wide shallow conical straw hat (1.46 D), radial straw lines, a darker rim, a small knob at the apex, and a chin
    cord down both sides of the face."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    ax = dx - 0.05 * yaw
    rx, yb, top = 0.73, -0.30, -0.70
    o = []
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014"/>'
                 % (s * 0.40 + dx, yb + 0.02, s * 0.44 + dx + 0.10 * yaw, 0.22, 0.12 * yaw + s * 0.06, 0.47, k.c(col["cord"])))
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    g = CE._gradient(k, "ht", col, x0=-rx, x1=rx, mid=0.35)
    cone = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - rx, yb, ax - 0.30, top + 0.12, ax, top, ax + 0.30, top + 0.12, dx + rx, yb, dx, yb + 0.07, dx - rx, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (cone, g, k.ink))
    ln = "".join("M%.4f,%.4f L%.4f,%.4f " % (ax, top + 0.03, dx + rx * f, yb + 0.035 * (1 - f * f)) for f in (-0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.011" opacity="0.75"/>' % (ln, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.85"/>'
             % (dx - rx + 0.08, yb - 0.04, ax - 0.30, top + 0.17, ax - 0.06, top + 0.04, k.c(col["shine"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>'
             % (dx - rx + 0.02, yb - 0.005, dx, yb + 0.06, dx + rx - 0.02, yb - 0.005, k.c(col["rim"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.030" fill="%s" stroke="%s" stroke-width="0.012"/>' % (ax, top - 0.005, k.c(col["dark"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - rx - 0.03, yb), (dx + rx + 0.03, yb), (ax, top - 0.05)))
    k.ext.append((0.12 * yaw, 0.49, 0.03))
    return "".join(o), (ax, top - 0.03)


HATS4 = {"hachimaki": _hat_hachimaki, "squarecap": _hat_squarecap, "chonmage": _hat_chonmage, "hairbun": _hat_hairbun, "sugegasa": _hat_sugegasa}


# ============================================================================= props
NEW_PROPS4 = ("mallet", "chain", "chain_up", "plank", "plaster_trowel", "lantern2")
# working point distance from the gripping hand (D): mallet = head centre, chain = bottom of the coil (hangs upright), chain_up =
# the hand (the chain is vertical), plank = far end, plaster_trowel = blade centre, lantern2 = centre of the paper body (upright)
NEW_TIP4 = {"mallet": 0.40, "chain": 0.40, "chain_up": 0.0, "plank": 1.05, "plaster_trowel": 0.32, "lantern2": 0.36}
CHAIN_UP, CHAIN_DOWN = 3.2, 0.55
PLANK_BACK = 0.55


def _chain_links(k, x, y0, y1):
    """a vertical chain from y0 to y1 at x: alternate face-on oval links and edge-on bars."""
    o = []
    n = max(1, int((y1 - y0) / 0.07))
    st = k.c("#8d939e")
    for i in range(n):
        y = y0 + i * (y1 - y0) / n
        if i % 2 == 0:
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.032" ry="0.050" fill="none" stroke="%s" stroke-width="0.030"/>' % (x, y + 0.035, k.ink))
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.032" ry="0.050" fill="none" stroke="%s" stroke-width="0.014"/>' % (x, y + 0.035, st))
        else:
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (x, y + 0.005, x, y + 0.065, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (x, y + 0.005, x, y + 0.065, k.c("#b8bec8")))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS4:
        return _O4["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    if kind == "chain_up":
        x, y = H
        top, bot = y - CHAIN_UP * sc, y + CHAIN_DOWN * sc
        o = [_chain_links(k, x, top, bot)]
        o.append('<circle cx="%.4f" cy="%.4f" r="0.030" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x, bot + 0.01, k.c("#5d636e"), ink))
        k.ext.append((x, y - 0.6, 0.05))
        k.ext.append((x, bot + 0.05, 0.05))
        return "".join(o), (x, y)
    if kind in ("chain", "lantern2"):
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        if kind == "chain":
            # a coil of chain hanging from the fist: three loops of links
            for (cx, cy, r) in ((-0.02, 0.21, 0.17), (0.03, 0.24, 0.15), (0.0, 0.26, 0.12)):
                d = "M0,0 C%.4f,%.4f %.4f,%.4f %.4f,%.4f S%.4f,%.4f 0,0" % (cx - r * 1.6, cy - r * 0.2, cx - r, cy + r, cx, cy + r, cx + r * 1.6, cy - r * 0.2)
                o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.052" stroke-linecap="round"/>' % (d, ink))
                o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-dasharray="0.045 0.018" stroke-linecap="butt"/>' % (d, k.c("#9aa1ac")))
            o.append('<path d="M0.02,0.30 L0.03,0.40" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % ink)
            o.append('<path d="M0.02,0.30 L0.03,0.40" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c("#9aa1ac"))
            ends = ((-0.30, 0.20), (0.30, 0.20), (0.0, 0.42))
        else:
            # chochin: paper lantern on a short cord, black lacquer caps, bamboo ribs, a red band, warm glow
            u = k.uid
            k.defs.append('<radialGradient id="%s_l2"><stop offset="0" stop-color="%s" stop-opacity="0.55"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
                          % (u, k.c("#ffcf7a"), k.c("#ff9a3a")))
            o.append('<circle cx="0" cy="0.36" r="0.40" fill="url(#%s_l2)"/>' % u)
            o.append('<path d="M0,0 L0,0.12" stroke="%s" stroke-width="0.014"/>' % ink)
            o.append('<path d="M-0.15,0.36 C-0.15,0.19 0.15,0.19 0.15,0.36 C0.15,0.53 -0.15,0.53 -0.15,0.36 Z" transform="translate(0 0) scale(1 1)" fill="%s" stroke="%s" stroke-width="0.016"/>'
                     % (k.c("#ffe7b0"), ink))
            o.append('<path d="M-0.13,0.30 Q0,0.29 0.13,0.30 M-0.148,0.36 L0.148,0.36 M-0.13,0.42 Q0,0.43 0.13,0.42" fill="none" stroke="%s" stroke-width="0.009" opacity="0.8"/>'
                     % k.c("#c88a40"))
            o.append('<path d="M-0.145,0.335 L0.145,0.335 L0.145,0.385 L-0.145,0.385 Z" fill="%s" opacity="0.85"/>' % k.c("#d0402e"))
            o.append('<rect x="-0.085" y="0.12" width="0.17" height="0.06" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#2a2228"), ink))
            o.append('<rect x="-0.085" y="0.54" width="0.17" height="0.05" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#2a2228"), ink))
            ends = ((-0.17, 0.36), (0.17, 0.36), (0.0, 0.60), (0.0, -0.01))
        o.append('</g>')
        for e in ends:
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0], H[1] + NEW_TIP4[kind] * sc)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind == "mallet":
        # kizuchi: wooden handle, a barrel-shaped wooden head across the handle's end, iron hoops round both faces
        o.append('<path d="M-0.08,-0.022 L0.34,-0.018 L0.34,0.018 L-0.08,0.024 Q-0.10,0 -0.08,-0.022 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#c99a5e"), ink))
        o.append('<path d="M-0.06,-0.007 L0.30,-0.006" stroke="%s" stroke-width="0.006" opacity="0.7"/>' % k.c("#e6c08a"))
        o.append('<path d="M0.33,-0.14 L0.47,-0.14 Q0.49,0 0.47,0.14 L0.33,0.14 Q0.31,0 0.33,-0.14 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#a8703e"), ink))
        for y in (-0.115, 0.115):
            o.append('<path d="M0.325,%.4f L0.475,%.4f" stroke="%s" stroke-width="0.022"/>' % (y, y, k.c("#5d636e")))
        o.append('<path d="M0.35,-0.09 L0.35,0.09" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % k.c("#d9a56a"))
        o.append('<path d="M0.42,-0.09 Q0.43,0 0.42,0.09" fill="none" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % k.c("#7a4a24"))
        ends = ((-0.10, 0.0), (0.48, -0.15), (0.48, 0.15), (0.32, -0.15), (0.32, 0.15))
    elif kind == "plank":
        # a sawn plank gripped 0.55 D from its back end: end grain on the far end, grain lines
        x0, x1 = -PLANK_BACK, NEW_TIP4["plank"]
        o.append('<path d="M%.4f,-0.050 L%.4f,-0.050 L%.4f,0.050 L%.4f,0.050 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (x0, x1, x1, x0, k.c("#d9b07a"), ink))
        o.append('<path d="M%.4f,-0.018 Q%.4f,-0.030 %.4f,-0.015 M%.4f,0.020 Q%.4f,0.010 %.4f,0.024" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>'
                 % (x0 + 0.05, (x0 + x1) / 2, x1 - 0.06, x0 + 0.10, (x0 + x1) / 2 + 0.1, x1 - 0.12, k.c("#a8763e")))
        o.append('<ellipse cx="%.4f" cy="0.006" rx="0.035" ry="0.016" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % ((x0 + x1) * 0.35, k.c("#a8763e")))
        o.append('<path d="M%.4f,-0.050 L%.4f,0.050" stroke="%s" stroke-width="0.020"/>' % (x1 - 0.012, x1 - 0.012, k.c("#b88a52")))
        o.append('<path d="M%.4f,-0.050 L%.4f,-0.050" stroke="#ffffff" stroke-width="0.010" opacity="0.4"/>' % (x0 + 0.03, x1 - 0.03))
        ends = ((x0, -0.06), (x0, 0.06), (x1, -0.06), (x1, 0.06))
    elif kind == "plaster_trowel":
        # kote: wooden grip, a gooseneck tang, a long flat steel blade with a pointed tip, white plaster on the blade
        o.append('<path d="M-0.08,-0.028 L0.08,-0.028 Q0.10,0 0.08,0.028 L-0.08,0.028 Q-0.10,0 -0.08,-0.028 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#9a6a3c"), ink))
        o.append('<path d="M0.08,0 Q0.12,0 0.13,0.025" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % ink)
        o.append('<path d="M0.12,0.020 L0.44,0.020 Q0.52,0.020 0.52,0.075 Q0.52,0.140 0.44,0.140 L0.12,0.140 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#aeb6c0"), ink))
        o.append('<path d="M0.14,0.036 L0.44,0.036" stroke="#ffffff" stroke-width="0.010" opacity="0.6"/>')
        o.append('<path d="M0.20,0.138 Q0.30,0.185 0.44,0.140 Q0.36,0.110 0.20,0.138 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#f4f1ea"), ink))
        ends = ((-0.10, 0.0), (0.52, 0.075), (0.12, 0.15), (0.44, 0.17))
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tip = NEW_TIP4[kind]
    tx, ty = _rot(tip * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


def rubble_svg(uid="rb", width=2.4, height=0.55, ink=P.INK, tint=None):
    """the pile of broken tower timber the master stands on at the end, as an SVG fragment in D units: the top of the pile
    (where the feet go) at (0, 0), its foot on the ground at y = height.  Beams, a snapped post with splinters, a few roof
    tiles.  Draw it at the figure's px per D, then plant the figure's feet at (0, 0) (STORY4_META["master_rubble_look"]["lift"])."""
    k = P._Ctx(str(uid), ink, P._rgb(tint) if P._is_hex(tint) else None)
    w, h = width / 2.0, height
    o = []
    mound = [(-w, h), (-w * 0.75, h * 0.55), (-w * 0.35, h * 0.12), (0.0, 0.0), (w * 0.40, h * 0.15), (w * 0.80, h * 0.62), (w, h)]
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_open(mound), k.c("#7a6050"), k.ink))
    beams = (((-w * 0.95, h * 0.85), (-w * 0.05, h * 0.25), 0.11, "#a8784a"), ((w * 0.95, h * 0.90), (w * 0.05, h * 0.18), 0.10, "#9a6a3e"),
             ((-w * 0.6, h * 0.40), (w * 0.55, h * 0.30), 0.09, "#b88a58"), ((-w * 0.35, h * 0.08), (w * 0.38, h * 0.02), 0.10, "#a8784a"))
    for (a, b, t, c) in beams:
        o.append(_ln([a, b], k.ink, t + 0.026))
        o.append(_ln([a, b], k.c(c), t))
        o.append(_ln([(a[0], a[1] - t * 0.25), (b[0], b[1] - t * 0.25)], k.c("#d9b07a"), 0.012, ' opacity="0.7"'))
    # snapped post with splinters, sticking up behind the feet
    px = w * 0.55
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (px - 0.07, h * 0.35, px - 0.08, -0.30, px - 0.03, -0.22, px, -0.36, px + 0.04, -0.25, px + 0.07, h * 0.35, k.c("#8a5a32"), k.ink))
    for (x, y) in ((-w * 0.70, h * 0.62), (-w * 0.30, h * 0.50), (w * 0.25, h * 0.55), (w * 0.70, h * 0.74)):
        o.append('<path d="M%.4f,%.4f q0.08,-0.05 0.16,0 l-0.02,0.045 q-0.06,-0.035 -0.12,0 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x, y, k.c("#5a5866"), k.ink))
    return '<g id="%s_rubble">%s</g>' % (k.uid, "".join(o))


# ============================================================================= cast
NEW_CAST4 = {
    # the hero: the carpenter's apprentice (0.8 of the adults): indigo happi with a white crest, white headband, short trousers, waraji
    "kenta": dict(
        _cast4=True, build="boy", seed=12.3,
        torso_w=0.64, torso_h=0.80, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.82, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.060, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a090",
        hat="newsboy", hat_style="hachimaki", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(band="#fbf8f0", dark="#b9b2a8"),
        hair=dict(color="#22202a", front=0.06, grow=0.18, shine="#55546a"),
        costume="happi", jacket_len=0.14, jacket_flare=0.07,
        ksleeve=dict(color="#2c3a72", dark="#1b2450", cuff="#f6f2ea", len=0.46, w=0.17, drop=0.07),
        shorts=dict(color="#5a4a3e", dark="#3a2e26", cuff="#6a584a", len=0.46, w=0.17),
        sandals=dict(color="#d0ab62", dark="#8a6a34", strap="#f2ead8"),
        colors=dict(base="#2c3a72", dark="#1b2450", collar="#f6f2ea", under="#e8dcc4", crest="#f8f6f0", belt="#b04a2c", belt_d="#7a2c18",
                    pants="#5a4a3e"),
    ),
    # the master builder: big, round, proud; square black cap, thick brows, long dark-brown coat open over a grey kimono
    "master": dict(
        _cast4=True, build="stout", seed=35.4,
        torso_w=1.24, torso_h=1.14, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.44, 0.44), arm=0.74, hip_x=0.17, leg=1.30, stance=0.06, wide=0.26, limb_w=0.070,
        eye_y=-0.010, brow="stroke", brow_th=0.082, mouth="frown", moustache=False, smirk_side=-1, cheeks="#ec8c7a",
        hat="newsboy", hat_style="squarecap", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#4a4448", base="#1f1b1e", dark="#0e0b0d", shine="#7a7278", edge="#5a5258", band="#2a2427"),
        hair=dict(color="#6a6468", front=0.07, grow=0.22),
        costume="mastercoat", hem_frac=0.80, skirt_flare=0.10,
        ksleeve=dict(color="#4f3322", dark="#2e1c12", cuff="#8e8a8c", len=0.78, w=0.22, drop=0.13),
        sandals=dict(color="#c49e5c", dark="#7a5a2c", strap="#2a2226"),
        colors=dict(base="#5a3a26", dark="#2e1c12", lapel="#2a1a10", kimono="#9a9aa2", kimono_d="#6a6a74", collar="#4a4a54", under="#d9d6dc",
                    obi="#1e1a1e", crest="#efe6d6", sheen="#8a6a50", himo="#c9a85a", pants="#3a3236"),
    ),
    # townspeople
    "merchant": dict(
        _cast4=True, build="regular", seed=29.9,
        torso_w=0.86, torso_h=1.02, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.18, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.020, brow="stroke", brow_th=0.044, mouth="smirk", moustache=False, smirk_side=1, cheeks="#f0a898",
        hat="newsboy", hat_style="chonmage", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(pate="#c9cfe0", cord="#f4f0e6", shine="#6a6670"),
        hair=dict(color="#2a2428", front=0.05, grow=0.18),
        costume="kimono", kimono_len="long", hem_frac=0.80, skirt_flare=0.07, obi_h=0.085,
        ksleeve=dict(color="#86888c", dark="#5a5c62", cuff="#2e3440", len=0.72, w=0.19, drop=0.12),
        sandals=dict(color="#c9a35c", dark="#8a6a34", strap="#3a2a2a"),
        colors=dict(base="#86888c", dark="#5a5c62", pattern="stripe", pat="#6a6c72", pat_op=0.8, collar="#2e3440", under="#e4e2dc",
                    obi="#6a4428", obi_d="#3e2614", pouch="#3f6a4a", pouch_d="#24402c", pants="#5a5c62"),
    ),
    "woman2": dict(
        _cast4=True, build="slim", seed=33.1,
        torso_w=0.58, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.225, 0.52), arm=0.72, hip_x=0.13, leg=1.14, stance=0.04, wide=0.20, limb_w=0.055,
        eye_y=0.050, brow="stroke", brow_th=0.030, mouth="smile", moustache=False, smirk_side=-1, lashes=True, cheeks="#f2a8b0",
        hat="newsboy", hat_style="hairbun", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(shine="#5a5a72", comb="#c8302a", comb_l="#f08a6a", stick="#f08a6a"),
        hair=dict(color="#1e1c26", front=0.10, grow=0.24),
        costume="kimono", kimono_len="long", hem_frac=0.86, skirt_flare=0.05, obi_h=0.16, obi_y=0.62, obi_cord="#f0c040",
        ksleeve=dict(color="#b44a64", dark="#7a2a40", cuff="#f6e8d8", len=0.74, w=0.18, drop=0.18),
        sandals=dict(color="#e2c890", dark="#a88a50", strap="#c8302a"),
        colors=dict(base="#b44a64", dark="#7a2a40", pattern="flower", pat="#f6e2d2", pat2="#f0c040", pat_op=0.9, collar="#f6e8d8",
                    under="#c8302a", obi="#2f7f78", obi_d="#1c5650", hem="#7a2a40", pants="#7a2a40"),
    ),
    "farmer": dict(
        _cast4=True, build="slim", seed=28.2,
        torso_w=0.66, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.74, hip_x=0.17, leg=1.30, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.040, brow="stroke", brow_th=0.046, mouth="dash", moustache=False, smirk_side=1, cheeks="#e89a84",
        hat="newsboy", hat_style="sugegasa", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#f0d890", base="#d6b462", dark="#9a7a36", shine="#fff0c0", rim="#8a6a2c", cord="#6a4a2a"),
        hair=dict(color="#2e2620", front=0.08, grow=0.20),
        costume="kimono", kimono_len=0.24, skirt_flare=0.08, obi_h=0.07, obi_knot="cord",
        ksleeve=dict(color="#6f7a4a", dark="#4a5230", cuff="#8a9460", len=0.42, w=0.15, roll=True),
        shorts=dict(color="#4a4a5a", dark="#30303c", cuff="#5a5a6a", len=0.80, w=0.11),
        sandals=dict(color="#c9a35c", dark="#8a6a34", strap="#efe6d0"),
        colors=dict(base="#6f7a4a", dark="#4a5230", collar="#3e4430", under="#d8cdb0", obi="#8a6a42", obi_d="#5a4224", pants="#4a4a5a"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast4.py canvas): every arm preset with
# mallet / chain / plank / plaster_trowel / lantern2 at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects and
# every STORY4 pose of the member; >= 0.32 D head room.  Wide in x because of the plank (1.05 D in front of the hand).
CANVAS4 = {
    "kenta": (-1.9375, -3.9375, 1.9375, 0.2500),
    "master": (-2.1875, -4.8750, 2.1875, 0.1875),
    "merchant": (-2.1250, -4.6250, 2.1250, 0.1875),
    "woman2": (-2.0625, -4.5625, 2.0625, 0.2500),
    "farmer": (-2.0625, -4.8125, 2.0625, 0.1250),
}


# ============================================================================= story poses
def _feet_y(cast, pose):
    return P.figure(cast, pose, "q")["feet_y"]


TOWN = (("merchant", ""), ("woman2", "_woman2"), ("farmer", "_farmer"))


def _story():
    S, M = {}, {}
    # --- kenta
    S["kenta_hammer"] = ("kenta", dict(yaw=0.6, pitch=0.35, expr="determined", head_roll=-4, lean=8,
                                       legs=dict(preset="wide", crouch=0.22, stride=0.3),
                                       arm_r=dict(hand=(0.46, -0.06), bend=-0.9, stretch=1.25), prop_r=dict(type="mallet", angle=-72),
                                       arm_l=dict(hand=(0.42, 0.78), bend=-0.3, stretch=1.2)))
    M["kenta_hammer"] = dict(note="mallet raised over the shoulder (wind-up); swap arm_r/prop_r with meta 'strike' for the blow: the "
                                  "mallet head (prop_tip_r) lands about 0.7 D in front at hip height",
                             strike=dict(arm_r=dict(hand=(0.55, 0.52), bend=-0.5, stretch=1.25), prop_r=dict(type="mallet", angle=40)))
    S["kenta_hang_chain"] = ("kenta", dict(yaw=0.6, pitch=-0.6, expr="determined", mouth="clench", head_roll=-6, lean=-8, gaze=(0.6, -0.8),
                                           legs=dict(preset="wide", crouch=0.12),
                                           arm_r=dict(hand=(0.64, -0.12), bend=-0.8, stretch=1.3),
                                           arm_l=dict(hand=(0.64, 0.20), bend=-0.4, stretch=1.3), prop_l="chain_up"))
    M["kenta_hang_chain"] = dict(note="both fists on a vertical chain hanging just right of his head (chain_up on the lower hand "
                                      "arm_l, the upper hand on the same x 0.32 D higher), leaning back, pulling it down; the chain is cut "
                                      "at the sprite canvas top: let the set's chain continue it. Chain x = 0.64 D right of the head")
    S["kenta_point_pagoda"] = ("kenta", dict(yaw=0.45, pitch=-0.5, expr="excited", head_roll=-6, gaze=(0.6, -0.8),
                                             arm_r=dict(hand=(0.62, -0.42), shape="point", bend=-0.8, stretch=1.3), arm_l="akimbo", legs="wide"))
    S["kenta_run_shout"] = ("kenta", dict(yaw=0.85, pitch=-0.2, expr="worried", mouth="talk_b", fx=["sweat"], lean=14, head_roll=-8,
                                          legs=dict(preset="step", stride=1.3, lift_l=0.9, knee_l=1.0, toe_r=1.0),
                                          arm_r=dict(hand=(0.56, 0.20), bend=-0.8, shape="open", stretch=1.2),
                                          arm_l=dict(hand=(-0.50, 0.85), bend=0.6, layer="back")))
    M["kenta_run_shout"] = dict(note="running to screen-right, the screen-right hand cupped beside the open mouth; "
                                     "alternate the stride sign for the second run frame")
    S["kenta_determined"] = ("kenta", dict(yaw=0.3, expr="determined", head_roll=-4, arm_l="akimbo", arm_r=dict(hand=(0.40, 0.98), bend=0.6),
                                           legs="wide", lean=2))
    S["kenta_worried"] = ("kenta", dict(yaw=-0.3, pitch=0.35, expr="worried", fx=["sweat"], head_roll=6,
                                        arm_r=dict(hand=(0.08, 0.84), bend=0.8), arm_l=dict(hand=(-0.04, 0.88), bend=0.8), legs="narrow"))
    # --- master
    S["master_laugh"] = ("master", dict(yaw=0.15, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], head_roll=14, lean=-6,
                                        head_dy=0.03, squash=(1.03, 0.97), t=0.3,
                                        arm_r=dict(hand=(0.30, 1.14), bend=0.9), arm_l=dict(hand=(-0.26, 1.18), bend=0.9), legs="wide"))
    M["master_laugh"] = dict(note="eyes closed (blink 2) and mouth wide; animate t for the tears")
    S["master_smug"] = ("master", dict(yaw=0.3, pitch=-0.35, expr="smug", head_roll=5, arm_r="akimbo", arm_l="akimbo"))
    S["master_arms_crossed"] = ("master", dict(yaw=-0.2, pitch=-0.3, expr="smug", head_roll=-4,
                                               arm_l=dict(hand=(0.34, 0.90), bend=0.5, sharp=0.3), arm_r=dict(hand=(-0.36, 0.84), bend=-0.5, sharp=0.3)))
    S["master_point_tower"] = ("master", dict(yaw=-0.35, pitch=-0.6, expr="smug", head_roll=-6, lean=-3, gaze=(-0.6, -0.8),
                                              arm_l=dict(hand=(-0.80, -0.62), shape="point", bend=-0.8, stretch=1.3), arm_r="akimbo", legs="wide"))
    M["master_point_tower"] = dict(note="points up-left at his tower (put it screen-left, or mirror=True)")
    S["master_pat_shoulder"] = ("master", dict(yaw=0.4, pitch=0.25, expr="grinning", head_roll=6, lean=3,
                                               arm_r=dict(hand=(0.92, 0.78), bend=-0.2, stretch=1.25), arm_l="akimbo"))
    M["master_pat_shoulder"] = dict(note="patronising pat: the screen-right hand rests on the shoulder of someone shorter on his right. "
                                         "Pin it on the stage: hands={'r': {'hand': <kenta shoulder world point>, 'stretch': 1.3}} "
                                         "(the hand ball sits on the shoulder top: target = kenta's shoulder anchor 0.06 D higher)")
    S["master_plaster"] = ("master", dict(yaw=0.6, pitch=0.0, expr="determined", head_roll=-3, lean=4, legs="wide", gaze=(0.8, 0.2),
                                          arm_r=dict(hand=(0.80, 0.30), bend=-0.6, stretch=1.25), prop_r=dict(type="plaster_trowel", angle=-8, scale=1.3),
                                          arm_l="akimbo"))
    M["master_plaster"] = dict(note="the trowel blade (prop_tip_r) pressed on a wall about 1.0 D right of the head; animate arm_r hand y "
                                     "0.10..0.50 for the strokes (trowel drawn at scale 1.3)",
                               stroke=dict(arm_r=dict(hand=(0.80, 0.50), bend=-0.5, stretch=1.25), prop_r=dict(type="plaster_trowel", angle=4, scale=1.3)))
    S["master_shocked"] = ("master", dict(yaw=-0.25, pitch=-0.2, expr="shocked", fx=["sweat"], head_roll=-5, lean=-4, squash=(0.97, 1.04),
                                          arm_r="raised", arm_l="raised", legs="wide"))
    S["master_rubble_look"] = ("master", dict(yaw=0.35, pitch=-1.2, expr="stunned", mouth="o", head_roll=4, gaze=(0.3, -1.0),
                                              arm_r=dict(hand=(0.30, 1.20), bend=0.8), arm_l=dict(hand=(-0.32, 1.18), bend=0.8),
                                              legs=dict(preset="wide", stride=0.4)))
    M["master_rubble_look"] = dict(lift=0.45, note="standing on the timber pile looking up at the swinging pillar: plant the feet on "
                                                   "rubble_svg()'s top (0, 0) -- 'lift' is the pile height used in poses.png")
    # --- townspeople
    for c, sfx in TOWN:
        ys = 1.0 if c != "woman2" else -1.0
        S["town_laugh_point" + sfx] = (c, dict(yaw=-0.35 * ys, pitch=-0.3, expr="laughing", fx=["tears"], head_roll=-10 * ys, lean=-5 * ys, t=0.6,
                                               arm_l=dict(hand=(-0.84, -0.12), shape="point", bend=-0.8, stretch=1.3),
                                               arm_r=dict(hand=(0.24, 1.02), bend=0.9), mirror=(ys < 0)))
        S["town_mock_shout" + sfx] = (c, dict(yaw=0.6, pitch=-0.4, expr="smug", mouth="talk_b", head_roll=6, lean=-4,
                                              arm_r=dict(hand=(0.58, 0.14), bend=-0.8, shape="open", stretch=1.2),
                                              arm_l=dict(hand=(0.56, 0.36), bend=-0.5, shape="open", stretch=1.3), legs="wide",
                                              mirror=(ys < 0)))
        S["town_run" + sfx] = (c, dict(yaw=0.85, pitch=-0.1, expr="shocked", fx=["sweat"], lean=14, head_roll=-6,
                                       legs=dict(preset="step", stride=1.2, lift_l=0.8, knee_l=1.0, toe_r=1.0),
                                       arm_r=dict(hand=(0.50, -0.30), bend=-0.9, shape="open", stretch=1.2),
                                       arm_l=dict(hand=(-0.40, -0.25), bend=-0.9, shape="open", layer="back", stretch=1.2)))
        crouch = dict(preset="crouch", crouch=0.55, knee_r=0.6, knee_l=-0.6) if c == "farmer" else dict(preset="narrow", crouch=0.10)
        S["town_shelter" + sfx] = (c, dict(yaw=0.2, pitch=1.0, expr="worried", blink=1, fx=["sweat"], lean=10, head_dy=0.08,
                                           squash=(1.0, 1.0) if c == "farmer" else (1.04, 0.95), legs=crouch,
                                           arm_r=dict(hand=(0.18, -0.44), bend=-1.0, layer="top", stretch=1.3),
                                           arm_l=dict(hand=(-0.20, -0.40), bend=-1.0, layer="top", stretch=1.3)))
    M["town_laugh_point"] = dict(note="merchant; _woman2 / _farmer variants for the others (woman2 mirrored: points screen-right)")
    M["town_shelter"] = dict(note="hunched, arms over the head (layer top), half-shut eyes; the farmer (short kimono) crouches deep, "
                                   "the long kimonos only bend the knees a little (the skirt is fixed to the torso)")
    return S, M


STORY4, STORY4_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast4_registered", False):
        CE.register_stage()
        if not STORY4:
            s, m = _story()
            STORY4.update(s)
            STORY4_META.update(m)
        return
    for name in ("_ink_limb", "_prop"):
        _O4[name] = getattr(P, name)
    P._ink_limb = _ink_limb
    P._prop = _prop
    CE.COSTUMES.update(COSTUMES4)
    CE.HATS.update(HATS4)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS4 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP4)
    for n, c in NEW_CAST4.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS4)
    P._cast4_registered = True
    s, m = _story()
    STORY4.update(s)
    STORY4_META.update(m)
    P.STORY.update(STORY4)
    CE.register_stage()


register()
