#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast14.py -- the cast of film 14 ("ไอ้บ้าผึ้ง": a beehive fence against elephants, Kenya) as an extension module on top of cast10.

    import sys; sys.path.insert(0, ".../v3/cast14"); import cast14     # registers on import (idempotent); imports cast10 .. cast_ext
    import puppet                                                      # the same module object, now with the new members
    cast, pose = cast14.STORY14["uncle_stung_nose"]
    f = puppet.figure(cast, pose, "f")
    e = puppet.figure("matriarch", cast14.cycle("matriarch", 0.25, "walk"), "e")     # the elephants go through puppet.figure too

Nothing in v2/puppet or v3/cast .. cast10 is edited (cast14 only adds table entries and wraps helpers).  Everything here
works from the repo (film/ is the root, PROJ is derived from this file's location, no /tmp path).  See API.md.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))        # film/
_d = os.path.join(PROJ, "v3", "cast10")
if _d not in sys.path:
    sys.path.insert(0, _d)
import cast10 as C10     # noqa: E402  (v3/cast10, read-only; imports cast9 .. cast_ext and v2/puppet)
import cast9 as C9       # noqa: E402
import cast8 as C8       # noqa: E402
import cast6 as C6       # noqa: E402
import cast2 as C2       # noqa: E402
import cast_ext as CE    # noqa: E402
import puppet as P       # noqa: E402

TT = P.TORSO_TOP
_clamp, _rot, _num = P._clamp, P._rot, P._num
_poly_d = P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O14 = {}
_POSE14 = {"nose": 0.0, "t": 0.0}

cycle6, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

PEOPLE14 = ("farmer14", "uncle14", "woman14", "kid14", "oldman14", "youth14")
ELEPHANTS = ("matriarch", "elephant_b", "elephant_c", "elephant_d", "calf")
CREATURES = ("bee", "swarm")
NEW14 = PEOPLE14 + ELEPHANTS + CREATURES

# scale: the farmer is 1.75 m tall = 3.0 D head top to soles  ->  1 D = 0.583 m.  An elephant shoulder of 3.3 m = 5.66 D.
M_PER_D = 1.75 / 3.0


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


# ============================================================================= colours
WOOD = dict(light="#e2b67c", base="#b9824a", dark="#7a512c", deep="#5a3a1e")
TIN = dict(light="#eef0f2", base="#b4bcc6", dark="#7a8494")
POTM = dict(light="#c9ccd4", base="#8e94a2", dark="#575c6c")
WIRE = dict(light="#d8dce4", base="#9aa0ae", dark="#5c6272")
FLAME = dict(outer="#ff9a2e", mid="#ffc43a", core="#fff0a0")
SKIN_TRUNK_PINK = dict(light="#ffb0a4", base="#ee6a5e", dark="#b83a3a")
HIDE = dict(light="#b9b6c6", base="#9a97ac", dark="#6a677f", deep="#4c4a60", ear="#dba5a6", ear_d="#b97a86")
IVORY = dict(light="#fffbe8", base="#f1e6c6", dark="#c4b48c")
BEE_GOLD, BEE_DARK = "#f2b72c", "#2a1d12"


# ============================================================================= hats (head frame)
def _hat_veil14(k, C, yaw):
    """the farmer's beekeeper hat PUSHED BACK: a wide straw brim tipped up behind the crown, the forehead free, a rolled-up
    net veil bunched on the brim and a gauze curtain hanging behind the head on the side away from the face."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = -1.0 if yaw >= 0 else 1.0
    o = []
    # the gauze curtain hanging behind the head (away from the face), cross-hatched
    w = 0.12 + 0.5 * (1 - 0.5 * min(1.0, abs(yaw)))
    u = k.uid
    k.defs.append('<pattern id="%s_c14vl" width="0.045" height="0.045" patternUnits="userSpaceOnUse"><path d="M0,0 L0.045,0.045 M0.045,0 L0,0.045" '
                  'stroke="%s" stroke-width="0.006" fill="none"/></pattern>' % (u, k.c("#6a6a78")))
    cx0 = s * 0.43
    cur = [(cx0 - s * 0.05, -0.34), (cx0 + s * 0.20, -0.30), (cx0 + s * 0.26, 0.08), (cx0 + s * 0.20, 0.32), (cx0 - s * 0.04, 0.30), (cx0 - s * 0.10, 0.05)]
    d = P._smooth_closed(cur)
    o.append('<path d="%s" fill="%s" fill-opacity="0.55" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c("#eef2f6"), k.ink))
    o.append('<path d="%s" fill="url(#%s_c14vl)"/>' % (d, u))
    k.ext.append((cx0 + s * 0.26, 0.10, 0.03))
    k.ext.append((cx0 + s * 0.20, 0.34, 0.03))
    o.append('<g transform="rotate(%.3f)">' % C["hat_tilt"])
    g = CE._gradient(k, "c14vh", col, x0=-0.70, x1=0.70, mid=0.34)
    # brim, tipped up at the back: a wide ellipse seen from below the head line, lifted
    brim = ("M%.4f,-0.46 C-0.62,-0.62 -0.34,-0.74 %.4f,-0.72 C0.34,-0.74 0.62,-0.62 0.80,-0.46 C0.70,-0.34 0.34,-0.36 %.4f,-0.40 "
            "C-0.34,-0.36 -0.70,-0.34 -0.80,-0.46 Z" % (-0.80 + dx, dx, dx))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, g, k.ink))
    o.append('<path d="M-0.66,-0.47 Q%.4f,-0.53 0.66,-0.47" fill="none" stroke="%s" stroke-width="0.010" opacity="0.75"/>' % (dx, k.c(col["dark"])))
    crown = "M%.4f,-0.48 C%.4f,-0.72 %.4f,-0.86 %.4f,-0.86 C%.4f,-0.86 %.4f,-0.72 %.4f,-0.48 Z" % (-0.34 + dx, -0.36 + dx, -0.20 + dx, dx, 0.20 + dx, 0.36 + dx, 0.34 + dx)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.46 %.4f,-0.52" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (-0.33 + dx, dx, 0.33 + dx, k.c(col["band"])))
    o.append('<path d="M%.4f,-0.70 Q%.4f,-0.82 %.4f,-0.84" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.9"/>' % (-0.26 + dx, -0.18 + dx, -0.06 + dx, k.c(col["shine"])))
    # the net veil rolled up on the brim: a pale bunched roll with a little gathered knot
    o.append('<path d="M%.4f,-0.43 Q%.4f,-0.34 %.4f,-0.43" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round" opacity="0.92"/>' % (-0.50 + dx, dx, 0.50 + dx, k.ink))
    o.append('<path d="M%.4f,-0.43 Q%.4f,-0.34 %.4f,-0.43" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (-0.50 + dx, dx, 0.50 + dx, k.c("#f4f6fa")))
    for i in range(7):
        x = -0.42 + i * 0.14 + dx
        o.append('<path d="M%.4f,-0.45 q0.02,0.05 0.0,0.09" fill="none" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % (x, k.c("#8a8a9a")))
    o.append('</g>')
    C10.C4._ext_hat(k, C, ((-0.82 + dx, -0.46), (0.82 + dx, -0.46), (dx, -0.88), (dx, -0.34)))
    return "".join(o), (dx, -0.86)


def _hat_headwrap14(k, C, yaw):
    """a bright cloth headwrap (kitenge): a tall folded turban of two layers with a patterned band and a knot with two tails."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.08 * yaw
    s = -1.0 if yaw >= 0 else 1.0
    u = k.uid
    o = []
    # tails of the knot, behind (away from the face)
    kx = s * (0.30 + 0.08 * min(1.0, abs(yaw) * 2)) + dx
    for (ang, ln) in ((-25, 0.30), (15, 0.26)):
        ex, ey = kx + s * ln * math.cos(math.radians(ang)) + 0.0, -0.58 + ln * math.sin(math.radians(ang)) * 0.8
        o.append('<path d="M%.4f,-0.62 L%.4f,%.4f L%.4f,-0.50 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (kx, ex, ey, kx + s * 0.02, k.c(col["base"]), k.ink))
        k.ext.append((ex, ey, 0.03))
    k.defs.append('<pattern id="%s_c14kt" width="0.12" height="0.12" patternUnits="userSpaceOnUse"><circle cx="0.03" cy="0.03" r="0.020" fill="%s"/>'
                  '<circle cx="0.09" cy="0.09" r="0.020" fill="%s"/><path d="M0,0.06 L0.12,0.06" stroke="%s" stroke-width="0.012"/></pattern>'
                  % (u, k.c(col["dot"]), k.c(col["dot"]), k.c(col["dark"])))
    g = CE._gradient(k, "c14hw", col, x0=-0.55, x1=0.55, mid=0.34)
    lay = [(-0.50 + dx, -0.20), (-0.56 + dx, -0.42), (-0.40 + dx, -0.66), (-0.12 + dx, -0.80), (0.20 + dx, -0.80), (0.44 + dx, -0.62), (0.56 + dx, -0.40), (0.52 + dx, -0.20)]
    d = P._smooth_open(lay) + " Q%.4f,-0.12 %.4f,-0.20 Z" % (fx, -0.50 + dx)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<clipPath id="%s_c14kc"><path d="%s"/></clipPath>' % (u, d))
    o.append('<g clip-path="url(#%s_c14kc)"><rect x="-0.7" y="-0.9" width="1.4" height="0.9" fill="url(#%s_c14kt)" opacity="0.9"/></g>' % (u, u))
    # fold lines
    o.append('<path d="M%.4f,-0.34 Q%.4f,-0.52 %.4f,-0.34 M%.4f,-0.50 Q%.4f,-0.70 %.4f,-0.50" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>'
             % (-0.50 + dx, dx, 0.50 + dx, -0.40 + dx, dx - 0.02, 0.38 + dx, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.22 Q%.4f,-0.16 %.4f,-0.22" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (-0.48 + dx, fx, 0.50 + dx, k.ink))
    o.append('<path d="M%.4f,-0.22 Q%.4f,-0.16 %.4f,-0.22" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (-0.48 + dx, fx, 0.50 + dx, k.c(col["band"])))
    o.append('<path d="M%.4f,-0.70 Q%.4f,-0.78 %.4f,-0.76" fill="none" stroke="#ffffff" stroke-width="0.018" stroke-linecap="round" opacity="0.7"/>' % (-0.22 + dx, -0.10 + dx, 0.06 + dx))
    # the knot
    o.append('<ellipse cx="%.4f" cy="-0.60" rx="0.085" ry="0.060" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, k.c(col["base"]), k.ink))
    k.ext.extend([(-0.58 + dx, -0.30, 0.02), (0.58 + dx, -0.30, 0.02), (dx, -0.82, 0.02)])
    return "".join(o), (dx, -0.80)


HATS14 = {"veil14": _hat_veil14, "headwrap14": _hat_headwrap14}


# ============================================================================= costumes (torso-local)
def _cos_tee14(k, C, m):
    """the farmer: a faded orange T-shirt (crew neck, ribbed collar, a worn patch and a wash crease), khaki trousers bowl with a
    rope belt below it."""
    X = _X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.16
    o = []
    # side fade + creases
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.7"/>' % (X(-0.16, 0.74) + X(-0.20, 0.90) + X(-0.14, yb - 0.04) + (k.c(col["dark"]),)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.6"/>' % (X(0.10, 0.62) + X(0.16, 0.80) + X(0.12, yb - 0.10) + (k.c(col["dark"]),)))
    # little chest print: a pale hexagon (a tee from a bee-keeping course), worn
    cx, cy = X(0.15, 0.66)
    hexp = " ".join("%.4f,%.4f" % (cx + 0.052 * math.cos(math.radians(60 * i + 30)), cy + 0.052 * math.sin(math.radians(60 * i + 30))) for i in range(6))
    o.append('<polygon points="%s" fill="%s" opacity="0.85" stroke="%s" stroke-width="0.008" stroke-opacity="0.5"/>' % (hexp, k.c(col["print"]), k.ink))
    # crew neck, ribbed collar
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (X(-0.21, 0.40) + X(0, 0.52) + X(0.21, 0.40) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (X(-0.21, 0.40) + X(0, 0.52) + X(0.21, 0.40) + (k.c(col["collar"]),)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="%s"/>' % (X(-0.17, 0.41) + X(0, 0.48) + X(0.17, 0.41) + (k.c("#fef7f6"),)))
    # hem + trousers
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (X(-0.45, yb - 0.02) + X(0, yb + 0.02) + X(0.45, yb - 0.02) + (k.c(col["dark"]),)))
    o.append(CE._bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.036"/>' % (yb + 0.02, yb + 0.05, yb + 0.02, k.ink))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-dasharray="0.03 0.012"/>' % (yb + 0.02, yb + 0.05, yb + 0.02, k.c(col["rope"])))
    return "".join(o), "", ""


def _cos_check14(k, C, m):
    """the uncle: a check shirt (two-colour plaid, open collar, buttons, a round belly) with a red shuka blanket slung over one
    shoulder and across the chest, tucked at the belt; a leather belt and the trousers bowl."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_c14ck" width="0.12" height="0.12" patternUnits="userSpaceOnUse"><rect width="0.12" height="0.036" y="0.042" fill="%s" opacity="0.55"/>'
                  '<rect height="0.12" width="0.036" x="0.042" fill="%s" opacity="0.55"/><path d="M0,0 L0.12,0 M0,0 L0,0.12" stroke="%s" stroke-width="0.006" opacity="0.5"/></pattern>'
                  % (u, k.c(col["check"]), k.c(col["check"]), k.c(col["check_d"])))
    k.defs.append('<pattern id="%s_c14sk" width="0.16" height="0.16" patternUnits="userSpaceOnUse"><rect width="0.16" height="0.026" y="0.02" fill="%s"/>'
                  '<rect width="0.16" height="0.026" y="0.10" fill="%s"/><rect height="0.16" width="0.020" x="0.02" fill="%s" opacity="0.9"/>'
                  '<rect height="0.16" width="0.020" x="0.10" fill="%s" opacity="0.9"/></pattern>'
                  % (u, k.c(col["shuka_s"]), k.c(col["shuka_s"]), k.c(col["shuka_b"]), k.c(col["shuka_b"])))
    o = ['<rect x="-0.9" y="0.3" width="1.8" height="%.4f" fill="url(#%s_c14ck)"/>' % (yb - 0.3, u)]
    # open collar + button placket
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (X(-0.22, 0.38) + X(0.0, 0.62) + X(-0.02, 0.40) + (k.c("#fef7f6"), k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (X(0.22, 0.38) + X(0.0, 0.62) + X(0.02, 0.40) + (k.c("#fef7f6"), k.ink)))
    o.append(_ln([X(0.0, 0.62), X(0.0, yb)], k.ink, 0.012, ' opacity="0.7"'))
    for y in (0.74, 0.90, 1.06):
        if y < yb - 0.02:
            o.append(_circ(X(0.02, y), 0.016, k.c("#f4eee2"), k, 0.007))
    # belly highlight crease under the belly
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.6"/>' % (X(-0.36, yb - 0.14) + X(0.0, yb - 0.04) + X(0.36, yb - 0.14) + (k.c(col["check_d"]),)))
    # the shuka: a diagonal band from the left shoulder across to the right hip
    band = [X(-0.52, 0.30), X(-0.18, 0.30), X(0.62, yb - 0.12), X(0.62, yb + 0.12), X(0.30, yb + 0.12), X(-0.52, 0.62)]
    d = _poly_d(band)
    o.append('<clipPath id="%s_c14sc"><path d="%s"/></clipPath>' % (u, d))
    o.append('<path d="%s" fill="%s"/>' % (d, k.c(col["shuka"])))
    o.append('<g clip-path="url(#%s_c14sc)"><rect x="-0.9" y="0.2" width="1.8" height="1.4" fill="url(#%s_c14sk)"/></g>' % (u, u))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, k.ink))
    # trousers + belt
    o.append(CE._bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.060"/>' % (yb + 0.01, yb + 0.04, yb + 0.01, k.ink))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f" fill="none" stroke="%s" stroke-width="0.040"/>' % (yb + 0.01, yb + 0.04, yb + 0.01, k.c(col["belt"])))
    bx, by = X(0.0, yb + 0.03)
    o.append('<rect x="%.4f" y="%.4f" width="0.080" height="0.064" rx="0.010" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx - 0.04, by - 0.032, k.c("#e2b442"), k.ink))
    # the shuka tail hanging over the shoulder (a flap at the left shoulder, in front)
    ov = ['<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
          % (X(-0.56, 0.30) + X(-0.20, 0.30) + X(-0.26, 0.66) + X(-0.62, 0.62) + (k.c(col["shuka"]), k.ink))]
    return "".join(o), "", "".join(ov)


def _cos_kanga14(k, C, m):
    """the village woman: a kitenge blouse and a wrap skirt (printed cloth, big motifs, a darker hem band) to mid-calf, knotted
    at the hip."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    u = k.uid
    k.defs.append('<pattern id="%s_c14kg" width="0.20" height="0.20" patternUnits="userSpaceOnUse"><circle cx="0.05" cy="0.05" r="0.034" fill="%s"/>'
                  '<circle cx="0.15" cy="0.15" r="0.034" fill="%s"/><path d="M0.05,0.15 q0.04,-0.06 0.09,-0.02" stroke="%s" stroke-width="0.014" fill="none"/></pattern>'
                  % (u, k.c(col["motif"]), k.c(col["motif"]), k.c(col["motif2"])))
    yw = TT + h * 0.72
    o = ['<rect x="-0.9" y="0.3" width="1.8" height="%.4f" fill="url(#%s_c14kg)" opacity="0.65"/>' % (yw - 0.3, u)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.060" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.56) + X(0.20, 0.40) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (X(-0.20, 0.40) + X(0, 0.56) + X(0.20, 0.40) + (k.c(col["trim"]),)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="%s"/>' % (X(-0.16, 0.41) + X(0, 0.51) + X(0.16, 0.41) + (k.c("#fef7f6"),)))
    hem = yB + C["leg"] * C.get("hem_frac", 0.70)
    a = hw * 0.82
    b = hw + C.get("skirt_flare", 0.22)
    sk = C2._grad(k, "sk", col["skirt"], -b, b)
    ov = [C2._skirt(k, "ks", X, yw - 0.02, a, hem, b, sk, sw=0.026,
                    folds=((-0.12, yw + 0.15, -0.22, hem - 0.05), (0.14, yw + 0.15, 0.26, hem - 0.05), (0.02, yw + 0.22, 0.04, hem - 0.06)), fold_col=k.c(col["skirt_d"]))]
    ov.append('<clipPath id="%s_c14kk"><path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z"/></clipPath>' % ((u,) + X(-a, yw) + X(a, yw) + X(b, hem) + X(-b, hem)))
    ov.append('<g clip-path="url(#%s_c14kk)"><rect x="-1.2" y="%.4f" width="2.4" height="%.4f" fill="url(#%s_c14kg)"/></g>' % (u, yw, hem - yw, u))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050"/>' % (X(-b + 0.02, hem - 0.05) + X(0, hem - 0.01) + X(b - 0.02, hem - 0.05) + (k.c(col["skirt_d"]),)))
    ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010"/>' % (X(-b + 0.02, hem - 0.08) + X(0, hem - 0.04) + X(b - 0.02, hem - 0.08) + (k.ink,)))
    ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.ink, 0.056))
    ov.append(_ln([X(-a - 0.02, yw - 0.02), X(a + 0.02, yw - 0.02)], k.c(col["belt"]), 0.036))
    kx, ky = X(a * 0.7, yw + 0.01)
    ov.append('<path d="M%.4f,%.4f q-0.04,0.10 -0.01,0.17 M%.4f,%.4f q0.03,0.09 0.04,0.15" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (kx, ky, kx, ky, k.c(col["belt"])))
    return "".join(o), "", "".join(ov)


def _cos_kanzu14(k, C, m):
    """the old man: a long cream cotton robe (kanzu) with a small collar and button placket, a worn wool waistcoat over it."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    o = []
    # waistcoat panels
    for s in (-1, 1):
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (_poly_d([X(s * 0.16, 0.40), X(s * 0.46, 0.34), X(s * 0.50, 0.96), X(s * 0.06, yB - 0.10), X(s * 0.04, 0.60)]), k.c(col["vest"]), k.ink))
    o.append(_ln([X(0.0, 0.58), X(0.0, 0.84)], k.c("#f4eee2"), 0.012))
    for y in (0.64, 0.78, 0.92):
        o.append(_circ(X(0.10, y), 0.014, k.c(col["button"]), k, 0.006))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % (X(-0.16, 0.40) + X(0, 0.50) + X(0.16, 0.40) + (k.ink,)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % (X(-0.16, 0.40) + X(0, 0.50) + X(0.16, 0.40) + (k.c(col["base"]),)))
    hem = yB + C["leg"] * C.get("robe_frac", 0.78)
    a = hw * 0.97
    b = hw + C.get("robe_flare", 0.12)
    g = "url(#%s_tg)" % k.uid
    ov = [C2._skirt(k, "kz", X, yB - 0.30, a, hem, b, g, sw=0.026,
                    folds=((-0.10, yB - 0.1, -0.16, hem - 0.04), (0.12, yB - 0.1, 0.20, hem - 0.04)), fold_col=k.c(col["dark"]))]
    # waistcoat bottom over the robe
    ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
              % (X(-0.50, yB - 0.30) + X(0.50, yB - 0.30) + X(0.46, yB - 0.02) + X(-0.46, yB - 0.02) + (k.c(col["vest"]), k.ink)))
    ov.append(_ln([X(0.0, yB - 0.30), X(0.0, yB - 0.02)], k.c("#f4eee2"), 0.012))
    return "".join(o), "", "".join(ov)


COSTUMES14 = {"tee14": _cos_tee14, "check14": _cos_check14, "kanga14": _cos_kanga14, "kanzu14": _cos_kanzu14}


# ============================================================================= the cast (head D = 1)
_FLAGS = dict(C10._FLAGS, _cast14=True)


def _mk(base, **kw):
    d = dict(P.CAST[base])
    d.update(_FLAGS)
    d.update(kw)
    return d


NEW_CAST14 = {
    # the young farmer: slim, short black hair, faded orange tee with a worn hexagon print, khaki trousers rolled to the calf,
    # rubber sandals, a straw beekeeper's hat pushed back on his head with a net veil
    "farmer14": _mk(
        "worker1", build="slim", seed=141.3,
        torso_w=0.60, torso_h=1.00, shoulder=(0.24, 0.50), arm=0.76, hip_x=0.15, leg=1.36, stance=0.07, wide=0.27, limb_w=0.056,
        eye_y=0.035, brow="stroke", brow_th=0.056, mouth="smile", moustache=False, smirk_side=1, cheeks="#eba08a",
        hat="newsboy", hat_style="veil14", hat_tilt=-7.0, ear_pencil=False,
        hat_colors=dict(light="#f4e6c0", base="#dcc48a", dark="#a8884a", band="#8a5a30", shine="#fffaf0"),
        hair=dict(color="#1f1818", front=0.10, grow=0.22),
        costume="tee14",
        sleeve=dict(color="#e0883c", dark="#b8662a", cuff="#e8a05a", len=0.50, w=0.15, roll=True),
        shorts=dict(color="#c9b27a", dark="#9a8450", cuff="#e0cf9c", len=0.60, w=0.14),
        boots=dict(color="#e8dcc0", cuff="#e8dcc0", h=0.035, toe=0.15),
        colors=dict(base="#e0883c", dark="#b8662a", collar="#c4682a", print="#f4c890", pants="#c9b27a", rope="#e4d2a0"),
    ),
    # the uncle: older, round belly, grey stubble, flat cap, check shirt, a red shuka over one shoulder, a belt
    "uncle14": _mk(
        "foreman", build="stout", seed=142.7,
        torso_w=1.30, torso_h=1.14, shoulder=(0.46, 0.44), arm=0.76, hip_x=0.18, leg=1.20, stance=0.07, wide=0.30, limb_w=0.068,
        eye_y=-0.01, brow="stroke", brow_th=0.082, mouth="smirk", moustache=False, cheeks="#ea8478", chins=True, age_lines=True,
        beard=dict(color="#c4c0c8", dark="#7a7686"),
        hat="newsboy", hat_style="flatcap", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#8a7a68", base="#6a5a4a", dark="#463a2e", visor="#54483a", shine="#b8a890"),
        hair=dict(color="#c4c0c8", front=0.04, grow=0.18),
        costume="check14",
        sleeve=dict(color="#4f8a9a", dark="#33606e", cuff="#6fa4b2", len=0.62, w=0.20, roll=True),
        shorts=dict(color="#6a5a48", dark="#463a2e", cuff="#6a5a48", len=0.92, w=0.17),
        boots=dict(color="#3a2c24", cuff="#3a2c24", h=0.09, toe=0.16),
        colors=dict(base="#4f8a9a", dark="#33606e", check="#ffffff", check_d="#2a4a58", shuka="#c8402e", shuka_s="#7a1c1c", shuka_b="#2a3a6a",
                    pants="#6a5a48", belt="#4a3226"),
    ),
    # the village woman: kitenge headwrap, printed blouse and wrap skirt
    "woman14": _mk(
        "woman1", seed=143.1,
        torso_w=0.66, torso_h=0.94, leg=1.12, hem_frac=0.74, limb_w=0.056, mouth="smile", cheeks="#f09a96", eye_y=0.04,
        hat="newsboy", hat_style="headwrap14", hat_tilt=-3.0,
        hat_colors=dict(light="#ffd45a", base="#f0a02a", dark="#b8661a", band="#c43a50", dot="#c43a50", shine="#ffffff"),
        hair=dict(color="#2a1e1a", front=0.0, grow=0.0),
        costume="kanga14", skirt_flare=0.24,
        sleeve=dict(color="#e8d868", dark="#b8a640", cuff="#e8d868", len=0.50, w=0.14, roll=True),
        boots=dict(color="#e8dcc0", cuff="#e8dcc0", h=0.035, toe=0.13),
        colors=dict(base="#e8d868", dark="#b8a640", trim="#3a7a5a", motif="#3a7a5a", motif2="#f4eee2", skirt="#d8483e", skirt_d="#8e2820", belt="#3a7a5a",
                    pants="#d8483e"),
    ),
    # the kid: small boy, green tee, shorts, bare feet-ish sandals, cropped hair
    "kid14": _mk(
        "kit", seed=144.9, build="boy",
        torso_w=0.62, torso_h=0.78, leg=0.86, arm=0.62, limb_w=0.054, cheeks="#f4a090", mouth="smile",
        hat="newsboy", hat_style="flatcap", hat_tilt=-6.0,
        hat_colors=dict(light="#f0c24a", base="#d8a02a", dark="#a8741a", visor="#b88420", shine="#fff0b0"),
        hair=dict(color="#1f1818", front=0.10, grow=0.20),
        costume="tee14", sleeve=dict(color="#58a860", dark="#3a7a42", cuff="#7ac082", len=0.45, w=0.15, roll=True),
        shorts=dict(color="#6a7aa8", dark="#46547e", cuff="#6a7aa8", len=0.45, w=0.13),
        boots=dict(color="#e8dcc0", cuff="#e8dcc0", h=0.035, toe=0.13, soft=True),
        colors=dict(base="#58a860", dark="#3a7a42", collar="#3a7a42", print="#c8e8c0", pants="#6a7aa8", rope="#e4d2a0"),
    ),
    # the old man: white stubble beard, white kofia cap, a long cream kanzu with a worn waistcoat
    "oldman14": _mk(
        "oldman", seed=145.2, build="regular",
        torso_w=0.80, torso_h=0.98, leg=1.08, limb_w=0.058, mouth="smile", cheeks="#ec9a88",
        hat_style="skullcap", hat_tilt=-2.0,
        hat_colors=dict(light="#ffffff", base="#f2eee4", dark="#bcb4a6", shine="#ffffff", band="#d8c8a8", cuff="#e4dccb", stitch="#c8b890", seam="#d0c6b0", light2="#ffffff"),
        hair=dict(color="#e8e4e8", front=0.04, grow=0.12),
        moustache=False, beard=dict(color="#e4e0ea", dark="#9a96a8"), beard8=None,
        costume="kanzu14", robe_frac=0.80, robe_flare=0.12,
        sleeve=dict(color="#f0e8d6", dark="#c4b89c", cuff="#f0e8d6", len=0.84, w=0.17),
        shorts=dict(color="#f0e8d6", dark="#c4b89c", cuff="#f0e8d6", len=0.90, w=0.12),
        boots=dict(color="#6a4a32", cuff="#6a4a32", h=0.04, toe=0.15, soft=True),
        colors=dict(base="#f0e8d6", dark="#c4b89c", vest="#6a7a58", button="#d8c6a0", pants="#f0e8d6"),
    ),
    # the youth: lanky, red tee, cap
    "youth14": _mk(
        "worker1", seed=146.6, build="slim",
        torso_w=0.58, torso_h=1.00, leg=1.38, limb_w=0.054, mouth="grin", cheeks="#eba08a",
        hat="newsboy", hat_style="flatnews", hat_tilt=6.0,
        hat_colors=dict(base="#3a6a9a", dark="#244668", light="#5a8aba", shine="#a8c8e8", visor="#2a4e72"),
        hair=dict(color="#1f1818", front=0.08, grow=0.22),
        costume="tee14",
        sleeve=dict(color="#c9453a", dark="#962a22", cuff="#d86a5a", len=0.50, w=0.14, roll=True),
        shorts=dict(color="#4a5a72", dark="#2e3a50", cuff="#6a7a92", len=0.64, w=0.13),
        boots=dict(color="#2a2630", cuff="#2a2630", h=0.05, toe=0.15),
        colors=dict(base="#c9453a", dark="#962a22", collar="#962a22", print="#ffd0a0", pants="#4a5a72", rope="#c8b890"),
    ),
}

CANVAS14 = {
    "farmer14": (-1.875, -4.50, 1.875, 0.125),
    "uncle14": (-2.0625, -4.625, 2.0625, 0.1875),
    "woman14": (-1.75, -4.4375, 1.75, 0.25),
    "kid14": (-1.625, -3.75, 1.625, 0.125),
    "oldman14": (-1.75, -4.3125, 1.75, 0.1875),
    "youth14": (-1.875, -4.625, 1.875, 0.125),
}


# ============================================================================= the swollen nose
def _face(k, C, P_, white):
    svg, L = _O14["_face"](k, C, P_, white)
    if C is None or not C.get("_cast14") or _POSE14["nose"] <= 0.01:
        return svg, L
    return svg + _nose_swell(k, L, P_, _POSE14["nose"], _POSE14["t"]), L


def _nose_swell(k, L, P_, n, t):
    """comic stung nose: from a pink tip (n 0.05) to a fat, shiny, trunk-like nose that hangs down over the mouth and curls at
    the tip (n 1), with the little sting mark and a few red lumps.  Drawn over the face, mouth under it still readable at n<0.5."""
    yaw = P_["yaw"] if isinstance(P_, dict) else 0.0
    cx = L["mx"] + 0.02 * yaw
    top = L["ey"] + 0.06
    e = n * n * (3 - 2 * n)
    ln = 0.06 + 0.36 * e                        # length below the root
    w = 0.050 + 0.175 * e                       # half width at the tip bulb
    wr = 0.040 + 0.045 * e                      # half width at the root
    curl = 0.24 * e * (1.0 if yaw >= -0.05 else -1.0)
    sway = 0.012 * math.sin(t * 2 * math.pi) * e
    ink = k.ink
    c0, c1, c2 = SKIN_TRUNK_PINK["light"], SKIN_TRUNK_PINK["base"], SKIN_TRUNK_PINK["dark"]
    # centre line: straight, then curling toward the facing side
    pts_l, pts_r = [], []
    N = 9
    for i in range(N + 1):
        u = i / N
        x = cx + curl * u * u + sway * u
        y = top + ln * u
        ww = wr + (w - wr) * (u ** 1.6) * (1.0 + 0.10 * math.sin(u * 3.14))
        if i == N:
            ww *= 0.8
        pts_l.append((x - ww, y))
        pts_r.append((x + ww, y))
    tipx, tipy = cx + curl + sway, top + ln + w * 0.55
    path = P._smooth_open(pts_l) + " Q%.4f,%.4f %.4f,%.4f" % (tipx - w * 0.9, tipy + w * 0.2, tipx, tipy) + " Q%.4f,%.4f %.4f,%.4f" % (tipx + w * 0.9, tipy + w * 0.2, pts_r[-1][0], pts_r[-1][1])
    rr = list(reversed(pts_r))
    path += " L" + P._smooth_open(rr)[1:] + " Z"
    u = k.uid
    k.defs.append('<linearGradient id="%s_c14nsg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(c0), k.c(c1), k.c(c2)))
    o = ['<path d="%s" fill="url(#%s_c14nsg)" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (path, u, ink)]
    # nostril dots and wrinkle rings like a trunk
    if e > 0.15:
        rings = int(2 + 5 * e)
        for i in range(rings):
            uu = 0.25 + 0.65 * i / max(1, rings - 1)
            x = cx + curl * uu * uu + sway * uu
            y = top + ln * uu
            ww = (wr + (w - wr) * (uu ** 0.7)) * 0.85
            o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>'
                     % (x - ww, y, x, y + 0.03 * e + 0.01, x + ww, y, k.c(c2)))
    for s in (-1, 1):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.95"/>' % (tipx + s * w * 0.38, tipy - w * 0.25, 0.020 + 0.022 * e, 0.014 + 0.016 * e, ink))
    # shine
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="%.4f" stroke-linecap="round" opacity="0.8"/>'
             % (cx - wr * 0.5, top + 0.04, cx - wr * 0.7 + curl * 0.2, top + ln * 0.5, cx - w * 0.55 + curl * 0.8, top + ln * 0.85, 0.012 + 0.008 * e))
    # the sting: a small dark point with three lines, a few lumps
    sx, sy = cx + wr * 0.4, top + 0.06 + 0.1 * e
    if n > 0.25:
        o.append('<path d="M%.4f,%.4f l0.012,0.040" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (sx, sy, ink))
        o.append('<path d="M%.4f,%.4f l-0.022,-0.010 M%.4f,%.4f l0.0,-0.026 M%.4f,%.4f l0.022,-0.010" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>'
                 % (sx, sy, sx, sy, sx, sy, k.c(c2)))
    for (dx_, dy_, r_) in ((-0.55, 0.45, 0.022), (0.5, 0.62, 0.018), (-0.2, 0.30, 0.014)):
        if e > 0.35:
            o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.6"/>' % (cx + dx_ * w + curl * dy_ * dy_, top + ln * dy_, r_ * (0.5 + e), k.c(c2)))
    # a rosy halo on the cheeks around it
    if e > 0.2:
        for s in (-1, 1):
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.07" ry="0.045" fill="%s" opacity="%.2f"/>' % (cx + s * (w + 0.09), top + 0.12, k.c("#f08a8a"), 0.35 * e))
    for (x, y) in ((cx - w * 1.1, top + ln * 0.9), (cx + w * 1.1 + curl, top + ln), (cx + curl, tipy + 0.03)):
        k.ext.append((x, y, 0.03))
    return "".join(o)


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE14["nose"] = _f(g("nose_swell"), 0.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE14["t"] = t if math.isfinite(t) else 0.0
    return _O14["_norm"](C, pose)


# ============================================================================= props (own local frames; hand at (0, 0))
def _tin_roof(k, x0, x1, y0, y1, ridge=0.04):
    """corrugated tin shade roof: a shallow gable (ridge at the middle) seen from the side, ribs, a light edge."""
    g = _lin(k, "c14rf", TIN["light"], TIN["base"], TIN["dark"], x0, 0, x1, 0)
    xm = (x0 + x1) / 2
    d = "M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (x0, y1, x0 + 0.10, y0 + ridge, x1 - 0.10, y0 + ridge, x1, y1)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, g, k.ink)]
    n = int((x1 - x0) / 0.075)
    rib = "".join("M%.4f,%.4f L%.4f,%.4f " % (x0 + 0.12 + i * 0.075 * (x1 - x0 - 0.24) / ((n - 1) * 0.075) , y0 + ridge + 0.012, x0 + 0.05 + i * (x1 - x0 - 0.10) / (n - 1), y1 - 0.012) for i in range(n))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" opacity="0.8" fill="none"/>' % (rib, k.c(TIN["dark"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (x0 + 0.14, y0 + ridge + 0.020, x1 - 0.16, y0 + ridge + 0.020))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.35"/>' % (x0 + 0.02, y1 - 0.045, x1 - 0.02, y1 - 0.045, x1, y1, x0, y1, k.c(TIN["dark"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x0 + 0.10, y0 + ridge, x1 - 0.10, y0 + ridge, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (x0 - 0.01, y1 + 0.004, x1 + 0.01, y1 + 0.004, k.ink))
    return "".join(o)


HIVE_L, HIVE_H = 1.50, 0.46          # a top-bar hive body, D (about 0.9 m x 0.27 m at 0.58 m / D)


def _hive_body(k, roof=True, bees=0.0, open_top=False, bars=True):
    """a Kenyan top-bar hive seen from the side, hung by its two ropes: a long trapezoid wooden box (wider at the top), planks,
    entrance holes with a landing strip, the shade roof of corrugated tin above.  Origin = the hanging point on the top bar
    (centre of the top edge of the box); the box runs from y 0 to HIVE_H; the roof sits above (y -0.20 .. -0.02)."""
    L2 = HIVE_L / 2
    g = _lin(k, "c14hv", WOOD["light"], WOOD["base"], WOOD["dark"], -L2, 0, L2, 0)
    o = []
    # hanging ropes up to the roof + the wire loop
    if roof:
        for x in (-L2 * 0.62, L2 * 0.62):
            o.append('<path d="M%.4f,0 L%.4f,-0.05" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x, x, k.ink))
            o.append('<path d="M%.4f,0 L%.4f,-0.05" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x, x, k.c("#d2b98a")))
    # body: trapezoid, top wider than the bottom, ends slightly sloped
    body = [(-L2, 0.0), (L2, 0.0), (L2 - 0.11, HIVE_H), (-L2 + 0.11, HIVE_H)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(body), g, k.ink))
    # planks and grain
    for yy, op in ((HIVE_H * 0.36, 0.8), (HIVE_H * 0.70, 0.8)):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.009" opacity="%.2f"/>' % (-L2 + 0.03 + 0.11 * yy / HIVE_H, yy, L2 - 0.03 - 0.11 * yy / HIVE_H, yy, k.c(WOOD["deep"]), op))
    o.append('<path d="M%.4f,%.4f q0.14,-0.012 0.28,0.0 M%.4f,%.4f q0.12,0.01 0.22,-0.004" fill="none" stroke="%s" stroke-width="0.007" opacity="0.7"/>'
             % (-L2 * 0.7, HIVE_H * 0.22, L2 * 0.1, HIVE_H * 0.55, k.c(WOOD["deep"])))
    o.append('<path d="M%.4f,0.030 L%.4f,0.030" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (-L2 + 0.05, L2 - 0.05, k.c(WOOD["light"])))
    # top bar strip (the hanging bar) along the top edge
    o.append('<rect x="%.4f" y="-0.034" width="%.4f" height="0.040" rx="0.010" fill="%s" stroke="%s" stroke-width="0.016"/>' % (-L2 - 0.02, HIVE_L + 0.04, k.c(WOOD["base"]), k.ink))
    if bars:
        for i in range(11):
            x = -L2 + 0.06 + i * (HIVE_L - 0.12) / 10
            o.append('<path d="M%.4f,-0.034 L%.4f,0.006" stroke="%s" stroke-width="0.006" opacity="0.8"/>' % (x, x, k.c(WOOD["deep"])))
    # entrance holes near one end, landing strip
    for i, x in enumerate((-L2 * 0.82, -L2 * 0.66, -L2 * 0.50)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.026" ry="0.022" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x + 0.04, HIVE_H * 0.30, k.c("#2a1a10"), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (-L2 * 0.92, HIVE_H * 0.46, -L2 * 0.44, HIVE_H * 0.46, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % (-L2 * 0.92, HIVE_H * 0.46, -L2 * 0.44, HIVE_H * 0.46, k.c(WOOD["light"])))
    # the wire through the bar (the series' wire), a little rope knot
    o.append('<circle cx="0" cy="-0.014" r="0.018" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#d2b98a"), k.ink))
    if roof:
        o.append(_tin_roof(k, -L2 - 0.12, L2 + 0.12, -0.26, -0.06, 0.05))
    return "".join(o)


HIVE_TIP = HIVE_H + 0.02


def _hivebox_body(k):
    """the EMPTY hive box (no roof, no bees), carried by its side: an open trapezoid trough with the top bars laid across it, a
    dark hollow inside and a pale rope handle on the near side.  Origin = the carrying point (centre of the top edge)."""
    L2 = HIVE_L / 2
    g = _lin(k, "c14hb", WOOD["light"], WOOD["base"], WOOD["dark"], -L2, 0, L2, 0)
    o = []
    # inside hollow (seen slightly from above): a parallelogram strip above the front face
    o.append('<path d="M%.4f,-0.075 L%.4f,-0.075 L%.4f,0.0 L%.4f,0.0 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (-L2 + 0.05, L2 - 0.05, L2, -L2, k.c("#4a3220"), k.ink))
    for i in range(7):
        x = -L2 + 0.14 + i * (HIVE_L - 0.28) / 6
        o.append('<path d="M%.4f,-0.075 L%.4f,0.0" stroke="%s" stroke-width="0.016"/>' % (x, x - 0.03 * (1 if x > 0 else -1) * 0.0, k.c(WOOD["light"])))
        o.append('<path d="M%.4f,-0.072 L%.4f,-0.004" stroke="%s" stroke-width="0.006"/>' % (x, x, k.ink))
    body = [(-L2, 0.0), (L2, 0.0), (L2 - 0.11, HIVE_H), (-L2 + 0.11, HIVE_H)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(body), g, k.ink))
    for yy in (HIVE_H * 0.36, HIVE_H * 0.70):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.009" opacity="0.8"/>' % (-L2 + 0.03 + 0.11 * yy / HIVE_H, yy, L2 - 0.03 - 0.11 * yy / HIVE_H, yy, k.c(WOOD["deep"])))
    for i, x in enumerate((-L2 * 0.82, -L2 * 0.66, -L2 * 0.50)):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.026" ry="0.022" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x + 0.04, HIVE_H * 0.30, k.c("#2a1a10"), k.ink))
    # rope handle over the middle
    o.append('<path d="M-0.16,0.04 Q0,-0.20 0.16,0.04" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.16,0.04 Q0,-0.20 0.16,0.04" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % k.c("#e0cc9c"))
    return "".join(o)


def _wirecoil_body(k):
    """a coil of fencing wire (a fat bundle of loops seen from the side, wire ends sticking out), hanging on the forearm: the
    hand is inside the loop at (0, 0), the coil centred 0.22 below."""
    o = []
    cy = 0.24
    for i, (rx, ry, dx) in enumerate(((0.28, 0.30, 0.0), (0.27, 0.29, 0.020), (0.26, 0.28, 0.038), (0.25, 0.27, 0.054), (0.24, 0.26, 0.068))):
        a = "#ffffff" if i == 0 else None
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.036"/>' % (dx - 0.03, cy, rx * 0.62, ry, k.ink))
    for i, (rx, ry, dx) in enumerate(((0.28, 0.30, 0.0), (0.27, 0.29, 0.020), (0.26, 0.28, 0.038), (0.25, 0.27, 0.054), (0.24, 0.26, 0.068))):
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="none" stroke="%s" stroke-width="0.020"/>' % (dx - 0.03, cy, rx * 0.62, ry, k.c(WIRE["base"] if i % 2 else WIRE["light"])))
    o.append('<path d="M-0.20,0.06 Q-0.12,-0.02 -0.04,-0.02 M0.12,0.46 Q0.20,0.55 0.34,0.50" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.20,0.06 Q-0.12,-0.02 -0.04,-0.02 M0.12,0.46 Q0.20,0.55 0.34,0.50" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % k.c(WIRE["light"]))
    o.append('<path d="M-0.20,0.14 Q-0.16,0.40 -0.14,0.44" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>')
    return "".join(o)


def _flame(k, x, y, t, s=1.0):
    """a flat three-layer flame whose tip sways with t (always pointing up on screen)."""
    sw = 0.022 * math.sin(t * 2 * math.pi) * s
    sw2 = 0.016 * math.sin(t * 4 * math.pi + 1.3) * s
    o = []
    for (w, h, col, dy) in ((0.115, 0.30, FLAME["outer"], 0.0), (0.082, 0.22, FLAME["mid"], 0.02), (0.045, 0.13, FLAME["core"], 0.04)):
        w, h, dy = w * s, h * s, dy * s
        d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
             % (x - w, y + dy, x - w * 1.15, y + dy - h * 0.45, x - w * 0.2 + sw2, y + dy - h * 0.7, x + sw, y + dy - h,
                x + w * 0.3 + sw2, y + dy - h * 0.65, x + w * 1.1, y + dy - h * 0.4, x + w, y + dy))
        d = d.replace("Z", "Q%.4f,%.4f %.4f,%.4f Z" % (x, y + dy + w * 0.9, x - w, y + dy))
        o.append('<path d="%s" fill="%s"%s stroke-linejoin="round"/>' % (d, k.c(col), (' stroke="%s" stroke-width="0.014"' % k.ink) if col == FLAME["outer"] else ""))
    return "".join(o)


def _pot_body(k):
    """a battered aluminium cooking pot (sufuria): round belly, rim, two ear handles; origin = the right ear handle where the hand
    grips it; the pot hangs to the left of it, always upright (as the paint pail)."""
    g = _lin(k, "c14pt", POTM["light"], POTM["base"], POTM["dark"], -0.50, 0, 0.0, 0)
    o = []
    body = "M-0.50,-0.10 Q-0.52,0.18 -0.40,0.28 Q-0.25,0.34 -0.10,0.28 Q0.0,0.18 -0.02,-0.10 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (body, g, k.ink))
    o.append('<ellipse cx="-0.26" cy="-0.10" rx="0.245" ry="0.050" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c(POTM["dark"]), k.ink))
    o.append('<ellipse cx="-0.26" cy="-0.095" rx="0.20" ry="0.032" fill="%s" opacity="0.9"/>' % k.c("#3a3a48"))
    o.append('<path d="M-0.46,0.02 Q-0.45,0.16 -0.38,0.22" fill="none" stroke="#ffffff" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>')
    o.append('<path d="M-0.18,0.12 q0.04,0.04 0.01,0.08 M-0.30,0.24 q0.04,0.02 0.08,0.0" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(POTM["dark"]))
    # ear handles
    o.append('<path d="M-0.02,-0.04 Q0.05,-0.06 0.06,0.0 Q0.05,0.05 -0.02,0.04" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.02,-0.04 Q0.05,-0.06 0.06,0.0 Q0.05,0.05 -0.02,0.04" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(POTM["light"]))
    o.append('<path d="M-0.50,-0.04 Q-0.57,-0.06 -0.58,0.0 Q-0.57,0.05 -0.50,0.04" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.50,-0.04 Q-0.57,-0.06 -0.58,0.0 Q-0.57,0.05 -0.50,0.04" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(POTM["light"]))
    return "".join(o)


def _spoon_body(k):
    """a long wooden cooking spoon (0.9 long), hand at the handle end (x 0), bowl at x 0.62 .. 0.92."""
    g = _lin(k, "c14sp", WOOD["light"], WOOD["base"], WOOD["dark"], 0, -0.04, 0, 0.04)
    o = ['<path d="M-0.08,-0.020 L0.64,-0.020 Q0.70,-0.075 0.80,-0.082 Q0.94,-0.082 0.94,0 Q0.94,0.082 0.80,0.082 Q0.70,0.075 0.64,0.020 L-0.08,0.020 Q-0.11,0 -0.08,-0.020 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<ellipse cx="0.80" cy="0" rx="0.085" ry="0.056" fill="%s" opacity="0.55"/>' % k.c(WOOD["dark"]))
    o.append('<path d="M0.0,-0.008 L0.58,-0.008" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c(WOOD["light"]))
    return "".join(o)


def _stick_body(k):
    """the uncle's walking stick (1.55 long), a crook handle at x 0 (a J hooking toward -y), a dark ferrule at the tip x 1.55."""
    g = _lin(k, "c14wk", WOOD["light"], WOOD["base"], WOOD["dark"], 0, -0.03, 0, 0.03)
    o = ['<path d="M-0.04,0 Q-0.16,-0.0 -0.18,-0.10 Q-0.16,-0.19 -0.05,-0.17" fill="none" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.04,0 Q-0.16,0.0 -0.18,-0.10 Q-0.16,-0.19 -0.05,-0.17" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c(WOOD["base"]))
    o.append('<path d="M-0.06,0 L1.50,0" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.06,0 L1.50,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % g)
    o.append('<path d="M0.04,-0.014 L1.44,-0.014" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c(WOOD["light"]))
    o.append('<path d="M1.46,-0.032 L1.56,-0.026 L1.56,0.026 L1.46,0.032 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#3a3236"), k.ink))
    o.append('<path d="M0.52,-0.026 q0.01,0.03 0,0.052 M0.98,-0.026 q-0.01,0.03 0,0.052" fill="none" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c(WOOD["dark"]))
    return "".join(o)


def _torch_body(k):
    """a home-made torch (0.95 long): a wooden stick, a fat rag bundle soaked in oil at the tip (x 0.80 .. 0.98) bound with wire.
    The flame is drawn by _prop (always upright)."""
    g = _lin(k, "c14tc", WOOD["light"], WOOD["base"], WOOD["dark"], 0, -0.03, 0, 0.03)
    o = ['<path d="M-0.10,-0.026 L0.84,-0.026 L0.84,0.026 L-0.10,0.026 Q-0.13,0 -0.10,-0.026 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    rag = "M0.74,-0.034 Q0.80,-0.09 0.90,-0.085 Q1.0,-0.07 0.99,-0.01 Q1.0,0.06 0.90,0.085 Q0.80,0.09 0.74,0.034 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (rag, k.c("#7a5a3e"), k.ink))
    o.append('<path d="M0.80,-0.07 Q0.84,0 0.80,0.07 M0.90,-0.08 Q0.94,0 0.90,0.08" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % k.c("#4a3220"))
    o.append('<path d="M0.84,-0.050 L0.84,0.050" stroke="%s" stroke-width="0.016"/><path d="M0.84,-0.050 L0.84,0.050" stroke="%s" stroke-width="0.008"/>' % (k.ink, k.c(WIRE["light"])))
    return "".join(o)


NEW_PROPS14 = ("tophive", "hivebox", "wirecoil", "torch14", "pot14", "spoon14", "stick14")
NEW_TIP14 = {"tophive": HIVE_TIP, "hivebox": HIVE_TIP, "wirecoil": 0.50, "torch14": 1.04, "pot14": 0.30, "spoon14": 0.94, "stick14": 1.56}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS14:
        return _O14["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    side = 1.0 if key == "r" else -1.0
    t = _POSE14["t"]

    def at(x, y):
        return (H[0] + x * sc, H[1] + y * sc)
    if kind in ("tophive", "hivebox"):
        # upright, hung at H on the top bar: the hand holds the bar, the box hangs below
        body = _hive_body(k, True) if kind == "tophive" else _hivebox_body(k)
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, body)
        for (x, y) in ((-HIVE_L / 2 - 0.1, -0.2), (HIVE_L / 2 + 0.1, -0.2), (-HIVE_L / 2, HIVE_H), (HIVE_L / 2, HIVE_H), (0, -0.28 if kind == "tophive" else -0.2)):
            k.ext.append(at(x, y) + (0.03,))
        an["hive_c_" + key] = at(0, HIVE_H / 2)
        an["hive_bottom_" + key] = at(0, HIVE_H)
        an["hive_top_" + key] = at(0, -0.26)
        return o, at(0, HIVE_TIP)
    if kind == "wirecoil":
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0], H[1], sc, _wirecoil_body(k))
        for (x, y) in ((-0.35, 0.24), (0.34, 0.24), (0.0, 0.58), (0.34, 0.50)):
            k.ext.append(at(x, y) + (0.03,))
        an["wire_end_" + key] = at(0.34, 0.50)
        return o, at(0.34, 0.50)
    if kind == "pot14":
        s2 = sc * (1.0 if side > 0 else 1.0)
        # the pot hangs towards the body side (-x for the right hand); mirror for the left hand
        o = '<g transform="translate(%.4f %.4f) scale(%.4f %.4f)">%s</g>' % (H[0], H[1], side * sc, sc, _pot_body(k))
        for (x, y) in ((-0.58, 0.0), (0.06, 0.0), (-0.26, 0.31), (-0.26, -0.15)):
            k.ext.append(at(side * x, y) + (0.03,))
        an["pot_c_" + key] = at(side * -0.26, 0.08)
        an["pot_face_" + key] = at(side * -0.26, 0.15)
        return o, at(side * -0.26, 0.10)
    ca = math.cos(math.radians(ang))
    if kind == "spoon14":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _spoon_body(k))
        for e in ((-0.10, 0.0), (0.94, -0.08), (0.94, 0.08)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        tx, ty = _rot(0.80 * sc, 0.0, ang)
        an["spoon_" + key] = (H[0] + tx, H[1] + ty)
        tx, ty = _rot(NEW_TIP14["spoon14"] * sc, 0.0, ang)
        return o, (H[0] + tx, H[1] + ty)
    if kind == "stick14":
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _stick_body(k))
        for e in ((-0.20, -0.20), (1.56, 0.0), (0.8, 0.0)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        tx, ty = _rot(1.56 * sc, 0.0, ang)
        an["stick_tip_" + key] = (H[0] + tx, H[1] + ty)
        return o, (H[0] + tx, H[1] + ty)
    # torch14
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _torch_body(k))
    hx, hy = _rot(0.90 * sc, 0.0, ang)
    fx, fy = H[0] + hx, H[1] + hy - 0.06 * sc
    o = ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="0.18"/>' % (fx, fy - 0.12 * sc, 0.46 * sc, k.c(FLAME["mid"]))) + o + _flame(k, fx, fy, t, sc)
    for (x, y) in ((fx - 0.12 * sc, fy), (fx + 0.12 * sc, fy), (fx, fy - 0.34 * sc)):
        k.ext.append((x, y, 0.03))
    an["flame_" + key] = (fx, fy - 0.12 * sc)
    return o, (fx, fy - 0.1 * sc)


def _svg_wrap(uid, name, ink, tint, fn, *a):
    k = _ctx(uid, ink, tint)
    s = fn(k, *a)
    return '<g id="%s_%s"><defs>%s</defs>%s</g>' % (k.uid, name, "".join(k.defs), s)


def tophive_svg(uid="th", roof=True, ink=P.INK, tint=None):
    """the top-bar hive hung by its ropes under its tin roof: origin = the middle of the top bar, box y 0 .. HIVE_H (D), length HIVE_L."""
    return _svg_wrap(uid, "hive", ink, tint, _hive_body, bool(roof))


def hivebox_svg(uid="hb", ink=P.INK, tint=None):
    return _svg_wrap(uid, "hbox", ink, tint, _hivebox_body)


def wirecoil_svg(uid="wc", ink=P.INK, tint=None):
    return _svg_wrap(uid, "coil", ink, tint, _wirecoil_body)


def torch_svg(uid="tc", t=0.0, ink=P.INK, tint=None):
    """the torch along +x with its flame at x 0.90 (flame drawn upright)."""
    k = _ctx(uid, ink, tint)
    s = _torch_body(k) + _flame(k, 0.90, -0.06, t)
    return '<g id="%s_torch"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s)


def pot_svg(uid="pt", ink=P.INK, tint=None):
    return _svg_wrap(uid, "pot", ink, tint, _pot_body)


def spoon_svg(uid="sp", ink=P.INK, tint=None):
    return _svg_wrap(uid, "spoon", ink, tint, _spoon_body)


def stick_svg(uid="wk", ink=P.INK, tint=None):
    return _svg_wrap(uid, "stick", ink, tint, _stick_body)


# ============================================================================= elephants: flat 2D puppets in the same ink / flat-fill style
# One drawing function, two views (side, front).  Design is in metres (y up, matriarch shoulder 3.3 m, origin on the ground under the
# shoulder), converted to D (1 D = 0.583 m) at the end, so the sizes stay true: matriarch 5.66 D at the shoulder, farmer 3.0 D tall.
S_D = 1.0 / M_PER_D
SPEC14 = {
    #            scale tusk ear   baby  hide shift (lightness)  notch  wrinkle
    "matriarch":  dict(s=1.00, tusk=1.15, ear=1.00, baby=0.0, hide="mat", notch=0, wr=1.0, lash=1),
    "elephant_b": dict(s=0.86, tusk=0.50, ear=1.02, baby=0.0, hide="cow", notch=0, wr=0.7, lash=1),
    "elephant_c": dict(s=0.93, tusk=0.80, ear=0.96, baby=0.0, hide="bull", notch=1, wr=0.8, lash=0),
    "elephant_d": dict(s=0.77, tusk=0.28, ear=1.04, baby=0.0, hide="lilac", notch=0, wr=0.5, lash=1),
    "calf":       dict(s=0.36, tusk=0.0, ear=1.00, baby=1.0, hide="baby", notch=0, wr=0.2, lash=1),
}
HIDES = {
    "mat":   dict(base="#9b97ac", light="#b9b6c8", dark="#6c6882", deep="#4a4762"),
    "cow":   dict(base="#a4a0b2", light="#c2bfd0", dark="#726e88", deep="#4e4b66"),
    "bull":  dict(base="#9a9693", light="#b8b5b2", dark="#6c6864", deep="#4a4642"),
    "lilac": dict(base="#a79ab6", light="#c6bcd4", dark="#766a8a", deep="#52486a"),
    "baby":  dict(base="#aaa4ba", light="#cbc6d8", dark="#7c7692", deep="#58526e"),
}
DUST = "#c49a7c"
EXPR_E = ("calm", "happy", "curious", "alarmed", "trumpet", "shut", "grumpy")
TRUNKS = {                      # a0 (deg at the root), a1 (deg at the tip), curl (extra bend at the tip), length factor
    "hang":    (-62, -98, 0.25, 1.00),
    "sniff":   (-28, -58, 0.30, 1.00),
    "forward": (6, -12, 0.10, 1.00),
    "reach":   (22, 8, 0.20, 1.00),
    "raised":  (70, 100, 0.70, 1.00),
    "curl":    (-40, 40, 1.10, 0.95),
    "swing":   (-50, -80, 0.40, 1.00),
    "tuck":    (-75, -150, 0.9, 0.9),
}
ENUM_E = ("view", "phase", "stride", "gait", "trunk", "trunk_a0", "trunk_a1", "trunk_curl", "ear_flare", "head_dip", "head_tilt", "mouth_open",
          "push", "lean", "expr", "blink", "tail", "t", "mirror", "tint", "ink", "squash", "head_turn", "crouch", "sway", "dust")


_CIDS = {}


def _cid(k, tag):
    """a clip-path id unique inside one figure (counter per uid, reset by elephant_figure: deterministic output)."""
    _CIDS[k.uid] = _CIDS.get(k.uid, 0) + 1
    return "%s_%s%d" % (k.uid, tag, _CIDS[k.uid])


def _hc(h, k, key):
    return k.c(HIDES[h][key])


def _rotp(x, y, a, cx, cy):
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    return (cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c)


def _ink_poly(k, pts, fill, w=0.030, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"%s/>' % (P._smooth_closed(pts), fill, k.ink, w, extra)


def _shaded(k, pts, hide, K, w=0.030, shade=0.50, dxy=(0.10, 0.13)):
    """a hide-coloured shape with the lower-right crescent in the dark tone (flat fill + one crescent, like the heads) and an ink rim."""
    cid = _cid(k, "ec")
    d = P._smooth_closed(pts)
    lit = P._smooth_closed([(x - dxy[0] * K, y - dxy[1] * K) for x, y in pts])
    return ('<path d="%s" fill="%s"/><clipPath id="%s"><path d="%s"/></clipPath>'
            '<g clip-path="url(#%s)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
            % (d, _hc(hide, k, "dark"), cid, d, cid, d, _hc(hide, k, "dark"), lit, _hc(hide, k, "base"), d, k.ink, w))


def _tube(cl, w0, w1, power=0.9):
    """(centre line points, half widths) -> left and right outline lists."""
    n = len(cl)
    L, R, W = [], [], []
    for i, (x, y) in enumerate(cl):
        u = i / (n - 1)
        if i == 0:
            dx, dy = cl[1][0] - x, cl[1][1] - y
        elif i == n - 1:
            dx, dy = x - cl[i - 1][0], y - cl[i - 1][1]
        else:
            dx, dy = cl[i + 1][0] - cl[i - 1][0], cl[i + 1][1] - cl[i - 1][1]
        m = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / m, dx / m
        w = w1 + (w0 - w1) * (1 - u) ** power
        L.append((x + nx * w, y + ny * w))
        R.append((x - nx * w, y - ny * w))
        W.append(w)
    return L, R, W


def _eye(k, x, y, r, expr, blink, lash, K, ink, baby, lidcol="#9b97ac"):
    """a big friendly eye: dark round pupil with a big glint, brow ridge and lashes; expr changes lids and brows."""
    o = []
    if blink >= 2 or expr == "shut":
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (x - r, y, x, y + r * 0.7, x + r, y - r * 0.05, ink))
        if lash:
            for dx_ in (-0.7, -0.2, 0.35):
                o.append('<path d="M%.4f,%.4f l%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (x + dx_ * r, y + r * 0.4, dx_ * r * 0.3, r * 0.4, ink))
        return "".join(o)
    big = {"alarmed": 1.35, "trumpet": 1.0, "curious": 1.12, "happy": 1.0, "grumpy": 0.9, "calm": 1.0}.get(expr, 1.0)
    rr = r * big
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (x, y, rr * 1.08, rr, k.c("#fbf1e8"), ink))
    pr = rr * (0.70 if expr != "alarmed" else 0.45)
    px_ = x + {"curious": 0.18, "alarmed": 0.0}.get(expr, 0.1) * rr
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (px_, y + 0.04 * rr, pr, k.c("#2a1a1c")))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="0.8"/>'
             % (px_ - pr * 0.35, y - pr * 0.30, pr * 0.34, px_ + pr * 0.30, y + pr * 0.35, pr * 0.14))
    # lid
    lid = {"calm": 0.14, "happy": 0.12, "curious": 0.08, "alarmed": -0.2, "trumpet": 0.35, "grumpy": 0.45}.get(expr, 0.25)
    if lid > 0:
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                 % (x - rr * 1.12, y - rr * 0.1, x, y - rr * 1.35, x + rr * 1.12, y - rr * 0.1,
                    x + rr * 1.12, y - rr * 0.1, x, y - rr * (1.0 - 2 * lid) + rr * 0.0, x - rr * 1.12, y - rr * 0.1, k.c(lidcol), ink))
    if expr == "happy":     # happy lower lid arc (smiling eye)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.8"/>' % (x - rr * 0.9, y + rr * 0.55, x, y + rr * 1.15, x + rr * 0.9, y + rr * 0.55, ink))
    if lash:
        for dx_, dy_ in ((-0.95, -0.5), (-0.55, -0.9), (-0.1, -1.05)):
            o.append('<path d="M%.4f,%.4f l%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
                     % (x + dx_ * rr, y + dy_ * rr * 0.95, dx_ * rr * 0.30, dy_ * rr * 0.38, ink))
    # brow
    bt = {"alarmed": (-0.9, -1.9), "curious": (-0.7, -1.7), "grumpy": (0.15, -1.1), "happy": (-0.5, -1.5), "trumpet": (-0.3, -1.4)}.get(expr, (-0.2, -1.5))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>'
             % (x - rr * 1.2, y + bt[0] * rr * 0.9 - rr * 0.9, x - rr * 0.1, y + bt[1] * rr * 0.75, x + rr * 1.3, y - rr * 1.2 + (0.5 * bt[0] * rr if expr == "grumpy" else 0), ink))
    return "".join(o)


def _smoothstep(u):
    u = _clamp(u, 0.0, 1.0)
    return u * u * (3 - 2 * u)


def _foot_cycle(ph, A, L):
    """(dx, lift) of one foot at gait phase ph (0..1): stance 62 % moving back linearly, swing 38 % forward with an arc."""
    u = ph % 1.0
    if u < 0.62:
        return A * (1.0 - 2.0 * u / 0.62), 0.0
    v = (u - 0.62) / 0.38
    return -A + 2.0 * A * _smoothstep(v), L * math.sin(math.pi * v)


def _ep(pose):
    """normalised elephant pose."""
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    e = {}
    e["view"] = g("view") if g("view") in ("side", "front") else "side"
    e["phase"] = _num(g("phase"), 0.0)
    e["stride"] = _f(g("stride"), 0.0, 0.0, 1.6)
    e["gait"] = g("gait") if g("gait") in ("walk", "run") else "walk"
    tr = g("trunk")
    e["trunk"] = tr if isinstance(tr, str) and tr in TRUNKS else "hang"
    e["a0"], e["a1"], e["curl"], e["tl"] = TRUNKS[e["trunk"]]
    if g("trunk_a0") is not None:
        e["a0"] = _f(g("trunk_a0"), e["a0"], -180, 180)
    if g("trunk_a1") is not None:
        e["a1"] = _f(g("trunk_a1"), e["a1"], -200, 200)
    if g("trunk_curl") is not None:
        e["curl"] = _f(g("trunk_curl"), e["curl"], -1.5, 1.5)
    e["flare"] = _f(g("ear_flare"), 0.0, 0.0, 1.0)
    e["dip"] = _f(g("head_dip"), 0.0, -40.0, 40.0)
    e["htilt"] = _f(g("head_tilt"), 0.0, -40.0, 40.0)
    e["mouth"] = _f(g("mouth_open"), 0.0, 0.0, 1.0)
    e["push"] = _f(g("push"), 0.0, 0.0, 1.0)
    e["lean"] = _f(g("lean"), 0.0, -30.0, 30.0)
    ex = g("expr")
    e["expr"] = ex if isinstance(ex, str) and ex in EXPR_E else "calm"
    e["blink"] = int(_f(g("blink"), 0, 0, 2))
    e["tail"] = _f(g("tail"), 0.0, -1.0, 1.0)
    e["t"] = _num(g("t"), 0.0) if math.isfinite(_num(g("t"), 0.0)) else 0.0
    e["mirror"] = bool(g("mirror"))
    e["tint"] = g("tint")
    e["ink"] = g("ink") if isinstance(g("ink"), str) else P.INK
    sq = g("squash")
    if isinstance(sq, (tuple, list)) and len(sq) == 2:
        e["squash"] = (_f(sq[0], 1.0, 0.3, 2.5), _f(sq[1], 1.0, 0.3, 2.5))
    else:
        s1 = _f(sq, 1.0, 0.3, 2.5) if sq is not None else 1.0
        e["squash"] = (s1, s1)
    e["turn"] = _f(g("head_turn"), 0.0, -1.0, 1.0)
    e["crouch"] = _f(g("crouch"), 0.0, 0.0, 1.0)
    e["dust"] = _f(g("dust"), 1.0, 0.0, 1.0)
    return e


def _side(k, cast, e):
    sp = SPEC14[cast]
    s, hide = sp["s"], sp["hide"]
    K = s * S_D
    baby = sp["baby"]
    hs = 1.10 + 0.28 * baby                        # a calf's head is big (and every elephant's a little, for charm)
    ink = k.ink
    pts_all = []

    def T(x, y):
        return (x * K, -y * K)

    def TT_(pts):
        return [T(x, y) for x, y in pts]

    def X(*ps):
        pts_all.extend(ps)
    ph = e["phase"]
    st = e["stride"] * (1.3 if e["gait"] == "run" else 1.0)
    A = 0.62 * st * (1.0 if e["gait"] == "walk" else 1.25)
    Lf = 0.42 * min(1.0, st) * (1.0 if e["gait"] == "walk" else 1.5)
    bob = (0.035 * math.sin(4 * math.pi * ph) * min(1.0, st)) * (1.0 if e["gait"] == "walk" else 2.2)
    push = e["push"]
    lean = e["lean"] + 5.0 * push
    # legs: (top x, top y, phase offset, near?)
    legs = [("rf", 0.50, 0.25, True, 1), ("rr", -1.85, 0.0, True, 0), ("lf", 0.50, 0.75, False, 1), ("lr", -1.85, 0.5, False, 0)]
    pivot = T(-1.8, 1.9)

    def body_xf(px, py):          # the upper-body transform in D space: tilt about the rear hip + bob
        x, y = _rotp(px, py, lean, pivot[0], pivot[1])
        return (x + 0.10 * push * S_D * s, y - bob * K)
    foot = {}
    leg_svg = {True: [], False: []}
    for (nm, tx, po, near, front) in legs:
        dx, lift = _foot_cycle(ph + po, A, Lf) if st > 0.01 else (0.0, 0.0)
        fx = tx + 0.04 + dx
        if push > 0:
            fx += (0.10 if front else -0.55) * push * (1.0 if near else 0.9)
        fy = lift
        top = body_xf(*T(tx, 2.15))
        foot[nm] = (T(fx, fy), top, near, front, lift)
    # ---------- tail
    tsw = 0.30 * math.sin(e["t"] * 2 * math.pi + 0.7) + 0.55 * e["tail"] + 0.10 * math.sin(4 * math.pi * ph)
    tb = body_xf(*T(-2.62, 2.70))
    tl = 1.55 * (1.0 - 0.15 * baby)
    tt = body_xf(*T(-2.75 - 0.35 * tsw, 2.70 - tl * (1.0 - 0.45 * abs(e["tail"]))))
    tmid = ((tb[0] + tt[0]) / 2 - 0.12 * K * (1 - tsw), (tb[1] + tt[1]) / 2)
    o = []
    tailsvg = ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (tb + tmid + tt + (ink, 0.085 * K + 0.030)))
    tailsvg += ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (tb + tmid + tt + (_hc(hide, k, "base"), 0.085 * K)))
    ang = math.degrees(math.atan2(tt[1] - tmid[1], tt[0] - tmid[0]))
    tailsvg += ('<g transform="translate(%.4f %.4f) rotate(%.2f)"><path d="M0,0 Q0.06,-0.10 0.20,-0.10 Q0.30,0 0.20,0.10 Q0.06,0.10 0,0 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
                '<path d="M0.06,0 L0.22,0" stroke="%s" stroke-width="0.012" opacity="0.6"/></g>' % (tt[0], tt[1], ang, _hc(hide, k, "deep"), ink, ink))
    X(tb, tt, (tt[0] + 0.3 * K, tt[1] + 0.3 * K), (tt[0] - 0.3 * K, tt[1] + 0.3 * K))
    o.append(tailsvg)

    # ---------- legs (far ones first, darker)
    def leg(nm, shade):
        f, top, near, front, lift = foot[nm]
        ax, ay = f[0] + 0.0, f[1] - 0.20 * K          # the ankle above the foot pad
        wd = (0.66 if front else 0.72) * K
        bow = 0.05 * K * (1 if front else -1)
        mx_, my_ = (top[0] + ax) / 2 + bow, (top[1] + ay) / 2
        col = _hc(hide, k, "dark") if shade else _hc(hide, k, "base")
        d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (top + (mx_, my_) + (ax, ay))
        # the ink starts where the leg leaves the belly
        t0 = 0.45
        sx, sy = top[0] + (ax - top[0]) * t0 + bow * 0.5, top[1] + (ay - top[1]) * t0
        d2 = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % ((sx, sy) + ((sx + ax) / 2 + bow * 0.6, (sy + ay) / 2) + (ax, ay))
        s_ = ['<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % (d2, ink, wd + 0.060)]
        s_.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, col, wd))
        # darker shade strip on the right side of the leg
        s_.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt" opacity="%.2f" transform="translate(%.4f 0)"/>'
                  % (d2, _hc(hide, k, "dark"), wd * 0.30, 0.0 if shade else 0.9, wd * 0.36))
        # a knee wrinkle
        kx, ky = (sx + ax) / 2 + bow * 0.6, (sy + ay) / 2
        s_.append('<path d="M%.4f,%.4f q%.4f,0.03 %.4f,0" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>' % (kx - wd * 0.35, ky, wd * 0.35, wd * 0.7, ink))
        # foot pad + nails
        fw, fh = 0.42 * K, 0.17 * K
        fcx, fcy = f[0] + 0.05 * K * (1 if front else 0.4), f[1] - fh * 0.6
        s_.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
                  % (fcx - fw * 0.95, fcy - fh * 0.6, fcx - fw * 1.05, fcy + fh * 1.3, fcx, fcy + fh * 1.3, fcx + fw * 1.1, fcy + fh * 1.1, fcx + fw * 0.95, fcy - fh * 0.5,
                     fcx + fw * 0.80, fcy - fh * 0.9, k.c(DUST) if e["dust"] > 0.5 else col, ink) if False else
                  '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.026"/>' % (fcx, fcy, fw, fh, col, ink))
        if e["dust"] > 0.05:
            s_.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" opacity="%.2f"/>'
                      % (fcx - fw * 0.9, fcy - fh * 0.2, fcx, fcy - fh * 1.3, fcx + fw * 0.9, fcy - fh * 0.2, fcx + fw * 0.8, fcy + fh * 0.5, fcx, fcy + fh * 0.95, fcx - fw * 0.8, fcy + fh * 0.5, k.c(DUST), 0.5 * e["dust"]))
        for i in range(3):
            nxp = fcx + fw * (0.45 + 0.28 * i) * (1 if front or True else 1)
            s_.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.012"/>' % (nxp - 0.03 * K, fcy + fh * 0.25, 0.06 * K * 0.8, 0.05 * K, k.c("#efe6da"), ink))
        X((fcx - fw * 1.2, fcy + fh * 1.3), (fcx + fw * 1.3, fcy + fh * 1.3), (top[0] - wd, top[1]), (top[0] + wd, top[1]))
        return "".join(s_)
    for nm in ("lf", "lr"):
        o.append(leg(nm, True))

    # ---------- torso
    body = [(0.35, 3.18), (-0.20, 3.30), (-1.00, 3.14), (-1.80, 3.20), (-2.45, 2.90), (-2.72, 2.30), (-2.58, 1.62), (-2.20, 1.28), (-1.30, 1.16),
            (-0.30, 1.14), (0.55, 1.26), (1.02, 1.68), (1.14, 2.40), (0.96, 3.00)]
    if e["crouch"] > 0:
        body = [(x, y - 0.25 * e["crouch"]) for x, y in body]
    bpts = [body_xf(*T(x, y)) for x, y in body]
    X(*bpts)
    upper = [_shaded(k, bpts, hide, K, 0.030)]
    # belly and hip wrinkles, withers, spine
    wr = sp["wr"]
    wrk = []
    for (x0, y0, x1, y1, bw) in ((-2.05, 1.95, -2.30, 1.55, 0.2), (-1.7, 2.1, -2.0, 1.7, 0.2), (0.3, 2.3, 0.1, 1.8, 0.25), (-0.1, 1.55, -0.6, 1.4, 0.15), (-1.1, 2.4, -1.3, 2.0, 0.25)):
        a = body_xf(*T(x0, y0))
        b = body_xf(*T(x1, y1))
        wrk.append("M%.4f,%.4f q%.4f,%.4f %.4f,%.4f" % (a[0], a[1], (b[0] - a[0]) * 0.2 - 0.05, (b[1] - a[1]) * 0.7, b[0] - a[0], b[1] - a[1]))
    upper.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="%.2f"/>' % ("".join(wrk), ink, 0.5 * wr))
    o.append("".join(upper))
    for nm in ("rf", "rr"):
        o.append(leg(nm, False))

    # ---------- head group: rotates about the neck, scaled for a calf
    npv = body_xf(*T(0.80, 2.75))
    dip = e["dip"] + 0.0
    headg = []
    hx = lambda x, y: (lambda p: (npv[0] + (p[0] - npv[0]) * hs, npv[1] + (p[1] - npv[1]) * hs))(_rotp(*body_xf(*T(x, y)), dip, npv[0], npv[1]))
    hd = [(0.65, 3.20), (0.95, 3.64), (1.45, 3.80), (1.95, 3.58), (2.26, 3.08), (2.38, 2.55), (2.32, 2.10), (2.05, 1.84), (1.62, 1.74), (1.22, 1.94), (0.95, 2.40), (0.66, 2.90)]
    hp = [hx(x, y) for x, y in hd]
    X(*hp)
    ear_s = sp["ear"] * (1.0 + 0.22 * baby)
    fl = e["flare"]
    # ears: the far ear peeks out behind the head when flared; the near ear lies over the shoulder (relaxed) or swings forward (flared)
    def ear_pts(rot, scl, root=(1.02, 3.18)):
        base = [(1.02, 3.42), (0.55, 3.84), (-0.15, 3.66), (-0.52, 3.05), (-0.40, 2.30), (0.10, 1.88), (0.58, 2.22), (0.96, 2.78), (1.10, 3.0)]
        if sp["notch"]:
            base = [(1.02, 3.42), (0.55, 3.84), (-0.10, 3.70), (-0.22, 3.50), (-0.14, 3.34), (-0.52, 3.05), (-0.40, 2.30), (0.10, 1.88), (0.58, 2.22), (0.96, 2.78), (1.10, 3.0)]
        out = []
        for (x, y) in base:
            xx = root[0] + (x - root[0]) * scl * ear_s
            yy = root[1] + (y - root[1]) * scl * ear_s
            xx, yy = _rotp(xx, yy, rot, root[0], root[1])
            out.append(hx(xx, yy))
        return out
    ear_near = ear_pts(-38.0 * fl, 1.0 + 0.16 * fl)
    ear_far = ear_pts(-70.0 * fl - 4.0, 1.0 + 0.10 * fl, (1.10, 3.20))
    if fl > 0.08:
        headg.append(_shaded(k, ear_far, "lilac" if False else hide, K, 0.026))
        headg.append('<path d="%s" fill="%s" opacity="%.2f"/>' % (P._smooth_closed(ear_far), k.c(HIDE["ear_d"]), 0.45 * fl))
    # tusks (far one behind the head)
    tuskL = sp["tusk"]
    tusk_tip = None

    def tusk(dx, dy, shade):
        if tuskL <= 0.01:
            return ""
        base0 = (2.05 + dx, 1.98 + dy)
        pts = []
        N = 9
        for i in range(N + 1):
            u = i / N
            x = base0[0] + tuskL * (0.82 * u + 0.05 * u * u)
            y = base0[1] - 0.20 * u + 0.60 * u ** 2.2 * tuskL * 0.9
            pts.append(hx(x, y))
        L, R, W = _tube(pts, 0.095 * K * (0.5 + 0.5 * min(1, tuskL)), 0.012, 0.9)
        d = P._smooth_open(L) + " L%.4f,%.4f " % (pts[-1][0] + 0.0, pts[-1][1] + 0.0) + P._smooth_open(list(reversed(R)))[1:] + " Z"
        col = IVORY["dark"] if shade else IVORY["base"]
        return ('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/><path d="%s" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>'
                % (d, k.c(col), ink, P._smooth_open([(p[0] + 0.0, p[1] - 0.02) for p in pts[1:6]]))), pts[-1]
    tf = tusk(0.14, 0.05, True)
    if tf:
        headg.append(tf[0])
        X(tf[1])
    # the head itself
    headg.append(_shaded(k, hp, hide, K * hs, 0.030))
    # forehead + brow wrinkles
    wrk = []
    for (x0, y0, x1, y1) in ((1.15, 3.55, 1.55, 3.62), (1.30, 3.30, 1.75, 3.40), (1.0, 2.85, 1.25, 2.55), (1.55, 2.25, 1.75, 2.05)):
        a, b = hx(x0, y0), hx(x1, y1)
        wrk.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a + ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 0.025) + b))
    headg.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="%.2f"/>' % ("".join(wrk), ink, 0.45 * wr + 0.1))
    # baby tuft of hair
    if baby:
        c = hx(1.35, 3.80)
        headg.append('<path d="M%.4f,%.4f q-0.06,-0.14 -0.02,-0.20 q0.04,0.08 0.06,0.02 q0.02,-0.12 0.08,-0.16 q-0.02,0.12 0.0,0.16 q0.06,-0.08 0.10,-0.06 q-0.04,0.10 -0.08,0.24 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                     % (c[0] - 0.08, c[1] + 0.04, k.c("#5a4a52"), ink))
    # mouth / jaw: a pink open mouth under the trunk root
    mo = e["mouth"]
    mc = hx(2.00, 1.95)
    if mo > 0.05:
        mw, mh = 0.40 * K * hs, (0.06 + 0.26 * mo) * K * hs
        headg.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
                     % (mc[0] - mw * 0.5, mc[1] - 0.02, mc[0] - mw * 0.2, mc[1] + mh * 1.9, mc[0] + mw * 0.7, mc[1] + mh * 0.9, mc[0] + mw * 0.4, mc[1] - 0.06, mc[0] - mw * 0.5, mc[1] - 0.02, k.c("#8e3a4a"), ink))
        headg.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s"/>'
                     % (mc[0] - mw * 0.35, mc[1] + mh * 0.9, mc[0] - mw * 0.1, mc[1] + mh * 1.45, mc[0] + mw * 0.45, mc[1] + mh * 0.75, mc[0] + mw * 0.1, mc[1] + mh * 0.35, mc[0] - mw * 0.35, mc[1] + mh * 0.9, k.c("#e87a8a")))
    else:
        headg.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>'
                     % (mc[0] - 0.30 * K * hs * 0.6, mc[1] + 0.02, mc[0], mc[1] + (0.12 if e["expr"] in ("happy",) else 0.04) * K * hs, mc[0] + 0.22 * K * hs * 0.6, mc[1] - (0.10 if e["expr"] in ("happy",) else 0.0) * K * hs, ink))
    # trunk from the face
    root = (2.30, 2.46)
    rx_, ry_ = hx(*root)
    # trunk is built in design coordinates of the rotated head: convert the root back so a0 is relative to the head tilt
    trun = e["trunk"] == "raised" or e["mouth"] > 0.5
    L_ = 2.15 * e["tl"] * (1.0 - 0.38 * baby)
    # build the trunk in the head's own frame (design coordinates), then place it with the head transform
    tsvg, ttip, tcl = _trunk_head(k, hide, K, hs, hx, root, e, L_, baby, dip, trun)
    headg.append(tsvg)
    X(ttip, *tcl[::3])
    # near tusk over the trunk root
    tn = tusk(0.0, 0.0, False)
    if tn:
        headg.append(tn[0])
        X(tn[1])
        tusk_tip = tn[1]
    # near ear over the head side
    headg.append(_shaded(k, ear_near, hide, K, 0.030))
    cen = (sum(p[0] for p in ear_near) / len(ear_near), sum(p[1] for p in ear_near) / len(ear_near))
    inner = [(cen[0] + (p[0] - cen[0]) * 0.80, cen[1] + (p[1] - cen[1]) * 0.80) for p in ear_near]
    headg.append('<path d="%s" fill="%s" opacity="%.2f"/>' % (P._smooth_closed(inner), k.c(HIDE["ear"]), 0.25 + 0.50 * fl))
    veins = []
    r0 = ear_near[0]
    for p in (ear_near[3], ear_near[4], ear_near[5], ear_near[6]):
        veins.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (r0[0], r0[1] + 0.03, (r0[0] + p[0]) / 2 - 0.02, (r0[1] + p[1]) / 2 + 0.05, p[0] * 0.9 + cen[0] * 0.1, p[1] * 0.9 + cen[1] * 0.1))
    headg.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.5"/>' % ("".join(veins), k.c(HIDE["ear_d"])))
    # eye, cheek
    ec = hx(1.86, 2.98)
    er = 0.155 * K * hs * (1.0 + 0.25 * baby)
    headg.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.55"/>' % (ec[0] + 0.06 * K, ec[1] + 0.26 * K * hs, 0.22 * K * hs, 0.14 * K * hs, k.c("#e89aa0")))
    headg.append(_eye(k, ec[0], ec[1], max(er, 0.060), e["expr"], e["blink"], sp["lash"], K, ink, baby, HIDES[hide]["base"]))
    X((ec[0], ec[1] - 0.2))
    o.append("".join(headg))
    for nm in ("rf",):
        pass
    X(*[foot[n][0] for n in foot])
    # ---------- assemble: shift so that the head centre (rest) is at the origin
    hc = T(1.50, 2.80)
    fxm = (foot["rf"][0][0] + foot["rr"][0][0]) / 2
    feet_y = -hc[1]
    ox, oy = -hc[0], -hc[1]
    xs = [p[0] + ox for p in pts_all]
    ys = [p[1] + oy for p in pts_all]
    anchors = {}

    def A_(p):
        return (p[0] + ox, p[1] + oy)
    anchors["head"] = (0.0, 0.0)
    anchors["eye_r"] = A_(ec)
    anchors["eye_l"] = A_(ec)
    anchors["mouth"] = A_(mc)
    anchors["head_top"] = A_(hx(1.45, 3.80))
    anchors["hat_top"] = anchors["head_top"]
    anchors["trunk_tip"] = A_(ttip)
    anchors["trunk_base"] = A_(hx(*root))
    anchors["tusk_tip"] = A_(tusk_tip) if tusk_tip else A_(hx(2.4, 1.9))
    anchors["chest"] = A_(body_xf(*T(1.12, 2.0)))
    anchors["chest_push"] = A_(body_xf(*T(1.18, 2.35)))
    anchors["shoulder_top"] = A_(body_xf(*T(0.1, 3.30)))
    anchors["rump"] = A_(body_xf(*T(-2.72, 2.30)))
    anchors["tail_tip"] = A_(tt)
    anchors["hip"] = A_(body_xf(*T(-0.6, 1.2)))
    anchors["belly"] = anchors["hip"]
    anchors["ear_tip"] = A_(ear_near[1])
    for nm, an in (("foot_r", "rf"), ("foot_l", "lf"), ("knee_r", "rf"), ("knee_l", "lf")):
        f_, top_, *_x = foot[an]
        anchors[nm] = A_(f_) if nm.startswith("foot") else A_(((f_[0] + top_[0]) / 2, (f_[1] + top_[1]) / 2))
    anchors["feet"] = (A_(((foot["rf"][0][0] + foot["rr"][0][0] + foot["lf"][0][0] + foot["lr"][0][0]) / 4, 0.0))[0], feet_y)
    anchors["shoulder_r"] = A_(body_xf(*T(0.4, 2.8)))
    anchors["shoulder_l"] = anchors["shoulder_r"]
    anchors["elbow_r"] = anchors["knee_r"]
    anchors["elbow_l"] = anchors["knee_l"]
    anchors["hand_r"] = anchors["trunk_tip"]
    anchors["hand_l"] = anchors["trunk_base"]
    anchors["prop_tip_r"] = anchors["trunk_tip"]
    anchors["prop_tip_l"] = anchors["trunk_base"]
    return "".join(o), (ox, oy), anchors, (min(xs) - 0.08, min(ys) - 0.08, max(xs) + 0.08, max(ys) + 0.08), feet_y


def _trunk_head(k, hide, K, hs, hx, root, e, L_, baby, dip, trun):
    """the trunk placed through the head transform: built by integrating in design space, mapped by hx()."""
    # build the centre line in design metres from the root, with angles relative to the head tilt (dip rotates the whole head)
    N = 18
    x, y = root
    cl = [root]
    ds = L_ / N
    a0, a1, curl = e["a0"], e["a1"], e["curl"]
    sw = 7.0 * math.sin(e["t"] * 2 * math.pi) * (1.0 if not trun else 0.35) + 4.0 * e["htilt"] / 10.0
    for i in range(N):
        u = (i + 0.5) / N
        a = a0 + (a1 - a0) * u + curl * 70.0 * u ** 3 + sw * math.sin(u * math.pi)
        x += ds * math.cos(math.radians(a))
        y += ds * math.sin(math.radians(a))
        cl.append((x, y))
    P_ = [hx(px, py) for px, py in cl]
    P_ = [(px, min(py, -0.10 * K)) for px, py in P_]          # the trunk tip never goes below the ground
    wb = 0.52 * K * hs * (1.0 + 0.05 * baby)
    wt = 0.22 * K * hs * (1.0 + 0.4 * baby)
    return _trunk_draw(k, P_, wb, wt, hide, e["t"], trun, baby, K)


def _trunk_draw(k, P_, wb, wt, hide, t, trumpet, baby, K):
    """tapered tube along P_ (D-space centre line), shade on the lower-right side, wrinkle rings, open at the root (no seam line)."""
    N = len(P_) - 1
    L, R, W = _tube(P_, wb, wt, 0.45)
    tipc = P_[-1]
    ex, ey = tipc[0] - P_[-2][0], tipc[1] - P_[-2][1]
    em = math.hypot(ex, ey) or 1.0
    ex, ey = ex / em, ey / em
    if trumpet:
        for arr in (L, R):
            arr[-1] = (tipc[0] + (arr[-1][0] - tipc[0]) * 2.1, tipc[1] + (arr[-1][1] - tipc[1]) * 2.1)
            arr[-2] = (P_[-2][0] + (arr[-2][0] - P_[-2][0]) * 1.4, P_[-2][1] + (arr[-2][1] - P_[-2][1]) * 1.4)
    cap = (tipc[0] + ex * W[-1] * 1.25, tipc[1] + ey * W[-1] * 1.25)
    Rend = R[-1]
    d_open = P._smooth_open(L) + " Q%.4f,%.4f %.4f,%.4f " % (cap[0], cap[1], Rend[0], Rend[1]) + P._smooth_open(list(reversed(R)))[1:]
    d_ink = P._smooth_open(L[3:]) + " Q%.4f,%.4f %.4f,%.4f " % (cap[0], cap[1], Rend[0], Rend[1]) + P._smooth_open(list(reversed(R[3:])))[1:]
    mL = sum(p[0] - p[1] for p in L) / len(L)
    mR = sum(p[0] - p[1] for p in R) / len(R)
    sh = L if mL > mR else R
    lit = R if sh is L else L
    shade = P._smooth_open([(0.45 * a[0] + 0.55 * b[0], 0.45 * a[1] + 0.55 * b[1]) for a, b in zip(P_, sh)]) + " L" + P._smooth_open(list(reversed(sh)))[1:] + " Z"
    cid = _cid(k, "tr")
    o = ['<path d="%s Z" fill="%s"/><clipPath id="%s"><path d="%s Z"/></clipPath>' % (d_open, _hc(hide, k, "base"), cid, d_open),
         '<g clip-path="url(#%s)"><path d="%s" fill="%s"/>' % (cid, shade, _hc(hide, k, "dark")),
         '<path d="%s" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round" opacity="0.75" transform="translate(%.4f %.4f)"/>'
         % (P._smooth_open([lit[i] for i in range(3, 11)]), _hc(hide, k, "light"), 0.0, 0.0)]
    rings = []
    nr = 7 if baby else 11
    for i in range(nr):
        u = 0.10 + 0.84 * i / (nr - 1)
        j = max(1, min(N - 1, int(u * N)))
        a, b = L[j], R[j]
        dxn, dyn = P_[j + 1][0] - P_[j - 1][0], P_[j + 1][1] - P_[j - 1][1]
        m = math.hypot(dxn, dyn) or 1
        rings.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a[0], a[1], (a[0] + b[0]) / 2 + dxn / m * 0.04, (a[1] + b[1]) / 2 + dyn / m * 0.04, b[0], b[1]))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/></g>' % ("".join(rings), k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round" stroke-linecap="round"/>' % (d_ink, k.ink))
    if trumpet:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%.2f %.4f %.4f)" fill="%s" stroke="%s" stroke-width="0.022"/>'
                 % (tipc[0] + ex * W[-1] * 0.5, tipc[1] + ey * W[-1] * 0.5, W[-1] * 0.9, W[-1] * 2.0, math.degrees(math.atan2(ey, ex)), tipc[0], tipc[1], k.c("#6a3040"), k.ink))
    else:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%.2f %.4f %.4f)" fill="%s"/>'
                 % (tipc[0] + ex * W[-1] * 0.7, tipc[1] + ey * W[-1] * 0.7, W[-1] * 0.30, W[-1] * 0.60, math.degrees(math.atan2(ey, ex)), tipc[0], tipc[1], k.ink))
    return "".join(o), (tipc[0] + ex * W[-1] * 1.2, tipc[1] + ey * W[-1] * 1.2), P_


def _front(k, cast, e):
    """the elephant seen head-on: two pillar legs, the big barrel behind, a huge head, two fan ears (relaxed or flared), the trunk
    hanging (or raised) and two tusks.  head_turn -1..1 slides the face features and the trunk to fake a turn."""
    sp = SPEC14[cast]
    s, hide = sp["s"], sp["hide"]
    K = s * S_D
    baby = sp["baby"]
    ink = k.ink
    pts_all = []
    fl = e["flare"]
    tn = e["turn"]
    ph = e["phase"]
    st = e["stride"]
    A = 0.22 * st
    bob = 0.03 * abs(math.sin(2 * math.pi * ph)) * min(1.0, st)

    def T(x, y):
        return (x * K, -(y + bob) * K)

    def X(*ps):
        pts_all.extend(ps)
    o = []
    hs = 1.0 + 0.30 * baby
    # far-to-near: back legs are hidden; draw the barrel, then legs in front, then the head
    barrel = [(-1.25, 3.05), (-0.6, 3.30), (0.6, 3.30), (1.25, 3.05), (1.40, 2.4), (1.30, 1.75), (0.9, 1.45), (-0.9, 1.45), (-1.30, 1.75), (-1.40, 2.4)]
    o.append(_shaded(k, TT_(barrel, T), hide, K, 0.030))
    X(*TT_(barrel, T))
    # legs
    for i, sx in enumerate((-1, 1)):
        liftv = max(0.0, math.sin(2 * math.pi * (ph + 0.5 * i))) * 0.30 * min(1.0, st)
        top = T(sx * 0.62, 2.0)
        bot = T(sx * (0.64 + 0.05 * A * sx), 0.18 + liftv)
        wd = 0.70 * K
        d = "M%.4f,%.4f L%.4f,%.4f" % (top + bot)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % ("M%.4f,%.4f L%.4f,%.4f" % (top[0], top[1] + 0.5 * K, bot[0], bot[1]), ink, wd + 0.060))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (d, _hc(hide, k, "base"), wd))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" opacity="0.9" transform="translate(%.4f 0)"/>'
                 % (top[0], top[1], bot[0], bot[1], _hc(hide, k, "dark"), wd * 0.28, wd * 0.36 * sx))
        fw, fh = 0.46 * K, 0.20 * K
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.026"/>' % (bot[0], bot[1] + 0.02, fw, fh, _hc(hide, k, "base"), ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" opacity="%.2f"/>'
                 % (bot[0] - fw * 0.9, bot[1] - fh * 0.1, bot[0], bot[1] - fh * 1.3, bot[0] + fw * 0.9, bot[1] - fh * 0.1, bot[0] + fw * 0.7, bot[1] + fh * 0.7, bot[0] - fw * 0.7, bot[1] + fh * 0.7, k.c(DUST), 0.5 * e["dust"]))
        for j in range(4):
            nxp = bot[0] + (j - 1.5) * fw * 0.42
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.012"/>' % (nxp, bot[1] + fh * 0.55, 0.075 * K, 0.06 * K, k.c("#efe6da"), ink))
        X((bot[0] - fw, bot[1] + fh), (bot[0] + fw, bot[1] + fh), (top[0] - wd / 2, top[1]), (top[0] + wd / 2, top[1]))
    # ears behind the head: big fans, relaxed (hanging) .. flared (spread wide)
    es = sp["ear"] * (1.0 + 0.22 * baby)
    for sx in (-1, 1):
        sp_ = 0.62 + 0.80 * fl                      # how far out the ear tip reaches (x)
        pts = [(sx * 0.85, 3.30), (sx * (0.9 + 0.9 * sp_ * es), 3.95 + 0.25 * fl), (sx * (1.0 + 1.9 * sp_ * es), 3.60 + 0.35 * fl), (sx * (1.15 + 2.1 * sp_ * es), 2.90 + 0.35 * fl),
               (sx * (1.0 + 1.7 * sp_ * es), 2.20 + 0.40 * fl), (sx * (0.9 + 0.9 * sp_ * es), 1.75 + 0.30 * fl), (sx * 0.95, 2.30), (sx * 0.95, 2.9)]
        if sp["notch"] and sx > 0:
            pts = pts[:3] + [(sx * (1.5 + 1.2 * sp_ * es), 3.35 + 0.35 * fl)] + pts[3:]
        ep = [T(x, y) for x, y in pts]
        o.append(_shaded(k, ep, hide, K, 0.030))
        cen = (sum(p[0] for p in ep) / len(ep), sum(p[1] for p in ep) / len(ep))
        inner = [(cen[0] + (p[0] - cen[0]) * 0.80, cen[1] + (p[1] - cen[1]) * 0.80) for p in ep]
        o.append('<path d="%s" fill="%s" opacity="%.2f"/>' % (P._smooth_closed(inner), k.c(HIDE["ear"]), 0.30 + 0.55 * fl))
        vein = ""
        for q in (ep[2], ep[3], ep[4]):
            vein += "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (ep[0][0], ep[0][1] + 0.1, (ep[0][0] + q[0]) / 2, (ep[0][1] + q[1]) / 2 + 0.1, q[0] * 0.9 + cen[0] * 0.1, q[1] * 0.9 + cen[1] * 0.1)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.5"/>' % (vein, k.c(HIDE["ear_d"])))
        X(*ep)
    # head: broad dome
    dx_ = 0.28 * tn
    hd = [(dx_ - 0.80, 3.10), (dx_ - 0.82, 3.55), (dx_ - 0.45, 3.95), (dx_ + 0.0, 4.02), (dx_ + 0.45, 3.95), (dx_ + 0.82, 3.55), (dx_ + 0.80, 3.10), (dx_ + 0.66, 2.50), (dx_ + 0.40, 2.00), (dx_ + 0.0, 1.85), (dx_ - 0.40, 2.00), (dx_ - 0.66, 2.50)]
    hp = [T(x * hs + (1 - hs) * 0, y) for x, y in hd]
    o.append(_shaded(k, hp, hide, K, 0.030))
    X(*hp)
    # forehead creases
    cr = ""
    for (yy, w_) in ((3.62, 0.5), (3.38, 0.42)):
        a, b = T(dx_ - w_, yy), T(dx_ + w_, yy)
        cr += "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a + (dx_ * K, a[1] - 0.04) + b)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.45"/>' % (cr, ink))
    # eyes + cheeks
    er = 0.15 * K * (1.0 + 0.25 * baby)
    ec = {}
    for sx in (-1, 1):
        ex_, ey_ = T(dx_ + sx * 0.50 * (1.0 + 0.1 * tn * sx), 3.00)
        ec[sx] = (ex_, ey_)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.5"/>' % (ex_ + sx * 0.05, ey_ + 0.30 * K, 0.20 * K, 0.12 * K, k.c("#e89aa0")))
        o.append(_eye(k, ex_, ey_, max(er, 0.06), e["expr"], e["blink"], sp["lash"], K, ink, baby, HIDES[hide]["base"]))
    # tusks (down and out, curving forward): drawn before the trunk
    tl = sp["tusk"]
    tips = []
    if tl > 0.01:
        for sx in (-1, 1):
            pts = []
            for i in range(9):
                u = i / 8
                x = dx_ + sx * (0.58 + 0.45 * u * tl * 0.8 + 0.1 * u)
                y = 2.00 - 0.55 * tl * u - 0.12 * u * u * tl
                pts.append(T(x, y))
            L, R, W = _tube(pts, 0.095 * K * (0.5 + 0.5 * min(1, tl)), 0.014, 0.9)
            d = P._smooth_open(L) + " L%.4f,%.4f " % pts[-1] + P._smooth_open(list(reversed(R)))[1:] + " Z"
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, k.c(IVORY["base"]), ink))
            o.append('<path d="%s" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % P._smooth_open([(p[0] - sx * 0.02, p[1]) for p in pts[1:6]]))
            tips.append(pts[-1])
            X(pts[-1])
    # trunk
    N = 18
    root = (dx_, 2.62)
    Lt = 2.2 * e["tl"] * (1.0 - 0.38 * baby)
    cl = [root]
    x, y = root
    ds = Lt / N
    trun = e["trunk"] == "raised"
    if trun:
        a0, a1, curl = 90, 90 + 12 * (1 if tn >= 0 else -1), 0.10
    elif e["trunk"] in ("hang", "swing", "tuck", "sniff", "curl"):
        a0, a1, curl = -90, -90 + 40 * e["curl"] * 0 + {"hang": 18, "swing": -22, "tuck": 30, "sniff": 10, "curl": 60}[e["trunk"]], {"curl": 0.6}.get(e["trunk"], 0.25)
    else:
        a0, a1, curl = -90 + 60, -90 + 40, 0.2
    a0 += 18 * tn
    sw = 9.0 * math.sin(e["t"] * 2 * math.pi) * (0.4 if trun else 1.0)
    for i in range(N):
        u = (i + 0.5) / N
        a = a0 + (a1 - a0) * u + curl * 60.0 * u ** 3 * (1 if tn >= 0 else -1) + sw * math.sin(u * math.pi)
        x += ds * math.cos(math.radians(a))
        y += ds * math.sin(math.radians(a))
        cl.append((x, y))
    # keep the trunk tip off the ground
    cl = [(px, max(py, 0.22)) for px, py in cl]
    Pc = [T(px, py) for px, py in cl]
    tsv, ttip, _ = _trunk_draw(k, Pc, 0.46 * K * hs, 0.20 * K * hs * (1.0 + 0.4 * baby), hide, e["t"], trun, baby, K)
    o.append(tsv)
    X(ttip, *Pc[::3])
    # mouth under the trunk base when open
    if e["mouth"] > 0.05:
        mc = T(dx_, 2.0)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.020"/>' % (mc[0], mc[1] + 0.05, 0.22 * K, (0.05 + 0.12 * e["mouth"]) * K, k.c("#c85a6a"), ink))
    # baby tuft
    if baby:
        c = T(dx_, 4.02)
        o.append('<path d="M%.4f,%.4f q-0.06,-0.14 -0.02,-0.20 q0.04,0.08 0.06,0.02 q0.02,-0.12 0.08,-0.16 q-0.02,0.12 0.0,0.16 q0.06,-0.08 0.10,-0.06 q-0.04,0.10 -0.08,0.24 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                 % (c[0] - 0.08, c[1] + 0.04, k.c("#5a4a52"), ink))
    hc = T(0.0, 3.0)
    ox, oy = -hc[0], -hc[1]
    xs = [p[0] + ox for p in pts_all]
    ys = [p[1] + oy for p in pts_all]
    feet_y = -hc[1]
    an = {}

    def A_(p):
        return (p[0] + ox, p[1] + oy)
    an["head"] = (0.0, 0.0)
    an["eye_r"], an["eye_l"] = A_(ec[1]), A_(ec[-1])
    an["mouth"] = A_(T(dx_, 2.0))
    an["head_top"] = A_(T(dx_, 4.02))
    an["hat_top"] = an["head_top"]
    an["trunk_tip"] = A_(ttip)
    an["trunk_base"] = A_(root and T(*root))
    an["tusk_tip"] = A_(tips[1]) if tips else an["trunk_base"]
    an["chest"] = A_(T(0.0, 2.0))
    an["chest_push"] = A_(T(0.0, 2.3))
    an["hip"] = A_(T(0.0, 1.5))
    an["belly"] = an["hip"]
    an["shoulder_top"] = A_(T(0.0, 3.3))
    an["rump"] = A_(T(0.0, 3.0))
    an["tail_tip"] = A_(T(0.0, 1.6))
    an["ear_tip"] = A_(T(1.9, 3.4))
    an["foot_r"], an["foot_l"] = A_(T(0.64, 0.18)), A_(T(-0.64, 0.18))
    an["knee_r"], an["knee_l"] = A_(T(0.64, 1.0)), A_(T(-0.64, 1.0))
    an["feet"] = (0.0, feet_y)
    an["shoulder_r"], an["shoulder_l"] = A_(T(0.9, 2.8)), A_(T(-0.9, 2.8))
    an["elbow_r"], an["elbow_l"] = an["knee_r"], an["knee_l"]
    an["hand_r"], an["hand_l"] = an["trunk_tip"], an["trunk_base"]
    an["prop_tip_r"], an["prop_tip_l"] = an["trunk_tip"], an["trunk_base"]
    return "".join(o), (ox, oy), an, (min(xs) - 0.08, min(ys) - 0.08, max(xs) + 0.08, max(ys) + 0.08), feet_y


def TT_(pts, T):
    return [T(x, y) for x, y in pts]


def elephant_figure(cast, pose=None, uid="e"):
    """puppet.figure() for an elephant: {"svg", "feet_y", "bbox", "anchors"} in the same conventions (D units, head centre at (0, 0),
    y down, feet_y = distance from the head centre to the soles)."""
    e = _ep(pose if isinstance(pose, dict) else {})
    k = P._Ctx(str(uid), e["ink"], P._rgb(e["tint"].lstrip("#")) if P._is_hex(e["tint"]) else None)
    fn = _side if e["view"] == "side" else _front
    _CIDS[k.uid] = 0
    body, (ox, oy), an, bb, feet_y = fn(k, cast, e)
    inner = '<g transform="translate(%.4f %.4f)">%s</g>' % (ox, oy, body)
    fx = an["feet"][0]
    sx, sy = e["squash"]
    if abs(sx - 1) > 1e-6 or abs(sy - 1) > 1e-6:
        inner = '<g transform="translate(%.4f %.4f) scale(%.4f %.4f) translate(%.4f %.4f)">%s</g>' % (fx, feet_y, sx, sy, -fx, -feet_y, inner)

        def sq(p):
            return (fx + (p[0] - fx) * sx, feet_y + (p[1] - feet_y) * sy)
        an = {n: sq(p) for n, p in an.items()}
        bb = (fx + (bb[0] - fx) * sx, feet_y + (bb[1] - feet_y) * sy, fx + (bb[2] - fx) * sx, feet_y + (bb[3] - feet_y) * sy)
    if e["mirror"]:
        inner = '<g transform="scale(-1 1)">%s</g>' % inner
        an = {n: (-p[0], p[1]) for n, p in an.items()}
        for a_, b_ in (("hand_r", "hand_l"), ("foot_r", "foot_l"), ("eye_r", "eye_l"), ("knee_r", "knee_l"), ("shoulder_r", "shoulder_l"), ("elbow_r", "elbow_l"), ("prop_tip_r", "prop_tip_l")):
            an[a_], an[b_] = an[b_], an[a_]
        bb = (-bb[2], bb[1], -bb[0], bb[3])
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(svg='<g id="%s_fig">%s%s</g>' % (k.uid, defs, inner), feet_y=feet_y if not (abs(sy - 1) > 1e-6) else feet_y, bbox=bb, anchors=an)


# ============================================================================= bees and the swarm
BEE_SIZE = 0.20         # body length in D (a real bee is 0.026 D: drawn big on purpose so that it reads at phone size)


def _bee_svg(k, x, y, size, ang, t, rest=0.0, blur=1.0, mirror=False, sting=0.6, seedv=0.0):
    """one gold-and-black bee card, facing +x, body length `size` (D), centred on (x, y): striped abdomen with a stinger,
    a furry thorax, a round head with an eye and two antennae, and two wings whose beat follows t (blurred ghost wings while flying,
    folded flat on the back at rest = 1).  Line weights stay at the series' ink weight, not scaled."""
    sc = size
    ink = k.ink
    lw = max(0.006, 0.012 / max(sc, 0.05) * 0.5)     # stroke width in bee units (about 0.006 D on screen)
    lw = 0.05
    o = ['<g transform="translate(%.4f %.4f) rotate(%.2f) scale(%.4f %.4f)">' % (x, y, ang, sc * (-1 if mirror else 1), sc)]
    beat = math.sin(2 * math.pi * t)
    wa = -62 + 30 * beat * (1 - rest) + 52 * rest          # wing angle: up and back, flapping
    wings = []
    for (a_, op, col) in ((wa, 0.88, "#eaf4ff"),):
        wings.append((a_, op))
    if rest < 0.5 and blur > 0.05:
        for da, op in ((-34, 0.22), (34, 0.22), (-17, 0.28), (17, 0.28)):
            wings.append((wa + da * blur, op * blur))
    for (a_, op) in sorted(wings, key=lambda w: w[1]):
        for dx_, sx in ((0.14, 1.0), (0.04, 0.82)):
            o.append('<g transform="translate(%.3f -0.14) rotate(%.2f)"><ellipse cx="0.30" cy="0" rx="%.3f" ry="%.3f" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.3f" stroke-opacity="%.2f"/></g>'
                     % (dx_, a_ + (-10 if sx < 1 else 0) , 0.34 * sx, 0.13 * sx, k.c("#d8ecff"), op * (1.0 if sx >= 1 else 0.8), k.c("#5a6a9a"), lw * 0.6, min(1.0, op + 0.2)))
    # abdomen + stripes
    cid = _cid(k, "bb")
    o.append('<clipPath id="%s"><ellipse cx="-0.20" cy="0.01" rx="0.40" ry="0.23"/></clipPath>' % cid)
    o.append('<ellipse cx="-0.20" cy="0.01" rx="0.40" ry="0.23" fill="%s"/>' % k.c(BEE_GOLD))
    o.append('<g clip-path="url(#%s)"><rect x="-0.44" y="-0.3" width="0.10" height="0.6" fill="%s"/><rect x="-0.22" y="-0.3" width="0.10" height="0.6" fill="%s"/><rect x="-0.60" y="-0.3" width="0.12" height="0.6" fill="%s"/>'
             '<path d="M-0.55,0.12 Q-0.2,0.30 0.18,0.12 L0.18,0.3 L-0.6,0.3 Z" fill="%s" opacity="0.28"/></g>' % (cid, k.c(BEE_DARK), k.c(BEE_DARK), k.c(BEE_DARK), k.c("#a8660a")))
    o.append('<ellipse cx="-0.20" cy="0.01" rx="0.40" ry="0.23" fill="none" stroke="%s" stroke-width="%.3f"/>' % (ink, lw))
    # stinger
    o.append('<path d="M-0.58,0.02 L-0.72,0.04 L-0.58,0.08 Z" fill="%s" stroke="%s" stroke-width="%.3f" stroke-linejoin="round"/>' % (k.c("#3a2a20"), ink, lw * 0.6))
    # thorax (fuzzy) + head
    o.append('<circle cx="0.20" cy="0" r="0.20" fill="%s" stroke="%s" stroke-width="%.3f"/>' % (k.c("#d9962a"), ink, lw))
    o.append('<path d="M0.10,-0.12 q0.06,-0.04 0.12,-0.02 M0.12,0.00 q0.07,-0.04 0.14,-0.02" fill="none" stroke="%s" stroke-width="%.3f" opacity="0.7" stroke-linecap="round"/>' % (k.c("#8a5a10"), lw * 0.7))
    o.append('<circle cx="0.46" cy="-0.01" r="0.15" fill="%s" stroke="%s" stroke-width="%.3f"/>' % (k.c(BEE_DARK), ink, lw))
    o.append('<circle cx="0.51" cy="-0.04" r="0.06" fill="#fffdf2"/><circle cx="0.53" cy="-0.04" r="0.030" fill="%s"/><circle cx="0.54" cy="-0.055" r="0.012" fill="#ffffff"/>' % k.c("#1a1210"))
    if rest > 0.5:
        o.append('<path d="M0.45,-0.03 q0.06,0.05 0.13,0" fill="none" stroke="#fffdf2" stroke-width="%.3f" stroke-linecap="round"/>' % (lw * 0.8))
    o.append('<path d="M0.56,-0.12 Q0.64,-0.26 0.76,-0.24 M0.50,-0.14 Q0.52,-0.28 0.62,-0.34" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round"/>' % (ink, lw * 0.8))
    # little legs
    o.append('<path d="M0.12,0.16 l-0.04,0.12 M0.22,0.17 l0.0,0.13 M0.30,0.14 l0.06,0.10" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round"/>' % (ink, lw * 0.8))
    o.append('</g>')
    return "".join(o)


def _bee_fig(pose, uid):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    size = _f(g("size"), BEE_SIZE, 0.04, 3.0)
    t = _num(g("t"), 0.0) if math.isfinite(_num(g("t"), 0.0)) else 0.0
    ang = _f(g("angle"), 0.0, -360, 360)
    rest = _f(g("rest"), 0.0, 0.0, 1.0)
    k = _ctx(uid, g("ink") if isinstance(g("ink"), str) else P.INK, g("tint"))
    _CIDS[k.uid] = 0
    mir = bool(g("mirror"))
    s = _bee_svg(k, 0.0, 0.0, size, ang, t, rest, _f(g("blur"), 1.0, 0.0, 1.0), mir)
    r = size * 0.85
    bb = (-r, -r, r, r)
    an = {n: (0.0, 0.0) for n in ("head", "eye_r", "eye_l", "mouth", "head_top", "hat_top", "chest", "hip", "hand_r", "hand_l", "prop_tip_r", "prop_tip_l", "shoulder_r", "shoulder_l",
                                  "elbow_r", "elbow_l", "knee_r", "knee_l", "foot_r", "foot_l", "feet")}
    an["feet"] = (0.0, 0.0)
    an["stinger"] = _rot(-0.72 * size * (-1 if mir else 1), 0.04 * size, ang)
    return dict(svg='<g id="%s_fig"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), feet_y=0.0, bbox=bb, anchors=an)


SWARM_SHAPES = ("cloud", "column", "stream", "ring")


def swarm_svg(uid="sw", n=40, radius=1.0, shape="cloud", seed=1.0, t=0.0, size=0.14, ang=0.0, length=3.0, ink=P.INK, tint=None, trails=True):
    """a swarm of n bees: shape "cloud" (a round buzzing ball of the given radius), "column" (a rising cone, base at (0, 0), height
    `length`), "stream" (a streak of bees from (0, 0) along ang over `length`, spread = radius), "ring" (bees orbiting a ring).  Each
    bee has its own wing phase, tilt and size (+-25 %); thin curved flight trails when trails=True.  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    _CIDS[k.uid] = 0
    n = int(_clamp(_num(n, 40), 1, 400))
    o = []
    pts = []
    for i in range(n):
        a, b, c, d = _hash(seed, i), _hash(seed, i + 100), _hash(seed, i + 200), _hash(seed, i + 300)
        if shape == "column":
            u = a
            ht = u * length
            wid = radius * (0.25 + 0.9 * u)
            x, y = (b * 2 - 1) * wid * (0.5 + 0.5 * c), -ht
            tilt = -90 + (b * 2 - 1) * 50
        elif shape == "stream":
            u = a
            ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            ln = u * length
            off = (b * 2 - 1) * radius * (0.2 + 0.8 * u)
            x, y = ln * ca - off * sa, ln * sa + off * ca
            tilt = ang + (c * 2 - 1) * 40
        elif shape == "ring":
            th = 2 * math.pi * (a + 0.12 * t)
            rr = radius * (0.85 + 0.3 * b)
            x, y = rr * math.cos(th), rr * math.sin(th) * 0.55
            tilt = math.degrees(th) + 90
        else:
            th = 2 * math.pi * a
            rr = radius * math.sqrt(b) * (0.6 + 0.4 * c)
            x, y = rr * math.cos(th), rr * math.sin(th) * 0.85
            tilt = (c * 2 - 1) * 180
        sz = size * (0.75 + 0.5 * d)
        pts.append((x, y, sz, tilt, (a * 7.7 + t * (1.0 + 0.4 * d)) % 1.0, (tilt > 90 or tilt < -90) and shape != "stream"))
    if trails:
        tr = []
        for (x, y, sz, tilt, ph, fl) in pts[::3]:
            ca, sa = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
            tr.append("M%.3f,%.3f q%.3f,%.3f %.3f,%.3f" % (x - ca * sz * 1.8, y - sa * sz * 1.8, -sa * sz * 0.5, ca * sz * 0.5, -ca * sz * 1.6, -sa * sz * 1.6))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.35"/>' % ("".join(tr), k.ink))
    for (x, y, sz, tilt, ph, fl) in sorted(pts, key=lambda p: p[1]):
        o.append(_bee_svg(k, x, y, sz, tilt if abs(tilt) <= 90 else tilt - 180, ph, 0.0, 0.8, mirror=abs(tilt) > 90))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    m = size * 1.3
    bb = (min(xs) - m, min(ys) - m, max(xs) + m, max(ys) + m)
    return '<g id="%s_swarm"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), "".join(o)), bb


def _swarm_fig(pose, uid):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    shape = g("shape") if g("shape") in SWARM_SHAPES else "cloud"
    s, bb = swarm_svg(uid, _num(g("n"), 40), _f(g("radius"), 1.0, 0.1, 8.0), shape, _num(g("seed"), 1.0), _num(g("t"), 0.0), _f(g("size"), 0.14, 0.03, 1.5),
                      _f(g("angle"), 0.0, -360, 360), _f(g("length"), 3.0, 0.2, 14.0), g("ink") if isinstance(g("ink"), str) else P.INK, g("tint"))
    if g("mirror"):
        s = '<g transform="scale(-1 1)">%s</g>' % s
        bb = (-bb[2], bb[1], -bb[0], bb[3])
    an = {n_: (0.0, 0.0) for n_ in ("head", "eye_r", "eye_l", "mouth", "head_top", "hat_top", "chest", "hip", "hand_r", "hand_l", "prop_tip_r", "prop_tip_l", "shoulder_r", "shoulder_l",
                                    "elbow_r", "elbow_l", "knee_r", "knee_l", "foot_r", "foot_l", "feet")}
    return dict(svg=s, feet_y=0.0, bbox=bb, anchors=an)


# ============================================================================= the stool under the uncle's feet
def _stool_svg(k, cx, y, w=1.30, h=0.78):
    """a three-legged wooden milking stool: round seat (top at y, the soles stand on it) and splayed legs down to y + h."""
    o = []
    for dx_, dy_, sw_ in ((-0.46, 0.0, 1), (0.46, 0.0, 1), (0.0, 0.05, 0.9)):
        x0 = cx + dx_ * w / 1.3 * 0.8
        x1 = cx + dx_ * w / 1.3 * 1.1
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.110" stroke-linecap="round"/>' % (x0, y + 0.10, x1, y + h, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % (x0, y + 0.10, x1, y + h, k.c(WOOD["base"] if dy_ < 0.04 else WOOD["dark"])))
    g = _lin(k, "c14stl", WOOD["light"], WOOD["base"], WOOD["dark"], cx - w / 2, 0, cx + w / 2, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (cx - w / 2 + 0.06, y - 0.05, cx + w / 2 - 0.06, y - 0.05, cx + w / 2, y + 0.10, cx - w / 2, y + 0.10, g, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (cx - w / 2 + 0.14, y + 0.045, cx + w / 2 - 0.14, y + 0.045, k.c(WOOD["deep"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (cx - w / 2 + 0.12, y - 0.03, cx + w / 2 - 0.2, y - 0.03, k.c(WOOD["light"])))
    return "".join(o), (cx - w / 2 - 0.1, y - 0.06, cx + w / 2 + 0.1, y + h + 0.06)


def stool_svg(uid="st", w=1.30, h=0.78, ink=P.INK, tint=None):
    """the stool alone: seat top at y 0 centred on x 0, legs down to y = h.  Returns (svg, bbox)."""
    k = _ctx(uid, ink, tint)
    s, bb = _stool_svg(k, 0.0, 0.0, w, h)
    return '<g id="%s_stool"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), s), bb


# ============================================================================= wrappers: figure, cycle, resolve/lerp for the creatures
def figure(cast_name, pose=None, uid="p"):
    if isinstance(cast_name, str):
        if cast_name in ELEPHANTS:
            return elephant_figure(cast_name, pose, uid)
        if cast_name == "bee":
            return _bee_fig(pose, uid)
        if cast_name == "swarm":
            return _swarm_fig(pose, uid)
    f = _O14["figure"](cast_name, pose, uid)
    if not isinstance(pose, dict) or cast_name not in PEOPLE14 or _f(pose.get("stool"), 0.0, 0.0, 1.0) < 0.5:
        return f
    k = P._Ctx(uid + "x", P.INK, None)
    an = dict(f["anchors"])
    s, bb = _stool_svg(k, an["feet"][0], f["feet_y"], _f(pose.get("stool_w"), 1.30, 0.6, 3.0), _f(pose.get("stool_h"), 0.78, 0.2, 3.0))
    b = list(f["bbox"])
    b = [min(b[0], bb[0]), min(b[1], bb[1]), max(b[2], bb[2]), max(b[3], bb[3])]
    an["stool_top"] = (an["feet"][0], f["feet_y"])
    an["stool_bottom"] = (an["feet"][0], f["feet_y"] + _f(pose.get("stool_h"), 0.78, 0.2, 3.0))
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    return dict(f, svg='<g id="%s_stoolfig">%s%s%s</g>' % (uid, defs, s, f["svg"]), bbox=tuple(b), anchors=an)


def resolve_pose(cast_name, pose=None):
    if isinstance(cast_name, str) and (cast_name in ELEPHANTS or cast_name in CREATURES):
        return dict(pose) if isinstance(pose, dict) else {}
    return _O14["resolve_pose"](cast_name, pose)


def lerp_pose(cast_name, a, b, t):
    if isinstance(cast_name, str) and (cast_name in ELEPHANTS or cast_name in CREATURES):
        t = _clamp(_num(t), 0.0, 1.0)
        A = dict(a) if isinstance(a, dict) else {}
        B = dict(b) if isinstance(b, dict) else {}
        out = dict(A if t < 0.5 else B)
        for key in set(A) | set(B):
            va, vb = A.get(key), B.get(key)
            if key in ("phase", "t"):
                continue
            if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and not isinstance(va, bool):
                out[key] = va + (vb - va) * t
            elif va is None and isinstance(vb, (int, float)) and not isinstance(vb, bool) and key in ("ear_flare", "mouth_open", "push", "stride", "head_dip", "lean", "head_turn", "nose_swell"):
                out[key] = vb * t
            elif vb is None and isinstance(va, (int, float)) and not isinstance(va, bool) and key in ("ear_flare", "mouth_open", "push", "stride", "head_dip", "lean", "head_turn", "nose_swell"):
                out[key] = va * (1 - t)
        for key in ("phase", "t"):
            if key in A or key in B:
                out[key] = _num(A.get(key, B.get(key)), 0.0) + (_num(B.get(key, A.get(key)), 0.0) - _num(A.get(key, B.get(key)), 0.0)) * t
        return out
    return _O14["lerp_pose"](cast_name, a, b, t)


def cycle(cast, phase, mode="walk", facing=1, base=None, arms="both", speed=1.0):
    """C6.cycle for the people (walk / run / sneak / march, arms, facing -1 mirrors).  For the elephants: one frame of the
    four-beat walk (mode "walk", about 48 frames per cycle at 30 fps), the lumbering trot "run" (about 28 frames), "sneak" /
    "march" = a short slow step (stride 0.7); the pose is view "side", mirror=True for facing -1, `speed` scales the stride; base is kept
    (expr, trunk, ear_flare ...).  See cycle_distance() for the ground speed (no foot slip)."""
    if isinstance(cast, str) and cast in ELEPHANTS:
        p = dict(base or {})
        p["view"] = "side"
        p["phase"] = _num(phase, 0.0) % 1.0
        run = mode == "run"
        p["gait"] = "run" if run else "walk"
        p["stride"] = _clamp(_num(speed, 1.0), 0.2, 1.6) * (0.7 if mode in ("sneak", "march") else 1.0)
        p["mirror"] = _num(facing, 1.0) < 0
        if "t" not in p:
            p["t"] = _num(phase, 0.0)
        if run:
            p.setdefault("lean", 2.0)
        return p
    return cycle6(cast, phase, mode, facing, base, arms, speed)


def cycle_distance(cast, mode="walk", speed=1.0):
    """D the body travels per cycle for the elephants without foot slip (stance 62 % of the cycle): move the actor by this much per cycle.
    For the people use the cast6 rule (stride ~ 1.05 D per step at speed 1)."""
    if cast in ELEPHANTS:
        sp = SPEC14[cast]
        st = _clamp(_num(speed, 1.0), 0.2, 1.6) * (0.7 if mode in ("sneak", "march") else 1.0)
        if mode == "run":
            st *= 1.3
        A = 0.62 * st * (1.25 if mode == "run" else 1.0)
        return 2.0 * A / 0.62 * sp["s"] * S_D
    return None


# ============================================================================= canvases (feet-relative, D)
def _ecanvas(cast):
    s = SPEC14[cast]["s"]
    # side view: symmetric (the same canvas serves both facings, mirror=True): trunk reach in front, tail behind, raised trunk and ears above
    w = 10.7 * s + 0.8
    return (round(-w * 16) / 16.0, round(-(8.4 * s + 0.9) * 16) / 16.0, round(w * 16) / 16.0, 0.5)


CANVAS14.update({c: _ecanvas(c) for c in ELEPHANTS})
CANVAS14["bee"] = (-0.5, -0.5, 0.5, 0.5)
CANVAS14["swarm"] = (-3.0, -5.0, 3.0, 1.0)
CANVAS14_STOOL = {"uncle14": (-2.0625, -5.5, 2.0625, 0.9375)}
# the elephant canvases above are for poses that stay in the walk / push / flee envelope; the front view with spread ears and the raised
# trunk is wider: use CANVAS14_FRONT
CANVAS14_FRONT = {c: (round(-5.0 * SPEC14[c]["s"] * S_D * 16) / 16.0, round((-5.3 * SPEC14[c]["s"] * S_D - 0.1) * 16) / 16.0, round(5.0 * SPEC14[c]["s"] * S_D * 16) / 16.0, 0.5) for c in ELEPHANTS}


# ============================================================================= story poses
def _story():
    S, M = {}, {}
    F, U = "farmer14", "uncle14"
    HV = dict(type="tophive", scale=0.85)
    # --- the farmer
    S["farmer_hang_hive"] = (F, dict(yaw=0.45, pitch=-0.25, expr="happy", mouth="smile", head_roll=-4, lean=3, gaze=(0.8, -0.6),
                                     arm_r=dict(hand=(1.05, -0.40), bend=-0.7, stretch=1.3, layer="front"), prop_r=HV,
                                     arm_l=dict(hand=(0.28, 0.46), bend=0.5, shape="open"), legs=dict(preset="step", stride=0.25)))
    M["farmer_hang_hive"] = dict(note="hanging a hive on the wire: both arms reach up, the top-bar hive (prop tophive, anchor hive_top_r = roof, hive_c_r) at head height on the "
                                      "screen-right; set hive_stage by the set")
    S["farmer_tie_wire"] = (F, dict(yaw=0.55, pitch=0.15, expr="determined", mouth="flat", head_roll=-3, lean=5, gaze=(0.9, 0.3),
                                    arm_r=dict(hand=(0.78, 0.30), bend=-0.2, stretch=1.2, shape="open"), arm_l=dict(hand=(-0.40, 0.90), bend=0.4), prop_l="wirecoil",
                                    legs=dict(preset="step", stride=0.20)))
    M["farmer_tie_wire"] = dict(note="tying the wire: a coil of wire on the left forearm (anchor wire_end_l), the right hand twisting the wire out in front (screen-right)")
    S["farmer_calm_smile"] = (F, dict(yaw=0.30, pitch=-0.10, expr="happy", mouth="smile", head_roll=3, gaze=(0.4, 0.0),
                                      arm_r=dict(hand=(0.40, 1.00), bend=0.3), prop_r=dict(type="hammer", angle=100, scale=1.1), arm_l="hip", legs="stand"))
    M["farmer_calm_smile"] = dict(note="calm smile while the village laughs; a hammer hanging in one hand, the other on the hip")
    S["farmer_proud"] = (F, dict(yaw=0.25, pitch=-0.45, expr="smug", mouth="smile", head_roll=-5, lean=-4, gaze=(0.6, -0.3),
                                 arm_r="akimbo", arm_l="akimbo", legs="wide", squash=(1.0, 1.02)))
    M["farmer_proud"] = dict(note="standing proud by his fence: chest out, head up, arms akimbo")
    S["farmer_hammer_post"] = (F, dict(yaw=0.55, pitch=0.05, expr="determined", mouth="flat", head_roll=-3, t=0.2,
                                       arm_r=dict(hand=(0.78, -0.30), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="hammer", angle=-40, scale=1.2),
                                       arm_l=dict(hand=(0.30, 0.70), bend=0.5, shape="open"), legs=dict(preset="step", stride=0.2)))
    M["farmer_hammer_post"] = dict(note="hammering a hive hook / post (screen-right); animate arm_r hand (0.78, -0.30) -> (0.70, 0.05) and prop angle -40 -> 15")
    S["farmer_boast"] = (F, dict(yaw=0.35, pitch=-0.25, expr="smirk", mouth="smile", head_roll=-4, gaze=(0.8, -0.2),
                                 arm_r=dict(hand=(0.95, 0.05), shape="point", bend=-0.5, stretch=1.3), arm_l="hip", legs="wide"))
    M["farmer_boast"] = dict(note="the hook: he points at his hive and says the bees will chase off the herd (screen-right; no lip-sync)")
    S["farmer_watch_night"] = (F, dict(yaw=0.65, pitch=-0.05, expr="stunned", mouth="o", head_roll=3, gaze=(1.0, 0.0), fx=["sweat"], lean=-3,
                                       arm_r=dict(hand=(0.50, 0.55), bend=0.6), arm_l=dict(hand=(-0.35, 0.95), bend=0.4), legs=dict(preset="step", stride=-0.2)))
    M["farmer_watch_night"] = dict(note="watches the herd come to the fence at night, a little nervous (screen-right)")
    S["farmer_walk"] = (F, cycle(F, 0.30, "walk", base=dict(expr="happy", mouth="smile", prop_r=dict(type="hammer", angle=100, scale=1.1)), arms="l"))
    M["farmer_walk"] = dict(note="one frame (phase 0.30) of cycle(); animate cycle('farmer14', frame / 28, 'walk', facing, base, arms)")
    # --- the uncle
    S["uncle_laugh_big"] = (U, dict(yaw=0.20, pitch=-0.85, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.02, 0.98),
                                    arm_r=dict(hand=(0.46, 1.00), bend=0.9, shape="open"), arm_l=dict(hand=(-0.50, 0.98), bend=0.9, shape="open"), legs="wide"))
    M["uncle_laugh_big"] = dict(note="belly laugh at the bee guy: head back, hands on the belly, tears (held open mouth, no lip-sync)")
    S["uncle_point_mock"] = (U, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8,
                                     arm_r=dict(hand=(1.08, 0.12), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"))
    M["uncle_point_mock"] = dict(lipsync=True, note="QUOTE 15.4-22.0: pointing and mocking (screen-right, mirror=True for left); LIP-SYNC mouth=talk_mouth(g) during the quote, 'flat' otherwise")
    S["uncle_arms_akimbo"] = (U, dict(yaw=0.20, pitch=-0.30, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"))
    M["uncle_arms_akimbo"] = dict(note="smug, arms akimbo (the end of the mocking, and 'See?' beats)")
    S["uncle_shout_torch"] = (U, dict(yaw=0.40, pitch=-0.35, expr="shouting", mouth="talk_b", head_roll=6, t=0.2,
                                      arm_r=dict(hand=(0.80, -0.62), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="torch14", angle=-80, scale=1.0),
                                      arm_l=dict(hand=(-0.55, 0.95), bend=0.3), legs="wide"))
    M["uncle_shout_torch"] = dict(lipsync=True, note="QUOTE 39.0-40.8 at night: shouting 'See? The elephants aren't scared at all!' with a torch held high (animate t for the flame), LIP-SYNC")
    S["uncle_look_field"] = (U, dict(yaw=0.35, pitch=0.20, expr="stunned", mouth=("open", 0.15, 0.20), fx=["sweat"], gaze=(0.6, 0.4), head_roll=4,
                                     arm_r=dict(hand=(0.30, -0.40), bend=-0.9, stretch=1.1, layer="top"), arm_l=dict(hand=(-0.55, 1.00), bend=0.3), legs="stand"))
    M["uncle_look_field"] = dict(note="looks at his trampled field, hand on his cap, mouth open (held, not lip-sync)")
    S["uncle_ask_sheepish"] = (U, dict(yaw=0.45, pitch=0.15, expr="worried", mouth="smirk", fx=["blush", "sweat"], head_roll=6, gaze=(-0.6, 0.2),
                                       arm_r=dict(hand=(0.56, 0.52), bend=0.5, stretch=1.2), prop_r=dict(type="hivebox", scale=0.7),
                                       arm_l=dict(hand=(-0.40, -0.30), bend=-0.9, stretch=1.2, shape="open", layer="back"), legs="stand"))
    M["uncle_ask_sheepish"] = dict(note="the next morning, asking sheepishly for hives: an EMPTY hive box in one hand (prop hivebox), scratching the back of his head")
    S["uncle_stool_hang"] = (U, dict(yaw=0.45, pitch=-0.20, expr="determined", mouth="flat", head_roll=-3, gaze=(0.8, -0.5), stool=1,
                                     arm_r=dict(hand=(0.95, -0.60), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="tophive", scale=0.74),
                                     arm_l=dict(hand=(0.35, 0.45), bend=0.5, shape="open"), legs="stand"))
    M["uncle_stool_hang"] = dict(note="standing on a stool (stool=1 draws it; CANVAS14_STOOL), hanging his first hive; pair with uncle_stung_nose. The set may carry its own stool: set stool=0")
    S["uncle_stung_nose"] = (U, dict(yaw=0.20, pitch=0.10, expr="shocked", mouth="o", nose_swell=1.0, gaze=(0.0, 0.7), fx=["sweat"], head_roll=-5, t=0.3, stool=1,
                                     arm_r=dict(hand=(0.30, 0.34), bend=-0.6, stretch=1.0, shape="open", layer="top"), arm_l=dict(hand=(-0.70, 0.55), bend=0.6, shape="open"),
                                     legs="stand", squash=(1.0, 1.02)))
    M["uncle_stung_nose"] = dict(note="THE GAG: stung on the nose, a shiny swollen trunk-like nose (pose key nose_swell 0..1; animate 0 -> 1 over ~20 frames "
                                     "with an ease-out, `t` sways the tip), eyes cross to look at it, hand hovering. stool=1 (set to 0 if the set has the stool)")
    S["uncle_stung_start"] = (U, dict(S["uncle_stung_nose"][1], nose_swell=0.30, expr="shocked", mouth="talk_o", arm_r=dict(hand=(0.50, 0.10), bend=-0.5, stretch=1.1, shape="open", layer="top")))
    M["uncle_stung_start"] = dict(note="the instant of the sting (nose_swell 0.3); blend into uncle_stung_nose")
    S["uncle_stick_idle"] = (U, dict(yaw=0.30, pitch=-0.15, expr="smug", mouth="flat", head_roll=4, arm_r=dict(hand=(0.45, 0.62), bend=0.5, stretch=1.0),
                                     prop_r=dict(type="stick14", angle=82, scale=1.0), arm_l="akimbo", legs="stand"))
    M["uncle_stick_idle"] = dict(note="leaning on his walking stick (anchor stick_tip_r on the ground)")
    S["uncle_walk"] = (U, cycle(U, 0.30, "walk", base=dict(expr="smug", mouth="flat", prop_r=dict(type="stick14", angle=80, scale=1.0)), arms="l"))
    M["uncle_walk"] = dict(note="one frame (phase 0.30) of cycle('uncle14', ...) with the walking stick in the right hand")
    # --- the villagers (no lip-sync)
    W, K_, O, Y = "woman14", "kid14", "oldman14", "youth14"
    S["villager_woman_laugh"] = (W, dict(yaw=0.25, pitch=-0.5, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=-8, lean=-4, t=0.3,
                                         arm_r=dict(hand=(0.38, 0.92), bend=0.9, shape="open"), arm_l=dict(hand=(-0.40, 0.92), bend=0.9, shape="open"), legs="stand"))
    S["villager_woman_bang_pot"] = (W, dict(yaw=0.40, pitch=-0.1, expr="excited", mouth="talk_b", head_roll=3, t=0.2,
                                            arm_l=dict(hand=(-0.22, 0.60), bend=0.5), prop_l="pot14",
                                            arm_r=dict(hand=(0.55, 0.32), bend=-0.6, stretch=1.1), prop_r=dict(type="spoon14", angle=210, scale=1.0), legs="wide"))
    S["villager_woman_wave_torch"] = (W, dict(yaw=0.40, pitch=-0.3, expr="shouting", mouth="talk_a", head_roll=-4, t=0.2,
                                              arm_r=dict(hand=(0.60, -0.62), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="torch14", angle=-75, scale=0.95),
                                              arm_l="akimbo", legs="wide"))
    S["villager_kid_laugh_point"] = (K_, dict(yaw=0.35, pitch=-0.35, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                              arm_r=dict(hand=(0.74, 0.02), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.28, 0.80), bend=0.9), legs="wide"))
    S["villager_kid_bang_pot"] = (K_, dict(yaw=0.30, pitch=-0.1, expr="excited", mouth="talk_b", head_roll=4, t=0.2,
                                           arm_l=dict(hand=(-0.20, 0.55), bend=0.5), prop_l=dict(type="pot14", scale=0.8),
                                           arm_r=dict(hand=(0.46, 0.20), bend=-0.5, stretch=1.1), prop_r=dict(type="spoon14", angle=205, scale=0.8), legs="wide"))
    S["villager_oldman_laugh"] = (O, dict(yaw=0.20, pitch=0.2, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], head_roll=-9, lean=8, t=0.6,
                                          arm_r=dict(hand=(0.44, 0.40), bend=0.6, stretch=1.0, shape="open"), prop_r=dict(type="stick14", angle=78, scale=1.0),
                                          arm_l=dict(hand=(-0.30, 0.96), bend=0.9, shape="open"), legs=dict(preset="crouch", crouch=0.12, spread=0.08)))
    S["villager_oldman_wave_torch"] = (O, dict(yaw=0.35, pitch=-0.2, expr="shouting", mouth="talk_a", head_roll=4, t=0.2,
                                               arm_r=dict(hand=(0.62, -0.50), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="torch14", angle=-80, scale=0.95),
                                               arm_l=dict(hand=(-0.45, 0.95), bend=0.3), legs="stand"))
    S["villager_youth_wave_torch"] = (Y, dict(yaw=0.40, pitch=-0.35, expr="shouting", mouth="talk_b", head_roll=-5, lean=-3, t=0.2,
                                              arm_r=dict(hand=(0.70, -0.62), bend=-0.7, stretch=1.3, layer="front"), prop_r=dict(type="torch14", angle=-70, scale=1.0),
                                              arm_l=dict(hand=(-0.50, 0.55), bend=0.7, shape="open"), legs="wide"))
    S["villager_youth_point_laugh"] = (Y, dict(yaw=0.35, pitch=-0.35, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=-5, t=0.4,
                                               arm_r=dict(hand=(0.86, 0.04), shape="point", bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.30, 0.86), bend=0.9), legs="wide"))
    S["villager_youth_bang_pot"] = (Y, dict(yaw=0.35, pitch=-0.15, expr="excited", mouth="talk_b", head_roll=4, t=0.2,
                                            arm_l=dict(hand=(-0.24, 0.60), bend=0.5), prop_l="pot14",
                                            arm_r=dict(hand=(0.60, 0.30), bend=-0.6, stretch=1.1), prop_r=dict(type="spoon14", angle=212, scale=1.05), legs="wide"))
    for n_, note in (("villager_woman_laugh", "the woman with the headwrap laughs at the bee guy (hands on cheeks / belly, tears)"),
                     ("villager_woman_bang_pot", "bangs a pot with a wooden spoon (spoon_r hits pot_face_l); animate arm_r hand (0.55, 0.32) <-> (0.30, 0.55)"),
                     ("villager_woman_wave_torch", "waves a torch (pivot beat); animate t for the flame"),
                     ("villager_kid_laugh_point", "the kid points and laughs (screen-right)"),
                     ("villager_kid_bang_pot", "the kid bangs a small pot"),
                     ("villager_oldman_laugh", "the old man cackles, leaning on his stick"),
                     ("villager_oldman_wave_torch", "the old man waves a torch"),
                     ("villager_youth_wave_torch", "the youth waves a torch and yells at the elephants"),
                     ("villager_youth_point_laugh", "the youth points and laughs (calls him ไอ้บ้าผึ้ง)"),
                     ("villager_youth_bang_pot", "the youth bangs a pot")):
        M[n_] = dict(note=note + "; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are)")
    # --- elephants
    for c in ELEPHANTS:
        baby = c == "calf"
        S[c + "_walk"] = (c, cycle(c, 0.10, "walk", base=dict(expr="calm", trunk="sniff" if not baby else "swing")))
        S[c + "_stand"] = (c, dict(view="side", expr="happy" if baby else "calm", trunk="hang", ear_flare=0.0))
        S[c + "_flee"] = (c, cycle(c, 0.22, "run", base=dict(expr="alarmed", trunk="raised", ear_flare=0.8, mouth_open=0.4, tail=0.8, head_dip=-6)))
        S[c + "_trumpet"] = (c, dict(view="side", expr="trumpet", trunk="raised", ear_flare=1.0, mouth_open=1.0, head_dip=-12, lean=-3, t=0.25, tail=0.4))
        S[c + "_ears_flared"] = (c, dict(view="front", expr="alarmed", trunk="hang", ear_flare=1.0, t=0.1))
        S[c + "_turn"] = (c, dict(view="front", expr="alarmed", trunk="swing", ear_flare=0.7, head_turn=0.8, t=0.4))
        S[c + "_front_calm"] = (c, dict(view="front", expr="calm" if not baby else "happy", trunk="hang", ear_flare=0.0))
        M[c + "_walk"] = dict(note="one frame (phase 0.10) of cycle('%s', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance()" % c)
        M[c + "_stand"] = dict(note="standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left)")
        M[c + "_flee"] = dict(note="flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left")
        M[c + "_trumpet"] = dict(note="trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway")
        M[c + "_ears_flared"] = dict(note="FRONT view, ears fully flared, alarmed face (hold or blend with _turn)")
        M[c + "_turn"] = dict(note="FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1")
        M[c + "_front_calm"] = dict(note="FRONT view, calm: arriving at the fence, facing the camera")
    S["matriarch_push"] = ("matriarch", dict(view="side", expr="grumpy", trunk="reach", push=1.0, head_dip=8, lean=2.0, ear_flare=0.15, t=0.2))
    M["matriarch_push"] = dict(note="pushes the wire with her chest: weight forward, rear legs back, head down; anchor chest_push = the point that touches the wire; push 0..1")
    S["matriarch_sniff_fence"] = ("matriarch", dict(view="side", expr="curious", trunk="sniff", head_dip=6, ear_flare=0.0, stride=0.0, t=0.15))
    M["matriarch_sniff_fence"] = dict(note="stands at the fence and sniffs the wire: curious face, trunk reaching low")
    S["matriarch_walk_to_fence"] = ("matriarch", cycle("matriarch", 0.10, "walk", base=dict(expr="calm", trunk="forward", head_dip=3), speed=0.8))
    M["matriarch_walk_to_fence"] = dict(note="the matriarch walks straight to the fence: calm walk, head forward")
    S["matriarch_swatted"] = ("matriarch", dict(view="side", expr="alarmed", trunk="curl", mouth_open=0.5, ear_flare=0.9, head_dip=-8, lean=-3, t=0.35, tail=0.7))
    M["matriarch_swatted"] = dict(note="the bee burst: startled, trunk curled up and in, ears flared (comic, no injury)")
    # --- bees
    S["bee_fly"] = ("bee", dict(t=0.1, angle=-8))
    S["bee_rest"] = ("bee", dict(rest=1.0, angle=0))
    S["swarm_cloud"] = ("swarm", dict(n=48, radius=1.1, shape="cloud", seed=3.0, t=0.2))
    S["swarm_burst"] = ("swarm", dict(n=70, radius=0.8, shape="stream", seed=5.0, t=0.4, length=3.6, angle=-35))
    S["swarm_column"] = ("swarm", dict(n=60, radius=0.8, shape="column", seed=7.0, t=0.3, length=3.2))
    M["bee_fly"] = dict(note="one bee card (size 0.20 D by default: drawn big on purpose), wings beat with t (blurred ghost wings); pose keys size, angle, t, rest, blur, mirror")
    M["bee_rest"] = dict(note="a sleeping bee: wings folded, eye closed (the false-calm beat)")
    M["swarm_cloud"] = dict(note="swarm helper: pose keys n, radius, shape (cloud / column / stream / ring), seed, t, size, angle, length; also swarm_svg()")
    M["swarm_burst"] = dict(note="the burst of bees streaming out of a hive toward the elephant's eyes (stream along angle)")
    M["swarm_column"] = dict(note="a rising column of bees from a hive entrance (base at (0, 0), card origin at the feet)")
    return S, M


STORY14, STORY14_META = {}, {}
LIPSYNC14 = ("uncle_point_mock", "uncle_shout_torch")


# ============================================================================= registration
def register():
    if getattr(P, "_cast14_registered", False):
        CE.register_stage()
        if not STORY14:
            s, m = _story()
            STORY14.update(s)
            STORY14_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "figure", "resolve_pose", "lerp_pose"):
        _O14[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P.figure = figure
    P.resolve_pose = resolve_pose
    P.lerp_pose = lerp_pose
    CE.COSTUMES.update(COSTUMES14)
    CE.HATS.update(HATS14)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS14 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP14)
    for n, c in NEW_CAST14.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS14)
    P._cast14_registered = True
    s, m = _story()
    STORY14.update(s)
    STORY14_META.update(m)
    P.STORY.update(STORY14)
    CE.register_stage()


register()
