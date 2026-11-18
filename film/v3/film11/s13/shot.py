#!/usr/bin/env python3
"""shot.py -- film 11 take s13: shot 13, day 9 (the false payoff opens): "วันที่เก้า เด็กตัวร้อน นอนซม" g 776..842 (+6 handle frames each side).
room_night / light C (candle).  James lies feverish in bed under the patchwork quilt (in_bed: flush, sweat, sad), his mother sits worried at the
bedside; the candle burns on the table in the foreground (set hook).  Slow push-in from behind the candle toward the bed.
No mouths (nobody speaks).  Sore: the blister card (overlay in James's sprite at upper_arm_l; blister = day 11+ look).
    python3 shot.py probe 13 a:b[:step]
    python3 shot.py stills 13 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 13 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
import cast11                                            # noqa: E402
from mathutils import Vector                             # noqa: E402

lerp, clamp, blink, ez, bf, u_of = C.lerp, C.clamp, C.blink, C.ez, C.bf, C.u_of
TMP = os.path.join(HERE, "work")
SHOT = 13
G0, G1 = C.g_bound(25.86), C.g_bound(28.10)              # 776, 843 (next shot starts at 843)
H = 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
DISSOLVE_IN = True
CUES = [{"frame": 779, "label": "candle flame flickers, fever night, soft wooden creak, the sick boy breathes heavily", "kind": "ambience"}]
PRESET, LIGHT = "room_night", None
TINT = "#f6dcc4"

CAM0 = ((0.9, 1.2, 3.0), (-3.5, 8.0, 1.95))
CAM1 = ((-1.2, 2.7, 2.75), (-3.9, 7.9, 1.95))
BED = (-5.2, 7.0)
BED_Z = 1.86
MOM = (-2.7, 8.1)


def cam_of(g):
    x = clamp((g - G0) / float(G1 - G0))
    u = 0.3 * ez(x, "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def quilt_svg():
    cols = ["#b9a98a", "#a9784a", "#7f9580", "#6f7f98", "#b9a98a", "#9a6a4a"]
    x0, x1, y0, y1 = -0.66, 0.14, 1.02, 1.93
    n, m = 2, 2
    w, h = (x1 - x0) / n, (y1 - y0) / m
    s = '<g stroke="#3a2832" stroke-width="0.018">'
    for i in range(n):
        for j in range(m):
            s += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="%s"/>' % (x0 + i * w, y0 + j * h, w, h, cols[(i * 2 + j * 3) % len(cols)])
    s += '</g>'
    # folded cream cuff at the chest edge
    s += '<rect x="%.3f" y="%.3f" width="0.11" height="%.3f" rx="0.04" fill="#f3ead4" stroke="#3a2832" stroke-width="0.02"/>' % (x1 - 0.02, y0 - 0.04, y1 - y0 + 0.08)
    return s


def james_overlay(f, pose, an):
    return quilt_svg() + C.sore_svg(an["upper_arm_l"], "blister")


def pose_james(g):
    p = dict(cast11.STORY11["james_in_bed"][1])
    p.update(lie=-90, head_roll=-72 + 2.0 * math.sin(g * 0.09), pitch=0.05 * math.sin(g * 0.07), tint=TINT, t=g / 30.0)
    p["blink"] = blink(g, [790, 812, 835])
    p["arm_r"] = dict(hand=(0.18, 0.9 + 0.02 * math.sin(g * 0.11)), bend=0.6)
    return p


def pose_mother(g):
    p = dict(cast11.STORY11["mother_sit_worried"][1])
    k = math.sin(g * 0.13)
    p.update(mirror=True, tint=TINT, head_roll=-3 + 2.0 * math.sin(g * 0.08), lean=1.5 * math.sin(g * 0.06),
             arm_r=dict(hand=(0.46 + 0.02 * k, 0.86 + 0.02 * math.sin(g * 0.17)), bend=0.5), prop_r="candle", flame=0.85 + 0.15 * math.sin(g * 0.7),
             arm_l=dict(hand=(0.22 - 0.03 * k, 1.16), bend=0.5))
    p["gaze"] = [0.7 + 0.1 * math.sin(g * 0.05), 0.5]
    p["blink"] = blink(g, [782, 806, 829])
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s13")
        self.jb = self.actors["jb"] = C.make_actor("jb", "james", os.path.join(TMP, "sprites"), canvas=cast11.CANVAS11_LIE["james"])
        self.mom = self.actors["mom"] = C.make_actor("mom", "mother", os.path.join(TMP, "sprites"))

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            C.place(self.jb, f, BED, z=BED_Z, scale=C.SCALE["james"])
            C.place(self.mom, f, MOM, scale=C.SCALE["mother"])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.jb.pose(f, pose_james(g), camera=self.cam)
            self.mom.pose(f, pose_mother(g), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.jb, 192), (self.mom, 192)], fr, overlays={"jb": james_overlay})

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
