#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast2.py -- the cast of film 2 ("the sky-poker", Brescia 1769) for the v2 puppet, as an extension module.

    import sys; sys.path.insert(0, ".../v3/cast2"); import cast2      # registers on import (idempotent); imports cast_ext too
    import puppet                                                     # the same module object, now with the new members
    f = puppet.figure("nico", cast2.STORY2["nico_hold_rod"][1], "n")

Neither v2/puppet/puppet.py nor v3/cast/cast_ext.py is edited.  This module adds entries to their tables at run time:
    cast_ext.COSTUMES  tunic, cassock, baker, shawl, oldcoat, soldier      (dispatch: CAST[name]["costume"])
    cast_ext.HATS      skullcap, saturno, flatcap, headscarf, stocking, tricorn   (dispatch: CAST[name]["hat_style"])
    cast_ext.CANVAS    one feet-relative sprite canvas per member (cast_ext's import hook copies it into sprites.DEFAULT_CANVAS)
and wraps two puppet helpers on top of cast_ext's wrappers (each falls through for everything it does not handle):
    _ink_limb   boots on the legs (CAST key "boots")
    _prop       rod, rod_mid, hammer, bell_rope, book, lantern, stick
New cast:  nico, padre, baker, woman, old, soldier.   New build: "boy" (arm presets of "slim" scaled to the 0.62 arm).
STORY2 / STORY2_META: the story poses (see API.md).

Command line (QA):  python3 test_cast2.py        lineup.png, poses.png, robustness run
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_CASTDIR = os.path.join(PROJ, "v3", "cast")
if _CASTDIR not in sys.path:
    sys.path.insert(0, _CASTDIR)
import cast_ext as CE  # noqa: E402  (v3/cast, read-only; registers itself and puts v2/puppet on sys.path)
import puppet as P     # noqa: E402  (v2, read-only)

NEW2 = ("nico", "padre", "baker", "woman", "old", "soldier")
TT = P.TORSO_TOP
_clamp, _lerp, _smooth, _rot = P._clamp, P._lerp, P._smooth, P._rot
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_O2 = {}                      # the helpers this module wrapped (cast_ext's wrappers)


def _cur():
    return CE._CUR[0]


# ============================================================================= helpers
def _grad(k, name, base, x0, x1, light=1.12, dark=0.72):
    """left-to-right airbrush gradient like the torso's (light left, base at 35 percent, dark right)."""
    u = k.uid
    k.defs.append('<linearGradient id="%s_%s" gradientUnits="userSpaceOnUse" x1="%.4f" y1="0" x2="%.4f" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, name, x0, x1, k.c(P._shade(base, light)), k.c(base), k.c(P._shade(base, dark))))
    return "url(#%s_%s)" % (u, name)


def _skirt_pts(X, yt, a, hem, b, flare=0.62, rag=0.0, n_rag=0):
    """outline of a skirt / coat tail / tunic hem in torso-local coordinates: top corners (-a, yt) (a, yt), sides flaring to
    the hem corners (+-b, hem), hem slightly convex.  rag > 0 adds a ragged zig-zag hem with n_rag teeth."""
    right = [X(a, yt), X(a + (b - a) * flare * 0.55, yt + (hem - yt) * 0.40), X(b, hem - 0.015)]
    hemp = []
    if rag > 0 and n_rag > 1:
        for i in range(n_rag + 1):
            t = i / float(n_rag)
            x = b - 2 * b * t
            y = hem + 0.025 * math.sin(math.pi * t) + (rag if i % 2 else 0.0) * (0.6 + 0.4 * math.sin(i * 2.1))
            hemp.append(X(x, y))
    else:
        hemp = [X(b * 0.5, hem + 0.022), X(0.0, hem + 0.030), X(-b * 0.5, hem + 0.022)]
    left = [X(-b, hem - 0.015), X(-(a + (b - a) * flare * 0.55), yt + (hem - yt) * 0.40), X(-a, yt)]
    return right, hemp, left


def _skirt(k, name, X, yt, a, hem, b, fill, sw=0.030, rag=0.0, n_rag=0, folds=None, fold_col=None, ext=True):
    """skirt-like piece drawn OVER the torso bottom: filled shape (no line along its top edge, so it merges with a torso of the
    same fill), ink on the sides and the hem.  fill: colour or url.  Returns svg."""
    right, hemp, left = _skirt_pts(X, yt, a, hem, b, rag=rag, n_rag=n_rag)
    pts = right + hemp + left
    d_fill = _poly_d(pts) if rag > 0 else P._smooth_open(pts) + " Z"
    side = right + hemp + left
    d_line = ("M" + " L".join("%.4f,%.4f" % p for p in side)) if rag > 0 else P._smooth_open(side)
    o = ['<path d="%s" fill="%s"/>' % (d_fill, fill)]
    if folds:
        for (x0, y0, x1, y1) in folds:
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.75"/>'
                     % (X(x0, y0) + X((x0 + x1) / 2 * 1.08, (y0 + y1) / 2) + X(x1, y1) + (fold_col or k.ink,)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>' % (d_line, k.ink, sw))
    if ext:
        for p in (right[-1], left[0], hemp[len(hemp) // 2]):
            k.ext.append((p[0], p[1], 0.035))
    return "".join(o)


# ============================================================================= costumes (torso-local)
def _cos_tunic(k, C, m):
    """nico: oversized rust-orange tunic.  Round neckline with a laced slit, rope belt with a knot and two frayed ends, the
    skirt of the tunic flares over the hips to mid-thigh with a ragged hem, a sewn-on ochre patch with cross stitches."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    o = []
    # neckline: darker band under the chin, laced slit
    o.append('<path d="M%.4f,0.40 Q%.4f,0.535 %.4f,0.40" fill="none" stroke="%s" stroke-width="0.040"/>' % (X(-0.17, 0.4)[0], X(0, 0.5)[0], X(0.17, 0.4)[0], k.c(col["dark"])))
    o.append(_poly(k, [X(-0.045, 0.47), X(0.045, 0.47), X(0.0, 0.66)], k.c(col["lining"]), 0.013))
    lac = "".join("M%.4f,%.4f L%.4f,%.4f " % (X(-0.03, y) + X(0.03, y + 0.03)) for y in (0.50, 0.555))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (lac, k.c(col["rope_d"])))
    # seams on the chest (oversized: the shoulder seam hangs low)
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                 % (X(s * 0.30, 0.56) + X(s * 0.20, 0.70) + X(s * 0.24, 0.86) + (k.c(col["dark"]),)))
    inside = "".join(o)
    # skirt of the tunic over the hips
    yt = TT + 0.58 * h
    a = m.hwa * 0.985
    hem = yB + C.get("tunic_len", 0.22)
    b = m.hwa + C.get("tunic_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [_skirt(k, "tn", X, yt, a, hem, b, g, sw=0.028, rag=0.022, n_rag=9,
                 folds=((-0.10, yt + 0.12, -0.16, hem - 0.03), (0.13, yt + 0.12, 0.20, hem - 0.04)), fold_col=k.c(col["dark"]))]
    # patch with cross stitches (screen-left, on the skirt)
    px, py, ps = -0.17, yB - 0.02, 0.135
    pts = [X(px - ps / 2, py - ps / 2), X(px + ps / 2, py - ps / 2 + 0.01), X(px + ps / 2 - 0.005, py + ps / 2), X(px - ps / 2 + 0.006, py + ps / 2 - 0.006)]
    ov.append(_poly(k, pts, k.c(col["patch"]), 0.013))
    st = ""
    for i in range(4):
        t = (i + 0.5) / 4.0
        for (a0, a1) in ((0, 1), (3, 2)):
            pa = (pts[a0][0] + (pts[a1][0] - pts[a0][0]) * t, pts[a0][1] + (pts[a1][1] - pts[a0][1]) * t)
            st += "M%.4f,%.4f l%.4f,%.4f M%.4f,%.4f l%.4f,%.4f " % (pa[0] - 0.012, pa[1] - 0.012, 0.024, 0.024, pa[0] + 0.012, pa[1] - 0.012, -0.024, 0.024)
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (st, k.c(col["stitch"])))
    # rope belt: twisted band + knot + two hanging frayed ends
    yb = TT + 0.60 * h
    belt = [X(-a - 0.01, yb - 0.01), X(-a * 0.5, yb + 0.018), X(0.0, yb + 0.025), X(a * 0.5, yb + 0.018), X(a + 0.01, yb - 0.01)]
    d = P._smooth_open(belt)
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (d, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (d, k.c(col["rope"])))
    tw = ""
    for i in range(14):
        t = i / 13.0
        x = -a + 2 * a * t
        p = X(x, yb + 0.025 * (1 - (2 * t - 1) ** 2) - 0.004)
        tw += "M%.4f,%.4f l0.016,0.026 " % (p[0] - 0.008, p[1] - 0.013)
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (tw, k.c(col["rope_d"])))
    kx, ky = X(0.11, yb + 0.02)
    for (dx, ln, cv) in ((-0.025, 0.25, -0.03), (0.020, 0.20, 0.03)):
        e = (kx + dx + cv, ky + ln)
        dd = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (kx + dx * 0.4, ky, kx + dx + cv * 2, ky + ln * 0.5, e[0], e[1])
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (dd, k.ink))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.027" stroke-linecap="round"/>' % (dd, k.c(col["rope"])))
        ov.append('<path d="M%.4f,%.4f l-0.012,0.035 M%.4f,%.4f l0.004,0.038 M%.4f,%.4f l0.015,0.032" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                  % (e[0], e[1], e[0], e[1], e[0], e[1], k.c(col["rope_d"])))
        k.ext.append((e[0], e[1] + 0.04, 0.03))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.033" fill="%s" stroke="%s" stroke-width="0.012"/>' % (kx, ky, k.c(col["rope"]), k.ink))
    return inside, "", "".join(ov)


def _cos_cassock(k, C, m):
    """padre: black cassock buttoned down the front with a row of small red buttons, white collar tab at the throat,
    a wide fascia (sash) at the waist with two hanging ends, the skirt of the cassock to just above the ankles."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    o = []
    # standing collar band + the white tab at the throat
    o.append('<path d="M%.4f,0.405 Q%.4f,0.545 %.4f,0.405" fill="none" stroke="%s" stroke-width="0.050"/>'
             % (X(-0.21, 0.4)[0], X(0, 0.5)[0], X(0.21, 0.4)[0], k.c(col["collar"])))
    c = X(0.0, 0.485)
    o.append('<rect x="%.4f" y="%.4f" width="0.080" height="0.062" rx="0.010" fill="%s" stroke="%s" stroke-width="0.011"/>'
             % (c[0] - 0.040, c[1] - 0.031, k.c(col["tab"]), k.ink))
    # front opening line + sheen stripe on the light side
    o.append(_ln([X(0.0, 0.53), X(0.0, yB + 0.05)], k.c(col["line"]), 0.012))
    o.append('<path d="M%.4f,0.62 Q%.4f,0.95 %.4f,1.30" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round" opacity="0.55"/>'
             % (-m.hwa * 0.80, -m.hwa * 0.86, -m.hwa * 0.78, k.c(col["sheen"])))
    for y in _cassock_buttons(C, 0.56, TT + 0.70 * h):
        o.append(_button(k, X(0.0, y), col))
    inside = "".join(o)
    # skirt of the cassock, drawn over the torso bottom and the legs
    yt = TT + 0.66 * h
    a = m.hwa * 0.975
    hem = yB - 0.04 + C["leg"] * C.get("hem_frac", 0.80)
    b = m.hwa + C.get("skirt_flare", 0.09)
    g = "url(#%s_tg)" % k.uid
    ov = [_skirt(k, "cs", X, yt, a, hem, b, g, sw=0.032,
                 folds=((-0.20, yt + 0.25, -0.30, hem - 0.06), (0.24, yt + 0.25, 0.33, hem - 0.06), (-0.05, yt + 0.35, -0.07, hem - 0.05)),
                 fold_col=k.c(col["line"]))]
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.5"/>'
              % (X(-a * 0.82, yt + 0.12) + X(-b * 0.90, (yt + hem) / 2) + X(-b * 0.92, hem - 0.10) + (k.c(col["sheen"]),)))
    ov.append(_ln([X(0.0, yt + 0.06), X(0.0, hem)], k.c(col["line"]), 0.012))
    for y in _cassock_buttons(C, yt + 0.11, hem - 0.06):
        ov.append(_button(k, X(0.0, y), col))
    # fascia: wide sash over the seam, two hanging ends on the screen-left hip
    ys = yt + 0.005
    band = [X(-a - 0.012, ys - 0.045), X(0.0, ys - 0.020), X(a + 0.012, ys - 0.045), X(a + 0.012, ys + 0.040), X(0.0, ys + 0.065), X(-a - 0.012, ys + 0.040)]
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
              % (band[0] + band[1] + band[2] + band[3] + band[4] + band[5] + (k.c(col["sash"]), k.ink)))
    sx = X(-0.30, ys)[0]
    for dx, ln in ((-0.040, 0.42), (0.045, 0.36)):
        x0 = sx + dx
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                  % (x0 - 0.045, ys + 0.03, x0 + 0.045, ys + 0.03, x0 + 0.050, ys + ln, x0 - 0.050, ys + ln, k.c(col["sash"]), k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016"/>' % (x0 - 0.050, ys + ln - 0.03, x0 + 0.050, ys + ln - 0.03, k.c(col["sash_l"])))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.055" ry="0.045" fill="%s" stroke="%s" stroke-width="0.013"/>' % (sx, ys + 0.02, k.c(col["sash"]), k.ink))
    return inside, "", "".join(ov)


def _cassock_buttons(C, y0, y1, step=0.082):
    n = max(1, int((y1 - y0) / step))
    return [y0 + i * (y1 - y0) / n for i in range(n + 1)]


def _button(k, c, col):
    return ('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.009"/>'
            '<circle cx="%.4f" cy="%.4f" r="0.007" fill="%s"/>' % (c[0], c[1], k.c(col["button"]), k.ink, c[0] - 0.007, c[1] - 0.007, k.c(col["button_l"])))


def _cos_baker(k, C, m):
    """baker: sage-green shirt with the sleeves' edge implied by a seam, white apron with a bib, neck strap, waist ties, a
    front pocket and a flour smudge; brown trouser bowl; the apron runs over the bowl to the upper thigh."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = []
    # shirt collar (open, two points) and placket
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.17, 0.42), X(s * 0.02, 0.50), X(s * 0.15, 0.56)], k.c(col["collar"]), 0.013))
    o.append(CE._bowl(k, col["pants"], yb, yB))
    # bib of the apron, neck strap
    ap = k.c(col["apron"])
    bib = [X(-0.18, 0.60), X(0.18, 0.60), X(0.20, yb - 0.08), X(-0.20, yb - 0.08)]
    o.append(_poly(k, bib, ap, 0.014))
    for s in (-1, 1):
        o.append(_ln([X(s * 0.165, 0.605), X(s * 0.10, 0.42)], ap, 0.034))
        o.append(_ln([X(s * 0.165, 0.605), X(s * 0.10, 0.42)], k.ink, 0.008, ' opacity="0.6"'))
    inside = "".join(o)
    # apron skirt over the bowl
    yt = yb - 0.10
    a = m.hwa * 0.80
    hem = yB + 0.30
    ov = [_skirt(k, "ap", X, yt, a, hem, a + 0.04, ap, sw=0.022, folds=((-0.12, yt + 0.12, -0.15, hem - 0.04), (0.14, yt + 0.12, 0.17, hem - 0.04)),
                 fold_col=k.c(col["apron_d"]))]
    # waist ties and knot
    ov.append(_ln([X(-m.hwa * 0.99, yt + 0.005), X(m.hwa * 0.99, yt + 0.005)], k.c(col["apron_d"]), 0.032))
    ov.append(_ln([X(-m.hwa * 0.99, yt + 0.005), X(m.hwa * 0.99, yt + 0.005)], ap, 0.020))
    # pocket + flour smudge
    ov.append(_poly(k, [X(0.04, yt + 0.12), X(0.20, yt + 0.12), X(0.19, yt + 0.25), X(0.05, yt + 0.25)], ap, 0.012))
    c = X(-0.12, 0.85)
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.070" ry="0.040" fill="%s" opacity="0.65" transform="rotate(-20 %.4f %.4f)"/>'
              % (c[0], c[1], k.c(col["flour"]), c[0], c[1]))
    return inside, "", "".join(ov)


def _cos_shawl(k, C, m):
    """woman: wine bodice, ochre knitted shawl over the shoulders crossing on the chest (fringe on its points), long dark-teal
    skirt drawn over the torso bottom and most of the legs."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    o = []
    sh = k.c(col["shawl"])
    # shawl: two wings from the shoulders crossing at the chest, points hanging to the waist
    for s in (1, -1):
        pts = [X(s * 0.40, 0.36), X(s * 0.40, 0.62), X(-s * 0.10, 0.92), X(-s * 0.04, 0.80), X(s * 0.05, 0.56), X(s * 0.14, 0.38)]
        o.append(_poly(k, pts, sh, 0.015))
        ln = "".join("M%.4f,%.4f L%.4f,%.4f " % (X(s * (0.33 - 0.07 * i), 0.62 + 0.065 * i) + X(s * (0.20 - 0.06 * i), 0.50 + 0.06 * i)) for i in range(4))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (ln, k.c(col["shawl_d"])))
        tip = X(-s * 0.10, 0.92)
        fr = "".join("M%.4f,%.4f l%.4f,0.06 " % (tip[0] - s * 0.02 * i, tip[1] - 0.04 * i, -s * 0.008) for i in range(4))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (fr, k.c(col["shawl_d"])))
    inside = "".join(o)
    yt = TT + 0.72 * h
    a = m.hwa * 0.96
    hem = yB - 0.04 + C["leg"] * C.get("hem_frac", 0.80)
    b = m.hwa + C.get("skirt_flare", 0.16)
    g = _grad(k, "sk", col["skirt"], -b, b)
    ov = [_skirt(k, "sk", X, yt, a, hem, b, g, sw=0.030,
                 folds=((-0.12, yt + 0.15, -0.20, hem - 0.05), (0.14, yt + 0.15, 0.22, hem - 0.05)), fold_col=k.c(col["skirt_d"]))]
    # waistband
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>'
              % (X(-a, yt) + X(0, yt + 0.025) + X(a, yt) + (k.ink,)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>'
              % (X(-a, yt) + X(0, yt + 0.025) + X(a, yt) + (k.c(col["band"]),)))
    # hem band
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020"/>'
              % (X(-b + 0.02, hem - 0.06) + X(0, hem - 0.03) + X(b - 0.02, hem - 0.06) + (k.c(col["band"]),)))
    return inside, "", "".join(ov)


def _cos_oldcoat(k, C, m):
    """old man: long grey-green coat over a brown waistcoat and a cream shirt, big patched elbow-less pockets, coat tails to
    the knee drawn over the trouser bowl."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    # waistcoat panel + shirt V
    o.append(_poly(k, [X(-0.17, 0.40), X(0.17, 0.40), X(0.16, yb - 0.02), X(0.0, yb + 0.03), X(-0.16, yb - 0.02)], k.c(col["vest"]), 0.014))
    o.append(_poly(k, [X(-0.11, 0.42), X(0.11, 0.42), X(0.0, 0.66)], k.c(col["shirt"]), 0.013))
    for y in (0.74, 0.84, 0.94):
        o.append(_circ(X(0.0, y), 0.020, k.c(col["vest_b"]), k, 0.008))
    # coat lapels (open coat)
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.17, 0.39), X(s * 0.30, 0.40), X(s * 0.24, 0.62), X(s * 0.17, yb)], k.c(col["lapel"]), 0.014))
    inside = "".join(o)
    yt = yb - 0.05
    a = m.hwa * 0.97
    hem = yB + C["leg"] * 0.42
    g = "url(#%s_tg)" % k.uid
    # two coat tails, open in front (the waistcoat bottom and the bowl show between them)
    ov = []
    for s in (-1, 1):
        pts = [X(s * a, yt), X(s * (a + 0.05), (yt + hem) / 2), X(s * (a + 0.07), hem), X(s * 0.12, hem + 0.02), X(s * 0.16, yt)]
        ov.append('<path d="%s" fill="%s"/>' % (_poly_d(pts), g))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
                  % (pts[0] + pts[1] + pts[2] + pts[3] + pts[4] + (k.ink,)))
        pk = [X(s * 0.20, yt + 0.10), X(s * 0.38, yt + 0.10), X(s * 0.37, yt + 0.24), X(s * 0.21, yt + 0.24)]
        ov.append(_poly(k, pk, k.c(col["pocket"]), 0.012))
        k.ext.append((pts[2][0], pts[2][1], 0.04))
    # elbow patch-like darn on the right tail
    c = X(0.30, hem - 0.10)
    ov.append('<path d="M%.4f,%.4f l0.05,0.03 M%.4f,%.4f l0.05,-0.03" stroke="%s" stroke-width="0.010" fill="none"/>' % (c[0] - 0.025, c[1] - 0.015, c[0] - 0.025, c[1] + 0.015, k.c(col["dark"])))
    return inside, "", "".join(ov)


def _cos_soldier(k, C, m):
    """soldier: blue coat with red facings, white waistcoat, two white cross belts with a brass plate, brass buttons, coat
    tails with red turnbacks over white breeches."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    o.append(_poly(k, [X(-0.13, 0.40), X(0.13, 0.40), X(0.12, yb), X(-0.12, yb)], k.c(col["vest"]), 0.013))
    for y in (0.62, 0.72, 0.82, 0.92):
        o.append(_circ(X(0.0, y), 0.016, k.c(col["brass"]), k, 0.007))
    # red facings (lapels) with brass buttons
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.13, 0.40), X(s * 0.27, 0.42), X(s * 0.25, 0.82), X(s * 0.13, 0.86)], k.c(col["facing"]), 0.014))
        for y in (0.52, 0.64, 0.76):
            o.append(_circ(X(s * 0.20, y), 0.019, k.c(col["brass"]), k, 0.008))
    # neck stock
    o.append('<path d="M%.4f,0.41 Q%.4f,0.52 %.4f,0.41" fill="none" stroke="%s" stroke-width="0.045"/>' % (X(-0.15, 0.4)[0], X(0, 0.5)[0], X(0.15, 0.4)[0], k.c(col["stock"])))
    # cross belts
    wb = k.c(col["belt"])
    for s in (-1, 1):
        a0, a1 = X(s * 0.36, 0.40), X(-s * 0.32, yb + 0.02)
        o.append(_ln([a0, a1], k.ink, 0.074))
        o.append(_ln([a0, a1], wb, 0.052))
    c = X(0.0, 0.70)
    o.append('<rect x="%.4f" y="%.4f" width="0.080" height="0.065" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (c[0] - 0.04, c[1] - 0.0325, k.c(col["brass"]), k.ink))
    inside = "".join(o)
    # coat tails with red turnbacks
    yt = yb - 0.03
    a = m.hwa * 0.98
    hem = yB + C["leg"] * 0.35
    g = "url(#%s_tg)" % k.uid
    ov = []
    for s in (-1, 1):
        pts = [X(s * a, yt), X(s * (a + 0.03), (yt + hem) / 2), X(s * (a + 0.04), hem), X(s * 0.20, hem - 0.02), X(s * 0.17, yt)]
        ov.append('<path d="%s" fill="%s"/>' % (_poly_d(pts), g))
        tb = [X(s * (a + 0.01), (yt + hem) / 2 + 0.03), X(s * (a + 0.04), hem), X(s * 0.20, hem - 0.02)]
        ov.append(_poly(k, tb, k.c(col["facing"]), 0.012))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
                  % (pts[0] + pts[1] + pts[2] + pts[3] + pts[4] + (k.ink,)))
        k.ext.append((pts[2][0], pts[2][1], 0.04))
    return inside, "", "".join(ov)


COSTUMES2 = {"tunic": _cos_tunic, "cassock": _cos_cassock, "baker": _cos_baker, "shawl": _cos_shawl, "oldcoat": _cos_oldcoat,
             "soldier": _cos_soldier}


# ============================================================================= hats (head frame, drawn over the head)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_skullcap(k, C, yaw):
    """nico: short soft brown felt cap pulled low over the head, rolled cuff, small stalk on the crown, one darning stitch.
    Narrower than the head (0.92 D), top 0.60 D above the head centre; no visor (the film-1 hero has one)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    sx = dx - 0.12 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.46, x1=0.46, mid=0.32)
    xl, xr, yb, top = -0.462 + dx, 0.462 + dx, -0.255, -0.585
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
            % (xl, yb, xl - 0.03, yb - 0.24, sx - 0.33, top, sx, top, sx + 0.33, top, xr + 0.03, yb - 0.24, xr, yb))
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="%s"/>' % (dome, g))
    # felt creases
    for f in (-0.55, 0.0, 0.55):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.013" stroke-linecap="round" opacity="0.7"/>'
                 % (sx + f * 0.12, top + 0.04, sx + f * 0.30, top + 0.12, dx + f * 0.36, yb - 0.08, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>'
             % (xl + 0.07, yb - 0.11, xl + 0.12, top + 0.10, sx - 0.15, top + 0.03, k.c(col["shine"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, k.ink))
    # stalk
    o.append('<path d="M%.4f,%.4f q0.012,-0.055 0.050,-0.060" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (sx - 0.01, top + 0.012, k.ink))
    o.append('<path d="M%.4f,%.4f q0.012,-0.055 0.050,-0.060" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (sx - 0.01, top + 0.012, k.c(col["base"])))
    # rolled cuff
    cuff = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl - 0.012, yb - 0.075, dx, yb - 0.035, xr + 0.012, yb - 0.075, xr + 0.006, yb + 0.012, dx, yb + 0.055, xl - 0.006, yb + 0.012))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (cuff, k.c(col["cuff"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
             % (xl + 0.03, yb - 0.025, dx, yb + 0.015, xr - 0.03, yb - 0.025, k.c(col["dark"])))
    # darning stitch on the cuff (screen-right)
    c = (dx + 0.25, yb - 0.010)
    o.append('<path d="M%.4f,%.4f l0.03,0.025 M%.4f,%.4f l0.03,-0.025 M%.4f,%.4f l0.03,0.025" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>'
             % (c[0] - 0.03, c[1] - 0.012, c[0], c[1] + 0.013, c[0] + 0.03, c[1] - 0.012, k.c(col["stitch"])))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.02, yb), (xr + 0.02, yb), (sx, top - 0.06), (dx, yb + 0.06)))
    return "".join(o), (sx, top - 0.05)


def _hat_saturno(k, C, yaw):
    """padre: saturno -- wide flat round black brim (1.62 D) seen nearly edge-on, low round crown sitting on it, a thin
    cord round the crown base, painted highlight streaks on the crown and along the brim's upper edge."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx - 0.06 * yaw
    rx, ry, cy = 0.81, 0.120, -0.335
    g = CE._gradient(k, "ht", col, x0=-0.40, x1=0.40, mid=0.30)
    gb = CE._gradient(k, "hb", dict(light=col["brim_l"], base=col["brim"], dark=col["dark"]), x0=-rx, x1=rx, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    # brim, full ellipse
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.030"/>' % (dx, cy, rx, ry, gb, k.ink))
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
             % (dx - rx * 0.82, cy - ry * 0.40, rx * 0.95, ry * 0.95, dx + rx * 0.10, cy - ry * 0.96, k.c(col["shine"])))
    # crown: half dome on the brim
    cw, ch = 0.37, 0.285
    yb = cy - 0.005
    crown = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" % (
        cx - cw, yb, cx - cw, yb - ch * 0.75, cx - cw * 0.55, yb - ch, cx, yb - ch, cx + cw * 0.55, yb - ch, cx + cw, yb - ch * 0.75, cx + cw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (cx - cw * 0.78, yb - 0.08, cx - cw * 0.70, yb - ch * 0.86, cx - cw * 0.20, yb - ch * 0.97, k.c(col["shine"])))
    # cord at the crown base
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>'
             % (cx - cw + 0.01, yb - 0.035, cx, yb - 0.005, cx + cw - 0.01, yb - 0.035, k.c(col["cord"])))
    # front lip of the brim over the crown base
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 0 %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (dx - rx, cy, rx, ry, dx + rx, cy, dx, cy + ry * 0.35, dx - rx, cy, gb, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round" opacity="0.7"/>'
             % (dx - rx * 0.75, cy + ry * 0.45, dx, cy + ry * 0.92, dx + rx * 0.6, cy + ry * 0.58, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - rx - 0.02, cy), (dx + rx + 0.02, cy), (cx, yb - ch - 0.02), (dx, cy + ry + 0.02)))
    return "".join(o), (cx, yb - ch)


def _hat_flatcap(k, C, yaw):
    """baker: low blue-grey flat cap, the flat top sloping forward onto a short stiff peak; one seam; no panels."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    vx = 0.22 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.46, x1=0.46, mid=0.30)
    xl, xr, yb = -0.455 + dx, 0.455 + dx, -0.265
    top = (P._smooth_open([(xl, yb), (xl - 0.02, yb - 0.13), (dx - 0.22, -0.52), (dx + 0.10, -0.535), (xr - 0.02, -0.43), (xr + 0.02, yb)]))
    d = top + " Q%.4f,%.4f %.4f,%.4f Z" % (vx * 0.5, yb + 0.03, xl, yb)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    hv = 0.36 - 0.06 * abs(yaw)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (vx - hv, yb, vx, yb + 0.105, vx + hv, yb, vx, yb + 0.03, vx - hv, yb, k.c(col["visor"]), k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (dx - 0.30, -0.36, dx + 0.02, -0.50, dx + 0.36, -0.36, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
             % (xl + 0.06, yb - 0.08, dx - 0.30, -0.49, dx - 0.10, -0.515, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.03, yb), (xr + 0.03, yb), (dx, -0.56), (vx, yb + 0.12)))
    return "".join(o), (dx, -0.545)


def _hat_headscarf(k, C, yaw):
    """woman: dark-blue headscarf with white dots framing the face (covers the crown and both temples down to the cheeks),
    knot and two tails on the side away from the face."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    u = k.uid
    outer = [(-0.53 + dx, 0.14), (-0.56 + dx, -0.22), (-0.38 + dx, -0.53), (dx, -0.625), (0.38 + dx, -0.53), (0.56 + dx, -0.22), (0.53 + dx, 0.14)]
    inner = [(0.42 + fx, 0.12), (0.42 + fx, -0.16), (0.25 + fx, -0.285), (fx, -0.31), (-0.25 + fx, -0.285), (-0.42 + fx, -0.16), (-0.42 + fx, 0.12)]
    d = P._smooth_open(outer) + " L" + P._smooth_open(inner)[1:] + " Z"
    k.defs.append('<pattern id="%s_sd" width="0.10" height="0.10" patternUnits="userSpaceOnUse"><circle cx="0.03" cy="0.03" r="0.012" fill="%s"/>'
                  '<circle cx="0.08" cy="0.08" r="0.012" fill="%s"/></pattern><clipPath id="%s_sc"><path d="%s"/></clipPath>'
                  % (u, k.c(col["dot"]), k.c(col["dot"]), u, d))
    g = CE._gradient(k, "ht", col, x0=-0.55, x1=0.55, mid=0.32)
    o = []
    # knot + tails behind the head on the far side
    s = -1.0 if yaw >= 0 else 1.0
    w = _smooth(0.0, 0.25, abs(yaw)) * 0.6 + 0.4
    kx = s * (0.50 + 0.04 * w)
    for (ang, ln) in ((20, 0.30), (55, 0.26)):
        ex, ey = kx + s * ln * math.cos(math.radians(ang)) * w, 0.05 + ln * math.sin(math.radians(ang))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (kx, -0.01, ex, ey, kx + s * 0.03, 0.10, k.c(col["base"]), k.ink))
        k.ext.append((ex, ey, 0.03))
    o.append('<path d="%s" fill="%s"/>' % (d, g))
    o.append('<g clip-path="url(#%s_sc)"><rect x="-0.7" y="-0.7" width="1.4" height="0.9" fill="url(#%s_sd)"/></g>' % (u, u))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.6"/>'
             % (-0.30 + dx, -0.50, dx + 0.05, -0.40, 0.33 + dx, -0.50, k.c(col["dark"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, k.ink))
    o.append('<circle cx="%.4f" cy="-0.01" r="0.050" fill="%s" stroke="%s" stroke-width="0.015"/>' % (kx, k.c(col["base"]), k.ink))
    k.ext.extend([(-0.58, -0.2, 0.02), (0.58, -0.2, 0.02), (0.0, -0.64, 0.02)])
    return "".join(o), (dx, -0.625)


def _hat_stocking(k, C, yaw):
    """old man: long red knitted stocking cap with a ribbed cuff; the floppy top folds over to the back of the head and ends
    in a small tassel; white tufts of hair poke out under the cuff."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = -1.0 if yaw >= 0.0 else 1.0            # the tail hangs on the side away from the face
    o = [CE._tufts(k, yaw, ytop=-0.25)]
    g = CE._gradient(k, "ht", col, x0=-0.46, x1=0.46, mid=0.32)
    xl, xr, yb = -0.455 + dx, 0.455 + dx, -0.27
    tipx, tipy = dx + s * 0.62, -0.30
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
         % (xl, yb, xl - 0.02, -0.52, dx - 0.15, -0.66, dx + s * 0.18, -0.66,
            dx + s * 0.50, -0.66, tipx, -0.50, tipx, tipy,
            tipx - s * 0.12, -0.42, xr - 0.05 if s > 0 else xl + 0.05, -0.45, xr, yb))
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.7"/>'
             % (dx - s * 0.20, -0.33, dx + s * 0.10, -0.60, tipx - s * 0.08, -0.42, k.c(col["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.055" fill="%s" stroke="%s" stroke-width="0.014"/>' % (tipx, tipy + 0.03, k.c(col["tassel"]), k.ink))
    cuff = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl - 0.015, yb - 0.085, dx, yb - 0.045, xr + 0.015, yb - 0.085, xr + 0.008, yb + 0.015, dx, yb + 0.055, xl - 0.008, yb + 0.015))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (cuff, k.c(col["cuff"]), k.ink))
    rib = "".join("M%.4f,%.4f L%.4f,%.4f " % (dx + x, yb - 0.06 + 0.04 * (x / 0.45) ** 2, dx + x, yb + 0.01 + 0.035 * (1 - (x / 0.45) ** 2)) for x in [i * 0.075 - 0.375 for i in range(11)])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (rib, k.c(col["dark"])))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.02, yb), (xr + 0.02, yb), (dx, -0.68), (tipx + s * 0.06, tipy + 0.03)))
    return "".join(o), (dx, -0.66)


def _hat_tricorn(k, C, yaw):
    """soldier: black felt tricorn, brim turned up into three corners (front corner over the brows), white lace edging and
    a red-and-white cockade on the screen-left side."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.22 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.6, x1=0.6, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    # crown peeping above the brim
    o.append('<path d="M%.4f,-0.48 C%.4f,-0.66 %.4f,-0.70 %.4f,-0.70 C%.4f,-0.70 %.4f,-0.66 %.4f,-0.48 Z" fill="%s" stroke="%s" stroke-width="0.028"/>'
             % (dx - 0.32, dx - 0.30, dx - 0.12, dx, dx + 0.12, dx + 0.30, dx + 0.32, k.c(col["dark"]), k.ink))
    pts = [(dx - 0.66, -0.47), (dx - 0.40, -0.58), (fx - 0.05, -0.50), (fx, -0.51), (fx + 0.05, -0.50), (dx + 0.40, -0.58), (dx + 0.66, -0.47),
           (dx + 0.45, -0.34), (fx + 0.10, -0.26), (fx, -0.215), (fx - 0.10, -0.26), (dx - 0.45, -0.34)]
    d = _poly_d(pts)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    lace = P._smooth_open([(dx - 0.60, -0.47), (dx - 0.42, -0.375), (fx - 0.10, -0.29), (fx, -0.25), (fx + 0.10, -0.29), (dx + 0.42, -0.375), (dx + 0.60, -0.47)])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (lace, k.c(col["lace"])))
    o.append('<path d="M%.4f,-0.53 Q%.4f,-0.57 %.4f,-0.52" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.50, dx - 0.35, dx - 0.15, k.c(col["shine"])))
    ck = (dx - 0.36 + 0.05 * yaw, -0.44)
    o.append('<circle cx="%.4f" cy="%.4f" r="0.062" fill="%s" stroke="%s" stroke-width="0.013"/>' % (ck + (k.c(col["cockade"]), k.ink)))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.030" fill="%s"/>' % (ck + (k.c(col["lace"]),)))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="%s"/>' % (ck + (k.c(col["brass"]),)))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.68, -0.47), (dx + 0.68, -0.47), (dx, -0.72), (fx, -0.20)))
    return "".join(o), (dx, -0.70)


HATS2 = {"skullcap": _hat_skullcap, "saturno": _hat_saturno, "flatcap": _hat_flatcap, "headscarf": _hat_headscarf,
         "stocking": _hat_stocking, "tricorn": _hat_tricorn}


# ============================================================================= boots (legs)
def _boot(k, A, T, w, B):
    """boot at the ankle A, toe direction from the foot stub end T; sole on the sole line (A.y + w/2 + 0.008)."""
    tx = T[0] - A[0]
    s = 1.0 if tx >= 0 else -1.0
    a = min(1.0, abs(tx) / P.FOOT_LEN)
    sole = A[1] + w / 2 + 0.008
    toe = B.get("toe", 0.13)
    hgt = B.get("h", 0.12)
    hw = w / 2 + 0.022
    heel = A[0] - s * (0.05 + 0.01 * a)
    tip = A[0] + s * (0.045 + toe * a)
    pts = [(A[0] - s * hw, A[1] - hgt), (A[0] + s * hw, A[1] - hgt), (A[0] + s * (hw + 0.004), A[1] - 0.01),
           (tip - s * 0.04, sole - 0.072), (tip, sole - 0.035), (tip, sole), (heel, sole), (heel - s * 0.006, A[1] - 0.01)]
    col = k.c(B["color"])
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts) if B.get("soft") else _poly_d(pts), col, k.ink)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (A[0] - s * hw, A[1] - hgt + 0.03, A[0] + s * hw, A[1] - hgt + 0.03,
                                                                                                         k.c(B.get("cuff", B["color"]))))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (heel, sole - 0.006, tip, sole - 0.006, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.35"/>'
             % (A[0] - s * hw * 0.4, A[1] - hgt + 0.05, A[0] - s * hw * 0.5, A[1] - 0.02, A[0], sole - 0.05))
    k.ext.append((tip, sole, 0.02))
    k.ext.append((heel, sole, 0.02))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O2["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = _cur()
    if tail is None and C is not None and C.get("limb_edge"):
        # arms in black sleeves over a black cassock: a thin light edge keeps the plum ink arm readable (arms only)
        out = ('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>'
               % (P._limb_d(S, E, H, kk), k.c(C["limb_edge"]), w + 0.034)) + out
    if tail is not None and C is not None and C.get("boots"):
        out += _boot(k, H, tail, w, C["boots"])
    return out


def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    C = _cur()
    out = _O2["_hand"](k, H, dirv, shape, hr, fold)
    if C is not None and C.get("limb_edge"):
        out = '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (H[0], H[1], hr + 0.017, k.c(C["limb_edge"])) + out
    return out


# ============================================================================= props
NEW_PROPS2 = ("rod", "rod_mid", "hammer", "bell_rope", "book", "lantern", "stick")
# working point distance from the gripping hand (D): rod point (rod gripped 0.9 D from its base), rod_mid point (gripped at the
# middle), hammer head centre, bell_rope = the hand (the rope is always vertical), book = the second hand's grip point (always
# upright, see _prop), lantern = centre of the glass (hangs upright), stick = its foot on the ground
NEW_TIP2 = {"rod": 1.70, "rod_mid": 1.30, "hammer": 0.36, "bell_rope": 0.0, "book": 0.50, "lantern": 0.30, "stick": 1.40}
ROD_LEN = 2.60
ROPE_UP, ROPE_DOWN = 3.6, 0.75
BOOK_W = 0.50


def _rod(k, x0, x1, sc):
    """thin iron rod along local +x from x0 to x1 (point at x1)."""
    r = 0.020
    tp = 0.13
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,0 L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
         % (x0, -r, x1 - tp, -r, x1, x1 - tp, r, x0, r, k.c("#5d6170"), k.ink)]
    o.append('<path d="M%.4f,-0.007 L%.4f,-0.005" stroke="%s" stroke-width="0.007" stroke-linecap="round" opacity="0.85"/>' % (x0 + 0.04, x1 - tp - 0.02, k.c("#b9c0cf")))
    o.append('<path d="M%.4f,-0.012 L%.4f,0 L%.4f,0.012 Z" fill="%s"/>' % (x1 - 0.05, x1 - 0.004, x1 - 0.05, k.c("#d8dde8")))
    # forged ring near the base and rust specks
    o.append('<rect x="%.4f" y="-0.030" width="0.030" height="0.060" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x0 + 0.10, k.c("#4a4d5a"), k.ink))
    for f, dy in ((0.28, 0.006), (0.55, -0.008), (0.71, 0.005)):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.006" fill="%s"/>' % (x0 + (x1 - x0) * f, dy, k.c("#9a5a34")))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS2:
        return _O2["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    if kind == "bell_rope":
        # hemp rope, always vertical: from ROPE_UP above the hand down to a knotted, frayed end ROPE_DOWN below it
        x, y = H
        top, bot = y - ROPE_UP * sc, y + ROPE_DOWN * sc
        o = ['<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.054" stroke-linecap="butt"/>' % (x, top, x, bot - 0.05, ink)]
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.032"/>' % (x, top, x, bot - 0.05, k.c("#c79a5c")))
        tw = "".join("M%.4f,%.4f l0.026,-0.030 " % (x - 0.013, top + 0.06 * i) for i in range(int((bot - top) / 0.06)))
        o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none" opacity="0.8"/>' % (tw, k.c("#8a6234")))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.042" ry="0.038" fill="%s" stroke="%s" stroke-width="0.013"/>' % (x, bot - 0.05, k.c("#c79a5c"), ink))
        o.append('<path d="M%.4f,%.4f l-0.020,0.060 M%.4f,%.4f l0,0.065 M%.4f,%.4f l0.022,0.058" stroke="%s" stroke-width="0.012" stroke-linecap="round" fill="none"/>'
                 % (x - 0.01, bot - 0.02, x, bot - 0.02, x + 0.01, bot - 0.02, k.c("#8a6234")))
        for e in ((x, y - 0.6), (x, bot + 0.05)):
            k.ext.append((e[0], e[1], 0.04))
        return "".join(o), (x, y)
    if kind == "lantern":
        # tin lantern hanging upright from the hand by its ring, warm glass and a soft glow
        u = k.uid
        k.defs.append('<radialGradient id="%s_lg"><stop offset="0" stop-color="%s" stop-opacity="0.55"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
                      % (u, k.c("#ffd27a"), k.c("#ffb347")))
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        o.append('<circle cx="0" cy="0.30" r="0.34" fill="url(#%s_lg)"/>' % u)
        o.append('<circle cx="0" cy="0.02" r="0.035" fill="none" stroke="%s" stroke-width="0.016"/>' % ink)
        o.append('<path d="M-0.10,0.14 L0,0.055 L0.10,0.14 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#4d4a52"), ink))
        o.append('<rect x="-0.095" y="0.14" width="0.19" height="0.27" rx="0.02" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#ffe09a"), ink))
        o.append('<path d="M0,0.36 Q-0.035,0.30 0,0.22 Q0.035,0.30 0,0.36 Z" fill="%s"/>' % k.c("#ff9a2e"))
        o.append('<path d="M-0.032,0.14 L-0.032,0.41 M0.032,0.14 L0.032,0.41" stroke="%s" stroke-width="0.011"/>' % k.c("#4d4a52"))
        o.append('<rect x="-0.115" y="0.40" width="0.23" height="0.045" rx="0.012" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#4d4a52"), ink))
        o.append('</g>')
        for e in ((-0.13, 0.15), (0.13, 0.15), (0.0, 0.46), (0.0, 0.0)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0], H[1] + 0.30 * sc)
    if kind == "book":
        # open book held upright by its lower edge: grip at the outer lower corner of the left page; the other hand belongs at
        # the returned tip point (BOOK_W to the right).  Left page: a lightning bolt striking a pointed rod (what nico read)
        w = BOOK_W
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        o.append('<path d="M-0.05,0.03 L-0.05,-0.31 Q%.4f,-0.35 %.4f,-0.31 Q%.4f,-0.35 %.4f,-0.31 L%.4f,0.03 Q%.4f,0.00 %.4f,0.04 Q%.4f,0.00 -0.05,0.03 Z" '
                 'fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (w * 0.25, w / 2, w * 0.75, w + 0.05, w + 0.05, w * 0.75, w / 2, w * 0.25, k.c("#7a3b28"), ink))
        o.append('<path d="M-0.02,0.00 L-0.02,-0.29 Q%.4f,-0.33 %.4f,-0.28 L%.4f,0.02 Q%.4f,-0.02 -0.02,0.00 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (w * 0.25, w / 2, w / 2, w * 0.25, k.c("#f6ecd2"), ink))
        o.append('<path d="M%.4f,0.02 L%.4f,-0.28 Q%.4f,-0.33 %.4f,-0.29 L%.4f,0.00 Q%.4f,-0.02 %.4f,0.02 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (w / 2, w / 2, w * 0.75, w + 0.02, w + 0.02, w * 0.75, w / 2, k.c("#efe3c4"), ink))
        # left page: bolt + rod + ground
        o.append('<path d="M0.06,-0.26 L0.11,-0.17 L0.085,-0.165 L0.14,-0.085" fill="none" stroke="%s" stroke-width="0.013" stroke-linejoin="round" stroke-linecap="round"/>' % k.c("#d9a21a"))
        o.append('<path d="M0.15,-0.085 L0.15,-0.035 M0.10,-0.03 L0.21,-0.03" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c("#4a3a40"))
        o.append('<path d="M0.15,-0.03 Q0.17,-0.01 0.20,-0.012" fill="none" stroke="%s" stroke-width="0.007" stroke-dasharray="0.012 0.008"/>' % k.c("#4a3a40"))
        # right page: text lines
        d = "".join("M%.4f,%.4f L%.4f,%.4f " % (w / 2 + 0.04, y, w - 0.04, y) for y in (-0.24, -0.205, -0.17, -0.135, -0.10, -0.065, -0.03))
        o.append('<path d="%s" stroke="%s" stroke-width="0.010" fill="none" opacity="0.7"/>' % (d, k.c("#8d8089")))
        o.append('<path d="M%.4f,-0.29 L%.4f,0.025" stroke="%s" stroke-width="0.010"/>' % (w / 2, w / 2, ink))
        o.append('</g>')
        for e in ((-0.06, 0.04), (w + 0.06, 0.04), (-0.06, -0.33), (w + 0.06, -0.33)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0] + w * sc, H[1])
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind in ("rod", "rod_mid"):
        tip = NEW_TIP2[kind]
        x0 = tip - ROD_LEN
        o.append(_rod(k, x0, tip, sc))
        ends = ((x0, 0.0), (tip, 0.0))
    elif kind == "hammer":
        tip = NEW_TIP2["hammer"]
        o.append('<path d="M-0.08,-0.020 L0.36,-0.017 L0.36,0.017 L-0.08,0.022 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#a8743f"), ink))
        o.append('<path d="M-0.06,-0.006 L0.30,-0.005" stroke="%s" stroke-width="0.006" opacity="0.7"/>' % k.c("#d9a56a"))
        o.append('<path d="M0.315,-0.115 L0.405,-0.115 L0.405,0.075 Q0.36,0.10 0.315,0.075 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#5d6170"), ink))
        o.append('<path d="M0.315,0.072 L0.405,0.072" stroke="%s" stroke-width="0.010"/>' % k.c("#b9c0cf"))
        o.append('<path d="M0.330,-0.10 L0.330,0.04" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c("#9aa2b4"))
        ends = ((-0.08, 0.0), (0.41, -0.12), (0.41, 0.09))
    else:  # stick
        tip = NEW_TIP2["stick"]
        o.append('<path d="M-0.02,-0.020 L1.40,-0.016 L1.40,0.016 L-0.02,0.020 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#8a5a32"), ink))
        o.append('<path d="M0.0,-0.018 Q-0.10,-0.02 -0.11,-0.10 Q-0.10,-0.17 -0.03,-0.17" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % ink)
        o.append('<path d="M0.0,-0.018 Q-0.10,-0.02 -0.11,-0.10 Q-0.10,-0.17 -0.03,-0.17" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.c("#8a5a32"))
        o.append('<path d="M0.30,-0.005 L0.32,0.010 M0.70,-0.006 L0.72,0.008" stroke="%s" stroke-width="0.008"/>' % k.c("#5a3820"))
        ends = ((-0.14, -0.17), (1.40, 0.0))
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(tip * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


# ============================================================================= builds
BOY_ARM = 0.62


def _build_presets():
    A = P.ARM_PRESETS
    if "boy" not in A:
        f = BOY_ARM / 0.74
        A["boy"] = dict((n, (v[0] * f, v[1] * f) + tuple(v[2:])) for n, v in A["slim"].items())
    A["boy"].setdefault("shade", (0.060, -0.560, -1.0, "top", "open", 0.35, 1.04))


# ============================================================================= cast
PROFILE_BOY = ((0.66, 0.02), (0.93, 0.11), (1.00, 0.27), (1.00, 0.50), (0.99, 0.70), (0.95, 0.85), (0.76, 0.96), (0.42, 1.00))
PROFILE_ROUND = ((0.50, 0.02), (0.80, 0.10), (0.93, 0.24), (0.99, 0.40), (1.00, 0.58), (0.98, 0.76), (0.92, 0.86), (0.72, 0.95), (0.40, 0.995))

NEW_CAST2 = {
    # the boy hero: smallest figure (0.8 of the adults), oversized rust tunic, rope belt, patch, brown felt cap, small boots
    "nico": dict(
        build="boy", seed=4.7,
        torso_w=0.64, torso_h=0.80, profile=PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.245, 0.50), arm=BOY_ARM, hip_x=0.15, leg=0.82, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="skullcap", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#a8774c", base="#86562f", dark="#5c3a1e", shine="#c99a68", cuff="#6e4524", stitch="#e2c48a"),
        hair=dict(color="#3e2a22", front=0.08, grow=0.20),
        costume="tunic", tunic_len=0.24, tunic_flare=0.11,
        boots=dict(color="#6b4428", cuff="#8a5c38", h=0.11, toe=0.12, soft=True),
        colors=dict(base="#cf5a26", dark="#8f3612", lining="#5e2a14", patch="#d8a050", stitch="#5b3a20", rope="#d6b47c", rope_d="#8a6a3c",
                    pants="#3a2832"),
    ),
    # the priest: tall and round, black cassock, red buttons, white collar tab, fascia, saturno, rosy cheeks
    "padre": dict(
        build="stout", seed=26.9,
        torso_w=1.06, torso_h=1.12, profile=PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.40, 0.44), arm=0.74, hip_x=0.15, leg=1.36, stance=0.05, wide=0.24, limb_w=0.068,
        eye_y=0.000, brow="stroke", brow_th=0.050, mouth="dash", moustache=False, smirk_side=-1, cheeks="#f29a96",
        hat="newsboy", hat_style="saturno", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#5a5366", base="#2f2a37", dark="#1c1922", shine="#a9a2c0", brim="#2a2531", brim_l="#4a4456", cord="#1a1720"),
        hair=dict(color="#6f6670", front=0.05, grow=0.20),
        costume="cassock", hem_frac=0.78, skirt_flare=0.09, limb_edge="#7d7596",
        boots=dict(color="#24212a", cuff="#24212a", h=0.08, toe=0.14),
        colors=dict(base="#332e3c", collar="#1d1a23", tab="#fbf8f2", line="#16131b", sheen="#6a6380", button="#d3322c", button_l="#f6a39a",
                    sash="#2a2532", sash_l="#4d465b", pants="#24212a"),
    ),
    # townspeople
    "baker": dict(
        build="regular", seed=20.1,
        torso_w=0.84, torso_h=1.04, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.22, stance=0.07, wide=0.28, limb_w=0.062,
        eye_y=0.030, brow="stroke", brow_th=0.050, mouth="dash", moustache=False, smirk_side=1, cheeks="#f4b0a0",
        hat="newsboy", hat_style="flatcap", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#9ba6bd", base="#6d7891", dark="#47506a", shine="#d2d9e8", visor="#5a647c"),
        hair=dict(color="#5a3a26", front=0.08, grow=0.22),
        costume="baker", boots=dict(color="#4d3524", cuff="#4d3524", h=0.08, toe=0.13),
        colors=dict(base="#6f9a52", collar="#e8e4d4", apron="#f5f1e8", apron_d="#bfb6a8", flour="#ffffff", pants="#5c4636"),
    ),
    "woman": dict(
        build="slim", seed=11.8,
        torso_w=0.58, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.225, 0.52), arm=0.72, hip_x=0.14, leg=1.18, stance=0.05, wide=0.24, limb_w=0.055,
        eye_y=0.040, brow="stroke", brow_th=0.032, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f2b0aa",
        hat="newsboy", hat_style="headscarf", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#5774b4", base="#34508f", dark="#223766", dot="#f1ece0"),
        hair=dict(color="#4a2e22", front=0.0, grow=0.0),
        costume="shawl", hem_frac=0.84, skirt_flare=0.18,
        boots=dict(color="#3d2c2a", cuff="#3d2c2a", h=0.06, toe=0.11),
        colors=dict(base="#9a3242", shawl="#dca64a", shawl_d="#a87522", skirt="#2f6166", skirt_d="#1c3d40", band="#c99a40", pants="#2f6166"),
    ),
    "old": dict(
        build="regular", seed=13.5,
        torso_w=0.74, torso_h=1.00, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.29, 0.48), arm=0.74, hip_x=0.15, leg=1.18, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.030, brow="stroke", brow_th=0.056, mouth="frown", moustache=False, smirk_side=1, age_lines=True,
        hat="newsboy", hat_style="stocking", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#c9584a", base="#a33b2e", dark="#6e231a", cuff="#8a3024", tassel="#e8d9b8"),
        hair=dict(color="#d9d2d8", front=0.06, grow=0.20),
        costume="oldcoat", boots=dict(color="#4a3a30", cuff="#4a3a30", h=0.08, toe=0.13),
        colors=dict(base="#6f7a62", dark="#454d3c", vest="#7a5034", vest_b="#d9b77a", shirt="#ece2cc", lapel="#5c664f", pocket="#606b54",
                    pants="#4a4250"),
    ),
    "soldier": dict(
        build="slim", seed=36.1,
        torso_w=0.66, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.74, hip_x=0.17, leg=1.30, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.020, brow="stroke", brow_th=0.046, mouth="frown", moustache=False, pencil_moustache=True, smirk_side=1,
        hat="newsboy", hat_style="tricorn", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#4a4552", base="#2b2731", dark="#19161d", shine="#9e98ad", lace="#f1ece0", cockade="#c7332b", brass="#e0c063"),
        hair=dict(color="#5a3a28", front=0.07, grow=0.22),
        costume="soldier", boots=dict(color="#1f1c22", cuff="#2c2830", h=0.30, toe=0.13),
        colors=dict(base="#2f55a3", vest="#efe9dc", facing="#c0362c", brass="#e0c063", stock="#20202a", belt="#f4f0e6", pants="#ece6d8"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D: every arm preset with hammer / book / lantern at yaw +-0.6 (mirrored: symmetric in x),
# squash 0.8..1.15, crouch, wide legs, steam + Z + sweat + tears, every STORY2 pose of the member; >= 0.32 D head room above that
# range (python3 test_cast2.py canvas).  The bell rope runs 3.6 D above the hand and is cut at the canvas top on purpose.
CANVAS2 = {
    "nico": (-1.6875, -3.8750, 1.6875, 0.1250),
    "padre": (-1.7500, -4.7500, 1.7500, 0.1875),
    "baker": (-1.6875, -4.5000, 1.6875, 0.1250),
    "woman": (-1.6250, -4.3750, 1.6250, 0.2500),
    "old": (-1.6875, -4.4375, 1.6875, 0.1250),
    "soldier": (-1.6875, -4.5625, 1.6875, 0.1250),
}


# ============================================================================= story poses
def _feet_y(cast, pose):
    return P.figure(cast, pose, "q")["feet_y"]


def _kneel_legs(C, side=1, depth=0.48):
    """kneeling legs (local targets): the front foot planted ahead with the knee up, the back knee on the ground and its shin
    lying behind.  side = +1 faces screen-right.  Ground line = hip + depth."""
    yh = TT + C["torso_h"] - 0.04 + 0.0
    hx = C["hip_x"]
    g = yh + depth
    L = C["leg"]
    front = (side * (hx + 0.40), g)
    back = (-side * (hx + 0.26), g - 0.03)
    return dict(foot_r=front if side > 0 else back, foot_l=back if side > 0 else front,
                knee_r=1.0 if side > 0 else -0.35, knee_l=0.35 if side > 0 else -1.0, toe_r=0.6 * side, toe_l=-0.6 * side), g


def _story():
    S = {}
    M = {}
    C = NEW_CAST2
    # --- nico
    S["nico_determined"] = ("nico", dict(yaw=0.3, expr="determined", head_roll=-4, arm_l="akimbo", arm_r=dict(hand=(0.40, 1.02), bend=0.6),
                                         legs="wide", lean=2))
    S["nico_worried"] = ("nico", dict(yaw=-0.3, pitch=0.35, expr="worried", fx=["sweat"], head_roll=6,
                                      arm_r=dict(hand=(0.06, 0.86), bend=0.8), arm_l=dict(hand=(-0.05, 0.90), bend=0.8), legs="narrow"))
    hold = dict(yaw=0.35, expr="determined", head_roll=-3, arm_l="down", legs="stand", prop_r=dict(type="rod", angle=-90))
    fy = _feet_y("nico", hold)
    hold["arm_r"] = dict(hand=(0.42, fy - 0.06 - 0.9), bend=0.7)
    S["nico_hold_rod"] = ("nico", hold)
    M["nico_hold_rod"] = dict(note="rod base rests on the floor beside the right foot; prop_tip_r = rod point")
    S["nico_carry_rod"] = ("nico", dict(yaw=0.7, expr="determined", legs=dict(preset="step", stride=0.8), lean=6,
                                        arm_r=dict(hand=(0.30, 0.42), bend=-0.6), arm_l=dict(hand=(-0.10, 0.63)),
                                        prop_r=dict(type="rod_mid", angle=-28)))
    legs, g = _kneel_legs(C["nico"], 1)
    hm = dict(yaw=0.55, pitch=-0.25, expr="determined", head_roll=-6, lean=8, legs=legs,
              arm_l=dict(hand=(0.48, g - 0.92), bend=-0.5, stretch=1.3), prop_l=dict(type="rod", angle=-90),
              arm_r=dict(hand=(0.68, 0.02), bend=-0.8, stretch=1.2), prop_r=dict(type="hammer", angle=-105))
    S["nico_hammer"] = ("nico", hm)
    M["nico_hammer"] = dict(note="kneeling on the roof edge; feet point = the roof surface; rod base on the roof, held by the left hand; "
                                  "animate arm_r/prop_r between this (raised) and STORY2_META['nico_hammer']['strike'] (head on the rod)",
                            strike=dict(arm_r=dict(hand=(0.16, 0.56), bend=-0.6), prop_r=dict(type="hammer", angle=-12)))
    S["nico_climb"] = ("nico", dict(yaw=0.85, pitch=-0.45, expr="determined", lean=6, head_roll=-6,
                                    arm_r=dict(hand=(0.60, -0.15), bend=-0.8, stretch=1.25), arm_l=dict(hand=(0.52, 0.48), bend=-0.4, stretch=1.3),
                                    legs=dict(preset="stand", lift_r=1.3, knee_r=1.0, toe_r=1.0, toe_l=0.8)))
    M["nico_climb"] = dict(note="climbing a ladder or the stair wall: the hands sit on rungs at x = +0.52..0.60 (put the ladder there)")
    pull = dict(yaw=0.35, pitch=-0.55, expr="determined", mouth="clench", head_roll=8, lean=-4, squash=(0.97, 1.04),
                arm_r=dict(hand=(0.58, -0.12), bend=-0.6, stretch=1.3), arm_l=dict(hand=(0.58, 0.36), bend=-0.5, stretch=1.3),
                prop_l=dict(type="bell_rope"),
                legs=dict(preset="stand", foot_l=(-0.22, 1.86), foot_r=(0.16, 1.78), knee_l=-0.6, knee_r=1.0, toe_l=-0.3, toe_r=0.5))
    S["nico_pull_rope"] = ("nico", pull)
    M["nico_pull_rope"] = dict(lift=0.32, note="feet off the ground: place the actor 'lift' D above the floor (actor.place(f, (x, y, lift)))")
    S["nico_read"] = ("nico", dict(yaw=0.15, pitch=0.9, expr="neutral", gaze=(0.2, 1.0), head_roll=5,
                                   arm_l=dict(hand=(-0.26, 0.98), bend=0.8), prop_l="book", arm_r=dict(hand=(-0.26 + BOOK_W, 0.98), bend=0.8)))
    M["nico_read"] = dict(note="the right hand sits on the book's right edge (anchors prop_tip_l)")
    # --- padre
    S["padre_order"] = ("padre", dict(yaw=-0.35, pitch=-0.6, expr="angry", head_roll=-7, lean=-3,
                                      arm_l=dict(hand=(-0.92, -0.22), shape="point", bend=-0.8, stretch=1.3), arm_r="akimbo", legs="wide"))
    S["padre_point_up"] = ("padre", dict(yaw=-0.3, pitch=-0.4, expr="smug", head_roll=-4,
                                         arm_l=dict(hand=(-0.92, -0.24), shape="point", bend=-0.8, stretch=1.3), arm_r="akimbo"))
    S["padre_laugh"] = ("padre", dict(yaw=0.15, expr="laughing", blink=2, mouth="talk_b", fx=["blush", "tears"], head_roll=14, lean=-6,
                                      head_dy=0.03, squash=(1.03, 0.97), t=0.3,
                                      arm_r=dict(hand=(0.24, 1.10), bend=0.9), arm_l=dict(hand=(-0.22, 1.14), bend=0.9), legs="wide"))
    S["padre_smug"] = ("padre", dict(yaw=0.3, pitch=-0.3, expr="smug", head_roll=5, arm_r="akimbo", arm_l="akimbo"))
    S["padre_arms_crossed"] = ("padre", dict(yaw=-0.2, pitch=-0.25, expr="smug", head_roll=-4,
                                             arm_l=dict(hand=(0.30, 0.86), bend=0.5, sharp=0.3), arm_r=dict(hand=(-0.32, 0.80), bend=-0.5, sharp=0.3)))
    sh = dict(yaw=0.4, pitch=-0.3, expr="smug", head_roll=6, arm_l="akimbo", prop_r=dict(type="rod", angle=-90))
    sh["arm_r"] = dict(hand=(0.86, 0.66), bend=-0.5)
    S["padre_smug_hand_rod"] = ("padre", sh)
    M["padre_smug_hand_rod"] = dict(note="offers the rod upright at arm's length; nico_hold_rod takes it")
    S["padre_ring"] = ("padre", dict(yaw=0.8, pitch=-0.3, expr="determined", head_roll=5, lean=3, legs="wide",
                                     arm_r=dict(hand=(0.60, -0.15), bend=-0.6, stretch=1.1), arm_l=dict(hand=(0.60, 0.56), bend=-0.5, stretch=1.3),
                                     prop_l=dict(type="bell_rope")))
    # --- extras
    S["extras_point_laugh"] = ("baker", dict(yaw=-0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=-10, lean=-5, t=0.6,
                                             arm_l=dict(hand=(-0.84, -0.26), shape="point", bend=-0.8, stretch=1.3), arm_r=dict(hand=(0.22, 1.02), bend=0.9)))
    S["extras_point_laugh_woman"] = ("woman", dict(yaw=0.4, pitch=-0.3, expr="laughing", head_roll=9, t=0.2, fx=["blush"],
                                                   arm_r=dict(hand=(0.76, -0.20), shape="point", bend=-0.8, stretch=1.3), arm_l="chin"))
    old = dict(yaw=0.3, expr="laughing", head_roll=10, lean=0, head_dx=-0.04, legs="stand", arm_l="down", prop_r=dict(type="stick", angle=96))
    fy = _feet_y("old", old)
    old["arm_r"] = dict(hand=P.hand_for_tip("stick", (0.62, fy - 0.035), 96), bend=0.5)
    S["extras_point_laugh_old"] = ("old", old)
    S["extras_ring"] = ("baker", dict(yaw=0.4, pitch=-0.3, expr="determined", mouth="clench", head_roll=4, lean=3, legs="wide",
                                      arm_r=dict(hand=(0.56, -0.15), bend=-0.6, stretch=1.1), arm_l=dict(hand=(0.56, 0.46), bend=-0.5, stretch=1.25),
                                      prop_l=dict(type="bell_rope")))
    S["extras_ring_woman"] = ("woman", dict(yaw=-0.4, pitch=-0.3, expr="worried", head_roll=-4, lean=-3,
                                            arm_l=dict(hand=(-0.55, -0.10), bend=-0.6, stretch=1.1), arm_r=dict(hand=(-0.55, 0.40), bend=-0.5, stretch=1.1),
                                            prop_r=dict(type="bell_rope")))
    st = dict(yaw=-0.3, expr="unimpressed", head_roll=-3, arm_l="down", prop_r=dict(type="stick", angle=92))
    fy = _feet_y("old", st)
    st["arm_r"] = dict(hand=P.hand_for_tip("stick", (0.55, fy - 0.035), 92), bend=0.5)
    S["old_stick"] = ("old", st)
    S["soldier_guard"] = ("soldier", dict(yaw=0.25, expr="unimpressed", arm_r="down", arm_l="behind", legs="narrow"))
    S["soldier_lantern"] = ("soldier", dict(yaw=-0.4, expr="neutral", arm_l=dict(hand=(-0.55, 0.62), bend=-0.3), prop_l="lantern", arm_r="down"))
    return S, M


STORY2, STORY2_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast2_registered", False):
        CE.register_stage()
        if not STORY2:
            s, m = _story()
            STORY2.update(s)
            STORY2_META.update(m)
        return
    for name in ("_ink_limb", "_prop", "_hand"):
        _O2[name] = getattr(P, name)
    P._ink_limb = _ink_limb
    P._prop = _prop
    P._hand = _hand
    CE.COSTUMES.update(COSTUMES2)
    CE.HATS.update(HATS2)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS2 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP2)
    _build_presets()
    for n, c in NEW_CAST2.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS2)
    s, m = _story()
    STORY2.update(s)
    STORY2_META.update(m)
    P.STORY.update(STORY2)
    P._cast2_registered = True
    CE.register_stage()


register()
