#!/usr/bin/env python3
"""shot.py -- film 19 take s19 = shot 19, SHIP ship_coast DAY_JAMAICA.  Shot g 1468..1580; handles 9 in (g 1459..1467, dissolve 13 in) and
9 out (g 1581..1589, hard cut to shot 20).  First frame of the take g 1459, last 1589, 131 frames.
"ถึงฝั่ง นาฬิกาคลาดไปแค่ห้าวินาที แม่นกว่าที่รางวัลกำหนดซะอีก": the ship has anchored in the bay; William stands on the Jamaican beach
(mark shore_a) and holds the H4 high in one hand and his tricorne in the other; two sailors (shore_b, and one at the left) cheer with
arms up.  Camera on the dry sand (preset ship_coast, world-fixed: the beach is not the ship), moving from the first frame.
    g 1459..1480  William lifts the watch (arm rises), sailors begin to cheer
    g 1496..1509  SNAP push + pan to William's watch on "แค่ห้าวินาที" (caption 49.80 = event g 1497)
    g 1510..1589  hold the cheer: bounce, hats up
Mouths: nobody speaks (expression mouths only).  NO DOF, NO text, NO caption_shade.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(48.92), C.g_bound(52.71)   # 1468, 1581: shot 19 = g 1468..1580
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1            # 1459 .. 1589
GS = list(range(GF, GL + 1))
G_WORD = C.cap_g("แค่ห้าวินาที")               # 1497
SNAP = (G_WORD - 2, G_WORD + 12)
G_LIFT = (GF, GF + 20)

LIGHT, PRESET = "DAY_JAMAICA", "ship_coast"
FINAL_SPP = 12
PPD = 192

CAM_LOC0 = (452.0, 61.2, 3.55)                 # near the preset start pose, 25 % closer to the subject
CAM_LOOK0 = (446.0, 61.0, 2.6)                 # subject point: William's chest
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=0.04, slide_px=-4.0, rise_px=6.0, arc_deg_s=-14.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.65, peak=1.5, shift=(1.9, 0.25))])


def _mix(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


def william_pose(g):
    p = dict(cast19.STORY19["william_cheer_hat"][1])
    u = u_of(g, *G_LIFT, kind="sine")
    hi = _mix((0.5, 0.55), (0.80, -0.72), u)
    p["arm_r"] = dict(hand=(hi[0], hi[1] + 0.05 * math.sin(2 * math.pi * g / 14.0)), bend=-0.4, stretch=1.3, shape="open", layer="top")
    p["prop_r"] = "h4_watch"
    p["arm_l"] = dict(hand=(-0.70, -0.62 + 0.05 * math.sin(2 * math.pi * g / 14.0 + 1.0)), bend=-0.5, stretch=1.3, shape="open", layer="top")
    p["prop_l"] = "tricorn_held"
    p["mirror"] = True
    p["expr"] = "happy"
    p["mouth"] = "grin"
    p.pop("fx", None)
    p["yaw"] = 0.25
    p["pitch"] = -0.25
    p["head_roll"] = -4 + 3 * math.sin(g * 0.2)
    p["blink"] = blink(g, [1470, 1520, 1562])
    p["t"] = g / 30.0
    return p


def sailor_pose(name, g, ph):
    p = dict(cast19.STORY19[name + "_cheer"][1])
    s = math.sin(2 * math.pi * g / 10.0 + ph)                     # ~3 Hz cheer
    p["arm_r"] = dict(p["arm_r"], hand=(0.74, -0.74 + 0.12 * s))
    p["arm_l"] = dict(p["arm_l"], hand=(-0.74, -0.7 - 0.12 * s))
    p["blink"] = blink(g, [1478 + int(ph * 5), 1540])
    p["t"] = g / 30.0
    return p


def bounce_z(g, ph, amp=0.06):
    return amp * abs(math.sin(math.pi * g / 10.0 + ph))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s19")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        sd = os.path.join(WORK, "sprites")
        self.wil = self.actors["wil"] = C.make_actor("wil", "william19", sd, contact=True, cam=self.cam)
        self.sa = self.actors["sa"] = C.make_actor("sa", "sailor_a", sd, contact=True, cam=self.cam)
        self.sb = self.actors["sb"] = C.make_actor("sb", "sailor_b", sd, contact=True, cam=self.cam)
        M = self.A["marks"]
        self.mw = Vector(M["shore_a"])
        self.ma = Vector(M["shore_b"]) + Vector((-0.4, -0.3, 0.0))
        self.mb = Vector(M["shore_c"]) + Vector((0.5, 2.1, 0.0))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.wil, f, self.mw + Vector((0, 0, bounce_z(g, 0.0, 0.04))))
            C.place(self.sa, f, self.ma + Vector((0, 0, bounce_z(g, 1.3))))
            C.place(self.sb, f, self.mb + Vector((0, 0, bounce_z(g, 2.6))))
            self.key_set(f, sea=(g - GF) / 30.0, roll=(g - GF) / 30.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.wil.pose(f, william_pose(g), camera=self.cam)
            self.sa.pose(f, sailor_pose("sailor_a", g, 1.3), camera=self.cam)
            self.sb.pose(f, sailor_pose("sailor_b", g, 2.6), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.wil, PPD), (self.sa, PPD), (self.sb, PPD)], fr)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print([r["px"] for r in rows][::4])
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
