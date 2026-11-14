#!/usr/bin/env python3
"""shot.py -- film 6b take s29: shots 29-31 (56.80-64.70 s = g 1704..1940, the END) + 6 in-handle frames (g 1698..1703), no
out-handle (the film cuts on g 1940).  Market MORNING.

    shot 29  g 1698..1790  "ฝรั่งเลยเรียกสิบสามว่า โหลของคนทำขนมปัง"
        29a  g 1698..1747  low, up at Henry's shop front: a new hanging sign "13 =" / "โหลของคนทำขนมปัง" swings on its bracket
                           (push + tilt), sun on the facade, blue shade under the jetty
        29b  g 1748..1790  kit in front of the shop, the sign above his head: he looks up at it (g 1748..1758), then grins into
                           the lens holding up a loaf (on "ขนมปัง" g 1776 a little hop of the loaf)
    shot 30  g 1791..1871  "ส่วนลุงเฮนรี่ วันนั้นได้ของครบโหล เป๊ะ"
        30a  g 1791..1830  low MCU, Henry pale and sweating in the pillory, two townsfolk in the foreground corners raise rotten
                           tomatoes (static jeer mouths), slow push
        30b  g 1831..1871  CU Henry (head ~60 % of the width), eyes darting, gulp; three raised tomatoes bob up into the bottom of
                           the frame; push in
    shot 31  g 1872..1940  ECU Henry.  A tomato flies in (g 1877..1882) and SPLATS on his face on "มะเขือเทศ" (g 1883); then the
                           rest rain in (12 hits by g 1931), a "12" counter in the corner flicks up 1 -> 12 with each hit; small
                           camera knock on every hit.  Last frame g 1940 = the cut (no hold).
Mouths: nobody speaks (no quoted line): the static mouth of each expression.  NO depth of field anywhere (client rule).
The set's 3D pillory board + post is cut out at runtime (as film6/s33); Henry carries the cast6 drawn pillory (pose key pillory).

    python3 shot.py probe|stills 29|30|31 a:b[:step] [<out_dir> [scale] [samples]]
    python3 shot.py final 29 | 30,31 a:b[:step] [scale] [samples]
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
sys.path.insert(0, FILM6)
import common as C                                       # noqa: E402
import bpy, bmesh                                        # noqa: E402
from mathutils import Vector                             # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageFilter  # noqa: E402

B, actors, camrig, cast6, render = C.B, C.actors, C.camrig, C.cast6, C.render
lerp, clamp, blink, pulse, ez = C.lerp, C.clamp, C.blink, C.pulse, C.ez
TMP = os.path.join(HERE, "work")
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FONT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
INK = "#3a2832"


def g_of(t):
    return int(round((t + 0.10) * 30))


def g_bound(t):
    return int(round(t * 30))


G29, G30, G31, GEND = g_bound(56.80), g_bound(59.69), g_bound(62.40), 1940      # 1704, 1791, 1872, last frame 1940
H = 6
RANGES = {29: (G29 - H, G30 - 1), 30: (G30, G31 - 1), 31: (G31, GEND)}
CUT_29B, CUT_30B = 1748, 1831
EV = dict(call13=g_of(57.35), dozen=g_of(58.4), bread=g_of(59.09), henry=g_of(59.68), got=g_of(60.55), full=g_of(61.42),
          exact=g_of(62.18), tomato=g_of(62.65), twelve=g_of(63.45))
HITS = [EV["tomato"], 1890, 1896, 1901, 1906, 1910, 1914, 1918, 1921, 1924, 1927, 1930]      # 12 hits, the last on "สิบสองลูก"


def bf(shot, g):
    return int(g) - 1600 + {29: 0, 30: 1000, 31: 2000}[shot]


def framing(shot, g):
    if shot == 29:
        return "29a" if g < CUT_29B else "29b"
    if shot == 30:
        return "30a" if g < CUT_30B else "30b"
    return "31"


# ----------------------------------------------------------------------------- staging (market world D)
PZ = 1.0
HENRY = (-4.0, 9.95)                       # pillory stand (platform top z 1.0)
WOMAN = (-4.95, 5.75)
MAN = (-3.10, 5.95)
KIT = (-18.55, 0.75)
SIGN = Vector((-21.15, 0.55, 4.55))        # hanging sign board centre (in front of Henry's facade, x -22)
SIGN_W = 3.4
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)
CANVAS_H = (-1.8125, -4.375, 1.8125, 0.125)

CAMS = {  # framing: (g_a, loc_a, look_a, g_b, loc_b, look_b, lens)
    "29a": (RANGES[29][0], (-15.6, -0.2, 1.8), (-21.2, 0.55, 4.25), CUT_29B - 1, (-16.6, 0.1, 2.1), (-21.2, 0.55, 4.45), 26.0),
    "29b": (CUT_29B, (-13.4, 0.25, 2.35), (-18.9, 0.70, 2.55), RANGES[29][1], (-13.9, 0.35, 2.40), (-18.9, 0.70, 2.57), 26.0),
    "30a": (G30, (-4.15, 2.40, 2.30), (-4.0, 9.9, 3.10), CUT_30B - 1, (-4.10, 3.20, 2.40), (-4.0, 9.9, 3.15), 32.0),
    "30b": (CUT_30B, (-3.85, 7.45, 3.05), (-4.0, 9.9, 3.30), RANGES[30][1], (-3.90, 7.75, 3.15), (-4.0, 9.9, 3.32), 30.0),
    "31": (G31, (-3.95, 7.70, 3.30), (-4.0, 9.9, 3.42), GEND, (-4.0, 7.86, 3.34), (-4.0, 9.9, 3.42), 30.0),
}


def knock(g):
    """small camera knock on each hit (shot 31)."""
    v = Vector((0, 0, 0))
    for i, h in enumerate(HITS):
        d = g - h
        if 0 <= d < 7:
            a = (0.035 if i == 0 else 0.018) * math.exp(-d / 2.2) * math.cos(d * 1.9)
            v += Vector((a * (1 if i % 2 else -1), 0.0, a * 0.6))
    return v


def cam_at(shot, g):
    fr = framing(shot, g)
    a, la, ka, b, lb, kb, lens = CAMS[fr]
    u = ez(clamp((g - a) / float(max(1, b - a))), "sine")
    if fr == "29a":                                        # the sign swings: a slow pan-ish drift
        u = clamp((g - a) / float(b - a))
    loc, look = Vector(lerp(la, lb, u)), Vector(lerp(ka, kb, u))
    if fr == "31":
        k = knock(g)
        loc += k
        look += k * 0.5
    return loc, look, lens


# ----------------------------------------------------------------------------- PIL pieces (Thai text: Kanit + raqm)
def _font(px):
    return ImageFont.truetype(FONT, px, layout_engine=ImageFont.Layout.RAQM)


def _text_ink(im, xy, text, f, fill, stroke):
    W, Hh = im.size
    m = Image.new("L", (W, Hh), 0)
    ImageDraw.Draw(m).text(xy, text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
    m = m.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    im.paste(Image.new("RGBA", (W, Hh), INK), (0, 0), m)
    ImageDraw.Draw(im).text(xy, text, font=f, fill=fill)


def sign_png():
    """the hanging sign: an oak board with iron rings at the top, "13 =" big, "โหลของคนทำขนมปัง" below, a loaf drawn beside "13"."""
    path = os.path.join(TMP, "labels", "sign13.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    W, Hh = 1360, 900
    im = Image.new("RGBA", (W, Hh), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # chains / rings
    for x in (250, W - 250):
        d.line([(x, 0), (x, 140)], fill=INK, width=14)
        for y in (30, 75, 120):
            d.ellipse((x - 16, y - 20, x + 16, y + 20), outline="#6a6a72", width=9)
    # board
    d.rounded_rectangle((20, 130, W - 20, Hh - 20), radius=46, fill="#9a5e2e", outline=INK, width=16)
    for i, y in enumerate(range(180, Hh - 60, 105)):
        d.line([(60, y), (W - 60, y)], fill="#87511f", width=8)
    d.rounded_rectangle((52, 160, W - 52, Hh - 52), radius=34, outline="#c48848", width=8)
    for (x, y) in ((70, 190), (W - 70, 190), (70, Hh - 70), (W - 70, Hh - 70)):
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill="#4a4048", outline=INK, width=4)
    f1, f2 = _font(300), _font(150)
    t1 = "13 ="
    l, t, r, b = f1.getbbox(t1)
    _text_ink(im, ((W - (r - l)) / 2 - l + 70, 160 - t + 18), t1, f1, "#ffd23c", 14)
    # a little loaf icon left of "13"
    cx, cy = (W - (r - l)) / 2 - 90, 160 + 175
    d.ellipse((cx - 95, cy - 70, cx + 95, cy + 60), fill="#f2e0b8", outline=INK, width=12)
    d.line([(cx - 40, cy - 30), (cx + 40, cy + 10)], fill="#d8b47c", width=12)
    d.line([(cx - 40, cy + 10), (cx + 40, cy - 30)], fill="#d8b47c", width=12)
    t2 = "โหลของคนทำขนมปัง"
    l, t, r, b = f2.getbbox(t2)
    _text_ink(im, ((W - (r - l)) / 2 - l, 560 - t + 28), t2, f2, "#ffffff", 10)
    im.save(path)
    return path


def splat_svg(k):
    """a cartoon tomato splat (comic, not cruel): a wobbly red star-blob with pulp, seeds, a drip and flying drops, ink outline.
    Box (-0.20,-0.16,0.20,0.20) D; centre (0, 0)."""
    rnd = random.Random(500 + k)
    pts = []
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n + rnd.uniform(-0.12, 0.12)
        r = (0.125 if i % 2 == 0 else 0.075) * rnd.uniform(0.8, 1.15)
        pts.append((r * math.cos(a), r * math.sin(a) * 0.85))
    d = "M %.4f %.4f " % pts[0]
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        d += "Q %.4f %.4f %.4f %.4f " % (x0 * 1.18 + x1 * 0.0, y0 * 1.18, (x0 + x1) / 2, (y0 + y1) / 2) if False else \
             "Q %.4f %.4f %.4f %.4f " % (x1 * 1.0 + (x0 - x1) * 0.15, y1 + (y0 - y1) * 0.15, x1, y1)
    d += "Z"
    drip = ('<path d="M -0.02 0.05 L -0.03 0.15 Q -0.03 0.18 0.0 0.18 Q 0.03 0.18 0.025 0.15 L 0.02 0.05 Z" fill="#c22a24" '
            'stroke="%s" stroke-width="0.010"/>' % INK)
    drops = "".join('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#c22a24" stroke="%s" stroke-width="0.008"/>'
                    % (0.17 * math.cos(a), 0.14 * math.sin(a), rnd.uniform(0.010, 0.018), INK)
                    for a in [rnd.uniform(0, 6.28) for _ in range(5)])
    pulp = '<ellipse cx="0.0" cy="0.0" rx="0.06" ry="0.045" fill="#e8554a"/>'
    seeds = "".join('<ellipse cx="%.4f" cy="%.4f" rx="0.008" ry="0.005" fill="#f6d27a" transform="rotate(%d %.4f %.4f)"/>'
                    % (x, y, rnd.randint(0, 180), x, y) for x, y in [(rnd.uniform(-0.05, 0.05), rnd.uniform(-0.035, 0.035)) for _ in range(6)])
    skin = '<path d="M -0.05 -0.03 q 0.03 -0.03 0.06 0" stroke="#ff9a8a" stroke-width="0.012" fill="none" stroke-linecap="round"/>'
    calyx = ('<path d="M %.3f %.3f l 0.03 -0.012 l -0.012 0.03 z" fill="#4f7a2a" stroke="%s" stroke-width="0.006"/>'
             % (rnd.uniform(-0.06, 0.04), rnd.uniform(-0.06, -0.02), INK)) if k % 2 == 0 else ""
    return (drops + drip + '<path d="%s" fill="#c22a24" stroke="%s" stroke-width="0.014" stroke-linejoin="round"/>' % (d, INK)
            + pulp + seeds + skin + calyx)


def counter_png(n):
    """the hit counter: a red tomato badge with the number."""
    path = os.path.join(TMP, "labels", "count%02d.png" % n)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    S = 400
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((24, 50, S - 24, S - 14), fill="#d8322a", outline=INK, width=14)
    d.ellipse((80, 95, 160, 150), fill="#f07a64")
    # calyx
    cx = S // 2
    for a in (-60, -20, 20, 60):
        x2, y2 = cx + 70 * math.sin(math.radians(a)), 62 + 30 * math.cos(math.radians(a))
        d.line([(cx, 50), (x2, y2)], fill="#3f7a2a", width=22)
    d.ellipse((cx - 20, 30, cx + 20, 70), fill="#3f7a2a", outline=INK, width=6)
    f = _font(230 if n < 10 else 200)
    txt = str(n)
    l, t, r, b = f.getbbox(txt)
    _text_ink(im, (S / 2 - (r + l) / 2, S / 2 + 20 - (b + t) / 2), txt, f, "#ffffff", 12)
    im.save(path)
    return path


# ----------------------------------------------------------------------------- poses
WRIST = cast6.PILLORY_WRIST_Y


def kit_pose(g):
    _, p0 = cast6.STORY6["kit_hold_loaf"]
    p = dict(p0)
    up = 1.0 - ez((g - (CUT_29B + 12)) / 8.0) if g >= CUT_29B else 1.0      # looks up at the sign, then to the lens
    p.update(yaw=lerp(0.18, -0.30, up), pitch=lerp(-0.12, -0.55, up), gaze=(lerp(0.1, -0.35, up), lerp(0.0, -0.95, up)),
             expr="grinning" if up < 0.5 else "happy", head_roll=lerp(-5, 6, up) + 2 * math.sin(g * 0.2),
             blink=blink(g, [CUT_29B + 15, 1784]), t=g / 30.0)
    hop = pulse(g, EV["bread"] - 2, EV["bread"] + 2, EV["bread"] + 8, 1.0)
    p["arm_r"] = dict(hand=(0.74, -0.02 - 0.18 * hop), bend=-0.6, stretch=1.3)
    return p


def henry_pose(shot, g):
    p = dict(yaw=0.0, pitch=0.10, expr="worried", pale=0.9, fx=["sweat"], head_roll=0, legs="stand", pillory=True,
             arm_r=dict(hand=(0.56, WRIST), bend=-0.6, stretch=1.3), arm_l=dict(hand=(-0.56, WRIST), bend=-0.6, stretch=1.3),
             t=g / 30.0)
    if shot == 30:
        dart = math.sin(g * 0.35) if g < CUT_30B else (1.0 if (g // 9) % 2 else -1.0)
        gulp = pulse(g, EV["exact"] - 3, EV["exact"], EV["exact"] + 6, 1.0)
        p.update(gaze=(0.75 * dart, 0.25), yaw=0.08 * dart, head_roll=3 * math.sin(g * 0.13), squash=(1 + 0.04 * gulp, 1 - 0.04 * gulp),
                 blink=blink(g, [1800, 1846, 1866]), expr="worried" if g < EV["full"] else "stunned")
    else:
        hit = [h for h in HITS if h <= g]
        last = hit[-1] if hit else None
        d = (g - last) if last is not None else 99
        k = math.exp(-d / 3.0) * (1 if len(hit) % 2 else -1) if last is not None else 0.0
        p.update(expr="worried" if not hit else ("shocked" if len(hit) < 4 else "stunned"),
                 head_roll=-9 * k, yaw=0.12 * k, pitch=0.10 - 0.08 * abs(k), gaze=(0.0, 0.0) if hit else (0.55, 0.10),
                 blink=2 if d <= 2 else (blink(g, [1874]) if not hit else 0), squash=(1 + 0.06 * abs(k), 1 - 0.06 * abs(k)))
        if not hit:
            p["expr"] = "worried"
            p["gaze"] = (0.6 - 0.1 * (g - G31) / 5.0, 0.2)
    return p


def crowd_pose(cast, g, i):
    _, p0 = cast6.STORY6["town_raise_veg" + ("" if cast == "woman1" else "_man1")]
    p = dict(p0)
    sh = math.sin(g * 0.45 + 1.7 * i)
    p.update(yaw=[0.70, -0.70][i], prop_r=dict(type="tomato", scale=1.6), head_roll=p0.get("head_roll", 0) + 3 * sh,
             blink=blink(g, [1805 + 9 * i, 1826 + 5 * i]), t=g / 30.0)
    p["arm_r"] = dict(p0["arm_r"], hand=(p0["arm_r"]["hand"][0], p0["arm_r"]["hand"][1] - 0.05 * sh))
    if i == 1:
        p["mirror"] = True
    return p


# ----------------------------------------------------------------------------- set changes
def cut_pillory_board():
    ob = bpy.data.objects.get("pillory")
    cx, cy = -4.0, 9.5
    bm = bmesh.new(); bm.from_mesh(ob.data)
    mw = ob.matrix_world
    kill = [v for v in bm.verts if (lambda p: p.z > PZ + 0.06 and abs(p.x - cx) < 1.85 and cy - 0.3 < p.y < cy + 0.55)(mw @ v.co)]
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(ob.data); bm.free(); ob.data.update()
    return len(kill)


USE29A = ()
USE = {29: ("kit",), 30: ("henry", "woman", "man"), 31: ("henry",)}


class Take(C.Take):
    def __init__(self, shots, quality="preview"):
        C.Take.__init__(self, "market", "MORNING", quality=quality, lens=26.0, name="cam_s29")
        self.shots = shots
        self.scene.cycles.transparent_max_bounces = 64          # many stacked splat / tomato cards: no black holes
        n = cut_pillory_board()
        print("s29: cut %d pillory verts" % n, flush=True)
        sd = os.path.join(TMP, "sprites")
        need = set(a for s in shots for a in USE[s])
        if "kit" in need:
            self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        if "henry" in need:
            self.actors["henry"] = C.make_actor("henry", "henry", sd, CANVAS_H)
        if "woman" in need:
            self.actors["woman"] = C.make_actor("woman", "woman1", sd)
            self.actors["man"] = C.make_actor("man", "man1", sd)
        # the sign
        sp = sign_png()
        w, h = Image.open(sp).size
        ppd = w / SIGN_W
        self.sign = C.PropCard("sign13", [sp], (-w / 2.0 / ppd, -h / 2.0 / ppd, w / 2.0 / ppd, h / 2.0 / ppd), shadow=True)
        # tomatoes: flying (whole) + splats (squash) + raised (30b) + the counter
        items = [(cast6.tomato_svg("tw%d" % k, r=0.075, rot=40 * k), (-0.12, -0.12, 0.12, 0.12), 900) for k in range(3)]
        items += [(splat_svg(k), (-0.20, -0.16, 0.20, 0.20), 900) for k in range(3)]
        P = C.svg_pngs(items, os.path.join(TMP, "props"))
        self.fly = [C.PropCard("fly%02d" % i, [P[i % 3]], (-0.12, -0.12, 0.12, 0.12), scale=0.0001, shadow=False) for i in range(12)]
        self.splat = [C.PropCard("splat%02d" % i, [P[3 + i % 3]], (-0.20, -0.16, 0.20, 0.20), scale=0.0001, shadow=False)
                      for i in range(12)]
        self.raised = [C.PropCard("raised%d" % i, [P[i % 3]], (-0.12, -0.12, 0.12, 0.12), scale=0.0001, shadow=False) for i in range(3)]
        cps = [counter_png(n) for n in range(1, 13)]
        self.counter = C.PropCard("counter", cps, (-0.5, -0.5, 0.5, 0.5), scale=0.0001, shadow=False)
        rnd = random.Random(31)
        # splat spots on Henry's face / head / board (local D, head centre, y down) and spin
        self.spots = [(0.06, 0.08)] + [(rnd.uniform(-0.48, 0.48), rnd.uniform(-0.45, 0.42)) for _ in range(11)]
        self.spin = [rnd.uniform(-40, 40) for _ in range(12)]
        self.from_ = [Vector((rnd.choice((-1, 1)) * rnd.uniform(0.5, 0.9), 0.0, rnd.uniform(-0.9, -0.4))) for _ in range(12)]
        self.from_[0] = Vector((0.75, 0.0, -0.7))

    # ---- helpers
    def _hide_actor(self, a, f, hidden):
        for o in a.objects():
            o.hide_render = hidden
            o.keyframe_insert("hide_render", frame=f)
            fc = C._fcurve(o, "hide_render")
            if fc is not None:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"

    def cam_axes(self, loc, look):
        fwd = (look - loc).normalized()
        right = fwd.cross(Vector((0, 0, 1))).normalized()
        up = right.cross(fwd).normalized()
        return fwd, right, up

    def pose(self, shot, gs):
        far = Vector((0, -80, -60))
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            self.key_cam(f, loc, look, lens)
            B.set_oven(1.0, frame=f)
            for nm, a in self.actors.items():
                self._hide_actor(a, f, nm not in USE[shot] or framing(shot, g) == "29a")
            if "kit" in self.actors:
                C.place(self.actors["kit"], f, KIT, 0.0)
            if "henry" in self.actors:
                C.place(self.actors["henry"], f, HENRY, PZ)
            if "woman" in self.actors:
                C.place(self.actors["woman"], f, WOMAN, 0.0)
                C.place(self.actors["man"], f, MAN, 0.0)
            # sign: swings gently on its rings (rotation about x = the facade normal axis)
            sw = math.radians(4.0 * math.sin(g * 0.16) * (1.0 if shot == 29 else 0.0))
            self.sign.root.location = SIGN
            self.sign.root.rotation_euler = (0.0, sw, math.radians(90.0))        # faces +x (the square)
            self.sign.root.keyframe_insert("location", frame=f)
            self.sign.root.keyframe_insert("rotation_euler", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 29:
                self.actors["kit"].pose(f, kit_pose(g), camera=self.cam)
            else:
                self.actors["henry"].pose(f, henry_pose(shot, g), camera=self.cam)
                if shot == 30:
                    self.actors["woman"].pose(f, crowd_pose("woman1", g, 0), camera=self.cam)
                    self.actors["man"].pose(f, crowd_pose("man1", g, 1), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(self.actors[n], {"kit": 448, "henry": 640 if shot == 31 else 448, "woman": 320, "man": 320}[n]) for n in USE[shot]]
        self.sprites_for(jobs, fr)
        # 2D tomato pieces need the head position: after the sprites
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            fwd, right, up = self.cam_axes(loc, look)
            n_hit = sum(1 for h in HITS if h <= g) if shot == 31 else 0
            hw = None
            if shot in (30, 31):
                a = self.actors["henry"]
                hx, hy = self.anch[("henry", f)]["head"]
                hw = lambda dx, dy: actors.local_to_world(a, (hx + dx, hy + dy), f, None, self.cam)
            for i in range(12):
                fpc, spc = self.fly[i], self.splat[i]
                showf, shows = False, False
                if shot == 31:
                    h = HITS[i]
                    tgt = hw(*self.spots[i])
                    tgt = tgt + (loc - tgt).normalized() * 0.10
                    if h - 6 <= g < h:
                        u = (g - (h - 6)) / 6.0
                        start = loc + fwd * 0.55 + right * self.from_[i].x + up * self.from_[i].z
                        p = start.lerp(tgt, u) + up * (0.15 * math.sin(math.pi * u))
                        fpc.root.scale = (1.4,) * 3
                        fpc.put(p, face=tuple(loc), frame=f)
                        showf = True
                    if g >= h:
                        d = g - h
                        sq = [1.35, 1.15, 1.0][min(d, 2)]
                        s = (1.7 if i == 0 else 0.95) * sq
                        spc.root.scale = (s, s, s * (1.0 + 0.004 * min(d, 20)))          # drips a touch longer
                        spc.put(tgt + Vector((0, 0, -0.004 * min(d, 20))), face=tuple(loc), frame=f)
                        shows = True
                if not showf:
                    fpc.root.scale = (0.0001,) * 3
                    fpc.put(far, face=tuple(loc), frame=f)
                if not shows:
                    spc.root.scale = (0.0001,) * 3
                    spc.put(far, face=tuple(loc), frame=f)
                for pc, on in ((fpc, showf), (spc, shows)):
                    pc.root.keyframe_insert("scale", frame=f)
                    pc.cards[0].hide_render = not on
                    pc.cards[0].keyframe_insert("hide_render", frame=f)
            # raised tomatoes bobbing into the bottom of the frame (30b)
            for i, pc in enumerate(self.raised):
                on = shot == 30 and g >= CUT_30B
                if on:
                    rise = ez(clamp((g - (CUT_30B + 2 + 4 * i)) / 8.0))
                    p = loc + fwd * 1.2 + right * [-0.42, 0.40, 0.05][i] + up * (lerp(-1.25, -0.62, rise) + 0.03 * math.sin(g * 0.5 + 2 * i))
                    pc.root.scale = (1.5,) * 3
                    pc.put(p, face=tuple(loc), frame=f)
                else:
                    pc.root.scale = (0.0001,) * 3
                    pc.put(far, face=tuple(loc), frame=f)
                pc.root.keyframe_insert("scale", frame=f)
                pc.cards[0].hide_render = not on
                pc.cards[0].keyframe_insert("hide_render", frame=f)
            # the counter (upper right of the frame, camera-relative)
            if shot == 31 and n_hit > 0:
                d = g - HITS[n_hit - 1]
                pp = 1.0 + 0.35 * math.exp(-d / 2.0) if d < 8 else 1.0
                lift = 0.03 * math.exp(-d / 2.0)
                p = loc + fwd * 1.0 + right * 0.20 + up * (0.42 + lift)
                self.counter.root.scale = (0.17 * pp,) * 3
                self.counter.put(p, face=tuple(loc), frame=f)
                for k, ob in enumerate(self.counter.cards):
                    ob.hide_render = k != n_hit - 1
            else:
                self.counter.root.scale = (0.0001,) * 3
                self.counter.put(far, face=tuple(loc), frame=f)
                for ob in self.counter.cards:
                    ob.hide_render = True
            self.counter.root.keyframe_insert("scale", frame=f)
            for ob in self.counter.cards:
                ob.keyframe_insert("hide_render", frame=f)
        for pc in self.fly + self.splat + self.raised + [self.counter]:
            for ob in pc.cards:
                fc = C._fcurve(ob, "hide_render")
                if fc is not None:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(shot, g)
        heads = C.head_report(self, f)
        out = dict(shot=shot, g=g, framing=framing(shot, g), cam=[round(c, 3) for c in loc], lens=lens,
                   heads={k: v for k, v in heads.items() if k in USE[shot]})
        if shot == 29:
            out["sign_px"] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(SIGN), f)[:2]]
        if shot == 31:
            out["hits"] = sum(1 for h in HITS if h <= g)
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take(shots, "preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(shots, q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
