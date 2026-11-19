#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast18.py -- the cast of film 18 ("the ox clerk": Tian Dan's fire oxen at Jimo, Warring States China, 279 BC, night) for the
v2 puppet, as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast18"); import cast18    # registers on import (idempotent)
    import puppet                                                     # the same module object, now with the new members
    cast, pose = cast18.STORY18["tiandan_tug_cloth"]
    f = puppet.figure(cast, pose, "f")
    ox = cast18.ox_figure("dragon", "side", "gallop", phase=0.25, flame=1, uid="ox")      # the ox is NOT a puppet: see API.md

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  robe18 (cross-collar hemp robe, sash, optional bamboo tally slips, optional contrast skirt), armour18
                       (dark lacquered lamellar with red cords, bronze belt, tassets; soldier variant)
    cast_ext.HATS      scholar18 (small black cap on a topknot), helm18 (bronze plumed helmet / iron cap / cloth cap),
                       bun18 (woman's bun and pin), tufts18 (child's twin tufts)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast10's wrappers: _norm (this module's pose keys), _face (long beard), _moustache (style
yan18), _ink_limb (shoulder lamellar guards), _prop (new props), figure (nothing extra).
New cast: tiandan, general, yan_soldier_a/b/c, old_man, woman, child, envoy, qi_soldier.
The ox (plain / dragon coat, blades, reed tail, flame) is a standalone drawing: ox_figure() / ox_svg(); flame_svg().
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
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW18 = ("tiandan", "general", "yan_soldier_a", "yan_soldier_b", "yan_soldier_c", "old_man", "woman", "child", "envoy", "qi_soldier")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_taper = C9._taper
_O18 = {}
_POSE18 = {"askew": 0.0, "fire": 0, "t": 0.0, "pot": 0.0, "slips": 1.0, "cup": 0.0, "bside": 1.0}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours
BRONZE = dict(light="#f6d27a", base="#cc9440", dark="#8a5a22", deep="#5a3a14")
LACQ = dict(light="#6a5a7c", base="#2e2834", dark="#1a1620", deep="#100e14")       # dark lacquer, a plum black
CORD = dict(light="#e8505a", base="#c0262e", dark="#7e1218")                       # red lacing cord
BAMBOO = dict(light="#f0dc9c", base="#d4b46a", dark="#8e7236")
HEMP = dict(light="#e4b86a", base="#c4924a", dark="#8c6228")
WOOD18 = dict(light="#d8a468", base="#a8703c", dark="#6a4420")
SILK = dict(light="#e8404a", base="#c4202c", dark="#7c1018", deep="#4e0a10")        # crimson silk
GOLD = dict(light="#fff0a8", base="#e8b840", dark="#a47a1c", deep="#6a4c0c")
FIRE = dict(core="#fffeec", mid="#ffb238", edge="#e8561c", deep="#b8340e")        # tail flame: never pure yellow
STRAW = dict(light="#e8d48c", base="#c8aa58", dark="#8a7030")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _path(d, fill, ink, sw=0.020, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"%s/>' % (d, fill, ink, sw, extra)


def _grad3(k, name, col, x0, x1, y0=0.0, y1=0.0):
    return _lin(k, name, col["light"], col["base"], col["dark"], x0, y0, x1, y1)


def _lamellar(k, name, base_dark, light, cord, w=0.15, h=0.105, sw=0.010):
    """a pattern of lacquered plates: rows of rounded plates (edges, a glint) laced with red cord (a horizontal lace on every
    row, a short vertical lace between plates).  Transparent ground: lies over the torso gradient."""
    pid = "%s_%s" % (k.uid, name)
    o = []
    for r in range(2):
        y = r * h
        off = 0.0 if r == 0 else w / 2
        for c in (-1, 0, 1):
            x = off + c * w
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
                     % (x + 0.01, y + 0.005, x + w - 0.01, y + 0.005, x + w - 0.01, y + h - 0.004, x + 0.01, y + h - 0.004, k.c(base_dark), sw * 1.6))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.7"/>'
                     % (x + 0.03, y + 0.030, x + 0.075, y + 0.028, k.c(light), sw))
        o.append('<path d="M-1,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f"/>' % (y + h * 0.5, 3 * w, y + h * 0.5, k.c(cord), sw * 1.3))
        for c in (-1, 0, 1, 2):
            x = off + c * w + w * 0.5 if False else off + c * w
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (x, y + 0.012, x, y + h - 0.010, k.c(cord), sw * 1.3))
    k.defs.append('<pattern id="%s" width="%.4f" height="%.4f" patternUnits="userSpaceOnUse">%s</pattern>' % (pid, w, 2 * h, "".join(o)))
    return "url(#%s)" % pid


# ============================================================================= hats / hair (head frame, head centre (0, 0))
def _askew_open(C):
    """extra rotation for a helmet / cap knocked askew (pose hat_askew, degrees): about the brow centre."""
    a = _POSE18["askew"]
    if abs(a) < 0.01:
        return "", "", 0.0
    return '<g transform="translate(0 -0.15) rotate(%.3f) translate(0 0.15)">' % a, "</g>", a


def _bowl_d(dx, yb, top, hw, drop=0.05):
    cy = yb + (top - yb) / 0.75
    return "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (dx - hw, yb, dx - hw, cy, dx + hw, cy, dx + hw, yb, dx, yb + drop, dx - hw, yb)


def _plume(k, tx, ty, s, col_main, col_dark, n=9, ln=0.85, droop=1.0, sw=0.012):
    """a horsehair plume rising from the socket (tx, ty) and streaming backwards (side s = -1 left, +1 right)."""
    o = []
    for i in range(n):
        u = (i - (n - 1) / 2.0) / ((n - 1) / 2.0)
        L = ln * (0.78 + 0.22 * (1 - abs(u)))
        pts = []
        for j in range(7):
            t = j / 6.0
            x = tx + s * (0.05 + 0.80 * L * t * (0.78 + 0.20 * u)) + 0.04 * u * t
            y = ty - 0.30 * math.sin(math.pi * min(1.0, t * 1.1)) * (0.90 + 0.25 * (1 - abs(u))) + droop * 0.50 * t * t * L + 0.06 * u * t
            pts.append((x, y))
        c = col_dark if i % 3 == 1 else col_main
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_taper(pts, 0.085 - 0.01 * abs(u), 0.012), k.c(c), k.ink, sw))
    return "".join(o)


def _hat_helm18(k, C, yaw):
    """Yan helmets.  C["helm18"] = dict(kind="general" | "iron" | "cloth" | "flap", plume="tall"|"tuft"|"none").
    general: a bronze bowl with a ridge comb, brow band with rivets, lamellar ear flaps and a tall red horsehair plume.
    iron: a small black iron bowl, red brow cord, a red tuft.  cloth: a soft black wrapped cap with a red band and a knot.
    flap: the iron bowl with ear flaps and a big red pompom."""
    spec = C.get("helm18", {})
    kind = spec.get("kind", "general")
    col = C.get("hat_colors", {})
    dx = -0.03 * yaw
    fx = dx + 0.10 * yaw
    s = -1.0 if yaw >= 0 else 1.0
    o0, o1, askew = _askew_open(C)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"], o0]
    ext = []
    yb = -0.20
    if kind in ("general", "flap"):
        # lamellar ear flaps
        for sd in (-1, 1):
            g = _clamp(1.0 - 0.55 * max(0.0, sd * yaw), 0.4, 1.0)
            xi, xo = dx + sd * 0.40, dx + sd * (0.40 + 0.17 * g)
            fp = [(xi, yb - 0.02), (xo, yb - 0.04), (xo + sd * 0.02, 0.16), (xo - sd * 0.01, 0.38), ((xi + xo) / 2, 0.42), (xi + sd * 0.02, 0.34)]
            d = P._smooth_closed(fp)
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, k.c(col.get("flap", LACQ["base"])), k.ink))
            o.append('<path d="%s" fill="%s" opacity="0.9"/>' % (d, _lamellar(k, "hf%d" % (sd + 1), LACQ["deep"], LACQ["light"], CORD["base"], w=0.075, h=0.055, sw=0.006)))
            ext.append((xo + sd * 0.03, 0.40))
    top = -0.66
    if kind == "general":
        top = -0.66
        o.append(_plume(k, fx, -0.70, s, "#c8282f", "#6a1016", n=9, ln=0.95, droop=1.0))
        ext += [(fx + s * 0.95, -0.35), (fx + s * 0.6, -0.78), (fx, -0.98)]
        g = _grad3(k, "hb", dict(light=col.get("light", BRONZE["light"]), base=col.get("base", BRONZE["base"]), dark=col.get("dark", BRONZE["dark"])), -0.55, 0.55)
        o.append(_path(_bowl_d(dx, yb, top, 0.51, 0.05), g, k.ink, 0.026))
        # ridge comb
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (fx - 0.01, yb - 0.02, fx + 0.03, top + 0.12, fx, top + 0.02, k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (fx - 0.01, yb - 0.02, fx + 0.03, top + 0.12, fx, top + 0.02, k.c(BRONZE["dark"])))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (fx - 0.025, yb - 0.04, fx + 0.01, top + 0.14, fx - 0.012, top + 0.04, k.c(BRONZE["light"])))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>' % (dx - 0.40, yb - 0.10, dx - 0.36, top + 0.14, dx - 0.18, top + 0.07))
        # brow band with rivets and a red cord
        bd = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
              % (dx - 0.53, yb - 0.115, dx, yb - 0.075, dx + 0.53, yb - 0.115, dx + 0.52, yb + 0.040, dx, yb + 0.090, dx - 0.52, yb + 0.040))
        o.append(_path(bd, k.c(BRONZE["base"]), k.ink, 0.022))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" opacity="0.9"/>' % (dx - 0.50, yb - 0.04, dx, yb + 0.005, dx + 0.50, yb - 0.04, k.c(CORD["base"])))
        for i in range(7):
            u = -0.44 + 0.88 * i / 6.0
            o.append('<circle cx="%.4f" cy="%.4f" r="0.014" fill="%s" stroke="%s" stroke-width="0.006"/>' % (fx * 0.5 + u * 0.99, yb - 0.075 + 0.06 * (1 - (u / 0.5) ** 2) * 0.55 + 0.015, k.c(BRONZE["light"]), k.ink))
        # socket
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                 % (fx - 0.060, top + 0.04, fx + 0.060, top + 0.04, fx + 0.045, top - 0.07, fx - 0.045, top - 0.07, k.c(BRONZE["base"]), k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.060" ry="0.020" fill="%s" stroke="%s" stroke-width="0.014"/>' % (fx, top - 0.07, k.c(BRONZE["light"]), k.ink))
        ext += [(dx - 0.55, yb), (dx + 0.55, yb), (fx, top - 0.10)]
        topy = top - 0.10
    elif kind in ("iron", "flap"):
        top = -0.60
        g = _grad3(k, "hb", dict(light=col.get("light", "#7a7488"), base=col.get("base", "#3e3a48"), dark=col.get("dark", "#1e1a26")), -0.55, 0.55)
        if spec.get("plume", "tuft") != "none":
            o.append(_plume(k, fx, -0.62, s, "#c8282f", "#6a1016", n=5, ln=0.34 if kind == "iron" else 0.22, droop=0.6))
        o.append(_path(_bowl_d(dx, yb, top, 0.50, 0.05), g, k.ink, 0.026))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>' % (dx - 0.38, yb - 0.10, dx - 0.34, top + 0.14, dx - 0.16, top + 0.07, k.c(col.get("light", "#7a7488"))))
        bd = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
              % (dx - 0.52, yb - 0.10, dx, yb - 0.07, dx + 0.52, yb - 0.10, dx + 0.51, yb + 0.03, dx, yb + 0.075, dx - 0.51, yb + 0.03))
        o.append(_path(bd, k.c(CORD["base"]), k.ink, 0.020))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (dx - 0.48, yb - 0.01, dx, yb + 0.03, dx + 0.48, yb - 0.01, k.c(CORD["dark"])))
        if kind == "flap":
            o.append('<circle cx="%.4f" cy="%.4f" r="0.085" fill="%s" stroke="%s" stroke-width="0.020"/>' % (fx, top - 0.02, k.c(CORD["base"]), k.ink))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.025" fill="%s"/>' % (fx - 0.03, top - 0.05, k.c(CORD["light"])))
            topy = top - 0.11
        else:
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.022" fill="%s" stroke="%s" stroke-width="0.014"/>' % (fx, top + 0.01, k.c(BRONZE["base"]), k.ink))
            topy = top - 0.03
        ext += [(dx - 0.53, yb), (dx + 0.53, yb), (fx, topy)]
    else:   # cloth cap: a soft wrapped black cap, a red band, a knot on top
        top = -0.62
        cl = dict(light=col.get("light", "#585064"), base=col.get("base", "#26222e"), dark=col.get("dark", "#12101a"))
        g = _grad3(k, "hb", cl, -0.55, 0.55)
        pts = [(dx - 0.50, yb), (dx - 0.52, yb - 0.20), (dx - 0.38, -0.54), (dx - 0.14, top + 0.03), (dx + 0.10, top), (dx + 0.36, -0.54), (dx + 0.52, yb - 0.20), (dx + 0.50, yb)]
        o.append(_path(P._smooth_open(pts) + " Z", g, k.ink, 0.026))
        o.append('<path d="M%.4f,-0.34 Q%.4f,-0.46 %.4f,-0.52 M%.4f,-0.30 Q%.4f,-0.40 %.4f,-0.46" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                 % (dx - 0.36, dx - 0.30, dx - 0.12, dx + 0.34, dx + 0.28, dx + 0.12, k.c(cl["light"])))
        bd = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
              % (dx - 0.52, yb - 0.12, dx, yb - 0.08, dx + 0.52, yb - 0.12, dx + 0.51, yb + 0.03, dx, yb + 0.08, dx - 0.51, yb + 0.03))
        o.append(_path(bd, k.c(spec.get("band", CORD["base"])), k.ink, 0.020))
        kn = [(fx - 0.13, top + 0.04), (fx - 0.10, top - 0.08), (fx, top - 0.12), (fx + 0.10, top - 0.08), (fx + 0.13, top + 0.04)]
        o.append(_path(P._smooth_open(kn) + " Z", k.c(cl["base"]), k.ink, 0.020))
        o.append('<path d="M%.4f,%.4f q0.04,0.03 0.0,0.07" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (fx - 0.01, top - 0.09, k.c(cl["light"])))
        ext += [(dx - 0.54, yb), (dx + 0.54, yb), (fx, top - 0.13)]
        topy = top - 0.13
    o.append(o1)
    o.append('</g>')
    C4._ext_hat(k, C, ext)
    return "".join(o), (fx, topy)


def _hat_scholar18(k, C, yaw):
    """a topknot and a small black cap (guan) with a bone pin; two thin ties at the ears.  hat_colors cap / cap_l / cap_d / pin."""
    col = C.get("hat_colors", {})
    dx = -0.03 * yaw
    fx = dx + 0.06 * yaw
    cap = dict(light=col.get("cap_l", "#4e4660"), base=col.get("cap", "#1c1822"), dark=col.get("cap_d", "#0c0a10"))
    o0, o1, askew = _askew_open(C)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"], o0]
    hair, top = C4._hair_dome(k, C, dx, -0.22, -0.50)
    o.append(hair)
    o.append('<path d="M%.4f,-0.30 Q%.4f,-0.42 %.4f,-0.47" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (dx - 0.32, dx - 0.22, dx - 0.04, k.c(C["hair"].get("shine", "#5a5a70"))))
    # the cap: a small flat-topped trapezoid sitting on the crown, a pin through it
    g = _grad3(k, "sc", cap, -0.36, 0.36)
    cp = [(fx - 0.34, -0.40), (fx - 0.31, -0.52), (fx - 0.24, -0.66), (fx - 0.06, -0.70), (fx + 0.16, -0.69), (fx + 0.27, -0.64), (fx + 0.32, -0.52), (fx + 0.35, -0.40)]
    d = P._smooth_open(cp) + " Q%.4f,%.4f %.4f,%.4f Z" % (fx, -0.34, fx - 0.34, -0.40)
    o.append(_path(d, g, k.ink, 0.026))
    o.append('<path d="M%.4f,-0.58 Q%.4f,-0.66 %.4f,-0.68" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.35"/>' % (fx - 0.20, fx - 0.16, fx - 0.04))
    o.append('<path d="M%.4f,-0.46 Q%.4f,-0.42 %.4f,-0.46" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (fx - 0.30, fx, fx + 0.30, k.c(cap["dark"])))
    pn = col.get("pin", "#e6d8b0")
    o.append('<path d="M%.4f,-0.54 L%.4f,-0.56" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (fx - 0.46, fx + 0.46, k.ink))
    o.append('<path d="M%.4f,-0.54 L%.4f,-0.56" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (fx - 0.45, fx + 0.45, k.c(pn)))
    # ties
    for sd in (-1, 1):
        o.append('<path d="M%.4f,-0.34 Q%.4f,-0.15 %.4f,-0.02" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (dx + sd * 0.40, dx + sd * 0.52, dx + sd * 0.46, k.ink))
        o.append('<path d="M%.4f,-0.34 Q%.4f,-0.15 %.4f,-0.02" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (dx + sd * 0.40, dx + sd * 0.52, dx + sd * 0.46, k.c(cap["light"])))
    o.append(o1)
    o.append('</g>')
    C4._ext_hat(k, C, ((fx - 0.47, -0.55), (fx + 0.47, -0.56), (fx, -0.71), (dx - 0.50, -0.02), (dx + 0.50, -0.02)))
    return "".join(o), (fx, -0.70)


def _hat_bun18(k, C, yaw):
    """a woman's hair: a smooth dome parted in the middle, a round bun on the crown with a bone hairpin and a red cord, two
    side locks.  hat_colors pin / cord."""
    col = C.get("hat_colors", {})
    dx = -0.03 * yaw
    hc = k.c(C["hair"]["color"])
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    bx = dx - 0.06 * yaw
    o.append('<ellipse cx="%.4f" cy="-0.64" rx="0.20" ry="0.15" fill="%s" stroke="%s" stroke-width="0.024"/>' % (bx, hc, k.ink))
    o.append('<path d="M%.4f,-0.68 Q%.4f,-0.76 %.4f,-0.72" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (bx - 0.12, bx - 0.02, bx + 0.08, k.c(C["hair"].get("shine", "#5a5a70"))))
    hair, top = C4._hair_dome(k, C, dx, -0.20, -0.55)
    o.append(hair)
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.40 %.4f,-0.24" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (dx, dx - 0.02, dx - 0.03, k.c(C["hair"].get("shine", "#5a5a70"))))
    o.append('<path d="M%.4f,-0.34 Q%.4f,-0.46 %.4f,-0.52" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (dx - 0.32, dx - 0.26, dx - 0.06, k.c(C["hair"].get("shine", "#5a5a70"))))
    # the cord tying the bun, and a long bone pin through it
    o.append('<path d="M%.4f,-0.54 L%.4f,-0.54" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (bx - 0.16, bx + 0.16, k.ink))
    o.append('<path d="M%.4f,-0.54 L%.4f,-0.54" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (bx - 0.15, bx + 0.15, k.c(col.get("cord", "#c0262e"))))
    o.append('<path d="M%.4f,-0.76 L%.4f,-0.56" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (bx - 0.28, bx + 0.32, k.ink))
    o.append('<path d="M%.4f,-0.76 L%.4f,-0.56" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (bx - 0.27, bx + 0.31, k.c(col.get("pin", "#efe2bc"))))
    # side locks over the ears
    for sd in (-1, 1):
        o.append('<path d="M%.4f,-0.20 Q%.4f,-0.02 %.4f,0.12 Q%.4f,0.02 %.4f,-0.12 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
                 % (dx + sd * 0.45, dx + sd * 0.55, dx + sd * 0.50, dx + sd * 0.40, dx + sd * 0.37, hc, k.ink))
    o.append('</g>')
    C4._ext_hat(k, C, ((bx - 0.30, -0.78), (bx + 0.34, -0.56), (bx, -0.79), (dx - 0.58, 0.12), (dx + 0.58, 0.12)))
    return "".join(o), (bx, -0.79)


def _hat_tufts18(k, C, yaw):
    """a child's hair: a short dome, two round tufts (buns) tied with red cord, one each side of the crown."""
    col = C.get("hat_colors", {})
    dx = -0.03 * yaw
    hc = k.c(C["hair"]["color"])
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    for sd in (-1, 1):
        g = _clamp(1.0 - 0.45 * max(0.0, sd * yaw), 0.55, 1.0)
        x = dx + sd * 0.30 * (0.92 + 0.08 * g)
        o.append('<ellipse cx="%.4f" cy="-0.60" rx="%.4f" ry="0.15" fill="%s" stroke="%s" stroke-width="0.024"/>' % (x, 0.145 * g, hc, k.ink))
        o.append('<path d="M%.4f,-0.66 Q%.4f,-0.71 %.4f,-0.69" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (x - 0.07, x - 0.01, x + 0.05, k.c(C["hair"].get("shine", "#5a5a70"))))
    hair, top = C4._hair_dome(k, C, dx, -0.22, -0.52)
    o.append(hair)
    for sd in (-1, 1):
        g = _clamp(1.0 - 0.45 * max(0.0, sd * yaw), 0.55, 1.0)
        x = dx + sd * 0.30 * (0.92 + 0.08 * g)
        o.append('<path d="M%.4f,-0.50 L%.4f,-0.50" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (x - 0.09 * g, x + 0.09 * g, k.ink))
        o.append('<path d="M%.4f,-0.50 L%.4f,-0.50" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x - 0.085 * g, x + 0.085 * g, k.c(col.get("cord", "#c0262e"))))
    o.append('<path d="M%.4f,-0.34 Q%.4f,-0.45 %.4f,-0.49" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (dx - 0.26, dx - 0.18, dx - 0.04, k.c(C["hair"].get("shine", "#5a5a70"))))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.46, -0.60), (dx + 0.46, -0.60), (dx - 0.30, -0.76), (dx + 0.30, -0.76)))
    return "".join(o), (dx, -0.76)


HATS18 = {"helm18": _hat_helm18, "scholar18": _hat_scholar18, "bun18": _hat_bun18, "tufts18": _hat_tufts18}


# ============================================================================= costumes (torso-local)
def _slips(k, x, y, ln, col_cord="#7a3a22"):
    """a bundle of bamboo tally slips tucked behind the sash, fanned out, tied with a cord: a few pale strips with ink edges."""
    o = []
    n = 5
    for i in range(n):
        a = (i - (n - 1) / 2.0) * 7.0
        o.append('<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (x, y, a))
        o.append('<path d="M-0.026,0 L0.026,0 L0.026,%.4f L-0.026,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (ln, ln, k.c(BAMBOO["base"] if i % 2 else BAMBOO["light"]), k.ink))
        o.append('<path d="M-0.008,0.03 L-0.008,%.4f" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (ln - 0.04, k.c(BAMBOO["dark"])))
        o.append('</g>')
    o.append('<path d="M%.4f,%.4f q%.4f,0.025 %.4f,0" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x - 0.07, y + 0.15, 0.07, 0.14, k.ink))
    o.append('<path d="M%.4f,%.4f q%.4f,0.025 %.4f,0" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x - 0.07, y + 0.15, 0.07, 0.14, k.c(col_cord)))
    k.ext.append((x - 0.12, y + ln, 0.03))
    k.ext.append((x + 0.12, y + ln, 0.03))
    return "".join(o)


def _cos_robe18(k, C, m):
    """a Warring States robe (shenyi-like): the left front panel crosses over to the right (a Y of two trimmed edges from the
    neck), a plain sash at the waist with a side knot and two hanging ends, the skirt of the robe to the calf; C["tally18"]:
    bamboo tally slips tucked in the sash; colors base / dark / trim / sash / sash_d / skirt (contrast skirt colour)."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * C.get("sash_y", 0.72)
    dark = k.c(col.get("dark", "#8a6a3a"))
    trim = k.c(col.get("trim", "#5a4228"))
    o = []
    # the under layer: neck to the middle chest; the over layer: from the right neck sloping down to the left waist
    under = [X(-0.17, 0.40), X(-0.07, 0.54), X(0.02, 0.64)]
    over = [X(0.17, 0.40), X(0.04, 0.56), X(-0.22, yw - 0.02)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.30"/>'
             % (over[0] + over[1] + over[2] + X(0.40, yw) + (k.c(P._shade(col["base"], 0.70)),)))
    o.append(_ln(under, k.ink, 0.058))
    o.append(_ln(under, trim, 0.034))
    o.append(_ln(over, k.ink, 0.062))
    o.append(_ln(over, trim, 0.038))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>' % (X(0.30, 0.62) + X(0.34, 0.80) + X(0.32, yw - 0.06) + (dark,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.5"/>' % (X(-0.34, 0.66) + X(-0.40, 0.82) + X(-0.36, yw - 0.06) + (dark,)))
    inside = "".join(o)
    # over: skirt + sash
    yt = yB - 0.16
    hem = yB + C.get("robe_len", 0.55)
    a = hw * 0.985
    b = hw + C.get("robe_flare", 0.10)
    skirt = col.get("skirt")
    if skirt:
        gs = C2._grad(k, "sk18", skirt, -b, b)
    else:
        gs = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "rb", X, yt, a, hem, b, gs, sw=0.026,
                    folds=((-0.12, yt + 0.12, -0.18, hem - 0.05), (0.08, yt + 0.16, 0.08, hem - 0.06), (-0.30, yt + 0.20, -0.40, hem - 0.06)),
                    fold_col=k.c(P._shade(skirt or col["base"], 0.70)))]
    fe = [X(-0.22, yt), X(-0.23, (yt + hem) / 2), X(-0.24, hem + 0.01)]
    ov.append(_ln(fe, k.ink, 0.046))
    ov.append(_ln(fe, trim, 0.026))
    if C.get("hem_band", True):
        hb = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-b + 0.03, hem - 0.040) + X(0.0, hem - 0.008) + X(b - 0.03, hem - 0.040))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" opacity="0.95"/>' % (hb, trim))
    sw = C.get("sash_w", 0.13)
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.ink, sw + 0.026))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.c(col.get("sash", "#2a2630")), sw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw * 0.9, yw - sw * 0.28) + X(0.0, yw + 0.04 - sw * 0.28) + X(hw * 0.9, yw - sw * 0.28)), k.c(col.get("sash_l", "#5a5462"))))
    # knot at the screen-right hip with two ends
    kx, ky = X(hw * 0.55, yw + 0.04)
    for (ex, ey) in ((0.07, 0.30), (-0.02, 0.36)):
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                  % (kx, ky, kx + ex - 0.035, ky + ey, kx + ex + 0.04, ky + ey - 0.02, k.c(col.get("sash", "#2a2630")), k.ink))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.055" ry="0.045" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, k.c(col.get("sash", "#2a2630")), k.ink))
    if C.get("tally18") and _POSE18["slips"] > 0.5:
        sx, sy = X(-hw * 0.50, yw - 0.12)
        ov.append(_slips(k, sx, sy, 0.50))
        # the sash passes over the slips' root
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (sx - 0.13, yw + 0.02, sx, yw + 0.07, sx + 0.13, yw + 0.02, k.c(col.get("sash", "#2a2630")), sw * 0.9))
    for p in (X(-b, hem), X(b, hem)):
        k.ext.append((p[0], p[1], 0.03))
    return inside, "", "".join(ov)


def _cos_armour18(k, C, m):
    """dark lacquered lamellar armour laced with red cord over a red robe.  C["armour18"] = dict(kind="general"|"soldier").
    Inside: lamellar plates over the whole torso, the red robe's crossed collar at the neck, red shoulder straps, a column of
    bronze studs down the front; over the hips: the red robe skirt under two lacquered tassets, a bronze-hooked belt, a front apron
    (general).  The soldier is simpler and shorter."""
    X = _X(m)
    col = C["colors"]
    spec = C.get("armour18", {})
    gen = spec.get("kind", "general") == "general"
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    yw = TT + h * C.get("sash_y", 0.72)
    robe = col.get("robe", "#b8202a")
    bz = k.c(BRONZE["base"])
    o = ['<rect x="-0.8" y="0.2" width="1.6" height="1.8" fill="%s" opacity="0.95"/>' % _lamellar(k, "ar", LACQ["deep"], LACQ["light"], CORD["base"])]
    # shoulder straps (red) and a vertical row of bronze studs / front lace
    for s in (-1, 1):
        st = [X(s * hw * 0.70, TT + 0.04), X(s * 0.20, TT + h * 0.34)]
        o.append(_ln(st, k.ink, 0.074))
        o.append(_ln(st, k.c(CORD["base"]), 0.046))
    if gen:
        for i in range(5):
            y = TT + h * (0.40 + 0.10 * i)
            c = X(0.0, y)
            o.append(_circ(c, 0.026, bz, k, 0.010))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.009" fill="%s"/>' % (c[0] - 0.007, c[1] - 0.007, k.c(BRONZE["light"])))
    # crossed collar of the red robe
    nk = [X(-0.24, 0.36), X(0.02, 0.66), X(0.26, 0.36)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (nk[0] + nk[1] + nk[2] + (k.c(robe), k.ink)))
    o.append(_ln([X(0.20, 0.38), X(-0.02, 0.60)], k.c(P._shade(robe, 0.65)), 0.020))
    o.append(_ln([X(-0.20, 0.38), X(0.08, 0.60)], k.c(BRONZE["base"]), 0.018))
    inside = "".join(o)
    yt = yB - 0.16
    hem = yB + C.get("robe_len", 0.50 if gen else 0.30)
    a = hw * 0.985
    b = hw + C.get("robe_flare", 0.14 if gen else 0.08)
    gr = C2._grad(k, "rb18", robe, -b, b)
    ov = [C2._skirt(k, "rb", X, yt, a, hem, b, gr, sw=0.026,
                    folds=((-0.10, yt + 0.20, -0.14, hem - 0.05), (0.12, yt + 0.20, 0.16, hem - 0.05)), fold_col=k.c(P._shade(robe, 0.65)))]
    if gen:
        fh = hem - 0.10
        sc = _lamellar(k, "sk", LACQ["deep"], LACQ["light"], CORD["base"], w=0.12, h=0.085, sw=0.008)
        for s in (-1, 1):
            pan = [X(s * 0.06, yt - 0.02), X(s * a * 1.01, yt - 0.02), X(s * (b + 0.03), fh - 0.02), X(s * (b * 0.55), fh + 0.04), X(s * 0.09, fh)]
            d = P._smooth_closed(pan)
            ov.append('<path d="%s" fill="%s"/>' % (d, k.c(LACQ["base"])))
            ov.append('<path d="%s" fill="%s"/>' % (d, sc))
            ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (d, k.ink))
            ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, k.c(CORD["base"])))
            k.ext.append((X(s * (b + 0.05), fh)[0], fh + 0.05, 0.03))
        ap = [X(-0.15, yw), X(0.15, yw), X(0.13, yw + 0.40), X(0.0, yw + 0.48), X(-0.13, yw + 0.40)]
        ov.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(ap), k.c(P._shade(robe, 0.80)), k.ink))
        cx_, cy_ = X(0.0, yw + 0.24)
        ov.append('<path d="M%.4f,%.4f l0.07,0.08 l-0.07,0.08 l-0.07,-0.08 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (cx_, cy_ - 0.08, bz, k.ink))
    else:
        # a plain apron of lacquered scales, shorter
        sc = _lamellar(k, "sk", LACQ["deep"], LACQ["light"], CORD["base"], w=0.12, h=0.085, sw=0.008)
        pan = [X(-a * 0.95, yt + 0.02), X(a * 0.95, yt + 0.02), X(b * 0.80, hem - 0.10), X(0.0, hem - 0.04), X(-b * 0.80, hem - 0.10)]
        d = P._smooth_closed(pan)
        ov.append('<path d="%s" fill="%s"/><path d="%s" fill="%s"/>' % (d, k.c(LACQ["base"]), d, sc))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.040" stroke-linejoin="round"/>' % (d, k.ink))
        ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(CORD["base"])))
    sw = C.get("sash_w", 0.15 if gen else 0.11)
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-hw, yw) + X(0.0, yw + 0.04) + X(hw, yw))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.ink, sw + 0.028))
    ov.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f"/>' % (band, k.c(col.get("belt", "#4a2228")), sw))
    if gen:
        for xx in (-0.60, -0.40, 0.40, 0.60):
            if abs(xx) > hw * 0.95:
                continue
            p = X(xx, yw + 0.04 * (1 - (xx / max(hw, 0.1)) ** 2))
            ov.append('<rect x="%.4f" y="%.4f" width="0.080" height="%.4f" rx="0.012" fill="%s" stroke="%s" stroke-width="0.010"/>' % (p[0] - 0.04, p[1] - sw * 0.34, sw * 0.68, bz, k.ink))
    bx, by = X(0.0, yw + 0.04)
    # bronze belt hook (daigou): a rounded plaque with a hook
    pw = sw * (1.6 if gen else 1.2)
    ov.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.02" fill="%s" stroke="%s" stroke-width="0.016"/>' % (bx - pw / 2, by - sw * 0.46, pw, sw * 0.92, bz, k.ink))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (bx - pw * 0.34, by - sw * 0.10, bx, by + sw * 0.38, bx + pw * 0.34, by - sw * 0.10, k.c(BRONZE["dark"])))
    ov.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.008"/>' % (bx, by - sw * 0.16, sw * 0.14, k.c(BRONZE["light"]), k.ink))
    for p in (X(-b, hem), X(b, hem)):
        k.ext.append((p[0], p[1], 0.03))
    return inside, "", "".join(ov)


COSTUMES18 = {"robe18": _cos_robe18, "armour18": _cos_armour18}


# ============================================================================= limbs: shoulder lamellar guards
def _guard18(k, S, E, C):
    """a lamellar shoulder guard: two rows of lacquered plates hanging along the upper arm, red cord, a bronze rim."""
    ang = math.degrees(math.atan2(E[1] - S[1], E[0] - S[0]))
    sz = C.get("guard18", 1.0)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (S[0], S[1], ang, sz)]
    for i, x in enumerate((0.18, 0.06)):
        d = "M%.4f,-0.15 Q%.4f,-0.19 %.4f,-0.14 L%.4f,0.14 Q%.4f,0.19 %.4f,0.15 Q%.4f,0.0 %.4f,-0.15 Z" % (x - 0.10, x + 0.02, x + 0.09, x + 0.09, x + 0.02, x - 0.10, x - 0.14, x - 0.10)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.c(LACQ["base"] if i == 0 else LACQ["dark"]), k.ink))
        o.append('<path d="M%.4f,-0.12 L%.4f,0.12" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x + 0.04, x + 0.04, k.c(CORD["base"])))
        o.append('<path d="M%.4f,-0.10 L%.4f,0.10" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.7"/>' % (x - 0.02, x - 0.02, k.c(LACQ["light"])))
    o.append('<path d="M-0.14,-0.14 Q-0.20,0 -0.14,0.14" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.14,-0.14 Q-0.20,0 -0.14,0.14" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(BRONZE["base"]))
    o.append('</g>')
    for (x, y) in ((-0.16, 0.0), (0.28, -0.2), (0.28, 0.2), (-0.10, -0.2), (-0.10, 0.2)):
        q = _rot(x * sz, y * sz, ang)
        k.ext.append((S[0] + q[0], S[1] + q[1], 0.03))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O18["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if tail is None and C is not None and C.get("_cast18") and C.get("guard18"):
        out += _guard18(k, S, E, C)
    return out


# ============================================================================= face: yan moustache, long white beard
def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "yan18":
        return _O18["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#1a161a")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    o = []
    for sd in (-1, 1):
        # a fat handlebar: from under the nose out over the cheek and curling up at the tip
        pts = [Q(sd * 0.02, -0.040), Q(sd * 0.14, -0.030), Q(sd * 0.28, 0.020), Q(sd * 0.40, 0.040), Q(sd * 0.50, 0.000), Q(sd * 0.56, -0.090), Q(sd * 0.55, -0.190)]
        d = _taper(pts, 0.150 * s, 0.020 * s)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round" opacity="0.85"/>'
                 % (Q(sd * 0.08, -0.060) + Q(sd * 0.30, -0.010) + Q(sd * 0.50, -0.040) + (k.c(C["colors"].get("moustache_l", "#5a5058")),)))
        k.ext.append(Q(sd * 0.56, -0.20) + (0.03,))
        k.ext.append(Q(sd * 0.40, 0.11) + (0.03,))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.011" stroke-linecap="round"/>' % (Q(0.0, -0.06) + Q(0.0, 0.0) + (k.ink,)))
    return "".join(o)


def _long_beard(k, C, L):
    """a long thin white beard hanging from the chin: a tapering fan of wisps ending in a point."""
    B = C["beard18"]
    mx, my = L["mx"], L["my"]
    ln = B.get("len", 0.55)
    col = k.c(B["color"])
    pts = [(mx - 0.22, my + 0.08), (mx - 0.20, my + 0.24), (mx - 0.10, my + 0.40 + ln * 0.5), (mx, my + 0.46 + ln), (mx + 0.10, my + 0.40 + ln * 0.5), (mx + 0.20, my + 0.24), (mx + 0.22, my + 0.08),
           (mx + 0.10, my + 0.14), (mx, my + 0.10), (mx - 0.10, my + 0.14)]
    d = P._smooth_closed(pts)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, col, k.ink)]
    ws = "".join("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f " % (mx + x * 0.7, my + 0.16, mx + x * 0.9, my + 0.34, mx + x * 0.25, my + 0.40 + ln * (0.85 - 0.5 * abs(x))) for x in (-0.14, -0.07, 0.0, 0.07, 0.14))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (ws, k.c(B.get("dark", "#aaa6b2"))))
    k.ext.append((mx, my + 0.47 + ln, 0.03))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O18["_face"](k, C, P_, white)
    if C is None or not C.get("_cast18"):
        return svg, L
    if C.get("beard18"):
        svg = _long_beard(k, C, L) + svg
    return svg, L


# ============================================================================= fire: the flame card (layered tongues)
_FLAME_TIPS = (
    # (left tongue, notch, main tip, notch, right tongue) per flicker drawing; x, y in flame units (height ~1.0 up = -y)
    ((-0.27, -0.72), (-0.12, -0.58), (0.01, -1.00), (0.10, -0.60), (0.24, -0.78)),
    ((-0.22, -0.84), (-0.10, -0.60), (0.06, -0.94), (0.12, -0.52), (0.28, -0.62)),
    ((-0.30, -0.62), (-0.14, -0.56), (-0.04, -1.06), (0.08, -0.66), (0.22, -0.86)),
)
_FLAME_SPARKS = (((0.30, -1.10, 0.030), (-0.22, -1.28, 0.022), (0.10, -1.42, 0.016)),
                 ((-0.28, -1.05, 0.028), (0.20, -1.24, 0.022), (-0.06, -1.40, 0.016)),
                 ((0.18, -1.12, 0.030), (-0.14, -1.20, 0.020), (0.30, -1.38, 0.014)))


def _flame_shape(f, lean, sx, sy, ox=0.0, oy=0.0):
    t = _FLAME_TIPS[f % 3]
    pts = [(-0.26, 0.02), (-0.31, -0.22), (-0.22, -0.46), t[0], t[1], t[2], t[3], t[4], (0.27, -0.42), (0.31, -0.18), (0.23, 0.02), (0.0, 0.08)]
    out = []
    for (x, y) in pts:
        out.append((ox + (x + lean * (-y)) * sx, oy + y * sy))
    return out


def flame_body(k, frame=0, lean=0.0, sparks=True, glow=True):
    """the tail / torch flame in its own frame: origin = the middle of its base, up = -y, height about 1.0 and 0.6 wide, layered
    tongues  core #fffeec -> mid #ffb238 -> outer #e8561c  (never pure yellow); lean shears the tip downwind (+x)."""
    f = int(frame) % 3
    o = []
    if glow:
        gid = "%s_fg" % k.uid
        if not any(gid in d for d in k.defs):
            k.defs.append('<radialGradient id="%s"><stop offset="0" stop-color="%s" stop-opacity="0.45"/><stop offset="0.5" stop-color="%s" stop-opacity="0.18"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (gid, k.c(FIRE["mid"]), k.c(FIRE["edge"]), k.c(FIRE["edge"])))
        o.append('<ellipse cx="%.4f" cy="-0.45" rx="0.95" ry="1.05" fill="url(#%s)"/>' % (0.2 * lean, gid))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(_flame_shape(f, lean, 1.0, 1.0)), k.c(FIRE["edge"]), k.c(FIRE["deep"])))
    o.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(_flame_shape(f, lean * 0.9, 0.74, 0.80, 0.0, -0.01)), k.c(FIRE["mid"])))
    o.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(_flame_shape(f, lean * 0.8, 0.42, 0.56, 0.0, -0.01)), k.c(FIRE["core"])))
    if sparks:
        for (x, y, r) in _FLAME_SPARKS[f]:
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x + lean * (-y) * 0.9, y, r, k.c(FIRE["mid"] if r > 0.018 else FIRE["edge"])))
    return "".join(o)


def flame_svg(uid="fl", frame=0, scale=1.0, lean=0.0, sparks=True, glow=True, ink=P.INK, tint=None):
    """standalone flame fragment (D units, origin at the base middle, scale = height in D).  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    body = flame_body(k, frame, lean, sparks, glow)
    s = '<defs>%s</defs>' % "".join(k.defs) if k.defs else ""
    s += '<g transform="scale(%.4f)">%s</g>' % (scale, body)
    return s, (-0.7 * scale, -1.5 * scale, (0.7 + abs(lean) * 1.5) * scale, 0.1 * scale)


# ============================================================================= props (own local frames, hand at the origin)
def _T(x, y, a=0.0, s=1.0):
    return '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (x, y, a, s)


def _jue_body(k, wine=1.0):
    """a bronze jue (three-legged wine cup, a long spout and a pointed tail, two posts, a loop handle), upright; the fist grips its
    legs at (0, 0); the rim is at y = -0.30."""
    g = _lin(k, "jb", BRONZE["light"], BRONZE["base"], BRONZE["dark"], -0.30, -0.3, 0.30, 0.0)
    o = []
    # legs
    for (x0, x1) in ((-0.10, -0.17), (0.0, 0.0), (0.12, 0.19)):
        o.append('<path d="M%.4f,-0.12 L%.4f,0.07 L%.4f,0.07 L%.4f,-0.12 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (x0 - 0.025, x1 - 0.020, x1 + 0.020, x0 + 0.025, k.c(BRONZE["dark"]), k.ink))
    # handle loop
    o.append('<path d="M0.15,-0.27 Q0.34,-0.30 0.31,-0.18 Q0.28,-0.10 0.15,-0.13" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.15,-0.27 Q0.34,-0.30 0.31,-0.18 Q0.28,-0.10 0.15,-0.13" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % k.c(BRONZE["base"]))
    # body: boat shaped, long spout at the left, short pointed tail at the right
    body = ("M-0.40,-0.41 Q-0.26,-0.31 -0.17,-0.26 Q-0.18,-0.14 -0.09,-0.09 Q0.0,-0.05 0.09,-0.09 Q0.17,-0.14 0.17,-0.26 Q0.26,-0.31 0.33,-0.40 Q0.14,-0.34 0.0,-0.34 Q-0.20,-0.34 -0.40,-0.41 Z")
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M-0.27,-0.30 Q-0.30,-0.22 -0.20,-0.16" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.5"/>')
    # patterned band
    o.append('<path d="M-0.15,-0.20 L0.15,-0.20" stroke="%s" stroke-width="0.030" opacity="0.9"/>' % k.c(BRONZE["deep"]))
    o.append('<path d="M-0.14,-0.20 l0.03,-0.02 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.02" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c(BRONZE["light"]))
    # wine surface and two posts
    if wine > 0.05:
        o.append('<ellipse cx="-0.01" cy="-0.355" rx="0.12" ry="0.026" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#c0662a"), k.ink))
        o.append('<path d="M-0.08,-0.362 Q-0.02,-0.372 0.04,-0.362" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % k.c("#f0b070"))
    for x in (-0.16, -0.06):
        o.append('<path d="M%.4f,-0.34 L%.4f,-0.44" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x, x, k.ink))
        o.append('<path d="M%.4f,-0.34 L%.4f,-0.44" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x, x, k.c(BRONZE["base"])))
        o.append('<circle cx="%.4f" cy="-0.455" r="0.026" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x, k.c(BRONZE["light"]), k.ink))
    return "".join(o)


def _spear_body(k):
    """a Warring States spear along +x: a bronze socket spike at the butt (-0.9), a wooden shaft, a leaf blade with a ridge at the
    head (2.18 .. 2.62), a red tassel under the head.  The hand is at 0."""
    o = []
    o.append('<path d="M-0.90,0 L2.22,0" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.90,0 L2.22,0" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % k.c(WOOD18["base"]))
    o.append('<path d="M-0.84,-0.010 L2.18,-0.010" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD18["light"]))
    o.append('<path d="M-0.96,-0.04 L-0.82,-0.034 L-0.82,0.034 L-0.96,0.04 L-1.02,0 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(BRONZE["base"]), k.ink))
    # tassel
    o.append('<path d="M2.12,0 Q2.04,0.10 2.00,0.24 M2.12,0 Q2.10,0.12 2.08,0.30 M2.12,0 Q2.16,0.10 2.18,0.26" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M2.12,0 Q2.04,0.10 2.00,0.24 M2.12,0 Q2.10,0.12 2.08,0.30 M2.12,0 Q2.16,0.10 2.18,0.26" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % k.c(CORD["base"]))
    # blade
    g = _lin(k, "sp", BRONZE["light"], BRONZE["base"], BRONZE["dark"], 2.2, -0.12, 2.6, 0.12)
    o.append('<path d="M2.18,-0.04 L2.24,-0.10 Q2.40,-0.14 2.66,0 Q2.40,0.14 2.24,0.10 L2.18,0.04 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink))
    o.append('<path d="M2.24,0 L2.60,0" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % k.c(BRONZE["dark"]))
    o.append('<path d="M2.30,-0.07 Q2.42,-0.10 2.54,-0.04" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.55"/>')
    return "".join(o)


def _mallet_body(k):
    """a short beating stick with a cloth-wrapped head along +x (0 .. 0.62)."""
    o = ['<path d="M-0.10,0 L0.52,0" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.10,0 L0.52,0" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.c(WOOD18["base"]),
         '<path d="M-0.06,-0.008 L0.48,-0.008" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD18["light"]),
         '<ellipse cx="0.56" cy="0" rx="0.085" ry="0.075" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#e8dcc0"), k.ink),
         '<path d="M0.52,-0.060 Q0.50,0 0.52,0.060" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % k.c("#9a8a68")]
    return "".join(o)


def _pot_body(k):
    """a round bronze vessel (a ding-like basin) with a rolled rim, two ring handles and a short foot, hanging by the ring at (0, 0):
    its rim is at y 0.10, its belly bottom at y 0.52."""
    g = _lin(k, "pt", BRONZE["light"], BRONZE["base"], BRONZE["dark"], -0.30, 0.1, 0.30, 0.5)
    o = []
    o.append('<path d="M-0.14,0.50 L-0.16,0.57 L-0.07,0.57 L-0.05,0.50 Z M0.05,0.50 L0.07,0.57 L0.16,0.57 L0.14,0.50 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(BRONZE["dark"]), k.ink))
    for sd in (-1, 1):
        o.append('<ellipse cx="%.4f" cy="0.17" rx="0.050" ry="0.060" fill="none" stroke="%s" stroke-width="0.046"/>' % (sd * 0.30, k.ink))
        o.append('<ellipse cx="%.4f" cy="0.17" rx="0.050" ry="0.060" fill="none" stroke="%s" stroke-width="0.024"/>' % (sd * 0.30, k.c(BRONZE["base"])))
    body = "M-0.28,0.12 Q-0.36,0.34 -0.18,0.50 Q0.0,0.58 0.18,0.50 Q0.36,0.34 0.28,0.12 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<ellipse cx="0" cy="0.12" rx="0.30" ry="0.055" fill="%s" stroke="%s" stroke-width="0.022"/>' % (k.c(BRONZE["dark"]), k.ink))
    o.append('<ellipse cx="0" cy="0.125" rx="0.25" ry="0.035" fill="%s"/>' % k.c(BRONZE["deep"]))
    o.append('<path d="M-0.30,0.28 Q0,0.34 0.30,0.28" fill="none" stroke="%s" stroke-width="0.014" opacity="0.9"/>' % k.c(BRONZE["deep"]))
    o.append('<path d="M-0.27,0.25 l0.03,-0.03 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.04 l0.03,0.04 l0.03,-0.03" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>' % k.c(BRONZE["light"]))
    o.append('<path d="M-0.22,0.22 Q-0.28,0.34 -0.17,0.44" fill="none" stroke="#ffffff" stroke-width="0.018" stroke-linecap="round" opacity="0.5"/>')
    # a cord from the hand to the rim
    o.append('<path d="M0,0 L-0.30,0.12 M0,0 L0.30,0.12" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0,0 L-0.30,0.12 M0,0 L0.30,0.12" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c(CORD["base"]))
    return "".join(o)


def _rings(k, cx, cy, t, lev=1.0):
    """sound rings: concentric arcs round the vessel (animate t 0..1 loop)."""
    o = []
    for i in range(3):
        f = (t + i / 3.0) % 1.0
        r = 0.34 + 0.60 * f
        op = (1.0 - f) * lev * _smooth(0.0, 0.12, f)
        a0, a1 = -50, 50
        for sd in (-1, 1):
            x0, y0 = cx + sd * r * math.cos(math.radians(a0)), cy + r * 0.9 * math.sin(math.radians(a0))
            x1, y1 = cx + sd * r * math.cos(math.radians(a1)), cy + r * 0.9 * math.sin(math.radians(a1))
            o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 %d %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round" opacity="%.3f"/>'
                     % (x0, y0, r, r * 0.9, 1 if sd > 0 else 0, x1, y1, k.c("#f6ecd2"), op * 0.9))
    return "".join(o)


def _torch_body(k, fire=1):
    """a torch along +x: a wooden stick (-0.25 .. 0.95), a head of reed bundled in cloth (0.78 .. 1.12) bound with red cord.  The
    flame is drawn by the caller (upright)."""
    o = ['<path d="M-0.25,0 L0.95,0" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.25,0 L0.95,0" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % k.c(WOOD18["base"]),
         '<path d="M-0.20,-0.010 L0.90,-0.010" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD18["light"])]
    hd = "M0.74,-0.065 Q0.80,-0.115 0.98,-0.125 Q1.16,-0.120 1.20,0 Q1.16,0.120 0.98,0.125 Q0.80,0.115 0.74,0.065 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (hd, k.c(STRAW["dark"]), k.ink))
    o.append('<path d="M0.84,-0.09 L1.12,-0.05 M0.84,-0.03 L1.16,0.0 M0.84,0.04 L1.14,0.05 M0.84,0.10 L1.08,0.09" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(STRAW["light"]))
    o.append('<path d="M0.80,-0.085 L0.80,0.085 M0.90,-0.115 L0.90,0.115" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(CORD["base"]))
    return "".join(o)


def _slips_body(k):
    """a bundle of bamboo tally slips (a rolled-out strip scroll) held at its bottom: 9 slips side by side, two cords, 0.62 tall."""
    o = []
    n = 9
    w = 0.040
    x0 = -w * n / 2
    for i in range(n):
        o.append('<rect x="%.4f" y="-0.62" width="%.4f" height="0.66" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x0 + i * w, w, k.c(BAMBOO["base"] if i % 2 else BAMBOO["light"]), k.ink))
        o.append('<path d="M%.4f,-0.58 L%.4f,-0.02" stroke="%s" stroke-width="0.006" opacity="0.7"/>' % (x0 + i * w + 0.012, x0 + i * w + 0.012, k.c(BAMBOO["dark"])))
    for y in (-0.50, -0.16):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030"/>' % (x0 - 0.010, y, x0 + n * w + 0.010, y, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016"/>' % (x0 - 0.010, y, x0 + n * w + 0.010, y, k.c("#7a3a22")))
    return "".join(o)


def _blade_body(k):
    """a short flat bronze blade (a leaf-shaped dagger) along +x: a tang with a red cord wrap at the root (0 .. 0.14), the blade
    to 0.62."""
    g = _lin(k, "bl", BRONZE["light"], BRONZE["base"], BRONZE["dark"], 0.1, -0.08, 0.6, 0.08)
    o = ['<path d="M-0.04,-0.020 L0.16,-0.020 L0.16,0.020 L-0.04,0.020 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(BRONZE["dark"]), k.ink),
         '<path d="M0.12,-0.075 L0.30,-0.090 Q0.50,-0.080 0.64,0 Q0.50,0.080 0.30,0.090 L0.12,0.075 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (g, k.ink),
         '<path d="M0.16,0 L0.60,0" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % k.c(BRONZE["dark"]),
         '<path d="M0.22,-0.056 Q0.40,-0.070 0.54,-0.030" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>']
    for x in (0.0, 0.045, 0.09):
        o.append('<path d="M%.4f,-0.034 L%.4f,0.034" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (x, x + 0.02, k.c(CORD["base"])))
    return "".join(o)


def _pick_body(k):
    """a digging pick along +x: a long wooden handle (-0.25 .. 1.0) and a heavy iron head across its end (a pointed, slightly curved
    pick): the working point at (0.98, 0.34)."""
    o = ['<path d="M-0.25,0 L1.0,0" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.25,0 L1.0,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c(WOOD18["base"]),
         '<path d="M-0.20,-0.012 L0.95,-0.012" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD18["light"])]
    g = _lin(k, "pk", "#bcb8c6", "#7c788a", "#44404e", 0.9, -0.3, 1.1, 0.3)
    head = "M0.88,-0.07 Q0.98,-0.20 1.06,-0.38 Q1.10,-0.20 1.10,-0.06 L1.10,0.06 Q1.10,0.22 1.06,0.38 Q0.98,0.20 0.88,0.07 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (head, g, k.ink))
    o.append('<path d="M0.94,-0.02 Q1.02,-0.16 1.05,-0.30" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.5"/>')
    o.append('<path d="M0.86,-0.05 L0.86,0.05" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.c("#7a3a22"))
    return "".join(o)


def _basket_body(k, load=1.0):
    """a woven bamboo basket carried by a rope handle: the hand holds the loop at (0, 0); the basket (0.50 wide) hangs from y 0.30 to 0.70,
    heaped with earth clods."""
    o = ['<path d="M-0.22,0.34 Q-0.20,0.0 0,0 Q0.20,0.0 0.22,0.34" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.22,0.34 Q-0.20,0.0 0,0 Q0.20,0.0 0.22,0.34" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(BAMBOO["dark"])]
    g = _lin(k, "bk", BAMBOO["light"], BAMBOO["base"], BAMBOO["dark"], -0.3, 0.3, 0.3, 0.7)
    if load > 0.05:
        o.append('<path d="M-0.26,0.38 Q-0.20,0.22 -0.08,0.26 Q0.0,0.15 0.10,0.24 Q0.22,0.22 0.26,0.38 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c("#8a6240"), k.ink))
        o.append('<circle cx="-0.10" cy="0.30" r="0.030" fill="%s"/><circle cx="0.08" cy="0.28" r="0.034" fill="%s"/><circle cx="0.17" cy="0.33" r="0.026" fill="%s"/>' % (k.c("#a87c54"), k.c("#a87c54"), k.c("#6a4a30")))
    body = "M-0.27,0.34 L-0.22,0.66 Q0,0.74 0.22,0.66 L0.27,0.34 Q0,0.40 -0.27,0.34 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M-0.26,0.44 Q0,0.50 0.26,0.44 M-0.25,0.52 Q0,0.58 0.25,0.52 M-0.24,0.60 Q0,0.66 0.24,0.60" fill="none" stroke="%s" stroke-width="0.010" opacity="0.9"/>' % k.c(BAMBOO["dark"]))
    o.append('<path d="M-0.15,0.37 L-0.12,0.68 M-0.04,0.39 L-0.03,0.70 M0.07,0.39 L0.06,0.70 M0.17,0.37 L0.14,0.67" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(BAMBOO["dark"]))
    o.append('<ellipse cx="0" cy="0.37" rx="0.27" ry="0.034" fill="none" stroke="%s" stroke-width="0.016"/>' % k.c(BAMBOO["dark"]))
    return "".join(o)


def _sash_body(k, t=0.0):
    """a general's investiture sash: a red silk band gathered in the fist at (0, 0) with two ends hanging down (gold stripes and tassels)
    and a bronze seal block on cords between them."""
    o = []
    w = 0.12
    for (x, ln, sw_) in ((-0.15, 0.64, 1), (0.15, 0.78, -1)):
        sway = 0.025 * math.sin(2 * math.pi * (t + (0.3 if sw_ > 0 else 0.0)))
        g = _lin(k, "sh%d" % (sw_ + 1), SILK["light"], SILK["base"], SILK["dark"], x - w, 0, x + w, 0)
        d = "M%.4f,0 L%.4f,0 Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,0 Z" % (x - w, x + w, x + w + sway, ln * 0.5, x + w * 0.9 + sway, ln, x - w * 0.9 + sway, ln, x - w + sway, ln * 0.5, x - w)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, g, k.ink))
        for yy in (0.10, ln - 0.16):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (x - w * 0.8 + sway * yy / ln, yy, x + w * 0.8 + sway * yy / ln, yy, k.c(GOLD["base"])))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                 % (x - 0.07 + sway, ln, x - 0.08 + sway, ln + 0.10, x + sway, ln, x + sway, ln + 0.12, x + 0.07 + sway, ln, x + 0.08 + sway, ln + 0.10, k.c(GOLD["base"])))
    # gathered knot in the fist
    o.append('<path d="M-0.28,-0.06 Q0,-0.14 0.28,-0.06 L0.26,0.07 Q0,0.12 -0.26,0.07 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c(SILK["base"]), k.ink))
    o.append('<path d="M-0.20,-0.04 Q0,-0.09 0.20,-0.04" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c(SILK["light"]))
    # seal block
    o.append('<path d="M-0.06,0.10 L-0.03,0.34 M0.06,0.10 L0.03,0.34" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(GOLD["dark"]))
    o.append('<rect x="-0.08" y="0.32" width="0.16" height="0.13" rx="0.014" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(BRONZE["base"]), k.ink))
    o.append('<path d="M-0.04,0.36 L0.04,0.36 M-0.04,0.40 L0.04,0.40" stroke="%s" stroke-width="0.010"/>' % k.c(BRONZE["deep"]))
    return "".join(o)


def _dragon_snip(k, gid):
    """a small gold dragon scroll for the silk cloth: an S-curve body with a head, in gold on crimson."""
    o = ['<path d="M-0.30,0.06 C-0.20,-0.14 -0.08,0.14 0.04,-0.02 C0.12,-0.12 0.22,-0.02 0.28,-0.10" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % k.c(GOLD["dark"]),
         '<path d="M-0.30,0.06 C-0.20,-0.14 -0.08,0.14 0.04,-0.02 C0.12,-0.12 0.22,-0.02 0.28,-0.10" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.c(GOLD["base"]),
         '<circle cx="0.30" cy="-0.11" r="0.045" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c(GOLD["base"]), k.c(GOLD["dark"])),
         '<path d="M-0.18,-0.04 q0.03,0.03 0.06,0 M-0.04,0.02 q0.03,0.03 0.06,0 M0.08,-0.06 q0.03,0.03 0.06,0" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % k.c(GOLD["deep"])]
    return "".join(o)


def _silk_body(k, t=0.0):
    """a length of crimson silk with a gold border and a gold dragon, pulled along +x from the fist at (0, 0): 1.0 long, 0.74 wide at
    the far end, a wavy free edge (animate t)."""
    g = _lin(k, "sk", SILK["light"], SILK["base"], SILK["dark"], 0.0, -0.4, 1.0, 0.4)
    w = lambda x: 0.03 * math.sin(2 * math.pi * (t + x * 1.6))     # noqa: E731
    top = [(0.0, -0.05), (0.30, -0.18 + w(0.3)), (0.62, -0.30 + w(0.62)), (1.00, -0.34 + w(1.0))]
    bot = [(1.04, 0.34 + w(0.9)), (0.68, 0.30 + w(0.68)), (0.32, 0.18 + w(0.32)), (0.0, 0.05)]
    d = P._smooth_closed(top + bot)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (d, g, k.ink),
         '<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round" opacity="0.95" transform="translate(0 0) scale(0.97)"/>' % (d, k.c(GOLD["base"]))]
    o.append('<g transform="translate(0.62 0.0) rotate(-6) scale(0.95)">%s</g>' % _dragon_snip(k, "ds"))
    o.append('<path d="M0.10,-0.02 Q0.30,0.06 0.46,0.10 M0.14,0.06 Q0.30,0.10 0.40,0.16" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c(SILK["dark"]))
    return "".join(o)


def _banner_body(k, side=1.0, t=0.0):
    """a plain cloth banner (no text): a pole (-0.5 .. 2.5), a bronze finial, a crossbar near the top and a rectangular cloth of
    undyed hemp hanging from it, its lower edge rippling (animate t); side = +1 hangs to +y of the pole in a screen-right wind."""
    o = ['<path d="M-0.55,0 L2.38,0" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % k.ink,
         '<path d="M-0.55,0 L2.38,0" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % k.c(WOOD18["base"]),
         '<path d="M-0.50,-0.010 L2.34,-0.010" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % k.c(WOOD18["light"])]
    # cloth hanging from a crossbar (the crossbar runs along +y, perpendicular to the pole) near the tip, flowing to the side
    x0, x1 = 1.12, 2.26
    wv = lambda x: 0.035 * math.sin(2 * math.pi * (t + x * 1.1))    # noqa: E731
    wd = 0.74
    pts = [(x0, 0.03), (x1, 0.03), (x1 + 0.03 + wv(1.0), wd * 0.5), (x1 + 0.02, wd), (x1 * 0.5 + x0 * 0.5, wd + 0.04 + wv(0.5)), (x0 - 0.02, wd + 0.01 + wv(0.2))]
    pts = [(x, y * side) for (x, y) in pts]
    g = _lin(k, "bn", "#fbf4e2", "#efe4cc", "#c4b494", x0, 0, x1, wd * side)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(pts), g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>'
             % (x0 + 0.10, 0.12 * side, x0 + 0.30, 0.34 * side, x0 + 0.16, 0.62 * side, x1 - 0.10, 0.12 * side, x1 - 0.30, 0.38 * side, x1 - 0.14, 0.66 * side, k.c("#b8a888")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x0 + 0.01, -0.02 * side, x1 + 0.01, -0.02 * side, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (x0 + 0.01, -0.02 * side, x1 + 0.01, -0.02 * side, k.c(WOOD18["base"])))
    o.append('<path d="M2.38,-0.04 L2.52,-0.050 L2.66,0 L2.52,0.050 L2.38,0.04 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(BRONZE["base"]), k.ink))
    return "".join(o)


NEW_PROPS18 = ("jue", "spear", "torch", "slips", "bronze_pot", "mallet", "sash", "silk", "blade", "pick", "basket", "banner")
NEW_TIP18 = {"jue": 0.34, "spear": 2.62, "torch": 1.12, "slips": 0.62, "bronze_pot": 0.52, "mallet": 0.64, "sash": 0.45, "silk": 1.0, "blade": 0.64,
             "pick": 1.10, "basket": 0.70, "banner": 2.6}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS18:
        return _O18["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    t = _POSE18["t"]
    ext = []
    if kind == "jue":
        tilt = _POSE18["cup"] * (1 if H[0] >= 0 else -1) * -1.0
        o = _T(H[0], H[1], tilt, sc) + _jue_body(k) + "</g>"
        for (x, y) in ((-0.40, -0.42), (0.33, -0.40), (0.0, 0.07), (0.31, -0.18)):
            ext.append(_rot(x * sc, y * sc, tilt))
        tip = _rot(0.0, -0.34 * sc, tilt)
        if abs(_POSE18["cup"]) > 25:
            sp = _POSE18["cup"] * (1 if H[0] >= 0 else -1) * -1.0
            sx, sy = _rot(-0.40 * sc, -0.41 * sc, tilt)
            for j in range(3):
                f = (t * 1.5 + j / 3.0) % 1.0
                o += '<path d="M%.4f,%.4f q-0.018,0.034 0,0.050 q0.018,-0.016 0,-0.050 Z" fill="%s" stroke="%s" stroke-width="0.007" opacity="%.3f"/>' % (H[0] + sx + 0.01 * j, H[1] + sy + 0.10 + 0.34 * f, k.c("#c0662a"), k.ink, 1.0 - f * f)
            ext.append((sx, sy + 0.5))
        an["cup_" + key] = (H[0] + tip[0], H[1] + tip[1])
        tp = (H[0] + tip[0], H[1] + tip[1])
    elif kind == "spear":
        o = _T(H[0], H[1], ang, sc) + _spear_body(k) + "</g>"
        for (x, y) in ((-1.02, 0.0), (2.66, 0.0), (2.0, 0.3), (2.4, -0.14), (2.4, 0.14)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(2.62 * sc, 0.0, ang)
        tp = (H[0] + tx, H[1] + ty)
        gx, gy = _rot(0.55 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        an["spear_tip_" + key] = tp
    elif kind == "torch":
        o = _T(H[0], H[1], ang, sc) + _torch_body(k) + "</g>"
        tx, ty = _rot(1.16 * sc, 0.0, ang)
        fx_, fy_ = H[0] + tx, H[1] + ty
        if _POSE18["fire"] >= 0:
            o += '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (fx_, fy_ + 0.04 * sc, 0.95 * sc, flame_body(k, _POSE18["fire"], 0.08 * math.sin(6.28 * t)))
            ext += [(fx_ - H[0] - 0.4 * sc, fy_ - H[1] - 1.5 * sc), (fx_ - H[0] + 0.4 * sc, fy_ - H[1] - 1.5 * sc)]
        for (x, y) in ((-0.30, 0.0), (1.22, -0.12), (1.22, 0.12)):
            ext.append(_rot(x * sc, y * sc, ang))
        tp = (fx_, fy_)
        an["torch_flame_" + key] = (fx_, fy_ - 0.5 * sc)
    elif kind == "slips":
        o = _T(H[0], H[1] - 0.0, ang + 90.0, sc) + _slips_body(k) + "</g>"
        for (x, y) in ((-0.20, -0.64), (0.20, -0.64), (-0.20, 0.04), (0.20, 0.04)):
            ext.append(_rot(x * sc, y * sc, ang + 90.0))
        tx, ty = _rot(0.0, -0.62 * sc, ang + 90.0)
        tp = (H[0] + tx, H[1] + ty)
    elif kind == "bronze_pot":
        o = _T(H[0], H[1], 0.0, sc) + _pot_body(k) + "</g>"
        for (x, y) in ((-0.38, 0.10), (0.38, 0.10), (-0.34, 0.58), (0.34, 0.58)):
            ext.append((x * sc, y * sc))
        if _POSE18["pot"] > 0.02:
            o += _rings(k, H[0], H[1] + 0.32 * sc, t, _POSE18["pot"])
            ext += [(-0.95, 0.1), (0.95, 0.1)]
        tp = (H[0], H[1] + 0.52 * sc)
        an["pot_top_" + key] = (H[0], H[1] + 0.12 * sc)
        an["pot_side_" + key] = (H[0] - side * 0.30 * sc, H[1] + 0.30 * sc)
    elif kind == "mallet":
        o = _T(H[0], H[1], ang, sc) + _mallet_body(k) + "</g>"
        for (x, y) in ((-0.12, 0.0), (0.66, -0.09), (0.66, 0.09)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(0.64 * sc, 0.0, ang)
        tp = (H[0] + tx, H[1] + ty)
        an["mallet_" + key] = tp
    elif kind == "sash":
        o = _T(H[0], H[1], 0.0, sc) + _sash_body(k, t) + "</g>"
        for (x, y) in ((-0.30, -0.08), (0.30, -0.08), (-0.25, 0.92), (0.25, 0.92)):
            ext.append((x * sc, y * sc))
        tp = (H[0], H[1] + 0.45 * sc)
        an["grip_far_" + key] = (H[0] - side * 0.26 * sc, H[1] + 0.02 * sc)
    elif kind == "silk":
        o = _T(H[0], H[1], ang, sc) + _silk_body(k, t) + "</g>"
        for (x, y) in ((0.0, 0.0), (1.06, -0.36), (1.06, 0.38)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(1.0 * sc, 0.0, ang)
        tp = (H[0] + tx, H[1] + ty)
    elif kind == "blade":
        o = _T(H[0], H[1], ang, sc) + _blade_body(k) + "</g>"
        for (x, y) in ((-0.06, 0.0), (0.66, 0.0), (0.3, -0.1), (0.3, 0.1)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(0.64 * sc, 0.0, ang)
        tp = (H[0] + tx, H[1] + ty)
        an["blade_" + key] = tp
    elif kind == "pick":
        o = _T(H[0], H[1], ang, sc) + _pick_body(k) + "</g>"
        for (x, y) in ((-0.30, 0.0), (1.1, -0.40), (1.1, 0.40)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(1.06 * sc, 0.38 * sc, ang)
        tp = (H[0] + tx, H[1] + ty)
        gx, gy = _rot(0.50 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
        an["pick_point_" + key] = tp
    elif kind == "basket":
        o = _T(H[0], H[1], 0.0, sc) + _basket_body(k) + "</g>"
        for (x, y) in ((-0.30, 0.2), (0.30, 0.2), (-0.26, 0.72), (0.26, 0.72)):
            ext.append((x * sc, y * sc))
        tp = (H[0], H[1] + 0.70 * sc)
        an["basket_bottom_" + key] = tp
    else:   # banner
        o = _T(H[0], H[1], ang, sc) + _banner_body(k, _POSE18["bside"], t) + "</g>"
        for (x, y) in ((-0.60, 0.0), (2.70, 0.0), (1.2, 0.8), (2.3, 0.8), (1.2, -0.8), (2.3, -0.8)):
            ext.append(_rot(x * sc, y * sc, ang))
        tx, ty = _rot(2.6 * sc, 0.0, ang)
        tp = (H[0] + tx, H[1] + ty)
    for (x, y) in ext:
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    return o, tp


# ============================================================================= pose keys
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE18["askew"] = _f(g("hat_askew"), 0.0, -60.0, 60.0)
    fr = g("fire_frame")
    _POSE18["fire"] = 0 if fr is None or isinstance(fr, (str, bool, list, dict)) else int(round(_f(fr, 0.0, -1.0, 2.0)))
    _POSE18["pot"] = _f(g("pot_ring"), 0.0, 0.0, 1.0)
    _POSE18["cup"] = _f(g("cup_tilt"), 0.0, -120.0, 120.0)
    _POSE18["slips"] = 0.0 if g("slips") in (0, False) and g("slips") is not None else 1.0
    bs = _num(g("banner_side"), 1.0)
    _POSE18["bside"] = -1.0 if bs < 0 else 1.0
    t = _num(g("t"), 0.0)
    _POSE18["t"] = t if math.isfinite(t) else 0.0
    return _O18["_norm"](C, pose)


# ============================================================================= cast
_FLAGS = dict(_cast18=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)
NEW_CAST18 = {
    # Tian Dan: a thin former market clerk. plain ochre hemp robe, crossed collar, dark sash with bamboo tally slips tucked in, a small
    # black scholar's cap on a topknot, a calm wry face.
    "tiandan": dict(
        _FLAGS, build="slim", seed=181.3,
        torso_w=0.64, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15, leg=1.30, stance=0.06, wide=0.26, limb_w=0.056,
        eye_y=0.035, brow="stroke", brow_th=0.050, mouth="smirk", moustache=False, smirk_side=1, cheeks="#e8a088",
        hat="newsboy", hat_style="scholar18", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(cap="#1c1822", cap_l="#4e4660", cap_d="#0c0a10", pin="#ece0bc"),
        hair=dict(color="#1c181c", front=0.08, grow=0.20, shine="#4a4a60"),
        costume="robe18", robe_len=0.62, robe_flare=0.10, sash_w=0.12, tally18=True,
        sleeve=dict(color="#c9964a", dark="#8c6228", cuff="#efe2c0", len=0.84, w=0.170),
        shorts=dict(color="#4a3e38", dark="#2e2622", cuff="#4a3e38", len=0.90, w=0.13),
        boots=dict(color="#2e2824", cuff="#2e2824", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#c9964a", dark="#8c6228", trim="#5a4026", sash="#2c2832", sash_l="#5a5462", pants="#4a3e38"),
    ),
    # the Yan general: stout, big belly, dark lacquered lamellar armour with red cords, bronze belt hook, plumed bronze helmet,
    # a huge upturned black moustache, ruddy cheeks
    "general": dict(
        _FLAGS, build="stout", seed=55.9,
        torso_w=1.48, torso_h=1.30, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.30, stance=0.07, wide=0.32, limb_w=0.070,
        eye_y=0.010, brow="stroke", brow_th=0.085, mouth="smirk", moustache=True, moustache_style="yan18", tache_scale=1.10,
        smirk_side=1, cheeks="#ec7a68", chins=True, guard18=1.45,
        hat="newsboy", hat_style="helm18", hat_tilt=-2.0, ear_pencil=False, helm18=dict(kind="general"),
        hat_colors=dict(light=BRONZE["light"], base=BRONZE["base"], dark=BRONZE["dark"], flap=LACQ["base"]),
        hair=dict(color="#1a161a", front=0.06, grow=0.20, shine="#4a4a5a"),
        costume="armour18", armour18=dict(kind="general"), robe_len=0.52, robe_flare=0.16, sash_w=0.17,
        sleeve=dict(color="#b8202a", dark="#7a1018", cuff="#cc9440", len=0.84, w=0.210),
        shorts=dict(color="#b8202a", dark="#7a1018", cuff="#b8202a", len=0.90, w=0.15),
        boots=dict(color="#241e24", cuff="#cc9440", h=0.16, toe=0.18),
        colors=dict(base="#2e2834", dark="#1a1620", light="#6a5a7c", robe="#b8202a", belt="#4a2228", pants="#b8202a", moustache="#1a161a", moustache_l="#5a5058"),
    ),
    # Yan soldiers in black and red: lacquered black lamellar over red, a spear.  a: tall, iron helmet with a red tuft; b: round,
    # bushy moustache, black cloth cap with a red band; c: short, ear-flap helmet with a red pompom
    "yan_soldier_a": dict(
        _FLAGS, build="slim", seed=18.4,
        torso_w=0.66, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.76, hip_x=0.15, leg=1.34, stance=0.06, wide=0.26, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.060, mouth="dash", moustache=False, smirk_side=-1, cheeks="#e8947c", guard18=0.9,
        hat="newsboy", hat_style="helm18", hat_tilt=-3.0, ear_pencil=False, helm18=dict(kind="iron", plume="tuft"),
        hat_colors=dict(light="#7a7488", base="#3e3a48", dark="#1e1a26"),
        hair=dict(color="#1a161a", front=0.06, grow=0.20),
        costume="armour18", armour18=dict(kind="soldier"), robe_len=0.34, robe_flare=0.08, sash_w=0.11,
        sleeve=dict(color="#a82028", dark="#6e1018", cuff="#2e2834", len=0.84, w=0.150),
        shorts=dict(color="#2e2834", dark="#1a1620", cuff="#2e2834", len=0.90, w=0.14),
        boots=dict(color="#241e24", cuff="#241e24", h=0.10, toe=0.15),
        colors=dict(base="#2e2834", dark="#1a1620", robe="#a82028", belt="#3a1a20", pants="#2e2834"),
    ),
    "yan_soldier_b": dict(
        _FLAGS, build="regular", seed=62.7,
        torso_w=0.96, torso_h=0.96, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.32, 0.47), arm=0.72, hip_x=0.16, leg=1.04, stance=0.06, wide=0.27, limb_w=0.064,
        eye_y=0.010, brow="stroke", brow_th=0.068, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.95, smirk_side=1, cheeks="#ee8472", guard18=1.0,
        hat="newsboy", hat_style="helm18", hat_tilt=5.0, ear_pencil=False, helm18=dict(kind="cloth"),
        hat_colors=dict(light="#585064", base="#26222e", dark="#12101a"),
        hair=dict(color="#2a1e1a", front=0.06, grow=0.20),
        costume="armour18", armour18=dict(kind="soldier"), robe_len=0.32, robe_flare=0.10, sash_w=0.12,
        sleeve=dict(color="#a82028", dark="#6e1018", cuff="#2e2834", len=0.84, w=0.165),
        shorts=dict(color="#2e2834", dark="#1a1620", cuff="#2e2834", len=0.90, w=0.15),
        boots=dict(color="#241e24", cuff="#241e24", h=0.10, toe=0.15),
        colors=dict(base="#2e2834", dark="#1a1620", robe="#a82028", belt="#3a1a20", pants="#2e2834", moustache="#2a1e1a"),
    ),
    "yan_soldier_c": dict(
        _FLAGS, build="slim", seed=27.5,
        torso_w=0.64, torso_h=0.86, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.24, 0.50), arm=0.70, hip_x=0.14, leg=1.08, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.050, brow="dome", brow_th=0.040, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a294", freckles=True, guard18=0.85,
        hat="newsboy", hat_style="helm18", hat_tilt=-4.0, ear_pencil=False, helm18=dict(kind="flap"),
        hat_colors=dict(light="#7a7488", base="#3e3a48", dark="#1e1a26", flap="#2e2834"),
        hair=dict(color="#3a2a22", front=0.10, grow=0.22),
        costume="armour18", armour18=dict(kind="soldier"), robe_len=0.30, robe_flare=0.08, sash_w=0.10,
        sleeve=dict(color="#a82028", dark="#6e1018", cuff="#2e2834", len=0.84, w=0.140),
        shorts=dict(color="#2e2834", dark="#1a1620", cuff="#2e2834", len=0.90, w=0.13),
        boots=dict(color="#241e24", cuff="#241e24", h=0.10, toe=0.13),
        colors=dict(base="#2e2834", dark="#1a1620", robe="#a82028", belt="#3a1a20", pants="#2e2834"),
    ),
    # townsfolk: an old man (white topknot and long white beard, grey-green hemp), a woman (indigo robe, hair bun with a bone pin),
    # a child (twin tufts, rust tunic)
    "old_man": dict(
        _FLAGS, build="regular", seed=43.1,
        torso_w=0.82, torso_h=0.92, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.30, 0.47), arm=0.70, hip_x=0.15, leg=0.92, stance=0.06, wide=0.24, limb_w=0.058,
        eye_y=0.020, brow="stroke", brow_th=0.056, mouth="dash", moustache=True, moustache_style="long9", tache_scale=0.70, tache_len=0.9, smirk_side=1,
        age_lines=True, cheeks="#e0a08a", beard18=dict(color="#f0eef2", dark="#aaa6b2", len=0.40),
        hat="newsboy", hat_style="topknot9", hat_tilt=3.0, ear_pencil=False,
        hat_colors=dict(band="#8a7a62", dark="#5a4e3c"), band_tails=True,
        hair=dict(color="#ece8f0", front=0.06, grow=0.18, shine="#ffffff"),
        costume="robe18", robe_len=0.55, robe_flare=0.10, sash_w=0.11, hem_band=True,
        sleeve=dict(color="#8a8c6e", dark="#5e6048", cuff="#b8b494", len=0.84, w=0.160),
        shorts=dict(color="#5a5448", dark="#3a362e", cuff="#5a5448", len=0.90, w=0.13),
        boots=dict(color="#3a322a", cuff="#3a322a", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#8a8c6e", dark="#5e6048", trim="#5a4a30", sash="#6a5a44", sash_l="#8a7a62", pants="#5a5448", moustache="#f0eef2", moustache_l="#aaa6b2"),
    ),
    "woman": dict(
        _FLAGS, build="slim", seed=71.6,
        torso_w=0.70, torso_h=0.96, profile=CE.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.72, hip_x=0.14, leg=1.12, stance=0.06, wide=0.24, limb_w=0.054,
        eye_y=0.040, brow="dome", brow_th=0.040, mouth="smile", moustache=False, smirk_side=1, cheeks="#f0a090", lashes=True,
        hat="newsboy", hat_style="bun18", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(pin="#efe2bc", cord="#c0262e"),
        hair=dict(color="#1c181c", front=0.08, grow=0.20, shine="#4a4a60"),
        costume="robe18", robe_len=0.92, robe_flare=0.18, sash_w=0.14, hem_band=True,
        sleeve=dict(color="#4e6e92", dark="#324e70", cuff="#ece0c0", len=0.84, w=0.160),
        shorts=dict(color="#324e70", dark="#243a56", cuff="#324e70", len=0.90, w=0.12),
        boots=dict(color="#3a322a", cuff="#3a322a", h=0.04, toe=0.12, soft=True),
        colors=dict(base="#4e6e92", dark="#324e70", trim="#ece0c0", sash="#d8c8a0", sash_l="#f0e4c4", pants="#324e70"),
    ),
    "child": dict(
        _FLAGS, build="child", seed=20.4,
        torso_w=0.52, torso_h=0.74, profile=CE.PROFILE_CHILD, shift_pow=1.0,
        shoulder=(0.20, 0.48), arm=CE.CHILD_ARM, hip_x=0.15, leg=0.78, stance=0.07, wide=0.22, limb_w=0.057,
        eye_y=0.060, brow="dome", brow_th=0.034, mouth="smile", moustache=False, smirk_side=1, cheeks="#f6a8a0",
        hat="newsboy", hat_style="tufts18", hat_tilt=0.0, ear_pencil=False,
        hat_colors=dict(cord="#c0262e"),
        hair=dict(color="#1c181c", front=0.07, grow=0.18, shine="#4a4a60"),
        costume="robe18", robe_len=0.24, robe_flare=0.08, sash_w=0.10, hem_band=False,
        sleeve=dict(color="#b8603a", dark="#8a4224", cuff="#ecd8b0", len=0.84, w=0.140),
        shorts=dict(color="#5a4a40", dark="#3a2e28", cuff="#5a4a40", len=0.90, w=0.12),
        boots=dict(color="#3a322a", cuff="#3a322a", h=0.04, toe=0.12, soft=True),
        colors=dict(base="#b8603a", dark="#8a4224", trim="#ecd8b0", sash="#c0262e", sash_l="#e8505a", pants="#5a4a40"),
    ),
    # the envoy: a plain undyed hemp robe, a plain brown cloth cap, a thin moustache; humble, bowing
    "envoy": dict(
        _FLAGS, build="regular", seed=34.9,
        torso_w=0.78, torso_h=0.98, profile=CE.PROFILE_REGULAR, shift_pow=1.0,
        shoulder=(0.29, 0.48), arm=0.74, hip_x=0.15, leg=1.16, stance=0.06, wide=0.25, limb_w=0.058,
        eye_y=0.025, brow="stroke", brow_th=0.052, mouth="dash", moustache=True, moustache_style="long9", tache_scale=0.55, tache_len=0.7, smirk_side=1, cheeks="#e4a088",
        hat="newsboy", hat_style="scholar18", hat_tilt=2.0, ear_pencil=False,
        hat_colors=dict(cap="#6a5642", cap_l="#947c62", cap_d="#3e3226", pin="#ece0bc"),
        hair=dict(color="#2a2024", front=0.08, grow=0.20, shine="#5a5a60"),
        costume="robe18", robe_len=0.72, robe_flare=0.10, sash_w=0.12, hem_band=True,
        sleeve=dict(color="#dcd2b6", dark="#b0a47e", cuff="#f2eace", len=0.84, w=0.190),
        shorts=dict(color="#6a5e4c", dark="#443c30", cuff="#6a5e4c", len=0.90, w=0.13),
        boots=dict(color="#3a322a", cuff="#3a322a", h=0.05, toe=0.14, soft=True),
        colors=dict(base="#dcd2b6", dark="#b0a47e", trim="#8a7c5a", sash="#8a7a5a", sash_l="#a89870", pants="#6a5e4c", moustache="#2a2024"),
    ),
    # a Qi soldier for crowds: the slim soldier body, plain iron cap, every colour near-black (draw it with qi_pose(): tint + ink)
    "qi_soldier": dict(
        _FLAGS, build="slim", seed=18.4,
        torso_w=0.66, torso_h=0.98, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.76, hip_x=0.15, leg=1.34, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.030, brow="stroke", brow_th=0.060, mouth="dash", moustache=False, smirk_side=-1,
        hat="newsboy", hat_style="helm18", hat_tilt=-3.0, ear_pencil=False, helm18=dict(kind="cloth", band="#1e1a26"),     # dark cloth cap: no red band, no tuft
        hat_colors=dict(light="#3a3644", base="#2a2632", dark="#1a1620"),
        hair=dict(color="#1a161a", front=0.06, grow=0.20),
        costume="robe18", robe_len=0.34, robe_flare=0.08, sash_w=0.11, hem_band=False,
        sleeve=dict(color="#2a2632", dark="#1a1620", cuff="#2a2632", len=0.84, w=0.140),
        shorts=dict(color="#2a2632", dark="#1a1620", cuff="#2a2632", len=0.90, w=0.13),
        boots=dict(color="#1a1620", cuff="#1a1620", h=0.08, toe=0.15),
        colors=dict(base="#2a2632", dark="#1a1620", trim="#1a1620", sash="#1a1620", sash_l="#3a3644", pants="#2a2632"),
    ),
}

CANVAS18 = {
    "tiandan": (-2.1875, -6.1875, 2.1875, 0.1250),          # the raised torch reaches 5.8 D above the soles
    "general": (-1.8750, -5.0000, 1.8750, 0.1250),
    "yan_soldier_a": (-1.5000, -5.2500, 1.5000, 0.1250),   # spear upright
    "yan_soldier_b": (-1.5000, -4.9375, 1.5000, 0.1875),
    "yan_soldier_c": (-1.5000, -4.8750, 1.5000, 0.1250),
    "old_man": (-1.6875, -4.1250, 1.6875, 0.1250),
    "woman": (-1.6875, -4.3750, 1.6875, 0.2500),
    "child": (-1.5000, -3.7500, 1.5000, 0.1250),
    "envoy": (-1.6250, -5.0625, 1.6250, 0.1875),            # banner upright
    "qi_soldier": (-3.5000, -4.6250, 3.5000, 0.1250),       # spear held out sideways
}
OX_CANVAS = (-3.3125, -4.3125, 3.1875, 0.3125)              # ox_figure() in D, feet-relative (x 0 = middle of the body, facing +x; mirrored: use the same width)



# ============================================================================= the ox (not a puppet: a standalone drawing)
# Local frame: D units, y down, the hooves on y = 0, x = 0 about the middle of the body, the ox faces +x (facing = -1 mirrors it).
# Side view: shoulder hump at x 0.65, back y -2.0 (hump -2.4), horn tips about y -3.0.  Three-quarter view: the ox comes toward
# the viewer's right: head in front and low, body behind.
OX_COL = dict(plain=dict(light="#b88050", base="#94603a", dark="#5e3a22", deep="#3a2214"),
              hoof="#2a2024", horn=dict(light="#fbf0d0", base="#eadcb4", dark="#a89870"), muzzle=dict(light="#f6e4c4", base="#e6c8a0", dark="#b8946a"),
              patch="#2e2428")
OX_HIP = {"fn": (0.80, -1.08), "ff": (0.52, -1.08), "hn": (-1.08, -1.12), "hf": (-0.82, -1.12)}


def _leg_path(hip, foot, bend, up=0.56, lo=0.60):
    dx, dy = foot[0] - hip[0], foot[1] - hip[1]
    d = math.hypot(dx, dy)
    L = up + lo
    d = min(d, L * 0.995)
    a = (up * up - lo * lo + d * d) / (2 * d) if d > 1e-6 else 0.0
    hh = math.sqrt(max(0.0, up * up - a * a))
    ux, uy = (dx / (math.hypot(dx, dy) or 1.0), dy / (math.hypot(dx, dy) or 1.0))
    px, py = hip[0] + ux * a, hip[1] + uy * a
    # bend > 0: knee towards +x
    nx, ny = -uy, ux
    if nx * bend < 0:
        nx, ny = -nx, -ny
    knee = (px + nx * hh, py + ny * hh)
    return knee


def _ox_leg(k, col, hip, foot, bend, far=False, w=(0.36, 0.26), hoof_turn=0.0):
    c = col["dark"] if far else col["base"]
    c = P._shade(c, 0.82) if far else c
    knee = _leg_path(hip, foot, bend)
    ink = k.ink
    o = []
    # ink first, then the fills, so the joints merge
    for (a, b, wd) in ((hip, knee, w[0]), (knee, foot, w[1])):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (a[0], a[1], b[0], b[1], ink, wd + 0.065))
    hf = 0.20
    ang = math.atan2(foot[1] - knee[1], foot[0] - knee[0])
    hx, hy = foot[0] + math.cos(ang) * 0.02, foot[1] + math.sin(ang) * 0.02
    hoof = '<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>'
    o.append('<g transform="translate(%.4f %.4f) rotate(%.2f)">%s</g>' % (foot[0], foot[1], math.degrees(ang) - 90 + hoof_turn,
             hoof % (-0.17, -0.10, 0.17, -0.10, 0.19, 0.14, -0.19, 0.14, k.c(OX_COL["hoof"]), ink) +
             '<path d="M0,-0.08 L0,0.14" stroke="%s" stroke-width="0.020"/>' % k.c(P._shade(OX_COL["hoof"], 2.2))))
    for (a, b, wd) in ((hip, knee, w[0]), (knee, foot, w[1])):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (a[0], a[1], b[0], b[1], k.c(c), wd))
    # darker sock on the lower leg
    sk = (knee[0] * 0.30 + foot[0] * 0.70, knee[1] * 0.30 + foot[1] * 0.70)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round" opacity="0.75"/>' % (sk[0], sk[1], foot[0], foot[1] - 0.06, k.c(OX_COL["patch"]), w[1] * 0.96))
    return "".join(o), knee


def _ox_gait(gait, phase, view="side"):
    """foot targets (hip -> foot), body bob (y), pitch (deg), tail angle, head angle, for each gait.  phase 0..1 loops."""
    p = phase % 1.0
    tw = 2 * math.pi
    H = OX_HIP
    feet, bob, pitch, tail, head = {}, 0.0, 0.0, 15.0, 8.0
    if gait == "gallop":
        offs = {"fn": 0.00, "ff": 0.07, "hn": 0.46, "hf": 0.53}
        for key, off in offs.items():
            q = tw * (p + off)
            hx, hy = H[key]
            front = key[0] == "f"
            x = hx + (0.55 if front else 0.66) * math.sin(q) + (0.10 if front else -0.05)
            lift = 0.56 * max(0.0, math.cos(q)) ** 0.8
            feet[key] = (x, -lift)
        bob = -0.14 * (0.5 + 0.5 * math.cos(2 * tw * p - 0.6))
        pitch = -5.0 * math.sin(tw * p + 0.5)
        tail, head = 105.0 + 10 * math.sin(tw * p), -4.0 + 6 * math.sin(tw * p)
    elif gait == "walk":
        offs = {"fn": 0.0, "hf": 0.25, "ff": 0.5, "hn": 0.75}
        for key, off in offs.items():
            q = tw * (p + off)
            hx, hy = H[key]
            x = hx + 0.34 * math.sin(q)
            lift = 0.26 * max(0.0, math.cos(q))
            feet[key] = (x, -lift)
        bob = -0.04 * abs(math.sin(tw * p * 2))
        pitch = 0.0
        tail, head = 18.0 + 6 * math.sin(tw * p), 10.0 + 5 * math.sin(tw * p * 2)
    elif gait == "startled":
        feet = {"fn": (H["fn"][0] + 0.38, 0.0), "ff": (H["ff"][0] + 0.20, 0.0), "hn": (H["hn"][0] - 0.22, 0.0), "hf": (H["hf"][0] - 0.05, 0.0)}
        bob, pitch, tail, head = -0.06, -4.0, 140.0, -22.0
    else:   # stand
        feet = {key: (H[key][0] + (0.02 if key[0] == "f" else -0.02), 0.0) for key in H}
        bob = 0.0
        tail, head = 12.0 + 2 * math.sin(tw * p), 10.0
    return feet, bob, pitch, tail, head


def _tpath(k, pts, w0, w1, fill, sw=0.026):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_taper(pts, w0, w1), fill, k.ink, sw)


def _horn(k, base, ang, sc, far=False, blade=True, ln=1.0):
    """a curved horn (cream, a dark tip) from base, drawn in the head frame; returns (svg, tip, tip_dir_deg)."""
    col = OX_COL["horn"]
    sgn = 1.0
    pts = [(base[0], base[1]), (base[0] - 0.08 * sc, base[1] - 0.28 * sc), (base[0] - 0.02 * sc, base[1] - 0.52 * sc * ln), (base[0] + 0.14 * sc, base[1] - 0.70 * sc * ln),
           (base[0] + 0.36 * sc, base[1] - 0.80 * sc * ln)]
    c = col["dark"] if far else col["base"]
    o = [_tpath(k, pts, 0.17 * sc, 0.05 * sc, k.c(c))]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (pts[0][0] - 0.03, pts[0][1] - 0.04, pts[1][0] - 0.07, pts[2][1], pts[3][0] - 0.02, pts[3][1] - 0.04, k.c(col["light"])))
    tip = pts[-1]
    d = math.degrees(math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0]))
    return "".join(o), tip, d


def _blade_on_horn(k, tip, d, sc):
    """a short flat bronze DAGGER blade lashed to the horn tip, pointing on along the horn (fix 15: about 52 % of the old 0.95 long leaf):
    bronze #8a6a3a body, a darker #5a4424 edge and a thin highlight, three red cord wraps at the root.  sc is the old scale (1.7 / 1.5)."""
    f = sc / 1.7
    s = _T(tip[0], tip[1], d + 24.0, f)        # swung forward off the horn line so horn + blade never read as one long spike
    s += '<path d="M-0.06,-0.095 L0.02,-0.115 L0.26,-0.105 L0.50,0 L0.26,0.105 L0.02,0.115 L-0.06,0.095 Z" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (k.c("#8a6a3a"), k.ink)
    s += '<path d="M0.02,-0.115 L0.26,-0.105 L0.50,0 L0.26,0.105 L0.02,0.115" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round" opacity="0.85"/>' % k.c("#5a4424")
    s += '<path d="M0.02,0 L0.44,0" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c("#5a4424")
    s += '<path d="M0.06,-0.055 L0.30,-0.050 L0.42,-0.012" fill="none" stroke="#d8c088" stroke-width="0.016" stroke-linecap="round" opacity="0.9"/>'
    for x in (-0.07, 0.0, 0.07):
        s += '<path d="M%.4f,-0.105 L%.4f,0.105" stroke="%s" stroke-width="0.048" stroke-linecap="round"/>' % (x, x + 0.03, k.ink)
        s += '<path d="M%.4f,-0.105 L%.4f,0.105" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x, x + 0.03, k.c(CORD["base"]))
    s += "</g>"
    return s


def _dragon(k, sx=1.0):
    """the dragon painted on the silk coat (round 3: a SERPENTINE body, not a face).  Local frame of the flank: x -1.4 .. 0.55, y -2.2 .. -1.25.
    A long gold S-curve body (thick in the middle, thin at the tail and at the neck) with a dark-gold belly line and scale ticks, a fin crest
    of small triangles along the back, a flame tail tuft, and a SMALL profile head (a long snout, two swept-back horns, a dot eye, no open mouth,
    about 15 % of the coat height) at mid-flank, x about -0.15; three cream cloud swirls around it."""
    o = []
    for (x, y, r, c) in ((-0.98, -1.33, 0.13, "#f4f0e6"), (0.18, -1.32, 0.12, "#f4f0e6"), (-0.50, -2.13, 0.10, "#f4f0e6")):
        d = 'M%.4f,%.4f a%.4f,%.4f 0 1 1 %.4f,%.4f a%.4f,%.4f 0 1 1 %.4f,%.4f' % (x - r, y, r, r, r * 1.2, r * 1.0, r * 0.7, r * 0.7, -r * 0.5, -r * 0.5)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (d, k.c(c)))
    spine = [(-1.34, -1.44), (-1.10, -1.84), (-0.80, -1.88), (-0.58, -1.56), (-0.36, -1.44), (-0.22, -1.66)]
    sm = _sample(spine, 24)
    n = len(sm)
    wp = [0.020 + 0.085 * math.sin(math.pi * min(1.0, i / (n - 1.0) * 1.08)) ** 0.8 for i in range(n)]
    L_, R_ = [], []
    nrm = []
    for i in range(n):
        a, b = sm[max(i - 1, 0)], sm[min(i + 1, n - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        Ln = math.hypot(dx, dy) or 1.0
        nrm.append((dy / Ln, -dx / Ln, dx / Ln, dy / Ln))
    # fin crest on the outer (upper) side
    for i in range(3, n - 3, 2):
        nx, ny, tx, ty = nrm[i]
        if ny > 0:
            nx, ny = -nx, -ny
        w = wp[i]
        px, py = sm[i]
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (
            px - tx * 0.07 + nx * w * 0.6, py - ty * 0.07 + ny * w * 0.6, px + nx * (w + 0.13) + tx * 0.04, py + ny * (w + 0.13) + ty * 0.04,
            px + tx * 0.07 + nx * w * 0.6, py + ty * 0.07 + ny * w * 0.6, k.c(GOLD["dark"]), k.ink))
    for i in range(n):
        nx, ny, tx, ty = nrm[i]
        L_.append((sm[i][0] + nx * wp[i], sm[i][1] + ny * wp[i]))
        R_.append((sm[i][0] - nx * wp[i], sm[i][1] - ny * wp[i]))
    pts = L_ + R_[::-1]
    body = "M" + " L".join("%.4f,%.4f" % p for p in pts) + " Z"
    # tail tuft
    o.append('<path d="M-1.33,-1.45 Q-1.50,-1.36 -1.56,-1.50 Q-1.44,-1.50 -1.50,-1.64 Q-1.32,-1.60 -1.26,-1.48 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(GOLD["dark"]), k.ink))
    g = _lin(k, "dgb", GOLD["light"], GOLD["base"], GOLD["dark"], -1.2, -2.0, 0.0, -1.4)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.036" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>' % (" L".join("%.4f,%.4f" % (x, y) for (x, y) in R_[3:-3:1]), k.c(GOLD["dark"])))
    for i in range(4, n - 4, 3):
        nx, ny, tx, ty = nrm[i]
        o.append('<path d="M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (
            sm[i][0] - nx * 0.04, sm[i][1] - ny * 0.04, tx * 0.03, ty * 0.03, -nx * 0.08 * 0, 0.0, k.c(GOLD["deep"])))
    # small profile head at the neck end, facing +x: about 0.20 tall, 0.40 long with the snout
    hx, hy = sm[-1]
    o.append('<g transform="translate(%.4f %.4f) rotate(-14)">' % (hx, hy))
    o.append('<path d="M0.0,-0.07 L0.10,-0.10 Q0.30,-0.10 0.46,-0.05 Q0.50,-0.02 0.46,0.01 L0.12,0.07 Q0.02,0.08 -0.04,0.05 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(GOLD["base"]), k.ink))
    o.append('<path d="M0.10,-0.10 Q0.20,-0.22 0.04,-0.30 M0.02,-0.08 Q0.06,-0.26 -0.12,-0.30" fill="none" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.10,-0.10 Q0.20,-0.22 0.04,-0.30 M0.02,-0.08 Q0.06,-0.26 -0.12,-0.30" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % k.c("#f4f0e6"))
    o.append('<path d="M0.44,0.0 Q0.58,0.08 0.52,0.18 M0.40,0.03 Q0.50,0.14 0.40,0.22" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % k.ink)
    o.append('<circle cx="0.16" cy="-0.03" r="0.020" fill="%s"/>' % k.ink)
    o.append('</g>')
    return "".join(o)


def _sample(pts, n=20):
    out = []
    m = len(pts) - 1
    for i in range(n + 1):
        u = i / float(n) * m
        j = min(int(u), m - 1)
        t = u - j
        p0, p1, p2, p3 = pts[max(j - 1, 0)], pts[j], pts[j + 1], pts[min(j + 2, m)]
        out.append(tuple(0.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t * t + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t ** 3) for c in (0, 1)))
    return out


def _ox_body_pts():
    return [(-1.58, -1.45), (-1.42, -1.86), (-0.95, -2.02), (-0.30, -2.00), (0.28, -2.22), (0.62, -2.60), (0.98, -2.52), (1.28, -2.02), (1.44, -1.60), (1.38, -1.22),
            (1.05, -0.92), (0.40, -0.84), (-0.40, -0.86), (-1.10, -0.92), (-1.50, -1.10)]


def _ox_side(k, state, gait, phase, flame, blades, reed, startled_eyes, coat, t):
    col = OX_COL["plain"]
    feet, bob, pitch, tail_a, head_a = _ox_gait(gait, phase)
    dragon = state == "dragon"
    o = []
    # --- far legs
    legs_far, legs_near = [], []
    pv = (0.0, -1.5)

    def body_pt(p):
        x, y = _rot(p[0] - pv[0], p[1] - pv[1], pitch)
        return (pv[0] + x, pv[1] + y + bob)
    for key in ("hf", "ff"):
        hip = body_pt(OX_HIP[key])
        s, kn = _ox_leg(k, col, hip, feet[key], 0.6 if key[0] == "f" else -0.6, far=True)
        legs_far.append(s)
    for key in ("hn", "fn"):
        hip = body_pt(OX_HIP[key])
        s, kn = _ox_leg(k, col, hip, feet[key], 0.6 if key[0] == "f" else -0.6)
        legs_near.append(s)
    o += legs_far
    o += legs_near
    # --- tail (behind the body)
    tail = _ox_tail(k, col, tail_a, reed, flame, body_pt((-1.50, -1.72)), t)
    o.append(tail[0])
    # --- body group
    b = ['<g transform="translate(0 %.4f) rotate(%.3f %.1f %.1f)">' % (bob, pitch, pv[0], pv[1])]
    bp = _ox_body_pts()
    g = _lin(k, "obg", col["light"], col["base"], col["dark"], -1.5, -2.3, 1.3, -0.8)
    d = P._smooth_closed(bp)
    # far horn + ear are part of the head below; body first
    b.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (d, g, k.ink))
    # belly shade and a lighter belly, hump highlight
    b.append('<path d="M-1.4,-1.0 Q-0.4,-0.78 1.1,-0.98" fill="none" stroke="%s" stroke-width="0.10" stroke-linecap="round" opacity="0.28"/>' % k.c(col["deep"]))
    b.append('<path d="M0.30,-2.30 Q0.62,-2.42 0.92,-2.32" fill="none" stroke="#ffffff" stroke-width="0.026" stroke-linecap="round" opacity="0.35"/>')
    # dewlap
    b.append('<path d="M1.30,-1.25 Q1.12,-1.00 0.98,-1.02 Q1.12,-1.20 1.10,-1.40 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c(col["dark"]), k.ink))
    if not dragon:
        b.append('<path d="M-1.0,-1.95 Q-0.85,-1.50 -1.20,-1.20 Q-1.48,-1.45 -1.40,-1.80 Z" fill="%s" opacity="0.30"/>' % k.c(OX_COL["patch"]))
        b.append('<path d="M-0.2,-1.95 q0.10,0.12 0.0,0.30 M0.05,-2.0 q0.10,0.12 0.0,0.34" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.5"/>' % k.c(col["deep"]))
    else:
        b.append(_ox_coat(k, coat))
    b.append('</g>')
    o.append("".join(b))
    # --- head (rotates about the neck)
    nk = body_pt((1.26, -1.86))
    o.append(_ox_head_side(k, col, nk, head_a + pitch * 0.5, blades, startled_eyes, dragon))
    if tail[1] is not None:
        o.append(tail[1])    # the flame is on top of everything
    return "".join(o), dict(tail_tip=tail[2], head=nk, feet=feet)


def _ox_coat(k, cover=1.0):
    """the crimson silk coat draped over the back: from the neck to the rump, hanging to the belly line, gold borders, a scalloped hem with
    tassels, the dragon on the flank.  cover < 1 draws it still being pulled on (shifted up and back)."""
    sh = (1.0 - cover)
    bp = _ox_body_pts()
    top = [(-1.62, -1.50), (-1.46, -1.90), (-0.95, -2.06), (-0.30, -2.04), (0.28, -2.26), (0.62, -2.64), (0.98, -2.56), (1.22, -2.12), (1.30, -1.84)]
    hem = []
    n = 8
    for i in range(n + 1):
        u = i / float(n)
        x = 1.20 - 2.82 * u
        y = -1.14 + 0.05 * math.sin(math.pi * u) + (0.0)
        hem.append((x, y))
    # scalloped hem: points down on every third step
    sc = []
    for i in range(10):
        x0 = 1.26 - 2.90 * i / 10.0
        x1 = 1.26 - 2.90 * (i + 1) / 10.0
        sc.append((x0, -1.14))
        sc.append(((x0 + x1) / 2, -0.98))
    sc.append((-1.64, -1.14))
    d = "M%s L%s Z" % (" L".join("%.4f,%.4f" % p for p in top), " L".join("%.4f,%.4f" % p for p in sc))
    g = _lin(k, "cog", SILK["light"], SILK["base"], SILK["dark"], -1.6, -2.3, 1.3, -1.0)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f -0.4 -1.8)">' % (-0.9 * sh, -0.55 * sh, -10 * sh)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (d, g, k.ink))
    # gold borders: along the back, along the hem
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y + 0.07) for (x, y) in top[1:-1]), k.c(GOLD["base"])))
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (" L".join("%.4f,%.4f" % (x, y + 0.10) for (x, y) in top[1:-1]), k.c(GOLD["deep"])))
    o.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y - 0.06 if y < -1.1 else y - 0.04) for (x, y) in sc[:-1]), k.c(GOLD["base"])))
    for i in range(10):
        x = (sc[2 * i][0] + sc[2 * i + 1][0]) / 2 - 0.0
        xm = sc[2 * i + 1][0]
        o.append('<path d="M%.4f,-0.98 L%.4f,-0.84" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (xm, xm, k.ink))
        o.append('<path d="M%.4f,-0.98 L%.4f,-0.84" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (xm, xm, k.c(GOLD["base"])))
    o.append(_dragon(k))
    o.append('</g>')
    return "".join(o)


def _ox_tail(k, col, a, reed, flame, root, t):
    """the tail from root, angle a degrees from straight down towards the back (180 = straight up), 0.62 long, with a tuft, or a reed bundle
    tied to it (0.95 long, tied with red cord) with the flame at the free end.  Returns (svg under the body, flame svg or None, tip)."""
    if reed and flame >= 0:
        a = max(a, 48.0)
    ra = math.radians(a)
    L = 0.70
    dx, dy = -math.sin(ra), math.cos(ra)       # direction of the tail (backwards = -x)
    tip = (root[0] + dx * L, root[1] + dy * L)
    o = []
    cp = (root[0] + dx * L * 0.5 + 0.10 * dy, root[1] + dy * L * 0.5 - 0.10 * dx)
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.100" stroke-linecap="round"/>' % (root[0], root[1], cp[0], cp[1], tip[0], tip[1], k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>' % (root[0], root[1], cp[0], cp[1], tip[0], tip[1], k.c(col["dark"])))
    fl = None
    end = tip
    if reed:
        # the reed bundle lies along the tail beyond the tuft: fat, straw coloured, a few stems fanning out at the free end, cord ties
        R = 0.95
        bx, by = tip
        ex, ey = bx + dx * R, by + dy * R
        nx, ny = -dy, dx
        pts = [(bx - nx * 0.07, by - ny * 0.07), (bx + dx * R * 0.5 - nx * 0.11, by + dy * R * 0.5 - ny * 0.11), (ex - nx * 0.15 + dx * 0.04, ey - ny * 0.15 + dy * 0.04),
               (ex + dx * 0.12, ey + dy * 0.12), (ex + nx * 0.15 + dx * 0.04, ey + ny * 0.15 + dy * 0.04), (bx + dx * R * 0.5 + nx * 0.11, by + dy * R * 0.5 + ny * 0.11), (bx + nx * 0.07, by + ny * 0.07)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(STRAW["base"]), k.ink))
        for u in (-0.9, -0.45, 0.0, 0.45, 0.9):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.9"/>' % (bx + nx * 0.07 * u + dx * 0.05, by + ny * 0.07 * u + dy * 0.05, ex + nx * 0.13 * u + dx * 0.08, ey + ny * 0.13 * u + dy * 0.08, k.c(STRAW["dark"] if u < 0.3 else STRAW["light"])))
        for q in (0.12, 0.45, 0.78):
            cx_, cy_ = bx + dx * R * q, by + dy * R * q
            w = 0.09 + 0.05 * q
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (cx_ - nx * w, cy_ - ny * w, cx_ + nx * w, cy_ + ny * w, k.ink))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (cx_ - nx * w, cy_ - ny * w, cx_ + nx * w, cy_ + ny * w, k.c(CORD["base"])))
        end = (ex + dx * 0.10, ey + dy * 0.10)
        if flame >= 0:
            lean = math.tan(math.radians(min(70.0, max(0.0, (a - 20.0) * 0.65)))) * -1.0
            rot = -min(70.0, max(0.0, (a - 20.0) * 0.6))
            fl = '<g transform="translate(%.4f %.4f) rotate(%.2f) scale(1.0)">%s</g>' % (end[0], end[1] + 0.03, rot, flame_body(k, flame, -0.12 + 0.0 * lean))
            # a charred end
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.10" ry="0.07" fill="%s" stroke="%s" stroke-width="0.016"/>' % (end[0] - dx * 0.04, end[1] - dy * 0.04, k.c("#4a2a1e"), k.ink))
    else:
        tf = [(tip[0] - 0.06, tip[1]), (tip[0] + dx * 0.10 - 0.10, tip[1] + dy * 0.10 + 0.14), (tip[0] + dx * 0.20, tip[1] + dy * 0.20 + 0.28), (tip[0] + dx * 0.10 + 0.10, tip[1] + dy * 0.10 + 0.14), (tip[0] + 0.06, tip[1])]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(tf), k.c(OX_COL["patch"]), k.ink))
        end = tf[2]
    return "".join(o), fl, end


def _ox_head_side(k, col, nk, ang, blades, wide, dragon):
    """the head, a chunky wedge with a pale broad muzzle, big friendly eye, a leaf ear, two horns (the far one behind); the neck pivot at nk."""
    mz = OX_COL["muzzle"]
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(1.16)">' % (nk[0], nk[1], ang)]
    # far horn and far ear first
    hs, htip, hd = _horn(k, (0.20, -0.36), 0, 1.0, far=True)
    o.append('<g transform="translate(-0.05 0.02)">' + hs + (_blade_on_horn(k, htip, hd, 1.7) if blades else "") + '</g>')
    o.append('<path d="M0.06,-0.30 Q-0.22,-0.42 -0.34,-0.28 Q-0.20,-0.20 0.04,-0.16 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round" transform="translate(0.04 0.0)"/>' % (k.c(col["dark"]), k.ink))
    skull = [(-0.20, -0.30), (0.10, -0.46), (0.50, -0.36), (0.80, -0.14), (0.98, 0.08), (0.98, 0.30), (0.80, 0.44), (0.40, 0.46), (0.05, 0.42), (-0.22, 0.28), (-0.30, 0.0)]
    g = _lin(k, "ohg", col["light"], col["base"], col["dark"], -0.3, -0.4, 1.0, 0.45)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (P._smooth_closed(skull), g, k.ink))
    if not dragon:
        o.append('<path d="M0.28,-0.40 Q0.40,-0.30 0.36,-0.05 Q0.20,-0.10 0.12,-0.30 Z" fill="%s" opacity="0.55"/>' % k.c(OX_COL["patch"]))
    # forehead tuft
    o.append('<path d="M0.12,-0.44 q0.04,-0.10 0.12,-0.04 q0.04,-0.08 0.12,-0.0" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c(col["deep"]), k.ink))
    # muzzle
    gm = _lin(k, "omz", mz["light"], mz["base"], mz["dark"], 0.5, 0.0, 1.0, 0.5)
    o.append('<path d="M0.60,0.02 Q0.84,-0.14 0.99,0.08 Q1.03,0.30 0.84,0.46 Q0.60,0.50 0.52,0.30 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (gm, k.ink))
    o.append('<ellipse cx="0.90" cy="0.12" rx="0.045" ry="0.060" fill="%s" stroke="%s" stroke-width="0.012" transform="rotate(-20 0.90 0.12)"/>' % (k.c("#6a3a3a"), k.ink))
    o.append('<path d="M0.62,0.36 Q0.80,0.44 0.96,0.34" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.62,0.28 q0.04,-0.03 0.06,0.0" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % k.ink)
    # eye
    ey = (0.40, -0.06)
    if wide:
        o.append('<circle cx="%.4f" cy="%.4f" r="0.115" fill="#ffffff" stroke="%s" stroke-width="0.024"/><circle cx="%.4f" cy="%.4f" r="0.042" fill="%s"/>' % (ey[0], ey[1], k.ink, ey[0] + 0.02, ey[1], k.ink))
        o.append('<path d="M0.26,-0.24 Q0.38,-0.32 0.52,-0.22" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.ink)
    else:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.085" ry="0.095" fill="#ffffff" stroke="%s" stroke-width="0.022"/><circle cx="%.4f" cy="%.4f" r="0.058" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.020" fill="#ffffff"/>'
                 % (ey[0], ey[1], k.ink, ey[0] + 0.020, ey[1] + 0.006, k.ink, ey[0] + 0.004, ey[1] - 0.024))
        o.append('<path d="M0.30,-0.17 Q0.40,-0.22 0.50,-0.15" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % k.ink)
    # near ear (pointing back and up) and near horn
    o.append('<path d="M0.04,-0.20 Q-0.28,-0.34 -0.42,-0.12 Q-0.24,-0.08 0.02,-0.04 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(col["base"] if dragon else OX_COL["patch"]), k.ink))
    o.append('<path d="M-0.04,-0.17 Q-0.22,-0.22 -0.32,-0.12 Q-0.20,-0.10 -0.02,-0.08 Z" fill="%s" opacity="0.8"/>' % k.c("#d49a8a"))
    hs, htip, hd = _horn(k, (0.20, -0.38), 0, 1.0)
    o.append(hs)
    if blades:
        o.append(_blade_on_horn(k, htip, hd, 1.7))
    o.append('</g>')
    return "".join(o)



def _ox_head_34(k, col, c, ang, blades, wide, dragon, sc=1.0):
    """the head seen three-quarter (turned toward screen-right): a broad skull, a cream muzzle with two nostrils, two eyes, two horns
    curving out and up, two ears, a forehead tuft.  centre c, scale sc."""
    mz = OX_COL["muzzle"]
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f)">' % (c[0], c[1], ang, sc)]
    # far side first: horn, ear
    hs, htip, hd = _horn(k, (0.0, 0.0), 0, 0.9, far=True)
    o.append('<g transform="translate(0.50 -0.40) rotate(18)">' + hs + (_blade_on_horn(k, htip, hd, 1.5) if blades else "") + '</g>')
    o.append('<path d="M0.46,-0.18 Q0.80,-0.34 0.96,-0.14 Q0.74,-0.02 0.50,0.0 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (k.c(col["dark"]), k.ink))
    g = _lin(k, "o3g", col["light"], col["base"], col["dark"], -0.6, -0.5, 0.7, 0.6)
    skull = [(-0.50, -0.30), (-0.20, -0.52), (0.28, -0.54), (0.58, -0.32), (0.64, 0.05), (0.52, 0.40), (0.15, 0.62), (-0.25, 0.56), (-0.52, 0.28), (-0.58, -0.02)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.036" stroke-linejoin="round"/>' % (P._smooth_closed(skull), g, k.ink))
    if not dragon:
        o.append('<path d="M0.02,-0.52 Q0.14,-0.40 0.10,-0.10 Q-0.04,-0.20 -0.08,-0.50 Z" fill="%s" opacity="0.55"/>' % k.c(OX_COL["patch"]))
    o.append('<path d="M-0.04,-0.55 q0.04,-0.10 0.12,-0.05 q0.04,-0.09 0.12,-0.01 q0.06,-0.06 0.12,0.02" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c(col["deep"]), k.ink))
    gm = _lin(k, "o3m", mz["light"], mz["base"], mz["dark"], -0.3, 0.2, 0.5, 0.7)
    o.append('<path d="M-0.32,0.22 Q-0.34,0.0 0.0,0.0 Q0.40,0.0 0.44,0.24 Q0.46,0.58 0.08,0.66 Q-0.34,0.62 -0.32,0.22 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (gm, k.ink))
    for x in (-0.14, 0.22):
        o.append('<ellipse cx="%.4f" cy="0.26" rx="0.048" ry="0.062" fill="%s" stroke="%s" stroke-width="0.012" transform="rotate(%.1f %.4f 0.26)"/>' % (x, k.c("#6a3a3a"), k.ink, 18 if x > 0 else -18, x))
    o.append('<path d="M-0.18,0.50 Q0.04,0.58 0.30,0.48" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.ink)
    for (x, y, rx, ry, big) in ((-0.20, -0.10, 0.095, 0.105, 1), (0.34, -0.12, 0.085, 0.095, 0)):
        if wide:
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" stroke="%s" stroke-width="0.024"/><circle cx="%.4f" cy="%.4f" r="0.044" fill="%s"/>' % (x, y, rx + 0.025, k.ink, x + 0.02, y, k.ink))
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (x - 0.12, y - 0.16, x, y - 0.26, x + 0.12, y - 0.15, k.ink))
        else:
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#ffffff" stroke="%s" stroke-width="0.022"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.020" fill="#ffffff"/>'
                     % (x, y, rx, ry, k.ink, x + 0.015, y + 0.008, 0.060 if big else 0.052, k.ink, x - 0.004, y - 0.026))
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (x - 0.11, y - 0.14 + (0.03 if not big else 0), x, y - 0.22, x + 0.11, y - 0.13, k.ink))
    o.append('<path d="M-0.40,-0.10 Q-0.78,-0.22 -0.92,0.0 Q-0.70,0.14 -0.44,0.12 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (k.c(col["base"] if dragon else OX_COL["patch"]), k.ink))
    o.append('<path d="M-0.48,-0.04 Q-0.70,-0.10 -0.80,0.0 Q-0.66,0.06 -0.48,0.06 Z" fill="%s" opacity="0.8"/>' % k.c("#d49a8a"))
    hs, htip, hd = _horn(k, (0.0, 0.0), 0, 1.0)
    o.append('<g transform="translate(-0.40 -0.42) rotate(-20)">' + hs + (_blade_on_horn(k, htip, hd, 1.7) if blades else "") + '</g>')
    o.append('</g>')
    return "".join(o)


def _ox_34(k, state, gait, phase, flame, blades, reed, wide, coat, t):
    col = OX_COL["plain"]
    dragon = state == "dragon"
    p = phase % 1.0
    tw = 2 * math.pi
    H = {"hf": (-0.60, -1.15), "hn": (-1.10, -1.10), "ff": (1.05, -1.20), "fn": (0.55, -1.15)}
    feet = {}
    bob, tail_a, head_a, tilt = 0.0, 14.0, 6.0, 0.0
    if gait == "gallop":
        offs = {"hn": 0.50, "hf": 0.56, "fn": 0.0, "ff": 0.06}
        for key, off in offs.items():
            q = tw * (p + off)
            front = key[0] == "f"
            lift = 0.60 * max(0.0, math.cos(q)) if True else 0
            reach = 0.38 * math.sin(q) * (1.0 if front else 0.6)
            feet[key] = (H[key][0] + reach * 0.7, -lift)
        bob = -0.16 * (0.5 + 0.5 * math.cos(2 * tw * p - 0.5))
        tail_a, head_a, tilt = 100.0 + 10 * math.sin(tw * p), -2.0 + 5 * math.sin(tw * p), 2.5 * math.sin(tw * p)
    elif gait == "walk":
        offs = {"fn": 0.0, "hf": 0.25, "ff": 0.5, "hn": 0.75}
        for key, off in offs.items():
            q = tw * (p + off)
            feet[key] = (H[key][0] + 0.18 * math.sin(q), -0.22 * max(0.0, math.cos(q)))
        bob = -0.04 * abs(math.sin(2 * tw * p))
        tail_a, head_a = 18.0 + 6 * math.sin(tw * p), 8.0 + 4 * math.sin(2 * tw * p)
    elif gait == "startled":
        feet = {"fn": (H["fn"][0] + 0.10, 0.0), "ff": (H["ff"][0] + 0.12, 0.0), "hn": (H["hn"][0] - 0.12, 0.0), "hf": (H["hf"][0] - 0.05, 0.0)}
        bob, tail_a, head_a = -0.05, 140.0, -14.0
    else:
        feet = {key: (H[key][0], 0.0) for key in H}
    o = []
    for key in ("hf", "ff"):
        s, kn = _ox_leg(k, col, (H[key][0], H[key][1] + bob), feet[key], 0.2, far=True, w=(0.38, 0.28))
        o.append(s)
    for key, bd in (("hn", -0.2), ("fn", 0.2)):
        s, kn = _ox_leg(k, col, (H[key][0], H[key][1] + bob), feet[key], bd, w=(0.40, 0.28))
        o.append(s)
    tail = _ox_tail(k, col, tail_a, reed, flame, (-1.62, -1.62 + bob), t)
    o.append(tail[0])
    bp = [(-1.80, -1.35), (-1.66, -1.95), (-1.05, -2.18), (-0.35, -2.22), (0.28, -2.40), (0.78, -2.34), (1.12, -1.98), (1.20, -1.40), (0.62, -0.96), (-0.40, -0.88), (-1.30, -0.92), (-1.78, -1.05)]
    g = _lin(k, "o3b", col["light"], col["base"], col["dark"], -1.8, -2.3, 1.2, -0.9)
    b = ['<g transform="translate(0 %.4f) rotate(%.2f -0.3 -1.5)">' % (bob, tilt)]
    b.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (P._smooth_closed(bp), g, k.ink))
    b.append('<path d="M-1.6,-1.0 Q-0.5,-0.80 0.9,-1.0" fill="none" stroke="%s" stroke-width="0.10" stroke-linecap="round" opacity="0.28"/>' % k.c(col["deep"]))
    b.append('<path d="M0.35,-2.30 Q0.65,-2.40 0.95,-2.28" fill="none" stroke="#ffffff" stroke-width="0.026" stroke-linecap="round" opacity="0.35"/>')
    if dragon:
        sh = 1.0 - coat
        top = [(-1.84, -1.45), (-1.70, -1.98), (-1.05, -2.22), (-0.35, -2.26), (0.28, -2.44), (0.78, -2.38), (1.16, -2.0), (1.26, -1.46)]
        sc_ = []
        for i2 in range(8):
            x0 = 1.26 - 3.10 * i2 / 8.0
            x1 = 1.26 - 3.10 * (i2 + 1) / 8.0
            sc_.append((x0, -1.12 + 0.03 * math.sin(i2)))
            sc_.append(((x0 + x1) / 2, -0.96))
        sc_.append((-1.84, -1.12))
        d = "M%s L%s Z" % (" L".join("%.4f,%.4f" % q for q in top), " L".join("%.4f,%.4f" % q for q in sc_))
        gc = _lin(k, "o3c", SILK["light"], SILK["base"], SILK["dark"], -1.8, -2.3, 1.2, -1.0)
        b.append('<g transform="translate(%.4f %.4f) rotate(%.2f -0.4 -1.8)">' % (-0.9 * sh, -0.55 * sh, -10 * sh))
        b.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (d, gc, k.ink))
        b.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y + 0.08) for (x, y) in top[1:-1]), k.c(GOLD["base"])))
        b.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y - 0.05) for (x, y) in sc_[:-1]), k.c(GOLD["base"])))
        b.append('<g transform="translate(-0.15 0) scale(0.86 1.0)">%s</g>' % _dragon(k))
        b.append('</g>')
    b.append('</g>')
    o.append("".join(b))
    # head, in front and low
    hc = (1.55, -1.70 + bob)
    # a crimson neck cloth under the head for the dragon ox
    if dragon:
        o.append('<path d="M0.62,-2.1 Q1.30,-2.20 1.72,-1.50 L1.60,-1.0 Q1.0,-1.1 0.62,-1.4 Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round" opacity="0.0"/>' % (k.c(SILK["base"]), k.ink))
    o.append(_ox_head_34(k, col, hc, head_a + tilt, blades, wide, dragon, 1.05))
    if tail[1] is not None:
        o.append(tail[1])
    return "".join(o), dict(tail_tip=tail[2], head=hc, feet=feet)


def _ox_front(k, state, gait, phase, flame, blades, reed, wide, coat, t):
    """FRONT three-quarter: the ox comes at the camera, a little toward screen-right.  Big low head in front (two eyes, both horns, both
    ears), a broad chest / neck, the hump behind it, the body running away to the left and getting smaller, the near front legs big, the far
    ones and the hind legs behind them.  The silk coat (dragon) shows its front edge over the chest and the dragon on the visible left flank.
    The tail with the reed and the flame stands up behind the back."""
    col = OX_COL["plain"]
    dragon = state == "dragon"
    p = phase % 1.0
    tw = 2 * math.pi
    H = {"hf": (-1.20, -1.22), "hn": (-0.62, -1.18), "ff": (-0.02, -1.16), "fn": (0.84, -1.12)}
    feet = {key: (H[key][0], 0.0) for key in H}
    bob, tail_a, head_a, roll, reach = 0.0, 150.0, 4.0, 0.0, {}
    hdy = 0.0
    if gait == "gallop":
        offs = {"hn": 0.50, "hf": 0.56, "fn": 0.0, "ff": 0.06}
        for key, off in offs.items():
            q = tw * (p + off)
            front = key[0] == "f"
            lift = (0.46 if front else 0.40) * max(0.0, math.cos(q)) ** 0.9
            feet[key] = (H[key][0] + (0.10 if front else 0.05) * math.sin(q), -lift)
            reach[key] = max(0.0, math.cos(q))
        bob = -0.15 * (0.5 + 0.5 * math.cos(2 * tw * p - 0.5))
        tail_a, head_a, roll = 120.0 + 12 * math.sin(tw * p), 6.0 + 5 * math.sin(2 * tw * p + 0.4), 2.2 * math.sin(tw * p)
        hdy = 0.07 * math.sin(2 * tw * p + 0.4)
    elif gait == "walk":
        offs = {"fn": 0.0, "hf": 0.25, "ff": 0.5, "hn": 0.75}
        for key, off in offs.items():
            q = tw * (p + off)
            feet[key] = (H[key][0] + 0.05 * math.sin(q), -0.24 * max(0.0, math.cos(q)))
            reach[key] = max(0.0, math.cos(q)) * 0.5
        bob = -0.04 * abs(math.sin(2 * tw * p))
        tail_a, head_a, roll = 20.0 + 6 * math.sin(tw * p), 4.0 + 3 * math.sin(2 * tw * p), 1.2 * math.sin(tw * p)
    elif gait == "startled":
        feet = {"fn": (H["fn"][0] + 0.22, 0.0), "ff": (H["ff"][0] - 0.06, 0.0), "hn": (H["hn"][0] - 0.06, 0.0), "hf": (H["hf"][0] - 0.16, 0.0)}
        bob, tail_a, head_a = -0.07, 128.0, -12.0
        hdy = -0.10
    else:
        tail_a = 14.0 + 2 * math.sin(tw * p)
    o = []
    for key, sc_, far in (("hf", 0.82, True), ("hn", 0.86, False), ("ff", 0.94, True), ("fn", 1.0, False)):
        hip = (H[key][0], H[key][1] + bob)
        w = (0.40 * sc_, 0.29 * sc_)
        sv, kn = _ox_leg(k, col, hip, feet[key], 0.04 if key[0] == "f" else -0.04, far=far, w=w)
        # a hoof lifted towards the camera shows as a bigger hoof: nothing to do, the drawing already foreshortens by y
        o.append(sv)
    tail = _ox_tail(k, col, tail_a, reed, flame, (-1.52, -2.02 + bob), t)
    o.append(tail[0])
    bp = [(-1.78, -1.55), (-1.70, -2.12), (-1.15, -2.36), (-0.55, -2.58), (0.05, -2.74), (0.65, -2.62), (1.12, -2.20), (1.28, -1.55), (1.14, -1.08), (0.55, -0.92),
          (-0.20, -0.90), (-1.10, -0.96), (-1.62, -1.10)]
    g = _lin(k, "ofb", col["light"], col["base"], col["dark"], -1.8, -2.5, 1.2, -1.0)
    b = ['<g transform="translate(0 %.4f) rotate(%.2f 0 -1.5)">' % (bob, roll)]
    b.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (P._smooth_closed(bp), g, k.ink))
    b.append('<path d="M-1.5,-1.04 Q-0.5,-0.82 1.0,-1.0" fill="none" stroke="%s" stroke-width="0.10" stroke-linecap="round" opacity="0.28"/>' % k.c(col["deep"]))
    b.append('<path d="M-0.20,-2.62 Q0.10,-2.70 0.45,-2.58" fill="none" stroke="#ffffff" stroke-width="0.026" stroke-linecap="round" opacity="0.35"/>')
    if not dragon:
        b.append('<path d="M-1.2,-2.2 Q-0.9,-1.7 -1.35,-1.35 Q-1.65,-1.6 -1.55,-2.0 Z" fill="%s" opacity="0.30"/>' % k.c(OX_COL["patch"]))
    else:
        sh = 1.0 - coat
        top = [(-1.84, -1.52), (-1.76, -2.16), (-1.15, -2.40), (-0.55, -2.62), (0.05, -2.78), (0.65, -2.66), (1.14, -2.22), (1.32, -1.56)]
        sc2 = []
        n = 8
        for i2 in range(n):
            x0 = 1.34 - 3.20 * i2 / float(n)
            x1 = 1.34 - 3.20 * (i2 + 1) / float(n)
            sc2.append((x0, -1.14))
            sc2.append(((x0 + x1) / 2, -0.98))
        sc2.append((-1.86, -1.14))
        d = "M%s L%s Z" % (" L".join("%.4f,%.4f" % q for q in top), " L".join("%.4f,%.4f" % q for q in sc2))
        gc = _lin(k, "ofc", SILK["light"], SILK["base"], SILK["dark"], -1.8, -2.5, 1.2, -1.0)
        b.append('<g transform="translate(%.4f %.4f) rotate(%.2f -0.4 -1.8)">' % (-0.9 * sh, -0.55 * sh, -10 * sh))
        b.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (d, gc, k.ink))
        b.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y + 0.08) for (x, y) in top[1:-1]), k.c(GOLD["base"])))
        b.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (" L".join("%.4f,%.4f" % (x, y - 0.05) for (x, y) in sc2[:-1]), k.c(GOLD["base"])))
        for i2 in range(n):
            xm = sc2[2 * i2 + 1][0]
            b.append('<path d="M%.4f,-0.98 L%.4f,-0.86" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (xm, xm, k.ink))
            b.append('<path d="M%.4f,-0.98 L%.4f,-0.86" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (xm, xm, k.c(GOLD["base"])))
        b.append('<g transform="translate(-0.55 -0.08) scale(0.80 1.0)">%s</g>' % _dragon(k))
        b.append('</g>')
    b.append('</g>')
    o.append("".join(b))
    # the broad chest / neck seen from the front, under the head (coat colour for the dragon ox: the coat front over the shoulders)
    hc = (0.48, -1.60 + bob + hdy)
    neck = [(-0.55, -2.55), (0.10, -2.78), (0.75, -2.62), (1.18, -2.10), (1.16, -1.40), (0.80, -0.98), (0.20, -0.92), (-0.30, -1.10), (-0.62, -1.80)]
    nd = _lin(k, "ofn", col["light"], col["base"], col["dark"], -0.6, -2.7, 1.1, -1.0)
    o.append('<g transform="translate(0 %.4f)"><path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (bob, P._smooth_closed(neck), nd, k.ink))
    if dragon:
        cl = [(-0.52, -2.50), (0.10, -2.74), (0.72, -2.58), (1.12, -2.10), (1.10, -1.62), (0.70, -1.44), (0.50, -1.30), (0.20, -1.44), (-0.30, -1.50), (-0.58, -1.90)]
        gc2 = _lin(k, "ofe", SILK["light"], SILK["base"], SILK["dark"], -0.6, -2.7, 1.1, -1.3)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (P._smooth_closed(cl), gc2, k.ink))
        o.append('<path d="M-0.50,-2.42 Q0.10,-2.66 0.70,-2.50 Q1.0,-2.20 1.05,-1.80" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % k.c(GOLD["base"]))
    o.append('</g>')
    o.append(_ox_head_34(k, col, hc, head_a + roll, blades, wide, dragon, 1.34))
    if tail[1] is not None:
        o.append(tail[1])
    return "".join(o), dict(tail_tip=tail[2], head=hc, feet=feet, mouth=(hc[0] + 0.05, hc[1] + 0.62), eye=(hc[0] - 0.22, hc[1] - 0.14), hump=(0.05, -2.78 + bob), back=(-0.6, -2.5 + bob))


OX_STATES = ("plain", "dragon")
OX_VIEWS = ("side", "three_quarter", "front_three_quarter")
OX_GAITS = ("stand", "walk", "gallop", "startled")
GALLOP_FRAMES = 8


def ox_figure(state="plain", view="side", gait="stand", phase=0.0, flame=-1, blades=False, reed=None, facing=1, coat=1.0, uid="ox", t=0.0, ink=P.INK, tint=None):
    """the ox as a figure dict like puppet.figure(): {"svg", "bbox", "anchors", "feet_y"} in D units with the hooves on y = 0 and x = 0 at the
    middle of the body (anchors["feet"] = (0, 0)).  state "plain" | "dragon"; view "side" | "three_quarter" | "front_three_quarter"; gait "stand" | "walk" | "gallop"
    | "startled"; phase 0..1 loops (gallop: 8 drawings = phase i / 8, walk: 12-16); flame -1 off, 0 / 1 / 2 = the lit tail flame drawing (a
    reed bundle is tied to the tail when flame >= 0 or reed=True); blades=True lashes a bronze blade to each horn; facing -1 mirrors; coat 0..1
    = how far the silk coat is pulled on (dragon only).  Anchors: head, mouth, eye, horn_tip_n / horn_tip_f (blade tips), tail_tip (flame
    base), back (middle of the back, for the coat), hump, flame_top."""
    st = state if state in OX_STATES else "plain"
    vw = view if view in OX_VIEWS else "side"
    gt = gait if gait in OX_GAITS else "stand"
    fl = int(_f(flame, -1.0, -1.0, 2.0)) if not isinstance(flame, bool) else (0 if flame else -1)
    rd = (fl >= 0) if reed is None else bool(reed)
    k = _ctx(uid, ink, tint)
    ph = _num(phase, 0.0)
    wide = gt == "startled"
    fn = {"side": _ox_side, "three_quarter": _ox_34, "front_three_quarter": _ox_front}[vw]
    svg, info = fn(k, st, gt, ph, fl, bool(blades), rd, wide, _f(coat, 1.0, 0.0, 1.0), _num(t, 0.0))
    fc = -1.0 if _num(facing, 1.0) < 0 else 1.0
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    top = -3.05 if vw == "side" else (-3.3 if vw == "front_three_quarter" else -3.0)
    bb = [-2.75, top - 0.35, 3.05, 0.20]
    if rd:
        bb[0] = -3.2
        bb[1] = top - 0.9 if fl >= 0 else top
    sv = defs + ('<g transform="scale(%d 1)">%s</g>' % (int(fc), svg) if fc < 0 else svg)
    box = (bb[0] * fc, bb[1], bb[2] * fc, bb[3]) if fc > 0 else (bb[2] * fc, bb[1], bb[0] * fc, bb[3])
    hd = info["head"]
    mo = info.get("mouth", (hd[0] + 0.95, hd[1] + 0.3))
    ey = info.get("eye", (hd[0] + 0.45, hd[1] - 0.1))
    hu = info.get("hump", (0.62, -2.4))
    bk = info.get("back", (0.0, -2.0))
    an = dict(feet=(0.0, 0.0), head=(hd[0] * fc, hd[1]), tail_tip=(info["tail_tip"][0] * fc, info["tail_tip"][1]),
              back=(bk[0] * fc, bk[1]), hump=(hu[0] * fc, hu[1]), mouth=(mo[0] * fc, mo[1]), eye=(ey[0] * fc, ey[1]),
              flame_top=(info["tail_tip"][0] * fc, info["tail_tip"][1] - 1.0))
    return dict(svg=sv, bbox=box, anchors=an, feet_y=0.0)


STORY18, STORY18_META = {}, {}

QI_TINT = "#2a2634"


def _two_hands(S, name, hand_from="r", bend=0.5, shape="ball", layer="top", stretch=1.3):
    """put the other hand on the prop's grip_far anchor (spear, pick, sash)."""
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def figure(cast_name, pose=None, uid="p"):
    return P.figure(cast_name, pose, uid)


def general_run_frame(phase=0.0, facing=1):
    """one frame of the general's RUN (phase 0..1, 16 frames): shocked, helmet askew, the cup held up in the right hand."""
    p = cycle("general", phase, "run", facing, dict(expr="shocked", mouth=("open", 0.16, 0.18), hat_askew=24, fx=["sweat"], t=0.3, prop_r=dict(type="jue", scale=1.6)), "l")
    p["arm_r"] = dict(hand=(0.70, 0.30), bend=0.9, sharp=0.6, stretch=1.0, layer="front")
    p["lean"] = 0.42 * p.get("lean", 0.0)        # fix 15: was 12-15 deg (read as a fall); now about 5-6 deg = a comic run
    p["head_roll"] = 0.6 * p.get("head_roll", 0.0)
    return p


def qi_pose(phase=0.0, facing=1, speed=1.0):
    """one frame (phase 0..1, 16 frames per cycle) of a Qi soldier running with a spear: a near-black silhouette (tint + ink), no face
    detail.  Draw it with puppet.figure('qi_soldier', qi_pose(...), uid)."""
    base = dict(expr="neutral", tint=QI_TINT, ink=QI_TINT, prop_r=dict(type="spear", angle=-18, scale=0.95), yaw=0.8)
    p = cycle("qi_soldier", phase, "run", facing, base, "l", speed)
    p["arm_r"] = dict(hand=(0.52, 0.30), bend=0.6, stretch=1.1, layer="front")
    p["prop_r"] = dict(type="spear", angle=-16, scale=0.95)
    return p


def _story():
    S, M = {}, {}
    T, G = "tiandan", "general"
    SA = (("yan_soldier_a", "_a"), ("yan_soldier_b", "_b"), ("yan_soldier_c", "_c"))
    TF = (("old_man", "old_man"), ("woman", "woman"), ("child", "child"))
    # --- Tian Dan
    S["tiandan_stand"] = (T, dict(yaw=0.30, expr="smirk", arm_r="down", arm_l="behind", legs="stand"))
    S["tiandan_walk"] = (T, cycle(T, 0.30, "walk", base=dict(expr="neutral")))
    S["tiandan_tug_cloth"] = (T, dict(yaw=0.55, pitch=0.1, expr="determined", lean=9, head_roll=-3, t=0.3, slips=1,
                                      arm_r=dict(hand=(0.80, 0.34), bend=-0.2, stretch=1.1, layer="front"), prop_r=dict(type="silk", angle=-14, scale=1.0),
                                      arm_l=dict(hand=(0.62, 0.16), bend=0.1, stretch=1.1, layer="front"), legs=dict(preset="step", stride=0.45)))
    M["tiandan_tug_cloth"] = dict(note="dressing an ox (screen-right): both hands pulling the crimson silk coat over it; the silk follows `angle`, t animates the wave; "
                                       "animate arm_r hand from (0.55, 0.0) to (0.95, 0.5) and lean 4 -> 14")
    S["tiandan_tie_blade"] = (T, dict(yaw=0.55, pitch=-0.1, expr="determined", lean=6, head_roll=-3,
                                      arm_r=dict(hand=(0.86, -0.12), bend=-0.4, stretch=1.2, layer="front"), prop_r=dict(type="blade", angle=-28, scale=1.0),
                                      arm_l=dict(hand=(0.74, 0.04), bend=-0.3, stretch=1.2, layer="front"), legs="wide"))
    M["tiandan_tie_blade"] = dict(note="lashing a short bronze blade to an ox horn (screen-right, hands at horn height; the horn tip of the ox is about 2.3 D above the "
                                       "soles); anchor blade_r = the blade tip")
    S["tiandan_raise_torch"] = (T, dict(yaw=0.30, pitch=-0.35, expr="determined", lean=-4, fire_frame=0, t=0.2,
                                        arm_r=dict(hand=(0.42, -0.55), bend=-0.6, stretch=1.3, layer="front"), prop_r=dict(type="torch", angle=-82, scale=1.0),
                                        arm_l=dict(hand=(-0.40, 1.05), bend=0.4), legs="wide"))
    M["tiandan_raise_torch"] = dict(note="raising the lit torch ('จุดไฟ'); fire_frame 0/1/2 = the three flame drawings (-1 = unlit); anchor torch_flame_r")
    S["tiandan_point"] = (T, dict(yaw=0.45, pitch=-0.15, expr="determined", mouth="flat", arm_r=dict(hand=(1.10, 0.10), shape="point", bend=-0.5, stretch=1.3),
                                  arm_l=dict(hand=(-0.40, 1.02), bend=0.4), legs="wide"))
    S["tiandan_calm_smile"] = (T, dict(yaw=0.25, pitch=-0.1, expr="happy", mouth="smile", head_roll=-3, arm_r="behind", arm_l="behind", legs="stand"))
    S["tiandan_accept_sash"] = (T, dict(yaw=0.30, pitch=0.05, expr="smirk", lean=5, head_roll=-3, t=0.2, slips=1,
                                        arm_r=dict(hand=(0.66, 0.50), bend=0.2, stretch=1.1, layer="front"), prop_r=dict(type="sash", scale=1.0),
                                        arm_l=dict(hand=(0.40, 0.52), bend=0.2, stretch=1.1, layer="front"), legs="stand"))
    M["tiandan_accept_sash"] = dict(note="accepting a general's sash (red silk, gold ends, bronze seal) with both hands held out, a small bow; t sways the ends")
    S["tiandan_read_slips"] = (T, dict(yaw=0.40, pitch=0.2, expr="neutral", arm_r=dict(hand=(0.55, 0.38), bend=0.3, layer="front"), prop_r=dict(type="slips", angle=-80, scale=1.0),
                                       arm_l=dict(hand=(0.20, 0.75), bend=0.5, layer="front"), legs="stand"))
    M["tiandan_read_slips"] = dict(note="the market clerk with a bundle of bamboo tally slips (the counting board stall, shot 5)")
    # --- the general
    S["general_stand"] = (G, dict(yaw=0.20, pitch=-0.3, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    S["general_laugh"] = (G, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                  arm_r=dict(hand=(0.46, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.50, 0.98), bend=0.9, shape="open"), legs="wide"))
    M["general_laugh"] = dict(note="BELLY LAUGH, a held drawing: head back, hands on the belly; bounce it by animating squash (1.02, 0.98) <-> (0.99, 1.02) at ~3 Hz "
                                   "and head_dy 0 <-> 0.06 (0.06 D)")
    S["general_arms_wide"] = (G, dict(yaw=0.15, pitch=-0.35, expr="smug", mouth="talk_b", head_roll=4,
                                      arm_r=dict(hand=(1.30, 0.10), bend=-0.3, stretch=1.3, shape="open"), arm_l=dict(hand=(-1.30, 0.12), bend=-0.3, stretch=1.3, shape="open", layer="back"),
                                      legs="wide"))
    M["general_arms_wide"] = dict(lipsync=True, note="QUOTE 1a: arms wide in mock disbelief; LIP-SYNC mouth=talk_mouth(g) during the quote, 'flat' otherwise")
    S["general_boast"] = (G, dict(yaw=0.30, pitch=-0.55, expr="smug", mouth="talk_a", head_roll=-6, lean=-5,
                                  arm_r=dict(hand=(0.16, 0.74), bend=0.9, stretch=1.0, shape="ball", layer="front"), arm_l="akimbo", legs="wide"))
    M["general_boast"] = dict(lipsync=True, note="QUOTE 1b: thumb (fist) to the chest, chin up, boasting; LIP-SYNC")
    S["general_toast"] = (G, dict(yaw=0.25, pitch=-0.4, expr="laughing", mouth="talk_b", head_roll=-6, t=0.3, squash=(1.01, 0.99),
                                  arm_r=dict(hand=(0.92, -0.40), bend=-0.6, stretch=1.3, layer="front"), prop_r=dict(type="jue", scale=1.6), arm_l="akimbo", legs="wide"))
    M["general_toast"] = dict(lipsync=True, note="QUOTE 2a: raising the bronze jue cup in a toast, laughing; LIP-SYNC; bounce like general_laugh. anchor cup_r")
    S["general_carve"] = (G, dict(yaw=0.30, pitch=-0.35, expr="excited", mouth="talk_b", head_roll=5, t=0.3, cup_tilt=40,
                                  arm_l=dict(hand=(-0.62, 0.50), bend=0.5, stretch=1.1, layer="front"), prop_l=dict(type="jue", scale=1.6),
                                  arm_r=dict(hand=(0.84, 0.46), bend=-0.2, stretch=1.2, shape="open", layer="front"), legs="wide"))
    M["general_carve"] = dict(lipsync=True, note="QUOTE 2b: miming carving the beef (the right hand saws across, animate hand x 0.6 <-> 0.95), the cup tilting in the left hand; LIP-SYNC")
    S["general_jaw_drop"] = (G, dict(yaw=0.25, pitch=0.1, expr="stunned", mouth=("open", 0.18, 0.20), head_dy=0.03, gaze=(0.8, 0.0), fx=["sweat"], squash=(0.99, 1.02),
                                    arm_r=dict(hand=(0.55, 1.10), bend=0.2), prop_r=dict(type="jue", scale=1.6), cup_tilt=75, arm_l=dict(hand=(-0.55, 1.06), bend=0.2), legs="stand"))
    M["general_jaw_drop"] = dict(note="jaw dropped (held open mouth), the cup tipping out of his hand")
    S["general_run"] = (G, cycle(G, 0.30, "run", base=dict(expr="shocked", mouth=("open", 0.16, 0.18), hat_askew=24, fx=["sweat"], t=0.3, prop_r=dict(type="jue", scale=1.6), cup_tilt=0), arms="l"))
    S["general_run"][1]["arm_r"] = dict(hand=(0.70, 0.30), bend=0.9, sharp=0.6, stretch=1.0, layer="front")
    M["general_run"] = dict(note="the ending: RUN, helmet askew (hat_askew 24), cup still in his hand. ONE frame (phase 0.30); animate cycle(general, frame / 16, 'run', facing, "
                                  "base=dict(expr='shocked', hat_askew=24, prop_r='jue', ...), arms='l') then re-set arm_r so the cup hand stays up (see general_run_frame())")
    # --- Yan soldiers
    for c, sf in SA:
        S["soldier_laugh_point" + sf] = (c, dict(yaw=0.35, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                                 arm_r=dict(hand=(0.80, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
        S["soldier_cheer_cup" + sf] = (c, dict(yaw=0.20, pitch=-0.4, expr="laughing", mouth="talk_b", head_roll=-6, t=0.3,
                                               arm_r=dict(hand=(0.50, -0.50), bend=-0.6, stretch=1.3, layer="front"), prop_r=dict(type="jue", scale=1.4), arm_l=dict(hand=(-0.46, 0.20), bend=-0.4, shape="open"), legs="wide"))
        S["soldier_mock_moo" + sf] = (c, dict(yaw=0.10, pitch=-0.2, expr="grinning", mouth=("open", 0.22, 0.16), head_roll=6, t=0.3,
                                              arm_r=dict(hand=(0.54, -0.56), bend=-0.9, stretch=1.2, shape="point", layer="top"), arm_l=dict(hand=(-0.54, -0.56), bend=-0.7, stretch=1.2, shape="point", layer="top"),
                                              legs="wide"))
        S["soldier_asleep" + sf] = (c, dict(yaw=0.30, pitch=0.5, expr="asleep", fx=["zzz"], head_roll=18, lean=12, t=0.3,
                                            arm_r=dict(hand=(0.15, 0.85), bend=0.9, layer="front"), arm_l="behind", legs=dict(preset="crouch", crouch=0.30, spread=0.12)))
        S["soldier_freeze" + sf] = (c, dict(yaw=0.30, pitch=0.05, expr="shocked", fx=["sweat"], squash=(0.97, 1.03), t=0.3,
                                            arm_r=dict(hand=(0.40, 0.95), bend=0.2, stretch=1.0), arm_l=dict(hand=(-0.40, 0.95), bend=0.2, stretch=1.0), legs="narrow"))
        S["soldier_fall_bottom" + sf] = (c, dict(yaw=0.30, pitch=-0.1, expr="stunned", mouth=("open", 0.16, 0.16), fx=["sweat"], lean=-10, head_dy=0.03, squash=(1.0, 0.93),
                                                 arm_r=dict(hand=(-0.35, 1.25), bend=0.3, stretch=1.1, layer="back"), arm_l=dict(hand=(0.95, 1.0), bend=0.2),
                                                 legs=dict(preset="crouch", crouch=0.60, spread=0.65)))
        S["soldier_flee" + sf] = (c, cycle(c, 0.30, "run", base=dict(expr="shocked", mouth=("open", 0.16, 0.18), fx=["sweat"])))
        S["soldier_stand" + sf] = (c, dict(yaw=0.30, expr="neutral", arm_r=dict(hand=(0.40, 0.55), bend=0.4, layer="front"), prop_r=dict(type="spear", angle=-90, scale=1.0), arm_l="down", legs="stand"))
    M["soldier_laugh_point"] = dict(note="laughing and pointing (screen-right; mirror=True for left): yan_soldier_a; names with suffix _a _b _c")
    M["soldier_cheer_cup"] = dict(note="cheering with a bronze cup raised (party shot); a/b/c")
    M["soldier_mock_moo"] = dict(note="mock moo: two index fingers as horns at the temples, mouth wide open; a/b/c")
    M["soldier_asleep"] = dict(note="asleep on his feet/slumped, zzz; a/b/c")
    M["soldier_freeze"] = dict(note="freeze in terror: wide eyes, sweat, arms stiff; a/b/c")
    M["soldier_fall_bottom"] = dict(note="comic fall on his bottom (squashed, legs splayed, unhurt); a/b/c")
    M["soldier_flee"] = dict(note="flee: one frame (phase 0.30) of cycle(c, phase, 'run', facing, base=dict(expr='shocked', ...)); a/b/c")
    M["soldier_stand"] = dict(note="standing with the spear upright (prop spear at angle -90); a/b/c")
    # --- townsfolk
    for c, nm in TF:
        S[nm + "_beat"] = (c, dict(yaw=0.30, pitch=-0.2, expr="shouting", mouth=("open", 0.26, 0.17), head_roll=-5, t=0.3, pot_ring=1.0,
                                   arm_l=dict(hand=(-0.38, 0.40), bend=0.5, stretch=1.0, layer="front"), prop_l="bronze_pot",
                                   arm_r=dict(hand=(0.62, 0.30), bend=-0.4, stretch=1.1, layer="front"), prop_r=dict(type="mallet", angle=-55, scale=1.3), legs="wide"))
        S[nm + "_stand"] = (c, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
        S[nm + "_worried"] = (c, dict(yaw=0.30, pitch=0.1, expr="worried", fx=["sweat"], arm_r=dict(hand=(0.14, 0.78), bend=0.9, layer="front"), arm_l=dict(hand=(-0.14, 0.80), bend=0.9, layer="front"), legs="stand"))
    M["old_man_beat"] = dict(note="beating a bronze vessel with a stick, shout face (mouth open, no lip-sync); pot_ring 0..1 = sound rings (animate t); prop_r mallet: "
                                  "animate its angle -120 <-> -70 (strike) and hand y; also woman_beat, child_beat")
    for c, nm in TF[:2]:
        S[nm + "_dig"] = (c, dict(yaw=0.45, pitch=0.1, expr="determined", lean=8, t=0.3, arm_r=dict(hand=(0.55, -0.50), bend=-0.7, stretch=1.3, layer="front"),
                                  prop_r=dict(type="pick", angle=-62, scale=1.0), arm_l=dict(hand=(0.2, 0.2), bend=0.3), legs=dict(preset="step", stride=0.3)))
        _two_hands(S, nm + "_dig", bend=0.4, layer="front", stretch=1.3)
        S[nm + "_carry_basket"] = (c, dict(yaw=0.40, expr="neutral", lean=4, arm_r=dict(hand=(0.36, 0.55), bend=0.5, layer="front"), prop_r="basket", arm_l="down", legs="stand"))
    S["child_carry_basket"] = ("child", dict(yaw=0.40, expr="happy", arm_r=dict(hand=(0.30, 0.45), bend=0.5, layer="front"), prop_r="basket", arm_l="down", legs="stand"))
    M["old_man_dig"] = dict(note="digging through the wall base with a pick (screen-right), both hands on the handle; anchor pick_point_r; the basket: *_carry_basket (also woman_dig)")
    S["envoy_stand"] = ("envoy", dict(yaw=0.30, expr="neutral", arm_r=dict(hand=(0.40, 0.60), bend=0.4, layer="front"), prop_r=dict(type="banner", angle=-90, scale=1.0), t=0.3, arm_l="down", legs="stand"))
    S["envoy_bow"] = ("envoy", dict(yaw=0.35, pitch=0.7, expr="neutral", mouth="flat", head_dy=0.12, lean=34, head_roll=6, blink=0,
                                    arm_r=dict(hand=(0.78, 0.74), bend=0.2, stretch=1.1, layer="top"), arm_l=dict(hand=(0.60, 0.80), bend=0.2, stretch=1.1, layer="top"), legs=dict(preset="stand", crouch=0.05)))
    M["envoy_bow"] = dict(note="bowing from the waist, hands clasped in front (no banner); animate lean 0 -> 34 and back")
    S["envoy_walk"] = ("envoy", cycle("envoy", 0.30, "walk", base=dict(expr="neutral", prop_r=dict(type="banner", angle=-90, scale=1.0), t=0.3), arms="l"))
    S["envoy_walk"][1]["arm_r"] = dict(hand=(0.40, 0.60), bend=0.4, layer="front")
    M["envoy_stand"] = dict(note="holding a plain cloth banner (no text) upright in the right hand; t waves the cloth, banner_side +/-1 flips its flow")
    # --- Qi soldier silhouette
    S["qi_run"] = ("qi_soldier", qi_pose(0.30))
    M["qi_run"] = dict(note="dark silhouette run frame with a spear; animate with qi_pose(frame / 16, facing)")
    for n in ("tiandan_walk", "soldier_flee_a"):
        M.setdefault(n, dict(note="one frame (phase 0.30) of cycle(); animate cycle(cast, frame / N, mode, facing, base, arms) with N = 28 walk / 16 run"))
    return S, M


# ============================================================================= registration
def register():
    if getattr(P, "_cast18_registered", False):
        CE.register_stage()
        if not STORY18:
            s, m = _story()
            STORY18.update(s)
            STORY18_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_ink_limb"):
        _O18[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    CE.COSTUMES.update(COSTUMES18)
    CE.HATS.update(HATS18)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS18 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP18)
    for n, c in NEW_CAST18.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS18)
    P._cast18_registered = True
    s, m = _story()
    STORY18.update(s)
    STORY18_META.update(m)
    P.STORY.update(STORY18)
    CE.register_stage()


register()
