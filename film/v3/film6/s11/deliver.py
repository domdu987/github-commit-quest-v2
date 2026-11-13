#!/usr/bin/env python3
"""deliver.py -- (shared by s11 and s16) from raw/s<shot>/g_*.png build frames/g_%04d.png, meta.json, cues.json, contact.jpg,
compare.jpg and take.mkv (libx264rgb crf 6).   python3 deliver.py <take folder>   (reads <take>/deliver_cfg.json)"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.abspath(sys.argv[1])
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
cfg = json.load(open(os.path.join(HERE, "deliver_cfg.json")))
G_FIRST, G_LAST = cfg["first_g"], cfg["last_g"]
N = G_LAST - G_FIRST + 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for shot, (a, b) in cfg["shot_frames"].items():
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s%s" % shot, "g_%04d.png" % g)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = shot
        rows.append(json.load(open(p[:-4] + ".json")))
assert sorted(src) == list(range(G_FIRST, G_LAST + 1)), "missing frames"
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

meta = dict(take=cfg["take"], film=6, shots=cfg["shots"], first_g=G_FIRST, n_frames=N, g0=cfg["g0"], g1=cfg["g1"],
            handle_in=cfg["g0"] - G_FIRST, handle_out=G_LAST + 1 - cfg["g1"],
            transition_in=cfg["transition_in"], transition_out=cfg["transition_out"],
            shot_ranges=cfg["shot_ranges"], cuts_inside=cfg["cuts_inside"], events=cfg["events"],
            set=cfg["set"], dof="none (client rule: cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) at build and before every render)",
            denoiser="OpenImageDenoise, albedo+normal, prefilter FAST",
            narration="film6/audio/narration_bankky.wav at +0.10 s; captions film6/script/captions.json",
            light=cfg["light"], cast=cfg["cast"], mouths=cfg["mouths"], samples=12, resolution=[720, 1280], threads=2, fps=30,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            frame_source={str(g): v for g, v in sorted(src.items())})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []
for c in cfg["cues"]:
    g0, g1 = c["g"]
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=c["kind"], label=c["label"])
    if "peak" in c:
        e["peak_frame"] = c["peak"]
    ev.append(e)
json.dump(dict(take=cfg["take"], fps=30, note="time = film seconds (g / 30); narration PROJ/film6/audio/narration_bankky.wav at +0.10 s, captions.json",
               cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = cfg.get("contact") or [G_FIRST + int(round(i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
rws = (len(gs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rws * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %s%s" % (g, g / 30.0, src[g], " handle" if (g < cfg["g0"] or g >= cfg["g1"]) else ""),
            fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

PAIRS = cfg["compare"]
w, h, lab = 360, 640, 20
Cm = Image.new("RGB", (len(PAIRS) * 2 * w + (len(PAIRS) - 1) * 12, h + lab), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
x = 0
for g, ref in PAIRS:
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, lab))
    dr.text((x + 4, 4), "shot %s  g %d (%.2f s)" % (src[g], g, g / 30.0), fill=(255, 255, 255))
    Cm.paste(Image.open(os.path.join(PROJ, "ref", ref)).convert("RGB").resize((w, h), Image.LANCZOS), (x + w, lab))
    dr.text((x + w + 4, 4), "ref %s" % ref, fill=(255, 220, 160))
    x += 2 * w + 12
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(G_FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %d frames + take.mkv; mean wall %.2f s, cpu %.2f s" % (N, np.mean(walls), np.mean(cpus)))
