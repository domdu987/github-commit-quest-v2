#!/usr/bin/env python3
"""shot.py -- film 24 take s03: shot 3 (sea fleet_wide), g 145..293 = 6 in-handle + g 151..287 + 6 out-handle.
The Japanese fleet sails +x (set_fleet_chase keyed every frame, s = seconds since g 145); the camera slides laterally +x with it
(slow eased move, 50 % of fleet speed so the fleet drifts gently).  No characters.  Blender frame of (id 3, g) = 2000 + g + 1.
    python3 shot.py probe 3 a:b[:step] | stills 3 a:b[:step] <out> [scale] [samples] | final 3 a:b [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J = C.J
bf = C.bf
G0, G1 = C.g_bound(5.0), C.g_bound(9.57)                 # 150, 287 (shot 3 g 151..287)
H = 6
RANGES = {3: (151 - H, 287 + H)}
SLIDE_K = 0.5


def cam_of(g, T):
    pc = T.A["cam"]; loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    a, b = RANGES[3]; x = (g - a) / float(b - a); u = C.calm(x)
    dx = J.CHASE_V * SLIDE_K * (b - a) / 30.0 * u
    d = Vector((dx, 0, 0))
    return loc0 + d, look0 + d, pc["lens"]


class Take(C.Take):
    def __init__(self, shot=3):
        C.Take.__init__(self, "fleet_wide", name="cam_s03")

    def pose(self, shot, gs):
        a = RANGES[3][0]
        for g in gs:
            f = bf(3, g); self.scene.frame_set(f)
            loc, look, lens = cam_of(g, self); self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=(g - a) / 30.0, korean_turn=0.0)

    def report(self, shot, g):
        f = bf(3, g); self.scene.frame_set(f); loc, look, lens = cam_of(g, self)
        return dict(shot=3, g=g, cam=[round(c, 3) for c in loc], lens=lens)

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(3, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[3][0] <= g <= RANGES[3][1]]
        Tk = Take(); Tk.pose(3, gs)
        for g in gs:
            print(json.dumps(Tk.report(3, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                st = Tk.render(3, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s3_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 4 else C.RES_PCT
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples("fleet_wide")
        C.final_loop(lambda s_: Take(), [3], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
