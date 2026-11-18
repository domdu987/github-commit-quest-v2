#!/usr/bin/env python3
"""shot.py -- film 13 take s10: shots 10 + 11 (g 585..731 incl. 6 in-handle + 6 out-handle frames), SUITE (top-floor room), DAY sky.
    id 10  g 585..649  (plan 19.70-21.68): the rich man at the window with his cup hears the plan, then bursts out laughing (laugh_big,
                       tea cup still in hand, no mouth sync); camera in the room pushes slowly in.
    id 11  g 650..731  (plan 21.68-24.20): Q1 starts, lip-sync (rich_mock_point), pointing out/down at the street; slow push + orbit.
Mouth rule: talk_mouth only inside Q1 (narration 21.68-28.09 +-0.15 s); 'flat' elsewhere (the laugh pose keeps its own held laugh mouth).
Blender frame = 1000 * (id - 1) + g + 1.
    python3 shot.py probe 10,11 a:b[:step] | stills 10,11 a:b[:step] out [scale] [samples] | final 10,11 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
D, actors, cast13 = C.D, C.actors, C.cast13
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G_CUT = C.g_bound(21.68)          # 650: shot 11 starts
G_END = C.g_bound(24.20)          # 726: shot 12 starts
G0 = C.g_bound(19.70) - 6         # 585
RANGES = {10: (G0, G_CUT - 1), 11: (G_CUT, G_END + 5)}
Q1 = (C.g_of(21.68) - 4, C.g_of(28.09) + 4)     # mouth window in film frames (+-0.15 s)
G_LAUGH = C.g_of(20.37) + 0                      # "บนสุดหัวเราะ": the burst (g 623?) -> see below
G_BURST = 612
LENS = 22.0

ZF = 30.0
RICH10 = Vector((0.7, 4.6, ZF))
RICH11 = Vector((-0.3, 1.4, ZF))

CAM10 = [((1.35, -2.2, 32.3), (0.5, 4.6, 31.7)), ((1.2, -0.6, 32.25), (0.6, 4.6, 31.8))]
CAM11 = [((1.6, 9.0, 32.5), (-0.4, 0.8, 31.5)), ((0.6, 6.4, 32.45), (-0.4, 0.8, 31.6))]


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    c0, c1 = (CAM10 if shot == 10 else CAM11)
    return Vector(lerp(c0[0], c1[0], u)), Vector(lerp(c0[1], c1[1], u))


def pose_10(g):
    R = cast13.STORY13
    if g < G_BURST:
        p = dict(R["rich_look_window_smug"][1])
        p["yaw"] = 0.55 + 0.05 * math.sin(g * 0.09)
        p["head_roll"] = -3 + 1.5 * math.sin(g * 0.13)
        p["lean"] = 1.0 * math.sin(g * 0.07)
        p["mouth"] = "flat"
        p["blink"] = blink(g, [596, 606])
        if g >= G_BURST - 6:                                   # hears: the head comes round to the camera, brows up
            k = ez((g - (G_BURST - 6)) / 6.0)
            p["yaw"] = lerp(p["yaw"], 0.25, k); p["expr"] = "surprised" if k > 0.5 else "smug"
        p["t"] = g / 30.0
        return p
    p = dict(R["rich_laugh_big"][1])
    ph = ((g - G_BURST) // 4) % 2
    p["squash"] = (1.02, 0.98) if ph == 0 else (0.99, 1.01)
    p["head_roll"] = -10 + 3 * math.sin((g - G_BURST) * 0.8)
    p["lean"] = -8 + 2 * math.sin((g - G_BURST) * 0.6)
    p["pitch"] = -0.85 + 0.1 * math.sin((g - G_BURST) * 0.7)
    p["arm_l"] = dict(hand=(-0.58, 0.98 + 0.03 * math.sin((g - G_BURST) * 0.8)), bend=0.9, shape="open")
    p["prop_l"] = {"type": "teacup_saucer", "scale": 1.5}
    p["t"] = g / 30.0
    if g < G_BURST + 3:                                        # the pop frames: squashed burst
        p["squash"] = (1.08, 0.92)
    return p


def pose_11(g):
    p = dict(cast13.STORY13["rich_mock_point"][1])
    inq = Q1[0] <= g <= Q1[1]
    p["mouth"] = cast13.talk_mouth(g, 1.0) if inq else "flat"
    p["head_roll"] = 8 + 2.0 * math.sin(g * 0.15)
    p["lean"] = 2.0 * math.sin(g * 0.11)
    p["yaw"] = 0.4 + 0.05 * math.sin(g * 0.07)
    p["pitch"] = -0.3 + 0.08 * math.sin(g * 0.17)
    bob = 0.05 * math.sin(g * 0.32)
    p["arm_r"] = dict(hand=(1.1, 0.42 + bob), shape="point", bend=-0.5, stretch=1.3)
    p["blink"] = blink(g, [666, 700])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview", shot=10):
        C.Take.__init__(self, "suite_room", quality=quality, lens=LENS, name="cam_s10", state="tea0")
        self.rich = self.actors["rich"] = C.make_actor("rich", "rich", os.path.join(TMP, "sprites"))

    def pose(self, shot, gs):
        r = self.rich
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            C.place(r, f, RICH10 if shot == 10 else RICH11)
            D.set_flames(1.0, frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            r.pose(f, pose_10(g) if shot == 10 else pose_11(g), camera=self.cam)
        self.sprites_for([(r, 320)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), mouth_q1=Q1[0] <= g <= Q1[1])

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
