#!/usr/bin/env python3
"""test_cast10.py -- QA for cast10.py (film 10: the zebra painter, dazzle camouflage).

    python3 test_cast10.py            sheet.jpg (all sections stacked), canvas check, robustness run
    python3 test_cast10.py sheet      sheet.jpg only: heights (with film 9's lin + general for scale) / every STORY10 pose /
                                      expressions, mouths, blinks / props.  Labels sit under each image.
    python3 test_cast10.py canvas     sprite canvas check (pose range per member against cast10.CANVAS10) + head_flip
    python3 test_cast10.py robust     v2 test_puppet.py (--quick) on the new members + cast10 pose-key garbage
Section images are kept in tmp/ (sec_*.png).
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast10  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast10.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"         # neutral greys
LINEUP = cast10.NEW10
REF = ("lin", "general")                                  # film 9, for scale
LINEUP_POSE = {
    "painter10": dict(expr="neutral", prop_r=dict(type="bigbrush", angle=-84, scale=0.95), arm_r=dict(hand=(0.40, 0.42), bend=0.6, stretch=1.1)),
    "admiral": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
    "sailor_a": dict(expr="neutral"),
    "sailor_b": dict(expr="happy"),
    "sailor_c": dict(expr="grinning"),
    "uboat_captain": dict(expr="determined", arm_r="behind", arm_l="behind"),
    "lin": dict(expr="neutral"),
    "general": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
}


def _svgdoc(W, H, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, body)


def _write(svg, w, h, base):
    sp = os.path.join(TMP, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(TMP, base + ".png")
    P._raster(sp, out, w, h, 1)
    try:
        os.remove(sp)
    except OSError:
        pass
    return out


def _fig(cast, pose, uid, D, x, y, shadow=0.9):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _under(x, y, text, size=14):
    """a label under an image (dark pill, white text)."""
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def sec_heights(D=120):
    members = LINEUP + REF
    colw = int(2.6 * D)
    W = colw * len(members) + 20
    top = int(1.2 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    hs = []
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG, 1.0 if c not in REF else 0.6))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        hs.append(ht)
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 13))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c + ("  (film 9, scale ref)" if c in REF else ""), 17))
    o.append(LABEL(10, 30, "cast10: front / 3-4, head D = %d px; heads top to soles in D.  film 9 lin + general at right for scale" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=74, cols=8):
    names = list(cast10.STORY10)
    cw, ch = int(3.2 * D), int(6.4 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast10.STORY10[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        gx = x0 + cw * (0.40 if pose.get("periscope") else 0.46)
        if pose.get("plank"):
            g, f = _fig(cast, dict(pose, t=0.3, plank_rope=3.6), "p%d" % i, D, gx, ground - int(0.55 * D), shadow=0)
        else:
            g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, gx, ground)
        o.append(g + "</svg>")
        meta = cast10.STORY10_META.get(n, {})
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n, 13))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")),
          ("laughing", dict(expr="laughing")), ("grinning", dict(expr="grinning")), ("smug", dict(expr="smug")), ("angry", dict(expr="angry")),
          ("shouting", dict(expr="shouting")), ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")), ("squint", dict(expr="squint")),
          ("sheepish", dict(expr="worried", mouth="smirk", fx=["blush"])), ("paint spots", dict(expr="worried", paint_spots=1.0)))


def sec_faces(D=96):
    cw, ch = int(1.45 * D), int(2.0 * D)
    W, H = 150 + cw * len(STATES), ch * len(LINEUP) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(LINEUP):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 15))
        for j, (lab, extra) in enumerate(STATES):
            pose = dict(yaw=0.3, **extra)
            f = P.figure(c, pose, "f%d_%d" % (r, j))
            cx, cy = 150 + j * cw + cw / 2, y0 + ch * 0.47
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (150 + j * cw, y0, cw, ch - 26, 150 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=200):
    items = []
    items.append(("bigbrush (black)", '<g transform="translate(-0.25 0) rotate(-20)">%s</g>' % cast10.bigbrush_svg("pa"), 0.55))
    items.append(("bigbrush (white)", '<g transform="translate(-0.25 0) rotate(-20)">%s</g>' % cast10.bigbrush_svg("pb", col="white"), 0.55))
    items.append(("bigbrush (clean)", '<g transform="translate(-0.25 0) rotate(-20)">%s</g>' % cast10.bigbrush_svg("pc", paint=0.0), 0.55))
    items.append(("paint_bucket", '<g transform="translate(0 -0.25)">%s</g>' % cast10.paint_bucket_svg("pd"), 1.25))
    items.append(("binoculars", cast10.binoculars_svg("pe"), 1.6))
    s, bb = cast10.plank_svg("pf", w=2.4, rope=1.2)
    items.append(("plank (plank=1)", '<g transform="translate(0 0.45)">%s</g>' % s, 0.33))
    items.append(("periscope (periscope=1)", '<g transform="translate(0.15 0)">%s</g>' % cast10.periscope_svg("pg", top=-1.3, bottom=1.3, handle_y=0.25, eye=(-0.40, -0.35)), 0.40))
    cw, ch = int(1.3 * D), int(1.45 * D)
    W, H = cw * len(items), ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, svg, sc) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, BG2 if i % 2 else BG))
        o.append('<svg x="%d" y="0" width="%d" height="%d" viewBox="%d 0 %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, cw, ch - 30, x0, cw, ch - 30, x0 + cw / 2, ch * 0.45, D * sc, svg))
        o.append(_under(x0 + cw / 2, ch - 10, lab, 14))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("poses", sec_poses), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    out = Image.new("RGB", (W, H), (60, 58, 60))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    p = os.path.join(HERE, "sheet.jpg")
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
        for pr in (None, "paint_bucket", "binoculars"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", sweat=1.0, paint_spots=1.0),
              dict(yaw=1.2), dict(yaw=-1.2)]
    poses += [p for (c, p) in cast10.STORY10.values() if c == name and not p.get("plank") and not p.get("periscope")]
    for m in cast10.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast10.cycle(name, i / 16.0, m, facing=fc))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-14s %-6s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                         "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast10.NEW10:
        bad += _check("", name, member_poses(name), cast10.CANVAS10[name])
    for name, c in cast10.CANVAS10_PLANK.items():
        lp = [p for (cc, p) in cast10.STORY10.values() if cc == name and p.get("plank")]
        lp += [dict(p, mirror=True) for p in lp] + [dict(plank=1), dict(plank=1, yaw=-0.6)]
        bad += _check("PLANK", name, lp, c)
    for name, c in cast10.CANVAS10_SCOPE.items():
        lp = [p for (cc, p) in cast10.STORY10.values() if cc == name and p.get("periscope")]
        lp += [dict(p, mirror=True) for p in lp]
        bad += _check("SCOPE", name, lp, c)
    probs = 0
    for n, (c, p) in cast10.STORY10.items():
        a = P.figure(c, p, "a")
        q = dict(p, mirror=not p.get("mirror", False))
        b = P.figure(c, q, "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("head_flip: %d poses checked, %d problems" % (len(cast10.STORY10), probs))
    return bad + probs


def robust():
    import random
    rnd = random.Random(10)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("paint_spots", "brush_paint", "brush_col", "bucket_paint", "plank", "plank_w", "plank_rope", "periscope", "sweat", "t", "squash", "mirror", "expr")
    t0 = time.time()
    for name in cast10.NEW10:
        for i in range(400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast10.NEW_PROPS10)
            p["prop_l"] = rnd.choice((None,) + cast10.NEW_PROPS10)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("admiral", cast10.STORY10["admiral_plank_sheepish"][1], "d")["svg"]
    b = P.figure("admiral", cast10.STORY10["admiral_plank_sheepish"][1], "d")["svg"]
    det = a == b
    # earlier casts unchanged: lin / general still draw
    P.figure("general", dict(), "z")
    print("cast10 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast10.NEW10
    rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        canvas_check()
    if what in ("all", "robust"):
        robust()
