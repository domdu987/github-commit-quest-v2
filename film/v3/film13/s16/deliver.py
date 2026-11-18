#!/usr/bin/env python3
"""deliver.py <take: s14|s15|s16> -- build frames/ from raw/, meta.json, cues.json, contact.jpg, phone_sheet.jpg, take.mkv for one of my takes."""
import os, sys, json, shutil, subprocess, glob
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); TAKE = os.path.basename(HERE)
CFG = {
 "s14": dict(shot=14, g0=912, g1=975, set="street_wide build, DAY, lift 0; runtime trench (terrain faces removed, rim walls, 45 deg bank, plank ramp, timbered tunnel mouth), prop jack pile", light="DAY",
             cast="cast13 worker13_a/b/c carrying iron jacks (STORY13 worker_carry_jack, cycle 28 f)", events={"file_enters_trench": [906, 980], "camera_push": [906, 980]},
             cues=[(0, 75, "ambience", "Chicago 1861 street, daylight, distant town murmur, wind, a cart creaking far off"),
                   (0, 75, "foley", "heavy boots on plank ramp, iron jacks clanking against shoulders, steady rhythm of the file (one clank per step)"),
                   (30, 75, "foley", "hollow thud of boots down into the trench, a dry creak of timbers at the tunnel mouth")]),
 "s15": dict(shot=15, g0=975, g1=1041, set="under_rows build (dense field, cut-away), CELLAR; set_jack_count keyed 100 -> 1000 (g 997) -> 5000 (g 1012); one worker per 10 jacks (cast13 turn-bar cards A/B)", light="CELLAR",
             cast="cast13 worker13_a/b/c bar-pose cards, hidden when their jacks are not yet shown or their chin passes y 862", events={"count_100": [979, 979], "count_1000": [997, 997], "count_5000": [1012, 1012], "camera_crane_up": [969, 1046]},
             cues=[(0, 66, "ambience", "under the hotel: low reverberant cellar, oil lamp hiss, dust, distant men"),
                   (4, 6, "foley", "a handful of iron jacks set down, short metal clank (100)"),
                   (22, 26, "foley", "metal rattle multiplying, jacks clacking into place (1000)"),
                   (37, 66, "foley", "dense metallic rattle swelling to a roar (5000), rising whoosh as the camera rises")]),
 "s16": dict(shot=16, g0=1041, g1=1107, set="under_wide build, CELLAR; runtime: set's oil lamps rebuilt without the 2.6 D halos; ~520 worker cards (3 per aisle slot, A/B bar pose cycling slowly)", light="CELLAR",
             cast="cast13 pullman (cycle walk, derby, head turns, scale 0.78 for the 2.8 D crawlspace), foreman13 with whistle at the far end, worker13_a/b/c cards", events={"pullman_walks": [1035, 1112], "dolly_in": [1035, 1112]},
             cues=[(0, 66, "ambience", "cellar crowd: five hundred men waiting, low murmur, shuffling boots, lamp hiss, dripping"),
                   (0, 66, "foley", "pullman's footsteps on the plank aisle, one step every 14 frames"),
                   (30, 40, "foley", "a few jack bars clink as men settle their hands")]),
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
