#!/usr/bin/env python3
"""film 17 take s06 = shots 14-15 (24.08-28.25 s).  14: records_desk / EVENING_INT g 719(handle)-782; 15: records_low / EVENING_INT g 783-856 (g1 850 + 6).
usage: python3 shot.py stills <shot> <g list> <outdir> | final <shot> <g list> [scale] [samples]"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import lerp, clamp, ease, mix, blink, cast17, K, Vector
import puppet

RANGE = {14: (719, 782), 15: (783, 856)}
PRESET = {14: "records_desk", 15: "records_low"}
G_THREE = 768          # "สามเดือน" 25.49 s


def cam_gen(wps, snap):
    """explicit waypoints (g, loc, look); mix easing (never a dead end); the snap segment eases in-out."""
    def f(g):
        for (g0, c0, l0), (g1, c1, l1) in zip(wps[:-1], wps[1:]):
            if g0 <= g <= g1:
                u = (g - g0) / float(g1 - g0); u = ease(u) if (g0, g1) in snap else mix(u, 0.1)
                return Vector([lerp(x, y, u) for x, y in zip(c0, c1)]), Vector([lerp(x, y, u) for x, y in zip(l0, l1)])
        raise ValueError(g)
    return f

cam14 = cam_gen([
    (719, (0.95, 0.00, 1.55), (-0.60, 3.0, 1.40)),
    (746, (0.25, 0.85, 1.50), (-0.35, 3.2, 1.42)),
    (756, (-0.60, 1.70, 1.50), (-0.35, 3.5, 1.45)),     # snap A (12 f): push + slide left; the finger shape swaps at its peak
    (770, (0.00, 1.45, 1.50), (-0.45, 3.5, 1.45)),
    (780, (0.60, 1.00, 1.50), (-0.15, 3.5, 1.45)),      # snap B (12 f): pull out + slide right
    (782, (0.63, 0.97, 1.50), (-0.14, 3.5, 1.45)),
], [(746, 756), (770, 780)])
cam15 = cam_gen([
    (783, (-0.60, -0.95, 0.50), (-0.20, 3.0, 2.0)),
    (802, (0.55, -0.45, 0.55), (-0.10, 3.0, 2.0)),
    (812, (-0.15, 1.15, 0.80), (0.40, 3.0, 2.0)),       # snap 1 (10 f): push in on the pince-nez; hand shape swaps at its peak
    (828, (-0.55, 0.75, 0.70), (0.30, 3.0, 1.95)),
    (838, (0.95, -0.45, 0.55), (-0.20, 3.0, 1.9)),      # snap 2 (10 f): pull out + slide right
    (856, (0.35, 0.15, 0.62), (0.05, 3.0, 1.9)),
], [(802, 812), (828, 838)])


def bertillon14(g):
    cast, p = cast17.STORY17["bertillon_writing"]
    p = dict(cast17.with_expr(p, "worried" if g > G_THREE - 14 else "determined"))
    nib = 4 * math.sin(g * 0.7)
    p["prop_r"] = dict(p["prop_r"], angle=200 + nib)
    p["blink"] = blink(g, [735, 790 if False else 772]); p["lean"] = 5 + 1.5 * math.sin(g * 0.13); p["t"] = g / 30.0
    return p


def prefect14(g):
    _, a = cast17.STORY17["prefect_stern"]; _, b = cast17.STORY17["prefect_finger_up_three"]
    u = clamp((g - 746) / 10.0)
    p = dict(b if u >= 0.5 else a)
    if 0 < u < 1:
        p["arm_r"] = dict(b["arm_r"], hand=(lerp(0.3, 0.98, ease(u)), lerp(0.86, -0.42, ease(u))), bend=lerp(0.6, -0.7, ease(u)), shape="three" if u > 0.5 else "ball")
        p["arm_l"] = dict(a["arm_l"])
    if u >= 1:
        p["arm_r"] = dict(b["arm_r"], hand=(0.98, -0.42 + 0.025 * math.sin((g - G_THREE) * 0.35)))   # the finger bobs on the beat
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.1); p["blink"] = blink(g, [745, 790]); p["t"] = g / 30.0
    return p


def bertillon15(g):
    cast, p = cast17.STORY17["bertillon_neutral"]
    u = ease(clamp((g - 802) / 10.0)); w = 0.02 * math.sin((g - 812) * 0.45) * u if g >= 812 else 0.0
    p = dict(cast17.with_expr(p, "worried"))
    p["arm_r"] = dict(hand=(lerp(0.40, 0.30, u) + w, lerp(1.0, 0.10, u) + 0.5 * w), bend=lerp(0.3, -0.8, u), stretch=1.0, layer="front", shape="point" if u > 0.5 else "ball")
    p["arm_l"] = "down"; p["yaw"] = 0.25; p["pitch"] = 0.12 * math.sin(g * 0.09)
    p["lean"] = 1.5 * math.sin(g * 0.11) - 1 * u; p["head_roll"] = -2 + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, [800, 838]); p["t"] = g / 30.0
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.2))
    return p


class S06(C.Take):
    def __init__(self, shot, mode, samples=None, threads=2):
        self.shot = shot
        C.Take.__init__(self, PRESET[shot], "EVENING_INT", mode=mode, samples=samples, threads=threads)
        if shot == 14:
            self.add("bert", "desk_clerk", "bertillon_writing")
            self.add("pref", "desk_stand", "prefect_stern", mirror=True)
        else:
            self.add("bert", "low_a", "bertillon_neutral")

    def pose(self, gs):
        K.key_life(min(gs), max(gs), dust=0.4)
        cf = cam14 if self.shot == 14 else cam15
        for g in gs:
            loc, look = cf(g); self.key_cam(g, loc, look)
        for g in gs:
            self.scene.frame_set(g)
            for k in self.acts:
                p = (bertillon14(g) if self.shot == 14 else bertillon15(g)) if k == "bert" else prefect14(g)
                self.finish_poses(g, k, self.pose_cast(k, g, cast17.silent(p)))
        self.make_sprites(gs)


if __name__ == "__main__":
    cmd = sys.argv[1]; shot = int(sys.argv[2]); lo, hi = RANGE[shot]
    gs = [g for g in C.parse(sys.argv[3]) if lo <= g <= hi]
    if cmd == "stills":
        T = S06(shot, "draft", samples=6); T.pose(gs); out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        for g in gs:
            print(g, json.dumps(T.heads(g)), flush=True); print("render", g, "%.1fs" % T.render(g, os.path.join(out, "g_%04d.png" % g)), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        mode = "draft" if scale < 1 else "final"
        out = os.path.join(HERE, "raw", "%s_s%d" % (mode, samples)); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        if todo:
            T = S06(shot, mode, samples=samples); T.pose(todo)
            for g in todo:
                dt = T.render(g, os.path.join(out, "g_%04d.png" % g)); json.dump(T.heads(g), open(os.path.join(out, "g_%04d.json" % g), "w")); print("g %d %.1fs" % (g, dt), flush=True)
