#!/usr/bin/env python3
"""shot.py -- film 11 take s14: shot 14, the false payoff's accusation: "เห็นมั้ย เด็กจะตายเพราะเอ็ง!" g 843..897 (+6 handle frames each side).
room_night / light C.  The town doctor stands in the open doorway (cane planted) and jabs his finger at Jenner (towndoc_point_door, mirrored so he
points screen-left into the room); lip-sync talk_mouth inside the quote window (g 849..899 = captions 28.21-29.85 s), flat before.  Jenner winces
(jenner_wince, hands half up), the mother stands wringing her hands at the left.  Slow push-in on the doorway.
    python3 shot.py probe 14 a:b[:step] | stills 14 a:b[:step] <out_dir> [scale] [samples] | final 14 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
import cast11                                            # noqa: E402
from mathutils import Vector                             # noqa: E402

lerp, clamp, blink, ez, bf, u_of = C.lerp, C.clamp, C.blink, C.ez, C.bf, C.u_of
TMP = os.path.join(HERE, "work")
SHOT = 14
G0, G1 = C.g_bound(28.10), C.g_bound(29.95)              # 843, 898
H = 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
DISSOLVE_IN = False
CUES = [{"frame": 849, "label": "the doctor shouts the accusation (quote window g 849-899)", "kind": "voice-window"}]
PRESET, LIGHT = "room_night", None
TINT = "#f6dcc4"
Q0, Q1 = C.g_of(28.21), C.g_of(29.85)                    # 849, 899: the quoted line

CAM0 = ((-0.9, -3.1, 2.7), (4.7, 5.5, 1.8))
CAM1 = ((0.3, -2.4, 2.6), (4.9, 5.3, 1.9))
DOC = (7.1, 3.9)
JEN = (3.4, 2.4)
MOM = (1.3, 3.6)


def cam_of(g):
    x = clamp((g - G0) / float(G1 - G0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def pose_doc(g):
    p = dict(cast11.STORY11["towndoc_point_door"][1])
    k = math.sin(g * 0.45)
    jab = 0.5 + 0.5 * math.sin(g * 0.32)                           # the finger jabs in time with his rage
    p.update(mirror=True, tint=TINT, head_roll=-3 + 2.0 * math.sin(g * 0.21), lean=2.0 * jab,
             arm_r=dict(hand=(1.05 + 0.08 * jab, 0.30 - 0.04 * jab), bend=-0.2, shape="point"))
    p["mouth"] = cast11.talk_mouth(g, 1.0) if Q0 <= g <= Q1 else "flat"
    p["blink"] = blink(g, [862, 889])
    p["t"] = g / 30.0
    return p


def pose_jen(g):
    p = dict(cast11.STORY11["jenner_wince"][1])
    k = math.sin(g * 0.2)
    p.update(tint=TINT, head_roll=6 + 1.5 * k, lean=-8 + 1.2 * math.sin(g * 0.11),
             arm_r=dict(hand=(0.62, 0.40 + 0.03 * k), bend=-0.3, shape="open"),
             arm_l=dict(hand=(-0.55, 0.50 - 0.03 * k), bend=-0.2, shape="open"))
    p["blink"] = blink(g, [851, 876])
    p["t"] = g / 30.0
    return p


def pose_mom(g):
    p = dict(cast11.STORY11["mother_stand_worried"][1])
    k = math.sin(g * 0.15)
    p.update(tint=TINT, head_roll=p.get("head_roll", 0) + 1.5 * math.sin(g * 0.09), t=g / 30.0)
    p["blink"] = blink(g, [845, 870])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s14")
        sd = os.path.join(TMP, "sprites")
        self.doc = self.actors["doc"] = C.make_actor("doc", "towndoc", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.mom = self.actors["mom"] = C.make_actor("mom", "mother", sd)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.doc, f, DOC, scale=C.SCALE["towndoc"])
            C.place(self.jen, f, JEN, scale=C.SCALE["jenner"])
            C.place(self.mom, f, MOM, scale=C.SCALE["mother"])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.doc.pose(f, pose_doc(g), camera=self.cam)
            self.jen.pose(f, pose_jen(g), camera=self.cam)
            self.mom.pose(f, pose_mom(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.doc, 192), (self.jen, 192), (self.mom, 192)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f),
                    mouth=("talk" if Q0 <= g <= Q1 else "flat"))

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
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
