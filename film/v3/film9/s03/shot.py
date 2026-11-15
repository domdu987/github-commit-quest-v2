#!/usr/bin/env python3
"""shot.py -- film 9 take s03: shots 3 + 4 (plan 3.62-9.01 s = g 109..269) + 6 handle frames each side (g 103..108, 270..275).
"Here's the thing: China 600 years ago, the emperor orders the city wall finished before the enemy army arrives."
Two locations-by-light (one build each, final_loop rebuilds on the change):

    id 1  g 103..194  shot 3, `site_wide` DAY, crane: the camera sinks ~3.8 D and pushes in over the huge construction site: Lin
                      stirring the steaming cauldron, workers carrying stacks of bricks (one up the plank ramp of the general's
                      scaffold), both sections with scaffolds, hoists and banners, the gate tower, the river plain and mountains.
                      g 103..108 = in-handle (the same move continued backwards in time).
    id 2  g 195..275  shot 4, `gate_dusk` DUSK: high from the site toward the gate tower; over the wall the enemy host's banners and
                      dust on the horizon (`army_horizon` stretched 1.7x in height at runtime so it reads at phone size), the
                      battlefield smoke 0.6; a worker walks toward the gate.  Slow push + slight tilt toward the horizon.
                      g 270..275 = out-handle.
No quote: no lip-sync.  NO depth of field (client rule; c9.Take switches it off).

    python3 shot.py probe|stills 1,2 a:b[:step] [out_dir scale samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402

W, actors, camrig, cast9 = C.B, C.actors, C.camrig, C.cast9
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(3.62)               # 109
G_S4 = C.g_bound(6.50)             # 195
G1 = C.g_bound(9.01)               # 270
H = 6
RANGES = {1: (G0 - H, G_S4 - 1), 2: (G_S4, G1 + H - 1)}
SETUP = {1: ("site_wide", "DAY"), 2: ("gate_dusk", "DUSK")}

CAM = {
    1: (((-19.4, 33.0, 20.6), (-2.6, 7.0, 1.0)), ((-17.0, 29.8, 16.6), (-3.4, 7.6, 1.6)), 20.0),
    2: (((14.0, 26.0, 21.0), (31.0, 2.0, 10.6)), ((15.4, 24.2, 20.3), (31.0, 2.0, 11.6)), 20.0),
}
PPD = {1: 160, 2: 160}


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    (l0, k0), (l1, k1), lens = CAM[shot]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lens


STIR = cast9.STORY9["lin_stir"][1]


def pose_stir(g):
    p = json.loads(json.dumps(STIR))
    ph = 2 * math.pi * g / 24.0
    p["arm_l"]["hand"] = (0.36 + 0.12 * math.cos(ph), 0.10 + 0.05 * math.sin(ph))
    p["prop_l"]["angle"] = 58 + 8 * math.sin(ph)
    p["lean"] = 8 + 4 * math.cos(ph)
    p["blink"] = blink(g, [130, 170])
    p["t"] = g / 30.0
    return p


def carry_walk(cast_key, g, facing, phase0=0.0):
    base = json.loads(json.dumps(cast9.STORY9[cast_key][1]))
    p = cast9.cycle(base.get("_c", None) or "x", 0, "walk") if False else None
    c = {"workers_carry": "worker_a", "workers_carry_b": "worker_b", "workers_carry_c": "worker_c"}[cast_key]
    p = cast9.cycle(c, phase0 + g / 28.0, "walk", facing=facing, base=base, arms="none", speed=0.8)
    p["t"] = g / 30.0
    return p


def walk(c, g, facing, phase0=0.0):
    p = cast9.cycle(c, phase0 + g / 28.0, "walk", facing=facing, base=dict(expr="neutral", blink=blink(g, [215, 250])), speed=0.9)
    p["t"] = g / 30.0
    return p


V = 0.055                          # D per frame of a walk at speed 0.8-0.9 (~1.5 D per 28-frame cycle)


def stage(shot, g, marks):
    """[(actor key, cast, feet xyz, flip, pose)]"""
    out = []
    if shot == 1:
        ls = marks["lin_stir"]
        out.append(("lin", "lin", ls, True, pose_stir(g)))
        x = -4.2 + V * (g - RANGES[1][0])                       # worker_a carries bricks along the site toward the general's trough
        out.append(("wa", "worker_a", (x, 11.6, 0.0), False, carry_walk("workers_carry", g, -1)))
        x = 4.0 + V * 0.9 * (g - RANGES[1][0])                  # worker_c climbs the plank ramp (3.5, 8, 0) -> (11.3, 8, 6)
        out.append(("wc", "worker_c", (x, 8.0, max(0.0, (x - 3.5) / 7.8 * 6.0)), False, carry_walk("workers_carry_c", g, -1, 0.4)))
        y = 16.8 - V * 0.8 * (g - RANGES[1][0])                 # worker_b walks in toward the wall with a stack
        out.append(("wb", "worker_b", (-1.2, y, 0.0), False, carry_walk("workers_carry_b", g, 1, 0.7)))
    else:
        pass                                                   # no figure: from this high camera any ground figure near the
                                                               # gate falls below the caption band (y 880)
    return out


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        preset, light = SETUP[shot]
        C.Take.__init__(self, "wall_site", preset, quality=quality, lens=20.0, name="cam_s03", light=light)
        self.shot = shot
        marks = self.A["marks"]
        self.marks = marks
        for key, cast, *_ in stage(shot, RANGES[shot][0], marks):
            self.actors[key] = C.make_actor(key, cast, os.path.join(TMP, "sprites%d" % shot))
        if shot == 2:                                          # QA_TECH B: make the host on the horizon read (taller banners + dust)
            ob = C.bpy.data.objects.get("army_horizon")
            if ob is not None:
                ob.scale = (1.0, 1.0, 1.7)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            if shot == 1:
                self.key_set(f, steam=1.0, heights=(18, 21))
            else:
                self.key_set(f, steam=1.0, heights=(18, 21), smoke=0.6, army=True)
            for key, cast, ft, flip, p in stage(shot, g, self.marks):
                C.place(self.actors[key], f, (ft[0], ft[1]), z=ft[2], flip=flip)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for key, cast, ft, flip, p in stage(shot, g, self.marks):
                self.actors[key].pose(f, p, camera=self.cam)
        if self.actors:
            self.sprites_for([(a, PPD[shot]) for a in self.actors.values()], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

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
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, s: Take(q, s), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
