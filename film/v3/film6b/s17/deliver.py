#!/usr/bin/env python3
"""deliver.py -- from raw/s17..s21 build frames/g_%04d.png (g 958..1243), meta.json, cues.json, contact.jpg, compare.jpg and
take.mkv (libx264rgb crf 6, all frames).  python3 deliver.py"""
import os, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RANGES = {17: (958, 1028), 18: (1029, 1082), 19: (1083, 1131), 20: (1132, 1163), 21: (1164, 1243)}
G0, G1, H = 964, 1238, 6
FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for s, (a, b) in RANGES.items():
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s%d" % s, "g_%04d.png" % g)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(s)
        rows.append(json.load(open(p[:-4] + ".json")))
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]
N = LAST - FIRST + 1
assert len(src) == N

shots = {"17": [964, 1028], "18": [1029, 1082], "19": [1083, 1131], "20": [1132, 1163], "21": [1164, 1237]}
meta = {"take": "s17", "film": "6b", "shots": [17, 18, 19, 20, 21], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0},
        "transition_out": {"type": "cut", "frames": 0},
        "transitions": [{"at": G0, "type": "cut", "handle": [FIRST, G0 - 1]}, {"at": 1029, "type": "cut"}, {"at": 1083, "type": "cut"},
                        {"at": 1132, "type": "cut", "note": "hard cut on the needle (drum)"}, {"at": 1164, "type": "cut"},
                        {"at": G1, "type": "cut", "handle": [G1, LAST]}],
        "shot_ranges": shots,
        "inner_cuts": {"17": "snap push g 1017-1021 (swap to inspector_royal on the blink g 1016/1017)", "18": "punch-in g 1062",
                       "20": "snap punch-in on 'ขาด!' g 1157 (label flares)", "21": "cut to the low wide at the pillory g 1197"},
        "events": {"hood_drop": [1007, 1016], "royal_reveal_on_พระราชา": 1017, "henry_counts_1_to_10": [1031, 1060],
                   "tag_12_punch_in": 1062, "หนึ่งโหล": 1069, "pour_loaves_land": [1094, 1122], "beam_settles_short": -7,
                   "ขาด_flare": 1157, "drag_start": 1164, "pillory_wide": 1197},
        "set": "v3/set3d6/bakery.py: market AFTERNOON (shots 17, 19, 20, 21), bakery AFTERNOON steam 0.15 (shot 18); custom cameras; "
               "shot 20 adds a blue enamel dial + red needle (PropCards, needle = 3 x beam tilt) in front of the balance pivot; shot 21 "
               "adds the Thai sign board 'ห้ามขายขาดน้ำหนัก!' on the pillory; shot 18 basket card (12 loaves) + tag '12 ก้อน'",
        "signs": "Kanit Black (film/fonts) embedded in the SVG, rasterised by Chromium (v3/set3d/raster.js)",
        "dof": "none (cam.data.dof.use_dof False + B.setup_dof(scene, None, None, cam=cam) before every render)",
        "denoiser": "OpenImageDenoise, albedo+normal, prefilter FAST",
        "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "cast": "v3/cast6: inspector (hooded) -> inspector_royal, henry (count / smug / dragged pale + sweat), guard1, guard2, woman1, man1",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in sorted(src.items())}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, 1029, "afternoon market square: low murmur, distant chickens, a brazier crackle", "ambience")
add(964, 1000, "slow footsteps on cobbles, cloak swish (the hooded stranger)", "foley")
add(1007, 1016, "hood thrown back: heavy cloth whoosh", "foley", peak_frame=1010)
add(1017, 1022, "royal reveal: short brass fanfare sting + snap-zoom whoosh", "accent", peak_frame=1017)
add(1029, 1083, "bakery interior: oven crackle", "ambience")
for g in range(1031, 1061, 3):
    add(g, g + 1, "finger count tick", "accent")
add(1062, 1064, "punch-in whoosh on the '12 ก้อน' tag; smug 'hmph'", "accent", peak_frame=1062)
add(1083, 1132, "market ambience, the balance creaks", "ambience")
for k in range(12):
    s = 1088 + int(round(2.5 * k))
    add(s + 6, s + 7, "loaf %d thuds onto the brass pan" % (k + 1), "prop")
add(1132, 1164, "tense held note, chains creak, needle tremble", "music")
add(1157, 1160, "BIG drum hit on 'ขาด!' (label flares)", "accent", peak_frame=1157)
add(1164, LAST + 1, "crowd jeers and laughter, guards' boots, henry's heels scraping on cobbles", "ambience")
add(1197, 1199, "cut to the pillory: crowd 'ooh'", "accent", peak_frame=1197)
json.dump(dict(take="s17", fps=30, note="time = film seconds (g / 30); narration film6b/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [958, 980, 1006, 1012, 1017, 1028, 1040, 1065, 1083, 1100, 1120, 1132, 1157, 1170, 1200, 1243]
w, h, lab, cols = 270, 480, 18, 8
S = Image.new("RGB", (cols * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    dr.text((x + 4, y + 3), "g %d %.2fs shot %s%s" % (g, g / 30.0, src[g], " handle" if g < G0 or g >= G1 else ""), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: four of our frames beside reference sheet crops (film/analysis/sheets, 1 frame per second of the hit shorts)
ref = Image.open(os.path.join(PROJ, "analysis", "sheets", "pink_0.jpg")).convert("RGB")
cw, ch = ref.width // 6, ref.height // 6
crops = [ref.crop((5 * cw, 1 * ch, 6 * cw, 2 * ch)), ref.crop((1 * cw, 3 * ch, 2 * cw, 4 * ch)), ref.crop((3 * cw, 0, 4 * cw, ch)),
         ref.crop((3 * cw, 4 * ch, 4 * cw, 5 * ch))]
w, h = 270, 480
Cm = Image.new("RGB", (8 * w, h + 20), (16, 12, 20)); dr = ImageDraw.Draw(Cm)
for i, g in enumerate((1028, 1072, 1157, 1185)):
    Cm.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (2 * i * w, 20))
    dr.text((2 * i * w + 4, 4), "s17 g %d" % g, fill=(255, 255, 255))
    Cm.paste(crops[i].resize((w, h), Image.LANCZOS), ((2 * i + 1) * w, 20))
    dr.text(((2 * i + 1) * w + 4, 4), "ref sheet pink_0", fill=(255, 220, 160))
Cm.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("delivered", N, "frames + take.mkv (%.1f MB); mean wall %.2f s, cpu %.2f s" % (os.path.getsize(mkv) / 1e6, np.mean(walls), np.mean(cpus)))
