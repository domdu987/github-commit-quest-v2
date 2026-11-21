#!/usr/bin/env python3
"""test_cast4.py -- QA for cast4.py (same checks as test_cast3.py).

    python3 test_cast4.py            lineup.png + poses.png (Chromium via v2/puppet/raster.js), canvas check, quick robustness run
    python3 test_cast4.py lineup     lineup.png only
    python3 test_cast4.py poses      poses.png only
    python3 test_cast4.py canvas     sprite canvas check (pose range per member against cast4.CANVAS4)
    python3 test_cast4.py robust     v2 test_puppet.py (--quick) on the five new names
    python3 test_cast4.py compare    compare.jpg: reference crops beside our figures at the same head size (review aid)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast4  # noqa: E402
import puppet as P  # noqa: E402

PROJ = cast4.PROJ
LABEL = P._label
SKY, WALL, STONE, NIGHT = "#9fb4d6", "#d9a46a", "#a68a74", "#2a3354"
LINEUP = ("kenta", "master", "merchant", "woman2", "farmer")
LINEUP_POSE = {"kenta": dict(expr="determined", arm_l="akimbo"), "master": dict(expr="smug", arm_r="akimbo", arm_l="akimbo"),
               "merchant": dict(expr="smirk", arm_r="hip"), "woman2": dict(expr="happy"), "farmer": dict(arm_l="akimbo")}
KIDS = ("kenta",)


def _write(svg, w, h, base, ext="png"):
    sp = os.path.join(HERE, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(HERE, base + "." + ext)
    rc = P._raster(sp, out, w, h, 1)
    print("%s (%dx%d) rc=%d" % (out, w, h, rc))
    return out


def _fig(cast, pose, uid, D, x, y, shadow=0.9, lift=0.0):
    """figure with its feet at (x, y - lift*D) px, contact shadow on the ground at (x, y)."""
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - lift * D - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow * (1 - 0.4 * min(lift, 1)), uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def build_lineup(D=120):
    """every member front and 3/4 on one ground line, same head size; dashed lines at head top, hat top and soles, labels in D."""
    colw = int(2.9 * D)
    W = colw * len(LINEUP) + 40
    top = int(1.4 * D)
    ground = top + int(3.55 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, SKY),
         '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.15 * D), W, H, STONE)]
    adults = []
    for i, c in enumerate(LINEUP):
        x0 = 20 + i * colw
        if i % 2:
            o.append('<rect x="%d" y="0" width="%d" height="%d" fill="%s" opacity="0.35"/>' % (x0, colw, ground - int(0.15 * D), WALL))
        f0 = P.figure(c, dict(LINEUP_POSE[c]), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["bbox"][1] - 0.02
        if c not in KIDS:
            adults.append(ht)
        for j, yw in enumerate((0.0, 0.5)):
            pose = dict(LINEUP_POSE[c], yaw=yw if yw == 0.0 else yw * (1 if LINEUP_POSE[c].get("yaw", 0.3) >= 0 else -1))
            g, f = _fig(c, pose, "l%d%d" % (i, j), D, x0 + colw * (0.28 + 0.46 * j), ground)
            o.append(g)
        yt = ground - ht * D
        yh = ground - hh * D
        for y, col in ((yt, "#1a1015"), (yh, "#5a1a1a")):
            o.append('<path d="M%d,%.1f L%d,%.1f" stroke="%s" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, y, x0 + colw - 4, y, col))
        o.append('<path d="M%d,%.1f L%d,%.1f M%d,%.1f L%d,%.1f M%d,%.1f L%d,%.1f" stroke="#1a1015" stroke-width="2"/>'
                 % (x0 + 10, yt, x0 + 10, ground, x0 + 4, yt, x0 + 16, yt, x0 + 4, ground, x0 + 16, ground))
        o.append(LABEL(x0 + 14, int(yt) - 8, "%.2f D" % ht, 15))
        o.append(LABEL(x0 + colw - 112, int(yh) - 8, "hat %.2f D" % hh, 13))
        o.append(LABEL(x0 + 8, 24, c, 20))
        o.append(LABEL(x0 + 8, H - 14, "front / 3-4", 13))
    mean = sum(adults) / len(adults)
    hero = P.figure("kenta", LINEUP_POSE["kenta"], "m")
    nh = hero["feet_y"] - hero["anchors"]["head_top"][1]
    o.append(LABEL(20, 52, "head top to soles; head D = %d px for all.  kenta / mean adult = %.2f / %.2f = %.2f" % (D, nh, mean, nh / mean), 16))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(o)), W, H


def build_poses(D=100):
    names = list(cast4.STORY4)
    cols = 6
    cw, ch = int(2.9 * D), int(5.6 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, SKY)]
    for i, n in enumerate(names):
        cast, pose = cast4.STORY4[n]
        meta = cast4.STORY4_META.get(n, {})
        x0, y0 = (i % cols) * cw, (i // cols) * ch
        bg = WALL if (i + i // cols) % 2 else "#c9b8a0"
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, bg))
        ground = y0 + ch - int(0.55 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.12 * D), cw, ch - (ground - int(0.12 * D) - y0), STONE))
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch, x0, y0, cw, ch))
        if meta.get("lift"):
            o.append('<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x0 + cw * 0.42, ground - meta["lift"] * D, D,
                                                                               cast4.rubble_svg("rb%d" % i, 2.6, meta["lift"])))
        g, f = _fig(cast, pose, "p%d" % i, D, x0 + cw * 0.42, ground, shadow=0.0 if meta.get("lift") else 0.9, lift=meta.get("lift", 0.0))
        o.append(g + "</svg>")
        o.append(LABEL(x0 + 8, y0 + 22, n, 15))
        o.append(LABEL(x0 + 8, y0 + ch - 10, cast + (" (lift %.2f D)" % meta["lift"] if "lift" in meta else ""), 12))
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, "".join(o)), W, H


def canvas_check(verbose=True):
    bad = 0
    for name in cast4.NEW4:
        C = P.CAST[name]
        poses = [{}]
        for a in sorted(P.ARM_PRESETS[C["build"]]):
            for pr in (None, "mallet", "chain", "plank", "plaster_trowel", "lantern2"):
                poses.append(dict(arm_r=a, arm_l=a, prop_r=pr, yaw=0.6))
                poses.append(dict(arm_r=a, arm_l=a, prop_l=pr, yaw=-0.6, squash=(0.8, 1.15)))
        poses += [dict(legs="crouch"), dict(legs="wide"), dict(fx=["steam", "zzz", "sweat", "tears"], expr="asleep"), dict(yaw=1.2), dict(yaw=-1.2)]
        poses += [p for (c, p) in cast4.STORY4.values() if c == name]
        x0 = y0 = 1e9
        x1 = y1 = -1e9
        for p in poses:
            f = P.figure(name, p, "c")
            fx, fy = f["anchors"]["feet"][0], f["feet_y"]
            b = f["bbox"]
            x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
        c = cast4.CANVAS4[name]
        clipped = x0 < c[0] or y0 - 0.30 < c[1] or x1 > c[2] or y1 > c[3]
        bad += clipped
        if verbose:
            print("%-8s range (%.3f, %.3f, %.3f, %.3f)  canvas %r  head room %.2f D  %s" % (name, x0, y0, x1, y1, c, y0 - c[1], "TOO SMALL" if clipped else "ok"))
    try:
        sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
        import sprites
        miss = [n for n in cast4.NEW4 if n not in sprites.DEFAULT_CANVAS]
        print("sprites.DEFAULT_CANVAS has the new members:", "yes" if not miss else "MISSING %r" % miss)
        bad += len(miss)
    except Exception as e:  # noqa: BLE001
        print("sprites import failed:", e)
    return bad


def robust():
    sys.path.insert(0, os.path.join(PROJ, "v2", "puppet"))
    import test_puppet as T
    T.CASTS = cast4.NEW4
    return T.main(["--quick"])


def head_flip_check():
    """the stage's head_flip (mirror inside scale(-1,1)) must give the same geometry for every member."""
    sys.path.insert(0, os.path.join(PROJ, "v3", "stage"))
    import sprites
    n = 0
    for name, (c, p) in cast4.STORY4.items():
        svg = sprites._head_flipped(c, p, "hf")
        a = P.figure(c, p, "a")
        b = P.figure(c, dict(p, mirror=True), "b")
        if abs(a["feet_y"] - b["feet_y"]) > 1e-9 or not svg.startswith('<g transform="scale(-1 1)">'):
            print("head_flip mismatch", name)
            n += 1
    print("head_flip: %d STORY4 poses checked, %d problems" % (len(cast4.STORY4), n))
    return n


def compare():
    """reference crops (clip A / B) beside our cast at the same head size, for the review."""
    from PIL import Image
    refs = [("a/t0010.jpg", (120, 400, 470, 1120), 285), ("a/t0040.jpg", (60, 560, 330, 1160), 185)]
    tiles = []
    for rel, box, Dpx in refs:
        im = Image.open(os.path.join(PROJ, "ref", rel)).convert("RGB").crop(box)
        tiles.append((im, Dpx))
    svg, W, H = build_lineup(D=150)
    out = _write(svg, W, H, "tmp_compare_lineup")
    ours = Image.open(out).convert("RGB")
    s = 150.0 / 150.0
    hh = max(ours.height, max(t[0].height for t in tiles))
    canvas = Image.new("RGB", (ours.width + sum(int(t[0].width * 150.0 / t[1]) for t in tiles) + 40, hh), (40, 40, 40))
    x = 0
    for im, Dpx in tiles:
        k = 150.0 / Dpx
        im2 = im.resize((int(im.width * k), int(im.height * k)))
        canvas.paste(im2, (x, 0))
        x += im2.width + 20
    canvas.paste(ours, (x, 0))
    p = os.path.join(HERE, "compare.jpg")
    canvas.save(p, quality=90)
    os.remove(out)
    os.remove(out[:-4] + ".svg")
    print(p)


def main(argv):
    cmd = argv[0] if argv else "all"
    rc = 0
    if cmd in ("all", "lineup"):
        svg, W, H = build_lineup()
        _write(svg, W, H, "lineup")
    if cmd in ("all", "poses"):
        svg, W, H = build_poses()
        _write(svg, W, H, "poses")
    if cmd in ("all", "canvas"):
        rc += canvas_check()
        rc += head_flip_check()
    if cmd in ("all", "robust"):
        rc += robust() or 0
    if cmd == "compare":
        compare()
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
