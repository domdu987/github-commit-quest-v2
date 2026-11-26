#!/usr/bin/env python3
"""shot.py -- film 24 take s09: shots 9a + 9 (g 913..1007: 6 in-handle frames, 9a g 919..953, hard cut, shot 9 g 954..1001, 6 out-handle frames).
    id 9   shot 9a  macro_oar (sea, special 'solo'): 40 mm f/2.8 at water level on the hero oar blade; set_oar_splash repeats every 24 frames
                    (t = phase / 15, first dip at g 922); the camera does one slow lateral slide (1.1 D) along the oar, focus on a world-fixed empty at
                    the preset look_at.  No people.
    id 19  shot 9   hansan_high: very high wide over the strait, the Korean ships (turtle + panokseon) flee AHEAD (set_korean_turn 0) with the Japanese
                    fleet behind (set_fleet_chase s grows); one slow push of 8 % along the view line.  No people.
Blender frame = 1000*(id-1) + g + 1.
    python3 shot.py probe 9,19 a:b | stills 9,19 a:b <out> [scale] [samples] | final 9|19|9,19 a:b [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402
J, actors, cast24 = C.J, C.actors, C.cast24
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
H = 6
G_9A, G_9, G_END = C.g_bound(30.64), C.g_bound(31.80), C.g_bound(33.40)     # 919, 954, 1002
RANGES = {9: (G_9A - H, G_9 - 1), 19: (G_9, G_END - 1 + H)}
PRESET = {9: "macro_oar", 19: "hansan_high"}
SLIDE9 = 1.1
PUSH19 = 0.08
SPLASH_PERIOD, SPLASH_LEN, SPLASH_G0 = 24, 15.0, G_9A + 3          # first dip at g 922


def splash_t(g):
    p = (g - SPLASH_G0) % SPLASH_PERIOD
    return p / SPLASH_LEN if p <= SPLASH_LEN else 0.0


def cam_of(shot, A, g):
    pc = A["cam"]
    a, b = RANGES[shot]
    u = C.calm((g - a) / float(b - a))
    loc0, look0 = Vector(pc["loc"]), Vector(pc["look_at"])
    if shot == 9:
        fwd = look0 - loc0; fwd.z = 0; fwd.normalize()
        right = fwd.cross(Vector((0, 0, 1)))
        return loc0 + right * (SLIDE9 * (u - 0.5)), look0 + right * (SLIDE9 * (u - 0.5)), pc["lens"]
    return loc0 + (look0 - loc0) * (PUSH19 * u), look0, pc["lens"]


class Take(C.Take):
    def __init__(self, shot):
        C.Take.__init__(self, PRESET[shot], name="cam_s09")
        self.shot = shot

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, self.A, g)
            self.key_cam(f, loc, look, lens=lens)
            if shot == 9:
                self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=0.0, korean_turn=0.0, damage=0.0, cannon_smoke=0.0,
                             special="solo", oar_splash=splash_t(g))
            else:
                self.key_set(f, spikes=3, ports=0, dragon_smoke=0.0, fleet_chase=(g - G_9) / 30.0, korean_turn=0.0, damage=0.0, cannon_smoke=0.0,
                             special="")

    def report(self, shot, g):
        loc, look, lens = cam_of(shot, self.A, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, splash=round(splash_t(g), 2) if shot == 9 else None)

    def render(self, shot, gs, out_dir, scale=C.RES_PCT, samples=C.SAMPLES, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take(shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 10
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall" % (shot, g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else C.RES_PCT
        for shot in shots:
            samples = int(sys.argv[5]) if len(sys.argv) > 5 else C.preset_samples(PRESET[shot])
            C.final_loop(lambda s_: Take(s_), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
