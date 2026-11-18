#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast13.py -- the cast of film 13 ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) for the v2 puppet, as an extension
module on top of cast10 (same API, scale and anchor conventions).

    import sys; sys.path.insert(0, ".../v3/cast13"); import cast13     # registers on import (idempotent); imports cast10 .. cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast13.STORY13["pullman_blow_whistle"]
    f = puppet.figure(cast, pose, "f")                                # f["anchors"]["whistle_r"] = the whistle
    p = dict(cast13.STORY13["rich_mock_point"][1], mouth=cast13.talk_mouth(g, 1.0), blink=cast13.blink_at(g, 90))

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables and wraps the puppet helpers on top of
cast10's wrappers (each wrapper falls through for everything it does not handle, so every earlier member draws exactly as before):
    cast_ext.COSTUMES  rich13 (loud green check waistcoat, gold chain + fob + watch), crinoline13 (hooped skirt over dress7),
                       pull13 (frock7 + a brass whistle on a chain in the waistcoat pocket)
    cast_ext.HATS      bonnet13 (1860s bonnet with a ribbon tied under the chin)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
    puppet.EXPRESSIONS "dazed" (dot eyes, one raised brow, wavy mouth) -- added only if missing
    _norm / _prop / figure   pose keys of this module, new props, set-dressing overlays (armchair, jack, mud, tumble, flying hat, birdies)
New cast: pullman, rich, worker13_a/_b/_c, foreman13, lady13, gentleman13, town_a/_b/_c (+ "<name>_nohat" internals).
STORY13 / STORY13_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: whistle_svg, plans_svg, teacup_svg, jack_bar_svg, iron_jack_svg, jack_svg, purse_svg, bills_svg, newspaper_svg, armchair_svg.

Command line (QA):  python3 test_cast13.py        sheet.jpg (every member, every pose), canvas check, robustness
"""
import copy
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10     # noqa: E402  (v3/cast10, read-only; imports cast9 .. cast_ext and v2/puppet)
import cast8 as C8       # noqa: E402
import cast6 as C6       # noqa: E402
import cast_ext as CE    # noqa: E402
import puppet as P       # noqa: E402

TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C10._lin
_splat = C10._splat
_O13 = {}
_POSE13 = {"t": 0.0, "blast": 0.0, "whistle_hang": 1.0, "jturn": 0.0, "tea": 1.0, "an": {}}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours (set palette: brick, cream, ochre, velvet)
BRASS = dict(light="#fff0a8", base="#dcae3c", dark="#9a7014", deep="#6a4a0c")
IRON = dict(light="#8c929a", base="#565c66", dark="#2e323a", deep="#1c1e24")
STEEL = dict(light="#c4cad0", base="#8a929c", dark="#555c66")
PAPER = dict(light="#fbf3dd", base="#eadcb4", dark="#c0ae84")
BLUEPRINT = dict(light="#8fb3d8", base="#4a78b0", dark="#2a4c80")
CHINA = dict(light="#ffffff", base="#f4eee2", dark="#cfc4b0", rim="#c8a040", band="#b8453a")
TEA = dict(base="#9a5a2a", light="#c08850")
LEATHER = dict(light="#a8744a", base="#7a4c2a", dark="#4a2c16")
VELVET = dict(light="#c4443c", base="#8e2230", dark="#561420")
VELVET_TEAL = dict(light="#3a9a96", base="#1f6a6c", dark="#10404a")
WOOD = dict(light="#c8945a", base="#8c5a30", dark="#573418")
MUD = dict(light="#9a7248", base="#6b4a2c", dark="#432a16")
BILL = dict(light="#d8e6c0", base="#a8c490", dark="#5a7a4c")
NEWS = dict(base="#e8e0cc", ink="#8a8478", dark="#c8bea6")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _hash(*a):
    return C10._hash(*a)


# ============================================================================= props (own local frames, +x along the prop's angle)
WHISTLE_TIP = 0.20
PLANS_TIP = 0.42
JBAR_LEN, JBAR_PIV, JBAR_GRIP2, JBAR_TIP = 1.30, 1.02, 0.34, 1.12
IJACK_TIP = 0.60
NEW_PROPS13 = ("whistle", "plans", "teacup", "saucer", "teacup_saucer", "jack_bar", "iron_jack", "purse", "bills", "newspaper13")
NEW_TIP13 = {"whistle": WHISTLE_TIP, "plans": PLANS_TIP, "teacup": 0.0, "saucer": 0.0, "teacup_saucer": 0.0, "jack_bar": JBAR_TIP,
             "iron_jack": IJACK_TIP, "purse": 0.0, "bills": 0.30, "newspaper13": 0.0}


def _whistle_body(k):
    """a brass bosun's whistle along +x: mouthpiece (-0.08 .. 0), round chamber (0 .. 0.17) with a cut window, ring at 0.19."""
    o = []
    g = _lin(k, "wh", BRASS["light"], BRASS["base"], BRASS["dark"], 0, -0.05, 0, 0.05)
    o.append('<path d="M-0.085,-0.018 L0.0,-0.022 L0.0,0.022 L-0.085,0.018 Q-0.095,0 -0.085,-0.018 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<ellipse cx="0.085" cy="0.0" rx="0.092" ry="0.055" fill="%s" stroke="%s" stroke-width="0.015"/>' % (g, k.ink))
    o.append('<path d="M0.050,-0.052 L0.095,-0.052 L0.080,-0.012 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(BRASS["deep"]), k.ink))
    o.append('<path d="M0.02,-0.030 Q0.07,-0.046 0.13,-0.030" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.9"/>' % k.c(BRASS["light"]))
    o.append('<circle cx="0.190" cy="0.0" r="0.024" fill="none" stroke="%s" stroke-width="0.020"/>' % k.ink)
    o.append('<circle cx="0.190" cy="0.0" r="0.024" fill="none" stroke="%s" stroke-width="0.010"/>' % k.c(BRASS["base"]))
    return "".join(o)


def _chain_path(k, a, b, sag=0.20):
    """a hanging gold chain from a to b with a sag (screen down)."""
    mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + sag
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a[0], a[1], mx, my + sag * 0.5, b[0], b[1])
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round" stroke-dasharray="0.018 0.010"/>' % (d, k.ink, d, k.c(BRASS["base"])))


def _plans_body(k):
    """rolled plans along +x (-0.26 .. 0.40): cream paper tube, a blue-print inner end with a grid, two red ribbons, spiral end."""
    o = []
    g = _lin(k, "pl", PAPER["light"], PAPER["base"], PAPER["dark"], 0, -0.07, 0, 0.07)
    o.append('<path d="M-0.26,-0.066 L0.40,-0.066 L0.40,0.066 L-0.26,0.066 Q-0.285,0 -0.26,-0.066 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.22,-0.040 L0.36,-0.040" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>')
    # blue-print flap peeling out of the far end
    o.append('<path d="M0.40,-0.066 Q0.52,-0.090 0.54,-0.030 Q0.55,0.030 0.44,0.040 L0.40,0.066 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(BLUEPRINT["base"]), k.ink))
    for i in range(3):
        o.append('<path d="M0.43,%.4f L0.53,%.4f" stroke="%s" stroke-width="0.006" opacity="0.8"/>' % (-0.05 + 0.03 * i, -0.06 + 0.03 * i, k.c("#d8e8f8")))
    o.append('<ellipse cx="0.40" cy="0" rx="0.026" ry="0.066" fill="%s" stroke="%s" stroke-width="0.013"/>' % (k.c(PAPER["base"]), k.ink))
    o.append('<path d="M0.40,-0.04 Q0.425,-0.02 0.40,0.0 Q0.38,0.02 0.40,0.035" fill="none" stroke="%s" stroke-width="0.007"/>' % k.c(PAPER["dark"]))
    for x in (-0.12, 0.20):
        o.append('<rect x="%.4f" y="-0.072" width="0.034" height="0.144" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x, k.c("#b8453a"), k.ink))
    return "".join(o)


def _cup_body(k, cx, cy, s=1.0, tea=1.0, hside=1.0):
    """a china tea cup upright at (cx, cy) = middle of the rim; handle on side hside (+1 right).  Rim width 0.22 s."""
    o = []
    w, h = 0.110 * s, 0.115 * s
    g = _lin(k, "cu%d" % int(cx * 1000 + 5000), CHINA["light"], CHINA["base"], CHINA["dark"], cx - w, 0, cx + w, 0)
    # handle first (behind the bowl)
    hx = cx + hside * w
    o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
             % (hx - hside * 0.01 * s, cy + 0.025 * s, hside * 0.085 * s, -0.01 * s, hside * 0.03 * s, 0.050 * s, -hside * 0.005 * s, 0.040 * s, -hside * 0.07 * s, 0.018 * s, k.ink, 0.030 * s))
    o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
             % (hx - hside * 0.01 * s, cy + 0.025 * s, hside * 0.085 * s, -0.01 * s, hside * 0.03 * s, 0.050 * s, -hside * 0.005 * s, 0.040 * s, -hside * 0.07 * s, 0.018 * s, k.c(CHINA["base"]), 0.014 * s))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.015" stroke-linejoin="round"/>'
             % (cx - w, cy, cx - w * 0.95, cy + h * 1.15, cx, cy + h * 1.15, cx + w * 0.95, cy + h * 1.15, cx + w, cy, g, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (cx, cy, w, 0.028 * s, k.c(CHINA["light"]), k.ink))
    if tea > 0.05:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (cx, cy + 0.004 * s, w * 0.86, 0.020 * s, k.c(TEA["base"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (cx - w * 0.9, cy + 0.052 * s, cx + w * 0.9, cy + 0.052 * s, k.c(CHINA["band"]), 0.016 * s))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" opacity="0.8"/>'
             % (cx - w * 0.7, cy + 0.03 * s, cx - w * 0.75, cy + 0.09 * s, cx - w * 0.4, cy + 0.12 * s, 0.012 * s))
    return "".join(o)


def _saucer_body(k, cx, cy, s=1.0):
    o = []
    w = 0.185 * s
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.015"/>' % (cx, cy + 0.012 * s, w, 0.046 * s, k.c(CHINA["dark"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.012"/>' % (cx, cy, w, 0.040 * s, k.c(CHINA["light"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.012"/>' % (cx, cy, w * 0.82, 0.026 * s, k.c(CHINA["rim"])))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (cx, cy, w * 0.44, 0.014 * s, k.c(CHINA["base"])))
    return "".join(o)


def _bar_body(k):
    """an iron jack bar along +x (-0.18 .. 1.12): round steel rod, a tapered turned-over end at 1.12, a knob at -0.18."""
    o = []
    g = _lin(k, "br", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.040, 0, 0.040)
    o.append('<path d="M-0.18,-0.036 L1.04,-0.034 L1.12,-0.018 L1.12,0.018 L1.04,0.034 L-0.18,0.036 Q-0.205,0 -0.18,-0.036 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.14,-0.014 L1.00,-0.012" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>')
    o.append('<path d="M0.60,-0.034 L0.60,0.034 M0.66,-0.034 L0.66,0.034" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c(STEEL["dark"]))
    return "".join(o)


def _jack_parts(k, x, y_collar, y_floor, top, turn=0.0, s=1.0, w=0.30):
    """a cast-iron screw jack standing at x: base plate on y_floor, a fat nut housing whose collar (the bar hole) is at y_collar,
    a threaded screw rising to y_top with a flat cap.  Returns (svg, anchors).  `turn` 0..1 slides the thread."""
    o = []
    hw = w / 2.0
    gi = _lin(k, "ij%d" % int(x * 1000 + 9000), IRON["light"], IRON["base"], IRON["dark"], x - hw, 0, x + hw, 0)
    gs = _lin(k, "is%d" % int(x * 1000 + 8000), STEEL["light"], STEEL["base"], STEEL["dark"], x - 0.065, 0, x + 0.065, 0)
    yb = y_floor
    # base plate
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (x - hw * 1.55, yb, x - hw * 1.20, yb - 0.075, x + hw * 1.20, yb - 0.075, x + hw * 1.55, yb, gi, k.ink))
    # housing (below the collar)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (x - hw * 0.95, yb - 0.075, x - hw * 0.78, y_collar + 0.05, x - hw * 0.70, y_collar - 0.12, x + hw * 0.70, y_collar - 0.12,
                x + hw * 0.78, y_collar + 0.05, x + hw * 0.95, yb - 0.075, gi, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (x - hw * 0.55, y_collar + 0.10, x - hw * 0.62, yb - 0.12, k.c(IRON["light"])))
    # screw (thread) above the housing, drawn before the collar ring
    yt = top
    o.append('<rect x="%.4f" y="%.4f" width="0.130" height="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (x - 0.065, yt, (y_collar - 0.10) - yt, gs, k.ink))
    n = int(((y_collar - 0.10) - yt) / 0.055)
    off = (turn % 1.0) * 0.055
    th = []
    for i in range(n + 1):
        yy = yt + 0.03 + i * 0.055 + off
        if yy < y_collar - 0.12:
            th.append("M%.4f,%.4f L%.4f,%.4f" % (x - 0.065, yy + 0.03, x + 0.065, yy - 0.01))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (" ".join(th), k.c(IRON["deep"])))
    # cap plate
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.060" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018"/>' % (x - hw * 0.95, yt - 0.058, hw * 1.9, gi, k.ink))
    # collar ring (the bar hole) around the screw at y_collar
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.110" rx="0.020" fill="%s" stroke="%s" stroke-width="0.018"/>' % (x - hw * 0.82, y_collar - 0.075, hw * 1.64, gi, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.026" ry="0.030" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x, y_collar - 0.02, k.c(IRON["deep"]), k.ink))
    return "".join(o), dict(jack_top=(x, yt - 0.06), jack_collar=(x, y_collar), jack_base=(x, yb))


def _ijack_body(k):
    """an iron jack carried on the shoulder along +x: base plate (-0.50), fat housing (-0.45 .. -0.02), thread up to a cap (0.60);
    a short bar pushed through the collar."""
    o = []
    gi = _lin(k, "cj", IRON["light"], IRON["base"], IRON["dark"], 0, -0.12, 0, 0.12)
    gs = _lin(k, "cs", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.06, 0, 0.06)
    o.append('<path d="M-0.52,-0.20 L-0.44,-0.20 L-0.44,0.20 L-0.52,0.20 Q-0.55,0 -0.52,-0.20 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gi, k.ink))
    o.append('<path d="M-0.44,-0.13 L-0.02,-0.10 L-0.02,0.10 L-0.44,0.13 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gi, k.ink))
    o.append('<rect x="-0.02" y="-0.055" width="0.58" height="0.110" fill="%s" stroke="%s" stroke-width="0.016"/>' % (gs, k.ink))
    th = "".join("M%.4f,-0.055 L%.4f,0.055 " % (0.04 + 0.05 * i, 0.07 + 0.05 * i) for i in range(10))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (th, k.c(IRON["deep"])))
    o.append('<rect x="0.55" y="-0.14" width="0.060" height="0.280" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (gi, k.ink))
    o.append('<rect x="-0.08" y="-0.085" width="0.070" height="0.170" rx="0.012" fill="%s" stroke="%s" stroke-width="0.016"/>' % (gi, k.ink))
    o.append('<path d="M-0.40,-0.09 L-0.06,-0.06" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.35"/>')
    return "".join(o)


def _purse_body(k, fat=1.0):
    """a fat leather purse hanging below the hand (origin = the gathered neck): round bag, cord, a bill poking out of the top, gold coin glint."""
    o = []
    g = _lin(k, "pu", LEATHER["light"], LEATHER["base"], LEATHER["dark"], -0.17, 0, 0.17, 0)
    r = 0.15 * (0.85 + 0.25 * fat)
    o.append('<path d="M-0.045,0.0 Q-0.20,0.10 %.4f,0.22 Q-0.10,%.4f 0,%.4f Q0.10,%.4f %.4f,0.22 Q0.20,0.10 0.045,0.0 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (-r, 0.35 + 0.05 * fat, 0.37 + 0.05 * fat, 0.35 + 0.05 * fat, r, g, k.ink))
    o.append('<path d="M-0.060,0.03 Q0,0.075 0.060,0.03" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.060,0.03 Q0,0.075 0.060,0.03" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c(BRASS["base"]))
    o.append('<path d="M-0.02,0.0 L-0.05,-0.085 L0.045,-0.075 L0.03,0.0 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(BILL["base"]), k.ink))
    o.append('<path d="M-0.10,0.14 Q-0.13,0.22 -0.09,0.30" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>' % k.c(LEATHER["light"]))
    o.append('<circle cx="0.07" cy="0.20" r="0.016" fill="%s" stroke="%s" stroke-width="0.007"/>' % (k.c(BRASS["base"]), k.ink))
    return "".join(o)


def _bills_body(k, n=5):
    """a fan of banknotes along +x (held at the origin end): pale green notes with a border, a seal and engraved bands, NO text."""
    o = []
    for i in range(n):
        a = -26 + 13 * i
        o.append('<g transform="rotate(%.1f 0 0)">' % a)
        o.append('<rect x="0.0" y="-0.075" width="0.36" height="0.150" rx="0.008" fill="%s" stroke="%s" stroke-width="0.013"/>' % (k.c(BILL["light"] if i % 2 else BILL["base"]), k.ink))
        o.append('<rect x="0.025" y="-0.052" width="0.31" height="0.104" fill="none" stroke="%s" stroke-width="0.007"/>' % k.c(BILL["dark"]))
        if i == n - 1:
            o.append('<circle cx="0.18" cy="0" r="0.034" fill="none" stroke="%s" stroke-width="0.008"/>' % k.c(BILL["dark"]))
            o.append('<path d="M0.06,-0.02 L0.13,-0.02 M0.06,0.01 L0.13,0.01 M0.23,-0.02 L0.30,-0.02 M0.23,0.01 L0.30,0.01" stroke="%s" stroke-width="0.007"/>' % k.c(BILL["dark"]))
        o.append('</g>')
    return "".join(o)


def _news_body(k, w=0.66, h=0.84, fold=True):
    """an open broadsheet, upright (origin = the middle of its left edge's grip point, drawn centred on 0,0): grey text columns, picture box, NO readable text."""
    o = []
    x0, y0 = -w / 2, -h / 2
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x0, y0, x0 + w, y0 + 0.015, x0 + w - 0.01, y0 + h, x0 + 0.008, y0 + h - 0.012, k.c(NEWS["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x0 + 0.08, y0 + 0.075, x0 + w - 0.09, y0 + 0.08, k.c(NEWS["ink"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.006"/>' % (x0 + 0.04, y0 + 0.115, x0 + w - 0.04, y0 + 0.118, k.c(NEWS["ink"])))
    for c in range(3):
        cx = x0 + 0.06 + c * (w - 0.12) / 3.0
        for r in range(11):
            yy = y0 + 0.17 + r * 0.056
            if c == 1 and r < 4:
                continue
            ln = (w - 0.12) / 3.0 - 0.04 - (0.05 if (r * 7 + c) % 4 == 0 else 0.0)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.85"/>' % (cx, yy, cx + ln, yy, k.c(NEWS["ink"])))
    o.append('<rect x="%.4f" y="%.4f" width="0.19" height="0.16" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x0 + 0.06 + (w - 0.12) / 3.0, y0 + 0.17, k.c(NEWS["dark"]), k.ink))
    if fold:
        o.append('<path d="M0,%.4f L0,%.4f" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % (y0 + 0.01, y0 + h - 0.01, k.c(NEWS["ink"])))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS13:
        return _O13["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    if kind == "whistle":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _whistle_body(k))
        ring = _rot(0.19 * sc, 0.0, ang)
        ring = (H[0] + ring[0], H[1] + ring[1])
        tgt = (side * 0.05, 0.98)
        o += _chain_path(k, ring, tgt, 0.18)
        mp = _rot(-0.085 * sc, 0.0, ang)
        mp = (H[0] + mp[0], H[1] + mp[1])
        for p in (mp, ring, tgt):
            k.ext.append((p[0], p[1], 0.03))
        bl = _POSE13["blast"]
        if bl > 0.02:
            # sound arcs radiating from the whistle's open window (up/away from the mouthpiece)
            cx, cy = H[0] + _rot(0.09 * sc, -0.05 * sc, ang)[0], H[1] + _rot(0.09 * sc, -0.05 * sc, ang)[1]
            for j in range(3):
                f = (_POSE13["t"] * 1.2 + j / 3.0) % 1.0
                r = 0.10 + 0.34 * f
                a0 = ang - 90 - 38
                a1 = ang - 90 + 38
                p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
                p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
                o += ('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round" opacity="%.3f"/>'
                      '<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="%.3f"/>'
                      % (p0[0], p0[1], r, r, p1[0], p1[1], k.ink, bl * (1.0 - f * f), p0[0], p0[1], r, r, p1[0], p1[1], k.c("#ffe9a0"), bl * (1.0 - f * f)))
                k.ext.append((cx + (r + 0.03) * math.cos(math.radians(ang - 90)), cy + (r + 0.03) * math.sin(math.radians(ang - 90)), 0.03))
        an["whistle_" + key] = (H[0] + _rot(0.085 * sc, 0, ang)[0], H[1] + _rot(0.085 * sc, 0, ang)[1])
        an["whistle_lip_" + key] = mp
        t = _rot(WHISTLE_TIP * sc, 0, ang)
        return o, (H[0] + t[0], H[1] + t[1])
    if kind == "plans":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _plans_body(k))
        for e in ((-0.28, 0.0), (0.55, 0.0), (0.45, 0.07), (0.45, -0.09)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        t = _rot(PLANS_TIP * sc, 0, ang)
        an["plans_end_" + key] = (H[0] + t[0], H[1] + t[1])
        gx, gy = _rot(0.22 * sc, 0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        return o, (H[0] + t[0], H[1] + t[1])
    if kind in ("teacup", "saucer", "teacup_saucer"):
        o = []
        if kind == "saucer":
            cx, cy = H[0], H[1] - 0.040 * sc
            o.append(_saucer_body(k, cx, cy, sc))
        elif kind == "teacup_saucer":
            cx, cy = H[0], H[1] - 0.040 * sc
            o.append(_saucer_body(k, cx, cy, sc))
            o.append(_cup_body(k, cx - side * 0.0, cy - 0.075 * sc, sc, _POSE13["tea"], hside=side))
        else:
            # the hand pinches the handle; the cup sits toward the body; the little finger sticks out
            cx, cy = H[0] - side * 0.11 * sc, H[1] - 0.045 * sc
            o.append(_cup_body(k, cx, cy, sc, _POSE13["tea"], hside=side))
            fx0, fy0 = H[0] + side * 0.02, H[1] - 0.04 * sc
            fx1, fy1 = H[0] + side * 0.115 * sc, H[1] - 0.115 * sc
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (fx0, fy0, fx1, fy1, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.5"/>' % (fx0, fy0, fx1, fy1, "#b7a9b3"))
            k.ext.append((fx1, fy1, 0.04))
            an["pinky_" + key] = (fx1, fy1)
            an["cup_" + key] = (cx, cy)
        for (x, y) in ((cx - 0.20 * sc, cy + 0.05), (cx + 0.20 * sc, cy + 0.05), (cx, cy - 0.20 * sc), (cx, cy + 0.15 * sc)):
            k.ext.append((x, y, 0.03))
        an["cup_" + key] = (cx, cy - (0.075 * sc if kind == "teacup_saucer" else 0.0))
        return "".join(o), (cx, cy)
    if kind == "jack_bar":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _bar_body(k))
        for e in (-0.20, 1.14):
            x, y = _rot(e * sc, 0.0, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.04))
        px, py = _rot(JBAR_PIV * sc, 0, ang)
        gx, gy = _rot(JBAR_GRIP2 * sc, 0, ang)
        tx, ty = _rot(JBAR_TIP * sc, 0, ang)
        an["bar_pivot_" + key] = (H[0] + px, H[1] + py)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        return o, (H[0] + tx, H[1] + ty)
    if kind == "iron_jack":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _ijack_body(k))
        for e in ((-0.55, -0.20), (-0.55, 0.20), (0.62, -0.14), (0.62, 0.14)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.04))
        gx, gy = _rot(-0.26 * sc, 0, ang)
        tx, ty = _rot(IJACK_TIP * sc, 0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        an["jack_top_" + key] = (H[0] + tx, H[1] + ty)
        return o, (H[0] + tx, H[1] + ty)
    if kind == "purse":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _purse_body(k, 1.0))
        for (x, y) in ((-0.17, 0.22), (0.17, 0.22), (0.0, 0.40), (-0.04, -0.09)):
            k.ext.append((H[0] + x * sc, H[1] + y * sc, 0.03))
        an["purse_bottom_" + key] = (H[0], H[1] + 0.40 * sc)
        return o, (H[0], H[1] + 0.40 * sc)
    if kind == "bills":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _bills_body(k))
        for e in ((0.36, -0.20), (0.36, 0.20), (0.36, 0.0)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        t = _rot(0.30 * sc, 0, ang)
        return o, (H[0] + t[0], H[1] + t[1])
    # newspaper13: held upright; the hand grips the near edge, the sheet extends toward the body centre
    w, h = 0.66 * sc, 0.84 * sc
    cx = H[0] - side * w * 0.46
    cy = H[1] - h * 0.12
    o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (cx, cy, sc, _news_body(k))
    for (x, y) in ((-w / 2, -h / 2), (w / 2, -h / 2), (-w / 2, h / 2), (w / 2, h / 2)):
        k.ext.append((cx + x, cy + y, 0.03))
    an["paper_centre_" + key] = (cx, cy)
    an["grip_far_" + key] = (cx - side * w * 0.46, H[1])
    return o, (cx, cy)


# ============================================================================= figure-level set dressing
def _armchair_svg(k, cx, hip_y, floor_y, hw, col="red", back_top=None):
    """a velvet armchair seen from the front, drawn BEHIND the seated figure (seat top at hip_y): tall tufted back, two rolled
    arms, a seat cushion with a front face, turned wooden legs.  Returns (svg, bbox)."""
    cc = VELVET if col == "red" else VELVET_TEAL
    o = []
    bw = hw + 0.34
    bt = back_top if back_top is not None else hip_y - 1.55
    gv = _lin(k, "ac%d" % int(cx * 100 + 7000), cc["light"], cc["base"], cc["dark"], cx - bw, 0, cx + bw, 0)
    # legs
    for sx in (-1, 1):
        for fx in (0.0, 1.0):
            x = cx + sx * (bw + 0.02 - 0.08 - fx * 0.0)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % (x, hip_y + 0.30, x, floor_y, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (x, hip_y + 0.30, x, floor_y, k.c(WOOD["base"])))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.055" fill="%s" stroke="%s" stroke-width="0.014"/>' % (x, (hip_y + 0.30 + floor_y) / 2, k.c(WOOD["light"]), k.ink))
    # back
    o[-1] = ('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
             % (cx - bw + 0.10, hip_y + 0.12, cx - bw, bt + 0.45, cx - bw - 0.02, bt + 0.05, cx - bw + 0.30, bt - 0.02, cx, bt - 0.14, cx + bw - 0.30, bt - 0.02,
                cx + bw + 0.02, bt + 0.05, cx + bw, bt + 0.45, cx + bw - 0.10, hip_y + 0.12, gv, k.ink))
    # tufting buttons
    for r in range(4):
        for c in range(-2, 3):
            if (r + c) % 2:
                continue
            x, y = cx + c * (bw * 0.36), bt + 0.34 + r * 0.30
            if y < hip_y - 0.2:
                o.append('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s"/>' % (x, y, k.c(cc["dark"])))
                o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>'
                         % (x, y, x - bw * 0.18, y + 0.15, x, y, x + bw * 0.18, y + 0.15, k.c(cc["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (cx - bw + 0.30, bt + 0.04, cx, bt - 0.10, cx + bw - 0.30, bt + 0.04, k.c(BRASS["base"])))
    # arms (rolls)
    for sx in (-1, 1):
        ax = cx + sx * (bw - 0.06)
        o.append('<rect x="%.4f" y="%.4f" width="0.26" height="%.4f" rx="0.13" fill="%s" stroke="%s" stroke-width="0.026"/>' % (ax - 0.13, hip_y - 0.50, 0.92, gv, k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.12" ry="0.075" fill="%s" stroke="%s" stroke-width="0.018"/>' % (ax, hip_y - 0.46, k.c(cc["light"]), k.ink))
    # seat cushion
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
             % (cx - bw + 0.06, hip_y - 0.02, cx + bw - 0.06, hip_y - 0.02, cx + bw + 0.02, hip_y + 0.12, cx + bw - 0.06, hip_y + 0.34, cx - bw + 0.06, hip_y + 0.34,
                cx - bw - 0.02, hip_y + 0.12, cx - bw + 0.06, hip_y - 0.02, k.c(cc["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" opacity="0.8"/>' % (cx - bw + 0.10, hip_y + 0.26, cx + bw - 0.10, hip_y + 0.26, k.c(BRASS["base"])))
    for fx in range(-3, 4):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (cx + fx * 0.14, hip_y + 0.28, cx + fx * 0.14, hip_y + 0.33, k.c(BRASS["base"])))
    return "".join(o), (cx - bw - 0.1, bt - 0.2, cx + bw + 0.1, floor_y + 0.02)


def armchair_svg(uid="ac", hip_y=0.0, floor_y=0.9, hw=0.7, col="red", ink=P.INK, tint=None):
    """standalone armchair (D units, centred on x = 0) -> (svg_with_defs, bbox)."""
    k = _ctx(uid, ink, tint)
    s, bb = _armchair_svg(k, 0.0, hip_y, floor_y, hw, col)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s), bb


def _mud_pool(k, cx, y, w, t):
    """a flat mud puddle seen from the front: dark ellipse, lighter lip, ripples and a few splash drops."""
    o = ['<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, y, w, 0.17, k.c(MUD["dark"]), k.ink),
         '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (cx, y - 0.015, w * 0.93, 0.135, k.c(MUD["base"])),
         '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
         % (cx - w * 0.7, y - 0.03, cx - w * 0.4, y - 0.08, cx - w * 0.1, y - 0.05, k.c(MUD["light"]))]
    for i in range(7):
        a = _hash(7.1, i)
        x = cx + (a - 0.5) * w * 1.9
        yy = y - 0.20 - 0.30 * _hash(3.3, i)
        r = 0.020 + 0.030 * _hash(5.5, i)
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, yy, r, k.c(MUD["base"]), k.ink))
    return "".join(o)


def _birdies(k, x, y, t, n=4):
    """dizzy stars circling above the head (flat yellow 5-point stars, drawn as 4-point sparkles)."""
    o = []
    for i in range(n):
        a = 2 * math.pi * (i / float(n) + t)
        sx, sy = x + 0.52 * math.cos(a), y + 0.11 * math.sin(a)
        r = 0.07 + 0.015 * math.sin(a + 1.0)
        pts = []
        for j in range(8):
            rr = r if j % 2 == 0 else r * 0.42
            pts.append((sx + rr * math.cos(math.pi / 4 * j - math.pi / 2), sy + rr * math.sin(math.pi / 4 * j - math.pi / 2)))
        o.append('<path d="M%s Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % ("L".join("%.4f,%.4f" % p for p in pts), k.c("#f4d24c"), k.ink))
        k.ext.append((sx, sy, 0.09))
    return "".join(o)


def _mud_on_body(k, an, lev, side):
    """mud smears on chest, belly, shoulder, hands and face: seeded blobs and a few drips."""
    o = []
    spots = [("chest", 0.10, 0.12, 0.060, 0.2), ("chest", -0.22, 0.45, 0.075, 0.3), ("hip", 0.20, -0.20, 0.065, 0.45), ("hip", -0.30, -0.35, 0.050, 0.55),
             ("hand_r", 0.0, 0.0, 0.055, 0.35), ("hand_l", 0.0, 0.0, 0.055, 0.5), ("shoulder_r", 0.05, 0.12, 0.045, 0.65), ("knee_l", 0.0, 0.0, 0.05, 0.7),
             ("foot_r", 0.0, 0.0, 0.05, 0.4), ("foot_l", 0.0, 0.0, 0.05, 0.6), ("mouth", 0.34, 0.06, 0.040, 0.25), ("eye_r", 0.14, -0.14, 0.032, 0.5),
             ("mouth", -0.30, -0.12, 0.030, 0.8), ("head", 0.0, -0.32, 0.045, 0.6)]
    for i, (nm, dx, dy, r, th) in enumerate(spots):
        if nm not in an or lev < th * 0.9:
            continue
        x, y = an[nm]
        o.append(_splat(k, x + dx, y + dy, r, MUD["base"], 20.0 + 1.7 * i))
        if i in (1, 2) and lev > 0.5:
            o.append(C10._drip(k, x + dx, y + dy + r * 0.8, 0.10 * lev, 0.020, MUD["base"]))
    return "".join(o)


def _tumble(f, ang):
    """rotate the whole figure by ang degrees about the hip (positive = clockwise on screen); the feet leave the ground (feet_y is
    kept for reference: it is the standing sole line, not a floor)."""
    a = ang
    hx, hy = f["anchors"]["hip"]
    x0, y0, x1, y1 = f["bbox"]
    cs = [_rot(x - hx, y - hy, a) for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    cs = [(hx + c[0], hy + c[1]) for c in cs]

    def T(p):
        q = _rot(p[0] - hx, p[1] - hy, a)
        return (hx + q[0], hy + q[1])
    an = dict((n, T(v)) for n, v in f["anchors"].items())
    svg = '<g transform="rotate(%.3f %.4f %.4f)">%s</g>' % (a, hx, hy, f["svg"])
    return dict(f, svg=svg, anchors=an, bbox=(min(c[0] for c in cs), min(c[1] for c in cs), max(c[0] for c in cs), max(c[1] for c in cs)))


JACK_TOP_ABOVE = 0.95        # the thread top above the collar (D)


def figure(cast_name, pose=None, uid="p"):
    isd = isinstance(pose, dict) and isinstance(cast_name, str) and cast_name in P.CAST
    fly = pose.get("hat_fly") if isd else None
    ok_fly = (isinstance(fly, (tuple, list)) and len(fly) >= 2 and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in fly[:3]) and cast_name + "_nohat" in P.CAST)
    f = _O13["figure"](cast_name + "_nohat" if ok_fly else cast_name, pose, uid)
    if not isd:
        return f
    an = dict(f["anchors"])
    b = list(f["bbox"])
    behind, front = [], []
    k = P._Ctx(uid + "w", pose.get("ink") if P._is_hex(pose.get("ink")) else P.INK, P._rgb(pose["tint"].lstrip("#")) if P._is_hex(pose.get("tint")) else None)
    mir = bool(pose.get("mirror"))
    t = _POSE13["t"]

    def grow(bb):
        b[0], b[1], b[2], b[3] = min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])
    ac = pose.get("armchair")
    if ac:
        cfg = P.CAST[cast_name]
        hip = an["hip"]
        hw = _clamp(_num(cfg.get("torso_w"), 0.8) * 0.5, 0.25, 1.0)
        floor = f["feet_y"]
        s, bb = _armchair_svg(k, hip[0], hip[1] + 0.02, floor + 0.02, hw, "teal" if ac == "teal" else "red")
        behind.append(s)
        grow(bb)
        an["chair_seat"] = (hip[0], hip[1] + 0.02)
    # the jack under a bar the worker pushes
    jack = _f(pose.get("jack"), 0.0, 0.0, 1.0)
    piv = None
    for kk in ("bar_pivot_r", "bar_pivot_l"):
        if kk in an:
            piv = an[kk]
    if jack >= 0.5 and piv is not None:
        ys = f["feet_y"]
        sv, ja = _jack_parts(k, piv[0], piv[1] + 0.02, ys, piv[1] - JACK_TOP_ABOVE, _POSE13["jturn"])
        behind.append(sv)
        for n, v in ja.items():
            an[n] = v
        grow((piv[0] - 0.6, piv[1] - JACK_TOP_ABOVE - 0.1, piv[0] + 0.6, ys + 0.02))
    # mud: a puddle under the sitter and smears on the clothes
    mud = _f(pose.get("mud"), 0.0, 0.0, 1.0)
    if mud > 0.02:
        cx = an["hip"][0]
        pool_w = 0.55 + 0.9 * mud
        behind.append(_mud_pool(k, cx, f["feet_y"] + 0.02, pool_w, t))
        grow((cx - pool_w - 0.1, f["feet_y"] - 0.5, cx + pool_w + 0.1, f["feet_y"] + 0.22))
        front.append(_mud_on_body(k, an, mud, 1))
    # flying hat
    if ok_fly:
        cfg = P.CAST[cast_name]
        hs = CE.HATS.get(cfg.get("hat_style"))
        if hs is not None:
            hx, hy = float(fly[0]), float(fly[1])
            rot = float(fly[2]) if len(fly) > 2 else 0.0
            if mir:
                hx, rot = -hx, -rot
            kh = P._Ctx(uid + "h", k.ink, k.tint)
            hsvg, htop = hs(kh, cfg, 0.0)
            front.append('<defs>%s</defs><g transform="translate(%.4f %.4f) rotate(%.3f)">%s</g>' % ("".join(kh.defs), hx, hy, rot, hsvg))
            for (x, y, r) in kh.ext:
                q = _rot(x, y, rot)
                grow((hx + q[0] - r, hy + q[1] - r, hx + q[0] + r, hy + q[1] + r))
            an["hat_fly"] = (hx, hy)
    # dizzy birdies above the head
    dz = _f(pose.get("dizzy"), 0.0, 0.0, 1.0)
    if dz > 0.5:
        ht = an["hat_top"] if "hat_top" in an else an["head_top"]
        front.append(_birdies(k, ht[0], ht[1] - 0.06, t))
        grow((ht[0] - 0.7, ht[1] - 0.35, ht[0] + 0.7, ht[1] + 0.1))
    if behind or front:
        defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
        f = dict(f, svg=defs + "".join(behind) + f["svg"] + "".join(front), bbox=tuple(b), anchors=an)
    tb = pose.get("tumble")
    if isinstance(tb, (int, float)) and not isinstance(tb, bool) and math.isfinite(tb) and abs(tb) > 0.01:
        ang = _clamp(float(tb), -180.0, 180.0)
        f = _tumble(f, -ang if mir else ang)
    return f


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    t = _num(g("t"), 0.0)
    _POSE13["t"] = t if math.isfinite(t) else 0.0
    _POSE13["blast"] = _f(g("blast"), 0.0, 0.0, 1.0)
    _POSE13["whistle_hang"] = _f(g("whistle_hang"), 1.0, 0.0, 1.0)
    _POSE13["jturn"] = _f(g("jack_turn"), 0.0, -100.0, 100.0)
    _POSE13["tea"] = _f(g("tea"), 1.0, 0.0, 1.0)
    return _O13["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _cos_rich13(k, C, m):
    """the rich man's waistcoat: v2 'waistcoat' in loud green with a yellow check over the stripes, a heavy gold watch chain
    swagged across the belly to a fob and a pocket watch."""
    X = _X(m)
    inside = P._costume_waistcoat(k, C, m)
    col = C["colors"]
    u = k.uid
    k.defs.append('<pattern id="%s_ck" width="0.20" height="0.20" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0" y="0.085" width="0.20" height="0.026" fill="%s"/></pattern>' % (u, m.c, k.c(col.get("check", "#e8c040"))))
    o = ['<rect x="-0.8" y="0.45" width="1.6" height="1.2" fill="url(#%s_ck)" opacity="0.75"/>' % u]
    a0, a1 = X(-0.36, 0.92), X(0.30, 0.90)
    mid = X(0.0, 1.30)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a0 + mid + a1)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (d, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" stroke-dasharray="0.030 0.012"/>' % (d, k.c(BRASS["base"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.006" stroke-linecap="round" opacity="0.9" transform="translate(0 -0.010)"/>' % (d, k.c(BRASS["light"])))
    for p, r in ((a0, 0.040), (a1, 0.040)):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.012"/>' % (p[0], p[1], r, k.c(BRASS["base"]), k.ink))
    # fob + watch hanging from the lowest point
    fx, fy = X(0.12, 1.12)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018"/>' % (fx, fy - 0.02, fx + 0.01, fy + 0.07, k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.058" fill="%s" stroke="%s" stroke-width="0.014"/>' % (fx + 0.012, fy + 0.13, k.c(BRASS["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.040" fill="%s" stroke="%s" stroke-width="0.008"/>' % (fx + 0.012, fy + 0.13, k.c("#fbf6e4"), k.c(BRASS["dark"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (fx + 0.012, fy + 0.13, fx + 0.012, fy + 0.10, fx + 0.012, fy + 0.13, fx + 0.035, fy + 0.13, k.ink))
    return inside + "".join(o)


def _cos_crinoline13(k, C, m):
    """cast7 dress7 with the skirt flared into a crinoline bell: the hoop rings show as soft bands, and the hem is wide."""
    inside, behind, over = C10.CE.COSTUMES["dress7"](k, C, m)
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hem = yB + C["leg"] * C.get("hem_frac", 0.88)
    b = m.hwa + C.get("skirt_flare", 0.34)
    hoops = []
    for fy, fw in ((0.30, 0.55), (0.55, 0.78), (0.80, 0.94)):
        yy = yB + (hem - yB) * fy
        ww = (m.hwa * 0.8) + (b - m.hwa * 0.8) * fw
        hoops.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>'
                     % (X(-ww, yy) + X(0, yy + 0.075) + X(ww, yy) + (k.c(col["skirt_d"]),)))
    # a ruffled apron-front panel of lighter cloth
    ap = ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" opacity="0.92" stroke="%s" stroke-width="0.010"/>'
          % (X(-0.16, yB - 0.04) + X(-0.19, yB + (hem - yB) * 0.5) + X(-0.30, hem - 0.10) + X(0.30, hem - 0.10) + X(0.19, yB + (hem - yB) * 0.5) + X(0.16, yB - 0.04)
             + (k.c(col.get("apron", "#f0e4c8")), k.c(col["skirt_d"]))))
    return inside, behind, over + ap + "".join(hoops)


def _cos_pull13(k, C, m):
    """frock7 (dark coat, waistcoat, cravat) + a brass whistle on a chain: the chain loops from a waistcoat button to the pocket
    where the whistle hangs (hidden while the pose holds the whistle in the hand: pose key whistle_hang 0)."""
    inside, behind, over = C10.CE.COSTUMES["frock7"](k, C, m)
    if _POSE13["whistle_hang"] < 0.5:
        return inside, behind, over
    X = _X(m)
    h = C["torso_h"]
    a0, a1 = X(0.0, TT + h * 0.55), X(-0.17, TT + h * 0.80)
    mid = X(-0.10, TT + h * 0.84)
    extra = ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
             '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" stroke-dasharray="0.014 0.008"/>'
             % (a0 + mid + a1 + (k.ink,) + a0 + mid + a1 + (k.c(BRASS["base"]),)))
    wx, wy = a1
    extra += '<g transform="translate(%.4f %.4f) rotate(90) scale(0.62)">%s</g>' % (wx + 0.01, wy - 0.02, _whistle_body(k))
    return inside + extra, behind, over


COSTUMES13 = {"rich13": _cos_rich13, "crinoline13": _cos_crinoline13, "pull13": _cos_pull13}


# ============================================================================= hats (head frame)
def _hat_bonnet13(k, C, yaw):
    """an 1860s bonnet: a stiff brim framing the face (a half-moon shell from ear to ear over the brow), a soft crown behind it,
    a bow of ribbon at one side and ties under the chin."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    gc = CE._gradient(k, "bn", col, x0=-0.55, x1=0.55, mid=0.32)
    # crown behind the head (soft dome sitting back on the hair)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
             % (dx - 0.50, -0.20, dx - 0.52, -0.66, dx + 0.02, -0.72, dx + 0.52, -0.66, dx + 0.50, -0.20, gc, k.ink))
    o[-1] = ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
             % (dx - 0.50, -0.18, dx - 0.58, -0.70, dx + 0.02, -0.74, dx + 0.58, -0.70, dx + 0.50, -0.18, gc, k.ink))
    # front brim: a band over the forehead curving down to both ears
    brim = ('M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z'
            % (dx - 0.50, 0.12, dx - 0.58, -0.50, dx, -0.52, dx + 0.58, -0.50, dx + 0.50, 0.12,
               dx + 0.42, 0.10, dx + 0.44, -0.36, dx, -0.38, dx - 0.44, -0.36, dx - 0.42, 0.10))
    brim = ('M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z'
            % (dx - 0.52, 0.10, dx - 0.60, -0.56, dx, -0.60, dx + 0.60, -0.56, dx + 0.52, 0.10,
               dx + 0.40, 0.08, dx + 0.46, -0.34, dx, -0.40, dx - 0.46, -0.34, dx - 0.40, 0.08))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (brim, gc, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.85"/>'
             % (dx - 0.36, -0.52, dx - 0.12, -0.60, dx + 0.20, -0.58, k.c(col["light"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (dx - 0.47, -0.30, dx, -0.46, dx + 0.47, -0.30, k.c(col["dark"])))
    # ribbon band + side bow + ties under the chin
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (dx - 0.50, -0.10, dx - 0.52, 0.30, dx - 0.40, 0.58, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (dx - 0.50, -0.10, dx - 0.52, 0.30, dx - 0.40, 0.58, k.c(col["ribbon"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (dx + 0.50, -0.10, dx + 0.52, 0.30, dx + 0.40, 0.58, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (dx + 0.50, -0.10, dx + 0.52, 0.30, dx + 0.40, 0.58, k.c(col["ribbon"])))
    bx, by = dx - 0.12, 0.56
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (dx + 0.20, 0.57, dx + 0.20 + s * 0.20 + 0.0, 0.50, dx + 0.20 + s * 0.17, 0.66, k.c(col["ribbon"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="0.575" rx="0.040" ry="0.044" fill="%s" stroke="%s" stroke-width="0.014"/>' % (dx + 0.20, k.c(col["ribbon"]), k.ink))
    # small flowers on the brim
    for i, (fx, fy) in enumerate(((0.30, -0.50), (0.42, -0.42), (0.22, -0.56))):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008"/>' % (dx + fx, fy, 0.036, k.c(col["rose"] if i != 1 else col["rose2"]), k.ink))
    o.append('</g>')
    C10.C4._ext_hat(k, C, ((dx - 0.62, -0.60), (dx + 0.62, -0.60), (dx, -0.76), (dx - 0.45, 0.62), (dx + 0.45, 0.66)))
    return "".join(o), (dx, -0.74)


HATS13 = {"bonnet13": _hat_bonnet13}

# ============================================================================= cast
_FLAGS = dict(_cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast5=True, _cast4=True, _cast3=True)


def _mk(base, **kw):
    c = copy.deepcopy(P.CAST[base])
    c.update(_FLAGS)
    for kk, v in kw.items():
        if isinstance(v, dict) and isinstance(c.get(kk), dict):
            c[kk].update(v)
        else:
            c[kk] = v
    return c


def _build_cast():
    C = {}
    # Pullman: slim young engineer, dark frock coat with the sleeves rolled to cream cuffs, an ochre-and-rust waistcoat, a teal cravat,
    # a low bowler, a small brown moustache, a brass whistle on a chain.
    C["pullman"] = _mk("gentleman", seed=61.3, chain=False, hat_style="derby", moustache_style="bushy", tache_scale=0.50, mouth="smile", eye_y=0.03,
                       torso_w=0.78, coat_len=0.40, costume="pull13",
                       hat_colors=dict(base="#4a3a32", dark="#2c211c", light="#7a6a5c", band="#1c1418", brim="#3a2c24", edge="#8a7a6a", shine="#aa9a8a"),
                       hair=dict(color="#4a3224"),
                       sleeve=dict(color="#3b3438", cuff="#f1e6cf", dark="#262024", len=0.84, w=0.17),
                       colors=dict(base="#3b3438", dark="#262024", lapel="#2f292d", vest="#c28a3c", vest_b="#7a4a22", tie="#2c8a86", tie_dark="#1a5654",
                                   moustache="#4a3224", pants="#6a5c58"))
    # Rich: big belly, huge loud green check waistcoat, gold chain, mutton-chop whiskers, a tall silk top hat.
    C["rich"] = _mk("boss", seed=9.9, torso_w=1.62, torso_h=1.16, profile=C10.C2.PROFILE_ROUND, shift_pow=1.25, shoulder=(0.50, 0.44), costume="rich13",
                    hat="newsboy", hat_style="tophat7", hat_tilt=-3.0, mouth="smirk", cheeks="#ee8470", chins=True, limb_w=0.070, hip_x=0.18, leg=1.30,
                    sideburns=dict(color="#c8c0b4", dark="#9a9488"),
                    hat_colors=dict(base="#2a2428", dark="#161216", light="#4e4650", band="#7a1e2a", brim="#221c20", shine="#8a8090"),
                    hair=dict(color="#c8c0b4"),
                    colors=dict(base="#1f9a56", dark="#126a3a", lapel="#0f5a32", stripe="#f2d45c", check="#f2d45c", tie="#c9352e", tie_dark="#8c1f1c",
                                moustache="#b8b0a4", pants="#4a3a40", brass="#e6bc44", brass_l="#fff0a8"))
    # Workers: three variants of cast3's overalls man.
    C["worker13_a"] = _mk("worker1", seed=71.5, hat_style="flatnews", moustache=True, moustache_style="bushy", tache_scale=0.85, mouth="dash",
                          hat_colors=dict(base="#6a5a4a", dark="#463a2e", light="#8e7c68", shine="#b8a48e", visor="#463a2e"),
                          hair=dict(color="#3a2a20"), moustache_col=None,
                          sleeve=dict(color="#d8c9a4", cuff="#e8dcbc", dark="#a89874", len=0.52, roll=True, w=0.14),
                          colors=dict(base="#d8c9a4", collar="#d8c9a4", check="#9a8a64", denim="#4d6f8e", denim_d="#3a566f", pants="#4d6f8e", stitch="#e2b44a",
                                      moustache="#3a2a20", moustache_l="#6a5240"))
    C["worker13_b"] = _mk("worker1", seed=44.2, build="regular", torso_w=0.80, torso_h=1.00, hat_style="flatnews", moustache=False, mouth="dash",
                          beard=dict(color="#7a4a2c", dark="#4a2a18"), cap_puff=0.0,
                          hat_colors=dict(base="#8a3a30", dark="#5a2220", light="#b0584a", shine="#d08878", visor="#5a2220"),
                          hair=dict(color="#7a4a2c"),
                          sleeve=dict(color="#4a7a78", cuff="#6a9a98", dark="#2c5654", len=0.52, roll=True, w=0.15),
                          colors=dict(base="#4a7a78", collar="#4a7a78", check="#2c5654", denim="#7a6a58", denim_d="#5a4a3a", pants="#7a6a58", stitch="#e2b44a"))
    C["worker13_c"] = _mk("worker1", seed=19.8, torso_w=0.62, torso_h=0.96, leg=1.22, hat_style="knit", moustache=True, moustache_style="bushy", tache_scale=0.62,
                          hair=dict(color="#c0642a"), cheeks="#eea090", freckles=True, mouth="dash",
                          hat_colors=dict(base="#2f6a72", dark="#1c444c", light="#5a98a2", stripe="#e8d8b0", cuff="#245a62", pom="#e8d8b0", ribbon="#c8482c"),
                          sleeve=dict(color="#efe6d2", cuff="#ffffff", dark="#cbbfa4", len=0.52, roll=True, w=0.13),
                          colors=dict(base="#efe6d2", collar="#efe6d2", check="#cbbfa4", denim="#6a4a3a", denim_d="#4a3024", pants="#6a4a3a", stitch="#e2b44a",
                                      moustache="#a8481c", moustache_l="#d07a3c"))
    # Foreman: the broad man of cast3, in a rust waistcoat and a brown derby, with the whistle in his mouth.
    C["foreman13"] = _mk("foreman", seed=83.1, hat_colors=dict(base="#5a3a28", dark="#38241a", light="#86604a", brim="#4e3222", band="#1c1410", edge="#a07a5c", shine="#c09a7a"),
                         colors=dict(vest="#a8452f", vest_d="#6e2a1c", base="#f1e6cf", moustache="#3a241a", moustache_l="#6a4630"))
    # guests: the lady (crinoline, bonnet), the gentleman with the paper
    C["lady13"] = _mk("lady", seed=33.7, costume="crinoline13", skirt_flare=0.95, hem_frac=0.86, torso_w=0.58, hat_style="bonnet13", hat_tilt=-3.0,
                      hat_colors=dict(base="#e8d6b0", dark="#b49c70", light="#fbf0d6", ribbon="#2f7a78", rose="#d84a5a", rose2="#f2a0b0"),
                      hair=dict(color="#5a3a26"),
                      sleeve=dict(color="#7a2a3a", cuff="#fbf0d6", dark="#4e1824", len=0.84, w=0.15),
                      colors=dict(jacket="#7a2a3a", skirt="#a63a46", skirt_d="#6e1e2c", pants="#6e1e2c", belt="#2a1420", trim="#e8c880", apron="#f0e4c8", cameo="#f0b0a0"))
    C["lady13_seat"] = copy.deepcopy(C["lady13"])
    C["lady13_seat"].update(skirt_flare=0.52, hem_frac=0.50)
    C["gentleman13"] = _mk("gentleman", seed=26.4, hat_style="derby", moustache_style="walrus", chain=True, hair=dict(color="#8a8478"),
                           hat_colors=dict(base="#3a3a44", dark="#202028", light="#62626e", band="#141018", brim="#30303a", edge="#7a7a86", shine="#a0a0aa"),
                           colors=dict(base="#8a6a46", dark="#5e4428", lapel="#7a5a3a", vest="#2f5a58", vest_b="#e8dcb0", tie="#a8352c", tie_dark="#701e1a",
                                       pants="#6a5848", moustache="#8a8478"))
    # townsfolk
    C["town_a"] = _mk("gentleman", seed=14.1, build="stout", torso_w=1.06, torso_h=1.04, shoulder=(0.40, 0.45), hat_style="flatcap",
                      moustache_style="bushy", tache_scale=0.9, chain=False, costume="frock7", coat_len=0.34, mouth="frown",
                      hat_colors=dict(base="#8a6a46", dark="#5a4228", light="#b08c60", shine="#d0aa7a", visor="#5a4228"),
                      hair=dict(color="#6a3a22"),
                      sleeve=dict(color="#7a8a62", cuff="#f6f2ea", dark="#566444", len=0.84, w=0.17),
                      colors=dict(base="#7a8a62", dark="#566444", lapel="#6a7a54", vest="#b8452f", vest_b="#e0d0a0", tie="#e8d8b0", tie_dark="#b8a47e", pants="#5a4a3a",
                                  moustache="#6a3a22"))
    C["town_b"] = _mk("lady", seed=52.8, costume="crinoline13", skirt_flare=0.50, hem_frac=0.88, torso_w=0.66, hat_style="bonnet13",
                      hat_tilt=-2.0, hair=dict(color="#3a2a20"),
                      hat_colors=dict(base="#d8a040", dark="#9a6c1c", light="#f0c870", shine="#fbe4a0", ribbon="#b8453a", rose="#d84a5a", rose2="#f2a0b0"),
                      sleeve=dict(color="#3f7a6a", cuff="#fbf0d6", dark="#24503e", len=0.84, w=0.15),
                      colors=dict(jacket="#3f7a6a", skirt="#5a4a8a", skirt_d="#3a2e5e", pants="#3a2e5e", belt="#2a1830", trim="#e8d0a0", apron="#f0e4c8", cameo="#e8a090"))
    C["town_c"] = _mk("newsboy", seed=7.7, hat_colors=dict(base="#4a5a78", dark="#2c3850", light="#7a8aa8", shine="#a8b8d0", visor="#2c3850"),
                      colors=dict(base="#9a5a38", dark="#6a3820", lapel="#8a4a2c", pants="#5a5a62", scarf="#e8c860", scarf_d="#b8983c", scarf_s="#2c7a78", shirt="#f1e6cf"))
    for n in list(C):
        nh = copy.deepcopy(C[n])
        nh["hat_style"] = "bare7"
        nh["hat_tilt"] = 0.0
        C[n + "_nohat"] = nh
    return C


NEW13 = ("pullman", "rich", "worker13_a", "worker13_b", "worker13_c", "foreman13", "lady13", "lady13_seat", "gentleman13", "town_a", "town_b", "town_c")
WORKERS13 = ("worker13_a", "worker13_b", "worker13_c")
TOWNS13 = ("town_a", "town_b", "town_c")

# measured by test_cast13.py canvas (feet-relative, D); per member over the ordinary poses, per special pose (armchair / jack / mud / tumble / flying hat) on its own
CANVAS13 = {
    "pullman": (-1.6875, -4.6250, 1.6875, 0.1250),
    "rich": (-1.8125, -4.9375, 1.8125, 0.1250),
    "worker13_a": (-1.6250, -4.6250, 1.6250, 0.1250),
    "worker13_b": (-1.6250, -4.5625, 1.6250, 0.1250),
    "worker13_c": (-1.6250, -4.4375, 1.6250, 0.1250),
    "foreman13": (-1.7500, -4.6875, 1.7500, 0.1250),
    "lady13": (-1.6250, -4.3750, 1.6250, 0.3125),
    "lady13_seat": (-1.6250, -4.3750, 1.6250, 0.1250),
    "gentleman13": (-1.6875, -4.6250, 1.6875, 0.1250),
    "town_a": (-1.7500, -4.6250, 1.7500, 0.1250),
    "town_b": (-1.6250, -4.3750, 1.6250, 0.3125),
    "town_c": (-1.5000, -3.8125, 1.5000, 0.1250),
}
CANVAS13_POSE = {
    "pullman_hand_on_jack_bar": (-1.8750, -3.3125, 1.8750, 0.1250),
    "rich_sit_tea": (-1.3125, -3.6250, 1.3125, 0.1250),
    "rich_fall": (-4.1250, -5.3750, 4.1250, 0.8125),
    "rich_sit_in_mud": (-1.5625, -3.5625, 1.5625, 0.2500),
    "worker_turn_bar_A_a": (-1.9375, -3.1875, 1.9375, 0.1250),
    "worker_turn_bar_B_a": (-1.9375, -3.1875, 1.9375, 0.1250),
    "worker_turn_bar_A_b": (-1.9375, -3.1250, 1.9375, 0.1250),
    "worker_turn_bar_B_b": (-1.9375, -3.1250, 1.9375, 0.1250),
    "worker_turn_bar_A_c": (-1.9375, -3.2500, 1.9375, 0.1250),
    "worker_turn_bar_B_c": (-1.9375, -3.2500, 1.9375, 0.1250),
    "lady_sip_tea": (-0.9375, -3.0625, 0.9375, 0.1250),
    "gentleman_read": (-0.8750, -3.2500, 0.8750, 0.1250),
}
SPECIAL_KEYS = ("armchair", "jack", "mud", "tumble", "hat_fly", "dizzy")

_DAZED = dict(eyes="ring", pupil=0.055, brows=("one", 0.19, -10.0, 0.036, 0.16, 0.0), mouth="wavy", mouth_dy=0.01)


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="front", stretch=1.3):
    """put the free hand on the far grip (anchor grip_far_<side>) of the piece the other hand holds."""
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _to_anchor(S, name, anchor, target, key="r", it=5, dx=0.0, dy=0.0):
    """move the hand of arm_<key> so that a prop anchor (e.g. whistle_lip_r) lands on `target` (an anchor name of the figure or a point)."""
    c, p = S[name]
    for _ in range(it):
        an = figure(c, p, "q")["anchors"]
        tx, ty = (an[target] if isinstance(target, str) else target)
        bx, by = an[anchor + "_" + key]
        h = p["arm_" + key]["hand"]
        p["arm_" + key]["hand"] = (h[0] + tx + dx - bx, h[1] + ty + dy - by)


SEAT = dict(preset="crouch", crouch=0.50, spread=-0.02)
BAR_P = (1.22, 0.82)          # the jack's bar hole in the worker's head frame (A and B share it)


def _bar_pose(c, ang, yaw=0.5, hand2="r", expr="determined", crouch=0.45, extra=None):
    """two hands on a jack bar whose hole is at BAR_P whatever the angle (the hands slide up/down as it turns)."""
    d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    H = (BAR_P[0] - JBAR_PIV * d[0], BAR_P[1] - JBAR_PIV * d[1])
    p = dict(yaw=yaw, expr=expr, jack=1, legs=dict(crouch=crouch, spread=0.10, knee_r=0.5, knee_l=-0.5), arm_r=dict(hand=H, bend=0.4, stretch=1.3, layer="front"),
             prop_r=dict(type="jack_bar", angle=ang))
    if extra:
        p.update(extra)
    return p


def _story():
    S, M = {}, {}
    PU, R = "pullman", "rich"
    # ----------------------------------------------------------------- pullman
    S["pullman_stand_calm"] = (PU, dict(yaw=0.30, pitch=-0.10, expr="neutral", mouth="smile", arm_r="behind", arm_l="akimbo", legs="stand"))
    M["pullman_stand_calm"] = dict(note="standing calm and sure, one hand behind the back, one on the hip; the whistle hangs on its chain in the waistcoat pocket")
    S["pullman_point_plan"] = (PU, dict(yaw=0.45, pitch=-0.15, expr="determined", mouth="smile", gaze=(0.7, -0.1),
                                        arm_r=dict(hand=(0.80, 0.18), bend=-0.5, stretch=1.25, layer="front"), prop_r=dict(type="plans", angle=-18),
                                        arm_l="akimbo", legs="wide"))
    M["pullman_point_plan"] = dict(note="explaining the plan: the rolled plans held like a baton, pointing it forward-right (screen-right; mirror=True for left); anchor plans_end_r")
    S["pullman_blow_whistle"] = (PU, dict(yaw=0.40, pitch=-0.05, expr="determined", mouth="none", whistle_hang=0, blast=1.0, t=0.3,
                                          arm_r=dict(hand=(0.45, 0.30), bend=-0.6, stretch=1.25, layer="top"), prop_r=dict(type="whistle", angle=0),
                                          arm_l=dict(hand=(-0.80, -0.35), bend=-0.7, stretch=1.2, shape="open", layer="front"), legs="stand"))
    M["pullman_blow_whistle"] = dict(note="the whistle between the lips (anchor whistle_lip_r on the mouth), sound arcs animated by t (pose key blast 0..1), "
                                          "the other hand raised flat as a signal. The chain runs from the whistle to the waistcoat pocket. Animate: 2 frames, blast arcs advance with t")
    S["pullman_hand_on_jack_bar"] = (PU, _bar_pose(PU, -16, yaw=0.5, extra=dict(pitch=0.10, t=0.3)))
    M["pullman_hand_on_jack_bar"] = dict(note="crouched, both hands on the jack bar, turning (screw jack drawn by pose key jack=1 under anchor bar_pivot_r); animate hand/bar angle -18 <-> +18 "
                                              "(see the workers' turn_bar_A / B); jack_turn 0..1 slides the screw thread")
    S["pullman_look_up_confident"] = (PU, dict(yaw=0.30, pitch=-0.75, expr="smirk", mouth="smile", head_roll=-4, gaze=(0.5, -0.9), arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["pullman_look_up_confident"] = dict(note="chin up, looking up at the rising hotel with quiet confidence, fists on hips")
    S["pullman_nod_smile"] = (PU, dict(yaw=0.20, pitch=0.45, expr="happy", mouth="smile", head_roll=3, arm_r="behind", arm_l="behind", legs="stand"))
    M["pullman_nod_smile"] = dict(note="the nod: pitch 0.45 (down) <-> -0.05 (up) over 6 frames (cast13.NOD from cast6 can be reused), smiling")
    _to_anchor(S, "pullman_blow_whistle", "whistle_lip", "mouth", dx=0.02)
    _two_hands(S, "pullman_hand_on_jack_bar", bend=0.4, layer="front")
    # ----------------------------------------------------------------- rich
    S["rich_laugh_big"] = (R, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                   arm_r=dict(hand=(0.55, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.58, 0.98), bend=0.9, shape="open"), legs="wide"))
    M["rich_laugh_big"] = dict(note="belly laugh, head thrown back, hands on the belly, tears; held open mouth (no lip-sync); animate squash (1.02, 0.98) <-> (0.99, 1.01) every 4 frames")
    S["rich_mock_point"] = (R, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                    arm_r=dict(hand=(1.20, 0.12), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    M["rich_mock_point"] = dict(lipsync=True, note="'lift a brick building by hand?!' / 'See? Not one inch!': pointing and mocking (screen-right; mirror=True for left); "
                                                   "LIP-SYNC: mouth=talk_mouth(g) during the quotes, 'flat' otherwise")
    S["rich_sit_tea"] = (R, dict(yaw=0.20, pitch=-0.25, expr="smug", mouth="flat", head_roll=4, armchair=1, legs=SEAT, tea=1.0,
                                 arm_r=dict(hand=(0.62, 0.60), bend=-0.5, stretch=1.2, layer="front"), prop_r=dict(type="teacup", scale=1.5),
                                 arm_l=dict(hand=(0.10, 1.02), bend=0.4, stretch=1.2, layer="front"), prop_l=dict(type="saucer", scale=1.5)))
    M["rich_sit_tea"] = dict(note="seated in a velvet armchair (pose key armchair=1; 'teal' for the teal one) with the cup lifted by its handle, little finger out "
                                  "(anchors cup_r, pinky_r), saucer in the other hand (cup_l). Tea level flat: pose key tea 0..1. Canvas CANVAS13_SEAT")
    S["rich_look_window_smug"] = (R, dict(yaw=0.85, pitch=-0.25, expr="smug", mouth="flat", head_roll=-3, gaze=(0.9, 0.0),
                                          arm_r="behind", arm_l=dict(hand=(0.10, 0.95), bend=0.5, stretch=1.2, layer="front"), prop_l=dict(type="teacup_saucer", scale=1.5),
                                          legs="stand"))
    M["rich_look_window_smug"] = dict(note="standing at the window looking out (screen-right; mirror=True for left), nose up, smug; one hand behind the back, "
                                           "the other holds cup + saucer with the tea perfectly still (anchor cup_l)")
    S["rich_step_out"] = (R, dict(yaw=0.45, pitch=0.05, expr="shocked", fx=["sweat"], gaze=(0.3, 0.9), lean=-6, t=0.3,
                                  arm_r=dict(hand=(1.05, -0.10), bend=-0.7, stretch=1.3, shape="open"), arm_l=dict(hand=(-0.95, 0.20), bend=-0.3, stretch=1.3, shape="open"),
                                  legs=dict(stride=1.0, lift_r=0.85, spread=0.0)))
    M["rich_step_out"] = dict(note="stepping out of the door: the front foot (screen-right) in the air over nothing, eyes wide, arms flung out (anchor foot_r = the foot in mid-air)")
    S["rich_fall"] = (R, dict(yaw=0.35, pitch=-0.20, expr="shouting", mouth="talk_b", fx=["sweat"], tumble=28, t=0.3, hat_fly=(0.85, -1.35, 38), head_roll=8,
                              arm_r=dict(hand=(0.80, -0.75), bend=-0.9, stretch=1.3, shape="open", layer="top"), arm_l=dict(hand=(-0.80, -0.65), bend=-0.9, stretch=1.3, shape="open", layer="top"),
                              legs=dict(lift_r=1.3, lift_l=0.9, spread=0.25)))
    M["rich_fall"] = dict(note="the comic fall: tumbling (pose key tumble = degrees about the hip), arms up, legs kicking, the top hat flying off (pose key hat_fly = (dx, dy, rotation) of the "
                               "hat relative to the head; cast 'rich_nohat' is drawn). Animate tumble 10 -> 90, hat_fly rising then dropping")
    S["rich_sit_in_mud"] = (R, dict(yaw=0.15, pitch=0.10, expr="dazed", head_roll=16, lean=6, mud=1.0, dizzy=1.0, t=0.3, hat_fly=(0.42, -0.10, 28),
                                    arm_r=dict(hand=(0.85, 1.30), bend=0.2, stretch=1.2), arm_l=dict(hand=(-0.85, 1.30), bend=0.2, stretch=1.2),
                                    legs=dict(crouch=0.62, spread=0.55, knee_r=0.6, knee_l=-0.6)))
    M["rich_sit_in_mud"] = dict(note="sitting dazed in the mud puddle (pose key mud 0..1: puddle + smears), hat askew (hat_fly), birdies circling (pose key dizzy, animate t); no injury")
    S["rich_pay_sad"] = (R, dict(yaw=0.40, pitch=0.55, expr="sad", fx=["sweat"], head_roll=6, gaze=(0.4, 0.8),
                                 arm_r=dict(hand=(1.20, 0.60), bend=0.2, stretch=1.3, layer="front"), prop_r=dict(type="purse", scale=1.45),
                                 arm_l=dict(hand=(0.30, 0.95), bend=0.5, stretch=1.2, layer="front"), prop_l=dict(type="bills", angle=-25, scale=1.1), legs="stand"))
    M["rich_pay_sad"] = dict(note="handing over the fat purse (screen-right; mirror=True for left), a bill sticking out of it; the other hand holds a fan of banknotes (prop bills)")
    # ----------------------------------------------------------------- workers (three variants)
    for c, sfx in (("worker13_a", "_a"), ("worker13_b", "_b"), ("worker13_c", "_c")):
        S["worker_turn_bar_A" + sfx] = (c, _bar_pose(c, -16, extra=dict(pitch=0.12, mouth="clench", jack_turn=0.0, lean=3)))
        S["worker_turn_bar_B" + sfx] = (c, _bar_pose(c, 16, extra=dict(pitch=-0.05, mouth="clench", jack_turn=0.5, lean=3)))
        _two_hands(S, "worker_turn_bar_A" + sfx, bend=0.4, layer="front")
        _two_hands(S, "worker_turn_bar_B" + sfx, bend=0.4, layer="front")
        S["worker_carry_jack" + sfx] = (c, cycle(c, 0.30, "walk", base=dict(expr="determined", mouth="dash", prop_r=dict(type="iron_jack", angle=-62, scale=1.0)), arms="l"))
        S["worker_carry_jack" + sfx][1]["arm_r"] = dict(hand=(0.42, 0.34), bend=-0.7, stretch=1.2, layer="top")
        S["worker_stand" + sfx] = (c, dict(yaw=0.30, expr="neutral", mouth="smile", arm_r="down", arm_l="hip", legs="stand"))
        S["worker_cheer" + sfx] = (c, dict(yaw=0.15, pitch=-0.30, expr="laughing", mouth="talk_b", t=0.3, head_roll=-5,
                                           arm_r=dict(hand=(0.78, -0.72), bend=-0.9, stretch=1.3, shape="open", layer="top"),
                                           arm_l=dict(hand=(-0.78, -0.72), bend=-0.9, stretch=1.3, shape="open", layer="top"), legs="wide", squash=(0.99, 1.02)))
    M["worker_turn_bar_A"] = dict(note="2-frame push cycle on a jack (pose key jack=1 draws the screw jack at anchor bar_pivot_r, which is IDENTICAL in A and B: the bar swings "
                                       "-16 / +16 degrees about it while the hands slide). Loop A, B, A, B every 4-6 frames (or A,A,B,B); jack_turn 0 / 0.5 slides the thread. "
                                       "worker_turn_bar_A_a/_b/_c are the three variants")
    M["worker_carry_jack"] = dict(note="walking with an iron jack (prop iron_jack) on the shoulder; a cast13.cycle() frame (phase 0.30) with the arm override: animate "
                                      "cycle(cast, g/28, 'walk', base=..., arms='l') and keep arm_r / prop_r")
    M["worker_stand"] = dict(note="standing, hand on hip (blink with blink_at)")
    M["worker_cheer"] = dict(note="both arms up cheering, mouth open (talk_b held); animate squash (0.99, 1.02) <-> (1.01, 0.99) every 3 frames and t for tears-free laugh")
    # ----------------------------------------------------------------- foreman (worker with the whistle)
    F = "foreman13"
    S["foreman_blow_whistle"] = (F, dict(yaw=0.40, pitch=-0.05, expr="determined", mouth="none", blast=1.0, t=0.3,
                                         arm_r=dict(hand=(0.45, 0.30), bend=-0.6, stretch=1.25, layer="top"), prop_r=dict(type="whistle", angle=0),
                                         arm_l=dict(hand=(-0.95, -0.30), bend=-0.7, stretch=1.2, shape="open", layer="front"), legs="stand"))
    _to_anchor(S, "foreman_blow_whistle", "whistle_lip", "mouth", dx=0.02)
    M["foreman_blow_whistle"] = dict(note="the foreman blows his whistle (same prop as Pullman's), other hand raised; blast arcs from t")
    S["foreman_stand"] = (F, dict(yaw=0.30, expr="neutral", mouth="frown", arm_r=dict(hand=(0.55, 1.10), bend=0.4, stretch=1.1, layer="front"), prop_r=dict(type="whistle", angle=70),
                                  arm_l="akimbo", legs="wide"))
    M["foreman_stand"] = dict(note="arms akimbo, the whistle in one hand on its chain, waiting for the signal")
    # ----------------------------------------------------------------- guests
    L, G = "lady13", "gentleman13"
    S["lady_sip_tea"] = ("lady13_seat", dict(yaw=0.30, pitch=-0.05, expr="happy", mouth="smile", head_roll=3, armchair="teal", legs=SEAT, tea=1.0,
                                 arm_r=dict(hand=(0.38, 0.55), bend=-0.5, stretch=1.2, layer="front"), prop_r=dict(type="teacup", scale=1.5),
                                 arm_l=dict(hand=(0.10, 0.92), bend=0.4, stretch=1.2, layer="front"), prop_l=dict(type="saucer", scale=1.5)))
    M["lady_sip_tea"] = dict(note="seated in a teal velvet armchair (armchair='teal'), cup lifted with the little finger out, saucer in the other hand (a held sip; no lip-sync)")
    S["lady_stand"] = (L, dict(yaw=0.30, expr="happy", mouth="smile", arm_r=dict(hand=(0.14, 0.88), bend=0.6, stretch=1.2, layer="front"),
                               arm_l=dict(hand=(-0.14, 0.90), bend=0.6, stretch=1.2, layer="front"), legs="stand"))
    M["lady_stand"] = dict(note="standing, hands folded in front")
    S["gentleman_read"] = (G, dict(yaw=0.20, pitch=0.25, expr="neutral", mouth="frown", armchair="red", legs=SEAT,
                                   arm_r=dict(hand=(0.55, 0.92), bend=0.4, stretch=1.2, layer="front"), prop_r=dict(type="newspaper13", scale=1.25)))
    _two_hands(S, "gentleman_read", bend=0.4, layer="front")
    M["gentleman_read"] = dict(note="seated in a red velvet armchair reading a broadsheet held in both hands (no readable text: grey rules and a picture box); anchor paper_centre_r")
    S["gentleman_stand"] = (G, dict(yaw=0.30, expr="neutral", mouth="frown", arm_r="behind", arm_l="behind", legs="stand"))
    M["gentleman_stand"] = dict(note="standing, hands behind the back")
    # ----------------------------------------------------------------- townsfolk
    for c, sfx in (("town_a", "_a"), ("town_b", "_b"), ("town_c", "_c")):
        S["town_laugh_point" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                               arm_r=dict(hand=(0.82, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
        S["town_stand" + sfx] = (c, dict(yaw=0.30, expr="neutral", mouth="smile", arm_r="down", arm_l="behind", legs="stand"))
    M["town_laugh_point"] = dict(note="pointing and laughing at the rich man (screen-right; mirror=True for left): town_laugh_point_a/_b/_c (man, woman, boy)")
    M["town_stand"] = dict(note="standing watching: town_stand_a/_b/_c")
    return S, M


STORY13, STORY13_META = {}, {}


# ============================================================================= standalone pieces (D units; hand / origin at (0, 0))
def whistle_svg(uid="wh", ink=P.INK, tint=None):
    """the brass whistle along +x (mouthpiece -0.085, ring 0.19) on a short chain."""
    k = _ctx(uid, ink, tint)
    s = _whistle_body(k) + _chain_path(k, (0.19, 0.0), (0.05, 0.42), 0.16)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def plans_svg(uid="pl", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s = _plans_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def teacup_svg(uid="tc", saucer=True, pinky=True, tea=1.0, ink=P.INK, tint=None):
    """cup (+ saucer) upright, centred on x = 0, rim at y = 0; pinky=True adds the little finger on the handle side."""
    k = _ctx(uid, ink, tint)
    o = []
    if saucer:
        o.append(_saucer_body(k, 0.0, 0.14))
    o.append(_cup_body(k, 0.0, 0.0, 1.0, tea, 1.0))
    if pinky:
        o.append('<path d="M0.13,0.04 L0.22,-0.05" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.ink)
    return "<defs>%s</defs>%s" % ("".join(k.defs), "".join(o))


def jack_bar_svg(uid="jb", ink=P.INK, tint=None):
    """the jack bar along +x (-0.18 .. 1.12); the hole of the jack's collar is at x = 1.02."""
    k = _ctx(uid, ink, tint)
    s = _bar_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def iron_jack_svg(uid="ij", ink=P.INK, tint=None):
    """the carried iron jack along +x: base plate at -0.52, thread to the cap at 0.61."""
    k = _ctx(uid, ink, tint)
    s = _ijack_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def jack_svg(uid="jk", x=0.0, y_collar=0.0, y_floor=1.0, top=None, turn=0.0, ink=P.INK, tint=None):
    """the standing screw jack the workers turn: base on y_floor, housing, collar (the bar hole) at y_collar, thread up to `top`
    (default y_collar - 0.95).  Returns (svg, anchors jack_top / jack_collar / jack_base)."""
    k = _ctx(uid, ink, tint)
    s, an = _jack_parts(k, x, y_collar, y_floor, y_collar - JACK_TOP_ABOVE if top is None else top, turn)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s), an


def purse_svg(uid="pu", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s = _purse_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def bills_svg(uid="bi", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s = _bills_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def newspaper_svg(uid="np", ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s = _news_body(k)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


def mud_pool_svg(uid="mp", w=1.0, ink=P.INK, tint=None):
    k = _ctx(uid, ink, tint)
    s = _mud_pool(k, 0.0, 0.0, w, 0.0)
    return "<defs>%s</defs>%s" % ("".join(k.defs), s)


# ============================================================================= canvases
def _range(name, poses):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for p in poses:
        f = P.figure(name, p, "c")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


def canvas_of(rng):
    """the canvas (x0, y0, x1, y1) for a measured range: symmetric in x, 0.33 D head room, rounded up to 1/16 D."""
    x0, y0, x1, y1 = rng
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    return (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)


def is_special(p):
    return any(p.get(kk) for kk in SPECIAL_KEYS)


def member_poses(name):
    """the ordinary pose set of a member (the canvas is measured over these): arm presets with the new props at yaw +-0.6, crouch, wide legs,
    all fx, yaw +-1.2, every non-special STORY13 pose of the member (and its mirror) and 16 phases x 4 modes x 2 facings of the cycles."""
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None, "whistle", "plans", "teacup", "teacup_saucer", "iron_jack", "purse", "bills"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", sweat=1.0), dict(yaw=1.2), dict(yaw=-1.2)]
    for (c, p) in STORY13.values():
        if c.replace("_seat", "") == name.replace("_seat", "") and not is_special(p):
            poses += [p, dict(p, mirror=True)]
    for m in CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cycle(name, i / 16.0, m, facing=fc))
    return poses


def _measure_canvases():
    for name in NEW13:
        CANVAS13[name] = canvas_of(_range(name, member_poses(name)))
    for n, (c, p) in STORY13.items():
        if is_special(p):
            CANVAS13_POSE[n] = canvas_of(_range(c, [p, dict(p, mirror=True)]))


# ============================================================================= registration
def register():
    if getattr(P, "_cast13_registered", False):
        CE.register_stage()
        if not STORY13:
            s, m = _story()
            STORY13.update(s)
            STORY13_META.update(m)
        return
    for name in ("_prop", "_norm", "figure"):
        _O13[name] = getattr(P, name)
    P._prop = _prop
    P._norm = _norm
    P.figure = figure
    CE.COSTUMES.update(COSTUMES13)
    CE.HATS.update(HATS13)
    P.EXPRESSIONS.setdefault("dazed", _DAZED)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS13 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP13)
    for n, c in _build_cast().items():
        P.CAST[n] = c
    P._cast13_registered = True
    s, m = _story()
    STORY13.update(s)
    STORY13_META.update(m)
    CE.CANVAS.update(CANVAS13)
    P.STORY.update(STORY13)
    CE.register_stage()


register()
