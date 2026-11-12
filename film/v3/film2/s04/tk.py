#!/usr/bin/env python3
"""tk.py -- delivery + QA helpers shared by takes s04, s06, s07 (one owner).

deliver(here, take, shots, plan, cams, ...) builds frames/g_%04d.png from raw/s<shot>/ (internal dissolves mixed with the
smoothstep of v2/shots/anim.smoothstep_mix, whip frames streaked horizontally), take.mkv (ffmpeg libx264rgb crf 6),
meta.json, cues.json, contact.jpg, and returns the QA numbers (heads, pins, pops, camera speeds, hue rows) as text."""
import os, sys, json, glob, shutil, math, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(V3), "v2", "shots"))
sys.path.insert(0, os.path.join(V3, "tools"))
from anim import smoothstep_mix  # noqa: E402
F_PX = 782.22


def raw(here, s, g):
    return os.path.join(here, "raw", "s%d" % s, "g_%04d.png" % g)


def streak(img, px):
    """horizontal motion streak of length px (box kernel), as the whip frames of the hook."""
    import cv2
    n = int(round(px))
    if n < 3:
        return img
    k = np.ones((1, n), np.float32) / n
    return cv2.filter2D(img, -1, k, borderType=cv2.BORDER_REFLECT)


def pan_speed(cam, g):
    """horizontal screen speed (px/frame at 720 wide) of the camera's look direction between g and g+1 (pure pan part)."""
    l0, k0 = cam(g); l1, k1 = cam(g + 1)
    a0 = math.atan2((k0 - l0).x, (k0 - l0).y); a1 = math.atan2((k1 - l1).x, (k1 - l1).y)
    d = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
    return abs(d) * F_PX


def deliver(here, take, order, dissolves, g_first, g_last, meta_extra, cues, cams=None, streak_min=40.0):
    """order: [(shot, g_a, g_b)] frame ranges taken straight from raw/s<shot>; dissolves: [(shot_a, shot_b, d0, n)] mixed
    frames d0..d0+n-1 (they override order)."""
    out = os.path.join(here, "frames")
    shutil.rmtree(out, ignore_errors=True); os.makedirs(out)
    src = {}
    for g in range(g_first, g_last + 1):
        s = None
        for sh, a, b in order:
            if a <= g <= b:
                s = sh
        mix = [d for d in dissolves if d[2] <= g < d[2] + d[3]]
        if mix:
            sa, sb, d0, n = mix[0]
            w = smoothstep_mix(g - d0 + 1, n)
            A = np.asarray(Image.open(raw(here, sa, g)).convert("RGB"), dtype=np.float32)
            B = np.asarray(Image.open(raw(here, sb, g)).convert("RGB"), dtype=np.float32)
            img = np.clip(A * (1 - w) + B * w + 0.5, 0, 255).astype(np.uint8); src[g] = "s%d*%.3f+s%d*%.3f" % (sa, 1 - w, sb, w)
        else:
            img = np.asarray(Image.open(raw(here, s, g)).convert("RGB")); src[g] = "s%d" % s
            if cams and s in cams:
                sp = pan_speed(cams[s], g)
                if sp > streak_min:
                    img = streak(img, min(0.5 * sp, 140)); src[g] += " streak %.0f" % min(0.5 * sp, 140)
        Image.fromarray(img).save(os.path.join(out, "g_%04d.png" % g))
    mkv = os.path.join(here, "take.mkv")
    if os.path.exists(mkv):
        os.remove(mkv)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-start_number", str(g_first), "-i", os.path.join(out, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    rows = []
    for sh in sorted({o[0] for o in order}):
        for js in glob.glob(os.path.join(here, "raw", "s%d" % sh, "g_*.json")):
            rows.append(json.load(open(js)))
    meta = dict(take=take, first_g=g_first, n_frames=g_last - g_first + 1)
    meta.update(meta_extra)
    meta.update(samples=12, resolution=[720, 1280], threads=2,
                s_per_frame_wall_mean=round(float(np.mean([r["wall"] for r in rows])), 2),
                s_per_frame_cpu_mean=round(float(np.mean([r["cpu"] for r in rows])), 2),
                frame_source={str(g): v for g, v in src.items()})
    json.dump(meta, open(os.path.join(here, "meta.json"), "w"), indent=1)
    json.dump(dict(take=take, fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=cues),
              open(os.path.join(here, "cues.json"), "w"), indent=1)
    # contact sheet: 16 evenly spaced final frames, label strip above each picture
    gs = [int(round(g_first + i * (g_last - g_first) / 15.0)) for i in range(16)]
    w, h, lab, cols = 270, 480, 18, 8
    S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(out, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:16]), fill=(255, 255, 255))
    S.save(os.path.join(here, "contact.jpg"), quality=88)
    return src, rows


def cue(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw)
    return e


def qa_text(here, shot_ranges, rows, cams, g_first, g_last, label):
    import hue_report as H
    import io, contextlib
    L = []
    for s, (a, b) in shot_ranges.items():
        rs = [r for r in rows if r["shot"] == s and a <= r["g"] <= b]
        L.append("shot %d (g %d..%d, %d raw frames): render wall %.2f s, cpu %.2f s per frame; retried %s"
                 % (s, a, b, len(rs), np.mean([r["wall"] for r in rs]), np.mean([r["cpu"] for r in rs]), [r["g"] for r in rs if r.get("retried")]))
        names = sorted({n for r in rs for n in r.get("heads", {})})
        for n in names:
            hh = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
            w = [v["w"] for g, v in hh]; y = [v["y"] for g, v in hh]; x = [v["x"] for g, v in hh]
            low = [g for g, v in hh if v["y"] + v["w"] / 2 > 880 and 0 < v["x"] < 720]
            L.append("  %-8s head w %4.0f..%4.0f px, centre x %5.0f..%5.0f, centre y %5.0f..%5.0f (%.2f..%.2f H); on-screen head bottom below 880: %s"
                     % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, (low[:4], len(low)) if low else "none"))
        pe = [max(v) for r in rs for v in r.get("pin_err", {}).values()] if rs and isinstance(rs[0].get("pin_err"), dict) else []
        if pe:
            L.append("  hand pins on the ropes: max solve error %.3f D" % max(pe))
    # camera speeds
    for s, cam in cams.items():
        a, b = shot_ranges[s]
        v = []
        for g in range(a, b):
            l0, k0 = cam(g); l1, k1 = cam(g + 1)
            m = 0.0
            from mathutils import Vector
            for sx in (-1, 0, 1):
                for sy in (-1, 0, 1):
                    def basis(loc, look):
                        f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); return f, r, r.cross(f)
                    f0, r0, u0 = basis(l0, k0)
                    p = l0 + (f0 + r0 * (sx * 360 / F_PX) + u0 * (sy * 640 / F_PX)) * 8.0

                    def proj(p, loc, look):
                        f, r, u = basis(loc, look); d = p - loc; z = d.dot(f)
                        return Vector((360 + F_PX * d.dot(r) / z, 640 - F_PX * d.dot(u) / z))
                    m = max(m, (proj(p, l0, k0) - proj(p, l1, k1)).length)
            v.append(m)
        st, run = [], 0
        for i, x in enumerate(v + [9]):
            if x < 0.25:
                run += 1
            else:
                if run > 0:
                    st.append((a + i - run, run))
                run = 0
        lin, run = [], 0
        for i in range(len(v) - 1):
            if v[i] > 1.0 and abs(v[i + 1] - v[i]) / v[i] < 0.02:
                run += 1
            else:
                if run >= 3:
                    lin.append((a + i - run, run + 1))
                run = 0
        pk = int(np.argmax(v))
        L.append("camera shot %d (points at 8 D): min %.2f, median %.2f, peak %.1f px/frame at g %d; static runs (<0.25 px) %s; constant-speed runs (>=4 f) %s"
                 % (s, min(v), sorted(v)[len(v) // 2], v[pk], a + pk, st or "none", lin or "none"))
    # pops
    fs = [os.path.join(here, "frames", "g_%04d.png" % g) for g in range(g_first, g_last + 1)]
    prev, d = None, []
    for f in fs:
        im = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append(float(np.abs(im - prev).mean()))
        prev = im
    pops = []
    for i, v in enumerate(d):
        p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
        if v > 1.8 * p and v > 1.8 * n and v > 1.0:
            pops.append((g_first + i, g_first + i + 1, round(v, 1)))
    L.append("popcheck (g -> g+1, mean abs change): %s" % pops)
    L.append("near-still transitions (< 0.35 levels): %s" % [g_first + i for i, v in enumerate(d) if v < 0.35])
    bad = []
    for f in fs:
        im = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
        if ((im[..., 0] > 200) & (im[..., 1] < 40) & (im[..., 2] > 200)).mean() > 0.002:
            bad.append(os.path.basename(f))
    L.append("magenta-texture frames: %s" % bad)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for s, (a, b) in shot_ranges.items():
            H.row("%s shot %d (g %d-%d)" % (label, s, a, b), [os.path.join(here, "frames", "g_%04d.png" % g) for g in range(a, b + 1)])
        H.row("%s all (g %d-%d)" % (label, g_first, g_last), fs)
    L.append(buf.getvalue())
    return "\n".join(L)
