#!/usr/bin/env python3
"""shot.py -- film 6b take s17: shots 17-21 (g 964..1237, handles g 958..963 and 1238..1243), afternoon of the inspector.

    shot 17  g  958..1028  market AFTERNOON, low medium: the hooded stranger walks into the square (long shadows to screen-right,
                           the pillory behind him), stops, turns to us, throws the hood back (hood 1 -> 0, g 1007..1016) and on a
                           blink (g 1016) becomes inspector_royal: tabard + chain, on "พระราชา" (g 1017) with a snap push to a CU.
    shot 18  g 1029..1082  bakery AFTERNOON, over the hooded customer's shoulder: henry counts on his fingers (1..10, both hands),
                           punch-in (g 1062) on henry + the basket with its Thai tag "12 ก้อน" (on "หนึ่งโหล" g 1069), smug point.
    shot 19  g 1083..1131  market, the big balance: inspector_royal tips the basket, 12 loaves fly one by one onto the bread pan
                           (set_loaves 0 -> 12); the beam rises from -11 but stops at -7 (short).
    shot 20  g 1132..1163  ECU of the balance needle on a blue enamel dial "ผ่าน | ขาด!": the needle stays on the red side; on
                           "ขาด!" (g 1157) the label flares and the camera snaps in (hard cut in, drum).
    shot 21  g 1164..1243  market: two guards drag pale sweating henry (heels sliding) toward the pillory; g 1164..1196 tracking
                           MCU on henry, g 1197.. low wide with the pillory sign "ห้ามขายขาดน้ำหนัก!", jeering townsfolk.
Mouths: no quoted line in this take: every mouth is the static mouth of its expression.
NO depth of field anywhere (client rule).  Blender frame of film frame g = g - 900 (one shot per process).

    python3 shot.py stills <shot> a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <shot> a:b[:step] [scale] [samples]
"""
import math, os, sys, json, copy, base64

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
sys.path.insert(0, FILM6)
import common as C                                       # noqa: E402  (paths, cast6 first, bpy, bakery, stage)
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6, sprites = C.B, C.actors, C.camrig, C.cast6, C.sprites
lerp, clamp, ez = C.lerp, C.clamp, C.ez
TMP = os.path.join(HERE, "work")
PROJ = C.PROJ
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")

RANGES = {17: (958, 1028), 18: (1029, 1082), 19: (1083, 1131), 20: (1132, 1163), 21: (1164, 1243)}
G0, G1, H = 964, 1238, 6
INK = "#2b1a2e"


def bf(g):
    return int(g) - 900


def g_of(t):
    return int(round((t + 0.10) * 30))


def ramp(g, a, b, kind="sine"):
    return ez((g - a) / float(b - a), kind) if b > a else float(g >= a)


def V(*a):
    return Vector(a)


def story(name):
    c, p = cast6.STORY6[name]
    return c, copy.deepcopy(p)


# ----------------------------------------------------------------------------- Thai signs (SVG, Kanit embedded)
_FONT_CSS = None


def font_css():
    global _FONT_CSS
    if _FONT_CSS is None:
        b = base64.b64encode(open(FONT, "rb").read()).decode()
        _FONT_CSS = "<style>@font-face{font-family:'KanitB';src:url(data:font/ttf;base64,%s) format('truetype');}</style>" % b
    return _FONT_CSS


def text_el(x, y, s, size, fill, stroke=INK, sw=None, anchor="middle", extra=""):
    sw = size * 0.16 if sw is None else sw
    return ('<text x="%.4f" y="%.4f" font-family="KanitB" font-size="%.4f" text-anchor="%s" fill="%s" stroke="%s" '
            'stroke-width="%.4f" stroke-linejoin="round" paint-order="stroke" %s>%s</text>' % (x, y, size, anchor, fill, stroke, sw, extra, s))


def board_svg(w, h, text, size, fill="#b3261e", bg="#f1dfb4", wood="#8a5a2e", ty=None):
    """a hanging wooden board with a parchment face and bold Thai text, drawn around (0, 0) (centre), D units."""
    ty = size * 0.36 if ty is None else ty
    s = font_css()
    s += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="%.3f" fill="%s" stroke="%s" stroke-width="0.045"/>' % (
        -w / 2, -h / 2, w, h, 0.06, wood, INK)
    m = 0.075
    s += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" rx="0.03" fill="%s" stroke="%s" stroke-width="0.02"/>' % (
        -w / 2 + m, -h / 2 + m, w - 2 * m, h - 2 * m, bg, INK)
    for sx in (-1, 1):
        for sy in (-1, 1):
            s += '<circle cx="%.3f" cy="%.3f" r="0.022" fill="#4a4048" stroke="%s" stroke-width="0.01"/>' % (sx * (w / 2 - m / 2), sy * (h / 2 - m / 2), INK)
    s += text_el(0, ty, text, size, fill)
    return s


def tag_svg(text, size=0.16):
    """a small parchment price tag with a string loop (the basket tag)."""
    w, h = 0.62, 0.30
    s = font_css()
    s += '<path d="M0,-0.30 L-0.12,%.3f M0,-0.30 L0.12,%.3f" stroke="%s" stroke-width="0.018" fill="none"/>' % (-h / 2, -h / 2, "#5a3a22")
    s += '<path d="M%.3f,%.3f L%.3f,%.3f L%.3f,%.3f L%.3f,%.3f Z" fill="#f6e7c1" stroke="%s" stroke-width="0.03" stroke-linejoin="round"/>' % (
        -w / 2, -h / 2, w / 2, -h / 2, w / 2, h / 2, -w / 2, h / 2, INK)
    s += text_el(0, size * 0.36, text, size, "#c0281e")
    return s


def dial_svg(flare=0.0):
    """the blue enamel dial behind the balance needle: origin = needle pivot, arc radius 1.0 above it (y up = negative).
    left half (screen-left) green 'ผ่าน', right half red 'ขาด!'; flare 0..1 lights the red label up."""
    R = 1.0
    s = font_css()
    s += ('<path d="M-1.18,-0.10 L-1.18,-0.95 A1.25,1.25 0 0 1 1.18,-0.95 L1.18,-0.10 Z" fill="#1d3f7a" stroke="%s" stroke-width="0.05"/>' % INK)
    s += '<path d="M-1.10,-0.16 L-1.10,-0.93 A1.17,1.17 0 0 1 1.10,-0.93 L1.10,-0.16 Z" fill="none" stroke="#e7c35a" stroke-width="0.025"/>'

    def arc(a0, a1, r, col, w):
        p0 = (r * math.sin(math.radians(a0)), -r * math.cos(math.radians(a0)))
        p1 = (r * math.sin(math.radians(a1)), -r * math.cos(math.radians(a1)))
        return '<path d="M%.4f,%.4f A%.3f,%.3f 0 0 1 %.4f,%.4f" fill="none" stroke="%s" stroke-width="%.3f"/>' % (p0[0], p0[1], r, r, p1[0], p1[1], col, w)
    s += arc(-40, -1.5, 0.88, "#3fbf5a", 0.13)
    s += arc(1.5, 40, 0.88, "#e0362a" if flare < 0.5 else "#ff5a3c", 0.13)
    for k in range(-8, 9):
        a = math.radians(k * 5.0)
        r0, r1 = (0.74, 0.97) if k % 4 == 0 else (0.80, 0.95)
        s += '<line x1="%.4f" y1="%.4f" x2="%.4f" y2="%.4f" stroke="#f3e2a8" stroke-width="%.3f"/>' % (
            r0 * math.sin(a), -r0 * math.cos(a), r1 * math.sin(a), -r1 * math.cos(a), 0.035 if k % 4 == 0 else 0.018)
    s += '<line x1="0" y1="-0.70" x2="0" y2="-1.02" stroke="#ffffff" stroke-width="0.05"/>'
    if flare > 0:
        for k in range(10):
            a = math.radians(14 + k * 7.5)
            s += '<line x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" stroke="#ffe066" stroke-width="0.04" stroke-linecap="round"/>' % (
                0.55 + 0.30 * math.cos(a), -0.45 - 0.30 * math.sin(a) + 0.05, 0.55 + 0.52 * math.cos(a), -0.45 - 0.52 * math.sin(a) + 0.05)
    s += text_el(-0.52, -0.38, "ผ่าน", 0.25, "#8ef09c")
    s += text_el(0.55, -0.36, "ขาด!", 0.34 if flare < 0.5 else 0.40, "#ff4b3a" if flare < 0.5 else "#fff04a",
                 sw=0.07)
    return s


def needle_svg():
    s = '<path d="M-0.045,0.10 L0.045,0.10 L0.012,-0.98 L0,-1.06 L-0.012,-0.98 Z" fill="#c8202a" stroke="%s" stroke-width="0.02"/>' % INK
    s += '<circle cx="0" cy="0" r="0.10" fill="#e7c35a" stroke="%s" stroke-width="0.025"/><circle cx="0" cy="0" r="0.035" fill="%s"/>' % (INK, INK)
    return s


# ----------------------------------------------------------------------------- helpers
def key_hidden(objs, f, hidden):
    for ob in objs:
        ob.hide_render = bool(hidden)
        ob.keyframe_insert("hide_render", frame=f)
        fc = C._fcurve(ob, "hide_render")
        if fc is not None:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def anchor_world(actor, pose, name, f, cam):
    """world point of a figure anchor (hand_r, basket_lip ...) of `pose` on the card at Blender frame f."""
    fig = sprites.puppet.figure(actor.cast, pose, "aw")
    an = fig["anchors"][name]
    feet = sprites.feet_of(actor.cast, pose)
    return actors.local_to_world(actor, an, f, feet, cam)


def legs_of(cast, phase, mode="walk"):
    return cast6.cycle(cast, phase, mode)["legs"]


class Shot(C.Take):
    def __init__(self, loc, preset, quality, lens=24.0):
        C.Take.__init__(self, loc, preset, quality=quality, lens=lens, name="cam_s17")
        self.sd = os.path.join(TMP, "sprites")
        self.pdir = os.path.join(TMP, "props")
        self.ppd = {}

    def add(self, key, cast, ppd, canvas=None):
        a = C.make_actor(key, cast, self.sd, canvas)
        self.actors[key] = a
        self.ppd[key] = ppd
        return a

    def kcam(self, f, loc, look, lens=None):
        self.key_cam(f, loc, look, lens=lens)

    def finish_sprites(self, fr, keys=None):
        keys = keys or list(self.actors)
        for k in keys:
            a = self.actors[k]
            frs = [f for f in fr if f in a.poses]
            if frs:
                self.sprites_for([(a, self.ppd[k])], frs)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

    def report(self, shot, g):
        f = bf(g)
        self.scene.frame_set(f)
        out = dict(shot=shot, g=g, heads=C.head_report(self, f))
        out.update(self.extra_report(g))
        return out

    def extra_report(self, g):
        return {}


# ============================================================================= shot 17: the hooded stranger, hood drop
S17_WALK = (958, 1000)
S17_X = (-3.55, -1.75)
S17_Y = 1.2
S17_HOOD = (1007, 1016)
S17_SWAP = 1017                      # "พระราชา" g 1017


class Shot17(Shot):
    def __init__(self, quality="preview"):
        Shot.__init__(self, "market", "AFTERNOON", quality, lens=24.0)
        self.add("ins", "inspector", 320)
        self.add("roy", "inspector_royal", 448)
        B.set_big_scale(-7.0); B.set_loaves(12)

    def xy(self, g):
        u = clamp((g - S17_WALK[0]) / float(S17_WALK[1] - S17_WALK[0]))
        if g > S17_WALK[1] - 6:          # ease into the stop
            u = 1.0 - (1.0 - u) * 0.6 if u < 1 else 1.0
        return (lerp(S17_X[0], S17_X[1], u), S17_Y)

    def camera(self, g):
        x, y = self.xy(g)
        if g < S17_SWAP:
            d = lerp(5.4, 3.0, ramp(g, 958, 1016, "sine"))
            hz = lerp(2.15, 2.75, ramp(g, 958, 1016))
            cz = lerp(1.15, 1.75, ramp(g, 958, 1016))
            lead = lerp(0.9, 0.0, ramp(g, 958, 1004))
        else:
            d = lerp(3.0, 2.05, ramp(g, S17_SWAP, S17_SWAP + 4, "sine")) - 0.15 * ramp(g, S17_SWAP + 4, 1034)
            hz = 2.95
            cz = lerp(1.75, 2.15, ramp(g, S17_SWAP, S17_SWAP + 4))
            lead = 0.0
        P = V(x + lead * 0.6, y, hz)
        dirv = V(0.22, -1.0, 0.0).normalized()
        loc = V(x + lead * 0.6, y, 0) + dirv * d
        loc.z = cz
        return loc, P

    def pose(self, shot, gs):
        ins, roy = self.actors["ins"], self.actors["roy"]
        for g in gs:
            f = bf(g)
            loc, look = self.camera(g)
            self.kcam(f, loc, look)
            x, y = self.xy(g)
            C.place(ins, f, (x, y), 0.0)
            C.place(roy, f, (x, y), 0.0)
            key_hidden(ins.objects(), f, g >= S17_SWAP)
            key_hidden(roy.objects(), f, g < S17_SWAP)
            self.key_set(f, oven=1.0)
            B.set_big_scale(-7.0, frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            if g < S17_SWAP:
                if g < S17_WALK[1]:
                    p = cast6.cycle("inspector", (g - 958) / 24.0, "walk", base=dict(expr="neutral", hood=1.0, yaw=0.35, pitch=0.1))
                    p["t"] = g / 30.0
                else:
                    u = ramp(g, 1000, 1006)
                    ua = ramp(g, 1001, 1008)
                    p = dict(yaw=lerp(0.35, 0.0, u), pitch=lerp(0.1, -0.2, u), expr="neutral" if g < 1008 else "determined", hood=1.0,
                             legs="stand" if g < 1004 else "wide", t=g / 30.0,
                             arm_r=dict(hand=(lerp(0.22, 0.40, ua), lerp(0.95, -0.55, ua)), bend=lerp(0.6, -1.0, ua), stretch=1.3),
                             arm_l=dict(hand=(lerp(-0.20, -0.40, ua), lerp(0.98, -0.52, ua)), bend=lerp(0.6, -1.0, ua), stretch=1.3))
                    p["hood"] = 1.0 - ramp(g, S17_HOOD[0], S17_HOOD[1])
                    if g == S17_HOOD[1] - 1:
                        p["blink"] = 1
                    elif g == S17_HOOD[1]:
                        p["blink"] = 2
                ins.pose(f, p, camera=self.cam)
                roy.pose(f, story("inspector_reveal")[1], camera=self.cam)
            else:
                _, p = story("inspector_reveal")
                u = ramp(g, S17_SWAP, S17_SWAP + 6)
                p.update(t=g / 30.0, pitch=-0.35, head_roll=lerp(-4, 2, u) + 1.0 * math.sin(g * 0.2),
                         blink=1 if g == S17_SWAP else 0, gaze=(0.0, 0.1))
                p["arm_r"] = dict(hand=(lerp(0.40, 0.62, u), lerp(-0.55, -0.22, u)), shape="open", bend=-0.6, stretch=1.2)
                roy.pose(f, p, camera=self.cam)
                ins.pose(f, dict(hood=0.0), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(ins, 320), (roy, 448)], fr)


# ============================================================================= shot 18: henry counts a dozen
S18_PUNCH = 1062
HENRY_B = (1.15, 1.6)
INS_B = (-0.45, -1.05)
BASKET_B = V(0.35, 0.72, 1.25)
BASKET_SC = 1.35


class Shot18(Shot):
    def __init__(self, quality="preview"):
        Shot.__init__(self, "bakery", "AFTERNOON", quality, lens=24.0)
        self.add("henry", "henry", 384)
        self.add("ins", "inspector", 256)
        svg, an = cast6.basket_svg("bk12", loaves=12)
        box = (-0.56, -0.06, 0.56, 0.72)
        self.basket = C.PropCard("basket", C.svg_pngs([(svg, box, 512)], self.pdir), box, scale=BASKET_SC, shadow=True)
        tb = (-0.36, -0.34, 0.36, 0.20)
        self.tag = C.PropCard("tag", C.svg_pngs([(tag_svg("12 ก้อน"), tb, 640)], self.pdir), tb, scale=BASKET_SC, shadow=False)
        loc, _ = self.camera(1029)
        self.basket.put(BASKET_B + V(0, 0, 0.66 * BASKET_SC), face=loc)
        self.tag.put(BASKET_B + V(0.05, -0.12, 0.30 * BASKET_SC), face=loc)

    def camera(self, g):
        if g < S18_PUNCH:
            u = ramp(g, 1023, S18_PUNCH, "sine")
            loc = V(lerp(0.70, 0.80, u), lerp(-2.10, -1.80, u), 2.55)
            look = V(lerp(0.85, 1.0, u), 1.6, lerp(2.30, 2.30, u))
        else:
            u = ramp(g, S18_PUNCH, 1089, "sine")
            loc = V(lerp(0.20, 0.32, u), lerp(-0.85, -0.65, u), lerp(2.05, 2.10, u))
            look = V(0.70, 1.6, lerp(2.05, 2.10, u))
        return loc, look

    def count(self, g):
        if g < 1031:
            return 0
        return min(10, 1 + (g - 1031) // 3)

    def pose(self, shot, gs):
        he, ins = self.actors["henry"], self.actors["ins"]
        for g in gs:
            f = bf(g)
            loc, look = self.camera(g)
            self.kcam(f, loc, look)
            C.place(he, f, HENRY_B, 0.0)
            C.place(ins, f, INS_B, 0.0)
            self.key_set(f, steam=0.15, oven=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            n = self.count(g)
            beat = 0.0 if n == 0 else max(0.0, 1.0 - ((g - 1031) % 3) / 2.0)
            if g < 1061:
                p = dict(yaw=-0.30, pitch=0.30 + 0.10 * beat, expr="unimpressed", head_roll=-4 + 2 * math.sin(g * 0.3), gaze=(-0.3, 0.7),
                         arm_r=dict(hand=(0.70, -0.08 - 0.05 * beat * (n <= 5)), bend=-0.8, stretch=1.3), fingers_r=min(5, n),
                         arm_l=dict(hand=(-0.70, -0.06 - 0.05 * beat * (n > 5)), bend=-0.8, stretch=1.3), fingers_l=max(0, n - 5),
                         legs="stand", t=g / 30.0)
                if n <= 5:
                    p["arm_l"] = "akimbo"
                    p.pop("fingers_l")
            else:
                u = ramp(g, 1061, 1067)
                p = dict(yaw=lerp(-0.30, -0.15, u), pitch=lerp(0.2, -0.25, u), expr="smug", head_roll=lerp(-4, 8, u), gaze=(-0.4, 0.5),
                         arm_l=dict(hand=(lerp(-0.70, -0.78, u), lerp(-0.08, 0.62, u)), shape="point" if u > 0.5 else None, bend=-0.6,
                                    stretch=1.3),
                         arm_r="akimbo", legs="stand", t=g / 30.0)
                if p["arm_l"]["shape"] is None:
                    p["arm_l"].pop("shape"); p["fingers_l"] = 5
            if g in (1047, 1080):
                p["blink"] = 2
            he.pose(f, p, camera=self.cam)
            _, q = story("inspector_hooded")
            q.update(yaw=0.55, pitch=0.25, t=g / 30.0)
            ins.pose(f, q, camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(he, 384), (ins, 256)], fr)


# ============================================================================= shots 19 + 20: the big balance
POUR_T0 = 1088                       # first loaf leaves the basket
POUR_DT = 2.5
FLY = 6
ROY_19 = (1.55, 5.45)


def landings():
    out = []
    for i in range(12):
        s = POUR_T0 + int(round(POUR_DT * i))
        out.append((s, s + FLY))
    return out


def beam_angles(g_end=1243):
    """film frame -> beam angle: empty bread pan -11 (weights down); every loaf lifts it a bit, it stops at -7 (short)."""
    L = landings()
    ang, a = {}, -11.0
    for g in range(1076, g_end + 1):
        landed = sum(1 for s, e in L if g >= e)
        tgt = -11.0 + 4.0 * landed / 12.0
        a += 0.45 * (tgt - a)
        kick = sum(0.55 * math.exp(-(g - e) / 2.5) * math.cos((g - e) * 1.3) for s, e in L if 0 <= g - e < 10)
        v = a + kick
        if g >= 1132:                                   # shot 20: settled at -7, a nervous shiver before "ขาด!"
            v = -7.0 + 0.35 * math.exp(-(g - 1132) / 6.0) * math.cos((g - 1132) * 0.9)
            if 1146 <= g < 1157:
                v += 0.25 * math.sin((g - 1146) * 2.4)
        ang[g] = v
    return ang


class Shot19(Shot):
    def __init__(self, quality="preview"):
        Shot.__init__(self, "market", "AFTERNOON", quality, lens=24.0)
        self.add("roy", "inspector_royal", 384)
        pngs = C.svg_pngs([(cast6.loaf_svg("lf%d" % k, seed=k + 3), (-0.2, -0.2, 0.2, 0.12), 512) for k in range(4)], self.pdir)
        self.loaf = [C.PropCard("fly%d" % k, [pngs[k]], (-0.2, -0.2, 0.2, 0.12), scale=1.05, shadow=True) for k in range(4)]
        self.ang = beam_angles()
        self.spots = None

    def camera(self, g):
        u = ramp(g, 1083, 1131, "sine")
        loc = V(lerp(1.35, 1.60, u), lerp(2.55, 3.05, u), lerp(4.05, 3.75, u))
        look = V(lerp(2.55, 2.75, u), 6.0, lerp(2.55, 2.45, u))
        return loc, look

    def roy_pose(self, g):
        _, p = story("inspector_pour")
        L = landings()
        gone = sum(1 for s, e in L if g >= s)
        ut = ramp(g, 1083, POUR_T0)
        p["basket"] = dict(loaves=12 - gone, tilt=lerp(5, 62, ut), pour=((g - POUR_T0) / 8.0) % 1.0 if POUR_T0 <= g < L[-1][0] else 0.0)
        p.update(t=g / 30.0, head_roll=-4 + 1.5 * math.sin(g * 0.25), blink=2 if g == 1110 else 0, pitch=0.15)
        p["arm_r"] = dict(hand=(0.92, -0.30), bend=-0.6, stretch=1.3)
        # second hand lifts the basket base: recompute from the anchors of this tilt
        an = sprites.puppet.figure("inspector_royal", p, "q")["anchors"]
        if "basket_base" in an:
            hx, hy = an["basket_base"]
            p["arm_l"] = dict(hand=(hx + 0.02, hy + 0.03), bend=0.5, stretch=1.3, shape="open")
        return p

    def pose(self, shot, gs):
        roy = self.actors["roy"]
        L = landings()
        for g in sorted(set(list(gs) + [1083])):
            f = bf(g)
            loc, look = self.camera(g)
            self.kcam(f, loc, look)
            C.place(roy, f, ROY_19, 0.0)
            self.key_set(f, oven=1.0)
            B.set_big_scale(self.ang[g], frame=f)
            B.set_loaves(sum(1 for s, e in L if g >= e), frame=f)
        lo = B.STATE["big"]["loaves"]
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            p = self.roy_pose(g)
            roy.pose(f, p, camera=self.cam)
            lip = anchor_world(roy, p, "basket_lip", f, self.cam)
            camloc = self.cam.matrix_world.to_translation()
            busy = {}
            for i, (s, e) in enumerate(L):
                if s <= g < e:
                    busy[i % 4] = i
            for k in range(4):
                card = self.loaf[k]
                if k in busy:
                    i = busy[k]
                    s, e = L[i]
                    u = (g - s + 0.5) / float(e - s)
                    tgt = sum((lo[i].matrix_world @ V(*c) for c in lo[i].bound_box), V(0, 0, 0)) / 8.0 + V(0, 0, 0.10)
                    p0 = lip + V(0.05, 0, -0.05)
                    pt = p0.lerp(tgt, u) + V(0, 0, 0.55 * math.sin(math.pi * u) * (1 - u) + 0.15 * math.sin(math.pi * u))
                    card.put(pt, face=camloc, frame=f)
                    card.show(0, frame=f)
                else:
                    card.put(lip, face=camloc, frame=f)
                    card.show(None, frame=f)
        self.sprites_for([(roy, 384)], [bf(g) for g in gs])

    def extra_report(self, g):
        return dict(beam=round(self.ang[g], 2), loaves=sum(1 for s, e in landings() if g >= e))


S20_HIT = 1157                        # "ขาด!"
PIV = V(6.0, 5.36, 6.6)
NEEDLE_K = 3.0


class Shot20(Shot):
    def __init__(self, quality="preview"):
        Shot.__init__(self, "market", "AFTERNOON", quality, lens=30.0)
        self.ang = beam_angles()
        db = (-1.26, -1.42, 1.26, 0.02)
        pngs = C.svg_pngs([(dial_svg(0.0), db, 600), (dial_svg(1.0), db, 600)], self.pdir)
        self.dial = C.PropCard("dial", pngs, db, scale=1.0, shadow=True)
        self.dial.put(PIV + V(0, 0.06, 0), face=PIV + V(0, -5, 0))
        nb = (-0.14, -1.10, 0.14, 0.14)
        self.needle = C.PropCard("needle", C.svg_pngs([(needle_svg(), nb, 600)], self.pdir), nb, scale=1.0, shadow=True)
        self.needle.put(PIV, face=PIV + V(0, -5, 0))
        B.set_loaves(12)

    def camera(self, g):
        if g < S20_HIT:
            u = ramp(g, 1132, S20_HIT, "sine")
            loc = V(lerp(5.85, 6.05, u), lerp(2.65, 3.25, u), lerp(6.55, 6.95, u))
            look = V(lerp(6.10, 6.20, u), 6.0, lerp(7.15, 7.2, u))
            return loc, look, 30.0
        u = ramp(g, S20_HIT, S20_HIT + 3, "sine")
        loc = V(lerp(6.05, 6.30, u), lerp(3.25, 4.05, u), lerp(6.95, 7.05, u)) + V(-0.02, 0.06, 0) * ramp(g, S20_HIT + 3, 1170)
        look = V(lerp(6.05, 6.5, u), 6.0, lerp(7.2, 7.1, u))
        return loc, look, 30.0

    def pose(self, shot, gs):
        for g in gs:
            f = bf(g)
            loc, look, lens = self.camera(g)
            self.kcam(f, loc, look, lens=lens)
            self.key_set(f, oven=1.0)
            B.set_big_scale(self.ang[g], frame=f)
            a = math.radians(-self.ang[g] * NEEDLE_K)
            self.needle.root.rotation_euler = (0.0, a, 0.0)
            self.needle.root.keyframe_insert("rotation_euler", frame=f)
            self.dial.show(1 if g >= S20_HIT else 0, frame=f)

    def extra_report(self, g):
        return dict(beam=round(self.ang[g], 2), needle_deg=round(-self.ang[g] * NEEDLE_K, 1))


# ============================================================================= shot 21: dragged to the pillory
S21_CUT = 1197                        # "ลากไปที่ขื่อ"


def henry_xy(g):
    u = (g - 1164) / float(1243 - 1164)
    return (lerp(1.7, -2.45, u), lerp(4.35, 5.55, u))


class Shot21(Shot):
    def __init__(self, quality="preview"):
        Shot.__init__(self, "market", "AFTERNOON", quality, lens=24.0)
        self.add("henry", "henry", 384)
        self.add("g1", "guard1", 320, canvas=(-2.5, -5.5, 2.5, 0.125))
        self.add("g2", "guard2", 320, canvas=(-2.5, -5.0625, 2.5, 0.125))
        self.add("w1", "woman1", 192)
        self.add("m1", "man1", 192)
        B.set_big_scale(-7.0); B.set_loaves(12)
        pl = B.STATE["pillory"]
        sb = (-1.0, -0.36, 1.0, 0.36)
        self.sign = C.PropCard("sign", C.svg_pngs([(board_svg(2.0, 0.72, "ห้ามขายขาดน้ำหนัก!", 0.27), sb, 512)], self.pdir), sb,
                               scale=1.0, shadow=True)
        cx, cy = pl["neck"][0], pl["neck"][1]
        self.sign.put(V(cx, cy + 0.02, pl["platform_z"] + 3.25), face=V(cx, cy - 10, pl["platform_z"] + 3.25))

    def camera(self, g):
        hx, hy = henry_xy(g)
        if g < S21_CUT:
            u = ramp(g, 1164, S21_CUT)
            P = V(hx + 0.15, hy, 2.45)
            loc = V(hx + lerp(0.55, 0.35, u), hy - lerp(3.0, 2.6, u), lerp(2.05, 2.15, u))
            return loc, P, 24.0
        u = ramp(g, S21_CUT, 1243, "sine")
        loc = V(lerp(-5.3, -5.0, u), lerp(1.6, 2.1, u), lerp(1.05, 1.2, u))
        look = V(lerp(-1.6, -1.9, u), lerp(8.4, 8.4, u), lerp(2.9, 3.0, u))
        return loc, look, 22.0

    def pose(self, shot, gs):
        he, g1, g2, w1, m1 = (self.actors[k] for k in ("henry", "g1", "g2", "w1", "m1"))
        for g in gs:
            f = bf(g)
            loc, look, lens = self.camera(g)
            self.kcam(f, loc, look, lens=lens)
            hx, hy = henry_xy(g)
            C.place(he, f, (hx, hy), 0.0)
            C.place(g1, f, (hx - 1.30, hy + 0.10), 0.0)
            C.place(g2, f, (hx + 1.25, hy - 0.05), 0.0)
            C.place(w1, f, (-6.4, 6.9), 0.0)
            C.place(m1, f, (0.35, 8.4), 0.0)
            wide = g >= S21_CUT
            key_hidden(w1.objects() + m1.objects(), f, not wide)
            self.key_set(f, oven=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            _, p = story("henry_dragged")
            jig = math.sin(g * 0.9)
            p.update(expr="shocked", pale=1.0, t=g / 30.0, head_roll=6 * jig, lean=-6 + 3 * math.sin(g * 0.45),
                     squash=(1.0 + 0.02 * jig, 1.0 - 0.02 * jig), gaze=(0.5 * math.sin(g * 0.21), -0.2))
            if g in (1180, 1222):
                p["blink"] = 2
            he.pose(f, p, camera=self.cam)
            # guards: legs from a march cycle, arms pinned on henry's wrists
            _, q1 = story("guard_drag")
            q1.update(t=g / 30.0, legs=legs_of("guard1", (g - 1164) / 20.0, "walk"), lean=-12 + 2 * math.sin(g * 0.3))
            hw = anchor_world(he, p, "hand_l", f, self.cam)
            g1.pose(f, q1, hands={"r": {"hand": tuple(hw), "bend": -0.5, "stretch": 1.3, "shape": "open"}}, camera=self.cam)
            _, q2 = story("guard_drag_guard2")
            q2.update(mirror=True, t=g / 30.0, lean=8, yaw=0.45, expr="angry",
                      legs=legs_of("guard2", (g - 1170) / 20.0, "walk"))
            hw2 = anchor_world(he, p, "hand_r", f, self.cam)
            g2.pose(f, q2, hands={"r": {"hand": tuple(hw2), "bend": -0.5, "stretch": 1.3, "shape": "open"}}, camera=self.cam)
            _, qw = story("town_point")
            qw.update(t=g / 30.0, head_roll=6 + 4 * math.sin(g * 0.4))
            w1.pose(f, qw, camera=self.cam)
            _, qm = story("town_laugh_man1")
            qm.update(t=g / 30.0 + 0.6, head_roll=-10 + 5 * math.sin(g * 0.5), squash=(1.0, 1.0 + 0.03 * math.sin(g * 0.8)))
            m1.pose(f, qm, camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(he, 384), (g1, 320), (g2, 320), (w1, 192), (m1, 192)], fr)


SHOTS = {17: Shot17, 18: Shot18, 19: Shot19, 20: Shot20, 21: Shot21}


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd == "stills":
        Tk = SHOTS[shot]("preview")
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        for g in gs:
            print(json.dumps(Tk.report(shot, g)), flush=True)
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: SHOTS[shot](q), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
