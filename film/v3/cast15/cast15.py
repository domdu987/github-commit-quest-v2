#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast15.py -- the cast of film 15 ("ไอ้ปลาดิ้น": Dick Fosbury and the flop; a 1963 high-school track and the 1968 Olympic
stadium) for the v2 puppet, as an extension module on top of cast10.

    import sys; sys.path.insert(0, ".../v3/cast15"); import cast15      # registers on import (idempotent); chains cast10 .. v2/puppet
    import puppet                                                       # the same module object, now with the new members
    f = puppet.figure("dick", cast15.pose("flop"), "f")                 # a jump pose for any jumper
    cast, pose = cast15.STORY15["dick_flop"]
    f = puppet.figure(cast, pose, "f")

Nothing in v2/puppet or v3/cast .. cast10 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  vest15 (running vest, optional chest stripes), jacket15 (windbreaker with lanyards), aloha15 (loud tourist
                       shirt), blazer15 (blazer, shirt and tie), shirt15 (plain shirt / jumper for spectators)
    cast_ext.HATS      hair15 (hair masses that stick out of the head disc: tousle / crew / curly / quiff / bouffant / bald),
                       cap15 (baseball-style cap), tourist15 (floppy hat with a striped pennant)
    cast_ext.CANVAS    one feet-relative sprite canvas per member (standing); CANVAS15_WIDE for the lying / bridge poses
and wraps puppet helpers on top of cast10's wrappers (each falls through for everything it does not handle):
    _norm       reads this module's pose keys (body_lean, hdx2, hdy2, roll2 with wider ranges than the base clamps, sawdust, buried,
                flash, medal, bob, t) and the skin tone
    _ink_limb   socks and shoes (sneakers, spikes, dress shoes) on the legs (CAST shoe15)
    _prop       clipboard, presscam
    figure      ears and a heavy jaw behind the head disc, `bob`, the sawdust mound `buried`, the flash burst, anchors
New cast: dick, coach, boy1..3, rival1..3, official1..2, photographer, crowd1..6.

Why this module exists: the puppet's torso is rigid and its pose keys are clamped (lean +-75, head_roll +-75, head_dx/dy +-0.8).
The FLOP (an arched bridge) and the STRADDLE (flat, face down) need the torso at 90..130 degrees, so `body_lean` and friends
take a wider range.  See API.md.
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
import cast8 as C8      # noqa: E402
import cast6 as C6      # noqa: E402
import cast4 as C4      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW15 = ("dick", "coach", "boy1", "boy2", "boy3", "rival1", "rival2", "rival3", "official1", "official2", "photographer",
         "crowd1", "crowd2", "crowd3", "crowd4", "crowd5", "crowd6")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d, _shade, _mix = P._poly, P._poly_d, P._shade, P._mix
_X, _ln, _circ, _bowl = CE._X, CE._ln, CE._circ, CE._bowl
_f = C6._f
_O15 = {}
_POSE15 = {"hat_off": 0.0, "sawdust": 0.0, "medal": 0.0, "flash": 0.0, "t": 0.0, "roll": 0.0, "yaw": 0.0, "bend": 0.0, "bend_y": 0.6}

cycle, talk_mouth, blink_at, NOD = C6.cycle, C6.talk_mouth, C6.blink_at, C6.NOD

# ============================================================================= colours
CHIP = ("#e2bd86", "#c99a5c", "#ecd09c", "#b98a4e")           # sawdust / wood chips
GOLD = dict(light="#fff0a8", base="#e2b442", dark="#a07818")
MAROON = dict(light="#a8394a", base="#7a1f33", dark="#4a1020")
TIN = C10.TIN
SKIN_TONES = {
    "fair": ("#fef7f6", "#e9dceb"),            # the puppet default
    "tan": ("#f1cfa6", "#d9b690"),
    "brown": ("#c8946a", "#a87a56"),
    "dark": ("#9a6a48", "#7e5438"),
    "ruddy": ("#f6c8b8", "#e0aea0"),
}


def _hash(*a):
    s = 0.0
    for i, v in enumerate(a):
        s += (i + 1.37) * v * 12.9898
    x = math.sin(s) * 43758.5453
    return x - math.floor(x)


def _chips(k, pts, seed, lev=1.0, size=0.05):
    """small wood chips at pts (x, y, ...): tilted rectangles in four sawdust browns, deterministic."""
    o = []
    for i, p in enumerate(pts):
        if lev < _hash(seed, i, 7.0) * 0.9 + 0.08:
            continue
        a = 360.0 * _hash(seed, i, 3.0)
        c = CHIP[i % len(CHIP)]
        w = size * (0.7 + 0.8 * _hash(seed, i, 5.0))
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="%.4f" transform="rotate(%.1f %.4f %.4f)" fill="%s" stroke="%s" stroke-width="0.006"/>'
                 % (p[0] - w / 2, p[1] - w * 0.2, w, w * 0.42, w * 0.1, a, p[0], p[1], k.c(c), k.c("#7a5a34")))
    return "".join(o)


def _hat_chips(k, C, yaw, ytop, yb):
    """chips lying on the hair / hat (head frame) when pose sawdust > 0."""
    lev = _POSE15["sawdust"]
    if lev < 0.02:
        return ""
    pts = []
    for i in range(16):
        x = -0.48 + 0.96 * _hash(C["seed"], i, 1.0)
        yy = ytop + (yb - ytop) * (0.15 + 0.8 * _hash(C["seed"], i, 2.0))
        pts.append((x * (1.0 - 0.35 * max(0.0, (yb - yy) / max(yb - ytop, 0.1) - 0.5)), yy))
    return _chips(k, pts, C["seed"] + 5.0, lev)


# ============================================================================= costumes (torso-local, inside the torso clip)
def _neck_skin(k, X, hw, y0, y1, w=0.30):
    """the bare neck / chest opening (skin colour = the head fill)."""
    return _poly(k, [X(-hw * w, y0 - 0.02), X(hw * w, y0 - 0.02), X(hw * w * 0.55, y1), X(-hw * w * 0.55, y1)], k.c(P.HEAD_FILL), 0.012)


def _medal_on_chest(k, X, hw):
    """pose medal=1: a gold medal on a red-white-blue ribbon (no letters): V ribbon round the neck and a disc on the breastbone."""
    if _POSE15["medal"] < 0.5:
        return ""
    o = []
    ribbon = ((-0.30, "#c8302a"), (0.30, "#2a4a9a"))
    for s, col in ((-1, "#c8302a"), (1, "#2a4a9a")):
        o.append(_poly(k, [X(s * hw * 0.46, 0.40), X(s * hw * 0.22, 0.40), X(s * hw * 0.02, 1.00), X(s * hw * 0.26, 1.00)], k.c(col), 0.010))
    o.append(_poly(k, [X(-hw * 0.06, 0.86), X(hw * 0.06, 0.86), X(hw * 0.07, 1.02), X(-hw * 0.07, 1.02)], k.c("#f4f2ee"), 0.008))
    c = X(0.0, 1.08)
    r = min(0.14, 0.17 * hw + 0.04)
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.016"/>' % (c[0], c[1], r, k.c(GOLD["base"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="none" stroke="%s" stroke-width="0.012"/>' % (c[0], c[1], r * 0.62, k.c(GOLD["dark"])))
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
             % (c[0] - r * 0.6, c[1] - r * 0.2, r * 0.65, r * 0.65, c[0] - r * 0.1, c[1] - r * 0.7, k.c(GOLD["light"])))
    return "".join(o)


def _torso_chips(k, C, X, hw, yB):
    lev = _POSE15["sawdust"]
    if lev < 0.02:
        return ""
    pts = [(X((_hash(C["seed"], i, 9.0) - 0.5) * 1.5 * hw, 0)[0], 0.45 + (yB - 0.55) * _hash(C["seed"], i, 4.0)) for i in range(18)]
    return _chips(k, pts, C["seed"] + 9.0, lev, 0.04)


def _cos_vest15(k, C, m):
    """running vest (singlet): colours base, trim (neck and armhole binding), s1 / s2 (two bands across the chest, optional),
    hem (a band above the shorts), pants (shorts bowl).  No letters, no numbers."""
    X = _X(m)
    col = C["colors"]
    hw = m.hwa
    yB = TT + C["torso_h"]
    yb = yB - 0.16
    o = []
    # bare shoulders / chest top: scooped neck
    o.append(_poly(k, [X(-hw * 0.62, 0.34), X(hw * 0.62, 0.34), X(hw * 0.5, 0.50), X(hw * 0.16, 0.66), X(-hw * 0.16, 0.66), X(-hw * 0.5, 0.50)], k.c(P.HEAD_FILL), 0.012))
    o.append(_ln([X(-hw * 0.5, 0.50), X(-hw * 0.16, 0.66), X(hw * 0.16, 0.66), X(hw * 0.5, 0.50)], k.c(col["trim"]), 0.034))
    if col.get("s1"):
        o.append(_poly(k, [X(-hw * 1.2, 0.76), X(hw * 1.2, 0.76), X(hw * 1.2, 0.87), X(-hw * 1.2, 0.87)], k.c(col["s1"]), 0.0))
    if col.get("s2"):
        o.append(_poly(k, [X(-hw * 1.2, 0.90), X(hw * 1.2, 0.90), X(hw * 1.2, 1.01), X(-hw * 1.2, 1.01)], k.c(col["s2"]), 0.0))
    if col.get("hem"):
        o.append(_poly(k, [X(-hw * 1.2, yb - 0.09), X(hw * 1.2, yb - 0.09), X(hw * 1.2, yb), X(-hw * 1.2, yb)], k.c(col["hem"]), 0.0))
    for s in (-1, 1):     # armhole binding
        o.append(_ln([X(s * hw * 0.98, 0.40), X(s * hw * 0.86, 0.60), X(s * hw * 0.92, 0.80)], k.c(col["trim"]), 0.030))
    if col.get("edge"):   # solid side bands: keep the white vest readable on pale ground
        for s in (-1, 1):
            o.append(_poly(k, [X(s * hw * 1.3, 0.30), X(s * hw * 0.80, 0.30), X(s * hw * 0.80, yb), X(s * hw * 1.3, yb)], k.c(col["edge"]), 0.0))
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append(_ln([X(-hw * 1.05, yb + 0.012), X(0, yb + 0.03), X(hw * 1.05, yb + 0.012)], k.c(_shade(col["pants"], 0.78)), 0.014))
    o.append(_medal_on_chest(k, X, hw))
    o.append(_torso_chips(k, C, X, hw, yB))
    return "".join(o)


def _cos_jacket15(k, C, m):
    """the coach's windbreaker: stand-up collar, a zip down the front, two side stripes, flapped pockets, an elastic hem, and
    two lanyards with a whistle and a stopwatch hanging over the belly.  Colours base, dark, trim, zip, collar, pants."""
    X = _X(m)
    col = C["colors"]
    hw = m.hwa
    yB = TT + C["torso_h"]
    yb = yB - 0.16
    o = []
    # open V at the neck with the white tee, collar flaps
    o.append(_poly(k, [X(-hw * 0.28, 0.36), X(hw * 0.28, 0.36), X(0.0, 0.66)], k.c("#f4f1ea"), 0.012))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * hw * 0.30, 0.34), X(s * hw * 0.62, 0.36), X(s * hw * 0.50, 0.58), X(s * hw * 0.04, 0.70), X(s * hw * 0.04, 0.50)], k.c(col["collar"]), 0.014))
    # side stripes
    for s in (-1, 1):
        o.append(_ln([X(s * hw * 0.80, 0.50), X(s * hw * 0.92, yb)], k.c(col["trim"]), 0.040))
    # zip + pockets
    o.append(_ln([X(0.0, 0.70), X(0.0, yb)], k.c(col["zip"]), 0.016))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * hw * 0.36, yb - 0.30), X(s * hw * 0.64, yb - 0.30), X(s * hw * 0.62, yb - 0.14), X(s * hw * 0.34, yb - 0.14)], k.c(col["dark"]), 0.012))
    # elastic hem band
    o.append(_poly(k, [X(-hw * 1.2, yb - 0.06), X(hw * 1.2, yb - 0.06), X(hw * 1.2, yb + 0.03), X(-hw * 1.2, yb + 0.03)], k.c(col["dark"]), 0.014))
    o.append(_bowl(k, col["pants"], yb + 0.02, yB))
    # lanyards: two cords from the neck, a whistle (right) and a stopwatch (left) hanging over the belly
    cw = k.c("#2a2430")
    wx, wy = X(hw * 0.20, 1.00)
    sx, sy = X(-hw * 0.14, 0.98 + 0.12 * min(1.0, hw))
    o.append('<path d="M%.4f,0.38 Q%.4f,0.80 %.4f,%.4f M%.4f,0.38 Q%.4f,0.80 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>'
             % (X(hw * 0.20, 0.38)[0], wx - 0.02, wx, wy - 0.05, X(-hw * 0.20, 0.38)[0], sx + 0.02, sx, sy - 0.10, cw))
    o.append('<rect x="%.4f" y="%.4f" width="0.15" height="0.065" rx="0.030" fill="%s" stroke="%s" stroke-width="0.014"/>' % (wx - 0.06, wy - 0.05, k.c("#c9ced4"), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.020" fill="%s" stroke="%s" stroke-width="0.008"/>' % (wx + 0.045, wy - 0.015, k.c("#3a3640"), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.100" fill="%s" stroke="%s" stroke-width="0.018"/>' % (sx, sy, k.c("#f6f2e6"), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.100" fill="none" stroke="%s" stroke-width="0.020" opacity="0.9"/>' % (sx, sy, k.c("#b9bec6")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (sx, sy, sx, sy - 0.065, sx, sy, sx + 0.045, sy + 0.020, k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="0.036" height="0.030" fill="%s" stroke="%s" stroke-width="0.008"/>' % (sx - 0.018, sy - 0.128, k.c("#b9bec6"), k.ink))
    o.append(_medal_on_chest(k, X, hw))
    o.append(_torso_chips(k, C, X, hw, yB))
    return "".join(o)


def _cos_aloha15(k, C, m):
    """the loud tourist shirt: open collar, hibiscus blobs and leaves on a bright ground, buttons, bermuda-ish trousers."""
    X = _X(m)
    col = C["colors"]
    hw = m.hwa
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    o = []
    seed = C["seed"]
    for i in range(9):
        x = (-0.9 + 1.8 * _hash(seed, i, 1.0)) * hw
        y = 0.55 + (yb - 0.65) * _hash(seed, i, 2.0)
        c = X(x, y)
        r = 0.060 + 0.050 * _hash(seed, i, 3.0)
        for j in range(5):
            a = 2 * math.pi * j / 5 + _hash(seed, i, 4.0) * 3
            o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%.1f %.4f %.4f)" fill="%s"/>'
                     % (c[0] + r * 0.55 * math.cos(a), c[1] + r * 0.55 * math.sin(a), r * 0.55, r * 0.34, math.degrees(a), c[0] + r * 0.55 * math.cos(a), c[1] + r * 0.55 * math.sin(a),
                        k.c(col["flower"] if i % 2 == 0 else col["flower2"])))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (c[0], c[1], r * 0.22, k.c(col["centre"])))
        a = 1.0 + 2.2 * _hash(seed, i, 6.0)
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%.1f %.4f %.4f)" fill="%s"/>'
                 % (c[0] + r * 1.2 * math.cos(a), c[1] + r * 1.2 * math.sin(a), r * 0.75, r * 0.22, math.degrees(a), c[0] + r * 1.2 * math.cos(a), c[1] + r * 1.2 * math.sin(a), k.c(col["leaf"])))
    # open collar
    o.append(_poly(k, [X(-hw * 0.32, 0.34), X(hw * 0.32, 0.34), X(0.0, 0.76)], k.c(P.HEAD_FILL), 0.012))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * hw * 0.30, 0.34), X(s * hw * 0.58, 0.40), X(s * hw * 0.40, 0.62), X(s * hw * 0.02, 0.78)], k.c(col["collar"]), 0.014))
    o.append(_ln([X(0.0, 0.80), X(0.0, yb)], k.c(_shade(col["base"], 0.72)), 0.014))
    for y in (0.92, 1.06, 1.20):
        if y < yb - 0.04:
            o.append(_circ(X(0.0, y), 0.022, k.c("#fff6d8"), k, 0.008))
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append(_torso_chips(k, C, X, hw, yB))
    return "".join(o)


def _cos_blazer15(k, C, m):
    """1968 official / spectator: blazer with notched lapels, white shirt, tie, two plain buttons, breast pocket with a
    white handkerchief, trousers.  Colours base, dark, lapel, shirt, tie, pants, button."""
    X = _X(m)
    col = C["colors"]
    hw = m.hwa
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    o = [_bowl(k, col["pants"], yb, yB)]
    o.append(_poly(k, [X(-hw * 0.30, 0.34), X(hw * 0.30, 0.34), X(0.0, 0.92)], k.c(col["shirt"]), 0.012))
    o.append(_poly(k, [X(-0.035, 0.46), X(0.035, 0.46), X(0.045, 0.62), X(0.0, 0.98), X(-0.045, 0.62)], k.c(col["tie"]), 0.010))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * hw * 0.28, 0.34), X(s * hw * 0.10, 0.50), X(s * hw * 0.34, 0.54)], k.c(col["shirt"]), 0.010))
        o.append(_poly(k, [X(s * hw * 0.34, 0.36), X(s * hw * 0.70, 0.42), X(s * hw * 0.52, 0.62), X(s * hw * 0.62, 0.74), X(s * hw * 0.06, 1.05), X(s * hw * 0.06, 0.80)], k.c(col["lapel"]), 0.016))
    o.append(_ln([X(hw * 0.06, 1.05), X(hw * 0.10, yb)], k.ink, 0.016))
    for y in (1.06, 1.20):
        if y < yb - 0.02:
            o.append(_circ(X(hw * 0.12, y), 0.026, k.c(col.get("button", "#d8b44a")), k, 0.010))
    # breast pocket + handkerchief (screen-left)
    px = -hw * 0.56
    o.append(_poly(k, [X(px - 0.09, 0.80), X(px + 0.09, 0.80), X(px + 0.09, 0.84), X(px - 0.09, 0.84)], k.c(col["dark"]), 0.010))
    o.append(_poly(k, [X(px - 0.05, 0.76), X(px + 0.00, 0.72), X(px + 0.05, 0.76), X(px + 0.05, 0.81), X(px - 0.05, 0.81)], k.c("#f6f4ee"), 0.008))
    o.append(_poly(k, [X(hw * 0.36, 1.12), X(hw * 0.70, 1.12), X(hw * 0.68, 1.16), X(hw * 0.38, 1.16)], k.c(col["dark"]), 0.010))
    o.append(_medal_on_chest(k, X, hw))
    o.append(_torso_chips(k, C, X, hw, yB))
    return "".join(o)


def _cos_shirt15(k, C, m):
    """plain collared shirt or jumper for spectators and the press: optional horizontal stripe (stripe), open collar."""
    X = _X(m)
    col = C["colors"]
    hw = m.hwa
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    o = []
    if col.get("stripe"):
        for i, y in enumerate((0.62, 0.80, 0.98, 1.16)):
            if y < yb - 0.04:
                o.append(_poly(k, [X(-hw * 1.2, y), X(hw * 1.2, y), X(hw * 1.2, y + 0.07), X(-hw * 1.2, y + 0.07)], k.c(col["stripe"]), 0.0))
    o.append(_poly(k, [X(-hw * 0.30, 0.34), X(hw * 0.30, 0.34), X(0.0, 0.62)], k.c(P.HEAD_FILL), 0.012))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * hw * 0.28, 0.34), X(s * hw * 0.56, 0.40), X(s * hw * 0.38, 0.58), X(s * hw * 0.02, 0.64)], k.c(col["collar"]), 0.014))
    o.append(_ln([X(0.0, 0.66), X(0.0, yb)], k.c(_shade(col["base"], 0.72)), 0.012))
    if col.get("tie"):
        o.append(_poly(k, [X(-0.03, 0.44), X(0.03, 0.44), X(0.04, 0.62), X(0.0, 1.00), X(-0.04, 0.62)], k.c(col["tie"]), 0.010))
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append(_torso_chips(k, C, X, hw, yB))
    return "".join(o)


COSTUMES15 = {"vest15": _cos_vest15, "jacket15": _cos_jacket15, "aloha15": _cos_aloha15, "blazer15": _cos_blazer15, "shirt15": _cos_shirt15}


# ============================================================================= hats and hair (head frame)
def _hat_hair15(k, C, yaw):
    """hair masses that stick out of the head disc (so the silhouette reads at phone size).  CAST hair_style15:
    tousle (spiky, uneven), crew (flat-top crew cut), curly (a cloud of curls), quiff (a combed wave), bouffant (a tall
    rounded 1960s set), bald (nothing).  Colour: hair["color"]; hair["shine"] optional."""
    st = C.get("hair_style15", "crew")
    col = k.c(C["hair"]["color"])
    hl = k.c(C["hair"].get("shine", _shade(C["hair"]["color"], 1.35)))
    dx = 0.10 * yaw
    sd = C["seed"]
    o = []
    top = -0.46
    if st == "bald":
        return "", (0.0, -0.49)
    if st == "tousle":
        base = [(-0.49 + dx * 0.3, -0.12), (-0.50 + dx * 0.3, -0.30), (-0.40 + dx, -0.47)]
        tufts = []
        n = 8
        for i in range(n):
            t = i / (n - 1.0)
            x = -0.40 + 0.80 * t + dx
            h = 0.10 + 0.17 * _hash(sd, i, 1.0)
            lean = (_hash(sd, i, 2.0) - 0.45) * 0.20
            tufts.append((x - 0.07, top + 0.05 - 0.02 * math.sin(math.pi * t)))
            tufts.append((x + lean, top - h - 0.06 * math.sin(math.pi * t)))
        pts = base + tufts + [(0.40 + dx, -0.47), (0.50 + dx * 0.3, -0.30), (0.49 + dx * 0.3, -0.12)]
        # forehead edge: ragged, higher over the face than at the temples
        edge = [(0.46 + dx * 0.3, -0.24), (0.30 + dx, -0.31), (0.16 + dx, -0.25), (0.02 + dx, -0.33), (-0.14 + dx, -0.26), (-0.30 + dx, -0.32), (-0.46 + dx * 0.3, -0.24)]
        d = "M" + " L".join("%.4f,%.4f" % p for p in pts) + " L" + " L".join("%.4f,%.4f" % p for p in edge) + " Z"
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, col, k.ink))
        o.append('<path d="M%.4f,-0.60 Q%.4f,-0.50 %.4f,-0.45" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (-0.16 + dx, -0.20 + dx, -0.24 + dx, hl))
        ytop = top - 0.28
    elif st == "crew":
        d = ("M%.4f,-0.14 L%.4f,-0.40 Q%.4f,-0.54 %.4f,-0.60 L%.4f,-0.60 Q%.4f,-0.54 %.4f,-0.40 L%.4f,-0.14 L%.4f,-0.27 Q%.4f,-0.34 %.4f,-0.31 Q%.4f,-0.35 %.4f,-0.30 Q%.4f,-0.27 %.4f,-0.25 Z"
             % (-0.50 + dx * 0.3, -0.52 + dx * 0.3, -0.45 + dx, -0.36 + dx, 0.36 + dx, 0.45 + dx, 0.52 + dx * 0.3, 0.50 + dx * 0.3,
                0.40 + dx, 0.20 + dx, 0.05 + dx, -0.12 + dx, -0.22 + dx, -0.40 + dx, -0.40 + dx))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, col, k.ink))
        for i in range(9):
            x = -0.34 + 0.085 * i + dx
            o.append('<path d="M%.4f,-0.585 L%.4f,-0.50" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % (x, x + 0.01, hl))
        ytop = -0.60
    elif st == "curly":
        pts = [(-0.48, -0.14), (-0.58, -0.30), (-0.54, -0.50), (-0.38, -0.66), (-0.14, -0.74), (0.14, -0.74), (0.38, -0.66), (0.54, -0.50), (0.58, -0.30), (0.48, -0.14)]
        for i, p in enumerate(pts):
            pass
        circ = []
        for i, (x, y) in enumerate(pts):
            circ.append((x * 1.0 + dx, y, 0.12 + 0.02 * _hash(sd, i, 1.0)))
        circ += [(-0.22 + dx, -0.60, 0.17), (0.04 + dx, -0.66, 0.18), (0.28 + dx, -0.58, 0.16), (-0.40 + dx, -0.38, 0.15), (0.40 + dx, -0.38, 0.15)]
        o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.026"/>' % (x, y, r + 0.0, col, k.ink) for (x, y, r) in circ))
        o.append("".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, y, r - 0.012, col) for (x, y, r) in circ))
        # clear a face window (forehead) over the curls
        o.append('<path d="M%.4f,-0.26 Q%.4f,-0.36 %.4f,-0.28 Q%.4f,-0.34 %.4f,-0.27 Q%.4f,-0.35 %.4f,-0.26 L%.4f,-0.20 L%.4f,-0.20 Z" fill="%s"/>'
                 % (-0.44 + dx, -0.30 + dx, -0.12 + dx, 0.10 + dx, 0.22 + dx, 0.36 + dx, 0.44 + dx, 0.44 + dx, -0.44 + dx, "none"))
        ytop = -0.86
    elif st == "quiff":
        d = ("M%.4f,-0.16 Q%.4f,-0.46 %.4f,-0.60 Q%.4f,-0.78 %.4f,-0.70 Q%.4f,-0.62 %.4f,-0.52 Q%.4f,-0.44 %.4f,-0.16 L%.4f,-0.27 Q%.4f,-0.35 %.4f,-0.31 Q%.4f,-0.37 %.4f,-0.30 Q%.4f,-0.36 %.4f,-0.25 Z"
             % (-0.50 + dx * 0.3, -0.52 + dx, -0.30 + dx, 0.10 + dx, 0.34 + dx, 0.50 + dx, 0.54 + dx * 0.3, 0.52 + dx * 0.3, 0.50 + dx * 0.3,
                0.40 + dx, 0.22 + dx, 0.05 + dx, -0.12 + dx, -0.26 + dx, -0.42 + dx, -0.42 + dx))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, col, k.ink))
        o.append('<path d="M%.4f,-0.64 Q%.4f,-0.70 %.4f,-0.60" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (-0.26 + dx, -0.05 + dx, 0.16 + dx, hl))
        ytop = -0.76
    else:   # bouffant
        d = ("M%.4f,-0.04 Q%.4f,-0.34 %.4f,-0.58 Q%.4f,-0.86 %.4f,-0.88 Q%.4f,-0.86 %.4f,-0.58 Q%.4f,-0.34 %.4f,-0.04 Q%.4f,-0.20 %.4f,-0.34 Q%.4f,-0.20 %.4f,-0.30 Q%.4f,-0.34 %.4f,-0.34 Q%.4f,-0.18 %.4f,-0.04 Z"
             % (-0.52, -0.64, -0.50 + dx, -0.30 + dx, 0.0 + dx, 0.30 + dx, 0.50 + dx, 0.64, 0.52,
                0.46, 0.30 + dx, 0.12 + dx, -0.02 + dx, -0.16 + dx, -0.32 + dx, -0.46, -0.52))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, col, k.ink))
        o.append('<path d="M%.4f,-0.70 Q%.4f,-0.80 %.4f,-0.72" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>' % (-0.28 + dx, -0.06 + dx, 0.18 + dx, hl))
        ytop = -0.88
    o.append(_hat_chips(k, C, yaw, ytop, -0.22))
    CE._ext(k, C, ((-0.58, -0.2), (0.58, -0.2), (0.0, ytop)))
    return "".join(o), (0.0, ytop)


def _hat_cap15(k, C, yaw):
    """baseball-style cap, plain (no letters): a domed crown in six panels, a button, a curved peak that swings to the facing
    side when the head turns.  hat_colors: crown / crown_l / crown_d / visor / visor_d / button."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    fx = 0.16 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    cr = dict(light=col["crown_l"], base=col["crown"], dark=col["crown_d"])
    g = CE._gradient(k, "cp", cr, x0=-0.55, x1=0.55, mid=0.34)
    yb = -0.27
    dome = "M%.4f,%.4f C%.4f,-0.58 %.4f,-0.72 %.4f,-0.72 C%.4f,-0.72 %.4f,-0.58 %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.50, yb, dx - 0.52, dx - 0.30, dx, dx + 0.30, dx + 0.52, dx + 0.50, yb, dx, yb + 0.07, dx - 0.50, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (dome, g, k.ink))
    for s in (-1, 1):
        o.append('<path d="M%.4f,-0.70 Q%.4f,-0.50 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>' % (dx, dx + s * 0.30 + fx * 0.3, dx + s * 0.40 + fx * 0.2, yb, k.c(col["crown_d"])))
    o.append('<circle cx="%.4f" cy="-0.72" r="0.034" fill="%s" stroke="%s" stroke-width="0.014"/>' % (dx, k.c(col.get("button", col["crown_d"])), k.ink))
    o.append('<path d="M%.4f,-0.62 Q%.4f,-0.70 %.4f,-0.69" fill="none" stroke="#ffffff" stroke-width="0.016" stroke-linecap="round" opacity="0.4"/>' % (dx - 0.34, dx - 0.22, dx - 0.08))
    # peak
    pw = 0.52 - 0.12 * abs(yaw)
    vis = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        fx - pw, yb + 0.005, fx, yb + 0.07, fx + pw, yb + 0.005, fx + pw * 0.95 + 0.28 * yaw, yb + 0.15, fx + 0.30 * yaw, yb + 0.17, fx - pw * 0.95 + 0.28 * yaw, yb + 0.15, fx - pw, yb + 0.005)
    gv = CE._gradient(k, "cv", dict(light=col["visor"], base=col["visor"], dark=col["visor_d"]), x0=-0.5, x1=0.5, mid=0.3)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (vis, gv, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="#ffffff" stroke-width="0.012" stroke-linecap="round" opacity="0.35"/>' % (fx - pw * 0.6, yb + 0.09, fx - 0.1, yb + 0.12, fx + 0.1, yb + 0.12))
    o.append(_hat_chips(k, C, yaw, -0.70, yb))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.52, yb), (dx + 0.52, yb), (dx, -0.74), (fx - pw, yb + 0.15), (fx + pw + 0.28 * yaw, yb + 0.17)))
    ho = _POSE15["hat_off"]
    if ho > 0.02:       # the cap flying off: lifted up and away, tumbling
        o.insert(0, '<g transform="translate(%.3f %.3f) rotate(%.1f)">' % (-0.45 * ho, -0.95 * ho, 55.0 * ho))
        o.append('</g>')
        k.ext.append((-0.45 * ho, -1.6 * ho, 0.5))
    return "".join(o), (dx, -0.74)


def _hat_tourist15(k, C, yaw):
    """the stands hat: a floppy cream hat with a wide brim, a red band and a striped pennant on a stick (stripes only: no
    letters, no flag).  hat_colors: light / base / dark (hat), band, pen1 / pen2 (pennant stripes)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    g = CE._gradient(k, "tt", col, x0=-0.6, x1=0.6, mid=0.34)
    yb = -0.30
    # pennant stick + pennant first (behind the crown)
    sx = dx - 0.14
    o.append('<path d="M%.4f,-0.55 L%.4f,-1.04" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (sx, sx + 0.04, k.ink))
    o.append('<path d="M%.4f,-0.55 L%.4f,-1.04" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (sx, sx + 0.04, k.c("#e8d8b0")))
    # a pennant: a long triangle flying to the right with three stripes
    px, py = sx + 0.04, -1.03
    stripes = [(0.00, col["pen1"]), (0.33, col["pen2"]), (0.66, col["pen1"])]
    tip = (px + 0.62, py + 0.14)
    for i, (f0, cc) in enumerate(stripes):
        a0 = (px, py + 0.0 + 0.20 * f0)
        a1 = (px, py + 0.20 * (f0 + 0.34))
        b0 = (px + (tip[0] - px) * (f0 + 0.0), a0[1] + (tip[1] - a0[1]) * (f0 + 0.0) * 0)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="none"/>' % (px, py + 0.20 * f0, px, py + 0.20 * (f0 + 0.34), tip[0], tip[1], k.c(cc)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="none" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (px, py, px, py + 0.20, tip[0], tip[1], k.ink))
    # crown
    crown = "M%.4f,%.4f C%.4f,-0.52 %.4f,-0.66 %.4f,-0.66 C%.4f,-0.66 %.4f,-0.52 %.4f,%.4f Z" % (dx - 0.40, yb, dx - 0.42, dx - 0.24, dx, dx + 0.24, dx + 0.42, dx + 0.40, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (crown, g, k.ink))
    # brim
    brim = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (
        dx - 0.76, yb + 0.04, dx, yb - 0.10, dx + 0.76, yb + 0.04, dx + 0.50, yb + 0.20, dx, yb + 0.15, dx - 0.50, yb + 0.20, dx - 0.76, yb + 0.04)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (brim, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (dx - 0.405, yb - 0.10, dx, yb - 0.06, dx + 0.405, yb - 0.10, dx + 0.41, yb - 0.02, dx, yb + 0.03, dx - 0.41, yb - 0.02, k.c(col["band"]), k.ink))
    o.append(_hat_chips(k, C, yaw, -0.64, yb))
    o.append('</g>')
    C4._ext_hat(k, C, ((dx - 0.78, yb + 0.1), (dx + 0.78, yb + 0.1), (dx, -0.68), (px, py), (tip[0], tip[1])))
    return "".join(o), (dx, -1.05)


HATS15 = {"hair15": _hat_hair15, "cap15": _hat_cap15, "tourist15": _hat_tourist15}


# ============================================================================= socks and shoes (legs)
def _shoe(k, E, A, T, w, SH):
    """sock + shoe at the ankle A (knee E, toe stub end T).  Drawn in a frame whose +y runs down the shin, so it still sits right
    when the leg hangs or kicks.  kind: sneaker / spike / dress.  Keys: sock (colour or None), sock_stripe, sock_len, color, toe, sole, stripe."""
    dx, dy = A[0] - E[0], A[1] - E[1]
    dl = math.hypot(dx, dy) or 1.0
    ang = math.degrees(math.atan2(dy, dx)) - 90.0
    ca, sa = math.cos(math.radians(-ang)), math.sin(math.radians(-ang))
    tx, ty = T[0] - A[0], T[1] - A[1]
    lx = tx * ca - ty * sa
    s = 1.0 if lx >= 0 else -1.0
    kind = SH.get("kind", "sneaker")
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f)">' % (A[0], A[1], ang)]
    sole = w / 2 + 0.008
    if SH.get("sock"):
        sl = SH.get("sock_len", 0.26)
        sw = w + 0.040
        o.append('<path d="M0,%.4f L0,0.01" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % (-sl, k.ink, sw + 0.026))
        o.append('<path d="M0,%.4f L0,0.01" stroke="%s" stroke-width="%.4f" stroke-linecap="butt"/>' % (-sl + 0.008, k.c(SH["sock"]), sw))
        if SH.get("sock_stripe"):
            for j, yy in enumerate((-sl + 0.04, -sl + 0.085)):
                o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018"/>' % (-sw / 2, yy, sw / 2, yy, k.c(SH["sock_stripe"] if j == 0 else SH.get("sock_stripe2", SH["sock_stripe"]))))
    col = k.c(SH["color"])
    hgt = 0.12 if kind == "dress" else 0.085
    hw = w / 2 + 0.030
    toe = SH.get("toe", 0.20)
    heel = -s * (hw + 0.030)
    tip = s * (hw + toe)
    pts = [(-s * hw, -hgt), (s * hw * 0.9, -hgt), (s * (hw + 0.02), -0.02), (tip - s * 0.06, sole - 0.080), (tip, sole - 0.040), (tip, sole), (heel, sole), (heel - s * 0.008, -0.01)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), col, k.ink))
    # sole
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (heel, sole + 0.004, tip, sole + 0.004, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (heel + s * 0.004, sole + 0.004, tip - s * 0.004, sole + 0.004, k.c(SH.get("sole", "#f2efe6"))))
    if kind == "sneaker":
        # toe cap + laces + side stripe
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % (tip - s * 0.10, sole - 0.015, tip - s * 0.09, sole - 0.060, tip - s * 0.03, sole - 0.040, k.ink))
        for j in range(3):
            xx = s * (0.00 + 0.035 * j)
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round"/>' % (xx - 0.012, -hgt + 0.012 + 0.012 * j, xx + 0.012, -hgt + 0.030 + 0.012 * j))
        if SH.get("stripe"):
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>' % (heel + s * 0.03, sole - 0.035, s * 0.02, -hgt + 0.03, k.c(SH["stripe"])))
    elif kind == "spike":
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (-s * 0.02, -hgt + 0.02, s * 0.12, sole - 0.05, k.c(SH.get("stripe", "#ffffff"))))
        for j in range(4):
            xx = heel + s * 0.04 + (tip - heel - s * 0.08) * j / 3.0
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.006"/>' % (xx - 0.014, sole + 0.010, xx + 0.014, sole + 0.010, xx, sole + 0.050, k.c("#c9ced4"), k.ink))
    o.append('</g>')
    k.ext.append((A[0] + (tip) * 1.0, A[1] + sole, 0.04))
    k.ext.append((A[0] - heel, A[1] + sole, 0.04))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O15["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = CE._CUR[0]
    if C is None or not C.get("_cast15"):
        return out
    if tail is not None and C.get("shoe15"):
        out += _shoe(k, E, H, tail, w, C["shoe15"])
    return out


# ============================================================================= held props
NEW_PROPS15 = ("clipboard", "presscam", "paper15")
NEW_TIP15 = {"clipboard": 0.30, "presscam": 0.30, "paper15": 0.0}


PAPER_W, PAPER_H = 1.30, 0.95


def _paper15_body(k):
    """an open newspaper held wide in both hands (no letters): origin = the grip of the hand that holds the RIGHT edge, the page
    extends toward -x (the other hand holds the left edge) and from -0.5 to +0.45 in y.  A big halftone photo of the arched
    jumper (a grey flop silhouette over a pale pit) and grey column bars."""
    w, h = PAPER_W, PAPER_H
    x0, y0 = -w + 0.04, -h * 0.5
    o = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.012" fill="%s" stroke="%s" stroke-width="0.022"/>' % (x0, y0, w, h, k.c("#efe9da"), k.ink)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010"/>' % (x0 + w / 2, y0 + 0.02, x0 + w / 2, y0 + h - 0.02, k.c("#b8b2a2")))
    # headline bars
    for i, (wd, th) in enumerate(((0.80, 0.045), (0.55, 0.030))):
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s"/>' % (x0 + 0.08, y0 + 0.06 + 0.07 * i, wd, th, k.c("#4a4850")))
    # the photo
    px, py, pw, ph = x0 + 0.08, y0 + 0.23, 0.62, 0.40
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s" stroke="%s" stroke-width="0.014"/>' % (px, py, pw, ph, k.c("#c8c6c0"), k.ink))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" fill="%s"/>' % (px + 0.01, py + ph * 0.72, pw - 0.02, ph * 0.27, k.c("#a8a69e")))
    # bar and the flop silhouette (a round arch, head low on the right, legs hanging on the left)
    bx0, bx1, by = px + 0.05, px + pw - 0.05, py + ph * 0.46
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012"/>' % (bx0, by, bx1, by, k.c("#5a585e")))
    cx = px + pw * 0.5
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round" stroke-linejoin="round"/>'
             % (cx - 0.17, py + ph * 0.80, cx - 0.20, py + ph * 0.46, cx - 0.02, py + ph * 0.40, cx + 0.10, py + ph * 0.38, cx + 0.15, py + ph * 0.62, k.c("#3c3a40")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (cx - 0.17, py + ph * 0.80, cx - 0.27, py + ph * 0.90, k.c("#3c3a40")))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.040" fill="%s"/>' % (cx + 0.17, py + ph * 0.70, k.c("#3c3a40")))
    # column bars: under the photo on the left page, a full column of bars on the right page
    for i in range(3):
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.022" fill="%s"/>' % (x0 + 0.08, py + ph + 0.05 + 0.055 * i, 0.62 - (0.10 if i == 2 else 0.0), k.c("#8a8890")))
    for i in range(11):
        wd = 0.50 if i % 5 != 4 else 0.32
        o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.022" fill="%s"/>' % (x0 + w / 2 + 0.08, y0 + 0.07 + 0.070 * i, wd, k.c("#8a8890")))
    return "".join(o)


def _clipboard_body(k):
    """a board with a steel clip and a sheet with grey bars (no letters), held by the clip edge at (0, 0); extends along -y."""
    o = ['<rect x="-0.20" y="-0.58" width="0.40" height="0.54" rx="0.020" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c("#a87a46"), k.ink)]
    o.append('<rect x="-0.165" y="-0.52" width="0.33" height="0.46" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#f6f3ea"), k.ink))
    for i in range(6):
        wdt = 0.26 if i % 3 != 2 else 0.17
        o.append('<path d="M-0.125,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (-0.46 + 0.058 * i, -0.125 + wdt, -0.46 + 0.058 * i, k.c("#9aa0aa")))
    o.append('<rect x="-0.075" y="-0.62" width="0.15" height="0.065" rx="0.016" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#c9ced4"), k.ink))
    return "".join(o)


CAM_LENS = (0.34, 0.0)


def _presscam_body(k, flash):
    """1960s press camera seen from the side, pointing +x, held by the grip at (0, 0): a black box, a bellows and lens in front, a
    bracket on the left carrying a big round flash reflector with a bulb in it.  flash 0..1 draws the burst."""
    o = []
    o.append('<rect x="-0.16" y="-0.17" width="0.40" height="0.30" rx="0.026" fill="%s" stroke="%s" stroke-width="0.020"/>' % (k.c("#2c2a30"), k.ink))
    o.append('<rect x="-0.12" y="-0.14" width="0.32" height="0.07" rx="0.016" fill="%s" opacity="0.8"/>' % k.c("#6a6670"))
    o.append('<path d="M0.24,-0.12 L0.36,-0.07 L0.36,0.05 L0.24,0.10 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#4a4650"), k.ink))
    o.append('<rect x="0.35" y="-0.09" width="0.09" height="0.17" rx="0.020" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#aab2bc"), k.ink))
    o.append('<circle cx="0.44" cy="-0.005" r="0.052" fill="%s" stroke="%s" stroke-width="0.014"/><circle cx="0.445" cy="-0.01" r="0.026" fill="%s"/>' % (k.c("#2a3a5a"), k.ink, k.c("#9ec4ea")))
    # bracket and reflector (left / rear of the camera, up)
    o.append('<path d="M-0.10,-0.17 L-0.10,-0.34 L0.10,-0.40" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" stroke-linejoin="round"/>' % k.ink)
    o.append('<ellipse cx="0.14" cy="-0.44" rx="0.080" ry="0.150" transform="rotate(-18 0.14 -0.44)" fill="%s" stroke="%s" stroke-width="0.018"/>' % (k.c("#d8dce2"), k.ink))
    o.append('<ellipse cx="0.150" cy="-0.44" rx="0.045" ry="0.100" transform="rotate(-18 0.15 -0.44)" fill="%s"/>' % k.c("#f4f1e0" if flash < 0.1 else "#ffffff"))
    o.append('<circle cx="0.155" cy="-0.44" r="0.026" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#fff6c0" if flash < 0.1 else "#ffffff"), k.ink))
    return "".join(o)


def _flash_burst(k, cx, cy, lev):
    """a star burst: white core, 12 spikes, a halo; lev 0..1 grows and fades."""
    if lev < 0.02:
        return ""
    r = 0.12 + 0.34 * lev
    pts = []
    for i in range(24):
        a = 2 * math.pi * i / 24 + 0.1
        rr = r * (1.0 if i % 2 == 0 else 0.42)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    o = ['<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#fff8d0" opacity="%.3f"/>' % (cx, cy, r * 0.95, 0.45 * lev),
         '<path d="%s" fill="#ffffff" stroke="#ffe27a" stroke-width="0.02" stroke-linejoin="round"/>' % _poly_d(pts),
         '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff"/>' % (cx, cy, r * 0.33)]
    k.ext.append((cx, cy, r))
    return "".join(o)


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS15:
        return _O15["_prop"](k, kind, H, ang, sc)
    key = C8._side_key()
    an = C8._POSE8["an"]
    if kind == "clipboard":
        # held on the hip / in front: the board hangs from the hand, always upright-ish (angle rotates it)
        o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang + 90.0, sc, _clipboard_body(k))
        a = math.radians(ang + 90.0)
        for (x, y) in ((-0.2, -0.6), (0.2, -0.6), (-0.2, 0.0), (0.2, 0.0)):
            rx, ry = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
            k.ext.append((H[0] + rx * sc, H[1] + ry * sc, 0.03))
        tip = (H[0], H[1])
        an["board_" + key] = tip
        return o, tip
    if kind == "paper15":
        side = 1.0 if key == "r" else -1.0
        o = '<g transform="translate(%.4f %.4f) scale(%.4f 1)"><g transform="scale(%.4f %.4f)">%s</g></g>' % (H[0], H[1], 1.0, side * sc, sc, _paper15_body(k))
        for (x, y) in ((-PAPER_W, -PAPER_H / 2), (0.04, -PAPER_H / 2), (-PAPER_W, PAPER_H / 2), (0.04, PAPER_H / 2)):
            k.ext.append((H[0] + side * x * sc, H[1] + y * sc, 0.03))
        an["paper_" + key] = (H[0] - side * PAPER_W / 2 * sc, H[1])
        return o, (H[0], H[1])
    lev = _POSE15["flash"]
    o = '<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">%s</g>' % (H[0], H[1], ang, sc, _presscam_body(k, lev))
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)

    def tr(x, y):
        return (H[0] + (x * ca - y * sa) * sc, H[1] + (x * sa + y * ca) * sc)
    for (x, y) in ((-0.16, -0.17), (0.24, -0.17), (0.46, 0.0), (0.14, -0.62), (0.14, -0.30)):
        q = tr(x, y)
        k.ext.append((q[0], q[1], 0.03))
    ref = tr(0.15, -0.44)
    an["flash_" + key] = ref
    an["lens_" + key] = tr(0.45, 0.0)
    if lev > 0.02:
        o += _flash_burst(k, ref[0], ref[1], lev)
    return o, tr(0.45, 0.0)


# ============================================================================= cast
_FLAGS = dict(_cast15=True, _cast10=True, _cast9=True, _cast8=True, _cast7=True, _cast6=True, _cast4=True, _cast3=True)
HAIRS = dict(brown="#6a4226", dark="#2a2020", black="#1c1820", blond="#d9b25a", red="#b4552a", grey="#a9a7ad", white="#e8e6ea", chestnut="#7a4a2c")


def _slim(build, torso_w, torso_h, leg, **kw):
    d = dict(_FLAGS, build=build, torso_w=torso_w, torso_h=torso_h, profile=CE.PROFILE_ATHLETE, shift_pow=1.0, shoulder=(0.24, 0.50),
             arm=0.76, hip_x=0.15, leg=leg, stance=0.07, wide=0.26, limb_w=0.056, eye_y=0.030, brow="stroke", brow_th=0.056, mouth="smirk",
             moustache=False, smirk_side=1, hat="newsboy", ear_pencil=False, cheeks="#eca090")
    d.update(kw)
    return d


def _hair(col, shine=None):
    return dict(color=HAIRS.get(col, col), front=0.06, grow=0.20, **({"shine": shine} if shine else {}))


SCHOOL = dict(base="#7a1f33", trim="#e2b442", s1="#e2b442", s2=None, hem="#e2b442", pants="#f4f2ee")
OLYMP = dict(base="#f6f4ee", trim="#1e2a5a", s1="#c8302a", s2="#2a4a9a", hem=None, pants="#1e2a5a", edge="#1e2a5a")
SNEAK = dict(kind="sneaker", color="#f2efe6", sole="#e6dcc6", stripe="#7a1f33", sock="#f6f4ee", sock_stripe="#7a1f33", sock_stripe2="#e2b442", sock_len=0.30, toe=0.22)
SPIKE = dict(kind="spike", color="#f6f4ee", sole="#2a2a30", stripe="#c8302a", sock="#f6f4ee", sock_len=0.22, toe=0.20)


def _sleeve(col, dark=None, ln=0.16, w=0.17):
    return dict(color=col, dark=dark or _shade(col, 0.72), cuff=col, len=ln, w=w)


def _shorts(col, ln=0.34, w=0.15):
    return dict(color=col, dark=_shade(col, 0.72), cuff=col, len=ln, w=w)


def _vest_cast(seed, torso_w, torso_h, leg, hair_col, hair_style, vest, shoe, skin="fair", hat_hair=None, **kw):
    sl = _sleeve(vest["base"], ln=0.07, w=0.13)
    d = _slim("slim", torso_w, torso_h, leg, seed=seed, costume="vest15", hat_style="hair15", hair_style15=hair_style, hair=_hair(hair_col),
              colors=dict(vest, moustache="#3a2620"), sleeve=sl, shorts=_shorts(vest["pants"], 0.26, 0.15 + 0.02 * torso_w),
              shoe15=dict(shoe), skin15=skin, hat_tilt=0.0, hat_colors=dict(light="#fff", base="#fff", dark="#ccc"), **kw)
    return d


NEW_CAST15 = {
    # Dick Fosbury: the tallest of the cast, lanky, long limbs, big ears, short tousled brown hair, friendly face
    "dick": _vest_cast(15.3, 0.56, 1.04, 1.86, "brown", "tousle", SCHOOL, SNEAK, ears15=1.0, brow="dome", brow_th=0.044, mouth="smile", limb_w=0.050, eye_y=0.020),
    # the veteran coach: stocky, belly, grey crew cut, big jaw, cap, maroon windbreaker with lanyards (whistle + stopwatch)
    "coach": dict(
        _FLAGS, build="stout", seed=63.1, torso_w=1.52, torso_h=1.14, profile=C10.C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.46, 0.44), arm=0.74, hip_x=0.20, leg=0.98, stance=0.07, wide=0.32, limb_w=0.072,
        eye_y=0.010, brow="stroke", brow_th=0.090, mouth="frown", moustache=False, smirk_side=1, cheeks="#ee8a78", chins=True,
        hat="newsboy", hat_style="cap15", hat_tilt=-3.0, ear_pencil=False, jaw15=1.0, ears15=0.7,
        hat_colors=dict(crown="#7a1f33", crown_l="#a8394a", crown_d="#4a1020", visor="#4a1020", visor_d="#2a0a14", button="#e2b442"),
        hair=dict(color="#a9a7ad", front=0.07, grow=0.22),
        costume="jacket15",
        sleeve=dict(color="#7a1f33", dark="#4a1020", cuff="#e2b442", len=0.86, w=0.20),
        shorts=dict(color="#3a3a44", dark="#26262e", cuff="#3a3a44", len=0.9, w=0.19),
        shoe15=dict(kind="dress", color="#2a2430", sole="#16141a", sock="#e8e4dc", sock_len=0.14, toe=0.20),
        colors=dict(base="#7a1f33", dark="#5a1426", trim="#e2b442", zip="#d8d4cc", collar="#6a1a2c", pants="#3a3a44"),
    ),
    "boy1": _vest_cast(21.7, 0.58, 0.98, 1.34, "chestnut", "crew", dict(SCHOOL, base="#1e2f6a", trim="#f4f2ee", s1="#f4f2ee", hem="#f4f2ee", pants="#f4f2ee"), dict(SNEAK, stripe="#1e2f6a", sock_stripe="#1e2f6a", sock_stripe2="#f4f2ee"), mouth="grin"),
    "boy2": _vest_cast(33.9, 0.62, 1.00, 1.46, "black", "curly", dict(SCHOOL, base="#2a5a8a", trim="#f4f2ee", s1="#f4f2ee", hem="#f4f2ee", pants="#e8e4dc"), dict(SNEAK, stripe="#2a5a8a", sock_stripe="#2a5a8a", sock_stripe2="#f4f2ee"), skin="brown", eye_y=0.040),
    "boy3": _vest_cast(47.2, 0.56, 0.94, 1.24, "blond", "quiff", dict(SCHOOL, base="#2f7a4a", trim="#f4f2ee", s1="#f4f2ee", hem="#f4f2ee", pants="#f4f2ee"), dict(SNEAK, stripe="#2f7a4a", sock_stripe="#2f7a4a", sock_stripe2="#f4f2ee"), skin="ruddy", brow="dome", brow_th=0.040, cheeks="#f08a78"),
    # Olympic jumpers: plain kits of different colours, spikes, taller and leaner
    "rival1": _vest_cast(52.4, 0.60, 1.02, 1.62, "dark", "crew", dict(base="#c8302a", trim="#f6f4ee", s1=None, s2=None, hem=None, pants="#c8302a"), dict(SPIKE), skin="tan", mouth="dash", eye_y=0.040),
    "rival2": _vest_cast(61.8, 0.62, 1.04, 1.70, "red", "quiff", dict(base="#2a8a6a", trim="#f6f4ee", s1=None, s2=None, hem=None, pants="#2a8a6a"), dict(SPIKE, stripe="#f6f4ee"), skin="ruddy", mouth="dash"),
    "rival3": _vest_cast(74.5, 0.60, 1.00, 1.56, "black", "curly", dict(base="#e8a82a", trim="#2a2a30", s1=None, s2=None, hem=None, pants="#2a2a30"), dict(SPIKE, stripe="#e8a82a"), skin="dark", mouth="dash", eye_y=0.040),
    # 1968 officials: blazers and ties
    "official1": dict(
        _FLAGS, build="regular", seed=82.2, torso_w=0.88, torso_h=1.02, profile=C10.C2.PROFILE_ROUND, shift_pow=1.05,
        shoulder=(0.32, 0.48), arm=0.74, hip_x=0.15, leg=1.30, stance=0.06, wide=0.26, limb_w=0.062,
        eye_y=0.020, brow="stroke", brow_th=0.070, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=0.7, smirk_side=-1, cheeks="#e48a7a",
        hat="newsboy", hat_style="hair15", hair_style15="crew", hat_tilt=0.0, ear_pencil=False, hair=_hair("grey"),
        costume="blazer15", sleeve=dict(color="#1f3a5a", dark="#142640", cuff="#1f3a5a", len=0.88, w=0.17),
        shorts=dict(color="#6a6a72", dark="#4a4a52", cuff="#6a6a72", len=0.9, w=0.15),
        shoe15=dict(kind="dress", color="#2a2430", sole="#16141a", toe=0.18), ears15=0.5,
        colors=dict(base="#1f3a5a", dark="#142640", lapel="#162c48", shirt="#f6f4ee", tie="#a8303a", pants="#6a6a72", button="#d8b44a", moustache="#8a8a92"),
    ),
    "official2": dict(
        _FLAGS, build="slim", seed=17.6, torso_w=0.66, torso_h=1.00, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=0.76, hip_x=0.15, leg=1.40, stance=0.07, wide=0.26, limb_w=0.056,
        eye_y=0.030, brow="stroke", brow_th=0.056, mouth="dash", moustache=False, smirk_side=1, cheeks="#eca090",
        hat="newsboy", hat_style="hair15", hair_style15="quiff", hat_tilt=0.0, ear_pencil=False, hair=_hair("#3a2a22"),
        costume="blazer15", sleeve=dict(color="#7a2a2a", dark="#521818", cuff="#7a2a2a", len=0.88, w=0.15),
        shorts=dict(color="#2a2a32", dark="#1a1a22", cuff="#2a2a32", len=0.9, w=0.14),
        shoe15=dict(kind="dress", color="#3a2a22", sole="#16141a", toe=0.18),
        colors=dict(base="#7a2a2a", dark="#521818", lapel="#5a1c1c", shirt="#f6f4ee", tie="#2a4a7a", pants="#2a2a32", button="#d8b44a"),
    ),
    # the press photographer: a flat cap, loosened tie, shirt sleeves, a press camera with a flash gun
    "photographer": dict(
        _FLAGS, build="regular", seed=90.4, torso_w=0.84, torso_h=0.98, profile=CE.PROFILE_PEAR, shift_pow=1.05,
        shoulder=(0.31, 0.48), arm=0.72, hip_x=0.15, leg=1.12, stance=0.06, wide=0.26, limb_w=0.060,
        eye_y=0.020, brow="stroke", brow_th=0.064, mouth="grin", moustache=True, moustache_style="bushy", tache_scale=0.5, smirk_side=1, cheeks="#ee8a78",
        hat="newsboy", hat_style="flatcap", hat_tilt=5.0, ear_pencil=False, hair=_hair("dark"),
        hat_colors=dict(light="#857262", base="#5e4c40", dark="#3c2f27", shine="#a99382", visor="#4a3b31"),
        costume="shirt15", sleeve=dict(color="#e8e4da", dark="#bfb9aa", cuff="#e8e4da", len=0.5, w=0.15, roll=True),
        shorts=dict(color="#4a4238", dark="#322c24", cuff="#4a4238", len=0.9, w=0.15),
        shoe15=dict(kind="dress", color="#2a2430", sole="#16141a", toe=0.18),
        colors=dict(base="#e8e4da", collar="#f4f1ea", tie="#3a4a6a", pants="#4a4238", moustache="#2a2020"),
    ),
}


def _crowd(seed, build, tw, th, leg, hat_style, hair_col, costume, colors, sleeve, skin="fair", hair_style="crew", **kw):
    d = dict(_FLAGS, build=build, seed=seed, torso_w=tw, torso_h=th, profile=CE.PROFILE_ATHLETE if build == "slim" else CE.PROFILE_PEAR, shift_pow=1.0,
             shoulder=(0.24, 0.50) if build == "slim" else (0.31, 0.48), arm=0.74, hip_x=0.15, leg=leg, stance=0.06, wide=0.26, limb_w=0.058, eye_y=0.030,
             brow="stroke", brow_th=0.056, mouth="smile", moustache=False, smirk_side=1, cheeks="#eca090", hat="newsboy", hat_style=hat_style,
             hair_style15=hair_style, hat_tilt=0.0, ear_pencil=False, hair=_hair(hair_col), costume=costume, colors=colors, sleeve=sleeve,
             shorts=_shorts("#4a4a56", 0.9, 0.15), shoe15=dict(kind="dress", color="#2a2430", sole="#16141a", toe=0.18), skin15=skin)
    d.update(kw)
    return d


NEW_CAST15.update({
    "crowd1": _crowd(11.1, "regular", 0.86, 0.98, 1.10, "cap15", "dark", "shirt15", dict(base="#3a7a9a", collar="#d8e8f0", pants="#4a4a56", stripe="#f4f2ee"),
                     _sleeve("#3a7a9a", ln=0.50, w=0.16), hat_tilt=4.0,
                     hat_colors=dict(crown="#2a3a6a", crown_l="#4a5a8a", crown_d="#161e3a", visor="#161e3a", visor_d="#0a1020", button="#e8e4dc")),
    "crowd2": _crowd(22.2, "slim", 0.62, 0.92, 1.12, "hair15", "chestnut", "shirt15", dict(base="#d8607a", collar="#f4e8ec", pants="#3a3a46"),
                     _sleeve("#d8607a", ln=0.5, w=0.15), hair_style="bouffant", cheeks="#f08a8a", brow="dome", brow_th=0.040, mouth="happy"),
    "crowd3": _crowd(33.3, "slim", 0.60, 0.92, 1.16, "hair15", "brown", "vest15", dict(base="#e8a82a", trim="#2a2a30", s1=None, s2=None, hem=None, pants="#3a3a46"),
                     _sleeve("#e8a82a", ln=0.5, w=0.16), hair_style="crew", skin="tan"),
    "crowd4": _crowd(44.4, "regular", 0.92, 1.00, 1.04, "fedora", "grey", "blazer15", dict(base="#5a4a3a", dark="#3a2e24", lapel="#4a3c30", shirt="#f4f1ea", tie="#2a5a4a", pants="#3a3a46", button="#d8b44a"),
                     _sleeve("#5a4a3a", ln=0.88, w=0.17), moustache=True, moustache_style="bushy", tache_scale=0.6,
                     hat_colors=dict(light="#dcb27a", base="#b8854c", dark="#7c5530", shine="#f1dcb2", band="#3b2a22", band_l="#5a4030", brim="#a77543", edge="#dcb985"), skin="ruddy", hat_tilt=-3.0),
    "crowd5": _crowd(55.5, "slim", 0.56, 0.84, 0.88, "hair15", "red", "shirt15", dict(base="#5aa0d8", collar="#f4f2ee", pants="#4a4a56", stripe="#f4f2ee"),
                     _sleeve("#5aa0d8", ln=0.5, w=0.14), hair_style="tousle", mouth="grin", eye_y=0.050, cheeks="#f2a294"),
    "crowd6": _crowd(66.6, "slim", 0.64, 0.94, 1.18, "kerchief", "black", "shirt15", dict(base="#8a5ab8", collar="#f0e8f6", pants="#3a3a46"),
                     _sleeve("#8a5ab8", ln=0.5, w=0.15), brow="dome", brow_th=0.040, skin="brown",
                     hat_colors=dict(light="#d8584a", base="#b8322a", dark="#7a1e18", dot="#f4e8d0")),
})


# costume variants (one CAST key per look)
NEW_CAST15["dick_olympic"] = dict(NEW_CAST15["dick"], colors=dict(OLYMP, moustache="#3a2620"), sleeve=_sleeve(OLYMP["base"], ln=0.07, w=0.13),
                                  shorts=_shorts(OLYMP["pants"], 0.26, 0.16), shoe15=dict(SPIKE, stripe="#c8302a"))
NEW_CAST15["coach_stands"] = dict(
    NEW_CAST15["coach"], costume="aloha15", hat_style="tourist15", hat_tilt=-4.0,
    hat_colors=dict(light="#f6eed6", base="#e8dcb4", dark="#b8a878", band="#c8302a", pen1="#c8302a", pen2="#f6f2e6"),
    colors=dict(base="#2aa89a", collar="#f6c83a", pants="#d8c8a0", flower="#ff5a6a", flower2="#ffd23a", centre="#8a2a1a", leaf="#1a6a4a"),
    sleeve=dict(color="#2aa89a", dark="#1a7a6e", cuff="#2aa89a", len=0.42, w=0.20),
    shorts=dict(color="#d8c8a0", dark="#b0a078", cuff="#d8c8a0", len=0.9, w=0.19), jaw15=1.0)
NEW_CAST15["coach"]["hair"] = dict(color="#a9a7ad", front=0.07, grow=0.22)
ALL15 = tuple(NEW_CAST15)


# ============================================================================= canvases (feet-relative, D; standing)
def _std_canvas(h):
    return (-2.125, -round((h + 0.75) * 16) / 16.0, 2.125, 0.125)


CANVAS15 = {}                  # filled in register() from the measured heights
CANVAS15_WIDE = (-4.25, -4.5, 4.25, 4.0)        # lying / bridge / straddle / sit / airborne poses (any member); place these by anchors, not by the soles


# ============================================================================= pose keys, skin, ears, jaw, mound
def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE15["sawdust"] = _f(g("sawdust"), 0.0, 0.0, 1.0)
    _POSE15["medal"] = _f(g("medal"), 0.0, 0.0, 1.0)
    _POSE15["hat_off"] = _f(g("hat_off"), 0.0, 0.0, 1.0)
    _POSE15["flash"] = _f(g("flash"), 0.0, 0.0, 1.0)
    t = _num(g("t"), 0.0)
    _POSE15["t"] = t if math.isfinite(t) else 0.0
    Pn = _O15["_norm"](C, pose)
    if C is not None and C.get("_cast15"):
        if g("body_lean") is not None:
            Pn["lean"] = _f(g("body_lean"), 0.0, -200.0, 200.0)
        if g("hdx2") is not None:
            Pn["head_dx"] = _f(g("hdx2"), 0.0, -4.0, 4.0)
        if g("hdy2") is not None:
            Pn["head_dy"] = _f(g("hdy2"), 0.0, -4.0, 4.0)
        if g("roll2") is not None:
            Pn["head_roll"] = _f(g("roll2"), 0.0, -200.0, 200.0)
        _POSE15["bend"] = _f(g("bend15"), 0.0, -90.0, 90.0)
        _POSE15["bend_y"] = _f(g("bend_y"), 0.6, 0.3, 0.9)
        _POSE15["roll"] = Pn["head_roll"]
        _POSE15["yaw"] = Pn["yaw"]
    return Pn


def _joint_y(C):
    return TT + _POSE15["bend_y"] * C["torso_h"]


def _rot_about(p, c, deg):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    dx, dy = p[0] - c[0], p[1] - c[1]
    return (c[0] + dx * ca - dy * sa, c[1] + dx * sa + dy * ca)


def _solve(C, Pn):
    """cast15 `bend15`: the torso is two segments; the lower one (hips) is rotated by bend15 degrees about the joint at
    TT + bend_y * torso_h, so the legs hang from the bent hips."""
    R = _O15["_solve"](C, Pn)
    b = _POSE15["bend"]
    if C is None or not C.get("_cast15") or abs(b) < 1e-6:
        return R
    T = R["T"]
    yB = R["yB"]
    m = R["m"]
    jt = T(0.0, _joint_y(C))
    hipx = C["hip_x"] * m.nf
    Lg = Pn["legs"]
    for q, sg in (("r", 1.0), ("l", -1.0)):
        S = _rot_about(T(sg * hipx, yB - 0.04), jt, b)
        tg = Lg["foot_" + q] if Lg["foot_" + q] is not None else R["legs"][q]["H"]
        E, A = P._ik(S, tg, C["leg"], R["legs"][q]["knee"])
        R["legs"][q] = dict(S=S, E=E, H=A, knee=R["legs"][q]["knee"], toe=R["legs"][q]["toe"])
    R["feet_y"] = max(R["legs"]["l"]["H"][1], R["legs"]["r"]["H"][1]) + Pn["limb_w"] / 2 + 0.008
    return R


def _head_behind(k, C, yaw, roll, mir, skin):
    """ears (CAST ears15 = size) and a heavy jaw (CAST jaw15) behind the head disc, in the head frame."""
    if mir:
        yaw, roll = -yaw, -roll
    o = []
    es = C.get("ears15", 0.0)
    if es > 0:
        for s in (-1, 1):
            vis = 1.0 - 0.80 * _smooth(0.05, 0.95, s * yaw)        # the ear on the side the face turns to goes behind the head
            if vis < 0.12:
                continue
            cx = s * (0.495 - 0.05 * _smooth(0.0, 1.0, s * yaw))
            rx, ry = 0.115 * es * vis, 0.165 * es
            o.append('<ellipse cx="%.4f" cy="0.030" rx="%.4f" ry="%.4f" transform="rotate(%.1f %.4f 0.03)" fill="%s" stroke="%s" stroke-width="0.030"/>'
                     % (cx, rx, ry, s * 12, cx, k.c(skin), k.ink))
            o.append('<path d="M%.4f,-0.020 Q%.4f,0.040 %.4f,0.100" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>'
                     % (cx + s * 0.01, cx + s * rx * 0.9, cx - s * 0.005, k.c(_shade(skin, 0.80))))
            k.ext.append(_rot(cx + s * rx, 0.03, roll) + (0.03,))
    jw = C.get("jaw15", 0.0)
    if jw > 0:
        w = 0.37 * jw + 0.0
        pts = [(-w, 0.20), (-w - 0.015, 0.50), (-w + 0.06, 0.60), (w - 0.06, 0.60), (w + 0.015, 0.50), (w, 0.20)]
        o.append('<path d="%s Z" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (P._smooth_open(pts), k.c(skin), k.ink))
        k.ext.append(_rot(0.0, 0.62, roll) + (0.1,))
    return '<g transform="rotate(%.2f)">%s</g>' % (roll, "".join(o)) if o else ""


def _mound(k, cx, ytop, ybot, w, seed, lev=1.0):
    """a heap of sawdust: a lumpy hill (cx, ytop .. ybot, half width w) with chips lying on it."""
    pts = [(cx - w, ybot)]
    n = 9
    for i in range(n + 1):
        t = i / float(n)
        x = cx - w * 0.92 + 1.84 * w * t
        h = (ybot - ytop) * (math.sin(math.pi * t) ** 0.4) * (0.92 + 0.12 * _hash(seed, i, 1.0))
        pts.append((x, ybot - h))
    pts.append((cx + w, ybot))
    d = P._smooth_open(pts[:-1]) + " L%.4f,%.4f Z" % (pts[-1][0], pts[-1][1])
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (d, k.c("#d6ae74"), k.ink)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.5"/>'
             % (cx + w * 0.1, ytop + 0.05, cx + w * 0.7, ytop + 0.25, cx + w * 0.98, ybot - 0.02, cx + w, ybot, cx + w * 0.25, ybot, k.c("#b8905a")))
    cp = []
    for i in range(46):
        x = cx + (_hash(seed, i, 2.0) * 2 - 1) * w * 0.92
        t = (x - (cx - w)) / (2 * w)
        top = ybot - (ybot - ytop) * (math.sin(math.pi * min(max(t, 0), 1)) ** 0.4)
        cp.append((x, top + (ybot - top) * (0.05 + 0.85 * _hash(seed, i, 3.0))))
    o.append(_chips(k, cp, seed + 1.0, 1.0, 0.07))
    k.ext.extend([(cx - w, ybot, 0.05), (cx + w, ybot, 0.05), (cx, ytop, 0.08)])
    return "".join(o)


def _bend_torso(svg, C, Pn, yaw, k, bend, byf, hw):
    """replace the torso group by two clipped copies: the upper segment as drawn, the lower one rotated by `bend` about the joint,
    plus a round cap in the costume colour that fills the wedge on the outer side of the bend."""
    start = '<g transform="translate(%.4f %.4f) rotate(%.4f)">' % (-Pn["head_dx"], -Pn["head_dy"], Pn["lean"])
    i = svg.find(start)
    if i < 0:
        return svg, ""
    depth, j = 0, i
    while j < len(svg):
        o, c = svg.find("<g", j), svg.find("</g>", j)
        if c < 0:
            return svg, ""
        if 0 <= o < c:
            depth += 1
            j = o + 2
        else:
            depth -= 1
            j = c + 4
            if depth == 0:
                break
    inner = svg[i + len(start):j - 4]
    ym = TT + byf * C["torso_h"]
    uid = k.uid
    cu, cl = uid + "_bu", uid + "_bl"
    defs = ('<clipPath id="%s"><rect x="-3" y="-3" width="6" height="%.4f"/></clipPath>'
            '<clipPath id="%s"><rect x="-3" y="%.4f" width="6" height="8"/></clipPath>' % (cu, ym + 0.05 + 3, cl, ym))
    r = hw * 0.97
    cap = ('<circle cx="0" cy="%.4f" r="%.4f" fill="%s"/><circle cx="0" cy="%.4f" r="%.4f" fill="%s"/>'
           % (ym, r + 0.03, P.INK, ym, r, k.c(C["colors"]["base"])))
    new = (start + cap + '<g clip-path="url(#%s)">%s</g>' % (cu, inner) +
           '<g transform="rotate(%.3f 0 %.4f)"><g clip-path="url(#%s)">%s</g></g></g>' % (bend, ym, cl, inner))
    return svg[:i] + new + svg[j:], defs



def figure(cast_name, pose=None, uid="p"):
    C = P.CAST.get(cast_name) if isinstance(cast_name, str) else None
    if C is None or not C.get("_cast15"):
        return _O15["figure"](cast_name, pose, uid)
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    sk = SKIN_TONES.get(C.get("skin15", "fair"), SKIN_TONES["fair"])
    old = (P.HEAD_FILL, P.HEAD_SHADE)
    P.HEAD_FILL, P.HEAD_SHADE = sk
    try:
        f = _O15["figure"](cast_name, pose, uid)
    finally:
        P.HEAD_FILL, P.HEAD_SHADE = old
    svg, bbox, an = f["svg"], list(f["bbox"]), dict(f["anchors"])
    k = P._Ctx(uid + "y", P.INK, None)
    bend = _f(g("bend15"), 0.0, -90.0, 90.0)
    byf = _f(g("bend_y"), 0.6, 0.3, 0.9)
    if abs(bend) > 1e-6:
        Pn = P._norm(C, pose or {})
        mm = P._TorsoMap(C, Pn["yaw"])
        svg, bdefs = _bend_torso(svg, C, Pn, Pn["yaw"], k, bend, byf, mm.hwa)
        if bdefs:
            svg = svg.replace("</defs>", bdefs + "</defs>", 1)
    mir = bool(g("mirror"))
    yaw = _f(g("yaw"), 0.0, -1.2, 1.2)
    roll = _f(g("roll2") if g("roll2") is not None else g("head_roll"), 0.0, -200.0, 200.0)
    pre = []
    hb = _head_behind(k, C, yaw, roll, mir, sk[0])
    if hb:
        pre.append('<g transform="translate(0 0)">%s</g>' % hb)
    bur = _f(g("buried"), 0.0, 0.0, 1.0)
    if bur >= 0.5:
        cx = _num(g("buried_x"), an["feet"][0] if "feet" in an else 0.0)
        ytop = _f(g("buried_y"), 0.62, -1.0, 4.0)
        w = _f(g("buried_w"), 1.5, 0.5, 5.0)
        yb = f["feet_y"] + 0.12
        pre.append(_mound(k, cx, ytop, yb, w, C["seed"]))
        bbox[0], bbox[2] = min(bbox[0], cx - w), max(bbox[2], cx + w)
        bbox[3] = max(bbox[3], yb + 0.05)
    if pre:
        marker = '<g transform="translate(%.4f %.4f)"><path d=' % P.FC
        i = svg.find(marker)
        extra = "".join(pre)
        if i < 0:
            i = svg.find("</defs>") + 7
        svg = svg[:i] + extra + svg[i:]
        if k.defs:
            svg = svg.replace("</defs>", "".join(k.defs) + "</defs>", 1)
    # thumbs up (pose thumb_r / thumb_l): an ink thumb standing on the hand of that limb
    th = []
    for key in ("r", "l"):
        if g("thumb_" + key):
            an_key = "hand_" + (("l" if key == "r" else "r") if mir else key)
            hx, hy = an[an_key]
            ang = _f(g("thumb_angle"), -90.0, -180.0, 180.0)
            th.append('<g transform="translate(%.4f %.4f) rotate(%.1f)"><path d="M0.03,0 L0.17,0" stroke="%s" stroke-width="0.100" stroke-linecap="round"/>'
                      '<path d="M0.04,0 L0.16,0" stroke="%s" stroke-width="0.040" stroke-linecap="round"/></g>' % (hx, hy, ang, P.INK, sk[0]))
            bbox[0], bbox[1], bbox[2], bbox[3] = min(bbox[0], hx - 0.2), min(bbox[1], hy - 0.25), max(bbox[2], hx + 0.2), max(bbox[3], hy + 0.1)
    if th:
        j = svg.rfind("</g>")
        svg = svg[:j] + "".join(th) + svg[j:]
    # the bar anchors.  apex = the highest point of the back (the outer edge of the bend); bar = the bar position: 0.13 D below the
    # underside of the back at the apex, so a visible gap of air stays between the back and the crossbar line.
    lean = _f(g("body_lean") if g("body_lean") is not None else g("lean"), 0.0, -200.0, 200.0)
    hdx_, hdy_ = _num(g("hdx2"), _num(g("head_dx"), 0.0)), _num(g("hdy2"), _num(g("head_dy"), 0.0))
    Gm = _geom(C, lean, yaw, hdx_, hdy_, bend, byf)
    hwv = P._TorsoMap(C, yaw).hwa
    th_ = math.radians(lean)
    au = (-math.sin(th_), math.cos(th_))                       # head -> joint direction
    tl = math.radians(lean + bend)
    al = (-math.sin(tl), math.cos(tl))                         # joint -> hips direction
    px, py = -(au[1] + al[1]), (au[0] + al[0])                # bisector of the two perpendiculars
    nl = math.hypot(px, py) or 1.0
    nx, ny = px / nl, py / nl
    if ny < 0:
        nx, ny = -nx, -ny
    jt = Gm["jt"]
    apex = (jt[0], jt[1] - hwv)                                 # top of the round back (the cap over the joint)
    k_ = hwv / max(0.5, math.cos(math.radians(abs(bend)) / 2.0))   # the inner corner of the bend lies further out than hw
    under = (jt[0] + nx * k_, jt[1] + ny * k_)
    bar = (under[0], under[1] + 0.13)
    hip = Gm["hc"]
    if mir:
        apex, bar, hip = (-apex[0], apex[1]), (-bar[0], bar[1]), (-hip[0], hip[1])
    an["apex"], an["bar"], an["hip"] = apex, bar, hip
    bob = _f(g("bob"), 0.0, -0.5, 0.5)
    if abs(bob) > 1e-6:
        svg = '<g transform="translate(0 %.4f)">%s</g>' % (-bob, svg)
        bbox[1] -= max(bob, 0.0)
        bbox[3] += max(-bob, 0.0)
        an = dict((n, (v[0], v[1] - bob) if n not in ("feet",) and not n.startswith(("foot", "knee")) else v) for n, v in an.items())
    return dict(f, svg=svg, bbox=tuple(bbox), anchors=an)


# ============================================================================= registration
STORY15, STORY15_META = {}, {}


def register():
    if getattr(P, "_cast15_registered", False):
        CE.register_stage()
        if not STORY15:
            _fill_story()
        return
    for name in ("_prop", "_norm", "_ink_limb", "figure", "_solve"):
        _O15[name] = getattr(P, name)
    P._prop = _prop
    P._norm = _norm
    P._ink_limb = _ink_limb
    P.figure = figure
    P._solve = _solve
    CE.COSTUMES.update(COSTUMES15)
    CE.HATS.update(HATS15)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS15 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP15)
    for n, c in NEW_CAST15.items():
        P.CAST[n] = c
    for n in ALL15:
        f = P.figure(n, {}, "h")
        CANVAS15[n] = _std_canvas(f["feet_y"] + 0.51)
    CE.CANVAS.update(CANVAS15)
    P._cast15_registered = True
    _fill_story()
    P.STORY.update(STORY15)
    CE.register_stage()


def _fill_story():
    for name, (cast, pose, note, lip) in _STORY_DEFS().items():
        STORY15[name] = (cast, pose)
        STORY15_META[name] = dict(note=note, **({"lipsync": True} if lip else {}))



# ============================================================================= pose builder
# Poses are authored for a figure travelling / facing screen-RIGHT (canonical).  facing=-1 adds mirror=True (as cast6.cycle()).
# The builder places limbs in polar form relative to the shoulders / hips of the cast being drawn, so one preset fits every
# member whatever its limb length:  arm=(angle deg, reach, bend)  leg=(angle deg, reach, knee)
#   angle: SVG angle of the limb from its root (0 = screen-right, 90 = down, -90 = up, 180 = left); reach: 0..1.15 of the limb length;
#   bend / knee: elbow bend -1..1 / knee direction -1..1 (+1 = knee toward +x).
def _geom(C, lean, yaw, hdx, hdy, bend=0.0, byf=0.6):
    m = P._TorsoMap(C, yaw)
    a = math.radians(lean)
    cl, sl = math.cos(a), math.sin(a)

    def T(x, y):
        return (x * cl - y * sl - hdx, x * sl + y * cl - hdy)
    yB = TT + C["torso_h"]
    sx, sy = C["shoulder"]
    sxa = sx * m.nf
    hipx = C["hip_x"] * m.nf
    jt = T(0.0, TT + byf * C["torso_h"])
    if abs(bend) > 1e-9:
        Hr, Hl, hc = (_rot_about(T(hipx, yB - 0.04), jt, bend), _rot_about(T(-hipx, yB - 0.04), jt, bend), _rot_about(T(0.0, yB - 0.04), jt, bend))
    else:
        Hr, Hl, hc = T(hipx, yB - 0.04), T(-hipx, yB - 0.04), T(0.0, yB - 0.04)
    return dict(S={"r": T(sxa, sy), "l": T(-sxa, sy)}, H={"r": Hr, "l": Hl}, hc=hc, T=T, yB=yB, jt=jt)


def _pol(root, ang, reach, length):
    a = math.radians(ang)
    return (root[0] + math.cos(a) * reach * length, root[1] + math.sin(a) * reach * length)


def J(cast, lean=0.0, yaw=0.0, roll=0.0, hdx=0.0, hdy=0.0, arm_r=None, arm_l=None, leg_r=None, leg_l=None, legs=None, bend=0.0, bend_y=0.6, **kw):
    """build a pose dict for `cast` (see above).  arm_* / leg_* tuples are polar, a dict/str is passed through (presets etc.)."""
    C = P.CAST[cast]
    G = _geom(C, lean, yaw, hdx, hdy, bend, bend_y)
    p = dict(yaw=yaw, body_lean=lean, roll2=roll, hdx2=hdx, hdy2=hdy)
    if abs(bend) > 1e-9:
        p["bend15"], p["bend_y"] = bend, bend_y
    for key, spec in (("r", arm_r), ("l", arm_l)):
        if spec is None:
            continue
        if isinstance(spec, tuple):
            ang, rc = spec[0], spec[1]
            bend = spec[2] if len(spec) > 2 else None
            d = dict(hand=_pol(G["S"][key], ang, rc, 0.74 * C["arm"] / 0.76), stretch=1.0)
            if bend is not None:
                d["bend"] = bend
            if len(spec) > 3:
                d.update(spec[3])
            p["arm_" + key] = d
        else:
            p["arm_" + key] = spec
    if legs is not None:
        p["legs"] = legs
    else:
        d = {}
        for key, spec in (("r", leg_r), ("l", leg_l)):
            if spec is None:
                continue
            ang, rc = spec[0], spec[1]
            d["foot_" + key] = _pol(G["H"][key], ang, rc, C["leg"])
            d["knee_" + key] = spec[2] if len(spec) > 2 else 0.8
            if len(spec) > 3:
                d["toe_" + key] = spec[3]
        if d:
            d["preset"] = "stand"
            p["legs"] = d
    p.update(kw)
    return p


def flip(pose):
    """a canonical (right-facing) pose as left-facing: mirror=True toggled (the same thing cycle(..., facing=-1) does)."""
    q = dict(pose)
    q["mirror"] = not bool(pose.get("mirror", False))
    return q


def pose_for(name, cast, facing=1, **over):
    """pose preset `name` (see POSE_NAMES) built for `cast`; facing +1 = screen-right, -1 = screen-left; keyword arguments override keys."""
    p = POSE_FUNCS[name](cast)
    p.update(over)
    return flip(p) if facing < 0 else p


# ============================================================================= the pose library
OPEN_WIDE = ("open", 0.30, 0.22)
OPEN_O = ("open", 0.20, 0.20)
BACK = dict(layer="back")
TOP = dict(layer="top")
PT = dict(shape="point")
OP = dict(shape="open")


def _legs_seat(L=None):
    return None


def _p_rock(a):
    def f(c):
        s = 1 if a else -1
        return J(c, lean=3 * s, yaw=0.55, roll=2 * s, expr="determined", gaze=(0.6, 0),
                 arm_r=(78 + 14 * s, 0.95, 0.4), arm_l=(104 - 14 * s, 0.95, 0.4, BACK),
                 legs=dict(preset="stand", crouch=0.10 + 0.08 * (1 if a else 0), spread=0.10, lift_r=0.0 if a else 0.22, lift_l=0.22 if a else 0.0), t=0.0)
    return f


def _p_plant(c):
    return J(c, lean=-13, yaw=0.45, roll=-4, expr="determined", arm_r=(150, 0.95, 0.5, BACK), arm_l=(40, 0.9, 0.6),
             leg_r=(58, 1.0, 0.4), leg_l=(118, 0.85, -0.6), gaze=(0.5, 0))


def _p_takeoff(c):
    return J(c, lean=-6, yaw=0.15, roll=0, expr="determined", arm_r=(-55, 1.05, -0.8), arm_l=(-115, 1.0, -0.8, BACK),
             leg_l=(95, 1.0, 0.1), leg_r=(38, 0.70, 1.0), gaze=(0.3, -0.4), hdy=0.0)


def _p_flop_rise(c):
    return J(c, lean=48, yaw=-0.1, roll=26, expr="determined", arm_r=(-35, 1.0, -0.5), arm_l=(-85, 1.0, -0.5, BACK),
             leg_l=(104, 1.0, 0.3), leg_r=(62, 0.82, 1.0))


def _arch(c, lean, hdx, hdy, roll, ang, depth, kn=-1, spread=12, bend=-48, by=0.55, **kw):
    """the flop family: a two-segment torso (upper back / chest fixed to the head at `lean`, lower back rotated by `bend`
    degrees about the joint), so the back is a round arch; head joined to the shoulders (hdx2 / hdy2 = small overlap), face
    turned toward the feet; thighs go down and out, shins hang (knees bent, kn -1 = knees toward the approach side).
    depth = how far the feet hang below the hips (D), ang = thigh direction (90 = straight down, 180 = straight back)."""
    L = P.CAST[c]["leg"]
    r = min(1.05, depth / (L * max(0.2, math.sin(math.radians(ang)))))
    p = J(c, lean=lean, yaw=-0.9, roll=roll, hdx=hdx, hdy=hdy, bend=bend, bend_y=by, expr="determined", arm_r=(92, 0.95, 0.3), arm_l=(110, 0.95, 0.3, BACK),
          leg_l=(ang, r, kn), leg_r=(ang - spread, r, kn))
    p.update(kw)
    return p


def _p_flop_head(c):      # head and shoulders already past the bar (hanging low), hips rising, legs trailing nearly straight
    return _arch(c, 128, 0.05, 0.22, 16, 122, 1.8, -0.5, 10, bend=-32, by=0.5)


def _p_flop_back(c):      # the arch almost complete, knees starting to bend
    return _arch(c, 152, 0.05, 0.24, 18, 112, 1.6, -0.7, 12, bend=-55, by=0.5)


def _p_flop(c):           # THE FLOP: a round upside-down U, belly up
    return _arch(c, 165, 0.05, 0.25, 20, 128, 1.4, -1, 16, bend=-70, by=0.45)


def _p_flop_flick(c):     # legs kicked up and over: jack-knife into an L
    return J(c, lean=140, yaw=-0.9, roll=16, hdx=0.05, hdy=0.2, bend=-42, bend_y=0.5, expr="happy", arm_r=(94, 0.95, 0.3), arm_l=(112, 0.95, 0.3, BACK),
             leg_l=(-112, 1.05, 0.0), leg_r=(-96, 1.05, 0.0))


def _p_land_back(c):      # on the back, knees up, arms flung out, a little bounce (torso slightly raised)
    return J(c, lean=84, yaw=-0.9, roll=80, expr="shocked", mouth="o", arm_r=(-75, 1.0, -0.4), arm_l=(112, 1.0, 0.4, BACK),
             leg_l=(-38, 0.62, -1.0), leg_r=(-62, 0.66, -1.0), sawdust=0.5)


def _p_lie_back(c):
    return J(c, lean=91, yaw=-0.9, roll=88, expr="neutral", arm_r=(60, 0.95, 0.2), arm_l=(35, 0.95, 0.2, BACK),
             leg_l=(172, 1.0, 0.0), leg_r=(184, 1.0, 0.0))


def _p_sit_up(c):
    return J(c, lean=-4, yaw=0.55, roll=7, expr="worried", mouth="smile", pitch=0.35, arm_r=(-70, 1.0, -0.6, TOP), arm_l=(118, 0.85, 0.2, BACK),
             leg_r=(8, 1.0, 0.3), leg_l=(-30, 0.78, -1.0), sawdust=1.0, fx=["sweat"])


def _p_straddle_a(c):     # STRADDLE: belly DOWN, face toward the ground, lead leg kicked high, arms reaching down
    return J(c, lean=102, yaw=0.9, roll=96, pitch=0.3, hdy=0.1, expr="determined", arm_r=(94, 1.1, 0.1), arm_l=(70, 1.1, 0.1, BACK),
             leg_r=(-100, 1.05, 0.0), leg_l=(150, 1.0, 0.2))


def _p_straddle_b(c):
    return J(c, lean=100, yaw=0.9, roll=94, pitch=0.3, hdy=0.1, expr="determined", arm_r=(100, 1.1, 0.1), arm_l=(76, 1.1, 0.1, BACK),
             leg_r=(160, 1.0, 0.2), leg_l=(-118, 1.05, 0.0))


def _p_knock(c):
    return J(c, lean=64, yaw=0.15, roll=25, expr="shocked", mouth="o", arm_r=(-30, 1.05, -0.5), arm_l=(-150, 1.05, 0.5, BACK),
             leg_r=(35, 1.0, 1.0), leg_l=(150, 1.0, -1.0))


def _p_lie_hands_face(c):
    return J(c, lean=91, yaw=-0.9, roll=88, expr="sad", arm_r=dict(hand=(0.02, 0.10), bend=-0.8, layer="top"),
             arm_l=dict(hand=(-0.10, 0.18), bend=0.6, layer="top"), leg_l=(172, 1.0, 0.0), leg_r=(184, 1.0, 0.0))


def _p_cheer(c):
    return J(c, lean=0, yaw=0.15, expr="excited", arm_r=(-55, 1.05, -0.6, OP), arm_l=(-125, 1.05, -0.6, dict(shape="open")),
             legs=dict(preset="wide"))


def _p_podium(c):
    return J(c, lean=0, yaw=0.25, roll=-4, expr="happy", arm_r=dict(preset="wave"), arm_l=(40, 0.8, 0.5), legs=dict(preset="stand"), medal=1)


def _p_thumb(c):
    return J(c, lean=0, yaw=0.3, expr="happy", arm_r=(-35, 0.85, -0.3), arm_l=(95, 0.9, 0.3, BACK), legs=dict(preset="stand"), thumb_r=1)


def _p_stand(c):
    return J(c, lean=0, yaw=0.3, expr="neutral", arm_r=dict(preset="down"), arm_l=dict(preset="down"))


def _p_sit_up_hand(c):      # sitting on the foam, smiling, thumb up (rivals)
    return J(c, lean=4, yaw=0.5, expr="happy", arm_r=(-40, 0.85, -0.3), arm_l=(110, 0.8, 0.2, BACK), leg_r=(6, 1.0, 0.3), leg_l=(2, 1.0, 0.3), thumb_r=1)


def _p_laugh(c):
    return J(c, lean=-5, yaw=0.3, roll=-10, expr="laughing", arm_r=dict(hand=(0.28, 1.0), bend=0.8), arm_l=dict(hand=(-0.25, 1.05), bend=0.8, layer="back"),
             fx=["tears"], legs=dict(preset="stand", crouch=0.05))


def _p_point_laugh(c):
    return J(c, lean=2, yaw=0.7, roll=6, expr="laughing", arm_r=(-6, 1.05, -0.3, PT), arm_l=dict(preset="hip"), fx=["tears"])


def _p_point(c):
    return J(c, lean=2, yaw=0.7, expr="smug", arm_r=(-8, 1.05, -0.3, PT), arm_l=dict(preset="hip"))


def _p_gape(c):
    return J(c, lean=-3, yaw=0.4, expr="shocked", mouth="o", pitch=-0.15, arm_r=dict(preset="shrug"), arm_l=(100, 0.7, 0.3, BACK),
             legs=dict(preset="stand"), fx=["sweat"])


def _p_jaw_drop(c):
    return J(c, lean=-3, yaw=0.4, expr="shocked", mouth=OPEN_WIDE, pitch=-0.2, arm_r=(98, 0.8, 0.3), arm_l=(84, 0.8, 0.3, BACK))


def _seat(L=1.0):
    return dict(leg_r=(38, 0.86, 1.0), leg_l=(44, 0.80, 1.0))


def _p_sit_cross(c):
    return J(c, lean=0, yaw=0.45, expr="unimpressed", arm_r=dict(hand=(-0.20, 0.86), bend=0.9), arm_l=dict(hand=(0.22, 0.90), bend=0.9), **_seat())


def _p_sit_laugh(c):
    return J(c, lean=-6, yaw=0.45, roll=-10, expr="laughing", arm_r=dict(hand=(0.28, 1.0), bend=0.8), arm_l=dict(hand=(-0.25, 1.05), bend=0.8, layer="back"), fx=["tears"], **_seat())


def _p_sit_cheer(c):
    return J(c, lean=0, yaw=0.3, expr="excited", arm_r=(-55, 1.05, -0.6, OP), arm_l=(-125, 1.05, -0.6, OP), **_seat())


def _p_sit_gape(c):
    return J(c, lean=-3, yaw=0.45, expr="shocked", mouth="o", arm_r=dict(preset="shrug"), arm_l=(100, 0.7, 0.3, BACK), **_seat())


def _p_sit_point(c):
    return J(c, lean=2, yaw=0.7, expr="laughing", arm_r=(-6, 1.05, -0.3, PT), arm_l=dict(hand=(-0.25, 1.05), bend=0.8, layer="back"), fx=["tears"], **_seat())


# ---- the coach
def _p_coach_laugh(c):
    return J(c, lean=-6, yaw=0.3, roll=-12, expr="laughing", arm_r=dict(hand=(0.42, 1.02), bend=0.9), arm_l=dict(hand=(-0.42, 1.02), bend=0.9, layer="front"),
             fx=["tears"], legs=dict(preset="stand", crouch=0.04))


def _p_coach_point(c):
    return J(c, lean=3, yaw=0.65, roll=-3, expr="smug", mouth="flat", arm_r=(-10, 1.05, -0.3, PT), arm_l=dict(preset="hip"))


def _p_coach_neck(c):
    return J(c, lean=2, yaw=0.2, roll=9, expr="shocked", mouth="clench", arm_r=dict(hand=(0.30, 0.52), bend=0.9, layer="top"),
             arm_l=dict(hand=(-0.30, 0.54), bend=0.9, layer="top"))


def _wag(c, ang):
    return J(c, lean=2, yaw=0.5, roll=-3, expr="unimpressed", mouth="flat", arm_r=dict(hand=(0.60 + 0.15 * ang, -0.02), bend=-1.0, shape="point"), arm_l=dict(preset="hip"))


def _p_coach_wag_a(c):
    return _wag(c, -1)


def _p_coach_wag_b(c):
    return _wag(c, 1)


def _p_coach_jab(c):
    return J(c, lean=-2, yaw=0.4, roll=-4, pitch=-0.2, expr="smug", mouth="flat", arm_r=dict(hand=(0.16, 0.92), bend=0.2, shape="point", layer="top"), arm_l=dict(preset="hip"))


def _p_coach_shout(c):
    return J(c, lean=4, yaw=0.5, pitch=-0.3, expr="angry", mouth="talk_b", arm_r=(-12, 1.05, -0.3, PT), arm_l=dict(preset="hip"))


def _p_coach_jaw(c):
    return _p_jaw_drop(c)


def _p_coach_sigh(c):
    return J(c, lean=7, yaw=0.35, pitch=0.8, hdy=0.04, expr="sad", mouth="frown", arm_r=dict(preset="chin"), arm_l=(98, 0.75, 0.3, BACK))


def _p_coach_clumsy_flop(c):   # a sagging, badly arched backwards flop: belly up, hips drooping, arms and legs flailing wide, the cap flying off
    return J(c, lean=128, yaw=-0.8, roll=40, hdx=0.05, hdy=0.25, bend=-34, bend_y=0.5, expr="shocked", mouth="o", hat_off=1.0,
             arm_r=(-25, 1.25, -0.4, TOP), arm_l=(-112, 1.25, 0.4, TOP), leg_r=(-118, 1.05, -0.3), leg_l=(96, 1.0, 0.2))


def _p_coach_buried(c):
    return J(c, lean=0, yaw=0.5, roll=-8, expr="worried", mouth="smile", pitch=0.2, arm_r=dict(hand=(0.78, 0.42), bend=0.2, layer="top"), arm_l=(100, 0.6, 0.2, BACK),
             legs=dict(preset="stand"), sawdust=1.0, buried=1, thumb_r=1)


def coach_clumsy_run(phase, cast="coach", facing=1):
    """the coach's clumsy run: cast6.cycle 'run' plus a heavy forward lean, flapping arms, a wobbling head."""
    b = dict(expr="shocked", mouth="o")
    p = cycle(cast, phase, "run", 1, base=b)
    s = math.sin(2 * math.pi * phase)
    p["lean"] = 22.0 + 4.0 * s * s
    p["arm_r"] = dict(hand=(0.9, -0.1 + 0.4 * s), bend=-0.6)
    p["arm_l"] = dict(hand=(0.1, -0.3 - 0.4 * s), bend=-0.6, layer="back")
    p["head_roll"] = 8.0 * s
    return flip(p) if facing < 0 else p


def run_curved(cast, phase, facing=1):
    """the jumper's curved approach: cast6.cycle 'run', leaning into the curve (about 18 degrees), eyes on the bar."""
    p = cycle(cast, phase, "run", 1, base=dict(expr="determined", gaze=(0.7, -0.1), lean=6.0, yaw=0.6))
    return flip(p) if facing < 0 else p


def laugh_bob(frame, fps=30.0, hz=3.0, amp=0.06):
    """value for the pose key `bob`: a belly-laugh bounce, hz cycles per second, amp D peak (0 .. amp)."""
    return amp * 0.5 * (1.0 + math.sin(2 * math.pi * hz * frame / fps - math.pi / 2))


def _p_photog_ready(c):
    return J(c, lean=2, yaw=0.45, expr="grinning", pitch=0.05, arm_r=dict(hand=(0.30, 0.22), bend=-0.2, layer="top"), arm_l=dict(hand=(0.62, 0.5), bend=0.4, layer="top"),
             prop_r=dict(type="presscam", angle=-4, scale=1.3), legs=dict(preset="stand", crouch=0.30, spread=0.20))


def _p_photog_flash(c):
    return J(c, lean=6, yaw=0.45, expr="grinning", pitch=-0.05, arm_r=dict(hand=(0.30, 0.16), bend=-0.2, layer="top"), arm_l=dict(hand=(0.62, 0.46), bend=0.4, layer="top"),
             prop_r=dict(type="presscam", angle=-8, scale=1.3), legs=dict(preset="stand", crouch=0.34, spread=0.22), flash=1.0)


def _p_official_stand(c):
    return J(c, lean=0, yaw=0.35, expr="neutral", arm_r=dict(preset="behind"), arm_l=dict(preset="behind"))


def _p_official_raise(c):
    return J(c, lean=0, yaw=0.3, pitch=-0.35, expr="determined", arm_r=(-70, 1.05, -0.4), arm_l=(-110, 1.05, -0.4, BACK))


def _p_official_point(c):
    return J(c, lean=2, yaw=0.6, expr="neutral", arm_r=(-20, 1.05, -0.3, PT), arm_l=dict(preset="behind"))


def _p_clip(c):
    return J(c, lean=0, yaw=0.4, expr="unimpressed", arm_r=dict(hand=(0.40, 0.95), bend=0.5), arm_l=dict(preset="hip"), prop_r=dict(type="clipboard", angle=0))


def _p_sit_read(c):       # seated, holding the open newspaper wide in both hands at chest height (shot 14); the right hand holds the right edge
    p = J(c, lean=0, yaw=0.0, pitch=0.25, expr="grinning", arm_r=dict(hand=(0.74, 0.92), bend=0.6), arm_l=dict(hand=(-0.74, 0.92), bend=0.6, layer="front"),
          prop_r=dict(type="paper15", angle=0, scale=1.2), **_seat())
    return p


def _p_walk_dejected(c, phase=0.25):
    p = cycle(c, phase, "walk", 1, base=dict(expr="sad", mouth="frown", pitch=1.0, yaw=0.6))
    s_ = math.sin(2 * math.pi * phase)
    p["lean"] = 12.0
    p["head_dy"] = 0.06
    p["head_roll"] = 8.0
    p["arm_r"] = dict(hand=(0.45 + 0.08 * s_, 1.45), bend=0.5)
    p["arm_l"] = dict(hand=(-0.30 - 0.08 * s_, 1.45), bend=0.5, layer="back")
    return p


def walk_dejected(cast, phase, facing=1):
    """head down, shoulders slumped, arms hanging, a slow walk (cast6 'walk', 28 frames per cycle)."""
    p = _p_walk_dejected(cast, phase)
    return flip(p) if facing < 0 else p


POSE_FUNCS = {
    "sit_read": _p_sit_read, "walk_dejected": _p_walk_dejected,
    # jumper
    "rock_a": _p_rock(True), "rock_b": _p_rock(False), "plant": _p_plant, "takeoff": _p_takeoff,
    "flop_rise": _p_flop_rise, "flop_head": _p_flop_head, "flop_back": _p_flop_back, "flop": _p_flop, "flop_flick": _p_flop_flick,
    "land_back": _p_land_back, "lie_back": _p_lie_back, "sit_up": _p_sit_up,
    "straddle_a": _p_straddle_a, "straddle_b": _p_straddle_b, "knock": _p_knock, "lie_hands_face": _p_lie_hands_face,
    "cheer": _p_cheer, "podium": _p_podium, "thumb": _p_thumb, "sit_thumb": _p_sit_up_hand, "stand": _p_stand,
    # boys / crowd
    "laugh": _p_laugh, "point_laugh": _p_point_laugh, "point": _p_point, "gape": _p_gape, "jaw_drop": _p_jaw_drop,
    "sit_cross": _p_sit_cross, "sit_laugh": _p_sit_laugh, "sit_cheer": _p_sit_cheer, "sit_gape": _p_sit_gape, "sit_point": _p_sit_point,
    # coach
    "coach_laugh": _p_coach_laugh, "coach_point": _p_coach_point, "coach_neck": _p_coach_neck, "coach_wag_a": _p_coach_wag_a, "coach_wag_b": _p_coach_wag_b,
    "coach_jab": _p_coach_jab, "coach_shout": _p_coach_shout, "coach_jaw": _p_coach_jaw, "coach_sigh": _p_coach_sigh,
    "coach_clumsy_flop": _p_coach_clumsy_flop, "coach_buried": _p_coach_buried, "clip": _p_clip,
    # press and officials
    "photog_ready": _p_photog_ready, "photog_flash": _p_photog_flash, "official_stand": _p_official_stand, "official_raise": _p_official_raise,
    "official_point": _p_official_point,
}
POSE_NAMES = tuple(POSE_FUNCS)


def _STORY_DEFS():
    D = {}

    def add(name, cast, pname, note, lip=False, **over):
        D[name] = (cast, pose_for(pname, cast, **over), note, lip)
    add("dick_rock", "dick", "rock_a", "at the mark, rocking: alternate rock_a / rock_b about every 0.25 s")
    add("dick_plant", "dick", "plant", "plant step of the curved approach")
    add("dick_takeoff", "dick", "takeoff", "take-off with the knee drive")
    add("dick_flop", "dick", "flop", "the arched bridge: hips at the apex, head and legs hang lower")
    add("dick_flick", "dick", "flop_flick", "legs flick over the bar")
    add("dick_land", "dick", "land_back", "landing on the back")
    add("dick_sit_up", "dick", "sit_up", "sheepish sit-up with chips in the hair")
    add("dick_straddle", "dick", "straddle_a", "straddle roll, face down (his failed attempt)")
    add("dick_knock", "dick", "knock", "bar knocked: flail")
    add("dick_lie_hands_face", "dick_olympic", "lie_hands_face", "lying on the foam, hands on his face")
    add("dick_cheer", "dick_olympic", "cheer", "arms-up cheer")
    add("dick_podium", "dick_olympic", "podium", "podium wave with the gold medal")
    add("coach_laugh", "coach", "coach_laugh", "belly laugh; drive pose key bob with laugh_bob()")
    add("coach_point", "coach", "coach_point", "pointing at Dick")
    add("coach_neck", "coach", "coach_neck", "broken-neck mime")
    add("coach_wag_a", "coach", "coach_wag_a", "finger wag (alternate with _b)")
    add("coach_wag_b", "coach", "coach_wag_b", "finger wag")
    add("coach_jab", "coach", "coach_jab", "jabbing his own chest")
    add("coach_shout", "coach", "coach_shout", "shouting (quote: mouth = talk_mouth(g), outside the quote mouth='flat')", True)
    add("coach_jaw", "coach", "coach_jaw", "jaw drop")
    add("coach_sigh", "coach", "coach_sigh", "sigh")
    add("coach_clumsy_flop", "coach", "coach_clumsy_flop", "the clumsy flop")
    add("coach_buried", "coach", "coach_buried", "buried in sawdust, weak thumbs-up (buried=1: mound drawn)")
    add("stands_shout", "coach_stands", "coach_shout", "in the stands: pennant hat, shouting (quote)", True)
    add("stands_jaw", "coach_stands", "coach_jaw", "in the stands: jaw drop")
    add("stands_point", "coach_stands", "coach_point", "in the stands: pointing")
    add("photographer_ready", "photographer", "photog_ready", "crouching with the press camera")
    add("photographer_flash", "photographer", "photog_flash", "FLASH (flash=1 burst; animate flash 1 -> 0 over 4 frames)")
    for i in (1, 2, 3):
        add("boy%d_laugh" % i, "boy%d" % i, "point_laugh", "pointing and laughing")
        add("boy%d_gape" % i, "boy%d" % i, "gape", "gaping")
        add("boy%d_sit_cross" % i, "boy%d" % i, "sit_cross", "sitting, arms crossed (bench)")
        add("rival%d_flop" % i, "rival%d" % i, "flop", "rival flop")
        add("rival%d_straddle" % i, "rival%d" % i, "straddle_a", "rival straddle roll: flat, face down")
    add("boy1_reader", "boy1", "sit_read", "newspaper reader, shot 14: seated, paper held wide at chest height, flop photo on the page")
    add("crowd1_reader", "crowd1", "sit_read", "newspaper reader (crowd member)")
    add("rival1_dejected", "rival1", "walk_dejected", "walking off dejected (shot 19)")
    add("official1_stand", "official1", "official_stand", "hands behind the back")
    add("official1_raise", "official1", "official_raise", "raising the crossbar")
    add("official2_raise", "official2", "official_raise", "raising the crossbar")
    add("official2_point", "official2", "official_point", "pointing")
    return D


register()
