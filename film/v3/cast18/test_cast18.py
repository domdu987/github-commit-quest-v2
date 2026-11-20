#!/usr/bin/env python3
"""test_cast18.py -- QA for cast18.py (film 18: Tian Dan's fire oxen).

    python3 test_cast18.py            sheet.jpg, canvas check, robustness run
    python3 test_cast18.py sheet      sheet.jpg only: heights / every STORY18 pose / faces / props / the ox (states, views, gallop, flame)
    python3 test_cast18.py canvas     sprite canvas check per member + head_flip + ox bbox check
    python3 test_cast18.py robust     pose-key garbage on the members, ox garbage, determinism, v2 test_puppet.py --quick
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast18  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast18.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
NIGHT, NIGHT2 = "#3a4258", "#464e66"
LINEUP = cast18.NEW18
LINEUP_POSE = {
    "tiandan": dict(expr="smirk", arm_r="down", arm_l="behind"),
    "general": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
    "yan_soldier_a": dict(expr="neutral"), "yan_soldier_b": dict(expr="happy"), "yan_soldier_c": dict(expr="grinning"),
    "old_man": dict(expr="neutral"), "woman": dict(expr="happy"), "child": dict(expr="happy"), "envoy": dict(expr="neutral"),
    "qi_soldier": cast18.qi_pose(0.3),
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
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def sec_heights(D=108):
    colw = int(2.4 * D)
    W = colw * len(LINEUP) + 20
    top = int(1.2 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    for i, c in enumerate(LINEUP):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            pp = dict(LINEUP_POSE[c], yaw=yw) if c != "qi_soldier" else dict(LINEUP_POSE[c])
            g, f = _fig(c, pp, "h%d%d" % (i, j), D, x0 + colw * (0.30 + 0.44 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 16))
    o.append(LABEL(10, 30, "cast18: front / 3-4, head D = %d px; head top to soles in D (qi_soldier = silhouette)" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=62, cols=12):
    names = list(cast18.STORY18)
    cw, ch = int(3.0 * D), int(5.9 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast18.STORY18[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        dark = cast == "qi_soldier"
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, (NIGHT if dark else (BG2 if (i + i // cols) % 2 else BG))))
        ground = y0 + ch - int(0.75 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.5 * D), x0, y0, cw, ch - int(0.5 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        meta = cast18.STORY18_META.get(n.rsplit("_", 1)[0] if n[-2:] in ("_a", "_b", "_c") else n, cast18.STORY18_META.get(n, {}))
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 16, "lip-sync", 11))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.18 * D), n, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cycles(D=62):
    rows = (("tiandan", "walk"), ("general", "run"), ("yan_soldier_a", "run"), ("yan_soldier_b", "run"), ("qi_soldier", "run"))
    ph = [i / 8.0 for i in range(8)]
    cw, ch = int(2.5 * D), int(4.2 * D)
    W, H = cw * 8, ch * len(rows)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, (c, mode) in enumerate(rows):
        for i, p in enumerate(ph):
            if c == "qi_soldier":
                pose = cast18.qi_pose(p)
            elif c == "general":
                pose = cast18.cycle(c, p, mode, 1, dict(expr="shocked", mouth=("open", 0.16, 0.18), hat_askew=24, prop_r="jue", fx=["sweat"]), "l")
                pose["arm_r"] = dict(hand=(0.70, 0.30), bend=0.9, sharp=0.6, stretch=1.0, layer="front")
            else:
                pose = cast18.cycle(c, p, mode, 1, dict(expr="shocked" if mode == "run" else "neutral"))
            x0, y0 = i * cw, r * ch
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, NIGHT if c == "qi_soldier" else (BG2 if (i + r) % 2 else BG)))
            g, f = _fig(c, pose, "c%d%d" % (r, i), D, x0 + cw * 0.5, y0 + ch - int(0.5 * D), shadow=0.8)
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">%s</svg>' % (x0, y0, cw, ch, x0, y0, cw, ch, g))
            o.append(_under(x0 + cw / 2, y0 + ch - 6, "%s %s %.3f" % (c, mode, p), 10))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
          ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing")), ("grinning", dict(expr="grinning")),
          ("smug", dict(expr="smug")), ("shouting", dict(expr="shouting", mouth=("open", 0.26, 0.17))), ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")),
          ("asleep", dict(expr="asleep")))


def sec_faces(D=84):
    cw, ch = int(1.4 * D), int(1.8 * D)
    members = [m for m in LINEUP if m != "qi_soldier"]
    W, H = 130 + cw * len(STATES), ch * len(members) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(members):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 13))
        for j, (lab, extra) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **extra), "f%d_%d" % (r, j))
            cx, cy = 130 + j * cw + cw / 2, y0 + ch * 0.50
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (130 + j * cw, y0, cw, ch - 22, 130 + j * cw, y0, cw, ch - 22, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 7, lab, 10))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=190):
    items = [("jue (bronze cup)", cast18_prop("jue", 0.0), 1.4, 0.4), ("spear", cast18_prop("spear", -90), 0.22, 0.0), ("torch + flame", cast18_prop("torch", -90), 0.5, 0.0),
             ("bamboo slips", cast18_prop("slips", -90), 0.9, 0.2), ("bronze pot", cast18_prop("bronze_pot", 0, ring=0.8), 0.9, -0.2), ("mallet", cast18_prop("mallet", 0), 0.9, 0.0),
             ("sash", cast18_prop("sash", 0), 0.9, -0.25), ("silk cloth", cast18_prop("silk", 0), 0.7, 0.0), ("blade", cast18_prop("blade", 0), 0.9, 0.0),
             ("pick", cast18_prop("pick", 0), 0.6, 0.0), ("basket", cast18_prop("basket", 0), 1.0, -0.3), ("banner (plain)", cast18_prop("banner", -90), 0.27, 0.9)]
    cw, ch = int(1.4 * D), int(1.5 * D)
    W, H = cw * 6, ch * 2
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, NIGHT)]
    for i, (lab, svg, sc, oy) in enumerate(items):
        x0, y0 = (i % 6) * cw, (i // 6) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, NIGHT2 if i % 2 else NIGHT))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 28, x0, y0, cw, ch - 28, x0 + cw / 2, y0 + ch * (0.48 + oy * 0.2), D * sc, svg))
        o.append(_under(x0 + cw / 2, y0 + ch - 9, lab, 14))
    return _svgdoc(W, H, "".join(o)), W, H


def cast18_prop(kind, ang, ring=0.0):
    """a prop alone: a held-hand-less puppet is not needed, draw the body in its own frame through the real _prop path."""
    k = P._Ctx("pp" + kind, P.INK, None)
    import cast8
    cast8._POSE8["an"] = {}
    cast8._POSE8["prop_i"] = 0
    cast8._POSE8["sides"] = ["r"]
    cast18._POSE18["pot"] = ring
    cast18._POSE18["fire"] = 1
    cast18._POSE18["t"] = 0.3
    cast18._POSE18["cup"] = 0.0
    svg, tip = cast18._prop(k, kind, (0.0, 0.0), ang, 1.0)
    return "<defs>%s</defs>%s" % ("".join(k.defs), svg)


def sec_ox(D=64):
    """states x views and the gallop cycle."""
    cw, ch = int(6.6 * D), int(5.4 * D)
    rows = []
    # row 1: stand / walk / startled, plain and dragon (side), 3/4
    cells = []
    for st in ("plain", "dragon"):
        for vw in ("side", "three_quarter"):
            cells.append((st, vw, "stand", 0.0, -1, True if st == "dragon" else False, "%s %s stand" % (st, vw.replace("three_quarter", "3/4"))))
    cells2 = []
    for st in ("plain", "dragon"):
        for vw in ("side", "three_quarter"):
            cells2.append((st, vw, "walk", 0.25, 0, True, "%s %s walk (lit)" % (st, vw.replace("three_quarter", "3/4"))))
    cells3 = [("dragon", "side", "startled", 0.0, -1, True, "dragon side startled"), ("dragon", "three_quarter", "startled", 0.0, -1, True, "dragon 3/4 startled"),
              ("plain", "side", "startled", 0.0, -1, False, "plain side startled"), ("plain", "three_quarter", "startled", 0.0, -1, False, "plain 3/4 startled")]
    cells4 = [("plain", "front_three_quarter", "stand", 0.0, -1, False, "plain front 3/4 stand"), ("dragon", "front_three_quarter", "stand", 0.0, 0, True, "dragon front 3/4 stand (lit)"),
              ("dragon", "front_three_quarter", "walk", 0.25, 1, True, "dragon front 3/4 walk (lit)"), ("dragon", "front_three_quarter", "startled", 0.0, 2, True, "dragon front 3/4 startled (lit)")]
    allrows = [cells, cells2, cells3, cells4]
    W = cw * 4
    H = ch * len(allrows) + 120
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, NIGHT)]
    r = 0
    for row in allrows:
        for i, (st, vw, g, ph, fl, bl, lab) in enumerate(row):
            x0, y0 = i * cw, r * ch
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, NIGHT2 if (i + r) % 2 else NIGHT))
            f = cast18.ox_figure(st, vw, g, ph, fl, bl, uid="ox%d_%d" % (r, i))
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%d)">%s</g></svg>'
                     % (x0, y0, cw, ch, x0, y0, cw, ch, x0 + cw * 0.58, y0 + ch * 0.84, D, f["svg"]))
            o.append(_under(x0 + cw / 2, y0 + ch - 8, lab + ("  blades" if bl else ""), 15))
        r += 1
    # gallop: 8 frames side plain/dragon and 3/4 plain/dragon, flame flicker 0,1,2,0...
    GD = 66
    cw2, ch2 = int(6.6 * GD), int(5.4 * GD)
    for (st, vw) in (("plain", "side"), ("dragon", "side"), ("dragon", "three_quarter"), ("plain", "three_quarter")):
        pass
    sub = []
    for fc_ in (None, "rage"):          # face=None: the original friendly face; "rage": the s21 / s22 reveal face
        for (st, vw) in (("dragon", "side"), ("dragon", "three_quarter"), ("dragon", "front_three_quarter")):
            for i in range(8):
                sub.append((st, vw, i, fc_))
    for vw in ("side", "three_quarter", "front_three_quarter"):       # face="panic" on the plain ox
        for i in range(4):
            sub.append(("plain", vw, i * 2, "panic"))
    o2 = []
    sw_ = cw2 * 4
    sh_ = ch2 * ((len(sub) + 3) // 4)
    body = ['<rect width="%d" height="%d" fill="%s"/>' % (sw_, sh_, NIGHT)]
    for n, (st, vw, i, fc_) in enumerate(sub):
        x0, y0 = (n % 4) * cw2, (n // 4) * ch2
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw2, ch2, NIGHT2 if (n + n // 4) % 2 else NIGHT))
        f = cast18.ox_figure(st, vw, "gallop", i / 8.0, i % 3 if st == "dragon" else -1, True, uid="g%d" % n, face=fc_)
        body.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%d)">%s</g></svg>'
                    % (x0, y0, cw2, ch2, x0, y0, cw2, ch2, x0 + cw2 * 0.58, y0 + ch2 * 0.84, GD, f["svg"]))
        body.append(_under(x0 + cw2 / 2, y0 + ch2 - 8, "%s %s gallop %d/8 %s" % (st, vw.replace("three_quarter", "3/4"), i, fc_ or "default"), 13))
    # flame cards
    fl = []
    for i in range(3):
        s, bb = cast18.flame_svg("fc%d" % i, i, 1.0)
        fl.append((i, s))
    return (_svgdoc(W, H - 120, "".join(o)), W, H - 120), (_svgdoc(sw_, sh_, "".join(body)), sw_, sh_), fl


def sec_flames(D=220):
    cw, ch = int(1.7 * D), int(1.9 * D)
    items = []
    for i in range(3):
        items.append(("flame %d (lit)" % i, i, 0.0))
    items.append(("flame 1 leaning (gallop)", 1, 0.45))
    W, H = cw * 4 + cw, ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, NIGHT)]
    for i, (lab, fr, lean) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, NIGHT2 if i % 2 else NIGHT))
        s, bb = cast18.flame_svg("fs%d" % i, fr, 1.0, lean)
        o.append('<g transform="translate(%.1f %.1f) scale(%d)">%s</g>' % (x0 + cw / 2, ch * 0.80, D, s))
        o.append(_under(x0 + cw / 2, ch - 10, lab, 14))
    # the lit / off tail card, sized as a flat card
    x0 = 4 * cw
    o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, NIGHT))
    o.append(LABEL(x0 + 10, 36, "flame colours: core #fffeec", 14))
    o.append(LABEL(x0 + 10, 60, "mid #ffb238, edge #e8561c", 14))
    o.append(LABEL(x0 + 10, 84, "never pure yellow", 14))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("poses", sec_poses), ("cycles", sec_cycles), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    a, b, fl = sec_ox()
    parts.append(_write(a[0], a[1], a[2], "sec_ox_a"))
    parts.append(_write(b[0], b[1], b[2], "sec_ox_b"))
    svg, w, h = sec_flames()
    parts.append(_write(svg, w, h, "sec_flames"))
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
    out.save(p, quality=86)
    print("wrote %s (%dx%d) in %.1f s" % (p, W, H, time.time() - t0))
    # also keep the sections separately for close inspection
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
        for pr in (None, "jue", "bronze_pot", "sash", "basket"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep"), dict(yaw=1.2), dict(yaw=-1.2), dict(hat_askew=30), dict(hat_askew=-30)]
    poses += [p for (c, p) in cast18.STORY18.values() if c == name]
    for m in cast18.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast18.cycle(name, i / 16.0, m, facing=fc))
    if name == "qi_soldier":
        poses += [cast18.qi_pose(i / 16.0, fc) for i in range(16) for fc in (1, -1)]
    return poses


def _check(name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-14s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast18.NEW18:
        bad += _check(name, member_poses(name), cast18.CANVAS18[name])
    probs = 0
    for n, (c, p) in cast18.STORY18.items():
        a = P.figure(c, p, "a")
        q = dict(p, mirror=not p.get("mirror", False))
        b = P.figure(c, q, "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("head_flip: %d poses checked, %d problems" % (len(cast18.STORY18), probs))
    # the ox: bbox against the drawing (rendered extents are checked on the sheet); report the numbers
    for st in cast18.OX_STATES:
        for vw in cast18.OX_VIEWS:
            for g in cast18.OX_GAITS:
                for i in range(8):
                    f = cast18.ox_figure(st, vw, g, i / 8.0, i % 3, True)
                    assert all(map(math.isfinite, f["bbox"]))
    print("ox: 2 states x 3 views x 4 gaits x 8 phases finite; bbox (side, lit) %r" % (cast18.ox_figure("dragon", "side", "gallop", 0.1, 1, True)["bbox"],))
    return bad + probs


def robust():
    import random
    rnd = random.Random(18)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("hat_askew", "fire_frame", "pot_ring", "cup_tilt", "slips", "banner_side", "t", "squash", "mirror", "expr")
    t0 = time.time()
    for name in cast18.NEW18:
        for i in range(300):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast18.NEW_PROPS18)
            p["prop_l"] = rnd.choice((None,) + cast18.NEW_PROPS18)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    for i in range(200):
        try:
            f = cast18.ox_figure(rnd.choice(garbage + ("plain", "dragon")), rnd.choice(garbage + ("side", "three_quarter", "front_three_quarter")), rnd.choice(garbage + ("gallop", "walk")),
                                 rnd.choice(garbage + (0.3,)), rnd.choice(garbage + (0, 1, 2)), rnd.choice(garbage), facing=rnd.choice((1, -1, "x")), coat=rnd.choice(garbage + (0.5,)))
            assert all(map(math.isfinite, f["bbox"]))
            n += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            if fail < 8:
                print("OX FAIL", repr(e))
    a = P.figure("tiandan", cast18.STORY18["tiandan_tug_cloth"][1], "d")["svg"]
    b = P.figure("tiandan", cast18.STORY18["tiandan_tug_cloth"][1], "d")["svg"]
    det = a == b and cast18.ox_figure("dragon", "side", "gallop", 0.3, 1, True)["svg"] == cast18.ox_figure("dragon", "side", "gallop", 0.3, 1, True)["svg"]
    P.figure("general", dict(), "z")
    print("cast18 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast18.NEW18
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
