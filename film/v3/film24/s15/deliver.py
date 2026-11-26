#!/usr/bin/env python3
"""deliver.py -- contact.jpg (16 frames, cyan line y 880), meta.json, cues.json for s15 (frames/ already copied from raw/s15)."""
import json, glob, os, statistics as st
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
F0, G0, G1, GC = 1761, 1767, 1949, 1867
gs = [int(round(F0 + i * (G1 - F0) / 15.0)) for i in range(16)] 
gs[gs.index(min(gs, key=lambda x: abs(x - GC)))] = GC
ims = []
for g in gs:
    im = Image.open(os.path.join(HERE, "frames", "g_%04d.png" % g)).convert("RGB").resize((180, 320))
    d = ImageDraw.Draw(im); d.line([(0, 220), (180, 220)], fill=(0, 255, 255)); d.text((3, 3), str(g), fill=(255, 255, 0)); ims.append(im)
c = Image.new("RGB", (180 * 8, 640))
for i, im in enumerate(ims): c.paste(im, ((i % 8) * 180, (i // 8) * 320))
c.save(os.path.join(HERE, "contact.jpg"), quality=88)
rows = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "raw/s15/g_*.json")))]
w, cp = round(st.mean(r["wall"] for r in rows), 1), round(st.mean(r["cpu"] for r in rows), 1)
meta = {"take": "s15", "film": 24, "shots": [15], "g0": G0, "g1": G1, "first_g": F0, "n_frames": G1 - F0 + 1, "handle_in": 6, "handle_out": 0,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "none", "note": "film ends on g 1949 (hard cut on the last word)"},
        "transitions": [{"at": G0, "type": "cut"}, {"at": GC, "type": "cut", "note": "inside the take: water/plank -> sand/crawl"}],
        "shot_ranges": {"15": [G0, G1]}, "preset": "shore", "samples": 24, "resolution": [720, 1280], "render_resolution": [540, 960], "fps": 30,
        "events": {"plank_phase": [G0, GC - 1], "sand_cut": GC, "crawl_step_frames": 8, "crawl_half_step_D": 0.45},
        "cast": "jp_cmd24_plank_cling (wet24 1, rides J.swell_z), jp_cmd24_crawl_a/crawl_b alternating every 8 frames (wet24 1)",
        "mouths": "held (no quote)", "dof": "off", "s_per_frame_wall_mean": w, "s_per_frame_cpu_mean": cp,
        "split": "take.mkv.partaa + take.mkv.partab (cat them back together)"}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
t = lambda g: round(g / 30.0, 3)
cues = [dict(time=t(G0), duration=round((GC - G0) / 30.0, 3), frame=G0, end_frame=GC, kind="ambience", label="surf and gentle swell, gulls, the wet commander gasping and clinging to the plank (splash)"),
        dict(time=t(GC), duration=0.0, frame=GC, end_frame=GC, kind="cut", label="HARD CUT inside the take to the sand: wet sand, crawling hands and knees, splash and sand scuffs on each limb step"),
        dict(time=t(G1), duration=0.0, frame=G1, end_frame=G1, kind="cut", label="film ends: hard cut on the last word")]
for g in range(GC + 4, G1, 8):
    cues.append(dict(time=t(g), duration=0.0, frame=g, end_frame=g, kind="foley", label="crawl step: wet sand squelch / hand slap", peak_frame=g))
json.dump({"take": "s15", "fps": 30, "cues": cues}, open(os.path.join(HERE, "cues.json"), "w"), indent=1)
print(meta["s_per_frame_wall_mean"], len(cues))
