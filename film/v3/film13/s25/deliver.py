#!/usr/bin/env python3
"""deliver.py <take: s14|s15|s16> -- build frames/ from raw/, meta.json, cues.json, contact.jpg, phone_sheet.jpg, take.mkv for one of my takes."""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); TAKE = os.path.basename(HERE)
CFG = {
 "s24": dict(shot=24, g0=1537, g1=1602, set="front_stair build (street, DAY, lift 0.9 keyed), stair cut short with void; runtime: street lamp / gap lamp glows / planks / piles hidden; 8 cast13 worker cards (stand + cheer) inside the gap among the cribbing", light="DAY",
             cast="cast13 worker13_a/b/c stand + cheer cards in the gap, distant town cards", events={"slow_crane": [1531, 1607]},
             cues=[(0, 83, "ambience", "Chicago 1861 street, daylight, a quiet hush, distant town murmur, timber creaks under the raised hotel"),
                   (20, 40, "foley", "soft cheer from the tiny workers under the hotel")]),
 "s25": dict(shot=25, g0=1602, g1=1680, set="under_rows build (dense 5000-jack field, cut-away), CELLAR light; camera at the back looking down the rows toward -y; runtime deck of beams on the jacks, lamps, taller shafts; 3 rows of cast13 worker13_a/b/c turn-bar cards", light="CELLAR",
             cast="cast13 worker13_a/b/c turn_bar_A/B cards: 7 big foreground workers + ~60 behind, all flipping on one beat", events={"swing_1": [1612, 1624], "swing_2": [1650, 1662], "beams_step": [1612, 1662]},
             cues=[(0, 90, "ambience", "under the hotel: low reverberant cellar, oil lamp hiss, thousands of men"),
                   (16, 28, "foley", "one great metallic ratchet, all bars swinging together, timbers creak as the beams rise"),
                   (54, 66, "foley", "second unison ratchet, beams groan upward")]),
}[TAKE]
H = 6; G0, G1 = CFG["g0"], CFG["g1"]; FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)
rows = []
for g in range(FIRST, LAST + 1):
    shutil.copyfile(os.path.join(HERE, "raw", "g_%04d.png" % g), os.path.join(OUT, "g_%04d.png" % g)); rows.append(json.load(open(os.path.join(HERE, "raw", "g_%04d.json" % g))))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]; N = LAST - FIRST + 1
meta = dict(take=TAKE, film=13, shots=[CFG["shot"]], first_g=FIRST, n_frames=N, g0=G0, g1=G1, handle_in=H, handle_out=H,
            transition_in={"type": "cut", "frames": 0}, transition_out={"type": "cut", "frames": 0},
            shot_ranges={str(CFG["shot"]): [G0, G1 - 1]}, events=CFG["events"], set="v3/set3d13/chicago.py " + CFG["set"], light=CFG["light"], cast=CFG["cast"],
            dof="none (cam.data.dof.use_dof False)", denoiser="OpenImageDenoise (set pipeline)", narration="film13/audio/narration.wav at +0.10 s",
            samples=12, resolution=[720, 1280], threads=2, fps=30, s_per_frame_wall_mean=round(float(np.mean(walls)), 2), s_per_frame_cpu_mean=round(float(np.mean(cpus)), 2))
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = [dict(time=round((FIRST + a) / 30.0, 3), duration=round((b - a) / 30.0, 3), frame=FIRST + a, end_frame=FIRST + b, kind=k, label=l) for (a, b, k, l) in CFG["cues"]]
json.dump(dict(take=TAKE, fps=30, note="time = film seconds (g / 30); narration film13/audio/narration.wav at +0.10 s", cues=cues), open(os.path.join(HERE, "cues.json"), "w"), indent=1)
# contact sheet (every 6th frame) and phone sheet (360x640, every 0.5 s = 15 frames)
def sheet(step, w, cols, path):
    gs = list(range(FIRST, LAST + 1, step)); h = int(round(w * 1280 / 720)); rowsn = (len(gs) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rowsn * h), (20, 20, 24)); d = ImageDraw.Draw(S)
    for i, g in enumerate(gs):
        im = Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS); S.paste(im, ((i % cols) * w, (i // cols) * h)); d.text(((i % cols) * w + 4, (i // cols) * h + 4), str(g), fill=(255, 255, 0))
    S.save(path, quality=88)
sheet(6, 180, 8, os.path.join(HERE, "contact.jpg")); sheet(15, 360, 6, os.path.join(HERE, "phone_sheet.jpg"))
mk = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mk], check=True)
if os.path.getsize(mk) > 45 * 1024 * 1024:
    subprocess.run("cd %s && split -b 40M take.mkv take.mkv.part && rm take.mkv" % HERE, shell=True, check=True)
print("delivered", TAKE, FIRST, LAST, N, "frames", os.path.getsize(mk) if os.path.exists(mk) else "split")
