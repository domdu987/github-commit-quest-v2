#!/usr/bin/env python3
"""test_cast12.py -- QA for cast12.py (film 12: the walking umbrella, London 1750s).

    python3 test_cast12.py            regression + canvas + head_flip + garbage robustness, prints ALL OK (about 40 s); then writes sheet.jpg
    python3 test_cast12.py sheet      sheet.jpg (heights, key poses, faces, props, mud / egg / soaked) and sheet_all_poses.jpg (every STORY12 pose)
    python3 test_cast12.py canvas     sprite canvas check (pose range per member against cast12.CANVAS12)
    python3 test_cast12.py regress    earlier STORY poses and earlier members must draw BYTE-IDENTICAL before and after cast12 is imported
    python3 test_cast12.py robust     garbage pose keys on the new members + v2 test_puppet.py --quick on them (slow)
Section images are kept in tmp/ (sec_*.png).
"""
import hashlib
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "cast10"))

# ---- snapshot of every earlier drawing BEFORE cast12 is imported (the regression baseline)
import cast10  # noqa: E402
import puppet as P  # noqa: E402


def _generic_poses(name):
    out = [dict(), dict(yaw=0.6, expr="smug", arm_r="point", arm_l="akimbo"), dict(yaw=-0.5, mirror=True, expr="laughing", fx=["tears", "sweat"], legs="wide", squash=(0.9, 1.1)),
           dict(arm_r="reach_up", prop_r="pencil", legs="crouch", tint="#fbdaf7", ink="#1e142e")]
    out += [cast10.cycle(name, i / 8.0, m) for m in ("walk", "run") for i in range(4)]
    return out


def _snapshot():
    snap = {}
    for n, (c, p) in sorted(P.STORY.items()):
        snap["story:" + n] = hashlib.sha1(P.figure(c, p, "r")["svg"].encode()).hexdigest()
    for c in sorted(P.CAST):
        for i, p in enumerate(_generic_poses(c)):
            snap["cast:%s:%d" % (c, i)] = hashlib.sha1(P.figure(c, p, "r")["svg"].encode()).hexdigest()
    return snap


BEFORE = _snapshot()
BEFORE_CAST = set(P.CAST)
import cast12  # noqa: E402

LABEL = P._label
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
BG, BG2, GROUND = "#d4cfc6", "#c9c3b8", "#aaa498"          # neutral warm greys
LINEUP = cast12.NEW12
REF = ("admiral",)                                          # film 10, for scale

LINEUP_POSE = {
    "hanway": dict(expr="smug", pitch=-0.3, arm_r=dict(hand=(0.66, 0.60), bend=0.5), prop_r=dict(type="umbrella_black_closed", angle=96, scale=0.85)),
    "coachman": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
    "coachman_b": dict(expr="smug", arm_r="akimbo", arm_l="akimbo"),
    "coachman_c": dict(expr="grinning", arm_r="akimbo", arm_l="akimbo"),
    "crowd_man_a": dict(expr="neutral"), "crowd_man_b": dict(expr="neutral"), "crowd_man_c": dict(expr="unimpressed"), "crowd_man_d": dict(expr="smug"),
    "crowd_woman_a": dict(expr="happy"), "crowd_woman_b": dict(expr="neutral"), "passenger_a": dict(expr="neutral"), "passenger_b": dict(expr="happy"),
    "admiral": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"),
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


def sec_heights(D=100):
    members = LINEUP + REF
    colw = int(2.5 * D)
    W = colw * len(members) + 20
    top = int(1.3 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GROUND)]
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), BG2 if i % 2 else BG, 1.0 if c not in REF else 0.6))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.30 + 0.42 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#444" stroke-width="1.2" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c + ("  (film 10, scale ref)" if c in REF else ""), 14))
    o.append(LABEL(10, 26, "cast12: front / 3-4, head D = %d px; head top to soles in D (hat top in brackets).  film 10 admiral at right for scale" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


KEY = ("hanway_walk_umbrella", "hanway_stroll_smug", "hanway_calm_front", "hanway_cabbage_flinch", "hanway_egg_tilt", "hanway_mud_splash", "hanway_mud_deadpan", "hanway_walk_closed",
       "hanway_smile_walk",
       "coachman_laugh", "coachman_point_mock", "coachman_boast", "coachman_shout", "coachman_gloat", "coachman_count_coins", "coachman_count_coins_sky", "coachman_grin_drop",
       "coachman_throw_windup", "coachman_throw_release", "coachman_box_point_mock", "coachman_box_laugh", "coachman_sulk_under_pink_umbrella",
       "coachman_b_laugh", "coachman_b_point_laugh", "coachman_b_throw_windup", "coachman_b_throw_release", "coachman_b_box_nod",
       "coachman_c_laugh", "coachman_c_glare", "coachman_c_throw_windup", "coachman_c_throw_release", "coachman_c_box_roar",
       "crowd_man_a_walk_hat", "crowd_man_a_walk_soaked", "crowd_man_a_point_laugh", "crowd_man_a_rush", "crowd_man_a_push", "crowd_man_a_wring_wig",
       "crowd_man_a_open_1", "crowd_man_a_open_2", "crowd_man_a_open_3", "crowd_man_b_walk_hat", "crowd_man_b_rush", "crowd_man_c_walk_soaked", "crowd_man_c_point_laugh",
       "crowd_man_d_walk_hat", "crowd_man_d_push",
       "crowd_woman_a_walk_umbrella", "crowd_woman_a_dry_pass", "crowd_woman_a_rush", "crowd_woman_b_walk_umbrella", "crowd_woman_b_point_laugh", "crowd_woman_b_push",
       "passenger_a_seated", "passenger_a_peek", "passenger_b_seated", "passenger_b_laugh")
LIPSYNC = ("coachman_point_mock", "coachman_boast", "coachman_shout", "coachman_box_point_mock", "coachman_box_boast", "coachman_box_shout")


def _with_box(n, pose):
    if "_box_" in n or "sulk" in n or n.startswith("passenger"):
        return dict(pose, coach_box=1)
    return pose


def sec_poses(names, D=64, cols=9):
    cw, ch = int(4.5 * D), int(6.2 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = cast12.STORY12[n]
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if (i + i // cols) % 2 else BG))
        ground = y0 + ch - int(0.95 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.10 * D), cw, int(0.25 * D), GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.6 * D), x0, y0, cw, ch - int(0.6 * D)))
        g, f = _fig(cast, dict(_with_box(n, pose), t=0.3), "p%d" % i, D, x0 + cw * 0.46, ground)
        o.append(g + "</svg>")
        if n in LIPSYNC:
            o.append(LABEL(x0 + 6, y0 + 16, "lip-sync", 12))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.22 * D), n, 11))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
          ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing")), ("grinning", dict(expr="grinning")),
          ("smug", dict(expr="smug")), ("angry", dict(expr="angry")), ("shouting", dict(expr="shouting")), ("shocked", dict(expr="shocked")), ("worried", dict(expr="worried")),
          ("sad", dict(expr="sad")), ("mud", dict(expr="shocked", mud=1.0)), ("soaked", dict(expr="unimpressed", soaked=1.0)))


def sec_faces(D=86):
    cw, ch = int(1.45 * D), int(2.0 * D)
    W, H = 130 + cw * len(STATES), ch * len(LINEUP) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(LINEUP):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 14))
        for j, (lab, extra) in enumerate(STATES):
            pose = dict(yaw=0.3, **extra)
            f = P.figure(c, pose, "f%d_%d" % (r, j))
            cx, cy = 130 + j * cw + cw / 2, y0 + ch * 0.47
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (130 + j * cw, y0, cw, ch - 26, 130 + j * cw, y0, cw, ch - 26, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 8, lab, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=150):
    items = []

    def umb(label, kind, o_, sc=0.42, **kw):
        items.append((label, '<g transform="translate(0 1.0)">%s</g>' % cast12.umbrella_svg("u%d" % len(items), kind, o_, **kw), sc))
    umb("umbrella_black open", "black", 1.0)
    umb("black half open", "black", 0.5)
    umb("black closed (furled)", "black", 0.0)
    umb("black + egg splat", "black", 1.0, egg=1.0)
    umb("black + cabbage leaf", "black", 1.0, leaf=1)
    umb("umbrella_pink open (lace)", "pink", 1.0)
    umb("pink half open", "pink", 0.5)
    umb("pink closed", "pink", 0.0)
    umb("small: maroon", "maroon", 1.0)
    umb("small: green", "green", 1.0)
    items.append(("whip", '<g transform="translate(-0.9 0)">%s</g>' % cast12.whip_svg("wh"), 0.46))
    items.append(("cabbage", cast12.cabbage_svg("cb", 20), 1.8))
    items.append(("egg", cast12.egg_svg("eg", 15), 2.6))
    items.append(("egg splat", cast12.egg_splat_svg("es", 0.22), 1.6))
    items.append(("coin purse (open)", '<g transform="translate(0 -0.2)">%s</g>' % cast12.purse_svg("pu", 1.0), 1.5))
    items.append(("coin", cast12.coin_svg("co", 0.14), 3.0))
    items.append(("coach box (coach_box=1)", '<g transform="translate(0 -0.3)">%s</g>' % cast12.coach_box_svg("cx"), 0.34))
    cw, ch = int(1.3 * D), int(1.45 * D)
    cols = 9
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, svg, sc) in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 30, x0, y0, cw, ch - 30, x0 + cw / 2, y0 + ch * 0.52, D * sc, svg))
        o.append(_under(x0 + cw / 2, y0 + ch - 10, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_variants(D=110):
    """mud levels, egg splat, soaked, tint variants of the crowd, seated coachman with the box, all on the neutral ground."""
    items = []
    h = cast12.STORY12["hanway_mud_deadpan"][1]
    for lv in (0.0, 0.35, 0.7, 1.0):
        items.append(("hanway mud=%.2f" % lv, "hanway", dict(h, mud=lv)))
    e = cast12.STORY12["hanway_egg_tilt"][1]
    items.append(("egg_splat 0.4", "hanway", dict(e, egg_splat=0.4)))
    items.append(("egg_splat 1.0", "hanway", dict(e, egg_splat=1.0)))
    for c, tn in (("crowd_man_a", "soaked 0"), ("crowd_man_a", "soaked 0.5"), ("crowd_man_a", "soaked 1.0")):
        items.append((c + " " + tn, c, dict(expr="unimpressed", soaked=float(tn.split()[1]), t=0.3)))
    for c in ("crowd_man_a", "crowd_man_b", "crowd_man_c", "crowd_man_d", "crowd_woman_a", "crowd_woman_b"):
        items.append((c + " dusk tint", c, dict(expr="neutral", tint="#c8c4f0", ink="#1e142e")))
    cw, ch = int(3.0 * D), int(5.6 * D)
    cols = 8
    rows = (len(items) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, (lab, c, p) in enumerate(items):
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        ground = y0 + ch - int(0.7 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.1 * D), cw, int(0.3 * D) + ch, GROUND))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.4 * D), x0, y0, cw, ch - int(0.4 * D)))
        g, f = _fig(c, p, "v%d" % i, D, x0 + cw * 0.5, ground)
        o.append(g + "</svg>")
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.2 * D), lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def _stack(parts, out_name, scale_w=None):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    ims = [i if i.width == W else i.resize((W, int(i.height * W / i.width)), Image.LANCZOS) for i in ims]
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    out = Image.new("RGB", (W, H), (60, 58, 60))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    if scale_w and W > scale_w:
        out = out.resize((scale_w, int(H * scale_w / W)), Image.LANCZOS)
    p = os.path.join(HERE, out_name)
    out.save(p, quality=88)
    print("wrote %s (%dx%d)" % (p, out.width, out.height))
    return p


def build_sheet():
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("poses", lambda: sec_poses(list(KEY))), ("faces", sec_faces), ("props", sec_props), ("variants", sec_variants)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    _stack(parts, "sheet.jpg")
    svg, w, h = sec_poses(list(cast12.STORY12), D=40, cols=14)
    _stack([_write(svg, w, h, "sec_allposes")], "sheet_all_poses.jpg")
    print("sheets in %.1f s" % (time.time() - t0))


# ============================================================================= checks
def _range(name, poses):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for p in poses:
        f = P.figure(name, p, "c")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


UMBS = ("umbrella_black", "umbrella_black_closed", "umbrella_pink", "umbrella_small", "whip", "cabbage12", "purse", "tricorn_held")


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None, "cabbage12", "purse", dict(type="whip", angle=-30)) + ((dict(type="umbrella_black", angle=-100),) if a in ("down", "hip", "akimbo", "forward", "point", "behind") else ()):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(yaw=1.2), dict(yaw=-1.2), dict(mud=1.0, soaked=1.0, fx=["sweat", "tears"], t=0.4)]
    poses += [p for (c, p) in cast12.STORY12.values() if c == name and not p.get("coach_box")]
    poses += [dict(p, mirror=True) for (c, p) in cast12.STORY12.values() if c == name]
    for m in cast12.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast12.cycle(name, i / 16.0, m, facing=fc))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-14s %-6s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                         "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast12.NEW12:
        bad += _check("", name, member_poses(name), cast12.CANVAS12[name])
    for name, c in cast12.CANVAS12_BOX.items():
        lp = [dict(p, coach_box=1) for (cc, p) in cast12.STORY12.values() if cc == name and p.get("legs") and isinstance(p["legs"], dict) and "foot_r" in p["legs"]]
        lp += [dict(p, mirror=True) for p in lp]
        bad += _check("BOX", name, lp, c)
    probs = 0
    for n, (c, p) in cast12.STORY12.items():
        a = P.figure(c, p, "a")
        q = dict(p, mirror=not p.get("mirror", False))
        b = P.figure(c, q, "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("head_flip: %d poses checked, %d problems" % (len(cast12.STORY12), probs))
    return bad + probs


def regress():
    """every earlier STORY pose and every earlier CAST member must give byte-identical SVG after cast12 is imported."""
    after = _snapshot()
    bad = [k for k, v in BEFORE.items() if after.get(k) != v]
    n_story = sum(1 for k in BEFORE if k.startswith("story:"))
    print("regression: %d earlier STORY poses + %d generic poses on %d earlier members: %d differ (STORY10 included: %d)"
          % (n_story, len(BEFORE) - n_story, len(BEFORE_CAST), len(bad), sum(1 for k in BEFORE if k.startswith("story:") and k[6:] in cast10.STORY10)))
    for k in bad[:10]:
        print("  DIFFERS", k)
    # the new members and poses are deterministic and uid-safe
    a = P.figure("hanway", cast12.STORY12["hanway_mud_splash"][1], "d")["svg"]
    b = P.figure("hanway", cast12.STORY12["hanway_mud_splash"][1], "d")["svg"]
    det = a == b
    c = P.figure("coachman", cast12.STORY12["coachman_sulk_under_pink_umbrella"][1], "x")["svg"]
    ids = len(set(__import__("re").findall(r'id="([^"]+)"', c))) == len(__import__("re").findall(r'id="([^"]+)"', c))
    print("deterministic %s, unique ids %s" % (det, ids))
    new_keys = [k for k in cast12.NEW12 if k in BEFORE_CAST]
    if new_keys:
        print("NEW KEY COLLIDES WITH EARLIER CAST:", new_keys)
    names = [n for n in cast12.STORY12 if n in {k[6:] for k in BEFORE if k.startswith("story:")}]
    if names:
        print("STORY12 NAME COLLIDES:", names[:5])
    return len(bad) + (0 if det and ids else 1) + len(new_keys) + len(names)


def robust(quick=False):
    import random
    rnd = random.Random(12)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("umb_open", "umb_col", "egg_splat", "leaf_stick", "mud", "soaked", "hat_off", "wig_off", "coach_box", "box_w", "whip_t", "purse_open", "t", "squash", "mirror", "expr", "tint")
    t0 = time.time()
    for name in cast12.NEW12:
        for i in range(120 if quick else 400):
            p = {}
            for kk in keys:
                if rnd.random() < 0.5:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast12.NEW_PROPS12)
            p["prop_l"] = rnd.choice((None,) + cast12.NEW_PROPS12)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    print("cast12 pose keys + garbage: %d ok, %d failed, %.1f s" % (n, fail, time.time() - t0))
    rc = 0
    if not quick:
        sys.path.insert(0, os.path.join(cast12.PROJ, "v2", "puppet"))
        import test_puppet as T
        T.CASTS = cast12.NEW12
        rc = T.main(["--quick"]) or 0
    return fail + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    bad = 0
    if what in ("all", "regress"):
        bad += regress()
    if what in ("all", "canvas"):
        bad += canvas_check()
    if what in ("all", "robust"):
        bad += robust(quick=(what == "all"))
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "regress", "canvas", "robust"):
        print("ALL OK" if bad == 0 else "FAILED (%d problems)" % bad)
