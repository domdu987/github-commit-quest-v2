#!/usr/bin/env python3
"""deliver_lib.py -- shared delivery helpers for takes s12, s14, s15 (one owner): dissolve mix, contact sheet, take.mkv,
camera-motion QA, popcheck, magenta check, hue rows, head-position summary."""
import os, sys, json, glob, math, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw

LIB = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(LIB))
PROJ = os.path.dirname(V3)
sys.path.insert(0, os.path.join(V3, "tools"))
sys.path.insert(0, os.path.join(PROJ, "v2", "shots"))
from anim import smoothstep_mix                          # noqa: E402
F = 782.22


def load(p):
    return np.asarray(Image.open(p).convert("RGB"), dtype=np.float32)


def save(a, p):
    Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).save(p)


def mix_files(pa, pb, w, dst):
    save(load(pa) * (1 - w) + load(pb) * w, dst)


def contact(frames_dir, gs, labels, out, cols=8, w=270, h=480, lab=18):
    rows = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        x, y = (i % cols) * w, (i // cols) * (h + lab)
        S.paste(Image.open(os.path.join(frames_dir, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
        dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, labels.get(g, "")[:14]), fill=(255, 255, 255))
    S.save(out, quality=88)


def encode(take_dir, first_g):
    out = os.path.join(take_dir, "take.mkv")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first_g), "-i",
           os.path.join(take_dir, "frames", "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", out]
    subprocess.check_call(cmd)
    n = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                     "stream=nb_read_frames", "-of", "csv=p=0", out]).decode().strip())
    return out, n


def _basis(loc, look):
    from mathutils import Vector
    f = (look - loc).normalized(); r = f.cross(Vector((0, 0, 1))).normalized(); u = r.cross(f)
    return f, r, u


def cam_speeds(camf, g0, g1, depth=12.0):
    """px per frame of the fastest of 9 screen points re-projected at `depth` D (720x1280)."""
    from mathutils import Vector
    out = []
    for g in range(g0, g1):
        l0, k0 = camf(g); l1, k1 = camf(g + 1)
        f, r, u = _basis(l0, k0); f1, r1, u1 = _basis(l1, k1)
        m = 0.0
        for sx in (-1, 0, 1):
            for sy in (-1, 0, 1):
                p = l0 + (f + r * (sx * 360 / F) + u * (sy * 640 / F)) * depth
                d = p - l1; z = d.dot(f1)
                b = Vector((360 + F * d.dot(r1) / z, 640 - F * d.dot(u1) / z))
                a = Vector((360 + sx * 360, 640 - sy * 640))
                m = max(m, (a - b).length)
        out.append((g, m))
    return out


def _runs(flags):
    o, s = [], None
    for i, fl in enumerate(list(flags) + [False]):
        if fl and s is None: s = i
        if not fl and s is not None: o.append((s, i - 1)); s = None
    return o


def cam_report(camf, g0, g1, depth=12.0):
    sp = cam_speeds(camf, g0, g1, depth)
    v = [m for g, m in sp]
    st = [(sp[a][0], sp[b][0] + 1) for a, b in _runs([x < 0.25 for x in v]) if b - a + 1 > 0]
    rel = [abs(v[i + 1] - v[i]) / max(v[i], 1e-6) for i in range(len(v) - 1)]
    lin = [(sp[a][0], sp[b][0] + 1) for a, b in _runs([(rel[i] < 0.02 and v[i] > 1.0) for i in range(len(rel))]) if b - a >= 3]
    pk = max(sp, key=lambda x: x[1])
    return dict(min_px=round(min(v), 3), median_px=round(sorted(v)[len(v) // 2], 2), peak=(pk[0], round(pk[1], 1)),
                static_runs=st, linear_runs=lin)


def popcheck(frames_dir, g0, g1):
    prev = None; d = []
    for g in range(g0, g1 + 1):
        a = np.asarray(Image.open(os.path.join(frames_dir, "g_%04d.png" % g)).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
        if prev is not None:
            d.append((g - 1, float(np.abs(a - prev).mean())))
        prev = a
    pops = []
    for i, (g, v) in enumerate(d):
        p = d[i - 1][1] if i else v; n = d[i + 1][1] if i + 1 < len(d) else v
        if v > 1.8 * p and v > 1.8 * n and v > 1.0:
            pops.append((g, g + 1, round(v, 1)))
    still = [g for g, v in d if v < 0.35]
    bad = []
    for g in range(g0, g1 + 1):
        a = np.asarray(Image.open(os.path.join(frames_dir, "g_%04d.png" % g)).convert("RGB").resize((90, 160)), dtype=np.int16)
        if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002:
            bad.append(g)
    return pops, still, bad


def hue_rows(rows):
    """rows: [(label, [files])] -> text table (hue_report.row prints; capture it)."""
    import io, contextlib
    import hue_report as H
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in H.NAMES) + "   sat  val dark")
        for lab, fl in rows:
            H.row(lab, fl)
    return buf.getvalue()


def heads_summary(rows, names=None):
    """rows: list of raw json dicts with 'heads' -> text lines."""
    out = []
    names = names or sorted({n for r in rows for n in r.get("heads", {})})
    for n in names:
        rr = [r for r in rows if n in r.get("heads", {})]
        if not rr:
            continue
        w = [r["heads"][n]["w"] for r in rr]; y = [r["heads"][n]["y"] for r in rr]; x = [r["heads"][n]["x"] for r in rr]
        inside = [r for r in rr if -r["heads"][n]["w"] / 2 < r["heads"][n]["x"] < 720 + r["heads"][n]["w"] / 2]
        low = [r["g"] for r in inside if r["heads"][n]["y"] + r["heads"][n]["w"] / 2 > 880]
        out.append("%-6s head w %4.0f..%4.0f px, centre x %5.0f..%5.0f, centre y %4.0f..%4.0f (%.2f..%.2f H); on-screen frames with head bottom below y 880: %s"
                   % (n, min(w), max(w), min(x), max(x), min(y), max(y), min(y) / 1280, max(y) / 1280, low if low else "none"))
    return out
