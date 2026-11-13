#!/usr/bin/env python3
"""shot.py -- film 6 take s21: shots 21-22 (plan 54.64-61.57 s -> g 1639..1846) + 6-frame handles (g 1633..1852), bakery AFTERNOON.

    21a g 1633..1693  street side, low sun: the HOODED stranger walks in from screen-left along the shutter board and stops at the
                      counter ("บ่ายวันนั้นเอง ชายใส่ผ้าคลุมเดินเข้ามา"); Henry behind the counter, kit on his stool beside him.
    21b g 1694..1739  reverse, from inside the shop, low: the hooded man against the bright street, face in the hood's shadow (eye
                      glints only); one hand comes up, "a dozen, please" (no mouth: not a quoted line).
    22a g 1740..1801  low angle on Henry counting on his fingers (fingers_r 1..5, 1..5, 1..2 = twelve, one head bob per count,
                      g 1753..1798 on "ลุงนับให้ สิบสองก้อนพอดี"), squinting, smug.
    22b g 1802..1829  two-shot from the street: Henry shoos kit away (flapping open hand, angry, mouth CLOSED: not a quoted line);
                      kit shrinks, hops off his stool and backs off into the shop ("แล้วไล่เด็กไปหลังร้าน").
    22c g 1830..1852  inside by the right-wall racks: kit at the back of the shop glances sideways at the spare (paler) loaf on the
                      shelf beside him -- the idea lands (determined).  Out-handle continues.
Mouths: nobody speaks on screen (the quoted lines are shots 11, 16, 27).  NO depth of field (common.Take).

Internal shot id 21.   python3 shot.py probe|stills|final 21 a:b[:step] [out] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(54.64), C.g_bound(61.57)          # 1639, 1847
H = 6
RANGES = {21: (G0 - H, G1 + H - 1)}                  # 1633..1852
CUTS = [1694, 1740, 1802, 1830]                      # 21a | 21b | 22a | 22b | 22c


def part(g):
    return sum(g >= c for c in CUTS)                 # 0..4


G_ARRIVE = 1688
COUNT0, COUNT1 = C.g_of(58.33), C.g_of(59.72) + 3    # 1753 .. 1797: twelve counts
G_SHOO = 1806
G_GLANCE = 1838

# staging (bakery world D)
INSP_Y = -2.05
INSP_X0, INSP_X1 = -2.6, 0.05
HENRY = (1.25, 1.60)
KIT = (-0.55, 1.45); KIT_Z = 0.98
KIT_BACK = (5.00, 2.05)                              # 22c: at the back by the right-wall racks
SPARE = Vector((6.20, 3.40, 2.70))                   # the paler spare loaf on the right-wall shelf (z 2.7 board)

CAMS = [
    (((3.10, -6.40, 2.55), (-0.30, 0.90, 2.40)), ((2.80, -5.90, 2.50), (-0.30, 0.90, 2.40)), 24.0),   # 21a
    (((0.95, 0.95, 1.55), (0.15, -2.05, 3.05)), ((0.88, 0.80, 1.52), (0.15, -2.05, 3.10)), 22.0),   # 21b low, inside
    (((1.00, -2.90, 1.80), (1.20, 1.60, 2.80)), ((1.05, -2.55, 1.76), (1.20, 1.60, 2.85)), 30.0),   # 22a low on henry
    (((0.40, -3.75, 2.45), (0.35, 1.50, 2.35)), ((0.40, -3.45, 2.45), (0.35, 1.50, 2.35)), 24.0),   # 22b two-shot
    (((2.25, 1.42, 2.05), (6.20, 3.05, 2.20)), ((2.55, 1.55, 2.05), (6.20, 3.05, 2.22)), 24.0),     # 22c
]


def cam(g):
    k = part(g)
    a = ([RANGES[21][0]] + CUTS)[k]
    b = (CUTS + [RANGES[21][1] + 1])[k]
    u = ez((g - a) / float(b - a), "sine")
    (l0, t0), (l1, t1), lens = CAMS[k]
    return Vector(lerp(l0, l1, u)), Vector(lerp(t0, t1, u)), lens


# ----------------------------------------------------------------------------- poses
def insp_x(g):
    u = clamp((g - RANGES[21][0]) / float(G_ARRIVE - RANGES[21][0]))
    return lerp(INSP_X0, INSP_X1, ez(u, "out") if False else u * (1.0 - 0.0)) if g < G_ARRIVE else INSP_X1


def insp_pose(g):
    if g < G_ARRIVE:
        p = cast6.cycle("inspector", (g - RANGES[21][0]) / 24.0, "walk", facing=1, base=dict(expr="neutral", hood=1.0))
        p["yaw"] = 0.55
    else:
        p = dict(cast6.STORY6["inspector_hooded"][1])
        p["yaw"] = lerp(0.55, 0.30, ez((g - G_ARRIVE) / 8.0))
        p["head_roll"] = 2 * math.sin(g * 0.07)
        if g >= 1712:                                 # one hand comes up: "a dozen"
            u = ez((g - 1712) / 6.0) * (1 - ez((g - 1734) / 6.0))
            p["arm_r"] = dict(hand=(lerp(0.20, 0.55, u), lerp(0.95, 0.05, u)), bend=lerp(0.6, -0.6, u), shape="open" if u > 0.5 else None, stretch=1.2)
            if p["arm_r"]["shape"] is None:
                p["arm_r"].pop("shape")
    p["hood"] = 1.0
    p["t"] = g / 30.0
    return p


def fingers_at(g):
    if g < COUNT0:
        return 0
    n = min(12, 1 + int((g - COUNT0) * 12 / float(COUNT1 - COUNT0)))
    return n


def henry_pose(g):
    k = part(g)
    if k <= 1:
        p = dict(yaw=-0.40, pitch=-0.10, expr="unimpressed", head_roll=3 + 2 * math.sin(g * 0.08), gaze=(-0.6, -0.1),
                 arm_l=dict(hand=(-0.55, 0.25), bend=-0.6), arm_r="akimbo", legs="stand")
        if g > G_ARRIVE - 4:
            p.update(expr="smug", gaze=(-0.8, 0.0))
    elif k == 2 or (k == 3 and g < G_SHOO):
        p = dict(cast6.STORY6["henry_count"][1])
        n = fingers_at(g)
        p["fingers_r"] = ((n - 1) % 5) + 1 if n else 1
        ph = ((g - COUNT0) * 12 / float(COUNT1 - COUNT0)) % 1.0 if COUNT0 <= g <= COUNT1 else 0.0
        p["pitch"] = 0.30 + 0.12 * math.sin(math.pi * ph)
        p["yaw"] = -0.25
        p["arm_r"] = dict(hand=(0.48, -0.55 + 0.04 * math.sin(math.pi * ph)), bend=-0.8, stretch=1.3, layer="top")
        p["expr"] = "smug" if g > COUNT1 else "unimpressed"
        p["gaze"] = (0.35, 0.6) if g <= COUNT1 else (-0.4, 0.0)
    else:
        p = dict(cast6.STORY6["henry_shoo"][1])
        u = ez((g - G_SHOO) / 4.0)
        flap = math.sin((g - G_SHOO) * 0.9)
        p["arm_l"] = dict(hand=(lerp(-0.4, -0.86, u), -0.12 + 0.14 * flap * u), shape="open", bend=-0.8, stretch=1.3)
    p["mouth"] = "flat" if p.get("expr") in ("angry",) else p.get("mouth")
    if p.get("mouth") is None:
        p.pop("mouth", None)
    p["blink"] = blink(g, [1660, 1722, 1746, 1800, 1840])
    p["t"] = g / 30.0
    return p


def kit_place(g):
    """(xy, z) of kit"""
    if part(g) == 4:
        return KIT_BACK, 0.0
    if g < G_SHOO + 4:
        return KIT, KIT_Z
    u = ez((g - (G_SHOO + 4)) / 16.0)
    xy = (lerp(KIT[0], KIT[0] - 0.35, u), lerp(KIT[1], KIT[1] + 1.10, u))
    hop = 0.18 * math.sin(math.pi * min(1.0, u * 1.6)) if u < 0.62 else 0.0
    return xy, lerp(KIT_Z, 0.35, u) + hop


def kit_pose(g):
    k = part(g)
    if k <= 2 or g < G_SHOO:
        p = dict(yaw=0.40, pitch=0.05, expr="neutral", head_roll=-3 + 2 * math.sin(g * 0.11), gaze=(0.8, 0.2),
                 arm_l=dict(hand=(-0.40, 0.75), bend=0.5), arm_r=dict(hand=(0.35, 0.75), bend=-0.5), legs="stand")
        if g > COUNT0:
            p.update(expr="worried", gaze=(0.85, 0.0))
    elif k == 3:
        p = dict(cast6.STORY6["kit_scared"][1])
        u = ez((g - G_SHOO) / 6.0)
        p["yaw"] = lerp(0.4, -0.55, u)
        p["gaze"] = (0.7, 0.1)
        p.pop("mouth", None)
    else:
        p = dict(yaw=0.15, pitch=0.10, expr="sad", head_roll=-3, gaze=(-0.2, 0.3),
                 arm_l=dict(hand=(-0.35, 0.80), bend=0.5), arm_r=dict(hand=(0.35, 0.80), bend=-0.5), legs="stand")
        if g >= G_GLANCE:
            u = ez((g - G_GLANCE) / 5.0)
            p.update(yaw=lerp(0.15, -0.45, u), gaze=(lerp(0.2, -0.95, u), lerp(0.3, -0.45, u)), pitch=lerp(0.10, -0.15, u))
            if g >= G_GLANCE + 5:
                p["expr"] = "determined"
    p["blink"] = blink(g, [1670, 1735, 1790, G_GLANCE + 3])
    p["t"] = g / 30.0
    return p


def pale_png(src):
    """the 13th loaf is the PALER one: blend the crust colours toward cream (ink lines stay dark)."""
    import numpy as np
    from PIL import Image
    out = src[:-4] + "_pale.png"
    if not os.path.exists(out):
        im = np.asarray(Image.open(src).convert("RGBA")).astype(np.float32)
        rgb, al = im[..., :3], im[..., 3:]
        lum = rgb.mean(axis=2, keepdims=True)
        k = np.clip((lum - 60.0) / 80.0, 0, 1) * 0.55
        rgb = rgb * (1 - k) + np.array([255, 238, 196], np.float32) * k
        Image.fromarray(np.concatenate([rgb, al], 2).clip(0, 255).astype(np.uint8)).save(out)
    return out


CANVAS_INSP = (-1.6875, -4.875, 1.6875, 0.125)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "AFTERNOON", quality=quality, lens=24.0, name="cam_s21")
        sd = os.path.join(TMP, "sprites")
        self.actors["inspector"] = C.make_actor("inspector", "inspector", sd)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        self.actors["kit"] = C.make_actor("kit", "kit", sd)
        svg = cast6.loaf_svg("spare", r=0.24, seed=13, tint="#fff1cf")
        png = C.svg_pngs([(svg, (-0.28, -0.19, 0.28, 0.16), 900)], os.path.join(TMP, "props"))
        png = [pale_png(png[0])]
        self.spare = C.PropCard("spare", png, (-0.28, -0.19, 0.28, 0.16), scale=1.0, shadow=True)
        self.spare.put(SPARE + Vector((0, 0, 0.13)), face=CAMS[4][0][0])

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(g)
            self.key_cam(f, loc, look, lens=lens)
            k = part(g)
            C.place(A["inspector"], f, (insp_x(g), INSP_Y), 0.0)
            xy, z = kit_place(g)
            C.place(A["kit"], f, xy, z)
            C.place(A["henry"], f, HENRY, 0.0)
            vis = dict(inspector=k in (0, 1), henry=k in (0, 2, 3), kit=k in (0, 3, 4))
            for n, a in A.items():
                a.card.hide_render = not vis[n]
                a.card.keyframe_insert("hide_render", frame=f)
            self.key_set(f, steam=0.0 if k == 1 else 0.35, oven=1.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            A["inspector"].pose(f, insp_pose(g), camera=self.cam)
            A["henry"].pose(f, henry_pose(g), camera=self.cam)
            A["kit"].pose(f, kit_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(A["inspector"], 400), (A["henry"], 400), (A["kit"], 400)], fr)
        for a in A.values():                      # hidden cards must stay hidden through the constant keys
            for fc in (C._fcurve(a.card, "hide_render"),):
                if fc is not None:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam(g)
        v = look - loc
        return dict(shot=shot, g=g, part=part(g), cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f),
                    fingers=fingers_at(g),
                    spare_px=[round(x, 1) for x in C.render.world_to_screen(self.cam, tuple(SPARE), f)[:2]])

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
