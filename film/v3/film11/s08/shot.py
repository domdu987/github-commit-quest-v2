#!/usr/bin/env python3
"""s08: film 11 shot 8 (16.95-18.17 s, g 508..544) garden_hut / A, closer: the gag he imagines.  James (james_horns pose) on the stool,
horns 0 -> 1 and cow ears popping out ("งอกเขาวัว" 17.01 s = g 513..), puzzled; Blossom in the garden behind him chews, flicks an ear and lifts her
head to moo.  Towndoc off screen: nobody speaks.  Red dot sore on his upper arm.  Handles 6 frames each side."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c11 as C
from c11 import lerp, clamp, u_of, blink, bf
cast11, actors = C.cast11, C.actors
from mathutils import Vector
TMP = os.path.join(HERE, "work")
G0, G1, H = C.g_bound(16.95), C.g_bound(18.17), 6
FIRST, LAST = G0 - H, G1 + H - 1
PRESET = "garden_hut"
JAMES = Vector((-8.0, -3.4, 0.13))
BLOSSOM = Vector((-8.9, 3.3, 0.0))
G_HORN = (C.g_of(17.01) - 2, C.g_of(17.01) + 14)           # 511..527
G_MOO = (C.g_of(17.6), C.g_of(18.1))
CAM0 = (Vector((-4.4 + 0.24, -4.9 + 0.66, 1.95)), Vector((-8.1 + 0.24, -3.5 + 0.66, 1.95)))
CAM1 = (CAM0[0].lerp(CAM0[1], 0.14), Vector((-8.1 + 0.24, -3.5 + 0.66, 2.0)))

def cam_of(g):
    x = clamp((g - FIRST) / float(LAST - FIRST)); u = 0.3 * (0.5 - 0.5 * math.cos(math.pi * x)) + 0.7 * x
    return CAM0[0].lerp(CAM1[0], u), CAM0[1].lerp(CAM1[1], u)

def pose_james(g):
    base = dict(cast11.STORY11["james_horns"][1]); p = dict(base)
    h = u_of(g, *G_HORN)
    p.update(horns=h, cow_ears=u_of(g, G_HORN[0] + 3, G_HORN[1] + 2), stool=0, yaw=-0.35, gaze=(-0.7, 0.1), expr="worried", mouth="wavy", fx=[], blink=blink(g, 74, 19), t=g / 30.0)
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 0.17) * (0.4 + h)
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.11)
    return p

def pose_blossom(g):
    ear = max(0.0, math.sin((g - G_HORN[0]) * 0.5)) if g > G_HORN[0] else 0.0
    moo = u_of(g, G_MOO[0] - 6, G_MOO[0]) * (1 - u_of(g, G_MOO[1], G_MOO[1] + 8))
    return dict(chew=g / 12.0, chew_amp=lerp(0.6, 1.5, moo), head_down=lerp(0.0, -0.5, moo), ear=ear, tail=0.6 * math.sin(g / 9.0), blink=blink(g, 60, 5), mirror=True)

class Take(C.Take):
    def __init__(self):
        C.Take.__init__(self, PRESET, name="cam_s08")
        sd = os.path.join(TMP, "sprites")
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd, contact=False)
        self.blo = self.actors["blo"] = C.make_actor("blo", "blossom", sd, canvas=cast11.CANVAS11["blossom"])
        self.sore = C.Sore(os.path.join(TMP, "sore"), size=0.14)
    def pose(self, gs):
        for g in gs:
            f = bf(g); loc, look = cam_of(g); self.key_cam(f, loc, look)
            C.place(self.jam, f, JAMES); C.place(self.blo, f, BLOSSOM)
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.jam.pose(f, pose_james(g), camera=self.cam); self.blo.pose(f, pose_blossom(g), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.jam, 384), (self.blo, 192)], fr)
        for g in gs:
            f = bf(g); loc, _ = cam_of(g)
            self.sore.key(f, "dot", self.world_anchor(self.jam, "upper_arm_l", f), loc)
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
