#!/usr/bin/env python3
"""deliver.py -- raw/s<id>/g_%04d.png (+ .json) -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv,
and work/qa.txt (head sizes / caption band, pops, black / magenta frames, hue rows, s per frame).  Config in take.json.
    python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import hue_report as HR

cfg = json.load(open(os.path.join(HERE, "take.json")))
g_first, g_last = cfg["first_g"], cfg["last_g"]
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for g in range(g_first, g_last + 1):
    sh = [s for s, (a, b) in cfg["raw_ranges"].items() if a <= g <= b][0]
    p = os.path.join(HERE, "raw", "s%s" % sh, "g_%04d.png" % g)
    shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = sh
    rows.append(json.load(open(p[:-4] + ".json")))
N = g_last - g_first + 1
walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
meta = dict(cfg["meta"]); meta.update(first_g=g_first, n_frames=N, last_g=g_last, samples=12, resolution=[720, 1280], threads=2, fps=30,
                                      s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
                                      frame_source={str(g): v for g, v in src.items()})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
ev = []
for c in cfg["cues"]:
    g0, g1, label, kind = c[:4]
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
    if len(c) > 4:
        e["peak_frame"] = c[4]
    ev.append(e)
json.dump(dict(take=cfg["meta"]["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 16 (or 24) frames
nc = 24 if N > 150 else 16
gs = [g_first + int(round(i * (N - 1) / float(nc - 1))) for i in range(nc)]
w, h, lab, cols = 270, 480, 18, 8
rws = (nc + cols - 1) // cols
S = Image.new("RGB", (cols * w, rws * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    hd = "handle" if (g < cfg["g0"] or g >= cfg["g1"]) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s %s" % (g, g / 30.0, src[g], hd), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
# compare: pairs (g, ref path)
w, h, lab = 360, 640, 20
P = cfg["compare"]
Cm = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, ref in P:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s g %d (%.2f s)" % (cfg["meta"]["take"], g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref " + ref, fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(g_first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)

# QA numbers
os.makedirs(os.path.join(HERE, "work"), exist_ok=True)
q = open(os.path.join(HERE, "work", "qa.txt"), "w")
pr = lambda *a: (print(*a), print(*a, file=q))
for sh in sorted(cfg["raw_ranges"], key=int):
    rs = [r for r in rows if str(r["shot"]) == sh]
    names = sorted({n for r in rs for n in r.get("heads", {})})
    pr("shot %s: %d frames (g %d..%d)" % (sh, len(rs), rs[0]["g"], rs[-1]["g"]))
    for n in names:
        hs = [(r["g"], r["heads"][n]) for r in rs if n in r["heads"]]
        vis = [(g, hh) for g, hh in hs if -hh["w"] / 2 < hh["x"] < 720 + hh["w"] / 2 and -hh["w"] / 2 < hh["y"] < 1280 + hh["w"] / 2]
        if not vis:
            continue
        ww = [hh["w"] for g, hh in vis]; yy = [hh["y"] for g, hh in vis]; xx = [hh["x"] for g, hh in vis]
        low = [g for g, hh in vis if hh["y"] + hh["w"] / 2 > 880]
        pr("  %-6s head w %4.0f..%4.0f px, centre x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
           % (n, min(ww), max(ww), min(xx), max(xx), min(yy), max(yy), min(yy) / 1280, max(yy) / 1280, (low[0], low[-1], len(low)) if low else "none"))
pr("render: wall %.2f s, cpu %.2f s per frame (mean); retried: %s" % (np.mean(walls), np.mean(cpus), [r["g"] for r in rows if r.get("retried")]))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(g_first, g_last + 1)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = []
for i, v in enumerate(d):
    p = d[i - 1] if i else v; n = d[i + 1] if i + 1 < len(d) else v
    if v > 1.8 * p and v > 1.8 * n and v > 1.0:
        pops.append((g_first + i, g_first + i + 1, round(v, 1)))
pr("popcheck (g -> g+1, change):", pops, " planned framing changes at", cfg.get("cuts", []))
pr("near-still transitions (< 0.35 levels):", [g_first + i for i, v in enumerate(d) if v < 0.35])
pr("frame change median %.2f, max %.2f levels" % (float(np.median(d)), max(d)))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
pr("magenta / black frames:", bad)
q.close()
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
    for lab_, a, b in cfg["hue_rows"]:
        HR.row(lab_, [os.path.join(OUT, "g_%04d.png" % g) for g in range(a, b + 1)])
    HR.row("ref a t0001 t0046 t0047", [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % t) for t in (1, 46, 47)])
print(buf.getvalue()); open(os.path.join(HERE, "work", "qa.txt"), "a").write(buf.getvalue())
print("delivered %d frames g %d..%d + take.mkv" % (N, g_first, g_last))
