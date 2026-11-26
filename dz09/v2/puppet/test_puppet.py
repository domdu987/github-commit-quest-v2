#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_puppet.py -- robustness tests for puppet.py (independent review).

  python3 test_puppet.py            run every check, exit code 1 on any failure (about 2 million checks, 1-2 minutes)
  python3 test_puppet.py --quick    the same checks on a thinner grid (about 20 s)
  python3 test_puppet.py --strip    additionally render tmp/rv/turn_strip.png (30 frames: hero yaw -1 -> +1 while raising an arm)
                                    and check the frame-to-frame pixel change for pops (needs node + playwright, numpy, Pillow)

Checks, for BOTH cast members
  1  every preset / expression / mouth / prop / effect draws: no exception, no NaN or inf in the SVG, finite anchors and bbox
  2  every numeric pose key swept through its full range in 40 steps: anchors move continuously (step bound below), and again
     in 240 steps with a 6 times tighter bound (a real discontinuity keeps its size when the step shrinks, a slope does not)
  3  arm hand target swept along circles around the shoulder, inside reach, at reach and far beyond it (radius up to 50 D), and
     on lines straight through the shoulder: hand stays within reach, hand and elbow move continuously, and with a fixed `bend`
     the elbow never changes side (no flip of the bend direction)
  4  the same for foot targets / knees
  5  garbage input (None, NaN, inf, wrong types, unknown names) never raises; an unknown cast name raises KeyError
  6  determinism, uid isolation (every id carries the uid, every url(#...) resolves), mirror symmetry of anchors,
     resolve_pose / lerp_pose consistency
  7  runtime below 10 ms per figure() call
"""
import math
import os
import random
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import puppet  # noqa: E402

CASTS = ("hero", "boss")
STEP40 = 0.30        # D: largest allowed anchor move between two of the 40 sweep steps
STEP240 = 0.050      # D: the same for the 240-step sweep (6 times finer, bound 6 times tighter)
FAILS = []
COUNT = [0]
QUICK = [False]


def check(cond, msg):
    COUNT[0] += 1
    if not cond:
        FAILS.append(msg)
        if len(FAILS) <= 60:
            print("  FAIL:", msg)
    return cond


_BAD = re.compile(r"nan|inf", re.I)


def finite_fig(f, what):
    ok = True
    s = f["svg"]
    # "nan" / "inf" can only appear as a number: no element or attribute name of the puppet contains these letters in sequence
    m = _BAD.search(s)
    ok &= check(m is None, "%s: '%s' in svg near ...%s..." % (what, m.group(0) if m else "", s[max(0, (m.start() if m else 0) - 40):(m.start() if m else 0) + 20]))
    ok &= check(math.isfinite(f["feet_y"]), "%s: feet_y not finite" % what)
    ok &= check(all(math.isfinite(v) for v in f["bbox"]) and f["bbox"][0] < f["bbox"][2] and f["bbox"][1] < f["bbox"][3], "%s: bad bbox %r" % (what, f["bbox"]))
    for k, v in f["anchors"].items():
        ok &= check(len(v) == 2 and math.isfinite(v[0]) and math.isfinite(v[1]), "%s: anchor %s = %r" % (what, k, v))
    return ok


def draw(cast, pose, what):
    try:
        f = puppet.figure(cast, pose, "t")
    except Exception as e:      # noqa: BLE001
        check(False, "%s: exception %s: %s" % (what, type(e).__name__, e))
        return None
    finite_fig(f, what)
    return f


def max_step(figs):
    """largest anchor displacement between consecutive figures: (distance, anchor name, index)."""
    best = (0.0, "", 0)
    for i in range(1, len(figs)):
        a, b = figs[i - 1]["anchors"], figs[i]["anchors"]
        for k in a:
            if k in b:
                d = math.hypot(a[k][0] - b[k][0], a[k][1] - b[k][1])
                if d > best[0]:
                    best = (d, k, i)
    return best


def side_of(S, E, H):
    """signed distance of the elbow from the shoulder-hand line (sign = bend direction)."""
    dx, dy = H[0] - S[0], H[1] - S[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        return 0.0
    return ((E[0] - S[0]) * dy - (E[1] - S[1]) * dx) / L


def lerp(a, b, t):
    return a + (b - a) * t


# numeric keys: name -> (lo, hi, function value -> pose fragment)
def _arm(key, sub):
    return lambda v: {key: {"preset": "point", sub: v}}


def _leg(sub, base="stand"):
    return lambda v: {"legs": {"preset": base, sub: v}}


NUMERIC = [
    ("yaw", -1.2, 1.2, lambda v: {"yaw": v}),
    ("yaw (step legs, point arm, pencil)", -1.2, 1.2, lambda v: {"yaw": v, "legs": "step", "arm_r": "point", "arm_l": "hip", "prop_r": "pencil", "expr": "smug"}),
    ("yaw (wink, sweat)", -1.2, 1.2, lambda v: {"yaw": v, "expr": "wink", "fx": ["sweat"]}),
    ("pitch", -1.5, 1.5, lambda v: {"pitch": v, "expr": "angry"}),
    ("head_roll", -75.0, 75.0, lambda v: {"head_roll": v}),
    ("head_dx", -0.8, 0.8, lambda v: {"head_dx": v}),
    ("head_dy", -0.8, 0.8, lambda v: {"head_dy": v}),
    ("lean", -75.0, 75.0, lambda v: {"lean": v}),
    ("lean (rigid legs)", -75.0, 75.0, lambda v: {"lean": v, "legs": "lean"}),
    ("squash", 0.3, 2.5, lambda v: {"squash": v}),
    ("squash x", 0.3, 2.5, lambda v: {"squash": (v, 1.0)}),
    ("squash y", 0.3, 2.5, lambda v: {"squash": (1.0, v)}),
    ("gaze x", -1.0, 1.0, lambda v: {"gaze": v}),
    ("gaze y", -1.0, 1.0, lambda v: {"gaze": (0.0, v), "expr": "shocked"}),
    ("t (steam, zzz, tears)", 0.0, 1.0, lambda v: {"t": v, "expr": "laughing", "fx": ["steam", "zzz", "tears", "blush", "anger_fill"]}),
    ("anger level", 0.0, 1.0, lambda v: {"expr": "furious", "fx": [{"type": "anger_fill", "level": v}]}),
    ("limb_w", 0.035, 0.09, lambda v: {"limb_w": v}),
    ("arm_r bend", -1.0, 1.0, _arm("arm_r", "bend")),
    ("arm_l bend", -1.0, 1.0, _arm("arm_l", "bend")),
    ("arm_r sharp", 0.0, 1.0, _arm("arm_r", "sharp")),
    ("arm_r stretch", 0.5, 1.3, _arm("arm_r", "stretch")),
    ("legs spread", -0.2, 0.8, _leg("spread")),
    ("legs stride", -1.5, 1.5, _leg("stride")),
    ("legs crouch", 0.0, 0.75, _leg("crouch")),
    ("legs crouch (wide)", 0.0, 0.75, _leg("crouch", "wide")),
    ("legs lift_r", 0.0, 1.5, _leg("lift_r")),
    ("legs lift_l", 0.0, 1.5, _leg("lift_l")),
    ("legs knee_r", -1.0, 1.0, lambda v: {"legs": {"preset": "crouch", "knee_r": v}}),
    ("legs knee_l", -1.0, 1.0, lambda v: {"legs": {"preset": "crouch", "knee_l": v}}),
    ("legs toe_r", -1.0, 1.0, _leg("toe_r")),
    ("legs toe_l", -1.0, 1.0, _leg("toe_l")),
    ("prop angle", -180.0, 180.0, lambda v: {"arm_r": "forward", "prop_r": {"type": "pointer", "angle": v}}),
    ("prop twist", -180.0, 180.0, lambda v: {"arm_r": "forward", "prop_r": {"type": "paper", "twist": v}}),
    ("prop scale", 0.3, 3.0, lambda v: {"arm_r": "forward", "prop_r": {"type": "pencil", "scale": v}}),
    ("sweat side", -1.0, 1.0, lambda v: {"expr": "worried", "fx": [{"type": "sweat", "side": v}]}),
]
# keys whose anchors legitimately travel far per unit (a 1.17 D pointer swung through 360 degrees, a 3x prop)
LOOSE = {"prop angle": 3.2, "prop twist": 3.2, "prop scale": 1.5}


def test_presets():
    n0 = COUNT[0]
    for cast in CASTS:
        C = puppet.CAST[cast]
        draw(cast, None, "%s default" % cast)
        draw(cast, {}, "%s empty" % cast)
        for e in puppet.EXPRESSIONS:
            for bl in (0, 1, 2):
                for yaw in (-1.0, 0.0, 0.6):
                    draw(cast, {"expr": e, "blink": bl, "yaw": yaw}, "%s expr %s blink %d yaw %s" % (cast, e, bl, yaw))
        for m in puppet.MOUTHS:
            draw(cast, {"mouth": m}, "%s mouth %s" % (cast, m))
        draw(cast, {"mouth": ("open", 0.2, 0.1)}, "%s mouth open" % cast)
        for a in puppet.ARM_PRESETS[C["build"]]:
            for b in puppet.ARM_PRESETS[C["build"]]:
                draw(cast, {"arm_r": a, "arm_l": b, "yaw": 0.4}, "%s arms %s/%s" % (cast, a, b))
        for lg in puppet.LEG_PRESETS:
            for yaw in (-1.0, 0.0, 1.0):
                draw(cast, {"legs": lg, "yaw": yaw, "lean": 10}, "%s legs %s" % (cast, lg))
        for p in puppet.PROP_TYPES:
            draw(cast, {"prop_r": p, "prop_l": {"type": p, "angle": 30, "scale": 1.4}, "arm_r": "forward", "arm_l": "raised"}, "%s prop %s" % (cast, p))
        for fx in puppet.FX_TYPES:
            for t in (0.0, 0.33, 0.99):
                draw(cast, {"fx": [fx], "t": t}, "%s fx %s" % (cast, fx))
        draw(cast, {"fx": list(puppet.FX_TYPES), "tint": "#fbdaf7", "ink": "#1e142e", "mirror": True}, "%s all fx" % cast)
        for name, (c2, pose) in puppet.STORY.items():
            draw(c2, pose, "story %s" % name)
    return COUNT[0] - n0


def test_numeric():
    n0 = COUNT[0]
    worst = (0.0, "")
    for cast in CASTS:
        for name, lo, hi, mk in NUMERIC:
            k40 = STEP40 * LOOSE.get(name, 1.0)
            k400 = STEP240 * LOOSE.get(name, 1.0)
            for n, bound in (((40, k40),) if QUICK[0] else ((40, k40), (240, k400))):
                figs = []
                for i in range(n + 1):
                    f = draw(cast, mk(lerp(lo, hi, i / float(n))), "%s %s = %.4f" % (cast, name, lerp(lo, hi, i / float(n))))
                    if f:
                        figs.append(f)
                d, k, i = max_step(figs)
                check(d <= bound, "%s sweep '%s' in %d steps: anchor %s jumps %.4f D at step %d (value %.4f), bound %.3f"
                      % (cast, name, n, k, d, i, lerp(lo, hi, i / float(n)), bound))
                if n == 240 and d / k400 > worst[0]:
                    worst = (d / k400, "%s '%s' %s %.4f D" % (cast, name, k, d))
            # mirrored figure: same sweep must be just as smooth
            figs = [puppet.figure(cast, dict(mk(lerp(lo, hi, i / 40.0)), mirror=True), "t") for i in range(41)]
            d, k, i = max_step(figs)
            check(d <= k40, "%s mirrored sweep '%s': anchor %s jumps %.4f D" % (cast, name, k, d))
    if not QUICK[0]:
        print("    tightest 240-step sweep: %.0f%% of the bound (%s)" % (100 * worst[0], worst[1]))
    return COUNT[0] - n0


def test_arm_targets():
    """hand target on circles around the shoulder (inside reach .. 50 D away) and on lines through the shoulder."""
    n0 = COUNT[0]
    for cast in CASTS:
        C = puppet.CAST[cast]
        L = C["arm"]
        for key, sgn in (("arm_r", 1), ("arm_l", -1)):
            q = key[-1]
            S = puppet.figure(cast, {}, "t")["anchors"]["shoulder_" + q]
            for bend in ((None, 1.0) if QUICK[0] else (None, 1.0, -1.0, 0.6)):
                for rad in ((0.02, 0.37, 1.0, 50.0) if QUICK[0] else (0.02, 0.10, 0.37, 0.74, 1.0, 5.0, 50.0)):
                    figs, sides = [], []
                    n = 180
                    for i in range(n + 1):
                        a = 2 * math.pi * i / n
                        spec = {"hand": (S[0] + rad * math.cos(a), S[1] + rad * math.sin(a))}
                        if bend is not None:
                            spec["bend"] = bend
                        f = draw(cast, {key: spec}, "%s %s circle r=%.2f a=%d bend=%s" % (cast, key, rad, i, bend))
                        if not f:
                            continue
                        A = f["anchors"]
                        reach = math.hypot(A["hand_" + q][0] - S[0], A["hand_" + q][1] - S[1])
                        check(reach <= L * 1.0 + 1e-6, "%s %s r=%.2f: hand %.3f D from the shoulder, arm is %.2f" % (cast, key, rad, reach, L))
                        check(abs(reach - min(rad, L)) < 1e-6, "%s %s r=%.2f: hand is %.4f D from the shoulder, expected %.4f"
                              % (cast, key, rad, reach, min(rad, L)))
                        figs.append(f)
                        sides.append(side_of(S, A["elbow_" + q], A["hand_" + q]))
                    d, k, i = max_step(figs)
                    # two degrees of a circle of radius <= arm length: the hand moves at most 0.026 D; allow 3x for the elbow
                    check(d <= 0.08, "%s %s circle r=%.2f bend=%s: anchor %s jumps %.4f D at %d deg" % (cast, key, rad, bend, k, d, i))
                    if bend is not None:
                        pos = [s for s in sides if s > 2e-3]
                        neg = [s for s in sides if s < -2e-3]
                        check(not (pos and neg), "%s %s circle r=%.2f bend=%s: bend direction flips (%d steps one way, %d the other)"
                              % (cast, key, rad, bend, len(pos), len(neg)))
                    else:
                        # automatic bend may change side, but only by passing through a straight arm (no jump of the elbow offset)
                        dj = max(abs(sides[i] - sides[i - 1]) for i in range(1, len(sides)))
                        check(dj <= 0.08, "%s %s circle r=%.2f auto bend: elbow offset jumps %.4f D" % (cast, key, rad, dj))
                # straight lines through the shoulder, from far left to far right and from far above to far below
                for (ax, ay) in ((1.0, 0.0), (0.0, 1.0), (0.7, 0.7), (0.7, -0.7)):
                    figs = []
                    n = 300
                    for i in range(n + 1):
                        s = lerp(-1.5, 1.5, i / float(n))
                        spec = {"hand": (S[0] + ax * s, S[1] + ay * s)}
                        if bend is not None:
                            spec["bend"] = bend
                        f = draw(cast, {key: spec}, "%s %s line" % (cast, key))
                        if f:
                            figs.append(f)
                    d, k, i = max_step(figs)
                    check(d <= 0.06, "%s %s line (%.1f, %.1f) through the shoulder, bend=%s: anchor %s jumps %.4f D at s = %.3f"
                          % (cast, key, ax, ay, bend, k, d, lerp(-1.5, 1.5, i / float(n))))
            # targets given through presets with stretch
            for st in (0.5, 1.0, 1.3):
                f = draw(cast, {key: {"hand": (sgn * 9.0, -9.0), "stretch": st}}, "%s %s far target stretch %.1f" % (cast, key, st))
                if f:
                    A = f["anchors"]
                    reach = math.hypot(A["hand_" + q][0] - A["shoulder_" + q][0], A["hand_" + q][1] - A["shoulder_" + q][1])
                    check(abs(reach - L * st) < 1e-6, "%s %s far target: reach %.4f, expected arm length %.4f" % (cast, key, reach, L * st))
    return COUNT[0] - n0


def test_leg_targets():
    n0 = COUNT[0]
    for cast in CASTS:
        C = puppet.CAST[cast]
        L = C["leg"]
        base = puppet.figure(cast, {}, "t")["anchors"]
        for q, sgn in (("r", 1), ("l", -1)):
            hip = (base["hip"][0] + sgn * C["hip_x"], base["hip"][1])
            for knee in ((None, 1.0) if QUICK[0] else (None, 1.0, -1.0)):
                for rad in ((0.05, 0.8, 50.0) if QUICK[0] else (0.05, 0.3, 0.8, L, 2.0, 50.0)):
                    figs, sides = [], []
                    for i in range(181):
                        a = 2 * math.pi * i / 180
                        lg = {"preset": "stand", "foot_" + q: (hip[0] + rad * math.cos(a), hip[1] + rad * math.sin(a))}
                        if knee is not None:
                            lg["knee_" + q] = knee
                        f = draw(cast, {"legs": lg}, "%s foot_%s circle r=%.2f" % (cast, q, rad))
                        if not f:
                            continue
                        A = f["anchors"]
                        figs.append(f)
                        sides.append(side_of(hip, A["knee_" + q], A["foot_" + q]))
                        reach = math.hypot(A["foot_" + q][0] - hip[0], A["foot_" + q][1] - hip[1])
                        check(reach <= L + 1e-6, "%s foot_%s r=%.2f: foot %.3f D from the hip, leg is %.2f" % (cast, q, rad, reach, L))
                    d, k, i = max_step(figs)
                    check(d <= 0.16, "%s foot_%s circle r=%.2f knee=%s: anchor %s jumps %.4f D at step %d (2 deg steps)" % (cast, q, rad, knee, k, d, i))
                    if knee is not None:
                        pos = [s for s in sides if s > 2.5e-2]      # the baked 0.012 D bow of a straight leg is not a bend
                        neg = [s for s in sides if s < -2.5e-2]
                        check(not (pos and neg), "%s foot_%s circle r=%.2f knee=%s: knee flips side" % (cast, q, rad, knee))
    return COUNT[0] - n0


def test_garbage():
    n0 = COUNT[0]
    nan, inf = float("nan"), float("inf")
    junk = [None, nan, inf, -inf, "x", "", [], {}, (), (nan, nan), (inf, -inf), [1], "0.5", True, 1e308, -1e308, object()]
    keys = ["yaw", "pitch", "head_roll", "head_dx", "head_dy", "lean", "squash", "expr", "mouth", "blink", "gaze", "arm_r", "arm_l",
            "legs", "prop_r", "prop_l", "fx", "t", "tint", "ink", "limb_w", "mirror", "nonsense"]
    for cast in CASTS:
        for key in keys:
            for j in junk:
                draw(cast, {key: j}, "%s garbage %s=%r" % (cast, key, j))
        for sub in ("hand", "bend", "sharp", "stretch", "layer", "shape", "preset"):
            for j in junk:
                draw(cast, {"arm_r": {sub: j}, "arm_l": {"hand": (0.3, 0.3), sub: j}}, "%s garbage arm.%s=%r" % (cast, sub, j))
        for sub in ("preset", "spread", "stride", "crouch", "lift_r", "lift_l", "foot_r", "foot_l", "knee_r", "knee_l", "toe_r", "toe_l", "rigid"):
            for j in junk:
                draw(cast, {"legs": {sub: j}}, "%s garbage legs.%s=%r" % (cast, sub, j))
        for sub in ("type", "angle", "twist", "scale"):
            for j in junk:
                draw(cast, {"arm_r": "forward", "prop_r": {"type": "pencil", sub: j}}, "%s garbage prop.%s=%r" % (cast, sub, j))
        for sub in ("type", "level", "t", "seed", "n", "side", "scale"):
            for j in junk:
                for fxn in puppet.FX_TYPES:
                    draw(cast, {"fx": [{"type": fxn, sub: j}]}, "%s garbage fx %s.%s=%r" % (cast, fxn, sub, j))
        draw(cast, {"fx": [None, 3, ("steam", nan), ("zzz",), {"type": None}]}, "%s garbage fx list" % cast)
        for junk_pose in (None, [], "x", 3, (1, 2)):
            draw(cast, junk_pose, "%s pose = %r" % (cast, junk_pose))
            try:
                puppet.resolve_pose(cast, junk_pose)
                puppet.lerp_pose(cast, junk_pose, {"yaw": 1}, 0.5)
                check(True, "")
            except Exception as e:      # noqa: BLE001
                check(False, "%s resolve/lerp with pose %r: %s" % (cast, junk_pose, e))
        draw(cast, {"arm_r": {"hand": (1e300, -1e300)}, "legs": {"foot_r": (1e300, 1e300), "foot_l": (nan, 0)}}, "%s huge targets" % cast)
        # hand / foot exactly on the joint root (the documented singular spot must still draw)
        A = puppet.figure(cast, {}, "t")["anchors"]
        draw(cast, {"arm_r": {"hand": A["shoulder_r"]}, "arm_l": {"hand": A["shoulder_l"]},
                    "legs": {"foot_r": (A["hip"][0] + puppet.CAST[cast]["hip_x"], A["hip"][1])}}, "%s targets on the joint roots" % cast)
    try:
        puppet.figure("nobody", {})
        check(False, "unknown cast name did not raise KeyError")
    except KeyError:
        check(True, "")
    # pose dict must not be modified by the call
    p = {"yaw": 0.3, "arm_r": {"hand": (0.5, 0.2)}, "fx": ["sweat"], "legs": {"preset": "wide"}}
    before = repr(p)
    puppet.figure("hero", p)
    puppet.resolve_pose("hero", p)
    check(repr(p) == before, "figure()/resolve_pose() modified the caller's pose dict")
    return COUNT[0] - n0


def test_fuzz(n=None, seed=1938):
    """random legal poses: no exception, no NaN, and neighbouring poses (tiny perturbation of every number) stay close."""
    n0 = COUNT[0]
    n = n or (300 if QUICK[0] else 1500)
    rnd = random.Random(seed)
    exprs = sorted(puppet.EXPRESSIONS)
    for it in range(n):
        cast = CASTS[it % 2]
        C = puppet.CAST[cast]
        arms = sorted(puppet.ARM_PRESETS[C["build"]])

        def arm():
            c = rnd.random()
            if c < 0.4:
                return rnd.choice(arms)
            d = {"hand": (rnd.uniform(-1.6, 1.6), rnd.uniform(-1.2, 2.2))}
            if rnd.random() < 0.5:
                d["bend"] = rnd.uniform(-1, 1)
            if rnd.random() < 0.3:
                d["stretch"] = rnd.uniform(0.5, 1.3)
            return d
        pose = dict(yaw=rnd.uniform(-1.2, 1.2), pitch=rnd.uniform(-1.5, 1.5), head_roll=rnd.uniform(-40, 40), head_dx=rnd.uniform(-0.3, 0.3),
                    head_dy=rnd.uniform(-0.3, 0.3), lean=rnd.uniform(-40, 40), squash=(rnd.uniform(0.7, 1.3), rnd.uniform(0.7, 1.3)),
                    expr=rnd.choice(exprs), blink=rnd.choice((0, 0, 0, 1, 2)), gaze=(rnd.uniform(-1, 1), rnd.uniform(-1, 1)),
                    arm_r=arm(), arm_l=arm(), legs=dict(preset=rnd.choice(sorted(puppet.LEG_PRESETS)), crouch=rnd.uniform(0, 0.6), stride=rnd.uniform(-1, 1)),
                    t=rnd.random(), mirror=rnd.random() < 0.3)
        if rnd.random() < 0.4:
            pose["prop_r"] = rnd.choice(puppet.PROP_TYPES)
        if rnd.random() < 0.4:
            pose["fx"] = rnd.sample(list(puppet.FX_TYPES), rnd.randint(1, 3))
        f = draw(cast, pose, "fuzz %d %s" % (it, cast))
        if not f:
            continue
        # neighbour: every top-level number nudged by 1e-3 of its range
        q = dict(pose)
        for key, rng in (("yaw", 2.4), ("pitch", 3.0), ("head_roll", 150.0), ("head_dx", 1.6), ("head_dy", 1.6), ("lean", 150.0)):
            q[key] = pose[key] + 1e-3 * rng * (1 if pose[key] < 0 else -1)
        g = draw(cast, q, "fuzz neighbour %d" % it)
        if g:
            d, k, _ = max_step([f, g])
            check(d <= 0.03, "fuzz %d %s: a 0.1 percent nudge moves anchor %s by %.4f D (pose %r)" % (it, cast, k, d, pose))
        bb, A = f["bbox"], f["anchors"]
        for k in ("hand_r", "hand_l", "foot_r", "foot_l", "head", "hat_top", "hip", "elbow_r", "elbow_l", "knee_r", "knee_l"):
            check(bb[0] - 0.02 <= A[k][0] <= bb[2] + 0.02 and bb[1] - 0.02 <= A[k][1] <= bb[3] + 0.02,
                  "fuzz %d %s: anchor %s %r outside bbox %r" % (it, cast, k, A[k], bb))
    return COUNT[0] - n0


def test_consistency():
    n0 = COUNT[0]
    for cast in CASTS:
        pose = {"yaw": 0.5, "lean": 6, "expr": "smug", "arm_r": "reach_up", "arm_l": "hip", "prop_r": "pencil", "legs": "step", "fx": ["sweat"]}
        a = puppet.figure(cast, pose, "u1")
        b = puppet.figure(cast, pose, "u1")
        check(a["svg"] == b["svg"], "%s: same input gives a different string" % cast)
        c = puppet.figure(cast, pose, "zz9")
        ids = re.findall(r'id="([^"]+)"', c["svg"])
        check(ids and all(i.startswith("zz9_") for i in ids), "%s: ids without the uid prefix: %r" % (cast, [i for i in ids if not i.startswith("zz9_")][:5]))
        check(len(ids) == len(set(ids)), "%s: duplicate ids inside one figure" % cast)
        refs = set(re.findall(r"url\(#([^)]+)\)", c["svg"])) | set(re.findall(r'href="#([^"]+)"', c["svg"]))
        check(refs <= set(ids), "%s: references to missing ids: %r" % (cast, sorted(refs - set(ids))[:5]))
        check("<svg" not in c["svg"], "%s: fragment contains an outer <svg>" % cast)
        check(c["svg"].count("<g") == c["svg"].count("</g>"), "%s: unbalanced <g>" % cast)
        # mirror: anchors x-negated with r/l swapped (the head disc itself is not mirrored, so skip the head-frame anchors)
        m = puppet.figure(cast, dict(pose, mirror=True), "m")
        for k, v in a["anchors"].items():
            if k in ("head_top", "head", "mouth", "eye_l", "eye_r", "hat_top"):
                continue
            k2 = k[:-2] + ("_l" if k.endswith("_r") else "_r") if k[-2:] in ("_r", "_l") else k
            w = m["anchors"][k2]
            check(abs(w[0] + v[0]) < 1e-9 and abs(w[1] - v[1]) < 1e-9, "%s mirror: anchor %s %r -> %s %r" % (cast, k, v, k2, w))
        # resolve_pose draws the same picture; lerp_pose reproduces its end points and is continuous in between
        r = puppet.figure(cast, puppet.resolve_pose(cast, pose), "u1")
        d, k, _ = max_step([a, r])
        check(d < 1e-6, "%s: resolve_pose moves anchor %s by %.6f" % (cast, k, d))
        p2 = {"yaw": -0.8, "lean": -10, "expr": "angry", "arm_r": "hip", "arm_l": "raised", "legs": "wide", "head_roll": 12}
        e0 = puppet.figure(cast, puppet.lerp_pose(cast, pose, p2, 0.0), "u1")
        e1 = puppet.figure(cast, puppet.lerp_pose(cast, pose, p2, 1.0), "u1")
        check(max_step([a, e0])[0] < 1e-6, "%s: lerp_pose(t=0) differs from pose a" % cast)
        check(max_step([puppet.figure(cast, p2, "u1"), e1])[0] < 1e-6, "%s: lerp_pose(t=1) differs from pose b" % cast)
        # (the prop itself switches at t = 0.5 by design, so the prop tip anchor is left out of this sweep)
        figs = [puppet.figure(cast, puppet.lerp_pose(cast, pose, p2, i / 60.0), "u1") for i in range(61)]
        for f in figs:
            f["anchors"] = dict((k, v) for k, v in f["anchors"].items() if not k.startswith("prop_tip"))
        d, k, i = max_step(figs)
        check(d <= 0.12, "%s: lerp_pose in 60 steps: anchor %s jumps %.4f D at step %d" % (cast, k, d, i))
        # place_svg / contact_shadow / hand_for_tip return usable fragments
        s = puppet.place_svg(a, 100.0, 200.0, 50.0) + puppet.contact_shadow(0.8, "cs1")
        check(_BAD.search(s) is None and s.count("<g") == s.count("</g>"), "%s: place_svg / contact_shadow fragment broken" % cast)
        hp = puppet.hand_for_tip("pencil", (0.75, 0.25), -48.0)      # a tip the arm can reach
        f = puppet.figure(cast, {"arm_r": {"hand": hp}, "prop_r": {"type": "pencil", "angle": -48.0}}, "u1")
        tip = f["anchors"]["prop_tip_r"]
        check(math.hypot(tip[0] - 0.75, tip[1] - 0.25) < 1e-3, "%s: hand_for_tip misses the tip by %.4f" % (cast, math.hypot(tip[0] - 0.75, tip[1] - 0.25)))
        # feet anchor: lowest drawn point of a standing figure is the sole line
        st = puppet.figure(cast, {}, "u1")
        check(abs(st["bbox"][3] - st["feet_y"]) < 0.05, "%s: bbox bottom %.3f vs feet_y %.3f" % (cast, st["bbox"][3], st["feet_y"]))
    return COUNT[0] - n0


def test_speed():
    n0 = COUNT[0]
    poses = [("hero", {}), ("boss", {}), puppet.STORY["hero_draw"], puppet.STORY["boss_rub"], puppet.STORY["hero_shock"],
             ("boss", {"expr": "furious", "fx": ["anger_fill", "steam", "sweat", "zzz", "tears", "blush", {"type": "focus_lines", "n": 80}],
                       "arm_r": "raised", "arm_l": "wave", "prop_r": "paper", "prop_l": "pointer", "legs": "crouch", "yaw": 0.7, "tint": "#fbdaf7"})]
    for cast, pose in poses:
        puppet.figure(cast, pose, "w")
    worst = 0.0
    for cast, pose in poses:
        best = 1e9
        for _ in range(5):                      # best of 5 batches: the machine is shared
            t0 = time.perf_counter()
            for i in range(40):
                puppet.figure(cast, dict(pose, t=i / 40.0), "s%d" % i)
            best = min(best, (time.perf_counter() - t0) / 40.0)
        worst = max(worst, best)
        check(best < 0.010, "figure(%s) takes %.2f ms per call (limit 10 ms)" % (cast, best * 1e3))
    print("    slowest pose: %.2f ms per call" % (worst * 1e3))
    return COUNT[0] - n0


# ----------------------------------------------------------------------------- 30-frame strip (visual pop check)
def strip_poses(n=30):
    a = {"yaw": -1.0, "arm_r": "down", "arm_l": "down", "expr": "neutral"}
    b = {"yaw": 1.0, "arm_r": "reach_up", "arm_l": "down", "expr": "neutral"}
    return [puppet.lerp_pose("hero", a, b, i / float(n - 1)) for i in range(n)]


def render_strip(out=None, n=30, D=150):
    import json
    import subprocess
    rv = os.path.join(HERE, "tmp", "rv")
    os.makedirs(rv, exist_ok=True)
    out = out or os.path.join(rv, "turn_strip.png")
    cw, ch = int(2.5 * D), int(4.0 * D)
    cols = 10
    rows = (n + cols - 1) // cols
    body = []
    poses = strip_poses(n)
    for i, p in enumerate(poses):
        f = puppet.figure("hero", p, "s%d" % i)
        x, y = (i % cols) * cw, (i // cols) * ch
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, cw, ch, "#a8663f" if (i + i // cols) % 2 == 0 else "#9c5d39"))
        body.append('<g transform="translate(%.1f %.1f) scale(%d)">%s</g>' % (x + cw * 0.42, y + ch - 0.28 * D - f["feet_y"] * D, D, f["svg"]))
        body.append('<text x="%d" y="%d" font-family="Arial" font-size="13" font-weight="700" fill="#fff">%02d  yaw %+.2f</text>' % (x + 6, y + 16, i, p["yaw"]))
    W, H = cols * cw, rows * ch
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>' % (W, H, W, H, "".join(body))
    sp = os.path.join(rv, "turn_strip.svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    jp = os.path.join(rv, "_strip_jobs.json")
    with open(jp, "w") as fh:
        json.dump([dict(svg=sp, out=out, w=W, h=H, bg="#a8663f")], fh)
    r = subprocess.run(["node", os.path.join(HERE, "raster_multi.js"), jp], cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    check(r.returncode == 0, "strip rasterisation failed: %s" % r.stdout[-300:])
    # pixel pop metric: mean absolute change between consecutive cells; a pop shows as one step far above its neighbours
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        print("    numpy / Pillow missing: strip rendered, pixel pop metric skipped")
        return out
    im = np.asarray(Image.open(out).convert("RGB")).astype(np.float32)
    cells = []
    for i in range(n):
        x, y = (i % cols) * cw, (i // cols) * ch
        c = im[y + 22:y + ch, x:x + cw].copy()
        if (i + i // cols) % 2 == 1:            # undo the checkerboard: map the darker cell colour to the lighter one
            m = (np.abs(c - np.array([0x9c, 0x5d, 0x39], dtype=np.float32)).sum(axis=2) < 6)
            c[m] = (0xa8, 0x66, 0x3f)
        cells.append(c)
    diffs = [float(np.abs(cells[i] - cells[i - 1]).mean()) for i in range(1, n)]
    med = sorted(diffs)[len(diffs) // 2]
    worst = max(range(len(diffs)), key=lambda i: diffs[i])
    print("    strip frame-to-frame change: median %.2f, max %.2f (frame %d -> %d), ratio %.2f" % (med, diffs[worst], worst, worst + 1, diffs[worst] / med))
    check(diffs[worst] <= 2.2 * med, "strip: frame %d -> %d changes %.2f, %.1f times the median %.2f (pop)" % (worst, worst + 1, diffs[worst], diffs[worst] / med, med))
    # anchors along the strip
    figs = [puppet.figure("hero", p, "s") for p in poses]
    d, k, i = max_step(figs)
    check(d <= 0.12, "strip: anchor %s jumps %.4f D between frames %d and %d" % (k, d, i - 1, i))
    return out


def main(argv):
    t0 = time.time()
    QUICK[0] = "--quick" in argv
    tests = [("presets, expressions, props, effects", test_presets), ("numeric key sweeps (40 and 240 steps)", test_numeric),
             ("arm targets: circles and lines through the shoulder", test_arm_targets), ("foot targets", test_leg_targets),
             ("garbage input", test_garbage), ("random poses", test_fuzz), ("determinism, ids, mirror, resolve / lerp", test_consistency),
             ("speed", test_speed)]
    for name, fn in tests:
        f0 = len(FAILS)
        n = fn()
        print("%-55s %6d checks  %s" % (name, n, "ok" if len(FAILS) == f0 else "%d FAILED" % (len(FAILS) - f0)))
    if "--strip" in argv:
        f0 = len(FAILS)
        out = render_strip()
        print("%-55s %s  -> %s" % ("30-frame turn strip", "ok" if len(FAILS) == f0 else "%d FAILED" % (len(FAILS) - f0), out))
    print("%d checks, %d failed, %.1f s" % (COUNT[0], len(FAILS), time.time() - t0))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
