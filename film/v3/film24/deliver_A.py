#!/usr/bin/env python3
"""deliver_A.py <take dir>: Look A delivery. raw/s<id>/g_*.png -> frames_A/, take_A.mkv (crf 12), meta_A.json, contact_A.jpg, work/A_qa.txt."""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
H = os.path.abspath(sys.argv[1]); cfg = json.load(open(os.path.join(H, "take.json"))); meta = json.load(open(os.path.join(H, "meta.json")))
OUT = os.path.join(H, "frames_A"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
shots = {int(k): v for k, v in cfg["shots"].items()}; F0, F1 = cfg["first_g"], cfg["last_g"]
sid = lambda g: [s for s, (a, b) in shots.items() if a <= g <= b][0]
rows = []
for g in range(F0, F1 + 1):
    raw = os.path.join(H, "raw", "s%d" % sid(g))
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
m = dict(meta); m.update(look="A", samples=8, resolution=[720, 1280], render_resolution=[720, 1280],
        s_per_frame_wall_mean=round(float(np.mean([r["wall"] for r in rows])), 1), s_per_frame_cpu_mean=round(float(np.mean([r["cpu"] for r in rows])), 1))
json.dump(m, open(os.path.join(H, "meta_A.json"), "w"), indent=1)
w, cols = 270, 8; h = w * 16 // 9; gs = [F0 + int(round(i * (F1 - F0) / 15.0)) for i in range(16)]
S = Image.new("RGB", (cols * w, 2 * (h + 18)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + 18)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + 18)); dr.text((x + 4, y + 3), "A g %d %.2f s" % (g, g / 30.0), fill=(255, 255, 255))
S.save(os.path.join(H, "contact_A.jpg"), quality=88)
subprocess.check_call(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(F0), "-i", os.path.join(OUT, "g_%04d.png"),
                       "-c:v", "libx264rgb", "-crf", "12", "-pix_fmt", "rgb24", os.path.join(H, "take_A.mkv")])
sz = os.path.getsize(os.path.join(H, "take_A.mkv")) / 1e6; print("take_A.mkv %.1f MB" % sz, m["s_per_frame_wall_mean"], m["s_per_frame_cpu_mean"])
if sz > 45:
    subprocess.check_call("cd %s && split -b 40M take_A.mkv take_A.mkv.part && rm take_A.mkv" % H, shell=True)
