#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cast5.py -- the cast of film 5 ("the bird boy", a British coal mine, early 1900s) for the v2 puppet, as an extension module.

    import sys; sys.path.insert(0, ".../v3/cast5"); import cast5      # registers on import (idempotent); imports cast4/3/2/cast_ext
    import puppet                                                     # the same module object, now with the new members
    f = puppet.figure("alfie", cast5.STORY5["alfie_hold_cage"][1], "a")
    b = puppet.figure("canary", cast5.CANARY5["perch_sing"], "c")     # the canary is its own small figure (not a person)
    c = puppet.figure("canary_in_cage", dict(state="fallen"), "cc")   # the brass cage with the bird inside

Nothing in v2/puppet or v3/cast..cast4 is edited.  This module adds entries to their tables:
    cast_ext.COSTUMES  pit (collarless shirt + braces / waistcoat / belt / neckerchief), gaffercoat
    cast_ext.HATS      leatherhelmet, capback, kerchief                  (miner1 uses cast2's skullcap, alfie cast3's flatnews)
    cast_ext.CANVAS    one feet-relative sprite canvas per member and per creature
and wraps puppet helpers on top of cast4's wrappers (each falls through for everything it does not handle):
    _norm      reads the pose keys of this module (flame, flame_blue, bird, cough)
    _face      soot smudges (CAST key "soot"), bushy sideburns ("sideburns"), cough puffs (pose key "cough")
    _prop      flame_lamp, oil_lamp_small, pickaxe, shovel, oxygen_box, cage (the canary in its cage, held by the ring)
    figure / resolve_pose / lerp_pose   the creature figures "canary" and "canary_in_cage" (own drawing, same return dict)
New cast:  alfie, gaffer, miner1, miner2, miner3  (+ creatures canary, canary_in_cage).
STORY5 / STORY5_META: the story poses; CANARY5: the canary states; cage_svg(), flame_lamp_svg(), bench_svg(): standalone pieces.

Command line (QA):  python3 test_cast5.py        lineup.png, canary.png, poses.png, canvas + head_flip checks, robustness runs
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
for _d in (os.path.join(PROJ, "v3", "cast4"), os.path.join(PROJ, "v3", "cast3"), os.path.join(PROJ, "v3", "cast2"), os.path.join(PROJ, "v3", "cast")):
    if _d not in sys.path:
        sys.path.insert(0, _d)
import cast4 as C4      # noqa: E402  (v3/cast4, read-only; imports cast3, cast2, cast_ext and v2/puppet)
import cast3 as C3      # noqa: E402
import cast2 as C2      # noqa: E402
import cast_ext as CE   # noqa: E402
import puppet as P      # noqa: E402

NEW5 = ("alfie", "gaffer", "miner1", "miner2", "miner3")
CREATURES = ("canary", "canary_in_cage")
TT = P.TORSO_TOP
_clamp, _rot, _num, _smooth = P._clamp, P._rot, P._num, P._smooth
_poly, _poly_d = P._poly, P._poly_d
_X, _ln, _circ = CE._X, CE._ln, CE._circ
_O5 = {}                      # the helpers this module wrapped
# pose keys of the figure being drawn (set by the _norm wrapper; figure() calls _norm before drawing anything)
_POSE5 = {"flame": 1.0, "flame_blue": 0.0, "bird": None, "cough": None, "t": 0.0}


def _cur():
    return CE._CUR[0]


def _f(v, d, lo, hi):
    """finite float clamped to [lo, hi] (garbage -> d)."""
    return _clamp(_num(v, d), lo, hi)


# ============================================================================= colours
CANARY = dict(body="#ffd21f", light="#fff27a", dark="#e3a20c", wing="#f2b81a", beak="#f08a24", beak_d="#b8561a", leg="#e98a5a",
              eye="#1a1418", cheek="#ff9a5a", note="#fff1c2", note_d="#f2c94a")
BRASS = dict(light="#f6db8a", base="#d9a83e", dark="#9a6a1c", shine="#fff3c4")


# ============================================================================= the canary (drawn by itself, no person pipeline)
# bird frame (D, scale 1): facing +x, the point between the feet (on the perch / floor) at (0, 0).  Body ~0.20 D wide.
BIRD_BC = (-0.010, -0.100)          # body centre
BIRD_RX, BIRD_RY = 0.098, 0.082
BIRD_HC = (0.055, -0.188)           # head centre (upright)
BIRD_HR = 0.064
LIE_DEG = 26.0                      # body rotation when lying on the floor (slumped forward onto the chest, head on the floor)
LIE_DROP = 0.026                    # the body sinks onto the floor (legs tucked) when lying

STATES = {
    # state: beak 0..1 (open), eyes 0..1 (0 closed line, 1 open), droop 0..1, ruffle 0..1, lie 0..1 (0 on the perch, 1 lying on the floor), notes
    "perch_sing": dict(beak=0.85, eyes=1.0, droop=0.0, ruffle=0.0, lie=0.0, notes=3),
    "perch_quiet": dict(beak=0.0, eyes=1.0, droop=0.0, ruffle=0.0, lie=0.0, notes=0),
    "droop": dict(beak=0.0, eyes=0.38, droop=1.0, ruffle=1.0, lie=0.0, notes=0),
    "fallen": dict(beak=0.0, eyes=0.0, droop=0.7, ruffle=0.6, lie=1.0, notes=0),
    "revive": dict(beak=0.0, eyes=0.55, droop=0.5, ruffle=0.5, lie=0.62, notes=0),
    "sing_one": dict(beak=0.65, eyes=0.85, droop=0.35, ruffle=0.3, lie=0.0, notes=1),
}
BIRD_KEYS = ("beak", "eyes", "droop", "ruffle", "lie", "notes", "breath", "t", "swing", "scale")


def _bird_norm(pose):
    """canary / cage pose -> plain numbers.  Unknown or garbage values fall back to the state's defaults (never raises)."""
    if isinstance(pose, str):
        pose = {"state": pose}
    if not isinstance(pose, dict):
        pose = {}
    st = pose.get("state")
    if not isinstance(st, str) or st not in STATES:
        st = "perch_quiet"
    d = STATES[st]
    g = pose.get
    B = dict(state=st)
    B["beak"] = _f(g("beak"), d["beak"], 0.0, 1.0)
    B["eyes"] = _f(g("eyes"), d["eyes"], 0.0, 1.0)
    B["droop"] = _f(g("droop"), d["droop"], 0.0, 1.0)
    B["ruffle"] = _f(g("ruffle"), d["ruffle"], 0.0, 1.0)
    B["lie"] = _f(g("lie"), d["lie"], 0.0, 1.0)
    B["notes"] = _f(g("notes"), d["notes"], 0.0, 5.0)
    B["breath"] = _f(g("breath"), 0.0, 0.0, 1.0)
    B["t"] = _num(g("t"), 0.0)
    B["swing"] = _f(g("swing"), 0.0, -40.0, 40.0)
    B["scale"] = _f(g("scale"), 1.0, 0.3, 4.0)
    B["mirror"] = bool(g("mirror", False)) if not isinstance(g("mirror"), (dict, list)) else False
    ink = g("ink")
    B["ink"] = ink if P._is_hex(ink) else P.INK
    if B["ink"][0] != "#":
        B["ink"] = "#" + B["ink"]
    tint = g("tint")
    if P._is_hex(tint):
        B["tint"] = P._rgb(tint if tint[0] != "#" else tint[1:])
    elif isinstance(tint, (tuple, list)) and len(tint) == 3:
        try:
            B["tint"] = tuple(_clamp(_num(c, 255.0), 0.0, 255.0) for c in tint)
        except Exception:  # noqa: BLE001
            B["tint"] = None
    else:
        B["tint"] = None
    return B


def _frac(x):
    return x - math.floor(x)


def _note(k, x, y, s, kind, col, cold):
    """one music note (head at (x, y)): kind 0 = eighth note with a flag, 1 = quarter note, 2 = two beamed eighths."""
    o = []
    hx, hy = 0.030 * s, 0.021 * s
    st = 0.085 * s
    sw = 0.012 * s
    heads = [(x, y)] if kind != 2 else [(x - 0.035 * s, y + 0.010 * s), (x + 0.040 * s, y - 0.006 * s)]
    stems = []
    for (cx, cy) in heads:
        sx = cx + hx * 0.80
        stems.append(((sx, cy - 0.004 * s), (sx, cy - st)))
    path = "".join("M%.4f,%.4f L%.4f,%.4f " % (a[0], a[1], b[0], b[1]) for a, b in stems)
    o.append('<path d="%s" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (path, k.ink, sw + 0.016 * s))
    if kind == 2:
        a, b = stems[0][1], stems[1][1]
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
                 % (a[0] - 0.006 * s, a[1], b[0] + 0.006 * s, b[1], b[0] + 0.006 * s, b[1] + 0.026 * s, a[0] - 0.006 * s, a[1] + 0.026 * s, k.c(col), k.ink, 0.010 * s))
    elif kind == 0:
        a = stems[0][1]
        fl = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" % (a[0], a[1], a[0] + 0.050 * s, a[1] + 0.020 * s, a[0] + 0.040 * s, a[1] + 0.065 * s,
                                                                          a[0] + 0.030 * s, a[1] + 0.035 * s, a[0], a[1] + 0.030 * s)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>' % (fl, k.c(col), k.ink, 0.010 * s))
    o.append('<path d="%s" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (path, k.c(col), sw * 0.8))
    for (cx, cy) in heads:
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(-22 %.4f %.4f)" fill="%s" stroke="%s" stroke-width="%.4f"/>'
                 % (cx, cy, hx, hy, cx, cy, k.c(col), k.ink, 0.013 * s))
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(-22 %.4f %.4f)" fill="%s" opacity="0.8"/>'
                 % (cx + 0.006 * s, cy + 0.004 * s, hx * 0.45, hy * 0.40, cx, cy, k.c(cold)))
        k.ext.append((cx, cy, hx + 0.02 * s))
    for a, b in stems:
        k.ext.append((b[0], b[1], 0.05 * s))
    return "".join(o)


def _notes(k, n, bx, by, t, s=1.0, side=1.0):
    """n music notes (0..5, rounded) floating up and forward from the beak tip (bx, by); `t` makes them bob (continuous)."""
    n = int(round(_clamp(n, 0.0, 5.0)))
    o = []
    for i in range(n):
        ph = 2.0 * math.pi * (t * 0.8 + i * 0.27)
        x = bx + side * s * (0.075 + 0.060 * i + 0.012 * math.sin(ph))
        y = by - s * (0.085 + 0.095 * i + 0.010 * math.cos(ph * 0.9))
        x += side * s * 0.035 * math.sin(i * 1.9)
        o.append(_note(k, x, y, s * (1.0 - 0.05 * i), (0, 2, 1, 0, 2)[i], CANARY["note"], CANARY["note_d"]))
    return "".join(o)


def _bird_xf(B, ox, oy, s):
    """transform of the bird frame -> parent: translate(ox oy) scale(s) rotate(lie about the body centre)."""
    a = LIE_DEG * _smooth(0.0, 1.0, B["lie"])
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))

    dy0 = LIE_DROP * _smooth(0.0, 1.0, B["lie"])

    def T(x, y):
        dx, dy = x - BIRD_BC[0], y - BIRD_BC[1]
        rx, ry = BIRD_BC[0] + dx * ca - dy * sa, BIRD_BC[1] + dx * sa + dy * ca + dy0
        return (ox + rx * s, oy + ry * s)
    tr = 'translate(%.4f %.4f) scale(%.4f) translate(0 %.4f) rotate(%.3f %.4f %.4f)' % (ox, oy, s, dy0, a, BIRD_BC[0], BIRD_BC[1])
    return T, tr


def _bird(k, B, ox, oy, s=1.0, notes=True):
    """the canary with its feet point at (ox, oy) of the parent (lying: body on the line y = oy), drawn at scale s.
    Returns (svg, anchors in the parent frame)."""
    T, tr = _bird_xf(B, ox, oy, s)
    dr, rf, ly, e = B["droop"], B["ruffle"], B["lie"], B["eyes"]
    br = 1.0 + 0.07 * B["breath"] * math.sin(2.0 * math.pi * B["t"] * 3.0)
    ink = k.ink
    u = k.uid
    bcx, bcy = BIRD_BC
    rx, ry = BIRD_RX * br, BIRD_RY * br
    lys = _smooth(0.0, 1.0, ly)
    hx, hy = BIRD_HC[0] + 0.030 * dr + 0.020 * lys, BIRD_HC[1] + 0.060 * dr + 0.030 * lys
    hr = BIRD_HR
    brot = 10.0 * dr                      # body tips forward when drooping
    o = ['<g transform="%s">' % tr]
    k.defs.append('<radialGradient id="%s_bdg" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/>'
                  '<stop offset="1" stop-color="%s"/></radialGradient>' % (u, k.c(CANARY["light"]), k.c(CANARY["body"]), k.c(CANARY["dark"])))
    # legs (tucked when lying)
    lg = 1.0 - 0.75 * _smooth(0.0, 1.0, ly)
    for lx in (-0.030, 0.012):
        a, b = (lx, -0.030), (lx + 0.004, -0.030 + 0.030 * lg)
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (a + b + (ink,)))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % (a + b + (k.c(CANARY["leg"]),)))
        toes = "M%.4f,%.4f q0.020,0.004 0.030,0.012 M%.4f,%.4f q-0.016,0.004 -0.022,0.012" % (b + b)
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (toes, ink))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.007" stroke-linecap="round"/>' % (toes, k.c(CANARY["leg"])))
    # tail: two feathers, lower when drooping
    td = 0.045 * dr
    for (dy, ln, col) in ((0.012, 1.0, CANARY["dark"]), (-0.010, 0.92, CANARY["wing"])):
        tl = [(bcx - 0.070, bcy - 0.020 + dy), (bcx - 0.070 - 0.080 * ln, bcy + 0.030 + dy + td - 0.016), (bcx - 0.072 - 0.088 * ln, bcy + 0.056 + dy + td),
              (bcx - 0.060, bcy + 0.040 + dy)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (P._smooth_closed(tl), k.c(col), ink))
    # body + head: one silhouette (ink pass of both, then the fills)
    body = '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%.3f %.4f %.4f)"%s/>'
    head = '<circle cx="%.4f" cy="%.4f" r="%.4f"%s/>'
    o.append(body % (bcx, bcy, rx, ry, -8.0 + brot, bcx, bcy, ' fill="%s" stroke="%s" stroke-width="0.026"' % (ink, ink)))
    o.append(head % (hx, hy, hr, ' fill="%s" stroke="%s" stroke-width="0.026"' % (ink, ink)))
    o.append(body % (bcx, bcy, rx, ry, -8.0 + brot, bcx, bcy, ' fill="url(#%s_bdg)"' % u))
    o.append(head % (hx, hy, hr, ' fill="url(#%s_bdg)"' % u))
    # neck fill between head and body (hides the head's lower ink arc inside the silhouette)
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.048" ry="0.040" fill="%s"/>' % ((hx + bcx) / 2 + 0.006, (hy + bcy) / 2 + 0.004, k.c(CANARY["body"])))
    # highlight on the crown, a soft chest shade
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.9"/>'
             % (hx - 0.040, hy - 0.020, hx - 0.025, hy - 0.052, hx + 0.008, hy - 0.056, k.c("#fffbe0")))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>'
             % (bcx + 0.050, bcy + 0.060, bcx + 0.010, bcy + 0.085, bcx - 0.050, bcy + 0.070, k.c(CANARY["dark"])))
    # wing (hangs open a little when drooping)
    wd = 0.030 * dr
    wing = [(bcx + 0.050, bcy - 0.035), (bcx - 0.010, bcy - 0.045), (bcx - 0.085, bcy - 0.005 + wd * 0.5), (bcx - 0.115, bcy + 0.030 + wd),
            (bcx - 0.060, bcy + 0.040 + wd * 0.6), (bcx + 0.020, bcy + 0.020)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (P._smooth_closed(wing), k.c(CANARY["wing"]), ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>'
             % (bcx + 0.005, bcy - 0.010, bcx - 0.045, bcy + 0.000 + wd * 0.5, bcx - 0.090, bcy + 0.024 + wd,
                bcx + 0.010, bcy + 0.010, bcx - 0.035, bcy + 0.022 + wd * 0.5, bcx - 0.070, bcy + 0.034 + wd, k.c(CANARY["dark"])))
    # ruffled feathers: small tufts on the back, the chest and the crown
    if rf > 0.02:
        tufts = []
        for (tx, ty, ang) in ((bcx - 0.060, bcy - 0.068, -120), (bcx + 0.020, bcy - 0.082, -85), (bcx + 0.085, bcy + 0.030, 10), (bcx + 0.060, bcy + 0.070, 50),
                              (hx - 0.050, hy - 0.040, -130)):
            ln = 0.030 * rf
            for da in (-25, 20):
                a = math.radians(ang + da)
                tufts.append("M%.4f,%.4f l%.4f,%.4f " % (tx, ty, ln * math.cos(a), ln * math.sin(a)))
        o.append('<path d="%s" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % ("".join(tufts), ink))
        o.append('<path d="%s" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % ("".join(tufts), k.c(CANARY["body"])))
    # crest tuft (a small curl on the crown)
    cx, cy = hx - 0.008, hy - hr + 0.004
    crest = "M%.4f,%.4f q0.000,-0.040 0.030,-0.042 q-0.020,0.012 -0.008,0.034" % (cx - 0.010, cy + 0.004)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (crest, k.c(CANARY["body"]), ink))
    # cheek
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.020" ry="0.012" fill="%s" opacity="0.65"/>' % (hx + 0.020, hy + 0.028, k.c(CANARY["cheek"])))
    # beak: upper and lower mandible, opened by `beak`
    bxb, byb = hx + hr - 0.010, hy + 0.006
    ob = B["beak"]
    up = [(bxb, byb - 0.019), (bxb + 0.050, byb + 0.000), (bxb, byb + 0.004)]
    lo = [(bxb, byb + 0.002), (bxb + 0.040, byb + 0.004), (bxb, byb + 0.018)]
    if ob > 0.01:
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (bxb - 0.004, byb - 0.010, bxb + 0.034 * (0.5 + ob * 0.5), byb + 0.004, bxb - 0.004, byb + 0.016, k.c("#7a2a2a"), ink))
    for pts, a, col in ((up, -24.0 * ob, CANARY["beak"]), (lo, 20.0 * ob, CANARY["beak_d"])):
        o.append('<path d="%s" transform="rotate(%.3f %.4f %.4f)" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
                 % (_poly_d(pts), a, bxb, byb, k.c(col), ink))
    # eye
    ex, ey = hx + 0.020, hy - 0.010
    er = 0.0165
    if e < 0.12:
        # gently closed: a soft downward-curved lid line with two tiny lashes (no X)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>'
                 % (ex - 0.020, ey - 0.002, ex, ey + 0.014, ex + 0.020, ey - 0.002, ink))
        o.append('<path d="M%.4f,%.4f l-0.008,0.008 M%.4f,%.4f l0.008,0.008" stroke="%s" stroke-width="0.006" stroke-linecap="round"/>'
                 % (ex - 0.010, ey + 0.009, ex + 0.010, ey + 0.009, ink))
    else:
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (ex, ey, er, k.c(CANARY["eye"])))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="%.3f"/>' % (ex - 0.006, ey - 0.006, er * 0.36, _smooth(0.3, 0.9, e)))
        if e < 0.98:
            lid = ey - er + 2.0 * er * (1.0 - e) * 0.85
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s"/>' % (ex - er - 0.004, ey - er - 0.006, ex + er + 0.004, ey - er - 0.006,
                                                                                              ex + er + 0.004, lid, ex - er - 0.004, lid, k.c(CANARY["body"])))
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (ex - er - 0.002, lid, ex + er + 0.002, lid, ink))
    o.append('</g>')
    # extents + anchors in the parent frame
    for p in ((bcx - rx - 0.015, bcy), (bcx + rx + 0.015, bcy), (bcx, bcy - ry - 0.015), (bcx, bcy + ry + 0.015), (hx, hy - hr - 0.05), (hx + hr + 0.06, hy),
              (bcx - 0.17, bcy + 0.07 + td), (0.0, 0.010)):
        q = T(*p)
        k.ext.append((q[0], q[1], 0.012 * s))
    an = dict(beak=T(bxb + 0.050, byb), eye=T(ex, ey), bird_head=T(hx, hy), bird_body=T(bcx, bcy), bird_feet=(ox, oy))
    svg = "".join(o)
    if notes and B["notes"] >= 0.5:
        bx, by = an["beak"]
        svg += _notes(k, B["notes"], bx, by, B["t"], s)
    return svg, an


# ============================================================================= the cage (ring top at (0, 0), base bottom at CAGE_H)
CAGE_W = 0.205                     # half width of the bars
CAGE_DOME, CAGE_BARS, CAGE_FLOOR, CAGE_H = 0.118, 0.238, 0.652, 0.748
CAGE_PERCH = 0.505
BIRD_X = -0.030


def _cage(k, B, notes=True):
    """the brass birdcage hanging from its ring (ring top at (0, 0)), the canary inside (on the perch, or on the floor when it
    lies), swung by B["swing"] degrees about the ring.  Returns (svg, anchors in the same frame)."""
    ink = k.ink
    u = k.uid
    sw = B["swing"]
    br = k.c(BRASS["base"])
    k.defs.append('<linearGradient id="%s_cgb" gradientUnits="userSpaceOnUse" x1="-0.24" y1="0" x2="0.24" y2="0"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(BRASS["light"]), k.c(BRASS["base"]), k.c(BRASS["dark"])))
    g = "url(#%s_cgb)" % u
    o = ['<g transform="rotate(%.3f)">' % sw]
    W = CAGE_W
    # back: a faint dark interior so the yellow bird reads against any wall
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" opacity="0.18"/>'
             % (-W, CAGE_BARS, W, CAGE_BARS, W, CAGE_FLOOR, -W, CAGE_FLOOR, k.c("#2a2030")))
    # back bars (thin, dim)
    back = "".join("M%.4f,%.4f L%.4f,%.4f " % (x, CAGE_BARS, x, CAGE_FLOOR) for x in [-W + 0.0275 + i * 0.055 for i in range(8)])
    o.append('<path d="%s" stroke="%s" stroke-width="0.006" opacity="0.45"/>' % (back, k.c(BRASS["dark"])))
    # perch (dowel) and the seed cup
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (-W + 0.01, CAGE_PERCH + 0.012, W - 0.01, CAGE_PERCH + 0.012, ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % (-W + 0.01, CAGE_PERCH + 0.012, W - 0.01, CAGE_PERCH + 0.012, k.c("#a8703e")))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (W - 0.075, CAGE_FLOOR - 0.090, W + 0.012, CAGE_FLOOR - 0.090, W + 0.006, CAGE_FLOOR - 0.040, W - 0.068, CAGE_FLOOR - 0.040, k.c("#e8e2d2"), ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.008" fill="%s"/>' % (W - 0.032, CAGE_FLOOR - 0.088, k.c("#b88a4a")))
    # sand / seed husks on the floor
    o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f Z" fill="%s" opacity="0.8"/>' % (-W + 0.01, CAGE_FLOOR, CAGE_FLOOR - 0.016, W - 0.01, CAGE_FLOOR, k.c("#c9a86a")))
    # the bird: on the perch, falling, or on the floor
    lie = _smooth(0.0, 1.0, B["lie"])
    oy = CAGE_PERCH + (CAGE_FLOOR - CAGE_PERCH) * lie
    ox = BIRD_X + 0.010 * lie
    bsvg, an = _bird(k, B, ox, oy, 1.0, notes=False)
    o.append(bsvg)
    # front bars (brass, ink-edged), door frame, rings
    bars = [-W + i * (2 * W / 8.0) for i in range(9)]
    d = "".join("M%.4f,%.4f L%.4f,%.4f " % (x, CAGE_BARS, x, CAGE_FLOOR) for x in bars)
    o.append('<path d="%s" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (d, ink))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % (d, br))
    o.append('<path d="%s" stroke="%s" stroke-width="0.003" stroke-linecap="round" opacity="0.8" transform="translate(-0.002 0)"/>' % (d, k.c(BRASS["shine"])))
    # door: a slightly heavier frame round the middle bars, a little latch
    dx0, dx1, dy0 = bars[3] - 0.012, bars[5] + 0.012, CAGE_BARS + 0.150
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>'
             % (dx0, CAGE_FLOOR, dx0, dy0, dx1, dy0, dx1, CAGE_FLOOR, ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (dx0, CAGE_FLOOR, dx0, dy0, dx1, dy0, dx1, CAGE_FLOOR, br))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.012" fill="%s" stroke="%s" stroke-width="0.008"/>' % (dx1 + 0.012, dy0 + 0.11, br, ink))
    for y in (CAGE_BARS + 0.010, CAGE_BARS + 0.140):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.024" stroke-linecap="round"/>' % (-W - 0.006, y, W + 0.006, y, ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % (-W - 0.006, y, W + 0.006, y, br))
    # dome: bars curving up to the top knob
    dome = []
    for x in bars:
        f = x / W
        dome.append("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f " % (x, CAGE_BARS + 0.004, x * 0.92, CAGE_DOME + 0.020 + 0.080 * (1 - f * f) * 0.2 + 0.03, x * 0.12, CAGE_DOME + 0.008))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round"/>' % ("".join(dome), ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/>' % ("".join(dome), br))
    o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (-W, CAGE_BARS + 0.004, CAGE_DOME - 0.06, W, CAGE_BARS + 0.004, ink))
    o.append('<path d="M%.4f,%.4f Q0,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (-W, CAGE_BARS + 0.004, CAGE_DOME - 0.06, W, CAGE_BARS + 0.004, br))
    o.append('<ellipse cx="0" cy="%.4f" rx="0.042" ry="0.020" fill="%s" stroke="%s" stroke-width="0.012"/>' % (CAGE_DOME + 0.004, g, ink))
    # hook stem + ring handle
    o.append('<path d="M0,%.4f L0,%.4f" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (0.062, CAGE_DOME - 0.008, ink))
    o.append('<path d="M0,%.4f L0,%.4f" stroke="%s" stroke-width="0.010" stroke-linecap="round"/>' % (0.062, CAGE_DOME - 0.008, br))
    o.append('<circle cx="0" cy="0.034" r="0.030" fill="none" stroke="%s" stroke-width="0.024"/>' % ink)
    o.append('<circle cx="0" cy="0.034" r="0.030" fill="none" stroke="%s" stroke-width="0.011"/>' % br)
    # base tray (brass, slightly flared) with two bands and little feet
    tray = [(-W - 0.030, CAGE_FLOOR - 0.006), (W + 0.030, CAGE_FLOOR - 0.006), (W + 0.020, CAGE_H - 0.018), (-W - 0.020, CAGE_H - 0.018)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(tray), g, ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (-W - 0.022, CAGE_FLOOR + 0.030, W + 0.022, CAGE_FLOOR + 0.030, k.c(BRASS["dark"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.9"/>' % (-W - 0.010, CAGE_FLOOR + 0.008, W - 0.040, CAGE_FLOOR + 0.008, k.c(BRASS["shine"])))
    for x in (-W + 0.010, W - 0.010):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>'
                 % (x - 0.024, CAGE_H - 0.020, x + 0.024, CAGE_H - 0.020, x + 0.018, CAGE_H, x - 0.018, CAGE_H, k.c(BRASS["dark"]), ink))
    o.append('</g>')
    ca, sa = math.cos(math.radians(sw)), math.sin(math.radians(sw))

    def R(p):
        return (p[0] * ca - p[1] * sa, p[0] * sa + p[1] * ca)
    for p in ((-W - 0.035, CAGE_FLOOR), (W + 0.035, CAGE_FLOOR), (-W - 0.025, CAGE_H), (W + 0.025, CAGE_H), (0.0, -0.005), (-W, CAGE_BARS), (W, CAGE_BARS)):
        q = R(p)
        k.ext.append((q[0], q[1], 0.012))
    an = dict((n, R(v)) for n, v in an.items())
    an.update(ring=(0.0, 0.0), cage_floor=R((0.0, CAGE_FLOOR)), cage_bottom=R((0.0, CAGE_H)), perch=R((BIRD_X, CAGE_PERCH)),
              cage_top=R((0.0, CAGE_DOME)))
    svg = "".join(o)
    if notes and B["notes"] >= 0.5:
        bx, by = an["beak"]
        svg += _notes(k, B["notes"], bx, by, B["t"], 1.0)
    return svg, an


def cage_svg(state="perch_quiet", uid="cg", ink=P.INK, tint=None, **keys):
    """the canary in its brass cage as an SVG fragment in D units, ring top at (0, 0), base bottom at (0, CAGE_H) = 0.748.
    state: a CANARY state name or a full canary pose dict; extra keyword keys (notes, eyes, beak, lie, swing, t, ...) override it.
    Returns (svg, anchors) -- anchors: ring, beak, eye, bird_head, bird_body, bird_feet, perch, cage_floor, cage_bottom, cage_top."""
    pose = dict(state) if isinstance(state, dict) else {"state": state}
    pose.update(keys)
    B = _bird_norm(pose)
    k = P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)
    svg, an = _cage(k, B)
    return '<g id="%s_cage"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), svg), an


# ============================================================================= lamps and props
FLAME_IN = (0.0, 0.392)            # flame base inside the safety lamp's glass (ring top at (0, 0))


def _flame(k, x, y, size, blue=0.0, t=0.0, glow=True, body=True):
    """a teardrop flame standing on (x, y), `size` 0..2 (0 = out, 1 = normal, 2 = burning bright and tall); blue 0..1 turns it
    into the pale-blue firedamp cap (gas!).  The glow halo grows with size."""
    o = []
    if size <= 0.02:
        o.append('<circle cx="%.4f" cy="%.4f" r="0.006" fill="%s"/>' % (x, y - 0.004, k.c("#8a2a1a")))
        return "".join(o)
    s = 0.35 + 0.65 * min(size, 1.0) + 0.55 * max(0.0, size - 1.0)
    fl = 1.0 + 0.06 * math.sin(2 * math.pi * t * 5.0) + 0.03 * math.sin(2 * math.pi * t * 13.0)
    h, w = 0.075 * s * fl, 0.024 * (0.6 + 0.4 * s)
    outer = _mixh("#ff8a1e", "#6aa0ff", blue)
    mid = _mixh("#ffd34a", "#a8c8ff", blue)
    core = _mixh("#fff8dc", "#eef6ff", blue)
    u = k.uid
    if glow:
        gid = "%s_fg%d" % (u, len(k.defs))
        k.defs.append('<radialGradient id="%s"><stop offset="0" stop-color="%s" stop-opacity="%.3f"/><stop offset="0.45" stop-color="%s" stop-opacity="%.3f"/>'
                      '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
                      % (gid, k.c(_mixh("#ffd27a", "#9cc0ff", blue)), 0.55 + 0.15 * min(size, 2.0) / 2.0, k.c(_mixh("#ffb050", "#7aa0ff", blue)), 0.22,
                         k.c(_mixh("#ff9a3a", "#5a80ff", blue))))
        gr = 0.07 + 0.09 * s
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="url(#%s)"/>' % (x, y - h * 0.45, gr, gid))
    if blue > 0.02:
        # the firedamp cap: a pale blue cone above the flame
        ch = h * (0.8 + 1.4 * blue)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" opacity="%.3f"/>'
                 % (x - w * 1.5, y - h * 0.4, x - w * 0.9, y - h - ch * 0.8, x, y - h - ch, x + w * 0.9, y - h - ch * 0.8, x + w * 1.5, y - h * 0.4,
                    k.c("#9cc4ff"), 0.55 * blue))
    if not body:
        return "".join(o)
    sway = 0.004 * math.sin(2 * math.pi * t * 3.0)
    for (ww, hh, col) in ((1.0, 1.0, outer), (0.66, 0.74, mid), (0.36, 0.45, core)):
        d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
             % (x, y, x - w * ww * 1.3, y - 0.004, x - w * ww * 0.9, y - h * hh * 0.6, x + sway, y - h * hh,
                x + w * ww * 0.9, y - h * hh * 0.6, x + w * ww * 1.3, y - 0.004, x, y))
        o.append('<path d="%s" fill="%s"/>' % (d, k.c(col)))
    k.ext.append((x, y - h, 0.02))
    return "".join(o)


def _mixh(a, b, t):
    return P._mix(a, b, _clamp(t, 0.0, 1.0))


def _flame_lamp(k, flame=1.0, blue=0.0, t=0.0):
    """Clanny-type flame safety lamp hanging from its ring (ring top at (0, 0)): brass bonnet, wire-gauze chimney between three
    brass pillars, a glass cylinder with the flame inside, the brass oil vessel.  Height 0.52 D."""
    ink = k.ink
    u = k.uid
    k.defs.append('<linearGradient id="%s_flb" gradientUnits="userSpaceOnUse" x1="-0.09" y1="0" x2="0.09" y2="0"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(BRASS["light"]), k.c(BRASS["base"]), k.c(BRASS["dark"])))
    g = "url(#%s_flb)" % u
    o = []
    # glow behind everything (the glass is clear)
    o.append(_flame(k, FLAME_IN[0], FLAME_IN[1], flame, 0.0, t, glow=True, body=False))
    # ring + hook
    o.append('<circle cx="0" cy="0.032" r="0.028" fill="none" stroke="%s" stroke-width="0.022"/>' % ink)
    o.append('<circle cx="0" cy="0.032" r="0.028" fill="none" stroke="%s" stroke-width="0.010"/>' % k.c(BRASS["base"]))
    o.append('<path d="M0,0.060 L0,0.085" stroke="%s" stroke-width="0.020"/>' % ink)
    # bonnet (top cap)
    o.append('<path d="M-0.045,0.085 L0.045,0.085 L0.070,0.135 L-0.070,0.135 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (g, ink))
    o.append('<path d="M-0.074,0.135 L0.074,0.135 L0.074,0.152 L-0.074,0.152 Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (g, ink))
    # gauze chimney
    o.append('<rect x="-0.055" y="0.152" width="0.110" height="0.150" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#8f949c"), ink))
    mesh = "".join("M-0.055,%.4f L0.055,%.4f " % (0.165 + 0.022 * i, 0.165 + 0.022 * i) for i in range(6))
    mesh += "".join("M%.4f,0.152 L%.4f,0.302 " % (-0.040 + 0.020 * i, -0.040 + 0.020 * i) for i in range(5))
    o.append('<path d="%s" stroke="%s" stroke-width="0.004" opacity="0.6"/>' % (mesh, k.c("#c8ccd2")))
    o.append('<rect x="-0.068" y="0.296" width="0.136" height="0.020" fill="%s" stroke="%s" stroke-width="0.012"/>' % (g, ink))
    # glass cylinder with the flame
    o.append('<rect x="-0.060" y="0.316" width="0.120" height="0.090" fill="%s" fill-opacity="0.28" stroke="%s" stroke-width="0.012"/>' % (k.c("#e8f4ff"), ink))
    o.append(_flame(k, FLAME_IN[0], FLAME_IN[1], flame, blue, t, glow=False))
    o.append('<path d="M-0.040,0.326 L-0.040,0.398" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.6"/>')
    # pillars
    pil = "M-0.064,0.150 L-0.064,0.410 M0.064,0.150 L0.064,0.410 M0.0,0.150 L0.0,0.300"
    o.append('<path d="%s" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (pil, ink))
    o.append('<path d="%s" stroke="%s" stroke-width="0.007" stroke-linecap="round"/>' % (pil, k.c(BRASS["base"])))
    # oil vessel
    o.append('<path d="M-0.072,0.406 L0.072,0.406 L0.078,0.418 L0.078,0.500 Q0,0.522 -0.078,0.500 L-0.078,0.418 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (g, ink))
    o.append('<path d="M-0.076,0.440 L0.076,0.440 M-0.077,0.478 L0.077,0.478" stroke="%s" stroke-width="0.008" opacity="0.8"/>' % k.c(BRASS["dark"]))
    o.append('<path d="M-0.055,0.420 L-0.055,0.495" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(BRASS["shine"]))
    for p in ((-0.09, 0.30), (0.09, 0.30), (0.0, 0.53), (0.0, -0.005), (-0.08, 0.50), (0.08, 0.50)):
        k.ext.append((p[0], p[1], 0.01))
    return "".join(o)


def flame_lamp_svg(uid="fl", flame=1.0, blue=0.0, t=0.0, ink=P.INK, tint=None):
    """the flame safety lamp alone (for the lamp inserts), ring top at (0, 0), bottom at y = 0.52 D, flame base at FLAME_IN.
    flame 0..2 (0 out, 1 normal, 2 bright), blue 0..1 (firedamp cap)."""
    k = P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)
    svg = _flame_lamp(k, _f(flame, 1.0, 0.0, 2.0), _f(blue, 0.0, 0.0, 1.0), _num(t, 0.0))
    return '<g id="%s_lamp"><defs>%s</defs>%s</g>' % (k.uid, "".join(k.defs), svg)


def _oil_lamp(k, x, y, sc=1.0, flame=0.8, t=0.0):
    """small brass 'teapot' oil lamp hanging from a hook at (x, y): round pot, lid knob, spout to +x with a small flame."""
    o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (x, y, sc)]
    ink = k.ink
    o.append('<path d="M0,0 Q0.020,0.010 0.0,0.045 L-0.004,0.060" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>' % ink)
    o.append('<path d="M0.040,0.090 L0.098,0.062 L0.104,0.072 L0.050,0.108 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), ink))
    o.append('<ellipse cx="0" cy="0.100" rx="0.060" ry="0.040" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c(BRASS["base"]), ink))
    o.append('<path d="M-0.040,0.088 Q-0.020,0.070 0.010,0.072" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.9"/>' % k.c(BRASS["shine"]))
    o.append('<path d="M-0.050,0.112 Q0,0.130 0.050,0.112" fill="none" stroke="%s" stroke-width="0.007" opacity="0.8"/>' % k.c(BRASS["dark"]))
    o.append('<ellipse cx="0" cy="0.062" rx="0.016" ry="0.010" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(BRASS["dark"]), ink))
    o.append(_flame(k, 0.102, 0.066, flame * 0.55, 0.0, t, glow=True))
    o.append('</g>')
    for p in ((-0.07, 0.10), (0.07, 0.10), (0.11, 0.02), (0.0, 0.15)):
        k.ext.append((x + p[0] * sc, y + p[1] * sc, 0.01))
    return "".join(o)


def _oxygen_box(k):
    """small brass resuscitation box (hand on its left handle at (0, 0)): riveted brass case with a glass window showing the
    blue oxygen bottle and a dial, a valve wheel on top, a red rubber tube curving up and out to a little brass nozzle."""
    ink = k.ink
    u = k.uid
    k.defs.append('<linearGradient id="%s_oxg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0.32" y2="0"><stop offset="0" stop-color="%s"/>'
                  '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(BRASS["light"]), k.c(BRASS["base"]), k.c(BRASS["dark"])))
    o = []
    x0, x1, y0, y1 = 0.020, 0.320, -0.120, 0.100
    tube = "M0.270,%.4f C0.290,-0.260 0.420,-0.300 0.470,-0.235 S0.540,-0.180 0.560,-0.215" % (y0 - 0.010)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (tube, ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round"/>' % (tube, k.c("#8a2e24")))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.006" stroke-linecap="round" opacity="0.6" transform="translate(-0.004 -0.005)"/>' % (tube, k.c("#d0705a")))
    # nozzle
    o.append('<path d="M0.552,-0.228 L0.600,-0.252 L0.612,-0.226 L0.566,-0.200 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c(BRASS["base"]), ink))
    # case
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.018" fill="url(#%s_oxg)" stroke="%s" stroke-width="0.016"/>' % (x0, y0, x1 - x0, y1 - y0, u, ink))
    o.append('<rect x="%.3f" y="%.3f" width="%.3f" height="0.020" fill="%s" stroke="%s" stroke-width="0.010"/>' % (x0 - 0.006, y0 - 0.006, x1 - x0 + 0.012, k.c(BRASS["dark"]), ink))
    # window with the bottle and a dial
    o.append('<rect x="0.050" y="-0.080" width="0.150" height="0.140" rx="0.010" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#cfe6f2"), ink))
    o.append('<rect x="0.085" y="-0.070" width="0.080" height="0.122" rx="0.034" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c("#3f6fa8"), ink))
    o.append('<path d="M0.098,-0.055 L0.098,0.030" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.55"/>')
    o.append('<path d="M0.060,-0.072 L0.090,0.050" stroke="#ffffff" stroke-width="0.008" stroke-linecap="round" opacity="0.5"/>')
    o.append('<circle cx="0.262" cy="-0.030" r="0.036" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#f6f0e0"), ink))
    o.append('<path d="M0.262,-0.030 L0.282,-0.050" stroke="%s" stroke-width="0.007" stroke-linecap="round"/>' % k.c("#b8322a"))
    for (rx_, ry_) in ((0.034, y0 + 0.020), (0.306, y0 + 0.020), (0.034, y1 - 0.016), (0.306, y1 - 0.016)):
        o.append('<circle cx="%.4f" cy="%.4f" r="0.008" fill="%s" stroke="%s" stroke-width="0.005"/>' % (rx_, ry_, k.c(BRASS["shine"]), ink))
    # valve wheel on top + side handle under the hand
    o.append('<path d="M0.180,%.4f L0.180,%.4f" stroke="%s" stroke-width="0.016"/>' % (y0 - 0.006, y0 - 0.040, ink))
    o.append('<ellipse cx="0.180" cy="%.4f" rx="0.040" ry="0.012" fill="%s" stroke="%s" stroke-width="0.010"/>' % (y0 - 0.044, k.c("#2a2428"), ink))
    o.append('<path d="M0.022,-0.040 Q-0.010,-0.010 0.022,0.030" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % ink)
    for p in ((0.0, y0), (x1 + 0.01, y1), (0.62, -0.26), (0.47, -0.31), (0.0, y1 + 0.01), (0.18, y0 - 0.065)):
        k.ext.append((p[0], p[1], 0.02))
    return "".join(o)


OXY_TIP = (0.606, -0.240)          # nozzle end, relative to the hand (box held upright)
NEW_PROPS5 = ("flame_lamp", "oil_lamp_small", "pickaxe", "shovel", "oxygen_box", "cage")
# working point distance from the gripping hand (D): flame_lamp = flame (hangs upright below the hand), oil_lamp_small = the
# spout flame, pickaxe = centre of the iron head, shovel = blade edge, oxygen_box = nozzle (upright; see OXY_TIP), cage = base
# bottom (hangs upright: hand_for_tip("cage", (x, feet_y), 90) stands it on the floor)
NEW_TIP5 = {"flame_lamp": FLAME_IN[1] - 0.05, "oil_lamp_small": 0.10, "pickaxe": 0.80, "shovel": 0.92,
            "oxygen_box": math.hypot(*OXY_TIP), "cage": CAGE_H}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in NEW_PROPS5:
        return _O5["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    t = _POSE5["t"]
    if kind == "cage":
        B = _bird_norm(_POSE5["bird"] or {})
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        n0 = len(k.ext)
        svg, an = _cage(k, B)
        o.append(svg + '</g>')
        k.ext[n0:] = [(H[0] + e[0] * sc, H[1] + e[1] * sc, e[2] * sc) for e in k.ext[n0:]]
        bot = an["cage_bottom"]
        return "".join(o), (H[0] + bot[0] * sc, H[1] + bot[1] * sc)
    if kind in ("flame_lamp", "oil_lamp_small", "oxygen_box"):
        o = ['<g transform="translate(%.4f %.4f) scale(%.4f)">' % (H[0], H[1], sc)]
        n0 = len(k.ext)
        if kind == "flame_lamp":
            o.append(_flame_lamp(k, _POSE5["flame"], _POSE5["flame_blue"], t))
            tip = (0.0, FLAME_IN[1] - 0.05)
        elif kind == "oil_lamp_small":
            o.append(_oil_lamp(k, 0.0, 0.0, 1.0, max(0.3, _POSE5["flame"]), t))
            tip = (0.102, 0.040)
        else:
            o.append(_oxygen_box(k))
            tip = OXY_TIP
        o.append('</g>')
        k.ext[n0:] = [(H[0] + e[0] * sc, H[1] + e[1] * sc, e[2] * sc) for e in k.ext[n0:]]
        return "".join(o), (H[0] + tip[0] * sc, H[1] + tip[1] * sc)
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    if kind == "pickaxe":
        # ash handle along +x (gripped 0.22 from its butt), the curved iron head across its end: a point and a chisel blade
        o.append('<path d="M-0.22,-0.026 L0.82,-0.022 L0.82,0.022 L-0.22,0.028 Q-0.245,0 -0.22,-0.026 Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (k.c("#b8834a"), ink))
        o.append('<path d="M-0.18,-0.008 L0.76,-0.006" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % k.c("#e2b47e"))
        head = "M0.775,-0.050 Q0.740,-0.230 0.640,-0.360 Q0.790,-0.250 0.845,-0.050 L0.845,0.050 Q0.805,0.230 0.700,0.330 L0.690,0.290 Q0.760,0.180 0.775,0.050 Z"
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (head, k.c("#6c7480"), ink))
        o.append('<path d="M0.792,-0.040 Q0.760,-0.200 0.690,-0.300" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round" opacity="0.8"/>' % k.c("#b8c0ca"))
        o.append('<rect x="0.770" y="-0.055" width="0.080" height="0.110" rx="0.010" fill="%s" stroke="%s" stroke-width="0.012"/>' % (k.c("#4f5660"), ink))
        ends = ((-0.25, 0.0), (0.64, -0.37), (0.70, 0.34), (0.85, 0.0))
    else:  # shovel: wooden shaft with a D-grip at its butt, iron socket, rounded steel blade
        o.append('<path d="M-0.30,-0.020 L0.56,-0.020 L0.56,0.020 L-0.30,0.020 Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (k.c("#b07a44"), ink))
        o.append('<path d="M-0.30,-0.020 L-0.40,-0.075 L-0.44,0.0 L-0.40,0.075 L-0.30,0.020" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % ink)
        o.append('<path d="M-0.30,-0.020 L-0.40,-0.075 L-0.44,0.0 L-0.40,0.075 L-0.30,0.020" fill="none" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % k.c("#9a6a3a"))
        o.append('<path d="M0.52,-0.030 L0.62,-0.040 L0.62,0.040 L0.52,0.030 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#5a6068"), ink))
        blade = "M0.60,-0.110 L0.80,-0.120 Q0.94,-0.100 0.94,0.0 Q0.94,0.100 0.80,0.120 L0.60,0.110 Q0.62,0 0.60,-0.110 Z"
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (blade, k.c("#8c949e"), ink))
        o.append('<path d="M0.66,-0.085 L0.84,-0.090" stroke="#ffffff" stroke-width="0.010" stroke-linecap="round" opacity="0.45"/>')
        o.append('<path d="M0.88,-0.07 Q0.925,0 0.88,0.07" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>' % k.c("#3a3236"))
        ends = ((-0.45, 0.0), (0.94, -0.12), (0.94, 0.12), (0.60, 0.12), (-0.40, 0.08), (-0.40, -0.08))
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(NEW_TIP5[kind] * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


def bench_svg(uid="bn", width=1.1, height=0.42, ink=P.INK, tint=None):
    """a rough wooden bench / crate top for the pithead ending: top surface at y = 0 from -width/2 to +width/2, legs to the
    ground at y = height.  Put cage_svg()'s base bottom on (x, 0)."""
    k = P._Ctx(str(uid), ink, P._rgb(tint.lstrip("#")) if P._is_hex(tint) else None)
    w = width / 2.0
    o = []
    for x in (-w + 0.08, w - 0.08):
        o.append('<path d="M%.4f,0.04 L%.4f,%.4f L%.4f,%.4f L%.4f,0.04 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (x - 0.04, x - 0.05, height, x + 0.04, height, x + 0.04, k.c("#6e4a2c"), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % (-w + 0.10, height * 0.62, w - 0.10, height * 0.62, k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (-w + 0.10, height * 0.62, w - 0.10, height * 0.62, k.c("#7a5232")))
    o.append('<rect x="%.4f" y="-0.005" width="%.4f" height="0.075" rx="0.012" fill="%s" stroke="%s" stroke-width="0.018"/>' % (-w, width, k.c("#9a6a40"), k.ink))
    o.append('<path d="M%.4f,0.020 L%.4f,0.016 M%.4f,0.046 L%.4f,0.050" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (-w + 0.05, w - 0.20, -w + 0.30, w - 0.05, k.c("#6a4428")))
    return '<g id="%s_bench">%s</g>' % (k.uid, "".join(o))


# ============================================================================= face: soot, sideburns, cough
SOOT_SPOTS = {
    # (anchor, dx, dy, rx, ry, rotation, opacity) -- anchor "eL"/"eR" = below that eye (cheek), "m" = mouth, "c" = face centre
    "boy": (("eR", 0.030, 0.105, 0.105, 0.055, -12, 1.0), ("eL", -0.040, 0.120, 0.060, 0.035, 10, 0.75), ("c", 0.200, -0.240, 0.070, 0.040, 25, 0.6),
            ("m", -0.120, 0.120, 0.050, 0.030, -5, 0.55)),
    "heavy": (("eR", 0.040, 0.100, 0.115, 0.060, -10, 1.0), ("eL", -0.050, 0.105, 0.100, 0.055, 12, 0.9), ("c", -0.180, -0.230, 0.110, 0.045, -18, 0.75),
              ("m", 0.080, 0.110, 0.090, 0.045, 0, 0.7), ("c", 0.0, 0.060, 0.040, 0.050, 0, 0.5)),
    "light": (("eR", 0.050, 0.110, 0.080, 0.040, -10, 0.8), ("c", -0.220, -0.200, 0.070, 0.035, -15, 0.6)),
}
SOOT_STREAKS = {
    "boy": (("eR", -0.040, 0.085, 0.120, 0.125),),          # a finger-wipe across the cheek: from (dx0, dy0) to (dx1, dy1)
    "heavy": (("eL", -0.090, 0.070, 0.010, 0.140), ("eR", -0.020, 0.150, 0.110, 0.080)),
    "light": (),
}


def _soot(k, C, P_, L):
    S = C["soot"]
    col = k.c(S.get("color", "#3b3442"))
    op = _clamp(_num(S.get("op"), 0.45), 0.0, 1.0)
    kind = S.get("spots", "boy")
    u = k.uid
    k.defs.append('<radialGradient id="%s_st"><stop offset="0" stop-color="%s" stop-opacity="0.95"/><stop offset="0.55" stop-color="%s" stop-opacity="0.65"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (u, col, col, col))
    cx = (L["xL"] + L["xR"]) / 2.0
    A = {"eL": (L["xL"], L["ey"]), "eR": (L["xR"], L["ey"]), "m": (L["mx"], L["my"]), "c": (cx, L["ey"])}
    o = ['<g clip-path="url(#%s_hc)" opacity="%.3f">' % (u, op)]
    for (an, dx, dy, rx, ry, rot, a) in SOOT_SPOTS.get(kind, ()):
        x, y = A[an][0] + dx, A[an][1] + dy
        o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" transform="rotate(%d %.4f %.4f)" fill="url(#%s_st)" opacity="%.2f"/>'
                 % (x, y, rx, ry, rot, x, y, u, a))
    for (an, x0, y0, x1, y1) in SOOT_STREAKS.get(kind, ()):
        ax, ay = A[an]
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round" opacity="0.55"/>'
                 % (ax + x0, ay + y0, ax + (x0 + x1) / 2, ay + (y0 + y1) / 2 + 0.02, ax + x1, ay + y1, col))
    o.append('</g>')
    return "".join(o)


def _sideburns(k, C, P_, L):
    """thick bushy sideburns from under the hat down to the jaw on both sides, clipped to the head fill, combed hair strokes."""
    SB = C["sideburns"]
    col, dk = k.c(SB["color"]), k.c(SB.get("dark", P._shade(SB["color"], 0.65)))
    cx = (L["xL"] + L["xR"]) / 2.0
    o = ['<g clip-path="url(#%s_hc)">' % k.uid]
    for s in (-1, 1):
        f = _clamp(1.0 - 0.55 * max(0.0, s * P_["yaw"]), 0.35, 1.0)        # the side the face turns toward gets narrower
        x0 = s * 0.56 + cx * 0.35
        w = 0.20 * f
        pts = [(x0, -0.30), (x0 - s * (w + 0.02), -0.28), (x0 - s * (w + 0.01), -0.10), (x0 - s * (w + 0.06), 0.06), (x0 - s * (w + 0.09), 0.17),
               (x0 - s * (w + 0.02), 0.25), (x0 - s * 0.02, 0.24), (x0 + s * 0.05, 0.10)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), col, k.ink))
        st = "".join("M%.4f,%.4f q%.4f,0.06 %.4f,0.11 " % (x0 - s * (w * fr + 0.02), -0.20 + 0.12 * j, -s * 0.02, -s * 0.03)
                     for fr in (0.35, 0.75) for j in range(3))
        o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % (st, dk))
    o.append('</g>')
    return "".join(o)


def _cough(k, P_, L, ph):
    """three small dust puffs coughed out in front of the mouth (toward the facing side); ph = phase 0..1 (they drift out)."""
    side = 1.0 if P_["yaw"] >= 0.0 else -1.0
    o = []
    for i in range(3):
        f = _frac(ph + i / 3.0)
        x = L["mx"] + side * (0.16 + 0.22 * f + 0.02 * i)
        y = L["my"] - 0.02 - 0.10 * f + 0.03 * i
        r = 0.035 + 0.040 * f
        a = 0.85 * (1.0 - _smooth(0.65, 1.0, f))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="0.012" opacity="%.3f"/>' % (x, y, r, k.c("#c9c2c8"), k.ink, a))
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" opacity="%.3f"/>' % (x + side * r * 0.5, y - r * 0.3, r * 0.6, k.c("#e6e0e4"), a))
        k.ext.append((x, y, r + 0.01))
    return "".join(o)


def _face(k, C, P_, white):
    svg, L = _O5["_face"](k, C, P_, white)
    if C is None or not C.get("_cast5"):
        return svg, L
    under, over = [], []
    if C.get("sideburns"):
        under.append(_sideburns(k, C, P_, L))
    if C.get("soot"):
        under.append(_soot(k, C, P_, L))
    if _POSE5["cough"] is not None:
        over.append(_cough(k, P_, L, _POSE5["cough"]))
    if not under and not over:
        return svg, L
    return "".join(under) + svg + "".join(over), L


def _norm(C, pose):
    g = pose.get if isinstance(pose, dict) else (lambda key, d=None: d)
    _POSE5["flame"] = _f(g("flame"), 1.0, 0.0, 2.0)
    _POSE5["flame_blue"] = _f(g("flame_blue"), 0.0, 0.0, 1.0)
    b = g("bird")
    _POSE5["bird"] = b if isinstance(b, (dict, str)) else None
    c = g("cough")
    if c is None or c is False:
        _POSE5["cough"] = None
    elif c is True:
        _POSE5["cough"] = 0.0
    else:
        v = _num(c, float("nan"))
        _POSE5["cough"] = _frac(v) if math.isfinite(v) else None
    _POSE5["t"] = _num(g("t"), 0.0)
    return _O5["_norm"](C, pose)


# ============================================================================= costumes (torso-local)
def _patch(k, X, x, y, w, h, col, rot):
    c = X(x, y)
    return ('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.010" fill="%s" stroke="%s" stroke-width="0.011" transform="rotate(%d %.4f %.4f)"/>'
            '<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.006" fill="none" stroke="%s" stroke-width="0.007" stroke-dasharray="0.016 0.011" '
            'transform="rotate(%d %.4f %.4f)" opacity="0.9"/>'
            % (c[0] - w / 2, c[1] - h / 2, w, h, k.c(col), k.ink, rot, c[0], c[1],
               c[0] - w / 2 + 0.014, c[1] - h / 2 + 0.014, w - 0.028, h - 0.028, k.c("#efe6d0"), rot, c[0], c[1]))


def _kerchief(k, X, col, dark, knot_x=0.05):
    """neckerchief tied at the throat: a band round the neck line, a knot and a small triangle hanging below it."""
    o = []
    band = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (X(-0.24, 0.392) + X(0.0, 0.47) + X(0.24, 0.392))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.092" stroke-linecap="round"/>' % (band, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (band, k.c(col)))
    kx, ky = X(knot_x, 0.455)
    tri = [(kx - 0.060, ky), (kx + 0.065, ky + 0.004), (kx + 0.012, ky + 0.135)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (_poly_d(tri), k.c(col), k.ink))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % (kx - 0.02, ky + 0.02, kx + 0.008, ky + 0.10, k.c(dark)))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.042" ry="0.034" fill="%s" stroke="%s" stroke-width="0.013"/>' % (kx, ky, k.c(col), k.ink))
    k.ext.append((kx, ky + 0.15, 0.02))
    return "".join(o)


def _cos_pit(k, C, m):
    """pit clothes: collarless work shirt (neck band, two-button placket), optional braces (colors susp), optional waistcoat
    (colors vest: open with a gap C["vest_gap"], lapels, buttons, welt pockets, sewn patches C["patches"], hem lowered by
    C["vest_hem"] for the oversized one), a leather belt with a buckle on the trouser bowl, optional neckerchief (colors
    kerchief), optional small oil lamp hanging from the belt at the hip (C["belt_lamp"])."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    hw = m.hwa
    o = [CE._bowl(k, col["pants"], yb, yB)]
    # belt on the trouser top
    if col.get("belt"):
        o.append(_ln([X(-1.0, yb + 0.030), X(1.0, yb + 0.030)], k.ink, 0.066))
        o.append(_ln([X(-1.0, yb + 0.030), X(1.0, yb + 0.030)], k.c(col["belt"]), 0.044))
        bx, by = X(0.0, yb + 0.030)
        o.append('<rect x="%.4f" y="%.4f" width="0.072" height="0.060" rx="0.010" fill="none" stroke="%s" stroke-width="0.024"/>' % (bx - 0.036, by - 0.030, k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.072" height="0.060" rx="0.010" fill="none" stroke="%s" stroke-width="0.012"/>' % (bx - 0.036, by - 0.030, k.c(col.get("buckle", "#c9a24a"))))
    # shirt: neck band and placket
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034"/>' % (X(-0.17, 0.386) + X(0.0, 0.47) + X(0.17, 0.386) + (k.c(col["shirt_d"]),)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010"/>' % (X(-0.17, 0.404) + X(0.0, 0.49) + X(0.17, 0.404) + (k.ink,)))
    o.append(_ln([X(0.0, 0.47), X(0.0, 0.66)], k.c(col["shirt_d"]), 0.012))
    for y in (0.52, 0.61):
        o.append(_circ(X(0.0, y), 0.013, k.c("#f4efe4"), k, 0.006))
    if col.get("susp"):
        o.append(C3._suspenders(k, X, col, 0.40, yb + 0.05, xs=C.get("susp_x", 0.12)))
    if col.get("vest"):
        gap = C.get("vest_gap", 0.04)
        hem = C.get("vest_hem", 0.0)
        g = C2._grad(k, "vs", col["vest"], -hw, hw)
        for s in (-1, 1):
            pts = [X(s * 1.0, 0.30), X(s * 0.215, 0.370), X(s * gap, 0.700), X(s * gap, yb + 0.040 + hem), X(s * (gap + 0.10), yb + 0.065 + hem),
                   X(s * 0.55, yb + 0.010 + hem * 0.5), X(s * 1.0, yb - 0.010 + hem * 0.3)]
            o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(pts), g, k.ink))
            lap = [X(s * 0.215, 0.370), X(s * 0.330, 0.400), X(s * (gap + 0.05), 0.640), X(s * gap, 0.700)]
            o.append(_poly(k, lap, k.c(col["vest_d"]), 0.012))
            o.append(_ln([X(s * 0.22, 0.90), X(s * 0.38, 0.895)], k.c(col["vest_d"]), 0.022))
            o.append(_ln([X(s * 0.22, 0.90), X(s * 0.38, 0.895)], k.ink, 0.007, ' opacity="0.6"'))
        bxs = gap + 0.035
        for i in range(4):
            y = 0.74 + i * (yb - 0.03 + hem * 0.5 - 0.74) / 3.0
            o.append(_circ(X(bxs, y), 0.018, k.c(col.get("button", "#d9b45a")), k, 0.007))
            o.append(_ln([X(-bxs - 0.012, y), X(-bxs + 0.012, y)], k.c(col["vest_d"]), 0.010))
        for (px, py, pw, ph, pc, pr) in C.get("patches", ()):
            o.append(_patch(k, X, px, py, pw, ph, pc, pr))
    inside = "".join(o)
    ov = []
    if col.get("kerchief"):
        ov.append(_kerchief(k, X, col["kerchief"], col.get("kerchief_d", "#5a1a14"), C.get("knot_x", 0.05)))
    if C.get("belt_lamp"):
        lx, ly = X(hw * 0.80, yb + 0.040)
        ov.append(_ln([(lx - 0.02, ly - 0.03), (lx, ly)], k.ink, 0.020))
        ov.append(_oil_lamp(k, lx, ly, 0.95, 0.8, _POSE5["t"]))
    return inside, "", "".join(ov)


def _cos_gaffercoat(k, C, m):
    """gaffer: long dark-navy wool coat hanging open (wide lapels, brass buttons, flap pockets on the skirt to the knee) over an
    ox-blood waistcoat with a brass watch chain, a collarless grey shirt and a mustard neckerchief."""
    X = _X(m)
    col = C["colors"]
    h = C["torso_h"]
    yB = TT + h
    yb = yB - P.BOWL_H
    o = [CE._bowl(k, col["pants"], yb, yB)]
    # the opening: waistcoat strip down the middle, shirt V at the top
    strip = [X(-0.21, 0.36), X(0.21, 0.36), X(0.32, yb + 0.12), X(-0.32, yb + 0.12)]
    o.append(_poly(k, strip, k.c(col["vest"]), 0.0, "none"))
    o.append(_poly(k, [X(-0.15, 0.37), X(0.15, 0.37), X(0.0, 0.62)], k.c(col["shirt"]), 0.012))
    o.append(_ln([X(-0.14, 0.38), X(0.0, 0.60), X(0.14, 0.38)], k.c(col["vest_d"]), 0.024))
    ys = [0.70 + i * (yb + 0.02 - 0.70) / 4.0 for i in range(5)]
    o.append(_ln([X(0.0, 0.62), X(0.0, yb + 0.10)], k.ink, 0.010, ' opacity="0.7"'))
    for y in ys:
        o.append(_circ(X(0.03, y), 0.020, k.c(col["brass"]), k, 0.008))
    a0, a1 = X(0.03, ys[2]), X(0.25, ys[3] + 0.02)
    cm = X(0.16, ys[2] + 0.12)
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (a0 + cm + a1)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.026" stroke-linecap="round"/>' % (d, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.013" stroke-linecap="round" stroke-dasharray="0.018 0.010"/>' % (d, k.c(col["brass"])))
    # coat fronts with wide lapels
    for s in (-1, 1):
        lap = [X(s * 0.17, 0.365), X(s * 0.44, 0.40), X(s * 0.36, 0.60), X(s * 0.30, 0.74), X(s * 0.215, 0.64)]
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(lap), k.c(col["lapel"]), k.ink))
        o.append(_ln([X(s * 0.215, 0.64), X(s * 0.30, yb + 0.12)], k.ink, 0.022))
        for y in (0.82, 0.98):
            o.append(_circ(X(s * 0.40, y), 0.024, k.c(col["brass"]), k, 0.008))
        o.append(_ln([X(s * 0.50, 0.66), X(s * 0.62, 0.66)], k.c(col["dark"]), 0.016))
    inside = "".join(o)
    # coat skirt: two panels from the open front edge to the flared sides, the trousers show between them
    yt = yb - 0.03
    a = m.hwa * 0.985
    hem = yB + C.get("coat_len", 0.42)
    fl = C.get("coat_flare", 0.10)
    g = "url(#%s_tg)" % k.uid
    ov = []
    for s in (-1, 1):
        pts = [X(s * a, yt), X(s * (a + fl * 0.6), (yt + hem) / 2), X(s * (a + fl), hem), X(s * 0.25, hem + 0.015), X(s * 0.30, yt)]
        ov.append('<path d="%s" fill="%s"/>' % (_poly_d(pts), g))
        ov.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
                  % (pts[0] + pts[1] + pts[2] + pts[3] + pts[4] + (k.ink,)))
        fx0, fx1 = 0.36, 0.62
        flap = [X(s * fx0, yt + 0.08), X(s * fx1, yt + 0.08), X(s * (fx1 - 0.01), yt + 0.15), X(s * (fx0 + 0.01), yt + 0.15)]
        ov.append(_poly(k, flap, k.c(col["dark"]), 0.013))
        ov.append(_ln([X(s * 0.29, yt + 0.06), X(s * 0.26, hem - 0.02)], k.c(col["dark"]), 0.012, ' opacity="0.8"'))
        k.ext.append((pts[2][0], pts[2][1], 0.04))
    ov.append(_kerchief(k, X, col["kerchief"], col["kerchief_d"], 0.02))
    return inside, "", "".join(ov)


COSTUMES5 = {"pit": _cos_pit, "gaffercoat": _cos_gaffercoat}


# ============================================================================= hats (head frame)
def _ext_hat(k, C, pts, r=0.02):
    t = C["hat_tilt"]
    for p in pts:
        k.ext.append(_rot(p[0], p[1], t) + (r,))


def _hat_leatherhelmet(k, C, yaw):
    """gaffer: hard tan leather pit helmet -- a tall rounded dome with a raised comb running front to back (it slides to the
    facing side with yaw), a stitched band, a narrow brim all round, and a brass lamp bracket (plate + hook) on the front."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    cx = dx + 0.20 * yaw
    yb, top = -0.300, -0.840
    rx, ry = 0.590, 0.078
    g = CE._gradient(k, "ht", col, x0=-0.46, x1=0.46, mid=0.30)
    gb = CE._gradient(k, "hb", dict(light=col["brim_l"], base=col["brim"], dark=col["dark"]), x0=-rx, x1=rx, mid=0.35)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.028"/>' % (dx, yb, rx, ry, gb, k.ink))
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z"
            % (dx - 0.445, yb + 0.005, dx - 0.475, yb - 0.330, cx - 0.300, top, cx, top, cx + 0.300, top, dx + 0.475, yb - 0.330, dx + 0.445, yb + 0.005))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.032" stroke-linejoin="round"/>' % (dome, g, k.ink))
    # comb (raised ridge)
    comb = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (cx - 0.02 * yaw, top + 0.004, cx + 0.03 * yaw, (top + yb) / 2, dx + 0.26 * yaw, yb - 0.075)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.076" stroke-linecap="round"/>' % (comb, k.ink))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>' % (comb, k.c(col["light"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8" transform="translate(-0.010 0)"/>' % (comb, k.c(col["shine"])))
    # shine streak on the dome
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.8"/>'
             % (dx - 0.37, yb - 0.11, dx - 0.33, top + 0.20, cx - 0.14, top + 0.05, k.c(col["shine"])))
    # stitched band
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.048"/>' % (dx - 0.455, yb - 0.050, dx, yb - 0.010, dx + 0.455, yb - 0.050, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.008" stroke-dasharray="0.020 0.014" opacity="0.9"/>'
             % (dx - 0.44, yb - 0.052, dx, yb - 0.012, dx + 0.44, yb - 0.052, k.c(col["stitch"])))
    # front lip of the brim
    o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 0 0 %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
             % (dx - rx, yb, rx, ry, dx + rx, yb, dx, yb + ry * 0.35, dx - rx, yb, gb, k.ink))
    # lamp bracket on the front: brass plate, two rivets, a hook
    bx, by = dx + 0.26 * yaw, yb - 0.150
    bw = 0.050 * (1.0 - 0.35 * abs(yaw))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>' % (bx, by - 0.060, bx, by - 0.115, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (bx, by - 0.110, bx + 0.040, by - 0.150, bx + 0.010, by - 0.175, k.c(col["brass"])))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % (bx, by - 0.060, bx, by - 0.115, k.c(col["brass"])))
    o.append('<rect x="%.4f" y="%.4f" width="%.4f" height="0.120" rx="0.016" fill="%s" stroke="%s" stroke-width="0.014"/>' % (bx - bw, by - 0.070, 2 * bw, k.c(col["brass"]), k.ink))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>' % (bx, by - 0.040, k.c(col["dark"]), bx, by + 0.020, k.c(col["dark"])))
    o.append('</g>')
    _ext_hat(k, C, ((dx - rx - 0.03, yb), (dx + rx + 0.03, yb), (cx, top - 0.03), (bx + 0.03, by - 0.19), (dx, yb + ry + 0.02)))
    return "".join(o), (cx, top)


def _hat_capback(k, C, yaw):
    """miner3: a flat cloth cap worn back to front -- the soft crown puffs toward the back, the short peak sticks out behind the
    head on the side away from the face (a stub over the far ear when seen from the front)."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    s = -1.0 if yaw >= 0.0 else 1.0
    e = 0.08 + 0.26 * _smooth(0.0, 0.9, abs(yaw))
    xl, xr, yb = -0.465 + dx, 0.465 + dx, -0.262
    ox = -0.06 * yaw
    g = CE._gradient(k, "ht", col, x0=-0.50, x1=0.50, mid=0.30)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    # the peak behind the head
    px0 = dx + s * 0.30
    peak = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (px0, yb - 0.070, dx + s * (0.50 + e * 0.5), yb - 0.115, dx + s * (0.47 + e), yb - 0.035,
               dx + s * (0.48 + e * 0.6), yb + 0.005, dx + s * 0.40, yb - 0.005, px0, yb - 0.030, px0, yb - 0.070))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (peak, k.c(col["visor"]), k.ink))
    top = P._smooth_open([(xl, yb), (xl - 0.03, yb - 0.12), (dx - 0.20 + ox, -0.555), (dx + 0.10 + ox, -0.565), (xr + 0.02, -0.46), (xr + 0.03, yb - 0.08), (xr, yb)])
    d = top + " Q%.4f,%.4f %.4f,%.4f Z" % (dx, yb + 0.030, xl, yb)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, g, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
             % (xl + 0.02, yb - 0.05, dx, yb - 0.02, xr - 0.02, yb - 0.05, k.c(col["dark"])))
    bx, by = dx - 0.02 + ox, -0.570
    for f in (-1, 1):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.8"/>'
                 % (bx, by + 0.02, bx + f * 0.24, by + 0.07, dx + f * 0.36, yb - 0.07, k.c(col["dark"])))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
             % (xl + 0.03, yb - 0.10, dx - 0.30, -0.50, dx - 0.10, -0.55, k.c(col["shine"])))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.040" ry="0.024" fill="%s" stroke="%s" stroke-width="0.011"/>' % (bx, by + 0.012, k.c(col["dark"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.06, yb - 0.1), (xr + 0.06, yb - 0.06), (dx, by - 0.04), (dx + s * (0.50 + e), yb - 0.06)))
    return "".join(o), (bx, by)


def _hat_kerchief(k, C, yaw):
    """miner2: a red spotted kerchief tied tight over the crown (a low cap down to the brows), knot and two short tails on the
    side away from the face."""
    col = C["hat_colors"]
    dx = -0.03 * yaw
    u = k.uid
    xl, xr, yb, top = -0.478 + dx, 0.478 + dx, -0.215, -0.585
    d = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (xl, yb, xl - 0.03, yb - 0.25, dx - 0.30, top, dx, top, dx + 0.30, top, xr + 0.03, yb - 0.25, xr, yb, dx, yb - 0.075, xl, yb))
    k.defs.append('<pattern id="%s_kd" width="0.11" height="0.11" patternUnits="userSpaceOnUse"><circle cx="0.03" cy="0.03" r="0.014" fill="%s"/>'
                  '<circle cx="0.085" cy="0.085" r="0.014" fill="%s"/></pattern><clipPath id="%s_kc"><path d="%s"/></clipPath>'
                  % (u, k.c(col["dot"]), k.c(col["dot"]), u, d))
    g = CE._gradient(k, "ht", col, x0=-0.50, x1=0.50, mid=0.32)
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    s = -1.0 if yaw >= 0 else 1.0
    f = _clamp(0.35 + abs(yaw), 0.35, 1.0)
    kx, ky = s * (0.46 - 0.08 * (1 - f)) + dx, -0.30
    tails = []
    for (ang, ln) in ((30.0, 0.24), (70.0, 0.20)):
        ex, ey = kx + s * ln * math.cos(math.radians(ang)) * f, ky + ln * math.sin(math.radians(ang))
        tl = [(kx, ky - 0.03), (ex + s * 0.03, ey - 0.01), (ex - s * 0.01, ey + 0.04), (kx, ky + 0.03)]
        tails.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (_poly_d(tl), k.c(col["base"]), k.ink))
        k.ext.append((ex + s * 0.03, ey + 0.04, 0.03))
    o.extend(tails)
    o.append('<path d="%s" fill="%s"/>' % (d, g))
    o.append('<g clip-path="url(#%s_kc)"><rect x="-0.7" y="-0.7" width="1.4" height="0.6" fill="url(#%s_kd)" opacity="0.9"/></g>' % (u, u))
    for fr in (-0.5, 0.1, 0.6):
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" opacity="0.7"/>'
                 % (dx + fr * 0.40, top + 0.06, dx + fr * 0.55 + s * 0.06, -0.42, kx * 0.9, ky + 0.01, k.c(col["dark"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.028" stroke-linejoin="round"/>' % (d, k.ink))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>'
             % (xl + 0.06, yb - 0.10, xl + 0.12, top + 0.10, dx - 0.15, top + 0.03, k.c(col["light"])))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.055" ry="0.048" fill="%s" stroke="%s" stroke-width="0.016"/>' % (kx, ky, k.c(col["base"]), k.ink))
    o.append('</g>')
    _ext_hat(k, C, ((xl - 0.03, yb), (xr + 0.03, yb), (dx, top - 0.03), (kx + s * 0.06, ky)))
    return "".join(o), (dx, top)


HATS5 = {"leatherhelmet": _hat_leatherhelmet, "capback": _hat_capback, "kerchief": _hat_kerchief}


# ============================================================================= cast
NEW_CAST5 = {
    # the hero: the youngest miner (0.8 of the adults): oversized patched brick-red waistcoat over a collarless shirt, braces,
    # rolled sleeves, short trousers, big boots, slate tweed flat cap, ginger hair, soot on the cheeks, oil lamp on the belt
    "alfie": dict(
        _cast5=True, _cast4=True, build="boy", seed=17.7,
        torso_w=0.66, torso_h=0.80, profile=C2.PROFILE_BOY, shift_pow=1.0,
        shoulder=(0.25, 0.50), arm=C2.BOY_ARM, hip_x=0.15, leg=0.82, stance=0.07, wide=0.24, limb_w=0.054,
        eye_y=0.055, brow="dome", brow_th=0.036, mouth="dash", moustache=False, smirk_side=1, cheeks="#f2a090",
        hat="newsboy", hat_style="flatnews", hat_tilt=-6.0, ear_pencil=False, cap_puff=1.30,
        hat_colors=dict(light="#77737e", base="#4f4b57", dark="#302d36", shine="#9a96a2", visor="#3c3944"),
        hair=dict(color="#b85a2a", front=0.08, grow=0.16),
        soot=dict(color="#3b3442", op=0.55, spots="boy"),
        costume="pit", vest_gap=0.12, vest_hem=0.07, belt_lamp=True, susp_x=0.075,
        patches=((0.33, 0.93, 0.13, 0.11, "#56708c", 8), (-0.34, 0.66, 0.11, 0.10, "#b08a5a", -7)),
        sleeve=dict(color="#e4ddca", dark="#b5ab94", cuff="#efe9da", len=0.56, w=0.150, roll=True),
        shorts=dict(color="#4f4a52", dark="#35313a", cuff="#5d5860", len=0.50, w=0.17),
        boots=dict(color="#3a2a22", cuff="#57402e", h=0.17, toe=0.18, soft=True),
        colors=dict(base="#e4ddca", shirt_d="#b5ab94", vest="#a4483a", vest_d="#6a2a20", button="#d9b45a", susp="#5a3a26", susp_b="#c9a24a",
                    belt="#3a2a22", buckle="#c9a24a", pants="#4f4a52"),
    ),
    # the foreman: big, barrel-chested; tan leather pit helmet with a lamp bracket, bushy sideburns and walrus moustache,
    # long navy coat hanging open over an ox-blood waistcoat, mustard neckerchief
    "gaffer": dict(
        _cast5=True, build="stout", seed=41.2,
        torso_w=1.24, torso_h=1.14, profile=C2.PROFILE_ROUND, shift_pow=1.25,
        shoulder=(0.45, 0.44), arm=0.74, hip_x=0.17, leg=1.30, stance=0.06, wide=0.26, limb_w=0.072,
        eye_y=-0.020, brow="stroke", brow_th=0.078, mouth="frown", moustache=True, moustache_style="bushy", tache_scale=1.12,
        smirk_side=-1, cheeks="#ec8c7a",
        sideburns=dict(color="#6a4430", dark="#3e2618"),
        soot=dict(color="#3b3442", op=0.30, spots="light"),
        hat="newsboy", hat_style="leatherhelmet", hat_tilt=-3.0, ear_pencil=False,
        hat_colors=dict(light="#cf9a5e", base="#9c6630", dark="#5e3a1a", shine="#f0c690", brim="#7e4e24", brim_l="#a8703c", stitch="#f0d8a4",
                        brass="#e0b24a"),
        hair=dict(color="#6a4430", front=0.05, grow=0.22),
        costume="gaffercoat", coat_len=0.46, coat_flare=0.11,
        sleeve=dict(color="#36425a", dark="#222b3c", cuff="#28324a", len=0.80, w=0.205),
        boots=dict(color="#2a221e", cuff="#2a221e", h=0.12, toe=0.15),
        colors=dict(base="#36425a", dark="#222b3c", lapel="#28324a", vest="#7a2a2a", vest_d="#4e1616", shirt="#d6d0c4", brass="#e0b24a",
                    kerchief="#d0a03a", kerchief_d="#8a6416", pants="#3e3a40", moustache="#6a4430", moustache_l="#9a6c50"),
    ),
    # miners
    "miner1": dict(   # tall, heavy soot, navy knitted cap, slate shirt, braces, pick-axe
        _cast5=True, build="slim", seed=23.9,
        torso_w=0.66, torso_h=1.04, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.26, 0.50), arm=0.76, hip_x=0.17, leg=1.42, stance=0.08, wide=0.30, limb_w=0.058,
        eye_y=0.030, brow="stroke", brow_th=0.052, mouth="dash", moustache=False, smirk_side=1,
        soot=dict(color="#332d3a", op=0.60, spots="heavy"),
        hat="newsboy", hat_style="skullcap", hat_tilt=-2.0, ear_pencil=False,
        hat_colors=dict(light="#56668a", base="#33405e", dark="#1e263c", shine="#7a8aac", cuff="#3e4c6c", stitch="#a6b0c8"),
        hair=dict(color="#2a2226", front=0.07, grow=0.22),
        costume="pit",
        sleeve=dict(color="#7a828e", dark="#525862", cuff="#8a929e", len=0.54, w=0.140, roll=True),
        boots=dict(color="#2e2622", cuff="#2e2622", h=0.12, toe=0.15),
        colors=dict(base="#7a828e", shirt_d="#59606a", susp="#3a2a22", susp_b="#9a8a6a", belt="#2a2020", buckle="#9aa0a8", pants="#3a3842"),
    ),
    "miner2": dict(   # short and stocky, black beard and moustache, red spotted kerchief cap, leather jerkin, shovel
        _cast5=True, _cast3=True, build="regular", seed=26.3,
        torso_w=0.94, torso_h=0.98, profile=CE.PROFILE_REGULAR, shift_pow=1.1,
        shoulder=(0.34, 0.47), arm=0.72, hip_x=0.17, leg=1.06, stance=0.08, wide=0.30, limb_w=0.066,
        eye_y=0.000, brow="stroke", brow_th=0.060, mouth="dash", moustache=True, moustache_style="bushy", tache_scale=0.85, smirk_side=-1,
        beard=dict(color="#4a3428", dark="#2a1a12"),
        soot=dict(color="#332d3a", op=0.45, spots="light"),
        hat="newsboy", hat_style="kerchief", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#d8584a", base="#b8322a", dark="#7a1e18", dot="#f4e8d0"),
        hair=dict(color="#4a3428", front=0.05, grow=0.22),
        costume="pit", vest_gap=0.06,
        sleeve=dict(color="#d8ceb4", dark="#aa9e84", cuff="#e6decc", len=0.50, w=0.155, roll=True),
        boots=dict(color="#2e2622", cuff="#2e2622", h=0.11, toe=0.15),
        colors=dict(base="#d8ceb4", shirt_d="#aa9e84", vest="#7a5636", vest_d="#4e341e", button="#c9b08a", belt="#2a2020", buckle="#c9a24a",
                    pants="#4a4038", moustache="#4a3428", moustache_l="#7a5a44"),
    ),
    "miner3": dict(   # lanky young man, flat cap back to front, sandy hair, oatmeal shirt, green braces, red neckerchief
        _cast5=True, build="slim", seed=19.4,
        torso_w=0.58, torso_h=1.06, profile=CE.PROFILE_ATHLETE, shift_pow=1.0,
        shoulder=(0.23, 0.50), arm=0.78, hip_x=0.15, leg=1.46, stance=0.07, wide=0.28, limb_w=0.052,
        eye_y=0.050, brow="stroke", brow_th=0.040, mouth="smirk", moustache=False, smirk_side=1, freckles=True,
        soot=dict(color="#3b3442", op=0.45, spots="boy"),
        hat="newsboy", hat_style="capback", hat_tilt=4.0, ear_pencil=False,
        hat_colors=dict(light="#8a9070", base="#636a4a", dark="#3e432e", shine="#b0b690", visor="#4e5438"),
        hair=dict(color="#c48a4a", front=0.08, grow=0.20),
        costume="pit", susp_x=0.11, knot_x=-0.04,
        sleeve=dict(color="#cbb68c", dark="#9a8660", cuff="#d8c6a0", len=0.52, w=0.130, roll=True),
        boots=dict(color="#3a2c26", cuff="#3a2c26", h=0.11, toe=0.15),
        colors=dict(base="#cbb68c", shirt_d="#9a8660", susp="#3e5a3a", susp_b="#c9a24a", belt="#3a2a22", buckle="#c9a24a",
                    kerchief="#c0362c", kerchief_d="#7a1a14", pants="#5a4636"),
    ),
}

# feet-relative sprite canvases (x0, y0, x1, y1), y down, snapped to 1/16 D (python3 test_cast5.py canvas): every arm preset with
# every film-5 prop at yaw +-0.6 (mirrored), squash 0.8..1.15, crouch, wide legs, all effects and every STORY5 pose of the member;
# >= 0.32 D head room.  The creatures: every state, 5 notes, swing +-40, lie 0..1.
CANVAS5 = {
    "alfie": (-1.8750, -3.8750, 1.8750, 0.1875),
    "gaffer": (-2.1250, -4.7500, 2.1250, 0.1250),
    "miner1": (-1.9375, -4.8750, 1.9375, 0.1250),
    "miner2": (-2.0000, -4.3125, 2.0000, 0.1250),
    "miner3": (-1.9375, -4.9375, 1.9375, 0.1250),
    "canary": (-0.7500, -1.1250, 0.7500, 0.1250),
    "canary_in_cage": (-1.0625, -1.3125, 1.0625, 0.2500),
}


# ============================================================================= creature figures ("canary", "canary_in_cage")
CANARY_FEET = 0.10        # standalone canary: the feet / floor line is 0.10 D below the origin


def _creature(name, pose, uid):
    """same return dict as puppet.figure(): svg in D units, feet_y, bbox, anchors (feet, hip, head, head_top, hat_top, chest,
    beak, eye, bird_head, bird_body, bird_feet; the cage adds ring, perch, cage_floor, cage_bottom, cage_top, hand_r, hand_l)."""
    B = _bird_norm(pose)
    k = P._Ctx(str(uid), B["ink"], B["tint"])
    sc = B["scale"]
    if name == "canary":
        svg, an = _bird(k, B, 0.0, CANARY_FEET, 1.0)
        feet_y = CANARY_FEET
    else:
        svg, an = _cage(k, B)
        feet_y = CAGE_H * math.cos(math.radians(B["swing"]))
        an["hand_r"] = an["hand_l"] = (0.0, 0.0)
    an["feet"] = (0.0, feet_y)
    an["head"] = an["bird_head"]
    an["head_top"] = (an["bird_head"][0], an["bird_head"][1] - BIRD_HR)
    an["hat_top"] = an["head_top"]
    an["chest"] = an["bird_body"]
    an["hip"] = (0.0, feet_y - (0.10 if name == "canary" else 0.30))
    an["mouth"] = an["beak"]
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for (x, y, r) in k.ext:
        x0, y0, x1, y1 = min(x0, x - r), min(y0, y - r), max(x1, x + r), max(y1, y + r)
    y1 = max(y1, feet_y)
    if B["mirror"]:
        svg = '<g transform="scale(-1 1)">%s</g>' % svg
        x0, x1 = -x1, -x0
        an = dict((n, (-v[0], v[1])) for n, v in an.items())
    pad = 0.02
    bbox = ((x0 - pad) * sc, (y0 - pad) * sc, (x1 + pad) * sc, (y1 + pad) * sc)
    an = dict((n, (v[0] * sc, v[1] * sc)) for n, v in an.items())
    out = '<g id="%s_fig" transform="scale(%.4f)"><defs>%s</defs>%s</g>' % (k.uid, sc, "".join(k.defs), svg)
    return {"svg": out, "feet_y": feet_y * sc, "bbox": bbox, "anchors": an}


def figure(cast_name, pose=None, uid="p"):
    if isinstance(cast_name, str) and cast_name in CREATURES:
        return _creature(cast_name, pose, uid)
    return _O5["figure"](cast_name, pose, uid)


def resolve_pose(cast_name, pose=None):
    if isinstance(cast_name, str) and cast_name in CREATURES:
        B = _bird_norm(pose)
        out = dict((key, B[key]) for key in ("state",) + BIRD_KEYS + ("mirror",))
        if pose and isinstance(pose, dict):
            for key in ("ink", "tint"):
                if key in pose:
                    out[key] = pose[key]
        return out
    return _O5["resolve_pose"](cast_name, pose)


def lerp_pose(cast_name, a, b, t):
    """creatures: numbers interpolate, the state name (and mirror) switch at t = 0.5."""
    if isinstance(cast_name, str) and cast_name in CREATURES:
        t = _f(t, 0.0, 0.0, 1.0)
        A, Bq = _bird_norm(a), _bird_norm(b)
        out = dict(state=A["state"] if t < 0.5 else Bq["state"], mirror=A["mirror"] if t < 0.5 else Bq["mirror"])
        for key in BIRD_KEYS:
            out[key] = A[key] + (Bq[key] - A[key]) * t
        return out
    return _O5["lerp_pose"](cast_name, a, b, t)


CANARY5 = dict((n, dict(state=n)) for n in STATES)
CANARY5["perch_sing"] = dict(state="perch_sing", notes=5)


# ============================================================================= story poses
def _feet_y(cast, pose):
    return P.figure(cast, pose, "q")["feet_y"]


MINERS = (("miner1", ""), ("miner2", "_miner2"), ("miner3", "_miner3"))
LAMP = dict(type="flame_lamp", scale=1.25)


def _story():
    S, M = {}, {}
    # --- alfie
    S["alfie_hold_cage"] = ("alfie", dict(yaw=0.40, pitch=-0.15, expr="happy", head_roll=-6, gaze=(0.8, -0.2), legs="wide",
                                          arm_r=dict(hand=(0.66, -0.20), bend=-0.9, stretch=1.3), prop_r="cage",
                                          arm_l="akimbo", bird=dict(state="perch_sing", notes=3)))
    M["alfie_hold_cage"] = dict(note="the cage raised beside his face, held by the ring (screen-right hand); pose key 'bird' sets the "
                                     "canary inside (any CANARY5 state + notes/eyes/... keys); prop_tip_r = cage base bottom")
    S["alfie_listen"] = ("alfie", dict(yaw=0.55, pitch=0.10, expr="worried", blink=1, head_roll=14, lean=4, gaze=(1.0, 0.2),
                                       arm_r=dict(hand=(0.78, -0.30), bend=-1.0, stretch=1.3), prop_r="cage",
                                       arm_l=dict(hand=(-0.06, 0.90), bend=0.7), legs="narrow", bird=dict(state="perch_quiet")))
    M["alfie_listen"] = dict(note="ear turned to the cage held up close on the screen-right side, eyes half shut, listening")
    S["alfie_shout_run"] = ("alfie", dict(yaw=0.80, pitch=-0.25, expr="shouting", mouth="talk_b", fx=["sweat"], lean=12, head_roll=-8,
                                          legs=dict(preset="step", stride=1.2, lift_l=0.8, knee_l=1.0, toe_r=1.0),
                                          arm_r=dict(hand=(0.78, 0.12), shape="point", bend=-0.6, stretch=1.3),
                                          arm_l=dict(hand=(-0.50, 0.70), bend=0.6, layer="back", stretch=1.2), prop_l="cage",
                                          bird=dict(state="fallen", swing=-18)))
    M["alfie_shout_run"] = dict(note="shouting 'run!', pointing to the exit (screen-right), the cage swinging back in the other hand")
    S["alfie_run_cage"] = ("alfie", dict(yaw=0.85, pitch=-0.10, expr="worried", mouth="talk_a", fx=["sweat"], lean=15, head_roll=-6,
                                         legs=dict(preset="step", stride=1.3, lift_l=0.9, knee_l=1.0, toe_r=1.0),
                                         arm_r=dict(hand=(0.62, 0.20), bend=-0.8, stretch=1.3), prop_r="cage",
                                         arm_l=dict(hand=(-0.50, 0.85), bend=0.6, layer="back"), bird=dict(state="fallen", swing=12)))
    M["alfie_run_cage"] = dict(note="sprint to screen-right, the cage held out in front; animate bird.swing -20..20 against the stride; "
                                    "alternate the stride sign for the second frame")
    S["alfie_worried"] = ("alfie", dict(yaw=-0.30, pitch=0.35, expr="worried", fx=["sweat"], head_roll=6,
                                        arm_r=dict(hand=(0.08, 0.84), bend=0.8), arm_l=dict(hand=(-0.04, 0.88), bend=0.8), legs="narrow"))
    S["alfie_determined"] = ("alfie", dict(yaw=0.30, expr="determined", head_roll=-4, arm_l="akimbo", arm_r=dict(hand=(0.40, 0.98), bend=0.6),
                                           legs="wide", lean=2))
    legs, g = C2._kneel_legs(NEW_CAST5["alfie"], 1)
    S["alfie_revive"] = ("alfie", dict(yaw=0.55, pitch=0.30, expr="worried", head_roll=-4, lean=10, gaze=(0.8, 0.3),
                                       legs=dict(legs, preset="stand"),
                                       arm_r=dict(hand=(0.36, g - 0.78), bend=0.5, stretch=1.2), prop_r="oxygen_box",
                                       arm_l=dict(hand=(0.48, g - 0.66), bend=0.5, stretch=1.3)))
    M["alfie_revive"] = dict(note="kneeling on one knee, the oxygen box in both hands, the tube nozzle (prop_tip_r) at the cage bars; "
                                  "stand canary_in_cage on a bench (bench_svg) so that its 'beak' anchor is about 0.07 D right of "
                                  "prop_tip_r (poses.png does this); bird state 'revive' then 'sing_one'",
                             cage=dict(state="revive"))
    # --- gaffer
    lamp = dict(flame=1.0)
    S["gaffer_laugh"] = ("gaffer", dict(lamp, yaw=0.15, expr="laughing", blink=2, mouth="talk_b", fx=["tears"], head_roll=14, lean=-6,
                                        head_dy=0.03, squash=(1.03, 0.97), t=0.3,
                                        arm_r=dict(hand=(0.30, 1.14), bend=0.9), arm_l=dict(hand=(-0.72, 0.90), bend=0.4), prop_l=LAMP, legs="wide"))
    M["gaffer_laugh"] = dict(note="eyes shut, mouth wide, one hand on the belly, the lamp hanging from the other; animate t for the tears")
    S["gaffer_lift_lamp"] = ("gaffer", dict(yaw=0.30, pitch=-0.55, expr="smug", head_roll=6, lean=-4, gaze=(0.8, -0.8), flame=1.6,
                                            arm_r=dict(hand=(1.00, -0.45), bend=-0.9, stretch=1.3), prop_r=LAMP,
                                            arm_l=dict(hand=(0.56, 0.66), shape="point", bend=-1.0, stretch=1.3), legs="wide"))
    M["gaffer_lift_lamp"] = dict(note="the lamp raised high on the screen-right side, pointing at it with the other hand, smug; pose key "
                                      "'flame' 0..2 sets the flame (1.6 = burning bright), 'flame_blue' 0..1 the blue firedamp cap")
    S["gaffer_smug"] = ("gaffer", dict(lamp, yaw=0.30, pitch=-0.35, expr="smug", head_roll=5, arm_r="akimbo",
                                       arm_l=dict(hand=(-0.70, 0.95), bend=0.4), prop_l=LAMP))
    S["gaffer_arms_crossed"] = ("gaffer", dict(yaw=-0.20, pitch=-0.30, expr="smug", head_roll=-4,
                                               arm_l=dict(hand=(0.34, 0.90), bend=0.5, sharp=0.3), arm_r=dict(hand=(-0.36, 0.84), bend=-0.5, sharp=0.3)))
    S["gaffer_shout"] = ("gaffer", dict(lamp, yaw=-0.35, pitch=-0.5, expr="angry", mouth="talk_b", head_roll=-7, lean=-3,
                                        arm_l=dict(hand=(-0.96, 0.10), shape="point", bend=-0.6, stretch=1.3),
                                        arm_r=dict(hand=(0.70, 0.95), bend=0.4), prop_r=LAMP, legs="wide"))
    S["gaffer_shocked"] = ("gaffer", dict(yaw=-0.25, pitch=-0.2, expr="shocked", fx=["sweat"], head_roll=-5, lean=-4, squash=(0.97, 1.04),
                                          flame=1.8, flame_blue=0.8, arm_r=dict(hand=(0.80, -0.30), bend=-0.8, shape="open", stretch=1.2),
                                          prop_l=LAMP, arm_l=dict(hand=(-0.82, -0.35), bend=-0.8, stretch=1.2), legs="wide"))
    M["gaffer_shocked"] = dict(note="both hands up, the lamp in the screen-left hand flaring blue (flame 1.8, flame_blue 0.8)")
    S["gaffer_run"] = ("gaffer", dict(lamp, yaw=0.85, pitch=-0.1, expr="shocked", fx=["sweat"], lean=14, head_roll=-6,
                                      legs=dict(preset="step", stride=1.1, lift_l=0.7, knee_l=1.0, toe_r=1.0),
                                      arm_r=dict(hand=(0.66, 0.30), bend=-0.9, stretch=1.2), prop_r=LAMP,
                                      arm_l=dict(hand=(-0.60, 0.70), bend=0.6, layer="back", shape="open")))
    # --- miners
    for c, sfx in MINERS:
        S["miners_laugh" + sfx] = (c, dict(yaw=-0.35, pitch=-0.3, expr="laughing", fx=["tears"], head_roll=-10, lean=-5, t=0.6,
                                           arm_l=dict(hand=(-0.84, -0.12), shape="point", bend=-0.8, stretch=1.3),
                                           arm_r=dict(hand=(0.24, 1.02), bend=0.9)))
        S["miners_mock" + sfx] = (c, dict(yaw=0.6, pitch=-0.4, expr="smug", mouth="talk_b", head_roll=6, lean=-4,
                                          arm_r=dict(hand=(0.58, 0.14), bend=-0.8, shape="open", stretch=1.2),
                                          arm_l=dict(hand=(0.56, 0.36), bend=-0.5, shape="open", stretch=1.3), legs="wide"))
        S["miners_run" + sfx] = (c, dict(yaw=0.85, pitch=-0.1, expr="shocked", fx=["sweat"], lean=14, head_roll=-6,
                                         legs=dict(preset="step", stride=1.2, lift_l=0.8, knee_l=1.0, toe_r=1.0),
                                         arm_r=dict(hand=(0.50, -0.30), bend=-0.9, shape="open", stretch=1.2),
                                         arm_l=dict(hand=(-0.40, -0.25), bend=-0.9, shape="open", layer="back", stretch=1.2)))
        S["miners_push" + sfx] = (c, dict(yaw=0.7, pitch=0.2, expr="determined", mouth="clench", head_roll=-4, lean=22, head_dy=0.02,
                                          legs=dict(preset="step", stride=1.0, crouch=0.15, toe_r=1.0, toe_l=0.8),
                                          arm_r=dict(hand=(0.82, 0.60), bend=-0.3, stretch=1.25, shape="open"),
                                          arm_l=dict(hand=(0.74, 0.74), bend=-0.3, stretch=1.3, shape="open")))
        S["miners_cough" + sfx] = (c, dict(yaw=0.45, pitch=0.5, expr="worried", mouth="talk_o", blink=1, head_roll=10, lean=12, cough=0.3,
                                           arm_r=dict(hand=(0.40, 0.40), bend=-0.6, stretch=1.2),
                                           arm_l=dict(hand=(-0.10, 0.95), bend=0.8), legs="narrow"))
    S["miners_work"] = ("miner1", dict(yaw=0.6, pitch=0.2, expr="determined", head_roll=-6, lean=6, legs=dict(preset="wide", crouch=0.15, stride=0.3),
                                       arm_r=dict(hand=(0.40, -0.40), bend=-0.9, stretch=1.25), prop_r=dict(type="pickaxe", angle=-110),
                                       arm_l=dict(hand=(0.28, -0.12), bend=-0.6, stretch=1.2)))
    S["miners_work_miner2"] = ("miner2", dict(yaw=0.6, pitch=0.5, expr="neutral", head_roll=-4, lean=14, legs=dict(preset="wide", crouch=0.25, stride=0.4),
                                              arm_r=dict(hand=(0.55, 0.72), bend=-0.4, stretch=1.25), prop_r=dict(type="shovel", angle=55),
                                              arm_l=dict(hand=(0.10, 0.62), bend=-0.5, stretch=1.2)))
    S["miners_work_miner3"] = ("miner3", dict(yaw=0.6, pitch=0.3, expr="unimpressed", head_roll=-4, lean=10, legs=dict(preset="wide", crouch=0.12),
                                              arm_r=dict(hand=(0.62, 0.48), bend=-0.5, stretch=1.2), prop_r=dict(type="pickaxe", angle=35),
                                              arm_l=dict(hand=(0.42, 0.62), bend=-0.5, stretch=1.2)))
    M["miners_work"] = dict(note="miner1 swinging the pick-axe (wind-up; 'strike' = the blow), miner2 digging with the shovel, miner3 "
                                 "with the pick lowered", strike=dict(arm_r=dict(hand=(0.62, 0.55), bend=-0.5, stretch=1.25),
                                                                     prop_r=dict(type="pickaxe", angle=20)))
    M["miners_push"] = dict(note="leaning into a coal tub on screen-right: both open hands ~0.75-0.85 D in front at hip height (the tub is "
                                 "set dressing); _miner2 / _miner3 variants")
    M["miners_cough"] = dict(note="hunched, fist at the mouth, pose key 'cough' (phase 0..1) draws dust puffs drifting out of the mouth")
    M["miners_laugh"] = dict(note="miner1; _miner2 / _miner3 variants for the others (same for mock / run / push / cough / work)")
    return S, M


STORY5, STORY5_META = {}, {}


# ============================================================================= registration
def register():
    if getattr(P, "_cast5_registered", False):
        CE.register_stage()
        if not STORY5:
            s, m = _story()
            STORY5.update(s)
            STORY5_META.update(m)
        return
    for name in ("_prop", "_face", "_norm", "figure", "resolve_pose", "lerp_pose"):
        _O5[name] = getattr(P, name)
    P._prop = _prop
    P._face = _face
    P._norm = _norm
    P.figure = figure
    P.resolve_pose = resolve_pose
    P.lerp_pose = lerp_pose
    CE.COSTUMES.update(COSTUMES5)
    CE.HATS.update(HATS5)
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in NEW_PROPS5 if t not in P.PROP_TYPES)
    P.PROP_TIP.update(NEW_TIP5)
    for n, c in NEW_CAST5.items():
        P.CAST[n] = c
    CE.CANVAS.update(CANVAS5)
    P._cast5_registered = True
    s, m = _story()
    STORY5.update(s)
    STORY5_META.update(m)
    P.STORY.update(STORY5)
    CE.register_stage()


register()
