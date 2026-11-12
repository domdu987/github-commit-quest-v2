#!/usr/bin/env python3
"""deliver.py -- raw/g_*.png (+json) -> frames/, take.mkv, meta.json, cues.json, contact.jpg, work/qa_numbers.json.  python3 deliver.py"""
CFG = dict(take="s11", shots=[11], g0=799, g1=883, handle_in=7, handle_out=6,
           transition_in={"type": "dissolve", "frames": 10, "note": "in-handle g 792..798 rendered in 3D (low wide on the crowd)"},
           transition_out={"type": "dissolve", "frames": 9, "note": "out-handle g 883..888 rendered in 3D (rod drifting at 420-440 mm)"},
           set="v3/set3d2/tower.py", light="DAY", refs=[("ref a t0062 t0040", ["a/t0062.jpg", "a/t0040.jpg"])],
           notes="punch-in on the rod is a tilt-up + snap zoom 22 -> 420 mm (g 846..856, geometric lens interpolation), then 420 -> 440 mm drift",
           cues=[(792, 889, "ambience", "square ambience: pigeons, distant voices, wind"),
                 (794, 803, "dissolve", "dissolve in from the spire montage"),
                 (799, 856, "crowd_laugh", "townspeople point up and laugh (three voices, rolling)"),
                 (826, 834, "camera_snap", "snap reframe closer on the laughing three (short whoosh)"),
                 (846, 856, "camera_snap", "tilt up + snap zoom onto the rod (big whoosh), lands g 856"),
                 (856, 856, "accent", "'mai chim fa' lands on the rod against the sky (comic sting)"),
                 (856, 889, "ambience", "high wind around the spire, crowd laughter far below"),
                 (879, 888, "dissolve", "dissolve to the storm chamber")])
# ---------------------------------------------------------------- shared delivery code (same in s08..s11)
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
import hue_report as H
RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
first, last = CFG["g0"] - CFG["handle_in"], CFG["g1"] + CFG["handle_out"] - 1
rows = {}
for g in range(first, last + 1):
    shutil.copyfile(os.path.join(RAW, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
    rows[g] = json.load(open(os.path.join(RAW, "g_%04d.json" % g)))
n = last - first + 1
walls = [r["wall"] for r in rows.values()]; cpus = [r["cpu"] for r in rows.values()]
mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
meta = dict(take=CFG["take"], shots=CFG["shots"], g0=CFG["g0"], g1=CFG["g1"], handle_in=CFG["handle_in"], handle_out=CFG["handle_out"],
            first_g=first, n_frames=n, transition_in=CFG["transition_in"], transition_out=CFG["transition_out"],
            shot_ranges={str(s): [CFG["g0"], CFG["g1"] - 1] for s in CFG["shots"]}, set=CFG["set"], light=CFG["light"],
            samples=12, resolution=[720, 1280], threads=2, s_per_frame_wall_mean=round(float(np.mean(walls)), 2),
            s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2), notes=CFG.get("notes", ""))
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
ev = []
for (g0, g1, kind, label) in CFG["cues"]:
    ev.append(dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label))
json.dump(dict(take=CFG["take"], fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)
# contact: 16 evenly spaced frames, label strip above
gs = [first + int(round(i * (n - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s" % (g, g / 30.0), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
# QA numbers
fs = [os.path.join(OUT, "g_%04d.png" % g) for g in range(first, last + 1)]
prev = None; d = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((180, 320), Image.BILINEAR), dtype=np.float32)
    if prev is not None:
        d.append(float(np.abs(a - prev).mean()))
    prev = a
pops = [(first + i, first + i + 1, round(v, 1)) for i, v in enumerate(d)
        if v > 1.8 * (d[i - 1] if i else v) and v > 1.8 * (d[i + 1] if i + 1 < len(d) else v) and v > 1.0]
still = [first + i for i, v in enumerate(d) if v < 0.35]
runs, cur = [], []
for g in still:
    if cur and g == cur[-1] + 1:
        cur.append(g)
    else:
        if len(cur) > 1: runs.append((cur[0], cur[-1] + 1))
        cur = [g]
if len(cur) > 1: runs.append((cur[0], cur[-1] + 1))
bad = []
for f in fs:
    a = np.asarray(Image.open(f).convert("RGB").resize((90, 160)), dtype=np.int16)
    if ((a[..., 0] > 200) & (a[..., 1] < 40) & (a[..., 2] > 200)).mean() > 0.002: bad.append(os.path.basename(f))
import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    print(f"{'set':44s} " + " ".join(f"{nm[:6]:>6s}" for nm in H.NAMES) + "   sat  val dark")
    H.row("%s g %d-%d" % (CFG["take"], first, last), fs)
    for lab_, refs in CFG.get("refs", []):
        H.row(lab_, [os.path.join(HERE, "..", "..", "..", "ref", r) for r in refs])
q = dict(first=first, last=last, n=n, wall=meta["s_per_frame_wall_mean"], cpu=meta["s_per_frame_cpu_mean"], pops=pops,
         still_runs=runs, mean_change=[round(float(np.min(d)), 2), round(float(np.median(d)), 2), round(float(np.max(d)), 2)],
         magenta=bad, hue=buf.getvalue(), rows={g: rows[g] for g in range(first, last + 1)})
json.dump(q, open(os.path.join(HERE, "work", "qa_numbers.json"), "w"), indent=1)
print(buf.getvalue()); print("pops", pops, "still runs", runs, "change min/med/max", q["mean_change"], "magenta", bad)
print("delivered %s: g %d..%d (%d frames), %.2f s wall %.2f s cpu per frame" % (CFG["take"], first, last, n, meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
