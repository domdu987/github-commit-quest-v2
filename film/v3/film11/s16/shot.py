#!/usr/bin/env python3
"""shot.py -- film 11 take s16: shot 16, "หกสัปดาห์ต่อมา หมอทำเรื่องที่บ้าที่สุด" g 983..1055 (+6 handle frames each side), transition_in dissolve 8.
garden_hut / light A.  Six weeks later: Jenner (jar up, lancet in the other hand) stands beside James, who sits brave on the stool at the hut door,
sleeve rolled; villagers peek over the flower beds behind.  Slow push-in.  Blister card on James's upper_arm_l.  Nobody speaks.
    python3 shot.py probe 16 a:b[:step] | stills 16 a:b[:step] <out_dir> [scale] [samples] | final 16 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
import cast11                                            # noqa: E402
from mathutils import Vector                             # noqa: E402

lerp, clamp, blink, ez, bf, u_of = C.lerp, C.clamp, C.blink, C.ez, C.bf, C.u_of
TMP = os.path.join(HERE, "work")
SHOT = 16
G0, G1 = C.g_bound(32.76), C.g_bound(35.20)              # 983, 1056
H = 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
DISSOLVE_IN = True
CUES = [{"frame": 983, "label": "garden, birds, a glass jar clinks in Jenner's hand", "kind": "ambience"}]
PRESET, LIGHT = "garden_hut", None

JAMES = (-8.0, -3.4)
JEN = (-6.3, -1.2)
PEEK = [("villager_b", (-8.3, 1.4)), ("villager_e", (-7.4, 2.8)), ("villager_a", (-9.8, 2.2))]
CAM0 = ((0.6, -6.4, 1.7), (-9.0, -0.6, 2.7))
CAM1 = ((-1.2, -5.6, 1.75), (-8.5, -1.4, 2.6))
STOOL_Z = 0.0


def cam_of(g):
    x = clamp((g - G0) / float(G1 - G0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def sore(f, pose, an):
    return C.sore_svg(an["upper_arm_r"], "blister")


def pose_james(g):
    p = dict(cast11.STORY11["james_brave"][1])
    p.update(mirror=True, t=g / 30.0, head_roll=-3 + 1.2 * math.sin(g * 0.08))
    p["blink"] = blink(g, [1000, 1031])
    return p


def pose_jen(g):
    p = dict(cast11.STORY11["jenner_jar_up"][1])
    k = math.sin(g * 0.1)
    p.update(mirror=True, prop_l=dict(type="lancet", angle=-70), t=g / 30.0, head_roll=3 * k, lean=1.0 * math.sin(g * 0.07))
    p["arm_r"] = dict(hand=(0.55, 0.2 + 0.03 * k), bend=-0.7)
    p["arm_l"] = dict(hand=(-0.5, 0.55 + 0.02 * k), bend=0.3)
    p["blink"] = blink(g, [992, 1024, 1046])
    return p


def pose_peek(i, g):
    nm = PEEK[i][0]
    p = dict(cast11.STORY11[nm + "_whisper"][1])
    p.update(mirror=True, t=g / 30.0, head_roll=p.get("head_roll", 0) + 2 * math.sin(g * 0.1 + i), lean=p.get("lean", 0) + 1.5 * math.sin(g * 0.08 + i))
    p["blink"] = blink(g, [990 + 13 * i, 1030 + 7 * i])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s16")
        sd = os.path.join(TMP, "sprites")
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.pk = [None] * len(PEEK)
        for i, (n, _) in enumerate(PEEK):
            self.pk[i] = self.actors["pk%d" % i] = C.make_actor("pk%d" % i, n, sd)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jam, f, JAMES, z=STOOL_Z, scale=C.SCALE["james"])
            C.place(self.jen, f, JEN, scale=C.SCALE["jenner"])
            for i, (n, xy) in enumerate(PEEK):
                C.place(self.pk[i], f, xy, scale=C.SCALE[n])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jam.pose(f, pose_james(g), camera=self.cam)
            self.jen.pose(f, pose_jen(g), camera=self.cam)
            for i in range(len(PEEK)):
                self.pk[i].pose(f, pose_peek(i, g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.jam, 192)], fr, overlays={"jam": sore})
        self.sprites_for([(self.jen, 192)] + [(a, 192) for a in self.pk], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

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
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
