#!/usr/bin/env python3
"""shot_C.py -- film 24 version C take s08C: the build-up, preset build_dock (yard slipway at dusk), g 734..1125 (g1 = 1126 exclusive)
+ 6 handle frames each side (728..1131).  No cast.  J.set_build_g(g, f) every frame, camera J.build_cam((g-734)/392), build_anchors.json.
Blender frame = 7000 + g + 1.    JOSEON_LOOK=C python3 shot_C.py probe a:b[:s] | stills a:b[:s] <out> [scale] [samples] | final a:b [scale] [samples] | anchors
"""
import os, sys, json
os.environ.setdefault("JOSEON_LOOK", "C")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
J = C.J
G0, G1, H = 734, 1126, 6
RANGES = {8: (G0 - H, G1 + H - 1)}
SHOT = 8


def bfr(g):
    return C.bf(SHOT, g)


class Take(C.Take):
    def __init__(self, shot=8):
        C.Take.__init__(self, "build_dock", name="cam_s08C")
        if J.LOOK != "C":
            J.set_look("C")

    def pose(self, shot, gs):
        self.stage = {}
        for g in gs:
            f = bfr(g); self.scene.frame_set(f)
            c = J.build_cam((g - G0) / float(G1 - G0 - 0))
            self.key_cam(f, c["loc"], c["look_at"], lens=c["lens"])
            self.key_set(f, spikes=None, ports=None, dragon_smoke=0.0)
            self.stage[g] = J.set_build_g(g, f)[0]

    def anchor(self, g):
        f = bfr(g); self.scene.frame_set(f); self.scene.camera = self.cam
        a = J.build_anchor(self.stage[g] if g in self.stage else J.build_at(g)[0])
        return dict(g=g, stage=J.build_at(g)[0], x=None if a is None else a[0], y=None if a is None else a[1])

    def report(self, shot, g):
        f = bfr(g); self.scene.frame_set(f); c = J.build_cam((g - G0) / float(G1 - G0))
        return dict(shot=8, g=g, cam=[round(v, 3) for v in c["loc"]], lens=c["lens"], stage=J.build_at(g)[0], anchor=self.anchor(g))

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bfr(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        gs = [g for g in C.parse(sys.argv[2]) if RANGES[8][0] <= g <= RANGES[8][1]]
        Tk = Take(); Tk.pose(8, gs)
        for g in gs:
            print(json.dumps(Tk.report(8, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.4; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 10
                os.makedirs(out, exist_ok=True)
                st = Tk.render(8, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s8_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else C.RES_PCT
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        C.final_loop(lambda s_: Take(), [8], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
