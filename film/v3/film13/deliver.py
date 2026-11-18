#!/usr/bin/env python3
"""deliver.py <take>  (s04|s07): raw/g_%04d.png -> frames/, take.mkv, meta.json, cues.json, contact.jpg (run inside the take folder via cwd arg)."""
import os, sys, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
take = sys.argv[1]; HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), take)
CFG = {
 "s04": dict(shots=[4, 5, 6], g0=162, g1=367, first=156, last=372, cuts=[237, 303], light="RAIN", preset="street_wide (own cameras per shot)",
             cues=[(5.3, 6.9, "rain bed (shots 4-6)"), (7.8, 2.2, "cart creak + wheel sinking splash, horse struggle"), (10.0, 2.1, "boots on planks, a squelch + comic slurp as the gentleman's boot sinks")]),
 "s07": dict(shots=[7, 8, 9], g0=367, g1=594, first=361, last=599, cuts=[447, 513], light="DAY", preset="street_wide (own cameras per shot)",
             cues=[(12.2, 2.6, "shovels scrape + dirt thuds (workers filling the street)"), (14.9, 2.2, "shovels on the fill mound by the stair"), (17.0, 2.7, "footsteps on gravel, plans rustle")]),
}[take]
fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
rows = []
for g in range(CFG["first"], CFG["last"] + 1):
    shutil.copyfile(os.path.join(HERE, "raw", "g_%04d.png" % g), os.path.join(fr, "g_%04d.png" % g))
    rows.append(json.load(open(os.path.join(HERE, "raw", "g_%04d.json" % g))))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(CFG["first"]), "-i", os.path.join(fr, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(HERE, "take.mkv"))
if sz > 45e6:
    subprocess.run("cd %s && split -b 40M take.mkv take.mkv.part && rm take.mkv" % HERE, shell=True, check=True)
walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
meta = dict(take=take, film=13, shots=CFG["shots"], g0=CFG["g0"], g1=CFG["g1"], first_g=CFG["first"], n_frames=len(rows), handle_in=CFG["g0"] - CFG["first"], handle_out=CFG["last"] + 1 - CFG["g1"],
            transition_in=dict(type="cut", frames=0), light=CFG["light"], preset=CFG["preset"], cuts_inside=CFG["cuts"], dof="none", samples=12, resolution=[720, 1280], fps=30, threads=2,
            s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2),
            set="v3/set3d13/chicago.py street (runtime: cast13 cards for crowd roles, own cameras, hooks keyed every frame)", cast="v3/cast13",
            take_mkv_split=sz > 45e6)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
json.dump([dict(t=a, dur=d, label=l) for a, d, l in CFG["cues"]], open(os.path.join(HERE, "cues.json"), "w"), indent=1, ensure_ascii=False)
idx = list(range(0, len(rows), 8)); W, H = 180, 320; cols = 10
sh = Image.new("RGB", (cols * W, ((len(idx) + cols - 1) // cols) * (H + 12)), (20, 20, 20)); d = ImageDraw.Draw(sh)
for k, i in enumerate(idx):
    im = Image.open(os.path.join(fr, "g_%04d.png" % (CFG["first"] + i))).resize((W, H)); x, y = (k % cols) * W, (k // cols) * (H + 12)
    sh.paste(im, (x, y)); d.text((x + 2, y + H), "g%d" % (CFG["first"] + i), fill=(230, 230, 230)); d.line([(x, y + int(H * 880 / 1280)), (x + W, y + int(H * 880 / 1280))], fill=(0, 200, 255))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
print(meta)
