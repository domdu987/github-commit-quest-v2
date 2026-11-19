#!/usr/bin/env python3
"""test_cast16.py -- QA for cast16.py (film 16: the telegraph).

    python3 test_cast16.py            everything below (sheet.jpg, story, identity, canvas, robust-lite); `full` adds the v2 test_puppet --quick run
    python3 test_cast16.py story      every STORY16 pose (and the variants / cycles) renders, finite bbox, deterministic, mouth rule, shot map
    python3 test_cast16.py identity   earlier casts unchanged: every pose of puppet.STORY (v2 + cast_ext + cast2..cast10) and a pose-key sweep over
                                      every earlier CAST member give byte-identical SVG with and without cast16 imported (two separate processes)
    python3 test_cast16.py canvas     every STORY16 pose (mirrored too), 16 phases x modes x facings of the cycles and the mule gaits fit CANVAS16
    python3 test_cast16.py sheet      sheet.jpg: lineup with a height ruler, every STORY16 pose labelled, the mule's gaits, mocker faces
    python3 test_cast16.py robust     garbage pose keys on the 11 members (+ the v2 test_puppet --quick run with `full`)
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
import cast16  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast16.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
PEOPLE = tuple(c for c in cast16.NEW16 if c != "mule")
LINEUP = ("morse16", "morse16:young", "mocker", "mocker:pm", "congressman_a", "congressman_b", "congressman_c", "messenger", "cornell", "worker16_a", "worker16_b", "clerk16", "mule")
LINEUP_POSE = {
    "morse16": dict(expr="neutral", yaw=0.3), "morse16:young": dict(expr="happy", yaw=0.3, young=1),
    "mocker": dict(expr="smug", yaw=0.3, arm_r="akimbo", arm_l="akimbo", legs="wide"), "mocker:pm": dict(expr="smug", yaw=0.3, sash=1, arm_r="akimbo", arm_l="akimbo", legs="wide"),
    "congressman_a": dict(expr="neutral", yaw=0.3), "congressman_b": dict(expr="happy", yaw=0.3), "congressman_c": dict(expr="smug", yaw=0.3),
    "messenger": dict(expr="neutral", yaw=0.3), "cornell": dict(expr="determined", yaw=0.3), "worker16_a": dict(expr="neutral", yaw=0.3),
    "worker16_b": dict(expr="neutral", yaw=0.3), "clerk16": dict(expr="neutral", yaw=0.3), "mule": dict(harness=0, expr="neutral"),
}
LIPSYNC = {"mocker_mock_point", "mocker_boast_chest", "mocker_boast_finger", "mocker_taunt_buggy"}


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


# ---------------------------------------------------------------------------------------------------- sheet sections
def sec_lineup(D=96):
    widths = [int((6.6 if n == 'mule' else 2.55) * D) for n in LINEUP]
    W = sum(widths) + 80
    top = int(0.9 * D)
    ground = top + int(4.6 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.10 * D), W, H, GROUND)]
    # height ruler: a tick every 1 D (head diameters), labelled
    for i in range(0, 5):
        y = ground - i * D
        o.append('<path d="M6,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1" opacity="0.7" stroke-dasharray="3 5"/>' % (y, W - 6, y))
        o.append('<path d="M6,%.1f L26,%.1f" stroke="#2e2a2c" stroke-width="2"/>' % (y, y))
        o.append(LABEL(30, int(y) - 4, "%d D" % i, 13))
    for i, name in enumerate(LINEUP):
        c, v = _split(name)
        colw = widths[i]
        x0 = 80 + sum(widths[:i])
        pose = dict(LINEUP_POSE[name])
        f0 = P.figure(c, pose, "m")
        if c == "mule":
            ht = f0["feet_y"] - f0["anchors"]["hat_top"][1]
            hh = f0["feet_y"] - f0["anchors"]["head_top"][1]
        else:
            ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
            hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        g, f = _fig(c, pose, "h%d" % i, D, x0 + colw * 0.5, ground, shadow=1.4 if c == "mule" else 0.9)
        o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#2e2a2c" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, ("%.2f D (ears)" if c == "mule" else "%.2f D") % ht + ("" if c == "mule" or abs(hh - ht) < 0.03 else " (hat %.2f)" % hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.50 * D), name, 14))
    o.append(LABEL(10, 26, "cast16 lineup: head D = %d px, heads top to soles in D (dashed line = top of head / ears), ruler at the left" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=62, cols=9):
    names = list(cast16.STORY16)
    cw, ch = int(3.7 * D), int(6.7 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast16.STORY16[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.85 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.5 * D), x0, y0, cw, ch - int(0.5 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        if cast16.STORY16_META.get(n, {}).get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        o.append(LABEL(x0 + cw - 60, y0 + 18, "shot " + str(cast16.STORY16_META.get(n, {}).get("shots", "")), 11))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.20 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_mule(D=60):
    items = [("walk %.3f" % (i / 8.0), cast16.cycle("mule", i / 8.0, "walk")) for i in range(8)]
    items += [("pull (plough) %.2f" % (i / 4.0), cast16.cycle("mule", i / 4.0, "pull", 1, dict(harness=1))) for i in range(4)]
    items += [("buggy walk %.2f" % (i / 4.0), cast16.cycle("mule", i / 4.0 + 0.1, "walk", 1, dict(harness=2))) for i in range(2)]
    items += [("idle", cast16.cycle("mule", 0.1, "idle")), ("idle, ear flick", cast16.cycle("mule", 0.2, "idle", base=dict(ear=1.0, expr="blink"))),
              ("bray (left)", cast16.cycle("mule", 0.0, "idle", -1, dict(bray=1, expr="strain", ear=-0.6))), ("surprised", dict(expr="surprised", ear=1.0)),
              ("happy, harness", dict(expr="happy", harness=1))]
    cols = 6
    cw, ch = int(6.4 * D), int(5.1 * D)
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, pose) in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.8 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.05 * D), cw, int(0.3 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.5 * D), x0, y0, cw, ch - int(0.5 * D)))
        g, f = _fig("mule", dict(pose, t=0.3), "u%d" % i, D, x0 + cw * 0.52, ground, shadow=3.2)
        o.append(g + "</svg>")
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.15 * D), lab, 13))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
          ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing", fx=["tears"])),
          ("smug", dict(expr="smug")), ("angry", dict(expr="angry")), ("shocked", dict(expr="shocked", fx=["sweat"])), ("jaw drop", dict(expr="shocked", mouth=("open", 0.26, 0.20))),
          ("yawn", dict(expr="asleep", mouth=("open", 0.30, 0.21))), ("worried", dict(expr="worried", fx=["sweat"])), ("sad", dict(expr="sad")))


def sec_faces(D=88):
    rows = (("mocker", {}), ("mocker (hat off)", dict(hat_off=1)), ("morse16", {}), ("morse16 young", dict(young=1)), ("congressman_a", {}), ("congressman_b", {}),
            ("congressman_c", {}), ("cornell", {}))
    cw, ch = int(1.5 * D), int(2.1 * D)
    W, H = 190 + cw * len(STATES), ch * len(rows) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, (lab, extra) in enumerate(rows):
        c = lab.split(" ")[0]
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, lab, 14))
        for j, (sl, st) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **dict(extra, **st)), "f%d_%d" % (r, j))
            cx, cy = 190 + j * cw + cw / 2, y0 + ch * 0.50
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (190 + j * cw, y0, cw, ch - 26, 190 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            if r == 0:
                o.append(_under(cx, y0 + ch - 8, sl, 11))
    o.append(LABEL(6, 16, "face states (mouths: lip-sync shapes only ever used on the mocker's quotes)", 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=170):
    items = (("letter", "wire_coil", "magnet", "bottle", "money_bag", "money_bag_empty", "telegraph_key", "candle", "stovepipe_held", "slouch_held", "keyring16", "palette16", "brush16",
              "cane16"))
    cw, ch = int(1.9 * D), int(1.7 * D)
    cols = 7
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, t in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        pose = dict(yaw=0.4, expr="neutral", arm_r=dict(hand=(0.2, 0.0), bend=0.0), prop_r=dict(type=t, angle=(0 if t in ("magnet", "bottle", "palette16", "brush16", "cane16") else None) if t not in ("cane16",) else 70, scale=0.55 if t == "cane16" else 1.0))
        f = P.figure("morse16", pose, "pr%d" % i)
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 24, x0, y0, cw, ch - 24, x0 + cw * 0.28, y0 + ch * 0.34, D * 0.62, f["svg"]))
        o.append(_under(x0 + cw / 2, y0 + ch - 8, t, 13))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    for nm, fn in (("lineup", sec_lineup), ("poses", sec_poses), ("mule", sec_mule), ("faces", sec_faces), ("props", sec_props)):
        svg, w, h = fn()
        parts.append((nm, _write(svg, w, h, "sec_" + nm), w, h))
        print("section %-7s %5d x %5d" % (nm, w, h))
    Wm = max(p[2] for p in parts)
    H = sum(p[3] for p in parts)
    im = Image.new("RGB", (Wm, H), (0xcf, 0xcc, 0xc6))
    y = 0
    for nm, path, w, h in parts:
        im.paste(Image.open(path).convert("RGB"), (0, y))
        y += h
    out = os.path.join(HERE, "sheet.jpg")
    im.save(out, quality=88)
    print("wrote %s (%d x %d) in %.1f s" % (out, Wm, H, time.time() - t0))
    return 0


# ---------------------------------------------------------------------------------------------------- tests
def _all_poses():
    for n, (c, p) in cast16.STORY16.items():
        yield n, c, p


def story_check():
    bad = 0
    t0 = time.time()
    names = list(cast16.STORY16)
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
    print("STORY16: %d poses render (plain + mirrored), deterministic: %d failed" % (n, bad))
    # mouth rule: talk_a / talk_b / talk_o only on the mocker's lip-sync poses; the lipsync META flag marks exactly those
    ls = {nm for nm in names if cast16.STORY16_META[nm].get("lipsync")}
    talk = {nm for nm, c, p in _all_poses() if p.get("mouth") in ("talk_a", "talk_b", "talk_o")}
    # the belly laugh holds a talk_b shape as a laugh mouth (held, never animated): allowed, documented
    held = {"mocker_belly_laugh", "mocker_taunt_buggy"} & talk
    if ls != LIPSYNC:
        bad += 1
        print("FAIL lipsync set", sorted(ls ^ LIPSYNC))
    stray = {nm for nm in talk if nm not in ls and nm not in held and not nm.startswith("mocker_")}
    if stray:
        bad += 1
        print("FAIL talk mouth on a non-mocker pose", sorted(stray))
    if any(cast16.STORY16[nm][0] != "mocker" for nm in ls):
        bad += 1
        print("FAIL lipsync on a non-mocker")
    print("mouth rule: lip-sync poses %s; held laugh mouths %s; no other talk mouths" % (sorted(ls), sorted(held)))
    # shot map covers 1..30 acting and names resolve
    missing = [(s, nm) for s, lst in cast16.STORY16_SHOTS.items() for nm in lst if nm not in cast16.STORY16]
    if missing:
        bad += 1
        print("FAIL STORY16_SHOTS names", missing)
    covered = sorted(cast16.STORY16_SHOTS)
    print("STORY16_SHOTS covers shots %s" % covered)
    # variants and cycles
    for c in PEOPLE:
        for mode in cast16.CYCLE_MODES:
            for ph in (0.0, 0.3, 0.7):
                for fc in (1, -1):
                    try:
                        f = P.figure(c, cast16.cycle(c, ph, mode, fc), "y")
                        assert all(map(math.isfinite, f["bbox"]))
                    except Exception as e:  # noqa: BLE001
                        bad += 1
                        print("FAIL cycle", c, mode, ph, fc, repr(e))
    for mode in ("walk", "pull", "idle"):
        for i in range(12):
            for fc in (1, -1):
                for h in (0, 1, 2):
                    try:
                        f = P.figure("mule", cast16.cycle("mule", i / 12.0, mode, fc, dict(harness=h)), "y")
                        assert all(map(math.isfinite, f["bbox"])) and abs(f["feet_y"] - cast16.MULE_G) < 1e-9
                    except Exception as e:  # noqa: BLE001
                        bad += 1
                        print("FAIL mule cycle", mode, i, fc, h, repr(e))
    print("cycles (people: %d casts x %d modes x 3 phases x 2 facings, mule: 3 modes x 12 phases x 2 facings x 3 harness) done, %.1f s" % (len(PEOPLE), len(cast16.CYCLE_MODES), time.time() - t0))
    for c in PEOPLE:
        for var in ({}, dict(young=1), dict(hat_off=1), dict(sash=1), dict(sash=1, hat_off=1), dict(stool=1, legs=dict(crouch=0.4))):
            f = P.figure(c, dict(var, expr="happy"), "v")
            assert all(map(math.isfinite, f["bbox"]))
    return bad


def _ident_run(with_new, names=None):
    code = (
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
        "         dict(squash=(1.05, 0.95), tint='#faded0', rim='#d9a27a', legs='step'), dict(hat_off=1, young=1, sash=1, belt_keys=0, glint=1)]\n"
        "skip = set(['mule', 'morse16', 'morse16_young', 'mocker', 'mocker_bare', 'mocker_pm', 'mocker_pm_bare', 'congressman_a', 'congressman_b', 'congressman_c', 'messenger', 'cornell', 'cornell_bare', 'worker16_a', 'worker16_b', 'clerk16'])\n"
        "for c in cast_names:\n"
        "    if c in skip:\n"
        "        continue\n"
        "    for i, p in enumerate(sweep):\n"
        "        res['cast:%%s:%%d' %% (c, i)] = h(c, p, i)\n"
        "print(json.dumps(res if names is None else res))\n"
        "if names is None:\n"
        "    sys.stderr.write(json.dumps(dict(story=keys, cast=cast_names)))\n" % ((HERE if with_new else os.path.join(PROJ, "v3", "cast10")), "cast16" if with_new else "cast10"))
    return code


def identity_check():
    t0 = time.time()
    # reference: cast10 alone
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
    print("identity: %d earlier STORY poses (v2 + cast_ext + cast2..cast10) + %d member/pose-key combinations compared with and without cast16: %d differ (%.1f s)"
          % (n_story, len(ref) - n_story, len(diff), time.time() - t0))
    for k in diff[:10]:
        print("  DIFF", k)
    return len(diff)


def _inside(r, c):
    return r[0] >= c[0] - 1e-9 and r[1] >= c[1] - 1e-9 and r[2] <= c[2] + 1e-9 and r[3] <= c[3] + 1e-9


def _rel(f):
    fx, fy, b = f["anchors"]["feet"][0], f["feet_y"], f["bbox"]
    return (b[0] - fx, b[1] - fy, b[2] - fx, b[3] - fy)


def canvas_check():
    bad = 0
    worst = {}

    def chk(cast, pose, canvas, tag):
        nonlocal bad
        for mir in (False, True):
            f = P.figure(cast, dict(pose, mirror=mir) if mir else pose, "k")
            r = _rel(f)
            m = min(r[0] - canvas[0], r[1] - canvas[1], canvas[2] - r[2], canvas[3] - r[3])
            w = worst.get(cast)
            if w is None or m < w[0]:
                worst[cast] = (m, tag)
            if m < 0.0:
                bad += 1
                print("OUTSIDE", cast, tag, "mirror" if mir else "", "margin %.3f" % m)
    for name, c, p in _all_poses():
        cv = cast16.CANVAS16_POLE.get(c) if "pole" in name and c in cast16.CANVAS16_POLE else cast16.CANVAS16[c]
        chk(c, p, cv, name)
    for c in PEOPLE:
        cv = cast16.CANVAS16[c]
        for mode in cast16.CYCLE_MODES:
            for i in range(16):
                for fc in (1, -1):
                    chk(c, cast16.cycle(c, i / 16.0, mode, fc), cv, "%s %d" % (mode, i))
        for yaw in (-1.2, -0.6, 0.0, 0.6, 1.2):
            chk(c, dict(yaw=yaw), cv, "yaw %.1f" % yaw)
    for mode in ("walk", "pull", "idle"):
        for i in range(24):
            for h in (0, 1):
                for ex in ("neutral", "strain"):
                    chk("mule", cast16.cycle("mule", i / 24.0, mode, 1, dict(harness=h, expr=ex, bray=i % 2)), cast16.CANVAS16["mule"], "%s %d h%d" % (mode, i, h))
            chk("mule", cast16.cycle("mule", i / 24.0, mode, 1, dict(harness=2)), cast16.CANVAS16_BUGGY["mule"], "buggy %s %d" % (mode, i))
    print("canvas: %d outside; smallest margins (D): %s" % (bad, ", ".join("%s %.2f (%s)" % (c, w[0], w[1]) for c, w in sorted(worst.items()))))
    return bad


def robust(full=False):
    import random
    rnd = random.Random(16)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("young", "hat_off", "sash", "stool", "stool_w", "stool_dx", "stool_dy", "glint", "key_press", "belt_keys", "t", "squash", "mirror", "expr", "phase", "stride", "lift", "bob",
            "head_pitch", "head_dy", "ear", "tail", "droop", "strain", "bray", "gaze", "harness", "rest", "tint", "ink")
    t0 = time.time()
    for name in cast16.NEW16:
        for i in range(400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast16.NEW_PROPS16)
            p["prop_l"] = rnd.choice((None,) + cast16.NEW_PROPS16)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"])), "bbox"
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 6:
                    print("FAIL", name, p, repr(e))
    a = P.figure("mocker", cast16.STORY16["mocker_stool_candle"][1], "d")["svg"]
    b = P.figure("mocker", cast16.STORY16["mocker_stool_candle"][1], "d")["svg"]
    det = a == b
    P.figure("admiral", dict(), "z")
    print("cast16 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    rc = 0
    if full:
        sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
        import test_puppet as T
        T.CASTS = PEOPLE
        rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + rc


def main(argv):
    what = argv[1] if len(argv) > 1 else "all"
    bad = 0
    if what in ("all", "story", "full"):
        bad += story_check()
    if what in ("all", "identity", "full"):
        bad += identity_check()
    if what in ("all", "canvas", "full"):
        bad += canvas_check()
    if what in ("all", "robust", "full"):
        bad += robust(what == "full")
    if what in ("all", "sheet", "full"):
        build_sheet()
    print("TOTAL FAILED:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
