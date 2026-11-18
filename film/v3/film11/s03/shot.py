#!/usr/bin/env python3
"""shot.py -- film 11 take s03 = shot 3 (lane_wide / A), g 161..236 (+6 handles each side).
1796 village lane: pockmarked villagers (villager_a/b/c) walk and whisper; the camera tracks along the lane (side-on from the green).
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
G0, G1 = C.g_bound(5.37), C.g_bound(7.90) - 1        # 161..236
H = 6
RANGE = (G0 - H, G1 + H)
PRESET, LIGHT = "lane_wide", "A"
SP = 0.07                                              # walking speed D / frame

CAM0 = ((30.0, -15.6, 1.6), (26.0, -9.0, 2.2))
CAM1 = ((21.0, -15.6, 1.65), (17.0, -9.0, 2.25))


def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0]))
    u = 0.15 * ez(x) + 0.85 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


S11 = cast11.STORY11


def whisper(name, mirror, g, ph):
    p = dict(S11[name + "_whisper"][1])
    p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(g * 0.16 + ph)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.11 + ph)
    p["blink"] = blink(g, [170 + int(ph * 7), 215 + int(ph * 5)])
    p["t"] = g / 30.0
    return p


def walker(cast, g, facing, ph, base=None, speed=1.0):
    p = C.cast11.cycle(cast, g / 28.0 + ph, "walk", facing=facing, base=dict(expr="neutral", mouth="flat", **(base or {})), speed=speed)
    p["blink"] = blink(g, [180 + int(ph * 20), 222])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s03", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        F = C.Fig
        self.figs = [
            F("wa", "villager_a", sd, lambda g: (22.4, -9.2, 0), lambda g: whisper("villager_a", False, g, 0.0), flip=False, ppd=256),
            F("wb", "villager_b", sd, lambda g: (23.9, -9.5, 0), lambda g: whisper("villager_b", True, g, 1.3), flip=True, ppd=256),
            F("wc", "villager_c", sd, lambda g: (26.8 - 0.13 * (g - 155), -10.2, 0), lambda g: walker("villager_c", g, -1, 0.0, speed=1.85), flip=True, ppd=256),
            F("wd", "villager_d", sd, lambda g: (31.0 - 0.10 * (g - 155), -8.7, 0), lambda g: walker("villager_d", g, -1, 0.4, speed=1.45), flip=True, ppd=256),
            F("we", "villager_e", sd, lambda g: (14.0 + 0.075 * (g - 155), -10.6, 0), lambda g: walker("villager_e", g, 1, 0.7, speed=1.1), flip=False, ppd=256),
            F("wf", "mother", sd, lambda g: (11.5 + 0.075 * (g - 155), -9.9, 0), lambda g: walker("mother", g, 1, 0.2, base=dict(yaw=0.6), speed=1.1), flip=False, ppd=256),
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
