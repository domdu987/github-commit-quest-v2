#!/usr/bin/env python3
"""shot.py -- film 19 take s14 = shot 14, THE REVEAL IMAGE (WORKSHOP shop_clock DAY, set_clock([1, 4])):
"แล้วเขาก็ย่อมันเหลือแค่เรือนกลม ๆ เท่าจานรอง" -- then he shrank it to a round piece the size of a saucer.
The tiny silver H4 on its red cloth beside the giant brass H1 (set_clock([1, 4]) puts H1 at x 0.93 D, H4 at x 2.07 D on the bench); Harrison
(harrison19 default: greying hair, apron) stands behind them and holds out an open palm toward the H4, proud.
Take = g 1007..1104: 9-frame dissolve in-handle g 1007..1015, shot g 1016..1095 (33.86-36.52 s), 9-frame out-handle g 1096..1104 (dissolve 11 f out).
    g 1016..1070 a wide-ish framing: the H1 big on the left, the tiny H4 on its cloth beside it, Harrison behind with his palm out
                  (captions: "แล้วเขาก็ย่อ" g 1017, "มันเหลือแค่" g 1038, "เรือนกลม ๆ" g 1059); the camera drifts, H1 bars rock
    g 1073..1091 SNAP / whip onto the H4 on "เท่าจานรอง" (caption 35.88 = g 1079): framing x ~2, panned to the H4; his palm presents it
    g 1091..1104 hold on the H4 (tick marks readable), still moving
NO DOF, NO text, NO caption_shade.   Mouths: nobody speaks (fixed expression mouth).

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

G0, G1 = C.g_bound(33.86), C.g_bound(36.52)            # 1016, 1096: shot 14 = g 1016..1095
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1            # 1007 .. 1104
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = C.cap_g("เท่าจานรอง")                         # 1079: caption start; "จานรอง" is spoken ~g 1085
SNAP = (G_WORD - 8, G_WORD + 12)                       # 1073..1089 (16 f)
G_LOOKUP = (G_WORD - 40, G_WORD - 24)                 # the palm goes out toward the H4 (g 1039..1055)
BLINKS = [1028, 1048, 1066, 1090]
H1_SHIFT = float(os.environ.get("H1_SHIFT", 0.14))
H1_X0 = 0.0

LIGHT, PRESET, CLOCK = "DAY", "shop_clock", [1, 4]
FINAL_SPP = 8
PPD = 256
CANVAS = None

MARK = "harrison_bench"
MARK_DX = float(os.environ.get("MARK_DX", -0.3))
MARK_DY = float(os.environ.get("MARK_DY", 0.0))
CAM_LOC0 = tuple(float(v) for v in os.environ.get("CAM_LOC0", "0.812,-2.848,2.98").split(","))
CAM_LOOK0 = tuple(float(v) for v in os.environ.get("CAM_LOOK0", "2.0,3.2,1.9").split(","))
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=float(os.environ.get("PUSH", 0.36)), slide_px=float(os.environ.get("SLIDE", -4)),
                rise_px=float(os.environ.get("RISE", 25)), arc_deg_s=float(os.environ.get("ARC", 8)), decay=0.25,
                snaps=[dict(g=SNAP, k=float(os.environ.get("SNAPK", 1.95)), peak=float(os.environ.get("SNAPPEAK", 3.0)), shift=(float(os.environ.get("SNAPSX", 0.6)), float(os.environ.get("SNAPSY", -0.22))))])

SWAY = float(os.environ.get("SWAY", 0.0))           # client rule (no camera shake): the handheld sway is OFF            # handheld sway (D) along the view's right axis, 1.5 Hz + a little vertical: more life in the wide, no net drift


def cam_at(g):
    loc, look = CAM.at(g)
    fwd = (look - loc).normalized()
    right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
    up = right.cross(fwd).normalized()
    ph = 2 * math.pi * g / 20.0
    off = right * (SWAY * math.sin(ph)) + up * (0.5 * SWAY * math.sin(ph * 0.7 + 1.0))
    return loc + off, look + off


BASE = dict(cast19.STORY19["harrison_show_h4"][1])


G_SWEEP = (1039, 1050)                                  # the palm sweeps out toward the H4 (captions: "มันเหลือแค่" g 1038)
G_LENS = (1056, 1068)                                   # eyes go from the H4 to a proud look at the lens
G_TADA = (G_WORD, G_WORD + 8)                           # 1079..1087: small "ta-da" bounce on "เท่าจานรอง"


def pose_of(g):
    p = dict(BASE)
    p.pop("prop_r", None)                                  # the H4 is the set's own (on its red cloth): his hand is an empty open palm
    p["mirror"] = True                                     # the H4 is at screen-left of him
    sw = u_of(g, *G_SWEEP, kind="sine")                    # 0 hand low -> 1 palm out at shoulder height, above the cloth
    ln = u_of(g, *G_LENS, kind="sine")                     # 0 eyes on the H4 -> 1 at the lens
    td = math.sin(math.pi * u_of(g, G_TADA[0], G_TADA[1] + 6))   # 0..1..0 bounce
    bob = 0.04 * math.sin(2 * math.pi * g / 15.0)
    hand = (lerp(0.42, 0.98, sw) + 0.05 * td, lerp(0.95, 0.30, sw) + bob - 0.10 * td)
    p["arm_r"] = dict(hand=hand, bend=-0.2, layer="top", shape="open", stretch=1.3)   # layer top: in front of the body
    p["arm_l"] = "hip"
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * g / 24.0)   # chest-puff breathing (1.25 Hz)
    p["squash"] = (1.0 + 0.012 * pulse + 0.035 * td, 1.0 - 0.012 * pulse - 0.035 * td)
    p["lean"] = lerp(1.0, -3.0, sw) - 3.0 * td + 1.2 * math.sin(g * 0.2)
    p["head_roll"] = -4.0 + 2.0 * math.sin(g * 0.15 + 0.6) + 3.0 * td
    p["pitch"] = -0.05
    p["yaw"] = 0.3
    p["gaze"] = (lerp(0.9, 0.1, ln), lerp(0.55, 0.0, ln))   # eyes on the H4 first, then a proud look at the lens
    p["expr"] = "smile" if g < 1058 else ("grinning" if g >= G_WORD - 4 else "happy")
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def bounce_z(g):
    """a small proud rise on the toes with the ta-da (D) + a 1.25 Hz breathing lift"""
    return 0.05 * math.sin(math.pi * u_of(g, G_TADA[0], G_TADA[1] + 6)) + 0.008 * math.sin(2 * math.pi * g / 24.0)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s14")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        global H1_X0
        H.set_clock([1, 4])
        H1_X0 = float(C.clock_root(1).location.x)
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True, cam=self.cam)

    def pose(self, gs):
        mark = Vector(self.A["marks"][MARK]) + Vector((MARK_DX, MARK_DY, 0))
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            C.place(self.har, f, mark + Vector((0, 0, bounce_z(g))))
            self.key_set(f, clock=(CLOCK,), balance=g / 30.0, candles=1.0)
            # the H1 stands 0.14 D further left so its corner post leaves a gap above the H4 (the root is a child of the 1.85-scaled set root)
            r1 = C.clock_root(1)
            r1.location.x = H1_X0 - H1_SHIFT / 1.85
            r1.keyframe_insert("location", frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_at(g)
        bars = C.clock_world(1, (0.0, 0.0, 0.64))
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
