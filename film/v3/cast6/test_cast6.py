#!/usr/bin/env python3
"""test_cast6.py -- QA for cast6.py.

    python3 test_cast6.py            lineup.jpg (all sections stacked), canvas check, robustness run
    python3 test_cast6.py lineup     lineup.jpg only: heights / every STORY6 pose / walk + run cycles / mouths + blinks / props
    python3 test_cast6.py canvas     sprite canvas check (pose range per member against cast6.CANVAS6) + head_flip
    python3 test_cast6.py robust     v2 test_puppet.py (--quick) on the nine new members + cast6 pose-key garbage
Section images are kept in tmp/ (sec_*.png) for close inspection.
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast6  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast6.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
WALL, WALL2, GROUND = "#c99a6a", "#b98a5e", "#7a6250"     # warm market plaster / cobbles
LINEUP = cast6.NEW6
KIDS = ("kit",)
LINEUP_POSE = {
    "kit": dict(expr="happy", arm_l="akimbo"),
    "henry": dict(expr="smug", arm_r="akimbo", arm_l="akimbo"),
    "inspector": dict(expr="neutral"),
    "inspector_royal": dict(expr="determined", arm_l="akimbo"),
    "guard1": dict(expr="determined", arm_r=dict(hand=(0.42, 0.60), bend=0.4), prop_r=cast6.SPEAR),
    "guard2": dict(expr="determined", arm_r=dict(hand=(0.42, 0.60), bend=0.4), prop_r=cast6.SPEAR),
    "woman1": dict(expr="happy", arm_r="akimbo"),
    "man1": dict(expr="smirk", arm_l="akimbo"),
    "baker2": dict(expr="sad", pitch=0.4),
}


def _svgdoc(W, H, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, body)


def _write(svg, w, h, base):
    sp = os.path.join(TMP, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(TMP, base + ".png")
    rc = P._raster(sp, out, w, h, 1)
    return out


def _fig(cast, pose, uid, D, x, y, shadow=0.9):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def sec_heights(D=146):
    colw = int(2.7 * D)
    W = colw * len(LINEUP) + 20
    top = int(1.4 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.5 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, WALL), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    adults = []
    for i, c in enumerate(LINEUP):
        x0 = 10 + i * colw
        if i % 2:
            o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="0.7"/>' % (x0, colw, ground - int(0.12 * D), WALL2))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        if c not in KIDS:
            adults.append(ht)
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#fff4e0" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 13))
        o.append(LABEL(x0 + 8, 22, c, 19))
    mean = sum(adults) / len(adults)
    k = P.figure("kit", LINEUP_POSE["kit"], "m")
    nk = k["feet_y"] - k["anchors"]["head_top"][1]
    o.append(LABEL(10, 46, "front / 3-4, head D = %d px.  kit / mean adult = %.2f / %.2f = %.2f" % (D, nk, mean, nk / mean), 14))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=78, cols=10):
    names = list(cast6.STORY6)
    cw, ch = int(2.6 * D), int(5.6 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, WALL)]
    for i, n in enumerate(names):
        cast, pose = cast6.STORY6[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, WALL2 if (i + i // cols) % 2 else WALL))
        ground = y0 + ch - int(0.40 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, ch - (ground - int(0.10 * D) - y0), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch, x0, y0, cw, ch))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.48, ground)
        o.append(g + "</svg>")
        o.append(LABEL(x0 + 6, y0 + 18, n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cycles(D=78):
    phases = (0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875)
    modes = (("walk", 1), ("run", 1), ("walk", -1))
    cw = int(1.75 * D)
    rh = int(5.0 * D)
    W = 150 + cw * len(phases) * len(modes) + 20 * len(modes)
    H = rh * len(LINEUP)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, WALL)]
    for r, c in enumerate(LINEUP):
        y0 = r * rh
        ground = y0 + rh - int(0.35 * D)
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, rh, WALL2 if r % 2 else WALL))
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.08 * D), W, int(0.43 * D), GROUND))
        o.append(LABEL(6, y0 + 20, c, 15))
        x = 150
        for (m, fc) in modes:
            o.append(LABEL(x, y0 + 38, "%s %s" % (m, "->" if fc > 0 else "<-"), 12))
            base = {}
            if c == "inspector_royal" or c == "inspector":
                base = dict(expr="determined")
            for j, ph in enumerate(phases):
                p = cast6.cycle(c, ph, m, facing=fc, base=base)
                p["mouth"] = cast6.talk_mouth(j * 2, 0.8) if m == "run" else None
                g, f = _fig(c, p, "c%d%s%d%d" % (r, m, fc + 1, j), D, x + cw * (j + 0.5), ground, shadow=0.7)
                o.append(g)
            x += cw * len(phases) + 20
    return _svgdoc(W, H, "".join(o)), W, H


def sec_faces(D=110):
    states = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
              ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("angry", dict(expr="angry")),
              ("laughing", dict(expr="laughing")), ("shocked", dict(expr="shocked")), ("pale 1", dict(expr="worried", pale=1.0)))
    cw, ch = int(1.45 * D), int(1.75 * D)
    W, H = 140 + cw * len(states), ch * len(LINEUP) + 30
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, WALL)]
    for j, (lab, _) in enumerate(states):
        o.append(LABEL(140 + j * cw + 8, 20, lab, 14))
    for r, c in enumerate(LINEUP):
        y0 = 30 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, WALL2 if r % 2 else WALL))
        o.append(LABEL(6, y0 + 22, c, 15))
        for j, (lab, extra) in enumerate(states):
            pose = dict(yaw=0.3, **extra)
            f = P.figure(c, pose, "f%d_%d" % (r, j))
            cx, cy = 140 + j * cw + cw / 2, y0 + ch * 0.52
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (140 + j * cw, y0, cw, ch, 140 + j * cw, y0, cw, ch, cx, cy, D, f["svg"]))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=260):
    items = []
    items.append(("loaf", cast6.loaf_svg("pa"), 0.0, 1.0))
    s, an = cast6.basket_svg("pb", 12)
    items.append(("basket 12", s, -0.30, 0.6))
    s, an = cast6.basket_svg("pc", 13)
    items.append(("basket 13", s, -0.30, 0.6))
    s, an = cast6.basket_svg("pd", 6, tilt=-70, pour=0.35)
    items.append(("basket pour", s, -0.40, 0.6))
    items.append(("cabbage (rotten)", cast6.cabbage_svg("pe"), 0.0, 1.0))
    items.append(("cabbage (fresh)", cast6.cabbage_svg("pf", rotten=0.0), 0.0, 1.0))
    items.append(("tomato", cast6.tomato_svg("pg", r=0.12), 0.0, 1.0))
    items.append(("tomato splat", cast6.tomato_svg("ph", r=0.12, squash=1.0), 0.0, 1.0))
    items.append(("loaf pile 12", cast6.loaf_pile_svg("pi", 12), 0.25, 0.7))
    items.append(("loaf pile 13", cast6.loaf_pile_svg("pj", 13), 0.25, 0.7))
    s, an = cast6.pillory_svg("pk", post_h=1.2)
    items.append(("pillory (empty)", s, -0.75, 0.42))
    cw, ch = int(1.25 * D), int(1.35 * D)
    W, H = cw * len(items), ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, WALL)]
    for i, (lab, svg, dy, sc) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, WALL2 if i % 2 else WALL))
        o.append('<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g>' % (x0 + cw / 2, ch * 0.55 + dy * D * sc, D * sc, svg))
        o.append(LABEL(x0 + 6, 20, lab, 14))
    return _svgdoc(W, H, "".join(o)), W, H


def build_lineup():
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("poses", sec_poses), ("cycles", sec_cycles), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    out = Image.new("RGB", (W, H), (40, 30, 34))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    p = os.path.join(HERE, "lineup.jpg")
    out.save(p, quality=88)
    print("wrote %s (%dx%d) in %.1f s" % (p, W, H, time.time() - t0))
    return p


def _range(name, poses):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for p in poses:
        f = P.figure(name, p, "c")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        props = [None, "loaf", "basket", "cabbage", "tomato"] + ([cast6.SPEAR, dict(type="spear", angle=-70)] if name.startswith("guard") else [])
        for pr in props:
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6, basket=dict(loaves=13, tilt=-90, pour=0.6)))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15), basket=dict(loaves=13, tilt=90, pour=0.9)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", pale=1.0), dict(yaw=1.2),
              dict(yaw=-1.2), dict(pillory=True, arm_r=dict(hand=(0.56, 0.47)), arm_l=dict(hand=(-0.56, 0.47)))]
    for h in (0.0, 0.3, 0.6, 1.0):
        poses.append(dict(hood=h, yaw=0.6))
        poses.append(dict(hood=h, yaw=-0.6))
    poses += [p for (c, p) in cast6.STORY6.values() if c == name]
    for m in cast6.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast6.cycle(name, i / 16.0, m, facing=fc))
    return poses


def canvas_check(verbose=True):
    bad = 0
    sugg = {}
    for name in cast6.NEW6:
        x0, y0, x1, y1 = _range(name, member_poses(name))
        c = cast6.CANVAS6[name]
        clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
        bad += clipped
        hw = math.ceil(max(-x0, x1) * 16) / 16.0
        sugg[name] = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
        if verbose:
            print("%-16s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok"))
    if bad:
        print("suggested CANVAS6:")
        for n, v in sugg.items():
            print('    "%s": (%.4f, %.4f, %.4f, %.4f),' % ((n,) + v))
    # head_flip (sprites): every STORY6 pose drawn mirrored inside scale(-1 1) must have the same feet / anchors
    probs = 0
    for n, (c, p) in cast6.STORY6.items():
        a = P.figure(c, p, "a")
        q = dict(p, mirror=not p.get("mirror", False))
        b = P.figure(c, q, "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("head_flip: %d poses checked, %d problems" % (len(cast6.STORY6), probs))
    return bad + probs


def robust():
    import random
    rnd = random.Random(6)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True)
    keys = ("basket", "hood", "pale", "fingers_r", "fingers_l", "pillory", "t")
    t0 = time.time()
    for name in cast6.NEW6:
        for i in range(400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast6.NEW_PROPS6)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            p["mirror"] = rnd.random() < 0.3
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("kit", cast6.STORY6["kit_hold_loaf"][1], "d")["svg"]
    b = P.figure("kit", cast6.STORY6["kit_hold_loaf"][1], "d")["svg"]
    det = a == b
    print("cast6 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast6.NEW6
    rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "lineup"):
        build_lineup()
    if what in ("all", "canvas"):
        canvas_check()
    if what in ("all", "robust"):
        robust()
