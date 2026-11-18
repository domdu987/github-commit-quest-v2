#!/usr/bin/env python3
"""deliver.py -- raw/s17 + raw/s18 + raw/s19 -> frames/g_%04d.png (g 1101..1302), meta.json, cues.json, contact.jpg, take.mkv."""
import os, json, shutil, subprocess
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
G0, G1 = 1101, 1302
SH = {17: (1101, 1169), 18: (1170, 1251), 19: (1252, 1302)}
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = []
for sid, (a, b) in SH.items():
    for g in range(a, b + 1):
        raw = os.path.join(HERE, "raw", "s%d" % sid)
        shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g))
        rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
n = G1 - G0 + 1
meta = {"take": "s17", "film": 13, "shots": [17, 18, 19], "first_g": G0, "n_frames": n, "g0": 1107, "g1": 1297, "handle_in": 6, "handle_out": 5,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "transitions": [{"at": 1107, "type": "cut"}, {"at": 1170, "type": "cut", "note": "17 -> 18, same location"}, {"at": 1252, "type": "cut", "note": "18 -> 19"}, {"at": 1297, "type": "cut"}],
        "shot_ranges": {"17": [1107, 1169], "18": [1170, 1251], "19": [1252, 1296]},
        "set": "v3/set3d13/chicago.py suite (SUITE light; plan MORNING/DAY not available for the suite location), cameras custom (22 / 40 / 22 mm), no DOF; tea ripple 0 keyed every frame; chandelier hidden from camera only",
        "cast": "cast13 rich (rich_look_window_smug; shot 19 cup raised in the near hand, lip-sync talk_mouth g 1255..1300 = 41.72-43.22 s), lady13 + gentleman13 (shot 19), 44 cast13 townsfolk cards in the street",
        "samples": 12, "resolution": [720, 1280], "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean([r.get("wall", 0) for r in rows])), 2), "s_per_frame_cpu_mean": round(float(np.mean([r.get("cpu", 0) for r in rows])), 2)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = [dict(t=36.9, dur=2.1, label="suite interior, tea room hush, faint street murmur far below"),
        dict(t=39.0, dur=2.7, label="porcelain: cup rests on saucer, tiny china tick; silence on the tea"),
        dict(t=41.72, dur=1.5, label="smug cup raised: soft china clink on 'ไม่ขยับสักนิ้ว'")]
json.dump({"take": "s17", "fps": 30, "cues": [dict(time=c["t"], duration=c["dur"], label=c["label"]) for c in cues]}, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
pick = list(range(G0, G1 + 1, 12))
ims = [Image.open(os.path.join(OUT, "g_%04d.png" % g)).resize((180, 320)) for g in pick]
cols = 6; rws = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (180 * cols, 320 * rws))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
sh.save(os.path.join(HERE, "contact.jpg"), quality=85)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(G0), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
print("done", n)
