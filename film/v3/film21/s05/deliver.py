#!/usr/bin/env python3
"""deliver.py -- encode take.mkv from raw/s13 + raw/s14, write meta.json, cues.json, contact.jpg, phone_sheet.jpg.
usage: python3 deliver.py"""
import os, glob, json, subprocess, shutil
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
FIRST, LAST = 787, 890
FR = os.path.join(HERE, "frames"); os.makedirs(FR, exist_ok=True)
miss = []
for g in range(FIRST, LAST + 1):
    sh = 13 if g < 837 else 14
    src = os.path.join(HERE, "raw", "s%d" % sh, "g_%04d.png" % g)
    if not os.path.exists(src): miss.append(g); continue
    dst = os.path.join(FR, "g_%04d.png" % g)
    if not os.path.exists(dst): shutil.copyfile(src, dst)
assert not miss, "missing frames %s" % miss
out = os.path.join(HERE, "take.mkv")
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-start_number", str(FIRST), "-i", os.path.join(FR, "g_%04d.png"),
                       "-c:v", "libx264rgb", "-crf", "6", "-preset", "slow", out])
size = os.path.getsize(out)
if size > 45e6:
    subprocess.check_call("split -b 40M take.mkv take.mkv.part", shell=True, cwd=HERE)
meta = dict(take="s05", name="nickname", shots=[13, 14], g0=793, g1=885, first_g=FIRST, n_frames=LAST - FIRST + 1,
            transition_in=dict(type="cut", frames=0), internal_cuts=[837], handle_frames=6, fps=30, size=[720, 1280],
            take_mkv_bytes=size)
json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
# contact sheet: every 6th frame, 8 columns, cut marked
ims = []
for g in range(FIRST, LAST + 1, 6):
    im = Image.open(os.path.join(FR, "g_%04d.png" % g)).convert("RGB").resize((180, 320))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 52, 14], fill=(0, 0, 0)); d.text((3, 2), "g%d" % g, fill=(255, 255, 255))
    d.line([0, 220, 180, 220], fill=(0, 255, 255)); ims.append(im)
cols = 9; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (180 * cols, 320 * rows), (20, 20, 20))
for i, im in enumerate(ims): sh.paste(im, ((i % cols) * 180, (i // cols) * 320))
sh.save(os.path.join(HERE, "contact.jpg"), quality=88)
# phone sheet: 360x640 tiles, 1 frame / 0.5 s
ims = []
for g in range(FIRST, LAST + 1, 15):
    ims.append(Image.open(os.path.join(FR, "g_%04d.png" % g)).convert("RGB").resize((360, 640)))
sh = Image.new("RGB", (360 * len(ims), 640))
for i, im in enumerate(ims): sh.paste(im, (i * 360, 0))
sh.save(os.path.join(HERE, "phone_sheet.jpg"), quality=88)
print("delivered", meta)
