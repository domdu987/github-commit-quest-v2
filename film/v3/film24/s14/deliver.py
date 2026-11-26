#!/usr/bin/env python3
"""deliver.py -- contact.jpg, meta.json, cues.json for s14 (frames/ copied from raw/s14).  g1 is EXCLUSIVE (first frame of the next shot)."""
import json, glob, os, statistics as st
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
F0, G0, G1 = 1601, 1607, 1767
gs = [int(round(F0 + i * (1772 - F0) / 15.0)) for i in range(16)]
c = Image.new("RGB", (180 * 8, 640))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(HERE, "frames", "g_%04d.png" % g)).convert("RGB").resize((180, 320))
    d = ImageDraw.Draw(im); d.line([(0, 220), (180, 220)], fill=(0, 255, 255)); d.line([(0, 107), (180, 107)], fill=(255, 0, 255)); d.text((3, 3), str(g), fill=(255, 255, 0))
    c.paste(im, ((i % 8) * 180, (i // 8) * 320))
c.save(os.path.join(HERE, "contact.jpg"), quality=88)
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw/s14/g_*.json")))]
meta = {"take": "s14", "film": 24, "shots": [14], "g0": G0, "g1": G1, "g1_exclusive": True, "first_g": F0, "n_frames": 1772 - F0 + 1, "handle_in": 6, "handle_out": 6,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0}, "preset": "aftermath", "samples": 24,
        "resolution": [720, 1280], "render_resolution": [540, 960], "fps": 30, "overlay": "overlay.json (g 1601..1772)",
        "events": {"damage_0.35_to_1": [1607, 1766], "cannon_smoke_1_to_0.35": [1600, 1670], "korean_turn": 1, "spikes": 3, "ports": 1},
        "camera": "custom: (150,-16,6.5) -> (122,-12,7), look (55,0,7) -> (50,0,7.5), 24 mm, 0.35 sine + 0.65 linear; DOF off",
        "split": "take.mkv.partaa + take.mkv.partab (cat together)"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
cues = [dict(time=t(G0), duration=t(G1 - G0), frame=G0, end_frame=G1, kind="ambience", label="calm sea after the battle, drifting smoke, creaking timbers, distant drums fading"),
        dict(time=t(1650), duration=3.0, frame=1650, end_frame=1740, kind="foley", label="ship hull creaks and groans, oars dipping; the turtle ship passes (heavy wake)"),
        dict(time=t(1743), duration=0.8, frame=1743, end_frame=1767, kind="accent", label="timber cracks as the Japanese fleet breaks up ('แตกไปกว่าครึ่ง')")]
json.dump({"take": "s14", "fps": 30, "cues": cues}, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
