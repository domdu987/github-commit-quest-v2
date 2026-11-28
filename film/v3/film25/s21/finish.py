#!/usr/bin/env python3
"""finish.py <take_dir> <row_label> <g0> <g1_exclusive> [first_g] [notes...]
compose all rendered frames (post_d), encode take.mkv (libx264rgb crf 12), meta.json, contact.jpg, QA_AUTO.md/phone_sheet.jpg, light_metrics, qa_jitter -> QA.md"""
import os, sys, json, subprocess, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
FILM = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
td = os.path.abspath(sys.argv[1]); label = sys.argv[2]; g0, g1 = int(sys.argv[3]), int(sys.argv[4])
first = int(sys.argv[5]) if len(sys.argv) > 5 else g0
notes = sys.argv[6] if len(sys.argv) > 6 else ""
import post_d as PD
from PIL import Image
frames = os.path.join(td, "frames"); os.makedirs(frames, exist_ok=True)
gs = [g for g in range(first, g1) if os.path.exists(os.path.join(td, "work", "meta", "g_%04d.json" % g))]
for g in gs:
    if not os.path.exists(os.path.join(frames, "g_%04d.png" % g)):
        PD.compose(g, os.path.join(td, "work"), frames)
assert gs == list(range(first, g1)), "missing frames: %s" % sorted(set(range(first, g1)) - set(gs))
mkv = os.path.join(td, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(frames, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "12", "-preset", "slow", mkv], check=True)
json.dump(dict(g0=g0, g1=g1, first_g=first, n_frames=g1 - first, transition_in=dict(type="cut", frames=0)), open(os.path.join(td, "meta.json"), "w"))
# contact sheet: 6 fps tiles
step = 5; sel = gs[::step]; cols = 8; tw, th = 135, 240
rows = (len(sel) + cols - 1) // cols
sh = Image.new("RGB", (cols * tw, rows * th))
for i, g in enumerate(sel):
    sh.paste(Image.open(os.path.join(frames, "g_%04d.png" % g)).resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
sh.save(os.path.join(td, "contact.jpg"), quality=88)
r1 = subprocess.run(["python3", os.path.join(FILM, "qa_auto.py"), mkv, "--first_g", str(first), "--out", td], capture_output=True, text=True)
r2 = subprocess.run(["python3", os.path.join(FILM, "film25", "tools", "light_metrics.py"), mkv], capture_output=True, text=True)
r3 = subprocess.run(["python3", os.path.join(FILM, "qa_jitter.py"), mkv], capture_output=True, text=True)
print(r1.stdout[-600:], r1.stderr[-300:]); print(r2.stdout); print(r3.stdout or "jitter: no shake seconds")
open(os.path.join(td, "metrics.txt"), "w").write(r2.stdout + "\n--- jitter ---\n" + (r3.stdout or "no shake seconds flagged") + "\n--- qa_auto ---\n" + r1.stdout[-1500:])
