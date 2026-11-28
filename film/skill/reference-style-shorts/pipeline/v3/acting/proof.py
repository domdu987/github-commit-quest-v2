#!/usr/bin/env python3
"""proof.py -- strips, sheet and continuity test of acting.py (no Blender).

    python3 proof.py strips [name ...]   # strips/<name>.png: 12 frames through the puppet (Chromium sprites)
    python3 proof.py sheet               # sheet.jpg: all strips stacked
    python3 proof.py continuity          # continuity.json + continuity.txt: anchor steps and pixel changes per frame
    python3 proof.py compare             # compare.jpg: strips beside the reference frames of the same acting
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acting as A                                         # noqa: E402
sys.path.insert(0, os.path.join(A.PROJ, "v3", "stage"))
import sprites                                             # noqa: E402
from PIL import Image, ImageDraw, ImageFont               # noqa: E402
import numpy as np                                         # noqa: E402

P = A.P
STRIPS = os.path.join(HERE, "strips")
TMP = os.path.join(A.PROJ, "v3", "tmp", "acting")
PPD = 96                                                   # px per D in the strips
BG = {"boss": "#b5484c", "hero": "#b5484c", "senior_a": "#b5484c", "senior_b": "#b5484c",
      "beach_man": "#d9b27a", "beach_woman": "#d9b27a"}
FONT = None
for fp in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",):
    if os.path.exists(fp):
        FONT = ImageFont.truetype(fp, 13)


def frames_of(dur, n=12):
    N = int(round(dur * A.FPS))
    return [int(round(i * N / float(n - 1))) for i in range(n)]


def overlay_for(cast, pose):
    if pose.get("_notes"):
        f = P.figure(cast, pose, "o")
        return A.note_glyphs_svg(pose["_notes"], f["anchors"]["mouth"], 1 if pose.get("yaw", 0) >= 0 else -1)
    return ""


def canvas_union(cast, poses, margin=0.2):
    c = [1e9, 1e9, -1e9, -1e9]
    for p in poses:
        b = sprites.bbox_card(cast, p)
        c = [min(c[0], b[0]), min(c[1], b[1]), max(c[2], b[2]), max(c[3], b[3])]
        if p.get("_notes"):
            c[1] = min(c[1], b[1] - 1.0)
            c[2] = max(c[2], b[2] + 0.6)
            c[0] = min(c[0], b[0] - 0.6)
    g = 1 / 16.0
    return (math.floor((c[0] - margin) / g) * g, math.floor((c[1] - margin) / g) * g,
            math.ceil((c[2] + margin) / g) * g, math.ceil((c[3] + margin) / g) * g)


def render_seq(name, frames, ppd=PPD, sub="seq"):
    cast, fn, dur = A.catalogue()[name]
    poses = [fn(f / float(A.FPS)) for f in frames]
    cv = canvas_union(cast, poses)
    d = os.path.join(TMP, sub, name)
    os.makedirs(d, exist_ok=True)
    jobs = [dict(cast=cast, pose=p, px_per_D=ppd, canvas=cv, out=os.path.join(d, "f_%04d.png" % f), overlay=overlay_for(cast, p))
            for f, p in zip(frames, poses)]
    res = sprites.render_sprites(jobs)
    return cast, poses, res, cv


def strip(name):
    cast, fn, dur = A.catalogue()[name]
    frames = frames_of(dur)
    cast, poses, res, cv = render_seq(name, frames)
    lift_max = max(p.get("_lift", 0.0) for p in poses)
    w, h = res[0]["size"]
    pad = int(lift_max * PPD) + 4
    cw, ch = w, h + pad + 20
    img = Image.new("RGB", (cw * len(frames), ch + 22), BG[cast])
    dr = ImageDraw.Draw(img)
    for i, (f, p, r) in enumerate(zip(frames, poses, res)):
        spr = Image.open(r["out"]).convert("RGBA")
        lift = int(round(p.get("_lift", 0.0) * PPD))
        x = i * cw
        y = pad + 20 - lift
        gy = pad + 20 + int(r["origin_px"][1])
        dr.line([(x, gy), (x + cw, gy)], fill="#3a2832", width=1)
        img.paste(spr, (x, y), spr)
        lab = "f%02d %.2fs" % (f, f / 30.0)
        mo = p.get("mouth") or ""
        dr.text((x + 4, 3), lab, fill="#ffffff", font=FONT)
        dr.text((x + 4, ch + 3), "%s %s%s" % (p.get("expr", ""), mo, " b%d" % p["blink"] if p.get("blink") else ""), fill="#ffffff", font=FONT)
        dr.line([(x + cw - 1, 0), (x + cw - 1, ch + 22)], fill="#00000040", width=1)
    os.makedirs(STRIPS, exist_ok=True)
    out = os.path.join(STRIPS, name + ".png")
    img.save(out)
    return out


def sheet():
    names = list(A.catalogue().keys())
    rows = []
    for n in names:
        p = os.path.join(STRIPS, n + ".png")
        im = Image.open(p).convert("RGB")
        s = 150.0 / im.height
        im = im.resize((int(im.width * s), 150), Image.LANCZOS)
        rows.append((n, im))
    W = max(r[1].width for r in rows) + 170
    cols = 2
    per = (len(rows) + cols - 1) // cols
    H = per * 152
    out = Image.new("RGB", (W * cols, H), "#222")
    dr = ImageDraw.Draw(out)
    for i, (n, im) in enumerate(rows):
        c, r = i // per, i % per
        out.paste(im, (c * W + 170, r * 152))
        dr.text((c * W + 6, r * 152 + 60), n, fill="#fff", font=FONT)
    out.save(os.path.join(HERE, "sheet.jpg"), quality=88)


# ----------------------------------------------------------------------------- continuity
ANCH = ("head", "hand_r", "hand_l", "prop_tip_r", "prop_tip_l", "foot_r", "foot_l", "feet", "hip", "chest", "hat_top",
        "elbow_r", "elbow_l", "knee_r", "knee_l")
DISCRETE = ("expr", "mouth", "blink", "hat_off", "gaze")


def _key(p):
    pr = tuple((k, str(p.get(k))) for k in DISCRETE)
    props = tuple(str((p.get("prop_r") or {}).get("type") if isinstance(p.get("prop_r"), dict) else p.get("prop_r")) for _ in [0]) + \
        tuple(str((p.get("prop_l") or {}).get("type") if isinstance(p.get("prop_l"), dict) else p.get("prop_l")) for _ in [0])
    shapes = tuple(str(p[a].get("shape")) if isinstance(p.get(a), dict) else str(p.get(a)) for a in ("arm_r", "arm_l"))
    fx = tuple(sorted(str(x if isinstance(x, str) else x.get("type")) for x in p.get("fx", [])))
    return pr + props + shapes + fx


# fast moves that are meant to be fast (one-frame or two-frame actions of the plan); flags inside them are reported as
# intended, not as pops
INTENDED = {
    "boss_pointer_whack": [(13, 17, "whack: tip comes down in 3 frames (cubic in), contact squash")],
    "boss_read_tape": [(12, 15, "tape torn: hands part in 3 frames")],
    "beach_palm_out": [(10, 23, "rain drops land on the palm: 1-frame dips")],
    "man_jump_run": [(0, 12, "jump scare: squash 2, leap 2, hang 2, land 2 (LOOK_SPEC 5.5.9)")],
    "woman_jump_run": [(0, 12, "jump scare: squash 2, leap 2, hang 2, land 2 (LOOK_SPEC 5.5.9)")],
    "boss_frozen_purple": [(0, 99, "steam effect loop (puppet fx) and eye twitch frames")],
    "beach_stretch": [(2, 12, "reviewed frame by frame: anticipation dip, then eyes close (happy) on the rise; no pop")],
    "beach_shade": [(2, 11, "reviewed: hand rises continuously; the arm changes draw layer (front -> top) at mid-move")],
    "woman_peg_towel": [(16, 19, "reviewed: the peg push (2-frame squash)")],
    "boss_stamp_thrust": [(19, 24, "reviewed: smug nod after the thrust")],
}


def continuity(names=None, step_lim=0.20, pix_ratio=2.6):
    """every frame of every function: (1) anchor travel per frame in D (feet-relative, + _lift), flagged above step_lim
    unless the frame is an intended jump (jump_run's leap, a face/prop swap frame); (2) pixel change between
    consecutive sprites at 48 px/D, flagged where it is over pix_ratio x the median change of the sequence and both
    neighbours AND no drawing swap (expr, mouth, blink, prop, hand shape, fx) happens on that frame."""
    rep = {}
    for name in (names or list(A.catalogue().keys())):
        cast, fn, dur = A.catalogue()[name]
        N = int(round(dur * A.FPS))
        frames = list(range(N + 1))
        poses = [fn(f / 30.0) for f in frames]
        anc = []
        for p in poses:
            f = P.figure(cast, p, "c")
            fx, fy = f["anchors"]["feet"][0], f["feet_y"]
            lift = p.get("_lift", 0.0)
            anc.append({a: (f["anchors"][a][0] - fx, f["anchors"][a][1] - fy - lift) for a in ANCH})
        steps = []
        flags = []
        for i in range(1, len(poses)):
            m = max(math.hypot(anc[i][a][0] - anc[i - 1][a][0], anc[i][a][1] - anc[i - 1][a][1]) for a in ANCH if a != "hat_top")
            steps.append(m)
        swaps = [False] + [_key(poses[i]) != _key(poses[i - 1]) for i in range(1, len(poses))]
        for i in range(1, len(poses)):
            m = steps[i - 1]
            prv = steps[i - 2] if i >= 2 else 0.0
            nxt = steps[i] if i < len(steps) else 0.0
            if swaps[i] or (i + 1 < len(swaps) and swaps[i + 1]) or swaps[i - 1]:
                continue                                    # a drawing swap on this frame or next to it: intended
            if m > 0.08 and m > 2.2 * prv and m > 2.2 * nxt:
                flags.append(dict(frame=i, kind="pop", step=round(m, 3)))          # one isolated jump
            elif m > step_lim and prv < 0.25 * m:
                flags.append(dict(frame=i, kind="unEased_start", step=round(m, 3), prev=round(prv, 3)))
            elif m > step_lim:
                flags.append(dict(frame=i, kind="fast", step=round(m, 3)))         # fast but eased (info)
        # pixels
        cast_, poses_, res, cv = render_seq(name, frames, ppd=48, sub="cont")
        ims = [np.asarray(Image.open(r["out"]).convert("RGBA"), dtype=np.float32) for r in res]
        diffs = [float(np.mean(np.abs(ims[i] - ims[i - 1]))) for i in range(1, len(ims))]
        med = float(np.median(diffs)) if diffs else 0.0
        for i in range(1, len(diffs) - 1):
            d = diffs[i]
            swap = _key(poses[i + 1]) != _key(poses[i])
            near_swap = _key(poses[i]) != _key(poses[i - 1]) or (i + 2 < len(poses) and _key(poses[i + 2]) != _key(poses[i + 1]))
            if d > pix_ratio * max(med, 0.05) and d > 1.8 * diffs[i - 1] and d > 1.8 * diffs[i + 1] and not swap and not near_swap:
                flags.append(dict(frame=i + 1, kind="pixel", change=round(d, 3), median=round(med, 3)))
        for fl in flags:
            for (a, b, why) in INTENDED.get(name, []):
                if a <= fl["frame"] <= b:
                    fl["intended"] = why
        nswap = sum(1 for i in range(1, len(poses)) if _key(poses[i]) != _key(poses[i - 1]))
        rep[name] = dict(pops=sum(1 for f in flags if f["kind"] in ("pop", "unEased_start", "pixel") and "intended" not in f), frames=len(frames), max_anchor_step=round(max(steps), 3), median_anchor_step=round(float(np.median(steps)), 4),
                         pixel_median=round(med, 3), pixel_max=round(max(diffs), 3), swaps=nswap, flags=flags)
    return rep


def compare():
    refs = [("a/t46.5.jpg", "boss_talk"), ("a/t16.0.jpg", "boss_shocked"), ("b/t05.0.jpg", "man_shocked"),
            ("b/t07.0.jpg", "senior_a_laugh"), ("a/t44.0.jpg", "boss_whistle_stroll"), ("b/t44.5.jpg", "boss_walk")]
    rows = []
    for rf, n in refs:
        ref = Image.open(os.path.join(A.PROJ, "ref", rf)).convert("RGB")
        ref = ref.resize((int(ref.width * 400 / ref.height), 400))
        st = Image.open(os.path.join(STRIPS, n + ".png")).convert("RGB")
        s = 400.0 / st.height
        st = st.resize((int(st.width * s), 400), Image.LANCZOS)
        row = Image.new("RGB", (ref.width + 8 + st.width, 400), "#111")
        row.paste(ref, (0, 0))
        row.paste(st, (ref.width + 8, 0))
        rows.append(row)
    W = max(r.width for r in rows)
    out = Image.new("RGB", (W, 404 * len(rows)), "#111")
    for i, r in enumerate(rows):
        out.paste(r, (0, i * 404))
    out.save(os.path.join(HERE, "compare.jpg"), quality=85)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "strips"
    if cmd == "strips":
        names = sys.argv[2:] or list(A.catalogue().keys())
        for n in names:
            print(strip(n))
    elif cmd == "sheet":
        sheet()
    elif cmd == "continuity":
        rep = continuity(sys.argv[2:] or None)
        json.dump(rep, open(os.path.join(HERE, "continuity.json"), "w"), indent=1)
        lines = ["%-22s POPS %d  frames %3d  max step %.3f D  median %.4f D  pixel med %.3f max %.3f  swaps %2d  flags %d %s"
                 % (n, r["pops"], r["frames"], r["max_anchor_step"], r["median_anchor_step"], r["pixel_median"], r["pixel_max"], r["swaps"],
                    len(r["flags"]), [f for f in r["flags"] if f["kind"] != "fast"][:4]) for n, r in rep.items()]
        open(os.path.join(HERE, "continuity.txt"), "w").write("\n".join(lines) + "\n")
        print("\n".join(lines))
    elif cmd == "compare":
        compare()
    sprites.close()
