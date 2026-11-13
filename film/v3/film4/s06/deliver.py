#!/usr/bin/env python3
"""deliver.py -- from raw/p<k>/g_%04d.png build frames/g_%04d.png, meta.json, contact.jpg, compare.jpg, take.mkv and the QA numbers
(work/qa.txt: heads per part, heads below y 880, pops, black / magenta frames, hue rows, s per frame).
The take's own numbers come from take_cfg.py in this folder.   python3 deliver.py [--no-mkv]"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(PROJ, "v3", "tools"))
import take_cfg as C
import hue_report as HR

RAW = os.path.join(HERE, "raw"); OUT = os.path.join(HERE, "frames"); WORK = os.path.join(HERE, "work")
for d in (OUT, WORK):
    os.makedirs(d, exist_ok=True)
first, last = C.FIRST_G, C.LAST_G
src = {}
for g in range(first, last + 1):
    k = max(k for k, (a, b) in C.PARTS.items() if a <= g <= b and True) if any(a <= g <= b for a, b in C.PARTS.values()) else None
    if k is None:
        raise SystemExit("no part renders g %d" % g)
    p = os.path.join(RAW, "p%d" % k, "g_%04d.png" % g)
    if not os.path.exists(p):
        raise SystemExit("missing " + p)
    shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = "p%d" % k

rows = {}
for k in C.PARTS:
    for js in glob.glob(os.path.join(RAW, "p%d" % k, "g_*.json")):
        m = json.load(open(js))
        if first <= m["g"] <= last:
            rows[(k, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]
meta = {"take": C.TAKE, "shots": C.SHOTS, "first_g": first, "n_frames": last - first + 1, "g0": C.G0, "g1": C.G1,
        "handle_in": C.G0 - first, "handle_out": last + 1 - C.G1,
        "transition_in": C.TRANS_IN, "transition_out": C.TRANS_OUT, "transitions": C.TRANSITIONS,
        "parts": {str(k): dict(range=list(v), what=C.PART_NOTES[k]) for k, v in C.PARTS.items()},
        "shot_ranges": C.SHOT_RANGES, "set": C.SET_NOTE, "dof": C.DOF, "narration": "film4/audio/narration_bankky.wav", "light": "DAY",
        "cast": C.CAST, "samples": 12, "resolution": [720, 1280], "threads": 2,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "encode": "ffmpeg -framerate 30 -start_number %d -i frames/g_%%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv" % first,
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
for (g0, g1, label, kind, kw) in C.CUES:
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw)
    ev.append(e)
ev.sort(key=lambda e: (e["frame"], e["kind"]))
json.dump(dict(take=C.TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film4/audio/narration_bankky.wav at +0.10 s, captions_bankky.json",
               cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact: 16 evenly spaced frames, label strip above each picture
N = last - first + 1
gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: per part one final frame beside its reference frame (ref a tNNNN), same size
w, h, lab = 360, 640, 20
P = C.COMPARE
Cm = Image.new("RGB", (len(P) * 2 * w + (len(P) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for label, g, tref in P:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "%s  g %d (%.2f s)" % (label, g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d (%d s)" % (tref, (tref - 1) // 2), fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

# QA numbers
q = []
for k, (a, b) in C.PARTS.items():
    rr = sorted([m for (kk, g), m in rows.items() if kk == k], key=lambda m: m["g"])
    q.append("part %d (g %d..%d, %d frames): wall %.2f s, cpu %.2f s per frame; retried %s"
             % (k, a, b, len(rr), np.mean([m["wall"] for m in rr]), np.mean([m["cpu"] for m in rr]), [m["g"] for m in rr if m.get("retried")]))
    for n in sorted({n for m in rr for n in m["heads"]}):
        hs = [(m["g"], m["heads"][n]) for m in rr if n in m["heads"]]
        ww = [hh["w"] for _, hh in hs]; yy = [hh["y"] for _, hh in hs]; xx = [hh["x"] for _, hh in hs]
        low = [g for g, hh in hs if hh["y"] + hh["w"] / 2 > 880]
        q.append("  %-8s head w %4.0f..%4.0f px, x %4.0f..%4.0f, y %4.0f..%4.0f (%.2f..%.2f H); bottom below 880: %s"
                 % (n, min(ww), max(ww), min(xx), max(xx), min(yy), max(yy), min(yy) / 1280, max(yy) / 1280, (low[0], low[-1], len(low)) if low else "none"))
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(first, last + 1)]
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
        pops.append((first + i, first + i + 1, round(v, 1)))
q.append("pops (g -> g+1, change): %s   expected at the cuts %s" % (pops, C.CUTS))
q.append("near-still transitions (< 0.35 levels): %s" % [first + i for i, v in enumerate(d) if v < 0.35])
q.append("max run of near-still transitions: %d" % max([0] + [len(r) for r in "".join("1" if v < 0.2 else "0" for v in d).split("0")]))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002 or (a.max(axis=2) < 6).mean() > 0.2:
        bad.append(os.path.basename(f))
q.append("magenta / black frames: %s" % bad)
open(os.path.join(WORK, "qa.txt"), "w").write("\n".join(q) + "\n")
print("\n".join(q))
print(f"{'set':44s} " + " ".join(f"{n[:6]:>6s}" for n in HR.NAMES) + "   sat  val dark")
fr = lambda a, b: [os.path.join(OUT, "g_%04d.png" % g) for g in range(max(a, first), min(b, last) + 1)]
for k, (a, b) in C.PARTS.items():
    HR.row("%s part %d (g %d-%d)" % (C.TAKE, k, a, b), fr(a, b))
HR.row("%s all (g %d-%d)" % (C.TAKE, first, last), fr(first, last))
HR.row("ref a " + " ".join("t%04d" % r for _, _, r in P), [os.path.join(PROJ, "ref", "a", "t%04d.jpg" % r) for _, _, r in P])
if "--no-mkv" not in sys.argv:
    mkv = os.path.join(HERE, "take.mkv")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                    "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
    print("take.mkv", os.path.getsize(mkv) // 1024, "KB")
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
