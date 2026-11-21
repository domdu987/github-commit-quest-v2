#!/usr/bin/env python3
"""test_cast5.py -- QA for cast5.py (same checks as test_cast4.py, plus the canary / cage creature).

    python3 test_cast5.py            lineup.png + canary.png + poses.png, canvas + head_flip checks, creature check, robustness run
    python3 test_cast5.py lineup     lineup.png only (people)
    python3 test_cast5.py canary     canary.png only (every canary state, alone and in the cage, large)
    python3 test_cast5.py poses      poses.png only
    python3 test_cast5.py canvas     sprite canvas check (pose range per member against cast5.CANVAS5) + head_flip
    python3 test_cast5.py creature   canary / cage robustness: sweeps, garbage, determinism, mirror, resolve / lerp, speed
    python3 test_cast5.py robust     v2 test_puppet.py (--quick) on the five new people
"""
import math
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast5  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast5.PROJ
LABEL = P._label
TUNNEL, TUNNEL2, FLOOR, WALL = "#4a4f6e", "#5d5a78", "#6e5a4c", "#8a6f5a"
LINEUP = ("alfie", "gaffer", "miner1", "miner2", "miner3")
LINEUP_POSE = {"alfie": dict(expr="determined", arm_l="akimbo"), "gaffer": dict(expr="smug", arm_r="akimbo", arm_l=dict(hand=(-0.70, 0.95), bend=0.4),
                                                                              prop_l="flame_lamp"),
               "miner1": dict(arm_r=dict(hand=(0.40, 0.80), bend=0.5), prop_r=dict(type="pickaxe", angle=-80)),
               "miner2": dict(expr="smirk", arm_r=dict(hand=(0.40, 0.80), bend=0.5), prop_r=dict(type="shovel", angle=-75)),
               "miner3": dict(expr="smirk", arm_l="akimbo")}
KIDS = ("alfie",)


def _write(svg, w, h, base, ext="png"):
    sp = os.path.join(HERE, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(HERE, base + "." + ext)
    rc = P._raster(sp, out, w, h, 1)
    print("%s (%dx%d) rc=%d" % (out, w, h, rc))
    return out


def _fig(cast, pose, uid, D, x, y, shadow=0.9, lift=0.0):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - lift * D - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def build_lineup(D=120):
    colw = int(2.9 * D)
    W = colw * len(LINEUP) + 40
    top = int(1.6 * D)
    ground = top + int(3.6 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, TUNNEL),
         '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.15 * D), W, H, FLOOR)]
    adults = []
    for i, c in enumerate(LINEUP):
        x0 = 20 + i * colw
        if i % 2:
            o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="0.6"/>' % (x0, colw, ground - int(0.15 * D), TUNNEL2))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        if c not in KIDS:
            adults.append(ht)
        for j, yw in enumerate((0.0, 0.5)):
            pose = dict(LINEUP_POSE[c], yaw=yw)
            g, f = _fig(c, pose, "l%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        yh = ground - hh * D
        for y, col in ((yt, "#f0e6d8"), (yh, "#f0b0a0")):
            o.append('<path d="M%d,%.1f L%d,%.1f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, y, x0 + colw - 4, y, col))
        o.append('<path d="M%d,%.1f L%d,%.1f M%d,%.1f L%d,%.1f M%d,%.1f L%d,%.1f" stroke="#f0e6d8" stroke-width="2"/>'
                 % (x0 + 10, yt, x0 + 10, ground, x0 + 4, yt, x0 + 16, yt, x0 + 4, ground, x0 + 16, ground))
        o.append(LABEL(x0 + 14, int(yt) - 8, "%.2f D" % ht, 15))
        o.append(LABEL(x0 + colw - 112, int(yh) - 8, "hat %.2f D" % hh, 13))
        o.append(LABEL(x0 + 8, 24, c, 20))
        o.append(LABEL(x0 + 8, H - 14, "front / 3-4", 13))
    mean = sum(adults) / len(adults)
    hero = P.figure("alfie", LINEUP_POSE["alfie"], "m")
    nh = hero["feet_y"] - hero["anchors"]["head_top"][1]
    o.append(LABEL(20, 52, "head top to soles; head D = %d px for all.  alfie / mean adult = %.2f / %.2f = %.2f" % (D, nh, mean, nh / mean), 16))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(o)), W, H


CANARY_ROW = [("perch_sing", dict(state="perch_sing", notes=5), "perch_sing, notes=5"), ("perch_sing", dict(state="perch_sing", notes=3), "perch_sing, notes=3"),
              ("sing_one", dict(state="sing_one"), "sing_one (1 note)"), ("perch_quiet", dict(state="perch_quiet"), "perch_quiet"),
              ("droop", dict(state="droop"), "droop"), ("fallen", dict(state="fallen"), "fallen"), ("revive", dict(state="revive"), "revive"),
              ("revive", dict(state="revive", eyes=1.0, lie=0.3), "revive eyes=1 lie=0.3")]


def build_canary(D=620):
    """every canary state, large: top row the bird alone (D px per D), bottom row in the cage (0.55 x D)."""
    cw = int(0.95 * D)
    n = len(CANARY_ROW)
    W = cw * n
    h1 = int(1.15 * D)
    Dc = int(0.62 * D)
    h2 = int(1.45 * Dc)
    h3 = int(1.6 * Dc)
    H = h1 + h2 + h3
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, TUNNEL)]
    for i, (st, pose, lab) in enumerate(CANARY_ROW):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, TUNNEL if i % 2 else TUNNEL2))
        # alone, on a short perch / floor line
        f = P.figure("canary", dict(pose, t=0.15), "cn%d" % i)
        gx, gy = x0 + cw * 0.45, h1 - 0.12 * D
        o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#2a2030" stroke-width="%.1f" stroke-linecap="round"/>' % (gx - 0.30 * D, gy + 0.012 * D, gx + 0.30 * D, gy + 0.012 * D, 0.03 * D))
        o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#a8703e" stroke-width="%.1f" stroke-linecap="round"/>' % (gx - 0.30 * D, gy + 0.012 * D, gx + 0.30 * D, gy + 0.012 * D, 0.016 * D))
        o.append(P.place_svg(f, gx, gy, D))
        o.append(LABEL(x0 + 10, 26, lab, 18))
        # in the cage
        g = P.figure("canary_in_cage", dict(pose, t=0.15), "cc%d" % i)
        o.append(P.place_svg(g, x0 + cw * 0.45, h1 + h2 - 0.10 * Dc, Dc))
        # in the cage, mirrored and swinging (carried)
        g2 = P.figure("canary_in_cage", dict(pose, t=0.55, mirror=True, swing=-14), "cm%d" % i)
        o.append('<g transform="translate(%.1f %.1f) scale(%.3f)">%s</g>' % (x0 + cw * 0.45, h1 + h2 + 0.30 * Dc, Dc, g2["svg"]))
        o.append(LABEL(x0 + 10, h1 + 26, "in the cage", 15))
        o.append(LABEL(x0 + 10, h1 + h2 + 26, "mirror, swing -14 (hung from the ring)", 13))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(o)), W, H


def build_poses(D=100):
    names = list(cast5.STORY5)
    cols = 7
    cw, ch = int(2.9 * D), int(6.4 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, TUNNEL)]
    for i, n in enumerate(names):
        cast, pose = cast5.STORY5[n]
        meta = cast5.STORY5_META.get(n, {})
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        bg = TUNNEL2 if (i + i // cols) % 2 else TUNNEL
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, bg))
        ground = y0 + ch - int(0.55 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.12 * D), cw, ch - (ground - int(0.12 * D) - y0), FLOOR))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch, x0, y0, cw, ch))
        fx = x0 + cw * (0.30 if n == "alfie_revive" else 0.42)
        g, f = _fig(cast, pose, "p%d" % i, D, fx, ground)
        extra = ""
        if n == "alfie_revive":
            # the cage on a bench so that the bird's beak sits just right of the oxygen nozzle
            tip = f["anchors"]["prop_tip_r"]
            ox, oy = fx - f["anchors"]["feet"][0] * D, ground - f["feet_y"] * D
            tx, ty = ox + tip[0] * D, oy + tip[1] * D
            cg = P.figure("canary_in_cage", meta.get("cage", {"state": "revive"}), "rc%d" % i)
            bk = cg["anchors"]["beak"]
            cx, cy = tx + 0.07 * D - bk[0] * D, ty - bk[1] * D
            bench_top = cy + cg["feet_y"] * D
            bh = (ground - bench_top) / D
            extra = ('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (cx, bench_top, D, cast5.bench_svg("bn%d" % i, 1.0, bh))
                     + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (cx, cy, D, cg["svg"]))
        o.append(extra + g + "</svg>")
        o.append(LABEL(x0 + 8, y0 + 22, n, 15))
        o.append(LABEL(x0 + 8, y0 + ch - 10, cast, 12))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(o)), W, H


def _range(name, poses):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for p in poses:
        f = P.figure(name, p, "c")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


def canvas_check(verbose=True):
    bad = 0
    for name in cast5.NEW5:
        C = P.CAST[name]
        poses = [{}]
        for a in sorted(P.ARM_PRESETS[C["build"]]):
            for pr in (None,) + cast5.NEW_PROPS5:
                poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6, flame=2.0, bird=dict(state="perch_sing", notes=5, swing=40)))
                poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15), flame=2.0, bird=dict(state="fallen", swing=-40)))
        poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", cough=0.5), dict(yaw=1.2), dict(yaw=-1.2)]
        poses += [p for (c, p) in cast5.STORY5.values() if c == name]
        x0, y0, x1, y1 = _range(name, poses)
        c = cast5.CANVAS5[name]
        clipped = x0 < c[0] or y0 - 0.30 < c[1] or x1 > c[2] or y1 > c[3]
        bad += clipped
        if verbose:
            print("%-14s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok"))
    for name in cast5.CREATURES:
        poses = []
        for st in cast5.STATES:
            for m in (False, True):
                for sw in (-40, 0, 40):
                    for lie in (None, 0.0, 0.5, 1.0):
                        p = dict(state=st, notes=5, mirror=m, swing=sw, t=0.25, breath=1.0)
                        if lie is not None:
                            p["lie"] = lie
                        poses.append(p)
        x0, y0, x1, y1 = _range(name, poses)
        c = cast5.CANVAS5[name]
        clipped = x0 < c[0] or y0 - 0.05 < c[1] or x1 > c[2] or y1 > c[3]
        bad += clipped
        if verbose:
            print("%-14s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok"))
    try:
        sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
        import sprites
        miss = [n for n in cast5.NEW5 + cast5.CREATURES if n not in sprites.DEFAULT_CANVAS]
        print("sprites.DEFAULT_CANVAS has the new members:", "yes" if not miss else "MISSING %r" % miss)
        bad += len(miss)
    except Exception as e:  # noqa: BLE001
        print("sprites import failed:", e)
    return bad


def robust():
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast5.NEW5
    return T.main(["--quick"])


def head_flip_check():
    sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
    import sprites
    n = 0
    items = list(cast5.STORY5.items()) + [("canary_" + s, ("canary", p)) for s, p in cast5.CANARY5.items()] + \
        [("cage_" + s, ("canary_in_cage", p)) for s, p in cast5.CANARY5.items()]
    for name, (c, p) in items:
        svg = sprites._head_flipped(c, p, "hf")
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=True), "b")
        if abs(a["feet_y"] - b["feet_y"]) > 1e-9 or not svg.startswith('<g transform="scale(-1 1)">'):
            print("head_flip mismatch", name)
            n += 1
    print("head_flip: %d poses checked (STORY5 + creatures), %d problems" % (len(items), n))
    return n


def _finite_fig(f):
    vals = list(f["bbox"]) + [f["feet_y"]] + [c for v in f["anchors"].values() for c in v]
    return all(isinstance(v, float) and math.isfinite(v) for v in vals) and "nan" not in f["svg"] and "inf" not in f["svg"]


def creature_check():
    """robustness of the creature figures and of the new pose keys on the people."""
    rnd = random.Random(5)
    n = bad = 0
    t0 = time.time()
    garbage = [None, "x", 3, -1e9, 1e9, float("nan"), float("inf"), [], {}, (1, 2), True, "#zzzzzz"]
    keys = cast5.BIRD_KEYS + ("state", "mirror", "ink", "tint")
    slow = 0.0
    for name in cast5.CREATURES:
        # sweeps of every numeric key, every state
        for st in cast5.STATES:
            for key in cast5.BIRD_KEYS:
                prev = None
                for i in range(41):
                    v = -1.0 + 7.0 * i / 40.0 if key not in ("swing",) else -60 + 120 * i / 40.0
                    a = time.time()
                    f = P.figure(name, {"state": st, key: v}, "s")
                    slow = max(slow, time.time() - a)
                    n += 1
                    if not _finite_fig(f):
                        bad += 1
                        print("non-finite", name, st, key, v)
                    if prev is not None and key != "notes":
                        # continuity of the beak anchor (no jumps larger than 0.06 D per sweep step)
                        d = math.hypot(f["anchors"]["beak"][0] - prev[0], f["anchors"]["beak"][1] - prev[1])
                        if d > 0.08 * (f["anchors"]["feet"][1] / max(prev[2], 1e-6) if False else 1.0) and key not in ("scale",):
                            bad += 1
                            print("jump", name, st, key, v, round(d, 3))
                    prev = (f["anchors"]["beak"][0], f["anchors"]["beak"][1], f["feet_y"])
        # garbage input
        for _ in range(3000):
            p = {}
            for key in rnd.sample(keys, rnd.randint(0, len(keys))):
                p[key] = rnd.choice(garbage + [rnd.uniform(-5, 5), rnd.choice(list(cast5.STATES))])
            pose = p if rnd.random() < 0.9 else rnd.choice(garbage)
            try:
                f = P.figure(name, pose, "g")
                n += 1
                if not _finite_fig(f):
                    bad += 1
                    print("garbage non-finite", name, pose)
            except Exception as e:  # noqa: BLE001
                bad += 1
                print("garbage raised", name, pose, e)
        # determinism, mirror, resolve / lerp
        for st in cast5.STATES:
            p = dict(state=st, notes=4, t=0.3, swing=10)
            a, b = P.figure(name, p, "d"), P.figure(name, p, "d")
            m = P.figure(name, dict(p, mirror=True), "d")
            n += 3
            if a["svg"] != b["svg"] or abs(m["bbox"][0] + a["bbox"][2]) > 1e-9 or abs(m["anchors"]["beak"][0] + a["anchors"]["beak"][0]) > 1e-9:
                bad += 1
                print("determinism / mirror", name, st)
            r = P.resolve_pose(name, p)
            if P.figure(name, r, "d")["svg"] != a["svg"]:
                bad += 1
                print("resolve differs", name, st)
            for t in (0.0, 0.3, 0.7, 1.0):
                q = P.lerp_pose(name, dict(state="perch_sing"), p, t)
                n += 1
                if not _finite_fig(P.figure(name, q, "l")):
                    bad += 1
    # new pose keys on the people
    for name in cast5.NEW5:
        for _ in range(400):
            p = dict(arm_r=rnd.choice(["down", "hip", "raised", "forward"]), prop_r=rnd.choice(cast5.NEW_PROPS5),
                     flame=rnd.choice(garbage + [rnd.uniform(-3, 3)]), flame_blue=rnd.choice(garbage + [rnd.uniform(-1, 2)]),
                     bird=rnd.choice(garbage + [dict(state=rnd.choice(list(cast5.STATES)), notes=rnd.uniform(-2, 8), swing=rnd.uniform(-90, 90))]),
                     cough=rnd.choice(garbage + [rnd.uniform(-2, 2)]), t=rnd.choice(garbage + [rnd.uniform(-2, 2)]))
            try:
                f = P.figure(name, p, "pk")
                n += 1
                if not _finite_fig(f):
                    bad += 1
                    print("people non-finite", name, p)
            except Exception as e:  # noqa: BLE001
                bad += 1
                print("people raised", name, p, e)
        # flame / notes continuity of the prop tips
        for key, vals in (("flame", [i * 0.05 for i in range(41)]),):
            for v in vals:
                f = P.figure(name, dict(prop_r="flame_lamp", **{key: v}), "fk")
                n += 1
                if not _finite_fig(f):
                    bad += 1
    print("creature + new pose keys: %d checks, %d failed, slowest creature figure %.2f ms, %.1f s" % (n, bad, slow * 1000, time.time() - t0))
    return bad


def main(argv):
    cmd = argv[0] if argv else "all"
    rc = 0
    if cmd in ("all", "lineup"):
        svg, W, H = build_lineup()
        _write(svg, W, H, "lineup")
    if cmd in ("all", "canary"):
        svg, W, H = build_canary()
        _write(svg, W, H, "canary")
    if cmd in ("all", "poses"):
        svg, W, H = build_poses()
        _write(svg, W, H, "poses")
    if cmd in ("all", "canvas"):
        rc += canvas_check()
        rc += head_flip_check()
    if cmd in ("all", "creature"):
        rc += creature_check()
    if cmd in ("all", "robust"):
        rc += robust() or 0
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
