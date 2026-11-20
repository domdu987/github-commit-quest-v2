#!/usr/bin/env python3
"""shot.py -- film 17 take s04 round 2 (shots 9-12, narration 14.72-21.61 s), g 445..650 + 6 handle frames each side (439..656).  Blender frame = g + 1.
The mock is about the calipers on an ear: the prisoner (prisoner_b) sits in the measuring chair through all four shots, Bertillon's calipers are pinned on his ear
in Bertillon's visible hand (team-1 s01 setup: ears_svg, hand_svg, pinned tip).
  9 (439-492)  right-front two-shot: the inspector strides in from the door side, stops, looks (shock), bursts out laughing at g 467 (bounce 3 Hz), gendarme_b laughs
  10 (493-539) low two-shot with the calipers on the ear; the inspector points AT the calipers; lips 16.32 s
  11 (540-591) the inspector flicks the caliper bar with a finger; the bar wobbles
  12 (592-656) snap onto the inspector tapping his own (visible, red) ear twice, chest out
    python3 shot.py stills a:b[:s] out [scale] [samples]     python3 shot.py final a:b[:s] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, bf, ez, lerp, clamp, bpy, Vector, cast17, actors
TMP = os.path.join(HERE, "work")
FIRST, LAST, G0, G1 = 439, 656, 445, 651
B9, B10, B11, B12 = 445, 493, 540, 592
RANGES = {9: (FIRST, B10 - 1), 10: (B10, B11 - 1), 11: (B11, B12 - 1), 12: (B12, LAST)}
G_LAUGH = C.g_of(15.46) - 1 if hasattr(C, "g_of") else 466
G_SPEAK0, G_SPEAK1 = 493, 650
def shot_of(g):
    for s, (a, b) in RANGES.items():
        if a <= g <= b: return s
def mix(a, b, u): return tuple(lerp(x, y, u) for x, y in zip(a, b))
def sm(u): u = clamp(u); return u * u * u * (u * (6 * u - 15) + 10)
def sine(u): return ez(u, "sine")
SLIDE = [0.46]

def _calipers_body(k):
    """cast17's calipers with an adjustable sliding jaw (SLIDE[0] = x of the jaw tip line; default 0.46) so the jaws can close."""
    c17 = cast17; dx = SLIDE[0] - 0.46
    g = c17._lin(k, "cb", c17.STEEL["light"], c17.STEEL["base"], c17.STEEL["dark"], 0, -0.05, 0, 0.05)
    o = ['<path d="M-0.12,-0.034 L0.88,-0.034 L0.88,0.034 L-0.12,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (g, k.ink)]
    tk = "".join("M%.3f,0.034 L%.3f,%.3f " % (x, x, 0.034 + (0.034 if i % 5 == 0 else 0.020)) for i, x in enumerate([0.02 + 0.04 * j for j in range(20)]))
    o.append('<path d="%s" stroke="%s" stroke-width="0.008" fill="none"/>' % (tk, k.c(c17.STEEL["deep"])))
    o.append('<path d="M-0.08,-0.018 L0.84,-0.018" stroke="#ffffff" stroke-width="0.008" opacity="0.7" stroke-linecap="round"/>')
    o.append('<path d="M0.80,0.030 L0.88,0.030 L0.88,0.30 L0.835,0.33 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>' % (k.c(c17.STEEL["base"]), k.ink))
    o.append('<path d="M%.3f,-0.050 L%.3f,-0.050 L%.3f,0.30 L%.3f,0.33 L%.3f,0.034 L%.3f,0.034 Z" fill="%s" stroke="%s" stroke-width="0.018" stroke-linejoin="round"/>'
             % (0.40 + dx, 0.52 + dx, 0.52 + dx, 0.485 + dx, 0.46 + dx, 0.40 + dx, k.c(c17.STEEL["light"]), k.ink))
    o.append('<circle cx="%.3f" cy="-0.075" r="0.036" fill="%s" stroke="%s" stroke-width="0.014"/>' % (0.46 + dx, k.c(c17.BRASS["base"]), k.ink))
    return "".join(o)
cast17._calipers_body = _calipers_body
_orig_svg = C.sprites.sprite_svg
def _svg(cast, pose, *a, **kw):
    g = (pose or {}).get("t", None)
    if g is not None and cast == "bertillon": SLIDE[0] = slide_of(int(round(g * 30)))
    return _orig_svg(cast, pose, *a, **kw)
C.sprites.sprite_svg = _svg


def theta_of(yaw): return math.radians(min(abs(yaw), 1.2) * 70.0)

def ear_local(an, g, name, s):
    """target for the caliper jaws (puppet-local D): the viewer-left ear (the near ear in profile).  Shot 1 approaches from below-left."""
    hx, hy = an["head"]
    yw = yaw_of(name, g)
    ex = hx - 0.52 * math.cos(theta_of(yw))
    u = clamp((g - 1) / 13.0) if s == 1 else 1.0
    k = 1.0 - sm(u)
    tap = 0.015 * math.sin(g * 0.8) * (1 if u >= 1 else 0)
    return (ex - 0.5 * k, hy + 0.02 + 1.0 * k + tap)

def ears_svg(pose, fill="#f4d4cb"):
    """cartoon ears (the puppet has none) -> (underlay, overlay) SVG, puppet-local D, y down.  Near ear in profile is drawn OVER the head."""
    yw = pose.get("yaw", 0.0); r = pose.get("head_roll", 0.0); dx = pose.get("head_dx", 0.0); dy = pose.get("head_dy", 0.0)
    ink = "#3a2832"
    c = math.cos(theta_of(yw)); prof = abs(yw) > 0.5
    def ear(x, sx, big):
        rx, ry = (0.19, 0.27) if big else 0.15, (0.25)
        if big: rx, ry = 0.19, 0.27
        else: rx, ry = 0.15, 0.25
        return ('<g transform="translate(%.3f %.3f) scale(%d 1)"><ellipse cx="0" cy="0.02" rx="%.3f" ry="%.3f" fill="%s" stroke="%s" stroke-width="0.035"/>'
                '<path d="M-0.05,-0.13 C0.05,-0.15 0.11,0.02 0.03,0.14" fill="none" stroke="%s" stroke-width="0.03" stroke-linecap="round"/></g>' % (x, 0, sx, rx, ry, fill, ink, ink))
    under = ear(0.52 * c, 1, False) + ear(-0.52 * c, 1, False) if not prof else ear(0.52 * c, 1, False)
    over = ear(-0.52 * c, 1, True) if prof else ""
    wrap = lambda g: '<g transform="rotate(%.2f %.3f %.3f) translate(%.3f %.3f)">%s</g>' % (r, dx, dy, dx, dy, g) if g else ""
    return wrap(under), wrap(over)

def hand_svg(an, side="r", big=1.0):
    """a visible forearm (lighter sleeve), white cuff and skin hand gripping the beam (puppet-local D, from the sprite's own anchors)."""
    ex, ey = an["elbow_" + side]; hx, hy = an["hand_" + side]
    dx, dy = hx - ex, hy - ey; L = math.hypot(dx, dy) or 1.0; ux, uy = dx / L, dy / L
    cx, cy = hx - ux * 0.13, hy - uy * 0.13
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.17" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#46598f" stroke-width="0.125" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#3a2832" stroke-width="0.155" stroke-linecap="butt" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="#fbf3ee" stroke-width="0.115" stroke-linecap="butt" fill="none"/>'
            '<circle cx="%.3f" cy="%.3f" r="%.3f" fill="#f4d4cb" stroke="#3a2832" stroke-width="0.03"/>'
            '<path d="M%.3f,%.3f q0.05,-0.02 0.09,0.03" stroke="#3a2832" stroke-width="0.02" fill="none"/></g>'
            % (ex, ey, hx, hy, ex, ey, hx, hy, cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045,
               cx - ux * 0.045, cy - uy * 0.045, cx + ux * 0.045, cy + uy * 0.045, hx, hy, 0.105 * big, hx - 0.04, hy - 0.01))


def glove_svg(an, side="l"):
    """shot 12: sleeve from the elbow, big white glove (r 0.19 D) and an extended index finger whose tip lands on the ear (puppet-local D)."""
    ex, ey = an["elbow_" + side]; hx, hy = an["hand_" + side]
    dx, dy = hx - ex, hy - ey; L = math.hypot(dx, dy) or 1.0; ux, uy = dx / L, dy / L
    fx, fy = hx + ux * 0.40, hy + uy * 0.40                         # fingertip
    ex, ey = hx - ux * 0.85, hy - uy * 0.85                          # long sleeve rising from the chest to the hand
    ink, glove, sleeve = "#3a2832", "#fbf3ee", "#46598f"
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.19" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.145" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.125" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.085" stroke-linecap="round" fill="none"/>'
            '<circle cx="%.3f" cy="%.3f" r="0.17" fill="%s" stroke="%s" stroke-width="0.035"/>'
            '<path d="M%.3f,%.3f q0.07,-0.03 0.12,0.04" stroke="%s" stroke-width="0.025" fill="none"/></g>'
            % (ex, ey, hx - ux * 0.1, hy - uy * 0.1, ink, ex, ey, hx - ux * 0.1, hy - uy * 0.1, sleeve,
               hx, hy, fx, fy, ink, hx, hy, fx, fy, glove, hx, hy, glove, ink, hx - 0.07 - uy * 0.0, hy - 0.04, ink))

def glove_ear_svg(an, g):
    """shot 12: forearm + big white glove below his own (screen-left) ear with the index finger tip ON the ear rim, tapping 3x g606-640.  Drawn from the head anchor."""
    hx, hy = an["head"]; c = math.cos(theta_of(0.88))
    ex, ey = hx - 0.52 * c, hy + 0.02                                 # ear centre
    tap = 0.05 * abs(math.sin((g - 606) * math.pi / 11.0)) if 606 <= g <= 640 else 0.0
    gx, gy = ex - 0.02, ey + 0.52 - tap                                # glove centre (below the ear, clear of the mouth)
    tx, ty = ex - 0.02, ey + 0.17                                      # fingertip on the lower rim of the ear
    bx, by = gx + 0.25, gy + 1.10                                      # sleeve root (chest)
    ink, glove, sleeve = "#3a2832", "#fbf3ee", "#46598f"
    return ('<g><path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.30" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.24" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.14" stroke-linecap="round" fill="none"/>'
            '<path d="M%.3f,%.3f L%.3f,%.3f" stroke="%s" stroke-width="0.09" stroke-linecap="round" fill="none"/>'
            '<circle cx="%.3f" cy="%.3f" r="0.17" fill="%s" stroke="%s" stroke-width="0.035"/>'
            '<path d="M%.3f,%.3f q0.07,-0.03 0.12,0.04" stroke="%s" stroke-width="0.025" fill="none"/></g>'
            % (bx, by, gx, gy + 0.12, ink, bx, by, gx, gy + 0.12, sleeve, gx, gy, tx, ty, ink, gx, gy, tx, ty, glove,
               gx, gy, glove, ink, gx - 0.07, gy - 0.04, ink))

def slide_of(g):
    return lerp(0.24, 0.50, ez((g - 440) / 30.0))          # jaws close during shot 9, then stay on the ear

def yaw_of(name, g): return 0.55

CH = (0.70, 2.30)
def sc_of(cast): return K.CAST_H[cast] / K.CAST_HD[cast]
SPOT = dict(pris=("prisoner_b", "prisoner_sitting_b", (CH[0], CH[1] - 0.14), "chair"),
            bert=("bertillon", "bertillon_measuring", (0.14, 1.92), None),
            ins=("inspector17", "inspector_pointing_mock", (1.5, 1.5), None),
            gB=("gendarme_b", "gendarme_laughing_b", (2.15, 3.05), None),
            gA=("gendarme_a", "gendarme_laughing_a", (-0.9, 3.0), None))
INS_WALK = [(439, (3.00, 1.40)), (460, (1.30, 2.30)), (466, (1.25, 2.32))]
INS_POS = {10: (1.30, 2.05), 11: (1.30, 1.80), 12: (0.95, 1.30)}

CAMS = {
    9: [(439, (2.05, 0.10, 1.42), (0.75, 2.2, 1.28), "d"), (466, (1.90, 0.28, 1.42), (0.75, 2.2, 1.28), "s"), (474, (1.62, 0.50, 1.40), (0.66, 2.2, 1.30), "d"), (482, (1.60, 0.52, 1.40), (0.66, 2.2, 1.30), "s"), (489, (1.44, 0.68, 1.38), (0.60, 2.2, 1.30), "d"), (492, (1.43, 0.69, 1.38), (0.60, 2.2, 1.30), "d")],
    10: [(493, (1.62, 0.44, 1.02), (0.68, 2.1, 1.35), "d"), (512, (1.66, 0.40, 1.02), (0.68, 2.1, 1.35), "s"), (519, (2.02, 0.10, 0.95), (0.72, 2.1, 1.35), "d"), (528, (2.05, 0.08, 0.95), (0.72, 2.1, 1.35), "s"), (535, (1.78, 0.30, 1.0), (0.64, 2.1, 1.35), "d"), (539, (1.76, 0.32, 1.0), (0.64, 2.1, 1.35), "d")],
    11: [(540, (1.62, 0.72, 1.40), (0.68, 2.0, 1.30), "d"), (566, (1.66, 0.68, 1.40), (0.68, 2.0, 1.30), "s"), (574, (2.15, 0.15, 1.42), (0.55, 2.0, 1.30), "d"), (591, (2.25, 0.08, 1.42), (0.55, 2.0, 1.30), "d")],
    12: [(592, (1.95, 0.30, 1.48), (0.80, 1.60, 1.38), "d"), (604, (1.92, 0.34, 1.48), (0.80, 1.60, 1.38), "s"), (611, (1.42, 0.52, 1.46), (0.90, 1.55, 1.38), "d"), (632, (1.38, 0.55, 1.46), (0.92, 1.55, 1.38), "s"),
         (639, (1.62, 0.64, 1.46), (1.00, 1.55, 1.38), "d"), (656, (1.66, 0.66, 1.46), (1.02, 1.55, 1.38), "d")],
}
def cam_of(g):
    wps = CAMS[shot_of(g)]; i = 0
    while i < len(wps) - 2 and g >= wps[i + 1][0]: i += 1
    a, b = wps[i], wps[i + 1]; u = (g - a[0]) / float(b[0] - a[0])
    e = sm(u) if a[3] == "s" else (0.35 * sine(u) + 0.65 * clamp(u) if 0 <= u <= 1 else u)
    loc = mix(a[1], b[1], e); look = mix(a[2], b[2], e)
    am = 0.08
    return (loc[0] + am * math.sin(2 * math.pi * g / 37.0), loc[1] + 0.5 * am * math.sin(2 * math.pi * g / 29.0), loc[2] + 0.4 * am * math.sin(2 * math.pi * g / 23.0)), look

def lerp_path(pts, g):
    if g <= pts[0][0]: return pts[0][1]
    for (g0, p0), (g1, p1) in zip(pts, pts[1:]):
        if g <= g1: u = (g - g0) / float(g1 - g0); return (lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u))
    return pts[-1][1]
def bounce(g, amp=0.06 * 1.7, hz=3.0, ph=0.0): return amp * abs(math.sin(math.pi * hz * g / 30.0 + ph))

def story(name, **kw):
    cast, p = cast17.STORY17[name]; p = dict(p); p.update(kw); p["seat17"] = None; return p
def rim(p, cast):
    c = K.RIM_FOR.get(cast)
    if c: p["rim"] = c; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
    return p
def speak(p, g):
    return cast17.speak(p, g, 0.85 + 0.15 * math.sin(g * 0.37)) if G_SPEAK0 <= g <= G_SPEAK1 else cast17.silent(p)

def pose_pris(g):
    t = g / 30.0; p = story("prisoner_sitting_b")
    p.update(yaw=yaw_of("pris", g), pitch=0.0, expr="unimpressed", mouth="flat", gaze=(-0.95, 0.05), head_roll=1.5 * math.sin(t * 1.9), blink=cast17.blink_at(g, 83, 11))
    p["squash"] = (1.0 + 0.008 * math.sin(t * 2.4), 1.0 - 0.008 * math.sin(t * 2.4))
    return cast17.silent(p)
def pose_bert(g):
    t = g / 30.0
    p = story("bertillon_measuring"); sway = math.sin(t * 2.1)
    p.update(lean=4 + 1.5 * sway, pitch=0.22, yaw=0.62, gaze=(1.0, 0.25), blink=cast17.blink_at(g, 90, 30), t=g / 30.0)
    return cast17.silent(p)
def pose_gend(name, g, ph):
    t = g / 30.0; lau = g >= G_LAUGH + 4 + ph
    p = story(("gendarme_laughing_" if lau else "gendarme_standing_") + ("b" if name == "gB" else "a"))
    p.update(blink=cast17.blink_at(g, 79 + ph, 9))
    if lau: p["lean"] = -6 + 3 * math.sin(g * 0.45 + ph)
    p["t"] = t
    return cast17.silent(p) if not lau else p
def pos_gend(name, g):
    lau = g >= G_LAUGH + 4 + (0 if name == "gB" else 4)
    return bounce(g, ph=0.8 if name == "gA" else 2.0) if lau else 0.0

def pose_ins(g):
    """(pose, xy, lift) -- hands pinned later."""
    s = shot_of(g); t = g / 30.0
    if s == 9:
        xy = lerp_path(INS_WALK, g)
        if g < 459:
            base = story("inspector_arms_crossed")
            p = cast17.cycle("inspector17", (g - 439) / 30.0 * 1.9, "march", 1, base=dict(base, arm_r="down", arm_l="down"))
            p.update(yaw=-0.5, expr="smug", pitch=-0.2)
            return cast17.silent(p), xy, 0.0
        if g < G_LAUGH:
            p = story("inspector_pointing_mock", expr="surprised", mouth="flat", yaw=-0.45)
            p["arm_r"] = dict(p["arm_r"], hand=(1.0, 0.0)); p["lean"] = 2 + 2 * math.sin(g * 0.3); p["head_roll"] = 6
            return cast17.silent(p), xy, 0.0
        u = sm((g - G_LAUGH) / 5.0)
        p = story("inspector_laughing"); p["lean"] = -8 + 3 * math.sin(g * 0.5); p["t"] = t; p["yaw"] = -0.3
        b = abs(math.sin(math.pi * 3.0 * g / 30.0)); p["squash"] = (1.0 + 0.03 * b, 1.0 - 0.03 * b)
        return p, xy, bounce(g) * u
    xy = INS_POS[s]
    p = story("inspector_pointing_mock", expr="smug"); p["yaw"] = -0.4
    if s == 10:
        p["head_roll"] = 6 + 3 * math.sin(g * 0.23); p["lean"] = -3 + 2 * math.sin(g * 0.31); p["mirror"] = True; p["yaw"] = 0.4
        p["arm_r"] = dict(p["arm_r"], hand=(1.30 + 0.05 * math.sin(g * 0.3), 0.30), stretch=1.3)
    if s == 11: p["head_roll"] = -4 + 3 * math.sin(g * 0.2); p["lean"] = 3 + 2 * math.sin(g * 0.33); p["yaw"] = 0.4; p["mirror"] = True
    if s == 12:
        k = clamp((g - B12) / 14.0)
        p.update(yaw=0.88, expr="smug", pitch=-0.35, head_roll=-3 + 2 * math.sin(g * 0.25), lean=-6 - 3 * sm(k) + 1.2 * math.sin(g * 0.3), arm_r="behind")
        sq = 1.0 + 0.09 * sm(k); p["squash"] = (sq, 1.0 - 0.01 * sm(k))
    return speak(p, g), xy, 0.0

def ins_ear_local(an, g):
    hx, hy = an["head"]; c = math.cos(theta_of(0.88))
    tap = 0.045 * abs(math.sin((g - 606) * math.pi / 11.0)) if 606 <= g <= 640 else 0.0     # 3 taps g606-640 (period 11 f), then hold
    return (hx - 0.52 * c + 0.0, hy + 0.62 - tap)

class Take(C.Take):
    def __init__(self, quality="draft"):
        C.Take.__init__(self, "measure_chair", quality, fg=True)
        self.q = quality
        sd = os.path.join(TMP, "sprites_" + quality)
        self.acts = {n: self.make_actor(n, v[0], sd) for n, v in SPOT.items()}
        for n, fill in (("pris", "#f4d4cb"), ("ins", "#e9857a")):
            a = self.acts[n]
            a.jobs = (lambda orig, fl: (lambda px, frames=None, overlay=None: [dict(j, underlay=ears_svg(j["pose"], fl)[0], overlay=ears_svg(j["pose"], fl)[1] + (j.get("overlay") or "")) for j in orig(px, frames, overlay)]))(a.jobs, fill)
        for o in bpy.data.objects:
            if any(m and m.name.startswith("beam_fx") for m in (getattr(o.data, "materials", None) or [])): o.hide_render = True
        self.ear = {}; self.info = {}
        self.cut_table_calipers()

    def cut_table_calipers(self):
        """delete the steel calipers (and their ink hull) lying on the small table at ~(1.9, 1.55): loose crossed rods that read as stray props."""
        import bmesh
        box = lambda c: 1.5 < c.x < 2.4 and 1.3 < c.y < 1.85 and 0.8 < c.z < 1.12
        n = 0; lo = Vector((9, 9, 9)); hi = Vector((-9, -9, -9)); steel = []
        for ob in bpy.data.objects:
            if ob.type != "MESH" or not ob.data.materials: continue
            mw = ob.matrix_world
            for p in ob.data.polygons:
                m = ob.data.materials[p.material_index]
                if m and m.name == "steel" and box(mw @ p.center):
                    steel.append((ob, p.index))
                    for vi in p.vertices:
                        v = mw @ ob.data.vertices[vi].co
                        lo = Vector((min(lo.x, v.x), min(lo.y, v.y), min(lo.z, v.z))); hi = Vector((max(hi.x, v.x), max(hi.y, v.y), max(hi.z, v.z)))
        for ob in bpy.data.objects:
            if ob.type != "MESH" or not ob.data.materials: continue
            mw = ob.matrix_world; bm = bmesh.new(); bm.from_mesh(ob.data); dead = []
            for f in bm.faces:
                m = ob.data.materials[f.material_index]
                if not m or m.name not in ("steel", "ink"): continue
                c = mw @ f.calc_center_median()
                if all(lo[i] - 0.03 < c[i] < hi[i] + 0.03 for i in range(3)) and (m.name == "steel" or True):
                    if m.name == "steel" and not box(c): continue
                    dead.append(f)
            if dead:
                bmesh.ops.delete(bm, geom=dead, context="FACES"); n += len(dead); bm.to_mesh(ob.data)
            bm.free()
        for ob in bpy.data.objects:                              # the floating crossed rods are thin cream faces hovering at z ~1.02 above the table
            if ob.type != "MESH" or not ob.data.materials: continue
            mw = ob.matrix_world; bm = bmesh.new(); bm.from_mesh(ob.data)
            dead = [f for f in bm.faces if ob.data.materials[f.material_index] and ob.data.materials[f.material_index].name == "cream"
                    and 1.4 < (mw @ f.calc_center_median()).x < 2.0 and 1.5 < (mw @ f.calc_center_median()).y < 1.95 and 0.9 < (mw @ f.calc_center_median()).z < 1.2]
            if dead: bmesh.ops.delete(bm, geom=dead, context="FACES"); n += len(dead); bm.to_mesh(ob.data)
            bm.free()
        print("cut_table_calipers: removed", n, "faces", tuple(round(v, 2) for v in lo), tuple(round(v, 2) for v in hi), flush=True)

    def ppd(self, s): return {9: 256, 10: 384, 11: 384, 12: 512}[s] * (1 if self.q == "final" else 0.5)

    def sprites(self, n, a, frames, overlay=None):
        for s in sorted(set(shot_of(f - 1) for f in frames)):
            fr = [f for f in frames if shot_of(f - 1) == s]
            p = int(self.ppd(s)); p -= p % 16
            for f, r in zip(fr, a.render_sprites(p, frames=fr, overlay=overlay)): self.anch[(a.name, f)] = r["anchors"]

    def pose(self, gs):
        gs = list(gs); cam = self.cam
        for g in sorted(set(gs) | set(x for y in gs for x in (y - 1, y + 1))):
            if FIRST <= g <= LAST: self.key_cam(bf(g), *cam_of(g))
        for g in gs:
            f = bf(g); s = shot_of(g)
            for n, a in self.acts.items():
                on = n in ("pris", "bert", "ins") or (n == "gB" and s == 9) or (n == "gA" and s == 9)
                C.vis(a, f, on)
            self.acts["pris"].place(f, (SPOT["pris"][2][0], SPOT["pris"][2][1], K.HEAD_Z["chair"] - sc_of("prisoner_b") * C.sprites.feet_of("prisoner_b", pose_pris(g))[1]), scale=sc_of("prisoner_b"))
            self.acts["bert"].place(f, (SPOT["bert"][2][0], SPOT["bert"][2][1], 0.10), scale=sc_of("bertillon"))
            p, xy, lift = pose_ins(g); self.acts["ins"].place(f, (xy[0], xy[1], lift), scale=sc_of("inspector17"))
            self.acts["gB"].place(f, (SPOT["gB"][2][0], SPOT["gB"][2][1], pos_gend("gB", g)), scale=sc_of("gendarme_b"))
            self.acts["gA"].place(f, (SPOT["gA"][2][0], SPOT["gA"][2][1], pos_gend("gA", g)), scale=sc_of("gendarme_a"))
            K.set_flicker(1.0, frame=f); K.set_dust(0.5, frame=f); K.set_smoke(1.0, frame=f); K.set_pendulum(frame=f)
        # pass 1: sitter, gendarmes
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.acts["pris"].pose(f, pose_pris(g), camera=cam)
            if shot_of(g) == 9:
                self.acts["gB"].pose(f, pose_gend("gB", g, 0), camera=cam); self.acts["gA"].pose(f, pose_gend("gA", g, 4), camera=cam)
        self.sprites("pris", self.acts["pris"], [bf(g) for g in gs])
        for n in ("gB", "gA"):
            fr = [bf(g) for g in gs if shot_of(g) == 9]
            if fr: self.sprites(n, self.acts[n], fr)
        # Bertillon: jaws pinned on the prisoner's viewer-left ear
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            an = self.anch[("pris", f)]; el = pris_ear_local(an, g)
            w = actors.local_to_world(self.acts["pris"], el, f, camera=cam); self.ear[g] = tuple(w)
            wob = self.wobble(g)
            p, info = self.acts["bert"].pose(f, pose_bert(g), hands={"r": {"tip": w, "prop": "calipers", "angle": -4 + wob, "prop_scale": 1.15, "stretch": 1.15}}, camera=cam)
            self.info[(g, "bert")] = round(info.get("r", {}).get("error", -1), 3)
        fr = [bf(g) for g in gs]
        self.sprites("bert", self.acts["bert"], fr)
        self.sprites("bert", self.acts["bert"], fr, overlay=lambda f, pose: hand_svg(self.anch[("bert", f)]))
        # inspector: pinned hands (needs Bertillon's anchors: the caliper bar)
        for g in gs:
            f = bf(g); s = shot_of(g); self.scene.frame_set(f)
            p, xy, lift = pose_ins(g); p = rim(dict(p), "inspector17"); hands = None
            if s == 11:
                ban = self.anch[("bert", f)]
                hx, hy = ban["hand_r"]; tx, ty = ban["prop_tip_r"]
                mid = actors.local_to_world(self.acts["bert"], ((hx + tx) * 0.5, (hy + ty) * 0.5), f, camera=cam)
                self.bar = tuple(mid)
                if True:
                    k = clamp((g - 548) / 10.0); out = (Vector(cam_of(g)[0]) - Vector(mid)).normalized() * (0.30 * (1 - sm(min(1.0, k))) + 0.02)
                    hands = {"r": {"hand": tuple(Vector(mid) + out), "stretch": 1.2}}
            if s == 12:
                an0 = self.anch.get(("ins", f))
            _, ii = self.acts["ins"].pose(f, p, hands=hands, camera=cam); self.info[(g, "ins")] = round(ii.get("r", {}).get("error", -1), 3) if ii else None
        fr = [bf(g) for g in gs]
        self.sprites("ins", self.acts["ins"], fr)
        for g in gs:
            if shot_of(g) == 12:
                f = bf(g); self.scene.frame_set(f); p, xy, lift = pose_ins(g); p = rim(dict(p), "inspector17")
                el = ins_ear_local(self.anch[("ins", f)], g)
                side = os.environ.get("EARARM", "l"); other = "r" if side == "l" else "l"
                pp = dict(p); pp["arm_" + other] = "behind"; pp["arm_" + side] = "behind"
                self.acts["ins"].pose(f, pp, camera=cam)
        fr12 = [bf(g) for g in gs if shot_of(g) in (11, 12)]
        if fr12:
            self.sprites("ins", self.acts["ins"], fr12)
            self.sprites("ins", self.acts["ins"], fr12, overlay=lambda f, pose: (glove_ear_svg(self.anch[("ins", f)], f - 1) if shot_of(f - 1) == 12 else hand_svg(self.anch[("ins", f)], "r")))

    def wobble(self, g):
        if 558 <= g <= 567: return 9.0 * math.sin((g - 558) * 1.7) * (1 - (g - 558) / 10.0)
        return 0.0

    def report(self, g):
        f = bf(g); self.scene.frame_set(f); out = dict(g=g, shot=shot_of(g), err=self.info.get((g, "bert")), ins_err=self.info.get((g, "ins")), ear=self.info.get((g, "ear")))
        heads = {}
        for n, a in self.acts.items():
            if a.card.hide_render or (a.name, f) not in self.anch: continue
            hx, hy = self.anch[(a.name, f)]["head"]; w0 = actors.local_to_world(a, (hx, hy), f, camera=self.cam); c = K.project(self.cam, tuple(w0))
            heads[n] = (round(c[0]), round(c[1]))
        out["heads"] = heads; return out

def pris_ear_local(an, g):
    hx, hy = an["head"]; return (hx - 0.52 * math.cos(theta_of(yaw_of("pris", g))), hy + 0.02 + 0.015 * math.sin(g * 0.8))

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        os.makedirs(out, exist_ok=True)
        T = Take("draft" if scale < 1 else "final"); T.pose(gs)
        for g in gs:
            print(json.dumps(T.report(g)), flush=True)
            st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale); os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        out = os.path.join(HERE, "raw_%d" % int(scale * 720)); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        T = Take("draft" if scale < 1 else "final")
        for i in range(0, len(todo), 12):
            ch = todo[i:i + 12]; T.pose(ch)
            for g in ch:
                st = T.render([bf(g)], out, scale, samples)[0]; K.grade(st["path"], scale=scale)
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); json.dump(T.report(g), open(os.path.join(out, "g_%04d.json" % g), "w"))
                print("g", g, round(st["wall"], 1), flush=True)
