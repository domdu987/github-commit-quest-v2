"""draw25d.py -- DEAD ZONE 09 cast drawn as a STACK OF SEPARATE LAYERS (2.5D puppets).

Pure Python 3 standard library, deterministic.  Uses the v2 puppet geometry helpers (smooth Catmull-Rom paths,
rotation) read-only; the drawing style follows uploads/character_sheet.webp: near-black ink outline, flat fills,
round white head, simple faces, full costumes (sleeves, trousers, boots) instead of v2 stick limbs.

Units and frame are the v2 puppet ones: 1 = D = head diameter, head centre (0, 0) when head_dx/dy are 0, x right,
y DOWN.  "r" / "l" = the screen-right / screen-left limb of the figure.

    fig = build(name, pose)            # name in CAST25
    fig["layers"]   list of dicts, back to front:  {"name", "svg" (fragment in D), "z" (depth in gap units, + = toward
                    the viewer), "kind" ("body"|"face"|"prop"), "shade" (toon weight 0..1)}
    fig["feet"]     (x, y) the point to plant on the floor (mid ankles, on the sole line)
    fig["seat"]     (x, y) hip centre (plant seated figures by this)
    fig["anchors"]  hand_r, hand_l, prop_tip_r, prop_tip_l, shoulder_*, elbow_*, knee_*, foot_*, head, eye_*, mouth, hip
    fig["view"]     "front" | "q" (three-quarter) | "side";  fig["s"] facing sign (-1, 0, +1)
    flat_svg(fig)   all layers in order: the 2D-flat composite (what v3 put on one card)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
import puppet as _pp                                      # read-only: path helpers

_smooth_closed = _pp._smooth_closed
_smooth_open = _pp._smooth_open

INK = "#1c1a22"
LW = 0.032                       # body outline width (D); ref/c f_014: coat 0.025-0.03, head 0.039-0.051 D
LW_HEAD = 0.044
VIEW_EDGES = (0.30, 0.80)        # |yaw| below 0.30 front, below 0.80 three-quarter, else side (x 35 deg: 10.5 and 28 deg)
VIEW_YAW = {"front": 0.0, "q": 0.5, "side": 1.0}

# ----------------------------------------------------------------------------------------------- small helpers
def _f(v):
    return "%.4f" % v


def _pt(p):
    return "%.4f,%.4f" % (p[0], p[1])


def _rot(p, deg, c=(0.0, 0.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _mul(a, k):
    return (a[0] * k, a[1] * k)


def _len(a):
    return math.hypot(a[0], a[1])


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _clamp(v, a, b):
    return a if v < a else b if v > b else v


def _wob(pts, seed, amp=0.006, closed=True):
    """baked hand-drawn wobble: each point is pushed along its normal by a fixed sum of sines of (index, seed)."""
    n = len(pts)
    out = []
    for i, p in enumerate(pts):
        a = pts[i - 1] if (closed or i > 0) else p
        b = pts[(i + 1) % n] if (closed or i < n - 1) else p
        t = _sub(b, a)
        L = _len(t) or 1.0
        nx, ny = -t[1] / L, t[0] / L
        k = amp * (math.sin(i * 2.17 + seed * 1.31) + 0.6 * math.sin(i * 5.03 + seed * 0.71))
        out.append((p[0] + nx * k, p[1] + ny * k))
    return out


def _shape(pts, fill, seed=0, lw=LW, amp=0.005, smooth=True, extra=""):
    pts = _wob(pts, seed, amp) if amp else pts
    d = _smooth_closed(pts) if smooth else "M" + " L".join(_pt(p) for p in pts) + " Z"
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"%s/>' % (d, fill, INK, _f(lw), extra)


def _line(pts, w=LW, col=INK, smooth=True, cap="round", op=None):
    d = _smooth_open(pts) if (smooth and len(pts) > 2) else "M" + " L".join(_pt(p) for p in pts)
    o = ' opacity="%.3f"' % op if op is not None else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"%s/>' % (
        d, col, _f(w), cap, o)


def _circle(c, r, fill, lw=LW, stroke=INK):
    s = ' stroke="%s" stroke-width="%s"' % (stroke, _f(lw)) if lw else ""
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"%s/>' % (_f(c[0]), _f(c[1]), _f(r), fill, s)


def _ellipse(c, rx, ry, fill, rot=0.0, lw=0.0, stroke=INK):
    s = ' stroke="%s" stroke-width="%s"' % (stroke, _f(lw)) if lw else ""
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" transform="rotate(%.2f %s %s)"%s/>' % (
        _f(c[0]), _f(c[1]), _f(rx), _f(ry), fill, rot, _f(c[0]), _f(c[1]), s)


def _poly_pts(path_pts, w, closed=False):
    """outline polygon of a polyline widened to w (miter-free, for clip paths)."""
    left, right = [], []
    n = len(path_pts)
    for i, p in enumerate(path_pts):
        a = path_pts[max(i - 1, 0)]
        b = path_pts[min(i + 1, n - 1)]
        t = _sub(b, a)
        L = _len(t) or 1.0
        nx, ny = -t[1] / L * w / 2, t[0] / L * w / 2
        left.append((p[0] + nx, p[1] + ny))
        right.append((p[0] - nx, p[1] - ny))
    return left + right[::-1]


def _tube(pts, w, fill, lw=LW, seed=0, amp=0.004):
    """an inked tube (sleeve, trouser leg): ink stroke w + 2 lw under a fill stroke w, round joins and caps."""
    pts = _wob(_resample(pts, 0.08), seed, amp, closed=False)
    d = _smooth_open(pts) if len(pts) > 2 else "M" + " L".join(_pt(p) for p in pts)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"/>') % (
        d, INK, _f(w + 2 * lw), d, fill, _f(w))


def _resample(pts, step):
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        L = _len(_sub(b, a))
        n = max(1, int(math.ceil(L / step)))
        for i in range(1, n + 1):
            out.append(_lerp(a, b, i / float(n)))
    return out


def _seg_band(pts, t0, t1, w, col, lw=0.012):
    """a band across a tube between path fractions t0..t1 (reflective sleeve stripes, cuffs)."""
    sub = _sub_path(pts, t0, t1)
    d = "M" + " L".join(_pt(p) for p in sub)
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="butt"/>'
            '<path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="butt"/>') % (
        d, INK, _f(w), d, col, _f(max(0.0, w - 2 * lw)))


def _sub_path(pts, t0, t1):
    segs = [_len(_sub(b, a)) for a, b in zip(pts[:-1], pts[1:])]
    tot = sum(segs) or 1.0

    def at(t):
        s = t * tot
        for (a, b), L in zip(zip(pts[:-1], pts[1:]), segs):
            if s <= L or L == segs[-1]:
                return _lerp(a, b, _clamp(s / (L or 1.0), 0.0, 1.0))
            s -= L
        return pts[-1]
    n = 6
    return [at(t0 + (t1 - t0) * i / float(n)) for i in range(n + 1)]


def _ik(S, T, L1, L2, pref):
    """two-bone IK. Returns (elbow, hand). pref: a direction; the elbow solution closer to it wins."""
    d = _sub(T, S)
    dist = _len(d)
    reach = (L1 + L2) * 0.999
    if dist > reach:
        T = _add(S, _mul(d, reach / dist))
        d = _sub(T, S)
        dist = reach
    dist = max(dist, abs(L1 - L2) + 1e-4, 1e-4)
    a = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
    h = math.sqrt(max(L1 * L1 - a * a, 0.0))
    u = (d[0] / dist, d[1] / dist)
    m = _add(S, _mul(u, a))
    e1 = (m[0] - u[1] * h, m[1] + u[0] * h)
    e2 = (m[0] + u[1] * h, m[1] - u[0] * h)
    pick = e1 if (e1[0] - m[0]) * pref[0] + (e1[1] - m[1]) * pref[1] >= (e2[0] - m[0]) * pref[0] + (e2[1] - m[1]) * pref[1] else e2
    return pick, T


# ----------------------------------------------------------------------------------------------- the cast
RESCUE = dict(jacket="#f07a1e", jacket_dk="#c9581a", band="#cfd5dc", band_line="#8d96a3", patch="#1d1c22",
              trouser="#2a2a30", trouser_ln="#4a4a54", boot="#17161b", sole="#5b5b63", glove="#1d1c21",
              pack="#34343b", pack_trim="#f07a1e", radio="#202024", strap="#2b2b31", belt="#151419",
              buckle="#b9bec6", collar="#2b2f3f")

CAST25 = {
    "kong": dict(label="Kong (38), rescue worker", seed=11, skin="#fbfaf5", hair="spiky", stubble=True,
                 costume="rescue", colors=dict(RESCUE), backpack=True, radio=True, flag=True,
                 sh_w=0.50, torso_top=0.44, hem=1.50, hip_y=1.56, hip_w=0.21, leg=1.13, arm1=0.55, arm2=0.50,
                 sleeve=0.235, leg_w=0.30, hand_r=0.118, boot=(0.40, 0.19), wet=False),
    "crew": dict(label="young rescue crew member", seed=23, skin="#fbfaf5", hair="mop", stubble=False,
                 costume="rescue", colors=dict(RESCUE), backpack=False, radio=True, flag=True,
                 sh_w=0.45, torso_top=0.44, hem=1.46, hip_y=1.52, hip_w=0.19, leg=1.12, arm1=0.53, arm2=0.48,
                 sleeve=0.215, leg_w=0.27, hand_r=0.11, boot=(0.37, 0.18), wet=False),
    "driver": dict(label="infected driver", seed=37, skin="#b8c3a8", skin_dk="#8e9a80", hair="messy", stubble=False,
                   costume="shirt", colors=dict(shirt="#a9bdd2", shirt_dk="#7f93ab", tear="#3b3f4c", stain="#6a2224",
                                                tie="#7d2a30", trouser="#545860", trouser_ln="#6d717a", boot="#1d1c21",
                                                sole="#4e4e56", belt="#1d1c21", buckle="#9aa0a8", collar="#a9bdd2"),
                   backpack=False, radio=False, flag=False, eyes="infected", hands="skin",
                   sh_w=0.46, torso_top=0.44, hem=1.50, hip_y=1.54, hip_w=0.20, leg=1.12, arm1=0.55, arm2=0.52,
                   sleeve=0.20, leg_w=0.27, hand_r=0.105, boot=(0.36, 0.15), wet=False),
    "namnuea": dict(label="Namnuea (14), Kong's daughter", seed=51, skin="#fbfaf5", hair="ponytail", stubble=False,
                    costume="hoodie", colors=dict(hoodie="#7c2230", hoodie_dk="#5c1622", tee="#f3efe8", trouser="#6d7078",
                                                  trouser_ln="#868991", boot="#c3262e", sole="#f1ede6", strap="#3b2b2e",
                                                  belt="#6d7078", buckle="#6d7078", collar="#7c2230", pack="#3d3a40",
                                                  pack_trim="#7c2230"),
                    backpack=True, radio=False, flag=False, lashes=True,
                    sh_w=0.40, torso_top=0.45, hem=1.40, hip_y=1.42, hip_w=0.17, leg=1.02, arm1=0.47, arm2=0.44,
                    sleeve=0.20, leg_w=0.24, hand_r=0.095, boot=(0.32, 0.15), wet=False),
}
# wet variant of Kong: darker fabric, flatter hair, drips; the shader adds glints (stage25 wet=True)
_kw = dict(CAST25["kong"])
_kw.update(label="Kong, wet (rain)", wet=True, hair="spiky_wet",
           colors=dict(RESCUE, jacket="#c8581b", jacket_dk="#9d4214", band="#aeb6c0", trouser="#1f1f25",
                       trouser_ln="#3a3a44", pack="#29292f", glove="#18171c"))
CAST25["kong_wet"] = _kw
_cw = dict(CAST25["crew"])
_cw.update(label="crew member, wet", wet=True, hair="mop_wet",
           colors=dict(RESCUE, jacket="#c8581b", jacket_dk="#9d4214", band="#aeb6c0", trouser="#1f1f25",
                       trouser_ln="#3a3a44"))
CAST25["crew_wet"] = _cw

EXPRESSIONS = {
    "kong": ["neutral", "determined", "tired", "guilty", "alarmed", "shouting", "talk", "blink"],
    "crew": ["neutral", "alarmed", "shouting", "pain", "blink"],
    "driver": ["still", "head_lift", "lunge"],
    "namnuea": ["smile", "neutral", "sad"],
}

# ----------------------------------------------------------------------------------------------- view logic
def view_of(yaw):
    a = abs(yaw)
    v = "front" if a < VIEW_EDGES[0] else "q" if a < VIEW_EDGES[1] else "side"
    s = 0 if v == "front" else (1 if yaw > 0 else -1)
    return v, s


def depth_table(view, s, seated=False):
    """layer -> depth in gap units (+ toward the viewer).  r/l limbs follow the facing: when the figure faces
    screen-right (s = +1) the screen-right limbs are the far ones."""
    if view == "front":
        z = dict(pack=-2.4, leg_r=-1.0, leg_l=-1.0, prop_far=None, torso=0.0, head=1.0, face=1.5, hair=2.0,
                 arm_r=2.6, arm_l=2.6, prop_r=2.3, prop_l=2.3, hairback=-0.6)
    else:
        far, near = ("r", "l") if s > 0 else ("l", "r")
        z = {"pack": -2.4, "hairback": -0.6, "torso": 0.0, "head": 1.0, "face": 1.5, "hair": 2.0,
             "arm_" + far: -1.6, "prop_" + far: -1.9, "leg_" + far: -1.1, "leg_" + near: -0.5,
             "arm_" + near: 2.6, "prop_" + near: 2.3}
        if seated:                                   # seated: thighs come toward the viewer over the seat
            z["leg_" + near] = 0.6
            z["leg_" + far] = -0.3
    return z


# ----------------------------------------------------------------------------------------------- body geometry
def _geom(C, view, s, pose):
    """shoulder, hip and head positions for the view (before lean)."""
    wf = {"front": 1.0, "q": 0.86, "side": 0.62}[view]
    g = {"wf": wf}
    sh_y = C["torso_top"] + 0.17
    if view == "front":
        g["sh"] = {"r": (C["sh_w"] - 0.02, sh_y), "l": (-(C["sh_w"] - 0.02), sh_y)}
        g["hp"] = {"r": (C["hip_w"], C["hip_y"]), "l": (-C["hip_w"], C["hip_y"])}
    elif view == "q":
        far, near = ("r", "l") if s > 0 else ("l", "r")
        cf, cn = (1 if far == "r" else -1), (1 if near == "r" else -1)
        g["sh"] = {near: (cn * (C["sh_w"] * 0.80), sh_y + 0.01), far: (cf * C["sh_w"] * 0.62, sh_y - 0.01)}
        g["hp"] = {near: (cn * C["hip_w"] * 0.85, C["hip_y"]), far: (cf * C["hip_w"] * 0.65, C["hip_y"] - 0.01)}
    else:
        far, near = ("r", "l") if s > 0 else ("l", "r")
        g["sh"] = {near: (-s * 0.04, sh_y + 0.01), far: (s * 0.06, sh_y - 0.02)}
        g["hp"] = {near: (-s * 0.02, C["hip_y"]), far: (s * 0.05, C["hip_y"] - 0.01)}
    return g


ARM_PRESETS = ("down", "hold", "phone_ear", "phone_look", "point", "raise", "reach", "push", "guard", "lap", "wheel",
               "claw", "drag", "wave")


def _arm_target(preset, c, view, s, C, sh, head):
    """hand target and elbow preference for a preset.  c = +1 (r) / -1 (l).  Facing sign s (0 in front view)."""
    L = C["arm1"] + C["arm2"]
    fs = s if s else c                               # 'forward' direction used by presets in front view
    near = (s == 0) or (c == -s)
    if preset == "down":
        if view == "front":
            return (sh[0] + c * 0.10, sh[1] + L * 0.97), (c, 0.3)
        return (sh[0] + s * (0.04 if near else 0.08), sh[1] + L * 0.97), (-s, 0.2)
    if preset == "hold":                             # carrying a heavy tool at the side, elbow slightly bent
        if view == "front":
            return (sh[0] + c * 0.16, sh[1] + L * 0.90), (c, -0.2)
        return (sh[0] + s * 0.12, sh[1] + L * 0.90), (-s, 0.1)
    if preset == "phone_ear":
        if view == "front":
            return (head[0] + c * 0.44, head[1] + 0.10), (c, 1.0)
        ex = head[0] - s * 0.34 if near else head[0] + s * 0.36
        return (ex, head[1] + 0.10), (-s * 0.3, 1.0)
    if preset == "phone_look":
        if view == "front":
            return (c * 0.12, sh[1] + 0.30), (c, 1.0)
        return (s * 0.42, sh[1] + 0.18), (-s * 0.2, 1.0)
    if preset == "point":
        return (sh[0] + fs * L * 0.96, sh[1] - 0.10), (0.0, 1.0)
    if preset == "raise":
        return (sh[0] + fs * 0.10, sh[1] - L * 0.92), (fs * -1.0 if view != "front" else c, 0.0)
    if preset == "reach":
        return (sh[0] + fs * L * 0.95, sh[1] + 0.05), (0.0, 1.0)
    if preset == "push":
        return (sh[0] + fs * L * 0.70, sh[1] + 0.32), (-fs * 0.5, 1.0)
    if preset == "guard":
        return (head[0] + fs * 0.30, head[1] + 0.25), (fs * 0.2, 1.0)
    if preset == "lap":
        return (sh[0] + fs * 0.32, sh[1] + 0.78), (-fs * 0.6, 0.6)
    if preset == "wheel":
        return (sh[0] + fs * 0.58, sh[1] + 0.30), (-fs * 0.2, 1.0)
    if preset == "claw":
        return (sh[0] + fs * L * 0.82, sh[1] - 0.25), (0.0, 1.0)
    if preset == "drag":
        return (sh[0] - fs * 0.30, sh[1] + L * 0.80), (fs, 0.2)
    if preset == "wave":
        return (sh[0] + c * 0.45, sh[1] - 0.55), (c, 0.4)
    return _arm_target("down", c, view, s, C, sh, head)


LEG_PRESETS = ("stand", "wide", "step", "lunge", "seated", "crouch", "fallen")


def _leg_targets(preset, view, s, C, hp, crouch=0.0):
    """ankle targets for r and l and knee preference."""
    L = C["leg"]
    base = C["hip_y"] + L * (1.0 - 0.38 * crouch)
    out = {}
    fs = s if s else 1
    for c, k in ((1, "r"), (-1, "l")):
        near = (s == 0) or (c == -s)
        h = hp[k]
        if preset == "seated":
            if view == "front":
                out[k] = ((h[0] + c * 0.05, h[1] + 0.78), (c * 0.2, -1.0))
            else:
                kx = h[0] + s * 0.62
                out[k] = ((kx + s * (0.02 if near else -0.05), h[1] + 0.64 + (0.0 if near else -0.02)), (s, -1.0))
            continue
        if preset == "wide":
            x = h[0] + c * 0.16 if view == "front" else h[0] + (s * 0.30 if near else -s * 0.22)
        elif preset == "step":
            x = h[0] + c * 0.03 if view == "front" else h[0] + (s * 0.34 if near else -s * 0.28)
        elif preset == "lunge":
            x = h[0] + c * 0.10 if view == "front" else h[0] + (s * 0.62 if not near else -s * 0.52)
        elif preset == "crouch":
            x = h[0] + c * 0.12 if view == "front" else h[0] + (s * 0.20 if near else -s * 0.10)
        else:
            x = h[0] + c * 0.035 if view == "front" else h[0] + (s * 0.03 if near else -s * 0.05)
        # knees bend toward the facing side (outward in front view)
        pref = (c * 0.7, -0.3) if view == "front" else (fs, -0.2)
        out[k] = ((x, base), pref)
    return out


# ----------------------------------------------------------------------------------------------- faces
def _face(C, expr, view, s, blink, mouth, gaze, wet):
    """face features in head-local coords (head centre 0,0, before head roll).  Returns svg."""
    sl = {"front": 0.0, "q": 0.13, "side": 0.27}[view] * (s if s else 0)
    esp = {"front": 0.30, "q": 0.25, "side": 0.0}[view]
    ey, by, my = -0.03, -0.18, 0.21
    infected = C.get("eyes") == "infected"
    pitch = 0.0
    if expr in ("guilty", "still"):
        pitch = 0.06
    if expr == "tired":
        pitch = 0.02
    ey += pitch; by += pitch; my += pitch * 0.8
    eyes = []
    if view == "side":
        eyes.append((sl + s * 0.02, ey, 1.0, "n"))
    else:
        if view == "front":
            eyes = [(-esp / 2, ey, 1.0, "l"), (esp / 2, ey, 1.0, "r")]
        else:
            far_x = sl + s * esp * 0.62
            near_x = sl - s * esp * 0.38
            eyes = [(near_x, ey, 1.0, "n"), (far_x, ey, 0.84, "f")]
    o = []
    gx, gy = (gaze if isinstance(gaze, tuple) else (gaze, 0.0))
    gx += 0.35 * s
    E = expr
    if blink == 2:
        E_eye = "closed"
    elif blink == 1:
        E_eye = "half"
    else:
        E_eye = {"neutral": "oval", "determined": "oval", "tired": "tired", "guilty": "down", "alarmed": "ring",
                 "shouting": "squeeze", "talk": "oval", "pain": "squeeze", "blink": "closed",
                 "still": "slit", "head_lift": "inf", "lunge": "inf_wide",
                 "smile": "happy", "sad": "down"}.get(E, "oval")
    for (x, y, sc, which) in eyes:
        sx = sc
        side_sign = -1 if x < sl else 1
        if E_eye == "oval":
            o.append(_ellipse((x + gx * 0.012, y), 0.040 * sx, 0.060, INK))
            o.append(_circle((x + gx * 0.012 + 0.012, y - 0.022), 0.012, "#ffffff", lw=0))
        elif E_eye == "tired":
            o.append('<path d="M%s A%s,%s 0 0 0 %s Z" fill="%s"/>' % (
                _pt((x - 0.042 * sx, y - 0.005)), _f(0.042 * sx), _f(0.045), _pt((x + 0.042 * sx, y - 0.005)), INK))
            o.append(_line([(x - 0.055 * sx, y - 0.012), (x + 0.055 * sx, y - 0.016)], 0.022))
            o.append(_line([(x - 0.04 * sx, y + 0.075), (x, y + 0.085), (x + 0.04 * sx, y + 0.072)], 0.010,
                           col="#8a8794"))
        elif E_eye == "down":
            o.append(_ellipse((x + gx * 0.01, y + 0.02), 0.036 * sx, 0.045, INK))
            o.append(_line([(x - 0.05 * sx, y - 0.018), (x + 0.05 * sx, y - 0.012)], 0.020))
        elif E_eye == "ring":
            o.append(_ellipse((x, y - 0.01), 0.068 * sx, 0.080, "#ffffff", lw=0.020))
            o.append(_circle((x + gx * 0.02, y - 0.005), 0.021, INK, lw=0))
        elif E_eye == "squeeze":
            d = side_sign if view == "front" else (1 if which == "n" else -1) * -s
            o.append(_line([(x - d * 0.055 * sx, y - 0.035), (x + d * 0.03 * sx, y), (x - d * 0.055 * sx, y + 0.035)], 0.024,
                           smooth=False))
        elif E_eye == "closed":
            o.append(_line([(x - 0.05 * sx, y + 0.005), (x, y + 0.02), (x + 0.05 * sx, y + 0.005)], 0.020))
        elif E_eye == "half":
            o.append('<path d="M%s A%s,%s 0 0 0 %s Z" fill="%s"/>' % (
                _pt((x - 0.040 * sx, y)), _f(0.040 * sx), _f(0.035), _pt((x + 0.040 * sx, y)), INK))
        elif E_eye == "happy":
            o.append(_line([(x - 0.05 * sx, y + 0.015), (x, y - 0.03), (x + 0.05 * sx, y + 0.015)], 0.022))
        elif E_eye == "slit":                       # infected, slumped: heavy lids, a sliver of white
            o.append(_ellipse((x, y + 0.02), 0.055 * sx, 0.022, "#eef0e6", lw=0.016))
            o.append(_line([(x - 0.065 * sx, y + 0.0), (x + 0.065 * sx, y + 0.008)], 0.022))
            o.append(_line([(x - 0.05 * sx, y + 0.07), (x + 0.05 * sx, y + 0.075)], 0.012, col=C.get("skin_dk", "#888")))
        elif E_eye in ("inf", "inf_wide"):
            ry = 0.075 if E_eye == "inf_wide" else 0.060
            o.append(_ellipse((x, y), 0.066 * sx, ry, "#f4f5ee", lw=0.020))
            o.append(_circle((x + gx * 0.012, y + 0.004), 0.013, "#d11f2b", lw=0))
            o.append(_line([(x - 0.06 * sx, y + ry + 0.035), (x + 0.055 * sx, y + ry + 0.04)], 0.013,
                           col=C.get("skin_dk", "#888")))
    # brows
    bro = {"neutral": (10, 0.0), "determined": (20, 0.01), "tired": (-6, 0.03), "guilty": (-20, -0.01),
           "alarmed": (-12, -0.06), "shouting": (30, 0.035), "talk": (14, 0.0), "pain": (-18, 0.0),
           "blink": (10, 0.0), "still": (0, 0.05), "head_lift": (22, 0.02), "lunge": (34, 0.03),
           "smile": (-8, -0.02), "sad": (-22, 0.0)}.get(E, (10, 0.0))
    bw = 0.040 if not C.get("lashes") else 0.022
    if C.get("eyes") == "infected":
        bw = 0.026
    for (x, y, sc, which) in eyes:
        if view == "front":
            side = 1 if x > 0 else -1                # inner end toward the centre
        else:
            side = s if which == "f" else -s
            if view == "side":
                side = -s
        ang = math.radians(bro[0])
        L = 0.085 * sc
        cx, cy = x, by + bro[1]
        # inner end (toward the nose) goes DOWN for positive angles
        inner = (cx - side * L * math.cos(ang) * 0.5 * -1, cy + L * math.sin(ang) * 0.5)
        outer = (cx + side * L * math.cos(ang) * 0.5, cy - L * math.sin(ang) * 0.5)
        inner = (cx - side * L * 0.5 * math.cos(ang), cy + L * 0.5 * math.sin(ang))
        o.append(_line([outer, inner], bw))
    # mouth
    mx = sl + (s * 0.07 if view == "side" else 0.0)
    m = mouth or {"neutral": "smirk", "determined": "flat", "tired": "flat_down", "guilty": "wavy", "alarmed": "o",
                  "shouting": "shout", "talk": "talk_b", "pain": "clench", "blink": "smirk", "still": "slack",
                  "head_lift": "slack_open", "lunge": "bite", "smile": "smile", "sad": "wavy"}.get(E, "flat")
    mw = 0.15 if view != "side" else 0.08
    if m == "smirk":
        o.append(_line([(mx - mw * 0.6, my), (mx + 0.01, my + 0.018), (mx + mw * 0.6, my - 0.012)], 0.020))
    elif m == "flat":
        o.append(_line([(mx - mw * 0.5, my + 0.005), (mx + mw * 0.5, my)], 0.022))
    elif m == "flat_down":
        o.append(_line([(mx - mw * 0.5, my + 0.015), (mx, my + 0.004), (mx + mw * 0.5, my + 0.016)], 0.020))
    elif m == "wavy":
        o.append(_line([(mx - mw * 0.5, my + 0.01), (mx - mw * 0.17, my - 0.008), (mx + mw * 0.17, my + 0.012),
                        (mx + mw * 0.5, my - 0.004)], 0.018))
    elif m == "smile":
        o.append(_line([(mx - mw * 0.55, my - 0.015), (mx, my + 0.035), (mx + mw * 0.55, my - 0.015)], 0.020))
    elif m in ("o", "talk_o"):
        o.append(_ellipse((mx, my + 0.02), 0.040, 0.050, "#4a1a22", lw=0.018))
    elif m in ("talk_a", "talk_b", "shout", "slack_open", "bite"):
        w, h = {"talk_a": (0.13, 0.05), "talk_b": (0.15, 0.09), "shout": (0.21, 0.15), "slack_open": (0.10, 0.06),
                "bite": (0.24, 0.17)}[m]
        if view == "side":
            w *= 0.6
        top = my - h * 0.3
        pts = [(mx - w / 2, top), (mx + w / 2, top), (mx + w * 0.38, top + h), (mx - w * 0.38, top + h)]
        o.append('<path d="%s" fill="#3b1218" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (
            _smooth_closed(pts), INK))
        if m in ("shout", "bite", "talk_b"):
            o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#fbfaf5"/>' % (
                _f(mx - w * 0.40), _f(top + 0.005), _f(w * 0.80), _f(h * 0.22)))
            o.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#c2414c"/>' % (
                _f(mx), _f(top + h * 0.82), _f(w * 0.25), _f(h * 0.16)))
        if m == "bite":
            for i in range(4):
                x0 = mx - w * 0.33 + i * w * 0.22
                o.append('<path d="M%s L%s L%s Z" fill="#e9e6d6"/>' % (
                    _pt((x0, top + h)), _pt((x0 + w * 0.06, top + h * 0.72)), _pt((x0 + w * 0.12, top + h))))
    elif m == "clench":
        o.append('<rect x="%s" y="%s" width="%s" height="0.06" rx="0.02" fill="#fbfaf5" stroke="%s" stroke-width="0.018"/>' % (
            _f(mx - mw * 0.6), _f(my - 0.02), _f(mw * 1.2), INK))
        o.append(_line([(mx - mw * 0.6, my + 0.01), (mx + mw * 0.6, my + 0.01)], 0.010))
    elif m == "slack":
        o.append(_line([(mx - mw * 0.45, my + 0.02), (mx, my + 0.03), (mx + mw * 0.45, my + 0.025)], 0.018))
    # stubble: Kong's chin and jaw dots, on the side of the face that shows
    if C.get("stubble"):
        k = 0
        for i in range(46):
            a = math.radians(25 + 130 * ((i * 0.618034) % 1.0))
            r = 0.30 + 0.13 * ((i * 0.381966 * 3.1) % 1.0)
            px, py = sl * 0.8 + math.cos(a) * r * (0.9 if view != "side" else 0.5), 0.08 + math.sin(a) * r * 0.85
            if px * px + py * py > 0.45 ** 2:
                continue
            if abs(px - mx) < 0.11 and abs(py - my) < 0.05:
                continue
            o.append(_circle((px, py), 0.0085, "#55525c", lw=0))
            k += 1
    # ear in 3/4 and side (back side of the head)
    if view != "front":
        ex = -s * (0.10 if view == "side" else 0.36)
        o.append('<path d="M%s C%s %s %s" fill="%s" stroke="%s" stroke-width="0.022"/>' % (
            _pt((ex + s * 0.02, -0.06)), _pt((ex - s * 0.10, -0.08)), _pt((ex - s * 0.10, 0.10)), _pt((ex + s * 0.02, 0.08)),
            C["skin"], INK))
    # cheeks
    if C.get("lashes"):
        for (x, y, sc, which) in eyes:
            o.append(_ellipse((x + (0.0 if view == "front" else 0.0), y + 0.11), 0.05 * sc, 0.025, "#f2a7a7", lw=0))
    # nose in side view
    if view == "side":
        o.append(_line([(sl + s * 0.20, -0.02), (sl + s * 0.235, 0.06), (sl + s * 0.19, 0.08)], 0.018))
    return "".join(o)


# ----------------------------------------------------------------------------------------------- hair
def _hair(C, view, s, seed):
    """returns (hairback_svg, hair_svg) in head-local coords."""
    style = C["hair"]
    sl = {"front": 0.0, "q": 0.13, "side": 0.27}[view] * (s if s else 0)
    back = ""
    if style.startswith("spiky") or style.startswith("mop"):
        wet = style.endswith("wet")
        mop = style.startswith("mop")             # crew: fewer, softer spikes swept to one side, long fringe
        n = 14 if not mop else 8
        a0, a1 = 196, 344                       # svg angle range over the crown (top = 270)
        if view != "front":                     # hair grows over the back of the head
            if s > 0:
                a0, a1 = 150, 336
            else:
                a0, a1 = 204, 390
        pts = []
        for i in range(n + 1):
            t = i / float(n)
            a = math.radians(a0 + (a1 - a0) * t)
            rv = 0.47
            pts.append((math.cos(a) * rv, math.sin(a) * rv))
            if i < n:
                am = math.radians(a0 + (a1 - a0) * (t + 0.5 / n))
                L = (0.63 if not wet else 0.56) + 0.04 * math.sin(i * 2.3 + seed) - (0.06 if mop else 0.0)
                lean = (0.18 if not wet else 0.45) * (1 if math.cos(am) > 0 else -1)
                if mop:
                    lean = 0.9 * (s if s else 1)
                dirx, diry = math.cos(am + lean * 0.5), math.sin(am + lean * 0.5)
                if wet:                          # drooping: tips pulled down
                    diry = diry * 0.75 + 0.35
                pts.append((math.cos(am) * 0.44 + dirx * (L - 0.44), math.sin(am) * 0.44 + diry * (L - 0.44)))
        # fringe zigzag back across the forehead
        fr_y = -0.27 if not wet else -0.22
        right = pts[-1]
        left = pts[0]
        fx0, fx1 = (-0.40, 0.40) if view == "front" else ((sl - 0.30, sl + 0.36) if s > 0 else (sl - 0.36, sl + 0.30))
        k = 6
        fr = []
        for i in range(k + 1):
            t = i / float(k)
            x = fx1 + (fx0 - fx1) * t
            fr.append((x, fr_y - 0.05 * math.sin(math.pi * t)))
            if i < k:
                xm = x + (fx0 - fx1) / (2 * k)
                tip = (0.13 if not wet else 0.18) + (0.07 if mop else 0.0)
                fr.append((xm + (0.04 if s >= 0 else -0.04), fr_y + tip - 0.04 * math.sin(math.pi * t)))
        poly = pts + [(right[0] * 0.98, right[1] * 0.98 + 0.03)] + fr + [(left[0] * 0.98, left[1] * 0.98 + 0.03)]
        hc = ("#141318" if not wet else "#101015") if not mop else ("#2e2422" if not wet else "#1d1716")
        svg = '<path d="M%s Z" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (
            " L".join(_pt(p) for p in _wob(poly, seed, 0.004)), hc, INK, _f(LW))
        # two grey highlight strokes
        svg += _line([(sl - 0.12, -0.40), (sl + 0.02, -0.44)], 0.018, col="#4a4955")
        if wet:                                  # wet sheen and drips from the tips
            svg += _line([(sl - 0.22, -0.33), (sl + 0.20, -0.38)], 0.020, col="#6f7f9a")
            for (x, y) in ((fx0 + 0.08, fr_y + 0.24), (fx1 - 0.14, fr_y + 0.26), (left[0] - 0.02, left[1] + 0.16)):
                svg += _drop((x, y), 0.035)
        return back, svg
    if style == "messy":                          # infected driver: thin, messy, dark
        pts = []
        for i in range(15):
            a = math.radians(190 + 160 * i / 14.0)
            r = 0.52 + 0.08 * ((i * 0.618) % 1.0)
            pts.append((math.cos(a) * r, math.sin(a) * r))
        pts += [(0.47, -0.10), (0.30 + sl, -0.24), (0.12 + sl, -0.12), (-0.05 + sl, -0.26), (-0.25 + sl, -0.14),
                (-0.40, -0.22), (-0.49, -0.08)]
        svg = '<path d="M%s Z" fill="#2c2a2a" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (
            " L".join(_pt(p) for p in _wob(pts, seed, 0.006)), INK, _f(LW))
        svg += _line([(-0.1, -0.5), (0.05, -0.62)], 0.02) + _line([(0.2, -0.47), (0.33, -0.58)], 0.02)
        return back, svg
    if style == "ponytail":
        side = s if s else 1
        # ponytail hangs behind the head on the back side
        px = -side * 0.42 if view != "front" else 0.42
        tail = [(px * 0.6, -0.36), (px + -side * 0.15 if view != "front" else 0.62, -0.30),
                (px + (-side * 0.28 if view != "front" else 0.30), 0.10), (px + (-side * 0.18 if view != "front" else 0.18), 0.45),
                (px + (-side * 0.06 if view != "front" else 0.05), 0.18), (px * 0.8, -0.10)]
        back = _shape(tail, "#17151a", seed + 3, LW, 0.004)
        top = []
        for i in range(15):
            a = math.radians(185 + 170 * i / 14.0)
            top.append((math.cos(a) * 0.54, math.sin(a) * 0.53))
        fr = [(0.50, 0.08), (0.36 + sl, -0.20), (0.18 + sl, -0.10), (0.0 + sl, -0.24), (-0.22 + sl, -0.12),
              (-0.38 + sl * 0.5, -0.22), (-0.50, 0.10)]
        svg = _shape(top + fr, "#17151a", seed, LW, 0.004)
        svg += _ellipse((px * 0.72, -0.32), 0.05, 0.035, "#c3262e", lw=0.014)   # red hair tie
        return back, svg
    return back, ""


def _drop(c, r):
    x, y = c
    d = "M%s C%s %s %s C%s %s %s Z" % (_pt((x, y - r * 1.6)), _pt((x + r * 0.2, y - r * 0.9)), _pt((x + r, y - r * 0.2)),
                                        _pt((x, y + r)), _pt((x - r, y - r * 0.2)), _pt((x - r * 0.2, y - r * 0.9)),
                                        _pt((x, y - r * 1.6)))
    return '<path d="%s" fill="#cfe3f5" stroke="#2d3550" stroke-width="0.010" opacity="0.95"/>' % d


# ----------------------------------------------------------------------------------------------- torso & costumes
def _torso_pts(C, view, s):
    wf = {"front": 1.0, "q": 0.86, "side": 0.62}[view]
    w = C["sh_w"] * wf
    top, hem = C["torso_top"], C["hem"]
    hw = (C["sh_w"] * 0.86) * wf
    sk = 0.0 if view == "front" else s * (0.03 if view == "q" else 0.07)
    pts = [(-w * 0.55 + sk, top), (-w * 0.96 + sk, top + 0.07), (-w * 1.03 + sk, top + 0.22),
           (-hw * 1.00, hem - 0.25), (-hw * 0.98, hem), (0.0, hem + 0.02), (hw * 0.98, hem), (hw * 1.00, hem - 0.25),
           (w * 1.03 + sk, top + 0.22), (w * 0.96 + sk, top + 0.07), (w * 0.55 + sk, top), (sk, top - 0.02)]
    if view == "side":                           # chest forward, back straight
        pts = [(-s * 0.04 + x if False else x, y) for (x, y) in pts]
    return pts, w, hw


def _torso_layer(C, view, s, uid):
    """torso layer: jacket / shirt / hoodie, pelvis block of the trousers, belt."""
    col = C["colors"]
    pts, w, hw = _torso_pts(C, view, s)
    seed = C["seed"]
    top, hem = C["torso_top"], C["hem"]
    cl = 0.0 if view == "front" else s * (0.17 if view == "q" else 0.30) * w / C["sh_w"]
    o = []
    # pelvis / trouser top under the jacket
    py0, py1 = hem - 0.12, C["hip_y"] + 0.22
    pel = [(-hw * 0.98, py0), (hw * 0.98, py0), (hw * 0.92, py1), (-hw * 0.92, py1)]
    o.append(_shape(pel, col["trouser"], seed + 5, LW, 0.003))
    cid = uid + "_tc"
    body_d = _smooth_closed(_wob(pts, seed, 0.004))
    o.append('<clipPath id="%s"><path d="%s"/></clipPath>' % (cid, body_d))
    cos = C["costume"]
    if cos == "rescue":
        fill = col["jacket"]
    elif cos == "shirt":
        fill = col["shirt"]
    else:
        fill = col["hoodie"]
    if cos == "shirt":                            # torn hem: jagged lower edge
        jag = []
        for i in range(9):
            t = i / 8.0
            x = hw * 0.98 - 2 * hw * 0.98 * t
            jag.append((x, hem + (0.06 if i % 2 else -0.02) + 0.02 * math.sin(i * 1.7)))
        pts2 = pts[:4] + jag[::-1] + pts[7:]
        pts2 = [pts[0], pts[1], pts[2], pts[3]] + [(p[0], p[1]) for p in reversed(jag)] + [pts[7], pts[8], pts[9], pts[10], pts[11]]
        body_d = _smooth_closed(_wob(pts, seed, 0.004))
        o.append('<path d="M%s Z" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (
            " L".join(_pt(p) for p in [pts[0], pts[1], pts[2], pts[3]] + jag[::-1] + [pts[7], pts[8], pts[9], pts[10], pts[11]]) if False else
            " L".join(_pt(p) for p in [pts[11], pts[0], pts[1], pts[2], pts[3]] + jag + [pts[7], pts[8], pts[9], pts[10]]),
            fill, INK, _f(LW)))
    else:
        o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>' % (body_d, fill, INK, _f(LW)))
    inner = []
    if cos == "rescue":
        # reflective bands (two) across the jacket, clipped
        for yb in (1.02, 1.24):
            inner.append('<rect x="-1" y="%s" width="2" height="0.085" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
                _f(yb), col["band"], col["band_line"]))
            inner.append('<rect x="-1" y="%s" width="2" height="0.012" fill="#eef2f6"/>' % _f(yb + 0.02))
        # zip / centre line and the collar
        inner.append(_line([(cl, top + 0.06), (cl * 0.95, hem)], 0.016, col="#7a3a12"))
        inner.append('<path d="M%s L%s L%s Z" fill="%s" stroke="%s" stroke-width="0.016"/>' % (
            _pt((cl - 0.20 * (1 if view != "side" else 0.4), top - 0.02)), _pt((cl, top + 0.16)),
            _pt((cl + 0.20 * (1 if view != "side" else 0.4), top - 0.02)), col["collar"], INK))
        # backpack straps
        if C.get("backpack"):
            for sx in ((-0.30, 0.30) if view == "front" else ((cl - s * 0.22,) if view == "q" else (cl - s * 0.05,))):
                inner.append('<path d="M%s L%s" stroke="%s" stroke-width="0.075" stroke-linecap="butt"/>' % (
                    _pt((sx, top + 0.02)), _pt((sx * 0.95, 0.98)), INK))
                inner.append('<path d="M%s L%s" stroke="%s" stroke-width="0.05" stroke-linecap="butt"/>' % (
                    _pt((sx, top + 0.02)), _pt((sx * 0.95, 0.98)), col["strap"]))
        # RESCUE patch on the chest
        if view != "side":
            px = cl - (0.05 if view == "front" else 0.0) - (0.0 if view == "front" else s * 0.02)
            pw = 0.46 if view == "front" else 0.38
            inner.append('<g transform="translate(%s %s)"><rect x="%s" y="-0.075" width="%s" height="0.15" rx="0.02" '
                         'fill="%s" stroke="%s" stroke-width="0.014"/>'
                         '<text x="0" y="0.047" text-anchor="middle" font-family="DejaVu Sans, Liberation Sans, Arial" '
                         'font-weight="bold" font-size="0.118" fill="#f6f4ee" textLength="%s" lengthAdjust="spacingAndGlyphs">RESCUE</text></g>' % (
                             _f(px), _f(0.80), _f(-pw / 2), _f(pw), col["patch"], INK, _f(pw * 0.86)))
        else:
            # side: the RESCUE word runs along the back panel, cut by the edge
            pass
        # chest radio on the strap (screen-right in front view, facing side otherwise)
        if C.get("radio"):
            rx = 0.30 if view == "front" else cl + s * (0.12 if view == "q" else 0.10)
            inner.append('<rect x="%s" y="0.56" width="0.12" height="0.20" rx="0.025" fill="%s" stroke="%s" stroke-width="0.016"/>' % (
                _f(rx - 0.06), col["radio"], INK))
            inner.append('<rect x="%s" y="0.60" width="0.07" height="0.04" fill="#6f8f7a"/>' % _f(rx - 0.035))
            inner.append(_line([(rx + 0.03, 0.56), (rx + 0.035, 0.38)], 0.024))
            inner.append(_circle((rx - 0.03, 0.71), 0.012, "#d33", lw=0))
        # hem shadow line (drawn ink, not lit)
        inner.append(_line([(-hw, hem - 0.05), (hw, hem - 0.05)], 0.012, col=col["jacket_dk"]))
    elif cos == "shirt":
        inner.append(_line([(cl, top + 0.08), (cl * 0.9, hem)], 0.012, col=col["shirt_dk"]))
        for yb in (0.70, 0.92, 1.14, 1.36):
            inner.append(_circle((cl + 0.03, yb), 0.016, "#e8eef4", lw=0.008))
        # loosened tie
        tx = cl + 0.02
        inner.append('<path d="M%s L%s L%s L%s Z" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
            _pt((tx - 0.035, top + 0.07)), _pt((tx + 0.045, top + 0.07)), _pt((tx + 0.10, 0.98)), _pt((tx + 0.02, 1.04)),
            col["tie"], INK))
        # rips: dark jagged openings and a stain at the collar
        for (cx, cy, sc) in ((-0.20, 1.05, 1.0), (0.24, 0.78, 0.8), (-0.05, 1.35, 0.7)):
            rp = [(cx - 0.10 * sc, cy), (cx - 0.03 * sc, cy - 0.05 * sc), (cx + 0.02 * sc, cy - 0.01 * sc),
                  (cx + 0.10 * sc, cy - 0.06 * sc), (cx + 0.06 * sc, cy + 0.04 * sc), (cx - 0.02 * sc, cy + 0.02 * sc)]
            inner.append('<path d="M%s Z" fill="%s" stroke="%s" stroke-width="0.012"/>' % (" L".join(_pt(p) for p in rp),
                                                                                          col["tear"], INK))
        inner.append(_ellipse((cl - 0.16, top + 0.12), 0.09, 0.05, col["stain"], rot=-15))
        inner.append(_ellipse((cl + 0.18, top + 0.30), 0.05, 0.03, col["stain"], rot=20))
        # collar points
        inner.append('<path d="M%s L%s L%s Z" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
            _pt((cl - 0.18, top - 0.01)), _pt((cl - 0.03, top + 0.12)), _pt((cl - 0.20, top + 0.10)), col["shirt"], INK))
        inner.append('<path d="M%s L%s L%s Z" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
            _pt((cl + 0.18, top - 0.01)), _pt((cl + 0.03, top + 0.12)), _pt((cl + 0.20, top + 0.10)), col["shirt"], INK))
    else:                                          # hoodie
        inner.append('<path d="M%s Q%s %s Q%s %s" fill="%s" stroke="%s" stroke-width="0.016"/>' % (
            _pt((cl - 0.30, top + 0.02)), _pt((cl - 0.05, top - 0.12)), _pt((cl, top + 0.10)),
            _pt((cl + 0.05, top - 0.12)), _pt((cl + 0.30, top + 0.02)), col["hoodie_dk"], INK))
        inner.append('<rect x="%s" y="%s" width="0.10" height="%s" fill="%s"/>' % (_f(cl - 0.05), _f(top + 0.08), _f(0.8),
                                                                                  col["tee"]))
        inner.append(_line([(cl - 0.05, top + 0.08), (cl - 0.05, hem)], 0.012, col=col["hoodie_dk"]))
        inner.append(_line([(cl + 0.05, top + 0.08), (cl + 0.05, hem)], 0.012, col=col["hoodie_dk"]))
        inner.append(_line([(cl - 0.10, top + 0.14), (cl - 0.12, top + 0.38)], 0.010, col="#e8dcd2"))
        inner.append(_line([(cl + 0.10, top + 0.14), (cl + 0.12, top + 0.38)], 0.010, col="#e8dcd2"))
        inner.append('<rect x="%s" y="%s" width="%s" height="0.18" rx="0.04" fill="none" stroke="%s" stroke-width="0.012"/>' % (
            _f(cl - 0.22), _f(hem - 0.40), _f(0.44), col["hoodie_dk"]))
        if C.get("backpack"):
            for sx in ((-0.26, 0.26) if view == "front" else ((cl - s * 0.20,),) [0]):
                inner.append('<path d="M%s L%s" stroke="%s" stroke-width="0.055" stroke-linecap="butt"/>' % (
                    _pt((sx, top + 0.02)), _pt((sx * 0.95, 0.95)), col["strap"]))
    if C.get("wet"):                               # wet: darker drip streaks and drops on the hem
        for i, x in enumerate((-0.30, -0.05, 0.22)):
            inner.append(_line([(x, 0.62 + 0.05 * i), (x + 0.01, 1.0 + 0.05 * i)], 0.018, col=col.get("jacket_dk", "#555"),
                               op=0.55))
        for x in (-0.32, 0.02, 0.30):
            inner.append(_drop((x, hem + 0.09), 0.032))
    o.append('<g clip-path="url(#%s)">%s</g>' % (cid, "".join(inner[:-3] if (C.get("wet") and False) else
                                                                [i for i in inner if 'cfe3f5' not in i])))
    o.extend([i for i in inner if 'cfe3f5' in i])     # drips hang below the hem, not clipped
    # belt over the trouser top
    o.append('<rect x="%s" y="%s" width="%s" height="0.075" fill="%s" stroke="%s" stroke-width="0.014"/>' % (
        _f(-hw * 0.95), _f(hem - 0.005), _f(2 * hw * 0.95), col["belt"], INK))
    if C["costume"] != "hoodie":
        o.append('<rect x="%s" y="%s" width="0.09" height="0.065" fill="%s" stroke="%s" stroke-width="0.012"/>' % (
            _f(cl - 0.045), _f(hem), col["buckle"], INK))
    return "".join(o)


def _pack_layer(C, view, s):
    if not C.get("backpack"):
        return ""
    col = C["colors"]
    top = C["torso_top"]
    if view == "front":
        out = ""
        for c in (-1, 1):
            pts = [(c * (C["sh_w"] * 0.80), top + 0.10), (c * (C["sh_w"] * 1.20), top + 0.12), (c * (C["sh_w"] * 1.24), top + 0.85),
                   (c * (C["sh_w"] * 0.90), top + 0.90)]
            out += _shape(pts, col["pack"], C["seed"] + c, LW, 0.003)
        return out
    w = 0.42 if view == "side" else 0.34
    x0 = -s * (C["sh_w"] * (0.30 if view == "side" else 0.55))
    pts = [(x0, top + 0.05), (x0 - s * w, top + 0.10), (x0 - s * (w + 0.04), top + 0.95), (x0 + s * 0.02, top + 1.00)]
    out = _shape(pts, col["pack"], C["seed"] + 7, LW, 0.003)
    out += _line([(x0 - s * w * 0.2, top + 0.40), (x0 - s * (w * 0.9), top + 0.42)], 0.03, col=col["pack_trim"])
    out += '<rect x="%s" y="%s" width="%s" height="0.22" rx="0.03" fill="none" stroke="%s" stroke-width="0.014"/>' % (
        _f(min(x0 - s * w * 0.85, x0 - s * w * 0.15)), _f(top + 0.55), _f(w * 0.7), INK)
    return out


# ----------------------------------------------------------------------------------------------- limbs
def _arm_svg(C, k, S, E, H, view, s, wet, flag):
    col = C["colors"]
    sleeve = col.get("jacket") or col.get("shirt") or col.get("hoodie")
    if C["costume"] == "shirt":
        sleeve = col["shirt"]
    if C["costume"] == "hoodie":
        sleeve = col["hoodie"]
    pts = [S, E, H]
    o = [_tube(pts, C["sleeve"], sleeve, LW, C["seed"] + (3 if k == "r" else 5))]
    if C["costume"] == "rescue":
        o.append(_seg_band(pts, 0.30, 0.36, C["sleeve"] + 0.02, col["band"]))
        o.append(_seg_band(pts, 0.70, 0.76, C["sleeve"] + 0.02, col["band"]))
        o.append(_seg_band(pts, 0.92, 0.98, C["sleeve"] + 0.01, col["jacket_dk"]))
        if flag:
            # Thai flag patch on the upper sleeve: red, white, blue (double), white, red
            sub = _sub_path(pts, 0.10, 0.24)
            a, b = sub[0], sub[-1]
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            m = _lerp(a, b, 0.5)
            fw, fh = 0.15, 0.11
            stripes = [("#c8102e", 1), ("#f4f2ee", 1), ("#2d2a6e", 2), ("#f4f2ee", 1), ("#c8102e", 1)]
            g = ['<g transform="translate(%s %s) rotate(%.2f)">' % (_f(m[0]), _f(m[1]), ang + 90 * 0)]
            y = -fh / 2
            for c_, n in stripes:
                hh = fh * n / 6.0
                g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (_f(-fw / 2), _f(y), _f(fw), _f(hh + 0.002), c_))
                y += hh
            g.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" stroke-width="0.012"/></g>' % (
                _f(-fw / 2), _f(-fh / 2), _f(fw), _f(fh), INK))
            # keep the flag upright-ish: rotate it with the sleeve but never upside down
            o.append("".join(g))
    elif C["costume"] == "shirt":
        sub = _sub_path(pts, 0.55, 0.62)          # a torn sleeve: dark rip
        m = sub[3]
        o.append('<path d="M%s L%s L%s L%s Z" fill="%s"/>' % (_pt((m[0] - 0.05, m[1] - 0.02)), _pt((m[0] + 0.01, m[1] - 0.05)),
                                                             _pt((m[0] + 0.05, m[1] + 0.01)), _pt((m[0] - 0.01, m[1] + 0.04)),
                                                             col["tear"]))
    if wet:
        o.append(_drop(_add(H, (0.0, C["hand_r"] + 0.07)), 0.03))
    # hand
    hc = col.get("glove", C["skin"]) if C.get("hands") != "skin" else C["skin"]
    if C["costume"] == "hoodie":
        hc = C["skin"]
    d = _sub(H, E)
    L = _len(d) or 1.0
    u = (d[0] / L, d[1] / L)
    hc_pt = _add(H, _mul(u, C["hand_r"] * 0.35))
    o.append(_circle(hc_pt, C["hand_r"], hc, lw=LW))
    th = _add(hc_pt, _add(_mul(u, -C["hand_r"] * 0.2), _mul((-u[1], u[0]), C["hand_r"] * 0.85 * (1 if k == "r" else -1))))
    o.append(_ellipse(th, C["hand_r"] * 0.42, C["hand_r"] * 0.30, hc, rot=math.degrees(math.atan2(u[1], u[0])), lw=0.022))
    if C.get("eyes") == "infected":              # claw fingers
        for i in (-1, 0, 1):
            dd = _rot(u, i * 22)
            p0 = _add(hc_pt, _mul(dd, C["hand_r"] * 0.9))
            p1 = _add(hc_pt, _mul(dd, C["hand_r"] * 1.65))
            o.append(_line([p0, p1], 0.032, col=INK))
            o.append(_line([p0, p1], 0.014, col=C["skin"]))
    return "".join(o)


def _leg_svg(C, k, Hp, K, A, view, s, wet, seated=False):
    col = C["colors"]
    pts = [Hp, K, A]
    o = [_tube(pts, C["leg_w"], col["trouser"], LW, C["seed"] + (7 if k == "r" else 9))]
    # cargo pocket on the thigh (outside), knee crease
    th = _sub_path(pts, 0.22, 0.42)
    m = th[3]
    a, b = th[0], th[-1]
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    if C["costume"] == "rescue":
        o.append('<g transform="translate(%s %s) rotate(%.2f)"><rect x="-0.08" y="-0.075" width="0.16" height="0.15" rx="0.02" '
                 'fill="%s" stroke="%s" stroke-width="0.014"/><path d="M-0.08,-0.035 L0.08,-0.035" stroke="%s" stroke-width="0.012"/></g>' % (
                     _f(m[0]), _f(m[1]), ang - 90, col["trouser"], col["trouser_ln"], col["trouser_ln"]))
    kn = _sub_path(pts, 0.50, 0.56)
    o.append(_line([_add(kn[0], (-0.06, 0)), _add(kn[-1], (0.05, 0.01))], 0.012, col=col["trouser_ln"]))
    if wet:
        o.append(_line(_sub_path(pts, 0.62, 0.9), 0.04, col="#3d4a66", op=0.45))
    # boot
    bl, bh = C["boot"]
    if view == "front" and not seated:
        cx = A[0] + (0.02 if k == "r" else -0.02)
        pts_b = [(cx - bl * 0.42, A[1] - 0.02), (cx + bl * 0.42, A[1] - 0.02), (cx + bl * 0.48, A[1] + bh * 0.75),
                 (cx + bl * 0.40, A[1] + bh), (cx - bl * 0.40, A[1] + bh), (cx - bl * 0.48, A[1] + bh * 0.75)]
    else:
        f = s if s else 1
        pts_b = [(A[0] - f * bl * 0.30, A[1] - 0.04), (A[0] + f * bl * 0.20, A[1] - 0.04), (A[0] + f * bl * 0.62, A[1] + bh * 0.45),
                 (A[0] + f * bl * 0.70, A[1] + bh), (A[0] - f * bl * 0.34, A[1] + bh)]
    o.append(_shape(pts_b, col["boot"], C["seed"] + (11 if k == "r" else 13), LW, 0.003))
    ys = A[1] + bh - 0.035
    xs = [p[0] for p in pts_b]
    o.append('<path d="M%s L%s" stroke="%s" stroke-width="0.03" stroke-linecap="round"/>' % (
        _pt((min(xs) + 0.04, ys)), _pt((max(xs) - 0.04, ys)), col["sole"]))
    return "".join(o)


# ----------------------------------------------------------------------------------------------- props
PROP_TYPES = ("cutter", "crowbar", "phone", "medkit")
PROP_TIP = {"cutter": 1.18, "crowbar": 1.30, "phone": 0.10, "medkit": 0.40}


def battery_colour(bars):
    return {3: "#39c45a", 2: "#f2c230", 1: "#e2453b"}.get(int(bars), "#5b5b63")


def prop_svg(kind, H, ang, sc=1.0, opts=None):
    """prop drawn in figure coords: grip at H, main axis along angle ang (deg, svg)."""
    opts = opts or {}
    o = ['<g transform="translate(%s %s) rotate(%.3f) scale(%.4f)">' % (_f(H[0]), _f(H[1]), ang, sc)]
    if kind == "cutter":
        # cordless hydraulic rescue cutter: rear loop handle (black) at the grip, battery pack, orange body, twin blades
        bars = int(_clamp(opts.get("bars", 3), 0, 3))
        o.append(_shape([(-0.16, -0.10), (0.16, -0.12), (0.20, 0.10), (-0.16, 0.12)], "#1d1c21", 61, 0.024, 0.0))   # handle block
        o.append('<rect x="-0.30" y="-0.17" width="0.20" height="0.34" rx="0.04" fill="#232228" stroke="%s" stroke-width="0.024"/>' % INK)
        o.append(_shape([(0.14, -0.15), (0.70, -0.13), (0.76, -0.08), (0.76, 0.08), (0.70, 0.13), (0.14, 0.15)],
                        "#f07a1e", 62, 0.026, 0.002))                                                             # orange body
        o.append('<rect x="0.30" y="-0.155" width="0.10" height="0.31" fill="#1d1c21" stroke="%s" stroke-width="0.016"/>' % INK)  # carry grip
        # battery indicator (review fix: it sat on the pack under the glove, 0.17 x 0.07 D, hidden at phone size).
        # Now on the open top of the orange body in front of the hand, 0.29 x 0.11 D with an ink border.
        o.append('<rect x="0.425" y="-0.128" width="0.29" height="0.108" rx="0.016" fill="#0c0c10" stroke="%s" '
                 'stroke-width="0.016"/>' % INK)
        for i in range(3):
            c = battery_colour(bars) if i < bars else "#3a3a42"
            o.append('<rect x="%s" y="-0.112" width="0.078" height="0.076" rx="0.010" fill="%s"/>' % (_f(0.442 + i * 0.088), c))
        o.append('<text x="0.53" y="0.06" text-anchor="middle" font-family="DejaVu Sans, Arial" font-weight="bold" font-size="0.075" '
                 'fill="#1d1c21">DZ-9</text>')
        # jaw: two curved blades
        o.append(_shape([(0.74, -0.08), (0.92, -0.10), (1.16, -0.02), (1.20, 0.01), (0.96, -0.01), (0.76, 0.0)],
                        "#9aa3ad", 63, 0.022, 0.0))
        o.append(_shape([(0.74, 0.0), (0.96, 0.03), (1.20, 0.03), (1.15, 0.07), (0.92, 0.11), (0.74, 0.08)],
                        "#7e8792", 64, 0.022, 0.0))
        o.append(_circle((0.80, 0.0), 0.035, "#d6dbe0", lw=0.016))
    elif kind == "crowbar":
        o.append(_line([(-0.30, 0.0), (1.20, 0.0)], 0.085, col=INK))
        o.append(_line([(-0.30, 0.0), (1.20, 0.0)], 0.050, col="#b8262a"))
        o.append(_line([(-0.25, -0.012), (1.15, -0.012)], 0.012, col="#e36a62"))
        # hooked claw end beyond the grip, chisel at the tip
        o.append('<path d="M-0.30,0 C-0.42,0 -0.48,0.10 -0.42,0.18 C-0.38,0.22 -0.32,0.20 -0.30,0.16" fill="none" stroke="%s" '
                 'stroke-width="0.085" stroke-linecap="round"/>' % INK)
        o.append('<path d="M-0.30,0 C-0.42,0 -0.48,0.10 -0.42,0.18 C-0.38,0.22 -0.32,0.20 -0.30,0.16" fill="none" stroke="#5c6068" '
                 'stroke-width="0.05" stroke-linecap="round"/>')
        o.append('<path d="M1.18,-0.035 L1.32,-0.01 L1.32,0.01 L1.18,0.035 Z" fill="#8f959d" stroke="%s" stroke-width="0.016"/>' % INK)
    elif kind == "phone":
        # held upright: the screen faces the viewer; ang only tilts it a little
        o.append('<g transform="rotate(%.3f)">' % (-ang + opts.get("tilt", 0.0)))
        w, h = 0.20, 0.38
        o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="0.03" fill="#141418" stroke="%s" stroke-width="0.020"/>' % (
            _f(-w / 2), _f(-h * 0.62), _f(w), _f(h), INK))
        scr = opts.get("screen", "call")
        sx, sy, sw, shh = -w / 2 + 0.014, -h * 0.62 + 0.022, w - 0.028, h - 0.044
        if scr and opts.get("screen_png"):
            o.append('<image x="%s" y="%s" width="%s" height="%s" preserveAspectRatio="none" href="%s"/>' % (
                _f(sx), _f(sy), _f(sw), _f(shh), opts["screen_png"]))
        elif scr:
            o.append('<rect x="%s" y="%s" width="%s" height="%s" rx="0.015" fill="#2a3a5c"/>' % (_f(sx), _f(sy), _f(sw), _f(shh)))
        o.append('</g>')
    elif kind == "medkit":
        o.append('<rect x="-0.20" y="0.02" width="0.40" height="0.28" rx="0.04" fill="#d8352f" stroke="%s" stroke-width="0.022"/>' % INK)
        o.append('<path d="M-0.03,0.09 h0.06 v0.04 h0.04 v0.06 h-0.04 v0.04 h-0.06 v-0.04 h-0.04 v-0.06 h0.04 Z" fill="#fff"/>')
    o.append("</g>")
    return "".join(o)


# ----------------------------------------------------------------------------------------------- build
def _prop_spec(p):
    if not p:
        return None
    if isinstance(p, str):
        return {"type": p}
    return dict(p)


def build(name, pose=None):
    if name not in CAST25:
        raise KeyError(name)
    C = CAST25[name]
    P = dict(pose or {})
    yaw = _clamp(float(P.get("yaw", 0.0)), -1.2, 1.2)
    view, s = view_of(yaw)
    if P.get("view"):                              # forced drawing (the stage passes it with hysteresis)
        view = P["view"]
        s = 0 if view == "front" else (1 if yaw >= 0 else -1)
    expr = P.get("expr", EXPRESSIONS.get(name.split("_")[0], ["neutral"])[0])
    blink = int(P.get("blink", 0))
    wet = bool(C.get("wet"))
    lean = _clamp(float(P.get("lean", 0.0)), -60, 60)
    hroll = _clamp(float(P.get("head_roll", 0.0)), -45, 45)
    hdx, hdy = float(P.get("head_dx", 0.0)), float(P.get("head_dy", 0.0))
    legs = P.get("legs", "stand")
    seated = (legs == "seated") or (isinstance(legs, dict) and legs.get("preset") == "seated")
    uid = P.get("uid", name)
    g = _geom(C, view, s, P)
    hipc = (0.0, C["hip_y"])
    R = lambda p: _rot(p, lean, hipc)
    head = R((hdx, hdy))
    sh = {k: R(v) for k, v in g["sh"].items()}
    layers = {}
    anchors = {"head": head, "hip": hipc}
    # ---------- arms
    for k, c in (("r", 1), ("l", -1)):
        spec = P.get("arm_" + k, "down")
        S = sh[k]
        if isinstance(spec, dict) and "hand" in spec:
            T = tuple(spec["hand"])
            pref = spec.get("pref", (c, 0.4))
        else:
            pre = spec.get("preset", "down") if isinstance(spec, dict) else spec
            T0, pref = _arm_target(pre, c, view, s, C, g["sh"][k], (hdx, hdy))
            T = R(T0) if pre not in ("phone_ear", "guard") else _add(R(g["sh"][k]), _sub(T0, g["sh"][k]))
            if pre in ("phone_ear", "guard"):
                T = _add(head, _sub(T0, (hdx, hdy)))
        E, H = _ik(S, T, C["arm1"], C["arm2"], pref)
        anchors["shoulder_" + k], anchors["elbow_" + k], anchors["hand_" + k] = S, E, H
        flag = C.get("flag") and ((k == "l" and view == "front") or (view != "front" and ((k == "l") == (s > 0))))
        svg = _arm_svg(C, k, S, E, H, view, s, wet, flag)
        layers["arm_" + k] = svg
        ps = _prop_spec(P.get("prop_" + k))
        anchors["prop_tip_" + k] = H
        if ps:
            d = _sub(H, E)
            ang = ps.get("angle", math.degrees(math.atan2(d[1], d[0])))
            gp = _add(H, _mul((d[0] / (_len(d) or 1), d[1] / (_len(d) or 1)), C["hand_r"] * 0.35))
            psvg = prop_svg(ps["type"], gp, ang, ps.get("scale", 1.0), ps)
            layers["prop_" + k] = psvg
            tl = PROP_TIP.get(ps["type"], 0.0) * ps.get("scale", 1.0)
            anchors["prop_tip_" + k] = _add(gp, (tl * math.cos(math.radians(ang)), tl * math.sin(math.radians(ang))))
    # ---------- legs
    lp = legs if isinstance(legs, str) else legs.get("preset", "stand")
    crouch = float(legs.get("crouch", 0.0)) if isinstance(legs, dict) else (0.35 if lp == "crouch" else 0.12 if lp == "lunge" else 0.0)
    tg = _leg_targets(lp, view, s, C, g["hp"], crouch)
    soles = []
    for k, c in (("r", 1), ("l", -1)):
        Hp = g["hp"][k]
        T, pref = tg[k]
        if isinstance(legs, dict) and legs.get("foot_" + k):
            T = tuple(legs["foot_" + k])
        K, A = _ik(Hp, T, C["leg"] * 0.5, C["leg"] * 0.5, pref)
        anchors["knee_" + k], anchors["foot_" + k] = K, A
        layers["leg_" + k] = _leg_svg(C, k, Hp, K, A, view, s, wet, seated)
        soles.append(A[1] + C["boot"][1])
    feet_y = max(soles)
    anchors["feet"] = ((anchors["foot_r"][0] + anchors["foot_l"][0]) / 2.0, feet_y)
    anchors["seat"] = (0.0, C["hip_y"] + 0.18)
    # ---------- torso, pack, head, face, hair (upper body rotates by lean about the hip)
    tr = '<g transform="rotate(%.3f %s %s)">' % (lean, _f(hipc[0]), _f(hipc[1]))
    layers["torso"] = tr + _torso_layer(C, view, s, uid) + "</g>"
    pk = _pack_layer(C, view, s)
    if pk:
        layers["pack"] = tr + pk + "</g>"
    ht = '<g transform="translate(%s %s) rotate(%.3f)">' % (_f(head[0]), _f(head[1]), hroll)
    # head disc: wobbly circle, flat fill, ink thicker on the side away from the key (screen-right by default)
    hp = []
    for i in range(40):
        a = 2 * math.pi * i / 40.0
        r = 0.482 + 0.004 * math.sin(3 * a + C["seed"]) + 0.003 * math.sin(5 * a + 1.3 * C["seed"])
        hp.append((math.cos(a) * r, math.sin(a) * r))
    layers["head"] = ht + '<path d="%s" fill="%s" stroke="%s" stroke-width="%s"/>' % (
        _smooth_closed(hp), C["skin"], INK, _f(LW_HEAD)) + "</g>"
    layers["face"] = ht + _face(C, expr, view, s, blink, P.get("mouth"), P.get("gaze", 0.0), wet) + "</g>"
    hb, hf = _hair(C, view, s, C["seed"])
    layers["hair"] = ht + hf + "</g>"
    if hb:
        layers["hairback"] = ht + hb + "</g>"
    anchors["mouth"] = _add(head, _rot((0.0, 0.21), hroll))
    # ---------- assemble with depths
    zt = depth_table(view, s, seated)
    out = []
    for nm, svg in layers.items():
        z = zt.get(nm)
        if z is None:
            z = 2.3 if nm.startswith("prop") else 0.0
        kind = "face" if nm == "face" else "prop" if nm.startswith("prop") else "body"
        out.append({"name": nm, "svg": svg, "z": z, "kind": kind,
                    "shade": 0.35 if nm == "face" else 1.0,
                    "rim": 0.45 if nm in ("hair", "hairback") else 0.3 if nm == "face" else 1.0})
    # stable order: by depth, ties by a fixed name order
    order = ["pack", "hairback", "arm_r", "arm_l", "prop_r", "prop_l", "leg_r", "leg_l", "torso", "head", "face", "hair"]
    out.sort(key=lambda L: (L["z"], order.index(L["name"]) if L["name"] in order else 99))
    # no two cards coplanar (coplanar transparent cards drop one of the two in Cycles): spread ties by 0.12 gap
    for i in range(1, len(out)):
        if out[i]["z"] <= out[i - 1]["z"] + 0.1:
            out[i]["z"] = out[i - 1]["z"] + 0.12
    xs = [a[0] for a in anchors.values()]
    ys = [a[1] for a in anchors.values()]
    bbox = (min(xs + [-0.75]) - 0.3, min(ys + [-0.75]) - 0.1, max(xs + [0.75]) + 0.3, feet_y + 0.02)
    return {"name": name, "layers": out, "feet": anchors["feet"], "feet_y": feet_y, "seat": anchors["seat"],
            "anchors": anchors, "view": view, "s": s, "bbox": bbox, "yaw": yaw}


def flat_svg(fig):
    return "".join(L["svg"] for L in fig["layers"])


def layer_svg(fig, names):
    names = set(names)
    return "".join(L["svg"] for L in fig["layers"] if L["name"] in names)


def doc(fragment, canvas, ppd, bg=None):
    """full SVG document: canvas (x0, y0, x1, y1) in D (figure coords), ppd pixels per D."""
    x0, y0, x1, y1 = canvas
    W, H = int(round((x1 - x0) * ppd)), int(round((y1 - y0) * ppd))
    b = '<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % (_f(x0), _f(y0), _f(x1 - x0), _f(y1 - y0), bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="%d" height="%d" '
            'viewBox="%s %s %s %s">%s%s</svg>') % (W, H, _f(x0), _f(y0), _f(x1 - x0), _f(y1 - y0), b, fragment), W, H
