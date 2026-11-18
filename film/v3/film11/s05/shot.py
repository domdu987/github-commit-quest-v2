#!/usr/bin/env python3
"""shot.py -- film 11 take s05 = shot 5 (barn_wide / A), g 318..406 (+6 handles each side).
The twist: Sarah and milkmaid2 with clear rosy faces carry pails on yokes through the golden barn, smiling; cows in the stalls.
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
G0, G1 = C.g_bound(10.60), C.g_bound(13.58) - 1        # 318..406
H = 6
RANGE = (G0 - H, G1 + H)
PRESET, LIGHT = "barn_wide", "A"
SPD = 0.078                                              # D / frame along the barn floor (cycle speed 1.25 matches)
CAM0 = ((-3.4, 3.4, 2.7), (-6.0, 10.8, 1.2))
CAM1 = ((-0.8, 3.4, 2.7), (-2.2, 10.8, 1.2))


def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0]))
    u = 0.25 * ez(x) + 0.75 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def yoke_walk(cast, g, ph, y_off=0.0):
    base = dict(expr="happy", mouth="smile", yoke=1, milk=1, yoke_w=0.86)
    p = cast11.cycle(cast, g / 28.0 + ph, "walk", facing=1, base=base, arms=None, speed=1.25)
    p["yaw"] = 0.35
    p["arm_r"] = dict(hand=(0.66, 0.62), bend=0.3); p["arm_l"] = dict(hand=(-0.66, 0.62), bend=0.3)
    p["blink"] = blink(g, [340 + int(ph * 10), 385])
    p["t"] = g / 30.0
    return p


def pose_cow(g):
    return dict(chew=g / 12.0, tail=0.5 * math.sin(g / 9.0), head_turn=0.0, ear=max(0.0, math.sin(g / 14.0)) * 0.6, blink=blink(g, [350]))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s05", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        F = C.Fig
        cy = cast11.CANVAS11_YOKE
        self.figs = [
            F("sa", "sarah", sd, lambda g: (-9.3 + SPD * (g - G0 + H), 10.3, 0), lambda g: yoke_walk("sarah", g, 0.0), canvas=cy["sarah"], ppd=256),
            F("mm", "milkmaid2", sd, lambda g: (-11.2 + SPD * (g - G0 + H), 11.7, 0), lambda g: yoke_walk("milkmaid2", g, 0.5), canvas=cy["milkmaid2"], ppd=256),
            F("bl", "blossom", sd, lambda g: (-0.5, 18.6, 0), lambda g: pose_cow(g), flip=True, canvas=cast11.CANVAS11["blossom"], ppd=256),
        ]
        self.hide("fghen")
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
