#!/usr/bin/env python3
"""test_cast20.py -- QA for cast20.py (film 20: Eiffel's tower and the artists' protest).

    python3 test_cast20.py            story + identity + canvas + robust + sheet
    python3 test_cast20.py story      every STORY20 pose renders (plain + mirrored), finite bbox, deterministic, no text, mouth rule
    python3 test_cast20.py identity   earlier casts unchanged: every pose of puppet.STORY + a pose-key sweep over every earlier CAST member give
                                      byte-identical SVG with and without cast20 imported (two separate processes)
    python3 test_cast20.py measure    print the CANVAS20 table (feet-relative bounds over poses, cycles, yaw sweeps)
    python3 test_cast20.py canvas     every pose / cycle fits CANVAS20
    python3 test_cast20.py robust     garbage pose keys on the new members
    python3 test_cast20.py sheet      sheet.jpg (everything) and sheet_small.jpg (360 px wide phone check)
"""
import hashlib
import json
import math
import os
import random
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
WITH = "identity-child" not in sys.argv
if "--nocast20" in sys.argv:
    sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "cast10")))
    import cast10  # noqa: E402,F401
    import puppet as P  # noqa: E402
    cast20 = None
else:
    import cast20  # noqa: E402
    import puppet as P  # noqa: E402
LABEL = P._label
BG, GROUND = "#cfccc6", "#a9a49a"
LIPSYNC = {n for n, m in (cast20.STORY20_META.items() if cast20 else []) if m.get("lipsync")}
FAILS = []


def check(ok, msg):
    if not ok:
        FAILS.append(msg)
        print("FAIL", msg)
    return ok


def _svgdoc(W, H, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, body)


def _raster(svg, w, h, base):
    sp = os.path.join(TMP, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(TMP, base + ".png")
    P._raster(sp, out, w, h, 1)
    os.remove(sp)
    return out


# ------------------------------------------------------------------------------------------------ story
def t_story():
    t0 = time.time()
    n = 0
    for name, (cast, pose) in cast20.STORY20.items():
        for mir in (False, True):
            p = dict(pose, mirror=mir)
            f = P.figure(cast, p, "t")
            f2 = P.figure(cast, p, "t")
            ok = f["svg"] == f2["svg"] and all(math.isfinite(v) for v in f["bbox"]) and math.isfinite(f["feet_y"])
            check(ok, "story %s mirror=%s" % (name, mir))
            check(not re.search(r"<text", f["svg"]), "text element in " + name)
            n += 1
    # mouth rule: only maupassant poses flagged lipsync are meant to be driven; other characters hold fixed mouths
    for name, (cast, pose) in cast20.STORY20.items():
        if name in LIPSYNC:
            check(cast == "maupassant", "lipsync pose not maupassant " + name)
        m = pose.get("mouth")
        if isinstance(m, str) and m.startswith("talk") and name not in LIPSYNC:
            check(False, "talk mouth outside lip-sync pose " + name)
    for c in cast20.NEW20:
        for lab, kw in cast20.EXPRS20[c].items():
            P.figure(c, dict(kw), "e")
    for c in cast20.NEW20:
        for mode in cast20.CYCLE_MODES:
            for ph in (0.0, 0.3, 0.7):
                for fc in (1, -1):
                    P.figure(c, cast20.cycle(c, ph, mode, fc), "c")
    for pr in cast20.NEW_PROPS20:
        P.figure("eiffel", dict(arm_r=dict(hand=(0.6, 0.6)), prop_r=pr), "pp")
    print("story: %d renders (%d poses x plain/mirrored), deterministic, no <text>, mouth rule ok, %d expression sets, cycles of %d casts, %d props (%.1f s)" % (
        n, len(cast20.STORY20), sum(len(v) for v in cast20.EXPRS20.values()), len(cast20.NEW20), len(cast20.NEW_PROPS20), time.time() - t0))


# ------------------------------------------------------------------------------------------------ identity
def _hash_all():
    h = hashlib.sha256()
    cnt = 0
    names = sorted(n for n in P.CAST if not (cast20 and (n in cast20.NEW20 or n.endswith("_bare") and n[:-5] in cast20.NEW20)))
    for k, (c, p) in sorted(P.STORY.items()):
        if cast20 and k in cast20.STORY20:
            continue
        h.update(P.figure(c, p, "i")["svg"].encode())
        cnt += 1
    keys = [dict(expr="happy", yaw=0.3, arm_r="point", prop_r="hammer"), dict(expr="shocked", yaw=-0.5, legs="wide", prop_l="paper", fx=["sweat"]),
            dict(expr="laughing", glow=1.0, napkin=1, bite=1, key_press=1, hat_off=1, t=0.4)]
    for n in names:
        for pk in keys:
            try:
                h.update(P.figure(n, dict(pk), "i")["svg"].encode())
            except Exception as e:      # pose keys of other casts may raise on some members the same way with and without cast20
                h.update(type(e).__name__.encode())
            cnt += 1
    return h.hexdigest(), cnt


def t_identity():
    t0 = time.time()
    a = subprocess.run([sys.executable, os.path.abspath(__file__), "identity-child", "--nocast20"], capture_output=True, text=True)
    b = subprocess.run([sys.executable, os.path.abspath(__file__), "identity-child"], capture_output=True, text=True)
    ha, hb = a.stdout.strip().split("\n")[-1], b.stdout.strip().split("\n")[-1]
    check(ha == hb and ha.count(" ") == 1, "identity: hashes differ %s / %s %s" % (ha, hb, a.stderr[-300:] + b.stderr[-300:]))
    print("identity: earlier STORY poses + pose-key sweep of every earlier member: %s (%s) %.1f s" % ("0 differ" if ha == hb else "DIFFER", ha.split()[-1] if ha else "", time.time() - t0))


# ------------------------------------------------------------------------------------------------ canvas
def _bounds_for(c, runs):
    x0 = y0 = 1e9
    x1 = y1 = -1e9
    for pose in runs:
        f = P.figure(c, pose, "m")
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        b = f["bbox"]
        x0, y0, x1, y1 = min(x0, b[0] - fx), min(y0, b[1] - fy), max(x1, b[2] - fx), max(y1, b[3] - fy)
    return x0, y0, x1, y1


def _runs(c):
    out = []
    for name, (cc, pose) in cast20.STORY20.items():
        if cc == c:
            out += [dict(pose), dict(pose, mirror=True)]
    for mode in cast20.CYCLE_MODES:
        for i in range(16):
            for fc in (1, -1):
                out.append(cast20.cycle(c, i / 16.0, mode, fc))
    for y in (-0.9, -0.5, 0, 0.5, 0.9):
        for ar in ("down", "raised", "point", "forward", "wave"):
            out.append(dict(yaw=y, arm_r=ar, arm_l=ar))
    return out


def t_measure():
    res = {}
    for c in cast20.NEW20:
        x0, y0, x1, y1 = _bounds_for(c, _runs(c))
        sn = lambda v, up: (math.ceil(v * 16) if up else math.floor(v * 16)) / 16.0
        w = max(abs(x0), abs(x1)) + 0.15
        res[c] = (-sn(w, True), sn(y0 - 0.12, False), sn(w, True), sn(y1 + 0.12, True))
    print("CANVAS20 = {")
    for c, v in res.items():
        print('    "%s": (%.4f, %.4f, %.4f, %.4f),' % ((c,) + v))
    print("}")


def t_canvas():
    bad, worst = 0, {}
    for c in cast20.NEW20:
        cv = cast20.CANVAS20[c]
        x0, y0, x1, y1 = _bounds_for(c, _runs(c))
        m = min(x0 - cv[0], y0 - cv[1], cv[2] - x1, cv[3] - y1)
        if m < 0:
            bad += 1
            print("FAIL canvas", c, m)
            FAILS.append("canvas " + c)
        worst[c] = m
    print("canvas: %d outside; smallest margins (D): %s" % (bad, ", ".join("%s %.2f" % (c, w) for c, w in sorted(worst.items()))))


# ------------------------------------------------------------------------------------------------ robust
def t_robust():
    rnd = random.Random(20)
    junk = [None, float("nan"), float("inf"), -1e9, 1e9, "x", [], {}, (1,), True, "happy", 0.5, -2]
    keys = ["yaw", "pitch", "expr", "mouth", "blink", "gaze", "arm_r", "arm_l", "legs", "prop_r", "prop_l", "fx", "squash", "lean", "head_roll",
            "glow", "napkin", "bite", "key_press", "hat_off", "stool", "t", "mirror", "tint", "ink"]
    n = bad = 0
    t0 = time.time()
    for c in cast20.NEW20:
        for _ in range(240):
            pose = {k: rnd.choice(junk) for k in rnd.sample(keys, rnd.randint(1, 8))}
            try:
                f = P.figure(c, pose, "r")
                ok = all(math.isfinite(v) for v in f["bbox"])
            except Exception as e:
                ok = False
                print("robust exception", c, pose, e)
            n += 1
            bad += 0 if ok else 1
    check(bad == 0, "robust %d bad" % bad)
    print("robust: %d garbage poses on %d members, %d failed (%.1f s)" % (n, len(cast20.NEW20), bad, time.time() - t0))


# ------------------------------------------------------------------------------------------------ sheet
def _fig(cast, pose, uid, D, x, y, shadow=0.9):
    f = P.figure(cast, pose, uid)
    tx, ty = x - f["anchors"]["feet"][0] * D, y - f["feet_y"] * D
    s = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (x, y, D, P.contact_shadow(shadow, uid + "s")) if shadow else ""
    return s + '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (tx, ty, D, f["svg"]), f


def _under(x, y, text, size=13):
    w = 0.60 * size * len(text) + 12
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="#2e2a2c" opacity="0.85"/>'
            '<text x="%.1f" y="%.1f" font-family="DejaVu Sans, sans-serif" font-size="%d" fill="#ffffff" text-anchor="middle">%s</text>' % (x - w / 2, y - size - 2, w, size + 8, x, y + 1, size, text))


LINEUP_POSE = {"eiffel": dict(expr="neutral", yaw=0.3), "eiffel_old": dict(expr="neutral", yaw=0.3, lean=4), "maupassant": dict(expr="smug", yaw=0.3, mouth="flat", arm_r="akimbo", arm_l="akimbo", legs="wide")}


def sec_lineup(D=96):
    names = list(cast20.NEW20)
    cw = int(2.55 * D)
    W = cw * len(names) + 80
    top, ground = int(0.9 * D), int(0.9 * D) + int(4.7 * D)
    H = ground + int(0.9 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.10 * D), W, H, GROUND)]
    for i in range(0, 5):
        y = ground - i * D
        o.append('<path d="M6,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1" opacity="0.7" stroke-dasharray="3 5"/><path d="M6,%.1f L26,%.1f" stroke="#2e2a2c" stroke-width="2"/>' % (y, W - 6, y, y, y))
        o.append(LABEL(30, int(y) - 4, "%d D" % i, 13))
    for i, c in enumerate(names):
        pose = dict(LINEUP_POSE.get(c, dict(expr="neutral", yaw=0.3)))
        f0 = P.figure(c, pose, "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        x = 80 + i * cw + cw // 2
        g, f = _fig(c, pose, "h%d" % i, D, x, ground)
        o.append(g)
        yt = ground - ht * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#2e2a2c" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x - cw // 2 + 4, yt, x + cw // 2 - 4, yt))
        o.append(LABEL(x - cw // 2 + 6, int(yt) - 6, "%.2f D" % ht + ("" if abs(hh - ht) < 0.03 else " (hat %.2f)" % hh), 12))
        o.append(_under(x, ground + int(0.5 * D), c, 13))
    o.append(LABEL(10, 26, "cast20 lineup: head D = %d px, heads top to soles in D (dashed line = top of head), ruler at the left" % D, 16))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_poses(D=58, cols=10):
    names = list(cast20.STORY20)
    cw, ch = int(3.5 * D), int(6.0 * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, name in enumerate(names):
        c, pose = cast20.STORY20[name]
        x, y = (i % cols) * cw + cw // 2, (i // cols) * ch + int(5.3 * D)
        g, f = _fig(c, pose, "p%d" % i, D, x, y)
        o.append(g)
        o.append(LABEL((i % cols) * cw + 4, y + 22, name + ("  [LIP-SYNC]" if name in LIPSYNC else ""), 11))
    return _svgdoc(W, H, "".join(o)), W, H


def _head(c, pose, uid, S, x, y):
    """head close-up in a clipped square of S px centred on (x, y): the figure's head centre is its origin."""
    f = P.figure(c, dict(pose, arm_r="down", arm_l="down"), uid)
    sc = S / 2.1
    return ('<svg x="%.1f" y="%.1f" width="%d" height="%d" viewBox="-1.05 -1.50 2.1 2.1"><rect x="-1.05" y="-1.50" width="2.1" height="2.1" fill="#ddd8d0"/>%s</svg>'
            % (x - S / 2, y - S / 2, S, S, f["svg"]))


def sec_faces(S=176):
    rows = list(cast20.NEW20)
    mx = max(len(cast20.EXPRS20[c]) for c in rows)
    W, H = 150 + mx * (S + 6), len(rows) * (S + 30) + 30
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for r, c in enumerate(rows):
        y = 30 + r * (S + 30) + S // 2
        o.append(LABEL(8, y, c, 14))
        for i, (lab, kw) in enumerate(cast20.EXPRS20[c].items()):
            x = 150 + i * (S + 6) + S // 2
            pose = dict(kw)
            pose.setdefault("yaw", 0.3)
            o.append(_head(c, pose, "f%d_%d" % (r, i), S, x, y))
            o.append(_under(x, y + S // 2 + 16, lab, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_mouths(S=150):
    n = len(cast20.MOUTH_SET)
    W, H = n * (S + 6) + 20, S + 100
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    o.append(LABEL(10, 22, "maupassant lip-sync mouth set (the only character with lip-sync): talk_mouth(frame, level) picks from flat / talk_a / talk_b; the rest are held shapes", 14))
    for i, m in enumerate(cast20.MOUTH_SET):
        x = 10 + i * (S + 6) + S // 2
        o.append(_head("maupassant", dict(expr="sneer", mouth=m, yaw=0.3), "m%d" % i, S, x, 40 + S // 2))
        o.append(_under(x, 40 + S + 22, m if isinstance(m, str) else "open %.2f x %.2f" % (m[1], m[2]), 12))
    return _svgdoc(W, H, "".join(o)), W, H


PROP_SHOW = [("blueprint", "eiffel", dict(angle=-30)), ("rivet20", "eiffel", dict(angle=-10)), ("giant_rivet", "eiffel", dict(angle=-35)), ("tongs_rivet", "riveter_tongs", dict(angle=-18)),
             ("tongs_cold", "riveter_forge", dict(angle=25)), ("rivet_hammer", "riveter_hammer", dict(angle=-60)), ("hammer20", "eiffel", dict(angle=-55)), ("quill", "poet20", dict(angle=-50)),
             ("news20", "maupassant", {}), ("sheet20", "architect20", {}), ("doc_seal", "official", {}), ("wine_glass", "maupassant", {}), ("fork20", "maupassant", dict(angle=-40)),
             ("knife20", "maupassant", dict(angle=-20)), ("cane20", "gent20", dict(angle=70, scale=0.7)), ("parasol20", "lady20", dict(angle=-62, scale=0.9)), ("tray20", "waiter", {}),
             ("towel20", "waiter", {}), ("morse_key", "telegraphist", {}), ("bowler_held", "eiffel", {}), ("tophat_held", "official", {}), ("palette", "painter20", dict(angle=0)),
             ("paintbrush", "painter20", dict(angle=-60))]


def sec_props(D=100, cols=6):
    cw, ch = int(3.4 * D), int(2.9 * D)
    rows = (len(PROP_SHOW) + cols - 1) // cols
    W, H = cw * cols, ch * rows + 40
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), LABEL(8, 24, "held props (each as drawn in a hand; all are text-free: papers are greeked bars / squiggles)", 15)]
    for i, (pr, c, kw) in enumerate(PROP_SHOW):
        x, y = (i % cols) * cw + cw // 2, 40 + (i // cols) * ch + int(1.0 * D)
        pose = dict(yaw=0.4, expr="neutral", arm_r=dict(hand=(0.82, 0.55), bend=-0.2, stretch=1.2), arm_l="down", prop_r=dict(type=pr, **kw))
        if pr in ("tray20", "towel20"):
            pose["arm_r"] = dict(hand=(0.62, 0.50), bend=-0.2)
        f = P.figure(c, pose, "pr%d" % i)
        sc = D * 0.8
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="-0.9 -0.9 3.4 2.4"><rect x="-0.9" y="-0.9" width="3.4" height="2.4" fill="#ddd8d0"/>%s</svg>' % (x - cw // 2 + 2, y - D + 2, cw - 4, int(2.4 / 3.4 * (cw - 4)), f["svg"]))
        o.append(_under(x, y - D + int(2.4 / 3.4 * (cw - 4)) + 6, pr, 12))
    return _svgdoc(W, H, "".join(o)), W, H


def t_sheet():
    from PIL import Image
    t0 = time.time()
    secs = [("lineup", sec_lineup()), ("faces", sec_faces()), ("mouths", sec_mouths()), ("props", sec_props()), ("poses", sec_poses())]
    imgs = []
    for nm, (svg, w, h) in secs:
        out = _raster(svg, w, h, "sec_" + nm)
        print("section %-8s %5d x %5d" % (nm, w, h))
        imgs.append(Image.open(out).convert("RGB"))
    W = max(i.width for i in imgs)
    H = sum(i.height for i in imgs)
    sheet = Image.new("RGB", (W, H), (0xcf, 0xcc, 0xc6))
    y = 0
    for im in imgs:
        sheet.paste(im, (0, y))
        y += im.height
    sp = os.path.join(HERE, "sheet.jpg")
    sheet.save(sp, quality=88)
    print("wrote %s (%d x %d) in %.1f s" % (sp, W, H, time.time() - t0))
    # phone check: lineup row + a few expression heads at 360 px wide
    small = Image.new("RGB", (360, 0))
    lu = imgs[0].resize((360, int(imgs[0].height * 360 / imgs[0].width)), Image.LANCZOS)
    S = 360
    names = ["eiffel", "maupassant", "painter20", "riveter_tongs", "telegraphist", "waiter"]
    D = 46
    pw = 60
    grid = Image.new("RGB", (360, 260), (0xcf, 0xcc, 0xc6))
    o = ['<rect width="360" height="260" fill="%s"/>' % BG]
    for i, c in enumerate(names):
        pose = dict(cast20.STORY20[{"eiffel": "eiffel_giant_rivet", "maupassant": "maupassant_quote_point", "painter20": "painter20_outraged", "riveter_tongs": "riveter_tongs_work",
                                    "telegraphist": "telegraphist_stand", "waiter": "waiter_tray"}[c]][1])
        g, f = _fig(c, pose, "s%d" % i, D, 30 + i * 60, 230)
        o.append(g)
    gp = _raster(_svgdoc(360, 260, "".join(o)), 360, 260, "sm")
    grid = Image.open(gp).convert("RGB")
    ph = Image.new("RGB", (360, lu.height + 260), (0xcf, 0xcc, 0xc6))
    ph.paste(lu, (0, 0))
    ph.paste(grid, (0, lu.height))
    pp = os.path.join(HERE, "sheet_small.jpg")
    ph.save(pp, quality=88)
    print("wrote %s (360 x %d)" % (pp, ph.height))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args and args[0] == "identity-child":
        print(*_hash_all())
        return
    what = args[0] if args else "all"
    t0 = time.time()
    if what in ("all", "story"):
        t_story()
    if what in ("all", "identity"):
        t_identity()
    if what == "measure":
        t_measure()
    if what in ("all", "canvas"):
        t_canvas()
    if what in ("all", "robust"):
        t_robust()
    if what in ("all", "sheet"):
        t_sheet()
    print("TOTAL FAILED: %d (%.1f s)" % (len(FAILS), time.time() - t0))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
