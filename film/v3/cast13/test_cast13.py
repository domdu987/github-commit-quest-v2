#!/usr/bin/env python3
"""test_cast13.py -- QA for cast13.py (film 13: raising the Tremont House, Chicago 1861).

    python3 test_cast13.py            sheet.jpg, canvas check, robustness
    python3 test_cast13.py sheet      sheet.jpg only: heights (+ film 10's admiral for scale) / EVERY STORY13 pose, grouped by character, labelled /
                                      faces + lip-sync mouths / props and set-dressing pieces.  Labels under each image, neutral warm grey ground.
    python3 test_cast13.py canvas     sprite canvas check (measured ranges against cast13.CANVAS13 / CANVAS13_POSE), mirror/head_flip, A/B jack pivot
    python3 test_cast13.py robust     pose-key garbage on all members, determinism, cast10 poses byte-identical with and without cast13, v2 test_puppet --quick
Section images are kept in tmp/ (sec_*.png).
"""
import hashlib
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast13  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast13.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#d2cbc2", "#c8c1b7", "#aca396"          # neutral warm greys
LINEUP = cast13.NEW13
REF = ("admiral",)                                         # film 10, for scale
LINEUP_POSE = {
    "pullman": dict(expr="neutral", mouth="smile", arm_r="behind", arm_l="akimbo"),
    "rich": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
    "foreman13": dict(expr="neutral", arm_r="akimbo", arm_l="akimbo"),
    "gentleman13": dict(expr="neutral", arm_r="behind", arm_l="behind"),
    "admiral": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
}
ORDER = ("pullman", "rich", "worker13_a", "worker13_b", "worker13_c", "foreman13", "lady13", "lady13_seat", "gentleman13", "town_a", "town_b", "town_c")


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
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def _lineup_pose(c):
    return dict(LINEUP_POSE.get(c, dict(expr="neutral")))


def sec_heights(D=100):
    members = ORDER + REF
    colw = int(2.55 * D)
    W = colw * len(members) + 20
    top = int(1.2 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG, 1.0 if c not in REF else 0.6))
        f0 = P.figure(c, _lineup_pose(c), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(_lineup_pose(c), yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c + ("  (film 10, scale ref)" if c in REF else ""), 15))
    o.append(LABEL(10, 30, "cast13: front / 3-4, head D = %d px; head top to soles and hat in D.  film 10 admiral at right for scale" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=70, cols=9):
    names = sorted(cast13.STORY13, key=lambda n: (ORDER.index(cast13.STORY13[n][0]) if cast13.STORY13[n][0] in ORDER else 99, list(cast13.STORY13).index(n)))
    cw, ch = int(3.5 * D), int(6.7 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast13.STORY13[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        dd = D * (0.55 if n == "rich_fall" else 1.0)
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, dd, x0 + cw * (0.40 if n == "rich_fall" else 0.46), ground - (int(1.2 * D) if n == "rich_fall" else 0), shadow=0 if n == "rich_fall" else 0.9)
        o.append(g + "</svg>")
        meta = cast13.STORY13_META.get(n, cast13.STORY13_META.get(n.rsplit("_", 1)[0], {}))
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")),
          ("laughing", dict(expr="laughing")), ("smug", dict(expr="smug")), ("angry", dict(expr="angry")), ("shouting", dict(expr="shouting")),
          ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")), ("sad", dict(expr="sad")), ("dazed", dict(expr="dazed")))


def sec_faces(D=84):
    cw, ch = int(1.45 * D), int(2.0 * D)
    W, H = 150 + cw * len(STATES), ch * len(ORDER) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(ORDER):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 14))
        for j, (lab, extra) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **extra), "f%d_%d" % (r, j))
            cx, cy = 150 + j * cw + cw / 2, y0 + ch * 0.47
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (150 + j * cw, y0, cw, ch - 26, 150 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=200):
    items = []
    items.append(("whistle + chain", '<g transform="translate(-0.05 -0.15)">%s</g>' % cast13.whistle_svg("pa"), 1.5))
    items.append(("plans (rolled)", '<g transform="translate(-0.1 0)">%s</g>' % cast13.plans_svg("pb"), 1.3))
    items.append(("teacup + saucer", '<g transform="translate(0 -0.1)">%s</g>' % cast13.teacup_svg("pc"), 1.5))
    items.append(("teacup (pinky)", '<g transform="translate(0 -0.1)">%s</g>' % cast13.teacup_svg("pd", saucer=False), 1.5))
    items.append(("jack_bar", '<g transform="translate(-0.45 0)">%s</g>' % cast13.jack_bar_svg("pe"), 0.62))
    items.append(("iron_jack (carried)", '<g transform="translate(-0.05 0)">%s</g>' % cast13.iron_jack_svg("pf"), 0.9))
    js, _ = cast13.jack_svg("pg", 0.0, 0.0, 0.95, top=-0.80)
    items.append(("jack (jack=1)", '<g transform="translate(0 0)">%s</g>' % js, 0.55))
    items.append(("purse", '<g transform="translate(0 -0.2)">%s</g>' % cast13.purse_svg("ph"), 1.5))
    items.append(("bills", '<g transform="translate(-0.15 0)">%s</g>' % cast13.bills_svg("pi"), 1.3))
    items.append(("newspaper", cast13.newspaper_svg("pj"), 0.85))
    s, bb = cast13.armchair_svg("pk", hip_y=0.0, floor_y=0.95, hw=0.7, col="red")
    items.append(("armchair (red)", '<g transform="translate(0 0.4)">%s</g>' % s, 0.52))
    s, bb = cast13.armchair_svg("pl", hip_y=0.0, floor_y=0.95, hw=0.7, col="teal")
    items.append(("armchair (teal)", '<g transform="translate(0 0.4)">%s</g>' % s, 0.52))
    items.append(("mud puddle", cast13.mud_pool_svg("pm", 1.0), 0.45))
    cw, ch = int(1.3 * D), int(1.45 * D)
    cols = 7
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, svg, sc) in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 30, x0, y0, cw, ch - 30, x0 + cw / 2, y0 + ch * 0.45, D * sc, svg))
        o.append(_under(x0 + cw / 2, y0 + ch - 10, lab, 14))
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
    print("wrote %s (%dx%d) in %.1f s; %d poses rendered" % (p, W, H, time.time() - t0, len(cast13.STORY13)))
    return p


def _check(label, name, poses, c):
    x0, y0, x1, y1 = cast13._range(name, poses)
    clipped = x0 < c[0] - 1e-9 or y0 - 0.32 < c[1] or x1 > c[2] + 1e-9 or y1 > c[3] + 1e-9
    sugg = cast13.canvas_of((x0, y0, x1, y1))
    print("%-24s %-5s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok",
                                                                                          ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast13.NEW13:
        bad += _check("", name, cast13.member_poses(name), cast13.CANVAS13[name])
    for n, c in cast13.CANVAS13_POSE.items():
        cn, p = cast13.STORY13[n]
        bad += _check("POSE", n if len(n) < 24 else n[:24], [p, dict(p, mirror=True)], c) if False else _check("POSE", cn, [p, dict(p, mirror=True)], c)
    probs = 0
    for n, (c, p) in cast13.STORY13.items():
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if p.get("tumble"):
                continue
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
                print("head_flip problem", n, key, va, vb)
    print("head_flip: %d poses checked, %d problems" % (len(cast13.STORY13), probs))
    # the jack pivot is identical in turn_bar A and B (the screw jack must not move between the two frames)
    pv = 0
    for sfx in ("_a", "_b", "_c"):
        fa = P.figure(*cast13.STORY13["worker_turn_bar_A" + sfx], "a")
        fb = P.figure(*cast13.STORY13["worker_turn_bar_B" + sfx], "b")
        da = (fa["anchors"]["jack_collar"][0] - fa["anchors"]["feet"][0], fa["anchors"]["jack_collar"][1] - fa["feet_y"])
        db = (fb["anchors"]["jack_collar"][0] - fb["anchors"]["feet"][0], fb["anchors"]["jack_collar"][1] - fb["feet_y"])
        ok = abs(da[0] - db[0]) < 1e-6 and abs(da[1] - db[1]) < 1e-6
        pv += 0 if ok else 1
        print("jack collar vs feet, A/B%s: %s %s" % (sfx, "identical" if ok else "DIFFERENT", tuple(round(v, 3) for v in da)))
    return bad + probs + pv


def _hash_story10():
    """sha1 of every cast10 STORY10 pose's svg, in a fresh interpreter without and with cast13 imported."""
    base = ("import sys, hashlib; sys.path.insert(0, %r)\nimport cast10\nimport puppet as P\n%%s"
            "h = hashlib.sha1()\nfor n in sorted(cast10.STORY10):\n    c, p = cast10.STORY10[n]\n    h.update(P.figure(c, p, 'z')['svg'].encode())\nprint(h.hexdigest())\n"
            % os.path.join(PROJ, "v3", "cast10"))
    plain = subprocess.run([sys.executable, "-c", base % ""], capture_output=True, text=True).stdout.strip()
    withc = subprocess.run([sys.executable, "-c", base % ("sys.path.insert(0, %r)\nimport cast13\n" % HERE)], capture_output=True, text=True).stdout.strip()
    return plain, withc


def robust():
    import random
    rnd = random.Random(13)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "teal", (1, 2, 3), (1, 2))
    keys = ("armchair", "jack", "jack_turn", "mud", "tumble", "hat_fly", "dizzy", "blast", "tea", "whistle_hang", "t", "squash", "mirror", "expr", "yaw")
    props = (None,) + cast13.NEW_PROPS13
    t0 = time.time()
    for name in cast13.NEW13:
        for i in range(300):
            p = {}
            for kk in keys:
                if rnd.random() < 0.45:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice(props)
            p["prop_l"] = rnd.choice(props)
            if not isinstance(p.get("yaw"), (int, float)) or isinstance(p.get("yaw"), bool):
                p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"])), f["bbox"]
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 6:
                    print("FAIL", name, p, repr(e))
    a = P.figure("rich", cast13.STORY13["rich_sit_in_mud"][1], "d")["svg"]
    b = P.figure("rich", cast13.STORY13["rich_sit_in_mud"][1], "d")["svg"]
    det = a == b
    for n_, (c, p) in cast13.STORY13.items():
        s = P.figure(c, p, "x")["svg"]
        if not s.startswith("<") or "nan" in s.lower():
            fail += 1
            print("BAD SVG", n_)
    print("cast13 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    plain, withc = _hash_story10()
    same = bool(plain) and plain == withc
    print("cast10 STORY10 svg hash without / with cast13: %s / %s  -> %s" % (plain[:12], withc[:12], "identical" if same else "DIFFERENT"))
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast13.NEW13
    rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + (0 if same else 1) + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    rcode = 0
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        rcode += canvas_check()
    if what in ("all", "robust"):
        rcode += robust()
    sys.exit(1 if rcode else 0)
