#!/usr/bin/env python3
"""test_cast25.py -- QA for cast25.py (film 25: Britain's first tank).

    python3 test_cast25.py            contact + canvas + identical + robust
    python3 test_cast25.py contact    contact.png: size line-up with a height ruler, walk strips, every STORY25 pose, faces, props
    python3 test_cast25.py canvas     canvas ranges per member and per special pose (suggestions printed; shipped ones checked) + head_flip
    python3 test_cast25.py identical  every earlier STORY pose / cycle draws byte-identical SVG with cast25 imported
    python3 test_cast25.py robust     pose-key garbage on the 13 members
"""
import hashlib
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast25  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast25.PROJ
SCRATCH = os.environ.get("CAST25_TMP", os.path.join(HERE, "tmp"))
TMP = SCRATCH
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
LINEUP = cast25.NEW25
REF = ("admiral", "yi24")
LINEUP_POSE = {n: dict(expr="neutral") for n in LINEUP}
LINEUP_POSE.update({"general25": dict(expr="smug", pitch=-0.2), "admiral": dict(expr="smug", pitch=-0.3), "yi24": dict(expr="neutral")})


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


def sec_heights(D=104):
    members = LINEUP + REF
    colw = int(2.05 * D)
    W = colw * len(members) + 70
    top = int(1.5 * D)
    ground = top + int(4.0 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    # height ruler on the left: a tick every 0.5 D, a long tick every 1 D (D = head diameter)
    for j in range(0, 9):
        y = ground - j * 0.5 * D
        L = 22 if j % 2 == 0 else 11
        o.append('<path d="M50,%.1f L%d,%.1f" stroke="#2e2a2c" stroke-width="2"/>' % (y, 50 - L, y))
        if j % 2 == 0:
            o.append('<text x="56" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="14" fill="#2e2a2c">%d D</text>' % (y + 5, j // 2))
    o.append('<path d="M50,%d L50,%.1f" stroke="#2e2a2c" stroke-width="2"/>' % (ground - 4 * D, ground))
    for i, c in enumerate(members):
        x0 = 70 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG, 1.0 if c not in REF else 0.6))
        for j in range(1, 8):
            o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1" opacity="0.35"/>' % (x0, ground - j * 0.5 * D, x0 + colw, ground - j * 0.5 * D))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        g, f = _fig(c, dict(LINEUP_POSE[c], yaw=0.0), "h%d" % i, D, x0 + colw * 0.5, ground)
        o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 14))
    o.append(LABEL(70, 30, "cast25 front line-up: head D = %d px, ruler in D (head diameters); heights head top to soles. admiral (film 10) and yi24 (film 24) at the right for scale" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_walk(D=50, n=6):
    """walk strips: 6 phases per member, two members side by side per row; then run strips for four members"""
    cw, ch = int(1.55 * D), int(4.5 * D)
    items = [(c, "walk") for c in LINEUP] + [(c, "run") for c in ("general25", "tommy_a25", "german_a25", "german_c25")]
    per = 2
    rows = [items[i:i + per] for i in range(0, len(items), per)]
    W = per * (cw * n + 70) + 40
    H = ch * len(rows)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, row in enumerate(rows):
        y0 = r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        ground = y0 + ch - int(0.45 * D)
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (ground - 2, W, int(0.15 * D), GROUND))
        for q, (c, mode) in enumerate(row):
            xo = q * (cw * n + 70)
            o.append(LABEL(xo + 6, y0 + ch // 2 - 6, c.replace("25", ""), 11))
            o.append(LABEL(xo + 6, y0 + ch // 2 + 10, mode, 11))
            for j in range(n):
                ph = j / float(n)
                pose = cast25.cycle(c, ph, mode, base=dict(expr="neutral"))
                g, f = _fig(c, pose, "w%d_%d_%d" % (r, q, j), D, xo + 70 + j * cw + cw / 2, ground)
                o.append(g)
    return _svgdoc(W, H, "".join(o)), W, H


WIDE = {"general25_march_flag": 1.3, "general25_laugh": 1.0}


def _pose_w(n, cw):
    if "helmet_on_stick" in n or "mg_crouch" in n or "mg_fire" in n or n.endswith("_push") or "blueprint" in n or "ladle" in n or "march_flag" in n or "run_away" in n:
        return 1.45
    return 1.0


def sec_poses(D=54, cols=17):
    names = list(cast25.STORY25)
    cw, ch = int(2.9 * D), int(6.2 * D)
    x = y = 0
    cells = []
    W = int(cw * cols)
    for n in names:
        w = int(cw * _pose_w(n, cw))
        if x + w > W:
            x, y = 0, y + ch
        cells.append((n, x, y, w))
        x += w
    H = y + ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (n, x0, y0, w) in enumerate(cells):
        cast, pose = cast25.STORY25[n]
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, ch, BG2 if i % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.04 * D), w, int(0.2 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, w, ch - int(0.6 * D), x0, y0, w, ch - int(0.6 * D)))
        gx = x0 + w * (0.40 if w > cw else 0.48)
        g, f = _fig(cast, dict(pose), "p%d" % i, D, gx, ground)
        o.append(g + "</svg>")
        meta = cast25.STORY25_META.get(n, {})
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        o.append('<path d="M%d,%d L%d,%d" stroke="#d02a2a" stroke-width="1" stroke-dasharray="4 3" opacity="0.7"/>' % (x0, ground, x0 + w, ground))
        o.append(_under(x0 + w / 2, y0 + ch - int(0.22 * D), n.replace("25", ""), 11))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")),
          ("laughing", dict(expr="laughing", fx=["tears"])), ("grinning", dict(expr="grinning")), ("smug", dict(expr="smug")), ("angry", dict(expr="angry")),
          ("shouting", dict(expr="shouting")), ("shocked", dict(expr="shocked", fx=["sweat"])), ("worried", dict(expr="worried", fx=["sweat"])),
          ("excited", dict(expr="excited")), ("sheepish", dict(expr="worried", mouth="smirk", fx=["blush"])), ("hat off", dict(hat_off25=1.0)))


def sec_faces(D=70):
    cw, ch = int(1.5 * D), int(1.9 * D)
    W, H = 150 + cw * len(STATES), ch * len(LINEUP) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(LINEUP):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 15))
        for j, (lab, extra) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **extra), "f%d_%d" % (r, j))
            cx, cy = 150 + j * cw + cw / 2, y0 + ch * 0.50
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (150 + j * cw, y0, cw, ch - 26, 150 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


PROPS = ("hammer25", "spanner25", "paint_brush25", "paint_pot25", "bucket25", "ladle25", "swagger25", "flag25", "helmet25", "helmet_stick25", "plan25", "mg25", "watering_can25", "shovel25", "tin_cup25", "toy_tank25", "chalkboard25")


def sec_props(D=100):
    cw, ch = int(3.0 * D), int(1.5 * D)
    cols = 6
    rows = (len(PROPS) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(PROPS):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        k = P._Ctx("pr%d" % i, P.INK, None)
        cast25._norm(P.CAST["general25"], dict(pour25=1.0 if n == "watering_can25" else 0.0, dirt25=1.0 if n == "shovel25" else 0.0, t=0.2))
        if n in cast25.UPRIGHT25 or n in cast25.HUNG25:
            body = cast25._upright_body(k, n)
            if n == "watering_can25":
                tl = cast25.CAN_TILT * 0.9
                rx, ry = cast25._rot(cast25.CAN_ROSE[0] + 0.05, cast25.CAN_ROSE[1], tl)
                body = '<g transform="rotate(%.2f)">%s</g>%s' % (tl, body, cast25._can_stream(k, rx, ry, 1.0, 0.2))
        else:
            cast25._POSE25["mg_drop"] = 0.52
            body = cast25._prop_body(k, n)
        sc = {"helmet_stick25": 0.55, "plan25": 0.9, "mg25": 1.0, "flag25": 1.1, "ladle25": 1.2, "swagger25": 1.2, "chalkboard25": 0.8, "shovel25": 0.9, "watering_can25": 0.7, "toy_tank25": 0.7}.get(n, 1.4)
        ln = {"plan25": -0.5, "helmet_stick25": 2.0, "bucket25": 0.0, "paint_pot25": 0.0, "helmet25": 0.0, "watering_can25": 0.6, "toy_tank25": 0.0, "chalkboard25": -0.8}.get(n, cast25.NEW_TIP25[n])
        defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
        yy = y0 + ch * (0.30 if n in cast25.UPRIGHT25 or n == "flag25" else (0.16 if n in cast25.HUNG25 else 0.42))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">%s<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch, x0, y0, cw, ch, defs, x0 + cw / 2 - (ln / 2) * D * sc, yy, D * sc, body))
        o.append(_under(x0 + cw / 2, y0 + ch - 8, n, 13))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet(out=None):
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("walk", sec_walk), ("poses", sec_poses), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    img = Image.new("RGB", (W, H), (60, 58, 60))
    y = 0
    for i in ims:
        img.paste(i, (0, y))
        y += i.height + 8
    p = out or os.path.join(HERE, "contact.png")
    img.save(p, optimize=True)
    for i, n in enumerate(("heights", "walk", "poses", "faces", "props")):
        parts_i = ims[i]
        parts_i.save(os.path.join(TMP, "part_%s.png" % n))
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


def _sugg(r):
    x0, y0, x1, y1 = r
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    return (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None, "hammer25", "swagger25"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep"), dict(yaw=1.2), dict(yaw=-1.2), dict(hat_up25=1.0), dict(hat_off25=1.0)]
    poses += [p for (n, (c, p)) in cast25.STORY25.items() if c == name and n not in cast25.SPECIAL25]
    for m in cast25.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast25.cycle(name, i / 16.0, m, facing=fc))
    for i in range(16):
        poses.append(cast25.run_away25(name, i / 16.0, 1, 1.0, 0.0))
        poses.append(cast25.run_away25(name, i / 16.0, -1, 1.0, 0.3))
    return poses


def canvas_check():
    bad = 0
    res = {}
    for name in LINEUP:
        r = _range(name, member_poses(name))
        res[name] = _sugg(r)
        print("%-12s range (%.3f, %.3f, %.3f, %.3f) -> canvas %r" % ((name,) + r + (res[name],)))
    spec = {}
    for n in cast25.SPECIAL25:
        c, p = cast25.STORY25[n]
        ps = [p, dict(p, mirror=True)]
        r = _range(c, ps)
        spec[n] = _sugg(r)
        print("%-30s range (%.3f, %.3f, %.3f, %.3f) -> canvas %r" % ((n,) + r + (spec[n],)))
    mg = 0
    for n, (c, p) in cast25.STORY25.items():
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                mg += 1
                print("  flip mismatch", n, key, va, vb)
    print("head_flip: %d poses checked, %d problems" % (len(cast25.STORY25), mg))
    for name, s in res.items():
        c = cast25.CANVAS25[name]
        if s[0] < c[0] - 1e-9 or s[1] < c[1] - 1e-9 or s[2] > c[2] + 1e-9 or s[3] > c[3] + 1e-9:
            print("CANVAS TOO SMALL for", name, c, "need", s)
            bad += 1
    for n, s in spec.items():
        c = cast25.CANVAS25_POSES.get(n)
        crop = n == "pilot25_lean_look"          # upper body only: the bottom is cut at the cockpit rim on purpose
        if c is None or s[0] < c[0] - 1e-9 or s[1] < c[1] - 1e-9 or s[2] > c[2] + 1e-9 or (s[3] > c[3] + 1e-9 and not crop):
            print("CANVAS TOO SMALL / MISSING for", n, c, "need", s)
            bad += 1
    # feet planted: feet anchor is on the sole line, both soles at feet_y, for every pose
    fl = 0
    for n, (c, p) in cast25.STORY25.items():
        f = P.figure(c, p, "a")
        an = f["anchors"]
        if abs(an["feet"][1] - f["feet_y"]) > 1e-6:
            fl += 1
            print("  feet anchor off the sole line:", n)
    print("feet planted: %d problems" % fl)
    print("canvas check:", "ok" if not bad else "%d too small" % bad)
    return bad + mg + fl


def _ref_hashes():
    out = {}
    for n, (c, p) in sorted(P.STORY.items()):
        out["story:" + n] = hashlib.md5(P.figure(c, p, "z")["svg"].encode()).hexdigest()
    import cast10
    import cast24
    for c in list(cast10.NEW10) + list(cast24.NEW24) + ["hero", "boss", "lin", "general", "kenta", "worker_a", "gunner_a", "tommy", "worker1", "foreman", "soldier"]:
        for m in ("walk", "run"):
            for i in range(0, 16, 3):
                out["cyc:%s:%s:%d" % (c, m, i)] = hashlib.md5(P.figure(c, cast10.cycle(c, i / 16.0, m), "z")["svg"].encode()).hexdigest()
    return out


def identical():
    """hashes the SVGs with cast24 only (a clean subprocess), then with cast25 imported (this process)"""
    ref_code = ("import sys, os, json, hashlib\nsys.path.insert(0, %r)\nimport cast24, cast10, puppet as P\n"
                "out = {}\n"
                "for n, (c, p) in sorted(P.STORY.items()):\n    out['story:' + n] = hashlib.md5(P.figure(c, p, 'z')['svg'].encode()).hexdigest()\n"
                "for c in list(cast10.NEW10) + list(cast24.NEW24) + ['hero', 'boss', 'lin', 'general', 'kenta', 'worker_a', 'gunner_a', 'tommy', 'worker1', 'foreman', 'soldier']:\n"
                "    for m in ('walk', 'run'):\n        for i in range(0, 16, 3):\n"
                "            out['cyc:%%s:%%s:%%d' %% (c, m, i)] = hashlib.md5(P.figure(c, cast10.cycle(c, i / 16.0, m), 'z')['svg'].encode()).hexdigest()\n"
                "print(json.dumps(out))\n" % os.path.join(PROJ, "v3", "cast24"))
    r = subprocess.run([sys.executable, "-I", "-c", ref_code], stdout=subprocess.PIPE, universal_newlines=True)
    ref = json.loads(r.stdout.strip().splitlines()[-1])
    now = _ref_hashes()
    diff = [k for k in ref if now.get(k) != ref[k]]
    extra = [k for k in now if k not in ref and not k.startswith("story:") or (k.startswith("story:") and k[6:] not in cast25.STORY25 and k not in ref)]
    print("earlier STORY / cycle SVGs byte-identical with cast25 imported: %d checked, %d differ %s" % (len(ref), len(diff), diff[:5]))
    return len(diff)


def robust():
    import random
    rnd = random.Random(25)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("hat_off25", "hat_up25", "mg_gy25", "paint_col25", "plan_w25", "pour25", "dirt25", "fire25", "glasses_dy25", "t", "squash", "mirror", "expr", "yaw", "lean")
    t0 = time.time()
    for name in LINEUP:
        for i in range(250):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast25.NEW_PROPS25)
            p["prop_l"] = rnd.choice((None,) + cast25.NEW_PROPS25)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("general25", cast25.STORY25["general25_march_flag"][1], "d")["svg"]
    b = P.figure("general25", cast25.STORY25["general25_march_flag"][1], "d")["svg"]
    print("cast25 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, a == b, time.time() - t0))
    return fail + (0 if a == b else 1)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "contact", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        canvas_check()
    if what in ("all", "identical"):
        identical()
    if what in ("all", "robust"):
        robust()
