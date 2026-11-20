#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast9.py -- the cast of film 9 ("the dessert mason": sticky-rice mortar, a Ming city wall, ~1370s) for the v2 puppet,
as an extension module on top of cast8.

    import sys; sys.path.insert(0, ".../v3/cast9"); import cast9      # registers on import (idempotent); imports cast8 .. cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast9.STORY9["lin_stir"]
    f = puppet.figure(cast, pose, "f")                                # stirring the rice soup in the giant cauldron
    w = puppet.figure("lin", cast9.cycle("lin", 0.25, "run"), "f")    # one frame of the run

Nothing in v2/puppet or v3/cast..cast8 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  armour9 (Ming general: scale armour, chest mirror, jade belt, armoured skirt over a red robe)
    cast_ext.HATS      helmet9 (Ming helmet: bowl, ribs, spike finial, red tassel plume, ear flaps; flies off with helmet_off),
                       topknot9 (hair bun + cloth headband with tails), furhat9 (felt cap with a fur brim and a tassel)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast8's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (helmet_off, wet, dust, trowel_mortar, paddle_soup, match_glow, t)
    _face       goatee (CAST goatee9), rain on the face (pose wet)
    _moustache  "long9": long thin drooping moustache (CAST moustache_style)
    _ink_limb   armour shoulder guards (CAST pauldron9) on the arms
    _prop       paddle, trowel, brick9, brick_stack, soup_bucket (cast8's bucket with rice soup: pours), linstock
    figure      dust cloud (pose dust)
New cast: lin, general, worker_a, worker_b, worker_c, gunner_a, gunner_b.
STORY9 / STORY9_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: helmet_svg, paddle_svg, trowel_svg, brick_svg, brick_stack_svg, linstock_svg, soup_bucket_svg.

Command line (QA):  python3 test_cast9.py        lineup.jpg (every member, every pose, cycles, mouths, props), canvas + robustness
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast8")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast8 as C8      # noqa: E402  (v3/cast8, read-only; imports cast7 .. cast_ext and v2/puppet)
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW9 = ("lin", "general", "worker_a", "worker_b", "worker_c", "gunner_a", "gunner_b")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly_d = P._poly_d
_X, _ln = CE._X, CE._ln
_f = C6._f
_O9 = {}
_POSE9 = {"helmet": 0.0, "wet": 0.0, "dust": 0.0, "mortar": 1.0, "soup": 1.0, "glow": 1.0, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
WOOD9 = dict(light="#d2a46a", base="#a8743e", dark="#6a4422")
SOUP = dict(light="#fffdf6", base="#efe6d0", dark="#b8a888")          # rice soup: milky off-white
MORTAR = dict(light="#f2eee6", base="#d8d2c6", dark="#a49c90")
BRICK9 = dict(light="#aeb2b6", base="#8a9096", dark="#5e646c", deep="#464c54", stamp="#6e747c")
STEEL9 = dict(light="#eef0f4", base="#b4bac4", dark="#646c78")
BRASS = dict(light="#fff2b0", base="#e0b040", dark="#9a6c18", deep="#6a4610")
EMBER = dict(core="#fff4a0", hot="#ff9a2a", red="#e0402a")
SMOKE = dict(light="#e8e4e8", base="#bdb6c0", dark="#8a8290")
DUST = dict(light="#efe0c4", base="#d8c4a0", dark="#a8916c")
RAIN = dict(light="#eef8ff", base="#a8d4f0", dark="#4a86b8")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _lin(k, name, c0, c1, c2, x0, y0, x1, y1):
    gid = "%s_%s" % (k.uid, name)
    k.defs.append('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%.4f" y1="%.4f" x2="%.4f" y2="%.4f"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.45" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (gid, x0, y0, x1, y1, k.c(c0), k.c(c1), k.c(c2)))
    return "url(#%s)" % gid


def _taper(pts, w0, w1):
    """closed outline of a stroke along pts whose width goes from w0 to w1 (moustache strands, plume strands)."""
    n = len(pts)
    left, right = [], []
    for i, p in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        tl = math.hypot(tx, ty) or 1.0
        nx, ny = -ty / tl, tx / tl
        w = (w0 + (w1 - w0) * i / float(max(1, n - 1))) / 2.0
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    return P._smooth_closed(left + right[::-1])


def _scales(k, name, dark, light, w=0.11, h=0.075, sw=0.011):
    """fish-scale (lamellar) pattern: dark scale edges with a light glint, transparent ground (lies over a gradient)."""
    pid = "%s_%s" % (k.uid, name)
    arcs = []
    for (ox, oy) in ((0.0, 0.0), (-w / 2, h / 2), (w / 2, h / 2), (0.0, h)):
        arcs.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f"/>'
                    % (ox - w / 2, oy, ox, oy + h * 1.25, ox + w / 2, oy, k.c(dark), sw))
        arcs.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.8"/>'
                    % (ox - w * 0.30, oy + h * 0.30, ox - w * 0.12, oy + h * 0.62, ox + w * 0.05, oy + h * 0.66, k.c(light), sw * 0.8))
    k.defs.append('<pattern id="%s" width="%.4f" height="%.4f" patternUnits="userSpaceOnUse">%s</pattern>' % (pid, w, h, "".join(arcs)))
    return "url(#%s)" % pid


# ============================================================================= pieces (drawn in their own local frame)
PADDLE_LEN = 1.55          # butt at -0.22 behind the hand, blade end at +1.55
PADDLE_TIP = 1.34          # blade centre
PADDLE_GRIP2 = 0.50        # where the other hand holds the shaft


def _paddle_body(k, soup=1.0):
    """the big wooden cauldron paddle along +x: shaft from x -0.22 (rounded butt) to the blade (x 1.12 .. 1.55, 0.20 wide),
    the lower blade coated with rice soup and dripping (soup 0..1)."""
    g = _lin(k, "pdl", WOOD9["light"], WOOD9["base"], WOOD9["dark"], 0, -0.03, 0, 0.03)
    o = ['<path d="M-0.22,-0.028 L1.16,-0.026 L1.16,0.026 L-0.22,0.028 Q-0.25,0 -0.22,-0.028 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
         % (g, k.ink)]
    o.append('<path d="M-0.18,-0.010 L1.10,-0.010" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD9["light"]))
    blade = P._smooth_closed([(1.10, -0.035), (1.22, -0.095), (1.48, -0.100), (1.56, -0.050), (1.57, 0.050), (1.48, 0.100), (1.22, 0.095), (1.10, 0.035)])
    gb = _lin(k, "pdb", WOOD9["light"], WOOD9["base"], WOOD9["dark"], 0, -0.10, 0, 0.10)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (blade, gb, k.ink))
    o.append('<path d="M1.16,0 L1.50,0" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % k.c(WOOD9["dark"]))
    if soup > 0.02:
        x0 = 1.56 - 0.40 * soup
        coat = P._smooth_closed([(x0, -0.090), (1.48, -0.098), (1.56, -0.050), (1.57, 0.050), (1.48, 0.098), (x0, 0.090), (x0 - 0.03, 0.04), (x0 + 0.02, 0.0),
                                 (x0 - 0.04, -0.05)])
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round" opacity="0.95"/>' % (coat, k.c(SOUP["base"]), k.c(SOUP["dark"])))
        o.append('<path d="M%.4f,-0.05 Q%.4f,-0.07 1.50,-0.06" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (x0 + 0.04, x0 + 0.15, k.c(SOUP["light"])))
    return "".join(o)


TROWEL_TIP = (0.47, 0.075)


def _trowel_body(k, mortar=1.0):
    """mason's pointed trowel along +x: round wooden handle (x -0.10 .. 0.13), brass ferrule, a bent steel tang dropping to the
    leaf-shaped blade (heel at x 0.15, point at 0.47, 0.075 below the handle line); a dollop of lime mortar on it (mortar)."""
    o = ['<path d="M0.12,0.0 L0.17,0.0 L0.20,0.055" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round" stroke-linejoin="round"/>' % k.ink]
    o.append('<path d="M0.12,0.0 L0.17,0.0 L0.20,0.055" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" stroke-linejoin="round"/>' % k.c(STEEL9["dark"]))
    gs = _lin(k, "trw", STEEL9["light"], STEEL9["base"], STEEL9["dark"], 0.15, 0.03, 0.40, 0.11)
    blade = "M0.150,0.055 Q0.155,0.020 0.200,0.022 L0.470,0.072 L0.205,0.118 Q0.150,0.110 0.150,0.055 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (blade, gs, k.ink))
    o.append('<path d="M0.19,0.040 L0.40,0.066" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>')
    if mortar > 0.02:
        s = 0.5 + 0.5 * mortar
        blob = P._smooth_closed([(0.20, 0.050), (0.23, 0.050 - 0.040 * s), (0.28, 0.050 - 0.058 * s), (0.33, 0.050 - 0.040 * s), (0.37, 0.060 - 0.016 * s),
                                 (0.36, 0.082), (0.24, 0.090)])
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (blob, k.c(MORTAR["base"]), k.ink))
        o.append('<path d="M0.235,%.4f Q0.27,%.4f 0.31,%.4f" fill="none" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>'
                 % (0.040 - 0.020 * s, 0.026 - 0.030 * s, 0.032 - 0.022 * s))
    o.append('<path d="M-0.10,-0.030 L0.11,-0.026 L0.11,0.026 L-0.10,0.030 Q-0.125,0 -0.10,-0.030 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (k.c(WOOD9["base"]), k.ink))
    o.append('<path d="M-0.08,-0.010 L0.09,-0.010" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD9["light"]))
    o.append('<rect x="0.10" y="-0.033" width="0.035" height="0.066" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["base"]), k.ink))
    return "".join(o)


LINSTOCK_LEN = 1.10        # staff end (fork) from the hand; the glowing match end 0.14 beyond it


def _linstock_body(k, glow=1.0):
    """the gunner's linstock along +x: wooden staff (-0.30 .. 1.02), a brass forked head, the slow match wound round the fork
    with its smouldering end at x 1.18 (glow 0..1: ember)."""
    o = ['<path d="M-0.30,-0.022 L1.00,-0.018 L1.00,0.018 L-0.30,0.022 Q-0.32,0 -0.30,-0.022 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
         % (k.c(WOOD9["base"]), k.ink)]
    o.append('<path d="M-0.26,-0.008 L0.96,-0.007" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD9["light"]))
    # brass fork: socket + two prongs
    o.append('<path d="M0.96,-0.030 L1.04,-0.030 L1.06,-0.070 L1.13,-0.075 L1.13,-0.050 L1.08,-0.045 L1.08,0.045 L1.13,0.050 L1.13,0.075 L1.06,0.070 L1.04,0.030 L0.96,0.030 Z" '
             'fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
    # slow match: a cord wound on the fork, its end hanging out
    o.append('<path d="M1.02,-0.06 Q1.08,-0.10 1.11,-0.06 Q1.14,-0.02 1.10,0.02 Q1.07,0.06 1.12,0.07 Q1.16,0.08 1.18,0.03" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M1.02,-0.06 Q1.08,-0.10 1.11,-0.06 Q1.14,-0.02 1.10,0.02 Q1.07,0.06 1.12,0.07 Q1.16,0.08 1.18,0.03" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c("#b8946a"))
    if glow > 0.02:
        o.append('<circle cx="1.18" cy="0.03" r="%.4f" fill="%s" opacity="%.3f"/>' % (0.075 * glow, k.c(EMBER["hot"]), 0.35 * glow))
        o.append('<circle cx="1.18" cy="0.03" r="0.026" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(EMBER["red"]), k.ink))
        o.append('<circle cx="1.183" cy="0.026" r="%.4f" fill="%s"/>' % (0.014 * glow, k.c(EMBER["core"])))
    else:
        o.append('<circle cx="1.18" cy="0.03" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#3a3436"), k.ink))
    return "".join(o)


def _smoke(k, x, y, t, lev=1.0, n=4):
    """a thin smoke wisp rising from (x, y) (screen up whatever the prop angle), puffs drifting with t."""
    o = []
    ph = t % 1.0
    for i in range(n):
        f = (i + ph) / float(n)
        r = 0.025 + 0.055 * f
        cx = x + 0.06 * math.sin(2 * math.pi * (f * 1.3 + 0.2 * i)) + 0.05 * f
        cy = y - 0.05 - 0.55 * f
        op = lev * 0.75 * (1.0 - f) * _smooth(0.0, 0.15, f)
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.006" opacity="%.3f"/>' % (cx, cy, r, k.c(SMOKE["light"]), k.c(SMOKE["dark"]), op))
    k.ext.append((x, y - 0.62, 0.10))
    return "".join(o)


def _brick_body9(k, w=0.46, h=0.16, dep=0.08, stamp=True):
    """a grey fired Ming wall brick centred on (0, 0): front face, top face, right side face; a darker kiln mottle, a few pits
    and the maker's stamp (a small sunken rectangle with marks) on the front."""
    x0, y0, x1, y1 = -w / 2, -h / 2 + dep * 0.5, w / 2 - dep * 0.6, h / 2
    ox, oy = dep * 0.6, -dep
    o = ['<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
         % (x1, y0, x1 + ox, y0 + oy, x1 + ox, y1 + oy, x1, y1, k.c(BRICK9["dark"]), k.ink)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x0, y0, x0 + ox, y0 + oy, x1 + ox, y0 + oy, x1, y0, k.c(BRICK9["light"]), k.ink))
    g = _lin(k, "bk9%d" % int(1000 * w), BRICK9["light"], BRICK9["base"], BRICK9["dark"], x0, y0, x1, y1)
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.008" fill="%s" stroke="%s" stroke-width="0.018"/>' % (x0, y0, x1 - x0, y1 - y0, g, k.ink))
    fw, fh = x1 - x0, y1 - y0
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.30"/>' % (x0 + fw * 0.30, y0 + fh * 0.55, fw * 0.18, fh * 0.30, k.c(BRICK9["deep"])))
    for (a, b, r) in ((0.12, 0.30, 0.008), (0.78, 0.70, 0.007), (0.88, 0.28, 0.006), (0.46, 0.80, 0.006)):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.8"/>' % (x0 + fw * a, y0 + fh * b, r, k.c(BRICK9["deep"])))
    if stamp and fw > 0.25:
        sx, sy, sw_, sh = x0 + fw * 0.56, y0 + fh * 0.24, fw * 0.26, fh * 0.52
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.007" opacity="0.9"/>' % (sx, sy, sw_, sh, k.c(BRICK9["stamp"]), k.c(BRICK9["deep"])))
        mk = "".join("M%.4f,%.4f l%.4f,0 " % (sx + sw_ * 0.18, sy + sh * f, sw_ * 0.64) for f in (0.3, 0.5, 0.7))
        mk += "M%.4f,%.4f l0,%.4f" % (sx + sw_ * 0.5, sy + sh * 0.2, sh * 0.6)
        o.append('<path d="%s" stroke="%s" stroke-width="0.006" opacity="0.8"/>' % (mk, k.c(BRICK9["deep"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.45"/>' % (x0 + 0.02, y0 + 0.012, x1 - 0.03, y0 + 0.012))
    return "".join(o), (x0, y0 + oy, x1 + ox, y1)


def _brick_stack_body(k, n=3, w=0.46, h=0.16):
    """n bricks stacked flat (slightly staggered), centred on (0, 0)."""
    o = []
    hh = n * (h - 0.01)
    bb = [1e9, 1e9, -1e9, -1e9]
    for i in range(n):
        y = hh / 2 - (i + 0.5) * (h - 0.01)
        x = (0.015, -0.02, 0.01, -0.01)[i % 4]
        s, b = _brick_body9(k, w, h, stamp=(i == 0))
        o.append('<g transform="translate(%.4f %.4f)">%s</g>' % (x, y, s))
        bb = [min(bb[0], b[0] + x), min(bb[1], b[1] + y), max(bb[2], b[2] + x), max(bb[3], b[3] + y)]
    return "".join(o), tuple(bb)


# ============================================================================= helmet (head frame)
def _helmet_parts(k, col, yaw, plume_col, flap=True):
    """the Ming helmet in the head frame with the brow line at y -0.20: iron bowl with gilt ribs, a gilt brow band, ear flaps
    (lamellar) hanging to y 0.42 on both sides, a spike finial with a cup and a big red horsehair tassel.  Returns
    (svg, ext points, top)."""
    dx = -0.03 * yaw
    fx = dx + 0.12 * yaw
    yb, yt = -0.20, -0.70
    o, ext = [], []
    # ear flaps (lamellar, drawn first: the bowl covers their tops)
    if flap:
        for s in (-1, 1):
            g = _clamp(1.0 - 0.55 * max(0.0, s * yaw), 0.4, 1.0)
            xi, xo = dx + s * 0.40, dx + s * (0.40 + 0.20 * g)
            fp = [(xi, yb - 0.02), (xo, yb - 0.04), (xo + s * 0.03, 0.18), (xo - s * 0.01, 0.40), ((xi + xo) / 2, 0.44), (xi + s * 0.02, 0.36)]
            d = P._smooth_closed(fp)
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, k.c(col["dark"]), k.ink))
            o.append('<path d="%s" fill="%s" opacity="0.9"/>' % (d, _scales(k, "fl%d" % (s + 1), col["deep"], col["light"], w=0.07, h=0.05, sw=0.008)))
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" stroke-linejoin="round" opacity="0.95"/>'
                     % (P._smooth_open(fp[1:5]), k.c(BRASS["base"])))
            ext.extend([(xo + s * 0.05, 0.18), ((xi + xo) / 2, 0.46)])
    # spike finial + tassel (behind the bowl top)
    ax = dx * 0.6 + fx * 0.4
    tip = (ax + 0.01, yt - 0.42)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (ax, yt, tip[0], tip[1], k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (ax, yt, tip[0], tip[1], k.c(BRASS["base"])))
    # red tassel: strands from a knot below the spike tip, falling outward over the bowl
    kx, ky = ax + 0.005, yt - 0.20
    strands = []
    for i in range(9):
        a = -1.0 + 2.0 * i / 8.0
        sx = kx + a * 0.30 - 0.04 * yaw
        sy = ky + 0.30 - 0.06 * abs(a)
        pts = [(kx + a * 0.02, ky), (kx + a * 0.15, ky + 0.06), (sx, sy)]
        strands.append(_taper(pts, 0.070, 0.020))
        ext.append((sx, sy))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (" ".join(strands), k.c(plume_col), k.ink))
    o.append('<path d="%s" fill="%s" opacity="0.55"/>' % (" ".join(strands[:4]), k.c(P._shade(plume_col, 1.25))))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.034" fill="%s" stroke="%s" stroke-width="0.012"/>' % (kx, ky, k.c(BRASS["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.028" fill="%s" stroke="%s" stroke-width="0.010"/>' % (tip[0], tip[1], k.c(BRASS["light"]), k.ink))
    ext.extend([(tip[0], tip[1] - 0.03), (kx - 0.34, ky + 0.30), (kx + 0.34, ky + 0.30)])
    # bowl
    bowl = [(dx - 0.53, yb), (dx - 0.53, yb - 0.14), (dx - 0.40, yt + 0.16), (ax - 0.16, yt + 0.01), (ax, yt - 0.01), (ax + 0.16, yt + 0.01), (dx + 0.40, yt + 0.16),
            (dx + 0.53, yb - 0.14), (dx + 0.53, yb)]
    d = P._smooth_open(bowl) + " Q%.4f,%.4f %.4f,%.4f Z" % (fx, yb + 0.05, dx - 0.53, yb)
    gb = CE._gradient(k, "hm", col, x0=-0.55, x1=0.55, mid=0.30)
    k.defs.append('<clipPath id="%s_hmc"><path d="%s"/></clipPath>' % (k.uid, d))
    o.append('<path d="%s" fill="%s"/>' % (d, gb))
    rib = []
    for f in (-0.66, -0.33, 0.0, 0.33, 0.66):
        x = fx + f * 0.52
        rib.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x, yb, x - f * 0.04, (yb + yt) / 2, ax + f * 0.10, yt + 0.02))
    o.append('<g clip-path="url(#%s_hmc)"><path d="%s" fill="none" stroke="%s" stroke-width="0.040"/><path d="%s" fill="none" stroke="%s" stroke-width="0.020"/>'
             '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.030" stroke-linecap="round" opacity="0.35"/></g>'
             % (k.uid, " ".join(rib), k.ink, " ".join(rib), k.c(BRASS["base"]), dx - 0.38, yb - 0.10, dx - 0.34, yt + 0.22, dx - 0.12, yt + 0.06))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, k.ink))
    # cup at the top
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (ax - 0.09, yt + 0.02, ax - 0.05, yt - 0.08, ax + 0.05, yt - 0.08, ax + 0.09, yt + 0.02, k.c(BRASS["base"]), k.ink))
    # brow band with a gilt plaque over the forehead
    band = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.545, yb - 0.075, fx, yb - 0.035, dx + 0.545, yb - 0.075, dx + 0.54, yb + 0.010, fx, yb + 0.055, dx - 0.54, yb + 0.010))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (band, k.c(BRASS["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.9"/>'
             % (dx - 0.50, yb - 0.050, fx, yb - 0.012, dx + 0.20, yb - 0.035, k.c(BRASS["light"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (fx, yb - 0.14, fx + 0.07, yb - 0.04, fx, yb + 0.05, fx - 0.07, yb - 0.04, k.c(BRASS["light"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s"/>' % (fx, yb - 0.045, k.c("#c8202e")))
    # small visor
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
             % (fx - 0.24, yb + 0.045, fx, yb + 0.10, fx + 0.24, yb + 0.045, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (fx - 0.22, yb + 0.045, fx, yb + 0.095, fx + 0.22, yb + 0.045, k.c(col["dark"])))
    ext.extend([(dx - 0.56, yb), (dx + 0.56, yb), (ax, yt - 0.1)])
    return "".join(o), ext, tip


def _bare_topknot(k, C, yaw, band=None, tails=False, crown=False):
    """black hair over the crown with a round bun (topknot) on top; band = (colour, dark) draws a cloth headband over the brow,
    tails = its knotted ends flicking out on the side away from the face; crown = a small gilt hair crown on the bun."""
    dx = -0.03 * yaw
    hc = k.c(C["hair"]["color"])
    bx = dx - 0.04 * yaw
    o = []
    o.append('<ellipse cx="%.4f" cy="-0.62" rx="0.15" ry="0.13" fill="%s" stroke="%s" stroke-width="0.024"/>' % (bx, hc, k.ink))
    o.append('<path d="M%.4f,-0.66 Q%.4f,-0.72 %.4f,-0.69" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (bx - 0.09, bx - 0.02, bx + 0.06, k.c(C["hair"].get("shine", "#5a5a70"))))
    hair, top = C4._hair_dome(k, C, dx, -0.22, -0.54)
    o.append(hair)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.32, -0.34, dx - 0.22, -0.48, dx - 0.04, -0.52, k.c(C["hair"].get("shine", "#5a5a70"))))
    # the bun's tie
    o.append('<path d="M%.4f,-0.53 L%.4f,-0.53" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (bx - 0.10, bx + 0.10, k.ink))
    o.append('<path d="M%.4f,-0.53 L%.4f,-0.53" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (bx - 0.09, bx + 0.09, k.c(band[0] if band else "#8a2a2a")))
    top = -0.75
    if crown:
        o.append('<path d="M%.4f,-0.62 L%.4f,-0.74 L%.4f,-0.70 L%.4f,-0.78 L%.4f,-0.70 L%.4f,-0.74 L%.4f,-0.62 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (bx - 0.10, bx - 0.10, bx - 0.04, bx, bx + 0.04, bx + 0.10, bx + 0.10, k.c(BRASS["base"]), k.ink))
        o.append('<path d="M%.4f,-0.66 L%.4f,-0.66" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (bx - 0.20, bx + 0.20, k.c(BRASS["light"])))
        top = -0.79
    ext = [(bx - 0.17, -0.62), (bx + 0.17, -0.62), (bx, top - 0.01), (dx - 0.50, -0.25), (dx + 0.50, -0.25)]
    if band:
        yb = -0.245
        bd = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
              % (-0.49 + dx, yb - 0.045, dx, yb - 0.005, 0.49 + dx, yb - 0.045, 0.485 + dx, yb + 0.040, dx, yb + 0.080, -0.485 + dx, yb + 0.040))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (bd, k.c(band[0]), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
                 % (-0.44 + dx, yb + 0.005, dx, yb + 0.045, 0.44 + dx, yb + 0.005, k.c(band[1])))
        if tails:
            s = -1.0 if yaw >= 0 else 1.0
            fz = _clamp(0.35 + abs(yaw), 0.35, 1.0)
            kx, ky = s * (0.47 - 0.10 * (1 - fz)) + dx, yb + 0.02
            for (ang, ln) in ((20.0, 0.26), (55.0, 0.22)):
                ex, ey = kx + s * ln * math.cos(math.radians(ang)) * fz, ky + ln * math.sin(math.radians(ang))
                tail = [(kx, ky - 0.025), (ex + s * 0.02, ey - 0.025), (ex, ey + 0.02), (kx, ky + 0.025)]
                o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(tail), k.c(band[0]), k.ink))
                ext.append((ex + s * 0.03, ey))
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.040" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, k.c(band[0]), k.ink))
    return "".join(o), ext, (bx, top)


HELMET_COL = dict(light="#8a94a8", base="#5a6478", dark="#363e50", deep="#22283a", shine="#c8d0e0")


def _helmet_fly(v, side):
    """where the flying helmet is (head frame) at progress v (0..1): up and back over the shoulder, spinning."""
    x = side * (0.30 + 1.35 * v)
    y = -0.45 - 1.90 * v + 1.20 * v * v
    return x, y, side * 470.0 * v


def _hat_helmet9(k, C, yaw):
    col = C.get("hat_colors", HELMET_COL)
    plume = C.get("plume9", "#d0202a")
    v = _POSE9["helmet"]
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    if v <= 0.0:
        svg, ext, top = _helmet_parts(k, col, yaw, plume)
        o.append(svg)
        o.append('</g>')
        C4._ext_hat(k, C, ext)
        return "".join(o), top
    # helmet off: the bare head with the topknot and a little gilt crown; the helmet flies (v < 1) or is gone (v >= 1)
    svg, ext, top = _bare_topknot(k, C, yaw, band=None, crown=True)
    o.append(svg)
    o.append('</g>')
    C4._ext_hat(k, C, ext)
    if v < 1.0:
        side = -1.0 if yaw >= 0 else 1.0
        x, y, r = _helmet_fly(v, side)
        hs, hext, _ = _helmet_parts(k, col, 0.0, plume, flap=True)
        o.append('<g transform="translate(%.4f %.4f) rotate(%.3f) translate(0 0.25)">%s</g>' % (x, y, r, hs))
        for (ex, ey) in hext:
            q = _rot(ex, ey + 0.25, r)
            k.ext.append((x + q[0], y + q[1], 0.03))
        # speed lines
        o.append('<path d="M%.4f,%.4f l%.4f,%.4f M%.4f,%.4f l%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
                 % (x - side * 0.55, y + 0.30, -side * 0.22, 0.12, x - side * 0.45, y + 0.48, -side * 0.18, 0.10, k.ink))
    return "".join(o), top


def _hat_topknot9(k, C, yaw):
    col = C.get("hat_colors", {})
    band = (col["band"], col.get("dark", "#555555")) if col.get("band") else None
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    svg, ext, top = _bare_topknot(k, C, yaw, band=band, tails=bool(band) and C.get("band_tails", True))
    o.append(svg)
    o.append('</g>')
    C4._ext_hat(k, C, ext)
    return "".join(o), top


def _hat_furhat9(k, C, yaw):
    """enemy gunner: rounded felt cap (dark) with a thick fur brim, a knob and a short red tassel on top."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    ax = dx - 0.03 * yaw
    yb, yt = -0.22, -0.78
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    crown = [(dx - 0.44, yb - 0.08), (dx - 0.42, yb - 0.26), (ax - 0.30, yt + 0.10), (ax, yt), (ax + 0.30, yt + 0.10), (dx + 0.42, yb - 0.26), (dx + 0.44, yb - 0.08)]
    g = CE._gradient(k, "fh", col, x0=-0.45, x1=0.45, mid=0.30)
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(crown), g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (ax, yt + 0.02, ax + 0.04, -0.50, ax + 0.02, yb - 0.10, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.6"/>'
             % (dx - 0.34, yb - 0.24, ax - 0.26, yt + 0.16, ax - 0.06, yt + 0.04, k.c(col["shine"])))
    # fur brim: a fuzzy band
    pts = []
    n = 16
    for i in range(n + 1):
        t = i / float(n)
        x = dx - 0.56 + 1.12 * t
        pts.append((x, yb - 0.13 + 0.03 * math.sin(math.pi * t) - (0.025 if i % 2 else 0.0)))
    low = []
    for i in range(n + 1):
        t = 1.0 - i / float(n)
        x = dx - 0.55 + 1.10 * t
        low.append((x, yb + 0.06 + 0.035 * math.sin(math.pi * t) + (0.022 if i % 2 else 0.0)))
    fur = "M" + " L".join("%.4f,%.4f" % p for p in pts + low) + " Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (fur, k.c(col["fur"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.48, yb - 0.06, dx, yb, dx + 0.30, yb - 0.04, k.c(col["fur_l"])))
    # knob + tassel
    o.append('<path d="M%.4f,%.4f q-0.06,0.10 -0.10,0.20 M%.4f,%.4f q0.00,0.12 0.02,0.22 M%.4f,%.4f q0.05,0.10 0.10,0.18" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
             % (ax, yt, ax, yt, ax, yt, k.ink))
    o.append('<path d="M%.4f,%.4f q-0.06,0.10 -0.10,0.20 M%.4f,%.4f q0.00,0.12 0.02,0.22 M%.4f,%.4f q0.05,0.10 0.10,0.18" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (ax, yt, ax, yt, ax, yt, k.c(col["tassel"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.036" fill="%s" stroke="%s" stroke-width="0.012"/>' % (ax, yt - 0.01, k.c(col["tassel"]), k.ink))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.58, yb), (dx + 0.58, yb), (ax, yt - 0.06), (dx, yb + 0.12)))
    return "".join(o), (ax, yt - 0.05)


HATS9 = {"helmet9": _hat_helmet9, "topknot9": _hat_topknot9, "furhat9": _hat_furhat9}


# ============================================================================= costume: Ming armour (torso-local)
def _cos_armour9(k, C, m):
    """the general's armour: lamellar scales over the whole torso (on the torso gradient), the red robe's crossed collar at
    the neck, a round polished brass chest mirror on crossed straps, a wide red belt with gilt plaques and a beast-face
    buckle; over the hips the red robe skirt to the knees under two armoured skirt flaps (scales, gilt border) and a front
    apron."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * C.get("sash_y", 0.70)
    robe = col.get("robe", "#b8202a")
    gold = k.c(BRASS["base"])
    o = ['<rect x="-0.8" y="0.2" width="1.6" height="1.8" fill="%s" opacity="0.9"/>' % _scales(k, "ar", col["dark"], col.get("light", "#ffffff"))]
    # straps from the shoulders to the mirror
    cy = TT + h * 0.40
    for s in (-1, 1):
        st = [X(s * hw * 0.80, TT + 0.06), X(0.0, cy)]
        o.append(_ln(st, k.ink, 0.070))
        o.append(_ln(st, k.c(col.get("strap", "#7a2a22")), 0.044))
    # crossed collar of the red robe
    nk = [X(-0.24, 0.36), X(0.02, 0.66), X(0.26, 0.36)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (nk[0] + nk[1] + nk[2] + (k.c(robe), k.ink)))
    o.append(_ln([X(-0.20, 0.38), X(0.10, 0.58)], gold, 0.030))
    o.append(_ln([X(0.22, 0.38), X(0.00, 0.62)], gold, 0.020))
    # chest mirror
    mx, my = X(0.0, cy)
    r = min(0.20, hw * 0.30)
    gm = _lin(k, "mir", BRASS["light"], BRASS["base"], BRASS["dark"], mx - r, my - r, mx + r, my + r)
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.022"/>' % (mx, my, r, gm, k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.012"/>' % (mx, my, r * 0.74, k.c(BRASS["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.010"/>' % (mx, my, r * 0.30, k.c(BRASS["light"]), k.c(BRASS["dark"])))
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.75"/>'
             % (mx - r * 0.62, my - r * 0.25, r * 0.66, r * 0.66, mx - r * 0.12, my - r * 0.62))
    for a in (45, 135, 225, 315):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.016" fill="%s" stroke="%s" stroke-width="0.006"/>'
                 % (mx + r * 0.87 * math.cos(math.radians(a)), my + r * 0.87 * math.sin(math.radians(a)), k.c(BRASS["light"]), k.ink))
    inside = "".join(o)
    # ---- over: robe skirt, armoured flaps, apron, belt
    yt = yB - 0.16
    hem = yB + C.get("robe_len", 0.56)
    a = hw * 0.985
    b = hw + C.get("robe_flare", 0.14)
    gr = C2._grad(k, "rb9", robe, -b, b)
    ov = [C2._skirt(k, "rb", X, yt, a, hem, b, gr, sw=0.026,
                    folds=((-0.10, yt + 0.20, -0.14, hem - 0.05), (0.12, yt + 0.20, 0.16, hem - 0.05)), fold_col=k.c(P._shade(robe, 0.65)))]
    fh = hem - 0.12
    ga = C2._grad(k, "fl9", col["base"], -b, b)
    sc = _scales(k, "sk", col["dark"], col.get("light", "#ffffff"))
    for s in (-1, 1):
        pan = [X(s * 0.05, yt - 0.02), X(s * a * 1.01, yt - 0.02), X(s * (b + 0.03), fh - 0.02), X(s * (b * 0.55), fh + 0.04), X(s * 0.08, fh)]
        d = P._smooth_closed(pan)
        ov.append('<path d="%s" fill="%s"/>' % (d, ga))
        ov.append('<path d="%s" fill="%s" opacity="0.9"/>' % (d, sc))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (d, k.ink))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, gold))
        k.ext.append((X(s * (b + 0.05), fh)[0], fh + 0.05, 0.03))
    # front apron (bixi) with a gilt diamond
    ap = [X(-0.17, yw), X(0.17, yw), X(0.15, yw + 0.46), X(0.0, yw + 0.54), X(-0.15, yw + 0.46)]
    ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(ap), k.c(P._shade(robe, 0.80)), k.ink))
    cx_, cy_ = X(0.0, yw + 0.28)
    ov.append('<path d="M%.4f,%.4f l0.07,0.08 l-0.07,0.08 l-0.07,-0.08 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (cx_, cy_ - 0.08, gold, k.ink))
    ov.append(_ln([X(-0.15, yw + 0.46), X(0.0, yw + 0.54), X(0.15, yw + 0.46)], gold, 0.016))
    # belt
    sw = C.get("sash_w", 0.15)
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.ink, sw + 0.028))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.c(col.get("belt", "#9a1a24")), sw))
    for xx in (-0.70, -0.48, -0.28, 0.28, 0.48, 0.70):
        if abs(xx) * 1.0 > hw * 0.95:
            continue
        p = X(xx, yw + 0.04 * (1 - (xx / max(hw, 0.1)) ** 2))
        ov.append('<rect x="%.4f" y="%.4f" width="0.10" height="%.4f" rx="0.012" fill="%s" stroke="%s" stroke-width="0.010"/>' % (p[0] - 0.05, p[1] - sw * 0.36, sw * 0.72, k.c(col.get("jade", "#7ec8a0")), k.ink))
    bx, by = X(0.0, yw + 0.04)
    ov.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (bx, by, sw * 0.80, gold, k.ink))
    # beast face on the buckle: two eyes, brows, a grin
    e = sw * 0.30
    ov.append('<path d="M%.4f,%.4f l%.4f,%.4f M%.4f,%.4f l%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
              % (bx - e * 1.3, by - e * 0.9, e * 0.9, e * 0.4, bx + e * 1.3, by - e * 0.9, -e * 0.9, e * 0.4, k.ink))
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>' % (bx - e * 0.7, by - e * 0.1, k.ink, bx + e * 0.7, by - e * 0.1, k.ink))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (bx - e, by + e * 0.6, bx, by + e * 1.3, bx + e, by + e * 0.6, k.ink))
    return inside, "", "".join(ov)


COSTUMES9 = {"armour9": _cos_armour9}


# ============================================================================= arms: shoulder guards
def _pauldron(k, S, E, C):
    """a lamellar shoulder guard over the top of the arm: three scalloped rows hanging along the upper arm, a gilt rim and a
    small beast mask at the shoulder."""
    dx, dy = E[0] - S[0], E[1] - S[1]
    ang = math.degrees(math.atan2(dy, dx))
    col = C["colors"]
    sz = C.get("pauldron9", 1.0)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (S[0], S[1], ang, sz)]
    for i, x in enumerate((0.20, 0.11, 0.02)):
        d = "M%.4f,-0.16 Q%.4f,-0.20 %.4f,-0.15 L%.4f,0.15 Q%.4f,0.20 %.4f,0.16 Q%.4f,0.0 %.4f,-0.16 Z" % (x - 0.10, x + 0.02, x + 0.08, x + 0.08, x + 0.02, x - 0.10, x - 0.14, x - 0.10)
        sc = [0.035 * j - 0.12 for j in range(8)]
        pc = col.get("pauldron", col["base"])
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(pc if i != 1 else P._shade(pc, 0.85)), k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>'
                 % (" ".join("M%.4f,%.4f q0.03,0.012 0.06,0" % (x - 0.03, y) for y in sc), k.c(col.get("pauldron_d", col["dark"]))))
        o.append('<path d="M%.4f,-0.15 Q%.4f,0.0 %.4f,0.15" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x + 0.07, x + 0.11, x + 0.07, k.c(BRASS["base"])))
    o.append('<circle cx="-0.06" cy="0" r="0.075" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<circle cx="-0.08" cy="-0.022" r="0.010" fill="%s"/><circle cx="-0.08" cy="0.022" r="0.010" fill="%s"/>' % (k.ink, k.ink))
    o.append('<path d="M-0.03,-0.03 Q-0.01,0 -0.03,0.03" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.ink)
    o.append('</g>')
    for (x, y) in ((-0.14, 0.0), (0.30, -0.2), (0.30, 0.2), (-0.10, -0.2), (-0.10, 0.2)):
        q = _rot(x * sz, y * sz, ang)
        k.ext.append((S[0] + q[0], S[1] + q[1], 0.03))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O9["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if tail is None and C is not None and C.get("pauldron9"):
        out += _pauldron(k, S, E, C)
    return out


# ============================================================================= face: long moustache, goatee, rain
def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "long9":
        return _O9["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#1a161a")
    s = s * C.get("tache_scale", 1.0)
    ln = C.get("tache_len", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    o = []
    for sd in (-1, 1):
        pts = [Q(sd * 0.02, -0.050), Q(sd * 0.12, -0.045), Q(sd * 0.22, 0.000), Q(sd * 0.27, 0.10 * ln), Q(sd * 0.29, 0.24 * ln), Q(sd * 0.27, 0.38 * ln), Q(sd * 0.31, 0.46 * ln)]
        d = _taper(pts, 0.085 * s, 0.018 * s)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>'
                 % (Q(sd * 0.06, -0.06) + Q(sd * 0.20, -0.03) + Q(sd * 0.24, 0.10 * ln) + (k.c(C["colors"].get("moustache_l", "#5a5058")),)))
        k.ext.append(Q(sd * 0.31, 0.47 * ln) + (0.03,))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (Q(0.0, -0.06) + Q(0.0, 0.0) + (k.ink,)))
    return "".join(o)


def _goatee(k, C, L):
    col = C["colors"].get("moustache", "#1a161a")
    mx, my = L["mx"], L["my"]
    pts = [(mx - 0.05, my + 0.10), (mx + 0.05, my + 0.10), (mx + 0.03, my + 0.24), (mx, my + 0.32), (mx - 0.03, my + 0.24)]
    k.ext.append((mx, my + 0.33, 0.02))
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink)


def _rain_face(k, L, lev, t):
    """wet in the rain: water running down the cheeks and drops falling off the chin / beside the head (animate t)."""
    o = []
    for i, (x, y0, ln) in enumerate(((L["xL"] - 0.04, L["ey"] + 0.10, 0.14), (L["xR"] + 0.05, L["ey"] + 0.06, 0.18), (L["mx"] + 0.16, L["my"] + 0.02, 0.10))):
        o.append('<path d="M%.4f,%.4f q0.012,%.4f 0,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="%.3f"/>'
                 % (x, y0, ln * 0.5, ln * lev, k.c(RAIN["base"]), 0.85 * lev))
    for i, (x, y0) in enumerate(((-0.60, -0.10), (0.62, -0.05), (0.0, 0.52), (-0.66, 0.30), (0.66, 0.34))):
        f = (t * 1.6 + 0.37 * i) % 1.0
        y = y0 + 0.40 * f
        op = lev * (1.0 - f) * _smooth(0.0, 0.1, f)
        o.append('<path d="M%.4f,%.4f q-0.036,0.064 0,0.088 q0.036,-0.024 0,-0.088 Z" fill="%s" stroke="%s" stroke-width="0.009" opacity="%.3f"/>'
                 % (x, y, k.c(RAIN["base"]), k.c(RAIN["dark"]), op))
        k.ext.append((x, y0 + 0.45, 0.03))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O9["_face"](k, C, P_, white)
    if C is None or not C.get("_cast9"):
        return svg, L
    under, over = [], []
    if C.get("goatee9"):
        under.append(_goatee(k, C, L))
    if _POSE9["wet"] > 0.02:
        over.append(_rain_face(k, L, _POSE9["wet"], _POSE9["t"]))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


# ============================================================================= props held in the hand
NEW_PROPS9 = ("paddle", "trowel", "brick9", "brick_stack", "soup_bucket", "linstock")
BRICK_W, BRICK_H = 0.46, 0.16
NEW_TIP9 = {"paddle": PADDLE_TIP, "trowel": math.hypot(*TROWEL_TIP), "brick9": BRICK_W / 2, "brick_stack": BRICK_W / 2,
            "soup_bucket": C8.BUCKET_RIM + C8.BUCKET_H, "linstock": LINSTOCK_LEN + 0.08}


def _flat9(k, kind, H, sc):
    """brick9 / brick_stack held like cast7's panels / cast8's mud brick (pose keys panel_grip side / bottom / top, panel_side)."""
    side = -1.0 if H[0] > 0.02 else 1.0
    if C7._POSE7["pside"]:
        side = C7._POSE7["pside"]
    if kind == "brick9":
        body, bb = _brick_body9(k, BRICK_W, BRICK_H)
    else:
        body, bb = _brick_stack_body(k, 3, BRICK_W, BRICK_H)
    w, h = (bb[2] - bb[0]) * sc, (bb[3] - bb[1]) * sc
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
        tr += ' scale(-1 1)'
    for (x, y) in ((bb[0], bb[1]), (bb[2], bb[1]), (bb[0], bb[3]), (bb[2], bb[3])):
        k.ext.append((cx + x * sc * side, cy + y * sc, 0.03))
    return '<g transform="%s">%s</g>' % (tr, body), (cx, cy), far


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS9:
        return _O9["_prop"](k, kind, H, ang, sc)
    if kind == "soup_bucket":
        keep = dict(C8.WATER)
        C8.WATER.update(SOUP)
        try:
            return _O9["_prop"](k, "bucket", H, ang, sc)
        finally:
            C8.WATER.clear()
            C8.WATER.update(keep)
    key = C8._side_key()
    an = C8._POSE8["an"]
    if kind in ("brick9", "brick_stack"):
        svg, tip, far = _flat9(k, kind, H, sc)
        an["grip_far_" + key] = far
        an["piece_centre_" + key] = tip
        return svg, tip
    if kind == "paddle":
        body = _paddle_body(k, _POSE9["soup"])
        pts = ((-0.25, 0.0), (1.12, -0.04), (1.12, 0.04), (1.50, -0.11), (1.50, 0.11), (1.58, 0.0))
        tipd, grip = (PADDLE_TIP, 0.0), (PADDLE_GRIP2, 0.0)
    elif kind == "trowel":
        body = _trowel_body(k, _POSE9["mortar"])
        pts = ((-0.12, 0.0), (0.15, 0.12), (0.47, 0.075), (0.28, -0.03))
        tipd, grip = TROWEL_TIP, None
    else:
        body = _linstock_body(k, _POSE9["glow"])
        pts = ((-0.32, 0.0), (1.13, -0.08), (1.13, 0.08), (1.22, 0.03))
        tipd, grip = (1.18, 0.03), (0.55, 0.0)
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    for e in pts:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(tipd[0] * sc, tipd[1] * sc, ang)
    tip = (H[0] + tx, H[1] + ty)
    if grip:
        gx, gy = _rot(grip[0] * sc, grip[1] * sc, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
    if kind == "paddle":
        an["blade_" + key] = tip
        if _POSE9["soup"] > 0.3:
            # a drip falling from the blade end (screen down)
            ex, ey = _rot(1.52 * sc, 0.0, ang)
            f = (_POSE9["t"] * 1.5) % 1.0
            o += ('<path d="M%.4f,%.4f q-0.022,0.04 0,0.055 q0.022,-0.015 0,-0.055 Z" fill="%s" stroke="%s" stroke-width="0.006" opacity="%.3f"/>'
                  % (H[0] + ex, H[1] + ey + 0.05 + 0.20 * f, k.c(SOUP["base"]), k.c(SOUP["dark"]), 1.0 - f))
            k.ext.append((H[0] + ex, H[1] + ey + 0.30, 0.03))
    elif kind == "trowel":
        an["trowel_tip_" + key] = tip
    else:
        an["match_" + key] = tip
        if _POSE9["glow"] > 0.02:
            o += _smoke(k, tip[0], tip[1], _POSE9["t"], _POSE9["glow"])
    return o, tip


# ============================================================================= standalone pieces
def _keep9(fn):
    keep8, keep9 = dict(C8._POSE8), dict(_POSE9)
    try:
        return fn()
    finally:
        C8._POSE8.clear()
        C8._POSE8.update(keep8)
        _POSE9.clear()
        _POSE9.update(keep9)


def helmet_svg(uid="hm", rot=0.0, yaw=0.0, plume="#d0202a", ink=P.INK, tint=None):
    """the general's helmet alone, head frame (as worn: brow line at y -0.20, a head of D = 1 centred on (0, 0) would wear it),
    rotated by rot degrees about (0, 0).  For the helmet flying / lying in the rubble after the fall.  Returns (svg, top)."""
    k = _ctx(uid, ink, tint)
    s, ext, top = _helmet_parts(k, HELMET_COL, yaw, plume)
    return '<g id="%s_helmet" transform="rotate(%.3f)"><defs>%s</defs>%s</g>' % (k.uid, rot, "".join(k.defs), s), top


def paddle_svg(uid="pd", soup=1.0, ink=P.INK, tint=None):
    """the cauldron paddle along +x (hand at (0, 0)), blade centre at x 1.34."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_paddle"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _paddle_body(k, _clamp(_num(soup, 1.0), 0.0, 1.0)))


def trowel_svg(uid="tw", mortar=1.0, ink=P.INK, tint=None):
    """the mason's trowel along +x (hand at (0, 0)), point at (0.47, 0.075)."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_trowel"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), _trowel_body(k, _clamp(_num(mortar, 1.0), 0.0, 1.0)))


def linstock_svg(uid="ls", glow=1.0, t=0.0, smoke=True, ink=P.INK, tint=None):
    """the linstock along +x (hand at (0, 0)), smouldering match end at (1.18, 0.03), smoke rising from it."""
    k = _ctx(uid, ink, tint)
    g = _clamp(_num(glow, 1.0), 0.0, 1.0)
    s = _linstock_body(k, g)
    if smoke and g > 0.02:
        s += _smoke(k, 1.18, 0.03, _num(t, 0.0), g)
    return '<g id="%s_linstock"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def brick_svg(uid="br", w=BRICK_W, h=BRICK_H, ink=P.INK, tint=None):
    """one grey Ming wall brick centred on (0, 0) (front w x h + top + side faces, maker's stamp).  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    s, bb = _brick_body9(k, w, h)
    return '<g id="%s_brick"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


def brick_stack_svg(uid="bs", n=3, w=BRICK_W, h=BRICK_H, ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s, bb = _brick_stack_body(k, int(_clamp(_num(n, 3), 1, 12)), w, h)
    return '<g id="%s_bricks"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


def soup_bucket_svg(uid="sb", pour=0.0, side=1, water=1.0, pour_len=1.0, ink=P.INK, tint=None):
    """cast8.bucket_svg with rice soup instead of water.  Returns (svg, anchors base, lip, end)."""
    keep = dict(C8.WATER)
    C8.WATER.update(SOUP)
    try:
        return C8.bucket_svg(uid, pour, side, water, pour_len, ink, tint)
    finally:
        C8.WATER.clear()
        C8.WATER.update(keep)


# ============================================================================= pose keys, dust (figure wrapper)
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE9["helmet"] = _f(g("helmet_off"), 0.0, 0.0, 1.0)
    _POSE9["wet"] = _f(g("wet"), 0.0, 0.0, 1.0)
    _POSE9["dust"] = _f(g("dust"), 0.0, 0.0, 1.0)
    _POSE9["mortar"] = _f(g("trowel_mortar"), 1.0, 0.0, 1.0)
    _POSE9["soup"] = _f(g("paddle_soup"), 1.0, 0.0, 1.0)
    _POSE9["glow"] = _f(g("match_glow"), 1.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE9["t"] = t if math.isfinite(t) else 0.0
    return _O9["_norm"](C, pose)


def _dust(lev, t, x0, x1, y, uid):
    """a dust cloud along the ground line y between x0 and x1 (figure coordinates): two rows of big overlapping soft puffs that
    swell and drift with t, a few flying grit specks."""
    o = []
    w = max(0.8, x1 - x0)
    cx = (x0 + x1) / 2
    ext = []
    puffs = []
    for row, n in ((0, 9), (1, 7), (2, 4)):
        for i in range(n):
            a = (i + 0.5) / n
            ph = (t * 0.7 + 0.29 * i + 0.5 * row) % 1.0
            r = (0.26 + 0.12 * math.sin(i * 2.7 + row) ** 2) * (0.55 + 0.45 * lev) * (0.9 + 0.2 * ph)
            x = cx + (a - 0.5) * (w + 0.4) * (0.8 + 0.2 * lev) * (1.0, 0.78, 0.50)[row] + 0.06 * math.sin(i * 1.9 + row)
            yy = y - 0.14 - 0.24 * row * lev - 0.10 * math.sin(math.pi * a) * lev * (1 + row) - 0.06 * ph
            puffs.append((row, x, yy, r))
            ext.append((x - r, yy - r, x + r, yy + r))
    op = 0.92 * lev
    # one merged cloud: an ink rim under all puffs, the fills over it (no outline between puffs), shade below, light on top
    o.append('<g opacity="%.3f">' % op)
    o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, yy, r + 0.022, P.INK) for (row, x, yy, r) in puffs))
    o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, yy, r, DUST["base"]) for (row, x, yy, r) in puffs))
    o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x - r * 0.12, yy - r * 0.16, r * 0.80, DUST["light"]) for (row, x, yy, r) in puffs))
    o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.8"/>' % (x - r * 0.25, yy - r * 0.32, r * 0.38, "#fbf4e6") for (row, x, yy, r) in puffs))
    o.append('</g>')
    for i in range(6):
        ph = (t * 1.3 + 0.17 * i) % 1.0
        x = cx + (i - 2.5) * w * 0.22 * (0.6 + 0.6 * ph)
        yy = y - 0.2 - 0.7 * ph + 0.5 * ph * ph
        o.append('<rect x="%.4f" y="%.4f" width="0.05" height="0.035" fill="%s" stroke="%s" stroke-width="0.008" transform="rotate(%.1f %.4f %.4f)" opacity="%.3f"/>'
                 % (x, yy, BRICK9["base"], P.INK, 200 * ph + 40 * i, x, yy, lev * (1 - ph)))
    return '<g id="%s_dust">%s</g>' % (uid, "".join(o)), ext


def figure(cast_name, pose=None, uid="p"):
    f = _O9["figure"](cast_name, pose, uid)
    if isinstance(pose, dict) and pose.get("dust") is not None and isinstance(cast_name, str) and cast_name in P.CAST:
        lev = _f(pose.get("dust"), 0.0, 0.0, 1.0)
        if lev > 0.02:
            t = _num(pose.get("t"), 0.0)
            t = t if math.isfinite(t) else 0.0
            b = f["bbox"]
            mir = bool(pose.get("mirror"))
            gy = f["feet_y"] - (0.35 * lev if pose.get("lie") else 0.0)      # lying: the cloud swallows the lower body
            s, ext = _dust(lev, t, b[0], b[2], gy, uid)
            if mir:
                s = '<g transform="scale(-1 1)">%s</g>' % s
                ext = [(-e[2], e[1], -e[0], e[3]) for e in ext]
            bb = (min([b[0]] + [e[0] for e in ext]), min([b[1]] + [e[1] for e in ext]), max([b[2]] + [e[2] for e in ext]), max([b[3]] + [e[3] for e in ext]))
            f = dict(f, svg=f["svg"] + s, bbox=bb)
    return f


# ============================================================================= cast
NEW_CAST9 = {
    # Lin: young Ming mason -- black hair in a topknot bun, a cloth headband (light blue-grey) tied at the back, simple blue
    # cross-collar tunic to mid-thigh, a dark sash, sleeves rolled, grey-black trousers, cloth shoes
    "lin": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=91.3,
        torso_w=0.70, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.27, 0.49), arm=0.74, hip_x=0.15, leg=1.26, stance=0.07, wide=0.27, limb_w=0.058,
        eye_y=0.040, brow="stroke", brow_th=0.066, mouth="dash", moustache=False, smirk_side=1, cheeks="#e8a088",
        hat="newsboy", hat_style="topknot9", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(band="#dfe6ee", dark="#9aa8b8"),
        hair=dict(color="#1e1a1e", front=0.10, grow=0.22, shine="#4a4a60"),
        costume="robe8", robe_len=0.34, robe_flare=0.10, sash_w=0.11, hem_band=False,
        sleeve=dict(color="#3a62a8", dark="#25427a", cuff="#dfe6ee", len=0.54, w=0.150, roll=True),
        shorts=dict(color="#3a3842", dark="#24222a", cuff="#3a3842", len=0.90, w=0.13),
        boots=dict(color="#2e2a30", cuff="#2e2a30", h=0.06, toe=0.14, soft=True),
        colors=dict(base="#3a62a8", dark="#25427a", trim="#dfe6ee", sash="#2a2a36", sash_d="#16161e", pants="#3a3842"),
    ),
    # the general: big, armoured -- iron Ming helmet with gilt ribs, spike and red tassel plume, ear flaps; long drooping black
    # moustache + goatee, heavy brows; gilt-bronze lamellar armour with a brass chest mirror, shoulder guards, a red belt with
    # jade plaques, armoured skirt flaps over a red robe; black boots
    "general": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=55.9,
        torso_w=1.46, torso_h=1.30, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.36, stance=0.07, wide=0.32, limb_w=0.070,
        eye_y=0.010, brow="stroke", brow_th=0.085, mouth="smirk", moustache=True, moustache_style="long9", tache_scale=1.10, tache_len=1.0,
        smirk_side=1, cheeks="#ec8070", goatee9=True, chins=True, pauldron9=1.45,
        hat="newsboy", hat_style="helmet9", hat_tilt=-2.0, ear_pencil=False, plume9="#d0202a",
        hat_colors=dict(HELMET_COL),
        hair=dict(color="#1a161a", front=0.06, grow=0.20, shine="#4a4a5a"),
        costume="armour9", robe_len=0.60, robe_flare=0.16, sash_w=0.17,
        sleeve=dict(color="#b8202a", dark="#7a1018", cuff="#e0b040", len=0.84, w=0.210),
        shorts=dict(color="#b8202a", dark="#7a1018", cuff="#b8202a", len=0.90, w=0.15),
        boots=dict(color="#2a2228", cuff="#e0b040", h=0.16, toe=0.18),
        colors=dict(base="#caa04a", dark="#6a4a18", light="#fff0b0", pauldron="#5a6478", pauldron_d="#22283a", robe="#b8202a", strap="#7a2a22", belt="#8a1420", jade="#8ad0aa",
                    pants="#b8202a", moustache="#1a161a", moustache_l="#5a5058", trim="#e0b040"),
    ),
    # the workers: worker_a tall and thin, conical straw hat, ochre tunic; worker_b round, topknot with a white headband, brown
    # tunic, apron of sacking; worker_c short and wiry, red-brown headband, grey-green tunic
    "worker_a": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=12.7,
        torso_w=0.62, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.76, hip_x=0.14, leg=1.34, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.030, brow="stroke", brow_th=0.050, mouth="dash", moustache=False, smirk_side=-1, cheeks="#e8a088",
        hat="newsboy", hat_style="sugegasa", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#f0d890", base="#d6b462", dark="#9a7a36", shine="#fff0c0", rim="#8a6a2c", cord="#6a4a2a"),
        hair=dict(color="#1e1a1e", front=0.08, grow=0.20),
        costume="robe8", robe_len=0.30, robe_flare=0.10, sash_w=0.10, hem_band=False,
        sleeve=dict(color="#c8963a", dark="#8a6420", cuff="#c8963a", len=0.50, w=0.140, roll=True),
        shorts=dict(color="#6a5a48", dark="#4a3e30", cuff="#6a5a48", len=0.62, w=0.13),
        boots=dict(color="#4a3a2a", cuff="#4a3a2a", h=0.05, toe=0.13, soft=True),
        colors=dict(base="#c8963a", dark="#8a6420", trim="#7a5a2a", sash="#5a4a3a", sash_d="#3a2e22", pants="#6a5a48"),
    ),
    "worker_b": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="regular", seed=33.4,
        torso_w=0.92, torso_h=0.96, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.32, 0.47), arm=0.72, hip_x=0.16, leg=1.04, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.010, brow="stroke", brow_th=0.060, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.70, smirk_side=1, cheeks="#ec9078",
        hat="newsboy", hat_style="topknot9", hat_tilt=2.0, ear_pencil=False,
        hat_colors=dict(band="#f4f0e6", dark="#b8b0a0"), band_tails=True,
        hair=dict(color="#1e1a1e", front=0.08, grow=0.20, shine="#4a4a60"),
        costume="robe8", robe_len=0.28, robe_flare=0.12, sash_w=0.10, hem_band=False,
        sleeve=dict(color="#8a5a3a", dark="#5e3a22", cuff="#8a5a3a", len=0.46, w=0.160, roll=True),
        shorts=dict(color="#4a4048", dark="#302a30", cuff="#4a4048", len=0.62, w=0.14),
        boots=dict(color="#3a2e28", cuff="#3a2e28", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#8a5a3a", dark="#5e3a22", trim="#c8b48a", sash="#c8b48a", sash_d="#8a7a58", pants="#4a4048", moustache="#2a2224"),
    ),
    "worker_c": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=71.2,
        torso_w=0.64, torso_h=0.86, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.70, hip_x=0.14, leg=1.06, stance=0.07, wide=0.26, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.040, mouth="dash", moustache=False, smirk_side=1, cheeks="#f0a090",
        hat="newsboy", hat_style="topknot9", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(band="#b84a2a", dark="#7a2a16"), band_tails=True,
        hair=dict(color="#1e1a1e", front=0.10, grow=0.22, shine="#4a4a60"),
        costume="robe8", robe_len=0.28, robe_flare=0.08, sash_w=0.09, hem_band=False,
        sleeve=dict(color="#6a8a6a", dark="#46604a", cuff="#6a8a6a", len=0.50, w=0.140, roll=True),
        shorts=dict(color="#8a7a62", dark="#5e5240", cuff="#8a7a62", len=0.62, w=0.13),
        boots=dict(color="#4a3a2a", cuff="#4a3a2a", h=0.05, toe=0.12, soft=True),
        colors=dict(base="#6a8a6a", dark="#46604a", trim="#d8c8a0", sash="#b84a2a", sash_d="#7a2a16", pants="#8a7a62"),
    ),
    # the enemy gunners: padded dark coats, round felt caps with fur brims and red tassels (simple, generic)
    "gunner_a": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="regular", seed=24.6,
        torso_w=0.84, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.30, 0.47), arm=0.72, hip_x=0.15, leg=1.12, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.070, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.80, smirk_side=-1, cheeks="#e88a78",
        hat="newsboy", hat_style="furhat9", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#6a5a7a", base="#463a56", dark="#2a2236", shine="#9a8aaa", fur="#8a6a4a", fur_l="#c8a882", tassel="#c8302a"),
        hair=dict(color="#1e1a1e", front=0.06, grow=0.20),
        costume="robe8", robe_len=0.44, robe_flare=0.14, sash_w=0.12, coat="#5a4430", coat_drop=-0.06,
        sleeve=dict(color="#5a4430", dark="#3a2a1c", cuff="#8a6a4a", len=0.80, w=0.170),
        shorts=dict(color="#3a3440", dark="#24202a", cuff="#3a3440", len=0.90, w=0.14),
        boots=dict(color="#2a2228", cuff="#5a4430", h=0.12, toe=0.15),
        colors=dict(base="#3e5a5a", dark="#263c3c", trim="#8a6a4a", sash="#7a2a22", sash_d="#4a1812", coat_trim="#8a6a4a", pants="#3a3440", moustache="#2a2224"),
    ),
    "gunner_b": dict(
        _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=86.1,
        torso_w=0.66, torso_h=0.96, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.49), arm=0.74, hip_x=0.14, leg=1.22, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.040, brow="stroke", brow_th=0.060, mouth="dash", moustache=False, smirk_side=1, cheeks="#e8907a",
        hat="newsboy", hat_style="furhat9", hat_tilt=4.0, ear_pencil=False,
        hat_colors=dict(light="#8a4a3a", base="#6a3226", dark="#421c14", shine="#b87a6a", fur="#a88a62", fur_l="#e0c8a0", tassel="#2a4a8a"),
        hair=dict(color="#1e1a1e", front=0.08, grow=0.20),
        costume="robe8", robe_len=0.42, robe_flare=0.12, sash_w=0.11, coat="#4a4a3a", coat_drop=-0.06,
        sleeve=dict(color="#4a4a3a", dark="#2e2e24", cuff="#a88a62", len=0.80, w=0.150),
        shorts=dict(color="#4a3a32", dark="#2e241e", cuff="#4a3a32", len=0.90, w=0.13),
        boots=dict(color="#2a2228", cuff="#4a4a3a", h=0.12, toe=0.14),
        colors=dict(base="#7a5a3a", dark="#4e3822", trim="#a88a62", sash="#2a2a36", sash_d="#16161e", coat_trim="#a88a62", pants="#4a3a32"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast9.py canvas).
CANVAS9 = {
    "lin": (-1.8750, -4.5000, 1.8750, 0.1250),
    "general": (-1.6875, -5.2500, 1.6875, 0.1250),
    "worker_a": (-1.4375, -4.5625, 1.4375, 0.1250),
    "worker_b": (-1.5000, -4.2500, 1.5000, 0.1250),
    "worker_c": (-1.4375, -4.1875, 1.4375, 0.1250),
    "gunner_a": (-1.8750, -4.3750, 1.8750, 0.1250),
    "gunner_b": (-1.8125, -4.4375, 1.8125, 0.1250),
}
# the general falling / landing / with the helmet flying (helmet_off) or a dust cloud: pass this canvas to Actor.build
CANVAS9_FALL = {"general": (-5.4375, -5.75, 5.4375, 0.3125)}


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="top", stretch=1.3):
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _pour_to_ground(S, name, key="r", margin=0.10):
    c, p = S[name]
    for _ in range(3):
        f = figure(c, p, "q")
        lip = f["anchors"].get("pour_lip_" + key)
        if lip is None:
            return
        p["pour_len"] = _clamp(f["feet_y"] - margin - lip[1], 0.2, 3.0)


WORKERS = (("worker_a", ""), ("worker_b", "_b"), ("worker_c", "_c"))
GUNNERS = (("gunner_a", ""), ("gunner_b", "_b"))


def _story():
    S, M = {}, {}
    L, G = "lin", "general"
    # --- lin
    S["lin_stand"] = (L, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
    S["lin_walk"] = (L, cycle(L, 0.30, "walk", base=dict(expr="determined")))
    S["lin_run"] = (L, cycle(L, 0.30, "run", base=dict(expr="worried", mouth="talk_o")))
    S["lin_stir"] = (L, dict(yaw=0.55, pitch=0.45, expr="determined", head_roll=-4, lean=8, gaze=(0.7, 0.6), t=0.3,
                             arm_l=dict(hand=(0.36, 0.10), bend=-0.5, stretch=1.25, layer="front"), prop_l=dict(type="paddle", angle=60, scale=1.35),
                             legs=dict(preset="step", stride=0.45, crouch=0.10)))
    M["lin_stir"] = dict(note="stirring the rice soup in the giant cauldron (screen-right) with the big paddle, both hands on the shaft "
                              "(the upper hand holds it: prop_l; the lower hand on grip_far_l); anchor blade_l = the blade in the pot.  Animate: move both hands on a small "
                              "ellipse (+-0.12, +-0.05) every 24 frames and the paddle angle 58 +- 8; t drives the soup drip")
    S["lin_pour"] = (L, dict(yaw=0.55, pitch=0.55, expr="determined", head_roll=-4, lean=16, gaze=(0.7, 0.8),
                             arm_r=dict(hand=(0.80, 0.55), bend=-0.3, stretch=1.3, layer="front"), prop_r=dict(type="soup_bucket", scale=1.25), pour=0.85, pour_side=1,
                             legs=dict(preset="step", stride=0.5, crouch=0.18)))
    M["lin_pour"] = dict(note="pouring the rice soup bucket into the lime mortar (screen-right): cast8 pour keys (pour 0 -> 0.85 -> 0, "
                              "pour_len set to reach his ground line), anchors pour_lip_r / pour_end_r, other hand on grip_far_r (the base)")
    S["lin_lay_brick"] = (L, dict(yaw=0.60, pitch=0.70, expr="determined", head_roll=-5, lean=20, gaze=(0.6, 0.8), head_dy=0.04,
                                  arm_r=dict(hand=(0.78, 0.98), bend=-0.2, stretch=1.25, layer="front"), prop_r=dict(type="trowel", angle=20, scale=1.35),
                                  arm_l=dict(hand=(0.46, 1.10), bend=0.3, stretch=1.25, layer="front"), prop_l="brick9", panel_grip="top", panel_side=1,
                                  legs=dict(preset="crouch", crouch=0.40, stride=0.35)))
    M["lin_lay_brick"] = dict(note="laying a brick on the course (screen-right, waist height): left hand pressing the brick down from above "
                                   "(panel_grip='top'), the trowel in the right hand scraping / tapping it (trowel_mortar 0..1 = mortar on the "
                                   "blade; anchor trowel_tip_r).  Animate: tap the trowel angle 20 -> -10 -> 20 every 8 frames")
    S["lin_trowel"] = (L, dict(yaw=0.55, pitch=0.60, expr="determined", head_roll=-4, lean=14, gaze=(0.7, 0.7),
                               arm_r=dict(hand=(0.82, 0.72), bend=-0.3, stretch=1.25, layer="front"), prop_r=dict(type="trowel", angle=10, scale=1.35),
                               arm_l=dict(hand=(-0.30, 0.86), bend=0.6), legs=dict(preset="step", stride=0.4, crouch=0.12)))
    M["lin_trowel"] = dict(note="spreading mortar with the trowel (screen-right); sweep the hand x 0.62 .. 0.95 along the course")
    S["lin_calm"] = (L, dict(yaw=0.25, pitch=-0.25, expr="smug", mouth="smile", head_roll=-5, gaze=(0.2, -0.1),
                             arm_r=dict(hand=(-0.16, 0.74), bend=0.7, layer="front"), arm_l=dict(hand=(0.18, 0.70), bend=0.7, layer="front"),
                             legs="stand"))
    M["lin_calm"] = dict(note="calm, confident smile, arms folded (laughed at, he keeps cooking rice)")
    S["lin_rain"] = (L, dict(yaw=0.30, pitch=-1.1, expr="worried", mouth="wavy", gaze=(0.2, -1.0), head_roll=-6, wet=1.0, t=0.2,
                             arm_r=dict(hand=(0.62, 0.05), bend=-0.6, stretch=1.2, shape="open"), arm_l=dict(hand=(-0.30, 0.82), bend=0.6),
                             legs="stand"))
    M["lin_rain"] = dict(note="the first rain: looking up worried, palm out to feel the drops (pose key wet 0..1: water on the face and "
                              "drops falling, animate t); the rice mortar is still soft")
    S["lin_watch"] = (L, dict(yaw=0.40, pitch=-0.10, expr="neutral", mouth="flat", gaze=(0.8, 0.0), head_roll=-2,
                              arm_r="behind", arm_l="behind", legs="stand"))
    M["lin_watch"] = dict(note="watching calmly as the cannons fire (screen-right), hands behind his back; blink with blink_at()")
    S["lin_explain"] = (L, dict(yaw=0.35, pitch=-0.15, expr="happy", mouth="talk_a", head_roll=-6,
                                arm_r=dict(hand=(0.62, 0.30), shape="open", bend=-0.6, stretch=1.25), arm_l=dict(hand=(-0.16, 0.80), bend=0.6), legs="stand"))
    S["lin_carry_bucket"] = (L, cycle(L, 0.30, "walk", base=dict(expr="neutral", prop_r="soup_bucket"), arms="l"))
    S["lin_carry_bucket"][1]["arm_r"] = dict(hand=(0.42, 1.02), bend=0.3, stretch=1.05)
    M["lin_carry_bucket"] = dict(note="walking with the bucket of rice soup: cycle(L, f / 28, 'walk', base=dict(prop_r='soup_bucket'), arms='l') "
                                      "then set arm_r as here")
    # --- general
    S["general_stand"] = (G, dict(yaw=0.20, pitch=-0.30, expr="smug", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    S["general_walk"] = (G, cycle(G, 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    S["general_laugh"] = (G, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                  arm_r=dict(hand=(0.40, 0.98), bend=0.9, shape="open"), arm_l=dict(hand=(-0.44, 0.95), bend=0.9, shape="open"),
                                  legs="wide"))
    M["general_laugh"] = dict(note="the big belly laugh, head thrown back, hands on the belly; animate squash (1.02, 0.98) <-> (0.99, 1.01) "
                                   "and mouth talk_b / talk_a every 3 frames")
    S["general_mock"] = (G, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                 arm_r=dict(hand=(1.05, 0.10), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    M["general_mock"] = dict(note="'Sticky rice? You're cooking dessert for the wall!': pointing and mocking (screen-right; mirror=True for left), "
                                 "lip-sync with talk_mouth()")
    S["general_wall_laugh"] = (G, dict(yaw=0.10, pitch=-0.90, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-12, lean=-6, t=0.3,
                                       arm_r="akimbo", arm_l="akimbo", legs="wide", squash=(1.02, 0.98)))
    M["general_wall_laugh"] = dict(note="on top of his (taller) wall: arms akimbo, head thrown back laughing; animate squash + mouth as general_laugh")
    S["general_rain_shout"] = (G, dict(yaw=0.40, pitch=-0.40, expr="shouting", mouth="talk_b", head_roll=6, wet=1.0, t=0.2,
                                       arm_r=dict(hand=(1.00, 0.20), shape="point", bend=-0.5, stretch=1.3),
                                       arm_l=dict(hand=(-0.95, -0.30), bend=-0.8, stretch=1.25, layer="front"), legs="wide"))
    M["general_rain_shout"] = dict(note="'See? Dessert gets soggy in the rain!': shouting in the rain (wet=1, animate t), pointing at the soft "
                                        "rice mortar (screen-right), the other fist up; lip-sync with talk_mouth()")
    S["general_fall"] = (G, dict(yaw=0.30, pitch=-0.6, expr="shocked", mouth="talk_o", head_roll=-14, lie=42, helmet_off=0.45, dust=0.8, t=0.2,
                                 arm_r=dict(hand=(0.78, -0.55), bend=-0.7, stretch=1.25, shape="open", layer="top"),
                                 arm_l=dict(hand=(-0.70, -0.60), bend=-0.7, stretch=1.25, shape="open", layer="top"),
                                 legs=dict(preset="stand", lift_r=1.2, lift_l=0.5, spread=0.25)))
    M["general_fall"] = dict(note="the comic fall (no injury): sliding down the rubble on his back feet first to screen-right (cast7 lie=42), "
                                  "arms flailing, the helmet flying off (pose key helmet_off 0..1 = progress of the helmet's arc, >= 1 gone; "
                                  "or draw helmet_svg() yourself), dust cloud (pose key dust 0..1, animate t).  Canvas CANVAS9_FALL['general']")
    S["general_land"] = (G, dict(yaw=0.20, pitch=-0.5, expr="laughing", mouth="talk_b", head_roll=-8, helmet_off=1.0, dust=0.6, t=0.6,
                                 fx=["tears"], arm_r=dict(hand=(0.70, 0.40), bend=-0.3, stretch=1.2, shape="open"),
                                 arm_l=dict(hand=(-0.70, 0.40), bend=-0.3, stretch=1.2, shape="open"),
                                 legs=dict(preset="crouch", crouch=0.70, spread=0.35)))
    M["general_land"] = dict(note="landed sitting in the rubble and dust, helmet gone (topknot showing), still laughing; place helmet_svg() "
                                  "in the rubble beside him")
    # --- workers
    for c, sfx in WORKERS:
        S["workers_laugh" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                            arm_r=dict(hand=(0.78, 0.05), shape="point", bend=-0.6, stretch=1.3),
                                            arm_l=dict(hand=(-0.28, 0.85), bend=0.9), legs="wide"))
        S["workers_point" + sfx] = (c, dict(yaw=0.40, pitch=-0.25, expr="smug", mouth="talk_a", head_roll=6,
                                            arm_r=dict(hand=(0.90, -0.02), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="stand"))
        S["workers_carry" + sfx] = (c, dict(yaw=0.50, pitch=0.15, expr="determined", fx=["sweat"], head_roll=-4, lean=-5, gaze=(0.8, 0.1),
                                            arm_r=dict(hand=(0.50, 0.86), bend=-0.3, stretch=1.25, layer="front"), prop_r="brick_stack",
                                            legs=dict(preset="step", stride=0.35)))
        S["workers_walk" + sfx] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
    M["workers_laugh"] = dict(note="the workers laugh at 'ไอ้ช่างขนม' (screen-right; mirror=True for left): worker_a; _b, _c")
    M["workers_point"] = dict(note="pointing and jeering, lip-sync with talk_mouth(): worker_a; _b, _c")
    M["workers_carry"] = dict(note="carrying a stack of three bricks in front with both hands (other hand on grip_far_r), leaning back: "
                                   "worker_a; _b, _c.  For walking: cycle(c, f / 28, 'walk', base=dict(prop_r='brick_stack'), arms='') and set "
                                   "both arms as here")
    # --- gunners
    for c, sfx in GUNNERS:
        S["gunner_light" + sfx] = (c, dict(yaw=0.55, pitch=0.45, expr="determined", head_roll=-4, lean=14, gaze=(0.7, 0.7), t=0.3,
                                           arm_r=dict(hand=(0.42, 0.40), bend=-0.4, stretch=1.25, layer="front"), prop_r=dict(type="linstock", angle=32),
                                           arm_l=dict(hand=(-0.20, 0.80), bend=0.6),
                                           legs=dict(preset="step", stride=0.6, crouch=0.20)))
        S["gunner_ears" + sfx] = (c, dict(yaw=-0.25, pitch=0.30, expr="shouting", blink=2, mouth="clench", head_roll=-8, lean=-6, squash=(1.03, 0.96),
                                          arm_r=dict(hand=(0.52, 0.02), bend=-0.9, stretch=1.15, shape="open", layer="top"),
                                          arm_l=dict(hand=(-0.52, 0.02), bend=-0.9, stretch=1.15, shape="open", layer="top"),
                                          legs=dict(preset="crouch", crouch=0.30, spread=0.10)))
        S["gunner_stand" + sfx] = (c, dict(yaw=0.40, pitch=0.0, expr="neutral", arm_r=dict(hand=(0.40, 0.55), bend=0.2), prop_r=dict(type="linstock", angle=-80),
                                           arm_l="down", legs="stand"))
    M["gunner_light"] = dict(note="enemy gunner touching the smouldering linstock to the cannon's touch hole (screen-right, low), other hand on "
                                  "the knee; anchor match_r = the glowing match end (smoke rises from it, animate t; match_glow 0..1): gunner_a; _b")
    M["gunner_ears"] = dict(note="covering both ears, eyes squeezed shut, wincing, ducking as the cannon fires: gunner_a; _b")
    M["gunner_stand"] = dict(note="standing by the cannon, linstock upright: gunner_a; _b")
    # the free hand on the far grip of two-handed pieces
    _two_hands(S, "lin_stir", hand_from="l", bend=0.3, layer="front")
    _two_hands(S, "lin_pour", bend=0.6)
    _pour_to_ground(S, "lin_pour")
    for c, sfx in WORKERS:
        _two_hands(S, "workers_carry" + sfx, bend=-0.3)
    for n in ("lin_walk", "lin_run", "general_walk") + tuple("workers_walk" + s for _, s in WORKERS):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast9.cycle(); animate: cycle(cast, frame / N, mode, facing, base, arms) with "
                                  "N = 28 walk / 16 run / 32 sneak / 24 march"))
    return S, M


STORY9, STORY9_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast9_registered", False):
        CE.register_stage()
        if not STORY9:
            s, m = _story()
            STORY9.update(s)
            STORY9_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_ink_limb", "figure"):
        _O9[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    P.figure = figure
    CE.COSTUMES.update(COSTUMES9)
    CE.HATS.update(HATS9)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS9 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP9)
    for n, c in NEW_CAST9.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS9)
    P._cast9_registered = True
    s, m = _story()
    STORY9.update(s)
    STORY9_META.update(m)
    P.STORY.update(STORY9)
    CE.register_stage()


register()
