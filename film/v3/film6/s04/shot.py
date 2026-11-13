#!/usr/bin/env python3
"""shot.py -- film 6 take s04: shot 4 only (plan 6.00-8.62 s = g 180..258) + 6 handle frames each side (g 174..264), bakery MORNING.

    shot 4  at the counter, from the street (as s01): the customer has gone, kit dusts his floury hands.
      A g 174..218  medium, a little right of s01's angle, slow drift left: Henry in the background by the oven weighing two loaves
                    in his hands (unaware, squinting at them).  On "เจ้านายเขา" (6.17 s, g 188) kit jerks a thumb back over his
                    shoulder at Henry with a smirk (g 186..204), then turns back to us.
      B g 219..264  punch-in on kit (framing change at g 219): he smiles into the lens and claps his floury hands (clap g 232):
                    a cartoon flour cloud bursts in front of his apron and drifts up / fades (g 232..264), kit grinning.
    Mouths: no quoted line -> static expression mouths only (smirk, happy, grinning).  Henry closed mouth.
NO depth of field anywhere (client rule).

    python3 shot.py stills 4 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 4 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(6.00), C.g_bound(8.62)       # 180, 259
H = 6
RANGES = {4: (G0 - H, G1 + H - 1)}              # 174 .. 264
G_CUT = 219                                     # framing change A -> B
G_THUMB = (186, 204)                            # "เจ้านายเขา" 6.17 s = g 188
G_CLAP = 232

KIT = (0.80, 1.48)
KIT_Z = 0.98
HENRY = (-1.70, 5.10)
CAM_A0 = ((1.55, -2.70, 2.70), (0.30, 2.6, 2.45))
CAM_A1 = ((1.30, -2.55, 2.70), (0.25, 2.6, 2.45))
CAM_B0 = ((1.02, -1.35, 2.80), (0.80, 1.6, 2.62))
CAM_B1 = ((0.98, -1.10, 2.80), (0.80, 1.6, 2.62))
LENS_A, LENS_B = 24.0, 26.0
STEAM = 0.3
CANVAS_KIT = (-1.5625, -3.875, 1.5625, 0.1875)


def cam(g):
    if g < G_CUT:
        u = ez((g - RANGES[4][0]) / float(G_CUT - 1 - RANGES[4][0]), "sine")
        a, b, lens = CAM_A0, CAM_A1, LENS_A
    else:
        u = ez((g - G_CUT) / float(RANGES[4][1] - G_CUT), "sine")
        a, b, lens = CAM_B0, CAM_B1, LENS_B
    return Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u)), lens


def flour_svg(uid, k):
    """cartoon flour cloud: crisp off-white puffs + specks, k 0..1 grows, drifts up, fades."""
    o = []
    op = (1 - k) ** 1.3 * min(1.0, k * 6 + 0.3)
    for i in range(11):
        a = i * 2.39
        d = (0.10 + 0.05 * (i % 4)) * (0.4 + 1.3 * k)
        cx = math.cos(a) * d * 1.3
        cy = math.sin(a) * d * 0.8 - 0.08 * k + 0.08 * k * k
        r = (0.09 + 0.04 * (i % 3)) * (0.5 + 1.1 * k)
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#fffaf0" opacity="%.3f"/>' % (cx, cy, r, 0.75 * op))
    for i in range(26):
        a = i * 1.7 + 0.4
        d = (0.15 + 0.03 * (i % 7)) * (0.5 + 1.8 * k)
        o.append('<circle cx="%.4f" cy="%.4f" r="%.4f" fill="#ffffff" opacity="%.3f"/>'
                 % (math.cos(a) * d * 1.4, math.sin(a) * d - 0.1 * k, 0.012 + 0.006 * (i % 3), 0.9 * op))
    return '<g id="%s">%s</g>' % (uid, "".join(o))


FLOUR_BOX = (-0.9, -1.1, 0.9, 0.6)
FLOUR_N = 33                                     # g 232 .. 264


def kit_pose(g):
    p = dict(yaw=0.10, pitch=0.05, expr="happy", head_roll=-2 + 2 * math.sin(g * 0.13), lean=3, gaze=(0.05, 0.0),
             legs="stand", t=g / 30.0)
    hands = {}
    if g < G_CUT:
        # dusting the hands: little pats in front of the apron bib
        ph = math.sin(g * 0.9)
        hands["r"] = dict(hand=(0.16 + 0.05 * ph, 0.95), bend=-0.4)
        hands["l"] = dict(hand=(-0.14 + 0.05 * ph, 0.98 - 0.03 * ph), bend=0.4)
        ut = ez((g - G_THUMB[0]) / 5.0) if g >= G_THUMB[0] else 0.0
        ub = ez((g - (G_THUMB[1] - 5)) / 5.0) if g >= G_THUMB[1] - 5 else 0.0
        u = ut * (1 - ub)
        if u > 0:
            hands["l"] = dict(hand=lerp((-0.14, 0.98), (-0.74, -0.10 + 0.03 * math.sin(g * 0.8)), u), bend=lerp(0.4, 1.0, u))
            p["fingers_l"] = 1 if u > 0.5 else 0
        p["yaw"] = lerp(0.10, -0.45, u)
        p["gaze"] = (lerp(0.05, -0.9, u), lerp(0.0, -0.1, u))
        p["head_roll"] += 6 * u
        if u > 0.3:
            p["expr"] = "smirk"
        p["blink"] = blink(g, [182, 212])
    else:
        # B: smile into the lens; hands apart (g 222..229), clap at G_CLAP, then hands held together, grin
        if g < G_CLAP - 4:
            hands["r"] = dict(hand=(0.40, 0.92), bend=-0.6)
            hands["l"] = dict(hand=(-0.40, 0.92), bend=0.6)
        elif g <= G_CLAP:
            u = ez((g - (G_CLAP - 4)) / 4.0)
            hands["r"] = dict(hand=(lerp(0.40, 0.03, u), 0.86), bend=-0.6)
            hands["l"] = dict(hand=(lerp(-0.40, -0.03, u), 0.86), bend=0.6)
        else:
            hands["r"] = dict(hand=(0.05, 0.86 - 0.02 * math.sin((g - G_CLAP) * 0.3)), bend=-0.5)
            hands["l"] = dict(hand=(-0.05, 0.86 - 0.02 * math.sin((g - G_CLAP) * 0.3)), bend=0.5)
        p["expr"] = "happy" if g < G_CLAP + 2 else "grinning"
        p["pitch"] = -0.05 + 0.08 * pulse(g, G_CLAP - 2, G_CLAP, G_CLAP + 6, 1.0)
        p["blink"] = blink(g, [G_CLAP, 256])
        p["yaw"] = 0.06
        p["gaze"] = (0.0, 0.0)
    return p, hands


def henry_pose(g):
    w = math.sin(g * 0.22)                         # weighing a loaf in each hand, up / down, squinting at them
    return dict(yaw=0.45, pitch=-0.20, expr="unimpressed", head_roll=-3 + 4 * w, gaze=(0.35 - 0.4 * w, -0.45),
                arm_l=dict(hand=(-0.55, -0.05 + 0.10 * w), bend=-0.6), prop_l="loaf",
                arm_r=dict(hand=(0.55, -0.05 - 0.10 * w), bend=0.6), prop_r="loaf",
                legs="wide", blink=blink(g, [196, 240]), t=g / 30.0)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=LENS_A, name="cam_s04")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd, CANVAS_KIT)
        self.actors["henry"] = C.make_actor("henry", "henry", sd)
        items = [(flour_svg("fl%d" % i, i / float(FLOUR_N - 1)), FLOUR_BOX, 360) for i in range(FLOUR_N)]
        self.flour = C.PropCard("flour", C.svg_pngs(items, os.path.join(TMP, "props")), FLOUR_BOX, scale=1.5, shadow=False)
        for ob in self.flour.cards:
            ob.visible_shadow = False

    def pose(self, shot, gs):
        kit, henry = self.actors["kit"], self.actors["henry"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(kit, f, KIT, KIT_Z)
            C.place(henry, f, HENRY, 0.0)
            for ob in henry.objects():          # B: henry is off frame left (head would be cut by the edge) -> not rendered
                if ob is None:
                    continue
                ob.hide_render = g >= G_CUT
                ob.keyframe_insert("hide_render", frame=f)
            self.key_set(f, steam=STEAM, oven=1.0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            p, hands = kit_pose(g)
            kit.pose(f, p, hands=hands, camera=self.cam)
            henry.pose(f, henry_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(kit, 512), (henry, 192)], fr)
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(g)
            k = g - G_CLAP
            if 0 <= k < FLOUR_N:
                self.scene.frame_set(f)
                w = actors.local_to_world(kit, (0.0, 0.98), f)
                pos = w + (loc - w).normalized() * 0.25
                self.flour.put(pos, face=loc, frame=f)
                self.flour.show(k, frame=f)
            else:
                self.flour.put(Vector((0, -50, 0)), face=loc, frame=f)
                self.flour.show(None, frame=f)

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look, lens = cam(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            Tk.pose(shot, gs)
            out = sys.argv[4]
            scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
            samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=1)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
