#!/usr/bin/env python3
"""shot.py -- film 20 take s27 = shot 27, THE LAST IMAGE (g 1968..2045; 4-frame in-handle g 1964..1967; the film ends on a hard cut at 2046).
TOWER tower_window_pull / DAY 1889: crash pull-out from the lit first-floor restaurant window (Maupassant eating at his table, eyes shut,
smug) to the whole Eiffel Tower (tower_window_end framing).  The camera flies from 6 m in front of the glass to 236 m back, with a
log-like ease (the first frames are the fastest), and the last 12 frames drift almost still.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(65.60), 2046                  # 1968 .. 2045
H = 4
G_FIRST, G_LAST = G0 - H, G1 - 1                 # 1964 .. 2045 (no out-handle: hard cut at the end of the film)
G_PULL = (G0, 2036)                          # the crash pull-out; 2034..2045 near still
G_WORD = C.cap_g("สักครั้ง")                     # 2020: last word
PRESET = "tower_window_pull"
PPD = 256
CLOSE = float(os.environ.get("CLOSE", "4.0"))
LOOK_DROP = float(os.environ.get("LDROP", "3.3"))
CANVAS = cast20.CANVAS20["maupassant"]


def cam_dicts(A):
    return A["cams"][PRESET], A["cams"]["tower_window_end"]


def cam_at(A, g):
    """(loc, look, shift_y) at film frame g.  Crash pull: u runs 0 -> 1 over G_PULL with a fast start / slow finish; the camera moves
    along log-distance (geometric), the aim sweeps from the window to the tower's mid height, the lens shift blends 0 -> end shift."""
    a, b = cam_dicts(A)
    u = min(1.0, (g - G_PULL[0]) / float(G_PULL[1] - G_PULL[0]))
    e = (1.0 - (1.0 - u) ** 1.9) if u >= 0 else 0.5 * 1.9 * u                     # crash ease-out: fastest on the first frames
    la, lb = Vector(a["loc"]) + Vector((0.0, CLOSE, 0.0)), Vector(b["loc"])
    pa, pb = Vector(a["look_at"]), Vector(b["look_at"])
    # distance to the tower (y axis) in log space, x/z linear in the same fraction
    ya, yb = abs(la.y), abs(lb.y)
    d = ya * (yb / ya) ** e
    f = (d - ya) / (yb - ya)
    loc = la.lerp(lb, f)
    pa = pa - Vector((0.0, 0.0, LOOK_DROP))
    look = pa.lerp(pb, max(f, 0.0) if f < 0 else f)
    if f < 0:
        loc = la.lerp(lb, f * 0.12)
    sh = lerp(a.get("shift", 0.0), b.get("shift", 0.0), f)
    # after the pull: a gentle residual drift (never parked), 0.15 %/s ...
    t_after = max(0.0, (g - G_PULL[1]) / 30.0)
    loc = loc + Vector((0.0, -1.0, 0.0)) * (1.2 * t_after)
    return loc, look, sh


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="DAY", quality=quality, name="cam_s27")
        self.scene.frame_set(bf(G_FIRST))
        self.key_cam(bf(G_FIRST), *cam_at(self.A, G_FIRST)[:2])
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.0, depth=0.4, opacity=0.5), cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"]["maupassant_window"]
        for g in gs:
            f = bf(g)
            loc, look, sh = cam_at(self.A, g)
            self.key_cam(f, loc, look)
            self.cam.data.shift_y = sh
            self.cam.data.keyframe_insert("shift_y", frame=f)
            C.place(self.mau, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look, sh = cam_at(self.A, g)
        return dict(g=g, cam=[round(c, 2) for c in loc], shift=round(sh, 3), heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def pose_of(g):
    p = dict(cast20.STORY20["maupassant_seated_eyes_shut_right"][1])
    p.update(seated=1, seat_h=SEAT_H, yaw=0.35)
    p["head_roll"] = 5.0 + 1.8 * math.sin(g * 0.2)
    p["squash"] = (1.0, 1.0 + 0.01 * math.sin(g * 0.3))
    p["lean"] = 1.2 * math.sin(g * 0.15)
    p["t"] = g / 30.0
    return p


SEAT_H = 0.865
if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        print("marks", {k: v for k, v in Tk.A["marks"].items() if "window" in k}, "cams", Tk.A["cams"][PRESET], Tk.A["cams"]["tower_window_end"])
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
