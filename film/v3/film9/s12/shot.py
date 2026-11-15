#!/usr/bin/env python3
"""shot.py -- film 9 take s12: shots 12 + 13 (plan 29.57-34.70 s = g 887..1040, handles g 881..886 and 1041..1046), the false payoff.
One location (wall_site, RAIN; heights lin 20 / general 26 = month 2), one build (two_sections), two custom cameras, cut at g 960:

    id 1  g 881..959   shot 12, the first rain: medium on Lin at the foot of his rice-mortar section.  The rice mortar behind him turns
                       soft and wet (set_mortar_wet 0.55 -> 1.0: glossy joints, milky runs over the bricks).  He looks at it, then up at
                       the rain, worried, palm out (on "ยังนิ่ม อยู่เลย").  Slow push in.
    id 2  g 960..1046  shot 13, on top of the general's section in the rain: the general shouts and laughs, pointing down at the
                       site (screen-right), the other fist up; lip-sync on his quote g 963..1039 (~32.0-34.6 s), mouth still before /
                       after.  Slow push in + drift.
Rain streaks (set_rain 1, compositor) keyed every frame; flames, steam keyed every frame.  NO depth of field (c9.Take).
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, cast9 = C.B, C.actors, C.cast9
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(29.57)              # 887
G_CUT = C.g_bound(32.00)           # 960
G_END = C.g_bound(34.70)           # 1041
H = 6
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G_END + H - 1)}
LIP = (C.g_of(32.0), C.g_of(34.6) - 2)     # 963..1039: the general's quote (mouth moves only here)
G_LOOKUP = (C.g_of(30.42) - 4, C.g_of(30.42) + 10)   # 912..926: from the soft mortar up to the rain
LIGHT = "RAIN"
HEIGHTS = [("lin", 20), ("general", 26)]

LIN = Vector((-1.9, 8.3, 0.0))
GEN = Vector((8.0, 2.4, 0.0))
CAM_A0 = ((0.2, 16.6, 4.5), (-2.6, 5.0, 3.1))
CAM_A1 = ((-0.6, 15.0, 4.3), (-2.8, 5.0, 3.1))
LENS_A = 24.0
CAM_B0 = ((15.6, 2.5, 16.4), (1.0, 3.6, 14.7))
CAM_B1 = ((13.6, 3.2, 16.1), (1.0, 3.8, 14.8))
LENS_B = 20.0
PPD = {1: 304, 2: 320}


def u_lin(x):
    x = clamp(x)
    return 0.35 * ez(x, "sine") + 0.65 * x


def cam_of(shot, g):
    a, b = RANGES[shot]
    u = u_lin((g - a) / float(b - a))
    c0, c1 = (CAM_A0, CAM_A1) if shot == 1 else (CAM_B0, CAM_B1)
    return Vector(lerp(c0[0], c1[0], u)), Vector(lerp(c0[1], c1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def wet_of(g):
    return lerp(0.55, 1.0, clamp((g - RANGES[1][0]) / 60.0))


def pose_lin(g):
    """first looks at the soft mortar beside him (screen-right, down), then up into the rain, worried, palm out."""
    p = dict(cast9.STORY9["lin_rain"][1])
    up = u_of(g, *G_LOOKUP)
    p["pitch"] = lerp(0.35, -1.1, up) + 0.05 * math.sin(g * 0.17)
    p["gaze"] = (lerp(0.9, 0.2, up) + 0.1 * up * math.sin(g * 0.13), lerp(0.6, -1.0, up))
    p["yaw"] = lerp(0.55, 0.3, up)
    p["head_roll"] = lerp(2.0, -6.0, up) + 1.5 * math.sin(g * 0.11)
    p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.45, 0.62, up), lerp(0.55, 0.05, up) + 0.02 * math.sin(g * 0.3)))
    p["lean"] = lerp(6.0, -3.0, up) + math.sin(g * 0.09)
    p["expr"] = "worried"
    p["blink"] = blink(g, [900, 940])
    p["t"] = g / 30.0
    return p


def pose_gen(g):
    p = dict(cast9.STORY9["general_rain_shout"][1])
    if LIP[0] <= g <= LIP[1]:
        p["mouth"] = cast9.talk_mouth(g, 1.0)
    else:
        p["mouth"] = "talk_b"                       # held open shout shape, not moving outside the quote
    k = math.sin(g * 0.7)
    p["squash"] = (1.0 + 0.015 * k, 1.0 - 0.015 * k)
    p["head_roll"] = 6 + 3 * math.sin(g * 0.21)
    p["pitch"] = -0.4 + 0.08 * math.sin(g * 0.27)
    p["lean"] = -3 + 2.0 * math.sin(g * 0.17)
    p["arm_l"] = dict(p["arm_l"], hand=(-0.95, -0.3 + 0.08 * math.sin(g * 0.5)))
    p["arm_r"] = dict(p["arm_r"], hand=(1.0, 0.2 + 0.05 * math.sin(g * 0.37)))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "wall_site", "two_sections", quality=quality, lens=LENS_A, name="cam_s12", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", sd)
        self.gen = self.actors["gen"] = C.make_actor("gen", "general", sd)

    def pose(self, shot, gs):
        ztop = W.top_z("general", 26)
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS_A if shot == 1 else LENS_B)
            self.key_set(f, steam=1.0, rain=1.0, mortar_wet=wet_of(g) if shot == 1 else 1.0, wall_height=HEIGHTS)
            if shot == 1:
                C.place(self.lin, f, LIN); C.place(self.gen, f, (40.0, 40.0, -50.0))
            else:
                C.place(self.gen, f, GEN, z=ztop); C.place(self.lin, f, (40.0, 41.0, -50.0))
            self.lin.card.hide_render = shot != 1; self.lin.card.keyframe_insert("hide_render", frame=f)
            self.gen.card.hide_render = shot != 2; self.gen.card.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                self.lin.pose(f, pose_lin(g), camera=self.cam)
            else:
                self.gen.pose(f, pose_gen(g), camera=self.cam)
        self.sprites_for([(self.lin if shot == 1 else self.gen, PPD[shot])], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f),
                    mortar_wet=round(wet_of(g), 3) if shot == 1 else 1.0, lip=bool(shot == 2 and LIP[0] <= g <= LIP[1]))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
