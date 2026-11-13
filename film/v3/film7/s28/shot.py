#!/usr/bin/env python3
"""shot.py -- film 7 take s28: shots 28-29 (91.49-99.33 s, g 2745..2979) + 6-frame handles (g 2739..2985), the Salon Carre
(louvre gallery, GALLERY_DAY, January 1914: the painting is back).  Plan: 28 the painting back on the wall, the crowd presses in (reveal);
29 match-dissolve from the empty-wall queue to the crowd at the painting, push in to her smile.  Dissolve in (from s26, the Florence shop).

    id 1  g 2739..2783  eye level at the rope (wall_eye area): she hangs alone again ("ภาพที่เคยไม่มีใครมอง"), then the crowd streams in
                        from both frame edges and stops at the rope, faces turned up to her.  Slow push.
    id 2  g 2784..2829  reverse from beside her on the wall (CUT on "กลายเป็นภาพ" 92.70): the packed crowd's faces looking up at her,
                        pressing against the red rope, rows to the back of the salon; they edge forward.  Slow push.
    id 3  g 2830..2864  side view along the wall (CUT on "เพราะมันหายไป" 94.73): the crowd in profile pressing toward her, she in her
                        gilt frame behind the glass on the right.  Slow track.
    id 4  g 2865..2911  shot 29: high oblique over the queue lanes (empty_wall_queue): the EMPTY wall (hooks, patch), the reopening queue.
    id 5  g 2900..2945  the same camera path, the painting back and a bigger crowd pressing in -> deliver.py cross-dissolves id 4 -> id 5
                        over g 2900..2911 (the match-dissolve, 12 f); the camera keeps pushing in toward her.
    id 6  g 2946..2985  ECU on her face behind the glass (punch-in on "ทำให้มันดัง" 98.54), slow push in to the smile; to the end + handle.
Mouths: no quoted line -> no lip-sync; static expression mouths ('mouth' keys of the STORY poses dropped).
NO depth of field anywhere (client rule): C.Take switches it off.

    python3 shot.py stills 1,.. a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final <id> a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7, bpy = C.L, C.actors, C.camrig, C.cast7, C.bpy
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0 = C.g_bound(91.49)              # 2745
G29 = C.g_bound(95.50)             # 2865
G1 = C.g_bound(99.33)              # 2980
H = 6
G_2 = C.g_of(92.70 - 0.10)         # 2784
G_3 = C.g_of(94.73 - 0.10)         # 2845 -> cut a little earlier for a 1.17 s set-up
G_3 = 2830
DIS = (2900, 2911)                 # match-dissolve empty wall -> crowd at the painting
G_6 = 2946
RANGES = {1: (G0 - H, G_2 - 1), 2: (G_2, G_3 - 1), 3: (G_3, G29 - 1), 4: (G29, DIS[1]), 5: (DIS[0], G_6 - 1), 6: (G_6, G1 + H - 1)}

# camera paths (loc0, look0, loc1, look1, lens); id 4 / 5 share one path over g 2865..2945
CAMS = {
    1: ((0.25, 15.0, 2.3), (0.0, 22.0, 2.85), (0.18, 16.1, 2.32), (0.0, 22.0, 2.9), 24.0),
    2: ((1.15, 21.25, 4.7), (-0.5, 15.0, 0.2), (0.95, 20.95, 4.55), (-0.6, 15.0, 0.25), 18.0),
    3: ((2.9, 18.5, 3.3), (-0.8, 21.4, 2.6), (2.75, 18.75, 3.3), (-0.8, 21.45, 2.6), 22.0),
    6: ((0.03, 19.75, 3.85), (0.0, 21.9, 3.85), (0.02, 20.6, 3.92), (0.0, 21.9, 3.93), 30.0),
}
Q0 = ((-5.4, 12.6, 6.1), (0.4, 21.6, 1.4))
Q1 = ((-5.0, 13.4, 5.8), (0.35, 21.6, 1.45))       # at DIS[1]
Q2 = ((-4.2, 14.4, 5.45), (0.15, 21.9, 2.85))       # at G_6 - 1
LENS_Q = 22.0


def cam_of(shot, g):
    if shot in (4, 5):
        if g <= DIS[1]:                       # linear: id 4 and id 5 hold the very same camera through the dissolve
            a, b = Q0, Q1
            u = clamp((g - G29) / float(DIS[1] - G29))
        else:                                 # accelerates from the same speed into the push to her
            a, b = Q1, Q2
            v = clamp((g - DIS[1]) / float(G_6 - 1 - DIS[1]))
            u = 0.13 * v + 0.87 * v * v
        return Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u)), LENS_Q
    a, b = RANGES[shot]
    u = ez((g - a) / float(b - a), "sine")
    l0, k0, l1, k1, lens = CAMS[shot]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lens


def nomouth(p):
    p = dict(p); p.pop("mouth", None); return p


POSES = dict(lady=("crowd_stare", "crowd_point", "lady_gasp"), gentleman=("crowd_stare_gentleman", "crowd_point_gentleman", None),
             newsboy=("crowd_stare_newsboy", "crowd_point_newsboy", None))


# crowd specs per set-up: (name, cast, mood 0 stare | 1 point | 2 gasp, start xy, end xy, g_in, mirror)
def crowd(shot):
    out = []
    if shot == 1:
        for nm, cs, md, a, b, gi, mr in (
                ("c1", "lady", 0, (-2.9, 19.9), (-1.05, 19.9), 2751, False),
                ("c2", "gentleman", 1, (-3.0, 19.5), (-1.75, 19.5), 2757, False),
                ("c3", "gentleman", 0, (2.9, 19.9), (1.05, 19.9), 2753, True),
                ("c4", "lady", 2, (3.0, 19.5), (1.75, 19.5), 2759, True)):
            out.append((nm, cs, md, a, b, gi, mr))
    elif shot == 2:
        rows = [(19.0, (-1.25, 0.0, 1.25)), (18.3, (-1.9, -0.62, 0.62, 1.9)), (17.5, (-2.4, -1.2, 0.0, 1.2, 2.4)), (16.6, (-1.7, 0.4, 2.3))]
        casts = ["lady", "gentleman", "lady", "gentleman", "lady", "lady", "gentleman", "lady", "gentleman", "lady", "gentleman",
                 "lady", "gentleman", "lady", "gentleman"]
        k = 0
        for y, xs in rows:
            for x in xs:
                cs = casts[k % len(casts)]
                md = (0, 1, 2)[k % 3] if cs == "lady" else (k % 2)
                out.append(("c%d" % k, cs, md, (x, y - 0.35), (x, y), G_2 - 10, x > 0))
                k += 1
    elif shot == 3:
        for k, (x, y, cs, md) in enumerate(((-0.3, 19.95, "lady", 0), (-1.2, 19.95, "gentleman", 1), (-2.1, 19.9, "lady", 2), (-3.0, 19.95, "gentleman", 0),
                                            (-1.7, 19.25, "lady", 1), (-2.6, 19.3, "gentleman", 0), (-3.5, 19.35, "lady", 0))):
            out.append(("c%d" % k, cs, md, (x, y - 0.45), (x, y), G_3 - 25, False))
    elif shot in (4, 5):
        # id 4: the reopening queue in the lanes staring at the empty wall; id 5: more people, pressed to the rope, pointing at her
        pts4 = [(-1.1, 19.6, "lady"), (0.9, 19.3, "gentleman"), (-0.2, 18.4, "lady"), (1.4, 17.3, "gentleman"), (-1.3, 17.4, "newsboy"),
                (0.1, 16.4, "lady")]
        pts5 = [(-1.5, 20.0, "lady"), (-0.5, 20.05, "gentleman"), (0.5, 20.0, "lady"), (1.5, 20.0, "gentleman"), (-2.1, 19.3, "gentleman"),
                (-1.0, 19.3, "newsboy"), (0.0, 19.25, "lady"), (1.0, 19.3, "lady"), (2.1, 19.25, "gentleman"),
                (-0.5, 18.45, "gentleman"), (0.6, 18.5, "lady"), (1.7, 18.4, "gentleman"), (2.6, 18.9, "lady"), (2.9, 19.8, "gentleman")]
        pts = pts4 if shot == 4 else pts5
        for k, (x, y, cs) in enumerate(pts):
            md = 0 if shot == 4 else (1 if k % 3 == 1 else (2 if (cs == "lady" and k % 3 == 2) else 0))
            out.append(("c%d" % k, cs, md, (x, y - (0.0 if shot == 4 else 0.3)), (x, y), G29 - 40, True))
    return out


def crowd_pos(spec, g):
    nm, cs, md, a, b, gi, mr = spec
    d = Vector((b[0] - a[0], b[1] - a[1], 0.0))
    dur = max(1.0, d.length / 0.075)
    u = clamp((g - gi) / dur)
    return Vector((a[0], a[1], 0.0)) + d * u, u < 1.0, gi + dur


def crowd_pose(spec, g, shot):
    nm, cs, md, a, b, gi, mr = spec
    seed = sum(ord(c) for c in nm) + 7 * shot
    pos, walking, g_arr = crowd_pos(spec, g)
    names = POSES[cs]
    pn = names[md] if names[md] else names[0]
    p = nomouth(cast7.STORY7[pn][1])
    if walking and abs(b[0] - a[0]) > 0.5:                   # streaming in from the side
        base = dict(expr="excited", yaw=0.6, pitch=-0.25, gaze=(0.6, -0.6))
        if cs == "gentleman":
            base["prop_r"] = None
        p = cast7.cycle(cs, (g - gi) / 26.0 + 0.13 * (seed % 7), "walk", facing=(-1 if mr else 1), base=base, speed=0.9)
        p.pop("prop_r", None)
    else:
        if shot in (2,):                                     # facing the lens = facing her (she is behind the camera)
            p["yaw"] = (-0.15 if mr else 0.15)
            p["gaze"] = (0.0, -0.75)
            p["pitch"] = -0.35
        elif shot == 6:
            pass
        else:
            p["yaw"] = 0.55 if md != 2 else 0.35
            p["gaze"] = (0.8, -0.55)
        p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.13 + seed)
        p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.11 + 0.7 * seed) + (3.0 if shot in (2, 5) else 0.0)
        p["mirror"] = mr
        if shot == 4:
            p["expr"] = "stunned"
    p["blink"] = blink(g, [2742 + (seed * 13) % 50, 2800 + (seed * 7) % 60, 2880 + (seed * 11) % 50, 2930 + (seed * 5) % 40])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        lens = LENS_Q if shot in (4, 5) else CAMS[shot][4]
        preset = "empty_wall_queue" if shot == 4 else "wall_eye"
        C.Take.__init__(self, "louvre", preset, quality=quality, lens=lens, name="cam_s28_%d" % shot)
        self.shot = shot
        self.scene.cycles.transparent_max_bounces = 64   # up to 18 crowd cards (+ proxies, decals) stacked along one ray: 8 went grey
        sd = os.path.join(TMP, "sprites")
        self.crowd = crowd(shot)
        for spec in self.crowd:
            self.actors[spec[0]] = C.make_actor(spec[0], spec[1], sd)

    def pose(self, shot, gs):
        assert shot == self.shot
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            self.key_set(f, mona=(shot != 4), queue=(shot == 4), mona_lift=0.0)
            for spec in self.crowd:
                pos, _, _ = crowd_pos(spec, g)
                if shot == 5:                                # they press in through the push
                    pos = pos + Vector((0.0, 0.3 * clamp((g - DIS[0]) / 40.0), 0.0))
                C.place(self.actors[spec[0]], f, pos)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for spec in self.crowd:
                self.actors[spec[0]].pose(f, crowd_pose(spec, g, shot), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(a, 320) for a in self.actors.values()], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens,
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))

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
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples,
                     take_key=lambda shot: shot)
