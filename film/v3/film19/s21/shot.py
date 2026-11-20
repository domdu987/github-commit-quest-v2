#!/usr/bin/env python3
"""shot.py -- film 19 take s21 = shot 21, SHIP ship_coast DAY_BARBADOS.  Shot g 1665..1755; handles 9 in (g 1656..1664, dissolve 13 in) and
9 out (g 1756..1764, dissolve 11 out).  Take g 1656..1764, 109 frames.
"รอบสองที่บาร์เบโดส นาฬิกาแม่นกว่าวิธีดวงจันทร์อีก": William stands calmly on the Barbados beach (mark shore_a) with the H4 on his open
palm; astro19_c (sent by the Board, at shore_c) fumbles a big brass quadrant at the sky beside him (wobbling, tipping, hop).  Camera on
the dry sand, world-fixed, moving from the first frame; SNAP on "นาฬิกาแม่น" (56.52, event g 1699) pushing toward William and the watch.
Mouths: nobody speaks.  NO DOF, NO text, NO caption_shade.
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(55.49), C.g_bound(58.53)   # 1665, 1756: shot 21 = g 1665..1755
H_IN, H_OUT = 9, 9
GF, GL = G0 - H_IN, G1 + H_OUT - 1            # 1459 .. 1589
GS = list(range(GF, GL + 1))
G_WORD = C.cap_g("นาฬิกาแม่น")                 # 1699
SNAP = (G_WORD - 1, G_WORD + 12)

LIGHT, PRESET = "DAY_BARBADOS", "ship_coast"
FINAL_SPP = 12
PPD = 192

CAM_LOC0 = (452.5, 61.0, 3.6)
CAM_LOOK0 = (445.0, 61.6, 2.5)                 # subject point: William's chest
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GF, GL, push=0.06, slide_px=10.0, rise_px=0.0, arc_deg_s=-7.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.5, peak=1.6, shift=(0.65, 0.2))])


def _mix(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


def william_pose(g):
    p = dict(cast19.STORY19["william_show_h4"][1])
    p["arm_r"] = dict(p["arm_r"], hand=(0.64 + 0.015 * math.sin(g * 0.15), 0.62 + 0.02 * math.sin(g * 0.11)))
    p["expr"] = "happy"
    p["mouth"] = "smile"
    p["yaw"] = 0.15
    p["head_roll"] = -3 + 1.5 * math.sin(g * 0.09)
    p["lean"] = 1.0 * math.sin(g * 0.07)
    p["gaze"] = (-0.4, 0.0) if g > G_WORD + 20 else (0.0, 0.0)      # a sideways glance at the astronomer's trouble
    p["blink"] = blink(g, [1672, 1718, 1750])
    p["t"] = g / 30.0
    return p


def astro_pose(g):
    """astro19_c fumbles a big quadrant: it wobbles and tips, he sways and hops, the face goes from smug to worried"""
    p = dict(cast19.STORY19["william_quadrant_sun"][1])
    for k in ("glint",):
        p.pop(k, None)
    w1 = math.sin(g * 0.37)
    w2 = math.sin(g * 0.23 + 1.0)
    p["arm_r"] = dict(hand=(0.50 + 0.10 * w2, 0.05 + 0.10 * w1), bend=-0.7, stretch=1.1, layer="top")
    p["arm_l"] = dict(hand=(-0.5 + 0.2 * w1, 0.80 + 0.25 * w2), bend=0.6, shape="open", layer="top")
    p["prop_r"] = dict(type="quadrant19", angle=-62 + 26 * w1 + 10 * w2, scale=1.5)
    p["yaw"] = 0.35
    p["pitch"] = -0.6
    p["expr"] = "worried" if g > G_WORD - 10 else "determined"
    p["gaze"] = (0.4, -0.9)
    p["lean"] = -4 + 9 * w2
    p["head_roll"] = 5 * w1
    p["legs"] = "wide"
    p["blink"] = blink(g, [1680, 1730])
    p["t"] = g / 30.0
    return p


def hop_z(g):
    return 0.05 * max(0.0, math.sin(g * 0.37 + 1.5)) ** 2


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s21")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(GF), *CAM.at(GF))
        self.scene.frame_set(bf(GF))
        sd = os.path.join(WORK, "sprites")
        self.wil = self.actors["wil"] = C.make_actor("wil", "william19", sd, contact=True, cam=self.cam)
        self.ast = self.actors["ast"] = C.make_actor("ast", "astro19_c", sd, contact=True, cam=self.cam)
        M = self.A["marks"]
        self.mw = Vector(M["shore_a"]) + Vector((0.0, 0.5, 0.0))
        self.ma = self.mw + Vector((0.0, -1.7, 0.0))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.wil, f, self.mw)
            C.place(self.ast, f, self.ma + Vector((0, 0, hop_z(g))))
            self.key_set(f, sea=(g - GF) / 30.0, roll=(g - GF) / 30.0)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.wil.pose(f, william_pose(g), camera=self.cam)
            self.ast.pose(f, astro_pose(g), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.wil, PPD), (self.ast, PPD)], fr)

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
