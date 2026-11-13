#!/usr/bin/env python3
"""shot.py -- film 6 take s16: shots 16-19 (plan 41.29-52.60 s = g 1239..1577) + 6-frame handles (g 1233..1583).

    shot 16  g 1233..1334  bakery MORNING, counter, low angle on henry.
             A g 1233..1284  henry belly-laughs (eyes shut, tears, bouncing; laughing drawing = static mouth: "ลุงเฮนรี่หัวเราะ" is
                             narration), kit small at frame left looking up at him.  Quote "พวกนั้นมันโกง ส่วนข้าซื่อสัตย์" g 1271..1336:
                             henry lip-syncs (smug drawing from g 1271).
             B g 1285..1334  lower punch-in, henry solo, arms crossed, smug, talking.
    shot 17  g 1335..1420  bakery MORNING, the cooling table.
             A g 1335..1378  insert: kit's basket of 13 on the table, steam; henry's fat hand comes in from the right, snatches the pale
                             13th loaf off the top (g 1347), pulls it away.
             B g 1379..1420  two-shot at the table: henry holds the loaf and wags a finger at kit (closed mouth); kit droops.
    shot 18  g 1421..1514  bakery AFTERNOON (low gold sun through the window), kit alone.
             A g 1421..1466  window_out: kit sneaks (tiptoe cycle) from the shop to the counter with a morning loaf on his palm.
             B g 1467..1514  closer, over the counter: he looks round, lays the loaf on the hand balance's empty pan (g 1489); the beam
                             swings from the weights side (-8) to about level.
    shot 19  g 1515..1583  bakery AFTERNOON, small_scale_insert.
             A g 1515..1547  ECU: the loaf side of the beam RISES (lighter) -- slow ease to -6 deg.
             B g 1548..1583  from the street side over the counter: the tilted balance, kit's face peeking over the counter, eyes wide.
Mouths: henry lip-syncs only in g 1271..1336 (quote 2); nobody else talks.  NO depth of field (common.Take).

    python3 shot.py probe 16 a:b[:step]
    python3 shot.py stills 16,17 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 18,19 a:b[:step] [scale] [samples]      (16,17 MORNING and 18,19 AFTERNOON are separate takes: one group per call)
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
gb = C.g_bound
H = 6
S16, S17, S18, S19, S20 = gb(41.29), gb(44.50), gb(47.37), gb(50.50), gb(52.60)     # 1239 1335 1421 1515 1578
RANGES = {16: (S16 - H, S17 - 1), 17: (S17, S18 - 1), 18: (S18, S19 - 1), 19: (S19, S20 - 1 + H)}
Q0, Q1 = C.g_of(42.28), C.g_of(44.43)                  # 1271, 1336: quote 2 (lip-sync window)
CUT = {16: 1285, 17: 1379, 18: 1467, 19: 1548}         # A -> B framing inside each shot
G_SNATCH = 1347
G_PUT = 1489
PRESET = {16: "MORNING", 17: "MORNING", 18: "AFTERNOON", 19: "AFTERNOON"}

# ----------------------------------------------------------------------------- staging (bakery world D)
HENRY16, HENRY_Z = (1.80, 1.95), 0.40
KIT16, KIT16_Z = (0.00, 1.70), 0.55
TBASKET = Vector((4.40, 3.12, 1.30))                   # kit's basket on the cooling table (near end)
BASKET_SCALE = 1.15
KIT17 = (3.15, 2.55)
KIT17B = (3.45, 3.40)
HENRY17 = (5.15, 2.80)
HENRY17A = (4.50, 2.55)                                # insert A: right behind the basket, seen from across the table
KIT18_A = (0.05, 3.00)
KIT18_B = (1.22, 1.50)
KIT19 = (2.80, 1.62)
KIT19_Z = -0.30                                        # only his head over the counter (chin on the counter top)
LOAF = dict(type="loaf", scale=0.9)
LOAF_UP = 0.145 * 0.9
SCALE_FOOT = Vector((2.4, 0.75, 1.25))

CAMS = {   # (shot, part) -> ((loc A, look A), (loc B, look B), lens)
    (16, "A"): (((0.90, -2.30, 1.75), (0.95, 1.9, 2.85)), ((0.90, -2.05, 1.75), (0.95, 1.9, 2.85)), 24.0),
    (16, "B"): (((1.30, -1.40, 1.80), (1.75, 1.9, 2.80)), ((1.32, -1.25, 1.80), (1.75, 1.9, 2.80)), 24.0),
    (17, "A"): (((4.10, 6.00, 2.05), (4.05, 3.00, 2.25)), ((4.10, 5.80, 2.05), (4.05, 3.00, 2.25)), 30.0),
    (17, "B"): (((4.25, 0.15, 2.45), (4.30, 3.20, 2.10)), ((4.25, 0.30, 2.45), (4.30, 3.20, 2.10)), 24.0),
    (18, "A"): (((0.60, 6.80, 2.70), (1.00, -6.0, 1.30)), ((0.62, 6.50, 2.65), (1.05, -6.0, 1.30)), 22.0),
    (18, "B"): (((1.80, -1.70, 2.30), (1.85, 1.30, 1.95)), ((1.80, -1.52, 2.30), (1.85, 1.30, 1.95)), 26.0),
    (19, "A"): (((1.55, 2.15, 2.00), (2.15, 0.75, 1.85)), ((1.66, 1.95, 1.98), (2.10, 0.75, 1.88)), 26.0),
    (19, "B"): (((2.45, -1.20, 1.95), (2.45, 1.5, 1.85)), ((2.45, -1.05, 1.95), (2.45, 1.5, 1.85)), 26.0),
}


def part(shot, g):
    return "A" if g < CUT[shot] else "B"


def cam_at(shot, g):
    pt = part(shot, g)
    (la, oa), (lb, ob), lens = CAMS[(shot, pt)]
    a = RANGES[shot][0] if pt == "A" else CUT[shot]
    b = CUT[shot] - 1 if pt == "A" else RANGES[shot][1]
    u = ez((g - a) / float(max(1, b - a)), "sine")
    return Vector(lerp(la, lb, u)), Vector(lerp(oa, ob, u)), lens


def small_scale_angle(g):
    """18: empty loaf pan up (-8); loaf on at G_PUT -> damped swing to about +1.  19: eases from +1 to -6 (the loaf side RISES)."""
    if g < G_PUT:
        return -8.0
    if g < S19:
        d = g - G_PUT
        return 1.0 - 9.0 * math.exp(-d / 7.0) * math.cos(d * 0.32)
    u = ez((g - (S19 + 4)) / 40.0, "sine") if g >= S19 + 4 else 0.0
    d = g - S19
    return lerp(1.0, -8.0, u) + 0.35 * math.sin(d * 0.25) * math.exp(-d / 30.0)


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
def henry16(g):
    talk = Q0 <= g <= Q1
    bounce = math.sin(g * 0.9)
    if g < Q0:     # belly laugh, eyes shut (laughing drawing, its own static mouth)
        p = dict(yaw=0.2, pitch=-0.4, expr="laughing", blink=2, fx=["tears"], head_roll=10 + 4 * bounce, lean=-6,
                 head_dy=0.03 + 0.02 * bounce, squash=(1.03 + 0.015 * bounce, 0.97 - 0.015 * bounce),
                 arm_r=dict(hand=(0.36, 1.1), bend=0.9), arm_l=dict(hand=(-0.4, 1.06), bend=0.9), legs="wide")
    else:          # smug, arms crossed high on the chest, talking
        p = dict(yaw=0.12, pitch=-0.35, expr="smug", head_roll=6 + 2 * math.sin(g * 0.3), lean=-5, legs="wide",
                 arm_r=dict(hand=(-0.30, 0.62), bend=-0.3, layer="top"), arm_l=dict(hand=(0.30, 0.66), bend=0.3, layer="top"),
                 gaze=(-0.3, 0.5))
        p["blink"] = blink(g, [1300, 1326])
    if talk:
        p["mouth"] = cast6.talk_mouth(g, 1.0, seed=16, hold=2)
    p["t"] = g / 30.0
    return p


def kit16(g):
    return dict(yaw=0.35, pitch=-0.35, expr="worried", head_roll=6, gaze=(0.85, -0.7), legs="narrow",
                arm_r=dict(hand=(0.18, 0.78), bend=0.5), arm_l=dict(hand=(-0.20, 0.80), bend=0.5),
                blink=blink(g, [1252, 1290, 1320]), t=g / 30.0)


def henry17(g):
    p = dict(yaw=-0.4, pitch=0.1, expr="unimpressed", head_roll=-4, lean=-3, legs="wide", gaze=(-0.8, 0.4),
             arm_r="akimbo", t=g / 30.0)
    if g >= CUT[17]:
        w = math.sin((g - CUT[17]) * 0.75)
        p.update(expr="angry", pitch=-0.15, gaze=(-0.85, 0.2), head_roll=-6 + 3 * w)
        p["arm_l"] = dict(hand=(-0.85 + 0.13 * w, -0.25), shape="point", bend=-0.7, stretch=1.25, layer="top")   # the wagging finger
        p["arm_r"] = dict(hand=(0.55, 0.30), bend=-0.6)
        p["prop_r"] = LOAF
    p["blink"] = blink(g, [1340, 1396])
    return p


def kit17(g):
    if g < G_SNATCH + 4:
        p = dict(yaw=0.35, pitch=0.25, expr="happy", head_roll=-3, gaze=(0.7, 0.5), legs="stand",
                 arm_r=dict(hand=(0.45, 0.62), bend=-0.5), arm_l=dict(hand=(-0.35, 0.8), bend=0.5))
    else:
        p = dict(yaw=0.30, pitch=0.30, expr="sad", head_roll=8, gaze=(0.8, -0.3), legs="narrow", squash=(1.02, 0.97),
                 arm_r=dict(hand=(0.15, 0.80), bend=0.4), arm_l=dict(hand=(-0.15, 0.80), bend=0.4))
    p["blink"] = blink(g, [1360, 1388, 1412])
    p["t"] = g / 30.0
    return p


def kit18(g):
    if g < CUT[18]:
        p = cast6.cycle("kit", (g - S18) / 18.0, "sneak", facing=-1,
                        base=dict(expr="smirk", prop_r=LOAF), arms="l")
        p["arm_r"] = dict(hand=(0.55, 0.30), bend=-0.5, stretch=1.3)
        p["gaze"] = (-0.8, 0.0) if (g // 14) % 2 == 0 else (0.8, 0.1)
        p["prop_r"] = LOAF
    else:
        look = -0.8 if g < 1478 else 0.75
        p = dict(yaw=0.40 if g >= 1478 else -0.30, pitch=0.2, expr="determined", head_roll=-4, gaze=(look, 0.3), legs="stand", lean=4,
                 arm_l=dict(hand=(-0.35, 0.80), bend=0.5))
        if g < G_PUT + 1:
            p["prop_r"] = LOAF
    p["blink"] = blink(g, [1450, 1480, 1508])
    p["t"] = g / 30.0
    return p


def kit19(g):
    p = dict(yaw=-0.25, pitch=-0.45, expr="neutral" if g < 1556 else "shocked", head_roll=-4, gaze=(-0.75, -0.8), legs="stand",
             arm_r=dict(hand=(0.35, 0.95), bend=0.5), arm_l=dict(hand=(-0.35, 0.95), bend=0.5))
    p["blink"] = blink(g, [1554])
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


class Take(C.Take):
    def __init__(self, quality="preview", preset="MORNING"):
        C.Take.__init__(self, "bakery", preset, quality=quality, lens=24.0, name="cam_s16")
        sd = os.path.join(TMP, "sprites_" + preset)
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.basket = None
        if preset == "MORNING":
            self.actors["henry"] = C.make_actor("henry", "henry", sd)
            items = [(cast6.basket_svg("bk%d" % n, loaves=n)[0], (-0.56, -0.06, 0.56, 0.72), 512) for n in (13, 12)]
            pngs = C.svg_pngs(items, os.path.join(TMP, "props"))
            self.basket = C.PropCard("basket", pngs, (-0.56, -0.06, 0.56, 0.72), scale=BASKET_SCALE, shadow=True)
            self.basket.put(TBASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=CAMS[(17, "A")][0][0])

    def loaf13(self):
        return self.basket.to_world((0.014, 0.114))

    def pan_loaf(self, g):
        """world centre of a loaf lying on the small balance's left (loaf) pan at film frame g (beam geometry from bakery_API:
        pivot z 2.2, arm 0.5, pans 0.62 below the beam ends; + angle = loaf pan down)."""
        a = math.radians(small_scale_angle(g))
        return Vector((SCALE_FOOT.x - 0.5 * math.cos(a), SCALE_FOOT.y, 2.2 - 0.5 * math.sin(a) - 0.62 + 0.10))

    # ---- per-shot keys
    def pose(self, shot, gs):
        kit = self.actors["kit"]
        henry = self.actors.get("henry")
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_at(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            steam = 0.3 if shot in (16, 17) else 0.0
            self.key_set(f, steam=steam, oven=1.0 if shot <= 17 else 0.7)
            hide_obj("opening_bundles", shot == 16 and g >= CUT[16], f)
            if shot in (16, 17):
                self.basket.show(None if shot == 16 else (0 if g <= G_SNATCH else 1), frame=f)
                if shot == 17:
                    self.basket.put(TBASKET + Vector((0, 0, 0.66 * BASKET_SCALE)), face=loc, frame=f)
                B.set_scale(0.0, frame=f)
                if shot == 16:
                    C.place(henry, f, HENRY16, HENRY_Z); C.place(kit, f, KIT16 if g < CUT[16] else (-0.9, 1.9), KIT16_Z)   # B: kit off frame left
                else:
                    if g < CUT[17]:
                        C.place(henry, f, HENRY17A, 0.40); C.place(kit, f, KIT17, 0.10)      # hidden steps: the basket rim at henry's belly
                    else:
                        C.place(henry, f, HENRY17, 0.0); C.place(kit, f, KIT17B, 0.0)
            else:
                B.set_scale(small_scale_angle(g), frame=f)
                B.set_scale_loaf(g > G_PUT, frame=f)
                if shot == 18:
                    if g < CUT[18]:
                        u = (g - S18) / float(CUT[18] - 1 - S18)
                        xy = lerp(KIT18_A, (1.45, 2.05), u)
                    else:
                        xy = KIT18_B
                    C.place(kit, f, xy, 0.0)
                else:
                    C.place(kit, f, KIT19, KIT19_Z)
                kit.card.hide_render = (shot == 19 and g < CUT[19])          # 19A: the ECU has no actor (kit's card would fill frame left)
                kit.card.keyframe_insert("hide_render", frame=f)
                fc = C._fcurve(kit.card, "hide_render")
                if fc is not None:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 16:
                henry.pose(f, henry16(g), camera=self.cam)
                kit.pose(f, kit16(g), camera=self.cam)
            elif shot == 17:
                p = henry17(g)
                hands = None
                if g < CUT[17]:
                    tgt = self.loaf13()
                    rest = tgt + Vector((-0.45, -0.85, -0.30))        # by his side, below the rim (hidden behind the basket)
                    grab = tgt + Vector((0, 0, 0.12))
                    keep = tgt + Vector((-0.30, -0.85, 0.35))         # held up at his chest, showing the pale loaf
                    if g < 1337:
                        pt, carry = rest, False
                    elif g <= G_SNATCH:
                        u = ez((g - 1337) / float(G_SNATCH - 1337))
                        pt, carry = (1 - u) ** 2 * rest + 2 * (1 - u) * u * (grab + Vector((-0.2, -0.3, 0.45))) + u * u * grab, False
                    else:
                        u = ez((g - G_SNATCH) / 10.0); pt, carry = grab.lerp(keep, u), True
                    if carry:
                        p["prop_l"] = LOAF
                        hands = C.held_on_palm(henry, self.cam, f, pt, up=LOAF_UP, side="l", bend=-0.4, stretch=1.4, layer="top")
                    else:
                        hands = {"l": {"hand": tuple(pt), "bend": -0.4, "stretch": 1.4, "layer": "top", "shape": "open"}}
                henry.pose(f, p, hands=hands, camera=self.cam)
                kit.pose(f, kit17(g), camera=self.cam)
            elif shot == 18:
                p = kit18(g)
                hands = None
                if g >= CUT[18] and g <= G_PUT + 6:
                    tgt = self.pan_loaf(g) if g > G_PUT else None
                    if g <= G_PUT:
                        # lift from the chest up and over onto the (still empty) pan
                        bpy_pan = self.pan_loaf(g)
                        start = Vector((KIT18_B[0] - 0.15, KIT18_B[1] - 0.1, 1.45))
                        u = ez((g - CUT[18]) / float(G_PUT - CUT[18]))
                        apex = (start + bpy_pan) / 2 + Vector((0, 0, 0.55))
                        pt = (1 - u) ** 2 * start + 2 * (1 - u) * u * apex + u * u * bpy_pan
                        hands = C.held_on_palm(kit, self.cam, f, pt, up=LOAF_UP, side="r", bend=-0.5, stretch=1.3)
                    else:
                        u = ez((g - G_PUT) / 6.0)
                        pt = tgt.lerp(Vector((KIT18_B[0] - 0.1, KIT18_B[1] - 0.1, 1.35)), u)
                        hands = {"r": {"hand": tuple(pt), "bend": -0.4, "stretch": 1.3}}
                elif g >= CUT[18]:
                    p["arm_r"] = dict(hand=(0.25, 0.70), bend=-0.5)
                _, inf = kit.pose(f, p, hands=hands, camera=self.cam)
                if os.environ.get("S16_DEBUG") and hands:
                    print("hand", g, [tuple(round(c, 2) for c in pt)], {k: (v.get("reached"), round(v.get("error", 0), 3)) for k, v in inf.items() if isinstance(v, dict)}, flush=True)
            else:
                kit.pose(f, kit19(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(kit, 448 if shot != 19 else 560)]
        if henry is not None:
            jobs.append((henry, 448))
        self.sprites_for(jobs, fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_at(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, part=part(shot, g), cam=[round(c, 3) for c in loc],
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f),
                    talk=bool(Q0 <= g <= Q1), scale_deg=round(small_scale_angle(g), 2) if shot >= 18 else 0.0)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    preset = PRESET[shots[0]]
    assert all(PRESET[s] == preset for s in shots), "one light preset per call: 16,17 or 18,19"
    if cmd in ("probe", "stills"):
        Tk = Take("preview", preset)
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
        C.final_loop(lambda q: Take(q, preset), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
