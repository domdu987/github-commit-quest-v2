#!/usr/bin/env python3
"""test_cast11.py -- QA for cast11.py (film 11: Jenner, cowpox, Berkeley 1796).

    python3 test_cast11.py            identity + canvas + robust + sheet
    python3 test_cast11.py identity   earlier casts still draw byte-identical with cast11 loaded (subprocess A: cast10 only, B: cast11)
    python3 test_cast11.py sheet      sheet.jpg (heights, every pose, faces, props, the cow + a milking scene) and a 360-px phone strip
    python3 test_cast11.py canvas     pose-range check of every member against cast11.CANVAS11 (+ LIE / YOKE canvases), head room
    python3 test_cast11.py robust     garbage pose keys on every member + v2 test_puppet.py --quick on the new members
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
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"

IDENT_SNIPPET = r'''
import sys, json, hashlib
sys.path.insert(0, %(c10)r)
if %(with11)s:
    sys.path.insert(0, %(c11)r)
    import cast11
else:
    import cast10
import puppet as P
out = {}
names = sorted(n for n in P.CAST if n not in %(new)r)
extra = ({}, dict(yaw=0.5, expr="happy", arm_r="point", arm_l="raised", fx=["sweat", "tears"], t=0.3), dict(yaw=-0.6, expr="angry", legs="wide", mirror=True, squash=(0.9, 1.1)))
for n in names:
    for i, p in enumerate(extra):
        out["%%s#%%d" %% (n, i)] = hashlib.md5(P.figure(n, p, "z")["svg"].encode()).hexdigest()
for n, (c, p) in sorted(P.STORY.items()):
    if c in names:
        out["story:" + n] = hashlib.md5(P.figure(c, p, "z")["svg"].encode()).hexdigest()
print(json.dumps(out))
'''


def _run_ident(with11):
    import cast11 as C11  # noqa: F401  (only for the paths)
    code = IDENT_SNIPPET % dict(c10=os.path.join(C11.PROJ, "v3", "cast10"), c11=HERE, with11=with11, new=tuple(C11.NEW11) + (C11.COW,))
    r = subprocess.run([sys.executable, "-c", code], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd="/")
    if r.returncode:
        print(r.stderr)
        raise SystemExit(1)
    return json.loads(r.stdout.strip().splitlines()[-1])


def identity():
    a = _run_ident(False)
    b = _run_ident(True)
    bad = [k for k in a if a[k] != b.get(k)]
    print("identity: %d drawings of earlier members (all CAST members x3 poses + their story poses), %d differ with cast11 loaded" % (len(a), len(bad)))
    for k in bad[:10]:
        print("  DIFF", k)
    return len(bad)


import cast11 as C11  # noqa: E402
import puppet as P  # noqa: E402
LABEL = P._label


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


LINEUP_POSE = {n: dict(expr="neutral") for n in C11.NEW11}
LINEUP_POSE["towndoc"] = dict(expr="smug", pitch=-0.3)
LINEUP_POSE["jenner"] = dict(expr="happy")


def sec_heights(D=110):
    members = list(C11.NEW11)
    colw = int(2.75 * D)
    W = colw * len(members) + 20
    top = int(1.1 * D)
    ground = top + int(3.7 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    rep = []
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        rep.append((c, ht, hh))
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 13))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c, 16))
    o.append(LABEL(10, 30, "cast11: front / 3-4, head D = %d px; head top to soles in D (dashed line)" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H, rep


def _canvas_for(name, pose=None):
    return None


def sec_poses(D=70, cols=9):
    names = [n for n in C11.STORY11 if C11.STORY11[n][0] != C11.COW]
    cw, ch = int(3.2 * D), int(4.9 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = C11.STORY11[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        g, f = _fig(cast, dict(pose, t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground, shadow=0 if pose.get("lie") else 0.9)
        o.append(g + "</svg>")
        if C11.STORY11_META.get(n, {}).get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "lip-sync", 12))
        if C11.STORY11_META.get(n, {}).get("gag"):
            o.append(LABEL(x0 + 6, y0 + 18, "GAG", 12))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
          ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing")), ("smug", dict(expr="smug")),
          ("angry", dict(expr="angry")), ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")), ("fever", dict(expr="sad", flush=1.0, sweat=1.0)),
          ("pocks=1", dict(pocks=1.0)), ("pocks=0", dict(pocks=0.0)))


def sec_faces(D=96):
    cw, ch = int(1.45 * D), int(2.0 * D)
    mem = list(C11.NEW11)
    W, H = 150 + cw * len(STATES), ch * len(mem) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(mem):
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


def _prop_fig(prop, uid, D, extra=None, cast="jenner"):
    pose = dict(yaw=0.0, arm_r=dict(hand=(0.55, 0.35), bend=-0.3), prop_r=prop)
    pose.update(extra or {})
    return P.figure(cast, pose, uid)


def sec_props(D=150):
    items = []
    for lab, prop, cast, extra, sc in (("lancet", dict(type="lancet", angle=-60), "jenner", None, 1.0),
                                       ("glass jar", "jar", "jenner", None, 1.0),
                                       ("notebook + quill", dict(type="notebook", angle=-20), "jenner", dict(arm_l=dict(hand=(-0.45, 0.35), bend=-0.3), prop_l=dict(type="quill", angle=20)), 1.0),
                                       ("milk pail", "pail", "sarah", dict(arm_r=dict(hand=(0.40, 0.8), bend=0.3)), 1.0),
                                       ("candle", "candle", "mother", dict(arm_r=dict(hand=(0.45, 0.55), bend=0.2)), 1.0),
                                       ("cane", dict(type="cane", angle=35), "towndoc", dict(arm_r=dict(hand=(-0.1, 0.9), bend=0.4)), 1.0),
                                       ("blister_hand", dict(type="blister_hand", angle=-70, scale=1.25), "sarah", dict(arm_r=dict(hand=(0.45, 0.45), bend=-0.2)), 1.0)):
        items.append((lab, prop, cast, extra))
    cw, ch = int(2.6 * D), int(2.5 * D)
    cols = len(items)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (cw * cols, ch + int(1.9 * D), BG)]
    for i, (lab, prop, cast, extra) in enumerate(items):
        x0 = i * cw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s"/>' % (x0, cw, ch, BG2 if i % 2 else BG))
        f = _prop_fig(prop, "q%d" % i, D, extra, cast)
        hx = f["anchors"]["head"]
        o.append('<svg x="%d" y="0" width="%d" height="%d" viewBox="%d 0 %d %d"><g transform="translate(%.1f %.1f) scale(%d)">%s</g></svg>'
                 % (x0, cw, ch - 28, x0, cw, ch - 28, x0 + cw * 0.42, D * 0.78, D, f["svg"]))
        o.append(_under(x0 + cw / 2, ch - 8, lab, 15))
    # row 2: stool, yoke, horns + ears, pockmarks, fever
    y0 = ch
    items2 = [("stool (stool=1)", "james", dict(yaw=-0.4, stool=1, legs=C11._sit("james")), 1.0),
              ("yoke (yoke=1)", "sarah", C11.STORY11["sarah_yoke"][1], 0.7),
              ("horns + cow_ears", "james", dict(yaw=0.2, expr="grinning", horns=1, cow_ears=1), 1.0),
              ("pockmarks (pocks=1)", "villager_a", dict(yaw=0.3, pocks=1.0), 1.0),
              ("fever flush + sweat", "james", dict(yaw=0.3, expr="sad", flush=1, sweat=1), 1.0)]
    for i, (lab, cast, pose, k) in enumerate(items2):
        x0 = i * cw
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, int(1.9 * D), BG2 if i % 2 == 0 else BG))
        f = P.figure(cast, pose, "r%d" % i)
        if i in (0, 1):
            sc, ox, oy = D * 0.62, 0.45, 0.95
        else:
            sc, ox, oy = D * 1.15, 0.45, 0.50
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.1f)">%s</g></svg>'
                 % (x0, y0, cw, int(1.9 * D) - 28, x0, y0, cw, int(1.9 * D) - 28, x0 + cw * ox, y0 + (0.98 * D if i not in (0, 1) else 0.30 * D), sc, f["svg"]))
        o.append(_under(x0 + cw / 2, y0 + int(1.9 * D) - 8, lab, 15))
    W, H = cw * cols, ch + int(1.9 * D)
    return _svgdoc(W, H, "".join(o)), W, H


def sec_cow(D=64):
    names = [n for n in C11.STORY11 if C11.STORY11[n][0] == C11.COW]
    cw, ch = int(6.7 * D), int(3.9 * D)
    cols = 3
    rows = (len(names) + 1 + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.9 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.1 * D), cw, int(0.3 * D), GROUND))
        g, f = _fig(C11.COW, dict(C11.STORY11[n][1], t=0.3), "c%d" % i, D, x0 + cw * 0.40, ground, shadow=3.3)
        o.append(g)
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.2 * D), n, 13))
    # the milking scene
    i = len(names)
    x0, y0 = (i % cols) * cw, (i // cols) * ch
    o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw * (cols - i % cols), ch, BG2))
    ground = y0 + ch - int(0.9 * D)
    cx = x0 + cw * 0.40
    gc, fc = _fig(C11.COW, dict(head_turn=0.8, chew=0.25, tail=0.3), "mc", D, cx, ground, shadow=3.3)
    sp = C11.STORY11["sarah_milk"][1]
    fs = P.figure("sarah", dict(sp, t=0.3), "ms")
    fa = fc["anchors"]
    mf = fa["milker_feet"]
    fx_ = cx + (mf[0] - fa["feet"][0]) * D
    gs, _ = _fig("sarah", dict(sp, t=0.3), "ms2", D, fx_, ground + 0.10 * D, shadow=1.0)
    # pail on the floor under the teats
    pk = '<g transform="translate(%.1f %.1f) scale(%d)">%s</g>' % (cx + (fa["pail_spot"][0] - fa["feet"][0]) * D, ground - 0.45 * D, D, C11._pail_body(P._Ctx("mp", P.INK, None)))
    o.append(gc + pk + gs)
    o.append(_under(x0 + cw / 2, y0 + ch - int(0.2 * D), "milking: sarah_milk (stool=1) + blossom + pail", 13))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_phone(D=75):
    """a 360-px-wide strip: head D = 75 px here equals D = 150 px in the 720 x 1280 frame."""
    W = 360
    rows = [(("jenner", C11.STORY11["jenner_lancet_up"][1]), ("james", C11.STORY11["james_sit_sleeve"][1]), ("sarah", C11.STORY11["sarah_show_hand"][1])),
            (("towndoc", C11.STORY11["towndoc_point_mock"][1]), ("villager_a", C11.STORY11["villager_a_point"][1]), ("villager_b", C11.STORY11["villager_b_laugh"][1])),
            (("villager_c", C11.STORY11["villager_c_whisper"][1]), ("mother", C11.STORY11["mother_stand_worried"][1]), ("milkmaid2", C11.STORY11["milkmaid2_smile"][1]))]
    rh = int(3.6 * D)
    H = rh * len(rows) + int(3.0 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, row in enumerate(rows):
        gy = r * rh + rh - int(0.2 * D)
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (gy - int(0.05 * D), W, int(0.3 * D), GROUND))
        for j, (c, p) in enumerate(row):
            g, f = _fig(c, dict(p, t=0.3), "ph%d%d" % (r, j), D * 0.82, W * (0.18 + 0.32 * j), gy)
            o.append(g)
    gy = len(rows) * rh + int(2.8 * D)
    o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (gy - int(0.05 * D), W, int(0.3 * D), GROUND))
    g, f = _fig(C11.COW, dict(head_turn=0.0, chew=0.25), "phc", D * 0.34, W * 0.40, gy, shadow=3.6)
    o.append(g)
    g, f = _fig("blossom", dict(head_turn=0.9), "phc2", D * 0.34, W * 0.40, gy - int(1.45 * D), shadow=0)
    g2, f2 = _fig("james", C11.STORY11["james_in_bed"][1], "phb", D * 0.5, W * 0.84, gy - int(0.1 * D), shadow=0)
    o.append(g2)
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    reps = []
    for name, fn in (("heights", sec_heights), ("poses", sec_poses), ("faces", sec_faces), ("props", sec_props), ("cow", sec_cow)):
        r = fn()
        svg, w, h = r[:3]
        if name == "heights":
            reps = r[3]
        parts.append(_write(svg, w, h, "sec_" + name))
    ph = sec_phone()
    pp = _write(ph[0], ph[1], ph[2], "sec_phone")
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    phone = Image.open(pp).convert("RGB")
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1) + 8 + phone.height
    out = Image.new("RGB", (W, H), (60, 58, 60))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    out.paste(phone, (0, y))
    from PIL import ImageDraw
    ImageDraw.Draw(out).text((380, y + 10), "<- phone-size strip: 360 px wide, head D = 75 px (= D 150 in the 720 x 1280 frame)", fill=(255, 255, 255))
    p = os.path.join(HERE, "sheet.jpg")
    out.save(p, quality=88)
    print("wrote %s (%dx%d) in %.1f s" % (p, W, H, time.time() - t0))
    for c, ht, hh in reps:
        print("  height %-11s head top to soles %.2f D (hat %.2f)" % (c, ht, hh))
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


MEMBER_PROPS = {"jenner": ("lancet", "jar", "notebook", "quill"), "james": ("jar",), "towndoc": ("cane", "jar"), "sarah": ("pail", "blister_hand", "candle"),
                "milkmaid2": ("pail",), "mother": ("candle", "pail"), "villager_a": ("pail",), "villager_b": ("pail", "candle")}


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None,) + MEMBER_PROPS.get(name, ()):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", sweat=1.0, flush=1.0, horns=1.0, cow_ears=1.0),
              dict(yaw=1.2), dict(yaw=-1.2), dict(horns=1.0, cow_ears=1.0, yaw=0.8, head_roll=20)]
    poses += [p for (c, p) in C11.STORY11.values() if c == name and not p.get("lie") and not p.get("yoke")]
    for m in C11.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(C11.cycle(name, i / 16.0, m, facing=fc))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-11s %-5s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                          "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in C11.NEW11:
        bad += _check("", name, member_poses(name), C11.CANVAS11[name])
    cow_poses = [dict(head_turn=h, ear=e, tail=t, chew=0.3, mirror=m) for h in (-0.4, 0, 0.5, 1) for e in (-1, 1) for t in (-1, 0, 1) for m in (False, True)]
    bad += _check("", "blossom", cow_poses, C11.CANVAS11["blossom"])
    for name, c in C11.CANVAS11_LIE.items():
        lp = [p for (cc, p) in C11.STORY11.values() if cc == name and p.get("lie")]
        lp += [dict(p, mirror=True, lie=-p["lie"], head_roll=-p["head_roll"]) for p in lp]
        bad += _check("LIE", name, lp, c)
    for name, c in C11.CANVAS11_YOKE.items():
        lp = [p for (cc, p) in C11.STORY11.values() if cc == name and p.get("yoke")]
        lp += [dict(p, mirror=True) for p in lp] + [dict(yoke=1, yoke_w=1.6, yoke_rope=1.2, yaw=y) for y in (-0.6, 0.6)]
        lp += [C11.cycle(name, i / 16.0, "walk") for i in range(16)] and [dict(C11.cycle(name, i / 16.0, "walk"), yoke=1) for i in range(16)]
        bad += _check("YOKE", name, lp, c)
    probs = 0
    for n, (c, p) in C11.STORY11.items():
        if c == C11.COW or p.get("lie"):
            continue
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=not p.get("mirror", False)), "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("mirror anchors: %d poses checked, %d problems" % (len(C11.STORY11), probs))
    return bad + probs


def robust():
    import random
    rnd = random.Random(11)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("pocks", "flush", "horns", "cow_ears", "hat_off", "stool", "stool_w", "stool_drop", "yoke", "yoke_w", "yoke_rope", "milk", "flame", "seated", "sweat", "t", "squash",
            "mirror", "expr", "lie", "head_turn", "ear", "tail", "chew", "chew_amp", "blink")
    t0 = time.time()
    for name in tuple(C11.NEW11) + (C11.COW,):
        for i in range(400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + C11.NEW_PROPS11)
            p["prop_l"] = rnd.choice((None,) + C11.NEW_PROPS11)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("towndoc", C11.STORY11["towndoc_sleeve_sheepish"][1], "d")["svg"]
    b = P.figure("towndoc", C11.STORY11["towndoc_sleeve_sheepish"][1], "d")["svg"]
    det = a == b
    print("cast11 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    sys.path.insert(0, os.path.join(C11.PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = tuple(C11.NEW11)
    rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    rc = 0
    if what in ("all", "identity"):
        rc += identity()
    if what in ("all", "canvas"):
        rc += canvas_check()
    if what in ("all", "robust"):
        rc += robust()
    if what in ("all", "sheet"):
        build_sheet()
    sys.exit(1 if rc else 0)
