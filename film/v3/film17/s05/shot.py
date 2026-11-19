#!/usr/bin/env python3
"""film 17 take s05 = shot 13 (21.61-24.08 s): the whole room laughs at Bertillon.  measure_high / DAY_INT, g0 651 g1 725, +-6 handles.
usage: python3 shot.py stills <g list> <outdir> [scale 0.5] | final <g list> [scale] [samples] | probe <g list>"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import lerp, clamp, ease, mix, blink, cast17, K, Vector

G0, G1, H = 651, 725, 6
FIRST, LAST = G0 - H, G1 + H
BASE_C = Vector((2.9, -3.8, 3.55)); BASE_L = Vector((-0.4, 1.9, 1.1))
# camera waypoints: (g, s = distance factor from the look point, lateral metres (right of view), look point, vertical metres)
WP = [
    (FIRST, 0.72, -0.25, (-0.95, 1.90, 0.95), 0.05),
    (688,   0.88,  0.10, (-0.95, 1.90, 1.05), 0.10),
    (704,   0.68, -0.20, (-1.00, 1.80, 1.10), -0.05),  # snap 16 f: push + reframe
    (LAST,  0.80,  0.20, (-1.00, 1.80, 1.10), 0.05),
]
SNAP = (688, 704)
SNAP2 = (712, 724)


def cam_of(g):
    for (g0, *a), (g1, *b) in zip(WP[:-1], WP[1:]):
        if g0 <= g <= g1:
            u = (g - g0) / float(g1 - g0)
            u = ease(u) if (g0, g1) in (SNAP, SNAP2) else mix(u, 0.25)
            if (g0, g1) == SNAP: u = clamp(u + 0.0)
            s = lerp(a[0], b[0], u); lat = lerp(a[1], b[1], u); L = Vector([lerp(x, y, u) for x, y in zip(a[2], b[2])]); dz = lerp(a[3], b[3], u)
            d = BASE_C - BASE_L
            C = L + d * s
            fwd = (L - C); fwd.z = 0; fwd.normalize()
            right = Vector((fwd.y, -fwd.x, 0))
            C = C + right * lat + Vector((0, 0, dz)); C.x = min(C.x, 3.0); C.y = max(C.y, -3.95)
            return C, L + right * lat * 0.55
    raise ValueError(g)


def bounce(g, ph, amp=0.09, hz=3.0):
    return amp * (0.5 + 0.5 * math.sin(2 * math.pi * hz * g / 30.0 + ph))


def laugh_pose(story, g, ph, extra=None, expr="laugh"):
    cast, p = cast17.STORY17[story]
    p = dict(cast17.with_expr(p, expr)) if expr else dict(p)
    p["head_roll"] = p.get("head_roll", 0) + 4 * math.sin(2 * math.pi * 3 * g / 30.0 + ph)
    p["lean"] = p.get("lean", 0) + 2.5 * math.sin(2 * math.pi * 1.5 * g / 30.0 + ph)
    p["squash"] = (1.0 + 0.02 * math.sin(2 * math.pi * 3 * g / 30.0 + ph), 1.0 - 0.02 * math.sin(2 * math.pi * 3 * g / 30.0 + ph))
    p["t"] = g / 30.0
    if extra: p.update(extra)
    return p


POINT_R = dict(hand=(0.95, 0.12), bend=-0.3, stretch=1.1, shape="point", layer="front")
POINT_L = dict(hand=(-0.95, 0.12), bend=-0.3, stretch=1.1, shape="point", layer="front")


def pose_for(key, g):
    ph = {"bench0": 0.0, "bench2": 1.7, "queue0": 3.1, "table": 4.4, "chair": 2.3}.get(key, 0.0)
    bob = 0.04 * math.sin(2 * math.pi * 1.5 * g / 30.0 + ph)
    if key == "bench0":
        return laugh_pose("prisoner_sitting_a", g, ph, dict(arm_r=dict(POINT_R, hand=(0.95, 0.12 + bob)), arm_l=dict(hand=(-0.3, 1.0), bend=0.4)))
    if key == "bench2":                       # the mimic: calipers, jaws on his own ear (hand_for_anchor)
        p = laugh_pose("prisoner_sitting_c", g, ph, dict(arm_r=dict(hand=(0.74, 0.02), bend=-0.7, stretch=1.0, layer="front"),
                       prop_r=dict(type="calipers", scale=0.9, angle=-90), arm_l=dict(hand=(-0.3, 1.0), bend=0.4)))
        return cast17.hand_for_anchor("prisoner_c", p, "r", "calipers_r", (0.50 + 0.03 * math.sin(g * 0.5), 0.02))
    if key == "queue0":                       # gendarme points at Bertillon
        return laugh_pose("gendarme_laughing_a", g, ph, dict(arm_r=dict(POINT_R, hand=(0.95, 0.12 + bob)), arm_l=dict(hand=(-0.34, 0.96), bend=0.9, shape="open")), expr=None)
    if key == "table":                        # second gendarme points (screen left, at Bertillon)
        return laugh_pose("gendarme_laughing_b", g, ph, dict(arm_l=dict(POINT_L, hand=(-0.95, 0.12 + bob)), arm_r=dict(hand=(0.3, 0.98), bend=0.9, shape="open")), expr=None)
    if key == "chair":
        return laugh_pose("inspector_seated_stiff", g, ph, dict(fx=["tears"]))
    if key == "tripod":                       # Bertillon, small and stiff, blinking
        cast, p = cast17.STORY17["bertillon_neutral"]
        p = dict(cast17.with_expr(p, "worried")); p["blink"] = blink(g, [FIRST + 14, FIRST + 58])
        p["lean"] = 1.5 * math.sin(g * 0.12); p["head_roll"] = -3 + 2 * math.sin(g * 0.1); p["yaw"] = -0.3
        p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.2)); p["t"] = g / 30.0
        return cast17.silent(p)
    raise KeyError(key)


class S05(C.Take):
    def __init__(self, mode, samples=None, threads=2):
        C.Take.__init__(self, "measure_high", "DAY_INT", mode=mode, samples=samples, threads=threads)
        self.add("bench0", "bench0", "prisoner_sitting_a", seated="bench")
        self.add("bench2", "bench2", "prisoner_sitting_c", seated="bench")
        self.add("queue0", "armspan", "gendarme_laughing_a")
        self.add("table", "clerk", "gendarme_laughing_b", dx=-0.55)
        self.add("chair", "chair", "inspector_seated_stiff", seated="chair")
        self.add("tripod", "tripod", "bertillon_neutral")

    def pose(self, gs):
        K.key_life(min(gs), max(gs), dust=0.4)
        for g in gs:
            loc, look = cam_of(g); self.key_cam(g, loc, look)
        for g in gs:
            self.scene.frame_set(g)
            for k in self.acts:
                dz = bounce(g, {"bench0": 0, "bench2": 1.7, "queue0": 3.1, "table": 4.4, "chair": 2.3}[k]) if k != "tripod" else 0.0
                p = self.pose_cast(k, g, pose_for(k, g), dz=dz)
                self.finish_poses(g, k, p)
        self.make_sprites(gs)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = C.parse(sys.argv[2])
    if cmd in ("stills", "probe"):
        T = S05("draft", samples=6)
        T.pose(gs)
        for g in gs:
            print(g, json.dumps(T.heads(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; os.makedirs(out, exist_ok=True)
                print("render", g, "%.1fs" % T.render(g, os.path.join(out, "g_%04d.png" % g)), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        mode = "draft" if scale < 1 else "final"
        out = os.path.join(HERE, "raw", "%s_s%d" % (mode, samples)); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        if todo:
            T = S05(mode, samples=samples); T.pose(todo)
            rep = {}
            for g in todo:
                dt = T.render(g, os.path.join(out, "g_%04d.png" % g)); rep[g] = T.heads(g)
                print("g %d %.1fs" % (g, dt), flush=True)
                json.dump(rep[g], open(os.path.join(out, "g_%04d.json" % g), "w"))
