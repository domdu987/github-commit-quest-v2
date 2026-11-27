#!/usr/bin/env python3
"""shot_C.py -- film 24 version C take s04: NEW HERO 1, preset hero_yard (yard, backlit finished turtle ship).  g 282..436 (g 288..430 + 6 handles).
Slow eased low push-in toward the look point; Yi (yi24 stand_arms_behind, one nod at the old cue g_of(11.6)) at anchor yi_hero with a warm rim;
dragon smoke every frame (smoke_start).  Blender frame = 3000 + g + 1.
    JOSEON_LOOK=C python3 shot_C.py probe 4 a:b[:s] | stills 4 a:b[:s] <out> [scale] [samples] | final 4 a:b [scale] [samples]
"""
import math, os, sys, json
os.environ.setdefault("JOSEON_LOOK", "C")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J = C.J
blink, bf = C.blink, C.bf
TMP = os.path.join(HERE, "work")
G0, G1, H = C.g_bound(9.60), C.g_bound(14.37), 6
RANGES = {4: (G0 - H, G1 + H - 1)}
PUSH = 0.11                                              # fraction of the way to the look point (eased, low push-in)
G_NOD = C.g_of(11.6)
PPD = 64


def cam_of(g, T):
    pc = T.A["cam"]; loc0, look = Vector(pc["loc"]), Vector(pc["look_at"])
    x = (g - RANGES[4][0]) / float(RANGES[4][1] - RANGES[4][0]); u = C.calm(x)
    loc = loc0 + (look - loc0) * (PUSH * u)
    loc.z = loc0.z + 0.25 * u                              # keep it low, rising a touch
    return loc, look, pc["lens"]


def pose_yi(g):
    c, p = C.story("yi24_stand_arms_behind")
    p["lean"] = 1.0 * math.sin(g * 0.09)
    k = g - G_NOD
    p["pitch"] = (0.28 * math.sin(math.pi * k / 16.0)) if 0 <= k <= 16 else 0.0
    p["blink"] = blink(g, [310, 372, 404]); p["t"] = g / 30.0
    return J.card_rim(p)


class Take(C.Take):
    def __init__(self, shot=4):
        C.Take.__init__(self, "hero_yard", name="cam_s04")
        sd = os.path.join(TMP, "sprites")
        self.yi = self.actors["yi"] = C.make_actor("yi", "yi24", sd)
        self.yi_at = tuple(self.A["marks"]["yi_hero"])

    def pose(self, shot, gs):
        for g in gs:
            f = bf(4, g); self.scene.frame_set(f)
            loc, look, lens = cam_of(g, self); self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=1.0, smoke_start=bf(4, RANGES[4][0]) - 40)
            C.place(self.yi, f, self.yi_at)
        for g in gs:
            f = bf(4, g); self.scene.frame_set(f)
            self.yi.pose(f, pose_yi(g), camera=self.cam)
        self.sprites_for([(self.yi, PPD)], [bf(4, g) for g in gs])

    def report(self, shot, g):
        f = bf(4, g); self.scene.frame_set(f); loc, look, lens = cam_of(g, self)
        return dict(shot=4, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f), feet=C.feet_report(self, f))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(4, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[4][0] <= g <= RANGES[4][1]]
        Tk = Take(); Tk.pose(4, gs)
        for g in gs:
            print(json.dumps(Tk.report(4, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                os.makedirs(out, exist_ok=True)
                st = Tk.render(4, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s4_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 24
        C.final_loop(lambda s_: Take(), [4], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
