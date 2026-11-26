"""draw9.py -- EP.1 cast: additions to v8/cast/draw8 (imported, never edited).

    import draw9 as D9            # patches the draw8 module in this process (old specs draw exactly as before)
    fig = D9.build("praew_wet", dict(view="q", s=1, expr="focused"))
    D9.SPECS  (= draw8.SPECS, with the new names)      D9.infected_crowd(14)      D9.watch_svg(sec)

New spec keys (all optional, so the hook's specs are untouched):
    outfit9      "suit" | "coat" | "rider" | "guard"      overlay drawn on top of the draw8 base outfit
    sleeve_col   sleeve colour (jacket / coat) when it differs from the shirt
    hair.style   "praew" | "slick" | "helmet" | "curly" | "flat" | "mop"  (+ draw8's)
    face.glasses "tos"            watch = dict(side="L", style="kong" | "silver", blood=bool)
    neck_wound   dict(side="L", blood=0..1, gauze=None | 0..1 (soak), dried=bool)
    tear         dict(side="L" | "R", level=1 torn | 2 blood-soaked cuff | 3 dripping)
    blood_hands  0..1 (gloves)    blood_forearm = "R"      crowbar_pack = True      knee_dirt = True
    wounds       list of dict(kind=...) for the crowd (see WOUND_KINDS)
    canvas_pad   (side, top[, bottom]) extra canvas in D (raised tools; a foot planted below the root in a leap)
Sides are ANATOMICAL ("L" = the character's left).  label_of() maps them to draw8's limb labels, which are
mirrored in the q / side drawings.
New pose keys: visor ("up" | "down"), z (dict layer -> z), arm dicts may carry fig=(x, y) (a figure-frame target)
or grab=dict(arm="n" | "f" | "R" | "L", t=0..1, dx, dy) (hold the other arm's forearm), coat_sway, shiver.
"""
import os, sys, math, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
if os.path.join(PROJ, "v8", "cast") not in sys.path:
    sys.path.append(os.path.join(PROJ, "v8", "cast"))
import draw8 as D
from draw8 import (f, path, ell, line, poly_stroke, g, pts_d, smooth_d, add, sub, nrm, lerp, ik2, shade, tint, mix_hex,
                   rot_pt, INK, _cyl_x, BODY_YAW, VIEW_YAW)

SPECS = D.SPECS
NO_FACE_BEADS = True          # the film's decision (v10 stage._face_clean): no pale rain beads on faces
BLOOD, BLOOD_DK, BLOOD_DRY = "#b3161b", "#7c1015", "#5a1a16"
INF_SKIN = "#c4cdb2"
CTX = {}                      # per-build context for the wrappers that do not get the pose (pack_layer)


def rect(x, y, w, h, fill, stroke=None, sw=0.0, rx=0.0, extra=""):
    s = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"' % (f(x), f(y), f(w), f(h), fill)
    if rx:
        s += ' rx="%s"' % f(rx)
    if stroke:
        s += ' stroke="%s" stroke-width="%s" stroke-linejoin="round"' % (stroke, f(sw))
    return s + extra + "/>"


def label_of(anat, view, s=1, back=False):
    """anatomical side ("L" / "R") -> draw8 limb label in this drawing.  Front: the same.  Back: swapped (draw8's
    back drawing is the front one unmirrored).  q / side: swapped (draw8 calls the camera-side limb "L" when the
    figure faces screen-right, but a figure facing screen-right shows its RIGHT side)."""
    other = "R" if anat == "L" else "L"
    if view in ("front",) and not back:
        return anat
    return other


def is_near(anat, view, s):
    """q / side: is the anatomical side toward the camera?  facing screen-left (s = -1) shows the left side."""
    return (anat == "L") == (s < 0)


# ====================================================================================================== expressions
D.EXPR.setdefault("serious", dict(eyes="oval", brows=(20, -0.005), mouth=("flat", 0.8)))
D.EXPR.update({
    # Praew
    "focused": dict(eyes="oval", brows=(11, -0.005), mouth=("flat", 0.7)),
    "doubtful": dict(eyes="glance", gaze=(-1.0, 0.25), brows=dict(lead=(-14, 0.055), trail=(13, -0.01)), mouth=("flat_down", 0.8)),
    "calm": dict(eyes="oval", brows=(0, 0.02), mouth=("smile", 0.8)),
    # Tos
    "arrogant": dict(eyes="oval", brows=dict(lead=(22, -0.01), trail=(5, 0.035)), mouth=("frown", 0.85)),   # checker: bold dot eyes as on the sheet (the half lids read as two T marks behind the glasses)
    "panicked": dict(eyes="ring_small", brows=(-24, 0.07), mouth=("wobble_open", 0.6), sweat=True),
    "evasive": dict(eyes="glance", gaze=(-1.3, 0.55), brows=(-10, 0.03), mouth=("wobble", 0.5), sweat=True),
    # James
    "cheerful": dict(eyes="arc", brows=None, mouth=("open", 0.75)),          # checker: no bars over the laughing arcs (they doubled the eyes)
    "terrified": dict(eyes="ring", brows=(-26, 0.08), mouth=("scream", 1.0), sweat=True),
    "urgent": dict(eyes="oval", brows=(-12, 0.06), mouth=("open", 0.55)),
    # the junior, wounded
    "pain": dict(eyes="pain", brows=(-20, 0.02), mouth=("grit", 1.0), sweat=True),
    "fading": dict(eyes="lid", brows=(-14, 0.0), mouth=("slack", 0.5), bags=True),
    "out": dict(eyes="closed", brows=(-6, -0.01), mouth=("slack", 0.25)),
    # the junior / crowd, infected
    "snap_open": dict(eyes="z_snap", brows=(-4, 0.06), mouth=("slack", 0.5)),
    "searching": dict(eyes="z_open", gaze=(1.6, 0.0), brows=(10, 0.0), mouth=("slack", 0.9)),
    "lunging": dict(eyes="z_wide", brows=(28, -0.01), mouth=("snarl", 0.8)),
    "moan": dict(eyes="z_lid", brows=(-8, 0.0), mouth=("slack", 1.0)),
    # guard, Kong
    "wary": dict(eyes="oval", brows=(16, 0.0), mouth=("frown", 0.8)),
    "grief": dict(eyes="down", brows=(-18, 0.03), mouth=("flat_down", 0.8)),
    "resolve": dict(eyes="oval", brows=(24, -0.01), mouth=("frown", 0.6)),
})

_eye0, _mouth0 = D._eye, D._mouth


def _eye9(kind, x, y, fs, sp, s, gaze, blink, small=1.0, side=1, ink=INK):
    F = sp["face"]
    if blink == 2:
        return _eye0("closed", x, y, fs, sp, s, gaze, blink, small, ink=ink)
    if kind == "pain":                                    # > < squeezed shut, pointing at the nose
        a, d = 0.075, -side
        return path("M%s %s L%s %s L%s %s" % (f(x - d * a), f(y - 0.055), f(x + d * a * 0.35), f(y), f(x - d * a), f(y + 0.05)),
                    stroke=ink, sw=0.038)
    if kind == "glance":                                  # bold ovals pushed to one side of their socket
        ew, eh = F["eye_w"] * small, F["eye_h"] * small * (0.45 if blink == 1 else 0.88)
        return ell(x + gaze[0] * 0.035, y + gaze[1] * 0.03, ew * max(fs, 0.35) / 2, eh / 2, ink)
    if kind == "z_snap":                                  # the eyes snap open: wider than z_wide, pin pupils, veins
        rx = F["eye_w"] / 2 * max(fs, 0.4) * 1.32
        ry = F["eye_h"] / 2 * 1.45
        o = ell(x, y, rx, ry, "#f7f5ec", ink, 0.026)
        for k, a in enumerate((205, 250, 325, 20)):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            o += line((x + ca * rx * 0.92, y + sa * ry * 0.92), (x + ca * rx * 0.5, y + sa * ry * 0.55), "#c9534f", 0.009)
        o += ell(x + gaze[0] * 0.02, y + gaze[1] * 0.015, 0.014, 0.014, "#d81c1c")
        o += path("M%s %s Q%s %s %s %s" % (f(x - rx), f(y + ry + 0.03), f(x), f(y + ry + 0.065), f(x + rx), f(y + ry + 0.03)),
                  stroke=sp.get("skin_dk", "#888"), sw=0.024)
        return o
    return _eye0(kind, x, y, fs, sp, s, gaze, blink, small, ink=ink)


def _mouth9(kind, amt, x, y, fs, sp, level=None, shape="a", ink=INK, s=1):
    W = sp["face"]["mouth_w"] * max(fs, 0.45)
    if level is not None and level > 0.06:
        return _mouth0(kind, amt, x, y, fs, sp, level=level, shape=shape, ink=ink)
    if kind == "grit":                                    # clenched teeth
        w, h = W * 1.05, 0.085
        o = rect(x - w / 2, y - h * 0.4, w, h, "#fbfbf6", ink, 0.028, rx=0.03)
        o += line((x - w / 2 + 0.01, y - h * 0.4 + h / 2), (x + w / 2 - 0.01, y - h * 0.4 + h / 2), ink, 0.012)
        for k in (-1, 0, 1):
            o += line((x + k * w * 0.25, y - h * 0.4 + 0.008), (x + k * w * 0.25, y + h * 0.6 - 0.008), ink, 0.011)
        return o
    if kind == "smirk":
        w = W * 0.42
        return path("M%s %s Q%s %s %s %s" % (f(x - s * w), f(y + 0.015), f(x + s * w * 0.3), f(y + 0.04), f(x + s * w), f(y - 0.035)),
                    stroke=ink, sw=0.030)
    if kind == "scream":
        return D._open_mouth(x, y - 0.05, W * 1.0, 0.25 * amt, ink, teeth=True, lower_teeth=False, round_=True)
    return _mouth0(kind, amt, x, y, fs, sp, level=level, shape=shape, ink=ink)


def _drop(x0, y0, r, col, ink=None, sw=0.0):
    return path("M%s %s Q%s %s %s %s A%s %s 0 1 1 %s %s Q%s %s %s %s Z" % (
        f(x0), f(y0 - r * 2.4), f(x0 + r * 0.45), f(y0 - r * 1.1), f(x0 + r), f(y0), f(r), f(r), f(x0 - r), f(y0),
        f(x0 - r * 0.45), f(y0 - r * 1.1), f(x0), f(y0 - r * 2.4)), col, ink, sw)


def _blob(cx, cy, rx, ry, seed, col, ink=None, sw=0.0, n=9, jag=0.28, rot=0.0):
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1.0 + rnd.uniform(-jag, jag)
        pts.append(rot_pt((rx * k * math.cos(a), ry * k * math.sin(a)), rot))
    return path(smooth_d([(cx + p[0], cy + p[1]) for p in pts], True, 0.6), col, ink, sw)


def _face9(sp, pose, view, s, yaw, cx, cy):
    """draw8._face with: asymmetric brows, expression gaze, the new eye / mouth kinds, Tos's glasses, face wounds."""
    F = sp["face"]
    ink = sp["ink"]
    expr = pose.get("expr") or sp.get("default_expr", "neutral")
    E = D.EXPR.get(expr, D.EXPR["neutral"])
    blink = pose.get("blink", 0)
    gaze = pose.get("gaze")
    if gaze is None:
        gz = E.get("gaze", (0.0, 0.0))
        gaze = (gz[0] * s, gz[1])                          # expression gazes are written for a figure facing right
    o = ""
    eye_lon = math.degrees(math.asin(min(F["eye_sp"] / 2 / 0.5, 0.95)))
    eye_lat = -F.get("eye_y", 0.0) / 0.47 * 57.3
    eyes = []
    for side in (-1, 1):
        x, y, fs = D.sph(cx, cy, yaw, side * eye_lon, eye_lat, 0.5)
        if fs < 0.12:
            continue
        eyes.append((side, x, y, fs))
    ekind = E["eyes"]
    if F["eye"] == "zombie" and not ekind.startswith("z_"):
        ekind = "z_open"
    shut = None
    for w in sp.get("wounds", ()):
        if w["kind"] == "eye_shut":
            shut = w.get("eye", 1) * (1 if s > 0 else -1)
    for side, x, y, fs in eyes:
        small = 0.9 if (fs < 0.75) else 1.0
        if shut == side:                                   # a swollen eye that no longer opens
            o += ell(x, y + 0.01, F["eye_w"] * 0.6 * max(fs, 0.4), 0.05, sp.get("skin_dk", "#888"))
            o += path("M%s %s Q%s %s %s %s" % (f(x - 0.06 * fs), f(y + 0.01), f(x), f(y + 0.04), f(x + 0.06 * fs), f(y + 0.01)), stroke=ink, sw=0.026)
            continue
        o += _eye9(ekind, x, y, fs, sp, s, gaze, blink, small, side=side, ink=ink)
    gl = F.get("glasses")
    if gl == "tos":
        # sheet: black rectangular rims, lenses 0.31 x 0.18 D, overall 0.77 D, the rim crosses just under the brows
        for side, x, y, fs in eyes:
            lw = 0.305 * max(fs, 0.30)
            lx = x + side * 0.012
            o += rect(lx - lw / 2, y - 0.105, lw, 0.185, "#ffffff", ink, 0.030, rx=0.022, extra=' fill-opacity="0.18"')
            o += line((lx - lw * 0.30, y - 0.065), (lx - lw * 0.12, y - 0.065), "#ffffff", 0.014)
            tx = lx + side * lw / 2                         # temple arm to the ear
            ex = cx + side * 0.47
            if (ex - tx) * side > 0.02:
                o += line((tx, y - 0.05), (ex, y - 0.035), ink, 0.026)
        if len(eyes) == 2:
            a_, b_ = eyes[0], eyes[1]
            o += line((a_[1] + a_[0] * 0.012 + 0.152 * max(a_[3], 0.3), a_[2] - 0.04), (b_[1] + b_[0] * 0.012 - 0.152 * max(b_[3], 0.3), b_[2] - 0.04), ink, 0.028)
    elif gl:
        for side, x, y, fs in eyes:
            gw = 0.17 * max(fs, 0.3)
            if gl == "round":
                o += ell(x, y, gw * 0.62, 0.095, "none", ink, 0.022)
            else:
                o += '<rect x="%s" y="%s" width="%s" height="%s" rx="0.02" fill="none" stroke="%s" stroke-width="0.024"/>' % (
                    f(x - gw * 0.62), f(y - 0.085), f(gw * 1.24), f(0.17), ink)
        if len(eyes) == 2:
            o += line((eyes[0][1] + 0.105 * eyes[0][3], eyes[0][2] - 0.03), (eyes[1][1] - 0.105 * eyes[1][3], eyes[1][2] - 0.03), ink, 0.02)
    # brows: straight bars; (angle, raise) for both, or dict(lead=, trail=): lead = the brow on the facing side
    B_ = E["brows"]
    o_face = o
    o = ""
    if not F.get("no_brows") and B_ is not None:
        for side, x, y, fs in eyes:
            if isinstance(B_, dict):
                ang, raise_ = B_["lead"] if side == (1 if s > 0 else -1) else B_["trail"]
            else:
                ang, raise_ = B_
            bl = F["brow_len"] * max(fs, 0.35)
            by = cy + F["brow_y"] - raise_
            inner = -side
            a = math.radians(ang)
            dx, dy = bl / 2, bl / 2 * math.tan(a)
            o += line((x + inner * dx, by + dy), (x - inner * dx, by - dy), sp["brow"], F["brow_th"], cap="round")
    if F.get("brow_over_hair"):
        halo = o.replace('stroke="%s"' % sp["brow"], 'stroke="%s"' % sp["skin"])
        halo = re.sub(r'stroke-width="([0-9.]+)"', lambda m: 'stroke-width="%s"' % f(float(m.group(1)) + 0.022), halo)
        pose["_brows_svg"] = halo + o
        o = o_face
    else:
        o = o_face + o
    mx, my, mfs = D.sph(cx, cy, yaw, 0.0, -math.degrees(math.asin(F["mouth_y"] / 0.5)), 0.5)
    lvl = pose.get("mouth")
    shape = "a"
    if isinstance(lvl, (tuple, list)):
        shape, lvl = lvl[0], lvl[1]
    mk, amt = E["mouth"]
    o += _mouth9(mk, amt, mx, my, mfs, sp, level=lvl, shape=shape, ink=ink, s=s)
    if F.get("moustache"):
        mw = 0.17 * max(mfs, 0.5)
        o += path("M%s %s Q%s %s %s %s Q%s %s %s %s Z" % (f(mx - mw), f(my - 0.03), f(mx), f(my - 0.11), f(mx + mw), f(my - 0.03),
                                                         f(mx), f(my - 0.06), f(mx - mw), f(my - 0.03)), sp["hair_col"] if "hair_col" in sp else ink)
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
    if F.get("blush") and F["eye"] != "zombie":
        for side, x, y, fs in eyes:
            o += ell(x + side * 0.03, y + 0.15, 0.06 * fs, 0.03, "#f2a7a4")
    if E.get("bags"):
        for side, x, y, fs in eyes:
            o += path("M%s %s Q%s %s %s %s" % (f(x - 0.05 * fs), f(y + 0.095), f(x), f(y + 0.125), f(x + 0.05 * fs), f(y + 0.095)),
                      stroke=ink, sw=0.014)
    if E.get("sweat") or pose.get("sweat"):
        sx, sy = cx + s * 0.36, cy - 0.20
        o += path("M%s %s Q%s %s %s %s A0.045 0.045 0 1 1 %s %s Q%s %s %s %s Z" % (
            f(sx), f(sy - 0.11), f(sx + 0.02), f(sy - 0.05), f(sx + 0.045), f(sy), f(sx - 0.045), f(sy), f(sx - 0.02), f(sy - 0.05),
            f(sx), f(sy - 0.11)), "#9fd3f2", ink, 0.018)
    if (pose.get("rain_drips") or sp.get("wet")) and not NO_FACE_BEADS:
        rnd = random.Random(3)
        for i in range(3):
            x0 = cx + rnd.uniform(-0.3, 0.3)
            y0 = cy + rnd.uniform(-0.15, 0.2)
            if any(abs(x0 - e[1]) < 0.11 and abs(y0 - e[2]) < 0.16 for e in eyes):
                continue
            o += _drop(x0, y0, 0.018, "#cfe6f5")
    # ---- face wounds (crowd)
    for w in sp.get("wounds", ()):
        k = w["kind"]
        sd = w.get("eye", 1) * (1 if s > 0 else -1)
        if k == "mouth_blood":
            o += path(smooth_d([(mx - 0.09 * mfs, my + 0.03), (mx + 0.10 * mfs, my + 0.035), (mx + 0.07 * mfs, my + 0.15), (mx + 0.02, my + 0.11),
                                (mx - 0.03 * mfs, my + 0.19), (mx - 0.07 * mfs, my + 0.10)], True, 0.5), BLOOD_DK)
        elif k == "cheek_bite":
            e = [e_ for e_ in eyes if e_[0] == sd]
            if e:
                x, y, fs = e[0][1], e[0][2], e[0][3]
                o += _blob(x + sd * 0.04, y + 0.20, 0.075 * fs, 0.055, w.get("seed", 3), BLOOD_DK, ink, 0.014)
                o += _blob(x + sd * 0.04, y + 0.20, 0.035 * fs, 0.025, w.get("seed", 3) + 1, "#3a0a0d")
                o += line((x + sd * 0.05, y + 0.25), (x + sd * 0.06, y + 0.36), BLOOD_DK, 0.022)
        elif k == "brow_cut":
            e = [e_ for e_ in eyes if e_[0] == sd]
            if e:
                x, y = e[0][1], e[0][2]
                o += line((x - 0.05, y - 0.30), (x + 0.04, y - 0.24), BLOOD_DK, 0.024)
                o += line((x + 0.03, y - 0.25), (x + 0.045, y - 0.10), BLOOD, 0.018)
        elif k == "veins":
            for i, a in enumerate((200, 230, 310, 340)):
                p0 = (cx + 0.44 * math.cos(math.radians(a)), cy - 0.44 * math.sin(math.radians(a)) * -1)
                p1 = (cx + 0.33 * math.cos(math.radians(a + 6)), cy + 0.33 * math.sin(math.radians(a + 6)))
                o += line(p0, p1, sp.get("skin_dk", "#888"), 0.012)
    return o


# ====================================================================================================== hair
_hair0, _hair_back0 = D._hair, D._hair_back
STYLES9 = ("praew", "slick", "helmet", "curly", "flat", "mop")


def _hair9(sp, pose, view, s, yaw, cx, cy):
    H = sp["hair"]
    st = H["style"]
    if st not in STYLES9:
        return _hair0(sp, pose, view, s, yaw, cx, cy)
    col = H.get("col", sp["hair_col"])
    ink = sp["ink"]
    fs_ = 1 if s > 0 else -1
    sh = math.sin(math.radians(yaw)) * 0.5                 # signed: how far the face centre has moved toward the facing side
    top = 0.5 + H["top"]
    hw = H["width"] / 2

    def P(pts, face_k=0.0):                                # (x toward the face side, y up) -> screen
        return [(cx + fs_ * x + sh * face_k - sh * 0.10, cy - y) for x, y in pts]

    o = ""
    if st == "praew":
        # sheet: a thin dark cap, the hairline a pointed arch from a parting right of centre, two locks in front of the
        # ears down past the chin, a lumpy bun low behind the head (screen-left when she faces right)
        loose = H.get("loose", 0.0)
        bx, by = cx - fs_ * (0.60 if view != "side" else 0.66) - sh * 0.25, cy + 0.02
        o += _blob(bx, by, 0.185, 0.205, 5, col, ink, 0.034, n=10, jag=0.10)
        o += path("M%s %s Q%s %s %s %s" % (f(bx - fs_ * 0.06), f(by - 0.10), f(bx + fs_ * 0.04), f(by - 0.02), f(bx - fs_ * 0.02), f(by + 0.10)),
                  stroke=tint(col, 0.25), sw=0.016)
        if loose > 0:
            o += path(smooth_d([(bx - fs_ * 0.10, by + 0.12), (bx - fs_ * 0.22, by + 0.30 + 0.2 * loose), (bx - fs_ * 0.10, by + 0.42 + 0.3 * loose)], False, 0.6),
                      "none", ink, 0.05)
        outer = [(0.455, -0.54), (0.515, -0.12), (0.545, 0.16)]
        n = 12
        for i in range(n + 1):
            a = math.radians(14 + (166 - 14) * i / n)
            outer.append((hw * math.cos(a) * 0.985, top * math.sin(a)))
        outer += [(-0.55, 0.10), (-0.515, -0.28), (-0.465, -0.50)]
        inner = [(-0.40, -0.20), (-0.36, 0.10), (-0.20, 0.30), (0.10, 0.445), (0.24, 0.30), (0.36, 0.12), (0.43, -0.12)]
        if view == "side":
            inner = [(-0.10, -0.20), (-0.04, 0.12), (0.08, 0.32), (0.30, 0.445), (0.38, 0.30), (0.44, 0.12), (0.46, -0.12)]
        fr = [(cx + fs_ * x + sh * 0.45 * (1 - abs(x)) - sh * 0.10, cy - y) for x, y in inner]
        poly = P(outer) + fr
        o += path(smooth_d(poly, True, 0.32), col, ink, 0.034)
        # sheen strokes following the sweep from the parting
        px_ = cx + fs_ * 0.10 + sh * 0.35
        o += path("M%s %s Q%s %s %s %s" % (f(px_ - fs_ * 0.10), f(cy - 0.50), f(px_ - fs_ * 0.40), f(cy - 0.40), f(cx - fs_ * 0.46 - sh * 0.1), f(cy - 0.12)),
                  stroke=tint(col, 0.22), sw=0.016)
        if H.get("wet") or loose > 0:
            lx = cx + fs_ * 0.26 + sh * 0.3                # a wet strand fallen across the forehead
            o += path(smooth_d([(lx, cy - 0.40), (lx + fs_ * 0.07, cy - 0.20), (lx + fs_ * 0.02, cy - 0.02 + 0.10 * loose)], False, 0.6), "none", ink, 0.042)
            for k in range(2):
                x0 = cx - 0.22 + k * 0.30
                o += path("M%s %s A0.02 0.02 0 1 0 %s %s" % (f(x0 - 0.02), f(cy - top + 0.12), f(x0 + 0.02), f(cy - top + 0.12)), "#cfe6f5")
        return o
    if st == "slick":
        # Tos (sheet): combed back off a high forehead, volume on the back side; the driver's fringe hangs to the brows
        pts = [(0.47, 0.13), (0.53, 0.34), (0.45, 0.57), (0.22, top - 0.005), (-0.08, top + 0.015), (-0.38, top - 0.05), (-0.59, 0.40),
               (-hw * 1.03, 0.16), (-0.57, -0.07), (-0.47, -0.10)]
        inner = [(-0.43, 0.10), (-0.37, 0.30), (-0.17, 0.405), (0.09, 0.43), (0.31, 0.365), (0.44, 0.22)]
        if view == "side":
            inner = [(-0.16, 0.06), (-0.08, 0.30), (0.10, 0.40), (0.28, 0.42), (0.42, 0.34), (0.48, 0.20)]
        fr = [(cx + fs_ * x + sh * 0.40 * (1 - abs(x)) - sh * 0.10, cy - y) for x, y in inner]
        o += path(smooth_d(P(pts) + fr, True, 0.34), col, ink, 0.034)
        for k, (x0, x1, yy) in enumerate(((0.26, -0.30, 0.53), (0.20, -0.36, 0.46))):
            o += path("M%s %s Q%s %s %s %s" % (f(cx + fs_ * x0 + sh * 0.2), f(cy - yy + 0.06), f(cx + fs_ * (x0 + x1) / 2), f(cy - yy - 0.045),
                                             f(cx + fs_ * x1 - sh * 0.1), f(cy - yy + 0.10)), stroke=tint(col, 0.20), sw=0.014)
        if H.get("wet"):
            lx = cx + fs_ * 0.30 + sh * 0.3
            o += path(smooth_d([(lx, cy - 0.38), (lx + fs_ * 0.06, cy - 0.24), (lx + fs_ * 0.03, cy - 0.12)], False, 0.6), "none", col, 0.045)
        return o
    if st == "helmet":
        # open-face rider's helmet: white shell, dark visor (up on the brow of the shell / down over the eyes), green rim, strap
        hc = H.get("shell", "#f4f4f0")
        rim = H.get("rim", "#3fa34d")
        vis = pose.get("visor", H.get("visor", "up"))
        ox = cx - sh * 0.12
        oy = cy - 0.07
        R = 0.615
        outer_pts = []
        for i in range(25):
            a = math.radians(-38 + 256 * i / 24)
            outer_pts.append((ox + R * math.cos(a), oy - R * 1.02 * math.sin(a)))
        outer = smooth_d(outer_pts, True, 0.5)
        fx = cx + sh * 0.95
        op = [(fx - 0.41, cy + 0.70), (fx - 0.43, cy + 0.0), (fx - 0.36, cy - 0.21), (fx, cy - 0.255), (fx + 0.36, cy - 0.21), (fx + 0.43, cy + 0.0), (fx + 0.41, cy + 0.70)]
        opening = smooth_d(op, True, 0.45)
        uid = "h%d" % (abs(hash((sp.get("name"), view, s, round(yaw, 2)))) % 99999)
        o += '<defs><mask id="%sm" maskUnits="userSpaceOnUse" x="-9" y="-9" width="18" height="18"><rect x="-9" y="-9" width="18" height="18" fill="#fff"/><path d="%s" fill="#000"/></mask>' % (uid, opening)
        o += '<clipPath id="%sc"><path d="%s"/></clipPath></defs>' % (uid, outer)
        tuft = ""
        if H.get("tuft", True):
            for k, (tx, dd) in enumerate(((-0.20, 0.10), (-0.05, 0.15), (0.11, 0.11))):
                tuft += path(pts_d([(fx + tx - 0.07, cy - 0.26), (fx + tx + 0.07, cy - 0.26), (fx + tx + 0.015, cy - 0.26 + dd)]), sp["hair_col"], ink, 0.02)
        o += tuft
        o += '<g mask="url(#%sm)">%s</g>' % (uid, path(outer, hc, ink, 0.036))
        inner = path(opening, "none", ink, 0.034)
        ry_ = oy + R * 0.60                                # rim band along the bottom of the shell
        inner += path("M%s %s Q%s %s %s %s" % (f(ox - R * 0.80), f(ry_), f(ox), f(ry_ + 0.07), f(ox + R * 0.80), f(ry_)), "none", rim, 0.05)
        o += '<g clip-path="url(#%sc)"><g mask="url(#%sm)">%s</g>%s</g>' % (uid, uid, path("M%s %s Q%s %s %s %s" % (
            f(ox - R * 0.80), f(ry_), f(ox), f(ry_ + 0.07), f(ox + R * 0.80), f(ry_)), "none", rim, 0.05), path(opening, "none", ink, 0.034))
        vcol = "#232a36"
        if vis == "down":
            vp = [(fx - 0.45, cy - 0.20), (fx, cy - 0.27), (fx + 0.45, cy - 0.20), (fx + 0.44, cy + 0.10), (fx, cy + 0.15), (fx - 0.44, cy + 0.10)]
            o += '<g clip-path="url(#%sc)">%s%s</g>' % (uid, path(smooth_d(vp, True, 0.4), vcol, ink, 0.03, ' fill-opacity="0.58"'),
                                                       line((fx - 0.30, cy - 0.13), (fx - 0.08, cy - 0.17), "#aab7c8", 0.022))
        else:
            vp = [(fx - 0.44, cy - 0.27), (fx - 0.30, cy - 0.47), (fx, cy - 0.53), (fx + 0.30, cy - 0.47), (fx + 0.44, cy - 0.27), (fx, cy - 0.335)]
            o += '<g clip-path="url(#%sc)">%s%s</g>' % (uid, path(smooth_d(vp, True, 0.45), vcol, ink, 0.03),
                                                       line((fx - 0.24, cy - 0.40), (fx - 0.04, cy - 0.45), "#aab7c8", 0.022))
        # chin strap
        xa_, xb_ = max(fx - 0.40, cx - 0.44), min(fx + 0.40, cx + 0.44)
        o += path("M%s %s Q%s %s %s %s" % (f(xa_), f(cy + 0.30), f((xa_ + xb_) / 2), f(cy + 0.60), f(xb_), f(cy + 0.30)), "none", "#26262a", 0.03)
        for sd in (-1, 1):
            hx_ = cx + sd * 0.585 - sh * 0.12
            if abs(hx_ - ox) < R:
                o += ell(hx_ - sd * 0.035, cy + 0.02, 0.028, 0.045, "#cfcfca", ink, 0.014)
        return o
    if st in ("curly", "flat", "mop"):
        pts = []
        if st == "curly":
            n = 14
            for i in range(n + 1):
                a = math.radians(-22 + 224 * i / n)
                r = 1.0 / math.sqrt((math.cos(a) / hw) ** 2 + (math.sin(a) / top) ** 2)
                pts.append((r * math.cos(a) * (1.04 if i % 2 else 0.93), r * math.sin(a) * (1.04 if i % 2 else 0.93)))
            inner = [(-0.42, -0.02), (-0.34, 0.20), (-0.18, 0.26), (-0.02, 0.21), (0.14, 0.27), (0.30, 0.20), (0.42, -0.02)]
            k_ = 0.75
        elif st == "flat":
            pts = [(0.50, 0.05), (0.56, 0.30), (0.50, top - 0.02), (0.20, top + 0.03), (-0.20, top + 0.03), (-0.50, top - 0.02), (-0.56, 0.30), (-0.50, 0.05)]
            inner = [(-0.44, 0.12), (-0.40, 0.33), (0.0, 0.37), (0.40, 0.33), (0.44, 0.12)]
            k_ = 0.2
        else:                                              # mop: a bowl cut with a straight heavy fringe
            n = 10
            for i in range(n + 1):
                a = math.radians(-14 + 208 * i / n)
                r = 1.0 / math.sqrt((math.cos(a) / hw) ** 2 + (math.sin(a) / top) ** 2)
                pts.append((r * math.cos(a), r * math.sin(a)))
            inner = [(-0.50, -0.14), (-0.42, 0.14), (-0.20, 0.17), (0.0, 0.14), (0.22, 0.17), (0.42, 0.14), (0.50, -0.14)]
            k_ = 0.3
        fr = [(cx + fs_ * x + sh * 0.45 * (1 - abs(x)) - sh * 0.10, cy - y) for x, y in inner]
        o += path(smooth_d(P(pts) + fr, True, k_), col, ink, 0.034)
        return o
    return ""


def _hair_back9(sp, cx, cy):
    H = sp["hair"]
    st = H["style"]
    if st not in STYLES9:
        return _hair_back0(sp, cx, cy)
    col = H.get("col", sp["hair_col"])
    ink = sp["ink"]
    top = 0.5 + H["top"]
    hw = H["width"] / 2
    if st == "helmet":
        R = 0.615
        pts = [(cx + R * math.cos(math.radians(-38 + 256 * i / 24)), cy - 0.07 - R * 1.02 * math.sin(math.radians(-38 + 256 * i / 24))) for i in range(25)]
        o = path(smooth_d(pts, True, 0.5), H.get("shell", "#f4f4f0"), ink, 0.036)
        ry_ = cy - 0.07 + R * 0.60
        o += path("M%s %s Q%s %s %s %s" % (f(cx - R * 0.80), f(ry_), f(cx), f(ry_ + 0.07), f(cx + R * 0.80), f(ry_)), "none", H.get("rim", "#3fa34d"), 0.05)
        o += line((cx, cy - 0.60), (cx, cy + 0.20), "#cfcfca", 0.02)
        return o
    pts = []
    n = 10
    for i in range(n + 1):
        a = math.radians(-20 + 220 * i / n)
        r = 1.0 / math.sqrt((math.cos(a) / hw) ** 2 + (math.sin(a) / top) ** 2)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    nape = [(cx - 0.44, cy + 0.20), (cx - 0.2, cy + 0.27), (cx + 0.2, cy + 0.27), (cx + 0.44, cy + 0.20)]
    o = path(smooth_d(pts + nape, True, 0.35), col, ink, 0.034)
    if st == "praew":
        o += _blob(cx, cy + 0.02, 0.19, 0.20, 5, col, ink, 0.034, n=10, jag=0.10)
        o += path("M%s %s Q%s %s %s %s" % (f(cx - 0.08), f(cy - 0.08), f(cx + 0.04), f(cy), f(cx - 0.04), f(cy + 0.1)), stroke=tint(col, 0.25), sw=0.016)
    return o


# ====================================================================================================== torso
_torso0, _collar0, _arm0, _hand0, _leg0, _pack0, _prop0 = D.torso_layer, D._collar, D.arm_layer, D._hand, D.leg_layer, D.pack_layer, D.prop_svg


def _geom(sp, view, s, K):
    th = s * BODY_YAW[view]
    a = sp["chest"] / 2
    b = a * 0.62
    ahalf = math.sqrt((a * math.cos(math.radians(th))) ** 2 + (b * math.sin(math.radians(th))) ** 2)
    bhalf = ahalf * sp["belt_w"] / sp["chest"]
    top = K["chin"] + sp["neck"]
    return dict(th=th, a=a, b=b, ahalf=ahalf, bhalf=bhalf, top=top, sy=K["shoulder_y"], belt=K["belt_y"], hem=K["belt_y"] + 0.02,
                crotch=K["crotch"], X=lambda phi, k=1.0: _cyl_x(phi, a * k, b, th))


def _collar9(sp, view, s, th, top, a, b, shirt):
    o9 = sp.get("outfit9")
    ink = sp["ink"]
    zx, zv = _cyl_x(3, a, b, th)
    if o9 == "coat":                                       # scrubs: a V neck with a darker trim
        o = path(pts_d([(zx - 0.17, top - 0.01), (zx + 0.17, top - 0.01), (zx + 0.01, top + 0.30)]), sp["skin"], ink, 0.020)
        o += poly_stroke([(zx - 0.17, top - 0.005), (zx + 0.01, top + 0.30), (zx + 0.17, top - 0.005)], shade(shirt, 0.30), 0.030)
        return o
    if o9 == "rider":                                      # zipped stand-up collar, a white tee inside
        o = path(pts_d([(zx - 0.10, top - 0.01), (zx + 0.10, top - 0.01), (zx, top + 0.11)]), "#f4f4f0", ink, 0.016)
        for side in (-1, 1):
            if view == "side" and side == -s:
                continue
            o += path(pts_d([(zx + side * 0.02, top + 0.10), (zx + side * 0.10, top - 0.045), (zx + side * 0.23, top - 0.02), (zx + side * 0.20, top + 0.13)]),
                      sp["col"]["jacket"], ink, 0.022)
        return o
    return _collar0(sp, view, s, th, top, a, b, shirt)


def _neck_wound(sp, pose, view, s, K, G, back):
    W = sp.get("neck_wound")
    if not W:
        return ""
    ink = sp["ink"]
    top, sy = G["top"], G["sy"]
    anat = W.get("side", "L")
    if view == "front":
        sg = (1 if anat == "L" else -1) * (-1 if back else 1)
        wx, wy = sg * 0.215, top + 0.045
        run = sg
        vis = True
    else:
        vis = is_near(anat, view, s)
        wx, wy = -s * (0.05 if view == "q" else 0.02), top + 0.05
        run = s * 0.6
    amt = W.get("blood", 1.0)
    dried = W.get("dried", False)
    c1, c2 = (BLOOD_DRY, "#3d100e") if dried else (BLOOD, BLOOD_DK)
    o = ""
    if not vis:                                           # the far side: only the soaked collar edge shows
        o += _blob(-s * 0.19, top + 0.06, 0.05, 0.07, 3, c2)
        return o
    if back and view == "front":
        o += _blob(wx, wy + 0.02, 0.09, 0.07, 3, c2, ink, 0.012)
        return o
    # blood down the chest on the wound side
    if amt > 0.05:
        L = 0.25 + 0.75 * amt
        o += path(smooth_d([(wx - 0.07, wy), (wx + 0.09, wy + 0.01), (wx + 0.11 + run * 0.02, wy + 0.30 * L), (wx + 0.05 + run * 0.05, wy + 0.72 * L),
                            (wx + run * 0.04, wy + 0.50 * L), (wx - 0.035 + run * 0.03, wy + 0.95 * L), (wx - 0.075, wy + 0.42 * L)], True, 0.5), c1)
        o += _drop(wx + 0.12 + run * 0.04, wy + 0.60 * L + 0.12, 0.022, c1)
    # torn collar flap + the bite: a ragged dark oval with tooth punctures
    o += path(pts_d([(wx - 0.13, wy - 0.035), (wx - 0.04, wy - 0.01), (wx - 0.09, wy + 0.05), (wx + 0.0, wy + 0.03), (wx - 0.02, wy + 0.11), (wx - 0.15, wy + 0.08)]),
              shade(sp["col"].get("shirt", "#888"), 0.35), ink, 0.014)
    o += _blob(wx, wy, 0.105, 0.070, 11, c2, ink, 0.016, n=10, jag=0.22)
    o += _blob(wx, wy, 0.055, 0.032, 12, "#2c0709")
    for k in range(4):
        a = math.radians(200 + k * 46)
        o += ell(wx + 0.082 * math.cos(a), wy + 0.050 * math.sin(a) - 0.004, 0.011, 0.011, "#2c0709")
    gz = W.get("gauze")
    if gz is not None:
        o += g(rect(-0.115, -0.10, 0.23, 0.20, "#f3f1ea", ink, 0.020, rx=0.02) +
               (_blob(0.01, 0.0, 0.03 + 0.085 * gz, 0.025 + 0.07 * gz, 21, c1) if gz > 0.02 else "") +
               line((-0.115, -0.045), (-0.16, -0.06), "#e8e2d2", 0.03) + line((0.115, 0.045), (0.16, 0.06), "#e8e2d2", 0.03),
               "translate(%s %s) rotate(%s)" % (f(wx), f(wy + 0.01), f(-14 * (1 if wx >= 0 else -1))))
    return o


def _suit(sp, pose, view, s, K, G, back):
    """navy single-breasted jacket open over the white shirt (sheet: Khun Tos), hem below the belt, notched lapels."""
    ink, bw = sp["ink"], sp["body_ink"]
    jk = sp["col"]["jacket"]
    X, ah, bh, top, sy, hem = G["X"], G["ahalf"], G["bhalf"], G["top"], G["sy"], G["hem"]
    jh = hem + 0.21
    o = ""
    if back:
        body = [(-ah * 0.62, top - 0.01), (-ah * 1.04, sy - 0.03), (-ah * 1.08, sy + 0.2), (-ah * 1.03, (sy + hem) / 2), (-bh * 1.10, jh), (bh * 1.10, jh),
                (ah * 1.03, (sy + hem) / 2), (ah * 1.08, sy + 0.2), (ah * 1.04, sy - 0.03), (ah * 0.62, top - 0.01)]
        o += path(smooth_d(body, True, 0.22), jk, ink, bw)
        o += line((0, top + 0.08), (0, jh - 0.26), shade(jk, 0.35), 0.014) + line((0, jh - 0.26), (0, jh), ink, 0.02)
        o += path("M-0.22 %s Q0 %s 0.22 %s" % (f(top - 0.015), f(top + 0.06), f(top - 0.015)), "none", ink, 0.024)
        return o
    zx = X(2)[0]
    for side in (-1, 1):
        if X(side * 50)[1] < -0.12:
            continue
        xb, xlow = X(side * 4)[0], X(side * 16)[0]
        xo = side * ah
        if (xo - xb) * side < 0.05:
            continue
        pan = [(zx + side * 0.15, top - 0.02), (xo * 1.03, sy - 0.03), (xo * 1.08, sy + 0.20), (xo * 1.04, (sy + hem) / 2), (side * bh * 1.12, jh),
               (xlow, jh), (xb, sy + 0.64), (zx + side * 0.07, top + 0.24)]
        o += path(smooth_d(pan, True, 0.16), jk, ink, bw)
        lap = [(zx + side * 0.15, top - 0.02), (X(side * 36)[0], sy + 0.20), (X(side * 30)[0], sy + 0.27), (xb, sy + 0.64), (zx + side * 0.07, top + 0.24)]
        if (lap[1][0] - lap[4][0]) * side > 0.03:
            o += path(pts_d(lap), tint(jk, 0.07), ink, 0.020)
        px_ = X(side * 52)[0]
        if X(side * 52)[1] > 0.2:                          # hip pocket flap
            o += line((px_ - 0.08, hem + 0.02), (px_ + 0.08, hem + 0.03), ink, 0.018)
        if side == 1 and X(40)[1] > 0.3:                   # the sheet's lapel pin
            o += rect(X(34)[0] - 0.02, sy + 0.16, 0.045, 0.022, "#8fb9e8")
    xb = X(0)[0]
    o += ell(xb, sy + 0.66, 0.018, 0.018, shade(jk, 0.5))
    return o


def _coat(sp, pose, view, s, K, G, back):
    """open white coat over light-blue scrubs (sheet: Dr. Praew): tunic hem, coat to mid-shin, lapels, pocket, badge,
    stethoscope round the neck."""
    ink, bw = sp["ink"], sp["body_ink"]
    c = sp["col"]
    ct = c["coat"]
    X, ah, bh, top, sy, hem, belt = G["X"], G["ahalf"], G["bhalf"], G["top"], G["sy"], G["hem"], G["belt"]
    cy_hem = G["crotch"] + 0.59 * sp["legs"]
    sway = pose.get("coat_sway", 0.0) * -s
    o = ""
    # tunic: the scrub top hangs over the hips
    tun = [(-bh * 1.0, belt - 0.05), (bh * 1.0, belt - 0.05), (bh * 1.05, belt + 0.25), (-bh * 1.05, belt + 0.25)]
    o += path(pts_d(tun), c["shirt"], ink, bw * 0.8)
    o += line((-bh * 0.96, belt - 0.05), (bh * 0.96, belt - 0.05), c["shirt"], 0.04)
    if back:
        body = [(-ah * 0.62, top - 0.01), (-ah * 1.08, sy - 0.03), (-ah * 1.13, sy + 0.25), (-bh * 1.24, belt + 0.1), (-bh * 1.55, cy_hem), (bh * 1.55, cy_hem),
                (bh * 1.24, belt + 0.1), (ah * 1.13, sy + 0.25), (ah * 1.08, sy - 0.03), (ah * 0.62, top - 0.01)]
        o += path(smooth_d(body, True, 0.14), ct, ink, bw)
        o += line((0, top + 0.1), (0, belt + 0.2), shade(ct, 0.18), 0.014) + line((0, belt + 0.2), (0, cy_hem), ink, 0.02)
        o += path("M-0.24 %s Q0 %s 0.24 %s L0.24 %s Q0 %s -0.24 %s Z" % (f(top - 0.02), f(top + 0.04), f(top - 0.02), f(top + 0.08), f(top + 0.14), f(top + 0.08)), ct, ink, 0.02)
        o += rect(-bh * 0.9, belt + 0.02, bh * 1.8, 0.07, ct, ink, 0.016)
        return o
    zx = X(2)[0]
    for side in (-1, 1):
        if X(side * 55)[1] < -0.15:
            continue
        xo = X(side * 25)[0]
        xe = side * ah
        if (xe - xo) * side < 0.05:
            continue
        pan = [(zx + side * 0.17, top - 0.02), (xe * 1.08, sy - 0.03), (xe * 1.13, sy + 0.25), (side * bh * 1.24, belt + 0.10),
               (side * bh * 1.56 + sway, cy_hem - 0.02), (xo * 1.25 + side * 0.10 + sway, cy_hem + 0.03), (xo * 1.08 + side * 0.03, belt + 0.25),
               (xo, sy + 0.52), (zx + side * 0.13, top + 0.22)]
        o += path(smooth_d(pan, True, 0.13), ct, ink, bw)
        lap = [(zx + side * 0.17, top - 0.02), (X(side * 42)[0], sy + 0.14), (X(side * 36)[0], sy + 0.22), (xo, sy + 0.52), (zx + side * 0.13, top + 0.22)]
        if (lap[1][0] - lap[4][0]) * side > 0.03:
            o += path(pts_d(lap), ct, ink, 0.020)
        vis = X(side * 55)[1]
        if side == -1 and vis > 0.25 or (view != "front" and side == -s and vis > 0.1):
            px_ = X(side * 55)[0] * 1.12                   # patch pocket with a flap, low on one panel
            o += rect(px_ - 0.11, belt + 0.30, 0.22, 0.24, ct, ink, 0.018, rx=0.015) + line((px_ - 0.11, belt + 0.375), (px_ + 0.11, belt + 0.375), ink, 0.014)
        if side == 1 and X(44)[1] > 0.3:                   # ID badge on a clip (no text: three grey lines)
            bx_ = X(44)[0]
            o += line((bx_, sy + 0.24), (bx_, sy + 0.31), "#3a3a3a", 0.022)
            o += rect(bx_ - 0.075, sy + 0.30, 0.15, 0.185, "#fbfbf8", ink, 0.016, rx=0.012)
            o += rect(bx_ - 0.075, sy + 0.30, 0.15, 0.045, "#6fa8dc")
            o += ell(bx_ - 0.03, sy + 0.395, 0.022, 0.022, "#b9c4cf")
            for k in range(2):
                o += line((bx_ + 0.005, sy + 0.385 + k * 0.03), (bx_ + 0.055, sy + 0.385 + k * 0.03), "#9aa6b2", 0.01)
    if sp.get("stethoscope", True):
        tb = "#2b2d33"
        xa, xb_ = X(-34)[0], X(34)[0]
        if X(-34)[1] > 0.0 and X(34)[1] > 0.0:
            d_ = "M%s %s C%s %s %s %s %s %s" % (f(xa * 0.95), f(top + 0.02), f(xa * 1.25), f(sy + 0.30), f(xb_ * 1.2), f(sy + 0.30), f(xb_ * 0.95), f(top + 0.02))
            lx, ly = xa * 0.98, sy + 0.14
            d2 = "M%s %s C%s %s %s %s %s %s" % (f(lx), f(ly), f(lx - 0.14), f(ly + 0.20), f(lx - 0.02), f(ly + 0.42), f(lx + 0.08), f(ly + 0.40))
            o += path(d_, "none", ink, 0.062) + path(d_, "none", tb, 0.034)
            o += path(d2, "none", ink, 0.056) + path(d2, "none", tb, 0.030)
            o += ell(lx + 0.10, ly + 0.40, 0.058, 0.058, "#d9dde2", ink, 0.022) + ell(lx + 0.10, ly + 0.40, 0.024, 0.024, "#8b949e")
            rx_, ry_ = xb_ * 0.98, sy + 0.14
            for k in (-1, 1):                              # the two ear tubes hanging on the other side
                o += line((rx_, ry_), (rx_ + k * 0.035, ry_ + 0.20), ink, 0.040) + line((rx_, ry_), (rx_ + k * 0.035, ry_ + 0.20), "#c9ced4", 0.018)
                o += ell(rx_ + k * 0.035, ry_ + 0.215, 0.02, 0.02, tb)
        else:
            xn = X(s * -10)[0]
            o += path("M%s %s Q%s %s %s %s" % (f(xn), f(top + 0.02), f(xn + s * 0.16), f(sy + 0.25), f(xn + s * 0.20), f(sy + 0.48)), "none", ink, 0.06)
            o += path("M%s %s Q%s %s %s %s" % (f(xn), f(top + 0.02), f(xn + s * 0.16), f(sy + 0.25), f(xn + s * 0.20), f(sy + 0.48)), "none", tb, 0.032)
            o += ell(xn + s * 0.21, sy + 0.52, 0.055, 0.055, "#d9dde2", ink, 0.022)
    return o


def _guard(sp, pose, view, s, K, G, back):
    ink = sp["ink"]
    X, top, sy = G["X"], G["top"], G["sy"]
    o = ""
    for side in (-1, 1):
        x, v = X(side * 62)
        if v > -0.1:                                       # epaulettes
            o += g(rect(-0.10, -0.03, 0.20, 0.06, "#1f2a44", ink, 0.014, rx=0.01), "translate(%s %s) rotate(%s)" % (f(x * 0.92), f(sy - 0.04), f(side * 12)))
        if back:
            continue
        px_, pv = X(side * 34)
        if pv > 0.25:                                      # chest pockets
            o += rect(px_ - 0.09 * pv, sy + 0.26, 0.18 * pv, 0.17, "none", shade(sp["col"]["shirt"], 0.35), 0.014, rx=0.01)
            o += line((px_ - 0.09 * pv, sy + 0.31), (px_ + 0.09 * pv, sy + 0.31), shade(sp["col"]["shirt"], 0.35), 0.014)
            if side == 1:                                  # a plain shield, no lettering
                o += path(pts_d([(px_ - 0.045, sy + 0.14), (px_ + 0.045, sy + 0.14), (px_ + 0.045, sy + 0.19), (px_, sy + 0.235), (px_ - 0.045, sy + 0.19)]), "#c9ced4", ink, 0.012)
    return o


WOUND_KINDS = ("mouth_blood", "cheek_bite", "brow_cut", "eye_shut", "veins", "chest_blood", "shoulder_bite", "belly_blood", "arm_bite",
               "sleeve_torn", "hand_blood", "knee_blood", "collar_blood", "shin_blood")


def _body_wounds(sp, pose, view, s, K, G, back):
    o = ""
    ink = sp["ink"]
    X, top, sy, hem = G["X"], G["top"], G["sy"], G["hem"]
    for w in sp.get("wounds", ()):
        k = w["kind"]
        sd = w.get("side", 1)
        if back and k != "collar_blood":
            continue
        if k == "chest_blood":
            x, v = X(sd * 24)
            if v > 0.2:
                o += _blob(x, sy + 0.34, 0.13 * v, 0.17, w.get("seed", 1), BLOOD_DK, n=8, jag=0.3)
                o += _drop(x + 0.03, sy + 0.66, 0.025, BLOOD_DK)
        elif k == "belly_blood":
            x, v = X(sd * 14)
            if v > 0.2:
                o += _blob(x, hem - 0.20, 0.15 * v, 0.12, w.get("seed", 2), BLOOD_DRY, n=9, jag=0.3)
        elif k == "shoulder_bite":
            x, v = X(sd * 58)
            if v > 0.0:
                o += _blob(x * 0.9, sy + 0.03, 0.10, 0.075, w.get("seed", 4), BLOOD_DK, ink, 0.014)
                o += _blob(x * 0.9, sy + 0.03, 0.045, 0.03, 5, "#2c0709")
                o += path(smooth_d([(x * 0.9 - 0.05, sy + 0.06), (x * 0.9 + 0.05, sy + 0.07), (x * 0.9 + 0.03, sy + 0.42), (x * 0.9 - 0.01, sy + 0.30), (x * 0.9 - 0.04, sy + 0.5)], True, 0.5), BLOOD_DK)
        elif k == "collar_blood":
            for sg in ((-1, 1) if not back else (sd,)):
                x, v = X(sg * 20)
                if v > 0.1:
                    o += _blob(x, top + 0.10 + 0.03 * sg, 0.085, 0.075, w.get("seed", 6) + sg, BLOOD_DRY, n=8, jag=0.35)
            o += _blob(X(sd * 30)[0], top + 0.30, 0.05, 0.10, w.get("seed", 6) + 5, BLOOD_DRY)
    return o


def torso9(sp, pose, view, s, K):
    o = _torso0(sp, pose, view, s, K)
    o9 = sp.get("outfit9")
    back = bool(pose.get("back"))
    if not (o9 or sp.get("neck_wound") or sp.get("wounds")):
        return o
    G = _geom(sp, view, s, K)
    if o9 == "suit":
        o += _suit(sp, pose, view, s, K, G, back)
    elif o9 == "coat":
        o += _coat(sp, pose, view, s, K, G, back)
    elif o9 == "guard":
        o += _guard(sp, pose, view, s, K, G, back)
    elif o9 == "rider" and not back:                       # the film's own scooter mark, at the sheet's size
        lx, lv = G["X"](8)
        if lv > 0.25:
            o += rect(lx - 0.22 * lv, G["sy"] + 0.10, 0.44 * lv, 0.34, sp["col"]["jacket"]) + D._scooter_logo(lx, G["sy"] + 0.25, 0.52 * lv)
    o += _neck_wound(sp, pose, view, s, K, G, back)
    o += _body_wounds(sp, pose, view, s, K, G, back)
    return o


# ====================================================================================================== limbs
def _hand9(sp, wr, d, shape, s, which, view):
    if shape not in ("claw_glove", "press", "fist_side"):
        return _hand0(sp, wr, d, shape, s, which, view)
    ink = sp["ink"]
    hsz = sp["hand"]
    col = sp["col"].get("glove", "#333333") if sp.get("glove") else sp["skin"]
    ang = math.degrees(math.atan2(d[1], d[0])) - 90
    side = (-1 if which == "R" else 1) if view == "front" else s
    o = ""
    if shape == "claw_glove":                              # a gloved hand hooked into a claw: thick spread fingers, no nails
        w, h = hsz * 0.95, hsz * 0.95
        for k in range(4):
            a = math.radians(-36 + k * 24)
            p0 = (math.sin(a) * w * 0.30, h * 0.50)
            p1 = (math.sin(a) * w * 0.66, h * 0.92)
            p2 = (math.sin(a) * w * 0.60 + 0.045 * side, h * 1.14)
            o += poly_stroke([p0, p1, p2], ink, 0.105)
            o += poly_stroke([p0, p1, p2], col, 0.060)
        o += ell(0, h * 0.36, w / 2, h * 0.38, col, ink, sp["body_ink"])
        o += ell(side * w * 0.47, h * 0.30, w * 0.16, h * 0.22, col, ink, sp["body_ink"] * 0.8, rot=-side * 30)
        o += rect(-w * 0.42, -0.02, w * 0.84, h * 0.2, shade(col, 0.3), ink, 0.018, rx=0.02)
    elif shape == "press":                                 # a flat hand laid on something, fingers together
        w, h = hsz * 1.0, hsz * 1.05
        o += rect(-w / 2, 0.0, w, h, col, ink, sp["body_ink"], rx=w * 0.32)
        for k in range(3):
            o += line((-w * 0.25 + k * w * 0.25, h * 0.55), (-w * 0.25 + k * w * 0.25, h * 0.92), shade(col, 0.5) if sp.get("glove") else ink, 0.014)
        o += ell(side * w * 0.46, h * 0.36, w * 0.17, h * 0.24, col, ink, sp["body_ink"] * 0.8, rot=-side * 20)
    else:                                                  # fist_side: hammer fist for banging
        w, h = hsz * 0.95, hsz * 0.90
        o += rect(-w / 2, 0.02, w, h, col, ink, sp["body_ink"], rx=w * 0.30)
        for k in range(3):
            o += line((-w * 0.5 + 0.03, h * (0.30 + 0.22 * k)), (-w * 0.20, h * (0.30 + 0.22 * k)), shade(col, 0.5) if sp.get("glove") else ink, 0.013)
    return g(o, "translate(%s %s) rotate(%s)" % (f(wr[0]), f(wr[1]), f(ang)))


def _watch_small(sp, el, wr, W):
    d = nrm(sub(wr, el))
    n_ = (-d[1], d[0])
    p = lerp(el, wr, 0.90)
    fw = max(sp["forearm"], sp.get("sleeve_w", 0.2) if sp["sleeve"] == "long" else sp["forearm"]) + 0.05
    ang = math.degrees(math.atan2(d[1], d[0])) - 90
    kong = W.get("style", "kong") == "kong"
    band, face = ("#17171a", "#f1efe6") if kong else ("#b9c0c8", "#f6f6f2")
    o = rect(-fw / 2 - 0.01, -0.045, fw + 0.02, 0.09, band, INK, 0.016, rx=0.01)
    o += ell(0, 0, 0.068, 0.068, face, INK, 0.022)
    if kong:
        o += line((0, 0), (0.034, -0.040), "#e0201c", 0.016)
        if W.get("blood"):
            o += ell(0, -0.050, 0.016, 0.016, BLOOD)
    else:
        o += line((0, 0), (0, -0.04), INK, 0.012) + line((0, 0), (0.03, 0.01), INK, 0.012)
    return g(o, "translate(%s %s) rotate(%s)" % (f(p[0]), f(p[1]), f(ang)))


def arm9(sp, pose, view, s, shoulder, hand, which, elbow=None, hand_shape=None, front_view_side=1):
    sp2 = sp
    if "sleeve_col" in sp:
        sp2 = dict(sp, col=dict(sp["col"], shirt=sp["sleeve_col"]), outfit="shirt" if sp["outfit"] in ("blazer", "delivery") else sp["outfit"])
    if hand_shape is None and sp.get("claws") and sp.get("glove"):
        hand_shape = "claw_glove"
    back = bool(pose.get("back"))
    o, an = _arm0(sp2, pose, view, s, shoulder, hand, which, elbow=elbow, hand_shape=hand_shape, front_view_side=front_view_side)
    el, wr = an["elbow"], an["wrist"]
    d = nrm(sub(wr, el))
    n_ = (-d[1], d[0])
    ink = sp["ink"]
    if sp.get("cuff_col") and sp["sleeve"] == "long":      # a shirt cuff showing under the jacket sleeve
        c0 = lerp(el, wr, 0.93)
        o_c = poly_stroke([c0, add(c0, d, 0.05)], ink, sp["sleeve_w"] * 0.86 + 0.05, cap="butt") + poly_stroke([add(c0, d, 0.004), add(c0, d, 0.046)], sp["cuff_col"], sp["sleeve_w"] * 0.86, cap="butt")
        o += o_c
    T = sp.get("tear")
    if T and which == label_of(T.get("side", "L"), view, s, back):
        lvl = T.get("level", 1)
        a0, a1 = lerp(el, wr, 0.30), lerp(el, wr, 0.90)
        sw_ = sp["sleeve_w"]
        if lvl >= 2:                                       # the cuff and lower sleeve dark and wet with blood
            o += poly_stroke([lerp(el, wr, 0.52), lerp(el, wr, 0.93)], BLOOD_DRY, sw_ * 0.92, cap="butt")
            o += poly_stroke([lerp(el, wr, 0.70), lerp(el, wr, 0.97)], BLOOD_DK, sw_ * 0.80, cap="butt")
        zig = []
        for k in range(7):                                 # the tear: a lengthwise gash, shirt and red inside
            p = lerp(a0, a1, k / 6.0)
            zig.append(add(p, n_, (0.05 if k % 2 else -0.035) * (1.0 if 0 < k < 6 else 0.2)))
        back_ = [add(lerp(a0, a1, k / 6.0), n_, -0.055 if 0 < k < 6 else 0.0) for k in range(6, -1, -1)]
        o += path(pts_d(zig + back_), "#f1eeea", ink, 0.016)
        o += poly_stroke([lerp(a0, a1, 0.15), lerp(a0, a1, 0.85)], BLOOD, 0.030)
        if lvl >= 3:                                       # blood running off the lowest point of the arm
            low = wr if wr[1] > el[1] else el
            o += poly_stroke([add(low, (0, -0.02)), add(low, (0.0, 0.16))], BLOOD, 0.028)
            o += _drop(low[0], low[1] + 0.33, 0.026, BLOOD)
            o += _drop(low[0] + 0.02, low[1] + 0.52, 0.018, BLOOD)
    W = sp.get("watch")
    if W and which == label_of(W.get("side", "L"), view, s, back):
        o += _watch_small(sp, el, wr, W)
    bh_ = sp.get("blood_hands", 0)
    if bh_:
        hp = an["hand"]
        o += _blob(hp[0] + 0.02, hp[1], 0.075 * (0.6 + 0.4 * bh_), 0.06, 31 + ord(which), BLOOD_DK, n=7, jag=0.35)
        o += _blob(hp[0] - 0.05, hp[1] - 0.06, 0.035, 0.03, 33, BLOOD)
    bf = sp.get("blood_forearm")
    if bf and sp["sleeve"] == "short" and which == label_of(bf, view, s, back):
        p0, p1 = lerp(el, wr, 0.25), lerp(el, wr, 0.80)
        o += poly_stroke([p0, lerp(p0, p1, 0.5), p1], BLOOD, sp["forearm"] * 0.55)
        o += _blob(lerp(p0, p1, 0.3)[0], lerp(p0, p1, 0.3)[1], 0.05, 0.035, 41, BLOOD_DK)
    for w in sp.get("wounds", ()):
        if w["kind"] in ("arm_bite", "sleeve_torn", "hand_blood") and which == w.get("arm", "L"):
            if w["kind"] == "arm_bite":
                p = lerp(shoulder, el, 0.62) if w.get("at", "upper") == "upper" else lerp(el, wr, 0.45)
                o += _blob(p[0], p[1], 0.085, 0.065, w.get("seed", 7), BLOOD_DK, ink, 0.014)
                o += _blob(p[0], p[1], 0.04, 0.028, 8, "#2c0709")
                o += poly_stroke([add(p, (0.0, 0.05)), add(p, (0.01, 0.24))], BLOOD_DK, 0.03)
            elif w["kind"] == "sleeve_torn":
                p = lerp(shoulder, el, 0.75)
                o += path(pts_d([add(p, n_, 0.11), add(add(p, n_, 0.05), d, 0.07), add(p, d, 0.01), add(add(p, n_, -0.05), d, 0.08), add(p, n_, -0.11),
                                 add(add(p, n_, -0.10), d, 0.16), add(add(p, n_, 0.10), d, 0.16)]), sp.get("skin_dk", "#97a38a"), ink, 0.014)
            else:
                hp = an["hand"]
                o += _blob(hp[0], hp[1], 0.08, 0.07, w.get("seed", 9), BLOOD_DK, n=7, jag=0.35)
    return o, an


def leg9(sp, pose, view, s, K, hip, foot, which, lift=0.0, toe=0.0, knee_bias=None):
    o, an = _leg0(sp, pose, view, s, K, hip, foot, which, lift, toe, knee_bias)
    knee, ank = an["knee"], an["ankle"]
    if sp.get("knee_dirt"):
        o += _blob(knee[0] + (s * 0.03 if view != "front" else 0), knee[1] + 0.04, 0.085, 0.10, 51 + ord(which), "#6b5a45", n=8, jag=0.3)
    for w in sp.get("wounds", ()):
        if w["kind"] == "knee_blood" and which == w.get("leg", "R"):
            o += _blob(knee[0], knee[1] + 0.02, 0.08, 0.11, w.get("seed", 3), BLOOD_DRY, n=8, jag=0.3)
        if w["kind"] == "shin_blood" and which == w.get("leg", "L"):
            p = lerp(knee, ank, 0.55)
            o += _blob(p[0], p[1], 0.07, 0.15, w.get("seed", 4), BLOOD_DK, n=8, jag=0.3)
    return o, an


def _crowbar_shape(L=1.55, col="#8d99a8"):
    """crowbar in its own frame: grip at the origin, shaft along +y, the hook at the +y end curling to +x, chisel at -y."""
    y0, y1 = -0.34, L - 0.34
    pts = [(0.0, y0 - 0.04), (0.0, y1 - 0.10), (0.03, y1), (0.12, y1 + 0.05), (0.20, y1 - 0.02), (0.21, y1 - 0.12)]
    d_ = smooth_d(pts, False, 0.5)
    o = path(d_, "none", INK, 0.105) + path(d_, "none", col, 0.060)
    o += line((-0.012, y0 + 0.10), (-0.012, y1 - 0.25), tint(col, 0.45), 0.014)
    o += path(pts_d([(-0.05, y0 - 0.02), (0.05, y0 - 0.02), (0.035, y0 - 0.16), (-0.02, y0 - 0.17)]), col, INK, 0.022)
    return o


def pack9(sp, view, s, K):
    o = _pack0(sp, view, s, K)
    if not sp.get("crowbar_pack"):
        return o
    back = CTX.get("back", False)
    sy, chin = K["shoulder_y"], K["chin"]
    # pushed through the pack's LEFT side loops, hook up over the left shoulder (continuity.md, scene 04 on)
    if view == "front":
        sg = -1 if back else 1                             # anatomical left: screen-right in front, screen-left from behind
        p_lo, p_hi = (sg * 0.30, sy + 0.95), (sg * 0.74, chin - 0.20)
        flip = sg
    else:
        p_lo, p_hi = (-s * 0.30, sy + 0.95), (-s * 0.86, chin - 0.22)
        flip = -s
    d = sub(p_hi, p_lo)
    ang = math.degrees(math.atan2(d[1], d[0])) - 90
    L = math.hypot(d[0], d[1])
    bar = g(_crowbar_shape(L), "translate(%s %s) rotate(%s) scale(%s 1) translate(0 0.34)" % (f(p_lo[0]), f(p_lo[1]), f(ang), f(-flip if ang < 0 else flip)))
    loops = ""
    for t in (0.18, 0.46):
        q = lerp(p_lo, p_hi, t)
        loops += g(rect(-0.075, -0.035, 0.15, 0.07, "#3a3a3d", INK, 0.016, rx=0.01), "translate(%s %s) rotate(%s)" % (f(q[0]), f(q[1]), f(ang)))
    return o + bar + loops


def prop9(kind, P, sp=None):
    if kind not in ("crowbar", "medbag", "flare", "torch", "helmet9", "gauze", "phone") or (kind == "phone" and not P.get("glow")):
        return _prop0(kind, P, sp)
    o = ""
    if kind == "phone":                                    # the lit screen pressed against the chest: only a halo escapes
        base = _prop0(kind, dict(P, at=(0, 0), angle=0.0, scale=None), sp)
        uid = "pg%d" % (abs(hash((round(P["at"][0], 3), round(P["at"][1], 3)))) % 99999)
        gl = float(P.get("glow", 1.0))
        o += '<defs><radialGradient id="%s"><stop offset="0" stop-color="#cfe4ff" stop-opacity="%s"/><stop offset="0.45" stop-color="#8fbaf5" stop-opacity="%s"/><stop offset="1" stop-color="#8fbaf5" stop-opacity="0"/></radialGradient></defs>' % (
            uid, f(0.85 * gl), f(0.35 * gl))
        o += ell(0, -0.06, 0.42, 0.46, "url(#%s)" % uid)
        o += base
    elif kind == "crowbar":
        o += _crowbar_shape(P.get("len", 1.55), P.get("col", "#8d99a8"))
    elif kind == "medbag":                                 # the small red first-aid pouch: wrist loop, flap, white cross
        loop = P.get("loop", True)
        if loop:
            o += path("M-0.07 0.10 C-0.14 -0.12 0.14 -0.12 0.07 0.10", "none", INK, 0.055) + path("M-0.07 0.10 C-0.14 -0.12 0.14 -0.12 0.07 0.10", "none", "#8c1f1b", 0.028)
        o += rect(-0.23, 0.08, 0.46, 0.36, "#c8322c", INK, 0.03, rx=0.06)
        o += path("M-0.23 0.17 Q0 0.27 0.23 0.17", "none", "#8c1f1b", 0.022)
        o += rect(-0.085, 0.215, 0.17, 0.17, "#f6f4ee", INK, 0.014, rx=0.02)
        o += rect(-0.018, 0.238, 0.036, 0.124, "#c8322c") + rect(-0.062, 0.282, 0.124, 0.036, "#c8322c")
        o += line((-0.20, 0.40), (-0.12, 0.40), "#e9a09a", 0.012)
    elif kind == "flare":                                  # road flare: red stick, white cap; lit = a hard pink-white jet
        lit = P.get("lit", False)
        o += rect(-0.045, -0.12, 0.09, 0.50, "#d23a2e", INK, 0.024, rx=0.02)
        o += rect(-0.045, 0.16, 0.09, 0.05, "#f1e9d6")
        o += rect(-0.05, -0.19, 0.10, 0.09, "#f4f2ec" if not lit else "#5a2a22", INK, 0.02, rx=0.015)
        if lit:
            uid = "fl%d" % (abs(hash((round(P["at"][0], 3), round(P["at"][1], 3), P.get("flick", 0)))) % 99999)
            k = 1.0 + 0.12 * math.sin(P.get("flick", 0) * 2.4)
            o += '<defs><radialGradient id="%s"><stop offset="0" stop-color="#ffd9d0" stop-opacity="0.85"/><stop offset="0.35" stop-color="#ff4a3a" stop-opacity="0.38"/><stop offset="1" stop-color="#ff2a2a" stop-opacity="0"/></radialGradient></defs>' % uid
            o += ell(0, -0.34, 0.62 * k, 0.62 * k, "url(#%s)" % uid)
            fl = [(-0.05, -0.19), (-0.12 * k, -0.34), (-0.05, -0.50 * k), (0.0, -0.72 * k), (0.06, -0.48 * k), (0.13 * k, -0.33), (0.05, -0.19)]
            o += path(smooth_d(fl, True, 0.6), "#ff5a4a", "#c81e1e", 0.016)
            o += path(smooth_d([(-0.03, -0.20), (-0.06, -0.32), (0.0, -0.50 * k), (0.06, -0.32), (0.03, -0.20)], True, 0.6), "#fff3e6")
            rnd = random.Random(int(P.get("flick", 0)) * 7 + 3)
            for i in range(6):
                a = math.radians(rnd.uniform(-70, 70) - 90)
                r0, r1 = rnd.uniform(0.30, 0.5), rnd.uniform(0.55, 0.85)
                o += line((r0 * math.cos(a), -0.26 + r0 * math.sin(a)), (r1 * math.cos(a), -0.26 + r1 * math.sin(a)), "#ffd0a8", 0.014)
    elif kind == "torch":                                  # the guard's torch, held but off
        o += rect(-0.045, -0.10, 0.09, 0.42, "#26272b", INK, 0.022, rx=0.02)
        o += path(pts_d([(-0.045, 0.30), (0.045, 0.30), (0.085, 0.42), (0.085, 0.50), (-0.085, 0.50), (-0.085, 0.42)]), "#3a3c42", INK, 0.022)
        o += rect(-0.07, 0.485, 0.14, 0.03, "#8d939b")
    elif kind == "helmet9":                                # carried helmet (sheet): white shell, dark visor, green rim
        o += ell(0, 0.17, 0.33, 0.31, "#f4f4f0", INK, 0.032)
        o += path("M-0.20 0.12 Q0.06 -0.02 0.30 0.12 L0.30 0.30 Q0.06 0.40 -0.16 0.33 Z", "#232a36", INK, 0.026)
        o += path("M-0.02 0.08 Q0.10 0.04 0.22 0.10", "none", "#aab7c8", 0.02)
        o += path("M-0.22 0.40 Q0.02 0.50 0.24 0.40", "none", "#3fa34d", 0.045)
        o += ell(-0.21, 0.22, 0.03, 0.05, "#cfcfca", INK, 0.014)
    elif kind == "gauze":
        gz = P.get("soak", 0.5)
        o += rect(-0.115, -0.02, 0.23, 0.20, "#f3f1ea", INK, 0.020, rx=0.02) + _blob(0.0, 0.08, 0.03 + 0.08 * gz, 0.025 + 0.065 * gz, 21, BLOOD)
    return g(o, "translate(%s %s) rotate(%s)%s" % (f(P["at"][0]), f(P["at"][1]), f(P.get("angle", 0.0)),
                                                     " scale(%s)" % f(P["scale"]) if P.get("scale") else ""))


_canvas0 = D.canvas_for


def canvas9(sp, margin=0.25):
    x0, y0, x1, y1 = _canvas0(sp, margin)
    pad = sp.get("canvas_pad")
    if pad:
        return (x0 - pad[0], y0 - pad[1], x1 + pad[0], y1 + (pad[2] if len(pad) > 2 else 0.0))
    return (x0, y0, x1, y1)


def watch_svg(sec=0.0, blood=True, smear=False, size=1.0):
    """the insert drawing of Kong's watch on the glove cuff, in a 2.4 x 2.4 box centred on (0, 0): no digits, twelve
    plain ticks, ONE red second hand, a drop of blood on the 12 mark.  sec = seconds since the bite (0 = on the drop)."""
    o = ""
    o += rect(-1.3, -0.42, 2.6, 0.84, "#17171a", INK, 0.05)                     # strap across the cuff
    for x in (-1.0, -0.82, 0.82, 1.0):
        o += ell(x, 0, 0.035, 0.035, "#3a3a3f")
    o += ell(0, 0, 0.86, 0.86, "#2b2d33", INK, 0.06)                            # case
    o += ell(0, 0, 0.72, 0.72, "#f1efe6", INK, 0.035)                           # dial
    o += rect(0.84, -0.09, 0.14, 0.18, "#3a3c42", INK, 0.03, rx=0.03)           # crown
    for k in range(12):
        a = math.radians(k * 30 - 90)
        r0 = 0.56 if k % 3 == 0 else 0.61
        o += line((r0 * math.cos(a), r0 * math.sin(a)), (0.67 * math.cos(a), 0.67 * math.sin(a)), INK, 0.05 if k % 3 == 0 else 0.028)
    if blood:
        o += _drop(0.0, -0.585, 0.085, BLOOD, BLOOD_DK, 0.012)
        o += ell(-0.025, -0.60, 0.02, 0.028, "#e8605f")
    if smear:
        o += path(smooth_d([(-0.45, 0.20), (-0.10, 0.05), (0.30, 0.22), (0.52, 0.10), (0.40, 0.36), (-0.05, 0.30), (-0.38, 0.42)], True, 0.6), BLOOD,
                  None, 0, ' fill-opacity="0.40"')
    a = math.radians(sec * 6.0 - 90)
    o += line((-0.16 * math.cos(a), -0.16 * math.sin(a)), (0.62 * math.cos(a), 0.62 * math.sin(a)), "#e0201c", 0.034)
    o += ell(0, 0, 0.055, 0.055, "#e0201c", INK, 0.016)
    o += path("M-0.50 -0.34 Q-0.18 -0.56 0.10 -0.50", "none", "#ffffff", 0.03, ' stroke-opacity="0.55"')
    return g(o, "scale(%s)" % f(size))


# ====================================================================================================== build
_build0 = D.build


def _unU(sp, pose, K, p):
    """figure-frame point -> the upper body's local frame (inverse of draw8.build's U)."""
    s = 1 if pose.get("s", 1) >= 0 else -1
    lean = pose.get("lean", 0.0)
    hip_y = K["hip_y"]
    piv = (K["hip_dx"], hip_y + 0.05)
    up = (K["hip_dx"], hip_y - (-sp["legs"] - 0.06))
    q = rot_pt(p, -lean * s, piv) if lean else p
    return (q[0] - up[0], q[1] - up[1])


ARM_KEYS = ("arm_n", "arm_f", "arm_r", "arm_l", "arm_R", "arm_L")


def _label_for_key(key, view, s):
    if key in ("arm_r", "arm_R"):
        return "R"
    if key in ("arm_l", "arm_L"):
        return "L"
    near = "L" if s > 0 else "R"
    far = "R" if s > 0 else "L"
    return near if key == "arm_n" else far


def build(spec, pose=None):
    sp = D.get_spec(spec)
    pose = dict(pose or {})
    view = pose.get("view", "front")
    back = view == "back"
    v2 = "front" if back else view
    s = 1 if pose.get("s", 1) >= 0 else -1
    CTX.clear()
    CTX.update(back=back, view=v2, s=s)
    K = D.skeleton(sp, pose)
    # ---- arm targets given in the figure frame / grabbing the other arm
    hd = tuple(pose.get("head", (0.0, 0.0, 0.0, 0.0))) + (0.0,) * 4
    for k in ARM_KEYS:                                     # targets named relative to the head: "neck" / "mouth"
        a = pose.get(k)
        if isinstance(a, dict) and "fig_rel" in a:
            a = dict(a)
            rel = a.pop("fig_rel")
            off = a.pop("_neck", (0.0, 0.0))
            if rel == "neck":
                a["hand"] = (off[0], K["chin"] + off[1])
            else:
                a["hand"] = (hd[2] + s * (0.0 if v2 == "front" else 0.16) + off[0], K["head_c"] + hd[3] + sp["face"]["mouth_y"] + 0.02 + off[1])
            a["absolute"] = True
            pose[k] = a
    need = [k for k in ARM_KEYS if isinstance(pose.get(k), dict) and ("fig" in pose[k] or "grab" in pose[k])]
    if any("grab" in pose[k] for k in need):
        p0 = dict(pose)
        for k in need:
            if "grab" in p0[k]:
                p0[k] = "down"
            else:
                a = dict(p0[k]); a["hand"] = _unU(sp, pose, K, a.pop("fig")); a["absolute"] = True; p0[k] = a
        an0 = _build0(sp, p0)["anchors"]
    for k in need:
        a = dict(pose[k])
        if "grab" in a:
            G_ = a.pop("grab")
            lab = _label_for_key("arm_" + G_["arm"], v2, s)
            el, wr = an0["elbow_" + lab], an0["wrist_" + lab]
            t = lerp(el, wr, G_.get("t", 0.8))
            a["fig"] = (t[0] + G_.get("dx", 0.0), t[1] + G_.get("dy", 0.0))
        a["hand"] = _unU(sp, pose, K, a.pop("fig"))
        a["absolute"] = True
        pose[k] = a
    zov = pose.pop("z", None)
    extra = pose.pop("extra", None)
    fig = _build0(sp, pose)
    if zov:
        near = "L" if s > 0 else "R"
        far = "R" if s > 0 else "L"
        alias = {"arm_n": "arm_" + near, "arm_f": "arm_" + far, "leg_n": "leg_" + near, "leg_f": "leg_" + far, "prop_n": "prop_" + near, "prop_f": "prop_" + far,
                 "arm_r": "arm_R", "arm_l": "arm_L"}
        for L in fig["layers"]:
            for k, z in zov.items():
                if alias.get(k, k) == L["name"]:
                    L["z"] = z
        fig["layers"].sort(key=lambda L: L["z"])
    if extra:
        for e in extra:
            fig["layers"].append(dict(name=e["name"], svg=e["svg"], z=e.get("z", 3.0), kind="prop", round=0.07))
        fig["layers"].sort(key=lambda L: L["z"])
    x0, y0, x1, y1 = D.canvas_for(sp)
    fig["bbox"] = (x0, y0, x1, y1)
    fig["anchors"]["mouth"] = (fig["anchors"]["head"][0] + s * (0.0 if v2 == "front" else 0.22), fig["anchors"]["head"][1] + sp["face"]["mouth_y"])
    return fig


def install():
    D._face = _face9
    D._hair = _hair9
    D._hair_back = _hair_back9
    D.torso_layer = torso9
    D._collar = _collar9
    D.arm_layer = arm9
    D._hand = _hand9
    D.leg_layer = leg9
    D.pack_layer = pack9
    D.prop_svg = prop9
    D.canvas_for = canvas9
    D.build = build


install()
flat_svg, doc, canvas_for, get_spec = D.flat_svg, D.doc, canvas9, D.get_spec
from specs9 import *          # noqa: E402,F401  (the EP.1 specs, the infected generator, pose helpers)
