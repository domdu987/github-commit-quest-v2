#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast23.py -- the cast of film 23 ("ไอ้กองทัพลูกโป่ง", the Ghost Army, Normandy 1944 / the Rhine 1945) for the v2 puppet,
as an extension module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).  Comic and bloodless: no weapon is
held by anybody.

    import sys; sys.path.insert(0, ".../v3/cast23"); import cast23     # registers on import (idempotent); BEFORE sprites
    import puppet                                                      # the same module object, now with the members below
    cast, pose = cast23.STORY23["gi_paint_star"]
    f = puppet.figure(cast, pose, "f")
    p = cast23.pump_frame("gi_pump", g / 20.0)                          # cycles return plain pose dicts
    p = cast23.ride_frame("fr_beret", g / 14.0)                         # the bicycle is drawn INSIDE the sprite

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  gi23 (M1941 field jacket + web belt), major23 (khaki officer tunic, Sam Browne belt), feld23 (German
                       field-grey tunic), mariniere23 (striped French shirt + red neckerchief)
    cast_ext.HATS      gi23 (dispatch: M1 helmet with net + dangling chin straps / overseas cap / bare / German M43 field cap;
                       optional headphones)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast10's wrappers: _norm (this module's pose keys), _face (red face, puffed cheeks, daze
stars, big sweat drop), _moustache (style major23), _hand (white paint on the hands), _prop (new props), figure (bicycle,
hand pump, crate carried / sat on, balloon at the mouth, the ground contact point).
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
import cast4 as C4      # noqa: E402
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_taper = C9._taper
_O23 = {}
_POSE23 = {}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours (period palette: olive, khaki, field grey; no harsh black)
OD = dict(light="#9ea06a", base="#7d7f4c", dark="#55572f", deep="#3c3e22")          # helmet olive drab
JACKET = dict(light="#b3aa78", base="#988f5e", dark="#6a633e")                     # M41 field jacket, olive-tan
PANTS_OD = dict(base="#6a6440", dark="#48432a")
WEB = dict(light="#d2c596", base="#b5a674", dark="#7e734c")                        # khaki webbing
BRASS = dict(light="#f2d98a", base="#c9a44a", dark="#8a6a26")
KHAKI = dict(light="#dcc596", base="#bfa26c", dark="#8a7046")                      # the Major's tunic
LEATHER = dict(light="#9a6440", base="#6e4026", dark="#46261a")
FELD = dict(light="#a3ab9c", base="#7f887a", dark="#59614f", collar="#4a5a48")     # German field grey
WHITE_P = dict(light="#ffffff", base="#f4f2ea", dark="#c9c5b8")                    # white paint
REC = dict(base="#2c2a33", groove="#4a4856", shine="#8a88a0", label="#c8402e", label2="#f0e2c0")
RUBBER = dict(light="#f08a7a", base="#d9483c", dark="#8e2a22")
BALLOON_COLS = ("#3f74c0", "#e9b632", "#4a9a5a", "#e07ab0", "#f2f0e8", "#d9483c")
BIKE_COLS = {"green": dict(light="#5f9a7a", base="#2f6a50", dark="#1c4232"), "maroon": dict(light="#b25a4e", base="#86302a", dark="#561a16")}
TYRE = "#2e2a30"
CHROME = dict(light="#eef0f4", base="#b8bec8", dark="#6e7480")
WOOD = dict(light="#e0b47a", base="#b8834c", dark="#7a5430")
CRATE = dict(light="#c9b27c", base="#a58c58", dark="#6e5a36", stencil="#4a4430")
BREAD = dict(light="#f2c47a", base="#d49040", dark="#8e5a22")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _path(d, fill, ink, sw=0.020, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"%s/>' % (d, fill, ink, sw, extra)


def _poly(k, pts, fill, sw=0.014):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (_poly_d(pts), fill, k.ink, sw)


def _g(k, name, col, x0, x1, y0=0.0, y1=0.0):
    return _lin(k, name, col["light"], col["base"], col["dark"], x0, y0, x1, y1)


# ============================================================================= hats (head frame, head centre (0, 0))
def _netting(k, dx, top, yb, hw):
    """the camouflage net over the M1 helmet: a loose diamond mesh clipped to the dome."""
    cid = "%s_net%d" % (k.uid, len(k.defs))
    dome = _dome_d(dx, yb, top, hw)
    k.defs.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, dome))
    ls = []
    for i in range(-6, 7):
        x = dx + i * 0.13
        ls.append("M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" % (x - 0.5, top - 0.05, x + 0.5, yb + 0.30, x + 0.5, top - 0.05, x - 0.5, yb + 0.30))
    return ('<g clip-path="url(#%s)"><path d="%s" fill="none" stroke="%s" stroke-width="0.011" opacity="0.55"/></g>'
            % (cid, "".join(ls), k.c(OD["deep"])))


def _dome_d(dx, yb, top, hw):
    c = yb + (top - yb) * 1.30
    return "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" % (dx - hw, yb, dx - hw * 1.02, c, dx + hw * 1.02, c, dx + hw, yb)


def _m1_helmet(k, C, yaw, ext):
    col = C.get("helmet_colors", OD)
    dx = -0.03 * yaw
    fx = dx + 0.10 * yaw
    yb, top, hw = -0.13, -0.70, 0.555
    o = []
    # dangling chin straps (unbuckled, the GI look), behind the brim
    for s in (-1, 1):
        g = _clamp(1.0 - 0.6 * max(0.0, s * yaw), 0.35, 1.0)
        x0 = dx + s * 0.47 * (0.75 + 0.25 * g)
        sway = 0.03 * s
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x0, yb + 0.02, x0 + sway, 0.10, x0 + 2 * sway, 0.24)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (d, k.ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (d, k.c(WEB["base"])))
        o.append('<rect x="%.4f" y="0.22" width="0.040" height="0.034" rx="0.006" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x0 + 2 * sway - 0.02, k.c(BRASS["base"]), k.ink))
        ext.append((x0 + 2 * sway, 0.27))
    gr = CE._gradient(k, "m1", col, x0=-0.6, x1=0.6, mid=0.30)
    dome = _dome_d(dx, yb, top, hw)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (dome, gr, k.ink))
    if C.get("net", True):
        o.append(_netting(k, dx, top, yb, hw))
    # highlight
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.40"/>'
             % (dx - 0.40, yb - 0.12, dx - 0.36, top + 0.16, dx - 0.12, top + 0.06))
    # the rim: a flat steel lip, wider than the dome, dipping slightly at the sides
    rim = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
           % (dx - hw - 0.07, yb + 0.03, fx, yb - 0.04, dx + hw + 0.07, yb + 0.03, dx + hw + 0.06, yb + 0.075, fx, yb + 0.015, dx - hw - 0.06, yb + 0.075))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (rim, k.c(col["dark"]), k.ink))
    ext += [(dx - hw - 0.09, yb + 0.05), (dx + hw + 0.09, yb + 0.05), (dx, top - 0.02)]
    return "".join(o), (dx, top - 0.01)


def _overseas_cap(k, C, yaw, ext):
    col = C.get("cap_colors", dict(light="#a8a06e", base="#857d4e", dark="#5a5434", piping="#d8c48a"))
    dx = -0.03 * yaw
    o = []
    pts = [(dx - 0.47, -0.30), (dx - 0.44, -0.44), (dx - 0.30, -0.56), (dx - 0.02, -0.63), (dx + 0.30, -0.58), (dx + 0.45, -0.46), (dx + 0.49, -0.31)]
    body = P._smooth_open(pts) + " Q%.4f,%.4f %.4f,%.4f Z" % (dx, -0.40, dx - 0.47, -0.30)
    gr = CE._gradient(k, "oc", col, x0=-0.5, x1=0.5, mid=0.3)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (body, gr, k.ink))
    # the folded curtain band and the centre crease
    o.append('<path d="M%.4f,-0.39 Q%.4f,-0.47 %.4f,-0.40" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (dx - 0.44, dx, dx + 0.46, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.42 Q%.4f,-0.52 %.4f,-0.60" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (dx + 0.02, dx + 0.0, dx - 0.02, k.c(col["dark"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.9"/>' % (P._smooth_open([(p[0], p[1] + 0.015) for p in pts[1:-1]]), k.c(col.get("piping", "#d8c48a"))))
    # a small brass disc badge on the curtain (screen-left side)
    o.append(_circ((dx - 0.26, -0.40), 0.028, k.c(BRASS["base"]), k, 0.008))
    ext += [(dx - 0.49, -0.29), (dx + 0.51, -0.30), (dx, -0.65)]
    return "".join(o), (dx, -0.64)


def _m43_cap(k, C, yaw, ext):
    col = C.get("cap_colors", dict(light=FELD["light"], base=FELD["base"], dark=FELD["dark"]))
    dx = -0.03 * yaw
    fx = dx + 0.11 * yaw
    o = []
    crown = [(dx - 0.47, -0.27), (dx - 0.49, -0.42), (dx - 0.38, -0.58), (dx, -0.66), (dx + 0.38, -0.58), (dx + 0.49, -0.42), (dx + 0.47, -0.27)]
    gr = CE._gradient(k, "m43", col, x0=-0.5, x1=0.5, mid=0.3)
    o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_open(crown), gr, k.ink))
    o.append('<path d="M%.4f,-0.56 Q%.4f,-0.46 %.4f,-0.42" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (dx - 0.30, dx - 0.36, dx - 0.40, k.c(col["dark"])))
    # turned-up flap with two small buttons
    flap = "M%.4f,-0.27 L%.4f,-0.38 Q%.4f,-0.42 %.4f,-0.38 L%.4f,-0.27 Q%.4f,-0.22 %.4f,-0.27 Z" % (dx - 0.48, dx - 0.47, fx, dx + 0.47, dx + 0.48, fx, dx - 0.48)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (flap, k.c(col["base"]), k.ink))
    for bx in (fx - 0.035, fx + 0.035):
        o.append(_circ((bx, -0.31), 0.014, k.c("#8a8e86"), k, 0.006))
    # eagle (spread wings) and cockade on the crown front
    o.append('<path d="M%.4f,-0.47 q-0.06,-0.04 -0.12,-0.01 q0.06,0.0 0.12,0.03 q0.06,-0.03 0.12,-0.03 q-0.06,-0.03 -0.12,0.01 Z" fill="%s" stroke="%s" stroke-width="0.006"/>'
             % (fx, k.c("#d8dcd4"), k.c(FELD["dark"])))
    o.append(_circ((fx, -0.405), 0.020, k.c("#e8e4dc"), k, 0.006))
    o.append('<circle cx="%.4f" cy="-0.405" r="0.008" fill="%s"/>' % (fx, k.c("#b8302a")))
    # short peak
    vis = ("M%.4f,-0.265 Q%.4f,-0.235 %.4f,-0.265 Q%.4f,-0.13 %.4f,-0.115 Q%.4f,-0.13 %.4f,-0.265 Z"
           % (fx - 0.34, fx, fx + 0.34, fx + 0.26, fx, fx - 0.26, fx - 0.34))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (vis, k.c("#4e5548"), k.ink))
    o.append('<path d="M%.4f,-0.20 Q%.4f,-0.16 %.4f,-0.17" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.35"/>' % (fx - 0.20, fx - 0.08, fx + 0.06))
    ext += [(dx - 0.50, -0.27), (dx + 0.50, -0.27), (dx, -0.68), (fx, -0.14)]
    return "".join(o), (dx, -0.67)


def _phones(k, C, yaw, ext, over_top):
    """headphones: a steel band over the head (or cap) and two black ear cups; a cord down from the near cup."""
    dx = -0.03 * yaw
    o = []
    for s in (-1, 1):
        g = _clamp(1.0 - 0.7 * max(0.0, s * yaw), 0.25, 1.0)
        x = dx + s * (0.44 + 0.06 * g)
        o.append('<ellipse cx="%.4f" cy="0.0" rx="%.4f" ry="0.150" fill="%s" stroke="%s" stroke-width="0.020"/>' % (x, 0.085 * (0.55 + 0.45 * g), k.c("#3a3440"), k.ink))
        o.append('<ellipse cx="%.4f" cy="-0.03" rx="%.4f" ry="0.060" fill="%s" opacity="0.8"/>' % (x - s * 0.015, 0.030 * g, k.c("#6a6474")))
        ext.append((x + s * 0.09, 0.0))
    band = "M%.4f,-0.10 C%.4f,%.4f %.4f,%.4f %.4f,-0.10" % (dx - 0.50, dx - 0.52, over_top - 0.20, dx + 0.52, over_top - 0.20, dx + 0.50)
    o.insert(0, '<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>'
             % (band, k.ink, band, k.c(CHROME["base"])))
    s = 1.0 if yaw >= 0 else -1.0
    x = dx - s * 0.50
    o.append('<path d="M%.4f,0.14 q%.4f,0.12 0.0,0.24 q%.4f,0.10 %.4f,0.20" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (x, -0.06 * s, 0.06 * s, 0.02 * s, k.c("#3a3440")))
    ext += [(dx, over_top - 0.06), (x, 0.56)]
    return "".join(o)


def _hat_gi23(k, C, yaw):
    """hat dispatch for cast23: C["hat23"] = "m1" | "overseas" | "bare" | "m43", overridden per pose by the key `hat23`;
    headphones on top with C["phones23"] or the pose key `phones23`."""
    kind = _POSE23.get("hat") or C.get("hat23", "m1")
    ext = []
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    if kind == "m1":
        s, top = _m1_helmet(k, C, yaw, ext)
    elif kind == "overseas":
        s, top = _overseas_cap(k, C, yaw, ext)
    elif kind == "m43":
        s, top = _m43_cap(k, C, yaw, ext)
    else:
        s, top = "", (0.0, -0.49)
        ext.append((0.0, -0.50))
    o.append(s)
    ph = _POSE23.get("phones")
    if ph is None:
        ph = C.get("phones23", False)
    if ph:
        o.append(_phones(k, C, yaw, ext, top[1]))
        top = (top[0], top[1] - 0.06)
    o.append("</g>")
    C4._ext_hat(k, C, ext)
    return "".join(o), top


HATS23 = {"gi23": _hat_gi23}


# ============================================================================= costumes (torso-local)
def _pocket(k, X, x, y, w, h, base, dark, btn, scallop=False):
    o = [_poly(k, [X(x - w / 2, y), X(x + w / 2, y), X(x + w / 2 - 0.005, y + h), X(x - w / 2 + 0.005, y + h)], k.c(base), 0.012)]
    if scallop:
        o.append(_poly(k, [X(x - w / 2 - 0.005, y - 0.02), X(x + w / 2 + 0.005, y - 0.02), X(x + w / 2, y + 0.035), X(x + w * 0.25, y + 0.045), X(x, y + 0.065),
                           X(x - w * 0.25, y + 0.045), X(x - w / 2, y + 0.035)], k.c(dark), 0.012))
    else:
        o.append(_poly(k, [X(x - w / 2 - 0.005, y - 0.02), X(x + w / 2 + 0.005, y - 0.02), X(x + w / 2, y + 0.04), X(x - w / 2, y + 0.04)], k.c(dark), 0.012))
    o.append(_circ(X(x, y + 0.02), 0.013, k.c(btn), k, 0.006))
    return "".join(o)


def _pack(k, C, m):
    """SCR-300 style radio pack on the back: a box behind the torso and a whip antenna rising behind the shoulder."""
    X = _X(m)
    s = -1.0
    bx, by = X(s * 0.30, 0.50)
    o = ['<rect x="%.4f" y="%.4f" width="0.36" height="0.62" rx="0.04" fill="%s" stroke="%s" stroke-width="0.022"/>' % (bx - 0.18, by - 0.06, k.c(OD["dark"]), k.ink)]
    ax, ay = bx - 0.10, by - 0.04
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (ax, ay, ax - 0.06, ay - 1.35, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (ax, ay, ax - 0.06, ay - 1.35, k.c("#8a8a7a")))
    o.append(_circ((ax - 0.06, ay - 1.36), 0.022, k.c("#5a5a4a"), k, 0.008))
    k.ext.append((ax - 0.06, ay - 1.40, 0.04))
    k.ext.append((bx - 0.22, by + 0.60, 0.03))
    return "".join(o)


def _cos_gi23(k, C, m):
    """the GI: an olive-tan M1941 field jacket (pointed collar over the dark OD shirt, front placket with buttons, two flapped chest
    pockets), a khaki web belt with a brass buckle, OD trousers below; optional radio pack on the back (C["pack23"])."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    hw = m.hwa
    dark = col.get("dark", JACKET["dark"])
    o = []
    o.append(_poly(k, [X(-0.14, 0.38), X(0.14, 0.38), X(0.0, 0.57)], k.c(col.get("shirt", "#5e5a3a")), 0.012))
    o.append(_ln([X(0.0, 0.57), X(0.0, yb)], k.c(dark), 0.014))
    for y in (0.64, 0.80, 0.96, 1.12):
        if y > yb - 0.10:
            break
        o.append(_circ(X(0.025, y), 0.016, k.c("#4a4430"), k, 0.006))
    for s in (-1, 1):
        x = s * 0.56 * hw
        o.append(_pocket(k, X, x, 0.62, 0.17, 0.15, col.get("pocket", col["base"]), dark, "#4a4430"))
        o.append(_poly(k, [X(s * 0.03, 0.385), X(s * 0.25, 0.37), X(s * 0.16, 0.58)], k.c(col.get("collar", JACKET["light"])), 0.014))
    o.append(CE._bowl(k, col.get("pants", PANTS_OD["base"]), yb, yB))
    ywb = yb - 0.035
    o.append(_ln([X(-hw * 1.1, ywb), X(hw * 1.1, ywb)], k.ink, 0.075))
    o.append(_ln([X(-hw * 1.1, ywb), X(hw * 1.1, ywb)], k.c(WEB["base"]), 0.052))
    o.append(_ln([X(-hw * 1.1, ywb - 0.012), X(hw * 1.1, ywb - 0.012)], k.c(WEB["light"]), 0.010, ' opacity="0.8"'))
    for xx in (-0.30, -0.20, 0.20, 0.30):
        if abs(xx) < hw:
            o.append('<circle cx="%.4f" cy="%.4f" r="0.008" fill="%s"/>' % (X(xx, ywb)[0], ywb + 0.012, k.c(WEB["dark"])))
    bx, by = X(0.0, ywb)
    o.append('<rect x="%.4f" y="%.4f" width="0.090" height="0.066" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx - 0.045, by - 0.033, k.c(BRASS["base"]), k.ink))
    behind = _pack(k, C, m) if C.get("pack23") else ""
    return "".join(o), behind, ""


def _cos_major23(k, C, m):
    """the Major: a khaki officer's tunic (notched lapels over a khaki shirt and a dark tie, four brass buttons, four flapped
    pockets, a ribbon bar), a brown Sam Browne belt (waist belt + the diagonal cross strap), the tunic skirt over the hips."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    dark = col.get("dark", KHAKI["dark"])
    o = []
    o.append(_poly(k, [X(-0.17, 0.38), X(0.17, 0.38), X(0.0, 0.70)], k.c(col.get("shirt", "#d8c49a")), 0.012))
    o.append(_poly(k, [X(-0.03, 0.40), X(0.03, 0.40), X(0.045, 0.62), X(0.0, 0.68), X(-0.045, 0.62)], k.c(col.get("tie", "#5a4630")), 0.010))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.04, 0.37), X(s * 0.30, 0.38), X(s * 0.22, 0.52), X(s * 0.26, 0.56), X(s * 0.04, 0.74)], k.c(col.get("lapel", KHAKI["light"])), 0.014))
        o.append(_pocket(k, X, s * 0.58 * hw, 0.70, 0.19, 0.16, col["base"], dark, BRASS["base"]))
        o.append(_pocket(k, X, s * 0.52 * hw, yB - 0.42, 0.24, 0.20, col["base"], dark, BRASS["base"]))
    for y in (0.80, 0.94, 1.08, 1.22):
        if y > yB - 0.22:
            break
        o.append(_circ(X(0.0, y), 0.022, k.c(BRASS["base"]), k, 0.008))
    # ribbon bar over the left (screen-right) breast pocket
    rx, ry = X(0.58 * hw, 0.60)
    for i, c in enumerate(("#b8302a", "#f0e8d0", "#3a5aa0", "#e0b84a")):
        o.append('<rect x="%.4f" y="%.4f" width="0.040" height="0.040" fill="%s" stroke="%s" stroke-width="0.006"/>' % (rx - 0.08 + 0.04 * i, ry - 0.04, k.c(c), k.ink))
    # Sam Browne cross strap: screen-right shoulder to screen-left hip
    yw = yB - 0.24
    st = [X(hw * 0.62, TT + 0.03), X(-hw * 0.10, 0.80), X(-hw * 0.62, yw)]
    o.append(_ln(st, k.ink, 0.074))
    o.append(_ln(st, k.c(LEATHER["base"]), 0.050))
    o.append(_ln(st, k.c(LEATHER["light"]), 0.010, ' opacity="0.7"'))
    inside = "".join(o)
    yt = yB - 0.16
    hem = yB + C.get("tunic_len", 0.20)
    gr = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "mj", X, yt, hw * 0.99, hem, hw + 0.06, gr, sw=0.024, folds=((-0.12, yt + 0.06, -0.14, hem - 0.03), (0.14, yt + 0.06, 0.16, hem - 0.03)),
                    fold_col=k.c(dark))]
    ov.append(_ln([X(0.0, yt), X(0.0, hem)], k.c(dark), 0.012))
    ov.append(_ln([X(-hw, yw), X(hw, yw)], k.ink, 0.080))
    ov.append(_ln([X(-hw, yw), X(hw, yw)], k.c(LEATHER["base"]), 0.056))
    ov.append(_ln([X(-hw, yw - 0.014), X(hw, yw - 0.014)], k.c(LEATHER["light"]), 0.010, ' opacity="0.7"'))
    bx, by = X(0.0, yw)
    ov.append('<rect x="%.4f" y="%.4f" width="0.10" height="0.075" rx="0.012" fill="none" stroke="%s" stroke-width="0.034"/>' % (bx - 0.05, by - 0.0375, k.ink))
    ov.append('<rect x="%.4f" y="%.4f" width="0.10" height="0.075" rx="0.012" fill="none" stroke="%s" stroke-width="0.018"/>' % (bx - 0.05, by - 0.0375, k.c(BRASS["base"])))
    ov.append(_circ(X(-hw * 0.62, yw), 0.026, k.c(BRASS["base"]), k, 0.008))
    return inside, "", "".join(ov)


def _cos_feld23(k, C, m):
    """German field-grey tunic: dark green collar with pale collar tabs, five buttons, four pockets with scalloped flaps, a dark
    leather belt with a dull buckle, the tunic skirt over the hips."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    dark = col.get("dark", FELD["dark"])
    o = []
    o.append(_ln([X(0.0, 0.46), X(0.0, yB)], k.c(dark), 0.014))
    for y in (0.54, 0.68, 0.82, 0.96, 1.10):
        if y > yB - 0.20:
            break
        o.append(_circ(X(0.02, y), 0.016, k.c("#9aa092"), k, 0.006))
    for s in (-1, 1):
        o.append(_pocket(k, X, s * 0.56 * hw, 0.62, 0.17, 0.15, col["base"], dark, "#9aa092", scallop=True))
        o.append(_pocket(k, X, s * 0.52 * hw, yB - 0.40, 0.22, 0.19, col["base"], dark, "#9aa092", scallop=True))
    inside = "".join(o)
    yt = yB - 0.16
    hem = yB + C.get("tunic_len", 0.18)
    gr = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "fg", X, yt, hw * 0.99, hem, hw + 0.05, gr, sw=0.024, folds=((-0.12, yt + 0.06, -0.14, hem - 0.03), (0.14, yt + 0.06, 0.16, hem - 0.03)),
                    fold_col=k.c(dark))]
    yw = yB - 0.22
    ov.append(_ln([X(-hw, yw), X(hw, yw)], k.ink, 0.074))
    ov.append(_ln([X(-hw, yw), X(hw, yw)], k.c("#3a3436"), 0.052))
    bx, by = X(0.0, yw)
    ov.append('<rect x="%.4f" y="%.4f" width="0.09" height="0.075" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (bx - 0.045, by - 0.0375, k.c("#9a9c94"), k.ink))
    # collar: dark green band with pale tabs
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.084" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.47) + X(0.20, 0.40) + (k.ink,)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.47) + X(0.20, 0.40) + (k.c(FELD["collar"]),)))
    for s in (-1, 1):
        p = X(s * 0.12, 0.44)
        ov.append('<rect x="%.4f" y="%.4f" width="0.064" height="0.030" rx="0.006" fill="%s" stroke="%s" stroke-width="0.006"/>' % (p[0] - 0.032, p[1] - 0.015, k.c("#c8ccc0"), k.ink))
    return inside, "", "".join(ov)


def _cos_mariniere23(k, C, m):
    """the French cyclist: cast7's striped marinière and rope belt, plus a red neckerchief knotted at the throat."""
    X = _X(m)
    inside = C7._cos_stripe7(k, C, m)
    col = k.c(C["colors"].get("scarf", "#c8342c"))
    kx, ky = X(0.06, 0.47)
    ov = ['<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.070" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.47) + X(0.20, 0.40) + (k.ink,)),
          '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.47) + X(0.20, 0.40) + (col,))]
    for (ex, ey) in ((0.10, 0.20), (-0.02, 0.24)):
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (kx, ky, kx + ex - 0.03, ky + ey, kx + ex + 0.04, ky + ey - 0.02, col, k.ink))
    ov.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (kx, ky, col, k.ink))
    return inside, "", "".join(ov)


COSTUMES23 = {"gi23": _cos_gi23, "major23": _cos_major23, "feld23": _cos_feld23, "mariniere23": _cos_mariniere23}


# ============================================================================= face: big handlebar moustache, red face, puffed cheeks, daze, big sweat
def _moustache(k, mx, my, s=1.0):
    C = CE._CUR[0]
    if not C or C.get("moustache_style") != "major23":
        return _O23["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#8a4a2a")
    s = s * C.get("tache_scale", 1.0)

    def Q(x, y):
        return (mx + x * s, my + y * s)
    o = []
    for sd in (-1, 1):
        pts = [Q(sd * 0.02, -0.050), Q(sd * 0.16, -0.050), Q(sd * 0.30, -0.005), Q(sd * 0.42, 0.020), Q(sd * 0.52, -0.020), Q(sd * 0.57, -0.100), Q(sd * 0.53, -0.170)]
        d = _taper(pts, 0.170 * s, 0.024 * s)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, k.c(col), k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.85"/>'
                 % (Q(sd * 0.08, -0.075) + Q(sd * 0.30, -0.030) + Q(sd * 0.48, -0.050) + (k.c(C["colors"].get("moustache_l", "#c07a4a")),)))
        k.ext.append(Q(sd * 0.58, -0.19) + (0.03,))
        k.ext.append(Q(sd * 0.42, 0.11) + (0.03,))
    return "".join(o)


def _disc_in_head_frame(P_):
    """transform that puts the head disc (drawn at translate(FC) in figure coordinates) into the face's head frame."""
    s = '<g transform="rotate(%.4f)%s">' % (-P_["head_roll"], " scale(-1 1)" if P_["mirror"] else "")
    return s


def _red_face(k, C, P_):
    ink_d, fill_d = P._head_geom(C["seed"])
    u = "%s_rf" % k.uid
    k.defs.append('<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="-0.05" cy="-0.06" r="0.56"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.68" stop-color="%s"/><stop offset="0.80" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  % (u, k.c("#f29a86"), k.c("#ec7c6a"), k.c("#d65a4e"), k.c("#d65a4e")))
    return _disc_in_head_frame(P_) + '<path d="%s" fill="url(#%s)"/></g>' % (fill_d, u)


def _cheeks(k, C, L, amt, white):
    o = []
    r = 0.13 + 0.06 * amt
    for sd, x in ((-1, L["xL"]), (1, L["xR"])):
        cx = x + sd * 0.17
        cy = L["my"] - 0.02
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (cx, cy, r, r * 0.86, white, k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.55"/>' % (cx + sd * 0.02, cy + 0.02, r * 0.55, r * 0.40, k.c("#f08a80")))
        k.ext.append((cx + sd * r, cy, 0.03))
    # pursed lips
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.034" fill="%s" stroke="%s" stroke-width="0.018"/>' % (L["mx"], L["my"] + 0.01, k.c("#8a3a3a"), k.ink))
    return "".join(o)


def _star(cx, cy, r, rot=0.0):
    pts = []
    for i in range(10):
        a = math.radians(rot - 90 + 36 * i)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return _poly_d(pts)


def _daze(k, t):
    o = []
    for i in range(3):
        a = 2 * math.pi * (t * 1.2 + i / 3.0)
        x, y = 0.50 * math.cos(a), -0.66 + 0.10 * math.sin(a)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_star(x, y, 0.075, 20 * i + 200 * t), k.c("#f4d04a"), k.ink))
        k.ext.append((x, y, 0.09))
    o.append('<ellipse cx="0" cy="-0.66" rx="0.50" ry="0.10" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.04 0.05" opacity="0.6"/>' % k.c("#fff4c0"))
    return "".join(o)


def _big_sweat(k, side):
    x, y = 0.40 * side, -0.24
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f A0.075,0.075 0 1 1 %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (x, y - 0.20, x + 0.02 * side, y - 0.10, x + 0.075, y + 0.02, x - 0.075, y + 0.02,
                                                                                         x - 0.02 * side, y - 0.10, x, y - 0.20)
    k.ext.append((x, y - 0.21, 0.03))
    k.ext.append((x, y + 0.10, 0.03))
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018"/><path d="M%.4f,%.4f q-0.03,0.04 -0.01,0.09" fill="none" stroke="#ffffff" stroke-width="0.016" '
            'stroke-linecap="round" opacity="0.9"/>' % (d, k.c("#bfe6ff"), k.c("#4a6a8a"), x - 0.02, y - 0.04))


def _face(k, C, P_, white):
    if C is None or not C.get("_cast23"):
        return _O23["_face"](k, C, P_, white)
    puff = _POSE23.get("puff", 0)
    Pf = P_
    if puff:
        Pf = dict(P_, mouth="none")
    svg, L = _O23["_face"](k, C, Pf, white)
    under, over = [], []
    if _POSE23.get("red"):
        under.append(_red_face(k, C, P_))
    if puff:
        over.append(_cheeks(k, C, L, 1.0 if puff >= 2 else 0.5, white if not _POSE23.get("red") else k.c("#ee8676")))
    if _POSE23.get("bigsweat"):
        over.append(_big_sweat(k, 1.0 if P_["yaw"] >= -0.05 else -1.0))
    if _POSE23.get("daze"):
        over.append(_daze(k, _POSE23.get("t", 0.0)))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


# ============================================================================= hands: white paint
def _hand(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    out = _O23["_hand"](k, H, dirv, shape, hr, fold)
    C = CE._CUR[0]
    if not C or not (C.get("paint_hands23") or _POSE23.get("paint_hands")):
        return out
    x, y = H
    w = k.c(WHITE_P["base"])
    return out + ('<path d="M%.4f,%.4f q0.03,-0.02 0.05,0.01 q0.01,0.03 -0.02,0.04 q-0.04,0.0 -0.03,-0.05 Z" fill="%s"/>'
                  '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>'
                  % (x - 0.04, y - 0.01, w, x + 0.025, y + 0.03, hr * 0.32, w, x - 0.03, y + 0.035, hr * 0.18, w))


# ============================================================================= props
def _T(x, y, a=0.0, s=1.0):
    return '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (x, y, a, s)


def _brush_body(k):
    o = ['<path d="M-0.16,-0.020 L0.30,-0.024 L0.30,0.024 L-0.16,0.020 Q-0.19,0 -0.16,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(WOOD["base"]), k.ink)]
    o.append('<path d="M0.28,-0.050 L0.40,-0.060 L0.40,0.060 L0.28,0.050 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(CHROME["base"]), k.ink))
    o.append('<path d="M0.40,-0.062 L0.53,-0.070 Q0.58,-0.035 0.575,0 Q0.58,0.035 0.53,0.070 L0.40,0.062 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#7a5a3a"), k.ink))
    o.append('<path d="M0.47,-0.066 L0.53,-0.070 Q0.58,-0.035 0.575,0 Q0.58,0.035 0.53,0.070 L0.47,0.066 Q0.49,0 0.47,-0.066 Z" fill="%s"/>' % k.c(WHITE_P["base"]))
    o.append('<path d="M0.50,0.065 q0.01,0.05 -0.005,0.08" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(WHITE_P["base"]))
    return "".join(o)


def _pot_body(k):
    """a paint tin hanging from its wire bail (bail top at (0, 0)), white paint at the rim and running down the side."""
    o = ['<path d="M-0.17,0.20 Q0,-0.08 0.17,0.20" fill="none" stroke="%s" stroke-width="0.016"/>' % k.ink]
    gr = _g(k, "pt", CHROME, -0.18, 0.18)
    o.append('<path d="M-0.18,0.16 L0.18,0.16 L0.17,0.50 Q0,0.53 -0.17,0.50 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (gr, k.ink))
    o.append('<rect x="-0.17" y="0.26" width="0.34" height="0.12" fill="%s" opacity="0.85"/>' % k.c("#5a7ab0"))
    o.append('<ellipse cx="0" cy="0.16" rx="0.18" ry="0.045" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(WHITE_P["base"]), k.ink))
    o.append('<path d="M0.08,0.17 q0.02,0.08 0.005,0.16 q-0.02,0.03 -0.03,-0.01 q0.0,-0.08 0.0,-0.13 Z" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(WHITE_P["base"]), k.c(WHITE_P["dark"])))
    return "".join(o)


def _record_body(k, spin=0.0):
    """a 16-inch transcription disc seen face-on, centre (0, 0), radius 0.55: grooves, sheen, red / cream label."""
    o = ['<circle cx="0" cy="0" r="0.55" fill="%s" stroke="%s" stroke-width="0.022"/>' % (k.c(REC["base"]), k.ink)]
    for r in (0.48, 0.41, 0.34, 0.27):
        o.append('<circle cx="0" cy="0" r="%.3f" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (r, k.c(REC["groove"])))
    a = spin * 360.0
    o.append('<g transform="rotate(%.2f)"><path d="M-0.40,-0.30 A0.50,0.50 0 0 1 0.05,-0.50" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round" opacity="0.55"/>'
             '<path d="M0.36,0.30 A0.47,0.47 0 0 1 -0.05,0.47" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.35"/></g>' % (a, k.c(REC["shine"]), k.c(REC["shine"])))
    o.append('<circle cx="0" cy="0" r="0.17" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(REC["label"]), k.ink))
    o.append('<g transform="rotate(%.2f)"><path d="M-0.10,-0.06 L0.10,-0.06 M-0.07,0.05 L0.07,0.05" stroke="%s" stroke-width="0.020" stroke-linecap="round"/></g>' % (a, k.c(REC["label2"])))
    o.append('<circle cx="0" cy="0" r="0.022" fill="%s"/>' % k.c("#e8e2d8"))
    return "".join(o)


def _handset_body(k):
    """a field telephone handset along +x centred on the grip: earpiece cup at -0.20, mouthpiece cup at +0.20 (both toward -y)."""
    c = k.c("#3a3438")
    o = ['<path d="M-0.20,-0.04 Q0,0.02 0.20,-0.04 L0.20,0.03 Q0,0.09 -0.20,0.03 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (c, k.ink)]
    for x in (-0.22, 0.22):
        o.append('<ellipse cx="%.4f" cy="-0.05" rx="0.075" ry="0.060" fill="%s" stroke="%s" stroke-width="0.016"/>' % (x, c, k.ink))
        o.append('<ellipse cx="%.4f" cy="-0.07" rx="0.040" ry="0.022" fill="%s" opacity="0.7"/>' % (x, k.c("#6a646c")))
    o.append('<path d="M0.20,0.05 q0.04,0.05 0.0,0.09 q-0.04,0.04 0.0,0.08 q0.04,0.04 0.0,0.08 q-0.04,0.04 0.01,0.10" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % c)
    return "".join(o)


def _clipboard_body(k):
    """masonite clipboard 0.46 x 0.60 (hand at its left edge middle), steel clip, a sheet with a pencil sketch of a tank."""
    o = ['<rect x="0.0" y="-0.30" width="0.46" height="0.60" rx="0.03" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#8a6440"), k.ink)]
    o.append('<rect x="0.035" y="-0.24" width="0.39" height="0.51" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#f6f2e6"), k.c("#b8b0a0")))
    o.append('<rect x="0.15" y="-0.33" width="0.16" height="0.08" rx="0.015" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(CHROME["base"]), k.ink))
    sk = k.c("#5a6a8a")
    o.append('<path d="M0.08,0.02 L0.38,0.02 L0.36,-0.05 L0.10,-0.05 Z M0.16,-0.05 Q0.18,-0.13 0.26,-0.12 Q0.30,-0.10 0.29,-0.05 M0.28,-0.09 L0.40,-0.10 '
             'M0.10,0.02 Q0.08,0.07 0.13,0.08 L0.33,0.08 Q0.38,0.07 0.36,0.02" fill="none" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % sk)
    o.append('<path d="M0.08,0.15 L0.34,0.15 M0.08,0.20 L0.28,0.20" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % sk)
    return "".join(o)


def _cigar_body(k):
    o = ['<path d="M0,-0.022 L0.20,-0.024 Q0.215,0 0.20,0.024 L0,0.022 Q-0.012,0 0,-0.022 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#7a4a2a"), k.ink)]
    o.append('<path d="M0.035,-0.023 L0.035,0.023" stroke="%s" stroke-width="0.018"/>' % k.c("#c9a24a"))
    o.append('<path d="M0.17,-0.024 L0.205,-0.024 Q0.22,0 0.205,0.024 L0.17,0.024 Z" fill="%s"/>' % k.c("#9c9496"))
    o.append('<circle cx="0.212" cy="0" r="0.011" fill="%s"/>' % k.c("#ff6a2a"))
    return "".join(o)


def _sausage_body(k):
    o = ['<path d="M0,-0.045 Q0.16,-0.075 0.30,-0.035 Q0.34,0 0.30,0.035 Q0.16,0.075 0,0.045 Q-0.035,0 0,-0.045 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#c86a52"), k.ink)]
    o.append('<path d="M0.05,-0.030 Q0.16,-0.050 0.27,-0.022" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>')
    o.append('<path d="M0.09,-0.05 L0.10,0.05 M0.20,-0.05 L0.21,0.05" stroke="%s" stroke-width="0.007" opacity="0.6"/>' % k.c("#8a3a2a"))
    return "".join(o)


def _chalk_body(k):
    return '<rect x="0.0" y="-0.016" width="0.13" height="0.032" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#f6f4ee"), k.ink)


def _pin_body(k):
    o = ['<path d="M0,-0.008 L0.26,0 L0,0.008 Z" fill="%s" stroke="%s" stroke-width="0.006" stroke-linejoin="round"/>' % (k.c(CHROME["light"]), k.ink)]
    o.append('<circle cx="0.0" cy="0" r="0.035" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#d9483c"), k.ink))
    o.append('<path d="M0.29,-0.05 L0.31,-0.02 M0.33,0 L0.37,0 M0.29,0.05 L0.31,0.02" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % k.c("#fff4b0"))
    return "".join(o)


def _rag_body(k):
    d = P._smooth_closed([(-0.06, -0.09), (0.08, -0.10), (0.14, -0.02), (0.11, 0.09), (0.0, 0.12), (-0.10, 0.06), (-0.12, -0.02)])
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014"/><path d="M-0.05,-0.02 Q0.02,0.01 0.08,-0.04 M-0.04,0.05 Q0.03,0.04 0.07,0.06" fill="none" stroke="%s" stroke-width="0.008"/>'
            % (d, k.c("#e6dcc4"), k.ink, k.c("#a89a80")))


def _stencil_body(k):
    """a card stencil 0.56 x 0.42 held at its left edge with a cut-out shield badge."""
    o = ['<rect x="0.0" y="-0.21" width="0.56" height="0.42" rx="0.02" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#d8c49a"), k.ink)]
    o.append('<path d="M0.18,-0.12 L0.38,-0.12 L0.38,0.02 Q0.38,0.12 0.28,0.15 Q0.18,0.12 0.18,0.02 Z" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#5a4a38"), k.ink))
    o.append('<path d="M0.20,0.10 q0.0,0.06 -0.01,0.10" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.c(WHITE_P["base"]))
    return "".join(o)


def _oar_body(k):
    """a canoe paddle along +x: T-grip at -0.25, shaft, blade 0.95 .. 1.45."""
    o = ['<path d="M-0.25,-0.065 L-0.20,-0.065 L-0.20,0.065 L-0.25,0.065 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(WOOD["base"]), k.ink)]
    o.append('<path d="M-0.20,-0.022 L1.00,-0.022 L1.00,0.022 L-0.20,0.022 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(WOOD["base"]), k.ink))
    o.append('<path d="M0.95,-0.03 Q1.05,-0.10 1.30,-0.10 Q1.46,-0.08 1.46,0 Q1.46,0.08 1.30,0.10 Q1.05,0.10 0.95,0.03 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(WOOD["light"]), k.ink))
    o.append('<path d="M1.00,0 L1.40,0" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % k.c(WOOD["dark"]))
    return "".join(o)


NEW_PROPS23 = ("brush23", "pot23", "record23", "handset23", "clipboard23", "cigar23", "sausage23", "chalk23", "pin23", "rag23", "stencil23", "oar23")
NEW_TIP23 = {"brush23": 0.57, "pot23": 0.52, "record23": 0.5, "handset23": 0.22, "clipboard23": 0.46, "cigar23": 0.21, "sausage23": 0.32,
             "chalk23": 0.13, "pin23": 0.26, "rag23": 0.0, "stencil23": 0.56, "oar23": 1.25}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS23:
        return _O23["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    ext = []
    t = _POSE23.get("t", 0.0)
    if kind == "brush23":
        o = _T(H[0], H[1], ang, sc) + _brush_body(k) + "</g>"
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((-0.19, 0.0), (0.59, -0.08), (0.59, 0.08))]
        tp = _rot(0.57 * sc, 0.0, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
        an["brush_" + key] = tp
    elif kind == "pot23":
        o = _T(H[0], H[1], 0.0, sc) + _pot_body(k) + "</g>"
        ext = [(x * sc, y * sc) for (x, y) in ((-0.20, 0.0), (0.20, 0.0), (-0.19, 0.53), (0.19, 0.53))]
        tp = (H[0], H[1] + 0.52 * sc)
        an["pot_bottom_" + key] = tp
    elif kind == "record23":
        cx, cy = _rot(0.50 * sc, 0.0, ang)
        o = _T(H[0] + cx, H[1] + cy, 0.0, sc) + _record_body(k, _POSE23.get("spin", 0.0)) + "</g>"
        ext = [(cx + x * sc, cy + y * sc) for (x, y) in ((-0.57, 0), (0.57, 0), (0, -0.57), (0, 0.57))]
        tp = (H[0] + cx, H[1] + cy)
        an["record_" + key] = tp
    elif kind == "handset23":
        o = _T(H[0], H[1], ang, sc) + _handset_body(k) + "</g>"
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((-0.30, -0.10), (0.30, -0.10), (0.25, 0.45))]
        e = _rot(-0.22 * sc, -0.05 * sc, ang)
        an["earpiece_" + key] = (H[0] + e[0], H[1] + e[1])
        tp = _rot(0.22 * sc, -0.05 * sc, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
    elif kind == "clipboard23":
        o = _T(H[0], H[1], ang, sc) + _clipboard_body(k) + "</g>"
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((0, -0.34), (0.47, -0.34), (0.47, 0.31), (0, 0.31))]
        tp = _rot(0.46 * sc, 0.0, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
        c = _rot(0.23 * sc, 0.0, ang)
        an["clipboard_" + key] = (H[0] + c[0], H[1] + c[1])
    elif kind == "stencil23":
        o = _T(H[0], H[1], ang, sc) + _stencil_body(k) + "</g>"
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((0, -0.22), (0.57, -0.22), (0.57, 0.22), (0, 0.22))]
        tp = _rot(0.28 * sc, 0.0, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
        an["stencil_" + key] = tp
    elif kind == "oar23":
        o = _T(H[0], H[1], ang, sc) + _oar_body(k) + "</g>"
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((-0.27, 0.0), (1.47, -0.11), (1.47, 0.11))]
        tp = _rot(1.25 * sc, 0.0, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
        g = _rot(0.62 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + g[0], H[1] + g[1])
        an["blade_" + key] = tp
    elif kind == "rag23":
        o = _T(H[0], H[1], 0.0, sc) + _rag_body(k) + "</g>"
        ext = [(-0.13 * sc, -0.11 * sc), (0.15 * sc, 0.13 * sc)]
        tp = H
    else:
        body = {"cigar23": _cigar_body, "sausage23": _sausage_body, "chalk23": _chalk_body, "pin23": _pin_body}[kind](k)
        o = _T(H[0], H[1], ang, sc) + body + "</g>"
        L = NEW_TIP23[kind]
        ext = [_rot(x * sc, y * sc, ang) for (x, y) in ((-0.04, -0.05), (L + 0.12, -0.06), (L + 0.12, 0.06))]
        tp = _rot(L * sc, 0.0, ang)
        tp = (H[0] + tp[0], H[1] + tp[1])
        an[kind.replace("23", "") + "_" + key] = tp
        if kind == "cigar23":
            o += ('<path d="M%.4f,%.4f q0.04,-0.06 0,-0.12 q-0.04,-0.06 0,-0.12" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.55" transform="translate(%.4f 0)"/>'
                  % (tp[0], tp[1] - 0.02, k.c("#ece6ee"), 0.02 * math.sin(6.28 * t)))
            ext.append((tp[0] - H[0], tp[1] - H[1] - 0.27))
    for (x, y) in ext:
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    return o, tp


# ============================================================================= pose keys
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    h = g("hat23")
    _POSE23["hat"] = h if h in ("m1", "overseas", "bare", "m43") else None
    ph = g("phones23")
    _POSE23["phones"] = None if ph is None or isinstance(ph, (str, list, dict)) else bool(ph)
    _POSE23["red"] = bool(g("red23")) and not isinstance(g("red23"), (str, list, dict))
    pf = g("puff23")
    _POSE23["puff"] = 0 if pf is None or isinstance(pf, (str, bool, list, dict)) else int(round(_f(pf, 0.0, 0.0, 2.0)))
    _POSE23["daze"] = bool(g("daze23")) and not isinstance(g("daze23"), (str, list, dict))
    _POSE23["bigsweat"] = bool(g("bigsweat23")) and not isinstance(g("bigsweat23"), (str, list, dict))
    _POSE23["paint_hands"] = bool(g("paint_hands23")) and not isinstance(g("paint_hands23"), (str, list, dict))
    _POSE23["spin"] = _f(g("spin23"), 0.0, -1e6, 1e6)
    t = _num(g("t"), 0.0)
    _POSE23["t"] = t if math.isfinite(t) else 0.0
    return _O23["_norm"](C, pose)


# ============================================================================= figure-level pieces: bicycle, pump, crate, balloon
def _unmir(an, mir):
    """anchors of the drawn figure -> unmirrored figure coordinates (x negated, r/l swapped back)."""
    if not mir:
        return dict(an)
    out = {}
    for n, v in an.items():
        if n.endswith("_r"):
            n = n[:-2] + "_l"
        elif n.endswith("_l"):
            n = n[:-2] + "_r"
        out[n] = (-v[0], v[1])
    return out


WHEEL_R = 0.62
CRANK = 0.24


def bike_geom(hip, leg):
    """the bicycle in unmirrored figure coordinates from the rider's hip point and leg length (D): dict of points (saddle, bb,
    rear / front axle, head tube, grip, basket, ground y).  The bike faces +x."""
    hx, hy = hip
    bb = (hx + 0.18, hy + leg - 0.30)
    ground = bb[1] + 0.48
    ra = (bb[0] - 0.80, ground - WHEEL_R)
    fa = (bb[0] + 1.05, ground - WHEEL_R)
    saddle = (hx - 0.02, hy + 0.10)
    ht = (fa[0] - 0.22, saddle[1] + 0.04)
    grip = (ht[0] - 0.24, ht[1] - 0.30)
    return dict(saddle=saddle, bb=bb, ground=ground, ra=ra, fa=fa, ht=ht, ht_lo=(fa[0] - 0.16, ht[1] + 0.20), grip=grip, stem=(ht[0] + 0.02, ht[1] - 0.26),
                basket=(fa[0] + 0.02, ht[1] - 0.10))


def pedal_pos(geom, phase, side):
    """pedal (foot) position for crank phase 0..1; side 'r' (near) or 'l' (far, opposite crank)."""
    a = 2 * math.pi * phase + (0.0 if side == "r" else math.pi)
    bx, by = geom["bb"]
    return (bx + CRANK * math.cos(a), by + CRANK * math.sin(a) - 0.02)


def _wheel(k, c, r, spin, tyre=TYRE):
    o = ['<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.075"/>' % (c[0], c[1], r - 0.035, k.ink)]
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.050"/>' % (c[0], c[1], r - 0.035, k.c(tyre)))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.016"/>' % (c[0], c[1], r - 0.085, k.c(CHROME["base"])))
    sp = []
    for i in range(8):
        a = 2 * math.pi * (spin + i / 8.0)
        sp.append("M%.4f,%.4f L%.4f,%.4f" % (c[0], c[1], c[0] + (r - 0.09) * math.cos(a), c[1] + (r - 0.09) * math.sin(a)))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" opacity="0.85"/>' % ("".join(sp), k.c(CHROME["dark"])))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.040" fill="%s" stroke="%s" stroke-width="0.010"/>' % (c[0], c[1], k.c(CHROME["base"]), k.ink))
    # a chalk-white mark on the tyre wall so the spin reads
    a = 2 * math.pi * spin
    o.append('<circle cx="%.4f" cy="%.4f" r="0.018" fill="%s"/>' % (c[0] + (r - 0.035) * math.cos(a), c[1] + (r - 0.035) * math.sin(a), k.c("#d8d2c8")))
    return "".join(o)


def _tube(k, a, b, col, w=0.055):
    return ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (a[0], a[1], b[0], b[1], k.ink, w + 0.026, a[0], a[1], b[0], b[1], col, w))


def _bike_back(k, G, spin, colors, basket=True, baguette=True):
    """the bicycle behind the rider: wheels, mudguards, frame, fork, handlebar, front basket with a baguette."""
    col = k.c(colors["base"])
    o = [_wheel(k, G["ra"], WHEEL_R, spin), _wheel(k, G["fa"], WHEEL_R, spin)]
    for c in (G["ra"], G["fa"]):
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>'
                 '<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>'
                 % (c[0] - WHEEL_R - 0.02, c[1] + 0.05, WHEEL_R + 0.06, WHEEL_R + 0.06, c[0] + WHEEL_R * 0.55, c[1] - WHEEL_R * 0.88, k.ink,
                    c[0] - WHEEL_R - 0.02, c[1] + 0.05, WHEEL_R + 0.06, WHEEL_R + 0.06, c[0] + WHEEL_R * 0.55, c[1] - WHEEL_R * 0.88, col))
    sd = G["saddle"]
    o.append(_tube(k, G["ra"], G["bb"], col, 0.040))
    o.append(_tube(k, G["ra"], (sd[0], sd[1] + 0.10), col, 0.040))
    o.append(_tube(k, G["bb"], (sd[0], sd[1] + 0.06), col))
    o.append(_tube(k, (sd[0] + 0.02, sd[1] + 0.14), G["ht"], col))
    o.append(_tube(k, G["bb"], G["ht_lo"], col))
    o.append(_tube(k, G["ht"], G["fa"], col, 0.045))
    o.append(_tube(k, G["ht"], G["stem"], k.c(CHROME["base"]), 0.040))
    bar = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (G["stem"][0], G["stem"][1], G["grip"][0] + 0.10, G["stem"][1] - 0.06, G["grip"][0], G["grip"][1])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
             % (bar, k.ink, bar, k.c(CHROME["base"])))
    # saddle
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
             % (sd[0] - 0.18, sd[1] + 0.02, sd[0], sd[1] - 0.06, sd[0] + 0.16, sd[1] + 0.02, sd[0], sd[1] + 0.08, sd[0] - 0.18, sd[1] + 0.02, k.c(LEATHER["base"]), k.ink))
    if basket:
        bx, by = G["basket"]
        if baguette:
            o.append('<g transform="translate(%.4f %.4f) rotate(-62)"><path d="M-0.05,-0.055 Q0.30,-0.075 0.58,-0.04 Q0.66,0 0.58,0.04 Q0.30,0.075 -0.05,0.055 Q-0.10,0 -0.05,-0.055 Z" '
                     'fill="%s" stroke="%s" stroke-width="0.016"/><path d="M0.12,-0.05 q0.04,0.05 0.08,0.0 M0.26,-0.055 q0.04,0.05 0.08,0.0 M0.40,-0.05 q0.04,0.05 0.08,0.0" '
                     'fill="none" stroke="%s" stroke-width="0.012"/></g>' % (bx - 0.02, by + 0.02, k.c(BREAD["base"]), k.ink, k.c(BREAD["light"])))
            k.ext.append((bx + 0.30, by - 0.55, 0.04))
        d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (bx - 0.20, by - 0.12, bx + 0.22, by - 0.12, bx + 0.17, by + 0.18, bx - 0.15, by + 0.18)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, k.c("#c8a060"), k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010"/>'
                 % (bx - 0.18, by - 0.02, bx + 0.20, by - 0.02, bx - 0.17, by + 0.08, bx + 0.19, by + 0.08, bx + 0.02, by - 0.12, bx + 0.01, by + 0.18, k.c("#8a6430")))
        k.ext.append((bx + 0.24, by + 0.2, 0.03))
    for c in (G["ra"], G["fa"]):
        k.ext.append((c[0], c[1], WHEEL_R + 0.06))
    return "".join(o)


def _bike_front(k, G, phase):
    """chainring and the near crank + pedal, drawn over the legs."""
    bx, by = G["bb"]
    p = pedal_pos(G, phase, "r")
    o = ['<circle cx="%.4f" cy="%.4f" r="0.13" fill="%s" stroke="%s" stroke-width="0.020"/>' % (bx, by, k.c(CHROME["base"]), k.ink)]
    o.append('<circle cx="%.4f" cy="%.4f" r="0.08" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.03 0.02"/>' % (bx, by, k.c(CHROME["dark"])))
    o.append(_tube(k, (bx, by), (p[0], p[1] + 0.02), k.c(CHROME["dark"]), 0.030))
    o.append('<rect x="%.4f" y="%.4f" width="0.14" height="0.040" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (p[0] - 0.07, p[1] + 0.03, k.c("#4a4448"), k.ink))
    return "".join(o)


def _bike_fallen(k, x0, ground, colors, spin):
    """the bicycle lying on the ground beside the fallen rider (seen from above-side: wheels as flat ellipses), front wheel spinning."""
    col = k.c(colors["base"])
    o = []
    for (cx, s) in ((x0 - 0.75, 0.0), (x0 + 0.75, spin)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.070"/>' % (cx, ground - 0.21, WHEEL_R, 0.17, k.ink))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.045"/>' % (cx, ground - 0.21, WHEEL_R, 0.17, k.c(TYRE)))
    o.append(_tube(k, (x0 - 0.75, ground - 0.21), (x0 + 0.75, ground - 0.24), col))
    o.append(_tube(k, (x0 - 0.10, ground - 0.21), (x0 + 0.55, ground - 0.34), col))
    o.append(_tube(k, (x0 + 0.55, ground - 0.34), (x0 + 0.80, ground - 0.46), k.c(CHROME["base"]), 0.040))
    for i in range(3):
        a = 2 * math.pi * (spin + i / 3.0)
        o.append('<path d="M%.4f,%.4f q0.05,-0.06 0.12,-0.03" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
                 % (x0 + 0.75 + 0.55 * math.cos(a), ground - 0.40 + 0.08 * math.sin(a), k.c("#fff6c8")))
    k.ext.append((x0 - 0.75 - WHEEL_R, ground - 0.40, 0.04))
    k.ext.append((x0 + 0.75 + WHEEL_R, ground, 0.04))
    return "".join(o)


PUMP_H = (1.30, 1.80)      # T-handle height above the soles, low .. high


def pump_geom(feet, ground, phase):
    """the hand pump in unmirrored figure coordinates: barrel foot, barrel top, T-handle centre for phase 0..1 (0 = handle high,
    0.5 = pushed down), hose end on the ground."""
    x = feet[0] + 0.72
    u = 0.5 + 0.5 * math.cos(2 * math.pi * phase)
    hy = ground - (PUMP_H[0] + (PUMP_H[1] - PUMP_H[0]) * u)
    return dict(x=x, ground=ground, top=ground - 1.05, handle=(x, hy), hose_end=(x + 1.10, ground - 0.04), u=u)


def _pump_svg(k, G, front=False):
    x, gy = G["x"], G["ground"]
    if front:
        hx, hy = G["handle"]
        return ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.090" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>'
                % (hx - 0.24, hy, hx + 0.24, hy, k.ink, hx - 0.24, hy, hx + 0.24, hy, k.c(WOOD["base"])))
    o = []
    hose = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (x + 0.10, gy - 0.12, x + 0.50, gy - 0.10, x + 0.60, gy + 0.02, G["hose_end"][0], G["hose_end"][1])
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.070" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.044" stroke-linecap="round"/>'
             % (hose, k.ink, hose, k.c("#3e3a3c")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (x - 0.30, gy, x + 0.30, gy, x + 0.26, gy - 0.06, x - 0.26, gy - 0.06, k.c(OD["dark"]), k.ink))
    hx, hy = G["handle"]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020"/>'
             % (x, G["top"], hx, hy, k.ink, x, G["top"], hx, hy, k.c(CHROME["base"])))
    gr = _g(k, "pb", OD, x - 0.10, x + 0.10)
    o.append('<rect x="%.4f" y="%.4f" width="0.20" height="%.4f" rx="0.03" fill="%s" stroke="%s" stroke-width="0.020"/>' % (x - 0.10, G["top"], gy - 0.06 - G["top"], gr, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="0.24" height="0.05" rx="0.015" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x - 0.12, G["top"] - 0.02, k.c(OD["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (x - 0.05, G["top"] + 0.06, x - 0.05, gy - 0.10, k.c(OD["light"])))
    if G["u"] < 0.35:      # pushing: a puff of air at the hose end
        ex, ey = G["hose_end"]
        o.append('<path d="M%.4f,%.4f q0.08,-0.10 0.16,-0.04 M%.4f,%.4f q0.10,0.0 0.18,0.06" fill="none" stroke="#ffffff" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
                 % (ex + 0.04, ey - 0.06, ex + 0.05, ey + 0.0))
    for p in ((x - 0.31, gy), (hx - 0.26, hy - 0.06), (hx + 0.26, hy - 0.06), (G["hose_end"][0] + 0.25, gy - 0.12)):
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o)


def _crate_svg(k, x0, y0, x1, y1, lid=True):
    """a wooden crate face (rectangle (x0, y0) .. (x1, y1)) with slats, corner battens and a stencilled star."""
    gr = _g(k, "cr%d" % len(k.defs), CRATE, x0, x1)
    o = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.02" fill="%s" stroke="%s" stroke-width="0.024"/>' % (x0, y0, x1 - x0, y1 - y0, gr, k.ink)]
    n = max(2, int(round((y1 - y0) / 0.20)))
    for i in range(1, n):
        y = y0 + (y1 - y0) * i / n
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (x0 + 0.02, y, x1 - 0.02, y, k.c(CRATE["dark"])))
    for x in (x0 + 0.05, x1 - 0.05):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.050"/>' % (x, y0 + 0.02, x, y1 - 0.02, k.c(CRATE["dark"])))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    o.append('<path d="%s" fill="%s" opacity="0.85"/>' % (_star(cx, cy, min(x1 - x0, y1 - y0) * 0.25), k.c(CRATE["stencil"])))
    k.ext.append((x0, y0, 0.02))
    k.ext.append((x1, y1, 0.02))
    return "".join(o)


def balloon_svg(uid="bl", size=1.0, color=None, angle=0.0, pop=0, ink=P.INK, tint=None):
    """a party balloon, neck at (0, 0), body along `angle` (deg, 0 = +x), size 0..1 (radius 0.06 .. 0.46 D).  pop=1 draws the
    burst (a star of jagged bits and rubber shreds) instead.  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    s = _balloon(k, (0.0, 0.0), size, color or BALLOON_COLS[0], angle, pop)
    x0 = min(e[0] - e[2] for e in k.ext)
    y0 = min(e[1] - e[2] for e in k.ext)
    x1 = max(e[0] + e[2] for e in k.ext)
    y1 = max(e[1] + e[2] for e in k.ext)
    return '<g><defs>%s</defs>%s</g>' % ("".join(k.defs), s), (x0, y0, x1, y1)


def _balloon(k, neck, size, color, angle, pop=0):
    r = 0.06 + 0.40 * _clamp(size, 0.0, 1.0)
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    cx, cy = neck[0] + ca * (r * 1.05 + 0.04), neck[1] + sa * (r * 1.05 + 0.04)
    if pop:
        o = []
        for i in range(10):
            a = 2 * math.pi * i / 10
            rr = r * (1.25 if i % 2 == 0 else 0.7)
            o.append("%.4f,%.4f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
        k.ext.append((cx, cy, r * 1.3))
        return ('<path d="M%s Z" fill="#fff6c8" stroke="%s" stroke-width="0.016" opacity="0.95"/>' % (" L".join(o), k.ink) +
                "".join('<path d="M%.4f,%.4f q0.03,0.04 0.0,0.08" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>'
                        % (cx + r * 0.9 * math.cos(2.3 * i), cy + r * 0.9 * math.sin(2.3 * i), k.c(color)) for i in range(4)))
    rx, ry = r * 1.10, r
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f)">' % (cx, cy, angle)]
    o.append('<path d="M%.4f,0 L%.4f,-0.035 L%.4f,0.035 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (-rx - 0.03, -rx + 0.02, -rx + 0.02, k.c(color), k.ink))
    o.append('<ellipse cx="0" cy="0" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (rx, ry, k.c(color), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#ffffff" opacity="0.55" transform="rotate(-25 %.4f %.4f)"/>' % (rx * 0.30, -ry * 0.42, rx * 0.26, ry * 0.13, rx * 0.30, -ry * 0.42))
    o.append('</g>')
    k.ext.append((cx, cy, max(rx, ry) + 0.03))
    return "".join(o)


def _redraw_hand(k, h, lw):
    hr = P.HAND_R * (lw / P.LW) ** 0.75
    return '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/><ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#b7a9b3" opacity="0.7"/>' % (
        h[0], h[1], hr, k.ink, h[0] - 0.34 * hr, h[1] - 0.40 * hr, 0.15 * hr, 0.095 * hr)


def _bbox_of(ext):
    return (min(e[0] - e[2] for e in ext), min(e[1] - e[2] for e in ext), max(e[0] + e[2] for e in ext), max(e[1] + e[2] for e in ext))


def figure(cast_name, pose=None, uid="p"):
    rk = pose.get("reach23") if isinstance(pose, dict) else None
    if isinstance(rk, (int, float)) and not isinstance(rk, bool) and math.isfinite(rk) and isinstance(cast_name, str) and cast_name in P.CAST and abs(rk - 1.0) > 1e-6:
        # rubber-hose reach: the arm bones are drawn longer by reach23 (1 .. 1.6) for this one drawing (lift overhead)
        C0 = P.CAST[cast_name]
        P.CAST[cast_name] = dict(C0, arm=C0["arm"] * _clamp(float(rk), 1.0, 1.6))
        try:
            return figure(cast_name, dict(pose, reach23=None), uid)
        finally:
            P.CAST[cast_name] = C0
    f = _O23["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or not isinstance(cast_name, str) or cast_name not in P.CAST:
        return f
    bike = pose.get("bike23")
    pump = pose.get("pump23")
    if not (isinstance(pump, (int, float)) and not isinstance(pump, bool) and math.isfinite(pump)):
        pump = None
    crate = pose.get("crate23")
    bal = pose.get("balloon23")
    seat = pose.get("ground23") == "seat"
    if not (isinstance(bike, dict) or isinstance(pump, (int, float)) and not isinstance(pump, bool) or crate in ("carry", "seat") or isinstance(bal, dict) or seat):
        return f
    mir = bool(pose.get("mirror"))
    sgn = -1.0 if mir else 1.0
    an = _unmir(f["anchors"], mir)
    k = P._Ctx(uid + "x", P.INK, None)
    behind, front = [], []
    feet_y = f["feet_y"]
    feet = an["feet"]
    lw = _num(P.CAST[cast_name].get("limb_w"), P.LW)
    extra = {}
    if seat:
        # sitting on the ground: the lowest drawn point of the body is the ground contact
        feet_y = f["bbox"][3] - 0.035
        feet = (feet[0], feet_y)
    if isinstance(bike, dict):
        bc = bike.get("color", "green")
        cols = BIKE_COLS.get(bc, BIKE_COLS["green"]) if isinstance(bc, str) else BIKE_COLS["green"]
        state = bike.get("state", "ride")
        ph = _num(bike.get("phase"), 0.0)
        if state == "fallen":
            behind.append(_bike_fallen(k, feet[0] + 0.30, feet_y, cols, ph))
        else:
            G = bike_geom(an["hip"], P.CAST[cast_name]["leg"])
            behind.append(_bike_back(k, G, -ph * 0.55, cols, bike.get("basket", True), bike.get("baguette", True)))
            front.append(_bike_front(k, G, ph))
            feet_y = G["ground"]
            feet = ((G["ra"][0] + G["fa"][0]) / 2, G["ground"])
            extra.update(bike_rear=(G["ra"][0], G["ground"]), bike_front=(G["fa"][0], G["ground"]), basket=G["basket"], grip=G["grip"])
    if isinstance(pump, (int, float)) and not isinstance(pump, bool):
        G = pump_geom(feet, feet_y, float(pump))
        behind.append(_pump_svg(k, G))
        front.append(_pump_svg(k, G, front=True))
        for h in ("hand_r", "hand_l"):
            front.append(_redraw_hand(k, an[h], lw))
        extra["hose_end"] = G["hose_end"]
        extra["pump_handle"] = G["handle"]
    if crate == "carry":
        hr, hl = an["hand_r"], an["hand_l"]
        cx, cy = (hr[0] + hl[0]) / 2, (hr[1] + hl[1]) / 2
        w = max(0.75, abs(hr[0] - hl[0]) - 0.02)
        front.append(_crate_svg(k, cx - w / 2, cy - 0.30, cx + w / 2, cy + 0.26))
        for h in (hr, hl):
            front.append(_redraw_hand(k, h, lw))
        extra["crate"] = (cx, cy)
    elif crate == "seat":
        hip = an["hip"]
        x0 = hip[0] - 0.80
        behind.append(_crate_svg(k, x0, hip[1] - 0.04, x0 + 1.45, feet_y))
        extra["crate_top"] = (hip[0], hip[1] + 0.02)
    if isinstance(bal, dict):
        mo = an["mouth"]
        yaw = _num(pose.get("yaw"), 0.0)
        side = 1.0 if yaw >= 0 else -1.0
        neck = (mo[0] + side * 0.05, mo[1] + 0.01)
        front.append(_balloon(k, neck, _num(bal.get("size"), 0.5), bal.get("color") if P._is_hex(bal.get("color")) else BALLOON_COLS[0], 90.0 - 90.0 * side + side * _num(bal.get("tilt"), -8.0), int(_num(bal.get("pop"), 0))))
        extra["balloon_neck"] = neck
    # assemble in the unmirrored frame, then mirror the extra pieces like the figure
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    wrap0 = '<g transform="scale(-1 1)">' if mir else "<g>"
    svg = defs + wrap0 + "".join(behind) + "</g>" + f["svg"] + wrap0 + "".join(front) + "</g>"
    b = list(f["bbox"])
    if k.ext:
        e = _bbox_of(k.ext)
        if mir:
            e = (-e[2], e[1], -e[0], e[3])
        b = [min(b[0], e[0]), min(b[1], e[1]), max(b[2], e[2]), max(b[3], e[3])]
    a2 = dict(f["anchors"])
    for n, v in extra.items():
        a2[n] = (sgn * v[0], v[1])
    a2["feet"] = (sgn * feet[0], feet_y)
    a2["ground"] = a2["feet"]
    return dict(f, svg=svg, bbox=tuple(b), anchors=a2, feet_y=feet_y)


# ============================================================================= cast
_FLAGS = dict(_cast23=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)
PROF_REG = CE.PROFILE_REGULAR
PROF_ATH = CE.PROFILE_ATHLETE
PROF_PEAR = CE.PROFILE_PEAR
PROF_ROUND = C2.PROFILE_ROUND


def _gi(seed, build="regular", tw=0.80, th=0.98, prof=None, leg=1.20, limb=0.060, hat="m1", hair="#5a3a26", jacket=None, extra=None, sleeve_roll=False):
    jc = jacket or JACKET
    d = dict(_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=prof or PROF_REG, shift_pow=1.0,
             shoulder=(0.28 if build != "stout" else 0.38, 0.48), arm=0.74, hip_x=0.15, leg=leg, stance=0.06, wide=0.26, limb_w=limb,
             eye_y=0.035, brow="stroke", brow_th=0.054, mouth="dash", moustache=False, smirk_side=1, cheeks="#eca08a",
             hat="newsboy", hat_style="gi23", hat23=hat, hat_tilt=-2.0, ear_pencil=False, helmet_colors=OD,
             hair=dict(color=hair, front=0.08, grow=0.20),
             costume="gi23",
             sleeve=dict(color=jc["base"], dark=jc["dark"], cuff=jc["light"] if sleeve_roll else jc["dark"], len=0.50 if sleeve_roll else 0.84, w=0.16, roll=sleeve_roll),
             shorts=dict(color=PANTS_OD["base"], dark=PANTS_OD["dark"], cuff=PANTS_OD["base"], len=0.84, w=0.13),
             boots=dict(color="#5a3c26", cuff="#b5a674", h=0.16, toe=0.15),
             colors=dict(base=jc["base"], dark=jc["dark"], collar=jc["light"], pocket=jc["base"], shirt="#5e5a3a", pants=PANTS_OD["base"]))
    if extra:
        d.update(extra)
    return d


NEW_CAST23 = {
    # 6+ distinct Ghost Army faces (heights 2.9 .. 3.3 D): role variants carry their props in the story poses
    # painter: lanky, overseas cap, ginger hair, freckles, white paint on the hands
    "gi_painter": _gi(231.4, "slim", 0.66, 1.00, PROF_ATH, 1.30, 0.056, "overseas", "#b8602e", sleeve_roll=True,
                      extra=dict(freckles=True, cheeks="#f2a08e", paint_hands23=True, brow="dome", brow_th=0.040, eye_y=0.05, hat_tilt=-9.0)),
    # sound man: round face, bare head with headphones over dark curly hair, small moustache
    "gi_sound": _gi(232.7, "regular", 0.86, 0.96, PROF_PEAR, 1.10, 0.062, "bare", "#2a2024",
                    extra=dict(phones23=True, pencil_moustache=True, colors=dict(base=JACKET["base"], dark=JACKET["dark"], collar=JACKET["light"], pocket=JACKET["base"], shirt="#5e5a3a", pants=PANTS_OD["base"], moustache="#2a2024"),
                               hair=dict(color="#2a2024", front=0.10, grow=0.22))),
    # radio man: M1 helmet, square jaw (stout-ish), radio pack with antenna on the back, heavy brows
    "gi_radio": _gi(233.9, "regular", 0.84, 1.02, PROF_REG, 1.20, 0.062, "m1", "#3a2a20", extra=dict(pack23=True, brow_th=0.070, mouth="frown")),
    # pump man: stocky, M1 helmet, sleeves rolled, ruddy, bushy moustache
    "gi_pump": _gi(234.2, "stout", 1.00, 0.94, PROF_PEAR, 1.04, 0.068, "m1", "#4a3022", sleeve_roll=True,
                   extra=dict(moustache=True, moustache_style="bushy", tache_scale=0.80, cheeks="#ee8a74", eye_y=0.01,
                              colors=dict(base=JACKET["base"], dark=JACKET["dark"], collar=JACKET["light"], pocket=JACKET["base"], shirt="#5e5a3a", pants=PANTS_OD["base"], moustache="#4a3022", moustache_l="#7a5a44"))),
    # clipboard designer: thin, round glasses, overseas cap, neat dark hair
    "gi_designer": _gi(235.6, "slim", 0.62, 1.02, PROF_ATH, 1.28, 0.054, "overseas", "#1e1a1e", extra=dict(glasses=True, brow_th=0.044, mouth="smirk", hat_tilt=6.0)),
    # the dry smiler ("แข็งแรงมาก"): big friendly lad, M1 helmet, wide face, blond
    "gi_smile": _gi(236.3, "regular", 0.92, 1.00, PROF_REG, 1.24, 0.064, "m1", "#d8b060", extra=dict(cheeks="#f4948a", eye_y=0.05, eye_scale=1.10, hair=dict(color="#d8b060", front=0.14, grow=0.22))),
    # the Major's driver: wiry, M1 helmet, a long nose look via pencil moustache, freckles off; dark eyebrows
    "gi_driver": _gi(237.8, "slim", 0.70, 0.96, PROF_ATH, 1.18, 0.058, "m1", "#6a4a30", extra=dict(age_lines=True, brow_th=0.066, mouth="frown", pencil_moustache=True, eye_y=0.02,
                                                                             colors=dict(base=JACKET["base"], dark=JACKET["dark"], collar=JACKET["light"], pocket=JACKET["base"], shirt="#5e5a3a", pants=PANTS_OD["base"], moustache="#5a3a24"))),
    # the Major (invented mocker): stout, khaki + Sam Browne, peaked cap, huge ginger-brown handlebar moustache, cigar
    "major": dict(
        _FLAGS, build="stout", seed=238.5, cigar_ok=True,
        torso_w=1.46, torso_h=1.26, profile=PROF_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.80, hip_x=0.20, leg=1.30, stance=0.07, wide=0.32, limb_w=0.070,
        eye_y=0.0, brow="stroke", brow_th=0.088, mouth="frown", moustache=True, moustache_style="major23", tache_scale=1.05,
        smirk_side=1, cheeks="#ee7a68", chins=True,
        hat="newsboy", hat_style="peaked10", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(crown="#8a7c52", crown_l="#b0a274", crown_d="#5e5434", band="#5a4a30", visor="#5a3622", visor_l="#9a6440", badge="#e2b442", badge_c="#e2b442"),
        hair=dict(color="#9a5a34", front=0.06, grow=0.20),
        costume="major23", tunic_len=0.22,
        sleeve=dict(color=KHAKI["base"], dark=KHAKI["dark"], cuff=KHAKI["dark"], len=0.84, w=0.21),
        shorts=dict(color="#cdb894", dark="#a08c66", cuff="#cdb894", len=0.62, w=0.16),
        boots=dict(color="#5a3420", cuff="#7a4a2c", h=0.46, toe=0.18),
        colors=dict(base=KHAKI["base"], dark=KHAKI["dark"], lapel=KHAKI["light"], shirt="#d8c49a", tie="#5a4630", pants="#cdb894", moustache="#8a4a2a", moustache_l="#c07a4a"),
    ),
    # the French cyclists: beret + marinière (+ red neckerchief), flat cap + waistcoat
    "fr_beret": dict(
        _FLAGS, build="regular", seed=239.1,
        torso_w=0.80, torso_h=0.94, profile=PROF_REG, shift_pow=1.05,
        shoulder=(0.30, 0.48), arm=0.72, hip_x=0.16, leg=1.16, stance=0.07, wide=0.27, limb_w=0.060,
        eye_y=0.05, brow="stroke", brow_th=0.054, mouth="smile", moustache=True, moustache_style="handlebar", tache_scale=0.72, smirk_side=1, cheeks="#f0a08a",
        hat="newsboy", hat_style="beret7", hat_tilt=-10.0, ear_pencil=False, beret_side=1,
        hat_colors=dict(base="#2a3456", dark="#161c34", light="#4a5880", shine="#6a78a0"),
        hair=dict(color="#2a2024", front=0.08, grow=0.20),
        costume="mariniere23",
        sleeve=dict(color="#f6f4ee", cuff="#1e2a5a", dark="#c8c8d0", len=0.55, w=0.15),
        shorts=dict(color="#5a6888", dark="#3a4664", cuff="#5a6888", len=0.88, w=0.13),
        boots=dict(color="#5a3a26", cuff="#5a3a26", h=0.06, toe=0.14, soft=True),
        colors=dict(base="#f6f4ee", dark="#c8c8d0", stripe="#1e2a5a", pants="#5a6888", rope="#c8a46a", scarf="#c8342c", moustache="#2a2024", moustache_l="#6a5a60"),
    ),
    "fr_cap": dict(
        _FLAGS, build="slim", seed=240.6,
        torso_w=0.70, torso_h=0.94, profile=PROF_REG, shift_pow=1.0,
        shoulder=(0.27, 0.48), arm=0.72, hip_x=0.15, leg=1.24, stance=0.07, wide=0.26, limb_w=0.058,
        eye_y=0.04, brow="stroke", brow_th=0.058, mouth="dash", moustache=False, smirk_side=-1, cheeks="#eca08a", age_lines=True,
        hat="newsboy", hat_style="flatnews", hat_tilt=4.0, ear_pencil=False, cap_puff=0.7,
        hat_colors=dict(base="#7a6a52", dark="#4e4232", light="#9e8c70", shine="#b8a88a", visor="#5e5040"),
        hair=dict(color="#4a3a30", front=0.09, grow=0.22),
        costume="foreman",
        sleeve=dict(color="#efe6d2", cuff="#f8f2e4", dark="#c8bca4", len=0.48, w=0.15, roll=True),
        shorts=dict(color="#6a5a44", dark="#46382a", cuff="#6a5a44", len=0.88, w=0.12),
        boots=dict(color="#3a2a22", cuff="#3a2a22", h=0.08, toe=0.14),
        colors=dict(base="#efe6d2", brass="#c9a44a", button="#c8b890", pants="#6a5a44", shirt_d="#cfc4ae", vest="#5a6a5a", vest_d="#3a4a3e"),
    ),
    # two German observers: grey field cap, grey tunic, binoculars, comic (never armed)
    "ger_tall": dict(
        _FLAGS, build="slim", seed=241.2,
        torso_w=0.70, torso_h=1.04, profile=PROF_ATH, shift_pow=1.0,
        shoulder=(0.27, 0.49), arm=0.76, hip_x=0.15, leg=1.36, stance=0.06, wide=0.26, limb_w=0.058,
        eye_y=0.03, brow="stroke", brow_th=0.060, mouth="dash", moustache=False, smirk_side=1, cheeks="#e8a08a",
        hat="newsboy", hat_style="gi23", hat23="m43", hat_tilt=-3.0, ear_pencil=False,
        cap_colors=dict(light=FELD["light"], base=FELD["base"], dark=FELD["dark"]),
        hair=dict(color="#c8a870", front=0.06, grow=0.20),
        costume="feld23", tunic_len=0.20,
        sleeve=dict(color=FELD["base"], dark=FELD["dark"], cuff=FELD["dark"], len=0.84, w=0.15),
        shorts=dict(color="#6e7468", dark="#4e5448", cuff="#6e7468", len=0.62, w=0.13),
        boots=dict(color="#2e2a2c", cuff="#2e2a2c", h=0.40, toe=0.15),
        colors=dict(base=FELD["base"], dark=FELD["dark"], pants="#6e7468"),
    ),
    "ger_round": dict(
        _FLAGS, build="stout", seed=242.9,
        torso_w=1.10, torso_h=1.00, profile=PROF_PEAR, shift_pow=1.15,
        shoulder=(0.36, 0.46), arm=0.72, hip_x=0.17, leg=1.04, stance=0.06, wide=0.28, limb_w=0.066,
        eye_y=0.01, brow="stroke", brow_th=0.066, mouth="dash", moustache=True, moustache_style="walrus", smirk_side=-1, cheeks="#f08a78", chins=True,
        hat="newsboy", hat_style="gi23", hat23="m43", hat_tilt=5.0, ear_pencil=False,
        cap_colors=dict(light=FELD["light"], base=FELD["base"], dark=FELD["dark"]),
        hair=dict(color="#5a4a3a", front=0.06, grow=0.20),
        costume="feld23", tunic_len=0.18,
        sleeve=dict(color=FELD["base"], dark=FELD["dark"], cuff=FELD["dark"], len=0.84, w=0.17),
        shorts=dict(color="#6e7468", dark="#4e5448", cuff="#6e7468", len=0.60, w=0.15),
        boots=dict(color="#2e2a2c", cuff="#2e2a2c", h=0.36, toe=0.16),
        colors=dict(base=FELD["base"], dark=FELD["dark"], pants="#6e7468", moustache="#6a5a48"),
    ),
}
GI23 = ("gi_painter", "gi_sound", "gi_radio", "gi_pump", "gi_designer", "gi_smile", "gi_driver")
NEW23 = GI23 + ("major", "fr_beret", "fr_cap", "ger_tall", "ger_round")

# feet-relative sprite canvases (x0, y0, x1, y1), D, y down; filled in by register() from CANVAS23_TABLE (measured by test_cast23.py canvas)
CANVAS23_TABLE = {}
CANVAS23_WIDE = {}          # the same members with a wide canvas for the bicycle, pump, balloon and crate poses


# ============================================================================= cycles and builders
LIFT_REACH = 1.60     # lifters' arms are drawn 1.6 x longer (rubber hose) so the hands clear the helmets
LIFT_H = 3.45          # height of the TOP of the lifters' hands above the soles (D): the tank's track bottoms rest here


def _hr(cast):
    lw = _num(P.CAST[cast].get("limb_w"), P.LW)
    return P.HAND_R * (lw / P.LW) ** 0.75


def lift_pose(cast, t=0.0, lift_h=LIFT_H, expr="determined", mouth=None, strain=1.0):
    """arms straight up, palms flat under an object held overhead: the TOP of both hands sits exactly lift_h D above the soles
    for every member (the legs bend or straighten to make it fit), so four lifters line up under one tank.  t animates a small
    strain wobble (0.06 D) that keeps the hand height fixed.  Anchors lift_r / lift_l = the hand tops (the object's underside)."""
    wob = math.sin(2 * math.pi * t)
    base = dict(yaw=0.25, pitch=-0.6, expr=expr, head_dy=0.10 * strain, reach23=LIFT_REACH, head_roll=2.0 * wob, fx=["sweat"] if strain > 0.5 else [], t=t)
    if mouth is not None:
        base["mouth"] = mouth
    hr = _hr(cast)
    lo, hi = 0.0, 0.70
    best = None
    for _ in range(18):
        cr = (lo + hi) / 2
        p = dict(base, legs=dict(preset="wide", crouch=cr, spread=0.12))
        fy = P.figure(cast, p, "q")["feet_y"]
        hy = fy - lift_h + hr              # hand centre y (local)
        sx = P.CAST[cast]["shoulder"][0]
        sy = P.CAST[cast]["shoulder"][1] - p["head_dy"]
        reach = math.hypot(0.40 - sx, hy - sy)
        best = (p, hy)
        if reach > P.CAST[cast]["arm"] * LIFT_REACH * 1.28:
            hi = cr          # too far: less crouch brings the hands' target closer
        else:
            lo = cr
    p, hy = best
    for s, key in ((1, "r"), (-1, "l")):
        p["arm_" + key] = dict(hand=(s * 0.42 + 0.01 * wob, hy), bend=-0.25 * s, stretch=1.30, shape="open", layer="front")
    return p


def lift_anchors(cast, pose):
    """(lift_r, lift_l): the hand tops of a lift_pose in local D (the object's underside)."""
    f = P.figure(cast, pose, "q")
    hr = _hr(cast)
    return tuple((f["anchors"][h][0], f["anchors"][h][1] - hr) for h in ("hand_r", "hand_l"))


def pump_frame(cast="gi_pump", phase=0.0, facing=1, expr="determined"):
    """one frame of the PUMP cycle (phase 0..1, about 20 frames per stroke): the T-handle of a hand pump standing in front goes up
    and down, both hands on it, the body crouches on the push.  Anchors pump_handle, hose_end (the hose lies on the ground toward
    the facing side: put the tank valve there)."""
    u = 0.5 + 0.5 * math.cos(2 * math.pi * phase)
    p = dict(yaw=0.55, pitch=0.25 + 0.2 * (1 - u), expr=expr, lean=6 + 12 * (1 - u), head_roll=-3, legs=dict(preset="wide", crouch=0.05 + 0.22 * (1 - u)),
             fx=["sweat"] if u < 0.3 else [], mirror=facing < 0, t=phase)
    f = P.figure(cast, dict(p), "q")
    an = _unmir(f["anchors"], facing < 0)
    G = pump_geom(an["feet"], f["feet_y"], phase)
    hx, hy = G["handle"]
    p["arm_r"] = dict(hand=(hx + 0.17, hy), bend=0.5, stretch=1.3, layer="front")
    p["arm_l"] = dict(hand=(hx - 0.17, hy), bend=0.5, stretch=1.3, layer="front")
    p["pump23"] = phase
    return p


def ride_frame(cast="fr_beret", phase=0.0, facing=1, expr="happy", mouth=None, color=None, state="ride", basket=None, look=0.0):
    """one frame of PEDALLING (phase 0..1 = one crank turn, 14 frames per turn for a relaxed ride): the bicycle is drawn inside the
    sprite (wheels spin with phase, cranks turn, feet on the pedals, hands on the grips).  The sprite's ground point is the wheels'
    contact line (anchors feet / ground, bike_rear, bike_front).  state "brake": cranks frozen, rider leans back.
    look: yaw of the head toward the camera (0 = profile-ish 0.65, 1 = front)."""
    col = color or ("green" if cast == "fr_beret" else "maroon")
    basket = (cast == "fr_beret") if basket is None else basket
    brake = state == "brake"
    yaw = 0.65 - 0.55 * look
    p = dict(yaw=yaw, pitch=-0.1, expr=expr, lean=(-6 if brake else 10), head_roll=(-4 if brake else 2 * math.sin(2 * math.pi * phase)), mirror=facing < 0,
             legs=dict(preset="stand"), t=phase, bike23=dict(phase=phase, color=col, basket=basket, baguette=basket, state=state))
    if mouth is not None:
        p["mouth"] = mouth
    f = P.figure(cast, dict(p, bike23=None), "q")
    an = _unmir(f["anchors"], facing < 0)
    G = bike_geom(an["hip"], P.CAST[cast]["leg"])
    for s in ("r", "l"):
        x, y = pedal_pos(G, phase, s)
        p["legs"]["foot_" + s] = (x, y - 0.02)
        p["legs"]["knee_" + s] = 1.0
        p["legs"]["toe_" + s] = 0.8
    g = G["grip"]
    p["arm_r"] = dict(hand=(g[0] + 0.04, g[1]), bend=0.3, stretch=1.3, layer="front")
    p["arm_l"] = dict(hand=(g[0] - 0.06, g[1] + 0.02), bend=0.3, stretch=1.3, layer="back")
    if brake:
        p["fx"] = ["sweat"]
    return p


def fall_pose(cast="fr_cap", t=0.0, facing=1, color=None):
    """fallen off the bike GENTLY: sitting on the ground, legs out, hands behind, dazed stars circling (t animates them), the
    bicycle lying beside him with the front wheel spinning.  The sprite ground point is his seat (no gap, no injury)."""
    col = color or ("green" if cast == "fr_beret" else "maroon")
    f0 = P.figure(cast, dict(yaw=0.4), "q")
    hip = f0["anchors"]["hip"]
    L = P.CAST[cast]["leg"]
    hy = hip[1] + 0.10
    return dict(yaw=0.35, pitch=0.1, expr="stunned", mouth=("open", 0.10, 0.08), head_roll=-8 + 4 * math.sin(2 * math.pi * t), daze23=1, t=t, mirror=facing < 0, lean=-8,
                legs=dict(foot_r=(hip[0] + L * 0.85, hy), foot_l=(hip[0] + L * 0.60, hy - 0.02), knee_r=1.0, knee_l=1.0, toe_r=0.9, toe_l=0.9),
                arm_r=dict(hand=(0.55, 1.30), bend=0.3, stretch=1.1, layer="front", shape="open"), arm_l=dict(hand=(-0.55, 1.32), bend=0.3, stretch=1.1, layer="back", shape="open"),
                bike23=dict(state="fallen", phase=t * 2.0, color=col), ground23="seat")


def sit_crate_pose(cast="major", **kw):
    """sitting on a wooden crate (drawn in the sprite, its bottom on the ground point): thighs level, shins down, feet on the ground."""
    f0 = P.figure(cast, dict(yaw=0.3), "q")
    hip = f0["anchors"]["hip"]
    L = P.CAST[cast]["leg"]
    up = L * 0.52
    p = dict(yaw=0.3, expr="neutral", legs=dict(foot_r=(hip[0] + up + 0.05, hip[1] + L - up + 0.02), foot_l=(hip[0] + up - 0.10, hip[1] + L - up + 0.02),
                                                 knee_r=1.0, knee_l=1.0, toe_r=1.0, toe_l=1.0), crate23="seat")
    p.update(kw)
    return p


BALLOON_PERIOD = 24    # frames per breath of the balloon cycle


def balloon_frame(cast="major", g=0, n=0, per=BALLOON_PERIOD * 3, color=None, seated=True, red=True):
    """the Major BLOWS UP balloons (S19): frame g of balloon number n.  Cheeks puff (two drawings, swapped on the beat), the balloon
    grows in steps per breath (3 breaths per balloon = `per` frames), tied off and replaced.  Seated on a crate by default."""
    i = g % per
    breath = i // BALLOON_PERIOD
    b = i % BALLOON_PERIOD
    blowing = b < 16
    size = (breath + (b / 16.0 if blowing else 1.0)) / 3.0
    col = color or BALLOON_COLS[n % len(BALLOON_COLS)]
    base = sit_crate_pose(cast) if seated else dict(yaw=0.3, legs="wide")
    base.update(yaw=0.35, pitch=-0.2, expr=("shouting" if blowing else "angry"), puff23=(2 if blowing and b > 4 else (1 if blowing else 0)), red23=red,
                mouth=("none" if blowing else "frown"), t=g / 30.0, fx=(["steam"] if red else []))
    an = P.figure(cast, dict(base), "q")["anchors"]
    mo = an["mouth"]
    base["arm_r"] = dict(hand=(mo[0] + 0.14, mo[1] + 0.08), bend=0.8, stretch=1.15, layer="top")
    base["arm_l"] = dict(hand=(0.15, 1.05), bend=0.5, layer="front")
    base["balloon23"] = dict(size=size, color=col)
    return base


def paint_frame(cast="gi_painter", phase=0.0, facing=1):
    """one frame of PAINTING (phase 0..1, 18 frames per stroke): the brush sweeps up and down at shoulder height toward the
    facing side, the tin in the other hand.  Anchor brush_r = the bristle tip (on the surface)."""
    s = math.sin(2 * math.pi * phase)
    return dict(yaw=0.55, pitch=-0.1, expr="determined", lean=3, mirror=facing < 0, t=phase,
                arm_r=dict(hand=(0.80, 0.10 - 0.28 * s), bend=-0.3, stretch=1.25, layer="front"), prop_r=dict(type="brush23", angle=-30 - 25 * s),
                arm_l=dict(hand=(-0.38, 0.92), bend=0.3), prop_l="pot23", legs=dict(preset="step", stride=0.3))


def wave_frame(cast, phase=0.0, facing=1, expr="happy"):
    """WAVE cycle (phase 0..1, 12 frames per wave): open hand raised beside the head, swinging."""
    s = math.sin(2 * math.pi * phase)
    return dict(yaw=0.30, pitch=-0.25, expr=expr, head_roll=3 * s, mirror=facing < 0, t=phase,
                arm_r=dict(hand=(0.62 + 0.14 * s, -0.42 - 0.03 * abs(s)), bend=-0.7, stretch=1.2, shape="open", layer="front"), arm_l="down", legs="stand")


def laugh_frame(cast, phase=0.0, base=None):
    """LAUGH bounce (phase 0..1, 10 frames = 3 Hz): squash (1.02, 0.98) <-> (0.99, 1.02), head_dy 0 <-> 0.06; the laugh drawing is HELD
    (no mouth change)."""
    s = 0.5 + 0.5 * math.sin(2 * math.pi * phase)
    p = dict(base or dict(yaw=0.25, pitch=-0.8, expr="laughing", fx=["tears"], head_roll=-8,
                          arm_r=dict(hand=(0.42, 0.98), bend=0.9, shape="open"), arm_l=dict(hand=(-0.46, 0.96), bend=0.9, shape="open"), legs="wide"))
    p["squash"] = (1.02 - 0.03 * s, 0.98 + 0.04 * s)
    p["head_dy"] = 0.06 * s
    p["t"] = phase
    return p


def paddle_frame(cast="gi_radio", phase=0.0, facing=1):
    """PADDLE a boat (phase 0..1, 24 frames per stroke): kneeling-sitting low (the boat's gunwale hides the legs), canoe paddle
    with both hands, blade dipping on the facing side.  The ground point is the knees (put it on the boat floor)."""
    s = math.sin(2 * math.pi * phase)
    c = math.cos(2 * math.pi * phase)
    p = dict(yaw=0.55, pitch=0.1, expr="determined", lean=8 + 6 * s, mirror=facing < 0, t=phase,
             legs=dict(preset="crouch", crouch=0.62, spread=0.20),
             arm_r=dict(hand=(0.45 + 0.30 * c, 0.20 + 0.25 * s), bend=0.2, stretch=1.2, layer="front"), prop_r=dict(type="oar23", angle=62 + 12 * c))
    an = P.figure(cast, dict(p), "q")["anchors"]
    g = an.get("grip_far_r")
    if g:
        p["arm_l"] = dict(hand=g, bend=0.3, stretch=1.3, layer="front")
    return p


def tiptoe_frame(cast, phase=0.0, facing=1, base=None):
    """TIPTOE (cast6 sneak cycle, 32 frames per cycle) with the finger to the lips: hush."""
    b = dict(base or dict(expr="worried", gaze=(0.6, 0.0)))
    p = cycle(cast, phase, "sneak", facing, b, "l")
    p["arm_r"] = dict(hand=(0.14, 0.28), shape="point", bend=0.9, stretch=1.0, layer="top")
    return p


def binocular_pose(cast, expr="squint", t=0.0):
    """binoculars raised to the eyes (cast10 `binoculars` placed on the eye midpoint), second hand on the far barrel."""
    p = dict(yaw=0.30, pitch=-0.05, expr=expr, t=t, legs="stand", prop_r="binoculars")
    f = P.figure(cast, dict(p, arm_r=dict(hand=(0.30, 0.20))), "q")
    er, el = f["anchors"]["eye_r"], f["anchors"]["eye_l"]
    mx, my = (er[0] + el[0]) / 2, (er[1] + el[1]) / 2
    p["arm_r"] = dict(hand=(mx + 0.16, my + 0.04), bend=0.9, stretch=1.1, layer="top")
    f = P.figure(cast, p, "q")
    g = f["anchors"].get("grip_far_r")
    if g:
        p["arm_l"] = dict(hand=g, bend=0.9, stretch=1.2, layer="top")
    return p


def carry_pose(cast, phase=None, facing=1):
    """CARRY A CRATE held in front with both hands (crate drawn in the sprite, hands over it).  phase=None: standing; a float:
    one frame of the walk cycle (28 frames) with the crate."""
    b = dict(expr="determined", crate23="carry", pitch=0.1)
    if phase is None:
        p = dict(b, yaw=0.40, legs="stand", lean=-4)
    else:
        p = cycle(cast, phase, "walk", facing, b, "none")
        p["lean"] = -3.0
    p["arm_r"] = dict(hand=(0.42, 0.82), bend=0.6, stretch=1.1, layer="front")
    p["arm_l"] = dict(hand=(-0.38, 0.84), bend=0.6, stretch=1.1, layer="front")
    return p


# ============================================================================= story poses
def _story():
    S, M = {}, {}
    PT, SD, RD, PM, DS, SM, DR, MJ = GI23 + ("major",)

    def two(name, from_side="r", bend=0.4, layer="front", stretch=1.3):
        c, p = S[name]
        an = P.figure(c, p, "q")["anchors"]
        g = an.get("grip_far_%s" % from_side)
        if g:
            other = "l" if from_side == "r" else "r"
            p["arm_" + other] = dict(hand=g, bend=bend, stretch=stretch, layer=layer)

    # ---------------- GIs: generic actions (every GI can take them)
    for c in GI23:
        sf = "_" + c[3:]
        S["gi_stand" + sf] = (c, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down", legs="stand"))
        S["gi_salute" + sf] = (c, dict(yaw=0.20, pitch=-0.2, expr="determined", arm_r=dict(hand=(0.42, -0.13), bend=-1.0, sharp=0.6, stretch=1.0, shape="open", layer="top"),
                                       arm_l="down", legs="narrow"))
        S["gi_point" + sf] = (c, dict(yaw=0.45, pitch=-0.15, expr="excited", arm_r=dict(hand=(1.05, 0.05), shape="point", bend=-0.5, stretch=1.3), arm_l=dict(hand=(-0.38, 0.95), bend=0.4), legs="wide"))
        S["gi_shock" + sf] = (c, dict(yaw=0.25, pitch=0.05, expr="shocked", mouth=("open", 0.14, 0.22), head_dy=0.04, fx=["sweat"], squash=(0.98, 1.03),
                                      arm_r=dict(hand=(0.62, 0.10), bend=-0.5, shape="open"), arm_l=dict(hand=(-0.62, 0.12), bend=-0.5, shape="open"), legs="narrow"))
        S["gi_sweat" + sf] = (c, dict(yaw=0.30, pitch=0.1, expr="worried", bigsweat23=1, arm_r=dict(hand=(0.30, -0.30), bend=-0.9, stretch=1.1, layer="top", shape="open"), arm_l="down", legs="stand"))
        S["gi_laugh" + sf] = (c, laugh_frame(c, 0.25))
        S["gi_wave" + sf] = (c, wave_frame(c, 0.25))
        S["gi_walk" + sf] = (c, cycle(c, 0.30, "walk", base=dict(expr="neutral")))
        S["gi_lift" + sf] = (c, lift_pose(c, 0.0))
        S["gi_carry" + sf] = (c, carry_pose(c))
        S["gi_tiptoe" + sf] = (c, tiptoe_frame(c, 0.3))
        S["gi_paddle" + sf] = (c, paddle_frame(c, 0.25))
        S["gi_droop" + sf] = (c, dict(yaw=0.30, pitch=0.9, expr="sad", head_dy=0.06, lean=6, arm_r="down", arm_l="down", legs="narrow"))
        S["gi_grin" + sf] = (c, dict(yaw=0.30, pitch=-0.2, expr="grinning", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["gi_*_<member>"] = dict(note="generic GI poses, suffix = member without 'gi_': stand, salute, point, shock (jaw drop), sweat (big drop, hand to helmet), laugh (bounce "
                                   "with laugh_frame), wave (wave_frame), walk (cycle), lift (lift_pose: hands overhead at LIFT_H), carry (crate in both hands), tiptoe, "
                                   "paddle, droop (crew droop at the nickname), grin")
    # ---------------- roles
    S["gi_paint_star"] = (PT, paint_frame(PT, 0.25))
    M["gi_paint_star"] = dict(note="painting the white star: animate paint_frame(gi_painter, g / 18); anchor brush_r = bristle tip; white paint on his hands")
    S["gi_painter_stencil"] = (PT, dict(yaw=0.55, expr="determined", lean=8, arm_l=dict(hand=(0.55, 0.30), bend=0.1, stretch=1.2, layer="front"), prop_l=dict(type="stencil23", angle=0),
                                        arm_r=dict(hand=(0.85, 0.20), bend=-0.2, stretch=1.25, layer="top"), prop_r=dict(type="brush23", angle=-20), legs=dict(preset="step", stride=0.3)))
    M["gi_painter_stencil"] = dict(note="S10: holds a card stencil flat on a bumper (screen-right) and dabs white paint through it; anchor stencil_l (cut-out centre)")
    S["gi_sound_carry_record"] = (SD, dict(yaw=0.40, expr="happy", arm_r=dict(hand=(0.55, 0.62), bend=0.3, layer="front"), prop_r=dict(type="record23", angle=-75), arm_l="down", legs="stand"))
    M["gi_sound_carry_record"] = dict(note="the sound man carries a big transcription disc (headphones on); also walk: cycle(gi_sound, ph, 'walk', base=pose, arms='l')")
    S["gi_sound_switches"] = (SD, dict(yaw=0.60, pitch=0.05, expr="determined", lean=6, arm_r=dict(hand=(0.95, 0.30), bend=-0.2, stretch=1.25, shape="point"),
                                       arm_l=dict(hand=(0.70, 0.45), bend=0.1, stretch=1.25), legs=dict(preset="step", stride=0.3)))
    M["gi_sound_switches"] = dict(note="S09: flipping switches on the sound truck panel (screen-right); animate the pointing hand y 0.25 <-> 0.40 every 6 frames")
    S["gi_radio_talk"] = (RD, dict(yaw=0.30, pitch=-0.1, expr="talking", mouth="talk_a", arm_r=dict(hand=(0.50, 0.06), bend=0.9, stretch=1.0, layer="top"), prop_r=dict(type="handset23", angle=-95),
                                   arm_l=dict(hand=(-0.35, 0.80), bend=0.6, shape="point"), legs="stand"))
    M["gi_radio_talk"] = dict(note="S10: fake radio chatter into the handset (pack + antenna on his back). NOT a quoted speaker: hold mouth 'talk_a' (or alternate "
                                   "talk_a / flat no faster than every 12 frames as 'chatter' if the director allows); anchor earpiece_r")
    S["gi_pump_pump"] = (PM, pump_frame(PM, 0.0))
    M["gi_pump_pump"] = dict(note="pump cycle: pump_frame(gi_pump, g / 20); anchors pump_handle, hose_end (on the ground, 1.8 D toward the facing side)")
    S["gi_designer_clipboard"] = (DS, dict(yaw=0.30, pitch=0.25, expr="smirk", arm_l=dict(hand=(0.08, 0.66), bend=0.6, layer="front"), prop_l=dict(type="clipboard23", angle=0),
                                           arm_r=dict(hand=(0.30, 0.62), bend=0.7, layer="top"), prop_r=dict(type="pencil", angle=-120), legs="stand"))
    M["gi_designer_clipboard"] = dict(note="the designer checks his tank sketch on the clipboard, pencil in hand, round glasses")
    S["gi_designer_point"] = (DS, dict(yaw=0.45, pitch=-0.15, expr="determined", arm_l=dict(hand=(-0.30, 0.70), bend=0.6, layer="front"), prop_l=dict(type="clipboard23", angle=0),
                                       arm_r=dict(hand=(1.05, 0.0), shape="point", bend=-0.5, stretch=1.3), legs="wide"))
    S["gi_smile_lift_quote"] = (SM, lift_pose(SM, 0.0, expr="grinning", mouth="talk_a", strain=0.6))
    S["gi_smile_lift_quote"][1]["bigsweat23"] = 1
    M["gi_smile_lift_quote"] = dict(lipsync=True, note="S13 QUOTE 'พวกเราอเมริกัน แข็งแรงมาก': the dry smile with the tank overhead; LIP-SYNC mouth=talk_mouth(g) in the "
                                                       "quote, 'grin' outside it; a big sweat drop; hands stay at LIFT_H")
    S["gi_smile_dry"] = (SM, lift_pose(SM, 0.0, expr="grinning", strain=0.6))
    S["gi_smile_dry"][1].update(bigsweat23=1, mouth="grin")
    S["gi_pin_prick"] = (DR, dict(yaw=0.55, pitch=0.1, expr="neutral", lean=4, arm_r=dict(hand=(0.80, 0.42), bend=-0.2, stretch=1.2), prop_r=dict(type="pin23", angle=-5),
                                  arm_l=dict(hand=(-0.30, 0.90), bend=0.4), legs=dict(preset="step", stride=0.25)))
    M["gi_pin_prick"] = dict(note="S03: pricks the tank by accident with the patch-kit pin (anchor pin_r = point); then gi_sweat_driver / gi_shock_driver")
    S["gi_polish"] = (RD, dict(yaw=0.55, pitch=-0.1, expr="happy", lean=4, arm_r=dict(hand=(0.85, -0.05), bend=-0.3, stretch=1.25), prop_r="rag23",
                               arm_l=dict(hand=(-0.36, 0.86), bend=0.4), legs=dict(preset="step", stride=0.25)))
    M["gi_polish"] = dict(note="S02: polishing a rubber barrel with a rag (screen-right); animate hand x 0.70 <-> 0.95 on 8 frames")
    S["gi_chalk"] = (DR, dict(yaw=0.55, pitch=0.1, expr="smirk", lean=6, arm_r=dict(hand=(0.88, 0.45), bend=-0.2, stretch=1.25), prop_r=dict(type="chalk23", angle=-20),
                              arm_l="akimbo", legs=dict(preset="step", stride=0.3)))
    M["gi_chalk"] = dict(note="S08: the Major's driver chalks 'BALLOON ARMY' on a crate (screen-right); anchor chalk_r = the chalk tip on the crate face")
    # ---------------- the Major
    S["major_stand"] = (MJ, dict(yaw=0.20, pitch=-0.3, expr="smug", cigar=True, arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["major_stand"] = dict(note="smug, chin up, cigar in the mouth corner (cigar=True; cast3 draws it only while the mouth is closed)")
    S["major_laugh"] = (MJ, laugh_frame(MJ, 0.25, dict(yaw=0.20, pitch=-0.85, expr="laughing", fx=["tears"], head_roll=-10, lean=-8,
                                                   arm_r=dict(hand=(0.46, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.20, 0.30), bend=0.6, layer="front"), prop_l="cigar23", legs="wide")))
    M["major_laugh"] = dict(note="S06 BELLY LAUGH (held laugh drawing, no lip-sync), cigar in the fingers: animate laugh_frame(major, g / 10, base=STORY23['major_laugh'][1])")
    S["major_point_quote"] = (MJ, dict(yaw=0.25, pitch=-0.45, expr="smug", mouth="talk_b", head_roll=4, arm_r=dict(hand=(1.10, 0.0), shape="point", bend=-0.5, stretch=1.3),
                                       arm_l=dict(hand=(-0.20, 0.30), bend=0.6, layer="front"), prop_l="cigar23", legs="wide"))
    M["major_point_quote"] = dict(lipsync=True, note="S07 QUOTE 1 'กองทัพลูกโป่งเนี่ยนะ!': points at the deflated tank, cigar in the other hand; LIP-SYNC")
    S["major_promise_quote"] = (MJ, dict(yaw=0.20, pitch=-0.55, expr="smug", mouth="talk_b", head_roll=-5, lean=-4, arm_r=dict(hand=(0.42, -0.45), shape="point", bend=-0.9, stretch=1.2, layer="front"),
                                         arm_l=dict(hand=(-0.06, 0.78), bend=0.9, layer="front", shape="open"), legs="wide"))
    M["major_promise_quote"] = dict(lipsync=True, note="S07 QUOTE 2 'ข้าจะเป่าลูกโป่งให้เองทุกลูก!': finger up, other hand on the chest; LIP-SYNC")
    S["major_angry_red"] = (MJ, dict(yaw=0.20, pitch=-0.6, expr="angry", red23=1, fx=["steam"], t=0.3, arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["major_angry_red"] = dict(note="red angry face (red23=1 swaps the whole face fill; steam fx, animate t)")
    S["major_jaw_drop"] = (MJ, dict(yaw=0.25, pitch=0.1, expr="stunned", mouth=("open", 0.18, 0.22), head_dy=0.03, fx=["sweat"], arm_r=dict(hand=(0.55, 1.10), bend=0.2), prop_r="cigar23",
                                    arm_l=dict(hand=(-0.55, 1.06), bend=0.2), legs="stand"))
    S["major_puff"] = (MJ, balloon_frame(MJ, 12, 0))
    M["major_puff"] = dict(note="S19 blowing up balloons on a crate, red-faced: animate balloon_frame(major, g, n) (puffed cheeks swap, balloon grows per breath); "
                                "the pile: balloon_svg(); last balloon pop: balloon23=dict(size=1, pop=1)")
    S["major_sit"] = (MJ, sit_crate_pose(MJ, expr="angry", red23=1, arm_r=dict(hand=(0.40, 0.95), bend=0.6), arm_l=dict(hand=(-0.30, 0.98), bend=0.6)))
    S["major_walk"] = (MJ, cycle(MJ, 0.30, "walk", base=dict(expr="smug", cigar=True)))
    S["driver_drive"] = (DR, dict(yaw=0.40, expr="neutral", arm_r=dict(hand=(0.60, 0.55), bend=0.4, layer="front"), arm_l=dict(hand=(0.30, 0.60), bend=0.4, layer="front"),
                                  legs=dict(preset="crouch", crouch=0.45, spread=0.1)))
    M["driver_drive"] = dict(note="the Major's driver at the jeep wheel (legs hidden by the jeep; hands at the wheel rim height)")
    # ---------------- the French cyclists
    for c, sf in (("fr_beret", "beret"), ("fr_cap", "cap")):
        S["fr_ride_" + sf] = (c, ride_frame(c, 0.25, expr="happy", mouth="smile"))
        S["fr_chat_" + sf] = (c, ride_frame(c, 0.25, expr="happy", mouth="talk_a", look=0.4))
        S["fr_stare_" + sf] = (c, ride_frame(c, 0.25, expr="stunned", state="brake", look=0.5))
        S["fr_jaw_" + sf] = (c, ride_frame(c, 0.25, expr="shocked", mouth=("open", 0.14, 0.24), state="brake", look=0.6))
        S["fr_fall_" + sf] = (c, fall_pose(c, 0.2))
        S["fr_stand_" + sf] = (c, dict(yaw=0.30, expr="happy", arm_r="down", arm_l="down", legs="stand"))
    M["fr_ride"] = dict(note="pedalling: ride_frame(fr_beret|fr_cap, g / 14, facing); bike inside the sprite, ground point = wheel contact; the beret rider has the "
                             "basket + baguette (green bike), the cap rider a maroon bike")
    M["fr_chat"] = dict(note="chatty face: a HELD open happy mouth (they are not quoted: no lip-sync)")
    M["fr_stare"] = dict(note="staring while braking (state='brake'): stunned eyes, cranks frozen")
    M["fr_jaw"] = dict(note="jaw drop while braking")
    M["fr_fall"] = dict(note="fallen off gently: fall_pose(c, g / 30) sitting on the ground, daze stars, bike lying beside him; ground point = his seat")
    # ---------------- German observers
    for c, sf in (("ger_tall", "tall"), ("ger_round", "round")):
        S["ger_binoc_" + sf] = (c, binocular_pose(c, "squint"))
        S["ger_surprise_" + sf] = (c, dict(yaw=0.30, pitch=-0.1, expr="shocked", mouth=("open", 0.12, 0.16), fx=["sweat"], arm_r=dict(hand=(0.30, 0.90), bend=0.6), prop_r="binoculars",
                                           arm_l=dict(hand=(-0.45, 0.20), bend=-0.5, shape="open"), legs="narrow"))
        S["ger_nudge_" + sf] = (c, dict(yaw=0.45, pitch=-0.1, expr="excited", head_roll=-6, lean=-6, arm_r=dict(hand=(0.40, 0.62), bend=1.0, sharp=0.9, stretch=0.8, layer="front"),
                                        arm_l=dict(hand=(-0.20, 0.80), bend=0.6), prop_l="binoculars", legs="stand"))
        S["ger_point_" + sf] = (c, dict(yaw=0.45, pitch=-0.2, expr="excited", arm_r=dict(hand=(1.05, -0.05), shape="point", bend=-0.5, stretch=1.3), arm_l=dict(hand=(-0.30, 0.85), bend=0.4), prop_l="binoculars", legs="wide"))
    S["ger_sausage"] = ("ger_round", dict(yaw=0.30, pitch=-0.1, expr="happy", arm_r=dict(hand=(0.36, 0.30), bend=0.8, layer="front"), prop_r=dict(type="sausage23", angle=-30),
                                          arm_l=dict(hand=(-0.30, 0.80), bend=0.4), prop_l="binoculars", legs="stand"))
    S["ger_drop_sausage"] = ("ger_round", dict(yaw=0.30, pitch=-0.2, expr="stunned", mouth=("open", 0.14, 0.18), arm_r=dict(hand=(0.40, 0.36), bend=0.8, shape="open", layer="front"),
                                               arm_l=dict(hand=(-0.30, 0.80), bend=0.4), prop_l="binoculars", legs="stand"))
    M["ger_sausage"] = dict(note="S17: eating a sausage; ger_drop_sausage: the hand opens and the sausage falls (draw it falling with sausage_svg(), "
                                 "starting at anchor hand_r)")
    M["ger_nudge"] = dict(note="nudge: elbow jabbed toward screen-right (mirror=True for the other side), excited grin; animate lean -6 <-> 0")
    return S, M


def sausage_svg(uid="ss", angle=0.0, ink=P.INK, tint=None):
    """the falling sausage alone (centre near (0.15, 0)), for the drop gag."""
    k = _ctx(uid, ink, tint)
    return '<g transform="rotate(%.2f)">%s</g>' % (angle, _sausage_body(k))


def record_svg(uid="rec", spin=0.0, ink=P.INK, tint=None):
    """the transcription disc alone (centre (0, 0), radius 0.55): spin 0..1 rotates the sheen + label (the turntable on the truck)."""
    k = _ctx(uid, ink, tint)
    return '<g>%s</g>' % _record_body(k, spin)


STORY23, STORY23_META = {}, {}


# ============================================================================= sprites with the ground point
def sprite(cast, pose, out, px_per_D=128, canvas=None, **kw):
    """render one sprite through stage/sprites.py and write <out>.json beside it with the ground point: origin_px (pixel of the
    feet / wheel / seat contact = the sprite's bottom anchor), canvas, px_per_D, and gap_px (rows between the lowest opaque pixel and
    the ground point; 0-2 = planted).  Returns that dict."""
    import json
    sp = _sprites()
    r = sp.render_sprites([dict(cast=cast, pose=pose, px_per_D=px_per_D, out=os.path.abspath(out), canvas=canvas or sp.DEFAULT_CANVAS[cast], **kw)])[0]
    info = dict(out=r["out"], canvas=r["canvas"], px_per_D=r["px_per_D"], origin_px=r["origin_px"], size=r["size"], clipped=r["clipped"], gap_px=_gap(r))
    with open(os.path.abspath(out) + ".json", "w") as fh:
        json.dump(info, fh)
    return info


def _gap(r):
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(r["out"]).getchannel("A")
    w, h = im.size
    bb = im.point(lambda a: 255 if a > 40 else 0).getbbox()
    if not bb:
        return None
    return int(round(r["origin_px"][1])) - bb[3]


def _sprites():
    sd = os.path.join(PROJ, "v3", "stage")
    if sd not in sys.path:
        sys.path.insert(0, sd)
    import sprites
    CE.register_stage(sprites)
    return sprites


# ============================================================================= registration
def register():
    if getattr(P, "_cast23_registered", False):
        CE.register_stage()
        if not STORY23:
            s, m = _story()
            STORY23.update(s)
            STORY23_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "_moustache", "_hand", "figure"):
        _O23[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P._moustache = _moustache
    P._hand = _hand
    P.figure = figure
    CE.COSTUMES.update(COSTUMES23)
    CE.HATS.update(HATS23)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS23 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP23)
    for n, c in NEW_CAST23.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS23)
    P._cast23_registered = True
    s, m = _story()
    STORY23.update(s)
    STORY23_META.update(m)
    P.STORY.update(STORY23)
    CE.register_stage()


# measured by `python3 test_cast23.py canvas` (union of every story pose, cycle frame and arm preset, 0.32 D head room, 1/16 grid)
CANVAS23 = {
    "gi_painter": (-1.7500, -3.8750, 1.7500, 0.1875),
    "gi_sound": (-1.6875, -3.8750, 1.6875, 0.3125),
    "gi_radio": (-1.6875, -4.0000, 1.6875, 0.1875),
    "gi_pump": (-1.6875, -3.8750, 1.6875, 0.3125),
    "gi_designer": (-1.6875, -3.8750, 1.6875, 0.1875),
    "gi_smile": (-1.6875, -3.8750, 1.6875, 0.1875),
    "gi_driver": (-1.6875, -3.8750, 1.6875, 0.2500),
    "major": (-1.5625, -4.0625, 1.5625, 0.1250),
    "fr_beret": (-1.1875, -3.5625, 1.1875, 0.1250),
    "fr_cap": (-1.1875, -3.5625, 1.1875, 0.1250),
    "ger_tall": (-1.2500, -3.8750, 1.2500, 0.1250),
    "ger_round": (-1.3125, -3.5000, 1.3125, 0.1250),
}
CANVAS23_WIDE = {
    "gi_painter": (-2.1875, -3.5625, 2.1875, 0.1250),
    "gi_sound": (-2.1875, -3.2500, 2.1875, 0.1250),
    "gi_radio": (-2.1875, -3.8125, 2.1875, 0.1250),
    "gi_pump": (-2.1875, -3.3750, 2.1875, 0.1250),
    "gi_designer": (-2.1875, -3.6250, 2.1875, 0.1250),
    "gi_smile": (-2.1875, -3.6250, 2.1875, 0.1250),
    "gi_driver": (-2.1875, -3.5000, 2.1875, 0.1250),
    "major": (-1.5625, -4.0625, 1.5625, 0.1250),
    "fr_beret": (-1.8125, -3.6875, 1.8125, 0.1875),
    "fr_cap": (-1.8125, -3.7500, 1.8125, 0.1875),
    "ger_tall": (-1.2500, -3.8750, 1.2500, 0.1250),
    "ger_round": (-1.3125, -3.5000, 1.3125, 0.1250),
}   # bicycle / pump poses

register()
