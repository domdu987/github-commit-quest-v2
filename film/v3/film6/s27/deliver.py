#!/usr/bin/env python3
"""deliver.py -- from raw/s<id>/ build frames/g_%04d.png, meta.json, cues.json, contact.jpg, compare.jpg (final frames beside the closest
ref a frames) and take.mkv (libx264rgb crf 6, every frame of the take incl. handles).  python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CFG = json.load(open(os.path.join(HERE, "deliver_cfg.json")))

TAKE, SHOTS = CFG["take"], CFG["shot_ranges"]                  # {"24": [g0, g1]} incl. handles at the ends of the take
G_FIRST = min(a for a, b in SHOTS.values()); G_LAST = max(b for a, b in SHOTS.values())
N = G_LAST - G_FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
src, rows = {}, []
for sid, (a, b) in SHOTS.items():
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s" + sid, "g_%04d.png" % g)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
        rows.append(json.load(open(p[:-4] + ".json")))
assert len(src) == N, (len(src), N)
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

meta = dict(take=TAKE, film=6, shots=[int(s) for s in SHOTS], first_g=G_FIRST, n_frames=N, g0=CFG["g0"], g1=CFG["g1"],
            handle_in=CFG["g0"] - G_FIRST, handle_out=G_LAST + 1 - CFG["g1"],
            transition_in=CFG["transition_in"], transition_out=CFG["transition_out"],
            transitions=CFG["transitions"], shot_ranges={k: [max(v[0], CFG["g0"]), min(v[1], CFG["g1"] - 1)] for k, v in SHOTS.items()},
            framings=CFG["framings"], events=CFG["events"], set=CFG["set"],
            dof="none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            denoiser="OpenImageDenoise, albedo+normal, prefilter FAST",
            narration="film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
            light=CFG["light"], cast=CFG["cast"], samples=12, resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            frame_source={str(g): v for g, v in sorted(src.items())})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
for c in CFG["cues"]:
    g0, g1 = c["frame"], c.get("end_frame", c["frame"])
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=c["kind"], label=c["label"])
    if "peak_frame" in c:
        e["peak_frame"] = c["peak_frame"]
    ev.append(e)
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s, captions.json",
               cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [G_FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    hd = " handle" if (g < CFG["g0"] or g >= CFG["g1"]) else ""
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s%s" % (g, g / 30.0, src[g], hd), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = CFG["compare"]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, tref in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (src[g], g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", "a", "t%04d.jpg" % tref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref a t%04d" % tref, fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", N, "frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
