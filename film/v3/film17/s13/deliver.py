#!/usr/bin/env python3
"""deliver.py -- take.mkv, meta.json, contact.jpg from raw/g_*.png (run from anywhere)."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, "raw")
G0, G1, FIRST = 1868, 2052, 1862; N = G1 - FIRST
missing = [g for g in range(FIRST, G1) if not os.path.exists(os.path.join(RAW, "g_%04d.png" % g))]
assert not missing, missing[:10]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(RAW, "g_%04d.png"),
                "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
json.dump(dict(take="s13", shots=[31, 32, 33], g0=G0, g1=G1, first_g=FIRST, n_frames=N, handle_before=G0 - FIRST, handle_after=0,
               transition_in=dict(type="dissolve", frames=11), cuts=[1947, 2014], end="hard cut at g 2052", width=720, height=1280, fps=30,
               shot_ranges={"31": [1868, 1946], "32": [1947, 2013], "33": [2014, 2051]}), open(os.path.join(HERE, "meta.json"), "w"), indent=1)
gs = list(range(FIRST, G1, 6)); tw, th = 180, 320; cols = 12; rows = (len(gs) + cols - 1) // cols
sheet = Image.new("RGB", (tw * cols, (th + 14) * rows), (20, 20, 20)); d = ImageDraw.Draw(sheet)
for i, g in enumerate(gs):
    im = Image.open(os.path.join(RAW, "g_%04d.png" % g)).convert("RGB").resize((tw, th)); x, y = (i % cols) * tw, (i // cols) * (th + 14)
    sheet.paste(im, (x, y)); d.text((x + 3, y + th + 1), "g%d" % g, fill=(230, 230, 230)); d.line((x, y + int(880 / 4), x + tw, y + int(880 / 4)), fill=(0, 255, 255))
sheet.save(os.path.join(HERE, "contact.jpg"), quality=85); print("ok", N)
