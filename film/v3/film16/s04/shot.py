#!/usr/bin/env python3
"""shot.py -- film 16 take s04 = shot 4, STUDIO studio_wide / DAY ("เกือบสองร้อยปีก่อน ... มอร์สเป็นจิตรกร").
Shot g 168..255 (5.59-8.53 s), dissolve in (15 f) from shot 3, hard cut out to shot 5; 9 handle frames each side: g 159..264.
Morse (young, the 1825 smock) paints the big unfinished general at the easel; the camera cranes down from the window light to him
while pulling back, with one eased SNAP push on "เกือบสองร้อย" (g 206).  Mouths still (no quote).  NO DOF, NO text.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] <out> [scale] [spp] | final a:b[:s] [scale] [spp]   (as s01)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
import puppet                                            # noqa: E402
import tg_studio as SD                                   # noqa: E402
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(5.59), C.g_bound(8.53)                # 168, 256 (exclusive)
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1                       # 159 .. 264
GS = list(range(GF, GL + 1))
G_SNAP_WORD = C.cap_g("เกือบสองร้อย")                    # 206
SNAP = (G_SNAP_WORD - 3, G_SNAP_WORD + 10)
PRESET, LIGHT = "studio_wide", "DAY"
PPD = 256
SUBJ = lambda mark: Vector(mark) + Vector((0.0, 0.0, 2.1))

# ----------------------------------------------------------------------------- camera (world D)
CAM_LOOK0 = (-0.1, 5.8, 2.4)
CAM_LOC0 = (1.7, -0.5, 5.0)
CAM_START = 1.0
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=-0.07, slide_px=75.0, rise_px=-50.0, arc_deg_s=11.0, decay=0.3,
                snaps=[dict(g=SNAP, k=2.0, peak=1.7, shift=(-0.7, -0.05))])

YOUNG = cast16.STORY16["morse_young_paint"][1]
BLINKS = [172, 191, 214, 238, 252, 163]


def pose_of(g):
    p = dict(YOUNG)
    cyc = (g % 34) / 34.0
    dip = 0.5 - 0.5 * math.cos(2 * math.pi * cyc)                    # 0 at the canvas, 1 at the palette
    hx = lerp(0.88, 0.56, dip) + 0.05 * math.sin(g * 0.9)
    hy = lerp(0.30, 0.62, dip) + 0.05 * math.sin(g * 0.7 + 1.0)
    p["arm_r"] = dict(YOUNG["arm_r"], hand=(hx, hy))
    p["arm_l"] = dict(YOUNG["arm_l"], hand=(-0.30 + 0.03 * math.sin(g * 0.3), 0.96 + 0.03 * math.sin(g * 0.37)))
    p["lean"] = 1.5 * math.sin(g * 0.17)
    p["head_roll"] = -4 + 1.5 * math.sin(g * 0.13)
    p["gaze"] = (0.9, lerp(-0.2, 0.25, dip))
    p["blink"] = blink(g, BLINKS)
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.2))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s04")
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.dress()

    def dress(self):
        """denser foreground: jars + canvases near the lens (the preset's own are for the preset camera)."""
        S = TG.STATE
        for o in S.get("fg", []):
            o.hide_render = True
        loc0 = Vector(CAM.at(GF)[0]) / K.SC
        look = Vector(CAM_LOOK0) / K.SC
        items = [("jars", -0.7, 1.3), ("canvases", 0.9, 1.5)]
        S["fg2"] = SD.fg_dress(S, S["M"], tuple(loc0), tuple(look), items, seed=11)

    def pose(self, gs):
        mark = self.A["marks"]["morse_easel"]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, mark)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mor, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows[::6]:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= GL]
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["studio"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
