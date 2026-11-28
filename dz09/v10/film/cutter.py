"""cutter.py -- the drawn battery cutter as a two-handed tool (no bpy).

    prop_svg(P, sp)          the drawing: rear D-handle at the origin, body along +y, fore grip with the far glove on it
                             at y = FORE, battery box, collar, jaws (P["jaw"] 1 open .. 0 shut)
    hold(sp, view, s, grip, tilt, scale)  ->  dict(arm_n, arm_f, prop_n) : near hand on the rear handle at `grip`
                             (relative to the near shoulder, +x = the way he faces), the tool tilted `tilt` degrees from
                             straight down toward his facing side, the far arm reaching to the fore grip.
"""
import math, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(HERE, "..", "..", "v8", "cast"))
import draw8 as D

FORE = 0.27          # fore grip along the body (prop units)
SCALE = 1.25


def prop_svg(P, sp=None):
    f = D.f; INK = D.INK
    bars = int(P.get("bars", 3)); wet = P.get("wet", False)
    org = "#ee7a1f" if not wet else "#d0621a"
    o = D.path("M-0.19 -0.05 C-0.30 -0.32 0.23 -0.37 0.17 -0.07", "none", INK, 0.10)
    o += D.path("M-0.19 -0.05 C-0.30 -0.32 0.23 -0.37 0.17 -0.07", "none", "#2a2a2a", 0.05)
    o += '<rect x="-0.12" y="-0.10" width="0.24" height="0.80" rx="0.07" fill="%s" stroke="%s" stroke-width="0.03"/>' % (org, INK)
    o += '<rect x="-0.10" y="-0.06" width="0.055" height="0.70" rx="0.027" fill="#fbc48d" opacity="0.55"/>'
    o += '<rect x="-0.12" y="0.045" width="0.24" height="0.05" fill="#f4f2ec" stroke="%s" stroke-width="0.016"/>' % INK
    # battery box with 3 bars
    o += '<rect x="-0.10" y="0.43" width="0.20" height="0.21" rx="0.02" fill="#151515" stroke="%s" stroke-width="0.02"/>' % INK
    colr = {3: "#3ee05a", 2: "#f2d22e", 1: "#ff3b30", 0: "#333"}[max(0, min(3, bars))]
    for k in range(3):
        on = (2 - k) < bars
        o += '<rect x="-0.07" y="%s" width="0.14" height="0.044" rx="0.008" fill="%s"/>' % (f(0.452 + k * 0.060), colr if on else "#3a3a3a")
    o += '<rect x="-0.14" y="0.68" width="0.28" height="0.11" rx="0.03" fill="#222" stroke="%s" stroke-width="0.024"/>' % INK
    o += D.ell(0, 0.84, 0.06, 0.06, "#bfc4ca", INK, 0.02)
    close = (1.0 - float(P.get("jaw", 1.0))) * 13.0
    for side in (-1, 1):
        jaw = [(side * 0.02, 0.80), (side * 0.15, 0.88), (side * 0.185, 1.08), (side * 0.10, 1.25), (side * 0.045, 1.19), (side * 0.09, 1.04),
               (side * 0.04, 0.90)]
        j = D.path(D.smooth_d(jaw, True, 0.25), "#b9bfc6", INK, 0.026)
        j += D.path(D.pts_d([(side * 0.065, 0.92), (side * 0.14, 1.06), (side * 0.095, 1.17)], False), "none", "#dfe3e8", 0.016)
        o += D.g(j, "rotate(%s 0 0.84)" % f(side * close))
    o += D.ell(0, 0.84, 0.03, 0.03, "#555")
    if P.get("fore", True):
        # the fore handle (a black bar across the body) and the far glove closed over it
        up = float(P.get("up", 1.0))                         # which side of the tool is "up" on screen (+1 / -1 in x)
        o += D.poly_stroke([(-0.20, FORE), (0.20, FORE)], INK, 0.10) + D.poly_stroke([(-0.20, FORE), (0.20, FORE)], "#2a2a2a", 0.055)
        col = (sp or {}).get("col", {}).get("glove", "#2b2b30") if (sp or {}).get("glove") else (sp or {}).get("skin", "#f1efe8")
        ink = (sp or {}).get("ink", INK); bw = (sp or {}).get("body_ink", 0.03)
        gx = up * 0.035
        o += D.ell(gx, FORE, 0.185, 0.135, col, ink, bw)
        o += D.ell(gx - up * 0.13, FORE - 0.085, 0.06, 0.075, col, ink, bw * 0.9, rot=up * 25)          # thumb, hooked under
        o += D.ell(gx, FORE, 0.165, 0.115, col)
        for k in range(3):
            y = FORE - 0.06 + k * 0.06
            o += D.line((gx + up * 0.07, y), (gx + up * 0.165, y), D.shade(col, 0.6) if (sp or {}).get("glove") else ink, 0.014)
        o += '<rect x="%s" y="%s" width="0.06" height="0.22" rx="0.02" fill="%s" stroke="%s" stroke-width="0.016"/>' % (
            f(gx - up * 0.20 - 0.03), f(FORE - 0.11), D.shade(col, 0.3), ink)                             # cuff
    return D.g(o, "translate(%s %s) rotate(%s)%s" % (f(P["at"][0]), f(P["at"][1]), f(P.get("angle", 0.0)),
                                                     " scale(%s)" % f(P["scale"]) if P.get("scale") else ""))


def hold(sp, view, s, grip=(0.30, 0.74), tilt=62.0, scale=SCALE, jaw=1.0, bars=3, wet=True):
    """two-handed carry for the q / side drawings."""
    la, lf = sp["upper_arm"], sp["fore_arm"]
    tgt = (grip[0] * s, grip[1])
    el, wr = D.ik2((0.0, 0.0), tgt, la, lf, s)
    dv = D.nrm(D.sub(wr, el))
    at = D.add(wr, dv, sp["hand"] * 0.45)                    # where draw8 puts the cutter's origin
    a = math.radians(tilt)
    ax = (s * math.sin(a), math.cos(a))                      # the tool's long axis on the drawing
    fore = (at[0] + ax[0] * FORE * scale, at[1] + ax[1] * FORE * scale)
    th = math.radians(D.BODY_YAW[view])
    a_half = math.sqrt((sp["chest"] / 2 * math.cos(th)) ** 2 + (sp["chest"] / 2 * 0.62 * math.sin(th)) ** 2)
    dsh = (s * a_half * ((0.35 + 0.25) if view == "side" else (0.55 + 0.62)), 0.03)       # near shoulder - far shoulder
    # the far wrist stops short of the fore grip along its own forearm, so the drawn glove on the tool covers the hand
    fx, fy = dsh[0] + fore[0], dsh[1] + fore[1]
    L = math.hypot(fx, fy); reach = la + lf - 0.02
    if L > reach: fx, fy = fx * reach / L, fy * reach / L
    return dict(arm_n=dict(hand=grip, elbow=None, hand_shape="grip"),
                arm_f=dict(hand=(fx * s, fy), elbow=None, hand_shape="grip"),
                prop_n=dict(type="cutter", bars=bars, wet=wet, jaw=round(jaw, 2), angle=round(-s * tilt, 2), scale=scale, two=True,
                            up=-s if tilt > 0 else s))
