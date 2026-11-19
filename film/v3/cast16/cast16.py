#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast16.py -- the cast of film 16 ("ไอ้บ้าลวด": Samuel Morse's telegraph, USA 1825-1845) for the v2 puppet, as an extension
module on top of cast10 (which chains cast9 .. cast_ext and v2/puppet).

    import sys; sys.path.insert(0, ".../v3/cast16"); import cast16     # registers on import (idempotent); import it BEFORE sprites
    import puppet                                                       # the same module object, now with the new members
    cast, pose = cast16.STORY16["mocker_boast_chest"]
    f = puppet.figure(cast, pose, "f")
    p = dict(pose, mouth=cast16.talk_mouth(g, 1.0), blink=cast16.blink_at(g, 90))
    m = puppet.figure("mule", cast16.cycle("mule", g / 30.0, "walk"), "m")      # the mule has its own figure() path

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  tail16 (the mocker's open black tailcoat over a big plaid waistcoat; postmaster sash + mail bag + key ring
                       with CAST sash16), braces16 (shirt, braces, trousers: Cornell and the labourers)
    cast_ext.HATS      stovepipe16 (tall black stovepipe), slouch16 (soft slouch hat), mane16 (Morse's swept-back hair mass)
    cast_ext.CANVAS    one feet-relative sprite canvas per member
and wraps puppet helpers on top of cast10's wrappers (each falls through for everything it does not handle):
    _norm / _face / _prop / figure   pose keys, side-whiskers + collar points + florid nose, new props, variants + stool + the mule
Variants (pose keys that pick a sibling CAST entry): morse16 young=1; mocker hat_off=1, sash=1 (any combination).
New cast: morse16, mocker, congressman_a/_b/_c, messenger, cornell, worker16_a/_b (spec: worker_a/_b), clerk16 (spec: clerk), mule.
STORY16 / STORY16_META: story poses.  cycle() (people: cast6; mule: walk / pull / idle), talk_mouth(), blink_at(), NOD.
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
import cast4 as C4      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW16 = ("morse16", "mocker", "congressman_a", "congressman_b", "congressman_c", "messenger", "cornell", "worker16_a", "worker16_b",
         "clerk16", "mule")
ALIAS16 = {"worker_a": "worker16_a", "worker_b": "worker16_b", "clerk": "clerk16"}      # spec names that earlier casts already own


def key16(name):
    """the CAST key for a film-16 name (worker_a -> worker16_a, worker_b -> worker16_b, clerk -> clerk16; others unchanged)."""
    return ALIAS16.get(name, name)


TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_f = C6._f
_lin = C9._lin
_O16 = {}
_POSE16 = {"glint": 0.0, "t": 0.0, "bag": 1.0, "keys": 1.0}

cycle_people, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD
CYCLE_MODES = C6.CYCLE_MODES

# ============================================================================= colours (style board: walnut, cream, federal green, brick red, navy)
WALNUT = dict(light="#b98a5a", base="#7a4a2a", dark="#3e2414")
COPPER = dict(light="#f0b27a", base="#c8743a", dark="#7a3c1a")
GLASSG = dict(light="#b8e0a0", base="#3c8a4a", dark="#14401e")
IRON = dict(light="#8a8f98", base="#4e535c", dark="#262a30")
BRASS = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
LEATHER = dict(light="#b88458", base="#7a4a2a", dark="#40240e")
CANVAS_C = dict(light="#e8d6ae", base="#c8a46a", dark="#8a6a3a")
FED_GREEN = dict(light="#5aa070", base="#2f6a4a", dark="#17382a")
BRICK = dict(light="#c8604a", base="#9c3a2a", dark="#5a1a12")
NAVY = dict(light="#4a5e9a", base="#26335e", dark="#121a34")
CREAM = dict(light="#fffaf0", base="#f0e4c8", dark="#c8b890")
GOLD = C10.GOLD
FELT = dict(light="#c8a878", base="#9a7a52", dark="#5e4630")


def _ctx(uid, ink, tint):
    return P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)


def _g3(k, name, c, x0, y0, x1, y1):
    return _lin(k, name, c["light"], c["base"], c["dark"], x0, y0, x1, y1)


# ============================================================================= props (own local frames, like cast10)
def _letter_body(k):
    """a sealed letter 0.40 x 0.28: cream paper, folded flap lines, a red wax seal (no writing)."""
    g = _g3(k, "ltr", CREAM, -0.2, -0.14, 0.2, 0.14)
    o = ['<path d="M-0.20,-0.14 L0.20,-0.14 L0.20,0.14 L-0.20,0.14 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M-0.20,-0.14 L0,0.02 L0.20,-0.14 M-0.20,0.14 L-0.04,0.00 M0.20,0.14 L0.04,0.00" fill="none" stroke="%s" stroke-width="0.010" stroke-linejoin="round" opacity="0.8"/>' % k.c(CREAM["dark"]))
    o.append('<path d="M-0.20,-0.14 L0,0.02 L0.20,-0.14" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round" opacity="0.5"/>' % (k.c("#ffffff"), k.ink))
    o.append('<circle cx="0" cy="0.02" r="0.052" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="-0.014" cy="0.008" r="0.016" fill="%s" opacity="0.8"/>'
             % (k.c(BRICK["base"]), k.ink, k.c(BRICK["light"])))
    o.append('<path d="M0.04,0.06 q0.03,0.02 0.025,0.05" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % k.c(BRICK["base"]))
    return "".join(o)


def _coil_body(k):
    """a coil of copper wire seen face-on: concentric loops round a hole, a loose end curling away."""
    o = ['<ellipse cx="0" cy="0" rx="0.215" ry="0.215" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c(COPPER["base"]), k.ink)]
    for r, c in ((0.185, "light"), (0.150, "dark"), (0.118, "light"), (0.088, "dark")):
        o.append('<circle cx="0" cy="0" r="%.3f" fill="none" stroke="%s" stroke-width="0.020" opacity="0.9"/>' % (r, k.c(COPPER[c])))
    o.append('<circle cx="0" cy="0" r="0.062" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#2a2018"), k.ink))
    o.append('<path d="M-0.15,-0.14 A0.20,0.20 0 0 1 0.02,-0.20" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>')
    o.append('<path d="M0.17,0.10 Q0.34,0.10 0.30,0.24 Q0.27,0.34 0.38,0.36" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.17,0.10 Q0.34,0.10 0.30,0.24 Q0.27,0.34 0.38,0.36" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(COPPER["base"]))
    return "".join(o)


def _magnet_body(k, spark=0.0):
    """horseshoe magnet along +x, open end toward +x, curve at the hand: red body, silver pole ends; optional blue spark."""
    o = []
    path = "M0.46,-0.15 L0.20,-0.15 A0.15,0.15 0 0 0 0.20,0.15 L0.46,0.15"
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.130" stroke-linejoin="round"/>' % (path, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.100" stroke-linejoin="round"/>' % (path, k.c(BRICK["base"])))
    o.append('<path d="M0.42,-0.185 L0.20,-0.185 A0.185,0.185 0 0 0 0.04,-0.05" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>' % k.c(BRICK["light"]))
    for s in (-1, 1):
        o.append('<rect x="0.34" y="%.3f" width="0.14" height="0.100" rx="0.012" fill="%s" stroke="%s" stroke-width="0.016"/>' % (s * 0.15 - 0.05, k.c(IRON["light"]), k.ink))
        o.append('<path d="M0.36,%.3f L0.46,%.3f" stroke="#ffffff" stroke-width="0.010" opacity="0.6"/>' % (s * 0.15 - 0.03, s * 0.15 - 0.03))
    if spark > 0.02:
        o.append('<path d="M0.50,-0.15 L0.58,-0.05 L0.54,-0.03 L0.62,0.06 L0.56,0.08 L0.50,0.15" fill="none" stroke="#bfe6ff" stroke-width="0.030" stroke-linejoin="round" opacity="%.2f"/>' % spark)
        o.append('<path d="M0.50,-0.15 L0.58,-0.05 L0.54,-0.03 L0.62,0.06 L0.56,0.08 L0.50,0.15" fill="none" stroke="#3a86ff" stroke-width="0.014" stroke-linejoin="round"/>')
    return "".join(o)


def _bottle_body(k, glint=0.0):
    """a green beer bottle 0.80 long along +x: the hand holds the neck at 0; body -0.54..-0.14, shoulder, neck to the lip at +0.28."""
    gg = _g3(k, "btl", GLASSG, 0, -0.1, 0, 0.1)
    d = ("M-0.54,-0.085 Q-0.54,-0.10 -0.50,-0.10 L-0.20,-0.10 Q-0.10,-0.095 -0.06,-0.040 Q-0.02,-0.032 0.0,-0.030 L0.22,-0.030 L0.22,-0.048 "
         "L0.29,-0.048 L0.29,0.048 L0.22,0.048 L0.22,0.030 L0.0,0.030 Q-0.02,0.032 -0.06,0.040 Q-0.10,0.095 -0.20,0.10 L-0.50,0.10 Q-0.54,0.10 -0.54,0.085 Z")
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, gg, k.ink)]
    o.append('<rect x="-0.46" y="-0.10" width="0.24" height="0.20" fill="%s" opacity="0.85"/>' % k.c("#e8d6a8"))       # blank label
    o.append('<path d="M-0.46,-0.10 L-0.46,0.10 M-0.22,-0.10 L-0.22,0.10" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(CREAM["dark"]))
    o.append('<path d="M-0.50,-0.078 L-0.20,-0.078 M-0.03,-0.020 L0.20,-0.020" fill="none" stroke="#ffffff" stroke-width="0.014" stroke-linecap="round" opacity="0.65"/>')
    o.append('<rect x="0.22" y="-0.050" width="0.07" height="0.100" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010" opacity="0.9"/>' % (k.c(GLASSG["light"]), k.ink))
    if glint > 0.02:
        s = 0.10 + 0.14 * glint
        o.append('<g transform="translate(-0.12 -0.05) scale(%.3f)"><path d="M0,-1 L0.16,-0.16 L1,0 L0.16,0.16 L0,1 L-0.16,0.16 L-1,0 L-0.16,-0.16 Z" fill="#ffffff" stroke="#fff6c8" stroke-width="0.04"/></g>' % s)
        o.append('<circle cx="-0.12" cy="-0.05" r="%.3f" fill="#fff6c8" opacity="0.35"/>' % (0.10 + 0.10 * glint))
    return "".join(o)


def _bag_body(k, empty=False):
    """a money sack hanging from its tied neck at (0, 0): plump canvas (no marks) or limp and empty with the lining turned out."""
    cc = CANVAS_C
    if not empty:
        d = "M-0.05,0.05 Q-0.13,0.10 -0.22,0.24 Q-0.28,0.40 -0.14,0.48 Q0,0.52 0.14,0.48 Q0.28,0.40 0.22,0.24 Q0.13,0.10 0.05,0.05 Z"
        g = _g3(k, "bag", cc, -0.28, 0, 0.28, 0)
        o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (d, g, k.ink)]
        o.append('<path d="M-0.17,0.22 Q-0.20,0.34 -0.12,0.42" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.55"/>')
        o.append('<path d="M-0.03,0.10 Q-0.05,0.30 -0.02,0.46 M0.07,0.10 Q0.10,0.30 0.08,0.46" fill="none" stroke="%s" stroke-width="0.008" opacity="0.6"/>' % k.c(cc["dark"]))
        # tied neck with a flared mouth
        o.append('<path d="M-0.09,-0.06 Q-0.02,-0.01 0,0.01 Q0.02,-0.01 0.09,-0.06 Q0.06,0.02 0.05,0.05 L-0.05,0.05 Q-0.06,0.02 -0.09,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(cc["base"]), k.ink))
        o.append('<path d="M-0.065,0.035 Q0,0.065 0.065,0.035" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.ink)
        o.append('<path d="M-0.065,0.035 Q0,0.065 0.065,0.035" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % k.c(LEATHER["base"]))
    else:
        d = "M-0.05,0.05 Q-0.10,0.14 -0.15,0.30 Q-0.17,0.44 -0.10,0.50 Q-0.04,0.46 0,0.52 Q0.05,0.46 0.11,0.50 Q0.17,0.44 0.15,0.30 Q0.10,0.14 0.05,0.05 Z"
        o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (d, k.c(cc["base"]), k.ink)]
        o.append('<path d="M-0.08,0.14 Q-0.10,0.30 -0.06,0.44 M0.02,0.12 Q0.04,0.30 0.0,0.44 M0.09,0.16 Q0.12,0.30 0.10,0.42" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(cc["dark"]))
        # inside-out lining pocket sticking out at the bottom corner
        o.append('<path d="M0.09,0.40 Q0.24,0.42 0.28,0.54 Q0.20,0.60 0.11,0.50 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(CREAM["base"]), k.ink))
        o.append('<path d="M-0.09,-0.06 Q-0.02,-0.01 0,0.01 Q0.02,-0.01 0.09,-0.06 Q0.06,0.02 0.05,0.05 L-0.05,0.05 Q-0.06,0.02 -0.09,-0.06 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c(cc["base"]), k.ink))
        o.append('<path d="M-0.065,0.035 Q0,0.060 0.065,0.035" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.c(LEATHER["base"]))
    return "".join(o)


def _tkey_body(k, press=0.0):
    """a telegraph key seen from the side: walnut base block, brass lever with a black knob (hand on the knob at (0, 0)), pivot post."""
    o = []
    gb = _g3(k, "tkb", WALNUT, 0, 0.12, 0, 0.30)
    o.append('<path d="M-0.16,0.20 L0.50,0.20 L0.54,0.32 L-0.20,0.32 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (gb, k.ink))
    o.append('<path d="M-0.15,0.22 L0.49,0.22" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % k.c(WALNUT["light"]))
    o.append('<rect x="0.38" y="0.10" width="0.10" height="0.10" rx="0.012" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c(BRASS["base"]), k.ink))      # pivot post
    ly = 0.05 + 0.04 * press
    o.append('<path d="M-0.06,%.3f L0.44,%.3f" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (ly + 0.06, 0.12, k.ink))
    o.append('<path d="M-0.06,%.3f L0.44,%.3f" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % (ly + 0.06, 0.12, k.c(BRASS["base"])))
    o.append('<path d="M-0.04,%.3f L0.40,%.3f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (ly + 0.045, 0.10, k.c(BRASS["light"])))
    o.append('<circle cx="0.46" cy="0.12" r="0.022" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(BRASS["light"]), k.ink))
    o.append('<ellipse cx="-0.01" cy="%.3f" rx="0.075" ry="0.055" fill="%s" stroke="%s" stroke-width="0.016"/>' % (ly + 0.02, k.c("#2a2628"), k.ink))
    o.append('<path d="M-0.05,%.3f Q-0.02,%.3f 0.01,%.3f" fill="none" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.5"/>' % (ly + 0.00, ly - 0.02, ly - 0.01))
    o.append('<circle cx="0.42" cy="0.26" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/><path d="M0.42,0.26 Q0.62,0.30 0.72,0.34" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (k.c(BRASS["base"]), k.ink, k.c(COPPER["base"])))
    return "".join(o)


def _candle_body(k, t=0.0):
    """a brass chamberstick: a dish with a ring handle on the -x side (hand at the handle), a cream candle and a flame."""
    o = ['<circle cx="0.02" cy="0.06" r="0.40" fill="#ffd27a" opacity="0.18"/><circle cx="0.20" cy="-0.22" r="0.26" fill="#ffe3a0" opacity="0.22"/>']
    o.append('<ellipse cx="-0.04" cy="0.06" rx="0.065" ry="0.075" fill="none" stroke="%s" stroke-width="0.042"/>' % k.ink)
    o.append('<ellipse cx="-0.04" cy="0.06" rx="0.065" ry="0.075" fill="none" stroke="%s" stroke-width="0.020"/>' % k.c(BRASS["base"]))
    o.append('<path d="M0.02,0.04 L0.40,0.04 Q0.43,0.10 0.36,0.13 L0.06,0.13 Q-0.01,0.10 0.02,0.04 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M0.06,0.06 L0.36,0.06" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % k.c(BRASS["light"]))
    o.append('<rect x="0.15" y="-0.22" width="0.10" height="0.27" rx="0.012" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c(CREAM["light"]), k.ink))
    o.append('<path d="M0.16,-0.20 q0.02,0.06 0.01,0.12" fill="none" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c(CREAM["dark"]))
    lean = 0.025 * math.sin(t * 2 * math.pi * 2.0)
    o.append('<path d="M%.3f,-0.23 Q%.3f,-0.30 %.3f,-0.42 Q%.3f,-0.30 %.3f,-0.23 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (0.20 - 0.035, 0.20 - 0.05 + lean, 0.20 + lean * 1.6, 0.20 + 0.05 + lean, 0.20 + 0.035, k.c("#ffb43a"), k.ink))
    o.append('<path d="M0.20,-0.24 Q0.185,-0.30 0.20,-0.34 Q0.215,-0.30 0.20,-0.24 Z" fill="#fff6c8"/>')
    return "".join(o)


def _hat_shape(k, col, dx, yb, yt, tw, bw, brim_w, nm="hs"):
    """a stovepipe: straight tall crown (half-width bw at the brim .. tw at the top), a ribbon band, a narrow brim curled up at the sides."""
    g = CE._gradient(k, nm, col, x0=-0.38, x1=0.38, mid=0.30)
    o = []
    crown = "M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - bw, yb, dx - tw, yt, dx, yt - 0.06, dx + tw, yt, dx + bw, yb, dx, yb + 0.04, dx - bw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.9"/>' % (dx - tw, yt, dx, yt + 0.06, dx + tw, yt, k.c(col["dark"])))
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - bw - 0.004, yb - 0.15, dx, yb - 0.11, dx + bw + 0.004, yb - 0.15, dx + bw, yb, dx, yb + 0.04, dx - bw, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (band, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round" opacity="0.75"/>' % (dx - 0.19, yt + 0.10, dx - 0.18, yb - 0.19, k.c(col["shine"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>' % (dx - 0.10, yt + 0.12, dx - 0.095, yb - 0.19, k.c(col["shine"])))
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - brim_w, yb - 0.08, dx - brim_w + 0.02, yb + 0.03, dx - 0.30, yb + 0.04, dx, yb + 0.10, dx + 0.30, yb + 0.04, dx + brim_w - 0.02, yb + 0.03, dx + brim_w, yb - 0.08,
        dx + brim_w - 0.10, yb - 0.02, dx, yb - 0.01, dx - brim_w + 0.10, yb - 0.02, dx - brim_w, yb - 0.08)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (brim, k.c(col["brim"]), k.ink))
    return "".join(o)


STOVE_COL = dict(light="#4a4650", base="#26222a", dark="#121016", shine="#9a96a4", band="#141018", brim="#1e1a22")


def _slouch_shape(k, col, dx, nm="sl"):
    """a soft felt slouch hat: wide drooping brim, a dented crown with a pinch, a leather band."""
    g = CE._gradient(k, nm, col, x0=-0.45, x1=0.45, mid=0.32)
    o = []
    brim = "M%.4f,-0.36 Q%.4f,-0.46 %.4f,-0.43 Q%.4f,-0.48 %.4f,-0.36 Q%.4f,-0.21 %.4f,-0.26 Q%.4f,-0.17 %.4f,-0.25 Q%.4f,-0.19 %.4f,-0.36 Z" % (
        dx - 0.66, dx - 0.40, dx, dx + 0.40, dx + 0.66, dx + 0.66, dx + 0.34, dx, dx - 0.34, dx - 0.64, dx - 0.66)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (brim, g, k.ink))
    crown = ("M%.4f,-0.37 C%.4f,-0.58 %.4f,-0.74 %.4f,-0.72 C%.4f,-0.69 %.4f,-0.78 %.4f,-0.76 C%.4f,-0.73 %.4f,-0.58 %.4f,-0.37 Q%.4f,-0.30 %.4f,-0.37 Z"
             % (dx - 0.40, dx - 0.42, dx - 0.34, dx - 0.20, dx - 0.10, dx + 0.04, dx + 0.14, dx + 0.36, dx + 0.42, dx + 0.40, dx, dx - 0.40))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (crown, g, k.ink))
    o.append('<path d="M%.4f,-0.70 Q%.4f,-0.60 %.4f,-0.50" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>' % (dx - 0.02, dx + 0.02, dx - 0.04, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.64 Q%.4f,-0.52 %.4f,-0.42" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.6"/>' % (dx - 0.26, dx - 0.30, dx - 0.30, k.c(col["light"])))
    band = "M%.4f,-0.45 Q%.4f,-0.41 %.4f,-0.45 L%.4f,-0.35 Q%.4f,-0.30 %.4f,-0.35 Z" % (dx - 0.41, dx, dx + 0.41, dx + 0.40, dx, dx - 0.40)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (band, k.c("#3a2a20"), k.ink))
    return "".join(o)


def _cane_body(k):
    """a black cane with a gold knob: knob at -0.04, shaft to the gold ferrule at 1.40."""
    o = ['<path d="M0.0,0 L1.40,0" stroke="%s" stroke-width="0.064" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M0.0,0 L1.40,0" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>' % k.c("#2a2024"))
    o.append('<path d="M0.10,-0.008 L1.30,-0.008" stroke="#ffffff" stroke-width="0.008" opacity="0.4"/>')
    o.append('<path d="M1.34,0 L1.42,0" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M1.34,0 L1.42,0" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (k.ink, k.c(BRASS["base"])))
    o.append('<circle cx="-0.04" cy="0" r="0.072" fill="%s" stroke="%s" stroke-width="0.016"/><path d="M-0.08,-0.03 A0.05,0.05 0 0 1 -0.03,-0.06" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
             % (k.c(BRASS["base"]), k.ink, k.c(BRASS["light"])))
    return "".join(o)


def _palette_body(k):
    """an artist's kidney palette 0.62 x 0.44: walnut, a thumb hole, dabs of red, ochre, blue, white, green and brown paint."""
    g = _g3(k, "pal", dict(light="#d9b27a", base="#b8864e", dark="#7a5530"), -0.1, -0.2, 0.5, 0.2)
    pts = [(-0.06, -0.10), (0.10, -0.20), (0.34, -0.22), (0.52, -0.12), (0.54, 0.06), (0.44, 0.20), (0.24, 0.22), (0.12, 0.12), (0.02, 0.15), (-0.08, 0.06)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (P._smooth_closed(pts), g, k.ink)]
    o.append('<ellipse cx="0.04" cy="-0.02" rx="0.035" ry="0.026" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#6a4a2c"), k.ink))
    for (x, y, c) in ((0.16, -0.14, "#c0392b"), (0.28, -0.16, "#e0a92a"), (0.40, -0.10, "#2c4f9e"), (0.46, 0.02, "#f6f2e6"), (0.38, 0.12, "#2f7a4a"), (0.24, 0.08, "#6a3a1e")):
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.048" ry="0.032" fill="%s" stroke="%s" stroke-width="0.008"/>' % (x, y, k.c(c), k.ink))
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="0.016" ry="0.008" fill="#ffffff" opacity="0.5"/>' % (x - 0.016, y - 0.010))
    return "".join(o)


def _brush_small(k, paint="#9c3a2a"):
    """an artist's brush 0.80 long: walnut handle (-0.10 .. 0.52), brass ferrule, a loaded round tip to 0.80."""
    o = ['<path d="M-0.10,-0.014 L0.52,-0.026 L0.52,0.026 L-0.10,0.014 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c(WALNUT["base"]), k.ink)]
    o.append('<path d="M0.52,-0.026 L0.64,-0.032 L0.64,0.032 L0.52,0.026 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), k.ink))
    o.append('<path d="M0.64,-0.032 Q0.74,-0.034 0.82,0 Q0.74,0.034 0.64,0.032 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(paint), k.ink))
    return "".join(o)


def _shovel_body(k):
    """a long-handled shovel 2.0 long: D grip at -0.10, ash handle to 1.55, a dark iron blade 1.55 .. 2.0 with a rolled top."""
    o = ['<path d="M-0.10,0 L1.62,0" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.10,0 L1.62,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c(WALNUT["light"]))
    o.append('<path d="M0.0,-0.012 L1.60,-0.012" stroke="#ffffff" stroke-width="0.008" opacity="0.4"/>')
    o.append('<path d="M-0.10,0 Q-0.20,-0.02 -0.20,-0.10 Q-0.18,-0.20 -0.06,-0.20" fill="none" stroke="%s" stroke-width="0.070" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M-0.10,0 Q-0.20,-0.02 -0.20,-0.10 Q-0.18,-0.20 -0.06,-0.20" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % k.c(WALNUT["light"]))
    gb = _g3(k, "shv", IRON, 1.5, 0, 2.0, 0)
    o.append('<path d="M1.52,-0.10 L1.60,-0.16 L1.98,-0.17 Q2.05,0 1.98,0.17 L1.60,0.16 L1.52,0.10 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (gb, k.ink))
    o.append('<path d="M1.62,-0.12 L1.96,-0.13" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.5"/>')
    o.append('<path d="M1.52,-0.10 Q1.50,0 1.52,0.10" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c(IRON["dark"]))
    return "".join(o)


def _pick_body(k):
    """a pickaxe 1.6 long: handle -0.10 .. 1.50, a curved double-spiked iron head across the end."""
    o = ['<path d="M-0.10,0 L1.50,0" stroke="%s" stroke-width="0.080" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.10,0 L1.50,0" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % k.c(WALNUT["light"]))
    o.append('<path d="M0.0,-0.012 L1.42,-0.012" stroke="#ffffff" stroke-width="0.008" opacity="0.4"/>')
    hd = "M1.50,-0.36 Q1.62,-0.22 1.58,0 Q1.62,0.22 1.50,0.36 Q1.46,0.16 1.44,0.05 L1.44,-0.05 Q1.46,-0.16 1.50,-0.36 Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (hd, _g3(k, "pck", IRON, 1.4, 0, 1.65, 0), k.ink))
    o.append('<path d="M1.50,-0.30 Q1.56,-0.18 1.54,-0.04" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.5"/>')
    return "".join(o)


def _pole_body(k, a, b):
    """a telegraph pole: a long walnut-brown round pole from x = a to x = b, 0.15 thick, bark rings, pale cut ends."""
    th = 0.075
    g = _g3(k, "pol", dict(light="#c8975e", base="#8a5a34", dark="#4e3018"), 0, -th, 0, th)
    o = ['<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (a, -th, b, -th, b, th, a, th, g, k.ink)]
    for i in range(int((b - a) / 0.42)):
        x = a + 0.30 + i * 0.42
        o.append('<path d="M%.3f,%.3f Q%.3f,0 %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.7"/>' % (x, -th + 0.01, x + 0.02, x, th - 0.01, k.c(WALNUT["dark"])))
    o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.35"/>' % (a + 0.05, -th + 0.025, b - 0.05, -th + 0.025))
    o.append('<ellipse cx="%.3f" cy="0" rx="0.026" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.012"/>' % (b, th, k.c("#e8c690"), k.ink))
    return "".join(o)


def _plough_body(k):
    """a plough handle from the hand (grip end at -0.30) down and forward to the beam bracket at 1.20: the hand grips near x 0."""
    o = ['<path d="M-0.30,0 L1.15,0" stroke="%s" stroke-width="0.090" stroke-linecap="round"/>' % k.ink]
    o.append('<path d="M-0.30,0 L1.15,0" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % k.c(WALNUT["light"]))
    o.append('<path d="M-0.28,-0.014 L1.10,-0.014" stroke="#ffffff" stroke-width="0.008" opacity="0.4"/>')
    o.append('<rect x="1.08" y="-0.075" width="0.20" height="0.15" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c(IRON["base"]), k.ink))
    o.append('<circle cx="1.14" cy="0" r="0.018" fill="%s"/><circle cx="1.23" cy="0" r="0.018" fill="%s"/>' % (k.c(IRON["light"]), k.c(IRON["light"])))
    return "".join(o)


def _keyring_body(k):
    """an iron ring of old keys hanging from the hand at (0, 0): a ring and five skeleton keys fanned down."""
    o = []
    ks = ((-0.16, 0.30, -14), (-0.08, 0.34, -6), (0.0, 0.36, 2), (0.09, 0.33, 9), (0.16, 0.29, 16))
    for (x, ln, a) in ks:
        o.append('<g transform="translate(%.3f 0.16) rotate(%d)"><path d="M0,0 L0,%.3f" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M0,0 L0,%.3f" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>'
                 '<path d="M0,%.3f l0.07,0 M0,%.3f l0.05,0" stroke="%s" stroke-width="0.036" stroke-linecap="round"/><path d="M0,%.3f l0.07,0 M0,%.3f l0.05,0" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                 '<circle cx="0" cy="0" r="0.036" fill="none" stroke="%s" stroke-width="0.040"/><circle cx="0" cy="0" r="0.036" fill="none" stroke="%s" stroke-width="0.018"/></g>'
                 % (x, a, ln, k.ink, ln, k.c(IRON["light"]), ln, ln - 0.07, k.ink, ln, ln - 0.07, k.c(IRON["light"]), k.ink, k.c(IRON["light"])))
    o.append('<circle cx="0" cy="0.10" r="0.095" fill="none" stroke="%s" stroke-width="0.046"/><circle cx="0" cy="0.10" r="0.095" fill="none" stroke="%s" stroke-width="0.022"/>' % (k.ink, k.c(IRON["light"])))
    return "".join(o)


NEW_PROPS16 = ("letter", "wire_coil", "magnet", "bottle", "money_bag", "money_bag_empty", "telegraph_key", "candle", "stovepipe_held", "slouch_held",
               "cane16", "palette16", "brush16", "shovel16", "pick16", "pole16", "pole16_end", "plough16", "keyring16")
NEW_TIP16 = {"letter": 0.20, "wire_coil": 0.0, "magnet": 0.50, "bottle": 0.29, "money_bag": 0.50, "money_bag_empty": 0.50, "telegraph_key": 0.0, "candle": 0.20,
             "stovepipe_held": 0.0, "slouch_held": 0.0, "cane16": 1.42, "palette16": 0.30, "brush16": 0.82, "shovel16": 2.0, "pick16": 1.6, "pole16": 2.4,
             "pole16_end": 3.4, "plough16": 1.2, "keyring16": 0.5}
_UPRIGHT = {"letter": (0.20, -0.02), "wire_coil": (0.16, 0.0), "money_bag": (0.0, 0.0), "money_bag_empty": (0.0, 0.0), "telegraph_key": (0.0, 0.0),
            "candle": (0.04, -0.06), "stovepipe_held": (0.0, 0.0), "slouch_held": (0.0, 0.30), "keyring16": (0.0, 0.0)}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS16:
        return _O16["_prop"](k, kind, H, ang, sc)
    key = C10.C8._side_key()
    an = C10.C8._POSE8["an"]
    ext = []
    if kind in _UPRIGHT:
        dx, dy = _UPRIGHT[kind]
        if kind == "letter":
            body = _letter_body(k)
            ext = [(-0.2, -0.14), (0.2, 0.14), (0.2, -0.14), (-0.2, 0.14)]
        elif kind == "wire_coil":
            body = _coil_body(k)
            ext = [(-0.22, -0.22), (0.22, 0.22), (0.38, 0.36), (-0.22, 0.22), (0.22, -0.22)]
        elif kind in ("money_bag", "money_bag_empty"):
            body = _bag_body(k, kind == "money_bag_empty")
            ext = [(-0.28, 0.0), (0.28, 0.58), (-0.28, 0.58), (0.28, 0.0)]
        elif kind == "telegraph_key":
            body = _tkey_body(k, _POSE16["bag"])
            ext = [(-0.2, 0.0), (0.72, 0.36), (-0.2, 0.36), (0.72, 0.0)]
            an["key_tip_" + key] = (H[0] + dx * sc, H[1] + dy * sc)
        elif kind == "candle":
            body = _candle_body(k, _POSE16["t"])
            ext = [(-0.14, -0.45), (0.44, 0.16), (0.44, -0.45), (-0.14, 0.16)]
            an["flame_" + key] = (H[0] + (dx + 0.20) * sc, H[1] + (dy - 0.32) * sc)
        elif kind == "stovepipe_held":
            body = _hat_shape(k, STOVE_COL, 0.0, 0.0, -0.66, 0.32, 0.30, 0.50, nm="hh")
            ext = [(-0.52, -0.72), (0.52, 0.12), (0.52, -0.72), (-0.52, 0.12)]
        elif kind == "slouch_held":
            body = _slouch_shape(k, FELT, 0.0, nm="hh")
            ext = [(-0.68, -0.40), (0.68, 0.12), (0.68, -0.40), (-0.68, 0.12)]
        else:
            body = _keyring_body(k)
            ext = [(-0.25, 0.0), (0.25, 0.55), (-0.25, 0.55), (0.25, 0.0)]
        o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + dx * sc * (0 if kind in ("stovepipe_held", "slouch_held") else 1), H[1] + (dy if kind in ("stovepipe_held", "slouch_held") else 0.0) * sc, sc, body)
        if kind in ("letter",):
            o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + 0.12 * sc, H[1] - 0.02 * sc, sc, body)
        elif kind == "wire_coil":
            o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + 0.10 * sc, H[1] + 0.02 * sc, sc, body)
        elif kind == "candle":
            o = '<g transform="translate(%.4f %.4f) scale(%.4f)">%s</g>' % (H[0] + 0.04 * sc, H[1] - 0.06 * sc, sc, body)
        ox = {"letter": 0.12, "wire_coil": 0.10, "candle": 0.04}.get(kind, 0.0)
        oy = {"letter": -0.02, "wire_coil": 0.02, "candle": -0.06, "stovepipe_held": 0.0, "slouch_held": 0.30}.get(kind, 0.0)
        for (x, y) in ext:
            k.ext.append((H[0] + (x + ox) * sc, H[1] + (y + oy) * sc, 0.03))
        tipd = NEW_TIP16[kind]
        return o, (H[0] + ox * sc, H[1] + oy * sc + tipd * 0.0)
    # props following the forearm / the angle
    if kind == "magnet":
        body, pts = _magnet_body(k, _POSE16["glint"]), ((0.0, -0.2), (0.66, -0.2), (0.66, 0.2), (0.0, 0.2))
    elif kind == "bottle":
        body, pts = _bottle_body(k, _POSE16["glint"]), ((-0.56, -0.11), (0.30, -0.06), (0.30, 0.06), (-0.56, 0.11))
    elif kind == "cane16":
        body, pts = _cane_body(k), ((-0.12, -0.08), (1.44, 0.04))
    elif kind == "palette16":
        body, pts = _palette_body(k), ((-0.1, -0.24), (0.56, -0.24), (0.56, 0.24), (-0.1, 0.24))
    elif kind == "brush16":
        body, pts = _brush_small(k), ((-0.12, -0.04), (0.84, 0.04))
    elif kind == "shovel16":
        body, pts = _shovel_body(k), ((-0.22, -0.22), (2.06, -0.18), (2.06, 0.18))
    elif kind == "pick16":
        body, pts = _pick_body(k), ((-0.12, -0.06), (1.64, -0.38), (1.64, 0.38))
    elif kind == "pole16":
        body, pts = _pole_body(k, -1.2, 2.4), ((-1.22, -0.08), (2.44, 0.08))
    elif kind == "pole16_end":
        body, pts = _pole_body(k, -0.2, 3.4), ((-0.22, -0.08), (3.44, 0.08))
    else:
        body, pts = _plough_body(k), ((-0.32, -0.06), (1.30, -0.08), (1.30, 0.08))
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, body)
    for (x, y) in pts:
        px, py = _rot(x * sc, y * sc, ang)
        k.ext.append((H[0] + px, H[1] + py, 0.03))
    tx, ty = _rot(NEW_TIP16[kind] * sc, 0.0, ang)
    tip = (H[0] + tx, H[1] + ty)
    an[{"magnet": "magnet_", "bottle": "bottle_", "cane16": "cane_", "palette16": "palette_", "brush16": "brush_", "shovel16": "blade_", "pick16": "pickhead_",
        "pole16": "pole_tip_", "pole16_end": "pole_tip_", "plough16": "beam_"}[kind] + key] = tip
    if kind in ("shovel16", "pick16", "plough16", "cane16", "pole16", "pole16_end"):
        gx, gy = _rot(0.55 * sc, 0.0, ang)
        an["grip_far_" + key] = (H[0] + gx, H[1] + gy)
    return o, tip


# ============================================================================= hats (head frame)
def _hat_stovepipe16(k, C, yaw):
    dx = -0.03 * yaw
    yb, yt = -0.36, -1.24
    o = '<g transform="rotate(%.3f)">%s</g>' % (C["hat_tilt"], _hat_shape(k, C["hat_colors"], dx, yb, yt, 0.30, 0.34, 0.52))
    C4._ext_hat(k, C, ((dx - 0.56, yb - 0.08), (dx + 0.56, yb - 0.08), (dx - 0.30, yt - 0.03), (dx + 0.30, yt - 0.03), (dx, yb + 0.12)))
    return o, (dx, yt - 0.06)


def _hat_slouch16(k, C, yaw):
    dx = -0.03 * yaw
    o = '<g transform="rotate(%.3f)">%s</g>' % (C["hat_tilt"], _slouch_shape(k, C["hat_colors"], dx))
    C4._ext_hat(k, C, ((dx - 0.68, -0.36), (dx + 0.68, -0.36), (dx, -0.78), (dx - 0.34, -0.20), (dx + 0.34, -0.20)))
    return o, (dx, -0.77)


def _hat_mane16(k, C, yaw):
    """Morse's hair: a swept-back mane mass rising off the forehead (a lock sweeping to the back), longer behind the ears."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    sw = C.get("mane_sweep", 1.0)
    g = CE._gradient(k, "mn", col, x0=-0.5, x1=0.5, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    mass = [(-0.50 + dx, -0.02), (-0.56 + dx, -0.32), (-0.42 + dx, -0.58), (-0.12 + dx, -0.74 * sw), (0.24 + dx, -0.80 * sw), (0.50 + dx, -0.66), (0.58 + dx, -0.40),
            (0.54 + dx, -0.10)]
    inner = [(0.42 + dx, -0.24), (0.26 + dx, -0.38), (0.04 + dx, -0.44), (-0.18 + dx, -0.40), (-0.36 + dx, -0.28), (-0.44 + dx, -0.12)]
    d = P._smooth_open(mass) + " L%.4f,%.4f " % (0.50 + dx, -0.04) + P._smooth_open(inner)[1:].replace("M", "L", 1) + " Z"
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, g, k.ink))
    st = []
    for i, x in enumerate((-0.34, -0.20, -0.04, 0.12, 0.28, 0.40)):
        st.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (x + dx, -0.34 - 0.02 * i % 3 * 0.01, x + 0.10 + dx, -0.52 - 0.03 * (i % 3), x + 0.22 + dx, -0.60 + 0.02 * (i % 2)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % ("".join(st), k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.52 Q%.4f,-0.64 %.4f,-0.66" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>' % (-0.26 + dx, -0.20 + dx, 0.06 + dx, k.c(col["light"])))
    # the lock swept over the brow
    o.append('<path d="M%.4f,-0.36 Q%.4f,-0.22 %.4f,-0.24 Q%.4f,-0.30 %.4f,-0.40 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (-0.02 + dx, 0.10 + dx + 0.06 * yaw, 0.26 + dx + 0.06 * yaw, 0.16 + dx, 0.06 + dx, k.c(col["base"]), k.ink))
    o.append('</g>')
    C4._ext_hat(k, C, ((-0.56 + dx, -0.30), (0.56 + dx, -0.30), (dx, -0.74 * sw), (-0.50 + dx, 0.0), (0.54 + dx, 0.0)))
    return "".join(o), (dx, -0.72 * sw)


HATS16 = {"stovepipe16": _hat_stovepipe16, "slouch16": _hat_slouch16, "mane16": _hat_mane16}


# ============================================================================= costumes (torso-local)
def _belly_poly(X, s, yB, a):
    """outline of the waistcoat over the belly (V neck, bulging to the sides, a point at the hem); a = half width factor."""
    pts = [X(-0.20, 0.40), X(0.20, 0.40), X(0.36 * s * a, 0.62), X(0.52 * s * a, 0.84), X(0.60 * s * a, yB - 0.30), X(0.56 * s * a, yB - 0.12), X(0.34 * s * a, yB + 0.02),
           X(0.0, yB + 0.07), X(-0.34 * s * a, yB + 0.02), X(-0.56 * s * a, yB - 0.12), X(-0.60 * s * a, yB - 0.30), X(-0.52 * s * a, 0.84), X(-0.36 * s * a, 0.62)]
    return pts


def _cos_tail16(k, C, m):
    """the mocker: an open black tailcoat over a big plaid waistcoat that fills the belly (gold buttons, a watch chain with a fob),
    a white shirt V and a cravat; side tails over the hips.  CAST sash16: a federal-green postmaster sash across the chest (gold
    edges) ending in a leather mail bag at the hip, an iron key ring on the belt."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    s = hw / 0.74
    o = []
    vp = _belly_poly(X, s, yB, 1.0)
    vest = C2._grad(k, "vs", col["vest"], -0.4, 0.4)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (_poly_d(vp), vest, k.ink))
    k.defs.append('<clipPath id="%s_vp"><path d="%s"/></clipPath>' % (k.uid, _poly_d(vp)))
    pl = []
    x = -0.62 * s
    while x < 0.62 * s:
        pl.append('<path d="M%.4f,0.36 L%.4f,%.4f" stroke="%s" stroke-width="0.030" opacity="0.75"/>' % (X(x, 0.5)[0], X(x, 0.5)[0], yB + 0.1, k.c(col["plaid"])))
        pl.append('<path d="M%.4f,0.36 L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (X(x + 0.07, 0.5)[0], X(x + 0.07, 0.5)[0], yB + 0.1, k.c(col["plaid2"])))
        x += 0.17 * s
    y = 0.45
    while y < yB + 0.1:
        pl.append('<path d="M-1.2,%.4f L1.2,%.4f" stroke="%s" stroke-width="0.030" opacity="0.75"/>' % (y, y, k.c(col["plaid"])))
        pl.append('<path d="M-1.2,%.4f L1.2,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (y + 0.07, y + 0.07, k.c(col["plaid2"])))
        y += 0.17
    o.append('<g clip-path="url(#%s_vp)">%s</g>' % (k.uid, "".join(pl)))
    # belly shading
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.030" stroke-linecap="round" opacity="0.18"/>' % (X(-0.40 * s, 0.86) + X(-0.46 * s, 1.0) + X(-0.40 * s, yB - 0.20)))
    o.append(_poly(k, [X(-0.12, 0.40), X(0.12, 0.40), X(0.0, TT + h * 0.34)], k.c(col["shirt"]), 0.012))
    o.append(C7._neck(k, X, col, C.get("neck", "cravat")))
    nb = 5
    for i in range(nb):
        yy = TT + h * 0.46 + i * (h * 0.46) / (nb - 1)
        o.append(_circ(X(0.0, yy), 0.026, k.c(BRASS["base"]), k, 0.009))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.009" fill="%s"/>' % (X(0.0, yy)[0] - 0.008, yy - 0.008, k.c(BRASS["light"])))
    a0, a1 = X(0.0, TT + h * 0.56), X(0.40 * s, TT + h * 0.60)
    cm = X(0.22 * s, TT + h * 0.80)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a0 + cm + a1)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (d, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" stroke-dasharray="0.020 0.010"/>' % (d, k.c(BRASS["base"])))
    fx, fy = X(0.30 * s, TT + h * 0.74)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012"/><circle cx="%.4f" cy="%.4f" r="0.034" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="%.4f" cy="%.4f" r="0.012" fill="%s"/>'
             % (cm[0] + 0.02, cm[1] - 0.02, fx, fy, k.ink, fx, fy + 0.03, k.c(BRASS["base"]), k.ink, fx - 0.010, fy + 0.020, k.c(BRASS["light"])))
    # coat fronts: black panels at the sides, silk lapels
    lap = k.c(col["lapel"])
    for sg in (-1, 1):
        panel = [X(sg * 0.22, 0.32), X(sg * 0.30, 0.52), X(sg * 0.50 * s, 0.84), X(sg * 0.64 * s, yB - 0.30), X(sg * 0.60 * s, yB - 0.12), X(sg * 0.40 * s, yB + 0.04),
                 X(sg * (hw + 0.30), yB + 0.04), X(sg * (hw + 0.30), 0.30)]
        o.append('<path d="%s" fill="url(#%s_tg)" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (_poly_d(panel), k.uid, k.ink))
        lp = [X(sg * 0.12, 0.38), X(sg * 0.26, 0.42), X(sg * 0.38, 0.52), X(sg * 0.30, 0.58), X(sg * 0.38 * s, 0.70), X(sg * 0.20, 0.66)]
        o.append(_poly(k, lp, lap, 0.014))
        o.append(_circ(X(sg * 0.40 * s, 0.82), 0.022, k.c("#1a1418"), k, 0.008))
    sash_over = ""
    if C.get("sash16"):
        sc_ = col.get("sash", FED_GREEN["base"])
        pa, pb = X(0.30 * s, 0.38), X(-0.52 * s, yB - 0.10)         # from the screen-right shoulder to the screen-left hip
        pa, pb = X(-0.26 * s, 0.36), X(0.58 * s, yB - 0.02)
        dx_, dy_ = pb[0] - pa[0], pb[1] - pa[1]
        L = math.hypot(dx_, dy_)
        ux, uy = dx_ / L, dy_ / L
        nx, ny = -uy, ux
        wd = 0.15
        q = [(pa[0] + nx * wd, pa[1] + ny * wd), (pb[0] + nx * wd, pb[1] + ny * wd), (pb[0] - nx * wd, pb[1] - ny * wd), (pa[0] - nx * wd, pa[1] - ny * wd)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (_poly_d(q), k.c(sc_), k.ink))
        for e in (-0.105, 0.105):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020"/>' % (pa[0] + nx * e, pa[1] + ny * e, pb[0] + nx * e, pb[1] + ny * e, k.c(BRASS["base"])))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.014" opacity="0.25"/>' % (pa[0] + nx * 0.04, pa[1] + ny * 0.04, pb[0] + nx * 0.04, pb[1] + ny * 0.04))
        mx_, my_ = pa[0] + dx_ * 0.40, pa[1] + dy_ * 0.40
        o.append('<circle cx="%.4f" cy="%.4f" r="0.052" fill="%s" stroke="%s" stroke-width="0.014"/><circle cx="%.4f" cy="%.4f" r="0.024" fill="%s" stroke="%s" stroke-width="0.008"/>'
                 % (mx_, my_, k.c(BRASS["base"]), k.ink, mx_, my_, k.c(FED_GREEN["dark"]), k.ink))
        sash_over = (pb, (ux, uy))
    inside = "".join(o)
    # the tails behind the hips
    bk = []
    for sg in (-1, 1):
        tl = [X(sg * 0.50 * s, yB - 0.24), X(sg * (hw - 0.02), yB - 0.24), X(sg * (hw + 0.10), yB + 0.34), X(sg * 0.60 * s, yB + 0.38)]
        bk.append('<path d="%s" fill="url(#%s_tg)" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(tl), k.uid, k.ink))
        bk.append(_ln([X(sg * 0.64 * s, yB - 0.04), X(sg * 0.68 * s, yB + 0.32)], k.c(col["dark"]), 0.012))
        k.ext.append(X(sg * (hw + 0.10), yB + 0.34) + (0.03,))
    ov = []
    if C.get("sash16"):
        # mail bag on the screen-right hip, key ring on the belt at the screen-left
        bx, by = X(0.62 * s, yB + 0.04)
        gb = _g3(k, "mbg", LEATHER, bx - 0.20, 0, bx + 0.20, 0)
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>'
                  % (bx - 0.02, by - 0.28, bx + 0.02, by + 0.02, k.ink, bx - 0.02, by - 0.28, bx + 0.02, by + 0.02, k.c(LEATHER["dark"])))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
                  % (bx - 0.19, by, bx + 0.19, by, bx + 0.21, by + 0.34, bx, by + 0.40, bx - 0.21, by + 0.34, gb, k.ink))
        ov.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>'
                  % (bx - 0.20, by - 0.03, bx, by + 0.20, bx + 0.20, by - 0.03, bx + 0.19, by, bx - 0.19, by, k.c(LEATHER["dark"]), k.ink))
        ov.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.075" rx="0.010" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx - 0.03, by + 0.11, k.c(BRASS["base"]), k.ink))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" stroke-dasharray="0.02 0.015" opacity="0.7"/>' % (bx - 0.16, by + 0.30, bx + 0.16, by + 0.30, k.c(LEATHER["light"])))
        for (x, y) in ((bx - 0.22, by + 0.38), (bx + 0.22, by + 0.38), (bx, by - 0.30), (bx + 0.20, by - 0.02)):
            k.ext.append((x, y, 0.03))
        kx, ky = X(-0.46 * s, yB - 0.08)
        if _POSE16["keys"] > 0.5:
            ov.append('<g transform="translate(%.4f %.4f)">%s</g>' % (kx, ky, _keyring_body(k)))
            for (x, y) in ((kx - 0.2, ky + 0.50), (kx + 0.2, ky + 0.50), (kx, ky - 0.02)):
                k.ext.append((x, y, 0.03))
    return inside, "".join(bk), "".join(ov)


def _cos_braces16(k, C, m):
    """shirt, braces and trousers (no coat): a buttoned placket, collar band, two braces from the shoulders to brass clips at the
    waist, a belt, optional plaid shirt (colors plaid) and dirt smudges (C dirt16)."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    hw = m.hwa
    s = min(1.5, hw / 0.70)
    o = [CE._bowl(k, col["pants"], yB - 0.10, yB, dip=0.03)]
    if col.get("plaid"):
        pl = []
        for i in range(-5, 6):
            pl.append('<path d="M%.4f,0.40 L%.4f,%.4f" stroke="%s" stroke-width="0.022" opacity="0.45"/>' % (X(i * 0.17 * s, 0.5)[0], X(i * 0.17 * s, 0.5)[0], yB, k.c(col["plaid"])))
        for j in range(0, 6):
            yy = 0.46 + j * 0.17
            pl.append('<path d="M-1.2,%.4f L1.2,%.4f" stroke="%s" stroke-width="0.022" opacity="0.45"/>' % (yy, yy, k.c(col["plaid"])))
        o.append("".join(pl))
    o.append(_ln([X(0.0, 0.44), X(0.0, yB - 0.10)], k.c(col.get("dark", "#8a8070")), 0.012))
    for yy in (0.56, 0.72, 0.88):
        if yy < yB - 0.16:
            o.append(_circ(X(0.02, yy), 0.015, k.c(col.get("button", "#efe6d2")), k, 0.007))
    o.append(_poly(k, [X(-0.11, 0.40), X(0.0, 0.52), X(0.11, 0.40), X(0.0, 0.44)], k.c(col.get("collar", col["base"])), 0.010))
    for sg in (-1, 1):
        pa, pb = X(sg * 0.17, 0.36), X(sg * (0.21 + 0.03 * (s - 1)), yB - 0.02)
        o.append(_ln([pa, pb], k.ink, 0.074))
        o.append(_ln([pa, pb], k.c(col["brace"]), 0.050))
        o.append(_ln([(pa[0] - 0.012, pa[1] + 0.02), (pb[0] - 0.012, pb[1] - 0.04)], k.c(col.get("brace_l", "#8a6440")), 0.012, ' opacity="0.7"'))
        cx_, cy_ = X(sg * (0.21 + 0.03 * (s - 1)), yB - 0.10)
        o.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.050" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>' % (cx_ - 0.03, cy_ - 0.025, k.c(BRASS["base"]), k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034"/>' % (X(-hw, yB - 0.06) + X(0, yB - 0.03) + X(hw, yB - 0.06) + (k.c(col.get("belt", "#3a2a20")),)))
    if C.get("dirt16"):
        for i in range(6):
            x, y = -0.30 + 0.60 * C10._hash(C["seed"], i), 0.62 + (yB - 0.78) * C10._hash(C["seed"], i + 20)
            c_ = X(x, y)
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.28" transform="rotate(%d %.4f %.4f)"/>' % (c_ + (0.03 + 0.03 * C10._hash(C["seed"], i + 9), 0.018, k.c("#3a2a1c"), 20 * i, c_[0], c_[1])))
    return "".join(o), "", ""


COSTUMES16 = {"tail16": _cos_tail16, "braces16": _cos_braces16}


# ============================================================================= face: side-whiskers, collar points, florid nose
def _whisker_path(k, s, a, y0, y1, w0, w1, wmid=None):
    """one side-whisker: its outer edge follows the head edge (scaled by sin of the turn angle a), the inner edge is w wide, widest
    at the bottom (mutton chop) or in the middle (long whisker); a rounded lower end."""
    R = 0.472
    f = math.sin(abs(a))
    cw = max(0.30, math.cos(a) * 0.0 + (1.0 - 0.45 * (f - 0.9) / 0.1 if f > 0.9 else 1.0))
    n = 8
    outer, inner = [], []
    for i in range(n + 1):
        t = i / float(n)
        y = y0 + (y1 - y0) * t
        xe = math.sqrt(max(R * R - y * y, 0.0))
        xo = s * (xe * f + 0.012 * (1 - f))
        if wmid is not None:
            w = w0 + (wmid - w0) * math.sin(math.pi * min(1.0, t * 1.15)) * (1 - 0.35 * t) + (w1 - w0) * t * 0.0
            w = max(w, w0 + (w1 - w0) * t)
        else:
            w = w0 + (w1 - w0) * t ** 1.4
        w *= (0.55 + 0.45 * (1.0 - f) * 4.0) if f > 0.80 else 1.0
        w = min(w, 0.30)
        outer.append((xo, y))
        inner.append((xo - s * w, y))
    pts = outer + [(outer[-1][0] - s * w1 * 0.5, y1 + 0.035)] + inner[::-1]
    return P._smooth_closed(pts)


def _whiskers16(k, C, P_, L):
    W = C.get("whisker16")
    if not W:
        return ""
    yaw = P_.get("yaw", 0.0) if isinstance(P_, dict) else 0.0
    col, sh = k.c(W.get("color", "#8a7a6a")), k.c(W.get("shade", "#5e5044"))
    o = []
    for s in (-1, 1):
        a = math.radians(s * 72.0 + 32.0 * yaw)
        if abs(a) > math.radians(97):
            continue
        if W.get("style") == "chops":
            d = _whisker_path(k, s, a, -0.10, W.get("y1", 0.30), 0.06, W.get("w", 0.17))
        else:
            d = _whisker_path(k, s, a, -0.12, W.get("y1", 0.42), 0.055, W.get("w", 0.075), wmid=W.get("wmid", 0.105))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round" opacity="0.98"/>' % (d, col, k.ink))
        f = math.sin(abs(a))
        xe = lambda y: math.sqrt(max(0.472 ** 2 - y * y, 0.0)) * f * s
        st = []
        for j, yy in enumerate((0.0, 0.08, 0.16, 0.24)):
            if yy < W.get("y1", 0.42) - 0.04:
                st.append("M%.4f,%.4f q%.4f,0.07 %.4f,0.11" % (xe(yy) - s * 0.03, yy, -s * 0.004, -s * 0.004))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.85"/>' % ("".join(st), sh))
    return "".join(o)


def _collar16(k, C, P_, L):
    if not C.get("collar16"):
        return ""
    yaw = P_.get("yaw", 0.0) if isinstance(P_, dict) else 0.0
    o = []
    for s in (-1, 1):
        sh = 0.10 * yaw
        x0, x1 = s * 0.075 + sh, s * 0.31 + sh * 0.6
        o.append('<path d="M%.4f,0.52 L%.4f,0.30 L%.4f,0.36 L%.4f,0.48 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (x0, x1, x1 + s * 0.012 - s * 0.03, x0 + s * 0.16, k.c("#ffffff"), k.ink))
        o.append('<path d="M%.4f,0.47 L%.4f,0.34" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % (x0 + s * 0.08, x1 - s * 0.035, k.c("#c8c0b0")))
    return "".join(o)


def _nose16(k, C, P_, L):
    c = C.get("nose16")
    if not c:
        return ""
    cx = (L["xL"] + L["xR"]) / 2.0
    cy = L["ey"] + (L["my"] - L["ey"]) * 0.42
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.042" ry="0.038" fill="%s" stroke="%s" stroke-width="0.012"/><ellipse cx="%.4f" cy="%.4f" rx="0.014" ry="0.010" fill="#ffffff" opacity="0.6"/>'
            % (cx, cy, k.c(c), k.ink, cx - 0.016, cy - 0.016))


def _face(k, C, P_, white):
    svg, L = _O16["_face"](k, C, P_, white)
    if C is None or not C.get("_cast16"):
        return svg, L
    return _nose16(k, C, P_, L) + svg + _whiskers16(k, C, P_, L) + _collar16(k, C, P_, L), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE16["glint"] = _f(g("glint"), 0.0, 0.0, 1.0)
    _POSE16["bag"] = _f(g("key_press"), 0.0, 0.0, 1.0)
    _POSE16["keys"] = _f(g("belt_keys"), 1.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE16["t"] = t if math.isfinite(t) else 0.0
    return _O16["_norm"](C, pose)


# ============================================================================= variants, stool, figure
def _variant(name, pose):
    if not isinstance(pose, dict):
        return name
    if name == "morse16" and pose.get("young"):
        return "morse16_young"
    if name == "mocker":
        return "mocker" + ("_pm" if pose.get("sash") else "") + ("_bare" if pose.get("hat_off") else "")
    if name == "cornell" and pose.get("hat_off"):
        return "cornell_bare"
    return name


def _stool_svg(k, cx, y_seat, y_floor, w):
    """a round three-legged walnut stool: seat top at y_seat (ellipse), legs splayed to the floor."""
    o = []
    for dx_ in (-0.62, 0.62, 0.0):
        x1 = cx + dx_ * w * 0.5
        x0 = cx + dx_ * w * 0.36
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.100" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>'
                 % (x0, y_seat + 0.05, x1, y_floor - 0.03, k.ink, x0, y_seat + 0.05, x1, y_floor - 0.03, k.c(WALNUT["base"] if dx_ else WALNUT["dark"])))
    g = _g3(k, "stl", WALNUT, cx - w / 2, 0, cx + w / 2, 0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (cx - w / 2, y_seat, cx + w / 2, y_seat, cx + w / 2 - 0.02, y_seat + 0.10, cx - w / 2 + 0.02, y_seat + 0.10, k.c(WALNUT["base"]), k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="0.075" fill="%s" stroke="%s" stroke-width="0.022"/>' % (cx, y_seat, w / 2, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (cx - w * 0.30, y_seat - 0.01, cx, y_seat + 0.03, cx + w * 0.30, y_seat - 0.01, k.c(WALNUT["light"])))
    return "".join(o), (cx - w / 2 - 0.1, y_seat - 0.08, cx + w / 2 + 0.1, y_floor + 0.05)


def figure(cast_name, pose=None, uid="p"):
    if cast_name == "mule":
        return mule_figure(pose, uid)
    name = _variant(cast_name, pose)
    f = _O16["figure"](name, pose, uid)
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
    """walk / run / sneak / march cycles of cast6 for the people; for "mule": mode "walk" / "pull" / "idle" (see mule_cycle)."""
    if cast == "mule":
        return mule_cycle(phase, mode, facing, base)
    return cycle_people(cast, phase, mode, facing, base, arms, speed)


# ============================================================================= cast
_FLAGS = dict(C10._FLAGS, _cast16=True)


def _mk(base, **kw):
    d = dict(P.CAST[base])
    d.update(_FLAGS)
    d.update(kw)
    return d


MORSE_HAIR = dict(light="#b4a48e", base="#8c7a66", dark="#5c4c3e")
MORSE_YOUNG_HAIR = dict(light="#6a4e3c", base="#42301f", dark="#241810")
MORSE_COLORS = dict(base="#26335e", dark="#121a34", lapel="#1c2646", vest="#7a4a2a", vest_b="#d8c090", shirt="#fbfaf6", collar="#ffffff", tie="#16141a",
                    tie_dark="#08070a", button="#16141a", pants="#3a3430")


def _cast_table():
    T = {}
    T["morse16"] = _mk(
        "gentleman", seed=161.3, build="slim", torso_w=0.66, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.25, 0.50), arm=0.76,
        hip_x=0.15, leg=1.42, stance=0.06, wide=0.26, limb_w=0.056, eye_y=0.030, brow="stroke", brow_th=0.052, mouth="dash", moustache=False,
        cheeks="#e8a894", age_lines=True, collar16=True, whisker16=dict(style="long", color="#8c7a66", shade="#5c4c3e", y1=0.44, w=0.075, wmid=0.105),
        hat="newsboy", hat_style="mane16", hat_tilt=-2.0, hat_colors=dict(MORSE_HAIR), hair=dict(color="#8c7a66", front=0.06, grow=0.18),
        costume="frock7", coat_len=0.52, coat_flare=0.10, neck="cravat", chain=True, vest_buttons=4, double=False, flower=None,
        sleeve=dict(color="#26335e", dark="#121a34", cuff="#fbfaf6", len=0.84, w=0.150),
        shorts=dict(color="#3a3430", dark="#22201c", cuff="#3a3430", len=0.92, w=0.120),
        boots=dict(color="#1a161c", cuff="#1a161c", h=0.07, toe=0.15), colors=dict(MORSE_COLORS))
    T["morse16_young"] = dict(
        T["morse16"], seed=161.9, hat_colors=dict(MORSE_YOUNG_HAIR), hair=dict(color="#42301f", front=0.06, grow=0.18), mane_sweep=0.88, age_lines=False,
        whisker16=dict(style="long", color="#42301f", shade="#241810", y1=0.34, w=0.065, wmid=0.085), cheeks="#eeaa96",
        costume="smock7", smock_len=0.42, smock_flare=0.10, paint=True, pencil=False,
        sleeve=dict(color="#e8dec6", dark="#b8ac90", cuff="#fffaf0", len=0.84, w=0.160, roll=False),
        colors=dict(base="#e8dec6", smock="#e8dec6", dark="#b8ac90", collar="#fffaf0", button="#fffaf0", pants="#4a4036"))
    mk = dict(
        seed=61.5, build="stout", torso_w=1.64, torso_h=1.26, profile=C2.PROFILE_ROUND, shift_pow=1.25, shoulder=(0.50, 0.44), arm=0.80, hip_x=0.20, leg=1.24,
        stance=0.07, wide=0.32, limb_w=0.070, eye_y=0.000, brow="stroke", brow_th=0.085, mouth="frown", moustache=False, cheeks="#e8584a", chins=True,
        nose16="#e8806a", whisker16=dict(style="chops", color="#b8b2a8", shade="#7a766e", y1=0.30, w=0.17),
        hat="newsboy", hat_style="stovepipe16", hat_tilt=-3.0, hat_colors=dict(STOVE_COL), ear_pencil=False,
        hair=dict(color="#a8a298", front=0.0, grow=0.0),
        costume="tail16", neck="cravat", sleeve=dict(color="#1c1a22", dark="#0e0c12", cuff="#fbfaf6", len=0.84, w=0.215),
        shorts=dict(color="#4a4a54", dark="#2c2c34", cuff="#4a4a54", len=0.90, w=0.17), boots=dict(color="#16141a", cuff="#16141a", h=0.08, toe=0.18),
        colors=dict(base="#1c1a22", dark="#0e0c12", lapel="#34303c", vest="#d9a63a", plaid="#8a4a2a", plaid2="#f6e2a0", shirt="#fbfaf6", collar="#ffffff",
                    tie="#9c3a2a", tie_dark="#5a1a12", button="#1a1418", pants="#4a4a54", sash="#2f6a4a"))
    T["mocker"] = _mk("admiral", **mk)
    for k_ in ("epaulette10", "gloves10", "moustache_style", "tache_scale", "braid"):
        T["mocker"].pop(k_, None)
    T["mocker_bare"] = dict(T["mocker"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#a8a298", front=0.06, grow=0.20, style="fringe", top=-0.08))
    T["mocker_pm"] = dict(T["mocker"], sash16=True)
    T["mocker_pm_bare"] = dict(T["mocker_bare"], sash16=True)
    T["congressman_a"] = _mk(
        "gentleman", seed=162.1, build="slim", torso_w=0.62, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.24, 0.50), arm=0.76, hip_x=0.15,
        leg=1.36, stance=0.06, wide=0.26, limb_w=0.054, eye_y=0.030, brow="stroke", brow_th=0.046, mouth="dash", moustache=False, glasses=True, age_lines=True,
        cheeks="#e6a08c", hat_style="derby", hat_tilt=-5.0, hat_colors=dict(light="#6a5e56", base="#3c342e", dark="#1e1a16", shine="#a89c90", band="#14110e", brim="#2e2822", edge="#7a6e64"),
        hair=dict(color="#4a3a2e", front=0.07, grow=0.20), coat_len=0.46, neck="tie", chain=True,
        sleeve=dict(color="#47584c", dark="#2a3a30", cuff="#f6f2ea", len=0.84, w=0.145), shorts=dict(color="#6a645c", dark="#46423c", cuff="#6a645c", len=0.92, w=0.115),
        colors=dict(base="#47584c", dark="#243026", lapel="#344238", vest="#c8b078", vest_b="#7a5a2a", shirt="#fbfaf6", collar="#ffffff", tie="#7a2a2a", tie_dark="#4a1414",
                    button="#1a1a16", pants="#6a645c"))
    T["congressman_b"] = _mk(
        "gentleman", seed=162.8, build="regular", torso_w=1.00, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.34, 0.47), arm=0.74, hip_x=0.17,
        leg=1.10, stance=0.06, wide=0.28, limb_w=0.064, eye_y=0.010, brow="stroke", brow_th=0.066, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.9,
        glasses=False, age_lines=True, cheeks="#ec8c7a", hat_style="bare7", hat_tilt=0.0, hat_colors=dict(light="#f6f3ee", base="#e8e4de", dark="#b8b4ae", shine="#ffffff"),
        hair=dict(color="#f0ece6", front=0.17, grow=0.30, style="cap", shine="#ffffff"),
        whisker16=dict(style="long", color="#f0ece6", shade="#b8b4ae", y1=0.36, w=0.075, wmid=0.10), coat_len=0.44, neck="tie", chain=True, vest_buttons=5,
        sleeve=dict(color="#6a4a36", dark="#3e2a1c", cuff="#f6f2ea", len=0.84, w=0.170), shorts=dict(color="#5a504a", dark="#38322e", cuff="#5a504a", len=0.90, w=0.13),
        colors=dict(base="#6a4a36", dark="#3a261a", lapel="#563a2a", vest="#9c3a2a", vest_b="#e8d8a0", shirt="#fbfaf6", collar="#ffffff", tie="#1a2a46", tie_dark="#0e1a30",
                    button="#2a1a12", pants="#5a504a", moustache="#e8e4de", moustache_l="#b8b4ae"))
    T["congressman_c"] = _mk(
        "gentleman", seed=163.4, build="slim", torso_w=0.64, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15,
        leg=1.30, stance=0.06, wide=0.26, limb_w=0.054, eye_y=0.040, brow="dome", brow_th=0.040, mouth="smirk", moustache=False, pencil_moustache=True, glasses=False,
        age_lines=False, cheeks="#f2a896", hat_style="tophat7", hat_tilt=9.0, hat_colors=dict(light="#d8d0c0", base="#a8a090", dark="#6a6458", shine="#fffaf0", band="#7a2e3a", brim="#8a8272"),
        hair=dict(color="#5a3a26", front=0.09, grow=0.22, style="curl"), coat_len=0.40, neck="cravat", chain=False, flower="#f0e6c8", vest_buttons=4, double=True,
        sleeve=dict(color="#7a2e3a", dark="#4a1a22", cuff="#fbfaf6", len=0.84, w=0.140), shorts=dict(color="#d8cfae", dark="#a89e80", cuff="#d8cfae", len=0.92, w=0.11),
        colors=dict(base="#7a2e3a", dark="#3e1219", lapel="#5e1e2a", vest="#e8d8a8", vest_b="#7a5a2a", shirt="#fbfaf6", collar="#ffffff", tie="#e0c060", tie_dark="#a88a30",
                    button="#e2b442", pants="#d8cfae"))
    T["messenger"] = _mk(
        "newsboy", seed=164.2, hat_style="flatnews", hat_tilt=-10.0, hat_colors=dict(light="#8a6e52", base="#5e4632", dark="#38281c", shine="#b49478", visor="#3e2c1e"),
        hair=dict(color="#6a4020", front=0.08, grow=0.16), cheeks="#f4a090", freckles=True,
        sleeve=dict(color="#3e5a4a", dark="#24382c", cuff="#4e6a5a", len=0.62, w=0.14, roll=True),
        colors=dict(base="#3e5a4a", dark="#24382c", lapel="#34503f", pocket="#36503f", button="#e2b442", shirt="#efe6d2", susp="#4a3a2a", susp_b="#c9a44a", pants="#4a4038",
                    scarf="#e8d8b0", scarf_d="#b8a47e", scarf_s="#9c3a2a"),
        shorts=dict(color="#4a4038", dark="#2e2822", cuff="#4a4038", len=0.55, w=0.13))
    brace = dict(braces="1")
    T["cornell"] = _mk(
        "foreman", seed=165.5, build="regular", torso_w=0.92, torso_h=1.02, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.33, 0.47), arm=0.76, hip_x=0.16, leg=1.24,
        stance=0.06, wide=0.27, limb_w=0.062, eye_y=0.010, brow="stroke", brow_th=0.062, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.9, smirk_side=1,
        cheeks="#e8907c", cigar_ok=False, hat_style="slouch16", hat_tilt=-4.0, hat_colors=dict(FELT, shine="#e0c8a0"), hair=dict(color="#5a4030", front=0.07, grow=0.20),
        costume="braces16", dirt16=True,
        sleeve=dict(color="#e8dcc0", dark="#b8aa8a", cuff="#e8dcc0", len=0.46, w=0.165, roll=True), shorts=dict(color="#5a5048", dark="#38322c", cuff="#5a5048", len=0.92, w=0.14),
        boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.14, toe=0.17),
        colors=dict(base="#e8dcc0", dark="#b8aa8a", collar="#e8dcc0", button="#f6f0e0", brace="#6a3a22", brace_l="#9a6a42", belt="#3a2a20", pants="#5a5048", moustache="#5a4030", moustache_l="#8a6a4a"))
    T["cornell_bare"] = dict(T["cornell"], hat_style="bare7", hat_tilt=0.0, hair=dict(color="#5a4030", front=0.12, grow=0.24, style="cap", shine="#8a6a4a"))
    T["worker16_a"] = _mk(
        "worker1", seed=166.1, build="regular", torso_w=0.90, torso_h=1.00, profile=CE.PROFILE_PEAR, shift_pow=1.05, shoulder=(0.32, 0.47), arm=0.74, hip_x=0.16, leg=1.20,
        stance=0.07, wide=0.28, limb_w=0.062, eye_y=0.020, brow="stroke", brow_th=0.058, mouth="dash", moustache=False, cheeks="#e89480", hat_style="flatnews", hat_tilt=-3.0,
        cap_puff=0.8, hat_colors=dict(light="#9a8a6a", base="#74644a", dark="#4a3e2c", shine="#bcae8e", visor="#4a3e2c"), hair=dict(color="#4a3020", front=0.08, grow=0.22),
        costume="braces16", dirt16=True, sleeve=dict(color="#b03a2e", dark="#6a1e16", cuff="#b03a2e", len=0.48, w=0.155, roll=True),
        shorts=dict(color="#6a5e4e", dark="#3e362c", cuff="#6a5e4e", len=0.92, w=0.14), boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.10, toe=0.16),
        colors=dict(base="#b03a2e", dark="#6a1e16", collar="#b03a2e", plaid="#5a1a14", button="#efe6d2", brace="#2a2a30", brace_l="#5a5a64", belt="#2a1e16", pants="#6a5e4e"))
    T["worker16_b"] = _mk(
        "worker1", seed=166.8, build="slim", torso_w=0.64, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15, leg=1.38,
        stance=0.06, wide=0.26, limb_w=0.056, eye_y=0.040, brow="stroke", brow_th=0.050, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.7, cheeks="#eaa08a",
        hat_style="strawhat", hat_tilt=-6.0, hat_colors=dict(light="#f0d890", base="#d8b866", dark="#a08440", shine="#fff0b8", band="#9c3a2a"), hair=dict(color="#7a5a3a", front=0.08, grow=0.22),
        costume="braces16", dirt16=True, sleeve=dict(color="#8a9aa8", dark="#5a6a78", cuff="#8a9aa8", len=0.46, w=0.14, roll=True),
        shorts=dict(color="#7a7060", dark="#4a443a", cuff="#7a7060", len=0.92, w=0.12), boots=dict(color="#3a2a20", cuff="#3a2a20", h=0.10, toe=0.15),
        colors=dict(base="#8a9aa8", dark="#5a6a78", collar="#8a9aa8", button="#efe6d2", brace="#a8844c", brace_l="#d8b878", belt="#3a2a20", pants="#7a7060", moustache="#7a5a3a", moustache_l="#a8845a"))
    T["clerk16"] = _mk(
        "clerk", seed=167.3, torso_w=0.54, leg=1.30, hat_style="eyeshade", hat_colors=dict(band="#2f2a36", visor="#2f6a4a", visor_l="#9fd8b0"),
        hair=dict(color="#3a2a22", front=0.085, grow=0.22, style="cap", shine="#6a4a38"), cheeks="#eaa090",
        colors=dict(base="#f2ead8", dark="#a89c84", stripe="#d8ccb0", collar="#fffaf0", tie="#16141a", tie_dark="#08070a", clip="#e2b442", pocket="#e4dac4", pencil1="#efc13a",
                    pencil2="#9c3a2a", button="#fbfbfb", belt="#4a3220", buckle="#e2b442", pants="#4a3e36", garter="#9c3a2a"))
    return T


CANVAS16 = {
    "morse16": (-1.8125, -3.8750, 1.8125, 0.1250),
    "mocker": (-1.5625, -4.4375, 1.5625, 0.1250),
    "congressman_a": (-1.2500, -3.6250, 1.2500, 0.1250),
    "congressman_b": (-1.2500, -3.0625, 1.2500, 0.1250),
    "congressman_c": (-1.2500, -3.9375, 1.2500, 0.1250),
    "messenger": (-1.1875, -2.7500, 1.1875, 0.1250),
    "clerk16": (-1.3125, -3.2500, 1.3125, 0.1250),
    "cornell": (-2.3750, -3.5625, 2.3750, 0.1250),
    "worker16_a": (-2.0625, -3.3750, 2.0625, 0.3750),
    "worker16_b": (-2.0625, -4.3125, 2.0625, 0.1875),
    "mule": (-3.1875, -4.1250, 3.1875, 0.1250),
}
# the long-pole poses (carry / raise a pole) need taller or wider cards: pass these to Actor.build for those poses
CANVAS16_POLE = {"morse16": (-1.5625, -5.5625, 1.5625, 0.1250), "worker16_a": (-2.8750, -6.3125, 2.8750, 0.1250), "worker16_b": (-2.8750, -6.5625, 2.8750, 0.1250)}
# the mule between buggy shafts (harness=2): the shaft end sticks out behind
CANVAS16_BUGGY = {"mule": (-3.1250, -4.1250, 3.1875, 0.1250)}


# ============================================================================= the mule (side view, faces screen-right; mirror=True for left)
# Frame: x right, y DOWN, D units.  Origin = the head centre of the neutral pose; the hooves stand on y = MULE_G; the body extends to -x.
MULE_G = 3.00
MULE_COL = dict(light="#b49478", base="#8a6a52", dark="#5a4234")
MULE_FAR = dict(light="#8a6c54", base="#6a5040", dark="#44322a")
MULE_MUZZLE = dict(light="#e8d8bc", base="#cdb898", dark="#9a8468")
MULE_MANE = "#3a2a22"
HOOF = "#2a2024"
HARN = dict(light="#9a6238", base="#6a3e22", dark="#3a2010")
_FRONT_S, _HIND_S = (-1.50, 1.28), (-3.00, 1.28)
_FRONT_L, _HIND_L = (0.95, 0.75), (1.00, 0.80)
_GAIT = dict(hn=0.0, fn=0.25, hf=0.50, ff=0.75)        # lateral-sequence walk: hind near, fore near, hind far, fore far


def _smoothstep(v):
    v = max(0.0, min(1.0, v))
    return v * v * (3 - 2 * v)


def _foot(u, S, lift_h, stance=0.62):
    """foot offset (dx, lift) for gait phase u in 0..1: the stance sweeps back at constant speed, the swing carries it forward."""
    u = u % 1.0
    if u < stance:
        return S * (1 - 2 * u / stance), 0.0
    v = (u - stance) / (1 - stance)
    return -S + 2 * S * _smoothstep(v), lift_h * math.sin(math.pi * v) ** 0.8


def _ik(S, F, L1, L2, kdir):
    dx, dy = F[0] - S[0], F[1] - S[1]
    d = math.hypot(dx, dy)
    d = max(abs(L1 - L2) + 1e-3, min(L1 + L2 - 1e-3, d))
    ux, uy = dx / (math.hypot(dx, dy) or 1.0), dy / (math.hypot(dx, dy) or 1.0)
    a = (L1 * L1 - L2 * L2 + d * d) / (2 * d)
    h = math.sqrt(max(L1 * L1 - a * a, 0.0))
    nx, ny = -uy, ux
    if nx * kdir < 0:
        nx, ny = -nx, -ny
    return (S[0] + ux * a + nx * h, S[1] + uy * a + ny * h), (S[0] + ux * d, S[1] + uy * d)


def _mule_leg(k, S, F, L1, L2, kdir, w1, w2, col, hoofang, hind):
    """one leg: ink pass + colour pass; returns (ink svg, colour svg, knee, fetlock)."""
    K, F2 = _ik(S, F, L1, L2, kdir)
    ink = ('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (S + K + F2 + (k.ink, 0)))
    ink = ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
           % (S[0], S[1], K[0], K[1], k.ink, w1 + 0.05, K[0], K[1], F2[0], F2[1], k.ink, w2 + 0.05))
    cs = ('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
          % (S[0], S[1], K[0], K[1], k.c(col["base"]), w1, K[0], K[1], F2[0], F2[1], k.c(col["base"]), w2))
    cs += '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (K[0], K[1], (w1 + w2) / 4, k.c(col["base"]))
    cs += '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.5"/>' % (S[0] - 0.05, S[1] + 0.05, K[0] - 0.04 * (1 if not hind else -1), K[1], k.c(col["light"]))
    # hoof
    c, sn = math.cos(math.radians(hoofang)), math.sin(math.radians(hoofang))

    def R(x, y):
        return (F2[0] + x * c - y * sn, F2[1] + x * sn + y * c)
    hp = [R(-0.075, 0.0), R(0.075, 0.0), R(0.105, 0.145), R(-0.095, 0.145)]
    cs += '<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (_poly_d(hp), k.c(HOOF), k.ink)
    k.ext.extend([(p[0], p[1], 0.03) for p in hp])
    k.ext.extend([(S[0] - w1, S[1], 0.03), (K[0], K[1], w1 / 2)])
    return ink, cs, K, F2, R(0.0, 0.145)


def _mule_head(k, ex, ear, bray, expr, gaze, harness):
    """the head in its own frame (poll pivot at (-0.30, 0.05)): skull, long muzzle, ring eye, nostril, mouth, bridle; returns (svg, ears_near, ears_far)."""
    g = _lin(k, "mhd", MULE_COL["light"], MULE_COL["base"], MULE_COL["dark"], 0, -0.25, 0, 0.60)
    hp = [(-0.42, -0.10), (-0.30, -0.22), (-0.02, -0.21), (0.30, -0.02), (0.55, 0.16), (0.69, 0.30), (0.72, 0.47), (0.62, 0.60), (0.36, 0.58), (0.08, 0.46), (-0.14, 0.42),
          (-0.34, 0.30), (-0.46, 0.10)]
    o = []
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (P._smooth_closed(hp), g, k.ink))
    mz = [(0.40, 0.14), (0.60, 0.22), (0.73, 0.34), (0.74, 0.48), (0.64, 0.62), (0.40, 0.60), (0.34, 0.40)]
    o.append('<path d="%s" fill="%s" opacity="0.95"/>' % (P._smooth_closed(mz), k.c(MULE_MUZZLE["base"])))
    o.append('<path d="M0.66,0.58 Q0.74,0.52 0.73,0.40" fill="none" stroke="%s" stroke-width="0.028" stroke-linecap="round" stroke-linejoin="round"/>' % k.ink)
    o.append('<path d="M-0.30,-0.15 Q-0.05,-0.19 0.20,-0.05" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.35"/>')
    # nostril + mouth
    o.append('<ellipse cx="0.64" cy="0.33" rx="0.030" ry="0.042" transform="rotate(-20 0.64 0.33)" fill="%s"/>' % k.ink)
    if bray > 0.5:
        o.append('<path d="M0.70,0.50 L0.40,0.50 Q0.38,0.66 0.50,0.76 Q0.66,0.74 0.72,0.62" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (k.c("#5a2430"), k.ink))
        o.append('<path d="M0.69,0.51 L0.60,0.51 M0.56,0.51 L0.46,0.51" stroke="#fffaf0" stroke-width="0.050" stroke-linecap="round"/>')
        o.append('<path d="M0.64,0.60 Q0.56,0.70 0.48,0.68" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round" opacity="0.8"/>' % k.c("#d8707a"))
    else:
        o.append('<path d="M0.70,0.50 Q0.55,0.54 0.38,0.48" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % k.ink)
    # eye
    ex_, ey_ = 0.08, 0.02
    if expr in ("blink", "sleepy"):
        o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (ex_ - 0.075, ey_, ex_, ey_ + 0.045, ex_ + 0.075, ey_, k.ink))
    elif expr == "strain":
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round" stroke-linejoin="round"/>' % (ex_ - 0.07, ey_ - 0.05, ex_ + 0.05, ey_ + 0.01, ex_ - 0.07, ey_ + 0.06, k.ink))
        o.append('<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.038" stroke-linecap="round"/>' % (ex_ - 0.10, ey_ - 0.13, ex_ + 0.10, ey_ - 0.07, k.ink))
    elif expr == "happy":
        o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (ex_ - 0.075, ey_ + 0.03, ex_, ey_ - 0.05, ex_ + 0.075, ey_ + 0.03, k.ink))
    else:
        r = 0.095 if expr != "surprised" else 0.115
        o.append('<ellipse cx="%.3f" cy="%.3f" rx="%.3f" ry="%.3f" fill="#fffaf2" stroke="%s" stroke-width="0.022"/>' % (ex_, ey_, r, r * 0.86, k.ink))
        o.append('<circle cx="%.3f" cy="%.3f" r="0.052" fill="%s"/><circle cx="%.3f" cy="%.3f" r="0.015" fill="#ffffff"/>' % (ex_ + 0.03 * gaze[0], ey_ + 0.025 * gaze[1], k.ink, ex_ + 0.020 + 0.03 * gaze[0], ey_ - 0.016 + 0.025 * gaze[1]))
        if expr != "surprised":
            o.append('<path d="M%.3f,%.3f Q%.3f,%.3f %.3f,%.3f L%.3f,%.3f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                     % (ex_ - r - 0.01, ey_ - 0.01, ex_, ey_ - r * 1.15, ex_ + r + 0.01, ey_ - 0.01, ex_ + r + 0.01, ey_ - 0.03, k.c(MULE_COL["base"]), k.ink))
    o.append('<path d="M-0.40,0.30 Q-0.30,0.40 -0.14,0.40" fill="none" stroke="%s" stroke-width="0.010" opacity="0.5"/>' % k.c(MULE_COL["dark"]))
    # forelock
    o.append('<path d="M-0.28,-0.20 Q-0.14,-0.34 -0.02,-0.18 Q-0.10,-0.22 -0.12,-0.12 Q-0.20,-0.16 -0.28,-0.20 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c(MULE_MANE), k.ink))
    if harness:
        # bridle: cheek strap, brow band, nose band, throat latch; bit ring at the mouth corner
        hc = k.c(HARN["base"])
        o.append('<path d="M-0.20,-0.18 L0.12,0.22 M-0.28,-0.12 L-0.20,0.40" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M-0.20,-0.18 L0.12,0.22 M-0.28,-0.12 L-0.20,0.40" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (k.ink, hc))
        o.append('<path d="M0.26,0.10 Q0.54,0.28 0.58,0.42 M0.12,0.22 L0.40,0.50" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/><path d="M0.26,0.10 Q0.54,0.28 0.58,0.42 M0.12,0.22 L0.40,0.50" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (k.ink, hc))
        o.append('<circle cx="0.40" cy="0.50" r="0.046" fill="none" stroke="%s" stroke-width="0.040"/><circle cx="0.40" cy="0.50" r="0.046" fill="none" stroke="%s" stroke-width="0.016"/>' % (k.ink, k.c(BRASS["base"])))
        o.append('<circle cx="0.12" cy="0.22" r="0.022" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(BRASS["base"]), k.ink))
    # ears (base near the poll)
    def ear_shape(bx, by, ang, ln, wd, inner, col):
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))

        def R(x, y):
            return (bx + x * c - y * s, by + x * s + y * c)
        pts = [R(0, -wd * 0.5), R(ln * 0.45, -wd * 0.62), R(ln, -wd * 0.10), R(ln * 1.0, wd * 0.10), R(ln * 0.45, wd * 0.58), R(0, wd * 0.5)]
        d = P._smooth_closed(pts)
        r = '<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)
        if inner:
            ip = [R(ln * 0.12, -wd * 0.2), R(ln * 0.5, -wd * 0.32), R(ln * 0.88, -wd * 0.04), R(ln * 0.5, wd * 0.30), R(ln * 0.12, wd * 0.2)]
            r += '<path d="%s" fill="%s" opacity="0.9"/>' % (P._smooth_closed(ip), k.c("#d8a090"))
        for p in pts:
            k.ext.append((p[0], p[1], 0.03))
        return r
    base_ang = -100.0 + 38.0 * ear                # ear > 0: forward, ear < 0: pinned back
    near = ear_shape(-0.26, -0.16, base_ang + 6, 0.80, 0.20, True, MULE_COL["base"])
    far = ear_shape(-0.32, -0.15, base_ang - 14, 0.78, 0.19, False, MULE_FAR["base"])
    for p in hp:
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o), near, far


def _mule_tail(k, swing, droop=0.0):
    """a mule tail: a short dock from the rump with a long hanging tuft; swing -1..1 swings it back / forward."""
    ox, oy = -3.34, 0.66
    a = math.radians(96 + 26 * swing - 20 * droop)
    ln = 1.55
    tx, ty = ox + ln * math.cos(a), oy + ln * math.sin(a)
    mx, my = ox + ln * 0.55 * math.cos(a - 0.10 * swing), oy + ln * 0.55 * math.sin(a - 0.10 * swing)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (ox, oy, mx, my, tx, ty)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.130" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.090" stroke-linecap="round"/>' % (d, k.ink, d, k.c(MULE_MANE))]
    # the tuft
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    tuft = [(mx + nx * 0.07, my + ny * 0.07), (tx + nx * 0.17 + ux * 0.04, ty + ny * 0.17 + uy * 0.04), (tx + ux * 0.22, ty + uy * 0.22), (tx - nx * 0.17 + ux * 0.04, ty - ny * 0.17 + uy * 0.04),
            (mx - nx * 0.07, my - ny * 0.07)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(tuft), k.c(MULE_MANE), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.6"/>' % (mx + nx * 0.03, my + ny * 0.03, tx + ux * 0.14 + nx * 0.05, ty + uy * 0.14 + ny * 0.05,
                                                                                                                      mx - nx * 0.03, my - ny * 0.03, tx + ux * 0.14 - nx * 0.05, ty + uy * 0.14 - ny * 0.05, k.c("#8a7a70")))
    k.ext.extend([(tx + ux * 0.24, ty + uy * 0.24, 0.04), (tx + nx * 0.18, ty + ny * 0.18, 0.04), (tx - nx * 0.18, ty - ny * 0.18, 0.04)])
    return "".join(o), (tx + ux * 0.22, ty + uy * 0.22)


def mule_figure(pose=None, uid="m"):
    """the mule, a side-view puppet.  pose keys (all optional): phase 0..1 (gait), stride 0..1.2 (0 = standing), lift 0..1.5, bob (D), head_pitch (deg, + = nose down),
    head_dy (D), ear -1 (pinned back) .. +1 (forward), tail -1..1, droop 0..1 (tail down), strain 0..1 (leaning into the collar), expr (neutral / strain / blink / sleepy / happy /
    surprised), bray 0/1 (mouth open), gaze (gx, gy), harness 0 none / 1 plough (collar, hames, back band, belly girth, breeching, traces) / 2 buggy (as 1 with shafts),
    rest 0..1 (idle: one hind leg cocked), mirror, tint, ink.  Returns the figure dict (svg, feet_y, bbox, anchors); anchors: head, head_top, hat_top, mouth, eye_r, eye_l,
    withers, hip, chest, feet, foot_r / foot_l (the near / far fore hoof), hoof_fn / hoof_ff / hoof_hn / hoof_hf, tail_tip, trace_end, shaft_end, collar."""
    pose = pose if isinstance(pose, dict) else {}
    g = pose.get
    tint = g("tint")
    ink = g("ink") if P._is_hex(g("ink") or "") else P.INK
    k = P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if isinstance(tint, str) and P._is_hex(tint) else None)
    ph = _num(g("phase"), 0.0) % 1.0
    strain = _f(g("strain"), 0.0, 0.0, 1.0)
    stride = _f(g("stride"), 0.0, 0.0, 1.2) * (1.0 - 0.35 * strain)
    lift = _f(g("lift"), 1.0, 0.0, 1.5)
    by = _f(g("bob"), 0.0, -0.2, 0.2) + 0.05 * strain
    pitch = _f(g("head_pitch"), 0.0, -40, 50) + 16.0 * strain
    hdy = _f(g("head_dy"), 0.0, -0.6, 0.8) + 0.18 * strain
    ear = _f(g("ear"), 0.0, -1.0, 1.0) - 0.5 * strain
    tail = _f(g("tail"), 0.0, -1.0, 1.0)
    droop = _f(g("droop"), 0.0, 0.0, 1.0)
    expr = g("expr") if g("expr") in ("neutral", "strain", "blink", "sleepy", "happy", "surprised") else ("strain" if strain > 0.6 else "neutral")
    bray = 1.0 if _f(g("bray"), 0.0, 0.0, 1.0) > 0.5 else 0.0
    gz = g("gaze")
    gaze = (_num(gz[0]), _num(gz[1])) if isinstance(gz, (tuple, list)) and len(gz) >= 2 else (_num(gz), 0.0)
    harness = int(_f(g("harness"), 0, 0, 2))
    rest = _f(g("rest"), 0.0, 0.0, 1.0)
    mir = bool(g("mirror"))
    G = MULE_G
    # ---- legs
    legs = {}
    for nm, (S0, Ls, kd, w1, w2, hind) in (("fn", (_FRONT_S, _FRONT_L, 1.0, 0.25, 0.13, False)), ("ff", (_FRONT_S, _FRONT_L, 1.0, 0.25, 0.13, False)),
                                           ("hn", (_HIND_S, _HIND_L, -1.0, 0.32, 0.14, True)), ("hf", (_HIND_S, _HIND_L, -1.0, 0.32, 0.14, True))):
        u = ph + _GAIT[nm]
        dx, lf = _foot(u, 0.62 * stride, 0.42 * lift * min(1.0, stride * 2.0)) if stride > 0.01 else (0.0, 0.0)
        if stride <= 0.01 and hind and nm == "hf" and rest > 0:
            lf = 0.16 * rest
            dx = -0.12 * rest
        if nm in ("ff", "hf"):
            dx += 0.10 if not hind else -0.06                       # the far legs stand a little apart from the near ones
        S = (S0[0] + (0.0 if nm in ("fn", "hn") else 0.0), S0[1] + by)
        fx = S0[0] + (0.14 if not hind else -0.10) + dx
        F = (fx, G - 0.145 - lf)
        ang = (-38.0 * (lf / 0.42) if lf > 0.01 else 0.0) * (1 if not hind else -1)
        if hind and lf > 0.01:
            ang = 40.0 * (lf / 0.42)
        legs[nm] = _mule_leg(k, S, F, Ls[0], Ls[1], kd, w1, w2, MULE_FAR if nm in ("ff", "hf") else MULE_COL, ang, hind)
    o = []
    for nm in ("hf", "ff"):
        o.append(legs[nm][0] + legs[nm][1])
    # ---- shafts (far) / tail
    tsvg, ttip = _mule_tail(k, tail, droop)
    o.append(tsvg)
    # ---- body + neck
    pts = [(-0.38, -0.10 + hdy * 0.0), (-0.70, 0.10), (-1.20, 0.38), (-1.80, 0.50), (-2.50, 0.50), (-3.05, 0.50), (-3.40, 0.72), (-3.52, 1.10), (-3.45, 1.55), (-3.15, 1.92), (-2.80, 1.84),
           (-2.20, 1.90), (-1.65, 1.93), (-1.28, 1.86), (-0.92, 1.62), (-0.74, 1.25), (-0.58, 0.88), (-0.30, 0.56), (-0.05, 0.40)]
    pts = [(x, y + by) for (x, y) in pts]
    gb = _lin(k, "mby", MULE_COL["light"], MULE_COL["base"], MULE_COL["dark"], 0, 0.3 + by, 0, 2.0 + by)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (P._smooth_closed(pts), gb, k.ink))
    # belly highlight, shoulder and haunch lines
    o.append('<path d="M-1.30,%.3f Q-2.20,%.3f -3.10,%.3f" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round" opacity="0.5"/>' % (1.78 + by, 1.86 + by, 1.70 + by, k.c(MULE_MUZZLE["base"])))
    o.append('<path d="M-1.50,%.3f Q-1.30,%.3f -1.38,%.3f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>' % (0.80 + by, 1.18 + by, 1.54 + by, k.c(MULE_COL["dark"])))
    o.append('<path d="M-3.00,%.3f Q-2.70,%.3f -2.95,%.3f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.6"/>' % (0.80 + by, 1.20 + by, 1.70 + by, k.c(MULE_COL["dark"])))
    o.append('<path d="M-2.40,%.3f Q-1.80,%.3f -1.40,%.3f" fill="none" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.25"/>' % (0.62 + by, 0.58 + by, 0.66 + by))
    # mane (short bristles along the neck)
    mane = []
    for i in range(9):
        t = i / 8.0
        x = -0.50 - 0.80 * t
        y = 0.08 + 0.33 * t + by
        mane.append("M%.4f,%.4f L%.4f,%.4f" % (x, y, x + 0.03, y - 0.15 - 0.03 * (i % 2)))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.050" stroke-linecap="round"/>' % ("".join(mane), k.c(MULE_MANE)))
    # ---- harness parts behind the near legs: traces (plough) or shafts (buggy)
    shaft_end = None
    trace_end = None
    hb, hd = k.c(HARN["base"]), k.c(HARN["dark"])

    def strap(d, w=0.07):
        return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round"/><path d="%s" fill="none" stroke="%s" stroke-width="%.3f" stroke-linecap="round" stroke-linejoin="round"/>'
                % (d, k.ink, w + 0.03, d, hb, w))
    if harness:
        hx, hy = -1.00, 1.06 + by
        if harness == 1:
            # traces: from the hames back along the flank to the trace end
            trace_end = (-4.15, 1.38 + by + 0.05 * strain)
            d = "M%.3f,%.3f Q-2.40,%.3f %.3f,%.3f" % (hx, hy, 1.22 + by, trace_end[0], trace_end[1])
            o.append(strap(d, 0.06))
            o.append('<circle cx="%.3f" cy="%.3f" r="0.050" fill="none" stroke="%s" stroke-width="0.050"/><circle cx="%.3f" cy="%.3f" r="0.050" fill="none" stroke="%s" stroke-width="0.024"/>' % (trace_end[0], trace_end[1], k.ink, trace_end[0], trace_end[1], k.c(IRON["light"])))
            k.ext.append((trace_end[0] - 0.08, trace_end[1], 0.03))
        else:
            shaft_end = (-5.10, 1.66 + by)
            sd = "M-0.84,%.3f L%.3f,%.3f" % (1.12 + by, shaft_end[0], shaft_end[1])
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.130" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.090" stroke-linecap="round"/><path d="M-1.0,%.3f L-4.6,%.3f" stroke="#ffffff" stroke-width="0.010" opacity="0.3"/>'
                     % (sd, k.ink, sd, k.c(WALNUT["base"]), 1.08 + by, 1.58 + by))
            o.append(strap("M-1.60,%.3f L-1.60,%.3f" % (1.22 + by, 1.52 + by), 0.06))                                               # shaft loop
            o.append(strap("M-2.40,%.3f L-2.40,%.3f" % (1.34 + by, 1.64 + by), 0.06))
            k.ext.append((shaft_end[0] - 0.08, shaft_end[1] + 0.07, 0.03))

    # ---- near legs
    for nm in ("hn", "fn"):
        o.append(legs[nm][0] + legs[nm][1])
    # ---- harness
    an = {}
    if harness:
        o.append(strap("M-1.95,%.3f Q-1.88,%.3f -2.02,%.3f" % (0.46 + by, 1.20 + by, 1.90 + by)))                                    # girth
        o.append('<rect x="-2.18" y="%.3f" width="0.34" height="0.12" rx="0.05" fill="%s" stroke="%s" stroke-width="0.022"/>' % (0.40 + by, k.c(BRICK["base"]), k.ink))       # saddle pad
        o.append('<circle cx="-2.02" cy="%.3f" r="0.075" fill="none" stroke="%s" stroke-width="0.060"/><circle cx="-2.02" cy="%.3f" r="0.075" fill="none" stroke="%s" stroke-width="0.030"/>' % (0.32 + by, k.ink, 0.32 + by, k.c(BRASS["base"])))
        o.append(strap("M-3.20,%.3f Q-3.42,%.3f -3.18,%.3f" % (0.62 + by, 1.20 + by, 1.78 + by), 0.085))                              # breeching round the haunch
        o.append(strap("M-2.60,%.3f Q-2.90,%.3f -3.20,%.3f" % (0.50 + by, 0.55 + by, 0.62 + by), 0.05))
        # collar: a thick padded ring round the base of the neck, brick-red pad, hames with brass knobs
        col_pts = [(-0.80, 0.80), (-0.98, 0.50), (-1.20, 0.42), (-1.30, 0.62), (-1.22, 1.12), (-1.02, 1.52), (-0.84, 1.40)]
        col_pts = [(x, y + by) for (x, y) in col_pts]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (P._smooth_closed(col_pts), k.c(BRICK["base"]), k.ink))
        cin = [(-0.88, 0.84), (-1.00, 0.60), (-1.16, 0.54), (-1.22, 0.70), (-1.14, 1.10), (-1.0, 1.38), (-0.90, 1.30)]
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" opacity="0.8"/>' % (P._smooth_closed([(x, y + by) for (x, y) in cin]), k.c(BRICK["light"])))
        o.append('<path d="M-1.10,%.3f L-0.94,%.3f" stroke="%s" stroke-width="0.080" stroke-linecap="round"/><path d="M-1.10,%.3f L-0.94,%.3f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>'
                 % (0.30 + by, 1.54 + by, k.ink, 0.30 + by, 1.54 + by, k.c(BRASS["base"])))
        o.append('<circle cx="-1.12" cy="%.3f" r="0.050" fill="%s" stroke="%s" stroke-width="0.012"/><circle cx="-0.95" cy="%.3f" r="0.040" fill="%s" stroke="%s" stroke-width="0.012"/>' % (0.28 + by, k.c(BRASS["light"]), k.ink, 1.58 + by, k.c(BRASS["base"]), k.ink))
        # reins from the bit back to the saddle ring (buggy)
    # ---- head (rotated about the poll pivot), ears
    px_, py_ = -0.30, 0.05 + by
    hsvg, near, far = _mule_head(k, 0, ear, bray, expr, gaze, harness)
    o.append('<g transform="translate(0 %.4f) rotate(%.3f %.4f %.4f)">%s%s%s</g>' % (hdy, pitch, px_, 0.05 - 0.0, far, "", ""))
    o.append('<g transform="translate(0 %.4f) rotate(%.3f %.4f %.4f)">%s%s</g>' % (hdy, pitch, px_, 0.05, hsvg, near))
    # reins
    if harness == 2:
        mx_, my_ = _rot_pt(0.40, 0.50, pitch, px_, 0.05, hdy)
        d = "M%.3f,%.3f Q-1.2,%.3f -2.02,%.3f" % (mx_, my_, 0.62 + by, 0.32 + by)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/><path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (d, k.ink, d, hb))
    # anchors
    def hp(x, y):
        return _rot_pt(x, y, pitch, px_, 0.05, hdy)
    an["head"] = hp(0.0, 0.0)
    an["head_top"] = hp(-0.05, -0.21)
    an["hat_top"] = hp(-0.40, -0.98)
    an["mouth"] = hp(0.55, 0.50)
    an["eye_r"] = hp(0.08, 0.02)
    an["eye_l"] = hp(0.08, 0.02)
    an["withers"] = (-1.25, 0.40 + by)
    an["hip"] = (-2.30, 0.95 + by)
    an["chest"] = (-0.90, 1.30 + by)
    an["collar"] = (-1.05, 0.95 + by)
    an["tail_tip"] = ttip
    for nm in ("fn", "ff", "hn", "hf"):
        an["hoof_" + nm] = (legs[nm][4][0], G if legs[nm][4][1] > G - 0.02 else legs[nm][4][1])
    an["foot_r"], an["foot_l"] = an["hoof_fn"], an["hoof_ff"]
    xs = [legs[nm][3][0] for nm in ("fn", "hn", "ff", "hf")]
    an["feet"] = (sum(xs) / 4.0, G)
    if trace_end:
        an["trace_end"] = trace_end
    if shaft_end:
        an["shaft_end"] = shaft_end
    ext = k.ext
    x0 = min(e[0] - e[2] for e in ext)
    x1 = max(e[0] + e[2] for e in ext)
    y0 = min(e[1] - e[2] for e in ext)
    y1 = max(e[1] + e[2] for e in ext)
    # the head and ears also count
    for p in [hp(-0.46, -1.0), hp(0.75, 0.65), hp(-0.46, -0.1), hp(0.75, 0.3)]:
        x0, x1, y0, y1 = min(x0, p[0]), max(x1, p[0]), min(y0, p[1]), max(y1, p[1])
    y1 = max(y1, G + 0.02)
    bb = (x0, y0, x1, y1)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    svg = '<g id="%s_fig">%s%s</g>' % (k.uid, defs, "".join(o))
    if mir:
        svg = '<g id="%s_fig" transform="scale(-1 1)">%s%s</g>' % (k.uid, defs, "".join(o))
        an = {n: (-p[0], p[1]) for n, p in an.items()}
        an["foot_r"], an["foot_l"] = an["foot_l"], an["foot_r"]
        bb = (-x1, y0, -x0, y1)
    return dict(svg=svg, feet_y=G, bbox=bb, anchors=an)


def _rot_pt(x, y, ang, cx, cy, dy):
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    return (cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c + dy)


def mule_cycle(phase, mode="walk", facing=1, base=None):
    """one frame of the mule: mode "walk" (about 36 frames per cycle at 30 fps), "pull" (plough / buggy: strained, slower; ~44 frames), "idle" (standing: tail swish,
    ear flick, a cocked hind leg; loop ~90 frames).  facing -1 mirrors.  base: a pose dict to start from."""
    p = dict(base or {})
    ph = _num(phase, 0.0)
    s = math.sin(2 * math.pi * ph)
    c = math.cos(2 * math.pi * ph)
    p["mirror"] = (_num(facing, 1.0) < 0)
    p["phase"] = ph % 1.0
    if mode == "idle":
        p.update(stride=0.0, bob=0.0, tail=0.8 * math.sin(2 * math.pi * ph * 2), ear=0.5 * max(0.0, math.sin(2 * math.pi * ph * 3)) - 0.15, head_pitch=4 + 3 * math.sin(2 * math.pi * ph),
                 rest=1.0)
    elif mode == "pull":
        p.update(stride=0.75, strain=1.0, bob=0.025 * math.cos(4 * math.pi * ph), tail=0.4 * s, head_pitch=3 * math.sin(4 * math.pi * ph), lift=0.9)
    else:
        p.update(stride=1.0, bob=0.035 * math.cos(4 * math.pi * ph), tail=0.5 * s, ear=0.15 * math.sin(4 * math.pi * ph + 1), head_pitch=-4 + 7 * math.sin(2 * math.pi * ph + 0.6))
    return p


def _mule_stub():
    d = dict(P.CAST["admiral"])
    d.update(_FLAGS, _mule=True)
    return d



# ============================================================================= story poses
def _grip2(S, name, hand_from="r", bend=0.5, shape="ball", layer="top", stretch=1.3):
    """put the other hand on the grip_far anchor of the prop held in `hand_from` (poles, shovels, handles, the cane)."""
    c, p = S[name]
    an = figure(c, p, "q")["anchors"]
    other = "l" if hand_from == "r" else "r"
    gx, gy = an["grip_far_%s" % hand_from]
    p["arm_" + other] = dict(hand=(gx, gy), bend=bend, stretch=stretch, shape=shape, layer=layer)


def _tip_to(S, name, key, target, prop_angle, it=4):
    """move the hand holding a prop so that its tip anchor lands on `target` (head frame) with the prop at prop_angle."""
    c, p = S[name]
    for _ in range(it):
        an = figure(c, p, "q")["anchors"]
        tx, ty = an[key]
        h = p["arm_" + ("r" if key.endswith("_r") else "l")]["hand"]
        p["arm_" + ("r" if key.endswith("_r") else "l")] = dict(p["arm_" + ("r" if key.endswith("_r") else "l")], hand=(h[0] + target[0] - tx, h[1] + target[1] - ty))


def _story():
    S, M = {}, {}
    MO, MY, MK = "morse16", "morse16", "mocker"
    A_, B_, C_ = "congressman_a", "congressman_b", "congressman_c"
    WA, WB, CO, ME, CL = "worker16_a", "worker16_b", "cornell", "messenger", "clerk16"
    shots = {}

    def add(name, cast, pose, note, shot=None, lipsync=False):
        S[name] = (cast, pose)
        M[name] = dict(note=note)
        if lipsync:
            M[name]["lipsync"] = True
        if shot is not None:
            M[name]["shots"] = shot

    # ------------------------------------------------------------------ Morse (adult)
    add("morse_idle", MO, dict(yaw=0.25, expr="neutral", arm_r="down", arm_l="down"), "standing, calm", "any")
    add("morse_cap_peg", MO, dict(yaw=0.45, pitch=-0.45, expr="determined", gaze=(0.6, -0.9), lean=-4, arm_r=dict(hand=(0.62, -0.78), bend=-0.6, stretch=1.3, layer="top"),
                                  prop_r=dict(type="bottle", angle=90, scale=1.0), glint=1.0, arm_l=dict(hand=(-0.46, 0.98), bend=0.5),
                                  legs=dict(stride=0.45, lift_l=0.85, crouch=0.06)), "on the ladder (3D rails in the set), arm up, capping the pole-top peg with the INVERTED bottle neck (lip down at anchor bottle_r); glint=1 flashes",
        "1, 23")
    add("morse_drape_wire", MO, dict(yaw=0.45, pitch=-0.35, expr="determined", gaze=(0.7, -0.7), lean=-3, arm_r=dict(hand=(0.70, -0.55), bend=-0.6, stretch=1.3, layer="top"),
                                      arm_l=dict(hand=(-0.50, 0.70), bend=0.6), prop_l="wire_coil", legs=dict(stride=0.40, lift_r=0.7, crouch=0.06)),
        "on the ladder, free hand lifting the wire over the glass, coil on the other arm", "1, 23")
    add("morse_proud_point", MO, dict(yaw=0.40, pitch=-0.25, expr="smug", mouth="smile", head_roll=-4, arm_r=dict(hand=(1.14, 0.30), shape="point", bend=-0.5, stretch=1.3),
                                      arm_l="hip", legs="wide"), "foot of the ladder, pointing proudly down the line of poles (screen-right)", "2")
    add("morse_tap_wire_grin", MO, dict(yaw=0.45, pitch=0.10, expr="grinning", head_roll=5, gaze=(0.8, 0.0), arm_r=dict(hand=(0.95, 0.50), shape="point", bend=-0.3, stretch=1.3),
                                         arm_l="hip", legs="stand"), "taps the wire (screen-right) and grins at it", "3")
    add("morse_cheer", MO, dict(yaw=0.20, pitch=-0.35, expr="laughing", fx=["tears"], head_roll=-6, t=0.3, arm_r=dict(hand=(0.78, -0.74), bend=-0.5, shape="open", stretch=1.3, layer="top"),
                                 arm_l=dict(hand=(-0.78, -0.70), bend=-0.5, shape="open", stretch=1.3, layer="top"), legs="wide", squash=(0.98, 1.03)),
        "both arms up, laughing with joy", "25, 26")
    add("morse_show_coil_magnet", MO, dict(yaw=0.35, pitch=-0.20, expr="excited", head_roll=-4, gaze=(0.5, -0.5), glint=1.0,
                                           arm_r=dict(hand=(0.74, 0.28), bend=-0.4, stretch=1.2), prop_r=dict(type="magnet", angle=-35),
                                           arm_l=dict(hand=(-0.50, 0.64), bend=0.5), prop_l="wire_coil", legs="stand"),
        "holds up the horseshoe magnet (blue spark at its poles, glint=1) and the copper coil: the idea", "7")
    add("morse_present_table", MO, dict(yaw=0.40, pitch=-0.15, expr="determined", head_roll=-3, arm_r=dict(preset="forward", hand=(1.00, 0.50), shape="open", bend=-0.3, stretch=1.3),
                                         arm_l=dict(hand=(-0.44, 0.88), bend=0.5), legs="wide"), "presenting the instrument to the tiers: one open hand out (screen-right)", "8")
    add("morse_clutch_coil", MO, dict(yaw=0.30, pitch=0.25, expr="worried", head_roll=4, gaze=(0.0, 0.5), fx=["sweat"], arm_r=dict(hand=(0.14, 0.86), bend=0.9, layer="top"),
                                       arm_l=dict(hand=(-0.12, 0.94), bend=0.9, layer="top"), prop_l=dict(type="wire_coil", scale=1.15), legs="stand"),
        "laughed at: clutches the copper coil to his chest, hurt but resolute", "11")
    add("morse_snap_up", MO, dict(yaw=0.20, pitch=-0.30, expr="determined", head_roll=-3, arm_r=dict(hand=(0.14, 0.86), bend=0.9, layer="top"),
                                   arm_l=dict(hand=(-0.12, 0.94), bend=0.9, layer="top"), prop_l="wire_coil", legs="stand"), "chin up after 'ไอ้บ้าลวด': coil held, jaw set", "11")
    add("morse_relieved", MO, dict(yaw=0.30, pitch=0.1, expr="happy", mouth="smile", head_roll=3, gaze=(0.6, 0.6), arm_r=dict(hand=(0.60, 1.05), bend=0.6, shape="open"), arm_l="hip", legs="stand"),
        "looking at the money bag on the table, a small relieved smile", "12")
    add("morse_key_press", MO, dict(yaw=0.55, pitch=0.35, expr="determined", gaze=(0.6, 0.9), lean=10, key_press=1.0, arm_r=dict(hand=(0.78, 1.52), bend=0.3, layer="front"),
                                     prop_r="telegraph_key", arm_l="hip", legs=dict(preset="stand", crouch=0.30)),
        "crouched at the crate, pressing the key (prop telegraph_key, anchor key_tip_r; key_press 0..1 animates the lever); skip the prop when the set shows the key", "15, 21")
    add("morse_key_wait", MO, dict(yaw=0.55, pitch=0.30, expr="worried", gaze=(0.5, 0.9), lean=8, key_press=0.0, arm_r=dict(hand=(0.78, 1.52), bend=0.3, layer="front"),
                                    prop_r="telegraph_key", arm_l=dict(hand=(-0.22, 0.90), bend=0.7), legs=dict(preset="stand", crouch=0.30)),
        "same crouch, key released, waiting: nothing happens", "15, 21")
    add("morse_empty_bag", MO, dict(yaw=0.30, pitch=0.30, expr="sad", gaze=(0.4, 0.9), head_roll=-4, squash=(1.02, 0.97), arm_r=dict(hand=(0.80, 0.70), bend=-0.2, stretch=1.1),
                                     prop_r="money_bag_empty", arm_l=dict(hand=(-0.44, 0.96), bend=0.5, shape="open"), legs="stand"),
        "turns out the empty money bag (lining sticking out), shoulders down", "17")
    add("morse_raise_pole", MO, dict(yaw=0.45, pitch=-0.3, expr="determined", gaze=(0.7, -0.6), lean=-6, arm_r=dict(hand=(0.78, -0.50), bend=-0.5, stretch=1.3, layer="top"),
                                      prop_r=dict(type="pole16", angle=-72), arm_l=dict(hand=(0.40, 0.10), bend=-0.2, layer="top"), legs=dict(preset="step", stride=0.4)),
        "heaving a bare pole up with the workers (pole16 at angle -72; anchor pole_tip_r)", "19")
    add("morse_bottle_sun", MO, dict(yaw=0.40, pitch=-0.50, expr="excited", gaze=(0.6, -0.9), head_roll=-5, glint=1.0, arm_r=dict(hand=(0.72, -0.62), bend=-0.6, stretch=1.3, layer="top"),
                                      prop_r=dict(type="bottle", angle=-60), arm_l="hip", legs="wide"),
        "'the answer is glass': holds the empty green bottle up to the sun, glint=1", "22")
    add("morse_read_tape", MO, dict(yaw=0.45, pitch=0.35, expr="excited", lean=8, gaze=(0.5, 0.9), arm_r=dict(hand=(0.82, 1.02), bend=0.2, stretch=1.1), prop_r=dict(type="paper", angle=60),
                                     arm_l=dict(hand=(-0.46, 0.96), bend=0.5), legs="stand"), "leans over the table reading the paper tape (dots and dashes are set art)", "26")
    add("morse_peek_door", MO, dict(yaw=-0.75, pitch=-0.05, expr="grinning", head_roll=8, head_dx=0.30, lean=14, arm_l=dict(hand=(-0.55, 0.50), shape="open", bend=-0.2, layer="front"),
                                     arm_r="behind", legs=dict(preset="stand", stride=0.2)), "peeking round the door frame at the end (screen-left), grinning", "30")
    # ------------------------------------------------------------------ Morse (1825, young=1)
    add("morse_young_idle", MY, dict(young=1, yaw=0.25, expr="neutral"), "the 1825 studio Morse standing", "4")
    add("morse_young_paint", MY, dict(young=1, yaw=0.55, pitch=-0.10, expr="determined", gaze=(0.9, -0.2), head_roll=-4, arm_r=dict(hand=(0.88, 0.30), bend=-0.5, stretch=1.3, layer="front"),
                                       prop_r=dict(type="brush16", angle=-25), arm_l=dict(hand=(-0.30, 0.96), bend=0.5), prop_l=dict(type="palette16", angle=-8), legs="stand"),
        "painting the big portrait on the easel (screen-right), brush in the right hand, palette on the other arm", "4, 5")
    add("morse_young_palette_ready", MY, dict(young=1, yaw=0.45, expr="happy", mouth="smile", head_roll=-3, arm_r=dict(hand=(0.50, 1.00), bend=0.4, stretch=1.1), prop_r=dict(type="brush16", angle=-70),
                                               arm_l=dict(hand=(-0.30, 0.96), bend=0.5), prop_l=dict(type="palette16", angle=-8), legs="stand"), "brush up, palette in hand, pleased", "5")
    add("morse_young_read_letter", MY, dict(young=1, yaw=0.30, pitch=0.30, expr="shocked", gaze=(0.0, 0.9), arm_r=dict(hand=(0.40, 0.80), bend=0.4, layer="top"), prop_r="letter",
                                             arm_l=dict(hand=(-0.40, 0.98), bend=0.5), prop_l=dict(type="palette16", angle=40), legs="stand"),
        "reads the sealed letter (prop letter), the palette starting to tip in the other hand", "6")
    add("morse_young_palette_drop", MY, dict(young=1, yaw=0.20, pitch=0.20, expr="shocked", gaze=(0.0, 0.5), fx=["sweat"], arm_r=dict(hand=(0.38, 0.78), bend=0.4, layer="top"), prop_r="letter",
                                              arm_l=dict(hand=(-0.50, 1.18), bend=0.2, shape="open"), prop_l=dict(type="palette16", angle=75), legs="stand"),
        "the palette slips from his fingers (animate prop_l angle 40 -> 90, then drop it in the set; no injury)", "6")
    add("morse_young_stool", MY, dict(young=1, yaw=0.40, pitch=0.40, expr="sad", gaze=(0.8, 0.7), head_roll=-5, lean=6, stool=1, arm_r=dict(hand=(0.30, 1.10), bend=0.6),
                                       arm_l=dict(hand=(-0.20, 1.10), bend=0.6), legs=dict(crouch=0.42, spread=0.05)),
        "sunk on a stool, looking at the small oval portrait (screen-right), hands in his lap", "6")
    # ------------------------------------------------------------------ the mocker
    add("mocker_idle", MK, dict(yaw=0.25, expr="smug", mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide"), "standing smug", "any")
    add("mocker_belly_laugh", MK, dict(yaw=0.20, pitch=-0.85, expr="laughing", fx=["tears"], head_roll=-10, lean=-8, t=0.3, squash=(1.03, 0.97),
                                        arm_r=dict(hand=(0.50, 1.02), bend=0.9, shape="open"), arm_l=dict(hand=(-0.54, 1.00), bend=0.9, shape="open"), legs="wide"),
        "BELLY LAUGH, head back, hands on the belly; the expression's own laughing mouth (no lip-sync); bounce: squash (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz and +/-0.06 D of hips", "11, 18 (lead-in)")
    add("mocker_mock_point", MK, dict(yaw=0.40, pitch=-0.30, expr="smug", mouth="talk_b", head_roll=8, squash=(1.02, 0.98),
                                       arm_r=dict(hand=(1.14, 0.06), shape="point", bend=-0.5, stretch=1.3), arm_l="akimbo", legs="wide"),
        "rising from the desk, pointing at the wire (screen-right), quote 1 'ส่งข่าวทางลวดเนี่ยนะ!'; LIP-SYNC with talk_mouth(g) 18.32-19.9", "9", True)
    add("mocker_boast_chest", MK, dict(yaw=0.30, pitch=-0.55, expr="smug", mouth="talk_a", head_roll=-6, lean=-6, squash=(1.01, 0.99),
                                        arm_r=dict(hand=(0.20, 0.74), bend=0.8, shape="open", layer="top"), prop_r=None, arm_l="akimbo", legs="wide"),
        "thumbs / thumps his own chest, chin up: 'ข้าจะมานั่งเฝ้ามันเอง!'; LIP-SYNC 19.9-23.2", "10", True)
    add("mocker_boast_finger", MK, dict(yaw=0.30, pitch=-0.40, expr="smug", mouth="talk_a", head_roll=-4, lean=-5, arm_r=dict(hand=(0.90, -0.48), shape="point", bend=-0.5, stretch=1.3),
                                         arm_l=dict(hand=(0.16, 0.76), bend=0.8, shape="open", layer="top"), legs="wide"),
        "alt for shot 10: index finger up, other hand on the chest; LIP-SYNC", "10", True)
    add("mocker_taunt_buggy", MK, dict(yaw=0.45, pitch=-0.25, expr="laughing", mouth="talk_b", fx=["tears"], head_roll=10, lean=16, t=0.3, squash=(1.02, 0.98),
                                        arm_r=dict(hand=(0.80, 1.14), shape="point", bend=0.0, stretch=1.3), arm_l=dict(hand=(-0.40, 1.00), bend=0.8, shape="open"), legs=dict(crouch=0.34, spread=0.1)),
        "leaning out of the open buggy (hips on the seat: legs crouched), laughing and pointing down at the furrow: 'เห็นมั้ย ลวดของเอ็ง ตายอยู่ใต้ดินแล้ว!'; LIP-SYNC 38.46-40.80 + bounce", "18", True)
    add("mocker_sour_arms", MK, dict(yaw=0.30, expr="unimpressed", mouth="frown", head_roll=4, pitch=-0.2, arm_r=dict(hand=(-0.46, 0.88), bend=0.9, layer="top"),
                                      arm_l=dict(hand=(0.46, 0.94), bend=0.9, layer="top"), legs="wide"), "SOUR: arms folded across the belly, mouth down", "12")
    add("mocker_jaw_drop", MK, dict(yaw=0.20, pitch=0.10, expr="shocked", mouth=("open", 0.26, 0.20), fx=["sweat"], arm_r="down", arm_l="down", squash=(0.98, 1.03), legs="stand"),
        "JAW DROP: held wide-open mouth, ring eyes, arms hanging", "26")
    add("mocker_hat_in_hand_amazed", MK, dict(hat_off=1, yaw=0.25, pitch=-0.1, expr="shocked", mouth=("open", 0.24, 0.18), arm_r=dict(hand=(0.60, 0.98), bend=0.4, layer="front"),
                                               prop_r="stovepipe_held", arm_l="down", legs="stand"), "hat off in his hand, jaw hanging (variant hat_off=1 shows the bald crown with the fringe)", "26")
    add("mocker_horror", MK, dict(sash=1, yaw=0.15, pitch=0.05, expr="shocked", mouth=("open", 0.16, 0.13), fx=["sweat"], head_roll=-4, squash=(0.98, 1.02),
                                   arm_r=dict(hand=(0.34, 0.40), bend=-0.2, shape="open", layer="top"), arm_l=dict(hand=(-0.34, 0.40), bend=-0.2, shape="open", layer="top"), legs="stand"),
        "HORROR (postmaster, sash on): hands up at the cheeks, ring eyes, sweat; the proud smile has dropped", "29")
    add("mocker_pm_proud", MK, dict(sash=1, yaw=0.30, pitch=-0.45, expr="smug", mouth="smile", head_roll=-4, lean=-5, squash=(1.01, 0.99),
                                     arm_r=dict(hand=(0.46, 0.76), bend=0.8, shape="open", layer="top"), arm_l="akimbo", legs="wide"),
        "POSTMASTER posing: chest out, hand on his sash (federal-green sash, leather mail bag at the hip, iron key ring on the belt)", "28")
    add("mocker_pm_keys", MK, dict(sash=1, yaw=0.35, pitch=-0.30, expr="smug", mouth="smile", head_roll=6, arm_r=dict(hand=(0.80, 0.56), bend=0.0, stretch=1.2), prop_r="keyring16", belt_keys=0,
                                    arm_l="akimbo", legs="wide"), "dangling a ring of keys from his hand (screen-right) as head of the Post Office", "28")
    add("mocker_pm_sour", MK, dict(sash=1, yaw=0.30, expr="unimpressed", mouth="frown", arm_r=dict(hand=(-0.46, 0.88), bend=0.9, layer="top"),
                                    arm_l=dict(hand=(0.46, 0.94), bend=0.9, layer="top"), legs="wide"), "postmaster, arms folded (sash on)", "28, 29")
    add("mocker_stool_candle", MK, dict(sash=1, hat_off=1, stool=1, yaw=0.40, pitch=-0.15, expr="asleep", mouth=("open", 0.30, 0.21), head_roll=-8, fx=[], t=0.3,
                                         arm_r=dict(hand=(0.74, 0.96), bend=0.4, layer="front"), prop_r="candle", arm_l=dict(hand=(-0.12, 0.34), bend=-0.2, shape="open", layer="top"),
                                         legs=dict(crouch=0.40, spread=0.05, stride=0.15), squash=(1.0, 1.0)),
        "ENDING: bald postmaster asleep-eyed on a stool, YAWNING (held wide mouth, hand to the mouth), candle in the other hand (animate t for the flame); tape piling at the boots is set art",
        "30")
    add("mocker_stool_candle_nod", MK, dict(sash=1, hat_off=1, stool=1, yaw=0.40, pitch=0.35, expr="asleep", mouth="flat", head_roll=-14, lean=6, t=0.3,
                                             arm_r=dict(hand=(0.74, 0.96), bend=0.4, layer="front"), prop_r="candle", arm_l="down", legs=dict(crouch=0.40, spread=0.05, stride=0.15)),
        "ENDING: head nodding on his chest, candle still in hand", "30")
    # ------------------------------------------------------------------ the congressmen
    for key, c in (("a", A_), ("b", B_), ("c", C_)):
        add("congressman_%s_laugh" % key, c, dict(yaw=0.25, pitch=-0.6, expr="laughing", fx=["tears"], head_roll=-8, lean=-6, t=0.3, squash=(1.03, 0.98),
                                                   arm_r=dict(hand=(0.40, 0.92), bend=0.8, shape="open"), arm_l=dict(hand=(-0.46, 0.90), bend=0.8, shape="open"), legs="wide"),
            "laughing, hands on the belly (bounce: squash 1.03/0.98 at ~3 Hz; the hat bounces with it)", "11")
        add("congressman_%s_point" % key, c, dict(yaw=0.40, pitch=-0.3, expr="laughing", head_roll=6, t=0.3, arm_r=dict(hand=(1.02, 0.16), shape="point", bend=-0.5, stretch=1.3), arm_l="hip", legs="wide"),
            "laughing and pointing at Morse (screen-right; mirror=True for left)", "11")
        add("congressman_%s_amazed" % key, c, dict(yaw=0.25, pitch=-0.1, expr="shocked", fx=["sweat"], arm_r=dict(hand=(0.46, 0.46), bend=0.3, shape="open", layer="top"),
                                                    arm_l=dict(hand=(-0.46, 0.52), bend=0.3, shape="open", layer="top"), legs="stand"), "amazed at the tape: ring eyes, hands up", "26")
    # ------------------------------------------------------------------ the messenger, the clerk
    add("messenger_hand_letter", ME, dict(yaw=0.40, pitch=-0.10, expr="neutral", mouth="smile", arm_r=dict(hand=(0.70, 0.74), bend=-0.1, stretch=1.1), prop_r="letter", arm_l="behind", legs="stand"),
        "holds the sealed letter out to Morse (screen-right)", "6")
    add("messenger_idle", ME, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing, cap on", "6")
    add("clerk_slide_instrument", CL, dict(yaw=0.40, pitch=0.10, expr="neutral", mouth="smile", lean=8, arm_r=dict(hand=(0.96, 0.98), bend=0.0, stretch=1.2, layer="front"),
                                            arm_l=dict(hand=(0.84, 1.04), bend=0.0, stretch=1.2, layer="front"), legs="stand"), "bent forward, both hands sliding the instrument across the table (screen-right)", "29")
    add("clerk_idle", CL, dict(yaw=0.30, expr="neutral", arm_r="down", arm_l="down"), "standing, sleeve garters", "29")
    # ------------------------------------------------------------------ Cornell
    add("cornell_plough", CO, dict(yaw=0.55, pitch=0.05, expr="determined", lean=14, head_roll=-3, arm_r=dict(hand=(0.70, 0.92), bend=0.2, layer="front"),
                                    prop_r=dict(type="plough16", angle=22), legs=dict(preset="step", stride=0.55)), "behind the plough, both hands on the handles, leaning into it (screen-right)", "13, 14")
    _grip2(S, "cornell_plough")
    add("cornell_hat_over", CO, dict(yaw=0.55, pitch=0.10, expr="worried", head_roll=-5, arm_r=dict(hand=(0.74, -0.42), bend=-0.4, stretch=1.3, layer="top"), prop_r="slouch_held",
                                      arm_l="hip", hat_off=1, legs="stand"), "holds his slouch hat over Morse in the rain (screen-right); hat_off=1 gives the bare head (the hat is in his hand)", "21")
    add("cornell_wait", CO, dict(yaw=0.40, expr="worried", arm_r=dict(hand=(-0.40, 0.92), bend=0.9, layer="top"), arm_l=dict(hand=(0.40, 0.96), bend=0.9, layer="top"), legs="wide"),
        "arms folded, waiting for the register to click", "15")
    add("cornell_direct", CO, dict(yaw=0.40, pitch=-0.10, expr="determined", arm_r=dict(hand=(1.04, 0.30), shape="point", bend=-0.4, stretch=1.3), arm_l="hip", legs="wide"),
        "directing the trench (screen-right)", "13")
    # ------------------------------------------------------------------ the workers
    for key, w in (("a", WA), ("b", WB)):
        add("worker_%s_lean_shovel" % key, w, dict(yaw=0.30, pitch=0.10, expr="worried", head_roll=-4, arm_r=dict(hand=(0.46, 0.92), bend=0.5, layer="front"), prop_r=dict(type="shovel16", angle=100, scale=0.90),
                                                    arm_l=dict(hand=(0.40, 0.84), bend=0.5, layer="top"), legs=dict(preset="stand", stride=0.2)), "leaning on the shovel, waiting", "15, 17")
        add("worker_%s_shovel" % key, w, dict(yaw=0.55, pitch=0.15, expr="determined", lean=10, arm_r=dict(hand=(0.60, 0.80), bend=0.3, layer="front"), prop_r=dict(type="shovel16", angle=62),
                                               arm_l=dict(hand=(0.50, 1.20), bend=0.3, layer="top"), legs=dict(preset="step", stride=0.45)), "digging / following the plough with the shovel (screen-right)", "13, 14")
        add("worker_%s_carry_pole" % key, w, dict(yaw=0.50, expr="determined", lean=-3, arm_r=dict(hand=(0.40, 0.46), bend=-0.2, layer="top"), prop_r=dict(type="pole16", angle=-8),
                                                   arm_l=dict(hand=(-0.30, 0.50), bend=-0.2, layer="front"), legs=dict(preset="step", stride=0.35)), "carrying a pole on the shoulder (screen-right; pole16 centred on the hand)", "19")
        add("worker_%s_raise_pole" % key, w, dict(yaw=0.45, pitch=-0.3, expr="determined", lean=-6, arm_r=dict(hand=(0.70, -0.40), bend=-0.5, stretch=1.3, layer="top"), prop_r=dict(type="pole16_end", angle=-75),
                                                   arm_l=dict(hand=(0.30, 0.30), bend=-0.2, layer="top"), legs=dict(preset="step", stride=0.4)), "heaving the pole upright with Morse (pole16_end at -75)", "19")
    add("worker_b_pick", WB, dict(yaw=0.40, pitch=0.05, expr="neutral", arm_r=dict(hand=(0.50, 0.10), bend=-0.5, layer="top"), prop_r=dict(type="pick16", angle=-128), arm_l=dict(hand=(0.34, 0.40), bend=-0.2, layer="top"),
                                  legs="wide"), "pick over the shoulder, leaning back", "13")
    wv = dict(yaw=0.30, expr="happy", head_roll=4, t=0.3, arm_r=dict(hand=(0.80, -0.55), bend=-0.5, shape="open", stretch=1.3, layer="top"), arm_l="down", legs="stand")
    add("messenger_wave", ME, dict(wv, expr="excited"), "waving the news on the platform (open hand up; animate hand x +-0.12 at 3 Hz)", "27")
    add("worker_a_wave", WA, dict(wv, expr="grinning"), "waving the news on the platform", "27")
    add("congressman_b_wave", B_, dict(wv, expr="laughing"), "waving, delighted, on the platform", "27")
    add("congressman_c_wave", C_, dict(wv, expr="grinning", arm_l=dict(hand=(-0.70, 0.30), bend=0.2, shape="open")), "dandy waving with both hands on the platform", "27")
    add("worker_a_wait_arms", WA, dict(yaw=0.30, expr="worried", arm_r=dict(hand=(-0.40, 0.90), bend=0.9, layer="top"), arm_l=dict(hand=(0.40, 0.94), bend=0.9, layer="top"), legs="wide"), "arms folded, waiting", "15, 21")
    return S, M


STORY16_SHOTS = {1: ["morse_cap_peg", "morse_drape_wire"], 2: ["morse_proud_point"], 3: ["morse_tap_wire_grin"], 4: ["morse_young_idle", "morse_young_paint"],
                 5: ["morse_young_paint", "morse_young_palette_ready"], 6: ["morse_young_read_letter", "morse_young_palette_drop", "morse_young_stool", "messenger_hand_letter", "messenger_idle"],
                 7: ["morse_show_coil_magnet"], 8: ["morse_present_table", "congressman_a_amazed"],
                 9: ["mocker_mock_point", "mocker_belly_laugh"], 10: ["mocker_boast_chest", "mocker_boast_finger"],
                 11: ["congressman_a_laugh", "congressman_b_laugh", "congressman_c_laugh", "congressman_a_point", "congressman_b_point", "congressman_c_point",
                      "mocker_belly_laugh", "morse_clutch_coil", "morse_snap_up"],
                 12: ["morse_relieved", "mocker_sour_arms"],
                 13: ["cornell_plough", "cornell_direct", "worker_a_shovel", "worker_b_shovel", "worker_b_pick"], 14: ["cornell_plough", "worker_a_shovel", "worker_b_shovel"],
                 15: ["morse_key_press", "morse_key_wait", "cornell_wait", "worker_a_lean_shovel", "worker_b_lean_shovel", "worker_a_wait_arms"],
                 17: ["morse_empty_bag", "worker_a_lean_shovel", "worker_b_lean_shovel"],
                 18: ["mocker_taunt_buggy", "mocker_belly_laugh"],
                 19: ["morse_raise_pole", "worker_a_raise_pole", "worker_b_raise_pole", "worker_a_carry_pole", "worker_b_carry_pole"],
                 21: ["morse_key_wait", "morse_key_press", "cornell_hat_over", "worker_a_wait_arms"], 22: ["morse_bottle_sun"], 23: ["morse_cap_peg", "morse_drape_wire"],
                 25: ["morse_cheer"], 27: ["messenger_wave", "worker_a_wave", "congressman_b_wave", "congressman_c_wave"], 26: ["morse_read_tape", "morse_cheer", "congressman_a_amazed", "congressman_b_amazed", "congressman_c_amazed", "mocker_jaw_drop", "mocker_hat_in_hand_amazed"],
                 28: ["mocker_pm_proud", "mocker_pm_keys", "mocker_pm_sour"], 29: ["clerk_slide_instrument", "clerk_idle", "mocker_pm_proud", "mocker_horror"],
                 30: ["mocker_stool_candle", "mocker_stool_candle_nod", "morse_peek_door"]}


STORY16, STORY16_META = {}, {}


def register():
    if getattr(P, "_cast16_registered", False):
        CE.register_stage()
        if not STORY16:
            s, m = _story()
            STORY16.update(s)
            STORY16_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "figure"):
        _O16[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P.figure = figure
    CE.COSTUMES.update(COSTUMES16)
    CE.HATS.update(HATS16)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS16 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP16)
    for n, c in _cast_table().items():
        P.CAST[n] = c
    P.CAST["mule"] = _mule_stub()
    CE.CANVAS.update(CANVAS16)
    P._cast16_registered = True
    s, m = _story()
    STORY16.update(s)
    STORY16_META.update(m)
    P.STORY.update(STORY16)
    CE.register_stage()


register()
