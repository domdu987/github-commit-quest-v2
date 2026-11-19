#!/usr/bin/env python3
"""test_cast19.py -- QA for cast19.py (film 19: John Harrison and the longitude).

    python3 test_cast19.py            everything below (story, identity, canvas, robust, sheets)
    python3 test_cast19.py story      every STORY19 pose (and variants / cycles) renders, finite bbox, deterministic, mouth rule
    python3 test_cast19.py identity   earlier casts unchanged: every pose of puppet.STORY (v2 + cast_ext + cast2..cast10) and a pose-key sweep over
                                      every earlier CAST member give byte-identical SVG with and without cast19 imported (two separate processes)
    python3 test_cast19.py canvas     every STORY19 pose (mirrored too), the cycles and variants fit CANVAS19;  `canvas print` prints a fresh table
    python3 test_cast19.py robust     garbage pose keys on the members
    python3 test_cast19.py sheet      lineup.png (height ruler), expressions.png, poses.png, props.png (PNG via the puppet's own renderer)
"""
import hashlib
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import cast19  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast19.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
PEOPLE = cast19.NEW19
LINEUP = ("harrison19:young", "harrison19", "harrison19:old", "william19", "astro19", "astro19_b", "astro19_c", "king19", "captain19", "sailor19_a", "sailor19_b", "sailor19_c")
LINEUP_POSE = {
    "harrison19:young": dict(expr="neutral", yaw=0.3, young=1), "harrison19": dict(expr="neutral", yaw=0.3), "harrison19:old": dict(expr="neutral", yaw=0.3, old=1),
    "william19": dict(expr="happy", yaw=0.3), "astro19": dict(expr="smug", yaw=0.3, arm_r="akimbo", arm_l="akimbo", legs="wide"), "astro19_b": dict(expr="unimpressed", yaw=0.3),
    "astro19_c": dict(expr="smug", yaw=0.3), "king19": dict(expr="neutral", yaw=0.3), "captain19": dict(expr="determined", yaw=0.3), "sailor19_a": dict(expr="happy", yaw=0.3),
    "sailor19_b": dict(expr="neutral", yaw=0.3), "sailor19_c": dict(expr="grinning", yaw=0.3),
}
MOUTH_OK = {"astro_mock_point"}          # the one pose holding a talk_b mouth (a mocking quote: drive it with talk_mouth)


def _svgdoc(W, H, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, body)


def _write(svg, w, h, base, ext="png"):
    sp = os.path.join(TMP, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(TMP, base + "." + ext)
    P._raster(sp, out, w, h, 1)
    try:
        os.remove(sp)
    except OSError:
        pass
    return out


def _under(x, y, text, size=13):
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def _fig(cast, pose, uid, D, x, y, shadow=0.9):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _split(name):
    c, _, v = name.partition(":")
    return c, v


def _save(svg, w, h, name):
    out = _write(svg, w, h, name)
    dst = os.path.join(HERE, name + ".png")
    with open(out, "rb") as a, open(dst, "wb") as b:
        b.write(a.read())
    print("wrote %s (%d x %d)" % (dst, w, h))


# ---------------------------------------------------------------------------------------------------- sheets
def sec_lineup(D=130):
    colw = int(2.5 * D)
    W = colw * len(LINEUP) + 80
    top = int(0.9 * D)
    ground = top + int(4.4 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.10 * D), W, H, GROUND)]
    for i in range(0, 5):
        y = ground - i * D
        o.append('<path d="M6,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1" opacity="0.7" stroke-dasharray="3 5"/>' % (y, W - 6, y))
        o.append('<path d="M6,%.1f L26,%.1f" stroke="#2e2a2c" stroke-width="2"/>' % (y, y))
        o.append(LABEL(30, int(y) - 4, "%d D" % i, 13))
    for i, name in enumerate(LINEUP):
        c, v = _split(name)
        x0 = 80 + colw * i
        pose = dict(LINEUP_POSE[name])
        f0 = P.figure(c, pose, "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        g, f = _fig(c, pose, "h%d" % i, D, x0 + colw * 0.5, ground)
        o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#2e2a2c" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, "%.2f D" % ht + ("" if abs(hh - ht) < 0.03 else " (hat/wig %.2f)" % hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.50 * D), name, 14))
    o.append(LABEL(10, 26, "cast19 lineup: head D = %d px, heads top to soles in D (dashed line = top of head), ruler at the left" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=82, cols=8):
    names = list(cast19.STORY19)
    cw, ch = int(3.7 * D), int(6.0 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast19.STORY19[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.85 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.5 * D), x0, y0, cw, ch - int(0.5 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        o.append(LABEL(x0 + cw - 70, y0 + 18, "shot " + str(cast19.STORY19_META.get(n, {}).get("shots", "")), 11))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.20 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
          ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing", fx=["tears"])),
          ("smug", dict(expr="smug")), ("angry", dict(expr="angry")), ("shocked", dict(expr="shocked", fx=["sweat"])), ("jaw drop", dict(expr="shocked", mouth=("open", 0.26, 0.20))),
          ("yawn", dict(expr="asleep", mouth=("open", 0.30, 0.21))), ("worried", dict(expr="worried", fx=["sweat"])), ("sad", dict(expr="sad")))


def sec_faces(D=96):
    rows = (("harrison19", {}), ("harrison19 young", dict(young=1)), ("harrison19 old", dict(old=1)), ("william19", {}), ("william19 (hat off)", dict(hat_off=1)), ("astro19", {}),
            ("astro19_b", {}), ("astro19_c", {}), ("king19", {}), ("captain19", {}), ("sailor19_a", {}), ("sailor19_b", {}), ("sailor19_c", {}))
    cw, ch = int(1.7 * D), int(2.3 * D)
    W, H = 200 + cw * len(STATES), ch * len(rows) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, (lab, extra) in enumerate(rows):
        c = lab.split(" ")[0]
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, lab, 14))
        for j, (sl, st) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **dict(extra, **st)), "f%d_%d" % (r, j))
            cx, cy = 200 + j * cw + cw / 2, y0 + ch * 0.48
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (200 + j * cw, y0, cw, ch - 26, 200 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            if r == 0:
                o.append(_under(cx, y0 + ch - 8, sl, 11))
    o.append(LABEL(6, 16, "expressions, mouths, blinks (heads, yaw 0.3)", 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=200):
    items = ("h4_watch", "pocketwatch19", "quadrant19", "candlestick19", "tricorn_held", "file19", "chisel19", "quill19", "scroll19", "chart19", "h1_clock19", "rope19", "bucket19")
    cw, ch = int(2.3 * D), int(1.8 * D)
    cols = 5
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    ang = dict(quadrant19=-30, file19=-10, chisel19=-10, quill19=-20, scroll19=-10, rope19=0)
    for i, t in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        pd = dict(type=t, scale=1.0)
        if t in ang:
            pd["angle"] = ang[t]
        pose = dict(yaw=0.4, expr="neutral", arm_r=dict(hand=(0.80, 0.95), bend=0.0, shape="open"), prop_r=pd, splash=1.0, t=0.3, glint=1.0)
        f = P.figure("harrison19", pose, "pr%d" % i)
        hx, hy = f["anchors"]["hand_r"]
        sc = D * (0.5 if t in ("h1_clock19", "rope19", "quadrant19", "chart19") else 1.0)
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 24, x0, y0, cw, ch - 24, x0 + cw * (0.32 if t in ("rope19", "file19", "chisel19", "quill19", "scroll19", "quadrant19") else 0.5) - hx * sc,
                    y0 + ch * 0.46 - hy * sc, sc, f["svg"]))
        o.append(_under(x0 + cw / 2, y0 + ch - 8, t, 13))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cycles(D=70):
    rows = (("harrison19", "walk"), ("astro19", "walk"), ("sailor19_a", "run"), ("king19", "march"))
    n = 8
    cw, ch = int(2.2 * D), int(4.0 * D)
    W, H = cw * n, ch * (len(rows) + 1)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, (c, mode) in enumerate(rows):
        for i in range(n):
            x0, y0 = i * cw, r * ch
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + r) % 2 else BG))
            g, f = _fig(c, cast19.cycle(c, i / float(n), mode, 1), "c%d_%d" % (r, i), D, x0 + cw / 2, y0 + ch - int(0.5 * D))
            o.append(g)
            if i == 0:
                o.append(_under(x0 + cw / 2, y0 + ch - 6, "%s %s" % (c, mode), 12))
    r = len(rows)
    for i in range(n):
        x0, y0 = i * cw, r * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + r) % 2 else BG))
        p = cast19.laugh_cycle(i / float(n), dict(yaw=0.25, pitch=-0.6, fx=["tears"], arm_r=dict(hand=(0.40, 0.92), bend=0.8, shape="open"), arm_l=dict(hand=(-0.46, 0.90), bend=0.8, shape="open"), legs="wide"))
        g, f = _fig("astro19_c", p, "lc%d" % i, D, x0 + cw / 2, y0 + ch - int(0.5 * D))
        o.append(g)
        if i == 0:
            o.append(_under(x0 + cw / 2, y0 + ch - 6, "laugh_cycle astro19_c", 12))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    t0 = time.time()
    for nm, fn in (("lineup", sec_lineup), ("poses", sec_poses), ("expressions", sec_faces), ("props", sec_props), ("cycles", sec_cycles)):
        svg, w, h = fn()
        _save(svg, w, h, nm)
    print("sheets in %.1f s" % (time.time() - t0))
    return 0


# ---------------------------------------------------------------------------------------------------- tests
def _all_poses():
    for n, (c, p) in cast19.STORY19.items():
        yield n, c, p


def story_check():
    bad = 0
    n = 0
    for name, c, p in _all_poses():
        try:
            a = P.figure(c, p, "s")
            b = P.figure(c, p, "s")
            assert a["svg"] == b["svg"], "not deterministic"
            assert a["svg"].startswith("<") and len(a["svg"]) > 500, "empty svg"
            assert all(map(math.isfinite, a["bbox"])) and a["bbox"][2] > a["bbox"][0] and a["bbox"][3] > a["bbox"][1], "bad bbox"
            for v in a["anchors"].values():
                assert all(map(math.isfinite, v)), "bad anchor"
            m = P.figure(c, dict(p, mirror=True), "s")
            assert all(map(math.isfinite, m["bbox"])), "mirror bbox"
            n += 1
        except Exception as e:  # noqa: BLE001
            bad += 1
            print("FAIL", name, repr(e))
    print("STORY19: %d poses render (plain + mirrored), deterministic: %d failed" % (n, bad))
    # no spec'd pose may lack its brief
    need = ("harrison_hold_h1", "harrison_file_bench", "harrison_show_h4", "harrison_tired_rub", "harrison_hopeful_door", "harrison_old_handover", "william_quadrant_sun",
            "william_show_h4", "william_cheer_hat", "astro_belly_laugh", "astro_mock_point", "astro_mock_bow", "astro_shrug_fluke", "astro_jaw_drop", "astro_sour_arms",
            "astro_b_laugh", "astro_c_laugh", "astro_b_peer", "astro_c_peer", "king_watch_squint", "king_write_seated", "king_point_decree", "captain_peer_chart")
    need += tuple("sailor_%s_%s" % (a, b) for a in "abc" for b in ("haul", "cheer", "bail"))
    miss = [nm for nm in need if nm not in cast19.STORY19]
    if miss:
        bad += 1
        print("FAIL missing poses", miss)
    # mouth rule: talk mouths only where documented
    talk = {nm for nm, c, p in _all_poses() if p.get("mouth") in ("talk_a", "talk_b", "talk_o")}
    stray = talk - MOUTH_OK
    if stray:
        bad += 1
        print("FAIL talk mouth outside the documented pose", sorted(stray))
    # variants and cycles
    for c in PEOPLE:
        for mode in cast19.CYCLE_MODES:
            for ph in (0.0, 0.3, 0.7):
                for fc in (1, -1):
                    try:
                        f = P.figure(c, cast19.cycle(c, ph, mode, fc), "y")
                        assert all(map(math.isfinite, f["bbox"]))
                    except Exception as e:  # noqa: BLE001
                        bad += 1
                        print("FAIL cycle", c, mode, ph, fc, repr(e))
        for var in ({}, dict(young=1), dict(old=1), dict(hat_off=1), dict(shavings=0), dict(stool=1, legs=dict(crouch=0.4))):
            f = P.figure(c, dict(var, expr="happy"), "v")
            assert all(map(math.isfinite, f["bbox"]))
    # the H4 watch: tick marks only, no text at all in any prop
    for t in cast19.NEW_PROPS19:
        svg = P.figure("harrison19", dict(arm_r=dict(hand=(0.4, 0.3)), prop_r=dict(type=t), splash=1.0), "z")["svg"]
        if "<text" in svg:
            bad += 1
            print("FAIL text in prop", t)
    return bad


def _ident_run(with_new):
    return (
        "import sys, hashlib, json, os\n"
        "sys.dont_write_bytecode = True\n"
        "sys.path.insert(0, %r)\n"
        "import %s\n"
        "import puppet as P\n"
        "res = {}\n"
        "names = json.loads(sys.argv[1]) if len(sys.argv) > 1 else None\n"
        "def h(c, p, tag):\n"
        "    return hashlib.sha1(P.figure(c, p, 'i')['svg'].encode()).hexdigest()\n"
        "keys = sorted(P.STORY) if names is None else names['story']\n"
        "for n in keys:\n"
        "    c, p = P.STORY[n]\n"
        "    res['story:' + n] = h(c, p, n)\n"
        "cast_names = sorted(P.CAST) if names is None else names['cast']\n"
        "sweep = [dict(), dict(yaw=0.6, expr='smug'), dict(yaw=-0.5, expr='laughing', arm_r='point', arm_l='akimbo', legs='wide'), dict(expr='shocked', mouth='talk_b', fx=['sweat'], head_roll=12),\n"
        "         dict(prop_r='shovel', arm_r='forward'), dict(prop_r='key', prop_l='palette', yaw=0.3), dict(prop_l='coin_purse', blink=1, mirror=True, lean=9), dict(prop_r='bigbrush', arm_r='raised'),\n"
        "         dict(squash=(1.05, 0.95), tint='#faded0', rim='#d9a27a', legs='step'), dict(hat_off=1, young=1, old=1, sash=1, belt_keys=0, glint=1, shavings=1, splash=1)]\n"
        "skip = set(%r)\n"
        "for c in cast_names:\n"
        "    if c in skip:\n"
        "        continue\n"
        "    for i, p in enumerate(sweep):\n"
        "        res['cast:%%s:%%d' %% (c, i)] = h(c, p, i)\n"
        "print(json.dumps(res))\n"
        "if names is None:\n"
        "    sys.stderr.write(json.dumps(dict(story=keys, cast=cast_names)))\n"
        % ((HERE if with_new else os.path.join(PROJ, "v3", "cast10")), "cast19" if with_new else "cast10", NEW_CAST_KEYS))


NEW_CAST_KEYS = ["harrison19", "harrison19_young", "harrison19_old", "william19", "william19_bare", "astro19", "astro19_b", "astro19_c", "king19", "captain19", "captain19_bare",
                 "sailor19_a", "sailor19_b", "sailor19_c"]


def identity_check():
    t0 = time.time()
    r0 = subprocess.run([sys.executable, "-c", _ident_run(False)], capture_output=True, text=True, cwd=TMP)
    if r0.returncode:
        print(r0.stderr[-2000:])
        return 1
    ref = json.loads(r0.stdout)
    names = json.loads(r0.stderr.strip().splitlines()[-1])
    r1 = subprocess.run([sys.executable, "-c", _ident_run(True), json.dumps(names)], capture_output=True, text=True, cwd=TMP)
    if r1.returncode:
        print(r1.stderr[-2000:])
        return 1
    new = json.loads(r1.stdout)
    diff = [k for k in ref if ref.get(k) != new.get(k)]
    n_story = sum(1 for k in ref if k.startswith("story:"))
    print("identity: %d earlier STORY poses (v2 + cast_ext + cast2..cast10) + %d member/pose-key combinations compared with and without cast19: %d differ (%.1f s)"
          % (n_story, len(ref) - n_story, len(diff), time.time() - t0))
    for k in diff[:10]:
        print("  DIFF", k)
    return len(diff)


def _rel(f):
    fx, fy, b = f["anchors"]["feet"][0], f["feet_y"], f["bbox"]
    return (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)


def _canvas_cases():
    """yield (member, pose) over everything the cast does."""
    for name, c, p in _all_poses():
        yield c, p
    for c in PEOPLE:
        for mode in cast19.CYCLE_MODES:
            for i in range(16):
                for fc in (1, -1):
                    yield c, cast19.cycle(c, i / 16.0, mode, fc)
        for yaw in (-1.2, -0.6, 0.0, 0.6, 1.2):
            yield c, dict(yaw=yaw)
    for i in range(8):
        for c in ("astro19", "astro19_b", "astro19_c", "sailor19_a", "king19"):
            yield c, cast19.laugh_cycle(i / 8.0, dict(yaw=0.25, pitch=-0.6, fx=["tears"], arm_r=dict(hand=(0.40, 0.92), bend=0.8, shape="open"), arm_l=dict(hand=(-0.46, 0.90), bend=0.8, shape="open"), legs="wide"))


def canvas_check(emit=False):
    bad = 0
    worst = {}
    u = {}
    for c, p in _canvas_cases():
        for mir in (False, True):
            f = P.figure(c, dict(p, mirror=True) if mir else p, "k")
            r = _rel(f)
            cast = c
            q = u.setdefault(cast, [9, 9, -9, -9])
            q[0], q[1], q[2], q[3] = min(q[0], r[0]), min(q[1], r[1]), max(q[2], r[2]), max(q[3], r[3])
            cv = cast19.CANVAS19.get(c)
            if cv:
                m = min(r[0] - cv[0], r[1] - cv[1], cv[2] - r[2], cv[3] - r[3])
                if c not in worst or m < worst[c]:
                    worst[c] = m
                if m < -1e-9:
                    bad += 1
    snap = lambda v, up: (math.ceil(v * 16) if up else math.floor(v * 16)) / 16.0      # noqa: E731
    table = {c: (snap(q[0] - 0.05, False), snap(q[1] - 0.10, False), snap(q[2] + 0.05, True), snap(q[3] + 0.10, True)) for c, q in sorted(u.items())}
    if emit:
        sx = max(abs(v[0]) if abs(v[0]) > abs(v[2]) else abs(v[2]) for v in table.values())
        print("CANVAS19_TABLE.update({")
        for c, v in table.items():
            print('    "%s": (%.4f, %.4f, %.4f, %.4f),' % ((c,) + v))
        print("})")
        return 0
    print("canvas: %d outside; smallest margins (D): %s" % (bad, ", ".join("%s %.2f" % (c, w) for c, w in sorted(worst.items()))))
    missing = [c for c in PEOPLE if c not in cast19.CANVAS19]
    if missing:
        print("FAIL canvas missing", missing)
        bad += 1
    return bad


def robust():
    import random
    rnd = random.Random(19)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("young", "old", "hat_off", "stool", "stool_w", "stool_dx", "stool_dy", "glint", "shavings", "splash", "t", "squash", "mirror", "expr", "gaze", "tint", "ink", "lean", "head_dy")
    t0 = time.time()
    for name in cast19.NEW19:
        for i in range(300):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast19.NEW_PROPS19)
            p["prop_l"] = rnd.choice((None,) + cast19.NEW_PROPS19)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"])), "bbox"
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 6:
                    print("FAIL", name, p, repr(e))
    a = P.figure("king19", cast19.STORY19["king_watch_squint"][1], "d")["svg"]
    b = P.figure("king19", cast19.STORY19["king_watch_squint"][1], "d")["svg"]
    print("cast19 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, a == b, time.time() - t0))
    return fail + (0 if a == b else 1)


def main(argv):
    what = argv[1] if len(argv) > 1 else "all"
    bad = 0
    if what in ("all", "story"):
        bad += story_check()
    if what in ("all", "identity"):
        bad += identity_check()
    if what in ("all", "canvas"):
        bad += canvas_check(len(argv) > 2 and argv[2] == "print")
    if what in ("all", "robust"):
        bad += robust()
    if what in ("all", "sheet"):
        build_sheet()
    print("TOTAL FAILED:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
