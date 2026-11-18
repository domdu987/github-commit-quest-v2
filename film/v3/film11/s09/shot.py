#!/usr/bin/env python3
"""s09: film 11 shot 9 (18.17-20.71 s, g 545..620) lane_high / A: Jenner walks the lane with his notebook; villagers point and laugh
(laugh / point poses, pockmarked a/b/c among them), nickname "ไอ้หมอวัว"; the camera follows him.  Handles 6 frames each side.
Red dot sore: Jenner's patient is not on screen, so no sore here."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c11 as C
from c11 import lerp, clamp, u_of, blink, bf
cast11, actors = C.cast11, C.actors
from mathutils import Vector
TMP = os.path.join(HERE, "work")
G0, G1, H = C.g_bound(18.17), C.g_bound(20.71), 6
FIRST, LAST = G0 - H, G1 + H - 1
PRESET = "lane_high"
V_PER_FRAME = 0.060
J_X0, J_Y = 4.6, -14.4
def jenner_x(g): return J_X0 - V_PER_FRAME * (g - FIRST)
CROWD = [  # slot (unused), cast, pos: two rows along the north side of the lane; Jenner walks in front of them
    ("c0", "villager_a", (-6.5, -12.0)), ("c1", "villager_d", (-3.0, -12.3)), ("c2", "villager_b", (0.5, -12.0)), ("c3", "villager_c", (3.8, -12.3)),
    ("c5", "villager_e", (-4.8, -10.0)), ("c6", "villager_d", (-1.2, -10.0)), ("c7", "villager_a", (2.2, -10.0))]
REL = Vector((4.2, -9.0, 4.6))            # camera offset from its target

def cam_of(g):
    x = clamp((g - FIRST) / float(LAST - FIRST))
    tx = jenner_x(FIRST) + 0.75 * (jenner_x(g) - jenner_x(FIRST)) - 1.0      # slower than he walks: he gains on the frame edge ahead (lead room, screen-left)
    tgt = Vector((tx, -13.0, 1.7)); k = lerp(1.0, 0.86, x)      # slow pull-back while tracking
    return tgt + REL * k, tgt

def pose_jenner(g):
    base = dict(cast11.STORY11["jenner_write"][1]); base.pop("mirror", None)
    b = dict(prop_r="notebook", expr="neutral", mouth="smile", yaw=0.75)
    b["arm_r"] = dict(hand=(0.55, 0.95), bend=0.5)
    p = cast11.cycle("jenner", g / 28.0, "walk", facing=-1, base=b, arms="l", speed=1.0)
    p["blink"] = blink(g, 80, 13); p["t"] = g / 30.0
    return p

def vill_state(i, g):
    ph = (g + 9 * i) % 40
    return "point" if ph < 22 else "laugh"

class Take(C.Take):
    def __init__(self):
        C.Take.__init__(self, PRESET, name="cam_s09")
        sd = os.path.join(TMP, "sprites")
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.v = []
        for i, (slot, cast, xy) in enumerate(CROWD):
            a = self.actors["v%d" % i] = C.make_actor("v%d" % i, cast, sd); self.v.append(a)
        self.mir = [False] * len(CROWD)
    def pose(self, gs):
        mir = [None] * len(CROWD)
        for g in gs:
            f = bf(g); loc, look = cam_of(g); self.key_cam(f, loc, look)
            C.place(self.jen, f, (jenner_x(g), J_Y, 0.0))
            for i, (slot, cast, xy) in enumerate(CROWD):
                C.place(self.v[i], f, (xy[0], xy[1], 0.0))
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            self.jen.pose(f, pose_jenner(g), camera=self.cam)
            for i, (slot, cast, xy) in enumerate(CROWD):
                st = vill_state(i, g); want = jenner_x(g) < xy[0]          # Jenner screen-left of him (-x) -> point / look left (mirror)
                if mir[i] is None: mir[i] = want
                if want != mir[i] and st == "laugh": mir[i] = want
                p = dict(cast11.STORY11["%s_%s" % (cast, st)][1]); p["mirror"] = mir[i]
                p["blink"] = blink(g, 70, 5 * i); p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin(g * 0.3 + i)
                p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.37 + 2 * i) * (1.5 if st == "laugh" else 0.5)
                self.v[i].pose(f, p, camera=self.cam)
        fr = [bf(g) for g in gs]
        self.sprites_for([(self.jen, 160)] + [(a, 128) for a in self.v], fr)
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
