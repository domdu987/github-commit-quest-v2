#!/usr/bin/env python3
"""test_cast22.py -- QA for cast22.py (film 22: Harry Beck's Underground diagram, London 1931-33).

    python3 test_cast22.py            everything below, prints ALL OK when every check passes
    python3 test_cast22.py sheet      sheet.jpg: heights; every STORY22 pose on a mid-grey AND a dark-blue ground (rim on the blue);
                                      18 face states per member; the props and set pieces on both grounds; the 16-person crowd
    python3 test_cast22.py canvas     sprite canvas check (pose range per member against cast22.CANVAS22) + head_flip
    python3 test_cast22.py identity   earlier casts unchanged: every puppet.STORY pose and every older CAST member draws byte-identical
                                      SVG with and without cast22 (a subprocess imports cast10 only and hashes the same set)
    python3 test_cast22.py robust     pose-key garbage on the new members, determinism, v2 test_puppet.py --quick on the new names
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
import cast22  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast22.PROJ
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
GREY, GREY_G = "#8e8b86", "#76726c"
NAVY, NAVY_G = "#16205a", "#0d1440"
RIM = "#a8bcff"
MEMBERS = cast22.NEW22
SCALE_REF = ("admiral", "painter10")
LINEUP_POSE = {
    "beck": dict(expr="neutral"), "official": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"), "clerk_a": dict(expr="neutral"),
    "clerk_b": dict(expr="happy"), "clerk_c": dict(expr="happy"), "pass_man": dict(expr="neutral"), "pass_woman": dict(expr="happy"),
    "pass_child": dict(expr="happy"), "old_gent": dict(expr="squint"), "porter": dict(expr="happy"),
    "admiral": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo"), "painter10": dict(expr="neutral"),
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


def _under(x, y, text, size=13):
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#0c0c14" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>'
            % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


def _fig(cast, pose, uid, D, x, y, shadow=0.9, shade="#05050c"):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s", shade, 0.55)) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def sec_heights(D=92):
    members = MEMBERS + SCALE_REF
    colw = int(2.5 * D)
    W = colw * len(members) + 20
    top = int(1.0 * D)
    ground = top + int(3.9 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREY), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.12 * D), W, H, GREY_G)]
    for i, c in enumerate(members):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x0, colw, ground - int(0.12 * D), "#9a9690" if i % 2 else GREY, 1.0))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        for j, yw in enumerate((0.0, 0.5)):
            g, f = _fig(c, dict(LINEUP_POSE[c], yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 8, int(yt) - 6, "%.2f D" % ht, 13))
        o.append(_under(x0 + colw / 2, ground + int(0.55 * D), c + ("  (cast10, scale ref)" if c in SCALE_REF else ""), 15))
    o.append(LABEL(10, 24, "cast22: front / 3-4, head D = %d px; heads top to soles in D; admiral + painter10 of film 10 at right for scale" % D, 15))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=64, pairs=5):
    names = list(cast22.STORY22)
    cw, ch = int(3.9 * D), int(5.2 * D)
    rows = (len(names) + pairs - 1) // pairs
    W, H = 2 * cw * pairs, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREY)]
    for i, n in enumerate(names):
        cast, pose = cast22.STORY22[n]
        px, py = (i % pairs) * 2 * cw, (i // pairs) * ch
        for side in (0, 1):
            x0 = px + side * cw
            bg, gg = (GREY, GREY_G) if side == 0 else (NAVY, NAVY_G)
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, py, cw, ch, bg))
            ground = py + ch - int(0.95 * D)
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground, cw, ch, gg))
            p = dict(pose, t=0.3)
            if side:
                p.update(rim=RIM, rim_w=0.02, rim_opacity=0.85)
            gx = x0 + cw * 0.36
            g, f = _fig(cast, p, "p%d_%d" % (i, side), D, gx, ground, shade="#02020a" if side else "#3a3630")
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">%s</svg>' % (x0, py, cw, ch, x0, py, cw, ch, g))
            if cast22.STORY22_META.get(n.rsplit("_", 1)[0] if n not in cast22.STORY22_META else n, {}).get("lipsync") or cast22.STORY22_META.get(n, {}).get("lipsync"):
                o.append(LABEL(x0 + 6, py + 34, "lip-sync", 12))
            o.append(_under(x0 + cw / 2, py + ch - int(0.30 * D), n, 12))
    return _svgdoc(W, H, "".join(o)), W, H


STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")),
          ("flat", dict(mouth="flat")), ("blink 1", dict(blink=1)), ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")),
          ("laughing", dict(expr="laughing", fx=["tears"])), ("grinning", dict(expr="grinning")), ("smug", dict(expr="smug")),
          ("sneer", dict(expr="unimpressed", mouth="smirk")), ("shocked", dict(expr="shocked", mouth=("open", 0.16, 0.18))), ("worried", dict(expr="worried", sweat=1.0)),
          ("squint", dict(expr="squint")), ("sad", dict(expr="sad", pitch=0.5)), ("red face", dict(expr="laughing", flush=1.0)), ("puffed", dict(expr="worried", mouth="flat", puff=1.0)))


def sec_faces(D=84):
    cw, ch = int(1.40 * D), int(1.8 * D)
    W, H = 110 + cw * len(STATES), ch * len(MEMBERS) + 10
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, GREY)]
    for r, c in enumerate(MEMBERS):
        y0 = 5 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, "#9a9690" if r % 2 else GREY))
        o.append(LABEL(6, y0 + ch // 2, c, 14))
        for j, (lab, extra) in enumerate(STATES):
            f = P.figure(c, dict(yaw=0.3, **extra), "f%d_%d" % (r, j))
            cx, cy = 110 + j * cw + cw / 2, y0 + ch * 0.46
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (110 + j * cw, y0, cw, ch - 24, 110 + j * cw, y0, cw, ch - 24, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 7, lab, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_props(D=190):
    items = []
    for kind, sc in (("ruler", 0.9), ("pen", 2.0), ("set_square", 1.0), ("t_square", 0.75), ("roll", 1.2), ("sheet", 0.8), ("stamp", 2.0), ("pocketmap", 1.8),
                     ("pocketmap_open", 1.2), ("fork", 1.5), ("fork_map", 1.2), ("knife", 1.5), ("letter", 1.5), ("circuit", 0.9), ("daily", 1.5), ("briefcase", 1.6),
                     ("umbrella", 0.7), ("handbag", 1.8), ("teacup", 3.0), ("magnifier", 1.6), ("handtruck", 0.6)):
        cxo = {"ruler": -0.25, "pen": -0.1, "set_square": -0.25, "t_square": -0.5, "roll": 0.0, "sheet": -0.48, "stamp": -0.1, "pocketmap": -0.17, "pocketmap_open": -0.32,
               "fork": -0.2, "fork_map": -0.25, "knife": -0.15, "letter": -0.24, "circuit": -0.42, "daily": -0.27, "briefcase": 0, "umbrella": -0.45, "handbag": 0, "teacup": 0.1,
               "magnifier": -0.25, "handtruck": -0.4}[kind]
        cyo = {"briefcase": -0.2, "handbag": -0.2, "teacup": 0.1, "handtruck": -0.6, "set_square": 0.15}.get(kind, 0.0)
        items.append((kind, '<g transform="translate(%.3f %.3f)">%s</g>' % (cxo, cyo, cast22.prop_svg(kind, "q" + kind)), sc))
    items.append(("board (board=1)", '<g transform="translate(-0.77 0)">%s</g>' % cast22.board_svg("bdx"), 0.55))
    items.append(("desk (desk=1)", '<g transform="translate(-0.8 -0.5)">%s</g>' % cast22.desk_svg("dkx", 1.6, 1.0, 1.0), 0.55))
    items.append(("typewriter", cast22.typewriter_svg("twx"), 1.2))
    items.append(("pillar (pillar=1)", '<g transform="translate(-0.25 -0.8)">%s</g>' % cast22.pillar_svg("pix", 0.5, 1.6), 0.8))
    cw, ch = int(1.35 * D), int(1.35 * D)
    per = 11
    rows = (len(items) + per - 1) // per
    W, H = cw * per, ch * rows * 2
    o = ['<rect width="%d" height="%d" fill="%s"/><rect y="%d" width="%d" height="%d" fill="%s"/>' % (W, H // 2, GREY, H // 2, W, H // 2, NAVY)]
    for bgi, (bg, gg) in enumerate(((GREY, GREY_G), (NAVY, NAVY_G))):
        for i, (lab, svg, sc) in enumerate(items):
            x0, y0 = (i % per) * cw, (bgi * rows + i // per) * ch
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, bg if (i % 2 == 0) else gg))
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (x0, y0, cw, ch - 24, x0, y0, cw, ch - 24, x0 + cw / 2, y0 + ch * 0.44, D * sc, svg))
            o.append(_under(x0 + cw / 2, y0 + ch - 8, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_crowd(D=70):
    n = len(cast22.CROWD_NAMES)
    cw, ch = int(2.5 * D), int(4.7 * D)
    per = 16
    W, H = cw * per, ch * 2
    o = ['<rect width="%d" height="%d" fill="%s"/><rect y="%d" width="%d" height="%d" fill="%s"/>' % (W, H, GREY, ch, W, ch, NAVY)]
    for i in range(n):
        name, pose = cast22.crowd_member(i, "pass_walk")
        for r in (0, 1):
            pz = dict(pose)
            if r:
                pz.update(rim=RIM, rim_w=0.02, rim_opacity=0.85)
            g, f = _fig(name, pz, "c%d_%d" % (i, r), D, i * cw + cw / 2, r * ch + int(4.0 * D), shade="#02020a" if r else "#3a3630")
            o.append(g)
    o.append(LABEL(8, 22, "crowd_member(i, 'pass_walk'): 16 variants (6 men, 7 women, 3 children) -- recoloured coats, hats, waistcoats, ties, hair, props", 15))
    return _svgdoc(W, H, "".join(o)), W, H


def build_sheet():
    from PIL import Image
    t0 = time.time()
    parts = []
    for name, fn in (("heights", sec_heights), ("poses", sec_poses), ("faces", sec_faces), ("props", sec_props), ("crowd", sec_crowd)):
        svg, w, h = fn()
        parts.append(_write(svg, w, h, "sec_" + name))
    ims = [Image.open(p).convert("RGB") for p in parts]
    W = max(i.width for i in ims)
    H = sum(i.height for i in ims) + 8 * (len(ims) - 1)
    out = Image.new("RGB", (W, H), (30, 30, 36))
    y = 0
    for i in ims:
        out.paste(i, (0, y))
        y += i.height + 8
    p = os.path.join(HERE, "sheet.jpg")
    out.save(p, quality=90)
    print("wrote %s (%dx%d) in %.1f s" % (p, W, H, time.time() - t0))
    return p


# ----------------------------------------------------------------------------- canvas
def _range(name, poses):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for p in poses:
        f = P.figure(name, p, "c")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


SETPOSE = ("board", "desk", "typewriter", "pillar")


def member_poses(name):
    C = P.CAST[name]
    poses = [{}]
    for a in sorted(P.ARM_PRESETS[C["build"]]):
        for pr in (None, "briefcase", "umbrella", "sheet") + (("handtruck",) if name == "porter" else ()):
            poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
            poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
    poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep", sweat=1.0, puff=1.0, flush=1.0), dict(yaw=1.2), dict(yaw=-1.2)]
    poses += [p for (c, p) in cast22.STORY22.values() if c == name and not any(p.get(k) for k in SETPOSE)]
    for m in cast22.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                poses.append(cast22.cycle(name, i / 16.0, m, facing=fc))
    return poses


def _check(label, name, poses, c):
    x0, y0, x1, y1 = _range(name, poses)
    clipped = x0 < c[0] or y0 - 0.32 < c[1] or x1 > c[2] or y1 > c[3]
    hw = math.ceil(max(-x0, x1) * 16) / 16.0
    sugg = (-hw, math.floor((y0 - 0.33) * 16) / 16.0, hw, math.ceil(max(y1, 0.12) * 16) / 16.0)
    print("%-12s %-6s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s%s" % (name, label, x0, y0, x1, y1, c, y0 - c[1],
                                                                                           "TOO SMALL" if clipped else "ok", ("  suggest %r" % (sugg,)) if clipped else ""))
    return clipped


def canvas_check():
    bad = 0
    for name in cast22.NEW22:
        bad += _check("", name, member_poses(name), cast22.CANVAS22[name])
    for name in cast22.CROWD_NAMES:
        base = cast22.CROWD_KIND[name]
        bad += _check("crowd", name, [cast22.crowd_member(i, "pass_walk")[1] for i in range(16)], cast22.CANVAS22[base])
    probs = 0
    for n, (c, p) in cast22.STORY22.items():
        a = P.figure(c, p, "a")
        q = dict(p, mirror=not p.get("mirror", False))
        b = P.figure(c, q, "b")
        for key in ("feet", "head", "hand_r", "hand_l"):
            kb = key.replace("_r", "_X").replace("_l", "_r").replace("_X", "_l")
            va, vb = a["anchors"][key], b["anchors"][kb]
            if abs(va[0] + vb[0]) > 1e-6 or abs(va[1] - vb[1]) > 1e-6:
                probs += 1
    print("head_flip: %d poses checked, %d problems" % (len(cast22.STORY22), probs))
    return bad + probs


# ----------------------------------------------------------------------------- identity
_HASH_SNIPPET = r'''
import sys, hashlib
sys.path.insert(0, %(p10)r)
%(imp)s
import puppet as P
new = set(%(new)r)
h = hashlib.sha1()
n = 0
for k in sorted(P.STORY):
    c, p = P.STORY[k]
    if k.startswith(%(skip)r) or c in new:
        continue
    h.update(k.encode()); h.update(P.figure(c, p, "i")["svg"].encode()); n += 1
for c in sorted(P.CAST):
    if c in new or c.startswith("crowd22"):
        continue
    for pz in ({}, dict(yaw=0.5, expr="smug", arm_r="point", prop_r="pencil"), dict(yaw=-0.4, expr="laughing", arm_l="raised", mirror=True, fx=["sweat"])):
        h.update(c.encode()); h.update(P.figure(c, pz, "i")["svg"].encode()); n += 1
print(n, h.hexdigest())
'''


def identity():
    names = list(cast22.STORY22)
    new = list(cast22.NEW22) + list(cast22.CROWD_NAMES)
    skip = "\x00"
    # STORY keys added by cast22 are excluded by name (they are not in the cast10-only process)
    code_a = _HASH_SNIPPET % dict(p10=os.path.join(PROJ, "v3", "cast10"), imp="import cast10", new=new, skip=skip)
    code_b = _HASH_SNIPPET % dict(p10=os.path.join(PROJ, "v3", "cast22"), imp="import cast22", new=new, skip=skip)
    # in the cast22 process the STORY22 poses must be skipped too: filter by name
    code_b = code_b.replace("if k.startswith(%r) or c in new:" % skip, "if k in %r or c in new:" % (names,))
    ra = subprocess.run([sys.executable, "-I", "-c", code_a], capture_output=True, text=True, cwd=HERE)
    rb = subprocess.run([sys.executable, "-I", "-c", code_b], capture_output=True, text=True, cwd=HERE)
    print("cast10 only :", ra.stdout.strip() or ra.stderr[-300:])
    print("with cast22 :", rb.stdout.strip() or rb.stderr[-300:])
    ok = ra.returncode == 0 and rb.returncode == 0 and ra.stdout.strip() == rb.stdout.strip() and ra.stdout.strip() != ""
    print("earlier casts byte-identical:", "yes" if ok else "NO")
    return 0 if ok else 1


# ----------------------------------------------------------------------------- robust
def robust(quick=True):
    import random
    rnd = random.Random(22)
    n = fail = 0
    garbage = (None, "x", float("nan"), float("inf"), -5, 1e9, [1, 2], {"a": 1}, True, "white")
    keys = ("napkin", "flush", "puff", "fork_map", "board", "board_x", "board_y", "board_s", "desk", "desk_x", "desk_y", "desk_w", "desk_drawer", "typewriter", "tw_x", "tw_y",
            "pillar", "pillar_x", "pillar_w", "sweat", "t", "squash", "mirror", "expr")
    t0 = time.time()
    for name in cast22.NEW22 + cast22.CROWD_NAMES[:2]:
        for i in range(250):
            p = {}
            for kk in keys:
                if rnd.random() < 0.4:
                    p[kk] = rnd.choice(garbage)
            p["prop_r"] = rnd.choice((None,) + cast22.NEW_PROPS22)
            p["prop_l"] = rnd.choice((None,) + cast22.NEW_PROPS22)
            p["yaw"] = rnd.uniform(-1.2, 1.2)
            try:
                f = P.figure(name, p, "r")
                assert all(map(math.isfinite, f["bbox"]))
                n += 1
            except Exception as e:  # noqa: BLE001
                fail += 1
                if fail < 5:
                    print("FAIL", name, p, repr(e))
    a = P.figure("official", cast22.STORY22["off_buried_eat"][1], "d")["svg"]
    b = P.figure("official", cast22.STORY22["off_buried_eat"][1], "d")["svg"]
    det = a == b
    print("cast22 pose keys + garbage: %d ok, %d failed, deterministic %s, %.1f s" % (n, fail, det, time.time() - t0))
    rc = 0
    if not quick:
        sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
        import test_puppet as T
        T.CASTS = cast22.NEW22
        rc = T.main(["--quick"]) or 0
    return fail + (0 if det else 1) + rc


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    bad = 0
    if what in ("all", "sheet"):
        build_sheet()
    if what in ("all", "canvas"):
        bad += 1 if canvas_check() else 0
    if what in ("all", "identity"):
        bad += identity()
    if what in ("all", "robust"):
        bad += 1 if robust(quick=(what == "all" and "--quick" not in sys.argv and False) or "--lite" in sys.argv) else 0
    if what == "all":
        print("ALL OK" if not bad else "FAILED (%d)" % bad)
        sys.exit(1 if bad else 0)
