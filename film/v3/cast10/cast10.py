#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast10.py -- the cast of film 10 ("the zebra painter": dazzle camouflage, a British naval dockyard, 1917) for the v2
puppet, as an extension module on top of cast9.

    import sys; sys.path.insert(0, ".../v3/cast10"); import cast10    # registers on import (idempotent); imports cast9 .. cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast10.STORY10["painter_paint_stroke"]
    f = puppet.figure(cast, pose, "f")                                # the big brush raised, sweeping a stripe
    w = puppet.figure("admiral", cast10.cycle("admiral", 0.25, "walk"), "f")

Nothing in v2/puppet or v3/cast .. cast9 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  overalls10 (painter's whites, paint-splattered), admiral10 (navy double-breasted coat, gold buttons, medal
                       ribbons, knee-length skirt), sailor10 (white jumper, blue square collar, black silk), ucoat10 (U-boat
                       leather coat over a white roll-neck)
    cast_ext.HATS      peaked10 (peaked cap: crown, band, badge, visor, optional gold braid; paint spots), dixie10 (white sailor cap)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
    puppet.EXPRESSIONS "squint" (both eyes squeezed, determined brows, frown) -- added only if missing
and wraps puppet helpers on top of cast9's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (paint_spots, brush_paint, brush_col, bucket_paint, plank, plank_w, plank_rope,
                periscope, t)
    _face       paint spots on the face and moustache (pose paint_spots)
    _moustache  "walrus10": the admiral's huge white walrus moustache (CAST moustache_style)
    _ink_limb   gold epaulettes on the arms (CAST epaulette10), paint splatter on the trouser legs (CAST splat10)
    _prop       bigbrush (dripping), paint_bucket, binoculars
    figure      hanging painter's plank under the feet (pose plank), the U-boat periscope column (pose periscope)
New cast: painter10, admiral, sailor_a, sailor_b, sailor_c, uboat_captain.
STORY10 / STORY10_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: bigbrush_svg, paint_bucket_svg, binoculars_svg, plank_svg, periscope_svg.

The painter is registered as "painter10" (CAST "painter" is cast7's copyist and must not change).

Command line (QA):  python3 test_cast10.py        sheet.jpg (every member, every pose, expressions, props), canvas + robustness
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast9")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast9 as C9      # noqa: E402  (v3/cast9, read-only; imports cast8 .. cast_ext and v2/puppet)
import cast8 as C8      # noqa: E402
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW10 = ("painter10", "admiral", "sailor_a", "sailor_b", "sailor_c", "uboat_captain")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O10 = {}
_POSE10 = {"spots": 0.0, "brush": 1.0, "bcol": "black", "bucket": 1.0, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
PAINT = {"black": dict(base="#1c1a20", light="#5a5866", dark="#0a090c"),
         "white": dict(base="#f6f4ee", light="#ffffff", dark="#b8b4aa"),
         "grey": dict(base="#8a9098", light="#c0c6ce", dark="#5a6068")}
WOOD10 = dict(light="#e0b47a", base="#b07a44", dark="#6e4a26")
PLANK = dict(light="#d8b07a", base="#b08452", dark="#76542e", deep="#5a3e20")
ROPE = dict(base="#d2b98a", dark="#8e7650")
TIN = dict(light="#e4e8ec", base="#aab2bc", dark="#6a727e")
GOLD = dict(light="#fff0a8", base="#e2b442", dark="#a07818", deep="#6a4c0c")
STEEL = dict(light="#a8b4b0", base="#6e7c78", dark="#46524e", deep="#2c3634")
GLASS = dict(light="#9ec4ea", base="#3a5a8a", dark="#14223a")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _hash(*a):
    """deterministic pseudo-random 0..1 from numbers."""
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _splat(k, x, y, r, col, seed, ext=False, op=1.0):
    """an irregular paint splat: a lumpy blob with two or three satellite drops (seeded)."""
    pts = []
    n = 9
    for i in range(n):
        a = 2 * math.pi * i / n + seed
        rr = r * (0.70 + 0.55 * _hash(seed, i))
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a) * 0.85))
    o = ['<path d="%s" fill="%s"%s/>' % (P._smooth_closed(pts), k.c(col), (' opacity="%.3f"' % op) if op < 0.999 else "")]
    for j in range(3):
        a = 2 * math.pi * _hash(seed, 20 + j)
        d = r * (1.6 + 0.9 * _hash(seed, 30 + j))
        rr = r * (0.18 + 0.20 * _hash(seed, 40 + j))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"%s/>' % (x + d * math.cos(a), y + d * math.sin(a), rr, k.c(col),
                                                                       (' opacity="%.3f"' % op) if op < 0.999 else ""))
    if ext:
        k.ext.append((x, y, r * 2.5))
    return "".join(o)


def _drip(k, x, y, ln, w, col):
    """a paint run from (x, y) downwards with a round drop at its end."""
    return ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>'
            % (x, y, x, y + ln, k.c(col), w, x, y + ln, w * 0.85, k.c(col)))


# ============================================================================= props (own local frames)
BRUSH_TIP = 1.02          # bristle ends along +x
BRUSH_GRIP2 = -0.42       # where the other hand holds the handle (butt side)


def _brush_body(k, paint=1.0, col="black"):
    """the big wall brush along +x: a long wooden handle (-0.56 .. 0.62), a broad tin ferrule (0.60 .. 0.74, 0.22 wide) and a
    thick flat bristle block (0.74 .. 1.02) loaded with paint (paint 0..1), runs of paint on the ferrule."""
    pc = PAINT.get(col, PAINT["black"])
    g = _lin(k, "bh", WOOD10["light"], WOOD10["base"], WOOD10["dark"], 0, -0.035, 0, 0.035)
    o = ['<path d="M-0.56,-0.026 Q-0.60,0 -0.56,0.026 L0.62,0.040 L0.62,-0.040 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M-0.50,-0.010 L0.56,-0.018" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD10["light"]))
    o.append('<circle cx="-0.50" cy="0" r="0.012" fill="%s" stroke="%s" stroke-width="0.006"/>' % (k.c(WOOD10["dark"]), k.ink))
    # bristles (behind the ferrule edge)
    bc = pc["base"] if paint > 0.05 else "#e8dcc0"
    bl = [(0.72, -0.120), (0.90, -0.140), (1.00, -0.135), (1.03, -0.070), (1.02, 0.000), (1.03, 0.070), (1.00, 0.135), (0.90, 0.140), (0.72, 0.120)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (P._smooth_closed(bl), k.c(bc), k.ink))
    st = "".join("M0.76,%.4f L%.4f,%.4f " % (y, 0.99 - 0.02 * abs(y) / 0.13, y * 1.05) for y in (-0.10, -0.06, -0.02, 0.02, 0.06, 0.10))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.6"/>' % (st, k.c(pc["light"] if paint > 0.05 else "#b8a888")))
    if paint > 0.05:
        o.append('<path d="M0.80,-0.115 Q0.92,-0.125 0.98,-0.100" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.85"/>' % k.c(pc["light"]))
    # ferrule
    gf = _lin(k, "bf", TIN["light"], TIN["base"], TIN["dark"], 0, -0.11, 0, 0.11)
    o.append('<path d="M0.60,-0.050 L0.68,-0.115 L0.76,-0.120 L0.76,0.120 L0.68,0.115 L0.60,0.050 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (gf, k.ink))
    o.append('<path d="M0.64,-0.080 L0.64,0.080 M0.70,-0.105 L0.70,0.105" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(TIN["dark"]))
    if paint > 0.3:
        # paint run back over the ferrule
        o.append('<path d="M0.76,-0.06 Q0.70,-0.05 0.69,-0.02 Q0.71,0.00 0.76,0.01 Z M0.76,0.05 Q0.72,0.06 0.73,0.09 L0.76,0.10 Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
                 % (k.c(pc["base"]), k.ink))
    return "".join(o)


def _bucket_body(k, paint=1.0, col="black"):
    """painter's tin pail hanging from its wire bail (hand at (0, 0)): rim at y 0.20, bottom at y 0.52, paint surface in the
    mouth and runs down the side.  Always upright."""
    pc = PAINT.get(col, PAINT["black"])
    o = ['<path d="M-0.175,0.215 Q-0.165,-0.035 0,-0.020 Q0.165,-0.035 0.175,0.215" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.175,0.215 Q-0.165,-0.035 0,-0.020 Q0.165,-0.035 0.175,0.215" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c(TIN["light"]))
    g = _lin(k, "pbk", TIN["light"], TIN["base"], TIN["dark"], -0.18, 0, 0.18, 0)
    o.append('<path d="M-0.185,0.215 L0.185,0.215 L0.150,0.510 Q0,0.535 -0.150,0.510 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.178,0.30 Q0,0.325 0.178,0.30 M-0.165,0.43 Q0,0.455 0.165,0.43" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(TIN["dark"]))
    o.append('<ellipse cx="0" cy="0.215" rx="0.185" ry="0.045" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c(TIN["dark"]), k.ink))
    if paint > 0.05:
        o.append('<ellipse cx="0" cy="%.4f" rx="%.4f" ry="0.032" fill="%s"/>' % (0.222 + 0.02 * (1 - paint), 0.165, k.c(pc["base"])))
        o.append('<path d="M-0.10,0.212 Q-0.02,0.200 0.06,0.208" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(pc["light"]))
        for (x, ln) in ((-0.13, 0.10), (-0.04, 0.17), (0.09, 0.07), (0.15, 0.13)):
            o.append('<path d="M%.4f,0.235 L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x, x * 0.97, 0.235 + ln, k.ink))
            o.append('<path d="M%.4f,0.235 L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x, x * 0.97, 0.235 + ln, k.c(pc["base"])))
    o.append('<circle cx="-0.180" cy="0.220" r="0.014" fill="%s" stroke="%s" stroke-width="0.006"/><circle cx="0.180" cy="0.220" r="0.014" fill="%s" stroke="%s" stroke-width="0.006"/>'
             % (k.c(TIN["light"]), k.ink, k.c(TIN["light"]), k.ink))
    return "".join(o)


BINO_SEP = 0.25           # barrel spacing
BINO_R = 0.112            # barrel radius


def _bino_body(k):
    """field glasses seen from the front (objectives towards the viewer), centred on (0, 0): two leather-covered barrels
    BINO_SEP apart, blue glass with a glint, the hinge bridge and the focus wheel."""
    o = []
    s2 = BINO_SEP / 2
    o.append('<rect x="%.4f" y="-0.060" width="%.4f" height="0.120" rx="0.04" fill="%s" stroke="%s" stroke-width="0.018"/>' % (-s2, BINO_SEP, k.c("#3a363e"), k.ink))
    o.append('<rect x="-0.030" y="-0.150" width="0.060" height="0.090" rx="0.015" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(TIN["base"]), k.ink))
    o.append('<path d="M-0.018,-0.140 L-0.018,-0.070 M0.0,-0.140 L0.0,-0.070 M0.018,-0.140 L0.018,-0.070" stroke="%s" stroke-width="0.006"/>' % k.c(TIN["dark"]))
    gl = '%s_bng' % k.uid
    k.defs.append('<radialGradient id="%s" cx="0.38" cy="0.35" r="0.75"><stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  % (gl, k.c(GLASS["light"]), k.c(GLASS["base"]), k.c(GLASS["dark"])))
    for sx in (-s2, s2):
        o.append('<circle cx="%.4f" cy="0" r="%.4f" fill="%s" stroke="%s" stroke-width="0.022"/>' % (sx, BINO_R, k.c("#2a272e"), k.ink))
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
                 % (sx - BINO_R * 0.75, -BINO_R * 0.45, BINO_R * 0.85, BINO_R * 0.85, sx - BINO_R * 0.15, -BINO_R * 0.85, k.c("#6a6670")))
        o.append('<circle cx="%.4f" cy="0" r="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (sx, BINO_R * 0.74, k.c(TIN["base"]), k.ink))
        o.append('<circle cx="%.4f" cy="0" r="%.4f" fill="url(#%s)" stroke="%s" stroke-width="0.010"/>' % (sx, BINO_R * 0.60, gl, k.ink))
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.85"/>'
                 % (sx - BINO_R * 0.38, -BINO_R * 0.12, BINO_R * 0.40, BINO_R * 0.40, sx - BINO_R * 0.08, -BINO_R * 0.40))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="#ffffff" opacity="0.9"/>' % (sx + BINO_R * 0.22, BINO_R * 0.22))
    return "".join(o)


# ============================================================================= hats (head frame)
def _cap_spots(k, pts, lev):
    o = []
    for i, (x, y, r) in enumerate(pts):
        if lev > 0.15 + 0.12 * i:
            o.append(_splat(k, x, y, r, PAINT["black"]["base"], 3.1 + 1.7 * i))
    return "".join(o)


def _hat_peaked10(k, C, yaw):
    """peaked naval cap: a wide flat crown (top ellipse + flaring sides), a dark band with a badge over the brow, a black
    peak curving over the eyes; braid=True: gold oak-leaf braid on the peak and a gold chin cord (the admiral).  Paint
    spots on the crown with pose paint_spots."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.12 * yaw
    tx = dx * 1.4 - 0.02 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    yb0, yb1 = -0.43, -0.27           # band top / bottom
    ytop = -0.62
    cr = dict(light=col["crown_l"], base=col["crown"], dark=col["crown_d"])
    g = CE._gradient(k, "pk", cr, x0=-0.64, x1=0.64, mid=0.34)
    # crown: sides flaring from the band to the top ellipse
    side = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" % (dx - 0.45, yb0 + 0.02, tx - 0.63, ytop + 0.02, tx, ytop + 0.16, tx + 0.63, ytop + 0.02,
                                                                        dx + 0.45, yb0 + 0.02)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (side, g, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.640" ry="0.115" fill="%s" stroke="%s" stroke-width="0.026"/>' % (tx, ytop, g, k.ink))
    o.append('<path d="M%.4f,%.4f A0.56,0.085 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
             % (tx - 0.50, ytop - 0.01, tx + 0.10, ytop - 0.08, k.c(cr["light"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (tx - 0.56, ytop + 0.07, tx, ytop + 0.20, tx + 0.56, ytop + 0.07, k.c(cr["dark"])))
    # band
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (dx - 0.46, yb0, fx, yb0 + 0.04, dx + 0.46, yb0, dx + 0.46, yb1, fx, yb1 + 0.04, dx - 0.46, yb1)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    if C.get("braid"):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (dx - 0.44, yb1 - 0.03, fx, yb1 + 0.01, dx + 0.44, yb1 - 0.03, k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (dx - 0.44, yb1 - 0.03, fx, yb1 + 0.01, dx + 0.44, yb1 - 0.03, k.c(GOLD["base"])))
        for sx in (-1, 1):
            o.append(_circ((dx + sx * 0.44, yb1 - 0.035), 0.022, k.c(GOLD["base"]), k, 0.008))
    # badge
    bx, by = fx, (yb0 + yb1) / 2 + 0.02
    if C.get("braid"):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
                 % (bx - 0.02, by + 0.07, bx - 0.13, by + 0.02, bx - 0.09, by - 0.09, bx + 0.02, by + 0.07, bx + 0.13, by + 0.02, bx + 0.09, by - 0.09, k.c(GOLD["base"])))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" stroke-dasharray="0.02 0.015"/>'
                 % (bx - 0.02, by + 0.07, bx - 0.13, by + 0.02, bx - 0.09, by - 0.09, bx + 0.02, by + 0.07, bx + 0.13, by + 0.02, bx + 0.09, by - 0.09, k.c(GOLD["dark"])))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.060" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx, by - 0.01, k.c(col["band"]), k.c(GOLD["dark"])))
        # small anchor
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
                 % (bx, by - 0.055, bx, by + 0.035, bx - 0.025, by - 0.035, bx + 0.025, by - 0.035, bx - 0.035, by + 0.005, bx, by + 0.050, bx + 0.035, by + 0.005, k.c(GOLD["light"])))
        o.append('<path d="M%.4f,%.4f l0.020,-0.030 l0.020,0.030 l0.020,-0.030 l0.020,0.030 l0.010,0.030 l-0.100,0 Z" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>'
                 % (bx - 0.050, by - 0.075, k.c(GOLD["base"]), k.ink))
    else:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.042" ry="0.040" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx, by - 0.005, k.c(col.get("badge", GOLD["base"])), k.ink))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.018" fill="%s"/>' % (bx, by - 0.005, k.c(col.get("badge_c", "#b8302a"))))
        o.append('<path d="M%.4f,%.4f q0.06,-0.04 0.12,0 M%.4f,%.4f q-0.06,-0.04 -0.12,0" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                 % (bx + 0.04, by - 0.07, bx - 0.04, by - 0.07, k.c(col.get("badge", GOLD["base"]))))
    # peak
    vis = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
           % (fx - 0.40, yb1 - 0.005, fx, yb1 + 0.04, fx + 0.40, yb1 - 0.005, fx + 0.30, yb1 + 0.13, fx, yb1 + 0.15, fx - 0.30, yb1 + 0.13, fx - 0.40, yb1 - 0.005))
    gv = CE._gradient(k, "pv", dict(light=col.get("visor_l", "#4a4652"), base=col["visor"], dark=col["visor"]), x0=-0.4, x1=0.4, mid=0.3)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (vis, gv, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.45"/>'
             % (fx - 0.26, yb1 + 0.06, fx - 0.10, yb1 + 0.10, fx + 0.06, yb1 + 0.10))
    if C.get("braid"):
        lv = []
        for i in range(9):
            t = i / 8.0
            x = fx - 0.32 + 0.64 * t
            y = yb1 + 0.11 + 0.035 * math.sin(math.pi * t)
            lv.append('<ellipse cx="%.4f" cy="%.4f" rx="0.034" ry="0.018" transform="rotate(%.1f %.4f %.4f)" fill="%s" stroke="%s" stroke-width="0.007"/>'
                      % (x, y, (-30 + 60 * t), x, y, k.c(GOLD["base"]), k.c(GOLD["deep"])))
        o.append("".join(lv))
    if _POSE10["spots"] > 0.02:
        o.append(_cap_spots(k, ((tx + 0.22, ytop + 0.02, 0.045), (tx - 0.30, ytop + 0.12, 0.035), (dx + 0.30, yb0 - 0.05, 0.030), (tx - 0.05, ytop - 0.03, 0.028)),
                            _POSE10["spots"]))
        o.append(_drip(k, dx + 0.30, yb0 - 0.02, 0.12 * _POSE10["spots"], 0.022, PAINT["black"]["base"]))
    o.append('</g>')
    C4._ext_hat(k, C, ((tx - 0.67, ytop), (tx + 0.67, ytop), (tx, ytop - 0.13), (fx - 0.40, yb1 + 0.13), (fx + 0.40, yb1 + 0.13)))
    return "".join(o), (tx, ytop - 0.115)


def _hat_dixie10(k, C, yaw):
    """sailor's white cap: a soft rounded crown and a thick rolled-up brim, tipped back on the head."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.08 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "dx", col, x0=-0.48, x1=0.48, mid=0.34)
    crown = [(dx - 0.40, -0.36), (dx - 0.38, -0.52), (dx - 0.22, -0.66), (dx, -0.69), (dx + 0.22, -0.66), (dx + 0.38, -0.52), (dx + 0.40, -0.36)]
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(crown), g, k.ink))
    o.append('<path d="M%.4f,-0.66 Q%.4f,-0.55 %.4f,-0.40" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (fx, fx + 0.03, fx + 0.02, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.50 Q%.4f,-0.62 %.4f,-0.645" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.9"/>' % (dx - 0.30, dx - 0.20, dx - 0.06))
    # rolled brim: a fat band, wider than the crown, its upper edge dipping in front
    brim = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.50, -0.42, fx, -0.36, dx + 0.50, -0.42, dx + 0.54, -0.33, dx + 0.47, -0.24, fx, -0.19, dx - 0.47, -0.24, dx - 0.54, -0.33, dx - 0.50, -0.42))
    gb = CE._gradient(k, "db", col, x0=-0.52, x1=0.52, mid=0.30)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (brim, gb, k.ink))
    o.append('<path d="M%.4f,-0.32 Q%.4f,-0.27 %.4f,-0.32" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.025 0.016" opacity="0.8"/>' % (dx - 0.44, fx, dx + 0.44, k.c(col["dark"])))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.52, -0.40), (dx + 0.52, -0.40), (dx, -0.71), (dx, -0.21)))
    return "".join(o), (dx, -0.70)


HATS10 = {"peaked10": _hat_peaked10, "dixie10": _hat_dixie10}


# ============================================================================= costumes (torso-local)
def _cos_overalls10(k, C, m):
    """the painter's whites: cast3/cast7 bib overalls in cream over a blue work shirt, splattered with black, white and grey paint."""
    inside, behind, over = CE.COSTUMES["overalls7"](k, C, m)
    X = _X(m)
    yB = TT + C["torso_h"]
    sp = []
    seed = C["seed"]
    for i in range(14):
        a, b = _hash(seed, i), _hash(seed, i + 50)
        x = -0.30 + 0.60 * a
        y = 0.62 + (yB - 0.62) * b
        r = 0.016 + 0.022 * _hash(seed, i + 90)
        cc = ("black", "black", "grey", "black", "white")[i % 5]
        sp.append(_splat(k, X(x, y)[0], y, r, PAINT[cc]["base"], seed + i, op=0.92))
    sp.append(_drip(k, X(-0.12, 0.66)[0], 0.66, 0.10, 0.020, PAINT["black"]["base"]))
    sp.append(_drip(k, X(0.15, 0.80)[0], 0.80, 0.14, 0.018, PAINT["grey"]["base"]))
    return inside + "".join(sp), behind, over


def _cos_admiral10(k, C, m):
    """the admiral's navy double-breasted coat: wide peaked lapels over a white shirt and black tie, two rows of gold buttons
    converging down the belly, medal ribbons on the chest, gold-edged pocket flaps; the coat skirt to above the knee."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    gold = k.c(GOLD["base"])
    o = []
    # shirt + tie in the neck V
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (X(-0.20, 0.38) + X(0.20, 0.38) + X(0.0, 0.70) + (k.c(col["shirt"]), k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (X(-0.035, 0.42) + X(0.035, 0.42) + X(0.03, 0.62) + X(-0.03, 0.62) + (k.c(col["tie"]), k.ink)))
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(s * 0.03, 0.385) + X(s * 0.17, 0.38) + X(s * 0.06, 0.47) + (k.c(col["shirt"]), k.ink)))
    # lapels (peaked)
    for s in (-1, 1):
        lp = [X(s * 0.20, 0.37), X(s * 0.36, 0.40), X(s * 0.42, 0.50), X(s * 0.30, 0.54), X(s * 0.34, 0.62), X(s * 0.06, 0.80), X(s * 0.03, 0.72)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["lapel"]), k.ink))
    # front edge of the overlapping breast (double-breasted: off-centre)
    o.append(_ln([X(0.06, 0.80), X(0.10, yB + 0.02)], k.ink, 0.016))
    # two rows of gold buttons converging downwards
    for i, y in enumerate((0.80, 0.98, 1.16, 1.34)):
        if y > yB - 0.06:
            break
        sx = (0.30 - 0.03 * i) * min(1.0, hw / 0.70)
        for s in (-1, 1):
            c = X(s * sx + 0.02, y)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.038" fill="%s" stroke="%s" stroke-width="0.012"/>' % (c[0], c[1], gold, k.ink))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.013" fill="%s"/>' % (c[0] - 0.010, c[1] - 0.010, k.c(GOLD["light"])))
    # medal ribbons (screen-left chest)
    rb = (("#c8302a", "#ffffff", "#2a4a9a"), ("#f0c040", "#2a7a4a", "#f0c040"), ("#6a2a8a", "#ffffff", "#6a2a8a"))
    x0, y0 = X(-0.56 * min(1.0, hw / 0.70) - 0.02, 0.64)
    for j, cs in enumerate(rb):
        xx = x0 + j * 0.085
        o.append('<rect x="%.4f" y="%.4f" width="0.080" height="0.055" fill="%s" stroke="%s" stroke-width="0.010"/>' % (xx, y0, k.c(cs[0]), k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.020" height="0.055" fill="%s"/>' % (xx + 0.030, y0, k.c(cs[1])))
    # pocket flaps
    for s in (-1, 1):
        px = s * 0.48 * min(1.0, hw / 0.70)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(px - 0.13, yB - 0.20) + X(px + 0.13, yB - 0.20) + X(px + 0.12, yB - 0.13) + X(px - 0.12, yB - 0.13) + (k.c(col["dark"]), k.ink)))
    inside = "".join(o)
    # coat skirt
    yt = yB - 0.12
    a = hw * 0.985
    hem = yB + C.get("coat_len", 0.40)
    b = hw + C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "ad", X, yt, a, hem, b, g, sw=0.026, folds=((-0.10, yt + 0.16, -0.16, hem - 0.04), (0.30, yt + 0.16, 0.36, hem - 0.04)),
                    fold_col=k.c(col["dark"]))]
    ov.append(_ln([X(0.10, yt), X(0.14, hem - 0.01)], k.ink, 0.016))
    return inside, "", "".join(ov)


def _cos_sailor10(k, C, m):
    """naval rating: white jumper, a big blue square collar with three white tapes, black silk knotted at the V with a white
    tape bow; navy trousers showing at the hips."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    nv = k.c(col["collar"])
    o = [CE._bowl(k, col["pants"], yB - 0.07, yB, dip=0.02)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (X(-0.45, yB - 0.10) + X(0.0, yB - 0.08) + X(0.45, yB - 0.10) + (k.c(col["dark"]),)))
    for s in (-1, 1):
        cl = [X(s * 0.40, 0.34), X(s * 0.40, 0.52), X(s * 0.02, 0.86), X(s * 0.02, 0.70), X(s * 0.15, 0.42), X(s * 0.15, 0.34)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(cl), nv, k.ink))
        for off in (0.030, 0.056, 0.082):
            o.append(_ln([X(s * (0.40 - off), 0.50 + off * 0.10), X(s * (0.03 + off * 0.45), 0.86 - off * 1.35)], k.c(col["tape"]), 0.011))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (X(-0.15, 0.40) + X(0.15, 0.40) + X(0.0, 0.70) + (k.c(col["base"]), k.ink)))
    o.append(_ln([X(-0.12, 0.47), X(0.12, 0.47)], k.c(col["collar"]), 0.016))
    # black silk + white tape bow
    c = X(0.0, 0.80)
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (c[0] + s * 0.012, c[1], c[0] + s * 0.050, c[1] + 0.170, c[0] + s * 0.005, c[1] + 0.150, k.c(col["silk"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.034" fill="%s" stroke="%s" stroke-width="0.012"/>' % (c[0], c[1], k.c(col["silk"]), k.ink))
    o.append('<path d="M%.4f,%.4f q-0.05,-0.03 -0.06,0.01 q0.03,0.02 0.06,-0.01 q0.05,-0.03 0.06,0.01 q-0.03,0.02 -0.06,-0.01 Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
             % (c[0], c[1] + 0.005, k.c(col["tape"]), k.ink))
    return "".join(o), "", ""


def _cos_ucoat10(k, C, m):
    """U-boat captain: a dark grey leather coat, double-breasted, wide lapels open on a white roll-neck sweater, a belt with a
    steel buckle; the coat skirt to mid-shin, leather sheen."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (X(-0.22, 0.34) + X(0.0, 0.44) + X(0.22, 0.34) + X(0.16, 0.66) + X(0.0, 0.72) + X(-0.16, 0.66) + (k.c(col["sweater"]), k.ink)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>'
             % (X(-0.18, 0.38) + X(0.0, 0.47) + X(0.18, 0.38) + X(-0.17, 0.43) + X(0.0, 0.52) + X(0.17, 0.43) + (k.c(col["sweater_d"]),)))
    for s in (-1, 1):
        lp = [X(s * 0.20, 0.36), X(s * 0.38, 0.40), X(s * 0.44, 0.54), X(s * 0.30, 0.60), X(s * 0.18, 0.86), X(s * 0.14, 0.66)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["lapel"]), k.ink))
    o.append(_ln([X(0.18, 0.86), X(0.20, yB + 0.02)], k.ink, 0.016))
    for y in (0.92, 1.10):
        for s in (-1, 1):
            o.append(_circ(X(s * 0.24 + 0.02, y), 0.030, k.c(col["button"]), k, 0.010))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.030" stroke-linecap="round" opacity="0.18"/>'
             % (X(-0.42, 0.62) + X(-0.48, 0.90) + X(-0.40, yB - 0.10)))
    inside = "".join(o)
    yt = yB - 0.12
    a = hw * 0.985
    hem = yB + C.get("coat_len", 0.62)
    b = hw + C.get("coat_flare", 0.12)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "uc", X, yt, a, hem, b, g, sw=0.026, folds=((-0.12, yt + 0.16, -0.18, hem - 0.04), (0.34, yt + 0.16, 0.40, hem - 0.04)),
                    fold_col=k.c(col["dark"]))]
    ov.append(_ln([X(0.20, yt), X(0.24, hem - 0.01)], k.ink, 0.016))
    yw = yB - 0.16
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.03) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.110"/>' % (band, k.ink))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.080"/>' % (band, k.c(col["belt"])))
    bx, by = X(0.04, yw + 0.03)
    ov.append('<rect x="%.4f" y="%.4f" width="0.110" height="0.090" rx="0.012" fill="none" stroke="%s" stroke-width="0.034"/>' % (bx - 0.055, by - 0.045, k.ink))
    ov.append('<rect x="%.4f" y="%.4f" width="0.110" height="0.090" rx="0.012" fill="none" stroke="%s" stroke-width="0.018"/>' % (bx - 0.055, by - 0.045, k.c(TIN["light"])))
    return inside, "", "".join(ov)


COSTUMES10 = {"overalls10": _cos_overalls10, "admiral10": _cos_admiral10, "sailor10": _cos_sailor10, "ucoat10": _cos_ucoat10}


# ============================================================================= limbs: epaulettes, splattered trousers
def _epaulette(k, S, E, C):
    """gold epaulette on top of the shoulder: an oval board with a navy centre and a silver star, a thick bullion fringe
    hanging along the upper arm."""
    ang = math.degrees(math.atan2(E[1] - S[1], E[0] - S[0]))
    sz = C.get("epaulette10", 1.0)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (S[0], S[1], ang, sz)]
    fr = []
    for j in range(7):
        y = -0.105 + 0.035 * j
        fr.append("M0.04,%.4f L0.20,%.4f" % (y, y * 1.12))
    o.append('<path d="%s" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (" ".join(fr), k.ink))
    o.append('<path d="%s" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (" ".join(fr), k.c(GOLD["base"])))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>' % (" ".join(fr), k.c(GOLD["light"])))
    o.append('<ellipse cx="0.0" cy="0" rx="0.085" ry="0.135" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(GOLD["base"]), k.ink))
    o.append('<ellipse cx="0.0" cy="0" rx="0.050" ry="0.092" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(C["colors"].get("base", "#1e2a4a")), k.c(GOLD["dark"])))
    o.append('<circle cx="0.0" cy="0" r="0.020" fill="%s"/>' % k.c("#e8ecf0"))
    o.append('</g>')
    for (x, y) in ((-0.10, 0.0), (0.24, -0.14), (0.24, 0.14), (0.0, -0.15), (0.0, 0.15)):
        q = _rot(x * sz, y * sz, ang)
        k.ext.append((S[0] + q[0], S[1] + q[1], 0.03))
    return "".join(o)


def _leg_splat(k, S, E, H, C):
    o = []
    seed = C["seed"] + 7.0 * (S[0] > 0)
    for i in range(6):
        t = 0.10 + 0.80 * _hash(seed, i)
        if t < 0.5:
            u = t / 0.5
            x, y = S[0] + (E[0] - S[0]) * u, S[1] + (E[1] - S[1]) * u
        else:
            u = (t - 0.5) / 0.5
            x, y = E[0] + (H[0] - E[0]) * u, E[1] + (H[1] - E[1]) * u
        x += (_hash(seed, i + 9) - 0.5) * 0.06
        cc = ("black", "grey", "black", "white", "black", "grey")[i]
        o.append(_splat(k, x, y, 0.014 + 0.012 * _hash(seed, i + 3), PAINT[cc]["base"], seed + i, op=0.92))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O10["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast10"):
        return out
    if tail is None and C.get("epaulette10"):
        out += _epaulette(k, S, E, C)
    if tail is not None and C.get("splat10"):
        out += _leg_splat(k, S, E, H, C)
    return out


# ============================================================================= hands: white gloves
def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    out = _O10["_hand"](k, H, dirv, shape, hr, fold)
    C = CE._CUR[0]
    if not C or not C.get("gloves10"):
        return out
    col = C["gloves10"]
    return out + ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="#ffffff" '
                  'stroke-width="%.4f" stroke-linecap="round" opacity="0.9"/>'
                  % (H[0], H[1], hr - 0.020, k.c(col), H[0] - hr * 0.55, H[1] - hr * 0.05, hr * 0.55, hr * 0.55, H[0] - hr * 0.10, H[1] - hr * 0.55, 0.014))


# ============================================================================= face: walrus moustache, paint spots
def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "walrus10":
        return _O10["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#f4f2ee")
    sh = C["colors"].get("moustache_l", "#c4c0c8")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    pts = [Q(0.0, -0.060), Q(-0.10, -0.085), Q(-0.22, -0.070), Q(-0.32, -0.010), Q(-0.36, 0.080), Q(-0.34, 0.170), Q(-0.29, 0.205), Q(-0.26, 0.150),
           Q(-0.21, 0.175), Q(-0.17, 0.110), Q(-0.10, 0.100), Q(-0.04, 0.060), Q(0.0, 0.070), Q(0.04, 0.060), Q(0.10, 0.100), Q(0.17, 0.110),
           Q(0.21, 0.175), Q(0.26, 0.150), Q(0.29, 0.205), Q(0.34, 0.170), Q(0.36, 0.080), Q(0.32, -0.010), Q(0.22, -0.070), Q(0.10, -0.085)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)]
    st = []
    for x in (-0.28, -0.20, -0.12, -0.05, 0.05, 0.12, 0.20, 0.28):
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (Q(x * 0.75, -0.05) + Q(x * 1.05, 0.03) + Q(x * 1.10, 0.11 + 0.03 * abs(x) / 0.28)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % ("".join(st), k.c(sh)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (Q(0.0, -0.055) + Q(0.0, 0.020) + (k.ink,)))
    k.ext.append(Q(-0.37, 0.21) + (0.03,))
    k.ext.append(Q(0.37, 0.21) + (0.03,))
    return "".join(o)


def _paint_face(k, L, lev):
    """black paint spots on the cheeks, forehead, nose and moustache, a run down one cheek."""
    o = []
    spots = ((L["xL"] - 0.10, L["ey"] + 0.13, 0.034), (L["xR"] + 0.06, L["ey"] - 0.20, 0.028), (L["mx"] + 0.17, L["my"] - 0.04, 0.030),
             (L["mx"] - 0.20, L["my"] + 0.02, 0.026), ((L["xL"] + L["xR"]) / 2 + 0.01, L["ey"] + 0.08, 0.020), (L["xR"] + 0.14, L["ey"] + 0.10, 0.022))
    for i, (x, y, r) in enumerate(spots):
        if lev > 0.10 + 0.13 * i:
            o.append(_splat(k, x, y, r, PAINT["black"]["base"], 11.3 + 2.1 * i))
    if lev > 0.5:
        o.append(_drip(k, L["xL"] - 0.10, L["ey"] + 0.15, 0.10 * lev, 0.020, PAINT["black"]["base"]))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O10["_face"](k, C, P_, white)
    if C is None or not C.get("_cast10"):
        return svg, L
    if _POSE10["spots"] > 0.02:
        svg = svg + _paint_face(k, L, _POSE10["spots"])
    return svg, L


# ============================================================================= props held in the hand
NEW_PROPS10 = ("bigbrush", "paint_bucket", "binoculars")
NEW_TIP10 = {"bigbrush": BRUSH_TIP, "paint_bucket": 0.52, "binoculars": 0.30}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS10:
        return _O10["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    if kind == "paint_bucket":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _bucket_body(k, _POSE10["bucket"], _POSE10["bcol"]))
        for (x, y) in ((-0.19, 0.20), (0.19, 0.20), (-0.16, 0.54), (0.16, 0.54), (0.0, -0.04)):
            k.ext.append((H[0] + x * sc, H[1] + y * sc, 0.03))
        tip = (H[0], H[1] + 0.52 * sc)
        an["bucket_bottom_" + key] = tip
        return o, tip
    if kind == "binoculars":
        # the hand grips the outer barrel from below; the glasses face the viewer, upright whatever the arm angle
        c1 = (H[0] - side * 0.050 * sc, H[1] - 0.075 * sc)
        cx = c1[0] - side * BINO_SEP / 2 * sc
        cy = c1[1]
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (cx, cy, sc, _bino_body(k))
        for (x, y) in ((-BINO_SEP / 2 - BINO_R, 0.0), (BINO_SEP / 2 + BINO_R, 0.0), (0.0, -0.16), (-BINO_SEP / 2, BINO_R), (BINO_SEP / 2, BINO_R)):
            k.ext.append((cx + x * sc, cy + y * sc, 0.03))
        an["binoc_" + key] = (cx, cy)
        an["grip_far_" + key] = (cx - side * (BINO_SEP / 2 + 0.050) * sc, cy + 0.075 * sc)
        return o, (cx, cy)
    # bigbrush
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _brush_body(k, _POSE10["brush"], _POSE10["bcol"]))
    for e in ((-0.60, 0.0), (0.72, -0.13), (0.72, 0.13), (1.03, -0.14), (1.03, 0.14)):
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(BRUSH_TIP * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    gx, gy = _rot(BRUSH_GRIP2 * sc, 0.0, ang)
    an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
    an["brush_" + key] = tip
    if _POSE10["brush"] > 0.3:
        pc = PAINT.get(_POSE10["bcol"], PAINT["black"])
        # drips falling from the lowest bristle corner (screen down), animated by t
        lo = max(((1.02, -0.13), (1.02, 0.13), (1.03, 0.0)), key=lambda p: _rot(p[0], p[1], ang)[1])
        ex, ey = _rot(lo[0] * sc, lo[1] * sc, ang)
        x0, y0 = H[0] + ex, H[1] + ey
        o += '<path d="M%.4f,%.4f q-0.016,0.05 0,0.075 q0.016,-0.025 0,-0.075 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x0, y0 - 0.005, k.c(pc["base"]), k.ink)
        for j in range(2):
            f = (_POSE10["t"] * 1.4 + 0.5 * j) % 1.0
            yy = y0 + 0.08 + 0.32 * f
            o += ('<path d="M%.4f,%.4f q-0.022,0.04 0,0.058 q0.022,-0.018 0,-0.058 Z" fill="%s" stroke="%s" stroke-width="0.007" opacity="%.3f"/>'
                  % (x0, yy, k.c(pc["base"]), k.ink, 1.0 - f * f))
        k.ext.append((x0, y0 + 0.46, 0.03))
    return o, tip


# ============================================================================= plank, periscope (figure level)
def _plank_svg(k, cx, y, w, rope):
    """a hanging painter's plank: a thick board w wide whose top surface is at y (the soles stand on it), seen a little from
    above; two hemp ropes from holes near its ends rise rope D; paint drips on its edge."""
    o = []
    x0, x1 = cx - w / 2, cx + w / 2
    th, top = 0.13, 0.07
    rx = (x0 + 0.14, x1 - 0.14)
    for x in rx:
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (x, y - rope, x, y - top * 0.5, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x, y - rope, x, y - top * 0.5, k.c(ROPE["base"])))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>'
                 % ("".join("M%.4f,%.4f l0.012,0.030 " % (x - 0.006, y - rope + 0.05 * i) for i in range(int(rope / 0.05))), k.c(ROPE["dark"])))
    gt = _lin(k, "plt", PLANK["light"], PLANK["base"], PLANK["dark"], x0, 0, x1, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (x0 + 0.04, y - top, x1 - 0.04, y - top, x1, y, x0, y, gt, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.012" fill="%s" stroke="%s" stroke-width="0.022"/>' % (x0, y, w, th, k.c(PLANK["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
             % (x0 + 0.06, y + th * 0.45, x0 + w * 0.42, y + th * 0.45, x0 + w * 0.55, y + th * 0.65, x0 + w * 0.70, y + th * 0.50, x1 - 0.06, y + th * 0.62, k.c(PLANK["deep"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>' % (x0 + 0.08, y - top * 0.5, x1 - 0.08, y - top * 0.5, k.c(PLANK["light"])))
    for x in rx:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.020" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x, y - top * 0.5, k.c(PLANK["deep"]), k.ink))
        o.append('<path d="M%.4f,%.4f q0.05,0.04 0.0,0.09 q-0.05,-0.05 0,-0.09" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x, y + th * 0.2, k.c(ROPE["base"]), k.ink))
    # paint on the plank
    o.append(_splat(k, x0 + w * 0.22, y - top * 0.45, 0.030, PAINT["black"]["base"], 5.5))
    o.append(_splat(k, x0 + w * 0.80, y - top * 0.40, 0.026, PAINT["white"]["base"], 8.1))
    o.append(_drip(k, x0 + w * 0.30, y + th - 0.01, 0.09, 0.022, PAINT["black"]["base"]))
    o.append(_drip(k, x0 + w * 0.66, y + th - 0.01, 0.06, 0.020, PAINT["black"]["base"]))
    return "".join(o), (x0 - 0.02, y - rope - 0.03, x1 + 0.02, y + th + 0.12)


def _scope_parts(k, cx, top, bottom, hy, eye, near_l):
    """the periscope: a steel column (cx, from top to bottom), a training-handle bar across it at hy with grips at both ends,
    and the eyepiece box reaching from the column to the eye (drawn separately, over the face).  near_l: the eye is left of
    the column.  Returns (behind svg, eyepiece svg, bbox)."""
    w = 0.36
    g = _lin(k, "psc", STEEL["light"], STEEL["base"], STEEL["dark"], cx - w / 2, 0, cx + w / 2, 0)
    b = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.024"/>' % (cx - w / 2, top, w, bottom - top, g, k.ink)]
    b.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.35"/>' % (cx - w * 0.28, top + 0.03, cx - w * 0.28, bottom - 0.03))
    for y in (top + 0.25, eye[1] - 0.24, hy + 0.30, bottom - 0.30):
        if top < y < bottom:
            b.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.060" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (cx - w / 2 - 0.025, y, w + 0.05, k.c(STEEL["dark"]), k.ink))
            b.append('<circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>' % (cx - w * 0.30, y + 0.030, k.c(STEEL["light"]), cx + w * 0.30, y + 0.030, k.c(STEEL["light"])))
    # handle bar with grips (in front of the figure: returned with the eyepiece)
    hl = 0.36
    e = []
    e.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.060" rx="0.020" fill="%s" stroke="%s" stroke-width="0.018"/>' % (cx - w / 2 - hl, hy - 0.030, w + 2 * hl, k.c(STEEL["light"]), k.ink))
    for s in (-1, 1):
        gx = cx + s * (w / 2 + hl - 0.02)
        e.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.150" rx="0.025" fill="%s" stroke="%s" stroke-width="0.016"/>' % (gx - 0.030, hy - 0.075, k.c("#2a2628"), k.ink))
    # eyepiece box from the column to the eye
    sd = -1.0 if near_l else 1.0
    ex0 = cx + sd * w / 2
    ex1 = eye[0] - sd * 0.08
    ey = eye[1]
    e.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (ex0, ey - 0.15, ex1, ey - 0.10, ex1, ey + 0.10, ex0, ey + 0.15, k.c(STEEL["light"]), k.ink))
    e.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.35"/>' % (ex0, ey - 0.08, ex1, ey - 0.055))
    cup = P._smooth_closed([(ex1 - sd * 0.02, ey - 0.10), (ex1 + sd * 0.08, ey - 0.12), (ex1 + sd * 0.14, ey - 0.06), (ex1 + sd * 0.14, ey + 0.06), (ex1 + sd * 0.08, ey + 0.12), (ex1 - sd * 0.02, ey + 0.10)])
    e.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (cup, k.c("#26222a"), k.ink))
    e.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (ex1 + sd * 0.05, ey - 0.09, ex1 + sd * 0.11, ey - 0.07, ex1 + sd * 0.12, ey - 0.01, k.c("#5a5660")))
    bb = (min(cx - w / 2 - hl - 0.05, ex1 - 0.18), top - 0.03, max(cx + w / 2 + hl + 0.05, ex1 + 0.18), bottom + 0.03)
    return "".join(b), "".join(e), bb


PLANK_W, PLANK_ROPE = 2.40, 3.90
SCOPE_DX = 0.44            # column centre from the eye at the eyepiece
SCOPE_GRIP = 0.52          # grips from the column centre
SCOPE_TOP = -1.30          # periscope column top, head frame (y of the head centre = 0)


def figure(cast_name, pose=None, uid="p"):
    f = _O10["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    pl = _f(pose.get("plank"), 0.0, 0.0, 1.0)
    sc = _f(pose.get("periscope"), 0.0, 0.0, 1.0)
    if pl < 0.5 and sc < 0.5:
        return f
    k = P._Ctx(uid + "x", P.INK, None)
    behind, front = [], []
    b = list(f["bbox"])
    an = dict(f["anchors"])
    if pl >= 0.5:
        w = _f(pose.get("plank_w"), PLANK_W, 1.0, 4.0)
        rope = _f(pose.get("plank_rope"), PLANK_ROPE, 0.3, 6.0)
        s, bb = _plank_svg(k, an["feet"][0], f["feet_y"], w, rope)
        behind.append(s)
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["plank_l"] = (an["feet"][0] - w / 2, f["feet_y"])
        an["plank_r"] = (an["feet"][0] + w / 2, f["feet_y"])
    if sc >= 0.5:
        hr_, hl_ = an["hand_r"], an["hand_l"]
        mir = bool(pose.get("mirror"))
        # the eye pressed to the eyepiece: the one on the column side
        eye = an["eye_l"] if mir else an["eye_r"]
        cx = eye[0] + (-SCOPE_DX if mir else SCOPE_DX)
        near_l = not mir
        hy = min((hr_, hl_), key=lambda h: abs(abs(h[0] - cx) - SCOPE_GRIP))[1]
        sb, se, bb = _scope_parts(k, cx, SCOPE_TOP, f["feet_y"] + 0.02, hy, eye, near_l)
        behind.append(sb)
        front.append(se)
        # the hands grip the bar: redraw them over it (ink balls, gloves if any)
        hr = P.HAND_R * (_num(P.CAST[cast_name].get("limb_w"), P.LW) / P.LW) ** 0.75
        for hh in (hr_, hl_):
            if abs(hh[1] - hy) < 0.12 and abs(abs(hh[0] - cx) - SCOPE_GRIP) < 0.15:
                front.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#b7a9b3" opacity="0.7"/>'
                             % (hh[0], hh[1], hr, P.INK, hh[0] - 0.34 * hr, hh[1] - 0.40 * hr, 0.15 * hr, 0.095 * hr))
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["scope_eye"] = eye
        an["scope_top"] = (cx, SCOPE_TOP)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + "".join(behind) + f["svg"] + "".join(front), bbox=tuple(b), anchors=an)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE10["spots"] = _f(g("paint_spots"), 0.0, 0.0, 1.0)
    _POSE10["brush"] = _f(g("brush_paint"), 1.0, 0.0, 1.0)
    _POSE10["bucket"] = _f(g("bucket_paint"), 1.0, 0.0, 1.0)
    bc = g("brush_col")
    _POSE10["bcol"] = bc if isinstance(bc, str) and bc in PAINT else "black"
    t = _num(g("t"), 0.0)
    _POSE10["t"] = t if math.isfinite(t) else 0.0
    return _O10["_norm"](C, pose)


# ============================================================================= standalone pieces
def bigbrush_svg(uid="bb", paint=1.0, col="black", ink=P.INK, tint=None):
    """the big wall brush along +x (hand at (0, 0)), bristle ends at x 1.02, other-hand grip at x -0.42."""
    k = _ctx(uid, ink, tint)
    s = _brush_body(k, _clamp(_num(paint, 1.0), 0.0, 1.0), col if col in PAINT else "black")
    return '<g id="%s_brush"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def paint_bucket_svg(uid="pb", paint=1.0, col="black", ink=P.INK, tint=None):
    """the painter's pail hanging from its bail (bail top at (0, 0), bottom at y 0.52)."""
    k = _ctx(uid, ink, tint)
    s = _bucket_body(k, _clamp(_num(paint, 1.0), 0.0, 1.0), col if col in PAINT else "black")
    return '<g id="%s_bucket"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def binoculars_svg(uid="bn", ink=P.INK, tint=None):
    """the field glasses from the front, centred on (0, 0) (barrels at x +-0.125)."""
    k = _ctx(uid, ink, tint)
    s = _bino_body(k)
    return '<g id="%s_bino"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def plank_svg(uid="pl", w=PLANK_W, rope=PLANK_ROPE, ink=P.INK, tint=None):
    """the hanging plank alone: top surface centred on (0, 0), ropes rising rope D.  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    s, bb = _plank_svg(k, 0.0, 0.0, _clamp(_num(w, PLANK_W), 0.5, 6.0), _clamp(_num(rope, PLANK_ROPE), 0.1, 8.0))
    return '<g id="%s_plank"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


def periscope_svg(uid="ps", top=-2.0, bottom=2.0, handle_y=0.3, eye=(-0.36, 0.0), ink=P.INK, tint=None):
    """the periscope column centred on x 0 from top to bottom with the handle bar at handle_y and the eyepiece reaching to
    eye (left of the column when eye x < 0).  Returns svg."""
    k = _ctx(uid, ink, tint)
    near_l = _num(eye[0], -0.36) < 0
    b, e, bb = _scope_parts(k, 0.0, _num(top, -2.0), _num(bottom, 2.0), _num(handle_y, 0.3), (_num(eye[0], -0.36), _num(eye[1], 0.0)), near_l)
    return '<g id="%s_scope"><defs>%s</defs>%s%s</g>' % (k.uid, "".join(k.defs), b, e)


# ============================================================================= cast
_FLAGS = dict(_cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)
ADM_CAP = dict(crown="#1e2848", crown_l="#3e4a72", crown_d="#10162a", band="#14182a", visor="#16141a", visor_l="#4a4652")
NEW_CAST10 = {
    # Norman, the marine painter: lean, a dark navy beret flopped to one side, a small dark moustache, a blue work shirt with
    # the sleeves rolled up, painter's cream bib overalls splattered with black, white and grey paint, brown boots
    "painter10": dict(
        _FLAGS, build="slim", seed=104.7,
        torso_w=0.62, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.76, hip_x=0.15, leg=1.34, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.040, brow="stroke", brow_th=0.058, mouth="smirk", moustache=True, moustache_style="bushy", tache_scale=0.62, smirk_side=1,
        cheeks="#eaa08a", hat="newsboy", hat_style="beret7", hat_tilt=-9.0, beret_side=-1, ear_pencil=False,
        hat_colors=dict(light="#4a5470", base="#2a3048", dark="#161a2a", shine="#6a7698"),
        hair=dict(color="#4a3226", front=0.08, grow=0.22),
        costume="overalls10", splat10=True,
        sleeve=dict(color="#7aa0cc", cuff="#9ab8dc", dark="#4e72a0", len=0.50, roll=True, w=0.14),
        shorts=dict(color="#ece4d0", dark="#bdb196", cuff="#ece4d0", len=0.90, w=0.13),
        boots=dict(color="#4a3428", cuff="#4a3428", h=0.10, toe=0.15),
        colors=dict(base="#7aa0cc", collar="#9ab8dc", denim="#ece4d0", denim_d="#cfc4aa", stitch="#a89878", brass="#c8a04a", pencil="#2a2630",
                    pants="#ece4d0", moustache="#3a2620", moustache_l="#6a4a3a"),
    ),
    # the admiral: big belly, navy double-breasted coat with gold buttons, gold epaulettes, medal ribbons, navy cap with gold
    # braid and an anchor badge, a huge white walrus moustache, white hair, ruddy cheeks, double chin
    "admiral": dict(
        _FLAGS, build="stout", seed=77.2,
        torso_w=1.48, torso_h=1.28, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.28, stance=0.07, wide=0.32, limb_w=0.070,
        eye_y=0.000, brow="stroke", brow_th=0.085, mouth="frown", moustache=True, moustache_style="walrus10", tache_scale=1.0,
        smirk_side=1, cheeks="#ee7a68", chins=True, epaulette10=1.15, age_lines=True, gloves10="#f4f2ee",
        hat="newsboy", hat_style="peaked10", hat_tilt=-3.0, ear_pencil=False, braid=True,
        hat_colors=dict(ADM_CAP),
        hair=dict(color="#e8e4ea", front=0.06, grow=0.20),
        costume="admiral10", coat_len=0.40, coat_flare=0.10,
        sleeve=dict(color="#2e3f70", dark="#18223e", cuff="#e2b442", len=0.84, w=0.210),
        shorts=dict(color="#1e2a4a", dark="#121a32", cuff="#1e2a4a", len=0.90, w=0.16),
        boots=dict(color="#16141a", cuff="#16141a", h=0.08, toe=0.18),
        colors=dict(base="#24325a", dark="#121a32", lapel="#1a2442", shirt="#fbfaf6", tie="#16141a", pants="#1e2a4a",
                    moustache="#f6f4f0", moustache_l="#c4c0ca"),
    ),
    # the sailors: white caps, white jumpers with blue square collars, black silk, navy bell-bottoms.  a: tall and thin;
    # b: round, bushy brown moustache; c: short, freckled, ginger
    "sailor_a": dict(
        _FLAGS, build="slim", seed=31.9,
        torso_w=0.62, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.76, hip_x=0.14, leg=1.36, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.030, brow="stroke", brow_th=0.052, mouth="dash", moustache=False, smirk_side=-1, cheeks="#eca090",
        hat="newsboy", hat_style="dixie10", hat_tilt=-10.0, ear_pencil=False,
        hat_colors=dict(light="#ffffff", base="#f2f2ee", dark="#bcbcb6"),
        hair=dict(color="#2a221e", front=0.08, grow=0.20),
        costume="sailor10",
        sleeve=dict(color="#f2f2ee", dark="#c4c4be", cuff="#24366b", len=0.84, w=0.150),
        shorts=dict(color="#24366b", dark="#141e40", cuff="#24366b", len=0.92, w=0.15),
        boots=dict(color="#16141a", cuff="#16141a", h=0.06, toe=0.14),
        colors=dict(base="#f2f2ee", dark="#c4c4be", collar="#24366b", tape="#ffffff", silk="#16141a", pants="#24366b"),
    ),
    "sailor_b": dict(
        _FLAGS, build="regular", seed=58.3,
        torso_w=0.94, torso_h=0.96, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.32, 0.47), arm=0.72, hip_x=0.16, leg=1.06, stance=0.06, wide=0.27, limb_w=0.062,
        eye_y=0.010, brow="stroke", brow_th=0.064, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=1, cheeks="#ee8a78",
        hat="newsboy", hat_style="dixie10", hat_tilt=8.0, ear_pencil=False,
        hat_colors=dict(light="#ffffff", base="#f2f2ee", dark="#bcbcb6"),
        hair=dict(color="#5a3a26", front=0.06, grow=0.20),
        costume="sailor10",
        sleeve=dict(color="#f2f2ee", dark="#c4c4be", cuff="#24366b", len=0.84, w=0.165),
        shorts=dict(color="#24366b", dark="#141e40", cuff="#24366b", len=0.92, w=0.16),
        boots=dict(color="#16141a", cuff="#16141a", h=0.06, toe=0.15),
        colors=dict(base="#f2f2ee", dark="#c4c4be", collar="#24366b", tape="#ffffff", silk="#16141a", pants="#24366b", moustache="#5a3a26"),
    ),
    "sailor_c": dict(
        _FLAGS, build="slim", seed=12.4,
        torso_w=0.64, torso_h=0.86, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.70, hip_x=0.14, leg=1.06, stance=0.07, wide=0.26, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.040, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a294", freckles=True,
        hat="newsboy", hat_style="dixie10", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#ffffff", base="#f2f2ee", dark="#bcbcb6"),
        hair=dict(color="#c8642a", front=0.10, grow=0.22),
        costume="sailor10",
        sleeve=dict(color="#f2f2ee", dark="#c4c4be", cuff="#24366b", len=0.84, w=0.140),
        shorts=dict(color="#24366b", dark="#141e40", cuff="#24366b", len=0.92, w=0.14),
        boots=dict(color="#16141a", cuff="#16141a", h=0.06, toe=0.13),
        colors=dict(base="#f2f2ee", dark="#c4c4be", collar="#24366b", tape="#ffffff", silk="#16141a", pants="#24366b"),
    ),
    # the U-boat captain: grey peaked cap with a small cockade, short dark beard + moustache, dark grey leather coat over a
    # white roll-neck, black boots
    "uboat_captain": dict(
        _FLAGS, build="regular", seed=43.8,
        torso_w=0.86, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.31, 0.48), arm=0.74, hip_x=0.15, leg=1.16, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.070, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.80, smirk_side=-1, cheeks="#e48a7a",
        beard=dict(color="#4a3a30", dark="#2a201a"),
        hat="newsboy", hat_style="peaked10", hat_tilt=4.0, ear_pencil=False, braid=False,
        hat_colors=dict(crown="#a4a8ae", crown_l="#d4d8dc", crown_d="#6a6e76", band="#2a2a30", visor="#16141a", visor_l="#4a4652",
                        badge="#c8a04a", badge_c="#2a2a30"),
        hair=dict(color="#4a3a30", front=0.04, grow=0.18),
        costume="ucoat10", coat_len=0.62, coat_flare=0.12,
        sleeve=dict(color="#4a4c54", dark="#2c2e34", cuff="#4a4c54", len=0.84, w=0.180),
        shorts=dict(color="#2c2a30", dark="#1a181e", cuff="#2c2a30", len=0.90, w=0.14),
        boots=dict(color="#16141a", cuff="#16141a", h=0.20, toe=0.15),
        colors=dict(base="#4a4c54", dark="#2c2e34", lapel="#3a3c44", sweater="#f2f0ea", sweater_d="#bcb8ae", button="#1e1c22", belt="#2a282e",
                    pants="#2c2a30", moustache="#4a3a30", moustache_l="#7a6050"),
    ),
}

CANVAS10 = {
    "painter10": (-1.8750, -4.6250, 1.8750, 0.1250),
    "admiral": (-1.8125, -5.0000, 1.8125, 0.1250),
    "sailor_a": (-1.5000, -4.5625, 1.5000, 0.1250),
    "sailor_b": (-1.5000, -4.2500, 1.5000, 0.1250),
    "sailor_c": (-1.4375, -4.1875, 1.4375, 0.1250),
    "uboat_captain": (-1.8750, -4.3750, 1.8750, 0.1250),
}
# on a hanging plank (pose plank=1, ropes PLANK_ROPE high) / at the periscope (pose periscope=1): pass these to Actor.build
CANVAS10_PLANK = {"painter10": (-1.8750, -4.6250, 1.8750, 0.3125), "admiral": (-1.8125, -5.0000, 1.8125, 0.3125)}
CANVAS10_SCOPE = {"uboat_captain": (-1.8750, -4.3750, 1.8750, 0.1875)}

_SQUINT = dict(eyes="squeeze", brows=("both", 0.110, 18.0, None, 0.17, 0.010), mouth="frown", mouth_dy=-0.01)


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="top", stretch=1.3):
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _bino_to_eyes(S, name, key="r", dy=0.0, it=4):
    """move the hand holding the binoculars so the glasses sit on the eyes (midpoint of eye_l / eye_r)."""
    c, p = S[name]
    for _ in range(it):
        an = figure(c, p, "q")["anchors"]
        bx, by = an["binoc_" + key]
        ex = (an["eye_l"][0] + an["eye_r"][0]) / 2
        ey = (an["eye_l"][1] + an["eye_r"][1]) / 2 + dy
        h = p["arm_" + key]["hand"]
        p["arm_" + key]["hand"] = (h[0] + ex - bx, h[1] + ey - by)


def _scope_hands(S, name, hy=0.80, free=None):
    """put the hands on the periscope grips (column at the facing eye + 0.36, grips 0.57 either side)."""
    c, p = S[name]
    for _ in range(4):
        an = figure(c, p, "q")["anchors"]
        cx = an["eye_r"][0] + SCOPE_DX
        if free != "l":
            h = an["hand_l"]
            o = p["arm_l"]["hand"] if isinstance(p.get("arm_l"), dict) and "hand" in p["arm_l"] else h
            p["arm_l"] = dict(p.get("arm_l") if isinstance(p.get("arm_l"), dict) else {}, hand=(o[0] + cx - SCOPE_GRIP - h[0], o[1] + hy - h[1]), layer="front")
        if free != "r":
            h = an["hand_r"]
            o = p["arm_r"]["hand"] if isinstance(p.get("arm_r"), dict) and "hand" in p["arm_r"] else h
            p["arm_r"] = dict(p.get("arm_r") if isinstance(p.get("arm_r"), dict) else {}, hand=(o[0] + cx + SCOPE_GRIP - h[0], o[1] + hy - h[1]), layer="front")


SAILORS = (("sailor_a", "_a"), ("sailor_b", "_b"), ("sailor_c", "_c"))
BRUSH = dict(type="bigbrush", scale=1.0)


def _story():
    S, M = {}, {}
    N, A, U = "painter10", "admiral", "uboat_captain"
    # --- the painter
    S["painter_paint_stroke"] = (N, dict(yaw=0.50, pitch=-0.45, expr="determined", head_roll=-6, lean=-4, gaze=(0.8, -0.6), t=0.3,
                                         arm_r=dict(hand=(0.66, -0.30), bend=-0.6, stretch=1.3, layer="front"), prop_r=dict(BRUSH, angle=-62),
                                         legs=dict(preset="step", stride=0.45)))
    M["painter_paint_stroke"] = dict(note="the big brush raised, sweeping a black stripe up the hull (screen-right); both hands on the handle "
                                          "(lower hand on grip_far_r), anchor brush_r = the bristles.  Animate: sweep arm_r hand from (0.70, 0.55) "
                                          "/ angle -20 to (0.66, -0.30) / angle -62 over ~14 frames; t drives the drips")
    S["painter_step_back_proud"] = (N, dict(yaw=0.30, pitch=-0.35, expr="smug", mouth="smile", head_roll=-6, lean=-8, gaze=(0.7, -0.4),
                                            arm_r=dict(hand=(0.46, 1.04), bend=0.3, stretch=1.1), prop_r=dict(BRUSH, angle=100, scale=0.95), brush_paint=0.6,
                                            arm_l="akimbo", legs=dict(preset="step", stride=-0.40), squash=(0.98, 1.02)))
    M["painter_step_back_proud"] = dict(note="stepped back, chest out, admiring the finished dazzle ship (screen-right), brush hanging at his side")
    S["painter_calm_smile"] = (N, dict(yaw=0.25, pitch=-0.15, expr="happy", mouth="smile", head_roll=-4, gaze=(0.4, 0.0),
                                       arm_r=dict(hand=(0.40, 0.42), bend=0.6, stretch=1.1), prop_r=dict(BRUSH, angle=-84, scale=0.95), brush_paint=0.7,
                                       arm_l=dict(hand=(-0.40, 1.02), bend=0.3), prop_l="paint_bucket", legs="stand"))
    M["painter_calm_smile"] = dict(note="laughed at, he smiles calmly, brush upright at his shoulder, bucket in the other hand")
    S["painter_on_plank"] = (N, dict(yaw=0.55, pitch=-0.20, expr="determined", head_roll=-4, gaze=(0.9, -0.2), t=0.3, plank=1,
                                     arm_r=dict(hand=(0.80, 0.30), bend=-0.5, stretch=1.3, layer="front"), prop_r=dict(BRUSH, angle=-20, scale=0.9),
                                     arm_l=dict(hand=(-0.40, 1.00), bend=0.3), prop_l="paint_bucket", legs="stand"))
    M["painter_on_plank"] = dict(note="on the hanging plank painting the hull (screen-right), bucket in the other hand. Pose plank=1 draws the "
                                      "plank + ropes (plank_w, plank_rope); set plank=0 when the set has its own plank. Canvas CANVAS10_PLANK")
    S["painter_grin"] = (N, dict(yaw=0.20, pitch=-0.25, expr="grinning", head_roll=6, gaze=(-0.4, -0.2),
                                 arm_r=dict(hand=(-0.16, 0.78), bend=0.7, layer="front"), arm_l=dict(hand=(0.18, 0.74), bend=0.7, layer="front"),
                                 legs="stand"))
    M["painter_grin"] = dict(note="the painter on deck grins as the torpedo misses (arms folded)")
    S["painter_walk"] = (N, cycle(N, 0.30, "walk", base=dict(expr="neutral", prop_r=dict(BRUSH, angle=-84, scale=0.95)), arms="l"))
    S["painter_walk"][1]["arm_r"] = dict(hand=(0.40, 0.42), bend=0.6, stretch=1.1)
    # --- the admiral
    S["admiral_laugh_big"] = (A, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                      arm_r=dict(hand=(0.44, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.48, 0.98), bend=0.9, shape="open"),
                                      legs="wide"))
    M["admiral_laugh_big"] = dict(note="bursts out laughing at the striped hull: head back, hands on the belly; the open laugh mouth is a held "
                                       "shape (no lip-sync); animate squash (1.02, 0.98) <-> (0.99, 1.01) every 4 frames")
    S["admiral_point_mock"] = (A, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                       arm_r=dict(hand=(1.08, 0.12), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    M["admiral_point_mock"] = dict(lipsync=True, note="'Warships must be grey!': pointing at the grey ships (screen-right; mirror=True for "
                                                    "left), mocking; LIP-SYNC: mouth=talk_mouth(g) during the quote, 'flat' otherwise")
    S["admiral_finger_up_promise"] = (A, dict(yaw=0.30, pitch=-0.40, expr="smug", mouth="talk_a", head_roll=-4, lean=-6,
                                              arm_r=dict(hand=(0.86, -0.50), shape="point", bend=-0.5, stretch=1.3),
                                              arm_l=dict(hand=(-0.26, 0.70), bend=0.8, shape="open", layer="front"), legs="wide", squash=(1.01, 0.99)))
    M["admiral_finger_up_promise"] = dict(lipsync=True, note="'If your ship survives, I'll paint mine zebra myself!': chest out, index finger up, "
                                                           "other hand on the chest; LIP-SYNC with talk_mouth()")
    S["admiral_arms_akimbo"] = (A, dict(yaw=0.20, pitch=-0.30, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["admiral_arms_akimbo"] = dict(note="smug, arms akimbo")
    S["admiral_binoculars_up"] = (A, dict(yaw=0.35, pitch=-0.10, expr="determined", mouth="flat",
                                          arm_r=dict(hand=(0.28, 0.12), bend=-0.6, stretch=1.2, layer="top"), prop_r="binoculars", legs="wide"))
    M["admiral_binoculars_up"] = dict(note="on the bridge with the field glasses at his eyes (glasses face the viewer); anchor binoc_r")
    S["admiral_shout"] = (A, dict(yaw=0.40, pitch=-0.40, expr="shouting", mouth="talk_b", head_roll=6,
                                  arm_r=dict(hand=(1.05, 0.16), shape="point", bend=-0.5, stretch=1.3),
                                  arm_l=dict(hand=(-0.50, 1.00), bend=0.3), prop_l=dict(type="binoculars", scale=1.15), legs="wide"))
    M["admiral_shout"] = dict(lipsync=True, note="'See? A crystal-clear target!': shouting on the bridge, pointing out to sea (screen-right), "
                                               "binoculars in the other hand; LIP-SYNC with talk_mouth()")
    S["admiral_jaw_drop"] = (A, dict(yaw=0.30, pitch=0.10, expr="stunned", mouth=("open", 0.15, 0.20), head_dy=0.03, gaze=(0.8, 0.0),
                                     arm_r=dict(hand=(0.50, 1.10), bend=0.2), prop_r=dict(type="binoculars", scale=1.15), arm_l=dict(hand=(-0.50, 1.06), bend=0.2),
                                     legs="stand", squash=(1.01, 0.99)))
    M["admiral_jaw_drop"] = dict(note="jaw dropped (held open mouth, not lip-sync), arms hanging, binoculars dangling from one hand")
    S["admiral_binoculars_lowered"] = (A, dict(yaw=0.35, pitch=-0.05, expr="shocked", gaze=(0.9, 0.0),
                                               arm_r=dict(hand=(0.36, 0.66), bend=-0.4, stretch=1.2, layer="front"), prop_r=dict(type="binoculars", scale=1.15), legs="wide"))
    M["admiral_binoculars_lowered"] = dict(note="has just lowered the glasses to chest height, eyes wide (blend into admiral_jaw_drop)")
    S["admiral_plank_sheepish"] = (A, dict(yaw=0.45, pitch=0.15, expr="worried", mouth="smirk", fx=["blush", "sweat"], head_roll=6, gaze=(-0.6, 0.2),
                                           paint_spots=1.0, plank=1, t=0.3,
                                           arm_r=dict(hand=(0.80, 0.40), bend=-0.5, stretch=1.3, layer="front"), prop_r=dict(BRUSH, angle=-28, scale=0.9),
                                           arm_l=dict(hand=(-0.52, -0.22), bend=-0.9, stretch=1.2, shape="open", layer="back"), legs="stand"))
    M["admiral_plank_sheepish"] = dict(note="the ending: on the hanging plank painting his own ship zebra, brush in hand, paint spots on his face, "
                                            "moustache and cap (paint_spots 0..1), sheepish glance back at camera, scratching his head. plank=1; "
                                            "canvas CANVAS10_PLANK")
    S["admiral_walk"] = (A, cycle(A, 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    # --- sailors
    for c, sfx in SAILORS:
        S["sailor_point_laugh" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                                 arm_r=dict(hand=(0.80, 0.04), shape="point", bend=-0.6, stretch=1.3),
                                                 arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
        S["sailor_laugh_hold_belly" + sfx] = (c, dict(yaw=0.15, pitch=0.25, expr="laughing", blink=2, fx=["tears"], head_roll=-8, lean=10, t=0.6,
                                                      arm_r=dict(hand=(0.24, 0.98), bend=0.9, shape="open", layer="front"),
                                                      arm_l=dict(hand=(-0.26, 0.94), bend=0.9, shape="open", layer="front"),
                                                      legs=dict(preset="crouch", crouch=0.15, spread=0.10)))
        S["sailor_idle" + sfx] = (c, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="behind", legs="stand"))
    M["sailor_point_laugh"] = dict(note="pointing and laughing at the painter (screen-right; mirror=True for left): sailor_a; _b, _c")
    M["sailor_laugh_hold_belly"] = dict(note="doubled over laughing, holding the belly, eyes shut: sailor_a; _b, _c")
    M["sailor_idle"] = dict(note="standing on deck / the quay; blink with blink_at(): sailor_a; _b, _c")
    # --- the U-boat captain
    S["uboat_periscope"] = (U, dict(yaw=0.50, pitch=0.05, expr="squint", head_roll=-3, lean=6, periscope=1,
                                    arm_r=dict(hand=(0.9, 0.3), bend=-0.6, stretch=1.3, layer="front"),
                                    arm_l=dict(hand=(0.3, 0.3), bend=0.5, stretch=1.3, layer="front"), legs=dict(preset="step", stride=0.25)))
    M["uboat_periscope"] = dict(note="at the periscope: one eye pressed to the eyepiece, the other squeezed shut, both hands on the training "
                                     "handles. pose periscope=1 draws the column (from SCOPE_TOP to the floor), the handle bar and the eyepiece "
                                     "over the facing eye. Animate: sway hands +-0.04 in x together. Canvas CANVAS10_SCOPE")
    S["uboat_aim"] = (U, dict(yaw=0.50, pitch=0.05, expr="squint", head_roll=-3, lean=6, periscope=1,
                              arm_r=dict(hand=(0.9, 0.3), bend=-0.6, stretch=1.3, layer="front"),
                              arm_l=dict(hand=(-0.55, -0.35), bend=-0.8, stretch=1.2, layer="back"), legs=dict(preset="step", stride=0.25)))
    M["uboat_aim"] = dict(note="aiming: eye still at the eyepiece, one hand on the handle, the other fist raised for 'fire' (mouth stays shut)")
    S["uboat_stand"] = (U, dict(yaw=0.30, pitch=-0.10, expr="determined", arm_r="behind", arm_l="behind", legs="stand"))
    M["uboat_stand"] = dict(note="standing, hands behind his back")
    # --- two-handed pieces, glasses on the eyes, hands on the periscope
    _two_hands(S, "painter_paint_stroke", bend=0.4, layer="front")
    _two_hands(S, "admiral_binoculars_up", bend=-0.4, layer="top", stretch=1.2)
    _bino_to_eyes(S, "admiral_binoculars_up")
    _two_hands(S, "admiral_binoculars_up", bend=-0.4, layer="top", stretch=1.2)
    _two_hands(S, "admiral_binoculars_lowered", bend=-0.4, layer="front", stretch=1.2)
    _scope_hands(S, "uboat_periscope")
    _scope_hands(S, "uboat_aim", free="l")
    for n in ("painter_walk", "admiral_walk"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast10.cycle(); animate: cycle(cast, frame / N, mode, facing, base, arms) with "
                                  "N = 28 walk / 16 run / 32 sneak / 24 march"))
    return S, M


STORY10, STORY10_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast10_registered", False):
        CE.register_stage()
        if not STORY10:
            s, m = _story()
            STORY10.update(s)
            STORY10_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_ink_limb", "_hand", "figure"):
        _O10[name] = getattr(P, name)
    P._hand = _hand
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    P.figure = figure
    CE.COSTUMES.update(COSTUMES10)
    CE.HATS.update(HATS10)
    P.EXPRESSIONS.setdefault("squint", _SQUINT)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS10 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP10)
    for n, c in NEW_CAST10.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS10)
    P._cast10_registered = True
    s, m = _story()
    STORY10.update(s)
    STORY10_META.update(m)
    P.STORY.update(STORY10)
    CE.register_stage()


register()
