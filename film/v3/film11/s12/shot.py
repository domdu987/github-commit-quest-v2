#!/usr/bin/env python3
"""s12: film 11 shot 12 (24.10-25.86 s, g 723..775) room_day / A: "day 7": James sits on the bed edge rubbing his armpit with a wince, blister on his upper arm;
mother stand_worried.  Handles 6 frames each side."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c11 as C
from c11 import lerp, clamp, u_of, blink, bf
cast11, actors = C.cast11, C.actors
from mathutils import Vector
TMP = os.path.join(HERE, "work")
G0, G1, H = C.g_bound(24.10), C.g_bound(25.86), 6
FIRST, LAST = G0 - H, G1 + H - 1
PRESET = "room_day"
JAMES = Vector((-3.55, 4.6, 1.33))        # seat z 1.80 (quilt top) minus the sprite's seat height 0.47 (stool=0, hips on the quilt)
JEN = Vector((-2.19, 5.62, 0.0))
MOM = Vector((-1.7, 6.6, 0.0))
SORE = "blister"
CAM0 = (Vector((0.6, -0.1, 2.5)), Vector((-3.0, 5.1, 2.3)))
CAM1 = (CAM0[0].lerp(CAM0[1], 0.14), Vector((-3.05, 5.1, 2.3)))
def cam_of(g):
    x = clamp((g - FIRST) / float(LAST - FIRST)); u = 0.3 * (0.5 - 0.5 * math.cos(math.pi * x)) + 0.7 * x
    return CAM0[0].lerp(CAM1[0], u), CAM0[1].lerp(CAM1[1], u)

def pose_james(g):
    """sits on the bed edge, faces screen-right (mirror), rubs the armpit of the sore arm with the other hand (circles), wince (worried + head roll)."""
    p = dict(cast11.STORY11["james_sit_sleeve"][1]); p.update(stool=0, mirror=True, expr="worried", mouth="frown", yaw=-0.3, gaze=(-0.4, 0.5),
                                                           blink=blink(g, 60, 23), t=g / 30.0)
    w = 0.5 - 0.5 * math.cos(math.pi * clamp((g - FIRST) / 8.0))
    cx, cy = -0.30 + 0.07 * math.sin(g * 0.55), 0.92 + 0.06 * math.cos(g * 0.55)
    p["arm_r"] = dict(hand=(lerp(0.3, cx, w), lerp(1.1, cy, w)), bend=0.6, layer="front")
    p["arm_l"] = dict(hand=(-0.45, 1.0), bend=0.3)                       # the sore arm held a little out from the side
    p["head_roll"] = 6.0 + 2.0 * math.sin(g * 0.21); p["lean"] = -4.0 + 1.2 * math.sin(g * 0.17); p["pitch"] = 0.15
    return p
def pose_jen(g):
    p = dict(cast11.STORY11["jenner_neutral"][1]); p.update(mirror=True, yaw=0.5, lean=9 + 1.5 * math.sin(g * 0.11), blink=blink(g, 95, 41), t=g / 30.0, expr="neutral")
    return p
def pose_mom(g):
    p = dict(cast11.STORY11["mother_stand_worried"][1]); p.update(mirror=True, blink=blink(g, 85, 7), t=g / 30.0)
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.15)
    return p

class Take(C.Take):
    def __init__(self):
        C.Take.__init__(self, PRESET, name="cam_s12")
        sd = os.path.join(TMP, "sprites")
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd, contact=False)
        self.mom = self.actors["mom"] = C.make_actor("mom", "mother", sd)
        self.sore = C.Sore(os.path.join(TMP, "sore"), size=0.16)
    def pose(self, gs):
        for g in gs:
            f = bf(g); loc, look = cam_of(g); self.key_cam(f, loc, look)
            C.place(self.jam, f, JAMES); C.place(self.mom, f, MOM)
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.jam.pose(f, pose_james(g), camera=self.cam); self.mom.pose(f, pose_mom(g), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.jam, 320), (self.mom, 256)], fr)
        for g in gs:
            f = bf(g); loc, _ = cam_of(g)
            self.sore.key(f, SORE, self.world_anchor(self.jam, "upper_arm_r", f), loc)  # mirrored James: anchors are named by screen side, his front arm is *_r
    def report(self, g):
        loc, look = cam_of(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=self.head_report(bf(g)))
    def render_g(self, g, out, **k): return C.Take.render(self, [bf(g)], out, **k)

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    Tk = Take()
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        os.makedirs(out, exist_ok=True); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            st = Tk.render_g(g, out, scale=scale, samples=samples, threads=1)[0]; os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(Tk, gs, HERE, scale=scale, samples=samples)
