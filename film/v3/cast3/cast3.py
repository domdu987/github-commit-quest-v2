#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast3.py -- the cast of film 3 ("the sweating tank", Boston, January 1919) for the v2 puppet, as an extension module.

    import sys; sys.path.insert(0, ".../v3/cast3"); import cast3      # registers on import (idempotent); imports cast2 + cast_ext
    import puppet                                                     # the same module object, now with the new members
    f = puppet.figure("tommy", cast3.STORY3["tommy_paint"][1], "t")

Neither v2/puppet/puppet.py, v3/cast/cast_ext.py nor v3/cast2/cast2.py is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  workjacket, foreman, overalls, wintercoat           (dispatch: CAST[name]["costume"])
    cast_ext.HATS      flatnews, derby, earflap, knit                     (dispatch: CAST[name]["hat_style"])
    cast_ext.CANVAS    one feet-relative sprite canvas per member (cast_ext's import hook copies it into sprites.DEFAULT_CANVAS)
and wraps five puppet helpers on top of cast2's / cast_ext's wrappers (each falls through for everything it does not handle):
    _ink_limb   sleeves on the arms (CAST key "sleeve": rolled shirt / jacket sleeves, full coat sleeves)
    _face       beard (CAST key "beard"), cigar (POSE key "cigar": True, only drawn while the mouth is closed)
    _moustache  "bushy" moustache (CAST key moustache_style="bushy", colour colors["moustache"], size "tache_scale")
    _prop       tin_bucket, paintbrush, paintpot, wrench; "bucket" is drawn as the tin bucket for the film-3 members
                (the film-1 sand pail stays the "bucket" of every other member)
    _norm       records the "cigar" pose key
New cast:  tommy, foreman, worker1, worker2, kid1, kid2.
STORY3 / STORY3_META: the story poses (see API.md).  bucket_svg(): the bucket standing on the ground (fill / overflow).

Command line (QA):  python3 test_cast3.py        lineup.png, poses.png, canvas + head_flip checks, robustness run
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
for _d in (os.path.join(PROJ, "v3", "cast2"), os.path.join(PROJ, "v3", "cast")):
    if _d not in sys.path:
        sys.path.insert(0, _d)
import cast2 as C2      # noqa: E402  (v3/cast2, read-only; imports cast_ext and v2/puppet)
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW3 = ("tommy", "foreman", "worker1", "worker2", "kid1", "kid2")
TT = P.TORSO_TOP
_clamp, _smooth, _rot = P._clamp, P._smooth, P._rot
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_O3 = {}                      # the helpers this module wrapped
_POSE = [False]               # "cigar" key of the pose being drawn (set by the _norm wrapper)


def _cur():
    return CE._CUR[0]


def _mine():
    C = _cur()
    return C is not None and C.get("_cast3", False)


# ============================================================================= sleeves (arms)
def _limb_pts(S, E, H, kk, n=12):
    c = P._limb_ctrl(S, E, H, kk)
    pts = [c[0]]
    for a in (0, 3):
        p0, p1, p2, p3 = c[a], c[a + 1], c[a + 2], c[a + 3]
        for i in range(1, n + 1):
            t = i / float(n)
            u = 1.0 - t
            b0, b1, b2, b3 = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
            pts.append((b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0], b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]))
    return pts


def _sleeve(k, S, E, H, kk, w, SL):
    """a sleeve over the first SL["len"] of the arm (fraction of its length), SL["w"] wide, with a rolled cuff band (roll=True)
    or a plain cuff at its end.  The sleeve follows the rubber-hose curve; the ink arm continues out of the cuff."""
    pts = _limb_pts(S, E, H, kk)
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1]
    if tot < 1e-6:
        return ""
    L = SL.get("len", 0.5) * tot
    sel = [pts[0]]
    end, tan = pts[0], (0.0, 1.0)
    for i in range(1, len(pts)):
        if cum[i] >= L:
            f = (L - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            end = (pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f)
            sel.append(end)
            break
        sel.append(pts[i])
        end = pts[i]
    a = sel[-2] if len(sel) > 1 else S
    tx, ty = end[0] - a[0], end[1] - a[1]
    tl = math.hypot(tx, ty)
    if tl > 1e-9:
        tan = (tx / tl, ty / tl)
    sw = SL.get("w", 0.15)
    d = "M" + " L".join("%.4f,%.4f" % p for p in sel)
    col = k.c(SL["color"])
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, k.ink, sw + 0.034)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, col, sw))
    if L > 0.12:
        # a crease along the sleeve on its shade side
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.55" transform="translate(%.4f %.4f)"/>'
                 % ("M" + " L".join("%.4f,%.4f" % p for p in sel[1:-1] or sel), k.c(SL.get("dark", P._shade(SL["color"], 0.7))),
                    sw * 0.22, sw * 0.12))
    nx, ny = -tan[1], tan[0]
    cw = sw / 2 + (0.028 if SL.get("roll") else 0.016)
    cl = 0.075 if SL.get("roll") else 0.05
    c0 = (end[0] - tan[0] * cl, end[1] - tan[1] * cl)
    cuff = [(c0[0] + nx * cw, c0[1] + ny * cw), (end[0] + nx * cw, end[1] + ny * cw), (end[0] - nx * cw, end[1] - ny * cw), (c0[0] - nx * cw, c0[1] - ny * cw)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(cuff) if SL.get("roll") else _poly_d(cuff),
                                                                                                   k.c(SL.get("cuff", SL["color"])), k.ink))
    if SL.get("roll"):
        m = ((c0[0] + end[0]) / 2, (c0[1] + end[1]) / 2)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>'
                 % (m[0] + nx * cw * 0.8, m[1] + ny * cw * 0.8, m[0] - nx * cw * 0.8, m[1] - ny * cw * 0.8, k.c(SL.get("dark", "#888888"))))
    for p in (S, end):
        k.ext.append((p[0], p[1], sw / 2 + 0.03))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O3["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = _cur()
    if tail is None and C is not None and C.get("sleeve"):
        out += _sleeve(k, S, E, H, kk, w, C["sleeve"])
    return out


# ============================================================================= face: beard, cigar, bushy moustache
_OPEN = ("talk_a", "talk_b", "talk_o", "o", "grin", "clench")


def _mouth_open(P_):
    m = P_.get("mouth")
    if isinstance(m, tuple):
        return True
    if m is None or m == "default":
        m = (P.EXPRESSIONS.get(P_["expr"]) or P.EXPRESSIONS["neutral"])["mouth"]
    return m in _OPEN


def _beard(k, C, P_, L):
    """full short beard on the lower face (clipped to the head fill), mouth drawn over it."""
    B = C["beard"]
    sx = L["mx"]
    my = L["my"]
    top = my - 0.065
    d = ("M%.4f,%.4f L%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f L%.4f,%.4f "
         "L0.70,0.80 L-0.70,0.80 Z"
         % (-0.70, -0.02, sx - 0.40, -0.02, sx - 0.36, top - 0.05, sx - 0.26, top + 0.02, sx - 0.14, top,
            sx, top - 0.025, sx + 0.14, top, sx + 0.26, top + 0.02, sx + 0.36, top - 0.05, sx + 0.40, -0.02, 0.70, -0.02))
    col = k.c(B["color"])
    o = ['<g clip-path="url(#%s_hc)">' % k.uid]
    o.append('<path d="%s" fill="%s"/>' % (d, col))
    hs = "".join("M%.4f,%.4f q%.4f,0.035 %.4f,0.070 " % (sx + x, top + 0.10 + 0.08 * abs(x), 0.01 * (1 if x > 0 else -1), 0.02 * (1 if x > 0 else -1))
                 for x in (-0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (hs, k.c(B.get("dark", "#5a3020"))))
    o.append('<path d="M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" '
             'stroke-width="0.014" stroke-linecap="round" opacity="0.6"/>'
             % (sx - 0.40, -0.02, sx - 0.36, top - 0.05, sx - 0.26, top + 0.02, sx - 0.14, top, sx, top - 0.025, sx + 0.14, top, sx + 0.26, top + 0.02,
                sx + 0.36, top - 0.05, sx + 0.40, -0.02, k.c(B.get("dark", "#5a3020"))))
    o.append('</g>')
    return "".join(o)


def _cigar(k, C, P_, L):
    side = 1.0 if P_["yaw"] >= 0.0 else -1.0
    x0, y0 = L["mx"] + side * 0.085, L["my"] + 0.012
    ang = 18.0 if side > 0 else 162.0
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (x0, y0, ang)]
    o.append('<path d="M0,-0.024 L0.20,-0.026 Q0.215,0 0.20,0.026 L0,0.024 Q-0.012,0 0,-0.024 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (k.c("#7a4a2a"), k.ink))
    o.append('<path d="M0.035,-0.025 L0.035,0.025" stroke="%s" stroke-width="0.020"/>' % k.c("#c9a24a"))
    o.append('<path d="M0.17,-0.026 L0.205,-0.026 Q0.22,0 0.205,0.026 L0.17,0.026 Z" fill="%s"/>' % k.c("#9c9496"))
    o.append('<circle cx="0.212" cy="0" r="0.012" fill="%s"/>' % k.c("#ff6a2a"))
    o.append('</g>')
    tx, ty = x0 + 0.22 * math.cos(math.radians(ang)), y0 + 0.22 * math.sin(math.radians(ang))
    o.append('<path d="M%.4f,%.4f q%.4f,-0.06 0,-0.12 q%.4f,-0.06 0,-0.12" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>'
             % (tx, ty - 0.02, 0.04 * side, -0.04 * side, k.c("#e8e2ea")))
    k.ext.append((tx, ty, 0.03))
    k.ext.append((tx, ty - 0.27, 0.03))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O3["_face"](k, C, P_, white)
    if C is None or not C.get("_cast3"):
        return svg, L
    under, over = [], []
    if C.get("beard"):
        under.append(_beard(k, C, P_, L))
    if _POSE[0] and C.get("cigar_ok") and not _mouth_open(P_) and P_["blink"] < 2:
        over.append(_cigar(k, C, P_, L))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _moustache(k, mx, my, s=1.0):
    C = _cur()
    if not C or C.get("moustache_style") != "bushy":
        return _O3["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#4a2a1c")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    # thick drooping walrus: wide brush over the upper lip, ends hanging past the mouth corners
    pts = [Q(0.0, -0.060), Q(-0.12, -0.080), Q(-0.225, -0.050), Q(-0.275, 0.030), Q(-0.262, 0.135), Q(-0.215, 0.110), Q(-0.170, 0.070),
           Q(-0.090, 0.058), Q(0.0, 0.070), Q(0.090, 0.058), Q(0.170, 0.070), Q(0.215, 0.110), Q(0.262, 0.135), Q(0.275, 0.030),
           Q(0.225, -0.050), Q(0.12, -0.080)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)]
    st = []
    for x in (-0.20, -0.13, -0.06, 0.06, 0.13, 0.20):
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (Q(x * 0.8, -0.04) + Q(x * 1.05, 0.015) + Q(x * 1.12, 0.06)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
             % ("".join(st), k.c(C["colors"].get("moustache_l", P._shade(col, 1.45)))))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (Q(0.0, -0.055) + Q(0.0, 0.020) + (k.ink,)))
    return "".join(o)


def _norm(C, pose):
    _POSE[0] = bool(pose.get("cigar")) if isinstance(pose, dict) else False
    return _O3["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _suspenders(k, X, col, ys, ye, xs=0.085):
    o = []
    for s in (-1, 1):
        pts = [X(s * xs * 1.25, ys), X(s * xs, ye)]
        o.append(_ln(pts, k.ink, 0.052))
        o.append(_ln(pts, k.c(col["susp"]), 0.032))
        o.append(_circ(X(s * xs, ye - 0.01), 0.018, k.c(col["susp_b"]), k, 0.008))
    return "".join(o)


def _cos_workjacket(k, C, m):
    """tommy: oversized grey-blue work jacket hanging open over a cream shirt and brown suspenders, brown trouser bowl, big
    patch pockets on the jacket skirt, chest pocket; red knitted winter scarf round the neck, one end hanging down the chest."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    o.append(_poly(k, [X(-0.13, 0.38), X(0.13, 0.38), X(0.11, yb + 0.03), X(-0.11, yb + 0.03)], k.c(col["shirt"]), 0.0, "none"))
    o.append(_suspenders(k, X, col, 0.40, yb + 0.05))
    for s in (-1, 1):
        # jacket front edge + lapel
        o.append(_poly(k, [X(s * 0.13, 0.385), X(s * 0.27, 0.43), X(s * 0.15, 0.66), X(s * 0.12, 0.62)], k.c(col["lapel"]), 0.014))
        o.append(_ln([X(s * 0.12, 0.62), X(s * 0.115, yb + 0.06)], k.ink, 0.020))
    # chest pocket (screen-left) with a pencil stub
    o.append(_poly(k, [X(-0.34, 0.70), X(-0.20, 0.70), X(-0.205, 0.80), X(-0.335, 0.80)], k.c(col["pocket"]), 0.012))
    o.append(_ln([X(-0.30, 0.70), X(-0.31, 0.64)], k.c("#d9b24a"), 0.022))
    # a darn patch on the right side
    c = X(0.27, 0.86)
    o.append('<path d="M%.4f,%.4f l0.045,0.03 M%.4f,%.4f l0.045,-0.03 M%.4f,%.4f l0.045,0.03" stroke="%s" stroke-width="0.009" fill="none" stroke-linecap="round"/>'
             % (c[0] - 0.02, c[1] - 0.04, c[0] - 0.02, c[1] + 0.0, c[0] - 0.02, c[1] + 0.02, k.c(col["dark"])))
    inside = "".join(o)
    # jacket skirt: two panels from the open front to the (flared) sides, over the trouser bowl
    yt = yb - 0.04
    a = m.hwa * 0.985
    hem = yB + C.get("jacket_len", 0.16)
    fl = C.get("jacket_flare", 0.06)
    g = "url(#%s_tg)" % k.uid
    ov = []
    for s in (-1, 1):
        pts = [X(s * a, yt), X(s * (a + fl * 0.6), (yt + hem) / 2), X(s * (a + fl), hem), X(s * 0.115, hem + 0.015), X(s * 0.115, yt)]
        ov.append('<path d="%s" fill="%s"/>' % (_poly_d(pts), g))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
                  % (pts[0] + pts[1] + pts[2] + pts[3] + pts[4] + (k.ink,)))
        px0, px1 = (0.15, 0.36)
        pk = [X(s * px0, yt + 0.08), X(s * px1, yt + 0.08), X(s * (px1 - 0.005), hem - 0.05), X(s * (px0 + 0.005), hem - 0.05)]
        ov.append(_poly(k, pk, k.c(col["pocket"]), 0.013))
        ov.append(_ln([X(s * px0, yt + 0.115), X(s * px1, yt + 0.115)], k.c(col["dark"]), 0.010, ' opacity="0.7"'))
        k.ext.append((pts[2][0], pts[2][1], 0.04))
    # buttons on the screen-right front edge (the jacket would button there)
    for y in (0.72, yb - 0.02, yt + 0.10):
        ov.append(_circ(X(0.155, y), 0.022, k.c(col["button"]), k, 0.008))
    # scarf: a band round the neck (shows beside the chin), a knot and one end hanging down the chest
    sc, scd = k.c(col["scarf"]), k.c(col["scarf_d"])
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.33, 0.405) + X(0.0, 0.62) + X(0.33, 0.405))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.150" stroke-linecap="round"/>' % (band, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.112" stroke-linecap="round"/>' % (band, sc))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
              % (X(-0.30, 0.43) + X(0.0, 0.60) + X(0.30, 0.43) + (scd,)))
    kx, ky = X(0.13, 0.55)
    tail = [(kx - 0.055, ky), (kx + 0.065, ky + 0.01), (kx + 0.095, ky + 0.40), (kx - 0.025, ky + 0.42)]
    ov.append(_poly(k, tail, sc, 0.016))
    for f in (0.55, 0.72):
        yy = ky + 0.41 * f
        ov.append(_ln([(kx - 0.052 + 0.07 * f * 0.4, yy), (kx + 0.06 + 0.035 * f, yy + 0.004)], k.c(col["scarf_s"]), 0.020))
    fr = "".join("M%.4f,%.4f l%.4f,0.055 " % (kx - 0.02 + 0.03 * i, ky + 0.415 + 0.004 * i, 0.004 * (i - 1.5)) for i in range(4))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (fr, scd))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.062" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, sc, k.ink))
    k.ext.append((kx, ky + 0.48, 0.03))
    return inside, "", "".join(ov)


def _cos_foreman(k, C, m):
    """foreman: brown waistcoat (V neck, pointed fronts, five buttons, two welt pockets, a pocket-watch chain swagged from the
    button to the screen-right pocket) over a white collarless shirt with a collar stud; dark trouser bowl."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    hw = m.hwa
    o = [CE._bowl(k, col["pants"], yb, yB)]
    # shirt: collar band + stud, a few folds on the shoulders
    o.append('<path d="M%.4f,0.40 Q%.4f,0.52 %.4f,0.40" fill="none" stroke="%s" stroke-width="0.040"/>' % (X(-0.17, 0.4)[0], X(0, 0.5)[0], X(0.17, 0.4)[0], k.c(col["shirt_d"])))
    o.append(_circ(X(0.0, 0.50), 0.016, k.c(col["brass"]), k, 0.007))
    g = C2._grad(k, "wc", col["vest"], -hw, hw)
    for s in (-1, 1):
        pts = [X(s * 0.30, 0.37), X(s * 0.12, 0.38), X(s * 0.012, 0.74), X(s * 0.012, yb + 0.07), X(s * 0.30, yb + 0.02), X(s * 0.95, yb - 0.01),
               X(s * 0.95, 0.92), X(s * 0.62, 0.70), X(s * 0.42, 0.52)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(pts), g, k.ink))
        # welt pocket
        o.append(_ln([X(s * 0.22, 0.98), X(s * 0.40, 0.975)], k.c(col["vest_d"]), 0.026))
        o.append(_ln([X(s * 0.22, 0.98), X(s * 0.40, 0.975)], k.ink, 0.008, ' opacity="0.6"'))
    o.append(_ln([X(0.0, 0.74), X(0.0, yb + 0.07)], k.ink, 0.014))
    ys = [0.79 + i * (yb - 0.02 - 0.79) / 4.0 for i in range(5)]
    for y in ys:
        o.append(_circ(X(0.0, y), 0.022, k.c(col["button"]), k, 0.008))
    # watch chain: from the third button to the screen-right pocket, a fob at the pocket
    a0, a1 = X(0.0, ys[2]), X(0.30, 0.975)
    cm = X(0.16, ys[2] + 0.14)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a0 + cm + a1)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (d, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" stroke-dasharray="0.018 0.010"/>' % (d, k.c(col["brass"])))
    o.append(_circ(a1, 0.024, k.c(col["brass"]), k, 0.008))
    inside = "".join(o)
    return inside, "", ""


def _cos_overalls(k, C, m):
    """dock worker: bib overalls (bib with a pocket and stitching, straps over the shoulders with brass buttons, the overall
    trousers as the bowl) over a work shirt (plaid when colors["check"] is given), open collar."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    u = k.uid
    o = []
    if col.get("check"):
        k.defs.append('<pattern id="%s_pl" width="0.12" height="0.12" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                      '<rect width="0.12" height="0.045" fill="%s" opacity="0.55"/><rect width="0.045" height="0.12" fill="%s" opacity="0.45"/></pattern>'
                      % (u, m.c, k.c(col["check"]), k.c(col["check"])))
        o.append('<rect x="-0.8" y="0.3" width="1.6" height="1.4" fill="url(#%s_pl)"/>' % u)
    # open collar
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.16, 0.40), X(s * 0.02, 0.47), X(s * 0.14, 0.56)], k.c(col["collar"]), 0.013))
    o.append(_poly(k, [X(-0.03, 0.44), X(0.03, 0.44), X(0.0, 0.58)], k.c(P.HEAD_FILL), 0.0, "none"))
    den = k.c(col["denim"])
    o.append(CE._bowl(k, col["denim"], yb - 0.02, yB, dip=0.02))
    bib = [X(-0.21, 0.60), X(0.21, 0.60), X(0.23, yb), X(-0.23, yb)]
    o.append(_poly(k, bib, den, 0.016))
    st = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" % (X(-0.185, yb - 0.01) + X(-0.18, 0.63) + X(0.18, 0.63))
    st += " L%.4f,%.4f" % X(0.185, yb - 0.01)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-dasharray="0.02 0.014" opacity="0.9"/>' % (st, k.c(col["stitch"])))
    o.append(_poly(k, [X(-0.11, 0.70), X(0.11, 0.70), X(0.10, 0.84), X(-0.10, 0.84)], k.c(col["denim_d"]), 0.012))
    o.append(_ln([X(-0.05, 0.70), X(-0.05, 0.63)], k.c(col.get("pencil", "#d9b24a")), 0.020))
    for s in (-1, 1):
        pts = [X(s * 0.18, 0.62), X(s * 0.30, 0.37)]
        o.append(_ln(pts, k.ink, 0.075))
        o.append(_ln(pts, den, 0.052))
        o.append(_circ(X(s * 0.175, 0.635), 0.025, k.c(col["brass"]), k, 0.009))
    # side buttons / pocket edges on the bowl
    for s in (-1, 1):
        o.append(_ln([X(s * 0.30, yb + 0.02), X(s * 0.36, yB)], k.c(col["denim_d"]), 0.014))
    return "".join(o), "", ""


def _cos_wintercoat(k, C, m):
    """street kid: winter coat, big turned-down collar, double row of big buttons, two flap pockets, the skirt of the coat
    flaring over the legs (longer for the girl, with a hem band)."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    o = []
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.02, 0.40), X(s * 0.30, 0.38), X(s * 0.30, 0.56), X(s * 0.06, 0.62)], k.c(col["collar"]), 0.016))
        for y in (0.68, 0.80, 0.92):
            o.append(_circ(X(s * 0.10, y), 0.026, k.c(col["button"]), k, 0.009))
    o.append(_ln([X(0.0, 0.62), X(0.0, yB)], k.c(col["dark"]), 0.012))
    if col.get("patch"):
        c = X(-0.20, 0.82)
        o.append('<rect x="%.4f" y="%.4f" width="0.10" height="0.09" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(8 %.4f %.4f)"/>'
                 % (c[0] - 0.05, c[1] - 0.045, k.c(col["patch"]), k.ink, c[0], c[1]))
    inside = "".join(o)
    yt = TT + 0.70 * h
    a = m.hwa * 0.97
    hem = yB + C.get("coat_len", 0.20)
    b = m.hwa + C.get("coat_flare", 0.08)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "ct", X, yt, a, hem, b, g, sw=0.026, folds=((-0.08, yt + 0.12, -0.12, hem - 0.03), (0.10, yt + 0.12, 0.14, hem - 0.03)),
                    fold_col=k.c(col["dark"]))]
    ov.append(_ln([X(0.0, yt), X(0.0, hem)], k.c(col["dark"]), 0.012))
    for s in (-1, 1):
        ov.append(_poly(k, [X(s * 0.12, yt + 0.06), X(s * 0.30, yt + 0.06), X(s * 0.29, yt + 0.12), X(s * 0.13, yt + 0.12)], k.c(col["dark"]), 0.012))
    if col.get("band"):
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030"/>'
                  % (X(-b + 0.02, hem - 0.045) + X(0, hem - 0.015) + X(b - 0.02, hem - 0.045) + (k.c(col["band"]),)))
    if col.get("belt"):
        ov.append(_ln([X(-a, yt - 0.01), X(a, yt - 0.01)], k.ink, 0.060))
        ov.append(_ln([X(-a, yt - 0.01), X(a, yt - 0.01)], k.c(col["belt"]), 0.040))
    return inside, "", "".join(ov)


COSTUMES3 = {"workjacket": _cos_workjacket, "foreman": _cos_foreman, "overalls": _cos_overalls, "wintercoat": _cos_wintercoat}


# ============================================================================= hats (head frame)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_flatnews(k, C, yaw):
    """tommy (and the dock workers in other cloth): soft flat newsboy cap, the puffy top overhanging the short stiff peak toward
    the face, one top button, two panel seams, a band line."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    vx = 0.24 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.50, x1=0.50, mid=0.30)
    xl, xr, yb = -0.465 + dx, 0.465 + dx, -0.262
    pf = C.get("cap_puff", 1.0)
    ox = 0.07 * yaw
    top = P._smooth_open([(xl, yb), (xl - 0.05 * pf, yb - 0.11), (dx - 0.30 + ox, -0.545 - 0.02 * pf), (dx + 0.06 + ox, -0.585 - 0.02 * pf),
                          (xr + 0.03 * pf, -0.47), (xr + 0.06 * pf, yb - 0.06), (xr, yb)])
    d = top + " Q%.4f,%.4f %.4f,%.4f Z" % (vx * 0.5, yb + 0.03, xl, yb)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    hv = 0.34 - 0.07 * abs(yaw)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (vx - hv, yb, vx, yb + 0.10, vx + hv, yb, vx, yb + 0.025, vx - hv, yb, k.c(col["visor"]), k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    bx, by = dx + 0.04 + ox, -0.585 - 0.02 * pf
    for f in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
                 % (bx, by + 0.02, bx + f * 0.24, by + 0.07, dx + f * 0.36, yb - 0.07, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (xl + 0.02, yb - 0.05, dx, yb - 0.02, xr - 0.02, yb - 0.05, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
             % (xl + 0.03, yb - 0.10, dx - 0.30, -0.50, dx - 0.10, -0.55, k.c(col["shine"])))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.024" fill="%s" stroke="%s" stroke-width="0.011"/>' % (bx, by + 0.012, k.c(col["dark"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.06, yb - 0.1), (xr + 0.07, yb - 0.06), (dx, by - 0.04), (vx, yb + 0.11)))
    return "".join(o), (bx, by)


def _hat_derby(k, C, yaw):
    """foreman: chocolate-brown derby (bowler) with a tall round crown, wide dark band with a bow, brim rolled up at the sides;
    no hair tufts.  Taller and darker than senior_b's pale bowler."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fdx = 0.20 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.44, x1=0.44, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    dome = "M%.4f,-0.380 C%.4f,-0.62 %.4f,-0.745 %.4f,-0.745 C%.4f,-0.745 %.4f,-0.62 %.4f,-0.380 Z" % (
        -0.43 + dx, -0.43 + dx, -0.22 + dx, dx, 0.22 + dx, 0.43 + dx, 0.43 + dx)
    o.append('<path d="%s" fill="%s"/>' % (dome, g))
    o.append('<path d="M%.4f,-0.48 Q%.4f,-0.66 %.4f,-0.71" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (-0.33 + dx, -0.26 + dx, -0.06 + dx, k.c(col["shine"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (dome, k.ink))
    o.append('<path d="M%.4f,-0.455 Q%.4f,-0.430 %.4f,-0.455 L%.4f,-0.380 L%.4f,-0.380 Z" fill="%s" stroke="%s" stroke-width="0.011"/>'
             % (-0.425 + dx, dx, 0.425 + dx, 0.43 + dx, -0.43 + dx, k.c(col["band"]), k.ink))
    bx = -0.30 + 0.12 * yaw
    o.append('<path d="M%.4f,-0.445 l0.05,0.02 l-0.05,0.02 Z M%.4f,-0.445 l-0.05,0.02 l0.05,0.02 Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
             % (bx, bx, k.c(col["band"]), k.ink))
    o.append('<path d="M-0.60,-0.410 Q-0.62,-0.330 -0.42,-0.318 Q%.4f,-0.232 0.42,-0.318 Q0.62,-0.330 0.60,-0.410 Q0.32,-0.352 %.4f,-0.356 '
             'Q-0.32,-0.352 -0.60,-0.410 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (fdx, fdx * 0.3, k.c(col["brim"]), k.ink))
    o.append('<path d="M-0.43,-0.340 Q%.4f,-0.270 0.41,-0.340" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.9"/>'
             % (fdx, k.c(col["edge"])))
    o.append('</g>')
    _ext_hat(k, C, ((-0.64, -0.41), (0.64, -0.41), (-0.25, -0.76), (0.25, -0.76), (fdx, -0.22)))
    return "".join(o), (dx, -0.745)


def _hat_earflap(k, C, yaw):
    """kid1: brown leather aviator cap with fleece trim and two ear flaps hanging over the ears (tie strings), the flap on
    the side the face turns to slides in and shrinks."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    sx = dx - 0.10 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.47, x1=0.47, mid=0.32)
    xl, xr, yb, top = -0.47 + dx, 0.47 + dx, -0.25, -0.60
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    for s in (-1, 1):
        gg = _clamp(1.0 - 0.6 * max(0.0, s * yaw), 0.3, 1.0)
        x0 = s * 0.47 + dx
        fl = [(x0 - s * 0.16 * gg, yb + 0.02), (x0 + s * 0.02, yb + 0.02), (x0 + s * 0.03, 0.02), (x0 - s * 0.06 * gg, 0.07), (x0 - s * 0.15 * gg, 0.03)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(fl), k.c(col["base"]), k.ink))
        o.append('<path d="M%.4f,%.4f q%.4f,0.10 %.4f,0.16" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                 % (x0 - s * 0.04 * gg, 0.06, s * 0.02, -s * 0.01, k.ink))
        k.ext.append((x0 + s * 0.04, 0.0, 0.03))
        k.ext.append((x0 - s * 0.05, 0.24, 0.02))
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
            % (xl, yb, xl - 0.02, yb - 0.25, sx - 0.32, top, sx, top, sx + 0.32, top, xr + 0.02, yb - 0.25, xr, yb))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (sx, top + 0.01, sx + 0.02, top + 0.15, dx + 0.02, yb - 0.04, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>'
             % (xl + 0.07, yb - 0.10, xl + 0.12, top + 0.10, sx - 0.15, top + 0.03, k.c(col["shine"])))
    fur = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
           % (xl - 0.01, yb - 0.06, dx, yb - 0.02, xr + 0.01, yb - 0.06, xr, yb + 0.02, dx, yb + 0.06, xl, yb + 0.02))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (fur, k.c(col["fur"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.03, yb), (xr + 0.03, yb), (sx, top - 0.03)))
    return "".join(o), (sx, top)


def _hat_knit(k, C, yaw):
    """kid2: knitted hat with a ribbed cuff, two stripes and a big pompom, two plaits hanging below it at the sides."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    sx = dx - 0.08 * yaw
    hc = k.c(C["hair"]["color"])
    o = []
    for s in (-1, 1):
        x = s * 0.47 + dx - 0.04 * yaw
        beads = [(x + s * 0.010 * i, -0.17 + 0.105 * i) for i in range(5)]
        for (bxx, byy) in beads:
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.066" fill="%s" stroke="%s" stroke-width="0.016"/>' % (bxx, byy, hc, k.ink))
        e = beads[-1]
        o.append('<path d="M%.4f,%.4f l-0.03,0.09 l0.06,0 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (e[0], e[1] + 0.05, hc, k.ink))
        o.append(_circ((e[0], e[1] + 0.05), 0.026, k.c(col["ribbon"]), k, 0.008))
        k.ext.append((e[0], e[1] + 0.15, 0.07))
    g = CE._gradient(k, "ht", col, x0=-0.48, x1=0.48, mid=0.32)
    xl, xr, yb, top = -0.48 + dx, 0.48 + dx, -0.245, -0.655
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
            % (xl, yb, xl - 0.03, yb - 0.27, sx - 0.33, top, sx, top, sx + 0.33, top, xr + 0.03, yb - 0.27, xr, yb))
    u = k.uid
    k.defs.append('<clipPath id="%s_kc"><path d="%s"/></clipPath>' % (u, dome))
    o.append('<path d="%s" fill="%s"/>' % (dome, g))
    o.append('<g clip-path="url(#%s_kc)">' % u)
    for y in (-0.47, -0.39):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040"/>' % (xl - 0.05, y + 0.02, dx, y - 0.02, xr + 0.05, y + 0.02, k.c(col["stripe"])))
    o.append('</g>')
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, k.ink))
    cuff = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl - 0.015, yb - 0.085, dx, yb - 0.045, xr + 0.015, yb - 0.085, xr + 0.008, yb + 0.015, dx, yb + 0.055, xl - 0.008, yb + 0.015))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (cuff, k.c(col["cuff"]), k.ink))
    rib = "".join("M%.4f,%.4f L%.4f,%.4f " % (dx + x, yb - 0.06 + 0.04 * (x / 0.45) ** 2, dx + x, yb + 0.01 + 0.035 * (1 - (x / 0.45) ** 2))
                  for x in [i * 0.075 - 0.375 for i in range(11)])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (rib, k.c(col["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.105" fill="%s" stroke="%s" stroke-width="0.022"/>' % (sx, top - 0.06, k.c(col["pom"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.050" fill="#ffffff" opacity="0.45"/>' % (sx - 0.035, top - 0.095))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.03, yb), (xr + 0.03, yb), (sx, top - 0.17)))
    return "".join(o), (sx, top - 0.165)


HATS3 = {"flatnews": _hat_flatnews, "derby": _hat_derby, "earflap": _hat_earflap, "knit": _hat_knit}


# ============================================================================= props
NEW_PROPS3 = ("tin_bucket", "paintbrush", "paintpot", "wrench")
# working point distance from the gripping hand (D): tin_bucket / paintpot = bottom centre below the hand (they hang upright),
# paintbrush = bristle edge, wrench = jaw centre
NEW_TIP3 = {"tin_bucket": 0.47, "paintbrush": 0.46, "paintpot": 0.38, "wrench": 0.58}
MOLASSES, MOLASSES_L, MOLASSES_D = "#6b3410", "#a8601e", "#3e1c08"


def _tin_bucket_body(k, fill=0.0, overflow=0.0, uidx="tb"):
    """the tin bucket in its own frame: bail top at (0, 0), rim at y 0.17, bottom centre at (0, 0.47)."""
    u = k.uid
    ink = k.ink
    k.defs.append('<linearGradient id="%s_%s" gradientUnits="userSpaceOnUse" x1="-0.17" y1="0" x2="0.17" y2="0"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, uidx, k.c("#d6dde4"), k.c("#a9b4be"), k.c("#6f7a86")))
    o = []
    o.append('<path d="M-0.165,0.175 L0.165,0.175 L0.130,0.465 Q0,0.482 -0.130,0.465 Z" fill="url(#%s_%s)" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (u, uidx, ink))
    for y, x in ((0.27, 0.153), (0.38, 0.141)):
        o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (-x, y, y + 0.02, x, y, k.c("#5f6874")))
    o.append('<path d="M-0.105,0.21 L-0.090,0.44" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>')
    o.append('<path d="M0.07,0.31 q0.025,0.02 0.010,0.05" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c("#5f6874"))
    if fill > 0.0 or overflow > 0.0:
        o.append('<ellipse cx="0" cy="0.180" rx="0.150" ry="0.030" fill="%s"/>' % k.c(MOLASSES))
        o.append('<path d="M-0.10,0.175 Q-0.03,0.165 0.06,0.172" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(MOLASSES_L))
    else:
        o.append('<ellipse cx="0" cy="0.180" rx="0.150" ry="0.028" fill="%s"/>' % k.c("#4f5862"))
    o.append('<ellipse cx="0" cy="0.175" rx="0.168" ry="0.034" fill="none" stroke="%s" stroke-width="0.020"/>' % ink)
    o.append('<path d="M-0.150,0.168 Q0,0.150 0.150,0.168" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c("#eef2f6"))
    if overflow > 0.0:
        f = _clamp(overflow, 0.0, 1.0)
        for (x0, ln, w) in ((-0.15, 0.20, 0.040), (-0.02, 0.13, 0.034), (0.13, 0.26, 0.044)):
            x1 = x0 * (0.82 if abs(x0) > 0.1 else 1.0)
            L = ln * f
            o.append('<path d="M%.4f,0.18 L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (x0, x1, 0.18 + L, k.ink, w + 0.02))
            o.append('<path d="M%.4f,0.18 L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (x0, x1, 0.18 + L, k.c(MOLASSES), w))
        o.append('<path d="M-0.17,0.185 Q0,0.235 0.17,0.185 Q0.17,0.150 0,0.150 Q-0.17,0.150 -0.17,0.185 Z" fill="%s" stroke="%s" stroke-width="0.014"/>'
                 % (k.c(MOLASSES), ink))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind == "bucket" and _mine():
        kind = "tin_bucket"
    if kind not in NEW_PROPS3:
        return _O3["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    if kind in ("tin_bucket", "paintpot"):
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        if kind == "tin_bucket":
            bail = "M-0.162,0.180 Q-0.150,-0.030 0,-0.022 Q0.150,-0.030 0.162,0.180"
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (bail, ink))
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (bail, k.c("#c3cad3")))
            o.append(_tin_bucket_body(k))
            ends = ((-0.18, 0.18), (0.18, 0.18), (0.0, 0.48), (0.0, -0.03))
        else:
            # paint pot: small tin pot hanging from its wire bail, brown paint on the rim and running down the side
            bail = "M-0.125,0.120 Q-0.115,-0.025 0,-0.020 Q0.115,-0.025 0.125,0.120"
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (bail, ink))
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (bail, k.c("#c3cad3")))
            o.append('<path d="M-0.130,0.115 L0.130,0.115 L0.125,0.375 Q0,0.390 -0.125,0.375 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
                     % (k.c("#9aa3ad"), ink))
            o.append('<rect x="-0.128" y="0.18" width="0.255" height="0.11" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#e8d9b0"), ink))
            o.append('<circle cx="0" cy="0.235" r="0.035" fill="%s"/>' % k.c(MOLASSES_L))
            o.append('<ellipse cx="0" cy="0.118" rx="0.128" ry="0.026" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(MOLASSES), ink))
            o.append('<path d="M0.07,0.12 L0.075,0.25" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % ink)
            o.append('<path d="M0.07,0.12 L0.075,0.25" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % k.c(MOLASSES))
            o.append('<path d="M-0.08,0.12 L-0.082,0.19" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % ink)
            o.append('<path d="M-0.08,0.12 L-0.082,0.19" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(MOLASSES))
            ends = ((-0.14, 0.12), (0.14, 0.12), (0.0, 0.39), (0.0, -0.025))
        o.append('</g>')
        for e in ends:
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return "".join(o), (H[0], H[1] + NEW_TIP3[kind] * sc)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind == "paintbrush":
        # wide flat house-painting brush: wooden handle, tin ferrule, bristles 0.15 wide, brown paint on the tips
        o.append('<path d="M-0.13,-0.022 Q-0.15,0 -0.13,0.022 L0.22,0.030 L0.22,-0.030 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#c08a52"), ink))
        o.append('<path d="M-0.10,-0.008 L0.20,-0.012" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c("#e2b47e"))
        o.append('<path d="M0.22,-0.060 L0.30,-0.070 L0.30,0.070 L0.22,0.060 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#b6bec8"), ink))
        o.append('<path d="M0.30,-0.075 L0.42,-0.078 L0.46,-0.070 L0.46,0.070 L0.42,0.078 L0.30,0.075 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#d9b77a"), ink))
        o.append('<path d="M0.385,-0.077 L0.46,-0.070 L0.46,0.070 L0.385,0.077 Q0.40,0.03 0.375,0.0 Q0.40,-0.04 0.385,-0.077 Z" fill="%s"/>' % k.c(MOLASSES))
        o.append('<path d="M0.32,-0.045 L0.44,-0.045 M0.32,0.0 L0.44,0.0 M0.32,0.045 L0.44,0.045" stroke="%s" stroke-width="0.007" opacity="0.6"/>' % k.c("#7a5a30"))
        ends = ((-0.15, 0.0), (0.46, -0.08), (0.46, 0.08))
    else:  # wrench: big monkey wrench, handle along +x, adjustable jaws at the far end
        o.append('<path d="M-0.10,-0.030 L0.46,-0.026 L0.46,0.026 L-0.10,0.030 Q-0.13,0 -0.10,-0.030 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#6f7884"), ink))
        o.append('<path d="M-0.08,-0.034 L0.16,-0.032 L0.16,0.032 L-0.08,0.034 Z" fill="%s" stroke="%s" stroke-width="0.011"/>' % (k.c("#7a4a2a"), ink))
        o.append('<path d="M0.44,-0.13 L0.60,-0.13 L0.60,-0.085 L0.50,-0.085 L0.50,-0.040 L0.44,-0.035 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#8f99a5"), ink))
        o.append('<path d="M0.44,0.035 L0.50,0.040 L0.50,0.045 L0.60,0.045 L0.60,0.090 L0.44,0.090 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#8f99a5"), ink))
        o.append('<rect x="0.40" y="-0.050" width="0.04" height="0.10" rx="0.01" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#5a636e"), ink))
        o.append('<path d="M0.0,-0.010 L0.42,-0.010" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c("#c3cad3"))
        ends = ((-0.13, 0.0), (0.60, -0.13), (0.60, 0.09))
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tip = NEW_TIP3[kind]
    tx, ty = _rot(tip * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


def bucket_svg(uid="bk", fill=0.0, overflow=0.0, ink=P.INK, tint=None, puddle=None):
    """the tin bucket standing on the ground, as an SVG fragment in D units with the bottom centre at (0, 0) (bail lying back,
    out of the way).  fill > 0: dark molasses surface at the rim; overflow 0..1: molasses running down the sides (drip
    length) and, with puddle (D wide, default 0.55 * overflow), a pool around the foot.  Same scale as the held bucket
    (draw it at the figure's px per D)."""
    k = P._Ctx(str(uid), ink, P._rgb(tint) if P._is_hex(tint) else None)
    body = _tin_bucket_body(k, fill, overflow, "sb")
    o = ['<g transform="translate(0 -0.47)">']
    pw = (0.55 * overflow) if puddle is None else puddle
    if pw > 0.0:
        o.append('<ellipse cx="0.03" cy="0.475" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>'
                 % (0.18 + pw * 0.5, 0.035 + pw * 0.06, k.c(MOLASSES), k.ink))
        o.append('<path d="M%.4f,0.465 Q0.0,0.452 %.4f,0.462" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
                 % (-0.10 - pw * 0.3, 0.05 + pw * 0.2, k.c(MOLASSES_L)))
    o.append('<path d="M-0.162,0.180 Q-0.24,0.08 -0.21,0.02" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.ink)
    o.append(body)
    o.append('</g>')
    return '<g id="%s_bucket"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), "".join(o))


# ============================================================================= cast
NEW_CAST3 = {
    # the hero: the youngest apprentice on the dock (0.8 of the adults), oversized grey-blue work jacket, red scarf, flat cap
    "tommy": dict(
        _cast3=True, build="boy", seed=9.3,
        torso_w=0.64, torso_h=0.80, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.82, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f3a49a",
        hat="newsboy", hat_style="flatnews", hat_tilt=-5.0, ear_pencil=False, cap_puff=1.1,
        hat_colors=dict(light="#857262", base="#5e4c40", dark="#3c2f27", shine="#a99382", visor="#4a3b31"),
        hair=dict(color="#9a6232", front=0.07, grow=0.15),
        costume="workjacket", jacket_len=0.17, jacket_flare=0.07,
        sleeve=dict(color="#6e86a2", dark="#46586f", cuff="#8ea2bb", len=0.60, w=0.150, roll=True),
        boots=dict(color="#4a3224", cuff="#5d4030", h=0.12, toe=0.14, soft=True),
        colors=dict(base="#6e86a2", dark="#46586f", lapel="#5a7090", pocket="#62799a", button="#3d3340", shirt="#efe6d2",
                    susp="#7a4a2a", susp_b="#d9b24a", pants="#7a5232", scarf="#d2362c", scarf_d="#8e1f1a", scarf_s="#f0d9b5"),
    ),
    # the foreman: big and round, brown derby, thick dark walrus moustache, brown waistcoat over a white shirt, rolled sleeves
    "foreman": dict(
        _cast3=True, build="stout", seed=31.6, cigar_ok=True,
        torso_w=1.16, torso_h=1.10, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.42, 0.44), arm=0.74, hip_x=0.16, leg=1.30, stance=0.06, wide=0.26, limb_w=0.070,
        eye_y=-0.030, brow="stroke", brow_th=0.060, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=1.0,
        smirk_side=-1, cheeks="#ec8c7a",
        hat="newsboy", hat_style="derby", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#7a5640", base="#4e3426", dark="#2c1c14", shine="#b48a6a", band="#1e1410", brim="#453023", edge="#9a7458"),
        hair=dict(color="#4a3428", front=0.06, grow=0.22),
        costume="foreman",
        sleeve=dict(color="#f4f0e8", dark="#c9c0b8", cuff="#ffffff", len=0.46, w=0.175, roll=True),
        boots=dict(color="#2f241e", cuff="#2f241e", h=0.10, toe=0.15),
        colors=dict(base="#f4f0e8", shirt_d="#d9d0c8", vest="#8a5a34", vest_d="#5e3a20", button="#d8c6a0", brass="#d9b45a",
                    pants="#4a4048", moustache="#4a2a1c", moustache_l="#7a4c34"),
    ),
    # dock workers
    "worker1": dict(
        _cast3=True, build="slim", seed=22.7,
        torso_w=0.66, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.74, hip_x=0.17, leg=1.34, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.048, mouth="dash", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="flatnews", hat_tilt=-2.0, ear_pencil=False, cap_puff=0.6,
        hat_colors=dict(light="#9a9aa0", base="#717178", dark="#4a4a52", shine="#c9c9d0", visor="#5c5c64"),
        hair=dict(color="#2e2420", front=0.08, grow=0.22),
        costume="overalls",
        sleeve=dict(color="#a8483a", dark="#6e2a22", cuff="#b85a4a", len=0.52, w=0.140, roll=True),
        boots=dict(color="#3a2c26", cuff="#3a2c26", h=0.10, toe=0.14),
        colors=dict(base="#a8483a", check="#5e2620", collar="#a8483a", denim="#4d6f9e", denim_d="#3a5682", stitch="#e2b44a",
                    brass="#d9b45a", pants="#4d6f9e"),
    ),
    "worker2": dict(
        _cast3=True, build="regular", seed=27.4,
        torso_w=0.88, torso_h=1.00, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.33, 0.47), arm=0.74, hip_x=0.16, leg=1.18, stance=0.07, wide=0.28, limb_w=0.064,
        eye_y=0.000, brow="stroke", brow_th=0.054, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=-1,
        beard=dict(color="#a0582c", dark="#6a3418"),
        hat="newsboy", hat_style="flatnews", hat_tilt=-3.0, ear_pencil=False, cap_puff=0.8,
        hat_colors=dict(light="#7f8a5a", base="#5c6740", dark="#3a4228", shine="#a8b47e", visor="#4a5434"),
        hair=dict(color="#8a4a26", front=0.06, grow=0.22),
        costume="overalls",
        sleeve=dict(color="#6f8aa8", dark="#4a6280", cuff="#88a0bc", len=0.50, w=0.150, roll=True),
        boots=dict(color="#3a2c26", cuff="#3a2c26", h=0.10, toe=0.14),
        colors=dict(base="#6f8aa8", collar="#6f8aa8", denim="#9a7448", denim_d="#74542e", stitch="#f0d9a0", brass="#d9b45a",
                    pants="#9a7448", moustache="#a0582c", moustache_l="#d08a50"),
    ),
    # street kids in winter coats
    "kid1": dict(
        _cast3=True, build="child", seed=15.2,
        torso_w=0.54, torso_h=0.72, profile=CE.PROFILE_CHILD, shift_pow=1.0,
        shoulder=(0.21, 0.48), arm=CE.CHILD_ARM, hip_x=0.14, leg=0.70, stance=0.07, wide=0.22, limb_w=0.056,
        eye_y=0.060, brow="dome", brow_th=0.034, mouth="smile", moustache=False, smirk_side=1, cheeks="#f4a8a0", freckles=True,
        hat="newsboy", hat_style="earflap", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(light="#9a6a44", base="#74492a", dark="#4a2c18", shine="#c0906a", fur="#efe4cc"),
        hair=dict(color="#3a2a22", front=0.07, grow=0.18),
        costume="wintercoat", coat_len=0.18, coat_flare=0.08,
        sleeve=dict(color="#c98f36", dark="#8e5f1e", cuff="#a8742a", len=0.90, w=0.140),
        boots=dict(color="#3d2c24", cuff="#3d2c24", h=0.10, toe=0.12, soft=True),
        colors=dict(base="#c98f36", dark="#8e5f1e", collar="#7a4a2a", button="#4a3226", patch="#7d8f5a", belt="#7a4a2a", pants="#4a4250"),
    ),
    "kid2": dict(
        _cast3=True, build="child", seed=24.1,
        torso_w=0.52, torso_h=0.72, profile=CE.PROFILE_CHILD, shift_pow=1.0,
        shoulder=(0.20, 0.48), arm=CE.CHILD_ARM, hip_x=0.13, leg=0.70, stance=0.06, wide=0.22, limb_w=0.055,
        eye_y=0.060, brow="dome", brow_th=0.032, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f6b0b0", lashes=True,
        hat="newsboy", hat_style="knit", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(light="#ec8a5e", base="#d4643a", dark="#9a4020", stripe="#f3e6c8", cuff="#c0552e", pom="#f3e6c8", ribbon="#3f8a80"),
        hair=dict(color="#6a3a22", front=0.08, grow=0.20),
        costume="wintercoat", coat_len=0.34, coat_flare=0.13,
        sleeve=dict(color="#3f7f78", dark="#285650", cuff="#e8dcc0", len=0.90, w=0.135),
        boots=dict(color="#4a2e26", cuff="#4a2e26", h=0.12, toe=0.11, soft=True),
        colors=dict(base="#3f7f78", dark="#285650", collar="#e8dcc0", button="#e8dcc0", band="#e8dcc0", pants="#3f7f78"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast3.py canvas): every arm preset with
# paintbrush / tin_bucket / wrench at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects, every STORY3 pose
# of the member; >= 0.32 D head room above that range.
CANVAS3 = {
    "tommy": (-1.6875, -3.8750, 1.6875, 0.1250),
    "foreman": (-1.8750, -4.6875, 1.8750, 0.1875),
    "worker1": (-1.6875, -4.6250, 1.6875, 0.1250),
    "worker2": (-1.7500, -4.4375, 1.7500, 0.1250),
    "kid1": (-1.5000, -3.6250, 1.5000, 0.1250),
    "kid2": (-1.5000, -3.6875, 1.5000, 0.1875),
}


# ============================================================================= story poses
def _feet_y(cast, pose):
    return P.figure(cast, pose, "q")["feet_y"]


def _story():
    S, M = {}, {}
    # --- tommy
    bp = dict(yaw=0.6, pitch=0.6, expr="worried", head_roll=6, lean=16, head_dy=0.0,
              legs=dict(preset="crouch", crouch=0.62, stride=0.35, toe_r=0.8, toe_l=0.5),
              arm_l=dict(hand=(0.32, 1.05), bend=0.6), prop_r=dict(type="tin_bucket"))
    fy = _feet_y("tommy", bp)
    bp["arm_r"] = dict(hand=P.hand_for_tip("tin_bucket", (0.62, fy), 90), bend=-0.3, stretch=1.3)
    S["tommy_bucket_place"] = ("tommy", bp)
    M["tommy_bucket_place"] = dict(note="crouching, the bucket's bottom touches the floor beside his front foot (prop_tip_r = "
                                        "bottom centre on the sole line); leave a bucket_svg() there when he lets go")
    S["tommy_listen"] = ("tommy", dict(yaw=-0.45, pitch=0.15, expr="worried", fx=["sweat"], head_roll=-12, lean=-3, gaze=(-1.0, -0.3),
                                       arm_r=dict(hand=(0.60, -0.04), bend=1.0, shape="open", layer="front", stretch=1.3),
                                       arm_l=dict(hand=(-0.12, 0.92), bend=0.8), legs="narrow"))
    M["tommy_listen"] = dict(note="cupped hand behind the screen-right ear, head tilted toward the tank (put the tank screen-right; "
                                  "or mirror=True)")
    S["tommy_paint"] = ("tommy", dict(yaw=0.75, pitch=-0.2, expr="determined", head_roll=-4, lean=4,
                                      arm_r=dict(hand=(0.62, 0.10), bend=-0.7, stretch=1.3), prop_r=dict(type="paintbrush", angle=-55),
                                      arm_l=dict(hand=(-0.05, 0.98), bend=0.7), prop_l="paintpot", legs="wide"))
    M["tommy_paint"] = dict(note="the brush tip (prop_tip_r) presses on a wall about 0.95 D right of the head; animate arm_r hand y "
                                 "-0.05..0.35 and angle -65..-40 for strokes",
                            stroke=dict(arm_r=dict(hand=(0.62, 0.40), bend=-0.5, stretch=1.3), prop_r=dict(type="paintbrush", angle=-40)))
    S["tommy_worried"] = ("tommy", dict(yaw=-0.3, pitch=0.35, expr="worried", fx=["sweat"], head_roll=6,
                                        arm_r=dict(hand=(0.08, 0.84), bend=0.8), arm_l=dict(hand=(-0.04, 0.88), bend=0.8), legs="narrow"))
    S["tommy_determined"] = ("tommy", dict(yaw=0.3, expr="determined", head_roll=-4, arm_l="akimbo", arm_r=dict(hand=(0.40, 1.00), bend=0.6),
                                           legs="wide", lean=2))
    S["tommy_run"] = ("tommy", dict(yaw=0.85, pitch=-0.1, expr="shocked", fx=["sweat"], lean=14, head_roll=-6,
                                    legs=dict(preset="step", stride=1.3, lift_l=0.9, knee_l=1.0, toe_r=1.0),
                                    arm_r=dict(hand=(0.55, 0.50), bend=-0.9, stretch=1.1), arm_l=dict(hand=(-0.50, 0.92), bend=0.6, layer="back")))
    M["tommy_run"] = dict(note="one run frame; alternate with mirror of the limbs: swap arm_r/arm_l hand x signs and stride sign")
    # --- foreman
    S["foreman_laugh"] = ("foreman", dict(yaw=0.15, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], head_roll=14, lean=-6,
                                          head_dy=0.03, squash=(1.03, 0.97), t=0.3,
                                          arm_r=dict(hand=(0.30, 1.12), bend=0.9), arm_l=dict(hand=(-0.26, 1.16), bend=0.9), legs="wide"))
    S["foreman_smug"] = ("foreman", dict(yaw=0.3, pitch=-0.3, expr="smug", head_roll=5, arm_r="akimbo", arm_l="akimbo", cigar=True))
    M["foreman_smug"] = dict(note="cigar=True (pose key of this module): drawn only while the mouth is closed")
    S["foreman_point"] = ("foreman", dict(yaw=-0.35, pitch=-0.2, expr="smug", head_roll=-4,
                                          arm_l=dict(hand=(-1.00, 0.20), shape="point", bend=-0.6, stretch=1.25), arm_r="akimbo", cigar=True))
    S["foreman_order"] = ("foreman", dict(yaw=-0.35, pitch=-0.6, expr="angry", mouth="talk_b", head_roll=-7, lean=-3,
                                          arm_l=dict(hand=(-0.96, -0.20), shape="point", bend=-0.8, stretch=1.3), arm_r="akimbo", legs="wide"))
    S["foreman_order_paint"] = ("foreman", dict(yaw=0.35, pitch=-0.4, expr="angry", mouth="talk_a", head_roll=6, lean=-2, legs="wide",
                                                arm_l=dict(hand=(-0.95, -0.30), shape="point", bend=-0.8, stretch=1.3),
                                                arm_r=dict(hand=(0.95, 0.62), bend=-0.5, stretch=1.2), prop_r=dict(type="paintbrush", angle=-10)))
    M["foreman_order_paint"] = dict(note="points up-left at the tank (screen-left) and holds the brush out to the right by its handle "
                                         "(tommy's hand pins to the handle: brush local point (+0.12, 0) from hand_r)")
    kick = dict(yaw=0.55, pitch=-0.3, expr="angry", head_roll=8, lean=-10,
                arm_r=dict(hand=(0.70, 0.30), bend=-0.6, shape="open"), arm_l=dict(hand=(-0.80, 0.20), bend=-0.7, shape="open"))
    fy = _feet_y("foreman", dict(kick, legs="stand"))
    kick["legs"] = dict(preset="stand", foot_l=(-0.20, fy - 0.012), foot_r=(0.95, fy - 0.62), knee_r=0.4, knee_l=-0.2, toe_r=1.0, toe_l=0.5)
    S["foreman_kick"] = ("foreman", kick)
    M["foreman_kick"] = dict(note="the screen-right boot kicks forward 0.62 D above the floor (anchors foot_r: put the bucket there "
                                  "on the impact frame); the standing foot stays on the floor")
    S["foreman_smug_kick_after"] = ("foreman", dict(yaw=0.4, pitch=-0.35, expr="smug", head_roll=6, arm_r="akimbo",
                                                    arm_l=dict(hand=(-0.20, 0.95), bend=0.7), cigar=True, legs="wide"))
    S["foreman_shocked"] = ("foreman", dict(yaw=-0.25, pitch=-0.2, expr="shocked", fx=["sweat"], head_roll=-5, lean=-4, squash=(0.97, 1.04),
                                            arm_r="raised", arm_l="raised", legs="wide"))
    S["foreman_arms_crossed"] = ("foreman", dict(yaw=-0.2, pitch=-0.25, expr="smug", head_roll=-4, cigar=True,
                                                 arm_l=dict(hand=(0.32, 0.88), bend=0.5, sharp=0.3), arm_r=dict(hand=(-0.34, 0.82), bend=-0.5, sharp=0.3)))
    # --- workers
    S["workers_laugh"] = ("worker1", dict(yaw=-0.35, pitch=-0.3, expr="laughing", fx=["tears"], head_roll=-10, lean=-5, t=0.6,
                                          arm_l=dict(hand=(-0.84, -0.20), shape="point", bend=-0.8, stretch=1.3), arm_r=dict(hand=(0.22, 1.02), bend=0.9)))
    S["workers_laugh_beard"] = ("worker2", dict(yaw=0.35, expr="laughing", blink=2, mouth="talk_b", head_roll=12, lean=-5, t=0.2,
                                                arm_r=dict(hand=(0.26, 1.06), bend=0.9), arm_l=dict(hand=(-0.24, 1.08), bend=0.9), legs="wide"))
    S["workers_paint"] = ("worker1", dict(yaw=-0.7, pitch=-0.3, expr="unimpressed", head_roll=4,
                                          arm_l=dict(hand=(-0.66, -0.05), bend=-0.6, stretch=1.2), prop_l=dict(type="paintbrush", angle=-125),
                                          arm_r=dict(hand=(0.10, 0.95), bend=0.7), legs="wide"))
    S["workers_paint_beard"] = ("worker2", dict(yaw=0.7, pitch=0.1, expr="neutral", head_roll=-3,
                                                arm_r=dict(hand=(0.70, 0.45), bend=-0.5, stretch=1.2), prop_r=dict(type="paintbrush", angle=-20),
                                                arm_l=dict(hand=(-0.10, 1.00), bend=0.7), prop_l="paintpot"))
    S["worker_wrench"] = ("worker2", dict(yaw=-0.4, expr="unimpressed", head_roll=-4, arm_l="down", arm_r=dict(hand=(0.40, 0.80), bend=0.5),
                                          prop_r=dict(type="wrench", angle=-70)))
    # --- kids
    S["kids_play"] = ("kid1", dict(yaw=0.4, expr="excited", head_roll=-8, lean=-4, squash=(0.97, 1.03),
                                   arm_r=dict(hand=(0.40, -0.42), bend=-0.8, shape="open", stretch=1.2), arm_l=dict(hand=(-0.45, 0.30), bend=-0.5, shape="open"),
                                   legs=dict(preset="stand", lift_r=0.6, knee_r=1.0, toe_r=0.6)))
    M["kids_play"] = dict(note="throwing a snowball (hand_r up); legs: one knee raised")
    S["kids_play_girl"] = ("kid2", dict(yaw=-0.35, expr="happy", head_roll=8, fx=["blush"],
                                        arm_r=dict(hand=(0.42, 0.10), bend=-0.6, shape="open"), arm_l=dict(hand=(-0.40, 0.08), bend=-0.6, shape="open"),
                                        legs="wide"))
    S["kids_run"] = ("kid1", dict(yaw=0.85, expr="shocked", fx=["sweat"], lean=14, head_roll=-6,
                                  legs=dict(preset="step", stride=1.3, lift_l=0.9, knee_l=1.0, toe_r=1.0),
                                  arm_r=dict(hand=(0.48, 0.42), bend=-0.9, stretch=1.1), arm_l=dict(hand=(-0.42, 0.85), bend=0.6, layer="back")))
    S["kids_run_girl"] = ("kid2", dict(yaw=0.85, expr="shocked", lean=12, head_roll=-6,
                                       legs=dict(preset="step", stride=1.2, lift_l=0.8, knee_l=1.0, toe_r=1.0),
                                       arm_r=dict(hand=(0.45, 0.40), bend=-0.9, stretch=1.1), arm_l=dict(hand=(-0.40, 0.82), bend=0.6, layer="back")))
    return S, M


STORY3, STORY3_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast3_registered", False):
        CE.register_stage()
        if not STORY3:
            s, m = _story()
            STORY3.update(s)
            STORY3_META.update(m)
        return
    for name in ("_ink_limb", "_prop", "_face", "_moustache", "_norm"):
        _O3[name] = getattr(P, name)
    P._ink_limb = _ink_limb
    P._prop = _prop
    P._face = _face
    P._moustache = _moustache
    P._norm = _norm
    CE.COSTUMES.update(COSTUMES3)
    CE.HATS.update(HATS3)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS3 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP3)
    for n, c in NEW_CAST3.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS3)
    s, m = _story()
    STORY3.update(s)
    STORY3_META.update(m)
    P.STORY.update(STORY3)
    P._cast3_registered = True
    CE.register_stage()


register()
