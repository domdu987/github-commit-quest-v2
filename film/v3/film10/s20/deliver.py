#!/usr/bin/env python3
"""deliver.py -- raw/s<id>/g_*.png -> frames/, take.mkv, meta.json, cues.json, contact.jpg.   python3 deliver.py"""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); TAKE = os.path.basename(HERE)
sys.path.insert(0, HERE)
CFG = {
 "s20": dict(shots={20: (1422, 1529), 21: (1530, 1632)}, g0=1428, g1=1627, in_=6, out=6, film_end=False,
   cuts=[1530], events={"binoculars_up": [1422, 1436], "lowered": [1436, 1450], "jaw_drop_hold": [1450, 1529], "painter_grins": [1428, 1529],
   "cut_to_harbour_wide": 1530, "harbour_dazzle_0_to_1": [1536, 1617]},
   cues=[(1428, 1530, "open sea, convoy: low swell, gulls, steady engine throb, a thin wind on the bridge wing", "ambience"),
         (1440, 1452, "binoculars lowered with a rattle of the leather strap", "prop"),
         (1450, 1458, "stunned gasp / jaw-drop sting (no speech)", "foley"),
         (1530, 1627, "dockyard in daylight: gulls, distant hammering, ship sirens one after another as each ship flips to dazzle", "ambience")]),
 "s22": dict(shots={22: (1621, 1709), 23: (1710, 1820)}, g0=1627, g1=1815, in_=6, out=5, film_end=True,
   cuts=[1710], events={"admiral_and_painter_look_at_grey_ship": [1621, 1709], "cut_to_plank": 1710, "stripe_painting": [1710, 1800], "hard_cut_on_eng": [1797, 1800]},
   cues=[(1627, 1710, "quiet dockyard, gulls; a single wry tuba note when the grey ship is seen", "ambience"),
         (1710, 1815, "scrape of a big brush on the iron hull, drips into the bucket, the plank creaks on its ropes, a sheepish cough", "foley")]),
}[TAKE]
OUT = os.path.join(HERE, "frames"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
first = min(a for a, b in CFG["shots"].values()); last = max(b for a, b in CFG["shots"].values())
rows = []; src = {}
for sid, (a, b) in CFG["shots"].items():
    for g in range(a, b + 1):
        shutil.copyfile(os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); src[g] = sid
        rows.append(json.load(open(os.path.join(HERE, "raw", "s%d" % sid, "g_%04d.json" % g))))
n = last - first + 1
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(first), "-i", os.path.join(OUT, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(HERE, "take.mkv"))
if sz > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE)
heads = [(r["g"], h["y"]) for r in rows for h in r["heads"].values()]
meta = dict(take=TAKE, film=10, shots=sorted(CFG["shots"]), first_g=first, n_frames=n, g0=CFG["g0"], g1=CFG["g1"], handle_in=CFG["g0"] - first, handle_out=last - CFG["g1"] + 1,
            transition_in={"type": "cut", "frames": 0}, cuts=CFG["cuts"], shot_ranges={str(k): list(v) for k, v in CFG["shots"].items()}, events=CFG["events"],
            set="v3/set3d10/harbour.py (unmodified); runtime: placeholder bgcards hidden, cast10 figures added", dof="none", samples=12, resolution=[720, 1280], fps=30,
            s_per_frame_wall_mean=round(float(np.mean([r["wall"] for r in rows])), 2), s_per_frame_cpu_mean=round(float(np.mean([r["cpu"] for r in rows])), 2),
            take_mkv_bytes=sz, frame_source={str(g): str(v) for g, v in src.items()})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
json.dump(dict(take=TAKE, fps=30, cues=[dict(time=round(a / 30, 3), duration=round((b - a) / 30, 3), frame=a, end_frame=b, kind=k, label=l) for a, b, l, k in CFG["cues"]]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
gs = list(range(first, last + 1, 8))[:24]
tw, th = 180, 320; cols = 8; rws = (len(gs) + cols - 1) // cols
sh = Image.new("RGB", (cols * tw, rws * th), "black")
for i, g in enumerate(gs):
    im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).resize((tw, th)); d = ImageDraw.Draw(im); y = int(880 / 4); d.line([(0, y), (tw, y)], fill=(0, 255, 255)); d.text((3, 3), str(g), fill=(255, 255, 255))
    sh.paste(im, ((i % cols) * tw, (i // cols) * th))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
print("delivered", TAKE, first, last, n, "frames", sz, "bytes")
