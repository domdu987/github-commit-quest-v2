#!/usr/bin/env python3
"""shot.py -- film 3 take s09: shots 9 and 10, harbor set WINTER (engine: take3.py, same folder).

    shot 9   g 747..836  9-frame dissolve in (in-handle g 741..746).
             9a g 741..779  low camera along the tank foot (tank_low family): tommy and the two workers paint the tank brown;
                            set_paint 0 -> 0.142 (the brown climbs from the foot past the first seam at z 3), every brush tip is
                            pinned on the wall at the paint line and strokes up and down; slow push and tilt up with the paint.
             9b g 780..843  hard cut-in on "tae ko aep ao" (25.9 s = g 780): days later, the tank all brown; tommy, crouched,
                            sneaks the tin bucket back under the drip (hand pinned on the bail, release g 797), glances left and
                            right, the first glossy drop lands in it.  (Raw to g 843 for the dissolve into shot 10.)
    shot 10  g 837..917  10-frame dissolve (mixed g 832..841, shot 10 raw from g 830).  Commercial Street: two dock workers in
                         front of the camera point back at the tank and laugh (mouths held: no lip movement); on "thang
                         nguea taek" (29.6 s = g 891) a crash zoom (g 887..893, camera forward 8 D, lens 22 -> 230 mm, camera forward 13 D) punches in
                         on the sweating brown seam (seep strips and drops).  Out-handle g 918..925 (12-frame dissolve).

Shot keys: 9 = 9a, 19 = 9b (cut-in), 10.
    python3 shot.py probe|stills|final <9|19|10> <a:b[:step]|all> [out_dir] [scale] [samples]
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import take3 as X                                      # noqa: E402
from take3 import W, g_of, kcam, sph, keys, ease, blink, pulse, lerp, clamp, H, Vector   # noqa: E402
import puppet                                          # noqa: E402
import cast3                                           # noqa: E402

G9, G10, G11 = 747, 837, 918
H_IN = 9 // 2 + 2                                      # 6
H_OUT = 12 // 2 + 2                                    # 8
D910 = 10
M0 = G10 - D910 // 2                                   # 832
CUTIN = g_of(25.9)                                     # 780
RNG = {9: (G9 - H_IN, CUTIN - 1), 19: (CUTIN, M0 + D910 + 1), 10: (M0 - 2, G11 + H_OUT - 1)}
NICK = g_of(29.6)                                      # 891
ZOOM = (NICK - 4, NICK + 2)                            # 887..893
RELEASE = 797


# ----------------------------------------------------------------------------- 9a: painting
PZ0, PZ1 = 0.7, 3.4                                   # paint line from / to (z, D)
def paint_z(g):
    return PZ0 + (PZ1 - PZ0) * ease((g - (G9 - H_IN)) / float(CUTIN - (G9 - H_IN)), "sine") * 0.92 + (PZ1 - PZ0) * 0.08 * clamp((g - 741) / 39.0)


def paint_state(z):
    return (z + 0.5) / (H.ROOF_Z + 1.2)


T9 = W(-0.7, 0.95)
W2_9 = W(-2.9, 1.05)
W1_9 = W(-5.0, 1.15)
HEAD9 = Vector((T9.x, T9.y, 1.9))


def cam9(g):
    lk = W(-1.9, 1.0, 2.1)
    ks = [(RNG[9][0], (7.2, -26.0, 7.0, lk.x, lk.y, 2.0), "sine"),
          (760, (6.8, -24.0, 9.0, lk.x, lk.y, 2.15), "sine"),
          (RNG[9][1], (6.3, -21.0, 12.0, lk.x, lk.y, 2.4), "hold")]
    return kcam(g, ks, 0.2)


def stroke(g, period, phase, amp):
    return amp * math.sin(2 * math.pi * (g + phase) / period)


def brush_pt(g, t, zmax, period, phase, amp=0.32, zmin=1.0):
    z = max(zmin, min(paint_z(g), zmax)) + stroke(g, period, phase, amp) - 0.05
    return W(t, 0.04, z)


def tommy9(g):
    p = dict(cast3.STORY3["tommy_paint"][1])
    p.pop("arm_r", None)
    p["blink"] = blink(g, [752, 774])
    p["head_roll"] = -4 + 3 * math.sin(g * 0.4)
    ang = -52 + 12 * math.sin(2 * math.pi * (g + 2) / 14.0)
    hands = {"r": {"tip": brush_pt(g, -0.05, 2.3, 14.0, 2, 0.32, 1.1), "prop": "paintbrush", "angle": ang, "stretch": 1.3, "bend": -0.6}}
    p["prop_r"] = dict(type="paintbrush", angle=ang)
    return p, hands


def worker2_9(g):
    p = dict(cast3.STORY3["workers_paint_beard"][1])
    p.pop("arm_r", None)
    p["blink"] = blink(g, [758])
    ang = -25 + 10 * math.sin(2 * math.pi * (g + 7) / 17.0)
    p["prop_r"] = dict(type="paintbrush", angle=ang)
    hands = {"r": {"tip": brush_pt(g, -2.1, 2.9, 17.0, 7, 0.4, 1.5), "prop": "paintbrush", "angle": ang, "stretch": 1.25, "bend": -0.5}}
    return p, hands


def worker1_9(g):
    p = dict(cast3.STORY3["workers_paint"][1])
    p["mirror"] = True
    p.pop("arm_l", None)
    ang = -55 + 10 * math.sin(2 * math.pi * (g + 4) / 15.0)
    p["prop_l"] = dict(type="paintbrush", angle=-180 - ang)
    p["blink"] = blink(g, [766])
    hands = {"l": {"tip": brush_pt(g, -5.75, 3.45, 15.0, 4, 0.35, 1.9), "prop": "paintbrush", "angle": ang, "stretch": 1.25, "bend": -0.6}}
    return p, hands


def state9(g):
    return dict(paint=paint_state(paint_z(g)), seep=0.8, bucket=(W(-6.0, 3.0), 0.0, False, None))


# ----------------------------------------------------------------------------- 9b: the cut-in
T19 = W(-1.05, 0.62)
B_END = Vector(H.BUCKET_MARK)
B_START = W(-0.3, 0.6, 0.14)


def bucket19(g):
    u = ease((g - CUTIN) / float(RELEASE - 3 - CUTIN), "sine")
    p = B_START.lerp(B_END, u)
    p.z = B_START.z * (1 - ease((g - CUTIN) / float(RELEASE - 3 - CUTIN), "cubic_out")) if g < RELEASE - 3 else 0.0
    return p


HEAD19 = Vector((T19.x, T19.y, 1.35))


def cam19(g):
    look = HEAD19.lerp(B_END, 0.42)
    ks = [(CUTIN, (3.3, 6.0, -4.0, look.x, look.y, 1.15), "sine"),
          (812, (3.05, 3.0, -3.0, look.x, look.y, 1.1), "cubic"),
          (RNG[19][1], (2.8, -2.0, -2.0, look.x - 0.05, look.y, 1.05), "hold")]
    return kcam(g, ks, 0.2)


def tommy19(g):
    bp = dict(cast3.STORY3["tommy_bucket_place"][1])
    bp.pop("prop_r", None)
    bp = dict(bp)
    hands = None
    if g < RELEASE:
        b = bucket19(g)
        hands = {"r": {"hand": (b.x, b.y, b.z + 1.06), "stretch": 1.3, "bend": -0.3}}
        bp["expr"] = "worried"
        bp["gaze"] = (0.6, 0.5)
    else:
        u = ease((g - RELEASE) / 6.0, "sine")
        bp["arm_r"] = dict(hand=(0.55 - 0.15 * u, 0.95 - 0.1 * u), bend=0.4)
        # sneaky glances: left (toward camera-left) g 800..815, right/up toward the drip g 818..832, then a small smirk
        if g < 816:
            bp["yaw"] = 0.6 - 1.1 * ease((g - 800) / 5.0, "sine") if g >= 800 else 0.6
            bp["gaze"] = (-1.0, 0.0) if g >= 802 else (0.6, 0.5)
            bp["expr"] = "worried"
        elif g < 833:
            bp["yaw"] = -0.5 + 1.2 * ease((g - 816) / 5.0, "sine")
            bp["gaze"] = (0.9, -0.8)
            bp["expr"] = "worried"
        else:
            bp["yaw"] = 0.7
            bp["gaze"] = (0.3, -0.2)
            bp["expr"] = "smirk"
    bp["blink"] = blink(g, [788, 815, 831])
    bp["head_roll"] = bp.get("head_roll", 6) + 2 * math.sin(g * 0.2)
    return bp, hands


DROPS19 = [dict(key="d0", strip=0, period=22, form=14, phase=7, floor=0.40, size=1.8, on=lambda g: g >= RELEASE - 4)]


def state19(g):
    fill = 0.08 + 0.05 * clamp((g - 805) / 40.0)
    return dict(paint=1.0, seep=0.85, bucket=(bucket19(g), fill, True, None))


# ----------------------------------------------------------------------------- 10: the street, crash zoom on the seam
C10 = Vector((2.3, -30.5, 2.25))
SEAM10 = W(0.1, 0.0, 2.45)
_f10 = (SEAM10 - C10); _f10.z = 0; _f10.normalize()
_r10 = Vector((_f10.y, -_f10.x, 0))
WK1 = C10 + _f10 * 4.0 - _r10 * 1.25; WK1.z = 0.0
WK2 = C10 + _f10 * 4.4 + _r10 * 1.35; WK2.z = 0.0


def cam10(g):
    hd = math.degrees(math.atan2(_f10.x, _f10.y))
    look0 = C10 + _f10 * 5.0 + Vector((0, 0, 0.55))
    look1 = C10 + _f10 * 5.0 + Vector((0, 0, 0.75))
    if g < ZOOM[0]:
        u = ease((g - RNG[10][0]) / float(ZOOM[0] - RNG[10][0]), "sine")
        u = 0.85 * u + 0.15 * (g - RNG[10][0]) / float(ZOOM[0] - RNG[10][0])
        loc = C10 + _r10 * (0.25 - 0.45 * u) + _f10 * (0.0 + 0.6 * u)
        look = look0.lerp(look1, u) + _r10 * (0.1 - 0.25 * u)
        return loc, look, 22.0
    z0 = (C10 + _r10 * -0.2 + _f10 * 0.6, look1 + _r10 * -0.15, 22.0)
    z1 = (C10 + _f10 * 13.0 + Vector((0, 0, 0.1)), SEAM10 + Vector((0, 0, 0.05)), 230.0)
    z2 = (C10 + _f10 * 14.2 + Vector((0, 0, 0.1)), SEAM10 + Vector((0.0, 0, -0.15)), 240.0)
    if g <= ZOOM[1]:
        u = ease((g - ZOOM[0]) / float(ZOOM[1] - ZOOM[0]), "quint")
        lens = math.exp(math.log(z0[2]) + (math.log(z1[2]) - math.log(z0[2])) * u)
        return z0[0].lerp(z1[0], u), z0[1].lerp(z1[1], u), lens
    u = (g - ZOOM[1]) / float(RNG[10][1] - ZOOM[1])
    u = 0.7 * ease(u, "cubic_out") + 0.3 * u
    return z1[0].lerp(z2[0], u), z1[1].lerp(z2[1], u), z1[2] + (z2[2] - z1[2]) * u


def wk1_10(g):
    p = dict(cast3.STORY3["workers_laugh"][1])
    p["mirror"] = True
    b = math.sin(g * 0.9)
    p["head_roll"] = -10 + 3 * b
    p["squash"] = (1.0 + 0.012 * b, 1.0 - 0.012 * b)
    p["t"] = (g - 830) / 30.0
    p["arm_l"] = dict(p["arm_l"]); h = p["arm_l"]["hand"]; p["arm_l"]["hand"] = (h[0], h[1] - 0.04 * math.sin(g * 0.45))
    return p, None


def wk2_10(g):
    p = dict(cast3.STORY3["workers_laugh_beard"][1])
    b = math.sin(g * 0.8 + 2)
    p["head_roll"] = 12 + 3 * b
    p["lean"] = -5 - 2 * abs(b)
    p["squash"] = (1.0 + 0.012 * b, 1.0 - 0.012 * b)
    return p, None


DROPS10 = [dict(key="d0", strip=0, period=22, form=14, phase=7, floor=0.40, size=1.8),
           dict(key="d1", strip=1, period=29, form=18, phase=2, floor=0.02, size=1.4),
           dict(key="d2", strip=2, period=35, form=22, phase=19, floor=0.02, size=1.4),
           dict(key="d3", strip=3, period=31, form=20, phase=11, floor=0.02, size=1.4),
           dict(key="d4", strip=4, period=27, form=16, phase=23, floor=0.02, size=1.4)]


def state10(g):
    return dict(paint=1.0, seep=1.0, bucket=(H.BUCKET_MARK, 0.3, True, None))


def build_fg(tk):
    """9a: a trestle-like shaded post at the near-left edge; 9b: a shaded barrel at the left edge"""
    M = tk.M
    loc, look = cam9(RNG[9][0])
    f = (look - loc); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0))
    p = loc + f * 1.6 - r * 1.15
    obs9 = [X._box("s9_post", (p.x - 0.22, p.y - 0.22, 0.0), (p.x + 0.22, p.y + 0.22, 9.0), M["wood"], tk.coll)]
    loc, look = cam19(CUTIN)[:2]
    f = (look - loc); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0))
    q = loc + f * 1.5 - r * 0.95
    obs19 = X.barrel("s19_barrel", (q.x, q.y, 0.0), tk.coll, M)
    for o in obs9 + obs19:
        o.visible_shadow = False
    return {"fg9": obs9, "fg19": obs19}


SHOTS = {
    9: dict(rng=RNG[9], cam=cam9, state=state9, fg=("fg9",), drops=[],
            actors={"tommy": dict(cast="tommy", place=lambda g: T9, pose=tommy9, ppd=320),
                    "worker2": dict(cast="worker2", place=lambda g: W2_9, pose=worker2_9, ppd=320),
                    "worker1": dict(cast="worker1", place=lambda g: W1_9, pose=worker1_9, ppd=256)}),
    19: dict(rng=RNG[19], cam=cam19, state=state19, fg=("fg19",), drops=DROPS19,
             actors={"tommy": dict(cast="tommy", place=lambda g: T19, pose=tommy19, ppd=448)},
             marks={"bucket": B_END}),
    10: dict(rng=RNG[10], cam=cam10, state=state10, fg=(), drops=DROPS10,
             actors={"worker1": dict(cast="worker1", place=lambda g: WK1, pose=wk1_10, ppd=384),
                     "worker2": dict(cast="worker2", place=lambda g: WK2, pose=wk2_10, ppd=384)},
             marks={"seam": SEAM10}),
}

if __name__ == "__main__":
    X.main(SHOTS, build_fg, "s09")
