#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast6.py -- the cast of film 6 ("the 13th loaf", a medieval English market town, 1260s) for the v2 puppet, as an extension module.

    import sys; sys.path.insert(0, ".../v3/cast6"); import cast6      # registers on import (idempotent); imports cast5/4/3/2/cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast6.STORY6["kit_hold_loaf"]
    f = puppet.figure(cast, pose, "k")                                # kit holding up the 13th loaf
    w = puppet.figure("henry", cast6.cycle("henry", 0.25, "walk"), "h")   # one frame of henry's walk cycle

Nothing in v2/puppet or v3/cast..cast5 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  apron6 (tunic + apron, flour), cloak6 (hooded cloak), tabard6 (royal tabard / guard tabard over mail)
    cast_ext.HATS      linencap, baldtuft, hood, hooddown, kettlehat, nasalhelm, wimple, strawhat
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast5's wrappers (each falls through for everything it does not handle):
    _norm         reads this module's pose keys (basket, hood, pale, fingers_r / fingers_l, t)
    _face         flour dust (CAST key "flour"), the pale wash (pose key "pale")
    _face_layout  small eyes (CAST key "eye_scale")
    _hand         counting fingers (pose keys fingers_r / fingers_l)
    _prop         loaf, basket, cabbage, tomato, spear
    figure        the pillory board (pose key "pillory"), drawn over the body with head and hands poking through
New cast:  kit, henry, inspector (hood up), inspector_royal (hood down, tabard, chain), guard1, guard2, woman1, man1, baker2.
STORY6 / STORY6_META: story poses.  cycle(): walk / run cycle frames.  talk_mouth(), blink_at(): lip-sync and blink helpers.
Standalone pieces: loaf_svg, basket_svg, cabbage_svg, tomato_svg, loaf_pile_svg, pillory_svg.

Command line (QA):  python3 test_cast6.py        lineup.jpg (every member, every pose, cycles, mouths, props), canvas + robustness
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
for _d in (os.path.join(PROJ, "v3", "cast5"), os.path.join(PROJ, "v3", "cast4"), os.path.join(PROJ, "v3", "cast3"),
           os.path.join(PROJ, "v3", "cast2"), os.path.join(PROJ, "v3", "cast")):
    if _d not in sys.path:
        sys.path.insert(0, _d)
import cast5 as C5      # noqa: E402  (v3/cast5, read-only; imports cast4, cast3, cast2, cast_ext and v2/puppet)
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW6 = ("kit", "henry", "inspector", "inspector_royal", "guard1", "guard2", "woman1", "man1", "baker2")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_O6 = {}                      # the helpers this module wrapped
# pose keys of the figure being drawn (set by the _norm wrapper; figure() calls _norm before drawing anything)
_POSE6 = {"basket": None, "hood": 1.0, "pale": 0.0, "fingers": {"l": 0, "r": 0}, "hand_i": 0, "t": 0.0, "L": None}


def _cur():
    return CE._CUR[0]


def _f(v, d, lo, hi):
    """finite float clamped to [lo, hi] (garbage -> d)."""
    return _clamp(_num(v, d), lo, hi)


def _frac(x):
    return x - math.floor(x)


def _hsh(i, s=0.0):
    """deterministic pseudo random 0..1 (no hash(), no random)."""
    v = math.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - math.floor(v)


# ============================================================================= colours
BREAD = dict(light="#f6cd7e", base="#de9a48", dark="#a45c26", crust="#8a4a1e", score="#f8e0a8", flour="#fbf6ea")
WICKER = dict(light="#e2b46e", base="#c08a44", dark="#7e5424", weave="#9a6a32")
GOLD = dict(light="#ffe58a", base="#e8b52e", dark="#a8771a")
ROYAL_RED = "#b5262e"
STEEL = dict(light="#dfe4ea", base="#9ea8b4", dark="#5d6672", shine="#ffffff")


# ============================================================================= bread, basket, veg (D units)
def _loaf(k, x, y, r, rot=0.0, seed=0.0, flour=True):
    """one round crusty cob loaf centred on (x, y), r = half width: domed top, flatter base, cross-scored, flour dust."""
    u = "%s_lf" % k.uid
    if u not in "".join(k.defs[:1]) and not any(('id="%s"' % u) in d for d in k.defs):
        k.defs.append('<radialGradient id="%s" cx="0.36" cy="0.30" r="0.80"><stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/>'
                      '<stop offset="1" stop-color="%s"/></radialGradient>' % (u, k.c(BREAD["light"]), k.c(BREAD["base"]), k.c(BREAD["dark"])))
    sw = max(0.006, 0.075 * r)
    ry = 0.80 * r
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (x, y, rot)]
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f 0,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f 0,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (-r, 0.25 * ry, -r * 1.02, -0.55 * ry, -0.55 * r, -ry, -ry, 0.55 * r, -ry, r * 1.02, -0.55 * ry, r, 0.25 * ry,
            r * 0.85, 0.62 * ry, 0.70 * ry, -r * 0.85, 0.62 * ry, -r, 0.25 * ry))
    o.append('<path d="%s" fill="url(#%s)" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (d, u, k.ink, sw))
    # darker crust band at the base
    o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.55"/>'
             % (-r * 0.80, 0.36 * ry, 0.62 * ry, r * 0.80, 0.36 * ry, k.c(BREAD["crust"]), 0.9 * sw))
    # scores: a cross (seed even) or three slashes
    if int(seed) % 2 == 0:
        sc = "M%.4f,%.4f Q0,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,0 %.4f,%.4f" % (-0.50 * r, -0.30 * ry, -0.48 * ry, 0.50 * r, -0.30 * ry,
                                                                            -0.05 * r, -0.80 * ry, 0.06 * r, 0.02 * r, 0.25 * ry)
    else:
        sc = "".join("M%.4f,%.4f L%.4f,%.4f " % (dx * r - 0.18 * r, -0.62 * ry, dx * r + 0.12 * r, 0.05 * ry) for dx in (-0.35, 0.0, 0.35))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (sc, k.c(BREAD["crust"]), 1.6 * sw))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (sc, k.c(BREAD["score"]), 0.75 * sw))
    # shine + flour
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" opacity="0.55"/>'
             % (-0.72 * r, -0.10 * ry, -0.66 * r, -0.62 * ry, -0.28 * r, -0.82 * ry, 0.9 * sw))
    if flour:
        for i in range(5):
            fx = (-0.55 + 1.1 * _hsh(i, seed)) * r
            fy = (-0.75 + 0.6 * _hsh(i + 7, seed)) * ry
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.8"/>' % (fx, fy, 0.07 * r, k.c(BREAD["flour"])))
    o.append('</g>')
    return "".join(o)


LOAF_R = 0.17                       # a held loaf: 0.34 D wide
BASKET_HANDLE = 0.40                # basket: hand on the handle top (0, 0), rim at y = 0.40
BASKET_ROWS = (5, 4, 3, 1)          # loaves per visible row, bottom row first (12 = the first three rows, 13 = + one on top)
BASKET_LR = 0.072


def _basket_body(k, n=12, tilt=0.0, pour=0.0, sc=1.0):
    """wicker basket hanging from its arched handle (handle top = (0, 0)), rim at y = 0.40, base at 0.66, rim 0.84 wide.
    n loaves (0..13) piled above the rim (rows 5, 4, 3, 1).  tilt rotates the basket about the handle top (degrees, positive =
    clockwise = the screen-right lip goes down); pour 0..1 = loaves tumbling out of the lower lip.  Returns (svg, anchors)."""
    rim = BASKET_HANDLE
    hw, bw, base = 0.42, 0.31, 0.66
    gid = "%s_wk" % k.uid
    if not any(('id="%s"' % gid) in d for d in k.defs):
        k.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/>'
                      '<stop offset="1" stop-color="%s"/></linearGradient>' % (gid, k.c(WICKER["light"]), k.c(WICKER["base"]), k.c(WICKER["dark"])))
    n = int(_clamp(round(_num(n, 12)), 0, 13))
    o = ['<g transform="rotate(%.3f)">' % tilt]
    # handle (behind the loaves): an arch from the rim corners to the hand
    hd = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f 0,0 C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (-hw + 0.06, rim, -hw + 0.02, 0.10, -0.22, -0.005, 0.22, -0.005, hw - 0.02, 0.10, hw - 0.06, rim)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (hd, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (hd, k.c(WICKER["base"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.030 0.022" opacity="0.8"/>' % (hd, k.c(WICKER["dark"])))
    # loaves, back rows first (the top row is the back of the pile)
    r = BASKET_LR
    rows = []
    left = n
    for cnt in BASKET_ROWS:
        rows.append(min(cnt, max(0, left)))
        left -= cnt
    rows_y = (rim - 0.035, rim - 0.115, rim - 0.195, rim - 0.270)
    loaf_pts = []
    for ri in range(len(rows) - 1, -1, -1):
        cnt = rows[ri]
        full = BASKET_ROWS[ri]
        for j in range(cnt):
            x = (j - (full - 1) / 2.0) * 2.02 * r + (0.02 if ri % 2 else -0.01)
            y = rows_y[ri] + 0.006 * math.sin(j * 2.1 + ri)
            loaf_pts.append((x, y, ri * 10 + j))
    for (x, y, s) in loaf_pts:
        o.append(_loaf(k, x, y, r, rot=(_hsh(s, 3.0) - 0.5) * 24, seed=s, flour=False))
    # body: trapezoid with a rolled rim, weave
    body = [(-hw, rim), (hw, rim), (bw, base), (-bw, base)]
    bd = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q0,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        -hw, rim, hw, rim, hw - 0.02, base - 0.10, bw, base, base + 0.025, -bw, base, -hw + 0.02, base - 0.10, -hw, rim)
    o.append('<path d="%s" fill="url(#%s)" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (bd, gid, k.ink))
    wv = []
    for i in range(3):
        y = rim + 0.065 + i * 0.065
        f = (y - rim) / (base - rim)
        xx = hw + (bw - hw) * f
        wv.append("M%.4f,%.4f Q0,%.4f %.4f,%.4f" % (-xx + 0.01, y, y + 0.02, xx - 0.01, y))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" opacity="0.85"/>' % (" ".join(wv), k.c(WICKER["weave"])))
    vv = []
    for i in range(9):
        t = (i + 0.5) / 9.0
        x0 = -hw + 2 * hw * t
        x1 = -bw + 2 * bw * t
        vv.append("M%.4f,%.4f L%.4f,%.4f" % (x0, rim + 0.03, x1, base - 0.01))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % (" ".join(vv), k.c(WICKER["dark"])))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.050" rx="0.025" fill="%s" stroke="%s" stroke-width="0.020"/>'
             % (-hw - 0.025, rim - 0.022, 2 * hw + 0.05, k.c(WICKER["light"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-dasharray="0.026 0.018" opacity="0.8"/>'
             % (-hw, rim + 0.003, hw, rim + 0.003, k.c(WICKER["dark"])))
    o.append('</g>')
    an = {}
    lip_side = 1.0 if tilt >= 0 else -1.0
    lip = _rot(lip_side * (hw + 0.02), rim, tilt)
    an["basket_lip"] = lip
    an["basket_centre"] = _rot(0.0, rim - 0.10, tilt)
    an["basket_base"] = _rot(0.0, base, tilt)
    an["basket_base_far"] = _rot(-lip_side * bw, base, tilt)     # where a second hand lifts the basket when pouring
    # loaves falling out of the low lip (in the figure frame, not rotated)
    pour = _f(pour, 0.0, 0.0, 1.0)
    if pour > 0.0:
        m = 6
        for i in range(m):
            f = _frac(pour * 1.0 + i / float(m))
            fx = lip[0] + lip_side * (0.04 + 0.10 * f + 0.02 * _hsh(i, 9.0))
            fy = lip[1] + 0.05 + 0.55 * f * f
            if f < 0.04:
                continue
            o.append(_loaf(k, fx, fy, r * 1.05, rot=lip_side * 140 * f + 30 * i, seed=40 + i, flour=False))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.5"/>'
                     % (fx - 0.05, fy - 0.10, fx - 0.05, fy - 0.18, k.c("#fbf6ea")))
            k.ext.append((fx, fy, r * 1.2))
    for p in ((-hw - 0.03, rim), (hw + 0.03, rim), (-bw, base + 0.03), (bw, base + 0.03), (0.0, rows_y[min(3, len([c for c in rows if c]))] - r)):
        q = _rot(p[0], p[1], tilt)
        k.ext.append((q[0], q[1], 0.03))
    k.ext.append((0.0, 0.0, 0.04))
    return "".join(o), an


def _cabbage(k, x, y, r, rot=0.0, rotten=1.0):
    """a rotten cabbage: olive-brown head with loose limp outer leaves, brown spots, stink lines."""
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (x, y, rot)]
    sw = 0.08 * r
    base, light, dark = ("#9aa04a", "#c9c879", "#5e5e26") if rotten > 0.5 else ("#8cc05a", "#c8e698", "#4f8a32")
    # outer leaves all round (limp and drooping when rotten), wavy edged
    leaf = "#7c7a34" if rotten > 0.5 else "#6fa040"
    for i in range(7):
        a = -90 + i * (360.0 / 7) + 12
        dr = 0.50 + (0.12 if (rotten > 0.5 and 20 < a < 160) else 0.0)
        lx, ly = math.cos(math.radians(a)) * r * dr, math.sin(math.radians(a)) * r * dr * 0.9
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%d %.4f %.4f)" fill="%s" stroke="%s" stroke-width="%.4f"/>'
                 % (lx, ly, r * 0.52, r * 0.42, a, lx, ly, k.c(leaf), k.ink, sw))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" opacity="0.6"/>'
                 % (lx * 0.6, ly * 0.6, lx * 1.7, ly * 1.7, k.c(light), 0.6 * sw))
    o.append('<circle cx="0" cy="0" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (r * 0.80, k.c(base), k.ink, sw))
    # leaf veins / layered edges
    for a in (-60, 20, 110, 190):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.9"/>'
                 % (math.cos(math.radians(a)) * r * 0.75, math.sin(math.radians(a)) * r * 0.75, math.cos(math.radians(a + 40)) * r * 0.25,
                    math.sin(math.radians(a + 40)) * r * 0.25, math.cos(math.radians(a + 90)) * r * 0.72, math.sin(math.radians(a + 90)) * r * 0.72,
                    k.c(dark), 0.7 * sw))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.8"/>'
             % (-0.5 * r, -0.2 * r, -0.4 * r, -0.6 * r, 0.0, -0.66 * r, k.c(light), 0.9 * sw))
    if rotten > 0.0:
        for (sx, sy, sr) in ((0.25, 0.20, 0.20), (-0.30, 0.30, 0.13), (0.35, -0.30, 0.10), (-0.05, 0.45, 0.10)):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="%.2f"/>'
                     % (sx * r, sy * r, sr * r, sr * r * 0.75, k.c("#6a4a24"), 0.85 * rotten))
        # stink lines
        for i, dx in enumerate((-0.35, 0.05, 0.42)):
            o.append('<path d="M%.4f,%.4f q%.4f,%.4f 0,%.4f q%.4f,%.4f 0,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="%.2f"/>'
                     % (dx * r, -0.95 * r, 0.12 * r, -0.12 * r, -0.24 * r, -0.12 * r, -0.12 * r, -0.24 * r, k.c("#a8b85a"), 0.7 * sw, 0.8 * rotten))
    o.append('</g>')
    k.ext.append((x, y, r * 1.1))
    k.ext.append((x, y - 1.5 * r, r * 0.3))
    return "".join(o)


def _tomato(k, x, y, r, rot=0.0, rotten=1.0, squash=0.0):
    """an over-ripe tomato: dark red, a brown bruise, wilted green calyx; squash 0..1 flattens it (a splat on impact)."""
    sy = 1.0 - 0.55 * squash
    sx = 1.0 + 0.45 * squash
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f %.4f)">' % (x, y, rot, sx, sy)]
    sw = 0.10 * r
    body = ("M0,{a} C{b},{c} {d},{e} {d},0 C{d},{f} {b},{g} 0,{h} C{nb},{g} {nd},{f} {nd},0 C{nd},{e} {nb},{c} 0,{a} Z"
            .format(a="%.4f" % (-0.82 * r), b="%.4f" % (0.55 * r), c="%.4f" % (-0.95 * r), d="%.4f" % r, e="%.4f" % (-0.55 * r),
                    f="%.4f" % (0.55 * r), g="%.4f" % (0.95 * r), h="%.4f" % (0.88 * r), nb="%.4f" % (-0.55 * r), nd="%.4f" % (-r)))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (body, k.c("#c8342a" if rotten < 0.5 else "#b02a26"), k.ink, sw))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" opacity="0.6"/>'
             % (-0.62 * r, -0.10 * r, -0.55 * r, -0.55 * r, -0.20 * r, -0.66 * r, 0.9 * sw))
    if rotten > 0.0:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="%.2f"/>' % (0.30 * r, 0.25 * r, 0.38 * r, 0.30 * r, k.c("#6e2a1a"), 0.9 * rotten))
        o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.8"/>'
                 % (0.15 * r, 0.20 * r, 0.10 * r, 0.12 * r, 0.30 * r, 0.05 * r, k.c("#4a1a10"), 0.8 * sw))
    # calyx
    cal = "".join("M0,%.4f L%.4f,%.4f " % (-0.80 * r, math.cos(math.radians(a)) * 0.42 * r, -0.80 * r + math.sin(math.radians(a)) * 0.22 * r + 0.06 * r)
                  for a in (-170, -120, -60, -10, 40, 140))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (cal, k.ink, 1.9 * sw))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (cal, k.c("#6e7a2a"), 0.9 * sw))
    o.append('</g>')
    k.ext.append((x, y, r * 1.5))
    return "".join(o)


# ============================================================================= props held in the hand
NEW_PROPS6 = ("loaf", "basket", "cabbage", "tomato", "spear")
SPEAR_BACK, SPEAR_FRONT = 0.95, 1.45          # spear gripped 0.95 D from its butt; the point is 1.45 D ahead of the hand
# working point distance from the gripping hand (D): loaf = its centre (held up on the palm), basket = its rim centre (hangs
# upright from the handle), cabbage / tomato = centre, spear = the point
NEW_TIP6 = {"loaf": LOAF_R * 0.85, "basket": BASKET_HANDLE - 0.10, "cabbage": 0.17, "tomato": 0.08, "spear": SPEAR_FRONT}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS6:
        return _O6["_prop"](k, kind, H, ang, sc)
    if kind == "spear":
        o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
        b, f = -SPEAR_BACK, SPEAR_FRONT
        o.append('<path d="M%.4f,-0.024 L%.4f,-0.020 L%.4f,0.020 L%.4f,0.024 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                 % (b, f - 0.24, f - 0.24, b, k.c("#a97a48"), k.ink))
        o.append('<path d="M%.4f,-0.008 L%.4f,-0.007" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (b + 0.03, f - 0.27, k.c("#d8aa74")))
        o.append('<rect x="%.4f" y="-0.030" width="0.050" height="0.060" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (b - 0.01, k.c(STEEL["dark"]), k.ink))
        blade = "M%.4f,-0.030 L%.4f,-0.030 Q%.4f,-0.085 %.4f,-0.050 L%.4f,0 L%.4f,0.050 Q%.4f,0.085 %.4f,0.030 L%.4f,0.030 Z" % (
            f - 0.30, f - 0.24, f - 0.20, f - 0.12, f, f - 0.12, f - 0.20, f - 0.24, f - 0.30)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (blade, k.c(STEEL["base"]), k.ink))
        o.append('<path d="M%.4f,-0.004 L%.4f,-0.002" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>' % (f - 0.22, f - 0.03, k.c(STEEL["light"])))
        o.append('<path d="M%.4f,-0.040 L%.4f,0.040" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (f - 0.30, f - 0.30, k.ink))
        o.append('</g>')
        for e in ((b - 0.02, 0.0), (f, 0.0), (f - 0.15, 0.06), (f - 0.15, -0.06)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        tx, ty = _rot(f * sc, 0.0, ang)
        return "".join(o), (H[0] + tx, H[1] + ty)
    # upright props (gravity / palm up)
    o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
    n0 = len(k.ext)
    if kind == "loaf":
        o.append(_loaf(k, 0.0, -LOAF_R * 0.85, LOAF_R, rot=-6.0, seed=2))
        k.ext.append((0.0, -LOAF_R * 0.85, LOAF_R + 0.02))
        tip = (0.0, -LOAF_R * 0.85)
    elif kind == "basket":
        B = _POSE6["basket"] or {}
        svg, an = _basket_body(k, B.get("loaves", 12), _f(B.get("tilt"), 0.0, -120.0, 120.0), B.get("pour", 0.0))
        o.append(svg)
        tip = an["basket_centre"]
        _POSE6["basket_an"] = dict((n_, (H[0] + v[0] * sc, H[1] + v[1] * sc)) for n_, v in an.items())
    elif kind == "cabbage":
        o.append(_cabbage(k, 0.0, -0.17, 0.19, rot=-10.0))
        tip = (0.0, -0.17)
    else:
        o.append(_tomato(k, 0.0, -0.07, 0.075, rot=8.0))
        tip = (0.0, -0.07)
    o.append('</g>')
    k.ext[n0:] = [(H[0] + e[0] * sc, H[1] + e[1] * sc, e[2] * sc) for e in k.ext[n0:]]
    return "".join(o), (H[0] + tip[0] * sc, H[1] + tip[1] * sc)


# ============================================================================= standalone pieces
def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def loaf_svg(uid="lf", r=LOAF_R, seed=2, ink=P.INK, tint=None):
    """one loaf, centre (0, 0), half width r (D).  Its base sits at y = 0.53 r."""
    k = _ctx(uid, ink, tint)
    s = _loaf(k, 0.0, 0.0, r, seed=seed)
    return '<g id="%s_loaf"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def loaf_pile_svg(uid="lp", n=12, r=0.10, ink=P.INK, tint=None):
    """a pile of n loaves (for a scale pan or a table), resting on y = 0, centred on x = 0; rows 5-4-3-1 (13 = one on top)."""
    k = _ctx(uid, ink, tint)
    n = int(_clamp(round(_num(n, 12)), 0, 30))
    o = []
    rows = []
    left = n
    w = 5
    while left > 0:
        c = min(w, left)
        rows.append(c)
        left -= c
        w = max(1, w - 1)
    for ri in range(len(rows) - 1, -1, -1):
        cnt = rows[ri]
        for j in range(cnt):
            x = (j - (cnt - 1) / 2.0) * 2.0 * r
            y = -0.53 * r - ri * 1.05 * r
            o.append(_loaf(k, x, y, r, rot=(_hsh(ri * 7 + j, 2.0) - 0.5) * 20, seed=ri * 7 + j))
    return '<g id="%s_pile"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), "".join(o))


def basket_svg(uid="bs", loaves=12, tilt=0.0, pour=0.0, ink=P.INK, tint=None):
    """the wicker basket alone (handle top at (0, 0), rim y 0.40, base y 0.66).  Returns (svg, anchors)."""
    k = _ctx(uid, ink, tint)
    s, an = _basket_body(k, loaves, tilt, pour)
    return '<g id="%s_basket"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), an


def cabbage_svg(uid="cb", r=0.15, rotten=1.0, rot=0.0, ink=P.INK, tint=None):
    """a (rotten) cabbage centred on (0, 0) -- also for flying / thrown veg."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_cab">%s</g>' % (k.uid, _cabbage(k, 0.0, 0.0, r, rot, rotten))


def tomato_svg(uid="tm", r=0.075, rotten=1.0, rot=0.0, squash=0.0, ink=P.INK, tint=None):
    """a (rotten) tomato centred on (0, 0); squash 0..1 = the splat on impact."""
    k = _ctx(uid, ink, tint)
    s = _tomato(k, 0.0, 0.0, r, rot, rotten, squash)
    if squash > 0.3:
        sp = "".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (math.cos(a) * r * (1.6 + 0.4 * _hsh(i)), math.sin(a) * r * 0.6 + r * 0.2,
                                                                           r * (0.14 + 0.1 * _hsh(i, 1.0)), k.c("#b02a26"))
                     for i, a in enumerate((0.3, 1.2, 2.4, 2.9, 3.6, 5.6)))
        s = sp + s
    return '<g id="%s_tom">%s</g>' % (k.uid, s)


PILLORY_W = 1.70          # board width (D)
PILLORY_H = 0.30          # board height (two planks)
PILLORY_HOLE_X = 0.56     # wrist holes at +-0.56 from the neck hole
PILLORY_WRIST_Y = 0.40 + 0.48 * 0.30   # hand y (head-centre frame) of the default board (top = head + 0.40): the split line


def _pillory_board(k, cx, top, post_to=None, empty=False, mirror=False):
    """the pillory board: two oak planks (top / bottom) with a neck hole and two wrist holes on the split line, iron hinges, a
    padlock; optional post from the board down to y = post_to.  cx, top: board centre x and top edge."""
    w, h = PILLORY_W, PILLORY_H
    x0 = cx - w / 2
    split = top + h * 0.48
    wood, wood_l, wood_d = k.c("#9a6a3c"), k.c("#c08c56"), k.c("#5e3c20")
    o = []
    if post_to is not None:
        pw = 0.15
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
                 % (cx - pw / 2, top + h - 0.02, cx + pw / 2, top + h - 0.02, cx + pw / 2 + 0.01, post_to, cx - pw / 2 - 0.01, post_to, wood, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.022" opacity="0.6"/>' % (cx + pw * 0.22, top + h + 0.04, cx + pw * 0.25, post_to - 0.03, wood_d))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" opacity="0.6"/>' % (cx - pw * 0.25, top + h + 0.04, cx - pw * 0.25, post_to - 0.10, wood_l))
        k.ext.append((cx, post_to, 0.1))
    gid = "%s_pw" % k.uid
    k.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/>'
                  '<stop offset="1" stop-color="%s"/></linearGradient>' % (gid, wood_l, wood, wood_d))
    holes = ((cx, 0.150), (cx - PILLORY_HOLE_X, 0.075), (cx + PILLORY_HOLE_X, 0.075))
    mask_id = "%s_pm" % k.uid
    if empty:
        k.defs.append('<mask id="%s"><rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="white"/>%s</mask>'
                      % (mask_id, x0 - 0.1, top - 0.1, w + 0.2, h + 0.2,
                         "".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="black"/>' % (hx, split, hr) for hx, hr in holes)))
    for (yy, hh) in ((top, split - top), (split, top + h - split)):
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.020" fill="url(#%s)" stroke="%s" stroke-width="0.024"%s/>'
                 % (x0, yy, w, hh, gid, k.ink, (' mask="url(#%s)"' % mask_id) if empty else ""))
        # grain
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.55"%s/>'
                 % (x0 + 0.08, yy + hh * 0.35, cx - 0.3, yy + hh * 0.25, cx - 0.20, yy + hh * 0.40, cx + 0.25, yy + hh * 0.60, cx + 0.45, yy + hh * 0.50,
                    x0 + w - 0.08, yy + hh * 0.62, wood_d, (' mask="url(#%s)"' % mask_id) if empty else ""))
    # hole rims (dark inner edge so the holes read)
    for hx, hr in holes:
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 0 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020"/>' % (hx - hr - 0.01, split, hr + 0.01, hr + 0.01, hx + hr + 0.01, split, k.ink))
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020"/>' % (hx - hr - 0.01, split, hr + 0.01, hr + 0.01, hx + hr + 0.01, split, k.ink))
        if empty:
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.85"/>' % (hx, split, hr, k.c("#2a1e1a")))
    # iron hinge straps at the ends + padlock
    for s in (-1, 1):
        hx = cx + s * (w / 2 - 0.10)
        o.append('<rect x="%.4f" y="%.4f" width="0.060" height="%.4f" rx="0.010" fill="%s" stroke="%s" stroke-width="0.012"/>'
                 % (hx - 0.03, top + 0.02, h - 0.04, k.c("#4a4650"), k.ink))
        for yy in (top + 0.06, top + h - 0.06):
            o.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="%s"/>' % (hx, yy, k.c("#9a96a2")))
    lx = cx + (-0.26 if mirror else 0.26)
    o.append('<path d="M%.4f,%.4f a0.035,0.035 0 0 1 0.070,0" fill="none" stroke="%s" stroke-width="0.018"/>' % (lx - 0.035, split + 0.01, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="0.090" height="0.075" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (lx - 0.045, split + 0.01, k.c("#6a6470"), k.ink))
    for p in ((x0 - 0.02, top), (x0 + w + 0.02, top), (x0 - 0.02, top + h), (x0 + w + 0.02, top + h)):
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o), split, holes


def pillory_svg(uid="pl", post_h=2.0, ink=P.INK, tint=None):
    """the empty pillory for the set: board top edge at y = 0 (centred on x = 0), post down to y = post_h + PILLORY_H.
    Returns (svg, anchors): neck / wrist hole centres, board_top, post_foot."""
    k = _ctx(uid, ink, tint)
    s, split, holes = _pillory_board(k, 0.0, 0.0, post_to=PILLORY_H + post_h, empty=True)
    an = dict(neck=(holes[0][0], split), wrist_l=(holes[1][0], split), wrist_r=(holes[2][0], split), board_top=(0.0, 0.0),
              post_foot=(0.0, PILLORY_H + post_h))
    return '<g id="%s_pillory"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), an


# ============================================================================= face: flour, pale, eyes, fingers
def _flour(k, C, P_, L):
    """flour: white dust over the hair crescents (reads on the hair only, the head is white) and a dusty smear on one cheek
    and the nose bridge, with a few speckles."""
    F = C["flour"]
    op = _clamp(_num(F.get("op"), 0.85), 0.0, 1.0)
    u = k.uid
    k.defs.append('<radialGradient id="%s_fl"><stop offset="0" stop-color="#ffffff" stop-opacity="1"/><stop offset="0.6" stop-color="#ffffff" stop-opacity="0.75"/>'
                  '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>' % u)
    o = ['<g clip-path="url(#%s_hc)" opacity="%.3f">' % (u, op)]
    for s in (-1, 1):
        for (y, rx) in ((-0.18, 0.11), (-0.02, 0.09), (0.10, 0.07)):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="url(#%s_fl)"/>' % (s * 0.43, y, rx, rx * 1.3, u))
    cheek = L["xR"] + 0.06 if F.get("side", 1) > 0 else L["xL"] - 0.06
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.085" ry="0.050" fill="%s" opacity="0.9" transform="rotate(-15 %.4f %.4f)"/>'
             % (cheek, L["ey"] + 0.11, k.c("#efe4d2"), cheek, L["ey"] + 0.11))
    for i in range(9):
        x = cheek + (-0.08 + 0.16 * _hsh(i, 2.0))
        y = L["ey"] + 0.07 + 0.09 * _hsh(i, 5.0)
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, y, 0.006 + 0.006 * _hsh(i, 8.0), k.c("#cdbfa8")))
    fx = (L["xL"] + L["xR"]) / 2
    for i in range(6):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.006" fill="%s"/>' % (fx - 0.12 + 0.24 * _hsh(i, 11.0), L["ey"] - 0.22 + 0.05 * _hsh(i, 13.0), k.c("#cdbfa8")))
    o.append('</g>')
    return "".join(o)


def _pale(k, C, P_, L, lev):
    """blood drains from the face: a cold lavender-blue wash from the crown down (clipped to the head) and four vertical
    gloom lines on the forehead."""
    u = k.uid
    k.defs.append('<linearGradient id="%s_pl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0.95"/>'
                  '<stop offset="0.55" stop-color="%s" stop-opacity="0.55"/><stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>'
                  % (u, k.c("#8d9ccc"), k.c("#b4c2e4"), k.c("#d8e0f4")))
    o = ['<g clip-path="url(#%s_hc)" opacity="%.3f">' % (u, _clamp(lev, 0.0, 1.0))]
    o.append('<rect x="-0.6" y="-0.6" width="1.2" height="%.4f" fill="url(#%s_pl)"/>' % (0.6 + L["my"] + 0.02, u))
    cx = (L["xL"] + L["xR"]) / 2
    for i, dx in enumerate((-0.15, -0.05, 0.05, 0.15)):
        y0 = -0.42 + 0.02 * (i % 2)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.75"/>'
                 % (cx + dx, y0, cx + dx, y0 + 0.13 + 0.03 * (i % 2), k.c("#4c4a86")))
    o.append('</g>')
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O6["_face"](k, C, P_, white)
    _POSE6["L"] = L
    _POSE6["blink"] = P_["blink"]
    _POSE6["expr"] = P_["expr"]
    if C is None or not C.get("_cast6"):
        return svg, L
    under, over = [], []
    if C.get("flour"):
        under.append(_flour(k, C, P_, L))
    if _POSE6["pale"] > 0.0:
        under.append(_pale(k, C, P_, L, _POSE6["pale"]))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _face_layout(C, yaw, pitch):
    r = _O6["_face_layout"](C, yaw, pitch)
    es = C.get("eye_scale") if isinstance(C, dict) else None
    if not es:
        return r
    xL, xR, ey, sL, sR, mx, my = r
    return xL, xR, ey, sL * es, sR * es, mx, my


def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    i = _POSE6["hand_i"]
    _POSE6["hand_i"] = i + 1
    key = "l" if i == 0 else "r"
    n = _POSE6["fingers"].get(key, 0) if i < 2 else 0
    if not n:
        return _O6["_hand"](k, H, dirv, shape, hr, fold)
    # counting hand: n fingers up, fanned around the forearm direction, then the ball
    g = hr / P.HAND_R
    ux, uy = dirv
    fl = 0.125 * g * fold
    d = ""
    spread = (-36.0, -14.0, 8.0, 30.0, 62.0)
    for j in range(int(n)):
        a = spread[j] if n < 5 else spread[j]
        vx, vy = _rot(ux, uy, a)
        ln = fl * (0.75 if j == 4 else 1.0)
        d += "M%.4f,%.4f L%.4f,%.4f " % (H[0], H[1], H[0] + vx * ln, H[1] + vy * ln)
        k.ext.append((H[0] + vx * ln, H[1] + vy * ln, 0.025))
    out = P._stroke(k, d, 0.034 * g)
    return out + _O6["_hand"](k, H, dirv, "ball", hr, fold)


def _hair(k, C, yaw):
    """hair style "fringe" (CAST hair key): the temple crescents cut off above y = -0.08, a bald man's fringe of hair round
    the back of the head at ear height."""
    out = _O6["_hair"](k, C, yaw)
    H = C.get("hair") if isinstance(C, dict) else None
    if not H or H.get("style") != "fringe":
        return out
    k.defs.append('<clipPath id="%s_fr"><rect x="-0.8" y="%.4f" width="1.6" height="1.2"/></clipPath>' % (k.uid, H.get("top", -0.08)))
    return '<g clip-path="url(#%s_fr)">%s</g>' % (k.uid, out)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    b = g("basket")
    _POSE6["basket"] = b if isinstance(b, dict) else ({} if b else None)
    _POSE6["hood"] = _f(g("hood"), 1.0, 0.0, 1.0)
    _POSE6["pale"] = _f(g("pale"), 0.0, 0.0, 1.0)
    _POSE6["fingers"] = {"r": int(_f(g("fingers_r"), 0, 0, 5)), "l": int(_f(g("fingers_l"), 0, 0, 5))}
    _POSE6["hand_i"] = 0
    _POSE6["t"] = _num(g("t"), 0.0)
    _POSE6["basket_an"] = None
    return _O6["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _neckline(k, X, col, y0=0.40, w=0.18, depth=0.10):
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-w, y0) + X(0.0, y0 + depth * 2) + X(w, y0))
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="0.040"/>' % (d, k.c(col))
            + '<path d="%s" fill="none" stroke="%s" stroke-width="0.010" transform="translate(0 0.020)"/>' % (d, k.ink))


def _flour_spots(k, X, pts, col="#ffffff"):
    o = []
    for (x, y, r, rot) in pts:
        c = X(x, y)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.75" transform="rotate(%d %.4f %.4f)"/>'
                 % (c[0], c[1], r, r * 0.55, k.c(col), rot, c[0], c[1]))
    return "".join(o)


def _purse(k, x, y, col="#6a4428", dark="#3e2614"):
    """a fat leather coin purse hanging from the belt by a cord, a coin peeking out."""
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014"/>' % (x, y - 0.02, x, y + 0.05, k.ink)]
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        x - 0.04, y + 0.06, x - 0.12, y + 0.14, x - 0.06, y + 0.22, x, y + 0.25, x + 0.06, y + 0.22, x + 0.12, y + 0.14, x + 0.04, y + 0.06)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (x - 0.05, y + 0.07, x, y + 0.09, x + 0.05, y + 0.07, k.c(dark)))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.030" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x + 0.035, y + 0.055, k.c(GOLD["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f q-0.02,0.04 0,0.08" fill="none" stroke="#ffffff" stroke-width="0.010" opacity="0.5"/>' % (x - 0.05, y + 0.12))
    k.ext.append((x, y + 0.26, 0.03))
    return "".join(o)


def _cos_apron6(k, C, m):
    """baker / apprentice: a short wool tunic (round neckline, tunic skirt to mid-thigh) under a big linen apron (bib with a
    neck strap, skirt to C["apron_len"] below the torso), waist ties, flour smudges; optional rope belt + coin purse
    (C["purse"]) on the apron strings."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    ap = k.c(col["apron"])
    apd = k.c(col["apron_d"])
    o = [_neckline(k, X, col["dark"], 0.395, 0.17, 0.05)]
    # bib + neck strap
    bw = C.get("bib_w", 0.20)
    bib = [X(-bw, 0.58), X(bw, 0.58), X(bw + 0.03, yB - 0.10), X(-bw - 0.03, yB - 0.10)]
    o.append(_poly(k, bib, ap, 0.014))
    for s in (-1, 1):
        o.append(_ln([X(s * (bw - 0.02), 0.59), X(s * 0.12, 0.41)], ap, 0.032))
        o.append(_ln([X(s * (bw - 0.02), 0.59), X(s * 0.12, 0.41)], k.ink, 0.007, ' opacity="0.6"'))
    o.append(_flour_spots(k, X, C.get("bib_flour", ((-0.08, 0.72, 0.06, -20), (0.10, 0.86, 0.045, 15)))))
    inside = "".join(o)
    # tunic skirt (over the legs) then the apron skirt over it
    yt = yB - 0.16
    a = hw * 0.985
    hem = yB + C.get("tunic_len", 0.26)
    b = hw + C.get("tunic_flare", 0.08)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "tk", X, yt, a, hem, b, g, sw=0.028, folds=((-0.14, yt + 0.10, -0.20, hem - 0.03), (0.15, yt + 0.10, 0.22, hem - 0.03)),
                    fold_col=k.c(col["dark"]))]
    ya = yB - 0.12
    aa = hw * C.get("apron_wf", 0.80)
    ahem = yB + C.get("apron_len", 0.34)
    ov.append(C2._skirt(k, "ak", X, ya, aa, ahem, aa + C.get("apron_flare", 0.06), ap, sw=0.024,
                        folds=((-0.10, ya + 0.12, -0.14, ahem - 0.05), (0.12, ya + 0.12, 0.16, ahem - 0.05), (0.0, ya + 0.20, 0.01, ahem - 0.08)),
                        fold_col=apd))
    ov.append(_flour_spots(k, X, C.get("apron_flour", ((-0.15, ya + 0.20, 0.08, -15), (0.16, ya + 0.32, 0.06, 20), (-0.02, ahem - 0.10, 0.07, 5)))))
    # dirty hand-wipe marks
    c = X(0.18, ya + 0.12)
    ov.append('<path d="M%.4f,%.4f l0.07,0.10 M%.4f,%.4f l0.07,0.10" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.45"/>'
              % (c[0], c[1], c[0] + 0.03, c[1] - 0.01, apd))
    # waist ties (+ rope belt)
    ov.append(_ln([X(-hw * 0.99, ya + 0.005), X(hw * 0.99, ya + 0.005)], k.ink, 0.044))
    ov.append(_ln([X(-hw * 0.99, ya + 0.005), X(hw * 0.99, ya + 0.005)], k.c(col.get("tie", col["apron"])), 0.026))
    kx, ky = X(-hw * 0.70, ya + 0.01)
    ov.append('<path d="M%.4f,%.4f q-0.04,0.10 -0.01,0.17 M%.4f,%.4f q0.03,0.09 0.04,0.15" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.ink))
    ov.append('<path d="M%.4f,%.4f q-0.04,0.10 -0.01,0.17 M%.4f,%.4f q0.03,0.09 0.04,0.15" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.c(col.get("tie", col["apron"]))))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.032" ry="0.025" fill="%s" stroke="%s" stroke-width="0.010"/>' % (kx, ky, k.c(col.get("tie", col["apron"])), k.ink))
    if C.get("purse"):
        px, py = X(hw * 0.62, ya + 0.01)
        ov.append(_purse(k, px, py))
    return inside, "", "".join(ov)


def _cos_cloak6(k, C, m):
    """the hooded stranger: a long brown wool cloak closed at the throat with a brass ring clasp, falling to the shins in
    heavy folds (drawn over the legs); the hood is the hat (hat_style "hood"); with the hood pulled down (pose key hood < 0.5)
    it lies bunched on the shoulders behind the neck."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    # front edges of the cloak meeting under the clasp, a dark gap with the tunic below
    o.append(_poly(k, [X(-0.03, 0.50), X(0.03, 0.50), X(0.07, yB + 0.1), X(-0.07, yB + 0.1)], k.c(col["under"]), 0.0, "none"))
    o.append(_ln([X(-0.03, 0.50), X(-0.07, yB + 0.1)], k.ink, 0.016))
    o.append(_ln([X(0.03, 0.50), X(0.07, yB + 0.1)], k.ink, 0.016))
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.7"/>'
                 % (X(s * 0.20, 0.55) + X(s * 0.26, 0.80) + X(s * 0.22, yB) + (k.c(col["dark"]),)))
    inside = "".join(o)
    yt = yB - 0.30
    a = hw * 0.99
    hem = yB + C["leg"] * C.get("cloak_frac", 0.70)
    b = hw + C.get("cloak_flare", 0.16)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "ck", X, yt, a, hem, b, g, sw=0.030,
                    folds=((-0.05, yt + 0.25, -0.06, hem - 0.02), (-0.22, yt + 0.20, -0.30, hem - 0.05), (0.20, yt + 0.20, 0.28, hem - 0.05),
                           (0.08, yt + 0.30, 0.10, hem - 0.03)), fold_col=k.c(col["dark"]))]
    ov.append(_ln([X(0.0, yt + 0.02), X(0.02, hem)], k.ink, 0.014, ' opacity="0.8"'))
    # hem band
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" opacity="0.8"/>'
              % (X(-b + 0.03, hem - 0.05) + X(0, hem - 0.02) + X(b - 0.03, hem - 0.05) + (k.c(col["dark"]),)))
    if _POSE6["hood"] < 0.5:
        ov.append(_hood_bunch(k, X, col))
    # clasp
    cx, cy = X(0.0, 0.47)
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.045" fill="none" stroke="%s" stroke-width="0.030"/>' % (cx, cy, k.ink))
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.045" fill="none" stroke="%s" stroke-width="0.016"/>' % (cx, cy, k.c(GOLD["base"])))
    return inside, "", "".join(ov)


def _hood_bunch(k, X, col):
    """a pulled-down hood: a thick roll of cloth round the neck, over the shoulders."""
    pts = [X(-0.40, 0.42), X(-0.30, 0.37), X(0.0, 0.36), X(0.30, 0.37), X(0.40, 0.42), X(0.32, 0.53), X(0.0, 0.56), X(-0.32, 0.53)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col.get("hood", col["base"])), k.ink)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.8"/>' % (X(-0.30, 0.46) + X(0.0, 0.52) + X(0.30, 0.46) + (k.c(col["dark"]),)))
    return "".join(o)


LION = ("M0.00,0.10 L0.06,0.02 Q0.10,-0.04 0.18,-0.02 L0.40,0.00 Q0.48,-0.10 0.56,-0.06 L0.62,-0.14 Q0.70,-0.20 0.78,-0.14 Q0.84,-0.12 0.84,-0.04 "
        "L0.92,0.00 L0.84,0.04 Q0.80,0.12 0.72,0.12 L0.70,0.24 L0.64,0.24 L0.64,0.14 L0.42,0.14 L0.36,0.26 L0.30,0.26 L0.30,0.14 "
        "Q0.18,0.16 0.16,0.24 L0.10,0.26 L0.10,0.14 Q0.02,0.20 -0.06,0.10 Q-0.14,0.02 -0.12,-0.10 Q-0.08,-0.16 -0.04,-0.10 Q-0.08,0.02 0.00,0.10 Z")


def _lion(k, x, y, s):
    """a gold lion passant guardant (the royal arms), about 1.04 s wide x 0.46 s tall, centred on (x, y)."""
    return ('<g transform="translate(%.4f %.4f) scale(%.4f)"><path d="%s" transform="translate(-0.40 -0.03)" fill="%s" stroke="%s" stroke-width="%.4f" '
            'stroke-linejoin="round"/><circle cx="0.30" cy="-0.11" r="0.025" fill="%s"/></g>'
            % (x, y, s, LION, k.c(GOLD["base"]), k.ink, 0.022 / max(s, 1e-3) * 0.6, k.ink))


def _chain(k, X, col):
    """chain of office: a heavy gold chain of round links over the shoulders and a big medallion with a crown."""
    o = []
    pts = []
    for i in range(15):
        t = i / 14.0
        x = -0.30 + 0.60 * t
        y = 0.42 + 0.30 * (1 - (2 * t - 1) ** 2)
        pts.append(X(x, y))
    for i, p in enumerate(pts):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.030" ry="0.022" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%d %.4f %.4f)"/>'
                 % (p[0], p[1], k.c(GOLD["base"] if i % 2 else GOLD["light"]), k.ink, (i - 7) * 8, p[0], p[1]))
    mx, my = X(0.0, 0.80)
    o.append('<circle cx="%.4f" cy="%.4f" r="0.085" fill="%s" stroke="%s" stroke-width="0.016"/>' % (mx, my, k.c(GOLD["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.060" fill="none" stroke="%s" stroke-width="0.008"/>' % (mx, my, k.c(GOLD["dark"])))
    crown = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (
        mx - 0.040, my + 0.025, mx - 0.045, my - 0.025, mx - 0.020, my - 0.005, mx, my - 0.040, mx + 0.020, my - 0.005, mx + 0.045, my - 0.025, mx + 0.040, my + 0.025)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (crown, k.c(GOLD["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f q-0.02,0.04 0.01,0.07" fill="none" stroke="#ffffff" stroke-width="0.012" opacity="0.7"/>' % (mx - 0.05, my - 0.03))
    return "".join(o)


def _mail_pattern(k):
    pid = "%s_ml" % k.uid
    if not any(('id="%s"' % pid) in d for d in k.defs):
        k.defs.append('<pattern id="%s" width="0.050" height="0.040" patternUnits="userSpaceOnUse"><rect width="0.05" height="0.04" fill="%s"/>'
                      '<path d="M0,0.02 a0.0125,0.0125 0 0 1 0.025,0 a0.0125,0.0125 0 0 1 0.025,0 M-0.0125,0.04 a0.0125,0.0125 0 0 1 0.025,0 '
                      'a0.0125,0.0125 0 0 1 0.025,0 a0.0125,0.0125 0 0 1 0.025,0" fill="none" stroke="%s" stroke-width="0.007"/></pattern>'
                      % (pid, k.c(STEEL["base"]), k.c(STEEL["dark"])))
    return "url(#%s)" % pid


def _cos_tabard6(k, C, m):
    """tabard over a tunic (the inspector, revealed) or over mail (guards): a red front panel from the neck to below the hips
    with a gold border and the gold lions (C["lions"] = 1 or 3), a belt.  C["mail"]: mail shows at the sides and as a skirt
    under the tabard.  C["chain"]: chain of office.  C["cloak_back"]: a brown cloak thrown back over the shoulders (seen at
    the sides, behind the body) with the hood bunched at the neck."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    if C.get("mail"):
        o.append('<rect x="-0.8" y="0.3" width="1.6" height="1.4" fill="%s" opacity="0.95"/>' % _mail_pattern(k))
    tw = C.get("tabard_w", 0.62)
    tab = [X(-tw * hw, 0.38), X(tw * hw, 0.38), X(tw * hw * 1.02, yB + 0.1), X(-tw * hw * 1.02, yB + 0.1)]
    gt = C2._grad(k, "tb", col["tabard"], -tw * hw, tw * hw)
    o.append(_poly(k, tab, gt, 0.016))
    o.append(_neckline(k, X, col.get("neck", "#3a2a2a"), 0.395, 0.16, 0.045))
    nl = C.get("lions", 3)
    if nl == 3:
        for (yy, s) in ((0.62, 0.20), (0.80, 0.20), (0.98, 0.20)):
            c = X(0.0, yy)
            o.append(_lion(k, c[0], c[1], s * min(1.0, hw / 0.33)))
    else:
        c = X(0.0, 0.74)
        o.append(_lion(k, c[0], c[1], 0.30 * min(1.0, hw / 0.33)))
    for s in (-1, 1):
        o.append(_ln([X(s * (tw * hw - 0.025), 0.40), X(s * (tw * hw * 1.02 - 0.025), yB + 0.1)], k.c(GOLD["base"]), 0.020))
    inside = "".join(o)
    behind = ""
    if C.get("cloak_back"):
        cc = col["cloak"]
        cd = col.get("cloak_d", P._shade(cc, 0.6))
        hem = yB + C["leg"] * 0.66
        bb = []
        for s in (-1, 1):
            pts = [X(s * hw * 0.6, 0.38), X(s * (hw + 0.08), 0.48), X(s * (hw + 0.18), (yB + hem) / 2), X(s * (hw + 0.24), hem), X(s * (hw - 0.05), hem + 0.03),
                   X(s * (hw - 0.10), yB)]
            bb.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(cc), k.ink))
            bb.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.8"/>'
                      % (X(s * (hw + 0.06), 0.60) + X(s * (hw + 0.14), (yB + hem) / 2) + X(s * (hw + 0.16), hem - 0.03) + (k.c(cd),)))
            k.ext.append((X(s * (hw + 0.24), hem)[0], hem, 0.05))
        behind = "".join(bb)
    # skirt part of the tabard (+ mail skirt under it)
    yt = yB - 0.10
    hem = yB + C.get("tabard_len", 0.34)
    ov = []
    if C.get("mail"):
        mhem = yB + C.get("mail_len", 0.22)
        ov.append(C2._skirt(k, "mk", X, yt - 0.04, hw * 0.98, mhem, hw + 0.06, _mail_pattern(k), sw=0.024))
    ov.append(C2._skirt(k, "tk", X, yt, tw * hw * 1.02, hem, tw * hw * 1.02 + 0.03, gt, sw=0.024,
                        folds=((-0.06, yt + 0.08, -0.08, hem - 0.03), (0.07, yt + 0.08, 0.09, hem - 0.03)), fold_col=k.c(col.get("tabard_d", "#7a141a"))))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018"/>'
              % (X(-tw * hw, hem - 0.04) + X(0, hem - 0.015) + X(tw * hw, hem - 0.04) + (k.c(GOLD["base"]),)))
    yb = yB - 0.10
    ov.append(_ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.ink, 0.060))
    ov.append(_ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.c(col.get("belt", "#3a2620")), 0.040))
    bx, by = X(0.0, yb)
    ov.append('<rect x="%.4f" y="%.4f" width="0.070" height="0.056" rx="0.010" fill="none" stroke="%s" stroke-width="0.012"/>' % (bx - 0.035, by - 0.028, k.c(GOLD["base"])))
    if C.get("sword"):
        sx, sy = X(-hw * 0.85, yb)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.055" stroke-linecap="round"/>' % (sx, sy, sx - 0.06, sy + 0.55, k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (sx, sy, sx - 0.06, sy + 0.55, k.c("#5a3a26")))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (sx - 0.07, sy - 0.02, sx + 0.07, sy + 0.01, k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (sx - 0.07, sy - 0.02, sx + 0.07, sy + 0.01, k.c(STEEL["base"])))
        k.ext.append((sx - 0.06, sy + 0.56, 0.04))
    if C.get("chain") and not C.get("cloak_back"):
        ov.append(_chain(k, X, col))
    if C.get("cloak_back"):
        # the hood bunched at the back of the neck: drawn as a collar behind the head (over the shoulders)
        ov.append(_hood_bunch(k, X, dict(base=col["cloak"], hood=col["cloak"], dark=col.get("cloak_d", "#3e2818"))))
        if C.get("chain"):
            ov.append(_chain(k, X, col))
    return inside, behind, "".join(ov)


COSTUMES6 = {"apron6": _cos_apron6, "cloak6": _cos_cloak6, "tabard6": _cos_tabard6}


# ============================================================================= hats (head frame)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_linencap(k, C, yaw):
    """kit: a soft oversized linen cap slouching to the back side (away from the face), a band at the brow, flour dust."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = -1.0 if yaw >= 0 else 1.0
    pf = C.get("cap_puff", 1.0)
    xl, xr, yb = -0.475 + dx, 0.475 + dx, -0.250
    px = dx + s * (0.28 + 0.18 * min(1.0, abs(yaw) + 0.3)) * pf
    g = CE._gradient(k, "ht", col, x0=-0.55, x1=0.55, mid=0.32)
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (xl, yb, xl - 0.05, -0.50, dx - 0.30, -0.70, dx + 0.02 * s, -0.68,
            px - s * 0.10, -0.66 + 0.02, px + s * 0.12, -0.52, px + s * 0.06, -0.40,
            px, -0.33, xr if s > 0 else xl, -0.30, xr if s > 0 else xl, yb, dx, yb + 0.03, xl, yb))
    if s < 0:      # slouch to the screen-left: mirror the outline about the cap centre
        d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
             % (xr, yb, xr + 0.05, -0.50, dx + 0.30, -0.70, dx + 0.02 * s, -0.68,
                px - s * 0.10, -0.66 + 0.02, px + s * 0.12, -0.52, px + s * 0.06, -0.40,
                px, -0.33, xl, -0.30, xl, yb, dx, yb + 0.03, xr, yb))
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    # soft folds toward the slouch
    for f in (0.0, 0.35):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
                 % (dx - s * 0.25 + s * f, -0.60, dx + s * (0.10 + f), -0.50, px - s * 0.02, -0.42 + 0.02 * f, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>'
             % (dx - s * 0.36, -0.40, dx - s * 0.30, -0.60, dx - s * 0.08, -0.66, k.c(col["shine"])))
    # band
    band = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl - 0.01, yb - 0.065, dx, yb - 0.030, xr + 0.01, yb - 0.065, xr + 0.005, yb + 0.010, dx, yb + 0.050, xl - 0.005, yb + 0.010))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    # flour on the cap
    for i in range(5):
        fx = dx - 0.30 + 0.55 * _hsh(i, 3.0)
        fy = -0.62 + 0.25 * _hsh(i, 4.0)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.025" fill="#ffffff" opacity="0.7"/>' % (fx, fy))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.06, yb), (xr + 0.06, yb), (dx, -0.72), (px + s * 0.14, -0.50)))
    return "".join(o), (dx, -0.70)


def _hat_baldtuft(k, C, yaw):
    """henry: bald crown with a shine and one curly tuft of hair sticking up on top."""
    col = C["hat_colors"]
    dx = 0.05 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="M%.4f,-0.36 Q%.4f,-0.44 %.4f,-0.42" fill="none" stroke="#ffffff" stroke-width="0.040" stroke-linecap="round" opacity="0.9"/>'
             % (dx - 0.28, dx - 0.20, dx - 0.08))
    tuft = ("M%.4f,-0.475 C%.4f,-0.58 %.4f,-0.66 %.4f,-0.62 C%.4f,-0.60 %.4f,-0.55 %.4f,-0.58 "
            "M%.4f,-0.48 C%.4f,-0.60 %.4f,-0.68 %.4f,-0.70 "
            "M%.4f,-0.475 C%.4f,-0.56 %.4f,-0.60 %.4f,-0.57" % (dx - 0.04, dx - 0.10, dx - 0.02, dx + 0.02, dx + 0.06, dx + 0.03, dx - 0.01,
                                                                 dx + 0.01, dx + 0.06, dx + 0.10, dx + 0.04,
                                                                 dx + 0.05, dx + 0.12, dx + 0.18, dx + 0.15))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (tuft, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (tuft, k.c(col["base"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx + 0.04, -0.72), (dx + 0.20, -0.58), (dx - 0.12, -0.60)))
    return "".join(o), (dx + 0.04, -0.70)


def _hat_hood(k, C, yaw):
    """the hood of the stranger's cloak: a deep wool hood with a short point at the back, the face opening framed by a
    turned edge; the opening is in deep shadow (only two glints for the eyes and the mouth below the shadow read).
    Pose key hood 0..1: 1 = up, lower values slide it back off the head (fade), < 0.12 = not drawn (the cloak costume then
    shows it bunched on the shoulders)."""
    hood = _POSE6["hood"]
    if hood < 0.12:
        return "", (0.0, -0.484)
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    u = k.uid
    back = -1.0 if yaw >= 0 else 1.0
    off = (1.0 - hood)
    ty = 0.28 * off
    tx = back * 0.30 * off
    base = [(-0.60, 0.48), (-0.63, 0.05), (-0.58, -0.32), (-0.38, -0.60), (0.0, -0.70), (0.28, -0.70), (0.50, -0.80), (0.57, -0.55),
            (0.63, -0.15), (0.60, 0.48)]
    if back < 0:
        base = [(-x, y) for (x, y) in reversed(base)]
    outer = [(x + dx, y) for (x, y) in base]
    inner = [(0.40 + fx, 0.36), (0.42 + fx, 0.0), (0.36 + fx, -0.30), (fx, -0.43), (-0.36 + fx, -0.30), (-0.42 + fx, 0.0), (-0.40 + fx, 0.36)]
    d_out = P._smooth_open(outer)
    d = d_out + " L" + P._smooth_open(inner)[1:] + " Z"
    k.defs.append('<clipPath id="%s_hd"><path d="%s"/></clipPath>' % (u, P._smooth_closed(inner)))
    k.defs.append('<linearGradient id="%s_hs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0.95"/>'
                  '<stop offset="0.60" stop-color="%s" stop-opacity="0.90"/><stop offset="0.70" stop-color="%s" stop-opacity="0.35"/>'
                  '<stop offset="0.76" stop-color="%s" stop-opacity="0"/></linearGradient>' % (u, k.c("#1c1222"), k.c("#2a1c30"), k.c("#3a2a40"), k.c("#3a2a40")))
    g = CE._gradient(k, "ht", col, x0=-0.62, x1=0.62, mid=0.32)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f)" opacity="%.3f">' % (tx, ty, C["hat_tilt"], _smooth(0.12, 0.45, hood))]
    # shadow inside the opening (over the face drawing)
    sh = _smooth(0.3, 1.0, hood)
    o.append('<g clip-path="url(#%s_hd)" opacity="%.3f"><rect x="-0.6" y="-0.5" width="1.2" height="0.86" fill="url(#%s_hs)"/></g>' % (u, sh, u))
    L = _POSE6.get("L")
    if L and sh > 0.5 and _POSE6.get("blink", 0) < 2:
        for (x, s_) in ((L["xL"], L["sL"]), (L["xR"], L["sR"])):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="%.3f"/>'
                     % (x - 0.008, L["ey"] - 0.004, 0.046 * s_, 0.026 * s_, k.c("#fff6dc"), sh))
    o.append('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (d, g))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d_out, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (P._smooth_open(inner), k.c(col["edge"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_open(inner), k.ink))
    # folds
    for sd in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.75"/>'
                 % (dx + sd * 0.52, -0.25, dx + sd * 0.56, 0.05, dx + sd * 0.50, 0.40, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>'
             % (dx - 0.46, -0.30, dx - 0.40, -0.55, dx - 0.15, -0.66, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.64 + tx, 0.0 + ty), (dx + 0.64 + tx, 0.0 + ty), (dx + tx, -0.80 + ty), (dx + back * 0.52 + tx, -0.80 + ty), (dx, 0.50)))
    return "".join(o), (dx + tx, -0.74 + ty)


def _hat_hooddown(k, C, yaw):
    """the inspector revealed: no hat -- short dark hair with grey temples is the hair dict; nothing drawn here."""
    return "", (0.0, -0.484)


def _hat_kettlehat(k, C, yaw):
    """guard1: a steel kettle hat -- round dome with a raised rib, a wide brim sloping down all round, rivets, highlights."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx - 0.05 * yaw
    yb = -0.30
    g = CE._gradient(k, "ht", col, x0=-0.45, x1=0.45, mid=0.28)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.46, yb - 0.04, dx, yb - 0.12, dx + 0.46, yb - 0.04, dx + 0.74, yb + 0.10, dx, yb + 0.02, dx - 0.74, yb + 0.10)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, g, k.ink))
    dome = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.44, yb - 0.04, dx - 0.46, yb - 0.38, cx - 0.22, yb - 0.50, cx, yb - 0.50, cx + 0.22, yb - 0.50, dx + 0.46, yb - 0.38, dx + 0.44, yb - 0.04,
        dx, yb - 0.10, dx - 0.44, yb - 0.04)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
             % (cx, yb - 0.50, cx + 0.03 * yaw, yb - 0.30, dx + 0.15 * yaw, yb - 0.09, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
             % (cx - 0.012, yb - 0.49, cx + 0.03 * yaw - 0.012, yb - 0.30, dx + 0.15 * yaw - 0.012, yb - 0.09, k.c(col["shine"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.36, yb - 0.10, dx - 0.36, yb - 0.36, cx - 0.14, yb - 0.46, k.c(col["shine"])))
    for x in (-0.36, -0.18, 0.0, 0.18, 0.36):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.016" fill="%s" stroke="%s" stroke-width="0.006"/>' % (dx + x, yb - 0.06 - 0.025 * (1 - (x / 0.4) ** 2), k.c(col["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.8"/>'
             % (dx - 0.66, yb + 0.07, dx, yb - 0.005, dx + 0.66, yb + 0.07, k.c(col["light"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.78, yb + 0.1), (dx + 0.78, yb + 0.1), (cx, yb - 0.53)))
    return "".join(o), (cx, yb - 0.50)


def _hat_nasalhelm(k, C, yaw):
    """guard2: a conical steel helmet with a nasal bar down the middle of the face, over a mail coif framing the face down to
    the shoulders."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.12 * yaw
    u = k.uid
    outer = [(-0.56 + dx, 0.52), (-0.58 + dx, 0.0), (-0.52 + dx, -0.30), (dx, -0.48), (0.52 + dx, -0.30), (0.58 + dx, 0.0), (0.56 + dx, 0.52)]
    inner = [(0.40 + fx, 0.30), (0.42 + fx, -0.02), (0.36 + fx, -0.24), (fx, -0.30), (-0.36 + fx, -0.24), (-0.42 + fx, -0.02), (-0.40 + fx, 0.30)]
    d = P._smooth_open(outer) + " L" + P._smooth_open(inner)[1:] + " Z"
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="%s" fill-rule="evenodd"/>' % (d, _mail_pattern(k)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, k.ink))
    # cone
    g = CE._gradient(k, "ht", col, x0=-0.45, x1=0.45, mid=0.28)
    yb = -0.20
    tipx = dx + 0.05 * yaw
    cone = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.48, yb, dx - 0.42, yb - 0.38, tipx, yb - 0.62, dx + 0.42, yb - 0.38, dx + 0.48, yb, dx, yb + 0.05, dx - 0.48, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (cone, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.34, yb - 0.06, dx - 0.30, yb - 0.30, tipx - 0.06, yb - 0.52, k.c(col["shine"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.49, yb - 0.07, dx, yb - 0.02, dx + 0.49, yb - 0.07, dx + 0.49, yb + 0.005, dx, yb + 0.055, dx - 0.49, yb + 0.005)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (band, k.c(col["dark"]), k.ink))
    # nasal bar
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (fx - 0.035, yb, fx + 0.035, yb, fx + 0.028, 0.13, fx - 0.028, 0.13, k.c(col["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (fx - 0.012, yb + 0.02, fx - 0.010, 0.11, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.60, 0.0), (dx + 0.60, 0.0), (tipx, yb - 0.64), (dx, 0.54)))
    return "".join(o), (tipx, yb - 0.62)


def _hat_wimple(k, C, yaw):
    """woman1: a linen kerchief / veil over the head falling to the shoulders, with a white band under the chin and over the
    brow (barbette) framing the face."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    back = -1.0 if yaw >= 0 else 1.0
    outer = [(-0.56 + dx + (0.06 if back < 0 else 0), 0.62), (-0.60 + dx, 0.10), (-0.56 + dx, -0.30), (-0.30 + dx, -0.58), (dx, -0.63), (0.30 + dx, -0.58),
             (0.56 + dx, -0.30), (0.60 + dx, 0.10), (0.56 + dx - (0.06 if back > 0 else 0), 0.62)]
    inner = [(0.38 + fx, 0.40), (0.42 + fx, 0.05), (0.38 + fx, -0.22), (fx, -0.31), (-0.38 + fx, -0.22), (-0.42 + fx, 0.05), (-0.38 + fx, 0.40)]
    d = P._smooth_open(outer) + " L" + P._smooth_open(inner)[1:] + " Z"
    g = CE._gradient(k, "ht", col, x0=-0.6, x1=0.6, mid=0.32)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    # barbette: the band under the chin and across the brow (inner frame)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.060"/>' % (P._smooth_open(inner), k.c(col["band"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016"/>' % (P._smooth_open(inner), k.ink))
    for sd in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.7"/>'
                 % (dx + sd * 0.48, -0.30, dx + sd * 0.55, 0.10, dx + sd * 0.50, 0.55, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.44, -0.30, dx - 0.36, -0.52, dx - 0.10, -0.60, k.c(col["shine"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.62, 0.1), (dx + 0.62, 0.1), (dx, -0.66), (dx, 0.64)))
    return "".join(o), (dx, -0.63)


def _hat_strawhat(k, C, yaw):
    """man1: a battered wide straw hat -- low round crown, floppy brim with a frayed edge, weave lines, a cord band."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx - 0.06 * yaw
    rx, ry, cy = 0.78, 0.13, -0.32
    g = CE._gradient(k, "ht", col, x0=-0.5, x1=0.5, mid=0.30)
    gb = CE._gradient(k, "hb", col, x0=-rx, x1=rx, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    # floppy brim: back half
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - rx, cy + 0.06, dx - rx * 0.6, cy - ry * 1.2, dx, cy - ry, dx + rx * 0.6, cy - ry * 1.2, dx + rx, cy + 0.06,
        dx + rx * 0.5, cy + ry * 1.3, dx, cy + ry * 0.9, dx - rx * 0.5, cy + ry * 1.3, dx - rx, cy + 0.06)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, gb, k.ink))
    cw, ch = 0.40, 0.30
    yb = cy - 0.01
    crown = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" % (
        cx - cw, yb, cx - cw - 0.02, yb - ch * 0.8, cx - cw * 0.5, yb - ch, cx + 0.03, yb - ch * 0.95, cx + cw * 0.55, yb - ch * 1.02, cx + cw + 0.02, yb - ch * 0.8, cx + cw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (crown, g, k.ink))
    wv = "".join("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f " % (cx - cw + 0.03, yb - f * ch, cx, yb - f * ch - 0.03, cx + cw - 0.03, yb - f * ch) for f in (0.25, 0.5, 0.75))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (wv, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030"/>' % (cx - cw + 0.01, yb - 0.04, cx, yb - 0.01, cx + cw - 0.01, yb - 0.04, k.c(col["band"])))
    # front lip of the brim with frayed edge
    lip = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (dx - rx, cy + 0.06, dx - rx * 0.5, cy + ry * 1.3, dx, cy + ry * 0.9, dx + rx * 0.5, cy + ry * 1.3, dx + rx, cy + 0.06)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8" transform="translate(0 -0.03)"/>' % (lip, k.c(col["dark"])))
    fr = "".join("M%.4f,%.4f l%.4f,0.035 " % (dx + x, cy + 0.06 + ry * 1.0 * (1 - (x / rx) ** 2) + 0.01, 0.01 * (1 if x > 0 else -1))
                 for x in (-0.66, -0.52, -0.30, -0.12, 0.10, 0.34, 0.55, 0.68))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (fr, k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - rx - 0.02, cy + 0.06), (dx + rx + 0.02, cy + 0.06), (cx, yb - ch - 0.03), (dx, cy + ry * 1.3 + 0.05)))
    return "".join(o), (cx, yb - ch)


HATS6 = {"linencap": _hat_linencap, "baldtuft": _hat_baldtuft, "hood": _hat_hood, "hooddown": _hat_hooddown, "kettlehat": _hat_kettlehat,
         "nasalhelm": _hat_nasalhelm, "wimple": _hat_wimple, "strawhat": _hat_strawhat}


# ============================================================================= cast
HOSE = dict(color="#5a4234", dark="#3a2a20", cuff="#5a4234", len=0.86, w=0.13)

NEW_CAST6 = {
    # the apprentice: small boy, oversized linen apron to the shins over a slate-blue tunic, floppy linen cap, flour on the
    # hair, cheek and cap, rolled sleeves, brown hose, soft boots
    "kit": dict(
        _cast6=True, _cast4=True, build="boy", seed=8.3,
        torso_w=0.64, torso_h=0.80, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.245, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.82, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.055, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a090",
        hat="newsboy", hat_style="linencap", hat_tilt=-5.0, ear_pencil=False, cap_puff=1.0,
        hat_colors=dict(light="#fbf3e2", base="#e6d6b6", dark="#b8a47e", shine="#ffffff", band="#c8b48c"),
        hair=dict(color="#7a4626", front=0.09, grow=0.18),
        flour=dict(op=0.9, side=1),
        costume="apron6", apron_len=0.50, apron_wf=0.92, apron_flare=0.08, tunic_len=0.20, bib_w=0.19,
        sleeve=dict(color="#5f84a0", dark="#3e5a72", cuff="#6e94b0", len=0.55, w=0.150, roll=True),
        shorts=dict(HOSE, len=0.90, w=0.12),
        boots=dict(color="#6a4428", cuff="#8a5c38", h=0.11, toe=0.13, soft=True),
        colors=dict(base="#5f84a0", dark="#3e5a72", apron="#f1e8d4", apron_d="#c4b496", tie="#e4d8bc", pants="#5a4234"),
    ),
    # uncle henry: the stingiest baker -- round as a loaf, short legs, bald with one curly tuft, grey-brown fringe, huge bushy
    # moustache, tiny eyes, red cheeks; brick-red tunic, floury apron, a fat coin purse on the apron strings
    "henry": dict(
        _cast6=True, _cast3=True, _cast4=True, build="stout", seed=44.1,
        torso_w=1.38, torso_h=1.10, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.44, 0.40), arm=0.70, hip_x=0.18, leg=1.00, stance=0.06, wide=0.26, limb_w=0.070,
        eye_y=-0.010, eye_scale=0.70, brow="stroke", brow_th=0.072, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=1.30,
        smirk_side=-1, cheeks="#ec7c6c",
        hat="newsboy", hat_style="baldtuft", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#9a7a60", base="#7a5a42", dark="#4a3424"),
        hair=dict(color="#8a6a54", front=0.13, grow=0.24, style="fringe", top=-0.10),
        costume="apron6", apron_len=0.36, apron_wf=0.80, apron_flare=0.05, tunic_len=0.22, bib_w=0.26, purse=True,
        bib_flour=((-0.12, 0.74, 0.07, -20), (0.14, 0.92, 0.05, 15), (0.0, 1.10, 0.05, 0)),
        sleeve=dict(color="#9a3e2c", dark="#62241a", cuff="#b24c38", len=0.52, w=0.200, roll=True),
        shorts=dict(color="#4a3a36", dark="#2e2420", cuff="#4a3a36", len=0.86, w=0.15),
        boots=dict(color="#3a2a22", cuff="#57402e", h=0.10, toe=0.15),
        colors=dict(base="#9a3e2c", dark="#62241a", apron="#f4ecdc", apron_d="#c4b496", tie="#e4d8bc", pants="#4a3a36",
                    moustache="#7a5a46", moustache_l="#a88a72"),
    ),
    # the King's bread inspector, disguised: tall and thin, long brown hooded cloak, face in the hood's shadow
    "inspector": dict(
        _cast6=True, _cast4=True, build="slim", seed=52.6,
        torso_w=0.62, torso_h=1.10, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.80, hip_x=0.15, leg=1.50, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.020, brow="stroke", brow_th=0.064, mouth="frown", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="hood", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#9a7652", base="#6e4e32", dark="#42301e", shine="#b89670", edge="#5a3e26"),
        hair=dict(color="#2a2226", front=0.07, grow=0.20),
        costume="cloak6", cloak_frac=0.74, cloak_flare=0.18,
        sleeve=dict(color="#6e4e32", dark="#42301e", cuff="#5a3e26", len=0.78, w=0.200),
        shorts=dict(color="#3a3036", dark="#241e22", cuff="#3a3036", len=0.88, w=0.11),
        boots=dict(color="#2e2420", cuff="#4a3a30", h=0.24, toe=0.14),
        colors=dict(base="#6e4e32", dark="#42301e", under="#3a3036", hood="#6e4e32", pants="#3a3036"),
    ),
    # the same man, hood down: the royal tabard (three gold lions on red), chain of office, cloak thrown back, stern
    "inspector_royal": dict(
        _cast6=True, _cast4=True, build="slim", seed=52.6,
        torso_w=0.62, torso_h=1.10, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.80, hip_x=0.15, leg=1.50, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.020, brow="stroke", brow_th=0.064, mouth="frown", moustache=False, pencil_moustache=False, smirk_side=1, age_lines=True,
        hat="newsboy", hat_style="hooddown", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#9a7652", base="#6e4e32", dark="#42301e"),
        hair=dict(color="#2a2226", front=0.10, grow=0.22, style="cap", shine="#8a8492"),
        costume="tabard6", lions=3, chain=True, cloak_back=True, tabard_w=0.80, tabard_len=0.40,
        sleeve=dict(color="#2c3a66", dark="#1a2444", cuff="#e8b52e", len=0.80, w=0.150),
        shorts=dict(color="#3a3036", dark="#241e22", cuff="#3a3036", len=0.88, w=0.11),
        boots=dict(color="#2e2420", cuff="#4a3a30", h=0.24, toe=0.14),
        colors=dict(base="#2c3a66", tabard=ROYAL_RED, tabard_d="#6e1218", neck="#1a2444", belt="#2a1c18", cloak="#6e4e32", cloak_d="#42301e",
                    pants="#3a3036"),
    ),
    # guards: mail, red tabard with one gold lion, belt and sword; guard1 tall in a kettle hat, guard2 stocky, bearded, in a
    # nasal helmet over a mail coif
    "guard1": dict(
        _cast6=True, _cast4=True, build="slim", seed=61.7,
        torso_w=0.70, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.27, 0.50), arm=0.78, hip_x=0.17, leg=1.40, stance=0.08, wide=0.30, limb_w=0.060,
        eye_y=0.040, brow="stroke", brow_th=0.056, mouth="frown", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="kettlehat", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#e4e8ee", base="#9aa4b0", dark="#5a6270", shine="#ffffff"),
        hair=dict(color="#5a3a26", front=0.08, grow=0.20),
        costume="tabard6", lions=1, mail=True, sword=True, tabard_w=0.70, tabard_len=0.30, mail_len=0.26,
        sleeve=dict(color="#8d97a3", dark="#5d6672", cuff="#6d7782", len=0.62, w=0.150),
        shorts=dict(color="#4a3c34", dark="#2e2620", cuff="#4a3c34", len=0.86, w=0.12),
        boots=dict(color="#2a2220", cuff="#3e3430", h=0.22, toe=0.14),
        colors=dict(base="#8d97a3", tabard=ROYAL_RED, tabard_d="#6e1218", neck="#5d6672", belt="#2a1c18", pants="#4a3c34"),
    ),
    "guard2": dict(
        _cast6=True, _cast3=True, _cast4=True, build="regular", seed=63.2,
        torso_w=0.92, torso_h=0.98, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.34, 0.47), arm=0.74, hip_x=0.17, leg=1.12, stance=0.08, wide=0.30, limb_w=0.066,
        eye_y=0.010, brow="stroke", brow_th=0.066, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.95, smirk_side=-1,
        beard=dict(color="#7a3a22", dark="#4a200e"),
        hat="newsboy", hat_style="nasalhelm", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#e4e8ee", base="#9aa4b0", dark="#5a6270", shine="#ffffff"),
        hair=dict(color="#7a3a22", front=0.0, grow=0.0),
        costume="tabard6", lions=1, mail=True, sword=True, tabard_w=0.66, tabard_len=0.28, mail_len=0.24,
        sleeve=dict(color="#8d97a3", dark="#5d6672", cuff="#6d7782", len=0.62, w=0.170),
        shorts=dict(color="#3e3a44", dark="#26222a", cuff="#3e3a44", len=0.86, w=0.13),
        boots=dict(color="#2a2220", cuff="#3e3430", h=0.20, toe=0.14),
        colors=dict(base="#8d97a3", tabard=ROYAL_RED, tabard_d="#6e1218", neck="#5d6672", belt="#2a1c18", pants="#3e3a44",
                    moustache="#7a3a22", moustache_l="#a85a3a"),
    ),
    # townsfolk
    "woman1": dict(
        _cast6=True, build="slim", seed=71.4,
        torso_w=0.62, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.235, 0.52), arm=0.72, hip_x=0.14, leg=1.16, stance=0.05, wide=0.24, limb_w=0.055,
        eye_y=0.040, brow="stroke", brow_th=0.034, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f2a0a0",
        hat="newsboy", hat_style="wimple", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#fbf7ee", base="#eae2d0", dark="#bcae92", shine="#ffffff", band="#ffffff"),
        hair=dict(color="#6a3a24", front=0.0, grow=0.0),
        costume="shawl", hem_frac=0.86, skirt_flare=0.20,
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.06, toe=0.11),
        colors=dict(base="#4e7a4a", shawl="#c79a62", shawl_d="#8a6634", skirt="#8a3c30", skirt_d="#5a2018", band="#d8b46a", pants="#8a3c30"),
    ),
    "man1": dict(
        _cast6=True, _cast3=True, _cast4=True, build="regular", seed=74.9,
        torso_w=0.86, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.20, stance=0.07, wide=0.28, limb_w=0.062,
        eye_y=0.030, brow="stroke", brow_th=0.052, mouth="smirk", moustache=False, smirk_side=1, cheeks="#e8907a",
        beard=dict(color="#8a6a40", dark="#5a4224"),
        hat="newsboy", hat_style="strawhat", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#f2d88e", base="#d8b25a", dark="#9a7a32", band="#7a4a2a"),
        hair=dict(color="#8a6a40", front=0.08, grow=0.20),
        costume="tunic", tunic_len=0.26, tunic_flare=0.10,
        sleeve=dict(color="#8a7a50", dark="#5e5232", cuff="#9a8a5e", len=0.52, w=0.150, roll=True),
        shorts=dict(color="#6a5a4a", dark="#463a2e", cuff="#7a6a58", len=0.55, w=0.13),
        boots=dict(color="#5a4030", cuff="#7a5a40", h=0.09, toe=0.13, soft=True),
        colors=dict(base="#8a7a50", dark="#5e5232", lining="#4a3e22", patch="#a8583a", stitch="#e8d8a8", rope="#d6b47c", rope_d="#8a6a3c",
                    pants="#6a5a4a"),
    ),
    # the other baker (pilloried in week 1): thin, droopy, sad; white linen coif, grey-green tunic, apron
    "baker2": dict(
        _cast6=True, _cast4=True, build="slim", seed=81.5,
        torso_w=0.56, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.22, 0.50), arm=0.76, hip_x=0.14, leg=1.34, stance=0.06, wide=0.24, limb_w=0.052,
        eye_y=0.050, brow="stroke", brow_th=0.040, mouth="wavy", moustache=False, pencil_moustache=True, smirk_side=1, age_lines=True,
        hat="newsboy", hat_style="skullcap", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#ffffff", base="#ece6da", dark="#bcb2a2", shine="#ffffff", cuff="#f6f2ea", stitch="#bcb2a2"),
        hair=dict(color="#3a2e2a", front=0.07, grow=0.20),
        flour=dict(op=0.5, side=-1),
        costume="apron6", apron_len=0.34, apron_wf=0.85, apron_flare=0.04, tunic_len=0.22, bib_w=0.16,
        sleeve=dict(color="#6f7a5e", dark="#4a523e", cuff="#7e8a6c", len=0.54, w=0.130, roll=True),
        shorts=dict(color="#4a4440", dark="#2e2a28", cuff="#4a4440", len=0.86, w=0.11),
        boots=dict(color="#3a2e26", cuff="#3a2e26", h=0.09, toe=0.13),
        colors=dict(base="#6f7a5e", dark="#4a523e", apron="#ece4d2", apron_d="#bcae92", tie="#e0d4ba", pants="#4a4440"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast6.py canvas): every arm preset with
# every film-6 prop at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects, the pillory, every STORY6 pose and
# the walk / run cycles of the member; >= 0.32 D head room.
CANVAS6 = {
    "kit": (-1.5625, -3.8750, 1.5625, 0.1875),
    "henry": (-1.8125, -4.3750, 1.8125, 0.1250),
    "inspector": (-1.6875, -4.8750, 1.6875, 0.1250),
    "inspector_royal": (-1.6875, -4.8750, 1.6875, 0.1250),
    "guard1": (-1.6875, -5.5000, 1.6875, 0.1250),
    "guard2": (-1.7500, -5.0625, 1.7500, 0.1250),
    "woman1": (-1.6875, -4.3125, 1.6875, 0.2500),
    "man1": (-1.7500, -4.4375, 1.7500, 0.1250),
    "baker2": (-1.6875, -4.5625, 1.6875, 0.1250),
}


# ============================================================================= figure wrapper: the pillory
def _pillory_wrap(f, spec, uid, mirror):
    """draw the pillory board over the body at the neck, then the head (everything above the board top, plus the head disc)
    and both hands again over it, so head and hands poke through the holes.  The post runs down to the feet line."""
    sp = spec if isinstance(spec, dict) else {}
    an = f["anchors"]
    k = P._Ctx(str(uid) + "_pl", P.INK, None)
    cx = _num(sp.get("x"), an["head"][0])
    top = _num(sp.get("top"), an["head"][1] + 0.40)
    post = sp.get("post", True)
    board, split, holes = _pillory_board(k, cx, top, post_to=(f["feet_y"] + 0.02) if post else None, mirror=mirror)
    u = k.uid
    hr = 0.115
    clip = ('<clipPath id="%s_pc"><rect x="-6" y="-8" width="12" height="%.4f"/><circle cx="%.4f" cy="%.4f" r="0.53"/>'
            '<circle cx="%.4f" cy="%.4f" r="%.4f"/><circle cx="%.4f" cy="%.4f" r="%.4f"/></clipPath>'
            % (u, top + 8.0, an["head"][0], an["head"][1], an["hand_l"][0], an["hand_l"][1], hr, an["hand_r"][0], an["hand_r"][1], hr))
    svg = ('%s<defs>%s%s</defs>%s<use href="#%s_fig" clip-path="url(#%s_pc)"/>'
           % (f["svg"], "".join(k.defs), clip, board, uid, u))
    x0, y0, x1, y1 = f["bbox"]
    for (x, y, r) in k.ext:
        x0, y0, x1, y1 = min(x0, x - r), min(y0, y - r), max(x1, x + r), max(y1, y + r)
    a = dict(an)
    a["pillory_top"] = (cx, top)
    a["pillory_neck"] = (holes[0][0], split)
    a["pillory_wrist_l"] = (holes[1][0], split)
    a["pillory_wrist_r"] = (holes[2][0], split)
    return dict(f, svg='<g id="%s_plw">%s</g>' % (uid, svg), bbox=(x0, y0, x1, y1), anchors=a)


def figure(cast_name, pose=None, uid="p"):
    f = _O6["figure"](cast_name, pose, uid)
    if isinstance(pose, dict) and pose.get("pillory") and isinstance(cast_name, str) and cast_name in P.CAST:
        f = _pillory_wrap(f, pose["pillory"], uid, bool(pose.get("mirror")))
    if _POSE6.get("basket_an") and isinstance(pose, dict) and pose.get("basket") is not None:
        a = dict(f["anchors"])
        sx, sy = (1.0, 1.0)
        sq = pose.get("squash")
        if isinstance(sq, (int, float)):
            sx = sy = float(sq)
        elif isinstance(sq, (tuple, list)) and len(sq) >= 2:
            sx, sy = float(sq[0]), float(sq[1])
        mir = -1.0 if pose.get("mirror") else 1.0
        for n, v in _POSE6["basket_an"].items():
            a[n] = (mir * v[0] * sx, v[1] * sy)
        f = dict(f, anchors=a)
    return f


# ============================================================================= cycles, lip-sync, blink
_SHOULDER = {}


def _shoulders(cast):
    if cast not in _SHOULDER:
        f = _O6["figure"](cast, {}, "q")
        _SHOULDER[cast] = (f["anchors"]["shoulder_l"], f["anchors"]["shoulder_r"], f["anchors"]["hand_l"], f["anchors"]["hand_r"])
    return _SHOULDER[cast]


def cycle(cast, phase, mode="walk", facing=1, base=None, arms="both", speed=1.0):
    """one frame of a walk or run cycle.  phase 0..1 (one full cycle = two steps; loop it: phase = frame / frames_per_cycle),
    mode "walk" (about 28 frames per cycle at 30 fps), "run" (about 16), "sneak" (tiptoe, crouched), "march" (stiff, guards);
    facing +1 = toward screen-right, -1 = toward screen-left (the figure is drawn with mirror=True: whatever base holds in
    prop_r then shows in the screen-left hand).  base: a pose dict to start from (expr, mouth, props, fx ... are kept);
    arms: "both", "r", "l" or "none" = which arms swing (keep the other arm of base, e.g. the one holding a loaf);
    speed scales the stride.  Returns a pose dict (stride / lift / knee bend, arm swing, lean, bob, head roll)."""
    b0 = dict(base or {})
    p = dict(b0)
    ph = 2.0 * math.pi * _num(phase, 0.0)
    s, c = math.sin(ph), math.cos(ph)
    fc = 1.0 if _num(facing, 1.0) >= 0 else -1.0
    sp = _clamp(_num(speed, 1.0), 0.3, 1.6)
    if mode == "run":
        stride, lift, crouch, lean, swing = 1.30, 1.00, 0.10, 12.0, 0.30
    elif mode == "sneak":
        stride, lift, crouch, lean, swing = 0.70, 0.60, 0.18, 9.0, 0.08
    elif mode == "march":
        stride, lift, crouch, lean, swing = 1.00, 0.60, 0.03, 0.0, 0.16
    else:
        mode = "walk"
        stride, lift, crouch, lean, swing = 1.05, 0.45, 0.04, 3.0, 0.20
    stride *= sp
    # right leg forward when s > 0; the leg swinging forward (velocity c > 0 for the right leg) is lifted
    lr = max(0.0, c) * lift * (1.0 - 0.35 * abs(s))
    ll = max(0.0, -c) * lift * (1.0 - 0.35 * abs(s))
    p["legs"] = dict(stride=stride * s, lift_r=lr, lift_l=ll, knee_r=0.5 + 0.5 * max(0.0, c), knee_l=0.5 + 0.5 * max(0.0, -c),
                     toe_r=1.0, toe_l=1.0, crouch=crouch + (0.05 if mode == "run" else 0.03) * s * s, spread=-0.03)
    if "yaw" not in b0:
        p["yaw"] = 0.75
    p["lean"] = b0.get("lean", 0.0) + lean + (1.0 if mode != "run" else 3.0) * abs(s)
    p["head_roll"] = b0.get("head_roll", 0.0) - 2.0 * s * (1.5 if mode == "run" else 1.0)
    p["head_dy"] = _clamp(b0.get("head_dy", 0.0) + 0.012 * c * c, -0.8, 0.8)
    sl, sr, hl, hr = _shoulders(cast)
    for key, sh, hd, sg in (("r", sr, hr, 1.0), ("l", sl, hl, -1.0)):
        if arms not in ("both", key):
            continue
        a = -s if key == "r" else s                # the arm opposite the forward leg swings forward (+x)
        if mode == "run":
            hx = sh[0] + 0.05 * sg + 0.30 * a
            hy = sh[1] + 0.38 - 0.16 * max(0.0, a) + 0.04 * max(0.0, -a)
            p["arm_" + key] = dict(hand=(hx, hy), bend=0.9, sharp=0.6, stretch=1.05, layer="back" if key == "l" else "front")
        else:
            hx = hd[0] + swing * a
            hy = hd[1] - 0.05 * abs(a)
            p["arm_" + key] = dict(hand=(hx, hy), bend=0.5, stretch=1.0, layer="back" if key == "l" else "front")
    if fc < 0:
        p["mirror"] = not bool(b0.get("mirror", False))
    return p


def talk_mouth(frame, level=1.0, seed=0.0, hold=2):
    """lip-sync mouth name for a frame (a new drawing every `hold` frames): silent level 0 = "flat"; loud = mostly talk_b."""
    lev = _clamp(_num(level, 1.0), 0.0, 1.0)
    if lev <= 0.02:
        return "flat"
    i = int(_num(frame, 0.0)) // max(1, int(hold))
    r = _hsh(i, seed)
    if r < 0.18:
        return "flat" if lev < 0.6 else "talk_a"
    if r < 0.30:
        return "talk_o"
    if r < 0.30 + 0.45 * lev:
        return "talk_b"
    return "talk_a"


def blink_at(frame, period=96, offset=0):
    """auto blink: 0 open, then half / closed / half (frames 0..2 of every period)."""
    f = (int(_num(frame, 0.0)) - int(offset)) % max(8, int(period))
    return {0: 1, 1: 2, 2: 1}.get(f, 0)


NOD = (0.0, 0.25, 0.45, 0.35, 0.10, 0.0)       # pitch keys of one slow nod (hold each about 4 frames)


# ============================================================================= story poses
def _feet_y(cast, pose):
    return P.figure(cast, pose, "q")["feet_y"]


GUARDS = (("guard1", ""), ("guard2", "_guard2"))
TOWN = (("woman1", ""), ("man1", "_man1"))
SPEAR = dict(type="spear", angle=-88)


def _story():
    S, M = {}, {}
    # --- kit
    S["kit_watch_steam"] = ("kit", dict(yaw=0.35, pitch=-0.55, expr="happy", head_roll=-5, gaze=(0.5, -0.9),
                                        arm_r=dict(hand=(0.10, 0.70), bend=0.8), arm_l=dict(hand=(-0.08, 0.72), bend=0.8), legs="narrow"))
    M["kit_watch_steam"] = dict(note="looking up happily at the steam rising off the fresh loaves, hands clasped")
    S["kit_hold_loaf"] = ("kit", dict(yaw=0.40, pitch=-0.25, expr="grinning", head_roll=-6, gaze=(0.6, -0.3),
                                      arm_r=dict(hand=(0.74, -0.02), bend=-0.6, stretch=1.3), prop_r="loaf", arm_l="akimbo", legs="wide"))
    M["kit_hold_loaf"] = dict(note="the 13th loaf held up on the screen-right palm (prop_tip_r = loaf centre)")
    S["kit_slip_loaf"] = ("kit", dict(yaw=0.55, pitch=0.25, expr="smirk", head_roll=4, gaze=(-0.9, 0.0), lean=12,
                                      arm_r=dict(hand=(0.70, 0.52), bend=-0.4, stretch=1.3), prop_r="loaf",
                                      arm_l=dict(hand=(-0.10, 0.60), shape="point", bend=0.7), legs=dict(preset="step", stride=0.5, crouch=0.10)))
    M["kit_slip_loaf"] = dict(note="sneaking the 13th loaf into the customer's basket on screen-right, glancing back at henry; put "
                                   "the basket's rim (set dressing or basket_svg) under prop_tip_r")
    S["kit_hold_basket"] = ("kit", dict(yaw=0.30, expr="happy", head_roll=-4, arm_r=dict(hand=(0.50, 0.30), bend=-0.7, stretch=1.3),
                                        prop_r="basket", basket=dict(loaves=13), arm_l="akimbo", legs="wide"))
    M["kit_hold_basket"] = dict(note="the basket of 13 hanging from his screen-right hand (pose key basket=dict(loaves=0..13))")
    S["kit_scared"] = ("kit", dict(yaw=-0.30, pitch=0.30, expr="worried", fx=["sweat"], head_roll=8, lean=-4, squash=(1.03, 0.96),
                                   arm_r=dict(hand=(0.18, 0.40), bend=-0.6, shape="open"), arm_l=dict(hand=(-0.20, 0.38), bend=-0.6, shape="open"),
                                   legs="narrow"))
    M["kit_scared"] = dict(note="cowering while henry yells (shrunk, hands up at the chest)")
    S["kit_think"] = ("kit", dict(yaw=0.30, pitch=-0.20, expr="determined", head_roll=-4, gaze=(0.7, -0.6),
                                  arm_r="chin", arm_l=dict(hand=(-0.10, 0.78), bend=0.7), legs="narrow"))
    M["kit_think"] = dict(note="thinking: hand on the chin (the afternoon re-weighing)")
    S["kit_shout_run"] = ("kit", dict(yaw=0.80, pitch=-0.35, expr="shouting", mouth="talk_b", fx=["sweat"], lean=12, head_roll=-8,
                                      legs=dict(preset="step", stride=1.2, lift_l=0.8, knee_l=1.0, toe_r=1.0),
                                      arm_r=dict(hand=(0.66, -0.50), bend=-0.9, stretch=1.3, layer="top"), prop_r="loaf",
                                      arm_l=dict(hand=(-0.50, 0.70), bend=0.6, layer="back", stretch=1.2, shape="open")))
    M["kit_shout_run"] = dict(note="running through the crowd shouting 'the weight evaporated, I'll make it up!', the loaf held high")
    S["kit_put_loaf"] = ("kit", dict(yaw=0.65, pitch=0.30, expr="determined", head_roll=-6, lean=14, gaze=(0.8, 0.4),
                                     arm_r=dict(hand=(0.80, 0.25), bend=-0.5, stretch=1.3), prop_r="loaf",
                                     arm_l=dict(hand=(0.50, 0.45), bend=-0.5, stretch=1.3, shape="open"), legs=dict(preset="step", stride=0.6)))
    M["kit_put_loaf"] = dict(note="placing the loaf on the big scale pan (screen-right): prop_tip_r = loaf centre; plant the pan under it")
    S["kit_proud"] = ("kit", dict(yaw=0.20, pitch=-0.35, expr="grinning", head_roll=-5, arm_l="akimbo", arm_r="akimbo", legs="wide"))
    # --- henry
    S["henry_yell"] = ("henry", dict(yaw=-0.40, pitch=-0.5, expr="furious", mouth="talk_b", fx=["steam", dict(type="anger_fill", level=0.55)], head_roll=-8, lean=-4,
                                     arm_l=dict(hand=(-0.98, 0.10), shape="point", bend=-0.6, stretch=1.3), arm_r="akimbo", legs="wide"))
    M["henry_yell"] = dict(note="yelling at kit (screen-left), pointing, steam out of the ears; animate fx anger_fill level 0->1 and "
                                "mouth with talk_mouth()")
    S["henry_laugh_smug"] = ("henry", dict(yaw=0.20, pitch=-0.40, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], head_roll=12, lean=-6,
                                           head_dy=0.03, squash=(1.03, 0.97), t=0.3,
                                           arm_r=dict(hand=(0.36, 1.10), bend=0.9), arm_l=dict(hand=(-0.40, 1.06), bend=0.9), legs="wide"))
    M["henry_laugh_smug"] = dict(note="'they cheat, I'm honest!': eyes shut, belly laugh, both hands on the belly", smug=dict(expr="smug", mouth="smirk", blink=0))
    S["henry_count"] = ("henry", dict(yaw=0.25, pitch=0.35, expr="unimpressed", head_roll=-4, gaze=(0.3, 0.8),
                                      arm_r=dict(hand=(0.74, -0.06), bend=-0.8, stretch=1.3), fingers_r=3,
                                      arm_l="akimbo", legs="stand"))
    M["henry_count"] = dict(note="counting on his fingers (pose key fingers_r / fingers_l = 1..5 fingers up), lips moving: step "
                                 "fingers_r 1..5 and talk_mouth() for 'eleven, twelve.'")
    S["henry_pale"] = ("henry", dict(yaw=-0.20, pitch=-0.10, expr="shocked", pale=1.0, fx=["sweat"], head_roll=-4, squash=(0.97, 1.03),
                                     arm_r=dict(hand=(0.50, 0.30), bend=-0.7, shape="open", stretch=1.2),
                                     arm_l=dict(hand=(-0.50, 0.28), bend=-0.7, shape="open", stretch=1.2), legs="narrow"))
    M["henry_pale"] = dict(note="pale with fright: pose key pale 0..1 drains the face blue (animate 0->1 over ~10 frames)")
    S["henry_dragged"] = ("henry", dict(yaw=0.10, pitch=-0.30, expr="shouting", pale=0.7, fx=["sweat"], head_roll=6, lean=-6,
                                        arm_r=dict(hand=(0.82, 0.10), bend=-0.5, shape="open", stretch=1.3),
                                        arm_l=dict(hand=(-0.82, 0.12), bend=-0.5, shape="open", stretch=1.3),
                                        legs=dict(preset="wide", crouch=0.12, toe_r=0.6, toe_l=-0.6)))
    M["henry_dragged"] = dict(note="arms out to both sides (a guard grabs each hand_r / hand_l), heels digging in, pale")
    S["henry_shoo"] = ("henry", dict(yaw=-0.45, pitch=-0.4, expr="angry", mouth="talk_a", head_roll=-6,
                                     arm_l=dict(hand=(-0.86, -0.12), shape="open", bend=-0.8, stretch=1.3), arm_r="akimbo", legs="stand"))
    M["henry_shoo"] = dict(note="shooing kit away (screen-left): animate the open hand flapping (hand y -0.12 .. 0.15)")
    S["henry_in_pillory"] = ("henry", dict(yaw=0.0, pitch=0.10, expr="worried", pale=0.8, fx=["sweat"], head_roll=0,
                                           arm_r=dict(hand=(0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3),
                                           legs="stand", pillory=True))
    M["henry_in_pillory"] = dict(note="henry locked in the pillory (pose key pillory=True: board over the neck, hands through)")
    S["henry_add_13th"] = ("henry", dict(yaw=0.45, pitch=0.30, expr="happy", head_roll=-6, lean=6,
                                         arm_r=dict(hand=(0.66, 0.50), bend=-0.5, stretch=1.3), prop_r="loaf",
                                         arm_l=dict(hand=(-0.40, 1.04), bend=0.6), legs="stand"))
    M["henry_add_13th"] = dict(note="the ending: henry himself puts the 13th loaf into the basket (screen-right), smiling")
    # --- inspector
    S["inspector_hooded"] = ("inspector", dict(yaw=0.25, pitch=0.15, expr="neutral", hood=1.0,
                                               arm_r=dict(hand=(0.20, 0.95), bend=0.6), arm_l=dict(hand=(-0.18, 0.98), bend=0.6), legs="stand"))
    M["inspector_hooded"] = dict(note="the hooded stranger at the counter, face in shadow (only eye glints and the mouth)")
    S["inspector_buy"] = ("inspector", dict(yaw=-0.45, pitch=0.10, expr="neutral", hood=1.0,
                                            arm_l=dict(hand=(-0.60, 0.30), bend=-0.6, stretch=1.3), prop_l="basket", basket=dict(loaves=12),
                                            arm_r=dict(hand=(0.16, 0.98), bend=0.6), legs="stand"))
    M["inspector_buy"] = dict(note="takes the basket of exactly 12 from henry (screen-left)")
    S["inspector_hood_drop"] = ("inspector", dict(yaw=0.0, pitch=-0.2, expr="determined", hood=0.45,
                                                  arm_r=dict(hand=(0.40, -0.55), bend=-1.0, stretch=1.3), arm_l=dict(hand=(-0.40, -0.52), bend=-1.0, stretch=1.3),
                                                  legs="wide"))
    M["inspector_hood_drop"] = dict(note="both hands throw the hood back: animate pose key hood 1 -> 0 over ~8 frames, then cut to "
                                         "inspector_royal (cloak open, tabard + chain) on a blink")
    S["inspector_reveal"] = ("inspector_royal", dict(yaw=0.0, pitch=-0.45, expr="determined", head_roll=0, arm_l="akimbo",
                                                     arm_r=dict(hand=(0.60, -0.20), shape="open", bend=-0.6, stretch=1.2), legs="wide"))
    M["inspector_reveal"] = dict(note="'the King's bread inspector!' -- stern, chain of office, one hand raised")
    S["inspector_pour"] = ("inspector_royal", dict(yaw=0.55, pitch=0.35, expr="determined", head_roll=-4, lean=6, gaze=(0.8, 0.6),
                                                   arm_r=dict(hand=(0.95, 0.52), bend=-0.4, stretch=1.3), prop_r="basket",
                                                   basket=dict(loaves=7, tilt=62, pour=0.35),
                                                   arm_l=dict(hand=(0.45, 0.62), bend=-0.5, stretch=1.3, shape="open"), legs="wide"))
    M["inspector_pour"] = dict(note="pours the basket onto the big scale pan (screen-right): pose key basket tilt -110..0 and pour 0..1 "
                                    "(animate pour as a phase while loaves counts 12 -> 0); the basket hangs in front of the chest, its opening "
                                    "to screen-right, loaves fall from anchor basket_lip; the other hand lifts anchor basket_base")
    S["inspector_nod"] = ("inspector_royal", dict(yaw=-0.30, pitch=0.30, expr="smug", head_roll=-3, arm_l="akimbo", arm_r="akimbo", legs="stand"))
    M["inspector_nod"] = dict(note="the slow nod: step pitch through cast6.NOD (0, .25, .45, .35, .10, 0), about 4 frames each", nod=NOD)
    S["inspector_stern"] = ("inspector_royal", dict(yaw=-0.40, pitch=-0.35, expr="angry", mouth="talk_a", head_roll=-3,
                                                    arm_l=dict(hand=(-0.92, 0.05), shape="point", bend=-0.6, stretch=1.3), arm_r="akimbo", legs="wide"))
    M["inspector_stern"] = dict(note="pointing at henry: 'short weight!'")
    # --- guards
    for c, sfx in GUARDS:
        S["guard_stand" + sfx] = (c, dict(yaw=0.30, pitch=-0.25, expr="determined", arm_r=dict(hand=(0.42, 0.60), bend=0.4), prop_r=SPEAR,
                                          arm_l="akimbo", legs="wide"))
        S["guard_drag" + sfx] = (c, dict(yaw=0.55, pitch=-0.10, expr="angry", lean=-10, head_roll=-4,
                                         arm_r=dict(hand=(0.80, 0.30), bend=-0.5, stretch=1.3, shape="open"),
                                         arm_l=dict(hand=(-0.30, 0.55), bend=0.4), prop_l=dict(type="spear", angle=-70),
                                         legs=dict(preset="wide", stride=0.3, crouch=0.10, toe_l=-0.8)))
        S["guard_point" + sfx] = (c, dict(yaw=-0.40, pitch=-0.40, expr="angry", mouth="talk_b", head_roll=-5,
                                          arm_l=dict(hand=(-0.95, 0.05), shape="point", bend=-0.6, stretch=1.3),
                                          arm_r=dict(hand=(0.42, 0.60), bend=0.4), prop_r=SPEAR, legs="wide"))
    M["guard_stand"] = dict(note="guard1 at ease, spear upright (prop_tip_r = spear point); _guard2 for guard2 (same for drag / point)")
    M["guard_drag"] = dict(note="hauling henry (screen-right): the open hand grabs henry's hand_l, leaning back")
    # --- townsfolk
    veg = {"woman1": "tomato", "man1": "cabbage"}
    for c, sfx in TOWN:
        S["town_laugh" + sfx] = (c, dict(yaw=-0.35, pitch=-0.3, expr="laughing", fx=["tears"], head_roll=-10, lean=-5, t=0.6,
                                         arm_l=dict(hand=(-0.84, -0.12), shape="point", bend=-0.8, stretch=1.3),
                                         arm_r=dict(hand=(0.24, 1.00), bend=0.9)))
        S["town_point" + sfx] = (c, dict(yaw=0.45, pitch=-0.3, expr="smug", mouth="talk_b", head_roll=6,
                                         arm_r=dict(hand=(0.95, 0.00), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
        S["town_raise_veg" + sfx] = (c, dict(yaw=0.40, pitch=-0.45, expr="angry", mouth="talk_b", head_roll=-6, lean=-6,
                                             arm_r=dict(hand=(0.66, -0.74), bend=-1.0, stretch=1.3, layer="top"), prop_r=veg[c],
                                             arm_l=dict(hand=(-0.50, 0.40), bend=-0.4, shape="open", stretch=1.2), legs="wide"))
        S["town_throw" + sfx] = (c, dict(yaw=0.55, pitch=-0.2, expr="furious", head_roll=8, lean=10,
                                         arm_r=dict(hand=(0.85, -0.25), bend=-0.6, stretch=1.3, shape="open"),
                                         arm_l=dict(hand=(-0.55, 0.50), bend=0.3), legs=dict(preset="step", stride=0.8)))
    M["town_raise_veg"] = dict(note="woman1 raises a rotten tomato, _man1 a rotten cabbage (prop_r); swap the prop for the other veg freely")
    M["town_throw"] = dict(note="release frame of a throw: no prop in the hand -- fly cabbage_svg() / tomato_svg() from prop_tip_r")
    # --- baker2
    S["baker2_pillory"] = ("baker2", dict(yaw=0.0, pitch=0.30, expr="sad", head_roll=-6,
                                          arm_r=dict(hand=(0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3),
                                          legs="narrow", pillory=True))
    M["baker2_pillory"] = dict(note="locked in the pillory: head and both hands through the board (pose key pillory=True or "
                                    "dict(top=y, x=x, post=bool); anchors pillory_top / pillory_neck / pillory_wrist_l / _r)")
    S["baker2_pillory_flinch"] = ("baker2", dict(yaw=-0.15, pitch=0.10, expr="shouting", head_roll=10, fx=["sweat"],
                                                 arm_r=dict(hand=(0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, PILLORY_WRIST_Y), bend=-0.6, stretch=1.3),
                                                 legs="narrow", pillory=True))
    M["baker2_pillory_flinch"] = dict(note="flinching as a tomato hits (put tomato_svg(squash=1) on his head/board)")
    S["baker2_sad"] = ("baker2", dict(yaw=0.30, pitch=0.80, expr="sad", head_roll=6, arm_r="down", arm_l="down", legs="narrow", lean=4))
    S["baker2_swear"] = ("baker2", dict(yaw=0.40, pitch=-0.20, expr="worried", mouth="talk_b", head_roll=-6, fx=["sweat"],
                                        arm_r=dict(hand=(0.74, -0.24), shape="open", bend=-0.9, stretch=1.3), arm_l=dict(hand=(-0.06, 0.62), bend=0.7)))
    M["baker2_swear"] = dict(note="'my bread was exact!' -- swearing, open hand raised")
    # the second hand of the pour lifts the basket's bottom (anchor basket_base)
    c, p = S["inspector_pour"]
    an = figure(c, p, "q")["anchors"]
    hx, hy = an["basket_base"]
    p["arm_l"] = dict(hand=(hx + 0.02, hy + 0.03), bend=0.5, stretch=1.3, shape="open")
    # cycle poses (one frame each; animate with cycle(cast, frame / N, mode, facing, base))
    S["kit_run"] = ("kit", cycle("kit", 0.30, "run", base=dict(expr="worried", fx=["sweat"])))
    S["kit_sneak"] = ("kit", cycle("kit", 0.30, "sneak", base=dict(expr="smirk", gaze=(-0.8, 0.0)), arms="l") )
    S["kit_sneak"][1].update(arm_r=dict(hand=(0.55, 0.35), bend=-0.5, stretch=1.3), prop_r="loaf")
    S["henry_walk"] = ("henry", cycle("henry", 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    S["inspector_walk"] = ("inspector", cycle("inspector", 0.30, "walk", base=dict(expr="neutral", hood=1.0)))
    S["inspector_royal_walk"] = ("inspector_royal", cycle("inspector_royal", 0.30, "walk", base=dict(expr="determined", pitch=-0.3)))
    S["guard_march"] = ("guard1", cycle("guard1", 0.30, "march", base=dict(expr="determined", prop_r=SPEAR), arms="l"))
    S["guard_march"][1]["arm_r"] = dict(hand=(0.42, 0.60), bend=0.4)
    S["guard_march_guard2"] = ("guard2", cycle("guard2", 0.30, "march", base=dict(expr="determined", prop_r=SPEAR), arms="l"))
    S["guard_march_guard2"][1]["arm_r"] = dict(hand=(0.42, 0.60), bend=0.4)
    S["town_walk"] = ("woman1", cycle("woman1", 0.30, "walk", base=dict(expr="happy")))
    S["town_walk_man1"] = ("man1", cycle("man1", 0.30, "walk", base=dict(expr="smirk")))
    for n in ("kit_run", "kit_sneak", "henry_walk", "inspector_walk", "inspector_royal_walk", "guard_march", "town_walk"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast6.cycle(); animate: cycle(cast, frame / N, mode, facing, base, arms) with "
                                  "N = 28 walk / 16 run / 32 sneak / 24 march"))
    return S, M


STORY6, STORY6_META = {}, {}
CYCLE_MODES = ("walk", "run", "sneak", "march")


# ============================================================================= registration
def register():
    if getattr(P, "_cast6_registered", False):
        CE.register_stage()
        if not STORY6:
            s, m = _story()
            STORY6.update(s)
            STORY6_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_hand", "_face_layout", "_hair", "figure"):
        _O6[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._hand = _hand
    P._face_layout = _face_layout
    P._hair = _hair
    P.figure = figure
    CE.COSTUMES.update(COSTUMES6)
    CE.HATS.update(HATS6)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS6 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP6)
    for n, c in NEW_CAST6.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS6)
    P._cast6_registered = True
    s, m = _story()
    STORY6.update(s)
    STORY6_META.update(m)
    P.STORY.update(STORY6)
    CE.register_stage()


register()
