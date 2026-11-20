#!/usr/bin/env python3
"""shot.py -- film 20 take s08 = shot 8, CAFE cafe_window (1887).  Over the artists' shoulders: they jab fingers at the window where the tower stub
smokes like a black factory chimney (smoke ramps 0 -> 1 over 17.10-18.96 s and holds 1.0 on "ปล่องโรงงานสีดำ").
Shot 8 = g 513..603 (17.10-20.15 s); cut in (4-frame handle g 509..512), cut out at 604 (out-handle g 604..607).  Whole take g 509..607 (99 frames).
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

G0, G1 = C.g_bound(17.10), C.g_bound(20.15)       # 513, 604
H_IN, H_OUT = 4, 4
GA, G_LAST = G0 - H_IN, G1 + H_OUT - 1             # 509 .. 607
GS = list(range(GA, G_LAST + 1))
G_CHIM = C.cap_g("เหมือนปล่อง")                   # 572: "like a chimney" -> smoke 1.0 + snap + jabs
G_BLACK = C.cap_g("โรงงานสีดำ")                    # 590: "black factory"
G_RAMP0 = C.g_bound(17.10)                         # 513: smoke starts
SNAP = (G_CHIM - 2, G_CHIM + 13)
LIGHT, PRESET, PPD = "DAY", "cafe_window", 192

ART = [("art1", "painter20", "artist_1"), ("art2", "composer20", "artist_2"), ("art3", "poet20", "artist_3"), ("art4", "architect20", "artist_4")]
# stage (D, world x/y); yaw sign = facing (negative mirrors); back = three-quarter back view toward the lens
SPOT = {"art1": (-2.7, 6.9), "art2": (0.4, 7.6), "art3": (3.5, 8.3), "art4": (-1.4, 6.3)}
BACK = {"art1": True, "art2": False, "art3": False, "art4": True}
YAW = {"art1": 0.35, "art2": 0.45, "art3": -0.4, "art4": 0.3}
PHASE = {"art1": 0.0, "art2": 1.7, "art3": 3.1, "art4": 4.4}
# where the pointing hand goes (arm local coords, D; the puppet arm 'hand' = (forward, up) from the shoulder)
POINT = {"art1": (0.95, 0.35), "art2": (1.0, 0.25), "art3": (1.0, 0.3), "art4": (0.9, 0.55)}


def cam_path(A):
    c = Vector(eval(os.environ.get("CAML", "(1.5, -0.8, 2.4)")))
    subj = Vector((1.4, 12.0, 3.3))
    return C.CamPath(c, subj, GA, G_LAST, push=float(os.environ.get("PUSH", "0.05")), slide_px=float(os.environ.get("SLIDE", "-45")),
                     tilt0=float(os.environ.get("TILT", "3")), tilt_deg_s=0.0, decay=0.25, arc_deg_s=float(os.environ.get("ARC", "0")),
                     snaps=[dict(g=SNAP, k=1.15, peak=1.7, shift=(0.0, 0.0), tilt=0.0),
                            dict(g=(G_BLACK - 2, G_BLACK + 12), k=1.12, peak=1.7, shift=(0.0, 0.0), tilt=0.0)])


def cam_path_static():
    return cam_path(None)


def pose_of(k, cast, g):
    t = g / 30.0
    ph = PHASE[k]
    w = 2 * math.pi * 1.9
    p = dict(cast20.STORY20[cast + "_outraged"][1])
    p["expr"] = "outraged"
    if BACK[k]:
        p["back"] = 1
    jab = 0.5 + 0.5 * math.sin(w * 1.3 * t + ph)                      # finger jab 0..1 (toward the window and back)
    up = u_of(g, SNAP[0], SNAP[1])
    hx, hy = POINT[k]
    p["arm_r"] = dict(hand=(hx + 0.30 * jab + 0.10 * up, hy + 0.10 * math.sin(w * t * 0.5 + ph)), shape="point", bend=-0.4, stretch=1.3, layer="top")
    p.pop("prop_r", None)
    p["yaw"] = abs(YAW[k])
    p["pitch"] = -0.15
    p["head_roll"] = -4 + 4 * math.sin(w * t * 0.5 + ph)
    p["lean"] = 2.0 * math.sin(w * t * 0.5 + ph + 1.0) + 2.0 * up
    p["squash"] = (1.0 + 0.012 * math.sin(2 * math.pi * 3.0 * t + ph), 1.0 - 0.012 * math.sin(2 * math.pi * 3.0 * t + ph))
    p["blink"] = blink(g, [520 + 11 * int(ph), 563 + 3 * int(ph)])
    p["t"] = t
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s08")
        self.path = cam_path(self.A)
        CO.setup_grade(self.scene, dict(sat=float(os.environ.get("SAT", "1.30"))))      # SAT_GRADE: film-wide saturation >= 0.47 (QA_TEAM §G)
        self.key_cam(bf(GA), *self.path.at(GA))
        self.scene.frame_set(bf(GA))
        for k, cast, mark in ART:
            self.actors[k] = C.make_actor(k, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                          contact=dict(width=1.2, depth=0.5, opacity=0.7))

    def smoke_v(self, g):
        return clamp((g - G_RAMP0) / float(G_CHIM - G_RAMP0))

    def pose(self, gs):
        M = self.A["marks"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            for k, cast, mark in ART:
                x, y = SPOT[k]
                self.actors[k].place(f, (x, y, M[mark][2]), scale=1.0, flip=YAW[k] < 0)
            self.key_set(f, set_window_view=("stub",), smoke=(self.smoke_v(g),))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, cast, mark in ART:
                self.actors[k].pose(f, pose_of(k, cast, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    smoke=round(self.smoke_v(g), 3), heads=C.head_report(self, f))

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
