#!/usr/bin/env python3
"""shot.py -- film 6 take s11: shot 11 (plan 26.32-31.09 s = g 790..932) + 6-frame handles (g 784..938), bakery MORNING, counter.

    F1  g 784..825  two-shot over the counter from the street: kit (screen-left, hidden stool) has just slipped the paler 13th loaf
                    on top of the customer's basket; henry (screen-right, by his hand balance) turns, sees it, goes red (anger fill
                    rises, steam from the ears).  Narration "ลุงเห็นก็โวยลั่นร้าน" (not a quote): henry's mouth is a static drawing.
    F2  g 826..857  tighter two-shot, slightly low: henry YELLS (lip-sync on the quote "เอ็งจะแจกขนมปังฟรีให้ข้าเจ๊งเหรอ" from g 825),
                    points at the 13th loaf; kit shrinks (scale 1.0 -> 0.88, sinks behind the counter, worried + sweat).
    F3  g 858..887  low-angle punch-in on henry still yelling, finger at the loaf; kit small at frame left.
    F4  g 888..938  cut (29.5 s + 0.1 = g 888) to henry at his hand balance, tapping the beam with a fat finger while he talks
                    ("ก้อนของข้า ชั่งมาเป๊ะแล้ว", quote ends g 935): the beam wobbles at each tap and settles level.
Mouths: henry lip-syncs only inside the quote (g 825..935); kit never speaks.  NO depth of field (common.Take).

    python3 shot.py probe 11 a:b[:step]
    python3 shot.py stills 11 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 11 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(26.32), C.g_bound(31.09)          # 790, 933
H = 6
RANGES = {11: (G0 - H, G1 - 1 + H)}                    # 784..938
Q0, Q1 = C.g_of(27.41), C.g_of(31.06)                  # 825, 935: the quote (lip-sync window)
F2, F3, F4 = 826, 858, C.g_of(29.5)                    # framing changes (F4 = 888, the plan's cut to the scale)
G_TURN = (792, 802)                                    # henry turns from the scale to kit
G_SHRINK = (828, 838)
TAPS = [896, 907, 918, 929]                            # finger taps on the beam

# ----------------------------------------------------------------------------- staging (bakery world D)
KIT, KIT_Z = (-0.15, 1.55), 0.80
HENRY, HENRY_Z = (1.80, 1.95), 0.40                    # on a hidden step behind the counter
HENRY4 = (2.05, 1.45)                                  # F4 (after the cut): right behind his hand balance
BASKET = Vector((0.62, 0.95, 1.25))
BASKET_SCALE = 1.3
SCALE_FOOT = Vector((2.4, 0.75, 1.25))
STEAM = 0.3
LENS = 24.0

CAMS = {   # framing -> ((loc A, look A), (loc B, look B), lens)   A -> B over the framing (slow push / drift)
    1: (((0.85, -2.95, 2.70), (0.85, 1.6, 2.55)), ((0.85, -2.70, 2.70), (0.85, 1.6, 2.55)), 24.0),
    2: (((0.85, -2.25, 2.25), (0.80, 1.6, 2.75)), ((0.85, -2.10, 2.25), (0.80, 1.6, 2.75)), 24.0),
    3: (((1.95, -1.55, 1.95), (1.55, 1.9, 3.05)), ((1.90, -1.40, 1.95), (1.55, 1.9, 3.05)), 24.0),
    4: (((2.70, -1.45, 2.95), (2.15, 1.6, 2.45)), ((2.66, -1.30, 2.95), (2.15, 1.6, 2.45)), 24.0),
}
SPANS = {1: (RANGES[11][0], F2 - 1), 2: (F2, F3 - 1), 3: (F3, F4 - 1), 4: (F4, RANGES[11][1])}


def framing(g):
    return 1 if g < F2 else 2 if g < F3 else 3 if g < F4 else 4


def cam_at(g):
    k = framing(g)
    (la, oa), (lb, ob), lens = CAMS[k]
    a, b = SPANS[k]
    u = ez((g - a) / float(max(1, b - a)), "sine")
    return Vector(lerp(la, lb, u)), Vector(lerp(oa, ob, u)), lens


def scale_angle(g):
    """hand balance: level, a small damped wobble after every tap (finger on the loaf side: + = loaf pan down)."""
    a = 0.0
    for t in TAPS:
        if g >= t:
            d = g - t
            a += 2.6 * math.exp(-d / 5.0) * math.cos(d * 0.75)
    return a


def hide_obj(name, hidden, f):
    """keyed (constant) hide_render of a set object -- the opening's hanging bundles come within ~1 D of the low / near cameras,
    where their painted texture is magnified into a soft smear (reads as blur: client rule 'sharp image')."""
    ob = C.bpy.data.objects.get(name)
    if ob is None:
        return
    ob.hide_render = bool(hidden)
    ob.keyframe_insert("hide_render", frame=f)
    fc = C._fcurve(ob, "hide_render")
    if fc is not None:
        for kp in fc.keyframe_points:
            kp.interpolation = "CONSTANT"


# ----------------------------------------------------------------------------- poses
def anger(g):
    return clamp((g - 794) / 24.0) * 0.6 + 0.3 * clamp((g - 826) / 10.0)


def henry_pose(g):
    talk = Q0 <= g <= Q1
    fr = framing(g)
    p = dict(expr="furious", head_roll=-8 + 3 * math.sin(g * 0.35), lean=-4, legs="wide", arm_r="akimbo", t=g / 30.0)
    lvl = anger(g)
    p["fx"] = ["steam"] if g >= 800 else []     # no anger_fill: its red-violet wash reads magenta on henry's face
    if fr == 1:
        u = ez((g - G_TURN[0]) / float(G_TURN[1] - G_TURN[0])) if g >= G_TURN[0] else 0.0
        p.update(yaw=lerp(0.35, -0.4, u), pitch=lerp(0.35, -0.3, u), gaze=(lerp(0.4, -0.8, u), lerp(0.6, 0.2, u)))
        p["expr"] = "unimpressed" if g < 798 else ("shocked" if g < 806 else "furious")
        p["arm_l"] = dict(hand=(-0.55, 0.35), bend=-0.6) if g < 812 else dict(hand=(-1.20, 0.30), shape="point", bend=0.15, stretch=1.45, layer="top")
    elif fr in (2, 3):
        jab = 0.06 * math.sin(g * 0.9)
        p.update(yaw=-0.42, pitch=-0.45, gaze=(-0.85, 0.35), lean=-6)
        p["arm_l"] = dict(hand=(-1.20 + jab, 0.30 + jab), shape="point", bend=0.15, stretch=1.45, layer="top")
        p["head_roll"] = -8 + 4 * math.sin(g * 0.5)
    else:
        p.update(yaw=-0.15, pitch=0.05, gaze=(0.25, 0.1), lean=4, expr="angry")
        p["arm_l"] = dict(hand=(-0.7, 0.6), shape="point", bend=0.4)
    if talk:
        p["mouth"] = cast6.talk_mouth(g, 1.0, seed=11, hold=2)
    p["blink"] = blink(g, [790, 846, 892, 924])
    return p


def kit_pose(g):
    s = ez((g - G_SHRINK[0]) / float(G_SHRINK[1] - G_SHRINK[0])) if g >= G_SHRINK[0] else 0.0
    if g < 806:   # still pleased with himself, then caught
        p = dict(yaw=0.25, pitch=0.15, expr="smirk" if g < 800 else "shocked", head_roll=-3, gaze=(0.6, 0.3) if g >= 798 else (0.1, 0.0),
                 arm_l=dict(hand=(-0.40, 0.80), bend=0.5), arm_r=dict(hand=(0.45, 0.62), bend=-0.5, stretch=1.2), legs="stand")
    else:
        p = dict(yaw=0.32, pitch=0.30, expr="worried", fx=["sweat"], head_roll=8 + 2 * math.sin(g * 0.6), lean=-4,
                 squash=(1.03, 0.96), gaze=(0.85, -0.2), legs="narrow",
                 arm_r=dict(hand=(0.18, 0.40), bend=-0.6, shape="open"), arm_l=dict(hand=(-0.20, 0.38), bend=-0.6, shape="open"))
        p["head_roll"] += 3 * s
    p["blink"] = blink(g, [812, 852, 880, 914])
    p["t"] = g / 30.0
    return p


def kit_scale(g):
    s = ez((g - G_SHRINK[0]) / float(G_SHRINK[1] - G_SHRINK[0])) if g >= G_SHRINK[0] else 0.0
    s = s + 0.04 * math.sin(clamp((g - G_SHRINK[0]) / 6.0) * math.pi) if g >= G_SHRINK[0] else s
    return 1.0 - 0.12 * s, KIT_Z - 0.18 * s


# ----------------------------------------------------------------------------- the take
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=LENS, name="cam_s11")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        svg, an = cast6.basket_svg("bk13", loaves=13)
        box = (-0.56, -0.06, 0.56, 0.72)
        pngs = C.svg_pngs([(svg, box, 512)], os.path.join(TMP, "props"))
        self.basket = C.PropCard("basket", pngs, box, scale=BASKET_SCALE, shadow=True)
        self.basket.put(BASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=CAMS[1][0][0])

    def loaf13(self):
        return self.basket.to_world((0.014, 0.114))

    def tap_point(self, g):
        """the beam just left of the pivot (loaf side); finger lifts 0.12 D between taps."""
        up = 0.0
        for t in TAPS:
            d = g - t
            if -4 <= d <= 0:
                up = 0.14 * (-d) / 4.0
            elif 0 < d <= 5:
                up = 0.14 * d / 5.0
        if g < TAPS[0] - 4 or g > TAPS[-1] + 5:
            up = 0.14
        return SCALE_FOOT + Vector((-0.18, 0.0, 0.95 + 0.05 + 0.6 * up))

    def pose(self, shot, gs):
        kit, henry = self.actors["kit"], self.actors["henry"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(g)
            self.key_cam(f, loc, look, lens=lens)
            sc, kz = kit_scale(g)
            C.place(kit, f, KIT, kz, scale=sc)
            C.place(henry, f, HENRY4 if framing(g) == 4 else HENRY, HENRY_Z)
            self.key_set(f, steam=STEAM, oven=1.0)
            B.set_scale(scale_angle(g), frame=f)
            hide_obj("opening_bundles", framing(g) == 4, f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            hands = None
            hp = henry_pose(g)
            if framing(g) == 4:
                hands = {"l": {"hand": tuple(self.tap_point(g)), "shape": "point", "bend": 0.4, "stretch": 1.35, "layer": "top"}}
            _, inf = henry.pose(f, hp, hands=hands, camera=self.cam)
            if os.environ.get("S11_DEBUG"):
                print("hand", g, {k: (v.get("reached"), round(v.get("error", 0), 3), round(v.get("clearance", 0), 3)) for k, v in inf.items() if isinstance(v, dict)}, flush=True)
            kit.pose(f, kit_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 448), (henry, 384)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(g)
        v = look - loc
        return dict(shot=shot, g=g, framing=framing(g), cam=[round(c, 3) for c in loc],
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f),
                    talk=bool(Q0 <= g <= Q1), scale_deg=round(scale_angle(g), 2))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
