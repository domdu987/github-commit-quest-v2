#!/usr/bin/env python3
"""deliver.py -- raw/s<id>/g_%04d.png (+ .json) -> frames/g_%04d.png, meta.json, cues.json, contact.jpg, take.mkv (libx264rgb crf 6),
split into take.mkv.part* if over 45 MB.  Take-specific data comes from take_info.py next to this file.     python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import take_info as TI

OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
first, last = TI.FIRST_G, TI.LAST_G
rows, src = [], {}
for g in range(first, last + 1):
    sid = [s for s, (a, b) in TI.RANGES.items() if a <= g <= b][0]
    raw = os.path.join(HERE, "raw", "s%d" % sid)
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[str(g)] = str(sid)
    rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
N = last - first + 1
by = {}
for r in rows:
    by.setdefault(r["shot"], []).append(r)
meta = dict(take=TI.TAKE, film=9, shots=TI.SHOTS, g0=TI.G0, g1=TI.G1, first_g=first, n_frames=N, handle_in=TI.G0 - first, handle_out=last + 1 - TI.G1,
            transition_in=TI.TRANSITION_IN, transition_out=TI.TRANSITION_OUT, transitions=TI.TRANSITIONS,
            shot_ranges={str(k): list(v) for k, v in TI.SHOT_RANGES.items()}, setups=TI.SETUPS, events=TI.EVENTS,
            set="v3/set3d9/wall.py (client-approved set, commit 5d511aa) wall_site; " + TI.SET_NOTE,
            cast="v3/cast9: " + TI.CAST_NOTE, mouths=TI.MOUTH_NOTE,
            dof="none (cam.data.dof.use_dof False + W.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            denoiser="OpenImageDenoise, prefilter FAST", narration="film9/audio/narration.wav at +0.10 s; captions film9/script/captions.json",
            samples=12, resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean([r["wall"] for r in rows])), 2), s_per_frame_cpu_mean=round(float(np.mean([r["cpu"] for r in rows])), 2),
            s_per_frame_by_shot={str(k): dict(wall=round(float(np.mean([r["wall"] for r in v])), 2), cpu=round(float(np.mean([r["cpu"] for r in v])), 2)) for k, v in by.items()},
            frame_source=src)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
for g0, g1, label, kind, extra in TI.CUES:
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(extra); ev.append(e)
json.dump(dict(take=TI.TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film9/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)

gs = [first + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.line([(x, y + lab + int(880 * h / 1280)), (x + w, y + lab + int(880 * h / 1280))], fill=(0, 200, 220))
    tag = " handle" if (g < TI.G0 or g >= TI.G1) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s%s" % (g, g / 30.0, src[str(g)], tag), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
for p in glob.glob(mkv + ".part*"):
    os.remove(p)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
size = os.path.getsize(mkv)
if size > 45e6:
    subprocess.run(["split", "-b", "40M", "take.mkv", "take.mkv.part"], cwd=HERE, check=True)
    os.remove(mkv)
print("delivered %s: g %d..%d (%d frames), take.mkv %.1f MB%s" % (TI.TAKE, first, last, N, size / 1e6, " (split)" if size > 45e6 else ""))
