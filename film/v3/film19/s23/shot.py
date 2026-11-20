#!/usr/bin/env python3
"""shot.py -- film 19 take s23 = shot 23 (HALL hall_door EVENING): "ตอนเขาอายุเกือบแปดสิบ พระราชาได้ยินเรื่องนี้".
Old Harrison (old=1) shuffles in through the panelled double door toward the camera, holding his new watch (h4_watch) on his palm.
g 1856..1932 = the shot (61.86-64.44 s); in-handle 9 f (dissolve 15 f in), out-handle 9 f (hard cut to shot 24).
Camera: crane DOWN + push from a high start (c19.CamPath, rise_px < 0), snap on "พระราชา" (caption 63.18 -> g 1898).
Hooks keyed every frame: set_candles flicker, set_regulator(True).  No DOF, no text, no caption_shade.

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

G0, G1 = C.g_bound(61.86), C.g_bound(64.44)            # 1856, 1933 (exclusive)
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP = C.cap_g("พระราชา")
SNAP = (G_SNAP - 2, G_SNAP + 18)
PRESET, LIGHT, FINAL_SPP, PPD = "hall_door", "EVENING", 8, 256
BLINKS = [1872, 1905, 1925]

D_START = Vector((0.0, -7.60, 0.0))     # in the corridor beyond the doorway (door mark is y -5.55): he walks THROUGH the door
D_END = Vector((0.55, -4.00, 0.0))
CAM_LOC0 = (2.95, 0.45, 2.20)
CAM_LOOK0 = (0.30, -4.60, 2.50)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.06, slide_px=-135.0, rise_px=-35.0, arc_deg_s=30.0, decay=0.12,
                snaps=[dict(g=SNAP, k=1.75, peak=2.3, shift=(6.00, -0.25))])

BASE = dict(cast19.STORY19["harrison_old_handover"][1])
CYC = 34.0


def walk_u(g):
    return clamp((g - G_FIRST) / float(G_LAST - G_FIRST))


def pos(g, mark):
    u = ez(walk_u(g) * 0.15 + walk_u(g) * 0.85, "sine") * 0.0 + walk_u(g)         # steady shuffle
    p = D_START + (D_END - D_START) * u
    return p


def pose_of(g):
    base = dict(BASE)
    base.pop("legs", None)
    base.update(yaw=0.30, pitch=0.08, gaze=(0.0, 0.3), head_roll=-2.0, expr="happy", mouth="smile")
    base["arm_r"] = dict(hand=(0.62, 0.84), bend=-0.1, shape="open", stretch=1.1, layer="front")
    base["prop_r"] = "h4_watch"
    p = cast19.cycle("harrison19", (g - G_FIRST) / CYC, "walk", 1, base=base, arms="l", speed=0.80)
    p["old"] = 1
    p["lean"] = 8.0 + 1.0 * math.sin(g * 0.22)
    p["mirror"] = False
    p["arm_r"] = dict(hand=(0.60, 0.86 + 0.03 * math.sin(g * 0.22)), bend=-0.1, shape="open", stretch=1.1, layer="front")
    p["prop_r"] = "h4_watch"
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s23")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), contact=dict(width=1.1, depth=0.5, opacity=0.8), cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.har, f, pos(g, None))
            self.key_set(f, candles=1.0, regulator=True)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

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
