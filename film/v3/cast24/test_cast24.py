#!/usr/bin/env python3
"""test_cast24.py -- QA for cast24.py (film 24: the turtle ship).

    python3 test_cast24.py            sheet + canvas + identical + robust
    python3 test_cast24.py sheet      sheet.jpg: size line-up / every STORY24 pose / faces / props
    python3 test_cast24.py canvas     canvas ranges per member and per special pose (kneel / crawl / plank) + head_flip
    python3 test_cast24.py identical  every earlier STORY pose draws byte-identical SVG with cast24 imported
    python3 test_cast24.py robust     pose-key garbage on the 10 members
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
import cast24  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast24.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
LINEUP = cast24.NEW24
REF = ("lin", "admiral")      # film 9 / film 10 members, for scale
LINEUP_POSE = {
    "yi24": dict(expr="neutral", arm_r="behind", arm_l="behind"),
    "jp_cmd24": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
    "lin": dict(expr="neutral"),
    "admiral": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
}
for _n in LINEUP:
    LINEUP_POSE.setdefault(_n, dict(expr="neutral"))


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


def sec_heights(D=100):
    members = LINEUP + REF
    colw = int(2.1 * D)
    W = colw * len(members) + 20
    top = int(1.5 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG, 1.0 if c not in REF else 0.6))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        g, f = _fig(c, dict(LINEUP_POSE[c], yaw=0.3), "h%d" % i, D, x0 + colw * 0.5, ground)
        o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 14))
    o.append(LABEL(10, 30, "cast24 size line-up: head D = %d px; heads top to soles in D. lin (film 9) and admiral (film 10) at the right for scale" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=62, cols=9):
    names = list(cast24.STORY24)
    wide = {"jp_cmd24_plank_cling": 2, "jp_cmd24_crawl_a": 2, "jp_cmd24_crawl_b": 2}
    cw, ch = int(3.0 * D), int(6.0 * D)
    # lay out with variable widths
    x = y = 0
    cells = []
    W = cw * cols
    for n in names:
        w = cw * wide.get(n, 1)
        if x + w > W:
            x, y = 0, y + ch
        cells.append((n, x, y, w))
        x += w
    H = y + ch
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (n, x0, y0, w) in enumerate(cells):
        cast, pose = cast24.STORY24[n]
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, w, ch, BG2 if i % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.04 * D), w, int(0.2 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, w, ch - int(0.6 * D), x0, y0, w, ch - int(0.6 * D)))
        gx = x0 + w * (0.42 if w > cw else 0.46)
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, gx, ground, shadow=0.0 if (pose.get("plank24") or pose.get("ground24") is not None) else 0.9)
        o.append(g + "</svg>")
        meta = cast24.STORY24_META.get(n, {})
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        if pose.get("ground24") is not None or pose.get("plank24"):
            o.append('<path d="M%d,%d L%d,%d" stroke="#d02a2a" stroke-width="1.2" stroke-dasharray="4 3"/>' % (x0, ground, x0 + w, ground))
        o.append(_under(x0 + w / 2, y0 + ch - int(0.22 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")),
          ("laughing", dict(expr="laughing")), ("grinning", dict(expr="grinning")), ("smug", dict(expr="smug")), ("angry", dict(expr="angry")),
          ("shouting", dict(expr="shouting")), ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")), ("squint", dict(expr="squint")),
          ("sheepish", dict(expr="worried", mouth="smirk", fx=["blush"])), ("wet", dict(expr="worried", wet24=1.0)))


def sec_faces(D=88):
    cw, ch = int(1.5 * D), int(2.0 * D)
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


PROPS = ("katana24", "yari24", "gunbai24", "ladder24", "spike24", "spike_bundle24", "hammer24", "mallet24", "rope24", "oar24")


def sec_props(D=100):
    cw, ch = int(3.0 * D), int(1.3 * D)
    cols = 5
    rows = (len(PROPS) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(PROPS):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        k = cast24._ctx("pr%d" % i, P.INK, "") if hasattr(cast24, "_ctx") else None
        k = P._Ctx("pr%d" % i, P.INK, None)
        body = cast24._prop_body(k, n)
        sc = {"yari24": 0.55, "ladder24": 0.7, "oar24": 0.62, "katana24": 0.9, "gunbai24": 1.0}.get(n, 1.6 if n in ("spike24", "spike_bundle24", "rope24") else 1.2)
        ln = cast24.NEW_TIP24[n]
        defs = "<defs>%s</defs>" % "".join(k.defs) if k.defs else ""
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">%s<g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch, x0, y0, cw, ch, defs, x0 + cw / 2 - (ln / 2 - 0.1) * D * sc, y0 + ch * 0.42, D * sc, body))
        o.append(_under(x0 + cw / 2, y0 + ch - 8, n, 13))
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


def _sugg(r):
    x0, y0, x1, y1 = r
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    return (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)


SPECIAL = ("plank", "ground24")


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None, "hammer24"):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", wet24=1.0), dict(yaw=1.2), dict(yaw=-1.2)]
    poses += [p for (n, (c, p)) in cast24.STORY24.items() if c == name and p.get("ground24") is None and not p.get("plank24")
              and not any(w in n for w in cast24.WIDE24)]
    for m in cast24.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast24.cycle(name, i / 16.0, m, facing=fc))
    return poses


def canvas_check(write=True):
    bad = 0
    res = {}
    for name in LINEUP:
        r = _range(name, member_poses(name))
        s = _sugg(r)
        res[name] = s
        print("%-10s range (%.3f, %.3f, %.3f, %.3f) -> canvas %r" % ((name,) + r + (s,)))
    spec = {}
    for n, (c, p) in cast24.STORY24.items():
        if p.get("ground24") is not None or p.get("plank24") or any(w in n for w in cast24.WIDE24):
            ps = [p, dict(p, mirror=True)]
            if "kneel" in n:
                # the hammer arm swing
                ps += [dict(p, arm_r=dict(hand=(0.78, 0.62), bend=-0.2, stretch=1.2, layer="front"), prop_r=dict(type=p["prop_r"]["type"], angle=20))]
            r = _range(c, ps)
            spec[n] = _sugg(r)
            print("%-28s range (%.3f, %.3f, %.3f, %.3f) -> canvas %r" % ((n,) + r + (spec[n],)))
    probs = 0
    for n, (c, p) in cast24.STORY24.items():
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
                print("  flip mismatch", n, key, va, vb)
    print("head_flip: %d poses checked, %d problems" % (len(cast24.STORY24), probs))
    # check against the shipped canvases
    for name, s in res.items():
        c = cast24.CANVAS24[name]
        if s[0] < c[0] - 1e-9 or s[1] < c[1] - 1e-9 or s[2] > c[2] + 1e-9 or s[3] > c[3] + 1e-9:
            print("CANVAS TOO SMALL for", name, c, "need", s)
            bad += 1
    for n, s in spec.items():
        c = cast24.CANVAS24_POSES[n]
        if s[0] < c[0] - 1e-9 or s[1] < c[1] - 1e-9 or s[2] > c[2] + 1e-9 or s[3] > c[3] + 1e-9:
            print("CANVAS TOO SMALL for", n, c, "need", s)
            bad += 1
    print("canvas check:", "ok" if not bad else "%d too small" % bad)
    return bad + probs


def _hashes():
    out = {}
    for n, (c, p) in sorted(P.STORY.items()):
        if n in cast24.STORY24:
            continue
        out["story:" + n] = hashlib.md5(P.figure(c, p, "z")["svg"].encode()).hexdigest()
    import cast10
    for c in list(cast10.NEW10) + ["hero", "boss", "lin", "general", "kenta", "worker_a", "gunner_a"]:
        for m in ("walk", "run"):
            for i in range(0, 16, 3):
                out["cyc:%s:%s:%d" % (c, m, i)] = hashlib.md5(P.figure(c, cast10.cycle(c, i / 16.0, m), "z")["svg"].encode()).hexdigest()
    return out


def identical():
    code = ("import sys, json, os; sys.path.insert(0, %r); sys.argv=['x']; import test_cast24_ref as T; print(json.dumps(T.ref()))" % HERE)
    ref_path = os.path.join(HERE, "test_cast24_ref.py")
    with open(ref_path, "w") as fh:
        fh.write(
            "import sys, os, json, hashlib\nsys.path.insert(0, %r)\nimport cast10, puppet as P\n"
            "def ref():\n    out = {}\n"
            "    for n, (c, p) in sorted(P.STORY.items()):\n        out['story:' + n] = hashlib.md5(P.figure(c, p, 'z')['svg'].encode()).hexdigest()\n"
            "    for c in list(cast10.NEW10) + ['hero', 'boss', 'lin', 'general', 'kenta', 'worker_a', 'gunner_a']:\n"
            "        for m in ('walk', 'run'):\n            for i in range(0, 16, 3):\n"
            "                out['cyc:%%s:%%s:%%d' %% (c, m, i)] = hashlib.md5(P.figure(c, cast10.cycle(c, i / 16.0, m), 'z')['svg'].encode()).hexdigest()\n"
            "    return out\n" % os.path.join(PROJ, "v3", "cast10"))
    r = subprocess.run([sys.executable, "-I", "-c", "import sys; sys.path.insert(0, %r); import test_cast24_ref as T, json; print(json.dumps(T.ref()))" % HERE],
                       stdout=subprocess.PIPE, universal_newlines=True)
    try:
        os.remove(ref_path)
    except OSError:
        pass
    ref = json.loads(r.stdout.strip().splitlines()[-1])
    now = _hashes()
    diff = [k for k in ref if now.get(k) != ref[k]]
    print("earlier poses byte-identical with cast24 imported: %d checked, %d differ %s" % (len(ref), len(diff), diff[:5]))
    return len(diff)


def robust():
    import random
    rnd = random.Random(24)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("wet24", "hat_rot24", "hat_dx24", "ground24", "plank24", "plank_w24", "plank_dx24", "plank_top24", "spike_n24", "sweat", "t", "squash", "mirror", "expr")
    t0 = time.time()
    for name in LINEUP:
        for i in range(300):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast24.NEW_PROPS24)
            p["prop_l"] = rnd.choice((None,) + cast24.NEW_PROPS24)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("jp_cmd24", cast24.STORY24["jp_cmd24_plank_cling"][1], "d")["svg"]
    b = P.figure("jp_cmd24", cast24.STORY24["jp_cmd24_plank_cling"][1], "d")["svg"]
    print("cast24 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, a == b, time.time() - t0))
    return fail + (0 if a == b else 1)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        canvas_check()
    if what in ("all", "identical"):
        identical()
    if what in ("all", "robust"):
        robust()
