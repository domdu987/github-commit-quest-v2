#!/usr/bin/env python3
"""shot.py -- film 19 take (shot 15 or 16: SHIP ship_deck NOON; set SHOT below).
Shot 15 (36.52-39.67 s): "ความลับคือ เที่ยงวันกลางทะเล ดวงอาทิตย์อยู่ตรงหัว": william19 aims the brass quadrant straight at the sun,
  set_sun_overhead 0 -> 1 keyed on every frame (the mast shadow shrinks to its foot); the camera cranes up toward the sun, settles,
  and SNAPS on "อยู่ตรงหัว" (38.98 = g 1172).  Captain at the wheel looks up too.
Shot 16 (39.67-42.65 s): "แต่นาฬิกายังบอกเวลาที่บ้าน": william19 holds the H4 out on his palm toward the camera (captain looks on);
  push to the watch with the wheel / rail in the foreground, snap on "บอกเวลา" (40.5 = g 1218).
Both: cards are parented to ship_root (C.ride_ship) and the camera rides the deck (C.on_ship); set_sea(t) / set_roll(t) / set_sun_overhead
keyed with the same t on EVERY frame.  No DOF, no text, no caption_shade.

    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

SHOT = 16
CFG = {
    15: dict(t0=36.52, t1=39.67, h_in=10, h_out=9, snap_word="อยู่ตรงหัว"),
    16: dict(t0=39.67, t1=42.65, h_in=9, h_out=9, snap_word="บอกเวลาที่"),
}[SHOT]
G0, G1 = C.g_bound(CFG["t0"]), C.g_bound(CFG["t1"])      # shot = g G0 .. G1-1
G_FIRST, G_LAST = G0 - CFG["h_in"], G1 + CFG["h_out"] - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP = C.cap_g(CFG["snap_word"])
SNAP = (G_SNAP - 8, G_SNAP + 12)                          # 20 frames
LIGHT, PRESET = "NOON", "ship_deck"
FINAL_SPP = 11
PPD = 384
BLINKS_W = [G0 + 22, G0 + 71] if SHOT == 15 else [G0 + 30, G0 + 80]
BLINKS_C = [G0 + 9, G0 + 60]

TS0 = G0 / 30.0                                           # sun overhead ramp: 0 at the shot start (shot 15), 1 from the snap word on


def sun_k(g):
    if SHOT == 16:
        return 1.0
    return clamp((g - (G0 - 10)) / float(G_SNAP + 4 - (G0 - 10)), 0.0, 1.0) ** 1.0


# ---- camera (rest frame of the deck: world D at t = 0) ------------------------------------------------------------
CAM_LOC0 = (-1.11, -39.59, 17.1125)                       # preset start
if SHOT == 15:
    CAM_LOOK0 = (0.55, -31.4, 15.3)
    CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.07, slide_px=-12.0, rise_px=30.0, arc_deg_s=0.0, decay=0.2,
                    snaps=[dict(g=SNAP, k=1.2, peak=1.8, shift=(0.0, 0.10))])
else:
    # continuity with s15: the cut lands on the framing s15 ends on (same rest-frame pose at g 1190), then a push to the watch
    _c15 = C.CamPath((-1.11, -39.59, 17.1125), (0.55, -31.4, 15.2), 1086, 1198, push=0.10, slide_px=-30.0, rise_px=0.0, arc_deg_s=5.0,
                     decay=0.2, snaps=[dict(g=(1166, 1182), k=1.5, peak=1.8, shift=(0.85, 2.0))])
    CAM_LOC0, CAM_LOOK0 = _c15.at(1190)
    CAM_LOC0 = CAM_LOOK0 + (CAM_LOC0 - CAM_LOOK0) * 1.8          # a little wider than s15's last frame, so both stay in frame through the push
    CAM_LOOK0 = CAM_LOOK0 + Vector((0.0, 0.0, 1.0))
    CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, 1190, G_LAST, push=0.10, slide_px=20.0, rise_px=-15.0, arc_deg_s=-6.0, decay=0.15,
                    snaps=[dict(g=SNAP, k=1.6, peak=1.4, shift=(0.0, -1.5))])

CAP_OFF = Vector((0.8, 1.7, 0.0)) if SHOT == 15 else Vector((1.5, 1.1, 0.0))   # s16: the captain stands close beside William so both fit at the push

# ---- poses ---------------------------------------------------------------------------------------------------------
W_Q = cast19.STORY19["william_quadrant_sun"][1]
W_H4 = cast19.STORY19["william_show_h4"][1]
C_IDLE = cast19.STORY19["captain_idle"][1]


def william_pose(g):
    t = g / 30.0
    if SHOT == 15:
        p = dict(W_Q)
        u = u_of(g, G_SNAP - 4, G_SNAP + 8)                       # the quadrant thrusts up on "อยู่ตรงหัว"
        sway = math.sin(2 * math.pi * g / 40.0)
        p["arm_r"] = dict(hand=(0.46 + 0.02 * sway, 0.10 - 0.10 * u), bend=-0.7, stretch=1.1, layer="top")
        p["prop_r"] = dict(type="quadrant19", angle=-62 + 3.0 * sway - 6.0 * u, scale=0.95)
        p["glint"] = 0.5 + 0.5 * math.sin(2 * math.pi * g / 12.0) if g >= G_SNAP - 6 else 0.4
        p["lean"] = -3 - 1.5 * u + 0.8 * math.sin(g * 0.2)
        p["gaze"] = (0.5, -0.9)
    else:
        p = dict(W_H4)
        u = u_of(g, G_SNAP - 4, G_SNAP + 12)
        p["arm_r"] = dict(hand=(0.30 - 0.06 * u, 0.86), bend=-0.2, shape="open", stretch=1.15, layer="top")
        p["prop_r"] = dict(type="h4_watch", scale=2.0)            # the H4 at 2x so it reads on a phone, held in front of the chest
        p["yaw"] = 0.10
        p["gaze"] = (0.0, 0.2)
        p["lean"] = 2.0 * math.sin(g * 0.13)
        p["head_roll"] = -3.0 + 1.5 * math.sin(g * 0.11)
    p["blink"] = blink(g, BLINKS_W)
    p["t"] = t
    return p


def captain_pose(g):
    p = dict(C_IDLE)
    p["yaw"] = 0.25
    p["lean"] = 1.0 * math.sin(g * 0.09)
    p["head_roll"] = 1.5 * math.sin(g * 0.07 + 1.0)
    if SHOT == 15:
        p["pitch"] = -0.35                                          # looks up at the sun (squint)
        p["gaze"] = (0.5, -0.8)
        p["expr"] = "determined"
    else:
        p["pitch"] = 0.05
        p["gaze"] = (0.9, 0.2)                                      # at William's watch
        p["expr"] = "neutral"
    p["blink"] = blink(g, BLINKS_C)
    p["t"] = g / 30.0
    return p


# ---- the take --------------------------------------------------------------------------------------------------------
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s%02d" % SHOT)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.root = self.A["ship_root"]
        f0 = bf(G_FIRST)
        H.set_sea(G_FIRST / 30.0, frame=f0)
        H.set_roll(G_FIRST / 30.0, frame=f0)
        self.key_cam(f0, *C.on_ship(self.root, f0, *CAM.at(G_FIRST)))
        self.scene.frame_set(f0)
        self.wil = self.actors["wil"] = C.make_actor("wil", "william19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.cap = self.actors["cap"] = C.make_actor("cap", "captain19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        # the parent inverse must be taken with the ship LEVEL (t = 0): key set_roll(0) on frame 1 and evaluate it there
        H.set_roll(0.0, frame=1)
        self.scene.frame_set(1)
        for a in (self.wil, self.cap):
            C.ride_ship(a, self.root)

    def pose(self, gs):
        M = self.A["marks"]
        for g in gs:
            f = bf(g)
            t = g / 30.0
            H.set_sea(t, frame=f)
            H.set_roll(t, frame=f)
            H.set_sun_overhead(sun_k(g), frame=f)
            self.key_cam(f, *C.on_ship(self.root, f, *CAM.at(g)))
            C.place(self.wil, f, Vector(M["william_deck"]))
            C.place(self.cap, f, Vector(M["captain_wheel"]) + CAP_OFF)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.wil.pose(f, william_pose(g), camera=self.cam)
            self.cap.pose(f, captain_pose(g), camera=self.cam)
        self.sprites_for([(self.wil, PPD), (self.cap, 256)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], sun=round(sun_k(g), 3), heads=C.head_report(self, f),
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
