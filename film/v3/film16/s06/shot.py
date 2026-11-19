#!/usr/bin/env python3
"""shot.py -- film 16 take s06 = shot 6, STUDIO studio_door / DAY ("เมียเขาป่วยหนัก ... เมียก็ตายไป แล้ว").
Shot g 314..400 (10.45-13.37 s), hard cuts both sides, 9 handle frames each side: g 305..409.
The messenger hands Morse the sealed letter (swap on a blink g 334), Morse reads; on "เมียก็ตายไป" (g 376) SNAP push to his face while the
palette tips; it slips (g 381) and falls to the floor with one bounce (set palette, no injury); he sinks onto the stool and looks at the
wife's small portrait (screen-right).  Mouths still.  NO DOF, NO text.

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

G0, G1 = C.g_bound(10.45), C.g_bound(13.37)             # 314, 401 (exclusive)
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1                       # 305 .. 409
GS = list(range(GF, GL + 1))
PRESET, LIGHT = "studio_door", "DAY"
PPD = 256
G_SWAP_LETTER = 334                                      # the letter changes hands (on a blink)
G_SHOCK = C.cap_g("เมียก็ตายไป")                          # 376: wife dead -> snap push on his face, palette tips
SNAP = (G_SHOCK - 3, G_SHOCK + 10)
G_DROP = 381                                             # palette leaves the hand
G_FALL = (381, 387)                                      # fall + bounce
G_SIT = 391                                              # pose swap to the stool on a blink (389..391)

# ----------------------------------------------------------------------------- staging (world D); camera looks toward -x so the wife's portrait is screen-right
M0 = Vector((-0.9, 3.5, 0.0))                            # Morse standing
M_SIT = Vector((-1.45, 3.65, 0.0))                       # on the set's stool (STOOL (-0.9, 2.0) m = (-1.67, 3.7) D)
N0 = Vector((-2.5, 2.9, 0.0))                          # messenger, screen-left of Morse
CAM_LOOK0 = (-1.0, 3.7, 2.35)
CAM_LOC0 = (3.0, 1.9, 2.9)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=0.08, slide_px=-95.0, rise_px=0.0, arc_deg_s=-20.0, decay=0.3,
                snaps=[dict(g=SNAP, k=1.4, peak=1.7, shift=(-0.35, 0.0))])

P = cast16.STORY16
Y_IDLE = P["morse_young_palette_ready"][1]
Y_READ = P["morse_young_read_letter"][1]
Y_DROP = P["morse_young_palette_drop"][1]
Y_STOOL = P["morse_young_stool"][1]
MSG_HAND = P["messenger_hand_letter"][1]
MSG_IDLE = P["messenger_idle"][1]
BLINKS = [322, G_SWAP_LETTER - 1, 352, 366, G_SIT - 2, 397, 405, 309]


def lp(a, b, u):
    out = puppet.lerp_pose("morse16", a, b, u)
    out["young"] = 1
    return out


def pose_mor(g):
    if g < G_SWAP_LETTER:
        p = dict(Y_IDLE)
        p["expr"], p["mouth"] = "neutral", "flat"
        p["gaze"] = (-0.6, 0.0)
        p["arm_r"] = dict(Y_IDLE["arm_r"], hand=(0.50, 1.0 + 0.03 * math.sin(g * 0.3)))
        p["prop_r"] = dict(type="brush16", angle=-70)
    elif g < G_DROP:
        u = u_of(g, G_SHOCK - 6, G_DROP)                 # palette tips as the news lands
        p = lp(Y_READ, Y_DROP, u)
        p["prop_r"] = "letter"
        p["prop_l"] = dict(type="palette16", angle=lerp(40, 75, u))
        p["expr"] = "shocked"
        p["fx"] = ["sweat"] if g > G_SHOCK else []
    elif g < G_SIT:
        p = dict(Y_DROP)
        p["prop_l"] = None
        p["arm_l"] = dict(Y_DROP["arm_l"], hand=(-0.50, 1.18 + 0.4 * u_of(g, G_DROP, G_SIT, "sine") * 0.5))
        p["legs"] = dict(Y_DROP["legs"]) if isinstance(Y_DROP["legs"], dict) else Y_DROP["legs"]
        p["expr"] = "shocked" if g < G_SIT - 3 else "sad"
    else:
        p = dict(Y_STOOL)
    p["young"] = 1
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.17)
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, BLINKS)
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.2))
    p["t"] = g / 30.0
    return p


def pose_msg(g):
    p = dict(MSG_HAND if g < G_SWAP_LETTER else MSG_IDLE)
    if g < G_SWAP_LETTER:
        p["arm_r"] = dict(MSG_HAND["arm_r"], hand=(0.70 + 0.03 * math.sin(g * 0.5), 0.74 + 0.02 * math.sin(g * 0.4)))
    if g >= G_SHOCK - 4:
        p["expr"] = "sad"
    p["lean"] = 1.2 * math.sin(g * 0.19 + 1.0)
    p["blink"] = blink(g, [318, 349, 380, 398])
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.23 + 0.5))
    p["t"] = g / 30.0
    return p


def mor_pos(g):
    return M0.lerp(M_SIT, u_of(g, G_DROP + 2, G_SIT + 2))


def fall_z(g):
    """palette height above the floor (D): in the hand until G_DROP, falls, bounces once, rests."""
    a, b = G_FALL
    if g < G_DROP:
        return None
    if g >= b + 6:
        return 0.0
    if g <= b:
        u = (g - a) / float(b - a)
        return 1.9 * (1 - u * u)
    u = (g - b) / 6.0
    return 0.25 * math.sin(math.pi * u)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s06")
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.msg = self.actors["msg"] = C.make_actor("msg", "messenger", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.dress()
        import bpy
        self.pal_root = bpy.data.objects.new("pal_root", None)
        bpy.context.scene.collection.objects.link(self.pal_root)
        self.pal = TG.STATE["palette"]
        for o in self.pal:
            o.parent = self.pal_root
        self.pal0 = Vector(self.A["marks"]["palette_floor"])

    def dress(self):
        """denser foreground (jars, canvases) 1-2 D from the lens; the preset's own FG belongs to the preset camera."""
        S = TG.STATE
        for o in S.get("fg", []):
            o.hide_render = True
        loc0 = Vector(CAM.at(GF)[0]) / K.SC
        look = Vector(CAM_LOOK0) / K.SC
        items = [("jars", 0.95, 1.0), ("canvases", -1.6, 1.6)]
        S["fg2"] = SD.fg_dress(S, S["M"], tuple(loc0), tuple(look), items, seed=11)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.mor, f, tuple(mor_pos(g)))
            C.place(self.msg, f, tuple(N0))
            z = fall_z(g)
            C.key_vis(self.pal, z is not None, f)
            if z is not None:
                tgt = mor_pos(g) + Vector((0.3, -0.5, 0.0))
                off = tgt - self.pal0
                self.pal_root.location = (off.x, off.y, z)
                self.pal_root.rotation_euler = (0.0, 0.0, 0.5 * u_of(g, *G_FALL))
                self.pal_root.keyframe_insert("location", frame=f)
                self.pal_root.keyframe_insert("rotation_euler", frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, pose_mor(g), camera=self.cam)
            self.msg.pose(f, pose_msg(g), camera=self.cam)
        self.sprites_for([(self.mor, PPD), (self.msg, PPD)], [bf(g) for g in gs])

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
