#!/usr/bin/env python3
"""deliver.py -- raw/g_*.png -> frames/ (per-shot complementary grade), meta.json, cues.json, contact.jpg, compare.jpg, take.mkv.
Grade (numpy, per shot, deterministic): AFTERNOON shots (22, 24) = gold highlights + blue-violet shadows (the cool counter-colour);
MORNING / dawn shots (23, 25) = cooler overall, blue shadows, whites kept white (the steam)."""
import os, json, glob, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RAW, OUT = os.path.join(HERE, "raw"), os.path.join(HERE, "frames")
os.makedirs(OUT, exist_ok=True)
G0, G1, H = 1238, 1458, 6
RANGES = {22: (1232, 1310), 23: (1311, 1343), 24: (1344, 1387), 25: (1388, 1463)}
FIRST, LAST = G0 - H, G1 + H - 1


def shot_of(g):
    return [s for s, (a, b) in RANGES.items() if a <= g <= b][0]


def grade(img, shot):
    x = img.astype(np.float32) / 255.0
    lum = (0.299 * x[..., 0] + 0.587 * x[..., 1] + 0.114 * x[..., 2])[..., None]
    sh = np.clip(1.0 - lum / 0.55, 0, 1) ** 1.5          # shadow weight
    hi = np.clip((lum - 0.55) / 0.45, 0, 1)              # highlight weight
    if shot in (22, 24):                                   # afternoon: gold vs blue-violet
        x = x + sh * np.array([-0.035, -0.010, 0.060]) + hi * np.array([0.025, 0.010, -0.030])
        x = (x - 0.5) * 1.06 + 0.5
    else:                                                  # dawn: cool
        x = x * np.array([0.93, 0.98, 1.06]) + sh * np.array([-0.02, 0.0, 0.06])
        wht = np.clip((lum - 0.80) / 0.2, 0, 1)            # keep the steam white
        x = x * (1 - wht) + (lum * np.ones(3)) * wht * 1.0
    return (np.clip(x, 0, 1) * 255 + 0.5).astype(np.uint8)


rows = {}
for g in range(FIRST, LAST + 1):
    im = np.array(Image.open(os.path.join(RAW, "g_%04d.png" % g)).convert("RGB"))
    Image.fromarray(grade(im, shot_of(g))).save(os.path.join(OUT, "g_%04d.png" % g))
    rows[g] = json.load(open(os.path.join(RAW, "g_%04d.json" % g)))
walls = [r["wall"] for r in rows.values()]; cpus = [r["cpu"] for r in rows.values()]
N = LAST - FIRST + 1

meta = {"take": "s22", "film": "6b", "shots": [22, 23, 24, 25], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0},
        "transition_out": {"type": "cut", "frames": 0},
        "shot_ranges": {"22": [G0, 1310], "23": [1311, 1343], "24": [1344, 1387], "25": [1388, G1 - 1]},
        "handles": {"in": [FIRST, G0 - 1], "out": [G1, LAST]},
        "internal_cuts": [1287, 1311, 1344, 1388, 1428],
        "events": {"kit_worried_to_determined": 1259, "punch_in_loaf": 1287, "beam_settles_level": [1311, 1330],
                   "beam_rises": [1348, 1366], "tag_flip_500_to_480": [1361, 1367], "big_steam": [1388, 1463], "crane_up": 1428},
        "set": "v3/set3d6/bakery.py: 22 + 24 AFTERNOON (steam 0), 23 + 25 MORNING (steam 0.35 / 1.5); set_scale keyed per frame (23 settle "
               "to level, 24 rise to -8); extra billboard steam puffs (emission cards, shot.py Puffs) in 23 and 25",
        "props": "parchment tag PropCard '500 ก.' / red '480 ก.' (Kanit Black via SVG -> Chromium raster), parented to the loaf pan",
        "grade": "deliver.py per-shot numpy grade: afternoon gold highlights + blue-violet shadows; dawn cool, whites kept white",
        "dof": "none (cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) before every render)",
        "narration": "film6b/audio/narration.wav at +0.10 s", "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2)}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=round(g0 / 30.0, 3), duration=round(max(0, g1 - g0) / 30.0, 3), frame=g0, end_frame=g1, kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, 1310, "empty bakery in the afternoon: quiet, a fly buzzing, distant street murmur", "ambience")
add(1259, 1265, "kit's eyes narrow (determined): small low 'hmm' sting", "accent", peak_frame=1259)
add(1287, 1290, "punch-in on the loaf held up: quick whoosh", "transition", peak_frame=1287)
add(1311, 1311, "cut to dawn (cool): soft morning birds", "cut")
add(1311, 1330, "brass balance wobbles and settles level: light metallic tick-tick", "prop", peak_frame=1313)
add(1330, 1336, "'500 ก.' tag: tiny bright ding", "accent", peak_frame=1330)
add(1344, 1344, "cut to afternoon (gold)", "cut")
add(1348, 1366, "loaf pan rises, weights pan clunks down: rising slide whistle + clunk", "prop", peak_frame=1364)
add(1361, 1367, "tag flips to red '480 ก.': paper flip + low 'bonk'", "accent", peak_frame=1364)
add(1388, LAST, "fresh loaves at dawn: soft hiss of steam, warm whoosh rising with the crane", "ambience")
add(1428, 1428, "cut: crane up into the white steam cloud", "cut")
json.dump(dict(take="s22", fps=30, note="time = film seconds (g / 30); narration film6b/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [int(round(FIRST + i * (N - 1) / 15.0)) for i in range(16)]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d  %.2f s  shot %d" % (g, g / 30.0, shot_of(g)), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

refs = sorted(glob.glob(os.path.join(PROJ, "analysis", "sheets", "pink_0.jpg")))
P = [1270, 1300, 1330, 1375, 1440]
C = Image.new("RGB", (len(P) * 270 + 540, 480), (16, 12, 20))
for i, g in enumerate(P):
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).resize((270, 480), Image.LANCZOS), (i * 270, 0))
if refs:
    r = Image.open(refs[0]).convert("RGB")
    C.paste(r.crop((0, 0, 900, 800)).resize((540, 480), Image.LANCZOS), (len(P) * 270, 0))
C.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i",
                os.path.join(OUT, "g_%04d.png"), "-frames:v", str(N), "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered %d frames g %d..%d; mean wall %.2f s, cpu %.2f s; mkv %.1f MB" % (N, FIRST, LAST, np.mean(walls), np.mean(cpus),
                                                                                  os.path.getsize(mkv) / 1e6))
