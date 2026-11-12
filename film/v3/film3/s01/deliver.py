#!/usr/bin/env python3
"""deliver.py -- from raw/s1 (g 0..51) and raw/s2 (g 52..129) build frames/g_%04d.png, take.mkv, meta.json, cues.json,
contact.jpg.   python3 deliver.py"""
import os, sys, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))

G_S2, G_S3, H_OUT = 52, 122, 8
FIRST, LAST = 0, G_S3 + H_OUT - 1
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)

src = {}
for g in range(FIRST, LAST + 1):
    s = 1 if g < G_S2 else 2
    shutil.copyfile(os.path.join(RAW, "s%d" % s, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = "s%d" % s

rows = {}
for s in (1, 2):
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-frames:v", str(LAST - FIRST + 1), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)

meta = {"take": "s01", "shots": [1, 2], "g0": 0, "g1": G_S3, "first_g": FIRST, "n_frames": LAST - FIRST + 1,
        "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "dissolve", "frames": 12, "note": "handle g 122..129 rendered in 3D (shot 2 camera continues)"},
        "internal": [{"at": G_S2, "type": "cut", "from_shot": 1, "to_shot": 2}],
        "shot_ranges": {"1": [0, G_S2 - 1], "2": [G_S2, G_S3 - 1]},
        "set": "v3/set3d3/harbor.py", "light": "WINTER", "paint": 0, "seep": 1.0, "samples": 12, "resolution": [720, 1280],
        "threads": 2, "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, LAST + 1, "harbour winter ambience at the tank foot: light wind, distant gulls, far harbour bell (bed under shots 1-2)", "ambience")
add(0, 19, "tin bucket scraped across the frozen yard into place under the seam (short metallic scrape, stops g 19)", "bucket_scrape")
add(0, 22, "the glossy molasses bead creeps down the seep strip (tiny wet slide, optional)", "drip_slide")
add(30, 30, "DRIP lands in the empty tin bucket: hollow 'tink-plip' (t 0.9)", "drip", impact_frame=30)
add(33, 51, "snap pull-up away from the bucket: whoosh out; the tank groans low, long and metallic as it towers over him", "camera_snap", peak_frame=41, peak_time=t(41))
add(36, 66, "tank groan: deep riveted-steel creak under the pull-up (swells to g 46, decays past the cut)", "groan")
add(60, 60, "second drip lands in the bucket (far, soft plip; under shot 2)", "drip", impact_frame=60)
add(G_S2, G_S2, "hard cut to the foreman at the tank base", "cut")
add(63, 63, "foreman jabs the brush up at the tank (cloth rustle, small whoosh)", "gesture")
add(71, 71, "second jab (cloth rustle, small whoosh)", "gesture")
add(78, 86, "foreman shoves the brush and the paint pot at tommy: whoosh; the pot's wire bail clanks against the tin", "whoosh")
add(84, 84, "paint pot clank (bail on tin, short)", "clank", impact_frame=84)
add(83, 89, "snap punch-in on the brush (short whoosh in), lands g 87 on 'สีมาทาทับแทน'", "camera_snap", peak_frame=86, peak_time=t(86))
add(G_S3 - 6, G_S3 + 6, "dissolve to the Boston establishing (s03)", "dissolve")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(i * (LAST - FIRST) / 15.0)) + FIRST for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
