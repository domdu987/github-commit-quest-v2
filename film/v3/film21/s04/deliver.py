#!/usr/bin/env python3
"""deliver.py -- s04: collect raw/table + raw/bank into frames/g_%04d.png, encode take.mkv, write meta.json, cues.json, contact.jpg."""
import os, sys, json, glob, shutil, subprocess
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FIRST, LAST = 535, 799
fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
miss = []
for g in range(FIRST, LAST + 1):
    src = os.path.join(HERE, "raw", "table" if g < 642 else "bank", "f_%04d.png" % g)
    if not os.path.exists(src):
        miss.append(g); continue
    shutil.copyfile(src, os.path.join(fr, "g_%04d.png" % g))
if miss:
    sys.exit("missing frames: %s" % miss[:20])
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(fr, "g_%04d.png"),
                "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", os.path.join(HERE, "take.mkv")], check=True)
sz = os.path.getsize(os.path.join(HERE, "take.mkv"))
if sz > 45e6:
    subprocess.run("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE, check=True)
meta = dict(take="s04", film=21, shots=[10, 11, 12], first_g=FIRST, n_frames=LAST - FIRST + 1, g0=542, g1=793, handle_in=7, handle_out=6,
            transition_in=dict(type="dissolve", frames=11), internal_cuts=[642, 707],
            shot_ranges={"10": [542, 641], "11": [642, 706], "12": [707, 793]}, presets={"10": "camp_table", "11": "camp_bank", "12": "camp_bank"},
            events=dict(coin_counting=[542, 589], looks_up=[590, 611], laugh_start=612, laugh_bounce=[612, 641], lipsync=[642, 791], purse_slap=709,
                        arm_at_bridge=[725, 744], chin_up=[772, 793]),
            samples=int(os.environ.get("SAMPLES", "24")), resolution=[720, 1280], fps=30, denoiser="OpenImageDenoise",
            dof="none", lens=dict(camp_table=22.0, camp_bank=26.0),
            frame_source={"table": [535, 641], "bank": [642, 799]})
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
cues = [
    (542, 588, "foley", "gold coins clink one by one into the open iron-bound chest; the little scale creaks and rocks"),
    (550, 641, "ambience", "English camp morning: tent canvas flapping, a distant horse, muffled voices, the river hush"),
    (612, 641, "sfx", "Cressingham bursts into a big fat belly laugh (laugh + wheeze), the chest rattles and the scale jiggles as he bounces"),
    (642, 706, "voice-fx", "mocking quote 'ชาวนาบนเนินไม่กี่คน' in his voice; a boastful tone"),
    (709, 712, "sfx", "slap on the leather coin purse, coins jingle inside (g 709)"),
    (725, 744, "sfx", "short cloth whoosh as the arm is flung at the bridge"),
    (772, 793, "sfx", "smug little hum / chuckle as he puts his thumbs in the belt"),
]
json.dump(dict(take="s04", fps=30, note="time = film seconds (g / 30)", cues=[dict(time=round(a / 30, 3), duration=round((b - a + 1) / 30, 3), frame=a, end_frame=b, kind=k, label=l) for a, b, k, l in cues]),
          open(os.path.join(HERE, "cues.json"), "w"), indent=1)
# contact sheet: 20 frames, cyan line at y 880
gs = [535, 542, 560, 580, 600, 612, 625, 641, 642, 660, 690, 706, 707, 715, 727, 745, 760, 775, 793, 799]
tw, th = 180, 320
S = Image.new("RGB", (tw * 10, th * 2), (16, 16, 20))
for k, g in enumerate(gs):
    im = Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB")
    d = ImageDraw.Draw(im); d.line([(0, 880), (720, 880)], fill=(0, 255, 255), width=3)
    S.paste(im.resize((tw, th), Image.LANCZOS), ((k % 10) * tw, (k // 10) * th))
S.save(os.path.join(HERE, "contact.jpg"), quality=90)
print("delivered", sz / 1e6, "MB")
