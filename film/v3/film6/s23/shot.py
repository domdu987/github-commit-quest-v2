#!/usr/bin/env python3
"""shot.py -- film 6 take s23: shot 23 (plan 61.57-64.50 s -> g 1847..1934) + 6-frame handles (g 1841..1940), market AFTERNOON.

    23a g 1841..1886  eye level in the square: the HOODED man strides out of the crowd toward us, to the square centre
                      ("ชายคนนั้น เดินไปกลางตลาด"); four townsfolk in his way step aside left and right (the crowd parts), turning
                      their heads after him; pillory behind at left, the big balance at right.
    23b g 1887..1915  low angle, medium: he stops, plants his feet and throws back the hood with both hands ("ถอดผ้าคลุมออก",
                      g 1896): pose key hood 1 -> 0 over g 1897..1909, then a blink (g 1913..1915).
    23c g 1916..1940  HARD CUT on the blink to a closer, lower angle: inspector_royal (hood down, royal tabard with three lions,
                      gold chain of office), stern, one hand raised; townsfolk behind gape ("เขาคือ ผู้ตรวจ...").
Mouths: no quoted line -> static mouths only.  NO depth of field (common.Take).

Internal shot id 23.   python3 shot.py probe|stills|final 23 a:b[:step] [out] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(61.57), C.g_bound(64.50)          # 1847, 1935
H = 6
RANGES = {23: (G0 - H, G1 + H - 1)}                  # 1841..1940
CUTS = [1887, 1916]
G_STOP = 1890
G_HOOD = (1898, 1911)
G_BLINK = (1913, 1915)


def part(g):
    return sum(g >= c for c in CUTS)


INSP0, INSP1 = (-0.30, 8.30), (0.00, 4.60)
CROWD = {   # name: (cast, start xy, parted xy, side)
    "woman1": ("woman1", (-0.95, 5.90), (-2.55, 5.55), -1),
    "man1": ("man1", (0.80, 6.30), (2.30, 6.00), 1),
    "woman1b": ("woman1", (1.25, 4.70), (2.70, 4.10), 1),
    "man1b": ("man1", (-1.10, 7.40), (-2.70, 7.70), -1),
}
BACK = {"woman1": (-1.75, 5.40), "man1": (1.80, 5.70), "woman1b": (-2.70, 6.60)}
PART_AT = {"man1b": 1846, "woman1": 1856, "man1": 1853, "woman1b": 1866}

CAMS = [
    (((0.35, -0.90, 1.95), (-0.30, 8.00, 2.70)), ((0.30, -0.35, 1.92), (-0.25, 8.00, 2.75)), 24.0),   # 23a
    (((1.05, 0.70, 1.95), (0.00, 4.60, 2.90)), ((0.95, 1.00, 1.93), (0.00, 4.60, 2.95)), 24.0),     # 23b low medium
    (((0.45, 2.15, 1.55), (0.00, 4.60, 3.05)), ((0.42, 2.30, 1.53), (0.00, 4.60, 3.08)), 26.0),     # 23c lower, closer
]


def cam(g):
    k = part(g)
    a = ([RANGES[23][0]] + CUTS)[k]
    b = (CUTS + [RANGES[23][1] + 1])[k]
    u = ez((g - a) / float(b - a), "sine")
    (l0, t0), (l1, t1), lens = CAMS[k]
    return Vector(lerp(l0, l1, u)), Vector(lerp(t0, t1, u)), lens


def insp_xy(g):
    u = clamp((g - RANGES[23][0]) / float(G_STOP - RANGES[23][0]))
    u = ez(u, "quad_out") * 0.25 + u * 0.75
    return lerp(INSP0[0], INSP1[0], u), lerp(INSP0[1], INSP1[1], u)


def insp_pose(g):
    if g < G_STOP:
        p = cast6.cycle("inspector", (g - RANGES[23][0]) / 18.0, "walk", facing=1, base=dict(expr="neutral", hood=1.0))
        p["yaw"] = 0.12
        p["hood"] = 1.0
    elif g < CUTS[1]:
        p = dict(cast6.STORY6["inspector_hood_drop"][1])
        u = ez((g - G_HOOD[0]) / float(G_HOOD[1] - G_HOOD[0])) if g >= G_HOOD[0] else 0.0
        p["hood"] = 1.0 - 0.85 * u            # ends at 0.15 (the hood slid back), never the bare hooded head: cut on the blink
        ua = ez((g - (G_HOOD[0] - 6)) / 6.0)
        p["arm_r"] = dict(hand=(lerp(0.20, 0.40 - 0.25 * u, ua), lerp(0.95, -0.55 - 0.25 * u, ua)), bend=-1.0, stretch=1.3)
        p["arm_l"] = dict(hand=(lerp(-0.18, -0.40 + 0.25 * u, ua), lerp(0.98, -0.52 - 0.25 * u, ua)), bend=-1.0, stretch=1.3)
        if g > G_HOOD[1]:
            p["arm_r"] = dict(hand=(0.45, 0.30), bend=-0.5, stretch=1.2)
            p["arm_l"] = dict(hand=(-0.45, 0.30), bend=-0.5, stretch=1.2)
        p["expr"] = "determined"
        p["pitch"] = lerp(0.10, -0.25, u)
        p["blink"] = 1 if g == G_BLINK[0] or g == G_BLINK[1] else (2 if G_BLINK[0] < g < G_BLINK[1] else 0)
    else:
        p = dict(cast6.STORY6["inspector_reveal"][1])
        u = ez((g - CUTS[1]) / 10.0)
        p["arm_r"] = dict(hand=(0.60, lerp(0.10, -0.20, u)), shape="open", bend=-0.6, stretch=1.2)
        p["pitch"] = -0.45 + 0.04 * math.sin((g - CUTS[1]) * 0.25)
        p["blink"] = blink(g, [1934])
    p["t"] = g / 30.0
    return p


def crowd_xy(n, g):
    cast_, a, b, side = CROWD[n]
    u = ez((g - PART_AT[n]) / 12.0) if g >= PART_AT[n] else 0.0
    return lerp(a[0], b[0], u), lerp(a[1], b[1], u), u


def crowd_pose(n, g):
    cast_, a, b, side = CROWD[n]
    _, _, u = crowd_xy(n, g)
    if 0.0 < u < 1.0:
        p = cast6.cycle(cast_, (g - PART_AT[n]) / 14.0, "walk", facing=side, base=dict(expr="shocked"))
    else:
        p = dict(yaw=0.0, pitch=0.0, expr="neutral" if u == 0 else "shocked", legs="stand",
                 arm_l=dict(hand=(-0.40, 0.75), bend=0.5), arm_r=dict(hand=(0.40, 0.75), bend=-0.5))
    look = -0.6 * side if u > 0 else 0.15 * side      # after parting: heads turned toward the inspector in the middle
    p["yaw"] = look
    p["gaze"] = (look, 0.1)
    if part(g) >= 2:
        p["expr"] = "stunned"
        p["arm_r"] = dict(hand=(0.30, 0.10), bend=-0.6, shape="open", stretch=1.1)
    p["head_roll"] = 3 * math.sin(g * 0.09 + len(n))
    p["blink"] = blink(g, [1860 + 7 * len(n), 1925 - len(n)])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=24.0, name="cam_s23")
        sd = os.path.join(TMP, "sprites")
        self.actors["inspector"] = C.make_actor("inspector", "inspector", sd)
        self.actors["royal"] = C.make_actor("royal", "inspector_royal", sd)
        for n, (cast_, a, b, s) in CROWD.items():
            self.actors[n] = C.make_actor(n, cast_, sd)

    def pose(self, shot, gs):
        A = self.actors
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam(g)
            self.key_cam(f, loc, look, lens=lens)
            k = part(g)
            ix, iy = insp_xy(g)
            C.place(A["inspector"], f, (ix, iy))
            C.place(A["royal"], f, (ix, iy))
            for n in CROWD:
                x, y, u = crowd_xy(n, g)
                if k >= 1:                            # after the cut: the parted crowd regrouped behind him (low-angle staging)
                    x, y = BACK.get(n, (x, y))
                C.place(A[n], f, (x, y))
            for n, a in A.items():
                vis = (n != "royal") if k < 2 else (n != "inspector")
                if (k >= 1 and n == "man1b") or (k == 2 and n in CROWD):
                    vis = False
                a.card.hide_render = not vis
                a.card.keyframe_insert("hide_render", frame=f)
            self.key_set(f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            pi = insp_pose(g)
            A["inspector" if part(g) < 2 else "royal"].pose(f, pi, camera=self.cam)
            A["royal" if part(g) < 2 else "inspector"].pose(f, dict(cast6.STORY6["inspector_reveal"][1]) if part(g) < 2
                                                            else dict(cast6.STORY6["inspector_hooded"][1]), camera=self.cam)
            for n in CROWD:
                A[n].pose(f, crowd_pose(n, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 400 if n in ("inspector", "royal") else 256) for n, a in A.items()], fr)
        for a in A.values():
            fc = C._fcurve(a.card, "hide_render")
            if fc is not None:
                for kp in fc.keyframe_points:
                    kp.interpolation = "CONSTANT"

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam(g)
        v = look - loc
        return dict(shot=shot, g=g, part=part(g), cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))

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
