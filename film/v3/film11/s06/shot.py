#!/usr/bin/env python3
"""shot.py -- film 11 take s06 = shot 6 (lane_wide / A), g 407..473 (+6 handles each side).
The towndoc (cane, tricorn) walks up to Jenner's gate, sees James's arm (James stands behind the picket fence, sleeve up, red dot),
laugh_big (head back); lip-sync from 14.84 narration s (g 449: the quote window starts, pose point_mock, mouth = talk_mouth(g)).
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
G0, G1 = C.g_bound(13.58), C.g_bound(15.80) - 1        # 407..473
H = 6
RANGE = (G0 - H, G1 + H)
PRESET, LIGHT = "lane_wide", "A"
S11 = cast11.STORY11
G_LIP0 = C.g_of(14.84)                                  # 448: lip-sync window opens (point_mock from the next frame)
G_STOP = 431
X_STOP, SPEED = -4.3, 0.095

CAM0 = ((2.4, -15.0, 1.7), (-2.6, -8.8, 2.3))
CAM1 = ((1.2, -14.8, 1.75), (-2.9, -8.8, 2.4))


def cam_of(g):
    x = clamp((g - RANGE[0]) / float(RANGE[1] - RANGE[0]))
    u = 0.25 * ez(x) + 0.75 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def doc_x(g): return X_STOP + SPEED * max(0, G_STOP - g)


def pose_doc(g):
    if g < G_STOP:
        p = cast11.cycle("towndoc", g / 28.0, "walk", facing=-1, base=dict(expr="smug", mouth="flat", prop_r=dict(type="cane", angle=96)), speed=1.3)
    elif g < G_LIP0 + 1:
        p = dict(S11["towndoc_laugh_big"][1])
        u = ez((g - G_STOP) / 6.0)
        p["lean"] = p.get("lean", 0) + 2.5 * math.sin(g * 0.55) * u        # shaking with laughter
        p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.43)
        p["t"] = g / 30.0
    else:
        p = dict(S11["towndoc_point_mock"][1])
        p["mouth"] = cast11.talk_mouth(g, 1.0)
        p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.2)
        p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, [415, 470])
    return p


def pose_james(g):
    p = dict(yaw=-0.25, expr="determined", mouth="smile", arm_l=dict(hand=(-0.62, 0.42), bend=-0.2, shape="open"), arm_r=dict(hand=(0.30, 1.0), bend=0.5), legs="stand")
    p["head_roll"] = 2.5 * math.sin(g * 0.12)
    p["lean"] = 1.0 * math.sin(g * 0.09)
    p["blink"] = blink(g, [425, 462])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s06", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        F = C.Fig
        self.figs = [
            F("jm", "james", sd, lambda g: (-1.5, -8.2, 0), lambda g: pose_james(g), ppd=256),
            F("td", "towndoc", sd, lambda g: (doc_x(g), -10.3, 0), lambda g: pose_doc(g), flip=lambda g: g < G_STOP, ppd=256),
        ]
        self.ov = C.sore_overlay("james", lambda f: 1.0)
        for fg in self.figs:
            self.actors[fg.name] = fg.actor

    def pose(self, gs):
        for g in gs:
            loc, look = cam_of(g)
            self.key_cam(bf(1, g), loc, look)
        C.pose_figs(self, self.figs, gs)
        self.figs[0].actor.render_sprites(256, frames=[bf(1, g) for g in gs], overlay=self.ov)

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
