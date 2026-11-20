#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast8.py -- the cast of film 8 ("the ice madman": ice in the desert, a Persian yakhchal, ~1600s) for the v2 puppet,
as an extension module on top of cast7.

    import sys; sys.path.insert(0, ".../v3/cast8"); import cast8      # registers on import (idempotent); imports cast7 .. cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast8.STORY8["farid_pour"]
    f = puppet.figure(cast, pose, "f")                                # pouring the bucket into the channel
    w = puppet.figure("farid", cast8.cycle("farid", 0.25, "run"), "f")   # one frame of the run

Nothing in v2/puppet or v3/cast..cast7 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  robe8 (Persian qaba tunic / long dress: wrap front with trim, sash or jewelled belt, open brocade coat)
    cast_ext.HATS      turban8 (wrapped turban; jewel, aigrette plume, red kulah baton, hanging tail), scarf8 (head scarf)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast7's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (pour, pour_side, pour_len, bucket_water, jar_hold, heat, cry)
    _face       long beard (CAST beard8), double chin (CAST chins), heat flush + shimmer (pose heat), tear streams (pose cry)
    _hand       rings on both hands (CAST rings)
    _prop       bucket (wooden water bucket; REPLACES cast_ext's sand pail while cast8 is loaded; pours), ice_saw, ice_pick,
                ice_block, mud_brick, coin_purse, coin, water_jar, fan
    figure      the anchors of the two-handed pieces and of the pour (grip_far_*, piece_centre_*, pour_lip_*, pour_end_*)
New cast: farid, merchant, woman, oldman, boy.
STORY8 / STORY8_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: bucket_svg, ice_block_svg, ice_stack_svg, mud_brick_svg, coin_purse_svg, coin_svg, water_jar_svg, ice_saw_svg,
fan_svg.

Command line (QA):  python3 test_cast8.py        lineup.jpg (every member, every pose, cycles, mouths, props), canvas + robustness
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast7")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast7 as C7      # noqa: E402  (v3/cast7, read-only; imports cast6 .. cast_ext and v2/puppet)
import cast6 as C6      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW8 = ("farid", "merchant", "woman", "oldman", "boy")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_O8 = {}
# pose keys of the figure being drawn (set by the _norm wrapper; figure() calls _norm before drawing anything)
_POSE8 = {"pour": 0.0, "pside": 0.0, "plen": 1.0, "water": 1.0, "jar": "shoulder", "heat": 0.0, "cry": 0.0, "t": 0.0,
          "an": {}, "sides": [], "prop_i": 0, "hand_i": 0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
ICE = dict(light="#f4fbff", base="#cfeaf8", mid="#a8d6f0", dark="#6fa9d2", deep="#4a86b8", crack="#ffffff")
WATER = dict(light="#e4f6ff", base="#8ccbea", dark="#3f8fc0")
WOOD8 = dict(light="#c89a62", base="#9a6a3a", dark="#5e3e20", hoop="#4a4650", hoop_l="#8a8692")
MUD = dict(light="#d8ae7c", base="#b8875a", dark="#8a5e3a", deep="#6a4428", straw="#ecd29a")
CLAY = dict(light="#e89a62", base="#c86a3a", dark="#8a3e1e", paint="#f2e2c0", paint2="#2a4a7a")
LEATHER = dict(light="#b07a48", base="#8a5630", dark="#5a3418", cord="#d8b04a")
GOLD8 = dict(light="#fff0a8", base="#e2b23a", dark="#9a6e18", deep="#6a4a10")
STEEL8 = dict(light="#e6eaf0", base="#a8b0bc", dark="#5e6674")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _lin(k, name, c0, c1, c2, x0, y0, x1, y1, op=1.0):
    gid = "%s_%s" % (k.uid, name)
    k.defs.append('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%.4f" y1="%.4f" x2="%.4f" y2="%.4f"><stop offset="0" stop-color="%s" stop-opacity="%.3f"/>'
                  '<stop offset="0.45" stop-color="%s" stop-opacity="%.3f"/><stop offset="1" stop-color="%s" stop-opacity="%.3f"/></linearGradient>'
                  % (gid, x0, y0, x1, y1, k.c(c0), op, k.c(c1), op, k.c(c2), op))
    return "url(#%s)" % gid


def _T(H, th, sc):
    """local -> figure: rotate by th degrees, scale sc, translate to H."""
    def f(x, y):
        rx, ry = _rot(x * sc, y * sc, th)
        return (H[0] + rx, H[1] + ry)
    return f


# ============================================================================= pieces (drawn in their own local frame)
BUCKET_RIM = 0.20          # the bail top is in the hand; the rim (and the ears the bail pivots on) 0.20 D below it
BUCKET_H = 0.27            # rim to bottom
BUCKET_RT, BUCKET_RB = 0.175, 0.145


def _bucket_body(k, water=1.0):
    """the wooden bucket in its own frame: rim centre (the pivot) at (0, 0), mouth up, bottom at y = BUCKET_H.  Staves,
    two iron hoops, the rim ellipse with the water surface inside."""
    rt, rb, h = BUCKET_RT, BUCKET_RB, BUCKET_H
    g = _lin(k, "bkw", WOOD8["light"], WOOD8["base"], WOOD8["dark"], -rt, 0, rt, 0)
    o = ['<path d="M%.4f,0 L%.4f,%.4f Q0,%.4f %.4f,%.4f L%.4f,0 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
         % (-rt, -rb, h, h + 0.035, rb, h, rt, g, k.ink)]
    st = "".join("M%.4f,%.4f L%.4f,%.4f " % (x * rt, 0.03, x * rb, h - 0.01) for x in (-0.62, -0.25, 0.12, 0.48))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (st, k.c(WOOD8["dark"])))
    for yy in (0.055, h - 0.055):
        w = rt + (rb - rt) * yy / h
        o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="butt"/>' % (-w, yy, yy + 0.03, w, yy, k.ink))
        o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="butt"/>' % (-w, yy, yy + 0.03, w, yy, k.c(WOOD8["hoop"])))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.006" opacity="0.8"/>'
                 % (-w * 0.8, yy - 0.004, -w * 0.4, yy + 0.008, -w * 0.05, yy + 0.012, k.c(WOOD8["hoop_l"])))
    o.append('<ellipse cx="0" cy="0" rx="%.4f" ry="0.040" fill="%s" stroke="%s" stroke-width="0.018"/>' % (rt, k.c(WOOD8["dark"]), k.ink))
    if water > 0.02:
        o.append('<ellipse cx="0" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (0.006 + 0.012 * (1 - water), rt * 0.86, 0.028, k.c(WATER["base"])))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>'
                 % (-rt * 0.55, 0.0, -rt * 0.2, -0.014, rt * 0.15, -0.006, k.c(WATER["light"])))
    for x in (-rt, rt):
        o.append('<circle cx="%.4f" cy="0" r="0.016" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, k.c(WOOD8["hoop"]), k.ink))
    return "".join(o)


def _stream(k, P0, P1, P2, w, op=0.85):
    """falling water: a quadratic ribbon P0 -> P2 (control P1), lighter core, a few drops round the end."""
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (P0 + P1 + P2)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="%.3f"/>' % (d, k.c(WATER["dark"]), w + 0.016, op * 0.55)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="%.3f"/>' % (d, k.c(WATER["base"]), w, op))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="%.3f" transform="translate(%.4f 0)"/>'
             % (d, k.c(WATER["light"]), max(0.006, w * 0.28), op, -w * 0.18))
    for i, (dx, dy, r) in enumerate(((-0.07, -0.05, 0.020), (0.08, -0.10, 0.016), (-0.03, 0.04, 0.014), (0.05, 0.02, 0.018))):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.006" opacity="%.3f"/>'
                 % (P2[0] + dx, P2[1] + dy, r * max(0.4, w / 0.06), k.c(WATER["base"]), k.c(WATER["dark"]), op))
    for p in (P0, P1, P2):
        k.ext.append((p[0], p[1], w / 2 + 0.03))
    k.ext.append((P2[0] - 0.09, P2[1] - 0.10, 0.03))
    k.ext.append((P2[0] + 0.10, P2[1] - 0.12, 0.03))
    return "".join(o)


def _ice_body(k, w, h, dep=0.10, melt=0.0, uid="ib"):
    """a translucent block of ice centred on (0, 0): front face w x h, the top face as a parallelogram rising to the upper right
    (depth dep), a right side face; frosted top, cloudy core, cracks, air bubbles, glints.  melt 0..1: rounded edges + drips."""
    u = "%s_%s%d" % (k.uid, uid, int(1000 * w))
    x0, y0, x1, y1 = -w / 2, -h / 2 + dep * 0.5, w / 2 - dep * 0.6, h / 2
    ox, oy = dep * 0.6, -dep
    r = 0.012 + 0.05 * melt
    k.defs.append('<linearGradient id="%s_f" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="%s" stop-opacity="0.92"/>'
                  '<stop offset="0.55" stop-color="%s" stop-opacity="0.80"/><stop offset="1" stop-color="%s" stop-opacity="0.88"/></linearGradient>'
                  % (u, k.c(ICE["base"]), k.c(ICE["mid"]), k.c(ICE["dark"])))
    k.defs.append('<radialGradient id="%s_c" cx="0.45" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffffff" stop-opacity="0.75"/>'
                  '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>' % u)
    o = []
    # side face (right) and top face
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" fill-opacity="0.85" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x1, y0, x1 + ox, y0 + oy, x1 + ox, y1 + oy, x1, y1, k.c(ICE["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" fill-opacity="0.95" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x0, y0, x0 + ox, y0 + oy, x1 + ox, y0 + oy, x1, y0, k.c(ICE["light"]), k.ink))
    # front face
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="%.4f" fill="url(#%s_f)" stroke="%s" stroke-width="0.020"/>'
             % (x0, y0, x1 - x0, y1 - y0, r, u, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="url(#%s_c)"/>' % ((x0 + x1) / 2 - 0.02, (y0 + y1) / 2 + 0.01, (x1 - x0) * 0.36, (y1 - y0) * 0.34, u))
    # cracks (white) with a blue shadow line
    fw, fh = x1 - x0, y1 - y0
    cr = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" % (
        x0 + fw * 0.18, y0 + fh * 0.10, x0 + fw * 0.34, y0 + fh * 0.42, x0 + fw * 0.30, y0 + fh * 0.60, x0 + fw * 0.46, y0 + fh * 0.88,
        x0 + fw * 0.34, y0 + fh * 0.42, x0 + fw * 0.52, y0 + fh * 0.36)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" stroke-linejoin="round" opacity="0.7" transform="translate(0.006 0.006)"/>'
             % (cr, k.c(ICE["deep"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>' % (cr, k.c(ICE["crack"])))
    # bubbles
    for (a, b, rr) in ((0.68, 0.30, 0.016), (0.74, 0.44, 0.010), (0.62, 0.62, 0.012), (0.80, 0.70, 0.008), (0.20, 0.74, 0.010)):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" fill-opacity="0.55" stroke="%s" stroke-width="0.004" stroke-opacity="0.6"/>'
                 % (x0 + fw * a, y0 + fh * b, rr, k.c(ICE["deep"])))
    # glints: a diagonal shine on the front face and the bright top edge
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="#ffffff" opacity="0.40"/>'
             % (x0 + fw * 0.06, y1 - fh * 0.10, x0 + fw * 0.16, y1 - fh * 0.10, x0 + fw * 0.40, y0 + fh * 0.08, x0 + fw * 0.30, y0 + fh * 0.08))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.9"/>' % (x0 + 0.03, y0 + 0.012, x1 - 0.04, y0 + 0.012))
    # frost speckle on the top face
    for i in range(6):
        a = 0.1 + 0.15 * i
        o.append('<circle cx="%.4f" cy="%.4f" r="0.007" fill="#ffffff" opacity="0.9"/>' % (x0 + ox * (0.3 + 0.4 * (i % 2)) + (x1 - x0) * a, y0 + oy * (0.3 + 0.4 * (i % 2))))
    if melt > 0.02:
        for (a, ln) in ((0.25, 0.06), (0.55, 0.10), (0.82, 0.05)):
            x = x0 + fw * a
            L = ln * melt
            o.append('<path d="M%.4f,%.4f q-0.018,%.4f 0,%.4f q0.018,%.4f 0,%.4f Z" fill="%s" fill-opacity="0.85" stroke="%s" stroke-width="0.006"/>'
                     % (x, y1 - 0.01, L * 0.7, L + 0.02, -L * 0.3, -L - 0.02, k.c(ICE["mid"]), k.c(ICE["deep"])))
        k.ext.append((0.0, y1 + 0.12 * melt, 0.02))
    return "".join(o), (x0, y0 + oy, x1 + ox, y1)


def _brick_body(k, w, h, dep=0.07):
    """a sun-dried mud brick centred on (0, 0): front face, top face, right side; rough edge, straw flecks, a thumb mark."""
    x0, y0, x1, y1 = -w / 2, -h / 2 + dep * 0.5, w / 2 - dep * 0.6, h / 2
    ox, oy = dep * 0.6, -dep
    o = []
    rough = lambda pts: P._smooth_closed(pts)  # noqa: E731
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x1, y0, x1 + ox, y0 + oy, x1 + ox, y1 + oy, x1, y1, k.c(MUD["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x0, y0, x0 + ox, y0 + oy, x1 + ox, y0 + oy, x1, y0, k.c(MUD["light"]), k.ink))
    g = _lin(k, "mb%d" % int(1000 * w), MUD["light"], MUD["base"], MUD["dark"], x0, y0, x1, y1)
    fr = rough([(x0, y0), ((x0 + x1) / 2, y0 - 0.006), (x1, y0), (x1 + 0.004, (y0 + y1) / 2), (x1, y1), ((x0 + x1) / 2, y1 + 0.006), (x0, y1), (x0 - 0.005, (y0 + y1) / 2)])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (fr, g, k.ink))
    fl = []
    for i, (a, b, ang) in enumerate(((0.15, 0.3, 20), (0.35, 0.65, -30), (0.55, 0.35, 60), (0.75, 0.7, 10), (0.88, 0.4, -50), (0.25, 0.8, 75))):
        x, y = x0 + (x1 - x0) * a, y0 + (y1 - y0) * b
        dx, dy = 0.028 * math.cos(math.radians(ang)), 0.028 * math.sin(math.radians(ang))
        fl.append("M%.4f,%.4f L%.4f,%.4f" % (x - dx, y - dy, x + dx, y + dy))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.85"/>' % (" ".join(fl), k.c(MUD["straw"])))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.030" ry="0.018" fill="%s" opacity="0.5"/>' % (x0 + (x1 - x0) * 0.62, (y0 + y1) / 2, k.c(MUD["deep"])))
    return "".join(o), (x0, y0 + oy, x1 + ox, y1)


def _purse_body(k, coins=True):
    """leather drawstring purse hanging from the gathered neck at (0, 0): frill above, cord bow, bulging pouch to y 0.30,
    gold coins peeking out of the neck, a tassel."""
    g = _lin(k, "pu", LEATHER["light"], LEATHER["base"], LEATHER["dark"], -0.15, 0, 0.15, 0)
    o = []
    if coins:
        for (x, y) in ((-0.035, -0.035), (0.03, -0.045)):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.022" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, y, k.c(GOLD8["base"]), k.ink))
    o.append('<path d="M-0.070,-0.020 L-0.090,-0.075 L-0.040,-0.050 L0.0,-0.085 L0.040,-0.050 L0.090,-0.075 L0.070,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (k.c(LEATHER["light"]), k.ink))
    body = P._smooth_closed([(-0.06, 0.02), (-0.13, 0.08), (-0.16, 0.18), (-0.12, 0.28), (0.0, 0.31), (0.12, 0.28), (0.16, 0.18), (0.13, 0.08), (0.06, 0.02)])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M-0.10,0.12 Q-0.11,0.22 -0.05,0.27 M0.03,0.10 Q0.05,0.20 0.02,0.28" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(LEATHER["dark"]))
    o.append('<path d="M-0.08,0.11 Q-0.10,0.17 -0.07,0.22" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.35"/>')
    # cord and bow at the neck, tassel
    o.append('<path d="M-0.075,0.015 Q0,0.040 0.075,0.015" fill="none" stroke="%s" stroke-width="0.026"/>' % k.ink)
    o.append('<path d="M-0.075,0.015 Q0,0.040 0.075,0.015" fill="none" stroke="%s" stroke-width="0.014"/>' % k.c(LEATHER["cord"]))
    o.append('<path d="M0.05,0.03 q0.03,0.05 0.0,0.10 M0.05,0.03 q0.06,0.03 0.05,0.09" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c(LEATHER["cord"]))
    o.append('<circle cx="0.05" cy="0.135" r="0.016" fill="%s" stroke="%s" stroke-width="0.007"/>' % (k.c("#b8302a"), k.ink))
    return "".join(o)


def _coin_body(k, r=0.045):
    o = ['<circle cx="0" cy="0" r="%.4f" fill="%s" stroke="%s" stroke-width="0.010"/>' % (r, k.c(GOLD8["base"]), k.ink)]
    o.append('<circle cx="0" cy="0" r="%.4f" fill="none" stroke="%s" stroke-width="0.006"/>' % (r * 0.7, k.c(GOLD8["dark"])))
    o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>'
             % (-r * 0.5, -r * 0.3, r * 0.2, -r * 0.4, r * 0.6, -r * 0.4, k.c(GOLD8["light"])))
    return "".join(o)


JAR_H = 0.62
JAR_W = 0.22               # half width at the shoulder


def _jar_body(k):
    """a terracotta water jar centred on (0, 0): mouth with a lip at y -0.31, neck, wide shoulder (+-0.22 at y -0.02),
    tapering body to a small foot at y 0.31, two loop handles neck -> shoulder, a painted cream zigzag band, a wet sheen."""
    g = _lin(k, "jr", CLAY["light"], CLAY["base"], CLAY["dark"], -JAR_W, 0, JAR_W, 0)
    o = []
    for s in (-1, 1):       # handles behind the body edge
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (s * 0.065, -0.24, s * 0.20, -0.25, s * 0.17, -0.10)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (d, k.c(CLAY["base"])))
    body = P._smooth_closed([(-0.060, -0.29), (-0.065, -0.20), (-0.17, -0.12), (-0.22, -0.02), (-0.20, 0.12), (-0.13, 0.24), (-0.075, 0.31),
                             (0.075, 0.31), (0.13, 0.24), (0.20, 0.12), (0.22, -0.02), (0.17, -0.12), (0.065, -0.20), (0.060, -0.29)])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M-0.205,-0.045 Q0,0.000 0.205,-0.045" fill="none" stroke="%s" stroke-width="0.034"/>' % k.c(CLAY["paint"]))
    zz = "M-0.19,-0.004 " + " ".join("L%.4f,%.4f" % (-0.19 + 0.038 * i, (0.03 if i % 2 else -0.004) + 0.012 * (1 - abs(-0.19 + 0.038 * i) / 0.2)) for i in range(1, 11))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (zz, k.c(CLAY["paint2"])))
    o.append('<path d="M-0.15,0.05 Q-0.17,0.14 -0.11,0.22" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.30"/>')
    # lip + dark mouth with a water glint
    o.append('<ellipse cx="0" cy="-0.300" rx="0.085" ry="0.026" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(CLAY["light"]), k.ink))
    o.append('<ellipse cx="0" cy="-0.302" rx="0.055" ry="0.014" fill="%s"/>' % k.c("#2a1a14"))
    o.append('<path d="M-0.025,-0.304 L0.020,-0.306" stroke="%s" stroke-width="0.006" stroke-linecap="round"/>' % k.c(WATER["base"]))
    return "".join(o)


SAW_LEN = 0.95


def _saw_body(k):
    """ice saw along +x: wooden handle in the fist (x -0.07 .. 0.13), a long steel blade to x 0.95 with coarse teeth on the
    lower edge (+y), a rivet pair."""
    g = _lin(k, "sw", STEEL8["light"], STEEL8["base"], STEEL8["dark"], 0, -0.04, 0, 0.07)
    o = []
    blade = "M0.10,-0.040 L%.4f,-0.034 L%.4f,0.020 L0.10,0.070 Z" % (SAW_LEN, SAW_LEN - 0.01)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (blade, g, k.ink))
    n = 16
    tt = []
    for i in range(n):
        xa = 0.12 + (SAW_LEN - 0.14) * i / n
        xb = 0.12 + (SAW_LEN - 0.14) * (i + 1) / n
        ya = 0.068 - 0.048 * (i / float(n))
        tt.append("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" % (xa, ya - 0.004, (xa + xb) / 2 + 0.008, ya + 0.026, xb, ya - 0.004 - 0.003))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (" ".join(tt), k.c(STEEL8["base"]), k.ink))
    o.append('<path d="M0.16,-0.022 L%.4f,-0.020" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (SAW_LEN - 0.05))
    o.append('<path d="M-0.075,-0.045 L0.135,-0.050 Q0.155,0.0 0.135,0.075 L-0.075,0.065 Q-0.095,0.010 -0.075,-0.045 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (k.c(WOOD8["base"]), k.ink))
    o.append('<path d="M-0.05,-0.025 L0.11,-0.030" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD8["light"]))
    for x in (0.115, 0.115):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.011" fill="%s" stroke="%s" stroke-width="0.006"/>' % (x, 0.0, k.c(STEEL8["light"]), k.ink))
    return "".join(o)


PICK_LEN = 0.52


def _pick_body(k):
    """ice pick along +x: wooden haft to x 0.52, an iron head across its end with a long spike toward +y and a short butt."""
    o = ['<path d="M-0.06,-0.026 L%.4f,-0.022 L%.4f,0.022 L-0.06,0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
         % (PICK_LEN, PICK_LEN, k.c(WOOD8["base"]), k.ink)]
    o.append('<path d="M-0.03,-0.010 L%.4f,-0.008" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (PICK_LEN - 0.04, k.c(WOOD8["light"])))
    hx = PICK_LEN - 0.02
    o.append('<path d="M%.4f,-0.10 L%.4f,-0.10 L%.4f,0.06 L%.4f,0.24 L%.4f,0.06 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (hx - 0.035, hx + 0.035, hx + 0.035, hx, hx - 0.035, k.c(STEEL8["base"]), k.ink))
    o.append('<path d="M%.4f,-0.08 L%.4f,0.14" stroke="#ffffff" stroke-width="0.008" opacity="0.7"/>' % (hx - 0.012, hx - 0.004))
    return "".join(o)


def _fan_body(k):
    """woven palm-leaf hand fan along +x: handle to x 0.20, the round leaf (0.34 x 0.30) beyond it, a red border."""
    o = ['<path d="M-0.04,0 L0.21,0" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.04,0 L0.21,0" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(WOOD8["light"]))
    leaf = P._smooth_closed([(0.19, 0.0), (0.24, -0.13), (0.37, -0.17), (0.50, -0.10), (0.53, 0.0), (0.50, 0.10), (0.37, 0.17), (0.24, 0.13)])
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (leaf, k.c("#e8cf8a"), k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (leaf, k.c("#b8302a")))
    wv = "".join("M0.21,0 L%.4f,%.4f " % (0.36 + 0.15 * math.cos(math.radians(a)), 0.15 * math.sin(math.radians(a))) for a in range(-75, 90, 25))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (wv, k.c("#a8843a")))
    o.append('<circle cx="0.36" cy="0" r="0.045" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#2e7a5a"), k.ink))
    return "".join(o)


# ============================================================================= props held in the hand
NEW_PROPS8 = ("bucket", "ice_saw", "ice_pick", "ice_block", "mud_brick", "coin_purse", "coin", "water_jar", "fan")
ICE_W, ICE_H = 0.62, 0.44              # the carried ice block (front face + top), D
BRICK_W, BRICK_H = 0.44, 0.17
NEW_TIP8 = {"bucket": BUCKET_RIM + BUCKET_H, "ice_saw": SAW_LEN, "ice_pick": PICK_LEN, "ice_block": ICE_W / 2, "mud_brick": BRICK_W / 2,
            "coin_purse": 0.18, "coin": 0.07, "water_jar": 0.0, "fan": 0.36}
JAR_HOLDS = ("shoulder", "hang", "hip")


def _side_key():
    i = _POSE8["prop_i"]
    _POSE8["prop_i"] = i + 1
    s = _POSE8["sides"]
    return s[i] if i < len(s) else "r"


def _flat8(k, kind, H, sc):
    """ice_block / mud_brick: held like cast7's panels (cast7 pose keys panel_grip side / bottom / top, panel_side)."""
    side = -1.0 if H[0] > 0.02 else 1.0
    if C7._POSE7["pside"]:
        side = C7._POSE7["pside"]
    if kind == "ice_block":
        w, h = ICE_W, ICE_H
        body, bb = _ice_body(k, ICE_W, ICE_H)
    else:
        w, h = BRICK_W, BRICK_H
        body, bb = _brick_body(k, BRICK_W, BRICK_H)
    w, h = w * sc, h * sc
    grip = C7._POSE7["grip"]
    inset = 0.03 * sc
    if grip == "bottom":
        cx, cy = H[0] + side * (w / 2 - 0.07 * sc), H[1] - h / 2 + inset
        far = (H[0] + side * (w - 0.14 * sc), H[1])
    elif grip == "top":
        cx, cy = H[0] + side * (w / 2 - 0.07 * sc), H[1] + h / 2 - inset
        far = (H[0] + side * (w - 0.14 * sc), H[1])
    else:
        cx, cy = H[0] + side * (w / 2 - inset), H[1]
        far = (H[0] + side * (w - 2 * inset), H[1])
    tr = 'translate(%.4f %.4f) scale(%.4f)' % (cx, cy, sc)
    if side < 0:
        tr += ' scale(-1 1)'          # the side / top faces always lead away from the hand that holds it
    for (x, y) in ((bb[0], bb[1]), (bb[2], bb[1]), (bb[0], bb[3]), (bb[2], bb[3])):
        k.ext.append((cx + x * sc * side, cy + y * sc, 0.03))
    return '<g transform="%s">%s</g>' % (tr, body), (cx, cy), far


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS8:
        _side_key()
        return _O8["_prop"](k, kind, H, ang, sc)
    key = _side_key()
    an = _POSE8["an"]
    if kind == "bucket":
        side = _POSE8["pside"] or (1.0 if H[0] >= 0 else -1.0)
        pour = _POSE8["pour"]
        th = 105.0 * pour * side
        piv = (H[0], H[1] + BUCKET_RIM * sc)
        Tb = _T(piv, th, sc)
        ears = (Tb(-BUCKET_RT, 0.0), Tb(BUCKET_RT, 0.0))
        bail = []
        for e in ears:
            c = (e[0] * 0.85 + H[0] * 0.15, H[1] * 0.75 + e[1] * 0.25 - 0.02 * sc)
            bail.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (H + c + e))
        d = " ".join(bail)
        o = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, k.ink, 0.030 * sc)]
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, k.c("#c8a46a"), 0.014 * sc))
        o.append('<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (piv[0], piv[1], th, sc, _bucket_body(k, _POSE8["water"])))
        for (x, y) in ((-BUCKET_RT, -0.04), (BUCKET_RT, -0.04), (-BUCKET_RB, BUCKET_H + 0.04), (BUCKET_RB, BUCKET_H + 0.04)):
            q = Tb(x, y)
            k.ext.append((q[0], q[1], 0.03))
        k.ext.append((H[0], H[1] - 0.03, 0.02))
        base = Tb(0.0, BUCKET_H)
        an["grip_far_" + key] = base
        an["bucket_base_" + key] = base
        tip = base
        flow = _smooth(0.35, 0.75, pour) * _POSE8["water"]
        if flow > 0.01:
            lip = Tb(BUCKET_RT * side, 0.0)
            nx, ny = _rot(0.0, -1.0, th)
            L = _POSE8["plen"] * (0.25 + 0.75 * flow)
            P1 = (lip[0] + nx * 0.16 * sc, lip[1] + ny * 0.16 * sc)
            P2 = (lip[0] + side * 0.26 * sc, lip[1] + L)
            o.insert(0, _stream(k, lip, P1, P2, 0.075 * sc * (0.4 + 0.6 * flow)))
            an["pour_lip_" + key] = lip
            an["pour_end_" + key] = P2
            tip = lip
        return "".join(o), tip
    if kind in ("ice_block", "mud_brick"):
        svg, tip, far = _flat8(k, kind, H, sc)
        an["grip_far_" + key] = far
        an["piece_centre_" + key] = tip
        return svg, tip
    if kind in ("ice_saw", "ice_pick", "fan"):
        body = {"ice_saw": _saw_body, "ice_pick": _pick_body, "fan": _fan_body}[kind](k)
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
        if kind == "ice_saw":
            pts, tl = ((-0.10, 0.0), (0.13, -0.06), (0.13, 0.08), (SAW_LEN, -0.04), (SAW_LEN, 0.05)), SAW_LEN
        elif kind == "ice_pick":
            pts, tl = ((-0.07, 0.0), (PICK_LEN + 0.02, -0.11), (PICK_LEN - 0.02, 0.25)), None
        else:
            pts, tl = ((-0.05, 0.0), (0.37, -0.19), (0.37, 0.19), (0.55, 0.0)), 0.36
        for e in pts:
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        if kind == "ice_pick":
            tx, ty = _rot((PICK_LEN - 0.02) * sc, 0.24 * sc, ang)
        else:
            tx, ty = _rot(tl * sc, 0.0, ang)
        if kind == "ice_saw":
            mx, my = _rot(0.55 * sc, 0.06 * sc, ang)
            an["saw_mid_" + key] = (H[0] + mx, H[1] + my)
        return o, (H[0] + tx, H[1] + ty)
    if kind == "coin_purse":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _purse_body(k))
        for e in ((-0.17, 0.18), (0.17, 0.18), (0.0, 0.32), (-0.09, -0.09), (0.09, -0.09)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.02))
        return o, (H[0], H[1] + 0.18 * sc)
    if kind == "coin":
        dx, dy = _rot(0.07 * sc, 0.0, ang)
        c = (H[0] + dx, H[1] + dy)
        k.ext.append((c[0], c[1], 0.06 * sc))
        return '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (c[0], c[1], sc, _coin_body(k)), c
    # water jar
    side = 1.0 if H[0] >= 0 else -1.0
    hold = _POSE8["jar"]
    if hold == "hang":
        c, tilt = (H[0], H[1] + 0.37 * sc), 0.0
    elif hold == "hip":
        c, tilt = (H[0] + side * 0.10 * sc, H[1] - 0.06 * sc), side * 18.0
    else:
        tilt = side * 14.0
        ox, oy = _rot(0.0, -0.30 * sc, tilt)
        c = (H[0] + ox, H[1] + oy)
    Tj = _T(c, tilt, sc)
    for e in ((-0.23, -0.02), (0.23, -0.02), (-0.09, -0.32), (0.09, -0.32), (-0.08, 0.32), (0.08, 0.32), (-0.20, -0.20), (0.20, -0.20)):
        q = Tj(*e)
        k.ext.append((q[0], q[1], 0.03))
    an["jar_mouth_" + key] = Tj(0.0, -0.30)
    return '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (c[0], c[1], tilt, sc, _jar_body(k)), Tj(0.0, -0.30)


def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    out = _O8["_hand"](k, H, dirv, shape, hr, fold)
    C = CE._CUR[0]
    if not C or not C.get("rings"):
        return out
    i = _POSE8["hand_i"]
    _POSE8["hand_i"] = i + 1
    g = hr / P.HAND_R
    x, y = H
    gem = ("#c8202e", "#2e8a5a")[i % 2]
    out += ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (x - 0.85 * hr, y + 0.10 * hr, x, y + 0.62 * hr, x + 0.85 * hr, y + 0.10 * hr, k.c(GOLD8["base"]), 0.020 * g))
    out += '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.007"/>' % (x + 0.15 * hr, y + 0.50 * hr, 0.026 * g, k.c(gem), k.c(GOLD8["base"]))
    out += '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="0.8"/>' % (x + 0.08 * hr, y + 0.44 * hr, 0.008 * g)
    return out


# ============================================================================= standalone pieces
def bucket_svg(uid="bk", pour=0.0, side=1, water=1.0, pour_len=1.0, ink=P.INK, tint=None):
    """the wooden water bucket alone, bail top at (0, 0) (where the hand holds it).  pour 0..1 tips it toward side (+1 screen-
    right) about the bail ears with the stream falling pour_len (D).  Returns (svg, anchors base, lip, end)."""
    k = _ctx(uid, ink, tint)
    keep = dict(_POSE8)
    _POSE8.update(pour=_clamp(_num(pour, 0.0), 0.0, 1.0), pside=1.0 if side >= 0 else -1.0, water=_clamp(_num(water, 1.0), 0.0, 1.0),
                  plen=_clamp(_num(pour_len, 1.0), 0.2, 3.0), an={}, sides=["r"], prop_i=0)
    s, tip = _prop(k, "bucket", (0.0, 0.0), 0.0, 1.0)
    an = dict(base=_POSE8["an"].get("bucket_base_r"), lip=_POSE8["an"].get("pour_lip_r"), end=_POSE8["an"].get("pour_end_r"))
    _POSE8.clear()
    _POSE8.update(keep)
    return '<g id="%s_bucket"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), an


def ice_block_svg(uid="ib", w=ICE_W, h=ICE_H, melt=0.0, ink=P.INK, tint=None):
    """one translucent ice block centred on (0, 0) (front face w x h, top + side faces).  melt 0..1: rounder, dripping.
    Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    s, bb = _ice_body(k, w, h, melt=_clamp(_num(melt, 0.0), 0.0, 1.0))
    return '<g id="%s_ice"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


def ice_stack_svg(uid="is", cols=3, rows=3, w=ICE_W, h=ICE_H, ink=P.INK, tint=None):
    """blocks stacked like the store inside the dome: rows x cols, bottom row on y = 0, centred on x = 0, each row offset
    by a quarter block.  Returns (svg, top_y)."""
    k = _ctx(uid, ink, tint)
    o = []
    for r in range(int(rows)):
        n = max(1, int(cols) - (r % 2))
        for c in range(n):
            x = (c - (n - 1) / 2.0) * (w - 0.04) + (0.05 if r % 2 else 0.0)
            y = -(r + 0.5) * (h - 0.06)
            k.uid = "%s_%d%d" % (uid, r, c)
            s, _ = _ice_body(k, w, h)
            o.append('<g transform="translate(%.4f %.4f)">%s</g>' % (x, y, s))
    k.uid = str(uid)
    return '<g id="%s_stack"><defs>%s</defs>%s</g>' % (uid, "".join(k.defs), "".join(o)), -rows * (h - 0.06) - 0.1


def mud_brick_svg(uid="mb", w=BRICK_W, h=BRICK_H, ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s, bb = _brick_body(k, w, h)
    return '<g id="%s_brick"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


def coin_purse_svg(uid="cp", coins=True, ink=P.INK, tint=None):
    """the purse hanging from its neck at (0, 0), pouch to y 0.31."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_purse"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _purse_body(k, coins))


def coin_svg(uid="cn", r=0.045, ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    return '<g id="%s_coin">%s</g>' % (k.uid, _coin_body(k, r))


def water_jar_svg(uid="wj", ink=P.INK, tint=None):
    """the clay jar centred on (0, 0), mouth at y -0.31, foot at y 0.31 (0.44 D wide)."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_jar"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _jar_body(k))


def ice_saw_svg(uid="sw", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    return '<g id="%s_saw"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _saw_body(k))


def fan_svg(uid="fn", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    return '<g id="%s_fan"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _fan_body(k))


# ============================================================================= face: long beard, double chin, heat, tears
def _beard8(k, C, L):
    """long beard from the cheeks to a soft point below the chin (old man), strands, the mouth drawn over it."""
    B = C["beard8"]
    mx, my = L["mx"], L["my"]
    ln = B.get("len", 0.55)
    wd = B.get("w", 0.40)
    col, dk = k.c(B["color"]), k.c(B.get("dark", "#b8b0b8"))
    pts = [(mx - wd, my - 0.17), (mx - wd - 0.02, my + 0.02), (mx - wd * 0.80, my + ln * 0.50), (mx - wd * 0.40, my + ln * 0.86), (mx + 0.03, my + ln),
           (mx + wd * 0.42, my + ln * 0.84), (mx + wd * 0.82, my + ln * 0.48), (mx + wd + 0.02, my + 0.02), (mx + wd, my - 0.17),
           (mx + wd * 0.55, my - 0.06), (mx, my - 0.02), (mx - wd * 0.55, my - 0.06)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, col, k.ink)]
    st = []
    for x in (-0.28, -0.16, -0.05, 0.07, 0.19, 0.29):
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (mx + x * wd / 0.40, my + 0.06, mx + x * wd / 0.40 * 0.9, my + ln * 0.5, mx + x * wd / 0.40 * 0.45, my + ln * 0.85))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (" ".join(st), dk))
    # mouth opening in the beard (the face's mouth is drawn over it)
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.10" ry="0.045" fill="%s" opacity="0.35"/>' % (mx, my + 0.01, k.c("#d8c8c8")))
    k.ext.append((mx + 0.03, my + ln, 0.03))
    k.ext.append((mx - wd - 0.02, my + 0.1, 0.02))
    k.ext.append((mx + wd + 0.02, my + 0.1, 0.02))
    return "".join(o)


def _chins(k, L):
    mx, my = L["mx"], L["my"]
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.55"/>'
            % (mx - 0.15, my + 0.17, mx, my + 0.235, mx + 0.15, my + 0.17, k.ink))


def _heat(k, L, lev, t):
    """overheated: red flush on the cheeks + wavy heat shimmer lines rising beside the head."""
    o = []
    for x in (L["xL"] - 0.04, L["xR"] + 0.04):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.085" ry="0.050" fill="%s" opacity="%.3f"/>' % (x, L["ey"] + 0.11, k.c("#e8584a"), 0.45 * lev))
    for i, (x, y0) in enumerate(((-0.70, 0.05), (0.70, 0.0), (-0.82, -0.25), (0.84, -0.30))):
        if i >= 2 and lev < 0.5:
            break
        ph = 2 * math.pi * (t * 1.3 + 0.27 * i)
        pts = []
        for j in range(7):
            y = y0 - 0.06 * j
            pts.append((x + 0.025 * math.sin(ph + j * 1.4), y))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="%.3f"/>'
                 % (P._smooth_open(pts), k.c("#f4a060"), 0.75 * lev))
        k.ext.append((x, y0 + 0.02, 0.04))
        k.ext.append((x, y0 - 0.38, 0.04))
    return "".join(o)


def _cry(k, L, lev, t):
    """laughing to tears: two streams running from the outer eye corners down the cheeks, a drop at each end."""
    o = []
    for s, x in ((-1, L["xL"] - 0.07), (1, L["xR"] + 0.07)):
        y0 = L["ey"] + 0.02
        ln = 0.18 + 0.20 * lev
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x, y0, x + s * 0.06, y0 + ln * 0.5, x + s * 0.03, y0 + ln)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round" opacity="0.9"/>' % (d, k.c(P.SWEAT[2])))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (d, k.c(P.SWEAT[0])))
        dy = (t * 2.0 % 1.0) * 0.10
        o.append(P._fx_sweat(k, x + s * 0.03, y0 + ln + 0.05 + dy, 0.7, 0.0))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O8["_face"](k, C, P_, white)
    if C is None or not C.get("_cast8"):
        return svg, L
    under, over = [], []
    if C.get("beard8"):
        under.append(_beard8(k, C, L))
    if C.get("chins"):
        under.append(_chins(k, L))
    if _POSE8["heat"] > 0.02:
        under.append(_heat(k, L, _POSE8["heat"], _POSE8["t"]))
    if _POSE8["cry"] > 0.02:
        over.append(_cry(k, L, _POSE8["cry"], _POSE8["t"]))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE8["pour"] = _f(g("pour"), 0.0, 0.0, 1.0)
    ps = _num(g("pour_side"), 0.0)
    _POSE8["pside"] = 1.0 if ps > 0.5 else (-1.0 if ps < -0.5 else 0.0)
    _POSE8["plen"] = _f(g("pour_len"), 1.0, 0.2, 3.0)
    _POSE8["water"] = _f(g("bucket_water"), 1.0, 0.0, 1.0)
    jh = g("jar_hold")
    _POSE8["jar"] = jh if jh in JAR_HOLDS else "shoulder"
    _POSE8["heat"] = _f(g("heat"), 0.0, 0.0, 1.0)
    _POSE8["cry"] = _f(g("cry"), 0.0, 0.0, 1.0)
    _POSE8["t"] = _num(g("t"), 0.0)
    if not math.isfinite(_POSE8["t"]):
        _POSE8["t"] = 0.0
    _POSE8["an"] = {}
    _POSE8["prop_i"] = 0
    _POSE8["hand_i"] = 0
    _POSE8["sides"] = [s for s in ("l", "r") if P._prop_spec(g("prop_" + s))]
    return _O8["_norm"](C, pose)


# ============================================================================= costume: the robe (torso-local)
def _cos_robe8(k, C, m):
    """Persian qaba: a tunic / robe wrapped right over left (a trimmed diagonal front edge from the neck to the sash, then
    straight down the skirt), a trimmed round neckline, a wide cloth sash at the waist knotted at the side with hanging ends
    (C["sash_knot"]), or a jewelled gold belt plate (C["jewels"]); C["coat"]: an open brocade coat over it (colors coat,
    coat_trim, coat_dot) with the robe showing between its fronts; C["robe_len"] below the torso, C["robe_flare"]."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * C.get("sash_y", 0.70)
    dark = k.c(col.get("dark", "#8a7a6a"))
    trim = k.c(col.get("trim", "#c8a050"))
    coat = C.get("coat")
    o = []
    # wrap front edge: neck (screen-left) diagonally down to the sash on the right
    edge = [X(-0.12, 0.42), X(0.04, 0.58), X(0.20, yw - 0.04)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.30"/>'
             % (edge[0] + edge[1] + edge[2] + X(0.45, yw - 0.04) + X(0.45, 0.42) + (k.c(P._shade(col["base"], 0.75)),)))
    o.append(_ln(edge, k.ink, 0.056))
    o.append(_ln(edge, trim, 0.034))
    if C.get("trim_dots"):
        for t in (0.15, 0.4, 0.65, 0.9):
            p = (edge[0][0] + (edge[2][0] - edge[0][0]) * t, edge[0][1] + (edge[2][1] - edge[0][1]) * t)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>' % (p[0], p[1], k.c(col.get("trim_d", "#7a2a1a"))))
    # soft fold lines
    fl = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.30, 0.62) + X(-0.26, 0.78) + X(-0.28, yw - 0.06) + X(0.30, 0.70) + X(0.34, 0.80) + X(0.33, yw - 0.06))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>' % (fl, dark))
    if coat:
        cc = coat
        gc = C2._grad(k, "co", cc, -hw, hw)
        if col.get("coat_dot"):
            k.defs.append('<pattern id="%s_cd" width="0.12" height="0.12" patternUnits="userSpaceOnUse"><path d="M0.06,0.02 L0.08,0.06 L0.06,0.10 L0.04,0.06 Z" fill="%s"/>'
                          '<circle cx="0" cy="0" r="0.012" fill="%s"/><circle cx="0.12" cy="0.12" r="0.012" fill="%s"/></pattern>'
                          % (k.uid, k.c(col["coat_dot"]), k.c(col["coat_dot"]), k.c(col["coat_dot"])))
        for s in (-1, 1):
            pan = [X(s * 0.17, 0.38), X(s * 0.95, 0.30), X(s * 0.95, yB + 0.1), X(s * 0.27, yB + 0.1), X(s * 0.22, 0.62)]
            o.append('<path d="%s" fill="%s"/>' % (_poly_d(pan), gc))
            if col.get("coat_dot"):
                o.append('<path d="%s" fill="url(#%s_cd)" opacity="0.75"/>' % (_poly_d(pan), k.uid))
            ed = [X(s * 0.17, 0.38), X(s * 0.22, 0.62), X(s * 0.27, yB + 0.1)]
            o.append(_ln(ed, k.ink, 0.060))
            o.append(_ln(ed, k.c(col.get("coat_trim", "#e2b23a")), 0.036))
    # neckline
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (X(-0.17, 0.40) + X(0, 0.48) + X(0.17, 0.40) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (X(-0.17, 0.40) + X(0, 0.48) + X(0.17, 0.40) + (trim,)))
    inside = "".join(o)
    # ---- over: the skirt of the robe, its front edge, hem band, coat skirts, sash
    yt = yB - 0.16
    hem = yB + C.get("robe_len", 0.40)
    a = hw * 0.985
    b = hw + C.get("robe_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "rb", X, yt, a, hem, b, g, sw=0.026,
                    folds=((-0.14, yt + 0.12, -0.20, hem - 0.05), (0.06, yt + 0.16, 0.05, hem - 0.06), (-0.30, yt + 0.20, -0.42, hem - 0.06)),
                    fold_col=dark)]
    fe = [X(0.20, yt), X(0.21, (yt + hem) / 2), X(0.24, hem + 0.02)]
    ov.append(_ln(fe, k.ink, 0.050))
    ov.append(_ln(fe, trim, 0.030))
    if C.get("hem_band", True):
        hb = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-b + 0.03, hem - 0.045) + X(0.0, hem - 0.012) + X(b - 0.03, hem - 0.045))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" opacity="0.95"/>' % (hb, trim))
    if coat:
        ch = hem + C.get("coat_drop", -0.04)
        cb = b + 0.04
        gc = "url(#%s_co)" % k.uid
        for s in (-1, 1):
            pan = [X(s * 0.27, yt), X(s * a, yt), X(s * (a + (cb - a) * 0.35), yt + (ch - yt) * 0.4), X(s * cb, ch), X(s * ((cb + 0.29) / 2), ch + 0.02), X(s * 0.29, ch)]
            ov.append('<path d="%s" fill="%s"/>' % (P._smooth_open(pan) + " Z", gc))
            if col.get("coat_dot"):
                ov.append('<path d="%s" fill="url(#%s_cd)" opacity="0.75"/>' % (P._smooth_open(pan) + " Z", k.uid))
            ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(pan[1:]), k.ink))
            ed = [X(s * 0.27, yt - 0.02), X(s * 0.28, (yt + ch) / 2), X(s * 0.29, ch)]
            ov.append(_ln(ed, k.ink, 0.060))
            ov.append(_ln(ed, k.c(col.get("coat_trim", "#e2b23a")), 0.036))
            hb = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(s * 0.30, ch - 0.03) + X(s * (cb + 0.29) / 2, ch - 0.01) + X(s * (cb - 0.03), ch - 0.04))
            ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030"/>' % (hb, k.c(col.get("coat_trim", "#e2b23a"))))
        k.ext.append((X(cb, ch)[0], ch + 0.03, 0.03))
        k.ext.append((X(-cb, ch)[0], ch + 0.03, 0.03))
    # sash
    sc = k.c(col.get("sash", "#3a5a8a"))
    sd = k.c(col.get("sash_d", P._shade(col.get("sash", "#3a5a8a"), 0.7)))
    sw = C.get("sash_w", 0.13)
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw * 1.0, yw) + X(0.0, yw + 0.03) + X(hw * 1.0, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.ink, sw + 0.026))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, sc, sw))
    for dy in (-sw * 0.22, sw * 0.22):
        bd = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw * 0.95, yw + dy) + X(0.0, yw + 0.03 + dy) + X(hw * 0.95, yw + dy))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (bd, sd))
    if C.get("sash_stripe"):
        bd = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw * 0.95, yw) + X(0.0, yw + 0.03) + X(hw * 0.95, yw))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" opacity="0.9"/>' % (bd, k.c(C["sash_stripe"])))
    if C.get("jewels"):
        bx, by = X(0.0, yw + 0.03)
        ov.append('<rect x="%.4f" y="%.4f" width="0.20" height="%.4f" rx="0.030" fill="%s" stroke="%s" stroke-width="0.016"/>'
                  % (bx - 0.10, by - sw * 0.62, sw * 1.24, k.c(GOLD8["base"]), k.ink))
        ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.040" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx, by, k.c("#c8202e"), k.c(GOLD8["dark"])))
        ov.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="#ffffff" opacity="0.8"/>' % (bx - 0.014, by - 0.012))
        for s in (-1, 1):
            ov.append('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/>' % (bx + s * 0.070, by, k.c("#2e8a5a"), k.c(GOLD8["dark"])))
            for xx in (0.24, 0.40):
                p = X(s * xx, yw + 0.03 - 0.012 * xx)
                ov.append('<circle cx="%.4f" cy="%.4f" r="0.016" fill="%s" stroke="%s" stroke-width="0.007"/>' % (p[0], p[1], k.c(GOLD8["light"]), k.ink))
    elif C.get("sash_knot", True):
        kx, ky = X(-0.20, yw + 0.02)
        ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.055" fill="%s" stroke="%s" stroke-width="0.014"/>' % (kx, ky, sc, k.ink))
        for (dx, ln, rot) in ((-0.03, 0.30, 8.0), (0.03, 0.24, -6.0)):
            x0 = kx + dx
            e = [(x0 - 0.035, ky + 0.03), (x0 + 0.035, ky + 0.03), (x0 + 0.040 + 0.02 * math.sin(math.radians(rot)), ky + ln), (x0 - 0.040, ky + ln + 0.01)]
            ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (_poly_d(e), sc, k.ink))
            fr = "".join("M%.4f,%.4f l%.4f,0.030 " % (x0 - 0.03 + 0.02 * j, ky + ln + 0.005, 0.004 * (j - 1.5)) for j in range(4))
            ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (fr, sd))
            k.ext.append((x0, ky + ln + 0.04, 0.03))
    return inside, "", "".join(ov)


COSTUMES8 = {"robe8": _cos_robe8}


# ============================================================================= hats (head frame)
def _hat_turban8(k, C, yaw):
    """a wrapped turban: a rounded wound dome over the crown from the brow line, the cloth bands crossing in a chevron over
    the forehead (slides with yaw), lighter ridges; C["turban"] = dict(w, h, jewel, plume, kulah, tail, band)."""
    col = C["hat_colors"]
    T8 = C.get("turban", {})
    tw = T8.get("w", 0.56)
    th = T8.get("h", 0.40)
    dx = -0.03 * yaw
    fx = dx + 0.13 * yaw
    yb = -0.22
    yt = -0.50 - th
    back = -1.0 if yaw >= 0 else 1.0
    g = CE._gradient(k, "ht", col, x0=-tw - 0.05, x1=tw + 0.05, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    ext = [(dx - tw - 0.06, yb - 0.18), (dx + tw + 0.06, yb - 0.18), (dx, yt - 0.02), (fx, yb + 0.07)]
    if T8.get("tail"):
        x0 = dx + back * (tw - 0.10)
        tl = [(x0 - 0.07, yb - 0.10), (x0 + 0.07, yb - 0.12), (x0 + back * 0.10, yb + 0.30), (x0 + back * 0.14, yb + 0.62), (x0 + back * 0.02, yb + 0.66),
              (x0 - back * 0.02, yb + 0.30)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(tl), k.c(col["dark"]), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>'
                 % (x0, yb, x0 + back * 0.08, yb + 0.30, x0 + back * 0.08, yb + 0.60, k.c(col["base"])))
        ext.append((x0 + back * 0.15, yb + 0.67))
    if T8.get("kulah"):
        kx = dx * 0.5 + fx * 0.5
        kc = T8["kulah"]
        kd = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" % (kx - 0.075, yt + 0.10, kx - 0.060, yt - 0.20, kx, yt - 0.26, kx + 0.060, yt - 0.20, kx + 0.075, yt + 0.10)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (kd, k.c(kc), k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.4"/>' % (kx - 0.03, yt - 0.16, kx - 0.035, yt + 0.02))
        ext.append((kx, yt - 0.27))
    pts = [(dx - tw, yb), (dx - tw - 0.055, yb - 0.17), (dx - tw * 0.90, yt + th * 0.48), (dx - tw * 0.55, yt + 0.035), (dx * 0.6 + fx * 0.4, yt),
           (dx + tw * 0.55, yt + 0.035), (dx + tw * 0.90, yt + th * 0.48), (dx + tw + 0.055, yb - 0.17), (dx + tw, yb), (fx + 0.26, yb + 0.030),
           (fx, yb + 0.050), (fx - 0.26, yb + 0.030)]
    d = P._smooth_closed(pts)
    k.defs.append('<clipPath id="%s_tb"><path d="%s"/></clipPath>' % (k.uid, d))
    o.append('<path d="%s" fill="%s"/>' % (d, g))
    # wound bands: chevrons over the forehead, rising toward the crown
    n = int(T8.get("bands", 5))
    bd, bl = [], []
    for i in range(n):
        y = yb - 0.02 - i * (yb - yt - 0.06) / float(n)
        rise = 0.10 + 0.03 * i
        bd.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (dx - tw - 0.1, y - rise, fx - 0.24, y + 0.02, fx, y + 0.07, fx + 0.24, y + 0.02, dx + tw + 0.1, y - rise))
        bl.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (dx - tw - 0.1, y - rise - 0.032, fx - 0.24, y - 0.012, fx, y + 0.038, fx + 0.24, y - 0.012,
                                                                       dx + tw + 0.1, y - rise - 0.032))
    o.append('<g clip-path="url(#%s_tb)"><path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.75"/>'
             '<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (k.uid, " ".join(bd), k.c(col["dark"]), " ".join(bl), k.c(col["shine"])))
    if T8.get("band"):
        y = yb - 0.06
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034"/>'
                 % (dx - tw - 0.1, y - 0.10, fx - 0.24, y + 0.02, fx, y + 0.07, fx + 0.24, y + 0.02, dx + tw + 0.1, y - 0.10, k.c(T8["band"])))
    o.append('</g>')
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, k.ink))
    top = (dx * 0.6 + fx * 0.4, yt)
    if T8.get("plume"):
        jx, jy = fx, yb - 0.20
        pl = [(jx - 0.02, jy - 0.06), (jx - 0.06, jy - 0.30), (jx + 0.02, jy - 0.58), (jx + 0.14, jy - 0.74), (jx + 0.10, jy - 0.52), (jx + 0.06, jy - 0.28),
              (jx + 0.03, jy - 0.06)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (P._smooth_closed(pl), k.c(T8["plume"]), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                 % (jx, jy - 0.06, jx - 0.01, jy - 0.40, jx + 0.12, jy - 0.70, k.c(col["dark"])))
        ext.append((jx + 0.15, jy - 0.76))
        top = (jx + 0.12, jy - 0.74)
    if T8.get("jewel"):
        jx, jy = fx, yb - 0.17
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.080" ry="0.095" fill="%s" stroke="%s" stroke-width="0.016"/>' % (jx, jy, k.c(GOLD8["base"]), k.ink))
        for a in range(0, 360, 45):
            o.append('<circle cx="%.4f" cy="%.4f" r="0.013" fill="#fbf6ee" stroke="%s" stroke-width="0.004"/>'
                     % (jx + 0.072 * math.cos(math.radians(a)), jy + 0.086 * math.sin(math.radians(a)), k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.042" ry="0.052" fill="%s" stroke="%s" stroke-width="0.008"/>' % (jx, jy, k.c(T8["jewel"]), k.c(GOLD8["dark"])))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.013" ry="0.018" fill="#ffffff" opacity="0.85"/>' % (jx - 0.014, jy - 0.018))
        # a pearl drop below
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.006"/><circle cx="%.4f" cy="%.4f" r="0.018" fill="#fbf6ee" stroke="%s" stroke-width="0.006"/>'
                 % (jx, jy + 0.095, jx, jy + 0.13, k.c(GOLD8["dark"]), jx, jy + 0.145, k.ink))
    o.append('</g>')
    for p in ext:
        k.ext.append(_rot(p[0], p[1], C["hat_tilt"]) + (0.02,))
    if T8.get("kulah") and not T8.get("plume"):
        top = (dx * 0.5 + fx * 0.5, yt - 0.26)
    return "".join(o), top


def _hat_scarf8(k, C, yaw):
    """the woman's head scarf: one cloth over the head and the shoulders framing the face (no chin band), a trim along the
    face opening, drape folds, a little dark hair at the parting."""
    col = C["hat_colors"]
    dx = -0.02 * yaw
    fx = 0.10 * yaw
    back = -1.0 if yaw >= 0 else 1.0
    outer = [(-0.58 + dx + (0.08 if back < 0 else 0), 0.66), (-0.62 + dx, 0.12), (-0.57 + dx, -0.30), (-0.30 + dx, -0.60), (dx, -0.65), (0.30 + dx, -0.60),
             (0.57 + dx, -0.30), (0.62 + dx, 0.12), (0.58 + dx - (0.08 if back > 0 else 0), 0.66)]
    inner = [(0.40 + fx, 0.44), (0.43 + fx, 0.05), (0.38 + fx, -0.22), (fx, -0.32), (-0.38 + fx, -0.22), (-0.43 + fx, 0.05), (-0.40 + fx, 0.44)]
    d = P._smooth_open(outer) + " L" + P._smooth_open(inner)[1:] + " Z"
    g = CE._gradient(k, "ht", col, x0=-0.62, x1=0.62, mid=0.32)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="M%.4f,-0.28 Q%.4f,-0.34 %.4f,-0.28 L%.4f,-0.20 Q%.4f,-0.26 %.4f,-0.20 Z" fill="%s"/>'
             % (fx - 0.34, fx, fx + 0.34, fx + 0.30, fx, fx - 0.30, k.c(C["hair"]["color"])))
    o.append('<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034"/>' % (P._smooth_open(inner), k.c(col.get("trim", col["shine"]))))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014"/>' % (P._smooth_open([(x * 1.07, y - 0.01) for (x, y) in inner]), k.ink))
    for sd in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.7"/>'
                 % (dx + sd * 0.50, -0.30, dx + sd * 0.58, 0.10, dx + sd * 0.52, 0.60, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.46, -0.30, dx - 0.38, -0.54, dx - 0.10, -0.62, k.c(col["shine"])))
    o.append('</g>')
    for p in ((dx - 0.64, 0.12), (dx + 0.64, 0.12), (dx, -0.68), (dx, 0.68)):
        k.ext.append(_rot(p[0], p[1], C["hat_tilt"]) + (0.02,))
    return "".join(o), (dx, -0.65)


HATS8 = {"turban8": _hat_turban8, "scarf8": _hat_scarf8}


# ============================================================================= cast
NEW_CAST8 = {
    # Farid: young, slim Persian ice-maker -- off-white wrapped turban with a tail, undyed linen knee-length qaba with a madder
    # trim, indigo sash, rolled sleeves, dark brown trousers, soft leather shoes; bold black brows, no beard
    "farid": dict(
        _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=48.2,
        torso_w=0.70, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.27, 0.49), arm=0.74, hip_x=0.15, leg=1.26, stance=0.07, wide=0.27, limb_w=0.058,
        eye_y=0.040, brow="stroke", brow_th=0.070, mouth="dash", moustache=False, smirk_side=1, cheeks="#e8a088",
        hat="newsboy", hat_style="turban8", hat_tilt=-3.0, ear_pencil=False,
        turban=dict(w=0.54, h=0.34, bands=5),
        hat_colors=dict(light="#fbf6ea", base="#e8dcc4", dark="#b0a286", shine="#ffffff"),
        hair=dict(color="#1e1a1e", front=0.10, grow=0.22),
        costume="robe8", robe_len=0.40, robe_flare=0.10, sash_w=0.12,
        sleeve=dict(color="#e6dcc6", dark="#b8ac92", cuff="#c8573a", len=0.56, w=0.150, roll=True),
        shorts=dict(color="#5a4232", dark="#3a2a20", cuff="#5a4232", len=0.90, w=0.13),
        boots=dict(color="#7a5232", cuff="#7a5232", h=0.06, toe=0.15, soft=True),
        colors=dict(base="#e6dcc6", dark="#a89c82", trim="#c8573a", sash="#2e4a7e", sash_d="#1e3058", pants="#5a4232"),
    ),
    # the rich water merchant: very fat, big white silk turban with a gold band, a ruby jewel, a white aigrette plume and the
    # red kulah baton; huge black handlebar moustache, double chin; saffron silk robe under an open crimson brocade coat with
    # gold trim, a jewelled gold belt; rings on both hands; red slippers
    "merchant": dict(
        _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=77.7,
        torso_w=1.50, torso_h=1.20, profile=C2.PROFILE_ROUND, shift_pow=1.3,
        shoulder=(0.44, 0.44), arm=0.76, hip_x=0.19, leg=1.18, stance=0.06, wide=0.30, limb_w=0.068,
        eye_y=0.000, brow="stroke", brow_th=0.072, mouth="smirk", moustache=True, moustache_style="handlebar", tache_scale=1.45, smirk_side=1,
        cheeks="#ec8070", chins=True, rings=True,
        hat="newsboy", hat_style="turban8", hat_tilt=-2.0, ear_pencil=False,
        turban=dict(w=0.66, h=0.52, jewel="#c8202e", plume="#fbf8f0", kulah="#b8202a", band="#e2b23a", bands=6),
        hat_colors=dict(light="#ffffff", base="#f0ece4", dark="#b8b0a8", shine="#ffffff"),
        hair=dict(color="#1a161a", front=0.06, grow=0.20),
        costume="robe8", robe_len=0.62, robe_flare=0.16, sash_w=0.16, jewels=True, coat="#a8243a", coat_drop=-0.02,
        sleeve=dict(color="#a8243a", dark="#6e1424", cuff="#e2b23a", len=0.84, w=0.200),
        shorts=dict(color="#7a1e2a", dark="#4a1018", cuff="#7a1e2a", len=0.90, w=0.15),
        boots=dict(color="#b8302a", cuff="#b8302a", h=0.06, toe=0.17, soft=True),
        colors=dict(base="#eab84e", dark="#a87a22", trim="#2e7a5a", sash="#2e7a5a", sash_d="#1a4a36", coat_trim="#e2b23a", coat_dot="#e8b84a",
                    pants="#7a1e2a", moustache="#1a161a", moustache_l="#5a5058"),
    ),
    # townsfolk: the woman with the water jar (deep blue scarf, long terracotta dress, ochre sash), the old man (white turban,
    # long white beard, grey robe under a brown cloak), the boy (felt cap, short green tunic, red sash)
    "woman": dict(
        _cast8=True, _cast7=True, _cast6=True, _cast4=True, build="slim", seed=19.4,
        torso_w=0.62, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.23, 0.52), arm=0.72, hip_x=0.13, leg=1.16, stance=0.04, wide=0.22, limb_w=0.054,
        eye_y=0.050, brow="stroke", brow_th=0.040, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f2a0a0", lashes=True,
        hat="newsboy", hat_style="scarf8", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#5a74b4", base="#34508e", dark="#1e3260", shine="#8aa4d8", trim="#e8c060"),
        hair=dict(color="#1e1a1e", front=0.10, grow=0.24),
        costume="robe8", robe_len=1.00, robe_flare=0.30, sash_w=0.09, sash_y=0.66, trim_dots=True,
        sleeve=dict(color="#c0583a", dark="#8a3a22", cuff="#e8c060", len=0.84, w=0.150),
        boots=dict(color="#4a2e22", cuff="#4a2e22", h=0.05, toe=0.11, soft=True),
        colors=dict(base="#c0583a", dark="#8a3a22", trim="#e8c060", trim_d="#34508e", sash="#e0a838", sash_d="#a87420", pants="#8a3a22"),
    ),
    "oldman": dict(
        _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="regular", seed=63.1,
        torso_w=0.80, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.30, 0.47), arm=0.72, hip_x=0.15, leg=1.08, stance=0.06, wide=0.24, limb_w=0.060,
        eye_y=0.000, brow="stroke", brow_th=0.060, mouth="dash", moustache=True, moustache_style="walrus", smirk_side=-1, age_lines=True,
        beard8=dict(color="#f4f0ec", dark="#c4bcc4", len=0.62, w=0.36),
        hat="newsboy", hat_style="turban8", hat_tilt=-2.0, ear_pencil=False,
        turban=dict(w=0.56, h=0.36, bands=5),
        hat_colors=dict(light="#ffffff", base="#efeae2", dark="#b8b0a6", shine="#ffffff"),
        hair=dict(color="#e8e4e8", front=0.08, grow=0.20),
        costume="robe8", robe_len=0.86, robe_flare=0.16, sash_w=0.10, coat="#6a4a32", coat_drop=0.0,
        sleeve=dict(color="#6a4a32", dark="#46301e", cuff="#8a6a4a", len=0.84, w=0.170),
        shorts=dict(color="#5a5058", dark="#3a343a", cuff="#5a5058", len=0.90, w=0.12),
        boots=dict(color="#5a3a24", cuff="#5a3a24", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#b8b4ac", dark="#7a766e", trim="#8a8478", sash="#7a6a4a", sash_d="#54482e", coat_trim="#8a6a4a", pants="#5a5058",
                    moustache="#f4f0ec"),
    ),
    "boy": dict(
        _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="boy", seed=8.3,
        torso_w=0.62, torso_h=0.78, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.80, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a090",
        hat="newsboy", hat_style="skullcap", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(light="#6a7ab8", base="#3e4e8a", dark="#26305a", shine="#8a9ad8", cuff="#c84a2a", stitch="#f0d070"),
        hair=dict(color="#1e1a1e", front=0.09, grow=0.18),
        costume="robe8", robe_len=0.22, robe_flare=0.08, sash_w=0.09, hem_band=False,
        sleeve=dict(color="#5e8a4a", dark="#3e6030", cuff="#e8c060", len=0.60, w=0.140, roll=True),
        shorts=dict(color="#d8ccb0", dark="#a89a7e", cuff="#d8ccb0", len=0.70, w=0.13),
        boots=dict(color="#7a5232", cuff="#7a5232", h=0.06, toe=0.12, soft=True),
        colors=dict(base="#5e8a4a", dark="#3e6030", trim="#e8c060", sash="#c83a2a", sash_d="#8a2418", pants="#d8ccb0"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast8.py canvas): every arm preset
# with every film-8 prop at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects, every STORY8 pose and the
# cycles of the member; >= 0.32 D head room.  CANVAS8_LIE: farid asleep (pose key lie).
CANVAS8 = {
    "farid": (-1.9375, -4.5000, 1.9375, 0.1250),
    "merchant": (-1.6875, -5.0625, 1.6875, 0.1250),
    "woman": (-1.5000, -4.3125, 1.5000, 0.3125),
    "oldman": (-1.5625, -4.3125, 1.5625, 0.1875),
    "boy": (-1.4375, -3.8125, 1.4375, 0.1250),
}
CANVAS8_LIE = {"farid": (-2.2500, -1.5625, 2.2500, 0.25)}


# ============================================================================= figure wrapper: anchors of held pieces
def figure(cast_name, pose=None, uid="p"):
    f = _O8["figure"](cast_name, pose, uid)
    if _POSE8["an"]:
        a = dict(f["anchors"])
        sx, sy = 1.0, 1.0
        sq = pose.get("squash") if isinstance(pose, dict) else None
        if isinstance(sq, (int, float)) and not isinstance(sq, bool):
            sx = sy = float(sq)
        elif isinstance(sq, (tuple, list)) and len(sq) >= 2 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in sq[:2]):
            sx, sy = float(sq[0]), float(sq[1])
        sx = _clamp(_num(sx, 1.0), 0.3, 2.5)
        sy = _clamp(_num(sy, 1.0), 0.3, 2.5)
        mir = isinstance(pose, dict) and bool(pose.get("mirror"))
        for n, v in _POSE8["an"].items():
            if mir:
                n = n[:-2] + ("_r" if n.endswith("_l") else "_l")
            a[n] = ((-v[0] if mir else v[0]) * sx, v[1] * sy)
        f = dict(f, anchors=a)
    return f


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="top"):
    """put the free hand on the far grip of the piece the other hand holds (anchor grip_far_<side>)."""
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=1.3, shape=shape, layer=layer)


def _pour_to_ground(S, name, key="r", margin=0.10):
    """set pour_len so the stream ends on the figure's own ground line (minus margin)."""
    c, p = S[name]
    for _ in range(3):
        f = figure(c, p, "q")
        lip = f["anchors"].get("pour_lip_" + key)
        if lip is None:
            return
        p["pour_len"] = _clamp(f["feet_y"] - margin - lip[1], 0.2, 3.0)


TOWN = (("woman", ""), ("oldman", "_oldman"), ("boy", "_boy"))


def _story():
    S, M = {}, {}
    F, MC = "farid", "merchant"
    # --- farid
    S["farid_stand"] = (F, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
    S["farid_walk"] = (F, cycle(F, 0.30, "walk", base=dict(expr="determined")))
    S["farid_run"] = (F, cycle(F, 0.30, "run", base=dict(expr="worried", mouth="talk_o")))
    M["farid_run"] = dict(note="one frame of cycle('farid', f / 16, 'run') -- late for the ice: worried, mouth open")
    S["farid_pour"] = (F, dict(yaw=0.55, pitch=0.55, expr="determined", head_roll=-4, lean=16, gaze=(0.7, 0.8),
                               arm_r=dict(hand=(0.80, 0.55), bend=-0.3, stretch=1.3, layer="front"), prop_r=dict(type="bucket", scale=1.25), pour=0.85, pour_side=1,
                               legs=dict(preset="step", stride=0.5, crouch=0.18)))
    M["farid_pour"] = dict(note="night: pouring the bucket into the shallow channel (screen-right).  Pose key pour 0..1 tips the bucket about "
                                "its bail ears (animate 0 -> 0.85 -> 0.85 -> 0); the stream starts at pour ~0.4; pour_len = stream length "
                                "(here set to reach his own ground line); anchors pour_lip_r / pour_end_r, other hand on grip_far_r (the base)")
    S["farid_carry_bucket"] = (F, cycle(F, 0.30, "walk", base=dict(expr="neutral", prop_r="bucket"), arms="l"))
    S["farid_carry_bucket"][1]["arm_r"] = dict(hand=(0.42, 1.02), bend=0.3, stretch=1.05)
    M["farid_carry_bucket"] = dict(note="walking to the channels with a full bucket hanging from the screen-right hand: "
                                        "cycle(F, f / 28, 'walk', base=dict(prop_r='bucket'), arms='l') then set arm_r as here")
    S["farid_saw"] = (F, dict(yaw=0.60, pitch=0.80, expr="determined", head_roll=-6, lean=26, gaze=(0.6, 0.9), head_dy=0.05,
                              arm_r=dict(hand=(0.48, 0.92), bend=-0.2, stretch=1.25), prop_r=dict(type="ice_saw", angle=32),
                              arm_l=dict(hand=(0.30, 1.30), bend=0.4, stretch=1.25, shape="open", layer="front"),
                              legs=dict(preset="crouch", crouch=0.42, stride=0.4)))
    M["farid_saw"] = dict(note="before sunrise: crouched over the channel sawing the ice sheet (screen-right), other hand bracing it.  Animate: "
                               "hand_r += 0.10 * sin(2 pi f / 10) * (cos 32deg, sin 32deg) along the blade; anchor saw_mid_r = the cut point")
    S["farid_pick"] = (F, dict(yaw=0.55, pitch=0.40, expr="determined", head_roll=-4, lean=-6, gaze=(0.6, 0.5),
                               arm_r=dict(hand=(0.66, -0.40), bend=-0.8, stretch=1.3, layer="top"), prop_r=dict(type="ice_pick", angle=-60),
                               arm_l=dict(hand=(0.58, -0.30), bend=-0.8, stretch=1.3, layer="front"), legs="wide"))
    M["farid_pick"] = dict(note="ice pick raised over the head to break the sheet (strike: lerp hand to (0.70, 0.60), angle -40 -> 60)")
    S["farid_carry_ice"] = (F, dict(yaw=0.55, pitch=0.25, expr="determined", fx=["sweat"], head_roll=-4, lean=-5, gaze=(0.8, 0.1),
                                    arm_r=dict(hand=(0.58, 0.82), bend=-0.3, stretch=1.25, layer="front"), prop_r="ice_block",
                                    legs=dict(preset="step", stride=0.35)))
    M["farid_carry_ice"] = dict(note="carrying a block of ice to the dome, leaning back under its weight; ice held in front of the body "
                                     "(cast7 keys panel_grip / panel_side apply); anchor piece_centre_r; the other hand on grip_far_r")
    S["farid_build_wall"] = (F, dict(yaw=0.55, pitch=-0.45, expr="determined", head_roll=-6, gaze=(0.8, -0.6), lean=-4,
                                     arm_l=dict(hand=(0.72, 0.02), bend=-0.6, stretch=1.3, layer="front"), prop_l="mud_brick",
                                     panel_grip="bottom", panel_side=1, legs="wide"))
    M["farid_build_wall"] = dict(note="building the tall shade wall: lifting a mud brick up onto the course above his head (screen-right), "
                                      "both hands under it (panel_grip='bottom', panel_side=1); anchor piece_centre_l")
    S["farid_sleep"] = (F, dict(yaw=0.0, pitch=-0.2, expr="asleep", mouth="smile", fx=["zzz"], lie=90, t=0.3,
                                arm_r=dict(hand=(0.20, 0.95), bend=0.6), arm_l=dict(hand=(-0.20, 0.95), bend=0.6), legs="narrow"))
    M["farid_sleep"] = dict(note="the day he oversleeps: asleep on his back (cast7 pose key lie=90, head to screen-left; canvas CANVAS8_LIE)")
    S["farid_wake_shocked"] = (F, dict(yaw=0.20, pitch=-0.20, expr="shocked", pale=0.7, sweat=1.0, head_roll=6, lean=-4, squash=(0.97, 1.04),
                                       arm_r=dict(hand=(0.40, -0.18), bend=-0.9, shape="open", stretch=1.2, layer="top"),
                                       arm_l=dict(hand=(-0.40, -0.16), bend=-0.9, shape="open", stretch=1.2, layer="top"),
                                       legs=dict(preset="crouch", crouch=0.15)))
    M["farid_wake_shocked"] = dict(note="wakes up late, sun already high: shocked, pale, sweat, hands flying to the head")
    S["farid_smile"] = (F, dict(yaw=0.25, pitch=-0.25, expr="smug", mouth="smile", head_roll=-5, gaze=(0.2, -0.1),
                                arm_r=dict(hand=(-0.16, 0.74), bend=0.7, layer="front"), arm_l=dict(hand=(0.18, 0.70), bend=0.7, layer="front"),
                                legs="stand"))
    M["farid_smile"] = dict(note="calm confident smile, arms folded (the dome is full in summer)")
    S["farid_explain"] = (F, dict(yaw=0.35, pitch=-0.15, expr="happy", mouth="talk_a", head_roll=-6,
                                  arm_r=dict(hand=(0.62, 0.30), shape="open", bend=-0.6, stretch=1.25), arm_l=dict(hand=(-0.16, 0.80), bend=0.6), legs="stand"))
    M["farid_explain"] = dict(note="'I'll sell ice in summer': open palm out, animate mouth with talk_mouth()")
    # --- merchant
    S["merchant_stand"] = (MC, dict(yaw=0.20, pitch=-0.30, expr="smug", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    S["merchant_walk"] = (MC, cycle(MC, 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    S["merchant_laugh"] = (MC, dict(yaw=0.20, pitch=-0.80, expr="laughing", mouth="talk_b", head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                    arm_r=dict(hand=(0.36, 0.95), bend=0.9, shape="open"), arm_l=dict(hand=(-0.40, 0.92), bend=0.9, shape="open"),
                                    legs="wide"))
    M["merchant_laugh"] = dict(note="the big belly laugh, head thrown back, hands on the belly; animate squash (1.02, 0.98) <-> (0.99, 1.01) "
                                    "and mouth talk_b / talk_a every 3 frames")
    S["merchant_mock"] = (MC, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                   arm_r=dict(hand=(1.00, 0.10), shape="point", bend=-0.5, stretch=1.3), arm_l=dict(hand=(-0.42, 0.92), bend=0.9, shape="open"),
                                   legs="wide"))
    M["merchant_mock"] = dict(note="'Ice in the desert? Madman! If you can do it I'll buy it all!': pointing and mocking (screen-right; "
                                   "mirror=True for left), lip-sync with talk_mouth()")
    S["merchant_tears"] = (MC, dict(yaw=0.30, pitch=-0.20, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], cry=1.0, head_roll=14, lean=12, t=0.2,
                                    arm_r=dict(hand=(0.62, 1.42), bend=0.5, shape="open", stretch=1.3),
                                    arm_l=dict(hand=(-0.36, 0.95), bend=0.9, shape="open"), legs=dict(preset="crouch", crouch=0.12, spread=0.15)))
    M["merchant_tears"] = dict(note="'See? No ice in the desert!': laughing to tears (pose key cry 0..1: streams down the cheeks; animate t), "
                                    "bent over, slapping his knee")
    S["merchant_sweat"] = (MC, dict(yaw=0.30, pitch=-0.10, expr="worried", mouth="talk_a", sweat=1.0, heat=1.0, head_roll=-6, t=0.0,
                                    arm_r=dict(hand=(0.52, -0.02), bend=-0.7, stretch=1.2), prop_r=dict(type="fan", angle=-70),
                                    arm_l=dict(hand=(-0.40, 0.92), bend=0.9, shape="open"), legs="wide"))
    M["merchant_sweat"] = dict(note="summer: sweating in the heat (pose keys sweat + heat), fanning himself: animate the fan angle -70 +- 25 "
                                    "every 4 frames and t for the heat shimmer")
    S["merchant_pay"] = (MC, dict(yaw=0.45, pitch=0.25, expr="grinning", sweat=0.5, fx=["blush"], head_roll=10, gaze=(0.6, 0.3), lean=4,
                                  arm_r=dict(hand=(0.78, 0.38), bend=-0.4, stretch=1.3), prop_r="coin_purse",
                                  arm_l=dict(hand=(-0.48, -0.30), bend=-0.9, stretch=1.2, layer="top"), legs="narrow"))
    M["merchant_pay"] = dict(note="the ending: sheepish, scratching the back of his turban, holding the fat coin purse out to farid (screen-right)")
    # --- townsfolk
    for c, sfx in TOWN:
        S["town_laugh" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                         arm_r=dict(hand=(0.78, 0.05), shape="point", bend=-0.6, stretch=1.3),
                                         arm_l=dict(hand=(-0.28, 0.85), bend=0.9), legs="wide"))
        S["town_point" + sfx] = (c, dict(yaw=0.40, pitch=-0.25, expr="smug", mouth="talk_a", head_roll=6,
                                         arm_r=dict(hand=(0.90, -0.02), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="stand"))
        S["town_fan" + sfx] = (c, dict(yaw=0.25, pitch=-0.10, expr="worried", mouth="talk_a", sweat=1.0, heat=0.8, head_roll=-6, t=0.0,
                                       arm_r=dict(hand=(0.46, 0.00), bend=-0.7, stretch=1.2), prop_r=dict(type="fan", angle=-75),
                                       arm_l=dict(hand=(-0.26, 0.80), bend=0.7), legs="stand"))
        S["town_walk" + sfx] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
    S["town_fan_boy"][1].update(arm_r=dict(hand=(0.42, -0.05), bend=-0.7, stretch=1.2, shape="open"), prop_r=None)
    S["town_point_oldman"][1].update(arm_l=dict(hand=(-0.40, 0.70), bend=0.4), prop_l=dict(type="stick", angle=95), legs="narrow", lean=4)
    M["town_laugh"] = dict(note="the bazaar laughs at 'the ice madman' (screen-right; mirror=True for left): woman; _oldman, _boy")
    M["town_point"] = dict(note="pointing and jeering, lip-sync with talk_mouth(): woman; _oldman (leaning on his stick), _boy")
    M["town_fan"] = dict(note="summer heat: sweat + heat, fanning (animate fan angle; the boy flaps an open hand): woman; _oldman, _boy")
    S["woman_jar"] = ("woman", dict(yaw=0.30, pitch=-0.10, expr="happy", head_roll=-4,
                                    arm_r=dict(hand=(0.64, 0.10), bend=-0.6, stretch=1.25, layer="back"), prop_r="water_jar", jar_hold="shoulder",
                                    arm_l=dict(hand=(-0.20, 0.85), bend=0.6), legs="stand"))
    M["woman_jar"] = dict(note="the water jar on her shoulder (jar_hold 'shoulder' / 'hang' / 'hip'); anchor jar_mouth_r")
    S["woman_jar_walk"] = ("woman", cycle("woman", 0.30, "walk", base=dict(expr="neutral", prop_r="water_jar", jar_hold="shoulder"), arms="l"))
    S["woman_jar_walk"][1]["arm_r"] = dict(hand=(0.64, 0.10), bend=-0.6, stretch=1.25, layer="back")
    S["oldman_stick"] = ("oldman", dict(yaw=0.30, pitch=0.20, expr="unimpressed", lean=6, head_roll=4,
                                        arm_r=dict(hand=(0.45, 0.70), bend=0.4), prop_r=dict(type="stick", angle=95),
                                        arm_l="behind", legs="narrow"))
    S["boy_run"] = ("boy", cycle("boy", 0.30, "run", base=dict(expr="excited", mouth="talk_b")))
    # the free hand on the far grip of two-handed pieces
    _two_hands(S, "farid_pour", bend=0.6)
    _pour_to_ground(S, "farid_pour")
    _two_hands(S, "farid_carry_ice", bend=-0.3)
    _two_hands(S, "farid_build_wall", hand_from="l", bend=-0.6, layer="front")
    for n in ("farid_walk", "farid_run", "merchant_walk", "town_walk", "boy_run"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast8.cycle(); animate: cycle(cast, frame / N, mode, facing, base, arms) with "
                                  "N = 28 walk / 16 run / 32 sneak / 24 march"))
    return S, M


STORY8, STORY8_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast8_registered", False):
        CE.register_stage()
        if not STORY8:
            s, m = _story()
            STORY8.update(s)
            STORY8_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_hand", "figure"):
        _O8[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._hand = _hand
    P.figure = figure
    CE.COSTUMES.update(COSTUMES8)
    CE.HATS.update(HATS8)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS8 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP8)
    for n, c in NEW_CAST8.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS8)
    P._cast8_registered = True
    s, m = _story()
    STORY8.update(s)
    STORY8_META.update(m)
    P.STORY.update(STORY8)
    CE.register_stage()


register()
