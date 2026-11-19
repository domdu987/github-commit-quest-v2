#!/usr/bin/env python3
"""shot.py -- film 16 take s07 = shot 7, STUDIO studio_window / DAY ("เขาเลยอยากส่งข่าวไปตามลวด ให้ถึงในพริบตา" ; was: ("เมียเขาป่วยหนัก ... เมียก็ตายไป แล้ว").
Shot g 401..474 (13.37-15.84 s), hard cuts both sides, 9 handle frames each side: g 392..483.
Morse at the window (long road outside), stands thinking, then lifts the copper coil and the horseshoe magnet; on "พริบตา" (g 465) a blue spark
jumps at the magnet poles (card glint) and his eyes light up; the camera pulls back 8 %/s with a slide, SNAP push on "พริบตา".  Mouth still.  NO DOF, NO text.

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

G0, G1 = C.g_bound(13.37), C.g_bound(15.84)             # 401, 475 (exclusive)
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1                       # 392 .. 483
GS = list(range(GF, GL + 1))
PRESET, LIGHT = "studio_window", "DAY"
PPD = 256
G_WORD = C.cap_g("พริบตา")                               # 465: "in the blink of an eye" -> spark + snap push
SNAP = (G_WORD - 3, G_WORD + 10)
G_LIFT = (C.cap_g("ให้ถึงใน") - 4, G_WORD - 6)            # arms rise to show the coil and the magnet (446 .. 459)
G_SPARK = G_WORD                                         # glint (blue spark at the poles) from here

ROAD_LIFT = 12.0
M0 = Vector((-4.6, 9.8, 0.0))                           # Morse stands in front of the window, the sill behind him
CAM_LOOK0 = (-3.3, 9.8, 2.6)
CAM_LOC0 = (-2.0, 6.2, 3.2)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=-0.08, slide_px=-115.0, rise_px=-40.0, arc_deg_s=-18.0, decay=0.3,
                snaps=[dict(g=SNAP, k=1.8, peak=1.8, shift=(-0.9, 0.25))])

P = cast16.STORY16
Y_IDLE = P["morse_young_idle"][1]
SHOW = dict(P["morse_show_coil_magnet"][1])
SHOW["young"] = 1
BLINKS = [398, 412, 428, 444, 455, 470, 481]


def lp(a, b, u):
    out = puppet.lerp_pose("morse16", a, b, u)
    out["young"] = 1
    return out


def pose_mor(g):
    u = u_of(g, *G_LIFT)
    p = lp(Y_IDLE, SHOW, u)
    p["young"] = 1
    p["yaw"] = lerp(0.45, 0.55, u)
    p["gaze"] = (0.9, lerp(-0.25, -0.15, u))              # out of the window (screen-right)
    p["arm_l"] = dict(p["arm_l"], hand=(lerp(p["arm_l"]["hand"][0], -0.86, u), lerp(p["arm_l"]["hand"][1], 0.34, u)), bend=0.3)
    if u < 0.5:
        p["prop_r"], p["prop_l"] = None, None
        p["expr"], p["mouth"] = "neutral", "flat"
    else:
        p["prop_r"] = dict(type="magnet", angle=-35)
        p["prop_l"] = "wire_coil"
    if g >= G_LIFT[1] - 4:
        p["expr"], p["mouth"] = "excited", "smile"          # closed-mouth grin (mouths move only in the quotes)
    p["glint"] = 1.0 if g >= G_SPARK else 0.0
    p["lean"] = 1.2 * math.sin(g * 0.17)
    p["head_roll"] = -2 + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, BLINKS)
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.2))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s07")
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.dress()

    def raise_road(self):
        """the long road to the horizon (plan): lift the street, its fields and the far houses so that the road is seen from standing
        eye height (set ground sits 9 m below the window) and drop the near rooftops that hid it."""
        import bpy
        for o in bpy.data.objects:
            n = o.name
            if n.startswith("rooftops_") and not n.endswith("f"):
                o.hide_render = True
            if n.startswith(("rooftops_", "street_", "trees_out_", "ground", "field", "gnd")):
                o.location.z += ROAD_LIFT
        import tg_studio as SDm
        M = TG.STATE["M"]
        mb = K.MB("road_wide")
        zz = -9.0 + ROAD_LIFT / K.SC + 0.05
        x0, x1 = SDm.WIN_X - 5.0, SDm.WIN_X + 5.0
        ys = [float(i) for i in range(int(SDm.BY + 1), 420, 4)]
        for a, b in zip(ys[:-1], ys[1:]):
            mb.quad(M["road2"], [(x0, a, zz), (x1, a, zz), (x1, b, zz), (x0, b, zz)][::-1])
        mb.finish()

    def dress(self):
        self.raise_road()
        S = TG.STATE
        for o in S.get("fg", []):
            o.hide_render = True
        loc0 = Vector(CAM.at(GF)[0]) / K.SC
        look = Vector(CAM_LOOK0) / K.SC
        S["fg2"] = SD.fg_dress(S, S["M"], tuple(loc0), tuple(look), [("jars", 1.1, 1.2), ("canvases", 1.9, 1.6)], seed=11)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, tuple(M0))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, pose_mor(g), camera=self.cam)
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
