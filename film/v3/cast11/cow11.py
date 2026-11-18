# -*- coding: utf-8 -*-
"""cow11.py -- "Blossom", the Gloucester-ish cow of film 11, as a 2D puppet with the same figure() contract as the human cast
(svg / feet_y / bbox / anchors in D units, y down, uid-prefixed ids).  Side view, facing screen-right (pose mirror=True: left).

Frame: origin = the middle of the barrel, hooves (soles) at y = FEET_Y = 1.82, back at y = -0.86 (2.68 D above the floor), rump at
x = -1.9, chest at x = +1.45, the head carried out to x = +2.9.  1 D = the head diameter of the human cast (a milkmaid is 3 D tall).

Pose keys (all optional, numbers clamped, garbage falls back to the default):
  head_turn  -0.4 .. 1   0 = head forward and a little down; 1 = turned down and back towards the flank (looks at the milkmaid)
  head_down  -0.5 .. 1   extra nod (grazing / lowing)
  ear        -1 .. 1     near ear flick (rotation about its base); animate with a quick +1 / -0.3 / 0 over ~6 frames
  tail       -1 .. 1     tail swish (the tail bends progressively: -1 = tuft forward, +1 = tuft swung back); animate with a sine
  chew       phase       setting it turns the chewing on: jaw and muzzle move once per unit of phase (pass frame / 12.0); None = mouth shut
  chew_amp   0 .. 1.5    chewing amplitude (default 1)
  blink      0, 1, 2     as the humans
  mirror, tint, ink, squash   as the humans
"""
import math

import puppet as P

FEET_Y = 1.82
_clamp, _num, _smooth = P._clamp, P._num, P._smooth

BROWN = dict(light="#b9764a", base="#94562f", dark="#5e3320")
WHITE = dict(light="#fffaf0", base="#f2e9d6", dark="#cdbf9f")
PINK = dict(light="#f9cdc0", base="#f0b0a0", dark="#d58878")
HOOF = "#4a3a38"
HORN = dict(base="#efdcb0", tip="#9a7648")

COW_CAST = dict(
    build="stout", seed=91.3, torso_w=1.0, torso_h=1.0, profile=((0.5, 0.02), (0.8, 0.1), (0.93, 0.24), (0.99, 0.4), (1.0, 0.58), (0.98, 0.76), (0.92, 0.86), (0.72, 0.95), (0.4, 0.995)),
    shift_pow=1.2, shoulder=(0.4, 0.44), arm=0.76, hip_x=0.17, leg=1.2, stance=0.06, wide=0.26, limb_w=0.066, eye_y=0.0, brow="stroke", brow_th=0.06, mouth="frown",
    hat="newsboy", hat_tilt=0.0, ear_pencil=False, hair=dict(color="#94562f", front=0.0, grow=0.0), costume="frock7",
    colors=dict(base="#94562f", dark="#5e3320", lapel="#94562f", vest="#f2e9d6", shirt="#f2e9d6", pants="#5e3320"),
    sleeve=dict(color="#94562f", cuff="#94562f", dark="#5e3320", len=0.8, w=0.2), shorts=dict(color="#5e3320", cuff="#5e3320", dark="#3a2018", len=0.9, w=0.14),
    boots=dict(color="#4a3a38", cuff="#4a3a38", h=0.08, toe=0.1),
    hat_style="bare7", hat_colors=dict(light="#b9764a", base="#94562f", dark="#5e3320", shine="#d9976a"), cow11=True)


def _ink(k, d, fill, sw=0.030, extra=""):
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.4f" stroke-linejoin="round" stroke-linecap="round"%s/>' % (d, fill, k.ink, sw, extra)


def _grad(k, name, c, vertical=True):
    k.defs.append('<linearGradient id="%s_%s" gradientUnits="objectBoundingBox" x1="0" y1="0" x2="%d" y2="%d"><stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (k.uid, name, 0 if vertical else 1, 1 if vertical else 0, k.c(c["light"]), k.c(c["base"]), k.c(c["dark"])))
    return "url(#%s_%s)" % (k.uid, name)


def _leg(k, pts, hoof_x, col, dark=False):
    """a cow leg: a smooth tapered outline through pts (outer edge going down, then the inner edge back up) and a cloven hoof."""
    d = P._smooth_closed(pts)
    s = _ink(k, d, k.c(col), 0.030)
    return s


def _bend(pts, a, o):
    """rotate pts about o by a (radians)."""
    c, s = math.cos(a), math.sin(a)
    return [(o[0] + (x - o[0]) * c - (y - o[1]) * s, o[1] + (x - o[0]) * s + (y - o[1]) * c) for (x, y) in pts]


def _tail(k, sw):
    """a tail from the tail head that bends progressively with sw (-1 .. 1); ends in a tuft."""
    root = (-1.83, -0.56)
    pts = [root]
    a = math.radians(98 + 4)                 # initial direction: down (SVG angle 90 = down), a hair backwards
    x, y = root
    n = 8
    for i in range(n):
        a += math.radians(-4) + sw * math.radians(9.5)
        x += 0.17 * math.cos(a)
        y += 0.17 * math.sin(a)
        pts.append((x, y))
    d = P._smooth_open(pts)
    o = ['<path d="%s" fill="none" stroke="%s" stroke-width="0.105" stroke-linecap="round"/>' % (d, k.ink)]
    o.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.062" stroke-linecap="round"/>' % (d, k.c(BROWN["base"])))
    ex, ey = pts[-1]
    ang = math.degrees(a) - 90
    tuft = ('<g transform="translate(%.4f %.4f) rotate(%.2f)"><path d="M0,-0.04 C0.13,0.04 0.14,0.22 0.03,0.36 C0.01,0.40 -0.01,0.40 -0.03,0.36 C-0.14,0.22 -0.13,0.04 0,-0.04 Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
            '<path d="M-0.03,0.02 Q-0.05,0.17 -0.02,0.32 M0.04,0.02 Q0.06,0.17 0.03,0.32" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round"/></g>'
            % (ex, ey, ang, k.c(WHITE["base"]), k.ink, k.c(WHITE["dark"])))
    k.ext.append((ex, ey + 0.34, 0.1))
    return "".join(o) + tuft, (ex + 0.36 * -math.sin(math.radians(ang)) * 0 + 0.0, ey + 0.36)


def _head(k, jaw, ear, blink, horn=True):
    """the head in its own frame: centre (0, 0), muzzle to +x; returns (svg, anchors dict)."""
    o = []
    # far ear (behind), far horn
    def ear_shape(rot, col, inner, sc=1.0):
        d = "M0,-0.05 C-0.10,-0.22 -0.36,-0.28 -0.50,-0.22 C-0.48,-0.08 -0.30,0.06 0,0.06 Z"
        return ('<g transform="rotate(%.2f) scale(%.3f)"><path d="%s" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round"/>'
                '<path d="M-0.06,-0.03 C-0.14,-0.14 -0.30,-0.19 -0.40,-0.17 C-0.38,-0.08 -0.26,0.01 -0.06,0.03 Z" fill="%s"/></g>' % (rot, sc, d, k.c(col), k.ink, k.c(inner)))
    o.append('<g transform="translate(-0.12 -0.30)">%s</g>' % ear_shape(-8 - 0.6 * ear, BROWN["dark"], "#d28f7e", 0.95))
    if horn:
        o.append('<path d="M-0.04,-0.36 C-0.06,-0.50 -0.02,-0.58 0.06,-0.62 C0.04,-0.52 0.07,-0.44 0.07,-0.36 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c(HORN["base"]), k.ink))
    # lower jaw (behind the head so the mouth opens below the muzzle)
    jx, jy = jaw
    o.append('<path d="M0.04,0.26 L0.62,0.27 Q0.74,0.28 %.3f,%.3f Q0.64,%.3f 0.48,%.3f L0.12,%.3f Z" fill="%s" stroke="%s" stroke-width="0.026" stroke-linejoin="round" transform="translate(%.3f %.3f)"/>'
             % (0.70, 0.36, 0.48, 0.45, 0.42, k.c(PINK["base"]), k.ink, jx, jy))
    if jy > 0.012:
        o.append('<path d="M0.12,0.30 L0.64,0.31 L0.62,%.3f L0.14,%.3f Z" fill="%s"/>' % (0.31 + jy, 0.31 + jy, k.c("#7a2f34")))
    # skull
    skull = [(-0.34, -0.06), (-0.30, -0.30), (-0.08, -0.43), (0.22, -0.34), (0.50, -0.14), (0.74, 0.06), (0.80, 0.22), (0.72, 0.34), (0.44, 0.38), (0.10, 0.38), (-0.20, 0.26)]
    g = _grad(k, "hd", BROWN)
    o.append(_ink(k, P._smooth_closed(skull), g, 0.032))
    # white blaze
    blaze = [(0.02, -0.40), (0.20, -0.33), (0.46, -0.14), (0.72, 0.07), (0.76, 0.20), (0.60, 0.13), (0.38, 0.0), (0.14, -0.13), (-0.04, -0.28)]
    o.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(blaze), k.c(WHITE["base"])))
    # muzzle (pink) with nostril
    muz = [(0.56, 0.04), (0.74, 0.07), (0.82, 0.22), (0.74, 0.34), (0.54, 0.36), (0.50, 0.20)]
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (P._smooth_closed(muz), k.c(PINK["base"]), k.ink))
    o.append('<ellipse cx="0.74" cy="0.14" rx="0.032" ry="0.048" fill="#7a3a3a" transform="rotate(-22 0.74 0.14)"/>')
    o.append('<path d="M0.56,0.31 Q0.66,0.34 0.76,0.31" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round"/>' % k.ink)
    o.append('<path d="M0.62,0.06 Q0.70,0.04 0.76,0.10" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.8"/>' % k.c(PINK["light"]))
    # eye
    if blink >= 2:
        o.append('<path d="M0.04,-0.10 Q0.12,-0.06 0.22,-0.11" fill="none" stroke="%s" stroke-width="0.030" stroke-linecap="round"/>' % k.ink)
    else:
        ry = 0.058 if blink == 0 else 0.026
        o.append('<ellipse cx="0.14" cy="-0.10" rx="0.074" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.018"/>' % (ry, k.c("#2a1c1c"), k.ink))
        if blink == 0:
            o.append('<circle cx="0.12" cy="-0.12" r="0.020" fill="#fff6e8"/>')
        o.append('<path d="M0.02,-0.17 Q0.14,-0.22 0.27,-0.14" fill="none" stroke="%s" stroke-width="0.020" stroke-linecap="round"/>' % k.c(BROWN["dark"]))
    # near ear and horn
    o.append('<g transform="translate(-0.20 -0.22)">%s</g>' % ear_shape(-4 + 26 * ear, BROWN["base"], "#f2b0a2", 1.08))
    if horn:
        o.append('<path d="M-0.20,-0.30 C-0.26,-0.42 -0.24,-0.52 -0.16,-0.58 C-0.15,-0.48 -0.10,-0.40 -0.08,-0.32 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (k.c(HORN["base"]), k.ink))
        o.append('<path d="M-0.17,-0.52 L-0.16,-0.58 L-0.22,-0.50 Z" fill="%s"/>' % k.c(HORN["tip"]))
    # cheek shading
    o.append('<path d="M-0.18,0.10 Q0.0,0.30 0.30,0.34" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.7"/>' % k.c(BROWN["dark"]))
    return "".join(o)


def cow_svg(k, pose):
    ht = _clamp(_num(pose.get("head_turn")), -0.4, 1.0)
    hd = _clamp(_num(pose.get("head_down")), -0.5, 1.0)
    ear = _clamp(_num(pose.get("ear")), -1.0, 1.0)
    sw = _clamp(_num(pose.get("tail")), -1.0, 1.0)
    chew = pose.get("chew")
    amp = _clamp(_num(pose.get("chew_amp"), 1.0), 0.0, 1.5)
    blink = int(_clamp(round(_num(pose.get("blink"))), 0, 2))
    o, an = [], {}
    # --- tail (behind everything)
    tsvg, ttip = _tail(k, sw)
    o.append(tsvg)
    # --- far legs (darker)
    dark = P._shade(BROWN["base"], 0.80)
    far_f = [(1.28, 0.45), (1.50, 0.50), (1.50, 1.12), (1.46, 1.32), (1.44, 1.66), (1.48, 1.74), (1.52, 1.80), (1.26, 1.80), (1.28, 1.68), (1.27, 1.30), (1.22, 1.10)]
    far_h = [(-1.22, 0.30), (-0.88, 0.45), (-0.96, 1.00), (-1.02, 1.30), (-0.99, 1.66), (-0.97, 1.74), (-0.93, 1.80), (-1.18, 1.80), (-1.16, 1.68), (-1.18, 1.38), (-1.26, 1.12)]
    for pts in (far_f, far_h):
        o.append(_ink(k, P._smooth_closed(pts), k.c(dark), 0.028))
    for (x0, x1) in ((1.26, 1.52), (-1.18, -0.93)):
        o.append('<path d="M%.3f,1.66 L%.3f,1.66 L%.3f,1.80 L%.3f,1.80 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (x0 + 0.01, x1 - 0.01, x1 + 0.0, x0 - 0.0, k.c(HOOF), k.ink))
    # --- body
    body = [(-1.88, -0.40), (-1.66, -0.74), (-1.10, -0.76), (-0.40, -0.72), (0.30, -0.78), (0.90, -0.88), (1.40, -0.74), (1.90, -0.56), (2.25, -0.45),
            (2.30, -0.02), (2.05, 0.18), (1.78, 0.38), (1.52, 0.62), (1.20, 0.82), (0.50, 0.90), (-0.30, 0.88), (-0.95, 0.74), (-1.50, 0.30), (-1.92, -0.04)]
    bd = P._smooth_closed(body)
    gid = "%s_bd" % k.uid
    k.defs.append('<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="0" y1="-0.9" x2="0" y2="0.9"><stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
                  % (gid, k.c(BROWN["light"]), k.c(BROWN["base"]), k.c(BROWN["dark"])))
    k.defs.append('<clipPath id="%s_bc"><path d="%s"/></clipPath>' % (k.uid, bd))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.034" stroke-linejoin="round"/>' % (bd, "url(#%s)" % gid, k.ink))
    # white markings, clipped to the body
    wh = []
    belly = [(-1.9, 0.40), (-1.2, 0.30), (-0.5, 0.42), (0.2, 0.36), (0.9, 0.44), (1.5, 0.30), (2.0, 0.06), (2.4, 0.2), (2.4, 1.2), (-1.9, 1.2)]
    wh.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(belly), k.c(WHITE["base"])))
    patch = [(-0.55, -0.60), (-0.1, -0.78), (0.45, -0.66), (0.62, -0.30), (0.40, -0.02), (-0.05, 0.04), (-0.50, -0.14), (-0.70, -0.38)]
    wh.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(patch), k.c(WHITE["base"])))
    p2 = [(-1.62, -0.52), (-1.28, -0.62), (-1.12, -0.36), (-1.34, -0.18), (-1.70, -0.24)]
    wh.append('<path d="%s" fill="%s"/>' % (P._smooth_closed(p2), k.c(WHITE["base"])))
    o.append('<g clip-path="url(#%s_bc)">%s' % (k.uid, "".join(wh)))
    # a few brown spots in the white belly for a hand-painted look, soft shading under the back
    o.append('<path d="M-0.35,0.62 q0.12,-0.10 0.25,-0.03 q0.04,0.12 -0.12,0.14 q-0.14,-0.01 -0.13,-0.11 Z" fill="%s"/>' % k.c(BROWN["light"]))
    o.append('<path d="M-1.9,0.74 Q-0.6,1.00 0.9,0.98 Q1.6,0.9 2.2,0.4 L2.4,1.2 L-1.9,1.2 Z" fill="%s" opacity="0.35"/>' % k.c(WHITE["dark"]))
    o.append('<path d="M-1.8,-0.66 Q-0.2,-0.84 1.0,-0.90 L1.0,-0.78 Q-0.2,-0.74 -1.8,-0.52 Z" fill="%s" opacity="0.45"/>' % k.c(BROWN["light"]))
    o.append('</g>')
    # shoulder / hip definition lines
    o.append('<path d="M0.95,-0.52 Q1.12,-0.10 1.00,0.34" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>' % k.c(BROWN["dark"]))
    o.append('<path d="M-1.30,-0.52 Q-1.12,-0.02 -1.30,0.40" fill="none" stroke="%s" stroke-width="0.016" stroke-linecap="round" opacity="0.7"/>' % k.c(BROWN["dark"]))
    # ribs
    o.append('<path d="M-0.10,-0.35 Q0.0,0.0 -0.10,0.30 M0.20,-0.38 Q0.30,0.0 0.20,0.30" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.5"/>' % k.c(BROWN["dark"]))
    # --- udder (between the hind legs, on the belly), teats hanging
    ud = [(-1.14, 0.64), (-0.80, 0.70), (-0.34, 0.68), (-0.28, 0.86), (-0.46, 0.99), (-0.92, 1.00), (-1.16, 0.88)]
    # far teats first
    for tx in (-0.40, -0.80):
        o.append('<path d="M%.3f,0.90 L%.3f,1.10 Q%.3f,1.15 %.3f,1.10 L%.3f,0.90 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (tx - 0.04, tx - 0.035, tx, tx + 0.035, tx + 0.04, k.c(PINK["dark"]), k.ink))
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="0.030" stroke-linejoin="round"/>' % (P._smooth_closed(ud), k.c(PINK["base"]), k.ink))
    o.append('<path d="M-1.02,0.76 Q-0.80,0.74 -0.52,0.78" fill="none" stroke="%s" stroke-width="0.014" stroke-linecap="round" opacity="0.8"/>' % k.c(PINK["light"]))
    o.append('<path d="M-0.84,0.78 Q-0.78,0.88 -0.80,0.96 M-0.62,0.80 Q-0.56,0.90 -0.58,0.96" fill="none" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.7"/>' % k.c(PINK["dark"]))
    for tx in (-0.52, -0.90):
        o.append('<path d="M%.3f,0.94 L%.3f,1.16 Q%.3f,1.22 %.3f,1.16 L%.3f,0.94 Z" fill="%s" stroke="%s" stroke-width="0.024" stroke-linejoin="round"/>' % (tx - 0.050, tx - 0.040, tx, tx + 0.040, tx + 0.050, k.c(PINK["base"]), k.ink))
        o.append('<path d="M%.3f,1.00 L%.3f,1.12" stroke="%s" stroke-width="0.010" stroke-linecap="round" opacity="0.9"/>' % (tx - 0.020, tx - 0.020, k.c(PINK["light"])))
    # --- near legs
    near_f = [(0.72, 0.40), (1.14, 0.46), (1.12, 1.10), (1.08, 1.32), (1.06, 1.66), (1.10, 1.74), (1.14, 1.80), (0.86, 1.80), (0.88, 1.68), (0.88, 1.34), (0.82, 1.10)]
    near_h = [(-1.78, 0.10), (-1.30, 0.34), (-1.24, 0.80), (-1.34, 1.12), (-1.46, 1.36), (-1.44, 1.66), (-1.40, 1.74), (-1.36, 1.80), (-1.62, 1.80), (-1.66, 1.68), (-1.68, 1.38), (-1.74, 1.14), (-1.84, 0.70)]
    cols = (k.c(BROWN["base"]), k.c(BROWN["base"]))
    for pts, c in ((near_f, cols[0]), (near_h, cols[1])):
        o.append(_ink(k, P._smooth_closed(pts), c, 0.030))
    # white socks on the lower legs
    o.append('<path d="M0.875,1.36 L1.065,1.36 L1.06,1.66 L1.10,1.74 L1.14,1.80 L0.86,1.80 L0.88,1.68 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c(WHITE["base"]), k.ink))
    o.append('<path d="M-1.46,1.36 L-1.69,1.38 L-1.66,1.68 L-1.62,1.80 L-1.36,1.80 L-1.40,1.74 L-1.44,1.66 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (k.c(WHITE["base"]), k.ink))
    for (x0, x1) in ((0.86, 1.14), (-1.62, -1.36)):
        o.append('<path d="M%.3f,1.72 L%.3f,1.72 L%.3f,1.80 L%.3f,1.80 Z" fill="%s" stroke="%s" stroke-width="0.020" stroke-linejoin="round"/>' % (x0 + 0.02, x1 - 0.02, x1, x0, k.c(HOOF), k.ink))
    # knee and hock marks
    o.append('<path d="M0.88,1.10 Q1.0,1.16 1.12,1.10 M-1.70,1.12 Q-1.52,1.20 -1.30,1.10" fill="none" stroke="%s" stroke-width="0.012" stroke-linecap="round" opacity="0.6"/>' % k.c(BROWN["dark"]))
    # --- head
    a_turn = 14.0 + 66.0 * ht + 34.0 * hd
    J = (2.10, -0.14)
    ra = math.radians(a_turn)
    L0 = (0.78, 0.24)
    Hc = (J[0] + L0[0] * math.cos(ra) - L0[1] * math.sin(ra) - 0.30 * ht, J[1] + L0[0] * math.sin(ra) + L0[1] * math.cos(ra) + 0.10 * hd)
    jaw = (0.0, 0.0)
    if chew is not None and amp > 0.0:
        ph = _num(chew, 0.0) * 2 * math.pi
        s = math.sin(ph)
        jaw = (0.035 * amp * math.sin(ph + 1.2), 0.060 * amp * max(0.0, s) + 0.008 * amp)
    o.append('<g transform="translate(%.4f %.4f) rotate(%.3f)">%s</g>' % (Hc[0], Hc[1], a_turn, _head(k, jaw, ear, blink)))
    # head extents
    for (x, y) in ((-0.34, -0.6), (0.84, -0.46), (0.84, 0.50), (-0.5, 0.5)):
        c, s_ = math.cos(ra), math.sin(ra)
        k.ext.append((Hc[0] + x * c - y * s_, Hc[1] + x * s_ + y * c, 0.04))
    c, s_ = math.cos(ra), math.sin(ra)

    def HL(x, y):
        return (Hc[0] + x * c - y * s_, Hc[1] + x * s_ + y * c)
    an["head"] = Hc
    an["mouth"] = HL(0.70, 0.31)
    an["muzzle"] = HL(0.80, 0.20)
    an["eye"] = HL(0.14, -0.10)
    an["ear"] = HL(-0.20, -0.22)
    # extents of the body
    for (x, y, r) in ((-2.0, -0.4, 0.1), (2.3, 0.0, 0.1), (0.0, -0.9, 0.1), (-1.9, 1.8, 0.05), (1.5, 1.8, 0.05), (ttip[0], ttip[1], 0.1)):
        k.ext.append((x, y, r))
    an.update(feet=(-0.30, FEET_Y), udder=(-0.72, 0.85), teat_r=(-0.52, 1.20), teat_l=(-0.90, 1.20), back=(0.0, -0.80), withers=(0.90, -0.88),
              flank=(-0.60, 0.20), tail_tip=ttip, tail_root=(-1.83, -0.56), pail_spot=(-0.72, FEET_Y), milker_feet=(-0.15, FEET_Y + 0.10),
              hip=(-0.30, 0.0), shoulder_r=(0.95, -0.4), shoulder_l=(0.95, -0.4), hand_r=(0.95, 0.2), hand_l=(0.95, 0.2), head_top=(Hc[0], Hc[1] - 0.6), hat_top=(Hc[0], Hc[1] - 0.7),
              chest=(1.4, 0.2), knee_r=(0.95, 1.1), knee_l=(-1.5, 1.1), foot_r=(1.0, FEET_Y), foot_l=(-1.5, FEET_Y), eye_r=an["eye"], eye_l=an["eye"],
              prop_tip_r=(0.95, 0.2), prop_tip_l=(0.95, 0.2), elbow_r=(0.95, 0.5), elbow_l=(0.95, 0.5))
    return "".join(o), an


def _mirror_pt(p):
    return (-p[0], p[1])


def cow_figure(pose=None, uid="p"):
    """figure()-compatible: {'svg', 'feet_y', 'bbox', 'anchors'} for Blossom (see the module docstring for the pose keys)."""
    if not isinstance(pose, dict):
        pose = {}
    ink = pose.get("ink")
    ink = ink if P._is_hex(ink) else P.INK
    tn = pose.get("tint")
    k = P._Ctx(str(uid), ink, P._rgb(tn.lstrip("#")) if P._is_hex(tn) else None)
    body, an = cow_svg(k, pose)
    sq = pose.get("squash")
    if isinstance(sq, (tuple, list)) and len(sq) >= 2:
        sx, sy = _clamp(_num(sq[0], 1.0), 0.3, 2.5), _clamp(_num(sq[1], 1.0), 0.3, 2.5)
    else:
        sx = sy = _clamp(_num(sq, 1.0), 0.3, 2.5)
    mir = bool(pose.get("mirror"))
    x0 = min(e[0] - e[2] for e in k.ext)
    x1 = max(e[0] + e[2] for e in k.ext)
    y0 = min(e[1] - e[2] for e in k.ext)
    y1 = max(e[1] + e[2] for e in k.ext)
    y1 = max(y1, FEET_Y + 0.03)
    # squash about the barrel centre; the soles stay at feet_y * sy
    tr = "scale(%.4f %.4f)" % ((-sx if mir else sx), sy)
    defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
    svg = '<g id="%s_fig" transform="%s">%s%s</g>' % (uid, tr, defs, body)
    fx = -1.0 if mir else 1.0
    anchors = {n: (v[0] * sx * fx, v[1] * sy) for n, v in an.items()}
    if mir:
        for n in list(anchors):
            if n.endswith("_r") or n.endswith("_l"):
                m = n[:-2] + ("_l" if n.endswith("_r") else "_r")
                anchors[n] = (an[m][0] * -sx, an[m][1] * sy)
    bx = sorted((x0 * sx * fx, x1 * sx * fx))
    return dict(svg=svg, feet_y=FEET_Y * sy, bbox=(bx[0], y0 * sy, bx[1], y1 * sy), anchors=anchors)
