#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""puppet.py -- production 2D SVG character puppets (white round-headed stick figures, plum ink).

Merges spec/character_puppet_proto.py (body) and spec/face_proto/faces_ref.py (faces) and
implements spec/character_anatomy.md section 3 + spec/face_expressions.md section 3.

Conventions (shared by every v2 module)
  * unit = D, the outer ink-to-ink head diameter.  x right, y DOWN.
  * puppet local frame: head centre at (0, 0); a standing figure is about 3 D tall.
  * every function returns SVG *fragments* (no outer <svg>) and takes a uid prefix for ids.

Public API (exact signatures, every pose key, presets, anchors and worked examples: API.md next to this file)
  CAST                                  dict of cast definitions ("hero", "boss")
  figure(cast_name, pose=None, uid="p") -> {"svg", "feet_y", "bbox", "anchors"}
  contact_shadow(width_D, uid="cs")     -> soft ellipse fragment centred on (0, 0)
  place_svg(fig, x, y, scale)           wrap a figure so its feet land on (x, y)
  hand_for_tip(prop, tip, angle)        hand target that puts a held prop's tip on a point
  resolve_pose / lerp_pose              presets -> numbers, in-between poses
  python3 puppet.py sheet|compare|test|bench        (measure.py re-measures the render against the spec)

Draw order, back to front (anatomy 3.4): focus lines, optional limb rim, back arms, legs and feet, torso ink silhouette,
torso fill and costume (clipped), front arms + props + hands, head ink disc, head fill + crescent (+ purple fill), hair
patches (clipped to the fill), face, blush / sweat / tears, ear pencil, hat, top-layer arms, steam and Z.

No random numbers, no time, no hash(): the same input always gives the same string.
Outline wobble is baked into the path geometry with a fixed seed per character (no filters).

Reviewed and repaired (REVIEW.md, test_puppet.py): own cast designs, hand-inked limbs with a per-cast weight, head outline
re-calibrated against the reference with one measuring tool, IK without dead zone or flip, input hardening, optional rim.
"""
import math
import os
import sys
from functools import lru_cache

__all__ = ["CAST", "figure", "contact_shadow", "resolve_pose", "lerp_pose", "place_svg", "hand_for_tip", "INK",
           "EXPRESSIONS", "MOUTHS", "ARM_PRESETS", "LEG_PRESETS", "PROP_TYPES", "PROP_TIP", "FX_TYPES", "STORY"]

# ----------------------------------------------------------------------------- constants
# ink: character_anatomy.md says #3a2832, face_expressions.md says #3a2a30 (2 levels apart).
# We use #3a2832 (anatomy spec; mean of its samples #382731 #3a2932 #382630) for everything.
INK = "#3a2832"
HEAD_FILL = "#fef7f6"      # face spec 2.2 (clip A, identical in 5 frames)
HEAD_SHADE = "#e9dceb"     # lavender crescent on the lower-right rim
CAV, TONG, TEETH = "#4d2433", "#7b626c", "#fef9f8"
SWEAT = ("#b6e3ff", "#def9ff", "#5c647a")
PURPLE = ("#b769e1", "#a152cd", "#7c35a8")
LW = 0.060                 # limb stroke, arms == legs (anatomy 3.1: 0.065, allowed 0.055-0.075; close shots measure 0.04-0.046)
HAND_R = 0.065             # hand ball diameter 0.13
R_FILL = 0.463             # head fill radius / D (face spec 2.1)
# the face spec measures from the centre of the white fill disc; the ink silhouette is offset
# down-right from it.  FC puts the fill centre so that the INK bounding box is centred on (0, 0).
FC = (-0.012, -0.023)
FOOT_LEN = 0.14            # clip A stub, anatomy "known gaps": 0.12-0.15


def _clamp(v, a, b):
    return a if v < a else (b if v > b else v)


def _num(v, d=0.0):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return d
    if v != v or v in (float("inf"), float("-inf")):
        return d
    if v > 1e6:
        return 1e6
    if v < -1e6:
        return -1e6
    return v


def _is_hex(h):
    """True for "#rrggbb" / "rrggbb"."""
    if not isinstance(h, str):
        return False
    h = h.lstrip("#")
    if len(h) != 6:
        return False
    try:
        int(h, 16)
    except ValueError:
        return False
    return True


def _smooth(e0, e1, x):
    if e1 == e0:
        return 0.0 if x < e0 else 1.0
    t = _clamp((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _lerp(a, b, t):
    return a + (b - a) * t


def _rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _hex(r, g, b):
    return "#%02x%02x%02x" % (int(_clamp(round(r), 0, 255)), int(_clamp(round(g), 0, 255)), int(_clamp(round(b), 0, 255)))


def _shade(h, k):
    r, g, b = _rgb(h)
    return _hex(r * k, g * k, b * k)


def _mix(h1, h2, t):
    a, b = _rgb(h1), _rgb(h2)
    return _hex(a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


class _Ctx(object):
    """per-figure drawing context: id prefix, ink colour and the per-shot multiply tint."""
    __slots__ = ("uid", "ink", "tint", "_cc", "defs", "ext")

    def __init__(self, uid, ink, tint):
        self.uid = uid
        self.ink = ink
        self.tint = tint          # None or (r, g, b) 0..255
        self._cc = {}
        self.defs = []
        self.ext = []             # bbox accumulator: (x, y, radius)

    def c(self, h):
        """fill colour after the shot tint (multiply)."""
        t = self.tint
        if t is None:
            return h
        v = self._cc.get(h)
        if v is None:
            r, g, b = _rgb(h)
            v = self._cc[h] = _hex(r * t[0] / 255.0, g * t[1] / 255.0, b * t[2] / 255.0)
        return v


def _pts(pts):
    return " ".join("%.4f,%.4f" % p for p in pts)


def _poly_d(pts):
    return "M" + "L".join("%.4f,%.4f" % p for p in pts) + "Z"


def _smooth_open(pts):
    """Catmull-Rom through pts as cubic beziers (open)."""
    n = len(pts)
    out = ["M%.4f,%.4f" % pts[0]]
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[0]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < n else pts[n - 1]
        out.append("C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (
            p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
            p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]))
    return "".join(out)


def _smooth_closed(pts):
    """closed Catmull-Rom through pts as cubic beziers.  Used for the head and torso contours: as straight-segment polygons
    they showed facets in extreme close-ups (head D = 690 px, as in reference B t21.0)."""
    n = len(pts)
    out = ["M%.4f,%.4f" % pts[0]]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        out.append("C%.4f,%.4f %.4f,%.4f %.4f,%.4f" % (
            p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
            p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, p2[0], p2[1]))
    out.append("Z")
    return "".join(out)


def _rot(x, y, deg):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


# ----------------------------------------------------------------------------- head disc
# outline width (D) every 30 degrees, 0 = 3 o'clock, 90 = bottom.  Re-calibrated in the review with ONE tool
# (review_measure.outline_profile) run on the reference frames and on our render: clip A reads 0.051 / 0.049-0.062 /
# 0.062-0.081 / 0.080-0.088 (chin, collar) / 0.051-0.058 / 0.032-0.045 / 0.024-0.030 at 0 / 30 / 60 / 90 / 120 / 150 / 180 deg.
# The first version followed the face spec table (2.0-4.4 percent on the lower left), which that tool reads 0.010-0.015 D
# thinner than the reference on the lower left.  210..330 (under the hat in every reference frame) are assumed.
_OUTLINE_W = (0.052, 0.059, 0.071, 0.074, 0.050, 0.036, 0.027, 0.024, 0.023, 0.024, 0.030, 0.041)


def _outline_w(deg):
    """periodic Catmull-Rom through the 12 table values.  (The first version eased between the nodes with a cosine, which
    put a plateau at every node: at head D = 690 px the outline read as a 12-sided polygon with rounded corners.)"""
    deg %= 360.0
    i = int(deg // 30) % 12
    t = (deg - 30 * i) / 30.0
    w0, w1, w2, w3 = _OUTLINE_W[i - 1], _OUTLINE_W[i], _OUTLINE_W[(i + 1) % 12], _OUTLINE_W[(i + 2) % 12]
    t2, t3 = t * t, t * t * t
    return 0.5 * (2 * w1 + (w2 - w0) * t + (2 * w0 - 5 * w1 + 4 * w2 - w3) * t2 + (3 * w1 - w0 - 3 * w2 + w3) * t3)


def _wob(th, s):
    return 0.6 * math.sin(3 * th + s) + 0.5 * math.sin(5 * th + 1.7 * s) + 0.3 * math.sin(8 * th + 0.6 * s)


def _rough(th, s):
    """fine felt-pen irregularity baked into the edge (replaces the feTurbulence of the prototypes)."""
    return 0.55 * math.sin(13 * th + 2.1 * s) + 0.45 * math.sin(21 * th + 0.7 * s) + 0.35 * math.sin(34 * th + 1.3 * s)


def _fill_r(th, seed):
    return R_FILL + 0.007 * math.cos(2 * th + 0.2 * seed) + 0.0105 * _wob(th, seed) + 0.0014 * _rough(th, seed + 4.0)


def _circle_fit(pts):
    """algebraic least-squares circle through pts -> (cx, cy, r).  Pure python (3 x 3 normal equations)."""
    n = float(len(pts))
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] * p[0] for p in pts)
    syy = sum(p[1] * p[1] for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    z = [p[0] * p[0] + p[1] * p[1] for p in pts]
    sz = sum(z)
    sxz = sum(p[0] * q for p, q in zip(pts, z))
    syz = sum(p[1] * q for p, q in zip(pts, z))
    # solve [sxx sxy sx; sxy syy sy; sx sy n] [a b c]^T = [sxz syz sz]^T  (x^2 + y^2 = a x + b y + c)
    m = [[sxx, sxy, sx, sxz], [sxy, syy, sy, syz], [sx, sy, n, sz]]
    for i in range(3):
        piv = max(range(i, 3), key=lambda r: abs(m[r][i]))
        m[i], m[piv] = m[piv], m[i]
        if abs(m[i][i]) < 1e-12:
            return 0.0, 0.0, R_FILL
        for r in range(3):
            if r != i:
                f = m[r][i] / m[i][i]
                m[r] = [a - f * b for a, b in zip(m[r], m[i])]
    a, b, c = m[0][3] / m[0][0], m[1][3] / m[1][1], m[2][3] / m[2][2]
    return a / 2.0, b / 2.0, math.sqrt(max(c + a * a / 4.0 + b * b / 4.0, 1e-12))


@lru_cache(maxsize=64)
def _head_geom(seed):
    """(ink silhouette d, fill d) as smooth closed curves through 144 points, fill centre at (0, 0).
    The wobbly fill disc is re-centred and re-scaled so that a circle fitted to its lower arc (25..155 degrees: the part
    that is never under a hat, and the definition of D in the face spec: D = 2.16 R_fill) is exactly R_FILL about the
    origin.  Without this the per-character wobble made one head read 2.7 percent larger than the other."""
    n = 144
    raw = []
    for i in range(n):
        d = i * 360.0 / n
        th = math.radians(d)
        rf = _fill_r(th, seed)
        ro = rf + _outline_w(d) + 0.005 * _wob(th, seed + 2.3) + 0.0016 * _rough(th, seed)
        raw.append((d, math.cos(th), math.sin(th), rf, ro))
    cx, cy, r = _circle_fit([(c * rf, s * rf) for (d, c, s, rf, ro) in raw if 25.0 <= d <= 155.0])
    g = R_FILL / r
    fil = [((c * rf - cx) * g, (s * rf - cy) * g) for (d, c, s, rf, ro) in raw]
    # the outline keeps its measured width: the ink edge is the normalised fill edge pushed out along the same ray
    ink = [(f[0] + c * (ro - rf), f[1] + s * (ro - rf)) for f, (d, c, s, rf, ro) in zip(fil, raw)]
    return _smooth_closed(ink), _smooth_closed(fil)


# ----------------------------------------------------------------------------- face building blocks
# all in the head frame (origin = fill centre).  k = _Ctx.  cx, cy = eye centre; mx, my = mouth centre.
def _eye_half(k, cx, cy, gaze=0.0, s=1.0, tilt=0.0, sq=1.0):
    """half-lid eye: lid bar .178 x .030, pupil = lower part of an ellipse rx .043 ry .062 (bbox .178 x .099).
    sq < 1 squashes the pupil (blink in-between)."""
    bar_y = cy - 0.035 * s
    rx, ry = 0.043 * s, 0.062 * s * sq
    ecx = cx + gaze
    xh = rx * 0.935
    body = ('<path d="M%.4f,%.4f A%.4f,%.4f 0 1 0 %.4f,%.4f Z" fill="%s"/>'
            '<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="%.4f" stroke-linecap="round" fill="none"/>'
            % (ecx - xh, bar_y, rx, ry, ecx + xh, bar_y, k.ink,
               cx - 0.074 * s, bar_y, cx + 0.074 * s, bar_y, k.ink, 0.030 * s))
    return '<g transform="rotate(%.3f %.4f %.4f)">%s</g>' % (tilt, cx, cy, body)


def _eye_ring(k, cx, cy, s=1.0, pupil=0.030, gx=0.0, gy=0.0, white=HEAD_FILL):
    """ring eye: outer dia .222, ring .025, pupil dia .060 (excited) or .033 (frightened)."""
    return ('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>'
            '<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>'
            % (cx, cy, 0.0985 * s, white, k.ink, 0.025 * s, cx + gx, cy + gy, pupil * s, k.ink))


def _eye_lens(k, cx, cy, s=1.0, white=HEAD_FILL):
    """blink in-between of a ring eye: almond .222 x .080, mostly ink."""
    return ('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>'
            % (cx, cy, 0.111 * s, 0.040 * s, k.ink,
               cx - 0.055 * s, cy, 0.022 * s, 0.013 * s, white,
               cx + 0.055 * s, cy, 0.022 * s, 0.013 * s, white))


def _eye_happy(k, cx, cy, s=1.0):
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (cx - 0.068 * s, cy + 0.016 * s, cx, cy - 0.048 * s, cx + 0.068 * s, cy + 0.016 * s, k.ink, 0.029 * s))


def _eye_closed(k, cx, cy, s=1.0):
    return ('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (cx - 0.068 * s, cy, cx + 0.068 * s, cy, k.ink, 0.029 * s))


def _eye_dot(k, cx, cy, s=1.0, sq=1.0):
    return '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/>' % (cx, cy, 0.041 * s, 0.0575 * s * sq, k.ink)


def _eye_squeeze(k, cx, cy, side, s=1.0):
    q = -side
    return ('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            '<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (cx - q * 0.080 * s, cy - 0.062 * s, cx + q * 0.070 * s, cy - 0.010 * s, k.ink, 0.033 * s,
               cx - q * 0.085 * s, cy + 0.032 * s, cx + q * 0.070 * s, cy + 0.016 * s, k.ink, 0.030 * s))


def _brow_stroke(k, cx, cy, side, ang=0.0, L=0.17, th=0.045, w=1.0):
    """slightly bowed stroke; ang > 0 = inner end lower (angry), < 0 = outer end lower (sad). w scales it (0..1)."""
    a = math.radians(ang) * (-side)
    L, th = L * w, th * w
    h = max(L - th, 0.0) / 2
    dx, dy = h * math.cos(a), h * math.sin(a)
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round"/>'
            % (cx - dx, cy - dy, cx, cy - 0.012 * w, cx + dx, cy + dy, k.ink, th))


def _brow_dome(k, cx, cy, s=1.0):
    """hero neutral brow: solid half-lens with a flat base, .16 x .04."""
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.006" stroke-linejoin="round"/>'
            % (cx - 0.08 * s, cy + 0.02 * s, cx, cy - 0.06 * s, cx + 0.08 * s, cy + 0.02 * s, k.ink, k.ink))


def _mouth_dash(k, mx, my, ang=0.0):
    return ('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round" transform="rotate(%.2f %.4f %.4f)"/>'
            % (mx - 0.035, my, mx + 0.035, my, k.ink, ang, mx, my))


def _mouth_frown(k, mx, my):
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
            % (mx - 0.045, my + 0.008, mx, my - 0.014, mx + 0.045, my + 0.008, k.ink))


def _mouth_smirk(k, mx, my, side=1):
    q = side
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.032" stroke-linecap="round"/>'
            % (mx - q * 0.042, my - 0.018, mx - q * 0.018, my + 0.026, mx + q * 0.042, my + 0.015, k.ink))


def _mouth_smile(k, mx, my):
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.034" stroke-linecap="round"/>'
            % (mx - 0.055, my - 0.012, mx, my + 0.040, mx + 0.055, my - 0.012, k.ink))


def _mouth_grin(k, mx, my, w=0.42):
    """crescent .42 x .12 with four upper teeth (clip id uid_gt)."""
    h = w / 2
    q = w / 0.42
    cid = k.uid + "_gt"
    teeth = "".join('<rect x="%.4f" y="%.4f" width="%.4f" height="0.11" fill="%s"/>'
                    % (mx + x * q - 0.0285 * q, my - 0.06, 0.057 * q, k.c(TEETH)) for x in (-0.111, -0.037, 0.037, 0.111))
    return ('<clipPath id="%s"><path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"/></clipPath>'
            '<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.006" stroke-linejoin="round"/>'
            '<g clip-path="url(#%s)">%s</g>'
            % (cid, mx - 0.155 * q, my - 0.035, mx, my + 0.008, mx + 0.155 * q, my - 0.035, mx, my + 0.110, mx - 0.155 * q, my - 0.035,
               mx - h, my - 0.055, mx, my - 0.005, mx + h, my - 0.055, mx, my + 0.185, mx - h, my - 0.055, k.ink, k.ink,
               cid, teeth))


def _mouth_flat(k, mx, my):
    return '<ellipse cx="%.4f" cy="%.4f" rx="0.143" ry="0.029" fill="%s"/>' % (mx, my, k.ink)


def _mouth_open(k, mx, my, w=0.28, h=0.17):
    """talking mouth: maroon ellipse with an ink rim .018 and two faint dashes."""
    w, h = max(w, 0.03), max(h, 0.03)
    t = _clamp((h - 0.05) / 0.05, 0.0, 1.0)      # dashes fade away in a nearly closed mouth
    return ('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="0.018"/>'
            '<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.008" stroke-linecap="round" fill="none" opacity="%.3f"/>'
            % (mx, my, max(w / 2 - 0.009, 0.006), max(h / 2 - 0.009, 0.006), k.c(CAV), k.ink,
               mx - 0.03, my - h * 0.30, mx + 0.03, my - h * 0.30, mx - 0.025, my + h * 0.33, mx + 0.025, my + h * 0.33, k.c(TONG), t))


def _mouth_o(k, mx, my):
    """shock: egg .19 x .17, narrower at the top."""
    return ('<path d="M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="0.024" ry="0.007" fill="%s"/>'
            % (mx, my - 0.076, mx + 0.100, my - 0.076, mx + 0.135, my + 0.076, mx, my + 0.076,
               mx - 0.135, my + 0.076, mx - 0.100, my - 0.076, mx, my - 0.076, k.c(CAV), k.ink, mx, my + 0.052, k.c(TONG)))


def _mouth_clench(k, mx, my):
    """rounded rect .18 x .13, 4 x 2 teeth."""
    w, h, t = 0.18, 0.13, 0.024
    s = ['<rect x="%.4f" y="%.4f" width="%.4f" height="%.4f" rx="0.032" fill="%s" stroke="%s" stroke-width="%.3f"/>'
         % (mx - w / 2 + t / 2, my - h / 2 + t / 2, w - t, h - t, k.c(TEETH), k.ink, t)]
    d = "M%.4f,%.4f L%.4f,%.4f" % (mx - w / 2 + t, my, mx + w / 2 - t, my)
    for q in (-1, 0, 1):
        x = mx + q * (w - 2 * t) / 4
        d += "M%.4f,%.4f L%.4f,%.4f" % (x, my - h / 2 + t, x, my + h / 2 - t)
    s.append('<path d="%s" stroke="%s" stroke-width="0.013" fill="none"/>' % (d, k.ink))
    return "".join(s)


def _mouth_wavy(k, mx, my):
    return ('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.040" stroke-linecap="round" stroke-linejoin="round"/>'
            % (mx - 0.105, my + 0.020, mx - 0.070, my - 0.045, mx - 0.030, my - 0.005, mx, my + 0.022, mx + 0.030, my - 0.005,
               mx + 0.070, my - 0.045, mx + 0.105, my + 0.020, k.ink))


def _moustache(k, mx, my, s=1.0):
    """chief's moustache (own design): short, bushy, drooping chevron .30 x .095 with a centre notch."""
    def P(x, y):
        return mx + x * s, my + y * s
    pts = [P(-0.150, 0.052), P(-0.128, -0.022), P(-0.060, -0.045), P(0.0, -0.030), P(0.060, -0.045), P(0.128, -0.022),
           P(0.150, 0.052), P(0.085, 0.022), P(0.0, 0.030), P(-0.085, 0.022)]
    d = ("M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f "
         "Q%.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
         % (pts[0] + P(-0.150, -0.030) + pts[2] + P(-0.020, -0.052) + pts[3] + P(0.020, -0.052) + pts[4] + P(0.150, -0.030) + pts[6]
            + P(0.100, 0.000) + pts[8] + P(-0.100, 0.000) + pts[0]))
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="0.008" stroke-linejoin="round"/>' % (d, k.ink, k.ink)


# name -> recipe.  brows: None | ("neutral",) | ("both"|"one", height above eye, angle, thickness or None, length, inset)
EXPRESSIONS = {
    "neutral":     dict(eyes="half", brows=("neutral",), mouth="default"),
    "unimpressed": dict(eyes="half", brows=("one", 0.136, 0.0, 0.037, 0.165, 0.0), mouth="frown"),
    "smirk":       dict(eyes="half", gaze=0.02, brows=None, mouth="smirk"),
    "determined":  dict(eyes="half", brows=("both", 0.120, 15.0, None, 0.17, 0.010), mouth="frown", mouth_dy=-0.01),
    "angry":       dict(eyes="half", tilt=10.0, brows=("both", 0.100, 24.0, 0.052, 0.19, 0.015), mouth="frown", mouth_dy=-0.02),
    "furious":     dict(eyes="half", tilt=10.0, brows=("both", 0.100, 24.0, 0.052, 0.19, 0.015), mouth="clench", mouth_dy=0.01),
    "smug":        dict(eyes="half", brows=("one", 0.140, -7.0, 0.048, 0.165, 0.010), mouth="flat"),
    "talking":     dict(eyes="half", brows=("one", 0.140, -7.0, 0.048, 0.165, 0.010), mouth="talk_b", mouth_dy=0.01),
    "shocked":     dict(eyes="ring", pupil=0.0165, brows=None, mouth="o", mouth_dy=0.02),
    "stunned":     dict(eyes="ring", pupil=0.030, brows=("one", 0.185, -8.0, 0.036, 0.16, 0.0), mouth="dash"),
    "excited":     dict(eyes="ring", pupil=0.030, brows=None, mouth="grin"),
    "happy":       dict(eyes="happy", brows=("both", 0.200, -7.0, 0.038, 0.165, 0.0), mouth="smile", mouth_dy=-0.01),
    "laughing":    dict(eyes="happy", brows=("both", 0.205, -10.0, 0.034, 0.15, 0.0), mouth="grin", mouth_dy=0.01, grin_w=0.43),
    "worried":     dict(eyes="half", brows=("both", 0.135, -9.0, 0.040, 0.165, 0.0), mouth="wavy", mouth_dy=0.01),
    "asleep":      dict(eyes="closed", eye_dy=0.02, brows=("both", 0.105, 0.0, 0.036, 0.15, 0.0), mouth="dash", mouth_ang=20.0),
    "shouting":    dict(eyes="squeeze", brows=None, mouth="clench", mouth_dy=0.01),
    "grinning":    dict(eyes="dot", brows=("both", 0.145, -10.0, 0.034, 0.16, 0.0), mouth="grin", grin_w=0.43),
    "wink":        dict(eyes="wink", brows=("one", 0.235, -8.0, 0.050, 0.20, 0.010), mouth="smirk"),
    "sad":         dict(eyes="half", brows=("both", 0.165, -28.0, 0.037, 0.17, 0.0), mouth="wavy", mouth_dy=0.01),
    "blink":       dict(eyes="closed", brows=("neutral",), mouth="default"),
}
MOUTHS = ("default", "none", "dash", "frown", "smirk", "smile", "grin", "flat", "talk_a", "talk_b", "talk_o", "o", "clench", "wavy")


def _face_layout(C, yaw, pitch):
    """face spec 3.2: features slide with yaw, spacing squeezes, the far (leading) eye shrinks."""
    a = abs(yaw)
    shift = 0.12 * yaw
    half = (0.26 - 0.075 * a) / 2
    far = 1 - 0.14 * a
    sL, sR = (far, 1.0) if yaw < 0 else (1.0, far)
    ey = C["eye_y"] + 0.07 * pitch
    return shift - half, shift + half, ey, sL, sR, shift, ey + 0.185


def _face(k, C, P, white):
    """returns (svg of eyes+brows+mouth, layout dict).  Never tweens eye shapes: expr is a discrete drawing."""
    yaw, pitch = P["yaw"], P["pitch"]
    xL, xR, ey, sL, sR, mx, my = _face_layout(C, yaw, pitch)
    E = EXPRESSIONS.get(P["expr"]) or EXPRESSIONS["neutral"]
    blink = P["blink"]
    gx, gy = P["gaze"]
    gxx = _clamp(gx, -1.0, 1.0) * 0.03 + E.get("gaze", 0.0)
    gyy = _clamp(gy, -1.0, 1.0) * 0.03
    # weight of the single brow / near eye: right eye for yaw <= 0.05, left eye for yaw >= 0.25 (cross-fades in between)
    wl = _smooth(0.05, 0.25, yaw)
    wr = 1.0 - wl
    o = []
    eyes = E["eyes"]
    eyy = ey + E.get("eye_dy", 0.0)
    tilt = E.get("tilt", 0.0)
    for (cx, s, side) in ((xL, sL, -1), (xR, sR, 1)):
        kind = eyes
        if kind == "wink":      # far (leading) eye is the happy arc, near eye stays half-lid
            near_is_right = wr >= 0.5
            kind = "half" if ((side == 1) == near_is_right) else "happy"
        if blink >= 2 and kind in ("half", "ring", "dot"):
            kind = "closed"
        if kind == "half":
            o.append(_eye_half(k, cx, eyy, gxx, s, -side * tilt, 0.45 if blink == 1 else 1.0))
        elif kind == "ring":
            if blink == 1:
                o.append(_eye_lens(k, cx, eyy, s, white))
            else:
                o.append(_eye_ring(k, cx, eyy, s, E.get("pupil", 0.03), gxx, gyy, white))
        elif kind == "happy":
            o.append(_eye_happy(k, cx, eyy, s))
        elif kind == "closed":
            o.append(_eye_closed(k, cx, eyy, s))
        elif kind == "dot":
            o.append(_eye_dot(k, cx, eyy, s, 0.45 if blink == 1 else 1.0))
        elif kind == "squeeze":
            o.append(_eye_squeeze(k, cx, eyy, side, s))
    br = E.get("brows")
    if br:
        if br[0] == "neutral":
            if C["brow"] == "dome":
                o.append(_brow_dome(k, xL - 0.005, ey - 0.125, sL))
                o.append(_brow_dome(k, xR - 0.005, ey - 0.125, sR))
            else:
                o.append(_brow_stroke(k, xL, ey - 0.130, -1, 3.0, 0.165, C["brow_th"], sL))
                o.append(_brow_stroke(k, xR, ey - 0.130, 1, 3.0, 0.165, C["brow_th"], sR))
        else:
            mode, hgt, ang, th, ln, inset = br
            th = th if th else C["brow_th"]
            if mode == "both":
                o.append(_brow_stroke(k, xL + inset, ey - hgt, -1, ang, ln, th, sL))
                o.append(_brow_stroke(k, xR - inset, ey - hgt, 1, ang, ln, th, sR))
            else:
                o.append(_brow_stroke(k, xL + inset, ey - hgt, -1, ang, ln, th, sL * wl))
                o.append(_brow_stroke(k, xR - inset, ey - hgt, 1, ang, ln, th, sR * wr))
    # mouth (a moustache pushes the mouth down and sits where the upper lip would be)
    m = P["mouth"] if P["mouth"] is not None else E["mouth"]
    mdy = E.get("mouth_dy", 0.0) if P["mouth"] is None else 0.0
    if C.get("moustache"):
        o.append(_moustache(k, mx, my - 0.032))
        my2 = my + 0.058
    else:
        my2 = my
    myy = my2 + mdy
    if isinstance(m, (tuple, list)):          # ("open", width, height): free lip-sync shape
        o.append(_mouth_open(k, mx, myy + 0.01, _clamp(_num(m[1], 0.2), 0.05, 0.34), _clamp(_num(m[2], 0.1), 0.03, 0.20)))
    else:
        if m == "default":
            m = C["mouth"]
        if m == "dash":
            o.append(_mouth_dash(k, mx, myy, E.get("mouth_ang", 0.0) if P["mouth"] is None else 0.0))
        elif m == "frown":
            o.append(_mouth_frown(k, mx, myy))
        elif m == "smirk":
            o.append(_mouth_smirk(k, mx, myy, C.get("smirk_side", 1)))
        elif m == "smile":
            o.append(_mouth_smile(k, mx, myy))
        elif m == "grin":
            o.append(_mouth_grin(k, mx, myy, E.get("grin_w", 0.42)))
        elif m == "flat":
            o.append(_mouth_flat(k, mx, myy))
        elif m == "talk_a":
            o.append(_mouth_open(k, mx, myy + 0.01, 0.28, 0.085))
        elif m == "talk_b":
            o.append(_mouth_open(k, mx, myy + 0.01, 0.285, 0.17))
        elif m == "talk_o":
            o.append(_mouth_open(k, mx, myy + 0.01, 0.18, 0.13))
        elif m == "o":
            o.append(_mouth_o(k, mx, myy))
        elif m == "clench":
            o.append(_mouth_clench(k, mx, myy))
        elif m == "wavy":
            o.append(_mouth_wavy(k, mx, myy))
    return "".join(o), dict(xL=xL, xR=xR, ey=ey, sL=sL, sR=sR, mx=mx, my=my2, wl=wl, wr=wr)


# ----------------------------------------------------------------------------- hats (head frame, drawn OVER the head)
def _hat_newsboy(k, C, yaw):
    """hero: flat 8-panel newsboy cap (own design).  Puffy dome 0.90 D wide over the top third of the head (y -0.56 .. -0.24),
    stiff visor down to y = -0.15 that slides to the facing side and pokes past the head contour at |yaw| = 1."""
    col = C["hat_colors"]
    a = abs(yaw)
    dx = -0.02 * yaw                    # dome drifts to the back of the head
    bx = dx - 0.10 * yaw                # top button
    vx = 0.30 * yaw                     # visor centre
    hv = 0.375 - 0.085 * a
    xl, xr, yb, top = -0.432 + dx, 0.432 + dx, -0.272, -0.558
    tx = dx + (bx - dx) * 0.5
    qx, qy = vx * 0.55, -0.228
    dome = ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z"
            % (xl, yb, xl - 0.078, yb - 0.125, tx - 0.37, top, tx, top, tx + 0.37, top, xr + 0.078, yb - 0.125, xr, yb, qx, qy, xl, yb))
    u = k.uid
    k.defs.append('<linearGradient id="%s_ht" gradientUnits="userSpaceOnUse" x1="-0.45" y1="0" x2="0.45" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.38" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  '<clipPath id="%s_hd"><path d="%s"/></clipPath>' % (u, k.c(col["light"]), k.c(col["base"]), k.c(col["dark"]), u, dome))
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    # visor (its top is tucked under the dome's front edge)
    vy0 = -0.268
    vr = 'transform="rotate(%.3f %.4f -0.24)"' % (10.0 * yaw, vx)
    o.append('<path %s d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f C%.4f,-0.104 %.4f,-0.104 %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (vr, vx - hv, vy0, vx, vy0 + 0.045, vx + hv, vy0, vx + hv * 0.82, vx - hv * 0.82, vx - hv, vy0, k.c(col["visor"]), k.ink))
    o.append('<path %s d="M%.4f,-0.180 Q%.4f,-0.143 %.4f,-0.180" fill="none" stroke="%s" stroke-width="0.009" stroke-linecap="round" opacity="0.8"/>'
             % (vr, vx - hv * 0.50, vx, vx + hv * 0.50, k.c(col["check"])))
    # dark band where the dome snaps onto the visor
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.046" stroke-linecap="round"/>'
             % (xl + 0.045, yb + 0.012, qx, qy + 0.028, xr - 0.045, yb + 0.012, k.c(col["band"])))
    # dome
    o.append('<path d="%s" fill="url(#%s_ht)"/>' % (dome, u))
    o.append('<g clip-path="url(#%s_hd)">' % u)
    by = top + 0.022
    # windowpane check: two latitude lines, then the panel seams fanning from the button
    for f in (0.40, 0.72):
        yy = top + (yb - top) * f
        o.append('<path d="M-0.6,%.4f Q%.4f,%.4f 0.6,%.4f" fill="none" stroke="%s" stroke-width="0.011" opacity="0.75"/>'
                 % (yy - 0.05, qx, yy + 0.085, yy - 0.05, k.c(col["check"])))
    for ui in (-0.84, -0.60, -0.36, -0.12, 0.12, 0.36, 0.60, 0.84):
        uu = ui + 0.30 * yaw * (1 - ui * ui)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010" opacity="0.75"/>'
                 % (bx, by, dx + 0.53 * uu, by + 0.02, dx + 0.50 * uu, yb + 0.07, k.c(col["check"])))
    for ui in (-0.72, -0.36, 0.0, 0.36, 0.72):
        uu = ui + 0.30 * yaw * (1 - ui * ui)
        o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round"/>'
                 % (bx, by, dx + 0.53 * uu, by + 0.02, dx + 0.50 * uu, yb + 0.07, k.c(col["seam"])))
    o.append('</g>')
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (dome, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.036" ry="0.017" fill="%s" stroke="%s" stroke-width="0.012"/>' % (bx, top + 0.006, k.c(col["light"]), k.ink))
    o.append('</g>')
    t = C["hat_tilt"]
    for p in ((-0.50, -0.40), (0.50, -0.40), (0.0, -0.61), (vx - hv - 0.02, -0.25), (vx + hv + 0.02, -0.25)):
        k.ext.append(_rot(p[0], p[1], t) + (0.02,))
    return "".join(o), (bx, top - 0.01)


def _hat_homburg(k, C, yaw):
    """boss: felt homburg (own design): round crown with a shallow centre crease, ribbon band with a flat bow,
    curled brim 1.12 D wide whose front dips to the brows (y = -0.26).  Crown 0.84 D wide, top at y = -0.69."""
    col = C["hat_colors"]
    dxc = -0.03 * yaw
    cdx = -0.10 * yaw + dxc
    fdx = 0.22 * yaw
    bxw = -0.27 + 0.10 * yaw
    u = k.uid
    crown = ("M%.4f,-0.36 C%.4f,-0.49 %.4f,-0.656 %.4f,-0.680 Q%.4f,-0.694 %.4f,-0.668 Q%.4f,-0.694 %.4f,-0.680 C%.4f,-0.656 %.4f,-0.49 %.4f,-0.36 Z"
             % (-0.415 + dxc, -0.442 + dxc, -0.425 + dxc, -0.27 + dxc, (cdx - 0.27 + dxc) / 2, cdx,
                (cdx + 0.27 + dxc) / 2, 0.27 + dxc, 0.425 + dxc, 0.442 + dxc, 0.415 + dxc))
    k.defs.append('<linearGradient id="%s_ht" gradientUnits="userSpaceOnUse" x1="-0.44" y1="0" x2="0.44" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.30" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (u, k.c(col["light"]), k.c(col["base"]), k.c(col["dark"])))
    o = ['<g transform="rotate(%.3f)">' % C["hat_tilt"]]
    o.append('<path d="%s" fill="url(#%s_ht)"/>' % (crown, u))
    # crease shadow under the dent, painted highlight streak on the upper left (never moves with the scene light)
    o.append('<path d="M%.4f,-0.660 Q%.4f,-0.615 %.4f,-0.565" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.75"/>'
             % (cdx, cdx + 0.010, cdx - 0.004, k.c(col["dark"])))
    o.append('<path d="M%.4f,-0.530 Q%.4f,-0.632 %.4f,-0.652" fill="none" stroke="%s" stroke-width="0.024" stroke-linecap="round" opacity="0.85"/>'
             % (-0.345 + dxc, -0.300 + dxc, -0.165 + dxc, k.c(col["shine"])))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (crown, k.ink))
    fc = C["colors"].get("feather")
    if fc:
        # feather tucked into the band beside the bow, leaning back over the crown (drawn after the crown outline and before the band, so its quill is hidden and its tip may poke past the crown)
        fx0, fy0 = bxw + 0.004, -0.455
        o.append('<g transform="translate(%.4f %.4f) rotate(-24)"><path d="M0,0 Q-0.046,-0.085 -0.006,-0.178 Q0.040,-0.090 0,0 Z" fill="%s" stroke="%s" '
                 'stroke-width="0.011" stroke-linejoin="round"/><path d="M0,-0.012 L-0.004,-0.150" fill="none" stroke="%s" stroke-width="0.008" stroke-linecap="round"/></g>'
                 % (fx0, fy0, k.c(fc), k.ink, k.c(C["colors"].get("feather_dark", fc))))
    # ribbon band + flat bow
    o.append('<path d="M%.4f,-0.482 Q%.4f,-0.455 %.4f,-0.482 L%.4f,-0.36 L%.4f,-0.36 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>'
             % (-0.440 + dxc, dxc, 0.440 + dxc, 0.424 + dxc, -0.424 + dxc, k.c(col["band"]), k.ink))
    o.append('<path d="M%.4f,-0.462 Q%.4f,-0.437 %.4f,-0.462" fill="none" stroke="%s" stroke-width="0.008" opacity="0.55"/>'
             % (-0.40 + dxc, dxc, 0.40 + dxc, k.c(col["edge"])))
    o.append('<path d="M%.4f,-0.474 L%.4f,-0.464 L%.4f,-0.372 L%.4f,-0.368 Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>'
             '<path d="M%.4f,-0.470 L%.4f,-0.370 M%.4f,-0.467 L%.4f,-0.371" fill="none" stroke="%s" stroke-width="0.010"/>'
             % (bxw - 0.058, bxw + 0.048, bxw + 0.046, bxw - 0.060, k.c(col["bow"]), k.ink,
                bxw - 0.020, bxw - 0.022, bxw + 0.008, bxw + 0.006, k.ink))
    # brim: tips curl up, front dips to the brows (y = -0.26)
    o.append('<path d="M-0.56,-0.388 Q-0.580,-0.325 -0.40,-0.31 Q%.4f,-0.215 0.40,-0.31 Q0.580,-0.325 0.56,-0.388 Q0.30,-0.343 %.4f,-0.350 Q-0.30,-0.343 -0.56,-0.388 Z" '
             'fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (fdx, fdx * 0.3, k.c(col["brim"]), k.ink))
    o.append('<path d="M-0.42,-0.336 Q%.4f,-0.266 0.39,-0.336" fill="none" stroke="%s" stroke-width="0.013" stroke-linecap="round" opacity="0.9"/>'
             % (fdx, k.c(col["edge"])))
    o.append('</g>')
    t = C["hat_tilt"]
    for p in ((-0.60, -0.36), (0.60, -0.36), (-0.3, -0.71), (0.3, -0.71)):
        k.ext.append(_rot(p[0], p[1], t) + (0.02,))
    return "".join(o), (cdx, -0.685)


def _ear_pencil(k, C, yaw):
    """hero detail: a yellow pencil tucked behind the (screen-right) ear, under the cap edge.  Fades as the head turns right."""
    vis = 1.0 - _smooth(0.15, 0.6, yaw)
    back = _clamp(-yaw, 0.0, 1.0)
    cx = _lerp(0.455, 0.30, back)
    cy = _lerp(-0.222, -0.232, back)
    ang = _lerp(-24.0, 8.0, back)
    L = _lerp(0.22, 0.36, back) * vis
    w = 0.030 * vis
    h = L / 2
    col = C["colors"]
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f)">' % (cx, cy, ang)]
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
             % (-h, -w / 2, h * 0.72, -w / 2, h * 0.72, w / 2, -h, w / 2, k.c(col["pencil"]), k.ink, 0.011 * vis))
    o.append('<path d="M%.4f,%.4f L%.4f,0 L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
             % (h * 0.72, -w / 2, h, h * 0.72, w / 2, k.c("#ecd2a8"), k.ink, 0.011 * vis))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
             % (-h, -w / 2, -h * 0.72, -w / 2, -h * 0.72, w / 2, -h, w / 2, k.c("#e58f98"), k.ink, 0.011 * vis))
    o.append('</g>')
    ex, ey = _rot(h, 0.0, ang)
    k.ext.append((cx + ex, cy + ey, 0.02))
    return "".join(o)


def _hair(k, C, yaw):
    """flat hair patches inside the head contour (clipped by the caller), no ink on the inner edge.
    front: one crescent per temple; turning: the far-side patch grows to a quarter..third of the head, the near one vanishes."""
    H = C["hair"]
    seed = C["seed"]
    col = k.c(H["color"])
    o = []
    R = 0.475
    for s in (-1, 1):
        sy = s * yaw
        w = H["front"] * (1 - _smooth(0.0, 0.6, sy)) + H["grow"] * max(0.0, -sy)
        yb = 0.10 + 0.11 * _clamp(-sy, 0.0, 1.0)
        rag = 0.003 + 0.05 * w
        pts = []
        y0 = -0.42
        for j in range(7):
            y = _lerp(y0, yb - 0.04, j / 6.0)
            f = _lerp(1.12, 0.92, j / 6.0)
            xe = math.sqrt(max(R * R - y * y, 0.0))
            x = xe - w * f + rag * math.sin(j * 2.4 + seed * 1.3 + s)
            pts.append((s * x, y))
        xe = math.sqrt(max(R * R - yb * yb, 0.0))
        pts.append((s * (xe - w * 0.66), yb - 0.012))
        pts.append((s * (xe - w * 0.28), yb + 0.002))
        pts.append((s * (xe + 0.04), yb + 0.012))
        d = _smooth_open(pts) + "L%.4f,%.4f L%.4f,%.4f Z" % (s * 0.60, yb, s * 0.60, y0)
        o.append('<path d="%s" fill="%s"/>' % (d, col))
    return "".join(o)


# ----------------------------------------------------------------------------- effects
def _fx_sweat(k, x, y, s=1.0, rot=0.0):
    """teardrop .075 x .115, slate outline (NOT ink), lighter left half."""
    w, h = 0.075 * s, 0.115 * s
    return ('<g transform="translate(%.4f %.4f) rotate(%.2f)"><path d="M0,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f A%.4f,%.4f 0 0 1 %.4f,%.4f C%.4f,%.4f %.4f,%.4f 0,%.4f Z" '
            'fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
            '<path d="M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f Z" fill="%s"/></g>'
            % (x, y, rot, -h / 2, w * 0.15, -h * 0.2, w / 2, h * 0.05, w / 2, h * 0.22, w / 2, w / 2, -w / 2, h * 0.22,
               -w / 2, h * 0.05, -w * 0.15, -h * 0.2, -h / 2, k.c(SWEAT[0]), k.c(SWEAT[2]), 0.014 * s,
               -w * 0.05, -h * 0.18, -w * 0.42, h * 0.05, -w * 0.40, h * 0.35, -w * 0.10, h * 0.40, k.c(SWEAT[1])))


_PUFF = ((-0.075, 0.02, 0.055), (-0.025, -0.03, 0.065), (0.045, -0.02, 0.06), (0.08, 0.03, 0.045), (0.0, 0.04, 0.06))


def _fx_puff(k, x, y, s, op):
    out = "".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x + a * s, y + b * s, (r + 0.014) * s, k.ink) for a, b, r in _PUFF)
    inn = "".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (x + a * s, y + b * s, r * s, k.c("#fffeff")) for a, b, r in _PUFF)
    return '<g opacity="%.3f">%s%s</g>' % (op, out, inn)


_STEAM_L = ((-0.30, -0.02), (-0.36, -0.11), (-0.49, -0.24), (-0.57, -0.42), (-0.62, -0.58))
_STEAM_R = ((0.48, -0.05), (0.56, -0.14), (0.67, -0.29), (0.75, -0.50), (0.80, -0.66))


def _fx_steam(k, t):
    """three puffs per side pumping up and out from hat-brim height; t in 0..1 loops seamlessly."""
    t = t % 1.0
    o = []
    for path in (_STEAM_L, _STEAM_R):
        for j in (2, 1, 0):
            q = (j + t) / 3.0                       # 0..1 along the path
            f = q * 4.0
            i = min(int(f), 3)
            ff = f - i
            x = _lerp(path[i][0], path[i + 1][0], ff)
            y = _lerp(path[i][1], path[i + 1][1], ff)
            s = 0.25 + 0.80 * _smooth(0.0, 0.30, q) + 0.10 * q
            op = _smooth(0.0, 0.06, q) * (1.0 - _smooth(0.62, 1.0, q))
            o.append(_fx_puff(k, x, y, s, op))
            k.ext.append((x, y, 0.16 * s))
    return "".join(o)


def _fx_blush(k, L):
    u = k.uid
    k.defs.append('<radialGradient id="%s_bl"><stop offset="0" stop-color="%s" stop-opacity="1"/><stop offset="0.55" stop-color="%s" stop-opacity="0.85"/>'
                  '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (u, k.c("#f6c9d8"), k.c("#f8d7e1"), k.c("#f8d7e1")))
    return ('<ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.045" fill="url(#%s_bl)"/><ellipse cx="%.4f" cy="%.4f" rx="0.075" ry="0.045" fill="url(#%s_bl)"/>'
            % (L["xL"] - 0.03, L["ey"] + 0.085, u, L["xR"] + 0.03, L["ey"] + 0.085, u))


def _fx_tear(k, x, y, rot, s, op):
    return ('<g transform="translate(%.4f %.4f) rotate(%.2f)" opacity="%.3f"><ellipse cx="0" cy="0" rx="%.4f" ry="%.4f" fill="%s" stroke="%s" stroke-width="%.4f"/>'
            '<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="%s"/></g>'
            % (x, y, rot, op, 0.055 * s, 0.030 * s, k.c("#b8e4dc"), k.c("#383f36"), 0.012 * s, -0.014 * s, -0.008 * s, 0.022 * s, 0.009 * s, k.c("#e9ffff")))


def _fx_tears(k, L, t):
    """laugh tears: chains flying sideways out of the outer eye corners; t in 0..1 loops."""
    t = t % 1.0
    o = []
    for side, x0 in ((-1, L["xL"]), (1, L["xR"])):
        for j in range(3):
            q = (j + t) / 3.0
            d = 0.115 + 0.36 * q
            y = L["ey"] - 0.02 + side * 0.0 + 0.16 * q * q * (1 if side > 0 else 0.3)
            o.append(_fx_tear(k, x0 + side * d, y, side * (10 + 60 * q * q) - (0 if side > 0 else 0), 1.0 - 0.40 * q,
                              _smooth(0.0, 0.08, q) * (1.0 - _smooth(0.7, 1.0, q))))
    return "".join(o)


_ZPTS = ((0.15, 0), (1.0, 0), (0.95, 0.24), (0.45, 0.76), (0.90, 0.76), (0.85, 1.0), (0.0, 1.0), (0.05, 0.76), (0.55, 0.24), (0.10, 0.24))


def _fx_zzz(k, t):
    """sleep Z: three at once rising 0.33 D apart with a +/-0.1 zig-zag; t in 0..1 = one spawn period (0.65 s)."""
    t = t % 1.0
    o = []
    for j in range(3):
        q = (j + t) / 3.0
        y = -(0.70 + 1.0 * q)
        x = 0.12 + 0.10 * math.sin(q * 3 * math.pi)
        size = 0.095 + 0.045 * q
        op = _smooth(0.0, 0.25, q) * 0.6 + 0.4 * _smooth(0.0, 0.45, q)
        op *= 1.0 - _smooth(0.75, 1.0, q)
        d = " ".join("%.4f,%.4f" % ((px - 0.5) * size * 0.92, (py - 0.5) * size) for px, py in _ZPTS)
        o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" paint-order="stroke" '
                 'transform="translate(%.4f %.4f) rotate(-10)" opacity="%.3f"/>' % (d, k.c("#dbd1fa"), "#221a3f", size * 0.26, x, y, op))
        k.ext.append((x, y, size))
    return "".join(o)


def _fx_focus(seed, n=30, r0=0.85, r1=2.7):
    """thin white radial streaks converging on the head centre; pass a new integer seed every frame (they are redrawn each frame)."""
    s = (int(seed) * 2654435761 + 12345) & 0xFFFFFFFF
    o = []
    for i in range(n):
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        a = (i + (s >> 8 & 0xFFFF) / 65535.0 * 0.9) * 2 * math.pi / n
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        ra = r0 + (s >> 8 & 0xFFFF) / 65535.0 * 0.55
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        rb = ra + 0.5 + (s >> 8 & 0xFFFF) / 65535.0 * (r1 - r0 - 0.9)
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        wd = 0.006 + (s >> 8 & 0xFFFF) / 65535.0 * 0.010
        c, sn = math.cos(a), math.sin(a)
        o.append("M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Z" % (ra * c, ra * sn, rb * c - sn * wd, rb * sn + c * wd, rb * c + sn * wd, rb * sn - c * wd))
    return '<path d="%s" fill="#ffffff" opacity="0.72"/>' % "".join(o)


FX_TYPES = ("sweat", "anger_fill", "steam", "blush", "focus_lines", "tears", "zzz")


# ----------------------------------------------------------------------------- torso
PROFILE_STOUT = ((0.50, 0.02), (0.82, 0.10), (0.93, 0.25), (0.98, 0.38), (1.00, 0.58), (0.98, 0.77), (0.93, 0.84), (0.72, 0.95), (0.40, 0.995))
PROFILE_SLIM = ((0.60, 0.02), (0.90, 0.10), (0.97, 0.25), (1.00, 0.50), (1.00, 0.70), (0.96, 0.85), (0.75, 0.96), (0.40, 1.00))
TORSO_TOP = 0.36
BOWL_H = 0.14


@lru_cache(maxsize=16)
def _torso_geom(w, h, profile, seed):
    """closed Catmull-Rom through the measured profile, sampled; returns tuples (x, y, nx, ny, line width, wob_out, wob_in).
    The profile is the OUTER silhouette (measured widths); the fill is inset by a contour that is thin on the left (0.023)
    and thick on the right (0.043), like the head.  Low-frequency wobble is baked in per character."""
    hw = w / 2.0
    right = [(hw * fx, TORSO_TOP + h * fy) for fx, fy in profile]
    left = [(-x, y) for x, y in reversed(right)]
    ctrl = [(0.0, TORSO_TOP)] + right + [(0.0, TORSO_TOP + h)] + left
    n = len(ctrl)
    sub = 6
    P = []
    for i in range(n):
        p0, p1, p2, p3 = ctrl[i - 1], ctrl[i], ctrl[(i + 1) % n], ctrl[(i + 2) % n]
        for j in range(sub):
            t = j / float(sub)
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            P.append((x, y))
    N = len(P)
    out = []
    for i in range(N):
        a, b = P[i - 1], P[(i + 1) % N]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty) or 1.0
        nx, ny = ty / L, -tx / L                    # clockwise traversal (y down) -> outward normal
        th = 2 * math.pi * i / N
        lw = 0.034 + 0.009 * nx + 0.004 * ny      # left 0.025, right 0.043 (reference 0.02-0.047; close shots about 0.03 on the left)
        wo = 0.0050 * _wob(th, seed + 1.0) + 0.0010 * _rough(th, seed + 2.0)
        wi = 0.0030 * _wob(th, seed + 3.1) + 0.0008 * _rough(th, seed + 0.4)
        out.append((P[i][0], P[i][1], nx, ny, lw, wo, wi))
    return tuple(out)


class _TorsoMap(object):
    """front-view costume x -> drawn x: the torso narrows with |yaw| and its centre line slides to the facing edge
    (anatomy 3.3: 0.10-0.15 D at three-quarter, 0.06 D inside the facing edge at near-profile)."""
    __slots__ = ("hw", "hwa", "c", "nf")

    def __init__(self, C, yaw):
        a = abs(yaw)
        self.nf = 1.0 - 0.15 * min(a, 1.2)
        self.hw = C["torso_w"] / 2.0
        self.hwa = self.hw * self.nf
        sg = 1.0 if yaw >= 0 else -1.0
        self.c = sg * (self.hwa - 0.075) * (min(a, 1.0) ** C["shift_pow"])

    def x(self, xf, y=1.0):
        """the centre line slides fully at the belly (y >= 0.95) and only 45 percent at the collar (y <= 0.42)."""
        c = self.c * (0.45 + 0.55 * _smooth(0.42, 0.95, y))
        uu = xf / self.hw
        if uu >= 0:
            return c + uu * (self.hwa - c)
        return c + uu * (self.hwa + c)


def _poly(k, pts, fill, sw=0.012, stroke=None):
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round"/>'
            % (_poly_d(pts), fill, stroke or k.ink, sw))


def _costume_vest(k, C, m):
    """hero: cobalt sweater vest with ribbed V-neck and hem, argyle row, cream shirt collar, ochre tie."""
    def X(x, y):
        return (m.x(x, y), y)
    col = C["colors"]
    yB = TORSO_TOP + C["torso_h"]
    yb = yB - BOWL_H
    o = []
    vt, vb, vw = 0.43, 0.715, 0.118
    # ribbing line outside the V
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
             % (X(-vw - 0.034, vt) + X(0, vb + 0.062) + X(vw + 0.034, vt) + (k.c(col["dark"]),)))
    # argyle row
    for cx in (-0.150, 0.0, 0.150):
        o.append('<path d="%s" fill="%s"/>' % (_poly_d([X(cx - 0.075, 0.905), X(cx, 0.800), X(cx + 0.075, 0.905), X(cx, 1.010)]), k.c(col["argyle"])))
    dd = "".join("M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" % (X(cx - 0.075, 0.800) + X(cx + 0.075, 1.010) + X(cx + 0.075, 0.800) + X(cx - 0.075, 1.010))
                 for cx in (-0.150, 0.0, 0.150))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" stroke-dasharray="0.022 0.016"/>' % (dd, k.c(col["stitch"])))
    # hem ribbing
    o.append('<path d="M-0.6,%.4f Q0,%.4f 0.6,%.4f L0.6,%.4f L-0.6,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014"/>'
             % (yb - 0.085, yb - 0.060, yb - 0.085, yb + 0.05, yb + 0.05, k.c(col["rib"]), k.ink))
    dd = "".join("M%.4f,%.4f L%.4f,%.4f" % (X(x, yb - 0.060) + X(x, yb + 0.02)) for x in (-0.24, -0.18, -0.12, -0.06, 0.0, 0.06, 0.12, 0.18, 0.24))
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.010" opacity="0.8"/>' % (dd, k.c(col["dark"])))
    # shirt V, tie, collar flaps, knot
    o.append(_poly(k, [X(-vw, vt), X(vw, vt), X(0, vb)], k.c(col["shirt"]), 0.016))
    o.append(_poly(k, [X(-0.022, 0.50), X(0.022, 0.50), X(0.031, 0.60), X(0.019, 0.66), X(0, 0.70), X(-0.019, 0.66), X(-0.031, 0.60)], k.c(col["tie"]), 0.013))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.009"/>'
             % (X(-0.028, 0.590) + X(0.028, 0.612) + X(-0.022, 0.635) + X(0.020, 0.655) + (k.c(col["tie_dark"]),)))
    for s in (-1, 1):
        o.append(_poly(k, [X(s * 0.124, 0.440), X(s * 0.012, 0.548), X(s * 0.078, 0.612)], k.c(col["shirt"]), 0.014))
    o.append(_poly(k, [X(-0.027, 0.505), X(0.027, 0.505), X(0.020, 0.552), X(-0.020, 0.552)], k.c(col["tie_dark"]), 0.011))
    # trouser bowl
    o.append('<path d="M-0.6,%.4f Q0,%.4f 0.6,%.4f L0.6,%.4f L-0.6,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022"/>'
             % (yb, yb + 0.03, yb, yB + 0.1, yB + 0.1, k.c(col["pants"]), k.ink))
    return "".join(o)


def _costume_waistcoat(k, C, m):
    """boss (own design): forest-green DOUBLE-BREASTED waistcoat with chalk pinstripes, dark shawl lapels, white shirt V,
    red bow tie, six brass buttons in two columns, white pocket square, straight hem.
    (Review: the first version repeated the reference boss's layout -- five buttons on the centre line, watch chain to a
    fob, three welt pockets, dot pattern, pointed hem -- in another colour.  None of those are used any more.)"""
    def X(x, y):
        return (m.x(x, y), y)
    col = C["colors"]
    yB = TORSO_TOP + C["torso_h"]
    yb = yB - BOWL_H
    u = k.uid
    k.defs.append('<pattern id="%s_pt" width="0.088" height="0.4" patternUnits="userSpaceOnUse" patternTransform="translate(%.4f 0)">'
                  '<rect x="0.040" y="0" width="0.010" height="0.4" fill="%s"/></pattern>' % (u, m.c, k.c(col["stripe"])))
    o = ['<rect x="-0.6" y="0.3" width="1.2" height="1.3" fill="url(#%s_pt)" opacity="0.5"/>' % u]
    vt, vb, vw = 0.44, 0.775, 0.130
    # double-breasted front edge: from the bottom of the V out to the screen-right hem
    o.append('<path d="M%.4f,%.4f Q%.4f,%.4f %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>'
             % (X(0.0, vb + 0.045) + X(0.245, vb + 0.10) + X(0.262, yb + 0.012) + (k.c(col["dark"]),)))
    # breast pocket (screen-left) with a white pocket square
    o.append(_poly(k, [X(-0.400, 0.705), X(-0.384, 0.628), X(-0.350, 0.672), X(-0.318, 0.618), X(-0.286, 0.705)], k.c(col["shirt"]), 0.013))
    o.append(_poly(k, [X(-0.418, 0.700), X(-0.268, 0.700), X(-0.268, 0.742), X(-0.418, 0.742)], k.c(col["dark"]), 0.014))
    # shawl lapels beside the shirt V
    for sg in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                 % (X(sg * vw, vt) + X(0.0, vb) + X(sg * 0.012, vb + 0.075) + X(sg * 0.225, 0.69) + X(sg * 0.238, vt - 0.01)
                    + (k.c(col["lapel"]), k.ink)))
    # shirt V with placket line
    o.append(_poly(k, [X(-vw, vt), X(vw, vt), X(0, vb)], k.c(col["shirt"]), 0.016))
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="0.010"/><circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>'
             % (X(0, 0.60) + X(0, vb - 0.03) + (k.c("#b3a49a"),) + X(0, 0.665) + (k.c("#b3a49a"),)))
    # bow tie
    for sg in (-1, 1):
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f Q%.4f,%.4f %.4f,%.4f Z" fill="%s" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>'
                 % (X(0, 0.560) + X(sg * 0.112, 0.508) + X(sg * 0.096, 0.560) + X(sg * 0.112, 0.612) + (k.c(col["tie"]), k.ink)))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.025" ry="0.031" fill="%s" stroke="%s" stroke-width="0.013"/>' % (X(0, 0.560) + (k.c(col["tie_dark"]), k.ink)))
    # six brass buttons, two columns of three
    for y in (0.915, 1.035, 1.155):
        for x in (-0.100, 0.100):
            o.append('<circle cx="%.4f" cy="%.4f" r="0.034" fill="%s" stroke="%s" stroke-width="0.015"/>' % (X(x, y) + (k.c(col["brass"]), k.ink)))
            o.append('<circle cx="%.4f" cy="%.4f" r="0.010" fill="%s"/>' % (m.x(x, y) - 0.009, y - 0.010, k.c(col["brass_l"])))
    # straight hem over the trouser bowl
    o.append('<path d="M-0.7,%.4f Q0,%.4f 0.7,%.4f L0.7,%.4f L-0.7,%.4f Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>'
             % (yb - 0.004, yb + 0.034, yb - 0.004, yB + 0.1, yB + 0.1, k.c(col["pants"]), k.ink))
    return "".join(o)


def _torso(k, C, m):
    """torso group in torso-local coordinates (caller applies lean / head offset)."""
    G = _torso_geom(C["torso_w"], C["torso_h"], C["profile"], C["seed"])
    nf = m.nf
    outer = _smooth_closed([(g[0] * nf + g[2] * g[5], g[1] + g[3] * g[5]) for g in G])
    inner = _smooth_closed([(g[0] * nf - g[2] * (g[4] + g[6]), g[1] - g[3] * (g[4] + g[6])) for g in G])
    u = k.uid
    base = C["colors"]["base"]
    hw = m.hwa
    k.defs.append('<linearGradient id="%s_tg" gradientUnits="userSpaceOnUse" x1="%.4f" y1="0" x2="%.4f" y2="0">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  '<clipPath id="%s_tc"><path d="%s"/></clipPath>'
                  % (u, -hw, hw, k.c(_shade(base, 1.12)), k.c(base), k.c(_shade(base, 0.72)), u, inner))
    cost = _costume_vest(k, C, m) if C["costume"] == "vest" else _costume_waistcoat(k, C, m)
    return ('<path d="%s" fill="%s"/><g clip-path="url(#%s_tc)"><rect x="-0.75" y="0.2" width="1.5" height="1.5" fill="url(#%s_tg)"/>%s</g>'
            % (outer, k.ink, u, u, cost))


# ----------------------------------------------------------------------------- limbs
def _bow(r):
    """elbow/knee offset factor for reach ratio r = d / L (rigid sqrt(1 - r^2), softened near full reach so the joint
    never snaps: bounded slope, reaches 0 exactly at r = 1)."""
    r0 = 0.90
    if r <= r0:
        return math.sqrt(max(1.0 - r * r, 0.0))
    if r >= 1.0:
        return 0.0
    g0 = math.sqrt(1.0 - r0 * r0)
    m0 = -r0 / g0 * (1.0 - r0)
    m1 = -2.5 * (1.0 - r0)
    t = (r - r0) / (1.0 - r0)
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * g0 + (t3 - 2 * t2 + t) * m0 + (t3 - t2) * m1


def _ik(S, Tg, L, chir):
    """two-bone IK with equal bones.  Returns (elbow, hand).  The hand is the target itself, clamped to the reach L
    (full reach = straight).  chir in -1..1 scales and signs the elbow offset (rubber hose: |chir| < 1 = shallower bend).
    Within 0.25 L of the joint root the hose retracts (the elbow offset fades to 0 with the reach), so hand AND elbow are
    continuous for every target, including one that travels straight through the shoulder or the hip.  The elbow stays on
    the same side of the root-to-hand line for a given sign of chir (the bend direction never flips)."""
    dx, dy = Tg[0] - S[0], Tg[1] - S[1]
    d = math.hypot(dx, dy)
    if d < 1e-9:
        ux, uy = 0.0, 1.0
    else:
        ux, uy = dx / d, dy / d
    dc = d if d < L else L
    h = 0.5 * L * _bow(dc / L) * chir * _smooth(0.0, 0.25 * L, dc)
    Hx, Hy = S[0] + ux * dc, S[1] + uy * dc
    Mx, My = S[0] + ux * dc * 0.5, S[1] + uy * dc * 0.5
    return (Mx + uy * h, My - ux * h), (Hx, Hy)


def _limb_ctrl(S, E, H, kk):
    """the two cubic segments S -> E -> H as 7 control points.  kk = 0: one smooth quadratic arc through E (rubber hose);
    kk = 1: sharp joint."""
    Mx, My = (S[0] + H[0]) / 2, (S[1] + H[1]) / 2
    Cx, Cy = 2 * E[0] - Mx, 2 * E[1] - My
    k1 = 1.0 - kk
    hx, hy = (H[0] - S[0]) * k1 / 6, (H[1] - S[1]) * k1 / 6
    return (S,
            (S[0] + (k1 * (Cx - S[0]) + kk * (E[0] - S[0])) / 3, S[1] + (k1 * (Cy - S[1]) + kk * (E[1] - S[1])) / 3),
            (E[0] - hx, E[1] - hy), E, (E[0] + hx, E[1] + hy),
            (H[0] + (k1 * (Cx - H[0]) + kk * (E[0] - H[0])) / 3, H[1] + (k1 * (Cy - H[1]) + kk * (E[1] - H[1])) / 3),
            H)


def _limb_d(S, E, H, kk):
    """path through S, E, H (see _limb_ctrl)."""
    c = _limb_ctrl(S, E, H, kk)
    return ("M%.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f C%.4f,%.4f %.4f,%.4f %.4f,%.4f"
            % (c[0] + c[1] + c[2] + c[3] + c[4] + c[5] + c[6]))


def _stroke(k, d, w=LW):
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>' % (d, k.ink, w)


_LIMB_T = (1.0 / 6, 2.0 / 6, 3.0 / 6, 4.0 / 6, 5.0 / 6, 1.0)


def _ink_limb(k, S, E, H, kk, w, seed, tail=None):
    """hand-inked rubber-hose limb.  The reference limbs are not constant-width vector strokes: their width breathes by
    about +/-10 percent along the limb and the edges waver slightly (boss legs 13-17 px at D = 191 px, A t16.0).
    Drawn as (1) a core stroke 0.86 w wide with round caps and joins (keeps sharp elbows and knees solid) and (2) a filled
    ribbon around the same centre line whose half-width is w / 2 * (1 + two slow sines of the position along the limb).
    The variation is a function of the position ALONG the limb and of a fixed per-limb seed only, so it travels with the
    limb and never boils; the joints themselves (S, E, H) are not displaced.  tail = end point of the foot stub after H."""
    c = _limb_ctrl(S, E, H, kk)
    pts = [c[0]]
    for a in (0, 3):
        p0, p1, p2, p3 = c[a], c[a + 1], c[a + 2], c[a + 3]
        for t in _LIMB_T:
            u = 1.0 - t
            b0, b1, b2, b3 = u * u * u, 3 * u * u * t, 3 * u * t * t, t * t * t
            pts.append((b0 * p0[0] + b1 * p1[0] + b2 * p2[0] + b3 * p3[0], b0 * p0[1] + b1 * p1[1] + b2 * p2[1] + b3 * p3[1]))
    core = _limb_d(S, E, H, kk)
    n = len(pts)
    cum = [0.0]
    for i in range(1, n):
        cum.append(cum[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    tot = cum[-1] or 1.0
    left, right = [], []
    hw0 = hw1 = w / 2
    for i in range(n):
        a, b = pts[i - 1] if i > 0 else pts[0], pts[i + 1] if i + 1 < n else pts[n - 1]
        tx, ty = b[0] - a[0], b[1] - a[1]
        tl = math.hypot(tx, ty)
        if tl < 1e-9:
            nx = ny = 0.0
        else:
            nx, ny = ty / tl, -tx / tl
        f = cum[i] / tot
        hw = 0.5 * w * (1.0 + 0.065 * math.sin(6.2832 * (1.15 * f) + seed) + 0.040 * math.sin(6.2832 * (2.7 * f) + 1.9 * seed))
        off = 0.06 * w * math.sin(6.2832 * (1.9 * f) + 0.7 * seed) * math.sin(3.1416 * f)      # sideways waver, zero at both ends
        px, py = pts[i][0] + nx * off, pts[i][1] + ny * off
        left.append((px + nx * hw, py + ny * hw))
        right.append((px - nx * hw, py - ny * hw))
        if i == 0:
            hw0 = hw
        hw1 = hw
    right.reverse()
    # ribbon outline: smooth left edge, round cap, smooth right edge back, round cap
    rs = _smooth_open(right)
    rs = rs[rs.index("C"):]
    d = _smooth_open(left) + "A%.4f,%.4f 0 0 1 %.4f,%.4f" % (hw1, hw1, right[0][0], right[0][1]) + rs + "A%.4f,%.4f 0 0 1 %.4f,%.4f Z" % (hw0, hw0, left[0][0], left[0][1])
    out = ('<path d="%s" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/><path d="%s" fill="%s"/>'
           % (core, k.ink, 0.86 * w, d, k.ink))
    if tail:
        # the foot stub is its own round-capped stroke, as wide as the ribbon is at the ankle: when the toe length passes
        # through zero (the figure turns) it shrinks into the ankle's round cap instead of flipping the ribbon's sides
        out += ('<path d="M%.4f,%.4f L%.4f,%.4f" fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round"/>'
                % (H[0], H[1], tail[0], tail[1], k.ink, 2 * hw1))
    return out


def _hand(k, H, dirv, shape, hr=HAND_R, fold=1.0):
    """ink ball (diameter 2 hr, 0.13 D at the default limb width) + one stroke for a pointing index, four short strokes
    for an open hand.  fold (0..1) shortens the fingers when the arm is retracted onto the shoulder."""
    o = []
    ux, uy = dirv
    g = hr / HAND_R
    if shape == "point":
        fl = 0.118 * g * fold
        o.append(_stroke(k, "M%.4f,%.4f L%.4f,%.4f" % (H[0], H[1], H[0] + ux * fl, H[1] + uy * fl), 0.036 * g))
        k.ext.append((H[0] + ux * fl, H[1] + uy * fl, 0.02))
    elif shape == "open":
        d = ""
        fl = 0.098 * g * fold
        for a in (-48.0, -17.0, 14.0, 45.0):
            vx, vy = _rot(ux, uy, a)
            d += "M%.4f,%.4f L%.4f,%.4f" % (H[0], H[1], H[0] + vx * fl, H[1] + vy * fl)
        o.append(_stroke(k, d, 0.028 * g))
        k.ext.append((H[0], H[1], 0.115 * g))
    o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s"/>' % (H[0], H[1], hr, k.ink))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="%.4f" ry="%.4f" fill="#b7a9b3" opacity="0.7" transform="rotate(-35 %.4f %.4f)"/>'
             % (H[0] - 0.34 * hr, H[1] - 0.40 * hr, 0.15 * hr, 0.095 * hr, H[0] - 0.34 * hr, H[1] - 0.40 * hr))
    k.ext.append((H[0], H[1], hr + 0.01))
    return "".join(o)


PROP_TYPES = ("pencil", "eraser", "pointer", "paper")
# distance from the gripping hand to the prop's working tip along the prop axis (D): pencil point, eraser face (under the hand),
# pointer tip, far edge of the paper
PROP_TIP = {"pencil": 0.36, "eraser": 0.0, "pointer": 1.17, "paper": 0.58}


def _prop(k, kind, H, ang, sc=1.0):
    """prop held in the hand at H; local +x is the pointing direction (ang degrees, SVG clockwise from +x).
    Returns (svg, tip point in figure coordinates)."""
    o = ['<g transform="translate(%.4f %.4f) rotate(%.3f) scale(%.4f)">' % (H[0], H[1], ang, sc)]
    ink = k.ink
    tip = PROP_TIP.get(kind, 0.0)
    if kind == "pencil":           # red map pencil, 0.46 long
        o.append('<path d="M-0.100,-0.019 L0.285,-0.019 L0.285,0.019 L-0.100,0.019 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#d5392f"), ink))
        o.append('<path d="M-0.02,-0.006 L0.27,-0.006" stroke="%s" stroke-width="0.007" fill="none" opacity="0.8"/>' % k.c("#f08a7c"))
        o.append('<path d="M0.285,-0.019 L0.360,0 L0.285,0.019 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#ecd2a8"), ink))
        o.append('<path d="M0.335,-0.0065 L0.360,0 L0.335,0.0065 Z" fill="%s" stroke="%s" stroke-width="0.006" stroke-linejoin="round"/>' % (k.c("#c8281f"), k.c("#c8281f")))
        o.append('<path d="M-0.100,-0.019 L-0.072,-0.019 L-0.072,0.019 L-0.100,0.019 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#cfcad8"), ink))
        ends = ((-0.10, 0.0), (0.36, 0.0))
    elif kind == "eraser":         # felt wall-map eraser seen from its wooden back, 0.35 x 0.18, long axis across the arm
        o.append('<rect x="-0.092" y="-0.175" width="0.184" height="0.350" rx="0.030" fill="%s" stroke="%s" stroke-width="0.016"/>' % (k.c("#4d4656"), ink))
        o.append('<rect x="-0.058" y="-0.162" width="0.138" height="0.324" rx="0.020" fill="%s" stroke="%s" stroke-width="0.011"/>' % (k.c("#cf9a5e"), ink))
        o.append('<path d="M-0.022,-0.125 L-0.022,0.125 M0.024,-0.125 L0.024,0.125" stroke="%s" stroke-width="0.007" fill="none" opacity="0.7"/>' % k.c("#9a6a38"))
        ends = ((-0.095, -0.18), (0.095, 0.18), (-0.095, 0.18), (0.095, -0.18))
    elif kind == "pointer":        # wooden map pointer, 1.25 long, brass ferrule and dark tip
        o.append('<path d="M-0.080,-0.016 L1.060,-0.011 L1.060,0.011 L-0.080,0.016 Z" fill="%s" stroke="%s" stroke-width="0.011" stroke-linejoin="round"/>' % (k.c("#c08a52"), ink))
        o.append('<path d="M1.060,-0.013 L1.170,-0.004 L1.170,0.004 L1.060,0.013 Z" fill="%s" stroke="%s" stroke-width="0.010" stroke-linejoin="round"/>' % (k.c("#4a3a40"), ink))
        o.append('<path d="M1.020,-0.015 L1.065,-0.014 L1.065,0.014 L1.020,0.015 Z" fill="%s" stroke="%s" stroke-width="0.009" stroke-linejoin="round"/>' % (k.c("#d9bd66"), ink))
        o.append('<circle cx="-0.090" cy="0" r="0.024" fill="%s" stroke="%s" stroke-width="0.010"/>' % (k.c("#d9bd66"), ink))
        ends = ((-0.11, 0.0), (1.17, 0.0))
    else:                          # paper: teletype sheet 0.60 long x 0.46 wide, held at the middle of the near edge
        o.append('<path d="M-0.030,-0.230 L0.580,-0.230 L0.580,0.165 L0.515,0.230 L-0.030,0.230 Z" fill="%s" stroke="%s" stroke-width="0.016" stroke-linejoin="round"/>' % (k.c("#fcf4e1"), ink))
        o.append('<path d="M0.580,0.165 L0.515,0.165 L0.515,0.230 Z" fill="%s" stroke="%s" stroke-width="0.012" stroke-linejoin="round"/>' % (k.c("#e2d6bd"), ink))
        d = "".join("M%.3f,-0.170 L%.3f,%.3f" % (x, x, e) for x, e in ((0.10, 0.17), (0.17, 0.10), (0.24, 0.17), (0.31, 0.02), (0.38, 0.17), (0.45, 0.12)))
        o.append('<path d="%s" stroke="%s" stroke-width="0.012" fill="none" stroke-linecap="round" opacity="0.85"/>' % (d, k.c("#8d8089")))
        ends = ((-0.03, -0.23), (0.58, -0.23), (0.58, 0.23), (-0.03, 0.23))
    o.append('</g>')
    for e in ends:
        x, y = _rot(e[0] * sc, e[1] * sc, ang)
        k.ext.append((H[0] + x, H[1] + y, 0.03))
    tx, ty = _rot(tip * sc, 0.0, ang)
    return "".join(o), (H[0] + tx, H[1] + ty)


# ----------------------------------------------------------------------------- cast
CAST = {
    # the youngest forecaster: slim pill, newsboy cap, cobalt sweater vest, ochre tie, pencil behind the ear
    "hero": dict(
        build="slim", seed=1.7,
        torso_w=0.57, torso_h=1.01, profile=PROFILE_SLIM, shift_pow=1.0,
        shoulder=(0.235, 0.54), arm=0.74, hip_x=0.22, leg=1.10, stance=0.10, wide=0.36, limb_w=0.054,
        eye_y=0.045, brow="dome", brow_th=0.038, mouth="dash", moustache=False, smirk_side=1,
        hat="newsboy", hat_tilt=-2.0, ear_pencil=True,
        # review: the first colourway (slate-blue cap with light lines, brown temple hair) made the head a near copy of the
        # reference hero (blue striped cap, brown hair).  Ochre tweed + auburn hair read as a different person at any size.
        hat_colors=dict(light="#f1cf7c", base="#dca63e", dark="#b27a26", visor="#c8932f", band="#5a3a22", check="#f7e3a6", seam="#8a5a22"),
        hair=dict(color="#a8492a", front=0.10, grow=0.24),
        costume="vest",
        colors=dict(base="#3b6fda", dark="#234a9c", rib="#2f5cc0", argyle="#8fb2f6", stitch="#f6ead0", shirt="#f4ede7",
                    tie="#e3a93a", tie_dark="#b47a22", pants="#4c4453", pencil="#d5392f"),
    ),
    # the chief forecaster: stout egg, felt homburg low on the brows, moustache, forest-green waistcoat, red bow tie, watch chain
    "boss": dict(
        build="stout", seed=4.2,
        torso_w=1.00, torso_h=1.06, profile=PROFILE_STOUT, shift_pow=1.25,
        shoulder=(0.37, 0.43), arm=0.74, hip_x=0.14, leg=1.45, stance=0.04, wide=0.22, limb_w=0.068,
        eye_y=-0.020, brow="stroke", brow_th=0.047, mouth="frown", moustache=True, smirk_side=-1,
        hat="homburg", hat_tilt=-4.0, ear_pencil=False,
        hat_colors=dict(light="#9c96aa", base="#6b6476", dark="#474151", shine="#dedaea", band="#2c2732", bow="#474150",
                        brim="#5d5667", edge="#b3adbf"),
        hair=dict(color="#988c98", front=0.0, grow=0.20),
        costume="waistcoat",
        colors=dict(base="#2f8b58", dark="#1e5f3b", lapel="#1f6641", stripe="#8fd3a8", shirt="#f1eae5", tie="#c9352e", tie_dark="#98241f",
                    brass="#e0c063", brass_l="#f1e2a4", pants="#3d3846", feather="#e2703a", feather_dark="#a84420"),
    ),
}

# arm presets: (dx, dy) of the hand from the shoulder (dx is mirrored for the left arm, + = away from the body),
# bend (+1 elbow out for a hanging arm, -1 elbow low/out for a raised or forward arm), layer, hand shape, joint sharpness, stretch
ARM_PRESETS = {
    "slim": {
        "down":     (0.055, 0.670, 0.50, "front", "ball", 0.15, 1.0),
        "hip":      (0.045, 0.620, 1.00, "front", "ball", 0.45, 1.0),
        "point":    (0.690, -0.100, -0.45, "front", "point", 0.20, 1.0),
        "raised":   (0.400, -0.600, -1.00, "front", "open", 0.30, 1.0),
        "behind":   (-0.100, 0.600, 0.90, "back", "ball", 0.30, 1.0),
        "forward":  (0.600, 0.220, -0.55, "front", "open", 0.30, 1.0),
        "reach_up": (0.560, -0.520, -0.40, "front", "ball", 0.20, 1.06),
        "rub":      (0.520, -0.400, -0.55, "front", "ball", 0.25, 1.05),
        "shrug":    (0.400, 0.020, -0.80, "front", "open", 0.40, 1.0),
        "chin":     (-0.215, -0.040, 1.00, "top", "ball", 0.45, 1.0),
        "wave":     (0.520, -0.330, -1.00, "front", "open", 0.30, 1.0),
    },
    "stout": {
        "down":     (0.180, 0.630, 0.90, "front", "ball", 0.15, 1.0),
        "hip":      (0.045, 0.450, 1.00, "front", "ball", 0.50, 1.0),
        "point":    (0.660, -0.060, -0.45, "front", "point", 0.20, 1.0),
        "raised":   (0.450, -0.500, -1.00, "front", "open", 0.30, 1.0),
        "behind":   (-0.160, 0.620, 0.90, "back", "ball", 0.30, 1.0),
        "forward":  (0.620, 0.200, -0.55, "front", "open", 0.30, 1.0),
        "reach_up": (0.560, -0.460, -0.40, "front", "ball", 0.20, 1.05),
        "rub":      (0.540, -0.380, -0.55, "front", "ball", 0.25, 1.05),
        "shrug":    (0.420, 0.040, -0.80, "front", "open", 0.40, 1.0),
        "chin":     (-0.340, 0.070, 1.00, "top", "ball", 0.45, 1.0),
        "wave":     (0.560, -0.280, -1.00, "front", "open", 0.30, 1.0),
    },
}
ARM_PRESETS["slim"]["akimbo"] = (0.050, 0.640, 1.00, "front", "ball", 0.0, 1.0)
ARM_PRESETS["stout"]["akimbo"] = (0.050, 0.470, 1.00, "front", "ball", 0.0, 1.0)

# leg presets -> parameters of the leg solver (spread None = the cast's own stance)
LEG_PRESETS = {
    "stand":  dict(spread=None, stride=0.0, crouch=0.0, rigid=False),
    "wide":   dict(spread="wide", stride=0.0, crouch=0.0, rigid=False),
    "narrow": dict(spread=-0.03, stride=0.0, crouch=0.0, rigid=False),
    "step":   dict(spread=-0.04, stride="yaw", crouch=0.04, rigid=False),
    "lean":   dict(spread=None, stride=0.0, crouch=0.0, rigid=True),
    "crouch": dict(spread=None, stride=0.0, crouch=0.28, rigid=False),
}
_LAYERS = ("back", "front", "top")
_SHAPES = ("ball", "point", "open")


def _pt(v):
    try:
        return (_num(v[0]), _num(v[1]))
    except Exception:
        return None


def _arm_spec(C, spec):
    tbl = ARM_PRESETS[C["build"]]
    base = tbl["down"]
    d = {}
    if isinstance(spec, dict):
        d = spec
        pr = d.get("preset")
        base = tbl.get(pr, base) if isinstance(pr, str) else base
    elif isinstance(spec, str):
        base = tbl.get(spec, base)
    out = dict(hand=None, rel=(base[0], base[1]), bend=base[2], layer=base[3], shape=base[4], sharp=base[5], stretch=base[6])
    if d:
        if d.get("hand") is not None:
            p = _pt(d["hand"])
            if p is not None:
                out["hand"] = p
                if "preset" not in d:
                    out["bend"] = None          # automatic, continuous in the hand height
                    out["shape"] = "ball"
                    out["layer"] = "front"
                    out["sharp"] = 0.25
                    out["stretch"] = 1.0
        if d.get("bend") is not None:
            out["bend"] = _clamp(_num(d["bend"], 1.0), -1.0, 1.0)
        if d.get("layer") in _LAYERS:
            out["layer"] = d["layer"]
        if d.get("shape") in _SHAPES:
            out["shape"] = d["shape"]
        if d.get("sharp") is not None:
            out["sharp"] = _clamp(_num(d["sharp"], 0.25), 0.0, 1.0)
        if d.get("stretch") is not None:
            out["stretch"] = _clamp(_num(d["stretch"], 1.0), 0.5, 1.3)
    return out


def _leg_spec(C, spec, yaw):
    d = spec if isinstance(spec, dict) else {}
    name = d.get("preset", "stand") if isinstance(spec, dict) else (spec if isinstance(spec, str) else "stand")
    base = LEG_PRESETS.get(name, LEG_PRESETS["stand"]) if isinstance(name, str) else LEG_PRESETS["stand"]
    sp = base["spread"]
    sp = C["stance"] if sp is None else (C["wide"] if sp == "wide" else sp)
    st = base["stride"]
    st = _clamp(yaw * 4.0, -1.0, 1.0) if st == "yaw" else st     # "step": stride follows the facing side
    out = dict(spread=sp, stride=st, crouch=base["crouch"], rigid=base["rigid"], lift_l=0.0, lift_r=0.0,
               foot_l=None, foot_r=None, knee_l=None, knee_r=None, toe_l=None, toe_r=None)
    if d:
        if d.get("spread") is not None:
            out["spread"] = _clamp(_num(d["spread"], sp), -0.2, 0.8)
        if d.get("stride") is not None:
            out["stride"] = _clamp(_num(d["stride"], 0.0), -1.5, 1.5)
        if d.get("crouch") is not None:
            out["crouch"] = _clamp(_num(d["crouch"], 0.0), 0.0, 0.75)
        for key in ("lift_l", "lift_r"):
            if d.get(key) is not None:
                out[key] = _clamp(_num(d[key], 0.0), 0.0, 1.5)
        for key in ("foot_l", "foot_r"):
            if d.get(key) is not None:
                out[key] = _pt(d[key])
        for key in ("knee_l", "knee_r", "toe_l", "toe_r"):
            if d.get(key) is not None:
                out[key] = _clamp(_num(d[key], 0.0), -1.0, 1.0)
        if "rigid" in d:
            out["rigid"] = bool(d["rigid"])
    return out


def _prop_spec(spec):
    if not spec:
        return None
    if isinstance(spec, str):
        spec = {"type": spec}
    if not isinstance(spec, dict):
        return None
    ty = spec.get("type")
    if not isinstance(ty, str) or ty not in PROP_TYPES:
        return None
    ang = spec.get("angle")
    return dict(type=spec["type"], angle=None if ang is None else _num(ang, 0.0), twist=_num(spec.get("twist"), 0.0),
                scale=_clamp(_num(spec.get("scale"), 1.0), 0.3, 3.0))


def _fx_spec(fx):
    out = []
    if not fx:
        return out
    if isinstance(fx, (str, dict)):
        fx = [fx]
    if not isinstance(fx, (list, tuple)):
        return out
    for it in fx:
        if isinstance(it, str):
            name, d = it, {}
        elif isinstance(it, dict):
            name, d = it.get("type"), it
        elif isinstance(it, (tuple, list)) and it:
            name = it[0]
            d = {"level": it[1], "t": it[1], "seed": it[1]} if len(it) > 1 else {}
        else:
            continue
        if isinstance(name, str) and name in FX_TYPES:
            out.append((name, d))
    return out


def _norm(C, pose):
    if not isinstance(pose, dict):
        pose = {}
    g = pose.get
    P = {}
    P["yaw"] = _clamp(_num(g("yaw")), -1.2, 1.2)
    P["pitch"] = _clamp(_num(g("pitch")), -1.5, 1.5)
    P["head_roll"] = _clamp(_num(g("head_roll")), -75.0, 75.0)
    P["head_dx"] = _clamp(_num(g("head_dx")), -0.8, 0.8)
    P["head_dy"] = _clamp(_num(g("head_dy")), -0.8, 0.8)
    P["lean"] = _clamp(_num(g("lean")), -75.0, 75.0)
    sq = g("squash")
    if isinstance(sq, (tuple, list)) and len(sq) >= 2:
        P["squash"] = (_clamp(_num(sq[0], 1.0), 0.3, 2.5), _clamp(_num(sq[1], 1.0), 0.3, 2.5))
    else:
        s = _clamp(_num(sq, 1.0), 0.3, 2.5)
        P["squash"] = (s, s)
    e = g("expr")
    P["expr"] = e if (isinstance(e, str) and e in EXPRESSIONS) else "neutral"
    mth = g("mouth")
    if isinstance(mth, (tuple, list)):
        mth = tuple(mth) if (len(mth) >= 3 and mth[0] == "open") else None
    elif not isinstance(mth, str) or mth not in MOUTHS:
        mth = None
    P["mouth"] = mth
    P["blink"] = int(_clamp(round(_num(g("blink"))), 0, 2))
    gz = g("gaze")
    if isinstance(gz, (tuple, list)) and len(gz) >= 2:
        P["gaze"] = (_num(gz[0]), _num(gz[1]))
    else:
        P["gaze"] = (_num(gz), 0.0)
    P["arm_r"] = _arm_spec(C, g("arm_r"))
    P["arm_l"] = _arm_spec(C, g("arm_l"))
    P["legs"] = _leg_spec(C, g("legs"), P["yaw"])
    P["prop_r"] = _prop_spec(g("prop_r"))
    P["prop_l"] = _prop_spec(g("prop_l"))
    P["fx"] = _fx_spec(g("fx"))
    P["t"] = _num(g("t"))
    tint = g("tint")
    P["tint"] = None
    if _is_hex(tint):
        P["tint"] = _rgb(tint)
    elif isinstance(tint, (tuple, list)) and len(tint) >= 3:
        P["tint"] = tuple(_clamp(_num(v, 255.0), 0.0, 255.0) for v in tint[:3])
    ink = g("ink")
    P["ink"] = ("#" + ink.lstrip("#")) if _is_hex(ink) else INK
    P["mirror"] = bool(g("mirror"))
    P["limb_w"] = _clamp(_num(g("limb_w"), C.get("limb_w", LW)), 0.035, 0.09)
    rim = g("rim")
    P["rim"] = ("#" + rim.lstrip("#")) if _is_hex(rim) else None
    P["rim_w"] = _clamp(_num(g("rim_w"), 0.014), 0.004, 0.05)
    P["rim_opacity"] = _clamp(_num(g("rim_opacity"), 0.6), 0.0, 1.0)
    return P


def _solve(C, P):
    """all joint positions for a normalised pose, in figure coordinates (head centre origin, before squash/mirror)."""
    yaw = P["yaw"]
    m = _TorsoMap(C, yaw)
    a = math.radians(P["lean"])
    cl, sl = math.cos(a), math.sin(a)
    hdx, hdy = P["head_dx"], P["head_dy"]

    def T(x, y):
        return (x * cl - y * sl - hdx, x * sl + y * cl - hdy)

    yB = TORSO_TOP + C["torso_h"]
    sx, sy = C["shoulder"]
    sxa = sx * m.nf
    R = dict(m=m, T=T, yB=yB)
    arms = {}
    for side, key in ((1, "r"), (-1, "l")):
        A = P["arm_" + key]
        S = T(side * sxa, sy)
        tg = A["hand"] if A["hand"] is not None else T(side * (sxa + A["rel"][0]), sy + A["rel"][1])
        bend = A["bend"]
        if bend is None:
            bend = _clamp((tg[1] - (S[1] + 0.10)) / 0.30, -1.0, 1.0)
        E, H = _ik(S, tg, C["arm"] * A["stretch"], bend * side)
        dx, dy = H[0] - E[0], H[1] - E[1]
        dl = math.hypot(dx, dy)
        if dl < 1e-6:
            dx, dy = H[0] - S[0], H[1] - S[1]
            dl = math.hypot(dx, dy)
        dirv = (dx / dl, dy / dl) if dl > 1e-6 else (0.0, 1.0)
        # 1 for a normal pose; fades to 0 when the hand sits on the shoulder (where the forearm direction is undefined)
        fold = _smooth(0.0, 0.25 * C["arm"] * A["stretch"], math.hypot(H[0] - S[0], H[1] - S[1]))
        arms[key] = dict(S=S, E=E, H=H, dir=dirv, bend=bend, spec=A, fold=fold)
    R["arms"] = arms
    # legs
    Lg = P["legs"]
    L = C["leg"]
    hipx = C["hip_x"] * m.nf
    yh = yB - 0.04
    hips = {"l": T(-hipx, yh), "r": T(hipx, yh)}
    hc = T(0.0, yh)
    sp, st, cr = Lg["spread"], Lg["stride"], Lg["crouch"]
    af = _smooth(0.2, 0.8, abs(yaw))
    sg = 1.0 if yaw >= 0 else -1.0
    sdir = _clamp(st * 4.0, -1.0, 1.0)
    sw = min(1.0, abs(st) * 2.0)
    auto = {"l": _lerp(_lerp(-1.0, sg, af), sdir, sw), "r": _lerp(_lerp(1.0, sg, af), sdir, sw)}
    tg = {}
    if Lg["rigid"]:
        drop = math.sqrt(max(L * L - sp * sp, 0.1 * L * L)) * (1.0 - cr)
        tg["l"] = T(-(hipx + sp) - 0.26 * st, yh + drop)
        tg["r"] = T((hipx + sp) + 0.34 * st, yh + drop)
    else:
        xs = {"l": hc[0] - (hipx + sp) - 0.26 * st, "r": hc[0] + (hipx + sp) + 0.34 * st}
        yg = min(hips[q][1] + math.sqrt(max(L * L - (xs[q] - hips[q][0]) ** 2, 0.1 * L * L)) for q in ("l", "r"))
        yg = hc[1] + (yg - hc[1]) * (1.0 - cr)
        tg["l"] = (xs["l"], yg - 0.30 * Lg["lift_l"])
        tg["r"] = (xs["r"], yg - 0.30 * Lg["lift_r"])
    legs = {}
    for q in ("l", "r"):
        if Lg["foot_" + q] is not None:
            tg[q] = Lg["foot_" + q]
        kd = Lg["knee_" + q] if Lg["knee_" + q] is not None else auto[q]
        toe = Lg["toe_" + q] if Lg["toe_" + q] is not None else auto[q]
        E, A = _ik(hips[q], tg[q], L, kd)
        # standing legs are "straight or very slightly bowed" (anatomy 1.5): a constant 0.012 D outward bow, baked per leg
        bw = 0.012 * (1.0 if q == "r" else -1.0)
        dl = math.hypot(A[0] - hips[q][0], A[1] - hips[q][1]) or 1.0
        E = (E[0] + (A[1] - hips[q][1]) / dl * bw, E[1] - (A[0] - hips[q][0]) / dl * bw)
        legs[q] = dict(S=hips[q], E=E, H=A, knee=kd, toe=toe)
    R["legs"] = legs
    R["feet_y"] = max(legs["l"]["H"][1], legs["r"]["H"][1]) + P["limb_w"] / 2 + 0.008
    return R


def resolve_pose(cast_name, pose=None):
    """expand presets into plain numbers: returns a pose dict whose arms are {"hand": (x, y), "bend", ...} and whose legs
    are {"foot_l", "foot_r", "knee_l", ...}.  figure(cast, resolve_pose(cast, p)) draws the same picture as figure(cast, p)."""
    C = CAST[cast_name]
    P = _norm(C, pose or {})
    R = _solve(C, P)
    out = dict(pose) if isinstance(pose, dict) else {}
    for key in ("yaw", "pitch", "head_roll", "head_dx", "head_dy", "lean", "squash", "blink", "gaze", "t"):
        out[key] = P[key]
    out["expr"] = P["expr"]
    for q in ("r", "l"):
        A = R["arms"][q]
        sp = A["spec"]
        # target, not the clamped hand: resolving twice must give the same drawing
        tgt = sp["hand"] if sp["hand"] is not None else R["T"]((1 if q == "r" else -1) * (C["shoulder"][0] * R["m"].nf + sp["rel"][0]), C["shoulder"][1] + sp["rel"][1])
        out["arm_" + q] = dict(hand=tgt, bend=A["bend"], layer=sp["layer"], shape=sp["shape"], sharp=sp["sharp"], stretch=sp["stretch"])
    Lg = P["legs"]
    leg = dict(preset="stand")
    for q in ("l", "r"):
        leg["foot_" + q] = R["legs"][q]["H"]
        leg["knee_" + q] = R["legs"][q]["knee"]
        leg["toe_" + q] = R["legs"][q]["toe"]
    out["legs"] = leg
    return out


def _lerp_hex(a, b, t):
    return _mix(a, b, t)


def lerp_pose(cast_name, a, b, t):
    """blend two poses (presets allowed) for in-betweens.  Numbers are interpolated; drawings that must not be tweened
    (expr, mouth, blink, props, fx, hand shape, layer) switch at t = 0.5."""
    t = _clamp(_num(t), 0.0, 1.0)
    A, B = resolve_pose(cast_name, a), resolve_pose(cast_name, b)
    first = A if t < 0.5 else B
    out = dict(first)
    for key in ("yaw", "pitch", "head_roll", "head_dx", "head_dy", "lean", "t"):
        out[key] = _lerp(A[key], B[key], t)
    out["squash"] = (_lerp(A["squash"][0], B["squash"][0], t), _lerp(A["squash"][1], B["squash"][1], t))
    out["gaze"] = (_lerp(A["gaze"][0], B["gaze"][0], t), _lerp(A["gaze"][1], B["gaze"][1], t))
    for q in ("arm_r", "arm_l"):
        x, y = A[q], B[q]
        d = dict(first[q])
        d["hand"] = (_lerp(x["hand"][0], y["hand"][0], t), _lerp(x["hand"][1], y["hand"][1], t))
        for f in ("bend", "sharp", "stretch"):
            d[f] = _lerp(x[f], y[f], t)
        out[q] = d
    leg = dict(preset="stand")
    for f in ("foot_l", "foot_r"):
        leg[f] = (_lerp(A["legs"][f][0], B["legs"][f][0], t), _lerp(A["legs"][f][1], B["legs"][f][1], t))
    for f in ("knee_l", "knee_r", "toe_l", "toe_r"):
        leg[f] = _lerp(A["legs"][f], B["legs"][f], t)
    out["legs"] = leg
    for q in ("prop_r", "prop_l"):
        pa, pb = _prop_spec(A.get(q)), _prop_spec(B.get(q))
        if pa and pb and pa["type"] == pb["type"] and pa["angle"] is not None and pb["angle"] is not None:
            d = dict(pa)
            d["angle"] = _lerp(pa["angle"], pb["angle"], t)
            d["scale"] = _lerp(pa["scale"], pb["scale"], t)
            out[q] = d
    ta, tb = A.get("tint"), B.get("tint")
    if isinstance(ta, str) and isinstance(tb, str):
        out["tint"] = _lerp_hex(ta, tb, t)
    return out


# ----------------------------------------------------------------------------- figure
def figure(cast_name, pose=None, uid="p"):
    """Draw one character.  Returns {"svg": <g> fragment in D units (head centre at the origin, y down),
    "feet_y": y of the soles, "bbox": (x0, y0, x1, y1), "anchors": {...}} -- all in the same local D units.
    See API.md for every pose key."""
    C = CAST[cast_name]
    P = _norm(C, pose or {})
    k = _Ctx(str(uid), P["ink"], P["tint"])
    u = k.uid
    R = _solve(C, P)
    m = R["m"]
    yaw = P["yaw"]
    roll = P["head_roll"]
    mir = P["mirror"]
    fcx = -FC[0] if mir else FC[0]        # inside a mirrored group the head frame must still land on the unmirrored disc
    fcy = FC[1]
    fx = dict(P["fx"])
    tph = P["t"]
    layers = {"back": [], "front": [], "top": []}
    anchors = {}
    lw = P["limb_w"]
    hand_r = HAND_R * (lw / LW) ** 0.75        # hand ball follows the limb weight ("about twice the stroke width")
    rim, rw = P["rim"], P["rim_w"]
    rims = []                                  # optional light halo behind arms, hands, legs and feet (dark backgrounds)

    # ---- arms (+ props, hands)
    for key in ("l", "r"):
        A = R["arms"][key]
        sp = A["spec"]
        S, E, H = A["S"], A["E"], A["H"]
        parts = [_ink_limb(k, S, E, H, sp["sharp"], lw, C["seed"] * 1.7 + (2.3 if key == "r" else 4.6))]
        k.ext.extend(((S[0], S[1], 0.04), (2 * E[0] - (S[0] + H[0]) / 2, 2 * E[1] - (S[1] + H[1]) / 2, 0.04), (E[0], E[1], 0.04)))
        prop = P["prop_" + key]
        shape = sp["shape"]
        tip = None
        if prop:
            ang = prop["angle"] if prop["angle"] is not None else math.degrees(math.atan2(A["dir"][1], A["dir"][0])) + prop["twist"]
            psvg, tip = _prop(k, prop["type"], H, ang, prop["scale"])
            parts.append(psvg)
            shape = "ball"
        parts.append(_hand(k, H, A["dir"], shape, hand_r, A["fold"]))
        if tip is None:
            r = (0.118 * hand_r / HAND_R if shape == "point" else hand_r) * A["fold"]
            tip = (H[0] + A["dir"][0] * r, H[1] + A["dir"][1] * r)
        layers[sp["layer"]].append("".join(parts))
        if rim:
            rims.append('<path d="%s"/><circle cx="%.4f" cy="%.4f" r="%.4f" fill="%s" stroke="none"/>'
                        % (_limb_d(S, E, H, sp["sharp"]), H[0], H[1], hand_r + rw, rim))
        anchors["hand_" + key] = H
        anchors["elbow_" + key] = E
        anchors["shoulder_" + key] = S
        anchors["prop_tip_" + key] = tip

    # ---- legs + feet (behind the torso)
    legs_svg = []
    for key in ("l", "r"):
        Lq = R["legs"][key]
        S, E, A = Lq["S"], Lq["E"], Lq["H"]
        toe = Lq["toe"]
        legs_svg.append(_ink_limb(k, S, E, A, 0.55, lw, C["seed"] * 1.7 + (6.9 if key == "r" else 9.2),
                                  tail=(A[0] + toe * FOOT_LEN, A[1] + 0.010 * abs(toe))))
        if rim:
            rims.append('<path d="%s L%.4f,%.4f"/>' % (_limb_d(S, E, A, 0.55), A[0] + toe * FOOT_LEN, A[1] + 0.010 * abs(toe)))
        k.ext.extend(((S[0], S[1], 0.04), (E[0], E[1], 0.06), (A[0], A[1], 0.045), (A[0] + toe * FOOT_LEN, A[1], 0.045)))
        anchors["foot_" + key] = A
        anchors["knee_" + key] = E
    feet_y = R["feet_y"]
    anchors["feet"] = ((anchors["foot_l"][0] + anchors["foot_r"][0]) / 2, feet_y)

    # ---- torso
    T = R["T"]
    torso = ('<g transform="translate(%.4f %.4f) rotate(%.4f)">%s</g>'
             % (-P["head_dx"], -P["head_dy"], P["lean"], _torso(k, C, m)))
    yB = R["yB"]
    for p in ((-m.hwa, 0.95), (m.hwa, 0.95), (-m.hwa * 0.8, 0.45), (m.hwa * 0.8, 0.45), (0.0, yB), (-m.hwa * 0.7, yB - 0.08), (m.hwa * 0.7, yB - 0.08)):
        q = T(p[0], p[1])
        k.ext.append((q[0], q[1], 0.03))
    anchors["hip"] = T(0.0, yB - 0.04)
    anchors["chest"] = T(m.c, 0.80)

    # ---- head disc (never rotated or mirrored: the thick side of the contour stays lower-right, face spec 3.1)
    ink_d, fill_d = _head_geom(C["seed"])
    white = k.c(HEAD_FILL)
    k.defs.append('<radialGradient id="%s_hg" gradientUnits="userSpaceOnUse" cx="-0.029" cy="-0.034" r="0.56">'
                  '<stop offset="0" stop-color="%s"/><stop offset="0.705" stop-color="%s"/><stop offset="0.80" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                  '<clipPath id="%s_hc"><path d="%s"/></clipPath>'
                  % (u, white, white, k.c(HEAD_SHADE), k.c(HEAD_SHADE), u, fill_d))
    disc = ['<g transform="translate(%.4f %.4f)">' % FC, '<path d="%s" fill="%s"/>' % (ink_d, k.ink),
            '<path d="%s" fill="url(#%s_hg)"/>' % (fill_d, u)]
    if "anger_fill" in fx:
        d = fx["anger_fill"]
        lev = _clamp(_num(d.get("level"), 1.0), 0.0, 1.0)
        ph = _num(d.get("t"), tph) * 2 * math.pi
        k.defs.append('<radialGradient id="%s_pg" gradientUnits="userSpaceOnUse" cx="-0.07" cy="-0.09" r="0.56">'
                      '<stop offset="0" stop-color="%s"/><stop offset="0.55" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
                      % (u, k.c(PURPLE[0]), k.c(PURPLE[1]), k.c(PURPLE[2])))
        yl = 0.52 - 1.06 * lev
        wave = [(-0.6 + 0.05 * i, yl + 0.012 * (1 - _smooth(0.9, 1.0, lev)) * math.sin(i * 1.1 + ph)) for i in range(25)]
        disc.append('<g clip-path="url(#%s_hc)"><path d="M%s L0.6,0.7 L-0.6,0.7 Z" fill="url(#%s_pg)"/>' % (u, "L".join("%.4f,%.4f" % p for p in wave), u))
        disc.append('<path d="M%s" fill="none" stroke="%s" stroke-width="0.020" opacity="%.3f"/>'
                    % ("L".join("%.4f,%.4f" % p for p in wave), k.c("#d49ff9"), 1 - _smooth(0.9, 1.0, lev)))
        for i, (bx, bo) in enumerate(((-0.17, 0.10), (0.06, 0.19), (0.23, 0.07))):
            disc.append('<circle cx="%.4f" cy="%.4f" r="0.017" fill="none" stroke="%s" stroke-width="0.008" opacity="%.3f"/>'
                        % (bx, yl + bo + 0.02 * math.sin(ph + i), k.c("#db96ff"), (1 - _smooth(0.85, 1.0, lev)) * _smooth(0.0, 0.2, lev)))
        a0, a1, rr = math.radians(188), math.radians(228), 0.40
        disc.append('</g><path d="M%.4f,%.4f A%.2f,%.2f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="%.3f"/>'
                    % (rr * math.cos(a0), rr * math.sin(a0), rr, rr, rr * math.cos(a1), rr * math.sin(a1), k.c("#f0b2ee"), _smooth(0.8, 1.0, lev)))
        white = _mix(white, k.c(PURPLE[0]), _smooth(0.45, 0.75, lev))
    disc.append('</g>')
    k.ext.append((0.0, 0.0, 0.515))

    # ---- hair (clipped to the fill disc), face, effects on the face, hat: all roll with the head
    head_tr = 'translate(%.4f %.4f) rotate(%.4f)' % (fcx, fcy, roll)
    hair = '<g transform="rotate(%.4f)">%s</g>' % (roll, _hair(k, C, yaw))
    face_svg, L = _face(k, C, P, white)
    hd = [face_svg]
    if "blush" in fx:
        hd.insert(0, _fx_blush(k, L))
    if "sweat" in fx:
        d = fx["sweat"]
        side = d.get("side")
        # temple beside the far (leading) eye: right for yaw >= -0.05, left for yaw <= -0.25, sliding in between
        side = _clamp(_num(side), -1.0, 1.0) if side is not None else 1.0 - 2.0 * _smooth(0.05, 0.25, -yaw)
        hd.append(_fx_sweat(k, 0.335 * side, C["eye_y"] - 0.155, _num(d.get("scale"), 1.0), 8.0 * side))
    if "tears" in fx:
        hd.append(_fx_tears(k, L, _num(fx["tears"].get("t"), tph)))
    n0 = len(k.ext)                     # everything recorded from here on is in the head frame
    if C.get("ear_pencil"):
        hd.append(_ear_pencil(k, C, yaw))
    if C["hat"] == "newsboy":
        hat_svg, hat_top = _hat_newsboy(k, C, yaw)
    elif C["hat"] == "homburg":
        hat_svg, hat_top = _hat_homburg(k, C, yaw)
    else:                               # hat=None: bare head (used by measure.py; no bare head exists in the reference)
        hat_svg, hat_top = "", (0.0, -0.484)
    hd.append(hat_svg)
    top_fx = []
    if "steam" in fx:
        top_fx.append(_fx_steam(k, _num(fx["steam"].get("t"), tph)))
    if "zzz" in fx:
        top_fx.append(_fx_zzz(k, _num(fx["zzz"].get("t"), tph)))

    def HP(x, y):                       # head frame -> figure coordinates (unmirrored figure)
        rx, ry = _rot(x, y, roll)
        return (FC[0] + rx, FC[1] + ry)

    # hat / fx extents were recorded in the head frame: move them to figure coordinates
    k.ext[n0:] = [HP(e[0], e[1]) + (e[2],) for e in k.ext[n0:]]
    anchors["mouth"] = HP(L["mx"], L["my"])
    anchors["eye_l"] = HP(L["xL"], L["ey"])
    anchors["eye_r"] = HP(L["xR"], L["ey"])
    anchors["head_top"] = (FC[0], FC[1] - 0.484)
    anchors["hat_top"] = HP(hat_top[0], hat_top[1])
    anchors["head"] = (0.0, 0.0)

    # ---- assemble (back to front)
    sxq, syq = P["squash"]
    body1 = []
    if "focus_lines" in fx:
        d = fx["focus_lines"]
        body1.append(_fx_focus(int(_num(d.get("seed"), 0.0)), int(_clamp(_num(d.get("n"), 30.0), 4, 80))))
    if rims:
        # one group, drawn behind the whole figure: the halo shows only where a limb leaves the body silhouette
        body1.append('<g fill="none" stroke="%s" stroke-width="%.4f" stroke-linecap="round" stroke-linejoin="round" opacity="%.3f">%s</g>'
                     % (rim, 1.11 * lw + 2 * rw, P["rim_opacity"], "".join(rims)))
    body1.extend(layers["back"])
    body1.extend(legs_svg)
    body1.append(torso)
    body1.extend(layers["front"])
    body2 = ['<g transform="%s">%s</g>' % (head_tr, "".join(hd))]
    body2.extend(layers["top"])
    if top_fx:
        body2.append('<g transform="%s">%s</g>' % (head_tr, "".join(top_fx)))
    hair_g = '<g transform="translate(%.4f %.4f)" clip-path="url(#%s_hc)">%s%s</g>' % (
        FC[0], FC[1], u, '<g transform="scale(-1 1)">' if mir else "", hair + ("</g>" if mir else ""))
    if mir:
        s1 = '<g transform="scale(-1 1)">%s</g>' % "".join(body1)
        s2 = '<g transform="scale(-1 1)">%s</g>' % "".join(body2)
    else:
        s1, s2 = "".join(body1), "".join(body2)
    svg = ('<g id="%s_fig" transform="scale(%.4f %.4f)"><defs>%s</defs>%s%s%s%s</g>'
           % (u, sxq, syq, "".join(k.defs), s1, "".join(disc), hair_g, s2))

    # ---- bbox, anchors: squash + mirror
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for (x, y, r) in k.ext:
        if x - r < x0:
            x0 = x - r
        if x + r > x1:
            x1 = x + r
        if y - r < y0:
            y0 = y - r
        if y + r > y1:
            y1 = y + r
    if feet_y > y1:
        y1 = feet_y
    if mir:
        x0, x1 = -x1, -x0
        an = {}
        for key, v in anchors.items():
            if key.endswith("_r"):
                key = key[:-2] + "_l"
            elif key.endswith("_l"):
                key = key[:-2] + "_r"
            an[key] = (-v[0], v[1])
        anchors = an
        anchors["head_top"] = (FC[0], FC[1] - 0.484)
    pad = 0.02
    bbox = ((x0 - pad) * sxq, (y0 - pad) * syq, (x1 + pad) * sxq, (y1 + pad) * syq)
    anchors = dict((key, (v[0] * sxq, v[1] * syq)) for key, v in anchors.items())
    return {"svg": svg, "feet_y": feet_y * syq, "bbox": bbox, "anchors": anchors}


def place_svg(fig, x, y, scale, anchor="feet"):
    """wrap a figure() result so that its feet (anchor="feet": point under the feet, on the sole line) or its head centre
    (anchor="head") lands on (x, y) of the parent frame, drawn at `scale` parent units per D."""
    if anchor == "feet":
        tx, ty = x - fig["anchors"]["feet"][0] * scale, y - fig["feet_y"] * scale
    else:
        tx, ty = x, y
    return '<g transform="translate(%.3f %.3f) scale(%.4f)">%s</g>' % (tx, ty, scale, fig["svg"])


def hand_for_tip(prop_type, tip, angle, scale=1.0):
    """hand target (local D units) that puts the tip of a held prop on `tip` when the prop is held at `angle` degrees
    (SVG convention: 0 = pointing right, -90 = pointing up).  Use it as arm_r={"hand": hand_for_tip(...)} together with
    prop_r={"type": prop_type, "angle": angle}; read anchors["prop_tip_r"] afterwards (the arm may not reach)."""
    L = PROP_TIP.get(prop_type, 0.0) * scale
    a = math.radians(angle)
    return (tip[0] - L * math.cos(a), tip[1] - L * math.sin(a))


def contact_shadow(width_D, uid="cs", color="#252432", opacity=0.6):
    """soft contact ellipse under the feet (clip B: about 0.4 D wide with a soft edge; lightkit: 0.75 of the body width,
    #252432 at 0.6).  Centred on (0, 0): translate it to (anchors["feet"][0], feet_y) in the figure's parent frame."""
    w = max(_num(width_D, 0.8), 0.01)
    return ('<defs><radialGradient id="%s_cs"><stop offset="0" stop-color="%s" stop-opacity="%.3f"/><stop offset="0.45" stop-color="%s" stop-opacity="%.3f"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient></defs>'
            '<ellipse cx="0" cy="0" rx="%.4f" ry="%.4f" fill="url(#%s_cs)"/>'
            % (uid, color, opacity, color, opacity * 0.82, color, w / 2.0, w * 0.115, uid))


# ============================================================================= command line: sheet / compare / test / bench
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
WALL, WALL_DARK, FLOOR = "#a8663f", "#55291a", "#1f2a55"

# the three story poses (also used by the sheet)
STORY = {
    "hero_draw":  ("hero", dict(yaw=0.55, pitch=-0.4, head_roll=6, lean=4, expr="determined", arm_r="reach_up",
                                prop_r=dict(type="pencil", angle=-48), arm_l="down", legs="stand")),
    "boss_rub":   ("boss", dict(yaw=-0.5, head_roll=-5, lean=-3, expr="smug", arm_l="rub", prop_l=dict(type="eraser", angle=-140),
                                arm_r="hip", legs="stand")),
    "hero_shock": ("hero", dict(yaw=-0.35, head_roll=-7, head_dy=-0.05, lean=5, squash=(0.97, 1.04), expr="shocked", fx=["sweat"],
                                arm_r="shrug", arm_l="shrug", legs="wide")),
}


def _place(cast, pose, uid, D, x, y, anchor="feet", shadow=0.0):
    """figure scaled to D px with its feet (or head centre) at pixel (x, y)."""
    f = figure(cast, pose, uid)
    if anchor == "feet":
        tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
        s = ('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, contact_shadow(shadow, uid + "s"))) if shadow else ""
    else:
        tx, ty, s = x, y, ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _label(x, y, txt, size=15):
    return ('<text x="%d" y="%d" font-family="Arial, Helvetica, sans-serif" font-size="%d" font-weight="700" fill="#ffffff" stroke="#1a1015" '
            'stroke-width="3" paint-order="stroke" stroke-linejoin="round">%s</text>' % (x, y, size, txt))


def build_sheet():
    W = 3000
    o = []
    y = 0
    uid = [0]

    def nid():
        uid[0] += 1
        return "f%d" % uid[0]

    # --- row 1: five yaw states for both cast members
    cw, ch, D = 300, 500, 112
    views = ((-1.0, "near-profile L"), (-0.5, "three-quarter L"), (0.0, "front"), (0.5, "three-quarter R"), (1.0, "near-profile R"))
    for ci, cast in enumerate(("hero", "boss")):
        for vi, (yw, name) in enumerate(views):
            x0 = (ci * 5 + vi) * cw
            fl = y + ch - 62
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/><rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                     % (x0, y, cw, ch, WALL if (ci + vi) % 2 == 0 else WALL_DARK, x0, fl - 14, cw, ch - (fl - 14 - y), FLOOR))
            g, f = _place(cast, dict(yaw=yw, arm_r="down", arm_l="hip" if cast == "hero" else "down", expr="neutral"), nid(), D, x0 + cw / 2, fl, shadow=0.9)
            o.append(g)
            o.append(_label(x0 + 8, y + 20, "%s yaw %+.1f %s" % (cast, yw, name)))
    y += ch
    # --- rows 2-5: the 20 expressions, both cast members (medium close-up, D = 190 px)
    cw, ch, D = 300, 310, 190
    names = ["neutral", "unimpressed", "smirk", "determined", "angry", "furious", "smug", "talking", "shocked", "stunned",
             "excited", "happy", "laughing", "worried", "asleep", "shouting", "grinning", "wink", "sad", "blink"]
    extra = {"furious": dict(fx=["anger_fill", dict(type="steam", t=0.35)], pitch=-0.6), "angry": dict(pitch=-0.9),
             "shocked": dict(fx=["sweat"]), "worried": dict(fx=["sweat"]), "laughing": dict(fx=["blush", dict(type="tears", t=0.3)], head_roll=14),
             "asleep": dict(fx=[dict(type="zzz", t=0.4)], pitch=0.6, head_roll=10), "sad": dict(pitch=1.0), "wink": dict(yaw=-0.7),
             "smug": dict(yaw=0.25), "talking": dict(yaw=0.25), "unimpressed": dict(yaw=-0.6), "smirk": dict(gaze=0.6), "blink": dict(blink=1, expr="excited"),
             "happy": dict(pitch=-0.4)}
    for ci, cast in enumerate(("hero", "boss")):
        for i, nm in enumerate(names):
            x0 = (i % 10) * cw
            yy = y + (ci * 2 + i // 10) * ch
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, yy, cw, ch, (WALL, WALL_DARK, "#7a3f2a")[(i + i // 10 + ci) % 3]))
            p = dict(expr=nm)
            p.update(extra.get(nm, {}))
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d">' % (x0, yy, cw, ch, cw, ch))
            g, f = _place(cast, p, nid(), D, cw / 2, ch / 2 + (18 if cast == "hero" else 40), anchor="head")
            o.append(g + "</svg>")
            o.append(_label(x0 + 8, yy + 20, "%s: %s" % (cast, "blink=1 (half)" if nm == "blink" else nm)))
    y += 4 * ch
    # --- row 6: body poses, including the three story poses
    cw, ch, D = 300, 560, 118
    poses = [
        ("hero", "akimbo, wide stance", dict(expr="smirk", arm_r="hip", arm_l="hip", legs="wide", head_roll=4)),
        ("hero", "pointing, 3/4", dict(yaw=0.6, expr="determined", arm_r="point", arm_l="hip", head_roll=5)),
        ("hero", "STORY draws on the map", STORY["hero_draw"][1]),
        ("hero", "STORY shocked", STORY["hero_shock"][1]),
        ("hero", "walking with paper", dict(yaw=1.0, expr="happy", legs=dict(preset="step", stride=0.9), arm_r="forward", prop_r=dict(type="paper", angle=-75), arm_l=dict(preset="down", layer="back"), lean=5)),
        ("hero", "crouch, worried", dict(yaw=-0.3, expr="worried", fx=["sweat"], legs="crouch", arm_l="chin", arm_r="down", head_roll=-8, lean=-6)),
        ("boss", "STORY rubs it out, smug", STORY["boss_rub"][1]),
        ("boss", "hand on hip + pointer, angry", dict(expr="angry", pitch=-0.9, arm_r="hip", arm_l=dict(preset="down"), prop_l=dict(type="pointer", angle=97), head_roll=-3)),
        ("boss", "leaning in, talking", dict(yaw=-0.8, lean=-20, head_dx=-0.10, head_roll=-12, expr="talking", mouth="talk_b", arm_l="point", arm_r=dict(preset="behind"), legs="stand")),
        ("boss", "hands behind, laughing", dict(yaw=0.3, expr="laughing", fx=["blush"], head_roll=12, lean=-6, arm_r="behind", arm_l="behind", legs="wide")),
    ]
    for i, (cast, nm, p) in enumerate(poses):
        x0 = i * cw
        fl = y + ch - 64
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/><rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                 % (x0, y, cw, ch, WALL if i % 2 else WALL_DARK, x0, fl - 14, cw, ch - (fl - 14 - y), FLOOR))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y, cw, ch, x0, y, cw, ch))
        g, f = _place(cast, p, nid(), D, x0 + cw / 2, fl, shadow=0.9)
        o.append(g + "</svg>")
        o.append(_label(x0 + 8, y + 20, "%s: %s" % (cast, nm), 14))
    y += ch
    # --- row 7: palette separation swatches, per-shot tint, mirror
    cw, ch, D = 300, 520, 112
    cells = [
        ("hero", WALL, None, None, "on #a8663f", {}), ("boss", WALL, None, None, "on #a8663f", {}),
        ("hero", WALL_DARK, None, None, "on #55291a", {}), ("boss", WALL_DARK, None, None, "on #55291a", {}),
        ("hero", FLOOR, None, None, "on #1f2a55", {}), ("boss", FLOOR, None, None, "on #1f2a55", {}),
        ("hero", "#3d346d", "#fbdaf7", "#1e142e", "tint night #fbdaf7", dict(expr="worried")),
        ("boss", "#3d346d", "#fbdaf7", "#1e142e", "tint night #fbdaf7", dict(expr="unimpressed", yaw=-0.5)),
        ("hero", "#6b2f22", "#faded0", None, "tint warm #faded0", dict(expr="smirk", yaw=0.5)),
        ("boss", "#6b2f22", "#faded0", None, "tint warm + mirror", dict(expr="smug", yaw=0.5, mirror=True, arm_r="hip")),
    ]
    for i, (cast, bg, tint, ink, nm, extra_p) in enumerate(cells):
        x0 = i * cw
        fl = y + ch - 60
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, cw, ch, bg))
        p = dict(arm_r="down", arm_l="hip" if cast == "hero" else "down")
        p.update(extra_p)
        if tint:
            p["tint"] = tint
        if ink:
            p["ink"] = ink
        g, f = _place(cast, p, nid(), D, x0 + cw / 2, fl, shadow=0.9)
        o.append(g)
        o.append(_label(x0 + 8, y + 20, "%s %s" % (cast, nm), 14))
    y += ch
    # --- row 8 (review): rim option on the dark office colours, akimbo preset, silhouettes, the pair at head D = 110 px
    cw, ch, D = 300, 520, 110
    RIM = "#8f9bd8"
    cells = [
        ("hero", FLOOR, "rim on #1f2a55", dict(rim=RIM, arm_l="hip")), ("boss", FLOOR, "rim on #1f2a55", dict(rim=RIM)),
        ("hero", WALL_DARK, "rim #d9a27a on #55291a", dict(rim="#d9a27a", arm_l="hip")), ("boss", WALL_DARK, "rim #d9a27a on #55291a", dict(rim="#d9a27a")),
        ("hero", WALL, "akimbo (smooth arcs)", dict(arm_r="akimbo", arm_l="akimbo", expr="smirk")),
        ("boss", WALL, "akimbo (smooth arcs)", dict(arm_r="akimbo", arm_l="akimbo", expr="smug")),
    ]
    for i, (cast, bg, nm, p) in enumerate(cells):
        x0 = i * cw
        fl = y + ch - 60
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, cw, ch, bg))
        g, f = _place(cast, p, nid(), D, x0 + cw / 2, fl, shadow=0.9)
        o.append(g)
        o.append(_label(x0 + 8, y + 20, "%s %s" % (cast, nm), 14))
    o.append('<defs><filter id="sheet_sil" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0 0 0 0 0.10  0 0 0 0 0.08  0 0 0 0 0.10  0 0 0 1 0"/></filter></defs>')
    for i, (bg, sil, nm) in enumerate(((("#efe9e2"), True, "silhouettes, D = 110 px"), (WALL, False, "pair on #a8663f, D = 110 px"), (FLOOR, False, "pair on #1f2a55, D = 110 px"))):
        x0 = 6 * cw + i * 400
        fl = y + ch - 60
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y, 400, ch, bg))
        g1, f1 = _place("hero", dict(arm_l="hip", yaw=0.3), nid(), D, x0 + 120, fl)
        g2, f2 = _place("boss", dict(arm_r="hip", yaw=-0.3), nid(), D, x0 + 280, fl)
        o.append(('<g filter="url(#sheet_sil)">%s%s</g>' if sil else "%s%s") % (g1, g2))
        o.append(_label(x0 + 8, y + 20, nm, 14))
    y += ch
    H = y
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, H, W, H, "".join(o)))
    return svg, W, H


def _raster(svg_path, out_path, w, h, dsf=1):
    import subprocess
    r = subprocess.run(["node", os.path.join(HERE, "raster.js"), svg_path, out_path, str(int(w)), str(int(h)), str(dsf)],
                       cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    sys.stdout.write(r.stdout)
    return r.returncode


# reference panels for `compare`: frame, crop box, head centre (px in the frame), head D (px), background, our cast + pose.
# Head centres / diameters: circle fits on the lower head arc (D = 2.16 * fill radius), see the specs.
COMPARE = [
    ("a/t02.0.jpg", (190, 330, 420, 660), (397, 503), 196, ("#b3301c", "#d9734d", 0.71), "hero",
     dict(expr="smirk", gaze=0.9, arm_r="hip", arm_l="hip", legs="wide", head_roll=3)),
    ("a/t16.0.jpg", (140, 330, 420, 760), (349, 530), 190, ("#8ea4dc", "#6e6a80", 0.80), "boss",
     dict(expr="angry", pitch=-0.9, arm_r="hip", arm_l="down", head_roll=-2)),
    ("a/t55.0.jpg", (60, 60, 560, 760), (336, 291), 350, ("#e98a3d", "#e79a4f", 0.72), "hero",
     dict(expr="excited", arm_r="down", arm_l="down", legs=dict(preset="stand", crouch=0.45))),
    ("a/t46.0.jpg", (0, 150, 720, 560), (172, 409), 333, ("#e0782c", "#e79a4f", 0.92), "hero",
     dict(expr="neutral", yaw=-0.45, arm_r="down", arm_l="down")),
    ("a/t20.0.jpg", (100, 470, 420, 560), (247, 619), 183, ("#4a4f9e", "#e2863f", 0.62), "hero",
     dict(expr="smirk", yaw=0.9, arm_r="forward", arm_l=dict(preset="down", layer="back"), head_roll=4)),
    ("b/t03.0.jpg", (60, 440, 420, 800), (250, 623), 238, ("#8b8496", "#555a86", 0.62), "hero",
     dict(expr="determined", yaw=0.75, head_roll=5, arm_r="point", arm_l=dict(preset="down", layer="back"))),
    ("b/t05.5.jpg", (150, 300, 420, 560), (357, 513), 320, ("#b4354a", "#b4354a", 1.0), "boss",
     dict(expr="unimpressed", yaw=-0.8, tint="#faf8ee", arm_r="down", arm_l="down")),
    ("b/t17.0.jpg", (230, 540, 360, 660), (404, 695), 180, ("#bfd8ee", "#d8d2c0", 0.60), "boss",
     dict(expr="unimpressed", yaw=-0.7, arm_r="behind", arm_l="behind")),
    ("b/t42.0.jpg", (280, 600, 400, 640), (462, 762), 200, ("#8d92c9", "#5d5490", 0.55), "hero",
     dict(expr="determined", yaw=0.8, head_roll=6, lean=8, tint="#c5b8ee", ink="#1e142e", arm_r="point", arm_l="forward", mouth="talk_a")),
]


def build_compare():
    import base64
    pad = 6
    panels = []
    for i, (frame, box, hc, D, bg, cast, pose) in enumerate(COMPARE):
        x0, y0, w, h = box
        b64 = base64.b64encode(open(os.path.join(PROJ, "ref", frame), "rb").read()).decode("ascii")
        ref = ('<svg width="%d" height="%d" viewBox="%d %d %d %d"><image href="data:image/jpeg;base64,%s" x="0" y="0" width="720" height="1280"/></svg>'
               % (w, h, x0, y0, w, h, b64))
        f = figure(cast, pose, "c%d" % i)
        ours = ('<svg x="%d" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="%s"/><rect y="%.1f" width="%d" height="%d" fill="%s"/>'
                '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g></svg>'
                % (w + pad, w, h, w, h, w, h, bg[0], h * bg[2], w, h, bg[1], hc[0] - x0, hc[1] - y0, D, f["svg"]))
        lab = _label(8, h - 10, "ref %s  |  ours: %s, head D = %d px" % (frame, cast, D), 15)
        panels.append((2 * w + pad, h, ref + ours + lab))
    # shelf packing, rows up to 2600 px wide
    maxw = 3000
    rows, cur, cw_ = [], [], 0
    for p in panels:
        if cur and cw_ + p[0] + pad > maxw:
            rows.append(cur)
            cur, cw_ = [], 0
        cur.append(p)
        cw_ += p[0] + pad
    if cur:
        rows.append(cur)
    o = []
    y = 0
    W = 0
    for r in rows:
        x = 0
        rh = max(p[1] for p in r)
        for p in r:
            o.append('<svg x="%d" y="%d" width="%d" height="%d">%s</svg>' % (x, y, p[0], p[1], p[2]))
            x += p[0] + pad
        W = max(W, x)
        y += rh + pad
    H = y
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" viewBox="0 0 %d %d">'
           '<rect width="%d" height="%d" fill="#2a2228"/>%s</svg>' % (W, H, W, H, W, H, "".join(o)))
    return svg, W, H


def _floats(s):
    """(coordinates and sizes, rotate() angles in degrees) found in an SVG string."""
    import re
    ang = [float(x) for x in re.findall(r"rotate\((-?\d+\.\d+)", s)]
    rest = re.sub(r"rotate\((-?\d+\.\d+)", "rotate(", s)
    return [float(x) for x in re.findall(r"-?\d+\.\d+", rest)], ang


def _step(a, b):
    """largest change between two drawings: (max coordinate change in D, max rotation change in degrees), or None if the
    element structure differs."""
    f0, a0 = _floats(a)
    f1, a1 = _floats(b)
    if len(f0) != len(f1) or len(a0) != len(a1):
        return None
    return (max([abs(x - y) for x, y in zip(f0, f1)] or [0.0]),
            max([abs((x - y + 180.0) % 360.0 - 180.0) for x, y in zip(a0, a1)] or [0.0]))


def self_test(verbose=True):
    """determinism, NaN, continuity (a small change of every numeric input must give a small change of every number in
    the SVG: coordinates < 0.05 D, rotations < 3 degrees per step), speed, resolve/lerp consistency."""
    import time
    ok = True
    base_poses = [
        {}, STORY["hero_draw"][1], STORY["boss_rub"][1], STORY["hero_shock"][1],
        dict(yaw=-0.8, lean=-20, head_dx=-0.1, head_roll=-12, expr="talking", arm_l="point", arm_r="behind", legs="step"),
        dict(yaw=0.1, expr="smug", fx=["sweat", "steam", "blush", dict(type="anger_fill", level=0.5)], legs="crouch", arm_r="chin", arm_l="raised"),
        dict(yaw=0.9, legs=dict(preset="step", stride=0.8), arm_r=dict(hand=(0.9, -0.2)), arm_l=dict(hand=(-0.2, 0.9)), prop_r="pointer", prop_l="paper", expr="excited"),
        dict(arm_r=dict(hand=(0.235, 0.54)), arm_l=dict(hand=(5, 5)), legs=dict(foot_l=(-0.2, 9), foot_r=(0.3, 2.0)), squash=(1.2, 0.8), expr="laughing", fx=["tears", "zzz"]),
    ]
    # key, step, sample points
    keys = [("yaw", 0.004, (-1.0, -0.5, -0.06, 0.0, 0.049, 0.2, 0.5, 0.97)), ("pitch", 0.01, (-1.0, 0.0, 0.7)),
            ("head_roll", 0.25, (-20.0, 0.0, 13.0)), ("head_dx", 0.004, (-0.3, 0.0, 0.2)), ("head_dy", 0.004, (-0.3, 0.0, 0.2)),
            ("lean", 0.25, (-20.0, 0.0, 19.4)), ("gaze", 0.02, (-1.0, 0.0, 0.5)), ("t", 0.004, (0.0, 0.33, 0.9))]
    worst = [0.0, None, 0.0, None]
    nstruct = ncheck = 0

    def check(cast, p0, p1, what, lim_xy=0.05, lim_ang=3.0):
        nonlocal ok, nstruct, ncheck
        ncheck += 1
        st = _step(figure(cast, p0, "t")["svg"], figure(cast, p1, "t")["svg"])
        if st is None:
            nstruct += 1
            return
        if st[0] > worst[0]:
            worst[0], worst[1] = st[0], what
        if st[1] > worst[2]:
            worst[2], worst[3] = st[1], what
        if st[0] > lim_xy or st[1] > lim_ang:
            ok = False
            print("JUMP xy %.4f D, angle %.3f deg at %s" % (st[0], st[1], what))

    for cast in ("hero", "boss"):
        for bi, bp in enumerate(base_poses):
            a = figure(cast, bp, "t")
            b = figure(cast, dict(bp), "t")
            if a["svg"] != b["svg"]:
                ok = False
                print("NOT deterministic", cast, bp)
            low = a["svg"].lower()
            if "nan" in low or "inf" in low:
                ok = False
                print("NaN/inf in svg", cast, bp)
            for v in list(a["anchors"].values()) + [a["bbox"][:2], a["bbox"][2:], (a["feet_y"], 0.0)]:
                if not all(abs(c) < 50 for c in v):
                    ok = False
                    print("bad anchor/bbox", cast, bi, v)
            if bi == 7:        # stress pose (hand target exactly on the shoulder, unreachable targets): only NaN / determinism
                continue
            for key, eps, starts in keys:
                for start in starts:
                    p0 = dict(bp)
                    p0[key] = start
                    p1 = dict(p0)
                    p1[key] = start + eps
                    # head_roll / lean are themselves rotations: their own step shows up 1:1 in rotate()
                    check(cast, p0, p1, (cast, bi, key, start), 0.05 if key != "t" else 0.2)
            for key in ("arm_r", "arm_l"):
                for hx, hy in ((0.6, 0.2), (0.9, -0.5), (0.3, 1.25), (2.0, 2.0), (-0.3, 0.9), (0.5, -0.19), (0.0, 0.5), (1.1, 0.43)):
                    p0 = dict(bp)
                    p0[key] = dict(hand=(hx, hy))
                    p1 = dict(bp)
                    p1[key] = dict(hand=(hx + 0.004, hy + 0.003))
                    check(cast, p0, p1, (cast, bi, key, (hx, hy)), 0.05, 6.0)
            for crouch in (0.0, 0.004, 0.1, 0.5):
                p0 = dict(bp)
                p0["legs"] = dict(preset="stand", crouch=crouch)
                p1 = dict(bp)
                p1["legs"] = dict(preset="stand", crouch=crouch + 0.004)
                check(cast, p0, p1, (cast, bi, "crouch", crouch))
            for stride in (-0.5, 0.0, 0.3):
                p0 = dict(bp)
                p0["legs"] = dict(preset="stand", stride=stride)
                p1 = dict(bp)
                p1["legs"] = dict(preset="stand", stride=stride + 0.004)
                check(cast, p0, p1, (cast, bi, "stride", stride))
    # a whole animated move must never pop: sweep a hand through full reach and back, yaw across the front, crouch, lean.
    # (the only singular spot of the rig is a hand target closer than 0.2 D to its own shoulder; the sweep skips it)
    N = 3000
    for cast in ("hero", "boss"):
        prev = None
        shx, shy = CAST[cast]["shoulder"]
        for i in range(N):
            ang = i / float(N) * 2 * math.pi
            hand = (0.55 + 0.75 * math.cos(ang * 3), 0.45 + 0.8 * math.sin(ang * 2))
            p = dict(yaw=1.1 * math.sin(ang * 2), arm_r=dict(hand=hand), arm_l="hip", head_roll=12 * math.sin(ang * 5),
                     lean=10 * math.sin(ang), legs=dict(preset="stand", crouch=0.15 + 0.15 * math.sin(ang * 4), stride=0.5 * math.sin(ang * 3)),
                     expr="smug", prop_r="pencil", fx=["sweat"])
            if math.hypot(hand[0] - shx, hand[1] - shy) < 0.25:
                prev = None
                continue
            cur = figure(cast, p, "t")["svg"]
            if prev is not None:
                st = _step(prev, cur)
                ncheck += 1
                if st is None:
                    nstruct += 1
                elif st[0] > 0.03 or st[1] > 4.0:
                    ok = False
                    print("JUMP in sweep %s frame %d: xy %.4f, angle %.3f" % (cast, i, st[0], st[1]))
            prev = cur
    # speed
    t0 = time.time()
    n = 0
    for i in range(150):
        for cast, bp in (("hero", STORY["hero_draw"][1]), ("boss", STORY["boss_rub"][1])):
            p = dict(bp)
            p["yaw"] = bp.get("yaw", 0) + 0.001 * i
            figure(cast, p, "t")
            n += 1
    ms = (time.time() - t0) / n * 1000.0
    if ms > 10.0:
        ok = False
    # resolve_pose must not change the drawing; lerp_pose endpoints must equal the inputs
    for cast in ("hero", "boss"):
        for bp in base_poses[:7]:
            st = _step(figure(cast, bp, "t")["svg"], figure(cast, resolve_pose(cast, bp), "t")["svg"])
            if st is None or st[0] > 2e-4 or st[1] > 1e-3:
                ok = False
                print("resolve_pose changes the drawing", cast, bp, st)
        for t in (0.0, 1.0):
            st = _step(figure(cast, base_poses[1 if t == 0 else 2], "t")["svg"], figure(cast, lerp_pose(cast, base_poses[1], base_poses[2], t), "t")["svg"])
            if st is None or st[0] > 2e-4:
                ok = False
                print("lerp_pose endpoint differs", cast, t, st)
        prev = None
        for i in range(41):                      # the in-betweens themselves are continuous (away from the t = 0.5 drawing switch)
            if i == 20:
                prev = None
                continue
            cur = figure(cast, lerp_pose(cast, base_poses[1], base_poses[2], i / 40.0), "t")["svg"]
            if prev is not None:
                st = _step(prev, cur)
                if st is not None and (st[0] > 0.08 or st[1] > 8.0):
                    ok = False
                    print("lerp_pose jump", cast, i, st)
            prev = cur
    if verbose:
        print("checks: %d, structure changes (element count differs): %d" % (ncheck, nstruct))
        print("worst coordinate step %.4f D at %s; worst rotation step %.3f deg at %s" % (worst[0], worst[1], worst[2], worst[3]))
        print("speed: %.3f ms per figure() call" % ms)
        print("self-test:", "PASS" if ok else "FAIL")
    return ok


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "sheet"
    if cmd == "sheet":
        svg, W, H = build_sheet()
        p = os.path.join(HERE, "sheet.svg")
        open(p, "w").write(svg)
        print("wrote", p, W, H)
        return _raster(p, os.path.join(HERE, "sheet.png"), W, H)
    if cmd == "compare":
        svg, W, H = build_compare()
        p = os.path.join(HERE, "compare.svg")
        open(p, "w").write(svg)
        print("wrote", p, W, H)
        return _raster(p, os.path.join(HERE, "compare.jpg"), W, H)
    if cmd == "test":
        return 0 if self_test() else 1
    if cmd == "bench":
        import time
        t0 = time.time()
        for i in range(1000):
            figure("hero" if i % 2 else "boss", dict(yaw=math.sin(i * 0.01), head_roll=10 * math.sin(i * 0.03), arm_r=dict(hand=(0.6, 0.2 * math.sin(i * 0.05)))), "b")
        print("%.3f ms per figure() call" % ((time.time() - t0)))
        return 0
    print("usage: python3 puppet.py sheet|compare|test|bench")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
