#!/usr/bin/env python3
"""shot.py -- film 19 take s06 = shot 6 (HALL hall_table DAY), g 356..465 + 9 in-handle (347..355) + 9 out-handle (466..474).
"สภาเลยตั้งรางวัล ... สองหมื่นปอนด์" (11.88-15.54 s): at "รางวัล" (12.50 -> g 378) a fat money bag DROPS onto the green baize
(set_moneybag('full') keyed at g 378, the pivot keyed to fall, bounce and settle); astro19 (left) and astro19_b (right) lean in, eyes on the bag,
excited.  Camera: push-in on "สองหมื่นปอนด์" (14.81 -> g 447) with a pan.  Mouths flat (no quote).  No DOF, no text, no caption_shade.
Hooks keyed every frame: moneybag state + the bag pivot, candles.

    python3 shot.py probe|stills|final a:b[:step] ...    (as s03)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(11.88), C.g_bound(15.54)    # 356, 466 (exclusive)
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_BAG = C.g_of(12.50)                          # "รางวัล" -> bag drops
G_SNAP_WORD = C.g_of(14.81)                    # "สองหมื่นปอนด์" -> push-in snap
SNAP = (G_SNAP_WORD - 8, G_SNAP_WORD + 8)
LIGHT, PRESET = "DAY", "hall_table"
FINAL_SPP = 8

CAM_LOC0 = (0.3, -2.7, 3.0)
CAM_LOOK0 = (0.0, 2.5, 2.0)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.09, slide_px=-60.0, rise_px=0.0, arc_deg_s=11.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.7, peak=1.4, shift=(1.2, 0.0))])

MARK_A = (-2.05, 2.60, 0.0)                    # astro19, left of the table, faces screen-right
MARK_B = (2.05, 3.05, 0.0)                     # astro19_b, right of the table, faces screen-left (mirror)
BAG_DROP, BAG_FALL, BAG_END = G_BAG, 5, G_BAG + 14


def bag_z(g):
    """metres above rest: falls 1.8 m in 5 f, bounces 0.22 m, then 0.06 m, settles (local metres under the scaled root)."""
    if g < BAG_DROP:
        return 2.0
    t = g - BAG_DROP
    if t < BAG_FALL:
        return 1.8 * (1 - (t / BAG_FALL) ** 2)
    t -= BAG_FALL
    if t < 4:
        return 0.22 * (1 - ((t - 2) / 2.0) ** 2)
    t -= 4
    if t < 3:
        return 0.06 * (1 - ((t - 1.5) / 1.5) ** 2)
    return 0.0


def bag_squash(g):
    t = g - BAG_DROP - BAG_FALL
    return 0.82 if 0 <= t < 1 else (0.92 if 1 <= t < 2 else 1.0)


def lean_u(g):
    return u_of(g, G_BAG + 4, G_BAG + 14, "sine")


def pose_a(g):
    p = dict(cast19.STORY19["astro_idle"][1])
    u = lean_u(g)
    p["mirror"] = False
    p["yaw"] = 0.35
    p["expr"] = "excited" if u > 0.5 else "smug"
    p["lean"] = 2.0 + 12.0 * u + 1.0 * math.sin(g * 0.2)
    p["pitch"] = 0.05 + 0.2 * u
    p["head_roll"] = 4.0 * u * math.sin(g * 0.3)
    p["gaze"] = (0.9, 0.6) if u > 0.2 else (0.2, 0.0)
    p["arm_r"] = dict(hand=(lerp(0.3, 0.95, u), lerp(1.1, 0.6, u)), bend=-0.3, shape="open", layer="top")
    p["arm_l"] = "akimbo"
    p["mouth"] = "flat"
    p["blink"] = blink(g, [372, 425])
    p["squash"] = (1.0 + 0.01 * math.sin(g * 0.4), 1.0)
    return p


def pose_b(g):
    p = dict(cast19.STORY19["astro_b_idle"][1])
    u = lean_u(g)
    p["mirror"] = True
    p["yaw"] = 0.4
    p["expr"] = "excited" if u > 0.5 else "unimpressed"
    p["lean"] = 2.0 + 14.0 * u + 1.0 * math.sin(g * 0.17)
    p["pitch"] = 0.05 + 0.3 * u
    p["head_roll"] = -3.0 * u
    p["gaze"] = (0.9, 0.7) if u > 0.2 else (0.2, 0.0)
    p["arm_r"] = dict(hand=(lerp(0.3, 0.55, u), lerp(1.1, 0.55, u)), bend=0.6, shape="open", layer="top")
    p["arm_l"] = dict(hand=(-0.35, 1.0), bend=0.5)
    p["mouth"] = "flat"
    p["blink"] = blink(g, [365, 410, 455])
    p["legs"] = "stand"
    return p


def bob(g, ph=0.0):
    return 0.012 * math.sin(2 * math.pi * g / 20.0 + ph)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s06")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.ab = self.actors["ab"] = C.make_actor("ab", "astro19_b", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.bag_rest = None
        self.aa = self.actors["aa"] = C.make_actor("aa", "astro19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.ab, f, Vector(MARK_B) + Vector((0, 0, bob(g))))
            C.place(self.aa, f, Vector(MARK_A) + Vector((0, 0, bob(g, 1.7))))
            self.key_set(f, candles=1.0, moneybag="full" if g >= G_BAG else "none")
            pv = H.STATE["hooks"]["bag_full"]
            if self.bag_rest is None:
                self.bag_rest = pv.location.copy()
            pv.location = (self.bag_rest.x, self.bag_rest.y, self.bag_rest.z + bag_z(g))
            pv.scale = (1.0 / math.sqrt(bag_squash(g)), 1.0 / math.sqrt(bag_squash(g)), bag_squash(g))
            pv.keyframe_insert("location", frame=f, options=set())
            pv.keyframe_insert("scale", frame=f, options=set())
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
