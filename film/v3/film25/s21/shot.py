#!/usr/bin/env python3
"""s21 -- row 21 GAG "ของเล่นชัดๆ!" (g 602-625), TRIAL, Look A.  The general dangles the toy tank (1.6x) by its string and sneers, lip-sync.
Low waist-up angle, near grey-olive plate 2 D behind him (his cast shadow lands on it), sky above it, mild DOF.  PUNCH 20 % over g 602-609, then a slow drift.
    python3 shot.py probe|draft|final <gspec>      post: python3 ../s21/post_d.py . <gspec>
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d25 as D                                          # noqa: E402
C, F, cast25 = D.C, D.F, D.C.cast25
from mathutils import Vector                             # noqa: E402

PRESET = "trial_close_general"
G0, G1 = 602, 626
ND, WALL_H, WALL_W = 2.0, 4.1, 14.0
LEVEL = None


def lvl(g):
    global LEVEL
    if LEVEL is None:
        LEVEL = C.audio_level()
    return LEVEL[g]


def story(name):
    c, p = cast25.STORY25[name]
    return json.loads(json.dumps(p))


def squash_accent(g, g0):
    seq = {0: 0.93, 1: 0.92, 2: 0.98, 3: 1.05, 4: 1.03, 5: 1.0}
    k = g - g0
    if k not in seq:
        return None
    s = seq[k]
    return [round(2.0 - s, 3) if s < 1 else round(1.0 - (s - 1.0) * 0.6, 3), s]


def blink(g, at):
    for b in at:
        if g - b in (0, 2): return 1
        if g - b == 1: return 2
    return 0


def pose_of(g):
    p = story("general25_toy_dangle")
    p["mouth"] = cast25.talk_mouth(g, lvl(g))
    p["prop_r"] = {"type": "toy_tank25", "scale": 1.6}
    p["t"] = round(0.2 + (g - G0) / 22.0, 4)                              # the toy swings, every frame
    sq = squash_accent(g, G0)
    if sq: p["squash"] = sq
    if g < 614:                                                           # eyes on the toy
        p["gaze"] = [0.6, 0.45]; p["yaw"] = 0.35; p["head_roll"] = 10
        p["arm_r"]["hand"] = [0.62, round(0.12 + 0.05 * math.sin((g - G0) * 0.7), 3)]      # a little dip and bob of the dangling hand
    else:                                                                 # "ชัดๆ!": sneers at us, lifts the toy
        w = C.smooth((g - 614) / 5.0)
        p["gaze"] = [round(0.6 - 0.6 * w, 2), round(0.45 - 0.45 * w, 2)]; p["yaw"] = round(0.35 - 0.2 * w, 3); p["head_roll"] = round(10 - 14 * w, 2)
        p["expr"] = "unimpressed" if g >= 615 else "smug"
        p["arm_r"]["hand"] = [0.62, round(0.12 - 0.12 * w, 3)]
    p["blink"] = blink(g, [613])
    p["light25"] = -1; p["rim25"] = 0.6
    return p


class Take(D.Rig):
    def __init__(self, work):
        D.Rig.__init__(self, PRESET, work, fstop=2.0)
        self.gen = self.actor("gen", "general25")
        m = F.S["mark"]
        self.P = Vector(m["pos"]); self.f0 = m["face_deg"]
        self.P.z = F.gh(self.P.x, self.P.y)
        azc = self.f0 + 18.0                                              # camera azimuth around the mark
        self.wall = D.add_wall("wall", (self.P.x - math.cos(math.radians(azc)) * ND, self.P.y - math.sin(math.radians(azc)) * ND), azc, WALL_W, WALL_H, D.plate_material())

    def cam_of(self, g):
        k = C.out_cubic((g - G0) / 7.0)
        d = 5.0 / (1.0 + 0.20 * k)
        w = C.calm((g - 609) / float(G1 - 1 - 609))
        d = d / (1.0 + 0.04 * w)
        az, cz, lz, lens, side = self.f0 + 24.0 - 6.0 * w, 1.55, 2.12 + 0.06 * w, 40.0, 0.25 * w
        A = math.radians(az)
        loc = Vector((self.P.x + math.cos(A) * d, self.P.y + math.sin(A) * d, self.P.z + cz))
        fwd = Vector((-math.cos(A), -math.sin(A), 0.0)); right = fwd.cross(Vector((0, 0, 1))).normalized()
        look = Vector((self.P.x, self.P.y, self.P.z + lz)) + right * (side * 0.6 - 0.10)
        return (loc + right * side, look), lens

    def setup(self, gs):
        for g in gs:
            cam, lens = self.cam_of(g)
            self.key_frame(g, cam, lens, dict(gen=dict(feet=self.P, pose=pose_of(g))), focus=self.P + Vector((0, 0, 2.7)))
        self.pose_frames(gs)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = C.parse(sys.argv[2])
    Tk = Take(os.path.join(HERE, "work"))
    Tk.setup(gs)
    if cmd == "probe":
        for g in gs:
            md = Tk.meta(g); print(g, {k: [round(v, 1) for v in a["head"]] + [round(a["hw"], 1)] for k, a in md["actors"].items()})
    elif cmd == "draft":
        sc = float(sys.argv[3]) if len(sys.argv) > 3 else 0.4
        for g in gs:
            md = Tk.render_frame(g, os.path.join(HERE, "work_draft"), scale=sc, samples=12, thr=0.05, sh_scale=0.3, sh_samples=6); print(g, md["wall_total"], flush=True)
    else:
        D.run_final(Tk, gs, os.path.join(HERE, "work"))
