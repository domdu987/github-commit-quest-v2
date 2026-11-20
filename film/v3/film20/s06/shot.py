#!/usr/bin/env python3
"""shot.py -- film 20 take s06 = shot 6, CAFE cafe_wide (1887, tower stub in the window).  Artists crowd round the marble table, outraged.
Shot 6 = g 404..465 (13.47-15.53 s); dissolved IN (DIS 13): in-handle 9 frames g 395..403; cut out at 466: out-handle 4 frames g 466..469.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples] | camreport
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(13.47), C.g_bound(15.53)       # 404, 466
H_IN, H_OUT = 9, 4                                 # DIS 13 -> 13/2 + 2 = 9 (rounded up); cut side 4
GA, G_LAST = G0 - H_IN, G1 + H_OUT - 1             # 395 .. 469
GS = list(range(GA, G_LAST + 1))
G_COUNT = C.cap_g("สี่สิบกว่าคน")                  # 444: strongest word -> snap + arms up
SNAP = (G_COUNT - 2, G_COUNT + 13)
LIGHT, PRESET, PPD = "DAY", "cafe_wide", 144

ART = [("art1", "painter20", "artist_1"), ("art2", "composer20", "artist_2"), ("art3", "poet20", "artist_3"), ("art4", "architect20", "artist_4")]
SPOT = {"art1": (-2.3, 6.9), "art2": (-0.9, 8.2), "art3": (0.5, 6.7), "art4": (-1.2, 5.9), "wtr": (2.0, 7.6)}   # stage (D, world x/y): a tight group, heads staggered
PROP = {"art1": dict(type="news20", angle=-25), "art2": None, "art3": dict(type="news20", angle=20), "art4": dict(type="news20", angle=-35)}
YAW = {"art1": 0.35, "art2": 0.1, "art3": -0.35, "art4": 0.2}            # toward the table centre (negative = faces screen-left: mirror)
PHASE = {"art1": 0.0, "art2": 1.7, "art3": 3.1, "art4": 4.4}


def cam_path(A):
    c = Vector(eval(os.environ.get("CAML", "(0.2, 0.5, 2.3)")))
    subj = Vector((-0.6, 6.7, 2.4))
    return C.CamPath(c, subj, GA, G_LAST, push=float(os.environ.get("PUSH","0.08")), slide_px=float(os.environ.get("SLIDE","-40")), tilt0=float(os.environ.get("TILT", "3")), tilt_deg_s=0.0, decay=0.25,
                     snaps=[dict(g=SNAP, k=1.2, peak=1.7, shift=(0.1, 0.0), tilt=0.0)])


def cam_path_static():
    import int20
    return cam_path(None)


def pose_of(k, cast, g):
    base = dict(cast20.STORY20[cast + "_outraged"][1])
    t = g / 30.0
    ph = PHASE[k]
    w = 2 * math.pi * 1.7
    up = u_of(g, SNAP[0], SNAP[1])                    # arms swing higher on the count
    arm = dict(base["arm_r"])
    hx, hy = arm["hand"]
    arm["hand"] = (hx + 0.10 * math.sin(w * t + ph), hy + 0.12 * math.cos(w * t + ph) + 0.12 * up)
    base["arm_r"] = arm
    if PROP[k]:
        pr = dict(PROP[k]); pr["angle"] = pr["angle"] + 22 * math.sin(w * t + ph + 0.8)
        base["prop_r"] = pr
    base["yaw"] = abs(YAW[k])
    base["head_roll"] = base.get("head_roll", 0) + 4 * math.sin(w * t * 0.5 + ph)
    base["lean"] = 2.0 * math.sin(w * t * 0.5 + ph + 1.0)
    base["squash"] = (1.0 + 0.012 * math.sin(2 * math.pi * 3.0 * t + ph), 1.0 - 0.012 * math.sin(2 * math.pi * 3.0 * t + ph))
    base["blink"] = blink(g, [8 + 17 * int(ph) + 400, 440 + 3 * int(ph)])
    base["t"] = t
    return base


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s06")
        self.path = cam_path(self.A)
        self.key_cam(bf(GA), *self.path.at(GA))
        self.scene.frame_set(bf(GA))
        self.cafe = self.A["hooks"]
        for k, cast, mark in ART:
            self.actors[k] = C.make_actor(k, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.7))
        self.waiter = self.actors["wtr"] = C.make_actor("wtr", "waiter", os.path.join(WORK, "sprites"), cam=self.cam,
                                                        contact=dict(width=1.2, depth=0.5, opacity=0.7))

    def pose(self, gs):
        M = self.A["marks"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            for k, cast, mark in ART:
                m = M[mark]
                self.actors[k].place(f, (SPOT[k][0], SPOT[k][1], m[2]), scale=1.0, flip=YAW[k] < 0)
            self.waiter.place(f, (SPOT["wtr"][0], SPOT["wtr"][1], M["waiter"][2]), scale=1.0, flip=True)
            self.key_set(f, set_window_view=("stub",), smoke=(0.0,))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, cast, mark in ART:
                self.actors[k].pose(f, pose_of(k, cast, g), camera=self.cam)
            w = dict(cast20.STORY20["waiter_idle"][1]); w["t"] = g / 30.0; w["lean"] = 1.5 * math.sin(g * 0.11)
            self.waiter.pose(f, w, camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = cam_path_static().report(GS[:-1])
        for r in rows[::4]:
            print(r)
        print("longest run under 0.25 px/frame: %d" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= G_LAST]
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
