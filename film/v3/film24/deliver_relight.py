#!/usr/bin/env python3
"""deliver_relight.py <take> <first_g> <last_g> <rawdir...>: relight-only take (same g as meta.json): frames_C, take_C.mkv crf 12, meta_C.json (copy of meta.json + version C), contact_C.jpg."""
import json, os, sys, shutil, subprocess, statistics as st
from PIL import Image, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); T = sys.argv[1]; f0, f1 = int(sys.argv[2]), int(sys.argv[3]); raws = sys.argv[4:]
D = os.path.join(H, T); fr = os.path.join(D, "frames_C"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr); walls = []
for g in range(f0, f1 + 1):
    for r in raws:
        b = os.path.join(D, r, "g_%04d" % g)
        if os.path.exists(b + ".png"):
            shutil.copy(b + ".png", os.path.join(fr, "g_%04d.png" % g)); walls.append(json.load(open(b + ".json")).get("wall", 0)); break
    else:
        sys.exit("missing frame %d" % g)
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(f0), "-i", fr + "/g_%04d.png", "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", os.path.join(D, "take_C.mkv")])
m = json.load(open(os.path.join(D, "meta.json"))); m.update(version="C", look="C", s_per_frame_wall_mean=round(st.mean(walls), 1)); json.dump(m, open(os.path.join(D, "meta_C.json"), "w"), indent=1)
gs = [int(round(f0 + i * (f1 - f0) / 15.0)) for i in range(16)]; c = Image.new("RGB", (180 * 8, 640))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((180, 320)); ImageDraw.Draw(im).text((3, 3), str(g), fill=(255, 255, 0)); c.paste(im, ((i % 8) * 180, (i // 8) * 320))
c.save(os.path.join(D, "contact_C.jpg"), quality=88); print(T, "frames", f1 - f0 + 1, "mean wall", m["s_per_frame_wall_mean"])
