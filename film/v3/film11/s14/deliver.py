#!/usr/bin/env python3
"""deliver.py -- build frames/, take.mkv, meta.json, cues.json, contact.jpg of one film-11 take and run qa_auto.  python3 deliver.py   (run inside the take folder)"""
import os, sys, json, shutil, subprocess, importlib.util
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("shot", os.path.join(HERE, "shot.py")); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SH = S.SHOT; a, b = S.RANGES[SH]; n = b - a + 1
OUT = os.path.join(HERE, "frames"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
raw = os.path.join(HERE, "raw", "s%d" % SH); rows = []
for g in range(a, b + 1):
    shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
dis = getattr(S, "DISSOLVE_IN", False)
heads = [dict(g=m["g"], **{k: v for k, v in m["heads"].items()}) for m in rows]
worst = max((h["chin"] for m in rows for h in m["heads"].values()), default=0)
meta = {"take": "s%d" % SH, "film": 11, "shots": [SH], "first_g": a, "n_frames": n, "g0": S.G0, "g1": S.G1, "handle_in": S.G0 - a, "handle_out": b - (S.G1 - 1),
        "transition_in": {"type": "dissolve" if dis else "cut", "frames": 8 if dis else 0},
        "set": "v3/set3d11/dairy.py preset %s (light %s)" % (S.PRESET, S.LIGHT or "preset default"), "cast": "v3/cast11 cards (see shot.py)",
        "dof": "none", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "max_chin_y": worst, "head_report": "raw/s%d/g_*.json" % SH}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = {"take": "s%d" % SH, "events": getattr(S, "CUES", [])}
json.dump(cues, open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
mk = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(a), "-i", os.path.join(OUT, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mk], check=True)
print("take.mkv", os.path.getsize(mk) / 1e6, "MB")
if os.path.getsize(mk) > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True); print("split; remember: do not commit the unsplit take.mkv")
# contact sheet: 8 evenly spaced frames, cyan line y 880
idx = [int(round(i)) for i in np.linspace(0, n - 1, 8)]
tiles = []
for i in idx:
    im = Image.open(os.path.join(OUT, "g_%04d.png" % (a + i))).convert("RGB").resize((240, 427)); d = ImageDraw.Draw(im); d.line([(0, 293), (240, 293)], fill=(0, 255, 255)); d.text((4, 4), "g%d" % (a + i), fill=(255, 255, 255)); tiles.append(im)
sh = Image.new("RGB", (240 * 4, 427 * 2))
for k, t in enumerate(tiles): sh.paste(t, ((k % 4) * 240, (k // 4) * 427))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
