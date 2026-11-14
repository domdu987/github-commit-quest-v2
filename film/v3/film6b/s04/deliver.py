#!/usr/bin/env python3
"""deliver.py -- raw/s<shot>/g_%04d.png -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg, take.mkv
(libx264rgb crf 6, all frames first_g .. last_g).  The take's facts live in take_cfg.py next to this file.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import take_cfg as T                                      # noqa: E402

OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for shot, (a, b) in sorted(T.RANGES.items()):
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s%d" % shot, "g_%04d.png" % g)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(shot)
        rows.append(json.load(open(p[:-4] + ".json")))
first, last = min(src), max(src)
assert sorted(src) == list(range(first, last + 1)), "gap in the frames"
N = last - first + 1
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
heads = {}
for m in rows:
    for k, v in m.get("heads", {}).items():
        if -100 < v["x"] < 820 and -100 < v["y"] < 1380:
            heads.setdefault("%s s%d" % (k, m["shot"]), []).append(v)

meta = dict(T.META)
meta.update({"first_g": first, "n_frames": N, "g0": T.G0, "g1": T.G1, "handle_in": T.G0 - first, "handle_out": last + 1 - T.G1,
             "shot_ranges": {str(s): [max(a, T.G0), min(b, T.G1 - 1)] for s, (a, b) in T.RANGES.items()},
             "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
             "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
             "head_px_range": {k: dict(w=[round(min(v["w"] for v in L)), round(max(v["w"] for v in L))],
                                        y=[round(min(v["y"] for v in L)), round(max(v["y"] for v in L))]) for k, L in heads.items()},
             "frame_source": {str(g): v for g, v in src.items()}})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []
for c in T.CUES:
    g0, g1, kind, label = c[:4]
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    if len(c) > 4:
        e["peak_frame"] = c[4]
    ev.append(e)
json.dump(dict(take=T.META["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film6b/audio/narration.wav at +0.10 s, "
               "captions PROJ/film6b/script/captions.json", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    hd = " handle" if (g < T.G0 or g >= T.G1) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s%s" % (g, g / 30.0, src[g], hd), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

w, h, lab = 360, 640, 20
C = Image.new("RGB", (len(T.PAIRS) * 2 * w + (len(T.PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(C)
x = 0
for g, ref, note in T.PAIRS:
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (src[g], g, g / 30.0), fill=(255, 255, 255))
    C.paste(Image.open(os.path.join(PROJ, ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), note, fill=(255, 220, 160))
    x += 2 * w + 12
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %d frames g %d..%d + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s"
      % (N, first, last, os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))
print(json.dumps(meta["head_px_range"]))
