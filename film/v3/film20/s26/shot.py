#!/usr/bin/env python3
"""shot.py -- film 20 take s26 = shot 26 (g 1912..1967, 4-frame handles each side: first_g 1908, last g 1971; hard cuts both sides).
"ที่มองไม่เห็นหอไอเฟล" -- RESTO resto_view / DAY 1889: over Maupassant's shoulder out of the big window: Paris, Seine, Trocadero and NO tower.
He sits with his back to us (cast20 maupassant_seated_back card) at the window table and raises his wine glass to the view.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(63.72), C.g_bound(65.60)    # 1912, 1968: shot = 1912..1967
H = 4
G_FIRST, G_LAST = G0 - H, G1 + H - 1           # 1908 .. 1971
G_TOWER = C.cap_g("หอไอเฟล")                    # 1939: snap + glass jerk up on "Eiffel tower"
SNAP = (G_TOWER - 2, G_TOWER + 12)
PRESET = "resto_view"
SEAT_H = 0.865
CAM_OFF = tuple(float(v) for v in os.environ.get("CAMOFF", "0.9,-3,0.1").split(","))
AIM_R = float(os.environ.get("AIMR", "1.2"))
TILT0 = float(os.environ.get("TILT0", "-0.3"))
PPD = 256
CANVAS = cast20.CANVAS20["maupassant"]
RAISE = (G0 + 2, G0 + 16)                       # glass rises (already part-way on frame 0: moving)
CLINK = G_TOWER                                  # extra lift / tilt of the glass on the word


def cam_path(A):
    cam = A["cams"][PRESET]
    subj = Vector(A["marks"]["maupassant_seated"]) + Vector((0.0, 0.0, 2.2))      # the back of his head
    subj = subj + Vector((AIM_R, 0.0, 0.0))                                        # aim right of him: he sits in the left third
    loc = Vector(cam["loc"]) + Vector(CAM_OFF)
    return C.CamPath(loc, subj, G_FIRST, G_LAST, push=0.22, slide_px=-60.0, rise_px=20.0, arc_deg_s=-8.0, tilt0=TILT0, tilt_deg_s=0.0,
                     decay=0.25, snaps=[dict(g=SNAP, k=1.95, peak=1.7, shift=(0.0, 0.0), tilt=0.0)])


def pose_of(g):
    p = dict(cast20.STORY20["maupassant_seated_toast"][1])
    p.update(seated=1, seat_h=SEAT_H, back=1, yaw=0.45, expr="smug", mouth=None)
    p.pop("mouth"); p.pop("gaze", None)
    up = ez(u_of(g, *RAISE))
    jerk = math.sin(math.pi * clamp((g - CLINK) / 8.0)) if g >= CLINK else 0.0
    p["arm_r"] = dict(hand=(lerp(0.62, 0.74, up) , lerp(0.62, 0.30, up) - 0.06 * jerk), bend=-0.3, stretch=1.2)
    p["pitch"] = -0.1 - 0.12 * jerk
    p["head_roll"] = -2.0 + 3.0 * math.sin(g * 0.23)
    p["lean"] = 2.5 * math.sin(g * 0.31) + 3.0 * jerk
    p["squash"] = (1.0, 1.0 + 0.02 * math.sin(g * 0.45))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="DAY", quality=quality, name="cam_s26")
        self.path = cam_path(self.A)
        self.key_cam(bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.6), cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"]["maupassant_seated"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.mau, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    GS = list(range(G_FIRST, G_LAST + 1))
    if cmd == "camreport":
        import tower20  # noqa
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        print("marks", {k: v for k, v in Tk.A["marks"].items() if "maupassant" in k or k == "window"}, "cam", Tk.A["cams"][PRESET])
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
