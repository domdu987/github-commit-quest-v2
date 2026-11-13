#!/usr/bin/env python3
"""shot.py -- film 7 take s02: shot 2 (plan 2.40-4.60 s = g 72..137) + 6-frame handles (g 66..71, g 138..143), cut in / cut out.
Plan: louvre / wall_eye, the empty wall spot: four hooks, the guard yawning beside it (set_mona False).  "...โดยไม่มีใครสังเกตเลยทั้งวัน".
Two set-ups (framing change at g 102, 1.0 s into the shot):

    id 1  g 66..101   ECU of the empty spot: the four iron hooks, the unfaded damask patch and its dust line, the brass plaque;
                      a slow pull back (35 -> 30 mm) that lets the guard's shoulder in at frame right.
    id 2  g 102..143  medium: the guard beside the empty spot gives a huge yawn and stretch (g 104..128), then sags back
                      half asleep; slow push in.  Mona keyed False on every frame.
Mouths: no quoted line -> no lip-sync; the yawn is one slow open / hold / close of the expression mouth (not speech).
NO depth of field (C.Take).

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(2.40), C.g_bound(4.60), 6          # 72, 138
G_CUT = 102
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G1 + H - 1)}
YAWN = (104, 112, 122, 130)                              # open .. full .. hold .. closed

GUARD = Vector((1.78, 20.95, 0.0))
SPOT = Vector((0.0, 21.92, 3.55))


def cam_of(shot, g):
    if shot == 1:
        u = ez((g - RANGES[1][0]) / float(RANGES[1][1] - RANGES[1][0]))
        loc = Vector(lerp((-0.05, 18.95, 3.52), (0.05, 18.25, 3.46), u))
        look = Vector(lerp((0.0, 21.9, 3.50), (0.02, 21.9, 3.38), u))
        return loc, look, lerp(34.0, 29.5, u)
    u = ez((g - RANGES[2][0]) / float(RANGES[2][1] - RANGES[2][0]))
    loc = Vector(lerp((0.25, 15.45, 2.75), (0.40, 16.20, 2.72), u))
    look = Vector(lerp((0.85, 21.9, 3.05), (0.95, 21.9, 3.02), u))
    return loc, look, 26.0


REST = dict(yaw=0.25, pitch=-0.15, expr="sleepy", head_roll=3.0, lean=0.0,
            arm_r=dict(hand=(0.30, 0.95), bend=0.35, stretch=1.0), arm_l=dict(hand=(-0.30, 0.95), bend=0.35, stretch=1.0, shape="open"),
            legs="stand")
YAWNP = cast7.STORY7["guard_yawn"][1]


def _mix_arm(a, b, u):
    out = dict(a)
    out["hand"] = tuple(lerp(a["hand"], b["hand"], u))
    out["bend"] = lerp(a.get("bend", 0.5), b.get("bend", 0.5), u)
    out["stretch"] = lerp(a.get("stretch", 1.0), b.get("stretch", 1.0), u)
    if u > 0.5 and "shape" in b:
        out["shape"] = b["shape"]
    return out


def guard_pose(g):
    a, b, c, d = YAWN
    if g < a or g > d + 8:
        u = 0.0
    elif g < b:
        u = ez((g - a) / float(b - a))
    elif g <= c:
        u = 1.0
    else:
        u = 1.0 - ez((g - c) / float(d + 8 - c))
    p = dict(REST)
    p["arm_r"] = _mix_arm(REST["arm_r"], YAWNP["arm_r"], u)
    p["arm_l"] = _mix_arm(REST["arm_l"], YAWNP["arm_l"], u)
    p["pitch"] = lerp(REST["pitch"], YAWNP["pitch"], u) + 0.04 * math.sin(g * 0.15)
    p["head_roll"] = lerp(REST["head_roll"], YAWNP["head_roll"], u) + 1.2 * math.sin(g * 0.11)
    p["lean"] = lerp(0.0, YAWNP["lean"], u) + 0.8 * math.sin(g * 0.09)
    p["yaw"] = lerp(0.25, 0.10, u)
    mo = clamp((g - a) / float(b - a)) if g <= c else clamp(1.0 - (g - c) / float(d - c))
    if mo > 0.05:
        p["mouth"] = ("open", 0.08 + 0.17 * mo, 0.05 + 0.27 * mo)
        p["expr"] = "asleep" if mo > 0.5 else "sleepy"
    else:
        p["mouth"] = "flat"
    if u > 0.5:
        p["legs"] = "wide"
    p["blink"] = blink(g, [76, 96, 140])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "louvre", "wall_eye", quality=quality, lens=30.0, name="cam_s02_%d" % shot)
        self.shot = shot
        self.actors["guard"] = C.make_actor("guard", "guard", os.path.join(TMP, "sprites"))

    def pose(self, shot, gs):
        gd = self.actors["guard"]
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            C.place(gd, f, GUARD, 0.0)
            self.key_set(f, mona=False)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            gd.pose(f, guard_pose(g), camera=self.cam)
        self.sprites_for([(gd, 320)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        loc, look, lens = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=lens, heads=C.head_report(self, f))

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
        C.final_loop(lambda q: Take(q, shots[0]), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
