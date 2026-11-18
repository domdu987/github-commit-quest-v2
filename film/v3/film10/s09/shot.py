#!/usr/bin/env python3
"""shot.py -- film 10 take s09: shots 9-11 (g 613..793 incl. 6 in / 6 out handle frames), "count" line 20.63-26.27 s.
  shot 9  g 613..674  hull_side DAY   day 1: zigzags painted (set_stripes 0.3 -> 1), the painter strokes on the scaffold
  shot 10 g 675..728  new angle DAY   day 2: staircases added (1 -> 2), painter on the stage
  shot 11 g 729..793  harbour_wide DUSK day 3: full dazzle (2 -> 3), the painter steps back proud
Mouths: nobody speaks.  Shots 9-10 build DAY, shot 11 builds DUSK: run them in separate processes.
Blender frame of (id, g) = 1000*(id-1)+g+1.
    python3 shot.py stills 9,10 a:b[:step] out [scale] [samples]
    python3 shot.py final 9,10|11 a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
H, actors, cast10 = C.H, C.actors, C.cast10
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")
HO = 6
G9, G10, G11, GE = C.g_bound(20.63), C.g_bound(22.50), C.g_bound(24.30), C.g_bound(26.27)   # 619 675 729 788
RANGES = {9: (G9 - HO, G10 - 1), 10: (G10, G11 - 1), 11: (G11, GE + HO - 1)}
PRESET = {9: ("hull_side", "DAY"), 10: ("hull_side", "DAY"), 11: ("harbour_wide", "DUSK")}
LENS = {9: 24.0, 10: 24.0, 11: 24.0}
PPD = {9: 320, 10: 320, 11: 192}

# camera paths: (loc0, look0, loc1, look1)
CAMS = {
    9: ((-8.6, -5.9, 3.5), (-1.6, 1.0, 4.7), (-7.4, -5.7, 3.6), (-1.4, 1.0, 4.8)),
    10: ((3.6, -5.4, 3.0), (-2.8, 1.5, 6.8), (2.7, -5.3, 3.1), (-3.0, 1.5, 7.0)),
    11: ((6.0, -10.5, 1.9), (-5.0, 0.5, 5.5), (5.2, -10.3, 2.0), (-5.4, 0.5, 5.6)),
}
PAINTER = {9: (-3.9, 0.51, 2.74), 10: (-2.6, 0.51, 2.74), 11: (-1.2, -3.0, 0.0)}


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    l0, k0, l1, k1 = CAMS[shot]
    return Vector([lerp(l0[i], l1[i], u) for i in range(3)]), Vector([lerp(k0[i], k1[i], u) for i in range(3)])


def stage_of(g):
    """day 1: the zigzag front crosses the brush tip (0.40 -> 0.52); day 2: staircase bands grow (1.10 -> 1.75); day 3: -> 3.0."""
    pts = [(613, 0.40), (674, 0.52), (675, 1.10), (728, 1.75), (729, 2.0), (770, 3.0), (793, 3.0)]
    for (g0, v0), (g1, v1) in zip(pts, pts[1:]):
        if g0 <= g <= g1:
            return lerp(v0, v1, (g - g0) / float(g1 - g0))
    return pts[-1][1]


def pose_of(shot, g):
    t = g / 30.0
    if shot in (9, 10):
        ph = 0.5 - 0.5 * math.cos(t * 2 * math.pi / 0.9)           # one stroke per 0.9 s
        base = cast10.STORY10["painter_on_plank"][1]
        p = dict(base)
        p["plank"] = 0
        p["arm_r"] = dict(p["arm_r"], hand=(lerp(0.74, 0.66, ph), lerp(0.60, -0.30, ph)))
        p["prop_r"] = dict(p["prop_r"], angle=lerp(-20, -62, ph))
        p["t"] = t
        p["blink"] = blink(g, [40, 97])
        return p
    p = dict(cast10.STORY10["painter_step_back_proud"][1])
    u = u_of(g, 729, 756)
    p["lean"] = lerp(-2.0, -8.0, u)
    p["legs"] = {"preset": "step", "stride": lerp(0.55, -0.35, u)}
    p["t"] = t
    p["blink"] = blink(g, [800])
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=9):
        pr, lt = PRESET[shot]
        C.Take.__init__(self, pr, light=lt, quality=quality, lens=LENS[shot], name="cam_s09")
        self.sh = shot
        canvas = cast10.CANVAS10_PLANK["painter10"] if False else None
        self.pa = self.actors["pa"] = C.make_actor("pa", "painter10", os.path.join(TMP, "sprites%d" % shot))
        self.crew = C.Crew(self, os.path.join(TMP, "crew%d" % shot), ppd=96)

        def _avoid(f, shot=shot):
            g = f - 1000 * (shot - 1) - 1
            px, py, pz = PAINTER[shot]
            if shot == 11:
                py -= 1.5 * u_of(g, 729, 752)
            return (px, py, pz + 2.7)
        self.crew.avoid = _avoid

    def pose(self, shot, gs):
        pa = self.pa
        for g in gs:
            f = C.bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            px, py, pz = PAINTER[shot]
            if shot == 11:                                   # steps back from the hull (toward the lens) and stops, proud
                py -= 1.5 * u_of(g, 729, 752)
            C.place(pa, f, (px, py), z=pz)
            H.set_stripes(stage_of(g), frame=f, interp="LINEAR")
            H.set_smoke(1.0, frame=f)
            H.set_flames(1.0, frame=f)
            self.crew.key(f)
        for g in gs:
            f = C.bf(shot, g)
            self.scene.frame_set(f)
            pa.pose(f, pose_of(shot, g), camera=self.cam)
            self.crew.pose(f, g)
        fr = [C.bf(shot, g) for g in gs]
        self.sprites_for([(pa, PPD[shot])], fr)
        self.crew.sprites(fr)

    def report(self, shot, g):
        f = C.bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        hp = {}
        a = self.pa
        if (a.name, f) in self.anch:
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            hp = dict(x=round(c[0], 1), y=round(c[1], 1))
        return dict(shot=shot, g=g, cam=[round(c, 2) for c in loc], stage=round(stage_of(g), 3), head=hp)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview", shots[0])
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            out = sys.argv[4]
            scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
            samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, shots[0]), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
