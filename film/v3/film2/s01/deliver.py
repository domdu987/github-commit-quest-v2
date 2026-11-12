#!/usr/bin/env python3
"""deliver.py -- from raw/s1, raw/s2, raw/s3 build frames/g_%04d.png (shot 2 -> 3 dissolve mixed in), meta.json, cues.json,
contact.jpg.  python3 deliver.py"""
import os, sys, json, glob, shutil
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "v2", "shots"))
from anim import smoothstep_mix

G_S2, G_S3, G_END, H_OUT, DISS = 67, 122, 211, 7, 12
D0 = G_S3 - DISS // 2            # 116: first mixed frame
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)


def raw(s, g):
    return os.path.join(RAW, "s%d" % s, "g_%04d.png" % g)


src = {}
for g in range(0, G_END + H_OUT):
    dst = os.path.join(OUT, "g_%04d.png" % g)
    if g < G_S2:
        shutil.copyfile(raw(1, g), dst); src[g] = "s1"
    elif g < D0:
        shutil.copyfile(raw(2, g), dst); src[g] = "s2"
    elif g < D0 + DISS:
        w = smoothstep_mix(g - D0 + 1, DISS)
        a = np.asarray(Image.open(raw(2, g)).convert("RGB"), dtype=np.float32)
        b = np.asarray(Image.open(raw(3, g)).convert("RGB"), dtype=np.float32)
        Image.fromarray(np.clip(a * (1 - w) + b * w + 0.5, 0, 255).astype(np.uint8)).save(dst); src[g] = "s2*%.3f+s3*%.3f" % (1 - w, w)
    else:
        shutil.copyfile(raw(3, g), dst); src[g] = "s3"

# per-frame stats from the render jsons
rows = {}
for s in (1, 2, 3):
    for js in glob.glob(os.path.join(RAW, "s%d" % s, "g_*.json")):
        m = json.load(open(js)); rows[(s, m["g"])] = m
walls = [m["wall"] for m in rows.values()]; cpus = [m["cpu"] for m in rows.values()]

meta = {"take": "s01", "shots": [1, 2, 3], "g0": 0, "g1": G_END, "handle_in": 0, "handle_out": H_OUT,
        "transition_in": {"type": "open", "frames": 0},
        "transition_out": {"type": "dissolve", "frames": 10, "note": "handle g 211..217 rendered in 3D (shot 3 camera continues)"},
        "internal": [{"at": G_S2, "type": "cut", "from_shot": 1, "to_shot": 2},
                     {"at": G_S3, "type": "dissolve", "frames": DISS, "mixed": [D0, D0 + DISS - 1], "from_shot": 2, "to_shot": 3,
                      "mix": "smoothstep P*P*(3-2P), P = i/(n+1); raw handles: shot 2 to g 129, shot 3 from g 114 (raw/)"}],
        "shot_ranges": {"1": [0, G_S2 - 1], "2": [G_S2, G_S3 - 1], "3": [G_S3, G_END - 1]},
        "set": "v3/set3d2/tower.py", "light": "DAY", "rod": "set_rod(1) throughout", "samples": 12, "resolution": [720, 1280],
        "threads": 2, "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in src.items()}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

# cues (film seconds = g / 30)
import importlib.util
sp = importlib.util.spec_from_file_location("shotmod", os.path.join(HERE, "shot.py"))
t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label); e.update(kw); ev.append(e)


add(0, G_END + H_OUT, "high wind on the top of the bell tower (bed under shots 1-3, louder in shot 1, softer in the square)", "ambience")
HITS = [12, 27, 42]
for i, g in enumerate(HITS):
    add(g, g, "hammer hit %d: iron hammer on the iron strap of the rod (sharp metal clank, ring tail); camera jolts" % (i + 1), "hammer_hit", impact_frame=g)
for g in range(HITS[-1] + 16, G_END + H_OUT, 16):
    if g < G_S2 + 1:
        add(g, g, "hammer hit during the pull-out (clank, already distant)", "hammer_hit_far", impact_frame=g)
    else:
        add(g, g, "tiny far clank: nico still hammering on the tower top (very soft, optional)", "hammer_hit_far", impact_frame=g)
add(44, 60, "snap pull-out up and away from the spire (big whoosh out), peak about g 51", "camera_snap", peak_frame=51, peak_time=t(51))
add(G_S2, G_S2, "hard cut to the square: padre, furious, pointing up at the tower", "cut")
add(100, 108, "snap punch-in on padre (short whoosh in), lands g 105 on 'thing choei loei'", "camera_snap", peak_frame=104, peak_time=t(104))
add(100, 113, "padre's pointing finger jabs harder (cloth rustle of the cassock sleeve)", "gesture")
add(D0, D0 + DISS, "dissolve to the town establishing", "dissolve")
add(G_S3, G_END + H_OUT, "town ambience: pigeons flutter, distant voices in the square, wind", "ambience")
add(138, 138, "'pi 1769' lands (title moment, optional soft sting)", "accent")
json.dump(dict(take="s01", fps=30, note="time = film seconds (g / 30); narration at +0.10 s", cues=ev), open(os.path.join(HERE, "cues.json"), "w"), indent=1)

# contact sheet: 16 evenly spaced final frames, label strip above each picture
gs = [int(round(i * (G_END + H_OUT - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  %s" % (g, g / 30.0, src[g][:12]), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)
print("delivered", len(src), "frames; mean wall %.2f s, cpu %.2f s" % (np.mean(walls), np.mean(cpus)))
