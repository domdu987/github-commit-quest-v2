#!/usr/bin/env python3
"""deliver.py <take dir> <first_g> <g0> <g1> <transition> <frames dir...> -> take.mkv, meta.json, contact.jpg, QA tools"""
import sys, os, json, subprocess, glob, shutil
from PIL import Image
d, first, g0, g1, trans = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
srcs = sys.argv[6:]
fr = os.path.join(d, "raw", "assembled"); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
for s in srcs:
    for p in sorted(glob.glob(os.path.join(s, "g_*.png"))):
        os.symlink(os.path.abspath(p), os.path.join(fr, os.path.basename(p)))
n = len(glob.glob(os.path.join(fr, "g_*.png")))
assert n == g1 - g0 + 13, n
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-start_number", str(first), "-i", fr + "/g_%04d.png", "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(d, "take.mkv")], check=True)
tr = {"type": "cut", "frames": 0} if trans == "cut" else {"type": "dissolve", "frames": int(trans)}
json.dump(dict(g0=g0, g1=g1, first_g=first, n_frames=n, transition_in=tr), open(os.path.join(d, "meta.json"), "w"), indent=1)
gs = list(range(first, first + n, 6)); cols = 6; rows = (len(gs) + cols - 1) // cols; w, h = 240, 427
S = Image.new("RGB", (cols * w, rows * h), (20, 20, 20))
for i, g in enumerate(gs): S.paste(Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((w, h)), ((i % cols) * w, (i // cols) * h))
S.save(os.path.join(d, "contact.jpg"), quality=82)
print("ok", n)
