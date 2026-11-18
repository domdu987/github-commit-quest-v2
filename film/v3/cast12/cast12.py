#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast12.py -- the cast of film 12 ("the walking umbrella": London, 1750s, Jonas Hanway, hackney coachmen, rain) for the v2 puppet,
as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast12"); import cast12     # registers on import (idempotent)
    import puppet                                                      # same module object, now with the new members
    cast, pose = cast12.STORY12["hanway_walk_umbrella"]
    f = puppet.figure(cast, pose, "f")

Nothing in v2/puppet or v3/cast .. cast10 is edited.  The module adds entries to their tables and wraps the puppet helpers on top of
cast10's wrappers (each falls through for everything it does not handle, so every earlier member draws exactly as before):
    cast_ext.COSTUMES  frockcoat12 (gentleman's frock coat, waistcoat, stock, jabot), greatcoat12 (many-caped drab greatcoat + scarf),
                       dress12 (gown, fichu, shawl, apron)
    cast_ext.HATS      tricorn12 (powdered wig with side curls + queue under a tricorn), roundfelt12, flatcap12, slouch12, bonnet12
    cast_ext.CANVAS    one feet-relative sprite canvas per member
    _norm   reads this module's pose keys (umb_open, umb_col, egg_splat, leaf_stick, mud, soaked, hat_off, coach_box, whip_t, purse_open, t)
    _face   mutton-chop whiskers (CAST chops12), red bulb nose / long nose (CAST nose12)
    _ink_limb  white stockings + buckled shoes (CAST stocking12)
    _prop   umbrella_black / umbrella_black_closed / umbrella_pink / umbrella_pink_closed / umbrella_small, whip, cabbage, egg, purse,
            coins, tricorn_held, wig
    figure  mud splatter + wet drips overlays, the coach-box seat
New cast: hanway, coachman, coachman_b, coachman_c, crowd_man_a .. crowd_man_d, crowd_woman_a, crowd_woman_b, passenger_a, passenger_b.
STORY12 / STORY12_META: story poses.  cycle(), talk_mouth(), blink_at(), NOD: as cast6 (re-exported).
Standalone pieces: umbrella_svg, cabbage_svg, egg_svg, egg_splat_svg, purse_svg, coin_svg, whip_svg, coach_box_svg.
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
import cast6 as C6      # noqa: E402
import cast2 as C2      # noqa: E402
import cast3 as C3      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW12 = ("hanway", "coachman", "coachman_b", "coachman_c", "crowd_man_a", "crowd_man_b", "crowd_man_c", "crowd_man_d",
         "crowd_woman_a", "crowd_woman_b", "passenger_a", "passenger_b")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O12 = {}
_POSE12 = {"umb": 1.0, "ucol": None, "egg": 0.0, "leaf": 0.0, "mud": 0.0, "soaked": 0.0, "hat_off": 0.0, "wig_off": 0.0, "box": 0.0, "whip_t": 0.0,
           "purse": 0.5, "t": 0.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES
_hash, _splat, _drip = C10._hash, C10._splat, C10._drip


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


# ============================================================================= colours
UMB = {
    "black": dict(base="#2a2832", light="#5e5c74", dark="#121018", rib="#8886a0", bind="#a8a6bc"),
    "pink": dict(base="#f2609e", light="#ff9ec9", dark="#c42f78", rib="#ffd0e4", bind="#fff0f6"),
    "maroon": dict(base="#8c2c40", light="#c05468", dark="#541624", rib="#e8a0aa", bind="#e8c8c8"),
    "green": dict(base="#2f6e4e", light="#5a9c78", dark="#173a28", rib="#a8d8bc", bind="#c8e0d0"),
    "navy": dict(base="#34509a", light="#6a86c8", dark="#1a2a5a", rib="#b0c4f0", bind="#d0d8f0"),
    "tan": dict(base="#b8905a", light="#e0be88", dark="#765630", rib="#f4e0b8", bind="#f4ead4"),
}
LACE = dict(base="#fff3f8", dark="#e98bb6", deep="#c4507e")
WOOD12 = dict(light="#d8a468", base="#9a6434", dark="#5e3a1c")
STEEL12 = dict(light="#c8ccd8", base="#8a8e9e", dark="#4a4e5e")
BRASS12 = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
CABB = dict(light="#c4ec88", base="#7cc050", dark="#3f8a34", deep="#2a6428", vein="#e6f6c0")
EGG = dict(light="#fffaf0", base="#f0e2c8", dark="#c8b48e")
YOLK = dict(light="#ffd868", base="#f2a81c", dark="#c07810")
MUD = dict(base="#6a4a2e", light="#8e6a44", dark="#3e2a18")
LEATHER = dict(light="#b07a48", base="#7e5230", dark="#4a2e18")
COIN = dict(light="#fff2a0", base="#f0c030", dark="#a8780c")
WATER = dict(base="#bcd8f0", dark="#6a98c8")


# ============================================================================= umbrella (props)
UMB_TOP = -1.95           # the apex of the canopy above the hand (D, prop scale 1.0)
UMB_HANDLE = 0.30         # the end of the crook below the hand


def _umb_y(o, R):
    """(top, rim, H) of the canopy for opening o (0 furled .. 1 open)."""
    H = 1.15 - 0.60 * o
    return UMB_TOP, UMB_TOP + H, H


def _umb_body(k, tag, o, pal, frill=False, egg=0.0, leaf=0.0):
    """umbrella in its own frame: hand at (0, 0), shaft along -y, canopy apex at UMB_TOP, rim between UMB_TOP + 0.55 (open) and
    + 1.15 (furled), the crook handle below the hand.  o = 0 furled .. 1 fully open (the dome 2.0 wide)."""
    o = _clamp(_num(o, 1.0), 0.0, 1.0)
    R = 0.105 + 0.895 * (o ** 0.85)
    top, rim, H = _umb_y(o, R)
    ink = k.ink
    out = []
    # crook handle (wood) and shaft
    out.append('<path d="M0,0 L0,0.20 Q0,0.34 -0.12,0.33 Q-0.20,0.31 -0.19,0.22" fill="none" stroke="%s" stroke-width="0.082" stroke-linecap="round" stroke-linejoin="round"/>' % ink)
    out.append('<path d="M0,0 L0,0.20 Q0,0.34 -0.12,0.33 Q-0.20,0.31 -0.19,0.22" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round" stroke-linejoin="round"/>' % k.c(WOOD12["base"]))
    out.append('<path d="M0.012,0.02 L0.012,0.20" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % k.c(WOOD12["light"]))
    out.append('<path d="M0,0.02 L0,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (top, ink))
    out.append('<path d="M0,0.02 L0,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (top, k.c(STEEL12["base"])))
    out.append('<path d="M0.008,0 L0.008,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (rim + 0.1, k.c(STEEL12["light"])))
    # canopy outline: over the top by an elliptical arc, the scalloped hem back
    sd = 0.075 * o
    tips = [R * math.cos(math.radians(a)) for a in (0, 45, 90, 135, 180)]      # right .. left
    hem = ""
    for i in range(4):
        x1, x2 = tips[i], tips[i + 1]
        hem += " Q%.4f,%.4f %.4f,%.4f" % ((x1 + x2) / 2, rim - 2 * sd, x2, rim)
    d = "M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f%s Z" % (-R, rim, R, H, R, rim, hem)
    g = _lin(k, "uc" + tag, pal["light"], pal["base"], pal["dark"], -R, 0, R, 0)
    # a back inner panel (the underside, seen through the hem) so an open dome reads from below
    out.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, ink))
    # ribs
    rb = []
    for x in tips:
        pts = []
        for j in range(9):
            s = j / 8.0
            pts.append((x * s, rim - H * math.sqrt(max(0.0, 1.0 - s * s * (1.0 if R < 0.12 else 1.0)))))
        if abs(x) < 1e-6:
            pts = [(0.0, top), (0.0, rim)]
        rb.append("M" + " L".join("%.4f,%.4f" % p for p in pts))
    out.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.85"/>' % (" ".join(rb), k.c(pal["rib"]), 0.012 + 0.006 * o))
    if o > 0.5:
        # sheen on the screen-left of the dome, a darker band under the rim
        out.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.026" stroke-linecap="round" opacity="0.30"/>'
                   % (-R * 0.80, rim - H * 0.40, -R * 0.62, rim - H * 0.82, -R * 0.20, rim - H * 0.96))
    # tip ferrules
    for x in tips:
        out.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, rim, 0.020 + 0.010 * o, k.c(STEEL12["light"]), ink))
    # finial
    out.append('<path d="M-0.030,%.4f L0,%.4f L0.030,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
               % (top + 0.02, top - 0.10, top + 0.02, k.c(BRASS12["base"]), ink))
    if o < 0.25:
        # the strap and button of a furled umbrella, folds
        ys = rim - 0.30
        out.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.070" rx="0.012" fill="%s" stroke="%s" stroke-width="0.012"/>' % (-R - 0.012, ys, 2 * R + 0.024, k.c(pal["dark"]), ink))
        out.append('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/>' % (0.0, ys + 0.035, k.c(STEEL12["light"]), ink))
        out.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>'
                   % (-R * 0.45, top + 0.20, -R * 0.40, rim - 0.40, R * 0.45, top + 0.20, R * 0.40, rim - 0.40, k.c(pal["dark"])))
    if frill:
        out.append(_lace_frill(k, tips, rim, sd, R, o))
    if egg > 0.02:
        out.append(_egg_on_canopy(k, R, top, rim, H, egg))
    if leaf > 0.5:
        out.append(_leaf_on_canopy(k, R, top, rim, H))
    return "".join(out), (R, top, rim)


def _lace_frill(k, tips, rim, sd, R, o):
    """the lace frill: a double row of small scallops hanging from the hem, with eyelet dots and a gathered ruffle line just above."""
    n = max(4, int(round(18 * (0.35 + 0.65 * o))))
    x0, x1 = -R, R
    out = []

    def y_edge(x):
        # y of the scalloped hem at x (between tips)
        for i in range(4):
            xa, xb = tips[i], tips[i + 1]
            lo, hi = min(xa, xb), max(xa, xb)
            if lo - 1e-9 <= x <= hi + 1e-9:
                t = (x - xa) / (xb - xa) if abs(xb - xa) > 1e-9 else 0.0
                return rim - 4 * sd * t * (1 - t)
        return rim
    fh = 0.105 + 0.050 * o
    for rowi, (h, col, ot) in enumerate(((fh * 1.0, LACE["base"], LACE["dark"]),)):
        for i in range(n):
            xa = x0 + (x1 - x0) * i / n
            xb = x0 + (x1 - x0) * (i + 1) / n
            ya, yb = y_edge(xa), y_edge(xb)
            xm, ym = (xa + xb) / 2, (y_edge((xa + xb) / 2))
            out.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                       % (xa, ya - 0.012, xm - (xb - xa) * 0.30, ym + h * 1.9, xb, yb - 0.012 + 0.0, xb, yb - 0.02, k.c(col), k.c(ot)))
            out.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (xm, ym + h * 0.30, 0.010 + 0.004 * o, k.c(LACE["deep"])))
    # ruffle line above the hem
    pts = []
    for i in range(0, 41):
        x = x0 + (x1 - x0) * i / 40.0
        pts.append((x, y_edge(x) - 0.020 - 0.012 * math.sin(i * 1.6)))
    out.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.9"/>' % (" L".join("%.4f,%.4f" % p for p in pts), k.c(LACE["base"])))
    return "".join(out)


def _egg_on_canopy(k, R, top, rim, H, lev):
    """an egg smashed on the dome: a lumpy albumen splat with a yolk, shell bits and runs down the black cloth."""
    x, y = R * 0.20, rim - H * 0.70
    r = (0.16 + 0.07 * lev) * (0.5 + 0.5 * min(1.0, R / 0.6))
    o = [_splat(k, x, y, r, EGG["light"], 4.4)]
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x - 0.02, y + 0.01, r * 0.50, k.c(YOLK["base"]), k.c(YOLK["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.9"/>' % (x - 0.05, y - 0.02, r * 0.16, k.c(YOLK["light"])))
    for dx, ln in ((-0.10, 0.20), (0.06, 0.28), (0.17, 0.17)):
        xx = x + dx * (r / 0.2)
        L = ln * lev
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (xx, y + r * 0.5, xx, y + r * 0.5 + L, k.c(EGG["base"])))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.022" fill="%s"/>' % (xx, y + r * 0.5 + L, k.c(EGG["base"])))
    for dx, dy, a in ((0.20, -0.06, 20), (-0.22, -0.02, -30), (0.05, -0.20, 60)):
        o.append('<path d="M%.4f,%.4f l0.050,-0.020 l0.010,0.050 Z" fill="%s" stroke="%s" stroke-width="0.007" transform="rotate(%d %.4f %.4f)"/>'
                 % (x + dx * (r / 0.2), y + dy * (r / 0.2), k.c(EGG["light"]), k.c(EGG["dark"]), a, x + dx, y + dy))
    return "".join(o)


def _leaf_on_canopy(k, R, top, rim, H):
    x, y = -R * 0.25, rim - H * 0.62
    o = ['<g transform="translate(%.4f %.4f) rotate(-25)">' % (x, y)]
    o.append('<path d="M-0.26,0 Q-0.20,-0.20 0,-0.17 Q0.22,-0.20 0.28,0.02 Q0.22,0.19 0,0.15 Q-0.20,0.17 -0.26,0 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (k.c(CABB["base"]), k.ink))
    o.append('<path d="M-0.22,0 L0.24,0.01 M-0.08,0 L0.02,-0.12 M0.06,0.01 L0.14,-0.10 M-0.08,0 L0.0,0.11 M0.06,0.01 L0.14,0.10" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c(CABB["vein"]))
    o.append('</g>')
    return "".join(o)


UMB_KINDS = {"umbrella_black": ("black", None, False), "umbrella_black_closed": ("black", 0.0, False),
             "umbrella_pink": ("pink", None, True), "umbrella_pink_closed": ("pink", 0.0, True), "umbrella_small": (None, None, False)}


# ============================================================================= whip, cabbage, egg, purse, coins, wig
WHIP_STOCK = 1.05


def _whip_stock(k):
    o = ['<path d="M-0.20,0 L%.4f,-0.012" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (WHIP_STOCK, k.ink)]
    o.append('<path d="M-0.20,0 L%.4f,-0.012" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (WHIP_STOCK, k.c(WOOD12["base"])))
    o.append('<path d="M-0.20,-0.010 L%.4f,-0.020" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (WHIP_STOCK, k.c(WOOD12["light"])))
    o.append('<path d="M-0.20,0 L0.14,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c("#3a2a22"))
    for x in (-0.14, -0.04, 0.06):
        o.append('<path d="M%.4f,-0.026 L%.4f,0.026" stroke="%s" stroke-width="0.010"/>' % (x, x + 0.03, k.c("#7a5a48")))
    for x in (0.30, 0.78, 1.00):
        o.append('<path d="M%.4f,-0.024 L%.4f,0.020" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x, x, k.c("#a8302a")))
    return "".join(o)


def _whip_lash(k, T, u, t):
    """the lash from the stock tip T (screen frame), first along u (unit), then drooping and curling by gravity; t animates a wave."""
    w = math.sin(t * 2 * math.pi) * 0.12
    c1 = (T[0] + 0.65 * u[0], T[1] + 0.65 * u[1])
    c2 = (T[0] + 1.25 * u[0] + w, T[1] + 1.25 * u[1] + 0.35)
    e = (T[0] + 1.55 * u[0] - 0.28 * w, T[1] + 1.45 * u[1] + 1.10)
    d = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (T + c1 + c2 + e)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.044" stroke-linecap="round"/>' % (d, k.ink)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (d, k.c("#e8d8b0")))
    o.append('<path d="M%.4f,%.4f l0.07,0.10 M%.4f,%.4f l-0.02,0.12 M%.4f,%.4f l-0.08,0.08" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (e + e + e + (k.c("#d8c8a0"),)))
    return "".join(o), e


def _cabbage_body(k, cx=0.0, cy=0.0, r=0.19, rot=0.0, tag="cb"):
    gid = "%s_%s" % (k.uid, tag)
    k.defs.append('<radialGradient id="%s" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  % (gid, k.c(CABB["light"]), k.c(CABB["base"]), k.c(CABB["dark"])))
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f)">' % (cx, cy, rot, r / 0.19)]
    o.append('<circle cx="0" cy="0" r="0.19" fill="url(#%s)" stroke="%s" stroke-width="0.016"/>' % (gid, k.ink))
    o.append('<path d="M-0.16,0.04 Q-0.08,-0.10 0.05,-0.04 Q0.16,0.02 0.12,0.12 M-0.10,-0.12 Q0.02,-0.20 0.12,-0.10 M-0.15,-0.02 Q-0.12,0.10 -0.04,0.16" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(CABB["deep"]))
    o.append('<path d="M-0.02,-0.01 L0.0,0.12 M-0.02,-0.01 L-0.10,0.07 M-0.02,-0.01 L0.07,0.06 M-0.10,-0.12 L-0.06,-0.06 M0.12,-0.10 L0.07,-0.05" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>' % k.c(CABB["vein"]))
    o.append('<path d="M-0.12,-0.10 Q-0.08,-0.15 -0.02,-0.16" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.55"/>')
    o.append('</g>')
    return "".join(o)


def _egg_body(k, cx=0.0, cy=0.0, s=1.0, rot=0.0, tag="eg"):
    gid = "%s_%s" % (k.uid, tag)
    k.defs.append('<radialGradient id="%s" cx="0.35" cy="0.30" r="0.8"><stop offset="0" stop-color="%s"/><stop offset="0.6" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  % (gid, k.c(EGG["light"]), k.c(EGG["base"]), k.c(EGG["dark"])))
    return ('<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f)"><path d="M0,-0.115 C0.08,-0.115 0.10,0.00 0.09,0.04 C0.07,0.10 0.03,0.115 0,0.115 C-0.03,0.115 -0.07,0.10 -0.09,0.04 C-0.10,0.00 -0.08,-0.115 0,-0.115 Z" '
            'fill="url(#%s)" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/><path d="M-0.05,-0.06 Q-0.04,-0.09 -0.01,-0.095" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/></g>'
            % (cx, cy, rot, s, gid, k.ink))


def _coin(k, x, y, r=0.05, ry=None, tilt=0.0):
    ry = r * 0.55 if ry is None else ry
    return ('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.010" transform="rotate(%.1f %.4f %.4f)"/>'
            '<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" transform="rotate(%.1f %.4f %.4f)"/>'
            % (x, y, r, ry, k.c(COIN["base"]), k.ink, tilt, x, y, x - r * 0.6, y - ry * 0.1, r * 0.6, ry * 0.7, x + r * 0.1, y - ry * 0.75, k.c(COIN["light"]), tilt, x, y))


def _purse_body(k, open_=0.5):
    """a leather coin purse hanging from the hand (hand at the gathered neck (0, 0)); coins show over the mouth when open_ > 0."""
    o = []
    g = _lin(k, "pu", LEATHER["light"], LEATHER["base"], LEATHER["dark"], -0.16, 0, 0.16, 0)
    if open_ > 0.15:
        for i, (x, y, a) in enumerate(((-0.05, 0.02, -10), (0.04, 0.0, 8), (0.0, -0.05, 0), (0.09, 0.04, 20))):
            if open_ > 0.15 + 0.2 * i:
                o.append(_coin(k, x, y, 0.045, 0.030, a))
    o.append('<path d="M-0.030,0.02 Q-0.19,0.09 -0.17,0.24 Q-0.15,0.36 0,0.37 Q0.15,0.36 0.17,0.24 Q0.19,0.09 0.030,0.02 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.10,0.12 Q-0.13,0.22 -0.08,0.30" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.35"/>')
    o.append('<path d="M-0.05,0.045 Q0,0.08 0.05,0.045" fill="none" stroke="%s" stroke-width="0.012"/>' % k.c(LEATHER["dark"]))
    o.append('<path d="M-0.045,0.035 Q0,0.065 0.045,0.035" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c("#d8c090"))
    o.append('<path d="M0.02,0.05 Q0.10,0.10 0.09,0.20 M-0.01,0.05 Q-0.03,0.12 -0.06,0.17" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % k.c("#d8c090"))
    o.append('<circle cx="0.09" cy="0.21" r="0.016" fill="%s" stroke="%s" stroke-width="0.006"/>' % (k.c("#d8c090"), k.ink))
    o.append(_coin(k, 0.02, 0.27, 0.030, 0.030, 0))
    return "".join(o)


def _coins_body(k):
    """three coins held on a flat hand: two stacked, one leaning (hand at (0, 0), coins above)."""
    o = []
    for (x, y, a) in ((-0.07, -0.03, -6), (0.06, -0.035, 8)):
        o.append(_coin(k, x, y, 0.062, 0.036, a))
    o.append(_coin(k, -0.07, -0.075, 0.062, 0.036, -6))
    o.append(_coin(k, 0.0, -0.13, 0.066, 0.040, 4))
    return "".join(o)


def _wig_body(k, drip=0.0):
    o = []
    g = _lin(k, "wg", "#ffffff", "#ece8f0", "#bdb6cc", -0.3, 0, 0.3, 0)
    o.append('<path d="M-0.28,0.05 Q-0.34,-0.12 -0.18,-0.22 Q0,-0.30 0.18,-0.22 Q0.34,-0.12 0.28,0.05 Q0.20,0.12 0.10,0.04 Q0,0.14 -0.10,0.04 Q-0.20,0.12 -0.28,0.05 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M-0.20,-0.04 Q-0.12,-0.14 -0.02,-0.08 M0.02,-0.16 Q0.12,-0.20 0.20,-0.08 M-0.22,0.02 Q-0.12,-0.04 -0.04,0.02" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c("#b4aec4"))
    for i, x in enumerate((-0.14, 0.0, 0.13)):
        L = 0.14 + 0.10 * ((i * 7) % 3)
        o.append('<path d="M%.4f,0.10 L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x, x, 0.10 + L * (0.7 + 0.5 * drip), k.c(WATER["base"])))
        o.append('<path d="M%.4f,0.10 L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (x, x, 0.10 + L * (0.7 + 0.5 * drip), "#ffffff"))
        o.append('<path d="M%.4f,%.4f q-0.024,0.04 0,0.058 q0.024,-0.018 0,-0.058 Z" fill="%s" stroke="%s" stroke-width="0.007"/>' % (x, 0.10 + L * (0.7 + 0.5 * drip) + 0.01, k.c(WATER["base"]), k.c(WATER["dark"])))
    return "".join(o)


# ============================================================================= tricorn (hat, also as a held prop)
def _tricorn_body(k, col, dx=0.0, fx=0.0, tag="tri"):
    """the tricorn seen from the front, head frame: a low crown over a flat folded front brim whose point dips to y -0.26, corners up
    at the sides, a light braid binding along the lower edges."""
    o = []
    g = CE._gradient(k, tag, col, x0=-0.72, x1=0.72, mid=0.34)
    # crown
    crown = ("M%.4f,-0.44 C%.4f,-0.60 %.4f,-0.70 %.4f,-0.705 C%.4f,-0.70 %.4f,-0.60 %.4f,-0.44 Z"
             % (-0.46 + dx, -0.48 + dx, -0.26 + dx, dx, 0.26 + dx, 0.48 + dx, 0.46 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.64 %.4f,-0.675" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>' % (-0.32 + dx, -0.30 + dx, -0.14 + dx, k.c(col["light"])))
    # front flap
    # drawn as one smooth shape: corners up-turned, the point down in front
    fl = ("M%.4f,-0.595 Q%.4f,-0.46 %.4f,-0.505 Q%.4f,-0.465 %.4f,-0.505 Q%.4f,-0.46 %.4f,-0.595 Q%.4f,-0.52 %.4f,-0.46 Q%.4f,-0.32 %.4f,-0.255 Q%.4f,-0.32 %.4f,-0.46 Q%.4f,-0.52 %.4f,-0.595 Z"
          % (-0.76 + dx, -0.70 + dx, -0.44 + dx, dx, 0.44 + dx, 0.70 + dx, 0.76 + dx, 0.62 + dx, 0.60 + dx, 0.30 + fx, fx, -0.30 + fx, -0.60 + dx, -0.62 + dx, -0.76 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (fl, g, k.ink))
    bind = ("M%.4f,-0.520 Q%.4f,-0.32 %.4f,-0.285 Q%.4f,-0.32 %.4f,-0.520"
            % (-0.62 + dx, -0.40 + fx * 0.6 + dx * 0.4, fx, 0.40 + fx * 0.6 + dx * 0.4, 0.62 + dx))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round" stroke-linejoin="round"/>' % (bind, k.c(col.get("bind", "#bfbccb"))))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7" transform="translate(0 -0.020)"/>' % (bind, k.ink))
    # cockade button and loop at the front point
    o.append('<circle cx="%.4f" cy="-0.375" r="0.028" fill="%s" stroke="%s" stroke-width="0.010"/>' % (fx * 0.9, k.c(col.get("btn", "#d8d4e0")), k.ink))
    # a sheen on the flap
    o.append('<path d="M%.4f,-0.51 Q%.4f,-0.47 %.4f,-0.45" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.28"/>' % (-0.52 + dx, -0.42 + dx, -0.30 + fx))
    return "".join(o)


def _wig(k, col, dx, yaw, tag="wg", natural=False):
    """powdered wig: a dome over the head, a curved hairline, two rolled side curls (buckles) each side, and a queue with a black ribbon
    hanging behind the head on the side away from where he faces."""
    o = []
    wc = col.get("wig", "#f4f1f6")
    wd = col.get("wig_d", "#cdc7d8")
    g = CE._gradient(k, tag, dict(light="#ffffff", base=wc, dark=wd), x0=-0.6, x1=0.6, mid=0.40)
    a = abs(yaw)
    # queue behind (drawn first, so the head and wig cover its root)
    sd = -1.0 if yaw >= -0.02 else 1.0
    qx = sd * (0.50 + 0.02 * a)
    if not natural:
      o.append('<path d="M%.4f,0.04 Q%.4f,0.22 %.4f,0.50 Q%.4f,0.64 %.4f,0.66 Q%.4f,0.58 %.4f,0.46 Q%.4f,0.22 %.4f,0.06 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (qx - sd * 0.03, qx + sd * 0.08, qx + sd * 0.12, qx + sd * 0.10, qx + sd * 0.02, qx - sd * 0.02, qx - sd * 0.06, qx - sd * 0.02, qx - sd * 0.10, g, k.ink))
    if not natural:
      o.append('<path d="M%.4f,0.18 l%.4f,0.04 M%.4f,0.52 l%.4f,0.04" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (qx - sd * 0.02, sd * 0.12, qx + sd * 0.02, sd * 0.10, k.c("#1e1c24")))
    # dome
    dome = ("M%.4f,0.10 C%.4f,-0.12 %.4f,-0.50 %.4f,-0.60 C%.4f,-0.67 %.4f,-0.67 %.4f,-0.60 C%.4f,-0.50 %.4f,-0.12 %.4f,0.10 "
            "L%.4f,0.04 Q%.4f,-0.22 %.4f,-0.30 Q%.4f,-0.35 %.4f,-0.30 Q%.4f,-0.22 %.4f,0.04 Z"
            % (-0.52 + dx, -0.62 + dx, -0.60 + dx, -0.32 + dx, -0.10 + dx, 0.10 + dx, 0.32 + dx, 0.60 + dx, 0.62 + dx, 0.52 + dx,
               0.47 + dx, 0.44 + dx, 0.28 + dx, dx, -0.28 + dx, -0.44 + dx, -0.47 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (dome, g, k.ink))
    # side curls
    for s in ((-1, 1) if not natural else ()):
        far = (s * yaw > 0.0)
        sx = 1.0 - (0.30 * a if far else 0.0)
        for j, (cy, rr) in enumerate(((0.00, 0.080), (0.145, 0.072))):
            cx = dx + s * (0.545 - (0.05 * a if far else 0.0)) * 1.0 + (0.0 if not far else 0.0)
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, cy, rr * 1.15 * sx, rr, g, k.ink))
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                     % (cx - rr * 0.6 * sx, cy + rr * 0.15, cx, cy - rr * 0.6, cx + rr * 0.6 * sx, cy + rr * 0.1, k.c(wd)))
    # powder curls on the dome
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.60 %.4f,-0.54 M%.4f,-0.48 Q%.4f,-0.55 %.4f,-0.50" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>'
             % (-0.30 + dx, -0.22 + dx, -0.12 + dx, 0.10 + dx, 0.20 + dx, 0.34 + dx, k.c(wd)))
    return "".join(o)


def _hat_tricorn12(k, C, yaw):
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.20 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    if _POSE12["wig_off"] > 0.5:
        o.append('</g>')
        return "".join(o), (0.0, -0.50)
    if C.get("wig", True):
        o.append(_wig(k, col, dx, yaw))
    elif C.get("hair") and C["hair"].get("color"):
        hc = C["hair"]["color"]
        o.append(_wig(k, dict(wig=hc, wig_d=P._shade(hc, 0.72)), dx, yaw, "hr", True))
    if not _POSE12["hat_off"] > 0.5:
        o.append(_tricorn_body(k, col, dx, fx))
        top = (dx, -0.705)
        ex = ((-0.78 + dx, -0.58), (0.78 + dx, -0.58), (dx, -0.72), (fx, -0.25))
    else:
        top = (dx, -0.67)
        ex = ((-0.64 + dx, -0.10), (0.64 + dx, -0.10), (dx, -0.68))
    o.append('</g>')
    CE._ext(k, C, ex + ((-0.68 + dx, 0.30), (0.68 + dx, 0.30)))
    for sd in (-1.0, 1.0):
        CE._ext(k, C, ((sd * 0.64 + dx, 0.66),))
    return "".join(o), top


def _hat_roundfelt12(k, C, yaw):
    """low round felt hat of a hackney coachman: a flat-topped dome crown, a band with a brass buckle, a narrow curled brim."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.12 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "rf", col, x0=-0.62, x1=0.62, mid=0.34)
    crown = ("M%.4f,-0.34 C%.4f,-0.46 %.4f,-0.62 %.4f,-0.64 C%.4f,-0.65 %.4f,-0.65 %.4f,-0.64 C%.4f,-0.62 %.4f,-0.46 %.4f,-0.34 Z"
             % (-0.46 + dx, -0.47 + dx, -0.40 + dx, -0.22 + dx, -0.10 + dx, 0.10 + dx, 0.22 + dx, 0.40 + dx, 0.47 + dx, 0.46 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,-0.50 Q%.4f,-0.60 %.4f,-0.625" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>' % (-0.34 + dx, -0.32 + dx, -0.16 + dx, k.c(col["light"])))
    o.append('<path d="M%.4f,-0.350 Q%.4f,-0.320 %.4f,-0.350 L%.4f,-0.440 Q%.4f,-0.412 %.4f,-0.440 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (-0.465 + dx, dx, 0.465 + dx, 0.480 + dx, dx, -0.480 + dx, k.c(col["band"]), k.ink))
    o.append('<rect x="%.4f" y="-0.435" width="0.090" height="0.100" rx="0.012" fill="none" stroke="%s" stroke-width="0.034"/><rect x="%.4f" y="-0.435" width="0.090" height="0.100" rx="0.012" fill="none" stroke="%s" stroke-width="0.018"/>'
             % (fx - 0.04, k.ink, fx - 0.04, k.c(BRASS12["base"])))
    brim = ("M%.4f,-0.46 Q%.4f,-0.30 %.4f,-0.31 Q%.4f,-0.25 %.4f,-0.31 Q%.4f,-0.30 %.4f,-0.46 Q%.4f,-0.37 %.4f,-0.38 Q%.4f,-0.37 %.4f,-0.46 Z"
            % (-0.68 + dx, -0.62 + dx, -0.34 + dx, fx, 0.34 + dx, 0.62 + dx, 0.68 + dx, 0.58 + dx, 0.30 + dx, -0.30 + dx, -0.58 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, k.c(col["brim"]), k.ink))
    o.append('<path d="M%.4f,-0.37 Q%.4f,-0.325 %.4f,-0.37" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (-0.40 + dx, fx, 0.40 + dx, k.c(col["light"])))
    o.append('</g>')
    CE._ext(k, C, ((-0.70 + dx, -0.40), (0.70 + dx, -0.40), (dx, -0.66), (fx, -0.26)))
    return "".join(o), (dx, -0.645)


def _hat_flatcap12(k, C, yaw):
    """a flat cloth cap with a short peak and a button (the short coachman, bald under it)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    vx = 0.30 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "fc", col, x0=-0.56, x1=0.56, mid=0.34)
    dome = ("M%.4f,-0.26 C%.4f,-0.34 %.4f,-0.56 %.4f,-0.585 C%.4f,-0.60 %.4f,-0.60 %.4f,-0.585 C%.4f,-0.56 %.4f,-0.34 %.4f,-0.26 Q%.4f,-0.22 %.4f,-0.26 Z"
            % (-0.50 + dx, -0.56 + dx, -0.46 + dx, -0.20 + dx, -0.08 + dx, 0.08 + dx, 0.20 + dx, 0.46 + dx, 0.56 + dx, 0.50 + dx, vx * 0.5, -0.50 + dx))
    vis = ("M%.4f,-0.28 Q%.4f,-0.23 %.4f,-0.28 Q%.4f,-0.14 %.4f,-0.12 Q%.4f,-0.14 %.4f,-0.28 Z"
           % (vx - 0.36, vx, vx + 0.36, vx + 0.30, vx, vx - 0.30, vx - 0.36))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (vis, k.c(col["visor"]), k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (dome, g, k.ink))
    for ui in (-0.7, -0.3, 0.1, 0.5):
        o.append('<path d="M%.4f,-0.575 Q%.4f,-0.40 %.4f,-0.27" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (dx + ui * 0.10, dx + ui * 0.35, dx + ui * 0.45, k.c(col["dark"])))
    for yy in (-0.50, -0.40, -0.32):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.5"/>' % (-0.52 + dx, yy, dx, yy + 0.04, 0.52 + dx, yy, k.c(col["light"])))
    o.append('<circle cx="%.4f" cy="-0.582" r="0.026" fill="%s" stroke="%s" stroke-width="0.010"/>' % (dx - 0.04 * yaw, k.c(col["dark"]), k.ink))
    o.append('<path d="M%.4f,-0.50 Q%.4f,-0.56 %.4f,-0.575" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.30"/>' % (-0.36 + dx, -0.30 + dx, -0.16 + dx))
    o.append('</g>')
    CE._ext(k, C, ((-0.52 + dx, -0.26), (0.52 + dx, -0.26), (dx, -0.60), (vx - 0.36, -0.20), (vx + 0.36, -0.20)))
    return "".join(o), (dx, -0.60)


def _hat_slouch12(k, C, yaw):
    """a battered slouch hat: a tall soft dented crown, a wide brim sagging in the rain, a frayed band."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.14 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "sl", col, x0=-0.7, x1=0.7, mid=0.34)
    crown = ("M%.4f,-0.34 C%.4f,-0.52 %.4f,-0.72 %.4f,-0.80 Q%.4f,-0.88 %.4f,-0.76 Q%.4f,-0.88 %.4f,-0.80 C%.4f,-0.72 %.4f,-0.52 %.4f,-0.34 Z"
             % (-0.42 + dx, -0.44 + dx, -0.40 + dx, -0.28 + dx, -0.12 + dx + fx * 0.3, dx + fx * 0.5, 0.12 + dx + fx * 0.3, 0.28 + dx, 0.40 + dx, 0.44 + dx, 0.42 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,-0.78 Q%.4f,-0.66 %.4f,-0.58" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.75"/>' % (dx + fx * 0.5, dx + fx * 0.5 + 0.02, dx + fx * 0.4, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.66 Q%.4f,-0.72 %.4f,-0.77" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.6"/>' % (-0.32 + dx, -0.30 + dx, -0.14 + dx, k.c(col["light"])))
    o.append('<path d="M%.4f,-0.36 Q%.4f,-0.33 %.4f,-0.36 L%.4f,-0.46 Q%.4f,-0.43 %.4f,-0.46 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (-0.43 + dx, dx, 0.43 + dx, 0.44 + dx, dx, -0.44 + dx, k.c(col["band"]), k.ink))
    bp = [(-0.74 + dx, -0.30), (-0.45 + dx, -0.40), (dx, -0.43), (0.45 + dx, -0.40), (0.74 + dx, -0.30), (0.80 + dx, -0.12), (0.62 + dx, -0.17), (0.30 + dx, -0.24),
          (fx, -0.27), (-0.30 + dx, -0.24), (-0.62 + dx, -0.17), (-0.80 + dx, -0.12)]
    brim = P._smooth_closed(bp)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, k.c(col["brim"]), k.ink))
    o.append('<path d="M%.4f,-0.30 Q%.4f,-0.34 %.4f,-0.30" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (-0.30 + dx, fx, 0.30 + dx, k.c(col["light"])))
    o.append('</g>')
    CE._ext(k, C, ((-0.78 + dx, -0.14), (0.78 + dx, -0.14), (dx, -0.84), (fx, -0.24)))
    return "".join(o), (dx + fx * 0.5, -0.83)


def _hat_bonnet12(k, C, yaw):
    """a woman's bonnet: a rounded crown with a frilled brim framing the face, ribbons tied in a bow under the chin."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "bn", col, x0=-0.62, x1=0.62, mid=0.34)
    far = _clamp(yaw, -1, 1)
    # ribbons first (under the bow)
    rb = col.get("ribbon", "#d8506a")
    o.append('<path d="M%.4f,0.04 Q%.4f,0.32 %.4f,0.50 M%.4f,0.04 Q%.4f,0.32 %.4f,0.50" fill="none" stroke="%s" stroke-width="0.052" stroke-linecap="round"/>' % (-0.47 + dx, -0.46 + dx, -0.10 + dx * 0.5, 0.47 + dx, 0.46 + dx, 0.10 + dx * 0.5, k.ink))
    o.append('<path d="M%.4f,0.04 Q%.4f,0.32 %.4f,0.50 M%.4f,0.04 Q%.4f,0.32 %.4f,0.50" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (-0.47 + dx, -0.46 + dx, -0.10 + dx * 0.5, 0.47 + dx, 0.46 + dx, 0.10 + dx * 0.5, k.c(rb)))
    # bow under the chin
    bx = dx * 0.5
    o.append('<path d="M%.4f,0.535 Q%.4f,0.45 %.4f,0.50 Q%.4f,0.60 %.4f,0.535 Z M%.4f,0.535 Q%.4f,0.45 %.4f,0.50 Q%.4f,0.60 %.4f,0.535 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (bx, bx - 0.12, bx - 0.15, bx - 0.12, bx, bx, bx + 0.12, bx + 0.15, bx + 0.12, bx, k.c(rb), k.ink))
    o.append('<path d="M%.4f,0.53 l-0.03,0.14 M%.4f,0.53 l0.04,0.13" stroke="%s" stroke-width="0.034" stroke-linecap="round"/><path d="M%.4f,0.53 l-0.03,0.14 M%.4f,0.53 l0.04,0.13" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
             % (bx, bx, k.ink, bx, bx, k.c(rb)))
    o.append('<circle cx="%.4f" cy="0.535" r="0.030" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx, k.c(rb), k.ink))
    # crown / brim (the face opening is left clear)
    body = ("M%.4f,0.14 C%.4f,-0.10 %.4f,-0.52 %.4f,-0.62 C%.4f,-0.69 %.4f,-0.69 %.4f,-0.62 C%.4f,-0.52 %.4f,-0.10 %.4f,0.14 "
            "L%.4f,0.06 C%.4f,-0.12 %.4f,-0.28 %.4f,-0.31 Q%.4f,-0.35 %.4f,-0.31 C%.4f,-0.28 %.4f,-0.12 %.4f,0.06 Z"
            % (-0.60 + dx, -0.70 + dx, -0.66 + dx, -0.30 + dx, -0.10 + dx, 0.10 + dx, 0.30 + dx, 0.66 + dx, 0.70 + dx, 0.60 + dx,
               0.49 + dx, 0.50 + dx, 0.34 + dx, 0.18 + dx, dx, -0.18 + dx, -0.34 + dx, -0.50 + dx, -0.49 + dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (body, g, k.ink))
    # frill along the inner edge
    fr = []
    for i in range(13):
        t = i / 12.0
        a = math.pi * (1.0 - t)
        x = dx + 0.485 * math.cos(a) * (1.0 if abs(math.cos(a)) > 0.55 else 0.9)
        y = 0.06 - 0.37 * math.sin(a) ** 0.8 - 0.0
        fr.append((x, y))
    for i in range(len(fr) - 1):
        xa, ya = fr[i]
        xb, yb = fr[i + 1]
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        nx, ny = (yb - ya), -(xb - xa)
        ln = math.hypot(nx, ny) or 1.0
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (xa, ya, mx - nx / ln * 0.09 * (1 if i < 6 else 1), my - ny / ln * 0.09, xb, yb, k.c(col.get("frill", "#fffaf0")), k.ink))
    # crown ribbon band
    o.append('<path d="M%.4f,-0.46 Q%.4f,-0.40 %.4f,-0.46" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M%.4f,-0.46 Q%.4f,-0.40 %.4f,-0.46" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
             % (-0.50 + dx, dx, 0.50 + dx, k.ink, -0.50 + dx, dx, 0.50 + dx, k.c(rb)))
    o.append('<path d="M%.4f,-0.55 Q%.4f,-0.64 %.4f,-0.66" fill="none" stroke="#ffffff" stroke-width="0.018" stroke-linecap="round" opacity="0.4"/>' % (-0.30 + dx, -0.26 + dx, -0.10 + dx))
    o.append('</g>')
    CE._ext(k, C, ((-0.72 + dx, -0.30), (0.72 + dx, -0.30), (dx, -0.70), (bx - 0.15, 0.70), (bx + 0.15, 0.70)))
    return "".join(o), (dx, -0.69)


HATS12 = {"tricorn12": _hat_tricorn12, "roundfelt12": _hat_roundfelt12, "flatcap12": _hat_flatcap12, "slouch12": _hat_slouch12,
          "bonnet12": _hat_bonnet12}


# ============================================================================= costumes (torso-local)
def _button(k, c, r=0.032, col="#e2b442"):
    return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.010"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="0.7"/>'
            % (c[0], c[1], r, k.c(col), k.ink, c[0] - r * 0.30, c[1] - r * 0.30, r * 0.28))


def _cos_frockcoat12(k, C, m):
    """a gentleman's frock coat: the coat open over a buff waistcoat with small buttons, turned-back lapels, a white stock and a lace
    jabot at the neck, brass buttons down both coat edges, flapped hip pockets; the full skirt to the knee with folds and a back vent."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    sc = min(1.0, hw / 0.70)
    o = []
    # waistcoat (centre panel)
    wv = 0.20 * max(0.8, sc)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (X(-0.15, 0.40) + X(0.15, 0.40) + X(wv + 0.04, yB + 0.02) + X(-wv - 0.04, yB + 0.02) + (k.c(col["vest"]), k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(0.0, 0.62) + X(0.0, yB + 0.02) + (k.c(col["vest_d"]),)))
    for y in (0.78, 0.92, 1.06, 1.20):
        if y < yB - 0.10:
            o.append(_button(k, X(0.0, y), 0.020, col.get("vest_btn", "#bda070")))
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(s * 0.10, yB - 0.20) + X(s * 0.20, yB - 0.20) + (k.c(col["vest_d"]),)))
    # coat fronts: from the lapel down, edges swinging out towards the hips
    for s in (-1, 1):
        edge = [X(s * 0.15, 0.50), X(s * 0.17, 0.72), X(s * 0.21 * sc + s * 0.02, 1.00), X(s * 0.24 * sc + s * 0.02, yB + 0.02)]
        outer = [X(s * 0.15, 0.40), X(s * 0.60 * sc, 0.40), X(s * 0.60 * sc, yB + 0.05), X(s * 0.24 * sc + s * 0.02, yB + 0.05)]
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (edge[0] + edge[1] + edge[2] + edge[2] + edge[3] + outer[2] + outer[0] + (k.c(col["base"]), k.ink)))
    # lapels
    for s in (-1, 1):
        lp = [X(s * 0.12, 0.38), X(s * 0.31 * sc + s * 0.02, 0.42), X(s * 0.30 * sc + s * 0.02, 0.62), X(s * 0.16, 0.80), X(s * 0.15, 0.58)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(lp), k.c(col["lapel"]), k.ink))
    # stock and jabot
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (X(-0.17, 0.36) + X(0.0, 0.34) + X(0.17, 0.36) + X(0.15, 0.50) + X(0.0, 0.54) + X(-0.15, 0.50) + (k.c(col["stock"]), k.ink)))
    jb = [X(-0.09, 0.50), X(0.09, 0.50), X(0.075, 0.64), X(0.045, 0.70), X(0.0, 0.66), X(-0.045, 0.72), X(-0.075, 0.65)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_poly_d(jb), k.c(col["stock"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (X(-0.03, 0.55) + X(-0.035, 0.68) + X(0.03, 0.55) + X(0.035, 0.68) + (k.c("#b8b4c0"),)))
    # brass buttons down both edges
    for s in (-1, 1):
        for i, y in enumerate((0.84, 0.98, 1.12, 1.26)):
            if y < yB - 0.04:
                xs = 0.20 + 0.012 * i
                o.append(_button(k, X(s * xs * sc + s * 0.01, y), 0.030, col["button"]))
    # hip pocket flaps
    for s in (-1, 1):
        px = s * 0.34 * sc
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(px - 0.10, yB - 0.22) + X(px + 0.10, yB - 0.18) + X(px + 0.10, yB - 0.10) + X(px - 0.10, yB - 0.14) + (k.c(col["dark"]), k.ink)))
    inside = "".join(o)
    yt = yB - 0.12
    a = hw * 0.985
    hem = yB + C.get("coat_len", 0.62)
    b = hw + C.get("coat_flare", 0.14)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "fk", X, yt, a, hem, b, g, sw=0.026, folds=((-0.12, yt + 0.18, -0.20, hem - 0.04), (0.16, yt + 0.18, 0.24, hem - 0.04), (0.38 * sc, yt + 0.16, 0.50 * sc, hem - 0.05)),
                    fold_col=k.c(col["dark"]))]
    # the open front of the coat shows the breeches' waistband: a narrow V
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
              % (X(-0.05, yt + 0.02) + X(0.05, yt + 0.02) + X(0.10, hem - 0.20) + X(-0.10, hem - 0.20) + (k.c(col["vest"]), k.ink)))
    return inside, "", "".join(ov)


def _cos_greatcoat12(k, C, m):
    """the coachman's greatcoat: a drab body with two rows of big horn buttons, a skirt to the shins, and several layered capes over the
    shoulders (each longer and wider than the last, scalloped hems), a wool scarf wound round the neck with a tail in front."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    sc = min(1.0, hw / 0.70)
    o = []
    # two rows of big horn buttons and the front opening
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016"/>' % (X(0.03, 0.62) + X(0.05, yB + 0.05) + (k.ink,)))
    for i, y in enumerate((0.96, 1.10, 1.24, 1.38)):
        if y < yB - 0.05:
            for s in (-1, 1):
                c = X(s * 0.20 * sc + 0.04, y)
                o.append('<circle cx="%.4f" cy="%.4f" r="0.046" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="%.4f" cy="%.4f" r="0.014" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.010" fill="#ffffff" opacity="0.6"/>'
                         % (c[0], c[1], k.c(col["button"]), k.ink, c[0], c[1], k.c(col["dark"]), c[0] - 0.014, c[1] - 0.014))
    # a patch pocket flap each side
    for s in (-1, 1):
        px = s * 0.38 * sc
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                 % (X(px - 0.15, yB - 0.25) + X(px + 0.15, yB - 0.25) + X(px + 0.14, yB - 0.12) + X(px - 0.14, yB - 0.12) + (k.c(col["dark"]), k.ink)))
    inside = "".join(o)
    yt = yB - 0.12
    a = hw * 0.985
    hem = yB + C.get("coat_len", 0.70)
    b = hw + C.get("coat_flare", 0.16)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "gc", X, yt, a, hem, b, g, sw=0.028, folds=((-0.14, yt + 0.18, -0.22, hem - 0.04), (0.14, yt + 0.18, 0.22, hem - 0.04), (0.40 * sc, yt + 0.16, 0.52 * sc, hem - 0.05),
                                                                  (-0.40 * sc, yt + 0.16, -0.52 * sc, hem - 0.05)), fold_col=k.c(col["dark"]))]
    # capes, longest first
    nc = int(C.get("capes", 3))
    for i in range(nc - 1, -1, -1):
        yh = 0.58 + 0.20 * i
        wt = hw * 0.80
        wb = hw * (1.02 + 0.06 * i) + 0.10
        cg = col["cape"][i % len(col["cape"])]
        pts = [X(-wt, 0.40), X(wt, 0.40), X(wb * 0.98, yh - 0.10), X(wb, yh)]
        # scalloped hem right -> left
        hm = []
        n = 5
        for j in range(n + 1):
            x = wb - 2 * wb * j / n
            hm.append(X(x, yh + 0.035 * (1 - (2.0 * j / n - 1.0) ** 2) - (0.0 if j % 2 else 0.0)))
        d = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (pts[0] + pts[1] + pts[2] + pts[3])
        for j in range(1, n + 1):
            xa, ya = hm[j - 1]
            xb_, yb_ = hm[j]
            d += " Q%.4f,%.4f %.4f,%.4f" % ((xa + xb_) / 2, max(ya, yb_) + 0.050, xb_, yb_)
        d += " Q%.4f,%.4f %.4f,%.4f Z" % (X(-wb * 0.98, yh - 0.10) + X(-wt, 0.40))
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, k.c(cg), k.ink))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                  % (X(-wt * 0.9, yh - 0.12) + X(0.0, yh - 0.04) + X(wt * 0.9, yh - 0.12) + (k.c(col["dark"]),)))
        for q in (-0.5, 0.5):
            for r_, y_ in ((q, yh - 0.20),):
                c = X(r_ * wb, y_)
                ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.5"/>' % (c[0], c[1], c[0] + 0.02, c[1] + 0.13, k.c(col["dark"])))
    # the scarf
    sk = col["scarf"]
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
              % (X(-0.28 * sc - 0.06, 0.40) + X(0.0, 0.55) + X(0.28 * sc + 0.06, 0.40) + X(0.0, 0.34) + X(-0.28 * sc - 0.06, 0.40) + (k.c(sk), k.ink)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(-0.22, 0.44) + X(0.0, 0.52) + X(0.22, 0.44) + (k.c(col.get("scarf_d", sk)),)))
    tx = X(0.17, 0.52)
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
              % (tx[0] - 0.05, tx[1] - 0.02, tx[0] + 0.07, tx[1] - 0.02, tx[0] + 0.10, tx[1] + 0.38, tx[0] - 0.03, tx[1] + 0.40, k.c(sk), k.ink))
    for dy, cc in ((0.12, col.get("scarf_d", sk)), (0.24, col.get("scarf_d", sk))):
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020"/>' % (tx[0] - 0.04 + dy * 0.1, tx[1] + dy, tx[0] + 0.08 + dy * 0.1, tx[1] + dy, k.c(cc)))
    for i in range(5):
        ov.append('<path d="M%.4f,%.4f l0.004,0.05" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (tx[0] - 0.025 + 0.026 * i, tx[1] + 0.40, k.c(sk)))
    return inside, "", "".join(ov)


def _cos_dress12(k, C, m):
    """a woman's gown: a laced bodice under a white fichu crossed on the chest, a shawl over the shoulders, an apron over a long skirt."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    sc = min(1.0, hw / 0.70)
    o = []
    # lacing
    for y in (0.78, 0.90, 1.02, 1.14):
        if y < yB - 0.06:
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (X(-0.07, y) + X(0.07, y + 0.07) + X(0.07, y) + X(-0.07, y + 0.07) + (k.c(col["lace"]),)))
    # apron bib
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (X(-0.17, yB - 0.38) + X(0.17, yB - 0.38) + X(0.24, yB + 0.05) + X(-0.24, yB + 0.05) + (k.c(col["apron"]), k.ink)))
    # fichu: a white triangle crossed on the chest
    fi = [X(-0.30 * sc - 0.04, 0.38), X(0.30 * sc + 0.04, 0.38), X(0.10, 0.62), X(0.0, 0.80), X(-0.10, 0.62)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_poly_d(fi), k.c(col["fichu"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (X(-0.20, 0.44) + X(0.06, 0.74) + X(0.20, 0.44) + X(-0.06, 0.74) + (k.c("#c8c4d0"),)))
    inside = "".join(o)
    yt = yB - 0.10
    a = hw * 0.985
    hem = yB + C.get("coat_len", 0.88)
    b = hw + C.get("coat_flare", 0.40)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "dr", X, yt, a, hem, b, g, sw=0.026, folds=((-0.20, yt + 0.20, -0.36, hem - 0.05), (0.22, yt + 0.20, 0.38, hem - 0.05), (-0.50 * sc, yt + 0.18, -0.70 * sc, hem - 0.05),
                                                                 (0.52 * sc, yt + 0.18, 0.72 * sc, hem - 0.05)), fold_col=k.c(col["dark"]))]
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round" opacity="0.9"/>'
              % (X(-b * 0.95, hem - 0.07) + X(0.0, hem - 0.03) + X(b * 0.95, hem - 0.07) + (k.c(col["trim"]),)))
    # apron over the skirt
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
              % (X(-0.24, yB + 0.04) + X(0.24, yB + 0.04) + X(0.36, hem - 0.14) + X(0.0, hem - 0.08) + X(-0.36, hem - 0.14) + (k.c(col["apron"]), k.ink)))
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (X(-0.10, yB + 0.12) + X(-0.14, hem - 0.14) + (k.c("#b8b4c0"),)))
    # shawl: two panels from the shoulders to a point low on the chest, fringed
    for s in (-1, 1):
        sw_ = [X(s * 0.10, 0.37), X(s * (hw * 0.98), 0.40), X(s * hw * 0.86, 0.70), X(s * 0.30 * sc, 0.98), X(s * 0.02, 1.16), X(s * 0.10, 0.80), X(s * 0.12, 0.50)]
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(sw_), k.c(col["shawl"]), k.ink))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(s * 0.16, 0.50) + X(s * 0.30, 0.80) + X(s * 0.06, 1.08) + (k.c(col["shawl_d"]),)))
        for j in range(6):
            t = j / 5.0
            x_, y_ = X(s * (0.04 + 0.26 * t * sc), 1.14 - 0.17 * t)
            ov.append('<path d="M%.4f,%.4f l%.4f,0.055" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (x_, y_, s * 0.012, k.c(col["shawl_d"])))
    return inside, "", "".join(ov)


COSTUMES12 = {"frockcoat12": _cos_frockcoat12, "greatcoat12": _cos_greatcoat12, "dress12": _cos_dress12}


# ============================================================================= face: mutton chops, noses
def _chops(k, L, C, yaw):
    """mutton chops: a whisker mass from the temple down the cheek, widening to the jaw, kept inside the head disc."""
    ch = C["chops12"]
    col = ch["color"]
    cx = (L["xL"] + L["xR"]) / 2
    o = []

    def hw(y):
        return math.sqrt(max(0.0, 0.47 * 0.47 - (y + 0.02) * (y + 0.02)))
    for sd in (-1, 1):
        s = L["sR"] if sd > 0 else L["sL"]
        yt = L["ey"] - 0.01
        ym = min(L["my"] + 0.05, 0.33)
        ys = [yt, L["ey"] + 0.06, L["my"] - 0.06, ym]
        outer = [(cx * 0.5 + sd * (hw(y) - 0.02) * (0.55 + 0.45 * s), y) for y in ys]
        inner = [(cx + sd * w * s, y) for (w, y) in ((0.37, ys[0]), (0.34, ys[1]), (0.29, ys[2]), (0.24, ys[3]))]
        pts = outer + [(outer[-1][0] + (inner[-1][0] - outer[-1][0]) * 0.5, ym + 0.035)] + inner[::-1]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink))
        st = []
        for j in range(5):
            y = yt + 0.05 + j * (ym - yt - 0.08) / 4.0
            xo = outer[min(3, j)][0]
            st.append("M%.4f,%.4f l%.4f,0.04" % (xo - sd * 0.02, y, -sd * 0.05))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % ("".join(st), k.c(ch.get("light", col))))
    return "".join(o)


def _nose(k, L, C, yaw):
    nz = C["nose12"]
    cx = (L["xL"] + L["xR"]) / 2
    ey, my = L["ey"], L["my"]
    kind = nz.get("kind", "bulb")
    col = nz.get("color", "#e0675a")
    if kind == "long":
        tipx = cx + 0.03 + 0.11 * yaw
        sd = 1.0 if yaw >= -0.1 else -1.0
        d = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
             % (cx - 0.035, ey + 0.02, cx - 0.06 + 0.04 * yaw, ey + 0.16, tipx - 0.01, ey + 0.27, tipx + sd * 0.06, ey + 0.26, tipx + 0.05, ey + 0.20, cx + 0.04, ey + 0.06, cx + 0.035, ey + 0.01))
        return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/><path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>'
                % (d, k.c(col), k.ink, cx - 0.015, ey + 0.08, cx - 0.03 + 0.03 * yaw, ey + 0.15, tipx - 0.02, ey + 0.22))
    nx = cx + 0.015 + 0.05 * yaw
    ny = ey + 0.115
    r = nz.get("r", 0.085)
    return ('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.018"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#ffffff" opacity="0.55"/><circle cx="%.4f" cy="%.4f" r="0.008" fill="%s" opacity="0.6"/><circle cx="%.4f" cy="%.4f" r="0.008" fill="%s" opacity="0.6"/>'
            % (nx, ny, r * 1.05, r, k.c(col), k.ink, nx - r * 0.35, ny - r * 0.35, r * 0.24, r * 0.15, nx + 0.03, ny + 0.02, k.ink, nx - 0.02, ny + 0.03, k.ink))


def _face(k, C, P_, white):
    svg, L = _O12["_face"](k, C, P_, white)
    if C is None or not C.get("_cast12"):
        return svg, L
    yaw = P_["yaw"]
    if C.get("nose12"):
        svg = svg + _nose(k, L, C, yaw)
    if C.get("chops12"):
        svg = svg + _chops(k, L, C, yaw)
    return svg, L


# ============================================================================= limbs: stockings and shoes
def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O12["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast12") or tail is None or not C.get("stocking12"):
        return out
    st = C["stocking12"]
    pts = C3._limb_pts(S, E, H, 0.55)
    cum = [0.0]
    for i in range(1, len(pts)):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1] or 1.0
    f0 = (C.get("shorts") or {}).get("len", 0.5) - 0.02
    hb = (C.get("boots") or {}).get("h", 0.06)
    sel = [p for p, c in zip(pts, cum) if c >= f0 * tot and p[1] < H[1] - hb + 0.01]
    if len(sel) < 2:
        return out
    d = "M" + " L".join("%.4f,%.4f" % p for p in sel)
    sw = w * 1.55 + 0.012
    out += '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.ink, sw + 0.030)
    out += '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" stroke-linejoin="round"/>' % (d, k.c(st["color"]), sw)
    out += '<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7" transform="translate(%.4f 0)"/>' % (d, k.c(st.get("shade", "#b8b4c0")), sw * 0.28)
    # the garter / knee band under the breeches, and the shoe buckle
    sx = 1.0 if (tail[0] - H[0]) >= 0 else -1.0
    out += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (sel[0][0] - sw / 2, sel[0][1], sel[0][0] + sw / 2, sel[0][1], k.c(st.get("garter", "#3a3640")))
    if st.get("buckle"):
        bx, by = H[0] + sx * 0.045, H[1] - 0.015
        out += ('<rect x="%.4f" y="%.4f" width="0.050" height="0.056" rx="0.008" fill="none" stroke="%s" stroke-width="0.022"/><rect x="%.4f" y="%.4f" width="0.050" height="0.056" rx="0.008" fill="none" stroke="%s" stroke-width="0.012"/>'
                % (bx - 0.025, by - 0.028, k.ink, bx - 0.025, by - 0.028, k.c("#e8e4f0")))
    return out


# ============================================================================= props held in the hand
NEW_PROPS12 = ("umbrella_black", "umbrella_black_closed", "umbrella_pink", "umbrella_pink_closed", "umbrella_small", "whip", "cabbage12", "egg",
               "purse", "coins", "tricorn_held", "wig")
NEW_TIP12 = {"umbrella_black": -UMB_TOP, "umbrella_black_closed": -UMB_TOP, "umbrella_pink": -UMB_TOP, "umbrella_pink_closed": -UMB_TOP,
             "umbrella_small": -UMB_TOP, "whip": WHIP_STOCK, "cabbage12": 0.15, "egg": 0.07, "purse": 0.37, "coins": 0.10, "tricorn_held": 0.10, "wig": 0.0}
HAT_COL_DEFAULT = dict(base="#2a2830", light="#55515f", dark="#14121a", bind="#c8c4d4", btn="#d8d4e0")


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS12:
        return _O12["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    if kind in UMB_KINDS:
        name, oo, frill = UMB_KINDS[kind]
        if name is None:
            name = _POSE12["ucol"] or "maroon"
        pal = UMB[name]
        op = _POSE12["umb"] if oo is None else oo
        egg = _POSE12["egg"] if name == "black" else 0.0
        leaf = _POSE12["leaf"] if name == "black" else 0.0
        body, (R, top, rim) = _umb_body(k, key, op, pal, frill, egg, leaf)
        rot = ang + 90.0
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], rot, sc, body)
        pts = {"top": (0.0, top), "mid": (0.0, (top + rim) / 2), "edge1": (-R, rim), "edge2": (R, rim), "handle": (-0.12, UMB_HANDLE)}
        wp = {}
        for n, (x, y) in pts.items():
            q = _rot(x * sc, y * sc, rot)
            wp[n] = (H[0] + q[0], H[1] + q[1])
            an["umb_%s_%s" % (n, key)] = wp[n]
        pad = 0.04 + (0.12 if frill else 0.0)
        for n in ("top", "edge1", "edge2", "handle"):
            k.ext.append((wp[n][0], wp[n][1], pad if n.startswith("edge") else 0.05))
        k.ext.append((wp["mid"][0], wp["mid"][1], 0.05))
        return o, wp["top"]
    if kind == "whip":
        rot = ang
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], rot, sc, _whip_stock(k))
        tx, ty = _rot(WHIP_STOCK * sc, -0.012 * sc, rot)
        T = (H[0] + tx, H[1] + ty)
        u = (math.cos(math.radians(rot)) * sc, math.sin(math.radians(rot)) * sc)
        ls, e = _whip_lash(k, T, u, _POSE12["whip_t"])
        k.ext.extend(((T[0], T[1], 0.05), (e[0], e[1], 0.10), ((T[0] + e[0]) / 2 + 0.2 * u[0], (T[1] + e[1]) / 2, 0.30), (H[0] - 0.2 * u[0], H[1] - 0.2 * u[1], 0.05)))
        an["whip_tip_" + key] = e
        an["whip_stock_" + key] = T
        return o + ls, T
    if kind == "cabbage12":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _cabbage_body(k, 0.0, -0.15, 0.19, 0.0, "cb" + key))
        k.ext.extend(((H[0], H[1] - 0.34 * sc, 0.03), (H[0] - 0.20 * sc, H[1] - 0.15 * sc, 0.03), (H[0] + 0.20 * sc, H[1] - 0.15 * sc, 0.03)))
        an["cabbage_" + key] = (H[0], H[1] - 0.15 * sc)
        return o, (H[0], H[1] - 0.15 * sc)
    if kind == "egg":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _egg_body(k, 0.0, -0.07, 1.0, 0.0, "eg" + key))
        k.ext.extend(((H[0], H[1] - 0.20 * sc, 0.03), (H[0] - 0.08 * sc, H[1], 0.03), (H[0] + 0.08 * sc, H[1], 0.03)))
        an["egg_" + key] = (H[0], H[1] - 0.07 * sc)
        return o, (H[0], H[1] - 0.07 * sc)
    if kind == "purse":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _purse_body(k, _POSE12["purse"]))
        for (x, y) in ((-0.19, 0.2), (0.19, 0.2), (0.0, 0.38), (0.0, -0.06)):
            k.ext.append((H[0] + x * sc, H[1] + y * sc, 0.03))
        an["purse_bottom_" + key] = (H[0], H[1] + 0.37 * sc)
        return o, (H[0], H[1] + 0.37 * sc)
    if kind == "coins":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _coins_body(k))
        k.ext.extend(((H[0] - 0.12 * sc, H[1] - 0.05 * sc, 0.03), (H[0] + 0.12 * sc, H[1] - 0.05 * sc, 0.03), (H[0], H[1] - 0.18 * sc, 0.03)))
        an["coins_" + key] = (H[0], H[1] - 0.10 * sc)
        return o, (H[0], H[1] - 0.10 * sc)
    if kind == "tricorn_held":
        C = CE._CUR[0] or {}
        col = C.get("hat_colors") if isinstance(C.get("hat_colors"), dict) and "light" in C.get("hat_colors", {}) else HAT_COL_DEFAULT
        body = _tricorn_body(k, col, 0.0, 0.0, "th" + key)
        o = '<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f)">%s</g>' % (H[0] - side * 0.36 * sc, H[1] + 0.32 * sc, side * -6.0, sc, body)
        for (x, y) in ((-0.76, -0.55), (0.76, -0.55), (0.0, -0.72), (0.0, -0.25)):
            q = _rot(x * sc, y * sc, side * -6.0)
            k.ext.append((H[0] - side * 0.36 * sc + q[0], H[1] + 0.32 * sc + q[1], 0.03))
        an["hat_held_" + key] = (H[0] - side * 0.36 * sc, H[1] + 0.32 * sc - 0.45 * sc)
        return o, (H[0], H[1])
    # wig
    o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1] - 0.04 * sc, sc, _wig_body(k, _POSE12["soaked"]))
    for (x, y) in ((-0.30, -0.22), (0.30, -0.22), (0.0, 0.40)):
        k.ext.append((H[0] + x * sc, H[1] + y * sc, 0.03))
    return o, (H[0], H[1])


# ============================================================================= figure overlays: mud, wet drips, coach-box seat
def _mud_overlay(k, an, lev, t):
    o = []
    seed = 7.7
    el, er, mo, ht = an["eye_l"], an["eye_r"], an["mouth"], an["hat_top"]
    ch, hp = an["chest"], an["hip"]
    spots = [  # (x, y, r, drip length)
        (el[0] - 0.05, el[1] + 0.12, 0.060, 0.0), (er[0] + 0.07, er[1] + 0.10, 0.050, 0.10), (ht[0] - 0.10, ht[1] + 0.10, 0.075, 0.0),
        (mo[0] + 0.03, mo[1] - 0.12, 0.040, 0.0), (ch[0] - 0.18, ch[1] + 0.12, 0.095, 0.16), (ch[0] + 0.20, ch[1] + 0.34, 0.085, 0.12),
        (hp[0] - 0.30, hp[1] - 0.10, 0.100, 0.18), (hp[0] + 0.28, hp[1] + 0.05, 0.110, 0.14), (hp[0] - 0.05, hp[1] + 0.30, 0.100, 0.20),
        (hp[0] + 0.10, hp[1] + 0.52, 0.090, 0.12), (ht[0] + 0.30, ht[1] + 0.18, 0.050, 0.0), (an["shoulder_r"][0] + 0.05, an["shoulder_r"][1] + 0.1, 0.070, 0.12),
        (an["knee_l"][0] - 0.04, an["knee_l"][1] - 0.05, 0.090, 0.12), (an["knee_r"][0] + 0.05, an["knee_r"][1] + 0.05, 0.095, 0.10),
        (an["foot_l"][0] - 0.02, an["foot_l"][1] - 0.22, 0.100, 0.0), (an["foot_r"][0] + 0.02, an["foot_r"][1] - 0.30, 0.100, 0.0),
        (an["foot_l"][0] + 0.03, an["foot_l"][1] - 0.50, 0.080, 0.0), (an["foot_r"][0] - 0.02, an["foot_r"][1] - 0.55, 0.080, 0.0),
        (an["hand_l"][0] - 0.02, an["hand_l"][1] - 0.02, 0.050, 0.0), (an["hand_r"][0] + 0.02, an["hand_r"][1] - 0.04, 0.050, 0.0)]
    n = len(spots)
    for i, (x, y, r, dl) in enumerate(spots):
        thr = 0.04 + 0.90 * i / n
        if lev < thr:
            continue
        r = r * (0.6 + 0.6 * min(1.0, (lev - thr) / 0.2 + 0.0))
        o.append(_splat(k, x, y, r, MUD["base"], seed + 1.9 * i))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.7"/>'
                 % (x - r * 0.4, y - r * 0.4, x - r * 0.1, y - r * 0.6, x + r * 0.3, y - r * 0.55, k.c(MUD["light"]), r * 0.18))
        if dl > 0 and lev > 0.6:
            o.append(_drip(k, x + r * 0.2, y + r * 0.6, dl * lev, r * 0.28, MUD["base"]))
    return "".join(o)


def _wet_overlay(k, an, lev, t):
    o = []
    el, ht, hp = an["eye_l"], an["hat_top"], an["hip"]
    src = [(el[0] - 0.46, el[1] - 0.20), (an["eye_r"][0] + 0.46, an["eye_r"][1] - 0.20), (an["mouth"][0] + 0.02, an["mouth"][1] - 0.10),
           (hp[0] - 0.55, hp[1] + 0.70), (hp[0] + 0.55, hp[1] + 0.70), (an["hand_l"][0], an["hand_l"][1] + 0.08), (an["hand_r"][0], an["hand_r"][1] + 0.08)]
    for i, (x, y) in enumerate(src):
        if lev < 0.1 + 0.1 * i:
            continue
        for j in range(2):
            f = (t * 1.2 + 0.37 * i + 0.5 * j) % 1.0
            yy = y + 0.04 + 0.34 * f
            o.append('<path d="M%.4f,%.4f q-0.022,0.040 0,0.060 q0.022,-0.020 0,-0.060 Z" fill="%s" stroke="%s" stroke-width="0.007" opacity="%.3f"/>'
                     % (x + 0.01 * j, yy, k.c(WATER["base"]), k.c(WATER["dark"]), (1.0 - f * f) * 0.95))
    return "".join(o)


def _box_svg(k, cx, y, w, h):
    """a coach-box seat: a cushion under the figure's hips (top at y) with a hammercloth valance and gold fringe, on a dark panel h deep."""
    x0 = cx - w / 2
    o = []
    g = _lin(k, "bx", "#4a6a5c", "#2e4a40", "#1a2e28", x0, 0, x0 + w, 0)
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.03" fill="%s" stroke="%s" stroke-width="0.030"/>' % (x0, y + 0.13, w, h, g, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.02" fill="none" stroke="%s" stroke-width="0.020" opacity="0.9"/>' % (x0 + 0.10, y + 0.30, w - 0.20, h - 0.30, k.c("#e0b050")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" opacity="0.8"/>' % (x0 + 0.10, y + 0.30 + (h - 0.30) / 2, x0 + w - 0.10, y + 0.30 + (h - 0.30) / 2, k.c("#c04a3a")))
    vg = _lin(k, "bv", "#c04a58", "#8e2a36", "#5a1622", x0, 0, x0 + w, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
             % (x0 - 0.05, y, x0 + w + 0.05, y, x0 + w + 0.03, y + 0.20, x0 + w / 2, y + 0.26, x0 - 0.03, y + 0.20, x0 - 0.03, y + 0.20, vg, k.ink))
    for i in range(int(w / 0.07)):
        xx = x0 + 0.03 + i * 0.07
        o.append('<path d="M%.4f,%.4f l0.004,0.07" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (xx, y + 0.21, k.c("#e8c060")))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.3"/>' % (x0 + 0.1, y + 0.05, x0 + w / 2, y + 0.00, x0 + w - 0.2, y + 0.05))
    return "".join(o), (x0 - 0.06, y - 0.02, x0 + w + 0.06, y + 0.13 + h + 0.03)


BOX_W = 2.30


def figure(cast_name, pose=None, uid="p"):
    f = _O12["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    mud = _f(pose.get("mud"), 0.0, 0.0, 1.0)
    soak = _f(pose.get("soaked"), 0.0, 0.0, 1.0)
    box = _f(pose.get("coach_box"), 0.0, 0.0, 1.0)
    if mud < 0.02 and soak < 0.02 and box < 0.5:
        return f
    an = dict(f["anchors"])
    b = list(f["bbox"])
    k = P._Ctx(uid + "w", P.INK, None)
    t = _f(pose.get("t"), 0.0, -1e6, 1e6)
    pre, post = [], []
    if box >= 0.5:
        bw = _f(pose.get("box_w"), BOX_W, 1.2, 4.0)
        hp = an["hip"]
        top = hp[1] + 0.06
        s, bb = _box_svg(k, hp[0], top, bw, max(0.5, f["feet_y"] - top + 0.10))
        pre.append(s)
        b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
        an["box_top"] = (hp[0], top)
    if mud >= 0.02:
        post.append(_mud_overlay(k, an, mud, t))
    if soak >= 0.02:
        post.append(_wet_overlay(k, an, soak, t))
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg=defs + "".join(pre) + f["svg"] + "".join(post), bbox=tuple(b), anchors=an)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE12["umb"] = _f(g("umb_open"), 1.0, 0.0, 1.0)
    uc = g("umb_col")
    _POSE12["ucol"] = uc if isinstance(uc, str) and uc in UMB else None
    _POSE12["egg"] = _f(g("egg_splat"), 0.0, 0.0, 1.0)
    _POSE12["leaf"] = _f(g("leaf_stick"), 0.0, 0.0, 1.0)
    _POSE12["mud"] = _f(g("mud"), 0.0, 0.0, 1.0)
    _POSE12["soaked"] = _f(g("soaked"), 0.0, 0.0, 1.0)
    _POSE12["hat_off"] = _f(g("hat_off"), 0.0, 0.0, 1.0)
    _POSE12["wig_off"] = _f(g("wig_off"), 0.0, 0.0, 1.0)
    _POSE12["box"] = _f(g("coach_box"), 0.0, 0.0, 1.0)
    _POSE12["whip_t"] = _f(g("whip_t"), 0.0, -1e6, 1e6)
    _POSE12["purse"] = _f(g("purse_open"), 0.5, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE12["t"] = t if math.isfinite(t) else 0.0
    if isinstance(pose, dict) and _POSE12["soaked"] > 0.02 and pose.get("tint") is None:
        s = _POSE12["soaked"]
        pose = dict(pose, tint=(255 - 22 * s, 255 - 17 * s, 255 - 5 * s))
    return _O12["_norm"](C, pose)


# ============================================================================= standalone pieces
def umbrella_svg(uid="um", kind="black", open_=1.0, egg=0.0, leaf=0.0, ink=P.INK, tint=None):
    """an umbrella alone (hand/grip at (0, 0), shaft along -y, apex at y -1.95): kind black / pink / maroon / green / navy / tan, open_ 0 furled .. 1 open.
    Pink has the lace frill.  egg 0..1 adds a smashed egg on the dome, leaf 1 a cabbage leaf."""
    k = _ctx(uid, ink, tint)
    kind = kind if kind in UMB else "black"
    body, _ = _umb_body(k, "s", _clamp(_num(open_, 1.0), 0.0, 1.0), UMB[kind], kind == "pink", _clamp(_num(egg, 0.0), 0.0, 1.0) if kind == "black" else 0.0,
                        leaf if kind == "black" else 0.0)
    return '<g id="%s_umb"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), body)


def cabbage_svg(uid="cb", rot=0.0, ink=P.INK, tint=None):
    """a cabbage 0.38 D across centred on (0, 0) (the thrown vegetable; rotate it yourself)."""
    k = _ctx(uid, ink, tint)
    s = _cabbage_body(k, 0.0, 0.0, 0.19, rot, "cs")
    return '<g id="%s_cab"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def egg_svg(uid="eg", rot=0.0, ink=P.INK, tint=None):
    """a hen's egg (0.18 x 0.23 D) centred on (0, 0)."""
    k = _ctx(uid, ink, tint)
    s = _egg_body(k, 0.0, 0.0, 1.0, rot, "es")
    return '<g id="%s_egg"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def egg_splat_svg(uid="es", r=0.22, ink=P.INK, tint=None):
    """a smashed egg splat (albumen, yolk, shell bits, runs) centred on (0, 0): for the set to stick on a surface."""
    k = _ctx(uid, ink, tint)
    s = _egg_on_canopy(k, 1.0, -0.2, 0.2, 0.4, 1.0)
    return '<g id="%s_splat" transform="translate(%.4f %.4f) scale(%.4f)"><defs>%s</defs>%s</g>' % (k.uid, -0.2 * r / 0.22, (0.4 * 0.70 - 0.2) * r / 0.22, r / 0.22, "".join(k.defs), s)


def purse_svg(uid="pu", open_=0.5, ink=P.INK, tint=None):
    """the coin purse hanging from its neck at (0, 0), bottom at y 0.37."""
    k = _ctx(uid, ink, tint)
    body = _purse_body(k, _clamp(_num(open_, 0.5), 0.0, 1.0))
    return '<g id="%s_purse"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), body)


def coin_svg(uid="co", r=0.05, tilt=0.0, ink=P.INK, tint=None):
    """one gold coin centred on (0, 0)."""
    k = _ctx(uid, ink, tint)
    return '<g id="%s_coin">%s</g>' % (k.uid, _coin(k, 0.0, 0.0, r, r * 0.55, tilt))


def whip_svg(uid="wh", t=0.0, ink=P.INK, tint=None):
    """the whip alone, stock along +x from the grip at (0, 0), lash hanging from x 1.05."""
    k = _ctx(uid, ink, tint)
    ls, e = _whip_lash(k, (WHIP_STOCK, -0.012), (1.0, 0.0), _num(t, 0.0))
    st = _whip_stock(k)
    return '<g id="%s_whip">%s%s</g>' % (k.uid, st, ls)


def coach_box_svg(uid="cx", w=BOX_W, h=0.9, ink=P.INK, tint=None):
    """the box seat alone: cushion top at y 0, centred on x 0, panel h deep.  Returns svg."""
    k = _ctx(uid, ink, tint)
    s, bb = _box_svg(k, 0.0, 0.0, w, h)
    return '<g id="%s_box"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast12=True)
_FLAGS.update(_cast10=True)
HAT_BLACK = dict(base="#2a2830", light="#55515f", dark="#14121a", bind="#c8c4d4", btn="#d8d4e0", wig="#f6f3f8", wig_d="#cdc7d8")


def _man(seed, build, tw, th, leg, coat, vest, hat, wig, hair, prof, eye=0.03, mouth="dash", cheeks="#eea898", tache=None, hat_tilt=-3.0, brow="stroke", stock="#f0ede6", hose=None, limb=0.058):
    d = dict(_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=prof, shift_pow=1.1, shoulder=(0.12 + tw * 0.20, 0.49), arm=0.74, hip_x=0.15 + 0.03 * max(0, tw - 0.8),
             leg=leg, stance=0.06, wide=0.28, limb_w=limb, eye_y=eye, brow=brow, brow_th=0.058, mouth=mouth, moustache=bool(tache), smirk_side=1, cheeks=cheeks,
             hat="newsboy", hat_style="tricorn12", hat_tilt=hat_tilt, ear_pencil=False, hat_colors=dict(hat), wig=wig, hair=hair, costume="frockcoat12",
             coat_len=0.58, coat_flare=0.14,
             sleeve=dict(color=coat["base"], dark=coat["dark"], cuff=coat.get("cuff", "#efe8d8"), len=0.84, w=0.15 + 0.03 * max(0, tw - 0.8)),
             shorts=dict(color=coat["pants"], dark="#1e1a18", cuff=coat["pants"], len=0.50, w=0.15),
             boots=dict(color="#1e1a1c", cuff="#1e1a1c", h=0.05, toe=0.16),
             stocking12=dict(color=hose or "#e8e4de", shade="#b8b4ac", buckle=True),
             colors=dict(coat, vest=vest[0], vest_d=vest[1], vest_btn=vest[2], stock=stock, button=coat.get("button", "#e2b442")))
    if tache:
        d.update(moustache_style="bushy", tache_scale=tache[0])
        d["colors"]["moustache"] = tache[1]
    return d


def _woman(seed, build, tw, th, leg, gown, bonnet, hair, prof, shawl, mouth="smile"):
    return dict(_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=prof, shift_pow=1.1, shoulder=(0.12 + tw * 0.20, 0.47), arm=0.70, hip_x=0.15,
                leg=leg, stance=0.06, wide=0.26, limb_w=0.054, eye_y=0.030, brow="dome", brow_th=0.040, mouth=mouth, moustache=False, smirk_side=-1, cheeks="#f2a094", lashes=True,
                hat="newsboy", hat_style="bonnet12", hat_tilt=-2.0, ear_pencil=False, hat_colors=dict(bonnet), hair=dict(hair, front=0.0, grow=0.0), costume="dress12", coat_len=0.88, coat_flare=0.40,
                sleeve=dict(color=gown[0], dark=gown[1], cuff="#fbfaf6", len=0.80, w=0.140),
                boots=dict(color="#2e2420", cuff="#2e2420", h=0.05, toe=0.15),
                colors=dict(base=gown[0], dark=gown[1], apron="#f4eee0", fichu="#fbfaf6", lace="#e8d8b8", trim=gown[2], shawl=shawl[0], shawl_d=shawl[1]))


NEW_CAST12 = {
    # Jonas Hanway: lean gentleman, powdered short wig with a queue under a black tricorn, long dark-blue frock coat with brass buttons,
    # buff waistcoat, white stock and lace jabot, dark breeches, white stockings, buckled shoes; calm, a little smug
    "hanway": _man(121.3, "slim", 0.66, 1.04, 1.38, dict(base="#34509a", dark="#22366a", lapel="#4a6ab4", pants="#2c2a36", cuff="#f4f0e6", button="#e8c050"),
                   ("#ece0c0", "#b8a880", "#bda070"), HAT_BLACK, True, dict(color="#e8e4ee", front=0.0, grow=0.0), CE.PROFILE_ATHLETE, eye=0.030,
                   mouth="smirk", cheeks="#f0b0a4", stock="#fbfaf6", hose="#f6f4f8", limb=0.056),
    # the head coachman: stout, red nose and cheeks, grey mutton-chop whiskers, low round felt hat, many-caped drab-olive greatcoat, red wool
    # scarf, big boots (the whip is a prop)
    "coachman": dict(
        _FLAGS, build="stout", seed=88.6,
        torso_w=1.52, torso_h=1.22, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.10, stance=0.07, wide=0.32, limb_w=0.070,
        eye_y=0.000, brow="stroke", brow_th=0.085, mouth="smirk", moustache=True, moustache_style="bushy", tache_scale=0.95, smirk_side=1, cheeks="#e8604f", chins=True,
        hat="newsboy", hat_style="roundfelt12", hat_tilt=5.0, ear_pencil=False,
        hat_colors=dict(base="#6a5a3c", light="#8e7c58", dark="#3e3424", band="#241e18", brim="#54462e"),
        hair=dict(color="#a29484", front=0.12, grow=0.26),
        costume="greatcoat12", coat_len=0.72, coat_flare=0.16, capes=3,
        sleeve=dict(color="#76723e", dark="#46422a", cuff="#5a5634", len=0.86, w=0.21),
        shorts=dict(color="#4a3e30", dark="#2a2218", cuff="#4a3e30", len=0.90, w=0.18),
        boots=dict(color="#2a1e16", cuff="#5a4430", h=0.26, toe=0.20),
        chops12=dict(color="#aa9888", light="#d8ccbc"), nose12=dict(kind="bulb", color="#e0584c", r=0.095),
        colors=dict(base="#7c7848", dark="#4c4a2c", cape=["#8a8650", "#767240", "#66623a"], scarf="#b8453a", scarf_d="#8a2e28", button="#5a4a38",
                    moustache="#a29484", moustache_l="#d0c4b4"),
    ),
    # coachman_b: tall and thin, a long nose, a sagging brown slouch hat, a two-caped brown coat, a mustard scarf
    "coachman_b": dict(
        _FLAGS, build="slim", seed=61.2,
        torso_w=0.64, torso_h=1.12, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.78, hip_x=0.15, leg=1.50, stance=0.06, wide=0.26, limb_w=0.054,
        eye_y=0.030, brow="dome", brow_th=0.045, mouth="smirk", moustache=True, moustache_style="bushy", tache_scale=0.55, smirk_side=-1, cheeks="#e8907c",
        hat="newsboy", hat_style="slouch12", hat_tilt=-5.0, ear_pencil=False,
        hat_colors=dict(base="#5a4632", light="#7e664a", dark="#32261a", band="#2a2018", brim="#4a3826"),
        hair=dict(color="#4a3a2c", front=0.10, grow=0.22),
        costume="greatcoat12", coat_len=0.80, coat_flare=0.12, capes=2,
        sleeve=dict(color="#6e5a46", dark="#463a2c", cuff="#4a3c2e", len=0.86, w=0.15),
        shorts=dict(color="#3a3228", dark="#201a14", cuff="#3a3228", len=0.90, w=0.14),
        boots=dict(color="#2a1e16", cuff="#5a4430", h=0.26, toe=0.18),
        nose12=dict(kind="long", color="#f2c0b0"),
        colors=dict(base="#7a6650", dark="#4e4032", cape=["#86725a", "#725e48"], scarf="#d8a830", scarf_d="#a87c1c", button="#3a2e24", moustache="#4a3a2c"),
    ),
    # coachman_c: short and round, bald under a flat cloth cap, red cheeks, a short dull-green jacket with one cape, a blue scarf
    "coachman_c": dict(
        _FLAGS, build="stout", seed=29.4,
        torso_w=1.30, torso_h=0.96, profile=C2.PROFILE_ROUND, shift_pow=1.2,
        shoulder=(0.40, 0.44), arm=0.70, hip_x=0.18, leg=0.88, stance=0.07, wide=0.30, limb_w=0.066,
        eye_y=0.020, brow="stroke", brow_th=0.070, mouth="grin", moustache=False, smirk_side=1, cheeks="#ee6a58", chins=True,
        hat="newsboy", hat_style="flatcap12", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(base="#7a6c5c", light="#a09080", dark="#4c4034", visor="#3a3028"),
        hair=dict(color="#d8d0c0", front=0.0, grow=0.0),
        costume="greatcoat12", coat_len=0.50, coat_flare=0.14, capes=1,
        sleeve=dict(color="#5e7058", dark="#3a4a38", cuff="#4a5a46", len=0.86, w=0.19),
        shorts=dict(color="#4a4038", dark="#2a241e", cuff="#4a4038", len=0.90, w=0.17),
        boots=dict(color="#2a1e16", cuff="#5a4430", h=0.22, toe=0.18),
        nose12=dict(kind="bulb", color="#ea7a68", r=0.080),
        colors=dict(base="#667a60", dark="#3e4e3c", cape=["#748a6c"], scarf="#3a64a8", scarf_d="#264a82", button="#3e3226"),
    ),
    # crowd men (period coats, tricorns): a brown, powdered; b burgundy, ginger hair; c grey-green, round; d ochre, tall
    "crowd_man_a": _man(14.2, "regular", 0.88, 1.00, 1.20, dict(base="#8a5a3a", dark="#5a3a24", lapel="#a46e48", pants="#3a2e26"), ("#e0d2ae", "#a89868", "#9a8458"),
                        dict(HAT_BLACK, base="#3a3430", light="#645c54", dark="#1c1814"), True, dict(color="#e8e4ee", front=0.0, grow=0.0), CE.PROFILE_PEAR, mouth="smirk", hat_tilt=6.0),
    "crowd_man_b": _man(27.7, "slim", 0.72, 1.00, 1.30, dict(base="#8a3446", dark="#5c1e2c", lapel="#a84c60", pants="#3a2c2c"), ("#d8d0b8", "#a09878", "#8a8060"),
                        dict(HAT_BLACK, base="#2e2c34", light="#58566a", dark="#16141c"), False, dict(color="#c86a30", front=0.08, grow=0.10), CE.PROFILE_ATHLETE, eye=0.04,
                        mouth="dash", hat_tilt=-6.0, brow="dome"),
    "crowd_man_c": _man(53.1, "stout", 1.22, 1.00, 1.00, dict(base="#5e7462", dark="#3a4c40", lapel="#7a9080", pants="#40382e"), ("#e8dcc0", "#b0a47c", "#a08c60"),
                        dict(HAT_BLACK, base="#4a4440", light="#746c64", dark="#26221e"), True, dict(color="#d8d4dc", front=0.0, grow=0.0), C2.PROFILE_ROUND, mouth="frown",
                        cheeks="#f08a78", hat_tilt=3.0, tache=(0.8, "#8a8490"), limb=0.064),
    "crowd_man_d": _man(76.9, "slim", 0.78, 1.02, 1.32, dict(base="#b4822e", dark="#7a5618", lapel="#cc9a46", pants="#463a2c"), ("#f0e6cc", "#b8a878", "#a89460"),
                        dict(HAT_BLACK, base="#26242c", light="#4e4c5c", dark="#100e16"), False, dict(color="#5a3a26", front=0.08, grow=0.10), CE.PROFILE_ATHLETE, eye=0.02,
                        mouth="smirk", hat_tilt=-2.0, tache=(0.62, "#5a3a26")),
    # crowd women (bonnets, shawls; the small umbrella is a prop): a rose gown, ochre shawl; b teal gown, terracotta shawl
    "crowd_woman_a": _woman(35.5, "regular", 0.80, 1.00, 1.05, ("#c04858", "#842a38", "#ecc27a"), dict(base="#f2e6d0", light="#fffaf0", dark="#c8b898", ribbon="#2f8a8a", frill="#fffaf0"),
                            dict(color="#7a4a30", front=0.10, grow=0.20), CE.PROFILE_HOURGLASS, ("#e6b85c", "#aa842e")),
    "crowd_woman_b": _woman(66.6, "slim", 0.66, 0.96, 1.08, ("#2f8084", "#1a5256", "#e8d098"), dict(base="#ecd8a0", light="#fff0c4", dark="#bca470", ribbon="#c8505a", frill="#fffaf0"),
                            dict(color="#2e2420", front=0.10, grow=0.22), CE.PROFILE_HOURGLASS, ("#d8704c", "#a04a2c"), mouth="smile"),
    # coach passengers: a gentleman in slate-grey with a powdered wig, a lady in plum with a cream bonnet
    "passenger_a": _man(91.4, "regular", 0.86, 1.00, 1.10, dict(base="#6a7690", dark="#445068", lapel="#8692ac", pants="#40404c"), ("#e8dcc0", "#b0a47c", "#a08c60"),
                        dict(HAT_BLACK, base="#34323a", light="#5e5c6c", dark="#1a1820"), True, dict(color="#eeeaf2", front=0.0, grow=0.0), CE.PROFILE_PEAR, mouth="dash", hat_tilt=2.0),
    "passenger_b": _woman(18.8, "regular", 0.78, 1.00, 1.05, ("#7a4a80", "#4e2a54", "#d8b0d8"), dict(base="#efe4d4", light="#fffaf0", dark="#c0b098", ribbon="#a878b0", frill="#fffaf0"),
                          dict(color="#a8704a", front=0.10, grow=0.20), CE.PROFILE_HOURGLASS, ("#d8c8e0", "#a894b4")),
}

CANVAS12 = {
    "hanway": (-3.3125, -5.375, 3.3125, 0.1875),
    "coachman": (-3.6875, -5.3125, 3.6875, 0.25),
    "coachman_b": (-3.3125, -5.625, 3.3125, 0.125),
    "coachman_c": (-3.4375, -4.75, 3.4375, 0.1875),
    "crowd_man_a": (-3.3125, -5.125, 3.3125, 0.125),
    "crowd_man_b": (-3.3125, -5.25, 3.3125, 0.125),
    "crowd_man_c": (-3.375, -4.875, 3.375, 0.125),
    "crowd_man_d": (-3.3125, -5.3125, 3.3125, 0.125),
    "crowd_woman_a": (-3.3125, -4.9375, 3.3125, 0.25),
    "crowd_woman_b": (-3.3125, -5.0, 3.3125, 0.25),
    "passenger_a": (-3.3125, -5.0, 3.3125, 0.125),
    "passenger_b": (-3.3125, -4.9375, 3.3125, 0.4375),
}
CANVAS12_BOX = {}


STORY12, STORY12_META = {}, {}


# ============================================================================= story poses
def _sh(c, key, dx, dy):
    """hand target relative to the shoulder of arm `key`: dx outward (away from the body), dy down."""
    sx, sy = P.CAST[c]["shoulder"]
    return ((sx + dx) if key == "r" else -(sx + dx), sy + dy)


def _arm(c, key, dx, dy, bend=None, stretch=1.0, shape="ball", layer="front"):
    d = dict(hand=_sh(c, key, dx, dy), stretch=stretch, shape=shape, layer=layer)
    if bend is not None:
        d["bend"] = bend
    return d


def _sit(c, yaw_dir=1.0):
    """legs of a seated figure (thighs forward, shins down) for the cast member c, facing screen-right (mirror=True for left)."""
    f = P.figure(c, {}, "q")
    hp = f["anchors"]["hip"]
    hx = P.CAST[c]["hip_x"]
    lg = P.CAST[c]["leg"]
    fx, fy = 0.52 * lg, 0.52 * lg
    return dict(foot_r=(hp[0] + hx * 0.4 + fx, hp[1] + fy), foot_l=(hp[0] - hx * 0.4 + fx * 0.85, hp[1] + fy), knee_r=1.0, knee_l=1.0, toe_r=0.8, toe_l=0.8)


HU = dict(type="umbrella_black", angle=-100)
WHIP = dict(type="whip", angle=-12)


CYCLE_BASE12 = {}          # story pose name -> (cast, mode, base pose, arms): the arguments that produced a cycle() frame
_LAST = [None]


def _cycle_rec(c, phase, mode="walk", facing=1, base=None, arms="both", speed=1.0):
    r = cycle(c, phase, mode, facing, base, arms, speed)
    _LAST[0] = (c, mode, dict(base or {}), arms)
    return r


class _Rec(dict):
    def __setitem__(self, key, val):
        if _LAST[0] is not None:
            CYCLE_BASE12[key] = _LAST[0]
            _LAST[0] = None
        dict.__setitem__(self, key, val)


def cycle_frame(name, phase, facing=1, speed=1.0):
    """one frame of the walk / run cycle that belongs to the story pose `name` (hanway_walk_umbrella, crowd_man_a_walk_hat, crowd_woman_a_rush ...):
    returns (cast, pose).  phase 0..1 loops (walk 28 frames per cycle, run 16)."""
    c, mode, base, arms = CYCLE_BASE12[name]
    return c, cycle(c, phase, mode, facing, base, arms, speed)


def _story():
    S, M = _Rec(), {}
    cycle = _cycle_rec
    H = "hanway"

    def hold(c="hanway", dx=0.40, dy=0.10):
        return dict(hand=_sh(c, "r", dx, dy), bend=0.5, stretch=1.0, layer="front")
    # ------------------------------------------------------------------ Hanway
    S["hanway_walk_umbrella"] = (H, cycle(H, 0.30, "walk", base=dict(expr="neutral", mouth="smirk", pitch=-0.15, prop_r=dict(HU), arm_r=hold(), yaw=0.75), arms="l"))
    M["hanway_walk_umbrella"] = dict(note="walk frame, open black umbrella in the screen-right hand (angle -100: leaning over him). Animate: cast12.cycle_frame('hanway_walk_umbrella', frame / 28.0, facing) "
                                          "(the umbrella arm stays still, the other arm swings)")
    S["hanway_stroll_smug"] = (H, dict(yaw=0.40, pitch=-0.40, expr="smug", mouth="smirk", head_roll=-4, lean=-3, arm_r=hold(dx=0.42, dy=0.08), prop_r=dict(HU, angle=-98),
                                       arm_l="behind", legs=dict(preset="step", stride=0.55), t=0.3))
    M["hanway_stroll_smug"] = dict(note="dry smug stroll: chin up, umbrella steady, free hand behind his back (shot 18, 21)")
    S["hanway_calm_front"] = (H, dict(yaw=0.0, pitch=-0.15, expr="neutral", mouth="smirk", arm_r=hold(dx=0.30, dy=0.12), prop_r=dict(HU, angle=-95), arm_l="behind", legs="stand"))
    M["hanway_calm_front"] = dict(note="standing calmly under the umbrella, facing the camera (hook, shot 1 / reaction frames)")
    S["hanway_cabbage_flinch"] = (H, dict(yaw=0.45, pitch=-0.10, expr="unimpressed", mouth="flat", head_roll=3, lean=2, arm_r=hold(dx=0.40, dy=0.12), prop_r=dict(HU, angle=-112),
                                          arm_l="behind", legs=dict(preset="step", stride=0.40), leaf_stick=1.0, squash=(1.0, 0.99)))
    M["hanway_cabbage_flinch"] = dict(note="the umbrella knocked back by the cabbage (angle -112), a cabbage leaf stuck on the dome (leaf_stick=1: set it to 0 when the set throws "
                                           "the leaf itself); he keeps walking, unbothered (shots 3, 10)")
    S["hanway_egg_tilt"] = (H, dict(yaw=0.30, pitch=-0.30, expr="smug", mouth="smirk", gaze=(0.3, -0.9), head_roll=4, arm_r=hold(dx=0.42, dy=0.12), prop_r=dict(HU, angle=-74),
                                    arm_l="behind", legs=dict(preset="step", stride=0.30), egg_splat=1.0))
    M["hanway_egg_tilt"] = dict(note="egg splat on the umbrella top (egg_splat 0..1), he tilts the umbrella and glances up, unbothered (shot 11). Animate egg_splat 0 -> 1 on impact")
    S["hanway_mud_splash"] = (H, dict(yaw=0.20, pitch=-0.05, expr="shocked", mouth="o", mud=1.0, squash=(1.06, 0.94), head_roll=-5, lean=-4,
                                      arm_r=dict(hand=_sh(H, "r", 0.55, -0.55), bend=-0.7, stretch=1.2), prop_r=dict(HU, angle=-128), arm_l=dict(hand=_sh(H, "l", 0.50, 0.05), bend=-0.5, shape="open"),
                                      legs="wide", fx=["sweat"]))
    M["hanway_mud_splash"] = dict(note="the mud wave hits: mud=1 (splatters over face, hat, coat, stockings), shocked, umbrella flung back, arms out. Animate mud 0 -> 1 over ~6 frames")
    S["hanway_mud_deadpan"] = (H, dict(yaw=0.0, pitch=0.10, expr="unimpressed", mouth="frown", mud=1.0, blink=0, arm_r=hold(dx=0.30, dy=0.12), prop_r=dict(HU, angle=-96),
                                       arm_l=dict(hand=_sh(H, "l", 0.10, 0.62), bend=0.6), legs="stand", t=0.3))
    M["hanway_mud_deadpan"] = dict(note="after the splash: mud-spattered head to toe, deadpan, umbrella still up (comic, shot 12 end)")
    S["hanway_walk_closed"] = (H, cycle(H, 0.30, "walk", base=dict(expr="neutral", mouth="smirk", pitch=-0.10, yaw=0.75,
                                                                   prop_r=dict(type="umbrella_black_closed", angle=96, scale=0.85), arm_r=dict(hand=_sh(H, "r", 0.30, 0.62), bend=0.5)), arms="l"))
    M["hanway_walk_closed"] = dict(note="walk frame with the furled umbrella as a walking stick (tip down)")
    S["hanway_smile_walk"] = (H, cycle(H, 0.30, "walk", base=dict(expr="happy", mouth="smile", pitch=-0.20, yaw=0.60, prop_r=dict(HU, angle=-98), arm_r=hold(dx=0.42, dy=0.10)), arms="l"))
    M["hanway_smile_walk"] = dict(note="the ending: he smiles as he walks among the sea of umbrellas")

    # ------------------------------------------------------------------ the head coachman
    C = "coachman"
    sit = _sit(C)

    def laugh(c, seated):
        p = dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-7, t=0.3, squash=(1.02, 0.98),
                 arm_r=_arm(c, "r", 0.0, 0.58, 0.9, shape="open"), arm_l=_arm(c, "l", 0.0, 0.58, 0.9, shape="open"), legs=sit if seated else "wide")
        return p

    def pointm(c, seated, lip=False):
        p = dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8, arm_r=_arm(c, "r", 0.58, -0.10, -0.5, 1.3), prop_r=dict(WHIP, angle=-14),
                 arm_l="akimbo", legs=sit if seated else "wide", whip_t=0.2)
        return p

    def boast(c, seated):
        return dict(yaw=0.30, pitch=-0.55, expr="smug", mouth="talk_a", head_roll=-5, lean=-7, squash=(1.02, 1.0), arm_r=_arm(c, "r", 0.35, 0.25, 0.3, 1.0),
                    prop_r=dict(WHIP, angle=-70), arm_l=dict(hand=(-0.18, 0.78), bend=0.8, shape="open", layer="front"), legs=sit if seated else "wide", whip_t=0.5)

    def shout(c, seated):
        return dict(yaw=0.40, pitch=-0.45, expr="shouting", mouth="talk_b", head_roll=6, lean=4, arm_r=_arm(c, "r", 0.35, -0.80, -0.6, 1.3, layer="front"),
                    prop_r=dict(WHIP, angle=-60), arm_l=_arm(c, "l", 0.62, -0.10, -0.5, 1.3, shape="point"), legs=sit if seated else "wide", whip_t=0.8)

    def gloat(c, seated):
        return dict(yaw=0.25, pitch=-0.60, expr="grinning", mouth="grin", head_roll=-6, lean=-5, arm_r="akimbo", arm_l="akimbo", legs=sit if seated else "wide")

    def count(c, seated):
        return dict(yaw=0.15, pitch=0.55, expr="grinning", mouth="grin", head_roll=4, arm_r=_arm(c, "r", -0.05, 0.55, 0.7), prop_r=dict(type="purse"), purse_open=1.0,
                    arm_l=_arm(c, "l", 0.00, 0.40, 0.7), prop_l="coins", legs=sit if seated else "stand")

    def count_sky(c, seated):
        return dict(yaw=0.30, pitch=-0.90, expr="grinning", mouth="grin", head_roll=-8, lean=-4, arm_r=_arm(c, "r", 0.25, 0.10, -0.4, 1.0), prop_r=dict(type="purse"), purse_open=1.0,
                    arm_l="akimbo", legs=sit if seated else "stand")

    def grindrop(c, seated):
        return dict(yaw=0.25, pitch=0.10, expr="stunned", mouth="flat", head_roll=3, arm_r="down", arm_l="down", legs=sit if seated else "stand", fx=["sweat"])

    def sulk(c, seated):
        return dict(yaw=0.45, pitch=0.55, expr="sad", mouth="frown", head_roll=7, lean=3, arm_l="chin", arm_r=dict(hand=_sh(c, "r", 0.22, 0.05), bend=0.3, layer="front"),
                    prop_r=dict(type="umbrella_pink", angle=-96), legs=sit if seated else "stand", t=0.3)

    def windup(c, seated, veg="cabbage12"):
        return dict(yaw=0.40, pitch=-0.10, expr="grinning", mouth="grin", head_roll=-6, lean=-9, arm_r=_arm(c, "r", 0.10, -0.85, -1.0, 1.3), prop_r=dict(type=veg),
                    arm_l="akimbo", legs=dict(preset="step", stride=-0.4) if not seated else sit)

    def release(c, seated):
        return dict(yaw=0.45, pitch=-0.10, expr="shouting", mouth="talk_b", head_roll=4, lean=9, squash=(0.98, 1.02), arm_r=_arm(c, "r", 0.85, -0.35, -0.3, 1.3, shape="open"),
                    arm_l=dict(hand=_sh(c, "l", -0.05, 0.55), bend=0.5), legs=dict(preset="step", stride=0.8) if not seated else sit)

    def glare(c, seated):
        return dict(yaw=0.55, pitch=-0.20, expr="angry", mouth="flat", head_roll=4, arm_r="akimbo", arm_l="akimbo", legs=sit if seated else "wide")

    def nod(c, seated):
        return dict(yaw=0.30, pitch=0.25, expr="smug", mouth="smirk", head_roll=-3, arm_r="akimbo", arm_l=dict(hand=_sh(c, "l", 0.0, 0.58), bend=0.7), legs=sit if seated else "stand")

    def roar(c, seated):
        return dict(yaw=0.20, pitch=-0.70, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=8, lean=5, t=0.3, arm_r=_arm(c, "r", 0.30, -0.60, -0.8, 1.2, shape="open"),
                    arm_l=_arm(c, "l", 0.10, 0.50, 0.8, shape="open"), legs=sit if seated else "wide")

    def point_laugh(c, seated):
        return dict(yaw=0.40, pitch=-0.55, expr="laughing", mouth="talk_b", head_roll=-8, lean=-4, t=0.3, arm_r=_arm(c, "r", 0.58, -0.10, -0.5, 1.3, shape="point"),
                    arm_l=_arm(c, "l", 0.0, 0.58, 0.9, shape="open"), legs=sit if seated else "wide")
    for seated in (False, True):
        pre = "coachman_box_" if seated else "coachman_"
        for nm, fn in (("laugh", laugh), ("point_mock", pointm), ("boast", boast), ("shout", shout), ("gloat", gloat), ("count_coins", count), ("grin_drop", grindrop),
                       ("throw_windup", windup), ("throw_release", release), ("nod", nod)):
            S[pre + nm] = (C, fn(C, seated))
        S[pre + "count_coins_sky"] = (C, count_sky(C, seated))
    S["coachman_sulk_under_pink_umbrella"] = (C, sulk(C, True))
    S["coachman_sulk_standing"] = (C, sulk(C, False))
    for nm in ("point_mock", "boast", "shout"):
        for pre in ("coachman_", "coachman_box_"):
            M[pre + nm] = dict(lipsync=True, note="head coachman quote pose: LIP-SYNC (mouth = talk_mouth(g) inside the quote windows 12.66-19.0 s and 33.0-34.9 s, 'flat' otherwise). "
                                                 "pose key whip_t animates the lash")
    M["coachman_laugh"] = dict(note="belly laugh, hands on the belly, tears; the open laugh mouth is a held shape; animate squash (1.02, 0.98) <-> (0.99, 1.01) every 4 frames. "
                                    "coachman_box_laugh = the same seated on the coach box (legs of the seat; the box itself comes from the set, or pose coach_box=1)")
    M["coachman_sulk_under_pink_umbrella"] = dict(note="the ending: seated on the empty coach box under his wife's pink frilled lace umbrella (prop umbrella_pink), chin on his hand, sulking. "
                                                       "coach_box=0: the set supplies the box; pass coach_box=1 for a self-contained seat. anchors umb_top_r / umb_mid_r / umb_edge1_r / umb_edge2_r")
    M["coachman_count_coins"] = dict(note="looking down at the purse (prop purse, anchor purse_bottom_r) with coins in the other palm; _sky looks up at the rain grinning (shot 15)")
    M["coachman_throw_windup"] = dict(note="arm back holding a cabbage (prop cabbage12, anchor cabbage_r) ready to throw; spawn the flying cabbage from the anchor, or use cabbage_svg")
    M["coachman_throw_release"] = dict(note="the arm snapped forward, hand open, the cabbage gone (the set flies it): lean forward, shouting")
    M["coachman_grin_drop"] = dict(note="the grin drops (shot 18): stunned eyes, flat mouth, sweat")

    # ------------------------------------------------------------------ the two jeerers
    for c, tag in (("coachman_b", "_b"), ("coachman_c", "_c")):
        sit_c = _sit(c)
        for seated in (False, True):
            pre = c + ("_box_" if seated else "_")
            lst = (("laugh", laugh), ("point_laugh", point_laugh), ("glare", glare), ("nod", nod), ("roar", roar), ("throw_windup", windup), ("throw_release", release))
            for nm, fn in lst:
                p = fn(c, seated)
                if seated:
                    p["legs"] = sit_c
                S[pre + nm] = (c, p)
        S[c + "_throw_egg_windup"] = (c, windup(c, False, "egg"))
        M[c + "_throw_windup"] = dict(note="cabbage wind-up; _throw_egg_windup holds an egg (prop egg) instead; _throw_release = the arm snapped forward")
        M[c + "_roar"] = dict(note="roaring with laughter (the other coachmen roar at the boast, shot 8)")
        M[c + "_glare"] = dict(note="glaring at Hanway (shot 2)")
        M[c + "_box_laugh"] = dict(note="seated on the coach box (see coachman_box_*)")

    # ------------------------------------------------------------------ crowd men
    def men_poses(c):
        sx, sy = P.CAST[c]["shoulder"]
        S[c + "_walk_hat"] = (c, cycle(c, 0.30, "walk", base=dict(expr="worried", mouth="frown", pitch=0.35, lean=5, yaw=0.75, hat_off=1.0, soaked=0.55,
                                                                   prop_r=dict(type="tricorn_held", angle=0), arm_r=dict(hand=(sx + 0.10, -0.34), bend=-0.9, stretch=1.25, layer="top")), arms="l"))
        S[c + "_walk_soaked"] = (c, cycle(c, 0.30, "walk", base=dict(expr="unimpressed", mouth="frown", pitch=0.30, lean=6, yaw=0.75, soaked=0.9, fx=["sweat"]), arms="both"))
        S[c + "_point_laugh"] = (c, dict(yaw=0.40, pitch=-0.35, expr="laughing", mouth="talk_b", head_roll=-8, t=0.3, arm_r=_arm(c, "r", 0.58, -0.10, -0.5, 1.3, shape="point"),
                                         arm_l=_arm(c, "l", 0.0, 0.55, 0.9, shape="open"), legs="wide"))
        S[c + "_rush"] = (c, cycle(c, 0.20, "run", base=dict(expr="shouting", mouth="talk_b", pitch=-0.10, yaw=0.80), arms="both"))
        S[c + "_push"] = (c, dict(yaw=0.70, pitch=0.05, expr="angry", mouth="clench", lean=15, arm_r=_arm(c, "r", 0.62, 0.05, -0.4, 1.3, shape="open"),
                                  arm_l=_arm(c, "l", 0.62, 0.15, -0.4, 1.3, shape="open", layer="back"), legs=dict(preset="step", stride=0.9)))
        M[c + "_walk_hat"] = dict(note="hunched walk, soaked tint, hat held over the head with the right hand (hat_off=1 + prop tricorn_held). Animate with cast12.cycle_frame(name, frame / 28.0, facing)")
        M[c + "_walk_soaked"] = dict(note="hunched, soaked (soaked=0.9: blue-grey tint, drips, sweat); animate with cast12.cycle_frame(name, frame / 28.0, facing)")
        M[c + "_rush"] = dict(note="running frame (run cycle), shouting; animate cast12.cycle_frame(name, frame / 16.0, facing) for the crowd rushing the coaches (shot 16)")
        M[c + "_push"] = dict(note="shoving through the crowd: both arms forward, leaning in, teeth clenched")
    for c in ("crowd_man_a", "crowd_man_b", "crowd_man_c", "crowd_man_d"):
        men_poses(c)
    for c in ("crowd_man_a", "crowd_man_c", "crowd_man_d"):
        S[c + "_wring_wig"] = (c, dict(yaw=0.20, pitch=0.30, expr="worried", mouth="wavy", soaked=1.0, wig_off=1.0, hat_off=1.0, t=0.3, arm_r=dict(hand=(0.10, 0.80), bend=0.7, layer="front"),
                                       prop_r=dict(type="wig"), arm_l=dict(hand=(-0.08, 0.95), bend=0.7, layer="front"), legs="stand", fx=["sweat"]))
        M[c + "_wring_wig"] = dict(note="a soaked gentleman wrings out his wig (the head is bare: wig_off=1; prop wig; soaked=1 animates the drips with t) (shot 5)")
    # the gentleman who opens his umbrella (3 stages) (shot 19-20)
    for c in ("crowd_man_a", "crowd_man_d", "crowd_man_c"):
        sx, sy = P.CAST[c]["shoulder"]
        S[c + "_open_1"] = (c, dict(yaw=0.50, pitch=-0.10, expr="stunned", mouth="flat", head_roll=-3, gaze=(0.8, 0.0), arm_r=dict(hand=(sx + 0.30, 0.55), bend=0.5),
                                    prop_r=dict(type="umbrella_black_closed", angle=-62), arm_l="hip", legs="stand"))
        S[c + "_open_2"] = (c, dict(yaw=0.30, pitch=-0.20, expr="excited", mouth="o", head_roll=2, umb_open=0.5, arm_r=dict(hand=(sx + 0.25, 0.05), bend=-0.6, stretch=1.15),
                                    prop_r=dict(type="umbrella_black", angle=-82), arm_l=dict(hand=(sx + 0.10, 0.18), bend=-0.2, shape="open", layer="front"), legs="stand"))
        S[c + "_open_3"] = (c, dict(yaw=0.20, pitch=-0.30, expr="happy", mouth="smile", head_roll=-3, umb_open=1.0, arm_r=dict(hand=(sx + 0.25, 0.30), bend=0.3),
                                    prop_r=dict(type="umbrella_black", angle=-98), arm_l="hip", legs="stand"))
        M[c + "_open_1"] = dict(note="stage 1 of a gentleman opening his umbrella: the furled umbrella in his hand, staring at Hanway")
        M[c + "_open_2"] = dict(note="stage 2: the umbrella half open (umb_open=0.5; animate 0.15 -> 0.9), surprised mouth")
        M[c + "_open_3"] = dict(note="stage 3: fully open overhead, smiling (umb_open=1). Animate the three stages with umb_open from 0 to 1 and prop type umbrella_black")

    # ------------------------------------------------------------------ crowd women
    def women_poses(c, col):
        sx, sy = P.CAST[c]["shoulder"]
        U = dict(type="umbrella_small", angle=-105, scale=0.78)
        S[c + "_walk_umbrella"] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral", mouth="smile", yaw=0.75, umb_col=col, prop_r=dict(U), arm_r=dict(hand=(sx + 0.15, 0.16), bend=0.5)), arms="l"))
        S[c + "_dry_pass"] = (c, dict(yaw=0.40, pitch=-0.45, expr="smug", mouth="smirk", head_roll=-4, umb_col=col, prop_r=dict(U, angle=-100), arm_r=dict(hand=(sx + 0.15, 0.16), bend=0.5),
                                      arm_l=dict(hand=(-sx - 0.05, 0.60), bend=0.8), legs=dict(preset="step", stride=0.5)))
        S[c + "_point_laugh"] = (c, dict(yaw=0.40, pitch=-0.35, expr="laughing", mouth="talk_b", head_roll=-8, t=0.3, umb_col=col, prop_l=dict(U, angle=-75), arm_l=dict(hand=(-sx - 0.18, 0.22), bend=0.5),
                                         arm_r=_arm(c, "r", 0.55, -0.10, -0.5, 1.3, shape="point"), legs="stand"))
        S[c + "_rush"] = (c, cycle(c, 0.20, "run", base=dict(expr="shocked", mouth="o", yaw=0.80, umb_col=col, prop_r=dict(U, angle=-125), arm_r=dict(hand=(sx + 0.25, 0.05), bend=-0.6), pitch=0.0), arms="l"))
        S[c + "_push"] = (c, dict(yaw=0.70, expr="angry", mouth="clench", lean=12, umb_col=col, arm_r=_arm(c, "r", 0.55, 0.05, -0.4, 1.3, shape="open"), arm_l=_arm(c, "l", 0.55, 0.15, -0.4, 1.3, shape="open", layer="back"),
                                  legs=dict(preset="step", stride=0.8)))
        M[c + "_walk_umbrella"] = dict(note="walk frame under a small umbrella (prop umbrella_small, scale 0.78, colour by pose key umb_col); animate with cast12.cycle_frame(name, frame / 28.0, facing)")
        M[c + "_dry_pass"] = dict(note="passes by dry and smug under her umbrella (shot 5)")
    women_poses("crowd_woman_a", "maroon")
    women_poses("crowd_woman_b", "green")

    # ------------------------------------------------------------------ passengers
    for c in ("passenger_a", "passenger_b"):
        sit_p = _sit(c)
        S[c + "_seated"] = (c, dict(yaw=0.30, expr="neutral", mouth="smirk", arm_r=dict(hand=(0.30, 1.02), bend=0.7), arm_l=dict(hand=(-0.30, 1.02), bend=0.7), legs=sit_p))
        S[c + "_peek"] = (c, dict(yaw=0.80, pitch=0.0, expr="shocked", mouth="o", lean=8, head_dx=0.06, arm_r=_arm(c, "r", 0.45, 0.10, -0.4, 1.0, shape="open"), arm_l="down", legs=sit_p))
        S[c + "_laugh"] = (c, dict(yaw=0.30, pitch=-0.60, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, t=0.3, arm_r=dict(hand=(0.30, 1.00), bend=0.8, shape="open"),
                                   arm_l=dict(hand=(-0.30, 1.00), bend=0.8, shape="open"), legs=sit_p))
        M[c + "_seated"] = dict(note="a coach passenger seated (thighs forward); the set's coach body hides the lower half. _peek leans out to look, _laugh laughs")
    return dict(S), M


# ============================================================================= registration
def register():
    if getattr(P, "_cast12_registered", False):
        CE.register_stage()
        if not STORY12:
            s, m = _story()
            STORY12.update(s)
            STORY12_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_ink_limb", "figure"):
        _O12[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._ink_limb = _ink_limb
    P.figure = figure
    CE.COSTUMES.update(COSTUMES12)
    CE.HATS.update(HATS12)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS12 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP12)
    for n, c in NEW_CAST12.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS12)
    P._cast12_registered = True
    s, m = _story()
    STORY12.update(s)
    STORY12_META.update(m)
    P.STORY.update(STORY12)
    CE.register_stage()


register()
