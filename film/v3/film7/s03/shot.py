#!/usr/bin/env python3
"""shot.py -- film 7 take s03: shot 3 (plan 4.60-7.80 s = g 138..233) + 6-frame handles (g 132..137, g 234..239), cut in / cut out.
Plan: paris / kiosk -- the kiosk fills fast with Mona Lisa front pages (set_papers 0 -> 24), the newsboy shouting (no lip-sync).
A flash-forward (common.py gotcha: the only shot before 17 where the papers may show her face).
"...และการขโมยครั้งนั้นแหละ คือเหตุผลที่มันดังที่สุดในโลก".  Two set-ups (framing change at g 186 = 6.20 s, 1.6 s into the shot):

    id 1  g 132..185  the sunlit kiosk front (kiosk preset area, STREET_GOLDEN): papers 0 until g 142, then they slap up one every
                      2-3 frames (kiosk front 8, sides 4, the Morris column 6, shop walls 6: 24 by g 196); the newsboy (behind,
                      right of the kiosk) waves the front page and shouts; slow push in toward the kiosk.
    id 2  g 186..239  closer, slightly low: the newsboy shouting "extra!" with the front page held high, the kiosk wall of her faces
                      and the column behind him; slow push.
Mouths: the newsboy's shout is a HELD open mouth (expression), no lip-sync.  NO depth of field (C.Take).

    python3 shot.py probe|stills|final ... (as s02)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(4.60), C.g_bound(7.80), 6          # 138, 234
G_CUT = 186
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G1 + H - 1)}
P_START, P_END = 142, 196                                # papers 0 -> 24


def papers_at(g):
    if g < P_START:
        return 0
    return int(min(24, 1 + (g - P_START) * 24.0 / (P_END - P_START)))


NEWSBOY = Vector((-3.05, 12.1, 0.0))
LADY0, LADY_V = Vector((-2.55, 17.0, 0.0)), Vector((0.026, 0.0, 0.0))     # setup 2 only, g 186 -> 239


WITH_LADY = False                                        # tried: she hid behind his front page / left frame at once


def cam_of(shot, g):
    if shot == 1:
        u = ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0]))
        loc = Vector(lerp((-1.10, 5.6, 2.55), (-1.60, 6.8, 2.45), u))
        look = Vector(lerp((-4.6, 10.8, 2.1), (-4.7, 11.0, 2.0), u))
        return loc, look, 22.0
    u = ez((g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0]))
    loc = Vector(lerp((-0.85, 8.45, 1.85), (-1.20, 9.05, 1.82), u))
    look = Vector(lerp((-3.9, 12.9, 2.25), (-3.9, 12.9, 2.20), u))
    return loc, look, 24.0


SHOUT = cast7.STORY7["newsboy_shout"][1]


def newsboy_pose(g):
    p = dict(SHOUT)
    w = math.sin(g * 0.55)
    hx, hy = SHOUT["arm_r"]["hand"]
    p["arm_r"] = dict(SHOUT["arm_r"], hand=(hx + 0.06 * w, hy - 0.05 * abs(w)))
    lx, ly = SHOUT["arm_l"]["hand"]
    p["arm_l"] = dict(SHOUT["arm_l"], hand=(lx - 0.04 * math.sin(g * 0.55 + 1.0), ly))
    p["head_roll"] = SHOUT["head_roll"] + 3.0 * math.sin(g * 0.27)
    p["lean"] = SHOUT["lean"] + 1.5 * math.sin(g * 0.55)
    p["pitch"] = SHOUT["pitch"] + 0.05 * math.sin(g * 0.3)
    p["mouth"] = ("open", 0.17, 0.20)                    # held shout, no lip-sync
    p["blink"] = blink(g, [150, 205])
    p["t"] = g / 30.0
    return p


def lady_pose(g):
    base = dict(expr="neutral", yaw=0.7, gaze=(-0.5, 0.0), pitch=-0.05)
    p = cast7.cycle("lady", (g - 132) / 28.0, "walk", facing=1, base=base, arms="both", speed=0.8)
    p["blink"] = blink(g, [160])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "paris", "kiosk", quality=quality, lens=22.0, name="cam_s03_%d" % shot)
        self.shot = shot
        sd = os.path.join(TMP, "sprites")
        self.actors["boy"] = C.make_actor("boy", "newsboy", sd)
        if WITH_LADY and shot == 2:
            self.actors["lady"] = C.make_actor("lady", "lady", sd)

    def pose(self, shot, gs):
        boy = self.actors["boy"]; lady = self.actors.get("lady")
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(boy, f, NEWSBOY, 0.0)
            if lady:
                C.place(lady, f, LADY0 + LADY_V * (g - 186), 0.0)
            self.key_set(f, flames=0.3, papers=papers_at(g))      # daytime: the kerb gas lamps turned low (no yellow blob at the lens)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            boy.pose(f, newsboy_pose(g), camera=self.cam)
            if lady:
                lady.pose(f, lady_pose(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        jobs = [(boy, 320)] + ([(lady, 240)] if lady else [])
        self.sprites_for(jobs, fr)

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look, lens = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, papers=papers_at(g), heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples, threads=1)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, shots[0]), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
