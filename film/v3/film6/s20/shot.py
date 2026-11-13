#!/usr/bin/env python3
"""shot.py -- film 6 take s20: shot 20 (plan 52.60-54.64 s -> g 1578..1638) + 6-frame handles (g 1572..1644), market AFTERNOON.

    20a g 1572..1605  pillory_low: the EMPTY pillory on its platform under the low afternoon sun, long raking shadows of the
                      board and posts across the planks and cobbles; slow push in + slight rise ("ที่โดนจับ ก็โดนตอนบ่าย").
    20b g 1606..1644  reverse: kit (flour boy) close, the pillory behind him over his shoulder in the same low sun (sharp, no
                      DOF). He studies it (hand on chin, 3/4 to screen-left), then on "ก็โดนตอนบ่าย / ทั้งนั้น" (g 1615-1623)
                      his eyes go WIDE (stunned -> shocked), he snaps his head round to the lens, a tiny squash-up.  Slow push.
Mouths: no quoted line -> kit's mouth is the static mouth of each expression.  NO depth of field (common.Take).

Internal shot id 20.   python3 shot.py probe|stills|final 20 a:b[:step] [out] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

B, actors, camrig, cast6 = C.B, C.actors, C.camrig, C.cast6
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1 = C.g_bound(52.60), C.g_bound(54.64)          # 1578, 1639
H = 6
RANGES = {20: (G0 - H, G1 + H - 1)}                  # 1572..1644
G_CUT = 1606                                         # 20a | 20b
G_WIDE = C.g_of(53.2) + 15                           # 1614: eyes widen ("ก็โดนตอนบ่าย")
G_TURN = (G_WIDE + 2, G_WIDE + 8)

CAM_A0 = ((0.20, 3.60, 1.75), (-4.0, 9.5, 2.25))
CAM_A1 = ((-0.55, 4.55, 1.60), (-4.0, 9.5, 2.40))
KIT = (0.55, 4.40)
CAM_B0 = ((1.20, 1.10, 2.15), (-1.60, 8.10, 2.15))
CAM_B1 = ((0.95, 1.55, 2.12), (-1.60, 8.10, 2.15))
LENS = 22.0


def cam(g):
    if g < G_CUT:
        u = ez((g - RANGES[20][0]) / float(G_CUT - RANGES[20][0]), "sine")
        A0, A1 = CAM_A0, CAM_A1
    else:
        u = ez((g - G_CUT) / float(RANGES[20][1] + 1 - G_CUT), "sine")
        A0, A1 = CAM_B0, CAM_B1
    return Vector(lerp(A0[0], A1[0], u)), Vector(lerp(A0[1], A1[1], u))


def kit_pose(g):
    p = dict(cast6.STORY6["kit_think"][1])
    p.update(t=g / 30.0)
    uw = ez((g - G_TURN[0]) / float(G_TURN[1] - G_TURN[0])) if g >= G_TURN[0] else 0.0
    # studying the pillory behind / screen-left of him
    p["yaw"] = lerp(-0.55 + 0.03 * math.sin(g * 0.2), 0.0, uw)
    p["pitch"] = lerp(-0.30, -0.05, uw)
    p["gaze"] = (lerp(-0.85, 0.0, uw), lerp(-0.55, 0.0, uw))
    p["head_roll"] = lerp(5, 0, uw)
    if g < G_WIDE:
        p["expr"] = "determined"
    elif g < G_TURN[0] + 3:
        p["expr"] = "stunned"
    else:
        p["expr"] = "shocked"
    if g >= G_WIDE:
        # hand drops from the chin, both hands open up in surprise
        u = ez((g - G_WIDE) / 6.0)
        p["arm_r"] = dict(hand=(lerp(0.15, 0.55, u), lerp(-0.05, 0.30, u)), bend=-0.6, shape="open", stretch=1.2)
        p["arm_l"] = dict(hand=(lerp(-0.10, -0.55, u), lerp(0.78, 0.30, u)), bend=-0.6, shape="open", stretch=1.2)
        s = pulse(g, G_WIDE, G_WIDE + 2, G_WIDE + 8, 1.0)
        p["squash"] = (1.0 - 0.04 * s, 1.0 + 0.05 * s)
    p["blink"] = blink(g, [1610])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "market", "AFTERNOON", quality=quality, lens=LENS, name="cam_s20")
        sd = os.path.join(TMP, "sprites")
        self.actors["kit"] = C.make_actor("kit", "kit", sd)

    def pose(self, shot, gs):
        kit = self.actors["kit"]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam(g)
            self.key_cam(f, loc, look)
            C.place(kit, f, KIT, 0.0)
            kit.card.hide_render = g < G_CUT
            kit.card.keyframe_insert("hide_render", frame=f)
            self.key_set(f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            kit.pose(f, kit_pose(g), camera=self.cam)
        self.sprites_for([(kit, 512)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam(g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc],
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
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
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
