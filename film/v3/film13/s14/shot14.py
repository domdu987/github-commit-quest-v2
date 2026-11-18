#!/usr/bin/env python3
"""shot14.py -- film 13 take s14: shot 14 (30.41-32.50 narration s = g 912..974, handles 906..980). street, DAY, lift 0:
workers file in carrying iron jacks on their shoulders along a plank lane, down a ramp into a trench dug in front of the hotel and
into the timbered mouth at its east end; pullman at the jack pile, townsfolk watching.  Calm camera: slow crane-push, always moving.
    python3 shot14.py stills a:b[:step] <out_dir> [scale] [samples]   |   python3 shot14.py final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c13 as C, dress14 as DR
import cast13
S = C.S; lerp = C.lerp
SHOT = 14
G0, G1 = C.g_bound(30.41), C.g_bound(32.50) - 1          # 912..974
H = 6
RANGE = (G0 - H, G1 + H)
TMP = os.path.join(HERE, "work")
CAM0 = ((-22.8, -13.8, 3.6), (-20.3, -3.6, 0.3))
CAM1 = ((-21.6, -12.2, 3.2), (-20.0, -3.6, 0.1))
LENS = 20.0
V = 0.092                                              # D per frame (matches the 28-frame walk cycle: 2.6 D per cycle)
VARS = ["a", "b", "c"]; CASTS = dict(a="worker13_a", b="worker13_b", c="worker13_c")
# walkers: (variant, start x at g = G0, phase)
WALK = [(VARS[i % 3], -24.0 + 2.7 * (i - 3) + 6.0 + (0.5 if i % 2 else -0.4), (0.13 * i) % 1.0) for i in range(11)]
SPEED_JIT = [1.0, 1.03, 0.97, 1.02, 0.98, 1.0, 1.03, 0.97, 1.02, 0.98, 1.0]

def cam_of(g):
    x = (g - RANGE[0]) / float(RANGE[1] - RANGE[0]); u = 0.3 * C.ez(x) + 0.7 * x
    return [tuple(lerp(CAM0[k][i], CAM1[k][i], u) for i in range(3)) for k in (0, 1)]

def carry_pose(cast, g, ph0, sfx):
    base = cast13.STORY13["worker_carry_jack_" + sfx][1]
    p = cast13.cycle(cast, g / 28.0 + ph0, "walk", base=dict(expr="determined", mouth="dash", prop_r=dict(type="iron_jack", angle=-62, scale=1.0)), arms="l")
    p["arm_r"] = dict(base["arm_r"]); p["blink"] = cast13.blink_at(g, 96, int(ph0 * 90))
    return p

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "street_wide", quality, lens=LENS, state="lift0", name="cam_s14")
        self.info = DR.dress()
        sd = os.path.join(TMP, "sprites"); self.walk = []
        for i, (sfx, x0, ph) in enumerate(WALK):
            a = self.actors["w%d" % i] = C.make_actor("w%d" % i, CASTS[sfx], sd); self.walk.append((a, sfx, x0, ph, SPEED_JIT[i]))

    def walker(self, a, sfx, x0, ph, spd, g):
        x = x0 + V * spd * (g - G0)
        return x, DR.lane_z(x)

    def pose(self, gs):
        fr = [C.bf(SHOT, g) for g in gs]
        for g, f in zip(gs, fr):
            loc, look = cam_of(g); self.key_cam(f, loc, look, lens=LENS)
            for (a, sfx, x0, ph, spd) in self.walk:
                x, z = self.walker(a, sfx, x0, ph, spd, g)
                vis = x < DR.XB - 0.7 and x > -45
                C.place(a, f, (x, DR.LANE_Y), z)
                a.card.hide_render = not vis; a.card.keyframe_insert("hide_render", frame=f)
        for g, f in zip(gs, fr):
            self.scene.frame_set(f)
            for (a, sfx, x0, ph, spd) in self.walk:
                a.pose(f, carry_pose(CASTS[sfx], g * spd, ph, sfx), camera=self.cam)
        jobs = [(a, 256) for (a, *_r) in self.walk]
        self.sprites_for(jobs, fr)

    def report(self, g):
        f = C.bf(SHOT, g); loc, look = cam_of(g)
        return dict(shot=SHOT, g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(SHOT, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]; out = sys.argv[3]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render([g], out, scale=scale, samples=samples)[0]; os.replace(st["path"], os.path.join(out, "s14_g_%04d.png" % g))
            print(json.dumps(Tk.report(g)), "%.1f s" % st["wall"], flush=True)
    else:
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), sys.argv[2], RANGE, HERE, SHOT, scale=scale, samples=samples)
