#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast20.py -- the cast of film 20 ("ไอ้ช่างหมุด": Eiffel's tower and the 1887 artists' protest, Paris 1887-1909) for the v2 puppet,
as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).  Same API as cast16.

    import sys; sys.path.insert(0, ".../v3/cast20"); import cast20     # registers on import (idempotent); import BEFORE sprites
    import puppet
    cast, pose = cast20.STORY20["maupassant_quote_point"]
    f = puppet.figure(cast, pose, "f")
    p = dict(pose, mouth=cast20.talk_mouth(g, 1.0), blink=cast20.blink_at(g, 90))      # lip-sync, Maupassant only

Nothing in v2/puppet or v3/cast .. cast10 is edited.  Adds: hats hair20 (wavy / long / wild / white / slick hair masses), costumes
waiter20 (waistcoat + long apron), bustle20 (dress7 + bustle), maupassant20 (frock7 + napkin tucked in), official20 (tailcoat + tricolour sash),
face layers (headphones), expressions (sneer, laughing20, blissful, avoid, sly, proud, cheer, working), props, STORY20, cycles, canvases.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10    # noqa: E402
import cast9 as C9      # noqa: E402
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW20 = ("eiffel", "eiffel_old", "maupassant", "painter20", "composer20", "architect20", "poet20", "riveter_tongs", "riveter_hammer",
         "riveter_forge", "telegraphist", "officer", "official", "waiter", "lady20", "gent20", "child20")
TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O20 = {}
_POSE20 = {"glow": 1.0, "t": 0.0, "key": 0.0, "napkin": 0.0, "bite": 0.0, "yaw": 0.3}

cycle_people, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES
MOUTH_SET = ("flat", "talk_a", "talk_b", "talk_o", "o", ("open", 0.12, 0.05), ("open", 0.20, 0.10), ("open", 0.30, 0.19))

# ============================================================================= colours
IRON = dict(light="#9aa0aa", base="#5a606a", dark="#2c3036")
STEEL = dict(light="#d4d8de", base="#8a919c", dark="#464c56")
BRASS = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
WOOD = dict(light="#c99a64", base="#8a5a34", dark="#4a2c16")
CREAM = dict(light="#fffaf0", base="#f0e4c8", dark="#c8b890")
BLUEPRINT = dict(light="#e8f0f8", base="#cfdceb", dark="#8ea4c0")
WINE = "#7a1830"
GLOWC = dict(light="#fff2a0", base="#ff7a22", dark="#c8281a")
LEATHER = dict(light="#b88458", base="#7a4a2a", dark="#40240e")
TRI = ("#2a4a9a", "#f6f2ea", "#c8322a")      # bleu, blanc, rouge
SEAL = dict(light="#e8584a", base="#b82a22", dark="#6e1410")


def _g3(k, name, c, x0, y0, x1, y1):
    return _lin(k, name, c["light"], c["base"], c["dark"], x0, y0, x1, y1)


# ============================================================================= props
def _blueprint_body(k):
    """a rolled blueprint 0.86 long along +x (hand at the middle): blue-grey paper roll, a cream tie ribbon, white grid lines (no text)."""
    g = _g3(k, "bp", BLUEPRINT, 0, -0.07, 0, 0.07)
    o = ['<path d="M-0.43,-0.07 L0.43,-0.07 Q0.47,0 0.43,0.07 L-0.43,0.07 Q-0.47,0 -0.43,-0.07 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<ellipse cx="0.43" cy="0" rx="0.030" ry="0.070" fill="%s" stroke="%s" stroke-width="0.014"/><ellipse cx="0.435" cy="0" rx="0.012" ry="0.040" fill="%s" opacity="0.7"/>' % (k.c("#a8bcd4"), k.ink, k.c("#5a7a9c")))
    o.append('<path d="M-0.30,-0.06 L-0.30,0.06 M-0.18,-0.06 L-0.18,0.06 M0.20,-0.06 L0.20,0.06 M0.32,-0.06 L0.32,0.06" stroke="#ffffff" stroke-width="0.008" opacity="0.7"/>')
    o.append('<path d="M-0.40,-0.04 L0.38,-0.04" stroke="#ffffff" stroke-width="0.010" opacity="0.6"/>')
    o.append('<rect x="-0.20" y="-0.078" width="0.060" height="0.156" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#b83a2a"), k.ink))
    return "".join(o)


def _rivet_shape(k, s, hot=0.0):
    """a rivet along +x, dome head at the -x end; s = scale; hot > 0 paints it glowing."""
    base = STEEL if hot < 0.05 else GLOWC
    g = _g3(k, "rv", base, 0, -0.1 * s, 0, 0.1 * s)
    o = []
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (-0.02 * s, -0.050 * s, 0.30 * s, -0.050 * s, 0.30 * s, 0.050 * s, -0.02 * s, 0.050 * s, g, k.ink))
    o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f L%.3f,%.3f Q%.3f,%.3f %.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (-0.02 * s, -0.115 * s, -0.20 * s, -0.115 * s, -0.20 * s, 0.0, -0.20 * s, 0.0, -0.20 * s, 0.115 * s, -0.02 * s, 0.115 * s, g, k.ink))
    o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>' % (-0.04 * s, -0.085 * s, -0.14 * s, -0.085 * s, -0.17 * s, -0.03 * s))
    if hot > 0.05:
        o.append('<path d="M%.3f,-0.03 L%.3f,-0.03" stroke="#fffbd0" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (0.02 * s, 0.26 * s))
    return "".join(o)


RUST = dict(light="#e88a64", base="#b8462e", dark="#6e2414")


def _giant_rivet_body(k):
    """GIANT rivet 0.74 long along +x: a big round red-lead dome head (0.56 across) at -x, a short thick shank with a blunt end; shine marks."""
    g = _g3(k, "gr", RUST, 0, -0.28, 0, 0.28)
    o = ['<path d="M-0.04,-0.085 L0.40,-0.075 Q0.46,0 0.40,0.075 L-0.04,0.085 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.04,-0.045 L0.36,-0.04" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>')
    o.append('<path d="M-0.02,-0.28 C-0.40,-0.28 -0.40,0.28 -0.02,0.28 Z" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.07,-0.23 C-0.28,-0.22 -0.33,-0.10 -0.33,0.0" fill="none" stroke="#ffffff" stroke-width="0.034" stroke-linecap="round" opacity="0.6"/>')
    o.append('<path d="M-0.02,-0.28 L-0.02,0.28" stroke="%s" stroke-width="0.018"/>' % k.c(RUST["dark"]))
    return "".join(o)


def _tongs_body(k, glow=1.0):
    """long smith's tongs along +x (hand at the grip, 0.0); two bars crossing at a rivet pin, jaws at +0.96 gripping a glowing rivet; halo."""
    o = []
    if glow > 0.02:
        o.append('<circle cx="1.04" cy="0" r="0.34" fill="#ff8a30" opacity="%.2f"/><circle cx="1.04" cy="0" r="0.20" fill="#ffd060" opacity="%.2f"/>' % (0.18 * glow, 0.30 * glow))
    for s in (-1, 1):
        d = "M-0.30,%.3f L0.50,%.3f Q0.72,%.3f 0.86,%.3f L1.00,%.3f" % (s * 0.055, s * 0.020, s * 0.0, s * 0.026, s * 0.034)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.070" stroke-linecap="round" stroke-linejoin="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.044" stroke-linecap="round" stroke-linejoin="round"/>' % (d, k.c(IRON["base"])))
    o.append('<path d="M-0.28,-0.05 L0.45,-0.016" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>' % k.c(IRON["light"]))
    o.append('<circle cx="0.52" cy="0" r="0.030" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(IRON["light"]), k.ink))
    o.append('<g transform="translate(1.00 0)">%s</g>' % _rivet_shape(k, 1.0, glow if glow > 0.05 else 0.0))
    return "".join(o)


def _rivet_hammer_body(k):
    """a riveter's hammer along +x: long wooden handle from the hand (-0.12) to the iron head at 0.60; head across (domed face)."""
    gw = _g3(k, "hw", WOOD, 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.14,-0.032 L0.60,-0.030 L0.60,0.030 L-0.14,0.032 Q-0.17,0 -0.14,-0.032 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gw, k.ink)]
    gi = _g3(k, "hi", IRON, 0.5, 0, 0.8, 0)
    o.append('<path d="M0.52,-0.150 L0.72,-0.150 Q0.78,-0.12 0.78,0 Q0.78,0.12 0.72,0.150 L0.52,0.150 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (gi, k.ink))
    o.append('<path d="M0.55,-0.12 L0.72,-0.12" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>')
    o.append('<path d="M0.52,-0.150 L0.52,0.150" stroke="%s" stroke-width="0.012"/>' % k.c(IRON["dark"]))
    return "".join(o)


def _hammer_small_body(k):
    gw = _g3(k, "hw", WOOD, 0, -0.04, 0, 0.04)
    o = ['<path d="M-0.12,-0.028 L0.34,-0.026 L0.34,0.026 L-0.12,0.028 Q-0.14,0 -0.12,-0.028 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (gw, k.ink)]
    gi = _g3(k, "hi", IRON, 0.3, 0, 0.5, 0)
    o.append('<path d="M0.30,-0.10 L0.46,-0.10 L0.46,0.10 L0.30,0.10 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gi, k.ink))
    return "".join(o)


def _news_body(k):
    """a folded newspaper 0.50 x 0.62, GREEKED: grey bars for text lines, a grey block for a photo, a thick headline bar, no letters."""
    o = ['<path d="M-0.25,-0.31 L0.25,-0.31 L0.25,0.31 L-0.25,0.31 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c("#f0ead8"), k.ink)]
    o.append('<rect x="-0.20" y="-0.26" width="0.40" height="0.065" fill="%s"/>' % k.c("#4a4448"))
    o.append('<rect x="-0.20" y="-0.15" width="0.17" height="0.15" fill="%s"/>' % k.c("#a8a094"))
    for i in range(4):
        o.append('<rect x="-0.01" y="%.3f" width="0.21" height="0.016" rx="0.006" fill="%s"/>' % (-0.15 + i * 0.04, k.c("#8a8478")))
    for i in range(6):
        o.append('<rect x="-0.20" y="%.3f" width="0.40" height="0.016" rx="0.006" fill="%s"/>' % (0.04 + i * 0.043, k.c("#8a8478")))
    o.append('<path d="M0,-0.31 L0,0.31" stroke="%s" stroke-width="0.008" opacity="0.5"/>' % k.c("#a8a094"))
    return "".join(o)


def _quill_body(k):
    """a quill pen along +x: big cream-white feather with a curl, a dark nib at +0.40."""
    o = ['<path d="M-0.55,-0.14 Q-0.35,-0.20 -0.05,-0.05 L0.02,0.0 L-0.02,0.035 Q-0.30,0.08 -0.55,-0.14 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#fbf6ec"), k.ink)]
    o.append('<path d="M-0.52,-0.13 Q-0.28,-0.04 0.30,0.012" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.45,-0.12 Q-0.30,-0.15 -0.20,-0.10 M-0.38,-0.05 Q-0.25,-0.08 -0.12,-0.04" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c("#b8aa90"))
    o.append('<path d="M0.28,0.008 L0.40,0.016 L0.28,0.026 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#2a2228"), k.ink))
    return "".join(o)


def _wine_body(k):
    """a wine glass, upright, the hand at the stem (0,0): bowl up (to -0.34), red wine, round foot at +0.18."""
    o = ['<path d="M-0.10,-0.34 Q-0.115,-0.16 -0.03,-0.08 L-0.012,-0.02 L-0.012,0.15 L0.012,0.15 L0.012,-0.02 L0.03,-0.08 Q0.115,-0.16 0.10,-0.34 Z" fill="%s" fill-opacity="0.55" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#e8f2f8"), k.ink)]
    o.append('<path d="M-0.100,-0.24 L0.100,-0.24 Q0.112,-0.15 0.03,-0.08 L-0.03,-0.08 Q-0.112,-0.15 -0.100,-0.24 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(WINE), k.ink))
    o.append('<path d="M-0.07,-0.31 Q-0.08,-0.2 -0.05,-0.12" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>')
    o.append('<ellipse cx="0" cy="0.155" rx="0.085" ry="0.022" fill="%s" fill-opacity="0.7" stroke="%s" stroke-width="0.014"/>' % (k.c("#e8f2f8"), k.ink))
    return "".join(o)


def _fork_body(k, morsel=0.0):
    """a table fork along +x (hand at the handle), tines at +0.34..0.50; optional morsel (a bite) on the tines."""
    o = ['<path d="M-0.10,-0.020 L0.26,-0.014 Q0.32,-0.014 0.33,-0.05 L0.50,-0.05 L0.50,-0.032 L0.36,-0.028 L0.50,-0.012 L0.36,-0.004 L0.50,0.012 L0.36,0.020 L0.50,0.036 L0.50,0.054 L0.33,0.054 Q0.32,0.016 0.26,0.014 L-0.10,0.020 Q-0.12,0 -0.10,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(STEEL["light"]), k.ink)]
    if morsel > 0.5:
        o.append('<path d="M0.38,-0.07 Q0.52,-0.12 0.58,-0.02 Q0.58,0.08 0.46,0.08 Q0.36,0.06 0.38,-0.07 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#c8783a"), k.ink))
        o.append('<path d="M0.43,-0.04 Q0.50,-0.07 0.53,-0.02" fill="none" stroke="%s" stroke-width="0.008"/>' % k.c("#f0b06a"))
    return "".join(o)


def _knife_body(k):
    o = ['<path d="M-0.10,-0.026 L0.12,-0.026 L0.12,0.026 L-0.10,0.026 Q-0.12,0 -0.10,-0.026 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#f0e4c8"), k.ink)]
    o.append('<path d="M0.12,-0.026 L0.50,-0.026 Q0.54,0.0 0.50,0.030 L0.12,0.026 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(STEEL["light"]), k.ink))
    o.append('<path d="M0.16,-0.012 L0.46,-0.012" stroke="#ffffff" stroke-width="0.008" opacity="0.8"/>')
    return "".join(o)


def _cane_body(k):
    o = ['<path d="M-0.10,0 L1.40,0" stroke="%s" stroke-width="0.060" stroke-linecap="round"/><path d="M-0.10,0 L1.40,0" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (k.ink, k.c("#2a2228"))]
    o.append('<path d="M0.0,-0.010 L1.3,-0.010" stroke="#ffffff" stroke-width="0.008" opacity="0.4"/>')
    o.append('<circle cx="-0.12" cy="0" r="0.062" fill="%s" stroke="%s" stroke-width="0.016"/><circle cx="-0.135" cy="-0.016" r="0.018" fill="%s"/>' % (k.c(BRASS["base"]), k.ink, k.c(BRASS["light"])))
    o.append('<rect x="1.34" y="-0.022" width="0.070" height="0.044" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["base"]), k.ink))
    return "".join(o)


def _parasol_body(k):
    """an open parasol seen from the side tilted along the stick (+x = the stick tip, canopy at -x ... hand at the handle (0,0))."""
    o = ['<path d="M-0.10,0 L1.0,0" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M-0.10,0 L1.0,0" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (k.ink, k.c("#7a4a2a"))]
    g = _g3(k, "pa", dict(light="#f6b0b8", base="#e07a8a", dark="#a84a5e"), 0, -0.5, 0, 0.5)
    o.append('<path d="M0.46,-0.50 Q1.14,-0.34 1.12,0 Q1.14,0.34 0.46,0.50 Q0.80,0.26 0.80,0 Q0.80,-0.26 0.46,-0.50 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M0.46,-0.50 L1.12,0 L0.46,0.50 Z" fill="%s" opacity="0.0"/>' % g)
    for a in (-0.30, -0.15, 0.0, 0.15, 0.30):
        o.append('<path d="M1.08,%.3f Q0.90,%.3f 0.70,%.3f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (a, a * 0.6, a * 0.2, k.c("#a84a5e")))
    o.append('<path d="M0.60,-0.36 Q0.82,-0.28 0.96,-0.10" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.5"/>')
    o.append('<circle cx="1.14" cy="0" r="0.028" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(BRASS["base"]), k.ink))
    return "".join(o)


def _tray_body(k):
    """a round serving tray held flat at hand height seen edge-on (upright prop): silver tray, a glass of wine and a covered dish on it."""
    o = []
    o.append('<path d="M-0.42,-0.01 Q0,0.05 0.42,-0.01 L0.40,0.03 Q0,0.09 -0.40,0.03 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(STEEL["light"]), k.ink))
    o.append('<path d="M-0.34,0.0 Q0,0.045 0.34,0.0" fill="none" stroke="#ffffff" stroke-width="0.010" opacity="0.8"/>')
    o.append('<path d="M-0.20,-0.01 Q-0.20,-0.20 0.0,-0.20 Q0.20,-0.20 0.20,-0.01 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round" transform="translate(0.10 0)"/>' % (k.c(STEEL["light"]), k.ink))
    o.append('<circle cx="0.10" cy="-0.225" r="0.025" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(STEEL["base"]), k.ink))
    o.append('<path d="M-0.04,-0.15 Q0.02,-0.20 0.06,-0.14" transform="translate(0.10 0)" fill="none" stroke="#ffffff" stroke-width="0.012" opacity="0.8" stroke-linecap="round"/>')
    o.append('<g transform="translate(-0.24 -0.01) scale(0.62)">%s</g>' % _wine_body(k).replace('<ellipse cx="0" cy="0.155"', '<ellipse cx="0" cy="0.155"'))
    return "".join(o)


def _towel_body(k):
    """a white napkin / towel folded over the forearm, hanging from the hand (upright): two ends with blue stripes."""
    o = ['<path d="M-0.12,-0.02 L0.12,-0.02 L0.14,0.42 L0.05,0.46 L0.0,0.42 L-0.06,0.47 L-0.13,0.40 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c("#fdfbf6"), k.ink)]
    o.append('<path d="M-0.13,0.34 L0.14,0.34 M-0.125,0.37 L0.14,0.37" stroke="%s" stroke-width="0.016" opacity="0.9"/>' % k.c("#5a7ab0"))
    o.append('<path d="M-0.02,0.0 Q0,0.20 -0.03,0.34" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c("#c8c0b0"))
    return "".join(o)


def _doc_body(k):
    """an official document 0.46 x 0.60 (upright, hand at its middle): cream paper, greeked bars, a BIG red wax seal with a trailing ribbon, no letters."""
    o = ['<path d="M-0.23,-0.30 L0.23,-0.30 L0.23,0.30 L-0.23,0.30 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c("#f6efdc"), k.ink)]
    for i in range(7):
        o.append('<rect x="-0.17" y="%.3f" width="%.3f" height="0.016" rx="0.006" fill="%s"/>' % (-0.22 + i * 0.046, 0.34 - (0.12 if i in (3, 6) else 0.0), k.c("#8a8478")))
    o.append('<path d="M0.05,0.14 L0.03,0.36 L0.08,0.31 L0.12,0.38 L0.14,0.14 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#2a4a9a"), k.ink))
    o.append('<circle cx="0.07" cy="0.14" r="0.115" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(SEAL["base"]), k.ink))
    o.append('<circle cx="0.07" cy="0.14" r="0.078" fill="none" stroke="%s" stroke-width="0.014"/><circle cx="0.07" cy="0.14" r="0.034" fill="%s" opacity="0.8"/>' % (k.c(SEAL["dark"]), k.c(SEAL["light"])))
    o.append('<path d="M0.00,0.07 Q-0.02,0.12 0.0,0.16" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>')
    return "".join(o)


def _tkey_body(k, press=0.0):
    """a Morse key on a walnut base (upright, hand on the knob at (0,0)): brass lever; press 0..1 lowers it."""
    g = _g3(k, "tk", WOOD, 0, 0.28, 0, 0.40)
    o = ['<path d="M-0.20,0.30 L0.70,0.30 L0.74,0.40 L-0.24,0.40 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink)]
    ly = 0.10 + 0.07 * press
    o.append('<path d="M0.62,0.27 L0.62,0.15 L0.40,%.3f L-0.10,%.3f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round" stroke-linejoin="round"/>' % (ly, ly, k.ink))
    o.append('<path d="M0.62,0.27 L0.62,0.15 L0.40,%.3f L-0.10,%.3f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round" stroke-linejoin="round"/>' % (ly, ly, k.c(BRASS["base"])))
    o.append('<circle cx="-0.10" cy="%.3f" r="0.075" fill="%s" stroke="%s" stroke-width="0.018"/>' % (ly - 0.04, k.c("#2a2228"), k.ink))
    o.append('<circle cx="0.62" cy="0.27" r="0.030" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="0.20" cy="0.30" r="0.026" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(BRASS["light"]), k.ink, k.c(BRASS["light"]), k.ink))
    return "".join(o)


def _bowler_body(k, col=None, dx=0.0):
    col = col or HAT_DARK
    g = CE._gradient(k, "bh", col, x0=-0.42, x1=0.42, mid=0.30)
    o = ['<path d="M%.3f,0 A0.420,0.31 0 0 1 %.3f,0 Z" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (-0.42, 0.42, g, k.ink)]
    o.append('<path d="M-0.30,-0.14 Q-0.20,-0.24 0.04,-0.26" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.85"/>' % k.c(col["shine"]))
    o.append('<path d="M-0.415,-0.06 Q0,-0.04 0.415,-0.06 L0.42,0 L-0.42,0 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(col["band"]), k.ink))
    o.append('<path d="M-0.56,0.015 Q-0.585,0.078 -0.40,0.09 Q0,0.17 0.40,0.09 Q0.585,0.078 0.56,0.015 Q0.30,0.06 0,0.055 Q-0.30,0.06 -0.56,0.015 Z" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (k.c(col["brim"]), k.ink))
    return "".join(o)


def _tophat_held_body(k):
    col = TOP_COL
    g = CE._gradient(k, "th", col, x0=-0.34, x1=0.34, mid=0.30)
    o = ['<path d="M-0.30,0 L-0.30,-0.62 Q0,-0.66 0.30,-0.62 L0.30,0 Q0,0.05 -0.30,0 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M-0.30,-0.12 Q0,-0.08 0.30,-0.12 L0.30,0 Q0,0.05 -0.30,0 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(col["band"]), k.ink))
    o.append('<path d="M-0.20,-0.55 L-0.20,-0.18" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.7"/>' % k.c(col["shine"]))
    o.append('<path d="M-0.46,0.0 Q-0.46,0.07 -0.30,0.05 Q0,0.12 0.30,0.05 Q0.46,0.07 0.46,0 Q0.30,-0.01 0,0.02 Q-0.30,-0.01 -0.46,0 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(col["brim"]), k.ink))
    return "".join(o)


def _sheet_body(k):
    """a sheet of paper with greeked ink lines and many scribbled signature squiggles (the protest letter, no readable text)."""
    o = ['<path d="M-0.26,-0.34 L0.26,-0.34 L0.26,0.34 L-0.26,0.34 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c("#f6efdc"), k.ink)]
    for i in range(4):
        o.append('<rect x="-0.20" y="%.3f" width="0.40" height="0.016" rx="0.006" fill="%s"/>' % (-0.28 + i * 0.045, k.c("#8a8478")))
    for i in range(6):
        y = -0.06 + i * 0.07
        o.append('<path d="M-0.20,%.3f q0.04,-0.06 0.08,0 q0.04,0.05 0.08,-0.02 q0.04,-0.04 0.10,0.02" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (y, k.c("#2a2a5a")))
    return "".join(o)


HAT_DARK = dict(light="#5a5058", base="#2a2630", dark="#14121a", shine="#a49aaa", band="#18141c", brim="#221e26", edge="#6a6070")
TOP_COL = dict(light="#5a5058", base="#2a2630", dark="#14121a", shine="#a49aaa", band="#18141c", brim="#221e26")

# kind -> (body fn, mode, ext points, tip distance, anchor prefix, hand offset)
#   mode "angle": follows the prop angle, +x forward;  "up": upright, drawn at the hand + offset
PROPS20 = {
    "blueprint": (_blueprint_body, "angle", ((-0.47, -0.08), (0.47, 0.08)), 0.45, "blueprint_", None),
    "rivet20": (lambda k: _rivet_shape(k, 1.0), "angle", ((-0.2, -0.12), (0.30, 0.12)), 0.30, "rivet_", None),
    "giant_rivet": (_giant_rivet_body, "angle", ((-0.40, -0.28), (0.47, 0.28)), 0.46, "rivet_", None),
    "tongs_rivet": (_tongs_body, "angle", ((-0.30, -0.08), (1.14, 0.12), (1.04, -0.32), (1.04, 0.32)), 1.04, "rivet_", None),
    "tongs_cold": (lambda k: _tongs_body(k, 0.0), "angle", ((-0.30, -0.08), (1.14, 0.12)), 1.04, "rivet_", None),
    "rivet_hammer": (_rivet_hammer_body, "angle", ((-0.16, -0.04), (0.80, -0.16), (0.80, 0.16)), 0.70, "hammer_", None),
    "hammer20": (_hammer_small_body, "angle", ((-0.14, -0.04), (0.48, -0.11), (0.48, 0.11)), 0.40, "hammer_", None),
    "quill": (_quill_body, "angle", ((-0.55, -0.20), (0.42, 0.05)), 0.40, "quill_", None),
    "fork20": (_fork_body, "angle", ((-0.12, -0.03), (0.52, 0.06)), 0.50, "fork_", None),
    "knife20": (_knife_body, "angle", ((-0.12, -0.03), (0.55, 0.03)), 0.50, "knife_", None),
    "cane20": (_cane_body, "angle", ((-0.2, -0.08), (1.44, 0.06)), 1.42, "cane_", None),
    "parasol20": (_parasol_body, "angle", ((-0.12, -0.04), (1.0, 0.04), (0.46, -0.52), (1.16, 0.0), (0.46, 0.52)), 1.0, "parasol_", None),
    "news20": (_news_body, "up", ((-0.27, -0.33), (0.27, 0.33), (0.27, -0.33), (-0.27, 0.33)), 0.0, "news_", (0.10, 0.0)),
    "sheet20": (_sheet_body, "up", ((-0.28, -0.36), (0.28, 0.36), (0.28, -0.36), (-0.28, 0.36)), 0.0, "sheet_", (0.10, 0.0)),
    "doc_seal": (_doc_body, "up", ((-0.25, -0.32), (0.25, 0.32), (0.25, -0.32), (-0.25, 0.42)), 0.0, "doc_", (0.10, 0.0)),
    "wine_glass": (_wine_body, "up", ((-0.12, -0.36), (0.12, 0.18)), 0.0, "glass_", (0.0, 0.0)),
    "tray20": (_tray_body, "up", ((-0.44, -0.26), (0.44, 0.10)), 0.0, "tray_", (0.0, -0.02)),
    "towel20": (_towel_body, "up", ((-0.15, -0.03), (0.16, 0.50)), 0.0, "towel_", (0.0, 0.0)),
    "morse_key": (_tkey_body, "up", ((-0.26, -0.05), (0.76, 0.42)), 0.0, "key_tip_", (0.0, 0.0)),
    "bowler_held": (lambda k: _bowler_body(k), "up", ((-0.58, -0.32), (0.58, 0.18)), 0.0, "hat_", (0.0, 0.0)),
    "tophat_held": (_tophat_held_body, "up", ((-0.48, -0.68), (0.48, 0.12)), 0.0, "hat_", (0.0, 0.10)),
}
NEW_PROPS20 = tuple(PROPS20)
NEW_TIP20 = {kk: v[3] for kk, v in PROPS20.items()}
_PROP_ST = {}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in PROPS20:
        return _O20["_prop"](k, kind, H, ang, sc)
    key = C10.C8._side_key()
    an = C10.C8._POSE8["an"]
    fn, mode, pts, tipd, anc, off = PROPS20[kind]
    if kind == "morse_key":
        body = _tkey_body(k, _POSE20["key"])
    elif kind == "tongs_rivet":
        body = _tongs_body(k, _POSE20["glow"])
    elif kind == "fork20":
        body = _fork_body(k, _POSE20["bite"])
    else:
        body = fn(k)
    if mode == "up":
        ox, oy = off
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + ox * sc, H[1] + oy * sc, sc, body)
        for (x, y) in pts:
            k.ext.append((H[0] + (x + ox) * sc, H[1] + (y + oy) * sc, 0.03))
        tip = (H[0] + ox * sc, H[1] + oy * sc)
        an[anc + key] = (tip[0], tip[1] + (0.0 if kind != "morse_key" else 0.0))
        if kind == "tophat_held":
            an["hat_" + key] = (H[0], H[1] - 0.3 * sc)
        return o, tip
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    for (x, y) in pts:
        px, py = _rot(x * sc, y * sc, ang)
        k.ext.append((H[0] + px, H[1] + py, 0.03))
    tx, ty = _rot(tipd * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[anc + key] = tip
    if kind in ("cane20", "parasol20", "rivet_hammer", "tongs_rivet", "tongs_cold"):
        gx, gy = _rot(0.55 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
    return o, tip


# ============================================================================= hats: hair masses (head frame)
def _hat_hair20(k, C, yaw):
    """hair20: a hair mass over the crown.  C["hair20"] = dict(kind="wavy" | "long" | "wild" | "slick" | "white"); colours in C["hat_colors"]."""
    H = C.get("hair20", {})
    kind = H.get("kind", "wavy")
    col = C["hat_colors"]
    dx = -0.03 * yaw
    g = CE._gradient(k, "hr", col, x0=-0.55, x1=0.55, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    ink = k.ink
    wild = kind in ("wild",)
    top = {"slick": -0.56, "long": -0.62, "wavy": -0.64}.get(kind, -0.66)
    w = 0.54 if not wild else 0.64
    mass = [(-0.50 + dx, 0.04), (-w + dx, -0.24), (-0.44 + dx, -0.48), (-0.14 + dx, top), (0.22 + dx, top - 0.02), (0.46 + dx, -0.48), (w + dx, -0.24), (0.51 + dx, 0.04)]
    if wild:
        mass = [(-0.50 + dx, 0.06), (-0.64 + dx, -0.10), (-0.60 + dx, -0.34), (-0.42 + dx, -0.54), (-0.16 + dx, -0.68), (0.20 + dx, -0.68), (0.46 + dx, -0.54), (0.62 + dx, -0.34),
                (0.66 + dx, -0.10), (0.51 + dx, 0.06)]
    inner = [(0.44 + dx, -0.08), (0.37 + dx, -0.22), (0.20 + dx, -0.30), (0.02 + dx, -0.26), (-0.16 + dx, -0.30), (-0.34 + dx, -0.24), (-0.43 + dx, -0.10)]
    d = P._smooth_open(mass) + " L%.4f,%.4f " % (0.46 + dx, -0.04) + P._smooth_open(inner)[1:].replace("M", "L", 1) + " Z"
    # long hair / side curtains hang beside the face over the shoulders (drawn first, under the crown mass)
    if kind == "long":
        for s in (-1, 1):
            cur = [(s * 0.48 + dx, -0.10), (s * 0.58 + dx, 0.12), (s * 0.60 + dx, 0.50), (s * 0.54 + dx, 0.88), (s * 0.45 + dx, 0.70), (s * 0.45 + dx, 0.40), (s * 0.45 + dx, 0.10)]
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(cur), g, ink))
            o.append('<path d="M%.4f,0.10 Q%.4f,0.45 %.4f,0.72 M%.4f,0.14 Q%.4f,0.45 %.4f,0.70" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
                     % (s * 0.52 + dx, s * 0.56 + dx, s * 0.52 + dx, s * 0.50 + dx, s * 0.52 + dx, s * 0.51 + dx, k.c(col["dark"])))
    if kind in ("white", "wild"):
        for s in (-1, 1):
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
                     % (P._smooth_closed([(s * 0.48 + dx, -0.02), (s * 0.62 + dx, 0.04), (s * 0.64 + dx, 0.22), (s * 0.54 + dx, 0.30), (s * 0.47 + dx, 0.14)]), g, ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, ink))
    st = []
    n = 6
    for i in range(n):
        x = -0.34 + i * 0.13
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x + dx, -0.30 - 0.02 * (i % 2), x + 0.10 + dx, max(top + 0.10, -0.50 - 0.04 * (i % 3)), x + 0.20 + dx, top + 0.07 + 0.02 * (i % 2)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % ("".join(st), k.c(col["dark"])))
    if kind in ("wavy", "slick", "long"):
        px = H.get("part", -0.12) - 0.10 * yaw
        o.append('<path d="M%.4f,-0.28 Q%.4f,-0.50 %.4f,-0.58" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.9"/>' % (px, px + 0.03, px + 0.01, k.c(col["light"])))
        o.append('<path d="M%.4f,-0.28 Q%.4f,-0.50 %.4f,-0.58" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (px + 0.012, px + 0.04, px + 0.02, k.c(col["dark"])))
    if kind == "wavy":      # waves over the temples
        for s in (-1, 1):
            o.append('<path d="M%.4f,-0.08 q%.4f,0.03 %.4f,0.0 q%.4f,-0.03 %.4f,-0.02" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>'
                     % (s * 0.52 + dx, -s * 0.04, -s * 0.07, -s * 0.04, -s * 0.07, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.7"/>' % (-0.26 + dx, top + 0.10, -0.18 + dx, top + 0.02, 0.10 + dx, top + 0.01, k.c(col["light"])))
    o.append('</g>')
    C4._ext_hat(k, C, ((-0.60 + dx, -0.20), (0.60 + dx, -0.20), (dx, top), (-0.52 + dx, 0.0), (0.54 + dx, 0.0)) + (((-0.66 + dx, 0.7), (0.66 + dx, 0.7)) if kind == "long" else ()))
    return "".join(o), (dx, top)


HATS20 = {"hair20": _hat_hair20}


# ============================================================================= costumes (torso-local)
def _cos_waiter20(k, C, m):
    """waiter: white shirt with a black waistcoat (buttons, bow tie) and a LONG white apron from the waist to the shins."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    vest = C2._grad(k, "vs", col["vest"], -0.4, 0.4)
    o.append(_poly(k, [X(-0.22, 0.40), X(0.22, 0.40), X(0.30, 0.62), X(0.28, yB - 0.04), X(0.0, yB + 0.03), X(-0.28, yB - 0.04), X(-0.30, 0.62)], vest, 0.014))
    o.append(_poly(k, [X(-0.11, 0.40), X(0.11, 0.40), X(0.0, TT + h * 0.40)], k.c(col["shirt"]), 0.012))
    o.append(C7._neck(k, X, col, "bow"))
    for i in range(4):
        o.append(_circ(X(0.0, TT + h * 0.44 + i * h * 0.13), 0.016, k.c("#e8dcc0"), k, 0.007))
    o.append(_ln([X(-0.22, 0.42), X(-0.28, 0.64)], k.c("#f4f0e8"), 0.016))
    o.append(_ln([X(0.22, 0.42), X(0.28, 0.64)], k.c("#f4f0e8"), 0.016))
    inside = "".join(o)
    yt = TT + h * 0.70
    hem = yB + C["leg"] * 0.66
    a = hw * 0.74
    ap = C2._grad(k, "ap", col["apron"], -a, a)
    ov = [C2._skirt(k, "wa", X, yt, a, hem, a + 0.07, ap, sw=0.024, folds=((-0.12, yt + 0.12, -0.14, hem - 0.04), (0.14, yt + 0.12, 0.16, hem - 0.04)), fold_col=k.c(col["apron_d"]))]
    ov.append(_ln([X(-a - 0.02, yt), X(a + 0.02, yt)], k.ink, 0.056))
    ov.append(_ln([X(-a - 0.02, yt), X(a + 0.02, yt)], k.c(col["apron"]), 0.038))
    ov.append(_ln([X(-a + 0.08, yt + 0.16), X(a - 0.08, yt + 0.16)], k.c(col["apron_d"]), 0.010, ' opacity="0.8"'))
    return inside, "", "".join(ov)


def _cos_bustle20(k, C, m):
    """dress7 with a BUSTLE: a puffed bow-draped bump behind the skirt (on the screen-left side) and a trailing hem."""
    inside, back, ov = C7._cos_dress7(k, C, m)
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * 0.70
    s = -1.0 if _POSE20["yaw"] >= 0 else 1.0
    hem = yB + C["leg"] * C.get("hem_frac", 0.88)
    bx = hw + C.get("skirt_flare", 0.34) + 0.02
    g = C2._grad(k, "bu", col["skirt"], -0.8, 0.8)
    pts = [X(s * (hw * 0.6), yw - 0.02), X(s * (hw + 0.22), yw + 0.04), X(s * bx, yw + 0.30), X(s * (bx + 0.06), yw + 0.62), X(s * (bx - 0.04), hem - 0.06), X(s * (bx - 0.30), hem - 0.02),
           X(s * hw * 0.5, hem - 0.30)]
    bk = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), g, k.ink)
    bk += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (
        X(s * (hw + 0.12), yw + 0.10) + X(s * (bx + 0.02), yw + 0.40) + X(s * (bx - 0.04), hem - 0.20) + X(s * (hw + 0.02), yw + 0.14) + X(s * (bx - 0.14), yw + 0.44) + X(s * (bx - 0.22), hem - 0.14) + (k.c(col["skirt_d"]),))
    k.ext.append(X(s * (bx + 0.06), yw + 0.62) + (0.03,))
    return inside, back + bk, ov


def _cos_maupassant20(k, C, m):
    """frock7 coat; with pose key napkin=1 a white napkin tucked into the collar hangs over the chest (drawn under the lapels)."""
    inside, back, ov = C7._cos_frock7(k, C, m)
    if _POSE20["napkin"] > 0.5:
        X = _X(m)
        nap = [X(-0.14, 0.40), X(0.14, 0.40), X(0.34, 0.72), X(0.30, 1.10), X(0.0, 1.16), X(-0.30, 1.10), X(-0.34, 0.72)]
        s = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(nap), k.c("#fdfbf6"), k.ink)
        s += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (
            X(-0.20, 0.60) + X(0.0, 0.72) + X(0.20, 0.60) + X(-0.12, 0.74) + X(-0.20, 1.06) + X(0.12, 0.74) + X(0.20, 1.06) + (k.c("#c8c0b0"),))
        s += '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (X(-0.14, 0.42) + X(0.0, 0.56) + X(0.14, 0.42) + (k.c("#c8c0b0"),))
        k.ext.append(X(0.30, 1.10) + (0.03,))
        k.ext.append(X(-0.30, 1.10) + (0.03,))
        # napkin goes OVER the waistcoat but under the coat lapels: put it before lapels by returning it in front of `inside`
        inside = inside + s
    return inside, back, ov


def _cos_official20(k, C, m):
    """black tailcoat (open, lapels), white waistcoat, white cravat, and a TRICOLOUR sash (blue-white-red, no text) over the shoulder to the hip with a gold-fringed knot."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    vest = C2._grad(k, "vs", col["vest"], -0.2, 0.2)
    o.append(_poly(k, [X(-0.22, 0.40), X(0.22, 0.40), X(0.21, yB - 0.06), X(0.0, yB + 0.0), X(-0.21, yB - 0.06)], vest, 0.014))
    o.append(_poly(k, [X(-0.11, 0.40), X(0.11, 0.40), X(0.0, TT + h * 0.36)], k.c("#fbfaf6"), 0.012))
    o.append(C7._neck(k, X, col, "cravat"))
    for i in range(4):
        o.append(_circ(X(0.0, TT + h * 0.42 + i * h * 0.12), 0.015, k.c("#d8c8a0"), k, 0.007))
    lap = k.c(col["lapel"])
    for s in (-1, 1):
        o.append('<path d="%s" fill="url(#%s_tg)"/>' % (_poly_d([X(s * 0.17, 0.60), X(s * 0.15, yB + 0.02), X(s * 0.95, yB + 0.02), X(s * 0.95, 0.30), X(s * 0.30, 0.30)]), k.uid))
        o.append(_poly(k, [X(s * 0.12, 0.38), X(s * 0.24, 0.42), X(s * 0.33, 0.50), X(s * 0.26, 0.55), X(s * 0.15, TT + h * 0.62)], lap, 0.014))
        o.append(_ln([X(s * 0.15, TT + h * 0.62), X(s * 0.14, yB + 0.02)], k.ink, 0.016))
    # tricolour sash from the screen-left shoulder to the screen-right hip, three stripes
    pa, pb = X(-0.30, 0.34), X(0.62, yB - 0.02)
    dx_, dy_ = pb[0] - pa[0], pb[1] - pa[1]
    L = math.hypot(dx_, dy_)
    ux, uy = dx_ / L, dy_ / L
    nx, ny = -uy, ux
    wd = 0.09
    for i, c in enumerate(TRI):
        off = (i - 1) * wd * 2.0 / 1.0
        q = [(pa[0] + nx * (off - wd), pa[1] + ny * (off - wd)), (pb[0] + nx * (off - wd), pb[1] + ny * (off - wd)), (pb[0] + nx * (off + wd), pb[1] + ny * (off + wd)), (pa[0] + nx * (off + wd), pa[1] + ny * (off + wd))]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(q), k.c(c), k.ink))
    q = [(pa[0] + nx * 3 * wd, pa[1] + ny * 3 * wd), (pb[0] + nx * 3 * wd, pb[1] + ny * 3 * wd), (pb[0] - nx * 3 * wd, pb[1] - ny * 3 * wd), (pa[0] - nx * 3 * wd, pa[1] - ny * 3 * wd)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(q), k.ink))
    kx, ky = pb[0] - ux * 0.04, pb[1] - uy * 0.04
    o.append('<circle cx="%.4f" cy="%.4f" r="0.060" fill="%s" stroke="%s" stroke-width="0.014"/>' % (kx, ky, k.c("#c8322a"), k.ink))
    for i in range(5):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (kx + (i - 2) * 0.034, ky + 0.04, kx + (i - 2) * 0.040, ky + 0.20, k.c(BRASS["base"])))
        k.ext.append((kx + (i - 2) * 0.040, ky + 0.20, 0.02))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.012" opacity="0.3"/>' % (pa[0] + nx * 0.02, pa[1] + ny * 0.02, pb[0] + nx * 0.02, pb[1] + ny * 0.02))
    inside = "".join(o)
    yt = yB - 0.10
    hem = yB + C.get("coat_len", 0.50)
    a = hw * 0.99
    b = hw + C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "oc", X, yt, a, hem, b, g, sw=0.026, folds=((-0.14, yt + 0.12, -0.20, hem - 0.04), (0.16, yt + 0.12, 0.22, hem - 0.04)), fold_col=k.c(col.get("dark", "#1a1418")))]
    return inside, "", "".join(ov)


COSTUMES20 = {"waiter20": _cos_waiter20, "bustle20": _cos_bustle20, "maupassant20": _cos_maupassant20, "official20": _cos_official20}


# ============================================================================= expressions
EXPR20 = {
    "sneer": dict(eyes="half", brows=("one", 0.175, -12.0, 0.052, 0.18, 0.010), mouth="smirk", mouth_dy=0.012),
    "laughing20": dict(eyes="squeeze", brows=("both", 0.205, -10.0, 0.036, 0.15, 0.0), mouth="grin", mouth_dy=0.012, grin_w=0.45),
    "blissful": dict(eyes="happy", brows=("both", 0.215, -12.0, 0.034, 0.15, 0.0), mouth="smile", mouth_dy=0.0),
    "avoid": dict(eyes="squeeze", brows=("both", 0.130, 10.0, 0.050, 0.17, 0.010), mouth="frown", mouth_dy=0.0),
    "sly": dict(eyes="half", brows=("one", 0.150, -9.0, 0.048, 0.165, 0.010), mouth="smirk"),
    "proud": dict(eyes="happy", brows=("both", 0.185, -4.0, 0.040, 0.16, 0.0), mouth="smile", mouth_dy=-0.005),
    "cheer": dict(eyes="squeeze", brows=None, mouth="talk_b", mouth_dy=0.01),
    "working": dict(eyes="half", brows=("both", 0.125, 14.0, 0.050, 0.17, 0.010), mouth="clench", mouth_dy=0.0),
    "stern": dict(eyes="half", brows=("both", 0.115, 12.0, 0.052, 0.18, 0.010), mouth="frown", mouth_dy=-0.012),
    "outraged": dict(eyes="half", tilt=10.0, brows=("both", 0.095, 26.0, 0.054, 0.19, 0.015), mouth="talk_o", mouth_dy=0.0),
}


# ============================================================================= face layers: headphones
def _headphones(k, C, P_, L):
    if not C.get("headphones20"):
        return ""
    yaw = P_.get("yaw", 0.0) if isinstance(P_, dict) else 0.0
    sh = 0.10 * yaw
    o = []
    for s in (-1, 1):
        far = (yaw > 0.5 and s > 0) or (yaw < -0.5 and s < 0)
        cx = s * (0.50 - 0.10 * abs(yaw)) + sh
        sc = 0.55 if far else 1.0
        o.append('<path d="M%.4f,0.0 Q%.4f,-0.42 %.4f,-0.52" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (cx, s * 0.58 + sh, s * 0.30 + sh, k.ink))
        o.append('<path d="M%.4f,0.0 Q%.4f,-0.42 %.4f,-0.52" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (cx, s * 0.58 + sh, s * 0.30 + sh, k.c("#3a3a44")))
        o.append('<ellipse cx="%.4f" cy="0.06" rx="%.4f" ry="0.150" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, 0.085 * sc, k.c("#4a4a56"), k.ink))
        o.append('<ellipse cx="%.4f" cy="0.06" rx="%.4f" ry="0.095" fill="%s" stroke="%s" stroke-width="0.010"/>' % (cx - s * 0.012, 0.045 * sc, k.c("#8a8a98"), k.ink))
    return "".join(o)


def _beard20(k, C, P_, L):
    """a short neat beard: chin and jaw to the ears, bare cheeks, rounded top edge under the moustache (clipped to the head fill)."""
    B = C.get("beard20")
    if not B:
        return ""
    sx, my = L["mx"], L["my"]
    top = my + 0.01
    w = B.get("w", 0.30)
    d = ("M-0.70,-0.04 L-0.49,-0.04 C-0.46,0.10 %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,%.4f 0.46,0.10 0.49,-0.04 L0.70,-0.04 L0.70,0.90 L-0.70,0.90 Z"
         % (sx - w - 0.10, top - 0.07, sx - 0.20, top - 0.01, sx - 0.10, top + 0.03, sx, top + 0.03, sx + 0.10, top + 0.03, sx + 0.20, top - 0.01, sx + w + 0.10, top - 0.07))
    col = k.c(B["color"])
    o = ['<g clip-path="url(#%s_hc)"><path d="%s" fill="%s"/>' % (k.uid, d, col)]
    hs = "".join("M%.4f,%.4f q%.4f,0.03 %.4f,0.06 " % (sx + x, top + 0.09 + 0.06 * abs(x), 0.01 * (1 if x > 0 else -1), 0.02 * (1 if x > 0 else -1)) for x in (-0.34, -0.24, -0.14, -0.04, 0.06, 0.16, 0.26, 0.36))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (hs, k.c(B.get("dark", "#4a3a2a"))))
    if B.get("edge"):
        e = ("M-0.49,-0.04 C-0.46,0.10 %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,%.4f 0.46,0.10 0.49,-0.04"
             % (sx - w - 0.10, top - 0.07, sx - 0.20, top - 0.01, sx - 0.10, top + 0.03, sx, top + 0.03, sx + 0.10, top + 0.03, sx + 0.20, top - 0.01, sx + w + 0.10, top - 0.07))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.85"/>' % (e, k.ink))
    o.append('</g>')
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O20["_face"](k, C, P_, white)
    if C is None or not C.get("_cast20"):
        return svg, L
    return _beard20(k, C, P_, L) + svg + _headphones(k, C, P_, L), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE20["glow"] = _f(g("glow"), 1.0, 0.0, 1.0)
    _POSE20["key"] = _f(g("key_press"), 0.0, 0.0, 1.0)
    _POSE20["napkin"] = _f(g("napkin"), 0.0, 0.0, 1.0)
    _POSE20["bite"] = _f(g("bite"), 0.0, 0.0, 1.0)
    y = _num(g("yaw"), 0.3)
    _POSE20["yaw"] = y if math.isfinite(y) else 0.3
    return _O20["_norm"](C, pose)


# ============================================================================= variants, stool, figure
def _variant(name, pose):
    if not isinstance(pose, dict):
        return name
    if name == "eiffel" and pose.get("hat_off"):
        return "eiffel_bare"
    if name == "eiffel_old" and pose.get("hat_off"):
        return "eiffel_old_bare"
    if name == "maupassant" and pose.get("hat_off"):
        return name
    if name in ("official", "architect20", "gent20") and pose.get("hat_off"):
        return name + "_bare"
    return name


def _stool_svg(k, cx, y_seat, y_floor, w):
    o = []
    for dx_ in (-0.62, 0.62, 0.0):
        x1, x0 = cx + dx_ * w * 0.5, cx + dx_ * w * 0.36
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.100" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>'
                 % (x0, y_seat + 0.05, x1, y_floor - 0.03, k.ink, x0, y_seat + 0.05, x1, y_floor - 0.03, k.c(WOOD["base"] if dx_ else WOOD["dark"])))
    g = _g3(k, "stl", WOOD, cx - w / 2, 0, cx + w / 2, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (cx - w / 2, y_seat, cx + w / 2, y_seat, cx + w / 2 - 0.02, y_seat + 0.10, cx - w / 2 + 0.02, y_seat + 0.10, k.c(WOOD["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="0.075" fill="%s" stroke="%s" stroke-width="0.022"/>' % (cx, y_seat, w / 2, g, k.ink))
    return "".join(o), (cx - w / 2 - 0.1, y_seat - 0.08, cx + w / 2 + 0.1, y_floor + 0.05)


def figure(cast_name, pose=None, uid="p"):
    name = _variant(cast_name, pose)
    f = _O20["figure"](name, pose, uid)
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


def cycle(cast, phase, mode="walk", facing=1, base=None, arms="both", speed=1.0):
    return cycle_people(cast, phase, mode, facing, base, arms, speed)


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast20=True)


def _mk(base, **kw):
    d = dict(P.CAST[base])
    d.update(_FLAGS)
    d.update(kw)
    return d


def _hair(c, **kw):
    return dict(light=kw.get("light", c), base=c, dark=kw.get("dark", c), shine=kw.get("shine", c))


def _cast_table():
    T = {}
    # ---------------- Eiffel: neat grey-brown beard and moustache, bowler, dark frock coat, waistcoat + watch chain
    BEARD = dict(color="#7a6a58", dark="#4e4236")
    EI_COL = dict(base="#34303c", dark="#1a1820", lapel="#26222c", vest="#a8804e", vest_b="#e8d8a8", shirt="#fbfaf6", collar="#ffffff", tie="#7a2e2e", tie_dark="#4a1a1a",
                  button="#1a1820", pants="#5a5560", moustache="#7a6a58", moustache_l="#a89884")
    T["eiffel"] = _mk(
        "gentleman", seed=201.3, build="regular", torso_w=0.80, torso_h=1.02, shift_pow=1.05, shoulder=(0.31, 0.47), leg=1.30, eye_y=0.020, brow="stroke", brow_th=0.056,
        mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.80, beard20=BEARD, cheeks="#eaa08c", smirk_side=1,
        hat_style="derby", hat_tilt=-3.0, hat_colors=dict(light="#6a6068", base="#34303a", dark="#1a181e", shine="#b0a8b8", band="#1c1820", brim="#2a262e", edge="#7a7080"),
        hair=dict(color="#7a6a58", front=0.07, grow=0.20), costume="frock7", coat_len=0.50, neck="tie", chain=True, vest_buttons=5,
        sleeve=dict(color="#34303c", dark="#1a1820", cuff="#f6f2ea", len=0.84, w=0.160), shorts=dict(color="#5a5560", dark="#3a3640", cuff="#5a5560", len=0.92, w=0.120),
        colors=dict(EI_COL))
    T["eiffel_bare"] = dict(T["eiffel"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#7a6a58", front=0.10, grow=0.24, style="cap", shine="#a89884"))
    OLDW = dict(color="#e4e0da", dark="#9a968e", edge=True)
    T["eiffel_old"] = dict(
        T["eiffel"], seed=201.9, beard20=OLDW, cheeks="#e8a090", age_lines=True, leg=1.24, torso_h=0.98, lean_rest=-6.0,
        colors=dict(EI_COL, moustache="#e8e4de", moustache_l="#b8b4ae", pants="#524e58"), hair=dict(color="#f0ece6", front=0.07, grow=0.20))
    T["eiffel_old_bare"] = dict(T["eiffel_old"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#f0ece6", front=0.10, grow=0.24, style="cap", shine="#ffffff"))
    # ---------------- Maupassant: stocky, thick dark walrus moustache, dark wavy parted hair, dark-blue suit, cravat; napkin variant via pose key
    MP_COL = dict(base="#2c3f78", dark="#16224a", lapel="#1e2c58", vest="#e8dcc0", vest_b="#8a6a3a", shirt="#fbfaf6", collar="#ffffff", tie="#c8442e", tie_dark="#8a2a1a",
                  button="#e2b442", pants="#2a3050", moustache="#2a1e1a")
    T["maupassant"] = _mk(
        "gentleman", seed=202.1, build="stout", torso_w=1.18, torso_h=1.08, shift_pow=1.20, shoulder=(0.42, 0.45), arm=0.77, hip_x=0.18, leg=1.16, stance=0.07, wide=0.30,
        limb_w=0.068, eye_y=0.000, brow="stroke", brow_th=0.072, mouth="smirk", moustache=True, moustache_style="walrus", chins=True, cheeks="#ec8c78", smirk_side=1,
        hat_style="hair20", hair20=dict(kind="wavy", part=-0.14), hat_tilt=-2.0, hat_colors=dict(light="#4a3a34", base="#241a18", dark="#100a0a", shine="#7a6a62"),
        hair=dict(color="#241a18", front=0.0, grow=0.0), costume="maupassant20", coat_len=0.46, neck="cravat", chain=True, vest_buttons=5,
        sleeve=dict(color="#2c3f78", dark="#16224a", cuff="#fbfaf6", len=0.84, w=0.190), shorts=dict(color="#2a3050", dark="#161a30", cuff="#2a3050", len=0.90, w=0.150),
        colors=dict(MP_COL))
    T["maupassant"].pop("beard", None)
    # ---------------- artists
    T["painter20"] = _mk(
        "painter10", seed=203.4, costume="smock7", smock_len=0.42, smock_flare=0.10, paint=True, pencil=False, splat10=False, hat_style="beret7", hat_tilt=-10.0, beret_side=-1, hat_colors=dict(light="#d85a4a", base="#b0342a", dark="#701a14", shine="#f0907a"),
        goatee=dict(color="#3a2620", light="#6a4a3a", len=0.18), moustache=True, moustache_style="bushy", tache_scale=0.7,
        sleeve=dict(color="#d8cdb0", cuff="#fffaf0", dark="#a89c80", len=0.84, w=0.150, roll=False),
        shorts=dict(color="#5a4a3e", dark="#34281e", cuff="#5a4a3e", len=0.9, w=0.12),
        colors=dict(base="#d8cdb0", smock="#d8cdb0", dark="#a89c80", collar="#fffaf0", button="#fffaf0", pants="#5a4a3e", moustache="#3a2620", moustache_l="#6a4a3a"))
    T["composer20"] = _mk(
        "gentleman", seed=204.2, build="regular", torso_w=0.84, torso_h=1.00, shift_pow=1.05, leg=1.26, eye_y=0.020, brow="stroke", brow_th=0.060, mouth="frown",
        moustache=False, beard20=dict(color="#e4e0da", dark="#9a968e", w=0.34, edge=True), cheeks="#eaa08c", age_lines=True,
        hat_style="hair20", hair20=dict(kind="wild"), hat_tilt=0.0, hat_colors=dict(light="#ffffff", base="#f2eee8", dark="#bdb8b0", shine="#ffffff"), hair=dict(color="#f2eee8", front=0.0, grow=0.0),
        costume="frock7", coat_len=0.50, neck="cravat", chain=False, vest_buttons=4, flower=None,
        sleeve=dict(color="#3e5e48", dark="#223a2a", cuff="#f6f2ea", len=0.84, w=0.160), shorts=dict(color="#4a4a50", dark="#2a2a30", cuff="#4a4a50", len=0.92, w=0.120),
        colors=dict(base="#3e5e48", dark="#1e3226", lapel="#2e4a38", vest="#c8b070", vest_b="#7a5a2a", shirt="#fbfaf6", collar="#ffffff", tie="#8a2a3a", tie_dark="#521620", button="#1a1a16", pants="#4a4a50"))
    T["architect20"] = _mk(
        "gentleman", seed=205.7, build="slim", torso_w=0.66, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shoulder=(0.25, 0.50), leg=1.34, eye_y=0.030, brow="stroke", brow_th=0.052, mouth="smirk",
        moustache=True, moustache_style="bushy", tache_scale=0.7, cheeks="#e8a08a",
        hat_style="tophat7", hat_tilt=-4.0, hat_colors=dict(light="#d0c4a8", base="#a8946a", dark="#6a5a3a", shine="#fffaf0", band="#3e5e48", brim="#8a7852"), hair=dict(color="#4a3a2a", front=0.07, grow=0.2),
        costume="frock7", coat_len=0.42, neck="tie", chain=True, vest_buttons=4,
        sleeve=dict(color="#8a6a44", dark="#523a22", cuff="#f6f2ea", len=0.84, w=0.145), shorts=dict(color="#6a6a72", dark="#44444a", cuff="#6a6a72", len=0.92, w=0.110),
        colors=dict(base="#8a6a44", dark="#4a321c", lapel="#6a4e30", vest="#e8d8a8", vest_b="#7a5a2a", shirt="#fbfaf6", collar="#ffffff", tie="#2a4a6a", tie_dark="#162a3e", button="#2a1a12", pants="#6a6a72", moustache="#4a3a2a"))
    T["architect20_bare"] = dict(T["architect20"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#4a3a2a", front=0.12, grow=0.24, style="cap", shine="#7a6a5a"))
    T["poet20"] = _mk(
        "gentleman", seed=206.9, build="slim", torso_w=0.60, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shoulder=(0.23, 0.50), leg=1.32, eye_y=0.040, brow="dome", brow_th=0.040, mouth="smile",
        moustache=False, cheeks="#f2a896", smirk_side=-1,
        hat_style="hair20", hair20=dict(kind="long", part=0.04), hat_tilt=0.0, hat_colors=dict(light="#9a6a44", base="#6a4228", dark="#3a2214", shine="#d0a070"), hair=dict(color="#6a4228", front=0.0, grow=0.0),
        costume="frock7", coat_len=0.44, neck="cravat", chain=False, vest_buttons=4,
        sleeve=dict(color="#5e2e5e", dark="#381a3a", cuff="#fbf6ee", len=0.84, w=0.140), shorts=dict(color="#3a3440", dark="#201c26", cuff="#3a3440", len=0.92, w=0.110),
        colors=dict(base="#5e2e5e", dark="#321832", lapel="#46224a", vest="#e8dcc0", vest_b="#8a6a3a", shirt="#fbfaf6", collar="#ffffff", tie="#fdfbf6", tie_dark="#c8c0b0", button="#2a1a2a", pants="#3a3440"))
    # ---------------- workers: blue smocks
    SM = dict(base="#3a5a9a", smock="#3a5a9a", dark="#243a6a", collar="#5a7ab8", button="#e8dcc0", pants="#6a5a4a", paint=False)
    wk = dict(costume="smock7", smock_len=0.40, smock_flare=0.12, paint=False, pencil=False, colors=dict(SM),
              sleeve=dict(color="#3a5a9a", dark="#243a6a", cuff="#4a6aaa", len=0.84, w=0.160, roll=True),
              shorts=dict(color="#6a5a4a", dark="#3e3228", cuff="#6a5a4a", len=0.92, w=0.130), boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.10, toe=0.16))
    T["riveter_tongs"] = _mk(
        "worker1", seed=207.1, build="regular", torso_w=0.84, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.31, 0.47), hip_x=0.16, leg=1.22, eye_y=0.020, brow="stroke", brow_th=0.060,
        mouth="dash", moustache=False, cheeks="#e89480", hat_style="flatnews", hat_tilt=-3.0, cap_puff=0.8,
        hat_colors=dict(light="#6a7a9a", base="#46567a", dark="#2a3652", shine="#9aaaca", visor="#2a3652"), hair=dict(color="#4a3020", front=0.08, grow=0.22), **wk)
    T["riveter_hammer"] = _mk(
        "worker1", seed=207.8, build="slim", torso_w=0.66, torso_h=1.02, shoulder=(0.26, 0.50), leg=1.34, eye_y=0.030, brow="stroke", brow_th=0.054, mouth="dash",
        moustache=True, moustache_style="bushy", tache_scale=0.8, cheeks="#eaa08a", hat_style="flatnews", hat_tilt=-5.0, cap_puff=0.6,
        hat_colors=dict(light="#a08a6a", base="#7a664a", dark="#4a3e2c", shine="#c4b090", visor="#4a3e2c"), hair=dict(color="#5a4030", front=0.08, grow=0.22),
        **dict(wk, colors=dict(SM, base="#2e4e8a", smock="#2e4e8a", dark="#1c3262", moustache="#4a3020", moustache_l="#7a5a3a"), sleeve=dict(color="#2e4e8a", dark="#1c3262", cuff="#3e5e9a", len=0.84, w=0.150, roll=True)))
    T["riveter_forge"] = _mk(
        "worker1", seed=208.4, build="regular", torso_w=0.96, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.34, 0.47), hip_x=0.16, leg=1.16, eye_y=0.010, brow="stroke", brow_th=0.064,
        mouth="dash", moustache=False, beard20=dict(color="#6a3a22", dark="#3e2010", w=0.34), cheeks="#e0705a", hat_style="kerchief", hat_tilt=0.0,
        hat_colors=dict(light="#d8584a", base="#b0342a", dark="#701a14", dot="#f6efe0"), hair=dict(color="#4a3020", front=0.08, grow=0.22),
        **dict(wk, colors=dict(SM, base="#46629a", smock="#46629a", dark="#2a3e6a"), sleeve=dict(color="#46629a", dark="#2a3e6a", cuff="#5676ae", len=0.80, w=0.165, roll=True)))
    # ---------------- soldier-telegraphist 1909 (kepi red top + blue band, blue tunic, red trousers, headphones) and officer (gold epaulettes)
    KEPI = dict(light="#e0584a", base="#c0302a", dark="#7a1a16", shine="#f6a090", band="#223a78", piping="#e8d8a0", visor="#16121a")
    T["telegraphist"] = _mk(
        "police", seed=209.2, headphones20=True, hat_style="kepi7", hat_tilt=-3.0, hat_colors=dict(KEPI), moustache=True, moustache_style="bushy", tache_scale=0.7, cheeks="#e8a08a",
        hair=dict(color="#3a2a22", front=0.07, grow=0.2), costume="uniform7", double=True,
        sleeve=dict(color="#2c4a8a", dark="#16264e", cuff="#e8d8a0", len=0.82, w=0.160), shorts=dict(color="#b03a3a", dark="#701e1e", cuff="#b03a3a", len=0.90, w=0.120),
        colors=dict(base="#2c4a8a", dark="#16264e", pocket="#34549a", button="#e8d8a0", belt="#2a1e18", patch="#c8322a", pants="#b03a3a", moustache="#3a2a22", moustache_l="#6a5a50"))
    T["officer"] = _mk(
        "police", seed=210.5, hat_style="kepi7", hat_tilt=-3.0, hat_colors=dict(KEPI, band="#223a78", piping="#e2b442"), moustache=True, moustache_style="handlebar", tache_scale=0.95, cheeks="#e8a08a",
        hair=dict(color="#4a3a32", front=0.07, grow=0.2), costume="uniform7", double=True, epaulette10=True, cord="#e2b442", gloves10=True,
        sleeve=dict(color="#2c4a8a", dark="#16264e", cuff="#e2b442", len=0.82, w=0.160), shorts=dict(color="#b03a3a", dark="#701e1e", cuff="#b03a3a", len=0.90, w=0.120),
        colors=dict(base="#2c4a8a", dark="#16264e", pocket="#34549a", button="#e2b442", belt="#c8a04a", patch="#c8322a", pants="#b03a3a", moustache="#4a3a32", moustache_l="#8a7a6a"))
    # ---------------- 1889 official: black tailcoat, tricolour sash, top hat
    T["official"] = _mk(
        "gentleman", seed=211.1, build="regular", torso_w=0.86, torso_h=1.02, shift_pow=1.05, leg=1.26, eye_y=0.020, brow="stroke", brow_th=0.058, mouth="frown",
        moustache=True, moustache_style="walrus", cheeks="#ea9a88", chins=False,
        hat_style="tophat7", hat_tilt=-2.0, hat_colors=dict(light="#5a5058", base="#2a2630", dark="#14121a", shine="#a49aaa", band="#c8322a", brim="#221e26"), hair=dict(color="#6a6a70", front=0.07, grow=0.2),
        costume="official20", coat_len=0.52, coat_flare=0.12, neck="cravat",
        sleeve=dict(color="#24202a", dark="#12101a", cuff="#fbfaf6", len=0.84, w=0.165), shorts=dict(color="#4a4650", dark="#2a2830", cuff="#4a4650", len=0.92, w=0.125),
        colors=dict(base="#24202a", dark="#100e14", lapel="#34303c", vest="#f4f0e6", shirt="#fbfaf6", collar="#ffffff", tie="#f6f2ea", tie_dark="#c8c0b0", button="#e2b442", pants="#4a4650", moustache="#8a8a90"))
    T["official_bare"] = dict(T["official"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#6a6a70", front=0.12, grow=0.24, style="cap", shine="#9a9aa0"))
    # ---------------- waiter
    T["waiter"] = _mk(
        "gentleman", seed=212.3, build="slim", torso_w=0.62, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shoulder=(0.24, 0.50), leg=1.34, eye_y=0.030, brow="stroke", brow_th=0.052, mouth="smile",
        moustache=True, moustache_style="handlebar", tache_scale=0.8, cheeks="#eaa08a", smirk_side=1,
        hat_style="hair20", hair20=dict(kind="slick", part=0.0), hat_tilt=0.0, hat_colors=dict(light="#4a4048", base="#241c22", dark="#0e0a0e", shine="#8a7a86"), hair=dict(color="#241c22", front=0, grow=0),
        costume="waiter20", chain=False,
        sleeve=dict(color="#fbfaf6", dark="#d8d0c4", cuff="#fbfaf6", len=0.84, w=0.145), shorts=dict(color="#22202a", dark="#100e16", cuff="#22202a", len=0.92, w=0.115),
        boots=dict(color="#16141a", cuff="#16141a", h=0.07, toe=0.15),
        colors=dict(base="#fbfaf6", vest="#1c1a22", shirt="#fbfaf6", collar="#ffffff", tie="#16141a", tie_dark="#08070a", apron="#fbfaf6", apron_d="#c8c0b0", pants="#22202a", moustache="#241c22", moustache_l="#5a4a52"))
    # ---------------- Parisians
    T["lady20"] = _mk(
        "lady", seed=213.6, costume="bustle20", hat_style="bighat7", hat_colors=dict(light="#f6e6d0", base="#e0c4a0", dark="#a8885a", ribbon="#3a6a8a", rose="#e0586a", rose2="#f6b0b8", plume="#fbf6f0", plume_d="#d0c4cc"),
        hair=dict(color="#6a3a22", front=0.1, grow=0.24), skirt_flare=0.30,
        sleeve=dict(color="#2e6a8a", dark="#1a4058", cuff="#ffffff", len=0.84, w=0.150),
        colors=dict(base="#fbf6f0", blouse_d="#e0d4d0", jacket="#2e6a8a", trim="#f0dcb0", skirt="#3a7a9a", skirt_d="#1e4a66", belt="#1e3a50", cameo="#f0b0a0", pants="#3a7a9a"))
    T["gent20"] = _mk(
        "gentleman", seed=214.2, build="regular", torso_w=0.86, torso_h=1.02, shift_pow=1.1, leg=1.32, eye_y=0.020, brow="stroke", brow_th=0.054, mouth="smirk", moustache=True, moustache_style="handlebar", tache_scale=0.9,
        cheeks="#eaa08c", hat_style="tophat7", hat_tilt=-3.0, hat_colors=dict(light="#6a6068", base="#322e38", dark="#18161c", shine="#b0a8b8", band="#18141c", brim="#26222c"), hair=dict(color="#5a3a26", front=0.07, grow=0.2),
        costume="frock7", coat_len=0.46, neck="cravat", chain=True, flower="#e86a7a", vest_buttons=5,
        sleeve=dict(color="#6a4a3a", dark="#3e2a1e", cuff="#f6f2ea", len=0.84, w=0.160), shorts=dict(color="#8a8478", dark="#5a564e", cuff="#8a8478", len=0.92, w=0.120),
        colors=dict(base="#6a4a3a", dark="#3a2418", lapel="#523626", vest="#e8d8a8", vest_b="#7a5a2a", shirt="#fbfaf6", collar="#ffffff", tie="#c8a038", tie_dark="#8a6e1e", button="#2a1a12", pants="#8a8478", moustache="#5a3a26"))
    T["gent20_bare"] = dict(T["gent20"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#5a3a26", front=0.12, grow=0.24, style="cap", shine="#8a6a4a"))
    T["child20"] = _mk(
        "kid1", seed=215.8, hat_style="sailor", hat_tilt=-6.0, hat_colors=dict(light="#ffffff", base="#f3f1ea", dark="#c8c4ba", band="#2a4a8a", gold="#e3c04f"),
        hair=dict(color="#7a4a2a", front=0.08, grow=0.18), costume="sailor", cheeks="#f4a090",
        colors=dict(base="#fbfaf6", navy="#2a4a8a", navy_l="#5a7ab8", button="#e2b442", star="#e2b442", kerchief="#c8322a", kerchief_d="#8a1e18", pants="#2a4a8a"),
        sleeve=dict(color="#fbfaf6", dark="#d8d0c4", cuff="#2a4a8a", len=0.6, w=0.14), shorts=dict(color="#2a4a8a", dark="#16264e", cuff="#2a4a8a", len=0.55, w=0.13))
    return T


_SAILOR_FALLBACK = None


# ============================================================================= canvases (feet-relative, D units); measured by test_cast20.py canvas
CANVAS20 = {
    "eiffel": (-1.6875, -3.6875, 1.6875, 0.1875),
    "eiffel_old": (-1.3750, -3.5625, 1.3750, 0.1875),
    "maupassant": (-1.5000, -3.5625, 1.5000, 0.1875),
    "painter20": (-1.3750, -3.6250, 1.3750, 0.1875),
    "composer20": (-1.3125, -3.5000, 1.3125, 0.1875),
    "architect20": (-1.3750, -4.0000, 1.3750, 0.1875),
    "poet20": (-1.3125, -3.5000, 1.3125, 0.1875),
    "riveter_tongs": (-2.4375, -3.4375, 2.4375, 0.1875),
    "riveter_hammer": (-2.1875, -4.0000, 2.1875, 0.1875),
    "riveter_forge": (-2.2500, -3.3125, 2.2500, 0.1875),
    "telegraphist": (-1.8125, -3.7500, 1.8125, 0.1875),
    "officer": (-1.3750, -3.7500, 1.3750, 0.1875),
    "official": (-1.3750, -3.9375, 1.3750, 0.1875),
    "waiter": (-1.3125, -3.5000, 1.3125, 0.1875),
    "lady20": (-1.5625, -3.6875, 1.5625, 0.3750),
    "gent20": (-1.3750, -4.0000, 1.3750, 0.1875),
    "child20": (-1.1250, -2.5625, 1.1250, 0.1875),
}
for _n in ('eiffel', 'eiffel_old', 'architect20', 'official', 'gent20'):
    CANVAS20[_n + '_bare'] = CANVAS20[_n]


STORY20, STORY20_META = {}, {}


# expression sets per character: label -> pose keys (head only; used by the sheet and as the API list)
EXPRS20 = {
    "eiffel": {"calm": dict(expr="neutral"), "determined": dict(expr="determined"), "proud": dict(expr="proud"), "worried": dict(expr="worried", pitch=0.2, fx=["sweat"], head_roll=4), "sly": dict(expr="sly", head_roll=-4, gaze=(0.7, 0.0))},
    "eiffel_old": {"worried": dict(expr="worried", pitch=0.2, fx=["sweat"], head_roll=4), "determined": dict(expr="determined", pitch=-0.2), "proud": dict(expr="proud"), "calm": dict(expr="neutral")},
    "maupassant": {"sneer": dict(expr="sneer", pitch=-0.25, head_roll=6), "laughing": dict(expr="laughing20"), "smug": dict(expr="smug", mouth="flat", gaze=(0.7, 0.0), pitch=-0.1), "shocked": dict(expr="shocked"),
                   "blissful": dict(expr="blissful"), "avoid": dict(expr="avoid", yaw=-0.7, pitch=-0.25)},
    "painter20": {"outraged": dict(expr="outraged"), "laughing": dict(expr="laughing20"), "sneering": dict(expr="sneer")},
    "composer20": {"outraged": dict(expr="outraged"), "laughing": dict(expr="laughing20"), "sneering": dict(expr="sneer")},
    "architect20": {"outraged": dict(expr="outraged"), "laughing": dict(expr="laughing20"), "sneering": dict(expr="sneer")},
    "poet20": {"outraged": dict(expr="outraged"), "laughing": dict(expr="laughing20"), "sneering": dict(expr="sneer")},
    "riveter_tongs": {"working": dict(expr="working"), "cheering": dict(expr="cheer")},
    "riveter_hammer": {"working": dict(expr="working"), "cheering": dict(expr="cheer")},
    "riveter_forge": {"working": dict(expr="working"), "cheering": dict(expr="cheer")},
    "telegraphist": {"focused": dict(expr="determined"), "listening": dict(expr="neutral", gaze=(0.0, 0.5)), "relieved": dict(expr="happy")},
    "officer": {"stern": dict(expr="stern"), "neutral": dict(expr="neutral"), "proud": dict(expr="proud")},
    "official": {"neutral": dict(expr="neutral"), "stern": dict(expr="stern"), "smiling": dict(expr="happy")},
    "waiter": {"neutral": dict(expr="neutral"), "smile": dict(expr="happy"), "alarmed": dict(expr="shocked")},
    "lady20": {"smile": dict(expr="happy"), "neutral": dict(expr="neutral"), "amazed": dict(expr="shocked")},
    "gent20": {"smug": dict(expr="smug"), "neutral": dict(expr="neutral"), "amazed": dict(expr="shocked")},
    "child20": {"happy": dict(expr="happy"), "amazed": dict(expr="shocked"), "neutral": dict(expr="neutral")},
}


def _story():
    S, M = {}, {}

    def add(name, cast, pose, note, lipsync=False):
        S[name] = (cast, pose)
        M[name] = dict(note=note)
        if lipsync:
            M[name]["lipsync"] = True

    def arm(x, y, **kw):
        return dict(hand=(x, y), **kw)
    FOLD_R, FOLD_L = dict(hand=(-0.40, 0.92), bend=0.9, layer="top"), dict(hand=(0.40, 0.96), bend=0.9, layer="top")
    # ---------------- Eiffel
    add("eiffel_calm", "eiffel", dict(yaw=0.25, expr="neutral", arm_r="down", arm_l="down"), "standing, calm")
    add("eiffel_blueprint", "eiffel", dict(yaw=0.35, expr="determined", arm_r=arm(0.72, 0.62, bend=-0.3, stretch=1.2), prop_r=dict(type="blueprint", angle=-30), arm_l="hip"),
        "holding the rolled blueprint out, determined")
    add("eiffel_blueprint_chest", "eiffel", dict(yaw=0.25, expr="proud", arm_r=arm(0.20, 0.92, bend=0.8, layer="top"), prop_r=dict(type="blueprint", angle=-60, scale=1.0), arm_l=arm(-0.30, 1.0, bend=0.8)),
        "blueprint clutched to the chest, proud smile")
    add("eiffel_giant_rivet", "eiffel", dict(yaw=0.40, expr="proud", pitch=-0.2, arm_r=arm(0.80, 0.30, bend=-0.4, stretch=1.2), prop_r=dict(type="giant_rivet", angle=-35), arm_l="hip", legs="wide"),
        "GIANT RIVET held up (the rivet that holds the tower), proud smile")
    add("eiffel_giant_rivet_show", "eiffel", dict(yaw=0.45, expr="determined", arm_r=arm(0.84, 0.70, bend=-0.3, stretch=1.25), prop_r=dict(type="giant_rivet", angle=-8, scale=1.2), arm_l=arm(-0.4, 0.95, bend=0.6)),
        "showing the giant rivet at chest height")
    add("eiffel_hammer", "eiffel", dict(yaw=0.40, expr="sly", arm_r=arm(0.60, 0.26, bend=-0.5, stretch=1.2), prop_r=dict(type="rivet_hammer", angle=-55, scale=0.9), arm_l="hip", legs="wide"),
        "rivet hammer raised, sly grin")
    add("eiffel_rivet_pinch", "eiffel", dict(yaw=0.40, pitch=0.1, expr="determined", arm_r=arm(0.62, 0.78, bend=-0.3), prop_r=dict(type="rivet20", angle=-10, scale=1.0), arm_l="hip"),
        "inspecting an ordinary rivet in the fingers")
    add("eiffel_worried", "eiffel", dict(yaw=0.30, pitch=0.2, expr="worried", fx=["sweat"], arm_r="chin", arm_l=arm(-0.3, 0.98, bend=0.7), head_roll=4),
        "worried, hand to the chin")
    add("eiffel_sly_hammer_down", "eiffel", dict(yaw=0.35, expr="sly", arm_r=arm(0.50, 0.95, bend=0.5), prop_r=dict(type="hammer20", angle=20), arm_l="hip", legs="wide"),
        "sly grin, small hammer in hand, thumbing at his critics")
    add("eiffel_hat_off", "eiffel", dict(hat_off=1, yaw=0.30, expr="worried", pitch=0.2, arm_r=arm(0.50, 0.90, bend=0.5), prop_r="bowler_held", arm_l="down"),
        "bowler in hand, bare head, worried")
    add("eiffel_point_up", "eiffel", dict(yaw=0.40, pitch=-0.35, expr="determined", arm_r=arm(0.62, -0.80, shape="point", bend=-0.6, stretch=1.3, layer="top"), arm_l="hip", legs="wide"),
        "pointing up at the tower, determined")
    # ---------------- Eiffel old
    add("eiffel_old_worried", "eiffel_old", dict(yaw=0.30, pitch=0.2, expr="worried", lean=5, head_roll=4, arm_r="chin", arm_l=arm(-0.3, 1.0, bend=0.7)), "1909: worried, stooped, hand to the chin")
    add("eiffel_old_point_up", "eiffel_old", dict(yaw=0.40, pitch=-0.3, expr="determined", lean=3, arm_r=arm(0.62, -0.78, shape="point", bend=-0.6, stretch=1.3, layer="top"), arm_l="hip"),
        "1909: pointing up at the antenna, determined")
    add("eiffel_old_proud", "eiffel_old", dict(yaw=0.25, pitch=-0.1, expr="proud", lean=4, arm_r=arm(0.22, 0.90, bend=0.8, layer="top"), arm_l=arm(-0.22, 1.0, bend=0.7)), "1909: proud smile, hand to the lapel")
    add("eiffel_old_calm", "eiffel_old", dict(yaw=0.25, expr="neutral", lean=4, arm_r="down", arm_l="down"), "1909: standing, slightly stooped")
    add("eiffel_old_hat_off", "eiffel_old", dict(hat_off=1, yaw=0.30, expr="proud", lean=4, arm_r=arm(0.50, 0.90, bend=0.5), prop_r="bowler_held", arm_l="down"), "1909: hat in hand, proud")
    # ---------------- Maupassant (the only lip-sync character)
    add("maupassant_idle", "maupassant", dict(yaw=0.25, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"), "standing smug, fists on hips")
    add("maupassant_read_news", "maupassant", dict(yaw=0.35, pitch=0.1, expr="sneer", arm_r=arm(0.55, 0.70, bend=0.4, stretch=1.2), prop_r="news20", arm_l=arm(-0.45, 0.82, bend=0.5), prop_l=None),
        "sneering over the greeked newspaper")
    add("maupassant_quote_point", "maupassant", dict(yaw=0.40, pitch=-0.25, expr="sneer", mouth="talk_b", head_roll=6, arm_r=arm(1.1, 0.0, shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"),
        "QUOTE 1 22.62-25.11 'ถ้าหอนี้ตั้งขึ้นมา ข้าจะไม่มองมันสักครั้ง!': pointing scornfully at the tower; LIP-SYNC with talk_mouth(g)", True)
    add("maupassant_quote_newspaper", "maupassant", dict(yaw=0.30, pitch=-0.35, expr="sneer", mouth="talk_a", head_roll=-5, arm_r=arm(0.55, 0.72, bend=0.4, stretch=1.2), prop_r="news20", arm_l="akimbo", legs="wide"),
        "QUOTE 1 alt: chin up, newspaper in hand; LIP-SYNC", True)
    add("maupassant_quote_chest", "maupassant", dict(yaw=0.30, pitch=-0.5, expr="smug", mouth="talk_a", head_roll=-6, lean=-5, arm_r=arm(0.22, 0.78, bend=0.8, shape="open", layer="top"), arm_l="akimbo", legs="wide"),
        "QUOTE 1 alt: hand on his chest, chin up; LIP-SYNC", True)
    add("maupassant_laugh_quote", "maupassant", dict(yaw=0.30, pitch=-0.6, expr="laughing20", mouth="talk_b", fx=["tears"], head_roll=-9, lean=-8, t=0.3, squash=(1.03, 0.97),
                                                      arm_r=arm(0.50, 1.0, bend=0.9, shape="open"), arm_l=arm(-0.56, 0.98, bend=0.9, shape="open"), legs="wide"),
        "QUOTE 2 37.12-40.67 'ฮ่าฮ่าฮ่า เห็นมั้ย หอของไอ้ช่างหมุด อีกหน่อยก็เป็นเศษเหล็ก!': belly laugh, eyes squeezed; LIP-SYNC + bounce (squash 1.03,0.97 <-> 0.99,1.01 at 3 Hz)", True)
    add("maupassant_laugh_thumb", "maupassant", dict(yaw=0.30, pitch=-0.5, expr="laughing20", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.3, squash=(1.02, 0.98),
                                                      arm_r=arm(0.52, 1.0, bend=0.9, shape="open"), arm_l=arm(-0.62, 0.24, shape="point", bend=0.6, stretch=1.2, layer="top"), legs="wide"),
        "laughing, thumb jerked over his shoulder (far arm, hand back over the shoulder, point shape); LIP-SYNC for quote 2 or hold the laughing mouth", True)
    add("maupassant_laugh_thumb_silent", "maupassant", dict(yaw=0.30, pitch=-0.5, expr="laughing20", fx=["tears"], head_roll=-8, lean=-6, t=0.3, squash=(1.02, 0.98),
                                                             arm_r=arm(0.52, 1.0, bend=0.9, shape="open"), arm_l=arm(-0.62, 0.24, shape="point", bend=0.6, stretch=1.2, layer="top"), legs="wide"),
        "same, the expression's own laughing mouth (no lip-sync)")
    add("maupassant_laugh_belly", "maupassant", dict(yaw=0.20, pitch=-0.8, expr="laughing20", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.03, 0.97),
                                                      arm_r=arm(0.50, 1.02, bend=0.9, shape="open"), arm_l=arm(-0.54, 1.0, bend=0.9, shape="open"), legs="wide"),
        "belly laugh, hands on the belly, mouth = expression grin")
    add("maupassant_smug_wine", "maupassant", dict(yaw=0.35, expr="smug", mouth="flat", arm_r=arm(0.66, 0.62, bend=-0.1), prop_r=dict(type="wine_glass", scale=1.0), arm_l="akimbo", legs="wide"),
        "smug, wine glass raised")
    add("maupassant_write", "maupassant", dict(yaw=0.45, pitch=0.2, expr="sneer", arm_r=arm(0.72, 0.84, bend=-0.2), prop_r=dict(type="quill", angle=60), arm_l=arm(-0.3, 0.92, bend=0.7), prop_l="sheet20"),
        "writing with the quill")
    add("maupassant_shocked", "maupassant", dict(yaw=0.20, pitch=0.1, expr="shocked", mouth=("open", 0.26, 0.20), fx=["sweat"], squash=(0.98, 1.03), arm_r=arm(0.52, 0.55, bend=0.3, shape="open"), arm_l=arm(-0.52, 0.55, bend=0.3, shape="open")),
        "SHOCKED: ring eyes, jaw hanging, hands up")
    add("maupassant_turn_away", "maupassant", dict(yaw=-0.85, pitch=-0.3, expr="avoid", head_roll=-6, lean=-4, arm_r=FOLD_R, arm_l=FOLD_L, legs="wide"),
        "TURNS AWAY, eyes shut, chin up, arms crossed (faces screen-left, away from the tower on the right)")
    add("maupassant_eat", "maupassant", dict(napkin=1, yaw=0.35, pitch=0.1, expr="blissful", mouth=("open", 0.16, 0.08), arm_r=arm(0.52, 0.66, bend=-0.2), prop_r=dict(type="fork20", angle=-40), bite=1.0,
                                              arm_l=arm(-0.4, 0.98, bend=0.6), prop_l=dict(type="knife20", angle=-10), legs="wide"),
        "ENDING: napkin tucked in the collar, eyes closed in bliss, fork with a bite raised to the mouth, knife in the other hand (animate mouth open / closed chewing)")
    add("maupassant_eat_chew", "maupassant", dict(napkin=1, yaw=0.35, pitch=0.05, expr="blissful", mouth="smile", arm_r=arm(0.50, 0.90, bend=0.3), prop_r=dict(type="fork20", angle=-20), bite=0.0,
                                                   arm_l=arm(-0.4, 0.98, bend=0.6), prop_l=dict(type="knife20", angle=-10), legs="wide", squash=(1.01, 0.99)),
        "ENDING: chewing blissfully, napkin in, fork down")
    add("maupassant_eat_back", "maupassant", dict(napkin=1, yaw=-0.55, pitch=0.0, expr="blissful", mouth="smile", arm_r=arm(0.50, 0.90, bend=0.3), prop_r=dict(type="fork20", angle=-20),
                                                   arm_l=arm(-0.4, 0.98, bend=0.6), prop_l=dict(type="knife20", angle=-10), legs="wide"),
        "ENDING: eating happily with his back to the view (use mirror for either side)")
    # ---------------- artists
    for nm, kw, note in (("painter20", dict(prop_r=dict(type="paintbrush", angle=-70, scale=1.0), prop_l=dict(type="palette", angle=0)), "palette + brush"),
                         ("composer20", dict(), "fist / baton"), ("architect20", dict(prop_r=dict(type="blueprint", angle=-50)), "blueprint"), ("poet20", dict(prop_r=dict(type="quill", angle=-40)), "quill")):
        add(nm + "_outraged", nm, dict(yaw=0.30, pitch=-0.2, expr="outraged", head_roll=-6, arm_r=arm(0.70, -0.30, shape="open", bend=-0.6, stretch=1.3, layer="top") if nm != "painter20" else arm(0.70, -0.20, bend=-0.6, stretch=1.3, layer="top"),
                                      arm_l="akimbo", legs="wide", **kw), "OUTRAGED, fist or hand raised (" + note + ")")
        add(nm + "_laughing", nm, dict(yaw=0.25, pitch=-0.4, expr="laughing20", fx=["tears"], head_roll=-8, t=0.3, squash=(1.02, 0.98),
                                        arm_r=arm(0.50, 1.0, bend=0.9, shape="open"), arm_l=arm(-0.54, 0.98, bend=0.9, shape="open"), legs="wide"), "LAUGHING, hands on the belly (bounce)")
        add(nm + "_sneering", nm, dict(yaw=0.35, pitch=-0.2, expr="sneer", head_roll=5, arm_r=FOLD_R, arm_l=FOLD_L, legs="wide"), "SNEERING, arms folded")
    add("painter20_palette", "painter20", dict(yaw=0.45, expr="sneer", arm_r=arm(0.72, 0.60, bend=-0.3), prop_r=dict(type="paintbrush", angle=-30), arm_l=arm(-0.30, 0.95, bend=0.5), prop_l=dict(type="palette", angle=-8)),
        "holding palette and brush, sneering")
    add("composer20_point", "composer20", dict(yaw=0.40, pitch=-0.2, expr="sneer", arm_r=arm(1.0, 0.10, shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"), "pointing scornfully (screen-right)")
    add("architect20_plan", "architect20", dict(yaw=0.35, expr="sneer", arm_r=arm(0.70, 0.62, bend=-0.2), prop_r=dict(type="blueprint", angle=-20), arm_l="hip"), "holding a rolled plan, sneering")
    add("poet20_quill", "poet20", dict(yaw=0.35, pitch=-0.15, expr="sneer", arm_r=arm(0.62, 0.50, bend=-0.3), prop_r=dict(type="quill", angle=-50), arm_l=arm(-0.3, 0.9, bend=0.6, shape="open")), "quill raised, sneering")
    add("artists_protest_sheet", "architect20", dict(yaw=0.30, expr="outraged", arm_r=arm(0.62, 0.40, bend=-0.3), prop_r="sheet20", arm_l="hip"), "holding the protest letter (greeked, scribbled signatures)")
    # ---------------- workers
    add("riveter_tongs_work", "riveter_tongs", dict(yaw=0.45, pitch=0.1, expr="working", arm_r=arm(0.62, 0.78, bend=-0.3, stretch=1.2), prop_r=dict(type="tongs_rivet", angle=-18), arm_l=arm(-0.1, 0.98, bend=0.6), legs=dict(preset="stand", crouch=0.08)),
        "holding the glowing red rivet in tongs (glow 0..1 pose key flickers it), working")
    add("riveter_tongs_cheer", "riveter_tongs", dict(yaw=0.20, pitch=-0.3, expr="cheer", head_roll=-5, arm_r=arm(0.70, -0.60, shape="open", bend=-0.6, stretch=1.3, layer="top"), arm_l=arm(-0.70, -0.55, shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide"),
        "CHEERING, both arms up")
    add("riveter_tongs_throw", "riveter_tongs", dict(yaw=0.50, pitch=-0.1, expr="working", lean=8, arm_r=arm(0.90, 0.20, bend=-0.4, stretch=1.3), prop_r=dict(type="tongs_rivet", angle=-5), arm_l=arm(-0.1, 0.98, bend=0.6), legs="wide"),
        "tongs held out forward with the glowing rivet, offering it to the riveter")
    add("riveter_hammer_work", "riveter_hammer", dict(yaw=0.45, expr="working", lean=6, arm_r=arm(0.60, -0.40, bend=-0.6, stretch=1.3, layer="top"), prop_r=dict(type="rivet_hammer", angle=-70), arm_l=arm(0.30, 0.90, bend=0.2), legs="wide"),
        "rivet hammer raised over the shoulder, working (animate prop angle -70 -> 10 for the blow)")
    add("riveter_hammer_hit", "riveter_hammer", dict(yaw=0.45, expr="working", lean=12, pitch=0.15, arm_r=arm(0.86, 0.66, bend=-0.2, stretch=1.3), prop_r=dict(type="rivet_hammer", angle=5), arm_l=arm(0.30, 0.90, bend=0.2), legs="wide"),
        "the blow: hammer at the target")
    add("riveter_hammer_cheer", "riveter_hammer", dict(yaw=0.20, pitch=-0.3, expr="cheer", head_roll=5, arm_r=arm(0.72, -0.60, bend=-0.6, stretch=1.3, layer="top", shape="open"), prop_r=dict(type="hammer20", angle=-60),
                                                         arm_l=arm(-0.70, -0.50, shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide"), "CHEERING, hammer in the air")
    add("riveter_forge_work", "riveter_forge", dict(yaw=0.45, pitch=0.25, expr="working", lean=10, arm_r=arm(0.80, 0.98, bend=-0.1, stretch=1.2), prop_r=dict(type="tongs_cold", angle=25), arm_l=arm(0.20, 0.96, bend=0.4),
                                                      legs=dict(preset="stand", crouch=0.10)),
        "heating at the forge: tongs held low and forward into the forge (set art), glow comes from the set; use tongs_rivet with glow for the lifted rivet")
    add("riveter_forge_lift", "riveter_forge", dict(yaw=0.45, pitch=0.1, expr="working", arm_r=arm(0.78, 0.70, bend=-0.3, stretch=1.2), prop_r=dict(type="tongs_rivet", angle=-10), arm_l=arm(0.20, 0.96, bend=0.4)),
        "lifting a glowing rivet out of the forge")
    add("riveter_forge_cheer", "riveter_forge", dict(yaw=0.20, pitch=-0.3, expr="cheer", head_roll=-5, arm_r=arm(0.70, -0.60, shape="open", bend=-0.6, stretch=1.3, layer="top"), arm_l=arm(-0.70, -0.50, shape="open", bend=-0.6, stretch=1.3, layer="top"), legs="wide"),
        "CHEERING, both arms up")
    # ---------------- telegraphist 1909
    add("telegraphist_key", "telegraphist", dict(yaw=0.55, pitch=0.25, expr="determined", lean=8, gaze=(0.5, 0.8), arm_r=arm(0.78, 1.45, bend=0.3, layer="front"), prop_r="morse_key", arm_l=arm(-0.35, 0.96, bend=0.6),
                                                  stool=1, legs=dict(crouch=0.40, spread=0.05)),
        "seated at the desk (stool = chair, the desk is set art), tapping the Morse key (key_press 0..1), headphones on")
    add("telegraphist_listen", "telegraphist", dict(yaw=0.45, pitch=0.1, expr="neutral", head_roll=6, gaze=(0.0, 0.6), arm_r=arm(0.62, 1.40, bend=0.3, layer="front"), prop_r="morse_key", arm_l=arm(0.46, 0.28, bend=0.5, shape="open", layer="top"),
                                                     stool=1, legs=dict(crouch=0.40, spread=0.05)),
        "seated, one hand to the headphone, listening")
    add("telegraphist_stand", "telegraphist", dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing at ease, headphones round his neck line")
    add("telegraphist_cheer", "telegraphist", dict(yaw=0.20, pitch=-0.2, expr="happy", head_roll=-4, arm_r=arm(0.62, -0.50, shape="open", bend=-0.5, stretch=1.3, layer="top"), arm_l="hip", legs="wide"), "relieved, one arm up")
    # ---------------- officer 1909
    add("officer_stern", "officer", dict(yaw=0.30, pitch=-0.15, expr="stern", arm_r=arm(-0.10, 0.95, bend=0.8, layer="top"), arm_l=arm(0.10, 1.00, bend=0.8), legs="stand"), "stern, hands clasped behind-front, chest out")
    add("officer_salute", "officer", dict(yaw=0.40, pitch=-0.1, expr="stern", arm_r=arm(0.42, -0.40, bend=-0.9, shape="open", stretch=1.2, layer="top"), arm_l="down", legs="stand"), "SALUTE: right hand flat to the kepi, stern")
    add("officer_point", "officer", dict(yaw=0.40, expr="stern", arm_r=arm(1.0, 0.20, shape="point", bend=-0.4, stretch=1.3), arm_l="hip", legs="wide"), "pointing an order (screen-right)")
    # ---------------- official 1889
    add("official_doc", "official", dict(yaw=0.30, expr="neutral", arm_r=arm(0.62, 0.72, bend=-0.2, stretch=1.1), prop_r="doc_seal", arm_l="hip"), "holding the sealed document (big red wax seal, greeked)")
    add("official_stern", "official", dict(yaw=0.30, pitch=-0.2, expr="stern", arm_r=arm(0.58, 0.58, bend=-0.2), prop_r="doc_seal", arm_l=arm(-0.3, 0.9, bend=0.6), legs="wide"), "stern, document held up")
    add("official_smile", "official", dict(yaw=0.25, pitch=-0.1, expr="happy", arm_r=arm(0.62, 0.74, bend=-0.2, stretch=1.1), prop_r="doc_seal", arm_l="hip"), "smiling with the document")
    add("official_hat_off", "official", dict(hat_off=1, yaw=0.30, expr="happy", arm_r=arm(0.55, 0.95, bend=0.4), prop_r="tophat_held", arm_l=arm(-0.3, 0.9, bend=0.6), prop_l="doc_seal"), "top hat in one hand, document in the other")
    # ---------------- waiter
    add("waiter_tray", "waiter", dict(yaw=0.35, expr="happy", arm_r=arm(0.62, 0.50, bend=-0.2), prop_r="tray20", arm_l=arm(-0.40, 0.90, bend=0.5), prop_l="towel20"), "tray in one hand (glass + covered dish), towel over the other arm")
    add("waiter_idle", "waiter", dict(yaw=0.25, expr="neutral", arm_r="down", arm_l=arm(-0.35, 0.92, bend=0.5), prop_l="towel20"), "standing, towel on the arm")
    add("waiter_bow", "waiter", dict(yaw=0.40, pitch=0.35, expr="happy", lean=14, arm_r=arm(0.40, 0.90, bend=0.5), arm_l=arm(-0.3, 1.0, bend=0.6), prop_l="towel20"), "a small bow, towel on the arm")
    add("waiter_alarmed", "waiter", dict(yaw=0.30, expr="shocked", fx=["sweat"], arm_r=arm(0.62, 0.50, bend=-0.2), prop_r="tray20", arm_l=arm(-0.4, 0.6, bend=0.3, shape="open")), "alarmed, tray wobbling")
    # ---------------- Parisians
    add("lady_parasol", "lady20", dict(yaw=0.35, expr="happy", arm_r=arm(0.50, 0.80, bend=0.2), prop_r=dict(type="parasol20", angle=-62, scale=0.9), arm_l="down"), "lady strolling with the open parasol on her shoulder, bustle")
    add("lady_amazed", "lady20", dict(yaw=0.25, pitch=-0.3, expr="shocked", arm_r=arm(0.50, 0.80, bend=0.2), prop_r=dict(type="parasol20", angle=-80, scale=0.9), arm_l=arm(-0.2, 0.7, bend=0.6, shape="open", layer="top")), "amazed, hand to the chest")
    add("lady_idle", "lady20", dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing")
    add("gent_cane", "gent20", dict(yaw=0.35, expr="smug", arm_r=arm(0.50, 0.95, bend=0.2), prop_r=dict(type="cane20", angle=70, scale=0.7), arm_l="hip"), "gentleman with top hat and cane")
    add("gent_amazed", "gent20", dict(hat_off=1, yaw=0.25, pitch=-0.3, expr="shocked", arm_r=arm(0.62, 0.30, bend=-0.4), prop_r="tophat_held", arm_l=arm(-0.4, 0.9, bend=0.5), prop_l=dict(type="cane20", angle=75, scale=0.7)), "hat lifted in amazement")
    add("gent_idle", "gent20", dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing")
    add("child_wave", "child20", dict(yaw=0.30, expr="happy", arm_r="wave", arm_l="down"), "child waving")
    add("child_point", "child20", dict(yaw=0.40, pitch=-0.4, expr="shocked", arm_r=arm(0.70, -0.20, shape="point", bend=-0.5, stretch=1.3), arm_l="down"), "child pointing up in wonder")
    add("child_idle", "child20", dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing")
    return S, M


def register():
    if getattr(P, "_cast20_registered", False):
        CE.register_stage()
        if not STORY20:
            s, m = _story()
            STORY20.update(s)
            STORY20_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "figure"):
        _O20[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P.figure = figure
    CE.COSTUMES.update(COSTUMES20)
    CE.HATS.update(HATS20)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS20 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP20)
    P.EXPRESSIONS.update(EXPR20)
    for n, c in _cast_table().items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS20)
    P._cast20_registered = True
    s, m = _story()
    STORY20.update(s)
    STORY20_META.update(m)
    P.STORY.update(STORY20)
    CE.register_stage()


register()
