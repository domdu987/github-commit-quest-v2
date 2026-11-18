#!/usr/bin/env python3
"""deliver.py <take> : raw/s<id>/g_*.png -> frames/, take.mkv, contact.jpg, meta.json, cues.json, QA_AUTO.md + phone_sheet.jpg."""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
TAKE = os.path.basename(HERE)
CFG = {"s01": dict(shots={1: (0, 68), 2: (69, 139)}, g0=0, g1=134, first=0, last=139, cuts=[69],
                   tin={"type": "open", "frames": 0}, plan="shots 1-2: hull_plank painter / harbour_wide crane out"),
       "s03": dict(shots={3: (128, 212), 4: (213, 298)}, g0=134, g1=293, first=128, last=298, cuts=[213],
                   tin={"type": "cut", "frames": 0}, plan="shots 3-4: convoy_wide periscope / hit and dive")}[TAKE]
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = {}
for sid, (a, b) in CFG["shots"].items():
    for g in range(a, b + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
        rows[g] = json.load(open(os.path.join(raw, "g_%04d.json" % g)))
n = CFG["last"] - CFG["first"] + 1
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(CFG["first"]), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(n), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
walls = [r["wall"] for r in rows.values()]; cpus = [r["cpu"] for r in rows.values()]
meta = dict(take=TAKE, film=10, plan=CFG["plan"], g0=CFG["g0"], g1=CFG["g1"], first_g=CFG["first"], n_frames=n, handle_in=CFG["g0"] - CFG["first"],
            handle_out=CFG["last"] - CFG["g1"] + 1, transition_in=CFG["tin"], transition_out={"type": "cut", "frames": 0},
            cuts=CFG["cuts"], shot_ranges={str(k): list(v) for k, v in CFG["shots"].items()}, samples=12, resolution=[720, 1280], fps=30, threads=2,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            dof="none", narration="film10/audio/narration.wav at +0.10 s")
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
gs = list(range(CFG["first"], CFG["last"] + 1, max(1, n // 16)))[:16]
tw, th = 180, 320
sheet = Image.new("RGB", (tw * 8, th * 2))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB")
    d = ImageDraw.Draw(im); d.line([(0, 880), (720, 880)], fill=(0, 255, 255), width=3)
    im = im.resize((tw, th)); ImageDraw.Draw(im).text((4, 4), "g%d" % g, fill=(255, 255, 0))
    sheet.paste(im, ((i % 8) * tw, (i // 8) * th))
sheet.save(os.path.join(HERE, "contact.jpg"), quality=88)
r = subprocess.run([sys.executable, os.path.join(HERE, "..", "..", "..", "qa_auto.py"), os.path.join(HERE, "take.mkv"), "--first_g", str(CFG["first"]),
                    "--cuts", ",".join(map(str, CFG["cuts"])), "--out", HERE], capture_output=True, text=True)
print(r.stdout[-1500:], r.stderr[-800:], "qa exit", r.returncode)
