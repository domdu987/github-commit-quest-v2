#!/usr/bin/env python3
"""deliver.py -- raw/s<id>/g_*.png -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, take.mkv (libx264rgb crf 6), qa.txt.
Take description lives in TAKE (take.json next to this file).  python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
TK = json.load(open(os.path.join(HERE, "take.json")))
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
first, last = TK["first_g"], TK["last_g"]
rows, src = [], {}
for g in range(first, last + 1):
    sid = [int(k) for k, (a, b) in TK["setups"].items() if a <= g <= b][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = last - first + 1
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
meta = dict(TK["meta"]); meta.update(first_g=first, n_frames=N, samples=12, resolution=[720, 1280], threads=2, fps=30,
                                     s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
                                     frame_source={str(g): v for g, v in src.items()})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = []
for g0, g1, kind, label, *pk in TK["cues"]:
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
    if pk: e["peak_frame"] = pk[0]
    cues.append(e)
json.dump(dict(take=TK["meta"]["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film9/audio/narration.wav at +0.10 s", cues=cues),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)
gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    hd = " handle" if g < meta["g0"] or g >= meta["g1"] else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  set-up %d%s" % (g, g / 30.0, src[g], hd), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
# ---- QA numbers
import hue_report as HR
q = []
for sid, (a, b) in TK["setups"].items():
    rs = [r for r in rows if a <= r["g"] <= b]
    for n in sorted({n for r in rs for n in r["heads"]}):
        hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
        low = [g for g, hh in hs if hh["y"] + hh["w"] / 2 > 880]
        q.append("set-up %s %-4s head w %3.0f..%3.0f px, centre y %4.0f..%4.0f (%.2f..%.2f H), x %3.0f..%3.0f; bottom below 880: %s" % (
            sid, n, min(hh["w"] for _, hh in hs), max(hh["w"] for _, hh in hs), min(hh["y"] for _, hh in hs), max(hh["y"] for _, hh in hs),
            min(hh["y"] for _, hh in hs) / 1280, max(hh["y"] for _, hh in hs) / 1280, min(hh["x"] for _, hh in hs), max(hh["x"] for _, hh in hs),
            (low[0], low[-1], len(low)) if low else "none"))
    q.append("set-up %s render: wall %.2f s, cpu %.2f s per frame" % (sid, np.mean([r["wall"] for r in rs]), np.mean([r["cpu"] for r in rs])))
prev = None; d = []
for g in range(first, last + 1):
    a = np.asarray(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None: d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0: pops.append((first + i, first + i + 1, round(v, 1)))
still = [first + i for i, v in enumerate(d) if v < 0.35]
runs, cur = [], []
for s in still:
    if cur and s == cur[-1] + 1: cur.append(s)
    else:
        if cur: runs.append(cur)
        cur = [s]
if cur: runs.append(cur)
q.append("popcheck: pops %s" % pops)
q.append("near-still transitions (< 0.35 levels): %d, longest run %d frames %s" % (len(still), max([len(r) for r in runs] or [0]), [ (r[0], r[-1]) for r in runs if len(r) > 3]))
q.append("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for g in range(first, last + 1):
    a = np.asarray(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2: bad.append(g)
q.append("magenta / black frames: %s" % bad)
open(os.path.join(HERE, "qa.txt"), "w").write("\n".join(q) + "\n")
print("\n".join(q))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':40s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    for sid, (a, b) in TK["setups"].items():
        HR.row("%s set-up %s (g %d-%d)" % (TK["meta"]["take"], sid, a, b), [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1, 3)])
open(os.path.join(HERE, "qa.txt"), "a").write(buf.getvalue()); print(buf.getvalue())
print("delivered %d frames + take.mkv (%.1f MB)" % (N, os.path.getsize(mkv) / 1e6))
