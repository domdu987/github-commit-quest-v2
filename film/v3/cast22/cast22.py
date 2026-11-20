#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast22.py -- the cast of film 22 ("ไอ้ช่างวงจร", Harry Beck's Underground diagram, London 1931-33) for the v2 puppet, as an
extension module on top of cast10.

    import sys; sys.path.insert(0, ".../v3/cast22"); import cast22     # registers on import (idempotent); imports cast10 .. cast_ext
    import puppet                                                      # the same module object, now with the new members
    cast, pose = cast22.STORY22["beck_rule_line"]
    f = puppet.figure(cast, pose, "f")
    c = cast22.crowd_member(3, "pass_walk")                            # (cast, pose) of crowd person 3, never cloned

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables (CAST, costumes, hats, props,
pose keys, STORY, canvases) and wraps puppet helpers on top of cast10's wrappers (_norm, _face, _prop, figure); each wrapper
falls through for everything it does not handle, so every earlier member draws byte-identically (test_cast22.py checks).
New members: beck, official, clerk_a, clerk_b, clerk_c, pass_man, pass_woman, pass_child, old_gent, porter.
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
import cast8 as C8      # noqa: E402
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW22 = ("beck", "official", "clerk_a", "clerk_b", "clerk_c", "pass_man", "pass_woman", "pass_child", "old_gent", "porter")
TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly_d = P._poly_d
_X, _ln, _circ, _poly, _bowl = CE._X, CE._ln, CE._circ, CE._poly, CE._bowl
_f = C6._f
_lin = C9._lin
_O22 = {}
_POSE22 = {"napkin": 0.0, "flush": 0.0, "puff": 0.0, "fork_map": 0.0, "board": 0.0, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
RED, BLUE, GREEN, YELLOW, BROWN = "#e2231a", "#0f5fd0", "#10a040", "#f5c400", "#8a4a22"
WOOD = dict(light="#f0cf8e", base="#d0a05a", dark="#8e6430")
DARKWOOD = dict(light="#a8683a", base="#7a4624", dark="#4a2814")
PAPER = dict(light="#ffffff", base="#f7f3e6", dark="#d6cfb8")
LEATHER = dict(light="#c47a3e", base="#8e4e22", dark="#5a2e12")
STEEL = dict(light="#e8edf2", base="#aab4c0", dark="#6a7480")
GOLDC = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
AMBER = dict(light="#ffd98a", base="#f2a93a", dark="#b8711a")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _roundel(k, cx, cy, r, sw=0.012):
    """the Underground roundel: a red ring with a blue bar across it."""
    o = ['<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (cx, cy, r, k.c(RED), k.ink, sw)]
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (cx, cy, r * 0.62, k.c("#fbf8f0"), k.ink, sw * 0.7))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (cx - r * 1.22, cy - r * 0.22, r * 2.44, r * 0.44, k.c(BLUE), k.ink, sw * 0.8))
    return "".join(o)


def _diagram(k, x0, y0, w, h, lw=0.030, rings=True):
    """a little Beck diagram in the box: straight red / blue / green / yellow lines at 0, 90 and 45 degrees, station ticks, white
    interchange rings.  Everything is drawn with an ink under-stroke so it survives a small size."""
    def X(u, v):
        return (x0 + u * w, y0 + v * h)
    lines = ((RED, [(0.06, 0.30), (0.94, 0.30)]),
             (BLUE, [(0.30, 0.06), (0.30, 0.50), (0.62, 0.82), (0.94, 0.82)]),
             (GREEN, [(0.06, 0.74), (0.46, 0.74), (0.78, 0.42), (0.78, 0.10)]),
             (YELLOW, [(0.52, 0.06), (0.52, 0.30), (0.52, 0.62), (0.94, 0.62)]))
    o = []
    for col, pts in lines:
        d = "M" + " L".join("%.4f,%.4f" % X(*p) for p in pts)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>' % (d, k.ink, lw + 0.016))
    for col, pts in lines:
        d = "M" + " L".join("%.4f,%.4f" % X(*p) for p in pts)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>' % (d, k.c(col), lw))
    if rings:
        for (u, v) in ((0.30, 0.30), (0.52, 0.30), (0.78, 0.30), (0.52, 0.62), (0.46, 0.74)):
            c = X(u, v)
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (c[0], c[1], lw * 0.95, k.c("#ffffff"), k.ink, lw * 0.45))
    return "".join(o)


# ============================================================================= props (own local frames, hand at (0, 0))
def _ruler_body(k):
    g = _lin(k, "rl", WOOD["light"], WOOD["base"], WOOD["dark"], 0, -0.05, 0, 0.05)
    o = ['<rect x="-0.20" y="-0.052" width="0.92" height="0.104" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018"/>' % (g, k.ink)]
    for i in range(24):
        x = -0.17 + i * 0.0375
        ln = 0.040 if i % 5 == 0 else 0.022
        o.append('<path d="M%.4f,-0.040 L%.4f,%.4f" stroke="%s" stroke-width="0.007"/>' % (x, x, -0.040 + ln, k.c("#3a2a1a")))
    o.append('<path d="M-0.18,0.040 L0.70,0.040" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(WOOD["light"]))
    return "".join(o)


def _pen_body(k):
    o = ['<path d="M-0.10,-0.026 L0.20,-0.026 Q0.23,-0.026 0.23,0 Q0.23,0.026 0.20,0.026 L-0.10,0.026 Q-0.12,0.026 -0.12,0 Q-0.12,-0.026 -0.10,-0.026 Z" '
         'fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#1c2f6a"), k.ink)]
    o.append('<path d="M-0.08,-0.012 L0.19,-0.012" stroke="#ffffff" stroke-width="0.007" stroke-linecap="round" opacity="0.6"/>')
    o.append('<rect x="0.06" y="-0.028" width="0.030" height="0.056" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(GOLDC["base"]), k.ink))
    o.append('<path d="M-0.06,-0.024 L-0.06,-0.074 L-0.045,-0.074 L-0.045,-0.026" fill="%s" stroke="%s" stroke-width="0.007"/>' % (k.c(GOLDC["base"]), k.ink))
    o.append('<path d="M0.23,-0.020 L0.36,0 L0.23,0.020 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(GOLDC["light"]), k.ink))
    o.append('<path d="M0.27,0 L0.35,0" stroke="%s" stroke-width="0.006"/>' % k.ink)
    return "".join(o)


def _setsq_body(k):
    pts = [(-0.08, 0.08), (0.58, 0.08), (-0.08, -0.58)]
    inn = [(0.06, 0.00), (0.34, 0.00), (0.06, -0.28)]
    d = _poly_d(pts) + " " + _poly_d(inn[::-1])
    o = ['<path d="%s" fill="%s" fill-rule="evenodd" stroke="%s" stroke-width="0.020" stroke-linejoin="round" opacity="0.96"/>' % (d, k.c(AMBER["base"]), k.ink)]
    o.append('<path d="M-0.02,0.06 L0.52,0.06 M-0.06,0.02 L-0.06,-0.52" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % k.c(AMBER["light"]))
    o.append('<path d="M0.12,-0.46 L0.46,-0.12" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % k.c(AMBER["light"]))
    for i in range(1, 6):
        o.append('<path d="M%.4f,0.08 L%.4f,0.052" stroke="%s" stroke-width="0.007"/>' % (0.06 + i * 0.09, 0.06 + i * 0.09, k.ink))
    o.append('<text x="0.045" y="-0.31" font-family="DejaVu Sans, Arial, sans-serif" font-size="0.052" font-weight="700" fill="%s" transform="rotate(-45 0.045 -0.31)" opacity="0.8">45</text>' % k.ink)
    return "".join(o)


def _tsq_body(k):
    gb = _lin(k, "ts", WOOD["light"], WOOD["base"], WOOD["dark"], 0, -0.04, 0, 0.04)
    gh = _lin(k, "th", DARKWOOD["light"], DARKWOOD["base"], DARKWOOD["dark"], -0.04, 0, 0.04, 0)
    o = ['<rect x="-0.10" y="-0.036" width="1.22" height="0.072" rx="0.010" fill="%s" stroke="%s" stroke-width="0.018"/>' % (gb, k.ink)]
    o.append('<path d="M0.02,0.030 L1.08,0.030" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(WOOD["dark"]))
    o.append('<rect x="-0.16" y="-0.20" width="0.10" height="0.40" rx="0.012" fill="%s" stroke="%s" stroke-width="0.020"/>' % (gh, k.ink))
    for x in (0.18, 0.18 + 0.22, 0.18 + 0.44, 0.18 + 0.66, 0.18 + 0.88):
        o.append('<path d="M%.4f,-0.030 L%.4f,-0.008" stroke="%s" stroke-width="0.007"/>' % (x, x, k.ink))
    return "".join(o)


def _roll_body(k):
    """a rolled drawing 0.84 long (-0.42 .. 0.42): white paper, a red tie band, and at the +x end the open spiral with
    the four line colours peeking out."""
    g = _lin(k, "rr", PAPER["light"], PAPER["base"], PAPER["dark"], 0, -0.085, 0, 0.085)
    o = ['<path d="M-0.42,-0.082 L0.40,-0.082 L0.40,0.082 L-0.42,0.082 Q-0.45,0 -0.42,-0.082 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M-0.38,-0.050 L0.38,-0.056" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(PAPER["dark"]))
    o.append('<rect x="-0.20" y="-0.086" width="0.050" height="0.172" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(RED), k.ink))
    # coloured lines peeking out of the end
    for col, y, ln in ((RED, -0.050, 0.075), (BLUE, -0.016, 0.050), (GREEN, 0.018, 0.085), (YELLOW, 0.052, 0.060)):
        o.append('<path d="M0.36,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (y, 0.40 + ln, y, k.ink))
    for col, y, ln in ((RED, -0.050, 0.075), (BLUE, -0.016, 0.050), (GREEN, 0.018, 0.085), (YELLOW, 0.052, 0.060)):
        o.append('<path d="M0.36,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (y, 0.40 + ln, y, k.c(col)))
    o.append('<ellipse cx="0.40" cy="0" rx="0.036" ry="0.082" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(PAPER["base"]), k.ink))
    o.append('<path d="M0.40,-0.04 Q0.43,0 0.40,0.04" fill="none" stroke="%s" stroke-width="0.008"/>' % k.ink)
    return "".join(o)


SHEET_W, SHEET_H = 0.96, 0.68


def _sheet_body(k):
    """the big diagram sheet: flat card hand-held by its left edge (x 0 .. 0.96, y +-0.34)."""
    o = ['<rect x="0.0" y="%.4f" width="%.4f" height="%.4f" rx="0.012" fill="%s" stroke="%s" stroke-width="0.022"/>' % (-SHEET_H / 2, SHEET_W, SHEET_H, k.c(PAPER["base"]), k.ink)]
    o.append('<rect x="0.04" y="%.4f" width="%.4f" height="0.070" fill="%s"/>' % (-SHEET_H / 2 + 0.03, SHEET_W - 0.08, k.c("#1c2f6a")))
    o.append('<rect x="0.06" y="%.4f" width="0.10" height="0.038" fill="%s"/><rect x="0.17" y="%.4f" width="0.10" height="0.038" fill="%s"/>'
             % (-SHEET_H / 2 + 0.046, k.c(RED), -SHEET_H / 2 + 0.046, k.c(YELLOW)))
    o.append(_diagram(k, 0.08, -SHEET_H / 2 + 0.13, SHEET_W - 0.16, SHEET_H - 0.20, lw=0.034))
    o.append('<path d="M0.0,%.4f L0.0,%.4f" stroke="#ffffff" stroke-width="0.012" opacity="0.5"/>' % (-SHEET_H / 2 + 0.02, SHEET_H / 2 - 0.02))
    return "".join(o)


def _stamp_body(k):
    gw = _lin(k, "sw", DARKWOOD["light"], DARKWOOD["base"], DARKWOOD["dark"], 0, -0.08, 0, 0.08)
    o = ['<path d="M-0.10,-0.060 Q-0.14,0 -0.10,0.060 Q-0.02,0.050 0.0,0.024 L0.10,0.024 L0.10,-0.024 L0.0,-0.024 Q-0.02,-0.050 -0.10,-0.060 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gw, k.ink)]
    o.append('<rect x="0.10" y="-0.095" width="0.130" height="0.190" rx="0.014" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c(DARKWOOD["base"]), k.ink))
    o.append('<rect x="0.230" y="-0.085" width="0.060" height="0.170" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#d8231c"), k.ink))
    o.append('<path d="M0.250,-0.060 L0.250,0.060" stroke="#ffffff" stroke-width="0.010" opacity="0.5"/>')
    o.append('<path d="M-0.08,-0.030 Q-0.10,0 -0.08,0.030" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(DARKWOOD["light"]))
    return "".join(o)


def _pmap_closed(k):
    """small folded pocket map seen from the cover: cream card, the red-blue roundel and UNDERGROUND (x 0 .. 0.34, y +-0.12)."""
    o = ['<rect x="0.0" y="-0.125" width="0.34" height="0.25" rx="0.010" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#f6efd8"), k.ink)]
    o.append('<rect x="0.0" y="-0.125" width="0.34" height="0.045" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#1c2f6a"), k.ink))
    o.append(_roundel(k, 0.17, 0.005, 0.075, 0.010))
    o.append('<text x="0.17" y="-0.092" font-family="DejaVu Sans, Arial, sans-serif" font-size="0.034" font-weight="700" fill="#ffffff" text-anchor="middle">UNDERGROUND</text>')
    o.append('<path d="M0.0,0.095 L0.34,0.095" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % k.c("#c9bfa0"))
    o.append('<path d="M0.17,-0.125 L0.17,0.125" stroke="%s" stroke-width="0.007" opacity="0.5"/>' % k.c("#c9bfa0"))
    return "".join(o)


def _pmap_open(k):
    """the same map opened: a zig-zag folded sheet 0.62 x 0.44 with the bright little diagram."""
    w, h = 0.64, 0.44
    o = ['<rect x="0.0" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (-h / 2, w, h, k.c("#fbf7e8"), k.ink)]
    for i in (1, 2, 3):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (w * i / 4, -h / 2, w * i / 4, h / 2, k.c("#b9ae90")))
    o.append('<rect x="0.0" y="%.4f" width="%.4f" height="0.055" fill="%s" stroke="%s" stroke-width="0.010"/>' % (-h / 2, w, k.c("#1c2f6a"), k.ink))
    o.append(_roundel(k, 0.06, -h / 2 + 0.027, 0.032, 0.006))
    o.append(_diagram(k, 0.04, -h / 2 + 0.07, w - 0.08, h - 0.10, lw=0.034))
    return "".join(o)


def _fork_body(k, with_map=0.0):
    sc = k.c(STEEL["base"])
    o = ['<path d="M-0.16,-0.018 L0.18,-0.012 L0.22,-0.060 L0.22,0.060 L0.18,0.012 L-0.16,0.018 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#6a4428"), k.ink)]
    o.append('<path d="M0.18,0 L0.34,0" stroke="%s" stroke-width="0.034" stroke-linecap="round"/><path d="M0.18,0 L0.34,0" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (k.ink, sc))
    for dy in (-0.052, 0.0, 0.052):
        o.append('<path d="M0.24,%.4f L0.50,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (dy, dy, k.ink))
    for dy in (-0.052, 0.0, 0.052):
        o.append('<path d="M0.24,%.4f L0.50,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (dy, dy, sc))
    if with_map > 0.5:
        # a little folded map speared on the fork tines
        o.append('<g transform="translate(0.34 -0.01) rotate(-14)"><rect x="0.0" y="-0.13" width="0.30" height="0.26" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#fbf7e8"), k.ink))
        o.append(_diagram(k, 0.02, -0.11, 0.26, 0.22, lw=0.030, rings=False))
        o.append('</g>')
        for dy in (-0.052, 0.0, 0.052):
            o.append('<path d="M0.42,%.4f L0.50,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (dy, dy, sc))
    return "".join(o)


def _knife_body(k):
    o = ['<path d="M-0.16,-0.020 L0.10,-0.016 L0.10,0.016 L-0.16,0.020 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#6a4428"), k.ink)]
    o.append('<path d="M0.10,-0.026 L0.46,-0.026 Q0.52,-0.020 0.50,0.020 L0.10,0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(STEEL["light"]), k.ink))
    o.append('<path d="M0.14,-0.010 L0.44,-0.010" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>')
    return "".join(o)


def _letter_body(k):
    """a letter marked NOTICE (x 0 .. 0.48, y +-0.17)."""
    o = ['<rect x="0.0" y="-0.17" width="0.48" height="0.34" rx="0.008" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#fbf7e8"), k.ink)]
    o.append('<rect x="0.0" y="-0.17" width="0.48" height="0.085" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#d8231c"), k.ink))
    o.append('<text x="0.24" y="-0.108" font-family="DejaVu Sans, Arial, sans-serif" font-size="0.062" font-weight="700" fill="#ffffff" text-anchor="middle">NOTICE</text>')
    for i in range(4):
        o.append('<path d="M0.05,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (-0.04 + i * 0.05, 0.43 - (i == 3) * 0.14, -0.04 + i * 0.05, k.c("#5a5a66")))
    o.append('<path d="M0.34,0.10 L0.44,0.10" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(RED))
    return "".join(o)


def _briefcase_body(k):
    """hangs from the hand by its handle (hand at 0, 0): body 0.46 x 0.30 below the handle, always upright."""
    g = _lin(k, "bc", LEATHER["light"], LEATHER["base"], LEATHER["dark"], -0.23, 0, 0.23, 0)
    o = ['<path d="M-0.07,0.14 Q-0.07,-0.02 0,-0.02 Q0.07,-0.02 0.07,0.14" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.07,0.14 Q-0.07,-0.02 0,-0.02 Q0.07,-0.02 0.07,0.14" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(LEATHER["dark"]))
    o.append('<rect x="-0.23" y="0.13" width="0.46" height="0.30" rx="0.030" fill="%s" stroke="%s" stroke-width="0.022"/>' % (g, k.ink))
    o.append('<path d="M-0.22,0.22 L0.22,0.22" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c(LEATHER["dark"]))
    o.append('<rect x="-0.045" y="0.20" width="0.090" height="0.055" rx="0.008" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(GOLDC["base"]), k.ink))
    for sx in (-0.17, 0.17):
        o.append('<path d="M%.4f,0.15 L%.4f,0.22" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (sx, sx, k.c(LEATHER["dark"])))
    o.append('<path d="M-0.20,0.16 Q-0.10,0.145 0.05,0.15" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % k.c(LEATHER["light"]))
    return "".join(o)


def _handbag_body(k):
    """a red handbag hanging from the hand (hand at 0, 0): strap loop, body 0.34 x 0.24, gold clasp, always upright."""
    g = _lin(k, "hb", "#f0584a", "#c8302a", "#8a1c18", -0.17, 0, 0.17, 0)
    o = ['<path d="M-0.10,0.14 Q-0.10,-0.04 0,-0.04 Q0.10,-0.04 0.10,0.14" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.10,0.14 Q-0.10,-0.04 0,-0.04 Q0.10,-0.04 0.10,0.14" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c("#8a1c18"))
    o.append('<path d="M-0.17,0.15 L0.17,0.15 L0.20,0.38 Q0,0.41 -0.20,0.38 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.17,0.20 Q0,0.23 0.17,0.20" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c("#8a1c18"))
    o.append('<circle cx="0" cy="0.215" r="0.028" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(GOLDC["base"]), k.ink))
    o.append('<path d="M-0.13,0.22 L-0.14,0.33" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.45"/>')
    return "".join(o)


def _umbrella_body(k):
    """a furled umbrella along +x: crook handle at -0.28, held at 0, shaft, black furled silk (0.30 .. 1.0) with a strap, ferrule."""
    o = ['<path d="M-0.20,0 L0.34,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M-0.20,0 L0.34,0" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (k.ink, k.c(DARKWOOD["base"]))]
    o.append('<path d="M-0.20,0 Q-0.30,0 -0.30,0.09 Q-0.30,0.17 -0.22,0.16" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.20,0 Q-0.30,0 -0.30,0.09 Q-0.30,0.17 -0.22,0.16" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.c(DARKWOOD["base"]))
    g = _lin(k, "um", "#4a4a5a", "#1c1c28", "#0a0a12", 0, -0.07, 0, 0.07)
    o.append('<path d="M0.30,-0.020 Q0.50,-0.085 0.74,-0.060 Q0.95,-0.030 1.02,-0.006 L1.02,0.006 Q0.95,0.030 0.74,0.060 Q0.50,0.085 0.30,0.020 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M0.42,-0.050 Q0.66,-0.048 0.90,-0.020 M0.42,0.052 Q0.66,0.048 0.90,0.022" fill="none" stroke="#7a7a90" stroke-width="0.008" opacity="0.8"/>')
    o.append('<rect x="0.60" y="-0.068" width="0.036" height="0.136" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#6a4a2a"), k.ink))
    o.append('<path d="M1.00,0 L1.12,0" stroke="%s" stroke-width="0.030" stroke-linecap="round"/><path d="M1.00,0 L1.12,0" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (k.ink, k.c(GOLDC["base"])))
    return "".join(o)


def _cup_body(k, t=0.0):
    """a tea cup held by its handle: cup body left of the hand (x -0.22 .. 0.0), handle at the hand (+x side), always upright."""
    g = _lin(k, "tc", "#ffffff", "#f4f0ea", "#cfc8bc", -0.22, 0, 0.0, 0)
    o = ['<path d="M-0.24,-0.12 L0.0,-0.12 Q0.0,-0.02 -0.06,0.02 L-0.18,0.02 Q-0.24,-0.02 -0.24,-0.12 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<ellipse cx="-0.12" cy="-0.12" rx="0.12" ry="0.022" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#6a3a1a"), k.ink))
    o.append('<path d="M-0.23,-0.07 L0.0,-0.07" stroke="%s" stroke-width="0.016" opacity="0.9"/>' % k.c(BLUE))
    o.append('<path d="M0.0,-0.10 Q0.09,-0.10 0.09,-0.04 Q0.09,0.0 0.0,-0.02" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.0,-0.10 Q0.09,-0.10 0.09,-0.04 Q0.09,0.0 0.0,-0.02" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c("#f4f0ea"))
    o.append('<ellipse cx="-0.12" cy="0.035" rx="0.15" ry="0.020" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#f4f0ea"), k.ink))
    for j in range(2):
        f = (t * 1.0 + 0.5 * j) % 1.0
        o.append('<path d="M%.4f,%.4f q0.03,-0.05 0,-0.10 q-0.03,-0.05 0.0,-0.10" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="%.2f"/>'
                 % (-0.15 + 0.06 * j, -0.15 - 0.10 * f, 0.8 - 0.6 * f))
    return "".join(o)


def _magnifier_body(k):
    """a magnifying glass along +x: wooden handle from -0.05 to 0.28, brass ring (centre 0.46, r 0.17), glass with a glint."""
    o = ['<path d="M-0.05,0 L0.30,0" stroke="%s" stroke-width="0.062" stroke-linecap="round"/><path d="M-0.05,0 L0.30,0" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (k.ink, k.c(DARKWOOD["base"]))]
    o.append('<circle cx="0.47" cy="0" r="0.175" fill="#cfe8f6" fill-opacity="0.45" stroke="%s" stroke-width="0.046"/>' % k.ink)
    o.append('<circle cx="0.47" cy="0" r="0.175" fill="none" stroke="%s" stroke-width="0.024"/>' % k.c(GOLDC["base"]))
    o.append('<path d="M0.37,-0.07 Q0.40,-0.12 0.47,-0.13" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.9"/>')
    o.append('<circle cx="0.55" cy="0.06" r="0.014" fill="#ffffff" opacity="0.8"/>')
    return "".join(o)


def _handtruck_body(k, sc):
    """a porter's two-wheeled sack truck carrying a MAPS crate.  Hand at the top of the handle (0, 0); the frame leans forward
    (+x) to a wheel on the floor GR below; the crate rests on the toe plate in front.  Always upright."""
    gr = 1.30 * sc
    wr = 0.15
    o = []
    # frame rails
    for dx in (0.0, 0.07):
        o.append('<path d="M%.4f,0 L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/><path d="M%.4f,0 L%.4f,%.4f" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>'
                 % (dx, dx + 0.13, gr - wr, k.ink, dx, dx + 0.13, gr - wr, k.c(STEEL["base"])))
    o.append('<path d="M-0.06,0 L0.14,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M-0.06,0 L0.14,0" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (k.ink, k.c(DARKWOOD["base"])))
    cx0, cx1 = 0.20, 0.78
    cy1 = gr - wr - 0.02
    cy0 = cy1 - 0.50 * sc
    g = _lin(k, "cr", WOOD["light"], WOOD["base"], WOOD["dark"], cx0, 0, cx1, 0)
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.022"/>' % (cx0, cy0, cx1 - cx0, cy1 - cy0, g, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (cx0, cy0 + (cy1 - cy0) * 0.5, cx1, cy0 + (cy1 - cy0) * 0.5, cx0 + 0.29, cy0, cx0 + 0.29, cy1, k.c(WOOD["dark"])))
    for (a, b) in ((cx0, cy0), (cx1, cy0), (cx0, cy1), (cx1, cy1)):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s"/>' % (a + (0.03 if a == cx0 else -0.03), b + (0.03 if b == cy0 else -0.03), k.c(STEEL["dark"])))
    o.append('<text x="%.4f" y="%.4f" font-family="DejaVu Sans, Arial, sans-serif" font-size="0.085" font-weight="800" fill="%s" text-anchor="middle">MAPS</text>' % ((cx0 + cx1) / 2, cy0 + (cy1 - cy0) * 0.40, k.c(RED)))
    o.append(_roundel(k, (cx0 + cx1) / 2, cy0 + (cy1 - cy0) * 0.73, 0.055, 0.008))
    o.append('<path d="M0.13,%.4f L0.82,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M0.13,%.4f L0.82,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (cy1 + 0.01, cy1 + 0.01, k.ink, cy1 + 0.01, cy1 + 0.01, k.c(STEEL["base"])))
    o.append('<circle cx="0.20" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.026"/><circle cx="0.20" cy="%.4f" r="%.4f" fill="%s"/><circle cx="0.20" cy="%.4f" r="0.025" fill="%s"/>'
             % (gr - wr, wr, k.c("#2a262c"), k.ink, gr - wr, wr * 0.55, k.c(STEEL["base"]), gr - wr, k.ink))
    return "".join(o), gr


def _board_body(k):
    """the drafting board (pose key board=1): a tilted board with the big diagram in progress, x 0 .. 1.5, y +-0.55."""
    g = _lin(k, "bd", "#e7d3a2", "#d2b57a", "#a88850", 0, -0.55, 0, 0.55)
    o = ['<path d="M0.05,-0.55 L1.55,-0.40 L1.50,0.55 L0.0,0.50 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.12,-0.48 L1.47,-0.34 L1.43,0.48 L0.07,0.44 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#f8f3e2"), k.ink))
    o.append('<g transform="matrix(1 0.10 0 1 0 0)">%s</g>' % _diagram(k, 0.22, -0.40, 1.14, 0.76, lw=0.045))
    return "".join(o)


def _circuit_body(k):
    """a circuit-diagram sheet: blue-print card (x 0 .. 0.84, y +-0.30) with white wires, a zig-zag resistor, a capacitor, a
    battery, a lamp and yellow solder dots."""
    o = ['<rect x="0.0" y="-0.30" width="0.84" height="0.60" rx="0.012" fill="%s" stroke="%s" stroke-width="0.022"/>' % (k.c("#2a5ec8"), k.ink)]
    w = k.c("#ffffff")
    o.append('<path d="M0.08,-0.18 L0.76,-0.18 L0.76,0.18 L0.08,0.18 Z" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % w)
    o.append('<path d="M0.20,-0.18 l0.04,-0.07 l0.06,0.14 l0.06,-0.14 l0.06,0.14 l0.04,-0.07" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round" stroke-linecap="round"/>' % k.c("#ffd23a"))
    o.append('<path d="M0.52,-0.18 L0.52,-0.22 M0.52,-0.14 L0.52,-0.18" stroke="%s" stroke-width="0.020"/><path d="M0.46,-0.22 L0.58,-0.22 M0.46,-0.14 L0.58,-0.14" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (w, w))
    o.append('<path d="M0.08,0.03 L0.08,0.10 M0.04,0.03 L0.12,0.03 M0.055,0.10 L0.105,0.10" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % w)
    o.append('<circle cx="0.76" cy="0.0" r="0.075" fill="#2a5ec8" stroke="%s" stroke-width="0.020"/><path d="M0.71,-0.05 L0.81,0.05 M0.81,-0.05 L0.71,0.05" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (w, k.c("#ffd23a")))
    o.append('<path d="M0.40,0.18 L0.40,0.10 L0.50,0.10 L0.50,0.18" fill="none" stroke="%s" stroke-width="0.020"/>' % w)
    for (x, y) in ((0.08, -0.18), (0.76, -0.18), (0.76, 0.18), (0.08, 0.18), (0.44, 0.18)):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, y, k.c("#ffd23a"), k.ink))
    o.append('<path d="M0.04,-0.26 L0.30,-0.26" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % w)
    return "".join(o)


def _typewriter_body(k):
    """a desk typewriter seen from the front, centred on (0, 0): paper rising from the roller, a carriage, rows of keys (0.84 x 0.62)."""
    o = ['<rect x="-0.16" y="-0.46" width="0.32" height="0.34" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#fbf7ea"), k.ink)]
    for i in range(4):
        o.append('<path d="M-0.12,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (-0.40 + i * 0.065, 0.12 - 0.05 * (i == 3), -0.40 + i * 0.065, k.c("#6a6a78")))
    o.append('<rect x="-0.42" y="-0.16" width="0.84" height="0.07" rx="0.030" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#2a2a34"), k.ink))
    o.append('<path d="M-0.34,-0.145 L0.34,-0.145" stroke="#9aa0b8" stroke-width="0.010" opacity="0.8"/>')
    o.append('<path d="M-0.36,-0.09 L0.36,-0.09 L0.42,0.30 L-0.42,0.30 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c("#34343e"), k.ink))
    for r in range(3):
        for c in range(9 - r):
            x = -0.30 + c * 0.075 + r * 0.03 - (0 if r == 0 else 0.0)
            o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, -0.02 + r * 0.085, k.c("#ece8d8"), k.ink))
    o.append('<rect x="-0.20" y="0.245" width="0.40" height="0.036" rx="0.012" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#ece8d8"), k.ink))
    return "".join(o)


def _pillar_body(k, w, h):
    """a stone pillar with a cap and a plinth (x 0 .. w, y 0 .. h) for off_peek."""
    g = _lin(k, "pi", "#f4ecd8", "#d8cba8", "#a89870", 0, 0, w, 0)
    o = ['<rect x="0" y="0.0" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.026"/>' % (w, h, g, k.ink)]
    o.append('<rect x="-0.05" y="0.0" width="%.4f" height="0.12" fill="%s" stroke="%s" stroke-width="0.022"/>' % (w + 0.10, k.c("#c4b48a"), k.ink))
    o.append('<rect x="-0.05" y="%.4f" width="%.4f" height="0.14" fill="%s" stroke="%s" stroke-width="0.022"/>' % (h - 0.14, w + 0.10, k.c("#c4b48a"), k.ink))
    for x in (0.16 * w, 0.40 * w):
        o.append('<path d="M%.4f,0.14 L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (x, x, h - 0.16, k.c("#a89870")))
    return "".join(o)


def _desk_body(k, w, h, drawer):
    """a 1930s office desk seen from the front (x 0 .. w, top surface y -0.10 .. 0, front panel to y = h): green leather inset, a
    drawer pedestal with brass handles; drawer > 0.5 pulls the top drawer open with papers in it."""
    gt = _lin(k, "dk", DARKWOOD["light"], DARKWOOD["base"], DARKWOOD["dark"], 0, 0, w, 0)
    o = ['<path d="M0.10,-0.12 L%.4f,-0.12 L%.4f,0.0 L0.0,0.0 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (w - 0.10, w, k.c("#2f7a52"), k.ink)]
    o.append('<path d="M0.16,-0.10 L%.4f,-0.10" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (w - 0.16, k.c("#5ab088")))
    o.append('<rect x="-0.05" y="0.0" width="%.4f" height="0.12" rx="0.014" fill="%s" stroke="%s" stroke-width="0.022"/>' % (w + 0.10, k.c(DARKWOOD["light"]), k.ink))
    o.append('<rect x="0.04" y="0.12" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.022"/>' % (w - 0.08, h - 0.12, gt, k.ink))
    px = 0.14
    o.append('<rect x="%.4f" y="0.20" width="0.78" height="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (px, h - 0.30, k.c(DARKWOOD["base"]), k.ink))
    hh = (h - 0.30) / 3.0
    for i in range(3):
        y = 0.20 + i * hh
        if i == 0 and drawer > 0.5:
            o.append('<rect x="%.4f" y="%.4f" width="0.78" height="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (px, y + 0.05, hh - 0.02, k.c("#2a1608"), k.ink))
            for j, (dx, dy, c) in enumerate(((0.06, -0.05, "#ffffff"), (0.14, -0.10, "#fbf3d8"), (0.30, -0.07, "#ffffff"), (0.46, -0.12, "#fbf3d8"))):
                o.append('<path d="M%.4f,%.4f l0.26,-0.02 l0.0,-0.14 l-0.26,0.02 Z" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%d %.4f %.4f)"/>' % (px + dx, y + 0.12 + dy, k.c(c), k.ink, (-8, 5, -3, 9)[j], px + dx, y + 0.12 + dy))
            continue
        o.append('<rect x="%.4f" y="%.4f" width="0.78" height="%.4f" rx="0.010" fill="%s" stroke="%s" stroke-width="0.014"/>' % (px + 0.03, y + 0.03, hh - 0.04, k.c(DARKWOOD["light"]), k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.18" height="0.036" rx="0.016" fill="%s" stroke="%s" stroke-width="0.010"/>' % (px + 0.33, y + hh * 0.42, k.c(GOLDC["base"]), k.ink))
    o.append('<rect x="%.4f" y="0.20" width="0.50" height="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (w - 0.64, h - 0.30, k.c("#3a2010"), k.ink))
    return "".join(o)


def _daily_body(k):
    """a folded daily newspaper (x 0 .. 0.54, y +-0.21): black masthead THE DAILY, a big headline, a photo box, columns of text."""
    o = ['<rect x="0.0" y="-0.21" width="0.54" height="0.42" rx="0.006" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#f1ecda"), k.ink)]
    o.append('<rect x="0.0" y="-0.21" width="0.54" height="0.075" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#1c1a20"), k.ink))
    o.append('<text x="0.27" y="-0.155" font-family="DejaVu Serif, Georgia, serif" font-size="0.050" font-weight="700" fill="#ffffff" text-anchor="middle">THE DAILY</text>')
    o.append('<rect x="0.03" y="-0.115" width="0.48" height="0.050" fill="%s"/>' % k.c("#2a2830"))
    o.append('<rect x="0.03" y="-0.040" width="0.20" height="0.140" fill="%s" stroke="%s" stroke-width="0.008"/><path d="M0.03,0.100 L0.11,0.02 L0.17,0.07 L0.23,0.00 L0.23,0.100 Z" fill="%s"/>' % (k.c("#9aa4b4"), k.ink, k.c("#5a6474")))
    for i in range(5):
        o.append('<path d="M0.26,%.4f L0.51,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.75"/>' % (-0.030 + i * 0.030, -0.030 + i * 0.030, k.c("#4a4a56")))
    for i in range(3):
        o.append('<path d="M0.03,%.4f L0.51,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.75"/>' % (0.130 + i * 0.026, 0.130 + i * 0.026, k.c("#4a4a56")))
    return "".join(o)


NEW_PROPS22 = ("ruler", "pen", "set_square", "t_square", "roll", "sheet", "stamp", "pocketmap", "pocketmap_open", "fork", "knife", "letter",
               "briefcase", "handbag", "umbrella", "teacup", "magnifier", "handtruck", "circuit", "daily")
NEW_TIP22 = {"ruler": 0.70, "pen": 0.36, "set_square": 0.50, "t_square": 1.10, "roll": 0.42, "sheet": SHEET_W, "stamp": 0.29, "pocketmap": 0.34,
             "pocketmap_open": 0.64, "fork": 0.50, "knife": 0.50, "letter": 0.48, "briefcase": 0.43, "handbag": 0.39, "umbrella": 1.12, "teacup": 0.0,
             "magnifier": 0.47, "handtruck": 1.30, "circuit": 0.84, "daily": 0.54}
_UPRIGHT22 = ("briefcase", "handbag", "teacup", "handtruck")
_EXT22 = {"ruler": ((-0.20, -0.05), (0.72, 0.05)), "pen": ((-0.12, -0.07), (0.36, 0.03)), "set_square": ((-0.08, 0.08), (0.58, 0.08), (-0.08, -0.58)),
          "t_square": ((-0.16, -0.20), (1.12, 0.04)), "roll": ((-0.45, -0.08), (0.48, 0.09)), "sheet": ((0, -0.34), (SHEET_W, -0.34), (0, 0.34), (SHEET_W, 0.34)),
          "stamp": ((-0.14, -0.06), (0.30, 0.10)), "pocketmap": ((0, -0.125), (0.34, 0.125)), "pocketmap_open": ((0, -0.22), (0.64, 0.22)),
          "fork": ((-0.16, -0.06), (0.52, 0.06)), "knife": ((-0.16, -0.03), (0.52, 0.03)), "letter": ((0, -0.17), (0.48, 0.17)),
          "umbrella": ((-0.32, 0.18), (1.13, -0.07)), "magnifier": ((-0.05, -0.18), (0.65, 0.18)), "circuit": ((0, -0.30), (0.84, 0.30)), "daily": ((0, -0.21), (0.54, 0.21))}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS22:
        return _O22["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    if kind in _UPRIGHT22:
        if kind == "briefcase":
            body, pts, tip = _briefcase_body(k), ((-0.24, 0.43), (0.24, 0.43), (0.0, -0.03)), 0.43
        elif kind == "handbag":
            body, pts, tip = _handbag_body(k), ((-0.20, 0.39), (0.20, 0.39), (0.0, -0.05)), 0.39
        elif kind == "teacup":
            body, pts, tip = _cup_body(k, _POSE22["t"]), ((-0.25, -0.12), (0.10, -0.12), (-0.12, 0.05), (-0.15, -0.40)), 0.0
        else:
            b, gr = _handtruck_body(k, sc)
            body, pts, tip = b, ((-0.06, 0.0), (0.84, 0.0), (0.84, gr), (0.04, gr)), gr
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc if kind != "handtruck" else 1.0, body)
        for (x, y) in pts:
            k.ext.append((H[0] + x * (sc if kind != "handtruck" else 1.0), H[1] + y * (sc if kind != "handtruck" else 1.0), 0.03))
        t = (H[0], H[1] + tip * (sc if kind != "handtruck" else 1.0))
        an["%s_%s" % (kind, key)] = t
        return o, t
    body = {"ruler": _ruler_body, "pen": _pen_body, "set_square": _setsq_body, "t_square": _tsq_body, "roll": _roll_body, "sheet": _sheet_body,
            "stamp": _stamp_body, "pocketmap": _pmap_closed, "pocketmap_open": _pmap_open, "knife": _knife_body, "letter": _letter_body,
            "umbrella": _umbrella_body, "magnifier": _magnifier_body, "circuit": _circuit_body, "daily": _daily_body}.get(kind)
    s = body(k) if body else _fork_body(k, _POSE22["fork_map"])
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, s)
    for e in _EXT22.get(kind, ((-0.1, -0.1), (0.5, 0.1))):
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(NEW_TIP22[kind] * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an["%s_%s" % (kind, key)] = tip
    return o, tip


# ============================================================================= standalone pieces (SVG fragments in D units)
def _std(name, fn, uid, ink, tint, *a):
    k = _ctx(uid, ink, tint)
    s = fn(k, *a)
    return '<g id="%s_%s"><defs>%s</defs>%s</g>' % (k.uid, name, "".join(k.defs), s)


def prop_svg(kind, uid="pp", ink=P.INK, tint=None):
    """one new prop alone (hand grip at (0, 0), drawn along +x, size as held).  kind in NEW_PROPS22."""
    fns = {"ruler": _ruler_body, "pen": _pen_body, "set_square": _setsq_body, "t_square": _tsq_body, "roll": _roll_body, "sheet": _sheet_body,
           "stamp": _stamp_body, "pocketmap": _pmap_closed, "pocketmap_open": _pmap_open, "knife": _knife_body, "letter": _letter_body,
           "briefcase": _briefcase_body, "handbag": _handbag_body, "umbrella": _umbrella_body, "teacup": _cup_body, "magnifier": _magnifier_body, "circuit": _circuit_body, "daily": _daily_body}
    k = _ctx(uid, ink, tint)
    if kind == "handtruck":
        s = _handtruck_body(k, 1.0)[0]
    elif kind == "fork":
        s = _fork_body(k, 0.0)
    elif kind == "fork_map":
        s = _fork_body(k, 1.0)
    else:
        s = fns[kind](k)
    return '<g id="%s_%s"><defs>%s</defs>%s</g>' % (k.uid, kind, "".join(k.defs), s)


def desk_svg(uid="dk", w=1.6, h=1.0, drawer=0.0, ink=P.INK, tint=None):
    """the office desk alone (x 0 .. w, top surface at y 0, front panel down to y = h)."""
    return _std("desk", lambda k: _desk_body(k, w, h, drawer), uid, ink, tint)


def typewriter_svg(uid="tw", ink=P.INK, tint=None):
    """the typewriter alone, centred on (0, 0) (0.84 x 0.78)."""
    return _std("typewriter", _typewriter_body, uid, ink, tint)


def pillar_svg(uid="pi", w=0.5, h=1.6, ink=P.INK, tint=None):
    """the pillar alone (x 0 .. w, y 0 .. h)."""
    return _std("pillar", lambda k: _pillar_body(k, w, h), uid, ink, tint)


def board_svg(uid="bd", ink=P.INK, tint=None):
    """the drafting board with the diagram in progress (x 0 .. 1.55, y -0.55 .. 0.55)."""
    return _std("board", _board_body, uid, ink, tint)


# ============================================================================= hair, hats (head frame)
def _arc_pts(R, a0, a1, n=9):
    return [(R * math.cos(math.radians(a0 + (a1 - a0) * i / (n - 1.0))), R * math.sin(math.radians(a0 + (a1 - a0) * i / (n - 1.0)))) for i in range(n)]


def _hair_parted(k, H, yaw):
    """Beck: neat dark side-parted hair: a cap over the skull with the parting on the left, a swept fringe on the long side
    and the short side swept back; sideburns above the ears."""
    col, sh = H["color"], H.get("shine", "#6a4a36")
    dx = 0.12 * yaw
    px = -0.10 + dx
    top = _arc_pts(0.515, 186, 354, 11)
    line = [(0.50, -0.02), (0.46, -0.11), (0.36, -0.19), (0.18, -0.27), (px + 0.06, -0.31), (px - 0.02, -0.25), (px - 0.12, -0.20), (-0.28, -0.16),
            (-0.40, -0.12), (-0.47, -0.05)]
    pts = top + line
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)]
    o.append('<path d="M%.4f,-0.50 Q%.4f,-0.40 %.4f,-0.31" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (px + 0.03, px + 0.01, px - 0.01, k.c("#cdb89a")))
    for (x0, x1) in ((-0.36, -0.20), (-0.24, -0.10)):
        o.append('<path d="M%.4f,-0.45 Q%.4f,-0.38 %.4f,-0.25" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (x0 + dx, (x0 + x1) / 2 + dx - 0.03, x1 + dx - 0.04, k.c(sh)))
    for (x0, x1) in ((0.12, 0.26), (0.26, 0.38)):
        o.append('<path d="M%.4f,-0.46 Q%.4f,-0.40 %.4f,-0.27" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (x0 + dx, (x0 + x1) / 2 + dx + 0.02, x1 + dx, k.c(sh)))
    o.append('<path d="M-0.30,-0.50 Q-0.10,-0.56 0.10,-0.54" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.35"/>')
    for p in top[::2] + [(-0.50, 0.0), (0.50, 0.0)]:
        k.ext.append(p + (0.03,))
    if H.get("pencil"):
        sd = -1.0 if yaw >= 0 else 1.0
        x0, y0, x1, y1 = sd * 0.43, 0.02, sd * 0.54, -0.20
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (x0, y0, x1, y1, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (x0, y0, x1, y1, k.c("#f2b820")))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.036" stroke-linecap="butt"/>' % (x1 - sd * 0.014, y1 + 0.03, x1 - sd * 0.02, y1 + 0.045, k.c("#e8a0a0")))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>' % (x0 - sd * 0.008, y0, x1 - sd * 0.008, y1, "#ffffff"))
        k.ext.append((x1, y1 - 0.04, 0.04))
    return "".join(o), (0.0, -0.55)


def _hair_comb(k, H, yaw, bald_col=None):
    """official: bald crown with a ring of ginger hair above the ears and five long strands combed across the scalp."""
    col, sh = H["color"], H.get("shine", "#e08a40")
    dx = 0.12 * yaw
    o = []
    for s in (-1, 1):
        pts = [(s * 0.30, -0.37), (s * 0.43, -0.30), (s * 0.52, -0.18), (s * 0.545, -0.04), (s * 0.52, 0.06), (s * 0.475, 0.00), (s * 0.47, -0.12), (s * 0.40, -0.23)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        for p in pts[1:5]:
            k.ext.append((p[0], p[1], 0.03))
    n = H.get("strands", 5)
    st = []
    for i in range(n):
        f = i / max(1.0, n - 1.0)
        y0 = -0.30 - 0.025 * i
        d = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (-0.42, y0, -0.30 + dx, -0.50 + 0.07 * f - 0.03, 0.10 + dx, -0.56 + 0.12 * f, 0.40, -0.26 - 0.03 * f)
        st.append(d)
    for w, c in ((0.026, k.ink), (0.011, k.c(col))):
        for d in st:
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, c, w))
    o.append('<path d="M0.16,-0.43 Q0.28,-0.40 0.34,-0.32" fill="none" stroke="#ffffff" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>')
    return "".join(o), (0.0, -0.52)


def _hair_bald(k, H, yaw):
    col = H["color"]
    o = []
    for s in (-1, 1):
        pts = [(s * 0.33, -0.28), (s * 0.45, -0.22), (s * 0.525, -0.10), (s * 0.54, 0.04), (s * 0.50, 0.10), (s * 0.465, 0.02), (s * 0.45, -0.10), (s * 0.39, -0.19)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        for p in pts[1:5]:
            k.ext.append((p[0], p[1], 0.03))
    o.append('<path d="M-0.16,-0.43 Q-0.04,-0.47 0.08,-0.45" fill="none" stroke="#ffffff" stroke-width="0.026" stroke-linecap="round" opacity="0.8"/>')
    o.append('<ellipse cx="0.20" cy="-0.38" rx="0.030" ry="0.018" fill="#ffffff" opacity="0.7" transform="rotate(-25 0.20 -0.38)"/>')
    return "".join(o), (0.0, -0.52)


def _hair_bob(k, H, yaw):
    """clerk_b: a 1930s bob (chin-length, finger-waved) with a straight-cut fringe and a small hair slide."""
    col, sh = H["color"], H.get("shine", "#8a5a3a")
    dx = 0.10 * yaw
    o = [CE._bob(k, yaw, col)]
    top = _arc_pts(0.515, 184, 356, 11)
    line = [(0.50, -0.03), (0.47, -0.12), (0.40, -0.17), (0.26, -0.19), (0.10, -0.205), (-0.08, -0.215), (-0.24, -0.20), (-0.38, -0.17), (-0.46, -0.11), (-0.50, -0.03)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(top + line), k.c(col), k.ink))
    for x in (-0.30, -0.12, 0.06, 0.24, 0.40):
        o.append('<path d="M%.4f,-0.46 Q%.4f,-0.34 %.4f,-0.21" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.85"/>' % (x + dx, x + dx - 0.02, x + dx * 0.5 - 0.01, k.c(sh)))
    o.append('<path d="M-0.30,-0.50 Q-0.10,-0.56 0.12,-0.54" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.35"/>')
    sx = -0.36
    o.append('<path d="M%.4f,-0.30 L%.4f,-0.22" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M%.4f,-0.30 L%.4f,-0.22" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
             % (sx + dx, sx + dx - 0.05, k.ink, sx + dx, sx + dx - 0.05, k.c(H.get("slide", "#e2b442"))))
    return "".join(o), (0.0, -0.55)


def _hair_white(k, H, yaw):
    return _hair_bald(k, dict(H, color=H["color"]), yaw)


def _hat_hair22(k, C, yaw):
    H = C["hair22"]
    st = H.get("style", "parted")
    fn = {"parted": _hair_parted, "comb": _hair_comb, "bald": _hair_bald, "bob": _hair_bob, "white": _hair_white}[st]
    svg, top = fn(k, H, yaw)
    return '<g transform="rotate(%.3f)">%s</g>' % (C.get("hat_tilt", 0.0), svg), top


def _hat_cloche22(k, C, yaw):
    """1930s cloche: a deep bell pulled down to the brows, a small turned-up edge, a ribbon band with a bow and a flower."""
    col = C["hat_colors"]
    dx = 0.10 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "cl", col, x0=-0.6, x1=0.6, mid=0.34)
    crown = [(-0.545, -0.06), (-0.585, -0.30), (-0.43, -0.58), (0.0 + dx * 0.4, -0.64), (0.43, -0.58), (0.585, -0.30), (0.545, -0.06),
             (0.40 + dx, -0.115), (0.0 + dx, -0.175), (-0.40 + dx, -0.115)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (P._smooth_closed(crown), g, k.ink))
    # ribbon band
    band = "M-0.56,-0.14 Q%.4f,-0.20 0.56,-0.14 L0.57,-0.235 Q%.4f,-0.29 -0.57,-0.235 Z" % (dx, dx)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    o.append('<path d="M-0.50,-0.54 Q-0.30,-0.62 -0.06,-0.60" fill="none" stroke="#ffffff" stroke-width="0.022" stroke-linecap="round" opacity="0.55"/>')
    o.append('<path d="M-0.40,-0.40 Q0.0,-0.34 0.40,-0.40" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(col["dark"]))
    # flower + bow at the side opposite the face
    sd = -1.0 if yaw >= 0 else 1.0
    fx, fy = sd * 0.40, -0.215
    for a in range(0, 360, 60):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.050" fill="%s" stroke="%s" stroke-width="0.010"/>' % (fx + 0.050 * math.cos(math.radians(a)), fy + 0.050 * math.sin(math.radians(a)), k.c(col["flower"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.032" fill="%s" stroke="%s" stroke-width="0.010"/>' % (fx, fy, k.c("#f6d84a"), k.ink))
    o.append('</g>')
    for p in ((-0.58, -0.30), (0.58, -0.30), (0.0, -0.64), (fx, fy + 0.06)):
        k.ext.append(_rot(p[0], p[1], C["hat_tilt"]) + (0.03,))
    return "".join(o), (0.0, -0.645)


def _hat_schoolcap22(k, C, yaw):
    """school cap: a round panelled crown with a button, a band with a badge, a short stiff peak on the facing side."""
    col = C["hat_colors"]
    dx = 0.10 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "sc", col, x0=-0.56, x1=0.56, mid=0.34)
    crown = [(-0.52, -0.20), (-0.56, -0.38), (-0.42, -0.56), (0.0 + dx * 0.4, -0.62), (0.42, -0.56), (0.56, -0.38), (0.52, -0.20), (0.0 + dx, -0.15)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(crown), g, k.ink))
    for x in (-0.30, -0.10, 0.12, 0.32):
        o.append('<path d="M%.4f,-0.60 Q%.4f,-0.40 %.4f,-0.17" fill="none" stroke="%s" stroke-width="0.010" opacity="0.9"/>' % (dx * 0.4 + x * 0.25, x * 1.1 + dx * 0.6, x + dx * 0.8, k.c(col["dark"])))
    o.append('<path d="M-0.52,-0.20 Q%.4f,-0.13 0.52,-0.20 L0.53,-0.30 Q%.4f,-0.23 -0.53,-0.30 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (dx, dx, k.c(col["band"]), k.ink))
    o.append('<circle cx="%.4f" cy="-0.625" r="0.030" fill="%s" stroke="%s" stroke-width="0.012"/>' % (dx * 0.4, k.c(col["piping"]), k.ink))
    o.append('<path d="M-0.40,-0.20 Q%.4f,-0.14 0.40,-0.20" fill="none" stroke="%s" stroke-width="0.014" opacity="0.95"/>' % (dx, k.c(col["piping"])))
    bx = dx + 0.10 * (1 if yaw >= 0 else -1) * 0 + 0.0
    o.append('<path d="M%.4f,-0.285 L%.4f,-0.285 L%.4f,-0.205 L%.4f,-0.19 L%.4f,-0.205 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (bx - 0.05, bx + 0.05, bx + 0.05, bx, bx - 0.05, k.c(col["piping"]), k.ink))
    vx = 0.30 * yaw
    o.append('<path d="M%.4f,-0.20 Q%.4f,-0.13 %.4f,-0.09 Q%.4f,-0.075 %.4f,-0.09 Q%.4f,-0.13 %.4f,-0.20 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (vx - 0.30, vx - 0.28, vx - 0.18, vx, vx + 0.18, vx + 0.28, vx + 0.30, k.c(col["dark"]), k.ink))
    o.append('</g>')
    for p in ((-0.56, -0.38), (0.56, -0.38), (0.0, -0.65), (vx - 0.30, -0.10), (vx + 0.30, -0.10)):
        k.ext.append(_rot(p[0], p[1], C["hat_tilt"]) + (0.03,))
    return "".join(o), (0.0, -0.65)


def _hat_porter22(k, C, yaw):
    svg, top = C10.HATS10["peaked10"](k, C, yaw)
    dx = -0.03 * yaw
    fx = dx + 0.12 * yaw
    badge = '<g transform="rotate(%.3f)">%s</g>' % (C["hat_tilt"], _roundel(k, fx, -0.335, 0.062, 0.010))
    return svg + badge, top


def _hat_bowler22(k, C, yaw):
    old = CE._tufts
    CE._tufts = lambda kk, yw: _hair_bald(kk, dict(color=C["hair"]["color"]), yw)[0]
    try:
        return CE._hat_bowler(k, C, yaw)
    finally:
        CE._tufts = old


HATS22 = {"bowler22": _hat_bowler22, "hair22": _hat_hair22, "cloche22": _hat_cloche22, "schoolcap22": _hat_schoolcap22, "porter22": _hat_porter22}


# ============================================================================= costumes (torso-local)
def _cos_vest22(k, C, m):
    """shirt + waistcoat (or a knitted jumper vest / school jumper): white collar, a tie (or bow), the waistcoat panels with a V
    opening, centre buttons, welt pockets, a pointed hem.  vest_style 'waistcoat' / 'knit'."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    vb = TT + h * C.get("vest_v", 0.40)
    knit = C.get("vest_style") == "knit"
    o = []
    o.append(_poly(k, [X(-0.13, 0.40), X(0.13, 0.40), X(0.0, vb + 0.02)], k.c(col["shirt"]), 0.012))
    vg = C2._grad(k, "vs", col["vest"], -hw, hw)
    for s in (-1, 1):
        pan = [X(s * 0.115, 0.39), X(s * hw * 1.2, 0.44), X(s * hw * 1.2, yB + 0.05), X(0.0, yB + 0.07), X(0.0, vb)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(pan), vg, k.ink))
        if knit:
            o.append(_ln([X(s * 0.115, 0.40), X(0.0, vb)], k.c(col.get("trim", "#f5c400")), 0.016))
            o.append(_ln([X(s * 0.135, 0.435), X(0.0, vb + 0.045)], k.c(col.get("trim2", "#d8231c")), 0.012))
    if knit:
        for i in range(9):
            x = -0.40 + i * 0.10
            o.append(_ln([X(x, yB - 0.10), X(x, yB + 0.05)], k.c(col["vest_d"]), 0.012, ' opacity="0.8"'))
        o.append(_ln([X(-0.8, yB - 0.10), X(0.8, yB - 0.10)], k.c(col["vest_d"]), 0.012))
    else:
        for i in range(4):
            y = vb + 0.09 + i * 0.11
            if y < yB - 0.04:
                o.append(_circ(X(0.0, y), 0.017, k.c(col.get("button", "#d8c070")), k, 0.008))
        for s in (-1, 1):
            o.append(_ln([X(s * 0.20, yB - 0.20), X(s * 0.34, yB - 0.18)], k.c(col["vest_d"]), 0.020))
        o.append(_ln([X(-0.28, 0.46), X(-0.30, 0.62)], k.c(P._shade(col["vest"], 1.35)), 0.010, ' opacity="0.7"'))
    # collar points + tie
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.11, 0.39), X(s * 0.015, 0.455), X(s * 0.10, 0.55)], k.c(col.get("collar", "#ffffff")), 0.013))
    neck = C.get("neck", "tie")
    tc, td = k.c(col["tie"]), k.c(col.get("tie_dark", P._shade(col["tie"], 0.7)))
    if neck == "bow":
        o.append(C7._neck(k, X, col, "bow", 0.40))
    else:
        o.append(_poly(k, [X(-0.030, 0.47), X(0.030, 0.47), X(0.022, 0.53), X(-0.022, 0.53)], td, 0.011))
        o.append(_poly(k, [X(-0.026, 0.52), X(0.026, 0.52), X(0.058, vb + 0.20), X(0.0, vb + 0.27), X(-0.058, vb + 0.20)], tc, 0.013))
        o.append(_ln([X(-0.010, 0.56), X(-0.022, vb + 0.16)], td, 0.009, ' opacity="0.7"'))
        if col.get("tie_stripe"):
            o.append(_ln([X(-0.04, vb + 0.06), X(0.04, vb + 0.02)], k.c(col["tie_stripe"]), 0.012))
            o.append(_ln([X(-0.05, vb + 0.12), X(0.05, vb + 0.08)], k.c(col["tie_stripe"]), 0.012))
    return "".join(o), "", ""


def _cos_woman22(k, C, m):
    """1930s woman: a blouse with a Peter Pan collar and a bow, a cardigan (or a coat when C coat=True) with a button band and
    pockets, a belt, an A-line skirt (or the coat skirt) to mid-calf, drawn over the legs."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * 0.68
    coat = bool(C.get("coat"))
    yh = yB + 0.04 if coat else yw + 0.06
    cg = C2._grad(k, "cg", col["cardigan"], -hw, hw)
    o = [_poly(k, [X(-0.14, 0.40), X(0.14, 0.40), X(0.0, TT + h * 0.50)], k.c(col["blouse"]), 0.012)]
    for s in (-1, 1):
        pan = [X(s * 0.12, 0.39), X(s * hw * 1.2, 0.44), X(s * hw * 1.2, yh), X(s * 0.01, yh), X(s * 0.012, TT + h * 0.46)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(pan), cg, k.ink))
    o.append(_ln([X(0.0, TT + h * 0.46), X(0.0, yh)], k.c(col["trim"]), 0.030))
    o.append(_ln([X(0.0, TT + h * 0.46), X(0.0, yh)], k.ink, 0.008))
    for i in range(4 if not coat else 5):
        y = TT + h * 0.52 + i * (0.12 if not coat else 0.13)
        if y < yh - 0.03:
            o.append(_circ(X(0.0, y), 0.020, k.c(col["button"]), k, 0.009))
    if not coat:
        for s in (-1, 1):
            o.append(_ln([X(s * 0.22, yw - 0.12), X(s * 0.34, yw - 0.10)], k.c(col["trim"]), 0.018))
    # Peter Pan collar + bow
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(s * 0.02, 0.45) + X(s * 0.10, 0.37) + X(s * 0.17, 0.46) + X(s * 0.14, 0.54) + X(s * 0.02, 0.52) + (k.c(col["collar"]), k.ink)))
    bx, by = X(0.0, 0.50)
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (bx, by, bx + s * 0.08, by - 0.04, bx + s * 0.08, by + 0.04, k.c(col["bow"]), k.ink))
    o.append(_circ((bx, by), 0.016, k.c(col["bow"]), k, 0.008))
    if coat:
        for s in (-1, 1):
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                     % (X(s * 0.06, 0.42) + X(s * 0.24, 0.36) + X(s * 0.36, 0.52) + X(s * 0.30, 0.74) + X(s * 0.04, 0.68) + (k.c(col["collar_c"]), k.ink)))
    inside = "".join(o)
    hem = yB + C["leg"] * C.get("hem_frac", 0.62)
    a = hw * (0.98 if coat else 0.82)
    b = hw + C.get("skirt_flare", 0.22)
    sk = C2._grad(k, "sk", col["cardigan"] if coat else col["skirt"], -b, b)
    ov = [C2._skirt(k, "w22", X, (yh - 0.05) if coat else (yw - 0.02), a, hem, b, sk, sw=0.026,
                    folds=((-0.12, yw + 0.20, -0.20, hem - 0.05), (0.12, yw + 0.20, 0.22, hem - 0.05), (0.0, yw + 0.24, 0.02, hem - 0.05)),
                    fold_col=k.c(P._shade(col["cardigan"] if coat else col["skirt"], 0.7)))]
    if coat:
        ov.append(_ln([X(0.0, yh), X(0.02, hem - 0.01)], k.ink, 0.014))
        for s in (-1, 1):
            ov.append(_ln([X(s * 0.20, yh + 0.10), X(s * 0.32, yh + 0.12)], k.c(col["trim"]), 0.018))
    else:
        ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.ink, 0.046))
        ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.c(col["belt"]), 0.026))
        c = X(0.0, yw - 0.02)
        ov.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.040" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (c[0] - 0.03, c[1] - 0.02, k.c(GOLDC["base"]), k.ink))
    return inside, "", "".join(ov)


def _pinstripe(k, name, x0, y0, x1, y1, col, op=0.55):
    k.defs.append('<pattern id="%s_%s" width="0.075" height="0.5" patternUnits="userSpaceOnUse"><rect x="0.030" y="0" width="0.010" height="0.5" fill="%s"/></pattern>' % (k.uid, name, k.c(col)))
    return '<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="url(#%s_%s)" opacity="%.2f"/>' % (x0, y0, x1 - x0, y1 - y0, k.uid, name, op)


def _cos_suit22(k, C, m):
    """the official: cast7's frock/lounge suit (peaked lapels, waistcoat, bow tie, watch chain, carnation) with navy chalk
    pinstripes on the coat, waistcoat and skirt; pose napkin=1 tucks a checked napkin into the collar."""
    inside, behind, over = C7._cos_frock7(k, C, m)
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    st = col.get("stripe", "#8fa8e8")
    extra = [_pinstripe(k, "pn0", -hw * 1.3, 0.40, -0.27, yB + 0.1, st), _pinstripe(k, "pn1", 0.27, 0.40, hw * 1.3, yB + 0.1, st),
             _pinstripe(k, "pn2", -0.11, yB * 0.72, 0.11, yB, st, 0.4)]
    inside = inside + "".join(extra)
    yt = yB - 0.10
    hem = yB + C.get("coat_len", 0.5)
    a = hw * 0.99
    over = over + _pinstripe(k, "pn3", -a * 0.97, yt + 0.02, a * 0.97, hem - 0.03, st, 0.5)
    if _POSE22["napkin"] > 0.5:
        nk = []
        nap = [X(-0.10, 0.40), X(0.10, 0.40), X(0.33, 0.78), X(0.30, 1.02), X(0.0, 1.07), X(-0.30, 1.02), X(-0.33, 0.78)]
        nk.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(nap), k.c("#fbfaf4"), k.ink))
        for i in range(5):
            y = 0.62 + i * 0.09
            nk.append(_ln([X(-0.30, y), X(0.30, y)], k.c("#d8433a"), 0.012, ' opacity="0.65"'))
        for i in range(7):
            x = -0.28 + i * 0.093
            nk.append(_ln([X(x, 0.52), X(x * 1.0, 1.02)], k.c("#d8433a"), 0.012, ' opacity="0.65"'))
        nk.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (X(-0.09, 0.44) + X(0.0, 0.52) + X(0.09, 0.44) + (k.ink,)))
        inside = inside + "".join(nk)
    return inside, behind, over


def _cos_porter22(k, C, m):
    inside, behind, over = C7._cos_uniform7(k, C, m)
    X = _X(m)
    c = X(-0.20, 0.84)
    return inside + _roundel(k, c[0], c[1], 0.075, 0.011), behind, over


COSTUMES22 = {"vest22": _cos_vest22, "woman22": _cos_woman22, "suit22": _cos_suit22, "porter22": _cos_porter22}


# ============================================================================= limbs (knee socks) and face (flush, puffed cheeks)
def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O22["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast22") or tail is None or not C.get("socks22"):
        return out
    sc = C["socks22"]
    dx, dy = H[0] - E[0], H[1] - E[1]
    ln = math.hypot(dx, dy)
    if ln < 0.02:
        return out
    ux, uy = dx / ln, dy / ln
    p0 = (E[0] + ux * 0.02, E[1] + uy * 0.02)
    p1 = (H[0] - ux * 0.045, H[1] - uy * 0.045)
    out += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % (p0[0], p0[1], p1[0], p1[1], k.ink, w * 1.55 + 0.022)
    out += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % (p0[0], p0[1], p1[0], p1[1], k.c(sc["color"]), w * 1.55)
    nx, ny = -uy, ux
    for t in (0.10, 0.22):
        c = (E[0] + ux * ln * t, E[1] + uy * ln * t)
        out += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020"/>' % (c[0] - nx * w * 0.78, c[1] - ny * w * 0.78, c[0] + nx * w * 0.78, c[1] + ny * w * 0.78, k.c(sc["band"]))
    return out


def _face(k, C, P_, white):
    svg, L = _O22["_face"](k, C, P_, white)
    if C is None or not C.get("_cast22"):
        return svg, L
    under, over = [], []
    if _POSE22["flush"] > 0.02:
        cx = (L["xL"] + L["xR"]) / 2
        under.append('<ellipse cx="%.4f" cy="0.07" rx="0.44" ry="0.41" fill="%s" opacity="%.3f"/>' % (cx, k.c("#e8321e"), 0.62 * _POSE22["flush"]))
        under.append('<ellipse cx="%.4f" cy="0.12" rx="0.30" ry="0.25" fill="%s" opacity="%.3f"/>' % (cx, k.c("#ff6a4a"), 0.40 * _POSE22["flush"]))
    if _POSE22["puff"] > 0.02:
        for x, sd in ((L["xL"], -1), (L["xR"], 1)):
            over.append('<ellipse cx="%.4f" cy="%.4f" rx="0.135" ry="0.150" fill="%s" fill-opacity="0.72" stroke="%s" stroke-width="0.018"/>'
                        % (x + sd * 0.115, L["my"] - 0.005, k.c("#f0644e"), k.ink))
            over.append('<path d="M%.4f,%.4f q%.4f,0.03 %.4f,0.07" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.6"/>'
                        % (x + sd * 0.115 - 0.05, L["my"] - 0.06, 0.02, 0.0))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE22["napkin"] = _f(g("napkin"), 0.0, 0.0, 1.0)
    _POSE22["flush"] = _f(g("flush"), 0.0, 0.0, 1.0)
    _POSE22["puff"] = _f(g("puff"), 0.0, 0.0, 1.0)
    _POSE22["fork_map"] = _f(g("fork_map"), 0.0, 0.0, 1.0)
    _POSE22["board"] = _f(g("board"), 0.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE22["t"] = t if math.isfinite(t) else 0.0
    return _O22["_norm"](C, pose)


def figure(cast_name, pose=None, uid="p"):
    f = _O22["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    bd = _f(pose.get("board"), 0.0, 0.0, 1.0) >= 0.5
    tw = _f(pose.get("typewriter"), 0.0, 0.0, 1.0) >= 0.5
    pl = _f(pose.get("pillar"), 0.0, 0.0, 1.0) >= 0.5
    dk = _f(pose.get("desk"), 0.0, 0.0, 1.0) >= 0.5
    if not (bd or tw or pl or dk):
        return f
    k = P._Ctx(uid + "b", P.INK, None)
    mir = bool(pose.get("mirror"))
    s = -1.0 if mir else 1.0
    an = dict(f["anchors"])
    hx = an["head"][0]
    b = list(f["bbox"])
    behind, front = [], []

    def grow(x0, y0, x1, y1):
        b[0], b[1], b[2], b[3] = min(b[0], x0, x1), min(b[1], y0, y1), max(b[2], x0, x1), max(b[3], y0, y1)
    if bd:
        bx = _f(pose.get("board_x"), 0.25, -3.0, 3.0)
        by = _f(pose.get("board_y"), 0.55, -2.0, 4.0)
        sz = _f(pose.get("board_s"), 1.0, 0.3, 2.5)
        behind.append('<g transform="translate(%.4f %.4f) scale(%.4f %.4f)">%s</g>' % (hx + s * bx, by, s * sz, sz, _board_body(k)))
        grow(hx + s * bx, by - 0.56 * sz, hx + s * (bx + 1.55 * sz), by + 0.56 * sz)
        an["board_c"] = (hx + s * (bx + 0.75 * sz), by)
    if tw:
        tx = _f(pose.get("tw_x"), 0.40, -3.0, 3.0)
        ty = _f(pose.get("tw_y"), 1.45, -1.0, 4.0)
        behind.append('<g transform="translate(%.4f %.4f)">%s</g>' % (hx + s * tx, ty, _typewriter_body(k)))
        grow(hx + s * tx - 0.45, ty - 0.48, hx + s * tx + 0.45, ty + 0.32)
    if pl:
        px = _f(pose.get("pillar_x"), -0.12, -2.0, 2.0)
        pw = _f(pose.get("pillar_w"), 1.3, 0.3, 3.0)
        ph = f["feet_y"] + 1.2
        x0 = min(hx + s * px, hx + s * px - s * pw)
        front.append('<g transform="translate(%.4f %.4f)">%s</g>' % (x0, -1.2, _pillar_body(k, pw, ph)))
        grow(x0 - 0.05, -1.2, x0 + pw + 0.05, f["feet_y"])
        an["pillar_edge"] = (hx + s * px, 0.3)
    if dk:
        dx_ = _f(pose.get("desk_x"), 0.5, -3.0, 3.0)
        dy_ = _f(pose.get("desk_y"), 1.30, 0.4, 3.0)
        dw = _f(pose.get("desk_w"), 2.2, 0.8, 4.0)
        dd = _f(pose.get("desk_drawer"), 0.0, 0.0, 1.0)
        dh = max(0.5, f["feet_y"] + 0.04 - dy_)
        x0 = hx + s * dx_ - dw / 2
        front.append('<g transform="translate(%.4f %.4f)">%s</g>' % (x0, dy_, _desk_body(k, dw, dh, dd)))
        grow(x0 - 0.05, dy_ - 0.12, x0 + dw + 0.05, dy_ + dh)
        an["desk_top"] = (hx + s * dx_, dy_ - 0.06)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + "".join(behind) + f["svg"] + "".join(front), bbox=tuple(b), anchors=an)


# ============================================================================= cast
import copy  # noqa: E402

_FLAGS = dict(C10._FLAGS, _cast22=True)
_SH = lambda c: P._shade(c, 0.72)  # noqa: E731

_clerk = copy.deepcopy(P.CAST["clerk"])
NEW_CAST22 = {
    # Harry Beck: slim, neat dark side-parted hair, round wire glasses, white shirt with rolled sleeves and black sleeve garters,
    # a dark grey waistcoat, the red tie, grey trousers, a pencil behind the ear
    "beck": dict(
        _FLAGS, build="slim", seed=22.3,
        torso_w=0.60, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.23, 0.50), arm=0.76, hip_x=0.15, leg=1.26, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.040, brow="stroke", brow_th=0.046, mouth="dash", moustache=False, smirk_side=1, glasses=True, garters=True,
        hat="newsboy", hat_style="hair22", hat_tilt=-2.0, ear_pencil=False,
        hair22=dict(style="parted", color="#2a1c16", shine="#7a5a46", pencil=True),
        hair=dict(color="#2a1c16", front=0.07, grow=0.20),
        costume="vest22", neck="tie", vest_v=0.38,
        sleeve=dict(color="#f6f3ec", dark="#cdc6b6", cuff="#f6f3ec", len=0.50, roll=True, w=0.14),
        shorts=dict(color="#8a8f9e", dark="#5e6270", cuff="#8a8f9e", len=0.90, w=0.13),
        boots=dict(color="#1c1a20", cuff="#1c1a20", h=0.07, toe=0.15),
        colors=dict(base="#f6f3ec", shirt="#f6f3ec", collar="#ffffff", vest="#4c5066", vest_d="#2a2c3c", button="#d8c27a",
                    tie="#d8261e", tie_dark="#8a1410", garter="#1c1a20", pants="#8a8f9e"),
    ),
    # the publicity official: stout, comb-over, huge ginger handlebar, ruddy cheeks, navy pinstripe three-piece, gold chain,
    # yellow bow tie, red carnation
    "official": dict(
        _FLAGS, build="stout", seed=77.9,
        torso_w=1.26, torso_h=1.10, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.42, 0.44), arm=0.78, hip_x=0.18, leg=1.42, stance=0.07, wide=0.30, limb_w=0.068,
        eye_y=0.005, brow="stroke", brow_th=0.078, mouth="smirk", moustache=True, moustache_style="handlebar", tache_scale=1.45,
        smirk_side=1, cheeks="#ec6a52", chins=True,
        hat="newsboy", hat_style="hair22", hat_tilt=-2.0, ear_pencil=False,
        hair22=dict(style="comb", color="#cf6a22", shine="#f0a060", strands=5),
        hair=dict(color="#cf6a22", front=0.05, grow=0.18),
        costume="suit22", coat_len=0.34, coat_flare=0.12, neck="bow", chain=True, vest_buttons=4, double=True, flower="#e8283c",
        sleeve=dict(color="#2a479a", dark="#16255c", cuff="#f6f2ea", len=0.84, w=0.200),
        shorts=dict(color="#22398a", dark="#121f58", cuff="#22398a", len=0.90, w=0.17),
        boots=dict(color="#16141a", cuff="#16141a", h=0.08, toe=0.17),
        colors=dict(base="#27449a", dark="#121f58", lapel="#1a2c70", vest="#3358b0", vest_b="#e2b442", shirt="#fbfaf6", collar="#ffffff",
                    tie="#f5c400", tie_dark="#b88a00", button="#e2b442", pants="#22398a", moustache="#d9601a", moustache_l="#ff9a50",
                    stripe="#a9c0ff"),
    ),
    # clerk_a: the lanky young man with the green eyeshade, slicked hair, teal-striped shirt, mustard tie, red garters
    "clerk_a": dict(
        _clerk, _cast22=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, seed=23.1,
        hair=dict(color="#231a16", front=0.085, grow=0.22, style="cap", shine="#7a5a48"),
        colors=dict(base="#f3efe0", dark="#8a96a8", stripe="#1f9a80", collar="#fbfcfd", tie="#e8a014", tie_dark="#a8680a", clip="#e3c46a",
                    pocket="#d6dee8", pencil1="#efc13a", pencil2="#cf3b2c", button="#fbfbfb", belt="#5b3a26", buckle="#e3c46a",
                    pants="#5a4a78", garter="#d0302a"),
    ),
    # the woman typist: 1930s bob with a fringe, mustard cardigan over a cream blouse with a red bow, teal skirt
    "clerk_b": dict(
        _FLAGS, build="slim", seed=31.7,
        torso_w=0.54, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.215, 0.52), arm=0.72, hip_x=0.135, leg=1.14, stance=0.05, wide=0.24, limb_w=0.055,
        eye_y=0.050, brow="stroke", brow_th=0.032, mouth="smile", moustache=False, smirk_side=-1, lashes=True, cheeks="#f4989a",
        hat="newsboy", hat_style="hair22", hat_tilt=0.0, ear_pencil=False,
        hair22=dict(style="bob", color="#4a2a1c", shine="#9a6a48", slide="#e2b442"),
        hair=dict(color="#4a2a1c", front=0.05, grow=0.16),
        costume="woman22", hem_frac=0.60, skirt_flare=0.20,
        sleeve=dict(color="#e6a41c", dark="#b0760a", cuff="#fbf3e0", len=0.84, w=0.150),
        boots=dict(color="#7a1c22", cuff="#7a1c22", h=0.05, toe=0.12),
        colors=dict(base="#fbf3e0", blouse="#fbf3e0", cardigan="#e6a41c", skirt="#1f7a8a", collar="#ffffff", bow="#d8261e", button="#7a3a12", trim="#b0760a",
                    belt="#5a2a12", pants="#1f7a8a"),
    ),
    # clerk_c: the chubby older bald man with spectacles, cream shirt, maroon knitted vest, navy bow tie
    "clerk_c": dict(
        _FLAGS, build="stout", seed=44.6,
        torso_w=1.08, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.36, 0.46), arm=0.74, hip_x=0.16, leg=1.10, stance=0.06, wide=0.26, limb_w=0.066,
        eye_y=0.010, brow="stroke", brow_th=0.058, mouth="smile", moustache=False, smirk_side=1, glasses=True, age_lines=True, cheeks="#f0907e",
        hat="newsboy", hat_style="hair22", hat_tilt=0.0, ear_pencil=False,
        hair22=dict(style="bald", color="#a8a4ae"),
        hair=dict(color="#a8a4ae", front=0.03, grow=0.10),
        costume="vest22", neck="bow", vest_style="knit", vest_v=0.34,
        sleeve=dict(color="#f1ead8", dark="#cfc6aa", cuff="#f1ead8", len=0.84, w=0.170),
        shorts=dict(color="#6a4a32", dark="#4a3220", cuff="#6a4a32", len=0.90, w=0.15),
        boots=dict(color="#2a1c14", cuff="#2a1c14", h=0.07, toe=0.16),
        colors=dict(base="#f1ead8", shirt="#f1ead8", collar="#ffffff", vest="#8a2a3a", vest_d="#5a1624", trim="#e2b442", trim2="#e2b442",
                    tie="#1f3a8a", tie_dark="#10224f", pants="#6a4a32"),
    ),
    # passenger: grey overcoat, bowler, a small moustache, red waistcoat
    "pass_man": dict(
        _FLAGS, build="regular", seed=52.2,
        torso_w=0.86, torso_h=1.02, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.30, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.052, mouth="dash", moustache=False, pencil_moustache=True, smirk_side=1,
        hat="newsboy", hat_style="bowler22", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#4a4654", base="#26222c", dark="#12101a", shine="#8a8498", band="#8a1f2d", brim="#1e1a24", edge="#5a5666"),
        hair=dict(color="#4a3224", front=0.06, grow=0.20),
        costume="frock7", coat_len=0.52, coat_flare=0.12, neck="tie", chain=True, vest_buttons=4, double=True,
        sleeve=dict(color="#6f7f98", dark="#46526a", cuff="#f6f2ea", len=0.84, w=0.165),
        shorts=dict(color="#3a3a4a", dark="#242430", cuff="#3a3a4a", len=0.90, w=0.13),
        boots=dict(color="#1a161c", cuff="#1a161c", h=0.07, toe=0.15),
        colors=dict(base="#6f7f98", dark="#3e485e", lapel="#56647c", vest="#b8322a", vest_b="#e8dcb0", shirt="#fbfaf6", collar="#ffffff",
                    tie="#1f4a8a", tie_dark="#12305a", button="#2a2228", pants="#3a3a4a"),
    ),
    # passenger: cloche hat, teal coat with a tan collar, red handbag
    "pass_woman": dict(
        _FLAGS, build="slim", seed=61.8,
        torso_w=0.58, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.225, 0.52), arm=0.72, hip_x=0.13, leg=1.16, stance=0.04, wide=0.22, limb_w=0.054,
        eye_y=0.050, brow="stroke", brow_th=0.030, mouth="smile", moustache=False, smirk_side=-1, lashes=True, cheeks="#f4989a",
        hat="newsboy", hat_style="cloche22", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(light="#f0584a", base="#d02a22", dark="#8a1612", band="#f6d84a", flower="#ffffff"),
        hair=dict(color="#8a4a2a", front=0.10, grow=0.20),
        costume="woman22", coat=True, hem_frac=0.62, skirt_flare=0.24,
        sleeve=dict(color="#1f9393", dark="#0c5f66", cuff="#c88a4a", len=0.84, w=0.150),
        boots=dict(color="#2a1a16", cuff="#2a1a16", h=0.05, toe=0.12),
        colors=dict(base="#fbf3e0", blouse="#fbf3e0", cardigan="#1f9393", collar="#fbf3e0", collar_c="#c88a4a", bow="#d8261e", button="#f6d84a", trim="#0c5f66",
                    belt="#0c5f66", pants="#1f9393"),
    ),
    # passenger child: school cap, red school jumper, grey shorts and knee socks
    "pass_child": dict(
        _FLAGS, build="boy", seed=70.4,
        torso_w=0.62, torso_h=0.78, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.80, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f4989a", freckles=True,
        hat="newsboy", hat_style="schoolcap22", hat_tilt=-6.0, ear_pencil=False,
        hat_colors=dict(light="#2fb066", base="#1c8a4a", dark="#0e5a2c", band="#0e5a2c", piping="#f5c400"),
        hair=dict(color="#c87a3a", front=0.08, grow=0.16),
        costume="vest22", neck="tie", vest_style="knit", vest_v=0.34, socks22=dict(color="#e8e4d4", band="#1c8a4a"),
        sleeve=dict(color="#d8301e", dark="#8a1a10", cuff="#f5c400", len=0.62, w=0.140),
        shorts=dict(color="#7a8498", dark="#4e566a", cuff="#7a8498", len=0.55, w=0.13),
        boots=dict(color="#2a1c14", cuff="#2a1c14", h=0.10, toe=0.13, soft=True),
        colors=dict(base="#d8301e", shirt="#ffffff", collar="#ffffff", vest="#d8301e", vest_d="#8a1a10", trim="#f5c400", trim2="#1c8a4a",
                    tie="#1c8a4a", tie_dark="#0e5a2c", tie_stripe="#f5c400", pants="#7a8498"),
    ),
    # the old gentleman: white beard, a monocle, white wisps, a bottle-green frock coat with a gold waistcoat; squints
    "old_gent": dict(
        _FLAGS, build="regular", seed=83.5,
        torso_w=0.80, torso_h=0.98, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.31, 0.47), arm=0.72, hip_x=0.15, leg=1.16, stance=0.05, wide=0.24, limb_w=0.058,
        eye_y=0.020, brow="stroke", brow_th=0.056, mouth="frown", moustache=False, smirk_side=1, age_lines=True, monocle=True, cheeks="#e8a090",
        beard=dict(color="#f4f2f0", dark="#c4c0c8"),
        hat="newsboy", hat_style="hair22", hat_tilt=0.0, ear_pencil=False,
        hair22=dict(style="white", color="#f4f2f0"),
        hair=dict(color="#f4f2f0", front=0.03, grow=0.12),
        costume="frock7", coat_len=0.46, coat_flare=0.10, neck="cravat", chain=True, vest_buttons=5, double=False,
        sleeve=dict(color="#2c6a4e", dark="#17402e", cuff="#f6f2ea", len=0.84, w=0.150),
        shorts=dict(color="#5a4a62", dark="#3a2e42", cuff="#5a4a62", len=0.90, w=0.12),
        boots=dict(color="#1a161c", cuff="#1a161c", h=0.07, toe=0.15),
        colors=dict(base="#2c6a4e", dark="#17402e", lapel="#1f5440", vest="#d8a030", vest_b="#7a4a12", shirt="#fbfaf6", collar="#ffffff",
                    tie="#b8322a", tie_dark="#7a1c14", button="#e2b442", pants="#5a4a62"),
    ),
    # Underground porter: navy tunic with the red-blue badge, peaked cap with the roundel, moustache
    "porter": dict(
        _FLAGS, build="regular", seed=92.1,
        torso_w=0.88, torso_h=1.02, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.32, 0.48), arm=0.74, hip_x=0.16, leg=1.22, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.020, brow="stroke", brow_th=0.058, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=-1, cheeks="#e88a78",
        hat="newsboy", hat_style="porter22", hat_tilt=-3.0, ear_pencil=False, braid=False,
        hat_colors=dict(crown="#2a3f9a", crown_l="#4a64c8", crown_d="#16215a", band="#16215a", visor="#16141a", visor_l="#4a4652",
                        badge="#c8a04a", badge_c="#2a2a30"),
        hair=dict(color="#3a2a22", front=0.05, grow=0.18),
        costume="porter22", double=True, tunic_len=0.20,
        sleeve=dict(color="#2a3f9a", dark="#16215a", cuff="#f5c400", len=0.82, w=0.170),
        shorts=dict(color="#1c2a66", dark="#101a44", cuff="#1c2a66", len=0.90, w=0.14),
        boots=dict(color="#16141a", cuff="#16141a", h=0.08, toe=0.15),
        colors=dict(base="#2a3f9a", dark="#16215a", pocket="#324aa8", button="#f2c230", belt="#1a1218", patch="#d8261e", pants="#1c2a66",
                    moustache="#3a2a22"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast22.py canvas): every arm preset with the
# film-22 props at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects, every STORY22 pose without a set piece
# (board / desk / typewriter / pillar) and the cycles; >= 0.32 D head room.  Crowd variants share their base member's canvas.
CANVAS22 = {
    "beck": (-2.0000, -4.8125, 2.0000, 0.1250),
    "official": (-2.1875, -5.0625, 2.1875, 0.1250),
    "clerk_a": (-2.0625, -4.8750, 2.0625, 0.1250),
    "clerk_b": (-2.0625, -4.6250, 2.0625, 0.1875),
    "clerk_c": (-2.1875, -4.5000, 2.1875, 0.1250),
    "pass_man": (-2.1250, -4.7500, 2.1250, 0.1250),
    "pass_woman": (-2.0625, -4.6250, 2.0625, 0.1250),
    "pass_child": (-1.9375, -3.9375, 1.9375, 0.3750),
    "old_gent": (-2.1250, -4.5625, 2.1250, 0.1250),
    "porter": (-2.1250, -4.6875, 2.1250, 0.1250),
}

STORY22, STORY22_META = {}, {}

SQ = dict(type="set_square", scale=0.95)


def _hand_to(cast, pose, key, target, it=4, anchor=None):
    """move arm_<key>'s hand target so the anchor (default the hand) lands on target (local D)."""
    for _ in range(it):
        an = figure(cast, pose, "q")["anchors"]
        cur = an[anchor or ("hand_" + key)]
        h = pose["arm_" + key]["hand"]
        pose["arm_" + key]["hand"] = (h[0] + target[0] - cur[0], h[1] + target[1] - cur[1])


def _crowd_walk(cast, phase, props=None, **kw):
    base = dict(expr="neutral")
    base.update(kw)
    return cycle(cast, phase, "walk", base=base, arms=props or "both")


def _story():
    S, M = {}, {}
    B, O = "beck", "official"
    # ------------------------------------------------------------------ Beck
    S["beck_rule_line"] = (B, dict(yaw=0.55, pitch=0.30, expr="determined", lean=14, head_roll=-4, gaze=(0.9, 0.6), board=1, board_x=-0.05, board_y=0.62, t=0.3,
                                   arm_l=dict(hand=(0.95, 0.88), bend=0.2, stretch=1.2, layer="front"), prop_l=dict(type="ruler", angle=-8),
                                   arm_r=dict(hand=(1.10, 0.66), bend=-0.2, stretch=1.2, layer="front"), prop_r=dict(type="pen", angle=62, scale=1.4),
                                   legs=dict(preset="step", stride=0.25)))
    M["beck_rule_line"] = dict(note="leaning in over the drafting board (pose board=1 draws it, board_x / board_y / board_s place it): ruler laid on the board "
                                    "in the far hand, fountain pen drawing a line along its edge; anchor pen_r = nib")
    S["beck_set_square"] = (B, dict(yaw=0.40, pitch=-0.10, expr="determined", head_roll=-3, gaze=(0.8, -0.4),
                                    arm_r=dict(hand=(0.72, 0.52), bend=-0.4, stretch=1.15, layer="front"), prop_r=dict(SQ, angle=-8),
                                    arm_l=dict(hand=(-0.40, 0.98), bend=0.4), legs="stand"))
    M["beck_set_square"] = dict(note="holds the 45 degree set square up beside his face and checks the angle")
    S["beck_hold_circuit"] = (B, dict(yaw=0.50, pitch=0.12, expr="determined", head_roll=-3, gaze=(0.9, 0.0),
                                      arm_r=dict(hand=(0.46, 0.60), bend=-0.3, stretch=1.15, layer="front"), prop_r=dict(type="circuit", angle=-6),
                                      arm_l="down", legs="stand"))
    M["beck_hold_circuit"] = dict(note="holds a circuit-diagram sheet beside him and studies it (the idea: the Tube is a circuit)")
    S["beck_thumb_push"] = (B, dict(yaw=0.55, pitch=0.28, expr="determined", lean=12, gaze=(0.9, 0.7), board=1, board_x=0.15, board_y=0.62,
                                    arm_r=dict(hand=(1.02, 0.86), bend=0.0, stretch=1.2, shape="open", layer="front"),
                                    arm_l=dict(hand=(0.55, 1.10), bend=0.5, stretch=1.1, layer="front"), prop_l=dict(type="pen", angle=-20),
                                    legs=dict(preset="step", stride=0.20)))
    M["beck_thumb_push"] = dict(note="pushes a station point along the board with his thumb (open hand pressed on the board), pen in the other hand")
    S["beck_carry_roll"] = (B, cycle(B, 0.30, "walk", base=dict(expr="neutral", pitch=0.05, prop_r=dict(type="roll", angle=-22)), arms="l"))
    S["beck_carry_roll"][1]["arm_r"] = dict(hand=(0.32, 0.92), bend=0.5, stretch=1.0, layer="front")
    M["beck_carry_roll"] = dict(note="one frame of the walk with the rolled drawing under his arm; animate cast22.walk_carry_roll(phase)")
    S["beck_present_roll"] = (B, dict(yaw=0.55, pitch=-0.10, expr="happy", mouth="smile", head_roll=-3, gaze=(0.9, 0.2), lean=6,
                                      arm_r=dict(hand=(1.10, 0.98), bend=0.4, stretch=1.2, layer="front"), prop_r=dict(type="roll", angle=2),
                                      arm_l=dict(hand=(0.66, 1.02), bend=0.5, stretch=1.2, layer="front"), legs=dict(preset="step", stride=0.2), desk=1, desk_x=1.45, desk_w=1.7, desk_y=1.24))
    M["beck_present_roll"] = dict(note="lays the roll on the desk, hopeful: both hands on the roll, eyebrows up, small hopeful smile")
    S["beck_sag"] = (B, cycle(B, 0.30, "walk", base=dict(expr="sad", pitch=0.9, head_dy=0.10, lean=8, yaw=0.6, prop_r=dict(type="roll", angle=70)), arms="l"))
    S["beck_sag"][1]["arm_r"] = dict(hand=(0.24, 1.22), bend=0.3, stretch=1.0, layer="front")
    M["beck_sag"] = dict(note="shoulders down, head low, walking away with the roll hanging from his hand; animate walk_sag(phase)")
    S["beck_knock"] = (B, dict(yaw=0.60, pitch=-0.05, expr="worried", head_roll=-3, gaze=(1.0, 0.0), lean=5,
                               arm_r=dict(hand=(0.92, 0.46), bend=-0.3, stretch=1.2, shape="ball", layer="front"),
                               arm_l=dict(hand=(0.10, 1.00), bend=0.5, layer="front"), prop_l=dict(type="roll", angle=-10), legs=dict(preset="step", stride=0.2)))
    M["beck_knock"] = dict(note="knocks on a door (screen-right) with his fist, the roll under the other arm; animate arm_r hand x 0.92 <-> 0.80")
    S["beck_read_notice"] = (B, dict(yaw=0.15, pitch=0.55, expr="sad", mouth="o", head_roll=-2, gaze=(0.0, 0.9), lean=2,
                                     arm_l=dict(hand=(-0.20, 0.92), bend=0.4, stretch=1.0, layer="front"), prop_l=dict(type="letter", angle=0, scale=1.0),
                                     arm_r=dict(hand=(0.34, 0.96), bend=0.4, stretch=1.0, layer="front"), legs="stand"))
    M["beck_read_notice"] = dict(note="reads the NOTICE letter (laid off), a sigh: letter in both hands at chest height, head bowed (mouth o = the sigh)")
    S["beck_proud"] = (B, dict(yaw=0.20, pitch=-0.25, expr="happy", mouth="smile", head_roll=4, gaze=(0.5, -0.1),
                               arm_r=dict(hand=(-0.16, 0.80), bend=0.7, layer="front"), arm_l=dict(hand=(0.18, 0.76), bend=0.7, layer="front"), legs="stand"))
    M["beck_proud"] = dict(note="the ending: arms folded, chin up, small proud smile")
    # ------------------------------------------------------------------ the official
    S["off_sit_glance"] = (O, dict(yaw=0.35, pitch=0.12, expr="smug", mouth="flat", head_roll=-4, gaze=(0.9, 0.7),
                                   arm_r=dict(hand=(0.85, 1.22), bend=0.3, stretch=1.1, layer="front"), prop_r=dict(type="sheet", angle=-4, scale=0.8),
                                   arm_l="akimbo", legs=dict(preset="crouch", crouch=0.60), desk=1, desk_x=0.15, desk_w=2.3, desk_y=1.36))
    M["off_sit_glance"] = dict(note="at his desk (pose desk=1 draws a desk in front; desk_x / desk_y / desk_w place it; legs bent behind it), glancing down at the sheet with a smug half-smile")
    S["off_stamp"] = (O, dict(yaw=0.30, pitch=-0.35, expr="smug", mouth="smile", head_roll=4, gaze=(0.6, -0.3), lean=-3,
                              arm_r=dict(hand=(0.80, -0.30), bend=-0.5, stretch=1.3, layer="top"), prop_r=dict(type="stamp", angle=92, scale=1.7),
                              arm_l="akimbo", legs="wide"))
    M["off_stamp"] = dict(note="the red rubber stamp raised high, about to come down: REJECTED; anchor stamp_r = the stamping face")
    S["off_laugh_back"] = (O, dict(yaw=0.20, pitch=-0.90, expr="laughing", mouth="talk_b", fx=["tears"], flush=1.0, head_roll=-10, lean=-10, t=0.3, squash=(1.02, 0.98),
                                   arm_r=dict(hand=(0.50, 1.06), bend=0.9, shape="open"), arm_l=dict(hand=(-0.52, 1.04), bend=0.9, shape="open"), legs="wide"))
    M["off_laugh_back"] = dict(lipsync=True, note="rocking back, laughing, the face goes red (flush 0..1): talking pose, mouth = talk_mouth(g) inside the quote, talk_b held otherwise")
    S["off_wave_sheet"] = (O, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_a", head_roll=6, lean=-4,
                                   arm_r=dict(hand=(0.80, 0.30), bend=-0.4, stretch=1.2, layer="top"), prop_r=dict(type="sheet", angle=-38, scale=0.95),
                                   arm_l="akimbo", legs="wide"))
    M["off_wave_sheet"] = dict(lipsync=True, note="waves the diagram sheet like a flag while he talks; animate prop angle -38 <-> -18; LIP-SYNC")
    S["off_eat_mime"] = (O, dict(yaw=0.35, pitch=-0.10, expr="smug", mouth="talk_b", head_roll=-3, gaze=(0.8, 0.0),
                                 arm_r=dict(hand=(0.30, 0.40), bend=-0.5, stretch=1.2, layer="top"), prop_r=dict(type="sheet", angle=-14, scale=0.80),
                                 arm_l="akimbo", legs="wide"))
    M["off_eat_mime"] = dict(lipsync=True, note="'I will eat it, the whole sheet!': holds the sheet to his open mouth as if biting; LIP-SYNC")
    S["off_toss_drawer"] = (O, dict(yaw=0.40, pitch=-0.15, expr="smug", mouth="flat", head_roll=3, gaze=(0.9, 0.5),
                                    arm_r=dict(hand=(0.98, 0.98), bend=0.2, stretch=1.25, shape="open", layer="front"), prop_r=dict(type="sheet", angle=34, scale=0.75),
                                    arm_l="akimbo", legs="wide", lean=4, desk=1, desk_x=1.35, desk_w=1.5, desk_y=1.48, desk_drawer=1))
    M["off_toss_drawer"] = dict(note="flicks the sheet into the drawer (screen-right, low): sheet tipped 40 degrees as it leaves the fingers")
    S["off_smug_rub"] = (O, dict(yaw=0.25, pitch=-0.40, expr="smug", mouth="talk_a", head_roll=5,
                                 arm_r=dict(hand=(0.06, 0.96), bend=0.8, shape="open", layer="front"), arm_l=dict(hand=(-0.14, 0.98), bend=0.8, shape="open", layer="front"),
                                 legs="wide"))
    M["off_smug_rub"] = dict(lipsync=True, note="rubbing his hands, smug: 'Watch the whole city get lost!'; animate the hands +-0.05 in x; LIP-SYNC")
    S["off_peek"] = (O, dict(yaw=0.55, pitch=-0.10, expr="smirk", mouth="flat", head_roll=8, head_dx=0.10, gaze=(0.9, 0.2), pillar=1, pillar_x=-0.22, pillar_w=0.9,
                             arm_r="down", arm_l=dict(hand=(-0.55, 0.95), bend=0.2), legs="stand"))
    M["off_peek"] = dict(note="peeks out from behind a pillar (pose pillar=1: drawn IN FRONT of the figure on the screen-left side; pillar_x = the pillar's "
                              "edge, pillar_w) to spy on the map test; mirror=True for the other side")
    S["off_jaw_drop"] = (O, dict(yaw=0.30, pitch=0.10, expr="shocked", mouth=("open", 0.18, 0.20), fx=["sweat"], sweat=1.0, head_dy=0.03, gaze=(0.8, 0.0),
                                 arm_r=dict(hand=(0.66, 1.04), bend=0.3, shape="open"), arm_l=dict(hand=(-0.66, 1.04), bend=0.3, shape="open"), legs="stand", squash=(1.01, 0.99)))
    M["off_jaw_drop"] = dict(note="shock: jaw dropped, eyes wide, sweat, hands open at his sides (held mouth, not lip-sync)")
    S["off_buried_eat"] = (O, dict(yaw=0.30, pitch=0.10, expr="worried", mouth="flat", puff=1.0, sweat=1.0, napkin=1, fork_map=1, head_roll=3, gaze=(0.7, 0.4),
                                   arm_r=dict(hand=(0.82, 0.80), bend=-0.2, stretch=1.2, layer="top"), prop_r=dict(type="fork", angle=-46, scale=1.5),
                                   arm_l=dict(hand=(-0.84, 0.86), bend=-0.2, stretch=1.2, layer="front"), prop_l=dict(type="knife", angle=-134, scale=1.5), legs="wide"))
    M["off_buried_eat"] = dict(note="the ending: napkin in his collar, knife and fork, a folded map speared on the fork, cheeks puffed (puff 0..1), sweating, "
                                    "mouth shut (towers of maps get piled behind him in the set)")
    S["off_sneer"] = (O, dict(yaw=0.30, pitch=-0.50, expr="unimpressed", mouth="smirk", head_roll=6, arm_r=dict(hand=(-0.30, 0.92), bend=0.8, layer="front"),
                              arm_l=dict(hand=(0.30, 0.90), bend=0.8, layer="front"), legs="wide"))
    M["off_sneer"] = dict(note="sneering at the diagram: arms folded, nose up")
    S["off_sulk"] = (O, dict(yaw=0.30, pitch=0.70, expr="sad", mouth="frown", head_dy=0.06, lean=6, flush=0.25, gaze=(0.0, 0.8),
                             arm_r=dict(hand=(0.60, 1.10), bend=0.3), arm_l=dict(hand=(-0.60, 1.10), bend=0.3), legs="stand"))
    M["off_sulk"] = dict(note="sulky defeat: head low, pouting, arms hanging")
    S["off_walk"] = (O, cycle(O, 0.30, "walk", base=dict(expr="smug", pitch=-0.3)))
    # ------------------------------------------------------------------ the clerks
    for c, sfx in (("clerk_a", "_a"), ("clerk_b", "_b"), ("clerk_c", "_c")):
        S["clerk_type" + sfx] = (c, dict(yaw=0.45, pitch=0.25, expr="neutral", mouth="flat", head_roll=-2, gaze=(0.8, 0.8), typewriter=1, tw_x=0.55, tw_y=1.20, desk=1, desk_x=0.35, desk_y=1.42,
                                         arm_r=dict(hand=(0.62, 1.00), bend=0.3, stretch=1.1, layer="front"), arm_l=dict(hand=(0.30, 1.02), bend=0.3, stretch=1.1, layer="front"),
                                         legs=dict(preset="crouch", crouch=0.35)))
        S["clerk_laugh_point" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                                arm_r=dict(hand=(0.80, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
        S["clerk_laugh_belly" + sfx] = (c, dict(yaw=0.15, pitch=0.25, expr="laughing", blink=2, fx=["tears"], head_roll=-8, lean=10, t=0.6,
                                                arm_r=dict(hand=(0.24, 0.98), bend=0.9, shape="open", layer="front"), arm_l=dict(hand=(-0.26, 0.94), bend=0.9, shape="open", layer="front"),
                                                legs=dict(preset="crouch", crouch=0.06, spread=-0.04) if c == "clerk_b" else dict(preset="crouch", crouch=0.15, spread=0.10)))
        S["clerk_sit" + sfx] = (c, dict(yaw=0.35, pitch=0.05, expr="smug", mouth="flat", head_roll=-4, gaze=(0.6, 0.3),
                                        arm_r="chin", arm_l=dict(hand=(0.45, 1.02), bend=0.3, stretch=1.1, layer="front"), legs=dict(preset="crouch", crouch=0.35), desk=1, desk_x=0.35, desk_y=1.42))
    M["clerk_type"] = dict(note="typing (typewriter=1 draws the machine behind the hands; tw_x / tw_y place it): clerk_a, _b, _c. Seated: legs bent for the desk")
    M["clerk_laugh_point"] = dict(note="laughing and pointing at Beck (screen-right; mirror=True for left): clerk_a, _b, _c")
    M["clerk_laugh_belly"] = dict(note="doubled over, holding the belly, eyes shut: clerk_a, _b, _c")
    M["clerk_sit"] = dict(note="seated, chin on hand, bored: clerk_a, _b, _c")
    # ------------------------------------------------------------------ passengers
    M_, W_, C_, G_ = "pass_man", "pass_woman", "pass_child", "old_gent"
    S["pass_walk_man"] = (M_, cycle(M_, 0.30, "walk", base=dict(expr="neutral", prop_r=dict(type="briefcase", scale=1.0)), arms="l"))
    S["pass_walk_man"][1]["arm_r"] = dict(hand=(0.40, 1.10), bend=0.4, stretch=1.0, layer="front")
    S["pass_walk_woman"] = (W_, cycle(W_, 0.30, "walk", base=dict(expr="happy", mouth="smile", prop_r=dict(type="handbag", scale=1.0)), arms="l"))
    S["pass_walk_woman"][1]["arm_r"] = dict(hand=(0.36, 1.08), bend=0.4, stretch=1.0, layer="front")
    S["pass_walk_child"] = (C_, cycle(C_, 0.30, "walk", base=dict(expr="happy", mouth="smile")))
    M["pass_walk_man"] = dict(note="walk-cycle frame, briefcase in the hand (cast22.walk(cast, phase) animates); the crowd: crowd_member(i, 'pass_walk')")
    S["pass_squint"] = (M_, dict(yaw=0.85, pitch=0.05, expr="squint", mouth="flat", lean=14, head_dx=0.06, gaze=(1.0, 0.0),
                                 arm_r=dict(hand=(-0.10, 1.02), bend=0.4, layer="back"), arm_l=dict(hand=(-0.30, 0.98), bend=0.4, layer="back"), legs=dict(preset="step", stride=0.15)))
    M["pass_squint"] = dict(note="nose almost on the wall map (screen-right), squinting, hands behind his back, leaning in")
    S["old_squint"] = (G_, dict(yaw=0.85, pitch=0.10, expr="squint", mouth="frown", lean=12, head_dx=0.06, gaze=(1.0, 0.0),
                                arm_r=dict(hand=(0.78, 0.50), bend=-0.4, stretch=1.15, layer="top"), prop_r=dict(type="magnifier", angle=-14),
                                arm_l=dict(hand=(-0.30, 0.98), bend=0.4, layer="back"), legs=dict(preset="step", stride=0.12)))
    M["old_squint"] = dict(note="the old gentleman peers at the old map through a magnifying glass, monocle and all (screen-right)")
    S["pass_unfold_map"] = (W_, dict(yaw=0.30, pitch=0.15, expr="happy", mouth="grin", head_roll=-3, gaze=(0.3, 0.8),
                                     arm_r=dict(hand=(0.62, 0.96), bend=0.3, stretch=1.1, layer="front"), prop_r=dict(type="pocketmap_open", angle=0),
                                     arm_l=dict(hand=(-0.20, 0.98), bend=0.3, stretch=1.1, layer="front"), prop_l=dict(type="pocketmap", angle=0), legs="stand"))
    M["pass_unfold_map"] = dict(note="unfolds the pocket map with both hands (open map in one, the cover half in the other)")
    S["pass_read_map"] = (M_, dict(yaw=0.40, pitch=0.30, expr="determined", head_roll=-3, gaze=(0.6, 0.9),
                                   arm_r=dict(hand=(0.46, 0.80), bend=-0.2, stretch=1.1, layer="front"), prop_r=dict(type="pocketmap_open", angle=-6),
                                   arm_l=dict(hand=(0.10, 1.04), bend=0.5, layer="front"), prop_l=dict(type="briefcase"), legs="stand"))
    M["pass_read_map"] = dict(note="reads the open pocket map held up in front of his chest, briefcase in the other hand")
    S["pass_tap_map"] = (W_, dict(yaw=0.30, pitch=0.30, expr="happy", mouth="smile", head_roll=-3, gaze=(0.5, 0.9),
                                  arm_l=dict(hand=(-0.34, 0.74), bend=0.3, stretch=1.1, layer="front"), prop_l=dict(type="pocketmap_open", angle=0, scale=1.3),
                                  arm_r=dict(hand=(0.14, 0.92), shape="point", bend=0.2, stretch=1.1, layer="top"), legs="stand"))
    M["pass_tap_map"] = dict(note="taps a station on the map with her index finger (the map in the other hand): 'red line, change here, get off there'")
    S["pass_read_paper"] = (M_, dict(yaw=0.30, pitch=0.30, expr="neutral", mouth="flat", head_roll=-2, gaze=(0.4, 0.9),
                                     arm_l=dict(hand=(-0.40, 0.88), bend=0.3, stretch=1.1, layer="front"), prop_l=dict(type="daily", angle=0, scale=1.45),
                                     arm_r=dict(hand=(0.44, 0.90), bend=0.3, stretch=1.1, layer="front"), legs="stand"))
    M["pass_read_paper"] = dict(note="reads the daily newspaper held up in both hands (1.45x, in both hands at chest height)")
    S["pass_point"] = (M_, dict(yaw=0.45, pitch=-0.15, expr="excited", head_roll=4, gaze=(1.0, -0.1),
                                arm_r=dict(hand=(1.08, 0.10), shape="point", bend=-0.5, stretch=1.3), arm_l=dict(hand=(-0.10, 0.92), bend=0.6, layer="front"),
                                prop_l=dict(type="pocketmap"), legs=dict(preset="step", stride=0.25)))
    M["pass_point"] = dict(note="points the way (screen-right) with the folded map in the other hand: 'this way!'")
    S["pass_smile_board"] = (C_, dict(yaw=0.60, pitch=-0.25, expr="happy", mouth="smile", head_roll=-4, gaze=(1.0, -0.1),
                                      arm_r=dict(hand=(0.45, 0.98), bend=0.4, layer="front"), prop_r=dict(type="pocketmap"), arm_l=dict(hand=(-0.50, 0.90), bend=0.6),
                                      legs=dict(preset="step", stride=0.60)))
    M["pass_smile_board"] = dict(note="a confident step toward the train, smiling, the map in his fist (child)")
    S["pass_smile_board_woman"] = (W_, dict(yaw=0.60, pitch=-0.25, expr="happy", mouth="smile", head_roll=-4, gaze=(1.0, -0.1),
                                            arm_r=dict(hand=(0.40, 1.00), bend=0.4, layer="front"), prop_r=dict(type="pocketmap"), arm_l=dict(hand=(-0.40, 0.95), bend=0.5),
                                            legs=dict(preset="step", stride=0.60)))
    S["pass_bump"] = (M_, dict(yaw=0.30, pitch=-0.10, expr="shocked", mouth="o", head_roll=-16, lean=14, gaze=(-0.8, 0.0), squash=(0.98, 1.03),
                               arm_r=dict(hand=(0.92, 0.30), bend=-0.6, stretch=1.3, shape="open", layer="front"), arm_l=dict(hand=(-0.86, 0.62), bend=-0.5, stretch=1.3, shape="open"),
                               prop_l=dict(type="briefcase"), legs=dict(preset="step", stride=-0.5)))
    M["pass_bump"] = dict(note="bumped from the left: stumbling, bowler askew (head_roll -16 tilts the hat with the head), arms flung out, briefcase swinging")
    # ------------------------------------------------------------------ the porter
    P_ = "porter"
    S["porter_hand_map"] = (P_, dict(yaw=0.55, pitch=-0.10, expr="happy", mouth="smile", head_roll=-3, gaze=(1.0, 0.0),
                                     arm_r=dict(hand=(0.98, 0.58), bend=-0.3, stretch=1.25, shape="open", layer="front"), prop_r=dict(type="pocketmap", angle=-4),
                                     arm_l=dict(hand=(-0.20, 0.96), bend=0.5, layer="front"), prop_l=dict(type="pocketmap_open", angle=-8, scale=0.8), legs="stand"))
    M["porter_hand_map"] = dict(note="hands a folded pocket map to a passenger (screen-right), a spare open map in the other hand")
    pp = dict(yaw=0.55, pitch=0.05, expr="determined", lean=10, head_roll=-2, gaze=(1.0, 0.2), arm_r=dict(hand=(0.66, 1.08), bend=0.2, stretch=1.15, layer="front"),
              prop_r=dict(type="handtruck", scale=1.0), arm_l=dict(hand=(0.20, 1.16), bend=0.4, stretch=1.1, layer="front"), legs=dict(preset="step", stride=0.3))
    an = figure(P_, pp, "q")
    hy = an["anchors"]["hand_r"][1]
    pp["prop_r"] = dict(type="handtruck", scale=_clamp((an["feet_y"] - hy) / 1.30, 0.6, 1.4))
    S["porter_push_crate"] = (P_, pp)
    M["porter_push_crate"] = dict(note="pushes a crate of MAPS on a sack truck (screen-right): prop scale makes the wheel touch the floor; leaning into it")
    S["porter_walk"] = (P_, cycle(P_, 0.30, "walk", base=dict(expr="neutral")))
    for n in ("off_walk", "porter_walk"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast22.cycle()"))
    return S, M


def pose_for(name, cast=None):
    """(cast, pose) for a generic brief name: pose_for("clerk_type", "clerk_b") -> STORY22["clerk_type_b"]; "pass_walk" -> the man
    (or cast "pass_woman" / "pass_child"); "clerk_*" without a cast -> clerk_a.  Full names (STORY22 keys) pass straight through."""
    if name in STORY22 and cast is None:
        return STORY22[name]
    if name.startswith("clerk_"):
        sfx = {"clerk_a": "_a", "clerk_b": "_b", "clerk_c": "_c", None: "_a"}[cast]
        return STORY22[name + sfx]
    if name in ("pass_walk", "pass_smile_board"):
        sfx = {"pass_man": "_man", "pass_woman": "_woman", "pass_child": "_child", None: "_man"}[cast]
        key = name + sfx
        return STORY22[key if key in STORY22 else name]
    return STORY22[name]


def walk(cast, phase, **kw):
    """walk cycle frame for any member with the member's own props (briefcase, handbag, roll) as in its pass_walk_* / beck_carry_roll pose."""
    if cast == "beck":
        p = cycle(cast, phase, "walk", base=dict(expr="neutral", pitch=0.05, prop_r=dict(type="roll", angle=-22), **kw), arms="l")
        p["arm_r"] = dict(hand=(0.32, 0.92), bend=0.5, stretch=1.0, layer="front")
        return p
    prop = {"pass_man": dict(type="briefcase"), "pass_woman": dict(type="handbag")}.get(cast)
    if prop:
        p = cycle(cast, phase, "walk", base=dict(expr="neutral", prop_r=prop, **kw), arms="l")
        p["arm_r"] = dict(hand=(0.40, 1.10), bend=0.4, stretch=1.0, layer="front")
        return p
    return cycle(cast, phase, "walk", base=dict(expr="neutral", **kw))


def walk_carry_roll(phase):
    return walk("beck", phase)


def walk_sag(phase):
    p = cycle("beck", phase, "walk", base=dict(expr="sad", pitch=0.9, head_dy=0.10, lean=8, yaw=0.6, prop_r=dict(type="roll", angle=70)), arms="l")
    p["arm_r"] = dict(hand=(0.24, 1.22), bend=0.3, stretch=1.0, layer="front")
    return p


# ============================================================================= crowd
def _fed(base, band):
    return dict(light=P._shade(base, 1.25), base=base, dark=P._shade(base, 0.62), shine=P._shade(base, 1.6), band=band, band_l=P._shade(band, 1.4),
                brim=P._shade(base, 0.9), edge=P._shade(base, 1.3))


def _bow(base, band="#8a1f2d"):
    return dict(light=P._shade(base, 1.7), base=base, dark=P._shade(base, 0.5), shine=P._shade(base, 2.4), band=band, brim=P._shade(base, 0.8), edge=P._shade(base, 1.9))


def _men_variant(coat, lapel, vest, hat, tie, hair):
    """(overrides) for a crowd man built on pass_man."""
    d = dict(sleeve=dict(color=coat, dark=P._shade(coat, 0.62), cuff="#f6f2ea", len=0.84, w=0.165), hair=dict(color=hair, front=0.06, grow=0.20),
             colors=dict(base=coat, dark=P._shade(coat, 0.6), lapel=lapel, vest=vest, vest_b="#e8dcb0", shirt="#fbfaf6", collar="#ffffff", tie=tie,
                         tie_dark=P._shade(tie, 0.6), button="#2a2228", pants="#3a3a4a"))
    d.update(hat)
    return d


def _women_variant(coat, hatc, band, hair, collar):
    return dict(hat_colors=dict(light=P._shade(hatc, 1.3), base=hatc, dark=P._shade(hatc, 0.6), band=band, flower="#ffffff"),
                hair=dict(color=hair, front=0.10, grow=0.20),
                sleeve=dict(color=coat, dark=P._shade(coat, 0.6), cuff=collar, len=0.84, w=0.150),
                colors=dict(base="#fbf3e0", blouse="#fbf3e0", cardigan=coat, collar="#fbf3e0", collar_c=collar, bow="#d8261e", button="#f6d84a",
                            trim=P._shade(coat, 0.6), belt=P._shade(coat, 0.6), pants=coat))


def _kid_variant(jumper, cap, piping, hair, sock):
    return dict(hat_colors=dict(light=P._shade(cap, 1.35), base=cap, dark=P._shade(cap, 0.6), band=P._shade(cap, 0.6), piping=piping),
                hair=dict(color=hair, front=0.08, grow=0.16), socks22=dict(color=sock, band=cap),
                sleeve=dict(color=jumper, dark=P._shade(jumper, 0.6), cuff=piping, len=0.62, w=0.140),
                colors=dict(base=jumper, shirt="#ffffff", collar="#ffffff", vest=jumper, vest_d=P._shade(jumper, 0.6), trim=piping, trim2=cap,
                            tie=cap, tie_dark=P._shade(cap, 0.6), tie_stripe=piping, pants="#7a8498"))


_FED = dict(hat_style="fedora", hat_tilt=-3.0)
_BOWL = dict(hat_style="bowler22", hat_tilt=-4.0)
CROWD_SPEC = (
    ("pass_man", _men_variant("#2f6a4a", "#1f4a34", "#d8a020", dict(_BOWL, hat_colors=_bow("#26222c")), "#8a1f2d", "#2a1c16")),
    ("pass_woman", _women_variant("#d02a22", "#1f9393", "#f6d84a", "#3a2418", "#c88a4a")),
    ("pass_man", _men_variant("#b8802a", "#8a5a18", "#2a4a8a", dict(_FED, hat_colors=_fed("#b8854c", "#3b2a22")), "#2a4a8a", "#6a4a2a")),
    ("pass_woman", _women_variant("#e0a020", "#1c8a4a", "#d8261e", "#8a4a2a", "#fbf3e0")),
    ("pass_child", _kid_variant("#2a5ec8", "#d8261e", "#f5c400", "#c87a3a", "#e8e4d4")),
    ("pass_man", _men_variant("#3a4a78", "#26335a", "#c8302a", dict(_BOWL, hat_colors=_bow("#6a4228", "#2a1c16")), "#f5c400", "#1a1a1a")),
    ("pass_woman", _women_variant("#1f7a4a", "#e0a020", "#8a1f2d", "#1a1a1a", "#d8a030")),
    ("pass_man", _men_variant("#8a2a3a", "#5a1824", "#e8dcb0", dict(_BOWL, hat_colors=_bow("#16141a", "#e0a020")), "#1f4a8a", "#8a5a30")),
    ("pass_woman", _women_variant("#7a2a8a", "#e8d8b0", "#7a2a8a", "#c8a050", "#e8c870")),
    ("pass_man", _men_variant("#1f7a88", "#0e4a58", "#e0a020", dict(_FED, hat_colors=_fed("#6a7080", "#16141a")), "#d8261e", "#3a2a1a")),
    ("pass_woman", _women_variant("#2a4a9a", "#d02a22", "#f6d84a", "#5a2a1a", "#e8e4d4")),
    ("pass_child", _kid_variant("#e0a020", "#2a4a9a", "#d8261e", "#4a2a1a", "#d8d4c4")),
    ("pass_woman", _women_variant("#c8302a", "#f6d84a", "#1f9393", "#8a2a1a", "#fbf3e0")),
    ("pass_man", _men_variant("#6f7f98", "#56647c", "#2f8a4a", dict(_FED, hat_colors=_fed("#4a5a78", "#f5c400")), "#d8261e", "#2a2018")),
    ("pass_child", _kid_variant("#1c8a4a", "#f5c400", "#2a4a9a", "#2a1c16", "#e8e4d4")),
    ("pass_woman", _women_variant("#1f9393", "#8a2a3a", "#e0a020", "#3a2418", "#c88a4a")),
)
CROWD_NAMES = tuple("crowd22_%02d" % i for i in range(len(CROWD_SPEC)))
CROWD_KIND = {n: spec[0] for n, spec in zip(CROWD_NAMES, CROWD_SPEC)}


def _build_crowd():
    for n, (base, ov) in zip(CROWD_NAMES, CROWD_SPEC):
        c = copy.deepcopy(P.CAST[base])
        c.update(ov)
        c["seed"] = c["seed"] + 3.1 * (1 + CROWD_NAMES.index(n))
        P.CAST[n] = c
        CE.CANVAS[n] = CANVAS22[base]
        CANVAS22[n] = CANVAS22[base]


def crowd_member(i, pose="pass_walk", phase=None, mirror=False):
    """(cast, pose) of crowd person i: 16 recoloured / re-hatted variants of the three passengers (coats, hats, waistcoats, ties,
    hair), props varied per person, so a crowd never looks cloned.  pose: "pass_walk" (a walk-cycle frame at `phase`, default
    spread by i; the man carries a briefcase / umbrella / newspaper or nothing, the woman a handbag or nothing) or the name of
    any STORY22 passenger pose (its own kind of person is picked), or a pose dict (kind from its 'kind' key, default the man)."""
    i = int(i)
    if isinstance(pose, str) and pose != "pass_walk":
        base, pz = STORY22[pose]
        pz = dict(pz)
    elif isinstance(pose, dict):
        base, pz = pose.get("kind", "pass_man"), {k: v for k, v in pose.items() if k != "kind"}
    else:
        base, pz = None, None
    if base is None:
        kinds = [CROWD_KIND[n] for n in CROWD_NAMES]
        name = CROWD_NAMES[i % len(CROWD_NAMES)]
        base = CROWD_KIND[name]
        ph = (0.30 + 0.137 * i) % 1.0 if phase is None else phase
        prop = None
        if base == "pass_man":
            prop = (dict(type="briefcase"), dict(type="umbrella", scale=0.9), dict(type="daily"), None)[i % 4]
        elif base == "pass_woman":
            prop = (dict(type="handbag"), None, dict(type="handbag"), dict(type="umbrella", scale=0.8))[i % 4]
        b = dict(expr=("neutral", "happy", "determined")[i % 3])
        if prop:
            b["prop_r"] = prop
        pz = cycle(name, ph, "walk", base=b, arms="l" if prop else "both")
        if prop:
            pz["arm_r"] = dict(hand=(0.40, 1.10), bend=0.4, stretch=1.0, layer="front")
            if prop.get("type") in ("umbrella",):
                pz["arm_r"] = dict(hand=(0.36, 0.98), bend=0.4, stretch=1.0, layer="front")
                pz["prop_r"] = dict(prop, angle=62)
            if prop.get("type") == "daily":
                pz["arm_r"] = dict(hand=(0.30, 0.90), bend=0.4, stretch=1.0, layer="front")
                pz["prop_r"] = dict(type="daily", angle=-70)
    else:
        same = [n for n in CROWD_NAMES if CROWD_KIND[n] == base] or [base]
        name = same[i % len(same)]
    if mirror:
        pz["mirror"] = not pz.get("mirror", False)
    return name, pz


# ============================================================================= registration
def register():
    if getattr(P, "_cast22_registered", False):
        CE.register_stage()
        if not STORY22:
            s, m = _story()
            STORY22.update(s)
            STORY22_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_ink_limb", "figure"):
        _O22[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._ink_limb = _ink_limb
    P.figure = figure
    CE.COSTUMES.update(COSTUMES22)
    CE.HATS.update(HATS22)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS22 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP22)
    for n, c in NEW_CAST22.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS22)
    _build_crowd()
    P._cast22_registered = True
    s, m = _story()
    STORY22.update(s)
    STORY22_META.update(m)
    P.STORY.update(STORY22)
    CE.register_stage()


register()
