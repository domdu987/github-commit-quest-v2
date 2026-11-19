#!/usr/bin/env python3
"""test_cast15.py -- QA for cast15.py (film 15: Dick Fosbury and the flop).

    python3 test_cast15.py            sheet.jpg + sheet_phone.jpg, canvas check, robustness
    python3 test_cast15.py sheet      sheet.jpg (labelled, head D = 70 px) and sheet_phone.jpg (phone scale, head D = 34 px)
    python3 test_cast15.py canvas     bbox of every character x every preset against CANVAS15 / CANVAS15_WIDE
    python3 test_cast15.py robust     pose-key garbage on all members, determinism, cast10 regression (byte-identical)
"""
import hashlib
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast15  # noqa: E402
import puppet as P  # noqa: E402

TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
BG, BG2, GROUND = "#cfccc6", "#c4c1ba", "#a9a49a"
HEIGHT = {}


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
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def _place(cast, pose, uid, D, hx, hy):
    """figure with its HEAD centre at (hx, hy)."""
    f = P.figure(cast, pose, uid)
    return '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (hx, hy, D, f["svg"]), f


def height_of(cast):
    if cast not in HEIGHT:
        f = P.figure(cast, {}, "h")
        HEIGHT[cast] = f["feet_y"] + 0.51
    return HEIGHT[cast]


# ------------------------------------------------------------------ sections
def sec_heights(D=100):
    members = cast15.ALL15
    colw = int(2.5 * D)
    W = colw * ((len(members) + 1) // 2) + 40
    rows = 2
    per = (len(members) + 1) // 2
    top = int(1.0 * D)
    ground = top + int(4.2 * D)
    H = rows * (ground + int(0.7 * D))
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r in range(rows):
        g0 = r * (ground + int(0.7 * D))
        o.append('<rect y="%d" width="%d" height="%d" fill="%s"/>' % (g0 + ground - int(0.12 * D), W, int(0.82 * D), GROUND))
        for i, n in enumerate(members[r * per:(r + 1) * per]):
            x = 20 + colw * i + colw // 2
            for j, (yw, dx) in enumerate(((0.0, -0.55), (0.55, 0.55))):
                f = P.figure(n, dict(yaw=yw, expr="neutral"), "h%s%d%d" % (n, r, j))
                tx, ty = x + dx * D - f["anchors"]["feet"][0] * D, g0 + ground - f["feet_y"] * D
                o.append('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]))
            h = height_of(n)
            o.append(_under(x, g0 + ground + int(0.4 * D), "%s  %.2f D" % (n, h)))
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_heights")


PRESET_CAST = {
    # jumper presets on dick / a boy, coach presets on the coach, crowd presets on crowd members
    "jump": ("dick", ["rock_a", "rock_b", "plant", "takeoff", "flop_rise", "flop_head", "flop_back", "flop", "flop_flick", "land_back", "lie_back",
                      "sit_up", "straddle_a", "straddle_b", "knock", "lie_hands_face", "cheer", "podium", "thumb", "sit_thumb", "stand", "walk_dejected"]),
    "coach": ("coach", ["coach_laugh", "coach_point", "coach_neck", "coach_wag_a", "coach_wag_b", "coach_jab", "coach_shout", "coach_jaw", "coach_sigh",
                        "coach_clumsy_flop", "coach_buried", "clip", "stand"]),
    "boys": ("boy1", ["laugh", "point_laugh", "point", "gape", "jaw_drop", "cheer", "sit_cross", "sit_laugh", "sit_cheer", "sit_gape", "sit_point", "sit_read"]),
    "press": ("photographer", ["photog_ready", "photog_flash"]),
    "officials": ("official1", ["official_stand", "official_raise", "official_point"]),
}
CASTMAP = {"dick": "dick", "podium": "dick_olympic", "cheer": None}


def sec_poses(D=70):
    items = []
    for key, (cast, names) in PRESET_CAST.items():
        for n in names:
            c = cast
            if n in ("podium", "lie_hands_face"):
                c = "dick_olympic"
            items.append((n, c, cast15.pose_for(n, c)))
    cols = 6
    cw, ch = 5.0, 4.5
    rows = (len(items) + cols - 1) // cols
    W, H = int(cols * cw * D), int(rows * ch * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (n, c, p) in enumerate(items):
        r, cc = divmod(i, cols)
        x0, y0 = cc * cw * D, r * ch * D
        o.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (x0, y0, cw * D, ch * D, BG if (r + cc) % 2 else BG2))
        hx, hy = x0 + cw * D * 0.5, y0 + ch * D * 0.28
        if n.startswith(("flop", "lie", "land", "straddle", "knock", "coach_clumsy")):
            hx, hy = x0 + cw * D * 0.62, y0 + ch * D * 0.45
        elif n.startswith("sit_up") or n == "sit_thumb":
            hx, hy = x0 + cw * D * 0.3, y0 + ch * D * 0.3
        s, f = _place(c, p, "p%d" % i, D, hx, hy)
        o.append(s)
        a = f["anchors"]
        if n in ("flop", "flop_back", "flop_head", "coach_clumsy_flop", "flop_flick"):
            bx, by = hx + a["bar"][0] * D, hy + a["bar"][1] * D
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e03030" stroke-width="3" opacity="0.8"/><circle cx="%.1f" cy="%.1f" r="5" fill="#e03030"/>' % (bx - 150, by, bx + 150, by, bx, by))
            o.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#20a040"/>' % (hx + a["apex"][0] * D, hy + a["apex"][1] * D))
        o.append(_under(x0 + cw * D / 2, y0 + ch * D - 6, "%s (%s)" % (n, c)))
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_poses")


def sec_compare(D=100):
    """FLOP sequence (curved bridge, belly up) above STRADDLE (flat, face down), same scale, bar line through the lower back / belly."""
    W, H = int(14.2 * D), int(8.4 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    seq = [("flop_rise", "dick"), ("flop_head", "dick"), ("flop_back", "dick"), ("flop", "dick"), ("flop_flick", "dick"), ("land_back", "dick")]
    x = 0.4 * D
    for i, (n, c) in enumerate(seq):
        s, f = _place(c, cast15.pose_for(n, c), "c%d" % i, D * 0.75, x + 1.2 * D, 2.4 * D)
        o.append(s)
        o.append(_under(x + 1.1 * D, 3.9 * D, n, 12))
        x += 2.3 * D
    seq = [("straddle_a", "boy1"), ("straddle_b", "boy1"), ("straddle_a", "rival1"), ("flop", "rival1"), ("flop", "boy2"), ("flop", "coach")]
    x = 0.4 * D
    for i, (n, c) in enumerate(seq):
        cc = "coach" if c == "coach" else c
        p = cast15.pose_for(n if c != "coach" else "coach_clumsy_flop", cc)
        s, f = _place(cc, p, "d%d" % i, D * 0.75, x + 1.2 * D, 6.4 * D)
        o.append(s)
        a = f["anchors"]
        if "flop" in n:
            by = 6.4 * D + a["bar"][1] * D * 0.75
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e03030" stroke-width="3" opacity="0.8"/>' % (x, by, x + 2.2 * D, by))
        o.append(_under(x + 1.1 * D, 8.1 * D, "%s %s" % (c, n if c != "coach" else "coach_clumsy_flop"), 12))
        x += 2.3 * D
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_compare")


def build_strip(D=90):
    """flop_strip.jpg: the four flop stages side by side (dick above, rival1 below), bar line at anchors["bar"] of the apex stage."""
    from PIL import Image
    stages = ["flop_head", "flop_back", "flop", "flop_flick"]
    cw, ch = 4.0, 4.2
    W, H = int(cw * D * 4), int(ch * D * 2)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(("dick", "rival1")):
        fa = P.figure(c, cast15.pose_for("flop", c), "ref")
        for i, n in enumerate(stages):
            x0, y0 = i * cw * D, r * ch * D
            o.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (x0, y0, cw * D, ch * D, BG if (i + r) % 2 else BG2))
            hx, hy = x0 + cw * D * 0.68, y0 + ch * D * 0.62
            s, f = _place(c, cast15.pose_for(n, c), "s%d%d" % (r, i), D, hx, hy)
            o.append(s)
            by = hy + fa["anchors"]["bar"][1] * D
            o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e03030" stroke-width="3" opacity="0.85"/>' % (x0 + 10, by, x0 + cw * D - 10, by))
            o.append(_under(x0 + cw * D / 2, y0 + ch * D - 8, "%d  %s (%s)" % (i + 1, n, c), 15))
    p = _write(_svgdoc(W, H, "".join(o)), W, H, "sec_strip")
    Image.open(p).convert("RGB").save(os.path.join(HERE, "flop_strip.jpg"), quality=90)
    print("wrote flop_strip.jpg", (W, H))


def sec_runs(D=80):
    items = []
    for ph in range(8):
        items.append(("run %.3f" % (ph / 8.0), "dick", cast15.run_curved("dick", ph / 8.0)))
    for ph in range(4):
        items.append(("clumsy run %.2f" % (ph / 4.0), "coach", cast15.coach_clumsy_run(ph / 4.0)))
    for fr in range(4):
        items.append(("laugh bob f%d" % fr, "coach", dict(cast15.pose_for("coach_laugh", "coach"), bob=cast15.laugh_bob(fr * 2.5))))
    cols = 8
    cw, ch = 3.2, 4.6
    rows = (len(items) + cols - 1) // cols
    W, H = int(cols * cw * D), int(rows * ch * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (n, c, p) in enumerate(items):
        r, cc = divmod(i, cols)
        x0, y0 = cc * cw * D, r * ch * D
        o.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (x0, y0, cw * D, ch * D, BG if (r + cc) % 2 else BG2))
        f = P.figure(c, p, "r%d" % i)
        gy = y0 + ch * D - 0.7 * D
        tx, ty = x0 + cw * D / 2 - f["anchors"]["feet"][0] * D, gy - f["feet_y"] * D
        o.append('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]))
        o.append(_under(x0 + cw * D / 2, y0 + ch * D - 8, n))
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_runs")


def sec_props(D=140):
    items = [("clipboard + coach", "coach", cast15.pose_for("clip", "coach")),
             ("presscam, flash 0", "photographer", dict(cast15.pose_for("photog_ready", "photographer"))),
             ("presscam, flash 1", "photographer", cast15.pose_for("photog_flash", "photographer")),
             ("medal (olympic vest)", "dick_olympic", cast15.pose_for("podium", "dick_olympic")),
             ("sawdust 1, hair chips", "dick", dict(cast15.pose_for("sit_up", "dick"))),
             ("buried (mound)", "coach", cast15.pose_for("coach_buried", "coach")),
             ("thumb", "boy2", cast15.pose_for("thumb", "boy2"))]
    cw, ch = 2.6, 3.4
    W, H = int(len(items) * cw * D), int(ch * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (n, c, p) in enumerate(items):
        x0 = i * cw * D
        o.append('<rect x="%.0f" width="%.0f" height="%d" fill="%s"/>' % (x0, cw * D, H, BG if i % 2 else BG2))
        s, f = _place(c, p, "q%d" % i, D, x0 + cw * D / 2 - 0.2 * D, 0.9 * D)
        o.append(s)
        o.append(_under(x0 + cw * D / 2, H - 8, n, 14))
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_props")


def sec_faces(D=130):
    members = ["dick", "coach", "boy1", "boy2", "boy3", "rival1", "rival2", "rival3", "official1", "official2", "photographer", "crowd1", "crowd2", "crowd3", "crowd4", "crowd5", "crowd6"]
    states = [("neutral", dict(expr="neutral")), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing", fx=["tears"])), ("shocked", dict(expr="shocked", mouth="o")),
              ("talk_b", dict(expr="talking", mouth="talk_b")), ("sawdust", dict(expr="worried", mouth="smile", sawdust=1.0, yaw=0.5))]
    cw, ch = 1.5, 1.6
    W, H = int(len(states) * cw * D) + 90, int(len(members) * ch * D) // 2 + 20
    cols2 = 2
    rows = (len(members) + 1) // 2
    W = int(len(states) * cw * D * 2)
    H = int(rows * ch * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(members):
        r, cc = divmod(i, 2)
        for j, (lab, p) in enumerate(states):
            x = cc * len(states) * cw * D + j * cw * D + cw * D / 2
            y = r * ch * D + 0.8 * D
            f = P.figure(n, dict(p), "f%d%d" % (i, j))
            o.append('<clipPath id="cp%d_%d"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (i, j, x - 0.72 * D, y - 1.0 * D, 1.44 * D, 1.62 * D))
            o.append('<g clip-path="url(#cp%d_%d)"><g transform="translate(%.2f %.2f) scale(%.3f)">%s</g></g>' % (i, j, x, y, D, f["svg"]))
        o.append(_under(cc * len(states) * cw * D + 60, r * ch * D + 14, n, 12))
    # mask the bodies: draw band backgrounds over the lower half of each cell
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_faces")


# ------------------------------------------------------------------ phone scale
def sec_phone(D=34):
    """characters and the key poses at phone scale: a 720-wide column layout, head D = 34 px (a wide shot)."""
    cells = [("dick", "stand"), ("coach", "stand"), ("boy1", "stand"), ("boy2", "stand"), ("boy3", "stand"), ("rival1", "stand"), ("rival2", "stand"), ("rival3", "stand"),
             ("official1", "official_stand"), ("official2", "official_stand"), ("photographer", "photog_ready"), ("crowd1", "sit_cheer"), ("crowd2", "sit_laugh"),
             ("crowd3", "sit_gape"), ("crowd4", "sit_point"), ("crowd5", "sit_cross"), ("crowd6", "sit_cheer"), ("coach_stands", "coach_shout"),
             ("dick", "flop"), ("dick", "straddle_a"), ("boy1", "straddle_b"), ("rival1", "flop"), ("dick", "takeoff"), ("dick", "plant"), ("dick", "land_back"),
             ("dick", "sit_up"), ("dick_olympic", "podium"), ("coach", "coach_laugh"), ("coach", "coach_buried"), ("dick_olympic", "lie_hands_face"), ("boy1", "sit_read"), ("rival1", "walk_dejected"), ("boy1", "stand"),
             ("coach", "coach_neck"), ("coach", "coach_point")]
    cols = 8
    cw, ch = 3.3 * D, 5.0 * D
    rows = (len(cells) + cols - 1) // cols
    W, H = int(cols * cw), int(rows * ch)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (c, n) in enumerate(cells):
        r, cc = divmod(i, cols)
        x0, y0 = cc * cw, r * ch
        o.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (x0, y0, cw, ch, BG if (r + cc) % 2 else BG2))
        p = cast15.pose_for(n, c) if n in cast15.POSE_FUNCS else dict(expr="neutral", yaw=0.3)
        if n == "stand":
            p = dict(expr="neutral", yaw=0.0)
        lying = n.startswith(("flop", "straddle", "land", "lie"))
        hx, hy = (x0 + cw * 0.66, y0 + ch * 0.52) if lying else ((x0 + cw * 0.2, y0 + ch * 0.3) if n == "sit_up" else (x0 + cw * 0.5, y0 + ch * 0.22))
        s, f = _place(c, p, "ph%d" % i, D, hx, hy)
        o.append(s)
        o.append('<text x="%.0f" y="%.0f" font-family="DejaVu Sans, sans-serif" font-size="9" fill="#222">%s</text>' % (x0 + 3, y0 + ch - 4, (c + " " + n)[:22]))
    return _write(_svgdoc(W, H, "".join(o)), W, H, "sec_phone")


def build_sheet():
    from PIL import Image, ImageDraw
    secs = [("heights", sec_heights()), ("compare", sec_compare()), ("poses", sec_poses()), ("runs", sec_runs()), ("props", sec_props()), ("faces", sec_faces())]
    ims = [(n, Image.open(p).convert("RGB")) for n, p in secs]
    Wm = max(im.size[0] for _, im in ims)
    Ht = sum(im.size[1] + 36 for _, im in ims)
    sheet = Image.new("RGB", (Wm, Ht), "#8a867e")
    d = ImageDraw.Draw(sheet)
    y = 0
    titles = {"heights": "cast15: front + 3/4, head D = 100 px, heights head top to soles in D",
              "compare": "FLOP (curved bridge, belly up) sequence, head D = 75 px",
              "poses": "pose presets (canonical right-facing; red line = bar anchor, green = apex)",
              "runs": "cycles: curved run (dick), clumsy run (coach), laugh bob (0.06 D at 3 Hz)",
              "props": "props and pose keys", "faces": "faces: neutral / happy / laughing / shocked / talk_b / sawdust"}
    for n, im in ims:
        d.text((8, y + 10), titles[n], fill="#ffffff")
        y += 36
        sheet.paste(im, (0, y))
        y += im.size[1]
    out = os.path.join(HERE, "sheet.jpg")
    sheet.save(out, quality=88)
    print("wrote", out, sheet.size)
    build_strip()
    ph = Image.open(sec_phone()).convert("RGB")
    ph.save(os.path.join(HERE, "sheet_phone.jpg"), quality=90)
    print("wrote sheet_phone.jpg", ph.size)


# ------------------------------------------------------------------ canvas
def all_pose_set():
    out = []
    for c in cast15.ALL15:
        for n in cast15.POSE_NAMES:
            for fc in (1, -1):
                out.append((c, n, cast15.pose_for(n, c, facing=fc)))
        for i in range(16):
            for fc in (1, -1):
                out.append((c, "run%d" % i, cast15.run_curved(c, i / 16.0, fc)))
    return out


def canvas_check():
    bad = 0
    worst = {}
    for c, n, p in all_pose_set():
        f = P.figure(c, p, "k")
        fx = f["anchors"]["feet"][0]
        b = f["bbox"]
        rel = (b[0] - fx, b[1] - f["feet_y"], b[2] - fx, b[3] - f["feet_y"])
        std = cast15.CANVAS15[c]
        wide = cast15.CANVAS15_WIDE
        ok_std = rel[0] >= std[0] and rel[1] >= std[1] and rel[2] <= std[2] and rel[3] <= std[3]
        ok_wide = rel[0] >= wide[0] and rel[1] >= wide[1] and rel[2] <= wide[2] and rel[3] <= wide[3]
        key = (c, n.rstrip("0123456789"))
        if not ok_wide:
            bad += 1
            print("OUTSIDE WIDE canvas:", c, n, tuple(round(v, 2) for v in rel))
        w = worst.setdefault(c, [9, 9, -9, -9])
        w[0], w[1], w[2], w[3] = min(w[0], rel[0]), min(w[1], rel[1]), max(w[2], rel[2]), max(w[3], rel[3])
    for c, w in worst.items():
        print("%-14s union rel feet: %s  standard canvas %s" % (c, tuple(round(v, 2) for v in w), cast15.CANVAS15[c]))
    print("canvas: %d poses outside the wide canvas" % bad)
    return bad


# ------------------------------------------------------------------ robustness
def robust():
    rnd = random.Random(15)
    keys = dict(body_lean=lambda: rnd.choice([-1e9, 1e9, float("nan"), float("inf"), "x", None, rnd.uniform(-300, 300)]),
                hdx2=lambda: rnd.choice([float("nan"), 1e9, "q", rnd.uniform(-9, 9)]), hdy2=lambda: rnd.choice([float("nan"), -1e9, [], rnd.uniform(-9, 9)]),
                roll2=lambda: rnd.choice([float("nan"), 1e9, {}, rnd.uniform(-400, 400)]), sawdust=lambda: rnd.choice([-5, 5, "a", None, float("nan")]),
                buried=lambda: rnd.choice([0, 1, 7, "x", None]), buried_y=lambda: rnd.choice([float("nan"), 1e9, -1e9, 0.5]), buried_w=lambda: rnd.choice([0, 1e9, "a", 2]),
                flash=lambda: rnd.choice([-1, 2, "z", None, float("nan"), 0.5]), medal=lambda: rnd.choice([0, 1, "x", None]), bob=lambda: rnd.choice([1e9, float("nan"), -3, 0.05]),
                thumb_r=lambda: rnd.choice([0, 1, "x"]), thumb_l=lambda: rnd.choice([0, 1, None]), thumb_angle=lambda: rnd.choice([float("nan"), 1e9, 45]),
                t=lambda: rnd.choice([float("nan"), 1e9, 0.3]), mirror=lambda: rnd.choice([True, False, 1, None]),
                yaw=lambda: rnd.choice([-5, 5, float("nan"), 0.3]), prop_r=lambda: rnd.choice([None, "clipboard", "presscam", {"type": "presscam", "angle": 1e9, "scale": -3}, "bogus"]),
                prop_l=lambda: rnd.choice([None, "clipboard", "presscam"]))
    n = fails = 0
    for c in list(cast15.ALL15):
        for i in range(120):
            p = {}
            for k in rnd.sample(list(keys), rnd.randint(1, 8)):
                p[k] = keys[k]()
            try:
                f = P.figure(c, p, "z")
                assert "<svg" not in f["svg"][:5]
                for v in f["bbox"]:
                    assert math.isfinite(v), "bbox"
                for kk, v in f["anchors"].items():
                    assert math.isfinite(v[0]) and math.isfinite(v[1]), kk
            except Exception as e:
                fails += 1
                print("FAIL", c, p, repr(e))
            n += 1
    for c in ("dick", "coach"):
        for nm in cast15.POSE_NAMES:
            a = P.figure(c, cast15.pose_for(nm, c), "d")["svg"]
            b = P.figure(c, cast15.pose_for(nm, c), "d")["svg"]
            n += 1
            if a != b:
                fails += 1
                print("NOT DETERMINISTIC", c, nm)
    print("robust garbage + determinism: %d checks, %d failed" % (n, fails))
    # regression: hero / boss and every earlier story pose must be byte-identical to what cast10 alone draws
    code = ("import sys,hashlib;sys.path.insert(0,%r);import cast10,puppet as P;h=hashlib.md5()\n"
            "for n,(c,p) in sorted(P.STORY.items()):\n h.update(P.figure(c,p,'r')['svg'].encode())\n"
            "for c in ('hero','boss','admiral','painter10','sailor_a','lin','general'):\n h.update(P.figure(c,dict(yaw=0.4,expr='happy'),'r')['svg'].encode())\n"
            "print(h.hexdigest())" % os.path.join(cast15.PROJ, "v3", "cast10"))
    base = subprocess.run([sys.executable, "-c", code], stdout=subprocess.PIPE, universal_newlines=True).stdout.strip()
    h = hashlib.md5()
    for nme, (c, p) in sorted(P.STORY.items()):
        if nme in cast15.STORY15:
            continue
        h.update(P.figure(c, p, "r")["svg"].encode())
    for c in ("hero", "boss", "admiral", "painter10", "sailor_a", "lin", "general"):
        h.update(P.figure(c, dict(yaw=0.4, expr="happy"), "r")["svg"].encode())
    print("cast10 regression:", "identical" if h.hexdigest() == base else "DIFFERENT (%s vs %s)" % (h.hexdigest(), base))
    if h.hexdigest() != base:
        fails += 1
    return fails


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "all"
    t0 = __import__("time").time()
    rc = 0
    if cmd in ("all", "sheet"):
        build_sheet()
    if cmd in ("all", "canvas"):
        rc += canvas_check()
    if cmd in ("all", "robust"):
        rc += robust()
    print("done in %.1f s" % (__import__("time").time() - t0))
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
