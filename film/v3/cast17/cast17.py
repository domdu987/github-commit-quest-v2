#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast17.py -- the cast of film 17 (Alphonse Bertillon's card index and the measuring chair, Paris 1882-83) for the v2 puppet,
as an extension module on top of cast10.

    import sys; sys.path.insert(0, ".../v3/cast17"); import cast17     # registers on import (idempotent); chains cast10 .. cast_ext
    import puppet                                                      # the same module object, now with the new members
    cast, pose = cast17.STORY17["bertillon_measuring"]
    f = puppet.figure(cast, pose, "f")                                  # f["anchors"]["calipers_r"] = the jaws
    p = cast17.speak(cast17.STORY17["inspector_pointing_mock"][1], g)   # lip-sync only while talking
    q = cast17.with_expr(pose, "proud")                                 # one of the 7 named expressions

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  jacket17 (patched / plain working jackets, thief + prisoners), cape17 (uniform7 tunic + a gendarme's cape),
                       sash17 (frock7 coat + the prefect's tricolour sash), inspector17 (uniform7 double-breasted, brass buttons)
    cast_ext.HATS      none new (tophat7, kepi7, flatcap, derby, beret7, bare7 are reused)
    puppet._SHAPES     "three" (index, middle and ring finger up), "fist"
and wraps puppet helpers on top of cast10's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (seat17, flush17)
    _face       pince-nez, narrow beard, grey side-whiskers, stubble, red flush
    _moustache  "curl17": the inspector's big waxed moustache with up-curled tips
    _hand       finger shapes "three", "fist"
    _prop       calipers, card, pen, ledger
    figure      the measuring chair / a bench under a seated figure (pose seat17)
New cast: bertillon, inspector17 (the CAST key of the chief inspector: "inspector" is cast8's), prefect, dupont, gendarme_a, gendarme_b,
prisoner_a, prisoner_b, prisoner_c.   cast17.KEY maps the short story names to the CAST keys.
STORY17 / STORY17_META: story poses.  EXPR17: the 7 named expressions.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
No text appears on any drawing (cards and the ledger carry pictures only).

Command line (QA):  python3 test_cast17.py        sheet.jpg (lineup, every pose, expressions, props), canvas + robustness
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
import cast7 as C7      # noqa: E402
import cast6 as C6      # noqa: E402
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW17 = ("bertillon", "inspector17", "prefect", "dupont", "gendarme_a", "gendarme_b", "prisoner_a", "prisoner_b", "prisoner_c")
KEY = {"bertillon": "bertillon", "inspector": "inspector17", "prefect": "prefect", "dupont": "dupont", "gendarme_a": "gendarme_a",
       "gendarme_b": "gendarme_b", "prisoner_a": "prisoner_a", "prisoner_b": "prisoner_b", "prisoner_c": "prisoner_c"}
MAIN17 = ("bertillon", "inspector17", "prefect", "dupont")           # the members with the 7 named expressions
TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_O17 = {}
_POSE17 = {"flush": 0.0, "seat": None}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours (period palette that reads on terracotta / ochre / honey wood)
STEEL = dict(light="#dfe6ea", base="#9aa6b0", dark="#5a6672", deep="#343c46")
BRASS = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
WOODP = dict(light="#c8884c", base="#8e5a30", dark="#573418")        # chair wood (darker than the honey floor)
CARD = dict(base="#ecdcae", dark="#c6b27c", edge="#a8945e", tab="#b8402e", photo="#8a7a6a", photo_d="#4a3e36")
LEDGER = dict(cover="#7a2630", dark="#4a141c", light="#a0434c", corner="#3c1a14", page="#e6d8b0", ribbon="#2f5f8a")
TRICOLOUR = ("#2f56a8", "#efe9d8", "#c8352e")


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _lin(k, name, c0, c1, c2, x0, y0, x1, y1):
    return C10._lin(k, name, c0, c1, c2, x0, y0, x1, y1)


# ============================================================================= props (own local frames, +x = along the grip direction)
CALIPER_TIP = 0.86        # fixed jaw
CARD_LEN, CARD_W = 0.50, 0.36
PEN_TIP = 0.52
LEDGER_LEN, LEDGER_W = 0.70, 0.54


def _calipers_body(k):
    """sliding steel calipers (the clerk's measuring instrument): a graduated beam from x -0.12 to 0.86, a fixed jaw at the far
    end pointing +y, a sliding jaw with a brass thumbscrew at x 0.46, tick marks (no figures)."""
    g = _lin(k, "cb", STEEL["light"], STEEL["base"], STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    # fixed jaw (far end)
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.24 L0.835,0.27 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink))
    # sliding jaw + thumbscrew
    o.append('<path d="M0.40,-0.050 L0.52,-0.050 L0.52,0.034 L0.52,0.034 L0.52,0.22 L0.485,0.25 L0.46,0.034 L0.40,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (k.c(STEEL["light"]), k.ink))
    o.append('<circle cx="0.46" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M0.44,-0.085 L0.48,-0.065" stroke="%s" stroke-width="0.008"/>' % k.c(BRASS["dark"]))
    return "".join(o)


GINGER = dict(hair="#c4601f", hair_d="#8e3e12", skin="#f3d2b4", cheek="#e68a7a", stub="#5a3a2e", scarf="#b8322c", jacket="#6a4a30", glass="#5f9a84", glass_l="#cfe8dc")


def _sp(cx, cy, s, d):
    """path data in head units (x right, y down, origin = head centre, unit = s): letters stay, number pairs are scaled and moved."""
    t = d.replace(",", " ").split(); out = []; nums = []; rel = False
    for w in t:
        if w.isalpha():
            out.append(w); rel = w.islower()
        else:
            nums.append(float(w))
            if len(nums) == 2:
                out.append("%.4f,%.4f" % ((0 if rel else cx) + nums[0] * s, (0 if rel else cy) + nums[1] * s)); nums = []
    return " ".join(out)


def _dupont_front(k, cx, cy, s):
    """Dupont bare-headed, full face, in upright card coordinates (x right, y down), centre (cx, cy), head half-width s: ginger hair, ruddy cheeks, stubble dots, ears, red neckerchief."""
    G = GINGER; c = k.c; ink = k.ink; sw = 0.006; o = []
    o.append('<path d="%s" fill="%s"/>' % (_sp(cx, cy, s, "M -1.5 1.7 L 1.5 1.7 L 1.25 1.05 L -1.25 1.05 Z"), c(G["jacket"])))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_sp(cx, cy, s, "M -0.85 0.9 L 0.85 0.9 L 0 1.75 Z"), c(G["scarf"]), ink, sw))
    for sd in (-1, 1):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (cx + sd * s, cy + 0.05 * s, 0.22 * s, 0.32 * s, c(G["skin"]), ink, sw))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.007"/>' % (cx, cy, 0.88 * s, 1.08 * s, c(G["skin"]), ink))
    for sd in (-1, 1):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.8"/>' % (cx + sd * 0.5 * s, cy + 0.28 * s, 0.24 * s, c(G["cheek"])))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.007" stroke-linejoin="round"/>'
             % (_sp(cx, cy, s, "M -0.92 -0.1 Q -1.15 -1.15 -0.1 -1.35 Q 0.6 -1.5 0.95 -0.7 Q 0.9 -0.05 0.75 -0.5 Q 0.1 -0.6 -0.45 -0.45 Q -0.7 -0.25 -0.92 -0.1 Z"), c(G["hair"]), ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.007" stroke-linecap="round"/>' % (_sp(cx, cy, s, "M -0.3 -1.2 q 0.2 0.25 0.1 0.4 M 0.2 -1.28 q 0.25 0.2 0.1 0.4"), c(G["hair_d"])))
    for sd in (-1, 1):
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (cx + sd * 0.36 * s, cy - 0.12 * s, 0.09 * s, ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (_sp(cx, cy, s, "M 0 -0.05 l -0.08 0.38 l 0.14 0.02"), ink, sw))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (_sp(cx, cy, s, "M -0.22 0.62 q 0.22 0.1 0.44 0"), ink, sw))
    o.append('<g fill="%s">' % c(G["stub"]))
    for i in range(26):
        a = _hash(7, i); b = _hash(9, i)
        x = (a - 0.5) * 1.5; y = 0.38 + b * 0.62
        if (x / 0.82) ** 2 + ((y - 0.1) / 1.0) ** 2 > 1.0 or (abs(x) < 0.2 and 0.5 < y < 0.75):
            continue
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f"/>' % (cx + x * s, cy + y * s, 0.055 * s))
    o.append('</g>')
    return "".join(o)


def _dupont_profile(k, cx, cy, s):
    """Dupont bare-headed, a true profile facing right: ginger hair with a back tuft, one ear, nose, stubble, red neckerchief."""
    G = GINGER; c = k.c; ink = k.ink; sw = 0.006; o = []
    o.append('<path d="%s" fill="%s"/>' % (_sp(cx, cy, s, "M -1.5 1.7 L 1.3 1.7 L 1.05 1.05 L -1.1 1.05 Z"), c(G["jacket"])))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_sp(cx, cy, s, "M -0.7 0.95 L 0.6 0.95 L 0.5 1.5 L -0.7 1.5 Z"), c(G["scarf"]), ink, sw))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.007" stroke-linejoin="round"/>'
             % (_sp(cx, cy, s, "M -0.85 -0.3 Q -0.95 -1.15 0 -1.2 Q 0.55 -1.0 0.8 -0.5 L 0.78 -0.2 L 1.12 0.12 Q 1.02 0.26 0.82 0.34 Q 0.8 0.44 0.74 0.6 Q 0.55 0.88 0.2 1.1 Q -0.35 1.0 -0.78 0.8 Z"), c(G["skin"]), ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.8"/>' % (cx + 0.35 * s, cy + 0.3 * s, 0.22 * s, c(G["cheek"])))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.007" stroke-linejoin="round"/>'
             % (_sp(cx, cy, s, "M -0.9 0.2 Q -1.2 -1.3 -0.1 -1.4 Q 0.7 -1.3 0.78 -0.55 Q 0.7 -0.25 0.2 -0.5 Q -0.3 -0.15 -0.3 0.2 Q -0.3 0.3 -0.6 0.1 Z"), c(G["hair"]), ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.007"/>' % (cx - 0.12 * s, cy + 0.12 * s, 0.26 * s, 0.4 * s, c(G["skin"]), ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.005" stroke-linecap="round"/>' % (_sp(cx, cy, s, "M -0.1 -0.02 q 0.1 0.14 0 0.34"), ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (cx + 0.56 * s, cy - 0.1 * s, 0.09 * s, ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (_sp(cx, cy, s, "M 0.62 0.62 q 0.14 0.06 0.22 0"), ink, sw))
    o.append('<g fill="%s">' % c(G["stub"]))
    for i in range(16):
        a = _hash(5, i); b = _hash(3, i)
        x = 0.05 + a * 0.62; y = 0.35 + b * 0.55
        if y > 0.4 + 0.5 * (1 - x) + 0.35:
            continue
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f"/>' % (cx + x * s, cy + y * s, 0.055 * s))
    o.append('</g>')
    return "".join(o)


def _bottle_icon(k, cx, cy, h):
    """an EMPTY glass bottle, upright, outline glass with a pale fill and a highlight; no label, no text. centre (cx, cy), height h (upright card coordinates)."""
    G = GINGER; c = k.c; w = h * 0.30; nw = w * 0.36
    top, bt = cy - h / 2, cy + h / 2; sh = cy - h * 0.12; r = w * 0.4
    path = ("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (cx - nw, top, cx + nw, top, cx + nw, cy - h * 0.2, cx + nw, sh, cx + w, sh + h * 0.08, cx + w, bt - r, cx + w, bt, cx + w - r, bt,
               cx - w + r, bt, cx - w, bt, cx - w, bt - r, cx - w, sh + h * 0.08, cx - nw, sh, cx - nw, cy - h * 0.2))
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (path, c(G["glass_l"]), c(G["glass"]), h * 0.055)]
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>' % (cx - nw * 1.25, cy - h / 2 - h * 0.05, nw * 2.5, h * 0.07, h * 0.02, c(G["glass"]), k.ink, h * 0.02))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" opacity="0.9"/>' % (cx - w * 0.55, cy + h * 0.12, cx - w * 0.55, cy + h * 0.38, h * 0.045))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.8"/>' % (cx - w * 0.9, cy + h * 0.46, cx + w * 0.9, cy + h * 0.46, c(G["glass"]), h * 0.03))
    return "".join(o)


def _card_body(k):
    """the HERO card as a prop (portrait; raised with angle -90 it stands upright): top tab, a framed name panel with an empty bottle (no text), two portraits of
    Dupont bare-headed (full face, true profile with an ear), a fingerprint and greeked rows.  Drawn in upright card coordinates (x right, y down) and
    mapped onto the prop frame (up = +x, right = +y), so heads stand up when the card is raised."""
    hw = CARD_W / 2; top, bot = -(0.02 + CARD_LEN), -0.02
    o = ['<g transform="matrix(0 1 -1 0 0 0)">']
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (-hw, top, CARD_W, CARD_LEN, k.c(CARD["base"]), k.ink))
    o.append('<rect x="%.3f" y="%.3f" width="0.075" height="0.07" fill="%s" stroke="%s" stroke-width="0.012"/>' % (hw - 0.095, top - 0.045, k.c(CARD["tab"]), k.ink))
    o.append('<rect x="%.3f" y="%.3f" width="0.22" height="0.115" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (-hw + 0.02, top + 0.02, k.c("#f6ecd0"), k.ink))
    o.append(_bottle_icon(k, -hw + 0.02 + 0.11, top + 0.02 + 0.0575, 0.095))
    o.append('<rect x="%.3f" y="%.3f" width="0.075" height="0.115" fill="none" stroke="%s" stroke-width="0.008" stroke-dasharray="0.012 0.010"/>' % (hw - 0.095 - 0.0, top + 0.02, k.c(CARD["dark"])))
    for j, xc in enumerate((-hw * 0.5, hw * 0.5)):
        px0, py0, pw, ph = xc - 0.077, top + 0.15, 0.154, 0.185
        o.append('<g><rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (px0, py0, pw, ph, k.c("#8aa0b4"), k.ink))
        o.append('<clipPath id="%s_pc%d"><rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.008"/></clipPath><g clip-path="url(#%s_pc%d)">' % (k.uid, j, px0, py0, pw, ph, k.uid, j))
        o.append((_dupont_front if j == 0 else _dupont_profile)(k, xc, py0 + 0.092, 0.050))
        o.append('</g></g>')
    fx, fy = -hw + 0.07, bot - 0.075
    for r in (0.040, 0.030, 0.020, 0.010):
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="none" stroke="%s" stroke-width="0.007"/>' % (fx, fy, r * 1.1, r * 0.85, k.ink))
    for i in range(3):
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (-hw + 0.15, bot - 0.105 + i * 0.03, hw - 0.04 - 0.03 * (i % 2), bot - 0.105 + i * 0.03, k.c(CARD["dark"])))
    o.append('</g>')
    return "".join(o)


def _pen_body(k):
    """a dip pen along +x: a quill feather at the back, a red-brown holder with a brass band, a steel nib with an ink drop."""
    o = ['<path d="M-0.02,0 Q-0.16,-0.095 -0.32,-0.070 Q-0.26,-0.030 -0.20,-0.016 Q-0.26,0.020 -0.31,0.050 Q-0.14,0.060 -0.02,0.006 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
         % (k.c("#f0e8d4"), k.ink)]
    o.append('<path d="M-0.02,0 Q-0.17,-0.012 -0.30,-0.014" stroke="%s" stroke-width="0.008" fill="none"/>' % k.c("#a8a090"))
    o.append('<path d="M-0.04,-0.016 L0.40,-0.016 L0.40,0.016 L-0.04,0.016 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#7a3a26"), k.ink))
    o.append('<path d="M0.02,-0.006 L0.36,-0.006" stroke="%s" stroke-width="0.006" opacity="0.7"/>' % k.c("#c88a62"))
    o.append('<path d="M0.38,-0.018 L0.43,-0.018 L0.43,0.018 L0.38,0.018 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M0.43,-0.012 L0.52,0 L0.43,0.012 Z" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (k.c(STEEL["base"]), k.ink))
    o.append('<circle cx="0.535" cy="0.012" r="0.010" fill="%s"/>' % k.c("#1c2230"))
    return "".join(o)


def _ledger_body(k):
    """a big bound register, long axis along +x (height), spine on the -y side: maroon cloth, dark leather corners, a brass band
    clasp, cream page edges at the far end, a blue ribbon marker hanging out."""
    x0, x1, hw = 0.04, 0.04 + LEDGER_LEN, LEDGER_W / 2
    g = _lin(k, "lg", LEDGER["light"], LEDGER["cover"], LEDGER["dark"], 0, -hw, 0, hw)
    o = ['<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
         % (x0, -hw, x1, -hw, x1, hw, x0, hw, g, k.ink)]
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.012"/>'
             % (x0, -hw, x1, -hw, x1, -hw + 0.085, x0, -hw + 0.085, k.c(LEDGER["dark"]), k.ink))
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x1 - 0.002, -hw + 0.10, x1 - 0.002, hw - 0.02, k.c(LEDGER["page"])))
    for (cx, cy, sx, sy) in ((x0, hw, 1, -1), (x1, hw, -1, -1)):
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (cx, cy, cx + sx * 0.12, cy, cx, cy + sy * 0.12, k.c(LEDGER["corner"]), k.ink))
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.010"/>'
             % (x0 + 0.24, -hw * 0.45, x0 + 0.46, -hw * 0.45, x0 + 0.46, hw * 0.45, x0 + 0.24, hw * 0.45, k.c(LEDGER["light"]), k.ink))
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x0 + 0.35, -hw * 0.45, x0 + 0.35, hw * 0.45, k.c(BRASS["base"])))
    o.append('<path d="M%.3f,%.3f q0.05,0.08 0.14,0.14 l0.03,-0.03 q-0.06,-0.04 -0.08,-0.12" fill="%s" stroke="%s" stroke-width="0.008"/>'
             % (x1 - 0.06, hw - 0.02, k.c(LEDGER["ribbon"]), k.ink))
    return "".join(o)


NEW_PROPS17 = ("calipers", "card", "pen", "ledger")
NEW_TIP17 = {"calipers": CALIPER_TIP, "card": 0.02 + CARD_LEN, "pen": PEN_TIP, "ledger": 0.04 + LEDGER_LEN}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS17:
        return _O17["_prop"](k, kind, H, ang, sc)
    C8 = C10.C8
    key = C8._side_key()
    an = C8._POSE8["an"]
    body = {"calipers": _calipers_body, "card": _card_body, "pen": _pen_body, "ledger": _ledger_body}[kind](k)
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    ext = {"calipers": ((-0.12, -0.08), (0.88, -0.08), (0.88, 0.27), (0.46, 0.25)),
           "card": ((0.02, -0.18), (0.52, -0.18), (0.52, 0.18), (0.02, 0.18)),
           "pen": ((-0.32, -0.07), (0.54, 0.0), (-0.31, 0.05)),
           "ledger": ((0.04, -0.27), (0.74, -0.27), (0.74, 0.27), (0.04, 0.27))}[kind]
    for (x, y) in ext:
        px, py = _rot(x * sc, y * sc, ang)
        k.ext.append((H[0] + px, H[1] + py, 0.03))
    tx, ty = _rot(NEW_TIP17[kind] * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    if kind == "calipers":
        jx, jy = _rot(0.67 * sc, 0.22 * sc, ang)        # between the jaws, at their tips
        an["calipers_" + key] = (H[0] + jx, H[1] + jy)
    elif kind == "card":
        cx, cy = _rot((0.02 + CARD_LEN / 2) * sc, 0.0, ang)
        an["card_" + key] = (H[0] + cx, H[1] + cy)
    elif kind == "pen":
        an["nib_" + key] = tip
    else:
        cx, cy = _rot((0.04 + LEDGER_LEN / 2) * sc, 0.0, ang)
        an["ledger_" + key] = (H[0] + cx, H[1] + cy)
    return o, tip


def _standalone(uid, body, ink, tint):
    k = _ctx(uid, ink, tint)
    b = body(k)
    return '<g id="%s_prop"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), b)


def calipers_svg(uid="ca", ink=P.INK, tint=None):
    """the steel calipers alone, beam along +x from (0, 0) (hand position), jaws toward +y."""
    return _standalone(uid, _calipers_body, ink, tint)


def card_svg(uid="cd", ink=P.INK, tint=None):
    """the record card alone, long axis along +x from (0, 0), width +-0.18."""
    return _standalone(uid, _card_body, ink, tint)


def pen_svg(uid="pn", ink=P.INK, tint=None):
    """the dip pen alone along +x (hand at (0, 0), nib at x 0.52, quill at -0.32)."""
    return _standalone(uid, _pen_body, ink, tint)


def ledger_svg(uid="lg", ink=P.INK, tint=None):
    """the ledger alone, long axis along +x from (0, 0), width +-0.27, spine on the -y side."""
    return _standalone(uid, _ledger_body, ink, tint)


# ============================================================================= hands: three fingers up, fist
def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    if shape not in ("three", "fist"):
        return _O17["_hand"](k, H, dirv, shape, hr, fold)
    ux, uy = dirv
    g = hr / P.HAND_R
    o = []
    if shape == "three":
        fl = 0.125 * g * fold
        d = ""
        for a in (-24.0, 0.0, 24.0):
            vx, vy = _rot(ux, uy, a)
            d += "M%.4f,%.4f L%.4f,%.4f" % (H[0], H[1], H[0] + vx * fl, H[1] + vy * fl)
            k.ext.append((H[0] + vx * fl, H[1] + vy * fl, 0.02))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, k.ink, 0.036 * g))
        # thumb and little finger tucked: two short stubs
        for a in (-82.0, 80.0):
            vx, vy = _rot(ux, uy, a)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
                     % (H[0], H[1], H[0] + vx * 0.055 * g, H[1] + vy * 0.055 * g, k.ink, 0.032 * g))
    else:
        hr = hr * 1.30
        k.ext.append((H[0], H[1], hr + 0.01))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (H[0], H[1], hr, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#b7a9b3" opacity="0.7" transform="rotate(-35 %.4f %.4f)"/>'
             % (H[0] - 0.34 * hr, H[1] - 0.40 * hr, 0.15 * hr, 0.095 * hr, H[0] - 0.34 * hr, H[1] - 0.40 * hr))
    k.ext.append((H[0], H[1], hr + 0.01))
    return "".join(o)


# ============================================================================= face: pince-nez, narrow beard, whiskers, stubble, flush, curled moustache
def _pincenez(k, C, L, blink):
    """oval steel-rimmed lenses pinched on the nose (a spring bridge, two pads), a black silk cord running from the screen-right
    lens round the ear to the lapel."""
    xL, xR, ey, sL, sR = L["xL"], L["xR"], L["ey"], L["sL"], L["sR"]
    half = (xR - xL) / 2.0
    rx = min(0.100, half - 0.012)
    o = []
    for x, s in ((xL, sL), (xR, sR)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" fill-opacity="0.28" stroke="%s" stroke-width="%.4f"/>'
                 % (x, ey, rx * s, 0.092 * s, k.c("#cfe4f0"), k.ink, 0.018 * s))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.011" stroke-linecap="round" opacity="0.9"/>' % (x - 0.050 * s, ey - 0.030 * s, x - 0.022 * s, ey - 0.060 * s))
    mid = (xL + xR) / 2
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (xL + rx * sL, ey - 0.012, mid, ey - 0.062, xR - rx * sR, ey - 0.012, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
             % (mid - 0.012, ey + 0.004, mid - 0.020, ey + 0.050, mid + 0.012, ey + 0.004, mid + 0.020, ey + 0.050, k.ink))
    # cord
    ox = xR + rx * sR
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
             % (ox, ey - 0.005, ox + 0.05, ey + 0.02, 0.43, ey + 0.10, 0.47, ey + 0.30, 0.44, ey + 0.52, k.ink))
    k.ext.append((0.46, ey + 0.52, 0.02))
    return "".join(o)


def _beard_narrow(k, C, L):
    """a narrow dark beard: a chin tuft that tapers to a point below the chin, joined by a thin strap along the jaw (clipped to the head)."""
    B = C["beard17"]
    mx, my = L["mx"], L["my"]
    col = k.c(B.get("color", "#2a1e1a"))
    top = my + 0.045
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (mx - 0.125, top, mx - 0.150, top + 0.09, mx - 0.12, 0.50, mx - 0.03, 0.62,
            mx + 0.02, 0.69, mx + 0.08, 0.58, mx + 0.125, 0.50,
            mx + 0.160, top + 0.08, mx + 0.125, top))
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, col, k.ink)]
    o.append('<path d="M%.4f,%.4f q0.01,0.06 0.0,0.12 M%.4f,%.4f q0.01,0.07 0.0,0.14 M%.4f,%.4f q0.0,0.06 0.01,0.12" stroke="%s" stroke-width="0.010" fill="none" stroke-linecap="round" opacity="0.8"/>'
             % (mx - 0.07, top + 0.10, mx, top + 0.10, mx + 0.07, top + 0.10, k.c(B.get("light", "#5a463c"))))
    # jaw strap (thin, along the head edge)
    o.append('<g clip-path="url(#%s_hc)">' % k.uid)
    for sd in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s"/>'
                 % (sd * 0.50, -0.02, sd * 0.50, 0.40, sd * 0.20, 0.62, sd * 0.18, 0.52, sd * 0.42, 0.36, sd * 0.44, -0.02, col))
    o.append('</g>')
    k.ext.append((mx + 0.02, 0.69, 0.02))
    return "".join(o)


def _whiskers(k, C, L, yaw):
    """grey side-whiskers: from the temples down the cheeks to the jaw, thick at the bottom, drawn on top of the head fill."""
    W = C["whiskers17"]
    col = k.c(W.get("color", "#b4b0b6"))
    hi = k.c(W.get("light", "#dcd8de"))
    dx = 0.10 * yaw
    o = ['<g clip-path="url(#%s_hc)">' % k.uid]
    for sd, sc in ((-1, L["sL"]), (1, L["sR"])):
        s = 0.55 + 0.45 * sc
        d = ("M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
             % (dx + sd * 0.60, -0.18, dx + sd * 0.60, 0.62, dx + sd * 0.30 * s, 0.62, dx + sd * 0.22 * s, 0.42,
                dx + sd * 0.26 * s, 0.30, dx + sd * 0.32 * s, 0.16, dx + sd * 0.36 * s, 0.02, dx + sd * 0.36 * s, -0.16))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, col, k.ink))
        hs = "".join("M%.4f,%.4f q%.4f,0.07 %.4f,0.14 " % (dx + sd * x * s, y, sd * 0.012, sd * 0.01) for (x, y) in ((0.38, -0.05), (0.42, 0.14), (0.34, 0.24), (0.30, 0.38)))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>' % (hs, hi))
    o.append('</g>')
    return "".join(o)


def _stubble(k, C, L):
    """five o'clock shadow: a soft grey shade over the jaw and upper lip plus dense tiny dots (not freckles: only the lower face)."""
    S = C["stubble17"]
    col = k.c(S.get("color", "#3a2e2e"))
    mx, my = L["mx"], L["my"]
    o = ['<g clip-path="url(#%s_hc)">' % k.uid]
    gid = "%s_stb" % k.uid
    k.defs.append('<radialGradient id="%s" cx="0.5" cy="0.45" r="0.5"><stop offset="0" stop-color="%s" stop-opacity="%.2f"/><stop offset="0.65" stop-color="%s" stop-opacity="%.2f"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (gid, k.c("#5a4a44"), 0.34 * S.get("opacity", 0.55) / 0.55, k.c("#5a4a44"), 0.22 * S.get("opacity", 0.55) / 0.55, k.c("#5a4a44")))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.66" ry="0.50" fill="url(#%s)"/>' % (mx, my + 0.20, gid))
    o.append('<g fill="%s" opacity="%.2f">' % (col, S.get("opacity", 0.55)))
    for i in range(130):
        a = _hash(C["seed"], i)
        b = _hash(C["seed"], i + 100)
        x = mx + (a - 0.5) * 0.84
        y = my - 0.13 + b * 0.62
        if abs(x - mx) < 0.09 and abs(y - my) < 0.04:
            continue
        if ((x - mx) / 0.46) ** 2 + ((y - (my + 0.12)) / 0.40) ** 2 > 1.0:
            continue
        o.append('<circle cx="%.4f" cy="%.4f" r="0.0055"/>' % (x, y))
    o.append('</g></g>')
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O17["_face"](k, C, P_, white)
    if C is None or not C.get("_cast17"):
        return svg, L
    under, over = [], []
    fl = _POSE17["flush"]
    if fl > 0.02:
        under.append('<g clip-path="url(#%s_hc)"><ellipse cx="%.4f" cy="0.04" rx="0.52" ry="0.56" fill="%s" opacity="%.3f"/>'
                     '<ellipse cx="%.4f" cy="%.4f" rx="0.34" ry="0.07" fill="%s" opacity="%.3f"/></g>'
                     % (k.uid, L["mx"] * 0.5, k.c("#d82a1e"), 0.78 * fl, (L["xL"] + L["xR"]) / 2, L["ey"] - 0.28, k.c("#c02c22"), 0.45 * fl))
    if C.get("whiskers17"):
        under.append(_whiskers(k, C, L, P_["yaw"]))
    if C.get("stubble17"):
        under.append(_stubble(k, C, L))
    if C.get("beard17"):
        under.append(_beard_narrow(k, C, L))
    if C.get("pincenez17") and P_["blink"] < 2:
        over.append(_pincenez(k, C, L, P_["blink"]))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "curl17":
        return _O17["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#3a2a22")
    sh = C["colors"].get("moustache_l", "#7a5e4c")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + (y * 0.72 - 0.006) * s)
    o = []
    for sd in (-1, 1):
        pts = [Q(0.0, -0.060), Q(sd * 0.12, -0.100), Q(sd * 0.25, -0.088), Q(sd * 0.36, -0.075), Q(sd * 0.45, -0.130), Q(sd * 0.520, -0.230),
               Q(sd * 0.500, -0.300), Q(sd * 0.455, -0.265), Q(sd * 0.440, -0.190), Q(sd * 0.390, -0.075), Q(sd * 0.300, 0.020),
               Q(sd * 0.180, 0.055), Q(sd * 0.060, 0.040), Q(0.0, 0.025)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round" opacity="0.9"/>'
                 % (Q(sd * 0.05, -0.02) + Q(sd * 0.24, -0.04) + Q(sd * 0.40, -0.08) + Q(sd * 0.48, -0.15) + Q(sd * 0.495, -0.27) + (k.c(sh),)))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>'
                 % (Q(sd * 0.10, 0.02) + Q(sd * 0.22, 0.03) + Q(sd * 0.30, -0.01) + (k.c(sh),)))
        k.ext.append(Q(sd * 0.52, -0.300) + (0.03,))
    return "".join(o)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE17["flush"] = _f(g("flush17"), 0.0, 0.0, 1.0)
    return _O17["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _patch(k, X, x, y, w, h, col, dark, rot=0.0):
    """a sewn-on square patch with dashed stitches just inside its edge."""
    pts = [X(x - w / 2, y - h / 2), X(x + w / 2, y - h / 2 + 0.004), X(x + w / 2 - 0.004, y + h / 2), X(x - w / 2 + 0.004, y + h / 2 - 0.006)]
    o = [_poly(k, pts, k.c(col), 0.010)]
    inner = [(p[0] + (x - p[0]) * 0.20, p[1] + (y - p[1]) * 0.20) for p in pts]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.007" stroke-dasharray="0.014 0.011" stroke-linecap="round" stroke-linejoin="round"/>'
             % (_poly_d(inner), k.c(dark)))
    return "".join(o)


def _cos_jacket17(k, C, m):
    """a working man's jacket: open fronts over a shirt (and a neckerchief), an optional waistcoat, two flapped pockets, buttons and
    sewn-on patches (C patches = (x, y, w, h, colour) tuples); a short skirt below the waist; trousers in colors pants."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    o.append(_poly(k, [X(-0.17, 0.38), X(0.17, 0.38), X(0.13, yb + 0.02), X(-0.13, yb + 0.02)], k.c(col["shirt"]), 0.0, "none"))
    if col.get("vest"):
        o.append(_poly(k, [X(-0.13, 0.52), X(0.13, 0.52), X(0.12, yb + 0.03), X(-0.12, yb + 0.03)], k.c(col["vest"]), 0.012))
        for y in (0.66, 0.78, 0.90):
            if y < yb - 0.04:
                o.append(_circ(X(0.0, y), 0.016, k.c(col.get("button", "#2a2222")), k, 0.006))
    if col.get("scarf"):
        o.append(_poly(k, [X(-0.15, 0.40), X(0.15, 0.40), X(0.07, 0.56), X(0.0, 0.62), X(-0.07, 0.56)], k.c(col["scarf"]), 0.014))
        o.append(_ln([X(-0.06, 0.47), X(0.0, 0.52), X(0.06, 0.47)], k.c(col.get("scarf_d", "#7a2a22")), 0.010))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.15, 0.64), X(s * 0.15, yb + 0.06), X(s * 0.95, yb + 0.06), X(s * 0.95, 0.30), X(s * 0.30, 0.30)], "url(#%s_tg)" % k.uid, 0.0, "none"))
        o.append(_poly(k, [X(s * 0.15, 0.38), X(s * 0.31, 0.43), X(s * 0.42, 0.53), X(s * 0.30, 0.56), X(s * 0.17, 0.66)], k.c(col["lapel"]), 0.014))
        o.append(_ln([X(s * 0.17, 0.66), X(s * 0.15, yb + 0.06)], k.ink, 0.018))
    for y in (0.78, 0.94):
        if y < yb - 0.06:
            o.append(_circ(X(0.11, y), 0.019, k.c(col.get("button", "#2a2222")), k, 0.007))
    for s in (-1, 1):
        x = s * 0.31
        o.append(_poly(k, [X(x - 0.10, yb - 0.16), X(x + 0.10, yb - 0.16), X(x + 0.095, yb - 0.04), X(x - 0.095, yb - 0.04)], k.c(col["pocket"]), 0.012))
        o.append(_ln([X(x - 0.10, yb - 0.145), X(x + 0.10, yb - 0.145)], k.c(col["dark"]), 0.012))
    for (px, py, pw, ph, pc) in C.get("patches", ()):
        o.append(_patch(k, X, px, py, pw, ph, pc, col["dark"]))
    inside = "".join(o)
    ov = ""
    sk = C.get("jacket_len", 0.14)
    if sk > 0.02:
        yt = yb - 0.02
        ov = C2._skirt(k, "jk", X, yt, hw * 0.99, yB + sk, hw + C.get("jacket_flare", 0.06), "url(#%s_tg)" % k.uid, sw=0.024,
                       folds=((-0.20, yt + 0.06, -0.24, yB + sk - 0.03), (0.20, yt + 0.06, 0.24, yB + sk - 0.03)), fold_col=k.c(col["dark"]))
        ov += _ln([X(0.0, yt), X(0.02, yB + sk)], k.ink, 0.014)
        for (px, py, pw, ph, pc) in C.get("patches_low", ()):
            ov += _patch(k, X, px, py, pw, ph, pc, col["dark"])
    return inside, "", ov


def _cos_inspector17(k, C, m):
    """the chief inspector's tunic: uniform7 (two rows of brass buttons, flapped pockets, belt) plus gold collar braid and piping
    down the front edges."""
    inside, behind, over = C7._cos_uniform7(k, C, m)
    X = _X(m)
    col = C["colors"]
    br = k.c(col.get("braid", "#e2b442"))
    o = []
    for s in (-1, 1):
        o.append(_ln([X(s * 0.14, 0.44), X(s * 0.30, 0.50)], br, 0.022))
    return inside + "".join(o), behind, over


def _cos_cape17(k, C, m):
    """a gendarme: uniform7 tunic (buttons, belt) under a short shoulder cape (colors cape, cape_l lining), the long cape flaring
    out behind the arms to knee height."""
    inside, behind, over = C7._cos_uniform7(k, C, m)
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    g = _lin(k, "cpg", P._shade(col["cape"], 1.14), col["cape"], P._shade(col["cape"], 0.70), -hw - 0.3, 0, hw + 0.3, 0)
    hem = yB + C.get("cape_len", 0.46)
    wb = hw + C.get("cape_flare", 0.34)
    back = [X(-0.30, 0.40), X(-hw - 0.10, 0.50), X(-wb, hem - 0.08), X(-wb * 0.55, hem + 0.02), X(0.0, hem + 0.05), X(wb * 0.55, hem + 0.02), X(wb, hem - 0.08), X(hw + 0.10, 0.50), X(0.30, 0.40)]
    bk = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(back), g, k.ink)
    bk += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.8"/>' % (
        X(-wb + 0.02, hem - 0.10) + X(0, hem - 0.02) + X(wb - 0.02, hem - 0.10) + (k.c(col["cape_l"]),))
    for fx_ in (-0.5, -0.2, 0.2, 0.5):
        bk += '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (
            X(fx_ * hw, 0.80) + X(fx_ * wb * 0.95, hem - 0.30) + X(fx_ * wb, hem - 0.05) + (k.c(P._shade(col["cape"], 0.6)),))
    for p in (back[2], back[6], back[4]):
        k.ext.append((p[0], p[1], 0.04))
    ov = []
    for s in (-1, 1):
        fl = [X(s * 0.12, 0.38), X(s * 0.30, 0.37), X(s * (hw + 0.12), 0.52), X(s * (hw + 0.16), 0.84), X(s * 0.70 * hw, 0.92), X(s * 0.28, 0.86), X(s * 0.17, 0.62)]
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_closed(fl), g, k.ink))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
                  % (X(s * 0.13, 0.40) + X(s * 0.16, 0.62) + X(s * 0.27, 0.85) + (k.c(col["cape_l"]),)))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>'
                  % (X(s * 0.40, 0.55) + X(s * (hw + 0.02), 0.70) + X(s * (hw + 0.06), 0.84) + (k.c(P._shade(col["cape"], 0.6)),)))
        for p in (fl[3], fl[4]):
            k.ext.append((p[0], p[1], 0.04))
    cx, cy = X(0.0, 0.43)
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.032" fill="%s" stroke="%s" stroke-width="0.012"/>' % (cx, cy, k.c(col.get("button", "#e2b442")), k.ink))
    return inside + "".join(ov), bk + behind, over


def _cos_sash17(k, C, m):
    """the prefect: black frock coat (frock7) with the tricolour sash of office -- blue, white and red running from the screen-right
    shoulder across the chest to a knot with gold fringe at the left hip."""
    inside, behind, over = C7._cos_frock7(k, C, m)
    X = _X(m)
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    p0 = X(hw * 0.78, 0.36)
    p1 = X(-hw * 0.62, yB - 0.04)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    wd = 0.15
    o = []
    for i, c in enumerate(TRICOLOUR):
        a = -wd / 2 + wd * i / 3.0
        b = -wd / 2 + wd * (i + 1) / 3.0
        pts = [(p0[0] + nx * a - ux * 0.10, p0[1] + ny * a - uy * 0.10), (p0[0] + nx * b - ux * 0.10, p0[1] + ny * b - uy * 0.10),
               (p1[0] + nx * b, p1[1] + ny * b), (p1[0] + nx * a, p1[1] + ny * a)]
        o.append('<path d="%s" fill="%s" stroke="none"/>' % (_poly_d(pts), k.c(c)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (p0[0] + nx * wd / 2 - ux * 0.10, p0[1] + ny * wd / 2 - uy * 0.10, p1[0] + nx * wd / 2, p1[1] + ny * wd / 2,
                p0[0] - nx * wd / 2 - ux * 0.10, p0[1] - ny * wd / 2 - uy * 0.10, p1[0] - nx * wd / 2, p1[1] - ny * wd / 2, k.ink))
    kx, ky = p1
    ov = []
    for j in range(7):
        f = -0.10 + 0.033 * j
        e = (kx + nx * f * 1.1 + ux * 0.16, ky + ny * f * 1.1 + uy * 0.16 + 0.04)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (kx + nx * f, ky + ny * f, e[0], e[1], k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (kx + nx * f, ky + ny * f, e[0], e[1], k.c(BRASS["base"])))
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.055" fill="%s" stroke="%s" stroke-width="0.014"/>' % (kx, ky, k.c(TRICOLOUR[2]), k.ink))
    ov.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (kx, ky, k.c(TRICOLOUR[1]), k.ink))
    k.ext.append((kx + ux * 0.16, ky + uy * 0.16 + 0.05, 0.05))
    return inside + "".join(o), behind, over + "".join(ov)


COSTUMES17 = {"jacket17": _cos_jacket17, "cape17": _cos_cape17, "sash17": _cos_sash17, "inspector17": _cos_inspector17}


# ============================================================================= seats (figure level)
def _chair_svg(k, cx, seat_y, floor_y, head_y, w=1.34):
    """the measuring chair: honey-brown oak, a tall slatted back with an iron head rest at head height, wide flat arms, a plank
    seat and turned legs.  Drawn behind the figure.  Returns (svg, bbox)."""
    g = _lin(k, "chw", WOODP["light"], WOODP["base"], WOODP["dark"], cx - w / 2, 0, cx + w / 2, 0)
    gd = k.c(WOODP["dark"])
    o = []
    top = head_y - 0.52
    for sd in (-1, 1):
        x = cx + sd * (w / 2 - 0.06)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.100" stroke-linecap="round"/>' % (x, top, x, seat_y, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.078" stroke-linecap="round"/>' % (x, top, x, seat_y, k.c(WOODP["base"])))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>' % (x - sd * 0.016, top + 0.05, x - sd * 0.016, seat_y - 0.04, k.c(WOODP["light"])))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.150" rx="0.04" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx - w / 2 + 0.01, top - 0.07, w - 0.02, g, k.ink))
    for i in range(3):
        y = top + 0.30 + i * 0.34
        if y < seat_y - 0.2:
            o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.130" fill="%s" stroke="%s" stroke-width="0.016"/>' % (cx - w / 2 + 0.10, y, w - 0.20, g, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (cx, head_y + 0.50, cx, head_y + 1.2, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (cx, head_y + 0.50, cx, head_y + 1.2, k.c(STEEL["base"])))
    o.append('<rect x="%.4f" y="%.4f" width="0.640" height="0.760" rx="0.200" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx - 0.32, head_y - 0.16, k.c("#7a3a2e"), k.ink))
    # back legs hidden; seat slab + front legs
    for sd in (-1, 1):
        x = cx + sd * (w / 2 - 0.10)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.100" stroke-linecap="round"/>' % (x, seat_y, x, floor_y, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % (x, seat_y, x, floor_y, k.c(WOODP["base"])))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>' % (x - sd * 0.014, seat_y + 0.10, x - sd * 0.014, floor_y - 0.04, k.c(WOODP["light"])))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.040" fill="%s" stroke="%s" stroke-width="0.014"/>' % (cx - w / 2 + 0.12, floor_y - 0.36, w - 0.24, gd, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.160" rx="0.030" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx - w / 2 - 0.04, seat_y, w + 0.08, g, k.ink))
    # arm rests
    for sd in (-1, 1):
        x = cx + sd * (w / 2 + 0.01)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % (x, seat_y - 0.58, x, seat_y, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>' % (x, seat_y - 0.58, x, seat_y, k.c(WOODP["base"])))
        o.append('<rect x="%.4f" y="%.4f" width="0.300" height="0.090" rx="0.040" fill="%s" stroke="%s" stroke-width="0.018"/>' % (x - 0.15, seat_y - 0.64, g, k.ink))
    bb = (cx - w / 2 - 0.20, top - 0.10, cx + w / 2 + 0.20, floor_y + 0.04)
    return "".join(o), bb


def _bench_svg(k, cx, seat_y, floor_y, w=2.0):
    """a plain prisoners' bench: one thick plank on two trestle ends.  Drawn behind the figure."""
    g = _lin(k, "bnw", WOODP["light"], WOODP["base"], WOODP["dark"], cx - w / 2, 0, cx + w / 2, 0)
    o = []
    for sd in (-1, 1):
        x = cx + sd * (w / 2 - 0.16)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.110" stroke-linecap="round" stroke-linejoin="round"/>' % (x - 0.07, floor_y, x, seat_y, x + 0.07, floor_y, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.080" stroke-linecap="round" stroke-linejoin="round"/>' % (x - 0.07, floor_y, x, seat_y, x + 0.07, floor_y, k.c(WOODP["base"])))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.130" rx="0.030" fill="%s" stroke="%s" stroke-width="0.022"/>' % (cx - w / 2, seat_y, w, g, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (cx - w / 2 + 0.1, seat_y + 0.03, cx + w / 2 - 0.1, seat_y + 0.03, k.c(WOODP["light"])))
    return "".join(o), (cx - w / 2 - 0.02, seat_y - 0.02, cx + w / 2 + 0.02, floor_y + 0.04)


def figure(cast_name, pose=None, uid="p"):
    f = _O17["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    seat = pose.get("seat17")
    if seat not in ("chair", "bench"):
        return f
    an = dict(f["anchors"])
    k = P._Ctx(uid + "s", P.INK, None)
    cx = an["hip"][0]
    seat_y = an["hip"][1] + 0.02 + C17_SEAT_DY
    if seat == "chair":
        s, bb = _chair_svg(k, cx, seat_y, f["feet_y"] + 0.02, an["head"][1])
        an["seat"] = (cx, seat_y)
    else:
        s, bb = _bench_svg(k, cx, seat_y, f["feet_y"] + 0.02, _f(pose.get("seat_w"), 2.0, 0.8, 4.0))
        an["seat"] = (cx, seat_y)
    b = list(f["bbox"])
    b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + s + f["svg"], bbox=tuple(b), anchors=an)


C17_SEAT_DY = 0.0


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast17=True)
_BOOT = dict(h=0.08, toe=0.15)
NEW_CAST17 = {
    # Alphonse Bertillon, 29: thin and tall young clerk, serious.  Black frock coat, dove-blue waistcoat, white collar, dark red tie,
    # parted dark-brown hair, a narrow dark beard, a neat pencil moustache and steel pince-nez on a cord
    "bertillon": dict(
        _FLAGS, build="slim", seed=17.3,
        torso_w=0.60, torso_h=1.02, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.23, 0.50), arm=0.78, hip_x=0.15, leg=1.42, stance=0.06, wide=0.24, limb_w=0.054,
        eye_y=0.030, brow="stroke", brow_th=0.052, mouth="dash", moustache=False, pencil_moustache=True, smirk_side=1,
        beard17=dict(color="#2c211c", light="#5a463c"), pincenez17=True,
        hat="newsboy", hat_style="bare7", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#000000", base="#000000", dark="#000000"),
        hair=dict(color="#352720", front=0.12, grow=0.25, style="cap", shine="#6a5446"),
        costume="frock7", coat_len=0.50, coat_flare=0.03, neck="tie", chain=False, vest_buttons=4, double=False,
        sleeve=dict(color="#2c2a34", dark="#16141a", cuff="#f0ebe0", len=0.84, w=0.140),
        shorts=dict(color="#3c3842", dark="#26222c", cuff="#3c3842", len=0.90, w=0.11),
        boots=dict(color="#1c1618", cuff="#1c1618", h=0.07, toe=0.14),
        colors=dict(base="#2c2a34", dark="#16141a", lapel="#403d4a", vest="#566a8a", vest_b="#d8d0b0", shirt="#f4efe4", collar="#fffdf6",
                    tie="#8a2a34", tie_dark="#5a1822", button="#16141a", pants="#3c3842", moustache="#2c211c", moustache_l="#5a463c"),
    ),
    # the chief inspector (the mocker): stout, red-cheeked, huge waxed moustache with curled tips, dark-blue kepi and double-breasted
    # tunic with two rows of brass buttons, gold braid
    "inspector17": dict(
        _FLAGS, build="stout", seed=88.4,
        torso_w=1.34, torso_h=1.16, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.44, 0.44), arm=0.78, hip_x=0.19, leg=1.22, stance=0.07, wide=0.30, limb_w=0.070,
        eye_y=0.000, brow="stroke", brow_th=0.080, mouth="frown", moustache=True, moustache_style="curl17", tache_scale=1.3, smirk_side=1,
        cheeks="#ee7a66", chins=True,
        hat="newsboy", hat_style="kepi7", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#4a62a0", base="#2c4580", dark="#16244c", shine="#8aa2d8", band="#c8402e", piping="#e2b442", visor="#16141a"),
        hair=dict(color="#6a5648", front=0.06, grow=0.20),
        costume="inspector17", double=True, tunic_len=0.20,
        sleeve=dict(color="#2c4580", dark="#16244c", cuff="#e2b442", len=0.84, w=0.200),
        shorts=dict(color="#1e2c56", dark="#121a38", cuff="#1e2c56", len=0.90, w=0.16),
        boots=dict(color="#16121a", cuff="#16121a", h=0.08, toe=0.17),
        colors=dict(base="#2c4580", dark="#16244c", pocket="#324c8a", button="#e8bc4a", belt="#2a1c18", patch="#c8402e", pants="#1e2c56",
                    braid="#e2b442", piping="#e2b442", moustache="#2a1e1a", moustache_l="#74604e"),
    ),
    # the prefect: tall top hat, black frock coat with the tricolour sash, grey side-whiskers, grey hair, a gold watch chain
    "prefect": dict(
        _FLAGS, build="regular", seed=51.6,
        torso_w=0.96, torso_h=1.08, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.35, 0.47), arm=0.76, hip_x=0.17, leg=1.40, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.000, brow="stroke", brow_th=0.066, mouth="frown", moustache=False, smirk_side=-1, cheeks="#e89484",
        whiskers17=dict(color="#aeaab2", light="#dcd8e0"),
        hat="newsboy", hat_style="tophat7", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#5a5668", base="#2a2830", dark="#14121a", shine="#a8a4b8", band="#16121a", brim="#24222a"),
        hair=dict(color="#aeaab2", front=0.06, grow=0.22),
        costume="sash17", coat_len=0.54, coat_flare=0.05, neck="cravat", chain=True, vest_buttons=4, double=False,
        sleeve=dict(color="#2c2a32", dark="#16141a", cuff="#efe9da", len=0.84, w=0.165),
        shorts=dict(color="#47434f", dark="#2e2a36", cuff="#47434f", len=0.90, w=0.13),
        boots=dict(color="#16121a", cuff="#16121a", h=0.07, toe=0.15),
        colors=dict(base="#2c2a32", dark="#16141a", lapel="#403c48", vest="#a89c82", vest_b="#e2b442", shirt="#f4efe4", collar="#fffdf6",
                    tie="#2f56a8", tie_dark="#1c3a78", button="#16141a", pants="#47434f"),
    ),
    # Dupont, the scruffy thief: flat cap, a patched brown jacket over a grubby shirt, red neckerchief, stubble, ginger hair
    "dupont": dict(
        _FLAGS, build="regular", seed=63.2,
        torso_w=0.72, torso_h=0.96, profile=CE.PROFILE_ATHLETE, shift_pow=1.05,
        shoulder=(0.28, 0.48), arm=0.74, hip_x=0.16, leg=1.24, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.056, mouth="dash", moustache=False, smirk_side=1, cheeks="#e8907c",
        stubble17=dict(color="#3a2e2e", opacity=0.55),
        hat="newsboy", hat_style="flatcap", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(light="#8a8466", base="#645e46", dark="#403c2c", shine="#aaa486", visor="#4a4634"),
        hair=dict(color="#9a5a2c", front=0.08, grow=0.22),
        costume="jacket17", jacket_len=0.14, jacket_flare=0.07,
        patches=((-0.34, 0.80, 0.22, 0.20, "#5a86b4"), (0.34, 0.98, 0.18, 0.20, "#d0a040")), patches_low=((0.20, 1.20, 0.15, 0.14, "#7a9a6a"),),
        sleeve=dict(color="#7a5a3a", dark="#4a3320", cuff="#6a4c30", len=0.84, w=0.150),
        shorts=dict(color="#4c5a6a", dark="#323c48", cuff="#4c5a6a", len=0.90, w=0.12),
        boots=dict(color="#4a3424", cuff="#4a3424", h=0.09, toe=0.15),
        colors=dict(base="#7a5a3a", dark="#4a3320", lapel="#6a4c30", pocket="#6e5034", button="#2a2222", shirt="#c4bba2", scarf="#b8402e",
                    scarf_d="#7a2a22", pants="#4c5a6a"),
    ),
    # the gendarmes: kepi, tunic and a long cape.  a: navy cape with a red lining, silver buttons, brown moustache.
    # b: tall and thin, grey-green cape with a mustard lining, brass buttons, black handlebar moustache
    "gendarme_a": dict(
        _FLAGS, build="regular", seed=21.5,
        torso_w=0.94, torso_h=1.04, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.34, 0.47), arm=0.76, hip_x=0.17, leg=1.26, stance=0.07, wide=0.28, limb_w=0.062,
        eye_y=0.020, brow="stroke", brow_th=0.064, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.95, smirk_side=-1, cheeks="#e88e7c",
        hat="newsboy", hat_style="kepi7", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#5870aa", base="#34478a", dark="#1c2a5a", shine="#9ab0e0", band="#c8402e", piping="#d8dce6", visor="#16141a"),
        hair=dict(color="#5a3a26", front=0.06, grow=0.20),
        costume="cape17", double=True, tunic_len=0.16, cape_len=0.46, cape_flare=0.34,
        sleeve=dict(color="#3a5090", dark="#1c2a5a", cuff="#d8dce6", len=0.84, w=0.170),
        shorts=dict(color="#222c54", dark="#141a38", cuff="#222c54", len=0.90, w=0.14),
        boots=dict(color="#16121a", cuff="#16121a", h=0.09, toe=0.15),
        colors=dict(base="#3a5090", dark="#1c2a5a", pocket="#405a9c", button="#d8dce6", belt="#2a1c18", patch="#c8402e", pants="#222c54",
                    cape="#2a3a7c", cape_l="#c8402e", moustache="#5a3a26", moustache_l="#8a6446"),
    ),
    "gendarme_b": dict(
        _FLAGS, build="slim", seed=24.9,
        torso_w=0.72, torso_h=1.06, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.28, 0.50), arm=0.78, hip_x=0.17, leg=1.40, stance=0.08, wide=0.30, limb_w=0.060,
        eye_y=0.030, brow="stroke", brow_th=0.062, mouth="frown", moustache=True, moustache_style="handlebar", tache_scale=1.0, smirk_side=1,
        hat="newsboy", hat_style="kepi7", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#6a7e72", base="#4a5c52", dark="#2a3830", shine="#9ab0a2", band="#c8a038", piping="#e2b442", visor="#16141a"),
        hair=dict(color="#2a2222", front=0.07, grow=0.20),
        costume="cape17", double=False, cord="#e2b442", tunic_len=0.20, cape_len=0.50, cape_flare=0.30,
        sleeve=dict(color="#566a5e", dark="#2a3830", cuff="#e2b442", len=0.84, w=0.150),
        shorts=dict(color="#2c3630", dark="#1a221e", cuff="#2c3630", len=0.90, w=0.12),
        boots=dict(color="#16121a", cuff="#16121a", h=0.09, toe=0.15),
        colors=dict(base="#566a5e", dark="#2a3830", pocket="#5c7266", button="#e8bc4a", belt="#2a1c18", patch="#c8a038", pants="#2c3630",
                    cape="#43584f", cape_l="#d0a838", moustache="#2a2222", moustache_l="#6a5a5a"),
    ),
    # waiting prisoners (simple): a thin, pale, in a grey-blue jacket and no hat; b stout in a brown waistcoat and a derby; c in an olive
    # jacket and a navy beret
    "prisoner_a": dict(
        _FLAGS, build="slim", seed=71.1,
        torso_w=0.62, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.74, hip_x=0.15, leg=1.30, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.040, brow="stroke", brow_th=0.048, mouth="dash", moustache=False, smirk_side=-1, cheeks="#e8a090",
        stubble17=dict(color="#3a3030", opacity=0.40),
        hat="newsboy", hat_style="bare7", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#000000", base="#000000", dark="#000000"),
        hair=dict(color="#3e3028", front=0.11, grow=0.24, style="cap", shine="#6a5a4c"),
        costume="jacket17", jacket_len=0.10, jacket_flare=0.05,
        patches=((0.33, 0.80, 0.15, 0.15, "#8a7a62"),), patches_low=(),
        sleeve=dict(color="#6a7a90", dark="#46546a", cuff="#58667c", len=0.84, w=0.140),
        shorts=dict(color="#58504c", dark="#3a3430", cuff="#58504c", len=0.90, w=0.11),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.08, toe=0.14),
        colors=dict(base="#6a7a90", dark="#46546a", lapel="#5a6a80", pocket="#62728a", button="#2a2630", shirt="#b8ae98", pants="#58504c"),
    ),
    "prisoner_b": dict(
        _FLAGS, build="stout", seed=74.6,
        torso_w=1.06, torso_h=1.00, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.40, 0.44), arm=0.74, hip_x=0.17, leg=1.12, stance=0.07, wide=0.28, limb_w=0.066,
        eye_y=0.000, brow="stroke", brow_th=0.064, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.9, smirk_side=-1, cheeks="#e88c78",
        hat="newsboy", hat_style="derby", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#8a6a4e", base="#5c4232", dark="#33241a", shine="#b8906e", band="#1e1410", brim="#4c3628", edge="#a07e60"),
        hair=dict(color="#4a3428", front=0.06, grow=0.20),
        costume="jacket17", jacket_len=0.12, jacket_flare=0.07,
        patches=(), patches_low=(),
        sleeve=dict(color="#6e5a46", dark="#463626", cuff="#5a4636", len=0.84, w=0.180),
        shorts=dict(color="#4a4650", dark="#2e2a36", cuff="#4a4650", len=0.90, w=0.14),
        boots=dict(color="#2e2420", cuff="#2e2420", h=0.09, toe=0.15),
        colors=dict(base="#6e5a46", dark="#463626", lapel="#5e4c3a", pocket="#665240", button="#2a2222", shirt="#cbc2aa", vest="#8a7a4a", pants="#4a4650",
                    moustache="#3a2a20", moustache_l="#6a5242"),
    ),
    "prisoner_c": dict(
        _FLAGS, build="regular", seed=77.9,
        torso_w=0.80, torso_h=0.94, profile=CE.PROFILE_REGULAR, shift_pow=1.05,
        shoulder=(0.30, 0.48), arm=0.72, hip_x=0.16, leg=1.14, stance=0.07, wide=0.27, limb_w=0.060,
        eye_y=0.050, brow="dome", brow_th=0.044, mouth="dash", moustache=False, smirk_side=1, cheeks="#eea294", freckles=True,
        hat="newsboy", hat_style="beret7", hat_tilt=-7.0, ear_pencil=False, beret_side=1,
        hat_colors=dict(light="#5a6a96", base="#38466e", dark="#1e2640", shine="#8a9acc"),
        hair=dict(color="#7a4a28", front=0.08, grow=0.20),
        costume="jacket17", jacket_len=0.12, jacket_flare=0.06,
        patches=((-0.34, 0.92, 0.15, 0.15, "#b08a4a"),), patches_low=(),
        sleeve=dict(color="#6e7650", dark="#444a30", cuff="#5a6242", len=0.84, w=0.150),
        shorts=dict(color="#5a5048", dark="#3a322c", cuff="#5a5048", len=0.90, w=0.12),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.08, toe=0.14),
        colors=dict(base="#6e7650", dark="#444a30", lapel="#5e6644", pocket="#667046", button="#2a2622", shirt="#bcb29a", scarf="#8a5a3a", scarf_d="#5a3a26",
                    pants="#5a5048"),
    ),
}
CANVAS17 = {
    "bertillon": (-1.9375, -4.8125, 1.9375, 0.1250),
    "inspector17": (-2.0625, -4.6875, 2.0625, 0.1250),
    "prefect": (-2.0000, -4.9375, 2.0000, 0.1250),
    "dupont": (-1.9375, -4.5000, 1.9375, 0.1250),
    "gendarme_a": (-2.0000, -4.6250, 2.0000, 0.1250),
    "gendarme_b": (-1.9375, -4.8125, 1.9375, 0.1250),
    "prisoner_a": (-1.9375, -4.5625, 1.9375, 0.1250),
    "prisoner_b": (-2.0000, -4.3750, 2.0000, 0.1250),
    "prisoner_c": (-1.9375, -4.3125, 1.9375, 0.1250),
}

# ============================================================================= expressions (the 7 named faces) and lip-sync helpers
# mouths are CLOSED in every face except laugh and surprised (which are held open shapes); talking only through speak().
EXPR17 = {
    "neutral": dict(expr="neutral"),
    "smirk": dict(expr="smirk"),
    "laugh": dict(expr="laughing", mouth="talk_b", pitch=-0.5),
    "angry": dict(expr="angry", pitch=-0.4),
    "surprised": dict(expr="shocked"),
    "worried": dict(expr="worried"),
    "proud": dict(expr="smug", mouth="smile", pitch=-0.35),
}
OPEN_FACES = ("laugh", "surprised")
_FACEKEYS = ("expr", "mouth", "pitch", "fx", "blink")


def with_expr(pose, name, **extra):
    """a copy of pose with one of the 7 named expressions (EXPR17).  Mouth stays closed except 'laugh' and 'surprised'."""
    p = dict(pose)
    if name == "laugh":
        p["fx"] = list(p.get("fx") or []) + ["tears"]
    p.update(EXPR17.get(name, EXPR17["neutral"]))
    p.update(extra)
    return p


def speak(pose, frame, level=1.0, seed=0, hold=2):
    """the pose with the mouth driven by cast6.talk_mouth(frame, level) -- the ONLY way a mouth opens and closes."""
    return dict(pose, mouth=talk_mouth(frame, level, seed, hold))


def silent(pose):
    """the pose with the mouth shut (flat) -- use between sentences."""
    return dict(pose, mouth="flat")


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="front", stretch=1.1):
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _story():
    S, M = {}, {}
    B, I, F, D, GA, GB = "bertillon", "inspector17", "prefect", "dupont", "gendarme_a", "gendarme_b"
    CALIP = dict(type="calipers", scale=1.0)
    CARDP = dict(type="card", scale=1.0)
    PEN = dict(type="pen", scale=1.0)
    LEDG = dict(type="ledger", scale=1.0)
    # --- Bertillon
    S["bertillon_neutral"] = (B, dict(yaw=0.20, expr="neutral", mouth="flat", arm_r="down", arm_l="down", legs="stand"))
    S["bertillon_measuring"] = (B, dict(yaw=0.50, pitch=0.12, expr="determined", mouth="flat", gaze=(0.8, 0.2), lean=4,
                                        arm_r=dict(hand=(0.88, 0.34), bend=-0.2, stretch=1.0, layer="front"), prop_r=dict(CALIP, angle=-4),
                                        arm_l=dict(hand=(-0.10, 0.95), bend=0.5, layer="front"), legs=dict(preset="step", stride=0.3)))
    S["bertillon_writing"] = (B, dict(yaw=0.40, pitch=0.55, expr="determined", mouth="flat", gaze=(0.3, 0.9), lean=5,
                                      arm_r=dict(hand=(0.66, 1.06), bend=0.3, stretch=1.0, layer="front"), prop_r=dict(PEN, angle=200),
                                      arm_l=dict(hand=(-0.14, 1.06), bend=0.7, stretch=1.0, layer="front"), prop_l=dict(CARDP, angle=-34), legs="stand"))
    S["bertillon_holding_card"] = (B, dict(yaw=0.30, pitch=-0.15, expr="smug", mouth="smile", gaze=(0.5, 0.0),
                                           arm_r=dict(hand=(0.66, 0.08), bend=-0.6, stretch=1.1, layer="front"), prop_r=dict(CARDP, angle=-90),
                                           arm_l=dict(hand=(-0.20, 0.96), bend=0.6, layer="front"), legs="stand"))
    S["bertillon_pointing"] = (B, dict(yaw=0.40, pitch=-0.10, expr="determined", mouth="flat", gaze=(0.9, 0.0),
                                       arm_r=dict(hand=(1.05, 0.18), shape="point", bend=-0.4, stretch=1.3, layer="front"),
                                       arm_l=dict(hand=(-0.62, 1.12), bend=0.5, layer="front"), prop_l=dict(LEDG, angle=-84, scale=0.9), legs="stand"))
    S["bertillon_triumphant"] = (B, dict(yaw=0.20, pitch=-0.55, expr="happy", mouth="smile", head_roll=-5, lean=-4,
                                         arm_r=dict(hand=(0.62, -0.62), bend=-0.7, stretch=1.3, shape="fist", layer="top"),
                                         arm_l="akimbo", legs="wide"))
    S["bertillon_tired"] = (B, dict(yaw=0.15, pitch=0.90, expr="sad", mouth="flat", head_roll=-7, head_dy=0.12, lean=12, squash=(1.0, 0.96),
                                    arm_r=dict(hand=(0.40, 1.34), bend=0.4), arm_l=dict(hand=(-0.26, 1.30), bend=0.4), legs="narrow"))
    # --- the chief inspector
    S["inspector_laughing"] = (I, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                       arm_r=dict(hand=(0.46, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.50, 0.98), bend=0.9, shape="open"), legs="wide"))
    S["inspector_pointing_mock"] = (I, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="flat", head_roll=8,
                                            arm_r=dict(hand=(1.10, 0.12), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    S["inspector_arms_crossed"] = (I, dict(yaw=0.20, pitch=-0.35, expr="smug", mouth="flat", head_roll=-4,
                                           arm_r=dict(hand=(-0.40, 0.84), bend=0.7, layer="front"), arm_l=dict(hand=(0.36, 0.90), bend=0.7, layer="front"), legs="wide"))
    S["inspector_shouting"] = (I, dict(yaw=0.35, pitch=-0.40, expr="shouting", mouth="flat", lean=-4,
                                       arm_r=dict(hand=(0.60, 0.30), shape="open", bend=-0.9, stretch=1.0, layer="top"), arm_l="akimbo", legs="wide"))
    S["inspector_shocked"] = (I, dict(yaw=0.20, pitch=0.10, expr="stunned", mouth=("open", 0.15, 0.20), head_dy=0.03, lean=-5, fx=["sweat"], squash=(1.01, 0.99),
                                      arm_r=dict(hand=(0.80, 0.80), shape="open", bend=0.3), arm_l=dict(hand=(-0.80, 0.80), shape="open", bend=0.3), legs="stand"))
    S["inspector_seated_stiff"] = (I, dict(yaw=0.10, pitch=0.0, expr="stunned", mouth="flat", gaze=(0.0, 0.0), fx=["sweat"], seat17="chair",
                                           arm_r=dict(hand=(0.82, 0.96), bend=0.2, layer="front"), arm_l=dict(hand=(-0.82, 0.96), bend=0.2, layer="front"),
                                           legs=dict(preset="narrow", crouch=0.45, knee_r=0.0, knee_l=0.0)))
    S["inspector_red_faced"] = (I, dict(yaw=0.25, pitch=-0.45, expr="furious", mouth="clench", flush17=1.0, fx=["steam"], t=0.3,
                                        arm_r=dict(hand=(0.60, 1.10), bend=0.5, shape="ball"), arm_l="akimbo", legs="wide"))
    # --- the prefect
    S["prefect_neutral"] = (F, dict(yaw=0.20, pitch=-0.15, expr="neutral", mouth="flat", arm_r="behind", arm_l="behind", legs="stand"))
    S["prefect_finger_up_three"] = (F, dict(yaw=0.30, pitch=-0.30, expr="determined", mouth="flat", lean=-3,
                                            arm_r=dict(hand=(0.62, -0.30), bend=-0.7, stretch=1.2, shape="three", layer="front"),
                                            arm_l=dict(hand=(-0.20, 0.82), bend=0.6, layer="front"), legs="stand"))
    S["prefect_stern"] = (F, dict(yaw=0.15, pitch=-0.45, expr="angry", mouth="flat", arm_r=dict(hand=(0.30, 0.86), bend=0.6, layer="front"),
                                  arm_l=dict(hand=(-0.30, 0.86), bend=0.6, layer="front"), legs="stand"))
    # --- Dupont
    S["dupont_innocent"] = (D, dict(yaw=0.20, pitch=-0.10, expr="worried", mouth="smile", head_roll=-6, gaze=(0.3, -0.3),
                                    arm_r=dict(preset="shrug"), arm_l=dict(preset="shrug"), legs="stand", squash=(1.0, 0.99)))
    S["dupont_held"] = (D, dict(yaw=0.0, pitch=0.2, expr="worried", mouth="flat", head_roll=5,
                                arm_r=dict(hand=(0.96, 0.78), bend=0.0, stretch=1.0, layer="front"), arm_l=dict(hand=(-0.96, 0.78), bend=0.0, stretch=1.0, layer="front"),
                                legs="narrow"))
    S["dupont_sweating"] = (D, dict(yaw=0.20, pitch=0.35, expr="worried", mouth="wavy", sweat=1.0, fx=["sweat"], gaze=(-0.7, 0.2), head_roll=4,
                                    arm_r=dict(hand=(0.08, 0.90), bend=0.8, layer="front"), arm_l=dict(hand=(-0.10, 0.92), bend=0.8, layer="front"), legs="narrow"))
    S["dupont_caught"] = (D, dict(yaw=0.10, pitch=-0.05, expr="shocked", mouth="o", gaze=(0.0, 0.0), head_dy=-0.03,
                                  arm_r=dict(hand=(0.74, 0.56), shape="open", bend=0.2), arm_l=dict(hand=(-0.74, 0.56), shape="open", bend=0.2), legs="stand", squash=(0.99, 1.02)))
    # --- gendarmes
    for c, sfx in ((GA, "_a"), (GB, "_b")):
        S["gendarme_escort" + sfx] = (c, dict(yaw=0.0, expr="determined", mouth="flat", pitch=-0.1,
                                              arm_r=dict(hand=(0.94, 0.78), bend=0.0, stretch=1.0, layer="front"), arm_l="behind", legs="stand"))
        S["gendarme_laughing" + sfx] = (c, dict(yaw=0.20, pitch=-0.7, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-6, t=0.4,
                                                arm_r=dict(hand=(0.30, 0.98), bend=0.9, shape="open"), arm_l=dict(hand=(-0.34, 0.96), bend=0.9, shape="open"), legs="wide"))
        S["gendarme_standing" + sfx] = (c, dict(yaw=0.0, expr="neutral", mouth="flat", arm_r="behind", arm_l="behind", legs="stand"))
    # --- prisoners
    for c, sfx in (("prisoner_a", "_a"), ("prisoner_b", "_b"), ("prisoner_c", "_c")):
        S["prisoner_sitting" + sfx] = (c, dict(yaw=0.15, pitch=0.30, expr="sad" if sfx != "_b" else "unimpressed", mouth="flat", seat17="bench",
                                               arm_r=dict(hand=(0.30, 1.00), bend=0.4), arm_l=dict(hand=(-0.30, 1.00), bend=0.4), legs=dict(preset="narrow", crouch=0.45, knee_r=0.0, knee_l=0.0)))
        S["prisoner_standing" + sfx] = (c, dict(yaw=0.20, pitch=0.15, expr="worried" if sfx == "_a" else "unimpressed", mouth="flat",
                                                arm_r="down", arm_l="down", legs="stand"))
    NOTES = {
        "bertillon_neutral": "serious, standing, arms down",
        "bertillon_measuring": "arm out holding the steel calipers (anchor calipers_r = the jaws between the tips); mirror=True for the ear measuring, standing right of the chair",
        "bertillon_writing": "head down, card in the screen-left hand, pen in the other (anchor nib_r touches the card)",
        "bertillon_holding_card": "card raised beside his head, smug",
        "bertillon_pointing": "pointing (screen-right) with the ledger under the other arm",
        "bertillon_triumphant": "fist up, head back, happy",
        "bertillon_tired": "slumped: head down and dropped, lean, arms hanging",
        "inspector_laughing": "head back, hands on the belly, tears (held open laugh mouth)",
        "inspector_pointing_mock": "pointing and mocking (screen-right), other hand on hip",
        "inspector_arms_crossed": "arms crossed, smug, chin up",
        "inspector_shouting": "one hand cupped at the mouth, shouting eyes, other hand on hip; mouth is driven by speak()",
        "inspector_shocked": "jaw dropped (held open mouth), eyes wide, sweat, open hands out",
        "inspector_seated_stiff": "sitting rigidly in the measuring chair (seat17='chair'), hands on the arms, eyes wide, sweat",
        "inspector_red_faced": "red_faced variant: flush17=1, furious, steam",
        "prefect_neutral": "hands behind the back, chin up",
        "prefect_finger_up_three": "three fingers up (hand shape 'three') = 3 months",
        "prefect_stern": "stern, hands folded at the belly",
        "dupont_innocent": "hands open, shrug, an innocent smile",
        "dupont_held": "arms out low, ready for the gendarmes' grip (hands at +-0.96 D)",
        "dupont_sweating": "sweating, hands wringing at the belt, looking away",
        "dupont_caught": "wide eyes, mouth 'o', open hands",
    }
    OPEN = ("inspector_laughing", "inspector_shocked", "dupont_caught", "gendarme_laughing_a", "gendarme_laughing_b")
    LIP = ("bertillon_pointing", "bertillon_holding_card", "bertillon_neutral", "inspector_pointing_mock", "inspector_shouting",
           "prefect_neutral", "prefect_finger_up_three", "prefect_stern", "dupont_innocent")
    for n in S:
        M[n] = dict(note=NOTES.get(n, n.replace("_", " ")))
        if n in OPEN:
            M[n]["open_mouth"] = True
        if n in LIP:
            M[n]["lipsync"] = True
    return S, M


def hand_for_anchor(cast, pose, arm, anchor, target, it=6):
    """a copy of pose whose arm_<arm> hand is moved until the figure's anchor (e.g. "calipers_r", "nib_r", "card_l"; with mirror=True the r/l of the anchor swap) lies on target (puppet-local D).
    The arm must be a dict with a "hand" entry.  Returns the new pose."""
    p = dict(pose)
    a = dict(p["arm_" + arm])
    sx = -1.0 if p.get("mirror") else 1.0          # anchors come back mirrored; the pose hand is in the unmirrored frame
    for _ in range(it):
        q = dict(p, **{"arm_" + arm: a})
        an = figure(cast, q, "q")["anchors"]
        cur = an[anchor]
        h = a["hand"]
        a["hand"] = (h[0] + sx * (target[0] - cur[0]), h[1] + target[1] - cur[1])
    return dict(p, **{"arm_" + arm: a})


ESCORT_SPACING = 1.30      # distance (D) between a gendarme and the held man for the arm grip
STORY17, STORY17_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast17_registered", False):
        CE.register_stage()
        if not STORY17:
            s, m = _story()
            STORY17.update(s)
            STORY17_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_hand", "figure"):
        _O17[name] = getattr(P, name)
    P._hand = _hand
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P.figure = figure
    P._SHAPES = tuple(P._SHAPES) + tuple(s for s in ("three", "fist") if s not in P._SHAPES)
    CE.COSTUMES.update(COSTUMES17)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS17 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP17)
    for n, c in NEW_CAST17.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS17)
    P._cast17_registered = True
    s, m = _story()
    STORY17.update(s)
    STORY17_META.update(m)
    P.STORY.update(STORY17)
    CE.register_stage()


register()
