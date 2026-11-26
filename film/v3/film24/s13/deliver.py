#!/usr/bin/env python3
"""deliver.py -- contact.jpg, meta.json, cues.json for s13 (frames/ copied from raw/s13).  g1 is EXCLUSIVE (first frame of the next shot)."""
import json, glob, os, statistics as st
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
F0, G0, G1 = 1407, 1413, 1607
gs = [int(round(F0 + i * (1612 - F0) / 15.0)) for i in range(16)]
c = Image.new("RGB", (180 * 8, 640))
for i, g in enumerate(gs):
    im = Image.open(os.path.join(HERE, "frames", "g_%04d.png" % g)).convert("RGB").resize((180, 320))
    d = ImageDraw.Draw(im); d.line([(0, 220), (180, 220)], fill=(0, 255, 255)); d.line([(0, 107), (180, 107)], fill=(255, 0, 255)); d.text((3, 3), str(g), fill=(255, 255, 0))
    c.paste(im, ((i % 8) * 180, (i // 8) * 320))
c.save(os.path.join(HERE, "contact.jpg"), quality=88)
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw/s13/g_*.json")))]
meta = {"take": "s13", "film": 24, "shots": [13], "g0": G0, "g1": G1, "g1_exclusive": True, "first_g": F0, "n_frames": 1612 - F0 + 1, "handle_in": 6, "handle_out": 6,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0}, "preset": "reveal_top", "samples": 24,
        "resolution": [720, 1280], "render_resolution": [540, 960], "fps": 30, "overlay": "overlay.json (g 1407..1612)",
        "events": {"korean_turn_0_to_1": [1440, 1500], "ports_open": [1492, 1502], "cannon_smoke_0_to_1": [1500, 1570], "damage_0_to_0.35": [1545, 1607]},
        "camera": "custom: (-22,-228,150) -> (-22,-205,178), look (-22,8,-5) -> (-22,6,-5), 24 mm, 0.35 sine + 0.65 linear; DOF off",
        "s_per_frame_wall_mean": round(st.mean(r.get("wall", 0) for r in rows), 1) if rows and "wall" in rows[0] else None,
        "split": "take.mkv.partaa + take.mkv.partab (cat together)"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
cues = [dict(time=t(G0), duration=t(G1 - G0), frame=G0, end_frame=G1, kind="ambience", label="open sea, wind, far oars and drums"),
        dict(time=t(1440), duration=2.0, frame=1440, end_frame=1500, kind="accent", label="the Korean ships turn: oars splash, creaking hulls, a drum roll"),
        dict(time=t(1500), duration=2.3, frame=1500, end_frame=1570, kind="foley", label="cannon booms from every side, building (many overlapping dull booms), smoke puffs", peak_frame=1563),
        dict(time=t(1545), duration=2.1, frame=1545, end_frame=1607, kind="foley", label="timber cracks and splintering as Japanese ships are hit one after another (no screams)")]
json.dump({"take": "s13", "fps": 30, "cues": cues}, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
