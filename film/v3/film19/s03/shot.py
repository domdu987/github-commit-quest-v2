#!/usr/bin/env python3
"""shot.py -- film 19 take s03 = shot 3 (HALL hall_window DAY), g 110..190 + 9 in-handle (101..109) + 9 out-handle (191..199).
"ทั้งที่นักปราชญ์ยังทำไม่ได้" (3.65-6.37 s): astro19_b peers through the brass telescope at the arched window; astro19 stands beside the
tube scratching his wig, puzzled.  Camera slides past the telescope tube (foreground) and pushes in; SNAP on "ทำไม่ได้" (g 177): astro_b
jerks his head from the eyepiece, frowning.  HALL DAY: set_candles(1.0) keyed on every frame; nobody speaks (mouths flat); no DOF, no text,
no caption_shade.

    python3 shot.py probe a:b[:step]        numbers only (camera, heads)
    python3 shot.py camreport               CamPath corner speed per frame (never parked)
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]    -> raw/ (or work/draft for scale < 1); run 2 processes, e.g. 101:199:2 / 102:199:2
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(3.65), C.g_bound(6.37)      # 110, 191 (exclusive): shot 3 = g 110..190
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1    # 101 .. 199
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP_WORD = C.g_of(5.80)                     # "ทำไม่ได้" 5.80 s -> g 177
SNAP = (G_SNAP_WORD - 8, G_SNAP_WORD + 7)      # 15 f, lands on the word
LIGHT, PRESET = "DAY", "hall_window"
FINAL_SPP = 8

# ----------------------------------------------------------------------------- camera
CAM_LOC0 = (0.3, -3.2, 2.3)
CAM_LOOK0 = (-2.95, 3.0, 2.7)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.10, slide_px=-25.0, rise_px=0.0, arc_deg_s=-21.0, decay=0.15,
                snaps=[dict(g=SNAP, k=2.0, peak=1.5, shift=(0.35, 0.05))])

# ----------------------------------------------------------------------------- cast
MARK_B = (-3.65, 2.60, 0.0)                    # astro19_b at the eyepiece (faces screen-left)
MARK_A = (-1.95, 3.10, 0.0)                    # astro19 beside the tube


def pose_b(g):
    """astro19_b: bends to the eyepiece (looking screen-left), then at the snap straightens up with a frown."""
    p = dict(cast19.STORY19["astro_b_idle"][1])
    u = 1.0 - u_of(g, SNAP[0] + 3, SNAP[0] + 12, "sine")            # 1 = at the eyepiece
    p["mirror"] = True
    p["yaw"] = 0.45
    p["expr"] = "squint" if u > 0.5 else "unimpressed"
    p["lean"] = 4.0 + 12.0 * u + 1.0 * math.sin(g * 0.15)
    p["pitch"] = 0.10 + 0.25 * u
    p["head_roll"] = 3.0 * u
    p["gaze"] = (0.9, 0.5) if u > 0.5 else (0.4, 0.0)
    p["arm_r"] = dict(hand=(0.45, 0.35 + 0.1 * (1 - u)), bend=0.8, shape="open", layer="top")
    p["arm_l"] = dict(hand=(-0.35, 0.95), bend=0.6)
    p["mouth"] = "flat"
    p["blink"] = blink(g, [128, 163, 190])
    p["legs"] = "stand"
    return p


def pose_a(g):
    """astro19: arm up scratching under the wig (small 3 Hz scrub), puzzled glance up, shifts weight."""
    p = dict(cast19.STORY19["astro_idle"][1])
    p["mirror"] = True
    p["yaw"] = 0.35
    p["expr"] = "worried" if (g // 40) % 2 == 0 else "unimpressed"
    scrub = 0.07 * math.sin(2 * math.pi * g / 9.0)
    p["arm_r"] = dict(hand=(0.50 + scrub, -0.42 + 0.5 * scrub), bend=0.9, shape="open", layer="top")
    p["arm_l"] = "akimbo"
    p["head_roll"] = -6.0 + 3.0 * math.sin(g * 0.11)
    p["lean"] = 1.0 + 1.0 * math.sin(g * 0.1)
    p["gaze"] = (0.8, 0.9)
    p["mouth"] = "flat"
    p["blink"] = blink(g, [118, 150, 181])
    return p


def bob(g, ph=0.0):
    return 0.012 * math.sin(2 * math.pi * g / 20.0 + ph)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s03")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.ab = self.actors["ab"] = C.make_actor("ab", "astro19_b", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.aa = self.actors["aa"] = C.make_actor("aa", "astro19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.ab, f, Vector(MARK_B) + Vector((0, 0, bob(g))))
            C.place(self.aa, f, Vector(MARK_A) + Vector((0, 0, bob(g, 1.7))))
            self.key_set(f, candles=1.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.ab.pose(f, pose_b(g), camera=self.cam)
            self.aa.pose(f, pose_a(g), camera=self.cam)
        self.sprites_for([(self.ab, 256), (self.aa, 256)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

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
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
