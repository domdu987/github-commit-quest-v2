#!/usr/bin/env python3
"""film 17 take s06 = shots 14-15 (24.08-28.25 s).  14: records_desk / EVENING_INT g 719(handle)-782; 15: records_low / EVENING_INT g 783-856 (g1 850 + 6).
usage: python3 shot.py stills <shot> <g list> <outdir> | final <shot> <g list> [scale] [samples]"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import lerp, clamp, ease, mix, blink, cast17, K, Vector
import puppet as P

_prev_hand = P._hand
def _glove(k, H, dirv, shape, hr=P.HAND_R, fold=1.0):
    """director fix: 'three' = a big bright glove with three clearly spread fingers (runtime override, the cast module is untouched)."""
    if shape != "three":
        return _prev_hand(k, H, dirv, shape, hr, fold)
    ux, uy = dirv; g = 2.7; o = []
    def rot(a):
        c, s_ = math.cos(math.radians(a)), math.sin(math.radians(a)); return ux * c - uy * s_, ux * s_ + uy * c
    for a in (-30.0, 0.0, 30.0):
        vx, vy = rot(a); fl = 0.205 if a == 0.0 else 0.18
        x1, y1 = H[0] + vx * fl, H[1] + vy * fl
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.074" stroke-linecap="round"/>' % (H[0], H[1], x1, y1, k.ink))
        k.ext.append((x1, y1, 0.05))
    for a in (-30.0, 0.0, 30.0):
        vx, vy = rot(a); fl = 0.205 if a == 0.0 else 0.18
        o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="#fbf6ee" stroke-width="0.046" stroke-linecap="round"/>' % (H[0], H[1], H[0] + vx * fl, H[1] + vy * fl))
    vx, vy = rot(-78.0)
    o.append('<path d="M%.4f,%.4f L%.4f,%.4f" stroke="%s" stroke-width="0.07" stroke-linecap="round"/><path d="M%.4f,%.4f L%.4f,%.4f" stroke="#fbf6ee" stroke-width="0.044" stroke-linecap="round"/>'
             % (H[0], H[1], H[0] + vx * 0.09, H[1] + vy * 0.09, k.ink, H[0], H[1], H[0] + vx * 0.09, H[1] + vy * 0.09))
    o.append('<circle cx="%.4f" cy="%.4f" r="0.115" fill="%s"/><circle cx="%.4f" cy="%.4f" r="0.095" fill="#fbf6ee"/>' % (H[0], H[1], k.ink, H[0], H[1]))
    o.append('<ellipse cx="%.4f" cy="%.4f" rx="0.04" ry="0.025" fill="#ffffff" transform="rotate(-35 %.4f %.4f)"/>' % (H[0] - 0.035, H[1] - 0.04, H[0] - 0.035, H[1] - 0.04))
    k.ext.append((H[0], H[1], 0.13))
    return "".join(o)
P._hand = _glove

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
    (770, (0.00, 1.45, 1.50), (-0.30, 3.5, 1.45)),
    (780, (0.60, 1.00, 1.50), (-0.10, 3.5, 1.45)),      # snap B (12 f): pull out + slide right
    (782, (0.63, 0.97, 1.50), (-0.09, 3.5, 1.45)),
], [(746, 756), (770, 780)])
TB = (0.45, 2.4)          # Bertillon's mark in shot 15 (low_a)
cam15 = cam_gen([
    (783, (-0.95, -1.00, 0.55), (0.95, 2.4, 1.90)),
    (791, (0.95, -0.95, 0.58), (-0.05, 2.4, 1.90)),     # sweep 1 (8 f): lateral + pan, same distance (no scale pop)
    (808, (0.55, -0.85, 0.60), (0.05, 2.4, 1.90)),
    (816, (-0.95, -1.00, 0.58), (1.00, 2.4, 1.90)),     # sweep 2 (8 f)
    (832, (-0.40, -0.95, 0.58), (0.90, 2.4, 1.90)),
    (840, (0.95, -0.90, 0.60), (-0.05, 2.4, 1.90)),     # sweep 3 (8 f)
    (856, (0.50, -0.85, 0.58), (0.05, 2.4, 1.90)),
], [(783, 791), (808, 816), (832, 840)])


def bertillon14(g):
    cast, p = cast17.STORY17["bertillon_writing"]
    p = dict(cast17.with_expr(p, "worried" if g > G_THREE - 14 else "determined"))
    p["prop_r"] = dict(p["prop_r"], angle=200 + 4 * math.sin(g * 0.7))          # the pen keeps writing
    p["prop_l"] = None                                                           # no card across the chest (director)
    p["arm_l"] = dict(hand=(-0.10, 1.12), bend=0.7, stretch=1.0, layer="front")  # the free hand rests on the desk
    p["blink"] = blink(g, [735, 772]); p["lean"] = 5 + 1.5 * math.sin(g * 0.13); p["t"] = g / 30.0
    return p


def prefect14(g):
    """stern -> the right arm bends up beside the face, a big three-finger glove (see _glove), held still g756-772, pointing toward Bertillon."""
    _, a = cast17.STORY17["prefect_stern"]; _, b = cast17.STORY17["prefect_finger_up_three"]
    u = ease(clamp((g - 746) / 10.0))
    p = dict(b if u >= 0.5 else a)
    hold = (0.80, 0.02)
    bob = 0.0 if g < 773 else 0.02 * math.sin((g - 773) * 0.35)
    p["arm_r"] = dict(hand=(lerp(0.30, hold[0], u), lerp(0.86, hold[1], u) + bob), bend=lerp(0.6, -0.85, u), stretch=1.0, sharp=0.6, shape="three" if u > 0.5 else "ball", layer="front")
    p["arm_l"] = dict(a["arm_l"])
    p["yaw"] = 0.45                                                              # turned toward Bertillon
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.1); p["blink"] = blink(g, [745, 790]); p["t"] = g / 30.0
    return p


def bertillon15(g):
    cast, p = cast17.STORY17["bertillon_neutral"]
    u = ease(clamp((g - 806) / 10.0)); push = 0.025 * math.sin((g - 816) * 0.5) if g >= 816 else 0.0
    p = dict(cast17.with_expr(p, "worried"))
    # fingertips on the bridge of the pince-nez, drawn in front of the face ('top' layer)
    p["arm_r"] = dict(hand=(lerp(0.40, 0.17, u), lerp(1.0, 0.07, u) + push), bend=lerp(0.3, -0.9, u), stretch=1.0, layer="top", shape="point" if u > 0.5 else "ball")
    p["arm_l"] = "down"; p["yaw"] = 0.25; p["pitch"] = 0.12 * math.sin(g * 0.09)
    p["lean"] = 1.5 * math.sin(g * 0.11) - 1 * u; p["head_roll"] = -2 + 1.5 * math.sin(g * 0.13)
    p["blink"] = blink(g, [800, 838]); p["t"] = g / 30.0
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.2))
    return p


def prefect15(g):
    """the prefect walks away down the aisle (profile, 'walk' cycle)."""
    _, base = cast17.STORY17["prefect_neutral"]
    return cast17.cycle("prefect", (g - 783) / 30.0, "walk", 1, dict(base, yaw=0.75, arms="both"))


def prefect15_dy(g):
    return lerp(-0.6, 3.8, clamp((g - 783) / 74.0))


class S06(C.Take):
    def __init__(self, shot, mode, samples=None, threads=2):
        self.shot = shot
        C.Take.__init__(self, PRESET[shot], "EVENING_INT", mode=mode, samples=samples, threads=threads, fg=(shot == 14))
        if shot == 14:
            self.add("bert", "desk_clerk", "bertillon_writing")
            self.add("pref", "desk_stand", "prefect_stern", mirror=True)
        else:
            self.add("bert", "low_a", "bertillon_neutral")
            self.add("pref", "wall_look", "prefect_neutral", dx=-0.45)

    def pose(self, gs):
        K.key_life(min(gs), max(gs), dust=0.4)
        cf = cam14 if self.shot == 14 else cam15
        for g in gs:
            loc, look = cf(g); self.key_cam(g, loc, look)
        for g in gs:
            self.scene.frame_set(g)
            for k in self.acts:
                if self.shot == 14:
                    p = bertillon14(g) if k == "bert" else prefect14(g); dy = 0.0
                else:
                    p = bertillon15(g) if k == "bert" else prefect15(g); dy = prefect15_dy(g) if k == "pref" else 0.0
                p = cast17.silent(p)
                if k == "pref" and self.shot == 15:
                    p["mirror"] = False
                self.finish_poses(g, k, self.pose_cast(k, g, p, dy=dy))
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
