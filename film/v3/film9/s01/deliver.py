#!/usr/bin/env python3
"""deliver.py -- raw/s<id>/g_%04d.png -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, take.mkv (split if > 45 MB).
Take description in TAKE.json beside this script.   python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "TAKE.json")))
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
first, last = T["first_g"], T["last_g"]
src, rows = {}, []
for g in range(first, last + 1):
    sid = [int(k) for k, (a, b) in T["setup_ranges"].items() if a <= g <= b][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[str(g)] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = last - first + 1
by = {}
for r in rows:
    by.setdefault(str(r["shot"]), []).append(r)
meta = dict(T["meta"])
meta.update(first_g=first, n_frames=N, samples=12, resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean([r["wall"] for r in rows])), 2),
            s_per_frame_cpu_mean=round(float(np.mean([r["cpu"] for r in rows])), 2),
            s_per_frame_by_setup={k: dict(wall=round(float(np.mean([r["wall"] for r in v])), 2), cpu=round(float(np.mean([r["cpu"] for r in v])), 2)) for k, v in by.items()},
            frame_source=src)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1, ensure_ascii=False)
ev = []
for c in T["cues"]:
    g0, g1 = c["frame"], c.get("end_frame", c["frame"])
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=c["kind"], label=c["label"])
    if "peak_frame" in c:
        e["peak_frame"] = c["peak_frame"]
    ev.append(e)
json.dump(dict(take=meta["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film9/audio/narration.wav at +0.10 s, captions PROJ/film9/script/captions.json", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
gs = [int(round(first + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    sh = [k for k, (a, b) in T["shot_of"].items() if a <= g <= b]
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, sh[0] if sh else "handle"), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
mkv = os.path.join(HERE, "take.mkv")
for p in glob.glob(mkv + ".part*"):
    os.remove(p)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
mb = os.path.getsize(mkv) / 1e6
if mb > 45:
    subprocess.run(["split", "-b", "40M", mkv, mkv + ".part"], check=True)
    os.remove(mkv)
print("delivered %d frames g %d..%d, take.mkv %.1f MB%s; mean wall %.2f s, cpu %.2f s" % (N, first, last, mb, " (split)" if mb > 45 else "",
      meta["s_per_frame_wall_mean"], meta["s_per_frame_cpu_mean"]))
