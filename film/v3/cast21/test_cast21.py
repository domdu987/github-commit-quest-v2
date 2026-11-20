#!/usr/bin/env python3
"""test_cast21.py -- QA for cast21.py (film 21: Stirling Bridge, 1297).

    python3 test_cast21.py            sheet.jpg, canvas check, robustness run
    python3 test_cast21.py sheet      sheet.jpg only (members on mid-green and teal, horses, riders, every pose, faces, props)
    python3 test_cast21.py canvas     sprite canvas check (pose ranges against cast21.CANVAS21) + mirror check
    python3 test_cast21.py robust     pose-key garbage + mouth rule + earlier casts still draw + v2 test_puppet.py --quick on the new members
    python3 test_cast21.py pose NAME [NAME..]   quick look: writes tmp/pose.png
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast21  # noqa: E402
import puppet as P  # noqa: E402

TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
GREEN, GREEN2, TEAL, TEAL2 = "#6f9a4e", "#648f46", "#2f7f8c", "#2a7480"
SWIM = ("swim21",)


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


def _under(x, y, text, size=13):
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="4" fill="#1e2a1c" opacity="0.88"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def _fig(cast, pose, uid, D, x, y, shadow=0.9):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = ""
    if shadow and not (isinstance(pose, dict) and pose.get("swim21") is not None):
        s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s", opacity=0.40))
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _is_water(cast, pose):
    return isinstance(pose, dict) and pose.get("swim21") is not None or cast == "helmet_float"


def _ground(o, x0, y0, w, h, ground, water, D):
    if water:
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, h, TEAL))
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.02 * D), w, h, TEAL2))
    else:
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, h, GREEN))
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.08 * D), w, h, GREEN2))


LINEUP = ("cressingham", "surrey", "knight_a", "knight_a_open", "knight_b", "knight_b_great", "footman_a", "footman_b", "wallace", "moray",
          "scot_a", "scot_b", "scot_c", "scot_horn")
LINEUP_POSE = {
    "cressingham": dict(expr="smug", mouth="smirk", pitch=-0.3, arm_r="akimbo", arm_l="akimbo", legs="wide"),
    "surrey": dict(expr="tired", pitch=0.3, arm_r="down", arm_l="down"),
    "wallace": dict(expr="neutral", mouth="flat", arm_r="down", arm_l="down", sheath21=1),
}


def sec_heights(D=76, water=False):
    members = LINEUP
    colw = int(2.8 * D)
    W = colw * len(members) + 20
    top = int(1.3 * D)
    ground = top + int(4.4 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, TEAL if water else GREEN)]
    o.append('<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.08 * D), W, H, TEAL2 if water else GREEN2))
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        pose = dict(LINEUP_POSE.get(c, dict(expr="neutral", mouth="flat", arm_r="down", arm_l="down")))
        f0 = P.figure(c, pose, "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(pose, yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground, shadow=0.9)
            o.append(g)
        yt = ground - hh * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.2" stroke-dasharray="6 4" opacity="0.7"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 5, "%.2f D" % hh, 11))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 13))
    o.append(LABEL(10, 26, "cast21 lineup (%s): front / 3-4, head D = %d px; head (hat) top to soles in D" % ("teal" if water else "mid-green", D), 15))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cards(D=62):
    """horse walk cycle (8 phases, three caparisons), riders on their horses, swimmers and floating helmets on teal."""
    items = []
    for i in range(8):
        items.append(("horse", dict(gait=i / 8.0, horse21=("red", "blue", "gold", "plain")[i % 4]), "walk %d/8" % i, False))
    for n, p in (("knight_a_mtd", dict(gait=0.1)), ("knight_b_mtd", dict(gait=0.4)), ("knight_a_open_mtd", dict(gait=0.7, horse21="gold")), ("knight_b_great_mtd", dict(gait=0.2, horse21="red", mirror=True)),
                 ("surrey_mtd", dict(gait=0.3)), ("moray_mtd", dict(gait=0.6, mode21="idle", t=0.3)), ("horse", dict(mode21="idle", t=0.3, horse21="blue", mirror=True)),
                 ("knight_a_mtd", dict(gait=0.0, expr="laughing", mouth="talk_b", fx=["tears"], yaw=0.7, pitch=-0.7, head_roll=-8))):
        items.append((n, p, n + (" mirror" if p.get("mirror") else ""), False))
    cw, ch = int(5.2 * D), int(5.3 * D)
    cols = 4
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
    for i, (n, p, lab, wat) in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        ground = y0 + ch - int(0.7 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, GREEN2 if i % 2 else GREEN))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - 24, x0, y0, cw, ch - 24))
        g, f = _fig(n, p, "c%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        o.append(_under(x0 + cw / 2, y0 + ch - 12, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=60, cols=10, names=None, water=False, title=None):
    names = names or list(cast21.STORY21)
    cw, ch = int(3.4 * D), int(6.3 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
    for i, n in enumerate(names):
        cast, pose = cast21.STORY21[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        wat = _is_water(cast, pose)
        ground = y0 + ch - int(1.0 * D)
        _ground(o, x0, y0, cw, ch, ground, wat, D)
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        g, f = _fig(cast, dict(pose, t=pose.get("t", 0.3)), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n.replace("_", " ")[:34], 11))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", None), ("smug", None), ("laughing", None), ("shocked", None), ("jawdrop", None), ("worried", None), ("sweat", None),
          ("tired", None), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)))


def sec_faces(D=84):
    cw, ch = int(1.5 * D), int(2.0 * D)
    members = LINEUP
    W, H = 160 + cw * len(STATES), ch * len(members) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
    for r, c in enumerate(members):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, GREEN2 if r % 2 else GREEN))
        o.append(LABEL(6, y0 + ch // 2, c, 13))
        for j, (lab, extra) in enumerate(STATES):
            pose = dict(yaw=0.3)
            if extra is None:
                pose = cast21.with_expr(pose, lab)
            else:
                pose.update(extra)
            f = P.figure(c, pose, "f%d_%d" % (r, j))
            cx, cy = 160 + j * cw + cw / 2, y0 + ch * 0.50
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (160 + j * cw, y0, cw, ch - 24, 160 + j * cw, y0, cw, ch - 24, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=190):
    S = cast21
    items = [("spear21 (point end)", '<g transform="translate(-1.30 0.20) rotate(-12)">%s</g>' % S.spear_svg("pa"), 0.5),
             ("shield21 ochre", S.shield_svg("pb", "ochre"), 0.9), ("shield21 red", S.shield_svg("pb2", "red"), 0.9), ("shield21 blue", S.shield_svg("pb3", "blue"), 0.9),
             ("horn21", '<g transform="translate(-0.45 0.15)">%s</g>' % S.horn_svg("pc"), 1.0),
             ("sword21", '<g transform="translate(-0.6 0.0) rotate(-14)">%s</g>' % S.sword_svg("pd"), 0.85),
             ("coin21", '<g transform="translate(-0.07 0.04)">%s</g>' % S.coin_svg("pe"), 4.0)]
    cw, ch = int(1.4 * D), int(1.4 * D)
    W, H = cw * len(items), ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
    for i, (lab, svg, sc) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, H, GREEN2 if i % 2 else GREEN))
        o.append('<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g>' % (x0 + cw / 2, ch * 0.45, D * sc, svg))
        o.append(_under(x0 + cw / 2, ch - 10, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cycles(D=70):
    """walk / run cycle frames: Scots run with the spear forward, footmen march, both facings."""
    rows = (("scot_a", "run", 1), ("scot_b", "run", -1), ("footman_a", "march", 1), ("footman_b", "walk", -1), ("wallace", "run", 1))
    cw, ch = int(3.2 * D), int(5.2 * D)
    cols = 8
    W, H = cw * cols, ch * len(rows)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREEN)]
    for r, (c, mode, fc) in enumerate(rows):
        ground = r * ch + ch - int(0.7 * D)
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.08 * D), W, ch, GREEN2))
        for i in range(cols):
            ph = i / float(cols)
            p = cast21.run_spear(c, ph, fc) if mode == "run" else cast21.walk_spear(c, ph, fc, mode)
            if c == "wallace":
                p = cast21.cycle(c, ph, "run", fc, base=dict(sheath21=0, expr="determined", mouth="flat", arm_r=dict(hand=(0.7, -0.4), bend=-0.6, stretch=1.3, layer="top"),
                                                             prop_r=dict(type="sword21", angle=-70)), arms="l")
            g, f = _fig(c, p, "y%d_%d" % (r, i), D, i * cw + cw * 0.5, ground)
            o.append(g)
        o.append(_under(cw / 2, r * ch + 18, "%s %s facing %+d (phase 0..7/8)" % (c, mode, fc), 12))
    return _svgdoc(W, H, "".join(o)), W, H


KEY_POSES = ("cressingham_neutral", "cressingham_smug_belt", "cressingham_counting", "cressingham_laughing", "cressingham_pointing", "cressingham_purse_slap",
             "cressingham_shocked", "cressingham_sweating", "surrey_standing", "surrey_tired", "surrey_shocked", "surrey_worried",
             "knight_a_stand", "knight_a_laughing", "knight_b_shocked", "knight_b_yawn", "knight_a_bump", "knight_b_great_tiptoe",
             "footman_a_stand", "footman_a_point_laugh", "footman_b_laughing", "footman_a_mime_hoe", "footman_b_worried", "footman_a_tiptoe",
             "wallace_calm", "wallace_eyebrow", "wallace_raise_sword", "wallace_stand_spear", "moray_stand_spear", "moray_spear_wall",
             "scot_a_fold_spear", "scot_b_chew_grass", "scot_c_scratch_nose", "scot_a_spear_wall", "scot_horn_blow", "scot_b_shield",
             "footman_b_jump_arms_up", "footman_a_jump_pinch_nose", "footman_a_jump_bomb", "footman_a_splutter", "footman_b_swim_bob", "footman_a_swim_splutter",
             "knight_a_swim_arms_up", "footman_b_swim_paddle")


def _sections(names_filter):
    return [n for n in cast21.STORY21 if cast21.STORY21[n][0] not in cast21.SPECIAL21 and names_filter(n)]


def _stack(parts, out, maxw=2400, quality=86):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    img = Image.new("RGB", (W, H), (40, 52, 36))
    y = 0
    for i in ims:
        img.paste(i, (0, y))
        y += i.height + 8
    if W > maxw:
        img = img.resize((maxw, int(H * maxw / W)), Image.LANCZOS)
    img.save(out, quality=quality)
    print("wrote %s (%dx%d)" % (out, img.width, img.height))


def build_sheet():
    """sheet.jpg: lineup (mid-green and teal), horses / riders / swim cards, cycles, props, the key poses, faces.
    sheet_all_poses.jpg: every STORY21 pose."""
    t0 = time.time()
    parts = []
    plan = (("heights", lambda: sec_heights(76, False)), ("heights_teal", lambda: sec_heights(76, True)), ("cards", sec_cards),
            ("cycles", sec_cycles), ("props", sec_props),
            ("poses_key", lambda: sec_poses(D=58, cols=8, names=list(KEY_POSES))), ("faces", sec_faces))
    for name, fn in plan:
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    _stack(parts, os.path.join(HERE, "sheet.jpg"), maxw=2300)
    allp = [n for n in _sections(lambda n: True)]
    parts = []
    for i in range(0, len(allp), 60):
        svg, w, h = sec_poses(D=50, cols=12, names=allp[i:i + 60])
        parts.append(_write(svg, w, h, "sec_all%d" % i))
    _stack(parts, os.path.join(HERE, "sheet_all_poses.jpg"), maxw=2300)
    print("sheets in %.1f s" % (time.time() - t0))


def look(names, out="pose.png", D=110):
    svg, w, h = sec_poses(D=D, cols=min(6, len(names)), names=names)
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
        for pr in (None,) + cast21.NEW_PROPS21:
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", puff21=1, stalk21=1, spit21=1, wet21=1), dict(yaw=1.2), dict(yaw=-1.2)]
    poses += [p for (c, p) in cast21.STORY21.values() if c == name and p.get("swim21") is None]
    poses += [dict(p, mirror=True) for (c, p) in cast21.STORY21.values() if c == name and p.get("swim21") is None]
    for m in cast21.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast21.cycle(name, i / 16.0, m, facing=fc, base=dict(prop_r=cast21.SPEAR21, arm_r=dict(hand=(0.6, 0.9)))))
    for i in range(16):
        poses.append(cast21.run_spear(name, i / 16.0, 1))
        poses.append(cast21.run_spear(name, i / 16.0, -1))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.30 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.31) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-14s %-6s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                         "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast21.NEW21:
        if "_v" in name:
            continue
        # the story poses, mirrored, the cycles and run_spear must fit (the sweep of every arm preset with every prop is reported but
        # is a worst case: a 4 D spear held at an odd arm angle can reach past the canvas)
        story = [dict()] + [p for (c, p) in cast21.STORY21.values() if c == name and p.get("swim21") is None]
        story += [dict(p, mirror=True) for p in story]
        story += [dict((k, v) for k, v in p.items() if k != "swim21") for (c, p) in cast21.STORY21.values() if c == name and p.get("swim21") is not None]
        for m in cast21.CYCLE_MODES:
            for i in range(16):
                for fc in (1, -1):
                    story.append(cast21.cycle(name, i / 16.0, m, facing=fc, base=dict(prop_r=cast21.SPEAR21, arm_r=dict(hand=(0.6, 0.9)))))
        for i in range(16):
            story += [cast21.run_spear(name, i / 16.0, 1), cast21.run_spear(name, i / 16.0, -1)]
        bad += _check("poses", name, story, cast21.CANVAS21[name])
        _check("sweep", name, member_poses(name), cast21.CANVAS21[name])
    # specials: horse / riders / helmets over their poses
    for name, c in cast21.CANVAS_SPECIAL21.items():
        poses = [dict(gait=i / 16.0, horse21=h, mode21=m, mirror=mi) for i in range(16) for h in ("red", "blue", "gold", "plain") for m in ("walk", "idle") for mi in (False, True)]
        poses += [dict(p, **{}) for (cc, p) in cast21.STORY21.values() if cc == name]
        poses += [dict(p, mirror=True) for (cc, p) in cast21.STORY21.values() if cc == name]
        if name == "helmet_float":
            poses = [dict(helm21=h, t=i / 8.0) for h in ("kettle", "bascinet", "great") for i in range(8)]
        x0, y0, x1, y1 = _range(name, poses)
        clipped = x0 < c[0] or y0 < c[1] or x1 > c[2] or y1 > c[3]
        print("%-18s range (%.3f, %.3f, %.3f, %.3f) canvas %r %s" % (name, x0, y0, x1, y1, c, "TOO SMALL" if clipped else "ok"))
        bad += clipped
    # swimmers: cropped cards fit the member canvas
    probs = 0
    for n, (c, p) in cast21.STORY21.items():
        if c in cast21.SPECIAL21:
            continue
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("mirror check: %d poses, %d problems" % (len(cast21.STORY21), probs))
    return bad + probs


def mouth_rule():
    """mouths move only when talking: every STORY21 pose has a closed mouth unless flagged open on purpose (laugh, shock, yawn, splutter);
    the Scots never open theirs."""
    bad = 0
    closed = ("flat", "smile", "smirk", "frown", "dash", "wavy", "clench", "default", None)
    for n, (c, p) in cast21.STORY21.items():
        m = p.get("mouth")
        meta = cast21.STORY21_META.get(n, {})
        if isinstance(m, tuple) or m in ("talk_a", "talk_b", "talk_o", "o"):
            if not meta.get("open_mouth"):
                print("MOUTH OPEN without flag:", n, m)
                bad += 1
            if c.startswith(("scot", "wallace", "moray")):
                print("SCOT MOUTH OPEN:", n, m)
                bad += 1
        elif m not in closed:
            print("odd mouth", n, m)
            bad += 1
    return bad


def robust():
    import random
    rnd = random.Random(21)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "red", "kettle")
    keys = ("puff21", "stalk21", "spit21", "wet21", "shield21", "sheath21", "swim21", "variant21", "gait", "mode21", "horse21", "helm21", "t", "squash", "mirror", "expr")
    t0 = time.time()
    names = list(cast21.NEW21) + list(cast21.SPECIAL21)
    for name in names:
        for i in range(250):
            p = {}
            for kk in keys:
                if rnd.random() < 0.4:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast21.NEW_PROPS21)
            p["prop_l"] = rnd.choice((None,) + cast21.NEW_PROPS21)
            p["arm_r"] = dict(hand=(rnd.uniform(-1.5, 1.5), rnd.uniform(-1, 1.5)), shape=rnd.choice(("ball", "point", "open", "zzz")))
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"])), f["bbox"]
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 6:
                    print("FAIL", name, p, repr(e))
    a = P.figure("knight_a_mtd", cast21.STORY21["knight_a_mounted"][1], "d")["svg"]
    b = P.figure("knight_a_mtd", cast21.STORY21["knight_a_mounted"][1], "d")["svg"]
    det = a == b
    for earlier in ("general", "inspector", "bertillon", "inspector17", "admiral", "guard1", "hero", "boss"):     # earlier casts still draw unchanged
        if earlier in P.CAST:
            P.figure(earlier, dict(), "z")
    import cast10
    ref = P.figure("admiral", dict(expr="smug", arm_r="akimbo"), "z")["svg"]
    same = ref == cast10.P.figure("admiral", dict(expr="smug", arm_r="akimbo"), "z")["svg"]
    mr = mouth_rule()
    print("cast21 pose keys + garbage: %d ok, %d failed, deterministic %s, mouth rule problems %d, earlier casts draw %s, %.1f s" % (n, fail, det, mr, "ok", time.time() - t0))
    sys.path.insert(0, os.path.join(cast21.PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast21.HUMANS21           # the 14 base members (the colour variants share their cast dicts)
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
