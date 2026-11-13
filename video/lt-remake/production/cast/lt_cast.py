#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lt_cast.py -- cast of the Thai short "ช่างเชื่อมสายฟ้า" for the v2 puppet (puppet.py and cast_ext.py are never edited).

    import sys; sys.path.insert(0, ".../v3/ltcast"); import lt_cast       # registers on import (idempotent)
    import puppet                                                         # the same module object, now with 6 more members
    f = puppet.figure("welder", {"hair_state": "bolt", "expr": "scream", "arm_r": "raised", "arm_l": "raised", "zap": ["body"]}, "w")
    lt_cast.render_png("welder", pose, "out.png", 512)                   # one transparent sprite card

New names in puppet.CAST:  welder, hong, kim, nurse, nb_man, nb_woman
New pose keys (read by the hooks, ignored by puppet's own normaliser):
    hair_state  "normal" | "bolt"      welder / nurse (kim is always spiky)
    mask        None | "down" | "up"   welder's welding mask
    zap         list of "hair", "finger_r", "finger_l", "torch_r", "torch_l", "body"   electric effects (t = flicker phase)
    hug_trunk   True or {"x": torso-local x, "w": width}   a tree trunk in front of the torso (arms go over it)
    stool       True                   red plastic soi stool under the hips (pair it with a crouch)
New expression:            scream
New arm presets (every build): fist_up, crossed, finger_up, cup_mouth, cheeks, fists, torch, hold, up_point
New props:                 torch, calculator, cash, handfan, screwdriver, phone
Command line:  python3 lt_cast.py lineup | poses | bench | test | canvas
"""
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
CASTDIR = os.path.join(PROJ, "v3", "cast")
if CASTDIR not in sys.path:
    sys.path.insert(0, CASTDIR)
import cast_ext as X  # noqa: E402  (registers the v3 cast and puts v2/puppet on sys.path)
import puppet as P    # noqa: E402

V2P = X.V2P
NEW = ("welder", "hong", "kim", "nurse", "nb_man", "nb_woman")
TT = P.TORSO_TOP
SKIN = P.HEAD_FILL
_clamp, _lerp, _smooth, _rot = P._clamp, P._lerp, P._smooth, P._rot
_ln, _circ, _bowl = X._ln, X._circ, X._bowl

_POSE = [{}]          # raw pose dict of the figure being drawn (set by the _norm hook)
_TRUNK = [None]       # trunk spec for the torso hook (set by the figure wrapper)
_O = {}               # wrapped originals (whatever was installed before this module)

YELLOW, YCORE = "#ffe23a", "#fffbe0"


def _pose(key, default=None):
    p = _POSE[0]
    v = p.get(key, default) if isinstance(p, dict) else default
    return default if v is None else v


def _cur():
    return X._CUR[0] or {}


def _hair_state(C):
    s = _pose("hair_state", C.get("hair_state", "normal"))
    return s if s in ("normal", "bolt") else "normal"


def _path(pts, close=True):
    return "M" + " L".join("%.4f,%.4f" % p for p in pts) + (" Z" if close else "")


def _star(c, r, rot=0.0, inner=0.32, n=4):
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = math.radians(rot + i * 180.0 / n)
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * math.sin(a)))
    return _path(pts)


def _hash(a, b=0.0):
    """deterministic pseudo-random 0..1 (no random module: output must be reproducible)."""
    v = math.sin(a * 12.9898 + b * 78.233) * 43758.5453
    return v - math.floor(v)


# ============================================================================= costumes (torso-local, torso clip)
def _cos_apron(k, C, m):
    """welder: dark-blue work tee (collar rib, short sleeves on the arms) under a brown leather welding apron: bib with
    a stitched chest pocket (soapstone holder + pencil), neck straps with brass rivets, waist ties, scorch marks; the apron
    hangs OVER the torso bottom down onto the thighs.  Dark work trousers (bowl)."""
    Xm = X._X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    inside = ['<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.036" stroke-linecap="round"/>'
              % (Xm(-0.165, 0.40) + Xm(0.0, 0.60) + Xm(0.165, 0.40) + (k.c(col["dark"]),)),
              _bowl(k, col["pants"], yb, yB)]
    hem = yB + C.get("apron_len", 0.30)

    def apron_d(ins):
        a = [Xm(-0.145 + ins, 0.640 + ins), Xm(0.145 - ins, 0.640 + ins), Xm(0.160 - ins, 0.820), Xm(0.170 - ins, 0.950),
             Xm(0.245 - ins, 0.990), Xm(0.255 - ins, hem - 0.06), Xm(0.255 - ins, hem - ins), Xm(0.190 - ins, hem - ins),
             Xm(-0.190 + ins, hem - ins), Xm(-0.255 + ins, hem - ins), Xm(-0.255 + ins, hem - 0.06), Xm(-0.245 + ins, 0.990),
             Xm(-0.170 + ins, 0.950), Xm(-0.160 + ins, 0.820)]
        return ("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
                % (a[0] + a[1] + a[2] + a[3] + a[4] + a[5] + a[6] + a[7] + a[8] + a[9] + a[10] + a[11] + a[12] + a[13]))
    k.defs.append('<linearGradient id="%s_ap" gradientUnits="userSpaceOnUse" x1="-0.28" y1="0" x2="0.28" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.38" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(col["apron_l"]), k.c(col["apron"]), k.c(col["apron_d"])))
    over = []
    for s in (-1, 1):               # neck straps
        a, b = Xm(s * 0.130, 0.665), Xm(s * 0.168, 0.365)
        over.append(_ln([a, b], k.ink, 0.058))
        over.append(_ln([a, b], k.c(col["strap"]), 0.034))
    over.append('<path d="%s" fill="url(#%s_ap)" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (apron_d(0.0), u, k.ink))
    over.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" stroke-dasharray="0.026 0.018" opacity="0.85"/>'
                % (apron_d(0.030), k.c(col["stitch"])))
    # chest pocket: soapstone holder and a pencil poking out
    over.append(_ln([Xm(-0.072, 0.655), Xm(-0.072, 0.735)], k.ink, 0.040))
    over.append(_ln([Xm(-0.072, 0.660), Xm(-0.072, 0.735)], k.c("#c9ced6"), 0.020))
    over.append(_ln([Xm(0.002, 0.672), Xm(0.002, 0.735)], k.ink, 0.034))
    over.append(_ln([Xm(0.002, 0.676), Xm(0.002, 0.735)], k.c("#efc13a"), 0.016))
    over.append(P._poly(k, [Xm(-0.120, 0.712), Xm(0.050, 0.712), Xm(0.046, 0.842), Xm(-0.116, 0.842)], k.c(col["pocket"]), 0.013))
    over.append(P._poly(k, [Xm(-0.124, 0.706), Xm(0.054, 0.706), Xm(0.050, 0.748), Xm(-0.120, 0.748)], k.c(col["apron_d"]), 0.012))
    for s in (-1, 1):               # rivets
        over.append(_circ(Xm(s * 0.122, 0.668), 0.018, k.c("#e0bd5a"), k, 0.008))
    for s in (-1, 1):               # waist ties to the torso edges
        over.append(_ln([Xm(s * 0.240, 0.985), Xm(s * 0.300, 0.968)], k.ink, 0.040))
        over.append(_ln([Xm(s * 0.240, 0.985), Xm(s * 0.300, 0.968)], k.c(col["strap"]), 0.020))
    for (x, y, r) in ((0.110, 1.31, 0.045), (-0.130, 1.50, 0.034), (0.040, 1.55, 0.020)):      # scorch marks
        c = Xm(x, y)
        over.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" opacity="0.75" transform="rotate(-18 %.4f %.4f)"/>'
                    % (c[0], c[1], r, r * 0.62, k.c(col["scorch"]), c[0], c[1]))
    for p in (Xm(-0.255, hem), Xm(0.255, hem)):
        k.ext.append((p[0], p[1], 0.03))
    return "".join(inside), "", "".join(over)


def _flower_pattern(k, u, col, m):
    k.defs.append('<pattern id="%s_fl" width="0.150" height="0.150" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '%s<circle cx="0.040" cy="0.040" r="0.011" fill="%s"/>'
                  '<circle cx="0.115" cy="0.112" r="0.008" fill="%s"/></pattern>'
                  % (u, m.c, "".join('<circle cx="%.4f" cy="%.4f" r="0.0125" fill="%s"/>'
                                     % (0.040 + 0.020 * math.cos(math.radians(a)), 0.040 + 0.020 * math.sin(math.radians(a)), k.c(col["flower"]))
                                     for a in range(-90, 270, 72)),
                     k.c(col["flower_c"]), k.c(col["flower"])))
    return "url(#%s_fl)" % u


def _cos_blouse(k, C, m):
    """hong: hot-magenta blouse with a small flower print, round collar, three pearl buttons, thick gold chain with a
    framed amulet, a brown money belt-bag at the waist (over), dark trousers."""
    Xm = X._X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    inside = ['<rect x="-0.8" y="0.3" width="1.6" height="1.3" fill="%s" opacity="0.9"/>' % _flower_pattern(k, u, col, m)]
    inside.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round"/>'
                  % (Xm(-0.215, 0.405) + Xm(0.0, 0.640) + Xm(0.215, 0.405) + (k.c(col["dark"]),)))
    for y in (0.800, 0.915, 1.030):
        inside.append(_circ(Xm(0.0, y), 0.020, k.c("#fbf3f6"), k, 0.009))
    inside.append(_bowl(k, col["pants"], yb, yB))
    # gold chain: a heavy rope with link marks, amulet in a gold frame
    ch = [Xm(-0.215, 0.430), Xm(0.0, 0.725), Xm(0.215, 0.430)]
    d = "M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" % (ch[0] + ch[1] + ch[2])
    over = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.056" stroke-linecap="round"/>' % (d, k.ink),
            '<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>' % (d, k.c(col["gold"])),
            '<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-dasharray="0.012 0.024" stroke-linecap="butt"/>' % (d, k.c(col["gold_d"]))]
    c = Xm(0.0, 0.655)
    over.append('<rect x="%.4f" y="%.4f" width="0.096" height="0.118" rx="0.030" fill="%s" stroke="%s" stroke-width="0.012"/>'
                % (c[0] - 0.048, c[1], k.c(col["gold"]), k.ink))
    over.append('<rect x="%.4f" y="%.4f" width="0.056" height="0.076" rx="0.020" fill="%s"/>' % (c[0] - 0.028, c[1] + 0.021, k.c("#5a3a2a")))
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s"/>' % (c[0] - 0.018, c[1] + 0.088, c[0], c[1] + 0.020, c[0] + 0.018, c[1] + 0.088, k.c(col["gold"])))
    # money belt-bag
    bx = 0.05
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040"/>'
                % (Xm(-0.50, yb - 0.06) + Xm(0.0, yb - 0.03) + Xm(0.50, yb - 0.06) + (k.ink,)))
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020"/>'
                % (Xm(-0.50, yb - 0.06) + Xm(0.0, yb - 0.03) + Xm(0.50, yb - 0.06) + (k.c(col["bag_d"]),)))
    p0, p1 = Xm(bx - 0.135, yb - 0.115), Xm(bx + 0.135, yb + 0.060)
    over.append('<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.050" fill="%s" stroke="%s" stroke-width="0.016"/>'
                % (p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], k.c(col["bag"]), k.ink))
    over.append(_ln([(p0[0] + 0.03, p0[1] + 0.055), (p1[0] - 0.03, p0[1] + 0.055)], k.c(col["gold"]), 0.012))
    over.append(_circ((p1[0] - 0.040, p0[1] + 0.055), 0.013, k.c(col["gold"]), k, 0.006))
    return "".join(inside), "", "".join(over)


def _cos_singlet(k, C, m):
    """kim: cream rib-knit singlet (เสื้อกล้าม) with a scoop neck and deep arm holes, khaki shorts with a brown belt and a
    leather tool pouch (pliers handles) on the screen-left hip."""
    Xm = X._X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_rb" width="0.042" height="0.4" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0.017" y="0" width="0.008" height="0.4" fill="%s"/></pattern>' % (u, m.c, k.c(col["rib"])))
    o = ['<rect x="-0.75" y="0.3" width="1.5" height="1.3" fill="url(#%s_rb)" opacity="0.55"/>' % u]
    skin = k.c(SKIN)
    for s in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
                 % (Xm(s * 0.150, 0.30) + Xm(s * 0.160, 0.42) + Xm(s * 0.175, 0.66) + Xm(s * 0.300, 0.700) + Xm(s * 0.40, 0.700)
                    + Xm(s * 0.40, 0.62) + Xm(s * 0.40, 0.30) + (skin, k.ink)))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>'
             % (Xm(-0.115, 0.30) + Xm(-0.110, 0.45) + Xm(-0.095, 0.625) + Xm(0.0, 0.630) + Xm(0.095, 0.625) + Xm(0.110, 0.45) + Xm(0.115, 0.30) + (skin, k.ink)))
    o.append(_bowl(k, col["pants"], yb, yB))
    o.append('<path d="M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f Q0,%.4f -0.75,%.4f Z" fill="%s" stroke="%s" stroke-width="0.012"/>'
             % (yb - 0.040, yb - 0.010, yb - 0.040, yb + 0.012, yb + 0.042, yb + 0.012, k.c(col["belt"]), k.ink))
    over = []
    px = -0.20
    for dx, c in ((-0.035, "#d0302a"), (0.0, "#e8c040"), (0.030, "#3a68b8")):
        over.append(_ln([Xm(px + dx, yb - 0.075), Xm(px + dx * 1.6, yb - 0.150)], k.ink, 0.034))
        over.append(_ln([Xm(px + dx, yb - 0.078), Xm(px + dx * 1.6, yb - 0.147)], k.c(c), 0.016))
    over.append(P._poly(k, [Xm(px - 0.085, yb - 0.085), Xm(px + 0.080, yb - 0.085), Xm(px + 0.070, yb + 0.105), Xm(px - 0.075, yb + 0.105)],
                        k.c(col["pouch"]), 0.015))
    over.append(_ln([Xm(px - 0.080, yb - 0.035), Xm(px + 0.076, yb - 0.035)], k.c(col["pouch_d"]), 0.012))
    k.ext.append((Xm(px, yb + 0.11)[0], yb + 0.11, 0.03))
    return "".join(o), "", "".join(over)


def _cos_nurse(k, C, m):
    """nurse: white uniform dress: pointed collar with light-blue piping, placket and three buttons, breast pocket with a
    pen, name tag and a pinned fob watch, light-blue belt, A-line skirt drawn over the hips with folds and a hem line."""
    Xm = X._X(m)
    col = C["colors"]
    u = k.uid
    yw = C.get("waist_y", 0.95)
    hem = TT + C["torso_h"] + C.get("skirt_len", 0.50)
    inside = [_ln([Xm(0.0, 0.62), Xm(0.0, yw - 0.06)], k.c(col["dark"]), 0.010)]
    for y in (0.700, 0.790, 0.880):
        inside.append(_circ(Xm(0.0, y), 0.017, k.c("#ffffff"), k, 0.008))
    px = -0.135               # breast pocket + pen
    inside.append(_ln([Xm(px + 0.020, 0.650), Xm(px + 0.020, 0.740)], k.ink, 0.032))
    inside.append(_ln([Xm(px + 0.020, 0.654), Xm(px + 0.020, 0.740)], k.c("#2f5fb8"), 0.015))
    inside.append(P._poly(k, [Xm(px - 0.060, 0.715), Xm(px + 0.060, 0.715), Xm(px + 0.056, 0.830), Xm(px - 0.056, 0.830)], k.c(col["pocket"]), 0.011))
    tg = Xm(0.140, 0.700)     # name tag + fob watch
    inside.append('<rect x="%.4f" y="%.4f" width="0.110" height="0.044" rx="0.008" fill="%s" stroke="%s" stroke-width="0.009"/>'
                  % (tg[0] - 0.055, tg[1], k.c(col["piping"]), k.ink))
    inside.append(_ln([(tg[0] - 0.035, tg[1] + 0.022), (tg[0] + 0.030, tg[1] + 0.022)], k.c("#ffffff"), 0.010))
    inside.append(_ln([(tg[0], tg[1] + 0.050), (tg[0] - 0.010, tg[1] + 0.090)], k.c("#c9ced6"), 0.008))
    inside.append(_circ((tg[0] - 0.012, tg[1] + 0.110), 0.026, k.c("#e9edf3"), k, 0.010))
    for s in (-1, 1):         # collar with piping
        pts = [Xm(s * 0.150, 0.420), Xm(s * 0.010, 0.565), Xm(s * 0.125, 0.640)]
        inside.append(P._poly(k, pts, k.c("#ffffff"), 0.014))
        inside.append(_ln([pts[0], pts[2]], k.c(col["piping"]), 0.012))
    a = 0.215
    b = C.get("skirt_w", 0.44)
    sk = [Xm(-a, yw - 0.02), Xm(a, yw - 0.02), Xm(b * 0.70, yw + 0.25), Xm(b, hem - 0.02), Xm(0.0, hem + 0.012), Xm(-b, hem - 0.02), Xm(-b * 0.70, yw + 0.25)]
    d = ("M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (sk[0] + sk[1] + sk[2] + sk[3] + (sk[3][0] * 0.5, hem + 0.030) + sk[4] + (sk[5][0] * 0.5, hem + 0.030) + sk[5] + sk[6] + sk[0]))
    k.defs.append('<clipPath id="%s_sk"><path d="%s"/></clipPath>' % (u, d))
    over = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.048" stroke-linejoin="round"/>' % (d, k.ink, k.ink),
            '<g clip-path="url(#%s_sk)"><rect x="-0.9" y="0.5" width="1.8" height="2.0" fill="url(#%s_tg)"/>' % (u, u)]
    for s in (-1, 1):
        over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
                    % (Xm(s * 0.09, yw + 0.10) + Xm(s * 0.13, yw + 0.35) + Xm(s * 0.21, hem - 0.04) + (k.c(col["dark"]),)))
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012"/>'
                % (Xm(-b - 0.05, hem - 0.07) + Xm(0.0, hem - 0.035) + Xm(b + 0.05, hem - 0.07) + (k.c(col["dark"]),)))
    over.append('</g>')
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                % (Xm(-a - 0.012, yw - 0.068) + Xm(0.0, yw - 0.050) + Xm(a + 0.012, yw - 0.068) + Xm(a + 0.012, yw - 0.012)
                   + Xm(0.0, yw + 0.006) + Xm(-a - 0.012, yw - 0.012) + (k.c(col["piping"]), k.ink)))
    c = Xm(0.0, yw - 0.030)
    over.append('<rect x="%.4f" y="%.4f" width="0.060" height="0.050" rx="0.008" fill="%s" stroke="%s" stroke-width="0.010"/>'
                % (c[0] - 0.030, c[1] - 0.025, k.c("#d9dde4"), k.ink))
    for p in (sk[3], sk[5], (sk[4][0], hem + 0.03)):
        k.ext.append((p[0], p[1], 0.04))
    return "".join(inside), "", "".join(over)


def _cos_jersey(k, C, m):
    """nb_man: green football jersey with a white V collar and a crest, navy shorts, a red-and-white checked
    pha khao ma (ผ้าขาวม้า) tied round the belly with the knot and two tails at the front."""
    Xm = X._X(m)
    col = C["colors"]
    yB = TT + C["torso_h"]
    yb = yB - 0.14
    u = k.uid
    k.defs.append('<pattern id="%s_js" width="0.090" height="0.4" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0.0" y="0" width="0.045" height="0.4" fill="%s"/></pattern>' % (u, m.c, k.c(col["stripe"])))
    o = ['<rect x="-0.75" y="0.3" width="1.5" height="1.3" fill="url(#%s_js)" opacity="0.35"/>' % u]
    vt, vb, vw = 0.42, 0.66, 0.12
    o.append(P._poly(k, [Xm(-vw - 0.04, vt), Xm(vw + 0.04, vt), Xm(0, vb + 0.05)], k.c("#ffffff"), 0.014))
    o.append(P._poly(k, [Xm(-vw, vt), Xm(vw, vt), Xm(0, vb)], k.c(SKIN), 0.012))
    c = Xm(-0.150, 0.770)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.010"/>'
             % (c[0] - 0.040, c[1] - 0.045, c[0] + 0.040, c[1] - 0.045, c[0] + 0.040, c[1] + 0.005, c[0] + 0.030, c[1] + 0.040, c[0], c[1] + 0.055,
                c[0] - 0.030, c[1] + 0.040, c[0] - 0.040, c[1] + 0.005, k.c("#f3d04a"), k.ink))
    o.append(_bowl(k, col["pants"], yb, yB))
    # pha khao ma
    k.defs.append('<pattern id="%s_pk" width="0.080" height="0.080" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect width="0.080" height="0.080" fill="%s"/><rect width="0.040" height="0.080" fill="%s" opacity="0.6"/>'
                  '<rect width="0.080" height="0.040" fill="%s" opacity="0.6"/><rect x="0.018" y="0" width="0.006" height="0.080" fill="%s"/></pattern>'
                  % (u, m.c, k.c(col["cloth"]), k.c(col["cloth_2"]), k.c(col["cloth_2"]), k.c("#ffffff")))
    yw = yb - 0.07
    band = ("M-0.75,%.4f Q0,%.4f 0.75,%.4f L0.75,%.4f Q0,%.4f -0.75,%.4f Z" % (yw - 0.06, yw - 0.02, yw - 0.06, yw + 0.05, yw + 0.09, yw + 0.05))
    over = []
    kx = Xm(0.06, yw + 0.02)
    tails = [(kx[0] - 0.01, kx[1]), (kx[0] - 0.07, kx[1] + 0.20), (kx[0] - 0.01, kx[1] + 0.23), (kx[0] + 0.03, kx[1] + 0.02)]
    tails2 = [(kx[0] + 0.01, kx[1]), (kx[0] + 0.09, kx[1] + 0.17), (kx[0] + 0.04, kx[1] + 0.20), (kx[0] - 0.005, kx[1] + 0.03)]
    for t in (tails, tails2):
        over.append('<path d="%s" fill="url(#%s_pk)" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>' % (_path(t), u, k.ink))
    o.append('<path d="%s" fill="url(#%s_pk)" stroke="%s" stroke-width="0.014"/>' % (band, u, k.ink))
    over.append('<ellipse cx="%.4f" cy="%.4f" rx="0.045" ry="0.036" fill="url(#%s_pk)" stroke="%s" stroke-width="0.013"/>' % (kx[0], kx[1], u, k.ink))
    k.ext.append((kx[0], kx[1] + 0.24, 0.03))
    return "".join(o), "", "".join(over)


def _cos_sarong(k, C, m):
    """nb_woman: sunflower-yellow tee with a round collar and a breast pocket; long indigo batik sarong (ผ้าถุง) from the
    waist to just above the ankles, drawn over the hips and legs, with a front overlap fold and a rolled waist."""
    Xm = X._X(m)
    col = C["colors"]
    u = k.uid
    yw = C.get("waist_y", 0.97)
    lg = _pose("legs", "stand")
    cr = _num(lg.get("crouch"), 0.0) if isinstance(lg, dict) else (P.LEG_PRESETS.get(lg, {}).get("crouch", 0.0) if isinstance(lg, str) else 0.0)
    hem = TT + C["torso_h"] + C["leg"] * (C.get("sarong_len", 0.80) - 0.95 * cr)     # a crouch shortens the drop to the floor
    inside = ['<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
              % (Xm(-0.16, 0.40) + Xm(0.0, 0.59) + Xm(0.16, 0.40) + (k.c(col["dark"]),))]
    inside.append(P._poly(k, [Xm(0.060, 0.700), Xm(0.170, 0.700), Xm(0.166, 0.800), Xm(0.064, 0.800)], k.c(col["pocket"]), 0.011))
    k.defs.append('<pattern id="%s_bt" width="0.130" height="0.130" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<path d="M0.065,0.020 L0.100,0.065 L0.065,0.110 L0.030,0.065 Z" fill="none" stroke="%s" stroke-width="0.011"/>'
                  '<circle cx="0.065" cy="0.065" r="0.012" fill="%s"/><circle cx="0" cy="0" r="0.010" fill="%s"/><circle cx="0.130" cy="0.130" r="0.010" fill="%s"/>'
                  '<circle cx="0.130" cy="0" r="0.010" fill="%s"/><circle cx="0" cy="0.130" r="0.010" fill="%s"/></pattern>'
                  % (u, m.c, k.c(col["motif"]), k.c(col["motif"]), k.c(col["motif2"]), k.c(col["motif2"]), k.c(col["motif2"]), k.c(col["motif2"])))
    a, b = 0.245, C.get("skirt_w", 0.30)
    sk = [Xm(-a, yw - 0.03), Xm(a, yw - 0.03), Xm(b + 0.02, yw + 0.40), Xm(b - 0.01, hem), Xm(0.0, hem + 0.015), Xm(-b + 0.01, hem), Xm(-b - 0.02, yw + 0.40)]
    d = ("M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (sk[0] + sk[1] + sk[2] + sk[3] + (sk[3][0] * 0.5, hem + 0.02) + sk[4] + (sk[5][0] * 0.5, hem + 0.02) + sk[5] + sk[6] + sk[0]))
    k.defs.append('<clipPath id="%s_sr"><path d="%s"/></clipPath>' % (u, d))
    k.defs.append('<linearGradient id="%s_sg" gradientUnits="userSpaceOnUse" x1="-0.32" y1="0" x2="0.32" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.38" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(P._shade(col["sarong"], 1.18)), k.c(col["sarong"]), k.c(P._shade(col["sarong"], 0.72))))
    over = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.046" stroke-linejoin="round"/>' % (d, k.ink, k.ink),
            '<g clip-path="url(#%s_sr)"><rect x="-0.9" y="0.5" width="1.8" height="3.0" fill="url(#%s_sg)"/>'
            '<rect x="-0.9" y="0.5" width="1.8" height="3.0" fill="url(#%s_bt)" opacity="0.9"/>' % (u, u, u)]
    fx = 0.10                 # front overlap fold
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
                % (Xm(fx, yw) + Xm(fx + 0.04, yw + 0.5) + Xm(fx + 0.02, hem) + (k.ink,)))
    over.append('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040"/>' % (Xm(-0.4, hem - 0.03) + Xm(0.4, hem - 0.03) + (k.c(col["border"]),)))
    over.append('</g>')
    over.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.013" stroke-linejoin="round"/>'
                % (Xm(-a - 0.01, yw - 0.07) + Xm(0.0, yw - 0.05) + Xm(a + 0.01, yw - 0.07) + Xm(a + 0.01, yw - 0.005)
                   + Xm(0.0, yw + 0.012) + Xm(-a - 0.01, yw - 0.005) + (k.c(col["border"]), k.ink)))
    for p in (sk[3], sk[5], (sk[4][0], hem + 0.03)):
        k.ext.append((p[0], p[1], 0.04))
    return "".join(inside), "", "".join(over)


LT_COSTUMES = {"apron": _cos_apron, "blouse": _cos_blouse, "singlet": _cos_singlet, "nurse": _cos_nurse, "jersey": _cos_jersey,
               "sarong": _cos_sarong}


def _trunk_svg(k, T):
    """tree trunk in front of the torso (torso-local frame), with bark lines, a knot and a three-colour sash (ผ้าสามสี)."""
    x, w, top, bot = T["x"], T["w"], T["top"], T["bottom"]
    h = w / 2
    u = k.uid
    k.defs.append('<linearGradient id="%s_tk" gradientUnits="userSpaceOnUse" x1="%.4f" y1="0" x2="%.4f" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, x - h, x + h, k.c("#a17550"), k.c("#7b5537"), k.c("#4e3322")))
    d = ("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Z"
         % (x - h, top, x + h, top, x + h + 0.01, bot - 0.22, x + h + 0.02, bot - 0.02, x + h + 0.16, bot, x - h - 0.16, bot,
            x - h - 0.02, bot - 0.02, x - h - 0.01, bot - 0.22, x - h, top))
    o = ['<path d="%s" fill="url(#%s_tk)" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, u, k.ink)]
    bark = ""
    for i, bx in enumerate((-0.30, -0.05, 0.22)):
        xx = x + bx * w
        y = top + 0.1
        pts = []
        while y < bot - 0.05:
            pts.append((xx + 0.018 * math.sin(y * 7.0 + i), y))
            y += 0.12
        bark += "M" + " L".join("%.4f,%.4f" % p for p in pts)
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.7"/>' % (bark, k.c("#3f2818")))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.050" ry="0.070" fill="%s" stroke="%s" stroke-width="0.012"/>' % (x + 0.08 * w, bot - 0.75, k.c("#4a2f1e"), k.ink))
    ys = T.get("sash_y", bot - 1.10)
    for j, cc in enumerate(("#e85a9a", "#f2c63a", "#3bb26a")):
        y0 = ys + j * 0.045
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s"/>'
                 % (x - h - 0.01, y0, x, y0 + 0.03, x + h + 0.01, y0, x + h + 0.01, y0 + 0.045, x, y0 + 0.075, x - h - 0.01, y0 + 0.045, k.c(cc)))
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012"/>'
             % (x - h - 0.01, ys, x, ys + 0.03, x + h + 0.01, ys, x - h - 0.01, ys + 0.135, x, ys + 0.165, x + h + 0.01, ys + 0.135, k.ink))
    return "".join(o)


def _torso(k, C, m):
    out = _O["_torso"](k, C, m)
    T = _TRUNK[0]
    if T is not None:
        out += _trunk_svg(k, T)
    return out


# ============================================================================= hair, hats, mask (head frame, over the head)
def _hair_cap(k, C, yaw, col, top=-0.64, fringe=None, side_y=-0.10):
    """short hair mass over the crown, outside the head contour, with a jagged fringe that slides with the face."""
    dx = -0.03 * yaw
    fx = 0.10 * yaw
    outer = [(-0.490 + dx, side_y), (-0.535 + dx, -0.30), (-0.470 + dx, -0.49), (-0.290 + dx, top + 0.035), (-0.110 + dx, top - 0.025),
             (-0.040 + dx, top + 0.010), (0.060 + dx, top - 0.035), (0.150 + dx, top + 0.015), (0.300 + dx, top + 0.045),
             (0.470 + dx, -0.49), (0.535 + dx, -0.30), (0.490 + dx, side_y)]
    fr = fringe or [(0.445, side_y), (0.410, -0.23), (0.300, -0.275), (0.235, -0.200), (0.160, -0.290), (0.060, -0.205),
                    (-0.030, -0.300), (-0.125, -0.215), (-0.205, -0.300), (-0.305, -0.245), (-0.410, -0.235), (-0.445, side_y)]
    inner = [(x + fx * (1.0 - abs(x) / 0.5), y) for x, y in fr]
    d = _path(outer + inner)
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (d, k.c(col), k.ink)]
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.022" stroke-linecap="round" opacity="0.85"/>'
             % (-0.40 + dx, -0.40, -0.30 + dx, -0.55, -0.12 + dx, -0.58, k.c(C["hair"].get("shine", "#5a5f80"))))
    for p in outer:
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o)


def _spike_poly(base_c, ang, L, w, zig, kinks=2):
    """one jagged lightning spike: axis from base_c in direction ang (deg) with `kinks` sideways steps, width w at the base
    tapering to the tip."""
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    nx, ny = -uy, ux
    axis = [(0.0, 0.0)]
    for i in range(1, kinks + 1):
        t = i / (kinks + 1.0)
        axis.append((t, zig * (1 if i % 2 else -1)))
    axis.append((1.0, 0.0))
    left, right = [], []
    for t, o in axis:
        hw = w / 2 * (1.0 - t) ** 0.9
        cx, cy = base_c[0] + ux * L * t + nx * o, base_c[1] + uy * L * t + ny * o
        left.append((cx + nx * hw, cy + ny * hw))
        right.append((cx - nx * hw, cy - ny * hw))
    return left[:-1] + [left[-1]] + right[-2::-1]


def _bolt_hair(k, C, yaw, col, n=7, L0=0.42, kinks=2, zig=0.045, spread=(-158, -22), w=0.20, shine=False, up=0.25):
    """hair blown straight up after the strike: the crown mass plus n jagged lightning spikes standing on it."""
    dx = -0.03 * yaw
    o = []
    polys = []
    a0, a1 = spread
    for i in range(n):
        f = i / (n - 1.0)
        a = _lerp(a0, a1, f)
        L = L0 * (0.80 + 0.30 * math.sin(math.pi * f)) * (0.92 + 0.16 * _hash(i, C["seed"]))
        r0 = 0.40
        bc = (dx + r0 * math.cos(math.radians(a)), -0.10 + r0 * math.sin(math.radians(a)))
        polys.append(_spike_poly(bc, _lerp(a, -90.0, up) + 6.0 * (f - 0.5), L, w, zig * (1 if i % 2 else -1), kinks))
    for pl in polys:
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>' % (_path(pl), k.ink, k.ink))
        for p in pl:
            k.ext.append((p[0], p[1], 0.03))
    for pl in polys:
        o.append('<path d="%s" fill="%s"/>' % (_path(pl), k.c(col)))
    if shine:
        for pl in polys[1:-1:2]:
            m = len(pl) // 2
            o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
                     % (pl[1][0] * 0.6 + pl[m][0] * 0.4, pl[1][1] * 0.6 + pl[m][1] * 0.4, pl[1][0] * 0.25 + pl[m][0] * 0.75,
                        pl[1][1] * 0.25 + pl[m][1] * 0.75, k.c(C["hair"].get("shine", "#5a5f80"))))
    return "".join(o)


def _spark_marks(k, pts, r=0.055):
    o = []
    for i, (x, y) in enumerate(pts):
        d = _star((x, y), r, 45.0 * (i % 2) + 10.0 * i)
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (d, k.c(YELLOW), k.ink))
        k.ext.append((x, y, r))
    return "".join(o)


def _mask(k, C, yaw, state, lift=0.0):
    """welding mask: dark-grey shell with a green glass window; "down" covers the face, "up" is flipped onto the crown."""
    col = C["mask_colors"]
    u = k.uid
    k.defs.append('<linearGradient id="%s_mk" gradientUnits="userSpaceOnUse" x1="-0.5" y1="0" x2="0.5" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  '<linearGradient id="%s_gl" gradientUnits="userSpaceOnUse" x1="0" y1="-0.1" x2="0" y2="0.1">'
                  '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(col["light"]), k.c(col["base"]), k.c(col["dark"]), u, k.c(col["glass_l"]), k.c(col["glass"])))
    fx = 0.10 * yaw
    o = []
    for s in (-1, 1):             # pivot knobs of the head gear
        c = (s * 0.495 - 0.02 * yaw, -0.14 - lift)
        o.append(_circ(c, 0.060, k.c(col["dark"]), k, 0.016))
        o.append('<circle cx="%.4f" cy="%.4f" r="0.022" fill="%s"/>' % (c[0], c[1], k.c(col["light"])))
        k.ext.append((c[0], c[1], 0.07))
    if state == "down":
        sh = [(-0.470 + fx * 0.5, -0.30), (-0.30 + fx, -0.43), (fx, -0.47), (0.30 + fx, -0.43), (0.470 + fx * 0.5, -0.30),
              (0.485 + fx * 0.6, 0.05), (0.40 + fx, 0.34), (0.16 + fx, 0.54), (fx, 0.57), (-0.16 + fx, 0.54), (-0.40 + fx, 0.34),
              (-0.485 + fx * 0.6, 0.05)]
        d = P._smooth_closed(sh)
        o.append('<path d="%s" fill="url(#%s_mk)" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, u, k.ink))
        o.append('<path d="M%.4f,0.30 Q%.4f,0.46 %.4f,0.30" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
                 % (-0.26 + fx, fx, 0.26 + fx, k.c(col["dark"])))
        gy = C["eye_y"] - 0.005
        o.append('<rect x="%.4f" y="%.4f" width="0.500" height="0.190" rx="0.030" fill="%s" stroke="%s" stroke-width="0.018"/>'
                 % (fx - 0.25, gy - 0.095, k.c(col["frame"]), k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.420" height="0.118" rx="0.014" fill="url(#%s_gl)" stroke="%s" stroke-width="0.012"/>'
                 % (fx - 0.21, gy - 0.059, u, k.ink))
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#ffffff" stroke-width="0.020" stroke-linecap="round" opacity="0.75"/>'
                 % (fx - 0.15, gy + 0.035, fx - 0.08, gy - 0.040))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>'
                 % (-0.38 + fx * 0.5, -0.20, -0.36 + fx * 0.5, -0.05, -0.33 + fx * 0.5, 0.12, k.c(col["shine"])))
        for p in sh:
            k.ext.append((p[0], p[1], 0.03))
    else:
        ly = -lift
        sh = [(-0.455, -0.24 + ly), (-0.47, -0.42 + ly), (-0.40, -0.66 + ly), (-0.20, -0.80 + ly), (0.0 + fx * 0.3, -0.83 + ly),
              (0.20, -0.80 + ly), (0.40, -0.66 + ly), (0.47, -0.42 + ly), (0.455, -0.24 + ly), (0.0, -0.31 + ly)]
        d = P._smooth_closed(sh)
        o.append('<g transform="rotate(%.3f 0 %.4f)">' % (-4.0 + 3.0 * yaw, -0.3 + ly))
        o.append('<path d="%s" fill="url(#%s_mk)" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (d, u, k.ink))
        o.append('<path d="M-0.40,%.4f Q0,%.4f 0.40,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.8"/>'
                 % (-0.36 + ly, -0.43 + ly, -0.36 + ly, k.c(col["dark"])))
        gy = -0.62 + ly
        o.append('<rect x="%.4f" y="%.4f" width="0.460" height="0.110" rx="0.025" fill="%s" stroke="%s" stroke-width="0.016"/>'
                 % (fx * 0.3 - 0.23, gy - 0.055, k.c(col["frame"]), k.ink))
        o.append('<rect x="%.4f" y="%.4f" width="0.380" height="0.056" rx="0.012" fill="url(#%s_gl)" stroke="%s" stroke-width="0.010"/>'
                 % (fx * 0.3 - 0.19, gy - 0.028, u, k.ink))
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round" opacity="0.7"/>'
                 % (-0.38, -0.36 + ly, -0.36, -0.55 + ly, -0.25, -0.70 + ly, k.c(col["shine"])))
        o.append('</g>')
        for p in sh:
            k.ext.append((p[0], p[1], 0.03))
    return "".join(o)


def _hat_welder(k, C, yaw):
    st = _hair_state(C)
    mask = _pose("mask", C.get("mask_default"))
    col = C["hair"]["color"]
    o = []
    top = (0.0, -0.66)
    if st == "bolt":
        o.append(_hair_cap(k, C, yaw, col))
        o.append(_bolt_hair(k, C, yaw, col))
        top = (0.0, -1.0)
    else:
        o.append(_hair_cap(k, C, yaw, col))
    if mask in ("down", "up"):
        o.append(_mask(k, C, yaw, mask, lift=0.30 if (mask == "up" and st == "bolt") else 0.0))
        if mask == "up":
            top = (0.0, min(top[1], -0.84 - (0.30 if st == "bolt" else 0.0)))
    if st == "bolt" and _pose("bolt_sparks", True):
        o.append(_spark_marks(k, [(-0.62, -0.78), (0.66, -0.70), (0.10, -1.08)], 0.050))
    return "".join(o), top


def _perm(k, C, yaw):
    """hong: dark curly perm: a cloud of curls around the top and the sides of the head, outside the contour, and a row of
    fringe curls over the forehead."""
    col = C["hair"]
    dx = -0.03 * yaw
    fx = 0.10 * yaw
    cur = []
    n = 13
    for i in range(n):
        f = i / (n - 1.0)
        a = math.radians(_lerp(158.0, 382.0, f))
        r = 0.115 - 0.030 * abs(f - 0.5) * 2 + 0.010 * _hash(i, 3.3)
        cur.append((dx + 0.555 * math.cos(a), -0.12 + 0.600 * math.sin(a), r))
    fr = [(fx + x, -0.300 + 0.025 * (i % 2), 0.078) for i, x in enumerate((-0.33, -0.20, -0.07, 0.07, 0.20, 0.33))]
    body = [(c[0], c[1]) for c in cur]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.050" stroke-linejoin="round"/>'
         % (_path(body + [(0.40 + fx, -0.24), (-0.40 + fx, -0.24)]), k.ink, k.ink)]
    for (x, y, r) in cur + fr:
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, y, r + 0.022, k.ink))
        k.ext.append((x, y, r + 0.025))
    o.append('<path d="%s" fill="%s"/>' % (_path(body + [(0.40 + fx, -0.24), (-0.40 + fx, -0.24)]), k.c(col["color"])))
    for (x, y, r) in cur + fr:
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x, y, r, k.c(col["color"])))
    for i, (x, y, r) in enumerate(cur + fr):
        o.append('<path d="M%.4f,%.4f A%.4f,%.4f 0 1 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.013" stroke-linecap="round" opacity="0.9"/>'
                 % (x - r * 0.45, y + r * 0.05, r * 0.45, r * 0.45, x + r * 0.05, y + r * 0.40, k.c(col["shine"])))
    # gold hair pin on the side away from the face
    side = -1.0 if yaw >= 0 else 1.0
    pc = (dx + side * 0.36, -0.40)
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_star(pc, 0.060, 0, 0.45, 5), k.c("#f0c040"), k.ink))
    return "".join(o), (dx, -0.82)


def _hat_perm(k, C, yaw):
    return _perm(k, C, yaw)


def _hat_kim(k, C, yaw):
    """kim: white-grey wiry hair standing straight up (struck forty years ago): a crown mass and eleven thin spikes."""
    col = C["hair"]["color"]
    o = [_hair_cap(k, C, yaw, col, top=-0.60, side_y=-0.08,
                   fringe=[(0.445, -0.08), (0.420, -0.28), (0.250, -0.360), (0.0, -0.385), (-0.250, -0.360), (-0.420, -0.28), (-0.445, -0.08)])]
    o.append(_bolt_hair(k, C, yaw, col, n=11, L0=0.40, kinks=1, zig=0.018, spread=(-172, -8), w=0.11, up=0.62))
    dx = -0.03 * yaw
    o.append('<path d="M%.4f,-0.48 Q%.4f,-0.54 %.4f,-0.50 M%.4f,-0.50 Q%.4f,-0.56 %.4f,-0.49" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/>'
             % (-0.26 + dx, -0.18 + dx, -0.10 + dx, 0.08 + dx, 0.16 + dx, 0.27 + dx, k.c("#b9b4bc")))
    return "".join(o), (dx, -0.92)


def _nurse_cap(k, C, yaw, lift=0.0, tilt=0.0):
    col = C["hat_colors"]
    dx = -0.03 * yaw
    ly = -lift
    o = ['<g transform="rotate(%.3f %.4f %.4f)">' % (C["hat_tilt"] + tilt, dx, -0.50 + ly)]
    crown = [(-0.25 + dx, -0.50 + ly), (-0.20 + dx, -0.74 + ly), (0.20 + dx, -0.74 + ly), (0.25 + dx, -0.50 + ly)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (_path(crown), k.c(col["base"]), k.ink))
    o.append(_ln([(-0.18 + dx, -0.68 + ly), (0.18 + dx, -0.68 + ly)], k.c(col["dark"]), 0.012))
    band = [(-0.42 + dx, -0.36 + ly), (-0.40 + dx, -0.54 + ly), (0.40 + dx, -0.54 + ly), (0.42 + dx, -0.36 + ly), (0.0 + dx, -0.40 + ly)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>' % (P._smooth_closed(band), k.c(col["light"]), k.ink))
    cx, cy = dx + 0.08 * yaw, -0.465 + ly
    o.append('<path d="M%.4f,%.4f h0.030 v0.030 h0.030 v0.040 h-0.030 v0.030 h-0.040 v-0.030 h-0.030 v-0.040 h0.030 v-0.030 Z" fill="%s" stroke="%s" stroke-width="0.008"/>'
             % (cx - 0.015, cy - 0.050, k.c(col["cross"]), k.ink))
    o.append('</g>')
    for p in crown + band:
        k.ext.append((p[0], p[1], 0.04))
    return "".join(o)


def _hat_nurse(k, C, yaw):
    col = C["hair"]["color"]
    st = _hair_state(C)
    o = []
    for bs, wgt in X._ribbon_sides(yaw):              # bun at the back, on the side away from the face
        o.append('<g opacity="%.3f">' % wgt if wgt < 0.999 else "<g>")
        c = (bs * 0.44, -0.36)
        o.append(_circ(c, 0.150, k.c(col), k, 0.024))
        o.append('<path d="M%.4f,%.4f A0.08,0.08 0 1 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" opacity="0.8"/>'
                 % (c[0] - 0.07, c[1], c[0] + 0.02, c[1] + 0.07, k.c(C["hair"]["shine"])))
        o.append('</g>')
        k.ext.append((c[0], c[1], 0.17))
    o.append(_hair_cap(k, C, yaw, col, top=-0.60, side_y=-0.02,
                       fringe=[(0.445, -0.02), (0.420, -0.20), (0.300, -0.31), (0.120, -0.355), (0.02, -0.30), (-0.06, -0.37),
                               (-0.260, -0.335), (-0.410, -0.21), (-0.445, -0.02)]))
    if st == "bolt":
        o.append(_bolt_hair(k, C, yaw, col, n=7, L0=0.40, spread=(-160, -20)))
        o.append(_nurse_cap(k, C, yaw, lift=0.38, tilt=14.0))
        if _pose("bolt_sparks", True):
            o.append(_spark_marks(k, [(-0.66, -0.72), (0.64, -0.80)], 0.045))
        return "".join(o), (0.0, -1.10)
    o.append(_nurse_cap(k, C, yaw))
    return "".join(o), (0.0, -0.74)


def _hat_flattop(k, C, yaw):
    """nb_man: black flat-top crew cut: squared crown with clipped sides, bristle texture along the flat top."""
    col = C["hair"]["color"]
    dx = -0.03 * yaw
    fx = 0.08 * yaw
    pts = [(-0.478 + dx, -0.12), (-0.515 + dx, -0.33), (-0.470 + dx, -0.53), (-0.400 + dx, -0.595), (-0.300 + dx, -0.612), (0.300 + dx, -0.612),
           (0.400 + dx, -0.595), (0.470 + dx, -0.53), (0.515 + dx, -0.33), (0.478 + dx, -0.12), (0.432 + fx, -0.13), (0.405 + fx, -0.28),
           (0.200 + fx, -0.305), (0.0 + fx, -0.315), (-0.200 + fx, -0.305), (-0.405 + fx, -0.28), (-0.432 + fx, -0.13)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink)]
    br = "".join("M%.4f,-0.600 L%.4f,-0.560" % (x + dx, x + dx + 0.004) for x in [-0.34 + 0.0425 * i for i in range(17)])
    o.append('<path d="%s" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.8"/>' % (br, k.c(C["hair"]["shine"])))
    o.append('<path d="M%.4f,-0.48 Q%.4f,-0.55 %.4f,-0.53" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.8"/>'
             % (-0.42 + dx, -0.36 + dx, -0.22 + dx, k.c(C["hair"]["shine"])))
    for p in pts:
        k.ext.append((p[0], p[1], 0.03))
    return "".join(o), (dx, -0.63)


def _hat_longhair(k, C, yaw):
    """nb_woman: long straight black hair falling to the shoulders as one silhouette, a blunt fringe, a yellow claw clip."""
    col = C["hair"]["color"]
    dx = -0.03 * yaw
    fx = 0.08 * yaw
    gl = _clamp(1.0 + 0.35 * max(0.0, yaw) - 0.45 * max(0.0, -yaw), 0.5, 1.4)    # screen-left lock grows when the face turns right
    gr = _clamp(1.0 + 0.35 * max(0.0, -yaw) - 0.45 * max(0.0, yaw), 0.5, 1.4)

    def L(x, y):
        return (-(0.44 + (x - 0.44) * gl) + dx, y)

    def R(x, y):
        return ((0.44 + (x - 0.44) * gr) + dx, y)
    outer = [L(0.64, 0.56), L(0.60, 0.28), L(0.575, 0.00), L(0.560, -0.25), (-0.47 + dx, -0.48), (-0.27 + dx, -0.615), (dx, -0.650),
             (0.27 + dx, -0.615), (0.47 + dx, -0.48), R(0.560, -0.25), R(0.575, 0.00), R(0.60, 0.28), R(0.64, 0.56)]
    inner = [R(0.53, 0.58), R(0.48, 0.42), R(0.452, 0.15), R(0.448, -0.12), (0.42 + fx, -0.235), (0.20 + fx, -0.245), (fx, -0.250),
             (-0.20 + fx, -0.245), (-0.42 + fx, -0.235), L(0.448, -0.12), L(0.452, 0.15), L(0.48, 0.42), L(0.53, 0.58)]
    pts = outer + inner
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (_path(pts), k.c(col), k.ink)]
    sh = k.c(C["hair"]["shine"])
    o.append(_ln([L(0.53, -0.20), L(0.545, 0.10), L(0.57, 0.40)], sh, 0.014))
    o.append(_ln([R(0.53, -0.20), R(0.545, 0.10), R(0.57, 0.40)], sh, 0.014))
    o.append('<path d="M%.4f,-0.46 Q%.4f,-0.58 %.4f,-0.58" fill="none" stroke="%s" stroke-width="0.018" stroke-linecap="round" opacity="0.85"/>'
             % (-0.40 + dx, -0.30 + dx, -0.12 + dx, sh))
    for p in pts:
        k.ext.append((p[0], p[1], 0.03))
    side = -1.0 if yaw >= 0 else 1.0
    c = (dx + side * 0.30, -0.52)
    o.append('<rect x="%.4f" y="%.4f" width="0.130" height="0.060" rx="0.022" fill="%s" stroke="%s" stroke-width="0.012" transform="rotate(%.1f %.4f %.4f)"/>'
             % (c[0] - 0.065, c[1] - 0.030, k.c("#f2c63a"), k.ink, side * 35.0, c[0], c[1]))
    return "".join(o), (dx, -0.66)


LT_HATS = {"welder": _hat_welder, "perm": _hat_perm, "kim": _hat_kim, "nurse": _hat_nurse, "flattop": _hat_flattop, "longhair": _hat_longhair}


# ============================================================================= face, moustache, sleeves and shoes
def _face(k, C, P_, white):
    if P_["expr"] == "scream" and P_["mouth"] is None:
        P_ = dict(P_)
        P_["mouth"] = ("open", 0.30, 0.20)
    return _O["_face"](k, C, P_, white)


def _moustache(k, mx, my, s=1.0):
    C = _cur()
    if C.get("moustache_style") != "brush":
        return _O["_moustache"](k, mx, my, s)
    col = C["colors"].get("moustache", "#a9a3ac")
    pts = [(mx - 0.165, my + 0.050), (mx - 0.135, my - 0.030), (mx - 0.060, my - 0.050), (mx, my - 0.032), (mx + 0.060, my - 0.050),
           (mx + 0.135, my - 0.030), (mx + 0.165, my + 0.050), (mx + 0.090, my + 0.028), (mx, my + 0.034), (mx - 0.090, my + 0.028)]
    o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink)]
    st = "".join("M%.4f,%.4f L%.4f,%.4f" % (mx + x, my - 0.025, mx + x * 1.15, my + 0.028) for x in (-0.11, -0.06, 0.06, 0.11))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round"/>' % (st, k.c("#7e7883")))
    return "".join(o)


def _bez_pts(c, tmax_len, n=24):
    """points along the limb's first cubic (shoulder side) up to an arc length."""
    p0, p1, p2, p3 = c[0], c[1], c[2], c[3]
    out = [p0]
    acc = 0.0
    for i in range(1, n + 1):
        t = i / float(n)
        u = 1.0 - t
        q = (u * u * u * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t * t * t * p3[0],
             u * u * u * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t * t * t * p3[1])
        seg = math.hypot(q[0] - out[-1][0], q[1] - out[-1][1])
        if acc + seg >= tmax_len:
            f = (tmax_len - acc) / seg if seg > 1e-9 else 0.0
            out.append((out[-1][0] + (q[0] - out[-1][0]) * f, out[-1][1] + (q[1] - out[-1][1]) * f))
            return out
        acc += seg
        out.append(q)
    return out


def _tube(k, pts, hw0, hw1, fill, cuff=None, back=0.03):
    """short sleeve / shorts leg along a polyline: fill without ink at the body end, ink on both sides and the cuff."""
    if len(pts) < 2:
        return ""
    a, b = pts[0], pts[1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    pts = [(a[0] - (b[0] - a[0]) / L * back, a[1] - (b[1] - a[1]) / L * back)] + pts
    n = len(pts)
    left, right = [], []
    for i in range(n):
        p, q = pts[max(i - 1, 0)], pts[min(i + 1, n - 1)]
        tx, ty = q[0] - p[0], q[1] - p[1]
        tl = math.hypot(tx, ty) or 1.0
        nx, ny = ty / tl, -tx / tl
        hw = _lerp(hw0, hw1, i / (n - 1.0))
        left.append((pts[i][0] + nx * hw, pts[i][1] + ny * hw))
        right.append((pts[i][0] - nx * hw, pts[i][1] - ny * hw))
    poly = left + right[::-1]
    o = ['<path d="%s" fill="%s"/>' % (_path(poly), fill)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.018" stroke-linejoin="round" stroke-linecap="round"/>'
             % (_path(left[1:] + right[::-1][:-1], close=False), k.ink))
    if cuff:
        e, f = left[-1], right[-1]
        cx, cy = pts[-1]
        bx, by = pts[-2] if n > 2 else pts[0]
        dl = math.hypot(cx - bx, cy - by) or 1.0
        ux, uy = (cx - bx) / dl * 0.035, (cy - by) / dl * 0.035
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                 % (_path([(e[0] - ux, e[1] - uy), e, f, (f[0] - ux, f[1] - uy)]), cuff, k.ink))
    return "".join(o)


def _shoe(k, H, tail, style, col):
    dx = tail[0] - H[0]
    s = 1.0 if dx >= 0 else -1.0
    ln = abs(dx)
    x0, x1 = H[0] - s * 0.05, H[0] + s * (ln + 0.045)
    y = H[1]
    if style == "boot":
        pts = [(x0, y - 0.115), (H[0] + s * 0.050, y - 0.115), (H[0] + s * 0.060, y - 0.040), (x1, y - 0.030), (x1 + s * 0.012, y + 0.030),
               (x0, y + 0.034)]
        o = ['<path d="%s" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink)]
        o.append(_ln([(x0 + s * 0.01, y + 0.022), (x1, y + 0.020)], k.c("#211a1e"), 0.020))
        o.append(_ln([(x0 + s * 0.015, y - 0.080), (H[0] + s * 0.040, y - 0.080)], k.c("#8a6a4e"), 0.010))
        return "".join(o)
    if style == "shoe":
        pts = [(x0, y - 0.045), (H[0] + s * 0.03, y - 0.065), (x1, y - 0.025), (x1 + s * 0.010, y + 0.028), (x0, y + 0.030)]
        return '<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (P._smooth_closed(pts), k.c(col), k.ink)
    # sandal: a coloured sole under the foot stub and one strap
    o = [_ln([(x0, y + 0.032), (x1, y + 0.032)], k.ink, 0.040), _ln([(x0 + s * 0.005, y + 0.032), (x1 - s * 0.005, y + 0.032)], k.c(col), 0.020)]
    o.append(_ln([(H[0] + s * 0.035, y - 0.030), (H[0] + s * 0.065, y + 0.025)], k.c(col), 0.016))
    return "".join(o)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    out = _O["_ink_limb"](k, S, E, H, kk, w, seed, tail)
    C = _cur()
    if not C or "lt_member" not in C:
        return out
    c = P._limb_ctrl(S, E, H, kk)
    if tail is None:
        sl = C.get("sleeve")
        if sl:
            pts = _bez_pts(c, sl["len"])
            out += _tube(k, pts, w / 2 + sl["w"], w / 2 + sl["w"] * sl.get("flare", 1.1), k.c(sl["color"]),
                         k.c(sl["cuff"]) if sl.get("cuff") else None)
    else:
        lg = C.get("shorts")
        if lg:
            pts = _bez_pts(c, lg["len"])
            out += _tube(k, pts, w / 2 + lg["w"], w / 2 + lg["w"] * 1.1, k.c(lg["color"]), k.c(lg["cuff"]) if lg.get("cuff") else None, back=0.05)
        sh = C.get("shoes")
        if sh:
            out += _shoe(k, H, tail, sh[0], sh[1])
    return out


# ============================================================================= props
LT_PROPS = ("torch", "calculator", "cash", "handfan", "screwdriver", "phone")
LT_TIP = {"torch": 0.44, "calculator": 0.0, "cash": 0.32, "handfan": 0.32, "screwdriver": 0.31, "phone": 0.0}


def _prop(k, kind, H, ang, sc=1.0):
    if kind not in LT_PROPS:
        return _O["_prop"](k, kind, H, ang, sc)
    ink = k.ink
    u = k.uid
    if kind == "torch":
        # gas welding torch: ribbed grip, two valve knobs, brass tube, nozzle bent 30 degrees; a red hose hangs from the butt
        bx, by = _rot(-0.10 * sc, 0.0, ang)
        B = (H[0] + bx, H[1] + by)
        hose = "M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (B[0], B[1], B[0] - 0.10, B[1] + 0.30, B[0] + 0.22, B[1] + 0.45, B[0] + 0.06, B[1] + 0.75)
        o = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.058" stroke-linecap="round"/>' % (hose, ink),
             '<path d="%s" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>' % (hose, k.c("#c4372e")),
             '<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.6" transform="translate(-0.006 -0.006)"/>' % (hose, k.c("#f08a7c"))]
        k.ext.append((B[0] + 0.06, B[1] + 0.75, 0.04))
        o.append('<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc))
        o.append('<path d="M0.130,-0.016 L0.300,-0.014 L0.300,0.014 L0.130,0.016 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#d8a84a"), ink))
        o.append('<path d="M0.295,-0.012 L0.400,0.045 L0.388,0.068 L0.290,0.014 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#c27a3e"), ink))
        o.append('<path d="M0.392,0.040 L0.440,0.066 L0.428,0.090 L0.380,0.064 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#8a4a2a"), ink))
        o.append('<rect x="-0.110" y="-0.036" width="0.250" height="0.072" rx="0.026" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#43464f"), ink))
        o.append('<path d="M-0.06,-0.030 L-0.06,0.030 M-0.02,-0.032 L-0.02,0.032 M0.02,-0.032 L0.02,0.032 M0.06,-0.030 L0.06,0.030" stroke="%s" stroke-width="0.009"/>' % k.c("#6f7380"))
        for x, cc in ((0.085, "#d0302a"), (0.120, "#2f8a4a")):
            o.append('<circle cx="%.4f" cy="-0.050" r="0.022" fill="%s" stroke="%s" stroke-width="0.009"/>' % (x, k.c(cc), ink))
        o.append('</g>')
        tx, ty = _rot(0.434 * sc, 0.078 * sc, ang)
        for e in ((-0.11, 0.0), (0.44, 0.08), (0.10, -0.075)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        return "".join(o), (H[0] + tx, H[1] + ty)
    if kind == "calculator":
        o = ['<g transform="translate(%.4f %.4f) rotate(-8) scale(%.4f)">' % (H[0], H[1], sc)]
        o.append('<rect x="-0.120" y="-0.330" width="0.240" height="0.360" rx="0.030" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#4d5260"), ink))
        o.append('<rect x="-0.092" y="-0.300" width="0.184" height="0.075" rx="0.010" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#b9cf9c"), ink))
        o.append('<path d="M-0.070,-0.262 L-0.040,-0.262 M-0.025,-0.262 L0.005,-0.262 M0.020,-0.262 L0.050,-0.262 M0.060,-0.262 L0.070,-0.262" stroke="%s" stroke-width="0.022"/>' % k.c("#3a4630"))
        for r in range(4):
            for cix in range(4):
                fill = "#f08a3a" if (r == 3 and cix == 3) else "#ece8e0"
                o.append('<rect x="%.4f" y="%.4f" width="0.040" height="0.030" rx="0.006" fill="%s"/>' % (-0.090 + cix * 0.048, -0.205 + r * 0.050, k.c(fill)))
        o.append('</g>')
        for e in ((-0.13, -0.34), (0.13, -0.34), (-0.13, 0.03), (0.13, 0.03)):
            k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.03))
        return "".join(o), (H[0], H[1])
    if kind == "cash":
        # fan of Thai banknotes (green 20, blue 50, red 100, purple 500, grey-brown 1000), always fanned upward
        cols = (("#5aa36a", "#c9e6cf"), ("#4a7ccc", "#cfe0f7"), ("#d8463c", "#f7d0c8"), ("#8e5bb5", "#e3d2f0"), ("#9a7e62", "#eadfcf"))
        o = []
        base = -90.0 + 0.15 * (ang + 90.0 if -270 < ang < 90 else 0.0)
        for i, (c0, c1) in enumerate(cols):
            a = base - 44.0 + i * 22.0
            o.append('<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], a, sc))
            o.append('<rect x="0.000" y="-0.075" width="0.360" height="0.150" rx="0.010" fill="%s" stroke="%s" stroke-width="0.013"/>' % (k.c(c0), ink))
            o.append('<rect x="0.030" y="-0.052" width="0.300" height="0.104" rx="0.006" fill="none" stroke="%s" stroke-width="0.010"/>' % k.c(c1))
            o.append('<circle cx="0.255" cy="0" r="0.034" fill="%s" stroke="%s" stroke-width="0.008"/>' % (k.c(c1), k.c(c0)))
            o.append('</g>')
            ex, ey = _rot(0.37 * sc, 0.0, a)
            k.ext.append((H[0] + ex, H[1] + ey, 0.09))
        tx, ty = _rot(0.32 * sc, 0.0, base)
        return "".join(o), (H[0] + tx, H[1] + ty)
    if kind == "handfan":
        o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
        r0, r1, sp = 0.12, 0.34, 58.0
        a0, a1 = math.radians(-sp), math.radians(sp)
        d = ("M%.4f,%.4f A%.3f,%.3f 0 0 1 %.4f,%.4f L%.4f,%.4f A%.3f,%.3f 0 0 0 %.4f,%.4f Z"
             % (r1 * math.cos(a0), r1 * math.sin(a0), r1, r1, r1 * math.cos(a1), r1 * math.sin(a1), r0 * math.cos(a1), r0 * math.sin(a1), r0, r0,
                r0 * math.cos(a0), r0 * math.sin(a0)))
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (d, k.c("#d6343c"), ink))
        rib = "".join("M0,0 L%.4f,%.4f" % (r0 * math.cos(math.radians(a)), r0 * math.sin(math.radians(a))) for a in range(-58, 59, 16))
        o.append('<path d="%s" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % (rib, k.c("#6a4428")))
        fold = "".join("M%.4f,%.4f L%.4f,%.4f" % (r0 * math.cos(math.radians(a)), r0 * math.sin(math.radians(a)), r1 * math.cos(math.radians(a)), r1 * math.sin(math.radians(a)))
                       for a in range(-50, 51, 10))
        o.append('<path d="%s" stroke="%s" stroke-width="0.007" opacity="0.7"/>' % (fold, k.c("#8e1f28")))
        o.append('<path d="M%.4f,%.4f A0.27,0.27 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016"/>'
                 % (0.27 * math.cos(a0), 0.27 * math.sin(a0), 0.27 * math.cos(a1), 0.27 * math.sin(a1), k.c("#f0c040")))
        o.append('</g>')
        for a in (-sp, 0.0, sp):
            x, y = _rot(r1 * sc * math.cos(math.radians(a)), r1 * sc * math.sin(math.radians(a)), ang)
            k.ext.append((H[0] + x, H[1] + y, 0.03))
        tx, ty = _rot(0.32 * sc, 0.0, ang)
        return "".join(o), (H[0] + tx, H[1] + ty)
    if kind == "screwdriver":
        o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
        o.append('<path d="M0.120,-0.012 L0.290,-0.010 L0.290,0.010 L0.120,0.012 Z" fill="%s" stroke="%s" stroke-width="0.009" stroke-linejoin="round"/>' % (k.c("#c9ced6"), ink))
        o.append('<path d="M0.288,-0.014 L0.312,-0.006 L0.312,0.006 L0.288,0.014 Z" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (k.c("#9aa0aa"), ink))
        o.append('<rect x="-0.070" y="-0.038" width="0.195" height="0.076" rx="0.030" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#d3302a"), ink))
        o.append('<path d="M-0.030,-0.022 L0.090,-0.022 M-0.030,0.000 L0.090,0.000 M-0.030,0.022 L0.090,0.022" stroke="%s" stroke-width="0.008"/>' % k.c("#8f1d18"))
        o.append('<path d="M-0.045,-0.026 L0.100,-0.026" stroke="%s" stroke-width="0.008" opacity="0.7"/>' % k.c("#f58a7f"))
        o.append('</g>')
        for e in ((-0.075, 0.0), (0.31, 0.0)):
            x, y = _rot(e[0] * sc, e[1] * sc, ang)
            k.ext.append((H[0] + x, H[1] + y, 0.04))
        tx, ty = _rot(0.31 * sc, 0.0, ang)
        return "".join(o), (H[0] + tx, H[1] + ty)
    # phone: held upright, screen to the viewer
    o = ['<g transform="translate(%.4f %.4f) rotate(-6) scale(%.4f)">' % (H[0], H[1], sc)]
    o.append('<rect x="-0.072" y="-0.270" width="0.144" height="0.285" rx="0.024" fill="%s" stroke="%s" stroke-width="0.014"/>' % (k.c("#2b2d36"), ink))
    k.defs.append('<linearGradient id="%s_ph" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c("#e9f6ff"), k.c("#8fc6f5")))
    o.append('<rect x="-0.056" y="-0.245" width="0.112" height="0.225" rx="0.010" fill="url(#%s_ph)"/>' % u)
    o.append('<circle cx="0.032" cy="-0.050" r="0.014" fill="%s"/>' % k.c("#e0413a"))
    o.append('<path d="M-0.040,-0.200 L0.040,-0.200 M-0.040,-0.175 L0.020,-0.175" stroke="%s" stroke-width="0.010"/>' % k.c("#5a7aa0"))
    o.append('</g>')
    for e in ((-0.08, -0.28), (0.08, -0.28), (-0.08, 0.02), (0.08, 0.02)):
        k.ext.append((H[0] + e[0] * sc, H[1] + e[1] * sc, 0.03))
    return "".join(o), (H[0], H[1])


# ============================================================================= arm presets, expression
# (dx, dy) of the hand from the shoulder (+dx away from the body), bend, layer, hand shape, sharpness, stretch
LT_ARMS = {
    "slim": {"fist_up": (0.48, -0.54, -1.0, "top", "ball", 0.35, 1.0), "crossed": (-0.40, 0.30, 1.0, "front", "ball", 0.45, 1.0),
             "finger_up": (0.40, -0.48, -1.0, "top", "point", 0.30, 1.0), "cup_mouth": (0.00, -0.30, -1.0, "top", "open", 0.35, 1.0),
             "cheeks": (0.075, -0.41, -1.0, "top", "open", 0.35, 1.0), "fists": (0.20, 0.50, 1.0, "front", "ball", 0.55, 1.0),
             "torch": (0.64, 0.18, -0.6, "front", "ball", 0.25, 1.0), "hold": (0.08, 0.24, 1.0, "front", "ball", 0.50, 1.0),
             "up_point": (0.40, -0.72, -1.0, "top", "point", 0.20, 1.14)},
    "stout": {"fist_up": (0.44, -0.46, -1.0, "top", "ball", 0.35, 1.0), "crossed": (-0.52, 0.34, 1.0, "front", "ball", 0.45, 1.0),
              "finger_up": (0.38, -0.44, -1.0, "top", "point", 0.30, 1.0), "cup_mouth": (-0.11, -0.22, -1.0, "top", "open", 0.35, 1.0),
              "cheeks": (-0.020, -0.31, -1.0, "top", "open", 0.35, 1.0), "fists": (0.18, 0.45, 1.0, "front", "ball", 0.55, 1.0),
              "torch": (0.62, 0.16, -0.6, "front", "ball", 0.25, 1.0), "hold": (-0.02, 0.26, 1.0, "front", "ball", 0.50, 1.0),
              "up_point": (0.42, -0.70, -1.0, "top", "point", 0.20, 1.14)},
    "regular": {"fist_up": (0.46, -0.50, -1.0, "top", "ball", 0.35, 1.0), "crossed": (-0.45, 0.32, 1.0, "front", "ball", 0.45, 1.0),
                "finger_up": (0.39, -0.46, -1.0, "top", "point", 0.30, 1.0), "cup_mouth": (-0.045, -0.27, -1.0, "top", "open", 0.35, 1.0),
                "cheeks": (0.050, -0.36, -1.0, "top", "open", 0.35, 1.0), "fists": (0.19, 0.48, 1.0, "front", "ball", 0.55, 1.0),
                "torch": (0.63, 0.17, -0.6, "front", "ball", 0.25, 1.0), "hold": (0.04, 0.24, 1.0, "front", "ball", 0.50, 1.0),
                "up_point": (0.41, -0.71, -1.0, "top", "point", 0.20, 1.14)},
}
SCREAM = dict(eyes="ring", pupil=0.014, brows=("both", 0.190, -14.0, 0.040, 0.15, 0.0), mouth="talk_b", mouth_dy=0.02)


# ============================================================================= cast
def _lt(d):
    d["lt_member"] = True
    d.setdefault("hat", "newsboy")
    d.setdefault("ear_pencil", False)
    d.setdefault("hat_tilt", 0.0)
    d.setdefault("hat_colors", {})
    d.setdefault("smirk_side", 1)
    d.setdefault("moustache", False)
    return d


LT_CAST = {
    # คุณ, the young welder: slim pill like the hero; dark-blue tee, brown leather apron, boots; short black hair
    "welder": _lt(dict(
        build="slim", seed=4.65,
        torso_w=0.57, torso_h=1.01, profile=P.PROFILE_SLIM, shift_pow=1.0,
        shoulder=(0.235, 0.54), arm=0.74, hip_x=0.21, leg=1.14, stance=0.10, wide=0.36, limb_w=0.056,
        eye_y=0.045, brow="dome", brow_th=0.038, mouth="dash", cheeks="#f4a9b4",
        hat_style="welder", hair_state="normal", mask_default=None,
        hair=dict(color="#221c27", front=0.06, grow=0.20, shine="#5d6488"),
        mask_colors=dict(light="#7a7f8a", base="#4c5059", dark="#2e3138", frame="#2a2c31", glass="#1f7a46", glass_l="#5fd08a", shine="#a9aebb"),
        costume="apron", apron_len=0.30,
        sleeve=dict(color="#2c4a8c", cuff="#1d3366", len=0.15, w=0.040),
        shoes=("boot", "#5a3a26"),
        colors=dict(base="#2c4a8c", dark="#1d3366", pants="#34303d", apron="#8b5a35", apron_l="#b07a4c", apron_d="#5e3b22", strap="#4e301c",
                    stitch="#e2bf8f", pocket="#7a4c2c", scorch="#3f2617"),
    )),
    # เจ๊หงส์, the shop owner: stout pear, curly perm, magenta flower blouse, gold chain, money belt-bag, sandals
    "hong": _lt(dict(
        build="stout", seed=11.55,
        torso_w=1.04, torso_h=1.00, profile=X.PROFILE_PEAR, shift_pow=1.25,
        shoulder=(0.35, 0.46), arm=0.74, hip_x=0.16, leg=1.06, stance=0.06, wide=0.26, limb_w=0.066,
        eye_y=0.030, brow="stroke", brow_th=0.044, mouth="flat", cheeks="#f08aa8",
        hat_style="perm",
        hair=dict(color="#3a2328", front=0.08, grow=0.20, shine="#7a4a52"),
        costume="blouse",
        sleeve=dict(color="#d42f86", cuff="#9c1d5f", len=0.17, w=0.055, flare=1.25),
        shoes=("sandal", "#e0a030"),
        colors=dict(base="#d42f86", dark="#9c1d5f", flower="#f9b9da", flower_c="#f6d34a", pants="#2c2a38", gold="#ecbc3c", gold_d="#a87a18",
                    bag="#6b3a2a", bag_d="#4a2618"),
    )),
    # เฮียกิม, the old electrician (70): slim and thin, tall wiry white hair standing up, round glasses, grey moustache,
    # cream singlet, khaki shorts with a tool pouch, sandals
    "kim": _lt(dict(
        build="slim", seed=27.05,
        torso_w=0.50, torso_h=0.98, profile=P.PROFILE_SLIM, shift_pow=1.0,
        shoulder=(0.205, 0.53), arm=0.74, hip_x=0.17, leg=1.16, stance=0.08, wide=0.30, limb_w=0.054,
        eye_y=0.020, brow="stroke", brow_th=0.046, mouth="dash", moustache=True, moustache_style="brush", glasses=True, age_lines=True,
        cheeks="#f3b0b8",
        hat_style="kim",
        hair=dict(color="#e9e6ec", front=0.08, grow=0.20, shine="#ffffff"),
        costume="singlet",
        shorts=dict(color="#b39a5e", cuff="#8f7a44", len=0.22, w=0.050),
        shoes=("sandal", "#3a5aa8"),
        colors=dict(base="#efe4c8", rib="#d4c49c", pants="#b39a5e", belt="#5b3a26", pouch="#7a4b2c", pouch_d="#4f2f1a", moustache="#aaa4ad"),
    )),
    # the nurse: slim hourglass, white dress with light-blue piping and belt, white cap with a red cross, dark bun
    "nurse": _lt(dict(
        build="slim", seed=20.15,
        torso_w=0.52, torso_h=0.90, profile=X.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.215, 0.52), arm=0.72, hip_x=0.135, leg=1.14, stance=0.05, wide=0.26, limb_w=0.055,
        eye_y=0.050, brow="stroke", brow_th=0.034, mouth="smile", cheeks="#f6a6b6",
        hat_style="nurse", hat_tilt=-4.0, hair_state="normal",
        hat_colors=dict(base="#ffffff", light="#ffffff", dark="#c9ccd4", cross="#d8312c"),
        hair=dict(color="#2b2026", front=0.08, grow=0.22, shine="#6a5560"),
        costume="nurse", waist_y=0.95, skirt_len=0.48, skirt_w=0.42,
        sleeve=dict(color="#f7f7f4", cuff="#9cc0e6", len=0.14, w=0.042),
        shoes=("shoe", "#f7f7f4"),
        colors=dict(base="#f4f4f1", dark="#a9aeb8", pocket="#ecedf0", piping="#8fb6e2", pants="#f4f4f1"),
    )),
    # soi neighbour, man: regular build with a belly, black flat-top, green football jersey, pha khao ma, navy shorts, flip-flops
    "nb_man": _lt(dict(
        build="regular", seed=26.85,
        torso_w=0.84, torso_h=1.00, profile=X.PROFILE_PEAR, shift_pow=1.1,
        shoulder=(0.28, 0.49), arm=0.74, hip_x=0.17, leg=1.12, stance=0.07, wide=0.30, limb_w=0.062,
        eye_y=0.035, brow="stroke", brow_th=0.050, mouth="dash", cheeks="#f2a6b0",
        hat_style="flattop",
        hair=dict(color="#231d26", front=0.06, grow=0.20, shine="#585e80"),
        costume="jersey",
        sleeve=dict(color="#2f9a52", cuff="#ffffff", len=0.16, w=0.045),
        shorts=dict(color="#28325e", len=0.20, w=0.055),
        shoes=("sandal", "#3a7ad0"),
        colors=dict(base="#2f9a52", stripe="#1f7a3e", pants="#28325e", cloth="#d8463c", cloth_2="#f4f0e8"),
    )),
    # soi neighbour, woman: slim, long black hair with a fringe, sunflower-yellow tee, long indigo batik sarong, red sandals
    "nb_woman": _lt(dict(
        build="slim", seed=35.95,
        torso_w=0.54, torso_h=0.92, profile=X.PROFILE_HOURGLASS, shift_pow=1.0,
        shoulder=(0.220, 0.52), arm=0.72, hip_x=0.135, leg=1.12, stance=0.05, wide=0.20, limb_w=0.055,
        eye_y=0.050, brow="stroke", brow_th=0.034, mouth="smile", cheeks="#f4a3b2",
        hat_style="longhair",
        hair=dict(color="#231c25", front=0.10, grow=0.22, shine="#5d5f84"),
        costume="sarong", waist_y=0.97, sarong_len=0.80, skirt_w=0.30,
        sleeve=dict(color="#f2c230", cuff="#d49a18", len=0.15, w=0.042),
        shoes=("sandal", "#d8463c"),
        colors=dict(base="#f2c230", dark="#c8920f", pocket="#e8b322", pants="#2d3a78", sarong="#2d3a78", motif="#e2b04a", motif2="#9fb4e6",
                    border="#8a3a2a"),
    )),
}

# poses that the brief asks for, by name (pose dicts; render with puppet.figure / render_png)
POSES = {
    "welder_idle":        ("welder", dict(yaw=0.2, mask="up", arm_r="down", prop_r=dict(type="torch", angle=70), arm_l="hip")),
    "welder_idle_bolt":   ("welder", dict(yaw=-0.2, hair_state="bolt", expr="stunned", arm_r="down", arm_l="down")),
    "welder_welding":     ("welder", dict(yaw=0.55, mask="down", lean=6, legs=dict(preset="wide", crouch=0.12),
                                          arm_r="torch", prop_r=dict(type="torch", angle=25), arm_l=dict(preset="forward", hand=(0.30, 0.95)),
                                          zap=["torch_r"])),
    "welder_shocked":     ("welder", dict(yaw=0.0, hair_state="bolt", expr="scream", arm_r="raised", arm_l="raised", legs="wide",
                                          squash=(0.96, 1.05), zap=["body", "hair"])),
    "welder_proud":       ("welder", dict(yaw=0.3, pitch=-0.4, hair_state="bolt", expr="laughing", arm_r="fist_up", arm_l="hip", legs="wide",
                                          head_roll=6)),
    "welder_point_spark": ("welder", dict(yaw=0.6, hair_state="bolt", expr="determined", arm_r="point", arm_l="fists", lean=4,
                                          legs=dict(preset="step", stride=0.6), zap=["finger_r"])),
    "welder_sad":         ("welder", dict(yaw=-0.25, pitch=1.0, expr="sad", arm_r="down", arm_l="behind", head_roll=-8, lean=-3, legs="narrow")),
    "welder_angry":       ("welder", dict(yaw=-0.2, pitch=-0.6, hair_state="bolt", expr="furious", arm_r="fists", arm_l="fists", legs="wide",
                                          fx=["steam"], zap=["hair"])),
    "welder_hug_tree":    ("welder", dict(yaw=0.4, expr="happy", fx=["blush"], head_dx=-0.04, head_roll=10, hug_trunk=dict(x=0.42, w=0.50),
                                          arm_l=dict(hand=(0.52, 0.88), bend=0.4), arm_r=dict(hand=(0.84, 0.98), layer="back"), legs="wide")),
    "welder_sit_stool":   ("welder", dict(yaw=0.7, expr="neutral", stool=True, legs=dict(foot_r=(0.70, 1.92), foot_l=(0.50, 1.92), knee_r=1, knee_l=1),
                                          arm_r=dict(hand=(0.62, 1.20)), arm_l=dict(hand=(0.45, 1.25)))),
    "hong_idle_fan":      ("hong", dict(yaw=-0.2, expr="smug", arm_l="hold", prop_l=dict(type="handfan", angle=-70), arm_r="hip")),
    "hong_shout_up":      ("hong", dict(yaw=0.35, pitch=-0.5, expr="talking", mouth="talk_b", arm_r="up_point", arm_l="hip", head_roll=8, lean=-4)),
    "hong_count_money":   ("hong", dict(yaw=0.25, pitch=0.6, expr="happy", arm_l=dict(preset="hold", hand=(-0.05, 0.78)), prop_l="cash",
                                        arm_r=dict(preset="hold", hand=(0.22, 0.70)), head_roll=4)),
    "hong_crossed_smug":  ("hong", dict(yaw=-0.3, pitch=-0.4, expr="smug", arm_r="crossed", arm_l="crossed", head_roll=-6)),
    "hong_angry_shout":   ("hong", dict(yaw=0.4, pitch=-0.6, expr="angry", mouth="talk_b", arm_r="point", arm_l="fists", lean=6,
                                        fx=["anger_fill", "steam"])),
    "hong_calculator":    ("hong", dict(yaw=0.3, pitch=0.5, expr="unimpressed", arm_l=dict(preset="hold", hand=(0.0, 0.80)), prop_l="calculator",
                                        arm_r=dict(preset="hold", hand=(0.16, 0.78)))),
    "kim_explain":        ("kim", dict(yaw=0.3, expr="talking", mouth="talk_a", arm_r="finger_up", arm_l="behind", head_roll=4)),
    "kim_shout_cupped":   ("kim", dict(yaw=0.2, pitch=-0.3, expr="shouting", mouth="talk_b", arm_r="cup_mouth", arm_l="cup_mouth", lean=-4)),
    "kim_point":          ("kim", dict(yaw=0.6, expr="determined", arm_r="point", arm_l="hold", prop_l=dict(type="screwdriver", angle=-60))),
    "nurse_idle":         ("nurse", dict(yaw=0.2, expr="neutral", arm_r="down", arm_l="hip")),
    "nurse_surprise":     ("nurse", dict(yaw=-0.15, expr="shocked", fx=["sweat"], arm_r="cheeks", arm_l="cheeks", legs="narrow", head_roll=-5)),
    "nurse_bolt":         ("nurse", dict(yaw=0.1, hair_state="bolt", expr="stunned", arm_r="shrug", arm_l="shrug", legs="wide", zap=["hair"])),
    "nb_man_phone":       ("nb_man", dict(yaw=0.4, expr="excited", arm_r=dict(preset="hold", hand=(0.80, 0.62)), prop_r="phone", arm_l="hip")),
    "nb_woman_phone":     ("nb_woman", dict(yaw=-0.4, expr="shocked", arm_l=dict(preset="hold", hand=(-0.74, 0.62)), prop_l="phone", arm_r="cheeks")),
}

CANVAS = {}           # feet-relative sprite canvases, filled by register() (see canvas_sweep())


# ============================================================================= overlays: electric effects and the stool
def _zig(p0, p1, n, amp, seed):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    pts = [p0]
    for i in range(1, n):
        t = i / float(n)
        o = amp * (1 if i % 2 else -1) * (0.55 + 0.45 * _hash(seed, i))
        pts.append((p0[0] + dx * t + nx * o, p0[1] + dy * t + ny * o))
    pts.append(p1)
    return pts


def _bolt(pts, ink, w=0.030):
    d = _path(pts, close=False)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"/>'
            % (d, ink, w + 0.030, d, YELLOW, w, d, YCORE, w * 0.35))


def _glow(uid, c, r, col, op):
    return ('<radialGradient id="%s"><stop offset="0" stop-color="%s" stop-opacity="%.3f"/><stop offset="0.45" stop-color="%s" stop-opacity="%.3f"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient><circle cx="%.4f" cy="%.4f" r="%.4f" fill="url(#%s)"/>'
            % (uid, col, op, col, op * 0.5, col, c[0], c[1], r, uid))


def _overlays(f, pose, uid, ink):
    """electric effects and the stool, in the figure's (squashed, mirrored) frame; returns (under, over, ext)."""
    A = f["anchors"]
    t = _num(pose.get("t"), 0.0)
    zap = pose.get("zap") or []
    if isinstance(zap, str):
        zap = [zap]
    if not isinstance(zap, (list, tuple)):
        zap = []
    under, over, ext = [], [], []
    for z in zap:
        if z in ("finger_r", "finger_l"):
            s = z[-1]
            H, E, tip = A["hand_" + s], A["elbow_" + s], A["prop_tip_" + s]
            dx, dy = H[0] - E[0], H[1] - E[1]
            L = math.hypot(dx, dy) or 1.0
            ux, uy = dx / L, dy / L
            c = (tip[0] + ux * 0.04, tip[1] + uy * 0.04)
            under.append(_glow(uid + "_fg" + s, c, 0.34, "#fff3a0", 0.85))
            ext.append((c[0], c[1], 0.30))
            for i, a in enumerate((-32.0, -8.0, 14.0, 36.0)):
                vx, vy = _rot(ux, uy, a + 8.0 * math.sin(t * 6.283 + i))
                ln = 0.30 + 0.12 * _hash(i, t * 7.0)
                p1 = (c[0] + vx * ln, c[1] + vy * ln)
                over.append(_bolt(_zig(c, p1, 4, 0.035, i + 3.1 * t), ink, 0.022))
                ext.append((p1[0], p1[1], 0.04))
            over.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (_star(c, 0.11, 22.0 + 30 * t, 0.30, 4), YCORE, ink))
        elif z in ("torch_r", "torch_l"):
            s = z[-1]
            c = A["prop_tip_" + s]
            under.append(_glow(uid + "_tg" + s, c, 0.48, "#dff4ff", 0.95))
            ext.append((c[0], c[1], 0.48))
            over.append(_glow(uid + "_tc" + s, c, 0.14, "#ffffff", 1.0))
            for i in range(16):
                a = math.radians(15.0 + 150.0 * _hash(i, 1.7 + t))
                ln = 0.16 + 0.30 * _hash(i, 4.2 + t)
                r0 = 0.06 + 0.10 * _hash(i, 9.1 + t)
                p0 = (c[0] + math.cos(a) * r0, c[1] + math.sin(a) * r0)
                p1 = (c[0] + math.cos(a) * (r0 + ln), c[1] + math.sin(a) * (r0 + ln))
                col = ("#ffd23a", "#ff9a2a", "#fff6c0")[i % 3]
                over.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>' % (p0 + p1 + (col, 0.012 + 0.010 * (i % 2))))
                ext.append((p1[0], p1[1], 0.02))
            over.append('<path d="%s" fill="#ffffff" stroke="%s" stroke-width="0.010"/>' % (_star(c, 0.10, 45.0 * t, 0.28, 4), "#bfe6ff"))
        elif z == "hair":
            top = A["hat_top"]
            hc = (A["head"][0], A["head"][1] - 0.30)
            for i in range(5):
                a = math.radians(-160.0 + 35.0 * i + 10.0 * math.sin(t * 6.283 + i))
                r0, r1 = 0.72, 0.98 + 0.12 * _hash(i, t)
                p0 = (hc[0] + math.cos(a) * r0, hc[1] + math.sin(a) * r0 * 1.05)
                p1 = (hc[0] + math.cos(a) * r1, hc[1] + math.sin(a) * r1 * 1.05)
                over.append(_bolt(_zig(p0, p1, 3, 0.040, i + 5.0 * t), ink, 0.020))
                ext.append((p1[0], p1[1], 0.04))
            for i, (x, y) in enumerate(((-0.72, -0.25), (0.74, -0.30), (-0.30, top[1] - 0.12), (0.36, top[1] - 0.08))):
                over.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
                            % (_star((hc[0] + x, y), 0.055, 20.0 * i + 40 * t, 0.32, 4), YELLOW, ink))
        elif z == "body":
            b = f["bbox"]
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            rx, ry = (b[2] - b[0]) / 2 + 0.25, (b[3] - b[1]) / 2 + 0.05
            under.append('<radialGradient id="%s_bg"><stop offset="0" stop-color="#fff6a8" stop-opacity="0.95"/><stop offset="0.6" stop-color="#ffe86a" stop-opacity="0.6"/>'
                         '<stop offset="1" stop-color="#ffe86a" stop-opacity="0"/></radialGradient>'
                         '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="url(#%s_bg)"/>' % (uid, cx, cy, rx, ry, uid))
            for i, (ax, ay, bx, by) in enumerate(((-1.0, -0.15, -1.35, -0.45), (1.0, -0.10, 1.38, -0.40), (-0.95, 0.55, -1.35, 0.70),
                                                  (0.95, 0.60, 1.36, 0.78), (-0.80, 0.92, -1.25, 1.00), (0.80, 0.95, 1.25, 1.02))):
                p0 = (cx + ax * (rx - 0.30), cy + ay * ry * 0.85)
                p1 = (cx + bx * (rx - 0.30), cy + by * ry * 0.85)
                over.append(_bolt(_zig(p0, p1, 4, 0.05, i + 2.0 * t), ink, 0.026))
                ext.append((p1[0], p1[1], 0.05))
            ext.append((cx - rx, cy, 0.0))
            ext.append((cx + rx, cy, 0.0))
    if pose.get("stool"):
        hip = A["hip"]
        fy = f["feet_y"]
        sy = hip[1] + 0.07
        h = fy - sy
        x = hip[0]
        u = uid + "_st"
        under.append('<linearGradient id="%s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ec5a4c"/><stop offset="0.4" stop-color="#d23a30"/>'
                     '<stop offset="1" stop-color="#99261e"/></linearGradient>' % u)
        body = [(x - 0.27, sy + 0.05), (x + 0.27, sy + 0.05), (x + 0.35, fy), (x - 0.35, fy)]
        under.append('<path d="%s" fill="url(#%s)" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (_path(body), u, ink))
        for s in (-1, 1):       # leg cut-outs
            under.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.016"/>'
                         % (x + s * 0.05, fy, x + s * 0.17, sy + 0.05 + h * 0.25, x + s * 0.29, fy, "#6e1a14", ink))
        under.append('<ellipse cx="%.4f" cy="%.4f" rx="0.300" ry="0.075" fill="#e04a3e" stroke="%s" stroke-width="0.024"/>' % (x, sy + 0.04, ink))
        under.append('<rect x="%.4f" y="%.4f" width="0.110" height="0.030" rx="0.015" fill="#6e1a14"/>' % (x - 0.055, sy + 0.025))
        ext.extend(((x - 0.36, fy, 0.0), (x + 0.36, fy, 0.0)))
    return "".join(under), "".join(over), ext


def _num(v, d=0.0):
    try:
        v = float(v)
        return v if math.isfinite(v) else d
    except Exception:
        return d


def figure(cast_name, pose=None, uid="p"):
    """puppet.figure plus the lt overlays (zap, stool) and the hug_trunk scenery.  Installed as puppet.figure."""
    pd = pose if isinstance(pose, dict) else {}
    tr = pd.get("hug_trunk")
    if tr:
        f0 = _O["figure"](cast_name, dict(pd, hug_trunk=None, zap=None, stool=None), uid)
        sq = pd.get("squash", 1.0)
        sy = sq[1] if isinstance(sq, (tuple, list)) else _num(sq, 1.0)
        spec = tr if isinstance(tr, dict) else {}
        _TRUNK[0] = dict(x=_num(spec.get("x"), 0.0), w=_num(spec.get("w"), 0.48), top=-3.6,
                         bottom=f0["feet_y"] / (sy or 1.0) + _num(pd.get("head_dy"), 0.0) + 0.02)
    try:
        f = _O["figure"](cast_name, pose, uid)
    finally:
        _TRUNK[0] = None
    if not (pd.get("zap") or pd.get("stool")):
        return f
    ink = pd.get("ink")
    under, over, ext = _overlays(f, pd, str(uid), ("#" + ink.lstrip("#")) if P._is_hex(ink) else P.INK)
    b = list(f["bbox"])
    for (x, y, r) in ext:
        b[0], b[1], b[2], b[3] = min(b[0], x - r), min(b[1], y - r), max(b[2], x + r), max(b[3], y + r)
    f = dict(f)
    f["svg"] = '<g id="%s_lt">%s%s%s</g>' % (uid, under, f["svg"], over)
    f["bbox"] = tuple(b)
    return f


# ============================================================================= registration
def _build_presets():
    for b, tbl in LT_ARMS.items():
        for n, v in tbl.items():
            P.ARM_PRESETS[b].setdefault(n, v)
    if "child" in P.ARM_PRESETS:
        f = X.CHILD_ARM / 0.74
        for n, v in LT_ARMS["slim"].items():
            P.ARM_PRESETS["child"].setdefault(n, (v[0] * f, v[1] * f) + tuple(v[2:]))


def register():
    if getattr(P, "_lt_cast_registered", False):
        return
    for name in ("_torso", "_face", "_moustache", "_ink_limb", "_prop", "_norm", "figure"):
        _O[name] = getattr(P, name)
    X.COSTUMES.update(LT_COSTUMES)
    X.HATS.update(LT_HATS)

    def _norm(C, pose):
        _POSE[0] = pose if isinstance(pose, dict) else {}
        return _O["_norm"](C, pose)
    P._norm = _norm
    P._torso = _torso
    P._face = _face
    P._moustache = _moustache
    P._ink_limb = _ink_limb
    P._prop = _prop
    P.figure = figure
    P.PROP_TYPES = tuple(P.PROP_TYPES) + tuple(t for t in LT_PROPS if t not in P.PROP_TYPES)
    P.PROP_TIP.update(LT_TIP)
    P.EXPRESSIONS.setdefault("scream", SCREAM)
    _build_presets()
    for n, c in LT_CAST.items():
        P.CAST[n] = c
    P.STORY.update(POSES)
    CANVAS.update(LT_CANVAS)
    X.CANVAS.update(LT_CANVAS)        # cast_ext puts these into sprites.DEFAULT_CANVAS as well
    X.register_stage()
    P._lt_cast_registered = True


# feet-relative canvases (x0, y0, x1, y1) in D, from canvas_sweep() (+0.3 D head room, snapped to 1/16)
LT_CANVAS = {
    "welder": (-1.8125, -4.3125, 1.8125, 0.1250),
    "hong": (-1.5625, -4.1250, 1.5625, 0.1250),
    "kim": (-1.4375, -4.1875, 1.4375, 0.1250),
    "nurse": (-1.4375, -4.1875, 1.4375, 0.1250),
    "nb_man": (-1.5000, -4.1875, 1.5000, 0.1250),
    "nb_woman": (-1.4375, -4.0625, 1.4375, 0.1250),
}

register()


# ============================================================================= sprite rendering (transparent PNG)
def sprite_svg(name, pose, height_px, fit="canvas", pad_px=4, uid="s"):
    """SVG text of one member at a given image height.  fit="canvas": the member's fixed feet-relative canvas (same D px and
    feet pixel for every pose: use this for frame sequences); fit="bbox": tight crop around this pose.
    Returns (svg, info) with info = {w, h, D_px, feet_px, anchors_px}."""
    f = P.figure(name, pose, uid)
    if fit == "canvas":
        x0, y0, x1, y1 = CANVAS.get(name) or X.CANVAS.get(name) or (-1.9, -4.6, 1.9, 0.125)
        D = float(height_px) / (y1 - y0)
        W = int(round((x1 - x0) * D))
        fx, fy = -x0 * D, -y0 * D
        ox = fx - f["anchors"]["feet"][0] * D
        oy = fy - f["feet_y"] * D
    else:
        b = f["bbox"]
        D = (float(height_px) - 2 * pad_px) / (b[3] - b[1])
        W = int(math.ceil((b[2] - b[0]) * D + 2 * pad_px))
        ox, oy = pad_px - b[0] * D, pad_px - b[1] * D
        fx, fy = ox + f["anchors"]["feet"][0] * D, oy + f["feet_y"] * D
    H = int(height_px)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><g transform="translate(%.3f %.3f) scale(%.4f)">%s</g></svg>'
           % (W, H, W, H, ox, oy, D, f["svg"]))
    an = dict((k_, (ox + v[0] * D, oy + v[1] * D)) for k_, v in f["anchors"].items())
    return svg, dict(w=W, h=H, D_px=D, feet_px=(fx, fy), anchors_px=an, bbox_D=f["bbox"])


def render_pngs(jobs, tmpdir=None):
    """jobs = [{"name", "pose", "out", "height_px", "fit" (opt)}...]: one Chromium launch for all of them (raster_multi.js).
    Returns the list of info dicts (see sprite_svg) with "out" and "ms_per_png" added."""
    tmpdir = tmpdir or os.path.join(HERE, "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    rjobs, infos = [], []
    for i, j in enumerate(jobs):
        svg, info = sprite_svg(j["name"], j.get("pose") or {}, j["height_px"], j.get("fit", "canvas"), uid="s%d" % i)
        sp = os.path.join(tmpdir, "sprite_%03d.svg" % i)
        with open(sp, "w") as fh:
            fh.write(svg)
        rjobs.append(dict(svg=sp, out=os.path.abspath(j["out"]), w=info["w"], h=info["h"], bg="transparent"))
        info["out"] = j["out"]
        infos.append(info)
    jp = os.path.join(tmpdir, "jobs.json")
    with open(jp, "w") as fh:
        json.dump(rjobs, fh)
    t0 = time.time()
    r = subprocess.run(["node", os.path.join(V2P, "raster_multi.js"), jp], cwd=V2P, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       universal_newlines=True)
    dt = (time.time() - t0) * 1000.0
    if r.returncode != 0:
        raise RuntimeError(r.stdout)
    for info in infos:
        info["ms_per_png"] = dt / max(len(jobs), 1)
    return infos


def render_png(name, pose, out_path, height_px, fit="canvas"):
    """one member in one pose / expression -> transparent PNG of the given pixel height (Chromium via raster_multi.js).
    For many frames call render_pngs() once: the browser launch (about 1 s) is then paid once."""
    return render_pngs([dict(name=name, pose=pose, out=out_path, height_px=height_px, fit=fit)])[0]


# ============================================================================= QA helpers
def canvas_sweep(verbose=True):
    res = {}
    for name in NEW:
        C = LT_CAST[name]
        poses = [{}]
        for a in sorted(P.ARM_PRESETS[C["build"]]):
            for pr in (None, "torch", "cash", "handfan", "phone"):
                poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6, hair_state="bolt", mask="up"))
                poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.9, 1.08), hair_state="bolt"))
        poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "sweat"], zap=["hair", "body"], hair_state="bolt")]
        for _, (nm, p) in POSES.items():
            if nm == name and not p.get("hug_trunk"):
                poses.append(p)
        x0 = y0 = 1e9
        x1 = y1 = -1e9
        for p in poses:
            f = P.figure(name, p, "c")
            fx, fy = f["anchors"]["feet"][0], f["feet_y"]
            b = f["bbox"]
            x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
        snap = lambda v: math.floor(v * 16) / 16.0 if v < 0 else math.ceil(v * 16) / 16.0   # noqa: E731
        c = (snap(min(x0, -x1) - 0.05), snap(y0 - 0.30), snap(max(x1, -x0) + 0.05), max(0.125, snap(y1 + 0.02)))
        res[name] = c
        if verbose:
            print("%-9s pose range (%.3f, %.3f, %.3f, %.3f) -> canvas %r   current %r" % (name, x0, y0, x1, y1, c, LT_CANVAS.get(name)))
    return res


def run_tests():
    """the v2 robustness suite (test_puppet.py, quick) on the new names, determinism and hero/boss unchanged."""
    import test_puppet as T
    T.CASTS = NEW
    rc = T.main(["--quick"])
    a = P.figure("welder", POSES["welder_shocked"][1], "d")["svg"]
    b = P.figure("welder", POSES["welder_shocked"][1], "d")["svg"]
    print("determinism:", "ok" if a == b else "FAIL")
    return rc


# ============================================================================= sheets
NIGHT, NIGHT_FLOOR, SOI, SOI_FLOOR = "#4a4a8a", "#3a3a6e", "#d8c8b0", "#bfae94"
NIGHT_RIM = "#9a9ae0"


def _label(x, y, txt, size=15, anchor="start"):
    return ('<text x="%d" y="%d" font-family="Arial, Loma, sans-serif" font-size="%d" font-weight="700" fill="#ffffff" stroke="#1a1015" '
            'stroke-width="3" paint-order="stroke" stroke-linejoin="round" text-anchor="%s">%s</text>' % (x, y, size, anchor, txt))


def _place(name, pose, uid, D, x, y, anchor="feet", shadow=0.0):
    f = P.figure(name, pose, uid)
    if anchor == "feet":
        tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
        s = ('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s"))) if shadow else ""
    else:
        tx, ty, s = x, y, ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


LINEUP = (("welder", "welder · คุณ", dict(yaw=0.2, mask="up", arm_l="hip", arm_r="down", prop_r=dict(type="torch", angle=75))),
          ("welder", "welder (bolt)", dict(yaw=-0.15, hair_state="bolt", arm_r="down", arm_l="down")),
          ("hong", "hong · เจ๊หงส์", dict(yaw=-0.2, arm_r="hip", arm_l="hold", prop_l=dict(type="handfan", angle=-70))),
          ("kim", "kim · เฮียกิม", dict(yaw=0.2, arm_r="hold", prop_r=dict(type="screwdriver", angle=-60), arm_l="behind")),
          ("nurse", "nurse · พยาบาล", dict(yaw=0.15, arm_r="down", arm_l="down")),
          ("nb_man", "nb_man · ลุงข้างบ้าน", dict(yaw=-0.15, arm_r="akimbo", arm_l="akimbo")),
          ("nb_woman", "nb_woman · ป้าข้างบ้าน", dict(yaw=0.2, arm_r=dict(preset="hold", hand=(0.70, 0.70)), prop_r="phone", arm_l="down")))


def build_lineup():
    o = []
    y = 0
    W = 0
    n = 0
    for D in (110, 220):
        for bg, floor, nm, night in ((NIGHT, NIGHT_FLOOR, "storm-night rooftop %s" % NIGHT, True), (SOI, SOI_FLOOR, "sunny soi %s" % SOI, False)):
            step = int(1.30 * D)
            h = int(4.55 * D)
            w = step * len(LINEUP) + int(0.5 * D)
            W = max(W, w)
            o.append('<rect x="0" y="%d" width="4000" height="%d" fill="%s"/>' % (y, h, bg))
            o.append('<rect x="0" y="%d" width="4000" height="%d" fill="%s"/>' % (y + h - int(0.36 * D), int(0.36 * D), floor))
            for i, (c, lab, p) in enumerate(LINEUP):
                n += 1
                pp = dict(p, expr="neutral")
                if night:
                    pp["rim"] = NIGHT_RIM
                g, f = _place(c, pp, "l%d" % n, D, int(0.25 * D) + step * i + step / 2, y + h - int(0.2 * D), shadow=0.9)
                o.append(g)
                l1, _, l2 = lab.partition(" · ")
                fs = 13 if D < 200 else 20
                o.append(_label(int(0.25 * D) + step * i + step // 2, y + 8 + fs, l1, fs, "middle"))
                if l2:
                    o.append(_label(int(0.25 * D) + step * i + step // 2, y + 12 + 2 * fs, l2, fs, "middle"))
            o.append(_label(8, y + h - 8, "%s, head D = %d px" % (nm, D), 14))
            y += h
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, y, W, y, "".join(o)), W, y


EXPR_ROW = (("normal", dict(expr="neutral")), ("happy", dict(expr="happy")), ("wide / shocked", dict(expr="shocked", fx=["sweat"])),
            ("angry", dict(expr="angry", pitch=-0.5)), ("sad", dict(expr="sad", pitch=0.8)), ("smug", dict(expr="smug", yaw=0.25)),
            ("scream", dict(expr="scream")), ("3/4 view", dict(expr="neutral", yaw=0.6)))
HEAD_ROWS = (("welder", {}), ("welder", dict(hair_state="bolt")), ("welder", dict(mask="up")), ("hong", {}), ("kim", {}), ("nurse", {}),
             ("nurse", dict(hair_state="bolt")), ("nb_man", {}), ("nb_woman", {}))


def build_poses():
    cw, ch = 300, 620
    cols = 8
    o = []
    y = 0
    names = list(POSES.keys())
    rows = [names[i:i + cols] for i in range(0, len(names), cols)]
    n = 0
    for ri, row in enumerate(rows):
        for ci, key in enumerate(row):
            name, p = POSES[key]
            x0 = ci * cw
            night = (ri + ci) % 2 == 0
            bg, floor = (NIGHT, NIGHT_FLOOR) if night else (SOI, SOI_FLOOR)
            fl = y + ch - 46
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, cw, ch, bg))
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, fl - 20, cw, ch - (fl - 20 - y), floor))
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y, cw, ch, x0, y, cw, ch))
            n += 1
            pp = dict(p)
            if night:
                pp["rim"] = NIGHT_RIM
            g, f = _place(name, pp, "p%d" % n, 128, x0 + cw / 2, fl, shadow=0.9)
            o.append(g + "</svg>")
            o.append(_label(x0 + 8, y + 22, key, 15))
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#1a1015" stroke-width="2"/>' % (x0, y, cw, ch))
        y += ch
    hw, hh = 300, 310
    for ri, (name, extra) in enumerate(HEAD_ROWS):
        for ci, (lab, p) in enumerate(EXPR_ROW):
            x0 = ci * hw
            night = (ri + ci) % 2 == 1
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, hw, hh, NIGHT if night else SOI))
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d">' % (x0, y, hw, hh, hw, hh))
            n += 1
            pp = dict(extra)
            pp.update(p)
            g, f = _place(name, pp, "h%d" % n, 150, hw / 2, hh * 0.68, anchor="head")
            o.append(g + "</svg>")
            tag = name + ("" if not extra else " " + ",".join("%s" % v for v in extra.values()))
            o.append(_label(x0 + 8, y + 20, "%s: %s" % (tag, lab), 14))
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#1a1015" stroke-width="2"/>' % (x0, y, hw, hh))
        y += hh
    W = cols * cw
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, y, W, y, "".join(o)), W, y


def _write(svg, w, h, base, small_w=1400):
    sp = os.path.join(HERE, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(HERE, base + ".png")
    t0 = time.time()
    r = subprocess.run(["node", os.path.join(V2P, "raster.js"), sp, out, str(int(w)), str(int(h)), "1"], cwd=V2P,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    print(r.stdout.strip(), "(%.1f s)" % (time.time() - t0))
    try:
        from PIL import Image
        im = Image.open(out).convert("RGB")
        s = small_w / float(im.width)
        im.resize((small_w, int(im.height * s)), Image.LANCZOS).save(os.path.join(HERE, base + "_s.jpg"), quality=88)
    except Exception as e:          # pragma: no cover
        print("no small jpg:", e)
    os.remove(sp)
    return out


def bench(n=24, height_px=512):
    """time per sprite PNG: one call of render_png (browser launch included) and a batch of n through render_pngs."""
    d = os.path.join(HERE, "tmp", "bench")
    os.makedirs(d, exist_ok=True)
    keys = list(POSES.keys())
    t0 = time.time()
    render_png("welder", POSES["welder_shocked"][1], os.path.join(d, "single.png"), height_px)
    t1 = time.time()
    jobs = [dict(name=POSES[keys[i % len(keys)]][0], pose=POSES[keys[i % len(keys)]][1], out=os.path.join(d, "b%02d.png" % i), height_px=height_px)
            for i in range(n)]
    infos = render_pngs(jobs)
    t2 = time.time()
    t3 = time.time()
    for i in range(200):
        P.figure("welder", POSES["welder_shocked"][1], "b")
    t4 = time.time()
    print("figure() call: %.2f ms" % ((t4 - t3) / 200 * 1000))
    print("render_png single (Chromium launch included): %.0f ms" % ((t1 - t0) * 1000))
    print("render_pngs batch of %d at %d px: %.0f ms total, %.0f ms per PNG (incl. one launch)" % (n, height_px, (t2 - t1) * 1000, (t2 - t1) * 1000 / n))
    return infos


def main(argv):
    cmd = argv[0] if argv else "lineup"
    if cmd == "lineup":
        svg, W, H = build_lineup()
        _write(svg, W, H, "lineup", 1600)
    elif cmd == "poses":
        svg, W, H = build_poses()
        _write(svg, W, H, "poses", 1600)
    elif cmd == "bench":
        bench()
    elif cmd == "canvas":
        canvas_sweep()
    elif cmd == "test":
        return run_tests()
    elif cmd == "png":            # python3 lt_cast.py png welder_shocked out.png 512
        nm, p = POSES[argv[1]]
        print(render_png(nm, p, argv[2], int(argv[3]) if len(argv) > 3 else 512))
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
