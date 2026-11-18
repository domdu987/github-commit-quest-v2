#!/usr/bin/env python3
"""shot.py -- film 11 take s04 = shot 4 (lane_high / A), g 237..317 (+6 handles each side).
High drift over the green: the crowd, pockmarked faces among them (a/b/c), a mother pulls a child (James) along.
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]    |    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C
from mathutils import Vector
D, actors, camrig, cast11, puppet, sprites = C.D, C.actors, C.camrig, C.cast11, C.puppet, C.sprites
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G0, G1 = C.g_bound(7.90), C.g_bound(10.60) - 1        # 237..317
H = 6
RANGE = (G0 - H, G1 + H)
PRESET, LIGHT = "lane_high", "A"
S11 = cast11.STORY11

CAM0 = ((3.0, -20.2, 6.6), (0.0, -12.4, 1.9))
CAM1 = ((-2.4, -20.4, 6.2), (-2.2, -12.4, 1.9))


def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0]))
    u = 0.2 * ez(x) + 0.8 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def idle(name, g, ph, **kw):
    p = dict(S11[name][1]); p.update(kw)
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 0.15 + ph)
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.10 + ph * 1.7)
    p["blink"] = blink(g, [250 + int(ph * 9), 290 + int(ph * 4)])
    p["t"] = g / 30.0
    return p


def walk(cast, g, facing, ph, base=None, speed=1.0):
    p = cast11.cycle(cast, g / 28.0 + ph, "walk", facing=facing, base=dict(dict(expr="neutral", mouth="flat"), **(base or {})), speed=speed)
    p["blink"] = blink(g, [255 + int(ph * 10), 300])
    return p


def mother_x(g): return -6.0 + 0.085 * (g - RANGE[0])


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s04", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        F = C.Fig
        J = cast11.STORY11["james_run"][1]
        def hold_pt(g, f, tk):                        # the joined hands: a point between mother and child, at hand height
            return Vector((mother_x(g) - 0.55, -15.5, 1.55))
        self.figs = [
            F("va", "villager_a", sd, lambda g: (-3.8, -12.6, 0), lambda g: idle("villager_a_whisper", g, 0.0), ppd=256),
            F("vb", "villager_b", sd, lambda g: (-2.3, -12.9, 0), lambda g: idle("villager_b_whisper", g, 1.1), flip=True, ppd=256),
            F("vc", "villager_c", sd, lambda g: (0.4, -11.3, 0), lambda g: idle("villager_c_point", g, 2.0), ppd=256),
            F("vd", "villager_d", sd, lambda g: (1.9, -13.5, 0), lambda g: idle("villager_d_laugh", g, 0.5), flip=True, ppd=256),
            F("ve", "villager_e", sd, lambda g: (-1.0, -10.3, 0), lambda g: idle("villager_e_whisper", g, 2.6), ppd=256),
            F("vm", "milkmaid2", sd, lambda g: (-5.4, -10.8, 0), lambda g: idle("milkmaid2_smile", g, 1.9, yaw=0.0), ppd=256),
            F("mo", "mother", sd, lambda g: (mother_x(g), -15.5, 0), lambda g: walk("mother", g, 1, 0.0, speed=0.85), ppd=256,
              hands=lambda g, f, tk: {"l": {"hand": tuple(hold_pt(g, f, tk))}}),
            F("ja", "james", sd, lambda g: (mother_x(g) - 1.15, -15.3, 0), lambda g: walk("james", g, 1, 0.45, base=dict(expr="worried"), speed=0.9), ppd=256,
              hands=lambda g, f, tk: {"r": {"hand": tuple(hold_pt(g, f, tk))}}),
        ]
        for fg in self.figs:
            self.actors[fg.name] = fg.actor

    def pose(self, gs):
        for g in gs:
            loc, look = cam_of(g)
            self.key_cam(bf(1, g), loc, look)
        C.pose_figs(self, self.figs, gs)

    def report(self, g):
        f = bf(1, g); self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render1(self, gs, out_dir, scale=1.0, samples=12):
        return C.Take.render(self, [bf(1, g) for g in gs], out_dir, scale=scale, samples=samples)


if __name__ == "__main__":
    cmd = sys.argv[1]
    spec = sys.argv[2]
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview")
        gs = [g for g in C.parse(spec) if RANGE[0] <= g <= RANGE[1]]
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            st = Tk.render1([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), [1], spec, {1: RANGE}, HERE, scale=scale, samples=samples)
