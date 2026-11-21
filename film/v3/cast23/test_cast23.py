#!/usr/bin/env python3
"""test_cast23.py -- QA for cast23.py (film 23: the Ghost Army).

    python3 test_cast23.py            cast_sheet.jpg + cycles.jpg + canvas / ground check + robustness
    python3 test_cast23.py sheet      cast_sheet.jpg (lineup, story poses, pose library, faces, props, lift line-up) and cycles.jpg (cycle strips)
    python3 test_cast23.py canvas     measures the feet-relative canvases over every pose / cycle frame (prints a table) and checks CANVAS23 / CANVAS23_WIDE
    python3 test_cast23.py ground     renders sprites through stage/sprites.py and checks the ground point: no gap under the feet / wheels / seat
    python3 test_cast23.py robust     pose-key garbage on every member, determinism
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast23  # noqa: E402
import puppet as P  # noqa: E402

TMP = os.path.join(HERE, "tmp")
os.makedirs(TMP, exist_ok=True)
LABEL = P._label
BG, BG2, GROUND = "#d3cfc6", "#c8c4ba", "#a9a49a"
NIGHT, NIGHT2 = "#3a4258", "#464e66"
LINEUP = cast23.NEW23
LINEUP_POSE = {"major": dict(expr="smug", pitch=-0.3, arm_r="akimbo", arm_l="akimbo", cigar=True), "gi_smile": dict(expr="grinning"),
               "fr_beret": dict(expr="happy"), "ger_round": dict(expr="neutral"), "gi_designer": dict(expr="smirk")}


def _svgdoc(W, H, body):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">%s</svg>' % (W, H, body)


def _write(svg, w, h, base):
    sp = os.path.join(TMP, base + ".svg")
    with open(sp, "w") as fh:
        fh.write(svg)
    out = os.path.join(TMP, base + ".png")
    P._raster(sp, out, w, h, 1)
    os.remove(sp)
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


def _title(W, text, h=40):
    return '<rect width="%d" height="%d" fill="#2e2a2c"/><text x="12" y="%d" font-family="DejaVu Sans, sans-serif" font-size="17" font-weight="bold" fill="#ffffff">%s</text>' % (W, h, h - 12, text)


def sec_heights(D=104):
    colw = int(2.3 * D)
    W = colw * len(LINEUP) + 20
    top = 40 + int(0.9 * D)
    ground = top + int(3.6 * D)
    H = ground + int(0.8 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.10 * D), W, H, GROUND)]
    for i, c in enumerate(LINEUP):
        x0 = 10 + i * colw
        o.append('<rect x="%d" y="40" width="%d" height="%d" fill="%s"/>' % (x0, colw, ground - int(0.10 * D) - 40, BG2 if i % 2 else BG))
        base = LINEUP_POSE.get(c, dict(expr="neutral"))
        f0 = P.figure(c, dict(base), "m")
        ht = f0["feet_y"] - f0["anchors"]["head_top"][1]
        hh = f0["feet_y"] - f0["anchors"]["hat_top"][1]
        for j, yw in enumerate((0.0, 0.55)):
            g, f = _fig(c, dict(base, yaw=yw), "h%d%d" % (i, j), D, x0 + colw * (0.30 + 0.42 * j), ground)
            o.append(g)
        yt = ground - hh * D
        o.append('<path d="M%d,%.1f L%d,%.1f" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="6 4"/>' % (x0 + 4, yt, x0 + colw - 4, yt))
        o.append(LABEL(x0 + 6, int(yt) - 6, "%.2f D (hat %.2f)" % (ht, hh), 12))
        o.append(_under(x0 + colw / 2, ground + int(0.50 * D), c, 17))
    o.append(_title(W, "cast23 (film 23, Ghost Army 1944-45): front / 3-4, head D = %d px, height head top to soles (hat)" % D))
    return _svgdoc(W, H, "".join(o)), W, H


def _grid(names, D, cols, title, cw=3.1, ch=5.6, poses=None, night=()):
    cw, ch = int(cw * D), int(ch * D)
    rows = (len(names) + cols - 1) // cols
    W, H = cw * cols, ch * rows + 40
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG)]
    for i, n in enumerate(names):
        cast, pose = poses[n] if poses else cast23.STORY23[n]
        x0, y0 = (i % cols) * cw, 40 + (i // cols) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, NIGHT if n in night else (BG2 if (i + i // cols) % 2 else BG)))
        ground = y0 + ch - int(0.62 * D)
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, ground - int(0.06 * D), cw, int(0.2 * D), GROUND))
        f = P.figure(cast, pose, "z")
        b = f["bbox"]
        cx = (b[0] + b[2]) / 2 - f["anchors"]["feet"][0]
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">' % (x0, y0, cw, ch - int(0.40 * D), x0, y0, cw, ch - int(0.40 * D)))
        g, f = _fig(cast, pose, "p%d" % i, D, x0 + cw * 0.5 - cx * D, ground)
        o.append(g + "</svg>")
        meta = cast23.STORY23_META.get(n, {})
        if meta.get("lipsync"):
            o.append(LABEL(x0 + 6, y0 + 18, "LIP-SYNC", 13))
        o.append(_under(x0 + cw / 2, y0 + ch - int(0.12 * D), n, 13))
    o.insert(1, _title(W, title))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_story(D=74):
    names = [n for n in cast23.STORY23 if not (n.startswith("gi_") and n.rsplit("_", 1)[-1] in [m[3:] for m in cast23.GI23] and n.count("_") == 2)]
    return _grid(names, D, 10, "STORY23: role and story poses (LIP-SYNC = quoted speaker; every other mouth is a held drawing)")


def sec_library(D=74):
    """the generic GI pose library, each pose on a different member so all seven faces show."""
    acts = ("stand", "salute", "point", "shock", "sweat", "laugh", "wave", "walk", "lift", "carry", "tiptoe", "paddle", "droop", "grin")
    names = []
    for i, a in enumerate(acts):
        m = cast23.GI23[i % len(cast23.GI23)]
        names.append("gi_%s_%s" % (a, m[3:]))
    return _grid(names, D, 7, "GI pose library: gi_<action>_<member> (all 7 GIs)")


FACE_STATES = (("neutral", {}), ("talk_a", dict(mouth="talk_a")), ("talk_b", dict(mouth="talk_b")), ("talk_o", dict(mouth="talk_o")), ("flat", dict(mouth="flat")),
               ("blink 2", dict(blink=2)), ("happy", dict(expr="happy")), ("laughing", dict(expr="laughing")), ("grinning", dict(expr="grinning")),
               ("smug", dict(expr="smug")), ("angry", dict(expr="angry")), ("shocked", dict(expr="shocked")), ("jaw drop", dict(expr="stunned", mouth=("open", 0.16, 0.24))),
               ("worried", dict(expr="worried")), ("squint", dict(expr="squint")))
SPECIAL = {"major": (("smug+cigar", dict(expr="smug", cigar=True)), ("RED angry", dict(expr="angry", red23=1)), ("puff 1", dict(expr="shouting", puff23=1, red23=1)),
                     ("puff 2", dict(expr="shouting", puff23=2, red23=1))),
           "gi_smile": (("dry smile", dict(expr="grinning", bigsweat23=1)),),
           "fr_beret": (("chatty", dict(expr="happy", mouth="talk_a")), ("dazed", dict(expr="stunned", daze23=1, t=0.2))),
           "fr_cap": (("chatty", dict(expr="happy", mouth="talk_a")), ("dazed", dict(expr="stunned", daze23=1, t=0.2))),
           "ger_tall": (("surprise", dict(expr="shocked", mouth=("open", 0.12, 0.16))),), "ger_round": (("surprise", dict(expr="shocked", mouth=("open", 0.12, 0.16))),)}


def sec_faces(D=86):
    cw, ch = int(1.35 * D), int(1.75 * D)
    ncol = len(FACE_STATES) + 4
    W, H = 150 + cw * ncol, ch * len(LINEUP) + 50
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), _title(W, "faces: whole drawings swapped (never tweened); specials at the right")]
    for r, c in enumerate(LINEUP):
        y0 = 45 + r * ch
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>' % (y0, W, ch, BG2 if r % 2 else BG))
        o.append(LABEL(6, y0 + ch // 2, c, 15))
        states = list(FACE_STATES) + list(SPECIAL.get(c, ()))
        for j, (lab, extra) in enumerate(states):
            f = P.figure(c, dict(dict(yaw=0.3), **extra), "f%d_%d" % (r, j))
            cx, cy = 150 + j * cw + cw / 2, y0 + ch * (0.58 if c == "major" else 0.52)
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                     % (150 + j * cw, y0, cw, ch - 22, 150 + j * cw, y0, cw, ch - 22, cx, cy, D, f["svg"]))
            o.append(_under(cx, y0 + ch - 7, lab, 11))
    return _svgdoc(W, H, "".join(o)), W, H


def sec_lift(D=64):
    """four lifters under one tank: the tank underside is one straight line at LIFT_H; every pair of hands touches it."""
    who = ("gi_smile", "gi_pump", "gi_painter", "gi_driver")
    W, H = int(13 * D), int(6.4 * D) + 40
    ground = H - int(0.7 * D)
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), _title(W, "lift: hand tops at LIFT_H = %.2f D for every lifter" % cast23.LIFT_H),
         '<rect y="%d" width="%d" height="%d" fill="%s"/>' % (ground - int(0.06 * D), W, H, GROUND)]
    yt = ground - cast23.LIFT_H * D
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="12" fill="#7d7f4c" stroke="#3a2832" stroke-width="3" opacity="0.92"/>' % (1.2 * D, yt - 2.2 * D, 10.6 * D, 2.2 * D))
    o.append('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="#c83a2e" stroke-width="2" stroke-dasharray="8 5"/>' % (0, yt, W, yt))
    for i, c in enumerate(who):
        p = cast23.STORY23["gi_smile_lift_quote"][1] if c == "gi_smile" else cast23.lift_pose(c, 0.2 * i)
        g, f = _fig(c, p, "l%d" % i, D, (2.2 + 2.9 * i) * D, ground)
        o.append(g)
        o.append(_under((2.2 + 2.9 * i) * D, ground + int(0.45 * D), c, 13))
    return _svgdoc(W, H, "".join(o)), W, H


def _prop_alone(kind, ang):
    k = P._Ctx("pp" + kind, P.INK, None)
    import cast8
    cast8._POSE8["an"] = {}
    cast8._POSE8["prop_i"] = 0
    cast8._POSE8["sides"] = ["r"]
    cast23._POSE23["t"] = 0.3
    svg, tip = cast23._prop(k, kind, (0.0, 0.0), ang, 1.0)
    return "<defs>%s</defs>%s" % ("".join(k.defs), svg)


def sec_props(D=150):
    items = [("brush23", 0, 1.0), ("pot23", 0, 1.0), ("record23", 0, 0.8), ("handset23", 0, 1.2), ("clipboard23", 0, 1.0), ("stencil23", 0, 1.0),
             ("cigar23", 0, 1.4), ("sausage23", 0, 1.4), ("chalk23", 0, 1.4), ("pin23", 0, 1.4), ("rag23", 0, 1.4), ("oar23", 0, 0.5)]
    cw, ch = int(1.3 * D), int(1.3 * D)
    extra = [("balloons", None, 0.42), ("balloon pop", None, 0.5), ("record (spin)", None, 0.8), ("falling sausage", None, 1.4)]
    allitems = items + extra
    W, H = cw * 8, ch * 2 + 40
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), _title(W, "props (drawn in the hand layer); standalone pieces for the set: balloon_svg, record_svg, sausage_svg")]
    for i, (lab, ang, sc) in enumerate(allitems):
        x0, y0 = (i % 8) * cw, 40 + (i // 8) * ch
        o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, y0, cw, ch, BG2 if i % 2 else BG))
        if lab == "balloons":
            svg = "".join('<g transform="translate(%.2f %.2f)">%s</g>' % (-0.45 + 0.3 * j, 0.25 - 0.1 * (j % 2), cast23.balloon_svg("b%d" % j, 0.3 + 0.2 * j, cast23.BALLOON_COLS[j], -90)[0]) for j in range(4))
        elif lab == "balloon pop":
            svg = cast23.balloon_svg("bp", 1.0, pop=1, angle=-90)[0]
        elif lab == "record (spin)":
            svg = cast23.record_svg("rs", 0.3)
        elif lab == "falling sausage":
            svg = cast23.sausage_svg("fs", 40)
        else:
            svg = _prop_alone(lab, ang)
        ox = -0.25 if lab in ("brush23", "handset23", "cigar23", "sausage23", "chalk23", "pin23", "oar23", "clipboard23", "stencil23") else 0.0
        oy = -0.25 if lab == "pot23" else (0.6 if lab in ("balloons", "balloon pop") else 0.0)
        if lab == "record23":
            ox = -0.5
        o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d"><g transform="translate(%.1f %.1f) scale(%.2f)">%s</g></svg>'
                 % (x0, y0, cw, ch - 26, x0, y0, cw, ch - 26, x0 + cw / 2 + ox * D * sc, y0 + ch * 0.45 + oy * D * sc, D * sc, svg))
        o.append(_under(x0 + cw / 2, y0 + ch - 8, lab, 13))
    return _svgdoc(W, H, "".join(o)), W, H


# ----------------------------------------------------------------------------- cycles
def cycle_rows():
    """(label, cast, [poses]) per strip: 8 frames each."""
    ph = [i / 8.0 for i in range(8)]
    R = []
    R.append(("walk  cycle(gi_radio, g/28, 'walk')", "gi_radio", [cast23.cycle("gi_radio", p, "walk", 1, dict(expr="neutral")) for p in ph]))
    R.append(("pump  pump_frame(gi_pump, g/20)", "gi_pump", [cast23.pump_frame("gi_pump", p) for p in ph]))
    R.append(("paint  paint_frame(gi_painter, g/18)", "gi_painter", [cast23.paint_frame("gi_painter", p) for p in ph]))
    R.append(("pedal  ride_frame(fr_beret, g/14)", "fr_beret", [cast23.ride_frame("fr_beret", p, expr="happy", mouth="smile") for p in ph]))
    R.append(("pedal  ride_frame(fr_cap, g/14, facing=-1)", "fr_cap", [cast23.ride_frame("fr_cap", p, facing=-1, expr="happy", mouth="talk_a") for p in ph]))
    R.append(("blow balloon  balloon_frame(major, g)  (every 9th frame)", "major", [cast23.balloon_frame("major", 9 * i, 1) for i in range(8)]))
    R.append(("laugh bounce  laugh_frame(major, g/10, base)", "major", [cast23.laugh_frame("major", p, cast23.STORY23["major_laugh"][1]) for p in ph]))
    R.append(("wave  wave_frame(gi_driver, g/12)", "gi_driver", [cast23.wave_frame("gi_driver", p) for p in ph]))
    R.append(("carry crate  carry_pose(gi_sound, g/28)", "gi_sound", [cast23.carry_pose("gi_sound", p) for p in ph]))
    R.append(("tiptoe  tiptoe_frame(gi_designer, g/32)", "gi_designer", [cast23.tiptoe_frame("gi_designer", p) for p in ph]))
    R.append(("paddle  paddle_frame(gi_smile, g/24)", "gi_smile", [cast23.paddle_frame("gi_smile", p) for p in ph]))
    R.append(("fall + daze  fall_pose(fr_cap, g/30)", "fr_cap", [cast23.fall_pose("fr_cap", p) for p in ph]))
    R.append(("lift strain  lift_pose(gi_pump, g/16)", "gi_pump", [cast23.lift_pose("gi_pump", p) for p in ph]))
    return R


def sec_cycles(D=56):
    rows = cycle_rows()
    cw, ch = int(3.2 * D), int(4.7 * D)
    lab_h = 26
    W, H = cw * 8, (ch + lab_h) * len(rows) + 40
    o = ['<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG), _title(W, "cycle strips (8 frames per cycle shown; red line = the sprite ground point)")]
    for r, (lab, c, poses) in enumerate(rows):
        y0 = 40 + r * (ch + lab_h)
        o.append('<rect x="0" y="%d" width="%d" height="%d" fill="#2e2a2c"/>' % (y0, W, lab_h))
        o.append('<text x="10" y="%d" font-family="DejaVu Sans" font-size="16" fill="#ffffff">%s</text>' % (y0 + 19, lab))
        for i, pose in enumerate(poses):
            x0 = i * cw
            yy = y0 + lab_h
            o.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x0, yy, cw, ch, BG2 if (i + r) % 2 else BG))
            g, f = _fig(c, pose, "c%d_%d" % (r, i), D, x0 + cw * 0.5, yy + ch - int(0.35 * D), shadow=0.8)
            o.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="%d %d %d %d">%s</svg>' % (x0, yy, cw, ch, x0, yy, cw, ch, g))
            gy = yy + ch - int(0.35 * D)
            o.append('<path d="M%d,%d L%d,%d" stroke="#c83a2e" stroke-width="1.5"/>' % (x0 + 4, gy, x0 + cw - 4, gy))
    return _svgdoc(W, H, "".join(o)), W, H


def _stack(paths, out, width=None, quality=88):
    from PIL import Image
    ims = [Image.open(p).convert("RGB") for p in paths]
    W = width or max(i.size[0] for i in ims)
    ims = [i if i.size[0] == W else i.resize((W, int(i.size[1] * W / i.size[0])), Image.LANCZOS) for i in ims]
    H = sum(i.size[1] for i in ims) + 8 * (len(ims) - 1)
    sheet = Image.new("RGB", (W, H), (46, 42, 44))
    y = 0
    for i in ims:
        sheet.paste(i, (0, y))
        y += i.size[1] + 8
    sheet.save(out, quality=quality)
    return out


def do_sheet():
    t0 = time.time()
    secs = []
    for name, fn in (("sec_heights", sec_heights), ("sec_story", sec_story), ("sec_library", sec_library), ("sec_lift", sec_lift), ("sec_faces", sec_faces), ("sec_props", sec_props)):
        svg, w, h = fn()
        secs.append(_write(svg, w, h, name))
    out = _stack(secs, os.path.join(HERE, "cast_sheet.jpg"), width=2600)
    svg, w, h = sec_cycles()
    cyc = _write(svg, w, h, "sec_cycles")
    out2 = _stack([cyc], os.path.join(HERE, "cycles.jpg"))
    print("sheet: %s, %s (%.1f s)" % (out, out2, time.time() - t0))


# ----------------------------------------------------------------------------- canvas + ground
def all_poses():
    """(cast, pose, kind) for every pose the module ships: story, cycles, generic arm presets."""
    out = [(c, p, "story") for (c, p) in cast23.STORY23.values()]
    for lab, c, poses in cycle_rows():
        out += [(c, p, "cycle") for p in poses]
    for c in cast23.NEW23:
        for i in range(16):
            for mode in ("walk", "run", "sneak", "march"):
                out.append((c, cast23.cycle(c, i / 16.0, mode, 1 if i % 2 else -1, dict(expr="neutral")), "cycle"))
        for a in ("down", "hip", "akimbo", "point", "raised", "forward", "reach_up", "shrug", "wave"):
            for yw in (-0.6, 0.6):
                out.append((c, dict(yaw=yw, arm_r=a, arm_l=a, fx=["sweat", "tears"]), "preset"))
    for c in cast23.GI23:
        for p in (0.0, 0.25, 0.5, 0.75):
            out.append((c, cast23.pump_frame(c, p), "wide"))
            out.append((c, cast23.paint_frame(c, p, -1), "std"))
            out.append((c, cast23.paddle_frame(c, p), "std"))
            out.append((c, cast23.carry_pose(c, p), "std"))
    for c in ("fr_beret", "fr_cap"):
        for p in (0.0, 0.25, 0.5, 0.75):
            for fc in (1, -1):
                out.append((c, cast23.ride_frame(c, p, fc), "wide"))
                out.append((c, cast23.fall_pose(c, p, fc), "wide"))
    for g in range(0, 72, 6):
        out.append(("major", cast23.balloon_frame("major", g, 0), "std"))
    return out


def _is_wide(pose):
    return isinstance(pose, dict) and (isinstance(pose.get("bike23"), dict) or "pump23" in pose)


def measure_canvas():
    U = {}
    for c, p, kind in all_poses():
        f = P.figure(c, p, "q")
        b = f["bbox"]
        fx, fy = f["anchors"]["feet"][0], f["feet_y"]
        key = (c, _is_wide(p))
        u = U.setdefault(key, [1e9, 1e9, -1e9, -1e9])
        u[0] = min(u[0], b[0] - fx)
        u[1] = min(u[1], b[1] - fy)
        u[2] = max(u[2], b[2] - fx)
        u[3] = max(u[3], b[3] - fy)
    return U


def _snap(v, up):
    g = 1.0 / 16.0
    return (math.ceil(v / g - 1e-9) if up else math.floor(v / g + 1e-9)) * g


def do_canvas(verbose=True):
    U = measure_canvas()
    bad = 0
    for (c, wide), u in sorted(U.items()):
        cv = (cast23.CANVAS23_WIDE if wide else cast23.CANVAS23)[c]
        need = (_snap(u[0] - 0.06, False), _snap(u[1] - 0.32, False), _snap(u[2] + 0.06, True), _snap(max(u[3], 0.0) + 0.06, True))
        ok = cv[0] <= u[0] and cv[1] <= u[1] - 0.30 and cv[2] >= u[2] and cv[3] >= u[3]
        bad += 0 if ok else 1
        if verbose or not ok:
            print("%-12s %-5s bbox (%.3f %.3f %.3f %.3f)  suggest %s  have %s  %s" % (c, "wide" if wide else "std", u[0], u[1], u[2], u[3], need, cv, "OK" if ok else "TOO SMALL"))
    print("canvas: %d problem(s)" % bad)
    return bad


def do_ground(px=96):
    """render one sprite per story pose + the cycle frames through stage/sprites.py: the lowest opaque pixel must sit on the ground point
    (gap 0..3 px down to -3 px: the soles' ink, the wheel tyres or the seat reach the ground row)."""
    sp = cast23._sprites()
    out_dir = os.path.join(TMP, "ground")
    jobs, labs = [], []
    seen = set()
    for c, p, kind in all_poses():
        if kind == "preset" or p.get("prop_r") and isinstance(p.get("prop_r"), dict) and p["prop_r"].get("type") == "oar23":
            continue      # the paddle blade dips below the boat floor on purpose
        key = (c, repr(sorted(p.items()))[:4000])
        if key in seen:
            continue
        seen.add(key)
        cv = (cast23.CANVAS23_WIDE if _is_wide(p) else cast23.CANVAS23)[c]
        jobs.append(dict(cast=c, pose=p, px_per_D=px, out=os.path.join(out_dir, "g%04d.png" % len(jobs)), canvas=cv))
        labs.append(c)
    t0 = time.time()
    res = sp.render_sprites(jobs)
    bad = 0
    gaps = []
    for r, lab, j in zip(res, labs, jobs):
        gap = cast23._gap(r)
        gaps.append(gap)
        if gap is None or gap > 3 or gap < -3 or r["clipped"]:
            bad += 1
            print("GROUND/CLIP problem: %s gap %s clipped %s  %s" % (lab, gap, r["clipped"], r["out"]))
    print("ground: %d sprites, gap px min %d max %d, %d problem(s), %.1f s" % (len(res), min(gaps), max(gaps), bad, time.time() - t0))
    sp.close()
    import shutil
    shutil.rmtree(out_dir, ignore_errors=True)       # 50+ MB of check sprites: not kept
    return bad


def do_robust():
    import random
    rnd = random.Random(23)
    junk = [None, "x", -1e9, 1e9, float("nan"), [], {}, (1, 2, 3), True, 0, 2, -3]
    keys = ("hat23", "phones23", "red23", "puff23", "daze23", "bigsweat23", "paint_hands23", "spin23", "t", "bike23", "pump23", "crate23", "balloon23", "ground23", "reach23")
    n = 0
    for c in cast23.NEW23:
        for i in range(60):
            p = dict(yaw=rnd.uniform(-1.2, 1.2), expr=rnd.choice(list(P.EXPRESSIONS)))
            for kk in keys:
                if rnd.random() < 0.4:
                    p[kk] = rnd.choice(junk)
            f = P.figure(c, p, "r")
            assert "nan" not in f["svg"].lower(), (c, p)
            n += 1
    for c, p, kind in all_poses()[:200]:
        a = P.figure(c, p, "d")["svg"]
        b = P.figure(c, p, "d")["svg"]
        assert a == b
        n += 1
    print("robust: %d checks OK" % n)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("sheet", "all"):
        do_sheet()
    if mode in ("canvas", "all"):
        do_canvas(mode == "canvas")
    if mode in ("ground", "all"):
        do_ground()
    if mode in ("robust", "all"):
        do_robust()
