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
RICH10 = Vector((4.0, 4.3, ZF))        # seated in the red armchair (the 3D chair is removed at runtime; the card draws its own)
RICH11 = Vector((-0.3, 1.3, ZF))        # standing at the window
PULL11 = (4.5, -54.0)

CAM10 = [((10.2, 10.8, 31.9), (3.5, 3.6, 31.6)), ((9.0, 9.4, 31.9), (3.5, 3.6, 31.7))]
CAM11 = [((-1.8, 6.6, 33.9), (1.2, -9.0, 26.4)), ((-1.0, 5.6, 33.8), (1.6, -9.0, 26.6))]


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    c0, c1 = (CAM10 if shot == 10 else CAM11)
    return Vector(lerp(c0[0], c1[0], u)), Vector(lerp(c0[1], c1[1], u))


def pose_10(g):
    """seated in the armchair, cup and saucer in hand: sips, looks out of the window (head turned to screen-left, the window), hears
    (g 600-611), turns to us and bursts into a CLOSED-mouth laugh (grin, squeezed eyes, tears, shaking) from g 612."""
    R = cast13.STORY13
    p = dict(R["rich_sit_tea"][1])
    p["mouth"] = "smile" if g >= G_BURST else "flat"
    look = 1.0 - ez((g - 598) / 10.0)                         # 1: looking out of the window, 0: to us
    p["yaw"] = lerp(0.20, -0.75, look)
    p["gaze"] = (lerp(0.0, -0.9, look), 0.0)
    p["pitch"] = -0.25 + 0.05 * math.sin(g * 0.1)
    p["head_roll"] = 4 + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, [592, 606])
    p["t"] = g / 30.0
    if g < G_BURST:
        p["expr"] = "smug" if g < 604 else "surprised"
        return p
    k = g - G_BURST
    p["expr"] = "laughing"; p["fx"] = ["tears"]; p["mouth"] = "smile"
    p["pitch"] = -0.7 + 0.1 * math.sin(k * 0.7)
    p["head_roll"] = -8 + 3 * math.sin(k * 0.8)
    p["lean"] = -5 + 2 * math.sin(k * 0.6)
    p["squash"] = (1.03, 0.97) if (k // 4) % 2 == 0 else (0.99, 1.01)
    if k < 3: p["squash"] = (1.08, 0.92)
    p.pop("blink", None)
    return p


def pose_11(g):
    p = dict(cast13.STORY13["rich_mock_point"][1])
    p["mouth"] = cast13.talk_mouth(g, 1.0) if Q1[0] <= g <= Q1[1] else "flat"
    p["head_roll"] = 6 + 2.0 * math.sin(g * 0.15)
    p["lean"] = 2.0 * math.sin(g * 0.11)
    p["yaw"] = 0.55 + 0.05 * math.sin(g * 0.07)
    p["pitch"] = 0.05 + 0.06 * math.sin(g * 0.17)
    p["gaze"] = (0.6, 0.7)                                      # eyes down at the street
    bob = 0.04 * math.sin(g * 0.32)
    p["arm_r"] = dict(hand=(0.95, 0.85 + bob), shape="point", bend=-0.3, stretch=1.3)       # pointing DOWN and out
    p["arm_l"] = dict(hand=(-0.1, 0.95), bend=0.5, stretch=1.2, layer="front")
    p["prop_l"] = {"type": "teacup_saucer", "scale": 1.5}       # the cup stays in his hand (continuity with shot 10)
    p["blink"] = blink(g, [666, 700])
    p["t"] = g / 30.0
    return p


def pose_pull(g):
    p = dict(cast13.STORY13["pullman_point_plan"][1])
    p["lean"] = 1.0 * math.sin(g * 0.07)
    p["t"] = g / 30.0
    return p


def remove_chair(cx, cy, r=2.3, obname="furniture"):
    import bmesh
    import numpy as np
    ob = bpy_obj(obname)
    me = ob.data
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float32); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
    M = np.array(ob.matrix_world, dtype=np.float64)
    w = co @ M[:3, :3].T + M[:3, 3]
    sel = np.flatnonzero((w[:, 2] < ZF + 4.6) & ((w[:, 0] - cx) ** 2 + (w[:, 1] - cy) ** 2 < r * r))
    p = np.linalg.inv(M) @ np.array([cx, cy, ZF - 8.0, 1.0])            # collapse the chair's vertices to one point under the floor (bmesh delete hangs on this mesh)
    co[sel] = p[:3].astype(np.float32)
    me.vertices.foreach_set("co", co.reshape(-1)); me.update()
    print("remove_chair: %d of %d verts" % (len(sel), n), flush=True)


def bpy_obj(name):
    return C.bpy.data.objects[name]


class Take(C.Take):
    def __init__(self, quality="preview", shot=10):
        C.Take.__init__(self, "suite_window", quality=quality, lens=LENS, name="cam_s10", state="")
        S = os.path.join(TMP, "sprites")
        remove_chair(4.2, 4.2)
        remove_chair(-3.4, 2.4, 2.6)                       # the tea table cups (the cup is in his hand)
        remove_chair(-3.4, 2.4, 2.6, "tea")
        self.seat = self.actors["seat"] = C.make_actor("seat", "rich", S, canvas=cast13.CANVAS13_POSE["rich_sit_tea"])
        self.rich = self.actors["rich"] = C.make_actor("rich", "rich", S)
        self.pul = self.actors["pul"] = C.make_actor("pul", "pullman", S)

    def pose(self, shot, gs):
        gnd = D._gnd(); away = (0.0, -300.0, -50.0)
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            D.set_flames(1.0, frame=f)
            C.place(self.seat, f, RICH10 if shot == 10 else away)
            C.place(self.rich, f, RICH11 if shot == 11 else away)
            C.place(self.pul, f, (PULL11[0], PULL11[1], gnd(*PULL11)) if shot == 11 else away, scale=2.4)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 10:
                self.seat.pose(f, pose_10(g), camera=self.cam)
                self.rich.pose(f, dict(cast13.STORY13["rich_look_window_smug"][1]), camera=self.cam)
                self.pul.pose(f, pose_pull(g), camera=self.cam)
            else:
                self.rich.pose(f, pose_11(g), camera=self.cam)
                self.pul.pose(f, pose_pull(g), camera=self.cam)
                self.seat.pose(f, pose_10(G_BURST + 20), camera=self.cam)
        self.sprites_for([(a, 320) for a in self.actors.values()], [bf(shot, g) for g in gs])

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
