#!/usr/bin/env python3
"""shot.py -- film 24 take s04: shot 4 (yard yard_wide), g 282..436 = 6 in-handle + g 288..430 + 6 out-handle.
The finished closed-roof turtle ship (spikes 3, ports 0) on the slipway; Yi on the quay in front (stand_arms_behind, one nod ~ "เหมือนกระดองเต่า"
afterwards), three small varied Korean workers planted on the quay.  One slow push-in toward the ship (8 %).  Mouths fixed (no quote).
Blender frame of (id 4, g) = 3000 + g + 1.
    python3 shot.py probe 4 a:b[:step] | stills 4 a:b[:step] <out> [scale] [samples] | final 4 a:b [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G0, G1 = C.g_bound(9.60), C.g_bound(14.37)               # 288, 431
H = 6
RANGES = {4: (G0 - H, G1 + H - 1)}
PRESET = {4: "yard_wide"}
PUSH = 0.08
G_NOD = C.g_of(11.6)                                      # one nod
YI = (8.9, 14.5, J.Z_Q)                                   # quay in front (nearest figure)
W = dict(b=(9.4, 4.5, J.Z_Q), c=(9.3, -4.6, J.Z_Q), a=(13.0, 9.5, J.Z_Q))
PPD = dict(yi=64, a=48, b=48, c=48)


def cam_of(g, T):
    pc = T.A["cam"]; loc0, look = Vector(pc["loc"]), Vector(pc["look_at"])
    x = (g - RANGES[4][0]) / float(RANGES[4][1] - RANGES[4][0]); u = C.calm(x)
    return loc0 + (look - loc0) * (PUSH * u), look, pc["lens"]


def pose_yi(g):
    c, p = C.story("yi24_stand_arms_behind")
    p["lean"] = 1.0 * math.sin(g * 0.09)
    k = g - G_NOD
    p["pitch"] = (0.28 * math.sin(math.pi * k / 16.0)) if 0 <= k <= 16 else 0.0      # nod: down and back
    p["blink"] = blink(g, [310, 372, 404]); p["t"] = g / 30.0
    return p


def pose_w(name, g, ph, mirror=False):
    c, p = C.story(name)
    p["mirror"] = mirror
    p["lean"] = p.get("lean", 0) + 0.9 * math.sin(g * 0.1 + ph)
    p["head_roll"] = 1.2 * math.sin(g * 0.07 + ph)
    p["blink"] = blink(g, [330 + int(ph * 10)]); p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, shot=4):
        C.Take.__init__(self, "yard_wide", name="cam_s04")
        sd = os.path.join(TMP, "sprites")
        self.yi = self.actors["yi"] = C.make_actor("yi", "yi24", sd)
        self.wa = self.actors["wa"] = C.make_actor("wa", "kor_a24", sd)
        self.wb = self.actors["wb"] = C.make_actor("wb", "kor_b24", sd)
        self.wc = self.actors["wc"] = C.make_actor("wc", "kor_c24", sd)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(4, g); self.scene.frame_set(f)
            loc, look, lens = cam_of(g, self); self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0)
            C.place(self.yi, f, YI); C.place(self.wa, f, W["a"]); C.place(self.wb, f, W["b"]); C.place(self.wc, f, W["c"])
        for g in gs:
            f = bf(4, g); self.scene.frame_set(f)
            self.yi.pose(f, pose_yi(g), camera=self.cam)
            self.wa.pose(f, pose_w("kor_a24_stand_carry_spikes", g, 0.0, True), camera=self.cam)
            self.wb.pose(f, pose_w("kor_b24_stand_carry_spikes", g, 1.9), camera=self.cam)
            self.wc.pose(f, pose_w("kor_c24_stand_rope", g, 3.1, True), camera=self.cam)
        self.sprites_for([(self.yi, PPD["yi"]), (self.wa, PPD["a"]), (self.wb, PPD["b"]), (self.wc, PPD["c"])], [bf(4, g) for g in gs])

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
                st = Tk.render(4, [g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s4_g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples("yard_wide")
        C.final_loop(lambda s_: Take(), [4], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
