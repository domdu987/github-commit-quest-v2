#!/usr/bin/env python3
"""deliver.py TAKE_ID  -> frames/ (from raw/), take.mkv, meta.json (spec in shot.py), contact.jpg.  usage: python3 deliver.py [first last g0 g1 shot_ids transition]"""
import os, sys, json, glob, shutil, subprocess, statistics
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
raw = os.path.join(HERE, "raw"); fr = os.path.join(HERE, "frames")
js = sorted(glob.glob(os.path.join(raw, "g_*.json"))); gs = [int(os.path.basename(p)[2:6]) for p in js]
first, last = min(gs), max(gs)
assert gs == list(range(first, last + 1)), "missing frames"
os.makedirs(fr, exist_ok=True)
for g in gs:
    shutil.copy(os.path.join(raw, "g_%04d.png" % g), os.path.join(fr, "g_%04d.png" % g))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(fr, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
reps = [json.load(open(p)) for p in js]
wall = statistics.mean(r["wall"] for r in reps); cpu = statistics.mean(r["cpu"] for r in reps)
print("frames", first, last, len(gs), "s/frame wall %.2f cpu %.2f" % (wall, cpu))
open(os.path.join(HERE, "timing.json"), "w").write(json.dumps(dict(first_g=first, last_g=last, n=len(gs), wall=round(wall, 2), cpu=round(cpu, 2))))
# contact sheet: 16 frames, cyan line y 880
pick = [gs[int(i * (len(gs) - 1) / 15)] for i in range(16)]
tw, th = 180, 320; sheet = Image.new("RGB", (tw * 8, th * 2))
for i, g in enumerate(pick):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((tw, th)); d = ImageDraw.Draw(im)
    d.line((0, 880 * th // 1280, tw, 880 * th // 1280), fill=(0, 255, 255)); d.text((3, 3), str(g), fill=(255, 255, 255))
    sheet.paste(im, (tw * (i % 8), th * (i // 8)))
sheet.save(os.path.join(HERE, "contact.jpg"), quality=85)
# head report: max chin / head y
ymax = max((h["y"] + h["w"] * 0.5) for r in reps for h in r["heads"].values()) if any(r["heads"] for r in reps) else None
print("lowest head bottom (head centre y + 0.5 w): %.0f (limit 880)" % ymax)
