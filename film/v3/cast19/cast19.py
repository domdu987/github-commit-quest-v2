#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast19.py -- the cast of film 19 ("ไอ้ช่างไม้": John Harrison, the carpenter who solved longitude, England 1730s-1773) for the v2
puppet, as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast19"); import cast19     # registers on import (idempotent); import it BEFORE sprites
    import puppet                                                       # the same module object, now with the new members
    cast, pose = cast19.STORY19["astro_belly_laugh"]
    f = puppet.figure(cast, pose, "f")
    p = dict(pose, mouth=cast19.talk_mouth(g, 1.0), blink=cast19.blink_at(g, 90))

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  georgian19 (period coat / gown / waistcoat / shirt / jabot / apron / sash+star, one drawing parametrised by CAST g19),
                       slops19 (sailor: striped or checked shirt panel in a short jacket, kerchief)
    cast_ext.HATS      wig19 (full-bottomed, bob, king, tie and own-hair-tied-back wigs; powdered), tricornhair19 (tricorne over tied hair)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast10's wrappers (each falls through for everything it does not handle):
    _norm / _face / _prop / _ink_limb / figure   pose keys, forehead spectacles + flush nose, new props, stockings + buckled shoes, variants + stool
Variants (pose keys that pick a sibling CAST entry): harrison19 young=1 / old=1 (stoop by default), william19 / captain19 hat_off=1.
New cast: harrison19, william19, astro19, astro19_b, astro19_c, king19, captain19, sailor19_a/_b/_c (spec: sailor_a/_b/_c).
STORY19 / STORY19_META: story poses.  cycle() (people: cast6), laugh_cycle(), talk_mouth(), blink_at(), NOD.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10    # noqa: E402  (v3/cast10, read-only; imports cast9 .. cast_ext and v2/puppet)
import cast9 as C9      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW19 = ("harrison19", "william19", "astro19", "astro19_b", "astro19_c", "king19", "captain19", "sailor19_a", "sailor19_b", "sailor19_c")
ALIAS19 = {"sailor_a": "sailor19_a", "sailor_b": "sailor19_b", "sailor_c": "sailor19_c"}      # spec names that earlier casts already own


def key19(name):
    """the CAST key for a film-19 name (sailor_a -> sailor19_a, ...; others unchanged)."""
    return ALIAS19.get(name, name)


TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O19 = {}
_POSE19 = {"shav": 1.0, "t": 0.0, "splash": 0.0, "glint": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours (warm Georgian: brown, buff, navy, crimson, gold)
BRASS = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
GOLDC = C10.GOLD
SILVER = dict(light="#f6f8fb", base="#c4cad4", dark="#7a8290")
WOOD = dict(light="#d8a868", base="#a8743c", dark="#5e3c1c")
LEATH = dict(light="#c8945e", base="#9a6a3c", dark="#5a3a1c")
PARCH = dict(light="#fff6dc", base="#ecdcae", dark="#b8a070")
STEEL = dict(light="#d8dde6", base="#9aa2b0", dark="#555c6a")
NAVYC = dict(light="#4a5e9a", base="#26335e", dark="#121a34")
CREAMC = dict(light="#fffaf0", base="#f0e4c8", dark="#c8b890")
HONEY = "#e8c47a"


def _g3(k, name, c, x0, y0, x1, y1):
    return _lin(k, name, c["light"], c["base"], c["dark"], x0, y0, x1, y1)


def _star(cx, cy, r, n=5, ratio=0.46, rot=-90.0):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * ratio
        a = math.radians(rot + i * 180.0 / n)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


# ============================================================================= props (own local frames, like cast16)
def _watch_body(k, c, face, rr=0.12, hands_t=0.0, lid=False):
    """round pocket watch seen face-on, centred on (0, 0): metal case, dial with minute + hour ticks only (NO numerals), two hands, bow ring."""
    g = _g3(k, "wc", c, -rr, -rr, rr, rr)
    o = []
    o.append('<path d="M0,%.3f q-0.045,-0.00 -0.040,-0.045 q0.04,-0.030 0.08,0 q0.005,0.045 -0.040,0.045 Z" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (-rr - 0.005, k.ink))
    o.append('<path d="M0,%.3f q-0.045,-0.00 -0.040,-0.045 q0.04,-0.030 0.08,0 q0.005,0.045 -0.040,0.045 Z" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (-rr - 0.005, k.c(c["base"])))
    o.append('<rect x="-0.016" y="%.3f" width="0.032" height="0.030" rx="0.008" fill="%s" stroke="%s" stroke-width="0.012"/>' % (-rr - 0.028, k.c(c["dark"]), k.ink))
    o.append('<circle cx="0" cy="0" r="%.3f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (rr, g, k.ink))
    rd = rr - 0.022
    o.append('<circle cx="0" cy="0" r="%.3f" fill="%s" stroke="%s" stroke-width="0.010"/>' % (rd, k.c(face), k.ink))
    r1 = rd - 0.012
    cir = 2 * math.pi * r1
    o.append('<circle cx="0" cy="0" r="%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-dasharray="%.4f %.4f" opacity="0.8"/>' % (r1, k.ink, 0.004, cir / 60.0 - 0.004))
    o.append('<circle cx="0" cy="0" r="%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-dasharray="%.4f %.4f" transform="rotate(-1.5)"/>' % (r1 - 0.004, k.ink, 0.011, cir / 12.0 - 0.011))
    ah = math.radians(-90 + 300.0 + 40 * hands_t)
    am = math.radians(-90 + 60.0 + 360 * hands_t)
    o.append('<path d="M0,0 L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (0.55 * rd * math.cos(ah), 0.55 * rd * math.sin(ah), k.ink))
    o.append('<path d="M0,0 L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (0.80 * rd * math.cos(am), 0.80 * rd * math.sin(am), k.ink))
    o.append('<circle cx="0" cy="0" r="0.012" fill="%s" stroke="%s" stroke-width="0.006"/>' % (k.c(c["light"]), k.ink))
    o.append('<path d="M%.3f,%.3f A%.3f,%.3f 0 0 1 %.3f,%.3f" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
             % (-rr * 0.80, -rr * 0.30, rr * 0.85, rr * 0.85, -rr * 0.25, -rr * 0.80))
    if lid:
        o.insert(0, '<path d="M-0.06,0.02 L-0.17,-0.17 A0.20,0.20 0 0 1 -0.20,0.02 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round" opacity="0.0"/>' % (k.c(c["base"]), k.ink))
    return "".join(o)


def _h4_body(k):
    return _watch_body(k, SILVER, "#fdfbf4", 0.12)


def _pocketwatch_body(k):
    o = _watch_body(k, BRASS, "#fff8e4", 0.13, hands_t=0.0)
    ch = ('<path d="M0,-0.20 Q-0.12,-0.34 -0.22,-0.20 Q-0.28,-0.08 -0.20,0.04" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>'
          '<path d="M0,-0.20 Q-0.12,-0.34 -0.22,-0.20 Q-0.28,-0.08 -0.20,0.04" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" stroke-dasharray="0.024 0.010"/>'
          % (k.ink, k.c(BRASS["base"])))
    return ch + o


def _quadrant_body(k):
    """a brass Hadley quadrant (a 45-degree sector, 0.62 long): hold at the apex (0, 0); the straight edges run along +x and (rotated) toward
    the arc; scale ticks, an index arm with a vernier, a mirror box and a sight vane.  Local +x = the frame bar."""
    R = 0.62
    a1 = math.radians(-60)
    p1, p2 = (R, 0.0), (R * math.cos(a1), R * math.sin(a1))
    g = _g3(k, "qd", BRASS, 0, 0, R, 0)
    d = "M0,0 L%.3f,%.3f A%.3f,%.3f 0 0 0 %.3f,%.3f Z" % (p1[0], p1[1], R, R, p2[0], p2[1])
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink)]
    o.append('<path d="M0.18,-0.02 L0.40,-0.02 A0.40,0.40 0 0 0 %.3f,%.3f L%.3f,%.3f Z" fill="%s" opacity="0.45"/>' % (0.40 * math.cos(a1), 0.40 * math.sin(a1), 0.18 * math.cos(a1), 0.18 * math.sin(a1), k.c(BRASS["dark"])))
    # scale arc: ticks
    r2 = R - 0.050
    arclen = r2 * math.radians(60)
    o.append('<path d="M%.3f,%.3f A%.3f,%.3f 0 0 0 %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.040" stroke-dasharray="0.005 %.4f"/>'
             % (r2, -0.004, r2, r2, r2 * math.cos(a1), r2 * math.sin(a1), k.ink, arclen / 30.0 - 0.005))
    o.append('<path d="M%.3f,%.3f A%.3f,%.3f 0 0 0 %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.012"/>'
             % (r2 - 0.022, -0.004, r2 - 0.022, r2 - 0.022, (r2 - 0.022) * math.cos(a1), (r2 - 0.022) * math.sin(a1), k.ink))
    # index arm to ~ -22 degrees with a vernier
    a2 = math.radians(-24)
    o.append('<path d="M0,0 L%.3f,%.3f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/><path d="M0,0 L%.3f,%.3f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
             % (R * math.cos(a2), R * math.sin(a2), k.ink, R * math.cos(a2), R * math.sin(a2), k.c(BRASS["light"])))
    o.append('<circle cx="%.3f" cy="%.3f" r="0.026" fill="%s" stroke="%s" stroke-width="0.012"/>' % (R * 0.90 * math.cos(a2), R * 0.90 * math.sin(a2), k.c(STEEL["light"]), k.ink))
    # horizon mirror box and sight vane on the straight edges
    o.append('<rect x="0.04" y="-0.080" width="0.085" height="0.090" rx="0.010" fill="%s" stroke="%s" stroke-width="0.014" transform="rotate(-8 0.08 -0.04)"/>' % (k.c(STEEL["base"]), k.ink))
    o.append('<path d="M0.58,0 L0.58,-0.075" stroke="%s" stroke-width="0.034" stroke-linecap="round"/><path d="M0.58,0 L0.58,-0.075" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (k.ink, k.c(STEEL["light"])))
    o.append('<path d="M0.06,-0.015 L0.55,-0.015" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>')
    g = _POSE19["glint"]
    if g > 0.02:       # a small four-point sparkle on the mirror box
        c, r = (0.36, -0.10), 0.05 + 0.07 * g
        o.append('<path d="%s" fill="#ffffff" stroke="%s" stroke-width="0.008" opacity="0.95"/>' % (_poly_d(_star(c[0], c[1], r, 4, 0.22)), k.ink))
    return "".join(o)


def _candlestick_body(k, t=0.0):
    """a brass candlestick, hand at the stem (0, 0): drip pan, knopped stem, a cream candle with a flame; foot below."""
    o = ['<circle cx="0" cy="-0.34" r="0.34" fill="#ffd27a" opacity="0.17"/>']
    o.append('<path d="M-0.12,0.30 Q-0.12,0.22 -0.04,0.20 L0.04,0.20 Q0.12,0.22 0.12,0.30 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M-0.025,0.20 L-0.020,0.04 M0.025,0.20 L0.020,0.04" stroke="%s" stroke-width="0.020"/><path d="M0,0.20 L0,0.04" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (k.ink, k.c(BRASS["base"])))
    o.append('<ellipse cx="0" cy="0.11" rx="0.045" ry="0.028" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M-0.10,-0.02 L0.10,-0.02 Q0.12,0.03 0.06,0.05 L-0.06,0.05 Q-0.12,0.03 -0.10,-0.02 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<rect x="-0.045" y="-0.34" width="0.090" height="0.32" rx="0.012" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(CREAMC["light"]), k.ink))
    o.append('<path d="M-0.02,-0.31 q0.01,0.08 0,0.17" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(CREAMC["dark"]))
    lean = 0.022 * math.sin(t * 2 * math.pi * 2.0)
    o.append('<path d="M-0.030,-0.35 Q%.3f,-0.42 %.3f,-0.55 Q%.3f,-0.42 0.030,-0.35 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (-0.045 + lean, lean * 1.6, 0.045 + lean, k.c("#ffb43a"), k.ink))
    o.append('<path d="M0,-0.36 Q-0.015,-0.42 0,-0.46 Q0.015,-0.42 0,-0.36 Z" fill="#fff6c8"/>')
    return "".join(o)


def _tricorn_held_body(k):
    """a tricorne seen from a three-quarter front, held by the front corner (0, 0): black felt, gold lace edging, low crown, cockade."""
    g = _g3(k, "th", dict(light="#4a4552", base="#2b2731", dark="#19161d"), -0.4, 0, 0.4, 0)
    o = ['<path d="M-0.20,-0.30 Q0,-0.46 0.20,-0.30 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c("#1c1a22"), k.ink)]
    d = "M-0.42,-0.22 Q-0.22,-0.34 0,-0.26 Q0.22,-0.34 0.42,-0.22 Q0.34,-0.06 0.06,0.04 Q0,0.08 -0.06,0.04 Q-0.34,-0.06 -0.42,-0.22 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M-0.40,-0.215 Q-0.34,-0.07 -0.06,0.03 Q0,0.06 0.06,0.03 Q0.34,-0.07 0.40,-0.215" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % k.c(GOLDC["base"]))
    o.append('<path d="M-0.30,-0.29 Q-0.18,-0.34 -0.06,-0.30" fill="none" stroke="#9e98ad" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>')
    o.append('<circle cx="-0.34" cy="-0.19" r="0.030" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#c7332b"), k.ink))
    return "".join(o)


def _file_body(k):
    """a hand file / rasp 0.80 long along +x: wooden handle 0..0.20, steel blade 0.20..0.80 (tapered, cross-hatched teeth)."""
    o = ['<path d="M0.20,-0.034 L0.80,-0.020 L0.80,0.020 L0.20,0.034 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink)]
    o.append('<path d="M0.26,-0.014 L0.78,-0.006 M0.26,0.014 L0.78,0.007" stroke="%s" stroke-width="0.012" stroke-dasharray="0.006 0.010" opacity="0.9"/>' % k.c(STEEL["dark"]))
    o.append('<path d="M0.24,-0.026 L0.78,-0.015" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>')
    o.append('<path d="M-0.02,-0.046 Q0.08,-0.060 0.20,-0.040 L0.20,0.040 Q0.08,0.060 -0.02,0.046 Q-0.05,0 -0.02,-0.046 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink))
    o.append('<rect x="0.19" y="-0.044" width="0.026" height="0.088" rx="0.006" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M0.0,-0.030 L0.17,-0.026" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(WOOD["light"]))
    return "".join(o)


def _chisel_body(k):
    """a wood chisel 0.55 long along +x: mushroom handle at the hand, steel ferrule and bevelled blade."""
    o = ['<path d="M0.18,-0.032 L0.52,-0.034 L0.55,0.028 L0.18,0.032 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink)]
    o.append('<path d="M0.22,-0.020 L0.52,-0.024" stroke="#ffffff" stroke-width="0.009" stroke-linecap="round" opacity="0.7"/>')
    o.append('<path d="M-0.04,-0.052 Q0.06,-0.070 0.18,-0.044 L0.18,0.044 Q0.06,0.070 -0.04,0.052 Q-0.08,0 -0.04,-0.052 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink))
    o.append('<rect x="0.17" y="-0.040" width="0.030" height="0.080" rx="0.006" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["base"]), k.ink))
    return "".join(o)


def _quill_body(k):
    """a quill pen 0.70 long: nib at +x, feather vane trailing toward -x."""
    o = ['<path d="M-0.34,-0.22 Q0.0,-0.20 0.22,-0.016 L0.22,0.008 Q-0.10,0.10 -0.34,-0.22 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#f4f0e4"), k.ink)]
    o.append('<path d="M-0.30,-0.14 Q-0.06,-0.04 0.40,0.0" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.30,-0.14 Q-0.06,-0.04 0.40,0.0" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % k.c("#d8cfa8"))
    o.append('<path d="M0.40,0.0 L0.46,0.004" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.ink)
    return "".join(o)


def _scroll_body(k):
    """a rolled decree held across the hand (0.62 long along +x): parchment roll with curled ends, a red ribbon and wax seal hanging."""
    g = _g3(k, "sc", PARCH, 0, -0.07, 0, 0.07)
    o = ['<path d="M-0.04,-0.07 L0.58,-0.07 L0.58,0.07 L-0.04,0.07 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink)]
    for x in (-0.04, 0.58):
        o.append('<ellipse cx="%.3f" cy="0" rx="0.030" ry="0.070" fill="%s" stroke="%s" stroke-width="0.016"/><ellipse cx="%.3f" cy="0" rx="0.012" ry="0.034" fill="none" stroke="%s" stroke-width="0.008"/>'
                 % (x, k.c(PARCH["light"]), k.ink, x, k.ink))
    o.append('<path d="M0.30,-0.07 L0.30,0.07" stroke="%s" stroke-width="0.028"/><path d="M0.30,0.07 Q0.34,0.18 0.30,0.28 M0.32,0.07 Q0.38,0.16 0.36,0.26" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>'
             % (k.c("#9c2a2a"), k.c("#9c2a2a")))
    o.append('<circle cx="0.33" cy="0.27" r="0.045" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="0.32" cy="0.26" r="0.014" fill="%s" opacity="0.7"/>' % (k.c("#b83a30"), k.ink, k.c("#e07a60")))
    return "".join(o)


def _chart_body(k):
    """an unrolled sea chart held by its left edge (0, 0): 0.74 x 0.52, a coast, a compass rose, rhumb lines and a pair of dividers; no text."""
    g = _g3(k, "ch", PARCH, 0, 0, 0.74, 0)
    o = ['<path d="M0,-0.26 L0.74,-0.26 L0.74,0.26 L0,0.26 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.02,-0.04 Q0.14,-0.10 0.20,-0.02 Q0.30,0.06 0.40,-0.12 Q0.46,-0.20 0.60,-0.17 L0.72,-0.20 L0.72,-0.25 L0.02,-0.25 Z" fill="%s" opacity="0.85" stroke="%s" stroke-width="0.010"/>' % (k.c("#c8a864"), k.ink))
    o.append('<path d="M0.05,0.06 Q0.18,0.02 0.30,0.10 M0.10,0.17 Q0.22,0.12 0.36,0.20" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c("#5a7aa0"))
    cx, cy = 0.56, 0.08
    o.append('<circle cx="%.2f" cy="%.2f" r="0.085" fill="none" stroke="%s" stroke-width="0.010"/>' % (cx, cy, k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.008"/>' % (_poly_d(_star(cx, cy, 0.105, 4, 0.30)), k.c("#b83a30"), k.ink))
    o.append('<path d="M0.04,0.21 L0.70,-0.06 M0.04,-0.03 L0.70,0.22 M0.30,0.25 L0.64,-0.14" stroke="%s" stroke-width="0.006" opacity="0.45"/>' % k.ink)
    o.append('<path d="M0.16,0.19 L0.22,0.06 M0.16,0.19 L0.28,0.12" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(BRASS["base"]))
    return "".join(o)


def _h1_body(k):
    """the H1 sea clock, 1.0 wide x 0.68 tall, hand grip at the middle of the base (0, 0): brass base plate and frame, two dumbbell balances
    linked by a bar with springs, a gear wheel; held overhead with two hands (grips at x = +-0.42)."""
    gb = _g3(k, "h1", BRASS, -0.5, 0, 0.5, 0)
    o = ['<path d="M-0.52,0.0 L0.52,0.0 L0.52,-0.06 L-0.52,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (gb, k.ink)]
    for x in (-0.44, 0.44):
        o.append('<path d="M%.2f,-0.06 L%.2f,-0.60" stroke="%s" stroke-width="0.052" stroke-linecap="round"/><path d="M%.2f,-0.06 L%.2f,-0.60" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
                 % (x, x, k.ink, x, x, k.c(BRASS["base"])))
    o.append('<path d="M-0.50,-0.60 L0.50,-0.60" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M-0.50,-0.60 L0.50,-0.60" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (k.ink, k.c(BRASS["base"])))
    # gear wheel
    o.append('<circle cx="0" cy="-0.22" r="0.15" fill="%s" stroke="%s" stroke-width="0.020" stroke-dasharray="0.030 0.020"/>' % (k.c(BRASS["light"]), k.ink))
    o.append('<circle cx="0" cy="-0.22" r="0.125" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M-0.10,-0.22 L0.10,-0.22 M0,-0.32 L0,-0.12 M-0.07,-0.29 L0.07,-0.15 M0.07,-0.29 L-0.07,-0.15" stroke="%s" stroke-width="0.012"/>' % k.c(BRASS["dark"]))
    o.append('<circle cx="0" cy="-0.22" r="0.022" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(STEEL["light"]), k.ink))
    # dumbbell balances (bar with a ball at each end), a spring
    o.append('<path d="M-0.26,-0.44 L0.26,-0.44" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.26,-0.44 L0.26,-0.44" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % k.c(BRASS["light"]))
    for x in (-0.30, 0.30):
        o.append('<circle cx="%.2f" cy="-0.44" r="0.075" fill="%s" stroke="%s" stroke-width="0.020"/><circle cx="%.2f" cy="-0.465" r="0.022" fill="#ffffff" opacity="0.6"/>'
                 % (x, _g3(k, "h1b%d" % int(x * 10), BRASS, x - 0.07, -0.5, x + 0.07, -0.4), k.ink, x - 0.02))
    o.append('<path d="M-0.20,-0.55 q0.05,-0.05 0.10,0 q0.05,0.05 0.10,0 q0.05,-0.05 0.10,0 q0.05,0.05 0.10,0" fill="none" stroke="%s" stroke-width="0.010"/>' % k.ink)
    return "".join(o)


def _rope_body(k):
    """a thick hauling rope 1.7 long along +x, sagging a little, twisted strands, frayed end; the hand grips at 0."""
    d = "M-0.30,0.02 Q0.40,0.10 1.00,0.02 Q1.50,-0.02 1.70,0.06"
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.085" stroke-linecap="round"/>' % (d, k.ink)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (d, k.c("#c8a46a")))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.058" stroke-dasharray="0.020 0.045" opacity="0.8"/>' % (d, k.c("#6e4c28")))
    o.append('<path d="M1.70,0.06 l0.07,-0.03 M1.70,0.06 l0.08,0.01 M1.70,0.06 l0.06,0.05" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c("#c8a46a"))
    return "".join(o)


def _bucket_body(k, splash=0.0):
    """a wooden bailing bucket, hand on the bail (0, 0): a staved bucket hanging below, iron hoops; splash > 0 throws water out to +x."""
    o = []
    g = _g3(k, "bk", WOOD, -0.16, 0, 0.16, 0)
    o.append('<path d="M-0.16,0.22 Q0,-0.10 0.16,0.22" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.15,0.18 L0.15,0.18 L0.12,0.46 L-0.12,0.46 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.05,0.19 L-0.04,0.45 M0.05,0.19 L0.04,0.45" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(WOOD["dark"]))
    for y, hw_ in ((0.24, 0.150), (0.40, 0.125)):
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (-hw_, y, hw_, y, k.c(STEEL["base"])))
    o.append('<ellipse cx="0" cy="0.18" rx="0.15" ry="0.030" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#4a7a9a"), k.ink))
    if splash > 0.02:
        s = splash
        o.append('<path d="M0.12,0.16 Q%.3f,-0.20 %.3f,0.20" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round" opacity="0.9"/>' % (0.30 + 0.25 * s, 0.30 + 0.60 * s, k.c("#7fb8d8")))
        o.append('<path d="M0.12,0.16 Q%.3f,-0.20 %.3f,0.20" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (0.30 + 0.25 * s, 0.30 + 0.60 * s))
        for i in range(4):
            o.append('<circle cx="%.3f" cy="%.3f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (0.34 + 0.16 * i * s + 0.12 * s, 0.22 - 0.10 * math.sin(i * 1.6) + 0.07 * i, k.c("#9ad0ea"), k.ink))
    return "".join(o)


# kind -> (body fn, upright (ox, oy) or None, ext points, tip distance, anchor prefix)
NEW_PROPS19 = ("h4_watch", "pocketwatch19", "quadrant19", "candlestick19", "tricorn_held", "file19", "chisel19", "quill19", "scroll19", "chart19", "h1_clock19",
               "rope19", "bucket19")
NEW_TIP19 = {"h4_watch": 0.0, "pocketwatch19": 0.0, "quadrant19": 0.62, "candlestick19": 0.0, "tricorn_held": 0.0, "file19": 0.80, "chisel19": 0.55, "quill19": 0.46,
             "scroll19": 0.62, "chart19": 0.74, "h1_clock19": 0.0, "rope19": 1.7, "bucket19": 0.0}
_UP19 = {"h4_watch": (0.0, -0.11), "pocketwatch19": (0.0, -0.11), "candlestick19": (0.0, 0.0), "tricorn_held": (0.0, -0.08), "h1_clock19": (0.0, 0.0), "bucket19": (0.0, 0.0),
         "chart19": (0.0, 0.0)}
_EXT19 = {"h4_watch": ((-0.15, -0.30), (0.15, 0.02)), "pocketwatch19": ((-0.30, -0.34), (0.15, 0.04)), "candlestick19": ((-0.14, -0.56), (0.14, 0.31)),
          "tricorn_held": ((-0.44, -0.46), (0.44, 0.08)), "h1_clock19": ((-0.54, -0.70), (0.54, 0.02)), "bucket19": ((-0.18, -0.12), (0.18, 0.48), (0.9, 0.2)),
          "chart19": ((0.0, -0.28), (0.76, 0.28))}
_ANG19 = {"quadrant19": (((0.0, -0.58), (0.62, 0.02), (0.30, 0.06)), "quad19_"), "file19": (((-0.06, -0.06), (0.82, 0.04)), "file_"), "chisel19": (((-0.08, -0.06), (0.56, 0.04)), "chisel_"),
          "quill19": (((-0.32, -0.16), (0.48, 0.04)), "quill_"), "scroll19": (((-0.08, -0.08), (0.62, 0.30)), "scroll_"), "rope19": (((-0.32, -0.06), (1.78, 0.12)), "rope_")}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS19:
        return _O19["_prop"](k, kind, H, ang, sc)
    key = C10.C8._side_key()
    an = C10.C8._POSE8["an"]
    if kind in _UP19:
        ox, oy = _UP19[kind]
        body = {"h4_watch": _h4_body, "pocketwatch19": _pocketwatch_body, "tricorn_held": _tricorn_held_body, "h1_clock19": _h1_body, "chart19": _chart_body}.get(kind)
        body = body(k) if body else (_candlestick_body(k, _POSE19["t"]) if kind == "candlestick19" else _bucket_body(k, _POSE19["splash"]))
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + ox * sc, H[1] + oy * sc, sc, body)
        for (x, y) in _EXT19[kind]:
            k.ext.append((H[0] + (x + ox) * sc, H[1] + (y + oy) * sc, 0.03))
        if kind == "h1_clock19":
            an["h1_grip_l_" + key] = (H[0] - 0.42 * sc, H[1] - 0.03 * sc)
            an["h1_grip_r_" + key] = (H[0] + 0.42 * sc, H[1] - 0.03 * sc)
        if kind == "h4_watch":
            an["watch_" + key] = (H[0] + ox * sc, H[1] + oy * sc)
        if kind == "chart19":
            an["chart_grip_far_" + key] = (H[0] + 0.74 * sc, H[1])
        return o, (H[0] + ox * sc, H[1] + oy * sc)
    body = {"quadrant19": lambda: _quadrant_body(k), "file19": lambda: _file_body(k), "chisel19": lambda: _chisel_body(k), "quill19": lambda: _quill_body(k),
            "scroll19": lambda: _scroll_body(k), "rope19": lambda: _rope_body(k)}[kind]()
    pts, anc = _ANG19[kind]
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    for (x, y) in pts:
        px, py = _rot(x * sc, y * sc, ang)
        k.ext.append((H[0] + px, H[1] + py, 0.03))
    tx, ty = _rot(NEW_TIP19[kind] * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[anc + key] = tip
    if kind == "rope19":
        gx, gy = _rot(0.62 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy + 0.04)
    return o, tip


# ============================================================================= hats / wigs (head frame; the head disc is r 0.47, top -0.51)
def _mirror_loop(right):
    """right-half points from the top centre round to the hairline centre -> a full closed outline (x -> -x on the way back)."""
    left = [(-x, y) for (x, y) in reversed(right)]
    if left and abs(left[0][0]) < 1e-6 and abs(right[-1][0]) < 1e-6:
        left = left[1:]
    return right + left


_WIGS = {
    # style -> (outer right half top->tail bottom, inner right half bottom->hairline centre, curl discs [(x, y, r)], queue?)
    "full": ([(0.0, -0.86), (0.20, -0.94), (0.46, -0.84), (0.68, -0.58), (0.78, -0.22), (0.80, 0.16), (0.83, 0.46), (0.79, 0.72), (0.84, 0.90), (0.70, 1.02), (0.55, 0.96), (0.51, 0.84)],
             [(0.49, 0.62), (0.46, 0.36), (0.45, 0.08), (0.43, -0.20), (0.31, -0.36), (0.15, -0.415), (0.0, -0.43)],
             [(0.70, 0.88, 0.085), (0.58, 0.82, 0.07)], None),
    "bob": ([(0.0, -0.78), (0.28, -0.82), (0.52, -0.68), (0.64, -0.34), (0.68, 0.06), (0.68, 0.42), (0.66, 0.64), (0.55, 0.72), (0.47, 0.64)],
            [(0.46, 0.50), (0.455, 0.20), (0.44, -0.08), (0.41, -0.26), (0.28, -0.36), (0.0, -0.41)],
            [(0.57, 0.62, 0.075)], None),
    "king": ([(0.0, -0.74), (0.26, -0.74), (0.48, -0.62), (0.58, -0.38), (0.58, -0.10), (0.54, 0.04)],
             [(0.46, 0.02), (0.43, -0.18), (0.31, -0.33), (0.0, -0.38)], [], "bag"),
    "tie": ([(0.0, -0.66), (0.26, -0.64), (0.46, -0.50), (0.54, -0.28), (0.54, -0.02)],
            [(0.46, 0.00), (0.44, -0.18), (0.30, -0.28), (0.0, -0.30)], [], "queue"),
    "tied": ([(0.0, -0.58), (0.26, -0.57), (0.46, -0.47), (0.51, -0.26), (0.51, -0.04)],
             [(0.46, -0.02), (0.43, -0.20), (0.30, -0.33), (0.12, -0.38), (0.0, -0.38)], [], "queue"),
}


def _wig_svg(k, C, yaw, style, col, hair_dy=0.0):
    outer, inner, discs, tail = _WIGS[style]
    if hair_dy:
        inner = [(x, y + hair_dy if y < -0.1 else y) for (x, y) in inner]
    dx = -0.03 * yaw
    loop = [(x + dx, y) for (x, y) in _mirror_loop(list(outer) + list(inner))]
    g = CE._gradient(k, "wg", col, x0=-0.8, x1=0.8, mid=0.30)
    o = []
    sb = -1 if yaw >= 0 else 1          # the back of the head
    if tail == "queue":
        x0 = sb * 0.46 + dx
        d = "M%.3f,0.02 Q%.3f,0.30 %.3f,0.50 Q%.3f,0.66 %.3f,0.92 Q%.3f,0.68 %.3f,0.40 Q%.3f,0.20 %.3f,-0.06 Z" % (
            x0, x0 + sb * 0.18, x0 + sb * 0.17, x0 + sb * 0.16, x0 + sb * 0.12, x0 + sb * 0.02, x0 + sb * 0.02, x0 - sb * 0.04, x0 - sb * 0.04)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, g, k.ink))
        o.append('<path d="M%.3f,0.34 q%.3f,0.14 %.3f,0.40" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (x0 + sb * 0.08, sb * 0.04, sb * 0.02, k.c(col["dark"])))
        bx, by = x0 + sb * 0.02, 0.10
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (bx, by, bx - 0.09, by - 0.05, bx - 0.09, by + 0.05, bx, by, bx + 0.09, by - 0.05, bx + 0.09, by + 0.05, k.c("#1a1418"), k.ink))
        o.append('<circle cx="%.3f" cy="%.3f" r="0.030" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx, by, k.c("#1a1418"), k.ink))
    elif tail == "bag":
        x0 = sb * 0.50 + dx
        o.append('<path d="M%.3f,0.00 Q%.3f,0.30 %.3f,0.44 L%.3f,0.78 Q%.3f,0.86 %.3f,0.78 L%.3f,0.40 Q%.3f,0.24 %.3f,-0.04 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                 % (x0 - sb * 0.04, x0 + sb * 0.12, x0 + sb * 0.10, x0 + sb * 0.18, x0 + sb * 0.12, x0 + sb * 0.02, x0 - sb * 0.02, x0 - sb * 0.10, x0 + sb * 0.04, k.c("#1a1a22"), k.ink))
        bx, by = x0 + sb * 0.04, 0.16
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (bx, by, bx - 0.10, by - 0.06, bx - 0.10, by + 0.06, bx, by, bx + 0.10, by - 0.06, bx + 0.10, by + 0.06, k.c("#101018"), k.ink))
    # ringlets behind the mass (they peek out at the bottom of the tails)
    for (x, y, r) in discs:
        for s in (-1, 1):
            o.append('<circle cx="%.3f" cy="%.3f" r="%.3f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (s * x + dx, y, r, g, k.ink))
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_open(loop), g, k.ink))
    # powder shading: curl lines
    cur = []
    for s in (-1, 1):
        for (x, y) in ((0.62, -0.46), (0.70, -0.14), (0.68, 0.22), (0.60, 0.54), (0.30, -0.70), (0.52, -0.62)):
            if style == "bob" and y > 0.6:
                continue
            if style in ("king", "tie", "tied") and (abs(x) > 0.56 or y > 0.0):
                continue
            if style in ("tie", "tied") and abs(x) > 0.5:
                continue
            xx = s * x * (0.80 if style in ("king", "tie", "tied", "bob") else 1.0) + dx
            cur.append("M%.3f,%.3f q%.3f,0.07 %.3f,0.13" % (xx, y, -s * 0.05, -s * 0.02))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.85"/>' % ("".join(cur), k.c(col["dark"])))
    ty = min(p[1] for p in outer) + 0.10
    o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f" fill="none" stroke="#ffffff" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>' % (-0.26 + dx, ty + 0.10, -0.16 + dx, ty, 0.06 + dx, ty))
    if style == "king":
        for s in (-1, 1):
            for j, y in enumerate((0.00, 0.17)):
                cx = s * 0.56 + dx
                o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.115" ry="0.075" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, y, g, k.ink))
                o.append('<path d="M%.3f,%.3f q%.3f,-0.04 %.3f,0.0 q%.3f,0.03 %.3f,0.0" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>'
                         % (cx - 0.07, y, 0.035, 0.07, -0.02, -0.05, k.c(col["dark"])))
    if style == "tie":
        for s in (-1, 1):
            cx = s * 0.52 + dx
            o.append('<ellipse cx="%.3f" cy="0.04" rx="0.080" ry="0.060" fill="%s" stroke="%s" stroke-width="0.018"/>' % (cx, g, k.ink))
    pts = [(-0.86 + dx, 0.0), (0.86 + dx, 0.0), (dx, -0.92)]
    if style == "full":
        pts += [(-0.82 + dx, 1.04), (0.82 + dx, 1.04)]
    elif style == "bob":
        pts += [(-0.68 + dx, 0.74), (0.68 + dx, 0.74)]
    elif style == "king":
        pts += [(sb * 0.72 + dx, 0.82)]
    elif style in ("tie", "tied"):
        pts += [(sb * 0.70 + dx, 0.92)]
    return "".join(o), pts


def _hat_wig19(k, C, yaw):
    W = C["wig19"]
    col = C["hat_colors"]
    o, pts = _wig_svg(k, C, yaw, W["style"], col, W.get("hair_dy", 0.0))
    o = '<g transform="rotate(%.3f)">%s</g>' % (C["hat_tilt"], o)
    C4._ext_hat(k, C, pts)
    top = min(p[1] for p in pts)
    return o, (-0.03 * yaw, top)


def _hat_tricornhair19(k, C, yaw):
    """a tricorne over own hair tied back (CAST hair19 colours, wig style 'tied'): hair at the temples and the queue show below the hat."""
    hc = C["hair19"]
    o1, pts = _wig_svg(k, C, yaw, "tied", hc)
    o2, top = C2._hat_tricorn(k, C, yaw)
    return '<g transform="rotate(%.3f)">%s</g>' % (C["hat_tilt"], o1) + o2, top


HATS19 = {"wig19": _hat_wig19, "tricornhair19": _hat_tricornhair19}


# ============================================================================= costumes (torso-local)
def _lace_jabot(k, X, y0, n, w0, col):
    o = []
    for i in range(n - 1, -1, -1):
        w = w0 - 0.006 * i
        cx, cy = X(0.0, y0 + 0.062 * i)
        r = w / 3.0
        o.append('<path d="M%.4f,%.4f a%.4f,%.4f 0 0 0 %.4f,0 a%.4f,%.4f 0 0 0 %.4f,0 a%.4f,%.4f 0 0 0 %.4f,0 L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (cx - w, cy - 0.03, r * 1.15, 0.055, 2 * r, r * 1.15, 0.055, 2 * r, r * 1.15, 0.055, 2 * r, cx + w, cy - 0.03, k.c(col), k.ink))
    return "".join(o)


def _cos_georgian19(k, C, m):
    """one Georgian drawing for all the period men, steered by CAST g19 (flags) and colors:
      coat=True  open coat with a skirt (coat_len), lapel strips in colors lapel (+ gold lace with g19 lace), brass buttons, pocket flaps;
      coat=False the torso base colour is the waistcoat itself (Harrison: shirt sleeves, apron)
      vest       colors vest + vbtn buttons;  shirt (V) + jabot (colors lace) or neckcloth;  star / sash (king);  gown (astro: gold stars)
      apron=True leather apron with bib, strap, tool pocket (+ shavings curls when the pose key shavings is on)."""
    X = _X(m)
    col = C["colors"]
    g = C["g19"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    a = max(1.0, hw / 0.70)
    gold = k.c(GOLDC["base"])
    o = []
    coat = g.get("coat", True)
    # ---- waistcoat (coat open over it)
    if coat and col.get("vest"):
        vp = [X(-0.20 * a, 0.40), X(0.20 * a, 0.40), X(0.27 * a, 0.70), X(0.31 * a, yB - 0.14), X(0.18 * a, yB + 0.05), X(0.0, yB + 0.10), X(-0.18 * a, yB + 0.05),
              X(-0.31 * a, yB - 0.14), X(-0.27 * a, 0.70)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(vp), C2._grad(k, "vs", col["vest"], -0.4, 0.4), k.ink))
        if g.get("vest_lace"):
            o.append(_ln([X(-0.19 * a, 0.42), X(-0.30 * a, 0.72), X(-0.30 * a, yB - 0.13), X(-0.17 * a, yB + 0.04), X(0.0, yB + 0.09), X(0.17 * a, yB + 0.04),
                           X(0.30 * a, yB - 0.13), X(0.30 * a, 0.72), X(0.19 * a, 0.42)], gold, 0.012, ' opacity="0.9"'))
    # ---- shirt V and neck
    sh = k.c(col.get("shirt", "#f4eee0"))
    o.append(_poly(k, [X(-0.12, 0.39), X(0.12, 0.39), X(0.07 * a, TT + h * 0.46), X(0.0, TT + h * 0.50), X(-0.07 * a, TT + h * 0.46)], sh, 0.012))
    if g.get("jabot"):
        o.append(_lace_jabot(k, X, 0.45, 5, 0.105, col.get("lace", "#ffffff")))
    else:
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (X(-0.12, 0.40) + X(0, 0.47) + X(0.12, 0.40) + (k.ink,)))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (X(-0.12, 0.40) + X(0, 0.47) + X(0.12, 0.40) + (k.c(col.get("neck", "#f4eee0")),)))
        o.append('<path d="M%.4f,%.4f q0.02,0.07 0.0,0.13 M%.4f,%.4f q-0.02,0.07 0.0,0.13" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (X(-0.02, 0.45) + X(0.02, 0.45) + (k.ink,)))
        o.append('<path d="M%.4f,%.4f q0.02,0.07 0.0,0.13 M%.4f,%.4f q-0.02,0.07 0.0,0.13" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (X(-0.02, 0.45) + X(0.02, 0.45) + (k.c(col.get("neck", "#f4eee0")),)))
    # ---- waistcoat buttons + welts
    nb = g.get("vbtn", 6)
    if col.get("vest_b"):
        y0, y1 = TT + h * 0.52, yB - 0.10
        for i in range(nb):
            y = y0 + (y1 - y0) * i / max(1, nb - 1)
            o.append(_circ(X(0.0, y), 0.020, k.c(col["vest_b"]), k, 0.008))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.007" fill="#ffffff" opacity="0.7"/>' % (X(-0.006, y - 0.006)[0], X(-0.006, y - 0.006)[1]))
    else:
        o.append(_ln([X(0.0, TT + h * 0.52), X(0.0, yB)], k.c(col.get("dark", "#3e2414")), 0.010))
    for s in (-1, 1):
        o.append(_ln([X(s * 0.12 * a, yB - 0.20), X(s * 0.27 * a, yB - 0.22)], k.c(col.get("dark", "#2a1a14")), 0.016))
    # ---- coat fronts (lapel strips), buttons
    ov = []
    if coat:
        lap = k.c(col.get("lapel", col["base"]))
        for s in (-1, 1):
            lp = [X(s * 0.12, 0.38), X(s * 0.24 * a, 0.42), X(s * 0.34 * a, 0.56), X(s * 0.30 * a, 0.80), X(s * 0.31 * a, yB - 0.14), X(s * 0.20 * a, yB + 0.05), X(s * 0.12 * a, yB + 0.02),
                  X(s * 0.17 * a, yB - 0.22), X(s * 0.19 * a, 0.80), X(s * 0.13 * a, 0.50)]
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(lp), lap, k.ink))
            if g.get("lace"):
                o.append(_ln([X(s * 0.13 * a, 0.50), X(s * 0.19 * a, 0.80), X(s * 0.17 * a, yB - 0.22), X(s * 0.12 * a, yB + 0.02)], gold, 0.014))
                o.append(_ln([X(s * 0.24 * a, 0.42), X(s * 0.34 * a, 0.56), X(s * 0.30 * a, 0.80), X(s * 0.31 * a, yB - 0.14)], gold, 0.012, ' opacity="0.9"'))
            nbc = g.get("cbtn", 4)
            for i in range(nbc):
                y = 0.64 + i * (yB - 0.22 - 0.64) / max(1, nbc - 1)
                o.append(_circ(X(s * 0.24 * a, y), 0.022, gold, k, 0.008))
            if g.get("stars"):
                pass
            o.append(_ln([X(s * 0.12 * a, yB - 0.18), X(s * 0.30 * a, yB - 0.20)], k.c(col.get("dark", "#1a1418")), 0.020))
            o.append(_circ(X(s * 0.31 * a, yB - 0.20), 0.020, gold, k, 0.008))
    # ---- sash and star (king)
    if g.get("sash"):
        p0, p1 = X(0.30 * a, 0.34), X(-0.26 * a, yB + 0.02)
        dxs, dys = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dxs, dys)
        nx, ny = -dys / L * 0.065, dxs / L * 0.065
        sp = [(p0[0] + nx, p0[1] + ny), (p0[0] - nx, p0[1] - ny), (p1[0] - nx, p1[1] - ny), (p1[0] + nx, p1[1] + ny)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(sp), k.c(col["sash"]), k.ink))
        o.append(_ln([(p0[0] + nx * 0.55, p0[1] + ny * 0.55), (p1[0] + nx * 0.55, p1[1] + ny * 0.55)], k.c(col.get("sash_l", "#6a8ad8")), 0.010, ' opacity="0.8"'))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.050" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="%.4f" cy="%.4f" r="0.016" fill="%s"/>'
                 % (p1[0], p1[1], k.c(col["sash"]), k.ink, p1[0], p1[1], gold))
    if g.get("star"):
        c = X(0.30 * a, 0.70)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(_star(c[0], c[1], 0.125, 8, 0.52, -90)), k.c(SILVER["base"]), k.ink))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (_poly_d(_star(c[0], c[1], 0.095, 8, 0.50, -67.5)), k.c(SILVER["light"]), k.ink))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.046" fill="%s" stroke="%s" stroke-width="0.010"/>' % (c[0], c[1], k.c("#f4f0e6"), k.ink))
        o.append('<path d="M%.4f,%.4f h0.060 M%.4f,%.4f v0.060" stroke="%s" stroke-width="0.016"/>' % (c[0] - 0.03, c[1], c[0], c[1] - 0.03, k.c("#b8322a")))
    # ---- gown stars (astronomer): small gold stars embroidered on the gown colour
    if g.get("stars"):
        pos = ((-0.52, 0.52), (-0.44, 0.88), (-0.58, 1.18), (0.50, 0.50), (0.46, 0.86), (0.56, 1.14), (-0.40, yB - 0.10), (0.42, yB - 0.12), (-0.62, 0.74), (0.60, 0.72))
        for i, (x, y) in enumerate(pos):
            if y < yB - 0.02 and (abs(x) * a < hw * 0.92):
                c = X(x * a, y)
                o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.007" stroke-linejoin="round"/>' % (_poly_d(_star(c[0], c[1], 0.050 + 0.008 * (i % 2), 5, 0.45, -90 + 12 * i)), gold, k.ink))
    # ---- leather apron (Harrison)
    if g.get("apron"):
        ap = C2._grad(k, "ap", col["apron"], -0.4, 0.4)
        bw = 0.19 * a
        bib = [X(-bw, 0.60), X(bw, 0.60), X(bw + 0.04 * a, yB - 0.12), X(-bw - 0.04 * a, yB - 0.12)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(bib), ap, k.ink))
        for s in (-1, 1):
            o.append(_ln([X(s * (bw - 0.02), 0.61), X(s * 0.10, 0.40)], k.ink, 0.040))
            o.append(_ln([X(s * (bw - 0.02), 0.61), X(s * 0.10, 0.40)], k.c(col["apron"]), 0.026))
        # tool pocket on the bib: file, chisel, a rule and a pencil
        px0, px1, py0, py1 = -0.150 * a, 0.020 * a, 0.80, 0.98
        tools = (("#a8743c", "#9aa2b0", -0.115 * a, 0.50, 0.075), ("#5e3c1c", "#cfd5df", -0.065 * a, 0.46, 0.090), ("#d8b878", "#d8b878", -0.012 * a, 0.40, 0.060))
        for i, (hc_, bc_, x, hgt, wd) in enumerate(tools):
            xx, yy = X(x, py0)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (xx, yy, xx + 0.005 * i, yy - 0.15 - 0.025 * i, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (xx, yy, xx + 0.005 * i, yy - 0.15 - 0.025 * i, k.c(bc_)))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (xx + 0.005 * i, yy - 0.15 - 0.025 * i, xx + 0.006 * i, yy - 0.215 - 0.025 * i, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (xx + 0.005 * i, yy - 0.15 - 0.025 * i, xx + 0.006 * i, yy - 0.215 - 0.025 * i, k.c(hc_)))
        pk = [X(px0, py0), X(px1, py0), X(px1 - 0.005, py1), X(px0 + 0.005, py1)]
        o.append(_poly(k, pk, k.c(col["apron_d"]), 0.016))
        o.append(_ln([X(px0 + 0.015, py0 + 0.03), X(px1 - 0.015, py0 + 0.03)], k.c(col["apron"]), 0.010, ' opacity="0.8"'))
        if _POSE19["shav"] > 0.5:
            for (sx, sy, sr) in ((0.10, 0.70, 1.0), (0.17, 0.90, 0.8), (0.02, yB - 0.20, 0.9)):
                c = X(sx * a, sy)
                o.append('<path d="M%.4f,%.4f c%.3f,%.3f %.3f,%.3f %.3f,%.3f s%.3f,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                         % (c[0], c[1], 0.03 * sr, -0.045 * sr, 0.08 * sr, -0.005 * sr, 0.05 * sr, 0.04 * sr, -0.07 * sr, 0.025 * sr, -0.06 * sr, -0.010 * sr, k.c(HONEY)))
    inside = "".join(o)
    # ---- skirt of the coat / gown, apron skirt over the legs
    yt = yB - 0.12
    if coat:
        hem = yB + C.get("coat_len", 0.46)
        b = hw + C.get("coat_flare", 0.12)
        gr = "url(#%s_tg)" % k.uid
        ov.append(C2._skirt(k, "gc", X, yt, hw * 0.985, hem, b, gr, sw=0.026,
                            folds=((-0.14, yt + 0.14, -0.20, hem - 0.04), (0.16, yt + 0.14, 0.22, hem - 0.04), (0.0, yt + 0.20, 0.01, hem - 0.05)), fold_col=k.c(col.get("dark", "#1a1418"))))
        ov.append(_ln([X(0.0, yt + 0.02), X(0.01, hem - 0.01)], k.ink, 0.014))
        if g.get("lace"):
            ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.95"/>' % (X(-b * 0.96, hem - 0.04) + X(0, hem - 0.02 + 0.03) + X(b * 0.96, hem - 0.04) + (gold,)))
        if g.get("stars"):
            for i, (x, y) in enumerate(((-0.55, 0.30), (-0.2, 0.36), (0.25, 0.30), (0.55, 0.36), (0.0, 0.18))):
                if yB + y < hem - 0.05:
                    c = X(x * a, yB + y)
                    ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.007" stroke-linejoin="round"/>' % (_poly_d(_star(c[0], c[1], 0.050, 5, 0.45, -90 + 20 * i)), gold, k.ink))
    if g.get("apron"):
        ya = yB - 0.14
        aa = hw * 0.80
        ahem = yB + 0.50
        ov.append(C2._skirt(k, "ak", X, ya, aa, ahem, aa + 0.05, C2._grad(k, "apk", col["apron"], -0.4, 0.4), sw=0.022,
                            folds=((-0.10, ya + 0.16, -0.13, ahem - 0.05), (0.12, ya + 0.16, 0.15, ahem - 0.05)), fold_col=k.c(col["apron_d"])))
        ov.append(_ln([X(-hw * 0.98, ya + 0.01), X(hw * 0.98, ya + 0.01)], k.ink, 0.042))
        ov.append(_ln([X(-hw * 0.98, ya + 0.01), X(hw * 0.98, ya + 0.01)], k.c(col["apron_d"]), 0.026))
        if _POSE19["shav"] > 0.5:
            c = X(-0.14, ahem - 0.20)
            ov.append('<path d="M%.4f,%.4f c0.03,-0.045 0.08,-0.005 0.05,0.04 s-0.07,0.025 -0.06,-0.010" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (c[0], c[1], k.c(HONEY)))
            c = X(0.12, ahem - 0.34)
            ov.append('<path d="M%.4f,%.4f c0.03,-0.045 0.08,-0.005 0.05,0.04 s-0.07,0.025 -0.06,-0.010" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (c[0], c[1], k.c(HONEY)))
    return inside, "", "".join(ov)


def _cos_slops19(k, C, m):
    """a sailor: a short open jacket (the torso colour) over a striped or checked shirt panel, a knotted kerchief at the throat; the wide slops
    are the CAST shorts (wide, to the calf)."""
    X = _X(m)
    col = C["colors"]
    g = C["g19"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    a = max(1.0, hw / 0.70)
    o = []
    poly = [X(-0.24 * a, 0.38), X(0.24 * a, 0.38), X(0.21 * a, yB - 0.02), X(0.0, yB + 0.03), X(-0.21 * a, yB - 0.02)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(poly), k.c(col["shirt"]), k.ink))
    k.defs.append('<clipPath id="%s_sp"><path d="%s"/></clipPath>' % (k.uid, _poly_d(poly)))
    st = []
    y = 0.36
    if g.get("check"):
        while y < yB + 0.05:
            st.append('<path d="M-1.2,%.4f L1.2,%.4f" stroke="%s" stroke-width="0.045" opacity="0.8"/>' % (y, y, k.c(col["stripe"])))
            y += 0.11
        x = -1.0
        while x < 1.0:
            st.append('<path d="M%.4f,0.3 L%.4f,%.4f" stroke="%s" stroke-width="0.045" opacity="0.8"/>' % (X(x, 0.5)[0], X(x, 0.5)[0], yB + 0.1, k.c(col["stripe"])))
            x += 0.11
    else:
        while y < yB + 0.05:
            st.append('<path d="M-1.2,%.4f L1.2,%.4f" stroke="%s" stroke-width="0.052"/>' % (y, y, k.c(col["stripe"])))
            y += 0.105
    o.append('<g clip-path="url(#%s_sp)">%s</g>' % (k.uid, "".join(st)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(poly), k.ink))
    for s in (-1, 1):
        o.append(_ln([X(s * 0.24 * a, 0.38), X(s * 0.22 * a, yB - 0.02)], k.c(col.get("dark", "#1a1418")), 0.012))
        for i in range(2):
            o.append(_circ(X(s * 0.30 * a, 0.80 + i * 0.22), 0.020, k.c(col.get("button", "#d8c070")), k, 0.008))
    # kerchief
    kc = k.c(col["kerchief"])
    c = X(0.0, 0.46)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (X(-0.18, 0.37) + X(0.18, 0.37) + X(0.04, 0.66) + X(0.0, 0.72) + X(-0.04, 0.66) + (kc, k.ink)))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.034" fill="%s" stroke="%s" stroke-width="0.012"/>' % (c[0] + 0.015, c[1] + 0.075, kc, k.ink))
    o.append('<path d="M%.4f,%.4f q0.05,0.05 0.03,0.11 M%.4f,%.4f q-0.04,0.05 -0.05,0.10" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (c[0], c[1] + 0.08, c[0], c[1] + 0.08, k.ink))
    o.append('<path d="M%.4f,%.4f q0.05,0.05 0.03,0.11 M%.4f,%.4f q-0.04,0.05 -0.05,0.10" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (c[0], c[1] + 0.08, c[0], c[1] + 0.08, kc))
    yt = yB - 0.12
    hem = yB + C.get("jacket_len", 0.16)
    ov = [C2._skirt(k, "sj", X, yt, hw * 0.985, hem, hw + 0.05, "url(#%s_tg)" % k.uid, sw=0.024, folds=((-0.14, yt + 0.06, -0.16, hem - 0.03), (0.15, yt + 0.06, 0.17, hem - 0.03)),
                    fold_col=k.c(col.get("dark", "#1a1418")))]
    ov.append(_ln([X(-hw * 0.99, yB - 0.10), X(hw * 0.99, yB - 0.10)], k.ink, 0.050))
    ov.append(_ln([X(-hw * 0.99, yB - 0.10), X(hw * 0.99, yB - 0.10)], k.c(col.get("belt", "#4a3220")), 0.032))
    bx, by = X(0.02, yB - 0.10)
    ov.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.050" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx - 0.03, by - 0.025, k.c("#d8c070"), k.ink))
    return "".join(o), "", "".join(ov)


COSTUMES19 = {"georgian19": _cos_georgian19, "slops19": _cos_slops19}


# ============================================================================= face: spectacles pushed up, flush
def _specs_up(k, C, P_, L):
    if not C.get("specs_up19"):
        return ""
    yaw = P_.get("yaw", 0.0) if isinstance(P_, dict) else 0.0
    cx = (L["xL"] + L["xR"]) / 2.0
    y = L["ey"] - 0.255
    o = []
    for s in (-1, 1):
        x = cx + s * 0.135
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.098" ry="0.082" fill="#dff0f6" fill-opacity="0.55" stroke="%s" stroke-width="0.030"/>' % (x, y, k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.098" ry="0.082" fill="none" stroke="%s" stroke-width="0.016"/>' % (x, y, k.c("#e2b442")))
        o.append('<path d="M%.4f,%.4f q0.03,-0.04 0.07,-0.035" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.9"/>' % (x - 0.05, y - 0.01))
    o.append('<path d="M%.4f,%.4f q0.0,-0.03 0.04,-0.0" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (cx - 0.04, y - 0.01, k.ink))
    o.append('<path d="M%.4f,%.4f q0.0,-0.03 0.04,-0.0" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (cx - 0.04, y - 0.01, k.c("#e2b442")))
    return "".join(o)


def _nose19(k, C, P_, L):
    c = C.get("nose19")
    if not c:
        return ""
    cx = (L["xL"] + L["xR"]) / 2.0
    cy = L["ey"] + (L["my"] - L["ey"]) * 0.42
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.036" fill="%s" stroke="%s" stroke-width="0.012"/><ellipse cx="%.4f" cy="%.4f" rx="0.013" ry="0.009" fill="#ffffff" opacity="0.6"/>'
            % (cx, cy, k.c(c), k.ink, cx - 0.015, cy - 0.015))


def _face(k, C, P_, white):
    svg, L = _O19["_face"](k, C, P_, white)
    if C is None or not C.get("_cast19"):
        return svg, L
    return _nose19(k, C, P_, L) + svg + _specs_up(k, C, P_, L), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE19["shav"] = _f(g("shavings"), 1.0, 0.0, 1.0)
    _POSE19["splash"] = _f(g("splash"), 0.0, 0.0, 1.0)
    _POSE19["glint"] = _f(g("glint"), 0.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE19["t"] = t if math.isfinite(t) else 0.0
    return _O19["_norm"](C, pose)


# ============================================================================= legs: stockings and buckled red-heeled shoes
def _stocking(k, S, E, H, kk, w, SL):
    """a stocking drawn from the end of the breeches (fraction SL['from']) to the ankle (fraction SL['to']) of a leg."""
    pts = C3._limb_pts(S, E, H, kk)
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1]
    if tot < 1e-6:
        return ""
    a, b = SL["from"] * tot, SL["to"] * tot
    sel = []
    for i in range(1, len(pts)):
        if cum[i] < a:
            continue
        if not sel:
            f = (a - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            sel.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f))
        if cum[i] >= b:
            f = (b - cum[i - 1]) / max(cum[i] - cum[i - 1], 1e-9)
            sel.append((pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * f, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f))
            break
        sel.append(pts[i])
    if len(sel) < 2:
        return ""
    d = "M" + " L".join("%.4f,%.4f" % p for p in sel)
    sw = SL.get("w", w + 0.050)
    o = '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.ink, sw + 0.026)
    o += '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.c(SL["color"]), sw)
    o += '<path d="%s" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.5" transform="translate(-0.018 0)"/>' % d
    return o


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O19["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = C4._cur()
    if C is None or not C.get("_cast19") or tail is None:
        return out
    if C.get("stock19"):
        out += _stocking(k, S, E, H, kk, w, C["stock19"])
        if C.get("boots"):
            out += C2._boot(k, H, tail, w, C["boots"])
    sh = C.get("shoe19")
    if sh:
        tx = tail[0] - H[0]
        s = 1.0 if tx >= 0 else -1.0
        sole = H[1] + w / 2 + 0.008
        if sh.get("heel"):
            hx = H[0] - s * 0.052
            out += '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (
                hx - 0.030, sole - 0.050, hx + 0.034, sole - 0.050, hx + 0.034, sole + 0.012, hx - 0.030, sole + 0.012, k.c(sh["heel"]), k.ink)
        if sh.get("buckle"):
            bx, by = H[0] + s * 0.055, sole - 0.092
            out += '<rect x="%.4f" y="%.4f" width="0.050" height="0.056" rx="0.008" fill="none" stroke="%s" stroke-width="0.020"/>' % (bx - 0.025, by - 0.028, k.ink)
            out += '<rect x="%.4f" y="%.4f" width="0.050" height="0.056" rx="0.008" fill="none" stroke="%s" stroke-width="0.011"/>' % (bx - 0.025, by - 0.028, k.c(sh["buckle"]))
    return out


# ============================================================================= variants, stool, figure
def _variant(name, pose):
    if not isinstance(pose, dict):
        return name
    if name == "harrison19":
        if pose.get("old"):
            return "harrison19_old"
        if pose.get("young"):
            return "harrison19_young"
    if name == "william19" and pose.get("hat_off"):
        return "william19_bare"
    if name == "captain19" and pose.get("hat_off"):
        return "captain19_bare"
    return name


def _stool_svg(k, cx, y_seat, y_floor, w):
    o = []
    for dx_ in (-0.62, 0.62, 0.0):
        x1 = cx + dx_ * w * 0.5
        x0 = cx + dx_ * w * 0.36
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.100" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>'
                 % (x0, y_seat + 0.05, x1, y_floor - 0.03, k.ink, x0, y_seat + 0.05, x1, y_floor - 0.03, k.c(WOOD["base"] if dx_ else WOOD["dark"])))
    g = _g3(k, "stl", WOOD, cx - w / 2, 0, cx + w / 2, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (cx - w / 2, y_seat, cx + w / 2, y_seat, cx + w / 2 - 0.02, y_seat + 0.10, cx - w / 2 + 0.02, y_seat + 0.10, k.c(WOOD["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="0.075" fill="%s" stroke="%s" stroke-width="0.022"/>' % (cx, y_seat, w / 2, g, k.ink))
    return "".join(o), (cx - w / 2 - 0.1, y_seat - 0.08, cx + w / 2 + 0.1, y_floor + 0.05)


STOOP19 = dict(lean=8.0, head_dy=0.05, head_dx=0.04)


def figure(cast_name, pose=None, uid="p"):
    name = _variant(cast_name, pose)
    if name == "harrison19_old" and isinstance(pose, dict):
        pose = dict(STOOP19, **pose)
    f = _O19["figure"](name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    st = _f(pose.get("stool"), 0.0, 0.0, 1.0)
    if st < 0.5:
        return f
    k = P._Ctx(uid + "w", P.INK, None)
    an = dict(f["anchors"])
    w = _f(pose.get("stool_w"), 0.95, 0.4, 2.0)
    dx_ = _f(pose.get("stool_dx"), -0.10, -1.0, 1.0)
    yseat = an["hip"][1] + _f(pose.get("stool_dy"), 0.16, -0.5, 1.0)
    s, bb = _stool_svg(k, an["hip"][0] + dx_, yseat, f["feet_y"], w)
    b = list(f["bbox"])
    b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
    an["seat"] = (an["hip"][0] + dx_, yseat)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + s + f["svg"], bbox=tuple(b), anchors=an)


def laugh_cycle(phase, base=None, hz_cycles=3):
    """a laugh as a pose: belly bounce (squash 1.03/0.97 <-> 0.99/1.01), head roll rocking and tears; phase 0..1 loops (3 bounces per loop)."""
    p = dict(base or {})
    s = math.sin(phase * 2 * math.pi * hz_cycles)
    p["squash"] = (1.01 + 0.02 * s, 0.99 - 0.02 * s)
    p["head_roll"] = (p.get("head_roll", 0.0)) + 3.0 * math.sin(phase * 2 * math.pi * hz_cycles * 0.5)
    p["t"] = phase
    p.setdefault("expr", "laughing")
    return p


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast19=True)


def _mk(base, **kw):
    d = dict(P.CAST[base])
    d.update(_FLAGS)
    d.update(kw)
    return d


def hair_cols(light, base, dark, shine=None):
    return dict(light=light, base=base, dark=dark, shine=shine or "#ffffff")


POWDER = hair_cols("#fffefa", "#f0ece6", "#b4b0aa")
GREYW = hair_cols("#e0dddc", "#b8b4b4", "#7e7a7c")
H_BROWN = hair_cols("#8a6a4a", "#5e4228", "#33221a", "#b08860")
H_GREY = hair_cols("#c8c0b4", "#9a9086", "#6a6258", "#e8e0d4")
H_WHITE = hair_cols("#ffffff", "#ece8e2", "#b6b2ac", "#ffffff")
H_BROWN2 = hair_cols("#7a5a3a", "#4e3420", "#2a1a10", "#a0784c")
H_BLACK = hair_cols("#5a4a48", "#2e2626", "#161012", "#8a7a78")


def _cast_table():
    T = {}
    # ---------------- Harrison: lean, kind, determined; the 1750s workshop carpenter (greying hair), a brown waistcoat, a leather apron
    hcol = dict(base="#6e4630", dark="#3a2214", lapel="#6e4630", vest="#6e4630", vest_b="#e2b442", shirt="#f2ead6", neck="#f4efe2", apron="#c9a06c", apron_d="#8a6238")
    hs = dict(
        build="slim", seed=191.3, torso_w=0.66, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15, leg=1.28,
        stance=0.06, wide=0.26, limb_w=0.056, eye_y=0.030, brow="stroke", brow_th=0.052, mouth="smile", moustache=False, cheeks="#eaa890", age_lines=True,
        hat="newsboy", hat_style="wig19", hat_tilt=0.0, wig19=dict(style="tied"), hat_colors=dict(H_GREY), hair=dict(color="#9a9086", front=0.0, grow=0.0), ear_pencil=False,
        costume="georgian19", g19=dict(coat=False, apron=True, vbtn=6), neck="cravat", coat_len=0.0, chain=False, flower=None,
        sleeve=dict(color="#f2ead6", dark="#c8bda0", cuff="#f2ead6", len=0.50, w=0.150, roll=True),
        shorts=dict(color="#c8ae80", dark="#8a7450", cuff="#b89a68", len=0.52, w=0.118),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#efe6d0"}),
        boots=dict(color="#2a1e18", cuff="#2a1e18", h=0.06, toe=0.15), shoe19=dict(buckle="#d8d8e0"), colors=dict(hcol))
    T["harrison19"] = _mk("gentleman", **hs)
    T["harrison19_young"] = dict(T["harrison19"], seed=191.9, hat_colors=dict(H_BROWN), hair=dict(color="#5e4228", front=0.0, grow=0.0), age_lines=False, cheeks="#f0a890")
    T["harrison19_old"] = dict(
        T["harrison19"], seed=192.4, hat_colors=dict(H_WHITE), hair=dict(color="#ece8e2", front=0.0, grow=0.0), glasses=True, age_lines=True, leg=1.30, torso_h=1.00,
        g19=dict(coat=True, apron=False, vbtn=6, cbtn=0), coat_len=0.50, coat_flare=0.10,
        colors=dict(hcol, base="#7a5030", dark="#3e2414", lapel="#7a5030", vest="#b88a50", vest_b="#e2b442"),
        sleeve=dict(color="#7a5030", dark="#3e2414", cuff="#f2ead6", len=0.84, w=0.150),
        shorts=dict(color="#a99a82", dark="#7a6e58", cuff="#8a7a60", len=0.52, w=0.118), brow_th=0.048, mouth="smile")
    # ---------------- William
    wcol = dict(base="#3f6a9c", dark="#22405e", lapel="#3f6a9c", vest="#e6d29c", vest_b="#e2b442", shirt="#f6f0e0", neck="#f6f0e0", lace="#ffffff")
    T["william19"] = _mk(
        "gentleman", seed=193.1, build="slim", torso_w=0.68, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.26, 0.50), arm=0.76, hip_x=0.15, leg=1.40,
        stance=0.06, wide=0.26, limb_w=0.056, eye_y=0.040, brow="stroke", brow_th=0.048, mouth="smile", moustache=False, cheeks="#f2a896", age_lines=False,
        hat="newsboy", hat_style="tricornhair19", hat_tilt=-3.0, hat_colors=dict(light="#4a4552", base="#2b2731", dark="#19161d", shine="#9e98ad", lace="#d8b858", cockade="#c7332b", brass="#e0c063"),
        hair19=dict(H_BROWN2), hair=dict(color="#4e3420", front=0.0, grow=0.0), ear_pencil=False,
        costume="georgian19", g19=dict(coat=True, vbtn=7, cbtn=4), coat_len=0.50, coat_flare=0.12, neck="cravat", chain=False,
        sleeve=dict(color="#3f6a9c", dark="#22405e", cuff="#7aa0c8", len=0.84, w=0.150),
        shorts=dict(color="#f0e4c8", dark="#c8b890", cuff="#d8c8a0", len=0.52, w=0.118), stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#f6f2ea"}),
        boots=dict(color="#1e1618", cuff="#1e1618", h=0.06, toe=0.15), shoe19=dict(buckle="#e2b442"), colors=dict(wcol))
    T["william19_bare"] = dict(T["william19"], hat_style="wig19", wig19=dict(style="tied"), hat_colors=dict(H_BROWN2), hat_tilt=0.0)
    # ---------------- the mocker: a plump, florid astronomer in a full-bottomed wig, a navy gown with gold stars over a crimson waistcoat
    acol = dict(base="#26335e", dark="#121a34", lapel="#34457a", vest="#a82a38", vest_b="#e2b442", shirt="#fffaf0", lace="#ffffff", neck="#ffffff")
    T["astro19"] = _mk(
        "admiral", seed=194.1, build="stout", torso_w=1.50, torso_h=1.20, profile=C2.PROFILE_ROUND, shift_pow=1.25, shoulder=(0.50, 0.44), arm=0.80, hip_x=0.20, leg=1.22,
        stance=0.07, wide=0.32, limb_w=0.070, eye_y=0.000, brow="stroke", brow_th=0.082, mouth="smile", moustache=False, cheeks="#ec5a4c", chins=True, nose19="#ec7a68",
        specs_up19=True, hat="newsboy", hat_style="wig19", hat_tilt=0.0, wig19=dict(style="full"), hat_colors=dict(POWDER), ear_pencil=False, hair=dict(color="#f0ece6", front=0.0, grow=0.0),
        costume="georgian19", g19=dict(coat=True, jabot=True, stars=True, vbtn=7, cbtn=0, vest_lace=True), coat_len=0.62, coat_flare=0.16,
        sleeve=dict(color="#26335e", dark="#121a34", cuff="#fffaf0", len=0.84, w=0.215), shorts=dict(color="#e8dcc0", dark="#b8a888", cuff="#c8b890", len=0.52, w=0.17),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#f2ece0", "w": 0.15}), boots=dict(color="#16141a", cuff="#16141a", h=0.07, toe=0.17), shoe19=dict(buckle="#e2b442"), colors=dict(acol))
    for kk in ("epaulette10", "gloves10", "moustache_style", "tache_scale", "braid"):
        T["astro19"].pop(kk, None)
    # thin and tall: grey bob wig, black coat
    T["astro19_b"] = _mk(
        "gentleman", seed=194.7, build="slim", torso_w=0.54, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.22, 0.50), arm=0.78, hip_x=0.14, leg=1.58,
        stance=0.06, wide=0.24, limb_w=0.050, eye_y=0.040, brow="stroke", brow_th=0.046, mouth="frown", moustache=False, cheeks="#e6b0a0", age_lines=True, glasses=False,
        hat="newsboy", hat_style="wig19", hat_tilt=0.0, wig19=dict(style="bob"), hat_colors=dict(GREYW), ear_pencil=False, hair=dict(color="#b8b4b4", front=0.0, grow=0.0),
        costume="georgian19", g19=dict(coat=True, jabot=False, vbtn=7, cbtn=5), coat_len=0.60, coat_flare=0.10, neck="tie",
        sleeve=dict(color="#26222a", dark="#121014", cuff="#f4f0e6", len=0.84, w=0.128), shorts=dict(color="#26222a", dark="#121014", cuff="#26222a", len=0.52, w=0.105),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#d8d4cc", "w": 0.088}), boots=dict(color="#16141a", cuff="#16141a", h=0.07, toe=0.15), shoe19=dict(buckle="#c8ccd6"),
        colors=dict(base="#2c2830", dark="#121014", lapel="#2c2830", vest="#8c8a94", vest_b="#c8ccd6", shirt="#fbf8f0", neck="#ffffff", lace="#ffffff"))
    # short and bald: a small tie wig set back on a high bald forehead, green coat
    T["astro19_c"] = _mk(
        "gentleman", seed=195.2, build="regular", torso_w=0.96, torso_h=0.92, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.34, 0.47), arm=0.74, hip_x=0.17, leg=1.00,
        stance=0.06, wide=0.28, limb_w=0.064, eye_y=0.010, brow="stroke", brow_th=0.066, mouth="smirk", moustache=False, cheeks="#ec9482", age_lines=True,
        hat="newsboy", hat_style="wig19", hat_tilt=0.0, wig19=dict(style="tie", hair_dy=0.20), hat_colors=dict(hair_cols("#e4ded2", "#c8c0b0", "#8a8274")), ear_pencil=False,
        hair=dict(color="#c8c0b0", front=0.0, grow=0.0),
        costume="georgian19", g19=dict(coat=True, jabot=False, vbtn=6, cbtn=4), coat_len=0.52, coat_flare=0.12, neck="tie",
        sleeve=dict(color="#3e6a48", dark="#22402c", cuff="#e8d8a8", len=0.84, w=0.165), shorts=dict(color="#d8c88e", dark="#a89a64", cuff="#a89a64", len=0.52, w=0.13),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#ece4d0", "w": 0.11}), boots=dict(color="#2a1e18", cuff="#2a1e18", h=0.07, toe=0.16), shoe19=dict(buckle="#d8d8e0"),
        colors=dict(base="#3e6a48", dark="#22402c", lapel="#3e6a48", vest="#d8c48c", vest_b="#e2b442", shirt="#fbf8f0", neck="#ffffff", lace="#ffffff"))
    # ---------------- the king: powdered wig with side curls, blue coat, Garter star and sash, white breeches, red heels
    T["king19"] = _mk(
        "gentleman", seed=196.1, build="regular", torso_w=0.84, torso_h=1.02, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.30, 0.48), arm=0.76, hip_x=0.16, leg=1.34,
        stance=0.06, wide=0.27, limb_w=0.060, eye_y=0.020, brow="stroke", brow_th=0.060, mouth="smile", moustache=False, cheeks="#f0a090", age_lines=False, chins=False,
        hat="newsboy", hat_style="wig19", hat_tilt=0.0, wig19=dict(style="king"), hat_colors=dict(POWDER), ear_pencil=False, hair=dict(color="#f0ece6", front=0.0, grow=0.0),
        costume="georgian19", g19=dict(coat=True, jabot=True, sash=True, star=True, lace=True, vbtn=7, cbtn=4, vest_lace=True), coat_len=0.56, coat_flare=0.14,
        sleeve=dict(color="#2b4a96", dark="#152a5a", cuff="#f6f0e0", len=0.84, w=0.165), shorts=dict(color="#faf6ec", dark="#d8d0bc", cuff="#d8d0bc", len=0.52, w=0.126),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#fbf8f0"}), boots=dict(color="#16141a", cuff="#16141a", h=0.06, toe=0.15), shoe19=dict(buckle="#f0f0f6", heel="#c8302a"),
        colors=dict(base="#2b4a96", dark="#152a5a", lapel="#2b4a96", vest="#ecdca4", vest_b="#e2b442", shirt="#fffaf0", lace="#ffffff", neck="#ffffff", sash="#3a62c0", sash_l="#7a9ae8"))
    # ---------------- the captain: navy coat, white facings, gold lace, cocked hat over tied hair
    T["captain19"] = _mk(
        "gentleman", seed=197.3, build="regular", torso_w=0.90, torso_h=1.04, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.32, 0.48), arm=0.76, hip_x=0.16, leg=1.40,
        stance=0.07, wide=0.28, limb_w=0.062, eye_y=0.010, brow="stroke", brow_th=0.064, mouth="frown", moustache=False, cheeks="#e89480", age_lines=True,
        hat="newsboy", hat_style="tricornhair19", hat_tilt=-4.0, hat_colors=dict(light="#3a4262", base="#1c2240", dark="#0e1226", shine="#8a92b6", lace="#e2b442", cockade="#14141a", brass="#e0c063"),
        hair19=dict(H_GREY), hair=dict(color="#9a9086", front=0.0, grow=0.0), ear_pencil=False,
        costume="georgian19", g19=dict(coat=True, jabot=False, lace=True, vbtn=7, cbtn=5), coat_len=0.58, coat_flare=0.12, neck="tie",
        sleeve=dict(color="#1f2c52", dark="#0e1632", cuff="#f2eee0", len=0.84, w=0.158), shorts=dict(color="#efe4c4", dark="#c8bc98", cuff="#d0c4a0", len=0.52, w=0.125),
        stock19=dict(**{"from": 0.52, "to": 0.88, "color": "#f2eee0"}), boots=dict(color="#16141a", cuff="#16141a", h=0.06, toe=0.15), shoe19=dict(buckle="#e2b442"),
        colors=dict(base="#1f2c52", dark="#0e1632", lapel="#f2eee0", vest="#efe4c4", vest_b="#e2b442", shirt="#fbf8f0", neck="#ffffff", lace="#e2b442"))
    T["captain19_bare"] = dict(T["captain19"], hat_style="wig19", wig19=dict(style="tied"), hat_colors=dict(H_GREY), hat_tilt=0.0)
    # ---------------- the sailors: slops (wide trousers), short jackets, striped or checked shirts
    sb = dict(build="regular", profile=CE.PROFILE_PEAR, shift_pow=1.05, hip_x=0.16, stance=0.07, wide=0.28, ear_pencil=False, moustache=False,
              costume="slops19", boots=None)
    T["sailor19_a"] = _mk(
        "worker1", seed=198.1, torso_w=0.90, torso_h=0.98, shoulder=(0.32, 0.47), arm=0.74, leg=1.16, limb_w=0.062, eye_y=0.020, brow="stroke", brow_th=0.060, mouth="grin", cheeks="#e89480",
        hat_style="knit", hat_tilt=-5.0, hat_colors=dict(light="#6a82b8", base="#3e5a94", dark="#22345e", stripe="#e8dcc0", cuff="#2c4474", pom="#e8dcc0", ribbon="#b8382e", shine="#9ab0d8"), hair=dict(color="#4a3020", front=0.08, grow=0.22),
        g19=dict(check=False), jacket_len=0.14, sleeve=dict(color="#4a5a78", dark="#2a3650", cuff="#4a5a78", len=0.50, w=0.158, roll=True),
        shorts=dict(color="#e4dcc4", dark="#a89e80", cuff="#c8bea0", len=0.90, w=0.20), boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.05, toe=0.15),
        colors=dict(base="#4a5a78", dark="#2a3650", shirt="#f4ecd8", stripe="#b8382e", kerchief="#e0b838", belt="#4a3220", button="#d8c070"),
        **{k_: v for k_, v in sb.items() if k_ not in ("build", "costume", "boots")}, costume="slops19", build="regular")
    T["sailor19_b"] = _mk(
        "worker1", seed=198.8, torso_w=0.64, torso_h=1.02, shoulder=(0.25, 0.50), arm=0.76, leg=1.30, limb_w=0.056, eye_y=0.040, brow="stroke", brow_th=0.050, mouth="dash", cheeks="#eaa08a",
        hat_style="kerchief", hat_tilt=-3.0, hat_colors=dict(light="#d8584a", base="#b03a2e", dark="#6a1e16", shine="#f09a8a", band="#b03a2e", dot="#f4ecd8"),
        hair=dict(color="#7a5a3a", front=0.08, grow=0.22), g19=dict(check=True), jacket_len=0.14,
        sleeve=dict(color="#6a4a36", dark="#3e2a1c", cuff="#6a4a36", len=0.48, w=0.14, roll=True), shorts=dict(color="#f0e8d0", dark="#b0a88c", cuff="#cfc6a8", len=0.90, w=0.19),
        boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.05, toe=0.15),
        colors=dict(base="#6a4a36", dark="#3e2a1c", shirt="#f4ecd8", stripe="#3e62a8", kerchief="#f4ecd8", belt="#4a3220", button="#d8c070"),
        **{k_: v for k_, v in sb.items() if k_ not in ("build", "costume", "boots", "profile", "shift_pow", "hip_x", "wide")}, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, hip_x=0.15, wide=0.26,
        costume="slops19", build="slim")
    T["sailor19_c"] = _mk(
        "worker1", seed=199.4, torso_w=1.04, torso_h=0.98, shoulder=(0.34, 0.47), arm=0.74, leg=1.08, limb_w=0.064, eye_y=0.010, brow="stroke", brow_th=0.064, mouth="smirk", cheeks="#e8907c",
        hat_style="wig19", wig19=dict(style="tied"), hat_tilt=0.0, hat_colors=dict(H_BLACK), hair=dict(color="#2e2626", front=0.0, grow=0.0), g19=dict(check=False), jacket_len=0.14, age_lines=True,
        sleeve=dict(color="#2c4a52", dark="#16282e", cuff="#2c4a52", len=0.50, w=0.17, roll=True), shorts=dict(color="#d8cdb2", dark="#a09878", cuff="#bcb292", len=0.90, w=0.21),
        boots=None, colors=dict(base="#2c4a52", dark="#16282e", shirt="#f0e8d2", stripe="#2a3a78", kerchief="#c85a3a", belt="#4a3220", button="#d8c070"),
        **{k_: v for k_, v in sb.items() if k_ not in ("build", "costume", "boots")}, costume="slops19", build="regular")
    for kk in ("sailor19_a", "sailor19_b", "sailor19_c"):
        if T[kk].get("boots") is None:
            T[kk].pop("boots", None)
    return T


# ============================================================================= story poses
def _grip2(S, name, hand_from="r", bend=0.5, shape="ball", layer="top", stretch=1.3, anchor="grip_far"):
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["%s_%s" % (anchor, hand_from)]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _story():
    S, M = {}, {}
    HA, HY, HO, WI = "harrison19", "harrison19", "harrison19", "william19"
    AS, AB, AC, KI, CA = "astro19", "astro19_b", "astro19_c", "king19", "captain19"
    SA, SB, SC = "sailor19_a", "sailor19_b", "sailor19_c"

    def add(name, cast, pose, note, shot=None):
        S[name] = (cast, pose)
        M[name] = dict(note=note)
        if shot is not None:
            M[name]["shots"] = shot

    idle = dict(yaw=0.25, expr="neutral", arm_r="down", arm_l="down")
    # ------------------------------------------------------------------ Harrison
    add("harrison_idle", HA, dict(idle), "standing, calm (1750s: greying hair, apron)", "any")
    add("harrison_young_idle", HY, dict(idle, young=1), "the 1730s Harrison: brown hair", "any")
    add("harrison_old_idle", HO, dict(idle, old=1), "about 80: white hair, spectacles, brown coat, a slight stoop", "any")
    add("harrison_hold_h1", HA, dict(yaw=0.20, pitch=-0.45, expr="grinning", head_roll=-4, lean=-3, t=0.3, arm_r=dict(hand=(0.55, -0.78), bend=-0.4, stretch=1.3, layer="top"),
                                      prop_r=dict(type="h1_clock19", scale=1.35), arm_l=dict(hand=(-0.62, -0.78), bend=-0.4, stretch=1.3, layer="top"), legs="wide"),
        "holding up the big sea clock (H1) overhead with both arms, proud grin (prop h1_clock19; anchors h1_grip_l_r / h1_grip_r_r)", "1")
    add("harrison_file_bench", HA, dict(yaw=0.50, pitch=0.35, expr="determined", gaze=(0.7, 0.9), lean=10, arm_r=dict(hand=(0.82, 1.06), bend=0.2, stretch=1.2, layer="front"),
                                         prop_r=dict(type="file19", angle=12), arm_l=dict(hand=(0.62, 1.12), bend=0.3, layer="front"), legs=dict(preset="stand", stride=0.15)),
        "filing a brass part at the bench (screen-right): file in the right hand, head bent over the work (the part itself is set art)", "2")
    add("harrison_chisel", HA, dict(yaw=0.50, pitch=0.30, expr="determined", gaze=(0.7, 0.9), lean=8, arm_r=dict(hand=(0.78, 1.00), bend=0.2, stretch=1.2, layer="front"),
                                     prop_r=dict(type="chisel19", angle=40), arm_l=dict(hand=(0.60, 1.10), bend=0.3, layer="front"), legs="stand"),
        "alt at the bench: working with a chisel", "2")
    add("harrison_show_h4", HA, dict(yaw=0.30, pitch=-0.05, expr="happy", mouth="smile", head_roll=-4, gaze=(0.0, 0.5), arm_r=dict(hand=(0.64, 0.60), bend=-0.2, shape="open", stretch=1.15, layer="top"),
                                      prop_r="h4_watch", arm_l="hip", legs="stand"),
        "holding up the H4 watch on his open palm (silver, white dial with tick marks, two hands, no numerals)", "3")
    add("harrison_tired_rub", HA, dict(yaw=0.20, pitch=0.30, expr="worried", blink=2, head_roll=6, fx=["sweat"], arm_r=dict(hand=(0.16, 0.04), bend=-0.5, shape="open", layer="top"),
                                        arm_l=dict(hand=(-0.40, 0.96), bend=0.5), squash=(1.01, 0.98), legs="stand"),
        "tired, rubbing his eyes with the back of one hand (eyes shut: blink 2)", "4")
    add("harrison_hopeful_door", HA, dict(yaw=0.70, pitch=-0.10, expr="worried", mouth="smile", gaze=(0.9, -0.1), head_roll=-5, lean=5,
                                           arm_r=dict(hand=(0.28, 0.80), bend=0.8, shape="open", layer="top"), arm_l=dict(hand=(0.18, 0.86), bend=0.8, shape="open", layer="top"),
                                           legs=dict(preset="stand", stride=0.2)),
        "hopeful at the door (door at screen-right; mirror=True for left): hands clasped at the chest, brows up, small smile", "5")
    add("harrison_old_handover", HO, dict(old=1, yaw=0.40, pitch=0.10, expr="happy", mouth="smile", head_roll=-3, gaze=(0.7, 0.5),
                                           arm_r=dict(hand=(0.82, 0.74), bend=-0.1, shape="open", stretch=1.2, layer="front"), prop_r="h4_watch", arm_l=dict(hand=(-0.30, 1.0), bend=0.6), legs="stand"),
        "old Harrison, stooped, handing over a watch to screen-right (the watch sits on his open palm; mirror=True for left)", "6")
    # ------------------------------------------------------------------ William
    add("william_idle", WI, dict(idle), "standing", "any")
    add("william_quadrant_sun", WI, dict(yaw=0.40, pitch=-0.75, expr="determined", gaze=(0.5, -0.9), lean=-3, glint=1.0, arm_r=dict(hand=(0.46, 0.10), bend=-0.7, stretch=1.1, layer="top"),
                                          prop_r=dict(type="quadrant19", angle=-62, scale=0.95), arm_l=dict(hand=(-0.46, 0.96), bend=0.5), legs="wide"),
        "aiming the brass quadrant at the sun (up and screen-right), squinting", "7")
    add("william_show_h4", WI, dict(yaw=0.30, expr="happy", mouth="smile", head_roll=-3, arm_r=dict(hand=(0.64, 0.62), bend=-0.2, shape="open", stretch=1.15, layer="top"),
                                     prop_r="h4_watch", arm_l="hip", legs="stand"), "showing the H4 on his open palm", "8")
    add("william_cheer_hat", WI, dict(hat_off=1, yaw=0.20, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=-6, t=0.3, arm_r=dict(hand=(0.74, -0.78), bend=-0.5, stretch=1.3, layer="top"),
                                       prop_r="tricorn_held", arm_l=dict(hand=(-0.60, 0.30), bend=-0.3, shape="open", layer="top"), legs="wide", squash=(0.98, 1.03)),
        "cheering with the tricorne raised in his hand (hat_off=1: own tied hair shows)", "9")
    # ------------------------------------------------------------------ the mocker astronomer
    add("astro_idle", AS, dict(yaw=0.25, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"), "standing smug, specs up on the forehead", "any")
    add("astro_belly_laugh", AS, dict(yaw=0.20, pitch=-0.80, expr="laughing", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.03, 0.97),
                                       arm_r=dict(hand=(0.50, 1.02), bend=0.9, shape="open"), arm_l=dict(hand=(-0.54, 1.00), bend=0.9, shape="open"), legs="wide"),
        "BELLY LAUGH (laugh cycle: laugh_cycle(phase, pose)): head back, hands on the belly, tears; bounce squash (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz", "1")
    add("astro_mock_point", AS, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8, squash=(1.02, 0.98),
                                      arm_r=dict(hand=(1.14, 0.06), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"),
        "mocking, pointing at Harrison (screen-right); mouth talk_b held, or drive it with talk_mouth(g)", "2")
    add("astro_mock_bow", AS, dict(yaw=0.45, pitch=0.30, expr="smug", mouth="smile", head_roll=10, lean=16, arm_r=dict(hand=(0.78, 0.96), bend=0.2, shape="open", stretch=1.1, layer="front"),
                                    prop_r=dict(type="pocketwatch19", scale=1.0), arm_l=dict(hand=(-0.98, 0.78), bend=-0.2, shape="open", stretch=1.2, layer="back"),
                                    legs=dict(preset="step", stride=0.4, crouch=0.04)),
        "a mock-royal bow, one arm swept back, holding a gold pocket watch as if timing a shot: the mockery", "3")
    add("astro_shrug_fluke", AS, dict(yaw=0.25, pitch=-0.20, expr="smug", mouth="smirk", head_roll=-6, squash=(1.0, 1.0),
                                       arm_r=dict(hand=(0.94, 0.62), bend=0.4, shape="open", stretch=1.2), arm_l=dict(hand=(-0.94, 0.62), bend=0.4, shape="open", stretch=1.2), legs="wide"),
        "shrug with both palms up: 'a fluke!'", "4")
    add("astro_jaw_drop", AS, dict(yaw=0.20, pitch=0.10, expr="shocked", mouth=("open", 0.26, 0.20), fx=["sweat"], arm_r="down", arm_l="down", squash=(0.98, 1.03), legs="stand"),
        "JAW DROP: held wide-open mouth, ring eyes, arms hanging", "9")
    add("astro_sour_arms", AS, dict(yaw=0.30, expr="unimpressed", mouth="frown", head_roll=4, pitch=-0.2, arm_r=dict(hand=(-0.46, 0.88), bend=0.9, layer="top"),
                                     arm_l=dict(hand=(0.46, 0.94), bend=0.9, layer="top"), legs="wide"), "SOUR: arms folded across the belly, mouth down", "9")
    # ------------------------------------------------------------------ the other astronomers
    for key, c in (("b", AB), ("c", AC)):
        add("astro_%s_idle" % key, c, dict(idle, yaw=0.30, expr="smug"), "standing", "any")
        add("astro_%s_laugh" % key, c, dict(yaw=0.25, pitch=-0.6, expr="laughing", fx=["tears"], head_roll=-8, lean=-6, t=0.3, squash=(1.03, 0.98),
                                             arm_r=dict(hand=(0.40, 0.92), bend=0.8, shape="open"), arm_l=dict(hand=(-0.46, 0.90), bend=0.8, shape="open"), legs="wide"),
            "laughing, hands on the belly (laugh cycle)", "1")
        add("astro_%s_peer" % key, c, dict(yaw=0.45, pitch=0.35, expr="unimpressed", blink=1, gaze=(0.7, 0.8), head_roll=6, lean=10,
                                            arm_r=dict(hand=(0.30, 0.52), bend=0.8, shape="open", layer="top"), arm_l=dict(hand=(-0.40, 0.94), bend=0.7), legs="stand"),
            "peering down at the watch (screen-right), eyes narrowed, one hand at the chin", "9")
    # ------------------------------------------------------------------ the king
    add("king_idle", KI, dict(idle, expr="neutral"), "standing, the Garter star and blue sash", "any")
    add("king_watch_squint", KI, dict(yaw=0.30, pitch=0.15, expr="unimpressed", blink=1, head_roll=4, gaze=(0.0, 0.5),
                                       arm_r=dict(hand=(0.62, 0.58), bend=-0.2, shape="open", stretch=1.15, layer="top"), prop_r="pocketwatch19",
                                       arm_l=dict(hand=(-0.62, 0.58), bend=-0.2, shape="open", stretch=1.15, layer="top"), prop_l="h4_watch", legs="stand"),
        "holding his gold pocket watch beside the silver H4 (one in each open hand, both at chest height) and squinting at them", "10")
    add("king_write_seated", KI, dict(stool=1, yaw=0.45, pitch=0.40, expr="determined", gaze=(0.7, 0.9), lean=10, head_roll=-4,
                                       arm_r=dict(hand=(0.80, 1.12), bend=0.2, stretch=1.1, layer="front"), prop_r=dict(type="quill19", angle=70),
                                       arm_l=dict(hand=(0.54, 1.20), bend=0.3, layer="front"), legs=dict(crouch=0.42, spread=0.05)),
        "seated at a table (the table is set art), writing with a quill (screen-right)", "11")
    add("king_point_decree", KI, dict(yaw=0.40, pitch=-0.35, expr="determined", head_roll=-3, lean=-3, arm_r=dict(hand=(1.06, 0.20), shape="point", bend=-0.5, stretch=1.3),
                                       arm_l=dict(hand=(-0.44, 0.88), bend=0.8, layer="front"), prop_l=dict(type="scroll19", angle=-70, scale=0.9), legs="wide"),
        "pointing a decree (screen-right), the rolled and sealed scroll in the other hand, chin up", "11")
    # ------------------------------------------------------------------ the captain and the sailors
    add("captain_idle", CA, dict(idle, expr="neutral", arm_r="behind", arm_l="behind"), "standing, hands behind his back", "any")
    add("captain_peer_chart", CA, dict(yaw=0.40, pitch=0.35, expr="determined", gaze=(0.8, 0.9), lean=8, arm_r=dict(hand=(0.60, 0.96), bend=0.3, layer="front"),
                                        prop_r=dict(type="chart19", scale=1.0), arm_l=dict(hand=(1.30, 1.00), bend=0.0, stretch=1.3, layer="front"), legs="wide"),
        "peering at a sea chart held out in both hands (screen-right)", "12")
    add("captain_cheer", CA, dict(yaw=0.20, pitch=-0.30, expr="happy", mouth="grin", head_roll=-5, t=0.3, arm_r=dict(hand=(0.76, -0.70), bend=-0.5, shape="open", stretch=1.3, layer="top"),
                                   arm_l=dict(hand=(-0.50, 0.90), bend=0.6), legs="wide"), "pleased, one arm up", "13")
    for key, s_, lean_ in (("a", SA, 12), ("b", SB, 16), ("c", SC, 10)):
        add("sailor_%s_idle" % key, s_, dict(idle, yaw=0.30), "standing", "any")
        add("sailor_%s_haul" % key, s_, dict(yaw=0.60, pitch=0.10, expr="shouting", lean=-lean_, arm_r=dict(hand=(0.60, 0.78), bend=0.2, layer="front"), prop_r=dict(type="rope19", angle=-12, scale=1.0),
                                              legs=dict(preset="step", stride=0.55, crouch=0.08)),
            "hauling on a rope (screen-right), leaning back with the whole body (the second hand goes on the rope: _grip2)", "14")
        add("sailor_%s_cheer" % key, s_, dict(yaw=0.20, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=-5, t=0.3, arm_r=dict(hand=(0.74, -0.74), bend=-0.5, shape="open", stretch=1.3, layer="top"),
                                               arm_l=dict(hand=(-0.74, -0.70), bend=-0.5, shape="open", stretch=1.3, layer="top"), legs="wide", squash=(0.98, 1.03)),
            "cheering, both arms up", "15")
        add("sailor_%s_bail" % key, s_, dict(yaw=0.50, pitch=0.15, expr="worried", mouth="o", fx=["sweat"], lean=lean_ - 6, splash=1.0, arm_r=dict(hand=(0.70, 0.70), bend=0.2, layer="front"),
                                              prop_r=dict(type="bucket19", scale=1.0), arm_l=dict(hand=(-0.46, 1.00), bend=0.5), legs=dict(preset="step", stride=0.3, crouch=0.10)),
            "bailing water out of the ship, comic: bucket flung to screen-right, a jet of water, worried face", "16")
    for key in ("a", "b", "c"):
        _grip2(S, "sailor_%s_haul" % key)
    return S, M


STORY19_SHOTS = {}
STORY19, STORY19_META = {}, {}


def register():
    if getattr(P, "_cast19_registered", False):
        CE.register_stage()
        if not STORY19:
            s, m = _story()
            STORY19.update(s)
            STORY19_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "figure", "_ink_limb"):
        _O19[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P.figure = figure
    P._ink_limb = _ink_limb
    CE.COSTUMES.update(COSTUMES19)
    CE.HATS.update(HATS19)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS19 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP19)
    for n, c in _cast_table().items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS19_TABLE)
    P._cast19_registered = True
    s, m = _story()
    STORY19.update(s)
    STORY19_META.update(m)
    P.STORY.update(STORY19)
    CE.register_stage()


CANVAS19_TABLE = {
    "astro19": (-1.5000, -4.0000, 1.5000, 0.1875),
    "astro19_b": (-1.3750, -4.1250, 1.3750, 0.1875),
    "astro19_c": (-1.3125, -3.3750, 1.3125, 0.1875),
    "captain19": (-1.6875, -3.6875, 1.6875, 0.1875),
    "harrison19": (-2.0000, -4.2500, 2.0000, 0.1875),
    "king19": (-1.3750, -3.8125, 1.3750, 0.1875),
    "sailor19_a": (-2.1875, -3.5625, 2.1875, 0.1875),
    "sailor19_b": (-2.1250, -3.5625, 2.1250, 0.1875),
    "sailor19_c": (-2.2500, -3.6250, 2.2500, 0.1875),
    "william19": (-1.1875, -4.0000, 1.1875, 0.1875),
}
CANVAS19 = CANVAS19_TABLE      # feet-relative sprite cards (x0, y0, x1, y1) in D, y down; verified by test_cast19.py canvas
register()
