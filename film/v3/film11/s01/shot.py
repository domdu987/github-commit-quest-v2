#!/usr/bin/env python3
"""shot.py -- film 11 take s01 = shot 1 (barn_milking / A), g 0..77 (+ 6 out-handle g 78..83).
Sarah on her stool by Blossom holds out her blistered hand (mirrored: faces screen-left); Jenner (examine_hand) bends over it,
lancet in hand, takes pus from a blister into the small jar.  Slow push-in.
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C
from mathutils import Vector
D, actors, camrig, cast11, puppet, sprites = C.D, C.actors, C.camrig, C.cast11, C.puppet, C.sprites
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G0, G1 = 0, C.g_bound(2.60) - 1          # 0..77
H_OUT = 6
RANGE = (G0, G1 + H_OUT)
PRESET, LIGHT = "barn_milking", "A"

SARAH = Vector((-5.74, 11.87, 0.0))     # hip over the 3D stool (-5.6, 12.6), card 0.6 D in front of it
JEN = Vector((-7.45, 11.85, 0.0))
BLOSS = Vector((-3.9, 15.4, 0.0))

CAM0 = ((-1.4, 6.4, 1.55), (-5.4, 13.6, 1.45))
CAM1 = ((-3.3, 8.2, 1.65), (-6.3, 12.9, 1.55))


def cam_of(g):
    x = clamp((g - G0) / float(G1 + H_OUT - G0))
    u = 0.3 * ez(x) + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_sarah(g):
    p = dict(cast11.STORY11["sarah_show_hand"][1])
    p.update(stool=1, legs=cast11._sit("sarah"), mirror=True, yaw=0.45, t=g / 30.0,
             arm_r=dict(hand=(0.70, 0.86 + 0.015 * math.sin(g * 0.2)), bend=-0.2))
    p["blink"] = blink(g, [40, 71])
    return p


def pose_jen(g):
    p = dict(cast11.STORY11["jenner_examine_hand"][1])
    u = ez((g - 6) / 30.0)                                  # bends in over the hand
    p["lean"] = lerp(6, 14, u) + 0.8 * math.sin(g * 0.17)
    p["prop_r"] = dict(type="lancet", angle=lerp(25, 55, u))
    p["prop_l"] = "jar"
    dip = 0.5 + 0.5 * math.sin(max(0, g - 30) * 0.33) if g > 30 else 0.0
    p["arm_r"] = dict(hand=(lerp(0.60, 0.70, u), lerp(0.88, 0.97, u) + 0.05 * dip), bend=0.1, shape="open")
    p["arm_l"] = dict(hand=(lerp(0.52, 0.60, u), 1.10), bend=0.3)
    p["mouth"] = "flat"
    p["blink"] = blink(g, [22, 60])
    return p


def pose_cow(g):
    return dict(chew=g / 12.0, tail=0.5 * math.sin(g / 9.0), head_turn=0.5, ear=max(0.0, math.sin(g / 14.0)) * 0.6, blink=blink(g, [50]))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, quality=quality, name="cam_s01", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.sar = self.actors["sar"] = C.make_actor("sar", "sarah", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", sd, canvas=cast11.CANVAS11["blossom"])

    def pose(self, gs):
        for g in gs:
            f = bf(1, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            self.sar.place(f, tuple(SARAH), flip=True)
            self.jen.place(f, tuple(JEN))
            self.blo.place(f, tuple(BLOSS), flip=True)
        fr = [bf(1, g) for g in gs]
        for g in gs:
            f = bf(1, g)
            self.scene.frame_set(f)
            self.sar.pose(f, pose_sarah(g), camera=self.cam)
            self.blo.pose(f, pose_cow(g), camera=self.cam)
        self.sprites_for([(self.sar, 320), (self.blo, 256)], fr)
        for g in gs:
            f = bf(1, g)
            self.scene.frame_set(f)
            an = self.anch[("sar", f)]
            wx, wy = an["hand_l"]; tx, ty = an["blister_hand_l"]
            pt = (wx + 0.55 * (tx - wx), wy + 0.55 * (ty - wy))                 # on the blistered hand
            w = actors.local_to_world(self.sar, pt, f, camera=self.cam)
            u = ez((g - 6) / 30.0)
            dip = (0.5 + 0.5 * math.sin((g - 30) * 0.33)) if g > 30 else 0.0
            tip = Vector(w) + Vector((0.0, 0.0, 0.10 - 0.22 * dip))
            jar = Vector(w) + Vector((-0.20, 0.05, -0.55))
            p = pose_jen(g)
            for k in ("arm_r", "arm_l", "prop_r", "prop_l"):
                p.pop(k, None)
            p["prop_r"] = dict(type="lancet", angle=lerp(10, 40, u)); p["prop_l"] = "jar"
            self.jen.pose(f, p, hands={"r": {"tip": tuple(tip), "prop": "lancet", "angle": lerp(10, 40, u)}, "l": {"hand": tuple(jar)}}, camera=self.cam)
        self.sprites_for([(self.jen, 320)], fr)

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
