#!/usr/bin/env python3
"""shot.py -- film 11 take s17: shot 17, "เขากรีดหนองฝีดาษของจริงใส่แขน" g 1056..1115 (+6 handle frames each side), cut in.
garden_hut / light A, closer.  Jenner brings the lancet to James's upper arm (scratch_arm, the tip pinned to James's upper_arm anchor and pressed in
rhythm); James sits brave on the stool; the town doctor scoffs with crossed arms behind (towndoc_scoff_crossed, mouth still).  Slow push-in.  Blister card on James's upper_arm_l.  Nobody speaks.
    python3 shot.py probe 17 a:b[:step] | stills 17 a:b[:step] <out_dir> [scale] [samples] | final 17 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
import cast11                                            # noqa: E402
from mathutils import Vector                             # noqa: E402

lerp, clamp, blink, ez, bf, u_of = C.lerp, C.clamp, C.blink, C.ez, C.bf, C.u_of
TMP = os.path.join(HERE, "work")
SHOT = 17
G0, G1 = C.g_bound(35.20), C.g_bound(37.20)              # 1056, 1116
H = 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
DISSOLVE_IN = False
CUES = [{"frame": 1078, "label": "lancet touches the arm", "kind": "foley"}]
PRESET, LIGHT = "garden_hut", None

JAMES = (-8.0, -3.4)
JEN = (-6.9, -2.7)
DOC = (-8.7, 0.3)
CAM0 = ((-2.4, -5.2, 1.55), (-8.0, -1.9, 1.9))
CAM1 = ((-3.4, -4.6, 1.6), (-7.8, -2.0, 1.9))
STOOL_Z = 0.0
ARM = 'upper_arm_r'


def cam_of(g):
    x = clamp((g - G0) / float(G1 - G0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def sore(f, pose, an):
    return C.sore_svg(an[ARM], "blister")


def pose_james(g):
    p = dict(cast11.STORY11["james_sit_sleeve"][1])
    p.update(mirror=True, t=g / 30.0, expr="determined", head_roll=-2 + 1.0 * math.sin(g * 0.08))
    wince = u_of(g, 1074, 1082) * (1 - u_of(g, 1094, 1104))              # a little wince as the lancet touches
    if wince > 0.3:
        p["expr"] = "worried"
    p["blink"] = blink(g, [1062, 1092, 1110])
    return p


def pose_doc(g):
    p = dict(cast11.STORY11["towndoc_scoff_crossed"][1])
    p.update(mirror=True, t=g / 30.0, head_roll=4 + 1.5 * math.sin(g * 0.07), lean=1.0 * math.sin(g * 0.05))
    p["blink"] = blink(g, [1070, 1101])
    return p


def pose_jen(g, tip):
    p = dict(cast11.STORY11["jenner_scratch_arm"][1])
    p.update(mirror=True, t=g / 30.0, head_roll=2 * math.sin(g * 0.09))
    p["prop_r"] = dict(type="lancet", angle=120)
    p["blink"] = blink(g, [1066, 1098])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s17")
        sd = os.path.join(TMP, "sprites")
        self.jam = self.actors["jam"] = C.make_actor("jam", "james", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)
        self.doc = self.actors["doc"] = C.make_actor("doc", "towndoc", sd)

    def pose(self, shot, gs):
        fr = [bf(shot, g) for g in gs]
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jam, f, JAMES, z=STOOL_Z, scale=C.SCALE["james"])
            C.place(self.jen, f, JEN, scale=C.SCALE["jenner"])
            C.place(self.doc, f, DOC, scale=C.SCALE["towndoc"])
        for g in gs:                                       # James first: his sprite gives the upper-arm anchor the lancet is pinned to
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jam.pose(f, pose_james(g), camera=self.cam)
            self.doc.pose(f, pose_doc(g), camera=self.cam)
        self.sprites_for([(self.jam, 192)], fr, overlays={"jam": sore})
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            an = self.anch[("jam", f)][ARM]
            w = C.actors.local_to_world(self.jam, an, f, camera=self.cam)
            press = 0.5 + 0.5 * math.sin(g * 0.35)
            tip = (w.x, w.y, w.z)
            hand = {"r": {"tip": tip, "prop": "lancet", "angle": 120}}
            p, info = self.jen.pose(f, pose_jen(g, tip), hands=hand, camera=self.cam)
            if g % 20 == 0:
                print("lancet reach error g%d: %.3f" % (g, info["r"]["error"]), flush=True)
        self.sprites_for([(self.jen, 192), (self.doc, 192)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

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
