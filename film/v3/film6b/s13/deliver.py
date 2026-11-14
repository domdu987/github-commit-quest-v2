#!/usr/bin/env python3
"""deliver.py -- take s13 of film 6b: raw/s13..s16 -> frames/g_%04d.png (g 616..969), meta.json, cues.json, contact.jpg,
compare.jpg (final frames beside reference-short frames) and take.mkv (libx264rgb crf 6).  python3 deliver.py"""
import os, json, glob, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
RANGES = {13: (616, 734), 14: (735, 796), 15: (797, 878), 16: (879, 969)}
G0, G1, H = 622, 964, 6
FIRST, LAST = G0 - H, G1 + H - 1
OUT = os.path.join(HERE, "frames"); os.makedirs(OUT, exist_ok=True)

src, rows = {}, []
for shot, (a, b) in RANGES.items():
    for g in range(a, b + 1):
        p = os.path.join(HERE, "raw", "s%d" % shot, "g_%04d.png" % g)
        shutil.copyfile(p, os.path.join(OUT, "g_%04d.png" % g)); src[g] = str(shot)
        rows.append(json.load(open(p[:-4] + ".json")))
N = LAST - FIRST + 1
assert len(src) == N
walls = [m["wall"] for m in rows]; cpus = [m["cpu"] for m in rows]

meta = {"take": "s13", "film": "6b", "shots": [13, 14, 15, 16], "g0": G0, "g1": G1, "first_g": FIRST, "n_frames": N,
        "handle_in": H, "handle_out": H,
        "transition_in": {"type": "cut", "frames": 0}, "transition_out": {"type": "cut", "frames": 0},
        "shot_ranges": {"13": [622, 734], "14": [735, 796], "15": [797, 878], "16": [879, 963]},
        "internal_cuts": {"13b_frontal_count": 668, "14": 735, "14_punch_in": 772, "15": 797, "15_punch_in_lipsync": 842,
                          "16": 879, "16_kit_two_shot": 945},
        "events": {"pop_1_nueng": 697, "pop_2_song": 712, "pop_3_saam": 724, "bubble_chang_pe": 787,
                   "henry_laugh": [797, 841], "henry_lipsync": [842, 874], "pluck_13th": [893, 914, 935], "kit_watches": [945, 969]},
        "plan_deviation": "shot 13/14 boundary moved from g 702 (23.40 s) to g 735 (24.50 s): the spoken count 'หนึ่ง สอง สาม' is at "
                          "23.12 / 23.63 / 24.02 s in narration.wav, so the heads pop inside shot 13 as the plan's picture asks",
        "set": "v3/set3d6/bakery.py: market MORNING (3D pillory + platform + lamps hidden; three 2D pillories = baker2 x3 with pose key "
               "pillory / cast6.pillory_svg empty boards, a beam + Thai plank sign), bakery MORNING (hand balance hidden, cool blue "
               "area fill from the street side as counter-colour, steam 0.2 / 0.35)",
        "signs": "signs.py (PIL + raqm, fonts/Kanit_900Black.ttf): plank 'ห้ามขายขาดน้ำหนัก!', count pops 'หนึ่ง!' 'สอง!' 'สาม!', bubble 'ชั่งเป๊ะ!'",
        "dof": "none (common.Take: use_dof False + setup_dof(None) before every render)",
        "narration": "film6b/audio/narration.wav at +0.10 s; captions film6b/script/captions.json",
        "samples": 12, "resolution": [720, 1280], "threads": 2, "fps": 30,
        "s_per_frame_wall_mean": round(float(np.mean(walls)), 2), "s_per_frame_cpu_mean": round(float(np.mean(cpus)), 2),
        "frame_source": {str(g): v for g, v in sorted(src.items())}}
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)

t = lambda g: round(g / 30.0, 3)
ev = []


def add(g0, g1, label, kind, **kw):
    e = dict(time=t(g0), duration=round(max(0, g1 - g0) / 30.0, 3), frame=int(g0), end_frame=int(g1), kind=kind, label=label)
    e.update(kw); ev.append(e)


add(FIRST, 734, "market square, morning: crowd murmur, jeers, distant hooves", "ambience")
for k, g in enumerate((697, 712, 724)):
    add(g, g + 3, "head pops into pillory %d: wooden CLACK + comic 'boing'; yellow count word pops" % (k + 1), "accent", peak_frame=g)
add(735, 796, "pilloried bakers sob and protest (muffled, no words), crowd laughter under", "ambience")
add(787, 790, "speech bubble 'ชั่งเป๊ะ!' pops: pop accent", "accent", peak_frame=787)
add(797, 878, "bakery: oven crackle; henry's belly laugh 797-841 (no words), then he speaks the quote 842-874", "ambience")
add(842, 842, "punch-in on henry for 'พวกขี้โกงทั้งนั้น!' (whoosh)", "cut")
for g in (893, 914, 935):
    add(g, g + 2, "henry plucks the pale 13th loaf off a basket: wicker rustle + soft 'plip'", "prop", peak_frame=g)
add(945, 952, "widen to kit, deadpan: one dry 'tsk' accent", "accent", peak_frame=945)
json.dump(dict(take="s13", fps=30, note="time = film seconds (g / 30); narration film6b/audio/narration.wav at +0.10 s", cues=ev),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)

gs = [622, 645, 668, 690, 698, 713, 725, 734, 740, 770, 790, 800, 830, 850, 870, 885, 896, 918, 935, 950, 963, 969, 616, 964]
gs = sorted(set(gs))
w, h, lab, cols = 240, 427, 18, 8
rows_n = (len(gs) + cols - 1) // cols
S = Image.new("RGB", (cols * w, rows_n * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
for i, g in enumerate(gs):
    x, y = (i % cols) * w, (i // cols) * (h + lab)
    S.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
    tag = " handle" if (g < G0 or g >= G1) else ""
    dr.text((x + 4, y + 3), "g %d %.2fs sh%s%s" % (g, g / 30.0, src[g], tag), fill=(255, 255, 255))
S.save(os.path.join(HERE, "contact.jpg"), quality=88)

# compare: our frames beside reference-short sheet tiles (1 frame per second, film/analysis/sheets)
C = Image.new("RGB", (4 * 300, 533 + 20), (16, 12, 20)); dr = ImageDraw.Draw(C)
for i, g in enumerate((725, 790, 850, 960)):
    C.paste(Image.open(os.path.join(OUT, "g_%04d.png" % g)).convert("RGB").resize((300, 533), Image.LANCZOS), (i * 300, 20))
    dr.text((i * 300 + 4, 4), "s13 g %d" % g, fill=(255, 255, 255))
C2 = Image.open(os.path.join(PROJ, "analysis", "sheets", "pink_0.jpg")).convert("RGB")
cw = C2.width // 6
ref = C2.crop((cw * 4, 0, cw * 6, C2.height * 2 // 5))
ref = ref.resize((int(ref.width * 553 / ref.height), 553))
F = Image.new("RGB", (C.width + ref.width + 12, 553), (16, 12, 20)); F.paste(C, (0, 0)); F.paste(ref, (C.width + 12, 0))
ImageDraw.Draw(F).text((C.width + 16, 4), "ref sheet pink_0 (MCU faces, signs)", fill=(255, 220, 160))
F.save(os.path.join(HERE, "compare.jpg"), quality=88)

mkv = os.path.join(HERE, "take.mkv")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(OUT, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", mkv], check=True)
print("take.mkv %.1f MB, %d frames from g %d" % (os.path.getsize(mkv) / 1e6, N, FIRST))
