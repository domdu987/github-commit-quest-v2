#!/usr/bin/env python3
"""s07: film 11 shot 7 (15.80-16.95 s, g 474..507) garden_hut / A two-shot: towndoc point_mock at James (lip-sync, quote window),
James seated on the hut stool (red dot sore on his upper arm), Jenner calm with his notebook.  Handles: 6 frames each side.
    python3 shot.py stills a:b[:step] outdir [scale] [samples]     python3 shot.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c11 as C
from c11 import lerp, clamp, u_of, blink, bf
cast11, actors = C.cast11, C.actors
from mathutils import Vector
TMP = os.path.join(HERE, "work")
G0, G1, H = C.g_bound(15.80), C.g_bound(16.95), 6          # 474, 508
FIRST, LAST = G0 - H, G1 + H - 1
PRESET = "garden_hut"
SE = {}                                                    # filled in __main__

JAMES = Vector((-8.0, -3.4, 0.13))   # sprite has no stool of its own (stool=0): his seat sits on the set stool top
RV = Vector((0.34, 0.94, 0.0))                             # screen-right on the ground for the camera below
DOC = Vector((-8.95, -6.0, 0.0))
JEN = Vector((-7.2, -1.3, 0.0))
CAM0 = (Vector((-1.0, -8.0, 1.8)), Vector((-9.1, -3.0, 2.0)))
CAM1 = (CAM0[0].lerp(CAM0[1], 0.13) + Vector((0, 0, 0.05)), Vector((-9.0, -3.0, 2.05)))

def cam_of(g):
    x = clamp((g - FIRST) / float(LAST - FIRST)); u = 0.3 * (0.5 - 0.5 * math.cos(math.pi * x)) + 0.7 * x
    return CAM0[0].lerp(CAM1[0], u), CAM0[1].lerp(CAM1[1], u)

def pose_doc(g):
    p = dict(cast11.STORY11["towndoc_point_mock"][1]); p["mouth"] = cast11.talk_mouth(g, 1.0); p["blink"] = blink(g, 70, 11)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.21); p["t"] = g / 30.0
    return p

def pose_james(g):
    p = dict(cast11.STORY11["james_sit_sleeve"][1]); p["blink"] = blink(g, 80, 23); p["t"] = g / 30.0
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.13); p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.09)
    p["expr"] = "worried"; p["stool"] = 0
    return p

def pose_jen(g):
    p = dict(cast11.STORY11["jenner_write"][1]); p["blink"] = blink(g, 95, 41); p["mirror"] = True; p["t"] = g / 30.0
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.11)
    return p

class Take(C.Take):
    def __init__(self):
        C.Take.__init__(self, PRESET, name="cam_s07")
        sd = os.path.join(TMP, "sprites")
        self.doc = self.actors["doc"] = C.make_actor("doc", "towndoc", sd)
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd, contact=False)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.sore = C.Sore(os.path.join(TMP, "sore"))
        self.stool = None
    def pose(self, gs):
        for g in gs:
            f = bf(g); loc, look = cam_of(g); self.key_cam(f, loc, look)
            C.place(self.doc, f, DOC); C.place(self.jam, f, JAMES); C.place(self.jen, f, JEN)
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.doc.pose(f, pose_doc(g), camera=self.cam); self.jam.pose(f, pose_james(g), camera=self.cam); self.jen.pose(f, pose_jen(g), camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.doc, 320), (self.jam, 320), (self.jen, 320)], fr)
        for g in gs:
            f = bf(g); loc, _ = cam_of(g)
            w = self.world_anchor(self.jam, "upper_arm_l", f)
            self.sore.key(f, "dot", w, loc)
    def report(self, g):
        loc, look = cam_of(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=self.head_report(bf(g)))
    def render_g(self, g, out, **k):
        return C.Take.render(self, [bf(g)], out, **k)

if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    Tk = Take()
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            st = Tk.render_g(g, out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(Tk, gs, HERE, scale=scale, samples=samples)
