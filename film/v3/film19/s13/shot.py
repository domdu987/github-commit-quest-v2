#!/usr/bin/env python3
"""shot.py -- film 19 take s13 = shot 13 (WORKSHOP shop_bench NIGHT, set_clock(3)): "จนผมหงอกทั้งหัว" (until his hair was all grey).
White-haired Harrison (harrison19 old=1: white hair, spectacles, brown coat) leans back from the bench and rubs his tired eyes (comic):
the candle stub is nearly burnt out.  Take = g 977..1024: 9-frame handle in (hard CUT in, so the handle is a pure safety margin) g 977..985,
shot g 986..1015 (32.85-33.86 s), 9-frame out-handle g 1016..1024 (shot 14 dissolves in over it).
    g 986..993  he bends over the work, the quick push-in already running
    g 993..1003 leans back (caption "จนผมหงอกทั้งหัว" 32.85 = g 989; the word หงอก is spoken ~g 996): the hand goes to his eyes, rubs
    g 1003..    rubs (small circles), a long tired sigh (head roll), blink; camera still pushing through the dissolve handle
Camera: shop_bench start region, push + slide; NO DOF, NO text, NO caption_shade.   Mouths: nobody speaks (fixed expression mouth).

    python3 shot.py probe a:b[:step]       numbers only        python3 shot.py camreport
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     (resumable; two processes e.g. 853:946:2 / 854:946:2)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(32.85), C.g_bound(33.86)            # 986, 1016: shot 13 = g 986..1015
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1            # 977 .. 1024
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = C.cap_g("จนผมหงอกทั้งหัว")                    # 989: caption start; the word หงอก is spoken ~g 996
SNAP = (G_WORD - 3, G_WORD + 13)                       # 991..1003 (12 f; the shot is only 1 s: a pronounced push, not a bible snap)
G_LOOKUP = (G_WORD + 4, G_WORD + 14)                   # he leans back and the hand goes to his eyes
BLINKS = []

LIGHT, PRESET, CLOCK = "NIGHT", "shop_bench", 3
FINAL_SPP = 8
PPD = 256
CANVAS = None

MARK = "harrison_bench"
MARK_DX = float(os.environ.get("MARK_DX", 0.0))
MARK_DY = float(os.environ.get("MARK_DY", 0.0))
CAM_LOC0 = tuple(float(v) for v in os.environ.get("CAM_LOC0", "2.4,0.3,2.3").split(","))
CAM_LOOK0 = tuple(float(v) for v in os.environ.get("CAM_LOOK0", "2.85,5.0,2.5").split(","))
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=float(os.environ.get("PUSH", 0.2)), slide_px=float(os.environ.get("SLIDE", -80)),
                rise_px=float(os.environ.get("RISE", 0)), arc_deg_s=float(os.environ.get("ARC", 8)), decay=0.25,
                snaps=[dict(g=SNAP, k=float(os.environ.get("SNAPK", 1.5)), peak=float(os.environ.get("SNAPPEAK", 2.8)), shift=(float(os.environ.get("SNAPSX", 0.8)), -0.1))])

BASE = dict(cast19.STORY19["harrison_tired_rub"][1])


def pose_of(g):
    p = dict(BASE)
    p["old"] = 1
    p["mirror"] = True                                    # the H3 is at screen-left of him
    lk = u_of(g, *G_LOOKUP, kind="sine")                  # 0 bent over the work -> 1 leaning back, rubbing
    rub = math.sin(2 * math.pi * g / 9.0)
    p["arm_r"] = dict(hand=(0.16 + 0.05 * rub * lk, 0.30 - 0.26 * lk + 0.04 * math.sin(2 * math.pi * g / 9.0 + 1.2) * lk), bend=-0.5,
                      layer="top", shape="open")
    p["arm_l"] = dict(hand=(-0.4, 0.96), bend=0.5)
    p["lean"] = lerp(8.0, -9.0, lk)                        # from bent over to leaning back
    p["pitch"] = lerp(0.30, -0.15, lk)
    p["head_roll"] = lerp(0.0, 7.0, lk) + 1.5 * math.sin(g * 0.3) * lk
    p["yaw"] = 0.2
    p["expr"] = "worried"
    p["blink"] = 2 if lk > 0.5 else 0                       # eyes shut while he rubs
    p["fx"] = ["sweat"] if lk > 0.7 else []
    p["t"] = g / 30.0
    return p


def candle_level(g):
    """the bench candle stub is nearly gone (continuity with shot 12, which ends at 0.30)"""
    return lerp(0.30, 0.18, clamp((g - G0) / float(G1 - G0)))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s13")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True, cam=self.cam)

    def pose(self, gs):
        mark = Vector(self.A["marks"][MARK]) + Vector((MARK_DX, MARK_DY, 0))
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.har, f, mark)
            self.key_set(f, clock=CLOCK, balance=g / 30.0, candles=candle_level(g))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        bars = C.clock_world(CLOCK, (0.0, 0.0, 0.64))
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), h1_bars_px=H.project(tuple(bars)),
                    dof=self.cam.data.dof.use_dof, caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
            print(r)
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
