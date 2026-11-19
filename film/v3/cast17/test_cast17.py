#!/usr/bin/env python3
"""test_cast17.py -- QA for cast17.py (film 17: Bertillon and the card index, Paris 1882-83).

    python3 test_cast17.py            sheet.jpg, canvas check, robustness run
    python3 test_cast17.py sheet      sheet.jpg only: full cast lineup (heights) / escort group / every STORY17 pose /
                                      the 7 expressions + mouth states per main character / props.  Labels sit under each image.
    python3 test_cast17.py canvas     sprite canvas check (pose range per member against cast17.CANVAS17) + mirror check
    python3 test_cast17.py robust     v2 test_puppet.py (--quick) on the new members + cast17 pose-key garbage + mouth rule
    python3 test_cast17.py pose NAME [NAME..]   quick look: writes tmp/pose.png
Section images are kept in tmp/.
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast17  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast17.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#c79b72", "#bd9068", "#8e6542"           # mid-warm: tan terracotta wall, a darker honey floor
LINEUP = cast17.NEW17
LINEUP_POSE = {
    "bertillon": dict(expr="neutral", mouth="flat", arm_r="down", arm_l="down"),
    "inspector17": dict(expr="smug", mouth="flat", pitch=-0.3, arm_r="akimbo", arm_l="akimbo", legs="wide"),
    "prefect": dict(expr="neutral", mouth="flat", pitch=-0.15, arm_r="behind", arm_l="behind"),
    "dupont": dict(expr="worried", mouth="flat", arm_r="down", arm_l="down"),
    "gendarme_a": dict(expr="neutral", mouth="flat", arm_r="behind", arm_l="behind"),
    "gendarme_b": dict(expr="neutral", mouth="flat", arm_r="behind", arm_l="behind"),
    "prisoner_a": dict(expr="sad", mouth="flat", pitch=0.15),
    "prisoner_b": dict(expr="unimpressed", mouth="flat"),
    "prisoner_c": dict(expr="worried", mouth="flat"),
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
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s", opacity=0.45)) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _under(x, y, text, size=14):
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="4" fill="#2e2018" opacity="0.88"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def sec_heights(D=88):
    members = LINEUP
    colw = int(2.25 * D)
    W = colw * len(members) + 20
    top = int(1.3 * D)
    ground = top + int(4.0 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4" opacity="0.8"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 15))
    o.append(LABEL(10, 30, "cast17 lineup: front / 3-4, head D = %d px; heads top to soles in D" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_group(D=170):
    """the escort group: gendarme_a + dupont held + gendarme_b (arms gripped), and the pair at the chair."""
    cw, ch = int(5.2 * D), int(5.4 * D)
    W, H = cw * 2, ch
    ground = ch - int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.10 * D), W, H, GROUND)]
    o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (cw, cw, ground - int(0.10 * D), BG2))
    sp = cast17.ESCORT_SPACING
    xs = (cw * 0.5 - sp * D, cw * 0.5, cw * 0.5 + sp * D)
    gd = cast17.STORY17["dupont_held"][1]
    ga = dict(cast17.STORY17["gendarme_escort_a"][1], mirror=False)
    gb = dict(cast17.STORY17["gendarme_escort_b"][1], mirror=True)
    for (cast, pose, x, nm) in (("gendarme_a", ga, xs[0], "ga"), ("dupont", gd, xs[1], "du"), ("gendarme_b", gb, xs[2], "gb")):
        g, f = _fig(cast, pose, "g" + nm, D, x, ground)
        o.append(g)
    o.append(_under(cw / 2, ground + int(0.6 * D), "escort: gendarme_a + dupont_held + gendarme_b (mirror=True)", 14))
    # the chair: inspector seated stiff, bertillon measuring his ear (screen-right ear) with the calipers
    ins = dict(cast17.STORY17["inspector_seated_stiff"][1])
    xi = cw + cw * 0.36
    g, fi = _fig("inspector17", ins, "ci", D, xi, ground)
    o.append(g)
    ear_w = (xi + (fi["anchors"]["head"][0] - fi["anchors"]["feet"][0] + 0.52) * D, ground - (fi["feet_y"] - fi["anchors"]["head"][1] - 0.10) * D)
    xb = cw + cw * 0.74
    bm = dict(cast17.STORY17["bertillon_measuring"][1], mirror=True, yaw=0.5)
    fb = P.figure("bertillon", bm, "t")
    tgt = ((ear_w[0] - xb) / D + fb["anchors"]["feet"][0], fb["feet_y"] - (ground - ear_w[1]) / D)
    bm = cast17.hand_for_anchor("bertillon", bm, "r", "calipers_l", tgt)
    g, f = _fig("bertillon", bm, "cb", D, xb, ground)
    o.append(g)
    o.append(_under(cw + cw / 2, ground + int(0.6 * D), "inspector_seated_stiff + bertillon_measuring (mirror=True, calipers on the ear)", 14))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=66, cols=8, names=None):
    names = names or list(cast17.STORY17)
    cw, ch = int(3.3 * D), int(6.6 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast17.STORY17[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", dict(expr="neutral")), ("smirk", dict(expr="smirk")), ("laugh", None), ("angry", None), ("surprised", None),
          ("worried", None), ("proud", None), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("closed", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)))


def sec_faces(D=88):
    cw, ch = int(1.45 * D), int(2.0 * D)
    members = LINEUP
    W, H = 150 + cw * len(STATES), ch * len(members) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(members):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 14))
        for j, (lab, extra) in enumerate(STATES):
            pose = dict(yaw=0.3)
            if extra is None:
                pose = cast17.with_expr(pose, lab)
            else:
                pose.update(extra)
            f = P.figure(c, pose, "f%d_%d" % (r, j))
            cx, cy = 150 + j * cw + cw / 2, y0 + ch * 0.47
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (150 + j * cw, y0, cw, ch - 26, 150 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=200):
    items = [("calipers", '<g transform="translate(-0.45 -0.12) rotate(-12)">%s</g>' % cast17.calipers_svg("pa"), 0.95),
             ("card (angle -90)", '<g transform="translate(0.0 0.30) rotate(-90)">%s</g>' % cast17.card_svg("pb"), 1.7),
             ("pen", '<g transform="translate(-0.15 0.15) rotate(-35)">%s</g>' % cast17.pen_svg("pc"), 1.9),
             ("ledger (angle -90)", '<g transform="translate(0.0 0.35) rotate(-90)">%s</g>' % cast17.ledger_svg("pd"), 1.5)]
    seats = []
    for seat, lab in (("chair", "seat17=chair"), ("bench", "seat17=bench")):
        c, pose = ("inspector17", cast17.STORY17["inspector_seated_stiff"][1]) if seat == "chair" else ("prisoner_a", cast17.STORY17["prisoner_sitting_a"][1])
        f = P.figure(c, pose, "sq")
        seats.append((lab, f["svg"], f["anchors"]["head"], 0.55))
    cw, ch = int(1.45 * D), int(1.5 * D)
    n = len(items) + len(seats)
    W, H = cw * n, ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, svg, sc) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, BG2 if i % 2 else BG))
        o.append('<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g>' % (x0 + cw / 2, ch * 0.45, D * sc, svg))
        o.append(_under(x0 + cw / 2, ch - 10, lab, 14))
    for j, (lab, svg, h, sc) in enumerate(seats):
        i = len(items) + j
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, BG2 if i % 2 else BG))
        o.append('<svg x="%d" y="0" width="%d" height="%d" viewBox="%d 0 %d %d"><g transform="translate(%.1f %.1f) scale(%.2f) translate(%.4f %.4f)">%s</g></svg>'
                 % (x0, cw, ch - 30, x0, cw, ch - 30, x0 + cw / 2, ch * 0.46, D * sc, -h[0], -h[1], svg))
        o.append(_under(x0 + cw / 2, ch - 10, lab, 14))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("group", sec_group), ("poses", sec_poses), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    out = Image.new("RGB", (W, H), (60, 44, 34))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    p = os.path.join(HERE, "sheet.jpg")
    out.save(p, quality=88)
    print("wrote %s (%dx%d) in %.1f s" % (p, W, H, time.time() - t0))
    return p


def look(names, out="pose.png", D=120):
    svg, w, h = sec_poses(D=D, cols=min(5, len(names)), names=names)
    p = _write(svg, w, h, os.path.splitext(out)[0])
    print(p)


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
        for pr in (None, "calipers", "card", "pen", "ledger"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", sweat=1.0, flush17=1.0),
              dict(yaw=1.2), dict(yaw=-1.2)]
    poses += [p for (c, p) in cast17.STORY17.values() if c == name]
    poses += [dict(p, mirror=True) for (c, p) in cast17.STORY17.values() if c == name]
    for m in cast17.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast17.cycle(name, i / 16.0, m, facing=fc))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.30 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.31) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-12s %-6s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                     "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast17.NEW17:
        bad += _check("", name, member_poses(name), cast17.CANVAS17[name])
    probs = 0
    for n, (c, p) in cast17.STORY17.items():
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("mirror check: %d poses, %d problems" % (len(cast17.STORY17), probs))
    return bad + probs


def mouth_rule():
    """mouths move only when talking: every STORY17 pose either has a closed mouth or is flagged open on purpose."""
    bad = 0
    closed = ("flat", "smile", "smirk", "frown", "dash", "wavy", "clench", "default", None)
    for n, (c, p) in cast17.STORY17.items():
        m = p.get("mouth")
        meta = cast17.STORY17_META.get(n, {})
        if isinstance(m, tuple) or m in ("talk_a", "talk_b", "talk_o", "o"):
            if not meta.get("open_mouth"):
                print("MOUTH OPEN without flag:", n, m)
                bad += 1
        elif m not in closed:
            print("odd mouth", n, m)
            bad += 1
    return bad


def robust():
    import random
    rnd = random.Random(17)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "chair", "bench")
    keys = ("seat17", "flush17", "seat_w", "sweat", "t", "squash", "mirror", "expr")
    t0 = time.time()
    for name in cast17.NEW17:
        for i in range(400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast17.NEW_PROPS17)
            p["prop_l"] = rnd.choice((None,) + cast17.NEW_PROPS17)
            p["arm_r"] = dict(hand=(rnd.uniform(-1.5, 1.5), rnd.uniform(-1, 1.5)), shape=rnd.choice(("ball", "point", "open", "three", "fist", "zzz")))
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("inspector17", cast17.STORY17["inspector_seated_stiff"][1], "d")["svg"]
    b = P.figure("inspector17", cast17.STORY17["inspector_seated_stiff"][1], "d")["svg"]
    det = a == b
    P.figure("general", dict(), "z")           # earlier casts still draw
    P.figure("inspector", dict(), "z")         # cast8's inspector is untouched
    mr = mouth_rule()
    print("cast17 pose keys + garbage: %d ok, %d failed, deterministic %s, mouth rule problems %d, %.1f s" % (n, fail, det, mr, time.time() - t0))
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast17.NEW17
    rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + mr + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what == "pose":
        look(sys.argv[2:])
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        canvas_check()
    if what in ("all", "robust"):
        robust()
