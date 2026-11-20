#!/usr/bin/env python3
"""shot.py -- film 19 take s24 = shot 24 (HALL hall_table EVENING): "เลยมาจับเวลานาฬิกาของเขาเองกับมือ ทุกวัน สิบสัปดาห์".
King19 stands at the head of the Board table and compares Harrison's silver watch (left hand) with his gold pocket watch (right hand),
squinting, glancing from one to the other, nodding.  The ten candle stubs pile up along the near table edge (set_stubs 0 -> 10, one
more every ~0.3 s: the ten-weeks time-lapse).  set_kings_chair(True), set_regulator(True), set_candles flicker, all keyed every frame.
g 2028-handle..: shot = g 1933..2027 (64.44-67.61 s); in-handle 9 f (hard cut in), out-handle 9 f (hard cut to shot 25).
Camera: custom low-ish dolly over the stubs toward the King (push + slide), snap on "สิบสัปดาห์" (66.77 s -> g 2006).
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(64.44), C.g_bound(67.61)            # 1933, 2028 (exclusive)
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP = C.cap_g("สิบสัปดาห์")                           # 2006
SNAP = (G_SNAP - 3, G_SNAP + 13)
PRESET, LIGHT, FINAL_SPP, PPD = "hall_table", "EVENING", 8, 256
BLINKS = [1950, 1978, 2012, 2030]

KING_M = (0.0, 4.25, 0.0)
CAM_LOC0 = (-1.30, -2.20, 2.35)
CAM_LOOK0 = (1.00, 7.9, 2.40)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.10, slide_px=-95.0, rise_px=-10.0, arc_deg_s=11.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.30, peak=2.1, shift=(2.00, 0.30))])

KB = dict(cast19.STORY19["king_watch_squint"][1])


def stubs_at(g):
    return int(clamp((g - G0) / float(G1 - 1 - G0)) * 10.0 + 0.5)


def pose_of(g):
    p = dict(KB)
    t = (g - G_FIRST) / 30.0
    # the comparison: the two hands alternate between "up to the eye" and "down", out of phase, ~0.9 s period
    ph = 2 * math.pi * t / 0.9
    ur, ul = 0.5 + 0.5 * math.sin(ph), 0.5 + 0.5 * math.sin(ph + math.pi)
    p["arm_r"] = dict(hand=(0.60, 0.45 + 0.42 * ur), bend=-0.2, shape="open", stretch=1.15, layer="top")
    p["arm_l"] = dict(hand=(-0.60, 0.45 + 0.42 * ul), bend=-0.2, shape="open", stretch=1.15, layer="top")
    p["gaze"] = (0.9 * math.sin(ph + 0.4), 0.55)           # eyes go from one watch to the other
    p["yaw"] = 0.20 + 0.18 * math.sin(ph + 0.4)
    p["head_roll"] = 4.0 + 7.0 * math.sin(ph * 0.5)
    p["pitch"] = 0.15 + 0.05 * math.sin(ph)
    p["lean"] = 2.0 + 4.0 * math.sin(ph)
    p["expr"] = "unimpressed"
    p["mouth"] = "flat"
    p["blink"] = 1 if (g // 10) % 4 == 1 and g % 10 < 3 else blink(g, BLINKS)   # squint: lids half down most of the time
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s24")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.king = self.actors["king"] = C.make_actor("king", "king19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose(self, gs):
        mark = Vector(K.W(KING_M))
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.king, f, mark + Vector((0, 0, 0.012 * math.sin(2 * math.pi * g / 20.0))))
            self.key_set(f, candles=1.0, regulator=True, kings_chair=True, stubs=stubs_at(g), moneybag="none", box="none")
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.king.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.king, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], stubs=stubs_at(g), heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print([r["px"] for r in rows])
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        samples = samples or FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
