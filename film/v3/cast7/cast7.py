#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast7.py -- the cast of film 7 ("the macaroni guy": the Mona Lisa theft, Paris 1911 / Florence 1913) for the v2 puppet,
as an extension module on top of cast6.

    import sys; sys.path.insert(0, ".../v3/cast7"); import cast7      # registers on import (idempotent); imports cast6 .. cast_ext
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast7.STORY7["vincenzo_hide_panel"]
    f = puppet.figure(cast, pose, "v")                                # the panel hidden under the white smock (a bulge)
    w = puppet.figure("vincenzo_smock", cast7.cycle("vincenzo_smock", 0.25, "sneak"), "v")   # one frame of the sneak

Nothing in v2/puppet or v3/cast..cast6 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  overalls7 (cast3 overalls, plaid id fixed), smock7 (work smock / artist smock, the bulge), frock7 (frock coat / lounge suit), uniform7 (kepi
                       uniform tunic), stripe7 (striped sailor shirt), dress7 (Edwardian blouse + long skirt)
    cast_ext.HATS      tophat7, kepi7, beret7, bighat7, bare7 (no hat, hair only)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast6's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (bulge, sweat, lie, panel_grip, panel_side, flip_text)
    _face       goatee, monocle, extra sweat drops (pose key sweat)
    _moustache  "handlebar" moustache (CAST key moustache_style="handlebar")
    _prop       mona_panel, mona_framed, newspaper (the Mona Lisa front page, replaces the v2 sheet), key, palette
    figure      lie (the whole figure rotated to lie down), the far-grip anchors of the paintings / newspaper
New cast: vincenzo, vincenzo_smock, director, coworker1, coworker2, plumber, guard, painter, police, young_painter, dealer,
          lady, gentleman, newsboy.
STORY7 / STORY7_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: mona_svg (the painting alone), mona_panel_svg, mona_framed_svg, newspaper_svg, key_svg, hooks_svg (the
empty wall spot with four iron hooks), easel_svg, poster_svg.

Command line (QA):  python3 test_cast7.py        lineup.jpg (every member, every pose, cycles, mouths, props), canvas + robustness
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
_d = os.path.join(PROJ, "v3", "cast6")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast6 as C6      # noqa: E402  (v3/cast6, read-only; imports cast5 .. cast_ext and v2/puppet)
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW7 = ("vincenzo", "vincenzo_smock", "director", "coworker1", "coworker2", "plumber", "guard", "painter", "police",
        "young_painter", "dealer", "lady", "gentleman", "newsboy")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_hsh, _f = C6._hsh, C6._f
_O7 = {}
# pose keys of the figure being drawn (set by the _norm wrapper; figure() calls _norm before drawing anything)
_POSE7 = {"bulge": 0.0, "sweat": 0.0, "grip": "side", "mirror": False, "flip_text": False, "an": {}, "sides": [], "pside": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
GOLD = dict(light="#ffe9a0", base="#d9a83a", dark="#8e6418", deep="#5e3e0c")
WOOD = dict(light="#d8b07a", base="#b08050", dark="#6e4a28")
IRON = dict(light="#9a96a2", base="#5c5862", dark="#2e2a32")
PAPER = dict(base="#efe6cf", dark="#c9bd9c", ink="#2e2a2c", text="#6a6266")
ML = dict(sky="#9fb09a", haze="#c9c08e", hill="#6f8a7c", hill2="#8a8a5e", road="#c09a5a", ground="#5e4826", hair="#3a2818",
          dress="#3a301e", dress2="#5a4a2a", sleeve="#8a5e2c", skin="#efc27c", skin_d="#c08a48", skin_l="#f8dca0", veil="#2a2018")


# ============================================================================= the Mona Lisa (drawn in a w x h box centred on 0, 0)
def _mona(k, w, h, uid=None, detail=1.0):
    """the painting itself: hazy green-blue sky, winding road and blue hills, the woman in a dark dress with folded hands,
    dark hair with the veil, the small smile; yellowed varnish and a dark vignette.  Box (-w/2, -h/2) .. (w/2, h/2)."""
    u = (uid or k.uid) + "_ml%d" % int(1000 * w)
    x0, y0 = -w / 2, -h / 2

    def U(a, b):
        return (x0 + a * w, y0 + b * h)

    def D(pts):
        return P._smooth_closed([U(a, b) for a, b in pts])
    o = []
    k.defs.append('<clipPath id="%s_c"><rect x="%.4f" y="%.4f" width="%.4f" height="%.4f"/></clipPath>' % (u, x0, y0, w, h))
    k.defs.append('<linearGradient id="%s_bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="0.38" stop-color="%s"/>'
                  '<stop offset="0.62" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(ML["sky"]), k.c(ML["haze"]), k.c(ML["hill2"]), k.c(ML["ground"])))
    k.defs.append('<radialGradient id="%s_fc" cx="0.42" cy="0.38" r="0.70"><stop offset="0" stop-color="%s"/><stop offset="0.6" stop-color="%s"/>'
                  '<stop offset="1" stop-color="%s"/></radialGradient>' % (u, k.c(ML["skin_l"]), k.c(ML["skin"]), k.c(ML["skin_d"])))
    k.defs.append('<radialGradient id="%s_vg" cx="0.5" cy="0.45" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0.55"/></radialGradient>' % (u, k.c("#1e1408")))
    o.append('<g clip-path="url(#%s_c)">' % u)
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="url(#%s_bg)"/>' % (x0, y0, w, h, u))
    # landscape: far blue hills both sides, a winding road (left), a bridge hint (right)
    o.append('<path d="%s" fill="%s" opacity="0.85"/>' % (D(((0.0, 0.30), (0.10, 0.26), (0.22, 0.32), (0.30, 0.42), (0.30, 0.60), (0.0, 0.62))), k.c(ML["hill"])))
    o.append('<path d="%s" fill="%s" opacity="0.85"/>' % (D(((1.0, 0.24), (0.88, 0.22), (0.76, 0.30), (0.70, 0.42), (0.70, 0.60), (1.0, 0.62))), k.c(ML["hill"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.9"/>'
             % (U(0.04, 0.58) + U(0.20, 0.52) + U(0.10, 0.46) + U(0.02, 0.42) + U(0.18, 0.38) + (k.c(ML["road"]), 0.018 * w)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" opacity="0.8"/>' % (U(0.80, 0.52) + U(0.98, 0.50) + (k.c(ML["road"]), 0.014 * w)))
    # hair mass behind the face, falling to the shoulders
    o.append('<path d="%s" fill="%s"/>' % (D(((0.50, 0.06), (0.68, 0.10), (0.75, 0.30), (0.74, 0.50), (0.78, 0.60), (0.62, 0.58), (0.50, 0.48),
                                              (0.38, 0.58), (0.22, 0.60), (0.26, 0.48), (0.25, 0.30), (0.32, 0.10))), k.c(ML["hair"])))
    # dress: dark body with the warm brown sleeves, neckline
    o.append('<path d="%s" fill="%s"/>' % (D(((0.30, 0.55), (0.50, 0.53), (0.72, 0.55), (0.92, 0.68), (1.02, 1.04), (-0.02, 1.04), (0.08, 0.70))), k.c(ML["dress"])))
    for s in (-1, 1):
        o.append('<path d="%s" fill="%s"/>' % (D(((0.5 + s * 0.30, 0.66), (0.5 + s * 0.44, 0.80), (0.5 + s * 0.48, 1.02), (0.5 + s * 0.24, 1.02),
                                                  (0.5 + s * 0.20, 0.86))), k.c(ML["sleeve"])))
        if detail > 0.5:
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.6"/>'
                     % (U(0.5 + s * 0.34, 0.74) + U(0.5 + s * 0.40, 0.86) + U(0.5 + s * 0.36, 0.98) + (k.c(ML["dress2"]), 0.010 * w)))
    # neck + chest (skin) with the curved neckline
    o.append('<path d="%s" fill="url(#%s_fc)"/>' % (D(((0.45, 0.44), (0.55, 0.44), (0.58, 0.53), (0.68, 0.58), (0.50, 0.65), (0.32, 0.58), (0.42, 0.53))), u))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.8"/>'
             % (U(0.32, 0.595) + U(0.50, 0.67) + U(0.68, 0.595) + (k.c(ML["dress2"]), 0.012 * w)))
    # face (turned slightly to her right = screen-left)
    o.append('<path d="%s" fill="url(#%s_fc)"/>' % (D(((0.50, 0.14), (0.62, 0.19), (0.645, 0.31), (0.60, 0.43), (0.50, 0.48), (0.40, 0.43), (0.36, 0.31), (0.39, 0.19))), u))
    if detail > 0.3:
        # eyes, nose, the smile
        for (a, b) in ((0.445, 0.290), (0.560, 0.290)):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (U(a, b) + (0.030 * w, 0.012 * h, k.c("#4a2e1a"))))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.6"/>'
                 % (U(0.505, 0.31) + U(0.50, 0.37) + U(0.485, 0.38) + (k.c(ML["skin_d"]), 0.008 * w)))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
                 % (U(0.455, 0.412) + U(0.50, 0.425) + U(0.550, 0.405) + (k.c("#8a4a2a"), 0.010 * w)))
    # folded hands (right over left)
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="url(#%s_fc)" transform="rotate(-12 %.4f %.4f)"/>'
             % (U(0.40, 0.90) + (0.13 * w, 0.050 * h, u) + U(0.40, 0.90)))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="url(#%s_fc)" transform="rotate(-6 %.4f %.4f)"/>'
             % (U(0.60, 0.87) + (0.14 * w, 0.050 * h, u) + U(0.60, 0.87)))
    if detail > 0.5:
        for i in range(3):
            o.append('<path d="M%.4f,%.4f l%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.5"/>'
                     % (U(0.52 + 0.04 * i, 0.855) + (0.03 * w, 0.03 * h, k.c(ML["skin_d"]), 0.006 * w)))
    # varnish + vignette
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" opacity="0.14"/>' % (x0, y0, w, h, k.c("#c8a040")))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="url(#%s_vg)"/>' % (x0, y0, w, h, u))
    o.append('</g>')
    return "".join(o)


PANEL_W, PANEL_H = 0.50, 0.72          # the bare poplar panel (D); the painted field is inset 0.025
FRAME_B = 0.11                         # frame border (D): framed piece is 0.72 x 0.94
PAPER_W, PAPER_H = 0.56, 0.76          # the newspaper page held open


def _panel_body(k, cx, cy, w=PANEL_W, h=PANEL_H, back=False):
    """the unframed panel: poplar board edge (lighter wood band), the painting inset, a dark side edge to give it thickness."""
    o = []
    th = 0.03
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (cx + w / 2, cy - h / 2, cx + w / 2 + th, cy - h / 2 + th, cx + w / 2 + th, cy + h / 2 + th, cx + w / 2, cy + h / 2, k.c(WOOD["dark"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (cx - w / 2, cy + h / 2, cx + w / 2, cy + h / 2, cx + w / 2 + th, cy + h / 2 + th, cx - w / 2 + th, cy + h / 2 + th, k.c(WOOD["base"]), k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx - w / 2, cy - h / 2, w, h, k.c(WOOD["light"]), k.ink))
    if back:
        for i in range(4):
            yy = cy - h / 2 + h * (0.2 + 0.2 * i)
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.6"/>'
                     % (cx - w / 2 + 0.03, yy, cx, yy + 0.02, cx + w / 2 - 0.03, yy - 0.01, k.c(WOOD["dark"])))
        return "".join(o)
    m = 0.025
    o.append('<g transform="translate(%.4f %.4f)">%s</g>' % (cx, cy, _mona(k, w - 2 * m, h - 2 * m)))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.6"/>'
             % (cx - w / 2 + m, cy - h / 2 + m, w - 2 * m, h - 2 * m, k.c(WOOD["dark"])))
    return "".join(o)


def _framed_body(k, cx, cy, w=PANEL_W, h=PANEL_H, glass=True):
    """the panel in its gilded frame behind the protective glass (the glass Vincenzo himself fitted): carved gold frame with a
    bead moulding, corner rosettes, a glare streak on the glass."""
    u = k.uid + "_fr%d" % int(1000 * w)
    b = FRAME_B * w / PANEL_W
    W, H = w + 2 * b, h + 2 * b
    k.defs.append('<linearGradient id="%s_g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/>'
                  '<stop offset="1" stop-color="%s"/></linearGradient>' % (u, k.c(GOLD["light"]), k.c(GOLD["base"]), k.c(GOLD["dark"])))
    o = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="url(#%s_g)" stroke="%s" stroke-width="0.022"/>' % (cx - W / 2, cy - H / 2, W, H, u, k.ink)]
    # inner and outer mouldings
    for (dw, col, sw) in ((0.22, GOLD["dark"], 0.012), (0.55, GOLD["light"], 0.010), (0.80, GOLD["deep"], 0.014)):
        ww, hh = W - 2 * b * dw, H - 2 * b * dw
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.9"/>'
                 % (cx - ww / 2, cy - hh / 2, ww, hh, k.c(col), sw))
    # bead moulding (dots) on the middle band
    n = 7
    for i in range(n + 1):
        t = i / float(n)
        for (px, py) in ((cx - W / 2 + b * 0.38 + (W - b * 0.76) * t, cy - H / 2 + b * 0.38), (cx - W / 2 + b * 0.38 + (W - b * 0.76) * t, cy + H / 2 - b * 0.38),
                         (cx - W / 2 + b * 0.38, cy - H / 2 + b * 0.38 + (H - b * 0.76) * t), (cx + W / 2 - b * 0.38, cy - H / 2 + b * 0.38 + (H - b * 0.76) * t)):
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (px, py, 0.012 * w / PANEL_W, k.c(GOLD["light"])))
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = cx + sx * (W / 2 - b * 0.5), cy + sy * (H / 2 - b * 0.5)
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.010"/>' % (px, py, b * 0.36, k.c(GOLD["base"]), k.c(GOLD["deep"])))
            for a in range(0, 360, 60):
                qx, qy = px + math.cos(math.radians(a)) * b * 0.22, py + math.sin(math.radians(a)) * b * 0.22
                o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (qx, qy, b * 0.08, k.c(GOLD["light"])))
    o.append('<g transform="translate(%.4f %.4f)">%s</g>' % (cx, cy, _mona(k, w, h)))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="none" stroke="%s" stroke-width="0.016"/>' % (cx - w / 2, cy - h / 2, w, h, k.ink))
    if glass:
        g = ("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (cx - w / 2 + w * 0.10, cy - h / 2, cx - w / 2 + w * 0.34, cy - h / 2,
                                                             cx - w / 2, cy - h / 2 + h * 0.46, cx - w / 2, cy - h / 2 + h * 0.20))
        o.append('<path d="%s" fill="#ffffff" opacity="0.30"/>' % g)
        g2 = ("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (cx + w / 2, cy + h / 2 - h * 0.40, cx + w / 2, cy + h / 2 - h * 0.30,
                                                              cx + w / 2 - w * 0.30, cy + h / 2, cx + w / 2 - w * 0.42, cy + h / 2))
        o.append('<path d="%s" fill="#ffffff" opacity="0.18"/>' % g2)
    return "".join(o), W, H


def _newspaper_body(k, cx, cy, w=PAPER_W, h=PAPER_H, headline="LA JOCONDE A DISPARU !", unflip=False):
    """a broadsheet front page: masthead, the big headline, the Mona Lisa picture in a black rule box, text columns."""
    o = []
    x0, y0 = cx - w / 2, cy - h / 2
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (x0, y0, x0 + w, y0 + 0.01, x0 + w - 0.005, y0 + h, x0 + 0.004, y0 + h - 0.008, k.c(PAPER["base"]), k.ink))
    t = ['<g%s>' % (' transform="translate(%.4f 0) scale(-1 1)"' % (2 * cx) if unflip else "")]
    t.append('<text x="%.4f" y="%.4f" font-family="Georgia, \'DejaVu Serif\', serif" font-weight="bold" font-size="%.4f" text-anchor="middle" '
             'fill="%s" textLength="%.4f" lengthAdjust="spacingAndGlyphs">LE GRAND JOURNAL</text>' % (cx, y0 + 0.075, 0.062, k.c(PAPER["ink"]), w * 0.84))
    t.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008"/>'
             % (x0 + 0.03, y0 + 0.095, x0 + w - 0.03, y0 + 0.095, x0 + 0.03, y0 + 0.108, x0 + w - 0.03, y0 + 0.108, k.c(PAPER["ink"])))
    t.append('<text x="%.4f" y="%.4f" font-family="Georgia, \'DejaVu Serif\', serif" font-weight="bold" font-size="%.4f" text-anchor="middle" '
             'fill="%s" textLength="%.4f" lengthAdjust="spacingAndGlyphs">%s</text>' % (cx, y0 + 0.165, 0.050, k.c("#8a1a16"), w * 0.90, headline))
    # picture box
    pw, ph = w * 0.54, h * 0.50
    px, py = cx - w * 0.17, y0 + 0.19 + ph / 2
    t.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s"/>' % (px - pw / 2 - 0.012, py - ph / 2 - 0.012, pw + 0.024, ph + 0.024, k.c(PAPER["ink"])))
    t.append('<g transform="translate(%.4f %.4f)"><g opacity="0.92">%s</g></g>' % (px, py, _mona(k, pw, ph, detail=0.8)))
    t.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" opacity="0.18"/>' % (px - pw / 2, py - ph / 2, pw, ph, k.c("#8a7a5a")))
    # text columns
    cl = []
    for i in range(9):
        yy = py - ph / 2 + 0.02 + i * (ph / 9.0)
        cl.append("M%.4f,%.4f L%.4f,%.4f" % (px + pw / 2 + 0.03, yy, x0 + w - 0.03 - 0.03 * (i % 3 == 2), yy))
    for i in range(5):
        yy = py + ph / 2 + 0.05 + i * 0.035
        if yy > y0 + h - 0.03:
            break
        cl.append("M%.4f,%.4f L%.4f,%.4f" % (x0 + 0.03, yy, cx - 0.02, yy))
        cl.append("M%.4f,%.4f L%.4f,%.4f" % (cx + 0.02, yy, x0 + w - 0.03 - 0.04 * (i == 4), yy))
    t.append('<path d="%s" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.75"/>' % (" ".join(cl), k.c(PAPER["text"])))
    t.append('</g>')
    o.extend(t)
    # fold line + curl shadow
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.55"/>' % (x0 + 0.004, cy + 0.04, x0 + w - 0.004, cy + 0.045, k.c(PAPER["dark"])))
    return "".join(o)


def _key_body(k, sc=1.0):
    """a big iron skeleton key along +x: oval bow (ring) at 0, shaft to 0.34, bit with two teeth at the end."""
    o = []
    o.append('<path d="M0.030,-0.016 L0.330,-0.014 L0.330,0.014 L0.030,0.016 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(IRON["base"]), k.ink))
    o.append('<path d="M0.27,0.010 L0.33,0.010 L0.33,0.075 L0.315,0.075 L0.315,0.050 L0.300,0.050 L0.300,0.075 L0.27,0.075 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
             % (k.c(IRON["base"]), k.ink))
    o.append('<ellipse cx="-0.020" cy="0" rx="0.062" ry="0.050" fill="none" stroke="%s" stroke-width="0.040"/>' % k.ink)
    o.append('<ellipse cx="-0.020" cy="0" rx="0.062" ry="0.050" fill="none" stroke="%s" stroke-width="0.022"/>' % k.c(IRON["base"]))
    o.append('<path d="M0.06,-0.008 L0.30,-0.006" stroke="%s" stroke-width="0.007" stroke-linecap="round" opacity="0.9"/>' % k.c(IRON["light"]))
    o.append('<rect x="0.030" y="-0.026" width="0.026" height="0.052" rx="0.008" fill="%s" stroke="%s" stroke-width="0.009"/>' % (k.c(IRON["dark"]), k.ink))
    return "".join(o)


def _palette_body(k, side):
    """painter's palette (kidney board, thumb hole at the hand, paint blobs), extending to `side` (+1 screen-right)."""
    s = side
    pts = [(0.0, -0.05), (s * 0.18, -0.13), (s * 0.40, -0.10), (s * 0.48, 0.02), (s * 0.38, 0.13), (s * 0.16, 0.12), (s * 0.06, 0.06)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c("#c89a62"), k.ink)]
    o.append('<circle cx="%.4f" cy="0.0" r="0.035" fill="%s" stroke="%s" stroke-width="0.010"/>' % (s * 0.05, k.c("#8a6038"), k.ink))
    for i, (x, y, c) in enumerate(((0.20, -0.07, "#d8352a"), (0.31, -0.06, "#f0c030"), (0.40, 0.0, "#3a7ac0"), (0.33, 0.08, "#f6f2e6"), (0.20, 0.07, "#3a8a4a"))):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.032" ry="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>' % (s * x, y, k.c(c), k.ink))
    for p in pts:
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o)


# ============================================================================= props held in the hand
NEW_PROPS7 = ("mona_panel", "mona_framed", "newspaper", "key", "palette")
KEY_LEN = 0.33
NEW_TIP7 = {"mona_panel": PANEL_W / 2, "mona_framed": PANEL_W / 2 + FRAME_B, "newspaper": PAPER_W / 2, "key": KEY_LEN, "palette": 0.25}
GRIPS = ("side", "bottom", "top")


def _flat_piece(k, kind, H, sc):
    """the paintings and the newspaper: flat upright pieces gripped by an edge.  Side grip: the hand holds the middle of the
    edge nearest to it, the piece extends toward the body centre line; bottom grip: the hand holds a bottom corner (lifting it
    up off the wall / holding it up); top grip: a top corner (carrying it hanging down).  Returns svg, tip, far grip point."""
    side = -1.0 if H[0] > 0.02 else 1.0                      # extend toward the body centre (pose key panel_side overrides)
    if _POSE7["pside"]:
        side = _POSE7["pside"]
    if kind == "mona_panel":
        w, h = PANEL_W, PANEL_H
    elif kind == "mona_framed":
        w, h = PANEL_W + 2 * FRAME_B, PANEL_H + 2 * FRAME_B
    else:
        w, h = PAPER_W, PAPER_H
    w, h = w * sc, h * sc
    grip = _POSE7["grip"]
    inset = 0.02 * sc
    if grip == "bottom":
        cx, cy = H[0] + side * (w / 2 - 0.07 * sc), H[1] - h / 2 + inset
        far = (H[0] + side * (w - 0.14 * sc), H[1])
    elif grip == "top":
        cx, cy = H[0] + side * (w / 2 - 0.07 * sc), H[1] + h / 2 - inset
        far = (H[0] + side * (w - 0.14 * sc), H[1])
    else:
        cx, cy = H[0] + side * (w / 2 - inset), H[1]
        far = (H[0] + side * (w - 2 * inset), H[1])
    unflip = bool(_POSE7["mirror"]) != bool(_POSE7["flip_text"])
    tr = 'translate(%.4f %.4f) scale(%.4f)' % (cx, cy, sc)
    if unflip:
        tr += ' scale(-1 1)'
    if kind == "mona_panel":
        body = _panel_body(k, 0.0, 0.0)
    elif kind == "mona_framed":
        body, _, _ = _framed_body(k, 0.0, 0.0)
    else:
        body = _newspaper_body(k, 0.0, 0.0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.ext.append((cx + sx * (w / 2 + 0.04), cy + sy * (h / 2 + 0.04), 0.02))
    return '<g transform="%s">%s</g>' % (tr, body), (cx, cy), far


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS7:
        return _O7["_prop"](k, kind, H, ang, sc)
    if kind in ("mona_panel", "mona_framed", "newspaper"):
        svg, tip, far = _flat_piece(k, kind, H, sc)
        key = _POSE7["sides"].pop(0) if _POSE7["sides"] else "r"
        _POSE7["an"]["grip_far_%s" % key] = far
        _POSE7["an"]["piece_centre_%s" % key] = tip
        _POSE7["an"]["piece_hand_%s" % key] = H
        return svg, tip
    if kind == "key":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _key_body(k))
        for e in ((-0.09, 0.0), (0.34, 0.0), (0.30, 0.08)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        tx, ty = _rot(KEY_LEN * sc, 0.0, ang)
        return o, (H[0] + tx, H[1] + ty)
    # palette
    side = 1.0 if H[0] >= 0 else -1.0
    n0 = len(k.ext)
    o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _palette_body(k, side))
    k.ext[n0:] = [(H[0] + e[0] * sc, H[1] + e[1] * sc, e[2] * sc) for e in k.ext[n0:]]
    return o, (H[0] + side * 0.25 * sc, H[1])


# ============================================================================= standalone pieces
def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def mona_svg(uid="ms", w=PANEL_W - 0.05, h=PANEL_H - 0.05, ink=P.INK, tint=None):
    """the painted image alone, centred on (0, 0), w x h (D)."""
    k = _ctx(uid, ink, tint)
    s = _mona(k, w, h)
    return '<g id="%s_mona"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def mona_panel_svg(uid="mp", back=False, ink=P.INK, tint=None):
    """the bare panel (0.50 x 0.72 D, + 0.03 thickness edge to the lower right), centred on (0, 0); back=True: the back of
    the board (no picture, wood grain) -- e.g. lying in the trunk."""
    k = _ctx(uid, ink, tint)
    s = _panel_body(k, 0.0, 0.0, back=back)
    return '<g id="%s_panel"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def mona_framed_svg(uid="mf", glass=True, ink=P.INK, tint=None):
    """the panel in its gilded frame behind glass, centred on (0, 0): 0.72 x 0.94 D.  Returns (svg, anchors): hooks
    (the four iron hook points on the frame's top and bottom edges), top / bottom centre."""
    k = _ctx(uid, ink, tint)
    s, W, H = _framed_body(k, 0.0, 0.0, glass=glass)
    an = dict(hook_tl=(-W * 0.32, -H / 2), hook_tr=(W * 0.32, -H / 2), hook_bl=(-W * 0.32, H / 2), hook_br=(W * 0.32, H / 2),
              top=(0.0, -H / 2), bottom=(0.0, H / 2), size=(W, H))
    return '<g id="%s_framed"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), an


def hooks_svg(uid="hk", ink=P.INK, tint=None, ghost=0.0):
    """the empty spot on the wall: the four iron hooks where the framed picture hung (same anchors as mona_framed_svg),
    optional ghost = 0..1 a paler rectangle of unfaded wall (the picture's outline).  Centred on (0, 0)."""
    k = _ctx(uid, ink, tint)
    W, H = PANEL_W + 2 * FRAME_B, PANEL_H + 2 * FRAME_B
    o = []
    if ghost > 0:
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="#ffffff" opacity="%.3f"/>' % (-W / 2, -H / 2, W, H, 0.22 * ghost))
    for (x, y, s) in ((-W * 0.32, -H / 2, -1), (W * 0.32, -H / 2, -1), (-W * 0.32, H / 2, 1), (W * 0.32, H / 2, 1)):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.022" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x, y + s * 0.03, k.c(IRON["dark"]), k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
                 % (x, y + s * 0.03, x, y - s * 0.03, x, y - s * 0.07, x + 0.035, y - s * 0.065, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
                 % (x, y + s * 0.03, x, y - s * 0.03, x, y - s * 0.07, x + 0.035, y - s * 0.065, k.c(IRON["light"])))
    an = dict(hook_tl=(-W * 0.32, -H / 2), hook_tr=(W * 0.32, -H / 2), hook_bl=(-W * 0.32, H / 2), hook_br=(W * 0.32, H / 2))
    return '<g id="%s_hooks">%s</g>' % (k.uid, "".join(o)), an


def newspaper_svg(uid="np", headline="LA JOCONDE A DISPARU !", ink=P.INK, tint=None):
    """the Mona Lisa front page (0.56 x 0.76 D) centred on (0, 0), for kiosks, posters, a stack (scale it freely)."""
    k = _ctx(uid, ink, tint)
    s = _newspaper_body(k, 0.0, 0.0, headline=headline)
    return '<g id="%s_news"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def poster_svg(uid="po", text="OU EST-ELLE ?", w=0.70, h=1.00, ink=P.INK, tint=None):
    """a kiosk poster / postcard: the portrait big in an oval cartouche, a title band; centred on (0, 0)."""
    k = _ctx(uid, ink, tint)
    o = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (-w / 2, -h / 2, w, h, k.c("#e8d6a8"), k.ink)]
    k.defs.append('<clipPath id="%s_ov"><ellipse cx="0" cy="%.4f" rx="%.4f" ry="%.4f"/></clipPath>' % (k.uid, -h * 0.08, w * 0.38, h * 0.36))
    o.append('<g clip-path="url(#%s_ov)"><g transform="translate(0 %.4f)">%s</g></g>' % (k.uid, -h * 0.08, _mona(k, w * 0.80, h * 0.78)))
    o.append('<ellipse cx="0" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.022"/>' % (-h * 0.08, w * 0.38, h * 0.36, k.c("#8a1a16")))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s"/>' % (-w / 2 + 0.03, h * 0.32, w - 0.06, h * 0.13, k.c("#8a1a16")))
    o.append('<text x="0" y="%.4f" font-family="Georgia, \'DejaVu Serif\', serif" font-weight="bold" font-size="%.4f" text-anchor="middle" fill="%s" '
             'textLength="%.4f" lengthAdjust="spacingAndGlyphs">%s</text>' % (h * 0.415, h * 0.075, k.c("#f8ecd0"), w * 0.80, text))
    return '<g id="%s_poster"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), "".join(o))


def key_svg(uid="ky", ink=P.INK, tint=None):
    """the big iron key alone along +x (bow centre at (-0.02, 0), bit end at x 0.33)."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_key">%s</g>' % (k.uid, _key_body(k))


def easel_svg(uid="es", canvas=True, painted=0.0, ink=P.INK, tint=None):
    """a wooden studio easel (feet on y = 0, 1.9 D tall) with an optional blank / half-painted canvas (painted 0..1 =
    a rough copy of the portrait fading in).  Returns (svg, anchors): canvas_centre, top."""
    k = _ctx(uid, ink, tint)
    wd, wdd = k.c(WOOD["base"]), k.c(WOOD["dark"])
    o = []
    for (x0, x1) in ((-0.42, -0.06), (0.42, 0.06)):
        o.append('<path d="M%.4f,0 L%.4f,-1.86" stroke="%s" stroke-width="0.075" stroke-linecap="round"/>' % (x0, x1, k.ink))
        o.append('<path d="M%.4f,0 L%.4f,-1.86" stroke="%s" stroke-width="0.045" stroke-linecap="round"/>' % (x0, x1, wd))
    o.append('<path d="M0,-1.70 L0.10,0" stroke="%s" stroke-width="0.060" stroke-linecap="round"/><path d="M0,-1.70 L0.10,0" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (k.ink, wdd))
    o.append('<rect x="-0.40" y="-0.78" width="0.80" height="0.06" rx="0.01" fill="%s" stroke="%s" stroke-width="0.016"/>' % (wd, k.ink))
    an = dict(top=(0.0, -1.88), canvas_centre=(0.0, -1.18))
    if canvas:
        cw, ch = 0.66, 0.80
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (-cw / 2, -0.78 - ch, cw, ch, k.c("#f4eee0"), k.ink))
        if painted > 0:
            o.append('<g transform="translate(0 %.4f)" opacity="%.3f">%s</g>' % (-0.78 - ch / 2, _clamp(painted, 0.0, 1.0), _mona(k, cw - 0.06, ch - 0.06, detail=0.6)))
    return '<g id="%s_easel"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), "".join(o)), an


# ============================================================================= face: goatee, monocle, sweat, handlebar
def _goatee(k, C, L):
    G = C["goatee"]
    mx, my = L["mx"], L["my"]
    col = k.c(G.get("color", "#2a2226"))
    ln = G.get("len", 0.20)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        mx - 0.085, my + 0.055, mx - 0.07, my + 0.06 + ln * 0.6, mx + 0.005, my + 0.05 + ln, mx + 0.07, my + 0.06 + ln * 0.6, mx + 0.085, my + 0.055,
        mx, my + 0.085, mx - 0.085, my + 0.055)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, col, k.ink)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.009" opacity="0.7"/>'
             % (mx - 0.02, my + 0.09, mx - 0.01, my + 0.05 + ln * 0.7, mx + 0.005, my + 0.04 + ln, k.c(G.get("light", "#6a5a5e"))))
    k.ext.append((mx, my + 0.06 + ln, 0.02))
    return "".join(o)


def _monocle(k, C, L):
    x, y, s = L["xR"], L["ey"], L["sR"]
    r = 0.085 * max(0.7, s)
    o = ['<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" fill-opacity="0.22" stroke="%s" stroke-width="0.024"/>' % (x, y, r, k.ink)]
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.012"/>' % (x, y, r, k.c(GOLD["base"])))
    o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>'
             % (x - r * 0.5, y - r * 0.4, r * 0.2, -r * 0.3, r * 0.6, -r * 0.4, "#ffffff"))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008"/>' % (x + r, y + 0.01, x + r + 0.08, y + 0.25, x + r - 0.02, y + 0.50, k.ink))
    return "".join(o)


def _sweat_drops(k, C, L, lev):
    """nervous sweat: up to five drops round the head + a damp shine streak on the forehead (pose key sweat 0..1)."""
    n = int(round(1 + 4 * lev))
    pts = ((0.43, -0.20, 9.0), (-0.42, -0.14, -10.0), (0.48, 0.02, 14.0), (-0.47, 0.06, -16.0), (0.30, -0.40, 4.0))
    o = []
    for i in range(n):
        x, y, r = pts[i]
        o.append(P._fx_sweat(k, x, y, 0.75 + 0.25 * lev, r))
    o.append('<path d="M%.4f,-0.30 Q%.4f,-0.34 %.4f,-0.31" fill="none" stroke="#ffffff" stroke-width="0.022" stroke-linecap="round" opacity="%.3f"/>'
             % (L["xL"] - 0.02, (L["xL"] + L["xR"]) / 2, L["xR"] + 0.02, 0.6 * lev))
    for (x, y, _) in pts[:n]:
        k.ext.append((x, y + 0.05, 0.08))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O7["_face"](k, C, P_, white)
    if C is None or not C.get("_cast7"):
        return svg, L
    over = []
    if C.get("goatee"):
        over.append(_goatee(k, C, L))
    if C.get("monocle") and P_["blink"] < 2:
        over.append(_monocle(k, C, L))
    if _POSE7["sweat"] > 0.02:
        over.append(_sweat_drops(k, C, L, _POSE7["sweat"]))
    if not over:
        return svg, L
    return svg + "".join(over), L


def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "handlebar":
        return _O7["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#2a2226")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    o = []
    for sd in (-1, 1):
        pts = [Q(0.0, -0.050), Q(sd * 0.10, -0.062), Q(sd * 0.19, -0.030), Q(sd * 0.25, -0.060), Q(sd * 0.27, -0.125), Q(sd * 0.30, -0.110),
               Q(sd * 0.30, -0.040), Q(sd * 0.24, 0.010), Q(sd * 0.15, 0.030), Q(sd * 0.06, 0.028), Q(0.0, 0.012)]
        d = P._smooth_closed(pts)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round" opacity="0.8"/>'
                 % (Q(sd * 0.04, -0.02) + Q(sd * 0.16, -0.01) + Q(sd * 0.25, -0.07) + (k.c(C["colors"].get("moustache_l", P._shade(col, 1.6))),)))
    return "".join(o)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE7["bulge"] = _f(g("bulge"), 0.0, 0.0, 1.0)
    _POSE7["sweat"] = _f(g("sweat"), 0.0, 0.0, 1.0)
    gr = g("panel_grip")
    _POSE7["grip"] = gr if gr in GRIPS else "side"
    _POSE7["mirror"] = bool(g("mirror"))
    _POSE7["flip_text"] = bool(g("flip_text"))
    ps = _num(g("panel_side"), 0.0)
    _POSE7["pside"] = 1.0 if ps > 0.5 else (-1.0 if ps < -0.5 else 0.0)
    _POSE7["an"] = {}
    _POSE7["sides"] = [s for s in ("l", "r") if P._prop_spec(g("prop_" + s))]
    return _O7["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _bulge(k, X, C, m, lev):
    """the Mona Lisa panel hidden under the smock: a stiff rectangle pressing out the cloth over the belly -- lighter cloth
    stretched over its face, a shaded lower / screen-right edge, the corners poking out and stress creases running from them."""
    col = C["colors"]
    h = C["torso_h"]
    yc = TT + h * 0.66
    bw = min(PANEL_W * 0.86, m.hwa * 1.55)
    bh = PANEL_H * 0.80
    sk = 0.02
    c = [X(-bw / 2, yc - bh / 2), X(bw / 2, yc - bh / 2 + sk), X(bw / 2 + 0.01, yc + bh / 2), X(-bw / 2 + 0.01, yc + bh / 2 - sk)]
    op = _clamp(lev, 0.0, 1.0)
    o = ['<g opacity="%.3f">' % op]
    # creases from the corners out to the torso sides / hem
    cr = []
    for (p, q) in ((c[0], X(-m.hwa * 0.95, yc - bh / 2 - 0.10)), (c[1], X(m.hwa * 0.95, yc - bh / 2 - 0.06)), (c[2], X(m.hwa * 1.0, yc + bh / 2 + 0.12)),
                   (c[3], X(-m.hwa * 1.0, yc + bh / 2 + 0.10)), (c[0], X(-0.05, TT + 0.10)), (c[1], X(0.08, TT + 0.12))):
        cr.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (p + ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.02) + q))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.85"/>' % (" ".join(cr), k.c(col.get("dark", "#9aa0b0"))))
    gid = "%s_bg7" % k.uid
    k.defs.append('<linearGradient id="%s" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
                  '<stop offset="1" stop-color="%s"/></linearGradient>' % (gid, k.c(P._shade(col["smock"], 1.06)), k.c(col["smock"]), k.c(P._shade(col["smock"], 0.80))))
    d = P._smooth_closed([c[0], ((c[0][0] + c[1][0]) / 2, c[0][1] - 0.012), c[1], ((c[1][0] + c[2][0]) / 2 + 0.012, (c[1][1] + c[2][1]) / 2), c[2],
                          ((c[2][0] + c[3][0]) / 2, c[2][1] + 0.012), c[3], ((c[3][0] + c[0][0]) / 2 - 0.012, (c[3][1] + c[0][1]) / 2)])
    o.append('<path d="%s" fill="url(#%s)" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, gid, k.ink))
    # shade band along the lower and screen-right edge, a highlight along the top-left
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round" opacity="0.45"/>'
             % (c[1][0] - 0.02, c[1][1] + 0.03, c[2][0] - 0.02, c[2][1] - 0.02, c[3][0] + 0.03, c[3][1] - 0.02, k.c(col.get("dark", "#9aa0b0"))))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linejoin="round" opacity="0.8"/>'
             % (c[3][0] + 0.03, c[3][1] - 0.05, c[0][0] + 0.025, c[0][1] + 0.025, c[1][0] - 0.05, c[1][1] + 0.025))
    for p in c:
        o.append('<circle cx="%.4f" cy="%.4f" r="0.016" fill="%s"/>' % (p[0], p[1], k.ink))
        k.ext.append((p[0], p[1], 0.03))
    o.append('</g>')
    return "".join(o)


def _cos_smock7(k, C, m):
    """white work smock (or the painter's paint-spattered smock, or a short blue worker's blouse): band collar, a yoke seam
    with gathered folds below it, a buttoned placket, one chest pocket, the skirt of the smock falling over the legs to
    C["smock_len"] below the torso with two hip pockets.  C["paint"]: paint splotches; C["bow"]: an artist's floppy bow.
    Pose key bulge 0..1: the hidden panel pressing out the cloth (vincenzo_smock)."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    dark = k.c(col.get("dark", "#aab0c0"))
    o = []
    # yoke seam + gathered folds
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.8"/>' % (X(-hw, 0.58) + X(0, 0.62) + X(hw, 0.58) + (dark,)))
    folds = []
    for x in (-0.24, -0.15, 0.15, 0.24):
        folds.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(x * hw / 0.33, 0.62) + X(x * hw / 0.33 * 1.05, 0.80) + X(x * hw / 0.33 * 1.1, yB - 0.05)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (" ".join(folds), dark))
    # placket + buttons
    o.append(_ln([X(0.0, 0.43), X(0.0, yB)], dark, 0.014))
    for y in (0.50, 0.62, 0.74):
        o.append(_circ(X(0.025, y), 0.016, k.c(col.get("button", "#f8f8f4")), k, 0.008))
    # chest pocket (screen-left)
    o.append(_poly(k, [X(-0.30 * hw / 0.33, 0.66), X(-0.14 * hw / 0.33, 0.66), X(-0.145 * hw / 0.33, 0.78), X(-0.295 * hw / 0.33, 0.78)], k.c(col["smock"]), 0.012))
    if C.get("pencil"):
        o.append(_ln([X(-0.24 * hw / 0.33, 0.66), X(-0.25 * hw / 0.33, 0.59)], k.c("#d9b24a"), 0.020))
    if C.get("paint"):
        for i, (x, y, r, c) in enumerate(((-0.15, 0.88, 0.040, "#d8352a"), (0.18, 0.72, 0.030, "#3a7ac0"), (0.10, 1.02, 0.036, "#f0c030"), (-0.22, 1.10, 0.025, "#3a8a4a"))):
            p = X(x, y)
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.85" transform="rotate(%d %.4f %.4f)"/>' % (p + (r, r * 0.6, k.c(c), 20 * i - 15) + p))
    inside = "".join(o)
    # skirt of the smock over the legs
    yt = yB - 0.16
    a = hw * 0.985
    hem = yB + C.get("smock_len", 0.40)
    b = hw + C.get("smock_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "sm", X, yt, a, hem, b, g, sw=0.026, folds=((-0.12, yt + 0.12, -0.18, hem - 0.04), (0.14, yt + 0.12, 0.20, hem - 0.04), (0.0, yt + 0.18, 0.01, hem - 0.06)),
                    fold_col=dark)]
    ov.append(_ln([X(0.0, yt), X(0.01, hem)], dark, 0.012))
    if C.get("smock_len", 0.40) > 0.22:
        for s in (-1, 1):
            px0, px1 = 0.12, 0.30
            yy = yt + 0.12
            ov.append(_poly(k, [X(s * px0, yy), X(s * px1, yy), X(s * (px1 - 0.005), yy + 0.14), X(s * (px0 + 0.005), yy + 0.14)], k.c(col["smock"]), 0.012))
            k.ext.append((X(s * px1, yy)[0], yy, 0.03))
    if C.get("paint"):
        p = X(0.14, hem - 0.12)
        ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.025" fill="%s" opacity="0.85"/>' % (p + (k.c("#d8352a"),)))
        p = X(-0.10, hem - 0.20)
        ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.030" ry="0.020" fill="%s" opacity="0.85"/>' % (p + (k.c("#3a7ac0"),)))
    if _POSE7["bulge"] > 0.02:
        ov.append(_bulge(k, X, C, m, _POSE7["bulge"]))
    # band collar (over the neck line)
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (X(-0.17, 0.40) + X(0, 0.47) + X(0.17, 0.40) + (k.ink,)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (X(-0.17, 0.40) + X(0, 0.47) + X(0.17, 0.40) + (k.c(col.get("collar", col["smock"])),)))
    if C.get("bow"):
        bx, by = X(0.0, 0.47)
        bc = k.c(col["bow"])
        for s in (-1, 1):
            ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                      % (bx, by, bx + s * 0.10, by - 0.09, bx + s * 0.17, by - 0.02, bx + s * 0.12, by + 0.08, bx, by, bc, k.ink))
            ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                      % (bx, by + 0.02, bx + s * 0.05, by + 0.12, bx + s * 0.09, by + 0.25, bx + s * 0.03, by + 0.26, bx + s * 0.02, by + 0.12, bx, by + 0.03, bc, k.ink))
        ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.035" ry="0.030" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx, by, bc, k.ink))
        k.ext.append((bx, by + 0.27, 0.03))
    return inside, "", "".join(ov)


def _neck(k, X, col, style, y0=0.40):
    """shirt neck pieces at the throat: 'cravat' (puffed silk knot + pearl pin), 'tie' (four-in-hand), 'bow' (small bow tie),
    'string' (thin string tie), 'none'."""
    o = []
    for s in (-1, 1):              # wing / pointed collar
        o.append(_poly(k, [X(s * 0.10, y0 + 0.01), X(s * 0.015, y0 + 0.07), X(s * 0.085, y0 + 0.13)], k.c(col.get("collar", "#fbfaf6")), 0.012))
    tc, td = k.c(col.get("tie", "#3a2a3a")), k.c(col.get("tie_dark", P._shade(col.get("tie", "#3a2a3a"), 0.7)))
    if style == "cravat":
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                 % (P._smooth_closed([X(-0.07, y0 + 0.08), X(0.07, y0 + 0.08), X(0.09, y0 + 0.20), X(0.0, y0 + 0.30), X(-0.09, y0 + 0.20)]), tc, k.ink))
        o.append(_ln([X(-0.03, y0 + 0.12), X(-0.04, y0 + 0.24)], td, 0.010, ' opacity="0.8"'))
        o.append(_circ(X(0.0, y0 + 0.17), 0.018, k.c("#f6f2ea"), k, 0.008))
    elif style == "tie":
        o.append(_poly(k, [X(-0.026, y0 + 0.10), X(0.026, y0 + 0.10), X(0.036, y0 + 0.32), X(0.0, y0 + 0.37), X(-0.036, y0 + 0.32)], tc, 0.012))
        o.append(_poly(k, [X(-0.030, y0 + 0.07), X(0.030, y0 + 0.07), X(0.024, y0 + 0.11), X(-0.024, y0 + 0.11)], td, 0.011))
    elif style == "bow":
        bx, by = X(0.0, y0 + 0.09)
        for s in (-1, 1):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
                     % (bx, by, bx + s * 0.07, by - 0.035, bx + s * 0.07, by + 0.035, tc, k.ink))
        o.append(_circ((bx, by), 0.018, td, k, 0.009))
    elif style == "string":
        bx, by = X(0.0, y0 + 0.09)
        o.append('<path d="M%.4f,%.4f q-0.04,-0.03 -0.05,0.0 q0.02,0.03 0.05,0 q0.04,-0.03 0.05,0 q-0.02,0.03 -0.05,0 M%.4f,%.4f l-0.02,0.10 M%.4f,%.4f l0.02,0.10" '
                 'fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (bx, by, bx, by, bx, by, tc))
    return "".join(o)


def _cos_frock7(k, C, m):
    """frock coat (director, gentleman) or lounge suit (dealer, C["coat_len"] short): coat in the torso colour, peaked silk
    lapels (C colors lapel), the waistcoat in the opening (colors vest, C["vest_buttons"]), shirt + C["neck"] neckwear, a
    watch chain (C["chain"]), a buttonhole flower (C["flower"]), double-breasted buttons (C["double"]); the coat skirt falls
    over the legs to C["coat_len"] below the torso."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    vb = TT + h * 0.62                      # bottom of the lapels' V
    o = []
    vest = C2._grad(k, "vs", col["vest"], -0.2, 0.2)
    o.append(_poly(k, [X(-0.20, 0.40), X(0.20, 0.40), X(0.19, yB - 0.08), X(0.0, yB - 0.02), X(-0.19, yB - 0.08)], vest, 0.014))
    # shirt V above the waistcoat
    o.append(_poly(k, [X(-0.11, 0.40), X(0.11, 0.40), X(0.0, TT + h * 0.36)], k.c(col.get("shirt", "#fbfaf6")), 0.012))
    o.append(_neck(k, X, col, C.get("neck", "cravat")))
    for i in range(C.get("vest_buttons", 4)):
        y = TT + h * 0.40 + i * (h * 0.45) / max(1, C.get("vest_buttons", 4))
        o.append(_circ(X(0.0, y), 0.014, k.c(col.get("vest_b", "#e0d0a0")), k, 0.007))
    if C.get("chain"):
        a0, a1 = X(0.0, TT + h * 0.62), X(0.17, TT + h * 0.68)
        cm = X(0.09, TT + h * 0.72)
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a0 + cm + a1)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.011" stroke-linecap="round" stroke-dasharray="0.016 0.008"/>' % (d, k.c(GOLD["base"])))
    # coat fronts + lapels
    lap = k.c(col["lapel"])
    for s in (-1, 1):
        front = [X(s * 0.12, 0.38), X(s * 0.20, 0.40), X(s * 0.30, 0.52), X(s * 0.23, 0.56), X(s * 0.17, vb), X(s * 0.15, yB + 0.02), X(s * 0.95, yB + 0.02), X(s * 0.95, 0.30)]
        o.append('<path d="%s" fill="url(#%s_tg)"/>' % (_poly_d(front[3:] + [X(s * 0.95, 0.30), X(s * 0.30, 0.30)]), k.uid))
        lp = [X(s * 0.12, 0.38), X(s * 0.24, 0.42), X(s * 0.33, 0.50), X(s * 0.26, 0.55), X(s * 0.15, vb)]
        o.append(_poly(k, lp, lap, 0.014))
        o.append(_ln([X(s * 0.15, vb), X(s * 0.14, yB + 0.02)], k.ink, 0.016))
    if C.get("flower"):
        fx, fy = X(-0.25, 0.53)
        for a in range(0, 360, 72):
            o.append('<circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.007"/>'
                     % (fx + 0.022 * math.cos(math.radians(a)), fy + 0.022 * math.sin(math.radians(a)), k.c(C["flower"]), k.ink))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s"/>' % (fx, fy, k.c("#f0d050")))
    # coat buttons
    if C.get("double"):
        for y in (vb + 0.04, vb + 0.16):
            for s in (-1, 1):
                o.append(_circ(X(s * 0.22, y), 0.020, k.c(col.get("button", "#2a2228")), k, 0.008))
    else:
        o.append(_circ(X(0.19, vb + 0.06), 0.020, k.c(col.get("button", "#2a2228")), k, 0.008))
    # pocket flaps
    for s in (-1, 1):
        o.append(_ln([X(s * 0.24, yB - 0.12), X(s * 0.40, yB - 0.13)], k.c(col.get("dark", "#1a1418")), 0.020))
    inside = "".join(o)
    yt = yB - 0.10
    hem = yB + C.get("coat_len", 0.50)
    a = hw * 0.99
    b = hw + C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "fc", X, yt, a, hem, b, g, sw=0.026, folds=((-0.14, yt + 0.12, -0.20, hem - 0.04), (0.16, yt + 0.12, 0.22, hem - 0.04)),
                    fold_col=k.c(col.get("dark", "#1a1418")))]
    ov.append(_ln([X(0.14, yt), X(0.10, hem)], k.ink, 0.016))
    if C.get("coat_len", 0.50) < 0.30:
        # lounge suit: the trousers show below the short coat; front edges curve away
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
                  % (X(0.14, yt + 0.05) + X(0.12, hem - 0.02) + X(0.20, hem + 0.01) + (k.c(col.get("dark", "#1a1418")),)))
    return inside, "", "".join(ov)


def _cos_uniform7(k, C, m):
    """kepi uniform tunic (Louvre guard, police agent): stand collar with coloured patches, one or two rows of buttons
    (C["double"]), two flapped chest pockets, a leather belt with a buckle, a short tunic skirt over the hips; an aiguillette
    cord (C["cord"]) on the screen-right chest."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    btn = k.c(col["button"])
    o = []
    for s in (-1, 1):
        x = s * 0.20 * hw / 0.33
        o.append(_poly(k, [X(x - 0.08, 0.62), X(x + 0.08, 0.62), X(x + 0.078, 0.74), X(x - 0.078, 0.74)], k.c(col.get("pocket", col["base"])), 0.012))
        o.append(_poly(k, [X(x - 0.085, 0.60), X(x + 0.085, 0.60), X(x + 0.08, 0.65), X(x, 0.67), X(x - 0.08, 0.65)], k.c(col.get("dark", "#1a2030")), 0.012))
        o.append(_circ(X(x, 0.645), 0.013, btn, k, 0.006))
    if C.get("double"):
        for y in (0.52, 0.68, 0.84, 1.00):
            if y > yB - 0.12:
                break
            for s in (-1, 1):
                o.append(_circ(X(s * 0.085, y), 0.020, btn, k, 0.008))
    else:
        o.append(_ln([X(0.0, 0.45), X(0.0, yB)], k.c(col.get("dark", "#1a2030")), 0.012))
        for y in (0.52, 0.64, 0.76, 0.88, 1.00, 1.12):
            if y > yB - 0.12:
                break
            o.append(_circ(X(0.0, y), 0.018, btn, k, 0.008))
    if C.get("cord"):
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(0.30, 0.44) + X(0.24, 0.62) + X(0.10, 0.60) + X(0.20, 0.70) + X(0.02, 0.66))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (d, k.c(C["cord"])))
    inside = "".join(o)
    yt = yB - 0.12
    hem = yB + C.get("tunic_len", 0.16)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "uk", X, yt, hw * 0.99, hem, hw + 0.05, g, sw=0.024, folds=((-0.10, yt + 0.06, -0.12, hem - 0.03), (0.12, yt + 0.06, 0.14, hem - 0.03)),
                    fold_col=k.c(col.get("dark", "#1a2030")))]
    ov.append(_ln([X(0.0, yt), X(0.0, hem)], k.c(col.get("dark", "#1a2030")), 0.012))
    yb = yB - 0.11
    ov.append(_ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.ink, 0.064))
    ov.append(_ln([X(-hw * 0.99, yb), X(hw * 0.99, yb)], k.c(col.get("belt", "#2a1c18")), 0.044))
    bx, by = X(0.0, yb)
    ov.append('<rect x="%.4f" y="%.4f" width="0.080" height="0.062" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx - 0.04, by - 0.031, btn, k.ink))
    # stand collar with coloured patches
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.072" stroke-linecap="round"/>' % (X(-0.17, 0.41) + X(0, 0.46) + X(0.17, 0.41) + (k.ink,)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.048" stroke-linecap="round"/>' % (X(-0.17, 0.41) + X(0, 0.46) + X(0.17, 0.41) + (k.c(col["base"]),)))
    for s in (-1, 1):
        p = X(s * 0.11, 0.435)
        ov.append('<rect x="%.4f" y="%.4f" width="0.050" height="0.034" rx="0.006" fill="%s" stroke="%s" stroke-width="0.006"/>' % (p[0] - 0.025, p[1] - 0.017, k.c(col["patch"]), k.ink))
    return inside, "", "".join(ov)


def _cos_stripe7(k, C, m):
    """the young painter: a sailor's striped shirt (white, navy horizontal stripes, boat neck), the trousers bowl below with
    a rope belt."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    u = k.uid
    k.defs.append('<pattern id="%s_st" width="0.4" height="0.090" patternUnits="userSpaceOnUse"><rect width="0.4" height="0.036" y="0.027" fill="%s"/></pattern>'
                  % (u, k.c(col["stripe"])))
    o = ['<rect x="-0.8" y="0.42" width="1.6" height="%.4f" fill="url(#%s_st)"/>' % (yb - 0.42, u)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022"/>' % (X(-0.22, 0.40) + X(0, 0.46) + X(0.22, 0.40) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (X(-0.12, 0.70) + X(-0.14, yb - 0.02) + (k.c(col.get("dark", "#c8c8d0")),)))
    o.append(CE._bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.040"/>' % (yb + 0.01, yb + 0.04, yb + 0.01, k.ink))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-dasharray="0.03 0.012"/>' % (yb + 0.01, yb + 0.04, yb + 0.01, k.c(col.get("rope", "#c8a46a"))))
    return "".join(o)


def _cos_dress7(k, C, m):
    """Edwardian lady: high-necked blouse (pin-tucks, lace jabot, cameo brooch at the collar), a fitted jacket bolero in
    colors["jacket"], belt at the waist, the long bell skirt to the ankles (drawn over the legs) with a flounce at the hem."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * 0.70
    o = []
    for x in (-0.06, -0.03, 0.03, 0.06):
        o.append(_ln([X(x, 0.48), X(x, yw - 0.02)], k.c(col.get("blouse_d", "#d8d0c8")), 0.008, ' opacity="0.8"'))
    jab = []
    for i in range(5):
        y = 0.50 + i * 0.065
        jab.append(X(0.0, y))
    for i, p in enumerate(jab):
        o.append('<path d="M%.4f,%.4f q-0.05,0.03 -0.04,0.06 q0.04,0.015 0.08,0 q0.01,-0.03 -0.04,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (p[0], p[1], k.c("#ffffff"), k.ink))
    jc = C2._grad(k, "jk", col["jacket"], -hw, hw)
    for s in (-1, 1):
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                 % (_poly_d([X(s * 0.14, 0.42), X(s * 0.95, 0.30), X(s * 0.95, yw), X(s * 0.18, yw), X(s * 0.12, 0.62)]), jc, k.ink))
        o.append(_ln([X(s * 0.14, 0.44), X(s * 0.12, 0.62), X(s * 0.18, yw)], k.c(col.get("trim", "#e8d8b0")), 0.016))
    inside = "".join(o)
    hem = yB + C["leg"] * C.get("hem_frac", 0.88)
    a = hw * 0.80
    b = hw + C.get("skirt_flare", 0.34)
    sk = C2._grad(k, "sk", col["skirt"], -b, b)
    ov = [C2._skirt(k, "ds", X, yw - 0.02, a, hem, b, sk, sw=0.028,
                    folds=((-0.10, yw + 0.15, -0.22, hem - 0.05), (0.12, yw + 0.15, 0.25, hem - 0.05), (0.0, yw + 0.25, 0.02, hem - 0.06),
                           (-0.25, yw + 0.30, -0.40, hem - 0.06), (0.27, yw + 0.30, 0.42, hem - 0.06)), fold_col=k.c(col["skirt_d"]))]
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050"/>'
              % (X(-b + 0.02, hem - 0.06) + X(0, hem - 0.02) + X(b - 0.02, hem - 0.06) + (k.c(col["skirt_d"]),)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012"/>'
              % (X(-b + 0.02, hem - 0.09) + X(0, hem - 0.05) + X(b - 0.02, hem - 0.09) + (k.ink,)))
    ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.ink, 0.060))
    ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.c(col["belt"]), 0.040))
    # high collar + cameo
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % (X(-0.14, 0.40) + X(0, 0.45) + X(0.14, 0.40) + (k.ink,)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (X(-0.14, 0.40) + X(0, 0.45) + X(0.14, 0.40) + (k.c("#ffffff"),)))
    cx, cy = X(0.0, 0.445)
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.026" ry="0.032" fill="%s" stroke="%s" stroke-width="0.010"/>' % (cx, cy, k.c(col.get("cameo", "#e8a090")), k.c(GOLD["base"])))
    return inside, "", "".join(ov)


def _cos_overalls7(k, C, m):
    """cast3's bib overalls with the plaid pattern under its own id: cast3 names it <uid>_pl, the same id as cast6's pale
    gradient, so with pale > 0 the face would be filled with the plaid.  Renamed to <uid>_ck."""
    n0 = len(k.defs)
    r = C3._cos_overalls(k, C, m)
    a, b = '%s_pl"' % k.uid, '%s_ck"' % k.uid
    a2, b2 = '#%s_pl)' % k.uid, '#%s_ck)' % k.uid
    for i in range(n0, len(k.defs)):
        k.defs[i] = k.defs[i].replace(a, b)
    if isinstance(r, tuple):
        return tuple(x.replace(a2, b2) for x in r)
    return r.replace(a2, b2)


COSTUMES7 = {"overalls7": _cos_overalls7, "smock7": _cos_smock7, "frock7": _cos_frock7, "uniform7": _cos_uniform7, "stripe7": _cos_stripe7, "dress7": _cos_dress7}


# ============================================================================= hats (head frame)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_tophat7(k, C, yaw):
    """the director: tall black silk top hat -- slightly flared crown, a ribbon band, a brim curled up at the sides, a sheen."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    tw, bw, yb, yt = 0.36, 0.32, -0.36, -1.02
    g = CE._gradient(k, "ht", col, x0=-0.38, x1=0.38, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    crown = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - bw, yb, dx - tw, yt, dx, yt - 0.05, dx + tw, yt, dx + bw, yb, dx, yb + 0.04, dx - bw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.9"/>' % (dx - tw, yt, dx, yt + 0.05, dx + tw, yt, k.c(col["dark"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - bw - 0.005, yb - 0.13, dx, yb - 0.09, dx + bw + 0.005, yb - 0.13, dx + bw, yb, dx, yb + 0.04, dx - bw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.026" stroke-linecap="round" opacity="0.75"/>' % (dx - 0.20, yt + 0.08, dx - 0.18, yb - 0.17, k.c(col["shine"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>' % (dx - 0.12, yt + 0.10, dx - 0.11, yb - 0.17, k.c(col["shine"])))
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.54, yb - 0.10, dx - 0.52, yb + 0.02, dx - 0.30, yb + 0.03, dx, yb + 0.10, dx + 0.30, yb + 0.03, dx + 0.52, yb + 0.02, dx + 0.54, yb - 0.10,
        dx + 0.44, yb - 0.02, dx, yb - 0.01, dx - 0.44, yb - 0.02, dx - 0.54, yb - 0.10)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (brim, k.c(col["brim"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.58, yb - 0.10), (dx + 0.58, yb - 0.10), (dx - tw, yt - 0.03), (dx + tw, yt - 0.03), (dx, yb + 0.12)))
    return "".join(o), (dx, yt - 0.04)


def _hat_kepi7(k, C, yaw):
    """kepi: a stiff cylinder leaning forward with a flat top, a coloured band with gold piping and a chin strap, a black
    leather visor, a badge in front."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = dx + 0.10 * yaw
    yb = -0.30
    g = CE._gradient(k, "ht", col, x0=-0.40, x1=0.40, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    body = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.40, yb, dx - 0.34, yb - 0.40, dx + 0.02, yb - 0.46, dx + 0.34, yb - 0.38, dx + 0.40, yb, dx, yb + 0.04, dx - 0.40, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.9"/>' % (dx - 0.34, yb - 0.40, dx + 0.02, yb - 0.34, dx + 0.34, yb - 0.38, k.c(col["dark"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.395, yb - 0.15, dx, yb - 0.11, dx + 0.395, yb - 0.15, dx + 0.40, yb, dx, yb + 0.04, dx - 0.40, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012"/>' % (dx - 0.39, yb - 0.15, dx, yb - 0.11, dx + 0.39, yb - 0.15, k.c(col["piping"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016"/>' % (dx - 0.38, yb - 0.03, dx, yb + 0.01, dx + 0.38, yb - 0.03, k.c(col["piping"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.7"/>' % (dx - 0.24, yb - 0.38, dx - 0.27, yb - 0.18, k.c(col["shine"])))
    # badge
    o.append('<path d="M%.4f,%.4f l0.045,0.035 l-0.015,0.06 l-0.06,0 l-0.015,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (fx, yb - 0.27, k.c(col["piping"]), k.ink))
    visor = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (dx - 0.36, yb - 0.01, fx, yb + 0.16, dx + 0.36, yb - 0.01, fx, yb + 0.05, dx - 0.36, yb - 0.01)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (visor, k.c(col["visor"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.010" opacity="0.5"/>' % (dx - 0.25, yb + 0.04, fx, yb + 0.11, dx + 0.20, yb + 0.05))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.42, yb), (dx + 0.42, yb), (dx, yb - 0.47), (fx, yb + 0.17)))
    return "".join(o), (dx, yb - 0.46)


def _hat_beret7(k, C, yaw):
    """painter: a big soft beret flopping over to one side, a little stalk on top."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = 1.0 if C.get("beret_side", 1) >= 0 else -1.0
    g = CE._gradient(k, "ht", col, x0=-0.55, x1=0.55, mid=0.32)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    pts = [(dx - s * 0.46, -0.27), (dx - s * 0.52, -0.40), (dx - s * 0.36, -0.58), (dx + s * 0.05, -0.64), (dx + s * 0.48, -0.56),
           (dx + s * 0.64, -0.42), (dx + s * 0.62, -0.30), (dx + s * 0.46, -0.27), (dx, -0.25)]
    d = P._smooth_closed(pts)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.8"/>' % (dx - s * 0.40, -0.30, dx + s * 0.05, -0.36, dx + s * 0.55, -0.32, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>' % (dx - s * 0.36, -0.46, dx - s * 0.20, -0.58, dx + s * 0.05, -0.60, k.c(col["shine"])))
    o.append('<path d="M%.4f,-0.635 q0.01,-0.05 0.04,-0.06" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (dx + s * 0.05, k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 0.58, -0.40), (dx + 0.66, -0.40), (dx + s * 0.05, -0.70)))
    return "".join(o), (dx + s * 0.05, -0.66)


def _hat_bighat7(k, C, yaw):
    """the lady: a huge Edwardian picture hat -- a wide tilted brim, a low crown, a ribbon, a cluster of roses on one side
    and an ostrich plume sweeping over the crown."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = 1.0 if C.get("hat_side", 1) >= 0 else -1.0     # flowers + plume side (fixed: no pop when the head turns)
    g = CE._gradient(k, "ht", col, x0=-0.6, x1=0.6, mid=0.30)
    gb = CE._gradient(k, "hb", col, x0=-0.98, x1=0.98, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    cy = -0.38
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.98, cy + 0.06, dx - 0.70, cy - 0.20, dx, cy - 0.22, dx + 0.70, cy - 0.20, dx + 0.98, cy + 0.06, dx + 0.60, cy + 0.20, dx, cy + 0.17,
        dx - 0.60, cy + 0.20, dx - 0.98, cy + 0.06)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (brim, gb, k.ink))
    # plume behind the crown, sweeping up and over to the far side
    pl = [(dx + s * 0.30, cy - 0.10), (dx + s * 0.10, cy - 0.50), (dx - s * 0.30, cy - 0.62), (dx - s * 0.66, cy - 0.46), (dx - s * 0.80, cy - 0.20),
          (dx - s * 0.62, cy - 0.34), (dx - s * 0.30, cy - 0.42), (dx + s * 0.02, cy - 0.30)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(pl), k.c(col["plume"]), k.ink))
    fr = []
    for i in range(7):
        t = i / 6.0
        x = dx + s * (0.20 - 0.90 * t)
        y = cy - 0.30 - 0.30 * math.sin(math.pi * min(1.0, t * 1.1))
        fr.append("M%.4f,%.4f q%.4f,0.05 %.4f,0.10" % (x, y, -s * 0.04, -s * 0.07))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (" ".join(fr), k.c(col.get("plume_d", "#c8b8d0"))))
    crown = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.42, cy - 0.04, dx - 0.44, cy - 0.30, dx - 0.20, cy - 0.36, dx, cy - 0.36, dx + 0.20, cy - 0.36, dx + 0.44, cy - 0.30, dx + 0.42, cy - 0.04)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, g, k.ink))
    rb = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (dx - 0.43, cy - 0.14, dx, cy - 0.10, dx + 0.43, cy - 0.14, dx + 0.42, cy - 0.04, dx, cy, dx - 0.42, cy - 0.04)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (rb, k.c(col["ribbon"]), k.ink))
    # roses
    for i, (x, y, r) in enumerate(((0.40, -0.10, 0.085), (0.55, -0.02, 0.075), (0.30, -0.02, 0.065), (0.62, -0.13, 0.060))):
        rx, ry = dx + s * x, cy + y
        c = col["rose"] if i % 2 == 0 else col.get("rose2", col["rose"])
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (rx, ry, r, k.c(c), k.ink))
        o.append('<path d="M%.4f,%.4f a%.4f,%.4f 0 1 1 %.4f,0" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (rx - r * 0.45, ry, r * 0.45, r * 0.40, r * 0.6, k.c(P._shade(c, 0.7))))
    for (x, y, a) in ((0.70, -0.02, 30), (0.22, 0.04, -40)):
        lx, ly = dx + s * x, cy + y
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.026" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%d %.4f %.4f)"/>'
                 % (lx, ly, k.c("#5a8a4a"), k.ink, s * a, lx, ly))
    o.append('</g>')
    _ext_hat(k, C, ((dx - 1.0, cy + 0.06), (dx + 1.0, cy + 0.06), (dx, cy - 0.40), (dx - s * 0.30, cy - 0.66), (dx - s * 0.82, cy - 0.22)))
    k.ext.append((dx - s * 0.20, cy - 0.62, 0.03))      # hat_top (unrotated) stays inside the bbox at any tilt / roll
    return "".join(o), (dx - s * 0.20, cy - 0.62)


def _hat_bare7(k, C, yaw):
    """no hat: only the hair dict (with hair style "cap" a full head of hair)."""
    return "", (0.0, -0.484)


HATS7 = {"tophat7": _hat_tophat7, "kepi7": _hat_kepi7, "beret7": _hat_beret7, "bighat7": _hat_bighat7, "bare7": _hat_bare7}


# ============================================================================= cast
TROUSERS = dict(color="#4a4450", dark="#2e2a32", cuff="#4a4450", len=0.88, w=0.12)
SHOES = dict(color="#2a2226", cuff="#2a2226", h=0.07, toe=0.14)

NEW_CAST7 = {
    # Vincenzo Peruggia: small Italian glazier, black hair, black moustache, flat cap; charcoal waistcoat over a collarless
    # cream shirt with rolled sleeves, brown-grey trousers
    "vincenzo": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=91.3,
        torso_w=0.70, torso_h=0.90, profile=CE.PROFILE_REGULAR, shift_pow=1.0,
        shoulder=(0.27, 0.48), arm=0.70, hip_x=0.15, leg=1.02, stance=0.07, wide=0.26, limb_w=0.058,
        eye_y=0.040, brow="stroke", brow_th=0.058, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.78, smirk_side=1,
        cheeks="#ec9c88",
        hat="newsboy", hat_style="flatnews", hat_tilt=-4.0, ear_pencil=False, cap_puff=0.7,
        hat_colors=dict(light="#6a6470", base="#47424e", dark="#2c2832", shine="#8e8896", visor="#36323c"),
        hair=dict(color="#1e1a1e", front=0.09, grow=0.22),
        costume="foreman",
        sleeve=dict(color="#efe6d2", dark="#c8bca4", cuff="#f8f2e4", len=0.48, w=0.150, roll=True),
        shorts=dict(color="#5e5448", dark="#3e362e", cuff="#5e5448", len=0.88, w=0.12),
        boots=dict(color="#3a2a22", cuff="#3a2a22", h=0.08, toe=0.14),
        colors=dict(base="#efe6d2", shirt_d="#cfc4ae", vest="#4a4650", vest_d="#2e2a34", button="#c8b890", brass="#c9a44a",
                    pants="#5e5448", moustache="#1e1a1e", moustache_l="#4a4048"),
    ),
    # the same man in the white smock the workers wear on Monday (pose key bulge: the panel under it)
    "vincenzo_smock": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=91.3,
        torso_w=0.70, torso_h=0.90, profile=CE.PROFILE_REGULAR, shift_pow=1.0,
        shoulder=(0.27, 0.48), arm=0.70, hip_x=0.15, leg=1.02, stance=0.07, wide=0.26, limb_w=0.058,
        eye_y=0.040, brow="stroke", brow_th=0.058, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.78, smirk_side=1,
        cheeks="#ec9c88",
        hat="newsboy", hat_style="flatnews", hat_tilt=-4.0, ear_pencil=False, cap_puff=0.7,
        hat_colors=dict(light="#6a6470", base="#47424e", dark="#2c2832", shine="#8e8896", visor="#36323c"),
        hair=dict(color="#1e1a1e", front=0.09, grow=0.22),
        costume="smock7", smock_len=0.42, smock_flare=0.10, pencil=True,
        sleeve=dict(color="#f6f4ee", dark="#c4c8d4", cuff="#ffffff", len=0.80, w=0.170),
        shorts=dict(color="#5e5448", dark="#3e362e", cuff="#5e5448", len=0.88, w=0.12),
        boots=dict(color="#3a2a22", cuff="#3a2a22", h=0.08, toe=0.14),
        colors=dict(base="#f4f2ec", smock="#f4f2ec", dark="#b8bccb", collar="#ffffff", button="#ffffff", pants="#5e5448",
                    moustache="#1e1a1e", moustache_l="#4a4048"),
    ),
    # the museum director: tall, portly, pompous -- black top hat, black frock coat, dove-grey waistcoat, silk cravat,
    # big grey handlebar moustache, monocle, watch chain
    "director": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=12.9,
        torso_w=1.10, torso_h=1.12, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.40, 0.44), arm=0.76, hip_x=0.17, leg=1.46, stance=0.06, wide=0.26, limb_w=0.066,
        eye_y=0.000, brow="stroke", brow_th=0.064, mouth="frown", moustache=True, moustache_style="handlebar", tache_scale=1.25, smirk_side=-1,
        cheeks="#ec8c80", age_lines=True, monocle=True,
        hat="newsboy", hat_style="tophat7", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#5a5462", base="#2c2832", dark="#16131a", shine="#a8a2b4", band="#1a161e", brim="#24202a"),
        hair=dict(color="#b8b0b8", front=0.06, grow=0.22),
        costume="frock7", coat_len=0.52, coat_flare=0.04, neck="cravat", chain=True, vest_buttons=4, double=False, flower="#c8302a",
        sleeve=dict(color="#423c4a", dark="#24202a", cuff="#f6f2ea", len=0.84, w=0.180),
        shorts=dict(color="#4a4652", dark="#2e2a34", cuff="#4a4652", len=0.90, w=0.13),
        boots=dict(color="#16121a", cuff="#16121a", h=0.07, toe=0.15),
        colors=dict(base="#36313e", dark="#16131a", lapel="#4e4858", vest="#a8a4b0", vest_b="#e8dcb0", shirt="#fbfaf6", collar="#ffffff",
                    tie="#5a2a4a", tie_dark="#3a1830", button="#16131a", pants="#4a4652", moustache="#d8d2d8", moustache_l="#ffffff"),
    ),
    # French co-workers who mock him: coworker1 tall and thin in blue overalls and a grey cap, coworker2 stout in a short
    # blue worker's blouse, flat cap, big black moustache
    "coworker1": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=33.8,
        torso_w=0.64, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.76, hip_x=0.16, leg=1.42, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.050, mouth="smirk", moustache=False, pencil_moustache=True, smirk_side=1,
        hat="newsboy", hat_style="flatnews", hat_tilt=-6.0, ear_pencil=False, cap_puff=0.6,
        hat_colors=dict(light="#a8a29a", base="#7e786e", dark="#545048", shine="#cfc8be", visor="#625c54"),
        hair=dict(color="#8a5a2e", front=0.08, grow=0.20),
        costume="overalls7",
        sleeve=dict(color="#d9c9a4", dark="#a8987a", cuff="#e8dab8", len=0.52, w=0.140, roll=True),
        boots=dict(color="#3a2c26", cuff="#3a2c26", h=0.10, toe=0.14),
        colors=dict(base="#d9c9a4", collar="#d9c9a4", denim="#2f5a8a", denim_d="#204470", stitch="#e2b44a", brass="#d9b45a", pants="#2f5a8a"),
    ),
    "coworker2": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=37.2,
        torso_w=1.08, torso_h=1.00, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.40, 0.42), arm=0.72, hip_x=0.17, leg=1.12, stance=0.07, wide=0.28, limb_w=0.066,
        eye_y=-0.010, brow="stroke", brow_th=0.070, mouth="smirk", moustache=True, moustache_style="bushy", tache_scale=1.05, smirk_side=-1,
        cheeks="#ec8070",
        hat="newsboy", hat_style="flatcap", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#6a7660", base="#4a5440", dark="#2e3628", shine="#8e9a82", visor="#3e4636", band="#2e3628"),
        hair=dict(color="#2a2024", front=0.06, grow=0.22),
        costume="smock7", smock_len=0.14, smock_flare=0.06,
        sleeve=dict(color="#4a6a9a", dark="#30486e", cuff="#5a7aaa", len=0.80, w=0.200),
        shorts=dict(color="#6a5a48", dark="#463a2e", cuff="#6a5a48", len=0.88, w=0.15),
        boots=dict(color="#2e2420", cuff="#2e2420", h=0.09, toe=0.15),
        colors=dict(base="#4a6a9a", smock="#4a6a9a", dark="#2e4a74", collar="#3a5a8a", button="#1e2a3a", pants="#6a5a48",
                    moustache="#2a2024", moustache_l="#5a4a50"),
    ),
    # the passing plumber with the key: friendly, round, ginger moustache, brown overalls over a green check shirt, cap
    "plumber": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="regular", seed=46.6,
        torso_w=0.92, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.34, 0.47), arm=0.74, hip_x=0.17, leg=1.18, stance=0.07, wide=0.28, limb_w=0.064,
        eye_y=0.020, brow="dome", brow_th=0.040, mouth="smile", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=1,
        cheeks="#f08a78",
        hat="newsboy", hat_style="flatnews", hat_tilt=3.0, ear_pencil=False, cap_puff=0.9,
        hat_colors=dict(light="#a0703e", base="#7a5028", dark="#4e3218", shine="#c8986a", visor="#5e3e20"),
        hair=dict(color="#b8642a", front=0.08, grow=0.22),
        costume="overalls7",
        sleeve=dict(color="#6a8a5a", dark="#46623a", cuff="#7a9a6a", len=0.52, w=0.150, roll=True),
        boots=dict(color="#3a2c26", cuff="#3a2c26", h=0.11, toe=0.15),
        colors=dict(base="#6a8a5a", check="#2e4a26", collar="#6a8a5a", denim="#8a6a3e", denim_d="#6a4e2a", stitch="#f0d9a0", brass="#d9b45a",
                    pants="#8a6a3e", moustache="#c0682a", moustache_l="#e89a5a"),
    ),
    # the Louvre guard: stout, older, grey walrus moustache, bottle-green uniform with brass buttons, green kepi
    "guard": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=58.4,
        torso_w=1.04, torso_h=1.06, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.38, 0.44), arm=0.74, hip_x=0.17, leg=1.24, stance=0.06, wide=0.26, limb_w=0.066,
        eye_y=0.000, brow="stroke", brow_th=0.064, mouth="dash", moustache=True, moustache_style="walrus", smirk_side=-1, age_lines=True,
        cheeks="#ec9080",
        hat="newsboy", hat_style="kepi7", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#5e7a62", base="#3a5240", dark="#22342a", shine="#8eaa92", band="#2a3c30", piping="#e0b84a", visor="#1e1a1e"),
        hair=dict(color="#c8c2c8", front=0.06, grow=0.20),
        costume="uniform7", double=True, tunic_len=0.16,
        sleeve=dict(color="#3a5240", dark="#22342a", cuff="#e0b84a", len=0.82, w=0.180),
        shorts=dict(color="#2e3830", dark="#1a221c", cuff="#2e3830", len=0.90, w=0.14),
        boots=dict(color="#16121a", cuff="#16121a", h=0.08, toe=0.15),
        colors=dict(base="#3a5240", dark="#22342a", pocket="#3e5844", button="#e0b84a", belt="#2a1c18", patch="#c83a2e", pants="#2e3830",
                    moustache="#ece8ec"),
    ),
    # the painter who comes to copy the picture: tall and thin, red beret, black goatee + handlebar, paint-spattered
    # pale-blue smock, black floppy artist's bow
    "painter": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=66.1,
        torso_w=0.60, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.23, 0.50), arm=0.78, hip_x=0.14, leg=1.46, stance=0.06, wide=0.24, limb_w=0.054,
        eye_y=0.040, brow="stroke", brow_th=0.044, mouth="dash", moustache=True, moustache_style="handlebar", tache_scale=0.80, smirk_side=1,
        goatee=dict(color="#2a2024", light="#6a5a60", len=0.20),
        hat="newsboy", hat_style="beret7", hat_tilt=-8.0, ear_pencil=False, beret_side=1,
        hat_colors=dict(light="#e85a4a", base="#b8302a", dark="#7a1a16", shine="#f08a7a"),
        hair=dict(color="#2a2024", front=0.08, grow=0.20),
        costume="smock7", smock_len=0.46, smock_flare=0.12, paint=True, bow=True,
        sleeve=dict(color="#c8d6e4", dark="#94a6ba", cuff="#d8e4f0", len=0.82, w=0.150),
        shorts=dict(color="#3e3a46", dark="#26222a", cuff="#3e3a46", len=0.88, w=0.11),
        boots=dict(color="#2a2226", cuff="#2a2226", h=0.07, toe=0.14),
        colors=dict(base="#c8d6e4", smock="#c8d6e4", dark="#8a9cb2", collar="#d8e4f0", button="#f4f4f4", bow="#1e1a22", pants="#3e3a46",
                    moustache="#2a2024", moustache_l="#6a5a60"),
    ),
    # the police inspector / agent: slim, black handlebar moustache, navy tunic with silver buttons and a silver cord, navy
    # kepi with silver piping
    "police": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="slim", seed=72.8,
        torso_w=0.72, torso_h=1.06, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.28, 0.50), arm=0.78, hip_x=0.17, leg=1.38, stance=0.08, wide=0.30, limb_w=0.060,
        eye_y=0.030, brow="stroke", brow_th=0.066, mouth="frown", moustache=True, moustache_style="handlebar", tache_scale=1.0, smirk_side=1,
        hat="newsboy", hat_style="kepi7", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#4a5a80", base="#2a3658", dark="#161e36", shine="#8a9ac0", band="#1a2240", piping="#d8dce6", visor="#141018"),
        hair=dict(color="#1e1a1e", front=0.07, grow=0.20),
        costume="uniform7", double=False, cord="#d8dce6", tunic_len=0.20,
        sleeve=dict(color="#2a3658", dark="#161e36", cuff="#d8dce6", len=0.82, w=0.160),
        shorts=dict(color="#24283a", dark="#141824", cuff="#24283a", len=0.90, w=0.12),
        boots=dict(color="#141018", cuff="#141018", h=0.09, toe=0.15),
        colors=dict(base="#2a3658", dark="#161e36", pocket="#2e3a5e", button="#d8dce6", belt="#1a1418", patch="#c83a2e", pants="#24283a",
                    moustache="#1e1a1e", moustache_l="#5a5060"),
    ),
    # a young painter questioned by the police (generic -- no likeness): short, stocky, dark hair, big dark eyes, a navy
    # striped sailor shirt, rope belt, brown trousers, espadrilles
    "young_painter": dict(
        _cast7=True, _cast6=True, _cast4=True, build="regular", seed=84.7,
        torso_w=0.80, torso_h=0.94, profile=CE.PROFILE_REGULAR, shift_pow=1.05,
        shoulder=(0.30, 0.48), arm=0.72, hip_x=0.16, leg=1.10, stance=0.07, wide=0.27, limb_w=0.060,
        eye_y=0.060, eye_scale=1.18, brow="stroke", brow_th=0.054, mouth="frown", moustache=False, smirk_side=1,
        hat="newsboy", hat_style="bare7", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(light="#000000", base="#000000", dark="#000000"),
        hair=dict(color="#24202a", front=0.12, grow=0.24, style="cap", shine="#5a5464"),
        costume="stripe7",
        sleeve=dict(color="#f6f4ee", dark="#c8c8d0", cuff="#1e2a5a", len=0.40, w=0.150),
        shorts=dict(color="#7a5a3a", dark="#523a24", cuff="#7a5a3a", len=0.88, w=0.13),
        boots=dict(color="#d8c8a0", cuff="#a89870", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#f6f4ee", stripe="#1e2a5a", dark="#c8c8d0", pants="#7a5a3a", rope="#c8a46a"),
    ),
    # the Florence art dealer: stout, grey homburg, pince-nez, grey goatee, cream linen lounge suit, bow tie
    "dealer": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="stout", seed=27.9,
        torso_w=1.00, torso_h=1.04, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.37, 0.45), arm=0.74, hip_x=0.16, leg=1.24, stance=0.06, wide=0.26, limb_w=0.064,
        eye_y=0.020, brow="stroke", brow_th=0.054, mouth="smirk", moustache=True, moustache_style="walrus", smirk_side=1, glasses=True,
        goatee=dict(color="#a8a0a8", light="#e8e4e8", len=0.16), cheeks="#ec9488",
        hat="homburg", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#9a96a2", base="#6e6a76", dark="#4a4652", band="#2c2832", brim="#625e6a", edge="#bcb8c4", shine="#dedae6", bow="#3a3640"),
        hair=dict(color="#a8a0a8", front=0.05, grow=0.20),
        costume="frock7", coat_len=0.20, coat_flare=0.06, neck="bow", chain=True, vest_buttons=4, double=True,
        sleeve=dict(color="#d8ccb0", dark="#a89a7e", cuff="#f6f2ea", len=0.84, w=0.180),
        shorts=dict(color="#c8bc9e", dark="#9a8e72", cuff="#c8bc9e", len=0.90, w=0.14),
        boots=dict(color="#6a4428", cuff="#6a4428", h=0.07, toe=0.15),
        colors=dict(base="#d8ccb0", dark="#9a8e72", lapel="#c8bc9e", vest="#8a6a4a", vest_b="#e8dcb0", shirt="#fbfaf6", collar="#ffffff",
                    tie="#7a2a2a", tie_dark="#4a1a1a", button="#6a5440", pants="#c8bc9e", moustache="#bcb4bc"),
    ),
    # crowd: the lady with the big hat, the gentleman with the bowler, the newspaper boy
    "lady": dict(
        _cast7=True, _cast6=True, _cast4=True, build="slim", seed=17.6,
        torso_w=0.60, torso_h=0.92, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.225, 0.52), arm=0.72, hip_x=0.13, leg=1.18, stance=0.04, wide=0.22, limb_w=0.054,
        eye_y=0.050, brow="stroke", brow_th=0.030, mouth="smile", moustache=False, smirk_side=-1, cheeks="#f2a8b0", lashes=True,
        hat="newsboy", hat_style="bighat7", hat_tilt=-7.0, ear_pencil=False,
        hat_colors=dict(light="#f4e4c8", base="#d8bc8e", dark="#9a7a4e", ribbon="#6a3a6a", rose="#d84a5a", rose2="#f2a0b0",
                        plume="#f6f0f8", plume_d="#c8b8d0"),
        hair=dict(color="#8a4a2a", front=0.10, grow=0.24),
        costume="dress7", hem_frac=0.88, skirt_flare=0.36,
        sleeve=dict(color="#6a3a6a", dark="#46224a", cuff="#ffffff", len=0.84, w=0.150),
        boots=dict(color="#2a2026", cuff="#2a2026", h=0.05, toe=0.11),
        colors=dict(base="#fbf6f0", blouse_d="#e0d4d0", jacket="#6a3a6a", trim="#e8d0a0", skirt="#5a3260", skirt_d="#3a1e40", belt="#2a1830",
                    cameo="#f0b0a0", pants="#5a3260"),
    ),
    "gentleman": dict(
        _cast7=True, _cast6=True, _cast4=True, build="regular", seed=22.4,
        torso_w=0.84, torso_h=1.02, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.34, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.052, mouth="frown", moustache=True, moustache_style="walrus", smirk_side=1,
        hat="newsboy", hat_style="derby", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#5a5262", base="#2e2834", dark="#18141c", shine="#9a92a8", band="#141018", brim="#26202c", edge="#6a6276"),
        hair=dict(color="#6a4a36", front=0.07, grow=0.20),
        costume="frock7", coat_len=0.44, coat_flare=0.10, neck="tie", chain=True, vest_buttons=4, double=False,
        sleeve=dict(color="#5e6270", dark="#3e4250", cuff="#f6f2ea", len=0.84, w=0.160),
        shorts=dict(color="#7a7480", dark="#52505a", cuff="#7a7480", len=0.90, w=0.12),
        boots=dict(color="#1a161c", cuff="#1a161c", h=0.07, toe=0.15),
        colors=dict(base="#5e6270", dark="#3a3e4a", lapel="#4e5260", vest="#7a5a3e", vest_b="#e8dcb0", shirt="#fbfaf6", collar="#ffffff",
                    tie="#2a4a6a", tie_dark="#1a3048", button="#2a2228", pants="#7a7480", moustache="#6a4a36"),
    ),
    "newsboy": dict(
        _cast7=True, _cast6=True, _cast4=True, _cast3=True, build="boy", seed=5.9,
        torso_w=0.62, torso_h=0.78, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.80, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.050, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f4a49a", freckles=True,
        hat="newsboy", hat_style="flatnews", hat_tilt=-8.0, ear_pencil=False, cap_puff=1.15,
        hat_colors=dict(light="#9a8a6a", base="#74644a", dark="#4a3e2c", shine="#bcae8e", visor="#5a4c36"),
        hair=dict(color="#c87a3a", front=0.08, grow=0.16),
        costume="workjacket", jacket_len=0.14, jacket_flare=0.06,
        sleeve=dict(color="#8a6a4a", dark="#5e4630", cuff="#9a7a5a", len=0.62, w=0.140, roll=True),
        shorts=dict(color="#4a4450", dark="#2e2a32", cuff="#4a4450", len=0.55, w=0.13),
        boots=dict(color="#3d2c24", cuff="#3d2c24", h=0.10, toe=0.13, soft=True),
        colors=dict(base="#8a6a4a", dark="#5e4630", lapel="#7a5a3e", pocket="#7e5e40", button="#3d3340", shirt="#efe6d2",
                    susp="#4a3a2a", susp_b="#c9a44a", pants="#4a4450", scarf="#e8d8b0", scarf_d="#b8a47e", scarf_s="#c8302a"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast7.py canvas): every arm preset
# with every film-7 prop at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects, every STORY7 pose and the
# cycles of the member; >= 0.32 D head room.  CANVAS7_LIE: the members that lie down (pose key lie).
CANVAS7 = {
    "vincenzo": (-1.5000, -4.3125, 1.5000, 0.1250),
    "vincenzo_smock": (-1.5000, -4.3125, 1.5000, 0.1250),
    "director": (-1.5625, -5.0625, 1.5625, 0.1250),
    "coworker1": (-1.5000, -4.9375, 1.5000, 0.1250),
    "coworker2": (-1.5625, -4.5625, 1.5625, 0.1250),
    "plumber": (-1.5625, -4.5625, 1.5625, 0.1250),
    "guard": (-1.5625, -4.7500, 1.5625, 0.1250),
    "painter": (-1.4375, -5.0000, 1.4375, 0.1250),
    "police": (-1.5000, -4.9375, 1.5000, 0.1250),
    "young_painter": (-1.5000, -4.3750, 1.5000, 0.1250),
    "dealer": (-1.5625, -4.6875, 1.5625, 0.1250),
    "lady": (-1.4375, -4.5000, 1.4375, 0.3125),
    "gentleman": (-1.5000, -4.8125, 1.5000, 0.1250),
    "newsboy": (-1.3750, -3.8125, 1.3750, 0.1250),
}
CANVAS7_LIE = {"vincenzo": (-2.0625, -1.4375, 2.0625, 0.25), "vincenzo_smock": (-2.0625, -1.4375, 2.0625, 0.25)}


# ============================================================================= figure wrapper: lie down, grip anchors
def _lie(f, ang):
    """rotate the whole figure by `ang` degrees about the hip (90 = lying on the back with the head to screen-left, -90 head
    to screen-right) and set it down: feet_y stays, the lowest point of the rotated drawing rests on it; anchors["feet"] is
    the middle of the lying body on that line (the sprite pipeline places it there)."""
    a = -ang
    hx, hy = f["anchors"]["hip"]
    x0, y0, x1, y1 = f["bbox"]
    corners = [_rot(x - hx, y - hy, a) for (x, y) in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    bot = max(c[1] for c in corners)
    shift = f["feet_y"] - (hy + bot)
    # a body lying flat is narrower than its bbox corners: use the extent of the figure's anchors for the resting line
    pts = [_rot(v[0] - hx, v[1] - hy, a) for v in f["anchors"].values()]
    rest = max(p[1] for p in pts) + 0.06
    shift = f["feet_y"] - (hy + max(rest, bot - 0.25))

    def T(p):
        q = _rot(p[0] - hx, p[1] - hy, a)
        return (hx + q[0], hy + q[1] + shift)
    an = dict((n, T(v)) for n, v in f["anchors"].items())
    cs = [T(c) for c in ((x0, y0), (x1, y0), (x0, y1), (x1, y1))]
    bx0, bx1 = min(c[0] for c in cs), max(c[0] for c in cs)
    by0, by1 = min(c[1] for c in cs), max(c[1] for c in cs)
    an["feet"] = ((bx0 + bx1) / 2, f["feet_y"])
    svg = '<g transform="translate(%.4f %.4f) rotate(%.3f %.4f %.4f)">%s</g>' % (0.0, shift, a, hx, hy, f["svg"])
    return dict(f, svg=svg, bbox=(bx0, by0, bx1, max(by1, f["feet_y"])), anchors=an)


def figure(cast_name, pose=None, uid="p"):
    f = _O7["figure"](cast_name, pose, uid)
    if _POSE7["an"]:
        a = dict(f["anchors"])
        sx, sy = 1.0, 1.0
        sq = pose.get("squash") if isinstance(pose, dict) else None
        if isinstance(sq, (int, float)) and not isinstance(sq, bool):
            sx = sy = float(sq)
        elif isinstance(sq, (tuple, list)) and len(sq) >= 2 and all(isinstance(v, (int, float)) for v in sq[:2]):
            sx, sy = float(sq[0]), float(sq[1])
        sx = _clamp(_num(sx, 1.0), 0.3, 2.5)
        sy = _clamp(_num(sy, 1.0), 0.3, 2.5)
        mir = isinstance(pose, dict) and bool(pose.get("mirror"))
        for n, v in _POSE7["an"].items():
            if mir:
                n = n[:-2] + ("_r" if n.endswith("_l") else "_l")
            a[n] = ((-v[0] if mir else v[0]) * sx, v[1] * sy)
        f = dict(f, anchors=a)
    if isinstance(pose, dict) and pose.get("lie") is not None and isinstance(cast_name, str) and cast_name in P.CAST:
        ang = _f(pose.get("lie"), 0.0, -100.0, 100.0)
        if pose.get("mirror"):
            ang = -ang                  # mirror flips the lying direction too (sprites' head_flip relies on it)
        if abs(ang) > 0.01:
            f = _lie(f, ang)
    return f


# ============================================================================= story poses
def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball"):
    """put the free hand on the far grip of the piece the other hand holds (anchor grip_far_<side>)."""
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=1.3, shape=shape, layer="top")


WORKERS = (("coworker1", ""), ("coworker2", "_coworker2"))
CROWD = (("lady", ""), ("gentleman", "_gentleman"), ("newsboy", "_newsboy"))


def _story():
    S, M = {}, {}
    V, VS = "vincenzo", "vincenzo_smock"
    # --- vincenzo (normal clothes)
    S["vincenzo_stand"] = (V, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
    S["vincenzo_mocked"] = (V, dict(yaw=-0.25, pitch=0.70, expr="sad", fx=["blush"], head_roll=8, lean=3, squash=(1.02, 0.96), gaze=(-0.5, 0.6),
                                    arm_r=dict(hand=(0.10, 0.82), bend=0.7), arm_l=dict(hand=(-0.12, 0.84), bend=0.7), legs="narrow"))
    M["vincenzo_mocked"] = dict(note="hurt by the mockery ('macaroni!'): head down, cheeks red, hands fiddling with the cap at the belt line")
    S["vincenzo_glare"] = (V, dict(yaw=-0.40, pitch=0.30, expr="angry", head_roll=-4, gaze=(-0.9, -0.1),
                                   arm_r=dict(hand=(0.30, 0.82), bend=0.4), arm_l=dict(hand=(-0.30, 0.82), bend=0.4), legs="stand"))
    M["vincenzo_glare"] = dict(note="the grudge: a side glare at the laughing co-workers (screen-left), fists clenched")
    S["vincenzo_hide_closet"] = (V, dict(yaw=0.20, pitch=0.20, expr="worried", fx=["sweat"], head_roll=-6, lean=8, gaze=(0.8, 0.0),
                                         arm_r=dict(hand=(0.40, 0.52), bend=-0.6, stretch=1.2), prop_r="lantern",
                                         arm_l=dict(hand=(-0.14, 0.62), bend=0.7), legs="crouch"))
    M["vincenzo_hide_closet"] = dict(note="Sunday night, crouched in the storage closet with a small lantern, listening")
    S["vincenzo_sleep"] = (V, dict(yaw=0.0, pitch=-0.2, expr="asleep", mouth="smile", fx=["zzz"], lie=90, t=0.3,
                                   arm_r=dict(hand=(0.18, 0.92), bend=0.6), arm_l=dict(hand=(-0.18, 0.92), bend=0.6), legs="narrow"))
    M["vincenzo_sleep"] = dict(note="asleep on his back, smiling (pose key lie=90: head to screen-left; canvas CANVAS7_LIE['vincenzo']); "
                                    "anchor feet = the middle of the body on the mattress line")
    S["vincenzo_peek_bed"] = (V, dict(yaw=0.60, pitch=0.70, expr="smirk", head_roll=-10, lean=34, gaze=(0.9, 0.7), head_dy=0.10,
                                      arm_r=dict(hand=(0.72, 0.95), bend=-0.3, stretch=1.3, shape="open"),
                                      arm_l=dict(hand=(0.10, 1.05), bend=0.5), legs=dict(preset="crouch", crouch=0.36, stride=0.3)))
    M["vincenzo_peek_bed"] = dict(note="bent low beside the bed, lifting the blanket edge (screen-right hand) to peek at the trunk underneath")
    S["vincenzo_offer"] = (V, dict(yaw=0.45, pitch=-0.10, expr="smug", head_roll=-5, gaze=(0.8, 0.0),
                                   arm_r=dict(hand=(0.46, 0.40), bend=-0.5, stretch=1.3), prop_r="mona_panel", panel_side=1,
                                   arm_l=dict(hand=(-0.20, 0.82), bend=0.6), legs="stand"))
    M["vincenzo_offer"] = dict(note="Florence 1913: shows the panel to the dealer (screen-right); prop_tip_r = panel centre")
    S["vincenzo_arrested"] = (V, dict(yaw=-0.30, pitch=0.75, expr="sad", head_roll=6, lean=4, squash=(1.0, 0.97),
                                      arm_r=dict(hand=(-0.05, 0.86), bend=0.9, layer="back"), arm_l=dict(hand=(-0.12, 0.84), bend=0.9, layer="back"),
                                      legs="narrow"))
    M["vincenzo_arrested"] = dict(note="arrested: hands behind the back, head down (police_arrest grips his upper arm)")
    S["vincenzo_walk"] = (V, cycle(V, 0.30, "walk", base=dict(expr="neutral")))
    # --- vincenzo in the white smock
    S["vincenzo_smock_stand"] = (VS, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
    S["vincenzo_sneak"] = (VS, cycle(VS, 0.30, "sneak", base=dict(expr="worried", gaze=(-0.8, 0.0))))
    M["vincenzo_sneak"] = dict(note="one frame of cycle('vincenzo_smock', f / 32, 'sneak'); tiptoe crouch, glancing back")
    S["vincenzo_lift"] = (VS, dict(yaw=0.55, pitch=-0.50, expr="determined", head_roll=-6, gaze=(0.7, -0.9), lean=-4,
                                   arm_l=dict(hand=(0.30, -0.18), bend=-0.8, stretch=1.3, layer="front"), prop_l="mona_framed",
                                   panel_grip="bottom", panel_side=1, legs="wide"))
    M["vincenzo_lift"] = dict(note="lifting the framed painting off its four hooks (screen-right, above his head): both hands under the bottom "
                                   "corners (panel_grip='bottom', panel_side=1); anchor prop_tip_l = frame centre, grip_far_l = the right "
                                   "hand's corner; raise both hands' y together to lift")
    S["vincenzo_carry"] = (VS, dict(yaw=0.55, pitch=0.15, expr="worried", fx=["sweat"], head_roll=-4, gaze=(-0.7, 0.0), lean=6,
                                    arm_r=dict(hand=(0.55, 0.44), bend=-0.4, stretch=1.3), prop_r="mona_framed",
                                    legs=dict(preset="step", stride=0.4)))
    M["vincenzo_carry"] = dict(note="carrying the framed painting toward the service stair, glancing back (other hand on grip_far_r)")
    S["vincenzo_unframe"] = (VS, dict(yaw=0.35, pitch=0.55, expr="determined", fx=["sweat"], head_roll=-4, lean=10, gaze=(0.4, 0.8),
                                      arm_r=dict(hand=(0.55, 0.62), bend=-0.4, stretch=1.3), prop_r="mona_panel",
                                      legs=dict(preset="crouch", crouch=0.22)))
    M["vincenzo_unframe"] = dict(note="in the service staircase: the bare panel out of its frame (put the empty frame on the steps as set dressing)")
    S["vincenzo_hide_panel"] = (VS, dict(yaw=0.25, pitch=0.25, expr="smirk", bulge=1.0, head_roll=4, gaze=(-0.8, 0.1),
                                         arm_r=dict(hand=(0.16, 0.92), bend=0.7, shape="open"), arm_l=dict(hand=(-0.20, 1.02), bend=0.7, shape="open"),
                                         legs="narrow"))
    M["vincenzo_hide_panel"] = dict(note="the panel hidden under the smock: pose key bulge 0..1 (animate 0 -> 1 as he slides it in), hands pressing it flat")
    S["vincenzo_sweat"] = (VS, dict(yaw=0.40, pitch=-0.10, expr="worried", bulge=1.0, sweat=1.0, pale=0.5, head_roll=6, gaze=(0.9, -0.2),
                                    arm_r=dict(hand=(0.80, 0.18), bend=-0.6, stretch=1.3, shape="open"), arm_l=dict(hand=(-0.18, 1.00), bend=0.7, shape="open"),
                                    legs="narrow"))
    M["vincenzo_sweat"] = dict(note="the exit door is locked: tugging the handle (screen-right hand), sweating (pose key sweat 0..1), a bit pale")
    S["vincenzo_nervous_smile"] = (VS, dict(yaw=0.45, pitch=-0.05, expr="grinning", bulge=1.0, sweat=0.6, head_roll=-6, gaze=(0.9, 0.0),
                                            arm_r=dict(hand=(0.22, 0.95), bend=0.7, shape="open"), arm_l=dict(hand=(-0.20, 1.00), bend=0.7, shape="open"),
                                            legs="narrow"))
    M["vincenzo_nervous_smile"] = dict(note="the plumber greets him: a stiff nervous grin back, hands still pressing the bulge, sweat")
    S["vincenzo_smug_walk"] = (VS, cycle(VS, 0.30, "walk", base=dict(expr="smug", bulge=1.0, pitch=-0.35, head_roll=-4), arms="l"))
    S["vincenzo_smug_walk"][1]["arm_r"] = dict(hand=(0.14, 0.94), bend=0.7, shape="open")
    M["vincenzo_smug_walk"] = dict(note="walking out with the bulge, chin up, smug: cycle(VS, f / 28, 'walk', base=dict(expr='smug', bulge=1, ...), "
                                        "arms='l') then set arm_r to keep the hand on the bulge")
    S["vincenzo_smock_walk"] = (VS, cycle(VS, 0.30, "walk", base=dict(expr="neutral")))
    # --- director
    S["director_boast"] = ("director", dict(yaw=0.30, pitch=-0.60, expr="smug", mouth="talk_b", head_roll=-8, lean=-6, gaze=(0.3, -0.5),
                                            arm_r=dict(hand=(0.56, -0.62), shape="point", bend=-1.0, stretch=1.3),
                                            arm_l=dict(hand=(-0.16, 0.66), bend=0.8), legs="wide"))
    M["director_boast"] = dict(note="'steal her? you might as well steal the towers of Notre-Dame!': chin up, finger to the sky, other hand "
                                    "on the lapel; animate mouth with talk_mouth()")
    S["director_proud"] = ("director", dict(yaw=0.20, pitch=-0.45, expr="smug", head_roll=-5, arm_r="akimbo", arm_l=dict(hand=(-0.16, 0.66), bend=0.8), legs="wide"))
    S["director_shocked"] = ("director", dict(yaw=-0.10, pitch=-0.20, expr="shocked", pale=1.0, sweat=0.7, head_roll=4, squash=(0.97, 1.04), lean=-6,
                                              arm_r=dict(hand=(0.42, -0.10), bend=-0.8, shape="open", stretch=1.2),
                                              arm_l=dict(hand=(-0.40, -0.12), bend=-0.8, shape="open", stretch=1.2), legs="narrow"))
    M["director_shocked"] = dict(note="the painting is gone: pale (pose key pale), sweating, both hands up")
    S["director_walk"] = ("director", cycle("director", 0.30, "walk", base=dict(expr="smug", pitch=-0.4)))
    # --- co-workers
    for c, sfx in WORKERS:
        S["coworkers_laugh" + sfx] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=-6, t=0.4,
                                              arm_r=dict(hand=(0.80, 0.02), shape="point", bend=-0.6, stretch=1.3),
                                              arm_l=dict(hand=(-0.30, 0.95), bend=0.9), legs="wide"))
        S["coworkers_point" + sfx] = (c, dict(yaw=0.40, pitch=-0.25, expr="smug", mouth="talk_a", head_roll=6,
                                              arm_r=dict(hand=(0.92, -0.02), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
        S["coworkers_walk" + sfx] = (c, cycle(c, 0.30, "walk", base=dict(expr="smirk")))
    M["coworkers_laugh"] = dict(note="laughing at him and pointing (screen-right) -- '_coworker2' for the stout one; mirror=True to face left")
    M["coworkers_point"] = dict(note="mocking point + jeer ('macaroni!'): animate mouth with talk_mouth()")
    # --- plumber
    S["plumber_open_door"] = ("plumber", dict(yaw=0.65, pitch=0.10, expr="happy", head_roll=-4, lean=6, gaze=(0.9, 0.2),
                                              arm_r=dict(hand=(0.82, 0.30), bend=-0.4, stretch=1.3), prop_r=dict(type="key", angle=0),
                                              arm_l=dict(hand=(-0.20, 0.80), bend=0.6), legs=dict(preset="step", stride=0.4)))
    M["plumber_open_door"] = dict(note="turning the big key in the lock (screen-right): prop_tip_r = the key's bit; animate prop angle 0 -> 90 for the turn")
    S["plumber_greet"] = ("plumber", dict(yaw=-0.30, pitch=-0.20, expr="happy", mouth="talk_a", head_roll=8,
                                          arm_l=dict(hand=(-0.50, -0.40), shape="open", bend=-1.0, stretch=1.2),
                                          arm_r=dict(hand=(0.30, 0.78), bend=0.5), prop_r=dict(type="key", angle=80), legs="stand"))
    M["plumber_greet"] = dict(note="'bonjour!': friendly wave to vincenzo (screen-left), key still in the other hand")
    S["plumber_walk"] = ("plumber", cycle("plumber", 0.30, "walk", base=dict(expr="happy")))
    # --- guard
    S["guard_at_ease"] = ("guard", dict(yaw=0.25, pitch=-0.20, expr="neutral", arm_r="behind", arm_l="behind", legs="stand"))
    S["guard_shrug"] = ("guard", dict(yaw=0.15, pitch=-0.20, expr="unimpressed", mouth="talk_a", head_roll=10, squash=(1.0, 0.98),
                                      arm_r="shrug", arm_l="shrug", legs="stand"))
    M["guard_shrug"] = dict(note="'the photographers must have taken it': a shrug, palms up")
    S["guard_yawn"] = ("guard", dict(yaw=0.10, pitch=-0.50, expr="asleep", mouth=("open", 0.20, 0.26), head_roll=-8, lean=-5,
                                     arm_r=dict(hand=(0.30, 0.10), bend=-0.9, stretch=1.2), arm_l=dict(hand=(-0.50, -0.70), bend=-1.0, stretch=1.3, shape="open"),
                                     legs="wide"))
    M["guard_yawn"] = dict(note="a huge yawn (mouth ('open', w, h)), hand patting the mouth / one arm stretched up")
    S["guard_walk"] = ("guard", cycle("guard", 0.30, "walk", base=dict(expr="neutral", pitch=-0.2)))
    # --- painter
    S["painter_ask"] = ("painter", dict(yaw=0.30, pitch=-0.15, expr="worried", mouth="talk_o", head_roll=10, gaze=(0.6, -0.2),
                                        arm_r=dict(hand=(0.62, 0.30), shape="open", bend=-0.6, stretch=1.3),
                                        arm_l=dict(hand=(-0.55, 0.30), shape="open", bend=-0.6, stretch=1.3), legs="stand"))
    M["painter_ask"] = dict(note="'where is she?': open palms to the empty wall, head tilted")
    S["painter_point"] = ("painter", dict(yaw=0.55, pitch=-0.40, expr="shocked", head_roll=-4, gaze=(0.9, -0.5),
                                          arm_r=dict(hand=(0.90, -0.42), shape="point", bend=-0.6, stretch=1.3),
                                          arm_l=dict(hand=(-0.25, 0.70), bend=0.6), prop_l="palette", legs="wide"))
    M["painter_point"] = dict(note="pointing up at the empty spot with the four hooks (screen-right), palette in the other hand")
    S["painter_paint"] = ("painter", dict(yaw=0.65, pitch=0.0, expr="neutral", head_roll=-6, gaze=(0.9, 0.0),
                                          arm_r=dict(hand=(0.80, 0.10), bend=-0.5, stretch=1.3), prop_r="paintbrush",
                                          arm_l=dict(hand=(-0.20, 0.55), bend=0.6), prop_l="palette", legs="stand"))
    S["painter_walk"] = ("painter", cycle("painter", 0.30, "walk", base=dict(expr="happy", pitch=-0.2)))
    # --- police
    S["police_stand"] = ("police", dict(yaw=0.30, pitch=-0.25, expr="determined", arm_r="akimbo", arm_l="behind", legs="wide"))
    S["police_search"] = ("police", dict(yaw=0.55, pitch=0.50, expr="determined", head_roll=-8, lean=22, gaze=(0.8, 0.6),
                                         arm_r=dict(hand=(0.78, 0.55), bend=-0.4, stretch=1.3), prop_r="lantern",
                                         arm_l=dict(hand=(-0.05, 0.90), bend=0.6, layer="back"), legs=dict(preset="crouch", crouch=0.20, stride=0.3)))
    M["police_search"] = dict(note="searching every corner: bent forward, lantern held out (screen-right)")
    S["police_question"] = ("police", dict(yaw=-0.40, pitch=-0.20, expr="angry", mouth="talk_b", head_roll=-5,
                                           arm_l=dict(hand=(-0.92, 0.05), shape="point", bend=-0.6, stretch=1.3), arm_r="akimbo", legs="wide"))
    M["police_question"] = dict(note="questioning (pointing at someone on screen-left, e.g. young_painter)")
    S["police_arrest"] = ("police", dict(yaw=-0.45, pitch=0.0, expr="determined", mouth="talk_a", head_roll=-3, lean=-4,
                                         arm_l=dict(hand=(-0.82, 0.42), shape="open", bend=-0.5, stretch=1.3),
                                         arm_r=dict(hand=(0.40, -0.50), shape="point", bend=-1.0, stretch=1.3), legs="wide"))
    M["police_arrest"] = dict(note="the arrest: open hand gripping vincenzo's arm (screen-left), the other finger raised ('you are under arrest')")
    S["police_walk"] = ("police", cycle("police", 0.30, "march", base=dict(expr="determined")))
    # --- young painter
    S["young_painter_questioned"] = ("young_painter", dict(yaw=0.30, pitch=0.10, expr="worried", fx=["sweat"], head_roll=8, gaze=(0.7, 0.0), lean=-4,
                                                            arm_r=dict(hand=(0.40, 0.25), shape="open", bend=-0.6, stretch=1.2),
                                                            arm_l=dict(hand=(-0.38, 0.25), shape="open", bend=-0.6, stretch=1.2), legs="narrow"))
    M["young_painter_questioned"] = dict(note="questioned by the police (screen-right): hands up, nervous")
    S["young_painter_indignant"] = ("young_painter", dict(yaw=0.40, pitch=-0.40, expr="furious", mouth="talk_b", fx=[dict(type="anger_fill", level=0.4)],
                                                           head_roll=-8, lean=-4,
                                                           arm_l=dict(hand=(-0.10, 0.60), shape="point", bend=0.8),
                                                           arm_r=dict(hand=(0.80, -0.10), shape="open", bend=-0.6, stretch=1.3), legs="wide"))
    M["young_painter_indignant"] = dict(note="'me? a thief?!': indignant, pointing at himself, anger fill")
    # --- dealer
    S["dealer_inspect"] = ("dealer", dict(yaw=-0.35, pitch=0.25, expr="stunned", head_roll=6, lean=6, gaze=(-0.6, 0.3), head_dy=0.03,
                                          arm_l=dict(hand=(-0.58, 0.30), bend=-0.5, stretch=1.3), prop_l="mona_panel", panel_side=-1,
                                          arm_r=dict(hand=(0.30, 0.10), bend=-0.8, stretch=1.2), legs="stand"))
    M["dealer_inspect"] = dict(note="peering at the panel through the pince-nez (held screen-left): it is the real one")
    S["dealer_signal"] = ("dealer", dict(yaw=0.55, pitch=-0.10, expr="wink", head_roll=-6, gaze=(0.9, 0.0),
                                         arm_r=dict(hand=(0.75, 0.28), shape="open", bend=-0.5, stretch=1.3),
                                         arm_l=dict(hand=(-0.06, 0.20), shape="point", bend=0.9), legs="stand"))
    M["dealer_signal"] = dict(note="secret signal to the police behind the door (screen-right): beckoning open hand, a wink; animate hand x 0.65..0.85")
    S["dealer_smile"] = ("dealer", dict(yaw=-0.30, pitch=-0.10, expr="happy", mouth="talk_a", head_roll=4, arm_r="akimbo",
                                        arm_l=dict(hand=(-0.60, 0.30), shape="open", bend=-0.6, stretch=1.2), legs="stand"))
    S["dealer_walk"] = ("dealer", cycle("dealer", 0.30, "walk", base=dict(expr="smirk")))
    # --- crowd
    for c, sfx in CROWD:
        S["crowd_stare" + sfx] = (c, dict(yaw=0.20, pitch=-0.55, expr="stunned", head_roll=-4, gaze=(0.2, -0.9),
                                          arm_r=dict(hand=(0.20, 0.70), bend=0.6), arm_l=dict(hand=(-0.22, 0.72), bend=0.6), legs="stand"))
        S["crowd_walk" + sfx] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
        S["crowd_point" + sfx] = (c, dict(yaw=0.45, pitch=-0.45, expr="excited", mouth="talk_o", head_roll=6,
                                          arm_r=dict(hand=(0.80, -0.40), shape="point", bend=-0.8, stretch=1.3), arm_l=dict(hand=(-0.22, 0.72), bend=0.6), legs="stand"))
    M["crowd_stare"] = dict(note="queuing to stare at the empty wall (up, screen-right): lady; _gentleman, _newsboy")
    S["crowd_stare_gentleman"][1].update(arm_r=dict(hand=(0.42, 0.62), bend=0.4), prop_r=dict(type="stick", angle=95))
    S["newsboy_shout"] = ("newsboy", dict(yaw=0.30, pitch=-0.45, expr="shouting", mouth="talk_b", head_roll=-8, lean=-4,
                                          arm_r=dict(hand=(0.52, -0.40), bend=-1.0, stretch=1.3), prop_r="newspaper", panel_side=1,
                                          arm_l=dict(hand=(-0.40, 0.30), shape="open", bend=-0.6, stretch=1.2), legs="wide"))
    M["newsboy_shout"] = dict(note="'extra! the Mona Lisa stolen!': front page waved high (prop newspaper = the Mona Lisa front page)")
    S["gentleman_read"] = ("gentleman", dict(yaw=0.15, pitch=0.45, expr="shocked", head_roll=-4,
                                             arm_r=dict(hand=(0.36, 0.42), bend=-0.6, stretch=1.2), prop_r="newspaper",
                                             legs="stand"))
    M["gentleman_read"] = dict(note="reading the front page, shocked; the other hand holds grip_far_r")
    S["lady_gasp"] = ("lady", dict(yaw=-0.20, pitch=-0.20, expr="shocked", head_roll=6, lean=-4,
                                   arm_r=dict(hand=(0.06, 0.20), bend=-0.9, shape="open", layer="top"), arm_l=dict(hand=(-0.30, 0.76), bend=0.6), legs="narrow"))
    M["lady_gasp"] = dict(note="a gloved hand to the mouth, gasping")
    # the free hand on the far grip of a two-handed piece
    _two_hands(S, "vincenzo_lift", hand_from="l", bend=-0.6)
    S["vincenzo_lift"][1]["arm_r"]["layer"] = "front"
    _two_hands(S, "vincenzo_carry")
    _two_hands(S, "vincenzo_unframe")
    _two_hands(S, "gentleman_read")
    for n in ("vincenzo_walk", "vincenzo_sneak", "vincenzo_smock_walk", "director_walk", "coworkers_walk", "plumber_walk", "guard_walk",
              "painter_walk", "police_walk", "dealer_walk", "crowd_walk"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cast7.cycle(); animate: cycle(cast, frame / N, mode, facing, base, arms) with "
                                  "N = 28 walk / 16 run / 32 sneak / 24 march"))
    return S, M


STORY7, STORY7_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast7_registered", False):
        CE.register_stage()
        if not STORY7:
            s, m = _story()
            STORY7.update(s)
            STORY7_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "figure"):
        _O7[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P.figure = figure
    CE.COSTUMES.update(COSTUMES7)
    CE.HATS.update(HATS7)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS7 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP7)
    for n, c in NEW_CAST7.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS7)
    P._cast7_registered = True
    s, m = _story()
    STORY7.update(s)
    STORY7_META.update(m)
    P.STORY.update(STORY7)
    CE.register_stage()


register()
