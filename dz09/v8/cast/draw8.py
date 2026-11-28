"""draw8.py -- the DEAD ZONE 09 cast drawn by code as separate SVG layers, in the character sheet's style.

Pure Python (stdlib only).  Units: D = bare head width including the outline.  Figure frame: x right, y DOWN,
origin on the ground between the feet (the soles of a standing figure are at y = 0).

    fig = build(spec_or_name, pose)          # -> dict(layers=[...], anchors={...}, bbox, spec, view, s)
    fig["layers"]  back to front: dict(name, svg, z (gap units, + toward the viewer), kind, round)
    flat_svg(fig)                            # every layer on one sheet
    doc(fragment, canvas, ppd, bg=None)      # full SVG document, canvas (x0, y0, x1, y1) in D
    SPECS["kong" | "kong_wet" | "crew" | "crew_wet" | "driver"]  and  extras(n, seed) -> list of specs

Pose keys: view (front | q | side), s (+1 faces screen-right, -1 screen-left), expr, mouth (level 0..1 or
(shape, level)), blink (0 open, 1 half, 2 closed), gaze (dx, dy), lean (deg, + = forward), head (yaw_extra deg,
tilt deg, dx, dy), arm_n / arm_f (or arm_r / arm_l in front view): preset name or dict(hand=(x, y), elbow=+1/-1, hand_shape),
legs: preset name or dict(foot_n=(x, y), foot_f=(x, y), hip=(dx, dy), lift_n, lift_f), prop_n / prop_f / prop_r / prop_l:
dict(type="cutter" | "phone" | "umbrella" | "bag" | "box", angle, bars, screen).
Near/far: in q/side views facing right (s=+1) the near limbs are the character's LEFT limbs.
"""
import math, random, re

# ------------------------------------------------------------------------------------------------ basic SVG helpers
INK = "#0e0e0d"


def f(v):
    s = "%.4f" % v
    s = s.rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def pts_d(pts, close=True):
    s = "M" + " L".join("%s %s" % (f(x), f(y)) for x, y in pts)
    return s + (" Z" if close else "")


def smooth_d(pts, close=True, k=0.5):
    """Catmull-Rom through the points -> cubic Bezier path."""
    n = len(pts)
    if n < 3:
        return pts_d(pts, close)
    P = list(pts)
    out = "M%s %s" % (f(P[0][0]), f(P[0][1]))
    rng = range(n) if close else range(n - 1)
    for i in rng:
        p0 = P[(i - 1) % n] if (close or i > 0) else P[i]
        p1 = P[i]
        p2 = P[(i + 1) % n]
        p3 = P[(i + 2) % n] if (close or i + 2 < n) else P[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 3, p1[1] + (p2[1] - p0[1]) * k / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 3, p2[1] - (p3[1] - p1[1]) * k / 3)
        out += " C%s %s %s %s %s %s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p2[0]), f(p2[1]))
    return out + (" Z" if close else "")


def path(d, fill="none", stroke=None, sw=0.0, extra=""):
    s = '<path d="%s" fill="%s"' % (d, fill)
    if stroke:
        s += ' stroke="%s" stroke-width="%s" stroke-linejoin="round" stroke-linecap="round"' % (stroke, f(sw))
    return s + extra + "/>"


def ell(cx, cy, rx, ry, fill="none", stroke=None, sw=0.0, rot=0.0):
    s = '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"' % (f(cx), f(cy), f(max(rx, 1e-4)), f(max(ry, 1e-4)), fill)
    if stroke:
        s += ' stroke="%s" stroke-width="%s"' % (stroke, f(sw))
    if rot:
        s += ' transform="rotate(%s %s %s)"' % (f(rot), f(cx), f(cy))
    return s + "/>"


def line(p0, p1, col, w, cap="round"):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="%s" stroke-linecap="%s" fill="none"/>' % (
        f(p0[0]), f(p0[1]), f(p1[0]), f(p1[1]), col, f(w), cap)


def poly_stroke(pts, col, w, cap="round", join="round"):
    return '<path d="%s" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="%s" fill="none"/>' % (
        pts_d(pts, False), col, f(w), cap, join)


def g(inner, tr=None):
    return "<g%s>%s</g>" % (' transform="%s"' % tr if tr else "", inner)


def rot_pt(p, a, c=(0, 0)):
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def add(a, b, k=1.0):
    return (a[0] + b[0] * k, a[1] + b[1] * k)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def ln(v):
    return math.hypot(v[0], v[1])


def nrm(v):
    l = ln(v) or 1.0
    return (v[0] / l, v[1] / l)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def mix_hex(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(round(ca[i] + (cb[i] - ca[i]) * t)) for i in range(3))


def shade(c, k):
    return mix_hex(c, "#000000", k)


def tint(c, k):
    return mix_hex(c, "#ffffff", k)


def ik2(root, target, l1, l2, bend):
    """two-bone IK in 2D.  bend = +1 / -1 picks the side of the root->target line where the middle joint goes
    (+1: to the right of the direction root->target in screen coords, y down).  Returns (mid, end)."""
    d = sub(target, root)
    L = ln(d)
    L = max(min(L, l1 + l2 - 1e-6), abs(l1 - l2) + 1e-6, 1e-6)
    u = nrm(d) if ln(d) > 1e-9 else (0.0, 1.0)
    end = add(root, u, L)
    a = (l1 * l1 + L * L - l2 * l2) / (2 * L)
    h = math.sqrt(max(l1 * l1 - a * a, 0.0))
    perp = (-u[1], u[0])                       # right of u (y down)
    mid = add(add(root, u, a), perp, h * bend)
    return mid, end


# ------------------------------------------------------------------------------------------------ cast specs
RESCUE_COL = dict(shirt="#ed7e24", shirt_dk="#c45f14", vest="#1b1b19", band="#d4d8dc", band_line="#9aa2ab",
                  trouser="#423e3b", trouser_dk="#2f2c2a", boot="#383838", sole="#1c1c1c", glove="#333333",
                  belt="#1b1b19", buckle="#c9c9c4", pack="#2b2b2d", pack_dk="#1c1c1e", strap="#1b1b19",
                  under="#2a2a2a", radio="#1f1f21")

BASE = dict(
    skin="#fdf6ed", ink=INK, hair_col="#1d1d1d", eye="#070805", brow="#0b0b0a",
    head_ink_top=0.030, head_ink_side=0.046, body_ink=0.032,
    neck=0.05, wet=False, age="adult",
)


def _spec(**kw):
    s = dict(BASE)
    s.update(kw)
    return s


SPECS = {}
SPECS["kong"] = _spec(
    name="kong", legs=1.72, torso=1.39, total_ref=4.31,
    hair=dict(style="spiky", top=0.19, width=1.26, extent=0.72, n=6, fringe=0.30, seed=11),
    shoulder=1.32, chest=0.98, belt_w=0.90, hip_w=0.90, leg_w=0.42, boot_h=0.64, sole_len=(0.40, 0.47, 0.54), boot_w=0.42,
    hand=0.33, forearm=0.155, sleeve="short", sleeve_w=0.30, upper_arm=0.56, fore_arm=0.50,
    outfit="rescue", pack=True, radio=True, flag=True, kneepads=True, thigh_pouch=True, hip_pouches=True,
    col=dict(RESCUE_COL), glove=True, shoe="boot",
    face=dict(eye="oval", eye_w=0.08, eye_h=0.20, eye_sp=0.31, brow_len=0.225, brow_th=0.047, brow_y=-0.165,
              mouth_y=0.26, mouth_w=0.25, stubble=True),
    default_expr="determined", exprs=("determined", "neutral", "tired", "guilty", "alarmed", "shouting", "blink"),
)
SPECS["crew"] = _spec(
    # review: legs 1.83 -> 1.74 (the head was 0.212-0.217 of the figure, James 0.223)
    name="crew", legs=1.74, torso=1.37, total_ref=4.49, head_ink_top=0.036, head_ink_side=0.054,
    hair=dict(style="crest", top=0.25, width=1.27, extent=0.90, n=8, fringe=0.36, seed=5),          # sheet James: ink-black clumps
    shoulder=0.80, chest=0.72, belt_w=0.74, hip_w=0.70, leg_w=0.31, boot_h=0.47, sole_len=(0.38, 0.47, 0.60), boot_w=0.34,
    hand=0.30, forearm=0.13, sleeve="long", sleeve_w=0.22, upper_arm=0.58, fore_arm=0.52,
    outfit="rescue", pack=False, radio=True, flag=True, kneepads=False, thigh_pouch=True, hip_pouches=False,
    col=dict(RESCUE_COL, trouser="#313131", trouser_dk="#202020"), glove=True, shoe="boot",
    face=dict(eye="oval", eye_w=0.08, eye_h=0.18, eye_sp=0.40, brow_len=0.20, brow_th=0.046, brow_y=-0.165,
              mouth_y=0.21, mouth_w=0.26, stubble=False, brow_over_hair=True),
    default_expr="neutral", exprs=("neutral", "joy", "shouting", "scared", "blink"),
)
SPECS["driver"] = _spec(
    name="driver", legs=1.75, torso=1.27, total_ref=4.22,
    hair=dict(style="swept", top=0.155, width=1.17, extent=0.79, n=6, fringe=0.22, seed=7, col="#302a26"),
    shoulder=0.76, chest=0.64, belt_w=0.68, hip_w=0.66, leg_w=0.30, boot_h=0.30, sole_len=(0.36, 0.45, 0.56), boot_w=0.30,
    hand=0.20, forearm=0.15, sleeve="long", sleeve_w=0.20, upper_arm=0.56, fore_arm=0.50,
    outfit="office", tie=True, torn=True, pack=False, radio=False, flag=False, kneepads=False, thigh_pouch=False,
    hip_pouches=False, glove=False, shoe="shoe", claws=True,
    skin="#c4cdb2", skin_dk="#97a38a",
    col=dict(shirt="#eef1f3", shirt_dk="#b9c2cc", trouser="#73767d", trouser_dk="#55585f", boot="#2e2e2e",
             sole="#1c1c1c", belt="#3a2a1e", buckle="#b9b2a0", tie="#7d1d22", stain="#7a6248"),
    face=dict(eye="zombie", eye_w=0.13, eye_h=0.11, eye_sp=0.35, brow_len=0.20, brow_th=0.040, brow_y=-0.19,
              mouth_y=0.24, mouth_w=0.18, stubble=False),
    default_expr="still", exprs=("still", "head_lift", "lunge", "bite"),
)


def _wet(sp):
    w = dict(sp)
    w["name"] = sp["name"] + "_wet"
    w["wet"] = True
    c = dict(sp["col"])
    c.update(shirt="#c8581b", shirt_dk="#9d4214", trouser=shade(c["trouser"], 0.14), trouser_dk=shade(c["trouser_dk"], 0.14),
             band="#b4bcc4", vest="#121211", boot="#262626")
    w["col"] = c
    h = dict(sp["hair"])
    h.update(wet=True, top=h["top"] * 0.80, extent=h["extent"] * 1.06)
    w["hair"] = h
    return w


SPECS["kong_wet"] = _wet(SPECS["kong"])
SPECS["crew_wet"] = _wet(SPECS["crew"])


def get_spec(s):
    return SPECS[s] if isinstance(s, str) else s


# ------------------------------------------------------------------------------------------------ skeleton
VIEW_YAW = {"front": 7.0, "q": 28.0, "side": 60.0}        # head yaw (deg) of each drawing
BODY_YAW = {"front": 6.0, "q": 34.0, "side": 82.0}


def skeleton(sp, pose):
    """landmarks of the standing figure in D (y down, soles at 0)."""
    legs, torso = sp["legs"], sp["torso"]
    crotch = -legs
    chin = crotch - torso
    hc = chin - 0.5
    lean = pose.get("lean", 0.0)
    bob = pose.get("bob", 0.0)
    hipdx, hipdy = pose.get("hip", (0.0, 0.0))
    return dict(crotch=crotch, chin=chin, head_c=hc, hip_y=crotch - 0.06 + bob + hipdy, hip_dx=hipdx,
                belt_y=chin + torso * 0.79, shoulder_y=chin + 0.20, lean=lean)


# ------------------------------------------------------------------------------------------------ heads
def head_layers(sp, pose, view, s, hc, tilt):
    """returns (head_svg, face_svg, hair_svg) around the head centre hc (x, y)."""
    ink = sp["ink"]
    yaw = s * (VIEW_YAW[view] + pose.get("head_yaw", 0.0))
    cx, cy = hc
    skin = sp["skin"]
    # -- skull: ink disc with a paper inset, thicker at the left/right equator (sheet: 4.9 px median, 12 px at the sides)
    it, isd = sp["head_ink_top"], sp["head_ink_side"]
    head = ell(cx, cy, 0.5, 0.5, ink)
    head += ell(cx + 0.004 * s, cy - 0.003, 0.5 - isd, 0.5 - it, skin)
    if pose.get("back"):
        face = ""
        hair = _hair_back(sp, cx, cy)
    else:
        face = _face(sp, pose, view, s, yaw, cx, cy)
        hair = _hair(sp, pose, view, s, yaw, cx, cy)
        hair += pose.pop("_brows_svg", "")
    tr = "rotate(%s %s %s)" % (f(tilt), f(cx), f(cy + 0.35)) if tilt else None
    return g(head, tr), g(face, tr), g(hair, tr)


def sph(cx, cy, yaw, lon, lat, r=0.47):
    """a point on the head sphere: lon (deg, + screen-right), lat (deg, + up) -> (x, y, foreshortening cos)."""
    a = math.radians(lon + yaw)
    la = math.radians(lat)
    return (cx + r * math.sin(a) * math.cos(la), cy - r * math.sin(la), math.cos(a))


EXPR = {
    # eyes: kind, scale; brows: (inner angle deg, raise); mouth: (kind, args)
    "determined": dict(eyes="oval", brows=(18, 0.0), mouth=("smile", 1.0)),
    "neutral": dict(eyes="oval", brows=(4, 0.01), mouth=("flat", 0.8)),
    "tired": dict(eyes="lid", brows=(-8, 0.0), mouth=("flat_down", 0.75), bags=True),
    "guilty": dict(eyes="down", brows=(-20, 0.03), mouth=("wobble", 0.6), sweat=True),
    "alarmed": dict(eyes="ring", brows=(-14, 0.07), mouth=("o", 0.55), sweat=True),
    "shouting": dict(eyes="squint", brows=(26, -0.01), mouth=("open", 1.0)),
    "scared": dict(eyes="ring_small", brows=(-22, 0.06), mouth=("wobble_open", 0.5), sweat=True),
    "blink": dict(eyes="closed", brows=(4, 0.0), mouth=("flat", 0.8)),
    # infected
    "still": dict(eyes="z_lid", brows=(-4, -0.01), mouth=("slack", 0.4)),
    "head_lift": dict(eyes="z_open", brows=(6, 0.02), mouth=("slack", 0.6)),
    "lunge": dict(eyes="z_wide", brows=(28, -0.01), mouth=("snarl", 0.8)),
    "bite": dict(eyes="z_wide", brows=(30, -0.02), mouth=("bite", 1.0)),
    # extras
    "smile": dict(eyes="oval", brows=(0, 0.02), mouth=("smile", 1.0)),
    "worried": dict(eyes="oval", brows=(-18, 0.04), mouth=("wobble", 0.6)),
    "joy": dict(eyes="arc", brows=(0, 0.04), mouth=("open", 0.7)),
    "stern": dict(eyes="oval", brows=(12, 0.0), mouth=("frown", 0.8)),
    "sad": dict(eyes="down", brows=(-16, 0.03), mouth=("frown", 0.7)),
    "talk": dict(eyes="oval", brows=(4, 0.01), mouth=("open", 0.5)),
    "angry": dict(eyes="oval", brows=(24, -0.01), mouth=("frown", 0.9)),
    "surprised": dict(eyes="ring", brows=(-6, 0.07), mouth=("o", 0.5)),
}


def _eye(kind, x, y, fs, sp, s, gaze, blink, small=1.0, lid_tilt=0.0, ink=INK):
    F = sp["face"]
    ew, eh = F["eye_w"] * small, F["eye_h"] * small
    w = ew * max(fs, 0.35)
    gx, gy = gaze
    if blink == 2 or kind == "closed":
        return path("M%s %s Q%s %s %s %s" % (f(x - w * 1.5), f(y + 0.005), f(x), f(y + 0.045), f(x + w * 1.5), f(y + 0.005)),
                    stroke=ink, sw=0.028)
    if kind == "arc":                              # joyful closed ^ arcs (James on the sheet)
        return path("M%s %s Q%s %s %s %s" % (f(x - w * 1.6), f(y + 0.03), f(x), f(y - 0.07), f(x + w * 1.6), f(y + 0.03)),
                    stroke=ink, sw=0.040)
    if kind in ("oval", "down"):
        dy = 0.035 if kind == "down" else 0.0
        h = eh * (0.45 if blink == 1 else 1.0)
        o = ell(x + gx * 0.02, y + dy + gy * 0.02 + (eh - h) * 0.5, w / 2, h / 2, ink)
        if kind == "down":
            o += line((x - w * 0.9, y - eh * 0.42 + dy), (x + w * 0.9, y - eh * 0.42 + dy), ink, 0.02)
        return o
    if kind == "lid":                              # tired: the lower half of the oval under a heavy flat lid
        h = eh * 0.55
        o = ell(x, y + eh * 0.18, w / 2, h / 2, ink)
        o += line((x - w * 1.05, y - eh * 0.06 + lid_tilt), (x + w * 1.05, y - eh * 0.06 - lid_tilt), ink, 0.032)
        return o
    if kind == "squint":                           # shouting: tight > < chevrons
        a = 0.075
        return poly_stroke([(x - a * s, y - 0.055), (x + a * s * 0.9, y), (x - a * s, y + 0.055)], ink, 0.036) if False else \
            path("M%s %s L%s %s L%s %s" % (f(x - a), f(y - 0.05), f(x + a * 0.2), f(y + 0.005), f(x - a), f(y + 0.045)),
                 stroke=ink, sw=0.036)
    if kind in ("ring", "ring_small"):
        rx = (0.075 if kind == "ring" else 0.068) * max(fs, 0.4)
        ry = 0.085 if kind == "ring" else 0.075
        pr = 0.030 if kind == "ring" else 0.020
        o = ell(x, y, rx, ry, "#ffffff", ink, 0.026)
        o += ell(x + gx * 0.025, y + gy * 0.02, pr * max(fs, 0.5), pr * 1.15, ink)
        return o
    if kind.startswith("z_"):                      # infected: white eye, tiny red pupil, dark under-eye line
        rx = F["eye_w"] / 2 * max(fs, 0.4) * (1.15 if kind == "z_wide" else 1.0)
        ry = F["eye_h"] / 2 * (1.25 if kind == "z_wide" else 1.0)
        o = ""
        if kind == "z_lid":
            ry *= 0.62
            y += 0.02
        o += ell(x, y, rx, ry, "#f4f2e8", ink, 0.022)
        o += ell(x + gx * 0.02, y + gy * 0.015, 0.016, 0.016, "#d81c1c")
        if kind == "z_lid":
            o += line((x - rx * 1.15, y - ry * 0.95), (x + rx * 1.15, y - ry * 0.95), ink, 0.03)
        o += path("M%s %s Q%s %s %s %s" % (f(x - rx), f(y + ry + 0.03), f(x), f(y + ry + 0.06), f(x + rx), f(y + ry + 0.03)),
                  stroke=sp.get("skin_dk", "#888"), sw=0.022)
        return o
    return ell(x, y, w / 2, eh / 2, ink)


def _mouth(kind, amt, x, y, fs, sp, level=None, shape="a", ink=INK):
    F = sp["face"]
    W = F["mouth_w"] * max(fs, 0.45)
    if level is not None and level > 0.06:           # lip sync: open D shape, height follows the level
        lvl = min(max(level, 0.0), 1.0)
        w = (0.13 + 0.12 * lvl) * (0.72 if shape == "o" else (1.12 if shape == "e" else 1.0)) * max(fs, 0.45)
        h = (0.035 + 0.17 * lvl) * (1.1 if shape == "o" else (0.6 if shape == "e" else 1.0))
        return _open_mouth(x, y - h * 0.25, w, h, ink, teeth=lvl > 0.55, round_=shape == "o")
    if kind == "smile":
        w = W / 2
        return path("M%s %s Q%s %s %s %s" % (f(x - w), f(y - 0.015), f(x), f(y + 0.06), f(x + w), f(y - 0.015)), stroke=ink, sw=0.030)
    if kind == "flat":
        w = W * 0.45
        return line((x - w, y + 0.01), (x + w, y + 0.01), ink, 0.032)
    if kind == "flat_down":
        w = W * 0.33
        return path("M%s %s Q%s %s %s %s" % (f(x - w), f(y + 0.03), f(x), f(y - 0.005), f(x + w), f(y + 0.03)), stroke=ink, sw=0.028)
    if kind == "frown":
        w = W * 0.38
        return path("M%s %s Q%s %s %s %s" % (f(x - w), f(y + 0.035), f(x), f(y - 0.025), f(x + w), f(y + 0.035)), stroke=ink, sw=0.030)
    if kind == "wobble":
        w = W * 0.36
        return path("M%s %s Q%s %s %s %s Q%s %s %s %s" % (f(x - w), f(y + 0.02), f(x - w / 2), f(y - 0.02), f(x), f(y + 0.01),
                                                       f(x + w / 2), f(y + 0.04), f(x + w), f(y + 0.0)), stroke=ink, sw=0.026)
    if kind == "wobble_open":
        return _open_mouth(x, y, W * 0.45, 0.07, ink, wavy=True)
    if kind == "o":
        return ell(x, y + 0.01, 0.045 * max(fs, 0.5), 0.06, "#6b1f24", ink, 0.026)
    if kind == "open":
        return _open_mouth(x, y - 0.03, W * 1.05, 0.21 * amt, ink, teeth=True)
    if kind == "slack":
        return ell(x, y + 0.01, W * 0.3, 0.04 * amt + 0.015, "#3a1a1c", ink, 0.024)
    if kind == "snarl":
        return _open_mouth(x, y - 0.01, W * 1.2, 0.12, ink, teeth=True, fangs=True, red=True)
    if kind == "bite":
        return _open_mouth(x, y - 0.02, W * 1.5, 0.26, ink, teeth=True, fangs=True, red=True, lower_teeth=True)
    return ""


def _open_mouth(x, y, w, h, ink, teeth=False, wavy=False, fangs=False, red=False, lower_teeth=False, round_=False):
    hw = w / 2
    if round_:
        d = "M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z" % (
            f(x - hw), f(y + h * 0.45), f(x - hw), f(y - h * 0.05), f(x + hw), f(y - h * 0.05), f(x + hw), f(y + h * 0.45),
            f(x + hw), f(y + h * 1.0), f(x - hw), f(y + h * 1.0), f(x - hw), f(y + h * 0.45))
    else:                                        # D shape: flat-ish top, round bottom
        d = "M%s %s Q%s %s %s %s C%s %s %s %s %s %s Z" % (
            f(x - hw), f(y), f(x), f(y - h * 0.12), f(x + hw), f(y),
            f(x + hw * 0.95), f(y + h * 1.25), f(x - hw * 0.95), f(y + h * 1.25), f(x - hw), f(y))
    inner = "#7a1d24" if not red else "#5e1418"
    o = '<clipPath id="mc%d"><path d="%s"/></clipPath>' % (abs(hash((round(x, 3), round(y, 3), round(w, 3)))) % 99999, d)
    cid = o[o.index('"') + 1:o.index('"', o.index('"') + 1)]
    o += path(d, inner)
    body = ""
    body += ell(x, y + h * 1.05, hw * 0.75, h * 0.42, "#e8858e")           # tongue
    if teeth:
        body += '<rect x="%s" y="%s" width="%s" height="%s" fill="#fbfbf6"/>' % (f(x - hw), f(y - h * 0.2), f(w), f(h * 0.24 + 0.012))
    if lower_teeth:
        body += '<rect x="%s" y="%s" width="%s" height="%s" fill="#fbfbf6"/>' % (f(x - hw), f(y + h * 0.88), f(w), f(h * 0.3))
    if fangs:
        for fx_ in (-0.55, 0.55):
            body += path(pts_d([(x + hw * fx_ - 0.02, y + h * 0.02), (x + hw * fx_ + 0.02, y + h * 0.02), (x + hw * fx_, y + h * 0.36)]), "#fbfbf6")
    o += '<g clip-path="url(#%s)">%s</g>' % (cid, body)
    o += path(d, "none", ink, 0.030)
    return o


def _face(sp, pose, view, s, yaw, cx, cy):
    F = sp["face"]
    ink = sp["ink"]
    expr = pose.get("expr") or sp.get("default_expr", "neutral")
    E = EXPR.get(expr, EXPR["neutral"])
    blink = pose.get("blink", 0)
    gaze = pose.get("gaze", (0.0, 0.0))
    o = ""
    eye_lon = math.degrees(math.asin(min(F["eye_sp"] / 2 / 0.5, 0.95)))
    eye_lat = -F.get("eye_y", 0.0) / 0.47 * 57.3
    eyes = []
    for side in (-1, 1):
        x, y, fs = sph(cx, cy, yaw, side * eye_lon, eye_lat, 0.5)
        if fs < 0.12:
            continue
        eyes.append((side, x, y, fs))
    ekind = E["eyes"]
    if sp["face"]["eye"] == "zombie" and not ekind.startswith("z_"):
        ekind = "z_open"
    for side, x, y, fs in eyes:
        small = 0.9 if (fs < 0.75) else 1.0
        o += _eye(ekind, x, y, fs, sp, s, gaze, blink, small, ink=ink)
    # glasses (extras)
    if F.get("glasses"):
        for side, x, y, fs in eyes:
            gw = 0.17 * max(fs, 0.3)
            if F["glasses"] == "round":
                o += ell(x, y, gw * 0.62, 0.095, "none", ink, 0.022)
            else:
                o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.02" fill="none" stroke="%s" stroke-width="0.024"/>' % (
                    f(x - gw * 0.62), f(y - 0.085), f(gw * 1.24), f(0.17), ink)
        if len(eyes) == 2:
            o += line((eyes[0][1] + 0.105 * eyes[0][3], eyes[0][2] - 0.03), (eyes[1][1] - 0.105 * eyes[1][3], eyes[1][2] - 0.03), ink, 0.02)
    # brows: straight bars, inner ends down for anger (+), up for worry (-)
    ang, raise_ = E["brows"]
    o_face = o
    o = ""
    if not F.get("no_brows"):
        for side, x, y, fs in eyes:
            bl = F["brow_len"] * max(fs, 0.35)
            by = cy + F["brow_y"] - raise_
            bx = x
            inner = -side                                  # the inner end points toward the face centre
            a = math.radians(ang)
            # inner end lower by ang: in screen coords y down
            dx, dy = bl / 2, bl / 2 * math.tan(a)
            p_in = (bx + inner * dx, by + dy)
            p_out = (bx - inner * dx, by - dy)
            o += line(p_in, p_out, sp["brow"], F["brow_th"], cap="round")
    if F.get("brow_over_hair"):
        # review fix: the crest fringe covered the crew's brows (weak face); they now ride on the hair card,
        # with a thin skin-coloured halo so they read on the black fringe
        halo = o.replace('stroke="%s"' % sp["brow"], 'stroke="%s"' % sp["skin"])
        halo = re.sub(r'stroke-width="([0-9.]+)"', lambda m: 'stroke-width="%s"' % f(float(m.group(1)) + 0.022), halo)
        pose["_brows_svg"] = halo + o
        o = o_face
    else:
        o = o_face + o
    # mouth
    mlon = 0.0
    mx, my, mfs = sph(cx, cy, yaw, mlon, -math.degrees(math.asin(F["mouth_y"] / 0.5)), 0.5)
    lvl = pose.get("mouth")
    shape = "a"
    if isinstance(lvl, (tuple, list)):
        shape, lvl = lvl[0], lvl[1]
    mk, amt = E["mouth"]
    o += _mouth(mk, amt, mx, my, mfs, sp, level=lvl, shape=shape, ink=ink)
    # moustache / beard (extras)
    if F.get("moustache"):
        mw = 0.17 * max(mfs, 0.5)
        o += path("M%s %s Q%s %s %s %s Q%s %s %s %s Z" % (f(mx - mw), f(my - 0.03), f(mx), f(my - 0.11), f(mx + mw), f(my - 0.03),
                                                         f(mx), f(my - 0.06), f(mx - mw), f(my - 0.03)), sp["hair_col"] if "hair_col" in sp else ink)
    # stubble: short ink ticks inside the jaw outline (sheet: 9-11 ticks, 45..130 deg, 3-5 px, 8-9 px apart)
    if F.get("stubble"):
        rnd = random.Random(17)
        n = 11
        a0, a1 = 42 + yaw * 0.6, 136 + yaw * 0.6
        for i in range(n):
            a = math.radians(a0 + (a1 - a0) * i / (n - 1) + rnd.uniform(-2.5, 2.5))
            r0 = 0.5 - sp["head_ink_top"] - 0.012
            L = rnd.uniform(0.028, 0.042)
            p0 = (cx + r0 * math.cos(a), cy + r0 * math.sin(a))
            p1 = (cx + (r0 - L) * math.cos(a), cy + (r0 - L) * math.sin(a))
            if p0[1] - cy < 0.33:
                continue
            o += line(p0, p1, ink, rnd.uniform(0.014, 0.022))
    if F.get("beard"):
        o += path("M%s %s A0.47 0.47 0 0 0 %s %s Q%s %s %s %s Z" % (
            f(cx - 0.40), f(cy + 0.24), f(cx + 0.40), f(cy + 0.24), f(mx), f(my + 0.02), f(cx - 0.40), f(cy + 0.24)), sp["hair_col"])
    if F.get("wrinkles"):
        for k in (0, 1):
            yy = cy - 0.30 + k * 0.045
            o += path("M%s %s Q%s %s %s %s" % (f(cx - 0.12 + yaw / 300), f(yy), f(cx + yaw / 300), f(yy - 0.02), f(cx + 0.12 + yaw / 300), f(yy)),
                      stroke=ink, sw=0.012)
    if F.get("blush"):
        for side, x, y, fs in eyes:
            o += ell(x + side * 0.03, y + 0.15, 0.06 * fs, 0.03, "#f2a7a4")
    if E.get("bags"):
        for side, x, y, fs in eyes:
            o += path("M%s %s Q%s %s %s %s" % (f(x - 0.05 * fs), f(y + 0.095), f(x), f(y + 0.125), f(x + 0.05 * fs), f(y + 0.095)),
                      stroke=ink, sw=0.014)
    if E.get("sweat") or pose.get("sweat"):
        sx, sy = cx + s * 0.36 + 0.0, cy - 0.20
        o += path("M%s %s Q%s %s %s %s A0.045 0.045 0 1 1 %s %s Q%s %s %s %s Z" % (
            f(sx), f(sy - 0.11), f(sx + 0.02), f(sy - 0.05), f(sx + 0.045), f(sy), f(sx - 0.045), f(sy), f(sx - 0.02), f(sy - 0.05),
            f(sx), f(sy - 0.11)), "#9fd3f2", ink, 0.018)
    if pose.get("rain_drips") or sp.get("wet"):
        rnd = random.Random(3)
        for i in range(3):
            x0 = cx + rnd.uniform(-0.3, 0.3)
            y0 = cy + rnd.uniform(-0.15, 0.2)
            if any(abs(x0 - e[1]) < 0.11 and abs(y0 - e[2]) < 0.16 for e in eyes):      # never a bead on an eye (reads as a tear)
                continue
            o += path("M%s %s Q%s %s %s %s A0.018 0.018 0 1 1 %s %s Q%s %s %s %s Z" % (
                f(x0), f(y0 - 0.045), f(x0 + 0.008), f(y0 - 0.02), f(x0 + 0.018), f(y0), f(x0 - 0.018), f(y0), f(x0 - 0.008), f(y0 - 0.02),
                f(x0), f(y0 - 0.045)), "#cfe6f5", None)
    return o


# ------------------------------------------------------------------------------------------------ hair
def _hair(sp, pose, view, s, yaw, cx, cy):
    H = sp["hair"]
    st = H["style"]
    col = H.get("col", sp["hair_col"])
    ink = sp["ink"]
    rnd = random.Random(H.get("seed", 1) * 31 + {"front": 0, "q": 1, "side": 2}[view])
    wet = H.get("wet", False)
    sh = math.sin(math.radians(yaw)) * 0.5            # how far the face centre has moved toward the facing side
    if st in ("spiky", "crest", "messy", "short_spiky"):
        top = 0.5 + H["top"]
        hw = H["width"] / 2
        low = (0.5 + H["top"]) - H["extent"]          # y-up of the lowest side spike, rel. to the head centre
        fs_ = 1 if s > 0 else -1                      # face side
        n = H["n"]
        crest = st == "crest"
        droop = 1.0 if wet else 0.0
        # --- outer boundary: from the face-side temple over the crown to the back temple (math angles, y up)
        out = []
        # face-side lock (in front of the ear) hanging to about low * 0.4
        if view != "side":
            out.append((0.475, 0.04))
            out.append((hw * 0.95, low + (0.10 if not crest else 0.02)))
            out.append((0.545, 0.20))
        else:
            out.append((0.50, 0.20))
        a0, a1 = -2.0, 182.0
        for i in range(n + 1):
            t = i / float(n)
            a = math.radians(a0 + (a1 - a0) * t)
            rx = hw * 0.93
            ry = top * 0.97
            r = 1.0 / math.sqrt((math.cos(a) / rx) ** 2 + (math.sin(a) / ry) ** 2) * rnd.uniform(0.96, 1.04)
            # clumps lean away from the face, wet clumps droop
            lean_a = a + math.radians(rnd.uniform(4, 16) + (10 if crest else 0)) * (1 if t < 0.5 else 0.6)
            tip = (r * math.cos(lean_a), r * math.sin(lean_a) - droop * 0.06 * math.cos(a) ** 2)
            if i > 0:
                am = (prev_a + a) / 2
                rv = 1.0 / math.sqrt((math.cos(am) / (hw * 0.86)) ** 2 + (math.sin(am) / (top * 0.80)) ** 2)
                rv = max(rv, 0.52)
                out.append((rv * math.cos(am), rv * math.sin(am)))
            out.append(tip)
            prev_a = a
        # back side: down to the lowest spike, then the nape
        out.append((-0.55, 0.16))
        out.append((-hw * 1.02, low))
        out.append((-0.50, low + 0.10))
        out.append((-hw * 0.88, low + 0.03))
        out.append((-0.46, low - 0.02))
        # --- hairline / fringe from the back temple across the forehead to the face temple
        fr = H["fringe"]
        fx = [-0.40, -0.18, 0.05, 0.27] if not crest else [-0.40, -0.22, -0.02, 0.18, 0.34]
        dep = [0.22, 0.30, 0.27, 0.20] if not crest else [0.20, 0.32, 0.36, 0.30, 0.20]
        inner = [(-0.47, 0.10)]
        for k, (x, dd) in enumerate(zip(fx, dep)):
            yv = 0.5 - 0.09                              # valley: high on the forehead
            if k > 0:
                inner.append(((fx[k - 1] + x) / 2 + 0.02, yv - 0.03))
            dd = dd * fr / 0.30 * rnd.uniform(0.9, 1.08)
            inner.append((x + 0.05, 0.5 - dd))          # tip (y up: 0.5 = skull top)
        if view != "side":
            inner.append((0.40, 0.30))
            inner.append((0.46, 0.12))
        # y-up -> screen, mirror for the facing side, the fringe follows the face when the head turns
        poly = []
        for x, y in out:
            poly.append((cx + fs_ * (x - (0.0)) - sh * 0.10, cy - y))
        for x, y in inner[::-1]:
            pass
        for x, y in inner[::-1][::-1][::-1]:
            pass
        fr_pts = [(cx + fs_ * x + sh * 0.45 * (1 - abs(x)) - sh * 0.10, cy - y) for x, y in inner]
        if view == "side":
            fr_pts = [p for p in fr_pts if (p[0] - cx) * fs_ < 0.40]
        poly = poly + fr_pts
        o = ""
        if st == "spiky" and not wet:
            # the sheet's cowlick: one clump standing up off the crown on the back side
            g_ = fs_ if view == "front" else -fs_         # sheet: on the screen-right of the crown in the front drawing
            bx_ = cx + g_ * 0.24 - sh * 0.10
            o += path(pts_d([(bx_ - g_ * 0.12, cy - top + 0.14), (bx_ + g_ * 0.10, cy - top - 0.10), (bx_ + g_ * 0.16, cy - top + 0.16)]),
                      col, ink, 0.034)
        o += path(pts_d(poly), col, ink, 0.034)
        if wet:
            for k, (x0, y0, dx, dy) in enumerate(((-0.30, 0.20, 0.07, -0.05), (-0.06, 0.13, 0.08, -0.03), (0.17, 0.17, 0.07, 0.02))):
                xa = cx + fs_ * x0 - sh * 0.10
                o += path("M%s %s Q%s %s %s %s" % (f(xa), f(cy - top + y0), f(xa + fs_ * dx * 0.5), f(cy - top + y0 + dy - 0.02),
                                                 f(xa + fs_ * dx), f(cy - top + y0 + dy)), stroke="#4a5059", sw=0.016)
            for k in range(3):                         # rain beads on the wet hair (kept off the eye line)
                x0 = cx - 0.3 + k * 0.28
                y0_ = cy - top + 0.16 + 0.05 * (k % 2)
                o += path("M%s %s A0.02 0.02 0 1 0 %s %s" % (f(x0 - 0.02), f(y0_), f(x0 + 0.02), f(y0_)), "#cfe6f5")
        return o
    if st in ("swept", "grey_swept", "neat"):
        top = 0.5 + H["top"]
        hw = H["width"] / 2
        fs_ = 1 if s > 0 else -1
        low = -0.5 + H["extent"]
        fr = H["fringe"]
        P = [(0.46, 0.24), (0.55, 0.36), (0.50, 0.54), (0.30, top - 0.01), (0.0, top), (-0.30, top - 0.02), (-0.54, 0.48),
             (-hw * 1.04, 0.22), (-hw * 1.0, 0.02), (-0.50, -0.06), (-0.44, 0.02), (-0.40, 0.22), (-0.22, 0.5 - fr * 0.2),
             (0.02, 0.5 - fr * 0.55), (0.26, 0.5 - fr * 0.95), (0.42, 0.20)]
        if H.get("messy"):
            P[4] = (0.02, top + 0.06)
        poly = [(cx + fs_ * x + (sh * 0.4 if y < 0.45 and x > -0.45 else 0) - sh * 0.1, cy - y) for x, y in P]
        o = path(smooth_d(poly, True, 0.35), col, ink, 0.034)
        o += path("M%s %s Q%s %s %s %s" % (f(cx - fs_ * 0.25), f(cy - top + 0.07), f(cx + fs_ * 0.02), f(cy - 0.30),
                                         f(cx + fs_ * 0.30), f(cy - 0.27)), stroke=tint(col, 0.22), sw=0.018)
        if H.get("messy"):
            for i in range(4):
                a = math.radians(50 + 25 * i)
                p0 = (cx + 0.55 * math.cos(a) * fs_, cy - 0.62 * math.sin(a))
                o += path(pts_d([p0, (p0[0] + 0.04, p0[1] - 0.09), (p0[0] + 0.08, p0[1] + 0.01)]), col, ink, 0.02)
        return o
    if st in ("bob", "long", "ponytail", "bun"):
        top = 0.5 + H["top"]
        half_w = H["width"] / 2
        f_side = 1 if s > 0 else -1
        low = {"bob": 0.38, "long": 1.05, "ponytail": 0.05, "bun": 0.05}[st]
        o = ""
        if st == "long":                               # the back panel of long hair, behind the shoulders
            pass
        if st == "ponytail":
            px, py = cx - f_side * 0.48 - sh * 0.3, cy - 0.15
            o += path(smooth_d([(px, py - 0.08), (px - f_side * 0.28, py + 0.1), (px - f_side * 0.22, py + 0.62), (px - f_side * 0.05, py + 0.5),
                                (px + f_side * 0.02, py + 0.08)], True, 0.5), col, ink, 0.032)
            o += ell(px - f_side * 0.02, py - 0.02, 0.06, 0.06, H.get("tie", "#d4373b"), ink, 0.02)
        if st == "bun":
            o += ell(cx - sh * 0.3 - f_side * 0.05, cy - top - 0.08, 0.17, 0.15, col, ink, 0.032)
        P = []
        for i in range(13):
            t = i / 12.0
            a = math.radians(-12 + 204 * t)
            r = 1.0 / math.sqrt((math.cos(a) / half_w) ** 2 + (math.sin(a) / top) ** 2)
            P.append((cx + r * math.cos(a), cy - r * math.sin(a)))
        P = [(cx + half_w + 0.01, cy + low)] + P + [(cx - half_w - 0.01, cy + low)]
        P += [(cx - half_w + 0.10, cy + low + 0.02), (cx - 0.44, cy - 0.05), (cx - 0.30, cy - 0.5 + H["fringe"]),
              (cx + 0.05, cy - 0.5 + H["fringe"] * 0.8), (cx + 0.32, cy - 0.5 + H["fringe"] * 1.05), (cx + 0.44, cy - 0.05),
              (cx + half_w - 0.10, cy + low + 0.02)]
        P = [(x - sh * 0.28, y) for x, y in P]
        o += path(smooth_d(P, True, 0.3), col, ink, 0.034)
        return o
    if st == "bald":
        f_side = 1 if s > 0 else -1
        o = ""
        for side in (-1, 1):
            x0 = cx + side * 0.47 - sh * 0.3
            o += path(smooth_d([(x0, cy - 0.25), (x0 + side * 0.07, cy - 0.1), (x0 + side * 0.04, cy + 0.08), (x0 - side * 0.04, cy + 0.02)], True, 0.4),
                      H.get("col", "#9a9a9a"), ink, 0.026)
        return o
    if st == "cap":
        f_side = 1 if s > 0 else -1
        ccol = H.get("cap_col", "#2f5fa8")
        o = path("M%s %s A0.53 0.56 0 0 1 %s %s Z" % (f(cx - 0.53 - sh * 0.2), f(cy - 0.08), f(cx + 0.53 - sh * 0.2), f(cy - 0.08)), ccol, ink, 0.032)
        o += path(pts_d([(cx + f_side * 0.05 + sh * 0.6, cy - 0.12), (cx + f_side * 0.80 + sh * 0.3, cy - 0.06), (cx + f_side * 0.78 + sh * 0.3, cy - 0.01),
                         (cx + f_side * 0.02 + sh * 0.6, cy - 0.04)]), shade(ccol, 0.25), ink, 0.03)
        o += line((cx - 0.5 - sh * 0.2, cy - 0.08), (cx + 0.5 - sh * 0.2, cy - 0.08), ink, 0.02)
        # hair tufts under the cap at the back
        o += path(pts_d([(cx - f_side * 0.48, cy - 0.08), (cx - f_side * 0.56, cy + 0.06), (cx - f_side * 0.44, cy + 0.02)]), sp["hair_col"], ink, 0.02)
        return o
    return ""


def _hair_back(sp, cx, cy):
    H = sp["hair"]
    col = H.get("col", sp["hair_col"])
    ink = sp["ink"]
    top = 0.5 + H["top"]
    hw = H["width"] / 2
    rnd = random.Random(H.get("seed", 1) * 7)
    spiky = H["style"] in ("spiky", "crest", "messy", "short_spiky")
    pts = []
    if spiky:
        # the sheet's clumps seen from behind: pointed tips over the crown, deep notches, side clumps down to the ears
        n = 12
        for i in range(n + 1):
            a = math.radians(-24 + 228 * i / n)
            r = 1.0 / math.sqrt((math.cos(a) / hw) ** 2 + (math.sin(a) / top) ** 2)
            if i % 2 == 0:
                r *= rnd.uniform(1.02, 1.09); a += math.radians(rnd.uniform(-5, 5))
            else:
                r *= 0.86
            pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
        nape = []
        for k in range(7):
            x = cx - 0.48 + k * 0.16
            nape.append((x, cy + 0.10 + (0.15 if k % 2 else 0.0) + (0.04 if k in (0, 6) else 0.0)))
        poly = pts + nape
        return path(pts_d(poly), col, ink, 0.034)
    n = 9
    for i in range(n + 1):
        a = math.radians(-20 + 220 * i / n)
        r = 1.0 / math.sqrt((math.cos(a) / hw) ** 2 + (math.sin(a) / top) ** 2)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    nape = []
    for k in range(5):
        x = cx - 0.42 + k * 0.21
        nape.append((x, cy + 0.12 + (0.10 if k % 2 else 0.0)))
    poly = pts + [(cx - 0.47, cy + 0.10)] + nape + [(cx + 0.47, cy + 0.10)]
    return path(smooth_d(poly, True, 0.3), col, ink, 0.034)


# ------------------------------------------------------------------------------------------------ torso
def _cyl_x(phi, a, b, th):
    """x of a front-surface point at angle phi (deg, 0 = front centre, + toward the screen-right edge in front view)
    on an elliptic cross-section (half width a, half depth b) turned by th (deg).  Returns (x, cos_visible)."""
    p, t = math.radians(phi), math.radians(th)
    x = a * math.sin(p) * math.cos(t) + b * math.cos(p) * math.sin(t)
    vis = math.cos(p + t)
    return x, vis


def torso_layer(sp, pose, view, s, K):
    c = sp["col"]
    ink = sp["ink"]
    bw = sp["body_ink"]
    th = s * BODY_YAW[view]
    chin = K["chin"]
    belt = K["belt_y"]
    crotch = K["crotch"]
    a = sp["chest"] / 2
    b = a * 0.62
    ahalf = math.sqrt((a * math.cos(math.radians(th))) ** 2 + (b * math.sin(math.radians(th))) ** 2)
    bhalf = ahalf * sp["belt_w"] / sp["chest"]
    cx = 0.0
    top = chin + sp["neck"]
    sy = K["shoulder_y"]
    o = ""
    out = sp["outfit"]
    # -- pelvis (trousers) from the belt to the crotch
    hw = max(sp["hip_w"] / 2 * (math.cos(math.radians(th)) * 0.75 + 0.25 * 0.75), bhalf * 0.9)
    hw = max(hw, bhalf * 0.92)
    pel = [(cx - bhalf, belt - 0.02), (cx + bhalf, belt - 0.02), (cx + hw + 0.01, crotch - 0.02), (cx + hw * 0.2, crotch - 0.01),
           (cx - hw * 0.2, crotch - 0.01), (cx - hw - 0.01, crotch - 0.02)]
    o += path(smooth_d(pel, True, 0.15), c["trouser"], ink, bw)
    if sp.get("skirt"):
        kn = crotch + 0.62
        sk = [(cx - bhalf, belt - 0.02), (cx + bhalf, belt - 0.02), (cx + bhalf * 1.45, kn), (cx - bhalf * 1.45, kn)]
        o += path(pts_d(sk), c["trouser"], ink, bw)
        for k in (-0.5, 0.0, 0.5):
            o += line((cx + bhalf * k * 0.8, belt + 0.1), (cx + bhalf * k * 1.3, kn - 0.02), shade(c["trouser"], 0.3), 0.012)
    if view == "front":
        o += line((cx + 0.02, belt + 0.07), (cx + 0.02, crotch - 0.02), shade(c["trouser"], 0.45), 0.016)
    # -- shirt body
    shoulder_drop = 0.10
    hem = belt + 0.02
    body = [(cx - ahalf * 0.62, top - 0.01), (cx - ahalf * 0.98, sy - 0.02), (cx - ahalf * 1.02, sy + 0.18), (cx - ahalf * 0.98, (sy + hem) / 2),
            (cx - bhalf, hem), (cx + bhalf, hem), (cx + ahalf * 0.98, (sy + hem) / 2), (cx + ahalf * 1.02, sy + 0.18),
            (cx + ahalf * 0.98, sy - 0.02), (cx + ahalf * 0.62, top - 0.01)]
    shirt = c.get("shirt", "#888")
    if out == "delivery":
        shirt = c["jacket"]
    o += path(smooth_d(body, True, 0.25), shirt, ink, bw)
    clip_id = "tc_%s_%s" % (sp["name"], view)
    o += '<clipPath id="%s"><path d="%s"/></clipPath>' % (clip_id, smooth_d(body, True, 0.25))
    inner = ""
    if out == "rescue" and pose.get("back"):
        py0, py1 = sy + 0.12, sy + 0.34
        kb = 0.62 if sp["shoulder"] < 1.0 else 0.8
        inner += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(-ahalf * kb), f(py0), f(ahalf * 2 * kb), f(py1 - py0), c["vest"])
        inner += ('<text x="0" y="%s" font-family="Inter" font-weight="900" font-size="%s" fill="#f4f2ec" text-anchor="middle" '
                  'textLength="%s" lengthAdjust="spacingAndGlyphs">RESCUE</text>') % (f(py1 - 0.055), f(0.15 if kb > 0.7 else 0.12), f(ahalf * 1.75 * kb))
        by0 = max(py1 + 0.20, hem - 0.36)
        inner += '<rect x="-2" y="%s" width="4" height="0.10" fill="%s"/>' % (f(by0), c["band"])
        inner += line((-2, by0 + 0.05), (2, by0 + 0.05), c["band_line"], 0.010)
        inner += line((0, top + 0.02), (0, py0), shade(shirt, 0.3), 0.012)
    elif out == "rescue":
        # black chest panel with RESCUE, reflective band below
        py0, py1 = sy + 0.27, sy + 0.51
        narrow = sp["shoulder"] < 1.0 and view == "front"    # review fix: crew's arm cut "RESCUE" to "RESCU"
        # backpack straps (sheet: black straps from beside the collar down the chest to under the arms), under the patch
        if sp.get("pack"):
            for phi in (-1, 1):
                x_top, v = _cyl_x(phi * 30, a, b, th)
                x_mid, v1_ = _cyl_x(phi * 46, a, b, th)
                x_bot, v2 = _cyl_x(phi * 66, a, b, th)
                if v > 0.05:
                    pts_ = [(x_top, top - 0.02), (x_mid, sy + 0.34), (x_bot, sy + 0.86)]
                    inner += path(smooth_d(pts_, False, 0.5), "none", ink, 0.165)
                    inner += path(smooth_d(pts_, False, 0.5), "none", "#2b2b2d", 0.115)
        x0, v0 = _cyl_x(-34 if narrow else -30, a, b, th)
        x1, v1 = _cyl_x(36 if narrow else 44, a, b, th)
        if view == "side":
            x0, x1 = _cyl_x(-10, a, b, th)[0], _cyl_x(75, a, b, th)[0]
        inner += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(min(x0, x1)), f(py0), f(abs(x1 - x0)), f(py1 - py0), c["vest"])
        tw = abs(x1 - x0) * 0.86
        if view != "side":
            inner += ('<text x="%s" y="%s" font-family="Inter" font-weight="900" font-size="0.115" fill="#f4f2ec" text-anchor="middle" '
                      'textLength="%s" lengthAdjust="spacingAndGlyphs">RESCUE</text>') % (f((x0 + x1) / 2), f(py1 - 0.06), f(tw))
        # silver reflective band low on the jacket (sheet: about 3/4 down, grey with lighter edges)
        by0 = max(py1 + 0.15, hem - 0.44)
        inner += '<rect x="-2" y="%s" width="4" height="0.13" fill="%s"/>' % (f(by0), tint(c["band"], 0.45))
        inner += '<rect x="-2" y="%s" width="4" height="0.062" fill="%s"/>' % (f(by0 + 0.034), shade(c["band"], 0.10))
        inner += line((-2, by0), (2, by0), shade(c["band"], 0.45), 0.010)
        inner += line((-2, by0 + 0.13), (2, by0 + 0.13), shade(c["band"], 0.45), 0.010)
        # placket / zip line
        zx, zv = _cyl_x(4, a, b, th)
        if zv > 0.1:
            inner += line((zx, top + 0.05), (zx, py0), shade(shirt, 0.35), 0.014)
            inner += line((zx, py1), (zx, hem), shade(shirt, 0.35), 0.014)
        if False:
            for phi in (-62, 64):
                x_top, v = _cyl_x(phi * 1.25, a, b, th)
                x_bot, v2 = _cyl_x(phi * 0.95, a, b, th)
                if v > 0.05:
                    inner += line((x_top, sy - 0.08), (x_bot, hem), c["strap"], 0.085, cap="butt")
                    inner += line((x_top - 0.0, sy - 0.08), (x_bot, hem), shade(c["strap"], 0.2), 0.012, cap="butt")
        # side seam shade (the side away from the facing direction is a little darker)
        if view != "front":
            inner += path(smooth_d([(cx - s * ahalf * 1.1, top), (cx - s * ahalf * 0.78, sy + 0.2), (cx - s * bhalf * 0.86, hem + 0.05),
                                    (cx - s * bhalf * 1.2, hem + 0.05), (cx - s * ahalf * 1.2, sy)], True, 0.3), shade(shirt, 0.12))
    elif out in ("office", "shirt", "polo", "tee", "hoodie", "blazer", "delivery", "dress"):
        zx, zv = _cyl_x(2, a, b, th)
        if out in ("office", "shirt", "blazer") and not pose.get("back"):
            # buttons + placket
            inner += line((zx, top + 0.06), (zx, hem), shade(shirt, 0.28), 0.012)
            for k in range(5):
                inner += ell(zx + 0.03 * (1 if th >= 0 else -1), top + 0.18 + k * 0.17, 0.014, 0.014, shade(shirt, 0.4))
        if out == "blazer":
            jk = c["jacket"]
            for side in (-1, 1):
                xs, v = _cyl_x(side * 30, a, b, th)
                xe = cx + side * ahalf * 1.05
                if v > -0.2:
                    inner += path(pts_d([(xs, top), (xe, top), (xe + side * 0.1, hem + 0.1), (zx + side * 0.06, hem + 0.1), (zx + side * 0.06, top + 0.55),
                                         (xs + side * 0.04, top + 0.22)]), jk, ink, bw * 0.8)
        if out == "hoodie":
            inner += path(smooth_d([(zx - 0.22, top + 0.02), (zx, top + 0.20), (zx + 0.22, top + 0.02)], False, 0.5), "none", shade(shirt, 0.35), 0.03)
            inner += line((zx - 0.06, top + 0.1), (zx - 0.07, top + 0.42), shade(shirt, 0.5), 0.016)
            inner += line((zx + 0.06, top + 0.1), (zx + 0.07, top + 0.42), shade(shirt, 0.5), 0.016)
            inner += '<rect x="%s" y="%s" width="0.42" height="0.20" rx="0.05" fill="%s" stroke="%s" stroke-width="0.016"/>' % (
                f(zx - 0.21), f(hem - 0.32), shade(shirt, 0.1), shade(shirt, 0.45))
        if out == "delivery":
            # green jacket, black lower half, white scooter logo
            inner += '<rect x="-2" y="%s" width="4" height="2" fill="%s"/>' % (f(sy + 0.55), c.get("jacket_lo", "#2c2c2c"))
            lx, lv = _cyl_x(10, a, b, th)
            if lv > 0.2:
                inner += _scooter_logo(lx, sy + 0.25, 0.30 * lv)
            inner += line((zx, top + 0.05), (zx, hem), shade(c["jacket"], 0.4), 0.014)
        if out == "polo":
            inner += line((zx, top + 0.04), (zx, top + 0.32), shade(shirt, 0.35), 0.014)
            for k in range(2):
                inner += ell(zx + 0.02, top + 0.12 + k * 0.1, 0.012, 0.012, shade(shirt, 0.45))
        if out == "dress":
            pass
        if sp.get("print"):
            px, pv = _cyl_x(0, a, b, th)
            if pv > 0.3:
                inner += ell(px, sy + 0.32, 0.13 * pv, 0.12, sp["print"], ink, 0.012)
        if sp.get("tie") and not pose.get("back"):
            tx, tv = _cyl_x(5, a, b, th)
            if tv > 0.15:
                tc = c["tie"]
                inner += path(pts_d([(tx - 0.045, top + 0.03), (tx + 0.045, top + 0.03), (tx + 0.025, top + 0.10), (tx - 0.025, top + 0.10)]),
                              tc, ink, 0.014)
                # loosened: the blade hangs a little to the side
                inner += path(pts_d([(tx - 0.025, top + 0.10), (tx + 0.025, top + 0.10), (tx + 0.075, top + 0.62), (tx + 0.03, top + 0.70),
                                     (tx - 0.015, top + 0.63)]), tc, ink, 0.014)
        if sp.get("torn"):
            # rips with darker inside + stains
            for (px, py, w, h) in ((0.18, sy + 0.42, 0.16, 0.12), (-0.25, sy + 0.70, 0.13, 0.10)):
                x_, v = _cyl_x(px * 120, a, b, th)
                if v < 0.2:
                    continue
                rp = [(x_ - w / 2, py), (x_ - w / 4, py - h / 2), (x_, py - h * 0.1), (x_ + w / 3, py - h / 2), (x_ + w / 2, py + h * 0.1),
                      (x_ + w / 6, py + h / 2), (x_ - w / 5, py + h * 0.2)]
                inner += path(pts_d(rp), sp["skin_dk"], ink, 0.014)
            for (px, py, r) in ((-0.10, sy + 0.25, 0.05), (0.22, sy + 0.95, 0.07), (-0.2, sy + 1.05, 0.04)):
                x_, v = _cyl_x(px * 120, a, b, th)
                if v > 0.2:
                    inner += ell(x_, py, r, r * 0.7, c["stain"], None)
        # collar
    # side shade band for non-rescue outfits
    if out != "rescue" and view != "front":
        inner += path(smooth_d([(cx - s * ahalf * 1.1, top), (cx - s * ahalf * 0.80, sy + 0.2), (cx - s * bhalf * 0.88, hem + 0.05),
                                (cx - s * bhalf * 1.2, hem + 0.05), (cx - s * ahalf * 1.2, sy)], True, 0.3), "#000000", None, 0,
                      ' fill-opacity="0.10"')
    o += '<g clip-path="url(#%s)">%s</g>' % (clip_id, inner)
    # re-stroke the outline over the clipped detail
    o += path(smooth_d(body, True, 0.25), "none", ink, bw)
    # hem: a torn jagged hem for the driver
    if sp.get("torn"):
        jag = []
        n = 9
        for k in range(n + 1):
            x = cx - bhalf + 2 * bhalf * k / n
            jag.append((x, hem + (0.07 if k % 2 else 0.0) + 0.02))
        o += path(pts_d([(cx - bhalf, hem - 0.03)] + jag + [(cx + bhalf, hem - 0.03)]), shirt, ink, 0.02)
    # -- collar
    if pose.get("back"):
        o += path("M%s %s Q0 %s %s %s L%s %s Q0 %s %s %s Z" % (f(-0.24), f(top - 0.02), f(top - 0.07), f(0.24), f(top - 0.02), f(0.24), f(top + 0.05),
                                                           f(top + 0.01), f(-0.24), f(top + 0.05)), shirt, ink, 0.022)
    else:
        o += _collar(sp, view, s, th, top, a, b, shirt)
    # -- belt
    if out not in ("dress",):
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
            f(cx - bhalf - 0.01), f(belt - 0.065), f(2 * bhalf + 0.02), f(0.13 if out == "rescue" else 0.08), c.get("belt", "#1b1b19"), ink, f(bw * 0.8))
        bx, bv = _cyl_x(2, a * 0.92, b, th)
        if bv > 0.1:
            bh = 0.10 if out == "rescue" else 0.07
            o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.01" fill="none" stroke="%s" stroke-width="0.022"/>' % (
                f(bx - 0.065 * bv), f(belt - bh / 2 - (0.0 if out == "rescue" else 0.015)), f(0.13 * bv), f(bh), c.get("buckle", "#c9c9c4"))
    # -- radio clipped on the screen-right chest strap (character's left), antenna up to chin height
    if sp.get("radio") and not pose.get("back"):
        big = bool(sp.get("pack"))
        rx, rv = _cyl_x(40 if big else 30, a * 0.85, b, th)
        if rv > 0.0:
            k_ = max(rv, 0.9 if view != "side" else 0.6)
            rw, rh = (0.25 if big else 0.14) * k_, (0.40 if big else 0.25)
            ry = sy - 0.10 if big else sy + 0.06
            ax = rx - rw * 0.22
            o += line((ax, ry + 0.02), (ax, ry - (0.30 if big else 0.20)), ink, 0.062 if big else 0.040)
            o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.03" fill="%s" stroke="%s" stroke-width="0.030"/>' % (
                f(rx - rw / 2), f(ry), f(rw), f(rh), "#2e2f33", ink)
            o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.01" fill="#6fa8dc"/>' % (f(rx - rw * 0.30), f(ry + 0.045), f(rw * 0.60), f(rh * 0.20))
            for k in range(3):
                for j in (-1, 0, 1):
                    o += ell(rx + j * rw * 0.24, ry + rh * 0.48 + k * rh * 0.14, 0.012, 0.010, "#0e0e0d")
    # -- hip pouches
    if sp.get("hip_pouches") and not pose.get("back"):
        for phi, kind in ((-68, "pouch"), (70, "holster")):
            px, pv = _cyl_x(phi, a * 1.02, b, th)
            if pv < -0.25:
                continue
            w = 0.17 * max(pv, 0.45)
            o += '<rect x="%s" y="%s" width="%s" height="0.24" rx="0.03" fill="%s" stroke="%s" stroke-width="0.022"/>' % (
                f(px - w / 2), f(belt - 0.04), f(w), c["vest"], ink)
            o += line((px - w / 2, belt + 0.03), (px + w / 2, belt + 0.03), "#3a3a3a", 0.012)
            if kind == "holster":
                o += '<rect x="%s" y="%s" width="%s" height="0.045" fill="%s"/>' % (f(px - w * 0.35), f(belt + 0.10), f(w * 0.7), c["shirt"])
    return o


def _scooter_logo(x, y, sz):
    s = sz
    o = ell(x - 0.32 * s, y + 0.22 * s, 0.11 * s, 0.11 * s, "#f4f4f0")
    o += ell(x + 0.32 * s, y + 0.22 * s, 0.11 * s, 0.11 * s, "#f4f4f0")
    o += path(pts_d([(x - 0.42 * s, y + 0.12 * s), (x + 0.10 * s, y + 0.12 * s), (x + 0.22 * s, y - 0.25 * s), (x + 0.36 * s, y - 0.25 * s),
                     (x + 0.42 * s, y + 0.15 * s), (x - 0.42 * s, y + 0.18 * s)]), "#f4f4f0")
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="#f4f4f0"/>' % (f(x - 0.40 * s), f(y - 0.16 * s), f(0.34 * s), f(0.22 * s))
    return o


def _collar(sp, view, s, th, top, a, b, shirt):
    ink = sp["ink"]
    out = sp["outfit"]
    zx, zv = _cyl_x(3, a, b, th)
    o = ""
    under = sp["col"].get("under", "#2a2a2a") if out == "rescue" else sp["skin"]
    if out in ("tee", "hoodie", "dress"):
        o += path("M%s %s Q%s %s %s %s" % (f(zx - 0.17), f(top + 0.01), f(zx), f(top + 0.12), f(zx + 0.17), f(top + 0.01)), "none", ink, 0.026)
        return o
    # V of the under layer (dark t-shirt for the rescue shirt, skin/undershirt for the office shirt)
    vw = 0.13
    o += path(pts_d([(zx - vw, top - 0.005), (zx + vw, top - 0.005), (zx, top + 0.17)]), under, ink, 0.018)
    if out == "office" or sp.get("tie"):
        pass
    cc = shirt if out != "blazer" else sp["col"].get("shirt", "#fff")
    if out == "delivery":
        cc = sp["col"]["jacket"]
    # big pointed collar wings
    for side in (-1, 1):
        if view == "side" and side == -s:
            continue
        x0 = zx + side * 0.02
        ww = 0.30 * (1.0 if view == "front" else (0.75 if side == s else 0.55))
        if view == "side":
            ww = 0.16
        wing = [(zx + side * 0.12 * (ww / 0.30), top - 0.03), (zx + side * ww, top + 0.02),
                (zx + side * 0.13 * (ww / 0.30), top + 0.24), (x0, top + 0.16)]
        o += path(pts_d(wing), cc, ink, 0.022)
    return o


# ------------------------------------------------------------------------------------------------ limbs
def leg_layer(sp, pose, view, s, K, hip, foot, which, lift=0.0, toe=0.0, knee_bias=None):
    """one leg: trouser tube hip -> knee -> ankle, knee pad, thigh pouch, boot/shoe.  foot = sole contact point
    under the ankle (x, y).  Returns (svg, anchors)."""
    c = sp["col"]
    ink = sp["ink"]
    bw = sp["body_ink"]
    lw = sp["leg_w"]
    ank_h = min(sp["boot_h"] * 0.42, 0.24)
    ankle = (foot[0], foot[1] - ank_h)
    leg_len = sp["legs"] + 0.06 - ank_h                 # constant: the bob moves the hip, never the bone lengths
    l1 = leg_len * 0.5
    l2 = leg_len * 0.5
    if view == "front":
        bend = 1 if hip[0] < 0 else -1               # knees bow a touch outward
        if knee_bias is not None:
            bend = knee_bias
    else:
        bend = -s if knee_bias is None else knee_bias  # the knee points toward the facing side
    knee, ank = ik2(hip, ankle, l1, l2, bend)
    trouser = c["trouser"]
    o = ""
    w_th = (lw - 2 * bw) * (1.0 if view != "side" else 0.95)          # outer (ink to ink) width = leg_w
    w_sh = (lw - 2 * bw) * 0.92
    if sp.get("shorts"):
        # shorts end above the knee, bare shins
        mid = lerp(hip, knee, 0.75)
        o += poly_stroke([hip, mid], ink, w_th + 2 * bw, cap="butt")
        o += poly_stroke([knee, ank], ink, sp["forearm"] * 1.1 + 2 * bw)
        o += poly_stroke([knee, ank], sp["skin"], sp["forearm"] * 1.1)
        o += poly_stroke([mid, knee], ink, sp["forearm"] * 1.2 + 2 * bw)
        o += poly_stroke([mid, knee], sp["skin"], sp["forearm"] * 1.2)
        o += poly_stroke([hip, mid], trouser, w_th, cap="butt")
        o += poly_stroke([hip, mid], ink, 0.0001)
        o += line(add(mid, nrm((-(knee[1] - hip[1]), knee[0] - hip[0])), w_th / 2 + bw / 2),
                  add(mid, nrm((-(knee[1] - hip[1]), knee[0] - hip[0])), -w_th / 2 - bw / 2), ink, bw)
    elif sp.get("skirt"):
        o += poly_stroke([knee, ank], ink, sp["forearm"] * 1.1 + 2 * bw)
        o += poly_stroke([knee, ank], sp.get("legwear", sp["skin"]), sp["forearm"] * 1.1)
    else:
        # ink underlay then fill: one clean outline around thigh + shin
        o += poly_stroke([hip, knee], ink, w_th + 2 * bw, cap="square")
        o += poly_stroke([knee, ank], ink, w_sh + 2 * bw)
        o += poly_stroke([knee, ank], trouser, w_sh)
        o += poly_stroke([hip, knee], trouser, w_th, cap="square")
        # crease
        dirv = nrm(sub(ank, knee))
        o += line(add(lerp(knee, ank, 0.1), (dirv[1] * -1 * s, dirv[0] * s), w_sh * 0.15), add(lerp(knee, ank, 0.75), (dirv[1] * -1 * s, dirv[0] * s), w_sh * 0.12),
                  sp["col"].get("trouser_dk", shade(trouser, 0.3)), 0.012)
    # thigh pouch with a strap band
    if sp.get("thigh_pouch") and which in ("r", "n", "R"):
        tdir = nrm(sub(knee, hip))
        pc = lerp(hip, knee, 0.62)
        ang = math.degrees(math.atan2(tdir[1], tdir[0])) - 90
        px = pc[0] + (lw * 0.12 * (s if view != "front" else (1 if hip[0] > 0 else -1)))
        o += g('<rect x="-0.12" y="-0.15" width="0.24" height="0.30" rx="0.03" fill="%s" stroke="%s" stroke-width="0.022"/>' % (
            c["trouser_dk"], ink) + line((-0.12, -0.08), (0.12, -0.08), ink, 0.014) +
            '<rect x="%s" y="-0.21" width="%s" height="0.055" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
                f(-w_th / 2 - 0.005), f(w_th + 0.01), "#1b1b19", ink), "translate(%s %s) rotate(%s)" % (f(px), f(pc[1]), f(ang)))
    # knee pad
    if sp.get("kneepads") and view != "side" or (sp.get("kneepads") and view == "side"):
        kdir = nrm(sub(ank, hip))
        ang = math.degrees(math.atan2(kdir[1], kdir[0])) - 90
        kp = add(knee, (0, 0.02))
        wpad = w_sh * (1.0 if view == "front" else 0.8)
        o += g('<rect x="%s" y="-0.12" width="%s" height="0.24" rx="0.07" fill="%s" stroke="%s" stroke-width="0.022"/>' % (
            f(-wpad / 2 + (0 if view == "front" else s * 0.04)), f(wpad), "#2a2928", ink),
            "translate(%s %s) rotate(%s)" % (f(kp[0]), f(kp[1]), f(ang)))
    # boot / shoe
    o += _foot(sp, view, s, ank, foot, lift, toe, which)
    return o, dict(hip=hip, knee=knee, ankle=ank, foot=foot)


def _foot(sp, view, s, ank, foot, lift, toe, which):
    c = sp["col"]
    ink = sp["ink"]
    bw = sp["body_ink"]
    bh = sp["boot_h"]
    kind = sp.get("shoe", "boot")
    bcol = c.get("boot", "#383838")
    scol = c.get("sole", "#1c1c1c")
    sole_len = {"front": sp["sole_len"][0], "q": sp["sole_len"][1], "side": sp["sole_len"][2]}[view]
    gy = foot[1]
    o = ""
    rot = toe
    if view == "front":
        w = sp["boot_w"]
        x = foot[0]
        top = gy - bh
        if kind in ("boot", "sneaker_high"):
            shaft = [(x - w * 0.42, top), (x + w * 0.42, top), (x + w * 0.46, gy - 0.16), (x + w * 0.56, gy - 0.05), (x + w * 0.56, gy),
                     (x - w * 0.56, gy), (x - w * 0.56, gy - 0.05), (x - w * 0.46, gy - 0.16)]
            o += path(smooth_d(shaft, True, 0.12), bcol, ink, bw)
            o += '<rect x="%s" y="%s" width="%s" height="0.06" rx="0.02" fill="%s" stroke="%s" stroke-width="%s"/>' % (
                f(x - w * 0.6), f(gy - 0.045), f(w * 1.2), scol, ink, f(bw * 0.7))
            if kind == "boot":
                for k in range(3):                                         # laces
                    yy = top + 0.10 + k * 0.08
                    o += line((x - w * 0.18, yy), (x + w * 0.18, yy + 0.03), "#5a5a5a", 0.014)
                o += path("M%s %s Q%s %s %s %s" % (f(x - w * 0.45), f(gy - 0.12), f(x), f(gy - 0.2), f(x + w * 0.45), f(gy - 0.12)), stroke="#4a4a4a", sw=0.014)
            else:
                o += path("M%s %s Q%s %s %s %s" % (f(x - w * 0.5), f(gy - 0.08), f(x), f(gy - 0.16), f(x + w * 0.5), f(gy - 0.08)), "none", "#f4f4f0", 0.04)
        else:                                                              # low shoe / sneaker / sandal
            sh = [(x - w * 0.40, gy - bh), (x + w * 0.40, gy - bh), (x + w * 0.55, gy - 0.06), (x + w * 0.55, gy), (x - w * 0.55, gy),
                  (x - w * 0.55, gy - 0.06)]
            o += path(smooth_d(sh, True, 0.2), bcol, ink, bw)
            o += line((x - w * 0.55, gy - 0.02), (x + w * 0.55, gy - 0.02), scol, 0.03)
        return o
    # q / side: profile boot pointing toward s
    L = sole_len
    heel = -L * 0.32
    toe_x = L * 0.68
    if view == "q":
        heel, toe_x = -L * 0.38, L * 0.62
    pts = [(heel, -bh), (heel + 0.30 * L if kind != "shoe" else heel + 0.2 * L, -bh), (heel + 0.40 * L, -0.24 if kind != "shoe" else -bh * 0.6),
           (toe_x - 0.06, -0.20 if kind != "shoe" else -bh * 0.75), (toe_x, -0.10), (toe_x + 0.01, -0.0), (heel - 0.01, 0.0)]
    if kind == "shoe":
        pts = [(heel, -bh), (heel + 0.42 * L, -bh), (toe_x - 0.05, -bh * 0.55), (toe_x, -0.06), (toe_x, 0.0), (heel - 0.01, 0.0)]
    tr = "translate(%s %s) scale(%s 1) rotate(%s)" % (f(foot[0]), f(gy), f(s), f(rot * s))
    inner = path(smooth_d(pts, True, 0.14), bcol, ink, bw)
    inner += '<rect x="%s" y="-0.05" width="%s" height="0.055" rx="0.02" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        f(heel - 0.02), f(toe_x - heel + 0.04), scol, ink, f(bw * 0.7))
    if kind == "boot":
        for k in range(3):
            yy = -bh + 0.12 + k * 0.08
            inner += line((heel + 0.30 * L, yy), (heel + 0.42 * L, yy + 0.03), "#5a5a5a", 0.014)
        inner += path("M%s %s Q%s %s %s %s" % (f(toe_x - 0.17), f(-0.05), f(toe_x - 0.13), f(-0.19), f(toe_x - 0.02), f(-0.13)), stroke="#4a4a4a", sw=0.014)
    elif kind == "sneaker_high":
        inner += path("M%s %s L%s %s" % (f(heel + 0.1), f(-0.10), f(toe_x - 0.05), f(-0.10)), stroke="#f4f4f0", sw=0.05)
    return g(inner, tr)


def arm_layer(sp, pose, view, s, shoulder, hand, which, elbow=None, hand_shape=None, front_view_side=1):
    """one arm: sleeve, (bare) forearm, glove/hand.  Returns (svg, anchors)."""
    c = sp["col"]
    ink = sp["ink"]
    bw = sp["body_ink"]
    la, lf = sp["upper_arm"], sp["fore_arm"]
    if elbow is None:
        elbow = -front_view_side if view == "front" else s
    wrist_target = hand
    el, wr = ik2(shoulder, wrist_target, la, lf, elbow)
    o = ""
    sleeve_col = c.get("shirt", "#888")
    out = sp["outfit"]
    if out == "blazer":
        sleeve_col = c["jacket"]
    if out == "delivery":
        sleeve_col = c["jacket"]
    fw = sp["forearm"]
    sw_ = sp["sleeve_w"]
    if sp["sleeve"] == "short":
        cuff = lerp(shoulder, el, 0.92)
        # bare forearm (white tube) from just inside the sleeve to the wrist
        o += poly_stroke([lerp(shoulder, el, 0.7), el, wr], ink, fw + 2 * bw)
        o += poly_stroke([lerp(shoulder, el, 0.7), el, wr], sp["skin"], fw)
        # sleeve: tapered tube shoulder -> cuff
        d = nrm(sub(cuff, shoulder))
        n_ = (-d[1], d[0])
        w0, w1 = sw_ * 0.55, sw_ * 0.47
        sh0 = add(shoulder, d, -0.04)
        sl = [add(sh0, n_, w0), add(cuff, n_, w1), add(cuff, n_, -w1), add(sh0, n_, -w0)]
        cap = add(shoulder, d, -0.16)
        sp_ = [sl[0], lerp(sl[0], sl[1], 0.5), sl[1], sl[2], lerp(sl[2], sl[3], 0.5), sl[3], add(cap, n_, -w0 * 0.6), cap, add(cap, n_, w0 * 0.6)]
        o += path(smooth_d(sp_, True, 0.25), sleeve_col, ink, bw)
        o += line(add(cuff, n_, w1 * 0.95), add(cuff, n_, -w1 * 0.95), shade(sleeve_col, 0.35), 0.016)
        if sp.get("flag") and which in ("R",):
            o += _flag_patch(lerp(shoulder, cuff, 0.45), d, n_, w0 * 1.25)
    else:
        # long sleeve: tube to the wrist, cuff
        cuff = lerp(el, wr, 0.92)
        o += poly_stroke([shoulder, el, cuff], ink, sw_ + 2 * bw)
        o += poly_stroke([shoulder, el, cuff], sleeve_col, sw_)
        dd = nrm(sub(cuff, el))
        nn = (-dd[1], dd[0])
        o += line(add(cuff, nn, sw_ * 0.5), add(cuff, nn, -sw_ * 0.5), shade(sleeve_col, 0.4), 0.016)
        if sp.get("flag") and which == "R":
            d = nrm(sub(el, shoulder))
            o += _flag_patch(lerp(shoulder, el, 0.42), d, (-d[1], d[0]), sw_ * 0.6)
        if sp.get("torn") and which == "L":
            rp = lerp(shoulder, el, 0.6)
            o += path(pts_d([(rp[0] - 0.06, rp[1]), (rp[0] - 0.02, rp[1] - 0.04), (rp[0] + 0.04, rp[1] - 0.01), (rp[0] + 0.05, rp[1] + 0.05),
                             (rp[0] - 0.01, rp[1] + 0.03)]), sp.get("skin_dk", "#777"), ink, 0.012)
    # hand
    hs = hand_shape or ("glove" if sp.get("glove") else ("claw" if sp.get("claws") else "hand"))
    o += _hand(sp, wr, nrm(sub(wr, el)), hs, s, which, view)
    return o, dict(shoulder=shoulder, elbow=el, wrist=wr, hand=add(wr, nrm(sub(wr, el)), sp["hand"] * 0.45))


def _flag_patch(p, d, n_, w):
    dev = math.degrees(math.atan2(d[0], d[1] if abs(d[1]) > 1e-6 else 1e-6))      # arm deviation from straight down
    if d[1] < 0:
        dev = 0.0
    tilt = max(-22.0, min(22.0, -dev * 0.7))
    hw, hh = w * 0.80, w * 0.54
    o = '<rect x="%s" y="%s" width="%s" height="%s" fill="#f4f4f0" stroke="%s" stroke-width="0.016"/>' % (f(-hw), f(-hh), f(2 * hw), f(2 * hh), INK)
    for k, col in enumerate(("#d5262b", "#f6f5f0", "#1f4f9e", "#1f4f9e", "#f6f5f0", "#d5262b")):
        o += '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(-hw), f(-hh + k * 2 * hh / 6), f(2 * hw), f(2 * hh / 6 + 0.002), col)
    o += '<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="0.016"/>' % (f(-hw), f(-hh), f(2 * hw), f(2 * hh), INK)
    return g(o, "translate(%s %s) rotate(%s)" % (f(p[0]), f(p[1]), f(tilt)))


def _hand(sp, wr, d, shape, s, which, view):
    ink = sp["ink"]
    hsz = sp["hand"]
    col = sp["col"].get("glove", "#333333") if sp.get("glove") else sp["skin"]
    ang = math.degrees(math.atan2(d[1], d[0])) - 90          # local +y along the forearm
    side = 1 if which in ("L",) else -1
    if view == "front":
        side = -1 if which == "R" else 1
    else:
        side = s
    o = ""
    if shape in ("glove", "fist", "grip", "hand"):
        w, h = hsz * 0.92, hsz * 0.95
        # palm mitten + thumb + knuckle lines
        o += ell(0, h * 0.48, w / 2, h / 2, col, ink, sp["body_ink"])
        o += ell(side * w * 0.42, h * 0.32, w * 0.20, h * 0.26, col, ink, sp["body_ink"] * 0.9, rot=-side * 25)
        o += ell(0, h * 0.48, w / 2 - 0.02, h / 2 - 0.02, col)
        if sp.get("glove"):
            o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.02" fill="%s" stroke="%s" stroke-width="0.018"/>' % (
                f(-w * 0.42), f(-0.02), f(w * 0.84), f(h * 0.2), shade(col, 0.3), ink)
        for k in range(3):
            o += line((-w * 0.28 + k * w * 0.2, h * 0.78), (-w * 0.28 + k * w * 0.2, h * 0.92), shade(col, 0.6) if sp.get("glove") else ink, 0.014)
    elif shape == "claw":
        w, h = hsz * 1.0, hsz * 1.0
        o += ell(0, h * 0.35, w / 2, h * 0.38, col, ink, sp["body_ink"])
        for k in range(4):
            a = math.radians(-35 + k * 23)
            p0 = (math.sin(a) * w * 0.35, h * 0.55)
            p1 = (math.sin(a) * w * 0.62, h * 0.95)
            p2 = (math.sin(a) * w * 0.55 + 0.03 * side, h * 1.12)
            o += poly_stroke([p0, p1], ink, 0.055)
            o += poly_stroke([p0, p1], col, 0.03)
            o += path(pts_d([add(p1, (-0.018, 0)), add(p1, (0.018, 0)), p2]), "#e9e4cf", ink, 0.012)
        o += ell(side * w * 0.45, h * 0.30, w * 0.15, h * 0.2, col, ink, sp["body_ink"] * 0.8, rot=-side * 30)
    elif shape == "point":
        w, h = hsz * 0.85, hsz * 0.8
        o += ell(0, h * 0.45, w / 2, h / 2, col, ink, sp["body_ink"])
        o += poly_stroke([(0, h * 0.7), (0, h * 1.35)], ink, 0.095)
        o += poly_stroke([(0, h * 0.7), (0, h * 1.35)], col, 0.05)
    elif shape == "open":
        w, h = hsz * 0.9, hsz * 0.9
        o += ell(0, h * 0.42, w / 2, h * 0.42, col, ink, sp["body_ink"])
        for k in range(4):
            x = -w * 0.33 + k * w * 0.22
            o += poly_stroke([(x, h * 0.6), (x * 1.2, h * 1.08)], ink, 0.07)
            o += poly_stroke([(x, h * 0.6), (x * 1.2, h * 1.08)], col, 0.035)
        o += ell(side * w * 0.5, h * 0.3, w * 0.14, h * 0.24, col, ink, sp["body_ink"] * 0.8, rot=-side * 40)
    return g(o, "translate(%s %s) rotate(%s)" % (f(wr[0]), f(wr[1]), f(ang)))


# ------------------------------------------------------------------------------------------------ props
def prop_svg(kind, P, sp=None):
    """prop drawn in its own frame: grip at the origin, its long axis along +y (down), then rotated by P['angle']."""
    o = ""
    if kind == "cutter":
        bars = int(P.get("bars", 3))
        wet = P.get("wet", False)
        org = "#ee7a1f" if not wet else "#d0621a"
        # D-handle loop around the grip (black)
        o += path("M-0.20 -0.06 C-0.32 -0.34 0.24 -0.40 0.18 -0.08", "none", INK, 0.10)
        o += path("M-0.20 -0.06 C-0.32 -0.34 0.24 -0.40 0.18 -0.08", "none", "#2a2a2a", 0.05)
        # orange body (cylinder) with a white band
        o += '<rect x="-0.13" y="-0.10" width="0.26" height="0.62" rx="0.07" fill="%s" stroke="%s" stroke-width="0.03"/>' % (org, INK)
        o += '<rect x="-0.11" y="-0.06" width="0.06" height="0.52" rx="0.03" fill="#fbc48d" opacity="0.55"/>'
        o += '<rect x="-0.13" y="0.10" width="0.26" height="0.07" fill="#f4f2ec" stroke="%s" stroke-width="0.016"/>' % INK
        # battery gauge box with 3 bars (green 3, yellow 2, red 1)
        o += '<rect x="-0.105" y="0.21" width="0.21" height="0.22" rx="0.02" fill="#151515" stroke="%s" stroke-width="0.02"/>' % INK
        colr = {3: "#3ee05a", 2: "#f2d22e", 1: "#ff3b30", 0: "#333"}[max(0, min(3, bars))]
        for k in range(3):
            on = (2 - k) < bars
            o += '<rect x="-0.075" y="%s" width="0.15" height="0.048" rx="0.008" fill="%s"/>' % (f(0.235 + k * 0.064), colr if on else "#3a3a3a")
        # black collar, then two silver jaws opened in a V
        o += '<rect x="-0.15" y="0.50" width="0.30" height="0.11" rx="0.03" fill="#222" stroke="%s" stroke-width="0.024"/>' % INK
        o += ell(0, 0.66, 0.06, 0.06, "#bfc4ca", INK, 0.02)
        for side in (-1, 1):
            jaw = [(side * 0.02, 0.62), (side * 0.16, 0.70), (side * 0.20, 0.92), (side * 0.11, 1.10), (side * 0.05, 1.04), (side * 0.10, 0.88),
                   (side * 0.04, 0.72)]
            o += path(smooth_d(jaw, True, 0.25), "#b9bfc6", INK, 0.026)
            o += path(pts_d([(side * 0.07, 0.74), (side * 0.15, 0.90), (side * 0.10, 1.02)], False), "none", "#dfe3e8", 0.016)
        o += ell(0, 0.66, 0.03, 0.03, "#555")
    elif kind == "phone":
        w, h = 0.17, 0.33
        o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.03" fill="#1c1d22" stroke="%s" stroke-width="0.022"/>' % (f(-w / 2), f(-h * 0.7), f(w), f(h), INK)
        scr = P.get("screen")
        if scr:
            o += '<image href="%s" x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none"/>' % (
                scr, f(-w / 2 + 0.012), f(-h * 0.7 + 0.014), f(w - 0.024), f(h - 0.028))
        else:
            o += '<rect x="%s" y="%s" width="%s" height="%s" fill="#3b5d9a"/>' % (f(-w / 2 + 0.012), f(-h * 0.7 + 0.014), f(w - 0.024), f(h - 0.028))
    elif kind == "umbrella":
        col = P.get("col", "#2f6fb3")
        o += line((0, 0.25), (0, -1.75), INK, 0.035)
        o += g(path("M-0.75 -1.05 Q0 -1.62 0.75 -1.05 Q0.56 -1.13 0.37 -1.05 Q0.19 -1.13 0 -1.05 Q-0.19 -1.13 -0.37 -1.05 Q-0.56 -1.13 -0.75 -1.05 Z",
                  col, INK, 0.03), "translate(0 -0.62)")
        o += path("M0 0.25 Q0 0.36 -0.08 0.34", "none", INK, 0.035)
    elif kind == "bag":
        col = P.get("col", "#6b4a2e")
        o += path("M-0.12 0.05 Q0 -0.2 0.12 0.05", "none", INK, 0.03)
        o += '<rect x="-0.22" y="0.04" width="0.44" height="0.36" rx="0.05" fill="%s" stroke="%s" stroke-width="0.03"/>' % (col, INK)
    elif kind == "helmet":
        o += ell(0, 0.15, 0.30, 0.28, "#f4f4f0", INK, 0.03)
        o += path("M-0.24 0.16 Q0 0.02 0.27 0.14 L0.26 0.32 Q0 0.40 -0.2 0.32 Z", "#2a3240", INK, 0.025)
    return g(o, "translate(%s %s) rotate(%s)%s" % (f(P["at"][0]), f(P["at"][1]), f(P.get("angle", 0.0)),
                                                     " scale(%s)" % f(P["scale"]) if P.get("scale") else ""))


def pack_layer(sp, view, s, K):
    if not sp.get("pack") and not sp.get("box"):
        return ""
    c = sp["col"]
    ink = sp["ink"]
    chin = K["chin"]
    sy = K["shoulder_y"]
    th = s * BODY_YAW[view]
    a = sp["chest"] / 2
    if sp.get("box"):                                        # delivery box (green)
        bx = {"front": -0.40, "q": -s * 0.55, "side": -s * 0.70}[view]
        w = {"front": 1.0, "q": 0.95, "side": 0.75}[view]
        x0 = bx - w / 2
        o = '<rect x="%s" y="%s" width="%s" height="0.92" rx="0.06" fill="%s" stroke="%s" stroke-width="0.03"/>' % (f(x0), f(sy - 0.25), f(w), c.get("box", "#3fa34d"), ink)
        o += line((x0 + 0.04, sy - 0.12), (x0 + w - 0.04, sy - 0.12), shade(c.get("box", "#3fa34d"), 0.35), 0.02)
        o += _scooter_logo(x0 + w / 2, sy + 0.25, 0.28)
        return o
    # backpack: shows on the screen-left side behind the shoulder in the front drawing (sheet), behind the back otherwise
    if view == "front":
        cx = -0.08
        w = 1.0 + 0.10
        x0 = cx - w / 2 - 0.05
    elif view == "q":
        cx = -s * 0.32
        w = 0.95
        x0 = cx - w / 2
    else:
        cx = -s * 0.55
        w = 0.58
        x0 = cx - w / 2
    y0 = sy - 0.20
    h = 1.10
    o = '<rect x="%s" y="%s" width="%s" height="%s" rx="0.10" fill="%s" stroke="%s" stroke-width="0.032"/>' % (f(x0), f(y0), f(w), f(h), c["pack"], ink)
    o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.06" fill="%s" stroke="%s" stroke-width="0.022"/>' % (
        f(x0 + 0.06), f(y0 + h * 0.48), f(w * 0.5), f(h * 0.4), c["pack_dk"], ink)
    o += '<rect x="%s" y="%s" width="0.12" height="0.045" fill="#d2452a"/>' % (f(x0 + 0.08), f(y0 + 0.07))
    o += line((x0 + 0.05, y0 + 0.2), (x0 + w - 0.05, y0 + 0.2), shade(c["pack"], 0.4), 0.014)
    return o


# ------------------------------------------------------------------------------------------------ presets
ARMS = {
    # hand targets relative to the shoulder, for an arm on the screen-right side in the front view / near arm facing right
    "down": dict(hand=(0.03, 1.05), elbow=None),
    "hang": dict(hand=(0.08, 1.02), elbow=None),
    "hips": dict(hand=(-0.18, 0.80), elbow=None, out=True),
    "hold_cutter": dict(hand=(0.10, 0.92), elbow=None, hand_shape="grip"),
    "phone_ear": dict(hand=(0.08, -0.60), elbow=None, hand_shape="grip"),
    "phone_look": dict(hand=(-0.20, 0.38), elbow=None, hand_shape="grip"),
    "point": dict(hand=(0.95, -0.10), elbow=None, hand_shape="point"),
    "raise": dict(hand=(0.30, -0.95), elbow=None, hand_shape="open"),
    "wave": dict(hand=(0.45, -0.75), elbow=None, hand_shape="open"),
    "reach": dict(hand=(0.95, 0.18), elbow=None, hand_shape="open"),
    "claw": dict(hand=(0.85, 0.05), elbow=None, hand_shape="claw"),
    "claw_up": dict(hand=(0.80, -0.30), elbow=None, hand_shape="claw"),
    "lap": dict(hand=(0.30, 0.75), elbow=None),
    "wheel": dict(hand=(0.75, 0.30), elbow=None),
    "cross": dict(hand=(-0.45, 0.55), elbow=None),
    "head": dict(hand=(-0.15, -0.70), elbow=None, hand_shape="open"),
    "pocket": dict(hand=(0.02, 0.78), elbow=None, hidden_hand=True),
    "carry": dict(hand=(-0.10, 0.60), elbow=None),
    "umbrella": dict(hand=(0.10, 0.40), elbow=None, hand_shape="grip"),
    "shout": dict(hand=(-0.12, -0.42), elbow=None, hand_shape="open"),
    "guard": dict(hand=(0.40, 0.25), elbow=None, hand_shape="open"),
}

LEGS = {
    "stand": dict(feet=(0.30, 0.30), spread_q=(0.10, -0.12)),
    "wide": dict(feet=(0.40, 0.40), spread_q=(0.25, -0.25)),
    "step": dict(feet=(0.30, 0.22), spread_q=(0.32, -0.28)),
    "lunge": dict(feet=(0.36, 0.30), spread_q=(0.62, -0.50), hip=(0.10, 0.18)),
    "crouch": dict(feet=(0.34, 0.34), spread_q=(0.20, -0.20), hip=(0.0, 0.40)),
}


def _arm_target(sp, pose, view, s, key, shoulder, outward):
    a = pose.get(key, "down")
    if isinstance(a, str):
        A = dict(ARMS.get(a, ARMS["down"]))
    else:
        A = dict(a)
    hx, hy = A.get("hand", (0.1, 1.0))
    if not A.get("absolute"):
        hand = (shoulder[0] + hx * outward, shoulder[1] + hy)
    else:
        hand = (hx, hy)
    el = A.get("elbow")
    if el is not None:
        el = el * outward
    return hand, el, A.get("hand_shape"), A.get("hidden_hand", False)


# ------------------------------------------------------------------------------------------------ build
def build(spec, pose=None):
    sp = get_spec(spec)
    pose = dict(pose or {})
    view = pose.get("view", "front")
    back = view == "back"
    if back:
        view = "front"
        pose["back"] = True
    s = 1 if pose.get("s", 1) >= 0 else -1
    if view == "front":
        s = 1 if pose.get("s", 1) >= 0 else -1
    K = skeleton(sp, pose)
    lean = pose.get("lean", 0.0)
    layers = []
    anchors = {}
    hip_y = K["hip_y"]
    # upper body pivots about the hip centre by `lean` (positive leans toward the facing side)
    piv = (K["hip_dx"], hip_y + 0.05)
    lean_tr = "rotate(%s %s %s)" % (f(lean * s), f(piv[0]), f(piv[1])) if lean else None
    up_shift = (K["hip_dx"], hip_y - (-sp["legs"] - 0.06))   # bob / crouch moves the whole upper body
    up_tr = "translate(%s %s)" % (f(up_shift[0]), f(up_shift[1]))

    def U(p):                                   # a point of the upper body -> figure coordinates
        q = (p[0] + up_shift[0], p[1] + up_shift[1])
        return rot_pt(q, lean * s, piv) if lean else q

    def upg(svg):
        inner = g(svg, up_tr)
        return g(inner, lean_tr) if lean_tr else inner

    # ---------------- legs
    Lg = pose.get("legs", "stand")
    th = s * BODY_YAW[view]
    hipw = sp["leg_w"] / 2 + 0.012                     # the legs part right at the crotch (sheet)
    if view == "front":
        hips = {"R": (-hipw + K["hip_dx"], hip_y), "L": (hipw + K["hip_dx"], hip_y)}
    else:
        dz = hipw * math.cos(math.radians(BODY_YAW[view])) * 0.6
        # near hip (character's left when facing right) sits a touch toward the viewer side
        near = "L" if s > 0 else "R"
        far = "R" if s > 0 else "L"
        hips = {near: (K["hip_dx"] + s * dz * 0.3, hip_y), far: (K["hip_dx"] - s * dz * 0.3, hip_y - 0.01)}
    feet = {}
    lifts = {"R": 0.0, "L": 0.0}
    toes = {"R": 0.0, "L": 0.0}
    if isinstance(Lg, dict) and ("foot_n" in Lg or "foot_R" in Lg):
        if view == "front":
            feet["R"] = Lg.get("foot_R", (-0.27, 0.0))
            feet["L"] = Lg.get("foot_L", (0.27, 0.0))
        else:
            near = "L" if s > 0 else "R"
            far = "R" if s > 0 else "L"
            feet[near] = Lg["foot_n"]
            feet[far] = Lg["foot_f"]
            toes[near] = Lg.get("toe_n", 0.0)
            toes[far] = Lg.get("toe_f", 0.0)
    elif isinstance(Lg, dict) and Lg.get("seated"):
        feet = None
    else:
        P = LEGS.get(Lg if isinstance(Lg, str) else "stand", LEGS["stand"])
        if view == "front":
            feet["R"] = (-P["feet"][0], 0.0)
            feet["L"] = (P["feet"][1], 0.0)
        else:
            near = "L" if s > 0 else "R"
            far = "R" if s > 0 else "L"
            feet[near] = (s * P["spread_q"][0] * (0.8 if view == "q" else 1.0), 0.0)
            feet[far] = (s * P["spread_q"][1] * (0.8 if view == "q" else 1.0), 0.0)
    seated = isinstance(Lg, dict) and Lg.get("seated") or Lg == "seated"
    leg_svgs = {}
    for side in ("R", "L"):
        if seated:
            # seated: thigh forward (foreshortened in front), shin down
            hp = hips[side]
            if view == "front":
                knee = (hp[0] * 1.15, hp[1] + 0.10)
                ft = (hp[0] * 1.2, hp[1] + sp["legs"] * 0.62)
            else:
                knee = (hp[0] + s * sp["legs"] * 0.48, hp[1] + 0.02)
                ft = (knee[0] + s * 0.06, hp[1] + sp["legs"] * 0.56)
            svg, an = _seated_leg(sp, view, s, hp, knee, ft, side)
        else:
            svg, an = leg_layer(sp, pose, view, s, K, hips[side], feet[side], side, lifts[side], toes[side],
                                knee_bias=(Lg.get("knee_bias") if isinstance(Lg, dict) else None))
        leg_svgs[side] = svg
        anchors["foot_" + side] = an.get("foot")
        anchors["knee_" + side] = an.get("knee")
        anchors["hip_" + side] = an.get("hip")
    # ---------------- torso, head
    torso = torso_layer(sp, pose, view, s, K)
    hd = pose.get("head", (0.0, 0.0, 0.0, 0.0))
    if len(hd) < 4:
        hd = tuple(hd) + (0.0,) * (4 - len(hd))
    hyaw, htilt, hdx, hdy = hd
    pose2 = dict(pose, head_yaw=hyaw)
    hc = (0.0 + s * (0.04 if view == "side" else 0.0) + hdx, K["head_c"] + hdy)
    head_svg, face_svg, hair_svg = head_layers(sp, pose2, view, s, hc, htilt * s)
    pack = pack_layer(sp, view, s, K)
    # ---------------- arms
    a_half = math.sqrt((sp["chest"] / 2 * math.cos(math.radians(th))) ** 2 + (sp["chest"] / 2 * 0.62 * math.sin(math.radians(th))) ** 2)
    shx = (sp["shoulder"] / 2 - sp["sleeve_w"] * (0.55 if sp["sleeve"] == "short" else 0.5) - sp["body_ink"])
    sh_y = K["shoulder_y"] + 0.05
    if view == "front":
        shoulders = {"R": (-shx, sh_y), "L": (shx, sh_y)}
        keys = {"R": pose.get("arm_r", pose.get("arm_R", "down")), "L": pose.get("arm_l", pose.get("arm_L", "down"))}
        outward = {"R": -1, "L": 1}
    else:
        near = "L" if s > 0 else "R"
        far = "R" if s > 0 else "L"
        sx_n = s * (a_half * (0.35 if view == "side" else 0.55))
        sx_f = -s * (a_half * (0.25 if view == "side" else 0.62))
        shoulders = {near: (sx_n, sh_y + 0.01), far: (sx_f, sh_y - 0.02)}
        keys = {near: pose.get("arm_n", pose.get("arm_" + near.lower(), "down")), far: pose.get("arm_f", pose.get("arm_" + far.lower(), "down"))}
        outward = {near: s, far: s}
    arm_svgs = {}
    prop_svgs = {}
    for side in ("R", "L"):
        sh = shoulders[side]
        hand, el, hshape, hidden = _arm_target(sp, {"k": keys[side]}, view, s, "k", sh, outward[side])
        if view != "front" and isinstance(keys[side], str) and keys[side] in ("down", "hang", "hold_cutter"):
            # hanging arms in profile: hand a little in front (near) / behind (far)
            hand = (sh[0] + (0.06 if side == ("L" if s > 0 else "R") else -0.02) * s, hand[1])
        svg, an = arm_layer(sp, pose, view, s, sh, hand, side, elbow=el, hand_shape=hshape,
                            front_view_side=(-1 if side == "R" else 1))
        arm_svgs[side] = svg
        for k_, v_ in an.items():
            anchors["%s_%s" % (k_, side)] = U(v_)
        # props in this hand
        pk = None
        if view == "front":
            pk = pose.get("prop_" + ("r" if side == "R" else "l"))
        else:
            pk = pose.get("prop_n" if side == ("L" if s > 0 else "R") else "prop_f") or pose.get("prop_" + side.lower())
        if pk:
            P = dict(pk) if isinstance(pk, dict) else {"type": pk}
            P.setdefault("angle", 0.0)
            P["at"] = an["wrist"] if P["type"] != "phone" else add(an["wrist"], nrm(sub(an["wrist"], an["elbow"])), sp["hand"] * 0.55)
            prop_front = P["type"] == "phone"            # the phone is held up in front of the glove (screen readable)
            if P["type"] == "cutter":
                dirv = nrm(sub(an["wrist"], an["elbow"]))
                P["at"] = add(an["wrist"], dirv, sp["hand"] * 0.45)
                P.setdefault("scale", 1.6)
                if "angle" not in pk if isinstance(pk, dict) else True:
                    P["angle"] = 0.0
            prop_svgs[side] = prop_svg(P["type"], P, sp)
            if P["type"] == "phone":
                prop_svgs["front_" + side] = True
            anchors["prop_" + side] = U(P["at"])
    # ---------------- layer order
    shade_head = dict(kind="head", round=0.5)
    if view == "front" and pose.get("back") and pack:
        pack = g(pack, "translate(0.08 0)")
    if view == "front":
        order = [("pack", pack, -3.0 if not pose.get("back") else 0.6, "pack", 0.22, True), ("leg_R", leg_svgs["R"], -1.2, "limb", 0.20, False),
                 ("leg_L", leg_svgs["L"], -1.0, "limb", 0.20, False), ("torso", torso, 0.0, "torso", 0.48, True),
                 ("head", head_svg, 1.0, "head", 0.5, True), ("face", face_svg, 1.35, "face", 0.5, True),
                 ("hair", hair_svg, 1.7, "hair", 0.16, True)]
        for side, z in (("R", 2.3), ("L", 2.45)):
            if side in prop_svgs:
                order.append(("prop_" + side, prop_svgs[side], z + (0.08 if prop_svgs.get("front_" + side) else -0.1), "prop", 0.07, True))
            order.append(("arm_" + side, arm_svgs[side], z, "limb", 0.12, True))
    else:
        near = "L" if s > 0 else "R"
        far = "R" if s > 0 else "L"
        order = [("pack", pack, -3.0, "pack", 0.22, True)]
        if far in prop_svgs:
            order.append(("prop_" + far, prop_svgs[far], -2.3, "prop", 0.07, True))
        order += [("arm_" + far, arm_svgs[far], -2.0, "limb", 0.12, True), ("leg_" + far, leg_svgs[far], -1.2, "limb", 0.20, False),
                  ("leg_" + near, leg_svgs[near], -0.6, "limb", 0.20, False), ("torso", torso, 0.0, "torso", 0.42, True),
                  ("head", head_svg, 1.0, "head", 0.5, True), ("face", face_svg, 1.35, "face", 0.5, True),
                  ("hair", hair_svg, 1.7, "hair", 0.16, True)]
        if near in prop_svgs:
            order.append(("prop_" + near, prop_svgs[near], 2.6 if prop_svgs.get("front_" + near) else 2.3, "prop", 0.07, True))
        order.append(("arm_" + near, arm_svgs[near], 2.5, "limb", 0.12, True))
    order.sort(key=lambda t: t[2])
    for name, svg, z, kind, rnd_, upper in order:
        if not svg:
            continue
        layers.append(dict(name=name, svg=upg(svg) if upper else svg, z=z, kind=kind, round=rnd_))
    anchors["head"] = U(hc)
    anchors["chin"] = U((hc[0], hc[1] + 0.5))
    anchors["hair_top"] = U((hc[0], hc[1] - 0.5 - sp["hair"]["top"]))
    anchors["crotch"] = U((0.0, K["crotch"]))
    return dict(layers=layers, anchors=anchors, spec=sp, view=view, s=s, pose=pose,
                bbox=(-1.6, -sp["legs"] - sp["torso"] - 1.4, 1.6, 0.15))


def _seated_leg(sp, view, s, hip, knee, foot, side):
    c = sp["col"]
    ink = sp["ink"]
    bw = sp["body_ink"]
    lw = sp["leg_w"]
    ank = (foot[0], foot[1] - min(sp["boot_h"] * 0.42, 0.24))
    o = poly_stroke([hip, knee], ink, lw + 2 * bw, cap="round")
    o += poly_stroke([knee, ank], ink, lw * 0.86 + 2 * bw)
    o += poly_stroke([knee, ank], c["trouser"], lw * 0.86)
    o += poly_stroke([hip, knee], c["trouser"], lw, cap="round")
    o += _foot(sp, view, s, ank, foot, 0, 0, side)
    return o, dict(hip=hip, knee=knee, ankle=ank, foot=foot)


def flat_svg(fig):
    return "".join(L["svg"] for L in fig["layers"])


def doc(fragment, canvas, ppd, bg=None):
    x0, y0, x1, y1 = canvas
    W, H = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
    b = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (f(x0), f(y0), f(x1 - x0), f(y1 - y0), bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" '
            'viewBox="%s %s %s %s">%s%s</svg>') % (W, H, f(x0), f(y0), f(x1 - x0), f(y1 - y0), b, fragment), W, H


def canvas_for(sp, margin=0.25):
    top = -(sp["legs"] + sp["torso"] + 1.0 + sp["hair"]["top"]) - 0.95
    return (-2.0, top, 2.0, 0.22)


SPECS["namnuea"] = _spec(
    name="namnuea", legs=1.62, torso=1.30, total_ref=4.2,
    hair=dict(style="ponytail", top=0.14, width=1.18, extent=0.6, n=6, fringe=0.30, seed=2, col="#1a1414", tie="#d4373b"),
    shoulder=0.86, chest=0.78, belt_w=0.74, hip_w=0.66, leg_w=0.30, boot_h=0.3, sole_len=(0.34, 0.42, 0.52), boot_w=0.30,
    hand=0.2, forearm=0.13, sleeve="long", sleeve_w=0.2, upper_arm=0.52, fore_arm=0.48, outfit="hoodie", shoe="sneaker",
    col=dict(shirt="#8e2a33", trouser="#5b5b60", trouser_dk="#444", boot="#c8343a", sole="#f4f4f0", belt="#333"),
    face=dict(eye="oval", eye_w=0.07, eye_h=0.15, eye_sp=0.38, brow_len=0.15, brow_th=0.03, brow_y=-0.19, mouth_y=0.22, mouth_w=0.2,
              stubble=False, blush=True),
    default_expr="smile")


# ------------------------------------------------------------------------------------------------ background people
EXTRA_ROLES = [
    # role, outfit, hair style, hair col, face extras, expr, pose (arms + prop), build
    dict(role="delivery rider", outfit="delivery", hair="crest", hair_col="#1d1d1d", face=dict(eye_w=0.075, eye_h=0.16), expr="worried",
         arms=dict(arm_r="carry", arm_l="down", prop_r=dict(type="helmet")), col=dict(jacket="#3fa34d", jacket_lo="#2c2c2c", trouser="#2b2b2e", boot="#3c8f45", sole="#f4f4f0"),
         box=True, shoe="sneaker_high", build=(0.94, 0.80, 0.33)),
    dict(role="office woman, phone", outfit="blazer", hair="bob", hair_col="#2a1d18", face=dict(eye_w=0.07, eye_h=0.15, blush=True), expr="worried",
         arms=dict(arm_r="phone_ear", arm_l="cross", prop_r=dict(type="phone")), col=dict(shirt="#f3f1ea", jacket="#7b2f45", trouser="#2e2f38", boot="#1f1f22"),
         skirt=True, shoe="shoe", build=(0.80, 0.70, 0.30), skin="#fbefe3"),
    dict(role="older man, grey", outfit="polo", hair="grey_swept", hair_col="#9b9ea3", face=dict(eye_w=0.06, eye_h=0.12, wrinkles=True, moustache=True, glasses="round"),
         expr="stern", arms=dict(arm_r="hips", arm_l="hips"), col=dict(shirt="#4f7fb8", trouser="#8c7a5e", boot="#5a3e2a"), shoe="shoe",
         build=(1.02, 0.96, 0.36), skin="#f6e6d2"),
    dict(role="teen, hoodie", outfit="hoodie", hair="messy", hair_col="#1a1414", face=dict(eye_w=0.085, eye_h=0.19), expr="surprised",
         arms=dict(arm_r="point", arm_l="down"), col=dict(shirt="#5b6470", trouser="#3d5f8f", boot="#e9e9e4", sole="#f4f4f0"),
         shoe="sneaker_high", build=(0.88, 0.74, 0.31)),
    dict(role="auntie, umbrella", outfit="tee", hair="bun", hair_col="#2b2420", face=dict(eye_w=0.065, eye_h=0.13, blush=True), expr="sad",
         arms=dict(arm_r=dict(hand=(0.30, 0.35)), arm_l="down", prop_r=dict(type="umbrella", col="#d0463a")), col=dict(shirt="#e7b23c", trouser="#4d4a6e", boot="#7d5b3f"),
         print="#c0392b", shoe="shoe", build=(1.04, 1.00, 0.38), skin="#f7e7d5"),
    dict(role="taxi driver, cap", outfit="shirt", hair="cap", hair_col="#1b1b1b", face=dict(eye_w=0.07, eye_h=0.14, beard=True),
         expr="angry", arms=dict(arm_r="wave", arm_l="down"), col=dict(shirt="#8fb7d8", trouser="#363636", boot="#2a2a2a"), cap_col="#e0a21b",
         shoe="shoe", build=(1.00, 0.92, 0.36)),
    dict(role="student, ponytail", outfit="shirt", hair="ponytail", hair_col="#151111", face=dict(eye_w=0.075, eye_h=0.17, blush=True),
         expr="scared", arms=dict(arm_r="guard", arm_l="guard"), col=dict(shirt="#ffffff", trouser="#1f2e5a", boot="#141414"), skirt=True,
         shoe="shoe", build=(0.82, 0.70, 0.29), tie=True, tie_col="#1f2e5a"),
    dict(role="young man, tee", outfit="tee", hair="spiky", hair_col="#232020", face=dict(eye_w=0.08, eye_h=0.18), expr="talk",
         arms=dict(arm_r="pocket", arm_l="phone_look", prop_l=dict(type="phone")), col=dict(shirt="#2f7f7a", trouser="#41536b", boot="#b33a2e", sole="#f4f4f0"),
         shorts=True, shoe="sneaker", build=(0.92, 0.78, 0.32)),
    dict(role="bald man, bag", outfit="office", hair="bald", hair_col="#555", face=dict(eye_w=0.06, eye_h=0.14, glasses="rect"),
         expr="neutral", arms=dict(arm_r="down", arm_l="down", prop_l=dict(type="bag", col="#5c3b22")), col=dict(shirt="#f2f2ee", trouser="#22262f", boot="#1a1a1a",
         tie="#2c5e9e"), tie=True, shoe="shoe", build=(1.06, 1.04, 0.38), skin="#f1dcc5"),
    dict(role="woman, long hair", outfit="tee", hair="long", hair_col="#3a261b", face=dict(eye_w=0.07, eye_h=0.16), expr="smile",
         arms=dict(arm_r="cross", arm_l="cross"), col=dict(shirt="#c86aa0", trouser="#d7c4a4", boot="#f0f0ec"), shoe="sneaker", build=(0.84, 0.72, 0.31),
         skin="#fcefe2"),
]


def extras(n=10, seed=0):
    """n distinct background people (stranded drivers, a delivery rider with a green box) in the sheet's style.
    Every one differs in face (eye size / extras / expression), hair (style + colour), clothes colours and pose."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        R = EXTRA_ROLES[i % len(EXTRA_ROLES)]
        sh, ch, lw = R["build"]
        legs = rnd.uniform(1.62, 1.82)
        torso = rnd.uniform(1.28, 1.42)
        col = dict(shirt="#888", trouser="#444", trouser_dk="#333", boot="#2a2a2a", sole="#1c1c1c", belt="#2b2b2b", buckle="#c9c9c4",
                   tie=R.get("tie_col", "#9b2a2a"), stain="#6f5a44", jacket="#555", jacket_lo="#2c2c2c", glove="#333")
        col.update(R["col"])
        col["trouser_dk"] = shade(col["trouser"], 0.3)
        if "tie" in R["col"]:
            col["tie"] = R["col"]["tie"]
        style = {"messy": "swept", "grey_swept": "swept"}.get(R["hair"], R["hair"])
        hair = dict(style=style, top=rnd.uniform(0.12, 0.2), width=rnd.uniform(1.12, 1.26), extent=rnd.uniform(0.62, 0.8), n=6 + i % 3,
                    fringe=rnd.uniform(0.2, 0.32), seed=100 + i, col=R["hair_col"], messy=R["hair"] == "messy", cap_col=R.get("cap_col", "#2f5fa8"))
        face = dict(eye="oval", eye_w=0.08, eye_h=0.18, eye_sp=rnd.uniform(0.30, 0.40), brow_len=rnd.uniform(0.15, 0.22),
                    brow_th=rnd.uniform(0.028, 0.045), brow_y=-rnd.uniform(0.15, 0.20), mouth_y=rnd.uniform(0.20, 0.26), mouth_w=rnd.uniform(0.17, 0.24),
                    stubble=False)
        face.update(R["face"])
        sp = _spec(name="extra%02d" % i, role=R["role"], legs=legs, torso=torso, hair=hair, hair_col=R["hair_col"],
                   shoulder=sh, chest=ch * 0.95, belt_w=ch * 0.98, hip_w=ch, leg_w=lw, boot_h=0.30 if R.get("shoe") in ("shoe", "sneaker") else 0.45,
                   sole_len=(0.36, 0.44, 0.54), boot_w=0.32, hand=0.21, forearm=0.13, sleeve="short" if R["outfit"] in ("tee", "polo") else "long",
                   sleeve_w=0.21, upper_arm=0.55, fore_arm=0.50, outfit=R["outfit"], col=col, glove=False, shoe=R.get("shoe", "shoe"),
                   tie=R.get("tie", False), print=R.get("print"), box=R.get("box", False), shorts=R.get("shorts", False), skirt=R.get("skirt", False),
                   skin=R.get("skin", "#fdf6ed"), face=face, default_expr=R["expr"], extra_pose=dict(R["arms"]))
        if sp["skirt"]:
            sp["legwear"] = sp["skin"]
        out.append(sp)
    _check_unique(out)
    return out


def _check_unique(specs):
    keys = {"face": lambda s: (round(s["face"]["eye_w"], 3), round(s["face"]["eye_h"], 3), s["default_expr"],
                               tuple(sorted(k for k in s["face"] if k in ("glasses", "moustache", "beard", "wrinkles", "blush")))),
            "hair": lambda s: (s["hair"]["style"], s["hair"].get("col"), s["hair"].get("messy")),
            "clothes": lambda s: (s["outfit"], s["col"].get("shirt"), s["col"].get("jacket"), s["col"]["trouser"]),
            "pose": lambda s: tuple(sorted((k, str(v)) for k, v in s["extra_pose"].items()))}
    for name, fn in keys.items():
        vals = [fn(s) for s in specs]
        if len(set(vals)) != len(vals):
            raise ValueError("extras not unique in %s: %s" % (name, vals))
    return True
