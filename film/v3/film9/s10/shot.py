#!/usr/bin/env python3
"""shot.py -- film 9 take s10: shots 10 + 11 (plan 23.24-29.57 s = g 697..886, handles g 691..696 and 887..892).
One location (wall_site, DAY), one build (two_sections), two custom cameras joined by the plan's cut at g 792:

    id 1  g 691..791  shot 10, "month 1": front view of both sections from the site.  Both sections stand at 18 courses; the general's
                      section grows course by course to 21 on "สูงกว่า สามชั้น" (g 742 / 750 / 758) while Lin trowels his rice
                      mortar at the foot of his section and the general, akimbo by his own section, watches it rise and puffs up.
                      Workers carry brick stacks.  Slow push in + small orbit.
    id 2  g 792..892  shot 11, "month 2": on top of the general's section (lin 20 / general 26 courses), the general stands arms akimbo,
                      head thrown back laughing (body shakes, static laughing mouth: no quote here), a worker with bricks behind him.
                      Slow push in + drift.
Mouths: no quote in shots 10-11 -> fixed expression mouths only.  NO depth of field (c9.Take).
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402  (paths, cast9 first, bpy, wall, stage)
from mathutils import Vector                             # noqa: E402

W, actors, cast9 = C.B, C.actors, C.cast9
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0 = C.g_bound(23.24)              # 697
G_CUT = C.g_bound(26.40)           # 792
G_END = C.g_bound(29.57)           # 887 (shot 12 starts here)
H = 6
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G_END + H - 1)}
G_COURSES = [C.g_of(24.63) - 3, C.g_of(24.63) + 5, C.g_of(25.10) + 2]    # 19, 20, 21 courses ("สูงกว่า" .. "สามชั้น")
LIGHT = "DAY"

# ----------------------------------------------------------------------------- staging (wall_site: inner face y 5, general x 0..22 screen-left)
LIN_A = Vector((-2.3, 11.0, 0.0))       # at the foot of his (rice) section, trowelling toward the wall
GEN_A = Vector((2.5, 11.2, 0.0))        # beside his own section
WK_A = [("wk_a", "worker_a", Vector((4.9, 8.6, 0.0)), "workers_carry"),
        ("wk_b", "worker_b", Vector((-4.6, 8.3, 0.0)), "workers_carry_b")]
GEN_B = Vector((8.0, 2.4, 0.0))        # on the general's top (z = top_z at 26)
WK_B = ("wk_c", "worker_c", Vector((4.0, 4.5, 0.0)), "workers_carry_c")

CAM_A0 = ((1.0, 22.0, 5.9), (0.3, 5.0, 2.7))
CAM_A1 = ((0.1, 20.6, 5.6), (0.2, 5.0, 2.6))
LENS_A = 20.0
CAM_B0 = ((17.6, 2.3, 16.7), (1.0, 3.4, 14.6))
CAM_B1 = ((14.9, 3.2, 16.1), (1.0, 3.6, 14.8))
LENS_B = 20.0
PPD = {1: 224, 2: 304}


def u_lin(x):
    x = clamp(x)
    return 0.35 * ez(x, "sine") + 0.65 * x


def cam_of(shot, g):
    a, b = RANGES[shot]
    u = u_lin((g - a) / float(b - a))
    c0, c1 = (CAM_A0, CAM_A1) if shot == 1 else (CAM_B0, CAM_B1)
    return Vector(lerp(c0[0], c1[0], u)), Vector(lerp(c0[1], c1[1], u))


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def gen_courses(g):
    return 18 + sum(1 for gc in G_COURSES if g >= gc)


# ----------------------------------------------------------------------------- poses
def pose_lin_a(g):
    """calm, arms folded, watching the general's section rise (mirrored: faces screen-left, toward it), a small knowing smile."""
    p = dict(cast9.STORY9["lin_calm"][1])
    up = u_of(g, G_COURSES[0] - 4, G_COURSES[0] + 10)
    p["mirror"] = True
    p["pitch"] = lerp(-0.2, -0.6, up) + 0.05 * math.sin(g * 0.12)
    p["gaze"] = (0.3, lerp(-0.1, -0.7, up))
    p["lean"] = 1.5 * math.sin(g * 0.09)
    p["head_roll"] = -5 + 2.0 * math.sin(g * 0.13)
    p["blink"] = blink(g, [720, 770])
    return p


def pose_gen_a(g):
    p = dict(cast9.STORY9["general_stand"][1])
    up = u_of(g, G_COURSES[0] - 6, G_COURSES[0] + 6)         # looks up at his growing section, then back down smug
    down = u_of(g, G_COURSES[-1] + 6, G_COURSES[-1] + 18)
    look = up * (1.0 - down)
    p["yaw"] = lerp(0.35, -0.1, look)
    p["pitch"] = lerp(-0.3, -0.9, look) + 0.05 * math.sin(g * 0.17)
    p["gaze"] = (lerp(0.4, -0.3, look), lerp(0.0, -0.8, look))
    p["expr"] = "smug" if g < G_COURSES[0] - 2 or g > G_COURSES[-1] + 10 else "happy"
    p["head_roll"] = -6 + 3 * math.sin(g * 0.11) + 4 * down
    p["lean"] = -2 - 4 * down + 1.0 * math.sin(g * 0.15)      # puffs up
    p["squash"] = (1.0 + 0.03 * down, 1.0 + 0.015 * down)
    p["blink"] = blink(g, [705, G_COURSES[0] - 2, G_COURSES[-1] + 10])
    return p


def pose_wk(name, g, phase):
    p = dict(cast9.STORY9[name][1])
    p["lean"] = -5 + 2.0 * math.sin(g * 0.25 + phase)
    p["head_roll"] = -4 + 2.0 * math.sin(g * 0.19 + phase)
    p["squash"] = (1.0, 1.0 + 0.012 * math.sin(g * 0.5 + phase))
    p["t"] = g / 30.0
    return p


def pose_gen_b(g):
    p = dict(cast9.STORY9["general_wall_laugh"][1])
    k = math.sin(g * 0.85)                                   # belly-laugh shake (the mouth shape stays as drawn: no quote)
    p["squash"] = (1.02 + 0.02 * k, 0.98 - 0.02 * k)
    p["head_roll"] = -12 + 4 * math.sin(g * 0.23)
    p["pitch"] = -0.9 + 0.08 * math.sin(g * 0.31)
    p["lean"] = -6 + 2.5 * math.sin(g * 0.19)
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "wall_site", "two_sections", quality=quality, lens=LENS_A, name="cam_s10", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.lin = self.actors["lin"] = C.make_actor("lin", "lin", sd)
        self.gen = self.actors["gen"] = C.make_actor("gen", "general", sd)
        for nm, cast, xy, pz in WK_A + [WK_B]:
            self.actors[nm] = C.make_actor(nm, cast, sd)

    def pose(self, shot, gs):
        ztop = W.top_z("general", 26)
        for g in gs:
            f = bf(shot, g)
            loc, look = self.cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS_A if shot == 1 else LENS_B)
            if shot == 1:
                self.key_set(f, steam=1.0, wall_height=[("lin", 18), ("general", gen_courses(g))])
                C.place(self.lin, f, LIN_A); C.place(self.gen, f, GEN_A)
                for nm, cast, xy, pz in WK_A:
                    C.place(self.actors[nm], f, xy)
                C.place(self.actors["wk_c"], f, (40.0, 40.0, -50.0))
            else:
                self.key_set(f, steam=1.0, wall_height=[("lin", 20), ("general", 26)])
                C.place(self.gen, f, GEN_B, z=ztop)
                C.place(self.actors["wk_c"], f, WK_B[2], z=ztop)
                C.place(self.lin, f, (40.0, 40.0, -50.0))
                for nm, cast, xy, pz in WK_A:
                    C.place(self.actors[nm], f, (40.0, 41.0, -50.0))
        vis = ["lin", "gen", "wk_a", "wk_b"] if shot == 1 else ["gen", "wk_c"]
        for nm, a in self.actors.items():
            for g in gs:
                f = bf(shot, g)
                a.card.hide_render = nm not in vis
                a.card.keyframe_insert("hide_render", frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                self.lin.pose(f, pose_lin_a(g), camera=self.cam)
                self.gen.pose(f, pose_gen_a(g), camera=self.cam)
                for i, (nm, cast, xy, pz) in enumerate(WK_A):
                    self.actors[nm].pose(f, pose_wk(pz, g, 1.7 * i), camera=self.cam)
            else:
                self.gen.pose(f, pose_gen_b(g), camera=self.cam)
                self.actors["wk_c"].pose(f, pose_wk(WK_B[3], g, 0.6), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.actors[n], PPD[shot]) for n in vis], fr)

    def cam_of(self, shot, g):
        return cam_of(shot, g)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f),
                    courses=dict(lin=18 if shot == 1 else 20, general=gen_courses(g) if shot == 1 else 26))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
