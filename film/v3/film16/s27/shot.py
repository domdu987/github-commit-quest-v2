#!/usr/bin/env python3
"""shot.py -- film 16 take s27 = shot 27 (58.89-60.18 s): LINE station / DAY.  g 1767..1804 + 9 handle frames each side (g 1758..1813).
"ก่อนรถไฟตั้งชั่วโมง" -> the station platform by the rail: the train only now puffing in, late, from the right; four people on the platform
(messenger, worker, two congressmen) already waving the news.  Camera on the rail looking across at the platform: quick pull-back + slide
(still moving on the last frame: hard cut).  Waving hands animate at 3 Hz.  Nobody speaks.  No DOF, no text.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(58.89), C.g_bound(60.18)
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 - 1 + H_OUT
GS = list(range(GA, GB + 1))
PRESET, LIGHT = "line_rail", "DAY"
CAST = [("msg", "messenger_wave", (95.8, 17.8, 1.85), 0.0), ("wka", "worker_a_wave", (97.5, 18.5, 1.85), 0.7),
        ("cgb", "congressman_b_wave", (99.2, 17.8, 1.85), 1.9), ("cgc", "congressman_c_wave", (100.9, 18.5, 1.85), 3.1)]
LOOK_AT_TRAIN = {"msg", "wka", "cgc"}                 # eye-lines toward the arriving train (screen right); the congressman waves at the camera
G_WORD = C.cap_g("ก่อนรถไฟตั้ง")                  # 1770
CAMP = C.CamPath((95.0, 1.0, 2.9), (102.0, 19.6, 6.4), GA, GB, push=-0.12, slide_px=-25.0, rise_px=8.0, arc_deg_s=10.0, decay=0.3,
                 snaps=[dict(g=(G_WORD - 2, G_WORD + 12), k=1.7, peak=1.7, shift=(0.5, 0.1))])


def train_x(g, front0):
    return 128.0 - 29.0 * u_of(g, GA, GA + 38, kind="quad_out") - 1.5 * u_of(g, GA + 38, GB)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s27")
        self.key_cam(bf(GA), *CAMP.at(GA))
        self.scene.frame_set(bf(GA))
        self.act = {}
        for nm, key, mark, ph in CAST:
            cname = cast16.STORY16[key][0]
            self.act[nm] = self.actors[nm] = C.make_actor(nm, cname, os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose_of(self, nm, key, ph, g):
        p = dict(cast16.STORY16[key][1])
        t = g / 30.0
        ar = dict(p["arm_r"])
        hx, hy = ar["hand"]
        ar["hand"] = (hx + 0.12 * math.sin(2 * math.pi * 3.0 * t + ph), hy + 0.04 * math.sin(2 * math.pi * 1.5 * t + ph))
        p["arm_r"] = ar
        p["lean"] = p.get("lean", 0) + 2.0 * math.sin(2 * math.pi * 1.5 * t + ph)
        p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(2 * math.pi * 1.5 * t + ph + 1)
        p["t"] = t
        if nm in LOOK_AT_TRAIN:
            p["gaze"] = (1.0, -0.15)
            p["yaw"] = max(p.get("yaw", 0.3), 0.45)
        return p

    def pose(self, gs):
        front0 = TG.STATE["train"]["front0"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAMP.at(g))
            TG.set_train(train_x(g, front0), frame=f, speed=2.0)
            TG.set_pulse(-1.0, frame=f)
            bounce = 0.05
            for nm, key, mark, ph in CAST:
                m = mark
                hop = abs(math.sin(2 * math.pi * 1.5 * g / 30.0 + ph)) * bounce
                C.place(self.act[nm], f, (m[0], m[1], m[2] + hop))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for nm, key, mark, ph in CAST:
                self.act[nm].pose(f, self.pose_of(nm, key, ph, g), camera=self.cam)
        self.sprites_for([(a, 192) for a in self.act.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAMP.report(GS[:-1])
        for r in rows:
            print(r)
        print("longest run under 0.25 px/frame: %d" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
