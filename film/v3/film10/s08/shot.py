#!/usr/bin/env python3
"""shot.py -- film 10 take s08: shot 8 (g 538..618 + 6 handle frames each side: g 532..624), harbour DAY, custom medium camera.
Sailors on the quay and on the berth deck point at the painter and laugh ("ไอ้ช่างม้าลาย", 17.92-20.63 s).  Nobody lip-syncs; the laughing
faces are held drawings (alternating pointing / doubled-over poses, squash bounce).  The painter stays calm with his brush.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                           # noqa: E402
from mathutils import Vector                              # noqa: E402
import puppet                                             # noqa: E402

actors, cast10 = C.actors, C.cast10
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf
TMP = os.path.join(HERE, "work")
S10 = cast10.STORY10
G0, G1 = C.g_bound(17.92), C.g_bound(20.63)       # 538 .. 619
H = 6
RANGE = (G0 - H, G1 + H - 1)
SHOT = 8
LOC = ("harbour", "harbour_wide")
LIGHT = "DAY"
STRIPES = 0.505                              # = s09 stage at its first frame (g 613): continuity across the s08 -> s09 cut
PPD = 256
LENS = 21.0
BRUSH = cast10.BRUSH

CAM0 = ((-7.6, -18.5, 3.4), (-8.4, -3.0, 3.0))
CAM1 = ((-6.4, -17.4, 3.3), (-7.4, -3.0, 3.1))


def cam_of(g):
    x = clamp((g - G0) / float(G1 - G0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return (Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)]))


def sailor_pose(name, g, k):
    """k 0..: phase offset.  Held laugh drawings; alternate pointing and doubled over every ~14 frames."""
    sfx = "_" + name[-1]
    ph = (g + 9 * k) % 28
    key = "sailor_point_laugh" + sfx if ph < 17 else "sailor_laugh_hold_belly" + sfx
    p = dict(S10[key][1])
    s = math.sin((g + 5 * k) * 0.9)
    p["squash"] = (1.0 + 0.02 * s, 1.0 - 0.02 * s)
    p["head_roll"] = p.get("head_roll", 0) + 2.5 * math.sin((g + 7 * k) * 0.45)
    p["t"] = g / 30.0
    return p


def pnt_pose(g):
    p = dict(S10["painter_calm_smile"][1])
    p["head_roll"] = -4 + 1.5 * math.sin(g * 0.11)
    a = dict(p["arm_r"]); a["hand"] = (a["hand"][0], a["hand"][1] + 0.03 * math.sin(g * 0.17)); p["arm_r"] = a
    p["blink"] = cast10.blink_at(g, 100, 47)
    p["mirror"] = True
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=LENS, name="cam_s08", light=LIGHT)
        m = self.A["marks"]
        C.B.STATE["cards"][7].hide_render = True       # bgcard_7 stood at (-8, -9.5): replaced by our sailors
        sd = os.path.join(TMP, "sprites")
        self.cast = [("sa", "sailor_a", Vector((-11.5, -6.6, 0.0)), 0), ("sb", "sailor_b", Vector((-9.0, -9.6, 0.0)), 1),
                     ("sc", "sailor_c", Vector((-6.0, -7.4, 0.0)), 2),
                     ("da", "sailor_a", Vector((-14.5, m["sailor_deck_a"][1], m["sailor_deck_a"][2])), 3), ("db", "sailor_c", Vector((-18.5, m["sailor_deck_b"][1], m["sailor_deck_b"][2])), 4)]
        for n, c, pos, k in self.cast:
            self.actors[n] = C.make_actor(n, c, sd)
        self.pnt = self.actors["pnt"] = C.make_actor("pnt", "painter10", sd)
        self.PNT = Vector((-4.9, -8.0, 0.0))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(SHOT, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look, lens=LENS)
            for n, c, pos, k in self.cast:
                C.place(self.actors[n], f, pos)
            C.place(self.pnt, f, self.PNT)
            self.key_set(f, stripes=STRIPES)
        for g in gs:
            f = bf(SHOT, g)
            self.scene.frame_set(f)
            for n, c, pos, k in self.cast:
                self.actors[n].pose(f, sailor_pose(c, g, k), camera=self.cam)
            self.pnt.pose(f, pnt_pose(g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(SHOT, g) for g in gs])

    def report(self, shot, g):
        f = bf(SHOT, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=SHOT, g=g, cam=[round(c, 3) for c in loc], mouth=None, heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(SHOT, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if RANGE[0] <= g <= RANGE[1]]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); print("marks", Tk.A["marks"])
        Tk.pose(SHOT, gs)
        for g in gs:
            print(json.dumps(Tk.report(SHOT, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render(SHOT, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (SHOT, g)))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), [SHOT], sys.argv[2], {SHOT: RANGE}, HERE, scale=scale, samples=samples)
